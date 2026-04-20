# QA CHECKS — dbm-publish

## Minimum output validity checks

The package run is valid only when all of the following are true:

1. The deterministic assembly, concordance, and source-supersession validation steps (when a supersession map is admitted) were invoked under the skill's tool policy; if any tool fails, the run must surface that failure explicitly in `Publication_Readiness.md` and the package QA trail.
2. The current package snapshot contains the expected package artifacts:
   - `Rewritten_DBM.md`
   - `Trace_Appendix.md`
   - `Publication_Manifest.md`
   - `Publication_QA.md`
   - `Publication_Concordance_Report.md`
   - `Publication_Concordance_Findings.csv`
   - `Publication_Concordance_Expansion_Candidates.csv`
   - `Publication_Readiness.md`
   - `Rerun_Recommendations.csv`
   - `Source_Supersession_Report.md` (when source-supersession validation was run)
   - `Source_Supersession_Findings.csv` (when source-supersession validation was run)
3. `Publication_Readiness.md` uses one of the required readiness classifications:
   - `READY`
   - `READY_WITH_MAJOR_NOTES`
   - `BLOCKED`
4. A `BLOCKED` result is used whenever:
   - required sections are missing,
   - assembly failed,
   - blocking concordance findings exist,
   - unmatched source-supersession divergences exist (when source-supersession validation was run),
   - unresolved `HIGH` concordance-expansion candidates remain.
5. `Rerun_Recommendations.csv` exists whenever readiness is not `READY`, and remains allowed even for `READY` when the run still yields improvement notes.
6. All writes stayed inside the approved package snapshot subtree / package output root.

## Required readiness artifact content

`Publication_Readiness.md` should, at minimum:
- state the readiness classification,
- summarize deterministic tool status,
- summarize section completeness,
- summarize blocking vs non-blocking concordance findings,
- summarize unresolved `HIGH` / `NORMAL` / `LOW` concordance-expansion candidates,
- summarize material readability/quality issues,
- summarize QA burden (`TBD`, assumptions, deferred confirmation, skipped inputs, terminology normalizations),
- identify whether targeted reruns are required or merely recommended.

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

## Required concordance-expansion candidate output

`Publication_Concordance_Expansion_Candidates.csv` must:
- aggregate all per-section `SEC-##_ASSERTION_DISCOVERY.csv` files from the current section set,
- deduplicate semantically overlapping candidates conservatively,
- classify each unresolved candidate as `HIGH`, `NORMAL`, or `LOW`,
- retain enough source detail for targeted reruns.

Minimum columns:
- `AssertionKey`
- `AssertionLabel`
- `AssertionDomain`
- `AssertionType`
- `SuggestedComparisonRule`
- `SuggestedComparisonParameter`
- `SuggestedAuthoritySectionID`
- `SuggestedRequiredSectionIDs`
- `Criticality`
- `DiscoverySource`
- `SupportingSectionIDs`
- `SourceArtifacts`
- `SourceRefs`
- `Disposition`
- `Notes`

Checks:
- `Disposition` should distinguish unresolved candidates from duplicates or already-covered items.
- Any unresolved `HIGH` candidate must be reflected in `Publication_Readiness.md` and `Rerun_Recommendations.csv`.
- If no unresolved candidates remain, the file may still exist with only a header row or explicit zero-findings note per local convention.

## Failure reporting expectations

Use `FAILED_INPUTS` when:
- required planning-artifact paths are missing,
- the section root or package root is invalid,
- the run would write outside the approved package subtree.

Use `FAILED` when:
- deterministic assembly or concordance execution fails in a way that prevents package outputs from being emitted,
- required package outputs cannot be written despite valid inputs.

Even when the run completes, the QA/readiness output must surface:
- missing sections,
- blocking concordance findings,
- unresolved expansion candidates by criticality,
- major readability issues,
- remaining unresolved conflict burden,
- rerun recommendations tied to specific findings.
