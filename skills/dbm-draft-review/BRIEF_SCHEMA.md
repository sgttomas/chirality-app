# BRIEF SCHEMA - dbm-draft-review

This file defines the INIT-TASK dispatch contract for `TASK + dbm-draft-review`.

## Purpose

Use this skill to review a human-prepared draft DBM against the governed knowledge base. The skill builds a review substrate using deterministic tools, then uses agent judgment to prepare candidate findings for human disposition via REVIEW.

## Scope model

- `ScopePath` should be the review output directory.
- `AllowedWriteTargets` must name exactly the 6 output files under REVIEW_OUTPUT_DIR.
- The brief must not grant write access to KTY folders, decomposition truth, publication planning artifacts, or the draft DBM file.

## Required brief fields

| Field | Type | Meaning | Example |
|---|---|---|---|
| `PURPOSE` | string | Why review is being run | `Review colleague's draft DBM against governed Deepcut knowledge base.` |
| `ScopePath` | path | Review output directory | `/repo/.../_Publication/DBM/_Review/REVIEW-20260422-1400/` |
| `TaskSkill` | string | Must equal `dbm-draft-review` | `dbm-draft-review` |
| `AllowedWriteTargets` | list[path] | Exactly the 6 output files | `[/.../Evidence_Bundle_Summary.md, /.../Section_Coverage.csv, /.../Draft_Claims.csv, /.../Body_Thinness.csv, /.../TBD_Inventory.csv, /.../Candidate_Findings.csv]` |
| `RuntimeOverrides.DRAFT_DBM_PATH` | path | The draft document to review | `/repo/.../colleague_draft_dbm.md` |
| `RuntimeOverrides.REVIEW_OUTPUT_DIR` | path | Output directory for evidence bundle | `/repo/.../_Publication/DBM/_Review/REVIEW-20260422-1400/` |
| `RuntimeOverrides.DOMAIN_ROOT` | path | DOMAIN decomposition root | `/repo/.../West_Doe_Deepcut_DBM/` |
| `ExpectedOutputs` | list[path] | All 6 outputs | `[/.../Evidence_Bundle_Summary.md, /.../Section_Coverage.csv, /.../Draft_Claims.csv, /.../Body_Thinness.csv, /.../TBD_Inventory.csv, /.../Candidate_Findings.csv]` |

## Optional brief fields

| Field | Type | Meaning | Example |
|---|---|---|---|
| `RuntimeOverrides.PUBLICATION_SCHEMA_PATH` | path | Approved publication schema | `/.../_Planning/Publication_Schema.md` |
| `RuntimeOverrides.SECTION_MAP_PATH` | path | Approved section map | `/.../_Planning/Section_Map.csv` |
| `RuntimeOverrides.PUBLICATION_RULES_PATH` | path | Approved publication rules | `/.../_Planning/Publication_Rules.md` |
| `RuntimeOverrides.SUPERSESSION_MAP_PATH` | path | Active supersession map | `/.../SCA-006/.../Supersession_Map.csv` |
| `RuntimeOverrides.SECTION_CONTEXT_ROOT` | path | Section context packets | `/.../_Planning/section-context/` |
| `RuntimeOverrides.EXISTING_PUBLISHED_DBM_PATH` | path | Previous published DBM for comparison | `/.../package/RUN-.../Rewritten_DBM.md` |
| `CustomInstructions` | string | Run-specific emphasis | `Focus on Utilities section (SEC-07) instrument air content.` |

## Runtime-override guidance

- When `PUBLICATION_SCHEMA_PATH` is missing, section coverage scanning is skipped and `EvidenceBundleStatus` is `PARTIAL`.
- When `SECTION_MAP_PATH` is missing, body thinness density ratios and governed-truth KA comparison are degraded. The bundle is `PARTIAL`.
- When `SUPERSESSION_MAP_PATH` is missing, supersession compliance is not assessed. The bundle notes this as a dimension not assessed.
- The skill does not require all optional inputs to produce useful findings. It degrades honestly — recording what was and was not assessed.

## Recommended CustomInstructions content

For format-critical defense-in-depth, orchestrators should include:

```
Emit all 6 evidence bundle files. Set Origin = AGENT_CHECK on every Candidate_Findings.csv row.
Use only controlled enum values for FindingType and Severity.
If governed inputs are missing, set EvidenceBundleStatus = PARTIAL and list affected dimensions.
```

## Example INIT-TASK brief

```md
PURPOSE: Review colleague's draft DBM against governed Deepcut knowledge base.
ScopePath: /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/_Review/REVIEW-20260422-1400/
TaskSkill: dbm-draft-review
AllowedWriteTargets:
  - /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/_Review/REVIEW-20260422-1400/Evidence_Bundle_Summary.md
  - /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/_Review/REVIEW-20260422-1400/Section_Coverage.csv
  - /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/_Review/REVIEW-20260422-1400/Draft_Claims.csv
  - /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/_Review/REVIEW-20260422-1400/Body_Thinness.csv
  - /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/_Review/REVIEW-20260422-1400/TBD_Inventory.csv
  - /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/_Review/REVIEW-20260422-1400/Candidate_Findings.csv
RuntimeOverrides:
  DRAFT_DBM_PATH: /repo/domains/West_Doe_Deepcut_DBM/_Sources/colleague_draft_dbm.md
  REVIEW_OUTPUT_DIR: /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/_Review/REVIEW-20260422-1400/
  DOMAIN_ROOT: /repo/domains/West_Doe_Deepcut_DBM/
  PUBLICATION_SCHEMA_PATH: /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/_Planning/Publication_Schema.md
  SECTION_MAP_PATH: /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/_Planning/Section_Map.csv
  PUBLICATION_RULES_PATH: /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/_Planning/Publication_Rules.md
ExpectedOutputs:
  - /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/_Review/REVIEW-20260422-1400/Evidence_Bundle_Summary.md
  - /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/_Review/REVIEW-20260422-1400/Section_Coverage.csv
  - /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/_Review/REVIEW-20260422-1400/Draft_Claims.csv
  - /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/_Review/REVIEW-20260422-1400/Body_Thinness.csv
  - /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/_Review/REVIEW-20260422-1400/TBD_Inventory.csv
  - /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/_Review/REVIEW-20260422-1400/Candidate_Findings.csv
```
