# OBS-1 — one live Codex turn at pin 0.158.0 against a local LM Studio model (observation record)

- **Date:** 2026-09-30 (turn 18:45:03–18:46:11 UTC). **Node:** OBS-1 (Type 2 TASK) of run `APP-V4-DESIGN-PASS-2-20260930`, launched by HELP_HUMAN.
- **Standing:** a dated observation at one version (Codex 0.158.0, LM Studio 0.4.16+2, one model). **Not qualification** of the pin, the provider or the model; not an X-02 fixture; no App candidate was involved. Every answer the harness could have given to a supplier request has origin `observation-harness`, never a person's act (none was needed: the supplier sent no server request).
- **Authority:** owner DECISION-K1 K1-6 and the model-download record with its recorder's correction (`OWNER_DECISIONS.md`, read at sha256 f5a8ff89d500…); the brief `WAVE_B/OBS-1_BRIEF.md` (sha256 b3e7a4b6d98f…) with the integrator's decisions in `BRIEFS.md` "OBS-1 — the live Codex turn" (sha256 b006996cd794…): P-5, part C and part D allowed; part B not run under that brief; S-8 → stop and return; route R-1 only. Context read: HOSTING_BOUNDARY §8.4, §9.1, F-28 (sha256 8b88a0ef5e2f…) and PIN_SPIKE §3 (sha256 0e090a4ca14e…), neither edited.
- **Result in one line:** the turn ran and completed through route R-1 (`wire_api = "responses"` to LM Studio's `/v1/responses`), but **no `mcpToolCall` item was produced (S-8)**. The model did try to call `example_lookup` twice; LM Studio discarded both calls because the tool was not in the list it passed to the model, having logged "Ignoring unsupported tool type(s): namespace." Part B was not run (see §6).

**Redaction (HOSTING §9.1).** Here, `<host>` stands for the host name (in the `serverName` element and in Codex's own log), `<installation-id>` for the installation identifier, `~` for the home path, `<scratchpad>` for the session scratchpad (whose path contains the user name), `$TMPDIR` for the per-user temporary folder, `<OBS>` for `$TMPDIR/chirality-obs1-0.158.0`, and `<host-addr>` for the host's own IP addresses. The host's time zone, which Codex put in the model's context, is also left out. The raw logs, unredacted, stay in `<OBS>/logs` until HELP_HUMAN decides what is committed (brief §12).

## 1. Versions and materials

| Item | Value |
|---|---|
| Codex binary (`V`) | `<scratchpad>/codex-0.158.0/pkg/node_modules/@openai/codex-darwin-arm64/vendor/aarch64-apple-darwin/bin/codex`, run directly (launcher `vendor`). sha256 `788a818fbb9596869c7a487554507cb8bdca17584b8671112b23f9e225ba35c8`, the same as SPIKE §3 (P-1 pass). Nothing was installed |
| userAgent (initialize) | `chirality-obs1/0.158.0 (Mac OS 26.6.2; arm64) unknown (chirality-obs1; 0.0.0-obs1)` |
| LM Studio | app 0.4.16+2 (`CFBundleShortVersionString`); CLI commit efce996; server on 127.0.0.1:1234 |
| Model | key `qwen/qwen3.5-9b` (variant `qwen/qwen3.5-9b@4bit`, MLX safetensors, 5,977,257,833 B; `trainedForToolUse` true, installed in June 2026 at `lmstudio-community/Qwen3.5-9B-MLX-4bit`). **No download** |
| Loaded context length | **24576** (first load at 32768, then reloaded once smaller: see D-1 in §5); parallel 4; 5.57 GiB |
| MCP test tool | `prototype/obs1_mcp_double.py` sha256 999ae54cd2d8…; `python3 run_cases.py` → `OBS1-test-doubles pass (model)` (TOTAL 35, FAIL 0) before the run |
| Harness | `prototype/obs1/obs1_harness.py` (Python 3.13.7, standard library); `prototype/obs1/download_watch.sh`; part C `prototype/obs1/partc_chat.py` |
| Host | macOS Darwin 25.6.0 arm64, 16 GB |

## 2. Configuration used (route R-1)

`CODEX_HOME=<OBS>/codex-home`, a `cp -Rp` copy of the spike's warm home (the spike folder was only read). The thread's cwd was `<OBS>/cwd` (empty; not a git repository). The one environment key added was `CODEX_HOME`; the harness's own environment was otherwise inherited. `<OBS>/codex-home/config.toml`:

```toml
model = "qwen/qwen3.5-9b"
model_provider = "obs1_lmstudio"
approval_policy = "on-request"
sandbox_mode = "read-only"
web_search = "disabled"
model_context_window = 24576

[analytics]
enabled = false

[model_providers.obs1_lmstudio]
name = "LM Studio (OBS-1)"
base_url = "http://127.0.0.1:1234/v1"
wire_api = "responses"

[mcp_servers.obs1]
command = "/usr/bin/python3"
args = ["<repo>/…/Design/prototype/obs1_mcp_double.py", "--log", "<OBS>/logs/mcp.jsonl"]
```

The spike's warm home did **not** have the plugin sync the brief expected (`.tmp/plugins/`, `plugins.sha`). It held a partial clone (`.tmp/plugins-clone-…`) and a `plugins.sync.lock`, so the supplier re-synced at start (§8).

## 3. Commands (in order; UTC)

| Time | Command | Outcome |
|---|---|---|
| 18:36:41 | `shasum -a 256 V`; `lms version`; `lms status`; `lms ls`; `lms ls --json`; model-folder listing (P-1, P-2, P-7) | hash equal; server OFF; key listed |
| 18:36:5x | `download_watch.sh` started (every 1 s: `lms get` processes, model-folder listing against a baseline, numeric IP sockets of LM Studio's processes; no name lookups) | ran until 19:02:17; 0 S-2 lines |
| 18:37:35 | `lms server start` (**started by this node**) | ON, 127.0.0.1:1234 |
| 18:37:42 | `lms load qwen/qwen3.5-9b --context-length 32768 -y` (P-3; estimate beforehand 7.79 GiB) | loaded; pressure level 2 (warn) |
| ~18:39 | `lms unload --all`; `lms load … --context-length 24576 -y` (the brief's one smaller retry) | loaded; pressure level still 2 |
| 18:39:5x | `GET /v1/models` (P-4); one `POST /v1/responses` (P-5) | key listed; HTTP 200 (§4) |
| 18:40:20 | `lms log stream --source server --json`, `lms log stream --source model --json` (P-6) | running |
| 18:45:00 | `python3 -B prototype/obs1/obs1_harness.py --obs <OBS> --binary V --model qwen/qwen3.5-9b --mcp-double …/obs1_mcp_double.py --part-d` | exit 0; stop none detected by the harness; S-8 found in analysis |
| 19:01:36 | `python3 -B prototype/obs1/partc_chat.py --model qwen/qwen3.5-9b --out <OBS>/logs/partc` (part C) | exit 0; 3 × HTTP 200 |
| 19:02:17 | `lms unload --all`; `lms server stop` (the server had been started by this node); log streams and download watch stopped | done |

## 4. Pre-flight

| # | Result |
|---|---|
| P-1 | pass (sha256 above) |
| P-2 | server was OFF and was started by this node; the model key was listed |
| P-3 | loaded at 32768, and the kernel memory-pressure level became 2 (warn; about 38–42 % free; swap 5.36 of 6.14 GB used). It was 1 (normal) with no model loaded. Reloaded once at 24576: still 2. **Deviation:** the brief's P-3 pass condition is "normal". The brief's S-9 is "cannot load, or memory pressure turns critical". Level 2 is not critical, so the run went ahead at 24576 and the harness sampled the pressure level every 250 ms, set to stop on level 4. During the run the level varied between 1 and 2 and never reached 4 |
| P-4 | pass: `/v1/models` lists `qwen/qwen3.5-9b` (and four other installed models) |
| P-5 | pass: `/v1/responses` is served. Invented input "Reply with the word OK." plus one invented function tool `example_ping` gave HTTP 200 and status `completed`, with output items `reasoning` (with `reasoning_text` content) and `message` ("\n\nOK"). **No function call came back** (the model chose not to call one). The echoed request shows `parallel_tool_calls: true`, `store: true` and the tool with `strict: false` |
| P-6 | log streams running (server and model sources, JSON) |
| P-7 | `lms ls` and the models folder (depth 2) were snapshotted before and after: **unchanged** |

## 5. The exchange (frames; `<OBS>/logs/frames.jsonl`: 8 sent, 183 received)

Sequence (harness monotonic ms; `emittedAtMs` from the supplier):

| # | Frame | Notes |
|---|---|---|
| s1 @19.8 | `initialize` {clientInfo chirality-obs1, experimentalApi false, requestAttestation false} | |
| r1 @242.5 | response {userAgent, codexHome `/private` + `$TMPDIR` + `…/codex-home` (the same folder, resolved: **S-1 not hit**), platformFamily unix, platformOs macos} | |
| s2 @242.7 | `initialized` | |
| r2 @242.8 | `remoteControl/status/changed` {status `disabled`, serverName `<host>`, installationId `<installation-id>`, environmentId null}, emittedAtMs 1 ms **before** `initialized` was written | same as the spike (H4) |
| s3/r3 | `mcpServerStatus/list` {} → `obs1`: runtimeStatus **null**, tools {example_lookup}, httpOrigin null, authStatus `unsupported`, serverInfo `obs1-example-host`, serverCapabilities tools | the list call started its own MCP double instance (the MCP log shows a separate initialize at the list's time) |
| s4/r4 @3593 | `thread/start` → model `qwen/qwen3.5-9b`, modelProvider `obs1_lmstudio` (**as requested; S-3 not hit**), approvalPolicy `on-request`, approvalsReviewer `user`, sandbox {type readOnly, networkAccess false}, **instructionSources [] (S-4 not hit)**, multiAgentMode `explicitRequestOnly`, thread.source `vscode`, originator `chirality-obs1`, rollout path under `<OBS>/codex-home/sessions/…` | 75 ms |
| r5, r6 | `thread/started`; `mcpServer/startupStatus/updated` obs1 `starting` | |
| s5 | `turn/start` {threadId, input [text: the §7 prompt]} | |
| r7 | `warning` "Model metadata for `qwen/qwen3.5-9b` not found. Defaulting to fallback metadata; this can degrade performance and cause issues." | before the turn/start response |
| r8 | turn/start response {turn: status inProgress, items []} | |
| r9 | `mcpServer/startupStatus/updated` obs1 `ready` (18 ms after `starting`) | |
| r10, r11 | `thread/status/changed`; `turn/started` | |
| r12, r13 | `item/started`/`item/completed` `userMessage` | |
| r14…r171 | three rounds of: `reasoning` item (started, 114 `item/reasoning/textDelta` in all, completed) and then an `agentMessage` item (32 `item/agentMessage/delta` in all). The first two agentMessages have text "\n\n"; the third says "The `example_lookup` tool is not available in this environment, so I cannot retrieve the proposal from EX-1 or check EX-ERR." | first reasoning item began 53 s after turn/start (prompt processing of 7,762 tokens) |
| r172 | `thread/tokenUsage/updated` total 23,725 (input 23,579, cached 15,771, output 146, reasoning 114), modelContextWindow 23,347 | |
| r173 | `account/rateLimits/updated` {limitId `codex`, all other elements null} | the supplier's own notification; no sign-in request |
| r174, r175 | `thread/status/changed`; **`turn/completed`** {status `completed`, error null, durationMs 67,711, items [the last agentMessage]} | |
| s6…s8 | part D (§7) | |

No server request of any kind was received (no approval, elicitation, requestUserInput, account or attestation request). No `serverRequest/resolved`, no `model/rerouted`, no `item/mcpToolCall/*` and no `error` notification appeared. The supplier's stderr was **0 bytes**.

**What reached the model and what happened (LM Studio logs).** LM Studio received **one** `POST /v1/responses` for the turn (18:45:03). It logged: "Ignoring unsupported tool type(s): namespace."; "unsupported field(s) prompt_cache_key … ignored"; "Developer role detected - replacing it with system role."; "include value(s) reasoning.encrypted_content are not supported and will be ignored." The tool list LM Studio placed in the model's prompt was `exec_command`, `write_stdin`, `list_mcp_resources`, `list_mcp_resource_templates`, `read_mcp_resource`, `request_user_input`, `view_image`, `get_goal`, `create_goal`, `update_goal`. **`example_lookup` was not among them.** Within that one request LM Studio ran three predictions:

1. The model emitted `<tool_call><function=example_lookup><parameter=key>EX-1</parameter></function></tool_call>`. LM Studio logged "Failed generating function tool request 'example_lookup' … due to an invalid tool name. Skipping function_call output item." It fed `"Cannot find tool with name example_lookup."` back to the model as a tool response itself.
2. The model tried the same call again, and LM Studio skipped it the same way.
3. The model answered that the tool was not available.

None of these calls reached Codex: the rollout has no `function_call` item, and the MCP double logged no `tools/call`.

**Reading (inference, not observed directly):** Codex 0.158.0 appears to offer MCP tools to a Responses provider as a `namespace` tool entry, which LM Studio 0.4.16 drops. The request body in LM Studio's log is truncated, and Codex's own log does not record it. The tool-list strings in the binary (`DynamicToolNamespaceSpec`) and the generated types' `namespaceTools` capability (HCG-A06) are consistent with this. Whether a provider capability or configuration setting would make Codex send flat function tools was not explored, because it would need another turn.

**Content sent to the model (brief §7).** The prompt LM Studio formatted contained Codex's base instructions, the invented developer instructions and prompt, the bundled skill descriptions with their root `<OBS>/codex-home/skills/.system`, and the environment context: cwd `$TMPDIR/chirality-obs1-0.158.0/cwd`, shell zsh, date 2026-09-30, **time zone** and a read-only permission profile. It contained no `/Users/` path, user name, host name or scratchpad path. **Finding:** Codex puts the host's IANA time zone in the model's context. It stayed on this machine, but it is not invented material (K1-6).

## 6. Stops and deviations

| Item | Record |
|---|---|
| **S-8 (hit)** | The turn completed (status `completed`) with **no `mcpToolCall` item**. Under the brief's §9 and the integrator's decision, this node stopped and returns. Nothing was downloaded. Qwen3 4B was **not** downloaded, since that step is HELP_HUMAN's under the owner's answer. The cause observed is a tool-form mismatch between Codex's request and LM Studio (§5), not the model's inability to produce a call: the model produced two well-formed calls in Qwen's format, and part C shows that it produces OpenAI-form calls through Chat Completions. A smaller model would likely meet the same `namespace` drop |
| Part B | **Not run.** After the turn, HELP_HUMAN relayed the owner's approval of part B ("yes, run the second Codex turn on the command-line path"), with the condition "If the first turn hit a stop condition, do not run Part B; return instead." The first turn hit S-8, so part B was not run. O-7 and A-7 are not observed. The harness had also already closed the supplier (D-9) before the message arrived |
| S-1…S-7, S-9…S-11 | not hit. S-2: no `lms get`, no new model folder (the listing before, after the turn and at the end is identical), 0 S-2 lines in 1,284 watch checks. S-5: during the turn the only socket of the Codex process group apart from the plugin fetch was loopback to 127.0.0.1:1234 (§8). S-6: no path under `~/.codex` was opened by the group in 237 snapshots. S-9: pressure level ≤ 2 throughout. S-10: exactly one Codex model request (one `POST /v1/responses`); LM Studio's three internal predictions were the server's own handling of that request |
| Deviation D-1 | P-3 pass condition "normal" not met (level 2, warn). The run went ahead under S-9's definition (critical) with continuous sampling (§4) |
| Deviation D-2 | The warm home was not fully warm (§2), so the plugin re-sync happened at start. The brief records this as not a stop (U-18) |
| Deviation D-3 | The harness's S-5 classifier took GitHub address ranges from a fixed list. The plugin fetch used an address outside that list, and it was classified from the process's command line instead (`git-remote-https https://github.com/openai/plugins.git`). The connection began before the turn |
| Interpretation | The harness would have accepted an elicitation carrying `_meta.codex_approval_kind = "mcp_tool_call"` for `obs1`, reading it as row 1 of the brief's answer table (an approval whose subject is the obs1 tool call). The binary's strings show that Codex can raise MCP tool approvals this way or through request_user_input. It did not arise |

## 7. Part D — per-thread MCP configuration (no model call)

After `turn/completed`, a second `thread/start` was sent with `config {"mcp_servers.obs1d": {"command": "/usr/bin/python3", "args": [the double, "--log", "<OBS>/logs/mcp_partd.jsonl"]}}` and no turn. It returned thread `…7f28280` with model and provider as configured. `mcpServer/startupStatus/updated` arrived for **both** `obs1d` and `obs1` on the new thread (`starting` → `ready` in 59 ms). `mcpServerStatus/list {threadId}` listed `obs1` and `obs1d`, each `runtimeStatus: "connected"` with tool `example_lookup`. `mcpServerStatus/list {}` listed only `obs1`, with `runtimeStatus: null`. LM Studio received no request for part D. **A-6: a dotted-key per-thread `config` adds an MCP server to that thread only, alongside the configured ones; it is observed only through a thread-scoped status list.**

## 8. Network and process observations

| Source | Observed |
|---|---|
| Codex → LM Studio | one loopback TCP connection 127.0.0.1 → 127.0.0.1:1234 from the turn's start to its end; endpoint `/v1/responses`, streamed (L-2 **observed** for this pair: Codex 0.158.0 used the Responses interface of LM Studio 0.4.16) |
| Codex → chatgpt.com (start-up, before any thread) | per Codex's own log in the scratch home: a remote-control websocket loop started for `https://chatgpt.com/backend-api/` and logged `installation_id` and `server_name` (it then waited: "remote control requires ChatGPT authentication"). A featured-plugins request to `https://chatgpt.com/backend-api/plugins/featured?platform=codex` failed with **401 Unauthorized**. Snapshots show one TLS socket from `codex` to a Cloudflare address (2606:4700:4408::…:443) from 18:45:00.6 to before 18:45:01.2. This is the supplier's own start-up traffic (L-4, U-18), not a model request and not a sign-in request to the client. **It is not treated as S-3 or S-5 (it occurred before the thread, and no `account/*` request or auth error came to the client), but HELP_HUMAN should note it.** Whether the logged installation id and host name were sent in that request is not observed |
| Plugin sync (S-F-10) | `git ls-remote` then a fetch of `https://github.com/openai/plugins.git` by `git` children of Codex (TLS to 2604:5580:21::…:443), from 18:45:00.6 to ≈18:45:29, **overlapping the first 25 s of the turn**. `.tmp/plugins/` and `plugins.sha` (5fd93af4cd0c…) were written; `.tmp` is 88 MB after the run. Recorded as the supplier's own traffic (U-18); not a stop |
| MCP test tool | stdio only; no IP socket |
| LM Studio itself (not attributed to Codex) | short TLS connections from the LM Studio app to Cloudflare addresses (2606:4700:20::…) roughly every 300 s, from before this node started the server and throughout. The `lmlink-connector` process held and opened many TLS connections to many hosts before and throughout (LM Studio's own peer service, already running before this node started). No `lms get`, no new model folder |
| Process tree | `codex` (own process group) with `git` descendants during the sync (one `<defunct>` seen briefly at 18:45:29) and the MCP double instances. At exit after stdin closed: exit code 0 in ≈14 ms, and **no survivors** in the group 500 ms later (H11: none at this exit) |
| Written into the scratch home | new: `sessions/2026/09/30/rollout-…jsonl` (44,719 B), `thread_history_1.sqlite` (+ -shm, -wal), `thread-writer-locks/`, `shell_snapshots/` (empty), `.sandbox_migration`, `.tmp/plugins/`, `.tmp/plugins.sha`; removed: `.tmp/plugins-clone-…`, some sqlite -shm/-wal files; `logs_2.sqlite` grew (447 log rows for this run, including the host name and installation id in the remote-control lines) |

## 9. Item rows

### EXEC (DEL-02-03, §2.5.3)

| ID | Observed value |
|---|---|
| O-1 | **not observed** (no `mcpToolCall` item; S-8). Observed instead: for each item, `item/started` then its deltas then `item/completed`, then `thread/tokenUsage/updated`, `account/rateLimits/updated`, `thread/status/changed` and `turn/completed`, in that order |
| O-2 | **not observed** (no call reached Codex). The model's attempted arguments were `{"key": "EX-1"}` (twice, in Qwen's XML tool format inside LM Studio) |
| O-3 | **not observed** (no call; no EX-ERR case) |
| O-4 | **not observed**: no approval request of any kind was raised during the turn under `on-request` / `read-only` / reviewer `user`, but no MCP call was attempted by Codex, so this says nothing about MCP-call approval |
| O-5 | **3** `agentMessage` items (texts "\n\n", "\n\n", then the final sentence). `phase` is present on every item, with value **null**. The last agentMessage completed (r171) **before** `turn/completed` (r175). `turn/completed.turn.items` held only the last agentMessage (`itemsView: "summary"`). Three `reasoning` items with `content` (raw text) and `summary` [] |
| O-6 | Item identity is the same in `item/started` and `item/completed` for all 7 items. `turn/completed` status `completed`, error null, durationMs 67,711. The turn object carries no model element (F-23 confirmed live) |
| O-7 | **not observed** (part B not run: §6) |
| O-8 | not in this brief |
| O-9 | **not observed**: no `item/tool/requestUserInput` (the tool `request_user_input` was offered to the model; it was not used) |

### ADAPTER (DEL-03-03, §3.5, §9, UNRESOLVED)

| ID | Observed value |
|---|---|
| A-1 | Before any thread, `mcpServerStatus/list {}` listed `obs1` with runtimeStatus **null**, tools {example_lookup (name, description, inputSchema as served)}, httpOrigin **null** (stdio), authStatus `unsupported`, serverInfo, serverCapabilities, resources [] (the double answers −32601 to `resources/list` and `resources/templates/list`, and Codex logged WARN and carried on). No startup notification came before the thread existed. On the thread: `mcpServer/startupStatus/updated` `starting` (right after `thread/started`) → `ready` 18 ms later, during turn start. The thread-scoped list shows `runtimeStatus: "connected"` (part D) |
| A-2 | **not observed** (= O-4) |
| A-3 | **not observed** for `tools/call`. Observed for the other messages the MCP server received: `initialize` {protocolVersion 2025-06-18, capabilities {elicitation {form, url}} plus, for the thread-scoped instances, `experimental {"codex/auth-change": {}}`, clientInfo {name `codex-mcp-client`, title `Codex`, version 0.158.0}}; `tools/list`, `resources/list` and `resources/templates/list` each with `_meta {progressToken n}` |
| A-4 | **not observed** (no call; no retry question arises) |
| A-5 | **partly observed**: the MCP stdio server, spawned by the supplier under `sandbox_mode = read-only`, wrote its log to `<OBS>/logs/mcp.jsonl`, outside the thread's cwd, at every instance. Its own file writes were not confined by the read-only sandbox. The `logWritable` element of a tool result was not observed (no call) |
| A-6 | **observed** (part D, §7) |
| A-7 | **not observed** (part B not run) |

### HOSTING (DEL-01-01)

| ID | Observed value |
|---|---|
| H1 | The vendor binary, unmodified (sha256 as SPIKE §3), was run directly with one added environment key `CODEX_HOME`; argv `V app-server`, own process group |
| H4 | Early frames: `remoteControl/status/changed` arrived with the initialize response, emitted before `initialized` (as in the spike). No MCP startup notification came before a thread existed. The `warning` (model metadata) came before the turn/start response |
| H6 | Every notification carried top-level `emittedAtMs`. The frames were kept unchanged in the log |
| H8, H10 | not exercised (no server request; every client request received a response) |
| H11 | At exit: 0 survivors in the group after 500 ms. During the run the supplier had `git` descendants (plugin sync) and one short-lived `<defunct>` child |
| H2, H3, H5, H7, H9 | not exercised by this observation (App-side invariants; no App candidate) |
| §8.3 / U-19 | Requested and reported values were equal at thread start (model `qwen/qwen3.5-9b`, provider `obs1_lmstudio`); no `model/rerouted`; the turn object carries no model element (F-23) |
| L-2 / U-22 | **observed at this pair**: the custom provider with `wire_api = "responses"` works against LM Studio 0.4.16 `/v1/responses` (streamed); LM Studio ignored `prompt_cache_key` and `include: reasoning.encrypted_content`, converted the developer role to system and **dropped `namespace` tools** |
| L-3 | **observed negative at this pair**: tool calling to an MCP tool through this provider did not work, because the tool never reached the model (§5). Function calling itself works in LM Studio's Chat Completions (part C). With the Responses interface, P-5 gave no call either (the model's choice), so function calls through `/v1/responses` are not shown either way |
| U-09 | not observed (no server request, so no `serverRequest/resolved`) |
| L-4 / U-18 | start-up traffic to chatgpt.com (remote control, featured plugins 401) and github.com (plugin sync), even with `[analytics] enabled = false` (§8) |
| stderr | 0 bytes |

## 10. Part C — Chat Completions representation points (LOOP fixture basis; not a Codex turn)

Three streamed requests to `POST http://127.0.0.1:1234/v1/chat/completions` with invented content, sent to LM Studio 0.4.16+2 serving `qwen/qwen3.5-9b` (context 24576). Raw SSE is in `<OBS>/logs/partc/C1.sse` (sha256 d60075f5ff6c…), `C2.sse` (5a433d06415f…) and `C3.sse` (abbd90360036…). Every request returned HTTP 200 with no `Server` header. Chunks carry `id`, `object: chat.completion.chunk`, `created`, `model` and `system_fingerprint` (= the model key). The first chunks stream `delta.reasoning_content`, before any content or tool call.

| Point | Observed |
|---|---|
| 1 — streamed tool-call fragments (C1: one tool `example_lookup`, "call it with key EX-1") | The call arrives in **two** `delta.tool_calls` chunks. First `{index 0, id "951856930", type "function", function {name "example_lookup", arguments ""}}`, then `{index 0, type "function", function {arguments "{\"key\":\"EX-1\"}"}}`: the id and name come once, and the arguments come as **one whole JSON string** in the second fragment, not character by character. The id is a numeric string. `delta.content` "\n\n" also appeared (whitespace) |
| 2 — finish reason | the final chunk has an empty `delta` and `finish_reason: "tool_calls"`, followed by `data: [DONE]`. All other chunks have `finish_reason: null` |
| 3 — several calls in one response (C2: "call example_lookup twice at the same time, EX-1 and EX-2") | **two calls in one response**, as index 0 (id "780803223", args `{"key":"EX-1"}`) and then index 1 (id "650034572", args `{"key":"EX-2"}`). Each index follows the same two-fragment pattern (name first, then whole arguments), and index 0 completes before index 1 begins. One final `finish_reason: "tool_calls"` |
| 4 — "no arguments" (C3: tool `example_ping`, parameters `{"type":"object","properties":{}}`) | the arguments text sent is **`"{}"`** (an empty JSON object as a string; not `""`, not null); `finish_reason: "tool_calls"` |

## 11. Files

| File | sha256 |
|---|---|
| `Design/OBS_1_0.158.0.md` (this record) | see the return file `WAVE_B/OBS-1.md` |
| `Design/prototype/obs1/obs1_harness.py` | 0b1325547b78c1a66b6685de4170d061dfa152fabc4a58752600b7ab045c8442 |
| `Design/prototype/obs1/download_watch.sh` | 79436fce9ffb9bea2b7503bfbf6ae06af093a000c0c2280b3e1c951ea2551172 |
| `Design/prototype/obs1/partc_chat.py` | cc5e1ded3fb6e0b308334ed48d36903d49270aacf21a5d242ce48e5859630756 |
| raw, not committed: `<OBS>/logs/frames.jsonl` | 0965e24adefacaf19c63bf9f7331d82429c31b22cbb82f9b332b1e9582e6ef2c |
| raw: `<OBS>/logs/mcp.jsonl`, `mcp_partd.jsonl` | 837eceb3bcebd29d…, 809366382ec74ef1… |
| raw: `<OBS>/logs/lmstudio.server.log`, `lmstudio.model.log` | e3ce145a6f3380a4…, 91ac78d5efc3c533… |
| raw: `snapshots.jsonl`, `harness_events.jsonl`, `download_watch.log`, `preflight.txt`, `p5_response.txt`, `partc/`, `codex_home_before/after.txt`, `models_before/after.txt`, the scratch home with its rollout | in `<OBS>/logs` and `<OBS>/codex-home` |

## UNRESOLVED

- Whether Codex 0.158.0 can be made to offer MCP tools as flat function tools to a Responses provider (a provider capability or configuration setting), and whether a different local server accepts `namespace` tools. Either needs another turn and an owner or HELP_HUMAN decision.
- O-1…O-4, O-7, A-2…A-4, A-7 and U-09 remain unobserved.
- Whether the start-up request to chatgpt.com carried the installation id or host name (Codex's local log records them beside the URL).

## OBS-1b (command-line turn)

- **Date:** 2026-09-30 (turn 19:15:14–19:16:07 UTC). **Node:** OBS-1b (Type 2 TASK) of run `APP-V4-DESIGN-PASS-2-20260930`, launched by HELP_HUMAN. Appended to this record; the sections above are unchanged.
- **Standing:** as above: a dated observation at one version (Codex 0.158.0, LM Studio 0.4.16+2, `qwen/qwen3.5-9b`), **not qualification**, no App candidate. The one approval answer in this turn came from the harness with origin `observation-harness`. It is not a person's act and is never A14 evidence.
- **Authority:** the owner's answer "Run the command-line turn locally (Recommended)" (`OWNER_DECISIONS.md` "OBS-1 follow-up after no tool call", read at sha256 b2fa81871cbf…); `BRIEFS.md` "OBS-1b — the command-line turn" (19e38ed8e0e3…); `WAVE_B/OBS-1_BRIEF.md` §11 Part B (b3e7a4b6d98f…). Limits applied: one fresh `app-server` process and thread, one turn, approval policy `untrusted`, sandbox `read-only`, no MCP server, route R-1 only, no Part C or D, no download, no sign-in, invented material only.
- **Result in one line:** **the command ran through Codex.** The model called the flat function tool `exec_command`. Codex raised one `item/commandExecution/requestApproval`, which the harness accepted. The command ran inside the read-only sandbox and exited 0 with the tool's JSON line. The sandbox **denied the local Unix-socket probe**: the kernel logged `deny(1) network-outbound <OBS-B>/probe.sock`. The turn completed with a one-sentence answer that reported both facts.

**Redaction:** as at the top of this record. Also `<OBS-B>` = `<OBS>/obs1b`. The host's time zone, which Codex again put in the model's context, is left out.

### B.1 Set-up and what differed from the first run

| Item | Value |
|---|---|
| Codex binary | the same vendor binary, sha256 `788a818f…35c8` (P-1 pass again at 19:12 UTC) |
| Scratch | `<OBS-B>/codex-home` = a `cp -Rp` copy of the first run's scratch home (`.tmp/plugins/` present, `plugins.sha` 5fd93af4cd0c…; no memories rows); `<OBS-B>/cwd` (empty, not a git repository); `<OBS-B>/logs`; `<OBS-B>/tool` |
| Test tool | `<OBS-B>/tool/obs1_cli_tool.py`, a copy of `prototype/obs1_cli_tool.py` (sha256 c27dc227c2f3… for both). **Adaptation:** the brief's `python3 <path>/obs1_cli_tool.py` would put the repository path in the model's context, and that path contains the user name. The copy under `$TMPDIR` keeps the material neutral. `python3 run_cases.py` → `OBS1-test-doubles pass (model)`, TOTAL 35, FAIL 0, before the run |
| Harness | `prototype/obs1/obs1b_harness.py`, which extends `obs1_harness.py` (unchanged). It listens on `<OBS-B>/probe.sock` (88 bytes, under the 104-byte limit). It records each connection with the peer's process id. It answers approvals by one rule, and classifies S-5 sockets from the owning process's command line (repairs D-3 above) |
| Approval rule (fixed before the run) | accept, with the per-request `accept` and never a session or amendment form, only when the request's command equals the named command token for token, after one `<shell> -c`/`-lc` wrapper is removed. Any other request gets the decline form. Named command: `python3 <OBS-B>/tool/obs1_cli_tool.py --key EX-1 --probe-socket <OBS-B>/probe.sock` |
| LM Studio | server started by this node at 19:12:48; model `qwen/qwen3.5-9b` loaded at context **24576**, the same as the first run (8.1 s load, 5.57 GiB, parallel 4). The memory-pressure level was **2 (warn)** after the load, the same deviation as D-1 above. The run went ahead under S-9 ("critical"). Sampled every 250 ms: 1–2, never 4 |
| Pre-flight | P-1, P-2, P-4, P-6, P-7 as above, all pass. **P-5 was not repeated**, to keep the model calls to the turn's own |
| Download watch | `download_watch.sh` from 19:12:40 to 19:16:22 (202 checks, **0 S-2 lines**) |

`<OBS-B>/codex-home/config.toml` as run (attempt 2):

```toml
model = "qwen/qwen3.5-9b"
model_provider = "obs1_lmstudio"
sandbox_mode = "read-only"
web_search = "disabled"
model_context_window = 24576

[analytics]
enabled = false

[model_providers.obs1_lmstudio]
name = "LM Studio (OBS-1)"
base_url = "http://127.0.0.1:1234/v1"
wire_api = "responses"
```

No `[mcp_servers]` entry. `mcpServerStatus/list {}` returned `{"data": [], "nextCursor": null}`.

### B.2 Attempt 1: the supplier refuses `approval_policy = "untrusted"` in config.toml (no thread, no turn)

At 19:13:13 the first `app-server` process was started with `approval_policy = "untrusted"` in config.toml. It exited within 385 ms, before answering `initialize`. It wrote **81 bytes to stderr**: `Error: approval_policy = "untrusted" is no longer supported; remove this setting`. No thread or turn existed and no model request was made (LM Studio received none). The process group opened no IP socket, so it made no network contact. The harness waited 60 s for the `initialize` response and then recorded S-11 (`<OBS-B>/logs/attempt1/`). **Finding:** at 0.158.0 the *configuration file* no longer takes `untrusted`, but the generated protocol type `AskForApproval` still lists `"untrusted"`, and `thread/start` accepted it (B.3).

**Deviation D-B1:** the key was removed, as the message says, and `untrusted` was requested on `thread/start` only. The harness would have started no turn unless the thread reported `approvalPolicy: "untrusted"`, and the thread did report it. A second fresh process ran the one turn. The limit of one turn on a fresh process and thread held, because the first process had no thread, no turn and no network activity.

### B.3 The exchange (attempt 2; `<OBS-B>/logs/frames.jsonl`: 6 sent, 109 received)

Times are wall-clock offsets from `turn/start` (19:15:14.041 UTC), taken from the supplier's `emittedAtMs`/`startedAtMs`/`completedAtMs`, or from the harness where marked.

| # | Frame | Notes |
|---|---|---|
| s1/r1 | `initialize` → {userAgent `chirality-obs1/0.158.0 (Mac OS 26.6.2; arm64) …`, codexHome `/private` + `<OBS-B>/codex-home` (**S-1 not hit**)} | |
| s2, r2 | `initialized`; `remoteControl/status/changed` {status `disabled`, serverName `<host>`, installationId `<installation-id>`} emitted 1 ms before `initialized` was written | as in the first run (H4) |
| s3/r3 | `mcpServerStatus/list {}` → `data []` | no MCP server |
| s4/r4, r5 | `thread/start` {approvalPolicy `untrusted`, sandbox `read-only`, invented developer instructions: "You are running an observation test with invented data. When asked, run the command you are given. Keep replies to one sentence."} → model `qwen/qwen3.5-9b`, modelProvider `obs1_lmstudio` (**S-3 not hit**), **approvalPolicy `untrusted`**, approvalsReviewer `user`, sandbox {type readOnly, networkAccess false}, activePermissionProfile null, **instructionSources [] (S-4 not hit)**; `thread/started` | the rollout's turn context records `permission_profile` {managed, file_system restricted: root read, network restricted} |
| s5 | `turn/start` with the prompt "This is a test with invented data. Run \`python3 <OBS-B>/tool/obs1_cli_tool.py --key EX-1 --probe-socket <OBS-B>/probe.sock\` and report the outcome in one sentence." | |
| r6, r7 | `warning` (model metadata not found; fallback), then the turn/start response {status inProgress} | as in the first run |
| r8…r11 | `thread/status/changed` active; `turn/started`; `userMessage` started and completed | |
| +38.7 s | `reasoning` item (22 deltas) and an `agentMessage` with text "\n\n", completed at +39.9 s | 38 s of prompt processing (6,684 tokens) |
| +48.656 s | `thread/status/changed` {activeFlags **[`waitingOnApproval`]**} | emitted before the item/started frame |
| +48.664 s | **`item/started` `commandExecution`** id `call_3063367296310002`, **status `inProgress`, source `agent`**, processId null, aggregatedOutput null, exitCode null | `startedAtMs` +48.664 s |
| +48.655 s (startedAtMs) | **`item/commandExecution/requestApproval`** (server request id **0**), received **after** `item/started` | details below |
| harness +48.667 s | answer `{"decision": "accept"}` (rule matched; origin `observation-harness`) | 1 ms after receipt |
| +48.675 s | **`serverRequest/resolved`** {threadId, requestId 0} | 8 ms after the answer (U-09) |
| +48.678 s | `thread/status/changed` {activeFlags []} | |
| +48.726 s | the tool's own `toolStartedAtMs` (in its output) | 59 ms after the answer |
| +48.733 s | kernel: `Sandbox: Python(<pid>) deny(1) network-outbound <OBS-B>/probe.sock` | unified log (`sandbox_kernel_log.txt`) |
| +48.756 s | **`item/completed` `commandExecution`**, same id: **status `completed`, source `unifiedExecStartup`**, **exitCode 0**, **durationMs 0**, processId `"14601"`, aggregatedOutput below | no `item/commandExecution/outputDelta` frames at all |
| +48.763 s | `thread/tokenUsage/updated` (6,707 total); `account/rateLimits/updated` {limitId `codex`, rest null} | |
| +50.0…+53.2 s | the second model request (below); `reasoning` item (28 deltas), then the `agentMessage` "\n\nThe command ran successfully and queued proposal \`P-EX-1\` but the local socket connection failed with a \`PermissionError\`." | |
| +53.235 s | `thread/tokenUsage/updated` total 13,740 (input 13,662, cached 6,860, output 78, reasoning 50), modelContextWindow 23,347; `account/rateLimits/updated`; `thread/status/changed` idle; **`turn/completed`** {status `completed`, error null, durationMs 53,226, items [the last agentMessage], itemsView `summary`} | |

**The approval request, whole (paths redacted):** `{"kind": "command", "threadId", "turnId", "itemId": "call_3063367296310002", "startedAtMs", "environmentId": "local", "command": "/bin/zsh -lc 'python3 <OBS-B>/tool/obs1_cli_tool.py --key EX-1 --probe-socket <OBS-B>/probe.sock'", "cwd": "<OBS-B>/cwd", "commandActions": [{"type": "unknown", "command": "python3 … --probe-socket <OBS-B>/probe.sock"}], "proposedExecpolicyAmendment": ["python3", "<OBS-B>/tool/obs1_cli_tool.py", "--key", "EX-1", "--probe-socket", "<OBS-B>/probe.sock"], "availableDecisions": ["accept", {"acceptWithExecpolicyAmendment": {"execpolicy_amendment": [the same argv]}}, "cancel"]}`. There was no `reason`, `additionalPermissions`, `networkApprovalContext`, `approvalId` or top-level `emittedAtMs` (it is the only received frame without `emittedAtMs`). **`decline` and `acceptForSession` were not among `availableDecisions`**. The harness's decline form for a non-matching request would therefore have been a decision the supplier did not offer. That case did not arise, and its effect is not observed.

**aggregatedOutput (verbatim):** `{"outcome": "queued", "proposal": "P-EX-1", "key": "EX-1", "note": "invented example material", "toolStartedAtMs": 1790795762767, "localSocket": "refused: PermissionError"}` followed by `\n`.

**What the model called, and what it received back (rollout; LM Studio logs).** LM Studio received **two** `POST /v1/responses` in the turn. The first came at +0.056 s. The second came at +48.795 s, after the command output, with 6,860 tokens restored from its prompt cache and 118 new. Both were logged with "Ignoring unsupported tool type(s): namespace." and the same three field warnings as the first run. The tool list LM Studio put in the model's prompt was `exec_command`, `write_stdin`, `request_user_input`, `view_image`, `get_goal`, `create_goal`, `update_goal`. The MCP resource tools of the first run were absent, as no MCP server was configured. Some tool of type `namespace` was still dropped, but its content is not in the truncated log. The model emitted `<tool_call><function=exec_command><parameter=cmd>python3 … --probe-socket <OBS-B>/probe.sock</parameter></function></tool_call>`. LM Studio returned it as a Responses `function_call` {name `exec_command`, arguments `{"cmd": "python3 …"}`, call_id `call_3063367296310002`}. **L-3 is positive for a flat function tool at this pair.** The function output returned to the model was text: `Chunk ID: …\nWall time: 0.0002 seconds\nProcess exited with code 0\nOriginal token count: 44\nOutput:\n<the JSON line>`. No LM Studio "invalid tool name" line appeared.

**Timing reading (inference):** Codex logged the `function_call` output item at 19:15:54. The command item started at 19:16:02.705, 4 ms after LM Studio's last log line for the first prediction (a prompt-cache write). This is consistent with Codex starting the command only once the response stream completed. The stream's end event is not in any log kept.

**Content sent to the model (brief §7, adapted):** Codex's base instructions, the bundled skill descriptions under `<OBS-B>/codex-home/skills/.system`, the invented developer text and prompt, and the environment context: cwd `<OBS-B>/cwd`, shell zsh, date, **time zone**, and a read-only permission profile with root read. Then the tool's invented output. The model log has no `/Users/` path, user name, host name, installation id or scratchpad path. The time-zone finding of the first run recurs.

### B.4 Stops and deviations

| Item | Record |
|---|---|
| S-1…S-11 | **none hit** in attempt 2. S-8 (part B: no `commandExecution` item) not hit. S-2: no `lms get`, models folder and `lms ls` unchanged before, after the turn and at the end. S-5: during the turn the Codex process group's only IP sockets were loopback to 127.0.0.1:1234 (two connections, one per model request). S-6: no path under `~/.codex` in 177 snapshots. S-10: one turn. Its two model requests were Codex's own continuation after the tool output, and no other request went to the model. S-3: no `account/*` request and no auth error. `account/rateLimits/updated` came twice, as a notification |
| D-B1 | attempt 1 refused by the supplier over `approval_policy = "untrusted"` in config.toml (B.2); `untrusted` requested on `thread/start` instead, and confirmed in the thread's response before the turn |
| D-B2 | the test tool was run from a scratch copy, identical in hash, not from the repository path (B.1) |
| D-B3 | memory-pressure level 2 (warn) with the model loaded, as D-1 above |
| D-B4 | P-5 not repeated (B.1) |
| Harness note | the base harness writes a `capture-metadata` event naming `on-request`. It is fixed text of `obs1_harness.py`, and the `capture-metadata-b` event that follows it gives the values actually used |

### B.5 Network and process observations (attempt 2)

| Source | Observed |
|---|---|
| Codex → chatgpt.com (start-up) | as in the first run. Codex's log shows the remote-control loop for `https://chatgpt.com/backend-api/` (the log line includes `<installation-id>` and `<host>`), "remote control requires ChatGPT authentication", then a retry about once a second for the rest of the run, and the featured-plugins request **401 Unauthorized**. One TLS socket from `codex` to 2606:4700:4408::…:443 was seen at +0.3 s after spawn, before any thread, and not again. No sign-in request reached the client |
| Plugin sync (U-18) | `git ls-remote https://github.com/openai/plugins.git HEAD` only: one TLS socket from `git-remote-https` to 2604:5580:21::…:443, from spawn +0.3 s to +1.3 s (exited). **No fetch**: `.tmp/plugins/` unchanged, `plugins.sha` unchanged |
| Codex → LM Studio | loopback only, `/v1/responses`, streamed, twice |
| The command | ran as `/bin/zsh -lc 'python3 …'` under the macOS sandbox. Kernel sandbox lines for the zsh/Python process show harmless denials (`/dev/tty` and `/dev/dtracehelper` writes, a few mach-lookups and sysctl reads) and the **network-outbound denial on the probe socket**. The harness's listener recorded **0 connections**. The process was too short-lived (~30 ms) for the 250 ms snapshots to see. Its OS process id differs from the item's `processId` "14601", which is the supplier's own identifier |
| LM Studio itself | the same background pattern as before this node (the `lmlink-connector` process's three persistent TLS connections; the app's short Cloudflare connections, one of them at 19:15:09–13, before the turn). Addresses were not resolved, so a connection to huggingface.co cannot be excluded by host name. The models-folder listing and the absence of any `lms get` process show that no download happened |
| Exit (H11) | stdin closed after `turn/completed` + 2 s; exit code 0 within 41 ms; **no survivors** 500 ms later |
| Written into the scratch home | new rollout `sessions/2026/09/30/rollout-…01a0f3be….jsonl` (43,743 B); `state_5.sqlite` 4 KB → 112 KB; the WAL files of `thread_history_1`, `state_5` and `logs_2` grew; `goals_1` -shm/-wal created; `config.toml` edited by this node (D-B1); `shell_snapshots/` stayed empty |

### B.6 Item rows (OBS-1b)

| ID | Observed value |
|---|---|
| **O-7** | **Command form:** the model sent `exec_command` {cmd: the bare command}. The item's `command` is the shell-wrapped string `/bin/zsh -lc '<cmd>'`, `commandActions` is [{type `unknown`, command: the bare command}], and `cwd` is the thread cwd. **source:** `agent` at `item/started`, **`unifiedExecStartup` at `item/completed`** (the value changes within one item). **Status:** `inProgress` → `completed`, with no intermediate item notification. **Exit code 0**; `durationMs` 0; `processId` null → "14601". **aggregatedOutput:** the JSON line plus `\n`. There were no output deltas. **Approval:** one `item/commandExecution/requestApproval` (kind `command`). Sequence: `thread/status/changed` [waitingOnApproval] → `item/started` (inProgress) → the request (its `startedAtMs` is 9 ms *earlier* than the item's) → answer → `serverRequest/resolved` → `thread/status/changed` [] → the tool runs → `item/completed`. The item is therefore announced as in progress while approval is pending |
| **A-7** | **JSON CLI content:** Codex carries the CLI's stdout as text. To the client it is `aggregatedOutput`, a string. To the model it is the JSON line inside `exec_command`'s text envelope (chunk id, wall time, exit code, token count). No structured content is derived. The model read the JSON correctly. **Local-socket probe under the read-only sandbox (OC-5):** **denied.** The connect to a Unix socket under `$TMPDIR` failed with `PermissionError` (EPERM). The kernel logged `deny(1) network-outbound` for that path, and the listener saw no connection. The **approved** command still ran inside the sandbox: under `untrusted`, approval did not lift the sandbox. Python itself ran, and read its script, under the read-only profile |
| O-4 / A-2 (command path) | an approval under `untrusted` offers `accept`, `acceptWithExecpolicyAmendment` and `cancel` only |
| O-5 | 2 `agentMessage` items ("\n\n", then the answer); `phase` present and null; the last completed before `turn/completed` |
| O-6 | same identities in started and completed for all items; turn `completed`, 53,226 ms; no model element on the turn (F-23) |
| O-9 | not used (`request_user_input` offered, not called) |
| O-1…O-3, A-1, A-3…A-6 | not in this part (no MCP server) |
| H1 | the unmodified vendor binary; `V app-server`; one added environment key `CODEX_HOME`; own process group |
| H4 | `remoteControl/status/changed` before `initialized`; `warning` before the turn/start response; `thread/status/changed` [waitingOnApproval] before both `item/started` and the approval request |
| H6 | every notification carried `emittedAtMs`; the server request did not (it carries its own `startedAtMs`) |
| H8, H10 | one server request, answered in 1 ms and resolved; every client request answered |
| H11 | 0 survivors at exit |
| U-09 | **observed:** `serverRequest/resolved` {threadId, requestId} arrives 8 ms after the client's answer, before the item continues |
| §8.3 / U-19 | requested = reported model and provider; no `model/rerouted` |
| L-2 / L-3 | Responses to LM Studio 0.4.16 again. **Function-tool calling works** through this pair (exec_command). MCP tools remain undelivered (`namespace` dropped) |
| L-4 / U-18 | start-up traffic to chatgpt.com and github.com (ls-remote only), none during the turn |
| stderr | 0 bytes (attempt 2); 81 bytes (attempt 1, B.2) |

### B.7 Files (OBS-1b)

| File | sha256 |
|---|---|
| `Design/prototype/obs1/obs1b_harness.py` | see the return file `WAVE_B/OBS-1b.md` |
| `Design/prototype/obs1/obs1_harness.py`, `download_watch.sh` | unchanged (0b1325547b78…, 79436fce9ffb…) |
| raw, not committed: `<OBS-B>/logs/frames.jsonl` | a50eb050dad61e6c… |
| raw: `harness_events.jsonl`, `snapshots.jsonl` | 8877806796425253…, fffeaaabee1487a7… |
| raw: `lmstudio.server.log`, `lmstudio.model.log` | 66da10670133babf…, 3dd3165fb4032784… |
| raw: `sandbox_kernel_log.txt` (17 kernel lines for the command's process) | 53ef246e9928fa5a… |
| raw: the rollout `rollout-…01a0f3be….jsonl` (file-name time redacted, node G) | 2293687ca945b3c7… |
| raw: `attempt1/` (frames 7c77a3dac75d50e0…, stderr 381d7e2499c6b4c0…, the config as first written) | in `<OBS-B>/logs` |

**UNRESOLVED (OBS-1b):** what the supplier does with a `decline` answer that `availableDecisions` did not offer under `untrusted` (not exercised); whether any setting lets a sandboxed command reach a local socket (OC-5 remains a design question for the App); what the `namespace` tool dropped in both runs contains (the LM Studio log truncates the request body).

## Change note (node G, run APP-V4-DESIGN-PASS-2-20260930; redaction only)

- 2026-09-30, node G under `R16_RESOLUTIONS.md` R16-3 (closeout C1-B §9 G-2;
  review V19-B n-2). §B.7 named the raw rollout of the OBS-1b turn by its
  full file name, whose time part is the host's local time; set beside the
  turn's UTC times (19:15 UTC), it showed the host's time-zone offset, which
  the redaction lines (top of this record and the OBS-1b section) say is left
  out. The time part is now redacted (`rollout-…01a0f3be….jsonl`), as §B.5
  already wrote it. Nothing else changed: no observation, value, hash or
  standing. The file's sha256 before this edit was
  `85707703e97b4fd5ea4332785aae83f96850bedacad5219c8827c41297c26182`; the
  pins of this record in HOSTING-BOUNDARY-v0.8, GUIDE-v0.5 and LOOP-v0.8
  headers name those earlier bytes, read at their nodes.
