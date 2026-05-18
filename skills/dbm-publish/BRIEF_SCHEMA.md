# BRIEF SCHEMA — dbm-publish

This file defines the INIT-TASK dispatch contract for `TASK + dbm-publish`.

## Purpose

Use this skill after approved section outputs exist and DBM_PUBLISHER wants the package-level assembly and QA artifacts.

## Scope model

- `ScopePath` should normally be the publication root or package root:
  - `{EXECUTION_ROOT}/_Publication/DBM/`
  - or `{EXECUTION_ROOT}/_Publication/DBM/package/`
- `AllowedWriteTargets` must remain inside the package snapshot subtree plus the package-level readiness artifacts for the current run.

The brief must not grant write access to KTY folders, decomposition truth, or unrelated tool roots.

## Required brief fields

| Field | Type | Meaning | Example |
|---|---|---|---|
| `PURPOSE` | string | Why the package run exists | `Assemble the rewritten DBM and classify publication readiness.` |
| `ScopePath` | path | Publication root or package root | `/abs/root/_Publication/DBM/` |
| `TaskSkill` | string | Must equal the skill folder/name | `dbm-publish` |
| `AllowedWriteTargets` | list[path/glob] | Package snapshot subtree and review outputs for the current run | `[/.../package/RUN-20260418-120000/*]` |
| `RuntimeOverrides.PUBLICATION_ROOT` | path | Publication tool root | `/.../_Publication/DBM/` |
| `RuntimeOverrides.PUBLICATION_INPUT_MANIFEST` | path | Frozen input manifest | `/.../_Planning/Publication_Input_Manifest.md` |
| `RuntimeOverrides.PUBLICATION_SCHEMA_PATH` | path | Approved publication schema | `/.../_Planning/Publication_Schema.md` |
| `RuntimeOverrides.SECTION_MAP_PATH` | path | Approved section map | `/.../_Planning/Section_Map.csv` |
| `RuntimeOverrides.PUBLICATION_RULES_PATH` | path | Approved publication rules | `/.../_Planning/Publication_Rules.md` |
| `RuntimeOverrides.SECTIONS_ROOT` | path | Current section output root | `/.../_Publication/DBM/sections/` |
| `RuntimeOverrides.PACKAGE_OUTPUT_ROOT` | path | Package snapshot root | `/.../_Publication/DBM/package/` |
| `ExpectedOutputs` | list[path] | Package outputs expected from the run | `[/.../Rewritten_DBM.md, /.../Publication_Readiness.md, ...]` |

## Optional brief fields

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
| `CustomInstructions` | string | Run-specific emphasis only; must not restate the skill contract | `Be strict about sections that still read like stitched excerpts.` |

## Runtime-override guidance

- `PACKAGE_OUTPUT_ROOT` should be the immutable snapshot parent, not a mutable working directory.
- `AllowedWriteTargets` should constrain the run to the intended snapshot subtree and package-level readiness artifacts. For `FULL_ENGINEERING_DBM` runs, it must include `Publication_Content_Adequacy.md`.
- The skill should always run against the latest complete current section set, not only against the rerun subset.
- The deterministic assembly step is expected to emit `Publication_Knowledge_Coverage.md` and `Publication_Open_Items.md` in the package snapshot.
- `Publication_Open_Items.md` must contain the required `Human Authority Rulings`, `Engineering TBDs`, and `Decomposition Gaps` tables, with explicit no-row statements when applicable.
- `DBM_OUTPUT_MODE` defaults to `FULL_ENGINEERING_DBM`. `DBM_DIGEST` must be present explicitly in the brief and publication rules when the human selected digest mode.
- In `FULL_ENGINEERING_DBM` mode, generated dispatch briefs must set `DBM_OUTPUT_MODE: FULL_ENGINEERING_DBM`, and `AllowedWriteTargets` and `ExpectedOutputs` must include `Publication_Content_Adequacy.md`.
- Post-authoring evidence bundle review is handled separately by `TASK + dbm-postauthor-concordance` after package assembly. The package skill focuses on assembly and QA, not concordance review.

## Recommended CustomInstructions content

Use `CustomInstructions` only for run-specific reinforcement such as:
- a request to be especially strict about readability,
- a reminder that a known quality issue should remain non-blocking for this pilot,
- a reminder to emphasize terminology consistency or amendment-note discipline.

Do not use `CustomInstructions` to recreate deterministic tool contracts or the skill contract.

## Example INIT-TASK brief

```md
PURPOSE: Assemble the rewritten DBM and classify publication readiness.
ScopePath: /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/
TaskSkill: dbm-publish
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
