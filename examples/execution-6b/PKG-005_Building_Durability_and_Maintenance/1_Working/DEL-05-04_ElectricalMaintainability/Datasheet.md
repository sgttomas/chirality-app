# Electrical Maintainability — Datasheet

## Identification

| Property | Value |
|----------|-------|
| **Deliverable ID** | DEL-05-04 |
| **Name** | Electrical Maintainability |
| **Package** | PKG-005 — Building Durability & Maintenance |
| **Type** | Durability / Narrative |
| **Discipline** | Electrical Engineering |
| **Responsible Party** | Electrical Engineer |
| **Status** | INITIALIZED |
| **Covers Scope Items** | SOW-0013 |
| **Objective Support** | OBJ-005 — Demonstrate durability and ease of maintenance (15 pts) |
| **Evaluation Weight** | 15 points (Building Durability / Ease of Repair and Maintenance) |

---

## Attributes

### Scope Overview

| Attribute | Value |
|-----------|-------|
| **Design Life — Main Building** | 50 years (RFP §2.2, p. 7–8) |
| **Design Life — Cold Storage (ancillary)** | 20 years (Decomposition v2.3, PKG-005 goal) |
| **Applicable RFP Section** | §7.1.4 — "Describe the approach to building durability (both exterior and interior), including design approach, selection of various systems, components, materials, and construction methods used. Also describe the ease of repair and maintenance of the building and all systems and components." (RFP p. 17) |
| **Primary Subject Matter** | Electrical systems maintainability strategy for the PSB — panels, lighting, controls, IT/telecom, security/access control, fire alarm, and emergency power |
| **Discipline Coordination** | Electrical Engineer (primary); coordinates with Architectural (cable routing, fixture placement), Structural (conduit support), and Mechanical (HVAC equipment electrical interfaces, generator) |

### System Coverage

| System | Primary Maintainability Aspect | Design Life Context |
|--------|-------------------------------|---------------------|
| **Electrical Panel & Distribution** | Panel accessibility; spare capacity; circuit labeling; future flexibility | 50-yr main / 20-yr Cold Storage |
| **Lighting Systems** | Standardized LED fixture/driver types; fixture access; wet-location rating in bays; lifecycle planning | 50-yr main / 20-yr Cold Storage |
| **Building Controls & Management** | Control system serviceability; zone isolation capability; programming documentation | 50-yr main |
| **IT / Telecom Infrastructure** | Structured cabling; conduit access; labeling; spare capacity; IT room accessibility | 50-yr main |
| **Security & Access Control** | System lifecycle; upgrade provisions; open-standards preference; key fob zones per Functional Program | 50-yr main (Optional Items 3 + 4) |
| **Fire Alarm System** | Component standardization; addressable architecture; testing accessibility; code upgrade compatibility | 50-yr main |
| **Emergency / Backup Power** | Generator integration; transfer switch serviceability; load testing provisions | 50-yr main |
| **UPS (Uninterruptible Power Supply)** | IT room power transition continuity during utility-to-generator switchover; protects active emergency management sessions | 50-yr main |
| **Solar-Ready Provisions** | Conduit rough-in; panel space reservation; inverter location designation for future PV | 50-yr main |

---

## Conditions

### Operational Environment

| Condition | Description | Source |
|-----------|-------------|--------|
| **Facility Type** | Combined Fire Hall + Public Works Operations (main building); Cold Storage (unheated ancillary) | RFP §2.2 (p. 7–8) |
| **Primary Users** | Volunteer firefighters and crew members; municipal public works staff — not professional electricians | RFP OSR §10.3.4 (p. 39) |
| **Usage Pattern** | 24/7 fire hall operations; regular municipal operations hours for Public Works | RFP OSR §10.3.5 (p. 40) implied |
| **Environmental Exposure — Apparatus Bays** | Vehicle exhaust and combustion particulates; moisture from snow-melt and bay sumps; de-icing salt tracked in from apparatus; heavy vibration from apparatus operation | RFP Addendum 03 §1.8 (bay sumps); RFP OSR §10.3.4 (p. 39) |
| **Environmental Exposure — Cold Storage** | Unheated building; Alberta freeze-thaw cycles; condensation risk | RFP OSR §11.1.2; Addendum 03 general |
| **Services at Site** | Electrical and communications are within a few feet of the site | Addendum 03 §1.6 |
| **Building Code** | NBCC; Alberta Building Code; fire code requirements | RFP §7.2 (p. 19); §1 (Definitions, p. 6) |
| **Electrical Code** | Canadian Electrical Code Part I (CEC) — **ASSUMPTION: applicable per local AHJ; specific clause locations TBD** | ASSUMPTION |

### Key Electrical Program Requirements — Functional Program (App B, p. 46)

| Space | Electrical / IT Requirements | Source |
|-------|------------------------------|--------|
| **Apparatus Bay 1** | 120V/20A drops from ceiling; 2-vehicle exhaust fume removal systems; compressed air lines dropped from ceiling; LED lighting; Bay Door: 16 ft × 16 ft | RFP App B (row 1.0, p. 46); Addendum 03 §1.10 |
| **Apparatus Bays 2 / 3 / 4** | 120V/20A drops from ceiling; 2-vehicle exhaust fume removal systems; compressed air; LED lighting; OH doors 14 ft × 14 ft (note: Addendum 03 §1.10 sets 16 ft minimum for main building doors) | RFP App B (rows 2.0–4.0, p. 46); Addendum 03 §1.10 |
| **Electrical Room** | Electrical systems; Key Fob access | RFP App B (row 13.0, p. 46) |
| **IT Room** | 2 needs / server room; Key Fob access | RFP App B (row 17.0, p. 46) |
| **Meeting Room / ICP** | Multiple displays, projector, training and Incident Command Post; multiple outlets; generator-backed (kitchen + ICP + 2 bathrooms minimum) | RFP App B (row 19.0, p. 46); Addendum 03 §1.15 |
| **Bunker Gear / Lockers** | LED lighting; outlets; fans; 40 bunker gear lockers; 2 bathrooms / change rooms; 2 standalone showers | RFP App B (row 22.0, p. 46); Addendum 03 §1.13 |
| **Workshop / Storage Bays** | LED lighting; 120V outlets; air circulation; air lines hard-plumbed throughout | RFP App B (rows 27.0–28.0, p. 46) |
| **Generator Area (outdoor)** | Dusk-to-dawn lights; perimeter-activated emergency lighting | RFP App B (row 30.0, p. 46); Addendum 03 §1.15 |
| **Cold Storage** | Motion-activated LED lighting (interior and exterior); 120V outlets interior; GFCI protection where moisture exposure is likely (**ASSUMPTION: GFCI requirement subject to CEC requirements at detailed design**) | RFP App B (row 32.0, p. 46); CEC (ASSUMPTION: applicable) |

### Key Addendum 03 Requirements Affecting Electrical Systems

| Addendum Item | Requirement | Reference |
|--------------|-------------|-----------|
| §1.8 | All bays require sumps — moisture management in bay electrical environment | Addendum 03 §1.8 |
| §1.10 | Minimum 16 ft overhead door height for main building | Addendum 03 §1.10 |
| §1.15 | Backup generator required; minimum loads = kitchen + meeting room (ICP) + 2 bathrooms; bay doors need secondary opening (generator OR manual) | Addendum 03 §1.15 |
| §1.16 | Water fill stations — 2" minimum, one in fire apparatus bay, one in PW bay | Addendum 03 §1.16 |
| §1.17 | Solar-capable roofing required; orientation: flat, south, west, or southwest | Addendum 03 §1.17 |
| §1.19 | No Town preference on security/camera suppliers; interoperability to be preserved | Addendum 03 §1.19 |

---

## Construction

### Narrative Outline (Deliverable to be Produced)

The electrical maintainability narrative addresses the following seven subject areas:

**1. Electrical Panel & Distribution Accessibility**
- Main service entrance and distribution panel location — designed for direct, unobstructed access without moving equipment or vehicles; dedicated electrical room (Functional Program row 13.0) with key fob access
- Spare breaker capacity at commissioning — **ASSUMPTION: minimum 20% spare capacity is typical practice for municipal facilities; specific percentage TBD at detailed design. See Guidance Conflict Table CON-001 for 20% vs. 25% discrepancy requiring Electrical Engineer resolution.**
- Sub-panel placement in apparatus bay, workshop areas, and office zones for localized service
- Conduit and cable tray routing with pull access points for future cable additions
- Circuit labeling protocol: all circuits labeled at panel and at termination point using durable engraved or laminated labels matching design drawings (Source: RFP OSR §10.4, p. 42)

**2. Lighting System — Standardization and Serviceability**
- LED fixture types standardized by zone category (apparatus bay industrial, office/shared, storage, outdoor) to minimize spare parts inventory
- IES-compliant lighting levels per zone type (Source: RFP OSR §10.5, p. 42)
- Emergency exit lights: internal battery type per code, accessible for battery testing and replacement (Source: RFP OSR §10.5, p. 42)
- Weatherproof fixture covers and switches at person doors of ancillary buildings (Source: RFP OSR §10.5, p. 42)
- Fixture mounting heights adjusted to avoid interference with machinery in apparatus bays and workshop bays (Source: RFP OSR §10.5, p. 42)
- Apparatus bay fixtures: IP65 minimum rated for wet/damp location; periodic lens cleaning required due to exhaust particulate
- Cold Storage: motion-activated LED (interior and exterior); cold-rated for Alberta freeze-thaw environment (Source: RFP App B, row 32.0, p. 46)
- Driver/LED module lifecycle: **ASSUMPTION: 50,000–100,000 operating hours typical (approximately 15–25 years); specific lifecycle TBD at detailed design**

**3. Building Controls & Management System Serviceability**
- Lighting controls (occupancy sensors, scheduling) selected from widely-supported product lines with local Alberta parts availability
- Zone-based circuit isolation — individual zones de-energizable without shutting down entire building
- Control panels and junction boxes accessible without tools from finished surfaces where possible
- Programming documentation (logic diagrams, zone maps, backup files) included in O&M manual
- Proprietary single-source dependencies minimized; vendor support requirements confirmed at procurement

**4. IT / Telecom Infrastructure Maintainability**
- Structured cabling installed in conduit or cable tray throughout main building; supports future re-cabling without demolition (Source: RFP OSR §10.6, p. 42)
- IT/Data compatibility throughout main structure (Source: RFP OSR §10.6, p. 42)
- Meeting room / ICP: minimum 15 concurrent internet access points for Emergency Management (Source: RFP OSR §10.6, p. 42)
- Fire apparatus bay display system (wall-mounted, laptop-connect for dispatch data) in bay closest to office area (Source: RFP OSR §10.6, p. 42)
- PA system throughout main structure; not required in ancillary buildings (Source: RFP OSR §10.6, p. 43)
- Network equipment room (IT Room, row 17.0) sized for patching, future equipment, and aisle clearance
- All cable runs labeled at both ends; cable schedule documented in as-built drawings
- Spare conduit stubs in accessible locations for future IT/telecom expansion

**5. Security & Access Control System Lifecycle (Optional Items 3 + 4)**
- Key Fob access control for electrical room, IT room, and other controlled zones per Functional Program (Source: RFP App B rows 13.0, 17.0, p. 46)
- Access control: multiple zones within main structure for shared space use and interdepartmental control; ancillary buildings excluded (Source: RFP OSR §12.3, p. 44)
- Access control hardware selected with open or widely-supported protocol to avoid vendor lock-in
- Security and camera system (Optional Item 4): interior and exterior cameras; installation and monitoring costs priced separately (Source: RFP OSR §12.4, p. 44)
- No Town preference on security/camera suppliers (Source: Addendum 03 §1.19); interoperability preserved
- Spare capacity in access control panel for future zone additions

**6. Fire Alarm System Maintenance Approach**
- Fire alarm system from ULCS527-certified product line; addressable architecture; components standardized to minimize SKU count
- All initiating and notification devices mounted at accessible heights; service access via standard ladder
- Annual inspection and testing: pull stations, smoke/heat detectors, and annunciator panel accessible without obstruction
- Fire alarm interfaced with access control and emergency lighting per AHJ requirements — **ASSUMPTION: interface requirements to be confirmed with AHJ at design stage**
- Upgrade compatibility: system reprogrammable; addressable architecture avoids full panel replacement for code updates

**7. Emergency / Backup Power Integration**
- Generator (outdoor, diesel standby): minimum load coverage = kitchen + ICP/meeting room + 2 bathrooms; bay doors with secondary opening mechanism — generator-powered OR manual (Design-Builder's choice) (Source: Addendum 03 §1.15)
- Transfer switch location accessible for testing and service (indoor, heated location preferred)
- Generator control panel and annunciator located in accessible indoor location (not solely on outdoor enclosure)
- Permanent load bank connection provision recommended for monthly load testing
- Solar-ready electrical rough-in: conduit stubs from roof to electrical room; panel space reserved; inverter location designated (Source: Addendum 03 §1.17)
- Fuel system designed to allow inspection without confined-space entry — **ASSUMPTION: TBD at detailed design**

---

## References

### Source Documents Used

| Source | Section | Pages | Accessibility |
|--------|---------|-------|---------------|
| RFP (AB-2024-07156-Penhold Public Services Building RFP_2024_004.pdf) | §7.1.4 — Building Durability / Ease of Repair and Maintenance | p. 17 | Accessible |
| RFP — OSR (Appendix A) | §10.4 Electrical System; §10.5 Lighting System; §10.6 IT & Telecom | pp. 42–43 | Accessible |
| RFP — OSR (Appendix A) | §12.3 Access Control; §12.4 Security and Camera System | p. 44 | Accessible |
| RFP — OSR (Appendix A) | §11.3 Materials | p. 44 | Accessible |
| RFP — OSR (Appendix A) | §10.3.4 Project Design; §10.3.5 Structural Objectives | pp. 39–40 | Accessible |
| RFP — Functional Program (Appendix B) | Room-level electrical/IT requirements | p. 46 | Accessible |
| Addendum 03 (AB-2024-07156-Penhold_Public Services Building Addendum03.pdf) | §1.6 (services on site); §1.8 (sumps); §1.10 (door heights); §1.13 (bunker gear lockers); §1.15 (generator); §1.16 (fill stations); §1.17 (solar); §1.19 (security suppliers) | pp. 3–4 of 5 | Accessible |
| Decomposition v2.3 FINAL | §9, DEL-05-04 definition; PKG-005 goal statement | — | Accessible |

### Cross-References

| Deliverable | Relationship |
|-------------|-------------|
| DEL-02-05 — Electrical/IT Concept Narrative | Conceptual design baseline; maintainability narrative must align with systems described there |
| DEL-04-03 — Electrical Energy Efficiency | Energy efficiency choices (LED standards, controls, solar-ready provisions) directly affect lifecycle cost and maintenance intervals |
| DEL-05-03 — Mechanical Maintainability | Mechanical-electrical interfaces (HVAC electrical connections, exhaust fans, generator, bay sump pumps) coordinated here |
| DEL-03-05 — Electrical/IT Design Brief | Design brief provides system philosophy; maintainability narrative adds operations-stage considerations |
| DEL-05-01 — Architectural Durability | Apparatus bay environment (mud, salt, moisture) establishes shared durability context |

### Standards Referenced

| Standard | Application | Status |
|----------|-------------|--------|
| Canadian Electrical Code Part I (CEC) | All electrical installation | **ASSUMPTION: applicable per local AHJ; specific clause TBD** |
| IES (Illuminating Engineering Society) | Lighting levels and fixture selection | Explicitly required by RFP OSR §10.5 (p. 42) |
| NBCC and Alberta Building Code | Emergency lighting, exit signs, safety, accessibility | Referenced in RFP §7.2 (p. 19); §1 (Definitions, p. 6) |
| CAN/ULC-S527 (or equivalent) | Fire alarm control equipment | **ASSUMPTION: applicable; location TBD** |
| TIA-568 (or equivalent Canadian standard) | Structured cabling | **ASSUMPTION: applicable for IT/telecom infrastructure; TBD** |
| CCDC 14-2013 (+ Appendix J Supplementary Conditions) | Contract framework; quality standards | RFP §1 (p. 6); App J (p. 61) |
| CSA C282 / NFPA 110 (or Canadian equivalent) | Emergency generator installation | **ASSUMPTION: applicable; Canadian equivalent to be confirmed; TBD** |
