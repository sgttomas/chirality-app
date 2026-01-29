# Guidance: DEL-10.04 Railcar Unloading Data Sheet Package

## Purpose

This guidance document supports the development of the **Railcar Unloading Data Sheet Package** for **PKG-10 Railcar Unloading System**.

The Data Sheet Package defines and substantiates equipment for the railcar unloading system, providing the technical documentation needed for procurement, fabrication review, installation, and operations. The package covers 32 unloading arms with quick-connect couplers and containment sump pump(s).

**Deliverable Classification:**
- Type: Data Sheet
- Discipline: Process
- Responsible: D&B Contractor

## Principles

**Project Objective Alignment:**

This deliverable supports the following project objectives (per decomposition §6 Objective Mapping):

| Objective | ID | Relevance to DEL-10.04 |
|-----------|-----|------------------------|
| Safe & Reliable Operation | OBJ-1 | Data sheets must specify equipment suitable for safe, reliable service |
| Throughput Capacity (1,000,000 MT/annum) | OBJ-2 | Equipment capacity must support required throughput |
| Operational Flexibility | OBJ-4 | Equipment specifications should enable flexible operations |
| Environmental Protection | OBJ-7 | Materials and containment equipment must protect environment |

**Data Sheet Development Principles:**

| Principle | Application | Specification Link |
|-----------|-------------|-------------------|
| Completeness | All required fields populated; no missing data | FN-04 through FN-07 |
| Accuracy | Data reflects design intent and calculation results | QA-05; IF-02 |
| Consistency | Tagging, units, and terminology consistent across package | QA-01; QA-02 |
| Traceability | Data traceable to design basis, specifications, calculations | IF-01; IF-02 |
| Procurement-ready | Sufficient detail for equipment procurement | FN-xx; UA-xx; SP-xx |

**Data Sheet Content Principles:**

| Principle | Rationale | Quality Link |
|-----------|-----------|--------------|
| Standard format | Use consistent template for each equipment type | QA-03 |
| Clear identification | Unambiguous equipment tagging and service description | FN-04; QA-01 |
| Complete conditions | All operating and design conditions specified | FN-05 |
| Material specification | Materials fully specified for procurement | FN-07 |
| Standards reference | Applicable codes and standards identified | UA-06; SP-05 |

## Considerations

**Equipment Selection Considerations:**

| Equipment | Key Considerations | Guidance |
|-----------|-------------------|----------|
| Unloading Arms | Product compatibility, flow capacity, reach, flexibility, maintainability | Select food-grade compatible; verify reach for railcar positions |
| Quick-Connects | Reliability, drip-free operation, ease of use, seal materials | Select proven couplers suitable for canola oil |
| Sump Pumps | Product compatibility, capacity, submersible vs. external, area classification | Size per containment drainage requirement; coordinate with PKG-17 |

**Process Condition Considerations:**

| Parameter | Consideration | Source |
|-----------|---------------|--------|
| Flow rate | Per station and header capacity | DEL-10.03 calculations |
| Operating temperature | Product temperature range; ambient effects | Product data; site conditions |
| Operating pressure | Gravity flow — low pressure; specify design pressure | DEL-10.03 calculations |
| Product properties | Density, viscosity — affects equipment selection | Product data sheets |

**Material Selection Considerations:**

| Component | Key Considerations | Guidance |
|-----------|-------------------|----------|
| Wetted parts | Food-grade compatibility; corrosion resistance | Per DEL-10.02 material requirements |
| Seals and gaskets | Product compatibility; temperature range | Select materials suitable for canola oil |
| External parts | Environmental exposure; durability | Per site conditions |

**Tagging Considerations:**

| Aspect | Consideration | Guidance |
|--------|---------------|----------|
| Tag scheme | Consistent with project tagging standard | **TBD** — per ER/project |
| Sequential numbering | 32 arms require systematic numbering | E.g., UA-1001 to UA-1032 |
| Location reference | Tags should correlate to physical location | Coordinate with DEL-10.01 drawings |
| P&ID reference | Data sheets should reference P&ID tag | Coordinate with process P&IDs |

## Trade-offs

**Equipment Selection Trade-offs:**

| Trade-off | Option A | Option B | Considerations |
|-----------|----------|----------|----------------|
| Arm type | Standard articulating | Custom design | Cost vs. optimization; **TBD** |
| Quick-connect type | Vendor A standard | Vendor B premium | Cost vs. reliability; **TBD** |
| Sump pump type | Submersible | External vertical | Installation vs. maintenance; **TBD** |
| Material grade | Standard food-grade | Premium stainless | Cost vs. durability; **TBD** |

**ASSUMPTION:** Trade-off decisions to be documented in design rationale records.

**Standardization vs. Optimization:**
- Standardizing all 32 arms simplifies procurement, spares, maintenance
- Custom optimization may improve specific performance aspects
- **ASSUMPTION:** Preference for standardization unless specific benefit identified

## Examples

**Reference Examples and Precedents:**

| Example Type | Source | Application |
|--------------|--------|-------------|
| Unloading arm data sheets | **TBD** — vendor templates, industry examples | Format and content |
| Pump data sheets | API 610 / ISO 13709 formats | Pump data sheet fields |
| Project data sheet templates | **TBD** — Employer's Requirements / contractor | Standard formats |

**Typical Unloading Arm Data Sheet Structure:**

| Section | Content |
|---------|---------|
| 1. General | Tag, service, location, P&ID reference |
| 2. Process Data | Product, flow rate, temperature, pressure |
| 3. Construction | Arm type, size, configuration, reach |
| 4. Connection | Quick-connect details, railcar interface |
| 5. Materials | Wetted parts, seals, external |
| 6. Controls | Limit switches, position indication |
| 7. Standards | Applicable codes, certifications |
| 8. Notes | Special requirements, vendor options |

**Typical Sump Pump Data Sheet Structure:**

| Section | Content |
|---------|---------|
| 1. General | Tag, service, location |
| 2. Operating Conditions | Fluid, flow, head, temperature, NPSH |
| 3. Construction | Pump type, size, mounting |
| 4. Driver | Motor data, area classification |
| 5. Materials | Casing, impeller, shaft, seals |
| 6. Performance | Design point, curve reference |
| 7. Standards | Applicable codes, certifications |
| 8. Notes | Special requirements |

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|-------------|----------|----------|----------|-------------------|-------------------|--------------|
| — | No conflicts identified | — | — | — | — | — |

*Note: `_REFERENCES.md` is not yet populated with specific Employer's Requirements clauses. Conflicts may emerge when ER content is reviewed. Update this table as needed during WORKING_ITEMS sessions.*

**Cross-Document Consistency Check:**

| Check | Status |
|-------|--------|
| Datasheet equipment list matches Specification requirements | Verified — 32 arms, quick-connects, sump pump covered |
| Specification content requirements have fields in Datasheet | Verified — typical fields documented |
| Specification requirements have rationale in Guidance | Verified — considerations address all requirement categories |
| Specification requirements have verification in Procedure | Verified — Procedure.md steps include review and check |
| Data sheet parameters align with DEL-10.03 calculations | To be verified during execution |
| Terminology consistent across documents | Verified — consistent equipment naming |
