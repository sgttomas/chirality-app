# QA CHECKS - dbm-draft-review

## Minimum output validity checks

The run is valid only when all of the following are true:

1. All 6 required outputs exist under REVIEW_OUTPUT_DIR:
   - `Evidence_Bundle_Summary.md`
   - `Section_Coverage.csv`
   - `Draft_Claims.csv`
   - `Body_Thinness.csv`
   - `TBD_Inventory.csv`
   - `Candidate_Findings.csv`
2. All writes stayed inside REVIEW_OUTPUT_DIR.
3. No draft, knowledge base, publication, or governed-pointer files were modified.
4. `Evidence_Bundle_Summary.md` contains all required H2 headings.
5. `Evidence_Bundle_Summary.md` contains both `EvidenceBundleStatus` and `ReviewStatus` values from their respective controlled enums.
6. `Candidate_Findings.csv` uses only controlled enum values for `FindingType` (`INCORRECT`, `UNSUPPORTED`, `MISSING`, `FLATTENED`, `OUTDATED`, `INCOMPLETE`).
7. `Candidate_Findings.csv` uses only controlled enum values for `Severity` (`HIGH`, `MEDIUM`, `LOW`, `ADVISORY`).
8. Every row in `Candidate_Findings.csv` has `Origin = AGENT_CHECK`.
9. Every row in `Candidate_Findings.csv` has a non-empty `Explanation` and `EvidenceSource`.
10. `Section_Coverage.csv` has one row per expected section from the schema/section-map (when provided).

## Required Candidate_Findings.csv schema

Required columns (in order):

- `FindingID` — sequential `F-001`, `F-002`, ...
- `FindingType` — controlled enum: `INCORRECT`, `UNSUPPORTED`, `MISSING`, `FLATTENED`, `OUTDATED`, `INCOMPLETE`
- `Severity` — controlled enum: `HIGH`, `MEDIUM`, `LOW`, `ADVISORY`
- `Origin` — `AGENT_CHECK` (required for REVIEW agent compatibility)
- `DraftLocation` — section heading or identifiable draft location
- `DraftLineNumber` — 1-based line number in draft (0 if not applicable)
- `DraftText` — relevant draft text excerpt (truncated to 200 chars)
- `GovernedTruthRef` — path to governing KA artifact or resource
- `GovernedTruthValue` — expected value from governed truth
- `SectionID` — section identifier (e.g., `SEC-07`)
- `KTYRef` — knowledge type reference (e.g., `KTY-05-02`)
- `KARef` — knowledge artifact reference (e.g., `KA-01`)
- `SupersessionRef` — supersession map reference (empty if not applicable)
- `Explanation` — agent rationale for the finding
- `EvidenceSource` — traces to substrate row (e.g., `Section_Coverage.csv:row-3`) or `AGENT_REVIEW:<description>`

## Required Section_Coverage.csv schema

- `SectionID`
- `SectionTitle`
- `SectionType`
- `SectionOrder`
- `CoverageStatus` — `COVERED`, `PARTIAL`, `MISSING`, `EXTRA`
- `DraftHeading`
- `DraftLineNumber`
- `AuthoritySource` — `SECTION_MAP` or `SCHEMA_ONLY`

## Required Draft_Claims.csv schema

- `ClaimID` — sequential `C-001`, `C-002`, ...
- `SectionHeading`
- `DraftLineNumber`
- `RawText`
- `ExtractedValue`
- `Unit`
- `ContextType` — `TABLE_CELL`, `PROSE_VALUE`, `CONFIGURATION`, `TBD_VALUE`
- `NearestTerm`

## Required Body_Thinness.csv schema

- `SectionID`
- `SectionHeading`
- `DraftLineNumber`
- `TotalLines`
- `NonBlankLines`
- `TableRows`
- `HeadingCount`
- `MappedPrimaryKAs`
- `MappedSupportingKAs`
- `DensityRatio`
- `ExpectedTableClasses`
- `FoundTableCount`
- `Signals`

## Required TBD_Inventory.csv schema

- `MarkerID` — sequential `M-001`, `M-002`, ...
- `MarkerType` — `TBD`, `TBC`, `ASSUMPTION`
- `DraftLineNumber`
- `DraftContext` — full line text, truncated to 200 chars
- `NearestSectionID`
- `KBResolutionStatus` — `RESOLVED`, `UNRESOLVED`, `NOT_IN_KB`, `NO_KB_PROVIDED`
- `KBResolutionRef`
- `Notes`

## Required Evidence_Bundle_Summary.md structure

Required H2 headings (in order):

1. `## Bundle Status`
2. `## Input Provenance`
3. `## Tool Run Results`
4. `## Review Dimensions`
5. `## Section Coverage Summary`
6. `## Body Adequacy Observations`
7. `## TBD and Open-Item Assessment`
8. `## Accuracy and Completeness Assessment`
9. `## Supersession Compliance`
10. `## Recommendations`

## Failure reporting expectations

Use `FAILED_INPUTS` when:
- `DRAFT_DBM_PATH` is missing or unreadable
- `REVIEW_OUTPUT_DIR` cannot be created or falls outside allowed scope
- `DOMAIN_ROOT` does not exist

Use `FAILED` when:
- Required outputs cannot be written despite valid inputs
- A tool exits with code 1 (fatal error) and cannot be skipped

Do NOT use `FAILED` for missing optional governed inputs — use `EvidenceBundleStatus = PARTIAL` instead.
