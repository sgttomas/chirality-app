---
name: dbm-publish
description: Assemble the full rewritten DBM package from approved section outputs, invoke deterministic concordance checks, and classify publication readiness.
compatibility: Chirality TASK; dispatched by DBM_PUBLISHER after section outputs exist for the current publication run.
allowed-tools: python3 tools/publication/assemble_publication.py:*, python3 tools/publication/check_concordance.py:*
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

## Tool usage

- This skill may invoke only these deterministic publication helpers:
  - `tools/publication/assemble_publication.py`
  - `tools/publication/check_concordance.py`
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

## Required readiness classification

- `READY`
- `READY_WITH_MAJOR_NOTES`
- `BLOCKED`

## Non-negotiable constraints

- Deterministic completeness/trace checks belong in `assemble_publication.py`, not inline in the skill.
- Deterministic cross-section concordance checks belong in `check_concordance.py`, not inline in the skill.
- Package publication always checks the full current section set, even when only a subset of sections was rerun.
- The skill may judge readiness, but final acceptance remains human-owned.

## Method

1. **Validate package inputs.** Confirm required planning artifacts, section root, and package root exist and are within the approved publication tool root.
2. **Invoke deterministic assembly.** Run `assemble_publication.py`.
3. **Handle assembly failure conservatively.** If assembly exits non-zero, emit `BLOCKED` and record the tool failure.
4. **Invoke deterministic concordance checking.** Run `check_concordance.py`.
5. **Aggregate per-section discovery outputs.** Read every `SEC-##_ASSERTION_DISCOVERY.csv` under `SECTIONS_ROOT`, merge and conservatively deduplicate the candidates, classify unresolved items as `HIGH`, `NORMAL`, or `LOW`, and write `Publication_Concordance_Expansion_Candidates.csv`.
6. **Read the assembled DBM and all section QA artifacts.** Assess whether each section reads as coherent engineering prose under `Publication_Rules.md` rather than an artifact dump.
7. **Aggregate material QA signals.** At minimum summarize:
   - total conflicts,
   - total `TBD` / assumption / deferred-confirmation items,
   - total skipped inputs,
   - total material terminology normalizations,
   - total unresolved `HIGH`, `NORMAL`, and `LOW` concordance-expansion candidates.
8. **Classify readiness.**
   - `BLOCKED` if required sections are missing, deterministic assembly failed, blocking concordance findings exist, or unresolved `HIGH` expansion candidates remain.
   - `READY_WITH_MAJOR_NOTES` if no blocking condition remains but unresolved `NORMAL` expansion candidates or other material quality/QA issues remain.
   - `READY` only if deterministic assembly/concordance pass and no material expansion candidates remain unresolved.
9. **Emit package review artifacts.** Write `Publication_Readiness.md`, `Publication_Concordance_Expansion_Candidates.csv`, and `Rerun_Recommendations.csv`.

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
