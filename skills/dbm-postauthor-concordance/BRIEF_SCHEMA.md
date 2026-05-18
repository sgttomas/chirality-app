# BRIEF SCHEMA - dbm-postauthor-concordance

This file defines the INIT-TASK dispatch contract for `TASK + dbm-postauthor-concordance`.

## Purpose

Use this skill after DBM section synthesis and package assembly to build a post-authoring evidence bundle and prepare candidate findings for human readiness judgment.

## Scope model

- `ScopePath` should be the review output directory within the package snapshot.
- `AllowedWriteTargets` must name exactly the 7 output files under REVIEW_OUTPUT_DIR.
- The brief must not grant write access to section output folders, planning artifacts, KTY folders, or source authority files.

## Required brief fields

| Field | Type | Meaning | Example |
|---|---|---|---|
| `PURPOSE` | string | Why review is being run | `Post-authoring concordance review for package RUN-20260422-175550.` |
| `ScopePath` | path | Review output directory | `/repo/.../_Publication/DBM/package/RUN-20260422-175550/review/` |
| `TaskSkill` | string | Must equal `dbm-postauthor-concordance` | `dbm-postauthor-concordance` |
| `AllowedWriteTargets` | list[path] | Exactly the 7 output files | `[/.../Evidence_Bundle_Summary.md, /.../Section_Coverage.csv, /.../Draft_Claims.csv, /.../Body_Thinness.csv, /.../TBD_Inventory.csv, /.../Candidate_Findings.csv, /.../Publication_Review_Disposition.csv]` |
| `RuntimeOverrides.ASSEMBLED_DBM_PATH` | path | Assembled Rewritten_DBM.md | `/.../package/RUN-.../Rewritten_DBM.md` |
| `RuntimeOverrides.REVIEW_OUTPUT_DIR` | path | Output directory | `/.../package/RUN-.../review/` |
| `RuntimeOverrides.DOMAIN_ROOT` | path | DOMAIN root | `/repo/.../West_Doe_Deepcut_DBM/` |
| `RuntimeOverrides.PUBLICATION_SCHEMA_PATH` | path | Approved schema | `/.../_Planning/Publication_Schema.md` |
| `RuntimeOverrides.SECTION_MAP_PATH` | path | Approved section map | `/.../_Planning/Section_Map.csv` |
| `RuntimeOverrides.PUBLICATION_RULES_PATH` | path | Approved rules | `/.../_Planning/Publication_Rules.md` |
| `ExpectedOutputs` | list[path] | All 7 outputs | (same as AllowedWriteTargets) |

## Optional brief fields

| Field | Type | Meaning | Example |
|---|---|---|---|
| `RuntimeOverrides.SUPERSESSION_MAP_PATH` | path | Active supersession map | `/.../SCA-006/.../Supersession_Map.csv` |
| `RuntimeOverrides.SECTION_CONTEXT_ROOT` | path | Section context packets | `/.../_Planning/section-context/` |
| `RuntimeOverrides.SECTIONS_ROOT` | path | Individual section output folders | `/.../_Publication/DBM/sections/` |
| `CustomInstructions` | string | Run-specific emphasis | `Pay special attention to shared utility cross-facility values.` |

## Runtime-override guidance

- All required inputs are expected to be available in valid pipeline runs. If any are missing, the skill sets `EvidenceBundleStatus = PARTIAL`.
- `SECTIONS_ROOT` provides access to individual section QA artifacts from `dbm-section-publish`. When available, the agent can cross-reference section-level adequacy findings.
- `--section-map` is always passed to substrate tools in pipeline mode (Section_Map.csv is the run-specific authority).

## Example INIT-TASK brief

```md
PURPOSE: Post-authoring concordance review for package RUN-20260422-175550.
ScopePath: /repo/domains/West_Doe_Comp_and_Liquids_DBM/_Publication/DBM/package/RUN-20260422-175550/review/
TaskSkill: dbm-postauthor-concordance
AllowedWriteTargets:
  - /repo/domains/West_Doe_Comp_and_Liquids_DBM/_Publication/DBM/package/RUN-20260422-175550/review/Evidence_Bundle_Summary.md
  - /repo/domains/West_Doe_Comp_and_Liquids_DBM/_Publication/DBM/package/RUN-20260422-175550/review/Section_Coverage.csv
  - /repo/domains/West_Doe_Comp_and_Liquids_DBM/_Publication/DBM/package/RUN-20260422-175550/review/Draft_Claims.csv
  - /repo/domains/West_Doe_Comp_and_Liquids_DBM/_Publication/DBM/package/RUN-20260422-175550/review/Body_Thinness.csv
  - /repo/domains/West_Doe_Comp_and_Liquids_DBM/_Publication/DBM/package/RUN-20260422-175550/review/TBD_Inventory.csv
  - /repo/domains/West_Doe_Comp_and_Liquids_DBM/_Publication/DBM/package/RUN-20260422-175550/review/Candidate_Findings.csv
  - /repo/domains/West_Doe_Comp_and_Liquids_DBM/_Publication/DBM/package/RUN-20260422-175550/review/Publication_Review_Disposition.csv
RuntimeOverrides:
  ASSEMBLED_DBM_PATH: /repo/domains/West_Doe_Comp_and_Liquids_DBM/_Publication/DBM/package/RUN-20260422-175550/Rewritten_DBM.md
  REVIEW_OUTPUT_DIR: /repo/domains/West_Doe_Comp_and_Liquids_DBM/_Publication/DBM/package/RUN-20260422-175550/review/
  DOMAIN_ROOT: /repo/domains/West_Doe_Comp_and_Liquids_DBM/
  PUBLICATION_SCHEMA_PATH: /repo/domains/West_Doe_Comp_and_Liquids_DBM/_Publication/DBM/_Planning/Publication_Schema.md
  SECTION_MAP_PATH: /repo/domains/West_Doe_Comp_and_Liquids_DBM/_Publication/DBM/_Planning/Section_Map.csv
  PUBLICATION_RULES_PATH: /repo/domains/West_Doe_Comp_and_Liquids_DBM/_Publication/DBM/_Planning/Publication_Rules.md
  SECTIONS_ROOT: /repo/domains/West_Doe_Comp_and_Liquids_DBM/_Publication/DBM/sections/
ExpectedOutputs:
  - /repo/domains/West_Doe_Comp_and_Liquids_DBM/_Publication/DBM/package/RUN-20260422-175550/review/Evidence_Bundle_Summary.md
  - /repo/domains/West_Doe_Comp_and_Liquids_DBM/_Publication/DBM/package/RUN-20260422-175550/review/Section_Coverage.csv
  - /repo/domains/West_Doe_Comp_and_Liquids_DBM/_Publication/DBM/package/RUN-20260422-175550/review/Draft_Claims.csv
  - /repo/domains/West_Doe_Comp_and_Liquids_DBM/_Publication/DBM/package/RUN-20260422-175550/review/Body_Thinness.csv
  - /repo/domains/West_Doe_Comp_and_Liquids_DBM/_Publication/DBM/package/RUN-20260422-175550/review/TBD_Inventory.csv
  - /repo/domains/West_Doe_Comp_and_Liquids_DBM/_Publication/DBM/package/RUN-20260422-175550/review/Candidate_Findings.csv
  - /repo/domains/West_Doe_Comp_and_Liquids_DBM/_Publication/DBM/package/RUN-20260422-175550/review/Publication_Review_Disposition.csv
```
