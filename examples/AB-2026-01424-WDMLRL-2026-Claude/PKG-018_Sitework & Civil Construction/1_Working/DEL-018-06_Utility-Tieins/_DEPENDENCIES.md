# DEL-018-06_Utility-Tieins | Dependencies

## Dependency Tracking Status
**Tracking Status**: TRACKED
**Register Schema**: v3.1
**Last Run**: 2026-03-26

## Dependency Framework

### Upstream Dependencies
Dependencies that must be satisfied before this deliverable can proceed:

| Dependency ID | Description | Status | Notes |
|---------------|-------------|--------|-------|
| UTILITY-COORD-001 | Utility provider coordination | Pending | Must engage gas, electrical, communications providers |
| DESIGN-001 | Utility routing design complete | Pending | Route planning and connection points |
| PERMITS-001 | Utility permits and approvals | Pending | Government and utility provider approvals |
| CAPACITY-001 | Utility capacity verification | Pending | Confirm available service capacity |
| SITE-PREP-001 | Site preparation (grading) | Pending | Access for trenching and installation |

### Downstream Dependencies
Deliverables that depend on completion of this deliverable:

| Dependent ID | Description | Status | Notes |
|--------------|-------------|--------|-------|
| FACILITY-OPS-001 | Facility full operational capability | Pending | Utilities required for all operations |
| PKG-017-INTERIOR | Building interior systems | Pending | Building utilities depend on site connections |
| PKG-016-CRANES | Crane electrical supply | Pending | Electrical tie-in required for crane operation |

## Critical Path Assessment
- **On Critical Path**: YES
- **Justification**: Utility tie-ins are absolutely critical for facility operations; essential for project completion and facility viability

## Dependency Management Notes
- Dependencies tracked at deliverable level within PKG-018
- Early utility provider engagement is critical - long lead times common
- Permit acquisition can take several weeks - start early in preparation phase
- Multiple utilities require coordinated routing to avoid conflicts

## Interdependency Matrix

### Within PKG-018
- Depends on site preparation (DEL-018-02 grading)
- Works in coordination with DEL-018-05 (Drainage) for utility placement
- Can coordinate with DEL-018-03, 04 for overall site construction sequencing

### Cross-Package Dependencies
- Critical for PKG-016 (Crane electrical supply)
- Critical for PKG-017 (Building electrical, water, sewer connections)
- Utilities support OBJ-005 (Infrastructure/Resilience) objectives
- Enables facility operations in support of OBJ-001

---

## Extracted Dependency Register

**Total rows**: 21 (21 ACTIVE, 0 RETIRED)
**ANCHOR rows**: 7 (1 IMPLEMENTS_NODE, 6 TRACES_TO_REQUIREMENT)
**EXECUTION rows**: 14

### ANCHOR Edges (Tree -- Definition Traceability)

| DependencyID | AnchorType | TargetType | TargetRefID | TargetName | Confidence |
|--------------|------------|------------|-------------|------------|------------|
| DEP-018-06-001 | IMPLEMENTS_NODE | WBS_NODE | | PKG-018 -- Sitework & Civil Construction | HIGH |
| DEP-018-06-002 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0080 | SOW-0080 -- Natural gas tie-in | HIGH |
| DEP-018-06-003 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0081 | SOW-0081 -- Electrical service tie-in | HIGH |
| DEP-018-06-004 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0082 | SOW-0082 -- Communication lines tie-in | HIGH |
| DEP-018-06-005 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-001 | OBJ-001 -- Code-compliant maintenance shop | HIGH |
| DEP-018-06-006 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-005 | OBJ-005 -- Electrical/low-voltage systems | HIGH |
| DEP-018-06-019 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0122 | SOW-0122 -- Electrical pole relocation (Add. 3 Q7) | HIGH |

### EXECUTION Edges (DAG -- Information Flow)

| DependencyID | Direction | DependencyType | TargetType | Target | EstimateImpact | Statement (summary) |
|--------------|-----------|----------------|------------|--------|----------------|---------------------|
| DEP-018-06-007 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-018-02 (Site Grading) | BLOCKING | Site grading must be complete before trenching (HP-01) |
| DEP-018-06-008 | UPSTREAM | PREREQUISITE | PACKAGE | PKG-005 (Civil Design) | BLOCKING | IFC drawings for utility routing required before installation |
| DEP-018-06-009 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-004 (Electrical Design) | BLOCKING | Electrical load calculation required for service sizing |
| DEP-018-06-010 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-003 (Mechanical Design) | BLOCKING | Gas load/sizing calculations required for gas service |
| DEP-018-06-011 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-009-03 (Safety Code Permits) | BLOCKING | Permits must be obtained before installation commences |
| DEP-018-06-012 | UPSTREAM | INTERFACE | EXTERNAL | Utility Providers (gas, electrical, comms) | BLOCKING | Provider coordination, agreements, and approvals required |
| DEP-018-06-013 | DOWNSTREAM | HANDOVER | PACKAGE | PKG-015 (Electrical Installation) | ADVISORY | Electrical service energization handed to PKG-015 |
| DEP-018-06-014 | DOWNSTREAM | HANDOVER | PACKAGE | PKG-013 (Mechanical Installation) | ADVISORY | Gas service handed to PKG-013 for heating commissioning |
| DEP-018-06-015 | UPSTREAM | INTERFACE | DOCUMENT | App B (Electrical Drawing) | INFO | Conceptual electrical loads for service sizing |
| DEP-018-06-016 | UPSTREAM | INTERFACE | DOCUMENT | App C (Site Maps) | INFO | Site location context for utility routing |
| DEP-018-06-017 | UPSTREAM | CONSTRAINT | DELIVERABLE | DEL-009-04 (Code Compliance Register) | ADVISORY | County must attend inspections; reports must be provided |
| DEP-018-06-018 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-018-05 (Wash Bay Drainage) | ADVISORY | Utility routing must avoid conflicts with drainage |
| DEP-018-06-020 | UPSTREAM | CONSTRAINT | EXTERNAL | County Gas Pipeline Relocation (SOW-0206 OUT) | ADVISORY | County gas pipeline relocation timing coordination required |
| DEP-018-06-021 | UPSTREAM | INTERFACE | EXTERNAL | Local Electrical Service Provider -- Pole Relocation | BLOCKING | Pole/transformer relocation coordination per SOW-0122 |

---

## Run Notes

### Run Parameters
- **Run Date**: 2026-02-26
- **MODE**: UPDATE
- **STRICTNESS**: CONSERVATIVE
- **CONSUMER_CONTEXT**: TASK_ESTIMATING
- **SOURCE_DOCS**: AUTO (resolved below)
- **ANCHOR_DOC**: AUTO -> Datasheet.md (selected: filename contains "datasheet", highest anchor-signal confidence)
- **EXECUTION_DOC_ORDER**: AUTO -> Procedure.md, Guidance.md, Specification.md (Procedure first for workflow clarity, then Guidance for directional context, then Specification for normative requirements)

### Paths Used
- **RUN_ROOT**: /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude
- **DELIVERABLE_PATH**: .../PKG-018_Sitework & Civil Construction/1_Working/DEL-018-06_Utility-Tieins/
- **DECOMPOSITION_PATH**: .../\_Decomposition/WDMLRL_Decomposition_Claude.md (found and used successfully)
- **Source documents scanned**: Datasheet.md, Guidance.md, Procedure.md, Specification.md
- **Read-only inputs**: _REFERENCES.md (used for document pointer resolution), _CONTEXT.md (not scanned for dependencies)

### Decomposition Validation
- Decomposition file located and loaded: WDMLRL_Decomposition_Claude.md (R1, 2026-02-25)
- DEL-018-06 confirmed in Decomposition SS7 under PKG-018
- SOW-0080, SOW-0081, SOW-0082 confirmed in Decomposition SS3 and Scope Ledger (rows 673-675)
- OBJ-001, OBJ-005 confirmed in Decomposition SS5 and SS7 DEL-018-06 row
- PKG-005, DEL-003, DEL-004, DEL-009-03, DEL-009-04, DEL-018-02, DEL-018-05, PKG-013, PKG-015 all confirmed as valid IDs in Decomposition

### Source Observations
- _REFERENCES.md contains incorrect SOW labeling (SOW-0080 labeled "Electrical", SOW-0081 labeled "Water/Sewer"); see CONF-001 in Guidance. Decomposition/RFP are authoritative. This agent did not modify _REFERENCES.md.
- _DEPENDENCIES.md (pre-existing) contained declared dependencies referencing "water, sewer" which are not in scope per Decomposition. Declared sections preserved as-is (human-owned).
- DEL-003 and DEL-004 are used in source documents as package-level shorthand references (e.g., "electrical design (DEL-004)"). The Decomposition defines these as packages (PKG-003, PKG-004) with multiple deliverables each. The source documents' usage of "DEL-003" and "DEL-004" is interpreted as referring to the package's design outputs collectively. TargetDeliverableID is recorded as stated in source.

### Assumptions Recorded
- None elevated to dependency rows at CONSERVATIVE strictness. All emitted rows are evidence-backed FACT.

### Run 2026-03-26 (SCA-001 Refresh)

**Parameters:**
- MODE: UPDATE
- STRICTNESS: CONSERVATIVE
- CONSUMER_CONTEXT: NONE
- SOURCE_DOCS: AUTO (resolved to: Datasheet.md, Guidance.md, Procedure.md, Specification.md)
- ANCHOR_DOC: Datasheet.md
- EXECUTION_DOC_ORDER: Procedure.md, Guidance.md, Specification.md
- DECOMPOSITION_PATH: WDMLRL_Decomposition_Claude.md R2 (2026-03-26, SCA-001)

**SCA-001 impact assessment:**
- **SOW-0122 (NEW)**: Electrical pole(s) and transformer relocation added to DEL-018-06 scope per Addendum 3, Q7. Decomposition decision D-013 maps SOW-0122 to existing DEL-018-06 rather than creating a new deliverable. New ANCHOR trace row DEP-018-06-019 added. New EXECUTION INTERFACE row DEP-018-06-021 added for service provider coordination.
- **SOW-0080 (MODIFIED)**: Gas supply parameters confirmed: 2-inch PVC pipe at 50 PSI constant pressure (Add. 3, Q8). These are parameter clarifications that do not change dependency structure. Existing DEP-018-06-002 (ANCHOR trace to SOW-0080) and DEP-018-06-010/014 (gas-related EXECUTION edges) remain valid.
- **SOW-0206 (NEW OUT)**: Gas pipeline relocation is County responsibility (Add. 3, Q9). New EXECUTION CONSTRAINT row DEP-018-06-020 added -- Contractor must coordinate gas tie-in timing with County pipeline relocation schedule.
- **_CONTEXT.md updated** to reflect SOW-0122 addition and gas parameter clarifications (Last amended: 2026-03-26).
- All 18 existing rows confirmed ACTIVE with LastSeen updated. 3 new rows added.

**Decomposition validation (R2):**
- SOW-0122 confirmed in R2 scope ledger: IN, PKG-018, DEL-018-06, OBJ-001, D-011.
- SOW-0206 confirmed in R2 scope boundaries: OUT, County responsibility.
- SOW-0080 confirmed with updated parameters (2" PVC, 50 PSI).
- D-011 and D-013 confirmed in R2 decision log.

**New rows added:**
1. DEP-018-06-019: ANCHOR TRACES_TO_REQUIREMENT -> SOW-0122 (electrical pole relocation)
2. DEP-018-06-020: EXECUTION CONSTRAINT -> SOW-0206 County gas pipeline relocation (EXTERNAL)
3. DEP-018-06-021: EXECUTION INTERFACE -> Local Electrical Service Provider pole relocation coordination (EXTERNAL, BLOCKING)

**Warnings:**
- None. Parent anchor (IMPLEMENTS_NODE) found: 1 row. No FLOATING_NODE or AMBIGUOUS_ANCHOR.

### Warnings (Run 2026-02-26)
- (none)

### Integrity Check Results
- Parent anchor (IMPLEMENTS_NODE) count: 1 -- OK
- DependencyID uniqueness: PASS (18 unique IDs)
- All ACTIVE rows have EvidenceFile and SourceRef: PASS
- All enum values canonical: PASS
- TargetDeliverableID placement rules: PASS
- CSV parseable: PASS

---

## Run History

| Run | Date | Mode | Strictness | Consumer | Decomp Status | Warnings | ACTIVE Anchors | ACTIVE Execution | Total ACTIVE |
|-----|------|------|------------|----------|---------------|----------|----------------|------------------|--------------|
| 1 | 2026-02-26 | UPDATE | CONSERVATIVE | TASK_ESTIMATING | Loaded (WDMLRL_Decomposition_Claude.md R1) | None | 6 | 12 | 18 |
| 2 | 2026-03-26 | UPDATE | CONSERVATIVE | NONE | Loaded (WDMLRL_Decomposition_Claude.md R2, SCA-001) | None | 7 | 14 | 21 |

---

## Lifecycle Summary

| Metric | Count |
|--------|-------|
| Total rows | 21 |
| ACTIVE | 21 |
| RETIRED | 0 |

### Closure State Breakdown (ACTIVE rows)

| SatisfactionStatus | Count |
|--------------------|-------|
| PENDING | 9 |
| TBD | 12 |

### Extraction Lifecycle

| Origin | ACTIVE | RETIRED |
|--------|--------|---------|
| EXTRACTED | 21 | 0 |
| DECLARED | 0 | 0 |

---

## Downstream Handoff Notes

**Consumer Context**: TASK_ESTIMATING

### Estimating-Critical Dependencies

The following dependencies are classified as **BLOCKING** for estimating readiness. Until these are resolved, meaningful cost/quantity estimation for DEL-018-06 is constrained:

1. **DEP-018-06-007** (DEL-018-02 Site Grading) -- Trenching cannot begin until grading is complete. Grading scope/schedule affects utility installation timing and potentially cost (mobilization, access).

2. **DEP-018-06-008** (PKG-005 Civil Design) -- Utility routing corridors, trench locations, and service entry points are undefined until civil IFC drawings are produced. Without these, trench lengths, depths, and routing cannot be quantified for estimating.

3. **DEP-018-06-009** (DEL-004 Electrical Design) -- Electrical load calculations determine service capacity, which drives service entrance equipment sizing, transformer requirements, and utility provider costs. Without this, electrical service tie-in costs cannot be estimated.

4. **DEP-018-06-010** (DEL-003 Mechanical Design) -- Gas load/sizing determines gas service capacity, pipe sizing, and potential gas main extension requirements. The gas main extension scenario (see Guidance) could significantly affect cost and schedule.

5. **DEP-018-06-011** (DEL-009-03 Safety Code Permits) -- Permit requirements may impose conditions that affect scope (e.g., additional inspection points, specific material requirements).

6. **DEP-018-06-012** (Utility Providers) -- Provider responses will determine: (a) distance to nearest infrastructure (gas, electrical, telecom), (b) whether gas main extension is required, (c) transformer ownership, (d) lead times. All of these directly affect cost estimates.

### Key Estimating Uncertainties

- **Gas main extension risk**: If the nearest gas main is distant, extension costs could be significant. The Guidance provides an evaluation framework but all cost/schedule values are TBD pending utility provider response. This is a potential major cost variable.
- **Transformer ownership**: Whether utility-owned or customer-owned affects capital cost. TBD.
- **Utility infrastructure proximity**: Distances from site boundary to nearest gas, electrical, and telecom infrastructure are all TBD. These distances directly drive trench length and material quantities.
- **Three-phase power availability**: Rural site may require utility infrastructure upgrades for three-phase service.

### Advisory Dependencies

- **DEP-018-06-013/014** (PKG-015, PKG-013 handovers) -- These define the boundary of DEL-018-06's scope. The estimator should confirm the demarcation point between site utility tie-in work and building-side installation work to avoid double-counting or gaps.
- **DEP-018-06-017** (DEL-009-04 inspections) -- Inspection scheduling and County attendance requirements affect labor planning and schedule.
- **DEP-018-06-018** (DEL-018-05 drainage coordination) -- Trench routing must avoid drainage infrastructure, which may affect trench lengths.
