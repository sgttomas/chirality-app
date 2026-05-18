# Source Index — EST_DEL-03-03_2026-02-18_1200

## Price Sources (used for pricing)

| # | File | Source Type | Parsing Notes | Supports | Limitations |
|---|------|------------|---------------|----------|-------------|
| 1 | Paving_Surfacing_Rates.csv | Rate Table | 9 rows; CSV; ItemIDs PS-01 through PS-09; all rates in CAD/unit | Heavy duty asphalt, light duty asphalt, aggregate surfacing, concrete aprons, curb/gutter, sidewalk, line painting, accessible signage, bollards | Rates are parametric (RateMin/RateMax/Recommended); not firm quotes. Confidence is MEDIUM for all items. Rates include base prep per notes (PS-01, PS-02). |
| 2 | Assumed_Project_Parameters.csv | Parametric parameters | 29 rows; CSV; ParameterIDs PP-01 through PP-29 | Quantity derivation: PP-10 (developed site area breakdown), PP-13 (main building overhead doors = 8), PP-14 (cold storage overhead doors = 2), PP-19 (parking stalls = 40) | Confidence varies (MEDIUM to LOW); quantities are assumptions pre-design. Site areas are estimated before site plan (DEL-03-01). |

## Price Sources (referenced but not used for DEL-03-03 pricing)

| # | File | Source Type | Reason Not Used |
|---|------|------------|-----------------|
| 3 | Construction_Labour_Rates.csv | Labour rate table | Labour rates are embedded in the Paving_Surfacing_Rates.csv unit rates (installed rates, not labour-only). No separate labour pricing needed. |
| 4 | Earthwork_Civil_Rates.csv | Rate table | Earthwork/grading scope belongs to DEL-03-02 per cost ownership rules. Not applicable to DEL-03-03. |
| 5 | Underground_Utility_Rates.csv | Rate table | Underground utilities scope belongs to DEL-03-04 per cost ownership rules. Not applicable to DEL-03-03. |
| 6 | Fees_Permits_Insurance.csv | Fee/permit schedule | Fees, permits, and insurance belong to PKG-001 general requirements. Not applicable to DEL-03-03. |
| 7 | Professional_Design_Fees.csv | Fee schedule | Design fees belong to PKG-001 general requirements or are percentage-based on construction value. Not applicable to DEL-03-03 construction estimate. |

## Deliverable Sources (read-only, for scope/quantity/dependency evidence)

| # | File | Purpose |
|---|------|---------|
| 8 | DEL-03-03 Datasheet.md | Surfacing zone definitions; pavement cross-sections; concrete apron parameters; quantity basis |
| 9 | DEL-03-03 Specification.md | Requirements governing surfacing design; zone delineation; cross-section standards |
| 10 | DEL-03-03 Guidance.md | Design intent; ESAL responsibility; transition zone considerations |
| 11 | DEL-03-03 Dependencies.csv | Dependency register; blocker identification |
| 12 | DEL-03-03 _CONTEXT.md | Deliverable identification and scope coverage |

## Decomposition Source

| # | File | Purpose |
|---|------|---------|
| 13 | Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md | Stable IDs (PKG-003, DEL-03-03); scope item mapping (SOW-0107, SOW-0108); package/deliverable hierarchy |
