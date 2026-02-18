# Assumptions Log -- EST_DEL-01-05_2026-02-18_2359

| AssumptionID | Assumption | Basis | Impact if Wrong | Lines Affected |
|---|---|---|---|---|
| ASM-01 | Schedule B construction content mirrors DEL-01-04 pricing exactly; no additional items or adjustments are needed between Schedule A compilation and Schedule B detail | Schedule B is a breakdown of Schedule A; same scope, same pricing, different presentation format | If additional line items emerge during Schedule B production, totals would change and reconciliation would fail | All B-* and C-* lines |
| ASM-02 | Main PSB building footprint is 18,000 sf (ground floor) with 12,000 sf bays and 6,000 sf office/admin | PP-05 from Assumed_Project_Parameters.csv | Quantity variance in all area-based pricing; mechanical, electrical, and interior lines most sensitive | B-BLD-100 through B-BLD-670 |
| ASM-03 | Cold storage building is 6,000 sf (60x100 ft) per PP-07 | PP-07 confirmed in RFP | Minimal impact; cold storage is a defined scope item | B-BLD-700, B-BLD-460, B-BLD-670 |
| ASM-04 | Developed site area is 4.5 acres per PP-10 | PP-10 assumption; 12-acre total less undeveloped areas | Earthwork quantities and paving areas proportional to developed area | B-SIT-100 through B-SIT-270 |
| ASM-05 | 80 screw piles at 6m centres for main PSB foundation | Derived from 18,000 sf footprint and typical spacing; geotechnical report supports screw pile approach | Pile count could vary +/-20% based on detailed structural design | B-BLD-100 |
| ASM-06 | Fire protection (wet sprinkler) is included at $108,000 | AHJ determination pending; sprinkler may not be required for this occupancy | If not required, $108,000 reduction to base cost; would require Schedule A update | B-BLD-420 |
| ASM-07 | CCIP insurance rate is 2.00% of project value ($12M) | FP-03 recommended rate; actual depends on insurer and risk profile | Rate could range from 1.50% to 2.50% ($180k-$300k range vs. $240k assumed) | B-GR-130 |
| ASM-08 | Building permit fee is 0.75% of construction value | FP-06 parametric; Penhold fee schedule not yet confirmed | Could be higher or lower depending on actual municipal fee structure | B-GR-160 |
| ASM-09 | Generator system ($150,000) covers all essential loads per Addendum 03 | EQ-04 system price for 100-150 kW; actual load TBD | If load exceeds 150 kW, generator and related systems cost increases | B-BLD-530 |
| ASM-10 | FF&E cash allowance is fixed at $20,000 per DEC-012 | Decision DEC-012 resolved OI-002 | None; this is a fixed decision | C-600 |
| ASM-11 | Production effort (44 hours) is sufficient to compile Schedule B from available pricing data | Level_of_Effort.csv allocation for DEL-01-05 | If additional iterations or reconciliation cycles are needed, hours could increase | A-010 through A-030 |
