# Source Index — EST_DEL-013-02_2026-02-27_0901

## Price Sources Indexed

| Source File | Source Type | Parsing Notes | Supports |
|---|---|---|---|
| Professional_Staff_Rates.csv | Rate Table | 25 roles; HourlyRate_CAD; PARAMETRIC basis; MEDIUM confidence | Professional staff LOE pricing (R-01 through R-25) |
| Level_of_Effort.csv | Rate Table / LOE | Multi-deliverable LOE matrix; 6 rows for DEL-013-02 (R-01, R-02, R-03, R-05, R-06, R-08) | Hours by role for DEL-013-02 professional staff |
| Assumed_Project_Parameters.csv | Parameters | 19 rows; provides facility area (13,000 sqft), ceiling height (35 ft), currency (CAD) | Parametric sizing inputs |
| Mechanical_System_Rates.csv | Rate Table / Allowance | 6 rows; MS-03 directly applicable (high-volume air exchanger); MS-06 for ductwork rate | Equipment pricing (MS-03) and ductwork rate (MS-06) |
| Construction_Labour_Rates.csv | Rate Table | 10 trades; fully burdened rates; T-06 HVAC Sheet Metal ($91.20), T-08 Labourer ($65.10), T-04 Electrician ($96.00) | Construction labour pricing |
| Equipment_Pricing.csv | Rate Table / Allowance | 3 rows; none directly applicable to DEL-013-02 (cranes, wash bay, compressor) | Not used for this deliverable |

## Source Coverage Assessment

- **Equipment (MS-03):** Direct match for "High-volume air exchanger, installed" — ALLOWANCE basis, LOW confidence, range $9,000–$18,000.
- **Ductwork (MS-06):** Direct match for installed ductwork normalized per m2 floor area — PARAMETRIC basis, MEDIUM confidence, $60/m2.
- **Professional Staff:** Full rate table available; LOE hours from Level_of_Effort.csv matched to DEL-013-02.
- **Construction Labour:** Fully burdened rates available for HVAC sheet metal (T-06), labourer (T-08), electrician (T-04).
- **Controls, vibration isolation, fire stopping, permits, condensate drain, heating integration:** No direct rate source — priced using parametric assumptions. Flagged in QA.

## Documents Read for Quantity Takeoff

| Document | Path | Key Extractions |
|---|---|---|
| _CONTEXT.md | DEL-013-02_Air-Exchanger/_CONTEXT.md | Deliverable identity, scope list (7 items), related deliverables |
| Datasheet.md | DEL-013-02_Air-Exchanger/Datasheet.md | Equipment type, facility dimensions, conditions, construction items |
| Specification.md | DEL-013-02_Air-Exchanger/Specification.md | 18 requirements (REQ-001 through REQ-018), standards, verification methods |
| Guidance.md | DEL-013-02_Air-Exchanger/Guidance.md | 5 principles, 7 considerations including condensate drain, trade-offs |
| Procedure.md | DEL-013-02_Air-Exchanger/Procedure.md | 5 phases, 20 steps, prerequisites, verification checks, records |
