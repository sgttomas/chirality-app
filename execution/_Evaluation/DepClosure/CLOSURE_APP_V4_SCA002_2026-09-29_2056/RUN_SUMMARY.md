# Run summary

RUN_STATUS = WARNINGS
CLOSURE_STATUS = BLOCKER relative to the raw acyclic production-order objective (six characterized SCCs, membership unchanged)
COVERAGE = PASS (no schema, orphan, outside-scope, isolated, declaration or ID defect)

- **Snapshot:** `projects/chirality-app-v4/execution/_Evaluation/DepClosure/CLOSURE_APP_V4_SCA002_2026-09-29_2056`. `_Evaluation/DepClosure/_LATEST.md` moved to it (observation pointer only).
- **Basis:** `8cd783d8d`, clean tree. 130-entry manifest `d0fc611d…40c5` (DAG-003 candidate). 41 accepted units, no exemptions, FULL_GRAPH.
- **Analyzer:** `tools/coordination/analyze_dep_closure.py` (sha256 `2b8de3cb…a9adc`), one run, COMPLETE, exit 0, subject FAIL.
- **Counts:** 826 rows (355 ANCHOR, 471 EXECUTION rows of which 465 ACTIVE and 6 RETIRED). 202 arcs over 41 nodes (+4 from 198, 0 removed). 6 SCCs, sizes 2/13/2/3/2/2, identical member sets. 24 bidirectional pairs (+2, both inside SCC-002). 4 hubs: DEL-04-03 (27), DEL-02-03 (23), DEL-02-01 (20), DEL-04-01 (20).
- **Checks:** schema PASS (41/41); orphans PASS; isolated PASS; ID format PASS; misplaced fields PASS; declared disagreements PASS; anchor coverage PASS (41/41); circular dependencies BLOCKER; hubs WARNING; bidirectional INFO; accepted-DAG currency WARNING (**DEPARTURE** against DAG-002: 4 arcs added, 0 removed, 5 deliverables `DAG pending`).
- **Supplemental:** `validate_decomposition_registers.py --families SCH,EVQ,DRB --strict`, exit 0, 0 errors, 0 warnings.
- **Next:** the SCC set is unchanged, so CASE-002 takes the four new held arcs as evidence and no case opens or closes. Currency is decided by the `project-dag` currency audit `CURRENCY_APP_V4_SCA002_2026-09-29_2057`. No register repair is prescribed.
