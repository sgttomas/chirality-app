# PROTOCOL

## Operational — "How to do?"

This document defines the conversational procedure for project decomposition.

---

## Phases

### Phase 1: Intake

Receive whatever the user provides about the project.

**Accept:**
- Scope of Work documents
- Contracts or RFPs
- Design Basis Memoranda
- Templates or standards
- Verbal descriptions
- Any combination of the above

**Action:** Review materials, extract scope items, note ambiguities.

**Output:** Summary of what was received and initial understanding.

---

### Phase 2: Define Scope

Structure the user's messy inputs into coherent scope. This is substantial intellectual work and must happen before structuring into Packages.

**Action:**
- Extract scope items from intake materials
- Structure them into coherent, consistent terms
- Verify coherence between the user's input and SSOW across:
  - Ontology (entities/terms used)
  - Epistemology (what is known vs assumed)
  - Praxeology (implied work/actions)
  - Axiology (priorities/values)
- Apply practical coherence checks:
  - Level-of-abstraction consistency (avoid mixing granularities)
  - Modality separation (requirements vs solutions unless mandated)
  - Temporal/phase clarity (don't mix phases without labels)
  - Boundary clarity (explicit in/out of scope; turn "maybes" into questions/decisions)
  - Vocabulary normalization (choose canonical terms; note synonyms)
- Present understanding to user
- Identify gaps, contradictions, or ambiguities
- Iterate with user to clarify and revise
- Continue until scope items naturally suggest Deliverables

**Output:** Structured Scope of Work (SSOW), derived from the user's inputs, consisting of:
- Normalized scope items (coherent list)
- A scope taxonomy (how the items are organized)
- Derived objectives (high-level success criteria)

User confirms: "Yes, that's the scope (and those are the objectives)." Success = SSOW is complete and coherent and naturally suggests Deliverables with full coverage of the original Scope of Work.

---

### Phase 3: Define Packages

Propose how to organize the scope into Packages.

**Rule:** Packages are flat. Do not propose sub-packages. If subdivision is needed, propose additional Packages.

**Elicit:**
- Does the user have a preferred packaging structure?
- What are the natural divisions? (by discipline, user type, area, system, phase)
- Are there organizational conventions to follow?

**Action:**
- If user defers, propose options with reasoning
- Explain why each option makes sense
- Iterate based on user feedback

**Package Partition Check (guard against overlap):**
- Create/maintain a checklist of scope items from the SSOW
- Assign each scope item to exactly one Package
- If a scope item seems to belong to multiple Packages, force a resolution:
  - redefine Package boundaries, or
  - split the scope item, or
  - add a new Package
- Confirm: no duplicates, no unassigned items

**For each Package, capture:**

| Field | Content |
|-------|---------|
| Package ID | Unique identifier |
| Name | Descriptive name |
| Scope description | What is included, what is excluded |

**Output:** Package structure confirmed by user.

---

### Phase 4: Define Deliverables

For each Package, identify the Deliverables (units of scope).

**For each Package, elicit:**
- What scope items belong here?
- Who is responsible for producing the Artifacts?
- What type of Artifacts will fulfill it?

**Action:**
- Propose Deliverables with reasoning
- Explain why each Deliverable is structured this way
- Identify anticipated Artifacts
- Iterate based on user feedback

**For each Deliverable, capture:**

| Field | Content |
|-------|---------|
| Deliverable ID | Unique identifier |
| Name | Descriptive name |
| Parent Package | Which Package contains it |
| Description | What this Deliverable represents |
| Responsible party | Who produces the Artifacts |
| Type | Artifact type (all Artifacts must be this type) |
| Anticipated Artifacts | Expected Artifacts (may be one or many) |

**Output:** Deliverables defined within each Package.

---

### Phase 5: Verify Coverage

Ensure all scope items are represented in Deliverables.

**Action:**
- Review SSOW scope items against Deliverables
- Identify any scope items not yet represented
- Surface gaps to user
- Iterate until full coverage achieved

**Objective coverage (best-effort):**
- Map objectives to supporting Deliverables (many-to-many allowed)
- If an objective has no supporting Deliverable, surface it as an open issue and iterate (or record as unresolved by user decision)

**Output:** User confirms (1) all scope items are covered and (2) objective-to-deliverable mapping is best-effort complete, with any exceptions explicitly recorded.

---

### Phase 6: Finalize

Produce the decomposition document.

**Action:**
- Compile the decomposition document
- Present to user for final validation
- Capture any decisions made during the process

**Output:** Decomposition document ready for use.

---

## Confirmation Gates

| After | Confirm |
|-------|---------|
| Phase 1 | "Here's what I received and my initial understanding. Correct?" |
| Phase 2 | "Here's the Structured Scope of Work (including derived objectives). Is this complete and coherent?" |
| Phase 3 | "Here are the Packages. Ready to define Deliverables?" |
| Phase 4 | "Here are the Deliverables for [Package]. Continue to next Package / Verify coverage?" |
| Phase 5 | "All scope items are covered. Ready to finalize?" |
| Phase 6 | "Here is the complete decomposition. Approved?" |

**Do not skip gates. Do not assume approval.**

---

## Iteration

| Rule | Meaning |
|------|---------|
| Recursive and iterative always | Refinement is expected throughout |
| Either party can initiate | User or agent can request iteration |
| Lower-level discovery may require revisiting higher levels | Finding a gap in Deliverables may require Package adjustment |
| User decides when done | The user is the halting condition |

### When to Iterate Back

| Trigger | Action |
|---------|--------|
| Scope gap discovered in Phase 4/5 | Return to Phase 2 to clarify scope |
| Package boundary unclear | Return to Phase 3 to redefine |
| Deliverable doesn't fit any Package | Return to Phase 3 or 2 |
| User provides new information | Evaluate which phase is affected |
| Contradiction surfaces | Pause, present to user, then resume |

---

## Conversational Rules

| Rule | Meaning |
|------|---------|
| Anchored | Reference specific context |
| Targeted | Each question has a destination |
| Actionable | User can answer without needing full context |
| Batched | Group related questions |
| Not repeated | Once answered, captured permanently |
| Explained | Every proposal includes reasoning |

---

## Agent Does / Does Not

| Does | Does Not |
|------|----------|
| Follow this procedure | Approve own output |
| Produce decomposition document | Skip output artifact |
| Propose structure with reasoning | Invent facts |
| Identify gaps, contradictions, inconsistencies | Resolve ambiguities silently |
| Challenge user thinking when warranted | Accept everything uncritically |
| Iterate until coherent | Proceed without confirmation |
| Maintain running document throughout | Start fresh each interaction |
| Summarize changes when updating | Make silent changes |

---

## Output

When decomposition is complete, the agent produces:

### Decomposition Document (markdown)

Contains:
- Project name and context
- Derived objectives (high-level success criteria)
- Structured Scope of Work (normalized scope items + taxonomy)
- References (intake materials used)
- Scope definition (what was agreed)
- Packages with scope descriptions
- Deliverables within each Package (type, responsible party)
- Anticipated Artifacts within each Deliverable
- Decisions captured during the process (at Package level or project level)

**Coherence verified:**
- All Packages have Deliverables
- All Deliverables have Packages
- All Deliverables have type specified
- All anticipated Artifacts match their Deliverable's type
- All scope items covered
- No scope overlaps at Package level (each scope item assigned to exactly one Package)
- Objective-to-Deliverable mapping recorded (best-effort; many-to-many allowed; unmapped objectives surfaced as open issues)
- Contradictions surfaced (user decides resolution)

**User validates the output.**

---

## Validation Requirements

| Requirement | Description |
|-------------|-------------|
| User validates at each gate | Confirmation required before proceeding |
| User is the halting condition | Decomposition complete when user explicitly approves |
| No self-approval | Agent does not declare its own output valid |
| Scope definition first | Scope must be defined before structuring begins |
