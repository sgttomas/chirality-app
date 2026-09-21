# dbm-publisher procedure

WORKING_ITEMS coordinates this procedure and assigns bounded visual or semantic stages to TASK. Tool commands resolve against the declared tool root.

### Gate 1 — Intake, Authority Confirmation, and Frozen Input Manifest

**Human provides:** One accepted DOMAIN execution root and publication intent.

**Agent does:**

1. Confirm that the requested run is **one execution root -> one rewritten DBM**.
2. Confirm `DBM_OUTPUT_MODE`. Default to `FULL_ENGINEERING_DBM` unless the human explicitly selects `DBM_DIGEST`. If `DBM_DIGEST` is selected, record that digest mode is not the default governing full-DBM publication output and requires explicit human selection.
3. Read the execution root's authoritative decomposition and scope-change pointers.
4. Confirm the active `_ScopeChange/_LATEST.md` pointer and the active snapshot directory.
5. **Publication reset / abandoned-run check.** Inspect existing `{PUBLICATION_ROOT}/_Planning/`, `{PUBLICATION_ROOT}/dispatch/`, `{PUBLICATION_ROOT}/sections/`, `{PACKAGE_ROOT}/_LATEST.md`, and prior package snapshots for abandoned, rejected, superseded, or quality-limited runs. Before writing or reusing any publication artifact, bring the finding to the human at Gate 1 and obtain an explicit decision:
   - `CLEAN_RESTART`: regenerate `_Planning`, `dispatch`, `sections`, and `package` artifacts from the current authoritative root state; prior publication outputs may be cited only as audit/history and must not seed the new run.
   - `TARGETED_RERUN`: allowed only when the human explicitly identifies the accepted baseline package and the bounded section/package scope to reuse; otherwise default to `CLEAN_RESTART`.
   Record the decision and rationale in `Publication_Input_Manifest.md`. Do not defer this decision past Gate 1.
6. Identify and freeze exact publication inputs in `Publication_Input_Manifest.md`:
   - `DBM_OUTPUT_MODE` and the selection basis (`DEFAULT_FULL_ENGINEERING_DBM` or explicit human-selected `DBM_DIGEST`),
   - exact decomposition files,
   - exact `_Sources` DBM/TOC files admitted as reference/provenance only,
   - exact scope-change pointers/snapshot directories,
   - exact active `Handoff_State.md`,
   - latest `audit-decomp` pointer and admitted audit snapshot / verdict,
   - exact vocabulary, open-issues, decision-log, scope-boundary, and telemetry files when present,
   - explicitly banned authority inputs.
   - active cumulative `Supersession_Map.csv` from the `_ScopeChange/_LATEST.md` snapshot, when present. When the active scope-change snapshot contains this file, freezing it into the manifest is mandatory. This map records accepted SCA incorporation/supersession of prior or reference facts and is consumed by the ConflictPrecedence rule and source/reference-fidelity validator.
   **Path format:** All paths in the manifest must resolve correctly when treated as relative to the `_Planning/` directory — this is `markdown_path.parent` for `build_section_map.py`'s `_resolve_manifest_path` function. Use `../../..` for `EXECUTION_ROOT` (three levels up from `_Planning/` to the domain root), `..` for `PUBLICATION_ROOT` (one level up to `DBM/`), and `../../../` prefix for paths within the execution root. For paths outside the execution root (e.g., shared reference/provenance files in a sibling domain), count the relative traversal from `_Planning/`. Do not use `{PLACEHOLDER}` variable substitution — the tool does not expand placeholders.
7. Evaluate the publication-admission basis from the active scope-change closure artifacts. A root is publication-admissible only when the active `Handoff_State.md` supports publication-phase consumption and the latest audit evidence is non-blocking.
8. Surface any missing mandatory input, ambiguous path, disputed input-authority classification, abandoned-run reuse ambiguity, or failed publication-admission condition. If the root is not publication-admissible, stop and ask the human to repair or explicitly override the upstream closure state before publication begins.
9. **Hypergraph discovery.** Check whether `{EXECUTION_ROOT}/_Aggregation/Hypergraph/` contains one or more snapshot directories. If a snapshot exists:
   - read its `_LATEST.md` pointer (if present) to identify the most recent snapshot,
   - read the snapshot's `RUN_SUMMARY.md` and `QA_Report.md` to determine the QA verdict,
   - present the finding to the human with a recommended `HYPERGRAPH_USE_MODE`:
     - if QA is non-blocking: recommend `AUXILIARY_PLANNING_AND_QA`,
     - if QA has blockers: recommend `AUXILIARY_PLANNING` (advisory only) or `NONE`,
     - if no snapshot exists: recommend `NONE` and note the absence.
   The human decides the use mode. Do not silently default to `NONE` when a usable snapshot is available.
10. When the chosen `HYPERGRAPH_USE_MODE != NONE`, freeze the following in the manifest before approval:
   - exact `HYPERGRAPH_SNAPSHOT_PATH`
   - exact `HYPERGRAPH_RUN_SUMMARY_PATH`
   - exact `HYPERGRAPH_QA_REPORT_PATH`
   - chosen `HYPERGRAPH_USE_MODE`
   - `HYPERGRAPH_QA_VERDICT` (`NON_BLOCKING`, `BLOCKED`, or `NOT_USED`)
   - `HYPERGRAPH_LIMITATIONS` (free-text list of known defects that constrain allowed use)
   The manifest must explicitly distinguish three authority roles: `content authority`, `admission / closure evidence`, and `auxiliary structure evidence`. Hypergraph evidence falls exclusively into auxiliary structure evidence.
11. The frozen input manifest locks the authoritative content-input set, publication-admission basis, and DBM output mode before derivative work begins. No section synthesis or package assembly may proceed until this manifest is approved.
12. Present the frozen input manifest to the human and ask: **"Approve this publication input set, DBM output mode, and admission basis?"**

**Human approves** or requests corrections.

If the manifest is not approved, do not continue.

---

### Gate 2 — Knowledge-Landscape Review Before Schema Design

**Agent does:**

Using only the frozen input manifest:

1. Read the category register and present category inventory with KTY counts and unit totals.
2. Read the KTY register and present knowledge types grouped by canonical schema / artifact type.
3. Read the objective register and summarize objective alignment.
4. Read active scope-change state and identify active, superseded, or retired areas where status is explicit.
5. Read subject and open-issues registers to identify recurring technical states, repeated parameters, and probable section-load hotspots.
6. Flag any candidate section that appears likely to exceed approved size limits.
7. When `HYPERGRAPH_USE_MODE` includes planning (`AUXILIARY_PLANNING` or `AUXILIARY_PLANNING_AND_QA`), perform an optional hypergraph-assisted landscape review:
   - use node/edge counts to identify dense KTY clusters,
   - use `KTY_SUPPORTS_OBJ` edges to identify objective-centered hubs,
   - use subject/artifact adjacency to detect likely section-load hotspots,
   - use ledger coverage in the hypergraph to identify unusually broad KTYs.
   All hypergraph-derived observations in the Gate 2 summary must be labeled `AUXILIARY_STRUCTURE_EVIDENCE`.
8. Produce a readable human-facing review summary under the publication tool root.

Ask the human: **"Does this landscape review support the target DBM structure you want?"**

**Human approves** the review baseline or redirects emphasis.

---

### Gate 3 — Publication Schema and Publication Rules Freeze

**Agent does:**

1. Draft `Publication_Schema.md` with both:
   - human-readable section intent (`InclusionRule`, `ExclusionRule`), and
   - machine-readable selector fields for deterministic mapping.
2. Ensure every section row includes at least:
   - `SectionID`, `SectionOrder`, `SectionTitle`, `SectionType`, `SectionPurpose`,
   - selector fields,
   - `ExpectedInputs`, `ExpectedOutputShape`, `ExpectedBodyComponents`, `ExpectedDesignBasisTables`, `SourceDBMGeometry`, `AdequacyRisks`,
   - `MaxKAFiles`, `MaxEstimatedTokens`, `ComplexityClass`, `SplitTrigger`, `SplitHint`.
3. Draft `Publication_Rules.md` and freeze publication behavior for:
   - `DBM_OUTPUT_MODE` (`FULL_ENGINEERING_DBM` by default; `DBM_DIGEST` only by explicit human selection),
   - voice and tone,
   - heading style,
   - facility naming,
   - body completeness standard,
   - tabular data policy,
   - trace vs engineering detail,
   - body vs QA artifact boundary,
   - standalone body usability,
   - section underdevelopment policy,
   - digest output prohibition when `DBM_OUTPUT_MODE = FULL_ENGINEERING_DBM`,
   - traceability mode,
   - conflict precedence,
   - amendment note behavior,
   - `TBD` handling,
   - terminology control,
   - large-section handling,
   - open-issue flattening behavior,
   - epistemic label flattening,
   - supersession body-note heuristic,
   - coverage expectation by mapping role.
4. Require schema design to evaluate whether any section is too broad for a full DBM treatment. Split or subdivide sections before approval when a section maps many systems, KTYs, design cases, or design-basis tables that cannot be represented as a coherent DBM-native section.
5. Explicitly include the `OVERVIEW` section type in the section taxonomy.
6. Run governed sizing before asking for approval:
   - `build_section_map.py --dry-run --schema {draft_schema} --manifest {frozen_manifest} --report-md {PLANNING_ROOT}/Draft_Section_Map_Coverage.md`.
   - Review KA counts, estimated tokens, KTY counts, SCA ref counts, open issue counts, lifecycle findings, and split-pressure signals.
   - Split sections, refine selectors, or adjust measurable limits before human approval when sizing indicates high split pressure.
7. Surface any selector/prose divergence risk before mapping begins.

Ask the human: **"Approve the target publication schema and publication rules?"**

**Human approves** or edits.

No mapping or synthesis begins before approval.

---

### Gate 4 — Section Map Freeze

**Agent does:**

1. Run or consume the candidate output from `build_section_map.py` using the approved schema and frozen input manifest.
2. Review candidate mapping coverage, duplicates, selector/prose divergence, lifecycle findings, retired/tombstone mapping findings, and section-load warnings.
3. Draft the human-approved `Section_Map.csv` with mapping rows and explicit `MappingRole` / `ContributionScope` semantics.
4. When `HYPERGRAPH_USE_MODE` includes planning (`AUXILIARY_PLANNING` or `AUXILIARY_PLANNING_AND_QA`), perform optional hypergraph-assisted section-map support:
   - use adjacency to suggest likely multi-KTY section clusters,
   - use repeated objective/KTY participation to suggest authority sections for recurring technical states,
   - use subject/artifact relationships to identify omitted participant sections.
   Hypergraph structure alone must not be used to create a section mapping that contradicts the approved decomposition and mapped KTY-local inputs. All hypergraph-derived suggestions remain advisory until human approval.
5. Run `build_section_context_packets.py` against the frozen manifest, approved schema, approved section map, admitted supersession map when present, and open issues register when present. Write deterministic, inspectable packets under `{SECTION_CONTEXT_ROOT}`. These packets become controlled read-only structural context inputs for section workers and do not require a separate human approval gate.
6. Perform and record the open-item scan required by the Open-Item Surfacing Standard for the candidate/final mapped section set. Resolve the findings into section-level `OpenItemPacket` content or package-level limitations before section dispatch; do not treat retired, tombstoned, archived-stubbed, or no-factual-use KTYs as active body inputs.
7. Present the final section map, context packet/open-item outputs for review, surfacing only targeted unresolved questions.

Ask the human: **"Approve the final section map?"**

**Human approves** or revises.

The approved `Section_Map.csv` becomes the run authority.

---

### Gate 5 — Dispatch Brief Freeze and Section Synthesis

**Agent does:**

1. Render deterministic INIT-TASK briefs for:
   - each approved section (`TASK + dbm-section-publish`), and
   - the package run (`TASK + dbm-publish`).
2. Ensure briefs conform to `docs/AGENT_WORKFLOW_RUNTIME.md` and the target workflow `CONTRACT.md#brief`. Each section brief must include `RuntimeOverrides.SECTION_CONTEXT_PATH` when the corresponding `{SECTION_CONTEXT_ROOT}/SEC-##_Context.md` packet exists.
3. Ensure each section and package brief includes `RuntimeOverrides.DBM_OUTPUT_MODE`; omit it only when the brief explicitly relies on the default `FULL_ENGINEERING_DBM`.
4. Ensure each section brief includes the approved body completeness standard, expected body components, expected design-basis tables/data classes, section-specific adequacy risks, source DBM geometry treatment (`PRESERVED`, `INTENTIONALLY_REDESIGNED`, or `NOT_AVAILABLE`), and the instruction that body brevity is acceptable only when mapped source material is genuinely sparse.
5. Ensure each section brief explicitly prohibits using mapped-assertion lists, controlled-assertion registers, raw caveat dumps, path inventories, or trace scaffolds as the main body structure in `FULL_ENGINEERING_DBM` mode.
6. Ensure each section brief includes an `OpenItemPacket` or equivalent brief block for section-relevant human rulings, engineering TBDs, and decomposition/publication gaps. If the scan found none, state that explicitly with the scan inputs used.
7. Pre-create section output directories.
8. Dispatch `TASK + dbm-section-publish` once per approved section.
9. Review section outputs for:
   - body readability,
   - QA completeness,
   - DBM content adequacy against the section QA `Design Basis Content Coverage` and `Table Treatment` records,
   - open-item treatment completeness,
   - `UNDERDEVELOPED_SECTION`, `UNJUSTIFIED_TABLE_OMISSION`, `PRIMARY_KTY_COLLAPSED`, `MISSING_DESIGN_BASIS_CLASS`, or `QA_SCAFFOLD_BODY_LEAKAGE` findings,
   - oversized or failed sections.
10. If a section fails with `FAILED_INPUTS`, stop that section path and push the issue back to schema/map/rules refinement rather than improvising a workaround.

Ask the human: **"Proceed with package publication using the current section set?"** only when every required section has one current output bundle ready for assembly.

**Human approves** package publication or requests section reruns/edits.

---

### Gate 6 — Package Assembly and Post-Authoring Evidence Bundle Review

**Agent does:**

1. Dispatch `TASK + dbm-publish` to create the package snapshot and run deterministic assembly, source/reference-fidelity validation when admitted, and package QA outputs (`Publication_Knowledge_Coverage.md`, `Publication_Open_Items.md`, `Publication_Content_Adequacy.md` when `FULL_ENGINEERING_DBM`, `Publication_Readiness.md`, `Rerun_Recommendations.csv`).
2. **Build post-authoring evidence bundle.** Run the shared review-substrate tools against the assembled `Rewritten_DBM.md`:
   - `scan_section_coverage.py` with `--section-map` (run-specific authority),
   - `extract_claims.py` (value/parameter/term extraction),
   - `scan_tbd_markers.py` with KB cross-reference,
   - `check_body_thinness.py` with `--section-map` and `--schema`.
3. **Dispatch `TASK + dbm-postauthor-concordance`** against the package snapshot with the substrate outputs. This workflow reads the substrate alongside governed truth (section map, KA artifacts, publication rules, open items, supersession state) and uses engineering judgment to prepare candidate findings for human disposition. It writes the evidence bundle (6 files) and `Publication_Review_Disposition.csv` with `HumanDisposition = TBD` for all rows.
4. **Optionally dispatch `TASK + dbm-concordance-verify`** for semantic cross-section consistency review. This is an observation-only review that produces semantic consistency observations for the reviewing agent/human — it does not produce automatic readiness verdicts or blocking decisions.
5. When `HYPERGRAPH_USE_MODE` includes QA (`AUXILIARY_QA` or `AUXILIARY_PLANNING_AND_QA`), perform optional package-level hypergraph QA:
   - verify all section-mapped KTYs appear in the admitted hypergraph,
   - detect any major connected cluster implied by the section map that is silently absent from the section set,
   - flag orphaned or weakly represented structural clusters.
   Hypergraph QA observations are advisory and feed into the evidence bundle review, not automatic gates.
6. Present the evidence bundle, candidate findings, and `Publication_Review_Disposition.csv` to the human. The human reviews and fills `HumanDisposition` for each finding. Readiness is a human judgment informed by the evidence bundle, not an automatic gate.
7. If the human requests revisions, identify targeted reruns and return to Gate 5 for only the affected sections.

Ask the human: **"Do you accept this package for publication, request targeted reruns, or reopen the planning artifacts?"**

**Human accepts** or requests another loop.

---

### Gate 7 — Acceptance, Pointer Update, and change Handoff

**Agent does:**

1. If the human accepts the package snapshot, confirm the accepted run snapshot under `{PACKAGE_ROOT}/RUN-YYYYMMDD-HHMMSS/`.
2. Write `Publication_Handoff_State.md` into the accepted package snapshot with at least:
   - accepted execution root,
   - admitted active scope-change snapshot,
   - exact `Publication_Input_Manifest.md` path,
   - `DBM_OUTPUT_MODE`,
   - section-set status,
   - post-authoring review status,
   - content adequacy status when `DBM_OUTPUT_MODE = FULL_ENGINEERING_DBM`,
   - admitted hypergraph evidence status when used,
   - publication readiness verdict,
   - remaining blockers / limits,
   - next owning workflow.
3. Update `{PACKAGE_ROOT}/_LATEST.md` to point to the accepted snapshot only after `Publication_Handoff_State.md` exists.
4. Record acceptance notes and any publication limits that remain.
5. Prepare a change handoff package with:
   - accepted file list,
   - recommended commit message,
   - any human notes on publication approval.

Ask the human: **"Hand off these accepted publication artifacts to change?"**

**Human approves** or stops after local acceptance.
