# Datasheet: DEL-24.01 Security System Design Drawing Set

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-24.01 |
| Name | Security System Design Drawing Set |
| Package | PKG-24 Security Systems |
| Discipline | Specialty |
| Type | Drawing |
| Responsible | D&B Contractor |
| Status | INITIALIZED |
| Project | Canola Oil Transload Facility — Phase 1 |
| Location | Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC |

*Source: `_CONTEXT.md`; Decomposition Section 5 — PKG-24*

## Attributes

### Drawing Set Characteristics

| Attribute | Value |
|-----------|-------|
| Drawing Number Prefix | **TBD** — To be assigned per project numbering system |
| Sheet Count (Estimated) | **TBD** — Typical security system drawing sets: 5-15 sheets **ASSUMPTION** |
| Sheet Size | **TBD** — Typical: ANSI D (24"×36") or ISO A1 **ASSUMPTION** |
| Scale | **TBD** — Typical: 1:100 for layouts, NTS for details **ASSUMPTION** |
| CAD Standard | **TBD** — To be confirmed per project CAD manual |
| Revision | **TBD** — Initial issue for review |
| Classification | For Construction **ASSUMPTION** |
| Format | DWG and PDF **ASSUMPTION** |

*Source: Standard industry practice for security system drawing sets*

### Security System Coverage

| Coverage Area | Description |
|---------------|-------------|
| CCTV Monitoring Zones | **TBD** — Areas requiring CCTV surveillance per ER |
| Camera Count (Estimated) | **TBD** — Based on coverage analysis and ER requirements |
| Access Control Points | **TBD** — Gates, doors, and controlled entry points per ER |
| Integration Points | Terminal security network interface per DEC-05 **TBD** — specific connection details |

*Source: Decomposition Section 5 — PKG-24 scope; DEC-05 (Section 7)*

### Drawing Content

| Drawing Type | Purpose | Status |
|--------------|---------|--------|
| CCTV Layout | Overall site camera placement and coverage zones | **TBD** |
| Camera Coverage Drawings | Detailed coverage analysis per zone | **TBD** |
| Access Control Layout | Card readers, controllers, door hardware locations | **TBD** |
| System Architecture | Network topology and integration with Terminal systems | **TBD ASSUMPTION** |
| Mounting Details | Camera and equipment mounting details | **TBD ASSUMPTION** |

*Source: `_CONTEXT.md` — Anticipated Artifacts; typical security system drawing set composition*

## Conditions

### Operational Context

**Facility Type:** Canola oil transload facility (CSD grade canola oil)
- Permitted throughput: 1,000,000 MT per annum
- Storage capacity: 45,000 MT (3 × 15,000 MT tanks)
- Railcar capacity: 32 unloading stations on 2 tracks

*Source: Decomposition Section 1.1 — Key Parameters*

**Security System Scope:** CCTV, access control, integration with Terminal security network

*Source: Decomposition Section 5 — PKG-24 scope*

### Environmental Conditions

| Condition | Value |
|-----------|-------|
| Location | Fraser Surrey Terminal, Surrey, BC |
| Climate Zone | Pacific Maritime **ASSUMPTION** |
| Operating Temperature Range | **TBD** — Outdoor: -20°C to +40°C typical for BC coastal **ASSUMPTION** |
| Environmental Classification | Outdoor/Industrial **ASSUMPTION** |
| Hazardous Area Classification | **TBD** — To be determined per facility hazardous area study; likely Class I Div 2 near loading areas **ASSUMPTION** |
| Seismic Requirements | **TBD** — Per NBC 2020 for Surrey, BC location **ASSUMPTION** |
| Weather Protection | IP66 minimum for outdoor cameras **ASSUMPTION** |
| Vandal Resistance | IK10 for accessible locations **ASSUMPTION** |

*Source: Project location (Decomposition Section 1); typical security equipment requirements for industrial facilities*

### Design Life

| Parameter | Value |
|-----------|-------|
| Design Life | **TBD** — Typical: 15-20 years for security infrastructure **ASSUMPTION** |
| Equipment Refresh Cycle | **TBD** — Typical: 5-7 years for cameras/electronics **ASSUMPTION** |
| Network Infrastructure Life | **TBD** — 20+ years for conduit/cable pathways **ASSUMPTION** |

## Construction

### System Components (Typical)

**CCTV System:**
- Fixed cameras: **TBD** — count and locations per coverage analysis
- PTZ cameras: **TBD** — for key monitoring points **ASSUMPTION**
- Network video recorder (NVR): **TBD** — capacity and redundancy requirements
- Video management system (VMS): **TBD** — software platform
- Network infrastructure: fiber/copper backbone **TBD**

**Access Control System:**
- Card readers: **TBD** — count and locations
- Access control panels: **TBD** — distributed or centralized architecture
- Electronic locks/strikes: **TBD** — per door schedule
- Access control software: **TBD** — platform and integration requirements

*Source: Typical security system components; specifics TBD per ER requirements*

### Integration Requirements

| Interface | Description |
|-----------|-------------|
| Terminal Security Network | Integration with existing DP World Fraser Surrey Terminal security infrastructure per DEC-05 |
| Network Segregation | **TBD** — VLAN separation, firewall requirements |
| Central Monitoring | **TBD** — Connection to Terminal security operations center |
| Protocols | **TBD** — ONVIF, OSDP, or proprietary protocols |

*Source: DEC-05 (Decomposition Section 7) — Terminal network interfaces treated as multiple distinct systems*

### Materials and Standards

| Material/Standard | Application |
|-------------------|-------------|
| Conduit and Cable | **TBD** — CSA-approved for Canadian installation **ASSUMPTION** |
| Camera Housings | Corrosion-resistant for marine/industrial environment **ASSUMPTION** |
| Mounting Hardware | Stainless steel for coastal environment **ASSUMPTION** |
| Network Cables | Cat6A minimum for IP cameras **ASSUMPTION** |
| Fiber Backbone | Single-mode for long runs **ASSUMPTION** |

### Installation Requirements

| Requirement | Description |
|-------------|-------------|
| Construction Method | **TBD** — Phased installation to minimize Terminal disruption per OBJ-5 |
| Cable Routing | Underground/overhead routing **TBD** — coordinate with PKG-03, PKG-17 |
| Commissioning | Integration testing with Terminal systems **TBD** |
| Training | Terminal security staff training on new systems **TBD** — likely covered under PKG-35 |

*Source: OBJ-5 (Decomposition Section 2) — Terminal Continuity objective*

## References

### Primary References

- Decomposition document: `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` — Sections 1, 2, 5 (PKG-24), 7 (DEC-05)
- `_CONTEXT.md` — Deliverable identity and anticipated artifacts
- `_REFERENCES.md` — No specific references identified yet; ER volumes expected

### Applicable Standards (ASSUMPTION — to be confirmed)

- **TBD** — CSA standards for security systems in Canada
- **TBD** — NFPA 72 (if integrated with fire alarm system)
- **TBD** — IEC 62676 series (Video surveillance systems)
- **TBD** — ONVIF (Open Network Video Interface Forum) profiles
- **TBD** — Employer's Requirements Volume 2 Parts 1-3 (location TBD)
- National Building Code of Canada 2020 — seismic/structural requirements **ASSUMPTION**
- CSA C22.1 (Canadian Electrical Code) — electrical installation requirements **ASSUMPTION**

### Cross-References

- See `_DEPENDENCIES.md` — NOT_TRACKED (dependencies coordinated externally)
- Interface packages: PKG-03 (Underground Utilities), PKG-17 (Electrical Power), PKG-25 (Communications & IT)
- Testing/Commissioning: PKG-29 (Testing), PKG-30 (Commissioning)
- Training: PKG-35 (Training & Handover)

---

*Document status: Enriched draft — Pass 1*
*Enrichment date: 2026-01-28*
*Next review: WORKING_ITEMS session for detailed requirements development*
