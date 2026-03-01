# DEL-013-04: Heavy Equipment Exhaust System - Dependencies

## Dependency Status
**Tracking Status**: TRACKED
**Register Schema Version**: v3.1

## External Dependencies
- Equipment specifications and exhaust requirements
- Shop floor layout finalization
- Exhaust outlet location approval
- Environmental compliance review
- Mechanical Contractor availability

## Internal Package Dependencies
- **DEL-013-01** (Heating System): Heat recovery from exhaust
- **DEL-013-02** (Air Exchanger): Stale air capture
- **DEL-013-03** (Makeup Air): Makeup air balances equipment exhaust
- **DEL-013-05** (Welding Exhaust): Separate exhaust system coordination
- **DEL-013-06** (Ceiling Fans): Distributed air circulation support

## Critical Integration Points
- Exhaust volume affects makeup air requirements
- Heat recovery integration with heating system
- Ductwork coordination with building structure
- Filtration and treatment requirements
- Exhaust outlet placement for safety and compliance

## Constraint Notes
- Equipment exhaust must be safely captured at source
- Exhaust volume determines fan sizing
- Filtration requirements based on equipment type
- Exhaust outlet must meet environmental standards
- System must be cleanable and maintainable

## Dependency Map
```
Equipment Location --> DEL-013-04 (Equip Exhaust)
                         |
              DEL-013-02 (Exchanger)
              DEL-013-03 (Makeup Air)
              DEL-013-01 (Heating/Recovery)
```

---

## Extracted Dependency Register

**Total rows:** 17 | **ACTIVE:** 17 | **RETIRED:** 0

### ANCHOR Dependencies (3 rows)

| DependencyID | AnchorType | TargetType | TargetRefID / TargetName | Confidence | Status |
|---|---|---|---|---|---|
| DEP-013-04-A01 | IMPLEMENTS_NODE | WBS_NODE | SOW-0038 | HIGH | ACTIVE |
| DEP-013-04-A02 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-001 | HIGH | ACTIVE |
| DEP-013-04-A03 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-004 | HIGH | ACTIVE |

### EXECUTION Dependencies (14 rows)

| DependencyID | Direction | DependencyType | TargetType | Target | Confidence | EstimateImpact | Status |
|---|---|---|---|---|---|---|---|
| DEP-013-04-E01 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-003-04 Exhaust System Plans | HIGH | BLOCKING | ACTIVE |
| DEP-013-04-E02 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-003-05 Mechanical Equipment Schedule | HIGH | BLOCKING | ACTIVE |
| DEP-013-04-E03 | UPSTREAM | PREREQUISITE | PACKAGE | PKG-010 Foundation Construction | HIGH | BLOCKING | ACTIVE |
| DEP-013-04-E04 | UPSTREAM | PREREQUISITE | PACKAGE | PKG-011 Building Structure & Envelope | HIGH | BLOCKING | ACTIVE |
| DEP-013-04-E05 | UPSTREAM | PREREQUISITE | EXTERNAL | County Equipment Fleet Data | HIGH | BLOCKING | ACTIVE |
| DEP-013-04-E06 | UPSTREAM | CONSTRAINT | EXTERNAL | Environmental Compliance Approval | HIGH | BLOCKING | ACTIVE |
| DEP-013-04-E07 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-015-04 Equipment Power Circuits | HIGH | ADVISORY | ACTIVE |
| DEP-013-04-E08 | UPSTREAM | INTERFACE | PACKAGE | PKG-002 Structural Design | MEDIUM | ADVISORY | ACTIVE |
| DEP-013-04-E09 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-013-05 Welding Station Exhaust System | HIGH | ADVISORY | ACTIVE |
| DEP-013-04-E10 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-013-03 Forced-Air Makeup System | HIGH | ADVISORY | ACTIVE |
| DEP-013-04-E11 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-013-03 Forced-Air Makeup System | MEDIUM | ADVISORY | ACTIVE |
| DEP-013-04-E12 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-013-01 High-Recovery Heating System | LOW | INFO | ACTIVE |
| DEP-013-04-E13 | UPSTREAM | PREREQUISITE | EXTERNAL | Shop Floor Plan Finalization | HIGH | BLOCKING | ACTIVE |
| DEP-013-04-E14 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-013-02 High-Volume Air Exchanger | MEDIUM | INFO | ACTIVE |

---

## Run Notes

**Run date:** 2026-02-26
**Mode:** UPDATE (initial run; no prior Dependencies.csv)
**Strictness:** CONSERVATIVE
**Consumer context:** TASK_ESTIMATING

### Defaults and Paths Used
- **RUN_ROOT:** `/Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude`
- **DECOMPOSITION_PATH:** `_Decomposition/WDMLRL_Decomposition_Claude.md` (found and validated)
- **ANCHOR_DOC:** `Datasheet.md` (selected: contains Identification table with SOW-0038, OBJ-001, OBJ-004)
- **EXECUTION_DOC_ORDER:** `Procedure.md` (primary; strongest prerequisite/workflow signal), `Specification.md`, `Guidance.md`
- **SOURCE_DOCS:** `Datasheet.md`, `Procedure.md`, `Specification.md`, `Guidance.md` (AUTO scan; excluded `_CONTEXT.md`, `_REFERENCES.md`, `_DEPENDENCIES.md`, `_SEMANTIC.md`, `_SEMANTIC_LENSING.md`, `_STATUS.md`)
- **_REFERENCES.md:** Read; used for document pointer resolution (no new dependency rows emitted from it alone)

### Decomposition Validation
- SOW-0038 confirmed in Decomposition Scope Ledger (line 634): IN scope, mapped to PKG-013, DEL-013-04, linked to OBJ-001 and OBJ-004.
- DEL-013-04 confirmed in Decomposition Deliverable Table (line 504): "Heavy Equipment Exhaust System", Mechanical Contractor, Installation, SOW-0038, OBJ-001/OBJ-004.
- All target deliverable IDs (DEL-003-04, DEL-003-05, DEL-013-01, DEL-013-02, DEL-013-03, DEL-013-05, DEL-015-04) confirmed in Decomposition Deliverable Table.
- All target package IDs (PKG-002, PKG-003, PKG-010, PKG-011, PKG-013, PKG-015) confirmed in Decomposition Package Table.

### Warnings
None.

### Assumptions Logged
- DEP-013-04-E12 (heat recovery interface with DEL-013-01): Marked ASSUMPTION per Specification REQ-007 labeling. Confidence LOW. See Guidance CQ-001.

### Items Not Extracted (conservative exclusion)
- **DEL-013-06 (Ceiling Fans):** Listed in `_DEPENDENCIES.md` declared list as "Distributed air circulation support" but no source document states an explicit information transfer, prerequisite, or artifact dependency between DEL-013-04 and DEL-013-06. Excluded per CONSERVATIVE strictness (coordination only).
- **Mechanical Contractor availability:** Listed in declared External Dependencies but is a resource/scheduling dependency, not an information-flow or artifact-transfer dependency. Excluded per protocol.
- **Filtration and treatment requirements:** Listed in Critical Integration Points but is an internal design decision within DEL-013-04 scope (CQ-002), not an inter-deliverable dependency. Referenced within E05 (equipment data) and E06 (environmental review) as contributing factors.

---

## Run History

| Run | Date | Mode | Strictness | Consumer | Decomp Status | Warnings | ANCHOR Active | EXECUTION Active | Total Active |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 2026-02-26 | UPDATE | CONSERVATIVE | TASK_ESTIMATING | Validated | None | 3 | 14 | 17 |

---

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 17 |
| RETIRED | 0 |

| SatisfactionStatus | Count |
|---|---|
| TBD | 5 |
| PENDING | 12 |

| DependencyClass | Count |
|---|---|
| ANCHOR | 3 |
| EXECUTION | 14 |

| EstimateImpactClass | Count |
|---|---|
| BLOCKING | 7 |
| ADVISORY | 5 |
| INFO | 2 |
| TBD | 3 |

---

## Downstream Handoff Notes

**Consumer context:** TASK_ESTIMATING

The following observations are provided for downstream task estimating workflows:

1. **7 BLOCKING dependencies** gate meaningful estimating for DEL-013-04. The most critical are:
   - **DEL-003-04 (Exhaust System Plans)** and **DEL-003-05 (Equipment Schedule)** from PKG-003 Mechanical Design: without IFC drawings and fan/equipment specifications, the installation scope cannot be quantified for estimating. These are the primary design-to-installation handoffs.
   - **County Equipment Fleet Data (EXTERNAL):** exhaust volumes, equipment types, and engine data must be obtained from the County before fan sizing, duct sizing, hose selection, and filtration determination can proceed. This is the single most significant external data gap affecting estimating precision.
   - **Environmental Compliance Approval (EXTERNAL):** outlet/stack design and any filtration requirements depend on environmental review outcome. Affects scope of filtration (in/out per CQ-002) and stack design.
   - **PKG-010/PKG-011 (structural prerequisites):** building must be substantially complete before installation. Standard construction sequencing.
   - **Shop Floor Plan Finalization (EXTERNAL):** equipment positions determine hose drop locations and duct routing.

2. **5 ADVISORY dependencies** may affect quantities or approach but do not gate estimating:
   - Electrical interface (DEL-015-04): fan circuit sizing and controls wiring.
   - Structural coordination (PKG-002): ductwork clearance with crane runways.
   - Welding exhaust separation (DEL-013-05): ductwork routing constraint.
   - Makeup air bidirectional interface (DEL-013-03): exhaust volume data exchange.

3. **2 INFO dependencies** provide context but are unlikely to change estimate totals:
   - Heat recovery interface (DEL-013-01): ASSUMPTION only; likely not cost-effective per Guidance analysis.
   - Air exchanger coordination (DEL-013-02): general air balance context.

4. **Key estimating risk:** Multiple TBD items in the Datasheet (TBD-DS-01 through TBD-DS-05) and unresolved Conflict Table items (CQ-001 through CQ-005) indicate that the design input chain from PKG-003 and the County is not yet mature enough for detailed quantity takeoff. Estimating should use parametric or analogous methods with appropriate contingency until BLOCKING dependencies are satisfied.
