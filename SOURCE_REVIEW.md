# Architecture Source Review

## Review scope

This document records a targeted walkthrough of the two source repositories. Their complete file trees were inventoried, followed by selected implementation paths for workspace access, imports, AI routing, task state, device queues, browser-AI execution, DOM actions, memory, and release boundaries.

This is not a full code audit or a new end-to-end acceptance run. The core-concept section records the product's intended design; implementation statements are tied to the snapshots below.

| Source | Reviewed commit |
|---|---|
| `yo20ywork-max/danieldowork-web` | `5f53fb0c504fe41d05eb509e2d44952d221deacb` |
| `yo20ywork-max/danieldowork-ai` | `2dcc01c6b10770c92ca719fc75acb47bb817563c` |

Source paths below identify the private implementation reviewed for the public explanation. They are provenance references, not a claim that those complete files are published in this showcase. Public runnable excerpts remain described in [EVIDENCE.md](EVIDENCE.md).

## Web application paths

Paths are relative to the web repository.

| Area | Selected files | What was checked |
|---|---|---|
| Framework and release | `overpower-app/package.json`, `CURRENT_RELEASE.md`, `overpower-app/vercel.json` | Current dependencies, recorded candidate state, and separate application deployment |
| Workspace context | `overpower-app/src/app/dashboard/page.tsx`, `src/lib/authz.ts`, `src/lib/workspace.ts` under the app root | Session and workspace resolution; project data loading |
| Spreadsheet flow | `overpower-app/src/app/api/import/xlsx/preview/route.ts` and `commit/route.ts` | Preview/commit separation, authorization, quota checks, and writes |
| Assistant route | `overpower-app/src/app/api/ai/route.ts`, `src/lib/ai/user-intelligence.ts` under the app root | Operation reservation, personal-account path, configured API fallback, and local caller fallback |
| Employee proxy | `overpower-app/src/app/api/ai-employee/[...path]/route.ts`, `src/lib/ai/employee/bridge.ts` under the app root | Allowed request paths, queue attempt, bridge attempts, and supported failure responses |
| Command and invocation | `overpower-app/src/app/api/agent/command/execute/route.ts`, `src/lib/ai/agent/invocation-gateway.ts`, `src/lib/ai/agent/create-agent-invocation.ts` under the app root | Stored command checks, duplicate status, selected runners, context links, and writeback policy |
| Device queue | `overpower-app/src/lib/ai/employee/device-workers.ts`; application `device-workers/poll` and `device-workers/complete` routes | Device identity, leases, scoped result completion, and response handling |
| Completion recovery | `overpower-app/src/lib/ai/employee/device-worker-completion-effects.ts`, `overpower-app/supabase/migrations/0093_device_worker_completion_effects.sql`, completion-effects cron route | Atomic result/effect persistence, effect claims, lease checks, and retry states |
| Flow/event records | `overpower-app/src/lib/ai/agent/tasks/task-flow-registry.ts`, `src/lib/ai/agent/session-actor-queue.ts` under the app root | Flow/task records, event history, actor leases, and wake-related state |
| DOM primitives | `overpower-app/src/core/perception/affordance-extractor.ts`, `src/core/execution/safe-action-executor.ts` under the app root | Page representation, live target checks, concrete DOM actions, and stability waits |
| Workspace writeback | `overpower-app/src/app/api/ai-employee/workspace-dispatch/route.ts` | Scoped workspace reads/mutations and result presentation |

## AI infrastructure paths

Paths are relative to the AI repository.

| Area | Selected files | What was checked |
|---|---|---|
| Chat and orchestration | `bridge/main.py` | Request processing, task/sensitivity plans, optional memory, model calls, events, and recorded responses |
| Routing labels | `bridge/sensitivity.py`, `bridge/personal_ai_router.py` | Local classifier behavior and separate personal-AI provider routing |
| Memory | `bridge/memory.py` | Optional Supabase storage, embedding destinations, filtering, and Python similarity ranking |
| Task queue/API | `bridge/task_queue.py`, `bridge/routes_worker.py`, `bridge/personal_ai_models.py` | SQLite backend, transactional claims, worker leases, task/event state, and retry handling |
| Conversation protocol | `desktop-ai-worker/protocol/prompts.py`, `parser.py` | Action vocabulary, FINAL/TOOL_CALL format, one action per response, and tool-result prompt |
| Worker loop | `desktop-ai-worker/worker.py` | Browser-provider selection, polling, renewal, parsing, tool calls, result feedback, and explicit failure states |
| Executor integration | `desktop-ai-worker/executor/openclaw.py` | Fake/CLI/HTTP modes, default fake mode, configured execution and input controls |
| Development frontend | `frontend/webllm-client.js` | WebGPU/WebLLM, bridge access, and offline queue; distinct from the product frontend |
| Environment composition | `dev/docker-compose.yml`, `desktop-ai-worker/README.md` | Configured service/worker relationships and development/live mode distinctions |

## Interpretation boundaries

- Web conversations with ChatGPT, Claude, or Gemini are a different execution path from local WebLLM inference and hosted model APIs.
- The inspected browser-AI protocol carries one tool request at a time. The broader task-checklist concept should not be read as evidence that every route has a complete dependency planner.
- Flow events and state changes coexist with polling/lease-based delivery.
- The OpenClaw adapter and the web repository's DOM executor are separate modules. Their presence does not establish one fully accepted integration path.
- The web device queue and bridge desktop-worker queue use different APIs and storage.
- Local inference, embedding generation, data storage, and provider-account use are separate configuration choices.
- Older architecture notes are useful history; the inspected code takes precedence for the behavior described here.
- Public validation records cover only the selected executable examples. This walkthrough adds no new model-performance, live browser, or production-acceptance claim.

[Return to the README](README.md)
