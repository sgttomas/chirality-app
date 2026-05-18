# Dependencies: DEL-003-04 Exhaust System Plans

## Coordination (human-owned)
- **Mode:** NOT_TRACKED
- **Notes:** Coordination representation pending -- to be confirmed by human via ORCHESTRATOR.

## Upstream (I need these before I can proceed) -- human-owned declarations
- Dependencies coordinated externally by humans.

## Downstream (These need me) -- human-owned declarations
- Dependencies coordinated externally by humans.

## Extracted Dependency Register

- **Status:** POPULATED
- **Dependencies.csv:** Dependencies.csv (27 rows, 27 ACTIVE, 0 RETIRED)
- **RegisterSchemaVersion:** v3.1

### Summary by Class

| DependencyClass | Count |
|---|---|
| ANCHOR | 10 |
| EXECUTION | 17 |
| **Total** | **27** |

### ANCHOR Rows (10)

| DependencyID | AnchorType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|
| DEP-003-04-001 | IMPLEMENTS_NODE | SOW-0013 | Complete final mechanical design (HVAC ventilation exhaust systems) | HIGH |
| DEP-003-04-002 | TRACES_TO_REQUIREMENT | SOW-0028 | Construct ventilated and lighted service pit | HIGH |
| DEP-003-04-003 | TRACES_TO_REQUIREMENT | SOW-0036 | Install high-volume air exchanger | HIGH |
| DEP-003-04-004 | TRACES_TO_REQUIREMENT | SOW-0038 | Install exhaust hoses and fans for heavy equipment in repair bays | HIGH |
| DEP-003-04-005 | TRACES_TO_REQUIREMENT | SOW-0039 | Install welding station ventilation/exhaust system | HIGH |
| DEP-003-04-006 | TRACES_TO_REQUIREMENT | SOW-0040 | Install 6 ceiling fans in main shop area | HIGH |
| DEP-003-04-007 | TRACES_TO_REQUIREMENT | SOW-0066 | Install exhaust fan(s) as shown on electrical drawing | HIGH |
| DEP-003-04-008 | TRACES_TO_REQUIREMENT | OBJ-001 | Deliver a code-compliant, fully functional maintenance shop | HIGH |
| DEP-003-04-009 | TRACES_TO_REQUIREMENT | OBJ-003 | Produce complete P.Eng.-stamped IFC design documentation | HIGH |
| DEP-003-04-010 | TRACES_TO_REQUIREMENT | OBJ-004 | Install and commission all mechanical systems to operational readiness | HIGH |

### EXECUTION Rows -- UPSTREAM (12)

| DependencyID | DependencyType | TargetType | TargetDeliverableID / TargetName | EstimateImpactClass |
|---|---|---|---|---|
| DEP-003-04-011 | PREREQUISITE | DELIVERABLE | DEL-003-01 Preliminary Mechanical Design | BLOCKING |
| DEP-003-04-012 | PREREQUISITE | DELIVERABLE | DEL-003-06 Mechanical Calculation Package | BLOCKING |
| DEP-003-04-013 | PREREQUISITE | DELIVERABLE | DEL-002-06 Service Pit Structural Details | BLOCKING |
| DEP-003-04-014 | PREREQUISITE | DELIVERABLE | DEL-002-07 Crane Support Structure Details | ADVISORY |
| DEP-003-04-015 | INTERFACE | DELIVERABLE | DEL-001-02 Architectural Floor Plans | ADVISORY |
| DEP-003-04-016 | INTERFACE | DELIVERABLE | DEL-004-03 Power Distribution Plans | ADVISORY |
| DEP-003-04-017 | INTERFACE | DELIVERABLE | DEL-003-02 HVAC Layout Plans | ADVISORY |
| DEP-003-04-018 | INTERFACE | DELIVERABLE | DEL-003-03 Ductwork & Distribution Plans | ADVISORY |
| DEP-003-04-019 | INTERFACE | DELIVERABLE | DEL-003-07 Mechanical Specification | INFO |
| DEP-003-04-020 | CONSTRAINT | DOCUMENT | R-01 AB-2026-01424-WDMLRL RFP.pdf | BLOCKING |
| DEP-003-04-021 | CONSTRAINT | DOCUMENT | R-04 AB-2026-01424-Appendix B (Shop).pdf | BLOCKING |
| DEP-003-04-027 | CONSTRAINT | EXTERNAL | Alberta Building Code and Safety Codes | ADVISORY |

### EXECUTION Rows -- DOWNSTREAM (5)

| DependencyID | DependencyType | TargetType | TargetDeliverableID / TargetName | EstimateImpactClass |
|---|---|---|---|---|
| DEP-003-04-022 | HANDOVER | DELIVERABLE | DEL-013-04 Heavy Equipment Exhaust System Installation | BLOCKING |
| DEP-003-04-023 | HANDOVER | DELIVERABLE | DEL-013-05 Welding Station Exhaust System Installation | BLOCKING |
| DEP-003-04-024 | HANDOVER | DELIVERABLE | DEL-003-05 Mechanical Equipment Schedule | ADVISORY |
| DEP-003-04-025 | HANDOVER | DELIVERABLE | DEL-009-02 Building Permit Application & Approval | ADVISORY |
| DEP-003-04-026 | HANDOVER | DELIVERABLE | DEL-009-03 Safety Code Permits | ADVISORY |

---

## Run Notes

### Run 2026-02-26 (Initial Extraction)

**Run Parameters:**
- MODE: UPDATE
- STRICTNESS: CONSERVATIVE
- CONSUMER_CONTEXT: TASK_ESTIMATING
- SCOPE: DEL-003-04_Exhaust-Plans

**Paths Used:**
- RUN_ROOT: `PKG-003_Mechanical Design/1_Working/DEL-003-04_Exhaust-Plans/`
- DECOMPOSITION_PATH: `_Decomposition/WDMLRL_Decomposition_Claude.md` (R1 -- 2026-02-25) -- AVAILABLE, used for anchor validation and target resolution
- SOURCE_DOCS (AUTO): `Datasheet.md`, `Guidance.md`, `Specification.md`, `Procedure.md`
- ANCHOR_DOC (AUTO): `Datasheet.md` (matched heuristic: "datasheet" keyword; contains Identification table with SOW/OBJ fields)
- EXECUTION_DOC_ORDER (AUTO): `Procedure.md`, `Guidance.md`, `Specification.md` (Procedure matched highest for workflow clarity)
- _REFERENCES.md: AVAILABLE, used for document target resolution (R-01, R-04 paths)

**Defaults Applied:**
- DOC_ROLE_MAP: DEFAULT heuristic applied. Datasheet.md matched ANCHOR_DOC. Procedure.md, Guidance.md matched EXECUTION_DOC.
- All SOW and OBJ identifiers validated against Decomposition S3 (SSOW), S5 (Objectives), S7 (Deliverables by Package).
- All target deliverable IDs validated against Decomposition S7.

**Warnings:**
- (none)

**Integrity Checks:**
- Parent anchor (IMPLEMENTS_NODE): 1 found (DEP-003-04-001, SOW-0013). PASS.
- DependencyID uniqueness: PASS (27 unique IDs).
- All ACTIVE rows have EvidenceFile + SourceRef: PASS.
- FromDeliverableID = DEL-003-04 for all rows: PASS.
- Enum values canonical: PASS.
- CSV parseable: PASS (27 rows, 31 columns).
- _DEPENDENCIES.md counts match Dependencies.csv: PASS.

**Assumptions Recorded:**
- ANCHOR rows use `TargetType=WBS_NODE` for both SOW items and OBJ items since these are definition-tree nodes, not formal REQUIREMENT-type entries. This follows the Decomposition's structure where SOW items and OBJ items are the canonical definition nodes.
- `EstimateImpactClass` and `ConsumerHint` populated for EXECUTION rows per CONSUMER_CONTEXT=TASK_ESTIMATING. Conservative assignment: BLOCKING only for explicit prerequisites/constraints that gate meaningful estimating.

---

## Run History

| Timestamp | Mode | Strictness | Consumer | Decomposition | Warnings | ANCHOR Active | EXECUTION Active | Total Active |
|---|---|---|---|---|---|---|---|---|
| 2026-02-26 | UPDATE | CONSERVATIVE | TASK_ESTIMATING | AVAILABLE (R1 2026-02-25) | (none) | 10 | 17 | 27 |

---

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 27 |
| RETIRED | 0 |

| SatisfactionStatus | Count |
|---|---|
| TBD | 10 |
| PENDING | 17 |

**Notes:**
- ANCHOR rows have `SatisfactionStatus=TBD` because anchor traceability satisfaction is a project-level assessment.
- EXECUTION rows have `SatisfactionStatus=PENDING` because the upstream inputs and downstream handovers are not yet fulfilled (design is in progress).

---

## Downstream Handoff Notes

**Consumer Context: TASK_ESTIMATING**

The following observations are relevant for downstream task estimating workflows:

1. **BLOCKING upstream dependencies (3 deliverable, 2 document):**
   - DEL-003-01 (Preliminary Mechanical Design): County approval gates IFC. Estimating cannot finalize exhaust system scope until preliminary design concept is approved.
   - DEL-003-06 (Mechanical Calculation Package): Fan sizing and airflow calculations drive equipment selection and quantities. Estimating requires at least preliminary calculation results to size equipment and ductwork.
   - DEL-002-06 (Service Pit Structural Details): Pit dimensions are TBD and required for service pit ventilation design. Without these, the pit ventilation subsystem cannot be estimated.
   - R-01 (RFP) and R-04 (Conceptual Floor Plan): These are available and do not gate estimating.

2. **ADVISORY upstream dependencies (6):**
   - DEL-002-07 (Crane Support Details): Crane clearances affect duct routing but do not gate scope definition.
   - DEL-001-02 (Architectural Floor Plans): Wall/ceiling routing affects duct lengths but not system scope.
   - DEL-004-03 (Power Distribution Plans): Fan motor electrical characteristics affect coordination but not mechanical scope.
   - DEL-003-02 (HVAC Plans): Air balance coordination affects system sizing but preliminary estimates can proceed.
   - DEL-003-03 (Ductwork Plans): Scope boundary (CFT-001/CFT-003) affects whether exhaust ductwork is in DEL-003-04 or DEL-003-03. Unresolved conflict; estimate should include exhaust-specific ductwork per the PROPOSAL in Guidance CFT-001.
   - Alberta Building Code / Safety Codes: Code editions TBD; unlikely to change system scope significantly.

3. **BLOCKING downstream handovers (2):**
   - DEL-013-04 and DEL-013-05 (mechanical installation deliverables) cannot proceed without DEL-003-04 IFC drawings. Installation estimating for these deliverables depends on design completion.

4. **Key estimating risks from dependency register:**
   - Wash bay exhaust scope boundary (CFT-001/B-003) is unresolved. Estimate should include wash bay exhaust as in scope of DEL-003-04 per the PROPOSAL, but flag as a scope risk.
   - Service pit dimensions (B-001) are TBD from DEL-002-06. Pit ventilation quantities cannot be finalized without these.
   - R-05 (electrical drawing) data gap (CFT-002/E-003) may affect exhaust fan counts and locations.
