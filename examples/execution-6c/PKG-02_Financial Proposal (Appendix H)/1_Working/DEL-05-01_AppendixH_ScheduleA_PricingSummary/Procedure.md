# Procedure: DEL-05-01 AppendixH ScheduleA PricingSummary

## Purpose

This procedure describes the process to **produce** the completed Appendix H Schedule A pricing summary for the Penhold Public Services Building Design-Build proposal.

**Scope of procedure:** Completion of Schedule A form from inputs (Schedule B, cost estimates, addenda log) to output (signed, reconciled Schedule A ready for PDF assembly).

**Responsible party:** Estimator / Commercial Lead (with review by Proposal Manager)

**Source:** Inferred from deliverable type and discipline (_CONTEXT.md); standard proposal development workflow

---

## Prerequisites

### Dependencies

**Mode:** NOT_TRACKED — Dependencies coordinated externally by humans (see `_DEPENDENCIES.md`)

**ASSUMPTION:** The following deliverables/inputs should be available or in progress before Schedule A can be completed:

| Prerequisite | Rationale | Status Tracking |
|--------------|-----------|-----------------|
| **DEL-05-02 (Schedule B) substantially complete** | Schedule A summarizes Schedule B; cannot reconcile until Schedule B values are established. **Clarification (Lensing: C-004):** "Substantially complete" means all pricing values finalized and approved by estimator; minimum 80% completion before Schedule A work begins, 100% before reconciliation step. | Coordinated by proposal manager |
| **Cost estimating complete** | Estimator has developed cost buildup for all base scope and additional options | Coordinated by estimator |
| **Addenda log finalized** | All addenda received and logged; addenda impacts assessed | Likely tracked in DEL-01-01 (Compliance Matrix) |
| **Scope clarifications resolved** | Any ambiguities resolved through RFP Authority questions or internal proposal team decisions | Coordinated by proposal manager |

**Source:** Inferred from deliverable production logic; _DEPENDENCIES.md states NOT_TRACKED mode

---

### Reference Materials Required

| Material | Purpose | Location |
|----------|---------|----------|
| **RFP Appendix H Schedule A template** | Blank form to be completed | RFP page 57 (`_Sources/AB-2024-07156-Penhold Public Services Building RFP_2024_004.pdf`) |
| **RFP Appendix H Schedule B** | Cost breakdown that Schedule A must reconcile to | RFP page 59 (same PDF) |
| **Addenda 01, 02, 03** | Scope modifications that affect pricing and must be acknowledged | `_Sources/` (addenda PDFs) |
| **Completed Schedule B (DEL-05-02)** | Provides detailed cost values for Schedule A summary lines | Deliverable folder (sibling deliverable in PKG-02) |
| **Pricing assumptions log** | Documents estimating assumptions, allowances, exclusions | **ASSUMPTION:** Internal estimating workpaper or pricing narrative draft (DEL-05-03) |

**Source:** _REFERENCES.md; deliverable interfaces identified in Specification section

---

### Tools and Systems

**TBD (Lensing: A-006):** Specific tools used by estimator/commercial team (e.g., Excel for reconciliation checks, Adobe Acrobat for PDF form filling, estimating software for cost buildup). Decision required from Estimator/Commercial Lead on:
- Fillable PDF approach (edit RFP template directly)
- Word recreation (recreate template in Word for editing)
- Excel compilation (maintain data in Excel, transfer to PDF for submission)

**ASSUMPTION:** Standard office productivity tools (spreadsheet, PDF editor) are sufficient

---

## Steps

### Step 1: Obtain and Prepare Schedule A Template

**Action:**
1. Extract Appendix H Schedule A template from RFP PDF (page 57)
2. Convert to editable format (fillable PDF or recreate in Word/Excel if needed)
3. Verify template integrity: 7 pricing lines (1-1 through 1-7), addenda acknowledgment section, signature block

**Verification:** Template structure matches RFP page 57 exactly

**Source:** RFP Section 4.3 (page 13); Appendix H (page 57)

---

### Step 2: Obtain Schedule B Totals

**Action:**
1. Obtain completed or near-final Schedule B from DEL-05-02 deliverable
2. Extract the following totals from Schedule B:
   - **Subtotal Base Requirements** → feeds Schedule A line 1-1
   - **Additional Item 1 subtotal** (Built-in Wash Bay) → feeds Schedule A line 1-2
   - **Additional Item 2 subtotal** (Yard Lighting) → feeds Schedule A line 1-3
   - **Additional Item 3 subtotal** (Access Control) → feeds Schedule A line 1-4
   - **Additional Item 4 subtotal** (Security and Camera System, **excluding monthly monitoring fee**) → feeds Schedule A line 1-5
   - **Additional Item 5 subtotal** (Signage) → feeds Schedule A line 1-6
   - **Additional Item 6 subtotal** (Appliances) → feeds Schedule A line 1-7

**Verification:** All Schedule B totals are final and approved by estimator

**Notes:**
- **Critical for line 1-5 (Lensing: F-009):** Monthly monitoring fee treatment must be resolved consistently. **Authoritative resolution:** Per Guidance Conflict-02, Schedule A line 1-5 reflects **installation cost only** (one-time capital cost); monthly monitoring fee documented in Schedule B but NOT added to Schedule A line 1-5. Clarify in pricing narrative (DEL-05-03).
- If Schedule B is still being revised, coordinate with estimator to lock values before completing Schedule A

**Source:** RFP Appendix H Schedule B template (page 59); reconciliation requirement (acceptance criteria)

---

### Step 3: Populate Schedule A Pricing Lines

**Action:**
1. Enter Schedule B totals into corresponding Schedule A lines:
   - Line 1-1: Enter "Subtotal Base Requirements" from Schedule B
   - Line 1-2: Enter "Additional Item 1" subtotal from Schedule B
   - Line 1-3: Enter "Additional Item 2" subtotal from Schedule B
   - Line 1-4: Enter "Additional Item 3" subtotal from Schedule B
   - Line 1-5: Enter "Additional Item 4" subtotal from Schedule B (clarify monitoring fee treatment)
   - Line 1-6: Enter "Additional Item 5" subtotal from Schedule B
   - Line 1-7: Enter "Additional Item 6" subtotal from Schedule B

2. Apply consistent formatting:
   - Use dollar symbol ($) before each value
   - Use standard number formatting (e.g., $1,234,567.89 or $1,234,567.00)
   - **ASSUMPTION (Lensing: X-003):** No decimal cents required; round to nearest dollar. **TBD:** Verify this assumption against RFP template format; if Schedule B uses different precision, reconciliation mismatches may occur.

**Verification:** Each line has a value entered (if an option is not priced, indicate "$0" or "Not priced" with explanation in pricing narrative)

**Source:** RFP Appendix H Schedule A template (page 57)

---

### Step 4: Verify Scope Exclusions (Addendum 03 Compliance)

**Action:**
1. Cross-check that base contract pricing (line 1-1) does **not** include pickled sand storage building costs
   - Review Schedule B to confirm no pickled sand building line item
   - Review estimating backup to confirm no pickled sand costs embedded

2. Cross-check that base contract pricing reflects 12-acre site (not 20-acre site)
   - Verify site work quantities in Schedule B align with 12-acre developable area

3. Cross-check that base contract pricing includes all Addendum 03 added requirements:
   - 16 ft overhead door heights
   - Bay sumps (all bays)
   - Fire apparatus exhaust ventilation (2 apparatus per bay, 4 bays total)
   - Backup generator (kitchen, meeting room/ICP, 2 bathrooms minimum)
   - Fill stations (2" minimum, one fire bay, one PW bay)
   - Solar-capable roof
   - 40 bunker gear lockers

**Verification:** Estimating backup or Schedule B line items confirm inclusion of added scope and exclusion of removed scope

**Source:** Addendum 03 sections 1.1, 1.2, 1.8, 1.10, 1.12, 1.13, 1.15, 1.16, 1.17; Acceptance criteria (_CONTEXT.md): "base excludes removed scope items"

**Output:** Scope compliance confirmed; any discrepancies flagged for estimator correction

---

### Step 5: Complete Addenda Acknowledgment Section

**Action:**
1. Locate the addenda acknowledgment section in Schedule A template (bottom of page 57)
2. Fill in the blank: "Addendum \_\_\_\_\_\_\_\_ to \_\_\_\_\_\_\_\_"
3. Enter: "01" in first blank, "03" in second blank (resulting in "Addendum 01 to 03")
4. Verify the pre-printed statement is present: "The Proponent acknowledges that they have received the following Addenda and have accounted for their contents in their Total Stipulated Price above"

**Verification:** Addenda acknowledgment section is complete and accurate

**Critical compliance note:** Failure to complete this section may result in price proposal disqualification per RFP warning (page 57)

**Source:** RFP Appendix H Schedule A (page 57); RFP Section 2.9 (page 11)

---

### Step 6: Perform Reconciliation Check

**Action:**
1. Create reconciliation checklist (see Guidance Example 3)
2. For each Schedule A line, verify that the value matches the corresponding Schedule B subtotal
3. Calculate sum of all Schedule A lines (base + options) and compare to Schedule B "TOTAL with Additional Items"
4. Document any discrepancies and return to estimator for correction

**Acceptance criteria:**
- Schedule A line 1-1 = Schedule B "Subtotal Base Requirements" (exact match)
- Schedule A lines 1-2 through 1-7 = Schedule B corresponding additional item subtotals (exact match)
- No unexplained variances

**Source:** Acceptance criteria (_CONTEXT.md); RFP Appendix H note (page 57)

**Output:** Reconciliation check pass/fail; discrepancies logged for correction

---

### Step 7: Add Tax Line (if applicable)

**Action:**
1. **TBD:** Confirm with commercial lead whether taxes are shown on Schedule A or only on Schedule B
2. **ASSUMPTION:** Based on RFP Section 4.3 requirement for "taxes shown separately," add tax calculation line(s) below the pricing lines in Schedule A
3. Calculate applicable taxes on base contract (line 1-1) and each option (lines 1-2 through 1-7)
   - **TBD:** GST rate (5% as of 2024? Confirm current rate)
   - **TBD:** PST applicability for Alberta construction (typically no PST, but verify)
4. Show tax calculations transparently (e.g., "GST (5% on base + options): $[calculated value]")

**Verification:** Tax calculation is mathematically correct and clearly labeled

**Source:** RFP Section 4.3 (page 13); **ASSUMPTION** on tax presentation format

**Note:** RFP template on page 57 does not show a tax line explicitly; this may need to be added or may be handled in Schedule B only. **Human ruling required** on tax presentation approach.

---

### Step 8: Obtain Authorized Signature

**Action:**
1. Prepare Schedule A for signature (all pricing lines complete, addenda acknowledged, reconciliation verified)
2. Identify authorized signing officer per proponent's governance:
   - If corporation: Officer with authority to bind + corporate seal required
   - If partnership/individual: Partner/proprietor with seal and witness
   - If joint venture: Each party signs
3. Obtain signature(s) in accordance with RFP Section 5.2 requirements (page 13)
4. Affix corporate seal if applicable
5. Date the signature

**Note (Lensing: E-002):** **TBD:** Does proponent's internal governance require board or officer approval for commitments above a certain threshold? If so, ensure internal approval is obtained before signature.

**Verification:** Signature block complete per RFP Section 5.2 requirements

**Source:** RFP Section 5.2 Signatures (page 13); Appendix H Schedule A signature block (page 57-58)

---

### Step 9: Final Quality Check

**Action:**

Perform final review against specification requirements (see Specification section):

| Check Item | Requirement | Spec Ref | Status |
|------------|-------------|----------|--------|
| Form completeness | All 7 pricing lines filled; addenda section complete | R-01.2, R-04.1 | ☐ Pass ☐ Fail |
| Reconciliation | Schedule A = Schedule B totals (base and each option) | R-03.1, R-03.2 | ☐ Pass ☐ Fail |
| Scope exclusions | Pickled sand building NOT in base price | R-06.1 | ☐ Pass ☐ Fail |
| Scope inclusions | All Addendum 03 added requirements reflected in pricing | R-04.2 | ☐ Pass ☐ Fail |
| Addenda acknowledgment | Addendum 01 to 03 acknowledged | R-04.1, R-04.3 | ☐ Pass ☐ Fail |
| Signature | Authorized signature and seal (if applicable) present | R-05.1, R-05.2 | ☐ Pass ☐ Fail |
| Tax separation | Taxes shown separately (if applicable to Schedule A presentation) | R-02.5 | ☐ Pass ☐ Fail |
| Mandatory compliance gate (Lensing: A-003) | All R-01 through R-07 requirements verified as unified gate | R-01 to R-07 | ☐ Pass ☐ Fail |

**Acceptance criteria:** All checks pass

**Output:** Schedule A approved for PDF assembly, or discrepancies flagged for correction

**Source:** Specification requirements R-01 through R-07; acceptance criteria (_CONTEXT.md)

**Note (Lensing: A-008):** Guidance Notes recommend "second reviewer" but this step does not mandate independent review. **Recommendation:** Require independent reviewer sign-off as mandatory for Gate 5 approval.

---

### Step 10: Deliver to PDF Assembly Process

**Action:**
1. Export Schedule A to PDF format (if working in Word/Excel) or retain as filled PDF
2. Provide completed Schedule A PDF to proposal assembly lead (confirm recipient — **TBD (Lensing: D-004):** likely Proposal Manager for DEL-01-02 but handoff point and acceptance criteria should be confirmed)
3. Verify Schedule A is included in proposal PDF in correct sequence per RFP Section 4.3: "using the main headings and presents the information in the order provided in Sections 6, 7, 8, and 9"
   - **ASSUMPTION:** Appendix H (pricing) is included in Section 8 (Evaluation of Proposals) presentation order

**Verification:** Schedule A PDF is included in final proposal PDF assembly

**Source:** RFP Section 4.3 (page 12); RFP Section 5 (page 13) submission requirements

**Output:** Schedule A delivered to PDF assembly process; ready for submission

---

### Step 10a: Verify PDF File Size (Lensing: F-006)

**Action:**
1. After Schedule A is assembled into proposal PDF, verify total PDF file size
2. Confirm total proposal PDF is under 15 MB (R-01.4 requirement)
3. If over limit, coordinate with PDF assembly lead to optimize file size

**Verification:** Total proposal PDF file size < 15 MB

**Source:** RFP Section 4.2 (page 12); Specification R-01.4

---

### Step 11: Coordinate with Pricing Narrative (Lensing: C-006)

**Action:**
1. Review DEL-05-03 (Pricing Narrative) draft for consistency with Schedule A values
2. Verify pricing assumptions documented in narrative align with Schedule A line items
3. Flag any discrepancies between narrative and Schedule A for resolution
4. Confirm addenda impacts documented in narrative match Schedule A addenda acknowledgment

**Verification:** Pricing narrative and Schedule A are internally consistent

**Source:** Specification interface with DEL-05-03; consistent pricing documentation practice

---

## Verification

### Process Verification (Quality Gates)

| Gate | Verification Activity | Responsible Party | Outcome |
|------|----------------------|-------------------|---------|
| **Gate 1: Form completeness** | All pricing lines and addenda section filled in | Estimator | Pass/Fail → proceed or return for completion |
| **Gate 2: Reconciliation** | Schedule A totals match Schedule B totals (mathematical verification) | Estimator + QA reviewer | Pass/Fail → proceed or return for correction |
| **Gate 3: Addenda compliance** | All addenda acknowledged; scope exclusions/inclusions verified | Proposal Manager | Pass/Fail → proceed or return for correction |
| **Gate 4: Signature** | Authorized signature and seal obtained | Commercial Lead | Pass/Fail → proceed or return for execution |
| **Gate 5: Final QC** | Independent review of completed Schedule A against specification requirements | Proposal Manager or QA Lead | Pass/Fail → approve for PDF assembly or return for correction |

**Source:** Inferred from specification requirements and standard proposal QC practice

### Gate-to-Requirement Mapping (Lensing: D-003)

| Gate | Specification Requirements Covered |
|------|-----------------------------------|
| Gate 1: Form completeness | R-01.1, R-01.2, R-01.3 |
| Gate 2: Reconciliation | R-03.1, R-03.2, R-03.3 |
| Gate 3: Addenda compliance | R-04.1, R-04.2, R-04.3, R-06.1, R-06.2 |
| Gate 4: Signature | R-05.1, R-05.2 |
| Gate 5: Final QC | R-01.4, R-02.1 through R-02.5, R-05.3, R-05.4, R-07.1 through R-07.4 |

**Note (Lensing: X-007):** Gate 2 requires "Estimator + QA reviewer" but no preceding step ensures QA reviewer availability. Add prerequisite check for reviewer assignment before Gate 2.

---

### Output Verification (Deliverable Acceptance)

**Acceptance criteria** (from _CONTEXT.md):
1. Totals reconcile to Schedule B ✓
2. Addenda acknowledgment completed ✓
3. Base excludes removed scope items ✓

**Additional verification** (from Specification requirements):
4. Form uses RFP template exactly (R-01.1) ✓
5. All 7 pricing lines completed (R-01.2) ✓
6. Taxes shown separately (R-02.5) ✓
7. Authorized signature present (R-05.1, R-05.2) ✓
8. Additional options priced per R-02.4 (incremental scope only) ✓ (Lensing: X-009)
9. R-07.1 through R-07.4 option-specific requirements verified ✓ (Lensing: X-009)

**Final check:** Schedule A is compliant, reconciled, and ready for submission

---

## Records

### Deliverable Outputs

| Output | Format | Destination | Retention |
|--------|--------|-------------|-----------|
| **Completed Schedule A (PDF)** | PDF (editable source + locked PDF) | Included in proposal submission PDF; submitted via email to spendergast@townofpenhold.ca | Permanent (part of proposal record and contract if successful) |
| **Addenda acknowledgment** | Text within Schedule A form | Embedded in Schedule A | Permanent |

**Source:** RFP Section 5.3 (page 14) submission requirements

---

### Supporting Records (for internal tracking)

**ASSUMPTION:** The following records should be maintained by the proposal team (not submitted to Owner):

| Record | Purpose | Retention |
|--------|---------|-----------|
| **Reconciliation check worksheet** | Documents verification that Schedule A = Schedule B | Retain until contract award or proposal closeout |
| **Addenda log** | Tracks all addenda received and acknowledged | Retain for compliance audit trail |
| **Estimating backup** | Supports Schedule B and Schedule A values; enables change order pricing if scope changes | Retain through contract delivery (if successful) |
| **QA review checklist** | Documents that final quality check was performed before submission | Retain until proposal submission |
| **Version control log** | Tracks Schedule A revisions if proposal is resubmitted | Retain until final submission |
| **Compliance check record (Lensing: C-002)** | Signed-off checklist with requirement IDs documenting that each Specification requirement was verified | Retain for post-submission audit defense |

**Source:** Inferred from standard proposal management practice

### Post-Submission Audit Trail (Lensing: A-005)

**Purpose:** Maintain records to demonstrate compliance if challenged during evaluation.

| Record | Purpose | Content |
|--------|---------|---------|
| **Reconciliation worksheet** | Prove Schedule A = Schedule B | Calculation showing exact match per line |
| **Addenda acknowledgment evidence** | Prove all addenda received and priced | Addenda log with dates received, pricing impacts noted |
| **Scope exclusion confirmation** | Prove pickled sand building excluded | Schedule B showing no related line items |
| **QC sign-off** | Prove independent review completed | Signed checklist with reviewer name and date |

**Note:** If Owner Evaluation Committee raises compliance questions post-submission, these records enable rapid response with documented evidence.

---

## Notes

- **Coordination point:** Schedule A completion depends on Schedule B completion; recommend establishing a cutoff date for Schedule B finalization to allow time for Schedule A reconciliation and QA
- **Timing estimate:** **TBD** — Actual time required depends on estimating complexity; assume minimum 0.5 day for Schedule A form completion and reconciliation after Schedule B is finalized
- **Revision process:** If proposal is revised and resubmitted (permitted until deadline per RFP Section 5.3, page 14), Schedule A must be updated with revision number clearly indicated
- **Risk mitigation:** Perform reconciliation check at least 24 hours before submission deadline to allow time for error correction
- **ASSUMPTION:** If any pricing line cannot be completed (e.g., proponent chooses not to price an optional item), indicate "$0" or "Not priced" and explain in pricing narrative (DEL-05-03)
- **Timing estimate (Lensing: F-004):** **TBD:** Minimum lead time from Schedule B finalization to submission deadline. Current estimate = minimum 0.5 day for Steps 1-10; confirm with Estimator/Proposal Manager based on team capacity.
- **Revision handling (Lensing: C-005):** If Schedule B values change after Schedule A has been populated, return to Step 2 and re-execute Steps 2-9. Maintain version control to track changes.
- **Personnel proficiency (Lensing: F-005):** Person executing this procedure should have: (1) familiarity with RFP requirements, (2) access to all source documents, (3) authority to enter pricing values or escalation path to commercial lead.
