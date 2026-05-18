---
name: dbm-postauthor-concordance
description: Post-authoring evidence bundle and review for pipeline-produced DBM sections — build review substrate, prepare candidate findings for human readiness judgment.
compatibility: Chirality TASK; dispatched by DBM_PUBLISHER Gate 6
allowed-tools: python3 tools/review/scan_section_coverage.py:*, python3 tools/review/extract_claims.py:*, python3 tools/review/scan_tbd_markers.py:*, python3 tools/review/check_body_thinness.py:*
metadata:
  chirality-skill-version: "1"
  chirality-task-profile: NONE
---

# SKILL - dbm-postauthor-concordance

## Purpose

Post-authoring review for pipeline-produced DBM sections. Build a structured evidence bundle using deterministic substrate tools, then use agent judgment to read governed truth alongside the authored DBM and prepare candidate findings for human readiness judgment.

This skill replaces the pre-authoring concordance model (Gates 3-4 concordance freeze). Concordance is now extracted and validated *after* authoring rather than constraining authoring. The evidence bundle is not a quality gate — findings are candidates for human disposition, not automatic blockers.

This skill is a reviewer only. It does not modify section outputs, the knowledge base, publication planning artifacts, or governed pointers.

## Suitable agent shells

- `TASK` (generic shell mode, no profile)

Typical dispatcher: `DBM_PUBLISHER` during Gate 6 after section synthesis and package assembly.

## Inputs

### Required

- `ASSEMBLED_DBM_PATH` — path to the assembled Rewritten_DBM.md (or sections root)
- `REVIEW_OUTPUT_DIR` — output directory for the evidence bundle
- `DOMAIN_ROOT` — absolute path to the DOMAIN root
- `PUBLICATION_SCHEMA_PATH` — approved Publication_Schema.md
- `SECTION_MAP_PATH` — approved Section_Map.csv
- `PUBLICATION_RULES_PATH` — approved Publication_Rules.md

### Optional

- `SUPERSESSION_MAP_PATH` — Supersession_Map.csv from active SCA
- `SECTION_CONTEXT_ROOT` — directory containing SEC-##_Context.md packets
- `SECTIONS_ROOT` — individual section output folders (for section-level QA artifact access)

## Runtime overrides

| Key | Meaning | Default | Allowed values |
|---|---|---|---|
| `ASSEMBLED_DBM_PATH` | Assembled DBM to review | **Required** | Absolute path to Rewritten_DBM.md |
| `REVIEW_OUTPUT_DIR` | Evidence bundle output root | **Required** | Path under `_Publication/DBM/package/<run-id>/review/` |
| `DOMAIN_ROOT` | DOMAIN decomposition root | **Required** | Absolute path to domain directory |
| `PUBLICATION_SCHEMA_PATH` | Publication schema | **Required** | Markdown path under `_Planning/` |
| `SECTION_MAP_PATH` | Section map | **Required** | CSV path under `_Planning/` |
| `PUBLICATION_RULES_PATH` | Publication rules | **Required** | Markdown path under `_Planning/` |
| `SUPERSESSION_MAP_PATH` | Supersession map | unset | CSV path under active SCA |
| `SECTION_CONTEXT_ROOT` | Section context packets | unset | Directory path |
| `SECTIONS_ROOT` | Section output folders | unset | Path under `_Publication/DBM/sections/` |

## Two-level status model

### EvidenceBundleStatus (process validity)

| Status | Meaning |
|---|---|
| `COMPLETE` | All tools ran, all governed inputs available, all substrate artifacts written |
| `PARTIAL` | One or more governed inputs unavailable; substrate is incomplete |
| `TOOL_ERROR` | A tool failed; substrate is unreliable |

Expected to be `COMPLETE` in valid pipeline runs, but the skill must still handle `PARTIAL` and `TOOL_ERROR` — files can be missing, malformed, stale, or unreadable.

### ReviewStatus (agent candidate-finding result)

| Status | Meaning |
|---|---|
| `NO_FINDINGS` | Agent review produced no candidate findings |
| `FINDINGS_FOR_DISPOSITION` | Agent prepared candidate findings for human disposition |
| `REVIEW_INCOMPLETE` | Agent could not complete review |

## Finding taxonomy (controlled enum)

| Type | Meaning |
|---|---|
| `INCORRECT` | Authored content contradicts governed KTY/SCA/supersession truth |
| `UNSUPPORTED` | Authored content makes a claim not warranted by the knowledge base |
| `MISSING` | Governed material exists but is absent from the authored content |
| `FLATTENED` | Authored content converts TBD/conflict/assumption into a firm fact |
| `OUTDATED` | Authored content uses superseded source DBM content |
| `INCOMPLETE` | Authored content has the right topic but lacks required engineering detail |

## Finding severity (controlled enum)

| Severity | Meaning |
|---|---|
| `HIGH` | Significant technical or governance concern |
| `MEDIUM` | Notable gap or inconsistency |
| `LOW` | Minor quality observation |
| `ADVISORY` | Noted for record; no action expected |

## Method

### Tool-first: build review substrate

1. **Validate inputs and write boundary.** Confirm all required paths exist. Create output directory if absent. If any required input is missing or unreadable, set `EvidenceBundleStatus = PARTIAL` and record the gap.

2. **Run `scan_section_coverage.py`.** Pass `--section-map` (required for pipeline review — Section_Map.csv is the run-specific authority after Gate 4). Write output to `{REVIEW_OUTPUT_DIR}/Section_Coverage.csv`.

3. **Run `extract_claims.py`.** Extract engineering values, parameters, configuration statements from assembled DBM. Write output to `{REVIEW_OUTPUT_DIR}/Draft_Claims.csv`.

4. **Run `scan_tbd_markers.py`.** Scan assembled DBM for TBD/TBC/ASSUMPTION markers with KB cross-reference. Write output to `{REVIEW_OUTPUT_DIR}/TBD_Inventory.csv`.

5. **Run `check_body_thinness.py`.** Pass `--section-map` and `--schema`. Write output to `{REVIEW_OUTPUT_DIR}/Body_Thinness.csv`.

### Agent judgment: review governed truth against authored content

6. **Read authored sections against mapped KA artifacts.** Use Section_Map.csv to identify PRIMARY-role KA artifacts per section. For each section, judge materiality, accuracy, and completeness. This is the core engineering judgment step.

7. **Check supersession compliance.** When SUPERSESSION_MAP_PATH is provided, verify authored content uses current values.

8. **Classify candidate findings.** Every finding must set `Origin = AGENT_CHECK`, cite governed-truth evidence, and trace to substrate where applicable.

9. **Emit evidence bundle and disposition artifact.** Write all outputs to REVIEW_OUTPUT_DIR. Write `Publication_Review_Disposition.csv` with `HumanDisposition = TBD` for all rows.

## Outputs

All outputs are written to REVIEW_OUTPUT_DIR. 7 files total:

| File | Purpose |
|---|---|
| `Evidence_Bundle_Summary.md` | `EvidenceBundleStatus`, `ReviewStatus`, tool run results, input provenance |
| `Section_Coverage.csv` | Structural coverage |
| `Draft_Claims.csv` | Values, parameters, terms located in authored text |
| `Body_Thinness.csv` | Section body underdevelopment signals |
| `TBD_Inventory.csv` | TBD/TBC/ASSUMPTION markers with KB cross-reference |
| `Candidate_Findings.csv` | Agent-prepared findings for human disposition |
| `Publication_Review_Disposition.csv` | Disposition artifact for human decision recording |

## Candidate_Findings.csv schema

Same as `dbm-draft-review`:

`FindingID, FindingType, Severity, Origin, DraftLocation, DraftLineNumber, DraftText, GovernedTruthRef, GovernedTruthValue, SectionID, KTYRef, KARef, SupersessionRef, Explanation, EvidenceSource`

## Publication_Review_Disposition.csv schema

`FindingID, FindingType, Severity, SectionID, Explanation, EvidenceSource, ProposedDisposition, HumanDisposition, HumanNotes, DispositionDate`

- `FindingID`: matches `Candidate_Findings.csv` FindingID
- `ProposedDisposition`: agent-recommended disposition
- `HumanDisposition`: `TBD` until human rules. Allowed values: `ACCEPT_AS_IS`, `REVISE`, `WAIVE_WITH_RATIONALE`, `DEFER`, `NOT_APPLICABLE`
- `HumanNotes`: empty until human fills in
- `DispositionDate`: empty until human fills in

DBM_PUBLISHER does not update acceptance pointers until all `HumanDisposition` values are recorded (no `TBD` remaining).

## Evidence_Bundle_Summary.md structure

Same required H2 headings as `dbm-draft-review`.

## Non-negotiable constraints

- The skill does NOT modify section outputs, knowledge base, publication artifacts, or governed pointers.
- Write boundary is exactly the 7 output files under REVIEW_OUTPUT_DIR.
- No finding is treated as accepted truth. Findings are candidates for human disposition.
- `Origin = AGENT_CHECK` on every finding row.
- No automatic readiness verdicts, PASS/FAIL judgments, or blocking decisions.
- `Publication_Review_Disposition.csv` is emitted with `HumanDisposition = TBD` — the skill does not pre-fill human decisions.

## QA expectations

- All 7 required outputs exist under REVIEW_OUTPUT_DIR.
- All writes stayed inside REVIEW_OUTPUT_DIR.
- `Candidate_Findings.csv` uses only controlled enum values for FindingType and Severity.
- Every finding has `Origin = AGENT_CHECK`, non-empty Explanation and EvidenceSource.
- `Publication_Review_Disposition.csv` has one row per finding, with `HumanDisposition = TBD`.
- `Evidence_Bundle_Summary.md` contains both `EvidenceBundleStatus` and `ReviewStatus`.
