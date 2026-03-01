# Dependencies: DEL-004-04 Lighting Plans

## Coordination (human-owned)
- **Mode:** NOT_TRACKED
- **Notes:** Coordination representation pending -- to be confirmed by human via ORCHESTRATOR.

## Upstream (I need these before I can proceed) -- human-owned declarations
- Dependencies coordinated externally by humans.

## Downstream (These need me) -- human-owned declarations
- Dependencies coordinated externally by humans.

## Extracted Dependency Register

- **Status:** COMPLETE
- **Dependencies.csv:** `Dependencies.csv` (v3.1 schema, 31 columns)
- **Total rows:** 18 (18 ACTIVE, 0 RETIRED)

### ANCHOR Dependencies (4 ACTIVE)

| DependencyID | AnchorType | TargetType | TargetRefID | Statement (abbreviated) | Confidence |
|---|---|---|---|---|---|
| DEP-004-04-001 | IMPLEMENTS_NODE | WBS_NODE | SOW-0014 | Implements SOW-0014: Complete final electrical design | HIGH |
| DEP-004-04-002 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-001 | Supports OBJ-001: Deliver code-compliant maintenance shop addition | HIGH |
| DEP-004-04-003 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-003 | Supports OBJ-003: Produce P.Eng.-stamped IFC documentation | HIGH |
| DEP-004-04-004 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-005 | Supports OBJ-005: Install/commission electrical and low-voltage systems | HIGH |

### EXECUTION Dependencies -- UPSTREAM (8 ACTIVE)

| DependencyID | DependencyType | TargetType | Target | Statement (abbreviated) | EstimateImpactClass |
|---|---|---|---|---|---|
| DEP-004-04-005 | PREREQUISITE | DELIVERABLE | DEL-004-01 (Preliminary Electrical Design) | County approval of preliminary design required before IFC issue | BLOCKING |
| DEP-004-04-006 | PREREQUISITE | DELIVERABLE | DEL-001-02 (Architectural Floor Plans) | Floor plans required for drawing background and dimension confirmation | BLOCKING |
| DEP-004-04-007 | INTERFACE | DELIVERABLE | DEL-002-03 (Structural Framing Plans) | Mounting point coordination at 35-foot ceiling | ADVISORY |
| DEP-004-04-008 | INTERFACE | DELIVERABLE | DEL-003-02 (HVAC Layout Plans) | Ceiling fan and exhaust fan location coordination | ADVISORY |
| DEP-004-04-009 | INTERFACE | DELIVERABLE | DEL-004-08 (Electrical Calculation Package) | Photometric calculations for illuminance verification | ADVISORY |
| DEP-004-04-010 | PREREQUISITE | DOCUMENT | R-05 (Appendix B -- Electrical) | Primary layout source for fixture inventory | INFO |
| DEP-004-04-011 | PREREQUISITE | DOCUMENT | R-01 (RFP) | Design requirements source (sections 3.3.2, 3.4) | INFO |
| DEP-004-04-018 | CONSTRAINT | EXTERNAL | AHJ | AHJ confirmation of applicable electrical codes | BLOCKING |

### EXECUTION Dependencies -- DOWNSTREAM (6 ACTIVE)

| DependencyID | DependencyType | TargetType | Target | Statement (abbreviated) | EstimateImpactClass |
|---|---|---|---|---|---|
| DEP-004-04-012 | INTERFACE | DELIVERABLE | DEL-004-03 (Power Distribution Plans) | Circuit ID coordination for circuit routing | ADVISORY |
| DEP-004-04-013 | INTERFACE | DELIVERABLE | DEL-004-06 (Panel Schedules) | Circuit ID coordination for breaker sizing and panel assignment | ADVISORY |
| DEP-004-04-014 | HANDOVER | DELIVERABLE | DEL-015-02 (Lighting Installation) | IFC Lighting Plans required before installation | BLOCKING |
| DEP-004-04-015 | HANDOVER | DELIVERABLE | DEL-009-03 (Safety Code Permits) | IFC Lighting Plans required for permit application | BLOCKING |
| DEP-004-04-016 | HANDOVER | DELIVERABLE | DEL-020-01 (Building Systems Commissioning) | Reference for commissioning | ADVISORY |
| DEP-004-04-017 | INTERFACE | DELIVERABLE | DEL-004-09 (Electrical Specification) | Product specification coordination for fixture types | ADVISORY |

---

## Run Notes

### Run Parameters
- **Timestamp:** 2026-02-26
- **MODE:** UPDATE
- **STRICTNESS:** CONSERVATIVE
- **CONSUMER_CONTEXT:** TASK_ESTIMATING
- **DECOMPOSITION_PATH:** `_Decomposition/WDMLRL_Decomposition_Claude.md` (available, validated)
- **RUN_ROOT:** `PKG-004_Electrical Design/1_Working/DEL-004-04_Lighting-Plans`

### Source Document Resolution
- **SOURCE_DOCS:** AUTO -- scanned deliverable folder, identified 4 source documents
- **ANCHOR_DOC:** `Datasheet.md` (AUTO -- selected by heuristic: contains `datasheet` in filename; contains Identification table with SOW/OBJ mappings)
- **EXECUTION_DOC_ORDER:** `Procedure.md`, `Guidance.md`, `Specification.md` (AUTO -- ordered by workflow clarity)
- **_REFERENCES.md:** Read-only, used for document pointer resolution (R-01, R-05)

### Defaults Applied
- All defaults from PROTOCOL applied without override.
- Decomposition available and used for anchor validation and target ID resolution.
- Extension columns (`EstimateImpactClass`, `ConsumerHint`) populated per TASK_ESTIMATING consumer context.

### Warnings
- None. All checks passed.

### Assumptions Recorded in Rows
- No ASSUMPTION-grade rows emitted (STRICTNESS=CONSERVATIVE). All rows are FACT-grade with explicit evidence.

### Notes on Mechanical Coordination Target
- Procedure prerequisites reference "DEL-003-02 or DEL-003-04" for mechanical coordination. DEL-003-02 (HVAC Layout Plans) was selected as the primary target because ceiling fan positions are most likely shown on the HVAC layout. DEL-003-04 (Exhaust System Plans) is also relevant but a single row was emitted to avoid duplication; the Notes field on DEP-004-04-008 records this.

---

## Run History

| Timestamp | Mode | Strictness | Consumer | Decomp Status | Warnings | ACTIVE Anchors | ACTIVE Execution | Total ACTIVE |
|---|---|---|---|---|---|---|---|---|
| 2026-02-26 | UPDATE | CONSERVATIVE | TASK_ESTIMATING | Available (validated) | None | 4 | 14 | 18 |

---

## Lifecycle Summary

### Extraction Lifecycle
- **ACTIVE:** 18
- **RETIRED:** 0

### Closure Lifecycle (SatisfactionStatus breakdown -- ACTIVE rows only)
- **PENDING:** 14
- **SATISFIED:** 2 (R-05 App B-Elec, R-01 RFP -- source documents already available)
- **NOT_APPLICABLE:** 2 (ANCHOR rows for SOW-0014 parent node; note: objective trace anchors also NOT_APPLICABLE)
- **TBD:** 0

### DependencyClass Breakdown
- **ANCHOR:** 4 (1 IMPLEMENTS_NODE, 3 TRACES_TO_REQUIREMENT)
- **EXECUTION:** 14 (8 UPSTREAM, 6 DOWNSTREAM)

### Tree x DAG Integrity
- Parent anchor (IMPLEMENTS_NODE): 1 ACTIVE -- OK
- No warnings.

---

## Downstream Handoff Notes

**Consumer context: TASK_ESTIMATING**

The following observations are relevant for downstream task estimating:

### BLOCKING Dependencies (affect estimating readiness)
1. **DEP-004-04-005 (DEL-004-01 Preliminary Electrical Design):** County approval of the preliminary electrical design is a hard gate before final IFC Lighting Plans can be issued. Estimating for this deliverable should account for the preliminary design approval cycle time.
2. **DEP-004-04-006 (DEL-001-02 Architectural Floor Plans):** Scaled architectural floor plans are required as the drawing background. Without these, only conceptual-level layout work can proceed. Estimating should note this as a prerequisite for full design effort.
3. **DEP-004-04-018 (AHJ Code Confirmation):** The Authority Having Jurisdiction must confirm the applicable CEC edition and Alberta amendments before code compliance can be verified. This gates the emergency/exit lighting scope determination (CONF-LT-003), which could add fixtures and design effort.
4. **DEP-004-04-014 (DEL-015-02 Lighting Installation):** This deliverable's IFC output is a hard gate for the electrical contractor's lighting installation work. Downstream estimating for PKG-015 should sequence after this deliverable.
5. **DEP-004-04-015 (DEL-009-03 Safety Code Permits):** IFC Lighting Plans are required for Safety Code permit application. Permitting timeline depends on this deliverable completion.

### ADVISORY Dependencies (may affect quantities or approach)
- Structural framing plans (DEL-002-03), mechanical layouts (DEL-003-02), and the electrical calculation package (DEL-004-08) provide coordination inputs that could affect fixture mounting details, layout adjustments, or photometric scope but are not hard gates for estimating the core lighting design work.
- Circuit coordination with Power Distribution Plans (DEL-004-03) and Panel Schedules (DEL-004-06) is bidirectional and represents a typical intra-package coordination pattern.

### Scope Uncertainty Flags for Estimating
- **Emergency/exit lighting (CONF-LT-003):** Whether emergency and exit lighting are required by Alberta Building Code is TBD. If required, additional fixtures, circuits, and potentially a separate life-safety drawing sheet would be added to this deliverable's scope. Estimating should carry a contingency for this potential scope addition.
- **Service pit fixtures (CONF-LT-002):** Fixture type, count, and specifications for the service pit are unresolved. This represents a minor scope uncertainty.
- **Wash bay fixture specs (CONF-LT-001):** Wattage and lumen output for wash bay high bay fixtures are TBD. This affects fixture schedule detail but not the overall fixture count (6 fixtures confirmed).
