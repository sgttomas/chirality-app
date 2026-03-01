# Dependencies: DEL-002-02 Foundation Plan

## Coordination (human-owned)
- **Mode:** NOT_TRACKED
- **Notes:** Coordination representation pending -- to be confirmed by human via ORCHESTRATOR.

## Upstream (I need these before I can proceed) -- human-owned declarations
- Dependencies coordinated externally by humans.

## Downstream (These need me) -- human-owned declarations
- Dependencies coordinated externally by humans.

---

## Extracted Dependency Register

**RegisterSchemaVersion:** v3.1
**Total ACTIVE rows:** 22
**Total RETIRED rows:** 0

### ANCHOR rows (5 ACTIVE)

| DependencyID | AnchorType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|
| DEP-002-02-A01 | IMPLEMENTS_NODE | SOW-0012 | Complete final structural design | HIGH |
| DEP-002-02-A01b | IMPLEMENTS_NODE | SOW-0019 | Design foundation (variable-price post-geotech) | HIGH |
| DEP-002-02-A02 | TRACES_TO_REQUIREMENT | OBJ-001 | Code-compliant functional facility | HIGH |
| DEP-002-02-A03 | TRACES_TO_REQUIREMENT | OBJ-003 | Complete P.Eng.-stamped IFC documentation | HIGH |
| DEP-002-02-A04 | TRACES_TO_REQUIREMENT | OBJ-006 | Foundation cost reconciled post-geotech | HIGH |

### EXECUTION rows -- UPSTREAM (8 ACTIVE)

| DependencyID | DependencyType | TargetType | TargetID/Name | Confidence | EstimateImpactClass |
|---|---|---|---|---|---|
| DEP-002-02-E01 | PREREQUISITE | DELIVERABLE | DEL-002-01 Preliminary Structural Design | HIGH | BLOCKING |
| DEP-002-02-E02 | PREREQUISITE | DELIVERABLE | DEL-008-01 Geotechnical Investigation & Report | HIGH | BLOCKING |
| DEP-002-02-E03 | INTERFACE | DELIVERABLE | DEL-008-02 Preliminary Site Survey | HIGH | ADVISORY |
| DEP-002-02-E04 | INTERFACE | DELIVERABLE | DEL-001-02 Architectural Floor Plans | MEDIUM | ADVISORY |
| DEP-002-02-E05 | INTERFACE | DELIVERABLE | DEL-005-02 Site Grading Plan | MEDIUM | ADVISORY |
| DEP-002-02-E06 | INTERFACE | EXTERNAL | Crane Supplier Technical Data | HIGH | BLOCKING |
| DEP-002-02-E07 | INTERFACE | PACKAGE | PKG-006 Plumbing Engineer Input | MEDIUM | ADVISORY |
| DEP-002-02-E08 | INTERFACE | PACKAGE | PKG-003 Mechanical Engineer Input | MEDIUM | ADVISORY |

### EXECUTION rows -- DOWNSTREAM (9 ACTIVE)

| DependencyID | DependencyType | TargetType | TargetID/Name | Confidence | EstimateImpactClass |
|---|---|---|---|---|---|
| DEP-002-02-E09 | HANDOVER | DELIVERABLE | DEL-010-01 Foundation Construction | HIGH | BLOCKING |
| DEP-002-02-E10 | INTERFACE | DELIVERABLE | DEL-002-10 Structural Calculation Package | HIGH | ADVISORY |
| DEP-002-02-E11 | INTERFACE | DELIVERABLE | DEL-002-06 Service Pit / Trench Structural Details | HIGH | ADVISORY |
| DEP-002-02-E12 | INTERFACE | DELIVERABLE | DEL-002-08 Steel Plate Embedment Plan | HIGH | ADVISORY |
| DEP-002-02-E13 | INTERFACE | DELIVERABLE | DEL-002-07 Crane Support Structure Details | HIGH | ADVISORY |
| DEP-002-02-E14 | INTERFACE | DELIVERABLE | DEL-002-03 Structural Framing Plans | HIGH | ADVISORY |
| DEP-002-02-E15 | INTERFACE | DELIVERABLE | DEL-002-05 Mezzanine Framing Details | MEDIUM | ADVISORY |
| DEP-002-02-E16 | HANDOVER | DELIVERABLE | DEL-009-02 Building Permit Application & Approval | HIGH | ADVISORY |
| DEP-002-02-E17 | HANDOVER | DELIVERABLE | DEL-002-11 Foundation Design Package (Variable-Price) | HIGH | BLOCKING |

---

## Run Notes

**Run timestamp:** 2026-02-26
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer context:** TASK_ESTIMATING
**Decomposition path:** `/Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/_Decomposition/WDMLRL_Decomposition_Claude.md` (R1 -- 2026-02-25)
**Decomposition status:** Available and used for validation/label resolution.

**Source documents scanned (AUTO):**
- **ANCHOR_DOC:** `Datasheet.md` (selected by heuristic: filename contains "datasheet")
- **EXECUTION_DOC_ORDER:**
  1. `Procedure.md` (filename contains "procedure")
  2. `Specification.md` (filename contains "spec")
  3. `Guidance.md` (filename contains "guidance")

**Defaults applied:**
- SOURCE_DOCS=AUTO: scanned Datasheet.md, Specification.md, Procedure.md, Guidance.md (excluded _CONTEXT.md, _REFERENCES.md, _DEPENDENCIES.md, _SEMANTIC.md, _SEMANTIC_LENSING.md, _STATUS.md, Dependencies.csv as non-source artifacts)
- ANCHOR_DOC=AUTO: selected Datasheet.md
- EXECUTION_DOC_ORDER=AUTO: Procedure.md, Specification.md, Guidance.md

**Read-only inputs used:**
- `_REFERENCES.md` -- used to confirm document pointers. No dependencies emitted solely from references.
- `_CONTEXT.md` -- used for deliverable identity confirmation only.

**Warnings:**
- [WARNING] AMBIGUOUS_ANCHOR: Multiple ACTIVE parent anchors (IMPLEMENTS_NODE) found. DEP-002-02-A01 (SOW-0012) and DEP-002-02-A01b (SOW-0019). This is because the decomposition explicitly assigns two scope items to DEL-002-02 (SOW-0012 and SOW-0019). Both are retained as FACT.

**Assumptions:**
- No rows emitted based on assumption alone. All rows have EXPLICIT evidence.
- Electrical engineer input (Procedure Step 1.4) was not emitted as a separate dependency row because it is mentioned only as an addition within the mechanical/plumbing coordination context and does not constitute a standalone information-flow prerequisite with its own identified deliverable or artifact.

---

## Run History

| Timestamp | Mode | Strictness | Consumer | Decomposition | Warnings | ACTIVE Anchors | ACTIVE Execution | ACTIVE Total |
|---|---|---|---|---|---|---|---|---|
| 2026-02-26 | UPDATE | CONSERVATIVE | TASK_ESTIMATING | Available (R1 2026-02-25) | AMBIGUOUS_ANCHOR (2 IMPLEMENTS_NODE) | 5 | 17 | 22 |

---

## Lifecycle Summary

| Category | Count |
|---|---|
| ACTIVE rows (total) | 22 |
| RETIRED rows (total) | 0 |
| ANCHOR -- ACTIVE | 5 |
| EXECUTION -- ACTIVE | 17 |

### Satisfaction Status Breakdown (ACTIVE rows)

| SatisfactionStatus | Count |
|---|---|
| TBD | 22 |
| PENDING | 0 |
| IN_PROGRESS | 0 |
| SATISFIED | 0 |
| WAIVED | 0 |
| NOT_APPLICABLE | 0 |

### Estimate Impact Breakdown (EXECUTION rows, ACTIVE)

| EstimateImpactClass | Count |
|---|---|
| BLOCKING | 5 |
| ADVISORY | 12 |
| INFO | 0 |
| TBD | 0 |

---

## Downstream Handoff Notes

**Consumer context:** TASK_ESTIMATING

### Key findings for estimating readiness:

1. **BLOCKING upstream prerequisites (3 rows):**
   - **DEL-002-01 (Preliminary Structural Design):** County approval required before IFC. If not yet approved, foundation plan scope/quantities cannot be finalized.
   - **DEL-008-01 (Geotechnical Investigation & Report):** Foundation type, bearing capacity, and depth are TBD until geotech is received. Preliminary estimate uses "normal ground conditions" assumption per RFP §4.8.2. The variable-price scope (SOW-0019) means final foundation cost is explicitly deferred post-geotech.
   - **Crane Supplier Technical Data:** Crane column footing design depends on supplier-specific reaction loads. Conservative preliminary loading may suffice for preliminary estimate.

2. **BLOCKING downstream handovers (2 rows):**
   - **DEL-010-01 (Foundation Construction):** Construction cannot begin without IFC foundation plans. Estimating for construction scope is gated.
   - **DEL-002-11 (Foundation Design Package, Variable-Price):** Post-geotech reconciliation package depends on foundation plan assumptions being documented.

3. **Variable-price scope impact:** This deliverable is central to OBJ-006 (foundation cost reconciled post-geotech). Estimating should treat foundation quantities as preliminary until DEL-008-01 is received. The boundary between firm-price and variable-price scope items is unresolved (see Conflict Table C-002 in Guidance.md).

4. **ADVISORY interfaces (12 rows):** Multiple PKG-002 internal coordination interfaces (DEL-002-03, -05, -06, -07, -08, -10) and cross-discipline interfaces (DEL-001-02, DEL-005-02, DEL-008-02, PKG-003, PKG-006) exist, plus downstream handovers to DEL-009-02 (Building Permit). These may affect quantities/specifications but are not hard gates for initiating estimates.
