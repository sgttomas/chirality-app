# DEL-013-03: Forced-Air Makeup System - Dependencies

## Dependency Status
**Tracking Status**: TRACKED
**Register**: Dependencies.csv (v3.1)

## External Dependencies
- DEL-012-02: Utility Room completion (equipment housing)
- Fresh air intake location finalization
- Supply ductwork routing through building
- Mechanical Contractor availability

## Internal Package Dependencies
- **DEL-013-01** (Heating System): Heating of makeup air
- **DEL-013-02** (Air Exchanger): Coordination with primary ventilation
- **DEL-013-04** (Equipment Exhaust): Makeup air balances equipment exhaust
- **DEL-013-05** (Welding Exhaust): Makeup air balances welding exhaust
- **DEL-013-06** (Ceiling Fans): Distribution support

## Critical Integration Points
- Fresh air intake coordinate with exchanger intake
- Heated air supply coordination
- Supply ductwork routing avoids conflicts
- Makeup air volume balances exhaust volumes
- Control dampers coordinate with other systems

## Constraint Notes
- Makeup volume must match exhaust volumes
- Fresh air quality critical for safety and comfort
- Supply ductwork must reach all facility areas
- Controls must prevent excessive pressurization
- Heating capacity must handle makeup air volume

## Dependency Map
```
DEL-012-02 (Utility) --> DEL-013-03 (Makeup Air)
DEL-013-01 (Heating) \                / DEL-013-02 (Exchanger)
                      \            /
                    DEL-013-04 & 05 (Exhaust)
```

---

## Extracted Dependency Register

**Total ACTIVE rows:** 16
**ANCHOR rows:** 3 (1 IMPLEMENTS_NODE, 2 TRACES_TO_REQUIREMENT)
**EXECUTION rows:** 13 (9 PREREQUISITE, 3 INTERFACE, 1 CONSTRAINT)

| DependencyID | Class | AnchorType | Dir | Type | TargetType | Target | Confidence |
|---|---|---|---|---|---|---|---|
| DEP-013-03-A01 | ANCHOR | IMPLEMENTS_NODE | UPSTREAM | OTHER | WBS_NODE | SOW-0037 | HIGH |
| DEP-013-03-A02 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | REQUIREMENT | OBJ-001 | HIGH |
| DEP-013-03-A03 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | REQUIREMENT | OBJ-004 | HIGH |
| DEP-013-03-E01 | EXECUTION | N/A | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-003-02 (HVAC Plans) | HIGH |
| DEP-013-03-E02 | EXECUTION | N/A | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-003-03 (Ductwork Plans) | HIGH |
| DEP-013-03-E03 | EXECUTION | N/A | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-003-05 (Equipment Schedule) | HIGH |
| DEP-013-03-E04 | EXECUTION | N/A | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-003-06 (Calculation Package) | HIGH |
| DEP-013-03-E05 | EXECUTION | N/A | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-003-07 (Mechanical Spec) | HIGH |
| DEP-013-03-E06 | EXECUTION | N/A | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-012-02 (Utility Room) | HIGH |
| DEP-013-03-E07 | EXECUTION | N/A | UPSTREAM | INTERFACE | DELIVERABLE | DEL-013-01 (Heating System) | HIGH |
| DEP-013-03-E08 | EXECUTION | N/A | UPSTREAM | INTERFACE | DELIVERABLE | DEL-013-02 (Air Exchanger) | HIGH |
| DEP-013-03-E09 | EXECUTION | N/A | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-013-04 (Equipment Exhaust) | HIGH |
| DEP-013-03-E10 | EXECUTION | N/A | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-013-05 (Welding Exhaust) | HIGH |
| DEP-013-03-E11 | EXECUTION | N/A | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-018-06 (Utility Tie-Ins) | MEDIUM |
| DEP-013-03-E12 | EXECUTION | N/A | UPSTREAM | INTERFACE | DELIVERABLE | DEL-015-04 (Equipment Power) | MEDIUM |
| DEP-013-03-E13 | EXECUTION | N/A | UPSTREAM | CONSTRAINT | DELIVERABLE | DEL-016-01 (Overhead Cranes) | HIGH |

---

## Run Notes

### Run: 2026-02-26

**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer Context:** TASK_ESTIMATING
**Decomposition Path:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/_Decomposition/WDMLRL_Decomposition_Claude.md
**Decomposition Status:** AVAILABLE -- used for anchor validation and target resolution.

**Source Documents Scanned:**
- ANCHOR_DOC: Datasheet.md (contains Identification with SOW Reference and Objective Linkage)
- EXECUTION_DOCS (in order): Procedure.md, Specification.md, Guidance.md, Datasheet.md
- Read-only inputs: _CONTEXT.md, _REFERENCES.md, _DEPENDENCIES.md (original declared lists)

**Defaults Applied:**
- SOURCE_DOCS: AUTO -- all four production documents scanned (Datasheet.md, Guidance.md, Procedure.md, Specification.md)
- DOC_ROLE_MAP: DEFAULT -- Datasheet.md matched ANCHOR_DOC; Procedure.md, Specification.md, Guidance.md matched EXECUTION_DOC
- ANCHOR_DOC: AUTO -- selected Datasheet.md (contains explicit SOW Reference and Objective Linkage fields)
- EXECUTION_DOC_ORDER: AUTO -- Procedure.md (explicit prerequisite table), Specification.md (requirements with dependency references), Guidance.md (principles and considerations), Datasheet.md (attribute cross-references)

**Extraction Decisions:**
- DEL-013-06 (Ceiling Fans): Listed in _DEPENDENCIES.md Internal Package Dependencies as "Distribution support." No explicit information/artifact transfer found in any source document. Omitted per information-flow-only rule. FACT: purely coordination/adjacency.
- DEL-003-09 (Controls Design): Referenced in Procedure Step 4.3 as "ASSUMPTION: controls design deliverable." Does not exist in decomposition. Not registered as a dependency. Noted as ASSUMPTION in Procedure.md.
- Building envelope prerequisite (Guidance C1, Procedure PRE-08): "Building envelope substantially complete" is stated in Procedure PRE-08, but the specific upstream deliverable is not identified (no deliverable ID for building envelope in context). Not registered because target cannot be resolved to a specific deliverable. CONSERVATIVE.
- Mechanical permit (Procedure PRE-06): An administrative prerequisite (not an information/artifact transfer from another deliverable). Not registered as a deliverable dependency.
- DEL-013-01, DEL-013-02: Bidirectional interfaces exist. Registered as UPSTREAM INTERFACE since the primary information need is from those deliverables TO DEL-013-03 (heating integration parameters, intake location data, controls interlock specs). The reverse direction (MUA volume data feeding heating sizing) is captured implicitly in the interface statement.
- DEL-013-04, DEL-013-05: Registered as UPSTREAM PREREQUISITE because exhaust volume data is a required input that gates MUA sizing (Guidance P1, Datasheet BLOCKING TBD).
- DEL-018-06 (SOW-0080 natural gas): Registered at MEDIUM confidence because gas-fired MUA is an ASSUMPTION.
- DEL-015-04 (Equipment Power): Registered at MEDIUM confidence; Procedure Step 4.2 explicitly references "DEL-015" but the specific sub-deliverable (DEL-015-04 Equipment Power Circuits) is inferred from decomposition mapping.

**Warnings:** None.

---

## Run History

| Run Date | Mode | Strictness | Consumer | Decomposition | Warnings | ANCHOR Active | EXECUTION Active | Total Active |
|---|---|---|---|---|---|---|---|---|
| 2026-02-26 | UPDATE | CONSERVATIVE | TASK_ESTIMATING | AVAILABLE | None | 3 | 13 | 16 |

---

## Lifecycle Summary

**Extraction Lifecycle:**
- ACTIVE: 16
- RETIRED: 0

**Closure Lifecycle (ACTIVE rows only):**
- SatisfactionStatus TBD: 6 (3 ANCHOR + 3 EXECUTION -- interfaces/constraint where satisfaction is not yet assessable)
- SatisfactionStatus PENDING: 10 (EXECUTION prerequisites awaiting design deliverables and construction readiness)
- SatisfactionStatus SATISFIED: 0
- SatisfactionStatus WAIVED: 0
- SatisfactionStatus NOT_APPLICABLE: 0

---

## Downstream Handoff Notes

**Consumer Context: TASK_ESTIMATING**

The following observations are relevant for downstream task estimating:

1. **BLOCKING dependencies (6 rows, EstimateImpactClass=BLOCKING):** DEL-013-03 cannot be meaningfully estimated for scope quantities (airflow rate, duct sizing, equipment capacity, heating load) until the following design deliverables are available:
   - DEL-003-06 (Mechanical Calculation Package) -- establishes the fundamental design parameter: required supply airflow rate. This is the single most critical blocking input.
   - DEL-003-05 (Mechanical Equipment Schedule) -- confirms MUA unit make/model/capacity.
   - DEL-003-07 (Mechanical Specification) -- governs installation standards, insulation, duct leakage class.
   - DEL-003-02 and DEL-003-03 (IFC HVAC and Ductwork Plans) -- required before procurement and installation.
   - DEL-012-02 (Utility Room) -- physical prerequisite for equipment setting.

2. **Exhaust volume dependencies (2 rows, BLOCKING):** DEL-013-04 and DEL-013-05 exhaust volume data is a required input for MUA sizing per Specification REQ-013-03-02 and Guidance P1. These may also be TBD pending DEL-003-06.

3. **ADVISORY dependencies (5 rows):** Interfaces with DEL-013-01 (heating), DEL-013-02 (air exchanger), DEL-015-04 (electrical power), DEL-016-01 (crane clearance), and DEL-018-06 (natural gas) are likely to affect quantities, specs, or procurement approach but are not hard gates for estimating.

4. **Key TBD values impacting estimates:** Required supply airflow rate, design outdoor air temperature, MUA unit make/model, ductwork insulation specification, duct leakage class, maximum building pressurization limit, minimum supply air temperature. All are pending DEL-003 series design deliverables.

5. **Assumption risk:** Gas-fired MUA (ASSUMPTION) drives the DEL-018-06 natural gas dependency. If the MUA uses electric or indirect heating instead, this dependency changes.
