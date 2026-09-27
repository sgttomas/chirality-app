# Chirality App v4: supplier-layer landscape as of 2026-09-25

**What this is.** This is the TASK return for HELPS_HUMANS under `chirality-root:bundled:workflow:reverse-engineer-software`. It describes the candidate layers as they stand. It does not select or recommend a supplier. I created or modified no local files, and my local inspection of REPO_ROOT was read-only.

**How to read the labels.** Each claim carries a label and a source ID. The sources are listed in §7.
- **VD** means vendor documentation.
- **RN** means release notes or a changelog.
- **TP** means a third-party report.
- **INF** means my own inference.
- **LOCAL** means a read-only inspection of REPO_ROOT.

I retrieved every web source on 2026-09-25. Where a publication date was available, it is given in §7. Some pages reached me only as tool summaries. Those claims are marked "(summary)" and are worth checking against the original before anyone relies on them.

---

## 0. The shape of the landscape

- **Harnesses have become platforms.** A study of 11 coding harnesses posted on 2026-07-15 found that every system uses its own hand-written async loop rather than a general agent framework. It also found that SKILL.md skills are the most-adopted extension point (9 of 11 systems) and MCP the second (8 of 11). The authors describe ACP as adding a third role, "harness hosting", and conclude that the coding harness "completed a turn from tool to platform" in the first half of 2026 (TP S48).
- **Each major vendor harness now ships a supported embedding surface:**
  - Codex: the App Server, a JSON-RPC interface.
  - Claude Code: the Agent SDK, a library around a bundled native binary.
  - GitHub Copilot: the Copilot SDK, which talks JSON-RPC to the Copilot CLI.
  - Gemini CLI: headless mode, ACP and an SDK package.

  (VD S2, S14, S26; RN S33)
- **The permissively licensed, provider-agnostic harnesses** are Pi, goose, OpenHands and OpenCode. They differ widely in how much governance they build in. Pi deliberately omits permission prompts, MCP and subagents (VD S36).
- **The protocol layer is consolidating:**
  - MCP 2026-07-28 moved to a stateless core with opt-in extensions, including Tasks and MCP Apps (VD S54).
  - OpenAI's Apps SDK UI patterns were folded into MCP Apps (VD S59, S62).
  - ACP is the editor-to-agent protocol (VD S63).
  - AG-UI covers the application-to-agent UI stream (VD S66).
  - A2A covers agent-to-agent traffic (VD S68).
- **Authentication and billing terms are the least stable facts in this landscape**, and they diverge sharply between vendors (§1.1, §1.2).
- **GUI operation splits in two.** Computer-use tools at the API level are generally available. Desktop computer-use features are tied to the vendors' own desktop apps and consumer plans, and are not exposed through their embedding surfaces (VD S71–S74).

**Context from REPO_ROOT.** The v3 Runtime now hosts a stock, lockfile-pinned `codex app-server` child inside an application-owned service. The earlier daemon-era integration was superseded on 2026-09-12 under D-GOV-43 (LOCAL1). The Runtime also contains:
- `engine-claude`, with adapters named `anthropic-direct` and `claude-agent-sdk`, both of which require an Anthropic API credential.
- `engine-pi-omlx`, pinned to `@earendil-works/pi-coding-agent` 0.82.0 and a local oMLX client.

(LOCAL2)

---

## 1. Layer 1: agent harnesses and SDKs

### 1.1 OpenAI Codex: App Server, Codex SDK and CLI

**What it provides**
- **Architecture.** The App Server separates Codex's agent loop, thread management and sandboxed execution from its clients. OpenAI published the architecture on 2026-02-17 (TP S4).
- **Primitives:**
  - *item*: has a lifecycle of started, deltas and completed.
  - *turn*: a group of items.
  - *thread*: a durable container that can be started, resumed, forked, archived and deleted.

  `thread/rollback` has been replaced by `thread/revert` (VD S1).
- **Surfaces built on it.** The CLI, VS Code, the web app, the desktop app, JetBrains and Xcode all use it (TP S4).
- **Positioning.** OpenAI documents the App Server for embedding Codex in a product, with authentication, history, approvals and streamed events. It positions the SDK for automation and CI. `command/exec` runs a single sandboxed command without creating a thread (VD S2).
- **Transports.** The default is newline-delimited JSON over stdio. WebSocket exists but is "experimental and currently unsupported for production". A Unix socket option has health probes (VD S2).
- **Approvals.** These arrive as server-initiated JSON-RPC requests. The client can answer `accept`, `acceptForSession`, `decline` or `cancel`, and can attach an optional `execpolicyAmendment` (VD S2). Approvals can be routed to `user`, `auto_review` or `guardian` reviewers (TP S5).
- **Sandbox policies.** The options are `readOnly`, `workspaceWrite`, `dangerFullAccess` and `externalSandbox`, each with a network-access control (VD S2).
- **Dynamic tools.** A client can pass `dynamicTools` on `thread/start`. Codex persists them and restores them on resume. This is one route for exposing host-application operations (VD S2).
- **Hooks.** A third-party guide (2026-04-29) lists six lifecycle hook events: `SessionStart`, `PreToolUse`, `PermissionRequest`, `PostToolUse`, `UserPromptSubmit` and `Stop` (TP S5). September 2026 releases added Interrupt hooks (RN S10).
- **Subagents.** These run as their own threads. The same guide says their approvals surface to the active UI labelled with the source thread (TP S5).
- **MCP.** Codex acts as an MCP client. Support for the 2026-07-28 protocol sits behind the feature flag `codex_apps_mcp_2026_07_28` (VD S1).
- **Event stream and schema:**
  - Notifications are complete by default, and a client can suppress specific ones with `optOutNotificationMethods` (VD S2).
  - Many APIs require the `experimentalApi` opt-in (VD S2).
  - `codex app-server generate-ts` emits per-version TypeScript or JSON Schema bindings (VD S2), and the schema drifts between CLI versions (TP S5).
- **SDKs.** The TypeScript SDK is described as production-ready. The Python SDK talks JSON-RPC to the App Server. `codex mcp-server` has been removed (VD S3, summary).
- **Models.** Local models run through `--oss` or `model_providers` (Ollama, LM Studio, MLX) (VD/TP S11).

**Embedding fit**
- The supported interface is a Rust binary speaking JSON-RPC over stdio (VD S2).
- A Tauri host could spawn it as an `externalBin` sidecar from Rust (VD S81). That is inference, not something I tested (INF).

**Authentication and billing**
- Sign-in options are Sign in with ChatGPT, an API key, enterprise Codex access tokens, and device-code sign-in (in beta).
- Credentials are stored in `~/.codex/auth.json` or the OS keyring (VD S6).
- The vendor authentication page says nothing about third-party apps using a user's ChatGPT sign-in (VD S6).
- A July 2026 analysis reports that OpenAI executives publicly endorsed ChatGPT-plan use inside third-party harnesses. It characterises this as tolerated practice rather than a contractual permission (TP S7).
- The "Sign in with ChatGPT" beta launched on 2026-08-02. It shares identity only (name, email and avatar), not model usage on the user's plan (TP S8).

**License and cadence**
- The CLI is Apache-2.0. The desktop app is proprietary (VD S9; TP S12).
- The latest release is v0.156.1, dated 2026-09-23, with releases roughly weekly (TP S10).
- The Codex app merged into the ChatGPT desktop app on 2026-07-09 (TP S12).

**Related hosted option.** OpenAI's Agents API entered public beta on 2026-09-10. It offers the Codex harness as a managed service, with a choice of OpenAI-hosted, self-hosted or partner sandboxes, and is billed by token and tool use (TP S13).

**Known limits**
- WebSocket is unsupported for production (VD S2).
- Experimental-API gating and schema drift apply (VD S2; TP S5).
- Computer use is not exposed through the App Server (VD S74; §3).

### 1.2 Anthropic: Claude Agent SDK and Claude Code headless

**What it provides**
- **Architecture.** The Agent SDK is "a library that runs the Claude Code binary", with TypeScript and Python packages. It exposes built-in tools, hooks, subagents, MCP, permissions, sessions (resume and fork), skills, commands, memory and plugins. For other languages, the documented path is running `claude -p` as a subprocess with JSON output (VD S14).
- **Binary.** Both SDKs bundle a platform-native Claude Code binary as an optional dependency (TP S25).
- **Permission evaluation order.** Hooks run first, then deny rules, then ask rules, then the permission mode, then allow rules, then the `canUseTool` callback (VD S15).
- **Permission modes:**
  - `default`
  - `dontAsk`
  - `acceptEdits`
  - `bypassPermissions`
  - `plan`
  - `auto`, in which a model classifier decides.

  Subagents inherit the parent's mode (VD S15).
- **Sessions.** These are stored as local JSONL files under `~/.claude/projects/`. They support continue, resume-by-ID and fork. A `SessionStore` adapter lets them resume across hosts, and file checkpointing is separate from session history. The V2 session API was removed in TypeScript SDK 0.3.142 (VD S16).
- **Hooks.** About 28 hook events are available as in-process callbacks in TypeScript, including `PermissionRequest`, `SubagentStart/Stop`, `Elicitation`, `InstructionsLoaded` and `ConfigChange`. The Python SDK supports a smaller subset; for example, it lacks `SessionStart` and `SessionEnd` (VD S17).
- **Headless stream.** The `stream-json` output provides:
  - a `system/init` event with a `capabilities` array;
  - subagent messages carrying `parent_tool_use_id`;
  - `permission_denied` events;
  - `api_retry` events.

  (VD S18)
- **Headless options:**
  - `--bare` skips hooks, `CLAUDE.md` and MCP discovery, and is the recommended mode for scripted use.
  - `--permission-prompt-tool` routes approvals to an MCP tool.

  (VD S18)
- **MCP.** The SDK can host MCP servers in-process with `createSdkMcpServer`, and has an alpha `readMcpResource` for MCP Apps `ui://` resources (RN S19).
- **Sandboxing.** Claude Code's sandboxed Bash tool isolates filesystem and network access (VD S72).

**Models**
- Claude is available through the Anthropic API, Bedrock, Google Cloud and Microsoft Foundry (VD S18).
- Local models can be reached by pointing `ANTHROPIC_BASE_URL` at an Anthropic-compatible server. Ollama has offered one since v0.14.0 (2026-01-16), with caveats: `cache_control` does not apply, and `tool_choice` is ignored (VD/TP S24).
- Whether Anthropic's terms allow this with the SDK is not established here (INF).

**Authentication and billing**
- Anthropic's documentation states: "Unless previously approved, Anthropic does not allow third party developers to offer claude.ai login or rate limits for their products, including agents built on the Claude Agent SDK." It directs developers to API-key authentication instead (VD S14).
- The support article, current at retrieval, says Agent SDK, `claude -p` and third-party app usage "still draw from your subscription's usage limits". It also says the monthly Agent SDK credit announced for 2026-06-15 is paused (VD S20).
- A February 2026 clarification said subscription OAuth tokens are for Claude Code and Claude.ai only (TP S21). The May 2026 credit announcement is reported in TP S22.
- Whether an individual may use their own subscription through an SDK-based tool, as opposed to a developer offering claude.ai login in a product, needs vendor clarification for SWBPIPE's distribution model (INF).
- Use is governed by Anthropic's Commercial Terms, and there are branding restrictions: no "Claude Code" naming (VD S14).

**Cadence.** The TypeScript SDK is at 0.3.282, tracking Claude Code 2.1.28x, with near-daily releases (RN S19). A September 2026 fix addressed `-p` and SDK sessions hanging after an internal error (RN S23).

**Related hosted option.** Claude Managed Agents is a hosted harness that uses either an Anthropic cloud sandbox or a self-hosted sandbox (VD S14).

**Limits**
- There is no Rust SDK. A Rust host would drive the binary over `stream-json` or through a Node or Python sidecar (VD S14; INF).
- Computer use requires an interactive, claude.ai-authenticated session (§3) (VD S72).

### 1.3 GitHub Copilot SDK (a prominent 2026 entry)

**What it provides**
- It became generally available on 2026-06-02 and offers programmatic access to Copilot's agent runtime. That includes planning, tool calls, file edits, streaming, multi-turn sessions, custom tools and MCP, system-prompt customisation, hooks around tool use and permission requests, and cloud-backed or remote sessions.
- It has OpenTelemetry tracing with W3C trace-context propagation.

(VD S26)

**Embedding fit**
- SDKs exist for Node/TypeScript, Python, Go, .NET, Java and **Rust**.
- All of them speak JSON-RPC to a Copilot CLI server. The CLI is bundled for Node, Python and .NET; for Go, Java and Rust it must be installed separately or found on `PATH` (VD S26, S27).

**Authentication, models and license**
- It works for Copilot subscribers, including the free tier.
- BYOK is supported for OpenAI, Microsoft, Anthropic and other providers, but only with key-based authentication (VD S26, S27).
- The SDK repository is MIT-licensed. I did not verify the license or terms of the CLI itself (INF).

### 1.4 OpenAI Agents SDK (Python and TypeScript)

**What it provides**
- Agents, handoffs, guardrails, human-in-the-loop, sessions, tracing, MCP and hosted tools, realtime and voice agents, and Sandbox Agents.
- It is described as provider-agnostic, supporting "100+ other LLMs" through LiteLLM or any-llm. MIT license (VD S28).
- An April 2026 update added a model-native harness (MCP, skills, `AGENTS.md`, shell and `apply_patch`), sandboxes and a Manifest abstraction. It shipped for Python first, with subagents and code mode then still in development (TP S29).
- The current sandbox guide lists these sandbox clients for both Python and TypeScript:
  - Unix-local
  - Docker
  - hosted providers: Blaxel, Cloudflare, Daytona, E2B, Modal, Runloop and Vercel

  (VD S30)
- There are three persistence layers: RunState (history and approvals), serialized sandbox session state, and workspace snapshots (VD S30).

**Class.** This is an in-process library. The application owns the process and the UI (INF).

### 1.5 Google: ADK and Gemini CLI

**ADK**
- Available in Python (1.x, with a 2.0 alpha in progress), TypeScript (2.0 GA, with graph workflows), Go (1.0), Java (1.0) and Kotlin.
- Provides sequential, loop, parallel and graph agents; sessions, state and memory; MCP and OpenAPI tools; action confirmations for human-in-the-loop; A2A; bidirectional streaming; plugins; and evaluation.
- Gemini, Gemma and Claude are supported directly; OpenAI, Ollama, vLLM and LiteLLM through adapters (VD S31).
- ADK Go 1.0 was released on 2026-03-31, adding OpenTelemetry, plugins, human-in-the-loop confirmation and YAML-defined agents (VD S32).
- License: Apache-2.0 (TP S31a).

**Gemini CLI**
- Apache-2.0 (VD S35), with weekly releases. The latest is v0.61.0, dated 2026-09-23 (RN S33).
- Provides subagents, including remote subagents over A2A; an SDK package; ACP mode; hooks; sandboxing (macOS Seatbelt, Windows, gVisor, LXC); a policy engine; plan mode; and headless JSON or stream-JSON output (RN S33).
- **2026 change.** Google announced on 2026-05-19 that from 2026-06-18, Gemini CLI would stop serving free, Google AI Pro and Ultra users. Those tiers moved to Antigravity CLI. Gemini CLI remains available with paid Gemini or Enterprise API keys (VD S34).
- Third parties describe Antigravity CLI as a closed-source Go binary (TP S34a).

### 1.6 Pi (earendil-works/pi, formerly badlogic/pi-mono)

**What it provides**
- Pi calls itself "a minimal agent harness". It deliberately omits MCP, subagents, permission popups, plan mode, built-in to-dos and background bash, on the view that users build these through extensions or packages.
- It supports more than 15 providers, has tree-structured session history, and runs in interactive, print/JSON, RPC and SDK modes. MIT license, maintained by Earendil Inc. (VD S36).
- Pi joined Earendil in April 2026 (TP S40).
- **RPC mode** uses LF-delimited JSONL over stdio. Commands include `prompt`, `steer`, `follow_up`, `abort`, `new_session`, `fork`, `switch_session`, `get_state`, `set_model`, `compact` and `bash`.
- Extension dialogs cross the RPC boundary as `extension_ui_request` and `extension_ui_response`.
- The documentation says to prefer the SDK for in-process Node or Bun integration, and the exported `RpcClient` for subprocess use (VD S38). Pi requires Node 22.19 or later (VD S37).

**Authentication and models.** Users can log in with a subscription or an API key per provider (VD S37). A July 2026 report says Pi and OpenCode together make up about 10% of Codex traffic (TP S7). Local use through oMLX exists in REPO_ROOT (LOCAL2).

**Cadence.** Several releases a week: v0.85.1 on 2026-09-05 through v0.87.1 on 2026-09-22. Recent releases added canonical session-context editing (v0.87.0) and new providers (RN S39).

**Fit implication.** Approvals, MCP and subagents would all be Chirality-built extensions (INF).

### 1.7 goose (AAIF)

**What it provides**
- Rust, Apache-2.0 (VD S45).
- Moved from Block to the Agentic AI Foundation on 2026-04-07; the repository is now `aaif-goose/goose` (VD S43).
- Permission modes: Autonomous (the default), Smart Approval, Manual Approval and Chat Only (VD S44).
- It is an MCP client and an MCP Apps host (VD S58).
- It currently ships three binaries: the `goose` CLI; `goosed`, which exposes REST plus server-sent events across 103 endpoints; and `goose-acp-server`. Maintainers proposed in March 2026 to consolidate on ACP, with `goose serve` exposing ACP over HTTP and WebSocket (VD S42, maintainer proposal).
- v1.51.0 (2026-09-17) routes the desktop app to the state-machine loop "via ACP prompt meta". v1.52.0 was released on 2026-09-23, and releases are weekly (RN S41).

**Embedding.** Options are a subprocess (ACP or `goosed`) or, in principle, Rust crates. How stable those internal crate APIs are is unknown (INF).

### 1.8 OpenHands Software Agent SDK

- A Python SDK with four packages: `sdk`, `tools`, `workspace` and `agent-server`.
- Workspaces can be local, or remote on Docker or Kubernetes.
- Conversation state is event-sourced.
- It includes a confirmation policy and a security analyzer, plus MCP, sub-agent delegation, and multiple LLMs through LiteLLM, including open models.
- It exposes REST/WebSocket and an OpenAI-compatible endpoint. MIT license.

(VD S46; TP S46a)

### 1.9 OpenCode and other 2026-prominent harnesses

**OpenCode** (MIT) runs `opencode serve`, a headless HTTP server with an OpenAPI 3.1 specification and a server-sent-event bus. It supports sessions (create, fork, abort, revert), permission-request responses and basic authentication. Its terminal UI is itself a client of that server, and a JS/TS SDK is generated from the specification (VD S47). ACP support is listed as native (VD S63).

**OpenClaw** (MIT) is a messaging-first personal agent. It had 247k GitHub stars by March 2026; its creator joined OpenAI, and stewardship is planned under an OpenClaw Foundation. Version 2.0 shipped on 2026-08-30, and it has had security incidents (TP S49). **Hermes** and **Mistral Vibe** appear in the harness study (TP S48). Neither is primarily an embedding SDK (INF).

### 1.10 Build-your-own-loop frameworks (the contrasting class)

In these frameworks, the application writes and owns the loop, the tools, the permissions and the persistence.

| Framework | Status and relevant features | Source |
|---|---|---|
| LangGraph | 1.0; durable, checkpointed state; interrupts for human-in-the-loop | VD S52 |
| Mastra | TypeScript; 1.0 in January 2026; workflows suspend and resume, with persisted snapshots | TP/VD S51 |
| Pydantic AI | Typed; MCP; AG-UI; durable execution on Temporal, DBOS, Prefect, Restate and others | VD S53 |
| Vercel AI SDK 7 | Released 2026-06-25; tool-approval workflows; durable `WorkflowAgent`; MCP Apps support; sandbox integration; a **`HarnessAgent` abstraction that drives Claude Code, Codex and other harnesses** | VD S50 |

The `HarnessAgent` abstraction means frameworks now also wrap harnesses rather than only competing with them (INF).

---

## 2. Layer 2: embedding and connection protocols

**MCP, current specification 2026-07-28**
- Released 2026-07-28 (VD S54).
- The protocol core is now stateless: the `initialize` handshake and session IDs are gone, capabilities travel per request in `_meta`, and there is an optional `server/discover`.
- Multi Round-Trip Requests let a server return `input_required` so the client retries with the answers.
- Other changes: header-based routing, cacheable lists, authorization hardening (CIMD replaces Dynamic Client Registration, which is deprecated), and a formal extensions framework.
- Roots, Sampling, Logging and HTTP+SSE are deprecated, with a removal window of at least 12 months.
- Tier-1 SDKs are TypeScript, Python, Go and C#; the **Rust SDK is in beta** (VD S54).
- Migration notes date removals to no earlier than 2027-07-28 (TP S60).

**MCP elicitation**
- It has a form mode (a flat, primitive-typed JSON Schema) and a URL mode for sensitive or out-of-band flows.
- Elicitation requests are delivered inside `InputRequiredResult`.
- Users can accept, decline or cancel.
- Servers must not request secrets through form mode (VD S56).

**MCP Tasks** (`io.modelcontextprotocol/tasks`)
- A durable `taskId` with the states `working`, `input_required`, `completed`, `failed` and `cancelled`.
- Clients poll with `tasks/get` and supply mid-flight input with `tasks/update`; `tasks/cancel` is cooperative.
- Server-sent notifications are optional.
- The documentation cites human approval gates as a use case (VD S57).

**MCP Apps** (`io.modelcontextprotocol/ui`, specification 2026-01-26)
- A tool declares a `ui://` resource. The host renders its HTML in a sandboxed iframe and talks to it over postMessage JSON-RPC (`ui/*`).
- From inside the iframe, an app can request tool calls, send messages and update the model's context.
- Hosts can build on the SDK's **AppBridge** module or on `@mcp-ui/client` (VD S58).
- It was co-developed by Anthropic, OpenAI's Apps SDK team and the creators of MCP-UI, and launched on 2026-01-26 (VD S59).
- Listed hosts: Claude, VS Code Copilot, M365 Copilot, goose, Postman, MCPJam and Archestra (VD S58), plus ChatGPT and Cursor by August (TP S61).
- JetBrains, Kiro and Antigravity were still not supporting it as of August 2026 (TP S61).
- If the two sides do not negotiate the extension correctly, tool calls silently fall back to plain text (TP S61).

**OpenAI Apps SDK.** ChatGPT implements MCP Apps. New UI work should use the standard keys and the `ui/*` bridge; `window.openai` remains for ChatGPT-only extensions, and OpenAI has no plans to deprecate it (VD S62).

**ACP (Agent Client Protocol)**
- JSON-RPC over stdio, with agents running as subprocesses of the editor. A remote HTTP/WebSocket transport is a work in progress.
- It reuses MCP's JSON representations where possible.
- The stable protocol version is 1. License Apache-2.0. Libraries exist for Rust, TypeScript, Python, Kotlin and Java (VD S63).
- The ACP Registry opened on 2026-01-28, with Zed and JetBrains as clients (VD S64). JetBrains became co-lead maintainer in February 2026 (TP S65).
- Claude Agent and Codex connect through adapters, `claude-agent-acp` and `codex-acp`. Gemini CLI, goose, OpenHands, Pi, OpenCode and Copilot are listed as native (VD S63).
- ACP's primitives are editor-oriented: files, terminals and diffs. How well they map onto an engineering application's domain objects is untested (INF).

**AG-UI**
- MIT; event-based over HTTP, server-sent events or WebSocket.
- About 16 event types: lifecycle, text, tool calls, state snapshots and deltas, interrupts, frontend tool calls, and others.
- Integrations include the Claude Agent SDK, ADK, Microsoft Agent Framework, Mastra, Pydantic AI and LangChain. SDKs include Rust.
- It lists MCP Apps as a supported generative-UI format (VD S66).
- CopilotKit, which leads AG-UI, raised a $27M Series A in May 2026 (TP S67).

**A2A.** Version 1.0 was announced on 2026-03-12, under Linux Foundation governance. It has JSON-RPC, gRPC and REST bindings and signed Agent Cards (VD/TP S68). Its scope is agent-to-agent delegation, not the host UI (INF).

**A2UI** (Google). A declarative UI specification at v0.9 (2026-04-17), with a v1.0 release candidate targeted for Q4 2026. Apache-2.0 (TP S69).

**Governance.** The AAIF, formed in December 2025, hosts MCP, goose and `AGENTS.md`; agentgateway joined in June 2026 (VD S70; TP S70a).

---

## 3. Layer 3: computer use and GUI operation

**Anthropic API computer use** (`computer_toolset_20260801`)
- Generally available on the Claude API and Google Cloud; beta on Bedrock and Foundry.
- 17 actions, including `zoom` (on by default) and batched actions.
- The client implements the environment. Anthropic's reference environment is a Linux container with a virtual X display (Xvfb).
- The documentation warns about prompt injection, advises keeping requests to about 20 screenshots or fewer, and recommends human confirmation for consequential actions.

(VD S71)

Because the client executes every action, the API itself is not tied to Linux (INF). The move to general availability is reported as 2026-08-19 (TP S82).

**Claude Code and Claude Desktop computer use**
- A research preview on Pro and Max plans only, not Team or Enterprise.
- Requires claude.ai authentication and is not available in `-p` mode. The CLI supports macOS only; Desktop supports macOS and Windows.
- Apps are approved per app, per session. Browsers are view-only and terminals and IDEs are click-only.
- Only one session can control the computer at a time; other apps are hidden while it works; Esc aborts.

(VD S72)

It is therefore not an embedding surface for a third-party app (INF).

**OpenAI API computer use**
- A "computer" tool plus a code-driven approach through Playwright or PyAutoGUI. Documented as GA.
- Models named on the page at retrieval include GPT-6 Astra and GPT-5.6-sol.
- The guidance says to restrict the environment and keep the user "in control of purchases, data transmission, destructive changes" (VD S73, summary).

**ChatGPT desktop (Codex) Computer Use**
- Available on macOS and Windows in the ChatGPT desktop app, for Work and Codex plans, in supported regions.
- Per the vendor page as summarised, it is **not** available in the CLI, App Server, IDE or API.
- Apps are approved individually, with an "Always allow" option, and administrators can restrict them. Terminal automation is blocked, and on Windows it runs in the foreground only.

(VD S74, summary)

It launched on macOS on 2026-04-16 with a background cursor (TP S75). A third party says it uses the accessibility tree and was unavailable in the EEA, UK and Switzerland at launch (TP S76).

**Accessibility-API approaches**
- MCP servers expose the operating system's accessibility tree: AXUIElement on macOS, UI Automation on Windows, AT-SPI on Linux. Examples are MacOS-MCP and OculOS.
- Some claim roughly 10× speed over screenshot-driven operation. That figure is unverified (TP S77).
- Windows 11 has an experimental agent workspace and an on-device MCP registry, with built-in MCP servers for File Explorer and Settings (VD/TP S78).

**Tauri-specific constraints**
- `tauri-driver` WebDriver supports Windows and Linux but not macOS, because Apple provides no WKWebView driver. Community or embedded drivers exist, and CrabNebula's fork requires a paid key on macOS (VD/TP S79).
- `tauri-plugin-mcp`-style plugins expose screenshots, the DOM and input to agents; they are oriented towards development and debugging (TP S80).
- How well the content of Tauri webviews (WKWebView, WebView2) shows up in operating-system accessibility trees is untested here (INF).

---

## 4. Cross-cutting facts relevant to fit (no ranking implied)

**Embedding classes**
- (a) An in-process library in the host language: the OpenAI Agents SDK, ADK, the frameworks, the Pi SDK and OpenHands. None is a Rust-native full harness, except that goose's crates could in principle be used (INF).
- (b) An SDK wrapping a bundled native binary: the Claude Agent SDK, the Copilot SDK (which includes a Rust SDK) and the Codex TypeScript SDK.
- (c) A server protocol: the Codex App Server over stdio, OpenCode over HTTP with server-sent events, `goosed` (moving to ACP), the OpenHands agent-server, and Pi RPC.
- (d) A hosted harness: Claude Managed Agents and the OpenAI Agents API.

A Tauri Rust host can bundle native binaries as sidecars (VD S81). A harness that exists only as a TypeScript library would need a JS runtime sidecar (INF).

**Approval primitives** differ in kind: server requests (Codex, ACP), callbacks (`canUseTool`, Copilot's permission handler), resumable interrupts (RunState, LangGraph, Mastra), protocol states (MCP `input_required`, AG-UI interrupts), or none at all (Pi). Both Claude (`auto`) and Codex (`auto_review` and `guardian`) offer **model-classifier approval modes** (VD S15; TP S5). This bears directly on the requirement that human decision rights are never transferred (INF).

**Audit evidence.** The available sources are:
- full JSON-RPC notification streams (Codex);
- `stream-json` output, hooks and JSONL transcripts (Claude);
- OpenTelemetry traces (Copilot, ADK Go);
- event-sourced state (OpenHands);
- JSONL events and session files (Pi);
- server-sent-event buses (OpenCode, `goosed`).

The formats are vendor-specific and change with versions (VD/TP as cited).

---

## 5. What only a local experiment can settle, with one experiment per class

**Settled only locally:**
1. Whether event streams are complete and stable across pinned versions.
2. Whether a subagent's approvals reach the host UI with enough identity for evidence.
3. What resume and fork actually preserve after a crash, and how that interacts with the filesystem.
4. Sidecar size, startup latency, and macOS signing and notarization inside a Tauri bundle.
5. How a nested harness sandbox interacts with the host app's sandbox and entitlements.
6. Whether MCP Apps render in WKWebView or WebView2 with nested iframes and CSP.
7. Whether Tauri webview content is exposed through AX or UI Automation.
8. How reliably local models call tools through each harness.
9. Actual MCP 2026-07-28 client behaviour in each harness.
10. How far each harness reads the user's global configuration (`~/.codex`, `~/.claude`) when embedded.

**Not settled by experiment.** Whether third-party use of consumer subscriptions is permitted needs written confirmation from the vendor.

All seven experiments below are disposable. Each runs in a temporary directory, with no product code and no downloads beyond the pinned package under test, and runs only once the owner approves.

**E1. Server-protocol harness: Codex App Server in a Tauri shell**
- *Setup:* A throwaway Tauri app spawns a pinned `codex app-server` sidecar over stdio. It registers one `dynamicTool` named `run_mock_solver` and uses the `workspaceWrite` sandbox.
- *Action:* A single turn that edits a file, calls the mock tool, and triggers a command approval. Then kill the child process and call `thread/resume`.
- *Observe:*
  - the approval round trip;
  - whether every item and turn notification arrives;
  - whether the dynamic tool survives resume;
  - which global config files are read;
  - the size of the regenerated schema diff between two CLI versions.
- *Limit:* Half a day, the owner's own credential, and one platform.

**E2. SDK-over-binary harness: Claude Agent SDK and Copilot SDK**
- *Setup:* (a) A Node sidecar running the Agent SDK with `canUseTool`, a `PreToolUse` audit hook and an in-process SDK MCP tool. (b) A Rust host driving `claude --bare -p --input-format stream-json` with `--permission-prompt-tool`. (c) Optionally, the Copilot SDK in Rust with BYOK.
- *Action:* The same task as E1, plus spawning one subagent.
- *Observe:*
  - approval fidelity in (a) versus (b);
  - whether subagent events carry `parent_tool_use_id`;
  - fork behaviour;
  - sidecar size and cold-start time.
- *Limit:* API keys only, with no subscription login, given §1.2.

**E3. Minimal open harness: Pi over RPC with a local model**
- *Setup:* Pi at its current pinned release in RPC mode, with a local oMLX or Ollama provider and one extension that gates `bash` or `write` through `extension_ui_request`.
- *Action:* The same task.
- *Observe:*
  - how much governance code the extension needs;
  - event completeness;
  - `fork` and `switch_session`;
  - the local model's tool-call error rate over 10 runs.
- *Limit:* One day.

**E4. Protocol-normalised embedding: an ACP client in Rust**
- *Setup:* The `agent-client-protocol` crate, driving goose, Gemini CLI (with an API key), `codex-acp` and `claude-agent-acp`.
- *Action:* A new session, a prompt, a permission request, then `session/load`.
- *Observe:* What each agent loses compared with its native protocol (dynamic tools, subagent visibility, sandbox choice), and how well ACP's editor primitives cover non-file domain objects.
- *Limit:* Two agents at minimum.

**E5. Build-your-own-loop: Vercel AI SDK 7 or Pydantic AI**
- *Setup:* One application tool marked as needing approval, plus durable execution (`WorkflowAgent`, or Temporal/DBOS).
- *Action:* Pause at the approval, restart the process, then approve.
- *Observe:* The lines of code needed to reach parity with E1 on approvals, evidence and resume. Also, where applicable, AI SDK 7's `HarnessAgent` wrapping Codex or Claude Code.
- *Limit:* One day.

**E6. Host-UI protocol: MCP Apps AppBridge in a Tauri webview**
- *Setup:* The ext-apps `basic-host` pattern embedded in a Tauri window, with one sample app (a plot or PDF viewer).
- *Action:* Render the app, call a tool from inside the iframe, and push an update to the model's context. Separately, emit the same turn as AG-UI events to a minimal panel.
- *Observe:* CSP and iframe behaviour in WKWebView versus WebView2, whether tool-call proxying works, and whether approvals are visible to the user.
- *Limit:* macOS plus one other operating system.

**E7. GUI operation: structured interface versus accessibility versus pixels**
- *Setup:* A toy Tauri app with three controls, reached in three ways: (i) as MCP tools; (ii) through an accessibility-tree MCP server; (iii) through screenshot computer use, meaning an interactive Claude Code session or the API toolset in a Linux VM build.
- *Action:* The same five-step task, run 10 times each way.
- *Observe:* Success rate, latency, whether the AX tree exposes webview content, and what the human sees and approves.
- *Limit:* No real engineering data. Screen control only on apps the owner explicitly approves.

---

## 6. Comparison tables

### Layer 1: harnesses

"n/v" means not verified in this pass. "none (design)" means the feature is deliberately left out by design.

| Candidate | Loop and built-in tools | MCP | Subagents | Sessions: persist, resume, fork | Approvals and modes | Sandbox | Hooks and event stream | Models, incl. local | Embedding and languages (Rust/Tauri fit) | Auth and billing | License | Maturity and cadence |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Codex App Server / SDK / CLI | Full coding loop; `command/exec`; dynamic tools | Client; 2026-07-28 behind a flag | Yes, as threads | start / resume / fork / archive / revert | Server requests: accept, acceptForSession, decline, cancel; reviewers user, auto_review, guardian | readOnly, workspaceWrite, dangerFullAccess, external; network toggle | 6+ hook events and Interrupt hooks; full JSON-RPC stream | OpenAI; `--oss` Ollama and LM Studio | Rust binary over stdio JSON-RPC (WebSocket experimental); TS and Python SDKs; sidecar | ChatGPT sign-in, API key, access tokens; third-party plan use tolerated, not contractual | Apache-2.0 (CLI) | v0.156.1, 2026-09-23; about weekly; schema drift |
| Claude Agent SDK / Claude Code `-p` | Claude Code tools | Client plus in-process servers; MCP Apps read (alpha) | Yes, nested | JSONL; continue, resume, fork; SessionStore; checkpoints | default, dontAsk, acceptEdits, bypass, plan, auto; `canUseTool`; rules | Sandboxed Bash | About 28 hook events (TS), fewer in Python; `stream-json` | Claude through the API and clouds; local through a compatible base URL (caveats) | TS or Python library around a bundled native binary; other languages via the CLI; no Rust SDK | API key for products; claude.ai login not allowed unless approved; SDK credit paused | Commercial Terms; proprietary binary | TS 0.3.282; near-daily |
| GitHub Copilot SDK | Copilot runtime | Yes | n/v | Multi-turn; cloud or remote sessions | Permission handler and hooks | n/v | Pre/post tool hooks; OpenTelemetry (W3C) | Copilot models; BYOK (key-only) | Node, Python, Go, .NET, Java, **Rust**; JSON-RPC to the CLI | Copilot plan (incl. free) or BYOK | SDK MIT; CLI n/v | GA 2026-06-02 |
| OpenAI Agents SDK | General loop; SandboxAgent (files, shell, compaction) | Yes | Handoffs; subagents in development (April) | Sessions; RunState; sandbox state and snapshots | Human-in-the-loop interruptions | Unix-local, Docker, hosted | Built-in tracing | 100+ via LiteLLM or any-llm | In-process Python or TS | Provider keys | MIT | Active; hosted Agents API beta from 2026-09-10 |
| Google ADK | LLM, workflow and graph agents | Yes | Native | SessionService, state, memory | Action confirmations | Deployment-level (INF) | Callbacks, plugins, OpenTelemetry | Gemini, Gemma, Claude; Ollama and vLLM via adapters | In-process Python, TS, Go, Java, Kotlin | Provider keys | Apache-2.0 (TP) | Go 1.0 2026-03-31; TS 2.0 GA |
| Gemini CLI | Coding loop | Client and extensions | Yes, incl. remote via A2A | Yes (n/v detail) | Policy engine, plan mode, workspace trust | Seatbelt, Windows, gVisor, LXC | Hooks; headless stream-JSON | Gemini API key or Vertex | Node CLI; headless; ACP; SDK package | Paid keys or Enterprise only from 2026-06-18 | Apache-2.0 | Weekly; v0.61.0 2026-09-23 |
| Pi | Minimal loop | none (design) | none (design) | Tree sessions; fork, switch; context editing | none (design); extension UI dialogs | None | RPC JSONL events | 15+ providers; local via custom providers | TS SDK in-process (Node ≥22.19); RPC subprocess; ACP | Subscription or API key per provider | MIT | Several releases a week |
| goose | Extension-based general agent; recipes | Client; MCP Apps host | Yes | Yes (n/v detail) | Autonomous (default), smart, manual, chat-only | n/v | `goosed` REST and server-sent events; moving to ACP | Many, incl. Ollama | Rust; CLI, `goosed`, ACP server | Provider keys | Apache-2.0 (AAIF) | Weekly; v1.52.0 2026-09-23 |
| OpenHands SDK | Software-agent tools | Yes | Delegation | Event-sourced | Confirmation policy and security analyzer | Docker, Kubernetes or local | Events; REST/WebSocket | LiteLLM, incl. open models | Python; agent-server | Provider keys | MIT | V1 |
| OpenCode | Build and plan agents | Yes | Yes (TP) | create / fork / revert | Permission endpoints | n/v | Server-sent-event bus; OpenAPI 3.1 | Many | HTTP server; JS/TS SDK; ACP | Provider logins or keys | MIT | Very active |
| Hosted harnesses (Claude Managed Agents, OpenAI Agents API) | Vendor loop | Yes (OpenAI) | Coordination (OpenAI) | Server-side | n/v | Vendor cloud or self-hosted sandbox | n/v | Vendor models | REST or SDK; loop runs off the device | API billing | Service terms | OpenAI beta from 2026-09-10 |
| Frameworks (LangGraph, Mastra, Pydantic AI, AI SDK 7) | You build the loop | Yes (most) | Composition | Checkpoints, snapshots, durable engines | Interrupts, needsApproval, tool approvals | Bring your own | OpenTelemetry and telemetry | Any, incl. local | In-process Python or TS | Provider keys | Open source (not re-verified) | 1.x / 7.x |

### Layer 2: protocols

| Protocol | Connects | Version and date | Transport | Human-in-the-loop primitive | UI primitive | Governance and license | Rust / TS |
|---|---|---|---|---|---|---|---|
| MCP | Host ↔ tool and data servers | 2026-07-28 | stdio, Streamable HTTP (stateless) | Elicitation (form or URL); MRTR `input_required`; Tasks | MCP Apps extension | AAIF / Linux Foundation | TS tier 1; Rust beta |
| MCP Apps | Server UI ↔ host | Specification 2026-01-26 | postMessage JSON-RPC in a sandboxed iframe | Via host tool approval | `ui://` HTML | MCP extension | TS SDK and AppBridge |
| ACP | Editor or host ↔ agent subprocess | Protocol v1 | stdio JSON-RPC; remote in progress | Permission requests | Markdown and diffs | Zed + JetBrains; Apache-2.0 | Both |
| AG-UI | App frontend ↔ agent backend | Active 2026 | HTTP, server-sent events, WebSocket | Interrupts | Events, state deltas, frontend tools, MCP Apps | CopilotKit-led; MIT | Both |
| A2A | Agent ↔ agent | v1.0, 2026-03-12 | JSON-RPC, gRPC, REST | `input-required` task state | None | Linux Foundation | SDK set n/v |
| OpenAI Apps SDK | App ↔ ChatGPT | Converged on MCP Apps | as MCP Apps | as MCP Apps | `ui/*` plus `window.openai` | OpenAI | TS |
| A2UI | Agent → declarative UI | v0.9; 1.0 RC targeted Q4 2026 | Payload format | None | Declarative components | Google; Apache-2.0 | Renderers listed |

### Layer 3: GUI operation

| Option | Perception | Embeddable in the owner's app? | Platforms | Auth and plan | Key constraints |
|---|---|---|---|---|---|
| Anthropic `computer_toolset_20260801` | Screenshots and zoom; batched actions | Yes, client-implemented | Any the client implements; Linux reference | API key | Prompt injection; latency; screenshot budget |
| Claude Code / Desktop computer use | Screenshots; OS permissions | No (INF) | CLI macOS; Desktop macOS and Windows | Pro/Max, claude.ai login, interactive only | One session at a time; app tiers |
| OpenAI computer tool / code execution | Screenshots or scripts | Yes, client-implemented | Browser and desktop | API key | Documented step limits |
| ChatGPT desktop (Codex) Computer Use | Accessibility-based per TP; background cursor | No: desktop app only | macOS, Windows | Work/Codex plans; regions | Terminals blocked; Windows foreground only |
| Accessibility-tree MCP servers | AX, UI Automation, AT-SPI tree | Yes | Per operating system | None intrinsic | Coverage depends on the app's accessibility |
| Tauri WebDriver / MCP plugins | DOM | Yes (dev-oriented) | WebDriver: Windows and Linux; macOS via community | None | No official macOS driver |

---

## 7. Questions the owner must answer before fit can be judged

1. **Distribution and credentials.** Will SWBPIPE-class apps go to other engineers? Whose model credentials pay: the owner's, each user's API key, an organisation account, or users' consumer subscriptions? The vendor terms in §1.1 and §1.2 turn on this answer.
2. **Model scope.** Must a single-vendor model be acceptable, must there be multi-provider choice, or must local or offline models be supported for confidential engineering data?
3. **Runtime footprint.** Inside a Tauri app, which sidecars are acceptable: native-binary only, Node or Bun, or Python? What limits apply to installer size, signing and auto-update?
4. **Where the loop runs.** Must it be on-device only, or may a hosted harness hold the conversation or state, given data residency and professional-engineering record-keeping?
5. **Gates.** Which operations are human-only decisions, such as sealed results or solver runs that change the record of design? May any vendor classifier mode (`auto`, `auto_review`, `guardian`) ever resolve a prompt?
6. **Evidence.** Is the vendor transcript acceptable as primary evidence, or must Chirality own a normalised record? What retention, hashing and replay standards apply?
7. **Tool surface.** Will the apps expose solver and model operations as MCP servers, as in-process dynamic tools, or both? Is computer use needed for the owner's own apps, or only for third-party software?
8. **UI contract.** Is the agent a native panel using app components, an MCP Apps or AG-UI surface, or an ACP-style editor pane? What must the human see before and after each operation?
9. **Multi-agent needs.** What parallelism, delegation depth, per-agent sandbox or worktree isolation, and project-management records are required?
10. **The standalone workflow-maker app.** Must it share one harness with the embedded apps? Must workflows (SKILL.md, `AGENTS.md`, workflow packages) be portable across harnesses?
11. **Platforms.** macOS only, or Windows and Linux as well? This affects sandboxes, WebDriver and computer use.
12. **Supplier-change tolerance.** Which pinning and upgrade cadence is acceptable against weekly-to-daily releases and schema drift? Is a proprietary binary under commercial terms acceptable?
13. **Carryover from v3.** Do D-GOV-43's host doctrines carry into v4 as requirements: no filtering, answering every server request, and no veto of the user's configuration?

---

### Sources

Every source below was retrieved on 2026-09-25; publication dates are given where known.

- S1 openai/codex app-server README (main): https://github.com/openai/codex/blob/main/codex-rs/app-server/README.md
- S2 ChatGPT Learn, App Server: https://learn.chatgpt.com/docs/app-server
- S3 ChatGPT Learn, Codex SDK: https://learn.chatgpt.com/docs/codex-sdk
- S4 InfoQ, 2026-02-17: https://www.infoq.com/news/2026/02/opanai-codex-app-server/
- S5 App-server guide gist, 2026-04-29: https://gist.github.com/oneryalcin/ee2c27e2d8aa040da8fbe7eebcc2ecea
- S6 ChatGPT Learn, Authentication: https://learn.chatgpt.com/docs/auth
- S7 manifest.build, 2026-07-01: https://manifest.build/blog/chatgpt-plus-tokens-third-party-harnesses/
- S8 TechTimes, 2026-08-03: https://www.techtimes.com/articles/322791/20260803/sign-chatgpt-launches-what-openai-retains-not-what-gets-shared.htm
- S9 openai/codex repository: https://github.com/openai/codex
- S10 Codex release trackers: https://www.havoptic.com/tools/openai-codex and https://www.gradually.ai/en/changelogs/codex-cli/
- S11 https://docs.ollama.com/integrations/codex and https://developers.openai.com/codex/config-advanced
- S12 https://en.wikipedia.org/wiki/OpenAI_Codex_(AI_agent)
- S13 xnews.sk, 2026-09-11: https://xnews.sk/en/2026/09/11/openai-agents-api-public-beta-cloud-agents/ (the openai.com original returned 403)
- S14 https://code.claude.com/docs/en/agent-sdk/overview
- S15 https://code.claude.com/docs/en/agent-sdk/permissions
- S16 https://code.claude.com/docs/en/agent-sdk/sessions
- S17 https://code.claude.com/docs/en/agent-sdk/hooks
- S18 https://code.claude.com/docs/en/headless
- S19 https://github.com/anthropics/claude-agent-sdk-typescript/blob/main/CHANGELOG.md
- S20 https://support.claude.com/en/articles/15036540-use-the-claude-agent-sdk-with-your-claude-plan
- S21 The Register, 2026-02-20: https://www.theregister.com/2026/02/20/anthropic_clarifies_ban_third_party_claude_access/
- S22 VentureBeat, 2026-05-13: https://venturebeat.com/technology/anthropic-reinstates-openclaw-and-third-party-agent-usage-on-claude-subscriptions-with-a-catch
- S23 https://code.claude.com/docs/en/changelog and https://platform.claude.com/docs/en/release-notes/overview
- S24 https://docs.ollama.com/api/anthropic-compatibility and https://ollama.com/blog/claude (2026-01-16)
- S25 https://fast.io/resources/claude-code-api-sdk-guide/ and https://code.claude.com/docs/en/agent-sdk/typescript
- S26 GitHub changelog, 2026-06-02: https://github.blog/changelog/2026-06-02-copilot-sdk-is-now-generally-available/
- S27 https://github.com/github/copilot-sdk
- S28 https://github.com/openai/openai-agents-python
- S29 Help Net Security, 2026-04-16: https://www.helpnetsecurity.com/2026/04/16/openai-agents-sdk-harness-and-sandbox-update/
- S30 https://developers.openai.com/api/docs/guides/agents/sandboxes
- S31 https://adk.dev/
- S31a https://futureagi.com/blog/what-is-google-adk-2026/
- S32 Google Developers Blog, 2026-03-31: https://developers.googleblog.com/adk-go-10-arrives/
- S33 https://geminicli.com/docs/changelogs/
- S34 Google Developers Blog, 2026-05-19: https://developers.googleblog.com/an-important-update-transitioning-gemini-cli-to-antigravity-cli/
- S34a The Register, 2026-05-20: https://www.theregister.com/ai-ml/2026/05/20/bye-bye-gemini-cli-google-nudges-devs-toward-antigravity/5243605
- S35 https://github.com/google-gemini/gemini-cli
- S36 https://pi.dev/
- S37 https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/README.md
- S38 https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/rpc.md
- S39 https://github.com/earendil-works/pi/releases
- S40 agent-wars, 2026-04-08: https://agent-wars.com/news/2026-04-08-pi-agent-creator-joins-earendil
- S41 https://github.com/aaif-goose/goose/releases
- S42 goose discussion #7697 (March 2026): https://github.com/aaif-goose/goose/discussions/7697
- S43 goose blog, 2026-04-07: https://goose-docs.ai/blog/2026/04/07/goose-moves-to-aaif/
- S44 https://goose-docs.ai/docs/guides/goose-permissions/
- S45 https://github.com/aaif-goose/goose
- S46 https://docs.openhands.dev/sdk and https://github.com/OpenHands/software-agent-sdk
- S46a https://arxiv.org/abs/2511.03690
- S47 https://opencode.ai/docs/server/ and https://github.com/anomalyco/opencode
- S48 arXiv 2609.00006, 2026-07-15: https://arxiv.org/abs/2609.00006
- S49 https://en.wikipedia.org/wiki/OpenClaw
- S50 Vercel, 2026-06-25: https://vercel.com/blog/ai-sdk-7
- S51 https://mastra.ai/docs/workflows/suspend-and-resume and https://dev.to/gabrielanhaia/mastra-in-2026-what-it-is-when-to-use-it-and-how-it-compares-2go1
- S52 https://www.langchain.com/blog/langchain-langgraph-1dot0 and https://docs.langchain.com/oss/python/langgraph/interrupts
- S53 https://ai.pydantic.dev/durable_execution/overview/
- S54 MCP blog, 2026-07-28: https://blog.modelcontextprotocol.io/posts/2026-07-28/
- S55 https://modelcontextprotocol.io/specification/2026-07-28
- S56 https://modelcontextprotocol.io/specification/2026-07-28/client/elicitation
- S57 https://modelcontextprotocol.io/extensions/tasks/overview
- S58 https://modelcontextprotocol.io/extensions/apps/overview
- S59 MCP blog, 2026-01-26: https://blog.modelcontextprotocol.io/posts/2026-01-26-mcp-apps/
- S60 AAIF, 2026-07-21: https://aaif.io/blog/mcp-2026-07-28-whats-changing-and-how-to-migrate
- S61 DevMoment, August 2026: https://www.devmoment.dev/journal/mcp-apps-field-log-2026
- S62 https://developers.openai.com/apps-sdk/mcp-apps-in-chatgpt
- S63 https://agentclientprotocol.com/overview/introduction, https://github.com/agentclientprotocol/agent-client-protocol and https://agentclientprotocol.com/get-started/agents
- S64 Zed, 2026-01-28: https://zed.dev/blog/acp-registry
- S65 https://www.danilchenko.dev/posts/agent-client-protocol/
- S66 https://docs.ag-ui.com/introduction and https://github.com/ag-ui-protocol/ag-ui
- S67 TechCrunch, 2026-05-05: https://techcrunch.com/2026/05/05/copilotkit-raises-27m-to-help-devs-deploy-app-native-ai-agents/
- S68 A2A, 2026-03-12: https://a2a-protocol.org/latest/announcing-1.0/
- S69 InfoQ, July 2026: https://www.infoq.com/news/2026/07/google-a2ui-genui/
- S70 https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation
- S70a AAIF member count and agentgateway reports (search results; the page was not fetched)
- S71 https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool
- S72 https://code.claude.com/docs/en/computer-use
- S73 https://developers.openai.com/api/docs/guides/tools-computer-use
- S74 https://learn.chatgpt.com/docs/computer-use
- S75 9to5Mac, 2026-04-16: https://9to5mac.com/2026/04/16/openais-codex-app-adds-three-key-features-for-expanding-beyond-agentic-coding/
- S76 Daniel Vaughan, 2026-04-17: https://codex.danielvaughan.com/2026/04/17/codex-app-computer-use-macos-background-gui-automation/
- S77 https://github.com/CursorTouch/MacOS-MCP and https://dev.to/devandrew/mastering-desktop-automation-the-state-of-computer-use-mcp-servers-in-2026-2dha
- S78 https://support.microsoft.com/en-us/windows/experimental-agentic-features-a25ede8a-e4c2-4841-85a8-44839191dfb3
- S79 https://v2.tauri.app/develop/tests/webdriver/ and https://danielraffel.me/2026/02/14/i-built-a-webdriver-for-wkwebview-tauri-apps-on-macos/
- S80 https://github.com/P3GLEG/tauri-plugin-mcp
- S81 https://v2.tauri.app/develop/sidecar/
- S82 Enterprise DNA, August 2026: https://enterprisedna.co/resources/news/anthropic-browser-use-computer-use-skills-api-enterprise-ga-august-2026/
- LOCAL1 `/Users/ryan/ai-env/projects/chirality/.claude/worktrees/chirality-app-v4-architecture-9f35c4/projects/chirality-runtime/docs/CODEX_MVP_INTEGRATION.md`
- LOCAL2 `/Users/ryan/ai-env/projects/chirality/.claude/worktrees/chirality-app-v4-architecture-9f35c4/projects/chirality-runtime/packages/engine-pi-omlx/package.json` and `/Users/ryan/ai-env/projects/chirality/.claude/worktrees/chirality-app-v4-architecture-9f35c4/projects/chirality-runtime/packages/engine-claude/src/index.ts`

**Evidence note.** I used WebSearch, WebFetch and read-only Bash. Two pages could not be fetched: openai.com returned 403, and npm returned 403. For those, I relied on the secondary reports cited.
