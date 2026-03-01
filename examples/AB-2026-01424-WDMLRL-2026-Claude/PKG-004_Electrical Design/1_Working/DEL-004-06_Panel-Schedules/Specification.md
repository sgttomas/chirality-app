# Specification — DEL-004-06 Panel Schedules

---

## Scope

### What This Deliverable Covers

DEL-004-06 Panel Schedules encompasses the production of complete, signed, and stamped electrical panel schedule document(s) for the New North Shop Addition at the West Dried Meat Lake Regional Landfill, to be submitted as part of the Issued For Construction (IFC) drawing set for PKG-004 (Electrical Design).

**Canonical building name:** "New North Shop Addition" is the canonical name used throughout this document set. (Lensing item X-003.)

The Panel Schedules shall tabulate all electrical panels/distribution boards serving the new addition, enumerating each circuit breaker position with: load description, circuit designation, breaker rating, conductor sizing, voltage, and connected/demand load. The schedules shall be consistent with and traceable to the Single-Line Diagram (DEL-004-02), Power Distribution Plans (DEL-004-03), Lighting Plans (DEL-004-04), Receptacle Layout Plans (DEL-004-05), and the Electrical Calculation Package (DEL-004-08).

Source: RFP §3.3.2, §3.4; Decomposition DEL-004-06 entry; App B (Electrical).

### What This Deliverable Excludes

- Electrical calculation worksheets (covered by DEL-004-08 Electrical Calculation Package)
- Single-line diagram (covered by DEL-004-02)
- Low-voltage system design details beyond identifying circuits (low-voltage plans covered by DEL-004-07)
- Physical installation of panels (covered by PKG-015)
- Panel schedules for the Old North Shop renovation scope, unless explicitly directed by the Electrical Engineer (scope not explicitly stated in sources -- ASSUMPTION: this deliverable covers the New North Shop Addition only). **Scope boundary clarification required: the County should confirm whether panel schedules cover the new addition only or also include any Old North Shop renovation scope. Ambiguity risks over-delivery or under-delivery.** (Lensing item D-001.)

---

## Requirements

### REQ-004-06-01 — Three-Phase Power
The Panel Schedules shall reflect a three-phase power distribution system for the New North Shop Addition. **Note:** The specific service voltage (120/208V, 120/240V, or 347/600V) remains TBD pending utility confirmation. See Guidance Conflict Table CF-004-06-01 for the open conflict requiring human ruling.
Source: RFP §3.4 ("The Proposed building shall run on three-phase power."); Guidance CF-004-06-01.
Verification: Panel schedule header(s) shall declare three-phase supply at the confirmed service voltage; single-line diagram shall confirm.

### REQ-004-06-02 — Complete Load Enumeration
The Panel Schedules shall include a circuit entry for every electrical load identified on the IFC drawings, including but not limited to the loads listed in the Datasheet (Section: Attributes — Known Loads to be Scheduled).
Source: RFP §3.4 and App B (Electrical) — load notes and legend.
Verification: Cross-check panel schedule circuit list against Lighting Plans (DEL-004-04), Receptacle Layout Plans (DEL-004-05), and Power Distribution Plans (DEL-004-03).

### REQ-004-06-03 — Crane Power Circuits
The Panel Schedules shall include dedicated circuit(s) for two (2) 5-tonne overhead cranes on trolley.
Source: App B (Electrical) notes ("Will need power for crane"); RFP §3.4 ("2 – 5-tonne overhead cranes on a trolley.")
Verification: Circuit(s) labeled and sized; confirmed against crane equipment specifications (TBD at design stage).

### REQ-004-06-04 — Overhead Door Power Circuits
The Panel Schedules shall include circuit(s) for overhead door operators.
Source: App B (Electrical) notes ("Will need power for crane and Overhead Doors").
Verification: Circuit(s) labeled and sized; confirmed against door operator specifications (TBD).

### REQ-004-06-05 — Lighting Circuits
The Panel Schedules shall include circuits for:
- 20 high bay LED lights (5 rows × 4 fixtures, 150W each, 22,000 Lumens) in the Main Shop
- 6 high bay LED lights (2 rows × 3 fixtures) in the Wash Bay
- 1 × 8 ft LED in the Office
- 2 × 8 ft LED in the Utility Room
- 6 × 8 ft LED in the Parts/Tool Room
Source: App B (Electrical) notes.
Verification: Circuit count and load totals consistent with Lighting Plans (DEL-004-04).

### REQ-004-06-05A — Ceiling Fan Circuits
The Panel Schedules shall include circuit(s) for six (6) ceiling fans in the Main Shop. Wattage, voltage, and circuit classification (lighting or mechanical) are TBD -- to be determined by the Electrical Engineer based on fan specifications.
Source: App B (Electrical) notes (6 ceiling fans shown); Datasheet Known Loads table.
ASSUMPTION: Ceiling fans are in scope for DEL-004-06. Classification under lighting or mechanical circuits to be confirmed by Electrical Engineer.
Verification: Six ceiling fan units accounted for in panel schedule circuit entries; load data confirmed against equipment specifications.

### REQ-004-06-05B — Service Pit Lighting and Ventilation Circuits
The Panel Schedules shall include circuit(s) for service pit lighting and service pit ventilation. The RFP requires a "ventilated and lighted service pit area for mechanics to perform servicing under equipment." Wattage and circuit count are TBD.
Source: RFP §3.4; App B (Electrical) drawing ("L" symbols near service trench area); Guidance C5.
ASSUMPTION: Service pit lighting and ventilation circuits are in scope for DEL-004-06. Electrical Engineer to confirm.
Verification: Service pit lighting and ventilation circuits present in panel schedule; consistent with Lighting Plans (DEL-004-04) and Mechanical Design (PKG-003).

### REQ-004-06-06 — Receptacle Circuits
The Panel Schedules shall include circuits for all receptacle types shown on the conceptual electrical drawing:
- 15A 120V receptacles (general purpose)
- 20A 120V receptacles
- 20A 240V receptacles
- 30A 240V receptacles
- 50A 240V receptacles (welding and heavy equipment)
Source: App B (Electrical) legend and drawing.
Verification: Circuit count and locations consistent with Receptacle Layout Plans (DEL-004-05).

### REQ-004-06-07 — Equipment Power Circuits (Named Loads)
The Panel Schedules shall include dedicated circuits for the following named equipment loads:
- 40A — Compressor
- 70A — Fire Hose Pump
- 70A — Pressure Washer
Source: App B (Electrical) notes.
Verification: Circuit breaker ratings and conductor sizing per CEC Part I requirements for motor and equipment loads; consistent with Electrical Calculation Package (DEL-004-08).

### REQ-004-06-08 — Exhaust Fan Circuits
The Panel Schedules shall include circuit(s) for exhaust fan(s) as shown in the Appendix B (Electrical) layout.
Source: App B (Electrical) legend (E symbol) and notes (welding station exhaust system referenced).
Verification: Consistent with Mechanical Design (PKG-003) exhaust system scope and Power Distribution Plans (DEL-004-03).

### REQ-004-06-09 — Low-Voltage System Provisions
The Panel Schedules or associated documentation shall identify provisions for low-voltage systems including security camera wiring and 2-way radio antenna wiring. ASSUMPTION: low-voltage systems may be on a separate low-voltage panel or distribution board; treatment to be determined by the Electrical Engineer.
Source: App B (Electrical) notes ("Wiring for Security Cameras"; "Antenna Wire for 2 Way Radios").
Verification: Consistent with Low-Voltage Plans (DEL-004-07).

### REQ-004-06-10 — Alberta Safety Code Compliance
All panel ratings, breaker sizes, conductor sizing, and clearances shown or implied by the Panel Schedules shall comply with the applicable Alberta Safety Codes and the Canadian Electrical Code, Part I (CSA C22.1). ASSUMPTION: CEC Part I is the governing electrical code in Alberta; **the specific edition and any Alberta amendments are TBD -- to be confirmed by the Electrical Engineer** (clause-level requirements not confirmed from accessible sources; location TBD).
Source: RFP §3.3.2 ("The proposed building must adhere to all Alberta Safety Codes.").
Verification: Reviewed and stamped by a P.Eng. licensed to practice in Alberta; clause-level compliance verification to be defined by the Electrical Engineer (see lensing items A-002, A-003).

### REQ-004-06-11 — Professional Engineer Stamp
The Panel Schedules, as part of the IFC drawing set, shall be signed and stamped by a Professional Engineer licensed to practice in the Province of Alberta.
Source: RFP §3.3.2 ("All Issued For Construction Drawings must be signed/stamped by a professional engineer licensed to practice in the province of Alberta.").
Verification: Stamp and signature present on issued documents.

### REQ-004-06-12 — Spare Capacity
The Panel Schedules shall include spare circuit positions. **The minimum spare capacity percentage is TBD -- to be defined as a design decision by the Electrical Engineer, or as a requirement from the County.** ASSUMPTION: Industrial maintenance facilities of this type commonly include 20-25% spare capacity; however, no binding requirement is stated in the RFP or App B. Until a specific target is confirmed, this requirement cannot be enforced. See Guidance Trade-offs for spare capacity analysis and Guidance Considerations for rationale.
Source: ASSUMPTION -- standard design practice; not explicitly stated in RFP or App B. (Lensing item F-001.)
Verification: Spare positions identified and counted in issued schedule; percentage confirmed against the Electrical Engineer's or County's defined target (TBD).

### REQ-004-06-13 — Preliminary Design County Approval
The preliminary electrical design (of which the panel schedule concept is a part) shall be submitted to and approved by the County project team before the final IFC design is issued. **Acceptance criteria for County preliminary approval are TBD: the format of submission, what the County is expected to evaluate, and what constitutes approval (e.g., written sign-off, email confirmation, meeting minutes) must be defined.** See Procedure Step 1.6 for the submission step.
Source: RFP §3.3.2 ("Deliver Preliminary Design for the County project team to approve."). (Lensing item D-003.)
Verification: County approval documented prior to IFC issue; approval record format to be defined by the County project team (TBD).

---

## Standards

| Standard | Applicability | Accessible? |
|---|---|---|
| Alberta Safety Codes (ASCA) | Mandatory — governs all electrical work in Alberta | ASSUMPTION: applicable; not accessible in sources (location TBD) |
| Canadian Electrical Code, Part I (CSA C22.1) | ASSUMPTION: governing electrical code adopted under Alberta Safety Codes | ASSUMPTION: applicable; not accessible in sources (location TBD) |
| CCDC 14–2013 | Contract form — Design-Build Stipulated Price | Referenced in RFP §2.7; not a technical electrical standard |
| CFTA / NWPTA | Procurement framework | RFP §2.21; not a technical design standard |

**Note:** No electrical-specific standards documents are included in the accessible sources. All standards references above are ASSUMPTIONs based on Alberta jurisdiction. The Electrical Engineer shall identify and apply all applicable codes and standards during final design.

---

## Verification

| Requirement | Verification Method |
|---|---|
| REQ-004-06-01 Three-phase power | Cross-check panel header with Single-Line Diagram (DEL-004-02) |
| REQ-004-06-02 Complete load enumeration | Cross-check circuit list against all IFC electrical drawings |
| REQ-004-06-03 Crane power circuits | Confirm circuit count = 2 minimum; verify against crane specs |
| REQ-004-06-04 Overhead door circuits | Confirm presence; verify against door operator specs |
| REQ-004-06-05 Lighting circuits | Cross-check with Lighting Plans (DEL-004-04); verify fixture count |
| REQ-004-06-05A Ceiling fan circuits | Confirm 6 ceiling fan units have circuit entries; load data confirmed against fan specifications |
| REQ-004-06-05B Service pit lighting/ventilation | Confirm service pit lighting and ventilation circuits present; cross-check with Lighting Plans (DEL-004-04) and Mechanical Design (PKG-003) |
| REQ-004-06-06 Receptacle circuits | Cross-check with Receptacle Layout Plans (DEL-004-05) |
| REQ-004-06-07 Equipment power circuits (40A, 70A, 70A) | Verify breaker ratings match load list; confirm with Calculation Package |
| REQ-004-06-08 Exhaust fan circuits | Confirm with Mechanical Design scope; verify on Power Distribution Plans |
| REQ-004-06-09 Low-voltage provisions | Confirm with Low-Voltage Plans (DEL-004-07) |
| REQ-004-06-10 Safety Code compliance | Design review by P.Eng.; Alberta Safety Codes inspection. **Clause-level verification checklist TBD -- Electrical Engineer to define which specific CEC Part I clauses will be verified and the method for each** (lensing item A-003) |
| REQ-004-06-11 P.Eng. stamp | Document check — stamp and signature present |
| REQ-004-06-12 Spare capacity | Count spare positions in issued schedule; verify against defined target percentage (TBD) |
| REQ-004-06-13 Preliminary approval | Document check -- County approval on record before IFC issue; **approval format and acceptance criteria TBD** (lensing item D-003) |

---

## Documentation

### Required Artifacts (from Anticipated Artifacts — _CONTEXT.md)

- Schedule document(s) per RFP — one or more panel schedule sheets, tabular format, forming part of the IFC drawing set for PKG-004.

### Relationship to Other Deliverables

| Deliverable | Relationship |
|---|---|
| DEL-004-02 Single-Line Diagram | Panel schedules must be consistent with the SLD hierarchy |
| DEL-004-03 Power Distribution Plans | Panel locations and feeder routing inform panel schedule scope |
| DEL-004-04 Lighting Plans | Lighting circuit counts feed into panel schedule |
| DEL-004-05 Receptacle Layout Plans | Receptacle circuit counts feed into panel schedule |
| DEL-004-08 Electrical Calculation Package | Load calculations govern panel and breaker ratings |
| DEL-004-09 Electrical Specification | Panel types and ratings referenced in specification |
| PKG-015 Electrical & Low-Voltage Installation | Panel schedules used for procurement and installation |

ASSUMPTION: The inter-deliverable relationships above are based on standard electrical design workflow and decomposition package membership. The decomposition does not explicitly state intra-package sequencing.
