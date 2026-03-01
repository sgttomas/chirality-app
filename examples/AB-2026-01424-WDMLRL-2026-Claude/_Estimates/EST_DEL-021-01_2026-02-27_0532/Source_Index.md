# Source Index — EST_DEL-021-01_2026-02-27_0532

## Pricing Sources

| # | Source File | Source Type | Parsing Notes | Supports |
|---|-----------|-------------|---------------|----------|
| 1 | `PriceSources/Professional_Staff_Rates.csv` | RATE_TABLE | 25 roles with CAD hourly rates; Basis=PARAMETRIC; Confidence=MEDIUM | Unit rates for all labour line items (ITEM-001 through ITEM-008) |
| 2 | `PriceSources/Level_of_Effort.csv` | PARAMETRIC | Hours by DeliverableID × RoleID; 8 rows for DEL-021-01 totalling 60 hours across 8 roles | Quantities (hours) for all labour line items |
| 3 | `PriceSources/Assumed_Project_Parameters.csv` | PARAMETRIC | 19 project parameters; PP-17 confirms CAD currency | Project context; currency confirmation |
| 4 | `PriceSources/Fees_Permits_Insurance.csv` | PARAMETRIC / ALLOWANCE | 5 fee items (FP-01 through FP-05); FP-01 covers performance bond premium but not bid bond premium specifically | Partial support — no explicit bid bond premium line; bid bond premium estimated parametrically |

## Source Limitations

- **Bid bond premium:** Fees_Permits_Insurance.csv provides FP-01 (performance bond premium allowance, $12,000–$35,000) and FP-02 (L&M payment bond premium) but does not include a separate line for bid bond premium. Bid bond premiums are typically a fraction of these amounts and are estimated parametrically (see Assumptions_Log ASM-003).
- **Courier/delivery cost:** No explicit source. Estimated parametrically (see Assumptions_Log ASM-004).
- **Certified cheque alternative:** Not priced separately. If a certified cheque is used instead of a bid bond, there is no premium cost, but funds are tied up. This estimate assumes bid bond route per Guidance P5.
