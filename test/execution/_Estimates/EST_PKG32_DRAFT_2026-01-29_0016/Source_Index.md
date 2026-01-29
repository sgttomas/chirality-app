# Source Index — PKG-32 Regulatory & Permits

**Snapshot ID:** EST_PKG32_DRAFT_2026-01-29_0016
**Date:** 2026-01-29
**Prepared By:** Estimating Agent (Automated Pipeline)

---

## Source Discovery Summary

This index lists all sources discovered and evaluated for pricing and quantity extraction during the estimating process.

**Search Strategy:**
1. Explicit pricing sources (vendor quotes, budgetary quotes, proposals)
2. Rate tables and cost libraries
3. Deliverable documents (Datasheet, Specification, Guidance, Procedure)
4. Fallback typical model (when no project-specific sources available)

**Discovery Result:** No project-specific pricing sources found; fallback typical model used.

---

## 1. Explicit Pricing Sources (Vendor Quotes, Budgetary Quotes)

**Status:** NOT FOUND

**Search Performed:**
- Checked deliverable `_REFERENCES.md` files for quote references: None found
- Searched execution workspace for files matching: `quote`, `proposal`, `budget`, `pricing`: None found
- Searched for permit fee schedules or consultant budgets: None found

**Impact:** Cannot use QUOTE method for line item pricing

---

## 2. Rate Tables and Cost Libraries

**Status:** NOT FOUND

**Search Performed:**
- Checked `execution/_Estimates/_RateTables/`: Folder exists but empty
- Searched workspace for files matching: `rate`, `unit cost`, `cost library`: None found
- Searched for labor rate tables, permit fee schedules: None found

**Impact:** Cannot use RATE_TABLE method for line item pricing

---

## 3. Deliverable Documents (Quantity and Scope Sources)

**Status:** FOUND — Used for scope understanding and qualitative quantity extraction

### PKG-32 Deliverable Folder Structure

**Path:** `/Users/ryan/ai-env/projects/chirality-app/test/execution/PKG-32_Regulatory_and_Permits/1_Working/`

**Deliverables (8 total):**

1. **DEL-32.01 Permit Applications**
   - Files: `_CONTEXT.md`, `_STATUS.md`, `Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md`
   - Scope: Contractor permit application preparation and submission
   - Quantity signals: "Contractor-responsible permits" (count TBD), regulatory authorities listed (VFPA, DFO, Transport Canada, City of Surrey, etc.), application process described
   - Cost drivers extracted: Engineering hours for permit prep, internal review, Employer review, authority submission, tracking
   - Pricing data: None

2. **DEL-32.02 Permits**
   - Files: `_CONTEXT.md`, `_STATUS.md`, `Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md`
   - Scope: Issued permit receipt, review, tracking, condition identification, distribution
   - Quantity signals: "Building permits, construction permits, environmental permits" (count TBD)
   - Cost drivers extracted: PM hours for permit receipt, review, tracking, distribution
   - Pricing data: None

3. **DEL-32.03 VFPA PER Compliance Installation & Test Records**
   - Files: `_CONTEXT.md`, `_STATUS.md`, `Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md`
   - Scope: VFPA Project and Environmental Review (PER) compliance documentation
   - Quantity signals: "PER condition compliance documentation" (condition count TBD)
   - Cost drivers extracted: QA/QC hours for compliance monitoring, documentation, reporting
   - Pricing data: None

4. **DEL-32.04 DFO Compliance Installation & Test Records**
   - Files: `_CONTEXT.md`, `_STATUS.md`, `Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md`
   - Scope: Department of Fisheries and Oceans (DFO) permit compliance documentation
   - Quantity signals: "DFO permit compliance documentation" (condition count TBD)
   - Cost drivers extracted: QA/QC hours for compliance monitoring, documentation, reporting (marine works focus)
   - Pricing data: None

5. **DEL-32.05 Transport Canada Compliance Installation & Test Records**
   - Files: `_CONTEXT.md`, `_STATUS.md`, `Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md`
   - Scope: Transport Canada compliance documentation (rail and marine interface)
   - Quantity signals: "TC compliance documentation" (condition count TBD)
   - Cost drivers extracted: QA/QC hours for compliance monitoring, documentation, reporting
   - Pricing data: None

6. **DEL-32.06 Code Compliance Installation & Test Records**
   - Files: `_CONTEXT.md`, `_STATUS.md`, `Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md`
   - Scope: Building code, fire code, electrical code compliance records
   - Quantity signals: "Code compliance certificates, inspection records" (inspection count TBD)
   - Cost drivers extracted: QA/QC hours for inspection coordination, documentation, closeout
   - Pricing data: None

7. **DEL-32.07 Authority & Stakeholder Correspondence Register**
   - Files: `_CONTEXT.md`, `_STATUS.md`, `Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md`
   - Scope: Correspondence tracking log
   - Quantity signals: "Correspondence log, meeting minutes register, RFI register" (entry count scales with project complexity)
   - Cost drivers extracted: PM hours for register setup, maintenance, update
   - Pricing data: None

8. **DEL-32.08 Authority & Stakeholder Correspondence Copies**
   - Files: `_CONTEXT.md`, `_STATUS.md`, `Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md`
   - Scope: Correspondence document copies and filing
   - Quantity signals: "Email/letter copies, submissions, approvals, meeting minutes" (document count TBD)
   - Cost drivers extracted: PM hours for document filing, archiving, closeout package preparation
   - Pricing data: None

**Quantities Extracted (Qualitative):**
- 8 deliverables (document/record types)
- Permit types identified: VFPA PER, DFO, Transport Canada, building, construction, environmental, fire (count TBD)
- Regulatory authorities identified: VFPA, DFO, Transport Canada, City of Surrey, WorkSafeBC, fire authority (count TBD)
- Compliance condition categories identified: pre-construction, during-construction, post-construction, operational (condition count TBD)
- Correspondence types identified: applications, RFIs, submittals, approvals, inspection requests, meeting minutes (entry count TBD)

**Quantities NOT Extracted (Missing Data):**
- Number of distinct permits required (count TBD — depends on Employer's Requirements)
- Number of permit conditions per permit (TBD — depends on issued permits)
- Engineering hours required per deliverable (TBD — no resource plan)
- PM/QA hours required per deliverable (TBD — no resource plan)
- Number of authority meetings/inspections (TBD — project schedule dependent)
- Permit fee amounts (TBD — authority fee schedules not available)
- Consultant scope and hours (TBD — procurement not complete)

**Impact:** Cannot create unit-rate-based QTO; forced to use LS allowances based on typical regulatory/permitting package complexity

---

## 4. Decomposition File

**Path:** `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`

**Content Used:**
- Section 5 PKG-32 (lines 699-717): Package description, deliverable list, deliverable types, anticipated artifacts
- Section 6 Objectives (line 785): OBJ-6 Regulatory Compliance mapped to PKG-32
- Section 1.1 Project Overview: Project parameters, location, scope

**Quantities Extracted:**
- 8 deliverables in PKG-32
- Project complexity indicators: 1M MT/annum throughput, 45,000 MT storage, 32 railcar stations, marine loading → suggests multi-authority, multi-permit project

**Pricing Data:** None

---

## 5. Employer's Requirements (Referenced but Not Accessible)

**Referenced Documents:**
- Volume 2 Part 1: Employer's Requirements (general)
- Volume 2 Part 2: Employer's Requirements (technical)
- Volume 2 Part 3: Employer's Requirements (environmental/regulatory)

**Status:** Referenced in deliverable documents but not read during estimate preparation

**Expected Content:**
- Permit responsibility matrix (Contractor vs Employer)
- Required permit list
- Regulatory authority requirements
- Permit submission schedule requirements

**Impact:** Cannot verify permit count, Contractor vs Employer scope split, or specific permit requirements; relying on deliverable document assumptions

---

## 6. Fallback Typical Model (Used)

**Source:** AGENT_ESTIMATING.md, lines 623-714 (Fallback Typical Model section)

**Components Used:**
- Allowance placeholders for engineering, PM, QA/QC hours (A-3201 through A-3213)
- Indirects factors: P=2%, PM=6%, COM=3% (D-3209)
- Contingency baseline by CBS with allowance-heavy adjustment (D-3206)

**Labeling:**
- All line items using fallback model labeled: `Method=ALLOWANCE` or `Method=PARAMETRIC`
- All line items using fallback model labeled: `Confidence=LOW` or `Confidence=MED`
- All line items reference decision IDs (D-32XX) or assumption IDs (A-32XX) in `SourceRef` field

**Transparency:** Fallback model use disclosed in BOE.md, Decision_Log.md (D-3208), and this Source_Index.md

---

## Source Hierarchy Applied

**Pricing Method Distribution (by base cost $):**

| Method | Base Cost | % of Total |
|--------|-----------|------------|
| QUOTE | $0 | 0% |
| RATE_TABLE | $0 | 0% |
| ALLOWANCE | $210,000 | 85% |
| PARAMETRIC | $38,000 | 15% |
| **Total Base** | **$248,000** | **100%** |

---

## Recommendations for Next Estimate Run

To improve estimate quality and reduce reliance on fallback model:

1. **Provide vendor quotes or budgetary pricing:**
   - Engage regulatory/environmental consultants for preliminary scope/budget estimates
   - Obtain permit fee schedules from applicable authorities (VFPA, DFO, Transport Canada, City of Surrey)

2. **Populate rate tables:**
   - Add labor rates (engineering, PM, QA/QC) to `_Estimates/_RateTables/`
   - Add consultant/specialist hourly rates
   - Add permit fee schedules

3. **Clarify Employer's Requirements:**
   - Provide permit responsibility matrix (Contractor vs Employer permits)
   - Provide required permit list
   - Provide permit submission schedule

4. **Develop resource plan:**
   - Estimate engineering hours per permit application (by permit type)
   - Estimate PM hours for permit tracking and coordination
   - Estimate QA/QC hours for compliance documentation (by authority)
   - Estimate consultant hours for permit support

---

**Prepared By:** Estimating Agent
**Date:** 2026-01-29 00:16
