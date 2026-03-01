# DEL-017-03_Washroom-Reno | Dependencies

## Dependency Tracking Status
**Tracking Status**: TRACKED
**Register Schema Version**: v3.1

## Dependency Framework

### Upstream Dependencies
Dependencies that must be satisfied before this deliverable can proceed:

| Dependency ID | Description | Status | Notes |
|---------------|-------------|--------|-------|
| CODE-REVIEW-001 | Building code compliance review | Pending | Must verify renovation meets current codes |
| ACCESS-REVIEW-001 | Accessibility standards review | Pending | Alberta Building Code barrier-free accessibility requirements |
| EXISTING-DOCS-001 | Existing washroom documentation | Pending | Current drawings and condition photos |
| UTILITY-001 | Plumbing/ventilation capacity verification | Pending | Confirm available capacity for expansion |

### Downstream Dependencies
Deliverables that depend on completion of this deliverable:

| Dependent ID | Description | Status | Notes |
|--------------|-------------|--------|-------|
| FACILITY-OPS-001 | Facility operations with updated washroom | Pending | Required for workforce amenities |

## Critical Path Assessment
- **On Critical Path**: YES
- **Justification**: Updated washroom facilities required for facility operations and code compliance; directly impacts workforce amenities and operational viability

## Dependency Management Notes
- Dependencies tracked at deliverable level within PKG-017
- Code compliance and accessibility assessments must occur early in preparation phase
- Dual SOW references (SOW-0072, SOW-0074) represent renovation component and expansion component of a single construction activity

## Interdependency Matrix

### Within PKG-017
- Interface with DEL-017-04 (Locker Room): shared wall/partition, potential shared plumbing chase, construction sequencing coordination required
- Electrical coordination with DEL-017-01 and DEL-017-04

### Cross-Package Dependencies
- PKG-001 (Architectural Design): DEL-001-09 Demolition Plans, DEL-001-10 Renovation Plans, DEL-001-08 Finish Schedule
- PKG-006 (Plumbing Design): IFC plumbing drawings covering washroom
- PKG-009 (Permitting): DEL-009-02 Building Permit, DEL-009-03 Safety Code Permits
- PKG-013 (Mechanical Installation): exhaust fan / ductwork interface
- PKG-014 (Plumbing Installation): system connections to cistern and septic
- PKG-015 (Electrical Installation): lighting, exhaust fan circuit, receptacles
- PKG-019 (Construction Management): DEL-019-01 Prime Contractor designation
- PKG-020 (Commissioning & Closeout): DEL-020-01 Commissioning, DEL-020-02 CCC (downstream)

---

## Extracted Dependency Register

**Total rows**: 22
**ACTIVE**: 22
**RETIRED**: 0

### ANCHOR rows (4 ACTIVE)

| DependencyID | AnchorType | TargetType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|---|
| DEP-017-03-001 | IMPLEMENTS_NODE | WBS_NODE | | PKG-017 -- Existing Building Renovation (Old North Shop) | HIGH |
| DEP-017-03-002 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0072 | Renovate existing washroom below mezzanine in Old North Shop | HIGH |
| DEP-017-03-003 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0074 | Expand washroom facilities to include urinal | HIGH |
| DEP-017-03-004 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-001 | Deliver a code-compliant fully functional maintenance shop addition | HIGH |

### EXECUTION rows (18 ACTIVE)

| DependencyID | Direction | DependencyType | TargetType | TargetName | Confidence | EstimateImpactClass |
|---|---|---|---|---|---|---|
| DEP-017-03-005 | UPSTREAM | PREREQUISITE | UNKNOWN | EXISTING-DOCS-001 -- Existing washroom documentation | HIGH | BLOCKING |
| DEP-017-03-006 | UPSTREAM | PREREQUISITE | UNKNOWN | CODE-REVIEW-001 -- Building code compliance review | HIGH | BLOCKING |
| DEP-017-03-007 | UPSTREAM | PREREQUISITE | UNKNOWN | ACCESS-REVIEW-001 -- Accessibility standards review | HIGH | ADVISORY |
| DEP-017-03-008 | UPSTREAM | PREREQUISITE | UNKNOWN | UTILITY-001 -- Plumbing/ventilation capacity verification | HIGH | ADVISORY |
| DEP-017-03-009 | UPSTREAM | CONSTRAINT | DELIVERABLE | DEL-009-02 Building Permit | HIGH | BLOCKING |
| DEP-017-03-010 | UPSTREAM | CONSTRAINT | DELIVERABLE | DEL-009-03 Safety Code Permits | HIGH | BLOCKING |
| DEP-017-03-011 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-001-10 Renovation Plans | HIGH | BLOCKING |
| DEP-017-03-012 | UPSTREAM | PREREQUISITE | PACKAGE | PKG-006 Plumbing Design | HIGH | BLOCKING |
| DEP-017-03-013 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-001-09 Demolition Plans | HIGH | BLOCKING |
| DEP-017-03-014 | UPSTREAM | CONSTRAINT | DELIVERABLE | DEL-019-01 Prime Contractor | HIGH | INFO |
| DEP-017-03-015 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-001-08 Finish Schedule | MEDIUM | ADVISORY |
| DEP-017-03-016 | UPSTREAM | INTERFACE | PACKAGE | PKG-014 Plumbing Installation | HIGH | ADVISORY |
| DEP-017-03-017 | UPSTREAM | INTERFACE | PACKAGE | PKG-013 Mechanical Installation | MEDIUM | ADVISORY |
| DEP-017-03-018 | UPSTREAM | INTERFACE | PACKAGE | PKG-015 Electrical Installation | MEDIUM | ADVISORY |
| DEP-017-03-019 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-017-04 Locker/Change Room | HIGH | ADVISORY |
| DEP-017-03-020 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-020-01 Building Systems Commissioning | HIGH | INFO |
| DEP-017-03-021 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-020-02 Final Inspection & CCC | HIGH | INFO |
| DEP-017-03-022 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-009-04 Code Compliance Register | MEDIUM | INFO |

---

## Run Notes

**Run Date**: 2026-02-26
**Mode**: UPDATE
**Strictness**: CONSERVATIVE
**Consumer Context**: TASK_ESTIMATING
**Source Docs Mode**: AUTO

### Paths Used
- **RUN_ROOT**: `/Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude`
- **DELIVERABLE_PATH**: `PKG-017_Existing Building Renovation (Old North Shop)/1_Working/DEL-017-03_Washroom-Reno/`
- **DECOMPOSITION_PATH**: `_Decomposition/WDMLRL_Decomposition_Claude.md` (found and loaded successfully)

### Source Document Resolution (AUTO)
- **ANCHOR_DOC**: `Datasheet.md` (selected: contains `datasheet` pattern; explicit identification fields with Objective, SOW, Package references)
- **EXECUTION_DOC_ORDER**:
  1. `Procedure.md` (contains `procedure` pattern; highest execution signal density -- prerequisites table, step-by-step phases)
  2. `Specification.md` (contains `spec` pattern; requirements, scope inclusions/exclusions)
  3. `Guidance.md` (contains `guidance` pattern; principles, considerations, conflict table)
  4. `Datasheet.md` (secondary pass for construction cross-references)

### Read-Only Inputs
- `_REFERENCES.md` (read; used for document pointer resolution)
- `_CONTEXT.md` (read; used for deliverable identity confirmation)

### Decomposition Validation
- Decomposition loaded successfully from `WDMLRL_Decomposition_Claude.md` (R1, 2026-02-25)
- DEL-017-03 confirmed in PKG-017 deliverable table: Name = "Washroom Renovation & Expansion", Covers SOW = "SOW-0072, SOW-0074", Supports OBJ = "OBJ-001"
- All cross-referenced deliverable IDs (DEL-001-08, DEL-001-09, DEL-001-10, DEL-009-02, DEL-009-03, DEL-009-04, DEL-017-04, DEL-019-01, DEL-020-01, DEL-020-02) confirmed in decomposition
- All cross-referenced package IDs (PKG-006, PKG-013, PKG-014, PKG-015) confirmed in decomposition

### Unresolved Targets
- EXISTING-DOCS-001: Referenced in Procedure prerequisites and Datasheet; appears to be a pre-project activity/artifact not assigned to a decomposition deliverable. Recorded as TargetType=UNKNOWN.
- CODE-REVIEW-001: Referenced in Procedure prerequisites; appears to be a design-phase review activity not assigned to a decomposition deliverable. Recorded as TargetType=UNKNOWN.
- ACCESS-REVIEW-001: Referenced in Procedure prerequisites; appears to be a design-phase review activity not assigned to a decomposition deliverable. Recorded as TargetType=UNKNOWN.
- UTILITY-001: Referenced in Procedure prerequisites; appears to be a design-phase verification not assigned to a decomposition deliverable. Recorded as TargetType=UNKNOWN.

### Warnings
- None. Parent anchor (IMPLEMENTS_NODE) found: exactly 1 (PKG-017). No FLOATING_NODE or AMBIGUOUS_ANCHOR condition.

### Assumptions Logged
- DEP-017-03-017: Ventilation requirement is an ASSUMPTION per source documents; coordination with PKG-013 is explicitly stated.

---

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE ANCHOR | ACTIVE EXECUTION | Notes |
|---|---|---|---|---|---|---|---|
| 2026-02-26 | UPDATE | CONSERVATIVE | WDMLRL_Decomposition_Claude.md (loaded OK) | None | 4 | 18 | Initial extraction. CONSUMER_CONTEXT=TASK_ESTIMATING. 22 total ACTIVE rows. |

---

## Lifecycle Summary

### Extraction Lifecycle
| Status | Count |
|---|---|
| ACTIVE | 22 |
| RETIRED | 0 |

### Closure Lifecycle (ACTIVE rows)
| SatisfactionStatus | Count |
|---|---|
| PENDING | 18 |
| TBD | 4 |

### By DependencyClass
| Class | ACTIVE | RETIRED |
|---|---|---|
| ANCHOR | 4 | 0 |
| EXECUTION | 18 | 0 |

### By Direction (EXECUTION only)
| Direction | Count |
|---|---|
| UPSTREAM | 15 |
| DOWNSTREAM | 3 |

### By EstimateImpactClass (EXECUTION only)
| Class | Count |
|---|---|
| BLOCKING | 7 |
| ADVISORY | 7 |
| INFO | 4 |

---

## Downstream Handoff Notes

**Consumer Context**: TASK_ESTIMATING

### Estimating-Relevant Observations

**BLOCKING dependencies (7)**: These represent hard gates where scope or key quantities cannot be meaningfully estimated without the upstream input:

1. **EXISTING-DOCS-001** (Existing condition survey): The existing washroom footprint, fixture inventory, and plumbing infrastructure are undocumented. Without this survey, demolition quantities, expansion extent, and fixture replacement count are unknown. This is the single most significant blocker for detailed estimating.
2. **CODE-REVIEW-001** (Code review): Determines whether the renovation triggers additional code upgrade requirements (fire separation, accessibility, etc.) that would expand scope.
3. **DEL-009-02** (Building Permit): Hard gate for construction start; cost implications for permit fees (County responsibility per RFP section 3.3.1) and schedule.
4. **DEL-009-03** (Safety Code Permits): Hard gate for construction start; multiple permits required (plumbing, mechanical, electrical, building).
5. **DEL-001-10** (IFC Renovation Plans): Defines the actual construction scope; without issued drawings, construction scope is conceptual only.
6. **PKG-006** (Plumbing Design): Defines plumbing rough-in scope including new urinal connections; required for plumbing cost estimation.
7. **DEL-001-09** (Demolition Plans): Defines demolition scope; required before demolition quantities can be estimated.

**ADVISORY dependencies (7)**: These are likely to change quantities, specifications, or procurement approach but are not hard gates for preliminary estimating:

1. **ACCESS-REVIEW-001**: May increase floor area requirements and add accessibility fixtures (grab bars, wider doors).
2. **UTILITY-001**: Verifies available capacity; unlikely to change scope fundamentally but may affect pipe sizing.
3. **DEL-001-08** (Finish Schedule): Finish material selections affect material cost; standard industrial-grade finishes can be assumed for preliminary estimate.
4. **PKG-014** (Plumbing Installation): Interface for system connections; scope defined by PKG-006 design.
5. **PKG-013** (Mechanical Installation): Exhaust fan/ductwork interface; modest scope impact.
6. **PKG-015** (Electrical Installation): Lighting and circuit interface; modest scope impact.
7. **DEL-017-04** (Locker/Change Room interface): Shared wall/partition and plumbing chase coordination; scope boundary must be resolved per Conflict Table C-01 before subcontract scope documents are finalized.

**Key estimating risk**: The Datasheet records multiple TBD attributes (existing condition size, expansion area, fixture counts). These TBDs trace directly to the BLOCKING dependency on EXISTING-DOCS-001. A preliminary estimate must either:
- (a) carry explicit contingency for these unknowns, or
- (b) be deferred until the existing condition survey is completed.

**Conflict requiring resolution**: Guidance Conflict Table C-01 (scope-split between DEL-017-03 and DEL-017-04) must be resolved before subcontract scope documents are finalized. This affects cost allocation between the two deliverables.
