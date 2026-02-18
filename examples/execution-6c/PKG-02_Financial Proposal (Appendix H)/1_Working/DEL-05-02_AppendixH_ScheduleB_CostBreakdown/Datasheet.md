# Datasheet: DEL-05-02 AppendixH ScheduleB CostBreakdown

## Identification

| Attribute | Value |
|-----------|-------|
| **Deliverable ID** | DEL-05-02 |
| **Name** | AppendixH ScheduleB CostBreakdown |
| **Type** | Financial Document |
| **Package** | PKG-02 Financial Proposal (Appendix H) |
| **Discipline** | Commercial / Estimating |
| **Responsible** | Estimator / Commercial Lead |
| **Status** | OPEN |
| **Source** | _CONTEXT.md |

## Attributes

### Document Properties

| Property | Value | Source |
|----------|-------|--------|
| **Template** | Appendix H Schedule B (RFP template) | RFP Section 4.3; _REFERENCES.md |
| **Template Location** | **[Lensing B-006]** TBD — Obtain from _Sources/ directory or Proposal Manager; RFP Section 4.3 | RFP Section 4.3 |
| **Format** | **[Lensing B-006]** TBD — If Excel: linked formulas enable reconciliation; If PDF: manual reconciliation required | ASSUMPTION: Standard RFP pricing form |
| **Evaluation Weight** | 35 points (Proposal Price category) | Decomposition Section 15 |
| **Compliance Level** | Mandatory | Decomposition Section 3 (C-05) |

### Cost Categories Required

| Category | Description | Source |
|----------|-------------|--------|
| **General Requirements** | Project management, supervision, mobilization, temporary facilities | Decomposition Section 8 (DEL-05-02); ASSUMPTION: CSI Division 01 |
| **Building** | Building construction costs by trade/system | Decomposition Section 8 (DEL-05-02); ASSUMPTION: CSI Divisions 02-16 |
| **Sitework** | Site development, utilities, grading, paving | Decomposition Section 8 (DEL-05-02); ASSUMPTION: CSI Division 02 (site) + 33 (utilities) |
| **Additional Options 1-6** | Separate line items for each optional scope | Decomposition Section 5 (Vocabulary Map); Section 8 (DEL-05-02) |

### Addendum 03 Technical Items — Cost Line Treatment

**[Lensing B-001]** The following Addendum 03 technical requirements require clarification on cost line treatment:

| Technical Item | Treatment | Line Item Location | Status |
|---------------|-----------|-------------------|--------|
| **Overhead doors (16 ft height)** | TBD: Separate line item or rolled into Building Systems | Building > Specialties OR Building > Openings | ASSUMPTION: Include in Building (2.8 Specialties) |
| **Bay sumps (apparatus bays)** | TBD: Separate line item or rolled into Plumbing | Building > Plumbing OR Building > Specialties | ASSUMPTION: Include in Building (2.5 Mechanical) |
| **Fire apparatus exhaust system** | TBD: Separate line item or rolled into Fire Protection | Building > Fire Protection OR Building > Mechanical | ASSUMPTION: Include in Building (2.7 Fire Protection) |
| **Emergency generator** | TBD: Separate line item or rolled into Electrical | Building > Electrical | ASSUMPTION: Include in Building (2.6 Electrical) |
| **Fill stations (apparatus fill)** | TBD: Separate line item or rolled into Specialties | Building > Specialties | ASSUMPTION: Include in Building (2.8 Specialties) |
| **Solar-ready provisions** | TBD: Separate line item or rolled into Electrical | Building > Electrical | ASSUMPTION: Include in Building (2.6 Electrical) |

**Source:** Decomposition Section 4 (Addendum 03 impacts); Procedure.md Step 2
**Action Required:** Confirm with Design Lead and Appendix H template whether items require separate line item visibility or can be aggregated into building system costs.

### Additional Options (line items required)

**[Lensing B-005]** Special requirements populated for comprehensive reporting:

| Option # | Description | Special Requirement | Operating Cost Component | Source |
|----------|-------------|---------------------|-------------------------|--------|
| **Option 1** | Built-in wash bay | Capital cost only; confirm wash bay system scope (in-ground vs. above-grade, water treatment, drainage) with Design Lead | None anticipated | Decomposition Section 5 (Vocabulary Map) |
| **Option 2** | Yard lighting | Capital cost only; confirm fixture count and coverage area with Civil/Electrical Lead | Potential energy cost (excluded from pricing; operating budget item) | Decomposition Section 5 (Vocabulary Map) |
| **Option 3** | Building access control | Capital cost only; confirm door count and system type (card reader, keypad, biometric) with Design Lead | Potential maintenance/software subscription (TBD if required) | Decomposition Section 5 (Vocabulary Map) |
| **Option 4** | Security/cameras | Monitoring fee must be separated; confirm camera count and coverage with Design Lead | **Monitoring fee (annual/monthly)** — MUST be separated as distinct line item | Decomposition Section 5 (Vocabulary Map); Section 8 (DEL-05-02) |
| **Option 5** | Exterior signage (branding) | Capital cost only; confirm sign type (illuminated/non-illuminated), size, and Town branding requirements | Potential maintenance (excluded; operating budget item) | Decomposition Section 5 (Vocabulary Map) |
| **Option 6** | Appliances | Capital cost only; confirm appliance list (refrigerator, stove, microwave, dishwasher, washer/dryer) with Design Lead | None anticipated | Decomposition Section 5 (Vocabulary Map) |

**Source:** Decomposition Section 5 (Vocabulary Map); Guidance.md Principle 4 (capital vs. operating costs)

## Conditions

### Scope Constraints

| Constraint | Implication | Source |
|------------|-------------|--------|
| **Pickled sand storage building removed** | Exclude from base cost | Decomposition Section 4 (Addendum 03 impacts) |
| **12-acre developable site** | Site costs limited to 12 acres (20 acres total; 8 acres dog park/storm pond in flood fringe) | Decomposition Section 4 (Addendum 03 impacts) |
| **Service tie-ins allowance approach** | Allowance permitted for service connections | Decomposition Section 12 (OI-003 resolved) |
| **FF&E treatment** | FF&E may be included as additional item, NOT in base cost | Decomposition Section 4 (Addendum 03 impacts); Section 12 (OI-004 OPEN) |

### Reconciliation Requirements

| Requirement | Description | Source |
|-------------|-------------|--------|
| **Totals match Schedule A** | Schedule B detailed breakdown must sum to Schedule A totals | Decomposition Section 8 (DEL-05-02 acceptance criteria); _CONTEXT.md |
| **Addenda acknowledgement** | Appendix H includes addenda acknowledgement line; failure may disqualify price proposal | Decomposition Section 3 (C-07) |
| **Completeness** | All required cost categories and line items must be present | Decomposition Section 8 (DEL-05-02 acceptance criteria); _CONTEXT.md |

## Construction

### Expected Cost Breakdown Structure

**[Lensing B-002]** The following structure is ASSUMED pending access to RFP Appendix H template. Actual template structure governs and may supersede this structure.

**ASSUMPTION:** Standard CSI MasterFormat-based structure expected, with the following breakdown logic:

| Level | Category | Sub-categories (typical) | Line Item Examples |
|-------|----------|--------------------------|-------------------|
| **1** | General Requirements | Project management, superintendence, mobilization/demobilization, temporary facilities, project closeout | 1.1–1.4 per Guidance.md Example |
| **2** | Building | Foundation, structure, envelope, roofing, interior finishes, mechanical, electrical, plumbing, fire protection, specialties | 2.1–2.8 per Guidance.md Example |
| **3** | Sitework | Earthwork, grading, utilities (water, sanitary, storm), paving, landscaping, site lighting (base scope) | 3.1–3.5 per Guidance.md Example |

**Granularity Guidance [Lensing B-003, C-003]:** Three potential structures exist in documentation:
1. **Datasheet (3 categories):** General Requirements, Building, Sitework
2. **Guidance.md Example (subdivisions):** Numbered line items 1.1–3.5
3. **Actual RFP Appendix H template:** TBD — **THIS GOVERNS**

**Action Required:** Obtain Appendix H template from RFP Section 4.3 and align all documents to actual template structure. If template permits flexibility, use minimum 3-level hierarchy (Category > Subcategory > Line Item) per Guidance.md Example to support evaluation scoring.

**Source:** Decomposition Section 8 (DEL-05-02); Decomposition Section 15 (35 points Proposal Price); _SEMANTIC_LENSING.md (B-002, B-003, C-003)

### Cost Allocation Logic (ASSUMPTION)

| Allocation Rule | Description |
|-----------------|-------------|
| **Direct costs** | Labor, material, equipment costs assigned to specific work items |
| **Indirect costs** | Overhead, profit, contingency (may be percentage-based or lump sum) |
| **Taxes** | Separated per RFP requirement (see DEL-05-01 Schedule A) |
| **Monitoring fee** | Separated line item for Option 4 only (security/cameras monitoring service) |

## References

| Reference | Location | Relevance |
|-----------|----------|-----------|
| **_CONTEXT.md** | Deliverable folder | Deliverable identity, acceptance criteria |
| **Decomposition document** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/_Decomposition/Penhold_PSB_Project_Decomposition_Final_AddendumIntegrated_v1.md | Deliverable definition (Section 8, DEL-05-02); constraints (Section 4); vocabulary (Section 5); evaluation criteria (Section 15) |
| **RFP Appendix H** | _Sources/AB-2024-07156-Penhold Public Services Building RFP_2024_004.pdf (location TBD) | Pricing template form and instructions |
| **Addendum 03** | _Sources/AB-2024-07156-Penhold_Public Services Building Addendum03.pdf (location TBD) | Scope removals, site clarifications, pricing approach guidance |
| **_REFERENCES.md** | Deliverable folder | Reference material index |

## Cross-References

| Related Document | Relationship | Key Links |
|------------------|--------------|-----------|
| **Specification.md** | Requirements governing this deliverable | R-001 to R-010 define mandatory characteristics of Schedule B |
| **Guidance.md** | Engineering rationale and principles | Principles 1-5 inform cost breakdown approach; Trade-offs guide estimating decisions |
| **Procedure.md** | Production workflow | Steps 1-6 describe how to produce Schedule B; Prerequisites list required inputs |
| **DEL-05-01 (Schedule A)** | Upstream summary pricing | Schedule B totals must reconcile to Schedule A (see Specification.md R-005) |
| **DEL-05-03 (Pricing Narrative)** | Supporting assumptions documentation | Assumptions and exclusions must be consistent (see Guidance.md coordination section) |

---

**Document Status:** Pass 3 (Semantic Lensing Enrichment)
**Last Updated:** 2026-02-04
**Lensing Items Incorporated:** B-001, B-002, B-003, B-005, B-006, C-003
**Completeness:** Base structure established; cross-references added; lensing enrichments added for technical item costing, Additional Options special requirements, format clarification, and cost structure consistency. TBD items require access to Appendix H template form and detailed project scope/quantity information.
