# Dependencies: DEL-003-07 Mechanical Specification
## Coordination (human-owned)
- **Mode:** NOT_TRACKED
- **Notes:** Coordination representation pending -- to be confirmed by human via ORCHESTRATOR.

## Upstream (I need these before I can proceed) -- human-owned declarations
- Dependencies coordinated externally by humans.

## Downstream (These need me) -- human-owned declarations
- Dependencies coordinated externally by humans.

## Extracted Dependency Register

- **Status:** COMPLETE
- **Dependencies.csv:** `Dependencies.csv` (v3.1, 18 rows)
- **Schema Version:** v3.1

### Summary

| Category | Count |
|---|---|
| Total rows | 18 |
| ANCHOR rows | 3 |
| EXECUTION rows | 15 |
| ACTIVE | 18 |
| RETIRED | 0 |

### ANCHOR Edges (Tree -- Definition/Structure)

| DependencyID | AnchorType | TargetType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|---|
| DEP-003-07-001 | IMPLEMENTS_NODE | WBS_NODE | SOW-0013 | Complete final mechanical design (HVAC ventilation exhaust systems) | HIGH |
| DEP-003-07-002 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-003 | Produce complete P.Eng.-stamped IFC design documentation | HIGH |
| DEP-003-07-003 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-004 | Install and commission all mechanical plumbing and water storage systems | HIGH |

### EXECUTION Edges -- UPSTREAM (DAG -- Information Flow TO this deliverable)

| DependencyID | DependencyType | TargetType | Target | Confidence | EstimateImpactClass |
|---|---|---|---|---|---|
| DEP-003-07-004 | PREREQUISITE | DELIVERABLE | DEL-003-06 Mechanical Calculation Package | HIGH | BLOCKING |
| DEP-003-07-005 | PREREQUISITE | DELIVERABLE | DEL-003-05 Mechanical Equipment Schedule | HIGH | BLOCKING |
| DEP-003-07-006 | PREREQUISITE | DELIVERABLE | DEL-001-02 Architectural Floor Plans | HIGH | BLOCKING |
| DEP-003-07-007 | PREREQUISITE | PACKAGE | PKG-002 Structural Design | HIGH | BLOCKING |
| DEP-003-07-008 | INTERFACE | PACKAGE | PKG-004 Electrical Design | HIGH | ADVISORY |
| DEP-003-07-009 | INTERFACE | PACKAGE | PKG-006 Plumbing Design | MEDIUM | ADVISORY |
| DEP-003-07-010 | PREREQUISITE | DELIVERABLE | DEL-008-01 Site Geotechnical Report | MEDIUM | ADVISORY |
| DEP-003-07-011 | PREREQUISITE | DELIVERABLE | DEL-003-01 Preliminary Mechanical Design | MEDIUM | ADVISORY |
| DEP-003-07-012 | CONSTRAINT | DOCUMENT | RFP Section 3.4 Design Requirements | HIGH | INFO |
| DEP-003-07-017 | INTERFACE | PACKAGE | PKG-005 Civil Design | MEDIUM | ADVISORY |
| DEP-003-07-018 | CONSTRAINT | EXTERNAL | Alberta Safety Codes -- Mechanical | HIGH | INFO |

### EXECUTION Edges -- DOWNSTREAM (DAG -- Information Flow FROM this deliverable)

| DependencyID | DependencyType | TargetType | Target | Confidence | EstimateImpactClass |
|---|---|---|---|---|---|
| DEP-003-07-013 | HANDOVER | DELIVERABLE | DEL-003-02 HVAC Layout Plans | HIGH | ADVISORY |
| DEP-003-07-014 | HANDOVER | DELIVERABLE | DEL-003-03 Ductwork and Distribution Plans | HIGH | ADVISORY |
| DEP-003-07-015 | HANDOVER | DELIVERABLE | DEL-003-04 Exhaust System Plans | HIGH | ADVISORY |
| DEP-003-07-016 | HANDOVER | PACKAGE | PKG-013 Mechanical and HVAC Installation | HIGH | BLOCKING |

---

## Run Notes

### Run Parameters
- **Run Date:** 2026-02-26
- **MODE:** UPDATE
- **STRICTNESS:** CONSERVATIVE
- **CONSUMER_CONTEXT:** TASK_ESTIMATING
- **SCOPE:** DEL-003-07_Specification

### Source Document Selection (AUTO)
- **ANCHOR_DOC:** `Datasheet.md` (selected via DEFAULT heuristic: filename contains "datasheet"; highest-confidence definition/traceability signal)
- **EXECUTION_DOC_ORDER:**
  1. `Procedure.md` (selected via DEFAULT heuristic: filename contains "procedure"; highest workflow clarity)
  2. `Specification.md` (selected via DEFAULT heuristic: filename contains "spec"; strong execution signal)
  3. `Guidance.md` (selected via DEFAULT heuristic: filename contains "guidance"; supplementary execution context)
- **Excluded from scan:** `_DEPENDENCIES.md`, `_REFERENCES.md`, `_CONTEXT.md`, `_STATUS.md`, `_SEMANTIC.md`, `_SEMANTIC_LENSING.md` (generated/meta artifacts)

### Decomposition
- **Path:** `_Decomposition/WDMLRL_Decomposition_Claude.md`
- **Status:** Available. Anchor validation and label resolution performed successfully.
- **Decomposition Revision:** R1 -- 2026-02-25

### References
- **`_REFERENCES.md`:** Read. Used to confirm RFP document locations (`_Sources/` path prefix). No additional dependency rows emitted solely from references.

### Warnings
- None.

### Assumptions Logged
- DEP-003-07-011: County preliminary mechanical design approval gate is flagged as conditional (ASSUMPTION) per Procedure Step 9 and Datasheet Approval Conditions. Status TBD pending County confirmation.

### Decisions
- PKG-002 structural input (DEP-003-07-007) recorded as PACKAGE-level target rather than individual deliverables because Procedure prerequisites cite a range (DEL-002-02 to DEL-002-09) without specifying which specific structural deliverable is the gating input.
- Specification exclusions mentioning PKG-004 and PKG-006 coordination were captured as INTERFACE dependencies (not PREREQUISITE) because the source text describes data exchange rather than hard prerequisites.
- REQ-M-011 (coordination with plumbing for wash bay drainage) was captured as INTERFACE to PKG-006 rather than a separate coordination-only note, because the Specification explicitly states coordination is "required" for mud sump integration.
- General "coordination" statements (e.g., Guidance P-5) were NOT extracted as dependencies because they describe structural adjacency without specific artifact/data transfer.

---

## Run History

| Run | Date | Mode | Strictness | Decomposition | Warnings | ACTIVE Anchors | ACTIVE Execution | Total ACTIVE |
|---|---|---|---|---|---|---|---|---|
| 1 | 2026-02-26 | UPDATE | CONSERVATIVE | Available (R1 2026-02-25) | None | 3 | 15 | 18 |

---

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 18 |
| RETIRED | 0 |

### Satisfaction Status Breakdown (ACTIVE rows)

| SatisfactionStatus | Count |
|---|---|
| TBD | 9 |
| PENDING | 9 |

### Extraction Lifecycle

| Dimension | Value |
|---|---|
| FirstSeen (earliest) | 2026-02-26 |
| LastSeen (latest) | 2026-02-26 |

---

## Downstream Handoff Notes

**Consumer Context:** TASK_ESTIMATING

### Estimating-Critical Dependencies

The following EXECUTION dependencies have been assessed for estimating impact:

**BLOCKING (4 rows):** These dependencies gate meaningful estimating because scope or key quantities are unknown without them.
- **DEP-003-07-004** (UPSTREAM PREREQUISITE): DEL-003-06 Mechanical Calculation Package -- All specification performance values (heating capacity BTU/hr, ventilation volumes CFM, air balance) are TBD pending this deliverable. Estimating cannot establish mechanical equipment quantities or capacities without it.
- **DEP-003-07-005** (UPSTREAM PREREQUISITE): DEL-003-05 Mechanical Equipment Schedule -- Equipment model selections, quantities, and performance tiers feed directly into specification requirements. Estimating cannot price mechanical equipment without this.
- **DEP-003-07-006** (UPSTREAM PREREQUISITE): DEL-001-02 Architectural Floor Plans -- Equipment placement and spatial feasibility depend on final architectural layout. Room locations and dimensions affect mechanical scope.
- **DEP-003-07-016** (DOWNSTREAM HANDOVER): PKG-013 Mechanical and HVAC Installation -- This specification is the primary contractual reference for mechanical installation scope. PKG-013 estimating is blocked until this specification is finalized.

**ADVISORY (8 rows):** These dependencies are likely to change quantities, specs, or procurement approach but are not hard gates.
- DEP-003-07-007 (PKG-002 Structural Design), DEP-003-07-008 (PKG-004 Electrical Design), DEP-003-07-009 (PKG-006 Plumbing Design), DEP-003-07-010 (DEL-008-01 Geotechnical), DEP-003-07-011 (DEL-003-01 Preliminary Design), DEP-003-07-013/014/015 (companion drawing deliverables), DEP-003-07-017 (PKG-005 Civil Design).

**INFO (2 rows):** Informational context with low likelihood of changing totals.
- DEP-003-07-012 (RFP Section 3.4), DEP-003-07-018 (Alberta Safety Codes).

### Key Estimating Observations
1. DEL-003-07 has extensive TBD performance values (heating capacity, ventilation volumes, air change rates, capture velocities) that are all dependent on DEL-003-06 calculations. Estimating precision for this deliverable is limited until those calculations are complete.
2. The specification explicitly states it provides requirements for PKG-013 installation -- meaning PKG-013 scope estimating is downstream-blocked on this specification.
3. Five of seven technical standards in the Standards section are marked ASSUMPTION with "edition TBD" -- confirming these does not likely affect cost estimates but may affect compliance scope.
