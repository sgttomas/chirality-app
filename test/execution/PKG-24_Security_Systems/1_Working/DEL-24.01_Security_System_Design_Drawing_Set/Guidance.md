# Guidance: DEL-24.01 Security System Design Drawing Set

## Purpose

This guidance document supports the development of the **Security System Design Drawing Set** for **PKG-24 Security Systems** at the Canola Oil Transload Facility.

**Deliverable objective:** Defines the design arrangement and details for security system per ER requirements, providing comprehensive CCTV and access control coverage for safe and secure facility operations.

*Source: `_CONTEXT.md`; Decomposition Section 5 — PKG-24*

**Classification:** Drawing deliverable under Specialty discipline, to be produced by D&B Contractor

**Project context:** This drawing set supports OBJ-1 (Safe & Reliable Operation) and OBJ-6 (Regulatory Compliance) by defining security infrastructure for a 1,000,000 MT/annum canola oil transload facility with 32 railcar unloading stations and marine loading capability.

*Source: Decomposition Sections 1.1 and 2 — Key Parameters and Objectives*

## Principles

### Security System Design Philosophy

#### Defense in Depth (ASSUMPTION — typical security design principle)
Security system design should employ multiple layers of protection:
1. **Perimeter protection** — Site boundary monitoring and access control
2. **Asset protection** — Critical equipment and process area surveillance
3. **Process monitoring** — Observation of operational activities for safety and security
4. **Integration** — Coordination with Terminal-wide security operations

*Source: Standard security design practice; specific requirements TBD per ER*

#### Risk-Based Design
- **Higher risk areas require higher coverage quality:**
  - Custody transfer points (metering, loading arms)
  - Hazardous process areas (tank farm, unloading stations)
  - Public-facing perimeter and access points
  - High-value asset locations

- **Coverage design should consider:**
  - Threat scenarios relevant to industrial transload facility **TBD** — per security risk assessment
  - Operational monitoring needs (safety observation, process verification)
  - Emergency response support (incident investigation, alarm verification)

*Source: ASSUMPTION — risk-based security design approach; specific risk assessment TBD*

#### Operational Integration
- Design shall support both security monitoring and operational needs:
  - Safety observation of remote/hazardous work areas
  - Process verification (loading operations, tank gauging)
  - Incident investigation and documentation
  - Integration with existing Terminal security operations per DEC-05

*Source: DEC-05 (Decomposition Section 7) — Terminal network interfaces; OBJ-1 (Safe & Reliable Operation)*

### Applicable Standards Context

**Security Industry Standards (ASSUMPTION — typical for IP-based security systems):**
- IEC 62676 series provides framework for video surveillance system design
- ONVIF ensures interoperability of IP cameras and VMS platforms
- OSDP (Open Supervised Device Protocol) enables secure access control communications

**Canadian Regulatory Context:**
- Privacy legislation (PIPEDA) governs collection and use of video surveillance **ASSUMPTION**
- Workplace safety regulations may require monitoring of hazardous work areas **ASSUMPTION**
- Port/transportation security requirements may apply **TBD**

*Source: Standard Canadian security system regulatory context; specifics TBD per ER and jurisdiction*

### Terminal Integration Considerations (DEC-05)

**Separate System Interfaces:**
Per DEC-05, Terminal network interfaces are treated as multiple distinct systems:
- CCTV system — separate integration point with Terminal video management
- Access control system — separate integration with Terminal access control platform
- Communications network — separate data network integration (PKG-25)

**Integration Design Principles:**
- Maintain clear system boundaries and interface points
- Document integration architecture and data flow
- Coordinate with Terminal IT/security operations for connection requirements
- Design for network segregation and security (VLANs, firewalls) **TBD**

*Source: DEC-05 (Decomposition Section 7)*

## Considerations

### Factors to Consider During Development

#### 1. Coverage Strategy

**CCTV Coverage Zones:**
- **Continuous monitoring areas:** Tank farm, railcar unloading, marine loading berth
- **Access monitoring:** Site gates, building entrances, restricted area boundaries
- **Safety monitoring:** Remote work areas, fall hazards, confined space entry points **TBD**
- **Operational monitoring:** Process equipment, custody transfer points
- **Perimeter monitoring:** Site boundary, fence line, public interfaces

*Source: Typical transload facility security coverage requirements; specifics TBD per ER*

**Coverage Quality Levels (ASSUMPTION):**
- **Identification level:** Facial recognition capability at access control points
- **Recognition level:** General person identification in restricted areas
- **Detection level:** Activity/movement detection at perimeter
- **Monitoring level:** General situational awareness and process observation

#### 2. Camera Placement Considerations

**Mounting Location Selection:**
- Building walls and roof edges — coordinate structural capacity with PKG-05, PKG-06, PKG-21
- Dedicated poles — coordinate foundation design with PKG-05, civil works
- Existing infrastructure — verify load capacity and condition
- Height selection — balance coverage area vs. image quality (facial detail at distance)

**Environmental Factors:**
- Sun glare and backlighting (orient cameras to avoid direct sun exposure)
- Weather (rain, fog, snow) impact on image quality — specify appropriate camera ratings
- Coastal/marine environment — corrosion resistance, salt spray protection
- Lighting coordination — work with PKG-18 to ensure adequate illumination for night coverage

**Installation Constraints:**
- Hazardous area classification — camera/equipment ratings, conduit sealing requirements **TBD**
- Construction phasing — maintain Terminal operations per OBJ-5 (Terminal Continuity)
- Cable routing — underground vs. overhead, coordination with PKG-03 and PKG-17
- Maintenance access — consider serviceability and future lens cleaning

*Source: Standard CCTV design considerations; OBJ-5 (Decomposition Section 2)*

#### 3. Access Control Strategy

**Access Control Zoning (ASSUMPTION — typical approach):**
- Public/unrestricted — site perimeter, parking areas
- Controlled access — site gates, building entrances
- Restricted access — process areas, tank farm, loading operations
- High security — equipment rooms, custody transfer/metering areas

**Door Hardware Coordination:**
- Fail-safe vs. fail-secure designation per life safety codes (coordinate with PKG-23 Fire Protection)
- Emergency egress requirements — free egress without card/credential
- Delayed egress where appropriate (high security with life safety compliance)
- Integration with building design — coordinate with PKG-21/PKG-22

#### 4. Network and Integration Architecture

**Network Design Considerations:**
- Bandwidth requirements — estimate based on camera count, resolution, frame rate
- Network segregation — separate VLANs for CCTV, access control, general IT
- Redundancy and failover — critical path redundancy **TBD**
- Terminal network integration — connection topology, firewall rules, security policies **TBD**

**System Integration:**
- Video management system (VMS) selection and licensing
- Access control platform selection and licensing
- Integration with Terminal existing systems — protocol compatibility, API availability
- Future expansion — design for Phase 2 growth per OBJ-8 (Future Expandability)

*Source: OBJ-8 (Decomposition Section 2) — Future Expandability*

#### 5. Regulatory and Compliance

**Privacy Compliance (ASSUMPTION):**
- Signage indicating video surveillance in use
- Data retention policies and storage duration limits
- Access to footage restricted to authorized personnel
- No surveillance in private areas (washrooms, changing rooms)

**Safety and Security Balance:**
- Security monitoring supports safety objectives (OBJ-1)
- Design shall not impede emergency egress or evacuation
- Integration with fire alarm and emergency communication systems **TBD**

*Source: OBJ-1 (Decomposition Section 2); standard privacy and safety practices*

#### 6. Drawing Production Specific

**CAD Standards and Layering:**
- Follow project CAD manual **TBD** — layer naming, line types, symbols
- Use consistent symbology for camera types, coverage zones, access control devices
- Coordinate base drawings with civil/structural/architectural disciplines
- Maintain drawing register and cross-references

**Coverage Analysis Methodology:**
- Use camera coverage calculation software **TBD** — specify tool and methodology
- Document assumptions (camera specs, mounting height, lens selection)
- Verify coverage against ER requirements **TBD**
- Identify and resolve coverage gaps or overlaps

**Interdisciplinary Coordination:**
- Attend interdisciplinary check (IDC) meetings
- Issue coordination drawings early for input from structural, electrical, civil
- Track and resolve IDC comments in coordination log
- Issue final drawings with all disciplines coordinated

## Trade-offs

### Competing Concerns to Evaluate

#### 1. Coverage Density vs. System Cost
**Trade-off:** More cameras provide better coverage and redundancy but increase capital cost and ongoing maintenance.

**Considerations:**
- Focus high-density coverage on high-risk/high-value areas
- Use PTZ cameras for flexible coverage of large areas (but consider operational manning)
- Optimize fixed camera placement to minimize count while meeting coverage requirements
- Consider future expansion — install conduit/infrastructure for future cameras at lower cost

*Decision approach: Risk-based prioritization; document coverage design rationale*

#### 2. Image Quality vs. Storage/Bandwidth
**Trade-off:** Higher resolution provides better forensic capability but requires more network bandwidth and storage capacity.

**Considerations:**
- Match resolution to coverage purpose (identification vs. detection vs. monitoring)
- Use variable bit rate and smart compression to optimize storage
- Size NVR storage based on retention policy and camera specifications
- Balance frame rate requirements (higher for critical areas, lower for perimeter)

*Decision approach: Specify resolution based on coverage zone requirements; document storage calculations*

#### 3. Standalone vs. Integrated Systems
**Trade-off:** Fully integrated systems provide unified interface but may increase complexity and vendor lock-in.

**Considerations:**
- Terminal integration requirements per DEC-05 — separate but coordinated systems
- Open protocol standards (ONVIF, OSDP) vs. proprietary integration
- Future flexibility and vendor options vs. optimized single-vendor solution
- Maintenance and support implications — single vendor vs. best-of-breed components

*Decision approach: Coordinate with Employer/Terminal IT to determine integration strategy*

*Source: DEC-05 (Decomposition Section 7) — Terminal interfaces as separate systems*

#### 4. Construction Phasing vs. Final Coverage
**Trade-off:** Phased installation minimizes Terminal disruption (OBJ-5) but may leave temporary coverage gaps.

**Considerations:**
- Sequence installation to maintain security coverage during construction
- Temporary cameras or extended coverage from existing Terminal systems **TBD**
- Coordinate with Employer on acceptable coverage during construction phases
- Plan commissioning sequence to minimize operational impact

*Decision approach: Develop phasing plan in coordination with Employer; document in installation drawings*

*Source: OBJ-5 (Decomposition Section 2) — Terminal Continuity*

#### 5. Design Conservatism vs. Material Efficiency
**Trade-off:** Over-designing system provides safety margin but increases cost and may complicate future changes.

**Considerations:**
- Design for known requirements plus reasonable expansion capability (OBJ-8)
- Avoid over-specification of equipment ratings beyond actual environmental conditions
- Balance redundancy requirements with cost and complexity
- Design for maintainability and future technology refresh cycles

*Decision approach: Design to meet requirements with ~20% expansion margin; document assumptions*

*Source: OBJ-8 (Decomposition Section 2) — Future Expandability; OBJ-9 — Lifecycle Cost Optimization*

#### 6. Schedule Compression vs. Quality
**Trade-off:** Accelerated drawing production may reduce coordination and review quality.

**Considerations:**
- Adequate time for interdisciplinary coordination (IDC process)
- Sufficient review cycles for Employer input and Terminal operations feedback
- Alignment with overall project schedule and critical path activities
- Risk of rework if insufficient coordination early in design

*Decision approach: Follow structured design review process; front-load coordination activities*

## Examples

### Reference Examples and Precedents

**Project-Specific References:**
- Employer's Requirements Volume 2 **TBD** — expected to provide:
  - Security coverage requirements and performance criteria
  - Integration requirements with Terminal systems
  - Equipment standards and approved manufacturers
  - Drawing submittal requirements and format

*Source: Decomposition Section 3 — Reference Documents*

**Industry Precedents (ASSUMPTION — typical references):**
- **TBD** — Similar transload/terminal facility security designs
- **TBD** — Bulk liquid storage facility security case studies
- **TBD** — Industrial CCTV design guidelines (IEC 62676-4, Operational requirements)
- **TBD** — Access control best practices for industrial facilities

**Terminal Existing Systems:**
- Review existing DP World Fraser Surrey Terminal security infrastructure
- Understand current monitoring/control center operations and procedures
- Identify integration points and standards for new Phase 1 facility
- **TBD** — Existing system documentation and as-built drawings

### Anticipated Artifacts — Content Examples

**1. CCTV Layout (Site Plan Drawing)**
- Site boundary and property lines
- Building footprints and major structures
- Camera locations with unique identifiers (CAM-01, CAM-02, etc.)
- Camera coverage zones shown as colored overlays or hatch patterns
- Cable routing — conduit/cable tray paths from cameras to equipment room
- Legend showing camera types (fixed, PTZ, etc.)
- Reference to coverage analysis drawings

**2. Camera Coverage Drawings (Zone Detail Drawings)**
- Field-of-view diagrams for each camera
- Coverage overlap areas
- Identification zones (where facial recognition is required)
- Detection zones (perimeter monitoring)
- Blind spots or coverage gaps with explanation/mitigation
- Notes on camera specifications (resolution, lens, mounting height)
- Coordination notes for lighting (reference to PKG-18 drawings)

**3. Access Control Layout (Floor Plan/Site Plan Drawings)**
- Building floor plans or site plan showing controlled doors/gates
- Card reader locations with device identifiers (ACR-01, etc.)
- Access control panel/controller locations
- Door hardware (electric strikes, magnetic locks, crash bars)
- Request-to-exit (REX) devices, door position switches
- Cable routing from readers to panels to central system
- Door grouping and access level zones
- Integration points with Terminal access control system

**4. System Architecture Diagram (ASSUMPTION — typical inclusion)**
- Network topology showing cameras, NVR, VMS, access control panels
- Network switches, firewalls, Terminal connection points
- VLAN segregation and IP addressing scheme **TBD**
- Redundancy and failover paths
- Physical and logical system boundaries

**5. Typical Mounting Details (ASSUMPTION — typical inclusion)**
- Camera mounting brackets and hardware
- Conduit entry and sealing details (especially for hazardous areas)
- Weatherproofing and cable management
- Structural attachment methods coordinated with PKG-05/PKG-06

*Source: Standard security system drawing set structure; specifics TBD per project requirements*

---

*Document status: Enriched draft — Pass 1*
*Enrichment date: 2026-01-28*
*Cross-references: Specification.md for requirements; Datasheet.md for system attributes; Procedure.md for production workflow*
