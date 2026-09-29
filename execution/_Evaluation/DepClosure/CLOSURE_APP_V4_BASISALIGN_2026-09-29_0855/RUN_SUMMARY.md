# Run summary

RUN_STATUS = WARNINGS
CLOSURE_STATUS = BLOCKER relative to the raw acyclic production-order objective (six characterized SCCs, membership unchanged)
COVERAGE = PASS (no schema, orphan, outside-scope, isolated, declaration or ID defect)

- **Snapshot:** `projects/chirality-app-v4/execution/_Evaluation/DepClosure/CLOSURE_APP_V4_BASISALIGN_2026-09-29_0855`. `_Evaluation/DepClosure/_LATEST.md` moved to it (observation pointer only).
- **Basis:** `b585e5ebe`, clean tree. 130-entry manifest `6d1021f1…93250`. 41 accepted units, no exemptions, FULL_GRAPH.
- **Analyzer:** `tools/coordination/analyze_dep_closure.py` (sha256 `2b8de3cb…a9adc`), one run, COMPLETE, exit 0, subject FAIL.
- **Counts:** 822 rows (355 ANCHOR, 467 EXECUTION rows of which 462 ACTIVE and 5 RETIRED). 198 arcs over 41 nodes (+37 from 161, 0 removed). 6 SCCs, sizes 2/13/2/3/2/2, identical member sets. 22 bidirectional pairs (+8, all inside SCC-002). 3 hubs: DEL-04-03 (27), DEL-02-03 (20), DEL-04-01 (20).
- **Checks:** schema PASS (41/41); orphans PASS; isolated PASS; ID format PASS; misplaced fields PASS; declared disagreements PASS; anchor coverage PASS (41/41); circular dependencies BLOCKER; hubs WARNING; bidirectional INFO; accepted-DAG currency WARNING (INCOMPLETE: pointer has no `Latest:` line).
- **Supplemental:** `validate_decomposition_registers.py --families SCH,EVQ,DRB --strict`, exit 0, 0 errors, 0 warnings.
- **Next:** the SCC set is unchanged, so CASE-002 takes the new held arcs as evidence and no case opens or closes. Currency is decided by the `project-dag` currency audit. No register repair is prescribed.
