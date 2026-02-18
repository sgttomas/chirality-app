# Source Index — EST_DEL-01-02_2026-02-18_1430

**RunID:** EST_DEL-01-02_2026-02-18_1430
**AsOf:** 2026-02-18

---

## Pricing Sources Used

| # | Source File | Source Type | Items Used | Supports | Parsing Notes |
|---|-----------|------------|-----------|----------|---------------|
| 1 | `_PriceSources/Professional_Staff_Rates.csv` | Rate Table | R-22 (Proposal Coordinator, $105/hr), R-02 (Project Manager, $175/hr) | Unit rates for all line items | CSV; 30 rows total; 2 used for DEL-01-02. All rates are MARKET basis, MEDIUM confidence. |
| 2 | `_PriceSources/Level_of_Effort.csv` | Level of Effort (Parametric) | 2 rows: DEL-01-02/R-22 (14h), DEL-01-02/R-02 (4h) | Quantity (hours) for all line items | CSV; 67 rows total; 2 rows for DEL-01-02. Hours are PARAMETRIC basis; notes indicate "slightly fewer deliverables to assemble than 6b (21 vs 38); still final QA". |
| 3 | `_PriceSources/Assumed_Project_Parameters.csv` | Project Parameters | PP-04 (proposal preparation = 6 weeks) | Context only; not used for pricing | CSV; 29 rows total. PP-04 confirms proposal timeline context. Not directly used in line-item pricing. |

---

## Dependency Sources Used

| # | Source | Type | Items | Supports |
|---|--------|------|-------|----------|
| 1 | `DEL-01-02_FormalSubmissionPackage/Dependencies.csv` | Dependency Register | 31 rows | Blocker detection; 20 upstream prerequisite deliverables identified, all PENDING |

---

## Sources NOT Used (available but not applicable)

| Source | Reason Not Used |
|--------|----------------|
| Construction rate files (Structural, Mechanical, Electrical, etc.) | DEL-01-02 is administrative/production only; no construction pricing content |
| `Fees_Permits_Insurance.csv` | Not applicable to DEL-01-02 (bonding/insurance is in DEL-01-03) |
| `Optional_Items_Pricing.csv` | Not applicable to DEL-01-02 |

---

## Source Coverage Assessment

- **Rate coverage:** 100% -- both roles used in DEL-01-02 have explicit rates in Professional_Staff_Rates.csv
- **Quantity coverage:** 100% -- both roles have explicit hours in Level_of_Effort.csv
- **Provenance completeness:** 100% -- all 2 line items have full SourceRef to file + row ID
