# Decision Log — EST_DEL-07-01_2026-02-18_2010

## Run-Level Decisions

### DEC-R01: CBS Mapping Rule

| Field | Value |
|---|---|
| **Decision** | CBS codes assigned based on role Category from Professional_Staff_Rates.csv |
| **Mapping** | Administrative -> CBS-ADMIN; Management -> CBS-MGMT |
| **Rationale** | DEL-07-01 has no explicit CBSHint in the decomposition. A deterministic mapping from role category to CBS code provides consistent, auditable cost structure breakdown. |
| **Alternatives Considered** | (a) Single CBS code for entire deliverable -- rejected; loses granularity. (b) CBS from SOW item -- SOW-016 does not map to a standard CBS. |

### DEC-R02: No Fallback Needed

| Field | Value |
|---|---|
| **Decision** | All line items priced directly from RATE_TABLE evidence; no fallback invoked |
| **Rationale** | FALLBACK_POLICY = STRICT, but moot -- Level_of_Effort.csv provides hours for both roles and Professional_Staff_Rates.csv provides rates. No TBD amounts. |

### DEC-R03: Dependency Blockers Do Not Block Estimate

| Field | Value |
|---|---|
| **Decision** | PENDING dependencies (RFP, OSR, Addendum 03, DEL-07-02, DEL-07-03) do not block cost estimation |
| **Rationale** | Cost drivers are hours x rates, which are independent of content readiness. The LOE table already calibrates effort for this deliverable scope. |

### DEC-R04: Rounding Applied

| Field | Value |
|---|---|
| **Decision** | ROUNDING = DOLLAR applied to all amounts |
| **Rationale** | Per brief configuration. All computed amounts are already whole dollars (16 x 105 = 1680; 4 x 175 = 700), so rounding has no effect on this run. |
