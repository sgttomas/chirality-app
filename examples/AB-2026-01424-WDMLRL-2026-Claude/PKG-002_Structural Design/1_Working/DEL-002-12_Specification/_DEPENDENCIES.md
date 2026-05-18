# Dependencies: DEL-002-12 Structural Specification

## Coordination (human-owned)
- **Mode:** NOT_TRACKED
- **Notes:** Coordination representation pending -- to be confirmed by human via ORCHESTRATOR.

## Upstream (I need these before I can proceed) -- human-owned declarations
- Dependencies coordinated externally by humans.

## Downstream (These need me) -- human-owned declarations
- Dependencies coordinated externally by humans.

## Extracted Dependency Register

- **Status:** POPULATED
- **Dependencies.csv:** Dependencies.csv (17 rows; 17 ACTIVE, 0 RETIRED)
- **Schema Version:** v3.1
- **Last Run:** 2026-02-26

### ANCHOR Rows (3 ACTIVE)

| DependencyID | AnchorType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|
| DEP-002-12-A01 | IMPLEMENTS_NODE | SOW-0012 | Complete final structural design (concrete structure 35 ft ceiling) | HIGH |
| DEP-002-12-A02 | TRACES_TO_REQUIREMENT | OBJ-001 | Deliver a code-compliant fully functional maintenance shop addition | HIGH |
| DEP-002-12-A03 | TRACES_TO_REQUIREMENT | OBJ-003 | Produce complete P.Eng.-stamped IFC design documentation across all disciplines | HIGH |

### EXECUTION Rows -- UPSTREAM (7 ACTIVE)

| DependencyID | DependencyType | Target | Statement (summary) | EstimateImpactClass |
|---|---|---|---|---|
| DEP-002-12-E01 | PREREQUISITE | DEL-008-01 (Geotechnical Investigation & Report) | Geotech report is essential data prerequisite for foundation-superstructure interface parameters | BLOCKING |
| DEP-002-12-E06 | CONSTRAINT | DEL-002-01 (Preliminary Structural Design) | P.Eng. signing shall not proceed until DEL-002-01 has received County approval | BLOCKING |
| DEP-002-12-E09 | PREREQUISITE | DEL-016-01 (Two 5-Tonne Overhead Cranes) | Crane manufacturer specs are an irrefutable prerequisite for crane runway design | BLOCKING |
| DEP-002-12-E10 | INTERFACE | DEL-001-02 (Architectural Floor Plans) | Architectural floor plans needed for structural coordination | ADVISORY |
| DEP-002-12-E11 | INTERFACE | PKG-003 (Mechanical Design) | Mechanical inputs needed for service pit ventilation and HVAC clearance | ADVISORY |
| DEP-002-12-E12 | INTERFACE | PKG-004 (Electrical Design) | Electrical inputs needed for crane conduit and pit lighting | ADVISORY |
| DEP-002-12-E13 | INTERFACE | DEL-001-10 (Old North Shop Renovation Plans) | Renovation plans needed for Old North Shop structural scope | ADVISORY |

### EXECUTION Rows -- DOWNSTREAM (7 ACTIVE)

| DependencyID | DependencyType | Target | Statement (summary) | EstimateImpactClass |
|---|---|---|---|---|
| DEP-002-12-E02 | INTERFACE | DEL-002-02 (Foundation Plan) | Spec governs material/performance requirements for foundation plan | ADVISORY |
| DEP-002-12-E03 | INTERFACE | DEL-002-03 (Structural Framing Plans) | Spec governs material/performance requirements for framing plans | ADVISORY |
| DEP-002-12-E04 | HANDOVER | PKG-010 (Foundation Construction) | Spec is reference standard for foundation construction | ADVISORY |
| DEP-002-12-E05 | HANDOVER | PKG-011 (Building Structure & Envelope) | Spec is reference standard for superstructure construction | ADVISORY |
| DEP-002-12-E07 | INTERFACE | DEL-002-10 (Structural Calculation Package) | Spec performance requirements feed calc package | ADVISORY |
| DEP-002-12-E08 | INTERFACE | DEL-002-11 (Foundation Design Package) | Spec includes general foundation requirements; cross-references DEL-002-11 | ADVISORY |
| DEP-002-12-E14 | HANDOVER | PKG-009 (Permitting & Regulatory Compliance) | Spec submitted as part of IFC package for building permit | ADVISORY |

---

## Run Notes

### Run: 2026-03-26 (SCA-001 refresh)

**Parameters:**
- SCOPE: PKG-002 (all deliverables DEL-002-01 through DEL-002-12)
- MODE: UPDATE | STRICTNESS: CONSERVATIVE | CONSUMER_CONTEXT: NONE
- DECOMPOSITION_PATH: `_Decomposition/WDMLRL_Decomposition_Claude.md` (R2 -- 2026-03-26, SCA-001)
- SOURCE_DOCS: AUTO | ANCHOR_DOC: Datasheet.md | EXECUTION_DOC_ORDER: Specification.md, Procedure.md, Guidance.md

**SCA-001 impact assessment:**
- SOW-0012 updated: "precast concrete walls, steel roof structure, interior walls precast concrete" (Add. 2/4). Structural Specification must now include: precast concrete panel specifications (exterior and interior walls), steel roof structure specifications, precast panel connection and erection requirements.
- _CONTEXT.md updated (2026-03-26): "Specification must address precast concrete panel requirements (exterior and interior walls) and steel roof structure (Add. 2/4)."
- **Impact on existing dependencies:** All existing edges remain valid. The specification's scope expands to include precast and steel roof material/performance requirements, but no new information-flow edges are required beyond what already exists (geotech, crane supplier, architectural coordination, MEP coordination are all represented).
- **Potential new dependency signal:** Precast panel manufacturer specification data (panel properties, tolerances, connection hardware) and steel joist/truss manufacturer data may be needed as specification inputs. Source documents not yet updated. Under CONSERVATIVE strictness, no new row emitted.
- **Recommendation:** After source documents are updated to reflect SCA-001, precast and steel roof supplier interfaces may warrant new EXECUTION rows.

**Extraction result:**
- All 17 existing ACTIVE rows re-confirmed. LastSeen updated to 2026-03-26.
- No new rows. No RETIRED rows.

**Warnings:**
- None.

---

### Defaults and Chosen Paths (2026-02-26)

| Parameter | Value |
|---|---|
| SCOPE | DEL-002-12_Specification |
| RUN_ROOT | .../PKG-002_Structural Design/1_Working/DEL-002-12_Specification |
| MODE | UPDATE |
| STRICTNESS | CONSERVATIVE |
| CONSUMER_CONTEXT | TASK_ESTIMATING |
| SOURCE_DOCS | AUTO (4 docs detected: Datasheet.md, Specification.md, Procedure.md, Guidance.md) |
| ANCHOR_DOC | Datasheet.md (selected by heuristic: filename contains 'datasheet') |
| EXECUTION_DOC_ORDER | Specification.md, Procedure.md, Guidance.md |
| DECOMPOSITION_PATH | _Decomposition/WDMLRL_Decomposition_Claude.md (available; validation enabled) |
| _REFERENCES.md | Available; used for document pointer resolution |

### Assumptions

- ASSUMPTION: DEL-001-02 (Architectural Floor Plans) listed as "coordination prerequisite" in Procedure -- treated as INTERFACE because the Procedure explicitly describes specific data transfer (room dimensions, layout coordination), not merely "keep aligned."
- ASSUMPTION: PKG-003 and PKG-004 interfaces are extracted because Procedure Step 6.1 lists specific structural penetrations and coordination items, constituting explicit information transfer requirements.

### Warnings

- None. All quality checks passed.

### Anchor Validation

- Parent anchor (IMPLEMENTS_NODE): 1 row (DEP-002-12-A01 -> SOW-0012). Confirmed in Decomposition Scope Ledger (SOW-0012 mapped to PKG-002, DEL-002-12).
- Trace anchors: 2 rows (OBJ-001, OBJ-003). Both confirmed in Decomposition Objectives section.

---

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Anchors | ACTIVE Execution | Total ACTIVE |
|---|---|---|---|---|---|---|---|
| 2026-03-26 | UPDATE | CONSERVATIVE | Available R2 SCA-001 (validated) | None | 3 | 14 | 17 |
| 2026-02-26 | UPDATE | CONSERVATIVE | Available (validated) | None | 3 | 14 | 17 |

---

## Lifecycle Summary

| Category | Count |
|---|---|
| Total rows | 17 |
| ACTIVE | 17 |
| RETIRED | 0 |
| Origin: EXTRACTED | 17 |
| Origin: DECLARED | 0 |

### SatisfactionStatus Breakdown (ACTIVE rows)

| Status | Count |
|---|---|
| TBD | 17 |
| PENDING | 0 |
| IN_PROGRESS | 0 |
| SATISFIED | 0 |

### EstimateImpactClass Breakdown (EXECUTION rows, ACTIVE)

| Class | Count |
|---|---|
| BLOCKING | 3 |
| ADVISORY | 11 |
| INFO | 0 |
| TBD | 0 |

---

## Downstream Handoff Notes (CONSUMER_CONTEXT: TASK_ESTIMATING)

### Blocking Dependencies for Estimating

The following 3 UPSTREAM dependencies are classified as BLOCKING for task estimating. These represent information gates where scope or key quantities cannot be established without the prerequisite being available:

1. **DEP-002-12-E01 -- DEL-008-01 (Geotechnical Investigation & Report):** Foundation-superstructure interface parameters (bearing pressure, frost depth, groundwater, soil classification) are unknown until the geotech report is available. Foundation design is variable-price scope per RFP 4.8.2. Superstructure design may be affected if geotechnical conditions are adverse.

2. **DEP-002-12-E06 -- DEL-002-01 (Preliminary Structural Design):** Explicit hold point: DEL-002-12 finalization (P.Eng. signing) shall not proceed until DEL-002-01 has received County approval. This gates the IFC specification and all downstream construction packages.

3. **DEP-002-12-E09 -- DEL-016-01 (Overhead Cranes -- manufacturer specs):** Crane manufacturer specifications (wheel loads, runway gauge, bridge span, CMAA service class) are described as an "irrefutable prerequisite" for crane runway structural design. Without these specs, crane support design cannot be finalized and the specification cannot be completed.

### Advisory Dependencies for Estimating

11 EXECUTION rows are classified ADVISORY. These represent interfaces and handovers that may affect quantities, specs, or procurement approach but do not hard-gate estimating readiness. Key items include:

- **Downstream interfaces to PKG-002 drawing set (DEL-002-02, DEL-002-03, DEL-002-10, DEL-002-11):** The specification governs performance requirements consumed by these deliverables. Changes in specification requirements will flow to drawing quantities.
- **Downstream handovers to construction packages (PKG-010, PKG-011):** The specification is a reference standard for construction execution.
- **Upstream interfaces from other disciplines (DEL-001-02, PKG-003, PKG-004, DEL-001-10):** Coordination inputs that may affect penetration locations, clearances, and renovation scope.
- **Downstream handover to PKG-009 (Permitting):** Specification is part of the IFC package submitted for building permit.

### Estimating Readiness Assessment

DEL-002-12 has 3 BLOCKING upstream dependencies with SatisfactionStatus = TBD. Estimating for this deliverable (and its downstream consumers) is constrained until at least the geotech report and preliminary design approval are resolved. Crane specification availability is a second-order constraint that may permit partial estimating with assumptions.
