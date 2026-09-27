# v3 Runtime and App: what they do, and how much v4 can reuse (read-only, main@2b0572fe0)

**Basis.** Every path below is relative to REPO_ROOT at `2b0572fe0`. The worktree HEAD `bf90ffc4d` has no diff from that revision in `projects/chirality-runtime` or `projects/chirality-app-dev`. Abbreviations: **RT** = `projects/chirality-runtime`, **FE** = `projects/chirality-app-dev/frontend`, **RUN** = `projects/chirality-app-dev/execution/_Coordination/AgentRuns/APP_V3_CODEX_HOST_REPLATFORM_20260912`.

**Method.** Line counts come from `wc -l`. "Unreachable" comes from an import-graph walk: relative imports plus `@chirality/*` package aliases, starting from the Next pages and routes, `electron/main.ts`, `preload.ts`, and `daemon/src/standalone-bin.ts`. Barrel re-exports make some unused runtime modules look reachable, so for those I checked where they are actually constructed. Nothing was built or run, and no files were written.

---

## Q1. What the Runtime service does for the v3 App

**Topology [implemented].**
- Electron main starts the service with `utilityProcess.fork` (`FE/electron/runtime-service-launcher.ts:1-63`).
- The service builds everything in `startAppOwnedRuntime` (`RT/packages/daemon/src/app-owned-composition.ts:154-257`).
- Inside it: one stock `codex app-server` child, a `RuntimeDaemon` with HTTP and SSE on a Unix socket, and a per-launch token written to a file (`:249-254`).

**Size [implemented].**
- Package sources total 20,191 lines in 85 files: contracts 5,402; core 8,642; daemon 3,963; client 926; cli 529; engine-pi-omlx 670; engine-claude 59.
- Tests: 9,609 lines in `RT/tests` (42 files), plus client 374 and cli 380.
- [executed check (record)] Runtime suite: 34 files / 309 tests passed, later 312 (`RUN/RUN_LOG.md:101-104`, `:162`).

**Protocol use [implemented].** The Runtime calls only 16 App Server methods: `initialize`, `thread/start|resume|settings/update|inject_items|loaded/list|read|unsubscribe`, `turn/start|steer|interrupt`, `account/read|login/start|login/cancel|logout`, `model/list`.
- It never passes `modelProvider`.
- It never calls `thread/list`, `skills/list` or `config/read`.
- Request payloads are hand-typed; no generated types are used.

### Responsibilities

"Native?" means whether Codex App Server already provides the behaviour. "Main-process?" means whether it could run in the App's own main process instead of a separate service.

| Responsibility | Where / size | Native? | Needed in v4? | Main-process? |
|---|---|---|---|---|
| **Codex process lifecycle and JSON-RPC client** | `daemon/src/codex-app-server-client.ts` (332). Spawns `codex -c cli_auth_credentials_store="file" -c thread_unload_delay_secs=0 app-server` with `CODEX_HOME` set to the effective home (`:41`, `:51-89`). Newline-delimited framing, 64 MB buffer cap (`:167-176`). Id correlation, 60 s default timeout. Notification fan-out. Every server request is answered, defaulting to `-32601` (`:202-207`). `initialize` sets `experimentalApi: true` (`:271`). Restart backoff 1–30 s, stops after 5 failures in 180 s (`:291-316`); SIGTERM then SIGKILL after 2 s. [implemented]. Tests: `tests/codex-app-server-client.test.ts` (102) plus fixture `fake-codex-app-server.mjs` (164) [test defined] | No; this is the host's job | Yes | Yes. Electron: near-verbatim. Tauri: a Rust port [agent inference] |
| **Version pin** | `assertCodexVersion` (`app-owned-composition.ts:118-128`), `FE/scripts/verify-codex-pin.mjs`, `FE/electron/codex-executable.ts` (95) [implemented] | No | Yes | Yes |
| **Effective Codex home ("auth overlay")** | `daemon/src/codex-effective-home.ts` (90). Symlinks every `~/.codex` entry into a private home except `auth*`, `models_cache.json` and `*.lock` (`:33-35`). So config, skills, MCP definitions and **sessions** are shared with the user's other Codex clients (`RT/README.md:31-37`) [implemented]. Test 91 [test defined] | Partly: `CODEX_HOME` is native; the overlay is Chirality's own | Only if Chirality keeps sign-in separate from the user's Codex CLI [agent inference] | Yes (trivial) |
| **Sign-in and model catalog** | `codex-login.ts` (107), `hosted-bootstrap.ts` (90), daemon hosted routes (`runtime-daemon.ts:413-478`). Only `{type:"chatgpt"}` login (`codex-login.ts:59`); **no API-key sign-in**. The "provider-network consent" route is kept as a no-op [implemented] | Yes (`account/*`, `model/list`); Chirality only relays | A thin version; API key must be added | Yes |
| **Answering server requests** | `codex-supervisor.ts:694-717` handles 5 approval methods plus user input, elicitation and dynamic tool calls. `account/chatgptAuthTokens/refresh` and `attestation/generate` get an explicit error (`:40-46`). Response shapes per method at `:719-735`. Pending requests are cancelled at turn end (`:605-611`). Answer route: `runtime-daemon.ts:758-768` [implemented]. D-GOV-43.proposed.md:123-127 records ten server-request types [described design] | The requests are Codex's; answering is the host's job | Yes | Yes |
| **Thread and turn orchestration** | `CodexSupervisor` (735). `thread/start` with `developerInstructions`, `config` (native roles), approvalPolicy, sandbox, model, `dynamicTools` (`:219`). Plan Mode via `thread/settings/update collaborationMode` (`:232`). `turn/start` sends text and localImage items (`:259`). `turn/steer` and `turn/interrupt` (`:372`, `:397`). Child-thread tracking (`:516-545`) [implemented]. Tests: `codex-supervisor.test.ts` 452, native-steering 136, codex-application-tools 254, codex-attachment-adapter 165 [test defined] | The primitives are native | Yes, simpler, and `modelProvider` must be added | Yes |
| **Cold-resume instruction supersession** | `codex-supervisor.ts:186-217` injects a developer message via `thread/inject_items`. `:277-350` walks `thread/loaded/list` and `thread/read`, then unsubscribes, before resuming. The comment says Codex 0.154 ignores hot-resume overrides [implemented] | Workaround for Codex behaviour | Behaviour probably yes; re-verify on each pin [agent inference] | Yes |
| **Turn ownership separate from observation** | `daemon/src/turn-registry.ts` (388): frame buffer, subscribe after a sequence number, 10 min retention. Daemon SSE with keepalives (`runtime-daemon.ts:962+`) [implemented]. Tests: turn-registry 267, turn-hardening 529 [test defined] | Codex already runs the turn independently of any client [agent inference] | It exists because of the socket/SSE hop; with an in-process host, only a small replay buffer for renderer reloads remains [agent inference] | Yes |
| **Session index and event log** | `core/src/session-store.ts` (1,243) and `project-registry.ts` (330) keep a per-session `session.json` and `events.jsonl` of translated events. `persistEvent` re-reads the whole file to de-duplicate each event (`:813-822`) [implemented]. Tests: session-and-residency 220, native-message-replay 29 [test defined] | Codex persists threads itself. D-GOV-43.proposed.md:115-129 calls v3 "re-deriving state that Codex persists" [described design] | Chirality metadata (role, workflow, basis) yes; a duplicate transcript is doubtful [agent inference] | Yes |
| **Instruction composition** | `runtime-method-service.ts` (675; product `AGENTS.md` at `:561-565`), `renderDeveloperInstructions` (`delegated-engine-adapter.ts:37-43`). Per-role TOML files written and passed as `agents.<role>.config_file` (`product-native-role-config.ts:8-37`, `native-role-config.ts:155-199`). `instruction-basis-store.ts` (679) keeps frozen bases and history [implemented]. Tests: instruction-basis-and-method-transition 740, native-role-config 66, product-native-role-config 36 [test defined] | Inputs are native (`developerInstructions`, `[agents]`); composing them is Chirality's own | Yes | Yes |
| **Workflow and skill catalog** | `method-catalog.ts` (648), `method-transition.ts` (118). Scans project, user and bundled workflows and skills itself [implemented]. Governance says App skills follow native `skills/list` (`docs/AGENT_WORKFLOW_RUNTIME.md:72-74`) [described design]; v3 does not call it. Tests: method-catalog 349 [test defined] | Skills yes; workflows no | Workflows yes | Yes |
| **Native plan registry** | `native-plan-registry.ts` (193) plus revisions, clarifications and export (`runtime-method-service.ts:303-412`) [implemented]. [executed check (record)] S-1 PASS (`RUN/spike/EVIDENCE.md:11`) | Plan items and collaboration mode are native; revision numbering and export are Chirality's | Yes, simplified | Yes |
| **Application dynamic-tool registry** | `daemon/src/application-tools.ts` (155), `contracts/src/application-tools.ts` (92), supervisor `:640-692`, routes `runtime-daemon.ts:663-690`, plus `application-tools.json` [implemented]. Tests: 159 + 116 [test defined] | `dynamicTools` and `item/tool/call` are native; the HTTP registry exists so an *external* host can answer | Only if the standalone App offers its own tools. Under D-19, host apps use Pi instead [agent inference] | Yes |
| **Managed delegation** | Native Codex multi-agent roles (`agents.max_depth=2`, `native-role-config.ts:184-197`) plus supervisor child tracking. Wrapped in the `DelegatedRuntime` worker/generation abstraction (437), `worker-retirement.ts` (119), `retirement-failure.ts` (63) and `delegated-engine-adapter.ts` (342) [implemented] | Native (Codex multi-agent) | The native part yes; the worker/generation layer no [agent inference] | Yes |
| **Translation into Chirality's own event names** | `delegated-engine-adapter.ts:180-330` maps Codex notifications to `tool.started|progress|completed`, `tool.permission`, `codex.notification`, `codex.request(.resolved)`, keeping raw params under `codex`. `UIEvent` framing (`contracts/src/events.ts`, `event-schema.ts`) [implemented] | No; this is the "generic vocabulary" v4 declines | No | — |
| **Socket API, tokens, client, CLI** | `runtime-daemon.ts` (1,460), `auth-registry.ts` (236), `client` (926), `cli` (529), `signal-shutdown.ts` (118) [implemented]. Tests: daemon 1,184, runtime-v3-api 838, runtime-daemon-signal 217, bootstrap-api 163, client 374, cli 380 [test defined] | — | Not for an in-process host | — |

### Unwired or legacy code in the production composition

- **Governed Agent 1 run coordinator** [implemented]
  - `agent1-run-coordinator.ts` (930) is never constructed: the `agent1Runs` argument is `undefined` at `app-owned-composition.ts:226`.
  - So `runAgent1` throws `REQUIRED_DELEGATION_MISSING` (`runtime-service.ts:664-673`).
  - The `/runs` route (`runtime-daemon.ts:591-616`) and CLI `runAgent1` are dead.
  - Its test (`agent1-run.test.ts`, 551) exercises the unwired class.
- **Classes never constructed in production** [implemented]: `ProcessSupervisor` (138), `DescendantTracker` (116), `CompatibilitySessionPolicy` (58), `physical-filesystem.ts` (35).
- **Offline stubs** [implemented]
  - `ResidencyCoordinator` (347) runs with offline stubs, and the credential store is stubbed (`app-owned-composition.ts:179-181`, `:225`).
  - So `/v1/credentials` and `/v1/models` (`runtime-daemon.ts:515-561`) are inert.
  - `EngineRegistry` (31) and the `AgentEnginePort` multi-engine layer carry only the Codex adapter.
- **Engine packages** [implemented]: `engine-claude` (59) and `engine-pi-omlx` (670) are imported only by tests (`pi-turn-runtime` 395, `omlx-client` 73, `pi-packaging` 154) and by FE devDependencies (`FE/package.json:61-62`).
- **Contracts modules used only by unreachable App code or the barrel** [implemented]: `harness/tool-descriptor.ts` (1,401), `engine-conformance.ts` (541), `domain-profile.ts` (252), `operation-proposal.ts` (142), `tool-catalog.ts` (159).
- **Total:** roughly **4.8k of 20.2k** runtime source lines are unwired, plus about 3.7k that exist only for the socket boundary [agent inference from the counts above].

---

## Q2. Hosting `codex app-server` without the Runtime service

### What a main process must do directly (taken from v3 code)

1. Resolve the pinned binary and check `codex --version`. The binary is native, not Node: it ships from `@openai/codex-darwin-arm64/vendor/aarch64-apple-darwin` (`FE/package.json:118-124`) [implemented].
2. Prepare `CODEX_HOME`, as in the overlay above, if Chirality keeps its own sign-in.
3. Spawn with piped stdio, redact stderr, and terminate with SIGTERM then SIGKILL [implemented, `codex-app-server-client.ts:51-89`].
4. Frame newline-delimited JSON-RPC 2.0: correlate ids, time out requests, fan out notifications, and dispatch server requests to one handler that **always answers** [`:108-208`].
5. Send `initialize` with `experimentalApi: true`. Plan Mode's `collaborationMode` is experimental and absent from the exported schema (`docs/governance_harness/_PROPOSALS/D-GOV-43_2026-09-11_codex_host_replatform/D-GOV-43.proposed.md:129-132`) [described design].
6. Restart with backoff. On exit, fail live turns and cancel pending requests [`codex-supervisor.ts:612-624`].
7. Use the method-specific answer and cancel shapes [`codex-supervisor.ts:719-735`].
8. Handle account, thread and turn calls as listed in Q1. v4 adds `modelProvider` per thread and API-key login [agent inference].
9. Compose instructions and role files, and persist Chirality metadata.

**Types [described design]**
- The spike used `codex app-server generate-json-schema|generate-ts` to establish protocol facts (`RUN/SPIKE_DESIGN.md:11-16`), but no generated types were committed or imported.
- An earlier 0.149 probe of those generators failed with exit 2 because the packaged assets lacked the wrapper (`RT/execution/_Coordination/AgentRuns/RUNTIME_EXECUTION_2026-09-06/TECHNICAL_AUDIT/REPORT.md:44`) [executed check (record)].
- T8 cites an upstream TypeScript schema tree, `codex-rs/app-server-protocol/schema/typescript/v2/ThreadStartParams.ts` (`projects/chirality-app-v4/execution/_Coordination/AgentRuns/V4-CONCEPT-20260925/tasks/T8-t3code.return.md:95`).
- Generated types omit the experimental fields, so a thin hand-written supplement would remain [agent inference].

**Electron main [agent inference]**
- Items 1–9 are Node code that already exists. `CodexAppServerClient`/`Host`, `CodexLogin`, the effective home and most of `CodexSupervisor` could run in main almost unchanged.
- The renderer would reach them over preload IPC instead of Next routes.
- Topology B had already found the precedent: "The daemon already runs in Electron main" (`RUN/TOPOLOGY_COMPARISON.md:233-236`).

**Tauri main [agent inference]**
- Rust would own spawn, stdio and restart (`tokio::process` plus `serde_json`). Either the JSON-RPC logic is ported to Rust, or Rust pipes lines to a TypeScript client in the webview.
- The v3 TypeScript client is about 330 lines, so either choice is small. The larger ports are the server-request policy and instruction composition.
- SWBPIPE currently uses only `tauri-plugin-dialog`, with no shell or sidecar plugin (`projects/chirality-piping/apps/desktop/src-tauri/Cargo.toml:15-33`) [implemented].

### v3 records on topology size and risk (`RUN/TOPOLOGY_COMPARISON.md`)

**Common work (C1–C6, `:92-104`).** Judged to be "70 to 80 percent of the total effort" and identical under A1, A2 and B [described design; the effort figures are marked judgment (U1, `:209`)].

| Topology | Effort | Risk | Lifecycle and maintenance |
|---|---|---|---|
| **A1** (launchd daemon kept) | Least new code | Low to medium | Three processes and launchd; highest maintenance; reconnection work unsized (`:117-137`) |
| **A2** (App-owned child service) | About 800 lines removed versus A1 | Low to medium | Keeps "about 2,600 lines" of transport: client, port, SSE, daemon routes (`:139-155`) |
| **B** (in-process host behind the existing port) | Deletes about 4,000 transport/lifecycle lines against 500–800 new | Medium: new composition, and a GUI crash ends the Codex children, mitigated by thread persistence | One process; lowest maintenance (`:157-184`) |

**Recommendation history.**
- The first recommendation was "B over A2, narrowly" (`:233-249`).
- The §8 addendum moved it to A2 because "A Node in-process library cannot be embedded in a Tauri main process" and the flagship App would then exercise the sidecar embedding path (`:284-302`).
- §9 corrections: size claims are estimates, and PEC compatibility was overstated (`:324-347`).

**Ruling (`docs/governance_harness/_DECISIONS/D-GOV-43_supplement_topology_A2.md`).**
- The owner chose A2 (`:25-35`).
- It recorded the constraint "Keep the Runtime host independent of Electron and Next" (`:70-73`).
- "Reuse is assessed by behaviour, not line counts" (`:92-94`).

**Outcome [executed check (record)].** A2 passed S-1..S-8 (`RUN/RUN_LOG.md:163-164`). Its build is recorded in `RUN/BUILD_EVIDENCE_20260912.md`.

**What changed since [agent inference].** A2 won on one premise: host applications would reuse the Node Runtime as a sidecar. D-19 instead gives host applications a Pi-based embedded agent. That premise no longer holds, which leaves B's findings (lowest maintenance, one process) as the standing comparison for the standalone App. The consumer guide also records that no Tauri sidecar distribution exists (`RT/docs/APPLICATION_CONSUMER_GUIDE.md:20-23`, `:173`).

---

## Q3. Reusing the frontend

**Size [implemented].**
- `FE/src`: components 14,176; lib 30,969; app 2,021; `globals.css` 4,661.
- Tests: 56,357 lines in 236 files.
- [executed check (record)] 201–202 files / 2,066 tests passed (`RUN/RUN_LOG.md:103`, `:168`).

**Transport chain today [implemented].**
- The browser calls `lib/harness/client.ts` (567) with `fetch` against 33 Next route files (828 lines).
- The routes call the ports in `lib/runtime-client` (1,737), which call `RuntimeClient`, which calls the socket.
- Next runs inside Electron main (`FE/electron/main.ts:573-600`).
- Electron lifecycle for the service: `runtime-service-host.ts` 557, `runtime-connectivity.ts` 255, `runtime-socket-watch.ts` 263.
- Filesystem work runs through Next routes too: `app/api/working-root` and `project` (974 lines) plus `lib/workspace/filesystem.ts` (1,302).

**Next.js coupling in client code is shallow [implemented].** Only `next/navigation` URL state (`chat-panel.tsx:8`, `woven-dialogue-shell.tsx:5`, `persona-picker.tsx:3`) and one `next/link` (`shell-frame.tsx:3`). Tests mock `next/navigation` in 14 files and `lib/harness/client` in 11.

### Components that carry v3's valuable interactions

| Interaction | Path (lines) | Coupling | Tests [test defined] |
|---|---|---|---|
| Request cards (approvals, questions, elicitation) | `components/shell/request-card.tsx` (286); `lib/shell/harness-event-views.ts` (610) | View is pure, with an injectable `answer` (`:152`); `useLiveSessionRequests` polls the Next API; rows derive from translated events | request-card 110, live-session-requests 71, harness-event-views 283 + 94 |
| Legacy permission cards | `components/shell/permission-requests.tsx` (168) | `lib/harness/client` | permission-cards 70 |
| Plan panel (Revise in chat / Execute plan / Turn into workflow) | `components/shell/native-plan-panel.tsx` (137; buttons at `:126-128`) | Presentational model props; imports only contracts types | native-plan-panel-executions 77; API clarifications 127 |
| Workflow draft review and registration | `components/woven-dialogue/workflow-draft-review.tsx` (85); `lib/harness/workflow-drafts.ts` (27); server `app/api/working-root/workflow-drafts/workflow-draft-store.ts` (181) | `fetch('/api/working-root/workflow-drafts')` | 70; API 149 + 62 |
| Activity views | `activity-shelf.tsx` (260), `tool-stream-view` 72, `subagent-stream-view` 66, `transcript-stream-view` 107 | Translated events via `harness-events-provider.tsx` (111), `deriveTranscriptView` from contracts | activity-strip 109, presentation 178, local-state 73 |
| Agents view | `agents-projection.tsx` (180), `lib/woven-dialogue/operator-projection.ts` (251), `recorded-agent-hierarchy.ts` (332) | Runtime session-record data shapes | 206, 124 |
| Replay lens | `selected-session-replay-lens.tsx` (382), `lib/woven-dialogue/selected-session-replay.ts` (368) | Runtime `/replay` (events, transcript, instruction bases) | 218, 315 |
| Attachment import | `lib/harness/ui-attachments.ts` (137), `lib/shell/native-attachments.ts` (19), `FE/electron/attachment-picker.ts` (161, imports `runtime-core`) | `window.chirality.attachments` preload bridge | 75, 93, chat-panel-native-attachments 129, turn-route-attachments 152 |
| Turn phases and outcome states | `lib/shell/turn-phase.ts` (79), `turn-activity.ts` (124), `components/shell/turn-activity.tsx` (31), `live-work-store.ts` (35) | Pure | turn-activity 64; phases also covered in chat-panel tests |
| Host surfaces | `chat-panel.tsx` (2,178), `woven-dialogue-shell.tsx` (1,068) | `next/navigation`, preload bridges, client | chat-panel 7 files (~2.8k), woven-dialogue-shell 862, runtime-reconnect 336 |

### Dead code [implemented]

- **Legacy route elements are discarded.** All four routes render `WovenDialogueShell`, and the `legacy` prop is thrown away with `void legacy` (`components/woven-dialogue/woven-dialogue-route.tsx:14-20`).
  - Portal/pipeline/workbench shells and surfaces are 15 files and 3,564 lines, reachable only through that discarded prop or `not-found.tsx`.
  - Examples: `pipeline-surface.tsx` 1,132, `workbench-surface.tsx` 603, `app-shell.tsx` 389.
- **Unreachable from any product entry:** 50 files, about 16.4k lines.
  - The multi-engine harness is about 6.3k of that: Anthropic/Claude/Pi managers and mappers, `sdk-message-mapper` 1,276, `turn-engine` 434, `engine-registry` 144, and others.
  - Also unreachable: MCP tool modules (~3.5k), `managed-delegation.ts` 992, `chirality-hooks.ts` 745, `permission-overlay.ts` 494.
  - Some of these are still imported by `FE/scripts/*` and tests, but not by the product.
- **API-key settings** cover Anthropic and oMLX only and are hidden when the account is hosted (`components/settings/settings-view.tsx:35`, `api-key-settings.tsx:83-99`).

### Portability [agent inference]

- **Move with modest change:**
  - native-plan-panel, turn-phase/turn-activity, chat-markdown, `RequestCard` (the view part), workflow-draft-review (swap its two fetches), attachment helpers.
  - The folder, attachment and plan-export bridge interfaces, which are already abstracted behind `window.chirality`.
  - `globals.css` and CSS modules work under Vite.
- **Tied to v3's transport or data shapes:**
  - Anything built on translated events or Runtime DTOs: harness-event-views, activity shelf, agents projection, replay lens, harness-events-provider.
  - Everything in `lib/harness/client`, the Next routes and `lib/runtime-client`.
  - `chat-panel` and `woven-dialogue-shell`, which mix all of the above.
  - If native App Server items go to native presentation, the derivations would be rebuilt over native items.
- **React version:** v3 uses React 18.2 (`FE/package.json:53`); SWBPIPE uses React 19 (`projects/chirality-piping/apps/desktop/package.json:22`).

---

## Q4. Evidence on Electron + Next versus Tauri + React/Vite

**Facts**
- **Codex does not need Node** [implemented]. It is a signed native binary tree (`FE/electron/codex-executable.ts:15-25`). npm is only the delivery vehicle.
- **The Runtime service does need Node** [implemented]. It runs on Electron's Node through `utilityProcess`, because the `runAsNode` fuse is off (`FE/electron/runtime-service-launcher.ts:1-13`; `FE/package.json:98-105`). The spike design had planned `ELECTRON_RUN_AS_NODE` (`RUN/SPIKE_DESIGN.md:386-389`); implementation had to change course.
  - Under Tauri, a Node sidecar or a rewrite would be required (`RT/docs/APPLICATION_CONSUMER_GUIDE.md:20-23`, `:173`) [described design].
- **Signing and packaging experience exists only for Electron.**
  - v3 has Developer ID signing with hardened runtime, and a custom `mac.sign` hook that signs both Codex binaries, with a JIT entitlement for `codex-code-mode-host` (`FE/scripts/sign-electron-runtime-v2.mjs:1-60`) [implemented].
  - The procedure is recorded in `RUN/PACKAGING_PROCEDURE.md:20-53` [described design].
  - [executed check (record)] One build produced a signed 337,038,438-byte DMG. The first sign-hook attempt failed; `spctl` rejected the bundle before notarization; notarization is an owner act (`RUN/BUILD_EVIDENCE_20260912.md:25-32`, `:49-61`).
  - SWBPIPE ships unsigned `.app` zips, with no notarization for v0.1 (DEC-057; `projects/chirality-piping/docs/BUILD_AND_RELEASE.md:40-48`, `:223-224`). Its Tauri config sets `csp: null` and bundle target `app` only (`projects/chirality-piping/apps/desktop/src-tauri/tauri.conf.json`) [implemented].
- **No in-place auto-update in either stack.** v3 checks the GitHub latest-release API and opens the download page (`FE/electron/app-update-source.ts:8-21`, `app-update.ts:432`, `main.ts:963`) [implemented]. SWBPIPE has no updater.
- **Electron hardening already written** [implemented]: `renderer-window-policy.ts` (774), `ipc-sender-policy.ts`, fuses, `proof:packaged-security` scripts. Electron-specific code totals 5,328 lines in `FE/electron`.
- **Governance constraint** [described design]: "Keep the Runtime host independent of Electron and Next" (D-GOV-43 supplement `:70-73`).

**For keeping Electron + Next [agent inference]**
- Signing, notarization and bundling of the Codex binaries are proven and scripted.
- The existing Node JSON-RPC and login code can move into main with little rewriting.
- Renderer hardening and the preload bridges exist.

**Against keeping Electron + Next [agent inference]**
- Next is used here as an in-process HTTP server for 44 route files that exist to relay to the Runtime or the filesystem. With no Runtime service, Next contributes URL state and a server that is not needed.
- Two frontend stacks would sit across Chirality products, against the "few stacks" principle.

**For Tauri + React/Vite [agent inference]**
- Shares SWBPIPE's stack (Vite 7, Vitest 4, React).
- Codex's native binary fits the sidecar model.
- The component logic ports, because Next coupling is shallow.

**Against Tauri + React/Vite [agent inference]**
- The Codex host (JSON-RPC, request answering, restart, overlay) must be re-implemented in Rust or relayed to the webview.
- Signing, JIT entitlements, notarization and a security-policy baseline must be re-established; SWBPIPE has no signing experience to reuse.
- React 18 to 19 alignment is needed.
- Bundle-size comparison is unmeasured: the 337 MB DMG has no recorded split between Electron and Codex.

---

## Disposition table [agent inference]

| Component / responsibility | Keep as is | Move / simplify | Drop |
|---|---|---|---|
| Codex JSON-RPC client and restart host | | ✓ into main process (Electron verbatim; Tauri port) | |
| Version pin check and `verify-codex-pin` | ✓ | | |
| Effective-home overlay | | ✓ only if separate sign-in stays | |
| CodexLogin / hosted-bootstrap routes | | ✓ direct `account/*`; add API key; drop consent no-op | |
| Server-request answering rules and shapes | | ✓ | |
| CodexSupervisor thread/turn calls, Plan Mode, steer, interrupt | | ✓ add `modelProvider`; drop worker/generation layer | |
| Cold-resume instruction supersession | | ✓ re-verify on newer pin | |
| DelegatedRuntime, worker retirement, delegated-engine-adapter | | | ✓ |
| Translation into Chirality event names, `UIEvent`, contracts vocabulary | | | ✓ |
| TurnRegistry and daemon SSE | | ✓ small replay buffer at most | |
| SessionStore `events.jsonl` transcript copy | | ✓ metadata index only; transcript from Codex | |
| InstructionBasisStore | | ✓ | |
| Instruction composition and native role TOML | | ✓ (move, same behaviour) | |
| Workflow catalog | ✓ | skills via `skills/list` | |
| Native plan registry and export | | ✓ | |
| Application dynamic-tool registry | | | ✓ for standalone (unless App-owned tools) |
| Steering receipts | | ✓ | |
| Socket API, AuthRegistry tokens, RuntimeClient, CLI, signal-shutdown | | | ✓ |
| Agent 1 coordinator, ProcessSupervisor, DescendantTracker, residency, credentials, EngineRegistry | | | ✓ |
| engine-claude, engine-pi-omlx, contracts harness legacy | | | ✓ (history only) |
| Next harness routes, `lib/harness/client`, `lib/runtime-client` ports | | | ✓ |
| Working-root routes, `filesystem.ts`, workflow-draft store | | ✓ to main-process commands | |
| RequestCard / RequestCards | | ✓ native payload shapes | |
| NativePlanPanel | ✓ | | |
| WorkflowDraftReview view | ✓ | (store moves) | |
| Activity shelf, stream views, harness-event-views | | ✓ rebase on native items | |
| Agents projection and replay lens | | ✓ from Codex thread data plus Chirality metadata | |
| Attachment helpers and picker | | ✓ | |
| turn-phase / turn-activity | ✓ | | |
| chat-panel / woven-dialogue-shell | | ✓ split; replace `next/navigation` | |
| Legacy portal/pipeline/workbench shells and unreachable `lib/harness` | | | ✓ |
| Electron runtime-service host, connectivity, socket watch | | | ✓ (replace with a Codex child host) |
| Electron signing hook, fuses, window policy, update check | ✓ if Electron | re-establish if Tauri | |
