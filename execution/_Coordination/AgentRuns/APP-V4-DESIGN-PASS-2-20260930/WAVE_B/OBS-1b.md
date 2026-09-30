# OBS-1b — return (Type 2 TASK, 2026-09-30)

Brief: `BRIEFS.md` "OBS-1b — the command-line turn" (sha256 19e38ed8e0e3…) and `WAVE_B/OBS-1_BRIEF.md` §11 Part B (b3e7a4b6d98f…), under the owner's answer in `OWNER_DECISIONS.md` "OBS-1 follow-up after no tool call" (read at b2fa81871cbf…). The record is the appended section "OBS-1b (command-line turn)" of `PKG-01…/DEL-01-01…/Design/OBS_1_0.158.0.md`.

## Outcome

- **The command ran through Codex.** The turn used the 0.158.0 vendor binary (sha256 788a818f… as in SPIKE §3), a fresh process and thread, route R-1, LM Studio 0.4.16+2 and `qwen/qwen3.5-9b` (installed; context 24576). The model called `exec_command` with the named command. Codex raised one approval, and the harness accepted it. The command ran under the read-only sandbox and exited 0. The turn completed in 53.2 s with a one-sentence answer that was correct.
- **O-7:** the item's `command` is `/bin/zsh -lc '<cmd>'`, and `commandActions` is [{unknown, bare cmd}]. `source` is `agent` at start and **`unifiedExecStartup` at completion**. Status goes `inProgress` → `completed`, exitCode 0, durationMs 0, and `aggregatedOutput` is the JSON line. There were no output deltas. Sequence: `thread/status/changed` [waitingOnApproval] → `item/started` → `item/commandExecution/requestApproval` (id 0; its startedAtMs is 9 ms before the item's) → answer → `serverRequest/resolved` (+8 ms; U-09 observed) → the tool runs (+59 ms) → `item/completed`.
- **Approval:** `availableDecisions` = `accept`, `acceptWithExecpolicyAmendment`, `cancel`. **No `decline`** was offered. The harness answered `accept` (one request, subject exactly the named command, origin `observation-harness`).
- **A-7:** Codex carries the CLI's JSON as text: `aggregatedOutput` to the client, and to the model the JSON inside `exec_command`'s text envelope. **The local-socket probe was denied by the sandbox** even though the command was approved: `PermissionError`, the kernel logged `deny(1) network-outbound <OBS-B>/probe.sock`, and the listener saw 0 connections.
- **L-3:** function-tool calling works through Responses at this pair. MCP tools are still not delivered (`namespace` dropped).

## Stops, deviations, network

- **D-B1:** attempt 1 was refused at start-up: `approval_policy = "untrusted" is no longer supported` (stderr, 81 B). There was no thread, no turn, no model request and no IP socket. The key was removed, `untrusted` was requested on `thread/start`, and the thread's response confirmed it before the turn. A second fresh process ran the one turn.
- D-B2: the tool was run from a scratch copy with the same hash, to keep the repository path, which contains the user name, out of the model's context. D-B3: memory pressure was 2 (warn), never critical. D-B4: P-5 was not repeated.
- No stop hit. There were 0 S-2 lines, the models folder and `lms ls` were unchanged, and nothing was downloaded. During the turn the Codex group had loopback sockets to 127.0.0.1:1234 only (two model requests, the second being Codex's own continuation after the tool output). At start-up: chatgpt.com (remote-control loop, featured plugins 401) and `git ls-remote` of github.com/openai/plugins (no fetch). There was no sign-in request. This node started and stopped the LM Studio server and unloaded the model.
- The time zone again reached the model's context.

## Files written (sha256, 12-char prefix)

| File | sha256 |
|---|---|
| `DEL-01-01…/Design/OBS_1_0.158.0.md` (one section appended) | 85707703e97b |
| `DEL-01-01…/Design/prototype/obs1/obs1b_harness.py` (new) | 28c90f8b8e37 |
| `WAVE_B/OBS-1b.md` (this file) | computed by the integrator |
| Scratch (not committed): `$TMPDIR/chirality-obs1-0.158.0/obs1b/` (logs, frames a50eb050dad6, attempt1/, the scratch home with its rollout) | — |

No other repository file was edited (`obs1_harness.py` is unchanged at 0b1325547b78), and no git writes were made.
