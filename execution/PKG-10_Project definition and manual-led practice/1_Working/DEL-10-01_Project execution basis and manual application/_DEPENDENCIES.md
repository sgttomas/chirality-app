# Dependencies: DEL-10-01 Project execution basis and manual application

## Dependency Tracking Mode
- **Mode:** FULL_GRAPH
- **Register:** the declared sections of this file together with Dependencies.csv (schema v3.1) when present (docs/SPEC.md §5.3)
- **Notes:** `projects/chirality-app-v4/execution/_Coordination/_COORDINATION.md`; no individual human-declared edge yet. Accepted interface descriptions are sources for later extraction, not declarations inferred by scaffolding.

---

## Declared Upstream (I need these before I can proceed)
- None declared at initial setup.

## Declared Downstream (These need me)
- None declared at initial setup.

---

## Extracted Dependency Register
- **Status:** EXTRACTED; schema v3.1 in `Dependencies.csv`.
- **Rows:** 22 ACTIVE; 0 RETIRED; 11 ANCHOR (one parent and ten traces); 11 EXECUTION.
- **Origin:** 22 EXTRACTED; 0 DECLARED. Execution targets: 8 DOCUMENT, 1 DELIVERABLE, 1 EXTERNAL, 1 UNKNOWN.
- Extracted rows are evidence and agent interpretation; they do not replace human declarations or establish an accepted project DAG.

| DependencyID | Class | Direction | Target | Required condition |
|---|---|---|---|---|
| DEP-10-01-001 | ANCHOR | UPSTREAM | PKG-10 | DEL-10-01 implements its accepted PKG-10 parent definition. |
| DEP-10-01-002 | ANCHOR | UPSTREAM | SOW-102 | DEL-10-01 covers SOW-102: Carry current human direction, manuals and Root's conceptual/organisational role without a new precedence tree. |
| DEP-10-01-003 | ANCHOR | UPSTREAM | SOW-210 | DEL-10-01 covers SOW-210: Define the accepted package/deliverable working, checking and issued-record handoff. |
| DEP-10-01-004 | ANCHOR | UPSTREAM | SOW-214 | DEL-10-01 covers SOW-214: Explain Conceptual, FEED, 30%, 60%, 90%, 100% as developmental positions. |
| DEP-10-01-005 | ANCHOR | UPSTREAM | SOW-215 | DEL-10-01 covers SOW-215: Use Field Book route, relevant Consolidated reasoning and User Manual application together. |
| DEP-10-01-006 | ANCHOR | UPSTREAM | SOW-216 | DEL-10-01 covers SOW-216: Identify actual editions and deliberately treat changes. |
| DEP-10-01-007 | ANCHOR | UPSTREAM | SOW-217 | DEL-10-01 covers SOW-217: Carry project edition selection into the owning adoption record, retaining OI-017. |
| DEP-10-01-008 | ANCHOR | UPSTREAM | SOW-218 | DEL-10-01 covers SOW-218: Keep practice from adding unaccepted product requirements. |
| DEP-10-01-009 | ANCHOR | UPSTREAM | SOW-219 | DEL-10-01 covers SOW-219: Account for the purpose and actual treatment of an unused manual mechanism. |
| DEP-10-01-010 | ANCHOR | UPSTREAM | SOW-228 | DEL-10-01 covers SOW-228: Recover the already accepted stable basis and treat subsequent material change explicitly. |
| DEP-10-01-011 | ANCHOR | UPSTREAM | OBJ-010 | The documentary contribution supports OBJ-010 through accepted-basis, manual-led practice and accountable contracts. |
| DEP-10-01-012 | EXECUTION | UPSTREAM | APP-V4-BASIS-20260926 | Use the actual accepted composite and its recorded standing to produce the execution-basis account; preserve historical source identity. |
| DEP-10-01-013 | EXECUTION | UPSTREAM | APP-V4-CLARIFICATION-20260927 | Carry the accepted later clarification into the execution basis, preserving included definition work and coherent treatment of method constraints. |
| DEP-10-01-014 | EXECUTION | UPSTREAM | GROUP3-20260928T001055Z | Consume the final accepted decomposition and its actual decisions when preparing the basis and setup/local-contract handoff. |
| DEP-10-01-015 | EXECUTION | UPSTREAM | APP-V4-_COORDINATION | Use already approved coordination and lifecycle choices for OUT-002 and distinguish missing artifact/input evidence from contract maturity. |
| DEP-10-01-016 | EXECUTION | UPSTREAM | F | Use Field Book v1 for its assigned role in the manual-purpose/application/departure account, limited to relevant practice and actual receiving use. |
| DEP-10-01-017 | EXECUTION | UPSTREAM | M | Use Consolidated manual v7 for its assigned role in the manual-purpose/application/departure account, limited to relevant practice and actual receiving use. |
| DEP-10-01-018 | EXECUTION | UPSTREAM | U | Use Agent User Manual v3 for its assigned role in the manual-purpose/application/departure account, limited to relevant practice and actual receiving use. |
| DEP-10-01-019 | EXECUTION | UPSTREAM | APP-V4-CURRENT-EXECUTION-BASIS | Use the owning selection/adoption record and scope to bind actual manual and method edition/content identities before dependent reliance. |
| DEP-10-01-020 | EXECUTION | DOWNSTREAM | DEL-11-02 | Supply affected basis/manual-application adoption implications, with consumer and source identity, to DEL-11-02 at each receiving transition or retirement point of need. |
| DEP-10-01-021 | EXECUTION | DOWNSTREAM | Setup, local-SoW and project-definition consumers | Provide usable execution-basis and local-contract handoff outputs to the named setup, local-SoW and project-definition readers; no individual Deliverable dependency is inferred. |
| DEP-10-01-022 | EXECUTION | UPSTREAM | App-v4 owner | Where the manual-application account identifies a consequential adoption or departure requiring a decision, retain the actual owner decision at that affected point of need. |

---

## Lifecycle Summary
- Register lifecycle: ACTIVE 22; RETIRED 0.
- Closure lifecycle: NOT_APPLICABLE 11 (anchors); TBD 11 (execution); SATISFIED 0.
- Deliverable remains INITIALIZED: checked SOW_V1 only; no output fulfillment, readiness, adoption or later lifecycle act is asserted.

---

## Run Notes
- SCOPE DEL-10-01; MODE UPDATE; STRICTNESS CONSERVATIVE; CONSUMER_CONTEXT NONE; ARCHITECTURE_BASIS_POLICY NONE.
- SOURCE_DOCS, ANCHOR_DOC and EXECUTION_DOC_ORDER: ScopeOfWork.md only; DOC_ROLE_MAP DEFAULT. Source SHA256 7a89fc3874386d42aacd2ddbc2b10b96fca2dac126ff9a8c4c717a89d22b9b47.
- RUN_ROOT: projects/chirality-app-v4/execution. DECOMPOSITION_PATH: projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md. Accepted standing resolved through adjacent DECISION.md and HANDOFF_STATE.md; frozen candidate labels are historical.
- Pass 1 completed first: one explicit PKG-10 parent, nine assigned SOW traces and OBJ-010. Pass 2: eight documentary inputs, one actual DEL-11-02 handoff, one explicitly named reader handoff without a resolved Deliverable, one conditional owner-decision constraint.
- Declared mirrors added/refreshed/retired: 0/0/0. Two None declared at initial setup placeholders skipped; no unread or conflicting declaration.
- Local _REFERENCES.md Subsequent current-basis disposition resolves OI-017 for this App-v4 project-definition run through CURRENT_EXECUTION_BASIS.md. Historical SoW/frozen OPEN wording is unchanged; no new edition choice. Core editions are Field Book v1, Consolidated v7, Agent User Manual v3.
- All EXECUTION fulfillment is TBD. INITIALIZED is a checked-contract threshold, not delivered output, satisfied input, provider readiness, adoption, release or professional reliance. Actual output/decision conditions stay in Statement and Notes.
- DEL-10-02/03/04 and DEL-11-01 owner inventories alone do not create edges. No DAG-before-30% narrative is converted into a prerequisite from DEL-10-04 to this deliverable. No PEC/SWB/Domains provider edge is evidenced here.
- [LIMIT] One UNKNOWN downstream consumer mapping (DEP-10-01-021) remains a faithful reader handoff, not a forced graph edge. Owner decision DEP-10-01-022 is conditional on a consequential departure; no current departure or act is invented.
- Local schema, every used enum/ID value, parent count, uniqueness, verbatim quotes <=30 words, source identity and human-owned-section preservation checked; command results and hashes are in _run_records/dependency-extract-20260927.md. Global EVQ/DRB, closure and DAG acceptance are deferred to manager fan-in while peers write.

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-28T03:39:48.848948+00:00 — TASK /root/renewal_research_strategy/workflow_method_delta ran dependency-extract UPDATE/CONSERVATIVE for DEL-10-01; 22 ACTIVE (11 ANCHOR, 11 EXECUTION), 0 RETIRED; accepted Group3 basis resolved; one unresolved reader-to-Deliverable mapping, one conditional owner-decision constraint; local checks recorded; no closure/adoption claim.
