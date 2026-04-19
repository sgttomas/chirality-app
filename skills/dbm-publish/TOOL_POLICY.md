# TOOL POLICY — dbm-publish

## Preferred tool order

1. Invoke `tools/publication/assemble_publication.py`.
2. Invoke `tools/publication/check_concordance.py`.
3. Read the assembled package, section QA artifacts, and all per-section assertion-discovery CSVs.
4. Use direct reasoning to aggregate unresolved concordance-expansion candidates, classify publication readiness, and write rerun guidance.

## Allowed deterministic tools

### TASK-enforced

- `python3 tools/publication/assemble_publication.py:*`
- `python3 tools/publication/check_concordance.py:*`

### Operationally invoked

- `tools/publication/assemble_publication.py` — deterministic package assembly, completeness checks, trace appendix generation, manifest generation, and package QA generation.
- `tools/publication/check_concordance.py` — deterministic cross-section concordance checking against the frozen concordance register.

## Expected use of reasoning

This skill uses reasoning to:
- judge readability and publication quality of the assembled DBM,
- interpret non-blocking quality notes after deterministic checks complete,
- merge and classify per-section assertion-discovery candidates into one package-level expansion view,
- convert findings into a clear `READY`, `READY_WITH_MAJOR_NOTES`, or `BLOCKED` decision,
- generate actionable `Rerun_Recommendations.csv` rows.

## Disallowed use

- No dispatching other skills or agents.
- No inline reimplementation of deterministic assembly or concordance logic that belongs in the tool layer.
- No mutation of KTY-local truth, section-planning artifacts, or approved section prose except package-level summaries.
- No partial concordance checking limited to rerun sections.
- No suppression of unresolved `HIGH` expansion candidates from readiness logic.

## Write boundary

The skill may write only inside the current package snapshot subtree plus the package-level readiness artifacts for that run.

It must not write in KTY folders, decomposition folders, or unrelated tool roots.
