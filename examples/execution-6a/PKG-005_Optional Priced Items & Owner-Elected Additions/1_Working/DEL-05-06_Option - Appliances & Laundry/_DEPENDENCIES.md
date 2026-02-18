# Dependencies: DEL-05-06 Option - Appliances & Laundry

## Coordination (human-owned)
- **Mode:** DECLARED
- **Notes:** See _Coordination/_COORDINATION.md for project-level coordination record.

## Upstream (I need these before I can proceed) -- human-owned declarations
- No upstream dependencies declared yet.

## Downstream (These need me) -- human-owned declarations
- No downstream dependencies declared yet.

## Extracted Dependency Register

- **Status:** COMPLETE
- **Dependencies.csv:** `Dependencies.csv` (10 rows; schema v3.1)
- **Summary:** 10 ACTIVE rows (2 ANCHOR + 8 EXECUTION); 0 RETIRED rows.

### ANCHOR Dependencies (2 ACTIVE)

| DependencyID | AnchorType | TargetRefID | TargetName | Confidence | Status |
|---|---|---|---|---|---|
| DEP-05-06-001 | IMPLEMENTS_NODE | SOW-0505 | Optional priced item: Appliances for kitchen and laundry | HIGH | ACTIVE |
| DEP-05-06-002 | TRACES_TO_REQUIREMENT | OBJ-010 | Transparent separable pricing for optional scope items | HIGH | ACTIVE |

### EXECUTION Dependencies (8 ACTIVE)

| DependencyID | Direction | DependencyType | TargetType | TargetName | Confidence | Status |
|---|---|---|---|---|---|---|
| DEP-05-06-003 | UPSTREAM | PREREQUISITE | DOCUMENT | OSR S12.6 - Appliances | HIGH | ACTIVE |
| DEP-05-06-004 | UPSTREAM | PREREQUISITE | DOCUMENT | Functional Program S16.0 - Lunch Room/Kitchen | HIGH | ACTIVE |
| DEP-05-06-005 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-02-05 Mechanical Plumbing Ventilation & Exhaust | HIGH | ACTIVE |
| DEP-05-06-006 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-02-06 Electrical Power Lighting IT-Telecom & PA | HIGH | ACTIVE |
| DEP-05-06-007 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-05-07 Cash Allowance - FF&E (scope boundary) | HIGH | ACTIVE |
| DEP-05-06-008 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-01-07 Commissioning Training Closeout & Warranty | MEDIUM | ACTIVE |
| DEP-05-06-009 | UPSTREAM | CONSTRAINT | EXTERNAL | Owner Option Election (Written Notice) | HIGH | ACTIVE |
| DEP-05-06-010 | UPSTREAM | INTERFACE | PACKAGE | PKG-002 Base Building Design Intent (Rough-in Locations) | HIGH | ACTIVE |

## Run Notes

- **Run date:** 2026-02-17
- **MODE:** UPDATE
- **STRICTNESS:** CONSERVATIVE
- **CONSUMER_CONTEXT:** NONE
- **SOURCE_DOCS:** AUTO (resolved: Datasheet.md, Procedure.md, Specification.md, Guidance.md)
- **ANCHOR_DOC:** AUTO (resolved: `Datasheet.md` -- matched heuristic for `datasheet` keyword)
- **EXECUTION_DOC_ORDER:** AUTO (resolved: `Procedure.md`, `Specification.md`, `Guidance.md`)
- **DECOMPOSITION_PATH:** `_Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md` (available; used for anchor validation and target resolution)
- **_REFERENCES.md:** Available (used for OSR source location context)

### Warnings
- None. All quality checks passed.

### Assumptions recorded in extraction
- DEP-05-06-008 (HANDOVER to DEL-01-07): Confidence set to MEDIUM because the Procedure describes commissioning/warranty activities that logically feed into project-level closeout, but the handover is not framed as a formal prerequisite in either direction -- it is inferred from the workflow sequence.
- DEP-05-06-007 (INTERFACE with DEL-05-07): SatisfactionStatus set to NOT_APPLICABLE because this is a scope boundary clarification, not an artifact transfer requiring closure.
- A conditional interface for gas service from PKG-002/PKG-003 (Guidance TBD B-003) was identified but NOT extracted under CONSERVATIVE strictness because it is contingent on a TBD fuel-type decision that has not been made.

### Tree x DAG Integrity
- **Parent anchor (IMPLEMENTS_NODE):** 1 ACTIVE row (DEP-05-06-001 -> SOW-0505). PASS.
- **No FLOATING_NODE warning.** PASS.
- **No AMBIGUOUS_ANCHOR warning.** PASS.

## Run History

| Timestamp | Mode | Strictness | DecompositionStatus | Warnings | ACTIVE_ANCHOR | ACTIVE_EXECUTION | ACTIVE_Total |
|---|---|---|---|---|---|---|---|
| 2026-02-17 | UPDATE | CONSERVATIVE | Available (v1.0 PHASE7) | None | 2 | 8 | 10 |

## Lifecycle Summary

- **ACTIVE:** 10 (2 ANCHOR + 8 EXECUTION)
- **RETIRED:** 0

### Closure-state breakdown (ACTIVE rows)

| SatisfactionStatus | Count |
|---|---|
| TBD | 9 |
| NOT_APPLICABLE | 1 |

## Consumer Handoff Notes (optional)
- CONSUMER_CONTEXT is NONE; no handoff notes generated.
