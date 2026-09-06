# DanielDoWork — AI Infrastructure

[Portfolio](https://github.com/yo20ywork-max/research-portfolio) · [Project map](https://github.com/yo20ywork-max/research-portfolio/blob/main/PROJECT_MAP.md)

Source repository identifier: `yo20ywork-max/danieldowork-ai`.

## Problem

An AI feature needs more than a chat interface: model access, routing, service health, memory integration, and a reliable way to deliver work to an execution environment.

## My implementation work

Development and integration of the AI service stack supporting DanielDoWork, including the bridge, local model routing, worker execution, and development tooling.

## Technical scope

- Python/FastAPI bridge services and model-routing integration.
- LiteLLM, Ollama, OpenClaw, and a browser-based WebLLM frontend in the development stack.
- Local worker modes for deterministic tests and separately configured live integrations.
- Container-based development and operational setup documentation.

## Evidence and current scope

The implementation includes local development instructions and integration documentation. Provider availability, hardware requirements, and end-to-end behavior depend on the selected configuration; the project is not presented as cost-free or continuously available.

## Relationship to other work

Companion infrastructure for DanielDoWork — AI Workspace, with a distinct service lifecycle. The two repositories represent different technical layers of the same product.

## Engineering perspective

Routing and fallback logic need observable states and realistic failure handling. A successful isolated worker test should be distinguished from a successful full application workflow.

For the public/private boundary, see [Public Disclosure Scope](DISCLOSURE.md).

## Public repository contents

This repository is the public presentation of the source project identified above. See [Evidence and technical scope](EVIDENCE.md) for the material included here. It is not an additional product or a replacement for the operational source repository.
