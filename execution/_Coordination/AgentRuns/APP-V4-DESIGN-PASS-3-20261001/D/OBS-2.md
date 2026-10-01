# OBS-2 — return to HELP_HUMAN

- Node OBS-2 (Type 2 TASK), run `APP-V4-DESIGN-PASS-3-20261001`, 2026-10-01 19:50–20:24 UTC.
- Brief: `BRIEFS.md` "OBS-2" (sha256 `b261394112d7…`); scope R17-16 (`R17_RESOLUTIONS.md` `b0af81bcbad9…`); authority K-11 (`OWNER_DECISIONS.md` `9d18c40dd7d8…`); method from `WAVE_B/OBS-1_BRIEF.md` and OBS-1's harness. Additions from HELP_HUMAN during the run, under the same limits: O-4a, O-4b, O-8.
- Record: `PKG-01…/DEL-01-01…/Design/OBS_2_0.158.0.md` (redacted as OBS-1's). Standing: dated observations at Codex 0.158.0 with LM Studio 0.4.16+2 and `qwen/qwen3.5-9b`; not qualification.
- Hard limits held: no sign-in, no API key or token, no download (`lms ls` and the models folder unchanged; 0 S-2 lines), no install, scratch `CODEX_HOME`s only (never `~/.codex`; S-6 not hit), invented material only. Every Codex process, tap, log stream and the download watch started by this node was stopped; LM Studio's server, which this node started, was stopped and the model unloaded.

## Items

| Item | Status | Finding |
|---|---|---|
| O-1 interrupt | observed | `turn/interrupt` → `{}` in ≈20 ms, then `turn/completed` status `interrupted`; the reasoning item that was open never gets `item/completed` and is not kept in history; Codex closes the provider stream ("Client disconnected", `userStopped`) |
| O-2 stop with live turn and pending request; restart; resume | observed (stdin close and SIGKILL) | Pending approval **not re-raised** and no resolution sent; history shows the turn `interrupted` after both stops (indistinguishable by status); command item absent; a graceful stop writes "The user interrupted the previous turn on purpose" into history; resume starts no model call |
| O-3 supplier resolves a request first | observed (provoked by `turn/interrupt`) | `turn/completed` (`interrupted`) then `serverRequest/resolved {requestId}` with no client answer; a late client answer is silently ignored; the command item never completes and is not in history. Also: answering `cancel` declines **and** interrupts the turn |
| O-4 delegation (`experimentalApi`) | **not provoked** on the stock pairing; **observed via an OBS-2 adapter** | Codex sends delegation tools only inside a Responses `namespace` tool (`multi_agent_v1`; `collaboration` under `multi_agent_v2`) and LM Studio 0.4.16 drops `namespace` tools, so a local model never sees `spawn_agent`; no setting flattens them (`tool_namespace` must not be empty). Through a loopback adapter that flattens the namespace and restores it in the response: `collabAgentToolCall` items (`spawnAgent`, `sendInput`, `wait`) on the parent; child notifications on the same connection with the child's threadId; no `thread/started` for the child; child readable by `thread/read` (`parentThreadId`, `agentRole`, `agentNickname`, `source.subAgent`); children absent from `thread/list`, present in `thread/loaded/list` |
| O-4a native child role | observed via the adapter | `agents.<role>.description` + `config_file` honoured: `spawn_agent` gains `agent_type` listing the role (with built-ins `default`, `explorer`, `worker`); `Thread.agentRole` = the role; the child's developer text is the role file's `developer_instructions`, **replacing** the parent's; the child has no delegation tools at default depth. The 9B model did not follow the role line |
| O-4b task guidance against delegation | observed via the adapter | With "You are a TASK agent; you do not delegate", the model still spawned a sub-agent; the spawn, send and wait were recorded and shown |
| O-5 resume with changed `developerInstructions` | observed | Accepted and **silently ignored** on a loaded thread and on one loaded by the resume; the response reports nothing about guidance in effect; the rollout keeps no trace. Supplementary O-5b: `turn/start` `collaborationMode.settings.developer_instructions` is applied, **added** to the thread's own text |
| O-6 K-1 mechanism | observed (credential-free) | A symlinked `config.toml` (live share; layer named by B's path) or `-c` launch overrides (`sessionFlags` layer; a copy) give home B A's configuration with B's own empty authentication (`account/read` null); `--profile` is refused for `app-server`; a shared home with `cli_auth_credentials_store` `ephemeral`/`keyring` runs, but separation cannot be judged without a credential. Default store is `file` |
| O-7 start-up traffic | observed | `[features] plugins = false` stops both start-up connections (chatgpt.com featured plugins, 401; github.com plugin repository, including a cold home's fetch). `remote_plugin`, `apps`, `remote_control` (feature `removed`) do not. No configuration key stops the remote-control loop; only `CODEX_INTERNAL_APP_SERVER_REMOTE_CONTROL_DISABLED=1` does, and without sign-in that loop opened no socket |
| O-8 plan mode | observed | A `plan` item streamed by `item/plan/delta`; no `turn/plan/updated`; no agentMessage; plan mode **persists** on a later turn without `collaborationMode`; the thread's developer text is still sent beside the plan-mode text (role line not visibly applied by this model). Gating flags: delegation `multi_agent` (stable, on) / `multi_agent_v2` (stable, off); plan mode none in use (`collaboration_modes` listed `removed`); neither shows in `config/read` |

## Stops and deviations

- **S-9 hit** at 20:17:52 UTC in O-4a (one sample at level 4 while parent and child predicted together at parallel 4). The scenario stopped; its turn had already completed. The model was reloaded with parallel 1 and O-4b and O-8 ran with continuous sampling (no recurrence). HELP_HUMAN may judge whether continuing after S-9 was within the brief.
- D-1: one level-4 sample right after the first model load, before any Codex process.
- D-2: O-4/O-4a/O-4b used a harness adapter (labelled in the record, §6.2).
- O-6 M3 refused at launch by Codex (that case's result).
- No other stop: S-1…S-8, S-10, S-11 not hit (details in the record §12).

## Network destinations seen

| From | To | When |
|---|---|---|
| Codex | 2606:4700:4408::…:443 (Cloudflare; chatgpt.com by inference from Codex's log: `GET https://chatgpt.com/backend-api/plugins/featured?platform=codex` → 401) | start-up, before any thread; stopped by `plugins = false` |
| `git-remote-https` child of Codex | 2604:5580:21::…:443 (`https://github.com/openai/plugins.git`, `ls-remote`) | start-up; stopped by `plugins = false` |
| Codex | loopback 127.0.0.1:1234 (LM Studio), :12340/:12341/:12342 (OBS-2 taps) | turns only |
| LM Studio's own `lmlink-connector` (not Codex) | several hosts, as before this node | throughout |

No non-loopback socket from the Codex process group during any turn. Codex's log names `https://chatgpt.com/backend-api/` for the remote-control loop, which opened no socket without sign-in.

## For the D nodes and node F (pointers, not edits)

- DEL-01-02 (D1): O-2 (no re-raise; `interrupted` after quit and kill; the history marker), O-3 (`resolved-by-supplier` provoked by interrupt; late answer ignored), O-1.
- DEL-01-03 (D2): O-4 (namespace delivery; child items/notifications; no `thread/started`; `thread/list` vs `thread/loaded/list`), O-4b, O-8 (plan item, persistence; no checklist).
- DEL-01-04 (D3): O-3 and `cancel` = decline + interrupt; O-2 no re-raise.
- DEL-01-05 (D4): O-6 (symlink or `-c`; no profile path), O-7 (which setting stops which connection; remote-control loop), K-2 needs no second home for configuration (inference from O-6).
- DEL-02-04 (D6): O-5 (resume override ignored; O-5b per-turn lever), O-4a (child roles via `agents.<role>`; role guidance replaces the parent's), O-4b (K-10 "stated, not enforced" confirmed).
- HOSTING (node F): P-15 now observed (ignored); H11 (a `git` child may outlive a quick stop); L-4/U-18 per O-7; the time zone and installation id reach the provider.

## Files written

| File | sha256 |
|---|---|
| `PKG-01_Native App and third-party harness integration/1_Working/DEL-01-01_Stock Codex hosting and supplier contract/Design/OBS_2_0.158.0.md` | `61cc34ffb811eb270542042ce4cfdc195efb0c5be4b89dbbe73eb9b99e104ac0` |
| `…/Design/prototype/obs2/obs2_harness.py` | `589a9d703a73e60776ec7983fb81112cc83fb25242578584e59e64752f7e5ad7` |
| `…/Design/prototype/obs2/obs2_provider_tap.py` | `b316815fc1cb9c5f689b005fe984572a8c7ccda7d2e5d4dcedcbf5e99b68d1ff` |
| `_Coordination/AgentRuns/APP-V4-DESIGN-PASS-3-20261001/D/OBS-2.md` (this file) | reported in the hand-back |
| scratch (not committed): `$TMPDIR/chirality-obs2-0.158.0/` (25 homes, logs; raw-log hashes in the record §15) | — |

## UNRESOLVED

As in the record: a local server that accepts `namespace` tools (delegation for local models); interrupt during a streaming agentMessage; remote-control and featured-plugins behaviour when signed in; O-6 M4/M5 with a credential; writes through a symlinked `config.toml`; collaborationMode precedence versus model adherence.
