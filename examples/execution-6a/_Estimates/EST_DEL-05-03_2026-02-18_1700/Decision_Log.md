# Decision Log -- EST_DEL-05-03_2026-02-18_1700

## Run Decisions

| DecisionID | Decision | Rationale | Impact |
|---|---|---|---|
| DEC-RUN-001 | Method fallback: QUOTE -> PARAMETRIC | Brief explicitly states "No vendor quote exists. Use parametric pricing from Optional_Items_Pricing.csv." FALLBACK_POLICY=ALLOW_ALLOWANCE and ALLOW_MIXED_METHODS=TRUE permit this. | All Detail.csv lines use Method=PARAMETRIC instead of QUOTE. Flagged in QA as BASIS_MISMATCH. |
| DEC-RUN-002 | Zone count assumed at 10 | PP-28 in Assumed_Project_Parameters.csv states 10 controlled access zones. Brief acknowledges "Number of controlled zones/doors is TBD (depends on DEL-02-01 floor plan)." | Used OPT-06 (10-zone system) as single line item. No additional zones priced via OPT-07 at this time. |
| DEC-RUN-003 | Single line item for system (not broken into components) | OPT-06 is priced as a complete system (readers + controllers + software + contacts + REX + wiring + programming + commissioning). No finer-grained breakdown is available in price sources. | Detail.csv has 1 line item. Component-level breakdown will require vendor quote. |
| DEC-RUN-004 | CBS assigned as 26 05 00 | No CBSHint in decomposition. Deterministic assignment: access control systems map to UniFormat II Division 26 (Electronic Safety and Security) Subdivision 05 (Electronic Access Control). | Consistent with industry convention for access control classification. |
| DEC-RUN-005 | Exclusions enforced per cost ownership rules | Brief specifies: IT network infrastructure -> DEL-02-06; door hardware -> DEL-02-01; electrical power circuits -> DEL-02-06. These are NOT included in DEL-05-03 pricing. | Prevents double-counting. Exclusions documented in Summary.md and Detail.csv notes. |
| DEC-RUN-006 | Rounding applied: DOLLAR | Per brief ROUNDING=DOLLAR. All amounts rounded to nearest whole dollar. | $45,000 is already a whole dollar amount; no rounding adjustment needed. |
