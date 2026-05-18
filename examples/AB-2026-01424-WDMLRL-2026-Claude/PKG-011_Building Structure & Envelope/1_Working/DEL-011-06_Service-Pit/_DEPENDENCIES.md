# Dependencies: DEL-011-06 Service Pit/Trench

## Coordination (human-owned)
- **Mode:** NOT_TRACKED
- **Notes:** Coordination representation pending -- to be confirmed by human via ORCHESTRATOR.

## Upstream (I need these before I can proceed) -- human-owned declarations
- PKG-010 Foundation Construction -- Foundation must be completed before pit excavation begins
- DEL-011-01 Superstructure -- Structural frame may affect pit access during construction
- Dependencies coordinated externally by humans.

## Downstream (These need me) -- human-owned declarations
- PKG-012 Interior Construction & Fit-Out -- Equipment access via pit for maintenance
- Dependencies coordinated externally by humans.

---

## Extracted Dependency Register

**Schema Version:** v3.1
**Total ACTIVE rows:** 17
**Total RETIRED rows:** 0

### ANCHOR Dependencies (2 ACTIVE)

| DependencyID | AnchorType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|
| DEP-011-06-A01 | IMPLEMENTS_NODE | SOW-0028 | SOW-0028 | HIGH |
| DEP-011-06-A02 | TRACES_TO_REQUIREMENT | OBJ-001 | OBJ-001 | HIGH |

### EXECUTION Dependencies -- UPSTREAM (11 ACTIVE)

| DependencyID | DependencyType | TargetType | Target | Statement (abridged) | Confidence | EstimateImpactClass |
|---|---|---|---|---|---|---|
| DEP-011-06-E01 | PREREQUISITE | DELIVERABLE | DEL-002-06 (PKG-002) | IFC structural drawings must be issued before pit construction | HIGH | BLOCKING |
| DEP-011-06-E02 | PREREQUISITE | PACKAGE | PKG-010 | Foundation must be complete before pit excavation | HIGH | BLOCKING |
| DEP-011-06-E03 | CONSTRAINT | DELIVERABLE | DEL-011-01 (PKG-011) | Superstructure sequencing must not obstruct pit work | HIGH | ADVISORY |
| DEP-011-06-E04 | INTERFACE | PACKAGE | PKG-003 | Mechanical design must define ventilation performance criteria | HIGH | BLOCKING |
| DEP-011-06-E05 | INTERFACE | PACKAGE | PKG-004 | Electrical design must define lighting performance criteria | HIGH | ADVISORY |
| DEP-011-06-E06 | INTERFACE | PACKAGE | PKG-006 | Plumbing design must define pit floor drain routing | MEDIUM | ADVISORY |
| DEP-011-06-E07 | INTERFACE | PACKAGE | PKG-013 | Ventilation rough-in requirements confirmed before concrete | HIGH | BLOCKING |
| DEP-011-06-E08 | INTERFACE | PACKAGE | PKG-015 | Lighting rough-in requirements confirmed before concrete | HIGH | BLOCKING |
| DEP-011-06-E09 | INTERFACE | PACKAGE | PKG-014 | Floor drain rough-in requirements confirmed before concrete | MEDIUM | ADVISORY |
| DEP-011-06-E14 | PREREQUISITE | EXTERNAL | Owner (Camrose County) | Owner must provide equipment fleet dimensions -- single most critical data dependency | HIGH | BLOCKING |
| DEP-011-06-E15 | PREREQUISITE | PACKAGE | PKG-009 | Building permits and Safety Code permits must be in force | HIGH | BLOCKING |

### EXECUTION Dependencies -- DOWNSTREAM (4 ACTIVE)

| DependencyID | DependencyType | TargetType | Target | Statement (abridged) | Confidence | EstimateImpactClass |
|---|---|---|---|---|---|---|
| DEP-011-06-E10 | HANDOVER | PACKAGE | PKG-012 | Completed pit handed over for interior fit-out and maintenance | HIGH | INFO |
| DEP-011-06-E11 | INTERFACE | PACKAGE | PKG-013 | Ventilation rough-in handed over for mechanical commissioning | HIGH | INFO |
| DEP-011-06-E12 | INTERFACE | PACKAGE | PKG-015 | Lighting rough-in handed over for electrical commissioning | HIGH | INFO |
| DEP-011-06-E13 | INTERFACE | PACKAGE | PKG-014 | Drain rough-in handed over for plumbing connection and testing | MEDIUM | INFO |

---

## Run Notes

### Run 2026-02-26 (Initial Extraction)

**Mode:** UPDATE | **Strictness:** CONSERVATIVE | **Consumer Context:** TASK_ESTIMATING
**Decomposition Path:** `_Decomposition/WDMLRL_Decomposition_Claude.md` (R1 -- 2026-02-25)
**Source Documents:** ANCHOR_DOC: Datasheet.md; EXECUTION_DOCS: Procedure.md, Specification.md, Guidance.md
**Warnings:** None.

### Run 2026-03-26 (SCA-001 Refresh)

**Mode:** UPDATE | **Strictness:** CONSERVATIVE | **Consumer Context:** NONE
**Decomposition Path:** `_Decomposition/WDMLRL_Decomposition_Claude.md` (R2 -- 2026-03-26, SCA-001)

**SCA-001 Changes Affecting This Deliverable:**
- SOW-0028 text unchanged in decomposition. No addendum changes directly affect service pit/trench scope.

**Changes Applied:**
- Updated LastSeen to 2026-03-26 on all 17 ACTIVE rows.
- No new rows added. No rows retired. No statement changes.

**Warnings:** None.

**Integrity Check Results:**
- Parent anchor (IMPLEMENTS_NODE): 1 ACTIVE row (DEP-011-06-A01 -> SOW-0028) -- PASS
- DependencyID uniqueness: PASS (17 unique IDs)
- All ACTIVE rows have EvidenceFile + SourceRef: PASS
- FromDeliverableID consistency: PASS
- Schema version: v3.1 on all rows -- PASS

---

## Run History

| Timestamp | Mode | Strictness | Consumer | Decomposition | Warnings | ACTIVE Anchors | ACTIVE Execution | Total ACTIVE |
|---|---|---|---|---|---|---|---|---|
| 2026-02-26 | UPDATE | CONSERVATIVE | TASK_ESTIMATING | WDMLRL_Decomposition_Claude.md (R1) | None | 2 | 15 | 17 |
| 2026-03-26 | UPDATE | CONSERVATIVE | NONE | WDMLRL_Decomposition_Claude.md (R2 SCA-001) | None | 2 | 15 | 17 |

---

## Lifecycle Summary

| Category | Count |
|---|---|
| ACTIVE | 17 |
| RETIRED | 0 |

### Satisfaction Status Breakdown (ACTIVE rows)

| SatisfactionStatus | Count |
|---|---|
| PENDING | 11 |
| TBD | 4 |
| NOT_APPLICABLE | 2 |
