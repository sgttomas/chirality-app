# Specification — DEL-003-06 Mechanical Calculation Package

---

## Scope

### What This Deliverable Covers

DEL-003-06 is the Mechanical Calculation Package for the West Dried Meat Lake Regional Landfill Maintenance Shop Addition (PKG-003 — Mechanical Design). It provides the engineering calculations that:

1. Size and verify the high-recovery heating system for the ~13,000 sq ft addition.
2. Size and verify the high-volume air exchanger.
3. Size and verify the forced-air makeup air (MUA) system.
4. Size and verify the heavy equipment exhaust systems for the two drive-through repair bays.
5. Size and verify the welding station exhaust/ventilation system.
6. Verify ventilation requirements for the service pit/trench.
7. Confirm ceiling fan selection and layout for the main shop area (6 fans).
8. Demonstrate overall mechanical system energy balance and coordination (supply vs. exhaust vs. makeup).

The calculation package provides the engineering basis of record for:
- DEL-003-02 (HVAC Layout Plans)
- DEL-003-03 (Ductwork & Distribution Plans)
- DEL-003-04 (Exhaust System Plans)
- DEL-003-05 (Mechanical Equipment Schedule)
- DEL-003-07 (Mechanical Specification)

SOW Coverage: SOW-0013 (Complete final mechanical design — HVAC, ventilation, exhaust systems).

### What This Deliverable Does Not Cover

- Plumbing and water system calculations (covered by PKG-006 / DEL-006-07)
- Electrical load calculations (covered by PKG-004 / DEL-004-08)
- Structural calculations for mechanical equipment supports (covered by PKG-002)
- Equipment procurement or installation (covered by PKG-013)
- Commissioning records (covered by PKG-020)
- Mechanical design for the Old North Shop renovation, except where directly mechanically interfacing with the addition (ASSUMPTION: renovation scope is limited to architectural/plumbing renovations per RFP S3.4 and App B; mechanical tie-ins TBD)

---

## Requirements

### REQ-M-001 — Heating Load Calculation
The calculation package shall include a complete heat loss calculation for the addition, covering all building zones. Calculation shall include:
- Envelope U-values for walls, roof, slab, doors, and windows
- Design outdoor conditions (Alberta, Camrose County region — **specific design heating temperature: TBD; shall be confirmed from NBCC climate data tables for the nearest weather station to Ferintosh, AB before calculations are finalized.** ASSUMPTION: approximately -35C or colder per NBCC/Alberta practice)
- Internal heat gains (occupancy, lighting, equipment — TBD)
- Infiltration allowances appropriate for an industrial occupancy with large overhead doors

> **[Enrichment A-001]:** The design outdoor heating temperature requires commitment to a specific NBCC value rather than deferral to "approximately -35C." Multiple documents reference this approximate value as assumption, but equipment sizing changes materially with the exact figure. Source: Specification.md REQ-M-001; Datasheet.md Conditions. PROPOSAL: Mechanical Engineer to confirm from NBCC climate data tables for nearest station to Ferintosh, AB.

**Source:** R-01 S3.4 (design requirements — high-recovery heating system); ASSUMPTION (ASHRAE/NBCC methodology)

### REQ-M-002 — Heating System Sizing
The high-recovery heating system shall be sized to maintain code-required and operationally appropriate temperatures throughout the main shop area, repair bays, wash bay, parts room, utility room, and office. **Indoor design temperature setpoints shall be confirmed per Alberta Building Code occupancy requirements for each zone type. Setpoints are critical to equipment capacity selection.** Minimum setpoints TBD (ASSUMPTION: Alberta practice for industrial occupancies — approximately +10C in shop areas during occupied periods; office areas per occupancy requirements). **Note: the choice between +5C, +10C, and +15C materially changes equipment sizing.**

> **[Enrichment C-001]:** Indoor design temperature setpoints are stated as approximate assumptions. Implementation decisions (equipment capacity) change materially depending on the specific setpoint. Source: Specification.md REQ-M-002. PROPOSAL: Mechanical Engineer to confirm per Alberta Building Code occupancy requirements.

**Source:** R-01 S3.4; SOW-0035; ASSUMPTION

### REQ-M-003 — Air Exchange / Ventilation Rate Calculation
The calculation package shall establish required air change rates (ACH) for each zone:
- Main shop and repair bays (combustion exhaust/vehicle exhaust environment)
- Wash bay
- Service pit/trench (REQ-M-007)
- Parts room, utility room, office (comfort ventilation)

Minimum ventilation rates shall comply with applicable Alberta codes and ASHRAE 62.1 (ASSUMPTION: applicable).

> **[Enrichment A-002]:** All code clause references in the Standards table are listed as "location TBD -- text not accessible." Specific Alberta Building Code and ASHRAE 62.1 clause references shall be added to each requirement where code compliance is claimed, once code texts are obtained. Source: Specification.md Standards; Specification.md REQ-M-010. PROPOSAL: Mechanical Engineer to populate specific code clause numbers once code texts are obtained.

**Source:** R-01 S3.4; SOW-0036; SOW-0028; ASSUMPTION

### REQ-M-004 — Makeup Air Unit (MUA) Sizing
The forced-air makeup air unit shall be sized to:
- Replace air exhausted by the heavy equipment exhaust fans, welding exhaust fan, and general exhaust
- Maintain positive or neutral building pressure balance (ASSUMPTION: neutral balance preferred for industrial shop operations)
- Temper supply air to prevent cold drafts at occupied zones

Minimum MUA capacity shall be calculated from the total exhaust flow determined in REQ-M-005 and REQ-M-006.

**Source:** R-04 App B (Forced Air Makeup listed as design feature); SOW-0037; ASSUMPTION

### REQ-M-005 — Heavy Equipment Exhaust System Sizing
Exhaust hoses and fans shall be sized for the two drive-through repair bays. Calculations shall include:
- Number of exhaust drops/connections per bay (TBD — not specified in accessible sources; **this is an indispensable input: if each bay has 2 drops rather than 1, exhaust flow doubles, affecting MUA sizing and system balance**)
- Required capture velocity at tailpipe connection
- Fan static pressure and flow rate
- Duct/hose sizing and routing

> **[Enrichment F-003]:** Exhaust drops per bay directly affects total exhaust flow and consequently MUA sizing (REQ-M-004) and system balance (REQ-M-009). Source: Datasheet.md Mechanical Systems Inventory; Specification.md REQ-M-005; Procedure.md Step 5. PROPOSAL: Design decision by Mechanical Engineer or RFI to Owner for operational requirements.

**Source:** R-01 S3.4; SOW-0038; ASSUMPTION (ACGIH Industrial Ventilation Manual methodology — location TBD)

### REQ-M-006 — Welding Station Exhaust/Ventilation Sizing
The welding station exhaust system shall be sized to:
- Achieve required capture velocity at the welding station hood (TBD — welding equipment specifications to be supplied by County per SOW-0204)
- Comply with applicable industrial ventilation standards for welding fume control

Note: County to supply welding equipment specifications (R-01 S3.4; SOW-0204). Calculation shall be finalized once specifications are received; interim sizing shall be based on ASSUMPTION of typical MIG/wire-feed welding operations for heavy equipment maintenance. **RFI timeline for County welding specs: TBD — no expected receipt date or escalation path is currently recorded.**

> **[Enrichment B-003]:** Multiple documents note this dependency (Guidance P-03, Procedure Step 6, Specification REQ-M-006) but no document records the expected receipt date or escalation path for County welding specs. Source: Specification.md REQ-M-006; Guidance.md P-03; Procedure.md Step 6. PROPOSAL: Project Manager to issue RFI and track response timeline.

**Source:** R-01 S3.4; R-04 App B (Welding Station Exhaust System); SOW-0039; ASSUMPTION

### REQ-M-007 — Service Pit Ventilation
The service pit/trench shall include a ventilation calculation demonstrating:
- Adequate air changes to dilute and remove combustion/exhaust gases
- Compliance with applicable confined-space or below-grade ventilation requirements (ASSUMPTION: Alberta OH&S and Alberta Building Code apply)

**Source:** R-01 S3.4; SOW-0028; ASSUMPTION

### REQ-M-008 — Ceiling Fan Selection
Six (6) ceiling fans shall be selected for the main shop area. Calculations or selection rationale shall include:
- Fan diameter and coverage area
- Airflow capacity (CFM or L/s)
- Compatibility with 35 ft ceiling height (destratification effectiveness)
- Power supply compatibility (three-phase power available per SOW-0051; fan voltage/phase TBD)

**Source:** SOW-0040; R-04 App B (ceiling fans noted); ASSUMPTION (fan selection criteria)

### REQ-M-009 — System Balance Summary
The calculation package shall include a system balance summary demonstrating:
- Total exhaust flow vs. total makeup/supply flow
- Net pressure effect on building
- Identification of any imbalance exceeding the **quantitative acceptance threshold (TBD — shall be a specific numeric value, e.g., net balance within +/-10% of total supply flow, to be confirmed by Mechanical Engineer and cited to applicable standard or engineering basis)**

> **[Enrichment A-003]:** The previous text stated "ASSUMPTION: +/-10% or per applicable standard" but the Verification table entry only required "acceptable net pressure" without a binding numeric threshold. Compliance determination requires a specific acceptance value. Source: Specification.md REQ-M-009; Specification.md Verification. PROPOSAL: Mechanical Engineer to set acceptance threshold and cite basis.

**Source:** ASSUMPTION (engineering best practice; no specific RFP clause)

### REQ-M-010 — Code Compliance
All calculations shall demonstrate compliance with:
- Alberta Building Code (current edition — ASSUMPTION: applicable)
- Alberta Safety Codes Act (ASSUMPTION: applicable)
- Applicable ASHRAE standards (ASSUMPTION: 62.1 for ventilation; **90.1 for energy: applicability TBD — shall be resolved to yes/no; if applicable, affects equipment efficiency requirements and may require additional calculations**)

Specific clause references shall be provided in the calculation package where compliance is claimed.

> **[Enrichment F-001]:** ASHRAE 90.1 applicability is stated as "may be applicable," which is too vague for a normative requirement. If ASHRAE 90.1 applies, it affects equipment efficiency requirements. Source: Specification.md REQ-M-010; Specification.md Standards. PROPOSAL: Mechanical Engineer to determine applicability from Alberta Building Code energy provisions.

**Source:** R-01 S3.3.2 (all applicable building codes and regulations); SOW-0008; SOW-0009; ASSUMPTION

### REQ-M-011 — IFC-Quality Engineering Basis
The calculation package shall constitute an IFC-quality engineering basis of record:
- Calculations shall be organized, indexed, and signed/stamped by a P.Eng. licensed to practice in Alberta
- All input assumptions shall be clearly stated
- All calculation methods shall reference applicable standards or be derived from first principles with justification
- **P.Eng. stamp scope: TBD — clarify whether the stamp requirement covers the entire calculation package or only the FINAL IFC version. If the PRELIMINARY version circulates without a stamp, confirm whether this satisfies interim compliance needs.**

> **[Enrichment D-001]:** Procedure Step 11.4 implies stamping occurs only at the final IFC stage. If the PRELIMINARY version circulates without a stamp, it may not satisfy interim compliance needs. Source: Specification.md REQ-M-011; Procedure.md Step 11. PROPOSAL: Clarify in Specification that stamp applies to FINAL IFC only, or state requirements for interim versions.

**Source:** R-01 S3.3.2; SOW-0018

### REQ-M-012 — Wash Bay Ventilation and Moisture Control
The calculation package shall include a dedicated ventilation and moisture control calculation for the enclosed wash bay zone, addressing:
- Required air change rate for moisture removal during vehicle washing operations
- Coordination with wash bay drainage (SOW-0027a, SOW-0027b) to determine moisture load
- Whether dedicated exhaust is required or whether the high-volume air exchanger provides adequate moisture control
- Compliance with applicable ventilation codes for the wash bay occupancy type

> **[Enrichment C-002]:** Guidance C-04 identifies wash bay humidity as a distinct zone requiring ventilation design, but no dedicated requirement existed. REQ-M-003 mentioned wash bay only as a line item in the ACH list without addressing moisture-specific requirements. Source: Specification.md REQ-M-003; Guidance.md C-04. PROPOSAL: Added as REQ-M-012 for wash bay ventilation/moisture control.

**Source:** R-01 S3.4; R-04 App B; SOW-0027a, SOW-0027b; Guidance.md C-04; ASSUMPTION (code applicability)

### REQ-M-013 — Combustion Air Supply Calculation (Conditional)
If gas-fired heating equipment is selected (ASSUMPTION per Guidance C-05: gas-fired is the expected fuel type), the calculation package shall include a combustion air supply calculation demonstrating:
- Combustion air requirements for all gas-fired equipment (unit heaters, MUA heating coil, or other)
- Compliance with Alberta Building Code provisions for combustion air supply
- Confirmation that combustion air supply does not create negative pressure conditions conflicting with system balance (REQ-M-009)

> **[Enrichment X-002]:** Guidance C-05 establishes the gas-fired assumption and Datasheet Conditions notes natural gas as the expected fuel source, but no requirement addressed combustion air calculation. Combustion air supply sizing is a code requirement for gas-fired equipment. Source: Specification.md Requirements (scanned -- no existing combustion air requirement); Guidance.md C-05. PROPOSAL: Added as REQ-M-013, conditional on gas-fired equipment selection.

**Source:** Guidance.md C-05; SOW-0080; Alberta Building Code (ASSUMPTION: applicable; location TBD)

---

## Standards

| Standard | Applicability | Accessibility Status |
|---|---|---|
| Alberta Building Code (current edition) | Building ventilation, HVAC requirements, and combustion air supply | ASSUMPTION: applicable; location TBD — text not accessible. **Specific clause references required per REQ-M-010 [Enrichment A-002]** |
| Alberta Safety Codes Act | All safety code requirements | ASSUMPTION: applicable; location TBD — text not accessible |
| National Building Code of Canada (NBCC) | Climate data, design conditions | ASSUMPTION: applicable; location TBD — text not accessible |
| ASHRAE Handbook of Fundamentals | Heating load methodology, psychrometrics | ASSUMPTION: applicable; location TBD — text not accessible |
| ASHRAE 62.1 — Ventilation for Acceptable Indoor Air Quality | Minimum ventilation rates | ASSUMPTION: applicable; location TBD — text not accessible |
| ASHRAE 90.1 — Energy Standard | Energy efficiency compliance | **Applicability: TBD — resolve to yes/no [Enrichment F-001]**; location TBD — text not accessible |
| SMACNA HVAC Duct Construction Standards | Ductwork design basis | ASSUMPTION: applicable; location TBD — text not accessible |
| AMCA Standards (210, 300) | Fan performance rating and selection | ASSUMPTION: applicable; location TBD — text not accessible |
| ACGIH Industrial Ventilation Manual (current edition) | Industrial exhaust system design (equipment exhaust, welding exhaust) | ASSUMPTION: applicable; location TBD — text not accessible |
| Alberta OH&S Code | Workplace ventilation requirements; confined space (service pit) | ASSUMPTION: applicable; location TBD — text not accessible |

---

## Verification

| Requirement | Verification Approach | Acceptance Criterion |
|---|---|---|
| REQ-M-001 — Heating Load | Peer review of heat loss calculation inputs and outputs against building envelope and climate data | TBD — **quantitative acceptance values to be populated as calculations are completed [Enrichment E-003]** |
| REQ-M-002 — Heating System Sizing | Confirm selected equipment capacity >= calculated peak heating load with safety factor | Equipment capacity >= peak load x (1 + safety factor); **safety factor value: TBD — see Guidance [Enrichment F-002]** |
| REQ-M-003 — Ventilation Rates | Compare calculated ACH against code minimums for each zone type | Each zone ACH >= code minimum (specific code clause values TBD) |
| REQ-M-004 — MUA Sizing | Confirm MUA flow rate >= total exhaust flow; verify tempered capacity against design outdoor conditions | MUA flow >= total exhaust; supply temperature >= TBD minimum |
| REQ-M-005 — Equipment Exhaust | Confirm fan performance point (flow vs. static pressure) meets capture velocity requirement | Fan operating point within rated curve; capture velocity >= TBD (per ACGIH) |
| REQ-M-006 — Welding Exhaust | Confirm capture velocity at hood meets ACGIH or applicable standard (pending County welding specs) | Capture velocity >= TBD (ACGIH minimum; PRELIMINARY until welding specs received) |
| REQ-M-007 — Service Pit Ventilation | Confirm ACH meets confined-space/below-grade requirements | ACH >= Alberta OH&S minimum for below-grade maintenance spaces (TBD) |
| REQ-M-008 — Ceiling Fans | Confirm 6 fans cover main shop area at 35 ft height with adequate destratification | Coverage area and destratification effectiveness confirmed per manufacturer data (TBD) |
| REQ-M-009 — System Balance | Confirm supply/exhaust balance table shows net balance within **quantitative acceptance threshold** | **Net balance within TBD% of total supply flow (PROPOSAL: +/-10%, to be confirmed by Mechanical Engineer) [Enrichment A-003]** |
| REQ-M-010 — Code Compliance | **Code compliance cross-reference matrix mapping each code requirement to the calculation section demonstrating compliance; P.Eng. stamp and code references included** | Code compliance matrix complete with all applicable clauses mapped to calculation sections; **[Enrichment X-003]** |
| REQ-M-011 — IFC Quality | Calculation package organized, indexed, and stamped per REQ-M-011 | Package complete, indexed, P.Eng. stamped (scope per REQ-M-011 clarification) |
| REQ-M-012 — Wash Bay Ventilation | Confirm wash bay ventilation calculation addresses moisture control and code minimums | ACH and moisture removal rate meet applicable code for wash bay zone type (TBD) |
| REQ-M-013 — Combustion Air (Conditional) | Confirm combustion air supply meets code for total gas-fired equipment capacity | Combustion air supply >= code requirement for installed gas-fired capacity (TBD; conditional on gas equipment selection) |

> **[Enrichment E-003]:** Acceptance Criterion column added. Current verification approaches use qualitative language only (e.g., "appropriate safety factor," "acceptable net pressure") without committed numeric values. Quantitative acceptance thresholds shall be populated as calculations are completed. Source: Specification.md Verification. PROPOSAL: Populate numeric acceptance criteria as calculations are completed.

> **[Enrichment X-003]:** REQ-M-010 verification strengthened beyond "P.Eng. stamp and code references included" to require a code compliance cross-reference matrix. Source: Specification.md Verification (REQ-M-010 row). PROPOSAL: Require a code compliance cross-reference matrix as part of Section 10 of the calculation package.

---

## Documentation

The following artifacts shall result from this deliverable (per _CONTEXT.md anticipated artifacts):

| Artifact | Description |
|---|---|
| Calculation Package documents | Organized calculation set covering all subjects listed in Requirements above |
| Sizing and load calculations | Heat loss, ventilation, exhaust, makeup air, and combustion air sizing calculations |
| Performance verification documents | System balance summary; equipment performance point verification |
| Equipment selection summary | Summary linking calculations to specified equipment (feeds DEL-003-05) |
| Assumptions register | Clear listing of all design assumptions made in the absence of confirmed data |
| Index / Table of Contents | Organized document index for the calculation package |
| Code compliance cross-reference matrix | Mapping of each applicable code requirement to the calculation section demonstrating compliance [Enrichment X-003] |
