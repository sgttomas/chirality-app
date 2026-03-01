# Dependencies: DEL-011-04 Entrance/Exit Doors

## Coordination (human-owned)
- **Mode:** NOT_TRACKED
- **Notes:** Coordination representation pending -- to be confirmed by human via ORCHESTRATOR.

## Upstream (I need these before I can proceed) -- human-owned declarations
- DEL-011-01 Superstructure -- Structural openings must be framed and ready
- Dependencies coordinated externally by humans.

## Downstream (These need me) -- human-owned declarations
- PKG-012 Interior Construction & Fit-Out -- Interior access depends on operational doors
- Dependencies coordinated externally by humans.

## Extracted Dependency Register

- **Status:** COMPLETE
- **Dependencies.csv:** Dependencies.csv (7 rows, 7 ACTIVE, 0 RETIRED)
- **Schema Version:** v3.1

### ANCHOR Edges (2 ACTIVE)

| DependencyID | AnchorType | TargetType | TargetRefID / TargetName | Confidence |
|---|---|---|---|---|
| DEP-011-04-001 | IMPLEMENTS_NODE | WBS_NODE | SOW-0026 | HIGH |
| DEP-011-04-002 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-001 | HIGH |

### EXECUTION Edges (5 ACTIVE)

| DependencyID | Direction | DependencyType | TargetType | Target | Confidence | EstimateImpact |
|---|---|---|---|---|---|---|
| DEP-011-04-003 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-001-07 Door & Window Schedule | HIGH | BLOCKING |
| DEP-011-04-004 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-001-11 Architectural Specification | HIGH | BLOCKING |
| DEP-011-04-005 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-011-01 Concrete Superstructure | HIGH | BLOCKING |
| DEP-011-04-006 | DOWNSTREAM | ENABLES | PACKAGE | PKG-012 Interior Construction & Fit-Out | HIGH | ADVISORY |
| DEP-011-04-007 | UPSTREAM | INTERFACE | PACKAGE | PKG-015 Electrical & Low-Voltage Installation | MEDIUM | ADVISORY |

## Run Notes

**Run Date:** 2026-02-26
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer Context:** TASK_ESTIMATING

**Decomposition Path:** `_Decomposition/WDMLRL_Decomposition_Claude.md` (R1, 2026-02-25) -- located and validated.

**Source Documents Scanned (with roles):**
- ANCHOR_DOC: `Datasheet.md` (matched heuristic: "datasheet")
- EXECUTION_DOCS (in order): `Procedure.md`, `Guidance.md`, `Specification.md`

**Defaults Applied:**
- SOURCE_DOCS: AUTO -- scanned deliverable folder; identified Datasheet.md, Guidance.md, Procedure.md, Specification.md as source documents (excluded _DEPENDENCIES.md, _REFERENCES.md, _CONTEXT.md, _STATUS.md, _SEMANTIC.md, _SEMANTIC_LENSING.md as non-source artifacts).
- DOC_ROLE_MAP: DEFAULT heuristic applied.
- ANCHOR_DOC: AUTO -- selected Datasheet.md (highest-confidence match for anchor signal).
- EXECUTION_DOC_ORDER: AUTO -- Procedure.md (procedure/method match), Guidance.md (guidance match), Specification.md (spec match).

**Extraction Notes:**
- Pass 1 (ANCHOR): Found 1 IMPLEMENTS_NODE anchor (SOW-0026) and 1 TRACES_TO_REQUIREMENT anchor (OBJ-001). Both confirmed against Decomposition §7 PKG-011 table and §5 Objectives.
- Pass 2 (EXECUTION): Found 3 UPSTREAM PREREQUISITE edges (DEL-001-07, DEL-001-11, DEL-011-01), 1 DOWNSTREAM ENABLES edge (PKG-012), and 1 UPSTREAM INTERFACE edge (PKG-015, conditional).
- DEP-011-04-007 (PKG-015 interface) is conditional on design decisions (electronic access control); marked IMPLICIT, Confidence=MEDIUM, ASSUMPTION in Notes.
- _REFERENCES.md was read to confirm available document pointers; no additional dependency rows were generated from it beyond what sources explicitly state.
- Declared upstream (DEL-011-01) and downstream (PKG-012) from human-owned sections are corroborated by extracted evidence in source documents.

**Warnings:** None.

## Run History

| Run | Date | Mode | Strictness | Decomp Status | Warnings | ACTIVE Anchors | ACTIVE Execution | Total ACTIVE |
|---|---|---|---|---|---|---|---|---|
| 1 | 2026-02-26 | UPDATE | CONSERVATIVE | Located (R1 2026-02-25) | None | 2 | 5 | 7 |

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 7 |
| RETIRED | 0 |

| SatisfactionStatus | Count |
|---|---|
| NOT_APPLICABLE | 2 |
| PENDING | 4 |
| TBD | 1 |

**Closure breakdown:**
- NOT_APPLICABLE (2): Anchor edges (DEP-011-04-001, DEP-011-04-002) -- anchors do not have closure lifecycle.
- PENDING (4): DEP-011-04-003 through DEP-011-04-006 -- these upstream prerequisites and downstream handover are open and awaiting fulfillment.
- TBD (1): DEP-011-04-007 -- PKG-015 interface is conditional on design decisions not yet made.

## Downstream Handoff Notes

**Consumer Context:** TASK_ESTIMATING

Estimating-relevant observations for this deliverable:

1. **Three BLOCKING upstream prerequisites** (DEL-001-07, DEL-001-11, DEL-011-01) must be satisfied before meaningful estimating of this deliverable can proceed. Door quantity, sizes, materials, hardware, and fire-rating requirements are all TBD pending these design documents. Without DEL-001-07 (Door & Window Schedule), the estimator cannot determine material quantities or specifications.

2. **DEL-001-07 is the critical gating document** for estimating readiness. It explicitly covers SOW-0026 and will specify door types, sizes, quantities, hardware sets, and any fire ratings. The Datasheet notes "Number of doors: TBD" and nearly all material attributes are TBD pending this schedule.

3. **DEL-001-11 (Architectural Specification)** governs installation requirements, tolerances, and material standards. It is the secondary gating document for detailed estimating (labour rates, installation methods, specialty requirements).

4. **DEL-011-01 (Concrete Superstructure)** is a physical sequencing prerequisite; it does not gate the estimating of this deliverable but does gate scheduling.

5. **PKG-015 interface** is conditional and unlikely to materially affect base estimating unless electronic access control is specified. Mark as ADVISORY for estimating purposes.

6. **PKG-012 downstream dependency** is informational for estimating -- it does not affect cost estimation of this deliverable but may affect schedule sequencing and critical path analysis.
