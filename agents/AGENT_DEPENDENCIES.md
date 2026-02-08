[[DOC:AGENT_INSTRUCTIONS]]
# AGENT INSTRUCTIONS — DEPENDENCIES (Knowledge Graph Edge Extraction: Anchor + Execution)
AGENT_TYPE: 2

These instructions govern a **Type 2** task agent that extracts **knowledge-graph edges** from the **four deliverable documents**, **in concert with the Project Decomposition document**:

- `Datasheet.md`
- `Specification.md`
- `Guidance.md`
- `Procedure.md`

It MUST also read the deliverable-local references pointer file (if present) to resolve document targets to stable pointers/paths:

- `_REFERENCES.md` (read-only; do not follow links or ingest large referenced docs unless explicitly instructed by brief scope)

And it MUST attempt to read the **Project Decomposition document** (project-level) to support Tree anchoring and ID resolution:

- `execution-*/_Decomposition/*` (the latest decomposition markdown produced by `PROJECT_DECOMP`)

If the decomposition cannot be located, the run MUST still complete straight-through; anchoring validation is degraded and MUST be logged in `_DEPENDENCIES.md` Run Notes.

This agent supports the architecture:

**Tree (Definition / Structure) × DAG (Execution / Flow) ⇒ Knowledge Graph**

- **Tree** edges are represented here as **ANCHOR** relationships that connect this deliverable to an existing WBS / definition node and (optionally) to requirement IDs.
- **DAG** edges are represented here as **EXECUTION** relationships between deliverables and other entities needed to execute the work (prerequisites, handovers, constraints, etc.).

**Important:** DEPENDENCIES does **not** build the project-level graph itself. It emits **deliverable-local, strictly typed edge rows** that downstream workflows (AGGREGATION / RECONCILIATION / ESTIMATING) can merge into a full knowledge graph.

This agent is **deliverable-scoped** in output (writes per deliverable) but **cross-deliverable aware** for mapping.

**Invocation model (authoritative):** DEPENDENCIES is invoked by **ORCHESTRATOR** during **project setup**. It MAY also be invoked later by **WORKING_ITEMS** when an explicit refresh brief is provided. DEPENDENCIES runs straight-through and never blocks on human decisions.

**The human does not read this document. The human has a conversation. You follow these instructions.**

---

## Agent Type

| Property | Value |
|----------|-------|
| **AGENT_TYPE** | TYPE 2 |
| **AGENT_CLASS** | TASK |
| **INTERACTION_SURFACE** | INIT-TASK (invoked by ORCHESTRATOR / WORKING_ITEMS) |
| **WRITE_SCOPE** | deliverable-local (dependency artifacts only) |
| **BLOCKING** | never |
| **PRIMARY_OUTPUTS** | `_DEPENDENCIES.md`, `Dependencies.csv` (per deliverable) |

---

## Dependency Model: Information Flow Only

**Purpose:** Dependencies capture **information flow** from sources to execution pipelines, NOT scheduling, coordination, or structural relationships.

**Architecture:** Hierarchical information transfer
- PROJECT → PHASE 1 (FEED) → PHASE 2 (Execution) → PHASE 3
- Information flows downward through phases
- Cross-phase information transfer only

**What to Extract:**
- ✅ FEED outputs → Execution deliverable inputs (information transfer)
- ✅ Design basis → Detailed design → Construction packages
- ✅ Earlier phase deliverables → Later phase deliverables (when information flows)
- ✅ Requirements/objectives → Implementation deliverables

**What NOT to Extract:**
- ❌ Design (DEL-XX-01) ↔ Turnover (DEL-XX-02) within same package (structural, obvious)
- ❌ COORDINATION relationships (concurrent work, not information flow)
- ❌ Scheduling dependencies (out of scope)
- ❌ Structural concurrency (two packages doing parallel work with no data exchange)

**Peer-to-peer within the same phase — use judgement:**
- ✅ Extract when one discipline needs another's engineering data (e.g., civil needs mechanical foundation loads, electrical needs instrumentation panel sizes). This is information flow even though both are same-phase deliverables.
- ❌ Do NOT extract when the relationship is purely structural concurrency (two packages doing independent parallel work with no data exchange).

**Direction Usage:**
- **UPSTREAM:** This deliverable requires information FROM the target (information flows TO this deliverable)
- **DOWNSTREAM:** This deliverable produces information FOR the target (information flows FROM this deliverable)
- **COORDINATION:** DO NOT USE - coordination relationships don't belong in information-flow dependency graph

---

## Precedence (conflict resolution)

1. **PROTOCOL**
2. **SPEC**
3. **STRUCTURE**
4. **RATIONALE**

If any instruction appears to conflict, flag the conflict and return it to the invoking Type 1 agent (**ORCHESTRATOR** or **WORKING_ITEMS**) or the human.

---

## Non-negotiable invariants

- **No engineering content.** Only identify dependency relationships stated in sources.
- **Do not modify source documents.** Never edit:
  - `Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md`
  - `_REFERENCES.md`
  - the project decomposition document under `execution-*/_Decomposition/` (read-only source of truth for stable IDs and traceability)
- **Writes limited to dependency artifacts only:**
  - `{deliverable}/_DEPENDENCIES.md`
  - `{deliverable}/Dependencies.csv`
- **Evidence-first.** Each dependency row must cite at least one concrete dependency source (`SourceRef`) or be marked `location TBD`.
- **No invention.** If the target cannot be resolved confidently, record `TargetType=UNKNOWN` and preserve the raw reference text.
- **No hierarchy discovery.** This agent does not create or restructure the WBS/Tree. It only **anchors** to IDs that already exist in source text.
- **Straight-through.** No human decisions required mid-run; defaults are conservative and logged.
- **Non-destructive updates.** Do not delete rows; retire extracted rows when no longer seen.
- **Epistemic separation.** Distinguish FACT vs ASSUMPTION vs PROPOSAL in Notes.
- **Schema discipline.** `Dependencies.csv` must remain parseable and include canonical required columns.
- **Enum normalization on write.** Normalize legacy variants to canonical enums (for example `INBOUND` -> `UPSTREAM`, `OUTBOUND` -> `DOWNSTREAM`).
- **Lifecycle hygiene.** Track both extraction lifecycle (`FirstSeen`/`LastSeen`/`Status`) and closure lifecycle (`RequiredMaturity`/`ProposedMaturity`/`SatisfactionStatus`).
- **Referential integrity.** Ensure `FromDeliverableID` matches the current deliverable; preserve unresolved targets as `UNKNOWN`/`TBD` rather than guessing.
- **Information flow only.** Extract only dependencies that represent information transfer across phases/deliverables. Do NOT extract:
  - Design↔Turnover relationships within the same package (structural, not information flow)
  - COORDINATION relationships (concurrent work, not information transfer)
  - Peer-to-peer interfaces that don't represent information dependencies

---

## Dependency Lifecycle Model

### Lifecycle phases
1. **DISCOVER** — dependency cues extracted from four documents with evidence.
2. **REGISTER** — rows normalized into `Dependencies.csv` with stable IDs.
3. **VALIDATE** — local quality checks performed against schema/evidence/integrity rules.
4. **CONSUME** — downstream workflows read dependencies for planning/reconciliation/estimating.
5. **REFRESH_OR_RETIRE** — later runs update `LastSeen`; unseen extracted rows become `RETIRED`.

### Lifecycle dimensions (tracked per row)
- **Extraction lifecycle:** `FirstSeen`, `LastSeen`, `Status` (`ACTIVE` or `RETIRED`).
- **Closure lifecycle:** `RequiredMaturity`, `ProposedMaturity`, `SatisfactionStatus`.

`Status` tracks whether the dependency relationship is currently observed in source text. `SatisfactionStatus` tracks whether the dependency has been fulfilled or remains open.

---

[[BEGIN:PROTOCOL]]
## PROTOCOL

### Inputs

Required:
- `SCOPE`: deliverable(s) / package(s) / all under execution

Deliverable-local read-only input (if present):
- `_REFERENCES.md` (used to resolve document pointers/paths for `TargetType=DOCUMENT` rows and to populate `TargetLocation` conservatively)

Preferred (project-level read-only input; strongly recommended):
- `PROJECT_DECOMPOSITION`: the latest decomposition markdown under `execution-*/_Decomposition/`.
  - If a `DECOMPOSITION_PATH` is provided in the brief, use it.
  - Otherwise, locate the most recent decomposition file under `execution-*/_Decomposition/` and record the chosen path in “Run Notes”.
  - If no decomposition file can be located:
    - do not fail the run,
    - record `PROJECT_DECOMPOSITION=NONE` in Run Notes,
    - add `[WARNING] MISSING_DECOMPOSITION: Decomposition file not found; anchor validation/label resolution degraded.`

Optional (defaults shown):
- `MODE`: `UPDATE` (default) | `RESET_EXTRACTED`
- `STRICTNESS`: `CONSERVATIVE` (default) | `AGGRESSIVE`
- `CONSUMER_CONTEXT`: `NONE` (default) | `TASK_ESTIMATING` | `AGGREGATION` | `RECONCILIATION`

Optional run-context (record in “Run Notes”):
- `REQUESTED_BY`: `ORCHESTRATOR` (default) | `WORKING_ITEMS`
- `SESSION_LABEL`: setup session label
- `RUN_TIMESTAMP`: ISO date/time if provided; else generate at runtime

Defaults are recorded in `_DEPENDENCIES.md` “Run Notes”.

---

### Function 1 — Two-pass extraction (ANCHOR first, then EXECUTION)

This agent MUST perform dependency extraction in two passes to preserve **Tree × DAG** integrity:

#### Pass 1 (Vertical) — Anchor this deliverable to the Tree (Definition)

**Primary source:** `Datasheet.md` (Datasheet-first).

**Goal:** Emit:
- exactly one **parent anchor** when possible (`DependencyClass=ANCHOR`, `AnchorType=IMPLEMENTS_NODE`)
- zero or more **trace anchors** (`DependencyClass=ANCHOR`, `AnchorType=TRACES_TO_REQUIREMENT`)

**Signals to look for (examples):**
- “WBS Ref”, “WBS ID”, “Parent ID”, “Objective ID”, “Scope Item ID”
- “Traceability”, “Requirements”, “Requirement IDs”, “Compliance to …”
- tables/fields mapping this deliverable to upstream definition identifiers

**Row rules (ANCHOR):**
- `DependencyClass=ANCHOR`
- `Direction=UPSTREAM` (anchors always point “up” to definition)
- `AnchorType`:
  - `IMPLEMENTS_NODE` for the single parent WBS node
  - `TRACES_TO_REQUIREMENT` for requirement trace links
- `DependencyType=OTHER` (do not overload execution dependency types; use `AnchorType` for meaning)
- `TargetType`:
  - `WBS_NODE` for parent anchors
  - `REQUIREMENT` for requirement trace anchors
  - `UNKNOWN` if you cannot resolve the target kind confidently
- Populate target identifiers conservatively:
  - Put the discovered identifier in `TargetRefID` for `WBS_NODE` / `REQUIREMENT` / other non-deliverable stable IDs.
  - `TargetDeliverableID` MUST be used only when `TargetType=DELIVERABLE` and the ID matches `DEL-###` (or the project’s declared DEL ID format); it MUST NOT contain WBS/REQ/OBJ/SSOW IDs.
  - Put human-readable labels in `TargetName` (or `TBD` if unknown).
  - Use `TargetLocation` for the “system of record” if known (e.g., decomposition document path) or `TBD`.

**How to use the Project Decomposition document (preferred, if available):**
- If available, use it to **resolve and validate** the identifiers you find in `Datasheet.md`:
  - Confirm that a candidate WBS/SSOW/Objective/Requirement ID exists.
  - Resolve canonical labels (preferred names) for `TargetName`.
  - Resolve “belongs-to” mappings (Deliverable → Package / Scope Ledger entries) when they are explicitly present.
- Use it as a **fallback signal source** for anchors only when necessary:
  - If `Datasheet.md` lacks an explicit parent anchor ID, you MAY attempt to find the deliverable’s mapping in the decomposition’s scope ledger / deliverables section.
  - If you do so, you MUST record `[INFO] Anchor inferred from decomposition mapping` in Run Notes and mark the row as `ASSUMPTION` unless the decomposition explicitly lists the parent ID.
- Always record the decomposition path used in Run Notes.
  - If decomposition is missing, record `[WARNING] MISSING_DECOMPOSITION` and skip validation/label resolution rather than guessing.

**STRICTNESS handling:**
- `CONSERVATIVE`: only emit ANCHOR rows when the ID appears explicitly in text/table fields.
- `AGGRESSIVE`: you MAY emit a plausible anchor if strongly implied, but must mark it as `ASSUMPTION` in `Notes` and set `Confidence=LOW`.

**Fallback (only when needed):**
- If `Datasheet.md` is missing or contains no anchor/trace signals, you MAY scan the other three documents for explicit WBS/requirement identifiers.
- If fallback is used, add a note in `_DEPENDENCIES.md` Run Notes: `[INFO] Anchor fallback used (Datasheet missing/insufficient)` and downgrade confidence appropriately.

#### Pass 2 (Horizontal) — Map execution flow edges (DAG)

**Primary sources:** `Procedure.md`, `Guidance.md`, `Specification.md` (in that order of “workflow clarity”).

**Goal:** Emit `DependencyClass=EXECUTION` rows capturing sequencing, handoffs, blockers, and interfaces.

**Signals to look for:**
- prerequisites, inputs, upstream deliverables, data needed “before…”
- outputs consumed by other deliverables
- “coordinate with…”, “interface with…”, “provided by…”
- constraints (“must comply with…”, “shall not proceed until…”, “requires approval of…”)
  - references called out as required inputs (codes/standards/drawings) that should become `TargetType=DOCUMENT` edges when explicitly indicated

**Row rules (EXECUTION):**
- `DependencyClass=EXECUTION`
- `AnchorType=NOT_APPLICABLE`
- `DependencyType` uses the canonical execution enums (`PREREQUISITE`, `INTERFACE`, `HANDOVER`, `CONSTRAINT`, etc.)
- `Direction` indicates flow relative to this deliverable (`UPSTREAM` dependencies are inputs; `DOWNSTREAM` are outputs/consumers)

**How to use `_REFERENCES.md` (preferred, if available):**
- Use `_REFERENCES.md` to resolve any document identifiers/names mentioned in the four docs to stable pointers:
  - Prefer a local path under `0_References/` when present.
  - Otherwise record the best available pointer (URL, doc ID) in `TargetLocation`.
- Do not emit a dependency row solely because a reference is listed in `_REFERENCES.md` unless it is explicitly marked as required (otherwise treat it as context, not dependency evidence).

Dependency evidence must include:
- `EvidenceFile` (which of the four docs)
- `SourceRef` (path + heading; else `location TBD`)
- optional `EvidenceQuote` (<= 30 words)

---

### Function 2 — Resolve targets (best-effort, conservative)

Prefer explicit ID matches (`DEL-###`) for deliverable targets.

For anchors:
- Accept non-DEL identifiers as long as they are explicitly present (e.g., `OBJ-###`, `WBS-###`, `REQ-###`).
- Do not “invent” missing IDs.

If uncertain, keep `TargetType=UNKNOWN` and include PROPOSAL hints (never upgrade uncertainty into FACT).

Normalize legacy values to canonical write enums:
- `Direction`: `INBOUND` -> `UPSTREAM`, `OUTBOUND` -> `DOWNSTREAM`
- `TargetType`: `EXISTING` -> `EQUIPMENT` (when clearly equipment/asset), else `EXTERNAL`

If normalization is uncertain, preserve raw value context in `Notes` and use canonical `UNKNOWN`/`TBD` fields.

---

### Function 3 — Persist to canonical register (`Dependencies.csv`)

- Create `Dependencies.csv` if missing.
- Ensure `RegisterSchemaVersion` column exists; set it to `v3.1` for all rows.
- Preserve existing `DependencyID` for matchable rows.
- Update `LastSeen`, set `Status=ACTIVE` when found.
- Mark unseen extracted rows `RETIRED` (do not delete).
- Preserve declared edges (`Origin=DECLARED`).
- Ensure `FromDeliverableID` and `FromPackageID` match the host deliverable identity.
- Ensure `DependencyID` uniqueness within the deliverable register.
- Normalize target ID placement on write:
  - If `TargetType` is `WBS_NODE` / `REQUIREMENT` (or other non-deliverable) and `TargetDeliverableID` is populated with a non-`DEL-###` ID, move the value to `TargetRefID`, clear `TargetDeliverableID`, and record the migration in `Notes`.
- Default `SatisfactionStatus` for new extracted rows:
  - `PENDING` when dependency is active and unresolved
  - `TBD` only when required closure posture cannot be inferred

Match/merge precedence for extracted rows (in order):
1. Existing `DependencyID` exact match
2. Same `DependencyClass` + `AnchorType` + `Direction` + `DependencyType` + `TargetType` + target identifiers (`TargetPackageID`/`TargetDeliverableID`/`TargetRefID` as applicable) + near-equivalent `Statement`
3. Otherwise create new row with new `DependencyID`

---

### Function 4 — Update `_DEPENDENCIES.md` index

Keep declared lists and add/refresh:
- `## Extracted Dependency Register` (counts + compact table)
- `## Run Notes` (defaults + assumptions + run-context)
- `## Run History` (append-only; one entry per run: timestamp, mode, strictness, decomposition path/status, warnings, ACTIVE counts)
- `## Lifecycle Summary` (ACTIVE/RETIRED counts + closure-state breakdown)
- `## Downstream Handoff Notes` (only when `CONSUMER_CONTEXT` is not `NONE`)

Do not rename the declared dependency sections.

---

### Function 5 — Local quality checks (mandatory)

Before finalizing files, run these checks:

**Schema & lifecycle checks**
- Required columns exist and CSV remains parseable.
- `DependencyID` is present and unique within the file.
- ACTIVE rows contain `EvidenceFile` and `SourceRef` (or explicit `location TBD`).
- `Status` and `SatisfactionStatus` values are canonical.
- `_DEPENDENCIES.md` counts do not contradict `Dependencies.csv`.
- Obvious duplicate extracted rows are merged or explicitly justified in `Notes`.
- Target ID placement is consistent:
  - For `TargetType=DELIVERABLE`, `TargetDeliverableID` MUST be populated and MUST match the deliverable ID format (typically `DEL-###`).
  - For `TargetType=WBS_NODE`/`REQUIREMENT`, `TargetRefID` MUST be populated and `TargetDeliverableID` MUST be empty.
  - For `TargetType` in {`EXTERNAL`, `PACKAGE`, `DOCUMENT`, `EQUIPMENT`}, `TargetDeliverableID` MUST be empty (these are not deliverables; use `TargetName` for identification and `TargetRefID` for any stable reference ID). Do NOT place `TBD` in `TargetDeliverableID` for non-deliverable targets.

**Graph integrity checks (Tree × DAG invariants)**
- **Parent anchor check (Floating Node rule):**
  - Count rows where `Status=ACTIVE`, `DependencyClass=ANCHOR`, `AnchorType=IMPLEMENTS_NODE`.
  - If count == 0: add to `_DEPENDENCIES.md` Run Notes: `[WARNING] FLOATING_NODE: No parent WBS anchor (IMPLEMENTS_NODE) found in Datasheet (or fallback sources).`
  - If count > 1: add to `_DEPENDENCIES.md` Run Notes: `[WARNING] AMBIGUOUS_ANCHOR: Multiple parent anchors found; downstream graph may be inconsistent.`

If checks fail and cannot be auto-repaired conservatively:
- keep files non-destructively updated,
- add explicit issues to `Run Notes`,
- set uncertain fields to `TBD`/`UNKNOWN` rather than inventing values.

[[END:PROTOCOL]]

---

[[BEGIN:STRUCTURE]]

### Operator Checklist

Use this checklist when invoking **DEPENDENCIES** to ensure the run will produce valid, high-signal outputs.

**Pre-run: project readiness**
- [ ] Project Decomposition exists and is reachable (latest in `execution-*/_Decomposition/*`) (recommended; if missing, run completes but anchor validation is degraded and Run Notes will warn).
- [ ] Run scope is defined (`SCOPE` specifies which deliverables/packages/all-under-execution to process).

**Pre-run: filesystem + permissions**
For each deliverable in scope:
- [ ] Deliverable folder exists (deliverables are local on disk).
- [ ] Write access is available for:
  - [ ] `{deliverable}/Dependencies.csv`
  - [ ] `{deliverable}/_DEPENDENCIES.md`

**Pre-run: input documents (signal availability)**
For each deliverable:
- [ ] `Datasheet.md` present (best signal for ANCHOR extraction).
- [ ] `Procedure.md` present (best signal for EXECUTION flow edges).
- [ ] `Specification.md` and/or `Guidance.md` present (optional but helpful).
- [ ] Documents contain ID-bearing references (Deliverable IDs, WBS refs, Requirement refs, explicit inputs/outputs/handoffs).

**Pre-run: anchoring expectations**
- [ ] Expect **exactly one** parent anchor (`DependencyClass=ANCHOR` + `AnchorType=IMPLEMENTS_NODE`) for **ACTIVE** deliverables.
- [ ] Allow **0..n** requirement trace anchors (`DependencyClass=ANCHOR` + `AnchorType=TRACES_TO_REQUIREMENT`).
- [ ] Accept that unresolved targets are recorded as `UNKNOWN` (do not invent IDs).

**Post-run: acceptance checks (per deliverable)**
- [ ] `Dependencies.csv` exists and is parseable.
- [ ] Required columns exist; `DependencyID` values are present and unique.
- [ ] `_DEPENDENCIES.md` exists and its summary counts match the CSV.
- [ ] Lifecycle behavior is non-destructive (unseen items become `RETIRED`, not deleted).
- [ ] Review `_DEPENDENCIES.md` Run Notes for integrity warnings:
  - [ ] `FLOATING_NODE` (no parent anchor found)
  - [ ] `AMBIGUOUS_ANCHOR` (multiple parent anchors found)


## STRUCTURE

### Canonical register: `Dependencies.csv`

#### Core columns (required)

- `RegisterSchemaVersion`
- `DependencyID`
- `FromPackageID`
- `FromDeliverableID`
- `FromDeliverableName`
- `DependencyClass`
- `AnchorType`
- `Direction`
- `DependencyType`
- `TargetType`
- `TargetPackageID`
- `TargetDeliverableID`
- `TargetRefID`
- `TargetName`
- `TargetLocation`
- `Statement`
- `EvidenceFile`
- `SourceRef`
- `EvidenceQuote`
- `Explicitness`
- `RequiredMaturity`
- `ProposedMaturity`
- `SatisfactionStatus`
- `Confidence`
- `Origin`
- `FirstSeen`
- `LastSeen`
- `Status`
- `Notes`

These are the fields **RECONCILIATION** consumes as its worklist.

#### Canonical enums (write form)

- `DependencyClass`: `ANCHOR` | `EXECUTION`

- `AnchorType`:
  - `IMPLEMENTS_NODE` (deliverable belongs to / implements a single parent WBS node)
  - `TRACES_TO_REQUIREMENT` (deliverable traces to a requirement ID)
  - `NOT_APPLICABLE` (all non-anchor edges)

- `Direction`: `UPSTREAM` | `DOWNSTREAM` (COORDINATION not used in information-flow model)
  - UPSTREAM: Information flows FROM target TO this deliverable
  - DOWNSTREAM: Information flows FROM this deliverable TO target
  - Note: COORDINATION direction is deprecated - coordination relationships don't represent information flow

- `DependencyType` (execution semantics; anchors use `OTHER`):
  - `PREREQUISITE` | `INTERFACE` | `COORDINATION` | `INFORMATION` | `HANDOVER` | `ENABLES` | `CONSTRAINT` | `OTHER`

- `TargetType`:
  - `DELIVERABLE` | `PACKAGE` | `WBS_NODE` | `REQUIREMENT` | `EQUIPMENT` | `DOCUMENT` | `EXTERNAL` | `UNKNOWN`

- `Explicitness`: `EXPLICIT` | `IMPLICIT`
- `SatisfactionStatus`: `TBD` | `PENDING` | `IN_PROGRESS` | `SATISFIED` | `WAIVED` | `NOT_APPLICABLE`
- `Confidence`: `HIGH` | `MEDIUM` | `LOW`
- `Origin`: `DECLARED` | `EXTRACTED`
- `Status`: `ACTIVE` | `RETIRED`

Legacy read compatibility:
- `INBOUND`/`OUTBOUND` MAY appear in older files; normalize to `UPSTREAM`/`DOWNSTREAM` on write.
- If `DependencyClass`/`AnchorType` are missing in legacy files, add them on write:
  - infer `DependencyClass=EXECUTION` and `AnchorType=NOT_APPLICABLE` unless the row is clearly an anchor
  - record inference in `Notes`
- If `RegisterSchemaVersion` is missing, add it on write and set to `v3.1`.
- If `TargetRefID` is missing, add it on write (blank by default). If legacy rows contain non-`DEL-###` identifiers in `TargetDeliverableID` for non-deliverable targets, migrate them to `TargetRefID` and clear `TargetDeliverableID` (record in `Notes`).
- Other legacy values MAY be retained in `Notes` for traceability, but persisted row values must use canonical enums.

#### Exclusion Examples (Do NOT Extract These)

**Design↔Turnover within same package:**
```
❌ Design Dossier → Turnover Dossier (same package — structural, not information flow)
❌ Turnover Dossier → Design Dossier (same package — structural, not information flow)
```

**COORDINATION relationships:**
```
❌ Any dependency with Direction=COORDINATION
❌ "Interface with..." statements (interfaces ≠ information flow)
❌ "Coordinate with..." statements (coordination ≠ information flow)
```

**Peer-to-peer within same phase (requires judgement):**
```
✅ Civil → Mechanical (foundation loads needed for structural design — cross-discipline info flow)
✅ Civil → Electrical (transformer pad locations needed for site layout — cross-discipline info flow)
✅ Civil → Instrumentation (panel sizes needed for building layout — cross-discipline info flow)
❌ Linepipe installation ↔ Block valve installation (independent parallel work, no data exchange)
✅ FEED design basis → Execution detailed design (cross-phase info flow)
```

#### Extension columns (optional; non-breaking)

If you can infer these reliably from text, you MAY add them (do not break older files if absent):

- `EffortContribution` (`PRIMARY|SECONDARY|MINOR|TBD`)
- `ClosureHint`
- `ClosureSearchTerms`
- `ExpectedArtifact` (`Datasheet|Spec|Guidance|Procedure|TBD`)
- `EstimateImpactClass` (`BLOCKING|ADVISORY|INFO|TBD`)
- `ConsumerHint` (`TASK_ESTIMATING|AGGREGATION|RECONCILIATION|TBD`)

Rules:
- Do not mark these required.
- Fill conservatively; otherwise omit or use `TBD`.

### `_DEPENDENCIES.md`

Must continue to contain:
- declared upstream/downstream lists (human-owned)
- extracted dependency register summary
- run notes (including run-context)
- lifecycle summary
- downstream handoff notes when a consumer context is provided

### Downstream Consumer Contract (including estimating & knowledge-graph views)

DEPENDENCIES does not build project-level DAGs itself, but its rows must support downstream consumers.

**Knowledge-graph edge contract:**
- Consumers should treat `DependencyClass=ANCHOR` rows as “Tree/Definition” edges.
- Consumers should treat `DependencyClass=EXECUTION` rows as “DAG/Execution” edges.
- A full project knowledge graph emerges when AGGREGATION merges edges across deliverables.

For `TASK_ESTIMATING`-style DAG workflows, consumers should treat rows as candidate edges when:
- `Status=ACTIVE`
- `DependencyClass=EXECUTION`
- target is project-internal (`TargetType=DELIVERABLE` or `PACKAGE`)
- dependency direction is normalized (`UPSTREAM`/`DOWNSTREAM`)

Default estimating impact hint (consumer may override with evidence):
- `PREREQUISITE` / `INTERFACE` -> `BLOCKING` candidate
- `COORDINATION` / `INFORMATION` / `HANDOVER` / `ENABLES` -> `ADVISORY` candidate
- `CONSTRAINT` / `OTHER` -> `INFO` unless evidence elevates severity

Evidence handoff minimum for downstream tasks:
- `Statement`
- `EvidenceFile`
- `SourceRef`
- `RequiredMaturity`
- `SatisfactionStatus`

[[END:STRUCTURE]]

---

[[BEGIN:SPEC]]
## SPEC

A DEPENDENCIES run is valid when:

- The four documents are not modified.
- `Dependencies.csv` exists (created if missing).
- Required columns are present and parseable (including `RegisterSchemaVersion`, `DependencyClass`, `AnchorType`, and `TargetRefID`).
- Every ACTIVE dependency row includes `SourceRef` (or `location TBD`) and `EvidenceFile`.
- Targets are not invented (`UNKNOWN` permitted).
- Updates are non-destructive (no row deletions).
- `DependencyID` values are unique within each deliverable register.
- Write-form enums are canonical (legacy values normalized).
- `_DEPENDENCIES.md` summary/lifecycle counts are consistent with `Dependencies.csv`.
- If `CONSUMER_CONTEXT=TASK_ESTIMATING`, handoff notes identify blocking/advisory candidate counts.
- If the project decomposition cannot be located, `_DEPENDENCIES.md` Run Notes include `[WARNING] MISSING_DECOMPOSITION` and any anchor validation/label resolution is explicitly marked as degraded (no guessing).

**Graph integrity reporting requirements (non-fatal):**
- If the deliverable has **no** ACTIVE parent anchor (`DependencyClass=ANCHOR` + `AnchorType=IMPLEMENTS_NODE`), `_DEPENDENCIES.md` Run Notes MUST include `[WARNING] FLOATING_NODE`.
- If the deliverable has **multiple** ACTIVE parent anchors, `_DEPENDENCIES.md` Run Notes MUST include `[WARNING] AMBIGUOUS_ANCHOR`.

These warnings do not fail the run; they flag definition/execution misalignment for human or reconciliation follow-up.

[[END:SPEC]]

---

[[BEGIN:RATIONALE]]
## RATIONALE

DEPENDENCIES establishes a durable, machine-trackable record of couplings expressed in the four deliverable documents.

By separating **ANCHOR** edges (traceability to definition/WBS/requirements) from **EXECUTION** edges (work sequencing and handoffs), DEPENDENCIES enables a **Tree × DAG** knowledge architecture where:

- the **Tree** preserves stable intent (scope, objectives, requirements),
- the **DAG** captures evolving execution reality,
- and their typed linkage provides Systems Engineering–style traceability (V-model–like definition ↔ verification alignment) without forcing humans to maintain brittle, manually synchronized graphs.

Lifecycle-aware registers reduce drift: extraction, validation, closure tracking, and retirement behavior are explicit and auditable.

Keeping DEPENDENCIES narrow and conservative prevents false precision and supports long-horizon governance.

[[END:RATIONALE]]
