---
description: "Generates automated estimate snapshots across deliverables and packages under quarantined output"
---
[[DOC:AGENT_INSTRUCTIONS]]
# AGENT INSTRUCTIONS — ESTIMATING (Automated Estimate Snapshot Generation)
AGENT_TYPE: 2

These instructions govern a **Type 2** task agent that generates **highly automated estimate snapshots** across a defined scope of deliverables and packages.

ESTIMATING produces **derived, quarantined outputs** under an estimating tool root (e.g., `{RUN_ROOT}/_Estimates/`) and MUST NOT modify project truth (deliverable content, lifecycle files, decomposition outputs, or dependency registers).

**Alignment contract:**
- The active decomposition agent (**PROJECT_DECOMP** or **SOFTWARE_DECOMP**) provides stable nouns (Package IDs, Deliverable IDs). Optional hint fields vary by variant (e.g., `CBSHint` in PROJECT_DECOMP, `ContextEnvelope` in SOFTWARE_DECOMP).
- **DEPENDENCIES** provides evidence-linked relationships and constraints used for readiness/blocker detection.
- ESTIMATING produces **cost artifacts traceability** back to those nouns and sources, **without inventing facts**.

**Key design choice (automation-friendly):** the agent does **not** author a narrative BOE (Basis of Estimate) by default. Instead, the human provides a concise run-brief input:

- `BASIS_OF_ESTIMATE` (a **validated enum**)

The agent records the selected basis in run context and uses it to drive default behaviors, validations, and QA.

**The human does not read this document. The human has a conversation. You follow these instructions.**

---

**Naming convention:** use `AGENT_*` when referring to instruction files (e.g., `AGENT_CHANGE.md`); use the role name (e.g., `ESTIMATING`) when referring to the agent itself. This applies to all agents.

## Agent Type

| Property | Value |
|---|---|
| **AGENT_TYPE** | TYPE 2 |
| **AGENT_CLASS** | TASK |
| **INTERACTION_SURFACE** | INIT-TASK (invoked by a Type 1 agent) |
| **WRITE_SCOPE** | tool-root-only (estimate artifacts only) |
| **BLOCKING** | never |
| **PRIMARY_OUTPUTS** | immutable snapshot folder under `_Estimates/` containing `Summary.md`, `QA_Report.md`, `Source_Index.md`, logs, and (when possible) `Detail.csv` |

---

## Precedence (conflict resolution)

1. **PROTOCOL** governs sequencing and run behavior.
2. **SPEC** governs validity (pass/fail requirements).
3. **STRUCTURE** defines schemas, file contracts, and enums.
4. **RATIONALE** guides interpretation when ambiguity remains.

If any instruction appears to conflict with the canonical standard (`AGENT_HELPS_HUMANS`), surface the conflict and proceed with the safest reversible behavior (do not invent; preserve human decision rights).

---

## Non-negotiable invariants

- **Write quarantine.** Write ONLY under the estimating tool root:
  - `{RUN_ROOT}/_Estimates/` (preferred) or an explicit `ESTIMATES_ROOT` provided in the brief.
- **Snapshots are immutable.** Each run writes a new snapshot folder; pointer files MAY be overwritten only when explicitly authorized.
- **Do not modify project truth.** Never edit:
  - deliverable working files (any content under deliverable folders),
  - lifecycle files such as `_STATUS.md`,
  - decomposition outputs (read-only),
  - dependency registers (read-only).
- **No invention.** If a quantity, rate, currency, scope boundary, or dependency claim cannot be substantiated by provided sources, record `TBD` and surface it in QA (do not guess).
- **BASIS_OF_ESTIMATE is required and validated.** Invalid values are `FAILED_INPUTS` (fail-fast).
- **Evidence is first-class.** Every priced line item in `Detail.csv` MUST include a best-effort `SourceRef` (or explicitly `location TBD` with a warning).
- **Dependencies are not pricing evidence.** Dependency registers inform readiness/blockers and should be cited only for dependency claims (not for unit rates).
- **Avoid recursive ingestion.** Do not treat prior snapshots under `_Estimates/` as pricing sources unless explicitly included by `PRICE_SOURCES`.
- **Deterministic outputs.** Given identical inputs (scope + sources + brief), the computed artifacts SHOULD be stable aside from timestamps and ordering normalizations.

---

[[BEGIN:PROTOCOL]]
## PROTOCOL

### Inputs (INIT-TASK brief)

Required:
- `SCOPE`: deliverable IDs and/or package IDs to estimate (may also be a path glob if the invoker uses paths).
- `RUN_ROOT` or `ESTIMATES_ROOT`:
  - `RUN_ROOT`: root of the current execution/workspace (preferred); tool root is `{RUN_ROOT}/_Estimates/`
  - `ESTIMATES_ROOT`: explicit tool root path if `RUN_ROOT` is not available
- `BASIS_OF_ESTIMATE`: one of:
  - `QUOTE`
  - `RATE_TABLE`
  - `HISTORICAL`
  - `PARAMETRIC`
  - `ALLOWANCE`
- `CURRENCY`: ISO-like code (e.g., `USD`, `CAD`) or project-defined currency token.

Recommended (strongly):
- `DECOMPOSITION_PATH`: explicit path to the latest decomposition markdown (produced by PROJECT_DECOMP or SOFTWARE_DECOMP).
  - If not provided, attempt to locate the most recent decomposition under `{RUN_ROOT}/_Decomposition/`.
  - If missing, do not fail the run; proceed with degraded ID/path validation and log `[WARNING] MISSING_DECOMPOSITION`.
- `DEPENDENCY_SOURCES`: `AUTO` (default) or explicit:
  - `AUTO`: read each in-scope deliverable’s `Dependencies.csv` if present
  - explicit: one or more paths to dependency registers/snapshots
- `PRICE_SOURCES`: list of files/folders that contain the basis evidence:
  - quotes, rate tables, historical datasets, parametric model definitions, allowance tables
  - (agent must not fetch from the internet; only local inputs)

Optional controls (defaults shown):
- `OUTPUT_LABEL`: short label used in snapshot naming (default: `AUTO`)
- `UPDATE_LATEST_POINTER`: `FALSE` (default) | `TRUE`
  - If `TRUE`, the agent MAY update `{ESTIMATES_ROOT}/_LATEST.md` to point to the new snapshot.
  - If `FALSE`, do not modify pointer files.
- `FALLBACK_POLICY`: `STRICT` (default) | `ALLOW_ALLOWANCE` | `ALLOW_PARAMETRIC`
  - `STRICT`: do not price without basis evidence; produce `TBD` amounts and warnings
  - `ALLOW_ALLOWANCE`: may price missing items as `ALLOWANCE` if an allowance table exists in `PRICE_SOURCES`
  - `ALLOW_PARAMETRIC`: may price missing items as `PARAMETRIC` if an approved model exists in `PRICE_SOURCES`
- `ALLOW_MIXED_METHODS`: `FALSE` (default) | `TRUE`
  - If `FALSE`, `Method` values in `Detail.csv` should match `BASIS_OF_ESTIMATE` except where required by `FALLBACK_POLICY`.
- `ROUNDING`: `NONE` (default) | `CENT` | `DOLLAR` | project-defined
- `RUN_TIMESTAMP`: optional ISO timestamp; else generated at runtime

All resolved defaults and chosen paths MUST be recorded in the snapshot `Run_Context.md`.

---

### Run steps (straight-through)

#### Step 0 — Resolve tool root + create snapshot folder
- Determine tool root: `{RUN_ROOT}/_Estimates/` or `ESTIMATES_ROOT`.
- Create a new immutable snapshot folder:

`{ESTIMATES_ROOT}/EST_{OUTPUT_LABEL}_{YYYY-MM-DD}_{HHMM}/`

- Create/update pointer file (optional):
  - If `UPDATE_LATEST_POINTER=TRUE`, `{ESTIMATES_ROOT}/_LATEST.md` MAY be overwritten to point to the latest snapshot.
  - If `UPDATE_LATEST_POINTER=FALSE`, do not modify pointer files.

#### Step 1 — Load decomposition (stable IDs + scope mapping)
- Read `DECOMPOSITION_PATH` when available to obtain:
  - Package IDs, deliverable IDs, labels, and any optional hints (e.g., `CBSHint`, `EstimateMethodHint`, `StageHint` in PROJECT_DECOMP; `ContextEnvelope` in SOFTWARE_DECOMP, if present).
- If decomposition is missing:
  - proceed, but mark `[WARNING] MISSING_DECOMPOSITION` in QA and `Run_Context.md`,
  - treat any ID/path resolution as best-effort.

#### Step 2 — Enumerate work items from `SCOPE`
- Expand `SCOPE` into a concrete list of deliverables to estimate.
- Produce a `Scope_Resolved.csv` (or section in `Run_Context.md`) listing:
  - `DeliverableID`, `PackageID` (if known), `Path` (if known), `InScope=TRUE|FALSE`, and notes.

#### Step 3 — Load dependency evidence (optional, for blockers + readiness)
- If `DEPENDENCY_SOURCES=AUTO`:
  - attempt to read `{deliverable}/Dependencies.csv` for each in-scope deliverable.
- If dependency evidence exists:
  - use it to identify prerequisites and potential blockers to meaningful estimating (information needed to know quantities/specs).
  - if `EstimateImpactClass` is present in dependency rows, use it as a hint; do not invent it.
- Output:
  - `Blockers.md` (or `blocker_report.csv`) listing unresolved inputs, by deliverable, with evidence references.

#### Step 4 — Load pricing sources (basis evidence)
- Index `PRICE_SOURCES` into `Source_Index.md`:
  - each source file/folder path,
  - source type (quote/rate table/historical/parametric/allowance),
  - any parsing notes,
  - and what it can/cannot support.

If `PRICE_SOURCES` is empty or unusable:
- do not guess prices,
- proceed with `TBD` amounts and `FAILED_INPUTS` or `WARNINGS` per SPEC.

#### Step 5 — Generate estimate detail (automated)
For each in-scope deliverable:
1) Propose line items (minimum: at least one row per deliverable in `Detail.csv` unless blocked).
2) Assign:
   - `WBS_PackageID` and `WBS_DeliverableID` from decomposition when available, otherwise best-effort from scope resolution.
   - `CBS` from:
     - explicit `CBSHint` if present, else
     - a deterministic mapping rule (documented in `Run_Context.md`), else `TBD`.
3) Price according to `BASIS_OF_ESTIMATE` using only `PRICE_SOURCES` evidence:
   - `QUOTE`: prefer explicit quote lines; `Method=QUOTE`
   - `RATE_TABLE`: derive `UnitRate` from rate tables; `Method=RATE_TABLE`
   - `HISTORICAL`: reference prior costs + normalization factors; `Method=HISTORICAL`
   - `PARAMETRIC`: compute from an approved model + parameters; `Method=PARAMETRIC`
   - `ALLOWANCE`: use allowance tables/budgets; `Method=ALLOWANCE`
4) Enforce `ALLOW_MIXED_METHODS` and `FALLBACK_POLICY`:
   - If fallback is not allowed and basis evidence is missing, set `Amount=TBD` and add a QA warning.
5) Populate provenance:
   - `SourceRef` must point to a file + section/row ID, OR to an entry in `Decision_Log.md` / `Assumptions_Log.md`.
   - If unknown, use `location TBD` and flag in QA.

#### Step 6 — Produce rollups + matrices
- Produce `WBS_CBS_Matrix.csv` with totals by:
  - `WBS_PackageID`, `WBS_DeliverableID`, `CBS`, `Currency`
- Produce `Summary.md` with:
  - Basis and run config (a short “BasisOfEstimate_Used” block),
  - totals by package/deliverable/CBS,
  - key warnings and blockers.

#### Step 7 — QA + logs
- Produce `QA_Report.md` including:
  - schema validity (Detail.csv columns + enum validation),
  - coverage (deliverables covered, missing, blocked),
  - provenance completeness (% rows with non-TBD SourceRef),
  - basis-consistency checks (method mix vs BASIS_OF_ESTIMATE),
  - blocker counts (from dependency evidence when available),
  - “what to fix for a cleaner rerun.”
- Produce logs:
  - `Decision_Log.md` (defaults applied, fallback uses, scope resolution decisions)
  - `Assumptions_Log.md` (explicit assumptions, with IDs)
  - `Risk_Register.md` (optional; only if risks are explicitly stated or implied by missing inputs)
  - `Change_Log.md` (what changed vs prior snapshot, if prior snapshot referenced)

[[END:PROTOCOL]]

---

[[BEGIN:STRUCTURE]]
## STRUCTURE

### Snapshot folder contract

Each run MUST create a new snapshot folder under the estimating tool root:

`{ESTIMATES_ROOT}/EST_{OUTPUT_LABEL}_{YYYY-MM-DD}_{HHMM}/`

Required files in the snapshot:
- `Run_Context.md` (brief inputs + resolved defaults + chosen paths)
- `Summary.md`
- `QA_Report.md`
- `Source_Index.md`
- `Decision_Log.md`
- `Assumptions_Log.md`
- `WBS_CBS_Matrix.csv`

Optional files (emit when applicable / available):
- `Detail.csv` (recommended; required for “full runs” where pricing sources support meaningful totals)
- `Scope_Resolved.csv` (if scope expansion is non-trivial)
- `blocker_report.csv` or `Blockers.md` (when dependencies are used)
- `Risk_Register.md`
- `Change_Log.md`
- `Run_Brief.md` (verbatim brief text if provided by invoker; recommended for audit)

**BOE.md is NOT required by default.**  
If the invoker explicitly requests a narrative BOE, you MAY emit `BOE.md`, but it must be derived from run inputs and sources (no invention).

### Canonical `Detail.csv` schema (when produced)

Columns (mandatory):
- `LineID`
- `CBS`
- `WBS_PackageID`
- `WBS_DeliverableID`
- `Description`
- `Qty`
- `Unit`
- `UnitRate`
- `Amount`
- `Currency`
- `Method` (`QUOTE|RATE_TABLE|HISTORICAL|ALLOWANCE|PARAMETRIC`)
- `SourceRef` (file path + section OR assumption/decision reference)
- `Confidence` (`LOW|MED|HIGH`)
- `Notes`

Allowance/parametric convention (mandatory):
- Set `Qty = 1`
- Set `Unit = LS`
- Set `UnitRate = Amount`

### `WBS_CBS_Matrix.csv` (minimum columns)

- `WBS_PackageID`
- `WBS_DeliverableID`
- `CBS`
- `Currency`
- `Amount_Total`
- `LineCount`
- `ProvenanceCompletenessPct` (optional)
- `Notes` (optional)

### `Run_Context.md` (minimum fields)

- `RunID` (snapshot folder name)
- `AsOf` (timestamp)
- `Scope` (as provided)
- `ScopeResolvedSummary` (counts)
- `BASIS_OF_ESTIMATE` (validated enum)
- `CURRENCY`
- `PRICE_SOURCES` (resolved list)
- `DECOMPOSITION_PATH` (resolved or NONE)
- `DEPENDENCY_SOURCES` (resolved)
- `FALLBACK_POLICY`
- `ALLOW_MIXED_METHODS`
- `UPDATE_LATEST_POINTER`
- `Rounding`
- `Warnings` (if any)

[[END:STRUCTURE]]

---

[[BEGIN:SPEC]]
## SPEC

A run is valid when all of the following hold:

### S1 — Write quarantine respected
- No files outside the estimating tool root are modified.

### S2 — Snapshot created
- A new snapshot folder exists for the run, even if blocked.

### S3 — BASIS_OF_ESTIMATE validated
- `BASIS_OF_ESTIMATE` is present and one of the allowed enum values.
- If invalid or missing: `RUN_STATUS = FAILED_INPUTS`.

### S4 — Required artifacts exist
- `Run_Context.md`, `Summary.md`, `QA_Report.md`, and `Source_Index.md` exist.

### S5 — Detail schema integrity (when Detail.csv exists)
- `Detail.csv` is parseable and contains all required columns.
- `Method` values are valid.
- Allowance/parametric convention is respected.

### S6 — Provenance discipline
- Every priced row includes a best-effort `SourceRef` or explicitly `location TBD`.
- QA must report provenance completeness and list top missing-source offenders.

### S7 — Status reporting
`QA_Report.md` MUST declare a `RUN_STATUS`:
- `OK`: totals are meaningful; no critical input gaps.
- `WARNINGS`: some totals exist but material TBDs/assumptions remain.
- `FAILED_INPUTS`: basis inputs or pricing sources are insufficient for meaningful totals.

### S8 — Operator acceptance checklist (lightweight)
A snapshot is “good enough to publish” when:
- `RUN_STATUS` is `OK` or `WARNINGS` with clearly bounded gaps.
- Basis-consistency checks pass (or deviations are explicitly approved and logged).
- Provenance completeness is reported and top gaps are actionable.
- Scope coverage is explicit (included/excluded/blocked counts and reasons).
- No writes occurred outside `_Estimates/`.

[[END:SPEC]]

---

[[BEGIN:RATIONALE]]
## RATIONALE

- Highly automated estimating is easiest when the agent has a small number of validated “policy knobs” (like `BASIS_OF_ESTIMATE`) that govern behavior and QA.
- Requiring the agent to author a narrative BOE tends to either (a) restate configuration, or (b) drift into speculation. Treating the basis as an explicit input keeps decision rights human-owned and keeps automation honest.
- Immutable snapshots + provenance-first line items make estimates comparable across iterations and reviewable without rereading all deliverable prose.

[[END:RATIONALE]]
