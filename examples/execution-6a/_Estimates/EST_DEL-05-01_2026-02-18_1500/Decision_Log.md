# Decision Log

## Estimate-Run Decisions

| DecisionID | Date | Decision | Rationale | AffectedItems |
|---|---|---|---|---|
| DEC-EST-001 | 2026-02-18 | Use ALLOWANCE method as fallback for all line items (instead of QUOTE). | BASIS_OF_ESTIMATE=QUOTE was specified, but the brief explicitly states no vendor quote exists. FALLBACK_POLICY=ALLOW_ALLOWANCE permits this. ALLOW_MIXED_METHODS=TRUE allows Method to deviate from declared basis. The Optional_Items_Pricing.csv provides budget-range figures self-reported as PARAMETRIC, but without a formal parametric model these are best characterized as budget allowances. | L-05-01-001, L-05-01-002, L-05-01-003 |
| DEC-EST-002 | 2026-02-18 | Use RecommendedPrice (midpoint of range) from Optional_Items_Pricing.csv for all line items. | PriceMin/PriceMax ranges are provided. RecommendedPrice represents the source author's best estimate within the range. No basis exists to prefer min or max. | L-05-01-001, L-05-01-002, L-05-01-003 |
| DEC-EST-003 | 2026-02-18 | Apply DOLLAR rounding per brief. | ROUNDING=DOLLAR was specified. All source prices are already whole dollar amounts; no rounding adjustment needed. | All line items |
| DEC-EST-004 | 2026-02-18 | CBS codes assigned as provisional (CBS-0500-EQUIP, CBS-0500-PLMB, CBS-0500-ENVR). | No CBSHint in decomposition for DEL-05-01. Codes are deterministic based on cost category (equipment, plumbing, environmental). Pending project-level CBS structure. | L-05-01-001, L-05-01-002, L-05-01-003 |
| DEC-EST-005 | 2026-02-18 | Scope boundary enforcement: exclude base building bay sumps, base mechanical rough-in, structural modifications, and PW bay functional fit-up from DEL-05-01 pricing. | Per brief Cost Ownership Rules. Base sumps owned by DEL-02-05 (SOW-0214). Base mechanical rough-in owned by DEL-02-05. Structural modifications owned by DEL-02-04. PW bay fit-up owned by DEL-02-03. | All line items (exclusion notes applied) |

## Upstream Decisions Referenced

| DecisionID | Source | Summary |
|---|---|---|
| DEC-001 | Decomposition v1.0 | Cold storage 60x100 (not relevant to this estimate but referenced for completeness). |
| DEC-004 | Decomposition v1.0 | Utility tie-ins as cash allowance (wash bay utility connections interface with DEL-03-04). |
