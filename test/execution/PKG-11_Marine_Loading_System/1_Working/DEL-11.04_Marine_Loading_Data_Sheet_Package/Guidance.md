# Guidance: DEL-11.04 Marine Loading Data Sheet Package

## Purpose

This guidance document supports the development of **Marine Loading Data Sheet Package** for **PKG-11 Marine Loading System**.

**Deliverable purpose:** Defines and substantiates marine loading equipment in accordance with Employer's Requirements (ER), providing the procurement basis and technical evaluation criteria for equipment selection and vendor qualification.

**Classification:** Data Sheet deliverable under the Process discipline, produced by the D&B Contractor.

**Objectives context (per decomposition Section 6):**
- **OBJ-1 Safe & Reliable Operation** — datasheets specify safety-critical parameters (ERC performance, leak detection sensitivity, hazardous area certification)
- **OBJ-2 Throughput Capacity** — datasheets define equipment capacity to support 1,000,000 MT/annum throughput
- **OBJ-4 Operational Flexibility** — datasheets specify operating ranges for diverse operating conditions
- **OBJ-7 Environmental Protection** — datasheets specify leak detection and containment equipment performance

## Principles

**Engineering rationale (Process discipline — equipment datasheets):**

1. **Procurement bridge:** Datasheets translate design requirements into procurement specifications that vendors can respond to. They must be unambiguous and based on controlled inputs.

2. **Design basis vs. vendor offered:** Datasheets should clearly distinguish between "required" values (from DEL-11.02/11.03) and "offered" values (from vendor data). This enables technical evaluation and compliance verification.

3. **Traceability:** Every design basis value should trace to DEL-11.02 (specification) or DEL-11.03 (calculations). Every vendor-offered value should reference the vendor document revision.

4. **Interface completeness:** Datasheets must capture all interface requirements (electrical, I&C, ESD, utilities) to enable coordination with adjacent packages.

**ASSUMPTION:** Applicable codes/standards and minimum requirements are defined by ER and project code register (to be referenced explicitly once available).

**Applicable standards context:**
- IEC 60079 series — hazardous area equipment certification — **TBD**
- API 610/682 — pump specifications (if applicable) — **TBD**
- Project datasheet templates — format and content — **TBD**

## Cross-Document Alignment Notes

| Alignment Check | Datasheet.md | Specification.md | Procedure.md |
|-----------------|--------------|------------------|--------------|
| Field structure | §Construction (field tables) | §Requirements (by item) | §Steps |
| Design basis source | §Conditions | §Related Deliverables | §Prerequisites |
| Interface requirements | §Interfaces | §Interface Requirements | §Steps (consistency) |
| Acceptance criteria | §Deliverable Acceptance | §Verification | §Verification |

**Cross-deliverable consistency:**
- Datasheet values must be consistent with DEL-11.02 Technical Specification
- Datasheet duty points must match DEL-11.03 Calculations
- Datasheet tags must match DEL-11.01 Drawing Set
- Datasheet revisions must be referenced by DEL-11.05 Test Records

Where required fields cannot be substantiated from controlled inputs or vendor data, mark them **TBD** (do not fill in "typical" values).

## Considerations

**Factors to consider during datasheet development:**

### Loading Arm Datasheet Considerations
- OEM data from DEL-11.06 may constrain available configurations
- ERC performance (release force, spillage) is safety-critical — verify against DEL-11.02 requirements
- Connection interface must accommodate design vessel range — verify against DEL-11.03 envelope
- Hazardous area certification requirements — coordinate with PKG-27

### Leak Detection Datasheet Considerations
- Detection philosophy must cover all potential leak paths (annulus, drip trays, sumps)
- Sensor technology affects maintenance requirements and reliability
- Alarm/trip setpoints balance early detection against nuisance alarms
- ESD integration requires coordination with PKG-19/PKG-29

### Sump Pump Datasheet Considerations
- Duty point (flow, head) must match DEL-11.03 drainage calculations
- Fluid properties may include canola oil contamination — verify material compatibility
- Hazardous area rating required for Zone 2 location (**ASSUMPTION**)
- Level control interface with leak detection system

### General Datasheet Quality
- Use consistent units (SI or project-specified)
- Use consistent terminology per project standards
- Cross-reference P&ID tag numbers from DEL-11.01
- Include clear revision control for both datasheet and referenced vendor data

## Trade-offs

**Competing concerns to evaluate:**

| Trade-off | Option A | Option B | Guidance |
|-----------|----------|----------|----------|
| Prescriptive vs. performance | Specify exact OEM model | Specify performance requirements | Performance-based preferred unless ER mandates specific OEM |
| Overdesign vs. optimization | Conservative ratings for margin | Optimize to design duty | Balance reliability against cost; document margin philosophy |
| Standardization vs. site-specific | Use project-standard equipment | Allow site-optimized selection | Prefer standardization where it meets ER; reduces spares complexity |
| Vendor flexibility vs. tight control | Allow vendor alternatives | Lock to specific model | Allow alternatives that meet performance; evaluate during procurement |

## Examples

**Reference examples and precedents:**

Anticipated datasheets (from decomposition):

| Datasheet | Key Content | Source Reference |
|-----------|-------------|------------------|
| Marine loading arm | Type, reach, ERC, materials, controls, electrical | DEL-11.06 OEM data, DEL-11.02 spec |
| Leak detection system | Sensor type, zones, alarm outputs, hazardous area | DEL-11.02 §6, PKG-19 interface |
| Sump pump | Duty point, materials, motor, hazardous area | DEL-11.03 drainage calc, PKG-20 interface |

**Datasheet structure (typical):**
1. Identification block (tag, service, location)
2. Design conditions block (pressure, temperature, product)
3. Equipment-specific blocks (by equipment type)
4. Interface block (electrical, I&C, ESD)
5. Hazardous area block (classification, certification)
6. Vendor data block (OEM, model, compliance)
7. Notes and attachments

**Employer's Requirements expectations:** **TBD** until clause references are provided.

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|-------------|----------|----------|----------|-------------------|-------------------|--------------|
| — | No conflicts identified at this stage | — | — | — | — | — |

*Note: Conflicts will be logged here when specific design basis values and vendor data become available and any discrepancies are identified.*

---

**Pass 3 Enrichment Notes (Final Quality Check):**
- Verified cross-document alignment table: All 4 alignment checks confirmed accurate
  - Field structure: Datasheet §Construction ↔ Specification requirements ↔ Procedure steps
  - Design basis source: Consistent DEL-11.02/11.03 references
  - Interface requirements: 6 interfaces in Datasheet, 4 INT requirements in Specification
  - Acceptance criteria: Align across all documents (6/5/7 items)
- Verified all 4 Principles link to procurement bridge, design basis, traceability, and interface completeness
- Verified 4 Considerations sections cover loading arm, leak detection, sump pump, and general quality
- Verified 4 Trade-offs reference appropriate procurement/selection decisions
- Verified Examples table lists 3 datasheets with source references
- Verified datasheet structure (7 block types) provides standard format
- Verified cross-deliverable consistency requirements: DEL-11.02, DEL-11.03, DEL-11.01, DEL-11.05 references
- Confirmed Conflict Table ready for use
- All TBDs and ASSUMPTIONs retained with explicit source citations
- Pass 3 complete — document ready for WORKING_ITEMS session
