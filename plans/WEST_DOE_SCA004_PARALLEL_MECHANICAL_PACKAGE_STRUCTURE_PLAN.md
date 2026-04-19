# West Doe SCA-004 Parallel Mechanical Package Structure Plan

## Summary

This plan defines a mirrored `SCOPE_CHANGE` execution for both West Doe `DOMAIN` roots so another agent can run the amendments without inventing policy.

The amendment is intentionally small in both roots:
- add one new `CAT-007` Knowledge Type
- add exactly two new Knowledge Subjects
- add exactly two new derived singleton ledger units
- update decomposition-local truth and `_ScopeChange` state only
- do not generate KTY-local `Scoping.md` / `KA-*.md` during Gates 1-5

The two roots must execute as parallel `SCA-004` amendments with the same KTY name, the same subject model, the same source-interpretation rules, and the same downstream rerun expectations.

## Roots And Authorities

### Root 1: Comp and Liquids

- Root: `domain-test/domains/West_Doe_Comp_and_Liquids_DBM`
- Active `_LATEST.md`: `SCA-003`
- Primary decomposition artifact:
  - `_Decomposition/WEST_DOE_DOMAIN_DECOMPOSITION.md`
- Governing package CSV sources:
  - `_Sources/Packages_3-25_1.csv`
  - `_Sources/Line-Items_3-25_1.csv`

Current source-table counts:
- `Packages_3-25_1.csv`: 23 data rows
- `Line-Items_3-25_1.csv`: 60 data rows

### Root 2: Deepcut

- Root: `domain-test/domains/West_Doe_Deepcut_DBM`
- Active `_LATEST.md`: `SCA-003`
- Primary decomposition artifact:
  - `_Decomposition/DeepCut_DOMAIN_DECOMP_FINAL_v4.md`
- Governing package CSV sources:
  - `_Sources/Packages_4-25_1.csv`
  - `_Sources/Line-Items_4-25_1.csv`

Current source-table counts:
- `Packages_4-25_1.csv`: 33 data rows
- `Line-Items_4-25_1.csv`: 72 data rows

### Governing contracts

Execution must follow the current repository contracts, especially:
- `agents/AGENT_SCOPE_CHANGE.md`
- `plans/WEST_DOE_TWO_ROOT_DBM_REMEDIATION_AND_PUBLICATION_PLAN.md`
- `plans/WEST_DOE_EXECUTION_MODEL.md`
- `agents/AGENT_AUDIT_DECOMP.md`

Those contracts now require:
- `DOMAIN` direct-write scope to stay within the decomposition package and `_ScopeChange`
- active snapshot completeness
- explicit direct-write vs downstream-rerun separation
- Phase 6 reruns to remain downstream from Gate 5, not folded into amendment execution

## Amendment Intent

The amendment adds a new plant-wide mechanical packaging KTY to both roots under `CAT-007 Plant Design Requirements`.

The KTY captures how facility equipment is grouped into packages for design, procurement, fabrication, construction, and installation planning, using the source-table structure already present in each root’s `_Sources/` folder.

This is not an edit to the existing VRU KTYs or any existing process KTY. It is a new `CAT-007` KTY in both roots.

## New KTY Contract

### New KTY ID and name

Both roots must add:

- `KTY-07-07_Mechanical-Package-Structure`

This is the next available `CAT-007` slot in both roots.

### Subject model

Both roots must add exactly these two subjects:

- `SUB-07-07-01_Package-Summary`
- `SUB-07-07-02_Package-Line-Items`

There must not be a third installation, housing, skid, or building subject. Any such detail must remain embedded as source-faithful row content inside the two approved subjects.

### Recommended KTY metadata

Use identical wording across both roots unless a file format forces a local variation:

- Name: `Mechanical Package Structure`
- Category: `CAT-007 Plant Design Requirements`
- Description:
  - `Defines the package roster and package line-item structure used to package, design, fabricate, install, and hand off facility equipment.`
- Intended users:
  - `Process, mechanical/package, procurement/fabrication, construction, layout, and project engineering users`
- When used:
  - `Use when defining package boundaries, package composition, area allocation, fabrication/procurement packages, and installation planning.`
- Canonical schema:
  - `Design Data Reference`

If a root requires a schema field split, use:
- schema type: `Design Data Reference`
- schema detail:
  - `Package Summary Table; Package Line-Item Table; Notes; References`

## Source Interpretation Rules

The KTY must mirror the actual two-table source structure directly.

### Subject 1: Package Summary

- Subject ID: `SUB-07-07-01_Package-Summary`
- Authority file:
  - `Packages_*`
- Required fields:
  - `Package Name`
  - `Line Items`
  - `LSD (Area)`
  - `Total Equipment`

This subject captures the package roster and package-level summary exactly as the summary CSV provides it.

### Subject 2: Package Line Items

- Subject ID: `SUB-07-07-02_Package-Line-Items`
- Authority file:
  - `Line-Items_*`
- Required fields:
  - `Tracking Number`
  - `Package Name`
  - `Line Item`
  - `LSD (Area)`
  - `Equipment Count`
  - `Equipment Tags`
  - `NOTES`

This subject captures package composition and detailed line-item membership exactly as the line-item CSV provides it.

### Interpretation constraints

The executing agent must follow these rules:
- do not infer package hierarchy beyond what the CSVs explicitly state
- do not normalize or rename package names
- do not deduplicate repeated equipment tags unless a separate amendment explicitly authorizes a source correction
- treat terms such as `Building`, `Skid`, `Train`, and `Unit` as source row content, not as a separate modeling layer
- if the package summary CSV and the line-item CSV disagree on totals or grouping, record that as an explicit scope-change finding instead of silently reconciling it

## Evidence Model

This amendment must remain lightweight.

Do not create one HBK unit per source row.

Instead, use exactly two new derived singleton units per root:
- one derived singleton unit for `SUB-07-07-01_Package-Summary`
- one derived singleton unit for `SUB-07-07-02_Package-Line-Items`

That means the new KTY adds:
- 1 new KTY
- 2 new subjects
- 2 new ledger units

and nothing more at the decomposition-unit level.

## Objective Mapping

The objective mapping differs by root and must be fixed as follows.

### Comp and Liquids

Map the new KTY to:

- `OBJ-006`

### Deepcut

Map the new KTY to:

- `OBJ-004`

## Gate Structure And Parallel Execution

The two amendments should be run in parallel, but with a single cross-root naming and scope check before Gate 5 execution.

### Shared Gate 1 baseline

For each root:
- confirm the two package CSVs exist
- confirm they are the only source authority for `SCA-004`
- confirm `KTY-07-07` does not already exist
- confirm the root’s `_LATEST.md` currently points to `SCA-003`

### Shared Gate 2 impact assessment

For each root:
- assess current `CAT-007` counts
- assess current objective mapping surfaces
- identify every decomposition-local derivative that duplicates KTY, subject, unit, or telemetry truth
- classify each affected surface as:
  - `DIRECT_EDIT`
  - `RECOMPUTE`
  - `NO_CHANGE`

### Shared Gate 3 approval text

Gate 3 must approve the same structural decision in both roots:
- new KTY `KTY-07-07_Mechanical-Package-Structure`
- exactly two subjects
- derived singleton evidence model
- no row-level HBK explosion

### Cross-root checkpoint before Gate 4 approval

Before either root proceeds to Gate 5, compare both Gate 4 plans and confirm:
- same KTY name
- same subject IDs
- same subject names
- same schema label
- same descriptive wording
- same downstream rerun model

The only intended differences between roots are:
- source filenames
- objective mapping
- root-local file names and telemetry totals

### Gate 5 execution model

Apply both roots’ Gate 5 direct writes in parallel only after the cross-root checkpoint passes.

No KTY-local `Scoping.md` or `KA-*.md` generation occurs during Gate 5.

## Root-Specific Direct-Write Scope

### Comp and Liquids write set

At minimum, update these decomposition-local and `_ScopeChange` surfaces:

- `_Decomposition/WEST_DOE_DOMAIN_DECOMPOSITION.md`
- `_Decomposition/annex_categories.csv`
- `_Decomposition/annex_category_telemetry.csv`
- `_Decomposition/annex_coverage_telemetry.csv`
- `_Decomposition/annex_domain_ledger.csv`
- `_Decomposition/annex_knowledge_subjects.csv`
- `_Decomposition/annex_knowledge_types.csv`
- `_Decomposition/annex_objectives.csv`
- `_Decomposition/annex_objective_kty_mapping.csv`
- `_Decomposition/annex_unit_category_assignment.csv`
- `_Decomposition/annex_unit_subject_mapping.csv`
- `_Decomposition/annex_validation_checks.csv`
- `_Decomposition/annex_decision_log.csv`
- `_ScopeChange/_LATEST.md`
- one new active snapshot folder under `_ScopeChange/`

Update any additional decomposition-local derivative if Gate 2 determines it duplicates the new KTY, subject, unit, or telemetry truth.

### Deepcut write set

At minimum, update these decomposition-local and `_ScopeChange` surfaces:

- `_Decomposition/DeepCut_DOMAIN_DECOMP_FINAL_v4.md`
- `_Decomposition/DeepCut_Category_Register_v4.csv`
- `_Decomposition/DeepCut_Coverage_Telemetry_v4.json`
- `_Decomposition/DeepCut_Domain_Ledger_v4.csv`
- `_Decomposition/DeepCut_Knowledge_Subject_Register_v4.csv`
- `_Decomposition/DeepCut_Knowledge_Type_Register_v4.csv`
- `_Decomposition/DeepCut_Node_Summary_v4.csv`
- `_Decomposition/DeepCut_Objective_Register_v4.csv`
- `_ScopeChange/_LATEST.md`
- one new active snapshot folder under `_ScopeChange/`

Do not edit these unless Gate 2 identifies a concrete duplicate-truth requirement:
- `DeepCut_Open_Issues_v4.csv`
- `DeepCut_Scope_Boundary_Register_v4.csv`
- `DeepCut_Standalone_Subject_Coverage_v4.csv`
- `DeepCut_Vocabulary_Map_v4.csv`
- `DeepCut_Publication_Manifest_v4.md`

## Decomposition-Level Deltas To Apply

### Comp and Liquids expected deltas

Current top-level counts:
- Total Handbook Units: `319`
- IN Units: `272`
- Knowledge Types: `84 active (4 retired, 88 total)`
- Knowledge Subjects: `272`
- Open Issues: `0`

Expected post-amendment deltas:
- Total Handbook Units: `+2` -> `321`
- IN Units: `+2` -> `274`
- Knowledge Types: `+1` -> `85 active (4 retired, 89 total)`
- Knowledge Subjects: `+2` -> `274`
- Open Issues: unchanged unless Gate 2 identifies a source-table contradiction

`CAT-007` expected deltas:
- KTY count: `6 -> 7`
- subject count on actual-telemetry surfaces: `15 -> 17`
- IN unit count: `15 -> 17`

The agent must preserve each file’s existing count convention. If `annex_categories.csv` uses an explicit-subject-count convention rather than the actual-subject-count convention, increment it consistently rather than forcing a new convention.

Use the next available new HBK IDs:
- `HBK-0320`
- `HBK-0321`

### Deepcut expected deltas

Current telemetry baselines:
- UnitCount: `5690`
- KnowledgeTypeCount: `97`
- SubjectCount: `432`
- OpenIssueCount: `571`

Expected post-amendment deltas:
- UnitCount: `+2` -> `5692`
- KnowledgeTypeCount: `+1` -> `98`
- SubjectCount: `+2` -> `434`
- OpenIssueCount: unchanged unless Gate 2 identifies a source-table contradiction

`CAT-007` expected deltas:
- type count: `6 -> 7`
- subject count: `15 -> 17`
- IN unit count: `178 -> 180`

Use the next available new HBK IDs:
- `HBK-5978`
- `HBK-5979`

Do not change `StandaloneSubjectCount` unless the agent can defend a real standalone-subject rule change. The preferred default is that it remains unchanged because this new KTY has two explicit subjects.

## Main Document Section Expectations

### Comp and Liquids

The main decomposition document is expected to change in at least these surfaces:
- publish summary / coverage summary
- objectives table for `OBJ-006`
- `CAT-007` category summary row
- `CAT-007` structured domain outline
- Knowledge Type Attribute Table
- Knowledge Subject Attribute Table
- Domain Ledger
- coverage / category telemetry sections
- validation check section
- decision log
- change log

### Deepcut

The main decomposition document is expected to change in at least these surfaces:
- category summary / `CAT-007` row
- `CAT-007` knowledge-type table
- subject summary table
- any domain-ledger-derived HTML/markdown surfaces
- coverage telemetry table
- objective mapping references where `OBJ-004` lists `CAT-007` KTYs
- decision/change tracking surfaces embedded in the file

## Active Snapshot Contract

Create one new active snapshot in each root using the same local timestamp token.

Recommended naming pattern:
- `SCA-004_2026-04-19_<HHMM>/`

The timestamp should be the same in both roots so the pair can be reviewed as a synchronized amendment set.

Each active snapshot must contain at least:
- `Brief.md`
- `Impact_Assessment.md`
- `Propagation_Plan.md`
- `Amendment_Actions.csv`
- `Pre_Change_Coverage.json`
- `Post_Change_Coverage.json`
- `Decision_Log.md`
- `Handoff_State.md`
- `RUN_SUMMARY.md`

`_ScopeChange/_LATEST.md` in each root must then be updated to point to that root’s new `SCA-004` snapshot.

## Downstream Phase 6 Obligations

This amendment creates a new KTY in each root, so Phase 6 must generate new KTY-local artifacts after Gate 5 acceptance.

Required downstream sequence after both roots finish Gate 5:
1. `TASK + domain-documents` for `KTY-07-07_Mechanical-Package-Structure` in each root
2. `TASK + kty-metadata-align` for the new KTY folder in each root
3. `TASK + decomposition-package-review` for each root
4. `DOMAIN_HYPERGRAPH`
5. `AUDIT_DECOMP`
6. root-level terminology / conformity sweep
7. targeted reruns only if the new KTY artifacts fail audit or metadata alignment

Default downstream scope:
- the new `KTY-07-07` only in each root
- do not rerun existing process KTYs unless Gate 5 wording introduces a real contradiction elsewhere

## Validation Requirements

The executing agent must validate all of the following before calling Gate 5 complete.

### Cross-root structural validation

- both roots use `KTY-07-07_Mechanical-Package-Structure`
- both roots use exactly the two approved subject IDs
- both roots use mirrored descriptive wording
- both roots use the same source interpretation rules

### Comp and Liquids validation

- `OBJ-006` includes `KTY-07-07_Mechanical-Package-Structure`
- `annex_objective_kty_mapping.csv`, `annex_objectives.csv`, and the main objectives table agree
- `CAT-007` counts agree across:
  - main decomposition
  - `annex_categories.csv`
  - `annex_category_telemetry.csv`
  - `annex_coverage_telemetry.csv`
  - validation checks
- both new HBK rows are present in:
  - `annex_domain_ledger.csv`
  - `annex_unit_category_assignment.csv`
  - `annex_unit_subject_mapping.csv`

### Deepcut validation

- `OBJ-004` includes `KTY-07-07_Mechanical-Package-Structure`
- `DeepCut_Objective_Register_v4.csv` agrees with the main decomposition
- `CAT-007` counts agree across:
  - main decomposition
  - `DeepCut_Category_Register_v4.csv`
  - `DeepCut_Node_Summary_v4.csv`
  - `DeepCut_Coverage_Telemetry_v4.json`
- both new HBK rows are present in:
  - `DeepCut_Domain_Ledger_v4.csv`
  - any category/type/subject summary derivatives that enumerate unit rows

### Snapshot and handoff validation

- both roots’ active snapshots are complete
- both roots’ `_LATEST.md` point to `SCA-004`
- both roots’ `RUN_SUMMARY.md` distinguish:
  - direct writes now
  - downstream reruns next
  - closure status after reruns

## Explicit Non-Goals

This amendment does not authorize:
- generating KTY-local files during Gate 5
- editing existing process KTY-local folders during Gate 5
- exploding source CSV rows into row-level HBK units
- modifying `_Aggregation/`, hypergraph, or publication outputs during Gate 5
- changing the source CSV files themselves

## Assumptions And Defaults

- This is a handoff plan only. It is not execution.
- Both roots use `SCA-004` for this amendment.
- The new KTY belongs in `CAT-007 Plant Design Requirements`.
- The KTY structure is defined by the actual two-table source shape, so there are exactly two subjects.
- The evidence model is derived-singleton, not row-level decomposition.
- The preferred schema label is `Design Data Reference`.
- If a root-specific source-table contradiction is discovered during Gate 2, the agent should surface it as an explicit issue rather than improvising a reconciliation.
