# DEL-017-04_Locker-Room | Dependencies

## Dependency Tracking Status
**Tracking Status**: TRACKED
**Register**: Dependencies.csv (v3.1)

## Dependency Framework

### Upstream Dependencies
Dependencies that must be satisfied before this deliverable can proceed:

| Dependency ID | Description | Status | Notes |
|---------------|-------------|--------|-------|
| SPACE-PLANNING-001 | Available space confirmation | Pending | Must confirm locker room footprint within building |
| DESIGN-001 | Locker room design plan | Pending | Final design and layout approval |
| LOCKER-SYSTEM-001 | Locker system selection/spec | Pending | Choose appropriate locker system product |
| UTILITY-001 | Plumbing/electrical capacity for sinks | Pending | Verify utility availability for lockers area |

### Downstream Dependencies
Deliverables that depend on completion of this deliverable:

| Dependent ID | Description | Status | Notes |
|--------------|-------------|--------|-------|
| WORKFORCE-AMENITIES-001 | Workforce locker/change facilities available | Pending | Required for operational viability and workforce amenities |

## Critical Path Assessment
- **On Critical Path**: CONDITIONAL
- **Justification**: Important facility amenity; can potentially follow other renovations if phased approach taken

## Dependency Management Notes
- Dependencies tracked at deliverable level within PKG-017
- Space planning must occur early in preparation phase
- Locker room could potentially be a prioritized first completion for workforce amenity availability

## Interdependency Matrix

### Within PKG-017
- Independent work scope; can proceed in parallel with other renovations
- May benefit from proximity to DEL-017-03 (Washroom) for shared utility infrastructure
- No hard sequencing requirements with other deliverables

### Cross-Package Dependencies
- Building envelope integrity required before interior work begins
- Relates to PKG-018 (Sitework) for overall facility completion sequencing
- May be desirable to complete early to support workforce comfort during other construction activities

---

## Extracted Dependency Register

**Schema Version:** v3.1
**Total ACTIVE rows:** 13
**ANCHOR rows:** 2 (1 IMPLEMENTS_NODE, 1 TRACES_TO_REQUIREMENT)
**EXECUTION rows:** 11

### ANCHOR Dependencies (Tree)

| DependencyID | AnchorType | TargetType | TargetRefID / TargetName | Confidence | Notes |
|--------------|------------|------------|--------------------------|------------|-------|
| DEP-017-04-001 | IMPLEMENTS_NODE | WBS_NODE | SOW-0073 | HIGH | FACT. Parent scope-of-work anchor. |
| DEP-017-04-002 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-001 | MEDIUM | ASSUMPTION. Datasheet marks as assumption; decomposition confirms. |

### EXECUTION Dependencies (DAG)

| DependencyID | Direction | DependencyType | TargetType | Target | Confidence | EstimateImpactClass |
|--------------|-----------|---------------|------------|--------|------------|---------------------|
| DEP-017-04-003 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-017-03 (Washroom Renovation & Expansion) | HIGH | ADVISORY |
| DEP-017-04-004 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-001-10 (Old North Shop Renovation Plans) | HIGH | BLOCKING |
| DEP-017-04-005 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-006 series (Plumbing Design) | HIGH | BLOCKING |
| DEP-017-04-006 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-004 series (Electrical Design) | HIGH | BLOCKING |
| DEP-017-04-007 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-009-01 (Development Permit) | HIGH | BLOCKING |
| DEP-017-04-008 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-009-02 (Building Permit) | HIGH | BLOCKING |
| DEP-017-04-009 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-009-03 (Safety Code Permits) | HIGH | BLOCKING |
| DEP-017-04-010 | UPSTREAM | CONSTRAINT | DOCUMENT | R-01 (AB-2026-01424-WDMLRL RFP.pdf) | HIGH | INFO |
| DEP-017-04-011 | UPSTREAM | CONSTRAINT | DOCUMENT | R-04 (Appendix B Drawings) | HIGH | ADVISORY |
| DEP-017-04-012 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-001-09 (Demolition Plans) | MEDIUM | ADVISORY |
| DEP-017-04-013 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-017-02 (Mezzanine Renovation) | MEDIUM | ADVISORY |

---

## Run Notes

### Run: 2026-02-26

**Parameters:**
- MODE: UPDATE
- STRICTNESS: CONSERVATIVE
- CONSUMER_CONTEXT: TASK_ESTIMATING
- SOURCE_DOCS: AUTO (resolved below)
- ANCHOR_DOC: AUTO -> Datasheet.md (contains identification/traceability fields)
- EXECUTION_DOC_ORDER: AUTO -> Specification.md, Procedure.md, Guidance.md
- DECOMPOSITION_PATH: _Decomposition/WDMLRL_Decomposition_Claude.md (found and used)
- _REFERENCES.md: present and read (used for document reference resolution)

**Defaults applied:**
- ANCHOR_DOC selected by heuristic: Datasheet.md (contains "Scope of Work Item", "Objective", "Package" identifiers)
- EXECUTION_DOC_ORDER: Specification.md first (normative requirements, scope boundary), then Procedure.md (explicit prerequisites/upstream dependencies/steps), then Guidance.md (considerations/trade-offs/sequencing)

**Source documents scanned (4):**
1. Datasheet.md (ANCHOR_DOC)
2. Specification.md (EXECUTION_DOC)
3. Procedure.md (EXECUTION_DOC)
4. Guidance.md (EXECUTION_DOC)

**Decomposition validation:**
- SOW-0073 confirmed in decomposition scope ledger: "Construct new locker/change room with laundry services" -> PKG-017, DEL-017-04
- OBJ-001 confirmed in decomposition objectives: DEL-017-04 Supports OBJ = OBJ-001
- DEL-017-03 confirmed: Washroom Renovation & Expansion (PKG-017, SOW-0072 + SOW-0074)
- DEL-001-10 confirmed: Old North Shop Renovation Plans (PKG-001, covers SOW-0073)
- DEL-001-09 confirmed: Old North Shop Demolition Plans (PKG-001, covers SOW-0070/0071/0072)
- DEL-009-01/02/03 confirmed: Permit deliverables in PKG-009
- DEL-006 series confirmed in PKG-006 (DEL-006-02 through DEL-006-08)
- DEL-004 series confirmed in PKG-004 (DEL-004-02 through DEL-004-09)
- DEL-017-02 confirmed: Old North Shop Mezzanine Renovation (PKG-017, SOW-0071)

**Warnings:** None.

**Decisions and assumptions:**
- DEL-006 series and DEL-004 series: Procedure references these as series rather than specific deliverables. Multiple candidate IDs exist in decomposition. TargetDeliverableID left empty; TargetName preserves series reference. FACT: explicit dependency exists; specific target ID is ambiguous.
- OBJ-001 anchor (DEP-017-04-002): Datasheet marks association as ASSUMPTION (package-grouping heuristic). Decomposition independently confirms OBJ-001. Confidence set to MEDIUM (not HIGH) because Datasheet itself flags uncertainty.
- DEL-001-09 (DEP-017-04-012): Procedure Step 2.2 states demolition coordination is conditional ("if required"). Dependency recorded as INTERFACE with MEDIUM confidence.
- No DOWNSTREAM execution dependencies extracted. Source documents describe this deliverable's outputs (workforce amenities, CCC contribution) in general operational terms, not as explicit information/artifact transfers to specific downstream deliverables.
- Building envelope integrity prerequisite (mentioned in existing _DEPENDENCIES.md "Cross-Package Dependencies") was not extracted as a formal row because no specific deliverable ID or artifact transfer is stated; it is a general sequencing note, not an information-flow dependency per the extraction model.

**Estimating extension columns:**
- CONSUMER_CONTEXT=TASK_ESTIMATING: EstimateImpactClass and ConsumerHint populated for all EXECUTION rows.
- BLOCKING: assigned to design drawing prerequisites (DEL-001-10, DEL-006 series, DEL-004 series) and permit prerequisites (DEL-009-01/02/03) because scope/quantities cannot be estimated without these inputs.
- ADVISORY: assigned to interface/coordination dependencies (DEL-017-03, DEL-017-02, DEL-001-09) and Appendix B drawings because they influence quantities/specs but do not gate estimating.
- INFO: assigned to RFP document constraint (R-01) because it is governing context already available.

---

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE ANCHOR | ACTIVE EXECUTION | Total ACTIVE |
|-----------|------|------------|---------------|----------|---------------|------------------|--------------|
| 2026-02-26 | UPDATE | CONSERVATIVE | _Decomposition/WDMLRL_Decomposition_Claude.md (found) | None | 2 | 11 | 13 |

---

## Lifecycle Summary

**Extraction lifecycle:**
- ACTIVE: 13
- RETIRED: 0

**Closure lifecycle (SatisfactionStatus breakdown, ACTIVE rows only):**
- TBD: 13
- PENDING: 0
- IN_PROGRESS: 0
- SATISFIED: 0
- WAIVED: 0
- NOT_APPLICABLE: 0

**Tree integrity:**
- Parent anchor (IMPLEMENTS_NODE): 1 (SOW-0073) -- OK
- Trace anchors (TRACES_TO_REQUIREMENT): 1 (OBJ-001)

---

## Downstream Handoff Notes

**Consumer context: TASK_ESTIMATING**

The following observations are relevant for downstream task estimating workflows:

### Blocking dependencies (6 rows)
These dependencies gate meaningful estimating because scope, quantities, or key design parameters are unknown without them:

1. **DEP-017-04-004** -- DEL-001-10 (Old North Shop Renovation Plans): The locker room layout, partition locations, door schedule, and finish schedule are defined in these IFC drawings. Without them, the locker room footprint, wall quantities, door count, and finish areas cannot be quantified.
2. **DEP-017-04-005** -- DEL-006 series (Plumbing Design): Plumbing fixture count, pipe sizing, and connection routing are defined in plumbing design. Without them, plumbing material quantities and labor scope are unknown.
3. **DEP-017-04-006** -- DEL-004 series (Electrical Design): Panel assignments, circuit counts, and lighting fixture schedule are defined in electrical design. Without them, electrical material quantities and labor scope are unknown.
4. **DEP-017-04-007** -- DEL-009-01 (Development Permit): Permit approval is a hard gate before construction can commence.
5. **DEP-017-04-008** -- DEL-009-02 (Building Permit): Building permit is a hard gate before construction.
6. **DEP-017-04-009** -- DEL-009-03 (Safety Code Permits): Safety code permits are hard gates before respective construction phases.

### Advisory dependencies (4 rows)
These dependencies are likely to change quantities, specifications, or procurement approach but are not hard gates:

1. **DEP-017-04-003** -- DEL-017-03 (Washroom Renovation & Expansion): Shared MEP infrastructure may affect plumbing/electrical routing and quantities.
2. **DEP-017-04-011** -- R-04 (Appendix B Drawings): Conceptual drawings provide space planning context that influences footprint assumptions.
3. **DEP-017-04-012** -- DEL-001-09 (Demolition Plans): Demolition scope (if any) within locker room zone affects preparation quantities.
4. **DEP-017-04-013** -- DEL-017-02 (Mezzanine Renovation): Space allocation coordination may affect available footprint.

### Informational dependencies (1 row)
1. **DEP-017-04-010** -- R-01 (RFP): Governing requirements document; already available as project context.

### Key TBDs affecting estimating readiness
These items from the source documents are not formal dependency rows but are noted for estimating context:
- **Workforce headcount**: Not stated in sources; required to size locker count, bench capacity, and overall footprint (Datasheet attribute [A-005]).
- **Shower facilities**: TBD pending County confirmation (Datasheet attribute [B-002]).
- **Laundry scope boundary**: Whether "laundry services" includes appliance supply or only rough-in is ambiguous (Specification REQ-017-04-02 TBD [C-001]).
- **Occupancy classification**: Affects ventilation rates, egress, plumbing fixture counts, and fire separation (Specification REQ-017-04-03 TBD [A-001]).
- **Finish specifications**: Flooring, wall, ceiling finishes are TBD (Specification Scope [D-003]).
- **Door fire rating**: Depends on fire separation analysis (Specification REQ-017-04-12 [F-001]).
