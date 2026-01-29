# Guidance: DEL-09.01 Marine Outfitting Design Drawing Set

## Purpose

This guidance document supports the development of **Marine Outfitting Design Drawing Set** for **PKG-09 Marine Outfitting**.

**Decomposition definition (authoritative):** Defines the design arrangement and details for marine outfitting per Employer's Requirements. (**Source:** Decomposition, DEL-09.01 row)

This deliverable is classified as a **Drawing** under the **Marine** discipline, to be produced by **D&B Contractor**.

**Downstream use:** The drawing set serves as the primary coordination and construction artifact for marine outfitting elements (fenders, bollards, ladders, life-saving equipment, Berth 10 upgrades/repairs). It translates design basis (from PKG-08 analyses and Employer's Requirements) into fabrication/installation instructions for construction execution.

## Principles

### Design Intent (Package Scope)

PKG-09 includes fenders, bollards, ladders, life-saving equipment, and existing Berth 10 upgrades/repairs. The drawing set is the primary coordination artifact for these elements — capturing geometry, setting-out, and installation details for construction.

**Design philosophy:**
- **Functionality:** Marine outfitting must support safe vessel berthing, mooring, cargo transfer operations, and personnel access/egress.
- **Durability:** Equipment must withstand marine environment (corrosion, UV, impact, cyclic loading) over design life.
- **Maintainability:** Design should facilitate inspection, maintenance, and component replacement.
- **Regulatory compliance:** All equipment and installations must comply with Employer's Requirements and applicable codes/standards (safety, marine, port authority).

**Cross-reference:** Requirements are defined in `Specification.md § 1`.

### Fenders (supports SPEC § 1.1)

**Purpose:** Fenders absorb berthing energy and protect the vessel hull and marine structure during berthing operations.

**Design basis:**
- Fender selection and arrangement are driven by:
  - **Berthing energy calculations (DEL-08.06):** Vessel characteristics (displacement, beam, velocity), approach velocity, environmental conditions (wind, current, waves), berthing angle.
  - **Fender system deflection characteristics (DEL-08.07):** Reaction force vs deflection curves for candidate fender systems; energy absorption capacity.
  - **Supplier design verification (DEL-08.08):** Confirmation of fender performance and suitability for design conditions.
- The drawings must show fender locations that provide adequate protection across the design vessel envelope while interfacing correctly with the marine structure (PKG-08).

**Key considerations:**
- **Fender type selection:** Consider cylindrical fenders, cone fenders, cell fenders, or arch fenders based on berthing energy, vessel characteristics, and interface constraints. (**TBD** — pending fender selection)
- **Fender spacing and coverage:** Ensure fender spacing provides continuous protection along berthing face; avoid gaps that could allow hull/structure contact.
- **Structural interface:** Fender reaction forces must be transferred to marine structure (PKG-08) via properly designed mounting hardware and structural supports. Coordinate with PKG-08 for structural capacity and connection details.
- **Vertical positioning:** Fender elevation must accommodate tidal range, vessel draft variations, and vessel freeboard to ensure effective contact during berthing. (**TBD** — site-specific tidal data and vessel design envelopes)

**ASSUMPTION:** Fender type and sizing will be coordinated with PKG-08 Marine Structures design and berthing energy analysis results prior to finalizing drawing set.

### Bollards (supports SPEC § 1.2)

**Purpose:** Bollards provide mooring attachment points for vessel lines during cargo transfer operations.

**Design basis:**
- Bollard locations and capacities are driven by:
  - **Mooring analysis (DEL-08.09):** Mooring line loads under design environmental conditions (wind, current, waves); vessel drift forces; line angles and geometry.
  - **Design vessel characteristics:** Mooring arrangement typical for design vessel class; number of lines, line types, and pretension.
  - **Operational requirements:** Mooring arrangement must accommodate cargo transfer operations and allow for vessel adjustments during loading/unloading.

**Key considerations:**
- **Bollard capacity:** Bollard rated capacity (typically expressed in kN or tonnes bollard pull) must exceed maximum mooring line load from mooring analysis with appropriate safety factors. (**TBD** — safety factor per code/ER requirements)
- **Bollard type:** Consider Tee-head bollards, horn bollards, or cruciform bollards based on capacity requirements and operational preferences.
- **Bollard spacing and locations:** Position bollards to provide effective mooring coverage for design vessel; consider operational access, line angles, and coordination with other deck equipment.
- **Proof load testing:** Some codes/port authorities require proof load testing of bollards after installation. If required, provide provisions for testing (e.g., load test attachment points, procedures). (**TBD** — per ER/code requirements)
- **Foundation interface:** Bollard loads must be transferred to supporting structure via foundations/anchors (embedment plates, anchor bolts, grout). Coordinate with PKG-08 for structural capacity and foundation design.

**ASSUMPTION:** Bollard capacities will be defined by mooring analysis prior to detail design.

### Ladders & Access (supports SPEC § 1.3)

**Purpose:** Ladders provide safe access between deck levels and to/from water level for emergency and maintenance purposes.

**Design basis:**
- Ladder design considerations:
  - **Safety codes:** Compliance with occupational safety codes governing ladder design, including rung spacing, width, cage requirements, rest platforms, toe clearance.
  - **Access requirements:** Operational and emergency access needs; coordinate with operational workflows and emergency egress plans.
  - **Environmental durability:** Materials must resist marine corrosion environment (typically marine-grade stainless steel or hot-dip galvanized steel with appropriate coating).

**Key considerations:**
- **Ladder type:** Consider fixed vertical ladder with cage, ship's ladder (inclined), or companionway based on access frequency, vertical height, and space constraints.
- **Safety features:**
  - **Safety cages:** Required for vertical ladders exceeding threshold height (typically 2.4 m / 8 ft per codes). Cage should extend from threshold height to top, with appropriate cage diameter and clearances.
  - **Rest platforms:** Required for extended vertical climbing distances (typically every 9–12 m per codes). Platforms provide rest opportunities and emergency egress points.
  - **Fall protection:** Consider integration with fall arrest systems if required by codes or operational safety requirements.
- **Access locations:** Position ladders to support operational workflows (access to loading arms, fender/bollard inspection/maintenance, vessel mooring operations) and emergency egress requirements (multiple escape routes per codes).
- **Structural attachment:** Ladder loads (live load, impact) must be transferred to supporting structure. Coordinate with PKG-08 for attachment points and structural capacity.

**ASSUMPTION:** Ladder safety features will comply with applicable occupational safety codes (e.g., CSA Z259 series, OSHA 1910.27) as required by Employer's Requirements.

### Life-Saving Equipment (supports SPEC § 1.4)

**Purpose:** Life-saving equipment (life rings, rescue ladders, throw lines, etc.) provides emergency rescue capability for personnel overboard situations.

**Design basis:**
- Equipment types and coverage shall comply with:
  - **Employer's Requirements:** Specific equipment list and performance requirements. (**TBD**)
  - **Applicable port/marine safety regulations:** May include Transport Canada requirements, provincial port authority requirements, or other regulatory frameworks. (**TBD**)
  - **Industry standards:** SOLAS (Safety of Life at Sea) or equivalent for marine safety equipment (if applicable to port/terminal operations).

**Key considerations:**
- **Equipment types:** May include life rings (with or without self-igniting lights), rescue ladders, throw lines/rescue ropes, retrieval hooks, emergency lighting, first aid stations. (**TBD** — specific equipment list per ER)
- **Coverage and locations:** Position equipment to provide coverage along berthing face and operational areas; ensure visibility and accessibility during emergency situations; avoid obstructing operational equipment or personnel movement.
- **Mounting and accessibility:** Provide secure mounting that resists environmental loads (wind, corrosion) but allows rapid deployment in emergency; consider mounting height and accessibility for personnel of varying statures.
- **Maintenance provisions:** Design should allow for inspection and replacement of equipment (e.g., life ring inspection schedule, equipment replacement after use).

**ASSUMPTION:** Life-saving equipment requirements will be extracted from Employer's Requirements and applicable regulatory frameworks during design development.

### Evidence Rules

- **Source fidelity:** If a requirement or value is not supported by a source (Employer's Requirements, design basis, vendor data, design calculations), label it **TBD** or **ASSUMPTION** and record the needed source.
- **Traceability:** All design decisions affecting marine outfitting arrangement should be traceable to input documents (berthing energy analysis, mooring analysis, codes/standards, ER).
- **Interface coordination:** All interfaces to PKG-08 Marine Structures and other packages must be explicitly identified and coordinated via interdisciplinary check (IDC) per `Procedure.md § Step 6`.

## Considerations

### Factors to Consider During Development

| Factor | Consideration | Reference |
|--------|---------------|-----------|
| Scope boundary | Confirm interface between PKG-08 Marine Structures and PKG-09 Marine Outfitting — where does structural design end and outfitting begin? | `Specification.md § 3` |
| Equipment mapping | Identify all marine outfitting items required by Employer's Requirements and map to drawings/sheets — ensure no scope gaps | `Datasheet.md Content Checklist` |
| Existing works | Berth 10 condition and repair scope — inputs **TBD** (survey/inspection findings, as-built documentation) | `Specification.md § 1.5` |
| Corrosion protection | Coatings and materials requirements per Employer's Requirements — coordinate with PKG-08 to ensure consistent corrosion protection strategy | `Specification.md § 1.6` |
| Constructability | Access for installation and inspection; lifting/handling constraints; construction sequencing (e.g., install fenders before or after structural completion?) | `Procedure.md § Steps 3, 4` |
| Operability | Layout should not impede cargo transfer operations or vessel maneuvering; consider line-of-sight for operators, safety zones, emergency egress | — |
| Maintenance | Provide access for inspection, maintenance, and replacement of equipment; consider equipment service life and replacement intervals | — |

### Existing Works (Berth 10)

- The scope includes upgrades and repairs to existing Berth 10 infrastructure.
- Design development requires:
  - **As-built survey/condition assessment:** Obtain survey data and condition assessment of existing elements (fenders, bollards, ladders, structural supports) to identify repair extents and remaining service life.
  - **Identification of repair extents and tie-in constraints:** Determine what can be retained, what must be repaired, and what must be replaced; identify tie-in constraints (geometry, structural capacity, access).
  - **Coordination with ongoing terminal operations:** Consider phasing of repairs to minimize disruption to terminal operations; coordinate with operational shutdown windows if required.
- **TBD:** Specific repair scope pending Employer's Requirements extraction and condition survey inputs.

### Tidal Range and Environmental Conditions

- **Tidal range:** Fender and ladder positioning must account for site-specific tidal range to ensure effective functionality across tidal cycle. Obtain tidal data for site (high water, low water, mean tide levels). (**TBD**)
- **Environmental loads:** Marine outfitting equipment must resist environmental loads (wind, waves, ice if applicable, vessel impact). Coordinate with PKG-08 for environmental load criteria. (**TBD**)
- **Corrosion environment:** Marine environment (salt water, salt spray, UV) imposes severe corrosion demands. Specify corrosion-resistant materials (marine-grade stainless steel, hot-dip galvanized steel) and protective coatings per Employer's Requirements and PKG-08 materials specifications.

## Trade-offs

### Competing Concerns to Evaluate

| Trade-off | Factors | Resolution Approach |
|-----------|---------|---------------------|
| Fender arrangement vs structural demands | Larger/more fenders increase protection but impose higher reaction loads on marine structure; must balance vessel protection with structural capacity/cost | Optimize based on berthing energy analysis; coordinate with PKG-08 structural design to ensure structural capacity matches fender loads; consider fender type (lower-reaction fenders may reduce structural demands) |
| Bollard positions vs operability | Bollard locations must serve mooring requirements without obstructing deck operations, cargo transfer equipment, personnel access | Coordinate with mooring analysis for required bollard locations; review layout with operational stakeholders; consider recessing bollards or using folding/retractable types if deck space constrained |
| Ladder locations vs access/safety | Ladders must be positioned for safe access but not obstruct equipment or create hazards; balance operational convenience with emergency egress requirements | Review against operational workflows and emergency egress plans; prioritize emergency egress requirements; consider multiple access points to provide redundancy |
| Standardization vs site-specific needs | Standard marine hardware may simplify procurement and reduce cost but may not suit all existing conditions (especially Berth 10 upgrades) | Balance standardization benefits (reduced procurement complexity, lower cost, proven performance) against specific interface constraints for Berth 10 upgrades; consider hybrid approach (standard hardware for new installations, custom solutions for existing interfaces) |
| Initial cost vs lifecycle cost | Higher-quality materials and corrosion protection increase initial cost but reduce maintenance and replacement costs over facility life | Conduct lifecycle cost analysis considering initial capital cost, maintenance frequency/cost, replacement intervals, and operational disruptions; prioritize lifecycle cost optimization per Employer's Requirements or project financial criteria |

## Examples

### Reference Checklists

- Use `Datasheet.md` (Content Checklist) as the minimum content checklist for this deliverable.
- Use the decomposition's anticipated artifacts as the baseline:
  - Fender arrangement drawings
  - Bollard installation details
  - Ladder details
- Expand as needed based on Employer's Requirements and operational requirements.

### Input Sources

| Input | Source Document | Purpose | Status |
|-------|-----------------|---------|--------|
| Berthing energy basis | DEL-08.06 Berthing Energy Calculation Report | Fender selection and sizing | **TBD** |
| Fender deflection data | DEL-08.07 Fender System Deflection Characteristics Data Package | Fender performance verification | **TBD** |
| Fender supplier verification | DEL-08.08 Fender Supplier Design Verification Letter/Report | Fender suitability confirmation | **TBD** |
| Mooring analysis | DEL-08.09 Mooring Analysis Report | Bollard locations and capacities | **TBD** |
| Marine structure geometry | DEL-08.01 Marine Structures Design Drawing Set | Interface coordination and structural geometry | **TBD** |
| Marine structure calculations | DEL-08.03 Marine Structures Design Calculations | Structural capacity for fender/bollard loads | **TBD** |
| Site survey/as-built (Berth 10) | Survey | Existing conditions and tie-in constraints | **TBD** |
| Employer's Requirements | ER Vol 2 Parts 1–3 | Requirements for marine outfitting equipment, materials, performance, safety | **TBD** — clauses to be extracted |

### Cross-Document Consistency

**Ensure consistency with other DEL-09.01 documents:**
- **Datasheet:** Content Checklist items match Specification requirements and Procedure steps.
- **Specification:** All requirements have corresponding rationale in this Guidance document and verification steps in Procedure.
- **Procedure:** All steps reference applicable Specification requirements and Guidance considerations.

### Employer's Requirements

Employer's Requirements clauses and applicable authority requirements are **TBD** — to be extracted and cited during design development (see `_REFERENCES.md`).

**Typical ER topics for marine outfitting (to be confirmed):**
- Fender system performance requirements (energy absorption, reaction force limits)
- Bollard capacity and spacing requirements
- Ladder and access design standards
- Life-saving equipment types and coverage
- Materials and corrosion protection requirements
- Quality assurance and testing requirements (e.g., proof load testing)
