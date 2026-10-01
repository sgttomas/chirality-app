# H — LOOP's four panel-needs gaps and current pins (return)

Node H, Type 2 TASK (Claude Code subagent, Claude Opus 5.5), dispatched by
HELP_HUMAN; no delegation. Written 2026-09-30 (local; finished about
2026-10-01 04:40 UTC). Working tree on `e4fd4f9a28` (clean at start).
Read-only git; no network; no install; no commit. Scratch: `$TMPDIR/h/`.

**Inputs read** (sha256 at this node): `BRIEFS.md` `bbc0e953…f7ee`
("Common rules", "Wave B" common rules, "H"); `closeout/G.md` `57d9f83a…0ec1`
(§2 PG-1…PG-4, §7 stale pins); `R15_RESOLUTIONS.md` `5f63689a…fd22` (R15-1);
`R16_RESOLUTIONS.md` `55444aa1…70ee`; `WAVE_B/B8.md` `e02a8e4b…7d54` §3 (pin
script). LOOP was read by section: header, change table, §1, §2.1, §2.3
(whole, with E-1…E-8), §3–§3.2, §4.1's OBS-1 source, §10 (whole), Findings
G-4, G-10…G-15, UNRESOLVED, Verification cases. PANEL: header, change
table, §3.9–§3.11, F-1, F-13, UNRESOLVED, VCs, prototype README. RS: §4 R1,
§13.3, §13.3.1, change table, `RS_RECORD.schema.json` `runOpened`. EXEC's
`checkpoint-record-entries.schema.json` (`checkpointListed`,
`declarationFinding`). HOSTING, GUIDE, RELAY and CA: headers, change tables
and every line naming `OBS_1_0.158.0.md` or `HANDOFF_SWBPIPE_DOMAINS.md`.
That is less than the Wave B rule "read each file whole"; reviewers should
know it.

## 1. PG-1…PG-4: what was done and where

All new structures are **PROPOSED**; R15-1 (DERIVED) decides only PG-2's
outcome.

| Gap | Closed in | What |
|---|---|---|
| **PG-1** | LOOP §2.3 (two rows); E-8 rows point to them | "Workflow run started, with its declared checkpoints listed as guidance" (subject, actor/reporter, evidence aligned with EXEC CE-1 `checkpointListed` and RS R1 / `run_opened`); "Declaration finding" (LP-9; CE-2) |
| **PG-2** | LOOP §2.3 row "Run not started — no model selected" | Cause, the loop's configuration state at start, the message reference, the notice to choose (no default); no destination, no boundary refusal; recorded only at a run's first turn as `run_opened` `notStarted` (RS §13.3.1 already had the row) |
| **PG-3** | LOOP §2.3 event "Return input answered"; new §3.3 | Per RI-1…RI-4: when received, refusals (*no credential*, *turn not active*, *run already ended*, *selection not established*), *run not started — no model selected*; RA-1 one answer per input; RA-2 order of checks at a first turn (selection, then model setting); RA-3 answer after its result events; RA-4 delivery, not a record element; RA-5 not an act; failure rows RA-a, RA-b. §3.2 gains two rows (selection no longer resolvable at first turn; stop while interrupted) |
| **PG-4** | New LOOP §3.4 | Request: conversation, from ‹n›, optionally to ‹m›. Answer RY-1 replayed with original ordinals, "replay complete to ‹k›"; RY-2 "events ‹n›–‹j−1› not held"; RY-3 nothing to replay; RY-4 refused *conversation not known*; RY-5 repeatable; failure rows RY-a…RY-c; retention stays the host owner's (OI-013) |

Follow-on in LOOP: E-6, §3 paragraph, F-12, §10.3 cell, §10.5 (17 of 17
supplied; node-G dispositions kept), UNRESOLVED row closed (residuals
named), VC-11, G-10, new G-16, header input line, change row "H".
**PANEL:** §3.11 intro and LN-3, LN-4, LN-5, LN-16 supplier cells marked
"supplied at node H" (LN-5's member corrected to `loop_outcome`); §3.9
RI-1, RI-4, RT-d; FD-3 (request form, "not held" display); Receivers, F-13,
VC-08, header input line, row "H". No schema, example or prototype change:
`loop_outcome` already holds every value §3.3 uses. **RS:** §13.3.1 gains
three mapping rows (run started → `run_opened` + `checkpoint_listed`;
declaration finding → `declaration_finding`; return-input answer and replay
→ no kind); row "H". No kind, schema or example change.

## 2. Pins (header pins claiming current bytes): 5 updated

| File | Pin | Now | Kept as history |
|---|---|---|---|
| HOSTING header (RP-3 inputs line) | OBS_1 | `7b984b54…cc43` | `85707703…6182` "as read at RP-3" |
| GUIDE v0.5 Basis line | OBS_1 | `7b984b54…cc43` | `85707703…6182` "as read at node B8" |
| LOOP §4.1 OBS-1 source line | OBS_1 | `7b984b54…cc43` added | `85707703…` "as read at RP-4" |
| RELAY Basis line (metadata) | HANDOFF | `3f39c129…4552` | `92f6e45a…` "at node A4" |
| CA Basis line | HANDOFF | `3f39c129…4552` | `92f6e45a…` "at node A4" |

Checked: `git diff 41899194c4 HEAD` shows node G changed OBS line 359
(§B.7) plus the appended note, and added six lines to HANDOFF; nothing in
OBS Part C changed. Left as history (they state bytes of a named time):
RELAY's verbatim old Basis line (`6e7a2f04…`), its closed UNRESOLVED row
and node-A4/G change rows; CA's v0.1–v0.4 Basis line, F-8 and its node-A4
row. No file outside the run records pins the old bytes (grep).

## 3. Prototypes (2026-09-30, Python 3.13.7, `PYTHONDONTWRITEBYTECODE=1`; script `$TMPDIR/h/run_protos.sh`, run before and after the edits; outputs identical apart from scratch paths)

| Prototype | Result |
|---|---|
| LOOP `assemble_tool_calls.py` | 22/22 |
| LOOP `destination_flow.py` | all expectations held (68 RS entries, 11 request records) |
| LOOP `schema_subset.py` ×2 | VALID / INVALID as intended (exit 1 by design) |
| PANEL `panel_double.py`; `schema_subset.py` | 4/4; VALID / INVALID as intended |
| RS `run_prototype.py` | 51 PASS, 0 FAIL |
| RS `exec_to_rs.py` | 40/40 valid; 11 samples valid; none without a kind |
| CA `run_w14_rehearsals.py --out …` | ALL CHECKS HOLD; examples not rewritten (unchanged) |

## 4. RELAY span

`awk '/^## 0\./{f=1} /^## 4\./{f=0} f' RELAY_QUESTIONS_SWBPIPE.md | shasum -a 256`:
`6e399c8389dc2ad991ba8b64084fee17d44ef9e8137d184dd8eb599a66340d4d` before
and after. ANS `afb6e063…`, FACTS `733fb88a…` unchanged.

## 5. GUIDE re-pin (last)

`pins.py` copied unchanged from `$TMPDIR/c0/` (sha256 `b943319d…5423`).
Run 1 (check): 12/18 (RS, LOOP, PANEL, HOSTING, CA, RELAY differed).
Run 2 (`--write`): "match 12/18 (before write)". Run 3 (check):
**rows 18; match 18/18**.

## 6. Changed files (sha256)

| File | sha256 |
|---|---|
| DEL-05-01 `LOOP_RECEIVING_CONTRACT.md` | adcb4f5ed69195c858b7fa8a9e6cf7f143913d08087ae7497c938a36e24a6bb2 |
| DEL-05-02 `PANEL_RECEIVING_CONTRACT.md` | ed71db6b71402e30f0bb358c038c839ff0a0bd4e598555fab7b269766fcac72b |
| DEL-04-03 `RECORD_SEMANTICS.md` | b25cc90e9e252f50f30fcaed7faf230ec7bbf4689dcc2cd90deb35c7dcf7f47b |
| DEL-01-01 `HOSTING_BOUNDARY.md` | 3cf0381c42358fec4a2088ab3886e14b66d6d2020482c72e195fda068a6d78b1 |
| DEL-03-04 `HOST_INTEGRATION_GUIDE.md` | 07a5a62c4ef4536d37bbb3b7a31cf4a7237c574a211024d62d25131d6517e1b3 |
| DEL-09-06 `RELAY_QUESTIONS_SWBPIPE.md` | 71ac39b4ece59ec8fda564d9148d56c32f6ed75c78c1127e4a9cbba3d5c4dad3 |
| DEL-09-06 `CONNECTED_ACTIVITY_CONTRACT.md` | 58167f7accaf356e1e9b0d8f14c004bcc89918b06be56b15d47e52f439cfe6ce |

Each has an "H" row in its change table; no version bump. No prototype,
schema or example file changed. No ScopeOfWork, register, status, basis,
decomposition, scope-change or DAG file written.

## 7. Returned, not done

- **For DEL-04-03:** whether a host-loop first turn refused *selection not
  established* (LOOP §3.3 RA-2: no run opened, nothing written) should be
  recorded, e.g. as a further `notStarted` cause; RS's `run_opened` needs
  a resolved workflow, which is why the selection is checked first.
- **Host owner (OI-013):** how long events are held for replay (RY-2).
- **Choices this node made (PROPOSED, for V20):** selection resolved at
  receipt and again at the first turn; a stop while *interrupted* ends the
  run "person stopped"; RI-3 on a *held* run (governance phase) is not
  stated.
- **Pair check (G-4 / PANEL F-1):** node H edited LOOP and PANEL as one
  executor; the independent check stays V20's.
- **Observed, not mine:** pre-existing tables in HOSTING, GUIDE, RS, LOOP
  and PANEL history sections have rows with an uneven cell count (e.g.
  "R8-13 close — in place"); untouched.
