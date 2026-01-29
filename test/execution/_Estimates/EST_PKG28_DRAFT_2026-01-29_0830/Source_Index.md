# Source Index — PKG-28 Design Verification Estimate

**Snapshot ID:** EST_PKG28_DRAFT_2026-01-29_0830
**Package Scope:** PKG-28 Design Verification
**Date:** 2026-01-29

---

## Source Discovery Summary

This index catalogs all pricing and quantity sources discovered during the estimate preparation phase, listed in priority order per AGENT_ESTIMATING protocol (Phase 2.2).

**Priority hierarchy:**
1. Explicit pricing sources (quotes, budgets, proposals)
2. Rate tables / cost libraries
3. Quantity sources (datasheets, specifications, procedures)
4. Embedded fallback model

---

## 1. Explicit Pricing Sources (Highest Priority)

**Status:** **NONE FOUND**

**Search performed:**
- Checked PKG-28 deliverable definitions in decomposition
- Searched for vendor quotes for independent design verification (IDV) services
- Searched for VFPA coordination cost data or similar project references
- Checked `_Estimates/_RateTables/` for engineering review rates

**Findings:**
- No vendor quotes for IDV services discovered
- No VFPA coordination cost references found
- No budgetary proposals or cost estimates for design verification services

**Impact:** Cannot price line items using project-specific vendor quotes. Must proceed to next source priority level.

**Resolution path:** Obtain budgetary quotes from independent engineering review firms, then re-run estimate.

---

## 2. Rate Tables / Cost Libraries

**Status:** **NONE FOUND**

**Search performed:**
- Checked `_Estimates/_RateTables/` directory for engineering labor rates
- Searched for coordination service rate tables
- Checked for BIM coordination service rates

**Findings:**
- `_Estimates/_RateTables/` directory exists but does not contain engineering review or coordination rates
- No project-specific rate tables for design verification services discovered

**Impact:** Cannot price line items using project rate tables. Must proceed to next source priority level.

**Resolution path:** Add rate tables to `_Estimates/_RateTables/` directory in CSV or XLSX format with columns: Description, Unit, UnitRate, Currency, Date. Then re-run estimate.

---

## 3. Quantity Sources

**Status:** **FOUND** — Decomposition provides scope descriptions

**Search performed:**
- Read PKG-28 package definition in decomposition
- Extracted deliverable types, artifact descriptions, and implied scope

**Findings:**

### DEL-28.01: Independent Design Verification Reports
- **Type:** Report
- **Artifacts:** IDV reports (by discipline/submission stage)
- **Implied Scope:** Design verification reviews across multiple disciplines at multiple submission stages
- **Quantities NOT Specified:**
  - Which disciplines require IDV
  - Review depth and approach
  - Number of submission stages requiring IDV
  - Iteration expectations

### DEL-28.02: VFPA IP Review Responses
- **Type:** Report
- **Artifacts:** IP review response documents
- **Implied Scope:** Formal responses to Vancouver Fraser Port Authority project review comments
- **Quantities NOT Specified:**
  - Number of VFPA submission cycles
  - Expected comment volume
  - Response format and complexity

### DEL-28.03: Design Coordination Installation & Test Records
- **Type:** Record
- **Artifacts:** Inter-discipline coordination records, clash detection reports, RFI logs
- **Implied Scope:** Design coordination across 36 packages and 210 deliverables
- **Quantities NOT Specified:**
  - Design duration and coordination frequency
  - BIM model complexity and clash detection volume
  - Expected RFI count

**Impact:** Quantities are primarily **deliverable types and descriptions** rather than effort-based service quantities. Service effort (review hours, coordination months, meeting count) must be estimated based on typical project experience.

**Limitation:** Cannot create detailed effort-based estimates without additional input from Employer on IDV requirements and VFPA coordination expectations.

**Resolution path:**
1. Clarify IDV requirements with Employer (disciplines, depth, stages)
2. Obtain VFPA project review requirements
3. Develop design schedule with coordination milestones

---

## 4. Embedded Fallback Model

**Status:** **ACTIVE** (primary pricing basis)

**Trigger:** No project-specific pricing sources or rate tables found (Sections 1-2 above).

**Application:** Per AGENT_ESTIMATING STRUCTURE section (Fallback Typical Model), the fallback model will be used to:
- Provide placeholder allowances for design verification services
- Apply default factors for indirects and project management
- Apply default contingency percentages by CBS bucket

**Method:**
- Line items priced using fallback model will be marked as `Method=ALLOWANCE` or `Method=PARAMETRIC`
- Confidence will be set to `LOW` or `MED`
- Source reference will cite applicable Decision Log entry (e.g., `SourceRef=D-005`)

**Fallback Model Components:**

### Design Verification Allowance Guidance:
- IDV services: $10,000-$15,000 per discipline per submission stage (typical)
- VFPA IP review: $15,000-$25,000 per major submission cycle (typical)
- Design coordination: $4,000-$6,000 per month of active design (typical)
- BIM coordination: $2,000-$3,000 per month (typical)
- RFI management: $75-$150 per RFI (typical)

### Indirects Factors (from AGENT_ESTIMATING):
- Construction Indirects (CI) = 18% of notional engineering review allocation
- Procurement (P) = 2% of third-party engineering services
- EPCM/PM = 6% of engineering base

### Contingency Baseline % (from AGENT_ESTIMATING):
- Engineering (E), PM, Procurement (P): 10%
- Construction Indirects (CI): 20%
- **Adjustment:** +5% if bucket allowance share >= 50%; +10% if >= 80%

**Disclosure:** All uses of fallback model are explicitly documented in Decision_Log.md (D-005, D-006, D-008, D-010, D-011) and will be flagged in QA_Report.md.

---

## Source Selection Decision

**Decision Reference:** D-005 (Decision_Log.md)

**Primary Basis:** Fallback typical model (no project-specific sources available)

**Confidence:** LOW

**Recommendation:** Acquire vendor quotes for IDV services and clarify VFPA coordination requirements to replace fallback allowances in next estimate iteration.

---

## Deliverables Inventory — Source Coverage

| Deliverable ID | Name | Scope Found | Pricing Found | Coverage Status |
|----------------|------|-------------|---------------|-----------------|
| DEL-28.01 | Independent Design Verification Reports | Artifact type only | None | Fallback |
| DEL-28.02 | VFPA IP Review Responses | Artifact type only | None | Fallback |
| DEL-28.03 | Design Coordination Records | Artifact type only | None | Fallback |

**Total Deliverables:** 3
**With Explicit Quotes:** 0 (0%)
**With Rate Table Pricing:** 0 (0%)
**With Fallback Pricing:** 3 (100%)

---

## Next Steps to Improve Source Coverage

1. **Clarify IDV requirements** with Employer:
   - Which disciplines require independent design verification?
   - What review depth is expected (calculation check, design review, full independent analysis)?
   - At which submission stages is IDV required?
   - What iteration/re-review is expected?

2. **Request vendor budgetary quotes** for:
   - Independent design verification services (by discipline)
   - Third-party engineering review services
   - BIM coordination and clash detection services

3. **Engage VFPA** to understand project review requirements:
   - Submission schedule and review cycles
   - Expected comment volume and response format
   - Coordination meeting requirements

4. **Develop project rate tables** for:
   - Engineering review labor rates (senior reviewer, discipline lead)
   - Coordination labor rates (coordinator, administrator)
   - BIM coordination service rates

5. **Add rate tables** to `_Estimates/_RateTables/` directory in standardized format

---

**Source Index Prepared By:** Estimating Agent
**Date:** 2026-01-29
**Status:** Complete (ready for pricing phase)
