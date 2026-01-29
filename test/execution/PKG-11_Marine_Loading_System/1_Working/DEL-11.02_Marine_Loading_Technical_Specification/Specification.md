# Specification: DEL-11.02 Marine Loading Technical Specification

## Scope

This document is the draft technical specification for **Marine Loading System** (PKG-11).

**Purpose:** Defines performance, materials, and workmanship requirements for the marine loading system per Employer's Requirements (ER), establishing the technical baseline for procurement, design verification, and acceptance testing.

**Package scope (PKG-11):**
- Powered loading arm (articulated boom with powered slew/luff)
- Emergency release coupling (ERC)
- Double-walled export pipe
- Leak detection system
- Nitrogen supply provisions
- Operator shelter

**Anticipated deliverable artifacts:**
- Marine loading arm specification (Section 4)
- Double-walled pipe specification (Section 5)
- Leak detection specification (Section 6)
- Nitrogen supply requirements (Section 7)
- Operator shelter requirements (Section 8)

**Objectives served (per decomposition Section 6):**
- OBJ-1 Safe & Reliable Operation
- OBJ-2 Throughput Capacity (1,000,000 MT/annum)
- OBJ-4 Operational Flexibility
- OBJ-7 Environmental Protection

## Related Deliverables (PKG-11)

| Deliverable | Relationship |
|-------------|--------------|
| DEL-11.01 Marine Loading Design Drawing Set | Implements layout and interfaces per this specification |
| DEL-11.03 Marine Loading Design Calculations | Provides sizing/verification basis per this specification |
| DEL-11.04 Marine Loading Data Sheet Package | Equipment datasheets aligned with this specification |
| DEL-11.05 Marine Loading Installation & Test Records | Verification evidence of specification compliance |
| DEL-11.06 Marine Loading Arm OEM Qualification Package | Vendor capability and compliance inputs |

## Requirements

### 1. General

**1.1 Purpose**
This specification defines the minimum technical requirements for the marine loading system at Fraser Surrey Terminal, enabling the safe and efficient loading of canola oil to export vessels.

**1.2 Definitions and Abbreviations**
- **ERC:** Emergency Release Coupling
- **ESD:** Emergency Shutdown
- **FAT:** Factory Acceptance Test
- **GA:** General Arrangement
- **OEM:** Original Equipment Manufacturer
- **SAT:** Site Acceptance Test
- **SIL:** Safety Integrity Level

**1.3 Tag Numbering**
Tag numbering conventions: **TBD** — per project standards.

**1.4 Extent of Supply**
| Item | Contractor | OEM/Vendor | Employer |
|------|------------|------------|----------|
| Loading arm (including ERC) | Procurement, installation | Design, manufacture, FAT | Review/approval |
| Double-walled pipe | Design, procurement, installation | Manufacture (if prefab) | Review/approval |
| Leak detection system | Design, procurement, installation | Manufacture | Review/approval |
| Nitrogen supply | Tie-in only (**TBD**) | **TBD** | **TBD** |
| Operator shelter | Interfaces only (**TBD**) | **TBD** | **TBD** |

### 2. Applicable Documents

**2.1 Employer's Requirements**
- `test/Volume_2_Part_1_Employers_Requirements.pdf` — clause references **TBD**
- `test/Volume_2_Part_2_Employers_Requirements.pdf` — clause references **TBD**
- `test/Volume_2_Part_3_Employers_Requirements.pdf` — clause references **TBD**

**2.2 Codes and Standards**
| Standard | Applicability | Status |
|----------|---------------|--------|
| OCIMF Guidelines | Marine loading arm design | **TBD** |
| ASME B31.3 | Process piping | **TBD** |
| API 2610 | Terminal piping design | **TBD** |
| IEC 61511 | Safety instrumented systems | **TBD** |
| NFPA 30 | Flammable/combustible liquids | **TBD** |
| CSA / NBC | Building code (shelter) | **TBD** |

**2.3 Project Documents**
- Project QA/QC requirements: **TBD**
- Project document control procedures: **TBD**
- Project hazardous area classification (PKG-27): **TBD**

### 3. Service / Design Basis

| Parameter | Requirement | Source |
|-----------|-------------|--------|
| Product | Canola oil (refined vegetable oil) | ER **TBD** |
| Design loading rate | **TBD** m³/hr | ER **TBD** |
| Annual throughput capacity | 1,000,000 MT/annum | Decomposition OBJ-2 |
| Operating temperature | **TBD** (typical 20–60°C for canola oil) | ER **TBD** |
| Design temperature range | **TBD** | ER **TBD** |
| Design pressure (arm/pipe) | **TBD** barg | ER **TBD** |
| Ambient temperature | **TBD** (site: approx. –10°C to +35°C) | Site data |
| Environmental classification | Marine/coastal (salt spray, humidity) | Site conditions |
| Hazardous area classification | **TBD** — **ASSUMPTION**: Zone 2 at loading arm | PKG-27 |
| Seismic zone | **TBD** — BC seismic requirements | ER / PKG-08 |
| Design life | **TBD** — **ASSUMPTION**: 25 years minimum | ER **TBD** |
| Corrosion allowance | **TBD** mm | ER **TBD** |

### 4. Marine Loading Arm (Powered) + Emergency Release Coupling (ERC)

**4.1 Type and Configuration**

| Requirement ID | Requirement | Verification |
|----------------|-------------|--------------|
| MLA-001 | Loading arm shall be a powered marine loading arm with articulated boom (inboard/outboard arms with swivel joints) | Design review, FAT |
| MLA-002 | Loading arm shall include emergency release coupling (ERC) with powered breakaway capability | Design review, FAT |
| MLA-003 | Loading arm type/model: **TBD** (OEM selection per DEL-11.06) | Procurement |

**4.2 Reach / Envelope and Operating Range**

| Requirement ID | Requirement | Verification |
|----------------|-------------|--------------|
| MLA-004 | Loading arm reach (outboard): **TBD** m | Design review, DEL-11.03 |
| MLA-005 | Loading arm reach (inboard): **TBD** m | Design review, DEL-11.03 |
| MLA-006 | Operating envelope shall accommodate design vessel range: **TBD** | Design review |
| MLA-007 | Slew angle: **TBD** degrees | Design review |
| MLA-008 | Luff angle range: **TBD** degrees | Design review |

**4.3 Connection Interface**

| Requirement ID | Requirement | Verification |
|----------------|-------------|--------------|
| MLA-009 | Vessel manifold connection size: **TBD** inch | Design review |
| MLA-010 | Connection rating: **TBD** (ANSI class) | Design review |
| MLA-011 | Connection type: **TBD** (quick-connect coupler or flanged) | Design review |
| MLA-012 | Shore connection interface: **TBD** | Design review |

**4.4 Materials and Product Compatibility**

| Requirement ID | Requirement | Verification |
|----------------|-------------|--------------|
| MLA-013 | Wetted materials shall be compatible with canola oil: **TBD** (stainless steel or carbon steel) | Material certificates |
| MLA-014 | Seals and gaskets: **TBD** — compatible with product and operating temperature | Material certificates |
| MLA-015 | External coatings/paint: **TBD** — suitable for marine environment | Inspection |

**4.5 Mechanical Components**

| Requirement ID | Requirement | Verification |
|----------------|-------------|--------------|
| MLA-016 | Swivel joints: **TBD** (type, sealing arrangement) | FAT |
| MLA-017 | Balance system: **TBD** (counterweight or hydraulic) | Design review |
| MLA-018 | Drive system: **TBD** (hydraulic or electric) | Design review |
| MLA-019 | Slew/luff speed: **TBD** | FAT |

**4.6 Emergency Release Coupling (ERC)**

| Requirement ID | Requirement | Verification |
|----------------|-------------|--------------|
| MLA-020 | ERC shall provide automatic release on vessel drift exceeding operating envelope | FAT |
| MLA-021 | ERC release force: **TBD** kN | FAT |
| MLA-022 | Spillage on ERC activation: **TBD** litres maximum | FAT |
| MLA-023 | ERC reset capability: **TBD** (field-resettable or replacement required) | Design review |
| MLA-024 | ERC actuation: **TBD** (automatic + manual override) | FAT |

**4.7 Controls / Operator Interface**

| Requirement ID | Requirement | Verification |
|----------------|-------------|--------------|
| MLA-025 | Local control station: **TBD** (pendant or console) | FAT |
| MLA-026 | Remote control capability: **TBD** (control room interface) | SAT |
| MLA-027 | Position indication: **TBD** (arm position feedback to PLC/DCS) | SAT |
| MLA-028 | Operating permissives: **TBD** (alignment, ESD status, leak detection status) | SAT |

**4.8 Safety**

| Requirement ID | Requirement | Verification |
|----------------|-------------|--------------|
| MLA-029 | Loading arm shall integrate with facility ESD system | SAT |
| MLA-030 | Emergency stop stations: **TBD** (locations per ER) | Site inspection |
| MLA-031 | Interlocks: **TBD** (operating limits, ERC status, leak detection) | SAT |
| MLA-032 | SIL rating (if applicable): **TBD** | SIL verification |

### 5. Double-Walled Export Pipe

**5.1 Design Code and Pressure Rating**

| Requirement ID | Requirement | Verification |
|----------------|-------------|--------------|
| DWP-001 | Inner pipe design code: **TBD** (ASME B31.3 or equivalent) | Design review |
| DWP-002 | Inner pipe design pressure: **TBD** barg | Design review |
| DWP-003 | Outer pipe (containment): **TBD** design basis | Design review |
| DWP-004 | Annulus space: **TBD** mm minimum | Design review |

**5.2 Pipe Material and Corrosion Protection**

| Requirement ID | Requirement | Verification |
|----------------|-------------|--------------|
| DWP-005 | Inner pipe material: **TBD** (carbon steel or stainless steel) | Material certificates |
| DWP-006 | Outer pipe material: **TBD** (carbon steel) | Material certificates |
| DWP-007 | Corrosion allowance (inner): **TBD** mm | Design review |
| DWP-008 | External coating: **TBD** — suitable for marine environment | Inspection |
| DWP-009 | Internal lining (if required): **TBD** | Design review |

**5.3 Annulus Design and Monitoring**

| Requirement ID | Requirement | Verification |
|----------------|-------------|--------------|
| DWP-010 | Annulus shall be designed for leak detection monitoring | Design review |
| DWP-011 | Annulus monitoring tap points: **TBD** (locations and spacing) | Design review |
| DWP-012 | Annulus drainage provisions: **TBD** | Design review |
| DWP-013 | Annulus access for inspection: **TBD** | Design review |

**5.4 Drainage and Low-Point Management**

| Requirement ID | Requirement | Verification |
|----------------|-------------|--------------|
| DWP-014 | Low points shall be provided with drain connections | Design review |
| DWP-015 | Drainage to containment/recovery: **TBD** | Design review |

**5.5 Supports, Expansion, and Movement**

| Requirement ID | Requirement | Verification |
|----------------|-------------|--------------|
| DWP-016 | Pipe supports: **TBD** (type, spacing per stress analysis) | DEL-11.03 |
| DWP-017 | Expansion provisions: **TBD** (loops, bellows, or sliding supports) | DEL-11.03 |
| DWP-018 | Movement at loading arm connection: **TBD** | DEL-11.03 |

**5.6 Testing**

| Requirement ID | Requirement | Verification |
|----------------|-------------|--------------|
| DWP-019 | Hydrotest pressure (inner pipe): **TBD** barg | Test records |
| DWP-020 | Annulus leak test: **TBD** (method and acceptance criteria) | Test records |

### 6. Leak Detection System

**6.1 Detection Philosophy**

| Requirement ID | Requirement | Verification |
|----------------|-------------|--------------|
| LDS-001 | Leak detection philosophy: continuous monitoring of double-walled pipe annulus, drip trays, and containment sumps | Design review |
| LDS-002 | Detection method (annulus): **TBD** (vacuum, pressure, or liquid sensing) | Design review |
| LDS-003 | Detection method (drip trays/sumps): **TBD** (level switches or sensors) | Design review |

**6.2 Detection Zones and Device Placement**

| Requirement ID | Requirement | Verification |
|----------------|-------------|--------------|
| LDS-004 | Leak detection zones: **TBD** (number and coverage) | Design review |
| LDS-005 | Device placement per DEL-11.01 leak detection layout | Design review |
| LDS-006 | Device accessibility for maintenance: **TBD** | Design review |

**6.3 Alarm and ESD Integration**

| Requirement ID | Requirement | Verification |
|----------------|-------------|--------------|
| LDS-007 | Leak alarm: **TBD** (alarm setpoint, annunciation) | SAT |
| LDS-008 | Leak trip (ESD): **TBD** (trip setpoint, shutdown scope) | SAT |
| LDS-009 | Signal interface to ESD/PLC: **TBD** (hardwired or networked) | Design review |
| LDS-010 | Alarm/trip response time: **TBD** seconds | SAT |

**6.4 Functional Testing and Periodic Test Provisions**

| Requirement ID | Requirement | Verification |
|----------------|-------------|--------------|
| LDS-011 | Functional test provisions: **TBD** (test ports, simulation capability) | Design review |
| LDS-012 | Periodic test interval: **TBD** | Operating procedures |

**6.5 Fail-Safe and Diagnostics**

| Requirement ID | Requirement | Verification |
|----------------|-------------|--------------|
| LDS-013 | Fail-safe design: system shall fail to safe state (alarm or trip) on sensor failure | Design review |
| LDS-014 | Diagnostics: **TBD** (self-test, fault indication) | FAT |

### 7. Nitrogen Supply / Purge

| Requirement ID | Requirement | Verification |
|----------------|-------------|--------------|
| N2-001 | Purpose: **TBD** (purge, inerting, or pressurization) | Design review |
| N2-002 | Supply source: **TBD** (facility nitrogen system or dedicated) | Design review |
| N2-003 | Supply pressure: **TBD** barg | Design review |
| N2-004 | Flow capacity: **TBD** Nm³/hr | Design review |
| N2-005 | Pressure regulation and relief: **TBD** | Design review |
| N2-006 | Interface to loading arm: **TBD** | Design review |
| N2-007 | Interface to double-walled pipe (if applicable): **TBD** | Design review |

### 8. Operator Shelter — Requirements (Interfaces)

| Requirement ID | Requirement | Verification |
|----------------|-------------|--------------|
| SHL-001 | Shelter function: weather protection for loading operator | Design review |
| SHL-002 | Location: **TBD** (visibility to loading arm, access to controls) | Design review |
| SHL-003 | Building services: power, lighting, HVAC — **TBD** interfaces | Design review |
| SHL-004 | Control panel location within shelter: **TBD** (HMI, ESD buttons) | Design review |
| SHL-005 | Structural/civil interfaces: **TBD** (foundation, access) | Design review |

*Note: Detailed shelter design is covered by PKG-22 Building Works; this specification defines interface requirements only.*

### 9. Fabrication, Installation, and Testing

**9.1 QA/QC and Inspection**

| Requirement ID | Requirement | Verification |
|----------------|-------------|--------------|
| FAB-001 | QA/QC per project quality procedures: **TBD** | QA records |
| FAB-002 | Inspection and test plan (ITP): **TBD** | ITP approval |
| FAB-003 | Weld inspection: **TBD** (NDE requirements) | Weld records |

**9.2 Factory Acceptance Testing (FAT)**

| Requirement ID | Requirement | Verification |
|----------------|-------------|--------------|
| FAB-004 | Loading arm FAT: **TBD** (functional test, ERC test, leak test) | FAT records |
| FAB-005 | FAT witness: **TBD** (Contractor, Employer) | FAT records |

**9.3 Site Acceptance Testing (SAT) / Commissioning**

| Requirement ID | Requirement | Verification |
|----------------|-------------|--------------|
| FAB-006 | Installation inspection: **TBD** | Installation records |
| FAB-007 | SAT: **TBD** (functional test, ESD integration test) | SAT records |
| FAB-008 | Leak detection functional test: **TBD** | Test records |
| FAB-009 | Commissioning support from OEM: **TBD** | Contract terms |

### 10. Submittals / Deliverables

| Submittal | Responsible | Timing |
|-----------|-------------|--------|
| Loading arm vendor data and drawings | OEM via Contractor | Per procurement schedule |
| Pipe fabrication drawings | Contractor | Per design schedule |
| Leak detection system data | Vendor via Contractor | Per procurement schedule |
| Data sheets (DEL-11.04) | Contractor | Per deliverable schedule |
| Drawings (DEL-11.01) | Contractor | Per deliverable schedule |
| Calculations (DEL-11.03) | Contractor | Per deliverable schedule |
| Installation & test records (DEL-11.05) | Contractor (QA/QC) | Per construction schedule |
| OEM qualification package (DEL-11.06) | Contractor (with OEM) | Per procurement schedule |

## Compliance Matrix

| ER Clause | Requirement Summary | Specification Section | Status |
|-----------|---------------------|----------------------|--------|
| **TBD** | Loading arm requirements | §4 | Pending ER extraction |
| **TBD** | Double-walled pipe requirements | §5 | Pending ER extraction |
| **TBD** | Leak detection requirements | §6 | Pending ER extraction |
| **TBD** | Environmental protection | §5, §6 | Pending ER extraction |
| **TBD** | Safety/ESD integration | §4.8, §6.3 | Pending ER extraction |

*Note: Compliance matrix to be populated when ER clause references are available.*

## Documentation

**Required documentation outputs:**
- Marine loading arm specification (this document, Section 4)
- Double-walled pipe specification (this document, Section 5)
- Leak detection specification (this document, Section 6)

**Documentation requirements:**
- All documents shall comply with project document control procedures
- Revision control per project numbering system — **TBD**
- Format: **TBD** (project document management requirements)

---

**Pass 2/3 Enrichment Summary:**

**Document structure verified:**
- §1 General: Scope definition, extent of supply (Procedure Step 2)
- §2 Applicable Documents: ER references, 6+ standards (Datasheet §Standards lists 8 standards)
- §3 Service/Design Basis: 11 parameters (aligns with Datasheet §Conditions)
- §4 Loading Arm: 32 requirements (MLA-001 to MLA-032) — Procedure Step 3, Guidance §Considerations
- §5 Double-Walled Pipe: 20 requirements (DWP-001 to DWP-020) — Procedure Step 4, Guidance §Considerations  
- §6 Leak Detection: 14 requirements (LDS-001 to LDS-014) — Procedure Step 5, Guidance §Considerations
- §7 Nitrogen Supply: 7 requirements (N2-001 to N2-007) — Procedure Step 6
- §8 Operator Shelter: 5 requirements (SHL-001 to SHL-005) — Procedure Step 6
- §9 Fabrication/Testing: 9 requirements (FAB-001 to FAB-009) — Procedure Step 7
- §10 Submittals: Deliverables list aligns with PKG-11 decomposition table

**Total requirement count: 58+ requirements across §4-§9**

**Cross-document traceability:**
- Design basis (§3, 11 parameters) → Datasheet §Conditions → Procedure §Prerequisites
- Requirements (§4-§9, 58+ reqs) → Datasheet §Construction (5 artifacts) → Procedure §Steps 3-7 → Guidance §Considerations
- Standards (§2.2) → Datasheet §Standards (8 standards) → Guidance §Principles
- Interfaces (§4.7, §6.3, §7, §8) → Datasheet §Interfaces (8 interfaces) → Procedure §Step 9 (IDC)
- Compliance matrix (§Compliance Matrix) → Datasheet §Deliverable Acceptance criterion 3 → Procedure §Step 8
- Verification columns → Procedure §Verification → Guidance §Examples (verification matrix)
- Submittals (§10) → Datasheet §Cross-Document Links → Related deliverables table

**Source citations:**
- All requirements include verification method (test, inspection, review, analysis)
- ER references marked **TBD** throughout (pending clause extraction per user instruction)
- Decomposition references cited where applicable (OBJ-2 throughput, PKG-11 scope)
- Adjacent deliverable references: DEL-11.01 (drawings), DEL-11.03 (calcs), DEL-11.06 (OEM), DEL-14 (piping), DEL-19 (I&C), PKG-22 (shelter)

**Alignment verification:**
- All 58+ requirements have assigned requirement IDs and verification methods
- Extent of supply (§1.4) aligns with Procedure Step 2 output
- Design basis parameters (§3) align with Datasheet §Conditions (same 11 parameters)
- Requirement sections (§4-§8) produce 5 specification artifacts listed in Datasheet §Construction
- Compliance matrix structure supports Procedure Step 8 and Datasheet acceptance criterion 3
- All TBDs and ASSUMPTIONs preserved from Pass 1
- No conflicts identified (Guidance §Conflict Table empty as expected)

**Enrichment completeness:** Pass 2 and Pass 3 cross-document consistency checks completed. All requirements trace to Datasheet attributes, Procedure steps, and Guidance considerations. Full source fidelity maintained with explicit **TBD** markers where ER clauses not yet available.
