# Decision Log

## EST_DEL-05-04_2026-02-18_1800

| DecisionID | Decision | Rationale | AffectedLines |
|---|---|---|---|
| DEC-EST-01 | Used PARAMETRIC method for all line items despite BASIS_OF_ESTIMATE=QUOTE | No vendor quote exists per brief. FALLBACK_POLICY=ALLOW_ALLOWANCE and ALLOW_MIXED_METHODS=TRUE permit method deviation. Parametric pricing from Optional_Items_Pricing.csv is the best available evidence. | L-0504-01, L-0504-02 |
| DEC-EST-02 | Used RecommendedPrice (midpoint) from OPT-08 and OPT-09 rather than PriceMin or PriceMax | RecommendedPrice is the designated best estimate in the source file. Range information preserved in Notes for reviewer reference. | L-0504-01, L-0504-02 |
| DEC-EST-03 | Applied Qty=1, Unit=LS, UnitRate=Amount convention for both lines | Both lines are parametric lump-sum items per STRUCTURE requirements for parametric/allowance convention. | L-0504-01, L-0504-02 |
| DEC-EST-04 | Separated installation cost (L-0504-01) from monitoring cost (L-0504-02) into distinct line items | RFP OSR Section 12.4 requires installation costs and monitoring costs to be presented separately. This is a submission format requirement. | L-0504-01, L-0504-02 |
| DEC-EST-05 | CBS codes assigned as 26-SECURITY and 26-SECURITY-MONITORING | No project CBS dictionary provided. Used deterministic mapping: security equipment/installation maps to Division 26/28 convention; monitoring is a recurring operating cost subcategory. Documented in Run_Context.md. | L-0504-01, L-0504-02 |
| DEC-EST-06 | Excluded IT network infrastructure, electrical power circuits, and exterior lighting from this estimate | Per brief cost ownership rules: these are owned by DEL-02-06. OPT-08 includes camera-side network switches and cabling but NOT the building IT backbone. | L-0504-01 |
| DEC-EST-07 | Did not add integration cost for DEL-05-03 (access control) | DEP-0504-006 is conditional (only if both options elected). Integration cost is not quantifiable without knowing if both are elected. Noted in Blockers.md. | N/A |
| DEC-EST-08 | Rounding applied at DOLLAR level | Per brief: ROUNDING=DOLLAR. Both amounts are already whole dollar amounts; no rounding adjustment needed. | All |
