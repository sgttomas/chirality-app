# Specification — DEL-004-02 Single-Line Diagram

**Document Type:** Specification (normative)
**Deliverable ID:** DEL-004-02
**Deliverable Name:** Single-Line Diagram
**Package:** PKG-004 Electrical Design
**Project:** 2026 Design Build — West Dried Meat Lake Regional Landfill Maintenance Shop Addition
**Owner:** Camrose County
**Responsible Party:** Electrical Engineer
**Last Updated:** 2026-02-26

---

## Scope

### What This Deliverable Covers

DEL-004-02 is the Single-Line Diagram (SLD) for the New North Shop electrical system. The SLD is a schematic drawing set that depicts the power distribution hierarchy from the building service entrance through all distribution panels, feeders, and branch circuits to the loads identified in the conceptual electrical drawing (App B — Electrical). The SLD serves as the top-level electrical power distribution document and is required as part of the Issued-for-Construction (IFC) electrical drawing package per SOW-0014 and SOW-0018.

The SLD covers the following systems for the New North Shop Addition (approximately 13,000 sq ft):

- Three-phase service entrance and main distribution (SOW-0051)
- Power distribution to all lighting circuits (SOW-0052 through SOW-0056)
- Power distribution to all receptacle circuits — 15A/120V, 20A/120V, 20A/240V, 30A/240V, 50A/240V (SOW-0058)
- Dedicated circuits for welding-grade receptacles at 50A/240V (SOW-0057; D-009)
- Dedicated equipment circuits: two 5-tonne overhead cranes (SOW-0059), all overhead doors (SOW-0060), 40A compressor (SOW-0061), 70A fire hose pump (SOW-0062), 70A pressure washer (SOW-0063)
- Exhaust fan circuit(s) (SOW-0066)
- Low-voltage system notation: security camera wiring (SOW-0064), antenna wire for 2-way radios (SOW-0065)
- Ceiling fans — 6 units in main shop (SOW-0040 / App B — Electrical)

### What This Deliverable Does Not Cover

- Mechanical/HVAC equipment electrical connection *design details* (covered under PKG-003 Mechanical Design; installation under PKG-013). **Note:** The SLD *does* include power provision notation and TBD placeholders for mechanical equipment feeds per REQ-SLD-012, but the detailed connection design (starter type, disconnect location, conduit routing) is covered under PKG-003.
- Plumbing system electrical connections (covered under PKG-006 Plumbing Design)
- Service pit/trench electrical details (covered under DEL-004-03 Power Distribution Plans and DEL-004-05 Receptacle Layout Plans)
- Low-voltage system design (detailed system design, head count, and routing for security cameras and radio antenna covered under DEL-004-07 Low-Voltage System Plans)
- Electrical renovation of Old North Shop — this SLD covers the New North Shop Addition only; Old North Shop renovation electrical scope TBD
- Panel schedules in tabular form (covered under DEL-004-06 Panel Schedules)
- Load calculations (covered under DEL-004-08 Electrical Calculation Package)
- Physical conduit and wire routing (covered under DEL-004-03 Power Distribution Plans)
- Utility service tie-in design details (SOW-0081 — coordinated under PKG-018 Sitework)

---

## Requirements

### REQ-SLD-001 — Service Entry Representation
The SLD shall depict the building electrical service entrance, including service voltage, phase configuration (three-phase per SOW-0051), main disconnect, and metering equipment.
**Source:** RFP §3.4; SOW-0051; App B (Electrical)
**Verification:** Drawing review — service entrance block present and annotated with voltage, phase, and ampacity.

### REQ-SLD-002 — Main Distribution Panel
The SLD shall show the main distribution panel (MDP) or main switchboard, including bus rating (TBD — to be sized by load calculation per DEL-004-08), with feeders to all sub-panels and directly connected equipment.
**Source:** RFP §3.4; SOW-0014
**Verification:** Drawing review — MDP shown with bus rating annotation; all feeders accounted for.

### REQ-SLD-003 — Lighting Circuits
The SLD shall account for all lighting loads listed in the conceptual drawing:
- 5 rows × 4 high bay lights in main shop (20 fixtures, 150W LED, 22,000 lumens each) — SOW-0052
- 2 rows × 3 high bay lights in wash bay (6 fixtures) — SOW-0053
- 1 × 8' LED fixture in office — SOW-0054
- 2 × 8' LED fixtures in utility room — SOW-0055
- 6 × 8' LED fixtures in parts/tool room — SOW-0056

Circuit grouping and sizing shall be determined by the Electrical Engineer based on load calculations.
**Source:** App B (Electrical); SOW-0052 through SOW-0056
**Verification:** Load count verified against App B (Electrical) conceptual drawing; circuit labels present.

### REQ-SLD-004 — Receptacle Circuits
The SLD shall account for all receptacle circuit types identified in the conceptual drawing:
- 15A/120V — general purpose
- 20A/120V — general purpose (heavier duty)
- 20A/240V — single-phase 240V
- 30A/240V — heavy-duty 240V
- 50A/240V — welding-grade (ASSUMPTION: 50A/240V per D-009; to be confirmed)

Circuit grouping and panel assignment shall be determined by the Electrical Engineer.
**Source:** App B (Electrical); SOW-0057, SOW-0058; D-009
**Verification:** All five receptacle circuit types represented in SLD; 50A/240V welding circuits clearly identified.

### REQ-SLD-005 — Dedicated Equipment Circuits
The SLD shall show individually identified dedicated circuits for the following equipment:

| Equipment | Dedicated Circuit Rating | Source |
|---|---|---|
| Overhead Crane #1 (5-tonne) | TBD — per crane manufacturer specification | SOW-0059; App B (Electrical) |
| Overhead Crane #2 (5-tonne) | TBD — per crane manufacturer specification | SOW-0059; App B (Electrical) |
| Overhead Door(s) | TBD — quantity and motor rating per architectural drawing | SOW-0060; App B (Electrical) |
| Compressor | 40A | SOW-0061; App B (Electrical) |
| Fire Hose Pump | 70A | SOW-0062; App B (Electrical) |
| Pressure Washer | 70A | SOW-0063; App B (Electrical) |
| Exhaust Fan(s) | TBD — per equipment selection | SOW-0066; App B (Electrical) |
| Ceiling Fans (×6) | TBD — per equipment selection | SOW-0040; App B (Electrical) |

**Source:** App B (Electrical); SOW-0040, SOW-0059 through SOW-0063, SOW-0066
**Verification:** Each dedicated circuit item listed in table above is individually shown and labeled on SLD.

### REQ-SLD-006 — Low-Voltage System Notation
The SLD shall include notation for low-voltage systems: security camera wiring (SOW-0064) and antenna wire for 2-way radios (SOW-0065). Detailed routing and head count are covered in DEL-004-07; the SLD shall at minimum identify the power supply circuit(s) for these systems where applicable.
**Source:** App B (Electrical); SOW-0064, SOW-0065
**Verification:** Low-voltage system power provisions noted on SLD.

### REQ-SLD-007 — P.Eng. Stamp
The SLD shall be signed and stamped by a Professional Engineer licensed in Alberta prior to use for construction (IFC issue).
**Source:** RFP §3.3.2; SOW-0018
**Verification:** Stamp and signature present on issued drawing.

### REQ-SLD-008 — County Approval Sequence
The Preliminary Electrical Design (DEL-004-01) must receive County approval before the SLD is finalized for IFC issuance. The SLD shall be consistent with the approved preliminary design.
**Source:** RFP §3.3.2; SOW-0010d
**Verification:** Issued SLD references or is consistent with approved preliminary design.

### REQ-SLD-009 — Three-Phase Service
The SLD shall reflect a three-phase power supply to the building, as required by SOW-0051.
**Source:** RFP §3.4; SOW-0051
**Verification:** Service block on SLD explicitly annotated as three-phase.

### REQ-SLD-010 — Cross-Discipline Coordination
The SLD shall be coordinated with:
- DEL-004-03 (Power Distribution Plans) — physical circuit routing must align with SLD hierarchy
- DEL-004-06 (Panel Schedules) — panel schedule circuit numbers shall match SLD
- DEL-004-08 (Electrical Calculation Package) — conductor and breaker sizing shown on SLD shall be supported by load calculations
- DEL-002-07 (Crane Support Structure Details) — crane power requirements inform SLD crane circuit sizing

**Source:** Decomposition §7 PKG-004; SOW-0014, SOW-0018
**Verification:** Cross-reference check between SLD and named deliverables prior to IFC issue. **The check shall be performed by the Electrical Engineer (or delegate) and shall verify consistency with each of the four named deliverables (DEL-004-03, DEL-004-06, DEL-004-08, DEL-002-07). A passing check requires documented confirmation that circuit hierarchy, breaker/conductor sizing, and panel designations are consistent between the SLD and each named deliverable. Any discrepancy shall be resolved and documented before IFC issue.** *(Enriched per X-003: essential adjudication basis requires specificity on who performs, what constitutes pass/fail, and scope of check.)*

### REQ-SLD-011 — CEC Edition Confirmation
The Electrical Engineer shall confirm the specific edition of the Canadian Electrical Code (CEC) currently adopted by the Alberta Safety Codes authority and document this confirmation before proceeding with detailed SLD design.
**Source:** ASSUMPTION: CEC governs electrical design in Alberta (location TBD); Alberta Safety Codes Act (RFP §3.3.2, SOW-0007, SOW-0009). *(Added per A-001, A-003: normative prescriptive direction and compliance determination require explicit code-edition gating.)*
**Verification:** Written record of confirmed CEC edition (letter, email, or online confirmation from Safety Codes authority) on file before SLD design commences.

### REQ-SLD-012 — Mechanical Equipment Electrical Provisions
The SLD shall include power provisions for mechanical equipment requiring electrical connections, including but not limited to: forced-air makeup air unit (SOW-0037), high-recovery heating system (SOW-0035), and mechanical exhaust systems (SOW-0038, SOW-0039). Circuit ratings shall be coordinated with the Mechanical Equipment Schedule (DEL-003-05). Where mechanical equipment electrical data is not yet available, TBD placeholders with equipment descriptions shall be shown.
**Source:** SOW-0035, SOW-0037, SOW-0038, SOW-0039; Decomposition PKG-003; Guidance.md Considerations (Coordination with Mechanical Electrical Loads). *(Added per A-002: mandatory practice gap -- Guidance identified coordination need but no normative requirement existed.)*
**Verification:** Each mechanical equipment item from DEL-003-05 that requires an electrical connection has a corresponding entry (or TBD placeholder) on the SLD.

### REQ-SLD-013 — Arc Flash / Short-Circuit Analysis Reference (TBD)
TBD — The Electrical Engineer shall determine whether an arc flash hazard analysis or short-circuit current rating study is required for this facility per CEC and/or CSA Z462, given the industrial load profile (70A dedicated circuits, crane power, multiple 240V circuits). If required, the SLD shall reference or note the arc flash study and applicable incident energy levels at the MDP and sub-panels.
**Source:** ASSUMPTION: CEC / CSA Z462 may require arc flash labeling for industrial facilities with high available fault current (location TBD). *(Added per C-001: obligatory compliance basis gap for industrial facility.)*
**Verification:** TBD — determination of applicability documented; if applicable, arc flash reference annotations present on SLD.

### REQ-SLD-014 — Grounding and Bonding System Representation
The SLD shall depict the grounding and bonding system, including at minimum: service grounding electrode, main bonding jumper, and equipment grounding conductor paths. The representation shall be consistent with CEC requirements for electrical installations.
**Source:** ASSUMPTION: CEC requires grounding/bonding for all electrical installations; industrial SLD typically shows the grounding system (location TBD in CEC). *(Added per C-002: exhaustive regulatory coverage gap -- no prior requirement addressed grounding/bonding on SLD.)*
**Verification:** Drawing review — grounding/bonding system elements present and annotated on SLD.

### REQ-SLD-015 — Electrical Permit Application Inclusion
The SLD shall be included in the electrical permit application package submitted per Alberta Safety Codes Act requirements (SOW-0007, SOW-0009). The Electrical Engineer shall confirm that the permit application references the SLD drawing number.
**Source:** RFP §3.3.2; SOW-0007, SOW-0009; Alberta Safety Codes Act. *(Added per F-001: enforceable regulatory mandate -- SLD inclusion in permit application was implicit but not explicitly required.)*
**Verification:** Permit application package includes SLD; permit application references SLD drawing number.

---

## Standards

The following standards are anticipated to govern this deliverable. Where the specific document text was not accessible, applicability is noted as ASSUMPTION.

| Standard / Code | Applicability | Accessibility |
|---|---|---|
| Canadian Electrical Code (CEC), CSA C22.1 — latest adopted edition in Alberta | Primary electrical design and installation standard for Alberta | ASSUMPTION: likely applicable; specific edition TBD per Alberta Safety Codes authority (location TBD). **The Electrical Engineer shall confirm the currently adopted CEC edition with the Alberta Safety Codes authority before design proceeds; this confirmation is a gating action for design (see REQ-SLD-011).** |
| Alberta Safety Codes Act and associated Electrical Code adoption | Permitting and inspection authority | RFP §3.3.2, SOW-0007, SOW-0009 |
| Alberta Building Code (ABC) — applicable electrical provisions | Building code compliance | RFP §3.3.2, SOW-0008 |
| CCDC 14–2013 | Contract form governing design-build obligations | RFP §2.7, SOW-0104 |
| APEGA / ASET — P.Eng. stamp requirements | Professional stamp obligations | RFP §3.3.2, SOW-0018 |
| CSA C22.3 / utility interconnection requirements | Service entrance and utility coordination | ASSUMPTION: likely applicable; location TBD |

**Note:** The Electrical Engineer shall confirm the specific edition of each applicable standard at the time of design. Clause-level requirements are not derived here due to inaccessibility of standard texts.

---

## Verification

| Requirement | Verification Method |
|---|---|
| REQ-SLD-001 — Service entry | Drawing review by Electrical Engineer and/or reviewing authority |
| REQ-SLD-002 — MDP/switchboard | Drawing review — bus rating annotated |
| REQ-SLD-003 — Lighting circuits | Load count audit against App B (Electrical) |
| REQ-SLD-004 — Receptacle circuits | Circuit type audit against App B (Electrical) legend and layout |
| REQ-SLD-005 — Dedicated equipment circuits | Item-by-item check against dedicated circuit table |
| REQ-SLD-006 — Low-voltage notation | Review for notation presence |
| REQ-SLD-007 — P.Eng. stamp | Visual confirmation of stamp and signature on IFC drawing |
| REQ-SLD-008 — County approval sequence | Confirm County approval of DEL-004-01 prior to SLD IFC issue |
| REQ-SLD-009 — Three-phase service | Annotation review |
| REQ-SLD-010 — Cross-discipline coordination | Coordinator sign-off or interdisciplinary review record. Check shall verify consistency of circuit hierarchy, breaker/conductor sizing, and panel designations with each named deliverable (DEL-004-03, DEL-004-06, DEL-004-08, DEL-002-07). Discrepancies resolved and documented before IFC. |
| REQ-SLD-011 — CEC edition confirmation | Written record of confirmed CEC edition from Safety Codes authority on file before SLD design commences |
| REQ-SLD-012 — Mechanical equipment electrical provisions | Each mechanical equipment item from DEL-003-05 has a corresponding SLD entry or TBD placeholder |
| REQ-SLD-013 — Arc flash / short-circuit (TBD) | TBD — applicability determination documented; if applicable, arc flash reference annotations on SLD |
| REQ-SLD-014 — Grounding and bonding | Drawing review — grounding/bonding system elements present and annotated |
| REQ-SLD-015 — Permit application inclusion | Permit application package includes SLD and references SLD drawing number |
| Voltage drop verification | Confirm voltage drop calculations for feeder runs (130' x 100' building) are performed per CEC and SLD feeder sizes reflect results. *(Added per F-002: critical functional imperative for large industrial building.)* Source: Procedure Step 3.2; CEC (ASSUMPTION — location TBD) |
| Safety Codes inspection readiness | Confirm SLD package (stamped drawing, revision register, coordination record) is assembled and available for Safety Codes Officer inspection per SOW-0084, SOW-0085. *(Added per X-004: fundamental inspection basis requires explicit readiness gate.)* |

---

## Documentation

The following artifacts are anticipated from this deliverable:

| Artifact | Description |
|---|---|
| Single-Line Diagram drawing(s) | The SLD drawing set, preliminary issue for County approval and final IFC issue with P.Eng. stamp |
| Drawing revision register | Record of revisions from preliminary through IFC |
| Coordination sign-off | Record of cross-discipline coordination check (REQ-SLD-010) before IFC |

**Note:** All artifacts must be retained and provided to the County as part of construction documentation and closeout (SOW-0093).
