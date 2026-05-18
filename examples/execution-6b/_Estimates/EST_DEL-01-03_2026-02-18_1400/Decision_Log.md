# Decision Log

**RunID:** EST_DEL-01-03_2026-02-18_1400

| DecisionID | Decision | Rationale |
|---|---|---|
| EST-D-001 | Used PP-25 ($12,000,000 estimated total project value) as the contract value basis for percentage-based bond and insurance premium calculations | PP-25 is the only contract value estimate available in PRICE_SOURCES. It is explicitly labeled PARAMETRIC / LOW confidence. The alternative would be TBD amounts, but FALLBACK_POLICY=ALLOW_ALLOWANCE permits this approach. |
| EST-D-002 | Applied recommended (midpoint) rates from Fees_Permits_Insurance.csv for all premium lines rather than min or max | Recommended rates represent the source author's best estimate within each range. Using midpoints is conservative (neither optimistic nor pessimistic). |
| EST-D-003 | Used ALLOWANCE method for premium lines (L-004 through L-007) rather than RATE_TABLE | Bond/insurance premiums are not "hours x rate" items. They are percentage-of-contract or lump-sum fees. ALLOWANCE is the correct method classification per the brief's Special Instructions and the fee source structure. |
| EST-D-004 | CBS codes assigned deterministically: 01.ADMIN.BOND_INS for production hours, 01.PREMIUM.BOND for bond premiums, 01.PREMIUM.INS for CCIP, 01.PREMIUM.BROKER for broker fee | No CBSHint was present in the decomposition. A functional CBS grouping was created to separate production effort from pass-through premiums, enabling clear cost visibility. |
| EST-D-005 | Builder's risk (FP-04) and general liability (FP-05) insurance NOT included in this deliverable's estimate | Per the brief's Cost Ownership Rules, DEL-01-03 covers bonding + CCIP insurance + broker fee. Builder's risk and general liability are project-wide insurance costs that would typically be carried in General Requirements (DEL-01-05 Schedule B) or a separate insurance deliverable. The brief's Special Instructions list only FP-01, FP-02, FP-03, and FP-19 for DEL-01-03. |
| EST-D-006 | Scope resolution: DEL-01-03 covers documentation production cost AND pass-through premium allowances | The brief explicitly states this deliverable has MIXED cost nature. Both categories are included to provide a complete cost picture for the deliverable. |
