# Source Index -- EST_DEL-05-05_2026-02-18_1800

## Indexed Price Sources

### 1. Optional_Items_Pricing.csv

| Field | Value |
|---|---|
| **Path** | `_PriceSources/Optional_Items_Pricing.csv` |
| **Source Type** | PARAMETRIC (allowance-grade parametric ranges) |
| **Parsing Notes** | CSV with columns: ItemID, Category, Description, Unit, PriceMin, PriceMax, RecommendedPrice, Basis, Confidence, Notes. 19 rows covering all optional items. |
| **Relevant Rows for DEL-05-05** | OPT-10 (non-illuminated signage, $8,000-$18,000, recommended $12,000/each), OPT-11 (illuminated signage, $15,000-$30,000, recommended $22,000/each) |
| **Cannot Support** | Exact vendor-quoted pricing; Town-specific branding design costs; installation labour as a separate line (installation is included in per-unit parametric pricing). |
| **Confidence** | LOW (per source file; Town branding guidelines are PENDING) |

### 2. Assumed_Project_Parameters.csv

| Field | Value |
|---|---|
| **Path** | `_PriceSources/Assumed_Project_Parameters.csv` |
| **Source Type** | Project parameters (quantities, areas, durations, financial assumptions) |
| **Parsing Notes** | CSV with columns: ParameterID, Category, Parameter, Value, Unit, Source, Confidence, Notes. 29 rows. |
| **Relevant Rows for DEL-05-05** | No directly relevant rows (no signage-specific parameters). General building parameters (PP-05, PP-06 for building area) provide context for sign sizing but are not pricing inputs. |
| **Cannot Support** | Sign quantity, size, or location decisions. |
| **Confidence** | N/A for signage pricing |

## Dependency Evidence (read-only; not a pricing source)

| File | Purpose |
|---|---|
| `DEL-05-05/Dependencies.csv` | 7 rows; used for blocker detection (DEP-05-05-007 = PENDING external constraint). Not used for pricing. |

## Sources NOT Available

| Expected Source | Status | Impact |
|---|---|---|
| Vendor quote for signage fabrication | NOT PROVIDED | No QUOTE-basis pricing possible; fallback to ALLOWANCE |
| Town of Penhold branding guidelines | PENDING (external; DEP-05-05-007) | Cannot finalize sign design, dimensions, materials, or illumination decision |
| Signage subtrade budget pricing | NOT PROVIDED | No competitive pricing data |
