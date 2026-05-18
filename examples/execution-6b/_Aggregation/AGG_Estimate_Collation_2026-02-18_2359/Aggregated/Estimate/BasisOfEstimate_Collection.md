# Basis of Estimate Collection — AGG_Estimate_Collation_2026-02-18_2359

## Summary

All 38 deliverables (40 estimate snapshots) use `BASIS_OF_ESTIMATE = RATE_TABLE` as their primary estimation method. Hours are sourced from `Level_of_Effort.csv` and rates from `Professional_Staff_Rates.csv`, both maintained under `_PriceSources/`.

Three deliverables have mixed methods:
- **DEL-01-03**: RATE_TABLE (production hours) + ALLOWANCE (bond/insurance premiums)
- **DEL-01-04**: RATE_TABLE (production hours) + RATE_TABLE/PARAMETRIC/ALLOWANCE (construction pricing content)
- **DEL-01-05**: RATE_TABLE (production hours) + RATE_TABLE/PARAMETRIC/ALLOWANCE (construction pricing detail)

## Common Price Sources

All estimates reference these shared sources:
- `Professional_Staff_Rates.csv` -- hourly rates by role (23+ roles, CAD 2024, MARKET basis, MEDIUM confidence)
- `Level_of_Effort.csv` -- estimated hours per deliverable per role (PARAMETRIC basis)
- `Assumed_Project_Parameters.csv` -- project-level assumptions (building area, site area, etc.)

DEL-01-03, DEL-01-04, and DEL-01-05 additionally reference:
- `Fees_Permits_Insurance.csv` -- bond/insurance premium rates and permit fee estimates
- Various construction cost rate sources (SC-*, BE-*, IA-*, MS-*, ES-*, EC-*, PS-*, UU-*, EQ-*, OPT-*, PB-*, DF-*)

## Per-Deliverable Basis Evidence

### PKG-001 -- Proposal Compliance, Commercial and Team Qualifications

**DEL-01-01** (Compliance Matrix): RATE_TABLE. Single role (R-22 Proposal Coordinator, 8 hrs x $105/hr). Tier 0 -- no upstream dependencies.

**DEL-01-02** (Final Submission): RATE_TABLE. Two roles (R-22 16 hrs + R-02 PM 4 hrs). Tier 4 -- depends on all other packages.

**DEL-01-03** (Bonding and Insurance): RATE_TABLE + ALLOWANCE. Production: 3 roles (PM 4hr, Legal 4hr, Admin 2hr). Financial allowances: performance bond $180k, L&M bond $120k, CCIP $240k, broker fee $3.5k. All premiums based on assumed $12M contract value (LOW confidence).

**DEL-01-04** (Schedule A): RATE_TABLE (production) + MIXED (construction). Production: 3 estimator/PM roles (72 hrs). Construction pricing: 86 line items totaling $7,710,000 covering structural, envelope, interior, mechanical, electrical, civil, paving, utilities, general requirements, and 6 optional items.

**DEL-01-05** (Schedule B): RATE_TABLE (production) + MIXED (construction). Production: 3 estimator/PM roles (44 hrs). Construction pricing: detailed breakdown mirroring DEL-01-04 totals (intentional duplicate per Schedule A/B relationship).

**DEL-01-06** (Pricing Narrative): RATE_TABLE. Two roles (PM 12hr, Senior Estimator 8hr). Tier 4 -- depends on DEL-01-04/05.

**DEL-01-07** (Firm Experience): RATE_TABLE. Two roles (Proposal Coordinator 16hr, PM 4hr). Tier 0.

**DEL-01-08** (Resumes): RATE_TABLE. Two roles (HR Coordinator 12hr, Proposal Coordinator 8hr). Tier 0.

**DEL-01-09** (Subtrade List): RATE_TABLE. Two roles (PM 8hr, Admin 4hr). Tier 0.

### PKG-002 -- Conceptual Design

**DEL-02-01** (Architectural Concept): RATE_TABLE. Four roles: Project Architect 40hr, Intermediate Architect 24hr, CAD Technician 60hr, PM 8hr. Highest single-deliverable effort at 132 hours.

**DEL-02-02** (Civil Concept): RATE_TABLE. Three roles: Senior Civil 24hr, Intermediate Civil 16hr, CAD Technician 16hr.

**DEL-02-03** (Structural Concept): RATE_TABLE. Two roles: Senior Structural 16hr, Intermediate Structural 8hr.

**DEL-02-04** (Mechanical Concept): RATE_TABLE. Two roles: Senior Mechanical 16hr, Intermediate Mechanical 8hr.

**DEL-02-05** (Electrical Concept): RATE_TABLE. Two roles: Senior Electrical 16hr, Intermediate Electrical 8hr.

### PKG-003 -- Design Brief

All 6 deliverables: RATE_TABLE, single senior role per discipline. DEL-03-01 Architect 12hr, DEL-03-02 Civil 10hr, DEL-03-03 Structural 10hr, DEL-03-04 Mechanical 10hr, DEL-03-05 Electrical 10hr, DEL-03-06 Architect (accessibility) 8hr.

### PKG-004 -- Sustainability and Energy

DEL-04-01: Building Science Consultant 12hr + Architect 4hr. DEL-04-02: Mechanical Engineer 10hr. DEL-04-03: Electrical Engineer 8hr.

### PKG-005 -- Durability and Maintenance

All 4 deliverables: single senior role per discipline. DEL-05-01 Architect 10hr, DEL-05-02 Structural 8hr, DEL-05-03 Mechanical 8hr, DEL-05-04 Electrical 8hr.

### PKG-006 -- Delivery Plan

Both deliverables: Design Manager (10hr each) + PM (4hr each).

### PKG-007 -- Construction Methodology

DEL-07-01: Construction Manager 12hr + PM 4hr. DEL-07-02: Construction Manager 8hr. DEL-07-03: PM 8hr. DEL-07-04: PM 6hr. DEL-07-05: Quality Lead 8hr + PM 4hr.

### PKG-008 -- Commissioning, Closeout and Warranty

DEL-08-01: Commissioning Lead 10hr + PM 4hr. DEL-08-02: Commissioning Lead 6hr + PM 2hr. DEL-08-03: PM 4hr + Commissioning Lead 4hr.

### PKG-009 -- Schedule

DEL-09-01: Scheduler 20hr + PM 8hr + Construction Manager 4hr.

### PKG-010 -- Due Diligence

DEL-10-01: PM 10hr + Construction Manager 4hr. DEL-10-02: PM 8hr + Civil Engineer 6hr + Geotechnical Engineer 4hr.
