# dbm-publish contract

## Brief

This file defines the INIT-TASK dispatch contract for `TASK + dbm-publish`.

### Purpose

Use this workflow after approved section outputs exist and dbm-publisher wants the package-level assembly and QA artifacts.

### Scope model

- `ScopePath` should normally be the publication root or package root:
  - `{EXECUTION_ROOT}/_Publication/DBM/`
  - or `{EXECUTION_ROOT}/_Publication/DBM/package/`
- `AllowedWriteTargets` must remain inside the package snapshot subtree plus the package-level readiness artifacts for the current run.

The brief must not grant write access to KTY folders, decomposition truth, or unrelated tool roots.

### Required brief fields

| Field | Type | Meaning | Example |
|---|---|---|---|
| `PURPOSE` | string | Why the package run exists | `Assemble the rewritten DBM and classify publication readiness.` |
| `ScopePath` | path | Publication root or package root | `/abs/root/_Publication/DBM/` |
| `Workflow` | string | Must equal the workflow folder/name | `dbm-publish` |
| `AllowedWriteTargets` | list[path/glob] | Package snapshot subtree and review outputs for the current run | `[/.../package/RUN-20260418-120000/*]` |
| `RuntimeOverrides.PUBLICATION_ROOT` | path | Publication tool root | `/.../_Publication/DBM/` |
| `RuntimeOverrides.PUBLICATION_INPUT_MANIFEST` | path | Frozen input manifest | `/.../_Planning/Publication_Input_Manifest.md` |
| `RuntimeOverrides.PUBLICATION_SCHEMA_PATH` | path | Approved publication schema | `/.../_Planning/Publication_Schema.md` |
| `RuntimeOverrides.SECTION_MAP_PATH` | path | Approved section map | `/.../_Planning/Section_Map.csv` |
| `RuntimeOverrides.PUBLICATION_RULES_PATH` | path | Approved publication rules | `/.../_Planning/Publication_Rules.md` |
| `RuntimeOverrides.SECTIONS_ROOT` | path | Current section output root | `/.../_Publication/DBM/sections/` |
| `RuntimeOverrides.PACKAGE_OUTPUT_ROOT` | path | Package snapshot root | `/.../_Publication/DBM/package/` |
| `ExpectedOutputs` | list[path] | Package outputs expected from the run | `[/.../Rewritten_DBM.md, /.../Publication_Readiness.md, ...]` |

### Optional brief fields

| Field | Type | Meaning | Example |
|---|---|---|---|
| `RuntimeOverrides.DBM_OUTPUT_MODE` | enum | Publication output mode; defaults to full engineering DBM when omitted | `FULL_ENGINEERING_DBM` |
| `RuntimeOverrides.RUN_LABEL` | string | Human-friendly run label | `pilot-deepcut-round-1` |
| `RuntimeOverrides.SOURCE_DOMAIN` | string | Domain label for reporting | `West_Doe_Deepcut_DBM` |
| `RuntimeOverrides.SUPERSESSION_MAP_PATH` | path | Frozen cumulative supersession map from the active SCA snapshot | `/.../_ScopeChange/SCA-004_.../Supersession_Map.csv` |
| `RuntimeOverrides.ROOT_NAME` | string | Root name for supersession applicability filtering; typically equals `SOURCE_DOMAIN` | `West_Doe_Deepcut_DBM` |
| `RuntimeOverrides.FACILITY_ID` | string | Facility identifier for supersession applicability filtering | `04-25` |
| `RuntimeOverrides.HYPERGRAPH_USE_MODE` | enum | Whether hypergraph evidence is admitted for this run | `AUXILIARY_PLANNING_AND_QA` |
| `RuntimeOverrides.HYPERGRAPH_SNAPSHOT_PATH` | path | Exact path to the admitted hypergraph snapshot | `/.../_Aggregation/Hypergraph/snapshot/` |
| `RuntimeOverrides.HYPERGRAPH_RUN_SUMMARY_PATH` | path | Exact path to the hypergraph run summary | `/.../_Aggregation/Hypergraph/Run_Summary.md` |
| `RuntimeOverrides.HYPERGRAPH_QA_REPORT_PATH` | path | Exact path to the hypergraph QA report | `/.../_Aggregation/Hypergraph/QA_Report.md` |
| `RuntimeOverrides.HYPERGRAPH_NODES_PATH` | path | Exact path to the hypergraph nodes CSV | `/.../_Aggregation/Hypergraph/nodes.csv` |
| `RuntimeOverrides.HYPERGRAPH_HYPEREDGES_PATH` | path | Exact path to the hypergraph hyperedges CSV | `/.../_Aggregation/Hypergraph/hyperedges.csv` |
| `RuntimeOverrides.HYPERGRAPH_EVIDENCE_ROOT` | path | Root folder containing hypergraph evidence CSVs | `/.../_Aggregation/Hypergraph/evidence/` |
| `RuntimeOverrides.HYPERGRAPH_QA_VERDICT` | enum | QA verdict for the admitted hypergraph snapshot | `NON_BLOCKING` |
| `RuntimeOverrides.HYPERGRAPH_LIMITATIONS` | string | Free-text list of known defects constraining allowed use | `Artifact-node collision in KTY-015 unresolved.` |
| `RuntimeOverrides.HYPERGRAPH_QA_BINDING_POLICY` | enum | Whether hypergraph QA findings can block package readiness | `ADVISORY_ONLY` |
| `CustomInstructions` | string | Run-specific emphasis only; must not restate the workflow contract | `Be strict about sections that still read like stitched excerpts.` |

### Runtime-override guidance

- `PACKAGE_OUTPUT_ROOT` should be the immutable snapshot parent, not a mutable working directory.
- `AllowedWriteTargets` should constrain the run to the intended snapshot subtree and package-level readiness artifacts. For `FULL_ENGINEERING_DBM` runs, it must include `Publication_Content_Adequacy.md`.
- The workflow should always run against the latest complete current section set, not only against the rerun subset.
- The deterministic assembly step is expected to emit `Publication_Knowledge_Coverage.md` and `Publication_Open_Items.md` in the package snapshot.
- `Publication_Open_Items.md` must contain the required `Human Authority Rulings`, `Engineering TBDs`, and `Decomposition Gaps` tables, with explicit no-row statements when applicable.
- `DBM_OUTPUT_MODE` defaults to `FULL_ENGINEERING_DBM`. `DBM_DIGEST` must be present explicitly in the brief and publication rules when the human selected digest mode.
- In `FULL_ENGINEERING_DBM` mode, generated dispatch briefs must set `DBM_OUTPUT_MODE: FULL_ENGINEERING_DBM`, and `AllowedWriteTargets` and `ExpectedOutputs` must include `Publication_Content_Adequacy.md`.
- Post-authoring evidence bundle review is handled separately by `TASK + dbm-postauthor-concordance` after package assembly. The package workflow focuses on assembly and QA, not concordance review.

### Recommended CustomInstructions content

Use `CustomInstructions` only for run-specific reinforcement such as:
- a request to be especially strict about readability,
- a reminder that a known quality issue should remain non-blocking for this pilot,
- a reminder to emphasize terminology consistency or amendment-note discipline.

Do not use `CustomInstructions` to recreate deterministic tool contracts or the workflow contract.

### Example INIT-TASK brief

```md
PURPOSE: Assemble the rewritten DBM and classify publication readiness.
ScopePath: /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/
Workflow: dbm-publish
AllowedWriteTargets:
  - /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/package/RUN-20260418-120000/*
RuntimeOverrides:
  PUBLICATION_ROOT: /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/
  PUBLICATION_INPUT_MANIFEST: /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/_Planning/Publication_Input_Manifest.md
  PUBLICATION_SCHEMA_PATH: /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/_Planning/Publication_Schema.md
  SECTION_MAP_PATH: /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/_Planning/Section_Map.csv
  PUBLICATION_RULES_PATH: /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/_Planning/Publication_Rules.md
  SECTIONS_ROOT: /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/sections/
  PACKAGE_OUTPUT_ROOT: /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/package/
  DBM_OUTPUT_MODE: FULL_ENGINEERING_DBM
  RUN_LABEL: pilot-deepcut-round-1
ExpectedOutputs:
  - /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/package/RUN-20260418-120000/Rewritten_DBM.md
  - /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/package/RUN-20260418-120000/Trace_Appendix.md
  - /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/package/RUN-20260418-120000/Publication_Manifest.md
  - /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/package/RUN-20260418-120000/Publication_QA.md
  - /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/package/RUN-20260418-120000/Publication_Knowledge_Coverage.md
  - /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/package/RUN-20260418-120000/Publication_Open_Items.md
  - /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/package/RUN-20260418-120000/Publication_Content_Adequacy.md
  - /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/package/RUN-20260418-120000/Publication_Readiness.md
  - /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/package/RUN-20260418-120000/Rerun_Recommendations.csv
```

## Acceptance

### Minimum output validity checks

The package run is valid only when all of the following are true:

1. The deterministic assembly and source/reference-fidelity validation steps (when a supersession map is admitted) were invoked under the workflow's tool policy; if any tool fails, the run must surface that failure explicitly in `Publication_Readiness.md` and the package QA trail.
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

Post-authoring evidence bundle review is handled separately by `TASK + dbm-postauthor-concordance` after this workflow completes. That workflow's candidate findings and disposition artifact are not part of this workflow's output set.

### Required readiness artifact content

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

### Required content adequacy artifact

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

### Required rerun recommendations schema

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
- `RecommendedAction` should be specific enough for dbm-publisher to trigger targeted reruns without guesswork.

### Failure reporting expectations

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

## Tool use

### Preferred tool order

1. Invoke `tools/publication/assemble_publication.py`.
2. Invoke `tools/publication/validate_source_supersession.py` when the frozen manifest admits a supersession map.
3. Read the assembled package, `Publication_Knowledge_Coverage.md`, `Publication_Open_Items.md`, and section QA artifacts.
4. In `FULL_ENGINEERING_DBM` mode, assemble `Publication_Content_Adequacy.md` from section QA outputs, optional content-profile smoke-test signals when available, and direct package review.
5. Use direct reasoning to classify publication readiness and write rerun guidance.

### Allowed deterministic tools

#### Operationally invoked

- `tools/publication/assemble_publication.py` — deterministic package assembly, completeness checks, trace appendix generation, manifest generation, package QA generation, knowledge coverage reporting, and open-items inventory generation.
- `tools/publication/validate_source_supersession.py` — deterministic source/reference-fidelity validation for supersession-governed divergences.

### Expected use of reasoning

This workflow uses reasoning to:
- judge readability and publication quality of the assembled DBM,
- judge full-DBM content adequacy without reducing the decision to word counts,
- interpret non-blocking quality notes after deterministic checks complete,
- interpret knowledge coverage and open-items package records,
- convert findings into a clear `READY`, `READY_WITH_MAJOR_NOTES`, or `BLOCKED` decision,
- generate actionable `Rerun_Recommendations.csv` rows.

Post-authoring concordance review is handled separately by `TASK + dbm-postauthor-concordance` after this workflow completes.

### Disallowed use

- No dispatching other workflows or agents.
- No inline reimplementation of deterministic assembly logic that belongs in the tool layer.
- No mutation of KTY-local truth, section-planning artifacts, or approved section prose except package-level summaries.
- No acceptance of materially underdeveloped body content as `READY` in `FULL_ENGINEERING_DBM` mode.

### Write boundary

The workflow may write only inside the current package snapshot subtree plus the package-level readiness artifacts for that run.

It must not write in KTY folders, decomposition folders, or unrelated tool roots.
