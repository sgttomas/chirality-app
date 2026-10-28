# OBS-2 — local observations of Codex App Server at pin 0.158.0 against a local LM Studio model (observation record)

- **Date:** 2026-10-01, 19:50–20:24 UTC. **Node:** OBS-2 (Type 2 TASK) of run `APP-V4-DESIGN-PASS-3-20261001`, dispatched by HELP_HUMAN.
- **Standing:** dated observations at one version (Codex 0.158.0, LM Studio 0.4.16+2, one model). **Not qualification** of the pin, the provider or the model; not an X-02 fixture; no App candidate was involved. Every answer the harness gave to a supplier request has origin `observation-harness`; none is a person's act or A14 evidence.
- **Authority:** owner DECISION-K3 K-11 (local-model observations only; `OWNER_DECISIONS.md`, sha256 `9d18c40dd7d8…`); ruling R17-16 items O-1…O-7 (`R17_RESOLUTIONS.md`, `b0af81bcbad9…`); `BRIEFS.md` "OBS-2" (`b261394112d7…`); method from `WAVE_B/OBS-1_BRIEF.md` (`b3e7a4b6d98f…`) §3, §6, §7, §8, §12, and the OBS-1 record (`OBS_1_0.158.0.md`, `7b984b541edc…`) and harness (`prototype/obs1/obs1_harness.py`, `0b1325547b78…`). Two additions from HELP_HUMAN during the run, under the same limits: **O-4a/O-4b** (native child role; task guidance against delegation) and **O-8** (plan mode). None of these files was edited.
- **Result in one line:** O-1, O-2, O-3, O-5, O-6 and O-7 were observed on the stock pairing. O-4 (delegation) could **not be provoked** on the stock pairing, because Codex sends its delegation tools only inside a `namespace` tool and LM Studio 0.4.16 drops `namespace` tools. It was then observed, together with O-4a and O-4b, through a loopback adapter written for this node that flattens the namespace (§6). O-8 was observed. One stop condition was hit: S-9 (memory pressure critical) during the O-4a run (§12).

**Redaction (HOSTING §9.1, OBS-1 brief §12).** `<host>` is the host name, `<installation-id>` an installation identifier, `~` the home path, `<scratchpad>` the session scratchpad (its path contains the user name), `$TMPDIR` the per-user temporary folder, `<OBS>` = `$TMPDIR/chirality-obs2-0.158.0`, and `<V>` the Codex binary. Remote IP addresses are shortened to their prefix. The host's time zone, which Codex puts in the model's context, is left out. Thread and turn identifiers are kept: they name invented test threads in scratch homes. The raw logs, unredacted, stay in `<OBS>/logs` and `<OBS>/homes` until HELP_HUMAN decides what is committed.

## 1. Versions and materials

| Item | Value |
|---|---|
| Codex binary `V` | `<scratchpad>/codex-0.158.0/pkg/node_modules/@openai/codex-darwin-arm64/vendor/aarch64-apple-darwin/bin/codex`, run directly. sha256 `788a818fbb9596869c7a487554507cb8bdca17584b8671112b23f9e225ba35c8` (checked with `shasum -a 256` at 19:50 UTC; equals PIN_SPIKE §3). Nothing installed |
| userAgent (initialize) | `chirality-obs2/0.158.0 (Mac OS 26.6.2; arm64) unknown (chirality-obs2; 0.0.0-obs2)` |
| LM Studio | app 0.4.16+2; CLI commit efce996; server on 127.0.0.1:1234, **started by this node** at 20:04 (it was OFF) and stopped by it at 20:24 |
| Model | `qwen/qwen3.5-9b` (installed; no download). Loaded at context **24576**, parallel **4** (20:04), then unloaded and reloaded at 24576 with parallel **1** (20:19, after S-9; §12) |
| Generated types | `<scratchpad>/codex-0.158.0/gen/ts-experimental/run1` (read only) |
| Harness | `prototype/obs2/obs2_harness.py` (Python 3.13.7, standard library) and `prototype/obs2/obs2_provider_tap.py`; OBS-1's `prototype/obs1/download_watch.sh` was run unchanged; the CLI test tool is a scratch copy of `prototype/obs1_cli_tool.py` (same sha256 `c27dc227c2f3…`) at `<OBS>/tool/obs2_cli_tool.py` |
| Host | macOS Darwin 25.6.0 arm64, 16 GB. The person's own Codex desktop app was running throughout; its processes were not touched and are not attributed here |

## 2. Configuration, homes and the provider path

- **Scratch homes only.** Every Codex process ran with `CODEX_HOME=<OBS>/homes/<name>` (25 homes) and cwd `<OBS>/cwd/<name>` (empty, not a git repository). No home held an `auth.json` or any credential; the harness refuses to start in a home holding one. `~/.codex` was never used, and the snapshots (1,137 in 17 sessions, every 100–250 ms) never saw the Codex process group open a path under `~/.codex` (S-6 not hit).
- **Warm plugin cache.** To avoid the ≈24 MB plugin-repository fetch a fresh home causes (S-F-10), each home except the cold one in O-7 v8 was seeded with a copy of `.tmp/plugins/` and `.tmp/plugins.sha` only (from OBS-1b's scratch home; no sessions, databases or credentials).
- **Base configuration** (keys as OBS-1b, provider renamed):

```toml
model = "qwen/qwen3.5-9b"
model_provider = "obs2_lmstudio"
sandbox_mode = "read-only"
web_search = "disabled"
model_context_window = 24576

[analytics]
enabled = false

[model_providers.obs2_lmstudio]
name = "LM Studio (OBS-2)"
base_url = "http://127.0.0.1:<port>/v1"
wire_api = "responses"
```

- **Provider path.** `<port>` was 1234 (LM Studio directly) for O-1, O-2, O-3; **12340**, a pass-through recorder (`obs2_provider_tap.py`, loopback only, forwards every request and response unchanged and records the request body, because LM Studio's own log truncates it) for the stock O-4 run, O-5 and O-8; **12341**, the same tap in `--capture-only` mode (records the request, answers HTTP 400, no model call) for the tool-list captures of §6.1; **12342**, the tap in `--flatten-namespaces` mode (an **adapter**, §6.2) for O-4a and O-4b. Codex was never modified.
- **Approval answers** (`observation-harness`): O-2 and O-3 held approval requests unanswered by design; elsewhere the harness gave the refusal form the request offered (`decline` if offered, else `cancel`); elicitations declined; account requests would have been refused with S-3 (none arrived).

## 3. Commands and timeline (UTC)

| Time | Command / scenario | Outcome |
|---|---|---|
| 19:50 | `shasum -a 256 V`; `lms version`, `lms status` (server OFF), `lms ls` | hash equal; model listed |
| 19:56 | `download_watch.sh` started (1 s period; `lms get` processes, models-folder listing against a baseline, LM Studio sockets) | ran to 20:24; 1,484 lines, **0 S-2 lines** |
| 19:56 | `obs2_harness.py probe` (no thread, no model) | features list, config layers, account read (§9, §10) |
| 19:57–20:01 | `o7`, variants v0…v8 (no thread, no model; 20 s idle each) | §10 |
| 20:01–20:04 | `o6`, cases M0…M5 (no thread, no model) | §9 |
| 20:04 | `lms server start`; `lms load qwen/qwen3.5-9b --context-length 24576 -y` | loaded 10.8 s, 5.57 GiB; one memory-pressure sample of 4 right after the load, then 2 (§12 D-1) |
| 20:04 | `lms log stream --source server --json`, `--source model --json` | running to 20:24 |
| 20:05 | `o1` | §4 |
| 20:07 | `o4` (stock, via tap 12340) | not provoked (§6.1) |
| 20:09 | `tools` (capture-only tap, five configurations, no model) | §6.1 |
| 20:10 | `o3` | §5.1 |
| 20:11, 20:12 | `o2` with stop by stdin close, then with SIGKILL (`--suffix=-kill`) | §5.2 |
| 20:13 | `o5` (via tap 12340) | §7 |
| 20:16 | `o4 --variants o4a` (adapter 12342) | observed; **S-9** at 20:17:52 (§12) |
| 20:19 | `lms unload --all`; `lms load … --parallel 1 -y`; pressure 1 | — |
| 20:19 | `o4 --variants o4b` (adapter 12342) | observed |
| 20:22 | `o8` (via tap 12340) | observed |
| 20:24 | taps, log streams and download watch stopped; `lms unload --all`; `lms server stop` | no Codex process, tap, `git` child or `lms` helper of this node remained (`pgrep`) |

Twenty-one `POST /v1/responses` model requests reached LM Studio in all (LM Studio server log), each part of a turn listed above. Models folder and `lms ls` were identical before and after.

## 4. O-1 — interrupt a running turn (`turn/interrupt`)

Thread `…dff59de`, turn `…2d17`, on-request, read-only. Invented prompt: write the numbers one to three hundred in words. Prompt processing took ≈41 s (7,309 tokens). The harness sent `turn/interrupt` 4.0 s after the first reasoning delta, while the model was still in its reasoning (no agentMessage had started).

| Harness ms | Frame |
|---|---|
| 44,745 | `item/started` `reasoning` `rs_yeu7…` (then 63 `item/reasoning/textDelta`) |
| 48,764 | → `turn/interrupt {threadId, turnId}` |
| 48,780 | `account/rateLimits/updated` (limitId `codex`, all else null) |
| 48,784.5 | ← response `{}` (**21 ms**) |
| 48,784.7 | `thread/status/changed` `idle` |
| 48,785.1 | `turn/completed` {status **`interrupted`**, error null, items [], itemsView `notLoaded`, durationMs 45,051} |

- Two reasoning deltas arrived after the interrupt was sent and before its response.
- **The open `reasoning` item never received `item/completed`.** No `error` notification.
- LM Studio logged "Client disconnected. Stopping generation…" 10 ms after the interrupt; its model log records `stopReason: "userStopped"` after 75 predicted tokens. Codex closes the provider stream on interrupt.
- `thread/read {includeTurns: true}` and `thread/turns/list`: thread `idle`; the turn `interrupted`, holding only the `userMessage` (the partial reasoning is not in history).
- Not observed: an interrupt while an `agentMessage` is streaming (whether a partial message is completed or kept).

## 5. O-2 and O-3 — pending requests, interrupt, stop and resume

Both use approval policy `untrusted` requested on `thread/start` (config.toml refuses it, OBS-1b B.2) and the invented prompt "Run `python3 <OBS>/tool/obs2_cli_tool.py --key EX-2` and report the outcome". In each run the model called `exec_command`; Codex sent `thread/status/changed` [`waitingOnApproval`], `item/started` `commandExecution` (inProgress, source `agent`) and then `item/commandExecution/requestApproval` (kind `command`, `availableDecisions` = `accept`, `acceptWithExecpolicyAmendment`, `cancel`), which the harness held unanswered.

### 5.1 O-3 — a request resolved by the supplier before the App answers (provoked)

Thread `…dc6b`. The request (id 0) was held for 5 s (no resolution arrived on its own), then the harness sent `turn/interrupt`:

| Harness ms | Frame |
|---|---|
| 23,986 | `item/commandExecution/requestApproval` id 0 (held) |
| 28,996 | → `turn/interrupt` |
| 29,023 | `thread/tokenUsage/updated`; `account/rateLimits/updated` |
| 29,029 | ← response `{}` |
| 29,030 | `thread/status/changed` `idle`; `turn/completed` {status **`interrupted`**} |
| 29,030.3 | **`serverRequest/resolved` {threadId, requestId 0}**, after `turn/completed` |
| 32,040 | → late answer from the harness to id 0: `{"decision": "cancel"}` |
| — | nothing in reply in the next 4 s: no error, no notification |

- **Observed:** `turn/interrupt` resolves a pending approval request on the supplier's side. The App then gets `serverRequest/resolved` with no answer of its own (HOSTING RT-10 `resolved-by-supplier`). A late answer to the resolved id is silently ignored.
- The `commandExecution` item `call_…0004` received **no `item/completed`**, and it is **absent from history**: `thread/read` lists the turn as `interrupted` with `userMessage`, `reasoning` and `agentMessage` only. The command did not run.
- Side observation (stock O-4 run, §6.1, on-request): answering an approval with **`cancel`** ended the turn: `item/completed` `commandExecution` status **`declined`**, then `turn/completed` status **`interrupted`**. `cancel` acts as decline plus interrupt.

### 5.2 O-2 — stop the app-server with a live turn and a pending request; restart; resume

Run A (stop by **closing stdin**, the App's ordinary quit) and run B (**SIGKILL** to the process group, an unexpected exit). In both, the stop came 3 s after the held request (A: thread `…6981`; B: thread `…0dc3`).

| | Run A (stdin closed) | Run B (SIGKILL) |
|---|---|---|
| Exit | code 0 in 21 ms; no survivors at 500 ms | signal 9 in 12.5 ms; no survivors |
| What the rollout gained at stop | `function_call_output` "Wall time: 3.0 seconds\naborted by user"; a user-role message `<turn_aborted> The user interrupted the previous turn on purpose. Any running unified exec processes may still be running in the background. If any tools/commands were aborted, they may have partially executed. </turn_aborted>`; `event_msg turn_aborted {reason: "interrupted"}` | nothing: the rollout ends at the `function_call` |
| New process: `thread/read` before resume | thread `notLoaded`; the turn **`interrupted`** with `userMessage`, `reasoning`, `agentMessage` | **the same**: `interrupted` (derived; no abort record exists) |
| `thread/resume {threadId}` | response: thread `idle`, approvalPolicy `untrusted`, the same one turn `interrupted` | the same |
| Notifications after resume (15 s) | `deprecationNotice` (full-history hydration), `thread/status/changed` idle, `thread/tokenUsage/updated`, `thread/goal/cleared` | the same without `thread/tokenUsage/updated` |
| Pending request re-raised? | **No** server request of any kind | **No** |
| Model request on resume? | none (LM Studio received nothing) | none |
| `thread/loaded/list` | the thread | — |

**O-2 findings.** A pending approval does not survive a supplier stop: it is not re-raised on resume and no resolution is sent for it (the old connection is gone). The turn reads back as `interrupted` after both a graceful stop and a kill, so the status alone does not distinguish them. On a graceful stop Codex tells the model, in history, that "the user interrupted the previous turn on purpose" (relevant to K-4's "interrupted by quit": the model's next turn will read it as the person's interrupt). The command item is not in history either way.

## 6. O-4, O-4a, O-4b — delegation with the experimental opt-in

### 6.1 Stock pairing: not provoked

`initialize` with `experimentalApi: true`. Feature `multi_agent` is **stable and enabled by default**; `multi_agent_v2` stable, disabled. The pass-through tap shows the first request's tools: `exec_command`, `write_stdin`, `request_user_input`, `view_image`, a **`namespace` tool `multi_agent_v1`** ("Tools for spawning and managing sub-agents.") holding `close_agent`, `resume_agent`, `send_input`, `spawn_agent`, `wait_agent`, and `get_goal`, `create_goal`, `update_goal`. LM Studio logged "Ignoring unsupported tool type(s): namespace." and the model never saw `spawn_agent`. Asked to start a helper agent, it tried `exec_command` instead (the approval was answered `cancel`, §5.1). **O-4 is not provoked on the stock pairing.** This is the namespace OBS-1 found dropped: it is the delegation tool set.

Tool-list captures (capture-only tap, no model call; one thread and turn per configuration):

| Configuration added | Delegation tools sent |
|---|---|
| none (default) | namespace `multi_agent_v1` [close_agent, resume_agent, send_input, spawn_agent, wait_agent]; `spawn_agent` parameters `fork_context`, `items`, `message`, `model`, `reasoning_effort` |
| `[features.multi_agent_v2] enabled = true` | namespace **`collaboration`** [followup_task, interrupt_agent, list_agents, send_message, spawn_agent, wait_agent]; `spawn_agent` parameters `fork_turns`, `message`, `model`, `reasoning_effort`, `task_name` |
| the same with `tool_namespace = ""` | refused at `thread/start`: "failed to load configuration: features.multi_agent_v2.tool_namespace must not be empty" |
| `[agents.obs2_task] description = "…"` | namespace `multi_agent_v1`; `spawn_agent` gains **`agent_type`**, whose description lists the roles `obs2_task` (the invented description), `default`, `explorer`, `worker` |
| `[features] multi_agent = false` | no delegation tools |

No configuration found makes Codex 0.158.0 send the delegation tools as flat functions. The `spawn_agent` description lists OpenAI model names as overrides even with the local provider. Every request's `client_metadata` carries the installation id and thread, session and turn ids to the provider (here a loopback endpoint).

### 6.2 Through the OBS-2 namespace adapter

`obs2_provider_tap.py --flatten-namespaces` (port 12342) replaces each `namespace` tool by its inner functions before forwarding to LM Studio, strips `namespace` from input items, and, in the streamed response, adds `"namespace": "multi_agent_v1"` back to any `function_call` whose name came from that namespace. Every rewrite is recorded (`<OBS>/logs/provider_adapter.jsonl`). **This is a harness adapter, not stock LM Studio behaviour.** What follows is Codex's own behaviour when its delegation tool is called.

Home `o4-*`: `[agents.obs2_task] description = "Invented task role for OBS-2: answers one short question."`, `config_file = "<home>/agents/obs2_task.toml"`, which holds `developer_instructions = "Invented role line: you are the OBS2 TASK ROLE. Begin every reply with the word TASKROLE."`

**O-4 / O-4a** (thread `…c12b`; developer text: observation test, "the user explicitly authorizes sub-agents"; prompt: call `spawn_agent` once with `agent_type "obs2_task"` and an invented message, then `wait_agent`, then report):

| Item / notification (parent thread unless marked) | Observed |
|---|---|
| `item/started` `collabAgentToolCall` | tool **`spawnAgent`**, status `inProgress`, senderThreadId parent, receiverThreadIds [], prompt = the message, model "", reasoningEffort `medium`, agentsStates {} |
| `item/completed` same id | status `completed`, receiverThreadIds [child `…e4b508d`], model `qwen/qwen3.5-9b`, agentsStates {child: {status `pendingInit`, message null}} |
| child notifications | delivered on the **same connection with the child's threadId**: `thread/status/changed`, `turn/started`, `item/started`/`item/completed` (userMessage, reasoning, agentMessage), deltas, `thread/tokenUsage/updated`, `turn/completed`. **No `thread/started` for the child** |
| `collabAgentToolCall` tool **`wait`** | started inProgress → completed with agentsStates {child: {status `completed`, message = the child's final text}} |
| parent final agentMessage | reports the child's reply |
| `thread/read {child, includeTurns}` | **readable**: status idle, **`parentThreadId` = parent**, **`agentRole` `obs2_task`**, `agentNickname` "Kepler", `ephemeral` false, `source` {subAgent {thread_spawn {parent_thread_id, depth 1, agent_path null, agent_nickname, agent_role `obs2_task`}}}, one turn `completed` with userMessage, reasoning, agentMessage |
| `thread/list {}` | the parent only (children not listed by default) |
| `thread/loaded/list` | parent and child |

**What instructions the child received (O-4a)**, from the child's own request at the tap: its developer messages were the **role's `developer_instructions`** ("Invented role line: … OBS2 TASK ROLE …"), the skills block and the permissions block. The **parent's developer instructions were not included.** The child's tools had **no delegation namespace** (depth 1 is the limit at defaults). The child's reply ("`EX-4` is an invented identifier …") did **not** begin with TASKROLE: the role text was supplied, and this 9B model did not follow it. The child reports nothing about its instructions in any App Server element beyond `agentRole`. **O-4a: native child-role configuration (`agents.<role>.description` and `config_file`) is honoured at 0.158.0: the role is offered as `agent_type`, recorded as `agentRole`, and its `developer_instructions` replace the parent's for the child.**

**O-4b** (thread `…b015`, same home, parallel 1; developer text "You are a TASK agent; you do not delegate. …"; prompt: "Please delegate this to a helper agent: spawn a sub-agent and ask it to reply with the word READY, then tell me what it said."): the model **delegated**. `collabAgentToolCall` `spawnAgent` (child `…2eaab0`, agentRole `obs2_task`, nickname "Meitner"), then `sendInput` to the child, then `wait` (child completed, "READY"); the parent replied "READY". **The guidance "you do not delegate" did not prevent delegation; the delegation was recorded and shown in full** (K-10 "stated, not enforced").

## 7. O-5 — resume with changed `developerInstructions` (P-15)

Home `o5`, via the pass-through tap. Thread `…b1ab` started with developer text A ("Marker ALPHA-7: end every reply with the word ALPHA."). Turn 1 → reply ending "ALPHA".

| Step | Request | What the thread reports | What reached the model (tap) | Reply |
|---|---|---|---|---|
| (a) loaded thread, same process | `thread/resume {threadId, developerInstructions: B (BRAVO-7)}` | response without error: thread idle, 1 turn, `instructionSources` [], and **no element naming the developer instructions in effect** | turn 2: developer message **ALPHA-7 only**; B absent | "… ALPHA" |
| (b) new process, thread not loaded | `thread/resume {threadId, developerInstructions: C (CHARLIE-7)}` | the same shape, 2 turns | turn 3: **ALPHA-7 only**; C absent | "… ALPHA" |

The rollout holds no trace of B or C. **O-5: at 0.158.0, `developerInstructions` on `thread/resume` is accepted without error and silently ignored, both for a loaded thread and for one loaded by the resume** (the v3 finding at 0.154 recurs; P-15's open half is now observed).

**O-5b (supplementary, from O-8's run).** `turn/start` with `collaborationMode {mode "default", settings {model, reasoning_effort null, developer_instructions: D (DELTA-7)}}` (experimental): the request gained a developer message `<collaboration_mode>…DELTA-7…</collaboration_mode>`, the thread's original developer text was still sent, `thread/settings/updated` reported the new collaborationMode with D, and the reply ended "DELTA". A per-turn developer text can be supplied this way; it is added, it does not replace the thread's own.

## 8. O-8 — plan mode (`collaborationMode` on `turn/start`)

Home `o8`, experimentalApi true, via the pass-through tap. Thread `…9173`, developer text with an invented role line ("OBS2 PLANNER ROLE. End every reply with the word ROLEMARK."). `collaborationMode/list` returns `Plan` (mode `plan`, reasoning_effort `medium`) and `Default`.

| Turn | Sent | Observed |
|---|---|---|
| 1 | `collaborationMode {mode "plan", settings {model, reasoning_effort null, developer_instructions null}}`; invented request for a three-step plan | `thread/settings/updated` with collaborationMode `plan` and Codex's built-in Plan Mode text as `developer_instructions`; **a `plan` item** (id `<turnId>-plan`) streamed by 188 `item/plan/delta` and completed; **no agentMessage**; **no `turn/plan/updated`** and no `update_plan` tool in the tool list; turn `completed` |
| 2 | no `collaborationMode` | **still plan mode**: the request still carried the `<collaboration_mode># Plan Mode…` developer message; no `thread/settings/updated`; the model replied "I am in Plan Mode." |
| 3 | `collaborationMode` default with D | §7 O-5b |

The thread's developer text (role line) was **sent alongside** the plan-mode text in every request. The replies did not end with ROLEMARK, so the role line was supplied but not visibly applied; with this model the precedence statement in the types ("Takes precedence over … developer instructions") cannot be separated from the model's adherence. **Feature flags:** plan mode is not gated by a listed flag in use (`collaboration_modes` is listed `removed`, enabled true); delegation is gated by `multi_agent` (stable, default on) and `multi_agent_v2` (stable, default off). `config/read` shows neither (no `features` key in the effective config unless set).

## 9. O-6 — the K-1 mechanism (config/read and account/read only)

Home A (`o6-A-shared`) stands in for the person's own home: an invented provider `obs2_shared_example`, an MCP server entry (`/usr/bin/true`, disabled), approval and sandbox keys, analytics off, and a profile file `obs2example.config.toml`. Homes B are the App's, with no configuration and no authentication. No credential existed anywhere, so every `account/read` returned `account: null`.

| Case | How | `config/read` (effective, layers) | `account/read` | Result |
|---|---|---|---|---|
| M0 | B alone | empty user layer at B; system layer `/etc/codex/config.toml` (empty) | null, `requiresOpenaiAuth` **true** (default OpenAI provider) | control |
| M1 | B's `config.toml` is a **symbolic link** to A's | A's values; user layer **named by B's path** (`…/o6-B-M1/config.toml`), content A's | null, `requiresOpenaiAuth` false | **works** |
| M2 | B launched with **`-c` overrides** carrying A's values (inline TOML tables for the provider and MCP entry) | A's values in a **`sessionFlags`** layer above B's empty user layer | null, false | **works** (a copy, not a share: the App must read and re-send A's file) |
| M3 | `codex --profile obs2example app-server` | — | — | **refused at launch**: "Error: --profile only applies to runtime commands and `codex mcp`…"; profile files live in `$CODEX_HOME` anyway |
| M4 | `CODEX_HOME` = A with `-c cli_auth_credentials_store="ephemeral"` | A's values plus a sessionFlags layer `cli_auth_credentials_store = "ephemeral"` | null, false | runs; with no credential anywhere, **separation of authentication is not distinguishable** |
| M5 | as M4 with `"keyring"` | as M4 with `keyring` | null, false | the same; whether the keyring was consulted is not observed |

- The effective default is `cli_auth_credentials_store = "file"` (M0–M2), so a separate `CODEX_HOME` gives separate authentication storage by construction (inference from the default and the file name `auth.json` in the binary's strings; not observed with a credential).
- A's `config.toml` was byte-identical before and after all cases (sha256 `7536731d4827…`): no case wrote through the symlink. Writes (`config/value/write`, `config/batchWrite`) were not exercised; through a symlink they would land in A's file (inference, not observed).
- Every process also read macOS managed preferences for `com.openai.codex` and looked for `/etc/codex/managed_config.toml` (Codex's own log); neither existed.
- **O-6 reading:** at 0.158.0, sharing one home's configuration with a second home that keeps its own authentication works by a symbolic link to `config.toml` (a live share) or by `-c` launch overrides (a copy). There is no `--profile` or configuration-file-location option for `app-server`. M4/M5 (shared home, separate credential store) cannot be judged without a credential.

## 10. O-7 — start-up traffic and the settings that stop it (K-12)

Each variant: a fresh warm home with the base configuration plus the variant, `app-server` with `initialize` (experimentalApi false) and `initialized`, then 20 s idle. Sockets of the Codex process group by `lsof -nP -a -i -g <pgid>` every 100 ms; attempts by the supplier's own log database in the scratch home (`logs_2.sqlite`). Nothing was intercepted; addresses were not resolved (no name lookups).

| Variant | Codex → 2606:4700:4408::…:443 (chatgpt.com, inferred: the log's only HTTPS target at that moment is the featured-plugins request) | `git-remote-https` → 2604:5580:21::…:443 (github.com/openai/plugins.git, from its command line) | Codex log |
|---|---|---|---|
| v0 baseline | yes | yes (`ls-remote` only; warm cache) | remote-control loop started for `https://chatgpt.com/backend-api/`, then "waiting to resolve remote control preference until authentication is available" and "Reloading auth" **once a second** (20 times in 20 s); featured plugins `GET https://chatgpt.com/backend-api/plugins/featured?platform=codex` → **401 Unauthorized** |
| v1 `[features] plugins = false` | **no** | **no** | remote-control loop as v0; no featured request |
| v2 `remote_plugin = false` | yes | yes | as v0 |
| v3 `apps = false` | yes | yes | as v0 |
| v4 env `CODEX_INTERNAL_APP_SERVER_REMOTE_CONTROL_DISABLED=1` | yes | yes | remote-control loop starts with `initial_desired_state=Disabled` and **no once-a-second auth loop**; featured 401 as v0 |
| v5 `remote_control = false` (feature listed `removed`) | yes | yes | as v0 (no effect) |
| v6 plugins, remote_plugin, apps, tool_suggest all false | **no** | **no** | as v1 |
| v7 v6 plus the env variable | **no** | **no** | loop starts Disabled; no auth loop; 17 log rows in all |
| v8 **cold home** (no plugin cache) with `plugins = false` | **no** | **no**; **no `.tmp/` created**, so no repository fetch | as v1 |

- In every variant `remoteControl/status/changed` reported `disabled` at start (with `serverName` `<host>` and an `<installation-id>`). Without sign-in the remote-control loop opened **no socket** in any variant (lsof): it is local work only. Whether it connects when signed in is not observed (K-11).
- **Which is which (O-7):** `[features] plugins = false` stops both start-up connections seen (the featured-plugins request to chatgpt.com and the plugin-repository check or fetch from github.com), including the ≈24 MB fetch of a fresh home. No configuration key stops the remote-control loop; only the internal environment variable does, and that loop made no connection without sign-in. `remote_plugin`, `apps` and `remote_control` features have no effect on these connections. During turns (O-1…O-8) the Codex process group had **no non-loopback socket** (S-5 not hit).
- `remoteControl/status/read` requires `experimentalApi` ("remoteControl/status/read requires experimentalApi capability").

## 11. Other observations

- **Process exit (H11).** In the five tool-list sessions (each stopped about 0.7 s after spawn) the plugin `git ls-remote` child was still running when Codex exited; it was re-parented to pid 1 in Codex's process group and the harness ended it at 500 ms. In every longer session there were no survivors. An App that stops Codex soon after start may leave this child unless it ends the process group.
- **Content sent to the model.** In all 21 model inputs: no `/Users/` path, user name, host name or scratchpad path. The host's time zone was present in every input (as in OBS-1). Each request's `client_metadata` carried the installation id (to a loopback provider here).
- Every `thread/read {includeTurns: true}` and `thread/resume` without `excludeTurns` produced a `deprecationNotice` (full-history hydration is deprecated in favour of `thread/turns/list` and `thread/items/list`).

## 12. Stops and deviations

| Item | Record |
|---|---|
| **S-9 (hit)** | 20:17:52 UTC, during O-4a, while parent and child predictions ran together (parallel 4): one sample of `kern.memorystatus_vm_pressure_level` = 4. The harness stopped the scenario. The parent turn had already reached its last step and completed inside the harness's 20 s grace period; the process was then stopped (stdin, exit 0). Pressure was 1 at 20:18:56. **Continuation:** the model was reloaded with parallel 1 (no concurrent predictions) and the remaining single-thread items (O-4b, O-8) ran with continuous sampling; level 4 did not recur. HELP_HUMAN may judge whether continuing after S-9 was within the brief |
| D-1 | Right after the first model load (20:04, before any Codex process) one sample read 4, then 2 for six samples. Swap use was 7.0 of 8.2 GB. The run went ahead with S-9 sampled every 250 ms during each scenario (not between scenarios) |
| D-2 | O-4 was observed through a harness adapter (§6.2) after the stock pairing could not provoke it. Labelled throughout |
| D-3 | O-6 M3 was refused at launch by Codex (recorded as that case's result; the harness's S-11 for it is not a failure of the run) |
| D-4 | The first O-4 run (stock, 20:07) used an earlier revision of the harness's `sc_o4` function, since replaced by the O-4a/O-4b version; its result file is `<OBS>/logs/o4/o4_result.json` |
| D-5 | The two O-2 runs share the log folders `o2-first/` and `o2-second/` (frames appended); their results are `o2_result_stdin.json` and `o2_result_kill.json` |
| S-1…S-8, S-10, S-11 | S-1: every `codexHome` equalled its scratch home. S-2: no `lms get`, models folder and `lms ls` unchanged, 0 S-2 lines. S-3: no `account/*` server request and no auth error to the client. S-4: every `instructionSources` was []. S-5: no non-loopback socket during any turn. S-6: none. S-7: every turn completed or was interrupted on purpose |

## 13. Network destinations seen (all sessions)

| From | To | When | Stopped by |
|---|---|---|---|
| Codex (`<V>`) | 2606:4700:4408::…:443 (Cloudflare; chatgpt.com by inference), featured-plugins request, 401 | start-up only, before any thread | `[features] plugins = false` |
| `git-remote-https` (child of Codex) | 2604:5580:21::…:443 (github.com/openai/plugins.git by its command line), `ls-remote` | start-up only | `[features] plugins = false` |
| Codex | 127.0.0.1:1234, :12340, :12341, :12342 (LM Studio and the taps) | turns only | — |
| LM Studio's own processes (not Codex) | its `lmlink-connector` held TLS connections to several hosts throughout, as before this node started; not attributed to Codex | throughout | — |

## 14. Item rows

| Item | Status | Finding |
|---|---|---|
| O-1 | observed | `turn/interrupt` answers `{}` in ≈20 ms; `turn/completed` `interrupted` follows; the open reasoning item gets no `item/completed` and is not kept; Codex closes the provider stream |
| O-2 | observed | A pending approval is not re-raised after a stop and resume; the turn reads back `interrupted` after a graceful stop and after a kill alike; a graceful stop writes a "user interrupted on purpose" marker into history |
| O-3 | observed (provoked) | `turn/interrupt` with a pending approval → `turn/completed` then `serverRequest/resolved`, no answer given; a late answer is ignored; the command item never completes and is not in history |
| O-4 | not provoked on the stock pairing; observed via the OBS-2 adapter | Delegation tools travel only in a `namespace` tool that LM Studio 0.4.16 drops. Via the adapter: `collabAgentToolCall` items (spawnAgent, sendInput, wait) on the parent; child notifications on the same connection with the child's threadId, no `thread/started`; child readable by `thread/read` |
| O-4a | observed via the adapter | `agents.<role>` with `config_file` is honoured: `agent_type` offered, `agentRole` recorded, the role's `developer_instructions` replace the parent's for the child |
| O-4b | observed via the adapter | "You do not delegate" in developer text did not stop a spawn; the delegation was recorded and shown |
| O-5 | observed | `developerInstructions` on `thread/resume` is accepted and ignored, loaded or not; nothing reports it. Supplementary O-5b: `collaborationMode.settings.developer_instructions` on `turn/start` is applied, added to the thread's own text |
| O-6 | observed (credential-free) | Symlinked `config.toml` or `-c` overrides share A's configuration with B's own empty authentication; `--profile` is refused for `app-server`; shared home with a separate credential store not distinguishable without a credential |
| O-7 | observed | `[features] plugins = false` stops both start-up connections (chatgpt.com featured plugins, github.com plugin repository); no setting stops the remote-control loop, which made no connection without sign-in |
| O-8 | observed | Plan mode yields a `plan` item via `item/plan/delta`, no `turn/plan/updated`, and persists on later turns without `collaborationMode`; developer text still sent beside it |

## 15. Files

| File | sha256 |
|---|---|
| `Design/OBS_2_0.158.0.md` (this record) | in the return file `D/OBS-2.md` |
| `Design/prototype/obs2/obs2_harness.py` | in the return file |
| `Design/prototype/obs2/obs2_provider_tap.py` | in the return file |
| raw, not committed (`<OBS>/logs`): `run_events.jsonl` f005b641bdc5…; `probe/probe_result.json` add40d83dd9f…; `o7_summary_v0-v7.json` 966e30014902…; `o7_summary.json` (v8) 0aec340723b9…; `o6_result.json` a9b4f7c756f3…; `o6_result_M4…+M5….json` e81a4cb39560…; `o1/frames.jsonl` 59e3a2eb8078…; `o3/frames.jsonl` 129a029579f7…; `o2-first/frames.jsonl` ad26ee2f01fd…; `o2-second/frames.jsonl` 256b7b8993f4…; `o2_result_stdin.json` c05b5c190927…; `o2_result_kill.json` 77311ed4698b…; `o5_result.json` d8e72d1b7037…; `o4/o4_result.json` 8e37b4bbc47d…; `tools_result.json` 545529849eac…; `o4-o4a/o4_result.json` 8d8bb85295fe…; `o4-o4b/o4_result.json` d3cd1bcbc137…; `o8/o8_result.json` 8c40fc27ba9e…; `provider_tap.jsonl` 85f198b494e0…; `provider_tap_capture.jsonl` 2cfbd583b401…; `provider_adapter.jsonl` a641a3d82d29…; `lmstudio.server.log` 6feb724f16d0…; `lmstudio.model.log` 348f611d952d…; `download_watch.log` f49ae5d62cb8… | as listed |

## UNRESOLVED

- Whether any local server accepts Responses `namespace` tools, or a later Codex offers flat delegation tools; until then delegation is unavailable to LM Studio-served models without an adapter (bears on K-5: the delegation view is absent for local models).
- An interrupt while an `agentMessage` streams (partial message kept or not).
- Whether the remote-control loop connects once signed in, and whether the featured-plugins request carries identifiers (K-11 excludes sign-in).
- O-6 M4/M5: whether a shared home with an ephemeral or keyring credential store keeps authentication separate (needs a credential).
- Whether `config/value/write` through a symlinked `config.toml` writes the shared file (writes were outside R17-16's means).
- Whether the precedence of `collaborationMode` over developer instructions is real or this model's adherence (the role lines were supplied and not followed in plan mode).
