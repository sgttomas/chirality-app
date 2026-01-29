# Guidance: DEL-29.02 Inspection and Test Plan With Hold/Witness Points

## Purpose

This guidance document supports the development of **Inspection and Test Plan With Hold/Witness Points** for **PKG-29 Testing**.

**Deliverable Purpose:** Defines the planned approach and controls for inspection and test plan with hold/witness points to meet ER requirements. **Source:** Decomposition line 647

This deliverable is classified as a **Plan** under the **T&C** discipline, to be produced by **D&B Contractor (QA/QC)**.

## Principles

### Quality Assurance Philosophy for ITPs

**Role of the ITP in Project Quality:**

The Inspection and Test Plan is a cornerstone document in EPC project quality management. It serves as:

1. **Quality Roadmap:** Defines "what gets inspected" and "when" across the entire project lifecycle
2. **Interface Agreement:** Documents the agreed inspection and witness requirements between Contractor and Employer
3. **Accountability Framework:** Establishes who is responsible for each inspection activity
4. **Traceability System:** Links design requirements → inspection activities → test records
5. **Risk Management Tool:** Focuses inspection resources on high-risk or high-consequence activities

**Source:** ISO 9001 quality management principles, typical EPC project practice **ASSUMPTION**

### Hold Point vs. Witness Point Philosophy

**Hold Point Rationale:**

Hold points are applied where:
- Proceeding without inspection would create unacceptable risk or irreversible consequences
- Code or regulatory requirements mandate inspection prior to proceeding
- Contract specifically requires Employer approval before next step
- Correction after the fact would be impractical or costly (e.g., concrete pour, backfill)

**Examples:** Tank bottom welding (must inspect before erecting shell), pressure boundary welding (must NDT before covering), concrete reinforcement (must inspect before pour)

**Witness Point Rationale:**

Witness points are applied where:
- Employer wants option to observe work but impact of non-attendance is manageable
- Inspection is important but not critical path (with proper notification)
- Contractor QC provides primary verification; Employer observation is for confidence/oversight
- Risk is moderate and Contractor has demonstrated competence in similar work

**Examples:** Pipe supports installation, cable pulling, instrument mounting, routine weld inspections (after initial qualification)

**Trade-off:** Too many hold points delay schedule; too few increase risk. ITPs balance rigor with practicality. **ASSUMPTION**

**Source:** Typical EPC hold/witness point selection criteria **ASSUMPTION**

### Project-Specific Context

**Project Objectives Alignment:**

This deliverable supports:
- **OBJ-1: Safe & Reliable Operation** — Quality verification ensures systems are safe
- **OBJ-6: Regulatory Compliance** — Inspection records provide evidence for authority approvals
- **OBJ-9: Lifecycle Cost Optimization** — Early defect detection reduces rework and future maintenance

**Source:** Decomposition Section 2 (lines 58-67), Section 6 Objective Mapping

**Facility Considerations:**
- Marine terminal environment: Emphasize corrosion protection inspections (coatings, cathodic protection)
- Food-grade product (canola oil): Emphasize cleanliness inspections for product-contact surfaces
- High throughput capacity: Emphasize metering accuracy and reliability inspections (custody transfer)
- Large storage tanks (3 × 15,000 MT): Emphasize tank construction and testing inspections per API 650

**Source:** Decomposition Section 1 (Project Context)

## Considerations

### Factors to Consider During ITP Development

**1. Scope and Coverage**
- Must capture all equipment, systems, and work activities requiring inspection
- Must align with project deliverable structure (PKG-01 through PKG-36)
- Must cover entire lifecycle (design, procurement, fabrication, construction, testing, commissioning)
- Must accommodate scope additions and changes as design matures

**2. Code and Regulatory Requirements**
- Identify all code-mandated inspections (ASME, API, AWS, CSA, etc.)
- Identify regulatory authority requirements (Transport Canada, fire marshal, building official, environmental)
- Identify third-party requirements (insurance surveyors, classification societies)
- **TBD** — Specific regulatory requirements as they are identified

**3. Employer Preferences and Risk Tolerance**
- Understand Employer's desired level of involvement in construction oversight
- Some Employers want high witness involvement; others rely more on Contractor QC with periodic audits
- Negotiate hold/witness points early to avoid disputes during construction
- Balance Employer oversight with schedule efficiency

**TBD** — Employer's Requirements **location TBD** should specify hold/witness point preferences

**4. Contractor QC Capabilities**
- Contractor with strong quality track record may receive fewer hold/witness points
- First-of-a-kind work or unproven sub-contractors may warrant more hold points
- FAT surveillance depends on vendor reputation and criticality of equipment
- **ASSUMPTION:** Contractor competence demonstrated through QC plan and qualifications

**5. Schedule and Logistics**
- Hold points create schedule dependencies on Employer availability
- Advance notification periods (48-72 hours typical) must accommodate Employer logistics
- Multiple hold points on critical path create cumulative delay risk
- Remote site locations may affect Employer's ability to witness

**6. Sub-Contractor and Vendor Coordination**
- Sub-contractors and vendors must understand ITP requirements
- Vendor quality plans must align with project ITP (FAT requirements, documentation)
- Sub-contractor quality plans must implement project ITP hold/witness points
- **TBD** — Sub-contractor and vendor coordination mechanisms

## Trade-offs

### Competing Concerns in ITP Development

**1. Inspection Rigor vs. Schedule Efficiency**

- **Trade-off:** More inspections and hold points improve quality confidence but slow progress
- **Consideration:** Prioritize hold points on high-risk, irreversible, or code-required activities
- **Recommendation:** Use witness points (not hold points) for routine inspections after Contractor demonstrates competence; reserve hold points for truly critical inspections **ASSUMPTION**

**2. Employer Involvement vs. Contractor Autonomy**

- **Trade-off:** High Employer involvement provides oversight but increases coordination burden and schedule risk
- **Consideration:** Employer's risk tolerance, Contractor's track record, and contract terms
- **Recommendation:** Negotiate balanced approach; Employer witnesses critical milestones and high-risk work; Contractor QC handles routine inspections with Employer audit rights **ASSUMPTION**

**3. Detailed ITP vs. Flexible ITP**

- **Trade-off:** Highly detailed ITP (line-by-line inspection activities) is comprehensive but rigid; high-level ITP is flexible but may have gaps
- **Consideration:** Design maturity, project complexity, and team experience
- **Recommendation:** Develop initial ITP at moderate detail level (system/major equipment), refine to detailed level as design and work packages mature; allow field adjustments for practical issues **ASSUMPTION**

**4. Single Master ITP vs. Multiple ITPs**

- **Trade-off:** Single master ITP document provides central control but becomes large and unwieldy (1000+ lines); multiple ITPs (by discipline or package) are manageable but require coordination
- **Consideration:** Project size and complexity
- **Recommendation:** For project of this scale (36 packages, ~210 deliverables), consider master ITP index with discipline/package sub-ITPs, all controlled through central document management **ASSUMPTION**

**5. Early Employer Acceptance vs. Progressive Development**

- **Trade-off:** Employer expects to review/accept ITP early; but ITP cannot be fully detailed until design is mature
- **Consideration:** Contract timing requirements vs. practical need for design information
- **Recommendation:** Issue initial ITP early for Employer acceptance of hold/witness principles and high-level coverage; issue updated ITPs progressively as design matures; establish change management process for ITP updates **ASSUMPTION**

## Examples

### ITP Structure Example

**Typical ITP Matrix Entry:**

| Item/System | Description | Spec/Dwg Ref | Inspection Activity | Acceptance Criteria | Responsible | H/W | Notification | Documentation | Status |
|-------------|-------------|--------------|---------------------|---------------------|-------------|-----|--------------|----------------|--------|
| TK-101 | Storage Tank #1 | API 650, Dwg M-101 | Tank bottom welding inspection | API 650 Sec 8, Visual + MT | Contractor QC + CWI | H | 48 hrs | Weld map, MT reports, photos | TBD |
| TK-101 | Storage Tank #1 | API 650, Dwg M-101 | Tank hydrostatic test | API 650 Sec 7, No leaks, max 5% pressure drop | Contractor QC + Engineer | H | 72 hrs | Hydro test report, pressure chart | TBD |
| P-201A | Transfer Pump | Dwg M-201, Spec MP-01 | Pump base grouting | Level within ±1mm, ACI 351 | Contractor QC | W | 24 hrs | Grout cert, level survey | TBD |

**Source:** Typical EPC ITP format **ASSUMPTION**

### Hold/Witness Point Selection Example

**Example System: Process Piping**

| Activity | Code Required? | Risk Level | Reversibility | Hold/Witness/Contractor | Rationale |
|----------|---------------|------------|---------------|------------------------|-----------|
| Pipe spool fabrication shop welding | Yes (ASME B31.3) | High | Difficult | H (first articles), W (production) | First articles verify welder qualification; production witness if Employer desires |
| Pipe spool NDT (RT/UT) | Yes (ASME B31.3) | High | Impossible after install | W | NDT by qualified third party; Contractor QC verifies; Employer may witness |
| Pipe support installation | No | Medium | Easy | Contractor | Routine work; Contractor QC adequate |
| Piping system hydrostatic test | Yes (ASME B31.3) | High | N/A | H | Code-required test; must pass before proceeding to commissioning |
| Pipe insulation installation | No | Low | Easy | Contractor | Cosmetic/performance; easy to correct |

**Source:** Typical piping inspection approach **ASSUMPTION**

### Inspection Matrix Example (Summary Format)

**Inspection Summary by Discipline:**

| Discipline | Total Inspections | Hold Points | Witness Points | Contractor Only | % Hold/Witness |
|------------|------------------|-------------|----------------|-----------------|---------------|
| Civil | 45 | 8 | 12 | 25 | 44% |
| Structural | 67 | 15 | 22 | 30 | 55% |
| Marine | 38 | 10 | 15 | 13 | 66% |
| Mechanical | 123 | 28 | 41 | 54 | 56% |
| Electrical | 56 | 8 | 18 | 30 | 46% |
| I&C | 72 | 10 | 25 | 37 | 49% |
| **Total** | **401** | **79** | **133** | **189** | **53%** |

**Note:** Numbers are illustrative for demonstration purposes **ASSUMPTION**

### Notification and Release Procedure Example

**Hold Point Notification and Release Process:**

1. **Contractor Notification:** Contractor provides written notification to Employer 48-72 hours (per ITP) prior to hold point activity
2. **Employer Confirmation:** Employer confirms receipt and plans to attend/release
3. **Pre-Inspection:** Contractor QC performs pre-inspection to verify readiness
4. **Inspection:** Employer representative and Contractor QC conduct inspection
5. **Release:** If acceptable, Employer provides written release (sign ITP, issue release form); if not acceptable, Employer issues non-conformance and holds release until corrected
6. **Proceed:** Contractor may proceed with next activity only after written release

**Witness Point Notification Process (typical):**

1. **Contractor Notification:** Contractor provides written notification per ITP advance notice period
2. **Employer Response:** Employer advises if witness will attend
3. **Inspection:** Contractor QC performs inspection; if Employer attends, Employer observes and may comment but does not formally release
4. **Proceed:** Contractor may proceed based on QC acceptance; if Employer does not attend after proper notification, work may proceed (per prior agreement)

**Source:** Typical EPC hold/witness procedures **ASSUMPTION**

**TBD:** Project-specific notification and release procedures per Employer's Requirements **location TBD**

## Conflict Table (for human ruling)

No conflicts identified during document development. If conflicts arise during ITP development (e.g., conflicting hold point requirements between codes and Employer, or between schedule and inspection requirements), they shall be documented here for resolution.

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|-------------|----------|----------|----------|-------------------|-------------------|--------------|
| — | — | — | — | — | — | **TBD** |
