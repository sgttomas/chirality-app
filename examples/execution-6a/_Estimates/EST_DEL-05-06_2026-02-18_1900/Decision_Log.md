# Decision Log: EST_DEL-05-06_2026-02-18_1900

## DEC-EST-001 -- Retail Appliance Pricing Treated as Quote-Equivalent

- **Date:** 2026-02-18
- **Context:** Optional_Items_Pricing.csv labels appliance rows (OPT-12 through OPT-17) with `Basis=PARAMETRIC`. However, the invoker brief states: "Appliance pricing from retail sources is effectively quote-based." The brief also states: "use the parametric rates in Optional_Items_Pricing.csv if they can be interpreted as quote-equivalent retail pricing."
- **Decision:** Treat the `RecommendedPrice` values from OPT-12 through OPT-17 as QUOTE method in Detail.csv, consistent with the invoker's explicit guidance.
- **Affected Lines:** L-0506-01 through L-0506-06 (all lines in Detail.csv)
- **Impact:** All `Method` values set to `QUOTE` rather than `PARAMETRIC`. No mixed methods. Consistent with `BASIS_OF_ESTIMATE=QUOTE` and `ALLOW_MIXED_METHODS=FALSE`.
- **Reversibility:** If vendor quotes are later obtained, rerun with actual quote data. If the invoker prefers to label these as PARAMETRIC, rerun with `ALLOW_MIXED_METHODS=TRUE`.

## DEC-EST-002 -- RecommendedPrice Selected Over Min/Max

- **Date:** 2026-02-18
- **Context:** Optional_Items_Pricing.csv provides PriceMin, PriceMax, and RecommendedPrice for each row. No guidance was provided on which column to use.
- **Decision:** Use `RecommendedPrice` for all line items as the best available point estimate. The min/max range is documented in Assumptions_Log.md (ASM-002) and Summary.md for risk context.
- **Affected Lines:** All (L-0506-01 through L-0506-06)
- **Impact:** Estimate total = $18,600 CAD. Range: $13,800 (all min) to $24,100 (all max).

## DEC-EST-003 -- CBS Codes Assigned Deterministically

- **Date:** 2026-02-18
- **Context:** No explicit CBSHint in the decomposition for DEL-05-06.
- **Decision:** Assigned CBS codes as:
  - `CBS-EQP` for equipment purchase line items (L-0506-01 through L-0506-05)
  - `CBS-INST` for installation/connection line items (L-0506-06)
- **Rationale:** Reflects the natural cost-type split between procurement (equipment) and installation (labor + materials for connections).

## DEC-EST-004 -- Scope Boundary Enforcement (DEL-05-06 vs DEL-05-07)

- **Date:** 2026-02-18
- **Context:** Brief provides explicit cost ownership rules and scope boundary definition. Per OSR S12.6: if an item is ambiguous (e.g., microwave -- plugs in but listed in appliance spec), it belongs in DEL-05-06.
- **Decision:** All items from OPT-12 through OPT-17 are classified as DEL-05-06 scope (connected appliances). No items redirected to DEL-05-07. Microwaves are included in DEL-05-06 per the OSR S12.6 rule cited in the brief.
- **Affected Lines:** L-0506-02 (microwaves) specifically noted; all lines confirmed.
