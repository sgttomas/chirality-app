---
name: dbm-publish
description: Assemble the full rewritten DBM package from approved section outputs, invoke deterministic concordance checks, and classify publication readiness.
compatibility: Chirality TASK; dispatched by DBM_PUBLISHER after section outputs exist for the current publication run.
allowed-tools: python3 tools/publication/assemble_publication.py:*, python3 tools/publication/check_concordance.py:*, python3 tools/publication/validate_source_supersession.py:*
metadata:
  chirality-skill-version: "1"
  chirality-task-profile: NONE
---

# SKILL — dbm-publish

## Purpose

Run the **package-level bounded publication gate** after section outputs already exist. This skill:
- invokes deterministic assembly,
- invokes deterministic concordance checking,
- aggregates per-section assertion-discovery outputs into a package-level expansion view,
- reviews the assembled package for qualitative publication readiness,
- writes `Publication_Readiness.md`,
- writes `Rerun_Recommendations.csv`.

It is **not** a dispatcher and it does **not** rewrite KTY-local truth or redesign the publication plan.

## Suitable agent shells

- `TASK` (generic shell mode, no profile)

Typical dispatcher: `DBM_PUBLISHER` after the section layer is complete enough for package assembly.

## Inputs

### Required

- `PUBLICATION_ROOT`
- `PUBLICATION_INPUT_MANIFEST`
- `PUBLICATION_SCHEMA_PATH`
- `SECTION_MAP_PATH`
- `PUBLICATION_RULES_PATH`
- `PUBLICATION_CONCORDANCE_REGISTER_PATH`
- `SECTIONS_ROOT`
- `PACKAGE_OUTPUT_ROOT`

### Optional

- `RUN_LABEL`
- `SOURCE_DOMAIN`
- `HYPERGRAPH_USE_MODE`
- `HYPERGRAPH_SNAPSHOT_PATH`
- `HYPERGRAPH_RUN_SUMMARY_PATH`
- `HYPERGRAPH_QA_REPORT_PATH`
- `HYPERGRAPH_NODES_PATH`
- `HYPERGRAPH_HYPEREDGES_PATH`
- `HYPERGRAPH_EVIDENCE_ROOT`
- `HYPERGRAPH_QA_VERDICT`
- `HYPERGRAPH_LIMITATIONS`
- `HYPERGRAPH_QA_BINDING_POLICY`

## Runtime overrides

| Key | Meaning | Default | Allowed values |
|---|---|---|---|
| `PUBLICATION_ROOT` | Publication tool root for the run | **Required** | Path to `_Publication/DBM/` |
| `PUBLICATION_INPUT_MANIFEST` | Frozen exact input-path manifest | **Required** | Markdown path |
| `PUBLICATION_SCHEMA_PATH` | Approved publication schema | **Required** | Markdown path |
| `SECTION_MAP_PATH` | Approved section map | **Required** | CSV path |
| `PUBLICATION_RULES_PATH` | Approved publication rules | **Required** | Markdown path |
| `PUBLICATION_CONCORDANCE_REGISTER_PATH` | Approved concordance register | **Required** | CSV path |
| `SECTIONS_ROOT` | Root containing current section output bundles | **Required** | Path under `_Publication/DBM/sections/` |
| `PACKAGE_OUTPUT_ROOT` | Root for immutable package snapshots | **Required** | Path under `_Publication/DBM/package/` |
| `RUN_LABEL` | Optional human-friendly run label | timestamped | Non-empty string |
| `SOURCE_DOMAIN` | Source domain label | inferred | Non-empty string |
| `HYPERGRAPH_USE_MODE` | Whether hypergraph evidence is admitted for this run | `NONE` | `NONE`, `AUXILIARY_PLANNING`, `AUXILIARY_QA`, `AUXILIARY_PLANNING_AND_QA` |
| `HYPERGRAPH_SNAPSHOT_PATH` | Exact path to the admitted hypergraph snapshot | unset | Path under `_Aggregation/Hypergraph/` |
| `HYPERGRAPH_RUN_SUMMARY_PATH` | Exact path to the hypergraph run summary | unset | Path |
| `HYPERGRAPH_QA_REPORT_PATH` | Exact path to the hypergraph QA report | unset | Path |
| `HYPERGRAPH_NODES_PATH` | Exact path to the hypergraph nodes CSV | unset | Path |
| `HYPERGRAPH_HYPEREDGES_PATH` | Exact path to the hypergraph hyperedges CSV | unset | Path |
| `HYPERGRAPH_EVIDENCE_ROOT` | Root folder containing hypergraph evidence CSVs | unset | Path under `_Aggregation/Hypergraph/` |
| `HYPERGRAPH_QA_VERDICT` | QA verdict for the admitted hypergraph snapshot | `NOT_USED` | `NON_BLOCKING`, `BLOCKED`, `NOT_USED` |
| `HYPERGRAPH_LIMITATIONS` | Free-text list of known defects constraining allowed use | unset | Free text |
| `HYPERGRAPH_QA_BINDING_POLICY` | Whether hypergraph QA findings can block package readiness | `ADVISORY_ONLY` | `ADVISORY_ONLY`, `BLOCK_ON_BINDING_FAILURE` |

## Tool usage

- This skill may invoke only these deterministic publication helpers:
  - `tools/publication/assemble_publication.py`
  - `tools/publication/check_concordance.py`
  - `tools/publication/validate_source_supersession.py` (when a supersession map is admitted)
- The `allowed-tools` frontmatter field is authoritative for this skill and enforces that deterministic tool boundary under `TASK`.

Disallowed behavior:
- No dispatching other workers.
- No rewriting of section body prose except for package-level readiness summaries.
- No mutation of KTY-local truth or section-planning artifacts.
- No partial-package concordance checking after targeted reruns.

## Outputs

The skill writes package-level review artifacts under the immutable package snapshot selected for the run:
- `Rewritten_DBM.md`
- `Trace_Appendix.md`
- `Publication_Manifest.md`
- `Publication_QA.md`
- `Publication_Concordance_Report.md`
- `Publication_Concordance_Findings.csv`
- `Publication_Concordance_Expansion_Candidates.csv`
- `Publication_Readiness.md`
- `Rerun_Recommendations.csv`
- `Source_Supersession_Report.md` (when source-supersession validation is run)
- `Source_Supersession_Findings.csv` (when source-supersession validation is run)

### `Publication_Concordance_Expansion_Candidates.csv` schema

Minimum required columns:
- `CandidateKey` — the proposed assertion key
- `SourceSection` — the section that discovered the candidate
- `DiscoverySource` — how the candidate was found (e.g., `PROSE_EXTRACTION`, `STRUCTURED_TABLE`, `CROSS_SECTION_REFERENCE`)
- `Criticality` — `HIGH`, `NORMAL`, or `LOW` (see criticality rubric in Method step 5)
- `TriageStatus` — `UNRESOLVED`, `DEFER`, `ACCEPT_AS_DOCUMENTED`, or `REJECT`
- `TriageJustification` — required when `TriageStatus` is not `UNRESOLVED`; documents the rationale for the triage decision
- `Notes` — additional context

## Required readiness classification

- `READY`
- `READY_WITH_MAJOR_NOTES`
- `BLOCKED`

## Non-negotiable constraints

- Deterministic completeness/trace checks belong in `assemble_publication.py`, not inline in the skill.
- Deterministic cross-section concordance checks belong in `check_concordance.py`, not inline in the skill.
- Package publication always checks the full current section set, even when only a subset of sections was rerun.
- The skill may judge readiness, but final acceptance remains human-owned.

## Hypergraph QA integration

When `HYPERGRAPH_USE_MODE` includes QA (`AUXILIARY_QA` or `AUXILIARY_PLANNING_AND_QA`) and the admitted hypergraph snapshot is available, the skill performs a package-level hypergraph QA sub-check as part of readiness classification.

### Finding classification

Hypergraph QA findings must be classified separately from deterministic concordance findings:
- `CONCORDANCE_BLOCKER` — deterministic concordance mismatch from the approved register (existing behavior, unchanged)
- `HYPERGRAPH_QA_WARNING` — hypergraph-derived structural concern that does not block readiness by default
- `HYPERGRAPH_QA_BLOCKER` — hypergraph-derived structural concern classified as blocking (e.g., a section-mapped KTY entirely absent from the admitted hypergraph, a major connected cluster with no corresponding section)

### Binding policy

Blocked hypergraph QA must only block package readiness when both conditions are met:
1. the manifest opted into hypergraph QA (`HYPERGRAPH_USE_MODE` includes QA), AND
2. the configured `HYPERGRAPH_QA_BINDING_POLICY` is `BLOCK_ON_BINDING_FAILURE`.

When `HYPERGRAPH_QA_BINDING_POLICY = ADVISORY_ONLY` (the default), `HYPERGRAPH_QA_BLOCKER` findings are reported but do not change the readiness classification.

When `HYPERGRAPH_QA_BINDING_POLICY = BLOCK_ON_BINDING_FAILURE`, `HYPERGRAPH_QA_BLOCKER` findings escalate the readiness classification to `BLOCKED`.

In either case, `HYPERGRAPH_QA_WARNING` findings never block readiness.

### Package summary requirements

`Publication_Readiness.md` must explicitly report:
- whether hypergraph evidence was used in the run,
- whether hypergraph use was planning-only or QA-binding,
- which `HYPERGRAPH_LIMITATIONS` were applied,
- the total count and severity of hypergraph QA findings when applicable.
- whether source-supersession validation was run,
- total source-fidelity assertions checked,
- total matched by supersession bindings,
- total unmatched source divergences,
- the blocking/non-blocking classification of source-supersession findings.

### Guard rails

- A `BLOCKED` `HYPERGRAPH_QA_VERDICT` must prevent hypergraph QA sub-checks from running. The package summary must note that hypergraph QA was skipped due to blocked snapshot quality.
- Hypergraph QA sub-checks must not replace, weaken, or override deterministic concordance checking. `CONCORDANCE_BLOCKER` findings always block readiness regardless of hypergraph policy.
- Hypergraph QA findings must appear in a dedicated section of `Publication_QA.md`, not interleaved with deterministic concordance findings.

## Method

1. **Validate package inputs.** Confirm required planning artifacts, section root, and package root exist and are within the approved publication tool root.
2. **Invoke deterministic assembly.** Run `assemble_publication.py`.
3. **Handle assembly failure conservatively.** If assembly exits non-zero, emit `BLOCKED` and record the tool failure.
4. **Invoke deterministic concordance checking.** Run `check_concordance.py`.
4a. **Invoke deterministic source-supersession validation (when admitted).** When a `Supersession_Map.csv` is frozen in the publication manifest, run `validate_source_supersession.py`. This tool compares source-fidelity-critical assertions against the admitted source authority, allows divergence only when matched by the active supersession map, and emits findings consumable by readiness classification. Unmatched source divergences (assertions that contradict the source with no supersession binding) are blocking findings, same as concordance blockers.
5. **Aggregate per-section discovery outputs.** Read every `SEC-##_ASSERTION_DISCOVERY.csv` under `SECTIONS_ROOT`, merge and conservatively deduplicate the candidates, classify unresolved items as `HIGH`, `NORMAL`, or `LOW`, and write `Publication_Concordance_Expansion_Candidates.csv`. **Criticality rubric:** `HIGH` — concordance-significant: the candidate represents a value with cross-section authority ambiguity, current-state scope risk (e.g., retired, shared, or cross-facility scope), or a design-basis value where independent section restatement without concordance tracking creates contradiction risk. `NORMAL` — useful multi-section coverage without blocking risk: the value appears across sections but authority is clear and values agree. `LOW` — local or prose-adjacent suggestion: single-section, minor, or editorial.
6. **Run optional hypergraph QA sub-check.** When `HYPERGRAPH_USE_MODE` includes QA and `HYPERGRAPH_QA_VERDICT != BLOCKED`, perform the package-level hypergraph QA checks defined in the Hypergraph QA integration section. Classify findings as `HYPERGRAPH_QA_WARNING` or `HYPERGRAPH_QA_BLOCKER`. Skip this step entirely when `HYPERGRAPH_USE_MODE = NONE` or `HYPERGRAPH_QA_VERDICT = BLOCKED`.
7. **Read the assembled DBM and all section QA artifacts.** Assess whether each section reads as coherent engineering prose under `Publication_Rules.md` rather than an artifact dump.
8. **Aggregate material QA signals.** At minimum summarize:
   - total conflicts,
   - total `TBD` / assumption / deferred-confirmation items,
   - total skipped inputs,
   - total material terminology normalizations,
   - total unresolved `HIGH`, `NORMAL`, and `LOW` concordance-expansion candidates,
   - total `HYPERGRAPH_QA_WARNING` and `HYPERGRAPH_QA_BLOCKER` findings (when hypergraph QA was run).
9. **Classify readiness.**
   - `BLOCKED` if required sections are missing, deterministic assembly failed, blocking concordance findings exist, unmatched source-supersession divergences exist, unresolved `HIGH` expansion candidates remain, or `HYPERGRAPH_QA_BLOCKER` findings exist when `HYPERGRAPH_QA_BINDING_POLICY = BLOCK_ON_BINDING_FAILURE`. **HIGH candidate triage:** Unresolved HIGH candidates block readiness until they are triaged. Triage means each HIGH candidate receives one of: `DEFER` (deferred to next register revision, with justification), `ACCEPT_AS_DOCUMENTED` (adequately covered by existing register keys or body prose), or `REJECT` (not a valid concordance item). Triaged HIGH candidates with documented justification are non-blocking. The triage must be presented to the human/controller for acceptance before readiness can advance.
   - `READY_WITH_MAJOR_NOTES` if no blocking condition remains but unresolved `NORMAL` expansion candidates, `HYPERGRAPH_QA_WARNING` findings, or other material quality/QA issues remain.
   - `READY` only if deterministic assembly/concordance pass, no material expansion candidates remain unresolved, and no unresolved hypergraph QA findings of any severity remain (when hypergraph QA was run).
10. **Emit package review artifacts.** Write `Publication_Readiness.md`, `Publication_Concordance_Expansion_Candidates.csv`, and `Rerun_Recommendations.csv`.

## `Rerun_Recommendations.csv` schema

Minimum columns:
- `SectionID`
- `RerunReason`
- `BlockingLevel`
- `SpecificFinding`
- `RecommendedAction`
- `Notes`

Recommended `BlockingLevel` values:
- `BLOCKING`
- `MAJOR_NOTE`
- `ADVISORY`
