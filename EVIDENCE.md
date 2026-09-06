# Evidence and Technical Scope

## Reviewable source excerpt

`protocol/parser.py` preserves the reviewed protocol parser from `desktop-ai-worker/protocol/parser.py` in DanielDoWork's AI infrastructure repository. It parses FINAL and TOOL_CALL responses, validates declared fields, checks caller-provided risk/approval flags, and enforces a step limit. It has no browser adapter, credentials, network client, or tool executor.

The selected tests are existing parser and guard tests extracted from `tests/test_desktop_worker_protocol.py`. Prompt-construction and fake-executor tests are omitted because those components are outside this excerpt.

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

See [validation](VALIDATION.md). A parsed tool call does not execute an action. Caller-provided risk labels are not independent authorization, and this parser alone is not a security boundary for a live agent.

## Larger project

The private application integrates model routing, local execution, bridge services, and worker orchestration. This public excerpt is a bounded example of its protocol layer, not the complete service stack.

[DanielDoWork product presentation](https://github.com/yo20ywork-max/danieldowork-showcase)

## Architecture walkthrough

The [README](README.md) explains the product concept, request flow, task execution, and component boundaries. The [source review map](SOURCE_REVIEW.md) identifies the fixed implementation snapshots used for that explanation. This additional documentation does not expand the scope of the executable validation recorded above.
