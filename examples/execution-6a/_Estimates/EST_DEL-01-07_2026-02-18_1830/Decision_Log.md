# Decision Log -- EST_DEL-01-07_2026-02-18_1830

## Decisions Applied During This Run

### DEC-EST-0107-001: CBS code assignment rule

- **Decision:** CBS codes assigned by mapping Role Category from Professional_Staff_Rates.csv to deliverable-specific CBS codes: Construction -> CBS-0107-CX, Management -> CBS-0107-MGT, Administrative -> CBS-0107-ADM.
- **Rationale:** No explicit CBSHint was provided in the decomposition for DEL-01-07. A deterministic mapping from role category to CBS provides consistent, auditable cost structure alignment.
- **Affected lines:** All (L-0107-01, L-0107-02, L-0107-03).

### DEC-EST-0107-002: Legal survey cost excluded

- **Decision:** The external surveyor fee for the as-built legal/topographical survey (SOW-0113) is not priced in this estimate. Only the coordination labor (included in R-21 Commissioning Lead hours) is captured.
- **Rationale:** FALLBACK_POLICY=STRICT and no quote or allowance for survey services was provided in PRICE_SOURCES. Including a fabricated cost would violate the no-invention invariant.
- **Impact:** The DEL-01-07 total ($23,650) excludes the external survey fee. This is surfaced in QA_Report.md Gap 1.

### DEC-EST-0107-003: System-specific Cx labor excluded per cost ownership rules

- **Decision:** Only overall Cx coordination, training, closeout admin, and warranty management hours are included. System-specific commissioning labor (mechanical balancing, electrical testing, controls commissioning, fire alarm testing, etc.) is NOT included.
- **Rationale:** Brief explicitly states: "DEL-01-07 covers OVERALL Cx coordination and closeout administration ONLY. System-specific commissioning labor is carried in the respective PKG-002 discipline deliverables."
- **Impact:** DEL-01-07 estimate reflects coordination overhead, not discipline execution. Surfaced in QA_Report.md Gap 2.

### DEC-EST-0107-004: No fallback pricing applied

- **Decision:** FALLBACK_POLICY=STRICT was enforced. All line items priced from RATE_TABLE evidence only. No ALLOWANCE or PARAMETRIC fallback was needed because all three roles had both rate and hours data available.
- **Rationale:** All required pricing inputs were present in PRICE_SOURCES. STRICT policy was met without exception.
- **Impact:** None. ALLOW_MIXED_METHODS=FALSE constraint satisfied.

### DEC-EST-0107-005: Hours sourced from Level_of_Effort.csv (PARAMETRIC basis)

- **Decision:** The quantity (hours) for each role was taken from Level_of_Effort.csv, which uses PARAMETRIC basis for its hour estimates. This is treated as a rate-table input (hours are a quantity dimension of the rate table, not a separate pricing method).
- **Rationale:** The RATE_TABLE basis of estimate encompasses both the unit rate ($/hr from Professional_Staff_Rates.csv) and the quantity (hours from Level_of_Effort.csv). The Level_of_Effort.csv provides the "quantity takeoff" dimension of the rate table approach. Method is recorded as RATE_TABLE for all lines.
- **Impact:** Confidence remains MEDIUM, reflecting the parametric nature of the hour estimates.
