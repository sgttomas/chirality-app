# Dependencies: DEL-011-07 Mezzanine Structure & Stairs

## Coordination (human-owned)
- **Mode:** NOT_TRACKED
- **Notes:** Coordination representation pending -- to be confirmed by human via ORCHESTRATOR.

## Upstream (I need these before I can proceed) -- human-owned declarations
- DEL-011-01 Superstructure -- Main structural frame must support mezzanine loads
- DEL-011-02 Steel Embedments -- Mezzanine attachment points may use floor embedments
- Dependencies coordinated externally by humans.

## Downstream (These need me) -- human-owned declarations
- PKG-012 Interior Construction & Fit-Out -- Mezzanine flooring and interior finishes
- Dependencies coordinated externally by humans.

## Extracted Dependency Register

- **Status:** POPULATED
- **Dependencies.csv:** Dependencies.csv (18 rows, schema v3.1)
- **Last Run:** 2026-03-26
- **Summary:** 5 ANCHOR + 13 EXECUTION = 18 total ACTIVE rows

### ANCHOR Edges (5 rows)

| DependencyID | AnchorType | TargetType | TargetRefID / TargetName | Confidence |
|---|---|---|---|---|
| DEP-011-07-001 | IMPLEMENTS_NODE | WBS_NODE | SOW-0032 Mezzanine storage -- no walls; steel railing; 10-foot forklift gate (Add. 4 Q6) | HIGH |
| DEP-011-07-002 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0032 Mezzanine storage -- no walls; steel railing; 10-foot forklift gate (Add. 4 Q6) | HIGH |
| DEP-011-07-003 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0033 Load-bearing capability | HIGH |
| DEP-011-07-004 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0034 Stairs to mezzanine | HIGH |
| DEP-011-07-005 | TRACES_TO_REQUIREMENT | WBS_NODE | OBJ-001 Functional maintenance shop addition | HIGH |

### EXECUTION Edges (13 rows)

| DependencyID | Direction | DependencyType | TargetType | Target | Confidence | EstimateImpactClass |
|---|---|---|---|---|---|---|
| DEP-011-07-006 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-011-01 Concrete Superstructure | HIGH | BLOCKING |
| DEP-011-07-007 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-011-02 Steel Plate Floor Embedments | HIGH | BLOCKING |
| DEP-011-07-008 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-002-05 Mezzanine Framing Details (IFC) | HIGH | BLOCKING |
| DEP-011-07-009 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-002-09 Stair Details (IFC) | HIGH | BLOCKING |
| DEP-011-07-010 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-002-10 Structural Calculation Package | MEDIUM | ADVISORY |
| DEP-011-07-011 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-002-12 Structural Specification | HIGH | BLOCKING |
| DEP-011-07-012 | UPSTREAM | CONSTRAINT | DELIVERABLE | DEL-009-02 Building Permit | HIGH | BLOCKING |
| DEP-011-07-013 | UPSTREAM | CONSTRAINT | DELIVERABLE | DEL-009-03 Safety Code Permits | HIGH | BLOCKING |
| DEP-011-07-014 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-019-04 Construction Quality Control Plan | MEDIUM | ADVISORY |
| DEP-011-07-015 | DOWNSTREAM | HANDOVER | PACKAGE | PKG-012 Interior Construction & Fit-Out | HIGH | BLOCKING |
| DEP-011-07-016 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-010-01 Foundation Construction | MEDIUM | ADVISORY |
| DEP-011-07-017 | UPSTREAM | CONSTRAINT | DOCUMENT | R-01 RFP (design requirements source) | HIGH | INFO |
| DEP-011-07-018 | UPSTREAM | CONSTRAINT | DOCUMENT | R-04 Appendix B Shop (conceptual drawing) | HIGH | INFO |

## Run Notes

### Run 2026-02-26 (Initial Extraction)

**Mode:** UPDATE | **Strictness:** CONSERVATIVE | **Consumer Context:** TASK_ESTIMATING
**Decomposition Path:** `_Decomposition/WDMLRL_Decomposition_Claude.md` (R1, 2026-02-25) -- located and used successfully.
**Source Documents:** ANCHOR_DOC: Datasheet.md; EXECUTION_DOCS: Procedure.md, Specification.md, Guidance.md
**Warnings:** None.

### Run 2026-03-26 (SCA-001 Refresh)

**Mode:** UPDATE | **Strictness:** CONSERVATIVE | **Consumer Context:** NONE
**Decomposition Path:** `_Decomposition/WDMLRL_Decomposition_Claude.md` (R2 -- 2026-03-26, SCA-001)

**SCA-001 Changes Affecting This Deliverable:**
- SOW-0032 significantly updated per Addendum 4, Q6: "Construct mezzanine storage above parts room, utility room, and wash bay; no perimeter walls -- standard steel safety railing with 10-foot sliding gate for forklift access"
- Key changes: (1) No perimeter walls required -- eliminates wall construction scope; (2) Steel safety railing required -- adds railing specification/procurement; (3) 10-foot sliding gate for forklift access -- adds gate specification and forklift loading interface.

**Changes Applied:**
1. **DEP-011-07-001 corrected:** IMPLEMENTS_NODE anchor was incorrectly targeting PKG-011 as a WBS_NODE. Corrected to target SOW-0032 as the primary scope item. Statement updated to reflect Add. 4 Q6 text.
2. **DEP-011-07-002 updated:** TRACES_TO_REQUIREMENT statement for SOW-0032 updated to reflect Add. 4 Q6 text (no walls, steel railing, forklift gate).
3. Updated LastSeen to 2026-03-26 on all 18 ACTIVE rows.
4. No new rows added under CONSERVATIVE mode. The forklift gate specification (10-foot sliding gate) may introduce a procurement/specification interface, but no explicit dependency edge is stated in source documents beyond what the existing structural design prerequisites (DEL-002-05) already cover. The gate specification will be captured in the IFC drawings.
5. No rows retired.

**Warnings:** None.

**Integrity Check Results:**
- Parent anchor (IMPLEMENTS_NODE): 1 ACTIVE row (DEP-011-07-001 -> SOW-0032) -- PASS (corrected from prior run which incorrectly anchored to PKG-011)
- DependencyID uniqueness: PASS (18 unique IDs)
- All ACTIVE rows have EvidenceFile + SourceRef: PASS
- FromDeliverableID consistency: PASS
- Schema version: v3.1 on all rows -- PASS
- Enum normalization: all values canonical -- PASS

## Run History

| Run Date | Mode | Strictness | Consumer | Decomposition | Warnings | ACTIVE Rows |
|---|---|---|---|---|---|---|
| 2026-02-26 | UPDATE | CONSERVATIVE | TASK_ESTIMATING | Located (R1) | None | 18 (5A + 13E) |
| 2026-03-26 | UPDATE | CONSERVATIVE | NONE | Located (R2 SCA-001) | None | 18 (5A + 13E) |

## Lifecycle Summary

| Category | Count |
|---|---|
| **ACTIVE** | 18 |
| **RETIRED** | 0 |
| **Total** | 18 |

### By DependencyClass

| Class | ACTIVE | RETIRED |
|---|---|---|
| ANCHOR | 5 | 0 |
| EXECUTION | 13 | 0 |

### SatisfactionStatus Breakdown (ACTIVE rows)

| Status | Count |
|---|---|
| PENDING | 13 |
| NOT_APPLICABLE | 5 |

### EstimateImpactClass Breakdown (ACTIVE EXECUTION rows)

| Class | Count |
|---|---|
| BLOCKING | 8 |
| ADVISORY | 3 |
| INFO | 2 |
