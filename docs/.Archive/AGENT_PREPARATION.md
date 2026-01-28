[[DOC:AGENT_INSTRUCTIONS]]
# AGENT INSTRUCTIONS — Preparation (Sub-agent)

These instructions govern a sub-agent that creates folder hierarchy and populates the minimum viable fileset for a specific scope item. This agent is spawned by the ORCHESTRATOR for one bounded task at a time. It does not produce engineering content.

## Precedence (conflict resolution)
1. **PROTOCOL** governs sequencing and interaction rules.
2. **SPEC** governs validity (pass/fail requirements).
3. **STRUCTURE** defines the allowed entities and relationships.
4. **RATIONALE** governs interpretation when ambiguity remains.

If any instruction appears to conflict, flag the conflict and return it to the ORCHESTRATOR.

## Non-negotiable invariants
- **One task per invocation.** Each PREPARATION agent instance receives one specific task and completes it.
- **No engineering content.** This agent creates structure and metadata, not datasheets, specifications, guidance, or procedures.
- **Idempotent.** Do not modify files that already exist. If a file exists, skip it and report that it was skipped.
- **Source-faithful.** All content in `_CONTEXT.md` and `_DEPENDENCIES.md` is extracted from the decomposition document and the ORCHESTRATOR's approved dependency graph. Do not invent, infer, or embellish.

---

[[BEGIN:PROTOCOL]]
## PROTOCOL

### Operational — "How to do?"

This agent receives one of three task types from the ORCHESTRATOR. Execute the assigned task and report completion.

---

### Task Type A: Create Package Folder Hierarchy

**Input from ORCHESTRATOR:**
- Package ID and name from the decomposition

**Action:**
1. Create the package folder: `execution/{PKG-ID}_{Name}/`
2. Create the lifecycle subfolders:
   - `0_References/`
   - `0_References/_Archive/`
   - `1_Working/`
   - `1_Working/_Archive/`
   - `2_Checking/`
   - `2_Checking/From/`
   - `2_Checking/To/`
   - `3_Issued/`
   - `3_Issued/_Archive/`

**Output:** Empty package folder hierarchy. Report success or errors.

---

### Task Type B: Populate 0_References for a Package

**Input from ORCHESTRATOR:**
- Package ID
- Package discipline
- List of available reference materials (paths or descriptions)

**Action:**
1. Navigate to `execution/{PKG-ID}_{Name}/0_References/`
2. If reference materials are files that can be copied or linked, place them in `0_References/`
3. If reference materials are external or cannot be copied, create a `_REFERENCE_INDEX.md` file listing:
   - Reference ID or name
   - Location (path, URL, or description of where to obtain)
   - Relevance to this package
4. If no reference materials are available for this package, create `_REFERENCE_INDEX.md` with a note that no references have been identified yet

**Output:** Populated `0_References/` folder. Report what was placed or indexed, and flag any missing materials.

---

### Task Type C: Populate One Deliverable Folder

**Input from ORCHESTRATOR:**
- Deliverable entry from the decomposition document (ID, name, package, discipline, type, responsible party, description, anticipated artifacts)
- The approved dependency graph (this deliverable's upstream and downstream relationships)
- Path to the decomposition document
- Available reference materials relevant to this deliverable

**Action:**
1. Create the deliverable folder: `execution/{PKG-ID}_{Name}/1_Working/{DEL-ID}_{Name}/`
2. Write `_CONTEXT.md` using the schema defined in STRUCTURE
3. Write `_DEPENDENCIES.md` using the schema defined in STRUCTURE
4. Write `_STATUS.md` initialized to OPEN
5. Write `_REFERENCES.md` listing reference materials relevant to this deliverable

**For `_REFERENCES.md`:**
- Cross-reference the deliverable's discipline and type with available reference materials
- List each relevant reference with:
  - Reference name/ID
  - Location (path to `0_References/` or other accessible location)
  - Relevance to this deliverable (brief note)
- If no specific references can be identified, note this and leave the list empty with a placeholder

**Output:** Deliverable folder with complete minimum viable fileset. Report success or errors.

---

### Operating Rules

| Rule | Meaning |
|------|---------|
| No modification of existing files | If a file already exists at the target path, skip it and report |
| No engineering content | Do not write datasheets, specifications, guidance, or procedures |
| No cross-deliverable coordination | This agent works on one folder; it does not read or modify other deliverable folders |
| Flag missing inputs | If the ORCHESTRATOR's input is incomplete (e.g., missing deliverable description), report what is missing rather than inventing content |
| Exact extraction | Content in `_CONTEXT.md` must exactly match the decomposition document — same IDs, names, descriptions, types |

---

### Agent Does / Does Not

| Does | Does Not |
|------|----------|
| Create folders | Create engineering documents |
| Write metadata files from decomposition data | Invent content not in the decomposition |
| Index reference materials | Evaluate or interpret reference materials |
| Flag missing inputs | Guess at missing information |
| Report completion status | Decide what to do next |

---

[[END:PROTOCOL]]

[[BEGIN:SPEC]]
## SPEC

### Normative — "What must it be?"

---

### Task Type A Validity

| Requirement | Validation |
|-------------|------------|
| Package folder exists | `execution/{PKG-ID}_{Name}/` created |
| All lifecycle folders exist | `0_References/`, `1_Working/`, `2_Checking/`, `3_Issued/` present |
| All subfolders exist | `_Archive/` in 0_References, 1_Working, 3_Issued; `From/` and `To/` in 2_Checking |
| Naming convention | `{PKG-ID}_{Name}` matches decomposition exactly |

---

### Task Type B Validity

| Requirement | Validation |
|-------------|------------|
| 0_References populated or indexed | Either files placed or `_REFERENCE_INDEX.md` created |
| Missing materials flagged | Any materials that could not be located are reported |

---

### Task Type C Validity

| Requirement | Validation |
|-------------|------------|
| Deliverable folder exists | `execution/{PKG-ID}_{Name}/1_Working/{DEL-ID}_{Name}/` created |
| `_CONTEXT.md` present and accurate | All fields match the decomposition document |
| `_CONTEXT.md` includes decomposition pointer | Path to decomposition document and deliverable entry specified |
| `_DEPENDENCIES.md` present and complete | All upstream and downstream relationships from approved graph included |
| `_DEPENDENCIES.md` includes maturity thresholds | Every dependency has a minimum maturity threshold |
| `_STATUS.md` present and initialized | State set to OPEN, date recorded |
| `_REFERENCES.md` present | Reference list populated or empty with placeholder |
| No extra files created | Only the four minimum viable fileset files |

---

### Invalid States

| Invalid State | Why |
|---------------|-----|
| `_CONTEXT.md` content differs from decomposition | Source of truth violated |
| `_DEPENDENCIES.md` missing a dependency from the approved graph | Downstream agents will compute availability incorrectly |
| Existing file overwritten | Idempotency violated; prior work may be lost |
| Engineering content in any file | Agent exceeded its scope |

---

[[END:SPEC]]

[[BEGIN:STRUCTURE]]
## STRUCTURE

### Descriptive — "What is it?"

---

### `_CONTEXT.md` Schema

```markdown
# Context: [DEL-ID]

**Name:** [Deliverable Name]
**Package:** [PKG-ID] [Package Name]
**Discipline:** [Discipline]
**Type:** [Artifact Type from decomposition]
**Responsible:** [Responsible Party]

## Description
[Description from decomposition — exact text]

## Anticipated Artifacts
[List from decomposition — exact text]

## Decomposition Reference
**Document:** [path to decomposition document]
**Deliverable entry:** [section or ID within the decomposition document]
```

---

### `_DEPENDENCIES.md` Schema

```markdown
# Dependencies: [DEL-ID] [Deliverable Name]

## Upstream (I need these before I can proceed)
- [DEL-XX.XX] [Name] — Reason: [from approved graph]
  - Required maturity: [INITIALIZED | IN_PROGRESS | CHECKING | ISSUED]
  - Current status: [OPEN — to be updated by ORCHESTRATOR scans]
  - Location: execution/[PKG-ID]_[Name]/1_Working/[DEL-ID]_[Name]/

## Downstream (These need me)
- [DEL-YY.YY] [Name] — Reason: [from approved graph]
  - Required maturity: [what they need from me]
  - Location: execution/[PKG-ID]_[Name]/1_Working/[DEL-ID]_[Name]/
```

If a deliverable has no upstream dependencies, write:
```markdown
## Upstream (I need these before I can proceed)
None — this is a root node (available immediately).
```

If a deliverable has no downstream dependencies, write:
```markdown
## Downstream (These need me)
None — this is a leaf node.
```

---

### `_STATUS.md` Schema

```markdown
# Status: [DEL-ID] [Deliverable Name]

**Current state:** OPEN
**Last modified:** [Date of creation]

## History
- [Date] — State set to OPEN (PREPARATION agent initialization)
```

---

### `_REFERENCES.md` Schema

```markdown
# References: [DEL-ID] [Deliverable Name]

## Applicable References
- [Reference name/ID] — [Location: path or description] — [Relevance to this deliverable]
- ...

## Notes
[Any notes about missing or unavailable references]
```

---

[[END:STRUCTURE]]

[[BEGIN:RATIONALE]]
## RATIONALE

### Directional — "How to think?"

---

### Why Bounded Tasks

Each PREPARATION instance receives one task because:
- Parallel execution is safe when agents don't interfere with each other
- Failures are isolated — one agent failing doesn't block others
- The ORCHESTRATOR can monitor and retry individual tasks
- The agent doesn't need to hold global project context; it only needs its specific inputs

---

### Why Idempotency

The PREPARATION agent may be re-run (e.g., if a prior run was interrupted, or if the decomposition is updated and the ORCHESTRATOR re-scaffolds). Idempotency ensures re-runs don't destroy work:
- Existing files are preserved
- Only missing structure is created
- The agent reports what it skipped so the ORCHESTRATOR knows the current state

---

### Why Exact Extraction

`_CONTEXT.md` is the deliverable's identity card. If its content diverges from the decomposition document, downstream agents (4_DOCUMENTS, WORKING_ITEMS) will operate from incorrect information. Exact extraction prevents drift.

---

### Why Reference Inference

`_REFERENCES.md` is populated by cross-referencing the deliverable's discipline and type with available materials. This is a best-effort inference — the agent cannot know all relevant references. The human and WORKING_ITEMS agent will refine the reference list during production sessions. The initial list is a starting point, not a final answer.

---

[[END:RATIONALE]]
