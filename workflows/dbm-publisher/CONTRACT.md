# dbm-publisher contract

## Runtime variables and defaults

This file is **execution-root generic**. Do not embed project-specific absolute paths.

Defaults (only when not otherwise specified by the human):
- `EXECUTION_ROOT` = required; one accepted DOMAIN execution root
- `PUBLICATION_ROOT = {EXECUTION_ROOT}/_Publication/DBM/`
- `PLANNING_ROOT = {PUBLICATION_ROOT}/_Planning/`
- `DISPATCH_ROOT = {PUBLICATION_ROOT}/dispatch/`
- `SECTIONS_ROOT = {PUBLICATION_ROOT}/sections/`
- `PACKAGE_ROOT = {PUBLICATION_ROOT}/package/`
- `PACKAGE_LATEST = {PACKAGE_ROOT}/_LATEST.md`
- `INPUT_MANIFEST_PATH = {PLANNING_ROOT}/Publication_Input_Manifest.md`
- `PUBLICATION_SCHEMA_PATH = {PLANNING_ROOT}/Publication_Schema.md`
- `SECTION_MAP_PATH = {PLANNING_ROOT}/Section_Map.csv`
- `PUBLICATION_RULES_PATH = {PLANNING_ROOT}/Publication_Rules.md`
- `SECTION_CONTEXT_ROOT = {PLANNING_ROOT}/section-context/`
- `SECTION_DISPATCH_INDEX = {DISPATCH_ROOT}/DISPATCH_INDEX.csv`
- `POSTAUTHOR_REVIEW_WORKFLOW = dbm-postauthor-concordance`
- `CONCORDANCE_VERIFY_WORKFLOW = dbm-concordance-verify` *(optional; semantic cross-section consistency review)*
- `SECTION_WORKFLOW = dbm-section-publish`
- `PACKAGE_WORKFLOW = dbm-publish`
- `SECTION_MAP_TOOL = tools/publication/build_section_map.py`
- `SECTION_CONTEXT_TOOL = tools/publication/build_section_context_packets.py`
- `REVIEW_SECTION_COVERAGE_TOOL = tools/review/scan_section_coverage.py`
- `REVIEW_CLAIMS_TOOL = tools/review/extract_claims.py`
- `REVIEW_TBD_TOOL = tools/review/scan_tbd_markers.py`
- `REVIEW_THINNESS_TOOL = tools/review/check_body_thinness.py`
- `DISPATCH_RENDER_TOOL = tools/publication/render_dispatch_briefs.py`
- `V1_SCOPE = one execution root -> one rewritten DBM`
- `DBM_OUTPUT_MODE = FULL_ENGINEERING_DBM`
- `TRACEABILITY_MODE = appendix-only`
- `CURRENT_STATE_BASIS = publication-admitted current-state root package`
- `HYPERGRAPH_USE_MODE = NONE`
- `HYPERGRAPH_SNAPSHOT_PATH = optional`
- `HYPERGRAPH_RUN_SUMMARY_PATH = optional`
- `HYPERGRAPH_QA_REPORT_PATH = optional`
- `HYPERGRAPH_NODES_PATH = optional`
- `HYPERGRAPH_HYPEREDGES_PATH = optional`
- `HYPERGRAPH_EVIDENCE_ROOT = optional`

Non-authoritative by default (must remain excluded unless the human explicitly promotes them for the run):
- `{EXECUTION_ROOT}/_Aggregation/*` — remains non-authoritative for section prose by default. Exception: a frozen hypergraph snapshot under `_Aggregation/Hypergraph/` may be consumed as auxiliary structure evidence when explicitly admitted in the frozen publication manifest via `HYPERGRAPH_USE_MODE != NONE`. Even when admitted, hypergraph evidence is auxiliary structure evidence only and does not become content authority for section prose.
- `{EXECUTION_ROOT}/_Coordination/*`
- `{EXECUTION_ROOT}/_Evaluation/*`
- `{EXECUTION_ROOT}/_Reconciliation/*`
- `*_MEMORY.md` — not factual authority, but whenever an agent reads a KTY `_STATUS.md`, it must also read sibling `_MEMORY.md` when present as non-authoritative operational context.
- `*_SEMANTIC.md`

---

## Publication requirements

- **One execution root -> one rewritten DBM in v1.** Cross-domain consolidated publication is out of scope unless the human explicitly expands the architecture later.
- **Full engineering DBM is the default output.** `DBM_OUTPUT_MODE` defaults to `FULL_ENGINEERING_DBM`. `DBM_DIGEST` is an explicit opt-in mode only and must not be treated as the governing DBM output unless the human selects digest mode in Gate 1 and records that decision in the manifest and publication rules.
- **Gate-controlled publication.** No planning artifact, section map, package snapshot, or accepted pointer becomes authoritative without the defined human gate.
- **Tool-root-only writes.** dbm-publisher writes only under `{EXECUTION_ROOT}/_Publication/DBM/`.
- **Frozen input set required.** Publication begins only after `Publication_Input_Manifest.md` freezes the exact decomposition, scope-change, mapped content, reference/provenance, and publication-admission evidence inputs for the run.
- **Publication admission is root-closure-gated.** Gate 1 must confirm that the active root `Handoff_State.md` and latest audit evidence support publication-phase consumption before any section synthesis begins.
- **Explicit authority stack.** Publication authority is: approved publication schema → approved publication rules → approved section map → approved merged decomposition state → accepted SCA state → mapped CAT/KTY/KA-local content. Reference/provenance inputs are not publication authority unless incorporated through accepted DOMAIN/SCA state.
- **Current-state publication.** The published DBM presents the publication-admitted current-state root package as the design basis. Superseded state may appear only as amendment, trace, or QA context.
- **Selector/prose split is explicit.** `build_section_map.py` consumes machine-readable selector fields only. Human-readable prose does not drive deterministic mapping.
- **Approved `Section_Map.csv` is run authority.** Candidate mappings are advisory until the human approves the final section map.
- **No orchestration-through-workflow.** `dbm-publish` is a bounded package assembly workflow. It never dispatches other workers.
- **Post-authoring evidence bundle, not pre-authoring concordance gate.** Concordance review happens *after* section authoring, not before. Deterministic tools prepare review substrate (structural coverage, extracted claims, TBD markers, body-thinness signals). Agentic workflows read the substrate alongside governed truth and use engineering judgment to prepare candidate findings. The human dispositions findings. This model replaces the prior pre-authoring concordance register freeze.
- **Evidence bundle is not a quality gate.** Hard gates are limited to process validity (inputs exist, tools ran, schemas valid, provenance present). Engineering judgment about materiality, adequacy, and significance stays with the reviewing agent and human. No tool or workflow produces automatic readiness verdicts or blocking decisions.
- **Three-layer review model.** Tools produce review substrate (factual, non-judgmental). Workflows produce candidate findings (agent judgment with evidence). Humans produce dispositions (accept, revise, waive, defer). No layer may bypass the one above it.
- **DBM body completeness is a publication gate.** In `FULL_ENGINEERING_DBM` mode, the DBM body must be adequate as a governing engineering design-basis document. Body completeness is equal in importance to traceability, post-authoring review, source/reference-fidelity, and open-item surfacing.
- **Open-item surfacing is agent-owned.** Unresolved human rulings, engineering TBDs, and decomposition/publication gaps must be actively surfaced by dbm-publisher during planning, section dispatch, and package review. They must not be buried only in worker QA, smoothed into confident design-basis prose, or inferred closed from decomposition summary counts.
- **Retired/no-factual-use content is not active publication content.** Retired, tombstoned, archived-stubbed, or no-factual-use KTYs must not be dispatched as active section body inputs. If they affect section structure, provenance, or reader risk, surface them as publication limitations or decomposition/publication gaps.
- **No invention.** Missing or unsupported content becomes `TBD`, an explicit assumption, or an exposed conflict. Nothing is guessed into the DBM body.
- **Engineering prose standard.** The published DBM must read as though written by a senior engineer authoring a governing facility document — the same register used to write codes, standards, and design basis memoranda. Every sentence must be technically precise, terminologically consistent, and structurally complete. Conciseness is required, but never at the cost of omitting a material design-basis statement. The prose must be authoritative and definitive, not hedged or conversational. Parallel structure, consistent units, and unambiguous antecedents are not stylistic preferences — they are correctness requirements. Section bodies must never read as stitched artifact dumps, paraphrased source extracts, or chatbot summaries.
- **Detailed traceability stays out of body prose.** Reference/provenance-level detail belongs in the trace appendix and section QA artifacts, not inline in the rewritten DBM body. This rule removes provenance clutter from the body; it does not remove design-basis values, capacities, operating limits, equipment configuration, interfaces, assumptions, TBDs, design constraints, or design-basis tables from the body.
- **Oversized sections fail fast.** If section input volume exceeds approved limits, the section design must be split or refined rather than forced through synthesis.
- **Package publication always re-checks the full current section set.** A targeted section rerun does not permit partial package assembly or partial post-authoring review.
- **Abandoned publication runs cannot seed new runs.** If the human abandons, rejects, or supersedes a publication run for quality or authority reasons, the next Gate 1 start must surface that status explicitly and regenerate `_Planning`, `dispatch`, `sections`, and `package` artifacts for the new run rather than reusing prior publication outputs as working authority.
- **Final acceptance remains human-owned.** dbm-publisher may recommend readiness; only the human accepts the package and authorizes pointer/CHANGE handoff updates.
- **Derivative publication packages do not replace authoritative decomposition + SCA state.** All publication outputs (`Rewritten_DBM.md`, `Trace_Appendix.md`, `Publication_Manifest.md`, etc.) are derived publication artifacts. They do not amend, supersede, or substitute for the canonical working package (decomposition truth, authoritative companion registers, and accepted `_ScopeChange` state) in the upstream root.
- **Hypergraph outputs are auxiliary structure evidence only.** Admitted hypergraph snapshots may inform planning and package-level QA, but they do not author section prose, override decomposition mappings, or replace KTY-local content authority.
- **Blocked hypergraph QA cannot silently power package QA.** If the admitted hypergraph snapshot carries a `BLOCKED` QA verdict, it must not be used for QA or content-adjacent decisions. Package readiness must never depend on a blocked hypergraph passing a QA check it was not qualified to support.
- **Hypergraph evidence supports post-authoring review but does not replace agent judgment.** Hypergraph-derived observations are advisory inputs to the post-authoring evidence bundle review. They do not produce automatic findings or blocking decisions.

---

## Publication Input Classes and Output Policy

Every file frozen into the manifest or consumed during publication must be assigned to exactly one input class. dbm-publisher may ingest more structure than it publishes: structure should shape schema design, mapping, completeness checks, and QA, while `Rewritten_DBM.md` remains a conventional current-state engineering DBM body plus rich package records.

| Class | Ingestion | Allowed use | May appear in `Rewritten_DBM.md` | Required package record |
|---|---|---|---|---|
| Body-authoring authority | Frozen in manifest or generated as approved planning authority | Primary basis for current-state section body prose | Yes: current engineering claims, design values, scope statements, and approved overview framing | Trace appendix and section QA |
| Publication-admission evidence | Frozen in manifest; read at Gate 1 and package gates | Admit/block publication and record closure basis | Never | `Publication_Manifest.md`, `Publication_QA.md` |
| Structural context | Frozen in manifest or generated deterministically at Gate 4 | Shape section design, context packets, completeness assessment, and worker framing | Only when expressing real facility intent or scope; never as visible decomposition metadata. `OVERVIEW` may synthesize facility/document framing from accepted objectives and structure | `Publication_Knowledge_Coverage.md`, section context packets |
| Operational caveat context | Read by agent and workers as readiness/QA context | Guide readiness, factual-use eligibility, and gap handling | Only as flattened `TBD`, `to be confirmed`, `assumed`, scope exclusion, or design limit | `Publication_QA.md`, `Publication_Open_Items.md` |

Explicit class assignments:

| Input | Class |
|---|---|
| Approved `Publication_Schema.md`, `Publication_Rules.md`, `Section_Map.csv` | Body-authoring authority |
| Mapped `Scoping.md` and `KA-*.md` | Body-authoring authority |
| `_CONTEXT.md` and `_REFERENCES.md` | Supporting body-authoring context for identity, scope, references, and terminology; they cannot originate unsupported design-basis claims |
| `Vocabulary_Map.csv` | Body-authoring authority for terminology control |
| Reference/provenance markdown, CSVs, and figures | Reference/provenance context only; not body-authoring authority unless incorporated through accepted DOMAIN/SCA state and mapped CAT/KTY/KA content |
| `Supersession_Map.csv` | Accepted SCA state support for explaining current-state incorporation/supersession; SCA process history stays in QA/trace |
| `Decision_Log.csv` | Conflict-resolution support; not direct body-authoring prose |
| `Handoff_State.md`, `RUN_SUMMARY.md`, latest `audit-decomp` pointer/verdict, `KTY_Remediation_Manifest.csv` | Publication-admission evidence |
| Category, KTY, Subject, Objective registers and Domain Ledger | Structural context |
| `Section_Context` packets | Structural context |
| Hypergraph evidence when admitted | Structural context / auxiliary structure evidence |
| `_STATUS.md`, `_MEMORY.md`, `_DEPENDENCIES.md`, `Open_Issues_Register.csv` | Operational caveat context |
| `_MEMORY.md` | Read only when paired with `_STATUS.md`; never factual authority and never a source for body claims |
| `_SEMANTIC.md` | Excluded from publication authority |

The class table is normative. A section worker or package workflow must not silently promote a lower-class input into body-authoring authority. If a run needs a different class assignment, dbm-publisher must surface it as a human decision before section synthesis.

### Open-Item Surfacing Standard

During Gates 1 through 6, dbm-publisher must preserve unresolved governance and engineering uncertainty as first-class publication state.

Before freezing the section map and again before dispatching section workers, scan the mapped active KTY set, the active `_ScopeChange/_LATEST.md` target, SCA handoff state, and KTY remediation/disposition records for:

- **Human authority rulings:** rows in `## Conflict Table (for human ruling)` whose ruling remains `TBD`, pending, open, deferred, or otherwise unresolved. Preserve the conflict ID, KTY, evidence/provenance references, proposed authority, impacted artifacts, and decision needed.
- **Engineering TBDs:** entries in `## Open Questions / TBD`, KTY-carried or reference-carried `TBC` values, `DeferredConfirmation`, `Assumption`, `ExternalResponsibility`, and similar uncertainty. Body prose may flatten these to `TBD`, `to be confirmed`, or `assumed`, but QA/package records must preserve the original governance label and KTY/provenance trail.
- **Decomposition/publication gaps:** cases where the accepted DOMAIN/SCA state, mapped KTY-local content, or reference/provenance inputs imply missing or misaligned publication structure, including absent subjects, voided subjects retained for bijection, retired/tombstoned material with publication risk, reference cross-reference gaps, or reference-table disagreements that cannot be resolved without scope amendment or human ruling.

For each publication section, provide the section worker an `OpenItemPacket` or equivalent brief block containing the section-relevant human rulings, engineering TBDs, and decomposition/publication gaps. The packet is operational caveat context; it does not expand body-authoring authority beyond the approved section map and mapped KTY-local inputs.

At package assembly, `Publication_Open_Items.md` must contain three explicit tables:

1. `Human Authority Rulings`
2. `Engineering TBDs`
3. `Decomposition Gaps`

Each row must include at least `KTY`, `Conflict/OpenIssue ID`, `Short Description`, `Publication Section`, `Publication Treatment`, `Required Resolution Owner`, and `Status`. If no rows are found for a table, include the table with `No open items found in mapped active KTYs as of <run date>` and cite the scan inputs used.

---

## Artifacts and tool interfaces

### Publication tool root

```text
{EXECUTION_ROOT}/_Publication/DBM/
  _Planning/
    Publication_Input_Manifest.md
    Publication_Schema.md
    Section_Map.csv
    Publication_Rules.md
    section-context/
      SEC-01_Context.md
      SEC-02_Context.md
      ...
  dispatch/
    DISPATCH_INDEX.csv
    SEC-01_INIT-TASK.md
    ...
    DBM_PUBLISH_INIT-TASK.md
  sections/
    SEC-01/
      SEC-01.md
      SEC-01_QA.md
    ...
  package/
    RUN-YYYYMMDD-HHMMSS/
      Rewritten_DBM.md
      Trace_Appendix.md
      Publication_Manifest.md
      Publication_QA.md
      Publication_Knowledge_Coverage.md
      Publication_Open_Items.md
      Publication_Content_Adequacy.md
      Publication_Readiness.md
      Publication_Handoff_State.md
      review/
        Evidence_Bundle_Summary.md
        Section_Coverage.csv
        Draft_Claims.csv
        Body_Thinness.csv
        TBD_Inventory.csv
        Candidate_Findings.csv
        Publication_Review_Disposition.csv
      Rerun_Recommendations.csv
    _LATEST.md
```

### Package-role classification of publication outputs

| Artifact | Package role |
|---|---|
| `Publication_Input_Manifest.md` | process record (frozen input set for the run) |
| `Publication_Schema.md` | process record (approved publication design) |
| `Section_Map.csv` | process record (approved run authority) |
| `Publication_Rules.md` | process record (approved publication behavior) |
| `review/Evidence_Bundle_Summary.md` | process record (post-authoring review substrate and findings summary) |
| `review/Candidate_Findings.csv` | process record (agent-prepared findings for human disposition) |
| `review/Publication_Review_Disposition.csv` | process record (human disposition of post-authoring findings) |
| `section-context/SEC-##_Context.md` | process record (deterministic structural context packet) |
| `Rewritten_DBM.md` | **derived publication artifact** |
| `Trace_Appendix.md` | **derived publication artifact** |
| `Publication_Manifest.md` | process record (package provenance) |
| `Publication_QA.md` | process record (package quality assessment) |
| `Publication_Knowledge_Coverage.md` | process record (knowledge coverage assessment) |
| `Publication_Open_Items.md` | process record (open items inventory) |
| `Publication_Content_Adequacy.md` | process record (full-DBM content adequacy gate) |
| `Publication_Readiness.md` | process record (readiness judgment) |
| `Publication_Handoff_State.md` | process record (accepted package closeout / next-workflow handoff) |

None of these outputs are authoritative working surfaces for decomposition amendment. The canonical working package in the upstream execution root remains authoritative.

Rules:
- Package snapshots are immutable.
- `_LATEST.md` is mutable and may point only to a human-accepted package snapshot after `Publication_Handoff_State.md` exists in that snapshot.
- `render_dispatch_briefs.py` pre-creates `sections/SEC-##/` directories so workers write files, not structure.

### `Publication_Input_Manifest.md`

Minimum required sections:
- `EXECUTION_ROOT`
- `PUBLICATION_ROOT`
- `DBM_OUTPUT_MODE`
- `Content Authority`
- `Admission / Closure Evidence`
- exact `_Decomposition` input paths
- exact reference/provenance `_Sources` input paths
- exact scope-change input paths
- exact active `Handoff_State.md` path
- exact latest `audit-decomp` pointer and admitted audit snapshot / verdict
- exact optional authority-supporting inputs (decision log, scope boundary, telemetry, vocabulary map, open issues)
- explicitly banned authority inputs

Optional `Source Supersession` section (required when an active `Supersession_Map.csv` exists in the `_ScopeChange/_LATEST.md` snapshot; omission or malformed fields are a Gate 1 input defect):
- `SUPERSESSION_MAP_PATH` — exact path to the cumulative `Supersession_Map.csv` from the active SCA snapshot
- `FACILITY_ID` — facility identifier for supersession applicability filtering (e.g., `03-25`, `04-25`)

Optional `Auxiliary Structure Evidence` section (required when `HYPERGRAPH_USE_MODE != NONE`):
- `HYPERGRAPH_USE_MODE` — `NONE`, `AUXILIARY_PLANNING`, `AUXILIARY_QA`, or `AUXILIARY_PLANNING_AND_QA`
- `HYPERGRAPH_SNAPSHOT_PATH` — exact path to the admitted hypergraph snapshot
- `HYPERGRAPH_RUN_SUMMARY_PATH` — exact path to the hypergraph run summary
- `HYPERGRAPH_QA_REPORT_PATH` — exact path to the hypergraph QA report
- `HYPERGRAPH_QA_VERDICT` — `NON_BLOCKING`, `BLOCKED`, or `NOT_USED`
- `HYPERGRAPH_LIMITATIONS` — free-text list of known defects constraining allowed use

Required authority-role content:
- `Content Authority` — approved publication schema, approved publication rules, approved decomposition state, accepted SCA state, mapped KTY-local files
- `Admission / Closure Evidence` — active scope-change closure artifacts, active `Handoff_State.md`, latest audit evidence, decision-log entries, open-issues register when needed
- `Auxiliary Structure Evidence` — admitted hypergraph snapshot (when `HYPERGRAPH_USE_MODE != NONE`)

### `Publication_Handoff_State.md`

Minimum required fields:
- `AcceptedPackageSnapshot`
- `AcceptedExecutionRoot`
- `ActiveScopeChangeSnapshot`
- `PublicationInputManifestPath`
- `DBMOutputMode`
- `SectionSetStatus`
- `PostAuthorReviewStatus`
- `ContentAdequacyStatus`
- `HypergraphEvidenceStatus`
- `PublicationReadinessVerdict`
- `RemainingBlockers`
- `NextOwningWorkflow`

### `Publication_Schema.md`

Minimum section table columns:
- `SectionID`
- `SectionOrder`
- `SectionTitle`
- `SectionType`
- `SectionPurpose`
- `InclusionRule`
- `ExclusionRule`
- `IncludeCategoryIDs`
- `IncludeKnowledgeTypeIDs`
- `IncludeCanonicalSchemas`
- `ExcludeCategoryIDs`
- `ExcludeKnowledgeTypeIDs`
- `ExpectedInputs`
- `ExpectedOutputShape`
- `ExpectedBodyComponents`
- `ExpectedDesignBasisTables`
- `SourceDBMGeometry`
- `AdequacyRisks`
- `MaxKAFiles`
- `MaxEstimatedTokens`
- `ComplexityClass`
- `SplitTrigger`
- `SplitHint`

`SectionType` values supported in v1:
- `OVERVIEW`
- `PROCESS_BASIS`
- `PHILOSOPHY`
- `DATA_REFERENCE`
- `DISCIPLINE_BASIS`
- `REGULATORY`

Rules:
- `InclusionRule` and `ExclusionRule` are human-readable only.
- Deterministic tools consume machine-readable selector fields only.
- If selector output diverges from prose intent, the divergence must be surfaced for human resolution.
- If the human edits the candidate mapping directly, the approved `Section_Map.csv` supersedes both selectors and prose for the run.
- **Selector union semantics.** `build_section_map.py` unions `IncludeCategoryIDs`, `IncludeKnowledgeTypeIDs`, and `IncludeCanonicalSchemas` to build each section's match set — it does not intersect them. If a section intends to select only a subset of a category's KTYs, remove that category from `IncludeCategoryIDs` and use `IncludeKnowledgeTypeIDs` exclusively. Use `IncludeCategoryIDs` only when the section genuinely includes the entire category. The same logic applies to `IncludeCanonicalSchemas` — a broad canonical-schema selector can pull in KTYs outside the intended section boundary.
- **KTY ID exact-match format.** All KTY IDs in `IncludeKnowledgeTypeIDs` and `ExcludeKnowledgeTypeIDs` must use the exact full `KnowledgeTypeID` values from the decomposition register CSV (format: `KTY-XX-YY_Full-Descriptive-Name`), not short anchors (`KTY-XX-YY`). The tool performs exact string matching — short-form IDs will silently fail to match.
- `ComplexityClass` is an agent annotation for human review, not a deterministic gate. `SplitTrigger` is the measurable gate criterion derived from `MaxKAFiles`, `MaxEstimatedTokens`, and sizing report signals.
- `ExpectedBodyComponents` must identify the DBM-native subsections or body elements required for the section, not only a broad purpose statement.
- `ExpectedDesignBasisTables` must identify likely body tables or table classes when mapped material contains design-basis values, capacities, limits, equipment lists, operating conditions, or interface matrices. Use `NONE_EXPECTED` only when the mapped basis appears genuinely non-tabular.
- `SourceDBMGeometry` records whether the source DBM-native geometry is `PRESERVED`, `INTENTIONALLY_REDESIGNED`, or `NOT_AVAILABLE`. Intentional redesign requires rationale in `AdequacyRisks` or the section notes.
- `AdequacyRisks` records likely full-DBM risks such as high KTY density, likely table omission, source geometry loss, scaffold leakage risk, sparse upstream basis, or unresolved open items.
- Sections must be subdivided before approval when the expected components and design-basis tables cannot fit into a coherent DBM-native section under the approved size limits.

### `Section_Map.csv`

Minimum required columns:
- `SectionID`
- `SectionTitle`
- `SectionType`
- `SourceDomain`
- `CategoryID`
- `KnowledgeTypeID`
- `SubjectID`
- `ArtifactPath`
- `MappingRole`
- `ContributionScope`
- `SCARefs`
- `DecisionRefs`
- `CurrentStateBasis`
- `LifecycleState`
- `LifecycleSource`
- `Notes`

`MappingRole` values:
- `PRIMARY`
- `SUPPORTING`
- `CONFLICTING`
- `CONTEXT_ONLY`

`ContributionScope` values:
- `FULL_ARTIFACT`
- `TARGET_HEADING`
- `TABLE_ONLY`
- `VALUES_ONLY`
- `BACKGROUND_ONLY`

### `Publication_Rules.md`

Required template fields:
- `DBMOutputMode`
- `ProseStandard`
- `Voice`
- `Tense`
- `HeadingStyle`
- `FacilityNamingRule`
- `BodyCompletenessStandard`
- `TabularDataPolicy`
- `TraceVsEngineeringDetailRule`
- `BodyVsQAArtifactBoundaryRule`
- `StandaloneBodyUsabilityRule`
- `SectionUnderdevelopmentPolicy`
- `DigestOutputRule`
- `ConflictPrecedence`
- `TBDRule`
- `AmendmentNoteRule`
- `TraceAppendixMode`
- `CanonicalTerminologyRule`
- `LargeSectionRule`
- `OpenIssueRule`
- `EpistemicFlatteningRule`
- `SupersessionBodyNoteRule`
- `CoverageExpectationRule`

Recommended defaults:
- `DBMOutputMode`: `FULL_ENGINEERING_DBM`; `DBM_DIGEST` requires explicit human selection and is not the default governing DBM publication output
- `ProseStandard`: engineering-document register — precise, definitive, consistent, concise without omission, comprehensive; the standard expected of a governing design basis document, not a summary or report
- `Voice`: third-person technical
- `Tense`: present tense for current design basis; past tense only for decisions or superseded history
- `HeadingStyle`: numbered hierarchical headings
- `FacilityNamingRule`: full facility name on first use, approved abbreviation thereafter
- `BodyCompletenessStandard`: in `FULL_ENGINEERING_DBM` mode, body sections must cover applicable design criteria, capacities/rates/loads/compositions/emissions/utility demands, equipment/package configuration, operating modes/design cases, controls/safeguards/shutdowns/relief/alarms/permissives, materials/standards/codes/environmental or regulatory limits, interfaces, assumptions/TBDs/exclusions/design-development requirements, and design-basis tables; omitted applicable classes require QA rationale
- `TabularDataPolicy`: design-basis tables belong in the body as included, consolidated, or split/reconstructed tables when mapped material supports them; trace, index, provenance, and reference-only tables remain in appendices or QA
- `TraceVsEngineeringDetailRule`: trace detail, source quotation, and provenance mechanics go to appendices/QA; engineering facts, values, conditions, limits, configurations, interfaces, assumptions, and TBDs stay in the body
- `BodyVsQAArtifactBoundaryRule`: QA assertions, mapped-assertion registers, raw caveat inventories, path inventories, and trace scaffolds must not define the main body shape in `FULL_ENGINEERING_DBM` mode
- `StandaloneBodyUsabilityRule`: the body must be usable for the core engineering design basis without reopening KA files; provenance records support auditability but must not be the only place where material basis content appears
- `SectionUnderdevelopmentPolicy`: emit and block on `UNDERDEVELOPED_SECTION` when mapped active material cannot be represented adequately within the approved section design
- `DigestOutputRule`: `DBM_DIGEST` is prohibited for full-DBM publication unless explicitly selected by the human and recorded in the manifest and rules
- `ConflictPrecedence`: accepted DOMAIN/SCA state and mapped CAT/KTY/KA-local content are the current-state publication authority. Reference/provenance inputs help investigate conflicts and support traceability, but they do not override that authority. When mapped CAT/KTY/KA content appears to conflict with a reference/provenance input, use the admitted `Supersession_Map.csv` and accepted SCA evidence to explain the current basis; if the conflict cannot be resolved from accepted DOMAIN/SCA state, escalate it as an unresolved publication conflict rather than silently preferring either side. A section worker may not infer broad override scope from SCA narrative alone — current-state bindings must be consumed from structured accepted artifacts.
- `TBDRule`: preserve as `TBD` with a note on what is missing
- `AmendmentNoteRule`: short, only when materially useful
- `TraceAppendixMode`: appendix-only
- `CanonicalTerminologyRule`: prefer vocabulary-map canonical terms
- `LargeSectionRule`: split oversize sections instead of forcing synthesis
- `OpenIssueRule`: flatten unresolved open issues to readable `TBD`-style prose when needed, but preserve detailed epistemic state in QA
- `EpistemicFlatteningRule`: body prose uses only `TBD`, `to be confirmed`, and `assumed`; QA preserves the original governance-state label
- `SupersessionBodyNoteRule`: QA/trace by default; a body note is allowed only when a superseded value/scope state remains likely visible to the reader and omitting the note could make the current basis look erroneous
- `CoverageExpectationRule`: every `PRIMARY` KTY should materially contribute to body prose; `SUPPORTING` qualifies or constrains; `CONTEXT_ONLY` remains QA/trace only

### `Publication_Content_Adequacy.md`

Required for `DBM_OUTPUT_MODE = FULL_ENGINEERING_DBM`. Optional for `DBM_DIGEST`.

Purpose:
- lean package-level gate record showing whether the assembled body is adequate as a full engineering DBM
- assembled by `TASK + dbm-publish` from section QA outputs, optional deterministic content-profile smoke-test signals, and direct package review
- not a prose mini-audit and not authored independently by section workers

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
   - include design-basis tables only
   - exclude trace, index, provenance, and reference-only tables
   - summarize included, consolidated/redesigned, omitted with rationale, and deferred because upstream truth is missing
4. `Blockers`
   - fixed finding-code list only: `UNDERDEVELOPED_SECTION`, `UNJUSTIFIED_TABLE_OMISSION`, `PRIMARY_KTY_COLLAPSED`, `MISSING_DESIGN_BASIS_CLASS`, `QA_SCAFFOLD_BODY_LEAKAGE`, `NON_STANDALONE_CORE_BASIS`, `DIGEST_MODE_USED_FOR_FULL_DBM`
5. `Human Review Notes`
   - only issues requiring human judgment
   - no general commentary or duplicate QA narrative

### Post-Authoring Evidence Bundle

The post-authoring evidence bundle is produced by `TASK + dbm-postauthor-concordance` in Gate 6. It lives under `{PACKAGE_ROOT}/RUN-YYYYMMDD-HHMMSS/review/` and contains:

- `Evidence_Bundle_Summary.md` — EvidenceBundleStatus, ReviewStatus, tool run results, input provenance, dimensions assessed
- `Section_Coverage.csv` — structural coverage (expected vs. found sections)
- `Draft_Claims.csv` — values, parameters, terms located in authored text
- `Body_Thinness.csv` — section body underdevelopment signals
- `TBD_Inventory.csv` — TBD/TBC/ASSUMPTION markers with KB cross-reference
- `Candidate_Findings.csv` — agent-prepared findings for human disposition (Origin = AGENT_CHECK)
- `Publication_Review_Disposition.csv` — human disposition artifact

See `workflows/dbm-postauthor-concordance/CONTRACT.md#acceptance` for CSV schemas and `workflows/dbm-postauthor-concordance/WORKFLOW.md` for the finding taxonomy and severity definitions.

### Section Context Packets

Purpose:
- deterministic per-section structural context generated by `build_section_context_packets.py` after section-map planning. Packets help section workers understand objectives, mapped KTY/Subject scope, factual-use eligibility, and open issues without turning governance machinery into body prose.

Each `SEC-##_Context.md` packet contains these fixed sections:
- `Mapped KTYs and Subjects`
- `Objectives Served`
- `Category and KTY Descriptions`
- `Applicable Supersession Bindings`
- `Open Issues Affecting This Section`
- `Factual-Use Eligibility`
- `Vocabulary Terms`
- `Section-Map Role Expectations`

Rules:
- context packets are structural context, not mapped KA content
- they are read-only inputs to section workers
- they may become body-authoring authority only for `OVERVIEW` facility/document framing, and only within the limitation stated in `dbm-section-publish`
- all technical values, operating conditions, equipment requirements, capacities, limits, and specifications must still be grounded in mapped CAT/KTY/KA authority; reference/provenance inputs may support traceability and conflict QA but cannot independently author the section
