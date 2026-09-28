# Quality and coverage

RUN_STATUS = WARNINGS. Analyzer process COMPLETE, exit 0; subject FAIL due to SCCs.

- Inventory: `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/Deliverables.csv`; 41 unique accepted units = 41 live workspace folders; no exemptions, missing folders or extra folders. All 41 local modes FULL_GRAPH.
- Basis: all 130 manifest entries verified against working bytes and `c1038ae5ac5c23a30ea7d3b516cd9033cb47f77b`. All 41 SoWs match extractor dispatch hashes. All 41 declaration/mode prefixes exactly match pre-extraction `ddd721a90ade401d452d102e6e40d1ffdae654eb`; zero actual declared entries, additions, disagreements or unread declarations.
- CSV: 41/41 readable and canonical v3.1 schema-valid; 758 logical data rows, 355 active anchors, 402 active execution, one retired execution. The analyzer's execution_rows=403 includes the retired row; active filtering excludes it from topology.
- Exactly one correct parent anchor per unit. Every active scope/objective anchor target set matches the sealed canonical row. Optional TargetPackageID omissions on WBS_NODE anchors do not impair parent identity.
- SCH/EVQ/DRB strict: zero errors/warnings; 758 evidence paths resolve locally, no multi-form ambiguity. Every one of 758 quotes occurs verbatim in its local SoW. File resolution/quote existence alone do not warrant production semantics.
- Local topology: 195 active deliverable rows deduplicate to 155 arcs over 41 nodes; no orphan, outside-scope, invalid direction/ID, misplaced target field, normalization or isolated-node finding. Seven SCCs contain 22 nodes and 37 distinct internal arcs represented by 48 rows. Thirteen bidirectional pairs; one degree-20 hub DEL-04-03.
- Seven representative cycles returned under MAX_CYCLES=200, not an exhaustive simple-cycle enumeration. Full nontrivial SCC membership is in Evidence/scc_summary.csv and the report. Nineteen other nodes are outside nontrivial SCCs; no implied readiness.
- Non-topological inputs: 143 EXTERNAL, 26 DOCUMENT, 21 PACKAGE, 17 UNKNOWN = 207 active rows. Nine package rows have named opposite-end local support, sometimes partial; 12 have none. The report inventories all 21 and all 17 unknowns.
- Satisfaction: 278 TBD and 124 PENDING active execution rows; none SATISFIED. All 195 deliverable-target rows use INITIALIZED as checked-contract maturity only; all 207 other active execution rows retain TBD maturity. Actual required artifacts/decisions/witnesses/release/adoption remain unproved.

## Examination limits

The semantic examination covered all 48 intra-SCC rows against actual source clauses, every UNKNOWN source clause, package rows/opposite-end named contributions and varied consequential human/provider/witness/adoption inputs. No concrete source-fidelity defect was established. This is a bounded positive finding, not proof that all 402 rows exhaust every implied production obligation. Source texts were treated as the settled basis, not re-authored or broadly re-audited against the PRD/decomposition. Provider implementation, operational capability, actual acts and current external delivery were not tested.

The source-fidelity check preserves the distinction between a runtime behavior rule and an actual production/verification input. Retired DEP-02-02-019 is retained as history and excluded from active topology. Sampled actual-human witness inputs have positive local verification requirements, not just owner/exclusion names.

No accepted DAG pointer is present; no currency PASS is invented. FULL_GRAPH is the selected tracking posture, not proof of fully allocated deliverable-level production coverage. SCC interpretation and material non-topological uncertainty must remain visible at the manager's concrete basis checkpoint.

## Reproduction and integrity

Tool_Run.json contains exact arguments, interpreter, tool/support hashes, 82 analyzer-input hashes, all 130 sealed source hashes, supplemental context and check methods/results. Evidence/register_validation.json records the independent canonical/schema checks. The source manifest was verified again while publishing the snapshot. No local source, register, index, status, accepted graph or Git state was mutated by this TASK.
