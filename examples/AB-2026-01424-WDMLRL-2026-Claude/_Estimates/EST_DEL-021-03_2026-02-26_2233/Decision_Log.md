# Decision Log — EST_DEL-021-03_2026-02-26_2233

| DecisionID | Decision | Rationale | Impact |
|---|---|---|---|
| DEC-001 | Used FP-03 recommended rate ($14,000) for builders risk despite TBD status in Datasheet | FP-03 provides a parametric range ($8,000-$22,000) with recommended midpoint; FALLBACK_POLICY=ALLOW_PARAMETRIC permits this | Builders risk line is priced but flagged MED confidence; may be removed if CCDC 14-2013 review determines it is not required |
| DEC-002 | Used FP-04 recommended rate ($6,000) for CGL/auto insurance | FP-04 provides a parametric range ($3,500-$9,500) with recommended midpoint | CGL line is priced at MED confidence; actual premium depends on contract value |
| DEC-003 | Set WCB, E&O, and Employer's Liability to TBD rather than estimating parametrically | No pricing data exists in any provided source for these coverages; WCB is payroll-dependent, E&O is Proponent-specific, Employer's Liability is often bundled. Inventing prices would violate the no-invention invariant. | 3 of 5 insurance premium lines are unpriced; total estimate is incomplete |
| DEC-004 | Labour hours sourced from Level_of_Effort.csv rather than derived from Procedure steps | Level_of_Effort.csv provides explicit per-role hour allocations for DEL-021-03; this is more systematic than counting procedure steps | Labour lines are fully priced with clear provenance |
| DEC-005 | CBS codes set as INS (insurance premiums) and LAB (professional labour) | No CBS scheme was prescribed in the brief; used descriptive codes for clarity | Affects WBS_CBS_Matrix.csv groupings |
| DEC-006 | SOW-0103 (name County as additional insured) not assigned a separate cost line | SOW-0103 is a policy condition, not a separately priceable activity; its cost is embedded in the insurance premiums and administrative labour already captured | No cost gap; SOW coverage is complete |
| DEC-007 | Subcontractor insurance costs excluded from estimate | Per Guidance ASMP-09 and Procedure Step 13, subcontractors are assumed individually responsible. No wrap-up / OCIP data in price sources. | If assumption is incorrect, material cost gap exists |
