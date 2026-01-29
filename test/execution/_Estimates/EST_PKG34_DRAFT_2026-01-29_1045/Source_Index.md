# Source Index — PKG-34 Coordination & Interfaces Estimate

**Snapshot ID:** EST_PKG34_DRAFT_2026-01-29_1045
**Package Scope:** PKG-34 Coordination & Interfaces
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
- Checked PKG-34 deliverable definitions in decomposition
- Searched for coordination service provider quotes
- Searched for trenchless monitoring service quotes
- Checked `_Estimates/_RateTables/` for coordination or monitoring rates

**Findings:**
- No coordination service provider quotes discovered
- No trenchless monitoring quotes found
- No interface management cost references found
- No budgetary proposals or cost estimates for coordination services

**Impact:** Cannot price line items using project-specific vendor quotes. Must proceed to next source priority level.

**Resolution path:** Obtain budgetary quotes from coordination service providers and survey/monitoring firms, then re-run estimate.

---

## 2. Rate Tables / Cost Libraries

**Status:** **NONE FOUND**

**Search performed:**
- Checked `_Estimates/_RateTables/` directory for coordination labor rates
- Searched for monitoring service rate tables
- Checked for interface management rate tables

**Findings:**
- `_Estimates/_RateTables/` directory exists but does not contain coordination or monitoring rates
- No project-specific rate tables for interface management discovered

**Impact:** Cannot price line items using project rate tables. Must proceed to next source priority level.

**Resolution path:** Add rate tables to `_Estimates/_RateTables/` directory in CSV or XLSX format with columns: Description, Unit, UnitRate, Currency, Date. Then re-run estimate.

---

## 3. Quantity Sources

**Status:** **FOUND** — Decomposition provides scope descriptions

**Search performed:**
- Read PKG-34 package definition in decomposition
- Extracted deliverable types, artifact descriptions, and implied scope

**Findings:**

### DEL-34.01: Coordination Meeting Installation & Test Records
- **Type:** Record
- **Artifacts:** Weekly Terminal coordination meeting minutes
- **Implied Scope:** Ongoing coordination meetings throughout construction
- **Quantities NOT Specified:**
  - Construction duration (meeting count dependent)
  - Meeting frequency confirmation
  - Administrative effort per meeting

### DEL-34.02: Interface Agreements
- **Type:** Document
- **Artifacts:** Interface agreements (FSPL-TI, Metro Vancouver, utilities)
- **Implied Scope:** Formal interface agreements with third parties
- **Quantities NOT Specified:**
  - Complete list of required interface agreements
  - Complexity and negotiation effort per interface
  - Legal/commercial review requirements

### DEL-34.03: Marine Coordination Installation & Test Records
- **Type:** Record
- **Artifacts:** Notices to mariners, marine coordination records
- **Implied Scope:** Port authority coordination for marine construction works
- **Quantities NOT Specified:**
  - Marine works duration
  - Notice to Mariners frequency
  - VFPA coordination requirements

### DEL-34.04: Security Compliance Installation & Test Records
- **Type:** Record
- **Artifacts:** CBSA/TC security compliance records
- **Implied Scope:** Security compliance documentation for port security zone
- **Quantities NOT Specified:**
  - Security zone requirements detail
  - TWIC/MSIC requirements
  - Access management scope

### DEL-34.05: Trenchless Crossing Monitoring Reports
- **Type:** Report
- **Artifacts:** Settlement monitoring reports, condition monitoring reports
- **Implied Scope:** Monitoring for HDD/trenchless crossings during installation
- **Quantities NOT Specified:**
  - Number of trenchless crossings (inferred 2-4 from PKG-03)
  - Monitoring frequency and duration
  - Stakeholder reporting requirements

**Impact:** Quantities are primarily **deliverable types and descriptions** rather than effort-based service quantities. Service effort (hours, months, meetings) must be estimated based on typical project experience.

**Limitation:** Cannot create detailed effort-based estimates without additional input on construction schedule, interface scope, and crossing count.

**Resolution path:**
1. Obtain project construction schedule for duration-based calculations
2. Clarify interface agreement requirements with Employer
3. Coordinate with PKG-03 for trenchless crossing details

---

## 4. Embedded Fallback Model

**Status:** **ACTIVE** (primary pricing basis)

**Trigger:** No project-specific pricing sources or rate tables found (Sections 1-2 above).

**Application:** Per AGENT_ESTIMATING STRUCTURE section (Fallback Typical Model), the fallback model will be used to:
- Provide placeholder allowances for coordination and monitoring services
- Apply default factors for indirects and project management
- Apply default contingency percentages by CBS bucket

**Method:**
- Line items priced using fallback model will be marked as `Method=ALLOWANCE` or `Method=PARAMETRIC`
- Confidence will be set to `LOW` or `MED`
- Source reference will cite applicable Assumption or Decision Log entry (e.g., `SourceRef=A-001`)

**Fallback Model Components:**

### Coordination & Interface Allowance Guidance:
- Weekly coordination meetings: $600-$750 per meeting (administrative effort)
- Interface agreements: $20,000-$35,000 per major interface (negotiation, documentation)
- Marine coordination: $4,000-$5,000 per month of active marine works
- Security compliance: $1,500-$2,000 per month of construction
- Trenchless monitoring: $20,000-$35,000 per crossing location (survey, instrumentation, reporting)

### Indirects Factors (from AGENT_ESTIMATING):
- Construction Indirects (CI) = 18% of notional coordination base
- Procurement (P) = 2% of third-party services
- EPCM/PM allocation included in direct PM allowances

### Contingency Baseline % (from AGENT_ESTIMATING):
- Engineering (E), PM, Procurement (P): 10%
- Construction Indirects (CI): 20%
- **Adjustment:** +5% if bucket allowance share >= 50%; +10% if >= 80%

**Disclosure:** All uses of fallback model are explicitly documented in Decision_Log.md (D-005, D-006, D-008, D-010) and flagged in QA_Report.md.

---

## Source Selection Decision

**Decision Reference:** D-005 (Decision_Log.md)

**Primary Basis:** Fallback typical model (no project-specific sources available)

**Confidence:** LOW

**Recommendation:** Acquire project construction schedule, clarify interface requirements, and obtain monitoring quotes to replace fallback allowances in next estimate iteration.

---

## Deliverables Inventory — Source Coverage

| Deliverable ID | Name | Scope Found | Pricing Found | Coverage Status |
|----------------|------|-------------|---------------|-----------------|
| DEL-34.01 | Coordination Meeting Records | Artifact type only | None | Fallback |
| DEL-34.02 | Interface Agreements | Artifact type + parties | None | Fallback |
| DEL-34.03 | Marine Coordination Records | Artifact type only | None | Fallback |
| DEL-34.04 | Security Compliance Records | Artifact type only | None | Fallback |
| DEL-34.05 | Trenchless Crossing Monitoring | Artifact type only | None | Fallback |

**Total Deliverables:** 5
**With Explicit Quotes:** 0 (0%)
**With Rate Table Pricing:** 0 (0%)
**With Fallback Pricing:** 5 (100%)

---

## Next Steps to Improve Source Coverage

1. **Obtain project construction schedule:**
   - Confirm construction phase duration
   - Establish marine works timeline
   - Define coordination milestones

2. **Clarify interface agreement requirements:**
   - Identify all required third-party interface agreements
   - Assess complexity and negotiation effort per interface
   - Confirm Employer vs. Contractor responsibility

3. **Coordinate with PKG-03 Underground Utilities:**
   - Confirm trenchless crossing count and locations
   - Clarify monitoring requirements per crossing
   - Obtain stakeholder monitoring requirements

4. **Request vendor budgetary quotes for:**
   - Trenchless crossing monitoring services (survey firms)
   - Coordination administrative support (if outsourced)

5. **Develop project rate tables for:**
   - Coordination labor rates (coordinator, administrator)
   - Meeting support effort (preparation, minutes, distribution)
   - Monitoring services (survey, instrumentation)

6. **Add rate tables** to `_Estimates/_RateTables/` directory in standardized format

---

**Source Index Prepared By:** Estimating Agent
**Date:** 2026-01-29
**Status:** Complete (ready for pricing phase)
