# Dependencies: DEL-01-02 Baseline Schedule, Updates & Reporting

## Coordination (human-owned)
- **Mode:** DECLARED
- **Notes:** See _Coordination/_COORDINATION.md for project-level coordination record.

## Upstream (I need these before I can proceed) -- human-owned declarations
- No upstream dependencies declared yet.

## Downstream (These need me) -- human-owned declarations
- No downstream dependencies declared yet.

## Extracted Dependency Register

- **Status:** COMPLETED
- **Dependencies.csv:** `Dependencies.csv` (9 rows)
- **Last Run:** 2026-02-17
- **Summary:** 4 ANCHOR rows + 5 EXECUTION rows = 9 total ACTIVE rows; 0 RETIRED rows.

### ANCHOR Edges (4 ACTIVE)

| DependencyID | AnchorType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|
| DEP-0102-001 | IMPLEMENTS_NODE | -- | PKG-001 General Requirements & Delivery Controls | HIGH |
| DEP-0102-002 | TRACES_TO_REQUIREMENT | SOW-0007 | SOW-0007 Provide detailed project schedule in Gantt format | HIGH |
| DEP-0102-003 | TRACES_TO_REQUIREMENT | SOW-0602 | SOW-0602 Project schedule not Owner-driven; leverage schedule flexibility | HIGH |
| DEP-0102-004 | TRACES_TO_REQUIREMENT | OBJ-008 | OBJ-008 Execute safe controlled Design-Build delivery with schedule flexibility optimization | HIGH |

### EXECUTION Edges (5 ACTIVE)

| DependencyID | Direction | DependencyType | TargetType | TargetDeliverableID / TargetName | Confidence |
|---|---|---|---|---|---|
| DEP-0102-005 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-01-01_Integrated-Design-Management | MEDIUM |
| DEP-0102-006 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-01-06_Site-Supervision-and-Logistics | MEDIUM |
| DEP-0102-007 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-01-04_Permitting-and-Inspections-Coordination | MEDIUM |
| DEP-0102-008 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-01-05_Project-Controls-and-Documentation | HIGH |
| DEP-0102-009 | UPSTREAM | PREREQUISITE | DOCUMENT | CCDC 14-2013 Supplementary Conditions (Appendix J) | HIGH |

## Run Notes

### Defaults and Paths Used
- **MODE:** UPDATE
- **STRICTNESS:** CONSERVATIVE
- **CONSUMER_CONTEXT:** NONE
- **SOURCE_DOCS:** AUTO -- resolved to: `Datasheet.md`, `Guidance.md`, `Procedure.md`, `Specification.md`
- **ANCHOR_DOC:** AUTO -- resolved to: `Datasheet.md` (contains `datasheet` keyword; highest-confidence match for definition/traceability signal)
- **EXECUTION_DOC_ORDER:** AUTO -- resolved to: `Procedure.md`, `Guidance.md`, `Specification.md` (Procedure ranked first for workflow signal; Guidance and Specification for supplementary execution cues)
- **DECOMPOSITION_PATH:** `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md` -- found and used for anchor validation and label resolution.
- **_REFERENCES.md:** Present; used for document pointer resolution (CCDC 14 Appendix J location confirmed as TBD).

### Warnings
- None.

### Assumptions Documented
- **DEP-0102-005, DEP-0102-006, DEP-0102-007:** Source text (Procedure.md Prerequisites) explicitly labels these upstream deliverable dependencies as ASSUMPTION rather than DECLARED. The source states: "No upstream dependencies declared in _DEPENDENCIES.md at time of document preparation. ASSUMPTION: The following information inputs are practically required before finalizing the schedule." These are recorded as EXTRACTED with Confidence=MEDIUM and Notes=ASSUMPTION. Guidance C7 corroborates the same dependency set.
- **DEP-0102-009:** CCDC 14-2013 Appendix J location is TBD per both Procedure.md and Specification.md. TargetLocation recorded as `location TBD`.

### Extraction Decisions
- Specification Out of Scope references to DEL-01-03, DEL-01-04, DEL-01-07, DEL-01-05 are scope boundary statements (structural adjacency), NOT information flow dependencies. Not extracted.
- Guidance C5 (Addenda impacts on schedule) references Addenda 01-03 as potentially affecting schedule assumptions but does not state a specific information/artifact transfer dependency. Not extracted as a separate edge (covered by general source document references in _REFERENCES.md).
- Guidance C8 (Independent Schedule Review) is a TBD consideration, not a dependency. Not extracted.
- Procedure Step C4 (Meeting Minutes scope boundary with DEL-01-05) is a scope boundary question, not an information flow dependency. Not extracted.

## Run History

| Timestamp | Mode | Strictness | DecompositionStatus | Warnings | ACTIVE_ANCHOR | ACTIVE_EXECUTION | ACTIVE_Total |
|---|---|---|---|---|---|---|---|
| 2026-02-17 | UPDATE | CONSERVATIVE | Found and used (v1.0 PHASE7) | None | 4 | 5 | 9 |

## Lifecycle Summary

### Extraction Lifecycle
- **ACTIVE:** 9
- **RETIRED:** 0

### Closure Lifecycle (SatisfactionStatus breakdown for ACTIVE rows)
- **TBD:** 5 (all EXECUTION rows)
- **NOT_APPLICABLE:** 4 (all ANCHOR rows)

## Consumer Handoff Notes (optional)
- CONSUMER_CONTEXT=NONE; no handoff notes generated.
