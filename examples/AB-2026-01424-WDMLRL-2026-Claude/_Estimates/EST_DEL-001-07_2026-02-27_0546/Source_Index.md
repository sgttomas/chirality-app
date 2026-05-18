# Source Index — EST_DEL-001-07_2026-02-27_0546

## Indexed Price Sources

### 1. Professional_Staff_Rates.csv

- **Path:** `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv`
- **Source Type:** Rate Table (PARAMETRIC basis)
- **Content:** 25 professional staff roles with hourly rates in CAD. Each role has a RoleID, category, hourly rate, basis (all PARAMETRIC), and confidence (all MEDIUM).
- **Roles used for DEL-001-07:**
  - R-01 Project Manager: $165/hr
  - R-08 Cost Estimator: $135/hr
  - R-11 Senior Architect: $180/hr
  - R-12 Architect: $135/hr
  - R-13 BIM Technician: $95/hr
- **Limitations:** Rates are parametric estimates, not firm quotes. Confidence is MEDIUM for all roles.

### 2. Level_of_Effort.csv

- **Path:** `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv`
- **Source Type:** Parametric Model
- **Content:** Hours-by-role allocation for each deliverable in the project. DEL-001-07 has 5 role entries totalling 50 hours.
- **DEL-001-07 entries:**
  - R-01 Project Manager: 6 hrs
  - R-08 Cost Estimator: 4 hrs
  - R-11 Senior Architect: 18 hrs
  - R-12 Architect: 14 hrs
  - R-13 BIM Technician: 8 hrs
- **Limitations:** Hours are parametric estimates based on deliverable type classification ("PKG-001 Architect -- Schedule"), not activity-level build-up. Confidence is MEDIUM.

### 3. Assumed_Project_Parameters.csv

- **Path:** `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv`
- **Source Type:** Reference Parameters
- **Content:** 19 project-level parameters including building area (~13,000 sqft), ceiling height (35 ft), equipment counts, currency (CAD).
- **Used for:** Parametric cross-check context (building area for fee percentage validation).
- **Limitations:** Some parameters are DERIVED or ASSUMPTION basis.

### 4. Professional_Design_Fees.csv

- **Path:** `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Design_Fees.csv`
- **Source Type:** Parametric Model
- **Content:** Design fee percentages by discipline as percentage of construction value. DF-01 (Architecture): recommended 4.5% of construction value.
- **Used for:** Cross-check only (not primary pricing basis for this deliverable).
- **Limitations:** Fee percentage is a broad benchmark; does not directly price individual deliverables.

### 5. Parametric_Building_Rates.csv

- **Path:** `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Parametric_Building_Rates.csv`
- **Source Type:** Parametric Model
- **Content:** Per-square-foot rates for industrial building types. PB-01: $285/sf recommended for maintenance shop.
- **Used for:** Cross-check only (construction value estimate for fee percentage validation).
- **Limitations:** Broad parametric rate; MEDIUM confidence.
