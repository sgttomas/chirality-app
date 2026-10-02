# F-B — EXEC first-increment edits (design pass 3)

- Run `APP-V4-DESIGN-PASS-3-20261001`, node **F-B**. Executor: Type 2 TASK
  (Claude Opus 5.5), dispatched by HELP_HUMAN; does not delegate. Written
  2026-10-02 in the working tree at HEAD `e4e14d6ae6`.
- Brief: `BRIEFS.md` "F — first-increment edits" (sha256 `316ea29325a0d450`);
  rows `F/F0_JOINS.md` §1.2 FE-01…FE-20 and §1.14 EXEC lines
  (`e93608be1c6e3eb0`), as ruled by R17 (`b0af81bcbad9bc52`), R18
  (`abf5eee6324647ff`) and R19 (`16930ecdcead7511`); `OWNER_DECISIONS.md`
  (`ea96c55710af41c9`: DECISION-K3 revised, DECISION-L).
- Write fence kept: one Design file edited,
  `PKG-02…/DEL-02-03…/Design/EXECUTION_COMPATIBILITY.md` (EXEC-v0.6 → v0.7),
  and this return file. `checkpoint-record-entries.schema.json` was **not**
  changed (see "Coordination with F-C"). The prototype, the examples, the
  other schema, ScopeOfWork, registers, `_STATUS.md` and every other Design
  file are untouched. Read-only git; no network; no Codex or model run.
  Scratch under `$TMPDIR/f-b/` (a copy of v0.6, the rerun output, a scratch
  copy of the prototype).
- How checked: EXEC-v0.6 was read whole before editing, and its hash matched
  F0's input (`64e732d502d0b91d`). Each edit replaced an exact, once-only
  string (scripted assertion of one match each). Table rows were checked for
  column counts after the edits (0 mismatched rows, as in v0.6). The
  `multiAgentMode` and `multiAgentVersion` texts were read in the committed
  generated bundle (`codex_app_server_protocol.v2.schemas.json`
  `34f28a486d00fbd2`). Cited identifiers in the new Design files (DEF-1…DEF-7,
  §4.1 tag / look up, §8.2 custody events; NIR §5.2, §9 PD-5; AAC §1.1, §1.2,
  §4.2, §5.2, VC-AAC-04; WR §4.1–§4.4, §6 SQ-H, §7, §8; ROLE §3.1 SL-7, §5.1,
  §6.1; ACCESS §8; NPTD §7.1) were read at their v0.1 bytes; they are cited by
  v0.2 label as the brief asks, and F-E checks the section numbers.

## Rows applied

| Row | Applied as | EXEC v0.7 location |
|---|---|---|
| FE-01 | Only the person's explicit end (RECOVERY DEF-4) or the run owner's end ends an App run; interrupt, quit, Codex stop/exit, observer and connection loss never do; relaunch leaves the run interrupted. *The person* in `run_ended` means DEF-4 only; *observed end* does not occur in App runs. Follow-ons: §4.4 run-ended supplier; NG-2's *stop* path in App runs (written at the person's end with that cause); §10 | AE-7; RE-6; CE-17 and shared spellings; A-11; §4.4; NG-2; §10 |
| FE-02 | AE-6 from DEL-01-02's custody events; DEF-1, DEF-2 readings; standing from OBS-2 O-2; A-4 failure cell | AE-6; A-4 |
| FE-03 | §2.7 points to RECOVERY; run starter tags the conversation (tag / look up); consumer side of the proposed row DEL-02-03 → DEL-01-02 (F0 §3 NR-01 = D1 NR-D1-1) | §2.7; A-2 |
| FE-04 | RE-4 cites `app_restart_interruption` and the tag lookup; fallback "interruption not recovered" | RE-4; A-11 |
| FE-05 | EV-3a `agent-delegation` re-based on C-04 (`Model.multiAgentVersion`, `namespaceTools`, `features.multi_agent`), no "experimental" label (C-05); `multiAgentMode` no longer read | EV-3a; note after it |
| FE-06 | §5 closing: designed in AAC-v0.2, PROPOSED until SCA-V4-003 (SC3-01-04-1) | §5 |
| FE-07 | CAP-1 and CAP-2 gain A15; L-4 multi-entry registration and release-registered shipped entries; decline only where ACT §2.3 defines one | CAP-1; CAP-2; §8 row |
| FE-08 | CAP-3 names `aac.capture-evidence.schema.json` | CAP-3 |
| FE-09 | §2.4.4 opening per R17-7 | §2.4.4; §2; §9.2 |
| FE-10 | RC-6 cites AAC-v0.2 | RC-6 |
| FE-11 | AE-2 standing DESIGNED (AAC-v0.2); A-7 failure cell | AE-2; A-7 |
| FE-12 | §9.1 DEL-01-04 row (v0.6 text kept as history); §10; §2; §8; U-E8; CH-23 (ii), CH-31 (ii), CH-32 states; §7.4 capture row | as listed |
| FE-13 | Applied because R18-5 accepted U-NIR-5: RC-4's "person's own click" sentence | RC-4 |
| FE-14 | HR-4 with DS-1/DS-2/DS-3 (K-6; WR SP-3, SP-4) | HR-4 |
| FE-15 | §6.5 closing cites WR SQ-H; F-12 disposition updated | §6.5; F-12 |
| FE-16 | RT-6 (WR SQ-H, P-32); RT-7 (K-6, SL-2) | RT-6; RT-7 |
| FE-17 | U-E19 restated | U-E19 |
| FE-18 | §9.1 DEL-02-02 row; §9.2 own row; §10; §2 | as listed |
| FE-19 | **Conflicts with R19; R19 wins.** F0's text (DEL-02-04 composes the workflow into `developerInstructions`, cite ROLE §5.1/§6.1) is superseded by R19-1/R19-7: the workflow is a text element of the run-start turn (registered revision's exact bytes, App-written framing), composed by DEL-02-02, started by DEL-02-03, recorded per run and checked against `thread/read` (OBS-3 W-4); DEL-02-04 composes role guidance only; no skill root, no `thread/settings/update`. The part R19 leaves standing (the check receives the role in force, possibly "no role", ROLE SL-7) is applied with EXEC's reading | A-3; §6.1 *supplied*, *selected*; §2.1 (i); §2.7 run starter; §3.4 role part; §9.1 DEL-02-04 row; RT-5 |
| FE-20 | CAP-8 per C-10 (ACCESS §8 supply; RS `codexAccount` reading; no plan type); U-E8 follows. L116 is change history: left | CAP-8; U-E8; §9.1 DEL-01-05 row |
| §1.14 EXEC lines | L25 annotated (history kept); L291 and L293 (§2 table); L1773 (§8 row); L1920 (U-E8); L1800, L1825 via FE-18 | as listed |

Brief items beyond the FE rows, applied:

| Item | Applied as | Location |
|---|---|---|
| R19-2 chaining (DECISION-L L-2) | New **RE-7**: one run at a time, never nested; "End ‹A› and start ‹B›" as A's DEF-4 (PROPOSED (F-B)); agent-proposed starts need the person's confirmation (ordinary input, R17-9; a proposal is never a selection); "or it completes" read as the person's end with cause *completed* (F-37); B cites the prior run as context, inheriting nothing (SP-6 still counts acts on current content); model told at B's start (R19-7) and, with no following run, by an App-written line on the next turn (F-39); forks carry no run (R19-8). New SD-6 (run boundaries); A-1, A-2 carry the rules | RE-7; SD-6; A-1; A-2; §2.7 run end |
| K-7 | HR-3, TR-1, T-1 stand and say so | §6.5; §6.3; §2.6 |
| R19-5 | §0 "Supplier versions" paragraph | §0 |
| Verification | VC-E-17 (run end, runs in sequence) and VC-E-18 (per-run supply), not run; §7.4 row for them | Verification cases; §7.4 |
| Findings | §11.6 F-37…F-40 | §11.6 |

## Rows not applied, with reason

- None of FE-01…FE-20 is left unapplied.
- FE-19's composition by DEL-02-04 was **replaced**, not applied, because
  R19-1/R19-7 supersede R17-8 (R19 wins, as the brief says).
- FE-05 in the **prototype** (`prototype/required_tool_check.py`
  `_delegation`; two readings in `prototype/run_all.py`) is not applied: the
  prototype is outside F-B's fence (F0 §6). Returned as F-38. A scratch check
  of the v0.7 row ran (below).

## Coordination with F-C (`runEnded`, FR-01)

No change to `checkpoint-record-entries.schema.json` is needed. FR-01
changes RS §3's run-ended row to "the run ended (DEF-4)". In EXEC the
`runEnded` body keeps `stoppedBy` ∈ {`the person`, `run owner`,
`observed end`}, `cause`, `waitingArrivals`. v0.7 narrows the meaning of
*the person* to DEF-4 (CE-17 shared spellings; RE-6) and states that
*observed end* does not occur in App runs; it stays for a host loop's end
(LOOP E-8). Spellings and structure are unchanged, so RS's `$ref` resolves as
before. If F-C wants the body's `description` to cite DEF-4, that is a
wording edit to this schema and can go with the prototype update (F-38).
Two RS spellings are F-C's to choose: the relation by which run B cites the
prior run in its conversation (RE-7, "context, not a dependency of
identity"), and whether the run-end line on the next turn (F-39) is an R3
`supplied_guidance` entry like the run-start text.

## Returned for others

- **F-37** (integrator): R19-2 (a)'s "or it completes" read as the person's
  DEF-4 end with cause *completed*.
- **F-38** (the prototype's owner): update `_delegation` and the two readings
  to the v0.7 EV-3a row; the scratch variant below is a model.
- **F-39** (DEL-02-02, integrator): wording and owner of the run-end line
  told to the model when no run follows (R19-2 last bullet).
- **F-40** (DEL-02-01; U-R10): EXEC reads "no role" where compatible roles
  are declared as *unsupported* (role), shown and recorded, the person free
  to proceed; WD §4.7 may state it.

## New sha256

| File | sha256 |
|---|---|
| `PKG-02_Workflow and role portability/1_Working/DEL-02-03_Workflow execution compatibility and round-trip support/Design/EXECUTION_COMPATIBILITY.md` (EXEC-v0.7) | `9c85b60b8f34cb9aef76f791e7981da6b4b268567606ac00f7ac655bd47b69a1` |
| `…/Design/checkpoint-record-entries.schema.json` (unchanged) | `55c65bd83908bdd3aa69243cb75bbb33a17fde8075aa5b8548ba7cad94bbf8dd` |
| Previous EXEC-v0.6 | `64e732d502d0b91da00e62069be1b77b61d1e84986b3744bc117b6e67524fa38` |
| `F/F-B.md` (this file) | reported in the hand-back |

## Rerun output

**Committed prototype** (check only; nothing written in the repository):

```
cd "…/DEL-02-03_…/Design/prototype"
PYTHONDONTWRITEBYTECODE=1 python3 run_all.py
```

Run 2026-10-02T18:42:50Z, Python 3.13.7. Exit 0; 116 lines (scratch copy of
the output sha256 `d00da864e497b6f8…`). Summary:

- Required-tool check: MT-1…MT-10, MT-12…MT-18 (MT-5, MT-12, MT-17 on two
  surfaces or editions): 20 case runs, each in both phases, all `ok`; 40
  reports validate. PS-2 and PS-4 wording `ok`.
- EV-3a readings: 18 `ok`. The two `agent-delegation` readings are the v0.6
  rule (`multiAgentMode` → present; none → not established); see F-38.
- Recorder: CH-7/CH-8, CH-10, CH-20, CH-31 (i), (ii) all `ok`; recorder
  outputs validate (12, 6, 6, 8, 9).
- Committed examples: the valid report and the 12 valid recorder outputs
  validate and equal the regenerated ones; the invalid report is rejected
  (4 errors); INV-EXEC-1…7 rejected.
- Last line: `ALL CHECKS HOLD: 0 failure(s)`.

No v0.7 edit changes an MT result, a CH result, a report element or a schema,
so the unchanged prototype holding is the expected result. It does not test
the v0.7 EV-3a delegation row, RE-7 or A-3; VC-E-17 and VC-E-18 are designed
and not run.

**Scratch check of the v0.7 `agent-delegation` row** (outside the
repository: `$TMPDIR/f-b/proto/ev3a_v07_delegation_check.py`, which imports a
copy of the committed `required_tool_check.py` and replaces the HCG-A08
reading in memory). Run 2026-10-02T18:43:45Z:

```
  ok   agent-delegation  v1, namespaceTools true                          -> present
  ok   agent-delegation  v2, namespaceTools true, multi_agent unset       -> present
  ok   agent-delegation  disabled                                         -> missing (availability signal of HCG-A08 reads unavailable)
  ok   agent-delegation  v1, features.multi_agent = false                 -> missing (availability signal of HCG-A08 reads unavailable)
  ok   agent-delegation  v1, namespaceTools false                         -> not_established (provider may not receive delegation tools (namespaceTools false; OBS-2 O-4, through an adapter))
  ok   agent-delegation  multiAgentVersion null                           -> not_established (availability signal of HCG-A08 not read)
  ok   agent-delegation  v0.6 signal only (multiAgentMode on thread start) -> not_established (availability signal of HCG-A08 not read)
  ok   agent-delegation  nothing read                                     -> not_established (availability signal of HCG-A08 not read)
EV-3a v0.7 agent-delegation readings: 8 case(s), 0 failure(s)
```

## Inferences, marked

- That DEF-4 is reached through the run panel's "End run" control is read from
  NIR §5.2 (v0.1 bytes).
- RE-7's "End ‹A› and start ‹B›" offer, the *completed* cause, the run-end
  line on the next turn, the forks rule and the "no role" reading are this
  node's proposals (PROPOSED (F-B)). They are not rulings.

---

## Round 2 (2026-10-02, after the coordinator's two messages)

Inputs: `R20_RESOLUTIONS.md` (`516d0fe0d3cddb1e`); the D round-2 sections of
`D/D1.md` (`df731fa3d29dc2c6`), `D/D2.md` (`943d51407c629575`), `D/D4.md`
(`c2c7e74d91f2d121`), `D/D6.md` (`9c6044c73833b1bc`); RECOVERY-v0.2
(`c528b47627ea116c`), NPTD-v0.2 (`5cfda3ac81b3d202`). D3 and D5 round 2 were
not yet available and are not reflected. EXEC stays labelled v0.7 (edited in
place; the change table gains four rows). Fence per R20-2: EXEC and
`DEL-02-03/Design/prototype/`.

### Applied

| Item | Change in EXEC-v0.7 |
|---|---|
| D1 E-3 | §2.7: tags are ordered (`seq`), several per conversation, read with `tags of` (RECOVERY-v0.2 §4.1). Each chained run keeps its own tag. DEL-02-03 picks the current run (the run opened last with no `run_ended`) from the ordered tags and its own records; A-2's tag failure row follows |
| D1 E-4 | RE-4, A-11, AE-6: on relaunch the run current in the conversation at the end stays interrupted; earlier ended runs of that conversation are unaffected |
| D2 J-5 | EV-3a row checked against NPTD-v0.2 §7.1 (C-04 availability, read at run time, not experimental): no further change |
| D2 J-11 | SD-6, §2.7 run starter, §9.2: run markers {thread, turn, start or end, workflow, revision} handed to DEL-01-03 as a runtime value for display, no row (NPTD-v0.2 §5.7) |
| D4 FE-20 | CAP-8 already has C-10's form: no change |
| D6 FE-19 | Matches what was applied. Added to the role part: every run chained in a conversation is checked against the conversation's fixed role (L-2), and a fork has its source's role |
| R20-1 | RE-7 cites it for "End ‹A› and start ‹B›" and for completion: the App offers "End run" when the agent reports the workflow finished; the person's choice ends the run with cause `completed`. F-37 closed |
| R20-2 | Prototype: `_delegation` reads `model_multi_agent_version`, `effective_config.features.multi_agent` and `namespaceTools` per the v0.7 row; the delegation limit has its own reason text; the two `agent-delegation` readings are now `v2` + `namespaceTools` true → present and `disabled` → missing; README notes the update. F-38 closed |
| R20-3 | RE-7: the App prefixes the person's next turn with one App-written line saying the run ended (workflow and revision named), worded by DEL-02-02 in its run-start schema, recorded with the per-run supply evidence (RS spelling F-C's). F-39 closed |
| R20-4 | §3.4 role part cites it for "no role" against declared compatible roles (*unsupported*, shown and recorded, the person may proceed). F-40 closed |

Still PROPOSED (F-B), not ruled: SD-6's wording, the run starter component,
the forks bullet of RE-7 and the rest of the role-part reading beyond R20-4.

### New sha256

| File | sha256 |
|---|---|
| `…/DEL-02-03_…/Design/EXECUTION_COMPATIBILITY.md` (EXEC-v0.7, round 2) | `70120eb1987b5e5fca298eb23888fc77e50600db059dacc56a41fa3e3892a086` |
| `…/Design/prototype/required_tool_check.py` | `defa897000b5370ccdb98467669a68044ab3bde114889242c6981e58fca93569` |
| `…/Design/prototype/run_all.py` | `b770bb42d409fbf5fcd01ebde86d532cf8125b4aa6cb0c0b4b0c184f1381adc3` |
| `…/Design/prototype/README.md` | `99ed803f6ec930fc17970afe46fc100bdd6b2f5dadcd4baa5d867e4ae50f4df7` |
| `…/Design/checkpoint-record-entries.schema.json` (unchanged) | `55c65bd83908bdd3aa69243cb75bbb33a17fde8075aa5b8548ba7cad94bbf8dd` |
| `F/F-B.md` (this file) | reported in the hand-back |

The round-1 EXEC hash (`9c85b60b…`) is superseded.

### Rerun output

`PYTHONDONTWRITEBYTECODE=1 python3 run_all.py` in `prototype/`,
2026-10-02T18:55:25Z, Python 3.13.7: exit 0, 116 lines, last line
`ALL CHECKS HOLD: 0 failure(s)` (scratch copy sha256 `2e2a275737c1e529…`).
Against round 1's output the only changed line is the second
`agent-delegation` reading:

```
  ok   agent-delegation      App Codex         -> present
  ok   agent-delegation      App Codex         -> missing (availability signal of HCG-A08 reads unavailable)
```

All MT cases, the 40 reports, the other 16 EV-3a readings, the recorder
cases, the examples and INV-EXEC-1…7 are unchanged. The eight scratch
readings, run against the committed `_delegation` (outside the repository,
`$TMPDIR/f-b/proto/ev3a_committed_check.py`): 8 cases, 0 failures (v1 or v2
with `namespaceTools` true → present; `disabled` or `multi_agent = false` →
missing; `namespaceTools` false → not established with the delegation limit;
null, `multiAgentMode` alone, or nothing read → not established).
