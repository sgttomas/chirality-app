# Procedure — DEL-004-08 Electrical Calculation Package

---

## Purpose

This procedure describes the steps to produce the Electrical Calculation Package (DEL-004-08) for the West Dried Meat Lake Regional Landfill Maintenance Shop Addition. The package constitutes the professional engineering record that supports all electrical IFC drawings (DEL-004-02 through DEL-004-07) and enables the Safety Code permit application (PKG-009).

The procedure addresses production of the deliverable, not installation or commissioning activities.

---

## Prerequisites

### Required Inputs Before Starting Calculations

| Input | Source | Status |
|---|---|---|
| RFP §3.4 design requirements | AB-2026-01424-WDMLRL RFP.pdf | Available |
| Appendix B (Electrical) conceptual drawing | AB-2026-01424-Appendix B (Electrical).pdf | Available |
| Project decomposition (SOW-0014, OBJ-003, OBJ-005) | WDMLRL_Decomposition_Claude.md | Available |
| Canadian Electrical Code, Part I — current Alberta adopted edition | Not provided in accessible sources; Electrical Engineer to obtain | TBD |
| Alberta Safety Code requirements (Electrical) | Not provided in accessible sources; Electrical Engineer to obtain | TBD |
| Crane manufacturer electrical data (motor FLA, voltage, phases) | Not provided in RFP; to be obtained via PKG-016 coordination | TBD |
| County welding equipment specifications | County responsibility per RFP §3.4; to be received from Owner | TBD |
| Mechanical equipment electrical data — heating system | To be obtained from PKG-003 (Mechanical Design); ASSUMPTION: heating system has electrical load requiring dedicated circuit (Lensing C-003) | TBD |
| Mechanical equipment electrical data — forced-air makeup air unit (MUA) | To be obtained from PKG-003 (Mechanical Design); ASSUMPTION: MUA has electrical load requiring dedicated circuit (Lensing C-003) | TBD |
| Mechanical equipment electrical data — exhaust fans (count, motor FLA, voltage) | To be obtained from PKG-003 (Mechanical Design) (Lensing B-003) | TBD |
| Mechanical equipment electrical data — ceiling fans | To be obtained from PKG-003 (Mechanical Design) | TBD |
| Overhead door operator electrical data (quantity, ampacity per unit) | To be coordinated with architectural/structural (DEL-001-07) (Lensing B-002) | TBD |
| Architectural floor plans (for lighting zone areas, including mezzanine) | DEL-001-02 (Architectural Floor Plans) (Lensing E-001) | TBD — upstream |
| Utility three-phase service voltage confirmation | Utility provider for site at SW 14-44-21-W4; **Responsible:** Electrical Engineer; **Target:** before preliminary calculations begin (Lensing A-005) | TBD |

### Required Downstream Awareness
The following deliverables consume outputs from this calculation package:
- DEL-004-02 (Single-Line Diagram) — service entrance and panel configuration
- DEL-004-03 (Power Distribution Plans) — feeder and branch circuit routing
- DEL-004-04 (Lighting Plans) — lighting layout confirmation
- DEL-004-05 (Receptacle Layout Plans) — circuit groupings
- DEL-004-06 (Panel Schedules) — load schedule directly populates panel schedules
- DEL-004-09 (Electrical Specification) — product specifications reference calculation outputs
- PKG-009 (Permitting) — Safety Code permit application requires calculation package

### Responsible Party
Electrical Engineer (P.Eng. licensed in Alberta required for stamp)

---

## Steps

### Step 1: Collect and Confirm Design Inputs

1.1 Obtain all applicable source documents (RFP, Appendix B Electrical, decomposition). Confirm the conceptual layout in App B (Electrical) is the current governing concept.

1.2 Obtain the applicable edition of the Canadian Electrical Code, Part I, as adopted by Alberta (Safety Codes Council). Record the edition in the calculation cover sheet.

1.3 Request County welding equipment specifications (per RFP §3.4). Document in calculation package if not received by the time preliminary calculations are prepared; flag as a design assumption to be resolved before IFC.

1.4 Coordinate with the Mechanical Engineer (PKG-003) to obtain electrical load data for: heating system, forced-air makeup air unit (MUA), exhaust fans, and ceiling fans. For each mechanical load, obtain: motor FLA, voltage, phases, and duty cycle (or equivalent electrical data). Record all received data with source reference. **Note (Lensing C-003):** The heating system and MUA are listed as connected loads in Step 3.1 and are now captured in Specification REQ-004-08-22. The Electrical Engineer should confirm with the Mechanical Engineer which specific mechanical equipment has electrical loads requiring dedicated circuits versus those powered through mechanical package controls.

1.5 Coordinate with crane procurement/specification (PKG-016 or Structural, PKG-002) to obtain crane manufacturer electrical data (motor FLA, voltage, phases, duty cycle). Document if not received; flag as prerequisite for finalizing crane circuit calculations.

1.6 Obtain architectural floor plan areas per zone (from DEL-001-02 when available, or use conceptual building dimensions: 130' × 100' per App B). Use conceptual dimensions for preliminary calculations and update when confirmed architectural plans are available.

1.7 Compile an Input Log recording all data sources, data received, and open data items. This log becomes part of the calculation package. **Clarification (Lensing X-004):** The Input Log (Step 1.7) and the Assumptions and Open Items Register (Step 8.4) are related but distinct sections of the calculation package. The Input Log records what data was received, from whom, and when. The Assumptions and Open Items Register records what assumptions were made in lieu of confirmed data and what items remain open for resolution. Both should cross-reference each other (e.g., an open item in the Input Log should have a corresponding entry in the Assumptions Register).

### Step 2: Establish Design Criteria

2.1 Record the following design criteria in the calculation cover sheet:
- Project name, location, and owner
- Applicable code edition (CEC Part I, edition TBD)
- Power supply: three-phase (voltage and frequency TBD — ASSUMPTION: 120/208 V or 347/600 V three-phase typical for Alberta industrial; Electrical Engineer to confirm service voltage with utility)
- Demand factors applied (per CEC)
- Voltage drop limits (per CEC)
- Design assumptions (welding ampacity, wash bay fixture wattage, overhead door operator size, etc.)

2.2 Confirm with the utility provider the available three-phase service voltage at the site (SW 14-44-21-W4). This affects all voltage calculations.

**ASSUMPTION: Site is in a rural Alberta location; three-phase service voltage confirmation is required early in the design process as it affects the entire electrical system design.**

### Step 3: Prepare Connected Load Schedule

3.1 Tabulate all electrical loads in a connected load schedule, organized by panel/circuit group. Include:
- All lighting circuits (main shop: 20 × 150 W = 3,000 W connected; wash bay: 6 × TBD W; office: 1 × 80 W = 80 W connected (ASSUMPTION — conservative planning value per Lensing X-001); utility room: 2 × 80 W = 160 W connected (ASSUMPTION); parts/tool room: 6 × 80 W = 480 W connected (ASSUMPTION); service pit: TBD)
- All receptacle circuits by type and quantity (15 A/120 V, 20 A/120 V, 20 A/240 V, 30 A/240 V, 50 A/240 V — quantities per App B Electrical drawing)
- Equipment circuits: compressor (40 A), fire hose pump (70 A), pressure washer (70 A)
- Crane feeds (×2): FLA per manufacturer data (TBD)
- Ceiling fans (6 × TBD W)
- Exhaust fans (TBD)
- Overhead doors (TBD per operator data)
- Forced-air makeup air unit (per mechanical data — TBD)
- Heating system (per mechanical data — TBD)
- Mezzanine electrical loads — lighting and receptacle circuits for mezzanine area above parts room, utility room, and wash bay (TBD — coordinate with architectural floor plans) (Lensing E-001)
- Low-voltage power supplies (security cameras, radio — TBD)

3.2 Apply CEC demand factors where applicable (lighting, receptacles, welding outlets, motors). Document the demand factor basis for each load category.

3.3 Calculate total connected load (kVA/kW) and total demand load (kVA/kW).

### Step 4: Service Entrance and Main Panel Sizing

4.1 Size the main service entrance based on total demand load calculated in Step 3.3. Apply a minimum growth margin. ASSUMPTION: growth margin to be determined by Electrical Engineer in consultation with Owner; typical practice is 20–25% spare capacity.

4.2 Determine the service entrance conductor size and overcurrent protection rating per CEC.

4.3 Document service entrance calculation with all intermediate values, CEC clause references, and the resulting service rating.

4.3A Determine the available fault current at the service entrance (from utility provider data or calculation). Verify that the main overcurrent protection device and all downstream devices have interrupting ratings adequate for the available fault current per CEC. Document the fault current determination and device verification. (Lensing X-003; supports REQ-004-08-21)

4.4 Determine panel board and/or distribution panel configuration. Number of panels TBD; for a building of this load density, a main distribution panel with sub-panels is likely required. ASSUMPTION: panel arrangement to be confirmed by Electrical Engineer.

### Step 5: Lighting Calculations

5.1 For each zone requiring lighting calculation, record:
- Zone dimensions (floor area, ceiling height, room surfaces)
- Required illuminance level (ASSUMPTION: Electrical Engineer to determine per IES or equivalent standard; specific standard TBD)
- Fixture type and efficacy
- Calculated illuminance (foot-candles or lux)
- Number of fixtures required vs. number proposed

5.2 Main shop: 20 × 150 W LED / 22,000 lm fixtures. Confirm that the proposed layout (5 rows × 4 fixtures) achieves adequate illuminance for heavy equipment maintenance work.

5.3 Wash bay: 6 high bay fixtures (wattage TBD). Confirm illuminance is adequate for wash bay operations. Confirm fixtures are rated for wet/damp locations.

5.4 Office, utility room, parts/tool room, service pit: confirm proposed fixture quantities achieve adequate illuminance for the respective work tasks.

5.5 Service pit: determine appropriate fixture type for below-grade confined space (may require wet-location rated, low-voltage, or explosion-proof fixtures depending on potential for flammable vapors — ASSUMPTION: Electrical Engineer to assess hazardous area classification).

5.6 Record lighting circuit loading per panel.

### Step 6: Branch Circuit and Feeder Sizing

6.1 For each branch circuit type, calculate conductor size and overcurrent protection per CEC:
- 15 A / 120 V circuits: confirm maximum outlets per circuit
- 20 A / 120 V circuits: confirm maximum outlets per circuit
- 20 A / 240 V circuits: sizing per CEC
- 30 A / 240 V circuits: sizing per CEC
- 50 A / 240 V welding circuits: sizing per CEC (welding outlet load factor applies)
- Dedicated equipment circuits (compressor, fire hose pump, pressure washer): size per motor/equipment rating

6.2 For crane circuits: size per CEC Section 40 (Cranes and Hoists) using manufacturer FLA data. ASSUMPTION: CEC Section 40 governs; specific clause TBD by Electrical Engineer.

6.3 Size sub-feeder conductors from main distribution panel to sub-panels.

6.4 Document each circuit with conductor size, conduit size (ASSUMPTION: standard EMT or rigid conduit per CEC), overcurrent protection device, and applicable CEC clause.

### Step 7: Voltage Drop Calculations

7.1 Calculate voltage drop for all main feeders and critical branch circuits. Confirm compliance with CEC voltage drop limits. **Note (Lensing F-002):** Typical Alberta practice uses 3% maximum on feeders and 5% maximum total (branch + feeder). However, the actual limits shall be confirmed from the specific CEC edition adopted by Alberta at the time of design (see Specification Standards table — CEC edition TBD). The Electrical Engineer shall record the actual code-specified limits in the design criteria summary (Step 2.1) once the CEC edition is confirmed, and update both this Procedure and Specification REQ-004-08-15 to reflect the confirmed values. See also Guidance Conflict Table CONF-004-08-05.

7.2 For circuits with long runs (e.g., cranes at far end of building from service entrance), give special attention to voltage drop. Upsize conductors if required.

7.3 Document voltage drop calculations with circuit ID, conductor size, run length, load current, and calculated % voltage drop.

### Step 8: Compile Calculation Package

8.1 Assemble the calculation package with the following sections (minimum):
- Cover sheet: project identification, P.Eng. name and stamp, calculation date, revision table
- Design criteria summary (code edition, supply voltage, demand factors, assumptions, open items)
- Input Log (data sources, received data, open items) (see Step 1.7)
- Connected and demand load schedule, with demand factor basis per load category (REQ-004-08-19)
- Service entrance sizing calculation
- Available fault current determination and overcurrent device interrupting rating verification (REQ-004-08-21; Step 4.3A)
- Panel configuration determination (REQ-004-08-20; Step 4.4)
- Lighting calculations (by zone, including mezzanine) with quantitative illuminance targets (REQ-004-08-23)
- Hazardous area classification assessment for service pit (REQ-004-08-24; Step 5.5)
- Branch circuit sizing calculations (by circuit type), with CEC clause references per circuit
- Feeder sizing calculations, with CEC clause references
- Voltage drop calculations
- Dedicated equipment circuit calculations (cranes, compressor, fire hose pump, pressure washer), with CEC clause references
- Heating/MUA circuit calculations (REQ-004-08-22)
- Crane circuit calculations (when manufacturer data available)

8.2 Cross-reference each calculation section to the corresponding drawing (DEL-004-02 through DEL-004-07) using a structured cross-reference table. **Format (Lensing D-003):** The cross-reference table shall include columns for: Calculation Section, Drawing Number, Drawing Title, Drawing Revision, and Notes. This table should be included as an appendix or summary section of the calculation package. Given that 6 downstream deliverables (DEL-004-02 through DEL-004-07) consume this package, a structured cross-reference mechanism improves traceability and supports the revision linkage process described in Guidance (see "Calculation Package as Living Document").

8.3 Clearly mark all assumptions in the package. Flag all open items requiring resolution before IFC. Cross-reference each assumption to the corresponding Input Log entry (Step 1.7) where applicable. (Lensing X-004)

8.4 Prepare an Assumptions and Open Items Register as an appendix. **Clarification (Lensing X-004):** This register is distinct from the Input Log (Step 1.7). The Input Log tracks data sources and receipt status. The Assumptions and Open Items Register tracks design decisions made in the absence of confirmed data and items requiring resolution before IFC. Each register entry should reference the corresponding Input Log item where applicable, creating a traceable chain from missing data to design assumption to resolution status.

### Step 9: Internal QC Review

9.1 The preparing Electrical Engineer (or a reviewing P.Eng.) shall perform an independent check of:
- Load schedule completeness (all App B loads accounted for)
- Arithmetic and formula correctness
- CEC code compliance for all sizing calculations
- Consistency between calculation outputs and drawing content

9.2 Document the review on the calculation cover sheet (reviewer name, date, signature).

### Step 9A: Assumption Resolution Gate (Lensing A-004)

9A.1 Before proceeding to P.Eng. stamp and IFC release, the Electrical Engineer shall conduct a formal review of all open assumptions and unresolved items in the Assumptions and Open Items Register (Step 8.4).

9A.2 For each open assumption, determine one of the following dispositions:
- **RESOLVED:** Data has been received and the assumption has been replaced with confirmed values. Record the resolution source and date.
- **ACCEPTED AS DESIGN ASSUMPTION:** The assumption is accepted as the basis of design, with documented risk. Record the rationale for acceptance and any risk mitigation.
- **DEFERRED:** The item cannot be resolved before IFC but does not prevent issuance. Record the plan for post-IFC resolution and impact assessment. ASSUMPTION: deferred items should be rare for IFC-stamped work.

9A.3 The assumption resolution gate is complete when all items in the register have a documented disposition. The reviewing P.Eng. shall sign off on the assumption resolution status before proceeding to Step 10.

9A.4 Key assumptions requiring resolution for this deliverable include (at minimum):
- Crane manufacturer electrical data (CONF-004-08-03)
- County welding equipment specifications (CONF-004-08-02)
- Three-phase service voltage confirmation from utility (Lensing A-005)
- Exhaust fan count and motor data from PKG-003 (Lensing B-003)
- CEC edition confirmation (Lensing A-001)

### Step 10: P.Eng. Stamp and IFC Release

10.1 The responsible Electrical Engineer (P.Eng., licensed in Alberta) shall review, sign, and stamp the calculation package as Issued for Construction.

10.2 The stamped calculation package shall be submitted as part of the Safety Code permit application (PKG-009).

10.3 Distribute the package to related deliverable owners (DEL-004-02 through DEL-004-07, DEL-004-09) for coordination.

---

## Verification

| Check | Verification Method | Responsible |
|---|---|---|
| All App B (Electrical) loads included in load schedule | Compare load schedule against App B fixture/circuit counts line by line | Electrical Engineer |
| Mezzanine loads included in load schedule | Confirm mezzanine lighting and receptacle loads are itemized (Lensing E-001) | Electrical Engineer |
| Heating/MUA loads included in load schedule | Confirm heating system and MUA loads are itemized per REQ-004-08-22 (Lensing C-003) | Electrical Engineer |
| Service entrance adequately sized | Calculation output exceeds total demand load with appropriate margin | Electrical Engineer (reviewer) |
| Available fault current documented | Fault current determination present; overcurrent device interrupting ratings verified (Lensing X-003) | Electrical Engineer (reviewer) |
| Demand factor basis documented | Demand factor documented per load category with CEC clause or rationale (Lensing F-001) | Electrical Engineer |
| Panel configuration documented | Number of panels, arrangement, and sizing basis recorded (Lensing X-002) | Electrical Engineer |
| Lighting illuminance adequate | Calculation output meets or exceeds applicable illuminance standard for each zone; quantitative illuminance targets documented (Lensing D-001) | Electrical Engineer |
| Hazardous area classification assessed | Service pit classification assessment documented (Lensing B-004) | Electrical Engineer |
| Branch circuit conductors and protection sized per CEC | CEC clause references recorded for each branch circuit (Lensing C-001, E-003) | Electrical Engineer |
| Feeder conductors and protection sized per CEC | CEC clause references recorded for each feeder (Lensing C-001, E-003) | Electrical Engineer |
| Dedicated equipment circuits sized per CEC | CEC clause references recorded for each dedicated equipment circuit (Lensing C-001, E-003) | Electrical Engineer |
| Voltage drop within limits | Calculated % VD ≤ confirmed CEC limits for all circuits (Lensing F-002) | Electrical Engineer (reviewer) |
| Assumptions flagged | All ASSUMPTION items labeled and tracked in Assumptions and Open Items Register | Electrical Engineer |
| Assumption resolution gate complete | All assumptions have documented disposition (RESOLVED, ACCEPTED, or DEFERRED) before IFC (Lensing A-004) | Electrical Engineer; reviewing P.Eng. |
| Cross-reference table complete | Structured cross-reference table links each calculation section to corresponding drawing (Lensing D-003) | Electrical Engineer |
| Input Log and Assumptions Register cross-referenced | Input Log (Step 1.7) and Assumptions Register (Step 8.4) are consistent and cross-referenced (Lensing X-004) | Electrical Engineer |
| P.Eng. stamp applied | Stamp, signature, and date present on cover sheet and all calculation sheets | P.Eng. |
| Safety Code permit application supported | Calculation package accepted by Safety Codes Officer | PKG-009 / Permitting team |

---

## Records

| Record | Purpose | Retention |
|---|---|---|
| Stamped Electrical Calculation Package (IFC issue) | Primary professional record supporting electrical design and permit | Project record — retain per CCDC 14-2013 and Alberta professional engineering practice requirements |
| Input Log (data sources and open items register) | Documents design basis and flags outstanding issues | Part of calculation package |
| QC Review record (reviewer name, date, sign-off on cover sheet) | Evidence of internal quality review | Part of calculation package |
| Revision history (cover sheet revision table) | Tracks design changes | Part of calculation package |
| Safety Code permit application submission record | Evidence of regulatory compliance initiation | PKG-009 records |
| Correspondence with County re: welding equipment specifications | Documents design assumption basis or confirmed inputs | Project correspondence file |
| Correspondence with crane manufacturer/supplier | Documents crane electrical data source | Project correspondence file |
