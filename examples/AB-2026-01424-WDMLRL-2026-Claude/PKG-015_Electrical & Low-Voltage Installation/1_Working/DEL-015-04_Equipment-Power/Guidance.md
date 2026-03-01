# Guidance — DEL-015-04 Equipment Power Circuits

---

## Purpose

This deliverable provides dedicated electrical power circuits for the facility equipment that is central to the operational program of the New North Shop Addition. The equipment served — overhead cranes, overhead doors, air compressor, fire hose pump, pressure washer, and exhaust fans — represents the working heart of the maintenance shop. Without reliable, correctly rated dedicated circuits for each load, the building cannot fulfill its primary function of servicing and maintaining heavy landfill equipment.

This guidance document is intended to help the Electrical Contractor, Electrical Engineer (PKG-004), and Project Manager understand the intent behind the requirements, the key decision points, and the risks to be managed during design and installation.

**Source:** Decomposition OBJ-001, OBJ-005; _CONTEXT.md; RFP §3.4

---

## Principles

1. **Equipment load data drives circuit design.** The amperage values stated in App B-Elec (40 A compressor, 70 A fire hose pump, 70 A pressure washer) are the Owner's anticipated values. Final circuit design must be validated against the actual equipment nameplates and manufacturer installation requirements. The Electrical Engineer (PKG-004) is responsible for confirming or revising these values in the IFC design.

   **Source:** App B-Elec; RFP §3.4 (design-build obligation — Contractor determines final design)

2. **Crane circuits require early coordination.** Overhead crane power supply is technically the most complex element in this deliverable. The supply method (conductor bar, festoon cable, or bus duct) must be coordinated between the Electrical Engineer (PKG-004), the Structural Engineer (PKG-002, crane support structure), and the Crane Contractor (PKG-016) before IFC drawings are finalized. Crane procurement (DEL-016-01) should be initiated early to obtain manufacturer's electrical requirements.

   **Source:** Decomposition SOW-0059, SOW-0067; _DEPENDENCIES.md

3. **Dedicated circuits protect critical equipment.** Each major equipment load is assigned a dedicated circuit rather than shared branch circuits. This protects against nuisance tripping, enables accurate load management, and supports future troubleshooting. ASSUMPTION: this principle is consistent with CEC requirements for motor loads above certain thresholds.

   **Source:** ASSUMPTION based on standard electrical practice and CEC motor circuit requirements; App B-Elec

4. **Three-phase power availability governs equipment selection.** The building runs on three-phase power (SOW-0051). Equipment that benefits from three-phase supply (cranes, larger pumps, compressors) should be selected accordingly. The Electrical Engineer should confirm phase requirements for each load in the load calculations (DEL-004-08).

   **Source:** RFP §3.4 ("The Proposed building shall run on three-phase power"); SOW-0051

5. **Safety Code compliance is non-negotiable.** All work must pass Alberta Safety Code electrical inspections. County representatives must be present at inspections; copies of all inspection reports must be provided to the Owner. Deficiencies must be rectified promptly.

   **Source:** RFP §3.3.2; RFP §2.10

---

## Considerations

### Crane Power Supply Method
The choice of crane power supply method (conductor bar system, festoon cable, or rigid bus duct) has implications for maintenance, safety, and cost. Conductor bar systems are common for overhead cranes in industrial maintenance shops and allow full travel along the crane runway without cable management issues. Festoon cable is simpler but may limit travel range and has a higher maintenance burden. The structural crane rails (DEL-011, crane supports DEL-002-07) must be coordinated with the power supply route. ASSUMPTION: this decision requires input from the crane supplier (DEL-016-01) and is therefore TBD until crane procurement advances.

**Source:** ASSUMPTION based on standard industrial crane electrical practice

### Overhead Door Quantity and Circuit Count
App B-Elec states "Will need power for … Overhead Doors" without specifying the number of circuits or ratings. App B-Shop drawing shows multiple overhead doors (24' wide bays, wash bay, parts room roll-up door). Each door operator is typically a separate circuit. The IFC electrical design (DEL-004) must enumerate all door operators and assign circuits accordingly.

**Source:** App B-Elec; App B-Shop (floor plan, door locations); Decomposition SOW-0025, SOW-0029, SOW-0060

### Exhaust Fan Count and Location
App B-Elec shows the exhaust fan symbol ("E") at the welding station area. However, the overall building program includes other areas requiring ventilation (e.g., repair bay exhaust hoses per SOW-0038 are mechanical scope, not electrical; service pit ventilation per SOW-0028 may include an electrical exhaust fan). Scope boundary between DEL-015-04 (exhaust fans per SOW-0066) and mechanical exhaust systems (PKG-013) must be clarified in the IFC design. ASSUMPTION: SOW-0066 covers electrically-powered exhaust fans shown on the electrical drawing; mechanically-driven or duct-only exhaust is PKG-013 scope.

**Source:** App B-Elec (legend — "E Exhaust Fan"); Decomposition SOW-0038, SOW-0039, SOW-0066; ASSUMPTION

### Load Sequencing and Panel Capacity
The combination of two 5-tonne crane circuits, a 70 A fire hose pump circuit, a 70 A pressure washer circuit, and a 40 A compressor circuit represents a significant aggregate electrical load in addition to the other PKG-015 circuits (lighting, receptacles). The Electrical Engineer must ensure the main service and distribution panel capacity (DEL-015-01, DEL-004-02) accommodate all concurrent loads without exceeding panel ratings. Load calculations (DEL-004-08) are critical.

**Source:** ASSUMPTION based on aggregate circuit ampacity analysis requirement; Decomposition SOW-0051, SOW-0014

### Coordination with Commissioning (DEL-020-01)
Equipment circuit commissioning requires the associated equipment to be in place and ready for test. Sequencing must be managed so that crane installation (DEL-016-01), door operator installation, and mechanical equipment installation are complete before final energization and functional testing of these circuits. This coordination is a project scheduling responsibility (PKG-019).

**Source:** Decomposition DEL-020-01; OBJ-005

### Installation Sequencing Priority
**[D-003]** The seven circuit types in this deliverable have different coordination dependencies, risk profiles, and lead times. Guidance on installation priority sequencing is TBD, but the following factors should inform the sequence:

- **Crane circuits (C-01, C-02)** may require the longest lead time due to structural coordination (crane runway must be in place) and dependency on crane procurement (DEL-016-01). ASSUMPTION: crane circuits should be among the first to be roughed-in (conduit/raceway) once structural steel is complete, even if the crane power supply system is installed later when manufacturer data is available.
- **Exhaust fan circuits (C-07)** have an unresolved scope boundary (CON-015-04-001) and should be deferred until scope is clarified per Step 1.4 of the Procedure.
- **Compressor (C-04), fire hose pump (C-05), and pressure washer (C-06)** circuits have known amperage values and can proceed once IFC design is finalized.
- **Overhead door circuits (C-03)** depend on door count and operator specifications being confirmed.

TBD — a formal installation priority recommendation should be developed by the Project Manager / Electrical Contractor based on the construction schedule and equipment procurement timeline.

**Source:** ASSUMPTION based on coordination dependencies described in this Guidance and Procedure documents; Decomposition SOW-0059 through SOW-0066

### Workmanship Quality Standards
**[F-003]** Beyond code compliance and functional testing, the following workmanship quality considerations apply to this deliverable. TBD — the gap between "passes inspection" and "quality installation" should be addressed:

- **Termination quality:** TBD — torque specifications for lugs and terminals should be per connector manufacturer's published values. Anti-oxidant compound required for aluminum conductors if used (ASSUMPTION: standard practice per CEC and manufacturer requirements).
- **Conduit installation:** Neat, consistently supported conduit runs per CEC spacing requirements and project quality expectations.
- **Labeling:** Consistent, durable labeling of all circuits at the panel and at each disconnect per CEC and project requirements.
- **General workmanship:** Per CCDC 14 quality provisions and Electrical Contractor best practices.

TBD — confirm whether the project has an explicit workmanship standard or quality specification beyond CEC compliance. Source: CCDC 14 quality provisions / Electrical Contractor best practices; **location TBD**

---

## Trade-offs

| Trade-off | Option A | Option B | Recommended Approach |
|---|---|---|---|
| Crane power supply method | Conductor bar (more durable, full travel) | Festoon cable (lower cost, simpler) | TBD — defer to crane manufacturer's requirements and Electrical Engineer recommendation; ASSUMPTION: conductor bar preferred for industrial maintenance shop environment |
| Compressor circuit voltage | 240 V single-phase | 3-phase (208V or 600V depending on service) | TBD — depends on compressor selection; 3-phase preferred for larger compressors for efficiency and motor longevity — ASSUMPTION |
| Pump/pressure washer circuit sizing | Size per App B-Elec values (70 A each) | Resize per actual equipment nameplate | Size per actual nameplate; App B-Elec values are design intent; IFC design must verify |

---

## Examples

No directly accessible source examples are available for this specific project. The following general patterns are noted from standard industrial electrical practice (ASSUMPTION — not derived from accessible project sources):

- For 5-tonne industrial overhead cranes, three-phase power feeds are typical, with conductor bar or enclosed bus duct supplying the crane runway. The Crane Contractor typically provides the runway electrification materials; the Electrical Contractor provides the feed circuit to the runway power supply unit.
- Motor circuit disconnecting means are typically located within sight of the motor/equipment they serve per standard electrical code practice.

These patterns should be validated against the IFC design and crane manufacturer's requirements when available.

---

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|---|---|---|---|---|---|---|
| CON-015-04-001 | App B-Elec shows "E" exhaust fan symbol at welding station. Decomposition SOW-0066 says "Install exhaust fan(s) as shown on electrical drawing." Decomposition SOW-0038 (PKG-013 scope) says "Install exhaust hoses and fans for heavy equipment." It is unclear whether the "E" symbols on the electrical drawing represent all exhaust fans in this deliverable, or only some (e.g., welding exhaust fan), with repair bay fans covered under PKG-013. **[X-001]** Confirmed unresolved through semantic lensing — substantiated governance scope is undermined until this scope boundary is resolved. | App B-Elec (Electrical Legend — E symbol locations); SOW-0066 | Decomposition SOW-0038; PKG-013 inclusion criteria | Specification REQ-015-04-006; Guidance Considerations (Exhaust Fan Count) | IFC electrical and mechanical drawings should resolve the scope boundary; pending IFC, treat SOW-0066 as covering all fans shown on the electrical drawing only | TBD |
| CON-015-04-002 | App B-Elec (conceptual) states "Will need power for crane and Overhead Doors" without specifying circuit ratings for cranes or door operators. Decomposition SOW-0059 covers crane power and SOW-0060 covers overhead door power, but no amperage is stated. The 40A/70A values are explicitly stated for compressor/pump/washer but crane and door ratings are absent from all accessible sources. | App B-Elec (notes — crane and door power mentioned without ratings); SOW-0059, SOW-0060 | No accessible source provides crane or door circuit ratings | Datasheet (Attributes — C-01 through C-03); Specification REQ-015-04-001, REQ-015-04-002 | Electrical Engineer (DEL-004-06 panel schedules) governs; crane manufacturer's data required | TBD |
| CON-015-04-003 | **[X-003]** Verification checks reference "connections tight" (Procedure Step 5.2) but no measurable standard for termination quality is provided. Torque specifications for lugs/terminals and anti-oxidant requirements for aluminum conductors (if used) are not stated anywhere in the production documents. The gap between "passes visual inspection" and "verified termination quality" is unaddressed. | Specification Verification table (general); Procedure Step 5.2 ("all connections tight") | No accessible source provides torque specifications or termination quality standards for this project | Specification Verification; Procedure Step 5.2; Guidance Workmanship Quality Standards | CEC / connector manufacturer torque specifications should govern; **location TBD** | TBD |
