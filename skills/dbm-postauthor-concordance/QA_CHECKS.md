# QA CHECKS - dbm-postauthor-concordance

## Minimum output validity checks

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

## Required Candidate_Findings.csv schema

Same as `dbm-draft-review`:

`FindingID, FindingType, Severity, Origin, DraftLocation, DraftLineNumber, DraftText, GovernedTruthRef, GovernedTruthValue, SectionID, KTYRef, KARef, SupersessionRef, Explanation, EvidenceSource`

## Required Publication_Review_Disposition.csv schema

`FindingID, FindingType, Severity, SectionID, Explanation, EvidenceSource, ProposedDisposition, HumanDisposition, HumanNotes, DispositionDate`

- `FindingID`: must match a FindingID in Candidate_Findings.csv
- `ProposedDisposition`: agent-recommended disposition (free text)
- `HumanDisposition`: must be `TBD` at emission. Allowed values after human review: `ACCEPT_AS_IS`, `REVISE`, `WAIVE_WITH_RATIONALE`, `DEFER`, `NOT_APPLICABLE`
- `HumanNotes`: empty at emission
- `DispositionDate`: empty at emission

## Required substrate CSV schemas

Same as `dbm-draft-review` QA_CHECKS.md — see that file for Section_Coverage.csv, Draft_Claims.csv, Body_Thinness.csv, and TBD_Inventory.csv column definitions.

## Required Evidence_Bundle_Summary.md structure

Same as `dbm-draft-review` — 10 required H2 headings.

## Failure reporting expectations

Use `FAILED_INPUTS` when:
- required runtime overrides are missing (ASSEMBLED_DBM_PATH, REVIEW_OUTPUT_DIR, DOMAIN_ROOT, PUBLICATION_SCHEMA_PATH, SECTION_MAP_PATH, PUBLICATION_RULES_PATH)
- output paths fall outside the package snapshot directory

Use `FAILED` when:
- required outputs cannot be written despite valid inputs
- a tool exits with code 1 (fatal error)
