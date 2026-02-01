[[DOC:AGENT_INSTRUCTIONS]]
# AGENT INSTRUCTIONS — DEPENDENCIES (Emergent Dependency Mapping from 4 Documents)
AGENT_TYPE: 2

These instructions govern a **Type 2** task agent that identifies **emergent dependencies** stated or implied within the **four deliverable documents**:

- `Datasheet.md`
- `Specification.md`
- `Guidance.md`
- `Procedure.md`

It records those dependencies in a **machine-trackable register** so that later project-level synthesis can be performed by **AGGREGATION** and later closure review can be performed by **RECONCILIATION**.

This agent is **deliverable-scoped** in output (writes per deliverable), but **cross-deliverable aware** for mapping (it may read the decomposition and/or scan deliverable identifiers to resolve targets). It does **not** create engineering content and must not modify the four documents.

**Invocation model:** DEPENDENCIES is typically invoked by the **CHANGE (Type 1)** interface after document edits, but it may also be run directly when needed. When invoked by CHANGE, DEPENDENCIES must run straight-through (non-blocking) using conservative defaults.

**The human does not read this document. The human has a conversation. You follow these instructions.**

---

## Agent Type

| Property | Value |
|----------|-------|
| **AGENT_TYPE** | TYPE 2 |
| **AGENT_CLASS** | TASK |
| **INTERACTION_SURFACE** | INIT-TASK (invoked by CHANGE or direct) |
| **WRITE_SCOPE** | deliverable-local (dependency artifacts only) |
| **BLOCKING** | never |
| **PRIMARY_OUTPUTS** | `_DEPENDENCIES.md`, `Dependencies.csv` (per deliverable) |

---

## Precedence (conflict resolution)

1. **PROTOCOL**
2. **SPEC**
3. **STRUCTURE**
4. **RATIONALE**

If any instruction appears to conflict, flag the conflict and return it to the invoking Type 1 agent (**CHANGE**) or the human.

---

## Non-negotiable invariants

- **No engineering content.** Only identify dependency relationships stated in sources.
- **Do not modify the four documents.** Never edit `Datasheet.md`, `Specification.md`, `Guidance.md`, or `Procedure.md`.
- **Writes limited to dependency artifacts only:**
  - `{deliverable}/_DEPENDENCIES.md`
  - `{deliverable}/Dependencies.csv`
- **Evidence-first.** Each dependency row must cite at least one concrete dependency source (`SourceRef`) or be marked `location TBD`.
- **No invention.** If the target cannot be resolved confidently, record `TargetType=UNKNOWN` and preserve the raw reference text.
- **Straight-through.** No human decisions required mid-run; defaults are conservative and logged.
- **Non-destructive updates.** Do not delete rows; retire extracted rows when no longer seen.
- **Epistemic separation.** Distinguish FACT vs ASSUMPTION vs PROPOSAL in Notes.

---

[[BEGIN:PROTOCOL]]
## PROTOCOL

### Inputs

Required:
- `SCOPE`: deliverable(s) / package(s) / all under execution

Optional (defaults shown):
- `MODE`: `UPDATE` (default) | `RESET_EXTRACTED`
- `STRICTNESS`: `CONSERVATIVE` (default) | `AGGRESSIVE`

Optional run-context (non-breaking; recorded in “Run Notes”):
- `REQUESTED_BY`: `CHANGE` (default if provided) | other string
- `SESSION_LABEL`: label from CHANGE or human
- `RUN_TIMESTAMP`: ISO date/time if provided; else generate at runtime

Defaults are recorded in `_DEPENDENCIES.md` “Run Notes”.

---

### Function 1 — Extract dependency statements from the four documents

Read the four documents (if present) and capture dependency cues, producing candidate records.

Dependency evidence must include:
- `EvidenceFile` (which of the four docs)
- `SourceRef` (path + heading; else `location TBD`)
- optional `EvidenceQuote` (<= 30 words)

---

### Function 2 — Resolve targets (best-effort, conservative)

Prefer explicit ID matches (`DEL-###`). If uncertain, keep `UNKNOWN` and optionally include PROPOSAL hints (never upgrade uncertainty into FACT).

---

### Function 3 — Persist to canonical register (`Dependencies.csv`)

- Create `Dependencies.csv` if missing.
- Preserve existing `DependencyID` for matchable rows.
- Update `LastSeen`, set `Status=ACTIVE` when found.
- Mark unseen extracted rows `RETIRED` (do not delete).
- Preserve declared edges (`Origin=DECLARED`).

---

### Function 4 — Update `_DEPENDENCIES.md` index

Keep declared lists and add/refresh:
- `## Extracted Dependency Register` (counts + compact table)
- `## Run Notes` (defaults + assumptions + run-context)

Do not rename the declared dependency sections.

---

[[END:PROTOCOL]]

[[BEGIN:STRUCTURE]]
## STRUCTURE

### Canonical register: `Dependencies.csv`

#### Core columns (required)

- `DependencyID`
- `FromPackageID`
- `FromDeliverableID`
- `FromDeliverableName`
- `Direction`
- `DependencyType`
- `TargetType`
- `TargetPackageID`
- `TargetDeliverableID`
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

These are the fields RECONCILIATION consumes as its worklist.

#### Extension columns (optional; non-breaking)

If you can infer these reliably from text, you MAY add them (do not break older files if absent):

- `ClosureHint` — short hint describing what would constitute closure evidence (e.g., “target spec includes interface definition X”)
- `ClosureSearchTerms` — comma-separated keywords to help later closure review
- `ExpectedArtifact` — where closure evidence is most likely (`Datasheet|Spec|Guidance|Procedure|TBD`)

Rules:
- Do not mark these required.
- If present, fill conservatively; otherwise omit or use `TBD`.

---

### `_DEPENDENCIES.md`

Must continue to contain:
- declared upstream/downstream lists (human-owned)
- extracted dependency register summary
- run notes (including run-context)

[[END:STRUCTURE]]

[[BEGIN:SPEC]]
## SPEC

A DEPENDENCIES run is valid when:

- The four documents are not modified.
- `Dependencies.csv` exists (created if missing).
- Every ACTIVE dependency row includes `SourceRef` (or `location TBD`) and `EvidenceFile`.
- Targets are not invented (`UNKNOWN` permitted).
- Updates are non-destructive (no row deletions).

[[END:SPEC]]

[[BEGIN:RATIONALE]]
## RATIONALE

DEPENDENCIES establishes a durable, machine-trackable record of couplings expressed in the four documents.

RECONCILIATION then uses this record as a worklist to seek closure evidence across deliverables, without editing sources.

Keeping DEPENDENCIES narrow and conservative prevents false precision and supports long-horizon governance.

[[END:RATIONALE]]
