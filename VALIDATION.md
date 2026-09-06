# Validation

Checked on 2026-09-06 using Python 3.12.6 and pytest 8.3.5.

`python -m pytest -q`: **9 passed**.

Coverage includes final-marker selection, missing markers, valid protocol calls, malformed JSON, unknown actions, mixed markers, declared approval/risk checks, and step limits. Tests parse synthetic strings only. They do not open browsers, send email, invoke an executor, or establish authorization for real actions.
