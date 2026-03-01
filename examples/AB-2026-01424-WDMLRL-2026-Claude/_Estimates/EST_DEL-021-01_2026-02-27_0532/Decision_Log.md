# Decision Log — EST_DEL-021-01_2026-02-27_0532

| DecisionID | Decision | Rationale | Source |
|-----------|----------|-----------|--------|
| DEC-001 | Use PARAMETRIC method for all line items | BASIS_OF_ESTIMATE = PARAMETRIC; all pricing sources support parametric method. FALLBACK_POLICY = ALLOW_PARAMETRIC. No fallback needed since primary method applies to all items. | INIT-TASK brief |
| DEC-002 | Price bid bond premium as surety fee, not face value | The bid bond face value (10% of bid amount) is a surety obligation, not a direct cost to the proponent. The proponent's cost is the bid bond premium (surety's fee for issuing the instrument). Priced as a lump-sum parametric estimate. | Guidance — P5 (Bid Bond vs. Certified Cheque trade-off); Datasheet — Construction section |
| DEC-003 | Assume bid bond route (not certified cheque) | Guidance P5 states bid bond is preferred for proponents with surety relationships, as it preserves liquidity. Priced accordingly. If certified cheque route is chosen, the $1,500 bid bond premium (L-009) would not apply, but cash would be tied up. | Guidance — P5 |
| DEC-004 | Include courier delivery as a separate line item | Procedure Phase 5 requires physical delivery to Camrose County. This is a direct cost of producing the deliverable. | Procedure — Phase 5 Step 5.1 |
| DEC-005 | Accept Level_of_Effort.csv hours as-is despite "TBD — TBD" notes | The LoE file provides explicit hour allocations for DEL-021-01 across 8 roles (60 total hours). The "PKG-021 TBD — TBD" in the Notes column appears to reflect incomplete package-level categorization, not invalid hours. Hours accepted per the parametric model. | Level_of_Effort.csv rows 539–546 |
| DEC-006 | CBS categories assigned as LABOUR / FEES / OTHER | Labour lines (L-001 through L-008) represent professional staff effort. Bid bond premium (L-009) is a surety fee. Courier (L-010) is a miscellaneous direct cost. | Standard CBS classification |
| DEC-007 | Single deliverable scope — no rollup aggregation needed beyond DEL-021-01 | SCOPE = DEL-021-01 only. WBS_CBS_Matrix includes a TOTAL row for the single deliverable. | INIT-TASK brief |
