# OBS-1 brief — one live Codex turn at pin 0.158.0 against a local LM Studio model

- Written by node B6 (Type 2 TASK) of run `APP-V4-DESIGN-PASS-2-20260930`, 2026-09-30. Status: **brief, not run.** Nothing here was executed against Codex or LM Studio.
- Runs: after round 2 of Wave B (BRIEFS, "After round 2"), by HELP_HUMAN or a Type 2 node it launches.
- Authority: owner DECISION-K1 **K1-6** (`OWNER_DECISIONS.md` sha256 1dfd5bf4…af15): one live Codex turn that calls a test tool; a local model in LM Studio first; the owner's Codex sign-in only if the local route cannot produce a tool call; anything sent to a model is invented example material; the result is a dated record at one version, not qualification. The model is `lmstudio-community/Qwen3.5-9B-MLX-4bit`, already installed (HELP_HUMAN's proposal in the recorder's correction of the model-download record: no download). The owner's download answer covers **only** Qwen3 4B (`lmstudio-community/Qwen3-4B-MLX-4bit`, 2.28 GB), and only if the installed model cannot produce a tool call.
- Serves: HOSTING-BOUNDARY-v0.8 U-19, U-22 (L-2, L-3), U-09, §8.3 (DEL-01-01); EXEC §2.5.3 O-1…O-9 (DEL-02-03, node B2); ADAPTER §3.5, §9 OC-3, OC-5, OC-7, OC-12 and its UNRESOLVED supplier behaviours (DEL-03-03); LOOP §4.1 OBS-1 column (DEL-05-01, node B9) as an optional part.

## 1. What OBS-1 is, and what it is not

One Codex App Server process at 0.158.0, driven over stdio by a small
harness, starts one thread and runs **one turn** whose model is the local
LM Studio model. The turn asks the agent to call one test tool, an MCP
server that the harness supplies (`obs1_mcp_double.py`). Everything the
supplier and the tool exchange is recorded.

It is not qualification of the pin, the provider or the model; not an X-02
fixture (no App candidate, no §7.2 verification step); and not a test of
any Chirality product code. Answers the harness gives to supplier requests
are the harness's, never a person's act and never A14 evidence of a person.

## 2. Materials (all local; nothing is installed)

| Item | Where | Check before use |
|---|---|---|
| Codex 0.158.0, vendor binary run directly (launcher `vendor`, as runs A-vendor and D-vendor of the spike) | `/private/tmp/claude-501/-Users-ryan-ai-env-projects-chirality--claude-worktrees-test-ci-optimization-f6cacd/a7659cd3-fdee-45df-ac08-f767111a9f26/scratchpad/codex-0.158.0/pkg/node_modules/@openai/codex-darwin-arm64/vendor/aarch64-apple-darwin/bin/codex` (call it `V`) | `shasum -a 256 V` = 788a818fbb9596869c7a487554507cb8bdca17584b8671112b23f9e225ba35c8 (SPIKE §3). If the scratchpad is gone, **stop**: reinstalling is a new download and needs its own approval |
| MCP test tool | `DEL-01-01…/Design/prototype/obs1_mcp_double.py` (one tool, `example_lookup`; keys `EX-1` → invented result, `EX-ERR` → tool-reported error; logs every message with wall-clock ms) | `python3 run_cases.py` in that folder passes its `OBS1-test-doubles` line |
| Command-line test tool (optional part B) | `…/Design/prototype/obs1_cli_tool.py` (prints one invented JSON result with its own start time; can probe a local Unix socket) | As above |
| LM Studio and its CLI | The installed app; `~/.lmstudio/bin/lms` | `lms version`; `lms ls` lists the model key; `lms status` |
| Model | `lmstudio-community/Qwen3.5-9B-MLX-4bit` (installed, 5.98 GB) | Its exact key from `lms ls`; record it |

## 3. Scratch layout and the CODEX_HOME to use

Use `$TMPDIR`, whose path (`/var/folders/…/T/`) carries no personal name, so
the working-directory path Codex puts in the model's context is neutral:

```
OBS=$TMPDIR/chirality-obs1-0.158.0
$OBS/codex-home   CODEX_HOME for every Codex process of OBS-1
$OBS/cwd          the thread's working directory; empty; not a git repository
$OBS/logs         frame log, MCP log, process and socket snapshots, LM Studio log
```

- **CODEX_HOME:** `$OBS/codex-home`, made as a copy of the spike's warm home
  (`cp -Rp <scratchpad>/codex-0.158.0/codex-home $OBS/codex-home`). The copy
  already holds the plugin sync (`.tmp/plugins/`, `.tmp/plugins.sha`), so the
  ≈24 MB fetch that a fresh home causes (S-F-10) is not expected at start.
  The spike folder itself is only read. Never `~/.codex`; never the person's
  own Codex home.
- **`$OBS/codex-home/config.toml`**, written by the harness (keys typed in
  the generated `Config` are marked T; the others are the published
  configuration form, `published-only`, and are confirmed by the run):

```toml
model = "<exact key from lms ls>"                 # T
model_provider = "obs1_lmstudio"                  # T
approval_policy = "on-request"                    # T
sandbox_mode = "read-only"                        # T
web_search = "disabled"                           # T (WebSearchMode)
model_context_window = <context length loaded in LM Studio>   # T

[analytics]                                       # T (AnalyticsConfig)
enabled = false

[model_providers.obs1_lmstudio]                   # published-only
name = "LM Studio (OBS-1)"
base_url = "http://127.0.0.1:1234/v1"
wire_api = "responses"

[mcp_servers.obs1]                                # published-only
command = "/usr/bin/python3"
args = ["<repo>/…/Design/prototype/obs1_mcp_double.py", "--log", "<OBS>/logs/mcp.jsonl"]
```

- **Provider route.** Route R-1 above defines the local server as an
  ordinary provider entry, so Codex has no reason to manage LM Studio's
  models. Route R-2, only if R-1 fails at thread start for a provider-form
  reason: the built-in `lmstudio` provider (`model_provider = "lmstudio"`,
  the CLI's `--oss --local-provider lmstudio` equivalent) with the model
  already loaded. F-28 of HOSTING-v0.8 records strings in the binary that
  suggest the built-in route can run `lms get --yes <model>`, a download;
  under R-2 the download watch of §6 is critical.

## 4. Pre-flight (no Codex process yet)

| # | Step | Pass condition | Otherwise |
|---|---|---|---|
| P-1 | `shasum -a 256 V` | equals the SPIKE §3 value | stop (S-11) |
| P-2 | `lms status`; `lms server start` if needed; `lms ls` | server on 127.0.0.1:1234; the model key listed | stop (S-11) |
| P-3 | `lms load <key> --context-length <n>` (confirm the flag with `lms load --help`; pick *n* ≥ 32768 if memory allows, and record it); `lms ps` | the model loaded; memory pressure normal (`memory_pressure` or Activity Monitor) | try a smaller *n* once; then stop (S-9) |
| P-4 | `GET /v1/models` | lists the key | stop (S-11) |
| P-5 | One `POST /v1/responses` with invented input ("Reply with the word OK.") and one invented function tool | a well-formed response; record whether a function call can come back | if `/v1/responses` is not served, stop before Codex (S-11): Codex 0.158.0 appears to need that interface (F-28) |
| P-6 | Start `lms log stream` into `$OBS/logs/lmstudio.log`; record the LM Studio app version | log running | continue without it, and say so |
| P-7 | Snapshot `lms ls` and LM Studio's models folder listing | recorded | — |

P-5 sends invented text straight to the local server, not through Codex. It
is a check of the server interface; if HELP_HUMAN reads K1-6 as excluding
it, skip it and let the Codex turn show the same.

## 5. The harness and the exact sequence

The harness extends the spike's `_spike/handshake.mjs` pattern (or is a
Python script): spawn `V app-server` with `CODEX_HOME=$OBS/codex-home`,
cwd `$OBS/cwd`, in its own process group; one reader for stdout (one JSON
object per line), one for stderr (bounded); a **recording tap** that writes
every frame in both directions to `$OBS/logs/frames.jsonl` with direction,
receipt or send position, monotonic offset and wall-clock ms, unchanged
(HOSTING §9.1). App→supplier frames carry `"jsonrpc":"2.0"` as in the spike.

| Step | Harness sends | Expected supplier frames (from the generated types; not observed) | Record | Serves |
|---|---|---|---|---|
| D-1 | spawn | — | pid, pgid, argv, env keys added | H1, S-F-02 |
| D-2 | `initialize` {clientInfo {name `chirality-obs1`, title `Chirality OBS-1`, version `0.0.0-obs1`}, capabilities {experimentalApi false, requestAttestation false}} | response {userAgent, codexHome, platformFamily, platformOs}; `remoteControl/status/changed` before `initialized` (recorded at the spike) | whole frames; **S-1** if `codexHome` ≠ `$OBS/codex-home` | §7.1 |
| D-3 | `initialized` | any early notifications, e.g. `mcpServer/startupStatus/updated` for `obs1` (`starting` → `ready` or `failed`) | order and times | ADAPTER §3.5 |
| D-4 | `mcpServerStatus/list` {} (App-origin read) | `obs1` with its tools, `runtimeStatus`, `httpOrigin` null (stdio) | whole response | ADAPTER OC-5; HOSTING §6.8 |
| D-5 | `thread/start` {cwd `$OBS/cwd`, model `<key>`, modelProvider `obs1_lmstudio`, approvalPolicy `on-request`, sandbox `read-only`, developerInstructions (invented, §7)} | response {thread, model, modelProvider, approvalPolicy, approvalsReviewer, sandbox, cwd, instructionSources, …}; `thread/started` | requested vs reported model and provider; **S-3**, **S-4** checks before D-6 | HOSTING §8.2, §8.3, F-20; RS R5 |
| D-6 | `turn/start` {threadId, input [{type `text`, text: the prompt of §7}]} | response {turn}; `turn/started`; `item/started`/`item/completed` for `userMessage`; reasoning items and deltas (if the provider sends them); **`item/started` of an `mcpToolCall`** {server `obs1`, tool `example_lookup`, arguments, status `inProgress`}; any server request (see D-7); `item/mcpToolCall/progress`; `item/completed` of the `mcpToolCall` (status, result, error); possibly a second call (`EX-ERR`); `agentMessage` items and `item/agentMessage/delta`; `thread/tokenUsage/updated`; `turn/completed` {turn status} | every frame; per item: identity, type, status at start and end, `startedAtMs`, `completedAtMs`; the MCP log's receipt time of each `tools/call` | EXEC O-1…O-6; HOSTING L-3, H6 |
| D-7 | Answers to server requests (table below) | `serverRequest/resolved` (if the supplier sends it) | request frame, answer frame, any resolution notification, times | EXEC O-4; HOSTING U-09, U-19; ADAPTER OC-12 |
| D-8 | nothing until `turn/completed` or the time limit (S-7) | — | — | — |
| D-9 | close stdin (a stop record is written first: actor HELP_HUMAN, reason "OBS-1 end") | exit | exit code and signal; process tree 500 ms after exit (MCP double reaped or not) | HOSTING §4.5, H11 |

**Answers the harness gives (origin `observation-harness`, recorded as such):**

| Server request | Answer |
|---|---|
| Any approval request (`item/permissions/requestApproval`, `item/commandExecution/requestApproval`, `item/fileChange/requestApproval`, legacy kinds) whose subject is the `obs1` tool call, or in part B the named CLI command | the accept form for that one request (`accept`, or the permissions grant with scope `turn`) |
| Any other approval request | the decline form |
| `mcpServer/elicitation/request` | `{"action": "decline"}` |
| `item/tool/requestUserInput` | answers map with the invented text "Invented example answer: proceed." (optional O-9 is recorded) |
| `currentTime/read`, `item/tool/call`, `account/*`, `attestation/generate`, anything else | explicit JSON-RPC error; `account/chatgptAuthTokens/refresh` is also **S-3** |

## 6. Expected network side effects, and how to observe them

| Source | Expected | Observed by | If something else happens |
|---|---|---|---|
| Codex → LM Studio | HTTP on loopback 127.0.0.1:1234, during the turn only | socket snapshots; `lmstudio.log` (endpoint paths, e.g. `/v1/responses`, and streaming) | a model request to any non-loopback host → **S-5** |
| Plugin sync (S-F-10) | none at start with the warm-home copy; a later re-sync is not observed and may happen (`git` children fetching `github.com/openai/plugins`, ≈24 MB) | process snapshots (`git` descendants); socket snapshots (443) | recorded as the supplier's own traffic (U-18); not a stop |
| Other supplier start-up traffic (model list refresh, analytics, remote control) | analytics disabled by configuration; remote control reported `disabled` at the spike; model-list refresh not observed | socket snapshots | recorded with process, host, port and time; stop only under S-5 |
| MCP test tool | none (stdio child of Codex) | its log; snapshots | any IP socket from it → record (it opens none by design) |
| LM Studio itself | not attributed to Codex; only downloads matter | `lms` processes; models-folder listing before and after | any `lms get` process, a new model folder, or a connection to `huggingface.co` → **S-2** |

**Snapshots:** every 250 ms from D-1 to 500 ms after exit:
`ps -axo pid,ppid,pgid,command` filtered to the Codex process group and to
`lms`; `lsof -nP -a -i -g <pgid>` for IP sockets; `lsof -nP -g <pgid>`
filtered to paths under `~/.codex` (S-6). Also a listing of
`$OBS/codex-home` before and after (what the supplier writes: rollouts,
databases; relevant to OI-009).

## 7. What may be sent to the model

Only invented example material, plus what Codex adds by itself:

- developer instructions: "You are running an observation test with
  invented data. When asked, use the example_lookup tool. Keep replies to
  one sentence."
- the prompt: "This is a test with invented data. Call the tool
  example_lookup with key EX-1. Then call it again with key EX-ERR. Then
  reply in one sentence naming the proposal from the first call and saying
  whether the second key was found." (The second call serves O-3's error
  case; the first call is the one that must happen.)
- the tool's invented name, description, schema and results
  (`obs1_mcp_double.py`);
- what Codex adds: its base instructions, the bundled skill descriptions in
  the scratch home, and its environment context (the `$TMPDIR` working
  directory, shell, date). Nothing from the repository, `~/.codex`, the
  owner's files or any real project.

After the run, read `lmstudio.log` for the prompt Codex actually sent and
record whether any path or name outside `$OBS` appears (for example the
scratchpad path of the binary, which contains the user name). If one does,
record it as a finding: it stayed on this machine, but K1-6 asks for
invented material only.

## 8. Stop conditions

On any stop: record the time and reason, close stdin, end the Codex process
group after 2 s (SIGTERM, then SIGKILL), take the exit snapshot, keep every
log, and report to HELP_HUMAN.

| ID | Condition | Where checked |
|---|---|---|
| S-1 | `codexHome` in the initialize response is not `$OBS/codex-home` | D-2 |
| S-2 | Any model download: an `lms get` process, a new model folder, a connection to `huggingface.co` (LM Studio or Codex) | throughout. Only Qwen3 4B may be downloaded, and only as §9 says |
| S-3 | The thread start reports another provider or model than configured, or any sign-in is asked for (an `account/*` request, `account/chatgptAuthTokens/refresh`, an auth error) | D-5, D-7. The owner's Codex sign-in needs a new owner answer |
| S-4 | `instructionSources` lists a path outside `$OBS` (e.g. `~/.codex/AGENTS.md`, a repository `AGENTS.md`) | D-5, before any turn |
| S-5 | During the turn, a connection from the Codex process group to a non-loopback host other than the plugin repository (a possible cloud fallback) | snapshots; send `turn/interrupt` once, then stop |
| S-6 | The Codex process group opens a path under `~/.codex` | snapshots |
| S-7 | No `turn/completed` within 10 minutes | send `turn/interrupt` once (this also observes its live effect, HP-2, U-19), wait 60 s, stop |
| S-8 | The turn completes with no `mcpToolCall` item | after D-6; see §9 |
| S-9 | LM Studio cannot load the model, or memory pressure turns critical | P-3; throughout |
| S-10 | A second turn or any extra model call not in this brief | never started without HELP_HUMAN's explicit decision |
| S-11 | A pre-flight step fails | §4 |

## 9. If no tool call comes out (S-8)

Stop, keep the record, and return to HELP_HUMAN. Under the owner's answer,
the next step is to download Qwen3 4B (`lmstudio-community/Qwen3-4B-MLX-4bit`,
2.28 GB, Apache-2.0) and try one turn once more with the same brief. Any
other model, or the owner's Codex sign-in, needs a new owner answer
(K1-6; the model-download record).

## 10. What to record for each consumer

**For DEL-02-03 (EXEC §2.5.3, node B2):**

| ID | Observation | From |
|---|---|---|
| O-1 | The full notification sequence for the `mcpToolCall` item and `turn/completed`; whether `item/started` reaches the harness **before** the MCP double logs the `tools/call` (compare `startedAtMs` and the harness's receipt wall-clock with the double's `wall_ms`) | frames.jsonl; mcp.jsonl |
| O-2 | Whether the item's server and tool equal `obs1` and `example_lookup`, and its arguments are the model's arguments as an object | frames.jsonl; mcp.jsonl `tools/call` params |
| O-3 | The completed item's result shape for `EX-1` (content, structuredContent) and for `EX-ERR` (isError): does the error show as status `failed` or as `completed` with error content | frames.jsonl |
| O-4 | Whether an approval request is raised for the MCP call under `on-request`, which kind, and where it falls in the sequence | frames.jsonl |
| O-5 | How many `agentMessage` items the turn has; whether `phase` is present; whether the last one completes before `turn/completed` | frames.jsonl |
| O-6 | Same item identity in `item/started` and `item/completed`; the `turn/completed` status | frames.jsonl |
| O-7 (part B) | The `commandExecution` item for the CLI tool: command form, `source`, status transitions, exit code, aggregated output; any approval request and its place | part B |
| O-8 (optional) | A file write: not in this brief (the sandbox is read-only); left for a later observation | — |
| O-9 (optional) | Whether the model used `item/tool/requestUserInput` | frames.jsonl |

**For DEL-03-03 (ADAPTER §3.5, §9, UNRESOLVED):**

| ID | Observation | From |
|---|---|---|
| A-1 | MCP startup states for `obs1` and the status list entry (`runtimeStatus`, tools, `httpOrigin`) | D-3, D-4 |
| A-2 | The MCP call's A14 path (= O-4) | D-7 |
| A-3 | What the MCP server receives: `tools/call` params, including any `_meta` Codex adds (OC-7: whether the App could carry metadata this way is a separate question) | mcp.jsonl |
| A-4 | Supplier behaviour on a tool-reported error: item status, whether Codex retries the call | O-3; mcp.jsonl call count |
| A-5 | Sandbox effect on the MCP stdio server: could it write its log (`logWritable` in its result) | mcp.jsonl; the tool result |
| A-6 (optional, part D) | Per-thread MCP configuration (OC-3 (b)) | part D |
| A-7 (part B) | Command-line tool content for a JSON CLI (OC-9) and the local-socket probe under the read-only sandbox (OC-5) | part B |

**For DEL-01-01 (HOSTING U-19, U-22, U-09, §8.3):** requested versus
reported model and provider at thread start, any `model/rerouted`, and
whether the turn object carries a model (F-23); the endpoint Codex calls on
LM Studio and whether tool calling works through it (L-2, L-3); the
`serverRequest/resolved` notification after any answered request (U-09;
the §6.2.1 reading); early frames and their order (H4); stderr bytes; the
process tree at exit (H11); every non-loopback connection (L-4); what the
supplier writes into the scratch home.

## 11. Optional parts (each needs HELP_HUMAN's explicit decision)

- **Part B — command-line path (O-7, A-7).** A second turn on the same
  thread with `approvalPolicy` `untrusted`: "Run `python3 <path>/obs1_cli_tool.py
  --key EX-1 --probe-socket <OBS>/probe.sock` and report the outcome in one
  sentence." The harness listens on `probe.sock` (Unix socket, local). K1-6
  names one turn: a second turn is an extension of it, for HELP_HUMAN to
  decide or to put to the owner. SWBPIPE offers a command-line seam, not
  MCP (ADAPTER OC-1), so this part is the more relevant one for the first
  connected operation.
- **Part C — LOOP fixture basis (R12-8; LOOP §4.1 OBS-1 column; node B9).**
  Direct requests from a small script to `POST /v1/chat/completions` on the
  same LM Studio server, not through Codex, with invented content: one
  streamed request with one tool (point 1: fragments and how arguments
  arrive; point 2: the finish reason); one request asking for two calls
  (point 3); one with a tool that has no parameters (point 4: the argument
  text sent). Record raw responses and the server version. This is not a
  Codex turn; HELP_HUMAN decides whether K1-6 covers it.
- **Part D — per-thread MCP configuration (A-6).** A second `thread/start`
  with a `config` object naming a second MCP server entry, **no turn**,
  then `mcpServerStatus/list` with its thread identity: does the entry
  appear? No model call is made.

## 12. The record OBS-1 leaves

A new dated observation record (for example `Design/OBS_1_0.158.0.md` in
DEL-01-01, beside `PIN_SPIKE_0.158.0.md`, which is not edited), with: the
commands, versions (Codex binary identity, LM Studio version, model key and
loaded context length), the configuration used, the frame log and the MCP
log redacted as HOSTING §9.1 says (host name, installation identifier, home
path, user name), the snapshot summaries, every stop or deviation, and one
row per O-, A- and H- item: observed value, or "not observed" with the
reason. Each observation is dated and at one version; nothing is qualified.
The raw logs stay in `$OBS/logs` until HELP_HUMAN decides what is committed.

## 13. Risks

| Risk | Effect | Handling |
|---|---|---|
| Codex's local-provider path can download a model (strings in the binary, F-28) | an unapproved multi-GB download | route R-1; model pre-loaded; download watch; S-2 |
| LM Studio does not serve `/v1/responses`, or not tool calls through it | no Codex turn possible with the local route | P-5 finds it before Codex starts; §9 |
| A 9B model at 4-bit may not issue a well-formed tool call through Codex's long system prompt; the context may overflow at a small window | S-8 | load with a large context (P-3); §9 (Qwen3 4B next) |
| 16 GB memory with the model and a large context | swapping or a failed load | P-3; S-9 |
| The warm-home copy re-syncs plugins during the run | ≈24 MB fetch from `github.com` | recorded, not a stop (U-18) |
| Codex reads instruction files outside the scratch home | non-invented material sent | S-4 before the turn |
| The harness's answers to approval requests could be mistaken for a person's A14 | a false act record | origin `observation-harness` on every answer; the record is never an X-04 or X-05 fixture |
| The session scratchpad (the binary) is removed before OBS-1 | no binary without a new download | P-1; stop and ask |
| The person's own Codex desktop process writes `~/.codex` during the run (F-18) | confusion over attribution | S-6 checks the Codex process group only; record, do not infer |
