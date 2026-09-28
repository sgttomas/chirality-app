# DAG-001 — proposed App v4 production-order basis

**Working preparation; checkpoint1 not presented or confirmed. No accepted DAG exists.** Trigger INITIAL; predecessor none. WORKING_ITEMS owns this preparation under the approved INITIAL route. This is one project's graph; it does not govern provider or sibling-project work.

## Proposed objective and semantics

Support production order and route selection for the accepted App v4 Deliverables by identifying each required contribution, its supplying/receiving responsibility and the part of the consumer's work that needs it. The graph is not a schedule, implementation authorization, product-readiness assessment or 30% decision.

Default edge meaning: the consumer requires the supplier's stated contribution, at the stated maturity, before the stated part of its work. Default INITIALIZED threshold concerns checked contract maturity only. Actual artifact, decision, host/provider response, qualification, release/adoption and witness inputs retain their own conditions and evidence; they are not supplied by that lifecycle value. Runtime behavior requirements alone are not production inputs. Candidate/held relationships do not supply missing input or make affected work ready.

Canonical arcs read **consumer → supplier (depends on)**. UPSTREAM is From→Target; DOWNSTREAM is Target→From. Any rendered production-order view will state supplier-before-consumer orientation. A whole Deliverable need not be finished before every unrelated part of another can begin; the row's actual required contribution and point of need govern the stated dependency.

## Inventory and standing

FULL_GRAPH is the owner's approved tracking mode; intended completeness is FULL for the selected semantics. Missing/invalid evidence or unresolved interpretation will be reported as limitations, not hidden by the intended label. The inventory is the immutable Group3 canonical Deliverables.csv, resolved through `execution/_Decomposition/checkpoint_snapshots/_LATEST_ACCEPTED.md`:11 Packages,41 Deliverables,262 scope IDs unchanged. There are no declared exemptions. The pre-extraction41-member inventory and local paths were fixed independently of dependency files in committed setup WORK_ITEMS.csv/INTEGRATION_INPUTS.json atddd721a90. Dependency availability does not select the nodes. A final DeliverableNodes.csv will retain all41, including isolates, with actual register states.

Case home: `execution/_DAG/cases/`. No SCC ruling or case has yet been made. No `_DAG/_LATEST.md` acceptance pointer is created during preparation.

## Proposed selection rules

Use selected `chirality-root:bundled:workflow:project-dag` default SR-1…SR-7, subject to the actual checkpoint1 decision:

1. Read every included unit's register at the frozen evidence manifest.
2. Admit only ACTIVE EXECUTION rows with canonical direction and a target Deliverable in this inventory into topology. Preserve external/document/package/unknown constraints and contributions as explicitly accounted non-topological inputs; exclusion from topology supplies no input or allocation decision.
3. Select all canonical dependency types. No type exclusion is proposed merely to remove a cycle.
4. Apply only actual recorded human cut/merge rulings. None exists now.
5. No extra confirmation-hold rule is proposed at this preparation point; source uncertainties/coverage limits remain explicit for checkpoint1.
6. One representative per ordered arc: consumer UPSTREAM, then DECLARED before EXTRACTED, then lowest dependency ID. Keep every mirror/same-arc row accounted and preserve any different actual contribution/condition when assessing readiness; selecting a representative does not delete other obligations.
7. Hold unresolved intra-SCC arcs and self-loops in the non-gating candidate layer, with actual case/evidence and affected work explained. Do not arbitrarily remove a subset to obtain an acyclic picture. A held edge means its input is still absent/unresolved for that part of the work.

## Evidence and next actual checkpoint

All41 local extractions have returned. Manager preflight reports758 rows:355 active anchors,402 active execution rows and one retired extraction. All41 source SoWs/statuses and human-owned declaration sections remain unchanged; XRG/EVQ/DRB strict passes with zero errors/warnings. Every execution input remains TBD or PENDING, with none claimed satisfied. DeliverableNodes.csv freezes the complete41-node inventory with PRESENT/FULL_GRAPH states; SOURCE_MANIFEST.sha256 binds the settled local registers/indexes/source SoWs and accepted inventory/coordination basis. These checks are not independent closure or proof of semantic source support.

Final source Git revision and independent closure snapshot/SCC findings remain pending. No assembled or accepted edge files, topological waves or dependency-based readiness verdict exist. Source-fidelity and closure will examine real reciprocal contributions, non-topological inputs and remaining unknowns before this basis is presented.

Checkpoint1 will present the objective/semantics/rules, inventory/exemptions, actual coverage limits and each SCC or bidirectional relationship with a concrete proposed treatment. The human confirms or adjusts that basis and any ready cut/merge. Subsequent assembly, canonical strict audit and separate independent review precede checkpoint2's actual version decision. Graph acceptance remains separate from lifecycle, dependency fulfilment, lifted holds, project implementation and the30% gate.
