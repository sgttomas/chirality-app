---
name: domain-documents
description: Draft knowledge-artifact document set for a DOMAIN Knowledge Type deliverable. Produces KA-* files per the variable artifact schema. DOMAIN pipeline only.
compatibility: Chirality TASK; invoked by DOMAIN_DOCUMENTS wrapper during ORCHESTRATOR setup pipeline for DOMAIN variant.
metadata:
  chirality-skill-version: "1"
  chirality-task-profile: NONE
---

# SKILL — domain-documents

## Purpose

Draft and iteratively enrich a **schema-driven, variable document set** for one DOMAIN Knowledge Type folder. This skill is the DOMAIN replacement for the `four-documents` skill (PROJECT/SOFTWARE), which generates a fixed four-document kit. DOMAIN Knowledge Types instead produce **variable Knowledge Artifacts** whose names and count depend on the topic. The skill derives those artifacts **from decomposition Knowledge Subjects** and grounds them in authoritative source material.

Invariant: each decomposition Knowledge Subject maps to exactly one Knowledge Artifact file.

**Two-layer model:**
- **Knowledge Subject (`SUB-*`)** = the decomposition-layer topic identity inside the Knowledge Type
- **Knowledge Artifact (`KA-*`)** = the document-layer file materialized from exactly one Knowledge Subject
- `Scoping.md` = the Knowledge-Type-level entrypoint that records the `SubjectID -> ArtifactID -> Filename` mapping; it is not itself a Knowledge Subject

**DOMAIN pipeline only.** This skill is NOT called by PROJECT or SOFTWARE variants. The DOMAIN pipeline chain is `PREPARATION → DOMAIN_DOCUMENTS → WORKING_ITEMS` (no CHIRALITY_FRAMEWORK, no CHIRALITY_LENS, no 4_DOCUMENTS). The quality gate is **source fidelity** (does the extraction faithfully represent the authoritative source?), not semantic enrichment.

## Suitable agent shells

- `TASK` (generic shell mode, no profile)

Typical dispatcher: `DOMAIN_DOCUMENTS` wrapper (invoked by ORCHESTRATOR during DOMAIN setup pipeline).

## Inputs

### Required

- `KTY_PATH` — absolute path to one Knowledge Type folder
- `DECOMPOSITION_REF` — path to DOMAIN decomposition folder or doc(s)

### Optional

- `DECOMP_VARIANT` — must be `DOMAIN` (this skill is DOMAIN-only); default `DOMAIN`
- `RUN_PASSES` — `FULL` | `P1_P2` | `P3_ONLY`; default `FULL`
- `ALLOW_OVERWRITE_STATES` — which `_STATUS.md` states permit overwrite; default `OPEN, INITIALIZED`
- `UNIT_SCOPE` — `EXAMPLES_ONLY` | `ALL_MAPPED`; default `EXAMPLES_ONLY`
- `ARTIFACT_NAMING` — `PREFIXED_TYPED_SLUG` | `TYPED_SLUG` | `PREFIXED_SLUG`; default `PREFIXED_TYPED_SLUG`
- `MAX_ARTIFACTS` — hard cap on artifact files; default `25`
- `SOURCES_ROOT` — path to shared source/reference files

## Runtime overrides

| Key | Meaning | Default | Allowed values |
|---|---|---|---|
| `KTY_PATH` | Path to one Knowledge Type folder | **Required** | Absolute directory path |
| `DECOMPOSITION_REF` | Path to DOMAIN decomposition folder or doc(s) | **Required** | Absolute path |
| `DECOMP_VARIANT` | Variant this skill supports | `DOMAIN` | `DOMAIN` only |
| `RUN_PASSES` | Which enrichment passes to run | `FULL` | `FULL`, `P1_P2`, `P3_ONLY` |
| `ALLOW_OVERWRITE_STATES` | Safe-update gate | `OPEN, INITIALIZED` | Comma-separated state list |
| `UNIT_SCOPE` | Which handbook units to use as evidence | `EXAMPLES_ONLY` | `EXAMPLES_ONLY`, `ALL_MAPPED` |
| `ARTIFACT_NAMING` | How to name artifact files | `PREFIXED_TYPED_SLUG` | `PREFIXED_TYPED_SLUG`, `TYPED_SLUG`, `PREFIXED_SLUG` |
| `MAX_ARTIFACTS` | Hard cap on artifact count | `25` | Positive integer |
| `UNIT_SCOPE` values | `EXAMPLES_ONLY` → use `KnowledgeTypes.csv.ExampleUnitIDs`; `ALL_MAPPED` → use all units mapped to this KTY in `DomainLedger.csv` (best-effort) | — | — |
| `ARTIFACT_NAMING` values | `PREFIXED_TYPED_SLUG` → `KA-01_{Type}__{Slug}.md`; `TYPED_SLUG` → `{Type}__{Slug}.md`; `PREFIXED_SLUG` → `KA-01_{Slug}.md` | — | — |

## Tool usage

- No deterministic tools for drafting. This is a reasoning-first extraction + authoring skill.
- Preferred utility script (for safe status updates):
  - `tools/scaffolding/write_status.sh` — update `_STATUS.md` under safe-update rules only.
- The `allowed-tools` frontmatter field is intentionally omitted.

Disallowed behavior:
- No modification of metadata files: `_CONTEXT.md`, `_REFERENCES.md`, `_MEMORY.md`/`MEMORY.md`, `_SEMANTIC.md`.
- No overwriting Knowledge Artifact files when `Current State` is outside `ALLOW_OVERWRITE_STATES`.
- No cross-Knowledge-Type scanning — one Knowledge Type folder per run.
- No fabrication of source excerpts when the source file is inaccessible.

## Outputs

- `Scoping.md` in `{KTY_PATH}` — stable entrypoint with identity, canonical schema, evidence table, artifact plan table, conflict table, source-fidelity log
- Variable `KA-*.md` Knowledge Artifact files in `{KTY_PATH}` (one per Knowledge Subject)
- `_STATUS.md` updated (OPEN → INITIALIZED only when Pass 1/2 ran)

## Authority hierarchy (source-grounded drafting)

When drafting or revising Knowledge Artifact content, consult sources in this order of authority:

1. **Authoritative source material** — original source file(s) referenced by `SourceSpan` in the decomposition and/or listed in `_REFERENCES.md`, located under `{SOURCES_ROOT}` or local `_Sources/`
2. **KTY-local reference pointers** — `_REFERENCES.md` (additional cited sources relevant to this Knowledge Type)
3. **Decomposition data** — `KnowledgeTypes.csv`, `HandbookUnits.csv`, `DomainLedger.csv` (scope, structure, evidence pointers)
4. **Existing drafted files** — prior versions of Knowledge Artifacts and `Scoping.md` (context only, not authority)

When source material and decomposition data disagree, source material is authoritative. Decomposition scopes and routes; source determines what the artifact must say. Record discrepancies in the Conflict Table. Do not treat decomposition summaries, atomic statements, or prior draft wording as if they were the source.

**Source slice:** the smallest local source region that preserves meaning for a cited claim. Includes the cited heading or section, its opening prose, embedded tables or lists, and the immediate parent heading when it frames scope. Adjacent exception or exclusion material should be included when it qualifies the claim.

## Method

### Step 0 — Preconditions & Safety Checks

1. Read `{KTY_PATH}/_STATUS.md` (if present) to determine `Current State`.
2. If `Current State` is not in `ALLOW_OVERWRITE_STATES`:
   - Do not overwrite or create Knowledge Artifact documents.
   - Return `RUN_STATUS=SKIPPED_PROTECT_HUMAN_WORK` + the observed state.
3. Interpret `RUN_PASSES`:
   - `FULL` → run Steps 1–7 as written.
   - `P1_P2` → run Steps 1–5 and then Step 7 (status update).
   - `P3_ONLY` → run Step 1 (full reads including source files), Step 6 (source-fidelity verification), and Step 7; do not re-run Pass 1 drafting.
4. If `DECOMP_VARIANT` is not `DOMAIN`: return `RUN_STATUS=UNSUPPORTED_VARIANT`. This skill is DOMAIN-only; PROJECT/SOFTWARE use the `four-documents` skill.

**Additional preconditions for `P3_ONLY`:**
- At least one Knowledge Artifact `.md` file must already exist in the Knowledge Type folder (non-metadata, not `Scoping.md`).
- The authoritative source file(s) referenced in `_REFERENCES.md` and/or `SourceSpan` fields in the decomposition data must be accessible.
- If either is missing: return `RUN_STATUS=FAILED_INPUTS` (do not modify files).

### Step 1 — Read Context & Decomposition Data (always)

1. Read `{KTY_PATH}/_CONTEXT.md` (best-effort). Extract: KnowledgeType ID, name, parent category, description, decomposition pointer.
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
   - `KnowledgeSubjects` (ordered set driving the artifact plan)
   - `ExampleUnitIDs`
   - `Description`, `IntendedUsers`, `WhenUsed`
   - `ParentCategoryID`, `ParentCategoryName`
5. Read `{KTY_PATH}/_REFERENCES.md` (best-effort) to identify accessible reference materials. Do not dereference URLs. If listed references cannot be accessed, record as missing and treat content as `TBD`.
6. Resolve authoritative source file(s) for this Knowledge Type:
   - Extract `SourceSpan` from the KTY row in `KnowledgeTypes.csv` (format: `{filename}:{startLine}-{startLine} -> {filename}:{endLine}-{endLine}`).
   - Parse the source filename and line ranges.
   - Locate the source file under `{SOURCES_ROOT}` or the path specified in `_REFERENCES.md`.
   - For all passes: read the source file section(s) bounded by `SourceSpan`. If the source file cannot be accessed, return `RUN_STATUS=FAILED_INPUTS` (no pass should proceed without source access).

### Step 2 — Parse Draft Plan (Pass 1 only)

1. Parse `KnowledgeSubjects` for this KTY into an ordered subject list:
   - Each Knowledge Subject represents one discrete domain topic and drives exactly one artifact file.
   - Do not split a single Knowledge Subject across multiple artifact files.
   - Do not merge multiple Knowledge Subjects into one artifact file.
   - Keep ordering stable (use SubjectID order when available).
   - If no Knowledge Subjects are found: create a single fallback artifact spec: `Overview (TBD)`.
2. Parse `ExampleUnitIDs` into a unit list (accept JSON list, Python list string, or semicolon-delimited; best-effort).
3. Build the evidence set based on `UNIT_SCOPE`:
   - `EXAMPLES_ONLY` → use `ExampleUnitIDs`
   - `ALL_MAPPED` → use all `UnitID` values from `DomainLedger.csv` where `KnowledgeTypeID(s)` includes this KTY (best-effort)
4. For each unit in the evidence set, look up in `HandbookUnits.csv`:
   - `AtomicStatement`
   - `SourceRef`
   - If a unit cannot be found: record it as missing and include `TBD` placeholders.
5. Determine the **document archetype** for each artifact:
   - Default: `CanonicalSchema` from the KTY row.
   - Additive "artifact-specific add-ons" (structural only) based on keywords in the Subject name or description:
     - contains `checklist` → add `CHECKLIST_BLOCK`
     - contains `template` or `log` or `form` → add `TEMPLATE_BLOCK`
     - contains `procedure` or `steps` → add `PROCEDURE_BLOCK`
     - contains `glossary` or `terms` → add `REFERENCE_BLOCK`
   - Record any add-ons in `Scoping.md` and the `Decision_Log` section inside `Scoping.md`.
   - Do not treat add-ons as evidence; they are scaffolding conveniences.
6. Determine output filenames using `ARTIFACT_NAMING` policy:
   - `Slug` = filesystem-safe slug from the Knowledge Subject name (letters/numbers/hyphen; collapse whitespace).
   - `Type` = base archetype (`Reference|Guidance|Checklist|Procedure`) from `CanonicalSchema`.
   - If the slug is empty, use `TBD`.
   - Apply a stable ordinal prefix when policy includes `PREFIXED_*`.

**Output:** A deterministic artifact plan: ordered list of `{ArtifactID, SubjectID, SubjectName, BaseType, AddOns, Filename}` plus evidence unit table.
- `SubjectID` is the decomposition-layer identifier.
- `ArtifactID` / `Filename` are the document-layer identifiers derived from that subject.

### Step 3 — Establish Default Section Schemas (Pass 1 only)

**Default schema sections (keep stable):**

| Base Type (`CanonicalSchema`) | Default Schema Sections |
|---|---|
| Reference | Identification, Scope, Definitions, Reference Content, Exceptions/Addenda, References |
| Guidance | Purpose, Applicability, Guidance Statements, Rationale, Examples, References |
| Checklist | Purpose, Applicability, Checklist, Evidence/Records, Notes, References |
| Procedure | Purpose, Prerequisites, Steps, Verification, Records, References |

Sections may be added if the artifact spec requires it, but defaults must not be removed.

**Artifact-specific add-on blocks (structural only):**
- `CHECKLIST_BLOCK` → add a checklist table section
- `TEMPLATE_BLOCK` → add a template/form fields section
- `PROCEDURE_BLOCK` → add a step table section
- `REFERENCE_BLOCK` → add a term/definition table section

Add-ons are **additive** and do not change the base type.

### Step 4 — Generate Documents (Pass 1)

Using the draft plan + evidence set, generate documents in `{KTY_PATH}`.

**Source-grounding rule:** When the authoritative source file is accessible, artifact prose MUST be grounded in the relevant source slices — not only in decomposition summaries, atomic statements, or prior draft wording. Decomposition scopes and structures; the source determines what the artifact must say.

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

1. Title: `# {ArtifactSpec}`
2. Artifact Metadata block:
   - Knowledge Type: ID + Name
   - Category: ID + Name
   - Knowledge Subject: SubjectID + Name (decomposition layer)
   - Artifact ID: `KA-##` (document layer)
   - Base Type: `{Reference|Guidance|Checklist|Procedure}`
   - Add-ons: list (if any)
   - Evidence Units: list (UnitIDs)
3. Default sections for the Base Type (Step 3 table)
4. Populate content **only** from:
   - decomposition fields (`Description`, `IntendedUsers`, `WhenUsed`)
   - `HandbookUnits.csv.AtomicStatement` (and `SourceRef` pointers)
   - accessible references listed in `_REFERENCES.md` (best-effort)
5. Use `TBD` when information is missing; do not invent values.
6. Label inferences as **ASSUMPTION**.
7. If contradictions appear:
   - add a row to `Scoping.md` Conflict Table with evidence pointers,
   - reference the Conflict ID in the affected artifact doc(s).

**Source excerpt rule (optional, best-effort):**
- If the source file referenced in `SourceRef` is accessible under the workspace's sources root, a short excerpt may be included.
- Always include the pointer (`SourceRef`) and never fabricate excerpt text if the source cannot be accessed.

### Step 5 — Cross-Artifact Consistency Check (Pass 2)

**Purpose:** Verify that the generated Scoping.md and Knowledge Artifact files form a coherent, internally consistent document set. This pass reads all generated content; it does not compare against the authoritative source (that is Pass 3).

1. Read every generated artifact file in `{KTY_PATH}` (Scoping.md + all KA-*.md files).
2. **Structural completeness:**
   - Every artifact listed in `Scoping.md` artifact plan table exists as a `.md` file.
   - Every KA-*.md file in the folder appears in the artifact plan table.
   - No duplicate filenames.
   - Each artifact contains all default schema sections for its base type.
3. **Identity consistency:**
   - KTY ID, Name, and Category are consistent across Scoping.md and all artifact metadata blocks.
   - SubjectID ↔ ArtifactID mappings in artifact metadata match the Scoping.md plan table.
4. **Cross-artifact value consistency:**
   - Where multiple artifacts reference the same parameter, design value, equipment tag, or operating condition, verify the values are identical or non-contradictory.
   - Where a value appears in both a "design basis" artifact and a "component detail" artifact, verify agreement.
5. **Evidence traceability:**
   - Every non-trivial claim in an artifact cites a UnitID, SourceRef, or is marked TBD/ASSUMPTION.
   - UnitIDs referenced in artifacts exist in the evidence set table in Scoping.md.
   - SourceRef pointers are syntactically consistent across all docs.
6. **Terminology consistency:**
   - Same terms used consistently across artifacts (prefer VocabularyMap.csv canonical terms if available).
   - Flag synonym drift (e.g., "inlet separator" vs "inlet knock-out drum") as Conflict Table entries unless resolved by VocabularyMap.
7. Fix inconsistencies when resolvable from the generated documents themselves or from the decomposition data.
8. Re-open authoritative source slices when:
   - values differ across artifacts and the correct value is not obvious from drafts alone,
   - identity or terminology inconsistencies cannot be resolved from draft text,
   - claims appear to overstate what the decomposition supports and may need source verification,
   - contradictions between Scoping.md and artifact content cannot be resolved locally.
9. If not resolvable:
   - prefer `TBD` over guessing,
   - add Conflict Table entries in `Scoping.md` with pointers to both artifacts.

### Step 6 — Source-Fidelity Verification (Pass 3)

**Purpose:** Verify and enrich the generated Knowledge Artifacts against the authoritative source document. For DOMAIN Knowledge Types, the source document (e.g., the DBM) is the ground truth — not a semantic lensing register.

> **Design note:** The `four-documents` skill (PROJECT/SOFTWARE) uses semantic enrichment (CHIRALITY_FRAMEWORK → CHIRALITY_LENS → Pass 3 lensing). `domain-documents` does not. Domain Knowledge Types are extracted from a specific authoritative source, so the quality gate is source fidelity: does the extraction faithfully and completely represent the source?

#### 6a) Preconditions
- The authoritative source file must be accessible (resolved in Step 1, item 6).
- At least one Knowledge Artifact `.md` file must exist.
- If the source file cannot be read: return `RUN_STATUS=FAILED_INPUTS`.

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
  - **Source reread evidence:** for each correction or enrichment, record which source slice was re-read before the change was applied
- Update the Conflict Table if source-artifact contradictions require human ruling.

#### 6f) Final structural sweep
After source-fidelity corrections, re-run the Step 5 structural completeness checks (items 1–3) to ensure no artifacts were broken by corrections.

### Step 7 — Update Status (safe update only)

- Read `_STATUS.md` and identify the current state.
- If `RUN_PASSES` includes Pass 1 or Pass 2 (i.e., `FULL` or `P1_P2`):
  - If (and only if) current state is `OPEN`, update: `tools/scaffolding/write_status.sh {kty_folder} INITIALIZED DOMAIN_DOCUMENTS`
- If current state is not `OPEN`, do not modify `_STATUS.md` (no state regression). Report that the status update was skipped.

**Output:** Knowledge Type folder contains `Scoping.md` and the planned Knowledge Artifact documents updated per pass directive, and `_STATUS.md` updated only when safe/applicable.

## Non-negotiable constraints

- **DOMAIN pipeline only.** This skill is invoked exclusively for DOMAIN Knowledge Types. If `DECOMP_VARIANT != DOMAIN`, halt with `UNSUPPORTED_VARIANT`. PROJECT/SOFTWARE variants use the `four-documents` skill.
- **One deliverable per run.** Each invocation processes exactly one Knowledge Type folder (`KTY_PATH`). No cross-Knowledge-Type scanning.
- **No human input.** The skill works from folder contents, references, and decomposition data. The human does not directly interact with this skill.
- **Respect human work.** `_STATUS.md` state must be within `ALLOW_OVERWRITE_STATES` (default: `OPEN, INITIALIZED`) before overwriting any Knowledge Artifact file. Otherwise halt with `SKIPPED_PROTECT_HUMAN_WORK`.
- **No metadata modification.** Never modify `_CONTEXT.md`, `_REFERENCES.md`, `_MEMORY.md`/`MEMORY.md`, or `_SEMANTIC.md`.
- **Subject-to-Artifact bijection.** Each Knowledge Subject maps to exactly one Knowledge Artifact file. No splitting or merging.
- **Variable artifact schema.** The artifact set is topic-dependent (no fixed 4-doc kit). Count and names derive from `KnowledgeSubjects`.
- **`KA-*` naming convention.** Default is `KA-01_{Type}__{Slug}.md`; configurable via `ARTIFACT_NAMING`. Stable ordinal prefix when policy includes `PREFIXED_*`.
- **No invention.** Missing information is `TBD`, inferences are labeled `ASSUMPTION`. Do not fabricate source excerpts when the source is inaccessible.
- **Source fidelity is the quality gate.** Pass 3 verifies artifact-to-source fidelity. No semantic lensing / semantic enrichment in this pipeline.
- **Authoritative source required.** If the source file(s) referenced by `SourceSpan` cannot be accessed, halt with `FAILED_INPUTS` before drafting.
- **Safe-update status only.** `_STATUS.md` transitions `OPEN → INITIALIZED` only when Pass 1/2 ran. Never regress state.
- **No SEMANTIC_READY state.** The DOMAIN lifecycle is `OPEN → INITIALIZED → IN_PROGRESS`; `SEMANTIC_READY` is not a valid state for DOMAIN Knowledge Types.

## QA expectations

See `QA_CHECKS.md` for the full invariant set. Summary:

- `Scoping.md` present with identity, canonical schema, evidence table, artifact plan table, conflict table.
- Every artifact listed in the plan table exists as a `.md` file; every `KA-*.md` file appears in the plan table.
- All default schema sections present per base type.
- Authoritative source file(s) accessed and read.
- Substantive claims grounded in source slices (not only decomposition summaries).
- Missing information marked `TBD`; inferences labeled `ASSUMPTION`; conflicts recorded in Conflict Table.
- Pass 3 (when run): source-fidelity corrections logged in `Source-Fidelity Log` with source reread evidence.
- `_STATUS.md` updated only under safe-update rules.

## See also

- `agents/AGENT_DOMAIN_DOCUMENTS.md` — thin wrapper that dispatches this skill
- `agents/AGENT_DOMAIN_DECOMP.md` — DOMAIN decomposition (upstream; produces KnowledgeSubjects)
- `agents/AGENT_PREPARATION.md` — creates Knowledge Type folders this skill populates
- `skills/four-documents/` — PROJECT/SOFTWARE counterpart (fixed 4-doc kit)
- `tools/EXTERNAL_TOOLS.md` — DOMAIN pipeline overview
- `.Archive/SEMANTIC_PIPELINE_ARCHITECTURE.md` — pipeline architecture context
