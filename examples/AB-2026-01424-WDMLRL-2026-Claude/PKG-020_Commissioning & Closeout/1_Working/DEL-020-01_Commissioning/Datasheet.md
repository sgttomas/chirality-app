# Datasheet — DEL-020-01: Building Systems Commissioning

**Document Type:** Datasheet (descriptive)
**Deliverable ID:** DEL-020-01_Commissioning
**Package:** PKG-020 — Commissioning & Closeout
**Generated:** 2026-02-26 (Pass 1+2, P1_P2 run)
**Enriched:** 2026-02-26 (Pass 3, Semantic Lensing)

---

## Identification

| Field | Value |
|---|---|
| Deliverable ID | DEL-020-01_Commissioning |
| Deliverable Name | Building Systems Commissioning |
| Package | PKG-020 — Commissioning & Closeout |
| Package Description | Systems commissioning, final self-inspection, CCC documentation, WCB clearance, statutory declaration, payment claim letter |
| Deliverable Type | Commissioning |
| Responsible Party | Commissioning Agent / Project Manager |
| SOW Coverage | SOW-0090 |
| Supported Objectives | OBJ-001, OBJ-002, OBJ-004, OBJ-005 |
| Contract Form | CCDC 14–2013 Design-Build Stipulated Price |
| Owner | Camrose County |
| Project | 2026 Design Build — West Dried Meat Lake Regional Landfill Maintenance Shop Addition |
| Location | SW 14–44–21–W4, near Ferintosh, Alberta |

Sources: `_CONTEXT.md`; Decomposition §7 PKG-020; Decomposition §6 PKG-020.

---

## Attributes

### Building Systems Subject to Commissioning

The RFP requires commissioning of "all building systems" (SOW-0090, R-01 §1.0). The specific systems installed and therefore subject to commissioning are derived from the project design requirements (RFP §3.4) and the decomposition objectives (OBJ-004, OBJ-005):

| System Category | Systems (from RFP §3.4 and Decomposition OBJ-004/005) | Commissioning Status |
|---|---|---|
| Mechanical / HVAC | High recovery heating system; high volume air exchanger; exhaust hoses and fans; ventilation at welding station; ceiling fans | To be commissioned (TBD — specific test criteria) |
| Plumbing & Water | 50,000 L cistern; pump (100 LPM, 2.5" fill connection); septic holding tank (2,000 US Gallon); wash bay drainage; mud sump; emergency shower; floor/sump drains; bulk water fill | To be commissioned (TBD — specific test criteria) |
| Electrical & Low-Voltage | Three-phase power distribution; lighting (all areas); receptacles (15A through 50A / welding circuits); crane power circuits; overhead door power; security camera wiring; radio antenna wiring | To be commissioned (TBD — specific test criteria) |
| Crane & Lifting | Two (2) 5-tonne overhead cranes on trolley | To be commissioned (TBD — load test specifics) |
| Building Envelope Systems | Overhead doors; entrance doors; service pit ventilation/lighting | To be commissioned (TBD — functional test criteria) |
| Safety & Emergency Systems | Emergency shower (performance parameters TBD — flow rate, activation method, compliance standard per Alberta OH&S requirements) | To be commissioned (TBD — specific test criteria) |

ASSUMPTION: The system list above is derived from RFP §3.4 design requirements and Decomposition OBJ-004/OBJ-005. Specific commissioning scope per system (e.g., which items require formal functional testing vs. visual inspection) must be confirmed in the Commissioning Plan.

**Note [B-001]:** The emergency shower is referenced in Procedure testing steps (Step 6, Step 9) as a testable system but was not previously enumerated as a distinct safety system category. Emergency shower performance parameters (flow rate, activation method, compliance standard) are TBD pending identification of applicable Alberta OH&S requirements. (Source: Procedure.md Step 6, Step 9; _SEMANTIC_LENSING.md B-001. ProposedAuthority: Alberta OH&S requirements for emergency showers.)

**Note [E-001]:** The wash bay appears in Procedure testing under both plumbing systems (Step 6 — drainage) and building envelope systems (Step 7 — enclosure). For commissioning scope purposes, the wash bay is treated as a cross-discipline system: its drainage and mud sump components are tested under Plumbing & Water; its enclosure components are tested under Building Envelope Systems. This dual categorization is intentional and is reflected in the Procedure step assignments. (Source: Procedure.md Steps 6, 7; _SEMANTIC_LENSING.md E-001. ProposedAuthority: Commissioning Plan system categorization.)

### Facility Context

| Attribute | Value | Source |
|---|---|---|
| Building area | Approximately 13,000 sq ft (new addition) | RFP §3.1 |
| Ceiling height | 35 ft (concrete structure) | RFP §3.4 |
| Power supply | Three-phase | RFP §3.4 |
| Facility type | Industrial maintenance shop addition | RFP §1.2 |
| Site location | SW-14-44-21-W4, Camrose County, Alberta | RFP §3.1; Decomposition §1 |
| Existing building | Old North Shop — partial renovation included | RFP §3.1, §3.4 |

**Note [B-002]:** The Old North Shop is noted as having "partial renovation included" per RFP §3.1 and §3.4, but it is unclear whether renovation-area systems require commissioning under DEL-020-01, or whether commissioning is limited to the new addition only. This scope determination is TBD and must be resolved by reference to the RFP renovation scope sections (RFP §3.1, §3.4). (Source: Datasheet.md Facility Context; _SEMANTIC_LENSING.md B-002. ProposedAuthority: RFP §3.1, §3.4 — renovation scope.)

### Commissioning Milestone Constraints

| Constraint | Value | Source |
|---|---|---|
| Project completion deadline | On or before December 31, 2026 | SOW-0091; RFP §3.1 |
| Commissioning start prerequisite | Substantial completion of all construction (PKG-019 sign-off) | `_DEPENDENCIES.md`; Decomposition PKG-020 |
| Commissioning sequence | Precedes final inspection (DEL-020-02) and closeout documentation (DEL-020-03) | `_DEPENDENCIES.md` |
| Owner representative involvement | County project manager to coordinate inspections | RFP §3.1 |

---

## Conditions

### Entry Conditions (Prerequisites)

| Condition | Source |
|---|---|
| All construction activities substantially complete (PKG-019 sign-off) | `_DEPENDENCIES.md` |
| QC management verification complete (DEL-019-04) | `_DEPENDENCIES.md`; Decomposition PKG-019 |
| All trade installations complete: mechanical (PKG-013), plumbing (PKG-014), electrical (PKG-015), crane (PKG-016) | Decomposition PKG-020 Exclusions; `_DEPENDENCIES.md` |
| IFC drawings and applicable Safety Code permits on hand | ASSUMPTION — standard commissioning precondition for Alberta |
| All applicable Safety Code inspections passed (PKG-009) | Decomposition PKG-009; RFP §3.3.2 |
| Commissioning Agent assigned | `_STATUS.md` Outstanding Items |

### Exit Conditions (Completion Criteria)

| Condition | Source |
|---|---|
| All building systems functionally tested per specifications | SOW-0090; RFP §1.0 |
| Performance criteria met or exceeded for each system | `_CONTEXT.md` Success Criteria |
| Operator training completed | `_CONTEXT.md` Scope Definition |
| Commissioning reports documented | `_CONTEXT.md` Success Criteria |
| Facility confirmed ready for occupancy | `_CONTEXT.md` Success Criteria |
| Documentation compiled and delivered to Owner | `_CONTEXT.md` Scope Definition |
| Final inspection readiness confirmed (handoff to DEL-020-02) | `_DEPENDENCIES.md` |

---

## Construction

### Commissioning Process Overview

ASSUMPTION: The following process structure reflects standard practice for design-build industrial facility commissioning in Alberta. Specific protocols are TBD pending Commissioning Plan development.

| Phase | Activities |
|---|---|
| Pre-Commissioning Planning | Develop Commissioning Plan; establish system-by-system test protocols; confirm acceptance criteria with Owner |
| Functional Testing | Individual system startup and functional test per discipline (mechanical, plumbing, electrical, crane) |
| Integrated Systems Testing | Cross-system verification (e.g., power to HVAC, crane interlock with electrical, plumbing pressure/flow) |
| Performance Verification | Verify each system meets specified performance parameters (flow rates, capacities, electrical loads) |
| Operator Training | Train County facility staff on operation and maintenance of commissioned systems |
| Documentation Compilation | Compile test records, O&M manuals, as-built drawings, training logs |
| As-Built Verification | Verify as-built drawings accurately reflect installed conditions during commissioning (see Procedure Step 9) |
| Final Review & Sign-off | Owner walkthrough; confirm commissioning complete; prepare for final inspection handoff |

### Anticipated Artifacts

The following artifacts are anticipated for this deliverable:

| Artifact | Description |
|---|---|
| Commissioning Plan | Plan document detailing scope, protocols, schedule, and responsibilities |
| System Test Records | Completed test checklists per system |
| Performance Verification Report | Summary of performance results against criteria |
| Operator Training Records | Attendance logs, training materials |
| O&M Manuals | Compiled operation and maintenance documentation for all systems |
| As-Built Drawings | Verified as-built drawings confirmed against installed conditions during commissioning (see Note [X-002]) |
| Commissioning Completion Report | Formal report confirming commissioning outcomes |

**Note [X-002]:** As-built drawings are listed as an anticipated artifact, and Procedure Step 9 references compiling as-built drawings. As-built accuracy should be verified against installed conditions as an explicit commissioning activity. This verification step has been added to Procedure Step 9. (Source: Datasheet.md Anticipated Artifacts; Procedure.md Step 9; _SEMANTIC_LENSING.md X-002. ProposedAuthority: Standard commissioning practice.)

---

## References

| Ref ID | Document | Sections Referenced |
|---|---|---|
| R-01 | AB-2026-01424-WDMLRL RFP.pdf | §1.0 (General Requirements / Scope); §3.1 (Project Background); §3.3 (Scope of Work); §3.4 (Design Requirements); §2.14 (Completion and Acceptance) |
| R-02 | AB-2026-01424-Addendum 1.pdf | §4.11 (Bid Security — not directly applicable to commissioning) |
| DECOMP | WDMLRL_Decomposition_Claude.md | §3 SOW-0090; §5 OBJ-001, OBJ-002, OBJ-004, OBJ-005; §6 PKG-020; §7 DEL-020-01; §8 Scope Ledger |
| LOCAL | `_CONTEXT.md` | All fields |
| LOCAL | `_DEPENDENCIES.md` | Upstream/downstream dependencies |
| LOCAL | `_STATUS.md` | Current state |
| LOCAL | `MEMORY.md` | Notes and outstanding questions |
