# Guidance: DEL-24.02 Security System Technical Specification

## Purpose

This guidance document supports the development of the **Security System Technical Specification** for **PKG-24 Security Systems** at the Canola Oil Transload Facility.

**Deliverable objective:** Defines performance, materials, and workmanship requirements for security system per ER requirements, providing the technical basis for equipment procurement and installation.

*Source: `_CONTEXT.md`; Decomposition Section 5 — PKG-24 (line 567)*

**Classification:** Specification deliverable under Specialty discipline, to be produced by D&B Contractor

**Project context:** This technical specification translates design intent (DEL-24.01) into procurable and constructible requirements, supporting OBJ-1 (Safe & Reliable Operation) and OBJ-6 (Regulatory Compliance) for a 1,000,000 MT/annum canola oil transload facility.

*Source: Decomposition Sections 1.1 and 2; DEL-24.01 as design basis*

## Principles

### Technical Specification Development Philosophy

#### Performance-Based vs. Prescriptive Specifications
**Approach:** Balance performance-based requirements (what the system must achieve) with prescriptive requirements (specific products/methods) based on project needs.

**Performance-based:**
- Allows contractor/supplier flexibility and innovation
- Suitable where outcome is well-defined but multiple valid solutions exist
- Example: "Cameras shall provide minimum 100 pixels per meter at 10m distance for facial identification"

**Prescriptive:**
- Specifies exact products, materials, or methods
- Suitable where specific standards, compatibility, or Terminal integration requirements exist
- Example: "Access control system shall be [specific manufacturer/model] for compatibility with Terminal systems"

**Project application (ASSUMPTION):**
- Prescriptive for Terminal integration components (per DEC-05 — must be compatible with existing Terminal systems)
- Performance-based for general equipment where multiple suppliers/products can meet requirements
- Balanced approach for critical systems (specify performance requirements plus approved manufacturers list)

*Source: DEC-05 (Decomposition Section 7); standard technical specification development practice*

#### Clear and Enforceable Requirements
- Use "shall" for mandatory requirements, "should" for recommendations, "may" for permissible options
- Requirements must be verifiable and testable (via inspection, testing, or documentation review)
- Avoid ambiguous terms like "adequate," "suitable," "high quality" without defining acceptance criteria
- Link requirements to verification methods (inspection, testing, analysis, demonstration)

*Source: Standard specification writing practice*

#### Traceability and Completeness
- All requirements shall be traceable to:
  - Employer's Requirements (ER) sections
  - Design basis (DEL-24.01 drawings)
  - Applicable codes and standards
  - Project objectives (OBJ-1, OBJ-5, OBJ-6, etc.)
- ER compliance matrix maintains traceability from ER to specification sections

*Source: Standard requirements management practice*

### Applicable Standards Context

**Security Industry Standards Framework:**
- IEC 62676 series provides international framework for video surveillance system design and specification
- ONVIF ensures camera/VMS interoperability across vendors
- OSDP provides secure, encrypted communication for access control (superior to legacy Wiegand protocol)

**Canadian Regulatory Context:**
- Canadian Electrical Code governs electrical safety and hazardous area installation methods
- NBC 2020 governs structural mounting and seismic requirements
- Privacy legislation (PIPEDA) governs video surveillance data collection, use, and retention **ASSUMPTION**
- WorkSafeBC and OHS regulations may require monitoring of remote/hazardous work areas

*Source: Standard Canadian security system regulatory context; specifics TBD per ER*

### Terminal Integration Strategy (DEC-05)

**Separate System Interfaces per DEC-05:**
- CCTV integration: Connection to Terminal VMS or separate monitoring station
- Access control integration: Credential synchronization with Terminal access control platform, or standalone operation with interface for reporting
- Communications network: Separate security VLAN on Terminal network backbone, or isolated network with firewall/gateway

**Integration Specification Approach:**
- Define clear interface points and protocols
- Specify data formats and exchange mechanisms
- Define security requirements (encryption, authentication, network segregation)
- Coordinate with Employer/Terminal IT for integration standards and procedures **TBD**

*Source: DEC-05 (Decomposition Section 7)*

## Considerations

### Factors to Consider During Specification Development

#### 1. Design Basis Integration
**The specification shall support the design (DEL-24.01):**
- Camera specifications (resolution, lens, performance) shall align with coverage analysis from DEL-24.01
- Equipment quantities and locations shall match design drawings
- Installation requirements shall support design mounting methods and cable routing
- Network specifications shall support design topology and bandwidth requirements

**Coordination process:**
- Review DEL-24.01 drawings to understand design intent
- Extract equipment counts, types, and performance requirements from coverage analysis
- Ensure specification requirements are sufficient to achieve design objectives

*Source: Standard design-to-specification workflow*

#### 2. Equipment Selection Strategy

**Approved Manufacturers List vs. Open Competition:**
- **Approved list:** Limits equipment to specific manufacturers meeting stringent requirements (quality, compatibility, support)
  - Advantages: Ensures compatibility, simplifies integration, reduces risk
  - Disadvantages: May increase cost, reduce competition
  - Recommended for: Terminal integration components, critical systems

- **Open performance specification:** Allows any equipment meeting performance requirements
  - Advantages: Competitive pricing, contractor flexibility, innovation
  - Disadvantages: Integration risk, variable quality, support inconsistency
  - Recommended for: General cameras, standard access control hardware

**Project application (ASSUMPTION):**
- Approved manufacturers list for VMS, access control platform, Terminal integration equipment
- Performance specification with minimum standards for cameras, network switches, UPS, cabling

*Source: Standard equipment procurement strategies*

#### 3. Environmental Requirements for Coastal Marine Facility

**Marine environment challenges:**
- Salt spray corrosion — specify marine-grade materials (stainless steel 316, powder-coated aluminum)
- High humidity — specify environmental ratings and conformal coating for electronics
- Temperature extremes — specify wide operating temperature range for outdoor equipment
- UV exposure — specify UV-resistant housings and cable jackets

**Hazardous area considerations:**
- Equipment in Class I Div 2 areas requires appropriate ratings and installation methods
- Specify conduit sealing requirements per CEC for hazardous areas
- Coordinate hazardous area equipment specifications with area classification drawings **TBD**

*Source: Fraser Surrey Terminal coastal location; industrial facility hazardous area requirements*

#### 4. Reliability and Maintainability

**Reliability requirements (support OBJ-1):**
- Specify equipment MTBF (Mean Time Between Failures)
- Require redundancy for critical components (NVR, network switches, power supplies) **TBD**
- Specify battery backup duration for power outages
- Require manufacturer support and warranty terms

**Maintainability requirements:**
- Specify spare parts and consumables inventory **TBD**
- Require manufacturer training for maintenance personnel
- Specify documentation requirements (manuals, as-builts, maintenance procedures)
- Consider standardization to reduce spare parts inventory

*Source: OBJ-1 (Decomposition Section 2); OBJ-9 (Lifecycle Cost Optimization)*

#### 5. Submittals and Shop Drawings

**Submittal requirements (detailed in DEL-24.03):**
- Equipment datasheets and technical specifications
- Shop drawings for custom fabrications
- Product certifications (UL, CSA, IP/IK ratings, environmental testing)
- Test reports (FAT results, environmental testing)
- Integration documentation (protocols, APIs, configuration guides)

**Submittal review process:**
- Contractor submits equipment proposals for approval
- Designer reviews for compliance with specification
- Employer reviews for acceptance **TBD** — review milestones
- Approved submittals become contract documents

*Source: Standard construction procurement and submittals process; DEL-24.03*

#### 6. Testing and Commissioning Requirements

**Specify testing at multiple stages:**
- Factory testing: Manufacturer QC and Factory Acceptance Testing (FAT) for major equipment
- Pre-installation testing: Verify equipment on-site before installation
- Installation testing: Verify proper installation per manufacturer instructions and codes
- System testing: Functional testing of integrated system (Site Acceptance Testing - SAT)
- Commissioning: Integrated operation with Terminal systems, performance verification

**Acceptance criteria:**
- Define clear, measurable acceptance criteria for each test stage
- Link acceptance criteria to functional and performance requirements
- Specify documentation requirements (test procedures, test results, deficiency lists)

*Source: Standard testing and commissioning requirements; PKG-29 (Testing), PKG-30 (Commissioning)*

## Trade-offs

### Competing Concerns to Evaluate

#### 1. Specification Detail vs. Contractor Flexibility
**Trade-off:** Highly detailed specifications reduce ambiguity but limit contractor innovation and competitiveness.

**Considerations:**
- Critical systems and Terminal integration: Detailed prescriptive specifications
- Standard components: Performance-based specifications with minimum standards
- Balance: Specify performance requirements, provide examples of acceptable products, allow equivalent

*Decision approach: Detailed for integration/critical systems, performance-based for standard equipment*

#### 2. Equipment Quality vs. Cost
**Trade-off:** Higher-grade equipment (commercial/industrial vs. consumer-grade) increases reliability but also cost.

**Considerations:**
- Industrial-grade equipment for harsh environment and 24/7 operation (support OBJ-1)
- Marine-grade materials for coastal environment
- Lifecycle cost analysis: Higher initial cost may reduce maintenance and replacement costs (OBJ-9)

*Decision approach: Specify industrial/commercial-grade equipment; justify with reliability and lifecycle cost benefits*

*Source: OBJ-1, OBJ-9 (Decomposition Section 2)*

#### 3. Open Standards vs. Proprietary Integration
**Trade-off:** Open standards (ONVIF, OSDP) enable multi-vendor interoperability but may sacrifice optimized integration; proprietary systems provide tighter integration but vendor lock-in.

**Considerations:**
- Open standards preferred for future flexibility and competitive pricing
- Proprietary acceptable where Terminal compatibility requires specific platforms
- API availability important for custom integrations

*Decision approach: Require open standards where feasible; accept proprietary for Terminal integration per Employer requirements*

*Source: DEC-05 integration requirements; industry best practice*

#### 4. Redundancy vs. Simplicity/Cost
**Trade-off:** Redundant systems (dual NVR, ring network topology) increase reliability but add complexity and cost.

**Considerations:**
- Redundancy for life-safety-critical functions (access control for emergency egress)
- Redundancy for high-value monitoring areas (custody transfer, critical assets)
- Graceful degradation acceptable for general monitoring (OBJ-1 supports reliability)
- Cost-benefit analysis: Redundancy cost vs. downtime impact

*Decision approach: Redundancy for critical systems; document redundancy strategy in specification*

*Source: OBJ-1 (Decomposition Section 2)*

#### 5. Future Expansion vs. Current Needs
**Trade-off:** Over-sizing infrastructure (network, NVR capacity, power) for future growth (OBJ-8) increases current cost.

**Considerations:**
- Design for Phase 2 expansion per OBJ-8
- Specify scalable architectures (distributed controllers, modular NVR storage)
- Provide excess capacity in infrastructure (conduit, cable tray, network backbone)
- Balance: 20-30% excess capacity typical for expansion without major over-investment

*Decision approach: Specify scalable systems with ~20% expansion capacity; document expansion approach*

*Source: OBJ-8 (Decomposition Section 2) — Future Expandability*

## Examples

### Reference Examples and Precedents

**Project-Specific References:**
- Employer's Requirements Volume 2 **TBD** — expected to provide:
  - Security system performance criteria and functional requirements
  - Equipment standards and approved manufacturers
  - Integration requirements with Terminal systems
  - Testing and acceptance criteria

*Source: Decomposition Section 3 — Reference Documents*

**Industry Standards and Guides (ASSUMPTION):**
- **TBD** — IEC 62676-4 (Operational requirements for video surveillance systems)
- **TBD** — ASIS/SIA security industry specifications and best practices
- **TBD** — CSI MasterFormat Division 28 (Electronic Safety and Security) specification examples

**Terminal Standards:**
- **TBD** — DP World Fraser Surrey Terminal security standards and specifications
- **TBD** — Existing Terminal security system specifications (for compatibility reference)

### Specification Structure Example (CSI MasterFormat Approach)

**Section 28 23 00 — Video Surveillance (CCTV) System (example structure):**

**Part 1 — General**
- 1.1 Summary (scope, related sections)
- 1.2 References (applicable standards)
- 1.3 Submittals (product data, shop drawings, O&M manuals, warranties)
- 1.4 Quality Assurance (manufacturer qualifications, installer qualifications, certifications)
- 1.5 Delivery, Storage, and Handling
- 1.6 Project Conditions (environmental requirements, coordination)
- 1.7 Warranty

**Part 2 — Products**
- 2.1 System Description (overall architecture, performance requirements)
- 2.2 Cameras (fixed, PTZ, specifications, environmental ratings)
- 2.3 Video Recording (NVR, storage, specifications)
- 2.4 Video Management System (VMS software, features, licensing)
- 2.5 Network Infrastructure (switches, cabling, fiber)
- 2.6 Accessories (mounts, enclosures, cable management)
- 2.7 Materials (conduit, cable, connectors)

**Part 3 — Execution**
- 3.1 Installation (general requirements, coordination, mounting, cable routing)
- 3.2 Testing (factory testing, pre-installation testing, system testing, acceptance criteria)
- 3.3 Commissioning (integration testing, performance verification)
- 3.4 Training (operations training, maintenance training)
- 3.5 Closeout (documentation, as-builts, warranties)

*Source: CSI MasterFormat structure (typical for technical specifications) **ASSUMPTION***

### Specification Language Examples

**Performance-based requirement:**
> "Cameras shall provide minimum image resolution of 100 pixels per meter at a distance of 10 meters, suitable for facial recognition and identification purposes. Camera selection and lens specifications shall be verified by coverage analysis per design drawings (DEL-24.01)."

**Prescriptive requirement:**
> "Network video recorder shall be [Manufacturer], Model [Model Number], or approved equivalent, with minimum 64 channels, 4K recording capability, and 90-day storage capacity at specified resolution and frame rate."

**Verification requirement:**
> "Contractor shall demonstrate camera coverage and image quality during Site Acceptance Testing by capturing test images of designated targets at specified locations and verifying pixel density, clarity, and identification capability per acceptance criteria."

---

*Document status: Enriched draft — Pass 1*
*Enrichment date: 2026-01-28*
*Cross-references: Specification.md for requirements; Datasheet.md for system attributes; Procedure.md for production workflow*
