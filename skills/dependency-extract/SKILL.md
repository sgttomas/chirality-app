---
name: dependency-extract
description: Extract dependency register (Dependencies.csv v3.1) from deliverable source documents using Anchor x Execution edge typing with evidence-first provenance. Setup-pipeline skill dispatched by ORCHESTRATOR during project setup.
compatibility: Chirality TASK; dispatched by ORCHESTRATOR setup pipeline (and control-loop refresh runs).
allowed-tools: python3 tools/validation/validate_dependencies_schema.py:*, python3 tools/validation/validate_enum.py:*
metadata:
  chirality-skill-version: "1"
  chirality-task-profile: NONE
---

# SKILL — dependency-extract

## Purpose

Extract typed knowledge-graph edges from a deliverable's source documents, producing a deliverable-local dependency register (`Dependencies.csv` v3.1 + `_DEPENDENCIES.md`) that downstream workflows (aggregation, reconciliation, estimating, scheduling) can merge into larger graphs.

The skill performs **two-pass extraction** to preserve **Tree x DAG** knowledge-graph integrity:

- **Tree** edges are emitted as `DependencyClass=ANCHOR` rows that connect this deliverable to an existing definition node (WBS/SSOW/objective) and optionally to requirement IDs.
- **DAG** edges are emitted as `DependencyClass=EXECUTION` rows between deliverables (and other entities) needed to execute the work (prerequisites, handovers, constraints, interfaces).

This skill does **not** build project-level graphs. It produces only deliverable-local registers that downstream aggregation agents can merge.

## Suitable agent shells

- `TASK` (generic shell mode, no profile)

Typical dispatcher: ORCHESTRATOR dispatches TASK with `TaskSkill: dependency-extract` during project setup, or later for explicit refresh runs during the tier control loop. Runs straight-through; never blocks on human decisions.

## Inputs

### Required

- `SCOPE` — deliverable(s) / package(s) / all deliverables under the current run root

### Optional run-root + decomposition settings

- `RUN_ROOT` — path to run workspace (if available to the invoker)
- `DECOMPOSITION_PATH` — explicit path to the latest decomposition markdown (preferred)
  - If not provided and `RUN_ROOT` exists: locate the most recent decomposition file under `{RUN_ROOT}/_Decomposition/` and record the chosen path in Run Notes.
  - If no decomposition file can be located: do not fail the run; record a warning and skip validation rather than guessing.

### Optional source-document settings (defaults shown)

- `SOURCE_DOCS`: `AUTO` (default) | explicit list of filenames/paths to scan per deliverable
  - `AUTO` means: scan the deliverable folder for candidate source documents, excluding dependency artifacts and obvious generated files.
- `DOC_ROLE_MAP`: `DEFAULT` (default) | explicit mapping of doc roles to filenames/patterns
  - Roles: `ANCHOR_DOC` (definition/traceability signal) and `EXECUTION_DOCS` (workflow/execution signal).
  - DEFAULT heuristic (overrideable):
    - ANCHOR_DOC candidates: filenames containing `datasheet`, `definition`, `requirements`, `scope`, `trace`, `spec`
    - EXECUTION_DOC candidates: filenames containing `procedure`, `method`, `plan`, `workflow`, `guidance`, `runbook`
- `ANCHOR_DOC`: `AUTO` (default) | explicit filename/path
  - `AUTO` means: choose the highest-confidence match from `DOC_ROLE_MAP` + `SOURCE_DOCS`; otherwise the first doc in `SOURCE_DOCS`.
- `EXECUTION_DOC_ORDER`: `AUTO` (default) | ordered list of filenames/paths
  - `AUTO` means: order execution docs by likely workflow clarity (per `DOC_ROLE_MAP`) and then the remaining docs.

### Optional controls (defaults shown)

- `MODE`: `UPDATE` (default) | `RESET_EXTRACTED`
- `STRICTNESS`: `CONSERVATIVE` (default) | `AGGRESSIVE`
- `CONSUMER_CONTEXT`: `NONE` (default) | `TASK_ESTIMATING` | `AGGREGATION` | `RECONCILIATION`

Defaults and chosen paths MUST be recorded in `_DEPENDENCIES.md` Run Notes.

### Deliverable-local read-only input (if present)

- `_REFERENCES.md` — used to resolve document pointers/paths for `TargetType=DOCUMENT` rows and to populate `TargetLocation` conservatively.

## Runtime overrides

| Key | Meaning | Default | Allowed values |
|---|---|---|---|
| `SCOPE` | Deliverables in scope for this run | **Required** | deliverable ID(s) / package ID(s) / `ALL` |
| `RUN_ROOT` | Path to run workspace | (invoker context) | Absolute path |
| `DECOMPOSITION_PATH` | Path to decomposition markdown | auto-discover under `{RUN_ROOT}/_Decomposition/` | Absolute path |
| `SOURCE_DOCS` | Documents to scan per deliverable | `AUTO` | `AUTO` / explicit list |
| `DOC_ROLE_MAP` | Role-to-filename mapping | `DEFAULT` | `DEFAULT` / explicit mapping |
| `ANCHOR_DOC` | Primary anchor doc | `AUTO` | `AUTO` / filename |
| `EXECUTION_DOC_ORDER` | Execution doc ordering | `AUTO` | `AUTO` / ordered list |
| `MODE` | Update vs reset behavior | `UPDATE` | `UPDATE` / `RESET_EXTRACTED` |
| `STRICTNESS` | Extraction posture | `CONSERVATIVE` | `CONSERVATIVE` / `AGGRESSIVE` |
| `CONSUMER_CONTEXT` | Downstream consumer hint | `NONE` | `NONE` / `TASK_ESTIMATING` / `AGGREGATION` / `RECONCILIATION` |

## Tool usage

Preferred deterministic helpers (called during Function 5 local quality checks):

- `python3 tools/validation/validate_dependencies_schema.py {deliverable_folder}/Dependencies.csv` — confirms all 29 required v3.1 columns are present and CSV is parseable.
- `python3 tools/validation/validate_enum.py {ENUM_NAME} {value}` — normalizes and validates enum field values (`DEPENDENCY_CLASS`, `ANCHOR_TYPE`, `DIRECTION`, `DEPENDENCY_TYPE`, `TARGET_TYPE`, `EXPLICITNESS`, `CONFIDENCE`, `ORIGIN`, `STATUS`, `SATISFACTION_STATUS`).
- `tools/validation/validate_id_format.sh {TYPE} {value}` — validates deliverable/package/WBS ID formats.

Disallowed behavior:

- No editing of any source document or `_REFERENCES.md`.
- No editing of decomposition outputs.
- No writes outside dependency artifacts (`{deliverable}/_DEPENDENCIES.md`, `{deliverable}/Dependencies.csv`).
- No hierarchy discovery (no creating or restructuring the decomposition Tree).
- No cross-deliverable synthesis (aggregation is downstream).

## Read boundary

Reads are limited to the current deliverable folder plus the decomposition document (if available):

| File | Read scope | Purpose |
|---|---|---|
| `{deliverable}/_REFERENCES.md` | Full (if present) | Resolve document pointers for `TargetType=DOCUMENT` rows |
| Source documents in scope | Full | Evidence extraction (anchors + execution edges) |
| `{deliverable}/Dependencies.csv` | Full (if present) | Match/merge with existing rows |
| `{deliverable}/_DEPENDENCIES.md` | Full (if present) | Preserve declared lists + Run History |
| `{DECOMPOSITION_PATH}` | Read-only | Validate anchors + resolve canonical labels |

## Write boundary

Writes are limited to dependency artifacts only:

- `{deliverable}/_DEPENDENCIES.md`
- `{deliverable}/Dependencies.csv`

No other files may be created or modified.

## Method

### Function 1 — Two-pass extraction (ANCHOR first, then EXECUTION)

Dependency extraction MUST be performed in two passes to preserve **Tree x DAG** integrity.

#### Pass 1 (Vertical) — Anchor this deliverable to the Tree (Definition)

**Primary source:** `{ANCHOR_DOC}`.

**Goal:** Emit:
- exactly one **parent anchor** when possible (`DependencyClass=ANCHOR`, `AnchorType=IMPLEMENTS_NODE`)
- zero or more **trace anchors** (`DependencyClass=ANCHOR`, `AnchorType=TRACES_TO_REQUIREMENT`)

**Signals to look for (examples):**
- "WBS Ref", "Parent ID", "Objective ID", "Scope Item ID"
- "Traceability", "Requirements", "Requirement IDs", "Compliance to ..."
- tables/fields mapping this deliverable to upstream definition identifiers

**Row rules (ANCHOR):**
- `DependencyClass=ANCHOR`
- `Direction=UPSTREAM` (anchors point "up" to definition)
- `AnchorType`:
  - `IMPLEMENTS_NODE` for the single parent definition node
  - `TRACES_TO_REQUIREMENT` for requirement trace links
- `DependencyType=OTHER` (do not overload execution dependency types; use `AnchorType` for meaning)
- `TargetType`:
  - `WBS_NODE` for parent anchors (or the project's canonical "definition node" type)
  - `REQUIREMENT` for requirement trace anchors
  - `UNKNOWN` if you cannot resolve the target kind confidently

**Using the decomposition document (preferred, if available):**
- Use it to validate and label anchors:
  - confirm the candidate identifier exists in the decomposition's scope ledger / packages / deliverables / objectives sections,
  - resolve canonical labels for `TargetName`,
  - resolve stable deliverable/package IDs when referenced.
- If decomposition is missing: record `[WARNING] MISSING_DECOMPOSITION` and skip validation/label resolution rather than guessing.

**STRICTNESS handling:**
- `CONSERVATIVE`: emit ANCHOR rows only when identifiers appear explicitly.
- `AGGRESSIVE`: you MAY emit a plausible anchor if strongly implied, but must mark it as `ASSUMPTION` in `Notes` and set `Confidence=LOW`.

#### Pass 2 (Horizontal) — Map execution flow edges (DAG)

**Primary sources:** `{EXECUTION_DOC_ORDER}`.

**Goal:** Emit `DependencyClass=EXECUTION` rows capturing prerequisites, handoffs, constraints, and explicit information transfer.

**Signals to look for:**
- prerequisites, required inputs, approvals, "before you can..."
- outputs consumed by other deliverables
- explicit data/artifact handoffs ("provided by...", "requires receipt of...", "uses the following output from...")
- constraints explicitly framed as requirements/approvals/artifacts

**Row rules (EXECUTION):**
- `DependencyClass=EXECUTION`
- `AnchorType=NOT_APPLICABLE`
- `DependencyType` uses canonical execution enums (`PREREQUISITE`, `INTERFACE`, `HANDOVER`, `CONSTRAINT`, `ENABLES`, `OTHER`)
- `Direction` indicates flow relative to this deliverable (`UPSTREAM` inputs; `DOWNSTREAM` outputs/consumers)

**Using `_REFERENCES.md` (preferred, if available):**
- Use it to resolve document identifiers/names mentioned in sources to stable pointers:
  - Prefer a local path when present.
  - Otherwise record the best available pointer (URL, doc ID) in `TargetLocation`.
- Do not emit a dependency row solely because a reference is listed in `_REFERENCES.md` unless the source explicitly states it is required.

Dependency evidence must include:
- `EvidenceFile` (which source document)
- `SourceRef` (path + heading; else `location TBD`)
- optional `EvidenceQuote` (<= 30 words)

### Function 2 — Resolve targets (best-effort, conservative)

**Deliverable targets (preferred):**
- Prefer exact matches to deliverable IDs defined by the decomposition (do not assume numeric formats).
- If decomposition exists, resolve target IDs by lookup.
- If decomposition is missing, accept explicit IDs as strings; otherwise use `TargetType=UNKNOWN`.

**Anchors:**
- Accept non-deliverable identifiers (WBS/SSOW/OBJ/REQ) when explicitly present.
- Do not invent missing IDs.

If uncertain:
- keep `TargetType=UNKNOWN`,
- preserve the raw reference in `TargetName` and/or `Statement`,
- mark hypotheses as `PROPOSAL` in `Notes` (never upgrade uncertainty into FACT).

Normalize legacy values on write:
- `Direction`: `INBOUND` -> `UPSTREAM`, `OUTBOUND` -> `DOWNSTREAM`

### Function 3 — Persist to canonical register (`Dependencies.csv`)

- Create `Dependencies.csv` if missing.
- Ensure `RegisterSchemaVersion` column exists; set to `v3.1` for all rows.
- Preserve existing `DependencyID` for matchable rows.
- Update `LastSeen`, set `Status=ACTIVE` when found.
- Mark unseen extracted rows `RETIRED` (do not delete).
- Preserve declared edges (`Origin=DECLARED`).
- Ensure `FromDeliverableID` matches the host deliverable identity.
- Ensure `DependencyID` uniqueness within the deliverable register.
- Normalize target ID placement on write:
  - For non-deliverable targets (e.g., `WBS_NODE`, `REQUIREMENT`, `DOCUMENT`, `EXTERNAL`), `TargetDeliverableID` MUST be empty; use `TargetRefID` (if a stable ID exists) and `TargetName`.
  - For `TargetType=DELIVERABLE`, `TargetDeliverableID` MUST contain the deliverable stable ID.

Match/merge precedence for extracted rows (in order):
1. Existing `DependencyID` exact match
2. Same `DependencyClass` + `AnchorType` + `Direction` + `DependencyType` + `TargetType` + target identifiers + near-equivalent `Statement`
3. Otherwise create new row with new `DependencyID`

### Function 4 — Update `_DEPENDENCIES.md` index

Keep declared lists and add/refresh:
- `## Extracted Dependency Register` (counts + compact table)
- `## Run Notes` (defaults + assumptions + paths used + warnings)
- `## Run History` (append-only; one entry per run: timestamp, mode, strictness, decomposition path/status, warnings, ACTIVE counts)
- `## Lifecycle Summary` (ACTIVE/RETIRED counts + closure-state breakdown)
- `## Downstream Handoff Notes` (only when `CONSUMER_CONTEXT` is not `NONE`)

Do not rename the declared dependency sections.

### Function 5 — Local quality checks (mandatory)

Before finalizing files, run these checks using deterministic tools where available:

**Schema validation**
- Validate schema: `python3 tools/validation/validate_dependencies_schema.py {deliverable_folder}/Dependencies.csv`
  Confirms all 29 required v3.1 columns are present and CSV is parseable.
- `DependencyID` is present and unique within the file.

**Enum validation**
- Validate enum fields on write using `python3 tools/validation/validate_enum.py`:
  - `DEPENDENCY_CLASS`, `ANCHOR_TYPE`, `DIRECTION`, `DEPENDENCY_TYPE`, `TARGET_TYPE`, `EXPLICITNESS`, `CONFIDENCE`, `ORIGIN`, `STATUS`, `SATISFACTION_STATUS`
- Normalize legacy values: `INBOUND` -> `UPSTREAM`, `OUTBOUND` -> `DOWNSTREAM` on write.

**ID format validation**
- Validate all ID fields: `tools/validation/validate_id_format.sh DEL {FromDeliverableID}`, `tools/validation/validate_id_format.sh PKG {FromPackageID}`, etc.

**Evidence & provenance checks**
- ACTIVE rows contain `EvidenceFile` and `SourceRef` (or explicit `location TBD`).
- `_DEPENDENCIES.md` counts do not contradict `Dependencies.csv`.
- Obvious duplicate extracted rows are merged or explicitly justified in `Notes`.

**Tree x DAG integrity checks**
- Parent anchor check:
  - Count rows where `Status=ACTIVE`, `DependencyClass=ANCHOR`, `AnchorType=IMPLEMENTS_NODE`.
  - If count == 0: add `[WARNING] FLOATING_NODE: No parent anchor (IMPLEMENTS_NODE) found.` to Run Notes.
  - If count > 1: add `[WARNING] AMBIGUOUS_ANCHOR: Multiple parent anchors found.` to Run Notes.

If checks fail and cannot be auto-repaired conservatively:
- keep files non-destructively updated,
- add explicit issues to Run Notes,
- set uncertain fields to `TBD`/`UNKNOWN` rather than inventing values.

## Dependency Model: Information Flow Only

**Purpose:** Dependencies capture **information flow / artifact transfer** and **explicit constraints** stated in sources.
They do **not** represent:
- scheduling decisions,
- coordination-only relationships,
- structural decomposition relationships (those belong in the decomposition agent).

**Stages (optional):**
- If stage metadata exists in decomposition, prefer it for interpreting "earlier -> later" transfer.
- If no stage metadata exists, treat the project as a single stage.
- Same-stage dependencies are permitted only when the source states an explicit information/asset transfer (not "we should coordinate").

**What to Extract (high signal):**
- Explicit prerequisites / inputs / approvals required *before* work can proceed
- Deliverable outputs explicitly consumed by another deliverable (handover)
- Explicit interfaces where one deliverable requires specific data/artifacts from another
- Explicit constraints ("shall not proceed until...", "requires approval of...", "requires receipt of...", "must comply with ... as a required input")
- Traceability statements linking deliverable intent to definition nodes and/or requirements

**What NOT to Extract (low signal / out of scope):**
- Pure "coordination" / "keep aligned" statements with no specific data/artifact transfer
- Structural adjacency that is obvious from decomposition (e.g., "Design <-> Turnover" as a package naming convention)
- Scheduling dependencies ("finish-to-start", "start date depends on...") unless explicitly expressed as an input/approval/artifact constraint

**Direction semantics (relative to this deliverable):**
- **UPSTREAM:** This deliverable requires information/asset FROM the target (information flows TO this deliverable)
- **DOWNSTREAM:** This deliverable produces information/asset FOR the target (information flows FROM this deliverable)

## Dependency Lifecycle Model

### Lifecycle phases
1. **DISCOVER** — dependency cues extracted from the deliverable's source documents with evidence.
2. **REGISTER** — rows normalized into `Dependencies.csv` with stable IDs.
3. **VALIDATE** — local quality checks performed against schema/evidence/integrity rules.
4. **CONSUME** — downstream workflows read dependencies for planning/reconciliation/estimating.
5. **REFRESH_OR_RETIRE** — later runs update `LastSeen`; unseen extracted rows become `RETIRED`.

### Lifecycle dimensions (tracked per row)
- **Extraction lifecycle:** `FirstSeen`, `LastSeen`, `Status` (`ACTIVE` or `RETIRED`).
- **Closure lifecycle:** `RequiredMaturity`, `ProposedMaturity`, `SatisfactionStatus`.

`Status` tracks whether the dependency relationship is currently observed in source text.
`SatisfactionStatus` tracks whether the dependency has been fulfilled or remains open.

## Output structure

### Canonical register: `Dependencies.csv` (v3.1 schema)

#### Core columns (required — 29 columns)

`RegisterSchemaVersion`, `DependencyID`, `FromPackageID`, `FromDeliverableID`, `FromDeliverableName`, `DependencyClass`, `AnchorType`, `Direction`, `DependencyType`, `TargetType`, `TargetPackageID`, `TargetDeliverableID`, `TargetRefID`, `TargetName`, `TargetLocation`, `Statement`, `EvidenceFile`, `SourceRef`, `EvidenceQuote`, `Explicitness`, `RequiredMaturity`, `ProposedMaturity`, `SatisfactionStatus`, `Confidence`, `Origin`, `FirstSeen`, `LastSeen`, `Status`, `Notes`

#### Canonical enums (write form)

- `DependencyClass`: `ANCHOR` | `EXECUTION`
- `AnchorType`: `IMPLEMENTS_NODE` | `TRACES_TO_REQUIREMENT` | `NOT_APPLICABLE`
- `Direction`: `UPSTREAM` | `DOWNSTREAM`
- `DependencyType`:
  - Preferred (emit when supported by evidence): `PREREQUISITE` | `INTERFACE` | `HANDOVER` | `CONSTRAINT` | `ENABLES` | `OTHER`
  - Legacy-compatible (do not emit in new extractions): `COORDINATION` | `INFORMATION`
- `TargetType`: `DELIVERABLE` | `PACKAGE` | `WBS_NODE` | `REQUIREMENT` | `DOCUMENT` | `EQUIPMENT` | `EXTERNAL` | `UNKNOWN`
- `Explicitness`: `EXPLICIT` | `IMPLICIT`
- `SatisfactionStatus`: `TBD` | `PENDING` | `IN_PROGRESS` | `SATISFIED` | `WAIVED` | `NOT_APPLICABLE`
- `Confidence`: `HIGH` | `MEDIUM` | `LOW`
- `Origin`: `DECLARED` | `EXTRACTED`
- `Status`: `ACTIVE` | `RETIRED`

Legacy read compatibility:
- `INBOUND`/`OUTBOUND` MAY appear in older files; normalize to `UPSTREAM`/`DOWNSTREAM` on write.
- If `RegisterSchemaVersion` is missing, add it on write and set to `v3.1`.

#### Extension columns (optional; non-breaking)

If you can infer these reliably from text, you MAY add them (do not break older files if absent):

- `EstimateImpactClass` (`BLOCKING|ADVISORY|INFO|TBD`)
- `ConsumerHint` (`TASK_ESTIMATING|AGGREGATION|RECONCILIATION|TBD`)

Rules:
- Do not mark these required.
- Fill conservatively; otherwise omit or use `TBD`.

Estimating-oriented guidance (when `CONSUMER_CONTEXT=TASK_ESTIMATING`):
- You SHOULD attempt to populate `ConsumerHint` and `EstimateImpactClass` for `DependencyClass=EXECUTION` rows **when evidence supports it**.
- Set `ConsumerHint=TASK_ESTIMATING` when the dependency plausibly affects estimating readiness or scope.
- Set `EstimateImpactClass` conservatively:
  - `BLOCKING`: explicit prerequisite/constraint/approval/input that gates meaningful estimating (scope or key quantities unknown without it).
  - `ADVISORY`: interface/handover likely to change quantities/specs or procurement approach, but not a hard gate.
  - `INFO`: informational context; low likelihood of changing totals.
- If unsure, use `TBD` (do not guess).

### `_DEPENDENCIES.md`

Must contain:
- declared upstream/downstream lists (human-owned)
- extracted register summary
- run notes + run history
- lifecycle summary
- downstream handoff notes when a consumer context is provided

## Outputs

- `{deliverable}/Dependencies.csv` — canonical structured register (v3.1 schema, 29 required columns)
- `{deliverable}/_DEPENDENCIES.md` — human-readable index with declared lists, extracted summary, run notes, run history, lifecycle summary

## Non-negotiable constraints

- **Evidence-first.** Each dependency row must cite at least one concrete evidence location (`EvidenceFile` + `SourceRef`) or explicitly state `location TBD`.
- **Do not modify source documents.** Never edit deliverable docs, `_REFERENCES.md`, or decomposition outputs.
- **Writes limited to dependency artifacts only:** `{deliverable}/_DEPENDENCIES.md` and `{deliverable}/Dependencies.csv`.
- **No invention.** If the target cannot be resolved confidently, record `TargetType=UNKNOWN` and preserve the raw reference text.
- **No hierarchy discovery.** This skill does not create or restructure the decomposition Tree; it only anchors to identifiers that already exist.
- **Straight-through.** No human decisions required mid-run; defaults are conservative and logged.
- **Non-destructive updates.** Do not delete rows; retire extracted rows when no longer seen.
- **Epistemic separation.** Distinguish FACT vs ASSUMPTION vs PROPOSAL in `Notes`.
- **Schema discipline.** `Dependencies.csv` must remain parseable and include all 29 canonical required columns.
- **Enum normalization on write.** Normalize legacy variants to canonical enums.
- **Lifecycle hygiene.** Track both extraction lifecycle (`FirstSeen`/`LastSeen`/`Status`) and closure lifecycle (`RequiredMaturity`/`ProposedMaturity`/`SatisfactionStatus`).
- **Referential integrity.** `FromDeliverableID` must match the current deliverable; preserve unresolved targets as `UNKNOWN`/`TBD` rather than guessing.
- **Information flow only.** Do not create edges that are merely "coordination" or "structural adjacency."
- **Two-pass discipline.** ANCHOR pass (Tree) must complete before EXECUTION pass (DAG); do not collapse passes.

## QA expectations

See `QA_CHECKS.md` for the authoritative invariant list. Summary:

- Source documents in scope are not modified.
- `Dependencies.csv` exists (created if missing) and is parseable with all 29 required columns.
- Every ACTIVE row includes `EvidenceFile` and `SourceRef` (or `location TBD`).
- Targets are not invented (`UNKNOWN` permitted).
- Updates are non-destructive (no row deletions; unseen rows `RETIRED`).
- `DependencyID` values are unique within each deliverable register.
- Write-form enums are canonical (legacy `INBOUND`/`OUTBOUND` normalized).
- `_DEPENDENCIES.md` summary/lifecycle counts are consistent with `Dependencies.csv`.
- Non-fatal integrity warnings: `[WARNING] FLOATING_NODE` (no parent anchor), `[WARNING] AMBIGUOUS_ANCHOR` (multiple parent anchors), `[WARNING] MISSING_DECOMPOSITION`.

## Downstream consumer

This skill produces deliverable-local registers only. Downstream workflows (AGGREGATION for project-level graphs, RECONCILIATION for cross-deliverable consistency, TASK_ESTIMATING for estimating readiness, AUDIT_DEP_CLOSURE for closure-level audit via `tools/coordination/analyze_dep_closure.py`) consume these registers. This skill does not build project-level graphs.
