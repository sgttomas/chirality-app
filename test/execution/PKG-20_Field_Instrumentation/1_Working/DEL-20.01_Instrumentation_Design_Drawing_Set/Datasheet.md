# Datasheet: DEL-20.01 Instrumentation Design Drawing Set

## Identification

| Field | Value | Specification § | Guidance § | Procedure Step |
|-------|-------|-----------------|------------|----------------|
| Deliverable ID | DEL-20.01 | Scope | Purpose | 1.1 |
| Name | Instrumentation Design Drawing Set | Scope | Purpose | 1.1 |
| Package | PKG-20 Field Instrumentation | Scope | Purpose | — |
| Discipline | I&C | Scope | Purpose | Prerequisites |
| Type | Drawing | Scope | Downstream Use | 1.2 |
| Responsible | D&B Contractor | Scope | Purpose | Prerequisites |
| Status | INITIALIZED | — | — | — |
| Project | Canola Oil Transload Facility — Phase 1 | Scope | Purpose | 1.1 |
| Location | Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC | FR-6 | Location: Marine Terminal | 1.1 |

## Attributes

| Attribute | Value | Specification § | Guidance § | Procedure Step |
|-----------|-------|-----------------|------------|----------------|
| Drawing Type | Instrumentation arrangement and installation details | FR-1 | Engineering Rationale | 2.1, 3.1 |
| Drawing Scale | **TBD** — **ASSUMPTION**: Typical scales 1:50, 1:100 for plans; NTS for details | PR-1 | Trade-off 3 | 3.1 |
| Sheet Size | **TBD** — **ASSUMPTION**: ISO A1 or ANSI D per project CAD standards | PR-1 | CAD Standards | 3.1 |
| CAD Standard | **TBD** — To be confirmed per project document management plan | PR-1, PR-2 | CAD Standards | 1.3 |
| Drawing Format | **TBD** — **ASSUMPTION**: Electronic PDF/DWG per project requirements | PR-1 | Documentation | 5.2 |
| Revision Control | **TBD** — Per project document control procedures | QR-2 | Quality Considerations | 6.1 |
| Classification | **TBD** — **ASSUMPTION**: Contractor's Design Documents (for construction) | Documentation | Downstream Use | 5.2 |

**Source:** Decomposition document `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`, Section PKG-20, DEL-20.01 (line 496)

## Conditions

**Project Context:**

This drawing set supports the Canola Oil Transload Facility Phase 1 where Crude Super Degummed (CSD) grade canola oil transfers from rail tank cars to liquid bulk carriers for export.

**Source:** Decomposition document, Section 1.1 Project Overview

**Key Project Parameters:**

| Parameter | Value | Source | Specification § | Guidance § |
|-----------|-------|--------|-----------------|------------|
| Permitted Throughput | 1,000,000 MT per annum | Decomposition, Section 1.1 | FR-6 | Facility Type |
| Storage Capacity | 45,000 MT (3 × 15,000 MT tanks) | Decomposition, Section 1.1 | FR-6 | Storage Tanks Example |
| Product Grade | CSD (Crude Super Degummed) canola oil | Decomposition, Section 1.1 | FR-6 | Facility Type |
| Railcar Capacity | 32 unloading stations on 2 tracks | Decomposition, Section 1.1 | FR-6 | Railcar Unloading Example |

**Operating / Environmental Context:**

| Condition | Value | Source | Specification § | Guidance § |
|-----------|-------|--------|-----------------|------------|
| Location | Marine terminal environment, British Columbia coast | Decomposition, Section 1.1 | FR-6 | Principle 2 |
| Operating temperature range | **TBD** — **ASSUMPTION**: Outdoor instrumentation rated for -30°C to +50°C (typical BC coastal range) | **TBD**: ER requirements | FR-6, PR-1 | Principle 2 |
| Environmental classification | **TBD** — Marine/coastal exposure with corrosion considerations | **TBD**: ER requirements | FR-6 | Principle 2 |
| Hazardous area classification | **TBD** — To be determined per facility hazardous area classification study (CSD canola oil vapor considerations) | **TBD**: Classification study | FR-3, Standards | Principle 3 |
| Seismic requirements | **TBD** — **ASSUMPTION**: Per NBC 2015 and BC Building Code for Surrey, BC location | **ASSUMPTION** | Standards | Location: Marine Terminal |
| Design life | **TBD** — **ASSUMPTION**: 25 years minimum per typical industrial facility standards | **ASSUMPTION** | — | — |

**Instrumentation Scope:**

Package PKG-20 scope includes field instruments, transmitters, switches, instrument cabling, and junction boxes.

**Source:** Decomposition document, Section PKG-20 Scope (line 490)

## Construction

**Anticipated Drawing Artifacts:**

The following drawing types shall be produced as part of this deliverable:

| Artifact | Description | Specification § | Guidance § | Procedure Step |
|----------|-------------|-----------------|------------|----------------|
| Instrument location plans | Show spatial arrangement of field instruments on facility plans | FR-2 | Example 1 | 2.1, 3.1 |
| Instrument installation details | Provide installation mounting and connection details for field instruments | FR-3 | Example 2 | 2.3, 3.2 |
| Cable schedules | Define instrument cable routing, terminations, and specifications | FR-4 | Example 3 | 2.2, 3.3 |

**Source:** Decomposition document, DEL-20.01 Anticipated Artifacts (line 496); `_CONTEXT.md`

**Instrumentation Types (Typical):**

Based on facility scope, instrumentation drawings will address:

| Instrument Type | Application | Related Package | Specification § | Guidance § |
|-----------------|-------------|-----------------|-----------------|------------|
| Level transmitters | Storage tanks, process vessels | PKG-13 Storage Tanks | FR-6, INT-1 | Storage Tanks Example |
| Pressure transmitters | Piping systems, loading arms | PKG-14 Process Piping | FR-6, INT-1 | Marine Loading Example |
| Flow instruments | Custody transfer metering, process control | PKG-12 Product Transfer | FR-6, INT-1 | Marine Loading Example |
| Temperature instruments | Product monitoring, tank heating | PKG-13 Storage Tanks | FR-6, INT-1 | Storage Tanks Example |
| Switches and local indicators | Safety interlocks, local display | Various | FR-6, INT-1 | Principle 1 |

**Source:** **ASSUMPTION** based on PKG-20 scope (field instruments, transmitters, switches) and facility function (storage, transfer, metering)

**Installation Requirements:**

| Requirement | Value | Specification § | Guidance § | Procedure Step |
|-------------|-------|-----------------|------------|----------------|
| Instrument mounting | **TBD** — Per manufacturer requirements and ISA standards | FR-3 | Principle 4 | 3.2 |
| Cable routing | **TBD** — Underground duct banks, cable trays, conduit systems (coordinate with PKG-23 Electrical Infrastructure) | FR-4, INT-1 | Cable Routing | 2.2, 3.3 |
| Junction boxes | **TBD** — Locations and environmental ratings per hazardous area classification | FR-4, INT-1 | Junction Box Locations | 2.2 |
| Weatherproofing | **TBD** — Outdoor instrument enclosures and environmental protection | FR-3, FR-6 | Principle 2 | 3.2 |

**Commissioning Interface:**

Installation details shall support loop checking and calibration activities per DEL-20.05 Instrumentation Installation & Test Records.

**Source:** Cross-reference to DEL-20.05 per decomposition (line 500)

## References

**Primary References:**

| Reference | Location | Specification § | Guidance § |
|-----------|----------|-----------------|------------|
| Decomposition document | `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` (Section PKG-20) | Scope | Purpose |
| `_CONTEXT.md` | Deliverable folder | Scope | Purpose |
| `_REFERENCES.md` | Deliverable folder — currently: no references identified | — | — |
| Employer's Requirements | **TBD**: Specific sections to be identified from Vol 2 Parts 1-3 | Standards | Standards Context |

**Applicable I&C Standards:**

| Standard | Description | Applicability | Specification § | Guidance § |
|----------|-------------|---------------|-----------------|------------|
| ISA 5.1 | Instrumentation Symbols and Identification | **ASSUMPTION**: Applicable for P&ID and instrumentation drawing symbology | Standards, PR-2 | Standards Context |
| ISA 84 / IEC 61511 | Functional Safety (SIS) | **ASSUMPTION**: Applicable if safety instrumented systems are included in facility design | Standards | Standards Context |
| CSA C22.1 | Canadian Electrical Code | **ASSUMPTION**: Applicable for instrument wiring and hazardous area installations in BC | Standards | Standards Context |
| API 554 | Process Instrumentation and Control | **ASSUMPTION**: Applicable for process industry instrumentation practices | Standards | Standards Context |

**Note:** Standards applicability to be confirmed based on Employer's Requirements and project specification. Specific clause-level requirements **TBD** pending access to standard documents.

**Related Deliverables:**

| Deliverable | Name | Relationship | Specification § |
|-------------|------|--------------|-----------------|
| DEL-20.02 | Instrumentation Technical Specification | Performance and material requirements | INT-2 |
| DEL-20.03 | Instrumentation Design Calculations | Sizing and verification basis | INT-2 |
| DEL-20.04 | Instrumentation Data Sheet Package | Equipment data sheets | INT-2 |
| DEL-20.05 | Instrumentation Installation & Test Records | Commissioning documentation | INT-2 |

**Source:** Decomposition document, PKG-20 deliverables (lines 496-500)

**Interface Packages:**

| Package | Interface Description | Specification § |
|---------|----------------------|-----------------|
| PKG-12 Product Transfer and Metering | Custody transfer instrumentation | INT-1 |
| PKG-13 Storage Tanks | Tank instrumentation (level, temperature) | INT-1 |
| PKG-14 Process Piping | Instrument connections to process piping | INT-1 |
| PKG-15 Pumps and Rotating Equipment | Equipment instrumentation | INT-1 |
| PKG-17 Electrical Power Distribution | Instrument power supply | INT-1 |
| PKG-22 Control Systems & SCADA | Control system I/O and network architecture | INT-1 |
| PKG-23 Electrical Infrastructure | Cable routing infrastructure | INT-1 |

**Dependencies:**

See `_DEPENDENCIES.md` — **NOT_TRACKED**: Dependencies coordinated externally by humans per project coordination plan.

**Project Objective Alignment:**

| Objective | Description | How Supported |
|-----------|-------------|---------------|
| OBJ-1 | Safe & Reliable Operation | Proper instrumentation design ensures safe, reliable facility operations |
| OBJ-6 | Regulatory Compliance | Drawings demonstrate compliance with CSA C22.1 and safety standards |
| OBJ-7 | Environmental Protection | Proper instrumentation enables leak detection and spill prevention |
| OBJ-10 | Custody Transfer Accuracy | Installation details support accurate metering system installation |

**Source:** Decomposition document, Section 6 Objective-to-Deliverable Mapping (line 780)

## Cross-Document Traceability

This Datasheet provides the factual identification, attributes, conditions, and references for DEL-20.01. The following documents provide complementary information:

| Document | Purpose | Key Linkages |
|----------|---------|--------------|
| Specification.md | Requirements and verification criteria | FR-1 to FR-6 define functional requirements; PR-1 to PR-3 define performance requirements; INT-1 to INT-2 define interfaces |
| Guidance.md | Engineering rationale and decision context | Principles 1-5 explain design rationale; Trade-offs 1-4 address key design decisions; Examples illustrate application |
| Procedure.md | Production workflow and verification steps | Steps 1-6 define production process; Verification section defines acceptance criteria; Records section defines outputs |

**Document Consistency Verification:**

- All instrument types listed in Datasheet appear in Specification FR-6 and Guidance Examples
- All interface packages listed in Datasheet appear in Specification INT-1 and Guidance Coordination Considerations
- All standards listed in Datasheet appear in Specification Standards section and Guidance Standards Context
- All related deliverables listed in Datasheet appear in Specification INT-2 and Procedure Integration section
