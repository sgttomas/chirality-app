# Assumptions Log — PKG-24 Security Systems Estimate

**Snapshot ID:** EST_PKG24_DRAFT_2026-01-28_0030
**Date:** 2026-01-28

This log documents assumptions and allowances used in the PKG-24 Security Systems estimate where project-specific data was not available.

---

## A-001: Engineering Design Allowance

**Statement:** Engineering design hours and blended rate for security systems design
**Reason:** No engineering labor rates or hours available in workspace
**Impacted WBS:** DEL-24.01, DEL-24.02, DEL-24.03, DEL-24.04
**Impacted CBS:** E
**Cost Impact:** $123,000 total (15% of base)
- DEL-24.01 drawing set: $48,000 (600-800 hours)
- DEL-24.02 specification: $32,000 (400-500 hours)
- DEL-24.03 datasheet support: $18,000 (200-250 hours)
- DEL-24.04 test support: $25,000 (300-350 hours)
**Basis:** Typical specialty engineering hours @ $140-175/hr blended rate (senior designer + CAD technician)
**Confidence:** LOW
**Resolution Path:** Obtain project engineering labor rates and hour estimates from design team

---

## A-002: CCTV Fixed Camera Quantity and Unit Cost

**Statement:** 18 fixed IP cameras @ $3,500/unit average ($2,500-4,500 range)
**Reason:** Camera count and locations TBD pending DEL-24.01 coverage design; unit cost from typical industrial IP camera pricing
**Impacted WBS:** DEL-24.01, DEL-24.03
**Impacted CBS:** MAT
**Cost Impact:** $63,000 (8% of base)
**Basis:**
- Quantity: Engineering judgment based on facility scope (tank farm, railcar unloading 32 stations, marine loading berth, perimeter, gates, buildings)
- Unit cost: Typical pricing for 2-4MP outdoor IP66/IP67 industrial cameras with IR illumination and marine-grade housings
**Confidence:** LOW
**Resolution Path:** Complete DEL-24.01 coverage analysis; obtain budgetary quotes from security system integrators

---

## A-003: CCTV PTZ Camera Quantity and Unit Cost

**Statement:** 3 PTZ IP cameras @ $12,000/unit average ($9,000-15,000 range)
**Reason:** PTZ count TBD pending coverage design; unit cost from typical industrial PTZ camera pricing
**Impacted WBS:** DEL-24.01, DEL-24.03
**Impacted CBS:** MAT
**Cost Impact:** $36,000 (4% of base)
**Basis:**
- Quantity: Engineering judgment (2-5 PTZ typical for key monitoring areas with flexible coverage needs)
- Unit cost: Typical pricing for 2-4MP PTZ with 30x optical zoom, outdoor IP66/IP67, heavy-duty pan/tilt, marine-grade
**Confidence:** LOW
**Resolution Path:** Complete DEL-24.01 coverage design specifying PTZ vs fixed camera strategy

---

## A-004: NVR System Quantity and Unit Cost

**Statement:** 2 NVR units @ $15,000/unit average ($12,000-18,000 range)
**Reason:** Redundant NVR configuration assumption; unit cost from typical NVR pricing
**Impacted WBS:** DEL-24.03
**Impacted CBS:** MAT
**Cost Impact:** $30,000 (4% of base)
**Basis:**
- Quantity: Redundant dual NVR configuration for 32-64 channels with 30-90 day retention @ 4MP
- Unit cost: Typical rack-mount enterprise NVR with RAID storage
**Confidence:** LOW
**Resolution Path:** Complete DEL-24.02 specification defining NVR capacity, retention period, redundancy requirements

---

## A-005: VMS Software and Licensing

**Statement:** VMS software platform with 5-10 user licenses @ $25,000
**Reason:** VMS requirements TBD; allowance based on typical industrial VMS deployment
**Impacted WBS:** DEL-24.03
**Impacted CBS:** MAT
**Cost Impact:** $25,000 (3% of base)
**Basis:** ONVIF-compliant VMS with alarm management, integration APIs, Terminal interface capability per DEC-05; typical 5-10 concurrent user licenses
**Confidence:** LOW
**Resolution Path:** Obtain Terminal VMS compatibility requirements; obtain vendor pricing for VMS software and licensing

---

## A-006: Access Control Card Reader Quantity and Unit Cost

**Statement:** 12 card readers @ $1,200/unit average ($800-1,500 range)
**Reason:** Reader count TBD pending access control layout; unit cost from typical reader pricing
**Impacted WBS:** DEL-24.01, DEL-24.03
**Impacted CBS:** MAT
**Cost Impact:** $14,400 (2% of base)
**Basis:**
- Quantity: Engineering judgment (site gates, building entrances, restricted areas); assume 12 controlled doors/gates
- Unit cost: Typical proximity or smart card reader (125kHz/13.56MHz) with IP65 outdoor rating, IK08 vandal resistance
**Confidence:** LOW
**Resolution Path:** Complete DEL-24.01 access control layout; obtain budgetary quotes

---

## A-007: Access Control Controller Quantity and Unit Cost

**Statement:** 2 access control panels @ $8,000/unit average ($6,000-10,000 range)
**Reason:** Controller architecture TBD; unit cost from typical panel pricing
**Impacted WBS:** DEL-24.03
**Impacted CBS:** MAT
**Cost Impact:** $16,000 (2% of base)
**Basis:**
- Quantity: Distributed network-based architecture; 2 panels @ 8-16 doors per panel for 12 total doors
- Unit cost: Typical TCP/IP network controller with battery backup, fail-safe/fail-secure configurable
**Confidence:** LOW
**Resolution Path:** Complete DEL-24.02 specification defining controller architecture and capacity

---

## A-008: Access Control Software and Licensing

**Statement:** Access control management software with 3-5 user licenses @ $18,000
**Reason:** Software requirements TBD; allowance based on typical industrial access control deployment
**Impacted WBS:** DEL-24.03
**Impacted CBS:** MAT
**Cost Impact:** $18,000 (2% of base)
**Basis:** Cardholder management, access level administration, audit trails, Terminal integration per DEC-05, reporting; typical 3-5 concurrent user licenses
**Confidence:** LOW
**Resolution Path:** Obtain Terminal access control compatibility requirements; obtain vendor pricing

---

## A-009: Door Hardware Quantity and Unit Cost

**Statement:**
- Electric strikes or magnetic locks: 12 units @ $650/unit average ($450-850 range) = $7,800
- REX devices and door position switches: 12 sets @ $180/set average ($120-240 range) = $2,160

**Reason:** Door hardware count matches controlled door count; unit costs from typical hardware pricing
**Impacted WBS:** DEL-24.03
**Impacted CBS:** MAT
**Cost Impact:** $9,960 total (1% of base)
**Basis:**
- Quantity: 12 controlled doors/gates (same as reader count A-006)
- Unit cost: Stainless steel fail-safe/fail-secure locks; REX motion sensors or buttons; magnetic door position switches
**Confidence:** LOW
**Resolution Path:** Complete DEL-24.01 door hardware schedule; confirm fail-safe/fail-secure requirements with PKG-23 fire protection

---

## A-010: Network Switch and Fiber Equipment Quantity and Unit Cost

**Statement:** 4 managed PoE switches with accessories @ $4,500/unit average ($3,500-5,500 range)
**Reason:** Network architecture TBD; unit cost from typical PoE switch pricing
**Impacted WBS:** DEL-24.03
**Impacted CBS:** MAT
**Cost Impact:** $18,000 (2% of base)
**Basis:**
- Quantity: 4 switches (24-48 port) distributed for 21 cameras + 12 readers + network redundancy
- Unit cost: Managed PoE+ switches with fiber SFP modules, patch panels
**Confidence:** LOW
**Resolution Path:** Complete DEL-24.01 network topology; coordinate with PKG-25 communications for backbone integration

---

## A-011: UPS Quantity and Unit Cost

**Statement:** 3 UPS units @ $2,800/unit average ($2,000-3,500 range)
**Reason:** UPS locations TBD; unit cost from typical UPS pricing
**Impacted WBS:** DEL-24.03
**Impacted CBS:** MAT
**Cost Impact:** $8,400 (1% of base)
**Basis:**
- Quantity: 3 units (equipment rooms and critical controllers); 4-8 hour battery backup
- Unit cost: Rack-mount or standalone UPS with battery
**Confidence:** LOW
**Resolution Path:** Complete DEL-24.02 specification defining UPS capacity and backup duration requirements

---

## A-012: Cabling and Conduit Materials Bulk Allowance

**Statement:** Bulk materials allowance for cabling and conduit @ $95,000
**Reason:** Cable routing and lengths TBD pending detailed design
**Impacted WBS:** DEL-24.01, DEL-24.03
**Impacted CBS:** MAT
**Cost Impact:** $95,000 (11% of base)
**Basis:**
- Cat6A cabling: 2000-3000m (21 cameras + 12 readers + network drops)
- Single-mode fiber: 500-800m (backbone)
- Outdoor-rated conduit and fittings
- Cable trays, pull boxes, labels
- Typical bulk cabling materials cost for mid-size facility
**Confidence:** LOW
**Resolution Path:** Complete DEL-24.01 cable routing drawings coordinated with PKG-03, PKG-17, PKG-25

---

## A-013: Camera Pole Quantity and Unit Cost

**Statement:** 8 camera poles @ $3,200/unit average ($2,500-4,000 range) including foundation
**Reason:** Pole count TBD based on mounting location availability; unit cost from typical pole installation pricing
**Impacted WBS:** DEL-24.01, DEL-24.03
**Impacted CBS:** MAT (pole materials included in L-017)
**Cost Impact:** $25,600 (3% of base)
**Basis:**
- Quantity: 8 dedicated poles (4-8m height) for areas without building/structure mounting availability
- Unit cost: Pole, foundation, grounding, installation
- Assumption: ~38% of cameras (8 of 21) require dedicated poles; remainder mount on buildings/structures
**Confidence:** LOW
**Resolution Path:** Complete DEL-24.01 mounting location survey and camera layout

---

## A-014: CCTV Camera Installation Labor

**Statement:** Camera installation labor @ 6-12 hours per camera, $120-150/hr loaded labor rate
**Reason:** Installation hours and labor rates TBD
**Impacted WBS:** DEL-24.04
**Impacted CBS:** CD
**Cost Impact:** $17,850 for 21 cameras (2% of base)
**Basis:** Typical labor hours for camera mounting, cable pulling/termination, aiming, configuration; loaded labor rate for security systems technician in BC Lower Mainland
**Confidence:** LOW
**Resolution Path:** Obtain contractor labor rates; develop installation productivity estimates

---

## A-015: Access Control Equipment Installation Labor

**Statement:** Access control installation labor @ 8-14 hours per door, $120-150/hr loaded labor rate
**Reason:** Installation hours and labor rates TBD
**Impacted WBS:** DEL-24.04
**Impacted CBS:** CD
**Cost Impact:** $13,200 for 12 doors (2% of base)
**Basis:** Typical labor hours for reader installation, controller installation, door hardware installation, cable pulling/termination, configuration; loaded labor rate for security systems technician
**Confidence:** LOW
**Resolution Path:** Obtain contractor labor rates; develop installation productivity estimates

---

## A-016: Network and Central Equipment Installation Labor

**Statement:** Network/central equipment installation and configuration @ 250-350 hours, $120-150/hr loaded labor rate
**Reason:** Installation hours and labor rates TBD
**Impacted WBS:** DEL-24.04
**Impacted CBS:** CD
**Cost Impact:** $42,000 (5% of base)
**Basis:** NVR/VMS server installation and configuration, network switch installation and configuration, fiber terminations, rack installation, UPS installation; loaded labor rate for security systems technician
**Confidence:** LOW
**Resolution Path:** Obtain contractor labor rates; develop detailed installation plan

---

## A-017: Underground Conduit Installation

**Statement:** Underground conduit installation (trenching or boring) @ $95,000 for 400-700 LM
**Reason:** Conduit routing and lengths TBD; must coordinate with PKG-03 underground utilities
**Impacted WBS:** DEL-24.01, DEL-24.04
**Impacted CBS:** CD
**Cost Impact:** $95,000 (11% of base)
**Basis:**
- Typical underground conduit runs for security systems in industrial facility
- Trenching or boring labor + backfill
- Coordinate with PKG-03 for shared trenches where possible
- Unit cost: $135-240/LM typical for security system conduit installation
**Confidence:** LOW
**Resolution Path:** Complete DEL-24.01 cable routing; coordinate with PKG-03 underground utilities design

---

## A-018: Camera Pole Foundation and Installation Labor

**Statement:** Camera pole foundation and erection labor @ 10-16 hours per pole, $120-150/hr loaded labor rate, plus concrete materials labor
**Reason:** Installation hours and labor rates TBD
**Impacted WBS:** DEL-24.04
**Impacted CBS:** CD
**Cost Impact:** $11,200 for 8 poles (1% of base)
**Basis:** Concrete foundation excavation, formwork, rebar, concrete placement, curing; pole erection and grounding; loaded labor rate
**Confidence:** LOW
**Resolution Path:** Obtain contractor labor rates and concrete subcontractor pricing; coordinate with PKG-05 for foundation design

---

## A-019: System Testing and Commissioning Labor

**Statement:** Testing and commissioning labor @ 400-550 hours, $120-150/hr loaded labor rate
**Reason:** Testing hours and labor rates TBD
**Impacted WBS:** DEL-24.04
**Impacted CBS:** CD
**Cost Impact:** $65,000 (8% of base)
**Basis:**
- Cable testing (continuity, termination verification)
- Camera functional testing (all 21 cameras)
- Access control functional testing (all 12 doors)
- Coverage verification (field-of-view, image quality)
- Integration testing (CCTV + access control, Terminal integration per DEC-05)
- SAT support and commissioning
- Loaded labor rate for security systems technician and commissioning engineer
**Confidence:** LOW
**Resolution Path:** Develop detailed testing and commissioning plan per PKG-29 and PKG-30; obtain labor rates

---

## A-020: BC Lower Mainland Loaded Labor Rate

**Statement:** Loaded labor rate for security systems technicians @ $120-150/hr
**Reason:** No project labor rates available
**Impacted WBS:** DEL-24.04 (all construction directs labor)
**Impacted CBS:** CD
**Cost Impact:** Affects all CD labor line items (L-018 through L-023)
**Basis:** Typical prevailing wage or union rates for security systems technicians in Vancouver/Lower Mainland BC area, including benefits, burden, small tools, overhead, profit
**Confidence:** LOW
**Resolution Path:** Obtain project labor rate tables or contractor pricing

---

## A-021: Terminal Integration Testing Labor Allocation

**Statement:** Terminal integration testing labor included in commissioning labor allowance (A-019)
**Reason:** Terminal integration scope and duration TBD
**Impacted WBS:** DEL-24.04
**Impacted CBS:** CD (labor), COM (services)
**Cost Impact:** Included in $65,000 commissioning labor (A-019) and $19,000 commissioning services factor
**Basis:**
- CCTV integration: Video stream testing, VMS interface verification, alarm integration
- Access control integration: Credential synchronization testing, event reporting verification
- Network integration: VLAN configuration, firewall testing, bandwidth verification
- Terminal coordination and acceptance per DEC-05
**Confidence:** LOW
**Resolution Path:** Obtain Terminal integration requirements; develop detailed integration test plan; coordinate with Terminal IT/security operations

---

## A-022: Coastal Marine Environment Equipment Ratings

**Statement:** Equipment environmental ratings for Fraser Surrey Terminal coastal environment:
- Outdoor equipment: IP66/IP67 minimum (dust-tight, protection against heavy seas)
- Vandal resistance: IK10 for accessible locations
- Operating temperature: -20°C to +40°C
- Corrosion resistance: Marine-grade materials, stainless steel, powder-coated aluminum

**Reason:** Environmental conditions at coastal marine terminal
**Impacted WBS:** DEL-24.02, DEL-24.03
**Impacted CBS:** MAT (affects equipment specifications and unit costs)
**Cost Impact:** Premium of 15-30% over standard industrial equipment (included in unit cost allowances A-002 through A-011)
**Basis:** Fraser Surrey Terminal location (coastal marine environment); salt spray, high humidity, UV exposure
**Confidence:** MEDIUM
**Resolution Path:** Confirm environmental specifications with Employer; verify with equipment manufacturers

---

## A-023: Terminal Integration Scope per DEC-05

**Statement:** Terminal security network integration treated as separate CCTV and access control interfaces (not unified system)
**Reason:** DEC-05 decision in decomposition
**Impacted WBS:** DEL-24.01, DEL-24.02, DEL-24.03, DEL-24.04
**Impacted CBS:** E (design), MAT (software), CD (installation), COM (commissioning)
**Cost Impact:**
- VMS software includes Terminal CCTV integration capability (A-005)
- Access control software includes Terminal access control integration capability (A-008)
- Network equipment sized for segregated VLANs (A-010)
- Commissioning includes separate integration testing (A-021)
**Basis:** Decomposition Section 7, DEC-05: "Terminal network interfaces treated as multiple distinct systems"
**Confidence:** MEDIUM (decision is explicit; implementation details TBD)
**Resolution Path:** Obtain Terminal security integration specification (protocols, credentials, network topology, VLANs, firewall rules)

---

**Assumptions Log Complete**
**Total Assumptions:** 23
**Prepared By:** Estimating Agent
**Date:** 2026-01-28

---

## Summary of High-Impact Assumptions (>5% of Base)

| Assumption ID | Description | Cost Impact | % of Base |
|---------------|-------------|-------------|-----------|
| A-001 | Engineering design hours and rates | $123,000 | 15% |
| A-012 | Cabling and conduit materials bulk allowance | $95,000 | 11% |
| A-017 | Underground conduit installation labor | $95,000 | 11% |
| A-002 | CCTV fixed cameras (18 units) | $63,000 | 8% |
| A-019 | Testing and commissioning labor | $65,000 | 8% |

**Total High-Impact Assumptions:** $441,000 (53% of base estimate)

**Validation Priority:** Focus on obtaining design quantities (camera count, cable routing), vendor quotes (cameras, NVR, access control), and installation labor rates to reduce uncertainty in these high-impact areas.
