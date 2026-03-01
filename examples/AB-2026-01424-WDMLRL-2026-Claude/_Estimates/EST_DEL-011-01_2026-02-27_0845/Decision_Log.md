# Decision Log — EST_DEL-011-01_2026-02-27_0845

| DecisionID | Decision | Rationale | Impact |
|---|---|---|---|
| DEC-001 | Used PARAMETRIC as primary pricing method with ALLOWANCE fallback for 3 items | Per `BASIS_OF_ESTIMATE=PARAMETRIC` and `FALLBACK_POLICY=ALLOW_PARAMETRIC` and `ALLOW_MIXED_METHODS=TRUE` | 98.9% PARAMETRIC, 1.1% ALLOWANCE by value |
| DEC-002 | Applied `RecommendedRate` from Structural_Concrete_Rates.csv rather than min/max extremes | RecommendedRate represents the source provider's central estimate; min/max retained in Notes for sensitivity analysis | Rates are mid-range; actual could vary within published min/max bounds |
| DEC-003 | Used ALLOWANCE method for steel plate embedments (L-003, ITM-003) | SC-08 in Structural_Concrete_Rates.csv is explicitly labelled `ALLOWANCE` basis with LOW confidence; locations/sizes TBD per design | $5,000 line; minor impact |
| DEC-004 | Used ALLOWANCE method for cistern structural provisions (L-017, ITM-017) | No specific rate table for cistern structural provisions; parametric estimate based on analogous slab penetration + local reinforcement | $5,000 line; minor impact |
| DEC-005 | Used ALLOWANCE method for cold-weather concreting provisions (L-021, ITM-021) | No specific rate table for cold-weather provisions; parametric estimate based on Alberta construction norms for a project of this scale | $15,000 line; moderate uncertainty |
| DEC-006 | Derived building footprint as 130 ft x 100 ft = ~1,208 m2 from Appendix B conceptual drawing | Consistent with Datasheet attribute and Assumed_Project_Parameters.csv PP-10 (~13,000 sqft) | Foundation for slab, roof, and envelope area calculations |
| DEC-007 | Estimated mezzanine area at ~30% of building footprint (~362 m2) | Mezzanine covers parts room + utility room + wash bay per Datasheet; ~30% is a reasonable parametric estimate for these program elements | $76,020 line; actual area TBD per DEL-002-05 |
| DEC-008 | Estimated steel plate embedment count at 20 EA | App B shows plates at multiple bay locations; 20 EA is a parametric estimate for a 13,000 sqft heavy equipment shop | Minor line ($5,000); actual count per DEL-002-08 |
| DEC-009 | Estimated 4 entrance/exit man doors | Typical shop layout with 2 exterior + 2 interior entry points; exact count TBD per DEL-001-07 | Minor line ($5,200); actual count per architectural design |
| DEC-010 | Estimated window glazing area at 20 m2 | Office area glazing in a maintenance shop; modest glazing expected | Minor line ($14,400); actual area TBD per architectural design |
| DEC-011 | Assumed cast-in-place (CIP) concrete as baseline structural system | RFP specifies "concrete structure"; CIP is the most conservative pricing baseline; tilt-up/precast could be lower cost | Structural frame ($630K) sensitive to system choice |
| DEC-012 | Assumed steel deck/bar joist roof system | Roof system TBD per structural design; steel deck/bar joist is common for industrial buildings with 35 ft clear height | Roof structure ($175K) sensitive to system choice |
| DEC-013 | Derived construction labour hours parametrically from area/quantity metrics | No explicit labour hour tables in PRICE_SOURCES for DEL-011-01 construction activities; used industry parametric rates (hr/m2) | Labour subtotal ~$146K; reasonable for project scale |
| DEC-014 | Priced crane runway structural supports at $35,000 per runway (2 EA) | Parametric estimate for structural runway beams/brackets for 5-tonne crane; excludes crane supply (DEL-016-01) | $70,000 total; sensitive to span length and beam specification |
| DEC-015 | Priced structural rough openings for OH doors at $8,500 each | Parametric estimate for structural framing (header/lintel + jamb) for 24 ft wide overhead door openings | $25,500 total for 3 openings |
| DEC-016 | Did not update `_LATEST.md` pointer | Per `UPDATE_LATEST_POINTER=FALSE` | No pointer file modified |
| DEC-017 | Used Rounding=NONE (default) | No rounding policy specified in brief | All amounts at full precision |
