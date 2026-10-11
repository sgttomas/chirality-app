# ST-5 and NV-04 development captures at Codex 0.160.0 (2026-10-10)

- **Standing:** development evidence. Captured with the HOSTING §9.1 method
  at stock Codex 0.160.0 by a prototype harness that stands in for the App
  side of the stdio boundary. There is no App candidate and no qualification
  pin (OI-012 stays open), so this is **not** DEL-09-02 U-SQ-6's candidate-pin
  capture and not an ST-4 counterpart at a candidate pin. It marks no
  acceptance criterion, VER item or examination result as met. The owner
  assesses reliance.
- **Supplier:** the npm platform package for macOS arm64, complete layout,
  with `codex-path` on the child's `PATH`. `codex-cli 0.160.0`; `bin/codex`
  sha256 `112fae7a5a1223e673c8a1791d32338f37df8b527ff1159bb8adac6c4dbf1b4b`.
  The match is a development assertion, not qualified distribution identity.
- **Setup:** scratch Codex home and workspace made with `mkdtemp`, never
  `~/.codex`. No sign-in, credential or download. Plugins and analytics are
  off. The model provider is a scripted loopback Responses stub
  (`prototype/st5/stub_provider.py`, 127.0.0.1 only, invented output). A
  0.25 s `lsof` watch of the Codex process group saw no non-loopback peer.
  That watch is a sample, not a guarantee; isolation rests on plugins off and
  no sign-in (HOSTING §10.2 OB2-9).
- **Files:** `prototype/st5/st5_harness.py` (method; rerun from that folder
  with `--binary`, `--codex-path`, `--out` and a scenario name).
  `prototype/st5/recordings/`:
  - `st5.recording.json`, `recorded-truncated`, sha256 `fa6add98…6717`;
  - `st5-race.recording.json`, `recorded-truncated`, sha256 `fea1bbb5…edc1`;
  - `nv04.recording.json`, `recorded`, sha256 `ae917be7…dbbc`.

  Each file carries the §9.1 metadata, the provider requests (tool names and
  input item types only), the harness events and every stdio frame. Each frame
  has its generation, direction, position and relative time. A redaction
  record lists what was replaced: personal paths, host name, `serverName`,
  installation identifier and the `userAgent` client identity. Redacted
  frames are marked, and they do not claim byte identity with the original.
  Thread and turn identifiers are generated values and are kept.

## ST-5: an answer written, then the process ends before any acknowledgment (X-09 form, RECOVERY RQ-05)

Generation 1 ran these steps:
1. `initialize`, `thread/start` (approval `on-request`, sandbox `read-only`)
   and `turn/start`.
2. The stub returned one `exec_command` call asking for escalation, for
   `mkdir` of an invented marker folder.
3. Codex sent `thread/status/changed` [`waitingOnApproval`],
   `item/started` `commandExecution` and
   `item/commandExecution/requestApproval` (id 0).
4. The harness froze the Codex process group with SIGSTOP. It then wrote the
   answer `{"decision":"accept"}` and one client request,
   `thread/turns/list`, to Codex's stdin.
5. The harness ended the group with SIGKILL while it was still frozen.
   Codex therefore could not read the answer, act on it or acknowledge it.

What was observed in generation 1:
- No `serverRequest/resolved`, no `item/completed` and no `turn/completed`.
- No response to the client request.
- Exit by signal 9, and no group member left behind.
- The marker folder was not created.

The App-side record this condition calls for is RQ-03 *answered* with write
result `written`. That is followed by RQ-05 acknowledgment *not-observed* at
the generation's close, plus E `acknowledgment_not_observed`. The client
request ends unanswered (X-09).

**Variant without the freeze (`st5-race`).** Here the answer and client
request were written and SIGKILL followed at once. In four runs, no
`serverRequest/resolved` or response arrived before the exit. Only the last
run's recording is committed; the other three are uncommitted observations
(the harness reruns them with `st5-race`). The frozen form is the method of record
because its outcome does not depend on timing.

**X-10: restart and recovery read (generation 2, same home).**
- **`thread/read` with turns:** the thread is `notLoaded`. Its one turn is
  `interrupted` and holds only the `userMessage`. The command item is absent
  from history. A `deprecationNotice` about full-history hydration was
  emitted.
- **`thread/turns/list` (`itemsView: full`):** the same single turn,
  `interrupted`.
- **`thread/loaded/list`:** empty.
- **`thread/resume`:** the thread is `idle` with the same interrupted turn.
  The response was followed by a `deprecationNotice` and
  `thread/goal/cleared`.
- **After the resume:** in a 3 s wait, no server request arrived. The approval
  was not raised again and no resolution was sent for it.
- **Exit:** graceful stdin stop, exit 0.

**Against the Design.** These results agree with RECOVERY RQ-05 and SQ-A, and
with HOSTING §6.2.1. Writing the answer is not an acknowledgment, and none
was observed before the generation closed. They also agree with what was
seen at 0.158.0 and again at 0.160.0 for an approval that was held
unanswered (OBS-2 §5.2; VERSION_ADVANCE §4.4 O-2): no re-raise and an
`interrupted` turn. The new element is that the answer was written first,
and that changed nothing in history. No difference from the Design's
assumptions was found.

Two supplier facts were seen again:
- `approval_policy = "untrusted"` in `config.toml` is still refused at start
  (81 bytes on stderr, before `initialize`), as at 0.158.0 (HOSTING §10.1
  OB-5). This was seen while developing the harness; it is an uncommitted
  observation, not a harness scenario.
- The harness therefore uses `on-request` with an escalation request.

## NV-04: the primary turn completes while a descendant is still active

**Run.** Approval was `never` and sandbox `read-only`; no feature flag was
added. At 0.160.0 Codex offered `multi_agent_v1.spawn_agent` (with
`close_agent`, `resume_agent`, `send_input` and `wait_agent`) as a
`namespace` tool on this local Responses route. The stub honoured the
namespace and made one `spawn_agent` call. It answered the parent's
follow-up at once and held the child's model response open for 8 s.

**Observed, in order:**
1. `item/started` `collabAgentToolCall` `spawnAgent`, carrying the spawn
   `prompt` and no `receiverThreadIds` yet.
2. The child's `thread/status/changed` (`idle`).
3. `item/completed` `spawnAgent`, with the child in `receiverThreadIds`.
4. The child's `turn/started`.
5. The parent's final `agentMessage` and the parent's `turn/completed`,
   about 4 ms after the child's turn began.
6. About 8 s later, the child's own `agentMessage` and `turn/completed`.

Other observations:
- No `thread/started` was sent for the child (RECOVERY §3.4).
- `thread/loaded/list` then listed both threads.
- Codex wrote 348 bytes to stderr. On a rerun these were two lines near
  shutdown, `ERROR codex_core::session: failed to record rollout items:
  thread <primary thread id> not found`.

**Against the Design.** This is NPTD NV-04's condition, recorded on the stock
supplier: the primary turn's completion says nothing about the child, which
was still active. It also bears on the native witness of 2026-10-10:
- There, on the ChatGPT route with the `collaboration` tool names, **no**
  spawn item was shown.
- Here, on the `multi_agent_v1` namespace, Codex emitted the `spawnAgent`
  item with its `prompt`.

So the absence seen in the witness belongs to that route or tool family, not
to every route. FLEET_RECORDS AS-2's input is observable on this one. Which
setting chooses the family was not read. This was one run with a scripted
model, and the child's status after the parent ended was observed only
through its own notifications.

## Remaining

- U-SQ-6 still needs this capture at the candidate's pin, on a named App
  candidate. ST-4 likewise needs an identified delegation route or a
  candidate-pin counterpart. Both stay in
  `app/examination/standalone/missing-inputs.json`.
- Not yet done: replaying the ST-5 recording on the supplier double as an EXP
  rehearsal (R23-27), and a schema-conformance pass of these frames against
  the 0.160.0 reference output (§9.3).
