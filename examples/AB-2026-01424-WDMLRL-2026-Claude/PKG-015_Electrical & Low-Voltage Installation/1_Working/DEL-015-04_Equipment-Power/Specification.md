# Specification — DEL-015-04 Equipment Power Circuits

---

## Scope

### Included

This deliverable covers the supply and installation of all dedicated power circuits for facility equipment in the New North Shop Addition at the West Dried Meat Lake Regional Landfill, as directed by the IFC electrical design. The in-scope circuits are:

- Power circuit(s) for two (2) 5-tonne overhead cranes on trolley (SOW-0059)
- Power circuit(s) for all overhead doors (SOW-0060)
- Dedicated 40 A circuit for the air compressor (SOW-0061)
- Dedicated 70 A circuit for the fire hose pump (SOW-0062)
- Dedicated 70 A circuit for the pressure washer (SOW-0063)
- Power circuit(s) for exhaust fan(s) as shown on the IFC electrical drawing (SOW-0066)

This deliverable includes all associated conductors, conduit/raceway, overcurrent protection devices, disconnecting means, terminations, and connection to the distribution panel(s) as specified in the IFC electrical design.

**Sources:** _CONTEXT.md; Decomposition §3.G, §7 PKG-015; App B-Elec

### Excluded

- Procurement and installation of the overhead crane equipment itself (DEL-016-01, PKG-016)
- Procurement of overhead doors, compressor, fire hose pump, pressure washer, exhaust fans (equipment procurement is out of scope for this deliverable — ASSUMPTION: equipment furnished by others or separate procurement)
- Three-phase power service and main distribution panel (DEL-015-01)
- General lighting circuits (DEL-015-02)
- General receptacle circuits (DEL-015-03)
- Low-voltage systems — security cameras, radio antenna wiring (DEL-015-05)
- Electrical design and IFC drawing production (DEL-004-02 through DEL-004-09, PKG-004)

---

## Requirements

### REQ-015-04-001 — Overhead Crane Power (SOW-0059)
Power shall be provided for two (2) 5-tonne overhead cranes on trolley. Circuit voltage, amperage, and supply method shall conform to the IFC electrical design (DEL-004-02, DEL-004-06). The supply method (festoon cable, conductor bar, bus duct, or other) is TBD per IFC design.

**Source:** App B-Elec ("Will need power for crane"); Decomposition SOW-0059

### REQ-015-04-002 — Overhead Door Power (SOW-0060)
Power shall be provided for all overhead doors in the New North Shop. Circuit type, quantity, amperage, and voltage are TBD per IFC electrical design. App B-Elec shows overhead doors requiring power; door operator load data is TBD.

**Source:** App B-Elec ("Will need power for … Overhead Doors"); Decomposition SOW-0060

### REQ-015-04-003 — Air Compressor Circuit (SOW-0061)
A dedicated 40 A circuit shall be provided for the air compressor. Voltage is TBD per IFC design and compressor specifications. ASSUMPTION: circuit is 240 V single-phase or three-phase consistent with compressor nameplate requirements.

**Source:** App B-Elec ("40 Amp Compressor"); Decomposition SOW-0061

### REQ-015-04-004 — Fire Hose Pump Circuit (SOW-0062)
A dedicated 70 A circuit shall be provided for the fire hose pump. Voltage is TBD per IFC design and pump specifications.

**Source:** App B-Elec ("70 Amp Fire Hose Pump"); Decomposition SOW-0062

### REQ-015-04-005 — Pressure Washer Circuit (SOW-0063)
A dedicated 70 A circuit shall be provided for the pressure washer. Voltage is TBD per IFC design and equipment specifications.

**Source:** App B-Elec ("70 Amp Pressure Washer"); Decomposition SOW-0063

### REQ-015-04-006 — Exhaust Fan Circuit(s) (SOW-0066)
Power circuits shall be provided for exhaust fan(s) as shown on the IFC electrical drawing. The number of circuits, amperage, and voltage are TBD per IFC design. App B-Elec shows an "E" (exhaust fan) symbol at the welding station area.

**Source:** App B-Elec (legend "E — Exhaust Fan"); Decomposition SOW-0066

### REQ-015-04-007 — Code Compliance
All work shall comply with applicable Alberta Safety Codes and the Canadian Electrical Code (CEC) Part I, edition as adopted by Alberta at time of permit application (TBD — specific edition to be confirmed by IFC Electrical Engineer / AHJ). **[A-001]** The applicable CEC edition must be identified prior to IFC design finalization. ASSUMPTION: CEC Part I (as adopted in Alberta under the Safety Codes Act) is the applicable electrical standard. All installations shall pass required Safety Code inspections.

**Source:** RFP §3.3.2, §3.4; RFP §3.4 ("adhere to all Alberta Safety Codes"); Decomposition SOW-0008, SOW-0009

### REQ-015-04-008 — IFC Design Compliance
All installations shall conform to the IFC electrical drawings and panel schedules (DEL-004-02 through DEL-004-06) signed and stamped by a P.Eng. licensed in the Province of Alberta.

**Source:** RFP §3.3.2 ("All Issued For Construction Drawings must be signed/stamped by a professional engineer licensed to practice in the province of Alberta"); Decomposition SOW-0018

### REQ-015-04-009 — Upstream Dependency
Equipment power circuits shall not be energized until the three-phase power service (DEL-015-01) is complete and energized.

**Source:** _DEPENDENCIES.md (Upstream: DEL-015-01)

### REQ-015-04-010 — Disconnecting Means for Motor Loads
Motor loads (cranes, compressor, pumps, fans) shall be provided with appropriate disconnecting means per CEC requirements. **[A-002]** TBD — confirm whether this requirement is mandatory per specific CEC Part I rule (motor disconnect provisions) or remains an assumption. If mandatory, cite the applicable CEC rule number. Pending confirmation, this requirement is treated as ASSUMPTION: individual motor disconnects are required per CEC Part I.

**Source:** ASSUMPTION based on CEC typical motor circuit requirements; RFP §3.3.2 (code compliance obligation); **location TBD** — CEC Part I motor disconnect rules

### REQ-015-04-011 — Completion Deadline
All equipment power circuits shall be installed, inspected, and commissioned on or before December 31, 2026.

**Source:** RFP §3.1 ("All Work … must be completed on or before December 31, 2026")

### REQ-015-04-012 — Installer Qualifications
**[F-001]** The electrical installer(s) performing this work shall hold appropriate electrical trade certification (e.g., journeyman electrician) and the Electrical Contractor shall be a licensed electrical contractor under the Alberta Safety Codes Act. TBD — confirm specific licensing requirements with AHJ.

**Source:** ASSUMPTION based on Alberta Safety Codes Act contractor licensing requirements; RFP §3.3.2 (code compliance obligation); **location TBD** — Alberta Safety Codes Act contractor licensing provisions

### REQ-015-04-013 — Upstream Energization Verification
**[F-002]** Prior to energization of any equipment power circuit (Procedure Phase 6), a formal go/no-go checkpoint shall confirm that DEL-015-01 (Three-Phase Power Service) is energized and that the distribution panel feeding these circuits is live and stable. This checkpoint shall be documented.

**Source:** _DEPENDENCIES.md (Upstream: DEL-015-01); REQ-015-04-009; Procedure Phase 6, Step 6.1

---

## Standards

| Standard | Applicability | Accessibility |
|---|---|---|
| Alberta Safety Codes Act | Governing legislation for electrical installations in Alberta | Accessible — referenced in RFP §3.3.2 |
| Canadian Electrical Code (CEC) Part I | Primary electrical installation standard (adopted by Alberta). **[C-001]** Applicability is stated as ASSUMPTION — TBD: confirm as binding requirement per Alberta Safety Codes Act / AHJ, or record as explicit TBD pending confirmation. Edition: TBD — use edition as adopted by Alberta at time of permit application (per A-001) | ASSUMPTION: likely applicable; specific edition TBD per IFC design |
| CCDC 14–2013 | Design-Build Stipulated Price Contract governing the Work | Referenced in RFP §2.7 |
| Alberta OH&S Legislation | Occupational Health and Safety requirements for construction | Referenced in RFP §2.15; Decomposition SOW-0083 |
| Crane manufacturer's installation requirements | Governs crane power supply method and electrical requirements | TBD — equipment not yet procured (DEL-016-01) |
| **[C-002]** Alberta Electrical and Communication Utility Code (or other Alberta-adopted amendments/bulletins) | TBD — determine whether Alberta-specific amendments, bulletins, or supplementary codes apply to this work scope beyond CEC Part I and the Safety Codes Act | TBD — confirm with Alberta Municipal Affairs / AHJ; **location TBD** |

**Note:** No electrical codes are independently accessible in the provided source set beyond the RFP's general reference to "Alberta Safety Codes." Specific code editions, Alberta-specific amendments, and clause-level requirements are TBD pending IFC design and AHJ confirmation.

---

## Verification

| Requirement | Verification Approach |
|---|---|
| REQ-015-04-001 (crane power) | Inspect installed circuit(s); verify connection at crane runway; functional test of crane operation. **[E-002]** Crane functional test acceptance criteria: specify measurable pass criteria including full travel range without fault, rated load test per crane manufacturer specifications, and no circuit trip during operation. TBD — confirm acceptance criteria per crane manufacturer / CAN/CSA overhead crane standards |
| REQ-015-04-002 (overhead door power) | Inspect installed circuit(s); verify each overhead door operator powers up and operates |
| REQ-015-04-003 (40A compressor circuit) | Verify circuit breaker rating is 40 A; inspect terminations; test compressor startup |
| REQ-015-04-004 (70A fire hose pump circuit) | Verify circuit breaker rating is 70 A; inspect terminations; test pump operation |
| REQ-015-04-005 (70A pressure washer circuit) | Verify circuit breaker rating is 70 A; inspect terminations; test pressure washer operation |
| REQ-015-04-006 (exhaust fan circuits) | Inspect installed circuit(s) per IFC drawing; test fan operation |
| REQ-015-04-007 (code compliance) | Safety Code inspection and sign-off; inspection reports provided to Owner. **[A-003]** Acceptance criteria: signed inspection certificate from AHJ with zero outstanding deficiencies. Pass artifact = signed inspection report. TBD — confirm specific acceptance criteria per Alberta Safety Codes Act inspection procedures |
| REQ-015-04-008 (IFC compliance) | Verify all work matches IFC drawings and panel schedules |
| REQ-015-04-009 (upstream dependency) | Confirm DEL-015-01 energized prior to equipment circuit energization |
| REQ-015-04-010 (disconnecting means) | Inspect presence and labeling of motor disconnects |
| REQ-015-04-011 (completion deadline) | Milestone tracking against December 31, 2026 |
| REQ-015-04-012 (installer qualifications) | Verify contractor licensing and installer trade certifications prior to work commencement |
| REQ-015-04-013 (upstream energization verification) | Documented go/no-go checkpoint confirming DEL-015-01 is energized before equipment circuit energization |
| **[D-001]** Aggregate conformance | All individual REQ verifications above must be completed and a formal deliverable acceptance sign-off obtained (e.g., "All REQs verified and deliverable accepted by Owner/PM"). TBD — confirm sign-off procedure per CCDC 14 completion provisions / Project Manager |

---

## Documentation

The following artifacts are anticipated for this deliverable:

| Artifact | Description | Status |
|---|---|---|
| IFC Electrical Drawings — Equipment Circuits | As drawn per DEL-004-02 and DEL-004-06; P.Eng.-stamped | TBD (to be produced under PKG-004) |
| Safety Code Inspection Report(s) — Electrical | Signed inspection reports confirming compliance | TBD (to be produced during construction) |
| As-Built Markups | Record of any field deviations from IFC design | TBD |
| Commissioning Records | Functional test records for each equipment circuit | TBD (produced under DEL-020-01) |
| Deficiency Closeout Records | Documentation of deficiency correction during guarantee period | TBD (per RFP §2.10–§2.11) |
