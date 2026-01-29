# Assumptions Log — PKG-25 Communications & IT

**Snapshot ID:** EST_PKG25_DRAFT_2026-01-29_0004
**Package:** PKG-25 Communications & IT
**Date:** 2026-01-29

---

## Purpose

This log documents assumptions and allowances required to complete the estimate where project-specific data was not available. Each assumption is linked to affected line items and includes a path to resolution.

---

## A-2501: Fiber Optic Cabling System Scope

**Assumption:** Fiber optic cabling network includes:
- 800-1500 linear meters (LM) total fiber cable (backbone + distribution)
- Single-mode OS2 fiber for inter-building backbone (300-600 LM)
- Multi-mode OM3/OM4 fiber for intra-building distribution (500-900 LM)
- Fiber counts: 12-24 fiber typical per cable
- Termination and splicing at 6-10 locations

**Why Needed:** Network design (DEL-25.01) not complete; fiber routing and quantities TBD
**Impacted WBS/CBS:** MAT (fiber cables, connectors), CD (installation)
**Cost Impact:** $120,000 CAD (21% of base estimate)
**Confidence:** LOW
**Resolution Path:** Complete DEL-25.01 Communications Design Drawing Set with fiber network layout and cable schedule

**Referenced In:** BOE.md §5.3, §13; Detail.csv LineID 2501-01, 2501-02; Summary.md

---

## A-2502: Structured Copper Cabling System Scope

**Assumption:** Structured copper cabling network includes:
- 1500-2500 linear meters (LM) horizontal copper cabling (Cat 6 or Cat 6A)
- 50-100 workstation/device outlet locations
- 4-8 telecommunications rooms (TRs) with home runs
- Backbone copper cabling between ER and TRs (if applicable)

**Why Needed:** Building layouts (DEL-21.01) not available; port count matrix TBD
**Impacted WBS/CBS:** MAT (copper cables, jacks), CD (installation, termination, testing)
**Cost Impact:** $85,000 CAD (15% of base estimate)
**Confidence:** LOW
**Resolution Path:** Complete building layouts (PKG-21), define workstation locations and device requirements, develop port count matrix

**Referenced In:** BOE.md §5.3, §13; Detail.csv LineID 2502-01, 2502-02; Summary.md

---

## A-2503: Network Switch Equipment

**Assumption:** Network infrastructure requires:
- 1 core/distribution switch (24-48 ports, fiber uplinks, Layer 3 capable)
- 3-7 access switches (24-48 ports each, copper + fiber uplinks)
- Total switch capacity: 150-300 ports
- Managed switches with VLAN and QoS capability
- PoE capability TBD (may increase cost 20-40% if required)

**Why Needed:** Network architecture not defined; bandwidth and port requirements TBD
**Impacted WBS/CBS:** MAT (equipment), P (procurement)
**Cost Impact:** $95,000 CAD (17% of base estimate)
**Confidence:** LOW
**Resolution Path:** Define network architecture (topology, bandwidth, redundancy); obtain equipment specifications; acquire vendor quotes

**Referenced In:** BOE.md §5.3, §13; Detail.csv LineID 2503-01; Summary.md

---

## A-2504: Patch Panel Equipment

**Assumption:** Patch panel requirements include:
- 4-6 fiber patch panels (24-48 ports each, LC or SC connectors per DEL-25.02)
- 4-9 copper patch panels (24-48 ports each, Cat 6 or Cat 6A per DEL-25.02)
- 19-inch rack-mounted per EIA-310-D
- Total patch panel capacity to match cabling system port counts

**Why Needed:** Port counts and rack layouts TBD pending DEL-25.01 design
**Impacted WBS/CBS:** MAT (patch panels, connectors)
**Cost Impact:** $30,000 CAD (5% of base estimate)
**Confidence:** LOW
**Resolution Path:** Complete DEL-25.01 patch panel location drawings and rack elevations; coordinate with DEL-25.02 connector type selections

**Referenced In:** BOE.md §5.3, §13; Detail.csv LineID 2504-01; Summary.md

---

## A-2505: Cable Management and Infrastructure

**Assumption:** Cable management and supporting infrastructure includes:
- J-hooks, D-rings, Velcro wraps, cable managers for horizontal and vertical cable support
- Machine-printed labels per TIA-606 (cables, patch panels, outlets)
- Telecommunications bonding backbone (TBB) and grounding per TIA-607
- Cable pathway coordination with PKG-17 Electrical (shared trays/conduits)
- Firestopping at fire-rated penetrations

**Why Needed:** Installation details TBD pending DEL-25.01 pathway design
**Impacted WBS/CBS:** MAT (cable management materials), CD (installation labor)
**Cost Impact:** $15,000 CAD (3% of base estimate)
**Confidence:** MED
**Resolution Path:** Complete DEL-25.01 cable pathway design; coordinate with PKG-17 for shared pathways; define grounding and labeling requirements

**Referenced In:** BOE.md §5.3; Detail.csv LineID 2505-01; Summary.md

---

## A-2506: Engineering Design Effort

**Assumption:** Engineering design scope includes:
- DEL-25.01: 300-400 hours (drawings, layouts, coordination)
- DEL-25.02: 100-150 hours (specifications)
- DEL-25.03: 100-150 hours (data sheets, equipment selection)
- DEL-25.04: 100-100 hours (test procedures, record templates)
- Total: 600-800 hours at $125-150/hr blended rate

**Why Needed:** No project-specific engineering rate tables or labor budgets available
**Impacted WBS/CBS:** E (engineering)
**Cost Impact:** $75,000 CAD (13% of base estimate)
**Confidence:** MED
**Resolution Path:** Obtain project labor rate tables; define design deliverable scope and level of detail; acquire engineering budget from similar projects

**Referenced In:** BOE.md §5.3, §13; Detail.csv LineID 2506-01; Summary.md

---

## A-2507: Site Conditions and Access

**Assumption:** Installation productivity assumptions:
- Active marine terminal operations require coordination and security clearances
- Terminal operational interface may reduce productivity 10-15%
- Standard telecommunications installation productivity otherwise (e.g., 150-200 LM copper/day, 100-150 LM fiber/day)
- Access restrictions during operational hours may require some work after-hours

**Why Needed:** No site-specific productivity data or construction constraints defined
**Impacted WBS/CBS:** CD (installation labor), CI (supervision, coordination)
**Cost Impact:** Reflected in CD contingency (30%)
**Confidence:** MED
**Resolution Path:** Conduct site visit; coordinate with terminal operations; develop construction execution plan with access windows

**Referenced In:** BOE.md §6; Risk_Register.md R-2507; Summary.md

---

## A-2508: Labor Rates

**Assumption:** Vancouver/Lower Mainland BC labor rates:
- Telecommunications technician: $65-85/hr loaded
- Fiber optic splicer/technician: $75-95/hr loaded
- Low-voltage electrician: $70-90/hr loaded
- Project engineer: $125-150/hr loaded
- Superintendent: $110-140/hr loaded

**Why Needed:** No project labor rate tables available
**Impacted WBS/CBS:** E (engineering), CD (installation), CI (supervision)
**Cost Impact:** Embedded in allowances A-2501 through A-2506
**Confidence:** MED
**Resolution Path:** Obtain project labor rate agreements or local union rates; populate `_RateTables/Labor_Rates.csv`

**Referenced In:** BOE.md §6; Detail.csv notes

---

## A-2509: Fiber Cable Installation Unit Costs

**Assumption:** Fiber optic cable installation costs:
- Indoor fiber installation (conduit/tray): $18-28/LM
- Outdoor fiber installation (direct burial or duct): $35-55/LM
- Fiber splicing: $150-250 per splice
- Fiber termination: $50-75 per connector
- Testing (OTDR + insertion loss): $75-125 per link

**Why Needed:** No vendor quotes or rate tables for fiber installation
**Impacted WBS/CBS:** CD (installation), MAT (materials bundled with labor in allowance)
**Cost Impact:** Embedded in A-2501 ($120k fiber system allowance)
**Confidence:** LOW
**Resolution Path:** Obtain vendor quotes for fiber installation; separate materials from labor; populate `_RateTables/Fiber_Installation_Rates.csv`

**Referenced In:** Detail.csv LineID 2501-01; BOE.md §5.3

---

## A-2510: Copper Cable Installation Unit Costs

**Assumption:** Structured copper cabling installation costs:
- Horizontal copper cable installation (plenum/riser): $8-15/LM
- Outlet installation and termination: $75-125 per outlet
- Patch panel termination: $12-20 per port
- Testing (certification per TIA-568): $15-25 per link

**Why Needed:** No vendor quotes or rate tables for copper cabling installation
**Impacted WBS/CBS:** CD (installation), MAT (materials bundled with labor in allowance)
**Cost Impact:** Embedded in A-2502 ($85k copper system allowance)
**Confidence:** LOW
**Resolution Path:** Obtain vendor quotes for structured cabling installation; separate materials from labor; populate `_RateTables/Copper_Cabling_Rates.csv`

**Referenced In:** Detail.csv LineID 2502-01; BOE.md §5.3

---

## A-2511: Network Equipment Pricing

**Assumption:** Network switch pricing (budgetary, without vendor quotes):
- Core/distribution switch (48-port, L3, fiber uplinks): $12,000-18,000 each
- Access switch (24-port, L2+, copper + uplinks): $2,500-4,500 each
- Access switch (48-port, L2+, copper + uplinks): $4,000-7,000 each
- PoE premium (if required): +30-50%
- SFP/SFP+ transceivers: $300-800 each

**Why Needed:** No vendor quotes for network equipment
**Impacted WBS/CBS:** MAT (equipment)
**Cost Impact:** Embedded in A-2503 ($95k network equipment allowance)
**Confidence:** LOW
**Resolution Path:** Obtain budgetary quotes from network equipment vendors (Cisco, Juniper, HPE, Aruba, etc.); define equipment specifications

**Referenced In:** Detail.csv LineID 2503-01; BOE.md §5.3

---

## A-2512: Patch Panel and Connector Pricing

**Assumption:** Patch panel and connectivity pricing (budgetary):
- Fiber patch panel (24-port, LC or SC): $400-800 each
- Fiber patch panel (48-port, LC or SC): $700-1,300 each
- Copper patch panel (24-port, Cat 6/6A): $150-300 each
- Copper patch panel (48-port, Cat 6/6A): $250-500 each
- Fiber patch cords: $15-35 each
- Copper patch cords: $8-18 each

**Why Needed:** No vendor quotes for patch panels and connectivity
**Impacted WBS/CBS:** MAT (patch panels, connectors, patch cords)
**Cost Impact:** Embedded in A-2504 ($30k patch panel allowance)
**Confidence:** LOW
**Resolution Path:** Obtain budgetary quotes from structured cabling suppliers; define connector types per DEL-25.02 specification

**Referenced In:** Detail.csv LineID 2504-01; BOE.md §5.3

---

## A-2513: Cable Management Materials Pricing

**Assumption:** Cable management and infrastructure materials (budgetary):
- J-hooks, D-rings, cable supports: $3-8/LM cable
- Cable labels (machine-printed): $1.50-3 each
- Grounding and bonding materials (TBB, TBC): $2,000-4,000 lump sum
- Firestopping materials: $50-150 per penetration
- Miscellaneous hardware and fasteners: 5-10% of cable materials

**Why Needed:** No vendor quotes for cable management materials
**Impacted WBS/CBS:** MAT (cable management)
**Cost Impact:** Embedded in A-2505 ($15k cable management allowance)
**Confidence:** MED
**Resolution Path:** Obtain pricing from electrical/telecommunications distributors; quantify cable support requirements from DEL-25.01 drawings

**Referenced In:** Detail.csv LineID 2505-01; BOE.md §5.3

---

## A-2514: Terminal Coordination Constraints

**Assumption:** Fraser Surrey Terminal operational constraints:
- Security clearance required for all workers (5-10 days lead time)
- Escort required in some operational areas
- Work permits and isolation procedures for work near active cargo handling
- Potential after-hours or weekend work to minimize operational disruption (10-20% premium)

**Why Needed:** Site-specific construction constraints not defined
**Impacted WBS/CBS:** CD (productivity impact), CI (coordination overhead)
**Cost Impact:** Reflected in CD and CI contingency (30%)
**Confidence:** MED
**Resolution Path:** Coordinate with terminal operations; develop site-specific safety and access plan; define work hour restrictions

**Referenced In:** BOE.md §6; Risk_Register.md R-2507

---

## A-2515: Telecommunications Room Locations

**Assumption:** Telecommunications infrastructure layout:
- 1 main equipment room (ER) in control/admin building
- 2-4 telecommunications rooms (TRs) distributed across facility
- TR locations coordinated with PKG-21 building layouts and PKG-22 HVAC
- ER and TR environmental control (HVAC) provided by PKG-22
- Equipment power (120/208V, UPS backup) provided by PKG-17

**Why Needed:** Building layouts and equipment room locations TBD
**Impacted WBS/CBS:** MAT (cabling distances), CD (installation scope)
**Cost Impact:** Influences cable quantities in A-2501, A-2502
**Confidence:** LOW
**Resolution Path:** Complete PKG-21 building layouts; coordinate equipment room locations with PKG-22 and PKG-17; update DEL-25.01 design

**Referenced In:** BOE.md §5.2; Decision_Log.md D-2512

---

## A-2516: Integration with PKG-19 Control Systems

**Assumption:** Communications network integration with control systems:
- Isolated network segments for SCADA/control data (per DEC-05 and typical industrial practice)
- Firewall/gateway devices at integration points (cost allocated to PKG-19)
- Fiber/copper media converters or network switches dedicated to control system interfaces
- Integration scope limited to physical connectivity (Layer 1-2); control system network design by PKG-19

**Why Needed:** Integration requirements with PKG-19 not defined
**Impacted WBS/CBS:** MAT (interface equipment), COM (integration testing)
**Cost Impact:** Minimal (integration devices assumed in PKG-19); reflected in COM allowance
**Confidence:** MED
**Resolution Path:** Coordinate with PKG-19 Control Systems; define network integration architecture and interface points

**Referenced In:** BOE.md §2.2; DEL-25.01 Specification.md §Interface Requirements

---

## A-2517: Testing and Commissioning Scope

**Assumption:** Testing and commissioning activities include:
- Fiber testing: OTDR trace, insertion loss, polarity verification per TIA-568.3
- Copper testing: Certification testing per TIA-568.2-D (all channels)
- Network equipment commissioning: Configuration, VLAN setup, connectivity verification
- System integration testing with PKG-19 control systems
- Test records and documentation per DEL-25.04

**Why Needed:** Commissioning plan and test procedures TBD
**Impacted WBS/CBS:** COM (commissioning labor), MAT (test equipment rental if not owned)
**Cost Impact:** Embedded in COM parametric ($16k = 3% of CD+CI+MAT base)
**Confidence:** MED
**Resolution Path:** Develop DEL-25.04 test procedures; define acceptance criteria; coordinate commissioning with PKG-30

**Referenced In:** BOE.md §7; Detail.csv LineID 2517-01; Summary.md

---

## A-2518: Spare Capacity and Future Growth

**Assumption:** Spare capacity allowances for future expansion per OBJ-8:
- Fiber: 25-40% spare fibers in backbone cables
- Copper: 20-30% spare capacity in pathways and patch panels
- Switch ports: 20-30% unused ports for future devices
- No cost allocated for future equipment (spare capacity in initial installation only)

**Why Needed:** Future expansion requirements not defined
**Impacted WBS/CBS:** MAT (cable sizes, panel sizes)
**Cost Impact:** Embedded in equipment and cabling allowances (A-2501 through A-2504)
**Confidence:** MED
**Resolution Path:** Define future expansion plan with Employer; quantify future port requirements; update DEL-25.01 design basis

**Referenced In:** BOE.md §5.2; Decomposition Section 2 OBJ-8; DEL-25.01 Specification.md Performance Requirements

---

## Summary

**Total Assumptions:** 18
**Assumptions with Cost Impact > $50k:** 3 (A-2501, A-2502, A-2503)
**Assumptions with LOW Confidence:** 9
**Assumptions with MED Confidence:** 9
**Assumptions with HIGH Confidence:** 0

**Critical Path to Reduce Uncertainty:**
1. Complete network architecture design (resolves A-2503, A-2511, A-2515, A-2516, A-2518)
2. Complete building layouts and telecommunications room locations (resolves A-2502, A-2515)
3. Obtain vendor quotes for equipment and materials (resolves A-2503, A-2504, A-2509, A-2510, A-2511, A-2512, A-2513)
4. Define site access and construction constraints (resolves A-2507, A-2514)

---

**Assumptions Log Prepared By:** Estimating Agent
**Date:** 2026-01-29
**Status:** Complete
