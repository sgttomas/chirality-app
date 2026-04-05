---
name: four-documents
description: Draft and iteratively enrich the four-document kit (Datasheet, Specification, Guidance, Procedure) for a PROJECT or SOFTWARE deliverable. Dispatched with RUN_PASSES parameter.
compatibility: Chirality TASK; dispatched by ORCHESTRATOR setup pipeline (Phases 2.2 and 2.5).
metadata:
  chirality-skill-version: "1"
  chirality-task-profile: NONE
---

# SKILL — four-documents

## Purpose

Draft and iteratively enrich the **four deliverable-local documents** for a single `PROJECT_DECOMP` or `SOFTWARE_DECOMP` production unit:

- `Datasheet.md` (descriptive)
- `Specification.md` (normative)
- `Guidance.md` (directional)
- `Procedure.md` (operational)

This skill runs up to three passes within a single invocation, selected by the `RUN_PASSES` brief parameter:

1. **Pass 1** — establish DOMAIN/TASK, generate the four documents grounded in accessible sources.
2. **Pass 2** — cross-reference consistency check; Conflict Table where needed.
3. **Pass 3** — semantic lensing enrichment using `_SEMANTIC_LENSING.md` as a candidate worklist.

The ORCHESTRATOR setup pipeline dispatches this skill twice via TASK:
- **Phase 2.2** with `TaskSkill: four-documents`, `RUN_PASSES: P1_P2` (before `_SEMANTIC_LENSING.md` exists)
- **Phase 2.5** with `TaskSkill: four-documents`, `RUN_PASSES: P3_ONLY` (after the `lens-register` skill produces `_SEMANTIC_LENSING.md`)

A single `FULL` run is supported for ad-hoc re-runs when the lensing register already exists.

**Non-goal:** this skill does NOT modify metadata files other than `_STATUS.md` (safe state update only); it does NOT produce `_SEMANTIC_LENSING.md` (that is the output of `skills/lens-register/`).

## Suitable agent shells

- `TASK` (generic shell mode, no profile)

## Inputs

### Required

- `DELIVERABLE_PATH` — absolute path to one production unit folder
- `DECOMPOSITION_REF` — path to decomposition doc(s) or folder

### Optional

- `RUN_PASSES` — `FULL` (default) | `P1_P2` | `P3_ONLY`
- `ALLOW_OVERWRITE_STATES` — comma-separated `_STATUS.md` states that permit overwrite (default `OPEN, INITIALIZED, SEMANTIC_READY`)
- `OBJECTIVE_ASSOCIATION_MODE` — default `PACKAGE_HEURISTIC`
- `DECOMP_VARIANT` — `PROJECT` (default) | `SOFTWARE`. `DOMAIN` is unsupported and returns `RUN_STATUS=UNSUPPORTED_VARIANT`.

## Runtime overrides

| Key | Meaning | Default | Allowed values |
|---|---|---|---|
| `RUN_PASSES` | Which enrichment passes to run | `FULL` | `FULL`, `P1_P2`, `P3_ONLY` |
| `ALLOW_OVERWRITE_STATES` | `_STATUS.md` states that permit overwrite | `OPEN, INITIALIZED, SEMANTIC_READY` | any subset of valid states |
| `OBJECTIVE_ASSOCIATION_MODE` | How objectives are associated to this deliverable | `PACKAGE_HEURISTIC` | `PACKAGE_HEURISTIC` or explicit mode |
| `DECOMP_VARIANT` | Decomposition variant that produced the deliverable | `PROJECT` | `PROJECT`, `SOFTWARE` (DOMAIN rejected with `UNSUPPORTED_VARIANT`) |

## Tool usage

This is a reasoning-only skill. No deterministic tools are required or allowed (the `allowed-tools` frontmatter is intentionally omitted).

- `tools/scaffolding/write_status.sh` may be invoked during Step 7 to perform the safe `_STATUS.md` update; its invocation is guided operationally, not enforced through the TASK-consumed allowed-tools contract.

Disallowed behavior:
- No writes outside `{DELIVERABLE_PATH}` (except the status helper which writes to the same folder).
- No modifications to `_CONTEXT.md`, `_DEPENDENCIES.md`, `_REFERENCES.md`, `_MEMORY.md`, `_SEMANTIC.md`, `_SEMANTIC_LENSING.md`.
- No cross-deliverable scanning or editing.

## Authority hierarchy (source-grounded drafting)

When drafting or revising content, consult sources in this order of authority:

1. **Authoritative source materials** — locally accessible documents explicitly referenced in `_REFERENCES.md` (standards, specifications, design basis documents, vendor data)
2. **Deliverable-local reference pointers** — `_REFERENCES.md` and `_CONTEXT.md` (scope, identity, constraints)
3. **Decomposition narrative** — the deliverable's entry in the decomposition (context, downstream use, objectives)
4. **Existing drafted files** — prior versions of the four documents (context only, not authority)
5. **`_SEMANTIC_LENSING.md`** — candidate worklist only, never authority

When source material and decomposition narrative disagree, source material is authoritative. Record the discrepancy in the Conflict Table.

Do not treat decomposition summaries, prior draft wording, or generic convention as if they were source material. Do not create requirements, design values, or procedural steps from decomposition prose when the actual source text is locally available.

## Method

### Step 0 — Preconditions & Safety Checks

1. Read `{DELIVERABLE_PATH}/_STATUS.md` (if present) to determine `Current State`.
2. If `Current State` is not in `ALLOW_OVERWRITE_STATES`:
   - Do not overwrite the four documents.
   - Return `RUN_STATUS=SKIPPED_PROTECT_HUMAN_WORK` + the observed state.
3. Interpret `RUN_PASSES`:
   - `FULL` → run Steps 1-7 as written.
   - `P1_P2` → run Steps 1-5 and then Step 7 (status update), skipping Step 6.
   - `P3_ONLY` → run Steps 1 (context read minimal), 6, and final mini consistency sweep (Step 5 table checks), then return; do not run Pass 1 generation.
4. If `DECOMP_VARIANT = DOMAIN`: return `RUN_STATUS=UNSUPPORTED_VARIANT`. This skill produces the standard four-doc set; DOMAIN Knowledge Types require the separate `domain-documents` skill.

**Additional preconditions for `P3_ONLY`:**
- The four docs must already exist in the deliverable folder.
- `{DELIVERABLE_PATH}/_SEMANTIC_LENSING.md` must exist.
If either is missing: return `RUN_STATUS=FAILED_INPUTS` (do not modify files).

### Step 1 — Read Context (always)

**Inputs:**
- Deliverable folder path (`DELIVERABLE_PATH`)
- Decomposition reference (`DECOMPOSITION_REF`)

**Action:**
1. Read `{DELIVERABLE_PATH}/_CONTEXT.md`
   - Extract: deliverable ID, name, package, discipline, type, responsible party, description, anticipated artifacts.
   - Extract: pointer to the decomposition entry (if present).
2. Read the deliverable's entry in the decomposition (`DECOMPOSITION_REF`), using the pointer if available; otherwise locate by deliverable ID.
   - Extract: deliverable narrative context, downstream use hints, any explicit requirements or constraints stated.
3. (Optional) Objectives:
   - If the decomposition includes an **objective-to-deliverable mapping** and it **explicitly lists this deliverable ID**, record those objectives as context.
   - If the mapping is ambiguous at the deliverable-ID level, use the package-grouping heuristic below (PROJECT_DECOMP and SOFTWARE_DECOMP decompositions are package-grouped) and record it as an ASSUMPTION unless the human confirms.
   - If `OBJECTIVE_ASSOCIATION_MODE = PACKAGE_HEURISTIC` (default), apply the original **package-grouping heuristic**:
     - If the decomposition's *Objective-to-Deliverable Mapping* lists **deliverable ranges grouped by parent package**, treat any objective row that mentions this deliverable's **package ID** (e.g., `PKG-014` for PROJECT_DECOMP, `PKG-14` for SOFTWARE_DECOMP) as *directionally relevant context*.
     - Record the association as **ASSUMPTION (best-effort mapping)** and do **not** treat it as a hard requirement unless the human confirms.
4. Read `{DELIVERABLE_PATH}/_REFERENCES.md` to identify reference materials.
5. Read locally accessible reference materials listed in `_REFERENCES.md`. These are the authoritative source set for this deliverable.
   - If `_REFERENCES.md` is absent or lists no sources: return `RUN_STATUS=FAILED_INPUTS` (no authoritative sources to ground in).
   - If NO listed reference materials are locally accessible: return `RUN_STATUS=FAILED_INPUTS` (source fidelity cannot be established without source access).
   - If some references are accessible and others are not: proceed with accessible sources; record inaccessible sources as missing. Content that depends solely on inaccessible sources becomes `TBD`.
   - For each accessible source, read the source slices relevant to this deliverable's scope (see Glossary: source slice).
6. Read `{DELIVERABLE_PATH}/_DEPENDENCIES.md` (best-effort):
   - Use only the **human-declared Upstream/Downstream** lists as constraints (if present).
   - Treat extracted summaries, run notes, and consumer notes as context only (unless supported by evidence sources).

**Output:** Internal understanding of deliverable identity, context, and available sources.

### Step 2 — Establish DOMAIN (Pass 1 only)

- Infer the discipline/domain primarily from `_CONTEXT.md` (discipline/type fields).
- Identify candidate standards/codes only from accessible sources (references and decomposition text).
- If a standard is mentioned but the relevant text is not available, record it as **ASSUMPTION: likely applicable** and do not derive clause-level requirements.

**Default schema sections (keep stable):**

| Document | Default Schema Sections |
|----------|--------------------------|
| Datasheet | Identification, Attributes, Conditions, Construction, References |
| Specification | Scope, Requirements, Standards, Verification, Documentation |
| Guidance | Purpose, Principles, Considerations, Trade-offs, Examples |
| Procedure | Purpose, Prerequisites, Steps, Verification, Records |

You may add sections if the deliverable type requires it, but do not remove the defaults.

### Step 3 — Establish TASK (Pass 1 only)

- Extract subject and constraints from `_CONTEXT.md` and the decomposition entry.
- Extract explicit constraints from accessible references (design limits, code requirements, interface boundaries).
- Extract anticipated artifacts from `_CONTEXT.md`.
- Label all inferences as **ASSUMPTION**.

### Step 4 — Generate Four Documents (Pass 1)

Using DOMAIN + TASK, generate the four documents in `{DELIVERABLE_PATH}`.

**Source-grounding rule:** When authoritative source material is locally accessible, draft content MUST be grounded in the relevant source slices — not only in decomposition summaries, `_CONTEXT.md`, or generic convention. Decomposition scopes and routes; sources determine what the deliverable must say.

**4a: `Datasheet.md`**
- Identification: populate from `_CONTEXT.md`.
- Attributes/Conditions/Construction: populate with values explicitly found in sources.
- References: list sources used.
- Use `TBD` when information is missing; do not invent values.

**4b: `Specification.md`**
- Scope: what the deliverable covers/excludes (from `_CONTEXT.md` and decomposition).
- Requirements: derive only from accessible sources; if a requirement is inferred, label **ASSUMPTION**.
- Standards: list governing standards (with `location TBD` if not accessible).
- Verification: map requirements to verification approaches.
- Documentation: list required artifacts (from anticipated artifacts).

**4c: `Guidance.md`**
- Purpose: why the deliverable exists (decomposition).
- Principles/Considerations/Trade-offs: rationale drawn from sources; otherwise `TBD`.
- Examples: only from sources; otherwise omit or mark `TBD`.
- If contradictions appear, create/update the Conflict Table (see Step 5).

**4d: `Procedure.md`**

**Interpretation rule:** Procedure may describe steps to **produce** the deliverable artifact and/or to **use/operate** it, depending on deliverable type and source availability.

- Prerequisites: include declared upstream dependencies (if present) and required references.
- Steps: derive from specification requirements + deliverable type conventions (use `TBD` where judgment would be needed).
- Verification: checks confirming steps succeeded.
- Records: what evidence/documents should result.

### Step 5 — Cross-Reference Consistency Check (Pass 2)

1. Check cross-document consistency:

| Check | What to Verify |
|-------|----------------|
| Datasheet ↔ Specification | Entities/attributes in Datasheet are reflected in requirements where appropriate |
| Specification ↔ Guidance | Requirements have rationale/considerations where appropriate |
| Specification ↔ Procedure | Requirements have verification hooks in Procedure |
| Terminology | Same terms used consistently across all four documents |
| Values | Numeric values/units consistent across documents |

2. Fix inconsistencies when resolvable from the drafted documents themselves.
3. Re-open authoritative source slices when:
   - values differ across documents and the correct value is not obvious from drafts alone,
   - requirements and verification approaches do not align,
   - guidance rationale appears to overstate what the source supports,
   - procedure steps imply actions not warranted by source,
   - standards or code references may be mismatched or overclaimed.
4. If not resolvable from available info:
   - prefer `TBD` over guessing,
   - add a Conflict Table in `Guidance.md`:

`## Conflict Table (for human ruling)`

Columns:
- Conflict ID
- Conflict (short statement)
- Source A (file + section)
- Source B (file + section)
- Impacted sections
- Proposed authority (PROPOSAL)
- Human ruling (TBD)

### Step 6 — Semantic Lensing Enrichment (Pass 3)

**Purpose:** Apply deliverable-local `_SEMANTIC_LENSING.md` as an enrichment **worklist**.

**Preconditions:**
- If `{DELIVERABLE_PATH}/_SEMANTIC_LENSING.md` exists: run this step.
- If missing:
  - If `RUN_PASSES` is `FULL`: skip lensing, do a final mini consistency sweep, and report the missing lensing file.
  - If `RUN_PASSES` is `P3_ONLY`: treat as `FAILED_INPUTS` and do not modify files.

**Action:**
1. Read `_SEMANTIC_LENSING.md` and treat each row as a **candidate improvement**, not evidence.
2. For every warranted item that would change artifact content, **re-read before changing**:
   - the target document section(s) being modified,
   - the authoritative source slice(s) that the change depends on,
   - sibling document sections implicated by the same topic.
3. Incorporate only when the source slice supports the change. Cite the source (`SourcePath` + `SectionRef`) or explicitly mark `location TBD`.
4. If underlying evidence is unavailable/insufficient:
   - convert to `TBD` or add to the Conflict Table,
   - avoid introducing new "facts."
5. Record evidence of source rereads in the run report: for each substantive change, note which source slice was consulted.

**Completion condition:**
- Each warranted item has been either:
  - incorporated with provenance and source reread evidence, or
  - converted into `TBD`/Conflict Table entries with provenance,
- then perform a final mini consistency sweep (Step 5 checks).

### Step 7 — Update Status (safe update only)

- Read `_STATUS.md` and identify the current state.
- If `RUN_PASSES` includes Pass 1 or Pass 2 (i.e., `FULL` or `P1_P2`):
  - If (and only if) current state is `OPEN`, update: `tools/scaffolding/write_status.sh {DELIVERABLE_PATH} INITIALIZED TASK+four-documents`
- If current state is not `OPEN`, do not modify `_STATUS.md` (no state regression). Report that the status update was skipped.

**Output:** Deliverable folder contains the four documents updated per pass directive, and `_STATUS.md` updated only when safe/applicable.

## Outputs

- `{DELIVERABLE_PATH}/Datasheet.md`
- `{DELIVERABLE_PATH}/Specification.md`
- `{DELIVERABLE_PATH}/Guidance.md`
- `{DELIVERABLE_PATH}/Procedure.md`
- `{DELIVERABLE_PATH}/_STATUS.md` (safe update only: `OPEN → INITIALIZED` when Pass 1/2 ran and state is `OPEN`)

A successful run produces all four documents regardless of pass directive (Pass 3 operates on already-existing drafts).

## Glossary

- **Minimum viable fileset** (seeded by PREPARATION): `_CONTEXT.md`, `_DEPENDENCIES.md`, `_STATUS.md`, `_REFERENCES.md`, `_SEMANTIC.md` (placeholder).
- **Four documents** (produced/overwritten here): `Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md`.
- **DOMAIN**: Domain/disciplined context (discipline, standards, schemas) inferred from folder contents and accessible references.
- **TASK**: The deliverable's subject, constraints, and objectives extracted from `_CONTEXT.md` and the decomposition (with conservative inference rules).
- **Dependency information**: `_DEPENDENCIES.md` is a container that may include (a) human-declared upstream/downstream lists and (b) extracted info-flow summaries. Treat declared lists as constraints; treat extracted summaries as context unless explicitly stated as requirements in evidence sources.
- **Source slice**: the smallest local source region that preserves meaning for a cited claim or requirement. Includes: the cited section or clause, its immediate parent heading (for scope framing), and any embedded tables, acceptance criteria, notes, or exceptions within that section. Adjacent exclusion or applicability material should be included when it qualifies the claim.

## Non-negotiable constraints

- **One deliverable per invocation.** This skill receives one deliverable folder and produces documents for that deliverable only.
- **All four documents, always.** `Datasheet`, `Specification`, `Guidance`, `Procedure` must all exist after a successful run (for the requested pass set).
- **Stable interface.** Do not rename the four documents. Keep default section headings present (you may add sections, but do not remove the defaults).
- **Source-anchored with explicit assumptions.** Non-trivial statements cite sources; if exact location is unknown, cite the source and mark **location TBD**. If inferred, label **ASSUMPTION**.
- **No human input.** Work entirely from the deliverable folder, accessible references, and the decomposition. Do not ask questions or wait for answers.
- **Respect human work.** If `_STATUS.md` indicates a state NOT in `ALLOW_OVERWRITE_STATES`, do not overwrite the four documents; return `SKIPPED_PROTECT_HUMAN_WORK`.
- **Cross-document consistency.** Terminology, entity names, and values must be consistent across all four documents.
- **Do not modify metadata files** created by PREPARATION (`_CONTEXT.md`, `_DEPENDENCIES.md`, `_REFERENCES.md`, `_MEMORY.md`, `_SEMANTIC.md`, `_SEMANTIC_LENSING.md`) except `_STATUS.md` (safe state update only).
- **Decomposition not overstated.** Do not create requirements, design values, or procedural steps from decomposition prose when the actual source text is locally available.
- **Pass 3 source rereads evidenced.** Each substantive Pass 3 change records which source slice was consulted.
- **DOMAIN variant unsupported.** A brief with `DECOMP_VARIANT=DOMAIN` returns `RUN_STATUS=UNSUPPORTED_VARIANT`; DOMAIN Knowledge Types use the separate `domain-documents` skill.

## QA expectations

See `QA_CHECKS.md` for the full invariant + quality gate set. Summary:

- Four docs exist after a successful run.
- Default schema sections present in each document.
- At least one locally accessible source was read from `_REFERENCES.md`.
- Substantive claims source-grounded; missing values marked `TBD`, inferences labeled `ASSUMPTION`.
- Non-trivial values/requirements cite sources (`SourcePath` + `SectionRef` or `location TBD`).
- Cross-document consistency achieved or conflicts captured in the Conflict Table.
- Pass 3 substantive changes record which source slice was consulted.
- `_STATUS.md` only modified per safe-update rules; no state regression.

## Precedence (conflict resolution)

1. **Method** (this file's Step 0-7) governs sequencing and interaction rules.
2. **QA_CHECKS.md** governs validity (pass/fail requirements).
3. **BRIEF_SCHEMA.md** defines the allowed brief fields and enums.
4. **Authority hierarchy** (above) governs interpretation when source ambiguity remains.

If any instruction appears to conflict with the brief from the invoker, do not silently reconcile. Report the conflict.
