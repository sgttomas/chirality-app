# Guidance: DEL-11.03 Marine Loading Design Calculations

## Purpose

This guidance document supports the development of **Marine Loading Design Calculations** for **PKG-11 Marine Loading System**.

**Deliverable purpose:** Provides the engineering basis and sizing/verification calculations for the marine loading system, demonstrating compliance with design requirements and deriving constraints for layout drawings and equipment specifications.

**Classification:** Calculation deliverable under the Process discipline, produced by the D&B Contractor.

**Objectives context (per decomposition Section 6):**
- **OBJ-1 Safe & Reliable Operation** — envelope calculations verify safe vessel approach and loading arm operation
- **OBJ-2 Throughput Capacity** — system sizing calculations support 1,000,000 MT/annum throughput
- **OBJ-4 Operational Flexibility** — envelope calculations confirm accommodation of diverse vessel types
- **OBJ-7 Environmental Protection** — drainage/containment calculations verify spill management capacity

## Principles

**Engineering rationale (Process discipline — marine loading calculations):**

1. **Traceability:** Every input value must have a documented source reference (ER clause, vendor data, adjacent deliverable). Every output that constrains the design must be explicitly communicated to drawings and specifications.

2. **Conservative assumptions:** Where inputs are not yet available, use conservative assumptions that bound the design space. Label these explicitly as **ASSUMPTION** and track to closure when actual inputs become available.

3. **Verifiable outputs:** Calculation results should be verifiable by independent check (arithmetic, methodology, reasonableness) and should produce clear constraints for layout and equipment selection.

4. **Sensitivity awareness:** Where results are sensitive to input assumptions, document the sensitivity and flag for early resolution of TBD inputs.

**ASSUMPTION:** Applicable codes/standards and acceptance criteria are defined by ER and project code register (to be referenced explicitly once available).

**Applicable standards context:**
- ASME B31.3 — pipe sizing (if applicable) — **TBD**
- Project calculation standards — format and content — **TBD**
- Project QA/QC procedures — check and approval — **TBD**

## Cross-Document Alignment Notes

| Alignment Check | Datasheet | Specification | Procedure |
|-----------------|-----------|---------------|-----------|
| Calculation topics | §Construction | §Requirements (ENV/DRN/N2) | §Steps |
| Design basis inputs | §Conditions | §Inputs tables | §Prerequisites |
| Output constraints | §Cross-Document Links | §Outputs lists | §Steps (Step 6) |
| Acceptance criteria | §Deliverable Acceptance | §Verification | §Verification |

**Cross-deliverable flow:**
- DEL-11.02 Technical Specification provides design basis inputs
- DEL-11.06 OEM Qualification provides loading arm envelope data
- Calculations produce constraints for DEL-11.01 drawings and verified values for DEL-11.04 datasheets

Where acceptance criteria are not available from ER/code register, keep them **TBD** and avoid "typical" defaults.

## Considerations

**Factors to consider during calculation development:**

### Loading Arm Envelope Considerations
- Vessel manifold height varies with vessel size and draft — account for full range
- Tidal variation affects relative vessel position — include in envelope analysis
- Fender compression at design berthing energy reduces clearance to platform edge
- ERC activation envelope must allow safe vessel drift without premature release or structural contact
- OEM arm geometry may constrain available configurations — coordinate with DEL-11.06

### Drainage Considerations
- Containment must accommodate design spill volume (ERC release) plus coincident rainfall
- Design storm return period should match project/ER requirements (typically 10-year or 25-year)
- Drainage discharge must route to oil-water separator or other approved treatment
- Sump pump capacity (if required) should empty containment in reasonable time post-event

### Nitrogen Purge Considerations
- Purge time affects vessel turnaround — balance against safety/inerting requirements
- Purge volume includes loading arm, header pipe, and any dead legs
- Target O₂ concentration depends on product and safety philosophy (typically <8% for inerting)
- Nitrogen supply must be sized for purge flow plus any continuous blanketing requirements

### General Calculation Quality
- Document tool/software versions for reproducibility
- Retain calculation files (spreadsheets, models) as project records
- Perform spot checks on software outputs to verify correctness
- Flag any results that appear counterintuitive for additional review

## Trade-offs

**Competing concerns to evaluate:**

| Trade-off | Option A | Option B | Guidance |
|-----------|----------|----------|----------|
| Conservative sizing vs. cost | Use maximum envelope for flexibility | Optimize to design vessel range | Balance flexibility (OBJ-4) against cost; confirm ER requirements |
| Preliminary vs. vendor-supported | Complete preliminary calcs with assumptions | Wait for vendor data | Complete preliminary calcs to inform layout; update with vendor data |
| Detail level vs. schedule | Detailed analysis for all scenarios | Bounding calculations for critical cases | Focus detail on safety-critical items (envelope, ERC); bound others |
| Sump size vs. pump capacity | Larger sump (passive storage) | Smaller sump with larger pump | Consider reliability, maintenance access, and failure modes |

## Examples

**Reference examples and precedents:**

Anticipated calculation deliverables (from decomposition):

| Calculation | Key Content | Source Reference |
|-------------|-------------|------------------|
| Loading arm envelope | Reach vs. vessel manifold position, slew/luff operating zone, clearance verification | DEL-11.06 OEM data, berth geometry |
| Drainage | Catchment area, design storm flow, sump sizing, pump sizing (if any) | Site data, DEL-11.02 spill volume |
| Nitrogen purge | System volume, purge flow, time to target O₂, supply capacity | DEL-11.02 purge philosophy, DEL-18 supply |

**Calculation format (typical structure):**
1. Purpose / Objective
2. References and governing codes
3. Inputs (with sources) and assumptions
4. Methodology (hand calc / spreadsheet / software)
5. Calculations and results
6. Conclusions and constraints for layout/specification
7. Appendices (raw data, software outputs)

**Employer's Requirements expectations:** **TBD** until clause references are provided.

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|-------------|----------|----------|----------|-------------------|-------------------|--------------|
| — | No conflicts identified at this stage | — | — | — | — | — |

*Note: Conflicts will be logged here when specific input data becomes available and any discrepancies between sources (e.g., ER vs. OEM data) are identified.*
