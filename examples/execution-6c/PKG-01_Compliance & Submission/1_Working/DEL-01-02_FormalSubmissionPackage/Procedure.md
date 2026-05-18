# Procedure: DEL-01-02 FormalSubmissionPackage

## Purpose

This procedure describes the process to **produce** the Formal Submission Package deliverable, which includes:

1. Final PDF assembly plan
2. Submission email package details
3. Revision control statement

**Outcome:** A compliant, ready-to-submit proposal PDF and submission package that passes all mandatory requirements (OBJ-001) and enables evaluation.

**Scope:** This procedure covers the assembly, verification, and submission preparation process. It does **not** cover the creation of proposal content (covered by upstream deliverables DEL-02 through DEL-09).

**Source:** Decomposition §8 DEL-01-02 description; Specification requirements R-01 through R-08.

---

## Guidance Context

**Source:** _SEMANTIC_LENSING X-004 (Matrix X, Lens: X:reviewing:consistency)

This procedure implements the principles and considerations described in Guidance.md. Procedure users should read Guidance.md first to understand strategic context.

**Key Guidance Principles Implemented:**
- **P-01 Compliance First:** Steps 0, 1, 5, 6, 10
- **P-02 Explicit Compliance:** Steps 2, 6, 9
- **P-03 Version Control:** Steps 5, 9, 11
- **P-04 Size Discipline:** Steps 4, 7
- **P-05 Email Fragility:** Steps 9, 10, 11

---

## Procedure-to-Requirement Traceability

**Source:** _SEMANTIC_LENSING D-001 (Matrix D, Lens: D:normative:applying)

**Issue:** Procedure Steps 1–12 did not explicitly map to Specification requirements, making it unclear which steps are compliance-critical vs. best practice.

| Step | Step Name | Specification Requirements | Decomposition Objective | Compliance Criticality |
|------|-----------|---------------------------|------------------------|------------------------|
| **Step 0** | Dependency Verification | R-08 (Content Completeness) | OBJ-001 | Critical — blocks assembly if not met |
| **Step 1** | Content Freeze and Timeline | — | OBJ-001 (process support) | Best practice |
| **Step 2** | Collect Final Content Files | R-03, R-06, R-08 | OBJ-001 | Critical — missing content = fail |
| **Step 3** | Verify RFP Structure | R-02 | OBJ-001 | Critical — wrong order = fail |
| **Step 4** | Optimize Graphics | R-01 | OBJ-001 | Critical — supports size compliance |
| **Step 5** | Assemble Initial PDF | R-01, R-02, R-05 | OBJ-001 | Critical — format/structure compliance |
| **Step 6** | Verify Compliance | R-02, R-03, R-06, R-07, R-08 | OBJ-001 | Critical — final compliance gate |
| **Step 7** | Check File Size | R-01 | OBJ-001 | Critical — size compliance |
| **Step 8** | QA Review | — | OBJ-001 (quality support) | Best practice (strongly recommended) |
| **Step 9** | Prepare Submission Email | R-04, R-05 | OBJ-001 | Critical — submission method compliance |
| **Step 10** | Final Pre-Submission Check | R-01 through R-08 | OBJ-001 | Critical — final gate |
| **Step 11** | Submit Proposal | R-04 | OBJ-001 | Critical — submission execution |
| **Step 12** | Post-Submission Actions | — | — | Best practice |

**Reading the Table:** Steps marked "Critical" directly support pass/fail compliance requirements. Skipping or failing a critical step may result in disqualification. Steps marked "Best practice" improve quality and reduce risk but are not directly tied to mandatory requirements.

---

## Prerequisites

### Dependencies

**Dependency tracking mode:** NOT_TRACKED — Dependencies coordinated externally by humans (see `_DEPENDENCIES.md`).

**Upstream deliverables that must be complete before assembly:**

| Deliverable | Content | Maturity Required |
|-------------|---------|-------------------|
| **DEL-01-01** | Compliance matrix and checklist | Final |
| **DEL-01-03** | Bonding and insurance evidence | Final (executed) |
| **DEL-02-01** | Concept design package | Final |
| **DEL-02-02** | Design brief narrative | Final |
| **DEL-02-03** | Sustainability and energy narrative | Final |
| **DEL-03-01** | Design methodology narrative | Final |
| **DEL-03-02** | Detailed design and construction docs plan | Final |
| **DEL-04-01** | Construction methodology narrative | Final |
| **DEL-04-02** | Budget control and change management plan | Final |
| **DEL-04-03** | Communications and reporting plan | Final |
| **DEL-05-01** | Appendix H Schedule A (pricing summary) | Final (executed) |
| **DEL-05-02** | Appendix H Schedule B (cost breakdown) | Final |
| **DEL-05-03** | Pricing narrative and assumptions | Final |
| **DEL-06-01** | Commissioning, training, closeout, warranty narrative | Final |
| **DEL-07-01** | Design-Build firm experience profile | Final |
| **DEL-07-02** | Key team members and resumes | Final |
| **DEL-07-03** | Appendix I (subtrade and consultant list) | Final |
| **DEL-08-01** | Detailed project schedule | Final |
| **DEL-09-01** | Risk register and mitigation plan | Final |
| **DEL-09-02** | Site conditions and due diligence summary | Final |

**ASSUMPTION:** "Final" maturity means content has passed internal QA review and is approved for inclusion in submission. Changes after content freeze require formal approval and trigger revision control process.

**Source:** Inferred from Decomposition §8 (deliverables list) and typical proposal assembly dependencies.

---

### Step 0: Dependency Verification (Pre-Assembly Gate)

**Source:** _SEMANTIC_LENSING F-002 (Matrix F, Lens: F:operative:sufficiency)

**Issue:** Step 2 assumes all upstream deliverables are available, but provides no contingency for upstream delays.

**Action:**
1. **Verify deliverable status** — Confirm that all upstream deliverables (DEL-01-01, DEL-01-03, DEL-02-01 through DEL-09-02) are in Final status.
2. **Check status list:**
   - For each deliverable in the Prerequisites table, verify status = "Final"
   - If any deliverable status is not Final, document which deliverable(s) and current status
3. **If dependencies not met:**
   - Escalate to Proposal Manager immediately
   - Assess whether content freeze deadline should be delayed
   - Document dependency delay in project log with estimated resolution time
   - Do NOT proceed to Step 1 until all critical dependencies are resolved or explicit waiver obtained

**Verification:** All deliverables in Final status; or explicit Proposal Manager approval to proceed with identified gaps.

**Responsible:** Proposal Manager

**Source:** _SEMANTIC_LENSING F-002; implied by Decomposition dependency structure.

---

### Reference Materials

**Required:**
- **RFP 2024_004** (primary RFP document) — Sections 4.2–4.3 (submission requirements), 5.2 (execution requirements), 6–9 (content structure)
- **Appendix G** — Letter of Offer template
- **Appendix H** — Financial Proposal template (for addenda acknowledgement verification)
- **Addendum 01, 02, 03** — For acknowledgement verification
- **Compliance matrix** (DEL-01-01) — For content completeness verification

**Source:** `_REFERENCES.md`; Specification requirements.

---

### Tools and Resources

**Required:**
- **PDF compilation software** (e.g., Adobe Acrobat Pro, PDF merge tool)
- **Image optimization software** (e.g., Adobe Photoshop, online compression tools)
- **Email client** with attachment size verification capability
- **File size monitoring tool** (file explorer properties, PDF info panel)

**Optional:**
- **Version control system** (e.g., Git, SharePoint) for tracking content changes
- **PDF compression tool** (e.g., Adobe Acrobat Reduce File Size, online tools)

**ASSUMPTION:** Tools are available and team members are trained in their use before final assembly begins.

---

### Personnel and Roles

| Role | Responsibility |
|------|----------------|
| **Proposal Manager** | Overall assembly coordination; final QA; submission execution |
| **Content Owners** | Provide final content files by content freeze deadline |
| **Estimator / Commercial Lead** | Verify pricing (Appendix H) accuracy and execution |
| **Legal / Contracts** | Verify execution requirements (signatures, seals) |
| **IT / Technical Support** | Troubleshoot email submission issues if they arise |

**Source:** Inferred from Decomposition §7 (package ownership) and typical proposal team structure.

---

## Steps

### Step 1: Establish Content Freeze and Assembly Timeline

**Action:**
1. **Set content freeze deadline** — Establish the date/time after which no content changes are allowed except critical compliance corrections.
   - **Recommended:** 48 hours before submission deadline (e.g., Aug 28, 2024 @ 2:00 PM for Aug 30 deadline).
2. **Communicate freeze deadline** — Notify all content owners (DEL-02 through DEL-09 leads) of the freeze deadline and consequences of late changes.
3. **Establish assembly timeline** — Schedule specific tasks between content freeze and submission:
   - Content freeze to initial PDF assembly: 4–6 hours
   - Initial PDF assembly to QA review: 2–4 hours
   - QA review to final PDF: 2–4 hours
   - Final PDF to submission: 1–2 hours buffer
4. **Define Critical Correction Escalation Protocol:**
   - **Critical corrections** are defined as: missing addenda acknowledgement, incorrect proponent name, wrong RFP number, missing required signature pages, or any item that would trigger automatic disqualification.
   - If critical correction is discovered AFTER content freeze but BEFORE final assembly:
     - Immediately notify Proposal Manager
     - Document correction need and justification
     - Proposal Manager approves or rejects correction within 30 minutes
     - If approved, correction is implemented and triggers abbreviated QA re-review (focus on corrected section only)
     - Maximum time allowance: 30 min for correction approval + 1 hour for reassembly and QA
   - Non-critical corrections (typos, minor formatting) are NOT allowed after content freeze unless bundled with a critical correction.

**Verification:** All content owners acknowledge freeze deadline; assembly timeline is documented and shared with team; critical correction protocol is understood.

**Responsible:** Proposal Manager

**Source:** Guidance consideration "Timing and Coordination"; _SEMANTIC_LENSING C-002 (critical correction escalation); industry best practice.

---

### Step 2: Collect Final Content Files

**Action:**
1. **Request final files** — Collect final versions of all deliverables (DEL-01-01, DEL-01-03, DEL-02-01 through DEL-09-02) from content owners.
   - **File format:** PDF preferred for consistency; source files (Word, Excel) as backup.
   - **Naming convention:** Use consistent file naming (e.g., `DEL-02-01_ConceptDesign_Final.pdf`).
2. **Verify file completeness** — Cross-check received files against compliance matrix (DEL-01-01) to ensure all mandatory content is present.
3. **Verify execution status** — Confirm that files requiring signatures/seals (Letter of Offer, Appendix H, bonding evidence) are executed and include original signatures (not placeholders).
4. **Verification Sign-Off** — Proposal Manager (or delegate) signs and dates a "Content File Verification Checklist" confirming:
   - All files present per DEL-01-01 compliance matrix
   - All executed documents verified with original signatures (not placeholders)
   - Any missing items documented with resolution plan
   - File checklist archived in project records

**Verification:** All files received and logged; no missing content; executed documents verified; verification sign-off completed and archived.

**Responsible:** Proposal Manager

**Source:** Specification requirement R-08 (content completeness); Guidance principle P-02 (explicit compliance); _SEMANTIC_LENSING E-002 (verification sign-off).

---

### Step 3: Verify RFP Structure and Heading Order

**Action:**
1. **Review RFP Sections 6–9** — Identify the exact heading text and sequence required by the RFP.
2. **Map content to RFP sections** — Assign each deliverable file to the appropriate RFP section/heading.
   - Example mapping (illustrative — verify against actual RFP):
     - **Section 6 (Mandatory Compliance):** DEL-01-02 (Letter of Offer), DEL-01-01 (compliance matrix), DEL-01-03 (bonding)
     - **Section 7 (Technical Proposal):** DEL-02-01, DEL-02-02, DEL-02-03, DEL-03-01, DEL-03-02, DEL-04-01, etc.
     - **Section 8 (Pricing):** DEL-05-01, DEL-05-02, DEL-05-03
     - **Section 9 (Team):** DEL-07-01, DEL-07-02, DEL-07-03
3. **Create assembly outline** — Document the exact section order and page numbering scheme to be used in final PDF.

**Verification:** Assembly outline matches RFP Sections 6–9 heading order exactly; no sections missing.

**Responsible:** Proposal Manager

**Source:** Specification requirement R-02 (heading order); Guidance principle P-01 (compliance first).

---

### Step 4: Optimize Graphics and File Sizes

**Action:**
1. **Inventory high-size files** — Identify files with large graphics (renderings, site plans, photos).
2. **Optimize images:**
   - **Renderings/photos:** Reduce to 150 dpi; compress JPEG quality to 80–85%.
   - **Drawings/plans:** Export as vector PDF if possible; if raster, use 200 dpi minimum.
   - **Charts/diagrams:** Export as vector format (PDF, SVG).
3. **Test individual file sizes** — Check size of each optimized file; aim for individual files to be under 2 MB if possible.
4. **Document optimization settings** — Record settings used (resolution, compression level) for consistency and future reference.

**Verification:** All graphics optimized; individual file sizes reasonable; visual quality remains acceptable for evaluation.

**Responsible:** Proposal Manager or designated Graphics Coordinator

**Source:** Specification requirement R-01 (15 MB limit); Guidance principle P-04 (size discipline); Guidance consideration "File Size Optimization Strategies."

---

### Step 5: Assemble Initial PDF

**Action:**
1. **Merge files in RFP order** — Use PDF compilation software to merge all content files into a single PDF following the assembly outline from Step 3.
2. **Add cover page** — Insert a cover page with:
   - Project title: "Town of Penhold Public Services Building Design-Build Proposal"
   - RFP number: "RFP 2024_004"
   - Proponent name and contact information
   - Submission date: "Aug 30, 2024"
   - Revision status: "ORIGINAL SUBMISSION" (or "REVISION [N]" if resubmitting)
3. **Add table of contents** — Generate or insert a table of contents linking to major RFP sections.
4. **Add page numbers** — Apply consistent page numbering throughout the document.
5. **Check bookmarks/navigation** — Ensure PDF bookmarks/navigation panel reflects RFP section structure for evaluator convenience.

**Verification:** PDF opens correctly; all content present in correct order; cover page complete; page numbers sequential; bookmarks functional.

**Responsible:** Proposal Manager

**Source:** Specification requirements R-01, R-02; Guidance example "Cover Page Revision Control."

---

### Step 6: Verify Compliance Requirements

**Action:**
1. **Cross-check against compliance matrix** (DEL-01-01) — Verify that every mandatory item listed in the compliance matrix is present in the assembled PDF.
   - Use the matrix as a checklist; mark each item as "verified" after locating it in the PDF.
2. **Verify specific compliance elements:**
   - **Letter of Offer (Appendix G):** Present and executed (Requirement R-06)
   - **Addenda acknowledgement:** Present in Appendix H and/or cover letter (Requirement R-07)
   - **Authorized signatures:** All signature pages include original signatures and seals as required (Requirement R-03)
   - **RFP heading order:** Content follows Sections 6–9 order (Requirement R-02)
3. **Document verification results** — Create a checklist or sign-off sheet confirming compliance verification is complete.

**Verification:** All mandatory items present and verified; no compliance gaps identified.

**Responsible:** Proposal Manager + Legal/Contracts (for execution verification)

**Source:** Specification requirements R-02, R-03, R-06, R-07, R-08; Guidance principle P-02 (explicit compliance).

---

### Step 7: Check File Size and Optimize if Needed

**Action:**
1. **Check assembled PDF size** — View file properties to confirm size in MB.
2. **If size > 15 MB:**
   - **Option A:** Use PDF compression tool (e.g., Adobe Acrobat "Reduce File Size") with settings that preserve readability.
   - **Option B:** Identify and further optimize largest graphic elements (re-export at lower resolution or higher compression).
   - **Option C:** Remove low-value content (optional appendices, redundant images) if optimization alone is insufficient.
3. **Re-check size after optimization** — Ensure final PDF is under 15 MB with headroom (target 12–13 MB).
4. **Verify visual quality** — Open optimized PDF and spot-check graphics, drawings, and text for readability. Ensure compression did not degrade quality below acceptable level.

**Verification:** Final PDF size < 15 MB; visual quality acceptable; no content lost during optimization.

**Responsible:** Proposal Manager

**Source:** Specification requirement R-01 (15 MB limit); Guidance principle P-04 (size discipline); Guidance consideration "File Size Optimization Strategies."

---

### Step 8: Conduct Quality Assurance (QA) Review

**Action:**
1. **Assemble QA team** — Proposal Manager + 1–2 senior reviewers (not primary content authors).
2. **Perform page-by-page review:**
   - **Content completeness:** Verify all sections present and complete.
   - **Visual quality:** Check graphics, drawings, and charts for clarity.
   - **Consistency:** Verify terminology, formatting, and style are consistent across sections.
   - **Errors:** Check for typos, formatting glitches, broken cross-references, missing page numbers.
3. **Check critical elements:**
   - Cover page includes correct project name, RFP number, proponent name, date, and revision status.
   - Table of contents matches actual content.
   - All signatures and seals are present and legible (not cut off or obscured).
   - Addenda acknowledgement is visible and correct.
4. **Document QA findings** — Create a punch list of issues to be corrected.
5. **Correct issues** — Address all QA findings and re-generate PDF if changes are needed.
6. **Re-verify after corrections** — Confirm all issues resolved; check file size again after changes.

**Verification:** QA review complete; all issues resolved; final PDF approved for submission.

**Responsible:** Proposal Manager (QA lead) + Senior Reviewers

**Source:** ASSUMPTION (proposal management best practice); implied by Decomposition acceptance criteria (PDF format, heading order, completeness).

---

### Step 9: Prepare Submission Email Package

**Action:**
1. **Draft submission email:**
   - **To:** [Submission email address from RFP §4.2–4.3 — **location TBD**]
   - **Subject:** "[Proponent Name] — Penhold PSB Proposal (RFP 2024_004) — [ORIGINAL/REVISION N]"
   - **Body text:**
     ```
     Dear Town of Penhold Procurement,

     Attached is [Proponent Name]'s proposal for the Public Services Building Design-Build project (RFP 2024_004).

     Submission details:
     - Proposal file: [filename.pdf]
     - File size: [X.X MB]
     - Submission date: Aug 30, 2024
     - Revision status: [ORIGINAL SUBMISSION / REVISION 1 — supersedes [previous submission time]]

     We acknowledge receipt and integration of Addendum 01 (Jul 11, 2024), Addendum 02 (Jul 15, 2024), and Addendum 03 (Jul 31, 2024).

     Please confirm receipt of this submission.

     Sincerely,
     [Signatory Name]
     [Signatory Title]
     [Proponent Name]
     [Contact Information]
     ```
2. **Finalize PDF file name:**
   - **Format:** `[ProponentName]_Penhold_PSB_RFP2024_004_[Original/Rev1].pdf`
   - **Example:** `ABC_Builders_Penhold_PSB_RFP2024_004_Original.pdf`
3. **Attach PDF to email** — Verify attachment is correct file and correct size.
4. **Test email setup:**
   - Verify recipient address is correct.
   - Verify attachment size does not exceed email server limits (typically 10–25 MB).
   - Enable read receipt or delivery confirmation if allowed.
5. **Save draft email** — Save as draft in email client for final review before sending.

**Verification:** Email drafted and saved; attachment verified; recipient address confirmed; file name follows convention.

**Responsible:** Proposal Manager

**Source:** Specification requirement R-04 (submission method); Specification requirement R-05 (revision control); Guidance principle P-03 (version control); Guidance principle P-05 (email submission fragility).

---

### Step 10: Final Pre-Submission Check

**Action:**
1. **Confirm deadline and time zone** — Verify submission deadline is Aug 30, 2024 @ 2:00 PM **MST** (not local time if different).
2. **Verify current time** — Check current time in MST to ensure sufficient time remains.
3. **Review submission checklist with consequence awareness:**

| Checklist Item | Consequence if Missed |
|----------------|----------------------|
| ☑ Final PDF is under 15 MB | PDF rejected by Town email server or evaluator system; automatic fail |
| ☑ PDF follows RFP Sections 6–9 heading order | Evaluators mark content as "missing"; potential disqualification |
| ☑ All mandatory content present (verified against compliance matrix) | Missing mandatory items trigger automatic disqualification |
| ☑ Letter of Offer (Appendix G) included and executed | Proposal legally non-binding; disqualification |
| ☑ Addenda acknowledged (Appendix H and/or cover letter) | Price proposal may be disqualified per Constraint C-07 |
| ☑ All signature pages executed with required seals | Unauthorized submission; disqualification |
| ☑ Cover page includes revision status | Evaluator confusion about version; may use wrong version |
| ☑ Submission email drafted with correct recipient, subject, body, and attachment | Email goes to wrong recipient or missing attachment; submission fails |
| ☑ PDF file name follows naming convention | Minor risk: confusion in Town records; low impact if other compliance met |

4. **Obtain final sign-off** — Proposal Manager and senior leadership approve submission.

**Verification:** All checklist items confirmed; final sign-off obtained.

**Responsible:** Proposal Manager + Senior Leadership

**Source:** Specification requirements R-01 through R-08; Guidance principle P-01 (compliance first); _SEMANTIC_LENSING X-002 (consequence rationale).

---

### Step 11: Submit Proposal

**Action:**
1. **Send submission email** — Click "Send" in email client; monitor for send confirmation.
2. **Verify send success:**
   - Check "Sent Items" folder to confirm email was sent.
   - Save screenshot of sent email with timestamp as proof of submission.
   - Monitor for delivery confirmation or read receipt (if enabled).
3. **Monitor for Town confirmation** — If RFP promises submission confirmation, monitor email for confirmation within 15 minutes.
4. **If submission fails or no confirmation received:**
   - Immediately troubleshoot (check spam folder, verify recipient address, check attachment size).
   - Resubmit if needed (with revised revision status if applicable).
   - Contact Town by phone to confirm receipt if email confirmation not received within 30 minutes.
5. **Retain proof of submission (Minimum Acceptable Standard):**

   **Source:** _SEMANTIC_LENSING D-002 (Matrix D, Lens: D:operative:reviewing)

   Minimum acceptable proof of submission that would defend against a "proposal not received" claim:

   | Proof Element | Description | Required? |
   |---------------|-------------|-----------|
   | **Email timestamp** | Screenshot or saved copy showing date/time sent from "Sent Items" folder | Required |
   | **Email header screenshot** | Screenshot showing recipient address, subject line, attachment name, and send time | Required |
   | **Attachment verification** | Confirmation that correct PDF file (name, size) was attached | Required |
   | **Town confirmation email** | If Town provides confirmation within 30 minutes, save as proof | Required (if received) |
   | **Read/delivery receipt** | If enabled and returned, save as supplementary proof | Optional |
   | **Submission log entry** | Documented record with timestamp, revision status, actions taken | Required |

   - Save all proof elements in secure project archive immediately after submission
   - If Town confirmation not received within 30 minutes, phone call follow-up becomes part of proof record

**Verification:** Email sent successfully; all required proof elements retained; confirmation received (or follow-up action documented).

**Responsible:** Proposal Manager

**Source:** Specification requirement R-04 (submission method/deadline); Guidance principle P-05 (email submission fragility); _SEMANTIC_LENSING D-002 (proof of submission standard).

---

### Step 12: Post-Submission Actions (Optional)

**Action:**
1. **Archive submission package** — Save final PDF, submission email, proof of submission, and all source files in secure project archive.
2. **Debrief with team** — Conduct brief lessons-learned session to document what went well and what could be improved for future proposals.
3. **Monitor for Town follow-up** — Watch for any Town requests for clarification, additional information, or interviews.

**Verification:** Files archived; debrief complete; team on standby for Town follow-up.

**Responsible:** Proposal Manager

**Source:** ASSUMPTION (proposal management best practice).

---

## Verification

### Step-by-Step Verification Summary

| Step | Verification Action | Checkpoint |
|------|---------------------|------------|
| **1** | Content freeze deadline communicated; assembly timeline documented | All content owners acknowledge deadline |
| **2** | All final content files received and logged; executed documents verified | No missing content; signatures present |
| **3** | Assembly outline matches RFP Sections 6–9 heading order | Outline approved |
| **4** | Graphics optimized; individual file sizes reasonable; visual quality acceptable | Files ready for assembly |
| **5** | PDF assembled; cover page, TOC, page numbers, bookmarks present | PDF structure complete |
| **6** | All mandatory items verified against compliance matrix; signatures/addenda checked | Compliance confirmed |
| **7** | Final PDF size < 15 MB; visual quality acceptable | Size compliant |
| **8** | QA review complete; all issues resolved; final PDF approved | QA sign-off obtained |
| **9** | Submission email drafted; attachment verified; recipient confirmed | Email ready |
| **10** | Final checklist complete; sign-off obtained | Ready to submit |
| **11** | Email sent; proof of submission retained; confirmation monitored | Submission confirmed |
| **12** | Files archived; debrief complete | Post-submission complete |

---

## Records

### Documentation to be Retained

1. **Final submitted PDF** — Exact file submitted to Town (with metadata/timestamp intact)
2. **Submission email** — Copy of sent email with timestamp (screenshot + saved email in "Sent Items")
3. **Proof of submission** — Screenshot of sent email; delivery/read receipt if available; Town confirmation email if received
4. **Submission log** — Record of submission time, revision status, any issues encountered, follow-up actions taken
5. **Assembly checklist** — Completed pre-submission checklist with sign-offs
6. **QA review notes** — QA findings and resolution documentation
7. **Source files** — All content files (DEL-01 through DEL-09) used in final assembly
8. **Compliance matrix verification** — Annotated compliance matrix showing all items verified

**Storage location:** Secure project archive (server, SharePoint, or other document management system)

**Retention period:** **ASSUMPTION:** Retain for duration of project + warranty period + any regulatory retention requirements (typically 7–10 years for public procurement).

**Source:** ASSUMPTION (proposal management best practice; public procurement record-keeping requirements).

---

## Revision History

| Date | Version | Change | Author |
|------|---------|--------|--------|
| 2026-02-04 | 1.0 | Initial generation (Pass 1) | 4_DOCUMENTS agent |
| 2026-02-04 | 1.1 | Cross-reference consistency check (Pass 2) — No issues found | 4_DOCUMENTS agent |
| 2026-02-04 | 1.2 | Semantic lensing enrichment (Pass 3) — Incorporated C-002 (critical correction escalation), D-001 (procedure-to-requirement traceability), D-002 (proof of submission standard), F-002 (dependency verification step), X-002 (consequence rationale), E-002 (verification sign-off); Added Step 0 and Guidance Context section | 4_DOCUMENTS agent |
