import pytest
from protocol.parser import (MaxStepError, ProtocolParseError, RiskGateError, ToolCallValidationError, enforce_max_steps, parse_final, parse_protocol_response)

def test_parse_final_uses_latest_marker():
    assert parse_final("FINAL:\nfirst\n\nnoise\nFINAL:\nsecond") == "second"

def test_parse_final_rejects_missing_marker():
    with pytest.raises(ProtocolParseError):
        parse_final("hello")

def test_parse_valid_tool_call():
    parsed = parse_protocol_response(
        'TOOL_CALL:\n{"tool":"openclaw","action":"website_check",'
        '"objective":"Check danieldowork.com","inputs":{"url":"https://danieldowork.com"},'
        '"risk":"low","needs_approval":false,"expected_result":"status"}'
    )
    assert parsed.kind == "tool_call"
    assert parsed.tool_call is not None
    assert parsed.tool_call["action"] == "website_check"
    assert parsed.tool_call["inputs"]["url"] == "https://danieldowork.com"

def test_parse_valid_email_send_tool_call():
    parsed = parse_protocol_response(
        'TOOL_CALL:\n{"tool":"openclaw","action":"email_send",'
        '"objective":"Send direct email","inputs":{"to":"owner@example.com","subject":"Hello","body":"Body"},'
        '"risk":"low","needs_approval":false,"expected_result":"email sent"}'
    )
    assert parsed.kind == "tool_call"
    assert parsed.tool_call is not None
    assert parsed.tool_call["action"] == "email_send"
    assert parsed.tool_call["inputs"]["to"] == "owner@example.com"

def test_malformed_tool_call_rejected():
    with pytest.raises(ToolCallValidationError):
        parse_protocol_response("TOOL_CALL:\n{not-json}")

def test_unknown_tool_action_rejected():
    with pytest.raises(ToolCallValidationError):
        parse_protocol_response(
            'TOOL_CALL:\n{"tool":"openclaw","action":"delete_everything",'
            '"objective":"bad","risk":"low","needs_approval":false}'
        )

def test_both_final_and_tool_call_prefers_tool_call():
    parsed = parse_protocol_response(
        'FINAL:\nLooks done.\n\nTOOL_CALL:\n{"tool":"openclaw","action":"website_check",'
        '"objective":"Check site","inputs":{},"risk":"low","needs_approval":false}'
    )
    assert parsed.kind == "tool_call"
    assert "both_final_and_tool_call_present" in parsed.warnings

def test_risk_gate_blocks_approval_required_tool_call():
    with pytest.raises(RiskGateError):
        parse_protocol_response(
            'TOOL_CALL:\n{"tool":"openclaw","action":"workflow_task",'
            '"objective":"Publish something","inputs":{},"risk":"high","needs_approval":true}'
        )

def test_max_step_guard_blocks_after_limit():
    enforce_max_steps(0, 1)
    with pytest.raises(MaxStepError):
        enforce_max_steps(1, 1)
