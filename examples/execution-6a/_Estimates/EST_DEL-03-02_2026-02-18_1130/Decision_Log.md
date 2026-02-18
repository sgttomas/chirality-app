# Decision Log: EST_DEL-03-02_2026-02-18_1130

## DEC-EST-001 — Rate Table Source Selection

| Field | Value |
|---|---|
| Decision | Earthwork_Civil_Rates.csv is the primary rate source for all construction line items. Rates used are the RecommendedRate column values. |
| Rationale | BASIS_OF_ESTIMATE = RATE_TABLE. All 11 items in Earthwork_Civil_Rates.csv are directly applicable to DEL-03-02 scope. RecommendedRate is the mid-point estimate per source file convention. |
| Alternatives | Could use RateMin (conservative low) or RateMax (conservative high); deferred to human decision if range estimates are needed. |

## DEC-EST-002 — Cost Ownership Exclusions

| Field | Value |
|---|---|
| Decision | Paving_Surfacing_Rates.csv, Underground_Utility_Rates.csv, and Fees_Permits_Insurance.csv are excluded from DEL-03-02 pricing per brief cost ownership rules. |
| Rationale | Brief explicitly assigns: pavement to DEL-03-03, utilities to DEL-03-04, environmental consultant fees to DEL-03-05, and permits/bonds to PKG-001. |
| Impact | No pricing gaps within DEL-03-02 from these exclusions; those costs are carried by their respective deliverable estimates. |

## DEC-EST-003 — Building Pad Preparation Included in DEL-03-02

| Field | Value |
|---|---|
| Decision | Building pad preparation for both main PSB and cold storage building is priced under DEL-03-02, not under PKG-002 or PKG-004. |
| Rationale | Brief cost ownership rule: "Building pad preparation (main building + cold storage) --> DEL-03-02 (NOT PKG-002, PKG-004)." |
| Impact | Lines L-005 and L-006 carry pad prep costs ($36,784 + $12,254 = $49,038). |

## DEC-EST-004 — Stormwater Pond Priced via Earthwork Rates

| Field | Value |
|---|---|
| Decision | Stormwater retention pond excavation is priced using the common excavation rate (EC-03, $15/m3) rather than a specialist pond rate. Outlet protection is priced as a separate lump sum (L-011). |
| Rationale | No dedicated pond construction rate in Earthwork_Civil_Rates.csv. Pond excavation is common earthwork in native soils (clayey sand and clay per Datasheet). Outlet protection is extrapolated from EC-08 drainage rates + professional judgment. |
| Risk | Pond may require liner, engineered berm, or specialized outlet structure not captured in base earthwork rates. Flagged in Risk_Register.md. |

## DEC-EST-005 — Civil Design Fee Scope Limitation

| Field | Value |
|---|---|
| Decision | Civil design fee (L-015) is calculated only on DEL-03-02 construction subtotal, not the full site/civil package. |
| Rationale | DF-02 describes fee as "% of construction cost of site/civil scope." To avoid double-counting across DEL-03-01/02/03/04/05 estimate snapshots, each deliverable carries its proportional share of civil design fees. |
| Impact | DEL-03-02 civil design fee = $11,514 (2.5% of $460,548). Other PKG-003 deliverables will carry their own proportional design fees. |

## DEC-EST-006 — ROUNDING Applied

| Field | Value |
|---|---|
| Decision | Per brief ROUNDING=DOLLAR, all individual line item amounts are rounded to the nearest whole dollar after Qty x UnitRate multiplication. |
| Rationale | Brief specifies ROUNDING: DOLLAR. |
| Impact | Rounding differences are immaterial (maximum $0.50 per line x 15 lines = $7.50 maximum total rounding impact). |

## DEC-EST-007 — ALLOW_MIXED_METHODS Enforcement

| Field | Value |
|---|---|
| Decision | All 15 line items use Method=RATE_TABLE, consistent with BASIS_OF_ESTIMATE=RATE_TABLE and ALLOW_MIXED_METHODS=FALSE. |
| Rationale | FALLBACK_POLICY=STRICT requires that items without rate table evidence be priced as TBD. All items have rate table evidence (Earthwork_Civil_Rates.csv or Professional_Design_Fees.csv). |
| Impact | No fallback methods used; no TBD amounts. Basis-consistency check PASS. |
