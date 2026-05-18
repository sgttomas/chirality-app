# QA CHECKS — dbm-publish

## Minimum output validity checks

The package run is valid only when all of the following are true:

1. The deterministic assembly and source/reference-fidelity validation steps (when a supersession map is admitted) were invoked under the skill's tool policy; if any tool fails, the run must surface that failure explicitly in `Publication_Readiness.md` and the package QA trail.
2. The current package snapshot contains the expected package artifacts:
   - `Rewritten_DBM.md`
   - `Trace_Appendix.md`
   - `Publication_Manifest.md`
   - `Publication_QA.md`
   - `Publication_Knowledge_Coverage.md`
   - `Publication_Open_Items.md`
   - `Publication_Content_Adequacy.md` (required when `DBM_OUTPUT_MODE = FULL_ENGINEERING_DBM`)
   - `Publication_Readiness.md`
   - `Rerun_Recommendations.csv`
   - `Source_Supersession_Report.md` (when source/reference-fidelity validation was run)
   - `Source_Supersession_Findings.csv` (when source/reference-fidelity validation was run)
3. `Publication_Readiness.md` uses one of the required readiness classifications:
   - `READY`
   - `READY_WITH_MAJOR_NOTES`
   - `BLOCKED`
4. A `BLOCKED` result is used whenever:
   - required sections are missing,
   - assembly failed,
   - unexplained source/reference-fidelity divergences exist (when source/reference-fidelity validation was run),
   - `DBM_OUTPUT_MODE = FULL_ENGINEERING_DBM` and `Publication_Content_Adequacy.md` has `AdequacyVerdict = BLOCKED` or any fixed blocker finding.
5. `Rerun_Recommendations.csv` exists whenever readiness is not `READY`, and remains allowed even for `READY` when the run still yields improvement notes.
6. All writes stayed inside the approved package snapshot subtree / package output root.

Post-authoring evidence bundle review is handled separately by `TASK + dbm-postauthor-concordance` after this skill completes. That skill's candidate findings and disposition artifact are not part of this skill's output set.

## Required readiness artifact content

`Publication_Readiness.md` should, at minimum:
- state the readiness classification,
- summarize deterministic tool status,
- summarize section completeness,
- summarize DBM content adequacy verdict and fixed blocker findings when `Publication_Content_Adequacy.md` is required,
- summarize material readability/quality issues,
- summarize QA burden (`TBD`, assumptions, deferred confirmation, skipped inputs, terminology normalizations),
- summarize knowledge-coverage gaps, including any `PRIMARY` KTY with zero material body contribution,
- summarize open-items burden from `Publication_Open_Items.md`,
- identify whether targeted reruns are required or merely recommended.

## Required content adequacy artifact

When `DBM_OUTPUT_MODE = FULL_ENGINEERING_DBM`, `Publication_Content_Adequacy.md` must exist and contain:
- `Package Verdict` with `AdequacyVerdict`, `DBMOutputMode`, `BlockingFindingCount`, and blocker list,
- `Section Adequacy Matrix` with one row per required section,
- `Table Treatment Summary` for design-basis tables only,
- `Blockers` using only the fixed finding codes,
- `Human Review Notes` limited to issues requiring human judgment.

`DesignBasisTablesHandled` values in the section matrix must preserve section QA table-treatment distinctions when material: `INCLUDED`, `CONSOLIDATED`, `SPLIT`, `OMITTED_WITH_RATIONALE`, `DEFERRED_UPSTREAM_MISSING`, or `NONE_APPLICABLE`.

Allowed content-adequacy blockers:
- `UNDERDEVELOPED_SECTION`
- `UNJUSTIFIED_TABLE_OMISSION`
- `PRIMARY_KTY_COLLAPSED`
- `MISSING_DESIGN_BASIS_CLASS`
- `QA_SCAFFOLD_BODY_LEAKAGE`
- `NON_STANDALONE_CORE_BASIS`
- `DIGEST_MODE_USED_FOR_FULL_DBM`

## Required rerun recommendations schema

`Rerun_Recommendations.csv` minimum columns:
- `SectionID`
- `RerunReason`
- `BlockingLevel`
- `SpecificFinding`
- `RecommendedAction`
- `Notes`

Checks:
- `SectionID` may use `PACKAGE` only for package-level findings that are not section-local.
- `BlockingLevel` should clearly distinguish blocking from advisory findings.
- `RecommendedAction` should be specific enough for DBM_PUBLISHER to trigger targeted reruns without guesswork.

## Failure reporting expectations

Use `FAILED_INPUTS` when:
- required planning-artifact paths are missing,
- the section root or package root is invalid,
- the run would write outside the approved package subtree.

Use `FAILED` when:
- deterministic assembly execution fails in a way that prevents package outputs from being emitted,
- required package outputs cannot be written despite valid inputs.

Even when the run completes, the QA/readiness output must surface:
- missing sections,
- content-adequacy blockers and major notes,
- major readability issues,
- knowledge coverage gaps,
- consolidated open items,
- remaining unresolved conflict burden,
- rerun recommendations tied to specific findings.
