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
