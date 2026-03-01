# DEL-012-01: Parts Storage Room - Dependencies

## Dependency Status
**Tracking Status**: TRACKED
**Register Schema Version**: v3.1
**Last Run**: 2026-02-26

## External Dependencies
- Facility shell construction completion
- Utility infrastructure (electrical, plumbing, HVAC) routing
- Design finalization and approval
- General Contractor availability and scheduling

## Internal Package Dependencies
- **DEL-012-02** (Utility Room): Coordinate timing and utility connections
- **DEL-012-03** (Office Space): Coordinate access routes and safety protocols

## PKG-013 Dependencies
- **PKG-013** (Mechanical & HVAC Installation): HVAC system routing through storage room
  - DEL-013-01: Heating System
  - DEL-013-02: Air Exchanger
  - DEL-013-03: Makeup Air System

## Constraint Notes
- Environmental control system must be operational before storage placement
- Access routes must be finalized before fixture installation
- Safety inspections required before occupancy

## Dependency Map
```
Facility Shell --> DEL-012-01 (Storage) --> Storage Operations
                |
          PKG-013 HVAC Systems
```

---

## Extracted Dependency Register

**Total ACTIVE rows**: 21
**Total RETIRED rows**: 0

| Class | Count |
|---|---|
| ANCHOR | 2 |
| EXECUTION | 19 |

### ANCHOR Rows (2 ACTIVE)

| DependencyID | AnchorType | TargetType | TargetRefID / TargetName | Confidence |
|---|---|---|---|---|
| DEP-012-01-A001 | IMPLEMENTS_NODE | WBS_NODE | SOW-0029 | HIGH |
| DEP-012-01-A002 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-001 | HIGH |

### EXECUTION Rows (19 ACTIVE)

| DependencyID | Direction | DependencyType | TargetType | Target | Confidence | EstimateImpactClass |
|---|---|---|---|---|---|---|
| DEP-012-01-E001 | UPSTREAM | PREREQUISITE | PACKAGE | PKG-011 Building Structure & Envelope | HIGH | BLOCKING |
| DEP-012-01-E002 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-011-07 Mezzanine Structure & Stairs | HIGH | BLOCKING |
| DEP-012-01-E003 | UPSTREAM | PREREQUISITE | PACKAGE | PKG-013 Mechanical & HVAC Installation | HIGH | BLOCKING |
| DEP-012-01-E004 | UPSTREAM | PREREQUISITE | PACKAGE | PKG-015 Electrical & Low-Voltage Installation | HIGH | BLOCKING |
| DEP-012-01-E005 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-013-01 High-Recovery Heating System | HIGH | ADVISORY |
| DEP-012-01-E006 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-013-02 High-Volume Air Exchanger | HIGH | ADVISORY |
| DEP-012-01-E007 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-013-03 Forced-Air Makeup System | HIGH | ADVISORY |
| DEP-012-01-E008 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-015-02 Lighting Installation | HIGH | ADVISORY |
| DEP-012-01-E009 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-015-04 Equipment Power Circuits | HIGH | ADVISORY |
| DEP-012-01-E010 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-015-03 Receptacle Installation | MEDIUM | ADVISORY |
| DEP-012-01-E011 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-001-08 Finish Schedule | HIGH | BLOCKING |
| DEP-012-01-E012 | UPSTREAM | CONSTRAINT | DOCUMENT | SOW-0018 IFC Drawings (P.Eng.-stamped) | HIGH | BLOCKING |
| DEP-012-01-E013 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-012-02 Utility Room | MEDIUM | ADVISORY |
| DEP-012-01-E014 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-012-03 Office Space | MEDIUM | INFO |
| DEP-012-01-E015 | UPSTREAM | CONSTRAINT | REQUIREMENT | REQ-012-01-012 HVAC operational before storage | HIGH | BLOCKING |
| DEP-012-01-E016 | UPSTREAM | PREREQUISITE | EXTERNAL | Alberta Safety Codes Permits and Inspections | HIGH | BLOCKING |
| DEP-012-01-E017 | UPSTREAM | PREREQUISITE | EXTERNAL | Development and Building Permits | HIGH | BLOCKING |
| DEP-012-01-E018 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-002-05 Mezzanine Framing Details | HIGH | BLOCKING |
| DEP-012-01-E019 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-020-02 Final Inspection & CCC | MEDIUM | INFO |

---

## Run Notes

**Run Date**: 2026-02-26
**Mode**: UPDATE
**Strictness**: CONSERVATIVE
**Consumer Context**: TASK_ESTIMATING

### Defaults and Paths Used
- **RUN_ROOT**: `/Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude`
- **DECOMPOSITION_PATH**: `/Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/_Decomposition/WDMLRL_Decomposition_Claude.md` (found and used)
- **ANCHOR_DOC**: `Datasheet.md` (selected: highest-confidence anchor signal -- contains SOW Reference, Objective Linkage, Package identity)
- **EXECUTION_DOC_ORDER**: `Procedure.md`, `Specification.md`, `Guidance.md`, `Datasheet.md`
- **SOURCE_DOCS scanned**: `Datasheet.md`, `Guidance.md`, `Procedure.md`, `Specification.md`, `_DEPENDENCIES.md` (declared), `_CONTEXT.md`, `_REFERENCES.md`
- **_REFERENCES.md**: Read; used for document pointer context but no additional dependencies derived solely from it.

### Decomposition Validation
- Decomposition file located and read successfully.
- DEL-012-01 confirmed in decomposition deliverables table (line 493): `DEL-012-01_Parts-Room | Parts Storage Room | General Contractor | Construction | SOW-0029 | OBJ-001`
- SOW-0029 confirmed in scope ledger (line 625): `SOW-0029 | IN | PKG-012 | DEL-012-01 | OBJ-001`
- OBJ-001 confirmed in objectives table (line 302).
- All target deliverable IDs (DEL-011-07, DEL-013-01, DEL-013-02, DEL-013-03, DEL-015-02, DEL-015-03, DEL-015-04, DEL-001-08, DEL-012-02, DEL-012-03, DEL-002-05, DEL-020-02) confirmed present in decomposition deliverables table.
- All target package IDs (PKG-011, PKG-013, PKG-015, PKG-001, PKG-002, PKG-012, PKG-020) confirmed present in decomposition packages table.

### Warnings
- None.

### Assumptions
- DEP-012-01-E012: IFC Drawings (SOW-0018) treated as `TargetType=DOCUMENT` rather than DELIVERABLE because SOW-0018 is a cross-cutting production obligation ("produce all IFC drawings"), not a single deliverable.
- DEP-012-01-E015: REQ-012-01-012 is a locally-defined requirement within this deliverable's Specification; treated as `TargetType=REQUIREMENT` capturing the constraint that HVAC must be operational before occupancy.
- Plumbing rough-in (PKG-014) was noted in Procedure Section 2.2 Row 5 but explicitly states "no plumbing expected in parts room per available drawings; confirm in design." Under CONSERVATIVE strictness, no dependency row emitted for PKG-014 because no explicit plumbing requirement exists for this room.

---

## Run History

| Run | Date | Mode | Strictness | Consumer | Decomposition | Warnings | ACTIVE Anchors | ACTIVE Execution | Total ACTIVE |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 2026-02-26 | UPDATE | CONSERVATIVE | TASK_ESTIMATING | Found and used | None | 2 | 19 | 21 |

---

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 21 |
| RETIRED | 0 |

| SatisfactionStatus | Count |
|---|---|
| PENDING | 19 |
| NOT_APPLICABLE | 2 |

| DependencyClass | ACTIVE | RETIRED |
|---|---|---|
| ANCHOR | 2 | 0 |
| EXECUTION | 19 | 0 |

---

## Downstream Handoff Notes

**Consumer Context**: TASK_ESTIMATING

The following observations are relevant for task estimating workflows consuming this register:

### Blocking Dependencies (10 rows, EstimateImpactClass=BLOCKING)
These dependencies represent hard gates that must be satisfied before meaningful estimating of this deliverable's construction scope can proceed:

1. **DEP-012-01-E001** (PKG-011 Building Shell): The entire interior fit-out is gated by building shell completion. Estimating must account for the shell construction timeline.
2. **DEP-012-01-E002** (DEL-011-07 Mezzanine): Mezzanine structure completion gates partition construction. A HOLD POINT exists for structural interface verification.
3. **DEP-012-01-E003** (PKG-013 Mechanical rough-in): HVAC ductwork stub-outs must be complete before partitions are built around them.
4. **DEP-012-01-E004** (PKG-015 Electrical rough-in): Conduit and boxes must be in place before partitions close off the wall cavities.
5. **DEP-012-01-E011** (DEL-001-08 Finish Schedule): Finish materials and quantities cannot be estimated until the Architect's finish schedule is produced.
6. **DEP-012-01-E012** (IFC Drawings): No construction can begin without P.Eng.-stamped IFC drawings. This is a HOLD POINT.
7. **DEP-012-01-E015** (HVAC Commissioning Constraint): Occupancy/operational readiness is gated by HVAC commissioning -- affects schedule tail.
8. **DEP-012-01-E016** (Safety Codes Permits): Regulatory prerequisite before construction and before occupancy.
9. **DEP-012-01-E017** (Development/Building Permits): Regulatory prerequisite before construction.
10. **DEP-012-01-E018** (DEL-002-05 Mezzanine Framing Details): Structural design drawings required for partition-to-mezzanine interface -- affects partition scope definition.

### Advisory Dependencies (7 rows, EstimateImpactClass=ADVISORY)
These dependencies may change quantities, specifications, or procurement approach but are not hard gates:

- HVAC system interfaces (DEL-013-01, DEL-013-02, DEL-013-03): May affect register/diffuser locations, penetration sizes, and coordination scope.
- Electrical interfaces (DEL-015-02 Lighting, DEL-015-04 Door Power, DEL-015-03 Receptacles): May affect blocking, rough opening counts, and coordination scope.
- DEL-012-02 (Utility Room): Adjacent room -- coordination affects access and sequencing.

### Key Estimating Uncertainties
- Shelving type, capacity, and configuration are TBD (no specification yet).
- Roll-up door type (manual vs. motorized) is TBD (Guidance CF-001).
- Wall, floor, and ceiling finish specifications depend on DEL-001-08 (Finish Schedule) which does not yet exist.
- Fire-rated partition requirement is TBD pending code consultant review (Guidance CF-005).
