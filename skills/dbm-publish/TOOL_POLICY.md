# TOOL POLICY — dbm-publish

## Preferred tool order

1. Invoke `tools/publication/assemble_publication.py`.
2. Invoke `tools/publication/validate_source_supersession.py` when the frozen manifest admits a supersession map.
3. Read the assembled package, `Publication_Knowledge_Coverage.md`, `Publication_Open_Items.md`, and section QA artifacts.
4. In `FULL_ENGINEERING_DBM` mode, assemble `Publication_Content_Adequacy.md` from section QA outputs, optional content-profile smoke-test signals when available, and direct package review.
5. Use direct reasoning to classify publication readiness and write rerun guidance.

## Allowed deterministic tools

### TASK-enforced

- `python3 tools/publication/assemble_publication.py:*`
- `python3 tools/publication/validate_source_supersession.py:*`

### Operationally invoked

- `tools/publication/assemble_publication.py` — deterministic package assembly, completeness checks, trace appendix generation, manifest generation, package QA generation, knowledge coverage reporting, and open-items inventory generation.
- `tools/publication/validate_source_supersession.py` — deterministic source/reference-fidelity validation for supersession-governed divergences.

## Expected use of reasoning

This skill uses reasoning to:
- judge readability and publication quality of the assembled DBM,
- judge full-DBM content adequacy without reducing the decision to word counts,
- interpret non-blocking quality notes after deterministic checks complete,
- interpret knowledge coverage and open-items package records,
- convert findings into a clear `READY`, `READY_WITH_MAJOR_NOTES`, or `BLOCKED` decision,
- generate actionable `Rerun_Recommendations.csv` rows.

Post-authoring concordance review is handled separately by `TASK + dbm-postauthor-concordance` after this skill completes.

## Disallowed use

- No dispatching other skills or agents.
- No inline reimplementation of deterministic assembly logic that belongs in the tool layer.
- No mutation of KTY-local truth, section-planning artifacts, or approved section prose except package-level summaries.
- No acceptance of materially underdeveloped body content as `READY` in `FULL_ENGINEERING_DBM` mode.

## Write boundary

The skill may write only inside the current package snapshot subtree plus the package-level readiness artifacts for that run.

It must not write in KTY folders, decomposition folders, or unrelated tool roots.
