# Source Index — EST_DEL-07-03_2026-02-18_1500

---

## Pricing Sources Used

| # | File | Source Type | Items Used | Supports | Parsing Notes |
|---|------|------------|------------|----------|---------------|
| 1 | `_PriceSources/Professional_Staff_Rates.csv` | Rate Table | R-02 (Project Manager, $175/hr), R-24 (Administrative / Document Control, $80/hr) | Hourly rates for all line items | CSV; 30 roles total; 2 used for DEL-07-03. Rates are parametric Alberta 2024 market estimates (Confidence: MEDIUM). |
| 2 | `_PriceSources/Level_of_Effort.csv` | Level of Effort | DEL-07-03 rows: R-02 (8 hrs), R-24 (4 hrs) | Hours per role for DEL-07-03 | CSV; 65 rows total; 2 rows for DEL-07-03. Hours are planning estimates based on comparable $15-20M DB municipal proposal efforts (Basis: PARAMETRIC). |
| 3 | `_PriceSources/Assumed_Project_Parameters.csv` | Project Parameters | PP-04 (6-week proposal timeline) | Context for coordination overhead calibration | CSV; 29 parameters. PP-04 used as context; no direct pricing impact on this deliverable. |

---

## Pricing Sources Not Used (provided but not applicable)

None. All three provided sources were consulted.

---

## Dependency Evidence Sources

| File | Location | Used For |
|------|----------|----------|
| `Dependencies.csv` | DEL-07-03 deliverable folder | Blocker/readiness assessment (3 upstream execution dependencies identified; 0 blocking) |
| `_DEPENDENCIES.md` | DEL-07-03 deliverable folder | Narrative context for dependency relationships |

---

## Source Limitations

| Source | Limitation |
|--------|-----------|
| Professional_Staff_Rates.csv | Rates are parametric market estimates, not actual firm rates. Accuracy +/-20-30%. |
| Level_of_Effort.csv | Hours are planning estimates (Basis: PARAMETRIC), not actual tracked effort. Accuracy +/-20-30%. |
| Dependencies.csv | 3 upstream execution dependencies PENDING (DEL-05-02, DEL-02-01, RFP Appendix I Template). These may affect deliverable content but do not affect the production hours estimate. |
