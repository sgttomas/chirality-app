# RX — residual sweep after the V18 repairs (return)

Node RX of run `APP-V4-DESIGN-PASS-2-20260930`. Type 2 TASK (Claude Code
subagent, Claude Opus 5.5; no delegation). Date 2026-09-30 local (final rerun
2026-10-01 02:07 UTC). Working tree at `2d32215cc9`, clean at start.

**Read whole:** BRIEFS.md ("Common rules", Wave B common rules, "RP", "RX"),
R14_RESOLUTIONS.md (binding), R13_RESOLUTIONS.md, WAVE_B/RP-1.md…RP-4.md.
I read the comparisons in `comparisons/` where an item needed the underlying
finding (V18-1 m-11, m-12; V18-2 m-4, m-9, m-12; V18-3 m-4; V18-4 J10). For
each item I grepped the named file's current text and read the passage.
SWBPIPE's files and RELAY were not opened. PIN_SPIKE, OBS_1 and
`prototype/obs1/` are byte-unchanged: `git diff --quiet` on them succeeds.

**Rules kept:**
- No version bump. Each changed Design file has "RX" rows in its Wave B change table.
- No git writes, no network, no install.
- Scratch was under `$TMPDIR/rx/`.
- No ScopeOfWork, register, status, basis, DAG or scope-change file was touched.

## 1. Residual items

The sources are the "what other files must now say" lists: RP-1 §4, RP-2 §3,
RP-3 §3 and RP-4 §3.

| # | Source | Target and what it must say | Result | Location |
|---|---|---|---|---|
| 1 | RP-1 | LOOP §2.3 and E-4 cite RS §13.3.1 | **Fixed** | LOOP E-4, E-8 |
| 2 | RP-1 | LOOP: interruption and recovery recorded as `observation_lost` / `observation_recovered` | **Fixed**. It was implied through E-8, which maps them to CE-13/CE-14 and then to RS §13.3; the row now states it | LOOP E-8 |
| 3 | RP-1 | LOOP F-10 cites RS W-1 | Said already | LOOP §3.1 F-10 |
| 4 | RP-1 | LOOP loop-side refusals use the R7 outcomes | Said already | LOOP §7 (record report, item 3); E-8 closing paragraph |
| 5 | RP-1, RP-4 | CA: regenerate `w14-result-record.example.valid.json` | **Fixed** with `--write-examples`. Only the pinned sha256 of EXEC `run_all.py` changed. The invalid example, which is derived from the valid one, changed the same way | CA examples |
| 6 | RP-1 | CA act citations use `rec:` identifiers | Said already. The recorder-double act is `rec:app:run-14:A4-T2`; `ACT-2` is SH-1's own host record identity | CA valid example |
| 7 | RP-1 | CA evidence limits use RS spelling | Said already. RP-4 did this; the CA check "every evidence limit is an RS R11 label" holds | CA §8.4 |
| 8 | RP-1 | WD tokens for capturing surface and reached-when are canonical | Said already | WD §3.6 (V18-2 m-5 row) |
| 9 | RP-1 | WD §4.3.4 reads "replaced by next arrival" | **Fixed** | WD §4.3.4; §4.3.7 MX-6 |
| 10 | RP-1 | P: `act_ref.captured_at`; when absent, write "not supplied by host" | Said already | P §9; `proposal_state.schema.json` description |
| 11 | RP-1 | HOSTING §6.8 names the required-tool check's catalog read as App-origin | **Fixed**. The carrying surface is left open; a `mcpServer/tool/call` use stays under U-24, because the existing texts do not choose one | HOSTING §6.8 (new paragraph) |
| 12 | RP-1 | HOSTING LT-12 receivers include DEL-03-03 and DEL-02-03 | Said already | HOSTING LT-12 |
| 13 | RP-1 | CA and XT read ADAPTER's `exec_event` as CE-n | Said already. Neither file nor either prototype reads `exec_event`; grep finds nothing | — |
| 14 | RP-1 | GUIDE cites the RS kinds and the EXEC-body arrangement | **Returned to B8**. GUIDE is still at its Wave A pins, and B8, the planned GUIDE node, re-pins last | — |
| 15 | RP-2 | ADAPTER RD-2, OM-9 and UNRESOLVED state R13-1 as ruled | Said already | ADAPTER §4.3 RD-2; §4.6 OM-9; UNRESOLVED |
| 16 | RP-2 | ADAPTER CO-4 takes cause and time from P's `item_left` | **Fixed** | ADAPTER §7.7 CO-4 |
| 17 | RP-2 | ADAPTER CO-2 and CO-3 map `captured_at` | Said already | CO-2; `observe_map.py` |
| 18 | RP-2 | RS §5: C §4.1's destination rows go under R15 | Said already | RS §5 |
| 19 | RP-2 | RS R11 adopts "de-duplication scope exceeded" | Said already | RS §4 R11; §5 |
| 20 | RP-2 | EXEC `item_decision` *left* carries P's cause and time | **Fixed**. Optional `leftTime` was added | EXEC §2.4.2 CE-7; schema |
| 21 | RP-2 | EXEC cites P-v0.8 §4.3, §13 and the schema elements | **Fixed**. §4.3 was already cited; the fix adds §13 and the elements `item_left` and `captured_at` | EXEC §9.1 |
| 22–24 | RP-2 | WD uses `applied`; cites P §13 and `item_left`; carries the tuple `derived_from` | Said already | WD §3.6, §4.3.6, §4.3.7, §8; `$defs/workflow_identity` |
| 25–26 | RP-2 | LOOP names CI-4 and the held edition; takes P's two v0.8 rows | Said already | LOOP §2.2, TL-2, §6.2 |
| 27 | RP-2 | PANEL takes P §13's additions | Said already | PANEL §3.3 |
| 28 | RP-2 | CA F-26 and XT F-25 are answered by C §10.8 | **Fixed** | CA §12 F-26; XT §9 F-25 |
| 29 | RP-2 | The "21 of 21" count stays true | Said already. Neither CA nor XT cites a count | — |
| 30 | RP-3 | EXEC EV-3 reads WD HC-7 and HOSTING §8.4 | Said already | EXEC EV-3 |
| 31 | RP-3 | EXEC AW-1, AW-8 and U-E26 cite HOSTING §10.1 OB-1 | **Fixed**. AW-8 already takes AW-1's reason | EXEC AW-1; U-E26 |
| 32 | RP-3 | EXEC V18-2 m-1, m-3, m-4, m-5, m-12 | m-1, m-3, m-5, m-12 and the fixtures were said already. **Fixed:** §9.1's WD row now reads WD-v0.8 and WD-EX-v0.8, and F-33 is marked closed there | EXEC §9.1 |
| 33 | RP-3 | EXEC: `derived_from` is a tuple | **Fixed** | `compatibility-report.schema.json` |
| 34 | RP-3 | ADAPTER cites HOSTING §10.1 OB-1, OB-2, OB-3, OB-6 and OB-10 | **Fixed** | ADAPTER §3.5; OM-1; OC-3; OC-5 |
| 35–36 | RP-3 | RS: origin `host` with source root required; U-27 thread scope | Said already | RS R2, R5; schema |
| 37 | RP-3 | LOOP and PANEL: V18-2 m-6, m-7, m-8 | Said already | LOOP §2.4; PANEL §3.2 |
| 38 | RP-3 | P: nothing further | Said already | — |
| 39–40 | RP-4 | RS §13.3 CE mapping; R11 label text | Said already | RS §13.3; §4 R11 |
| 41 | RP-4 | RS `boundary_refusal` reasons "no credential" and "no model chosen" | "No credential" was said already. **"No model chosen" is returned**: see §2. LOOP F-2 now states both halves | RS schema; LOOP F-2 |
| 42 | RP-4 | RS R15 counts each request *raised* (an already-allowed target raises none) | **Fixed** | RS §4 R15 |
| 43–44 | RP-4 | RS does not record E-6; RS R7 has the loop-side values | Said already | RS §13.3.1; §5 |
| 45 | RP-4 | P §13 "Provide to DEL-05-02" | Said already | P §13 |
| 46 | RP-4 (V18-2 m-9) | PANEL and RS type `derived_from` as a tuple | **Fixed** in PANEL and RS (`run_opened`), and in P's `proposal.schema.json` for consistency. RS A15 `relations.derivedFrom` names a draft and stays a reference | three schemas |
| 47 | RP-4 | Rerun W14 and XT with `--write-examples` | CA is #5. XT holds without regeneration | — |

**Counts:** 30 said already, 15 fixed, 2 returned.

## 2. Returned

- **#41.** LOOP F-2 records the unconfigured case ("no model chosen") as `boundary_refusal`. RS has no such reason, and `boundary_refusal` requires a `destination`, which an unconfigured setting does not have. LOOP MS-02 gives the evidence for that case as "observed absence". Choosing between an RS reason with an optional destination and recording nothing needs a ruling.
- **#14.** The GUIDE uptake belongs to node B8.

## 3. Prototype reruns

Final rerun on 2026-10-01 02:07 UTC with Python 3.13.7 and `PYTHONDONTWRITEBYTECODE=1`. The script is `$TMPDIR/rx/verify.sh`, and the outputs are in `$TMPDIR/rx/final/`. Every result is as expected.

| Prototype | Result |
|---|---|
| HOSTING `run_cases.py` | TOTAL 35, FAIL 0 |
| WD `wdproto.py selftest` | 62 of 62 |
| EXEC `run_all.py` | ALL CHECKS HOLD |
| SH-1 `run_fixture.py --out` | 22 of 22 |
| `validate_all.py --run` | all checks passed |
| ADAPTER `observe_map.py --run` | all checks passed |
| P `proposal_states.py --check` | all checks passed |
| ACT, AS | all expectations held |
| RS `run_prototype.py` | 49 PASS |
| RS `exec_to_rs.py` | 12 of 12 and 40 of 40 valid; none without a kind |
| LOOP `assemble_tool_calls.py` | 22 of 22 |
| LOOP `destination_flow.py` | all held |
| PANEL `panel_double.py` | 4 of 4 |
| LOOP and PANEL `schema_subset.py` | valid examples VALID and invalid examples INVALID; exit 1 is the tool's code for an invalid instance |
| CA `run_w14_rehearsals.py` | ALL CHECKS HOLD. "Valid example equals the regenerated W14-05" now **PASS**; it failed at baseline |
| XT `run_xt_suite.py` | ALL CHECKS HOLD |

Before editing, the same rerun matched this, except for that one CA failure.

Separate scratch checks (`$TMPDIR/rx/neg/`):

- A string `derived_from` is refused by EXEC, PANEL, P and RS; a tuple is accepted; PANEL `null` is accepted.
- RS `item_decision` *left* with `leftCause` and `leftTime` is valid through EXEC's body.
- An empty `leftTime` is refused.

## 4. Changed files (sha256, 12-character prefix)

| File | sha256 |
|---|---|
| DEL-01-01 HOSTING_BOUNDARY.md | 11ffae515234 |
| DEL-02-01 WORKFLOW_DECLARATION.md | 6f3a114d0cf9 |
| DEL-02-03 EXECUTION_COMPATIBILITY.md | b82dba72cd7d |
| DEL-02-03 checkpoint-record-entries.schema.json | 55c65bd83908 |
| DEL-02-03 compatibility-report.schema.json | 8e2bf4a25742 |
| DEL-03-02 PROPOSAL_LIFECYCLE_AND_OUTCOMES.md | f0eef087d187 |
| DEL-03-02 proposal.schema.json | 2c81bab4a725 |
| DEL-03-03 ADAPTER_ENABLEMENT_AND_RECEIVING.md | a9e7d0a26f38 |
| DEL-04-03 RECORD_SEMANTICS.md | f966134c09b5 |
| DEL-04-03 RS_RECORD.schema.json | 7edd2adcde48 |
| DEL-05-01 LOOP_RECEIVING_CONTRACT.md | 1962f7d0c737 |
| DEL-05-02 PANEL_RECEIVING_CONTRACT.md | 3bd6c38f9e49 |
| DEL-05-02 PANEL_RETURN_INPUT.schema.json | 47d9acfa760f |
| DEL-09-06 CONNECTED_ACTIVITY_CONTRACT.md | 11d1302c5e4f |
| DEL-09-06 w14-result-record.example.invalid.json | aa5ab483dce3 |
| DEL-09-06 w14-result-record.example.valid.json | bce18b1edeb6 |
| DEL-09-09 EXTERNAL_TRACE_CASES.md | 6f4bea46c1c3 |

`git status --short` shows only these 17 files and this return file. This file cannot carry its own hash.
