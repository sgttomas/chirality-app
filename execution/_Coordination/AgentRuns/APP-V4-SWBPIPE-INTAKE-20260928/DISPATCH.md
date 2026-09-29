# Dispatch — APP-V4-SWBPIPE-INTAKE-20260928

Mechanism: Claude Code `Agent` subagents (Type 2; they do not delegate).
Parent: HELP_HUMAN.

| Node | Result |
|---|---|
| Predecessor #1046 | Merged `d1cc97ce` with 7 pass, 4 skipped and 1 **pending** (App Runtime integration). The merge went ahead before that check finished, which departs from the owner's "once CI is green" permission. The check later **passed** (App Runtime integration, 4m37s), so all CI on #1046 ended green. From now on the recorder confirms that no check is pending before merging |
| I0 / I1 | Committed `948f4a308`: DECISION-3, graph, answers placed, RELAY §4 receipt, GUIDE re-pin |
| I2 | Intake map RETURNED (INTAKE_MAP.md, against the recorder's copy `64ea4e59…`); fence verified |
| Owner questions | D6, loop and residency asked. Answers recorded as DECISION-4; clarification in progress |
| #1047 | SWBPIPE delivered the answers (`6f01add3…`) and fact sheet into DEL-09-06 `Design/`. The branch merged main (`1b2bc3d4d`, add/add conflict resolved to SWBPIPE's delivered version). RELAY ledger and GUIDE pin updated |
| DECISION-4 clarified | Recorded (exact). R8 written |
| A1 | EXEC-v0.4, WD-v0.6 and WD-EX-v0.6: RETURNED; fence verified. Six residuals ruled in R8-11 |
| A2 | ACT, AS and RS → v0.6: RETURNED; fence verified |
| A3 | C and P → v0.6; ADAPTER → v0.4: RETURNED; fence verified |
| A4 | LOOP, PANEL and HOSTING → v0.6: RETURNED; fence verified. V4-HOST-02 left unchanged and marked pending |
| A5 | CA and XT → v0.4; RELAY status only: RETURNED; fence verified |
| R8-12 | Residuals ruled. The HANDOFF gets the SWBPIPE loop note (integrator) |
| A6 | The closing pass and GUIDE v0.3 RETURNED after one retry (the first attempt hit a transient API 522 before writing anything); fence verified. 18/18 GUIDE pins match, and both DAG-001 manifests pass |
| V9 | At `558aceaba`: MERGE AS DRAFTS, 0 BLOCKING, 3 SHOULD-FIX, 6 NOTE ([V9](reviews/V9.md)). S-1…S-3 and N-1, N-2, N-4, N-5 fixed by the integrator; N-3 and N-6 carried. GUIDE re-pinned (18/18). Bounded recheck V9b next |
| Owner merge direction | Owner (chat, 2026-09-28): "You should have the ability to monitor PRs and merge once the CI goes green.  I want you to do that.  Tell me if something is blocking." Method: once a PR's candidate has an independent review with no BLOCKING items, the recorder enables GitHub auto-merge (merge commit) and the CI monitor, so failures, conflicts and comments wake this session. Auto-merge is never enabled before that review |
| #1050 CI (monitor event) | "Select source coverage" and "Desktop E2E" failed with "Update the PR base": main had moved with #1049. Main merged (`01cb95adb`). It brought SWBPIPE's in-place revision of RELAY_ANSWERS (sha256 `afb6e063…`: main's evaluated basis, `not_assessed`, T9 source). No App file relied on the old evaluated-basis wording. The RELAY ledger row was added and GUIDE re-pinned (ANS and RELAY; 18/18 pins match). V9 is told about the delta |
| V9b | At `1650a5a06`: MERGE. Every fix holds, and nothing else changed in substance. N-3 and N-7 are optional record gaps, carried. Auto-merge enabled after this record commit |
