---
name: dbm-publish
description: Assemble the full rewritten DBM package from approved section outputs and produce package QA artifacts.
compatibility: Chirality TASK; dispatched by DBM_PUBLISHER after section outputs exist for the current publication run.
allowed-tools: python3 tools/publication/assemble_publication.py:*, python3 tools/publication/validate_source_supersession.py:*
metadata:
  chirality-skill-version: "1"
  chirality-task-profile: NONE
---

# SKILL — dbm-publish

## Purpose

Run the **package-level bounded assembly** after section outputs already exist. This skill:
- invokes deterministic assembly,
- performs the package-level DBM content adequacy review in `FULL_ENGINEERING_DBM` mode,
- reviews the assembled package for qualitative readiness assessment,
- writes `Publication_Content_Adequacy.md` in `FULL_ENGINEERING_DBM` mode,
- writes `Publication_Readiness.md`,
- writes `Rerun_Recommendations.csv`.

Post-authoring concordance review is handled separately by `TASK + dbm-postauthor-concordance` after this skill completes package assembly.

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
- `SECTIONS_ROOT`
- `PACKAGE_OUTPUT_ROOT`

### Optional

- `DBM_OUTPUT_MODE` — `FULL_ENGINEERING_DBM|DBM_DIGEST`, default `FULL_ENGINEERING_DBM`
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
| `SECTIONS_ROOT` | Root containing current section output bundles | **Required** | Path under `_Publication/DBM/sections/` |
| `PACKAGE_OUTPUT_ROOT` | Root for immutable package snapshots | **Required** | Path under `_Publication/DBM/package/` |
| `DBM_OUTPUT_MODE` | Publication output mode for the run | `FULL_ENGINEERING_DBM` | `FULL_ENGINEERING_DBM`, `DBM_DIGEST` |
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
  - `tools/publication/validate_source_supersession.py` (when a supersession map is admitted)
- The `allowed-tools` frontmatter field is authoritative for this skill and enforces that deterministic tool boundary under `TASK`.

Disallowed behavior:
- No dispatching other workers.
- No rewriting of section body prose except for package-level readiness summaries.
- No mutation of KTY-local truth or section-planning artifacts.

## Outputs

The skill writes package-level review artifacts under the immutable package snapshot selected for the run:
- `Rewritten_DBM.md`
- `Trace_Appendix.md`
- `Publication_Manifest.md`
- `Publication_QA.md`
- `Publication_Knowledge_Coverage.md`
- `Publication_Open_Items.md`
- `Publication_Content_Adequacy.md` (required when `DBM_OUTPUT_MODE = FULL_ENGINEERING_DBM`)
- `Publication_Readiness.md`
- `Rerun_Recommendations.csv`
- `Source_Supersession_Report.md` (when source/reference-fidelity validation is run)
- `Source_Supersession_Findings.csv` (when source/reference-fidelity validation is run)

### `Publication_Open_Items.md` minimum structure

`Publication_Open_Items.md` must contain these tables, even when no rows are found:
- `Human Authority Rulings`
- `Engineering TBDs`
- `Decomposition Gaps`

Each table row must include at least:
- `KTY`
- `Conflict/OpenIssue ID`
- `Short Description`
- `Publication Section`
- `Publication Treatment`
- `Required Resolution Owner`
- `Status`

If no rows are found for a table, include `No open items found in mapped active KTYs as of <run date>` and cite the scan inputs used. Do not infer closure from decomposition summary counts alone.

### `Publication_Content_Adequacy.md` minimum structure

Required when `DBM_OUTPUT_MODE = FULL_ENGINEERING_DBM`. Optional when `DBM_OUTPUT_MODE = DBM_DIGEST`.

The package gate assembles this record from section QA outputs, optional deterministic content-profile smoke-test signals when available, and direct package review. Section workers provide section QA inputs; they do not author this package artifact from scratch.

Required sections:

1. `Package Verdict`
   - `AdequacyVerdict`: `PASS`, `PASS_WITH_NOTES`, or `BLOCKED`
   - `DBMOutputMode`
   - `BlockingFindingCount`
   - short blocker list, if any
2. `Section Adequacy Matrix`
   - `SectionID`
   - `SectionTitle`
   - `CoreBasisStandalone`: `YES` or `NO`
   - `DBMNativeStructure`: `YES` or `NO`
   - `SourceDBMGeometry`: `PRESERVED`, `INTENTIONALLY_REDESIGNED`, `NOT_AVAILABLE`, or `FAIL`
   - `DesignBasisTablesHandled`: `INCLUDED`, `CONSOLIDATED`, `SPLIT`, `OMITTED_WITH_RATIONALE`, `DEFERRED_UPSTREAM_MISSING`, or `NONE_APPLICABLE`
   - `PrimaryKTYsMateriallyUsed`: `YES` or `NO`
   - `QAScaffoldLeakage`: `NONE`, `WARNING`, or `BLOCKER`
   - `UnderdevelopedSection`: `NO` or `YES`
   - `SectionVerdict`: `PASS`, `PASS_WITH_NOTES`, or `BLOCKED`
3. `Table Treatment Summary`
   - design-basis tables only; exclude trace, index, provenance, and reference tables
   - summarize included, consolidated/redesigned, omitted with rationale, and deferred because upstream truth is missing
4. `Blockers`
   - fixed finding-code list only: `UNDERDEVELOPED_SECTION`, `UNJUSTIFIED_TABLE_OMISSION`, `PRIMARY_KTY_COLLAPSED`, `MISSING_DESIGN_BASIS_CLASS`, `QA_SCAFFOLD_BODY_LEAKAGE`, `NON_STANDALONE_CORE_BASIS`, `DIGEST_MODE_USED_FOR_FULL_DBM`
5. `Human Review Notes`
   - only issues requiring human judgment; no general commentary or duplicate QA narrative

## Required readiness classification

- `READY`
- `READY_WITH_MAJOR_NOTES`
- `BLOCKED`

## Non-negotiable constraints

- Deterministic completeness/trace checks belong in `assemble_publication.py`, not inline in the skill.
- Package publication always assembles from the full current section set, even when only a subset of sections was rerun.
- `FULL_ENGINEERING_DBM` mode requires `Publication_Content_Adequacy.md`; the package cannot be `READY` without a `PASS` or `PASS_WITH_NOTES` adequacy verdict.
- `DBM_DIGEST` cannot satisfy full-DBM readiness unless the human explicitly selected digest mode and the package is not being accepted as a governing full DBM.
- The skill may judge readiness, but final acceptance remains human-owned.

## Hypergraph QA integration

When `HYPERGRAPH_USE_MODE` includes QA (`AUXILIARY_QA` or `AUXILIARY_PLANNING_AND_QA`) and the admitted hypergraph snapshot is available, the skill performs a package-level hypergraph QA sub-check as part of readiness classification.

### Finding classification

Hypergraph QA findings use their own classification:
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
- whether source/reference-fidelity validation was run,
- total source/reference-fidelity assertions checked,
- total matched by supersession bindings,
- total unexplained reference divergences,
- the blocking/non-blocking classification of source/reference-fidelity findings.

### Guard rails

- A `BLOCKED` `HYPERGRAPH_QA_VERDICT` must prevent hypergraph QA sub-checks from running. The package summary must note that hypergraph QA was skipped due to blocked snapshot quality.
- Hypergraph QA findings must appear in a dedicated section of `Publication_QA.md`.

## Method

1. **Validate package inputs.** Confirm required planning artifacts, section root, and package root exist and are within the approved publication tool root.
2. **Invoke deterministic assembly.** Run `assemble_publication.py`. Assembly must produce the DBM body, trace appendix, package manifest, package QA, deterministic knowledge coverage appendix, and deterministic open-items inventory.
3. **Handle assembly failure conservatively.** If assembly exits non-zero, emit `BLOCKED` and record the tool failure.
4. **Invoke deterministic source/reference-fidelity validation (when admitted).** When a `Supersession_Map.csv` is frozen in the publication manifest, run `validate_source_supersession.py`. This tool compares source-fidelity-critical values against admitted reference/provenance material, allows divergence when accepted DOMAIN/SCA state or the active supersession map explains the current basis, and emits findings consumable by readiness classification.
5. **Run optional hypergraph QA sub-check.** When `HYPERGRAPH_USE_MODE` includes QA and `HYPERGRAPH_QA_VERDICT != BLOCKED`, perform the package-level hypergraph QA checks defined in the Hypergraph QA integration section. Classify findings as `HYPERGRAPH_QA_WARNING` or `HYPERGRAPH_QA_BLOCKER`. Skip this step entirely when `HYPERGRAPH_USE_MODE = NONE` or `HYPERGRAPH_QA_VERDICT = BLOCKED`.
8. **Read the assembled DBM and all section QA artifacts.** Assess whether each section reads as coherent engineering prose under `Publication_Rules.md` rather than an artifact dump.
9. **Run DBM content adequacy review when `DBM_OUTPUT_MODE = FULL_ENGINEERING_DBM`.** Assemble `Publication_Content_Adequacy.md` from section QA `Design Basis Content Coverage`, `Table Treatment`, and `Section Adequacy Findings`; optional deterministic content-profile smoke-test signals when available; and direct review of `Rewritten_DBM.md`. Use the fixed schema above. Treat quantitative signals as anomaly flags, not as the adequacy definition.
10. **Validate open-item inventory.** Confirm `Publication_Open_Items.md` contains the required three tables and row fields. Cross-check section QA gap/conflict registers and mapped active KTY scan evidence where available. If unresolved items were flattened to confirmed prose, classify the package as `BLOCKED` and recommend targeted section reruns.
11. **Aggregate material QA signals.** At minimum summarize:
   - total conflicts,
   - total `TBD` / assumption / deferred-confirmation items,
   - total human authority rulings, engineering TBDs, and decomposition/publication gaps from `Publication_Open_Items.md`,
   - total skipped inputs,
   - total `PRIMARY` KTYs with zero material body contribution from `Publication_Knowledge_Coverage.md`,
   - total content-adequacy blockers by fixed finding code,
   - total material terminology normalizations,
   - total `HYPERGRAPH_QA_WARNING` and `HYPERGRAPH_QA_BLOCKER` findings (when hypergraph QA was run).
10. **Classify readiness.**
   - `BLOCKED` if required sections are missing, deterministic assembly failed, unexplained source/reference-fidelity divergences exist, any `FULL_ENGINEERING_DBM` content-adequacy blocker exists (`UNDERDEVELOPED_SECTION`, `UNJUSTIFIED_TABLE_OMISSION`, `PRIMARY_KTY_COLLAPSED`, `MISSING_DESIGN_BASIS_CLASS`, `QA_SCAFFOLD_BODY_LEAKAGE`, `NON_STANDALONE_CORE_BASIS`, or `DIGEST_MODE_USED_FOR_FULL_DBM`), or `HYPERGRAPH_QA_BLOCKER` findings exist when `HYPERGRAPH_QA_BINDING_POLICY = BLOCK_ON_BINDING_FAILURE`.
   - `READY_WITH_MAJOR_NOTES` if no blocking condition remains but `HYPERGRAPH_QA_WARNING` findings, `PRIMARY` KTY coverage gaps, or other material quality/QA issues remain. A `PRIMARY` KTY with zero material body contribution is a `COVERAGE_GAP` finding by default; it is non-blocking unless the human/controller escalates it.
   - `READY` only if deterministic assembly passes and no unresolved hypergraph QA findings of any severity remain (when hypergraph QA was run).

Post-authoring concordance review is handled separately by `TASK + dbm-postauthor-concordance` after this skill completes. That skill's candidate findings are dispositioned by the human via `Publication_Review_Disposition.csv` and do not feed into this skill's readiness classification.

11. **Emit package review artifacts.** Write `Publication_Content_Adequacy.md` when required, `Publication_Readiness.md`, and `Rerun_Recommendations.csv`.

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
