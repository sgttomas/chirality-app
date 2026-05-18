# Guidance — DEL-013-02: High-Volume Air Exchanger

---

## Purpose

DEL-013-02 exists to satisfy the Owner's explicit requirement for a "high volume air exchanger" in the New North Shop addition at the West Dried Meat Lake Regional Landfill (Source: R-01 §3.4 Design Requirements).

The air exchanger serves three interconnected purposes within the facility's mechanical system:

1. **Occupant health and air quality:** The maintenance shop environment generates diesel exhaust, vehicle exhaust, welding fumes, solvents, and particulates. Regular, high-volume air exchange removes these contaminants and supplies fresh outdoor air, maintaining safe and acceptable indoor air quality for workers.

2. **Thermal energy recovery:** Alberta's cold continental climate means that exchanging large volumes of air without heat recovery would impose a significant heating penalty. The heat recovery function of the air exchanger recaptures thermal energy from the outgoing stale air and transfers it to the incoming fresh air, reducing demand on the High-Recovery Heating System (DEL-013-01).

3. **System integration and balance:** The air exchanger is the central balancing element of the facility's ventilation strategy. It works in concert with the Forced-Air Makeup System (DEL-013-03), the Heavy Equipment Exhaust System (DEL-013-04), the Welding Station Exhaust System (DEL-013-05), and the Ceiling Fans (DEL-013-06) to maintain positive or neutral pressure and manage the movement of air through the entire building.

**Objective linkage:**
- OBJ-001: Deliver a code-compliant, fully functional maintenance shop addition (Source: Decomposition §5).
- OBJ-004: Install and commission all mechanical systems to operational readiness, including HVAC/ventilation systems (Source: Decomposition §5: "This includes the HVAC/ventilation systems").

---

## Principles

**P-1: Size for the actual facility volume, not a rule of thumb.**
The New North Shop is an industrial building approximately 13,000 sq ft with 35 ft ceilings (approximately 455,000 cu ft — ASSUMPTION). Industrial occupancies with vehicle exhaust, welding fumes, and heavy equipment require ventilation rates significantly higher than office or residential occupancies. The Mechanical Engineer must size the air exchanger based on a full load analysis per ASHRAE 62.1 or equivalent, not default values. (Source: _DEPENDENCIES.md Constraint Notes; R-01 §3.4; ASSUMPTION re: ASHRAE 62.1 applicability.)

**P-2: Heat recovery is essential for Alberta climate operation.**
Without a heat recovery core, ventilating a ~455,000 cu ft shop at the required air change rate in a −40°C Alberta winter would impose an enormous heating demand. The heat recovery function is not optional in this climate. Cold-climate performance including defrost provisions must be confirmed with the equipment manufacturer. (Source: _CONTEXT.md Description: "recovering thermal energy"; ASSUMPTION re: defrost requirement based on location.)

**P-3: Intake and exhaust placement governs system effectiveness.**
Re-entrainment of exhaust air into the fresh air intake is a common and serious failure mode in industrial ventilation. The intake and exhaust must be separated both horizontally and vertically per mechanical code requirements, and the intake must be positioned upwind of or away from vehicle exhaust entry points, wash bay exhaust, and other contamination sources. (Source: _DEPENDENCIES.md Constraint Notes: "Fresh air intake location must avoid contamination; Exhaust outlet placement critical for air quality.")

**P-4: The air exchanger is a system hub — coordinate before design locks in.**
Five other PKG-013 deliverables (DEL-013-01 through DEL-013-06) share ductwork, controls, and airflow interactions with the air exchanger. Ductwork routing conflicts are much cheaper to resolve on paper than in the field. The Mechanical Engineer's design coordination (PKG-003) must precede Mechanical Contractor procurement and rough-in. (Source: _DEPENDENCIES.md Internal Package Dependencies; Decomposition PKG-013.)

**P-5: Upstream precondition — Utility Room must be complete before installation.**
The air exchanger is to be installed in the Utility Room (DEL-012-02). The room must be structurally complete and weathertight before equipment delivery and installation can proceed. (Source: _DEPENDENCIES.md External Dependencies: "DEL-012-02: Utility Room completion (equipment housing).")

---

## Considerations

### Mechanical Design Dependency
The selection of the specific air exchanger model, airflow rates, ductwork sizing, and controls integration logic depends on the completion and approval of the Mechanical Engineering design package (PKG-003). Until DEL-003-02 (HVAC Layout Plans), DEL-003-03 (Ductwork Plans), DEL-003-05 (Mechanical Equipment Schedule), and DEL-003-07 (Mechanical Specification) are complete, specific equipment cannot be confirmed. Procurement should not proceed ahead of design sign-off without Owner and design-team concurrence.

### Ventilation Design for Industrial Occupancy
ASHRAE 62.1 (Ventilation for Acceptable Indoor Air Quality — ASSUMPTION: likely applicable, location TBD) addresses ventilation requirements by occupancy category. A heavy-equipment maintenance shop may require specific analysis for contaminant classes including diesel exhaust (particulates, NOx), welding fumes (metallic particulates, ozone, UV-generated gases), and solvents. The Mechanical Engineer should confirm applicable ventilation rate standards and whether dedicated source-capture exhaust (DEL-013-04, DEL-013-05) reduces the general ventilation demand on the air exchanger.

### Cold-Climate HRV/ERV Performance
In Alberta winter conditions, the heat recovery core of the air exchanger is subject to freezing if moisture from exhaust air condenses on the core surfaces at temperatures below 0°C. Most industrial HRV/ERV units require a defrost cycle or preheating of incoming air. The equipment specification should require:
- Cold-climate rating (typically tested to −25°C or lower for Alberta applications — ASSUMPTION).
- Defrost method (recirculation, electric preheat, or glycol preheat coil).
- Freeze protection controls.

(Source: ASSUMPTION — based on project location and Alberta climate; manufacturer specifications TBD.)

### Structural Support and Vibration
Large commercial/industrial HRV/ERV units can be heavy (hundreds to thousands of pounds depending on capacity). Structural verification may be needed if the unit is floor-mounted in the Utility Room on an upper level, or if the Utility Room floor slab was not designed for concentrated equipment loads. Vibration isolation is typically required for large rotating equipment to prevent vibration transmission to the building structure, which can cause noise, structural fatigue, and occupant discomfort. (Lensing item F-002)
- **When structural engineer involvement is triggered:** If the unit weight exceeds the Utility Room floor design live load at the mounting footprint, or if the unit is to be roof-mounted or suspended, structural coordination is required.
- **Vibration isolation:** The Mechanical Engineer should specify whether vibration isolation (spring mounts, rubber pads, or inertia base) is required based on equipment type and manufacturer recommendations.
TBD — Mechanical Engineer to confirm unit weight and structural coordination need in design (DEL-003-07); Specification REQ-016 captures the vibration isolation requirement. (Source: ASSUMPTION — structural and vibration considerations are standard for industrial HVAC equipment; specific requirements TBD pending equipment selection.)

### Coordination with Exhaust Systems
The Heavy Equipment Exhaust System (DEL-013-04) and Welding Station Exhaust System (DEL-013-05) provide source-capture ventilation at specific points. These systems discharge air from the building and create a negative pressure tendency in the zones they serve. The air exchanger's supply air distribution must account for these local exhaust loads to prevent cross-contamination, drafts, or combustion appliance backdrafting. Coordination between the Mechanical Engineer, Mechanical Contractor, and the design for DEL-013-03 (Makeup Air) and DEL-013-04/05 is essential. (Source: _DEPENDENCIES.md Exhaust stream coordination.)

### Electrical Interface
The air exchanger requires a power supply. The building runs on three-phase power (R-01 §3.4). The electrical scope boundary between PKG-013 (Mechanical) and PKG-015 (Electrical Installation) must be clearly defined — typically the Electrical Contractor provides the circuit to a disconnect, and the Mechanical Contractor connects the unit. This boundary is TBD and should be confirmed during design coordination. (ASSUMPTION: standard trade scope split; confirmation required.)

### Condensate Drain Management
HRV/ERV units produce condensate from the heat recovery core, particularly during the heating season when warm, moist exhaust air condenses on the cold incoming-air side of the core. In Alberta's cold climate, condensate production can be significant. The installation must address: (Lensing item X-001)
- Condensate drain routing from the unit to an appropriate drain or disposal point.
- Freeze protection for the condensate drain line, especially if routed through unheated spaces.
- Condensate trap (if required by manufacturer).
- Confirmation that the Utility Room has an adequate floor drain or alternative condensate disposal path.

TBD — Mechanical Engineer to address condensate drain provisions in the equipment specification (DEL-003-07). (Source: ASSUMPTION — condensate management is a standard requirement for HRV/ERV installations in cold climates; specific provisions TBD pending equipment selection.)

### Permitting and Inspections
The installation requires a mechanical permit under the Alberta Safety Codes Act. The Owner (County project representative) must be present at all inspections and shall receive copies of all completed inspection reports. (Source: R-01 §3.3.2.)

### Design Coordination Sequencing
The Mechanical Engineer's design outputs (PKG-003: DEL-003-02 through DEL-003-07) must be finalized before PKG-013 procurement can proceed. Given the December 31, 2026, completion deadline (R-01 §3.1), delays in design finalization directly compress the procurement-to-commissioning timeline. (Lensing item D-001)
- **Milestone dependency:** A design-to-procurement handoff milestone should be established in the project schedule, identifying the latest date by which approved IFC drawings and equipment schedules must be available to allow procurement, delivery, installation, and commissioning within the remaining schedule.
- **Escalation path:** If design completion falls behind the established milestone, the Design-Builder should escalate to the Owner with options (e.g., phased procurement, pre-purchase of long-lead equipment with risk acceptance, schedule extension).
TBD — Project Manager to establish design-to-procurement milestone in the project schedule. (Source: _DEPENDENCIES.md; Guidance Principle P-4; R-01 §3.1 completion deadline.)

### Energy Performance and Sustainability
The Owner's objectives (OBJ-001: code-compliant functional facility; OBJ-004: mechanical systems to operational readiness) establish a baseline for code-minimum energy performance. However, heat recovery efficiency directly affects long-term operating costs, energy consumption, and the facility's environmental footprint. (Lensing item E-004)
- The Mechanical Engineer and Owner should consider whether the project values energy performance **beyond** code minimums — e.g., selecting a higher-efficiency HRV/ERV unit that exceeds ASHRAE 90.1 or NRCan minimum requirements.
- A higher initial capital cost for a more efficient unit may be justified by reduced heating demand over the facility's lifecycle, particularly given the high ventilation volumes required in a ~455,000 cu ft industrial shop in an Alberta cold climate.
TBD — Design-Builder/Owner to confirm whether energy performance beyond code minimum is a project value. (Source: ASSUMPTION — OBJ-001 and OBJ-004 do not explicitly require exceeding code minimums; this is a value judgment for the Owner.)

---

### Terminology: HRV vs. ERV vs. HRV/ERV
Across the production documents, the equipment is referred to variously as "HRV," "ERV," "HRV / ERV," "heat recovery ventilator / energy recovery ventilator," and "heat recovery ventilation." The canonical term pending Mechanical Engineer determination is **"HRV/ERV"** (with forward slash, no spaces around slash) to indicate that the final selection between HRV and ERV is TBD. All documents should use "HRV/ERV" consistently when referring to the equipment generically, and reserve "HRV" or "ERV" only when specifically discussing the distinction between the two types (e.g., in the Trade-offs section below). (Lensing item B-004)

_CONTEXT.md uses "heat recovery ventilation" which suggests HRV, but the RFP §3.4 says "high volume air exchanger" without specifying type. The Conflict Table entry C-001 below captures this ambiguity for human ruling.

---

## Trade-offs

| Trade-off | Option A | Option B | Preferred Approach | Rationale |
|---|---|---|---|---|
| HRV vs. ERV | Heat Recovery Ventilator (HRV) — recovers sensible heat only | Energy Recovery Ventilator (ERV) — recovers both sensible heat and moisture | ASSUMPTION: HRV likely preferred for industrial shop (lower moisture carryover, simpler maintenance) | Shop generates vehicle/equipment exhaust with combustion moisture; excessive moisture transfer can cause frost and corrosion issues. Final selection by Mechanical Engineer. |
| Single unit vs. distributed units | One large central HRV/ERV | Multiple smaller distributed units | TBD — Mechanical Engineer to determine | Depends on ductwork routing feasibility through 35 ft ceiling space. Central unit simplifies maintenance; distributed units offer redundancy. |
| Dedicated fresh air ductwork vs. integration with makeup air | Separate fresh air distribution duct system | Shared ductwork with DEL-013-03 Makeup Air | TBD — Mechanical Engineer to determine | May overlap with makeup air system; coordination required to avoid over-pressurization or under-delivery to specific zones. |
| Defrost method | Electric preheat coil on intake | Recirculation defrost cycle | TBD — per manufacturer recommendation and energy analysis | Electric preheat adds operating cost; recirculation temporarily reduces fresh air supply. Both are standard approaches. |

---

## Examples

No confirmed case-study examples from accessible project sources. The following is provided as ASSUMPTION/context only:

**Industrial HRV typical application context (ASSUMPTION):** In Alberta agricultural and industrial facilities of comparable size (10,000–20,000 sq ft with high ceilings), commercial/industrial HRV units in the range of 1,000–5,000 CFM are commonly used, sometimes in multiple units. For a ~455,000 cu ft shop requiring 4–6 air changes per hour (ASSUMPTION — typical for vehicle maintenance per ASHRAE 62.1 guidance), the required airflow would be in the range of approximately 30,000–45,000 CFM total (ASSUMPTION — for illustrative sizing guidance only; Mechanical Engineer must confirm). High-volume industrial HRV units by manufacturers such as dais analytic, Venmar CES, or equivalents are typical for this application in Canada. Equipment selection is TBD pending Mechanical Engineering design.

---

## Conflict Table (for human ruling)

No unresolvable contradictions identified between accessible sources at this stage. The following items are noted as ambiguities for confirmation during design:

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|---|---|---|---|---|---|---|
| C-001 | RFP §3.4 lists "High volume air exchanger" without specifying whether heat recovery (HRV) or energy recovery (ERV) type is required. _CONTEXT.md describes "heat recovery ventilation" suggesting HRV. | R-01 §3.4 (lists equipment type generically) | _CONTEXT.md Description ("heat recovery ventilation") | Specification REQ-002; Datasheet Attributes; Guidance Trade-offs | PROPOSAL: Mechanical Engineer to confirm HRV vs. ERV during design (DEL-003-07); treat as HRV in interim. | TBD |
| C-002 | The electrical scope boundary between PKG-013 (Mechanical Contractor) and PKG-015 (Electrical Contractor) for power supply to the air exchanger unit is not defined in accessible sources. | _DEPENDENCIES.md (no electrical boundary stated) | R-01 §3.4 (three-phase power required for building) | Specification REQ-008; Procedure Steps | PROPOSAL: Design-builder to define scope split in trade coordination matrix during design phase. | TBD |
| C-003 | The specific ventilation rate standard (ASHRAE 62.1 or Alberta mechanical code equivalent) to be applied for airflow sizing is not confirmed in the RFP text — only "high volume" is stated. | R-01 §3.4 ("High volume air exchanger") | _REFERENCES.md ("ASHRAE standards for ventilation systems") | Specification REQ-001, REQ-010 | PROPOSAL: Mechanical Engineer to identify governing standard and minimum ACH/CFM in DEL-003-06 (Calculation Package) and DEL-003-07 (Specification). | TBD |
| C-004 | **(Supplements C-002)** The electrical scope boundary between PKG-013 (Mechanical Contractor) and PKG-015 (Electrical Contractor) for the air exchanger power connection is not defined in any accessible source. This is an essential signal for both contractors and affects both procurement and installation sequencing. (Lensing item B-003) | _DEPENDENCIES.md (no electrical boundary stated) | R-01 §3.4 (three-phase power required); Procedure Step 3.6 | Specification REQ-008; Procedure Step 3.6; Guidance — Electrical Interface | PROPOSAL: Design-Builder to define scope split in trade coordination matrix during design phase. Same resolution path as C-002. | TBD |
| C-005 | Guidance Conflict Table C-001 proposes "treat as HRV in interim" but Specification Scope and Datasheet Attributes both use "HRV / ERV" leaving both options open. The interim assumption in Guidance is not reflected in the other documents. (Lensing item E-003) | Guidance — Conflict Table C-001 ("treat as HRV in interim") | Specification — Scope ("heat recovery ventilator / energy recovery ventilator"); Datasheet — Attributes ("HRV / ERV") | Specification Scope; Datasheet Attributes; Guidance Trade-offs | PROPOSAL: Human ruling needed on whether to adopt "HRV" as interim assumption across all documents or retain "HRV/ERV" pending Mechanical Engineer confirmation. | TBD |
