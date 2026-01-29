# Guidance: DEL-13.06 Storage Tank Fabrication Quality Documentation Package

## Purpose

This guidance document supports the development of **Storage Tank Fabrication Quality Documentation Package** for **PKG-13 Storage Tanks**.

### Deliverable Context

**Description:** Defines and substantiates storage tank fabrication quality documentation package in accordance with ER requirements.

**Source:** _CONTEXT.md, Decomposition document DEL-13.06

This deliverable is classified as a **Document Package** under the **Mechanical** discipline, to be produced by **D&B Contractor**.

### Role in Project Delivery

The fabrication quality documentation package demonstrates that:
1. **Fabricator is qualified** to fabricate API 650 tanks per applicable standards
2. **Welding procedures are qualified** and adequate for materials and joint configurations used
3. **Welders are qualified and competent** to perform production welding
4. **Materials conform** to specifications as evidenced by mill test reports and impact tests
5. **Fabrication conforms** to design and specifications as evidenced by shop inspections and weld inspections
6. **Welds meet quality standards** as evidenced by NDE during fabrication

This package is **pre-qualification and process documentation**, complementing the **installation and test records** (DEL-13.05) which document the final as-built product. Together, these deliverables provide complete quality assurance coverage from fabricator selection through testing.

**Source:** Typical fabrication quality documentation purpose

### Downstream Use

- **D&B Contractor Quality Assurance:** Verifies fabricator capability and process quality before and during fabrication
- **Client Review:** Client reviews fabricator qualifications and procedures before fabrication begins; reviews shop inspections during fabrication
- **Regulatory Compliance:** Authorities may require fabrication quality documentation for permit compliance
- **Future Reference:** Welding procedures and material data provide baseline for future repairs or modifications
- **Dispute Resolution:** Documentation provides objective evidence if quality disputes arise

**Source:** Typical fabrication quality documentation downstream use

---

## Principles

### Design Principles

**DP-01: Fabricator Qualification Philosophy**

API 650 tanks are pressure-retaining equipment requiring specialized fabrication capability. Not all steel fabricators are qualified to fabricate API 650 tanks.

**Key principle:** Fabricator shall demonstrate qualification **before** fabrication begins through:
- Shop quality system (CSA W47.1 certification, ISO 9001, or equivalent)
- API 650 experience (references from previous projects)
- Welding capability (qualified welders and procedures)
- Shop audit by D&B Contractor (verify equipment, processes, quality controls)

Do not assume fabricator is qualified. Verify through documented evidence.

**Source:** API 650 fabricator requirements; typical fabricator pre-qualification practice

**DP-02: Welding Procedure Qualification**

Welding is the critical fabrication activity for API 650 tanks. Welds must have adequate strength, ductility, and toughness. Unqualified welding procedures or unqualified welders result in defective welds that may fail in service.

**Qualification hierarchy:**
1. **Procedure Qualification (PQR → WPS):** Test welds are made using trial parameters; destructive tests verify weld quality; if tests pass, parameters are documented in WPS for production use
2. **Welder Qualification (WPQ):** Individual welder makes test welds using qualified WPS; tests verify welder skill; if tests pass, welder is qualified to use that WPS in production
3. **Production Welding:** Qualified welders use qualified WPS to make production welds; NDE verifies production weld quality

**Key principle:** No production welding occurs until procedures and welders are qualified. Qualification is proactive (demonstrate capability before production), not reactive (test production welds and hope they pass).

**Source:** API 650 Section 8.2; CSA W59 Section 5 and 6 welding qualification philosophy

**DP-03: API 650 and CSA W59 Compliance Documentation**

API 650 and CSA W59 specify documentation requirements to ensure fabrication quality. These are **mandatory** documentation requirements, not optional:

| API 650/CSA W59 Requirement | Documentation Evidence |
|-----------------------------|------------------------|
| Section 8.2 / 5: Procedures qualified | WPS and PQR |
| Section 8.2.5 / 6: Welders qualified | WPQ |
| Section 2.2: Materials meet specifications | MTRs and impact test results |
| Section 8: Welds examined and accepted | NDE reports and weld inspection records |
| Section 8: Fabrication conforms to design | Shop inspection reports |

**Key principle:** Fabrication quality documentation is not "paperwork" — it is objective evidence of code compliance. Missing or deficient documentation indicates non-compliance.

**Source:** API 650 and CSA W59 quality documentation requirements

**DP-04: Overlap with Installation & Test Records (DEL-13.05)**

Some documents appear in both fabrication quality documentation package (DEL-13.06) and installation & test records (DEL-13.05):
- **MTRs:** Included in both (material procurement evidence in DEL-13.06; installation traceability in DEL-13.05)
- **NDE reports:** Included in both (fabrication process quality in DEL-13.06; installation acceptance evidence in DEL-13.05)

**Key principle:** Overlap is acceptable and typical. The two deliverables serve different purposes:
- **DEL-13.06:** Demonstrates fabricator capability and fabrication process quality
- **DEL-13.05:** Demonstrates final as-built product quality and acceptance

Some records (like MTRs and NDE reports) support both purposes.

**Source:** Typical documentation structure for fabricated equipment

**DP-05: Timing: Pre-Fabrication Approval Critical**

WPS/PQR/WPQ must be approved **before fabrication begins**. If fabrication starts with unqualified procedures or welders, all work may be defective and require rework or rejection.

**Key principle:** Establish clear pre-fabrication hold point in ITP (DEL-29.02). Fabricator shall not begin welding until WPS/PQR/WPQ are reviewed and approved by D&B Contractor. This is a **quality gate**, not administrative paperwork.

**Source:** Typical welding qualification workflow and ITP practice

---

## Considerations

### Factors to Consider During Development

**C-01: Fabricator Selection and Qualification Timing**

Fabricator must be selected early enough to develop and qualify welding procedures before fabrication schedule begins.

**Typical timeline:**
- Fabricator selection: 4-6 months before fabrication start
- WPS/PQR/WPQ development and qualification: 2-3 months (includes test coupon welding, testing, review, approval)
- Shop audit (if required): 1 month before fabrication start

**TBD** — Project schedule for fabricator selection and qualification

**Key consideration:** Early fabricator selection enables early procedure qualification. Delayed fabricator selection compresses procedure qualification into fabrication schedule, increasing risk.

**Source:** Typical tank fabrication procurement schedule

**C-02: Canadian Project: CSA Standards vs. API Standards**

This project is located in Canada (Surrey, BC). Canadian fabricators typically work to CSA standards (CSA W59, CSA W47.1) rather than (or in addition to) AWS standards.

**Key consideration:** Determine applicable welding standards early:
- **API 650 alone:** U.S. fabricators typically follow API 650 welding requirements (which reference AWS)
- **API 650 + CSA W59:** Canadian fabricators typically follow API 650 design requirements but CSA W59 welding requirements
- **Fabricator certification:** Canadian fabricators typically have CSA W47.1 certification rather than ASME certification

**TBD** — Applicable welding standards per ER and project specification (DEL-13.02)

**ASSUMPTION** in this document: CSA W59 and CSA W47.1 are applicable for Canadian project

**Source:** Typical Canadian vs. U.S. welding standard practice

**C-03: Impact Testing Applicability**

Impact testing is required for materials subject to low-temperature service or seismic loading per API 650.

**Typical applicability:**
- **Operating temperature:** If tank operates below -29°C, impact tests are required per API 650 Section 2.2.11
- **Seismic design:** If tank is designed per API 650 Appendix E (seismic), impact tests may be required for anchorage and shell materials

**Key consideration:** Determine impact testing applicability early (before material procurement). Impact testing requires specific material heat treatment and test specimens, which must be specified in material purchase orders.

**TBD** — Operating temperature and seismic design requirements per ER and design (DEL-13.03)

**Source:** API 650 Section 2.2.11; API 650 Appendix E

**C-04: Shop Inspection Frequency and Scope**

Shop inspections can be:
- **Full-time resident inspector:** Inspector on-site daily during fabrication (highest assurance, highest cost)
- **Periodic inspections:** Inspector visits shop weekly or at milestones (balanced assurance and cost)
- **Remote inspections:** Inspector reviews fabricator's records remotely with occasional site visits (lowest cost, lower assurance)

**Key consideration:** Determine inspection frequency and scope based on:
- Fabricator experience and track record
- Tank criticality (large capacity, seismic zone, environmental sensitivity)
- Client requirements
- Project budget

**TBD** — Shop inspection frequency and scope per project quality plan

**Source:** Typical shop inspection options

**C-05: Third-Party Inspection vs. D&B Contractor Self-Inspection**

Shop inspections can be performed by:
- **D&B Contractor QA staff:** Lower cost, faster communication, potential perception of conflict of interest
- **Third-party inspection agency:** Independent, higher credibility, higher cost, potential communication delays

**Key consideration:** Determine inspection party based on client requirements and project risk. Many clients require third-party inspection for critical equipment.

**TBD** — Inspection party requirements per ER

**Source:** Typical shop inspection party selection

**C-06: Documentation Submittal Timing**

Fabrication quality documentation can be submitted:
- **Pre-fabrication (WPS/PQR/WPQ):** Required for approval before fabrication begins
- **During fabrication (shop inspection reports, MTRs, NDE reports):** Submitted progressively as work proceeds; allows early identification of issues
- **Post-fabrication (complete package):** Submitted after fabrication complete; delayed feedback if issues exist

**Recommendation:** Progressive submittal during fabrication preferred. Early submission of shop inspection reports and NDE reports enables early issue identification and resolution.

**TBD** — Documentation submittal timing per project procedures and ER

**Source:** Typical fabrication documentation submittal practice

**C-07: Interface with Installation & Test Records (DEL-13.05)**

Fabrication quality documentation (DEL-13.06) feeds into installation & test records (DEL-13.05):
- WPS numbers from DEL-13.06 are referenced on weld maps in DEL-13.05
- Welder qualifications (WPQ) from DEL-13.06 are verified against weld map welder IDs in DEL-13.05
- MTRs and NDE reports are included in both deliverables (different purposes)

**Key consideration:** Establish consistent numbering and referencing between DEL-13.06 and DEL-13.05. WPS numbers and welder IDs shall be unique and traceable.

**Source:** Typical documentation interface between fabrication quality and installation records

---

## Trade-offs

### Competing Concerns to Evaluate

**T-01: Fabricator Pre-Qualification Depth: Shop Audit vs. Document Review**

**Trade-off:**
- **Shop audit (site visit to fabricator):** Verifies equipment, processes, personnel capability in person; highest assurance; requires travel time and cost
- **Document review only (review fabricator certifications and references):** Faster, lower cost; lower assurance (paper qualifications may not reflect current capability)

**Recommendation:** Shop audit recommended for first-time fabricators or critical tanks. Document review acceptable for established fabricators with strong track record on similar projects.

**TBD** — Fabricator pre-qualification approach per project risk assessment

**Source:** Typical fabricator qualification practice

**T-02: Welding Procedure Qualification: API 650 vs. CSA W59**

**Trade-off:**
- **API 650 alone:** Simpler if U.S. fabricator with AWS-qualified procedures; may not satisfy Canadian regulatory requirements
- **CSA W59 alone:** Satisfies Canadian requirements; may require re-qualification if fabricator has AWS procedures only
- **Both (API 650 design + CSA W59 welding):** Satisfies both API 650 design intent and Canadian welding standards; requires fabricator to have or develop CSA W59 qualified procedures

**Recommendation:** For Canadian project, specify API 650 design with CSA W59 welding requirements. This is standard practice for Canadian API 650 tank projects.

**TBD** — Applicable welding standards per ER and project specification (DEL-13.02)

**Source:** Typical Canadian API 650 tank project welding standard approach

**T-03: Shop Inspection Frequency: Full-Time vs. Periodic**

**Trade-off:**
- **Full-time resident inspector:** Maximum oversight, early issue detection, higher cost, may slow fabricator productivity (inspection delays)
- **Periodic inspection (weekly):** Balanced oversight and cost, some risk of issues not detected until periodic visit
- **Milestone inspection only:** Lowest cost, higher risk of issues not detected until late in fabrication

**Recommendation:** Periodic inspection (weekly) typically provides good balance. Full-time inspection justified for very large or critical tanks. Milestone inspection acceptable only for low-risk tanks with highly experienced fabricators.

**TBD** — Inspection frequency per project quality plan and risk assessment

**Source:** Typical shop inspection frequency selection

**T-04: NDE Extent During Fabrication: Spot vs. Full**

**Trade-off:**
- **Spot examination per API 650:** Lower cost, meets code minimum, some defects may be missed
- **Full examination (100% NDE):** Higher cost, maximum defect detection, high confidence in weld quality

**Key consideration:** Fabrication NDE (DEL-13.06) demonstrates fabrication process quality. Final NDE (DEL-13.05) provides final acceptance evidence. The two serve different purposes.

**Recommendation:** Follow API 650 spot examination requirements during fabrication unless fabricator has known quality issues. Full examination can be performed during final acceptance (DEL-13.05) if desired.

**TBD** — Fabrication NDE extent per project specification (DEL-13.02)

**Source:** API 650 Section 8.1; typical fabrication vs. final NDE practice

---

## Examples

### Reference Examples and Precedents

**Example 1: WPS Typical Content**

Typical WPS includes:
- WPS Number: WPS-001
- Base Metal: ASTM A36 plate, 6mm to 25mm thickness
- Filler Metal: AWS E7018 electrode (SMAW process)
- Welding Process: SMAW (Shielded Metal Arc Welding)
- Joint Design: Single-V groove, full penetration
- Preheat: Not required for ASTM A36 at room temperature; 100°C minimum if ambient below 0°C
- Interpass Temperature: 250°C maximum
- PWHT: Not required
- PQR Reference: PQR-001

**Source:** Typical SMAW WPS for carbon steel plate

**Example 2: PQR Typical Test Results**

Typical PQR includes test coupon welding parameters and test results:
- **Welding parameters actually used:** Electrode size 4mm, current 140A, voltage 24V, travel speed 150mm/min
- **Test results:**
  - Visual examination: Acceptable (no undercut, porosity, or cracks)
  - Radiographic examination: Acceptable per API 650 Section 8.2.2.2
  - Tensile test: Ultimate strength 520 MPa (exceeds base metal minimum 400 MPa)
  - Guided bend test: 4 specimens (2 face, 2 root), all passed (no cracks exceeding 3mm)
  - **Acceptance:** PQR qualifies WPS-001 per API 650 Section 8.2.4

**Source:** Typical PQR test results for carbon steel

**Example 3: Shop Inspection Report Scenario**

**Scenario:** D&B Contractor inspector visits fabricator shop on Week 3 of fabrication. Inspector observes:
- Shell course 1 for Tank TK-101 completed; shell course 2 in progress
- Welding performed by welders W-01, W-02, W-03 (all qualified per WPQ records)
- WPS-001 used for shell vertical seams (correct per design)
- Visual inspection of completed welds shows good quality (no visible defects)
- Shop cleanliness good; materials organized and labeled
- **Non-conformance identified:** One shell plate heat number not matching material requisition. Fabricator to verify MTR and correct if needed.

**Shop inspection report documents observations and non-conformance. Follow-up inspection verifies non-conformance closure (MTR verified correct, label error only).**

**Lesson:** Shop inspections provide real-time feedback and early issue detection. Non-conformance was minor and quickly resolved because it was caught during fabrication.

**Source:** Typical shop inspection scenario

**Example 4: WPQ Test Failure Scenario**

**Scenario:** Welder W-05 performs WPQ test for GMAW process, 1G position (flat). Bend test shows cracks exceeding 3mm in root bend specimens (failure per API 650 Section 8.2.5).

**Resolution:**
- Welder W-05 does not pass qualification; WPQ test record documents failure
- Root cause: Welder unfamiliar with GMAW process (experienced in SMAW only)
- Corrective action: Welder W-05 receives additional GMAW training and practice; re-tests after 2 weeks
- Re-test: Welder W-05 passes WPQ on second attempt; qualified for GMAW 1G position

**Lesson:** Welder qualification tests serve their purpose — identify welders who need additional training before they perform production welding. Failure is an acceptable outcome; it prevents defective production welds.

**Source:** Typical WPQ test failure and resolution scenario

---

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|-------------|----------|----------|----------|-------------------|-------------------|--------------|
| CT-13.06-01 | Applicable welding standards (API 650/AWS vs. CSA W59) for Canadian project | Trade-off T-02 | ER / DEL-13.02 specification (TBD) | Datasheet.md Standards; Specification.md PR-01 | ER + project specification | **TBD** |
| CT-13.06-02 | Fabricator pre-qualification approach (shop audit vs. document review) | Trade-off T-01 | Project risk assessment (TBD) | Specification.md FR-02; Procedure.md Step 1 | Project quality plan + risk assessment | **TBD** |
| CT-13.06-03 | Shop inspection frequency and party (full-time vs. periodic; D&B vs. third-party) | Considerations C-04, C-05 | ER / project quality plan (TBD) | Specification.md FR-04; Procedure.md Step 4 | ER + project quality plan | **TBD** |
| CT-13.06-04 | Impact testing applicability based on MDMT and seismic design | Consideration C-03 | DEL-13.03 design calculations / ER (TBD) | Datasheet.md MTRs; Specification.md PR-03 | Design calculations + ER | **TBD** |

**Note:** These conflicts represent fabrication quality decisions requiring project specification, ER, and quality plan inputs. Resolution during WORKING_ITEMS will enable fabrication quality planning.

---

**Document Status:** Pass 3 Complete — Enrichment complete. Design principles, considerations, trade-offs, and examples developed. Conflict Table added for fabrication quality decisions requiring human ruling. Cross-document references verified. All TBDs marked. ASSUMPTIONs labeled. Ready for WORKING_ITEMS refinement.

**Last Updated:** 2026-01-28
