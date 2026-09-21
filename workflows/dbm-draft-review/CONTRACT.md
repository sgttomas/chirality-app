# dbm-draft-review contract

## Brief

This file defines the INIT-TASK dispatch contract for `TASK + dbm-draft-review`.

### Purpose

Use this workflow to review a human-prepared draft DBM against the governed knowledge base. The workflow builds a review substrate using deterministic tools, then uses agent judgment to prepare candidate findings for human disposition via review.

### Scope model

- `ScopePath` should be the review output directory.
- `AllowedWriteTargets` must name exactly the 6 output files under REVIEW_OUTPUT_DIR.
- The brief must not grant write access to KTY folders, decomposition truth, publication planning artifacts, or the draft DBM file.

### Required brief fields

| Field | Type | Meaning | Example |
|---|---|---|---|
| `PURPOSE` | string | Why review is being run | `Review colleague's draft DBM against governed Deepcut knowledge base.` |
| `ScopePath` | path | Review output directory | `/repo/.../_Publication/DBM/_Review/REVIEW-20260422-1400/` |
| `Workflow` | string | Must equal `dbm-draft-review` | `dbm-draft-review` |
| `AllowedWriteTargets` | list[path] | Exactly the 6 output files | `[/.../Evidence_Bundle_Summary.md, /.../Section_Coverage.csv, /.../Draft_Claims.csv, /.../Body_Thinness.csv, /.../TBD_Inventory.csv, /.../Candidate_Findings.csv]` |
| `RuntimeOverrides.DRAFT_DBM_PATH` | path | The draft document to review | `/repo/.../colleague_draft_dbm.md` |
| `RuntimeOverrides.REVIEW_OUTPUT_DIR` | path | Output directory for evidence bundle | `/repo/.../_Publication/DBM/_Review/REVIEW-20260422-1400/` |
| `RuntimeOverrides.DOMAIN_ROOT` | path | DOMAIN decomposition root | `/repo/.../West_Doe_Deepcut_DBM/` |
| `ExpectedOutputs` | list[path] | All 6 outputs | `[/.../Evidence_Bundle_Summary.md, /.../Section_Coverage.csv, /.../Draft_Claims.csv, /.../Body_Thinness.csv, /.../TBD_Inventory.csv, /.../Candidate_Findings.csv]` |

### Optional brief fields

| Field | Type | Meaning | Example |
|---|---|---|---|
| `RuntimeOverrides.PUBLICATION_SCHEMA_PATH` | path | Approved publication schema | `/.../_Planning/Publication_Schema.md` |
| `RuntimeOverrides.SECTION_MAP_PATH` | path | Approved section map | `/.../_Planning/Section_Map.csv` |
| `RuntimeOverrides.PUBLICATION_RULES_PATH` | path | Approved publication rules | `/.../_Planning/Publication_Rules.md` |
| `RuntimeOverrides.SUPERSESSION_MAP_PATH` | path | Active supersession map | `/.../SCA-006/.../Supersession_Map.csv` |
| `RuntimeOverrides.SECTION_CONTEXT_ROOT` | path | Section context packets | `/.../_Planning/section-context/` |
| `RuntimeOverrides.EXISTING_PUBLISHED_DBM_PATH` | path | Previous published DBM for comparison | `/.../package/RUN-.../Rewritten_DBM.md` |
| `CustomInstructions` | string | Run-specific emphasis | `Focus on Utilities section (SEC-07) instrument air content.` |

### Runtime-override guidance

- When `PUBLICATION_SCHEMA_PATH` is missing, section coverage scanning is skipped and `EvidenceBundleStatus` is `PARTIAL`.
- When `SECTION_MAP_PATH` is missing, body thinness density ratios and governed-truth KA comparison are degraded. The bundle is `PARTIAL`.
- When `SUPERSESSION_MAP_PATH` is missing, supersession compliance is not assessed. The bundle notes this as a dimension not assessed.
- The workflow does not require all optional inputs to produce useful findings. It degrades honestly — recording what was and was not assessed.

### Recommended CustomInstructions content

For format-critical defense-in-depth, orchestrators should include:

```
Emit all 6 evidence bundle files. Set Origin = AGENT_CHECK on every Candidate_Findings.csv row.
Use only controlled enum values for FindingType and Severity.
If governed inputs are missing, set EvidenceBundleStatus = PARTIAL and list affected dimensions.
```

### Example INIT-TASK brief

```md
PURPOSE: Review colleague's draft DBM against governed Deepcut knowledge base.
ScopePath: /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/_Review/REVIEW-20260422-1400/
Workflow: dbm-draft-review
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

## Acceptance

### Minimum output validity checks

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

### Required Candidate_Findings.csv schema

Required columns (in order):

- `FindingID` — sequential `F-001`, `F-002`, ...
- `FindingType` — controlled enum: `INCORRECT`, `UNSUPPORTED`, `MISSING`, `FLATTENED`, `OUTDATED`, `INCOMPLETE`
- `Severity` — controlled enum: `HIGH`, `MEDIUM`, `LOW`, `ADVISORY`
- `Origin` — `AGENT_CHECK` (required for review workflow compatibility)
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

### Required Section_Coverage.csv schema

- `SectionID`
- `SectionTitle`
- `SectionType`
- `SectionOrder`
- `CoverageStatus` — `COVERED`, `PARTIAL`, `MISSING`, `EXTRA`
- `DraftHeading`
- `DraftLineNumber`
- `AuthoritySource` — `SECTION_MAP` or `SCHEMA_ONLY`

### Required Draft_Claims.csv schema

- `ClaimID` — sequential `C-001`, `C-002`, ...
- `SectionHeading`
- `DraftLineNumber`
- `RawText`
- `ExtractedValue`
- `Unit`
- `ContextType` — `TABLE_CELL`, `PROSE_VALUE`, `CONFIGURATION`, `TBD_VALUE`
- `NearestTerm`

### Required Body_Thinness.csv schema

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

### Required TBD_Inventory.csv schema

- `MarkerID` — sequential `M-001`, `M-002`, ...
- `MarkerType` — `TBD`, `TBC`, `ASSUMPTION`
- `DraftLineNumber`
- `DraftContext` — full line text, truncated to 200 chars
- `NearestSectionID`
- `KBResolutionStatus` — `RESOLVED`, `UNRESOLVED`, `NOT_IN_KB`, `NO_KB_PROVIDED`
- `KBResolutionRef`
- `Notes`

### Required Evidence_Bundle_Summary.md structure

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

### Failure reporting expectations

Use `FAILED_INPUTS` when:
- `DRAFT_DBM_PATH` is missing or unreadable
- `REVIEW_OUTPUT_DIR` cannot be created or falls outside allowed scope
- `DOMAIN_ROOT` does not exist

Use `FAILED` when:
- Required outputs cannot be written despite valid inputs
- A tool exits with code 1 (fatal error) and cannot be skipped

Do NOT use `FAILED` for missing optional governed inputs — use `EvidenceBundleStatus = PARTIAL` instead.

## Tool use

### Preferred tool order

1. Run `tools/review/scan_section_coverage.py` — structural coverage substrate.
2. Run `tools/review/extract_claims.py` — value/parameter/term extraction substrate.
3. Run `tools/review/scan_tbd_markers.py` — TBD/TBC/ASSUMPTION marker substrate.
4. Run `tools/review/check_body_thinness.py` — body underdevelopment signal substrate.
5. Read substrate outputs and draft sections alongside mapped KA artifacts for agent judgment.
6. Emit the 6 evidence bundle files.

### Allowed deterministic tools

#### Operationally invoked

- `tools/review/scan_section_coverage.py` — compare draft section headings against Publication_Schema.md section table, optionally enriched by Section_Map.csv.
- `tools/review/extract_claims.py` — locate engineering values, design parameters, configuration statements, and controlled terms in draft text.
- `tools/review/scan_tbd_markers.py` — locate TBD/TBC/ASSUMPTION markers with line numbers and optional KB cross-reference.
- `tools/review/check_body_thinness.py` — compute section body underdevelopment signals (line counts, density ratios, table presence).

### Expected use of reasoning

- **Governed-truth comparison:** Read mapped KA artifacts (from Section_Map.csv, PRIMARY role) alongside draft sections. Judge whether governed design-basis content is materially represented — configurations, operating modes, interfaces, design parameters, tables.
- **Supersession compliance:** When Supersession_Map.csv is provided, verify draft uses current design-basis values, not superseded source wording.
- **Materiality judgment:** Decide which substrate signals represent material engineering concerns versus harmless formatting variations. A tool can extract "2 x 100%" from the draft; the agent decides whether it matches the governed "2 × 100% capacity air compressors in lead-lag operation."
- **Finding classification:** Assign the 6-type taxonomy and severity to each candidate finding. Provide rationale and evidence citations.
- **Completeness assessment:** Judge whether sections adequately represent their mapped KTY content at the level expected for a senior-engineer Design Basis Memorandum.
- **Evidence bundle assembly:** Write the Evidence_Bundle_Summary.md with narrative interpretation of substrate results and agent findings.

### Disallowed use

- No modification of the draft, knowledge base, publication artifacts, or governed pointers.
- No dispatching other agents or workflows.
- No inline reimplementation of deterministic checks that belong in the tool layer (e.g., do not manually regex-scan for TBD markers when `scan_tbd_markers.py` does this).
- No reading of raw source DBM files except through structured supersession map comparisons.
- No invention of engineering facts not present in the governed knowledge base.
- No automatic readiness verdicts, PASS/FAIL judgments, or blocking decisions. Findings are candidates for human disposition.

### Write boundary

Writes are limited to the 6 evidence bundle files, all under the REVIEW_OUTPUT_DIR specified in the brief:

- `Evidence_Bundle_Summary.md`
- `Section_Coverage.csv`
- `Draft_Claims.csv`
- `Body_Thinness.csv`
- `TBD_Inventory.csv`
- `Candidate_Findings.csv`

No other file may be created, modified, or deleted.
