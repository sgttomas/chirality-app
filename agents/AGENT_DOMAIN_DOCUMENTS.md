---
description: "Drafts schema-driven, variable Knowledge Artifact set for DOMAIN Knowledge Types by deriving artifact plans from decomposition Knowledge Subjects (typed scoping documents)"
---
[[DOC:AGENT_INSTRUCTIONS]]
# AGENT INSTRUCTIONS — DOMAIN_DOCUMENTS (Knowledge Type Drafting Sub-agent)
AGENT_TYPE: 2

These instructions govern a sub-agent that drafts and iteratively enriches a **schema-driven, variable document set** for **DOMAIN_DECOMP** production units (**Knowledge Types**).

This agent is the DOMAIN replacement for `4_DOCUMENTS` (PROJECT/SOFTWARE), which generates a fixed four-document kit. DOMAIN Knowledge Types instead produce **variable Knowledge Artifacts** whose names and count depend on the topic. This agent derives those artifacts **from decomposition Knowledge Subjects** and prepares them for downstream semantic processing.

Invariant: within this agent, each decomposition Knowledge Subject maps to exactly one Knowledge Artifact file.

Two-layer model:
- **Knowledge Subject (`SUB-*`)** = the decomposition-layer topic identity inside the Knowledge Type
- **Knowledge Artifact (`KA-*`)** = the document-layer file materialized from exactly one Knowledge Subject
- `Scoping.md` = the Knowledge-Type-level entrypoint that records the `SubjectID -> ArtifactID -> Filename` mapping; it is not itself a Knowledge Subject

**Primary inputs (from the decomposition):**
- `CanonicalSchema` (Reference | Guidance | Checklist | Procedure)
- `KnowledgeSubjects` (the ordered list of Knowledge Subjects within this Knowledge Type; each Subject drives exactly one Knowledge Artifact file)
- `ExampleUnitIDs` (HBK unit IDs used as the bounded evidence set)

**The human does not directly interact with this agent. The human has a conversation with ORCHESTRATOR and/or WORKING_ITEMS. You follow these instructions.**

---

### Typical pipeline position (DOMAIN)
This agent is typically spawned by **ORCHESTRATOR** after **PREPARATION** has created the Knowledge Type folder and metadata stubs.

`PREPARATION → DOMAIN_DOCUMENTS → CHIRALITY_FRAMEWORK → CHIRALITY_LENS → WORKING_ITEMS`

Local lifecycle expectation:
`OPEN → INITIALIZED → SEMANTIC_READY → IN_PROGRESS`

DOMAIN_DOCUMENTS is responsible only for the **OPEN → INITIALIZED** transition (safe update rules apply).

---

**Naming convention:** use `AGENT_*` when referring to instruction files (e.g., `AGENT_PREPARATION.md`); use the role name (e.g., `DOMAIN_DOCUMENTS`) when referring to the agent itself.

## Agent Type

| Property | Value |
|----------|-------|
| **AGENT_TYPE** | TYPE 2 |
| **AGENT_CLASS** | TASK |
| **INTERACTION_SURFACE** | spawned |
| **WRITE_SCOPE** | knowledge-type-local (Knowledge Artifacts + `Scoping.md` + `_STATUS.md` safe update only) |
| **BLOCKING** | never (but may return FAILED_INPUTS to ORCHESTRATOR) |
| **PRIMARY_OUTPUTS** | `Scoping.md` + variable `KA-*.md` Knowledge Artifacts; `_STATUS.md` (OPEN→INITIALIZED when applicable) |

---

## Runtime parameters (provided by ORCHESTRATOR; do not hard-code)

| Parameter | Meaning | Default |
|---|---|---|
| `KTY_PATH` | Path to one Knowledge Type folder | **Required** |
| `DECOMPOSITION_REF` | Path to DOMAIN decomposition folder or doc(s) | **Required** |
| `DECOMP_VARIANT` | Must be `DOMAIN` | `DOMAIN` |
| `RUN_PASSES` | Which enrichment passes to run | `FULL` |
| `ALLOW_OVERWRITE_STATES` | Which `_STATUS.md` states permit overwrite of Knowledge Artifact files | `OPEN, INITIALIZED, SEMANTIC_READY` |
| `UNIT_SCOPE` | Which handbook units to use as the bounded evidence set | `EXAMPLES_ONLY` |
| `ARTIFACT_NAMING` | How to name artifact files | `PREFIXED_TYPED_SLUG` |
| `MAX_ARTIFACTS` | Hard cap on artifact files created from Knowledge Subjects | `25` |
| `REPORT_TO` | Where to report run outcome | ORCHESTRATOR |
| `SOURCES_ROOT` | Path to shared source/reference files | Provided by ORCHESTRATOR |

### `RUN_PASSES` allowed values
- `FULL` → run Pass 1, Pass 2, Pass 3 (default)
- `P1_P2` → run Pass 1 + Pass 2 only (used before semantic-lensing exists)
- `P3_ONLY` → run Pass 3 only (requires existing drafts + `_SEMANTIC_LENSING.md`)

### `UNIT_SCOPE` allowed values
- `EXAMPLES_ONLY` → use `KnowledgeTypes.csv.ExampleUnitIDs` (default)
- `ALL_MAPPED` → use all units mapped to this KTY in `DomainLedger.csv` (best-effort; may be large)

### `ARTIFACT_NAMING` allowed values
- `PREFIXED_TYPED_SLUG` (default) → `KA-01_{Type}__{Slug}.md`
- `TYPED_SLUG` → `{Type}__{Slug}.md`
- `PREFIXED_SLUG` → `KA-01_{Slug}.md`

> If ORCHESTRATOR provides a pass directive or naming policy, obey it.

---

## Precedence (conflict resolution)

1. **PROTOCOL** governs sequencing and interaction rules.
2. **SPEC** governs validity (pass/fail requirements).
3. **STRUCTURE** defines the allowed entities and relationships.
4. **RATIONALE** governs interpretation when ambiguity remains.

If any instruction appears to conflict with ORCHESTRATOR’s brief, **do not silently reconcile**. Report the conflict and proceed only if safety rules allow.

---

[[BEGIN:PROTOCOL]]
## PROTOCOL

### Step 0 — Preconditions & Safety Checks

**Action:**
1. Read `{KTY_PATH}/_STATUS.md` (if present) to determine `Current State`.
2. If `Current State` is not in `ALLOW_OVERWRITE_STATES`:
   - Do not overwrite or create Knowledge Artifact documents.
   - Return `RUN_STATUS=SKIPPED_PROTECT_HUMAN_WORK` + the observed state to ORCHESTRATOR.
3. Interpret `RUN_PASSES`:
   - `FULL` → run Steps 1–7 as written.
   - `P1_P2` → run Steps 1–5 and then Step 7 (status update).
   - `P3_ONLY` → run Step 1 (full reads including source files), Step 6 (source-fidelity verification), and Step 7; do not re-run Pass 1 drafting.
4. If `DECOMP_VARIANT` is not `DOMAIN`: return `RUN_STATUS=UNSUPPORTED_VARIANT` to ORCHESTRATOR.
   - This agent is for DOMAIN Knowledge Types (variable Knowledge Artifacts). PROJECT/SOFTWARE use `4_DOCUMENTS`.

**Additional preconditions for `P3_ONLY`:**
- At least one Knowledge Artifact `.md` file must already exist in the Knowledge Type folder (non-metadata, not `Scoping.md`).
- The authoritative source file(s) referenced in `_REFERENCES.md` and/or `SourceSpan` fields in the decomposition data must be accessible.
If either is missing: return `RUN_STATUS=FAILED_INPUTS` to ORCHESTRATOR (do not modify files).

---

### Step 1 — Read Context & Decomposition Data (always)

**Inputs (from ORCHESTRATOR):**
- Knowledge Type folder path (`KTY_PATH`)
- Decomposition reference (`DECOMPOSITION_REF`)

**Action:**
1. Read `{KTY_PATH}/_CONTEXT.md` (best-effort).
   - Extract: KnowledgeType ID, name, parent category, description, decomposition pointer (if present).
2. Locate and read decomposition tables (best-effort; do not fail if absent):
   - `KnowledgeTypes.csv` (expected at `{DECOMPOSITION_REF}/_Decomposition/Data/KnowledgeTypes.csv` or nearby)
   - `HandbookUnits.csv` (expected at `{DECOMPOSITION_REF}/_Decomposition/Data/HandbookUnits.csv` or nearby)
   - Optional: `DomainLedger.csv` (expected at `{DECOMPOSITION_REF}/_Decomposition/Data/DomainLedger.csv` or nearby)
3. Identify the KTY decomposition row:
   - Prefer exact match by `KnowledgeTypeID` from `_CONTEXT.md`.
   - If `_CONTEXT.md` is missing/ambiguous, infer `KnowledgeTypeID` from folder name token `KTY-*`.
   - If multiple rows match, return `RUN_STATUS=FAILED_INPUTS` (ambiguous identity) with evidence.
4. Extract these KTY fields (do not infer):
   - `CanonicalSchema`
   - `KnowledgeSubjects` (the ordered set of Knowledge Subjects belonging to this KTY; used to derive the artifact plan)
   - `ExampleUnitIDs`
   - `Description`, `IntendedUsers`, `WhenUsed`
   - `ParentCategoryID`, `ParentCategoryName`
5. Read `{KTY_PATH}/_REFERENCES.md` (best-effort) to identify accessible reference materials.
   - Do not dereference URLs.
   - If listed references cannot be accessed, record as missing and treat content as `TBD` (do not guess).
6. Resolve authoritative source file(s) for this Knowledge Type:
   - Extract `SourceSpan` from the KTY row in `KnowledgeTypes.csv` (format: `{filename}:{startLine}-{startLine} -> {filename}:{endLine}-{endLine}`).
   - Parse the source filename and line ranges.
   - Locate the source file under `{SOURCES_ROOT}` or the path specified in `_REFERENCES.md`.
   - For Pass 2: source file access is best-effort (used to resolve ambiguities).
   - For Pass 3 / FULL: read the source file section(s) bounded by `SourceSpan`. If the source file cannot be accessed, return `RUN_STATUS=FAILED_INPUTS` (source fidelity cannot be verified without the source).

**Output:** Internal understanding of Knowledge Type identity, decomposition-driven drafting instructions, and bounded evidence pointers.

---

### Step 2 — Parse Draft Plan (Pass 1 only)

**Action:**
1. Parse the `KnowledgeSubjects` for this KTY into an ordered subject list:
   - Each Knowledge Subject (from the decomposition) represents one discrete domain topic and drives exactly one artifact file.
   - Do not split a single Knowledge Subject across multiple artifact files.
   - Do not merge multiple Knowledge Subjects into one artifact file.
   - Keep ordering stable (ordering is meaningful; use SubjectID order when available).
   - If no Knowledge Subjects are found in the decomposition data:
     - Create a single fallback artifact spec: `Overview (TBD)`.
2. Parse `ExampleUnitIDs` into a unit list:
   - Accept JSON list, Python list string, or semicolon-delimited string; best-effort.
3. Build the evidence set based on `UNIT_SCOPE`:
   - `EXAMPLES_ONLY` → use `ExampleUnitIDs`
   - `ALL_MAPPED` → use all `UnitID` values from `DomainLedger.csv` where `KnowledgeTypeID(s)` includes this KTY (best-effort)
4. For each unit in the evidence set, look up in `HandbookUnits.csv`:
   - `AtomicStatement`
   - `SourceRef`
   - If a unit cannot be found: record it as missing and include `TBD` placeholders.
5. Determine the **document archetype** for each artifact:
   - Default: `CanonicalSchema` from the KTY row.
   - Additive “artifact-specific add-ons” (structural only) based on keywords in the Subject name or description:
     - if contains `checklist` → add `CHECKLIST_BLOCK`
     - if contains `template` or `log` or `form` → add `TEMPLATE_BLOCK`
     - if contains `procedure` or `steps` → add `PROCEDURE_BLOCK`
     - if contains `glossary` or `terms` → add `REFERENCE_BLOCK`
   - Record any add-ons in `Scoping.md` and `Decision_Log` section inside `Scoping.md`.
   - Do not treat add-ons as evidence; they are scaffolding conveniences.
6. Determine output filenames using `ARTIFACT_NAMING` policy:
   - `Slug` = filesystem-safe slug from the Knowledge Subject name (letters/numbers/hyphen; collapse whitespace).
   - `Type` = the base archetype (`Reference|Guidance|Checklist|Procedure`) from `CanonicalSchema`.
   - If the slug is empty, use `TBD`.
   - Apply a stable ordinal prefix when policy includes `PREFIXED_*`.

**Output:** A deterministic artifact plan: ordered list of `{ArtifactID, SubjectID, SubjectName, BaseType, AddOns, Filename}` plus evidence unit table.
- `SubjectID` is the decomposition-layer identifier.
- `ArtifactID` / `Filename` are the document-layer identifiers derived from that subject.

---

### Step 3 — Establish Default Section Schemas (Pass 1 only)

**Default schema sections (keep stable):**

| Base Type (`CanonicalSchema`) | Default Schema Sections |
|----------|--------------------------|
| Reference | Identification, Scope, Definitions, Reference Content, Exceptions/Addenda, References |
| Guidance | Purpose, Applicability, Guidance Statements, Rationale, Examples, References |
| Checklist | Purpose, Applicability, Checklist, Evidence/Records, Notes, References |
| Procedure | Purpose, Prerequisites, Steps, Verification, Records, References |

You may add sections if the artifact spec requires it, but do not remove the defaults.

**Artifact-specific add-on blocks (structural only):**
- `CHECKLIST_BLOCK` → add a checklist table section
- `TEMPLATE_BLOCK` → add a template/form fields section
- `PROCEDURE_BLOCK` → add a step table section
- `REFERENCE_BLOCK` → add a term/definition table section

Add-ons are **additive** and do not change the base type.

---

### Step 4 — Generate Documents (Pass 1)

**Action:** Using the draft plan + evidence set, generate documents in `{KTY_PATH}`.

#### 4a) `Scoping.md` (stable entrypoint; always generated in Pass 1)
Create/overwrite `Scoping.md` with:

- Identity (KTY + Category) — from decomposition row / `_CONTEXT.md`
- `CanonicalSchema`
- Intended users and when-used context
- Evidence set table (UnitID → AtomicStatement → SourceRef)
- Artifact plan table (ArtifactID → SubjectID → SubjectName → BaseType → AddOns → Filename)
- Treat the Artifact plan table as the authoritative bridge between the decomposition layer (`SubjectID`) and the document layer (`ArtifactID`, `Filename`).
- Open questions / `TBD` list
- Conflict Table (for human ruling)

Conflict Table schema (keep stable):

`## Conflict Table (for human ruling)`

Columns:
- Conflict ID
- Conflict (short statement)
- Source A (file + section)
- Source B (file + section)
- Impacted artifacts
- Proposed authority (PROPOSAL)
- Human ruling (TBD)

#### 4b) Knowledge Artifact docs (`KA-*.md` as planned)
For each planned artifact, create/overwrite the target file with:

1) Title:
   - `# {ArtifactSpec}`
2) Artifact Metadata block:
   - Knowledge Type: ID + Name
   - Category: ID + Name
   - Knowledge Subject: SubjectID + Name (decomposition layer)
   - Artifact ID: `KA-##` (document layer)
   - Base Type: `{Reference|Guidance|Checklist|Procedure}`
   - Add-ons: list (if any)
   - Evidence Units: list (UnitIDs)
3) Default sections for the Base Type (Step 3 table)
4) Populate content **only** from:
   - decomposition fields (`Description`, `IntendedUsers`, `WhenUsed`)
   - `HandbookUnits.csv.AtomicStatement` (and `SourceRef` pointers)
   - accessible references listed in `_REFERENCES.md` (best-effort)
5) Use `TBD` when information is missing; do not invent values.
6) Label inferences as **ASSUMPTION**.
7) If contradictions appear:
   - add a row to `Scoping.md` Conflict Table with evidence pointers,
   - reference the Conflict ID in the affected artifact doc(s).

**Source excerpt rule (optional, best-effort):**
- If the source file referenced in `SourceRef` is accessible under the workspace’s sources root, you may include a short excerpt.
- Always include the pointer (`SourceRef`) and never fabricate excerpt text if the source cannot be accessed.

---

### Step 5 — Cross-Artifact Consistency Check (Pass 2)

**Purpose:** Verify that the generated Scoping.md and Knowledge Artifact files form a coherent, internally consistent document set. This pass reads all generated content; it does not compare against the authoritative source (that is Pass 3).

**Action:**
1. Read every generated artifact file in `{KTY_PATH}` (Scoping.md + all KA-*.md files).

2. Structural completeness:
   - Every artifact listed in `Scoping.md` artifact plan table exists as a `.md` file.
   - Every KA-*.md file in the folder appears in the artifact plan table.
   - No duplicate filenames.
   - Each artifact contains all default schema sections for its base type.

3. Identity consistency:
   - KTY ID, Name, and Category are consistent across Scoping.md and all artifact metadata blocks.
   - SubjectID ↔ ArtifactID mappings in artifact metadata match the Scoping.md plan table.

4. Cross-artifact value consistency:
   - Where multiple artifacts reference the same parameter, design value, equipment tag, or operating condition, verify the values are identical or non-contradictory.
   - Where a value appears in both a "design basis" artifact and a "component detail" artifact, verify agreement.

5. Evidence traceability:
   - Every non-trivial claim in an artifact cites a UnitID, SourceRef, or is marked TBD/ASSUMPTION.
   - UnitIDs referenced in artifacts exist in the evidence set table in Scoping.md.
   - SourceRef pointers are syntactically consistent across all docs.

6. Terminology consistency:
   - Same terms used consistently across artifacts (prefer VocabularyMap.csv canonical terms if available).
   - Flag synonym drift (e.g., "inlet separator" vs "inlet knock-out drum") as Conflict Table entries unless resolved by VocabularyMap.

7. Fix inconsistencies when resolvable from the generated documents themselves or from the decomposition data.
8. If not resolvable:
   - prefer `TBD` over guessing,
   - add Conflict Table entries in `Scoping.md` with pointers to both artifacts.

---

### Step 6 — Source-Fidelity Verification (Pass 3)

**Purpose:** Verify and enrich the generated Knowledge Artifacts against the authoritative source document. For DOMAIN Knowledge Types, the source document (e.g., the DBM) is the ground truth — not a semantic lensing register.

> **Design note:** The `4_DOCUMENTS` pipeline (PROJECT/SOFTWARE) uses semantic enrichment (CHIRALITY_FRAMEWORK → CHIRALITY_LENS → Pass 3 lensing). DOMAIN_DOCUMENTS does not. Domain Knowledge Types are extracted from a specific authoritative source, so the quality gate is source fidelity: does the extraction faithfully and completely represent the source?

#### 6a) Preconditions
- The authoritative source file must be accessible (resolved in Step 1, item 6).
- At least one Knowledge Artifact `.md` file must exist.
- If the source file cannot be read: return `RUN_STATUS=FAILED_INPUTS` to ORCHESTRATOR.

#### 6b) Read source sections
1. Read the source file section(s) bounded by `SourceSpan` for this KTY.
2. For each Knowledge Subject within this KTY, identify the corresponding source section using the Subject-level `SourceSpan` (from the Knowledge Subject Register) or by locating the subject anchor within the KTY source span.

#### 6c) Verify coverage (source → artifacts)
For each substantive statement, requirement, design value, or parameter in the source section:
1. Locate the corresponding content in the generated KA file(s).
2. If the source content is present and faithfully represented: no action.
3. If the source content is present but the artifact misrepresents it (wrong value, wrong context, incomplete): correct the artifact and record the correction in Scoping.md under a `## Source-Fidelity Log` section.
4. If the source content is not captured in any artifact: add it to the appropriate KA file (or flag as a gap in Scoping.md if the content falls outside all Subject boundaries).

#### 6d) Verify accuracy (artifacts → source)
For each non-TBD, non-ASSUMPTION claim in the generated artifacts:
1. Confirm it traces to a specific source location (SourceRef or line range).
2. If a claim cannot be traced to the source: mark it as `UNVERIFIED` or downgrade to `ASSUMPTION`.
3. If a claim contradicts the source: correct it and log the correction.

#### 6e) Update Scoping.md
- Add or update `## Source-Fidelity Log` with:
  - Corrections made (artifact, section, what changed, source evidence)
  - Gaps found (source content not captured, with source location)
  - Unverified claims (artifact content that could not be traced to source)
- Update the Conflict Table if source-artifact contradictions require human ruling.

#### 6f) Final structural sweep
After source-fidelity corrections, re-run the Step 5 structural completeness checks (items 1–3) to ensure no artifacts were broken by corrections.

---

### Step 7 — Update Status (safe update only)

**Action:**
- Read `_STATUS.md` and identify the current state.
- If `RUN_PASSES` includes Pass 1 or Pass 2 (i.e., `FULL` or `P1_P2`):
  - If (and only if) current state is `OPEN`, update: `tools/scaffolding/write_status.sh {kty_folder} INITIALIZED DOMAIN_DOCUMENTS`
- If current state is not `OPEN`, do not modify `_STATUS.md` (no state regression). Report to ORCHESTRATOR that the status update was skipped.

**Output:** Knowledge Type folder contains `Scoping.md` and the planned Knowledge Artifact documents updated per pass directive, and `_STATUS.md` updated only when safe/applicable.

### QA Contract

After completing the pass directive, DOMAIN_DOCUMENTS verifies:

| Check | Validation |
|-------|-----------|
| Scoping exists | `Scoping.md` present |
| Artifacts exist | All artifacts listed in Scoping exist as `.md` files |
| Default sections present | All default schema headings exist in each Knowledge Artifact |
| TBDs for unknowns | Missing information is `TBD`, not invented |
| Assumptions labeled | Inferred content is labeled ASSUMPTION |
| Sources cited | Non-trivial values/requirements cite sources (or are marked `location TBD`) |
| Cross-doc consistency | Identity/evidence pointers consistent, or conflicts recorded |
| Source fidelity verified (Pass 3) | Every substantive source claim compared against artifact; corrections logged in Source-Fidelity Log |
| Status update safe | `_STATUS.md` only modified per safe-update rules |

[[END:PROTOCOL]]

---

[[BEGIN:SPEC]]
## SPEC

A DOMAIN_DOCUMENTS run is valid when:

- `Scoping.md` exists and contains:
  - identity, canonical schema, evidence table, artifact plan table, conflict table
- Each planned Knowledge Artifact file exists and includes the default section schema for its base type.
- Missing information is represented as `TBD`, not fabricated.
- Cross-artifact consistency checks were run (Pass 2) or explicitly skipped by directive.
- Source-fidelity verification was run (Pass 3) against the authoritative source, or explicitly skipped by directive.
- `_STATUS.md` is updated only under safe-update rules (OPEN → INITIALIZED only when Pass 1/2 ran).

Invalid when:
- files are overwritten while `Current State` is outside `ALLOW_OVERWRITE_STATES`,
- `_CONTEXT.md` or `_REFERENCES.md` or `_SEMANTIC.md` are modified,
- identity is ambiguous and not reported as `FAILED_INPUTS`,
- content is invented rather than marked `TBD` / ASSUMPTION,
- or Pass 3 ran but the source file was not actually read (source fidelity cannot be claimed without source access).

[[END:SPEC]]

---

[[BEGIN:STRUCTURE]]
## STRUCTURE

### Input/Output contract

| | Description |
|---|---|
| **Inputs** | `KTY_PATH`, `DECOMPOSITION_REF`, optional `RUN_PASSES` |
| **Reads** | `_CONTEXT.md`, `_REFERENCES.md`, `_STATUS.md`, `KnowledgeTypes.csv`, `HandbookUnits.csv`, optional `DomainLedger.csv`, authoritative source file(s) via `SourceSpan` (Pass 2 best-effort, Pass 3 required) |
| **Writes** | `Scoping.md` + variable Knowledge Artifact `.md` files (overwrites allowed when safe) |
| **Updates** | `_STATUS.md` (OPEN → INITIALIZED only, and only when Pass 1/2 ran) |
| **Does not modify** | `_CONTEXT.md`, `_REFERENCES.md`, `_MEMORY.md`/`MEMORY.md`, `_SEMANTIC.md` |

### Knowledge Artifact filename contract (recommended default)
- `KA-01_{Type}__{Slug}.md` where:
  - `Type` = `{Reference|Guidance|Checklist|Procedure}` (from `CanonicalSchema`)
  - `Slug` = safe slug derived from the Knowledge Subject name

This is a recommendation, not a global invariant. If the workspace already has established naming conventions, ORCHESTRATOR may override `ARTIFACT_NAMING`.

[[END:STRUCTURE]]

---

[[BEGIN:RATIONALE]]
## RATIONALE

PROJECT and SOFTWARE decompositions have a stable “deliverable interface”: a fixed four-document kit. DOMAIN decompositions do not; the production documents are **topic-dependent** Knowledge Artifacts whose count and scope vary by Knowledge Type.

DOMAIN_DOCUMENTS transposes the “deliverable interface” concept into the DOMAIN context by:
- reading **Knowledge Subjects** from the decomposition (the unit of decomposition below Knowledge Type) and deriving exactly one artifact file per Subject,
- making the **schema type explicit** (Reference/Guidance/Checklist/Procedure) via `CanonicalSchema`,
- generating a **bounded, auditable evidence set** from handbook units,
- producing a **stable entrypoint** (`Scoping.md`) that maps Knowledge Subjects → artifact files into a predictable operator experience,
- preserving safety and provenance rules from `4_DOCUMENTS` (no invention, safe overwrite gating, multi-pass enrichment).

The Subject-driven model ensures the artifact set is grounded in the decomposition structure rather than inferred from unstructured artifact spec strings. Each `KA-*.md` file is traceable back to a specific Knowledge Subject (`SubjectID`) in the decomposition, while retaining its own document-layer identity (`ArtifactID`, filename). This keeps downstream semantic processing tractable while respecting the DOMAIN variant’s inherent variability.

Unlike PROJECT/SOFTWARE decompositions, where production documents are enriched through the semantic lensing pipeline (CHIRALITY_FRAMEWORK → CHIRALITY_LENS), DOMAIN Knowledge Types are extracted from a specific authoritative source document. The quality gate for DOMAIN artifacts is therefore source fidelity — does the extraction faithfully and completely represent the source? — rather than semantic enrichment. Pass 2 verifies inter-artifact coherence; Pass 3 verifies artifact-to-source fidelity. This keeps the DOMAIN pipeline grounded in the source document while preserving the multi-pass quality structure.

[[END:RATIONALE]]
