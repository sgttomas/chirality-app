# DAG-001 — qualified initial graph candidate

**Basis confirmed; version assembled and audited. Independent version review is a separate required record; no graph-version acceptance or 30% passage is inferred.** Trigger: INITIAL. Predecessor: none. Case home: `_DAG/cases/`. No accepted `_DAG/_LATEST.md` exists or is written by this assembly.

The owner confirmed the full required-contribution basis and six characterized unresolved groups in [BASIS_DECISION.md](BASIS_DECISION.md), decision `APP-V4-DAG-BASIS-20260928-DECISION-1`, SHA256 `5a269b838d8e923cd4b9c4911b1128244d4854e33c0f4f1c7ab061d18b2acb60`. The exact 79-member proposal is preserved at `2a461a47adee03bb868e433a73048265cc0be808`; actual decision-applied origin is `0139b067dcc49cb0c90b7a250e4dd09b19250585`. The original reader, BASIS_* records and case history remain unchanged by assembly. Current graph files are derivatives, not bytes claimed previously presented or accepted.

The owner subsequently directed, via HELP_HUMAN and WORKING_ITEMS, that approval after completion and review of the combined final package will also pass the 30% gate. Graph acceptance and the 30% effect must therefore be explicit in that future single act, without inventing a second later approval turn. This assembly supplies only the graph component; WORKING_ITEMS prepares the final readiness/handoff account. That future approval has not occurred.

## Objective, semantics and coverage

The initial project graph accounts for production-order and route-selection relationships in this App project using the full required-contribution semantics: **the consumer requires the supplier's stated contribution, at the stated maturity/condition, before the stated part of its work**. It does not require every part of a supplier to finish before any part of a consumer begins. It is neither a cross-project graph nor a schedule.

Canonical arcs are consumer → supplier (depends on): UPSTREAM is From → Target; DOWNSTREAM is Target → From. Source Direction is preserved. No quotient node or Deliverable merge is used.

TrackingMode is FULL_GRAPH; Completeness is **FULL for the selected semantics, with the explicit unresolved-input/candidate qualifications below**. The accepted Group3 register `_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/Deliverables.csv` independently supplies 41 nodes in 11 packages, no exemptions. All 41 registers are PRESENT and FULL_GRAPH. [DeliverableNodes.csv](DeliverableNodes.csv) preserves accepted identities and actual paths byte for byte; no node is removed because it has held or unsatisfied inputs.

Dependency evidence is source `85dcc17c3fda4bce82332a40f27aa9b4e849653e`; [SOURCE_MANIFEST.sha256](SOURCE_MANIFEST.sha256) SHA256 `0b60d9a2a9342acf40ac7074876115954d897a7e595ec319b223e7460e0e80a4` binds 130 unchanged files. The refreshed closure is `_Evaluation/DepClosure/CLOSURE_APP_V4_TARGETS_2026-09-27_2237`, report SHA256 `6b0b0268e79315eddb4e2595dffd30e12b5f483bd6c74e2341be03b67d2a1a11`. Its input basis matches; the prior initial observation remains historical. Closure found no schema/orphan/declaration/isolated-node defect and identified six SCCs. Its raw-acyclic BLOCKER/subject FAIL does not demand resolution before 30%.

## Selection and complete row account

The confirmed default SR-1…SR-7 are applied in order from `chirality-root:bundled:workflow:project-dag`:

1. Use included registers at the frozen manifest.
2. Select ACTIVE EXECUTION canonical local-Deliverable target rows for topology; preserve non-Deliverable inputs in exclusions.
3. Admit all canonical dependency types to selection. No type-wide exclusion applies.
4. Apply no cut or graph merge-group ruling; none exists. CP1 case tracking is not such a ruling.
5. Apply no additional confirmation hold.
6. Choose one row per canonical arc: consumer UPSTREAM, then DECLARED before EXTRACTED, then lowest DependencyID. Retain other rows as MIRROR or SAME_ARC, pointing to the exact representative.
7. Hold every intra-SCC representative in the non-gating candidate layer, citing the refreshed SCC and actual continuing case. No arbitrary subset of cycle edges is removed.

| Account | Rows / arcs |
|---|---:|
| ACTIVE EXECUTION source rows | 403 |
| Admitted: DependencyEdges.csv | 109 |
| Held: CandidateEdges.csv | 52 |
| Excluded: NOT_TOPOLOGICAL | 202 |
| Excluded: MIRROR / SAME_ARC | 38 / 2 |
| Active ANCHOR / RETIRED execution, outside denominator | 355 / 1 |

The 201 local-target rows yield 161 representative arcs. Admitted + candidate + excluded is exactly 403, with zero overlap or missing rows. All 29 core fields of all 161 representatives match source values; the complete 403-row core account is additionally preserved in [Evidence/all_execution_rows.csv](Evidence/all_execution_rows.csv). Every exclusion has source identity, disposition and rule; every mirror/same-arc row names its representative. Full per-register balance and closure comparison are in [Evidence/Accounting.md](Evidence/Accounting.md).

## Unresolved groups and actual input conditions

All six current cases are EVIDENCE_ACCUMULATING with actual CP1 basis/case tracking confirmed; no case is closed. Table counts include every source row on held arcs, including excluded duplicates. Exact node sets appear in [Evidence/SCC_Accounting.json](Evidence/SCC_Accounting.json).

| Refreshed SCC / continuing case | Nodes | Held arcs / source rows | Work/input limits and future route under existing owners |
|---|---:|---:|---|
| SCC-001 / [SCC-CASE-001](../../cases/SCC-CASE-001/Case_Datasheet.md) | 2 | 2 / 4 | Supplier and account owners identify the actual selected pin/protocol, embedding contribution and conditional native-sign-in/substitution return. Definition may proceed; affected protocol/account implementation and qualification need their named inputs and observed evidence. |
| SCC-002 / [SCC-CASE-002](../../cases/SCC-CASE-002/Case_Datasheet.md) | 13 | 40 / 46 | Existing owners identify portable/native/workspace, catalog/proposal, policy-record, role and host receiving versions and compare actual contributions. Catalog/adapter definitions can proceed; dependent finalization, conformance and live witness claims need actual versions, policy, host outcomes and person acts. Extension trace production in DEL-09-09 remains distinct from the OI-003 owner ruling. |
| SCC-003 / [SCC-CASE-003](../../cases/SCC-CASE-003/Case_Datasheet.md) | 2 | 2 / 2 | Examination owner supplies reusable support/interfaces; packaging supplies the actual candidate and package/signing/entitlement evidence. Native smoke and packaged-witness claims require actual native evidence. Support/case definition does not require completed future witnesses. Public-release-only terms remain at their separate point of need. |
| SCC-004 / [SCC-CASE-005](../../cases/SCC-CASE-005/Case_Datasheet.md) | 3 | 4 / 8 | Common source-file recovery and connector owners coordinate meanings and cases. Later PEC use requires exact qualification/release/adoption evidence; Domains reliance requires actual admitted sources/query/boundary inputs and preserves unresolved provider allocation. Neither connector's availability gates initial App or ordinary-file recovery. |
| SCC-005 / [SCC-CASE-006](../../cases/SCC-CASE-006/Case_Datasheet.md) | 2 | 2 / 3 | Undertaking/dependency owners identify applicable current control/practice records for initial graph examination. An actual accepted/current graph is needed for later graph-based selection. No already-accepted-graph bootstrap requirement or completed-controls blanket hold is introduced. |
| SCC-006 / [SCC-CASE-007](../../cases/SCC-CASE-007/Case_Datasheet.md) | 2 | 2 / 3 | Continuity and replacement-evidence owners identify current account, baseline and actual candidate dossiers. A later attributable owner disposition returns to continuity when supplied. Recording an act never performs it; favorable replacement, adoption or retirement is not inferred. |

SCC-002 actually continues CASE-002 for all 13 nodes; [CASE-004](../../cases/SCC-CASE-004/Case_Datasheet.md) remains constituent history of its original catalog/proposal inquiry. Original CASE-002 nine-member history also remains. This changes case tracking only, not scope, responsibilities, Deliverable identity or graph merge groups. Historical proposed/pending passages in preserved case bodies are governed by their current confirmed-tracking preface and actual ruling rows, rather than silently rewritten.

The candidate layer is **non-gating**. It supplies no waves, schedules, priorities, blocker queues or dispatch-readiness verdicts. An acyclic admitted layer neither resolves these SCCs nor supplies their missing contributions. Only work that actually needs a missing contribution is limited at that point. No further SCC-resolution or interface-production tranche is inserted as a pre-30% condition.

## Inputs outside topology, mirrors and findings

All 202 non-topological rows remain explicit in [Evidence/NonTopologicalInputs.csv](Evidence/NonTopologicalInputs.csv): 144 EXTERNAL, 26 DOCUMENT, 18 PACKAGE and 14 UNKNOWN. The 32 package/unknown rows retain the independent audit's row-specific A/B/C account: A is established allocation/partial support; B is a future actual candidate, source/value, contract subset or recipient instance; C is a genuine technical/allocation choice with its recorded actor. Mixed classes remain mixed. These are not 32 new human choices. Package membership is not expanded into guessed dependencies, and a known producer does not supply its actual value or contribution.

SWB/PEC/provider construction, receiving qualification/adoption, actual human decisions and source admission remain separately owned/evidenced. The known selected-pin producer remains distinct from its still-open actual value. Existing policy, catalog/schema/encoding, host/model placement/interface and Domains admission/allocation choices keep their existing points of need. INITIALIZED is checked-contract maturity only: 195 execution rows require it; 208 require TBD. Satisfaction remains 278 TBD and 125 PENDING, with none SATISFIED. No field is promoted.

[Evidence/MirrorAssessment.md](Evidence/MirrorAssessment.md) and its 40-row comparison/assessment account preserve all distinct obligations. There are 37 type differences and 13 TBD/PENDING differences, but no maturity difference. No material contradiction was identified in the bounded comparison: supplier HANDOVER and consumer prerequisite/interface/constraint commonly describe complementary contributions. In particular pin versus qualification, PEC terms versus later envelope evidence, and current-graph later-use conditions remain distinct. A representative never erases these obligations. Any contradiction found by separate review must remain a finding routed to both source owners; this account does not certify all source semantics afresh.

## Verification, reproduction and limits

The registered `tools/coordination/audit_dag.py` ran on the 161-arc admissible set, then with `--canonical --strict` on the 109-arc admitted layer, and optionally on candidates. Strict admitted exit is **0 / PASS**: zero canonical, schema, endpoint, ragged-edge, SCC, duplicate-arc or bidirectional-pair findings. Additional checks cover all 41 node rows, node identities/paths, self-loops, source field fidelity and row accounting. All 41 nodes are touched even in the admitted layer; this does not establish input availability. The raw 21-degree record-interface hub and six SCCs remain characterized source observations.

Non-strict admissible/candidate audits exit 0 because their process completed, while cyclic subjects remain FAIL against an acyclic objective. Their six exact SCC member sets agree with refreshed closure. No strictness exception is taken. No DEV-001 markdown is published or relied upon; the tool's project-specific `dev001_projection` JSON and legacy source-docstring authority wording do not govern this graph. Actual tool/script hashes and exact arguments are in [Evidence/Tool_Run.json](Evidence/Tool_Run.json) and [Evidence/ManifestCheck_Run.json](Evidence/ManifestCheck_Run.json).

From repository root, run `python3 projects/chirality-app-v4/execution/_DAG/_Candidates/DAG-001/Evidence/assemble_graph.py`, then the adjacent `describe_graph.py` for this account. These are bounded assembly reruns, not independent review. They preserve protected inputs and write only authorized candidate files. The second script records the explicit `sha256sum -c` invocation from EXECUTION_ROOT. [SOURCE_BASIS.json](SOURCE_BASIS.json) records exact source/decision/history/method/tool origins; [ASSEMBLY_RUN.md](ASSEMBLY_RUN.md) records parentage and the host-versus-brief limit.

The next action is separate independent version review and manager integration into the completed final package for the owner's combined decision. This assembly creates no accepted snapshot/pointer, readiness claim, lifecycle transition, fulfilled input, provider/product activation, release, adoption or professional act.
