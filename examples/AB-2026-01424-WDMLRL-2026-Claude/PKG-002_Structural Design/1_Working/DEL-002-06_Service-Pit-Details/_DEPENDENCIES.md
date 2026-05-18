# Dependencies: DEL-002-06 Service Pit / Trench Structural Details

## Coordination (human-owned)
- **Mode:** NOT_TRACKED
- **Notes:** Coordination representation pending -- to be confirmed by human via ORCHESTRATOR.

## Upstream (I need these before I can proceed) -- human-owned declarations
- Dependencies coordinated externally by humans.

## Downstream (These need me) -- human-owned declarations
- Dependencies coordinated externally by humans.

## Extracted Dependency Register

- **Status:** COMPLETE
- **Dependencies.csv:** `Dependencies.csv` (v3.1 schema, 15 rows)
- **Last Run:** 2026-02-26
- **ACTIVE rows:** 15
- **RETIRED rows:** 0

### ANCHOR rows (3 ACTIVE)

| DependencyID | AnchorType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|
| DEP-002-06-A01 | IMPLEMENTS_NODE | SOW-0012 | Complete final structural design (concrete structure) | HIGH |
| DEP-002-06-A02 | TRACES_TO_REQUIREMENT | OBJ-001 | Deliver a code-compliant fully functional maintenance shop | HIGH |
| DEP-002-06-A03 | TRACES_TO_REQUIREMENT | OBJ-003 | Produce complete P.Eng.-stamped IFC design documentation | HIGH |

### EXECUTION rows (12 ACTIVE)

| DependencyID | Direction | DependencyType | TargetType | Target | Confidence | EstimateImpactClass |
|---|---|---|---|---|---|---|
| DEP-002-06-E01 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-008-01 Geotechnical Investigation & Report | HIGH | BLOCKING |
| DEP-002-06-E02 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-002-11 Foundation Design Package (Variable-Price) | MEDIUM | ADVISORY |
| DEP-002-06-E03 | UPSTREAM | INTERFACE | PACKAGE | PKG-003 Mechanical Design (Ventilation) | MEDIUM | ADVISORY |
| DEP-002-06-E04 | UPSTREAM | INTERFACE | PACKAGE | PKG-004 Electrical Design (Lighting) | MEDIUM | ADVISORY |
| DEP-002-06-E05 | UPSTREAM | INTERFACE | PACKAGE | PKG-006 Plumbing Design (Drainage) | MEDIUM | ADVISORY |
| DEP-002-06-E06 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-011-06 Service Pit/Trench (Construction) | HIGH | BLOCKING |
| DEP-002-06-E07 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-001-02 Architectural Floor Plans | MEDIUM | ADVISORY |
| DEP-002-06-E08 | UPSTREAM | PREREQUISITE | EXTERNAL | Equipment Load Specification (Owner) | HIGH | BLOCKING |
| DEP-002-06-E09 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-002-10 Structural Calculation Package | HIGH | ADVISORY |
| DEP-002-06-E10 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-002-12 Structural Specification | MEDIUM | INFO |
| DEP-002-06-E11 | DOWNSTREAM | ENABLES | DELIVERABLE | DEL-009-04 Code Compliance Register & Inspection Log | MEDIUM | INFO |
| DEP-002-06-E12 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-009-02 Building Permit Application & Approval | MEDIUM | ADVISORY |

---

## Run Notes

### Run: 2026-03-26 (SCA-001 refresh)

**Parameters:**
- SCOPE: PKG-002 (all deliverables DEL-002-01 through DEL-002-12)
- MODE: UPDATE | STRICTNESS: CONSERVATIVE | CONSUMER_CONTEXT: NONE
- DECOMPOSITION_PATH: `_Decomposition/WDMLRL_Decomposition_Claude.md` (R2 -- 2026-03-26, SCA-001)
- SOURCE_DOCS: AUTO | ANCHOR_DOC: Datasheet.md | EXECUTION_DOC_ORDER: Procedure.md, Specification.md, Guidance.md

**SCA-001 impact assessment:**
- No direct addenda changes affect the service pit scope. SOW-0028 is unchanged.
- The structural system change (precast walls + steel roof) does not directly alter service pit structural details, which are a below-grade concrete structure.
- No new dependency edges identified under CONSERVATIVE strictness.

**Extraction result:**
- All 15 existing ACTIVE rows re-confirmed. LastSeen updated to 2026-03-26.
- No new rows. No RETIRED rows.

**Warnings:**
- None.

---

### Run: 2026-02-26

**Parameters:**
- MODE: UPDATE
- STRICTNESS: CONSERVATIVE
- CONSUMER_CONTEXT: TASK_ESTIMATING
- SOURCE_DOCS: AUTO (resolved to: Datasheet.md, Specification.md, Procedure.md, Guidance.md)
- ANCHOR_DOC: AUTO (resolved to: Datasheet.md -- contains Identification section with SOW/OBJ traceability)
- EXECUTION_DOC_ORDER: AUTO (resolved to: Procedure.md, Specification.md, Datasheet.md, Guidance.md)
- DECOMPOSITION_PATH: `_Decomposition/WDMLRL_Decomposition_Claude.md` (available, R1 2026-02-25)
- _REFERENCES.md: available (read-only; used for document pointer resolution)

**Defaults applied:**
- ANCHOR_DOC heuristic selected Datasheet.md (contains "datasheet" in filename and Identification/traceability fields).
- EXECUTION_DOC_ORDER heuristic prioritized Procedure.md (contains "procedure" in filename and explicit prerequisites table), then Specification.md (contains "spec" and requirements with verification methods), then Datasheet.md and Guidance.md.

**Decomposition validation:**
- DEL-002-06 confirmed in decomposition: PKG-002, covers SOW-0012, supports OBJ-001 and OBJ-003.
- All referenced deliverable IDs validated against decomposition: DEL-008-01 (PKG-008), DEL-002-11 (PKG-002), DEL-011-06 (PKG-011), DEL-001-02 (PKG-001), DEL-002-10 (PKG-002), DEL-002-12 (PKG-002), DEL-009-04 (PKG-009), DEL-009-02 (PKG-009).

**Changes from prior extraction (2026-02-26 initial run):**
- DEP-002-06-E02: Target updated from DEL-002-02 (Foundation Plan) to DEL-002-11 (Foundation Design Package) to match explicit Datasheet text ("Foundation design (DEL-002-11, DEL-010-01) must be completed or coordinated first"). Prior extraction used DEL-002-02 which was not explicitly named in source.
- DEP-002-06-E07 through E12: 6 new EXECUTION rows added based on full multi-document extraction.
- Evidence quotes updated to be more precise across all rows.
- Notes updated with epistemic markers (FACT/ASSUMPTION) and decomposition validation confirmations.

**Warnings:**
- None. Parent anchor (IMPLEMENTS_NODE) count = 1: normal.

**SOW-0028 note:** The Datasheet Identification section references SOW-0028 (service pit/trench construction) in addition to SOW-0012. However, the decomposition scope ledger maps SOW-0028 to PKG-011/DEL-011-06, not to DEL-002-06. Per CONSERVATIVE strictness, SOW-0028 is not emitted as an ANCHOR for DEL-002-06. The relationship is captured instead as EXECUTION row DEP-002-06-E06 (DOWNSTREAM HANDOVER to DEL-011-06).

---

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ANCHOR ACTIVE | EXECUTION ACTIVE | Total ACTIVE |
|---|---|---|---|---|---|---|---|
| 2026-03-26 | UPDATE | CONSERVATIVE | Available (R2, SCA-001) | None | 3 | 12 | 15 |
| 2026-02-26 | UPDATE | CONSERVATIVE | Available (R1 2026-02-25) | None | 3 | 12 | 15 |

---

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 15 |
| RETIRED | 0 |

### Closure-state breakdown (ACTIVE rows)

| SatisfactionStatus | Count |
|---|---|
| TBD | 15 |

### By DependencyClass

| Class | ACTIVE | RETIRED |
|---|---|---|
| ANCHOR | 3 | 0 |
| EXECUTION | 12 | 0 |

---

## Downstream Handoff Notes

**Consumer Context: TASK_ESTIMATING**

The following dependencies are flagged as relevant to task estimating readiness:

### BLOCKING dependencies (3) -- gate meaningful estimating

| DependencyID | Direction | Target | Rationale |
|---|---|---|---|
| DEP-002-06-E01 | UPSTREAM | DEL-008-01 Geotechnical Investigation & Report | Pit depth, wall thickness, waterproofing system, and excavation scope all depend on geotech parameters. Quantities cannot be reliably estimated without this input. |
| DEP-002-06-E08 | UPSTREAM | Equipment Load Specification (Owner) | Cover system structural design (material type, thickness, framing) depends on equipment load data. Cost of cover system is a significant line item that cannot be estimated without confirmed loads. |
| DEP-002-06-E06 | DOWNSTREAM | DEL-011-06 Service Pit/Trench (Construction) | Construction estimating for the service pit requires this design drawing set. Handover timing affects construction schedule estimating. |

### ADVISORY dependencies (7) -- may affect quantities/specs

| DependencyID | Direction | Target | Rationale |
|---|---|---|---|
| DEP-002-06-E02 | UPSTREAM | DEL-002-11 Foundation Design Package | Foundation interface may affect pit edge/connection detailing. |
| DEP-002-06-E03 | UPSTREAM | PKG-003 Mechanical Design (Ventilation) | Ventilation penetrations affect structural blockout scope. |
| DEP-002-06-E04 | UPSTREAM | PKG-004 Electrical Design (Lighting) | Electrical penetrations affect structural blockout scope. |
| DEP-002-06-E05 | UPSTREAM | PKG-006 Plumbing Design (Drainage) | Drainage provisions affect pit floor slab design. |
| DEP-002-06-E07 | UPSTREAM | DEL-001-02 Architectural Floor Plans | Pit position confirmation affects dimensional scope. |
| DEP-002-06-E09 | DOWNSTREAM | DEL-002-10 Structural Calculation Package | Companion calculation deliverable; estimating of DEL-002-10 scope depends on DEL-002-06 complexity. |
| DEP-002-06-E12 | DOWNSTREAM | DEL-009-02 Building Permit | Permit submission timing depends on IFC drawing availability. |

### INFO dependencies (2) -- low likelihood of changing estimating totals

| DependencyID | Direction | Target | Rationale |
|---|---|---|---|
| DEP-002-06-E10 | UPSTREAM | DEL-002-12 Structural Specification | Companion specification; unlikely to change structural quantities. |
| DEP-002-06-E11 | DOWNSTREAM | DEL-009-04 Code Compliance Register | Inspection logging; does not affect design estimating. |
