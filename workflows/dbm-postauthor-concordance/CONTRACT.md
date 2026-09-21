# dbm-postauthor-concordance contract

## Brief

This file defines the INIT-TASK dispatch contract for `TASK + dbm-postauthor-concordance`.

### Purpose

Use this workflow after DBM section synthesis and package assembly to build a post-authoring evidence bundle and prepare candidate findings for human readiness judgment.

### Scope model

- `ScopePath` should be the review output directory within the package snapshot.
- `AllowedWriteTargets` must name exactly the 7 output files under REVIEW_OUTPUT_DIR.
- The brief must not grant write access to section output folders, planning artifacts, KTY folders, or source authority files.

### Required brief fields

| Field | Type | Meaning | Example |
|---|---|---|---|
| `PURPOSE` | string | Why review is being run | `Post-authoring concordance review for package RUN-20260422-175550.` |
| `ScopePath` | path | Review output directory | `/repo/.../_Publication/DBM/package/RUN-20260422-175550/review/` |
| `Workflow` | string | Must equal `dbm-postauthor-concordance` | `dbm-postauthor-concordance` |
| `AllowedWriteTargets` | list[path] | Exactly the 7 output files | `[/.../Evidence_Bundle_Summary.md, /.../Section_Coverage.csv, /.../Draft_Claims.csv, /.../Body_Thinness.csv, /.../TBD_Inventory.csv, /.../Candidate_Findings.csv, /.../Publication_Review_Disposition.csv]` |
| `RuntimeOverrides.ASSEMBLED_DBM_PATH` | path | Assembled Rewritten_DBM.md | `/.../package/RUN-.../Rewritten_DBM.md` |
| `RuntimeOverrides.REVIEW_OUTPUT_DIR` | path | Output directory | `/.../package/RUN-.../review/` |
| `RuntimeOverrides.DOMAIN_ROOT` | path | DOMAIN root | `/repo/.../West_Doe_Deepcut_DBM/` |
| `RuntimeOverrides.PUBLICATION_SCHEMA_PATH` | path | Approved schema | `/.../_Planning/Publication_Schema.md` |
| `RuntimeOverrides.SECTION_MAP_PATH` | path | Approved section map | `/.../_Planning/Section_Map.csv` |
| `RuntimeOverrides.PUBLICATION_RULES_PATH` | path | Approved rules | `/.../_Planning/Publication_Rules.md` |
| `ExpectedOutputs` | list[path] | All 7 outputs | (same as AllowedWriteTargets) |

### Optional brief fields

| Field | Type | Meaning | Example |
|---|---|---|---|
| `RuntimeOverrides.SUPERSESSION_MAP_PATH` | path | Active supersession map | `/.../SCA-006/.../Supersession_Map.csv` |
| `RuntimeOverrides.SECTION_CONTEXT_ROOT` | path | Section context packets | `/.../_Planning/section-context/` |
| `RuntimeOverrides.SECTIONS_ROOT` | path | Individual section output folders | `/.../_Publication/DBM/sections/` |
| `CustomInstructions` | string | Run-specific emphasis | `Pay special attention to shared utility cross-facility values.` |

### Runtime-override guidance

- All required inputs are expected to be available in valid pipeline runs. If any are missing, the workflow sets `EvidenceBundleStatus = PARTIAL`.
- `SECTIONS_ROOT` provides access to individual section QA artifacts from `dbm-section-publish`. When available, the agent can cross-reference section-level adequacy findings.
- `--section-map` is always passed to substrate tools in pipeline mode (Section_Map.csv is the run-specific authority).

### Example INIT-TASK brief

```md
PURPOSE: Post-authoring concordance review for package RUN-20260422-175550.
ScopePath: /repo/domains/West_Doe_Comp_and_Liquids_DBM/_Publication/DBM/package/RUN-20260422-175550/review/
Workflow: dbm-postauthor-concordance
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

## Acceptance

### Minimum output validity checks

The run is valid only when all of the following are true:

1. All 7 required outputs exist under REVIEW_OUTPUT_DIR:
   - `Evidence_Bundle_Summary.md`
   - `Section_Coverage.csv`
   - `Draft_Claims.csv`
   - `Body_Thinness.csv`
   - `TBD_Inventory.csv`
   - `Candidate_Findings.csv`
   - `Publication_Review_Disposition.csv`
2. All writes stayed inside REVIEW_OUTPUT_DIR.
3. No section outputs, planning artifacts, KTY files, or governed-pointer files were modified.
4. `Evidence_Bundle_Summary.md` contains all required H2 headings and both `EvidenceBundleStatus` and `ReviewStatus`.
5. `Candidate_Findings.csv` uses only controlled enum values for `FindingType` and `Severity`.
6. Every row in `Candidate_Findings.csv` has `Origin = AGENT_CHECK`.
7. Every row in `Candidate_Findings.csv` has a non-empty `Explanation` and `EvidenceSource`.
8. `Publication_Review_Disposition.csv` has exactly one row per `FindingID` in `Candidate_Findings.csv`.
9. Every row in `Publication_Review_Disposition.csv` has `HumanDisposition = TBD`.
10. `Section_Coverage.csv` has `AuthoritySource = SECTION_MAP` (pipeline review always uses section map).

### Required Candidate_Findings.csv schema

Same as `dbm-draft-review`:

`FindingID, FindingType, Severity, Origin, DraftLocation, DraftLineNumber, DraftText, GovernedTruthRef, GovernedTruthValue, SectionID, KTYRef, KARef, SupersessionRef, Explanation, EvidenceSource`

### Required Publication_Review_Disposition.csv schema

`FindingID, FindingType, Severity, SectionID, Explanation, EvidenceSource, ProposedDisposition, HumanDisposition, HumanNotes, DispositionDate`

- `FindingID`: must match a FindingID in Candidate_Findings.csv
- `ProposedDisposition`: agent-recommended disposition (free text)
- `HumanDisposition`: must be `TBD` at emission. Allowed values after human review: `ACCEPT_AS_IS`, `REVISE`, `WAIVE_WITH_RATIONALE`, `DEFER`, `NOT_APPLICABLE`
- `HumanNotes`: empty at emission
- `DispositionDate`: empty at emission

### Required substrate CSV schemas

Same as `dbm-draft-review` CONTRACT.md#acceptance — see that file for Section_Coverage.csv, Draft_Claims.csv, Body_Thinness.csv, and TBD_Inventory.csv column definitions.

### Required Evidence_Bundle_Summary.md structure

Same as `dbm-draft-review` — 10 required H2 headings.

### Failure reporting expectations

Use `FAILED_INPUTS` when:
- required runtime overrides are missing (ASSEMBLED_DBM_PATH, REVIEW_OUTPUT_DIR, DOMAIN_ROOT, PUBLICATION_SCHEMA_PATH, SECTION_MAP_PATH, PUBLICATION_RULES_PATH)
- output paths fall outside the package snapshot directory

Use `FAILED` when:
- required outputs cannot be written despite valid inputs
- a tool exits with code 1 (fatal error)

## Tool use

### Preferred tool order

1. Run `tools/review/scan_section_coverage.py` with `--section-map` (required in pipeline mode).
2. Run `tools/review/extract_claims.py` — value/parameter/term extraction.
3. Run `tools/review/scan_tbd_markers.py` — TBD/TBC/ASSUMPTION marker scan with KB cross-ref.
4. Run `tools/review/check_body_thinness.py` with `--section-map` and `--schema`.
5. Read substrate outputs and authored sections alongside mapped KA artifacts for agent judgment.
6. Emit the 7 output files (6 evidence bundle + disposition artifact).

### Allowed deterministic tools

#### Operationally invoked

- `tools/review/scan_section_coverage.py` — compare authored section headings against Publication_Schema.md, enriched by Section_Map.csv (run-specific authority).
- `tools/review/extract_claims.py` — locate engineering values, parameters, configuration statements, and controlled terms in authored text.
- `tools/review/scan_tbd_markers.py` — locate TBD/TBC/ASSUMPTION markers with KB cross-reference via Section_Map.csv Scoping.md discovery.
- `tools/review/check_body_thinness.py` — compute section body underdevelopment signals with mapped-artifact density ratios.

### Expected use of reasoning

- **Governed-truth comparison:** Read mapped KA artifacts (PRIMARY role) alongside authored sections. Judge whether governed design-basis content is materially represented.
- **Supersession compliance:** Verify authored content uses current values when Supersession_Map.csv is provided.
- **Materiality judgment:** Distinguish material engineering concerns from formatting variations.
- **Finding classification:** Assign 6-type taxonomy and severity. Cite governed evidence and trace to substrate.
- **Completeness assessment:** Judge section adequacy at the level expected for a senior-engineer Design Basis Memorandum.
- **Disposition preparation:** Write `Publication_Review_Disposition.csv` with agent-proposed dispositions and `HumanDisposition = TBD`.
- **Section QA cross-reference:** When SECTIONS_ROOT is available, cross-reference section-level QA artifacts from `dbm-section-publish` for additional context.

### Disallowed use

- No modification of section outputs, knowledge base, publication artifacts, or governed pointers.
- No dispatching other agents or workflows.
- No inline reimplementation of deterministic checks that belong in the tool layer.
- No reading of raw source DBM files except through structured supersession map comparisons.
- No invention of engineering facts not present in the governed knowledge base.
- No automatic readiness verdicts, PASS/FAIL judgments, or blocking decisions.
- No pre-filling of `HumanDisposition` values — all rows emit as `TBD`.

### Write boundary

Writes are limited to the 7 output files, all under the REVIEW_OUTPUT_DIR specified in the brief:

- `Evidence_Bundle_Summary.md`
- `Section_Coverage.csv`
- `Draft_Claims.csv`
- `Body_Thinness.csv`
- `TBD_Inventory.csv`
- `Candidate_Findings.csv`
- `Publication_Review_Disposition.csv`

No other file may be created, modified, or deleted.
