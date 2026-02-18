# Run Context -- EST_DEL-01-05_2026-02-18_2359

| Field | Value |
|---|---|
| **RunID** | EST_DEL-01-05_2026-02-18_2359 |
| **AsOf** | 2026-02-18T23:59:00-07:00 |
| **Scope** | DEL-01-05 |
| **ScopeResolvedSummary** | 1 deliverable in scope (DEL-01-05); 0 excluded; 0 blocked |
| **BASIS_OF_ESTIMATE** | RATE_TABLE |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv, Level_of_Effort.csv, Assumed_Project_Parameters.csv, Structural_Concrete_Rates.csv, Building_Envelope_Rates.csv, Interior_Architectural_Rates.csv, Mechanical_System_Rates.csv, Electrical_System_Rates.csv, Earthwork_Civil_Rates.csv, Paving_Surfacing_Rates.csv, Underground_Utility_Rates.csv, Equipment_Pricing.csv, Optional_Items_Pricing.csv, Parametric_Building_Rates.csv, Construction_Labour_Rates.csv, Professional_Design_Fees.csv, Fees_Permits_Insurance.csv |
| **DECOMPOSITION_PATH** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/_Decomposition/Penhold_PSB_Project_Decomposition_v2.md (v2.3 FINAL) |
| **DEPENDENCY_SOURCES** | AUTO -- read from DEL-01-05/Dependencies.csv (20 dependency rows loaded) |
| **FALLBACK_POLICY** | ALLOW_ALLOWANCE |
| **ALLOW_MIXED_METHODS** | TRUE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | DOLLAR |
| **OUTPUT_LABEL** | DEL-01-05 |

---

## Resolved Defaults and Decisions

- **Dual cost nature:** DEL-01-05 has both production cost lines (Method=RATE_TABLE) for estimator hours to compile the Schedule B, and construction pricing content lines (Method=RATE_TABLE/PARAMETRIC/ALLOWANCE) that represent the actual Schedule B detailed breakdown.
- **Construction pricing content source:** All construction content lines are derived from the same rate sources used in EST_DEL-01-04_2026-02-18_2359, reorganized into Schedule B categories (General Requirements, Public Services Buildings, Public Services Sitework, Additional Items 1-6).
- **Reconciliation target:** Construction content total MUST equal $7,710,000 from DEL-01-04 Schedule A (base $7,327,000 + options $383,000).
- **CBS mapping rule:** Production costs use CBS=PRD.COMP. Construction content lines use CBS codes matching the Schedule B category structure: CON.GR (General Requirements), CON.BLD (Buildings), CON.SIT (Sitework), OPT.* (Additional Items).
- **DEL-01-04 dependency:** EST_DEL-01-04_2026-02-18_2359 was completed first; its construction content totals are the binding target for this estimate's Schedule B reconciliation.

---

## Warnings

1. Mixed methods active per ALLOW_MIXED_METHODS=TRUE: RATE_TABLE (primary), PARAMETRIC (cold storage PEMB), ALLOWANCE (workshop equipment, municipal tie-ins, utility fees, FF&E).
2. Bond/insurance premiums (B-1110 through B-1195) are priced in General Requirements as part of Schedule B content; the underlying basis evidence is in DEL-01-03 scope but pricing is computed from Fees_Permits_Insurance.csv.
3. Fire protection (B-420) at LOW confidence -- AHJ determination pending.
4. Generator system (B-530) at LOW confidence -- final load calculations pending.
