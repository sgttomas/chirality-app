# Dependencies: DEL-004-03 Power Distribution Plans

## Coordination (human-owned)
- **Mode:** NOT_TRACKED
- **Notes:** Coordination representation pending — to be confirmed by human via ORCHESTRATOR.

## Upstream (I need these before I can proceed) — human-owned declarations
- Dependencies coordinated externally by humans.

## Downstream (These need me) — human-owned declarations
- Dependencies coordinated externally by humans.

## Extracted Dependency Register

- **Status:** COMPLETE
- **Dependencies.csv:** `Dependencies.csv` (v3.1 schema, 22 rows: 4 ANCHOR + 18 EXECUTION)
- **Summary:**

### ANCHOR Rows (4 ACTIVE)

| DependencyID | AnchorType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|
| DEP-004-03-A01 | IMPLEMENTS_NODE | SOW-0014 | Complete final electrical design | HIGH |
| DEP-004-03-A02 | TRACES_TO_REQUIREMENT | OBJ-001 | Deliver a code-compliant fully functional maintenance shop | HIGH |
| DEP-004-03-A03 | TRACES_TO_REQUIREMENT | OBJ-003 | Produce complete P.Eng.-stamped IFC design documentation | HIGH |
| DEP-004-03-A04 | TRACES_TO_REQUIREMENT | OBJ-005 | Install and commission all electrical and low-voltage systems | HIGH |

### EXECUTION Rows (18 ACTIVE)

| DependencyID | Direction | Type | TargetType | Target | Confidence | EstimateImpact |
|---|---|---|---|---|---|---|
| DEP-004-03-E01 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-004-01 Preliminary Electrical Design | HIGH | BLOCKING |
| DEP-004-03-E02 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-004-02 Single-Line Diagram | HIGH | BLOCKING |
| DEP-004-03-E03 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-001-02 Architectural Floor Plans | HIGH | BLOCKING |
| DEP-004-03-E04 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-002-03 Structural Framing Plans | HIGH | ADVISORY |
| DEP-004-03-E05 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-003-05 Mechanical Equipment Schedule | HIGH | BLOCKING |
| DEP-004-03-E06 | UPSTREAM | PREREQUISITE | EXTERNAL | Crane supplier specifications (PKG-016) | HIGH | BLOCKING |
| DEP-004-03-E07 | UPSTREAM | PREREQUISITE | EXTERNAL | Utility service information (ATCO Electric) | HIGH | BLOCKING |
| DEP-004-03-E08 | UPSTREAM | PREREQUISITE | EXTERNAL | County welding equipment specifications | MEDIUM | ADVISORY |
| DEP-004-03-E09 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-004-08 Electrical Calculation Package | HIGH | BLOCKING |
| DEP-004-03-E10 | DOWNSTREAM | HANDOVER | PACKAGE | PKG-015 Electrical & Low-Voltage Installation | HIGH | INFO |
| DEP-004-03-E11 | UPSTREAM | INTERFACE | PACKAGE | PKG-006 Plumbing Design | MEDIUM | ADVISORY |
| DEP-004-03-E12 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-001-07 Door and Window Schedule | HIGH | ADVISORY |
| DEP-004-03-E13 | UPSTREAM | PREREQUISITE | EXTERNAL | Alberta Safety Code permit application requirements | MEDIUM | ADVISORY |
| DEP-004-03-E14 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-009-03 Safety Code Permits | HIGH | INFO |
| DEP-004-03-E15 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-004-04 Lighting Plans | HIGH | ADVISORY |
| DEP-004-03-E16 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-004-05 Receptacle Layout Plans | HIGH | ADVISORY |
| DEP-004-03-E17 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-004-06 Panel Schedules | HIGH | ADVISORY |
| DEP-004-03-E18 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-004-09 Electrical Specification | MEDIUM | INFO |

---

## Run Notes

### Run 2026-02-26 (current)

**Parameters:**
- SCOPE: DEL-004-03_Power-Plans
- MODE: UPDATE
- STRICTNESS: CONSERVATIVE
- CONSUMER_CONTEXT: TASK_ESTIMATING
- DECOMPOSITION_PATH: `_Decomposition/WDMLRL_Decomposition_Claude.md` (R1, 2026-02-25) -- located and validated
- SOURCE_DOCS: AUTO -- resolved to: Datasheet.md, Specification.md, Procedure.md, Guidance.md
- ANCHOR_DOC: AUTO -- resolved to: Datasheet.md (contains Identification section with SOW/OBJ references)
- EXECUTION_DOC_ORDER: AUTO -- resolved to: Procedure.md, Specification.md, Guidance.md (by workflow clarity)

**Defaults applied:**
- DOC_ROLE_MAP: DEFAULT heuristic used. Datasheet.md matched ANCHOR_DOC pattern ("datasheet"). Procedure.md matched EXECUTION_DOC primary ("procedure"). Specification.md and Guidance.md matched EXECUTION_DOC secondary ("spec", "guidance").
- _REFERENCES.md: Read; used to confirm R-01 and R-05 accessibility status; no additional dependency rows emitted solely from references.

**Assumptions:**
- ASSUMPTION: TargetType=PACKAGE used for PKG-015 and PKG-006 where the source text references the package rather than a specific deliverable.
- ASSUMPTION: DEP-004-03-E10 TargetType changed from DELIVERABLE to PACKAGE to reflect that the handover is to the package (PKG-015) not a specific deliverable within it. The source text says "PKG-015 Electrical & Low-Voltage Installation."
- ASSUMPTION: DEP-004-03-E11 TargetType changed from DELIVERABLE to PACKAGE for same reason (source references "PKG-006" generically).

**Warnings:**
- None. All quality checks passed.

**New rows added in this run (vs. prior extraction):**
- DEP-004-03-E13: Alberta Safety Code permit application requirements (EXTERNAL PREREQUISITE) -- was listed in Procedure prerequisites table but missing from prior extraction.
- DEP-004-03-E14: DEL-009-03 Safety Code Permits (DOWNSTREAM HANDOVER) -- Procedure Step 7.2 explicitly references submission to AHJ as part of DEL-009-03.
- DEP-004-03-E15: DEL-004-04 Lighting Plans (UPSTREAM INTERFACE) -- Specification and Procedure Step 4.3 require explicit coordination/cross-check.
- DEP-004-03-E16: DEL-004-05 Receptacle Layout Plans (UPSTREAM INTERFACE) -- Specification and Procedure Step 4.2 require explicit coordination/cross-check.
- DEP-004-03-E17: DEL-004-06 Panel Schedules (UPSTREAM INTERFACE) -- Specification and Procedure Step 4.4 require explicit coordination/cross-check.
- DEP-004-03-E18: DEL-004-09 Electrical Specification (UPSTREAM INTERFACE) -- Specification Related Deliverables explicitly states it governs materials/workmanship.

**Corrections to prior rows:**
- DEP-004-03-E10: TargetType corrected from DELIVERABLE to PACKAGE (source references PKG-015 not a specific deliverable).
- DEP-004-03-E11: TargetType corrected from DELIVERABLE to PACKAGE (source references PKG-006 generically).
- Notes fields enriched with decomposition validation and cross-references.

---

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Anchors | ACTIVE Execution | Total ACTIVE |
|---|---|---|---|---|---|---|---|
| 2026-02-26 | UPDATE | CONSERVATIVE | _Decomposition/WDMLRL_Decomposition_Claude.md (R1) | None | 4 | 18 | 22 |

---

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 22 |
| RETIRED | 0 |

### By DependencyClass

| Class | ACTIVE | RETIRED |
|---|---|---|
| ANCHOR | 4 | 0 |
| EXECUTION | 18 | 0 |

### Closure-State Breakdown (ACTIVE rows)

| SatisfactionStatus | Count |
|---|---|
| PENDING | 16 |
| TBD | 6 |

**Notes:** ANCHOR rows (4) have SatisfactionStatus=TBD (traceability links are structural, not "satisfied" in the execution sense). DOWNSTREAM HANDOVER rows (E10, E14) have SatisfactionStatus=TBD (output not yet produced). Remaining 16 EXECUTION UPSTREAM rows are PENDING as the project is in pre-construction design phase.

---

## Downstream Handoff Notes

**Consumer context: TASK_ESTIMATING**

The following observations are provided for downstream estimating workflows:

### Blocking Dependencies (EstimateImpactClass=BLOCKING)

These dependencies gate meaningful estimating because scope, quantities, or key technical parameters cannot be finalized without them:

1. **DEP-004-03-E01** (DEL-004-01 Preliminary Electrical Design) -- County approval gates IFC release; no final scope lock without it.
2. **DEP-004-03-E02** (DEL-004-02 Single-Line Diagram) -- System-level electrical architecture must be established for power plan scope to be firm.
3. **DEP-004-03-E03** (DEL-001-02 Architectural Floor Plans) -- Drawing underlay is mandatory; building dimensions drive conduit lengths and circuit routing quantities.
4. **DEP-004-03-E05** (DEL-003-05 Mechanical Equipment Schedule) -- Motor ratings for HVAC/exhaust equipment are unknown without this; affects panel sizing and feeder quantities.
5. **DEP-004-03-E06** (Crane supplier specifications) -- Crane circuit ratings TBD; affects panel capacity and conductor sizing.
6. **DEP-004-03-E07** (Utility service information) -- Service voltage (120/208V vs 347/600V) changes all panelboard and wiring specifications. Procedure Step 1A creates an explicit gate.
7. **DEP-004-03-E09** (DEL-004-08 Electrical Calculation Package) -- Panel sizes and feeder sizes derive from load calculation; estimating conductor quantities without this is unreliable.

### Advisory Dependencies (EstimateImpactClass=ADVISORY)

These may change quantities or specifications but do not hard-gate estimating:

1. **DEP-004-03-E04** (DEL-002-03 Structural Framing Plans) -- Conduit penetration coordination may affect routing quantities.
2. **DEP-004-03-E08** (County welding equipment specifications) -- If actual welding equipment differs from 50A/240V assumption, receptacle circuits and panel sizing may change.
3. **DEP-004-03-E11** (PKG-006 Plumbing Design) -- Plumbing equipment electrical feeds may add circuits not currently counted.
4. **DEP-004-03-E12** (DEL-001-07 Door and Window Schedule) -- Overhead door count is TBD; each door operator adds a circuit.
5. **DEP-004-03-E13** (Alberta Safety Code permit requirements) -- May affect drawing content or process but unlikely to change material quantities significantly.
6. **DEP-004-03-E15** (DEL-004-04 Lighting Plans) -- Lighting circuit count coordination; quantities are substantially known from App B Electrical.
7. **DEP-004-03-E16** (DEL-004-05 Receptacle Layout Plans) -- Receptacle locations and circuit assignments; quantities substantially known from App B Electrical.
8. **DEP-004-03-E17** (DEL-004-06 Panel Schedules) -- Coordination deliverable; unlikely to change total quantities.

### Key Estimating Risks

- **Service voltage uncertainty** (CONF-003-02) is the single largest estimating risk: 120/208V vs 347/600V changes conductor sizes, panelboard specifications, and potentially transformer requirements.
- **Crane circuit ratings** are TBD pending supplier specifications from PKG-016; conservative assumptions may be used but carry rework risk.
- **Overhead door count** is TBD pending DEL-001-07; each powered door adds an operator circuit.
- **Mechanical equipment electrical loads** are TBD pending DEL-003-05; affects panel capacity reserves.
