# Specification — DEL-013-06: Ceiling Fans

---

## Scope

### Included in this Deliverable

This deliverable covers the supply, installation, and commissioning of **six (6) ceiling fans** in the main shop area (repair bay) of the New North Shop at the West Dried Meat Lake Regional Landfill Maintenance Shop Addition. Scope includes:

- Selection and procurement of ceiling fans meeting the performance and environmental requirements of the facility
- Mounting bracket and structural attachment hardware installation
- Downrod and fan assembly installation
- Coordination with Electrical Contractor for branch circuit terminations at fan junction boxes
- Control switch or control system installation (wall switches or integrated controls)
- Balancing, functional testing, and commissioning
- Documentation: as-built record, commissioning report, and manufacturer O&M manuals

Source: SOW-0040 (R-01, Decomposition §8); _CONTEXT.md Scope section.

### Excluded from this Deliverable

- Branch circuit wiring from panel to fan junction boxes (Electrical Contractor, DEL-015 scope)
- Structural ceiling/purlin/beam modifications or reinforcement (Structural scope, DEL-002 interface)
- HVAC system design and mechanical engineering calculations (PKG-003 design scope)
- Ceiling fans in wash bay, office, parts room, or utility room (not listed in SOW-0040 or App B-Elec)

---

## Requirements

### REQ-013-06-01: Quantity
Six (6) ceiling fans shall be supplied and installed in the main shop area.
- **Source**: SOW-0040 (R-01); App B-Elec (R-05) Electrical Notes.
- **Verification**: Physical count at completion inspection.

### REQ-013-06-02: Installation Location
All fans shall be installed in the main shop area (repair bay) of the New North Shop. Individual fan positions shall be determined during the design phase and shown on Issued for Construction (IFC) drawings.
- **Source**: SOW-0040 ("main shop area"); App B-Elec (R-05).
- **Note**: Individual fan coordinate positions are TBD pending final mechanical/layout design.

### REQ-013-06-03: Air Circulation Function
Fans shall provide supplemental air circulation to reduce thermal stratification, improve temperature uniformity, and enhance occupant comfort throughout the main shop area.
- **Source**: _CONTEXT.md Description and Key Requirements.
- **Verification**: Commissioning functional test. **Acceptance criterion TBD (X-001):** No measurable pass/fail criterion is currently defined. PROPOSAL: Define a measurable criterion such as minimum air velocity (m/s) at 1.5 m height in the occupied zone, or maximum temperature differential (degrees C) between floor level and ceiling level during heating season. Mechanical Engineer to determine appropriate threshold.
- **Note**: Current ASSUMPTION of "perceptible air movement at floor level at all speed settings" is subjective and may be disputed. A numeric threshold is required for objective verification.

### REQ-013-06-04: Code-Compliant Electrical Installation
Fan electrical connections shall comply with the Alberta Electrical Code and all applicable Alberta Safety Codes. All Issued for Construction Drawings shall be signed/stamped by a professional engineer licensed to practice in Alberta.
- **Source**: RFP §3.3.2 (R-01); RFP §3.4 ("The proposed building must adhere to all Alberta Safety Codes"); _REFERENCES.md Standard References.
- **Verification**: Electrical inspection sign-off; Safety Code permit close-out.

### REQ-013-06-05: Structural Adequacy
The ceiling mounting structure (structural attachment point — type TBD per Datasheet Conditions, see Conflict Table CF-013-06-03) shall be capable of supporting the fan dead load plus dynamic (vibration) loading. Structural adequacy shall be confirmed by the Structural Engineer of Record or a qualified structural engineer prior to installation.
- **Source**: _DEPENDENCIES.md Constraint Notes ("Ceiling structure must support fan weight and vibration"); _REFERENCES.md Approval Documents ("Structural engineer approval (load-bearing)").
- **Verification**: Structural engineer written approval or stamped drawing prior to fan installation.

### REQ-013-06-06: Clearance from Overhead Cranes
Fan blade tip clearance from the operating envelope of the two (2) 5-tonne overhead cranes shall meet or exceed the requirements of applicable Alberta Safety Codes and manufacturer minimum clearance specifications.
- **Source**: App B-Shop (R-04) and App B-Elec (R-05) — cranes shown in main shop area; _DEPENDENCIES.md Constraint Notes ("Adequate clearance required for safe operation").
- **Note**: Crane hook height and crane rail elevation are TBD from structural/crane shop drawings (DEL-002 / DEL-016 interface). Clearance confirmation requires IFC crane and structural drawings. **Specific applicable code clause and numeric clearance minimum TBD (A-003).** PROPOSAL: Safety Codes Officer or Mechanical Engineer to identify applicable Alberta Building Code / Safety Code clause and extract numeric clearance minima.
- **Verification**: Design review against IFC crane and structural drawings; field verification prior to energisation.

### REQ-013-06-07: Minimum Blade-to-Floor Clearance
Fan blade assemblies shall maintain minimum clearance above finished floor level as required by applicable building codes and safety standards.
- **Source**: _REFERENCES.md Standard References ("Safety standards for ceiling-mounted equipment"); Alberta Building Code (location TBD — ASSUMPTION: likely applicable).
- **Note**: At 35 ft ceiling height (App B-Shop, R-04), fan mounting height will depend on downrod length selected during design. **Specific applicable code clause and numeric minimum clearance value TBD (A-003).** PROPOSAL: Safety Codes Officer or Mechanical Engineer to identify applicable Alberta Building Code / Safety Code clause and extract numeric clearance minimum.
- **Verification**: Design drawing review; field measurement.

### REQ-013-06-08: Equipment Durability and Product Safety Certification
Fans shall be industrial or heavy-commercial grade, suitable for continuous operation in a shop environment subject to dust, vehicle exhaust, welding fumes, and temperature cycling.
- **Source**: _CONTEXT.md Key Requirements ("Durable equipment for facility environment"); _DEPENDENCIES.md description of co-located exhaust systems.
- **Environmental Protection Rating (E-003)**: Minimum IP or NEMA enclosure rating for fan motors TBD. The operating environment (dust, vehicle exhaust, welding fumes, temperature cycling) suggests at least IP44 or NEMA 3/12 would be appropriate. PROPOSAL: Mechanical Engineer to specify minimum IP/NEMA rating appropriate for the operating environment. ASSUMPTION: IP44 or equivalent is likely minimum; confirm with Mechanical Engineer.
- **Product Safety Certification (X-004)**: All ceiling fans shall bear CSA, UL, or equivalent product safety certification (e.g., CSA C22.2 No. 113 or UL 507). Product safety certification is mandatory for electrical inspector acceptance. ASSUMPTION: CSA or equivalent certification will be required; this should be verified with the electrical Safety Codes Officer.
- **Note (A-001)**: Whether the fan type must be specifically HVLS or may be any industrial fan that meets performance criteria is TBD. Guidance P2 strongly implies HVLS is the appropriate product type for a 35 ft ceiling, but this requirement currently says "industrial or heavy-commercial grade" without mandating HVLS. PROPOSAL: Mechanical Engineer to determine whether to mandate HVLS or to state minimum performance criteria (e.g., minimum airflow volume, minimum effective coverage area per fan) that effectively select the appropriate fan type.
- **Verification**: Manufacturer specification review; submittals; CSA/UL certification verification.

### REQ-013-06-09: Integration with HVAC System
Ceiling fan controls shall be compatible with and not adversely interfere with the operation of the heating system (DEL-013-01), air exchanger (DEL-013-02), makeup air (DEL-013-03), equipment exhaust (DEL-013-04), and welding exhaust (DEL-013-05) systems.
- **Source**: _CONTEXT.md Key Requirements ("Integration with overall HVAC system"); _DEPENDENCIES.md Support Functions.
- **Verification**: Commissioning test confirming no interference with co-located systems. **Acceptance criteria for "no adverse interference" TBD (X-003):** Observable indicators of adverse interaction should be defined (e.g., exhaust capture efficiency reduction at welding hoods, thermostat cycling instability, pressure imbalance at exhaust hoods). PROPOSAL: Define specific observable indicators of adverse interaction for the commissioning test protocol.

### REQ-013-06-10: Noise Level
Fan operating noise at all speed settings shall not exceed TBD dBA measured at TBD distance/condition.
- **Source**: _DEPENDENCIES.md Constraint Notes ("Noise levels must be acceptable for work environment").
- **Note (A-002)**: The previous language "acceptable for a maintenance shop work environment" is subjective and unenforceable. A numeric dBA threshold and measurement method are required for objective compliance determination. PROPOSAL: Mechanical Engineer to specify dBA limit or reference applicable occupational noise standard (e.g., Alberta OHS Code Part 16 noise limits). **Measurement method TBD (X-002):** Specify measurement protocol (e.g., sound level meter reading at 1.5 m floor level, all fans running at maximum speed) and pass/fail threshold.
- **Verification**: Sound level measurement at commissioning per defined protocol; manufacturer spec review.

### REQ-013-06-11: Control System
Each fan shall be individually controllable. Speed control (minimum 2 speeds) shall be provided. Direction reversal (for winter destratification and summer cooling modes) is TBD — status of this requirement (mandatory vs. recommended) requires resolution.
- **Source**: _CONTEXT.md Scope ("Control system integration; Balancing and speed verification").
- **Note (C-001)**: The previous language said direction reversal "is recommended," but the Verification table (Procedure Step 7.1) requires "Both forward and reverse modes confirmed operational," implying it is mandatory for acceptance. This inconsistency must be resolved. PROPOSAL: Mechanical Engineer to rule on whether reversibility is mandatory (shall) or recommended (should); update requirement language and verification criteria accordingly. If mandatory, use "shall" language. If recommended, remove from verification pass/fail criteria.
- **Verification**: Functional test of all speed settings at commissioning. Direction reversal verification: TBD pending resolution of mandatory/recommended status (C-001).

### REQ-013-06-12: Balancing and Vibration
Each fan shall be balanced in accordance with manufacturer instructions to eliminate excessive vibration prior to final acceptance.
- **Source**: _CONTEXT.md Scope ("Balancing and speed verification").
- **Vibration Acceptance Threshold (F-001)**: TBD — a measurable vibration pass/fail criterion is required. Current language ("vibration observation at all speeds") and Procedure Step 7.3 ("vibration is within manufacturer limits") reference manufacturer limits that are not yet available. PROPOSAL: Reference manufacturer vibration limits once equipment is selected; add measurable pass/fail criterion to this requirement (e.g., maximum vibration velocity in mm/s at bearing housing, or manufacturer-specified limit).
- **Verification**: Commissioning record; vibration measurement at all speeds against defined threshold.

### REQ-013-06-13: Warranty (F-002)
The fan manufacturer shall provide a minimum warranty covering parts and labor for a period of TBD years from the date of substantial completion. Warranty scope, duration, and start date shall be confirmed with the Owner.
- **Source**: Procedure Step 8.2 references warranty documentation in O&M manuals; Records table lists "Fan warranty certificates." ASSUMPTION: A minimum warranty period is expected but no specific duration is stated in project sources.
- **Note (F-002)**: Warranty is part of the total assurance registry for this deliverable. Without a specified minimum warranty period, the Owner has no basis to evaluate or enforce warranty terms. PROPOSAL: Confirm Owner expectations for minimum warranty period (e.g., minimum 1-year manufacturer warranty) and add to contract requirements.
- **Verification**: Warranty certificate review at handover; confirmed warranty period meets or exceeds specified minimum.

---

## Standards

The following standards are expected to apply. Specific clause references are TBD unless noted; ASSUMPTION: likely applicable based on project jurisdiction (Alberta, Canada) and deliverable type.

| Standard | Description | Applicability | Location |
|---|---|---|---|
| Alberta Building Code (ABC) | Building code requirements including ceiling-mounted equipment, occupancy, and safety. **Specific clause references for blade-to-floor clearance and blade-to-crane clearance TBD (A-004).** PROPOSAL: Design-Builder's P.Eng. to identify applicable clauses during design phase. | Mandatory | Location TBD — A-004 |
| Alberta Electrical Code (AEC) / Canadian Electrical Code Part I (CSA C22.1) | Electrical installation of fan branch circuits and connections. **Specific clause references TBD (A-004).** | Mandatory | Location TBD — A-004 |
| Alberta Safety Codes Act | Umbrella safety code framework; Safety Code permits required. **Note (C-002):** Determine whether a separate mechanical Safety Code permit is required for ceiling fan installation in addition to the electrical permit. PROPOSAL: Confirm with Safety Codes Officer. | Mandatory | RFP §3.3.2 (R-01) |
| CCDC 14–2013 | Design-Build Stipulated Price Contract form | Contract | RFP §2.7 (R-01) |
| Manufacturer Installation Instructions | Fan-specific structural attachment, downrod, wiring, and balancing requirements | Mandatory | TBD — to be provided with equipment submittals |
| CSA C22.2 No. 113 (or equivalent UL 507) | Ceiling fan product safety standard. **All ceiling fans shall bear CSA, UL, or equivalent product safety certification (X-004).** | Mandatory — ASSUMPTION: required for electrical inspector acceptance | Location TBD — A-004 |

---

## Verification

| Requirement | Verification Method | Timing | Acceptance Criterion |
|---|---|---|---|
| REQ-013-06-01: Quantity (6 fans) | Physical count at completion inspection | Pre-acceptance | 6 fans installed |
| REQ-013-06-02: Installation location | Drawing review (IFC vs. as-built); field walk | Design + post-installation | Fan locations match IFC drawings |
| REQ-013-06-03: Air circulation function | Commissioning functional test | Commissioning | TBD — measurable criterion required (X-001): minimum air velocity or maximum temperature differential |
| REQ-013-06-04: Code-compliant electrical | Electrical Safety Code inspection and permit sign-off | During/post installation | Inspection passed; no outstanding deficiencies |
| REQ-013-06-05: Structural adequacy | Structural engineer approval documentation | Pre-installation | Stamped drawing or written approval on file |
| REQ-013-06-06: Crane clearance | Design drawing review; field measurement | Design + post-installation | Clearance meets or exceeds code minimum (value TBD) |
| REQ-013-06-07: Blade-to-floor clearance | Drawing review; field measurement | Design + post-installation | Clearance meets or exceeds code minimum (value TBD) |
| REQ-013-06-08: Equipment durability and certification | Submittal review (manufacturer spec sheet); CSA/UL certification check | Pre-procurement | Manufacturer spec meets environmental requirements; valid CSA/UL/equivalent certification confirmed |
| REQ-013-06-09: HVAC integration | Commissioning test (co-running with other systems) | Commissioning | No adverse interaction per defined indicators (TBD — X-003) |
| REQ-013-06-10: Noise level | Sound level measurement per defined protocol | Commissioning | Does not exceed TBD dBA at defined measurement point (A-002, X-002) |
| REQ-013-06-11: Control system | Functional test at commissioning | Commissioning | All speed settings operate; direction reversal TBD (C-001) |
| REQ-013-06-12: Balancing and vibration | Vibration measurement at all speeds | Commissioning | Vibration does not exceed TBD threshold (F-001) |
| REQ-013-06-13: Warranty | Warranty certificate review | Handover | Warranty period meets or exceeds TBD minimum |

---

## Documentation

The following artifacts shall be produced as part of this deliverable:

| Artifact | Description | Timing | Notes |
|---|---|---|---|
| Equipment Submittal | Manufacturer product data sheets, shop drawings, mounting details, electrical data, CSA/UL certification, IP/NEMA rating for Owner/Engineer review | Pre-procurement | — |
| IFC Layout Drawing | Fan locations shown on mechanical or electrical IFC drawing, signed/stamped by P.Eng. (Alberta) | Pre-installation | — |
| Structural Approval | Written confirmation or stamped drawing from Structural Engineer confirming ceiling attachment adequacy | Pre-installation | — |
| Safety Code Permit | Electrical permit required; mechanical permit TBD (C-002) — confirm with Safety Codes Officer | Pre-installation | — |
| Commissioning Report | Record of functional tests, speed/direction verification, balancing results, vibration measurement, noise measurement, HVAC integration test results | Post-installation | — |
| As-Built Drawing | Updated drawing showing final fan locations and electrical connections. **Note (E-002):** As-Built Drawing supersedes IFC Layout Drawing and must reflect all field changes made during installation. | Post-installation | Supersedes IFC Layout Drawing |
| O&M Manuals | Manufacturer operation and maintenance manuals for all fan models installed. **Must include maintenance access method and recommended access equipment for 35 ft ceiling height (E-004).** | At handover | See Guidance Considerations "Maintenance Access" |
| Inspection Reports | Copies of all Safety Code inspection reports provided to Owner | Post-inspection | — |
| Installation Photographs (X-006) | Photographic documentation of installation stages: mounting brackets installed, structural connections, pre-energisation state | During installation | Provides audit record for hidden conditions (structural connections) that cannot be reinspected after completion |
| Fan Warranty Certificates | Warranty documentation confirming coverage period, scope, and terms per REQ-013-06-13 | At handover | — |

Source: _CONTEXT.md Scope (anticipated artifacts); RFP §3.3.2 (R-01) ("Submit all inspection requests ... provided with a copy of all complete inspection reports").

---

## Semantic Lensing Enrichment Log (Pass 3)

The following warranted items from `_SEMANTIC_LENSING.md` were incorporated into this document during Pass 3:

| ItemID | Type | Action Taken |
|---|---|---|
| A-001 | WeakStatement | Added note to REQ-013-06-08 clarifying HVLS vs. general industrial fan ambiguity; proposed resolution via performance criteria |
| A-002 | WeakStatement | Replaced subjective noise language in REQ-013-06-10 with TBD numeric dBA threshold requirement |
| A-003 | TBD_Question | Enhanced REQ-013-06-06 and REQ-013-06-07 with explicit note about missing code clause and numeric clearance values |
| A-004 | MissingSlot | Added specific clause reference TBDs to Standards table entries for ABC, AEC, and CSA C22.2 No. 113 |
| C-001 | WeakStatement | Restructured REQ-013-06-11 to surface mandatory vs. recommended conflict for direction reversal; linked to verification |
| C-002 | TBD_Question | Added mechanical permit TBD to Standards table (Alberta Safety Codes Act) and Safety Code Permit in Documentation |
| E-002 | Normalization | Added note to As-Built Drawing clarifying it supersedes IFC Layout Drawing |
| E-003 | RationaleGap | Added IP/NEMA rating requirement to REQ-013-06-08 with proposed minimum |
| E-004 | Normalization | Added maintenance access requirement to O&M Manuals artifact |
| F-001 | VerificationGap | Added measurable vibration threshold requirement to REQ-013-06-12 |
| F-002 | MissingSlot | Added new REQ-013-06-13 (Warranty) with TBD duration |
| X-001 | VerificationGap | Added measurable acceptance criterion requirement for REQ-013-06-03 air circulation |
| X-002 | VerificationGap | Added measurement method and protocol requirement for REQ-013-06-10 noise verification |
| X-003 | WeakStatement | Added observable indicator definition requirement for REQ-013-06-09 HVAC integration verification |
| X-004 | MissingSlot | Added mandatory CSA/UL product safety certification to REQ-013-06-08 and Standards table |
| X-006 | MissingSlot | Added Installation Photographs to Documentation artifacts table |
