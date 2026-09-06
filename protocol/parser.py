from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Literal


ALLOWED_TOOL = "openclaw"
ALLOWED_ACTIONS = {
    "browser_task",
    "website_check",
    "screenshot_task",
    "form_check",
    "local_file_task",
    "workflow_task",
    "note_task",
    "email_send",
}
ALLOWED_RISKS = {"low", "medium", "high"}
MAX_AI_RESPONSE_CHARS = 80_000
MAX_TOOL_CALL_CHARS = 20_000

TOOL_CALL_SCHEMA: dict[str, Any] = {
    "type": "object",
    "required": ["tool", "action", "objective", "risk", "needs_approval"],
    "properties": {
        "tool": {"type": "string", "enum": [ALLOWED_TOOL]},
        "action": {"type": "string", "enum": sorted(ALLOWED_ACTIONS)},
        "objective": {"type": "string", "minLength": 1},
        "inputs": {"type": "object"},
        "risk": {"type": "string", "enum": sorted(ALLOWED_RISKS)},
        "needs_approval": {"type": "boolean"},
        "expected_result": {"type": "string"},
    },
    "additionalProperties": False,
}


class ProtocolParseError(ValueError):
    pass


class FinalParseError(ProtocolParseError):
    pass


class ToolCallValidationError(ProtocolParseError):
    pass


class RiskGateError(ProtocolParseError):
    pass


class MaxStepError(ProtocolParseError):
    pass


@dataclass(frozen=True)
class ParsedProtocolResponse:
    kind: Literal["final", "tool_call"]
    raw_text: str
    final_text: str | None = None
    tool_call: dict[str, Any] | None = None
    warnings: list[str] = field(default_factory=list)


def parse_final(text: str) -> str:
    parsed = parse_protocol_response(text)
    if parsed.kind != "final" or not parsed.final_text:
        raise FinalParseError("latest_response_is_not_final")
    return parsed.final_text


def parse_protocol_response(text: str) -> ParsedProtocolResponse:
    raw = text or ""
    if len(raw) > MAX_AI_RESPONSE_CHARS:
        raise ProtocolParseError("ai_response_too_large")

    final_index = raw.rfind("FINAL:")
    tool_index = raw.find("TOOL_CALL:")
    if final_index < 0 and tool_index < 0:
        raise ProtocolParseError("missing_final_or_tool_call")

    warnings: list[str] = []
    if final_index >= 0 and tool_index >= 0:
        warnings.append("both_final_and_tool_call_present")

    if tool_index >= 0:
        tool_call = _parse_tool_call_json(raw[tool_index + len("TOOL_CALL:") :])
        tool_call = validate_tool_call_schema(tool_call)
        enforce_risk_gate(tool_call)
        return ParsedProtocolResponse(
            kind="tool_call",
            raw_text=raw,
            tool_call=tool_call,
            warnings=warnings,
        )

    final_text = raw[final_index + len("FINAL:") :].strip()
    if not final_text:
        raise FinalParseError("empty_final")
    return ParsedProtocolResponse(kind="final", raw_text=raw, final_text=final_text)


def validate_tool_call_schema(tool_call: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(tool_call, dict):
        raise ToolCallValidationError("tool_call_must_be_object")

    required = TOOL_CALL_SCHEMA["required"]
    for field_name in required:
        if field_name not in tool_call:
            raise ToolCallValidationError(f"missing_required_field:{field_name}")

    allowed_fields = set(TOOL_CALL_SCHEMA["properties"].keys())
    extra_fields = sorted(set(tool_call.keys()) - allowed_fields)
    if extra_fields:
        raise ToolCallValidationError(f"unknown_fields:{','.join(extra_fields)}")

    if tool_call.get("tool") != ALLOWED_TOOL:
        raise ToolCallValidationError("unknown_tool")

    action = tool_call.get("action")
    if action not in ALLOWED_ACTIONS:
        raise ToolCallValidationError("unknown_action")

    objective = tool_call.get("objective")
    if not isinstance(objective, str) or not objective.strip():
        raise ToolCallValidationError("invalid_objective")

    inputs = tool_call.get("inputs", {})
    if inputs is not None and not isinstance(inputs, dict):
        raise ToolCallValidationError("inputs_must_be_object")

    risk = tool_call.get("risk")
    if risk not in ALLOWED_RISKS:
        raise ToolCallValidationError("invalid_risk")

    if not isinstance(tool_call.get("needs_approval"), bool):
        raise ToolCallValidationError("needs_approval_must_be_boolean")

    expected_result = tool_call.get("expected_result")
    if expected_result is not None and not isinstance(expected_result, str):
        raise ToolCallValidationError("expected_result_must_be_string")

    normalized = dict(tool_call)
    normalized["objective"] = objective.strip()
    normalized["inputs"] = inputs or {}
    return normalized


def enforce_risk_gate(tool_call: dict[str, Any]) -> None:
    if tool_call.get("needs_approval") is True:
        raise RiskGateError("approval_required")
    if tool_call.get("risk") != "low":
        raise RiskGateError(f"risk_not_auto_allowed:{tool_call.get('risk')}")


def enforce_max_steps(current_step: int, max_steps: int) -> None:
    if current_step >= max_steps:
        raise MaxStepError("max_steps_exceeded")


def _parse_tool_call_json(text: str) -> dict[str, Any]:
    candidate = text.strip()
    if len(candidate) > MAX_TOOL_CALL_CHARS:
        raise ToolCallValidationError("tool_call_too_large")
    try:
        value, _ = json.JSONDecoder().raw_decode(candidate)
    except json.JSONDecodeError as exc:
        raise ToolCallValidationError(f"malformed_tool_call_json:{exc.msg}") from exc
    if not isinstance(value, dict):
        raise ToolCallValidationError("tool_call_must_be_object")
    return value
