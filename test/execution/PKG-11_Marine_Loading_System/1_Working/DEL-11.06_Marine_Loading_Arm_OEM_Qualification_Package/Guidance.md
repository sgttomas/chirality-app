# Guidance: DEL-11.06 Marine Loading Arm OEM Qualification Package

## Purpose

This guidance document supports the development of **Marine Loading Arm OEM Qualification Package** for **PKG-11 Marine Loading System**.

**Deliverable purpose:** Defines and substantiates marine loading arm OEM qualification in accordance with Employer's Requirements (ER), demonstrating OEM capability, product compliance, and suitability for the project prior to procurement commitment.

**Classification:** Document Package under the Process discipline, produced by the D&B Contractor with OEM/Supplier input.

**Objectives context (per decomposition Section 6):**
- **OBJ-1 Safe & Reliable Operation** — OEM qualification verifies safety-critical equipment meets quality standards
- **OBJ-2 Throughput Capacity** — OEM capability verification ensures design capacity can be delivered
- **OBJ-4 Operational Flexibility** — OEM envelope data confirms operational flexibility requirements
- **OBJ-7 Environmental Protection** — OEM compliance verifies ERC and containment features

## Principles

**Engineering rationale (Process discipline — OEM qualification):**

1. **Risk reduction:** The purpose of OEM qualification is to reduce procurement and technical risk by verifying OEM capability and product compliance before commitment. This avoids costly changes later.

2. **Structured submission:** The package should be structured so reviewers can quickly find: (a) OEM capability evidence, (b) compliance statements with deviations, and (c) substantiating documentation.

3. **Transparency on deviations:** All deviations/exceptions must be explicitly listed — not buried in footnotes or technical data. Silent departures from requirements create hidden risk.

4. **Comparable references:** References should genuinely match the application — same product type, similar service, similar environment. Generic terminal references may not demonstrate vegetable oil experience.

**ASSUMPTION:** ER defines any mandatory OEM prequalification criteria (clause references **TBD**).

**Applicable standards context:**
- OCIMF Guidelines — marine loading arm design guidance — **TBD**
- ISO 9001 — OEM quality management system certification — required
- IEC 60079 series — hazardous area equipment certification — **TBD**

## Cross-Document Alignment Notes

| Alignment Check | Datasheet.md | Specification.md | Procedure.md |
|-----------------|--------------|------------------|--------------|
| Package contents | §Construction | §Requirements (QUAL/REF/COMP/DOC) | §Steps |
| OEM data items | §Interfaces | §Interface Requirements | §Steps (data collection) |
| Acceptance criteria | §Deliverable Acceptance | §Verification | §Verification |
| Deviation handling | §Deliverable Acceptance | §Quality Requirements | §Steps (deviation review) |

**Cross-deliverable data flow:**
- OEM envelope data must be carried into DEL-11.01 drawings (reach, slew, luff limits)
- OEM compliance/deviations must be reflected in DEL-11.02 extent of supply
- OEM-offered values populate DEL-11.04 datasheets (vendor data block)
- OEM FAT procedures inform DEL-11.05 test records

Any OEM-stated limits or deviations should be visible wherever they affect design, procurement, or verification — not isolated in the OEM package alone.

## Considerations

**Factors to consider during package development:**

### OEM Qualification Considerations
- Verify OEM has genuine manufacturing capability (not reseller/agent)
- Verify quality system certification is current and relevant scope
- Verify design capability includes marine loading arm engineering (not just fabrication)
- Verify after-sales support is available for project location

### Comparable Reference Considerations
- References should match product type (powered marine loading arm with ERC)
- References should include similar product service (vegetable oils preferred; liquid bulk acceptable)
- References should include similar environment (marine, coastal, similar climate)
- Verify reference clients are willing to provide feedback (if contact is needed)

### Compliance Statement Considerations
- Develop compliance matrix against DEL-11.02 requirements (when available)
- Identify any ER clauses that cannot be met exactly — list as deviations
- Ensure hazardous area certification matches project Zone classification
- Verify type testing covers the proposed product configuration

### Deviation Management Considerations
- Deviations are not automatically rejections — they require evaluation and disposition
- Some deviations may be acceptable with design changes or operating restrictions
- Critical deviations (safety, capacity) require explicit Employer acceptance
- Track all deviations in project deviation register

## Trade-offs

**Competing concerns to evaluate:**

| Trade-off | Option A | Option B | Guidance |
|-----------|----------|----------|----------|
| Single OEM vs. competition | Prequalify single preferred OEM | Prequalify multiple OEMs for competition | Multiple OEMs reduce risk; confirm ER allows single-source |
| Standard product vs. custom | Accept OEM standard configuration | Require project-specific modifications | Prefer standard product where it meets ER; reduces lead time and cost |
| Early vs. late qualification | Qualify OEM before detailed design | Qualify during procurement | Early qualification reduces design iteration risk |
| Strict compliance vs. deviation acceptance | Reject OEMs with any deviation | Evaluate deviations on merit | Evaluate deviations; some may be acceptable with mitigation |

## Examples

**Reference examples and precedents:**

Anticipated package structure (from decomposition):

| Section | Key Content | Source Reference |
|---------|-------------|------------------|
| OEM qualification | Company profile, manufacturing, QA, design capability | OEM submission |
| Comparable references | 3+ relevant projects with dates, clients, scope | OEM submission |
| Compliance statements | ER matrix, code compliance, deviation register | OEM + Contractor review |
| Supporting documentation | Brochures, GA drawings, datasheets, certificates | OEM submission |

**Typical deviation register format:**

| Dev ID | Requirement | OEM Position | Impact | Proposed Disposition | Status |
|--------|-------------|--------------|--------|---------------------|--------|
| D-001 | Example requirement | Partial compliance | Minor | Accept with clarification | **TBD** |
| D-002 | Example requirement | Non-compliant | Major | Design change required | **TBD** |

**Employer's Requirements expectations:** **TBD** until clause references are provided.

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|-------------|----------|----------|----------|-------------------|-------------------|--------------|
| — | No conflicts identified at this stage | — | — | — | — | — |

*Note: Conflicts will be logged here when OEM submissions are received and any discrepancies between OEM capabilities and ER/specification requirements are identified.*
