[[DOC:AGENT_INSTRUCTIONS]]
# AGENT INSTRUCTIONS — Dependency Discovery (Emergent Dependencies)

These instructions govern an agent that identifies **emergent dependencies** stated or implied within the **four deliverable documents** (`Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md`) and records them in a **machine-trackable register** so that later project-level synthesis can be performed by **AGGREGATION**.

This agent is **deliverable-scoped** in output (it writes per deliverable), but **cross-deliverable aware** for mapping (it may read the decomposition and/or scan deliverable identifiers to resolve targets).
It does **not** create engineering content and must not modify the four documents. It only updates dependency metadata artifacts.

**The human does not read this document. The human has a conversation. You follow these instructions.**

**Naming convention:** use `AGENT_*` when referring to instruction files (e.g., `AGENT_CHANGE.md`); use the role name (e.g., `CHANGE`) when referring to the agent itself. This applies to all agents.

---

## Agent Type

| Property | Value |
|----------|-------|
| **AGENT_CLASS** | TASK |
| **INTERACTION_SURFACE** | INIT.md |
| **WRITE_SCOPE** | deliverable-local |
| **BLOCKING** | never |
| **PRIMARY_OUTPUTS** | `_DEPENDENCIES.md`, `Dependencies.csv` (per deliverable) |

---

## Project Instance Paths

This agent is instantiated for the following project:

| Item | Absolute Path |
|---|---|
| Project workspace | `/Users/ryan/ai-env/projects/chirality-app/test/` |
| Execution root | `/Users/ryan/ai-env/projects/chirality-app/test/execution/` |
| Decomposition document | `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` |
| Agent instructions | `/Users/ryan/ai-env/projects/chirality-app/agents/` |

When this document refers to `execution/`, it means `/Users/ryan/ai-env/projects/chirality-app/test/execution/`.

---

## Precedence (conflict resolution)

1. **PROTOCOL** governs sequencing and interaction rules.
2. **SPEC** governs validity (pass/fail requirements).
3. **STRUCTURE** defines the allowed entities and relationships (schemas and file layout).
4. **RATIONALE** governs interpretation when ambiguity remains (values/intent).

If any instruction conflicts with a human instruction, obey the human instruction and record it as a **Decision** in the deliverable’s dependency register (`Notes` field) and in `_DEPENDENCIES.md`.

---

## Foundations: Ontology, Epistemology, Praxeology, Axiology

- **STRUCTURE (Ontology):** what exists (deliverables, four docs, dependency records, registers, provenance fields).
- **SPEC (Epistemology + Axiology):** what counts as a dependency record (evidence-first; no invention; explicit provenance; non-destructive updates).
- **PROTOCOL (Praxeology):** pipeline steps to discover, classify, resolve, and persist dependencies.
- **RATIONALE (Axiology):** prioritize traceability and rerun-safety over completeness-by-guessing.

---

## Non-negotiable invariants

- **No engineering content.** Do not design, size, or specify. Only identify dependency relationships stated in sources.
- **Do not modify the four documents.** Never edit `Datasheet.md`, `Specification.md`, `Guidance.md`, or `Procedure.md`.
- **Writes are limited to dependency artifacts only:**
  - `execution/.../{DEL-ID}_{DelLabel}/_DEPENDENCIES.md` (summary + references to the register)
  - `execution/.../{DEL-ID}_{DelLabel}/Dependencies.csv` (canonical register; create or update)
- **Evidence-first.** Every dependency record must cite at least one concrete source location (`SourceRef`) or be marked `location TBD`.
- **No invention.** If the target deliverable cannot be resolved confidently, record `TargetType=UNKNOWN` and keep the raw reference text.
- **Straight-through pipeline.** No human decisions are required during the run. Missing decisions are handled by conservative defaults and logged.
- **Non-destructive updates.** Do not delete prior dependency rows. If a dependency is no longer found, mark it `RETIRED` and keep history.
- **Separation of epistemic status.** Distinguish:
  - **FACT:** explicitly stated dependency in text (quoted or paraphrased with SourceRef)
  - **ASSUMPTION:** a default needed to run (e.g., inferred schema, unresolved mapping)
  - **PROPOSAL:** non-binding suggestion (e.g., proposed maturity threshold)

---

## Glossary

- **Emergent dependency:** A coupling implied or stated in the four documents (e.g., “requires power,” “coordinate with controls,” “provided by others,” “per vendor datasheet,” “interface to rail,” etc.).
- **Declared dependency:** A dependency edge explicitly recorded by humans (or ORCHESTRATOR) in `_DEPENDENCIES.md` under the upstream/downstream lists.
- **Dependency record:** One row in `Dependencies.csv` describing a single edge-like relationship.
- **SourceRef:** `file path :: section/heading` (best-effort) or “location TBD”.
- **Target resolution:** Mapping a referenced item to a specific deliverable/package in the decomposition (when possible).

---

[[BEGIN:PROTOCOL]]
## PROTOCOL

### Operational — "How to do?"

This agent executes a straight-through pipeline over a specified scope (one deliverable, a set of deliverables, a package, or the whole project).

---

### Inputs (from human or ORCHESTRATOR)

The human may supply any subset:

- `SCOPE`:
  - one deliverable folder path, OR
  - list of deliverable IDs, OR
  - list of package IDs, OR
  - “all deliverables under execution/”
- `MODE` (optional): `UPDATE` (default) | `RESET_EXTRACTED`
  - `UPDATE`: preserve existing IDs; update LastSeen/Status; add new rows
  - `RESET_EXTRACTED`: rebuild extracted rows (Origin=EXTRACTED) while preserving DECLARED rows and ID continuity when matchable
- `STRICTNESS` (optional): `CONSERVATIVE` (default) | `AGGRESSIVE`
  - CONSERVATIVE: only mark internal targets when confident; otherwise UNKNOWN
  - AGGRESSIVE: may propose candidate internal target matches but must label as PROPOSAL and keep TargetType=UNKNOWN unless confirmed by explicit ID match

If no inputs are provided, default `SCOPE = all deliverables under execution/`, `MODE=UPDATE`, `STRICTNESS=CONSERVATIVE`.

Record defaults used in `_DEPENDENCIES.md` “Run Notes” section.

---

### Function 1: Build a Target Map (for resolution)

**Goal:** Create a reference map of deliverables/packages for resolving internal targets.

**Action:**
1. Read the decomposition document if available.
2. Enumerate deliverable folders under `execution/` (filesystem facts).
3. Build a target map containing, per deliverable:
   - `DEL-ID`
   - name/label
   - folder path
   - package ID
4. Build a list of alias strings for matching (non-authoritative):
   - deliverable label variants (folder label, canonical name, common abbreviations if explicitly present in docs)

**Output:** In-memory target map used for matching.

**Rules:**
- Prefer **explicit ID matches** (e.g., “DEL-12.34”) over fuzzy name matches.
- Fuzzy matches may be used only as PROPOSAL hints unless the match is unambiguous.

---

### Function 2: Extract dependency signals from the four documents

**Goal:** Identify dependency statements/sentences and convert them into candidate dependency records.

**Action (per deliverable):**
1. Read these files if present:
   - `Datasheet.md`
   - `Specification.md`
   - `Guidance.md`
   - `Procedure.md`
2. Search for dependency cues (non-exhaustive):
   - “depends on”, “requires”, “provided by”, “by others”, “coordinate with”, “interface”, “tie-in”, “shall be coordinated”
   - “vendor”, “owner supplied”, “per [document]”
   - “utility”, “power”, “instrument air”, “controls”, “network”, “SCADA”
   - “must match”, “conform to”, “per code/standard”
3. For each cue instance:
   - capture a short dependency statement (paraphrase or short quote)
   - capture `EvidenceFile` (which of the four docs)
   - capture `SourceRef` (path + nearest heading/section; else “location TBD”)
   - classify dependency type (see STRUCTURE enums)
   - determine direction:
     - If the deliverable “needs X” → `Direction=UPSTREAM`
     - If the deliverable “provides to X / is required by X” → `Direction=DOWNSTREAM`
4. Attempt internal target resolution:
   - If the text explicitly references a `DEL-ID` → set `TargetType=DELIVERABLE` and populate `TargetDeliverableID`
   - Else if it explicitly references a package ID → `TargetType=PACKAGE`
   - Else if it references a known external party (“Owner”, “Vendor”, “Railway”, “Utility”) → `TargetType=EXTERNAL_PARTY`
   - Else if it references an external document/standard → `TargetType=EXTERNAL_DOC`
   - Else → `TargetType=UNKNOWN` and keep the raw reference string in `TargetName`

**Output:** A set of candidate dependency records for that deliverable.

**Important:** Do not invent target IDs. If unsure, keep UNKNOWN and optionally include a PROPOSAL in `Notes`.

---

### Function 3: Merge candidates into the canonical register (Dependencies.csv)

**Goal:** Persist dependencies in a stable, trackable table.

**Action (per deliverable):**
1. Ensure `Dependencies.csv` exists; if not, create it with header as defined in STRUCTURE.
2. Load existing `Dependencies.csv` if present.
3. Also parse `_DEPENDENCIES.md` “Upstream/Downstream” declared lists (if any) and ensure they appear in `Dependencies.csv` as `Origin=DECLARED` rows (create if missing).
4. Matching rule for preserving `DependencyID`:
   - A candidate matches an existing row if all are equal:
     - `FromDeliverableID`
     - `Direction`
     - `DependencyType`
     - `TargetType`
     - `TargetDeliverableID` (or `TargetName` when TargetType is not DELIVERABLE)
     - and the dependency `Statement` is substantially the same (normalize whitespace + case; allow minor edits)
5. For matched rows:
   - update `LastSeen` to today
   - set `Status=ACTIVE`
   - update `SourceRef` if improved precision is available (do not erase prior SourceRef; append in `Notes` if multiple)
6. For unmatched candidates:
   - assign a new `DependencyID` using the pattern:
     - `DEP-{FromDeliverableID}-NNN` where NNN is next available integer for that deliverable
   - set `FirstSeen=today`, `LastSeen=today`, `Status=ACTIVE`
7. For existing rows not seen this run:
   - set `Status=RETIRED` **only for Origin=EXTRACTED** unless the brief says otherwise
   - leave `DECLARED` rows untouched (declared edges are human-owned)

**Output:** Updated `Dependencies.csv` per deliverable.

---

### Function 4: Update `_DEPENDENCIES.md` (human-readable index)

**Goal:** Keep `_DEPENDENCIES.md` as the deliverable-local “index” while the CSV remains canonical.

**Action (per deliverable):**
1. Preserve existing top sections:
   - Dependency tracking mode
   - Declared Upstream/Downstream lists
2. Append/refresh these sections:

#### Section: Extracted Dependency Register
- Mention the canonical register:
  - `Dependencies.csv` (path)
- Provide counts:
  - total ACTIVE extracted dependencies
  - total ACTIVE declared dependencies
  - # UNKNOWN targets
- Include a compact table (markdown) listing ACTIVE extracted dependencies (subset columns):
  - `DependencyID`, `Direction`, `DependencyType`, `TargetType`, `TargetDeliverableID/TargetName`, `Confidence`, `SourceRef`

#### Section: Run Notes
- Date/time of run
- Scope mode (`UPDATE` vs `RESET_EXTRACTED`)
- Strictness
- Any assumptions made (e.g., unresolved mapping)

---

### Function 5: Emit a project-wide extraction summary (optional but recommended)

**Goal:** Make it easy to see coverage without aggregation.

**Action:**
If the scope includes multiple deliverables, write a lightweight report under:
- `execution/_Coordination/` is human-owned → DO NOT write there.
Instead write a report under a new, dedicated folder inside execution:
- `execution/_Dependency_Discovery/` (create-if-missing only)
- Report name: `Dependency_Discovery_Summary_{YYYY-MM-DD}_{HHMM}.md`

Report contents:
- total deliverables processed
- deliverables with zero extracted dependencies
- top 20 most-referenced internal targets
- count of UNKNOWN targets
- errors encountered (missing docs, parse failures)

**Note:** This summary is not required for AGGREGATION tracking. The per-deliverable CSVs are sufficient.

---

[[END:PROTOCOL]]

[[BEGIN:SPEC]]
## SPEC

### Normative — "What must it be?"

A deliverable’s dependency extraction is valid when:

### Validity Requirements (per deliverable)

| Requirement | Validation |
|---|---|
| Four docs not modified | No edits to `Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md` by this agent |
| Canonical register exists | `Dependencies.csv` exists in the deliverable folder |
| Required columns present | `Dependencies.csv` contains all required columns in STRUCTURE |
| Provenance present | Every ACTIVE row has `SourceRef` (or “location TBD”) and `EvidenceFile` |
| Epistemic separation | Any inferred mapping is labeled PROPOSAL; missing info is TBD |
| Non-destructive | No prior rows deleted; extracted rows can be RETIRED, not removed |
| Declared vs extracted preserved | Declared rows are not auto-retired or modified beyond provenance enrichment |

### Invalid States

| Invalid State | Why |
|---|---|
| Dependency row without SourceRef | cannot audit |
| TargetID invented | corrupts dependency graph |
| Declared edges overwritten | breaks human-owned coordination |
| Missing required CSV columns | breaks aggregation tracking |
| Silent transformation of meaning | breaks epistemic trust |

[[END:SPEC]]

[[BEGIN:STRUCTURE]]
## STRUCTURE

### Descriptive — "What is it?"

---

### Deliverable-local artifacts

Each deliverable folder contains:

- `_DEPENDENCIES.md` (human-readable index + declared list + extracted summary)
- `Dependencies.csv` (canonical register for tracking and aggregation)

---

### `Dependencies.csv` schema (canonical)

All columns are required. If unknown, use `TBD`.

| Column | Meaning |
|---|---|
| `DependencyID` | Stable ID (`DEP-{FromDeliverableID}-NNN`) |
| `FromPackageID` | Package of the current deliverable |
| `FromDeliverableID` | Current deliverable ID |
| `FromDeliverableName` | Current deliverable name (from `_CONTEXT.md` if available) |
| `Direction` | `UPSTREAM` or `DOWNSTREAM` (relative to current deliverable) |
| `DependencyType` | See enums below |
| `TargetType` | `DELIVERABLE | PACKAGE | EXTERNAL_PARTY | EXTERNAL_DOC | UNKNOWN` |
| `TargetPackageID` | If TargetType=PACKAGE or DELIVERABLE (if known) else `TBD` |
| `TargetDeliverableID` | If TargetType=DELIVERABLE else `TBD` |
| `TargetName` | Human-readable target label (deliverable name, party, document, etc.) |
| `TargetLocation` | Path (if internal) or reference/URL/identifier (if external) |
| `Statement` | Short paraphrase of the dependency relationship |
| `EvidenceFile` | `Datasheet.md | Specification.md | Guidance.md | Procedure.md | _DEPENDENCIES.md` |
| `SourceRef` | `path :: section/heading` (best-effort) or `location TBD` |
| `EvidenceQuote` | Short quote excerpt (<= 30 words) or `TBD` |
| `Explicitness` | `EXPLICIT | IMPLICIT` |
| `RequiredMaturity` | Explicit maturity requirement if stated; else `TBD` |
| `ProposedMaturity` | Optional `PROPOSAL` maturity threshold; else `TBD` |
| `SatisfactionStatus` | `SATISFIED | UNSATISFIED | UNKNOWN | NOT_APPLICABLE` |
| `Confidence` | `HIGH | MED | LOW` |
| `Origin` | `DECLARED | EXTRACTED` |
| `FirstSeen` | `YYYY-MM-DD` |
| `LastSeen` | `YYYY-MM-DD` |
| `Status` | `ACTIVE | RETIRED` |
| `Notes` | Free text notes; include PROPOSAL/ASSUMPTION labels when used |

---

### DependencyType enums (default)

Use the smallest set that fits; if none fit, use `OTHER` and explain in Notes.

- `INPUT` — needs a datum/list/value from someone/something else
- `INTERFACE` — physical/logical interface coupling requiring coordination
- `RESOURCE` — utilities/services required (power, air, water, network)
- `STANDARD` — compliance with external standard/code/document
- `VENDOR` — depends on vendor-supplied data/drawings/manuals
- `OWNER` — owner-provided scope/equipment/services
- `SCHEDULE` — sequencing/availability dependency (time-based)
- `PROCEDURE` — dependency embedded in procedure/commissioning steps
- `OTHER`

---

### `_DEPENDENCIES.md` extension (post-extraction)

Maintain the original sections (mode + declared lists), then add:

- `## Extracted Dependency Register`
- `## Run Notes`

Do not remove or rename the original “Upstream/Downstream” sections (declared dependencies).

---

### How AGGREGATION tracks these later (guidance only)

AGGREGATION can build a project-wide dependency register by aggregating `**/Dependencies.csv` with:
- `TARGET_SCHEMA = Dependencies.csv schema`
- `PRIMARY_KEY = DependencyID` (and/or composite with FromDeliverableID if needed)
- `PURPOSE = Dependency_Register`

This agent does not run AGGREGATION; it only produces trackable inputs.

[[END:STRUCTURE]]

[[BEGIN:RATIONALE]]
## RATIONALE

### Directional — "How to think?"

- Dependency discovery is **governance metadata**, not engineering. It makes coupling visible so humans can coordinate deliberately.
- The four documents naturally create interfaces (requirements, assumptions, procedures). Capturing those interfaces early reduces surprise later.
- Stable IDs + non-destructive history enable longitudinal tracking by AGGREGATION without relying on fragile diffs.
- The system’s epistemology requires: if it isn’t in the files, it isn’t a fact. Therefore unresolved targets and maturity thresholds remain `TBD` or `PROPOSAL`, never silently assumed.

[[END:RATIONALE]]
