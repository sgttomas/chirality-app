# Dependencies: DEL-011-02 Steel Plate Floor Embedments

## Coordination (human-owned)
- **Mode:** NOT_TRACKED
- **Notes:** Coordination representation pending -- to be confirmed by human via ORCHESTRATOR.

## Upstream (I need these before I can proceed) -- human-owned declarations
- DEL-011-01 Superstructure -- Concrete deck system must be cured and ready for embedment installation
- Dependencies coordinated externally by humans.

## Downstream (These need me) -- human-owned declarations
- PKG-012 Interior Construction & Fit-Out -- Equipment installation depends on embedments
- Dependencies coordinated externally by humans.

## Extracted Dependency Register

- **Status:** POPULATED
- **Dependencies.csv:** `Dependencies.csv` (v3.1 schema, 12 rows)
- **Summary:**

| DependencyID | Class | AnchorType | Direction | Type | TargetType | Target | Status |
|---|---|---|---|---|---|---|---|
| DEP-011-02-001 | ANCHOR | IMPLEMENTS_NODE | UPSTREAM | OTHER | WBS_NODE | SOW-0024 | ACTIVE |
| DEP-011-02-002 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | REQUIREMENT | OBJ-001 | ACTIVE |
| DEP-011-02-003 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-002-08 (Steel Plate Embedment Plan) | ACTIVE |
| DEP-011-02-004 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-002-12 (Structural Specification) | ACTIVE |
| DEP-011-02-005 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-002-10 (Structural Calculation Package) | ACTIVE |
| DEP-011-02-006 | EXECUTION | NOT_APPLICABLE | UPSTREAM | INTERFACE | DELIVERABLE | DEL-011-01 (Concrete Superstructure) | ACTIVE |
| DEP-011-02-007 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-009-03 (Safety Code Permits) | ACTIVE |
| DEP-011-02-008 | EXECUTION | NOT_APPLICABLE | UPSTREAM | INTERFACE | DELIVERABLE | DEL-018-05 (Wash Bay Drainage & Mud Sump) | ACTIVE |
| DEP-011-02-009 | EXECUTION | NOT_APPLICABLE | UPSTREAM | INTERFACE | DELIVERABLE | DEL-011-05 (Wash Bay Enclosure) | ACTIVE |
| DEP-011-02-010 | EXECUTION | NOT_APPLICABLE | DOWNSTREAM | HANDOVER | PACKAGE | PKG-012 (Interior Construction & Fit-Out) | ACTIVE |
| DEP-011-02-011 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DOCUMENT | R-01 (RFP) | ACTIVE |
| DEP-011-02-012 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DOCUMENT | R-04 (Appendix B Shop) | ACTIVE |

**Counts:** 12 ACTIVE, 0 RETIRED

## Run Notes

### Run 2026-02-26 (Initial Extraction)

**Run timestamp:** 2026-02-26
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer context:** TASK_ESTIMATING
**Decomposition path:** `_Decomposition/WDMLRL_Decomposition_Claude.md` (R1, 2026-02-25) -- AVAILABLE, used for anchor validation and target resolution.

**Defaults applied:**
- SOURCE_DOCS: AUTO -- scanned deliverable folder; identified Datasheet.md, Guidance.md, Procedure.md, Specification.md
- ANCHOR_DOC: AUTO -- selected Datasheet.md
- EXECUTION_DOC_ORDER: AUTO -- Procedure.md, Specification.md, Guidance.md
- DOC_ROLE_MAP: DEFAULT heuristic applied.

**Pass 1 (Anchor) observations:**
- Parent anchor identified: SOW-0024, confirmed in Decomposition S3, S7, and S8.
- Requirement trace identified: OBJ-001, confirmed in Decomposition S5 and S7.

**Pass 2 (Execution) observations:**
- Three upstream PKG-002 design deliverables as hard prerequisites (DEL-002-08, DEL-002-10, DEL-002-12).
- DEL-011-01 critical construction interface.
- DEL-009-03 regulatory prerequisite.
- Two scope boundary interfaces (DEL-018-05, DEL-011-05).
- One downstream handover to PKG-012.
- Two document dependencies (R-01 RFP, R-04 Appendix B).

**Warnings:** None.

### Run 2026-03-26 (SCA-001 Refresh)

**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer context:** NONE
**Decomposition path:** `_Decomposition/WDMLRL_Decomposition_Claude.md` (R2 -- 2026-03-26, SCA-001)

**SCA-001 Changes Affecting This Deliverable:**
- No direct changes to SOW-0024. The structural system clarification (precast walls + steel roof per Add. 2/4) affects the upstream superstructure (DEL-011-01) but does not alter the steel plate embedment scope or dependencies.

**Changes Applied:**
- Updated LastSeen to 2026-03-26 on all 12 ACTIVE rows.
- No new rows added. No rows retired. No statement changes.

**Warnings:** None.

## Run History

| Run | Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Count |
|---|---|---|---|---|---|---|
| 1 | 2026-02-26 | UPDATE | CONSERVATIVE | Available (R1, 2026-02-25) | None | 12 |
| 2 | 2026-03-26 | UPDATE | CONSERVATIVE | Available (R2, 2026-03-26 SCA-001) | None | 12 |

## Lifecycle Summary

### Extraction lifecycle
- **ACTIVE:** 12 rows
- **RETIRED:** 0 rows

### Closure lifecycle (ACTIVE rows)
| SatisfactionStatus | Count |
|---|---|
| NOT_APPLICABLE | 2 (ANCHOR rows) |
| PENDING | 5 (upstream deliverable prerequisites/interfaces awaiting issuance) |
| TBD | 3 (scope boundary interfaces and downstream handover -- status undetermined) |
| SATISFIED | 2 (document dependencies R-01 and R-04 -- accessible in _Sources/) |

### Dependency class breakdown (ACTIVE)
| DependencyClass | Count |
|---|---|
| ANCHOR | 2 |
| EXECUTION | 10 |

### Direction breakdown (ACTIVE EXECUTION rows)
| Direction | Count |
|---|---|
| UPSTREAM | 9 |
| DOWNSTREAM | 1 |
