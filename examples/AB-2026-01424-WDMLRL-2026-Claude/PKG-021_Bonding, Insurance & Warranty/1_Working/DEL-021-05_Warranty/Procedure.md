# Procedure — DEL-021-05: Guarantee Period Obligations

**Document Type:** Procedure (operational)
**Deliverable ID:** DEL-021-05_Warranty
**Package:** PKG-021 — Bonding, Insurance & Warranty
**Project:** AB-2026-01424-WDMLRL-2026-Claude
**Prepared by:** 4_DOCUMENTS agent (Pass 1+2; Pass 3 enrichment applied)
**Date:** 2026-02-26

---

## Terminology Note

The RFP uses the term "guarantee period" (RFP §2.10) while common industry usage and several sections of these production documents use "warranty period." These terms are synonymous in the context of this deliverable. The authoritative term from the RFP is "guarantee period"; "warranty period" is used interchangeably throughout these documents for readability. Where precision is required for audit or contractual purposes, prefer "guarantee period" as the governing term. (Source: RFP §2.10 heading; Semantic Lensing item E-002)

---

## Purpose

This procedure describes the operational steps to administer the guarantee period obligations for the 2026 Design Build of the West Dried Meat Lake Regional Landfill Maintenance Shop Addition from the issuance of the Construction Completion Certificate (CCC) through to warranty period expiry and final holdback release.

The procedure fulfils the requirements established in Specification REQ-021-05-01 through REQ-021-05-06 and implements the guarantee period terms of RFP §2.10 and §2.11.

**Responsible Party:** Project Manager (source: _CONTEXT.md)

---

## Prerequisites

### Required Upstream Deliverables (from _DEPENDENCIES.md)

| Prerequisite | Deliverable | Condition Required |
|---|---|---|
| Construction Completion Certificate issued | DEL-020-02 (Final Inspection & CCC) | CCC must be issued and signed by Owner before warranty period begins |
| Performance bond in effect | DEL-021-02 (Performance & Payment Bonds) | Performance bond must remain in effect during warranty period |
| Contractor insurance in effect | DEL-021-03 (Insurance Package) | Contractor insurance should remain in effect during warranty period |
| Contract terms established | DEL-021-04 (Contract Execution — CCDC 14-2013) | Contract warranty terms must be understood and accessible |
| Commissioning & Closeout complete | PKG-020 | Substantial completion triggers warranty period start |

### Required Reference Materials

| Reference | Sections | Accessibility |
|---|---|---|
| AB-2026-01424-WDMLRL RFP.pdf | §2.10 (Guarantee Period), §2.11 (Deficiency Holdback) | Accessible |
| Executed CCDC 14-2013 Contract | Warranty and guarantee clauses as executed | ASSUMPTION: Available at contract execution; location TBD at time of procedure execution |
| Contractor contact information (key personnel, emergency contacts) | — | TBD — source and timing for obtaining Contractor warranty-period contact information to be determined. **ASSUMPTION:** This is a CCC-phase deliverable to be obtained from the Contractor at or before CCC (Semantic Lensing item B-001). Consider whether DEL-021-04 (Contract Execution) should produce this as an output, or whether it is a standalone CCC-phase requirement. See Guidance OI-002 for scheduling context. |
| DEL-021-04 (Contract Execution) | Executed contract terms | Available upon completion of DEL-021-04 |

### Required Administrative Setup

- Deficiency log template established (TBD format; see Specification REQ-021-05-05 and Guidance OI-009 for format standards).
- Deficiency Holdback ledger established.
- Warranty period register template available.

---

## Steps

### Phase 1: Warranty Period Initiation (at CCC Issuance)

**Step 1.1 — Record CCC Date and Establish Warranty Period Register**

Upon receipt of the signed Construction Completion Certificate (CCC) from the Owner:

1. Record the CCC date as the Warranty Period Start Date.
2. Calculate the Warranty Period Expiry Date: CCC date + 2 calendar years. (Source: RFP §2.10.2)
3. Create the Warranty Period Register documenting:
   - CCC date (start date)
   - Warranty period expiry date
   - Project ID: AB-2026-01424-WDMLRL-2026-Claude
   - Responsible Project Manager name and contact
   - Contractor name and contact information

**Source:** RFP §2.10.2; Specification REQ-021-05-01.

---

**Step 1.2 — Confirm Contractor Contact Information**

1. Record primary Contractor contact(s) for warranty period: name, phone, email, after-hours emergency contact.
2. Confirm that the Contractor's representative is aware of the 10-day rectification obligation. (Source: RFP §2.10.6)
3. File Contractor contact information in the Warranty Period Register.

**Note (Semantic Lensing item B-001):** The source and timing for obtaining Contractor warranty-period contact information is TBD. This step requires the information to be available at CCC; determine in advance whether DEL-021-04 (Contract Execution) will produce this as an output or whether a separate request to the Contractor is required at CCC. See Prerequisites.

**Source:** Guidance C-3; RFP §2.10.6.

---

**Step 1.3 — Verify Bond and Insurance Continuation**

1. Obtain written confirmation from the Contractor (or bond/insurance provider) that the performance bond (DEL-021-02) remains in effect during the warranty period.
2. Obtain written confirmation that contractor insurance (DEL-021-03) remains in effect during the warranty period.
3. File confirmation records in the Warranty Period Register.
4. If continuation is not confirmed: escalate to Owner and review CCDC 14-2013 contract terms (DEL-021-04). ASSUMPTION: Continuation is expected per _DEPENDENCIES.md; exact terms subject to executed contract.

**Source:** _DEPENDENCIES.md; Specification REQ-021-05-06; Guidance C-5.

---

**Step 1.4 — Establish Deficiency Holdback Ledger**

1. Confirm with the Owner whether any Deficiency Holdback amounts are being retained from the final payment.
2. Record any initial holdback amount and the specific deficiency items it is associated with.
3. Open the Deficiency Holdback Ledger with the following fields per item:
   - Deficiency ID
   - Description
   - Estimated holdback value (valuation method TBD -- see Specification REQ-021-05-04 and Guidance OI-006)
   - Date identified
   - Date Owner written instruction issued
   - Target rectification date (instruction date + 10 days)
   - Date remediation completed
   - Date Owner approved
   - Amount released
4. Retain holdback until deficiencies are corrected and approved by Owner. (Source: RFP §2.11.2)

**Note:** The ledger fields above are aligned with the artifact description in Datasheet Construction (Semantic Lensing item E-001) to ensure traceability between the descriptive and operational views of this artifact.

**Source:** RFP §2.11.1, §2.11.2; Specification REQ-021-05-04.

---

**Step 1.5 — Schedule Post-Completion Inspections (ASSUMPTION)**

ASSUMPTION: The following inspection schedule is recommended based on standard practice; the specific schedule is not prescribed by the RFP and is subject to Owner agreement. The inspection schedule should be confirmed with the Owner at CCC rather than treated as a default (Semantic Lensing item A-004; see Guidance OI-002).

1. Confirm with the Owner a proactive inspection schedule for the warranty period. Suggested schedule:
   - 6-month inspection
   - 12-month inspection
   - 20-22 month inspection (near warranty expiry, to allow time for remediation before period end)
2. Document the agreed inspection dates in the Warranty Period Register.
3. If the Owner does not agree to a proactive schedule, document the decision and proceed with reactive deficiency management only.

**Source:** Guidance C-2; _CONTEXT.md Success Criteria ("Post-completion inspections conducted").

---

### Phase 2: Deficiency Management (Ongoing During Warranty Period)

**Step 2.1 — Deficiency Identification and Logging**

When the Owner identifies a defect or deficiency through use, tests, or inspection:

1. Record the deficiency in the Deficiency Log:
   - Deficiency ID (sequential)
   - Date identified
   - Description (location, nature of defect)
   - How discovered (use, test, inspection)
   - ASSUMPTION: Severity classification (safety-critical / functional / cosmetic) — TBD framework (see Guidance OI-001 and Specification REQ-021-05-02)
2. Assess whether the deficiency constitutes an emergency condition requiring immediate action. (Source: RFP §2.10.5; see Guidance C-4 for emergency vs. standard judgment criteria.)

**Source:** RFP §2.10.4; Specification REQ-021-05-01.

---

**Step 2.2 — Issue Owner Deficiency Notification to Contractor**

1. Notify the Contractor immediately by available means (phone, email). (Source: RFP §2.10.4)
2. Confirm notification in writing (written instruction letter or email with read receipt), addressed to the Contractor's designated representative.
3. The written instruction must:
   - Identify the deficiency (Deficiency ID, location, description)
   - State the requirement to rectify within 10 days (Source: RFP §2.10.6)
   - Reference the guarantee obligation (RFP §2.10 / CCDC 14-2013)
4. Record the written instruction date and method in the Deficiency Log and Holdback Ledger.
5. Calculate the 10-day deadline and record it: **Deadline = Written Instruction Date + 10 calendar days**.

**Source:** RFP §2.10.4, §2.10.6; Specification REQ-021-05-02.

---

**Step 2.3 — Emergency Deficiency Response**

If the deficiency presents an immediate risk of serious damage, injury, or loss of life (see Guidance C-4 for judgment criteria):

1. The Owner may immediately perform or cause to be performed the necessary work. (Source: RFP §2.10.5)
2. Notify the Contractor as soon as practicable by available means.
3. Document all emergency work performed, costs incurred, and notifications sent.
4. Recover all emergency work costs from the Contractor. (Source: RFP §2.10.7)

**Step 2.3a — Verify Owner-Performed Emergency Work (Semantic Lensing item X-001)**

When the Owner (rather than the Contractor) performs or causes emergency work to be performed:

1. Document the scope of Owner-performed work (description, location, materials used, labor involved).
2. Record all costs incurred by the Owner for the emergency work (labor, materials, equipment, subcontractors).
3. Confirm that the Contractor was notified of the emergency work scope and cost.
4. Verify that cost documentation is sufficient to support recovery from the Contractor (per RFP §2.10.7).
5. Update the Deficiency Holdback Ledger if holdback funds are used for cost recovery (per RFP §2.11.3).
6. Record the verification completion in the Deficiency Log.

**Source:** RFP §2.10.5, §2.10.7; Specification REQ-021-05-03; Semantic Lensing item X-001.

---

**Step 2.4 — Monitor Contractor Rectification**

1. Track the 10-day deadline for each open deficiency.
2. If the Contractor completes rectification within the 10-day window:
   - Inspect the remediated work.
   - Verify remediation quality against the Contract Documents (acceptance criteria TBD -- see Specification Verification table, items F-001 and F-003).
   - Obtain Owner approval of the remediation (approval method TBD -- see Specification Verification table, item F-001).
   - Record completion date and approval date in the Deficiency Log and Holdback Ledger.
   - Release the associated holdback amount to the Contractor. (Source: RFP §2.11.4)
3. If the Contractor does **not** complete rectification within the 10-day window:
   - Record the missed deadline in the Deficiency Log.
   - The Owner may take whatever action is necessary to complete the work. (Source: RFP §2.10.6)
   - Document all costs incurred by Owner for work completion.
   - Withdraw from the Deficiency Holdback sufficient to cover costs. (Source: RFP §2.11.3)
   - Recover any costs exceeding the holdback directly from the Contractor. (Source: RFP §2.10.7, §2.10.8)

**Step 2.4a — Verify Owner-Performed Default Remediation (Semantic Lensing item X-001)**

When the Owner performs work after Contractor failure to rectify within 10 days:

1. Document the scope of Owner-performed remediation work (description, location, materials, labor).
2. Record all costs incurred by the Owner.
3. Confirm that the Contractor was notified of the Owner's intent to perform work (per RFP §2.10.6).
4. Verify that cost documentation is sufficient to support recovery from the Contractor and/or holdback withdrawal.
5. Update the Deficiency Holdback Ledger to reflect any holdback withdrawals (per RFP §2.11.3).
6. If applicable, document any consequential damages for cost recovery (see Guidance P-4).
7. Record the verification completion in the Deficiency Log.

**Source:** RFP §2.10.6, §2.10.7, §2.11; Specification REQ-021-05-02, REQ-021-05-04; Semantic Lensing item X-001.

---

**Step 2.5 — Conduct Scheduled Inspections**

At each scheduled inspection (per Step 1.5 agreed schedule):

1. Conduct physical inspection of the facility. ASSUMPTION: Inspection should cover at minimum: structural elements, roof/envelope, mechanical systems, plumbing, electrical systems, concrete floors and steel plate embedments, wash bay drainage and mud sump, service pit, mezzanine, overhead cranes, cistern and pump systems.
2. Document all findings in an inspection report.
3. For each deficiency found, proceed with Step 2.1 through Step 2.4.

**Source:** RFP §2.10.4; _CONTEXT.md Success Criteria.

---

**Step 2.6 — Mid-Period Administrative Review (ASSUMPTION; Semantic Lensing item X-002)**

ASSUMPTION: Whether a formal mid-period administrative review is conducted is TBD (see Guidance C-8). If adopted, conduct at approximately the 12-month mark:

1. Review overall warranty administration status:
   - Deficiency Log currency and completeness.
   - Notification timeliness (all written instructions issued promptly).
   - Holdback Ledger accuracy and reconciliation.
   - Bond and insurance status re-confirmation.
2. Review outstanding open items and their aging.
3. Assess adequacy of documentation practices against established format standards (if any; see Guidance OI-009).
4. Document lessons learned from the first year of administration.
5. File the administrative review report in the Warranty Period Register.

**Source:** Guidance C-8; Semantic Lensing item X-002.

---

### Phase 3: Warranty Period Closure

**Step 3.1 — Final Deficiency Review (Before Warranty Expiry)**

No later than 60 days before the warranty expiry date (ASSUMPTION: 60-day lead time is not prescribed by RFP; recommended as best practice to allow remediation time):

1. Review the Deficiency Log — identify any open or unresolved items.
2. Issue written instructions for any remaining open deficiencies.
3. Confirm all 10-day deadlines will fall within the warranty period.
4. Conduct the near-expiry inspection (Step 2.5 — 20-22 month inspection).

**Source:** _CONTEXT.md Success Criteria ("Warranty expiration properly managed"); Guidance C-2.

---

**Step 3.2 — Warranty Expiration Checklist**

At warranty period expiry:

1. Complete the Warranty Expiration Checklist, confirming:
   - All identified deficiencies have been remediated and Owner-approved.
   - Deficiency Holdback Ledger is fully reconciled (zero unresolved items; see Specification Verification table, item A-003).
   - All holdback amounts have been released or cost-recovered.
   - All documentation is complete and filed.
   - Bond and insurance coverage status is confirmed (if applicable at expiry).
2. ASSUMPTION: Obtain Owner written acknowledgment that all guarantee obligations have been discharged. (Trigger for full holdback release per RFP §2.11.4; final release may require Owner written approval — see Guidance OI-005.)

**Source:** RFP §2.11.4; _CONTEXT.md Success Criteria; Guidance OI-005.

---

**Step 3.3 — Final Holdback Release**

1. Upon Owner approval of all deficiency corrections:
   - Release all remaining Deficiency Holdback funds to Contractor. (Source: RFP §2.11.4)
   - Record final release in Holdback Ledger.
2. Obtain Owner written confirmation of final payment / holdback release.
3. Archive all warranty period documentation.

**Source:** RFP §2.11.4; Specification REQ-021-05-04.

---

**Step 3.4 — Archive Warranty Documentation**

1. Compile all warranty period records into a complete archive:
   - Warranty Period Register (signed, with CCC date, start/expiry dates)
   - Deficiency Log (complete, all items resolved)
   - All deficiency notification letters
   - All remediation completion and Owner approval records
   - Deficiency Holdback Ledger (fully reconciled)
   - All inspection reports
   - Mid-period administrative review report (if conducted; Step 2.6)
   - Warranty Expiration Checklist
   - Bond and insurance confirmation records
2. Archive per project record retention policy. Retention period: TBD (see Specification REQ-021-05-05 and Guidance OI-004). ASSUMPTION: Retain for at least the applicable Alberta statutory limitation period for construction claims.

**Source:** Specification REQ-021-05-05; MEMORY.md; Guidance C-7.

---

## Verification

| Step | Verification Check | Method |
|---|---|---|
| Step 1.1 | Warranty Period Register exists with CCC date and expiry date | Review register |
| Step 1.2 | Contractor contact information recorded | Review register |
| Step 1.3 | Bond and insurance continuation confirmed in writing | Review confirmation records |
| Step 1.4 | Deficiency Holdback Ledger opened and reconciled with initial holdback | Review ledger |
| Step 1.5 | Inspection schedule agreed with Owner and documented (or reactive-only decision documented) | Review register |
| Step 2.2 | Every deficiency has a written notification record with date | Review Deficiency Log vs. notification file |
| Step 2.3a | Owner-performed emergency work documented with costs and Contractor notification | Review emergency work records |
| Step 2.4 | 10-day deadline tracked and documented for every deficiency | Review Deficiency Log deadlines |
| Step 2.4 | Holdback updated at each deficiency resolution | Review Holdback Ledger |
| Step 2.4a | Owner-performed default remediation documented with costs and holdback withdrawals | Review default remediation records |
| Step 2.6 | Mid-period administrative review completed (if adopted) | Review administrative review report |
| Step 3.1 | Near-expiry review completed before warranty end | Review inspection report date |
| Step 3.2 | Warranty Expiration Checklist completed | Review checklist |
| Step 3.3 | Final holdback fully released and documented | Review final Holdback Ledger entry |
| Step 3.4 | Complete archive assembled | Review archive completeness checklist |

---

## Records

| Record | Custodian | Timing | Retention |
|---|---|---|---|
| Warranty Period Register | Project Manager | Created at CCC; maintained throughout | TBD (post-project; see Guidance OI-004) |
| Deficiency Log | Project Manager | Ongoing during warranty period | TBD (post-project; see Guidance OI-004) |
| Deficiency Notification Letters | Project Manager | Per deficiency event | TBD (post-project; see Guidance OI-004) |
| Remediation Completion & Owner Approval Records | Project Manager | Per deficiency closure | TBD (post-project; see Guidance OI-004) |
| Deficiency Holdback Ledger | Project Manager | Ongoing; final reconciliation at period end | TBD (post-project; see Guidance OI-004) |
| Post-Completion Inspection Reports | Project Manager | Per scheduled inspection | TBD (post-project; see Guidance OI-004) |
| Bond & Insurance Continuation Confirmations | Project Manager | At warranty period start | TBD (post-project; see Guidance OI-004) |
| Mid-Period Administrative Review Report | Project Manager | At ~12-month mark (if adopted) | TBD (post-project; see Guidance OI-004) |
| Warranty Expiration Checklist | Project Manager | At warranty period end | TBD (post-project; see Guidance OI-004) |
| Final Holdback Release Confirmation | Project Manager | At warranty period end | TBD (post-project; see Guidance OI-004) |
| Owner-Performed Work Documentation | Project Manager | Per emergency or default remediation event | TBD (post-project; see Guidance OI-004) |
