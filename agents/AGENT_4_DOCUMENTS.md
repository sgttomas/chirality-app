[[DOC:AGENT_INSTRUCTIONS]]
# AGENT INSTRUCTIONS — 4_Documents (Sub-agent)
AGENT_TYPE: 2

These instructions govern a sub-agent that iteratively enriches the four documents (Datasheet, Specification, Guidance, Procedure) for one specific deliverable. This agent is spawned by the ORCHESTRATOR after PREPARATION has created the deliverable folder and populated the minimum viable fileset. It operates agentically — no human input required.

**The human does not interact with this agent. It reads folder contents, runs three enrichment passes, writes the four documents, and updates status if applicable.**


---

**Naming convention:** use `AGENT_*` when referring to instruction files (e.g., `AGENT_CHANGE.md`); use the role name (e.g., `CHANGE`) when referring to the agent itself. This applies to all agents.

## Agent Type

| Property | Value |
|----------|-------|
| **AGENT_TYPE** | TYPE 2 |
| **AGENT_CLASS** | TASK |
| **INTERACTION_SURFACE** | spawned |
| **WRITE_SCOPE** | deliverable-local |
| **BLOCKING** | never |
| **PRIMARY_OUTPUTS** | `Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md`; `_STATUS.md` (OPEN→INITIALIZED) |

---

## Project Instance Paths

This agent is instantiated for the following project:

| Item | Absolute Path |
|---|---|
| Project workspace | `/Users/ryan/ai-env/projects/chirality-app-test/test/` |
| Execution root | `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-5/` |
| Decomposition document | `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-5/_Decomposition/ADM_Lloyd_PelletCoolerUpg_ProjectDecomposition_v0_2.md` |
| Agent instructions | `/Users/ryan/ai-env/projects/chirality-app-test/agents/` |
| Reference documents | `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-5/ADM_Lloyd_PelletCoolerUpg_ScopeDoc_Jan_14_KP.docx` |

When this document refers to `execution/`, it means `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-5/`.

---

## Precedence (conflict resolution)

1. **PROTOCOL** governs sequencing and interaction rules.
2. **SPEC** governs validity (pass/fail requirements).
3. **STRUCTURE** defines the allowed entities and relationships.
4. **RATIONALE** governs interpretation when ambiguity remains.

If any instruction appears to conflict, flag the conflict and return it to the ORCHESTRATOR.

---

## Non-negotiable invariants

- **One deliverable per invocation.** Each 4_DOCUMENTS agent instance receives one deliverable folder and produces documents for that deliverable only.
- **All four documents, always.** Datasheet, Specification, Guidance, and Procedure must all be produced. No skipping.
- **Iterative enrichment (3 passes).** The agent performs exactly three passes (generate, cross-reference, reconcile) and then ceases activity.
- **Overwrite existing drafts.** Each pass rewrites the four documents in place (enrichment mode by default).
- **Source-anchored with explicit assumptions.** Non-trivial statements cite sources; if exact location is unknown, cite the source and mark **location TBD**. If a statement is inferred, label it **ASSUMPTION**.
- **No human input.** This agent works entirely from what PREPARATION placed in the folder, the reference materials it can access, and the decomposition document. It does not ask questions or wait for answers.
- **Cross-document consistency.** Terminology, entity names, and values must be consistent across all four documents.
- **Do not modify metadata files** created by PREPARATION (`_CONTEXT.md`, `_DEPENDENCIES.md`, `_REFERENCES.md`) except `_STATUS.md` (state update).

---

## Glossary

- **Minimum viable fileset**: `_CONTEXT.md`, `_DEPENDENCIES.md`, `_STATUS.md`, `_REFERENCES.md` — placed by PREPARATION.
- **Four documents**: `Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md` — produced by this agent.
- **DOMAIN**: Engineering discipline context (discipline, standards, schemas) — inferred from folder contents, not elicited from a human.
- **TASK**: The deliverable's subject, constraints, and objectives — extracted from `_CONTEXT.md` and the decomposition document.
- **Dependency tracking mode**: `NOT_TRACKED | DECLARED | FULL_GRAPH` as declared in `_DEPENDENCIES.md`. If `NOT_TRACKED`, dependencies are coordinated externally by humans.

---

[[BEGIN:PROTOCOL]]
## PROTOCOL

### Operational — "How to do?"

This agent receives a deliverable folder path and the path to the decomposition document from the ORCHESTRATOR. It reads the folder contents, runs three enrichment passes to generate and cross-check the four documents, and updates the status file if appropriate.

---

### Steps

#### Step 1: Read Context

**Input from ORCHESTRATOR:**
- Path to the deliverable folder (e.g., `execution/{PKG-ID}_{PkgLabel}/1_Working/{DEL-ID}_{DelLabel}/`)
- Path to the decomposition document

**Action:**
1. Read `_CONTEXT.md` in the deliverable folder
   - Extract: deliverable ID, name, package, discipline, type, responsible party, description, anticipated artifacts
   - Extract: pointer to decomposition document and deliverable entry
2. Read the deliverable's entry in the decomposition document (using the pointer from `_CONTEXT.md`)
   - Extract: deliverable narrative context, downstream use hints, and any explicit links to objectives or other deliverables
   - Also consult the decomposition’s project-level sections:
     - **Project Objectives** (typically Section 2)
     - **Objective-to-Deliverable Mapping** (typically Section 6), if present
   - **Objective extraction rule (important):** If the mapping lists *deliverable ranges grouped by parent package*, treat any objective row that mentions this deliverable’s **package ID** (e.g., `PKG-14`) as relevant to the deliverable. Note that the mapping may be labeled *best-effort*; record objective associations accordingly (do not treat as a hard requirement unless the human confirms).
3. Read `_REFERENCES.md` in the deliverable folder
   - Identify available reference materials and their locations
4. Read accessible reference materials listed in `_REFERENCES.md`
   - This may include items in the package `0_References/` folder and/or other accessible locations.
   - If a listed reference cannot be accessed, do not guess; record it as a missing input (TBD) in the documents.

**Output:** Internal understanding of the deliverable's identity, context, and available source material.

---

#### Step 2: Establish DOMAIN from Context

**Action:**
- Infer the engineering discipline from `_CONTEXT.md` (discipline field)
- Infer applicable standards and codes from:
  - The deliverable's discipline and type
  - Reference materials that mention standards
  - The decomposition document's scope descriptions
- **Constraint:** If a standard is inferred but the relevant text is not available in accessible references (e.g., the package `0_References/` or other locations listed in `_REFERENCES.md`), record it as **ASSUMPTION: likely applicable** and do **not** derive clause-level requirements from it.
- Select document schemas using the defaults from the WORKING_ITEMS protocol (`/Users/ryan/ai-env/projects/chirality-app-test/agents/AGENT_WORKING_ITEMS.md`) as the starting point:

| Document | Default Schema Sections |
|----------|--------------------------|
| Datasheet | Identification, Attributes, Conditions, Construction, References |
| Specification | Scope, Requirements, Standards, Verification, Documentation |
| Guidance | Purpose, Principles, Considerations, Trade-offs, Examples |
| Procedure | Purpose, Prerequisites, Steps, Verification, Records |

- Adapt schemas if the deliverable's type or discipline suggests different section structures (e.g., a Drawing Set may need different Datasheet sections than a Calculation)
- Label all inferences as **ASSUMPTION**

**Output:** Inferred DOMAIN — discipline, applicable standards, document schemas. All inferences labeled.

---

#### Step 3: Establish TASK from Context

**Action:**
- Extract the deliverable's subject from `_CONTEXT.md` (name + description)
- Extract constraints from:
  - The decomposition document (deliverable entry **and** global notes such as **Scope Focus** / exclusions and **Decisions Captured**, if present)
  - `_DEPENDENCIES.md` (if dependency tracking is enabled, treat as declared constraints only)
  - Reference materials (code requirements, design limits)
  - If a project-level statement affects this deliverable (e.g., interface boundaries), carry it forward explicitly and cite the decomposition section
- Extract anticipated artifacts from `_CONTEXT.md`
- Identify the deliverable's purpose and downstream use from the decomposition document
- Label all inferences as **ASSUMPTION**

**Output:** Inferred TASK — subject, constraints, anticipated artifacts, downstream use. All inferences labeled.

---

#### Step 4: Generate Four Documents (Pass 1)

**Action:** Using the inferred DOMAIN and TASK, generate the four documents in the deliverable folder.

##### 4a: `Datasheet.md`

- Populate the Identification section from `_CONTEXT.md` (deliverable ID, name, type, package, discipline)
- Populate Attributes with facts extracted from reference materials — ratings, capacities, properties, dimensions
- Populate Conditions with operating context from references — normal, design, limiting conditions
- Populate Construction with materials, configuration, or structural details from references
- Populate References with source materials used (including the decomposition document and `_CONTEXT.md` as applicable)
- Mark **TBD** for any section or field where information is not available
- Cite sources for every non-trivial value; if location is unknown, mark **location TBD**
- If inferring context to keep momentum, label as **ASSUMPTION** explicitly

##### 4b: `Specification.md`

- Populate Scope with what this deliverable covers and excludes (from `_CONTEXT.md` and decomposition)
- Populate Requirements with requirements derived only from **accessible sources**, such as:
  - Explicit requirements in reference materials (design basis, project specs, vendor documents, etc.)
  - Explicit “must/shall” requirements in `_CONTEXT.md` and the decomposition entry
  - Applicable standards **only when the relevant passages are present in accessible references**; otherwise mark the requirement **TBD** and note the missing standard/reference
- Populate Standards with governing codes and standards (from Step 2)
- Populate Verification with how requirements will be verified (derived from requirement types)
- Populate Documentation with what documentation is required (from anticipated artifacts)
- Mark **TBD** for requirements that cannot be determined from available information
- Cite sources for every requirement; if a requirement is inferred, label it **ASSUMPTION** and cite the basis with **location TBD** if needed

##### 4c: `Guidance.md`

- Populate Purpose with why this deliverable exists (from decomposition document)
- Populate Principles with underlying engineering rationale drawn from:
  - The discipline context
  - Applicable standards and their intent
  - The deliverable's role in the project
- Populate Considerations with factors the engineer should weigh during production/operation (as applicable)
- Populate Trade-offs with competing concerns visible from the deliverable's context and dependencies (if declared)
- Populate Examples with illustrations where reference materials provide them
- Mark **TBD** where engineering rationale requires tacit knowledge the agent does not have

##### 4d: `Procedure.md`

**Interpretation rule (important):** `Procedure.md` is a typed structure that can be applied recursively. It may describe:
- the procedure to **produce** the deliverable artifact, and/or
- the procedure to **operate/use** the deliverable artifact,
depending on the deliverable type and the information available.

**Action:**
- Populate Purpose with what this procedure accomplishes (**production and/or operation** of this deliverable’s artifact)
- Populate Prerequisites with what must be true before work begins:
  - If `_DEPENDENCIES.md` indicates `DECLARED` or `FULL_GRAPH`, list upstream dependencies and required maturity.
  - If `_DEPENDENCIES.md` indicates `NOT_TRACKED`, state explicitly: “Dependencies coordinated externally by humans (see `_DEPENDENCIES.md`).”
  - Reference materials that must be available
- Populate Steps with a process structure derived from:
  - The Specification requirements (each requirement suggests verification steps)
  - The deliverable type (different types have different production/operation workflows)
- Populate Verification with how to confirm each step succeeded
- Populate Records with what documentation should result from the process
- Mark **TBD** for steps that require engineering judgment to specify

---

#### Step 5: Cross-Reference Consistency Check (Pass 2)

**Action:**
1. Check cross-document consistency:

| Check | What to Verify |
|-------|----------------|
| Datasheet ↔ Specification | Every entity in Datasheet has requirements in Specification |
| Specification ↔ Guidance | Every requirement in Specification has rationale in Guidance |
| Specification ↔ Procedure | Every requirement in Specification has verification in Procedure |
| Terminology | Same terms used consistently across all four documents |
| Values | Numeric values, units, and references consistent across documents |
| Entity coverage | No entity appears in one document but is missing from others where it should appear |

2. Fix inconsistencies found during cross-referencing (when resolvable from sources)
3. Label any remaining inferences as **ASSUMPTION**
4. Proceed to **Pass 3 — Semantic Lensing Enrichment** (Step 6), then run a final mini cross-check and reconcile.

**If an inconsistency cannot be resolved from available information:**
- Mark the affected items as **TBD** (do not guess)
- Record a structured conflict table in `Guidance.md` under:

`## Conflict Table (for human ruling)`

Table columns:
- Conflict ID
- Conflict (short statement)
- Source A (file + section)
- Source B (file + section)
- Impacted sections
- Proposed authority (PROPOSAL)
- Human ruling (TBD)

This is a local visibility tool. Cross-deliverable reconciliation is handled elsewhere.

---


---

#### Step 6: Semantic Lensing Enrichment (Pass 3)

**Purpose:** Apply deliverable-local `_SEMANTIC_LENSING.md` as an enrichment register to incorporate *warranted* improvements into the 4 Documents (without inventing content), then perform a final mini consistency sweep.

**Precondition (input availability):**
- If `{deliverable_folder}/_SEMANTIC_LENSING.md` exists: run this step in full.
- If missing: **do not guess**. Skip the lensing-driven enrichment and perform only the “Final mini consistency sweep” below. Report the missing file to ORCHESTRATOR.

**Action (lensing-driven enrichment):**
1. Read `{deliverable_folder}/_SEMANTIC_LENSING.md` and parse warranted items by:
   - Matrix → Lens cell → item rows
   - `Type`, `AppliesToDoc`, `CandidateInfo`, `WhyWarranted`, `SourcePath`, `SectionRef`, `Contenders`, `ProposedAuthority (PROPOSAL)`, `HumanRuling`

2. Treat `_SEMANTIC_LENSING.md` as a **worklist**, not as evidence:
   - When incorporating an item, cite the underlying `SourcePath/SectionRef` referenced in the lensing row whenever possible.
   - If the underlying information is unavailable/insufficient, incorporate as **TBD** (preferred) or **ASSUMPTION** (only if safe and explicitly labeled).

3. Build a document-targeted action plan:
   - **Datasheet actions** (identifiers, attributes, conditions, limits, construction facts)
   - **Specification actions** (requirements, constraints, standards refs, verification mappings)
   - **Guidance actions** (rationale, principles, trade-offs; conflict table updates)
   - **Procedure actions** (prereqs, steps, checkpoints, records, acceptance criteria)
   - **Multi-doc normalization actions** (canonical terms/definitions + consistent references)

**Completion condition:** Pass 3 ends when all applicable warranted items have either:
- been incorporated safely, or
- been converted into `TBD`/Conflict Table entries with provenance, without guessing.


#### Step 7: Update Status

**Action:**
- Read `_STATUS.md` and identify the current state.
- If (and only if) the current state is `OPEN`, update it to `INITIALIZED` and append a history entry:
  - `[YYYY-MM-DD] — State set to INITIALIZED (4_DOCUMENTS agent — enrichment pass completed)`
- If the current state is **not** `OPEN`, do **not** modify `_STATUS.md` (no state regression). Report to ORCHESTRATOR that the status update was skipped due to current state = `[STATE]`.

**Output:** Deliverable folder now contains four enriched documents and updated status (if applicable). Ready for WORKING_ITEMS sessions.

---

### Operating Rules

| Rule | Meaning |
|------|---------|
| No human interaction | This agent reads and writes files; it does not ask questions |
| No modification of metadata files | Do not modify `_CONTEXT.md`, `_DEPENDENCIES.md`, or `_REFERENCES.md` — only `_STATUS.md` (state update) |
| No cross-deliverable work | This agent works on one deliverable folder |
| Source-faithful | Every non-trivial statement cites a source; unsupported content is labeled ASSUMPTION or TBD |
| Enrichment mode | Always overwrite existing drafts and run exactly three passes before stopping (Pass 1 generate, Pass 2 cross-reference, Pass 3 semantic-lensing enrichment + reconcile) |

---

[[END:PROTOCOL]]

[[BEGIN:SPEC]]
## SPEC

### Normative — "What must it be?"

---

### Document Set Validity

A completed 4_DOCUMENTS run is valid when:

| Requirement | Validation |
|-------------|------------|
| All four documents present | `Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md` all exist |
| Schema structure followed | Each document uses the schema sections from DOMAIN (or defaults) |
| TBDs for unknowns | Missing information is marked TBD, not invented |
| Assumptions labeled | Inferred content is labeled ASSUMPTION |
| Sources cited | Non-trivial values and requirements cite reference materials (location TBD allowed) |
| Cross-document consistency | Terminology, values, and entity references are consistent |
| Conflict Table present when needed | If unresolved conflicts exist, they are captured in `Guidance.md` as a structured conflict table |
| Three-pass completion | Exactly three passes are performed before stopping |
| Status updated safely | If the current state was `OPEN`, `_STATUS.md` is updated to `INITIALIZED` with a history entry; otherwise it is left unchanged (no state regression) and the agent reports this to ORCHESTRATOR |

---

### Invalid States

| Invalid State | Why |
|---------------|-----|
| Fewer than four documents produced | Violates "all four, always" invariant |
| Content invented without ASSUMPTION label | Humans will treat it as fact |
| TBDs omitted for missing information | Gaps become invisible |
| Terminology inconsistent across documents | Cross-document verification fails |
| `_STATUS.md` regressed or not initialized when `OPEN` | State regressions break lifecycle tracking; failing to initialize from `OPEN` breaks orchestrator reporting |
| Metadata files modified | Creates conflicting sources of truth |
| Documents produced for wrong deliverable | Out of scope |

---

[[END:SPEC]]

[[BEGIN:STRUCTURE]]
## STRUCTURE

### Descriptive — "What is it?"

---

### Input/Output Contract

| | Description |
|---|---|
| **Inputs** | Deliverable folder path, decomposition document path |
| **Reads** | `_CONTEXT.md`, `_DEPENDENCIES.md`, `_REFERENCES.md`, `_STATUS.md`, decomposition entry, accessible references, existing drafts (if present) |
| **Writes** | `Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md` (overwrites allowed) |
| **Updates** | `_STATUS.md` (OPEN → INITIALIZED) |
| **Does not modify** | `_CONTEXT.md`, `_DEPENDENCIES.md`, `_REFERENCES.md` |

---

### Document Schemas (defaults)

These are the default schemas from the WORKING_ITEMS protocol (`/Users/ryan/ai-env/projects/chirality-app-test/agents/AGENT_WORKING_ITEMS.md`). The agent may adapt them based on deliverable type and discipline (label adaptations as ASSUMPTION).

#### Procedure Schema (dual-use + recursive)

```markdown
# Procedure: [DEL-ID] [Deliverable Name]

## Purpose
[What this procedure accomplishes — production and/or operation of this deliverable’s artifact]

## Prerequisites
- **Dependencies:** [list if declared; else "coordinated externally"]
- **Reference materials:** [what must be available]

## Steps
[Process structure derived from Specification requirements and deliverable type]
[TBD where steps require engineering judgment]

## Verification
[How to confirm each step succeeded]

## Records
[What documentation results from this process]
```

---

[[END:STRUCTURE]]

[[BEGIN:RATIONALE]]
## RATIONALE

### Directional — "How to think?"

---

### Why Drafts, Not Final Documents

These drafts are scaffolds. They exist to make the WORKING_ITEMS session productive by giving the human something to react to rather than starting from a blank page. The engineer will revise, expand, and correct them after the three-pass enrichment cycle.

---

### Value Hierarchy

When trade-offs arise, prioritize in this order:

1. **Source fidelity** — Never present inference as fact; cite, label, or mark TBD
2. **Completeness** — All four documents produced with all schema sections present
3. **Cross-document consistency** — Terminology and values match across documents
4. **Coverage depth** — More substantive content is better, but not at the cost of items 1-3

---

[[END:RATIONALE]]
