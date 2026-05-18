# QA_CHECKS — proposal-format

## Minimum output validity

| Check | Validation |
|---|---|
| PROPOSAL blocks complete | Every block contains Evidence, Change, Why, Risk, Status |
| Evidence grounded | Evidence cites file + section/heading (or `location TBD`) |
| Change specific | Change descriptions are actionable without further interpretation |
| Status correct | PROPOSED (default), APPLIED (only when edit was made), NEEDS_HUMAN_RULING (contradictions/trade-offs) |
| No unsupported proposals | No proposal lacks evidence |
| Decision interface present | MISSING, NEEDS_HUMAN_RULING, DEPENDENCY_NOTES sections all present (may be `none`) |
| Scope respected | All proposals reference content within the single deliverable |

## Failure reporting

- If no production documents exist: report in `MISSING`
- If no meaningful issues are found: state this explicitly — do not pad output
- If `Tasks` specified work that could not be completed: report in `MISSING` with reason

## Baseline scan checks (when Tasks omitted)

- At least one category of proposals was assessed (completeness, consistency, verification, source fidelity, or identity)
- TBD items are reported separately from proposals
- Dependency notes are reported when cross-deliverable interfaces are visible
