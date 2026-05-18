---
name: dbm-draft-review
description: Review a human-prepared draft DBM against the governed knowledge base — build review substrate, prepare candidate findings for human disposition.
compatibility: Chirality TASK; dispatched by WORKING_ITEMS or ORCHESTRATOR
allowed-tools: python3 tools/review/scan_section_coverage.py:*, python3 tools/review/extract_claims.py:*, python3 tools/review/scan_tbd_markers.py:*, python3 tools/review/check_body_thinness.py:*
metadata:
  chirality-skill-version: "1"
  chirality-task-profile: NONE
---

# SKILL - dbm-draft-review

## Purpose

Review a human-prepared draft DBM document against the governed knowledge base (decomposed KTY/KA artifacts, accepted SCA/supersession state, frozen publication planning artifacts). Build a structured evidence bundle using deterministic substrate tools, then use agent judgment to prepare candidate findings for human disposition via the REVIEW agent.

This skill is a reviewer only. It does not modify the draft, the knowledge base, publication planning artifacts, or governed pointers.

The evidence bundle is not a quality gate. Hard gates are limited to process validity (inputs exist, tools ran, schemas valid, provenance present). Engineering judgment about materiality, adequacy, and significance stays with the reviewing agent and human.

## Suitable agent shells

- `TASK` (generic shell mode, no profile)

Typical dispatchers: `WORKING_ITEMS` for interactive human-draft review sessions. `ORCHESTRATOR` for batch review.

## Inputs

### Required

- `DRAFT_DBM_PATH` — path to the draft DBM document (markdown)
- `REVIEW_OUTPUT_DIR` — output directory for the evidence bundle
- `DOMAIN_ROOT` — absolute path to the DOMAIN root (e.g., `West_Doe_Deepcut_DBM`)

### Optional (governed inputs — when unavailable, bundle status is PARTIAL)

- `PUBLICATION_SCHEMA_PATH` — approved Publication_Schema.md
- `SECTION_MAP_PATH` — approved Section_Map.csv
- `PUBLICATION_RULES_PATH` — approved Publication_Rules.md
- `SUPERSESSION_MAP_PATH` — Supersession_Map.csv from active SCA
- `SECTION_CONTEXT_ROOT` — directory containing SEC-##_Context.md packets
- `EXISTING_PUBLISHED_DBM_PATH` — previous pipeline-produced Rewritten_DBM.md for comparative review

## Runtime overrides

| Key | Meaning | Default | Allowed values |
|---|---|---|---|
| `DRAFT_DBM_PATH` | Draft to review | **Required** | Absolute path to markdown file |
| `REVIEW_OUTPUT_DIR` | Evidence bundle output root | **Required** | Path under `_Publication/DBM/_Review/<review-id>/` |
| `DOMAIN_ROOT` | DOMAIN decomposition root | **Required** | Absolute path to domain directory |
| `PUBLICATION_SCHEMA_PATH` | Publication schema | unset | Markdown path under `_Planning/` |
| `SECTION_MAP_PATH` | Section map | unset | CSV path under `_Planning/` |
| `PUBLICATION_RULES_PATH` | Publication rules | unset | Markdown path under `_Planning/` |
| `SUPERSESSION_MAP_PATH` | Supersession map | unset | CSV path under active SCA |
| `SECTION_CONTEXT_ROOT` | Section context packets | unset | Directory path |
| `EXISTING_PUBLISHED_DBM_PATH` | Published DBM for comparison | unset | Markdown path under `package/` |

## Two-level status model

### EvidenceBundleStatus (process validity)

| Status | Meaning |
|---|---|
| `COMPLETE` | All tools ran, all governed inputs available, all substrate artifacts written |
| `PARTIAL` | One or more governed inputs unavailable; substrate is incomplete — affected review dimensions listed in summary |
| `TOOL_ERROR` | A tool failed; substrate is unreliable |

### ReviewStatus (agent candidate-finding result)

| Status | Meaning |
|---|---|
| `NO_FINDINGS` | Agent review produced no candidate findings |
| `FINDINGS_FOR_DISPOSITION` | Agent prepared candidate findings for human disposition |
| `REVIEW_INCOMPLETE` | Agent could not complete review (substrate was PARTIAL or TOOL_ERROR) |

## Finding taxonomy (controlled enum)

| Type | Meaning |
|---|---|
| `INCORRECT` | Draft contradicts governed KTY/SCA/supersession truth |
| `UNSUPPORTED` | Draft makes a claim not warranted by the knowledge base |
| `MISSING` | Governed material exists but is absent from the draft |
| `FLATTENED` | Draft converts TBD/conflict/assumption into a firm fact |
| `OUTDATED` | Draft uses superseded source DBM content |
| `INCOMPLETE` | Draft has the right topic but lacks required engineering detail |

## Finding severity (controlled enum)

| Severity | Meaning |
|---|---|
| `HIGH` | Significant technical or governance concern |
| `MEDIUM` | Notable gap or inconsistency |
| `LOW` | Minor quality observation |
| `ADVISORY` | Noted for record; no action expected |

## Method

### Tool-first: build review substrate

1. **Validate inputs and write boundary.** Confirm DRAFT_DBM_PATH exists and is readable. Confirm REVIEW_OUTPUT_DIR resolves to an acceptable path. Create output directory if absent. If governed inputs (schema, section map, rules) are missing, set `EvidenceBundleStatus = PARTIAL` and record exactly what is unavailable and which review dimensions are affected. Do not improvise a weaker hidden standard.

2. **Run `scan_section_coverage.py`.** When PUBLICATION_SCHEMA_PATH is available, compare draft section headings against the schema. When SECTION_MAP_PATH is also available, pass it as `--section-map` for run-specific authority. Write output to `{REVIEW_OUTPUT_DIR}/Section_Coverage.csv`.

3. **Run `extract_claims.py`.** Extract engineering values, parameters, configuration statements, and controlled terms from draft text. Write output to `{REVIEW_OUTPUT_DIR}/Draft_Claims.csv`.

4. **Run `scan_tbd_markers.py`.** Scan draft for TBD/TBC/ASSUMPTION markers. When SECTION_MAP_PATH and DOMAIN_ROOT are available, pass them for KB cross-reference. Write output to `{REVIEW_OUTPUT_DIR}/TBD_Inventory.csv`.

5. **Run `check_body_thinness.py`.** Compute section body underdevelopment signals. Pass `--section-map` and `--schema` when available. Write output to `{REVIEW_OUTPUT_DIR}/Body_Thinness.csv`.

### Agent judgment: review governed truth against authored content

6. **Read draft sections against mapped KA artifacts.** When SECTION_MAP_PATH is available, read the Section_Map.csv to identify PRIMARY-role KA artifacts mapped to each section. For each section, read the draft section text and the mapped KA artifacts. Judge:
   - Is the governed design-basis content materially represented?
   - Are configurations, operating modes, interfaces, and design parameters accurately stated?
   - Are tables present where the source material warrants them?
   - Use publication rules and section-type expectations as the review standard.
   - This is the core engineering judgment step — it cannot be replaced by deterministic tools.

7. **Check supersession compliance.** When SUPERSESSION_MAP_PATH is provided, verify that the draft uses current design-basis values, not superseded source wording. Flag OUTDATED findings for any use of superseded content.

8. **Classify candidate findings.** Assign each finding a type from the 6-type taxonomy and a severity. Every finding must:
   - Cite governed-truth evidence (KA path, section, line) and draft location
   - Set `Origin = AGENT_CHECK` (required for REVIEW compatibility)
   - Trace to its substrate source where applicable (e.g., `Section_Coverage.csv:row-3`)

9. **Emit evidence bundle.** Write all outputs to REVIEW_OUTPUT_DIR. Set `EvidenceBundleStatus` and `ReviewStatus` in the summary.

## Outputs

All outputs are written to REVIEW_OUTPUT_DIR. Exactly 6 files:

| File | Purpose |
|---|---|
| `Evidence_Bundle_Summary.md` | `EvidenceBundleStatus`, `ReviewStatus`, tool run results, input provenance, dimensions assessed vs. not assessed |
| `Section_Coverage.csv` | Structural coverage (expected vs. found sections) |
| `Draft_Claims.csv` | Values, parameters, terms located in draft |
| `Body_Thinness.csv` | Section body underdevelopment signals |
| `TBD_Inventory.csv` | TBD/TBC/ASSUMPTION markers with KB cross-reference |
| `Candidate_Findings.csv` | Agent-prepared findings for human disposition |

## Candidate_Findings.csv schema

Required columns:

`FindingID, FindingType, Severity, Origin, DraftLocation, DraftLineNumber, DraftText, GovernedTruthRef, GovernedTruthValue, SectionID, KTYRef, KARef, SupersessionRef, Explanation, EvidenceSource`

- `FindingID`: sequential `F-001`, `F-002`, ...
- `FindingType`: controlled enum from finding taxonomy
- `Severity`: controlled enum from finding severity
- `Origin`: `AGENT_CHECK` for all findings (required for REVIEW agent compatibility)
- `EvidenceSource`: traces to substrate row (e.g., `Section_Coverage.csv:row-3`, `Body_Thinness.csv:row-7`) or `AGENT_REVIEW:<brief description>` for pure-judgment findings

## Evidence_Bundle_Summary.md structure

Required H2 headings:

1. `## Bundle Status` — `EvidenceBundleStatus` and `ReviewStatus` with explanation
2. `## Input Provenance` — paths consumed, which governed inputs were available vs. missing
3. `## Tool Run Results` — per-tool: ran/skipped, exit code, output path, row count
4. `## Review Dimensions` — which review dimensions were assessed (structural coverage, claim accuracy, supersession compliance, body adequacy, TBD fidelity) and which could not be assessed due to missing inputs
5. `## Section Coverage Summary` — narrative interpretation of Section_Coverage.csv
6. `## Body Adequacy Observations` — narrative interpretation of Body_Thinness.csv signals
7. `## TBD and Open-Item Assessment` — narrative interpretation of TBD_Inventory.csv
8. `## Accuracy and Completeness Assessment` — per-section assessment from agent judgment (step 6)
9. `## Supersession Compliance` — assessment from step 7 (or "not assessed" when no supersession map)
10. `## Recommendations` — actionable recommendations for the draft author, organized by severity

## Non-negotiable constraints

- The skill does NOT modify the draft, knowledge base, publication artifacts, or governed pointers.
- Write boundary is exactly the 6 output files under REVIEW_OUTPUT_DIR.
- Deterministic tool outputs feed reasoning; the skill does not reinvent mechanical checks inline.
- No finding is treated as accepted truth. Findings are candidates for human disposition.
- `Origin = AGENT_CHECK` on every finding row.
- When governed inputs are missing, the skill emits `EVIDENCE_INCOMPLETE` / `PARTIAL` — it does not silently downgrade the review standard.

## QA expectations

- All 6 required outputs exist under REVIEW_OUTPUT_DIR.
- All writes stayed inside REVIEW_OUTPUT_DIR.
- `Candidate_Findings.csv` uses only controlled enum values for FindingType and Severity.
- Every finding has a non-empty Explanation and EvidenceSource.
- `Evidence_Bundle_Summary.md` contains all required H2 headings.
