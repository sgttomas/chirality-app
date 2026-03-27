# Dependencies: DEL-001-02 Architectural Floor Plans

## Coordination (human-owned)
- **Mode:** NOT_TRACKED
- **Notes:** Coordination representation pending -- to be confirmed by human via ORCHESTRATOR.

## Upstream (I need these before I can proceed) -- human-owned declarations
- Dependencies coordinated externally by humans.

## Downstream (These need me) -- human-owned declarations
- Dependencies coordinated externally by humans.

## Extracted Dependency Register

- **Status:** POPULATED
- **Dependencies.csv:** Dependencies.csv (v3.1 schema)
- **Total ACTIVE rows:** 20
- **Total RETIRED rows:** 0

### ANCHOR Rows (3 ACTIVE)

| DependencyID | AnchorType | TargetType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|---|
| DEP-001-02-A01 | IMPLEMENTS_NODE | WBS_NODE | SOW-0011 | Complete final architectural design for the addition | HIGH |
| DEP-001-02-A02 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-001 | Deliver a code-compliant, fully functional maintenance shop addition | HIGH |
| DEP-001-02-A03 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-003 | Produce complete P.Eng.-stamped IFC design documentation across all disciplines | HIGH |

### EXECUTION Rows (17 ACTIVE)

| DependencyID | Direction | DependencyType | TargetType | TargetDeliverableID / TargetRefID | TargetName | Confidence |
|---|---|---|---|---|---|---|
| DEP-001-02-E01 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-001-01 | Preliminary Architectural Design | HIGH |
| DEP-001-02-E02 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-008-01 | Geotechnical Investigation & Report | HIGH |
| DEP-001-02-E03 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-008-02 | Preliminary Site Survey | HIGH |
| DEP-001-02-E04 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-002-03 | Structural Framing Plans | HIGH |
| DEP-001-02-E05 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-006-04 | Cistern & Pump Details | HIGH |
| DEP-001-02-E06 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-003-02 | HVAC Layout Plans | HIGH |
| DEP-001-02-E07 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-002-06 | Service Pit / Trench Structural Details | HIGH |
| DEP-001-02-E08 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-002-05 | Mezzanine Framing Details | HIGH |
| DEP-001-02-E09 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-002-07 | Crane Support Structure Details | HIGH |
| DEP-001-02-E10 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-002-08 | Steel Plate Embedment Plan | HIGH |
| DEP-001-02-E11 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-001-09 | Old North Shop Demolition Plans | MEDIUM |
| DEP-001-02-E12 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-009-02 | Building Permit Application & Approval | HIGH |
| DEP-001-02-E13 | UPSTREAM | CONSTRAINT | DOCUMENT | (none) | Alberta Building Code (current edition) | HIGH |
| DEP-001-02-E14 | UPSTREAM | PREREQUISITE | DOCUMENT | R-04 | Appendix B Conceptual Drawing (Shop) | HIGH |
| DEP-001-02-E15 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-011-01 | Concrete Superstructure | MEDIUM |
| DEP-001-02-E16 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-004-04 | Lighting Plans | MEDIUM |
| DEP-001-02-E17 | UPSTREAM | PREREQUISITE | DOCUMENT | R-10 | Addendum 4 (precast walls, folding doors, crane spacing, mezzanine railing) | HIGH |

## Run Notes

### Run: 2026-03-26 (R2 refresh)

**Parameters:**
- SCOPE: DEL-001-02_Floor-Plans (as part of PKG-001 full refresh)
- MODE: UPDATE
- STRICTNESS: CONSERVATIVE
- CONSUMER_CONTEXT: NONE
- SOURCE_DOCS: AUTO
- ANCHOR_DOC: AUTO (resolved to Datasheet.md)
- EXECUTION_DOC_ORDER: AUTO (resolved to Procedure.md, Specification.md, Guidance.md)
- DECOMPOSITION_PATH: `_Decomposition/WDMLRL_Decomposition_Claude.md` (R2, 2026-03-26, SCA-001)

**Extraction Decisions:**
- Pass 1 (ANCHOR): 3 rows carried forward; all confirmed against R2 decomposition. SOW-0011 text updated in R2 (interior walls precast concrete per Add. 4 Q5) but SOW-0011 ID unchanged; anchor row unchanged.
- Pass 2 (EXECUTION): 16 prior rows confirmed ACTIVE; all updated with LastSeen=2026-03-26.
- 1 new row added: DEP-001-02-E17 (R-10 Addendum 4 as prerequisite document). Addendum 4 materially changes floor plan parameters including interior wall material (precast concrete), overhead door type (folding outward), crane runway bay spacing (max 25 ft), corbel-supported crane, and mezzanine guard (railing with forklift gate, no walls).

**Warnings:**
- None.

### Run: 2026-02-26 (initial + re-extraction)

- MODE: UPDATE | STRICTNESS: CONSERVATIVE | CONSUMER_CONTEXT: TASK_ESTIMATING
- 19 rows extracted. No warnings.

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Count |
|---|---|---|---|---|---|
| 2026-02-26 | UPDATE | CONSERVATIVE | R1 (validated) | None | 19 |
| 2026-03-26 | UPDATE | CONSERVATIVE | R2, SCA-001 (validated) | None | 20 |

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 20 |
| RETIRED | 0 |

### Closure state breakdown (ACTIVE rows)

| SatisfactionStatus | Count |
|---|---|
| PENDING | 15 |
| TBD | 4 |
| SATISFIED | 1 |

**Notes:**
- 3 ANCHOR rows have SatisfactionStatus=TBD.
- DEP-001-02-E14 (R-04 Appendix B) remains SATISFIED.
- DEP-001-02-E17 (R-10 Addendum 4) is TBD -- document available but design impact assessment pending.
- All other EXECUTION rows are PENDING.
