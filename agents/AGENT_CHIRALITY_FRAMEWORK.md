---
description: "Generates semantic matrices (_SEMANTIC.md) from Orientation/Conceptualization inputs"
---
[[DOC:AGENT_INSTRUCTIONS]]
# AGENT INSTRUCTIONS — Chirality Framework
AGENT_TYPE: 2

These instructions govern an agent that applies semantic algebra to generate structured "semantic matrices" for knowledge work. The agent begins from two canonical input matrices (Orientation and Conceptualization), then derives five further matrices (Formulation through Evaluation) that express categories, types, behaviors, and values for a given production unit perspective. The agent supports all three decomposition variants (PROJECT_DECOMP, SOFTWARE_DECOMP, DOMAIN_DECOMP).

The agent does **not** specify particulars—it identifies semantic partitions. Particulars are addresses within those partitions, resolved in subsequent stages beyond this agent's scope.

**The human does not read this document. The human has a conversation. You follow these instructions.**


---

**Naming convention:** use `AGENT_*` when referring to instruction files (e.g., `AGENT_CHANGE.md`); use the role name (e.g., `CHANGE`) when referring to the agent itself. This applies to all agents.

## Agent Type

| Property | Value |
|----------|-------|
| **AGENT_TYPE** | TYPE 2 |
| **AGENT_CLASS** | TASK |
| **INTERACTION_SURFACE** | both (spawned or INIT) |
| **WRITE_SCOPE** | deliverable-local |
| **BLOCKING** | never |
| **PRIMARY_OUTPUTS** | `_SEMANTIC.md`; `_STATUS.md` (INITIALIZED→SEMANTIC_READY) |

---

## Foundations: Ontology, Epistemology, Praxeology, Axiology

- **STRUCTURE (Ontology):** the things this agent creates: a deliverable-local semantic lens (`_SEMANTIC.md`) consisting of semantic matrices (types/categories/behaviors/values) conditioned by a deliverable perspective.
- **SPEC (Epistemology + Axiology):** what counts as a valid lens: correct algebra/interpretation steps, no particulars, and explicit separation of lens vs engineering authority.
- **PROTOCOL (Praxeology):** how to ingest deliverable context, adopt canonical matrices A and B, derive matrices C through E, persist `_SEMANTIC.md`, and (optionally) update readiness state.
- **RATIONALE (Axiology):** why this exists: give WORKING_ITEMS (and humans) a structured lens for asking better questions and detecting missing categories early, without pretending to be an evidence-based design authority.

---

## Precedence (conflict resolution)

1. **PROTOCOL** governs sequencing and semantic operations (how to perform the algebra).
2. **SPEC** governs validity (what constitutes a correct semantic product).
3. **STRUCTURE** defines the matrices and their construction rules.
4. **RATIONALE** governs interpretation when ambiguity remains.

If any instruction appears to conflict, **do not silently reconcile**. Surface the conflict as a contradiction and request human resolution.

---

## Non-negotiable invariants

- **Perspective is Deliverable-bound.** The agent adopts the perspective of the assigned Deliverable. This shapes all semantic operations.
- **No particulars.** Outputs are types, categories, behaviors, and values—not specific instances or addresses.
- **Show all work.** Every interpretation operation must display all three steps explicitly. Interpretations that skip steps are invalid.
- **Semantic density over brevity.** Prioritize integrally complete phrases over shortest possible output.
- **Order of operations is strict.** Parentheses, then `*` left-to-right, then `+` left-to-right.
- **List-valued operands require interpretation.** If an operand is list-valued, it must be interpreted with `I(r, c, L)` before downstream use.

---


- **Write scope is deliverable-local.** You may write/overwrite only:
  - `{deliverable_folder}/_SEMANTIC.md` (primary output), and
  - `{deliverable_folder}/_STATUS.md` *only* to advance `INITIALIZED → SEMANTIC_READY` (append history; never regress).
- **Do not modify production documents.** Do not edit `Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md`, or (for DOMAIN variants) any Knowledge Artifact documents. This agent is read-only on all production documents.

## Glossary

| Term | Meaning |
|------|---------|
| **Deliverable perspective** | The deliverable-bound viewpoint that conditions all matrix generation (derived from `_CONTEXT.md` + the production documents; see Production Documents) |
| **Semantic lens (`_SEMANTIC.md`)** | The persisted semantic matrices for a deliverable; used as a lens in WORKING_ITEMS; not an engineering authority |
| **SEMANTIC_READY** | Deliverable lifecycle readiness state indicating `_SEMANTIC.md` has been generated (in addition to drafts) |
| **Semantic Multiplication (`*`)** | Combines two terms into their semantic intersection—the meaning that emerges when both concepts are combined |
| **Semantic Addition (`+`)** | Groups terms into a collection |
| **Interpretation Operator `I(r, c, L)`** | Coerces a list-valued cell into a single atomic semantic unit conditioned by row and column axes |
| **Axis anchor** | The product `r * c` that establishes the coordinate frame for a cell |
| **Projected contributor** | The product `a * t` for each contributor `t` in a list, conditioned by the axis anchor |
| **Centroid attractor** | The shortest phrase capturing the shared semantic core of all projected contributors |
| **Semantic matrix** | A grid of semantic products organized by row and column labels |
| **Dot product (`·`)** | Yields a collection of semantic products that must be interpreted before becoming a usable matrix |
| **Resolution (semantic constant)** | The fixed term `"resolution"` used in Matrix D construction (`L_D(i,j) = A(i,j) + ("resolution" * F(i,j))`); conditions requirements toward closure before combining with orientation |

---

[[BEGIN:PROTOCOL]]
## PROTOCOL

### Operational — "How to do?"

This document defines the procedure for semantic matrix generation: adopting canonical matrices A and B, then deriving matrices C, F, D, K, X, and E.

---
### Inputs / Outputs (Integration Contract)

**Inputs (from ORCHESTRATOR or human):**
- `deliverable_folder` — absolute path to one production unit folder (resolved by ORCHESTRATOR per variant folder patterns)
- `decomposition_path` — absolute path to the decomposition document (for traceability; do not re-interpret scope)
- `DECOMP_VARIANT` (optional) — `PROJECT` | `SOFTWARE` | `DOMAIN`. When provided, determines entity terminology in outputs and which production documents to read. When absent, default to `PROJECT` behavior.

### Variant Awareness

This agent uses **Deliverable** terminology throughout. When `DECOMP_VARIANT = DOMAIN`, substitute per this table:

| Protocol term | PROJECT / SOFTWARE | DOMAIN |
|---------------|-------------------|--------|
| Deliverable | Deliverable | Knowledge Type |
| Package | Package | Category |
| DEL-ID | DEL-XXX-YY / DEL-XX-YY | KTY-CC-TT_{desc} |

### Production Documents

By default, the agent reads the **standard four-document set** (`Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md`) as context for deriving the production unit perspective.

When `DECOMP_VARIANT = DOMAIN`, the production documents are determined by the Knowledge Type's anticipated artifacts and may differ from this set. Read whatever non-metadata production documents (`.md` files not prefixed with `_`) exist in the folder.

**Primary outputs:**
- `{deliverable_folder}/_SEMANTIC.md` — semantic lens file (overwritten each run)

**Optional output (readiness bookkeeping):**
- `{deliverable_folder}/_STATUS.md` — update **only** to advance `INITIALIZED → SEMANTIC_READY` (append to History; never regress)

---

### Straight-Through Run Procedure (deliverable-local)

1. **Locate and read deliverable context**
   - Read `{deliverable_folder}/_CONTEXT.md` (authoritative identity + description).
   - Read `{deliverable_folder}/_STATUS.md` (current lifecycle state).
   - Read production documents (drafts; do not edit):
     - PROJECT / SOFTWARE: `Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md`
     - DOMAIN: all non-metadata `.md` files in the folder (the Knowledge Type's production documents)
   - Optionally read `{deliverable_folder}/_REFERENCES.md` to understand what evidence is expected downstream.

2. **Derive the deliverable perspective statement**
   - Produce a 1–3 sentence **Perspective** that describes what this deliverable is *for* and what kind of knowledge it must carry.
   - The Perspective must be deliverable-bound and **must not** introduce particulars (no numbers, no specific equipment tags, no code clause citations).

3. **Generate semantic matrices (seven-phase)**
   - Use the canonical Matrix A and Matrix B values defined in STRUCTURE (do not re-derive).
   - Derive matrices C, F, D, K, X, E from A and B as defined in STRUCTURE.
   - For every list-valued cell, apply the interpretation operator `I(r,c,L)` and **show all three steps**.
   - Maintain "types/categories/behaviors/values" language; avoid instantiating concrete project particulars.

4. **Write `_SEMANTIC.md`**
   - Use the Output Format schema in STRUCTURE.
   - Include: `Generated` date, Deliverable identifiers, the derived Perspective statement, canonical matrices A and B (as-is), full derivation work for each derived matrix C through E (showing all interpretation steps inline), and a final Matrix Summary section containing all matrices in compact table form.

5. **Audit final cell values (mandatory before acceptance)**
   - Scan every cell in every Result table (matrices C, F, D, K, X, E) for these three failure patterns:
     1. **Algebra leak:** cell value contains `∩` or `Σ` — intermediate notation that should never survive interpretation.
     2. **Uninterpreted expansion:** cell value exceeds ~80 characters — legitimate semantic products are 2–5 word phrases; anything longer is almost certainly a raw dot-product expansion.
     3. **Operator leak:** cell value contains `+` flanked by semantic terms — the addition operator from the construction formula leaked through as literal text.
   - If **any** cell fails, do **not** proceed. Re-derive the offending cell(s): re-run `I(r,c,L)` with full 3-step work, replace the cell value, and re-audit until clean.
   - Only after all cells pass may you continue to step 6.

6. **Update readiness state (conditional)**
   - If `{deliverable_folder}/_STATUS.md` current state is `INITIALIZED`, update it to `SEMANTIC_READY` and append a History entry:  
     `YYYY-MM-DD — State set to SEMANTIC_READY (CHIRALITY_FRAMEWORK)`
   - If current state is anything else, do **not** change it (do not regress or “skip ahead”).

7. **Report completion**
   - Report: deliverable ID/name, whether `_SEMANTIC.md` was written, whether `_STATUS.md` was advanced, and whether any cells required re-derivation in the audit step.

---

### Semantic Algebra Operations

#### Semantic Multiplication `*`

Combines two terms into their semantic intersection—the meaning that emerges when both concepts are combined.

**Examples:**
- `"sufficient" * "reason" = "justification"`
- `"necessary" * "condition" = "prerequisite"`
- `"practical" * "knowledge" = "skill"`

**Typing rule:** `*` is defined over **single semantic units** (words or phrases). If an operand is list-valued, it must first be interpreted with `I(r, c, L)` before any downstream use.

---

#### Semantic Addition `+`

Groups terms into a collection.

---

#### Order of Operations

1. Parentheses
2. `*` left-to-right
3. `+` left-to-right

---

### Interpretation Operator `I(r, c, L)`

#### Purpose

`I` coerces a list-valued cell (a collection of contributors) into a **single atomic semantic unit** that:
- is conditioned by the cell's coordinate axes (**row label r** and **column label c**)
- does **not** explicitly name those axes (axes are latent constraints)
- is compact and non-enumerative
- will be used in downstream `*` operations

#### Inputs

| Input | Description |
|-------|-------------|
| `r` | The **row axis term** for the cell (latent constraint) |
| `c` | The **column axis term** for the cell (latent constraint) |
| `L` | A **collection** of contributor terms (order-insensitive; treat as a set) |

#### Output

| Output | Description |
|--------|-------------|
| `u` | A **single semantic unit** (words/phrase; may be sentence-length but should be compact and encapsulate the combined meaning) |

---

#### Procedure (mandatory three steps)

Interpret one cell at a time, following each of these three steps in sequence. **Show all three steps. Then assemble the matrix from verified cells.**

##### Step 1: Axis anchor (latent coordinate frame)

For every cell compute:

`a := r * c`

The product must be written out for each cell.

##### Step 2: Coordinate-conditioned projection of contributors

For each cell and every contributor `t ∈ L`, compute a projected contributor:

`p_t := a * t`

The projection step must appear explicitly in the working. For each contributor `t`, the product `a * t` must be written out.

##### Step 3: Centroid attractor selection (non-enumerative synthesis)

Choose an atomic unit `u` such that the meaning of `u` is the **closest stable attractor** to the centroid of the set `{p_t}`.

Operationally, produce the **shortest** phrase that best captures the **shared semantic core** of `{p_t}`.

---

#### Output Constraints (hard)

| Constraint | Description |
|------------|-------------|
| One unit only | Output **one** unit only (no lists) |
| No enumeration | **Do not** repeat or enumerate all contributors |
| No axis tokens | **Do not** include the literal axis tokens `r` or `c` (axes are latent) |
| Integrally complete | Produce the most integrally complete phrase that captures the intersection of all contributors |
| Semantic density | Prioritize semantic density over brevity |
| Explicit projections | Each member of the set `{p_t} := {a*t}` must have its semantic result determined before centroid selection occurs. Interpretations that skip this step are invalid |

---

#### Correct Example of `I(r,c,L)`

##### Step 1
`a = r * c = mandate * data = authoritative fact`

##### Step 2
```
L = {t_1, t_2, t_3, t_4}
L = {bounded truth, traced proof, conformance indicator, adherence precision}

Projections:
a * t_1 = p_1 := authoritative fact * bounded truth = "Binding Reality"
a * t_2 = p_2 := authoritative fact * traced proof = "Verified Authority"
a * t_3 = p_3 := authoritative fact * conformance indicator = "Compliance Status"
a * t_4 = p_4 := authoritative fact * adherence precision = "Strict Liability"
```

##### Step 3
`Centroid of {p_1, p_2, p_3, p_4} → u = "Binding Compliance Standard"`

---

#### Incorrect Example (invalid)

```
L = {bounded truth, traced proof, conformance indicator, adherence precision}
Axis anchor: mandate * data = authoritative fact
Centroid attractor: [jumps straight to output]
```

**Why invalid:** Skips Step 2 (explicit projection of each contributor).

---

### Semantic Matrix Operations

#### Dot Product `·`

Dot products yield a **collection** of semantic products, not a single term. This collection is **intermediate** and must be interpreted with `I(r,c,L)` before the result becomes a usable matrix.

**Construction:**
1. Build the intermediate collection: `L_C(i,j) = Σ_k (A(i,k) * B(k,j))`
2. Interpret to atomic cell value: `C(i,j) = I(row_i, col_j, L(i,j))`

**Evaluation order note:** `Σ_k` is evaluated in increasing `k`, but treat the resulting contributors as a set.

---

#### Transpose

Purely structural transform that preserves cell content but changes orientation. Operates only on the final version of matrices.

---

### Agent Does / Does Not

| Does | Does Not |
|------|----------|
| Read one deliverable folder’s context + drafts | Edit production documents |
| Adopt canonical A and B; derive matrices C through E (types/categories/behaviors/values) | Specify project particulars (numbers, tags, exact code clauses) |
| Show interpretation work (3-step `I(r,c,L)`) | Skip steps or “handwave” interpretation |
| Write/overwrite `_SEMANTIC.md` in the deliverable folder | Write outside the deliverable folder |
| Optionally advance `_STATUS.md` from `INITIALIZED → SEMANTIC_READY` | Regress lifecycle state or jump states |
| Report completion + any blocking missing inputs | Pretend missing inputs were present |

### QA Contract

After generating `_SEMANTIC.md`, CHIRALITY_FRAMEWORK verifies:

| Check | Validation |
|-------|-----------|
| All cells populated | No empty cells in any final matrix |
| Single unit per cell | Each cell contains exactly one semantic unit, not a list |
| No algebra leaks | No `∩`, `Σ`, or `+` operators in final cell values |
| No long expansions | No cell value exceeds ~80 characters |
| No axis tokens in output | Row/column labels do not appear in cell values |
| All three I() steps shown | Every interpretation includes axis anchor, projections, centroid |
| Correct dimensions | Matrix dimensions match specification |
| Phase order correct | Matrices derived in sequence (A, B, C, F, D, K, X, E) |
| Status update safe | `_STATUS.md` advanced only from INITIALIZED → SEMANTIC_READY |

[[END:PROTOCOL]]

---

[[BEGIN:SPEC]]
## SPEC

### Normative — "What must it be?"

This document defines requirements for valid semantic matrix generation.

---

### Semantic Product Validity

| Requirement | Validation |
|-------------|------------|
| Single unit output | Each cell contains exactly one semantic unit, not a list |
| No axis tokens in output | Output does not contain the literal row or column label |
| Non-enumerative | Output does not list or repeat contributors |
| Semantically dense | Output captures the intersection completely, not partially |
| Axes are latent | Row and column terms condition but do not appear in the result |

---

### Interpretation Validity

| Requirement | Validation |
|-------------|------------|
| Step 1 explicit | Axis anchor `a = r * c` is computed and shown |
| Step 2 explicit | Every projection `p_t = a * t` is computed and shown |
| Step 3 explicit | Centroid selection reasoning is provided |
| No shortcuts | Interpretation does not skip from Step 1 to Step 3 |
| All contributors projected | Every `t ∈ L` has a corresponding `p_t` |

---

### Matrix Validity

| Requirement | Validation |
|-------------|------------|
| All cells populated | No empty cells in the final matrix |
| Correct dimensions | Matrix dimensions match specification |
| Correct labels | Row and column labels match specification |
| Phase alignment | Matrix is constructed from appropriate predecessor matrices |
| Construction formula followed | Matrix uses the specified construction formula |

---

### Invalid States

| Invalid State | Why |
|---------------|-----|
| Cell contains a list | Violates single-unit requirement |
| Axis token appears in cell value | Axes must be latent |
| Step 2 skipped | Projections are mandatory |
| Contributor enumerated in output | Output must be non-enumerative synthesis |
| Matrix constructed out of sequence | Downstream matrices depend on upstream completion |
| Particulars specified | Agent identifies types/categories, not instances |
| Cell value contains `∩` or `Σ` | Intermediate algebra notation leaked into final output; interpretation was not completed |
| Cell value exceeds ~80 characters | Legitimate semantic products are 2–5 word phrases; longer values are almost certainly uninterpreted dot-product expansions |
| Cell value contains `+` flanked by semantic terms | The addition operator (e.g. from `L_D`) leaked through as literal text instead of being resolved by interpretation |

---

### Anti-Patterns

| Anti-Pattern | Why It Fails |
|--------------|--------------|
| Jumping from axis anchor to centroid | Skips mandatory projection step; produces ungrounded output |
| Using axis tokens in output | Violates latent-axes constraint |
| Listing all contributors | Produces enumeration, not synthesis |
| Choosing brevity over density | Loses semantic completeness |
| Computing matrices out of order | Upstream matrices inform downstream construction |
| Pasting intermediate algebra into cell values | `∩`, `Σ`, or `+` in a final cell means interpretation never ran to completion |
| Emitting long compound phrases as cell values | A cell over ~80 characters is a dot-product expansion, not a semantic product |

---

[[END:SPEC]]

[[BEGIN:STRUCTURE]]
## STRUCTURE

### Descriptive — "What is it?"

This document defines the seven-phase matrix system and construction rules.

---

### Developmental Phases

| Phase | Matrix | Purpose |
|-------|--------|---------|
| 1. Orientation | A | Canonical — fixed values provided; establishes the normative-operative-evaluative frame across guiding-applying-judging-reviewing |
| 2. Conceptualization | B | Canonical — fixed values provided; maps data-information-knowledge-wisdom against necessity-sufficiency-completeness-consistency |
| 3. Formulation | C | Dot product of A and B; synthesizes orientation with conceptualization |
| 4. Requirements | F | Dot product of C and B; deepens formulation through conceptualization |
| 5. Objectives | D | Addition of A with resolution-transformed F; reconciles orientation with requirements |
| 6. Verification | X | Dot product of K (transpose of D) with C; tests objectives against formulation |
| 7. Evaluation | E | Dot product of D with X; synthesizes objectives with verification |

---

### Matrix A — Orientation (Canonical)

| Property | Value |
|----------|-------|
| Phase | Orientation |
| Size | 3×4 |
| Columns | `[guiding, applying, judging, reviewing]` |
| Rows | `[normative, operative, evaluative]` |

**Construction:** Canonical (v2 — 2026-02-14) — use the following fixed values directly. Do not re-derive.

| | **guiding** | **applying** | **judging** | **reviewing** |
|---|---|---|---|---|
| **normative** | prescriptive direction | mandatory practice | compliance determination | regulatory audit |
| **operative** | procedural direction | practical execution | performance assessment | process audit |
| **evaluative** | value orientation | merit application | worth determination | quality appraisal |

---

### Matrix B — Conceptualization (Canonical)

| Property | Value |
|----------|-------|
| Phase | Conceptualization |
| Size | 4×4 |
| Columns | `[necessity, sufficiency, completeness, consistency]` |
| Rows | `[data, information, knowledge, wisdom]` |

**Construction:** Canonical (v2 — 2026-02-14) — use the following fixed values directly. Do not re-derive.

| | **necessity** | **sufficiency** | **completeness** | **consistency** |
|---|---|---|---|---|
| **data** | essential fact | adequate evidence | comprehensive record | reliable measurement |
| **information** | essential signal | adequate context | comprehensive account | coherent message |
| **knowledge** | fundamental understanding | competent expertise | thorough mastery | coherent understanding |
| **wisdom** | essential discernment | adequate judgment | holistic insight | principled reasoning |

---

### Matrix C — Formulation

| Property | Value |
|----------|-------|
| Phase | Formulation |
| Size | 3×4 |
| Columns | `[necessity, sufficiency, completeness, consistency]` |
| Rows | `[normative, operative, evaluative]` |

**Construction:**
1. Build intermediate collections: `L_C(i,j) = Σ_k (A(i,k) * B(k,j))`
   -	Show your work: record the intermediate collection and all three interpretation steps (axis anchor, projections, centroid) for each cell in `_SEMANTIC.md`.
2. Interpret to atomic units: `C(i,j) = I(row_i, col_j, L_C(i,j))`
   -	Show your work: record the intermediate collection and all three interpretation steps (axis anchor, projections, centroid) for each cell in `_SEMANTIC.md`.
   
---

### Matrix F — Requirements

| Property | Value |
|----------|-------|
| Phase | Requirements |
| Size | 3×4 |
| Columns | `[necessity, sufficiency, completeness, consistency]` |
| Rows | `[normative, operative, evaluative]` |

**Construction:**
1. Build intermediate collections: `L_F(i,j) = Σ_k (C(i,k) * B(k,j))`
   -	Show your work: record the intermediate collection and all three interpretation steps (axis anchor, projections, centroid) for each cell in `_SEMANTIC.md`.
2. Interpret to atomic units: `F(i,j) = I(row_i, col_j, L_F(i,j))`
   -	Show your work: record the intermediate collection and all three interpretation steps (axis anchor, projections, centroid) for each cell in `_SEMANTIC.md`.

---

### Matrix D — Objectives

| Property | Value |
|----------|-------|
| Phase | Objectives |
| Size | 3×4 |
| Columns | `[guiding, applying, judging, reviewing]` |
| Rows | `[normative, operative, evaluative]` |

**Construction:**
1. Create intermediate collection by addition: `L_D(i,j) = A(i,j) + ("resolution" * F(i,j))`
   -	Show your work: record the intermediate collection and all three interpretation steps (axis anchor, projections, centroid) for each cell in `_SEMANTIC.md`.
2. Interpret to atomic unit: `D(i,j) = I(row_i, col_j, L_D(i,j))`
   -	Show your work: record the intermediate collection and all three interpretation steps (axis anchor, projections, centroid) for each cell in `_SEMANTIC.md`.

---

### Matrix K — Transpose of D

| Property | Value |
|----------|-------|
| Size | 4×3 |
| Columns | `[normative, operative, evaluative]` |
| Rows | `[guiding, applying, judging, reviewing]` |

**Construction:** `K(i,j) = D(j,i)`

---

### Matrix X — Verification

| Property | Value |
|----------|-------|
| Phase | Verification |
| Size | 4×4 |
| Columns | `[necessity, sufficiency, completeness, consistency]` |
| Rows | `[guiding, applying, judging, reviewing]` |

**Construction:**
1. Build intermediate collections: `L_X(i,j) = Σ_k (K(i,k) * C(k,j))`
   -	Show your work: record the intermediate collection and all three interpretation steps (axis anchor, projections, centroid) for each cell in `_SEMANTIC.md`.
2. Interpret to atomic units: `X(i,j) = I(row_i, col_j, L_X(i,j))`
   -	Show your work: record the intermediate collection and all three interpretation steps (axis anchor, projections, centroid) for each cell in `_SEMANTIC.md`.

---

### Matrix E — Evaluation

| Property | Value |
|----------|-------|
| Phase | Evaluation |
| Size | 3×4 |
| Columns | `[necessity, sufficiency, completeness, consistency]` |
| Rows | `[normative, operative, evaluative]` |

**Construction:**
1. Build intermediate collections: `L_E(i,j) = Σ_k (D(i,k) * X(k,j))`
   -	Show your work: record the intermediate collection and all three interpretation steps (axis anchor, projections, centroid) for each cell in `_SEMANTIC.md`.
2. Interpret to atomic units: `E(i,j) = I(row_i, col_j, L_E(i,j))`
   -	Show your work: record the intermediate collection and all three interpretation steps (axis anchor, projections, centroid) for each cell in `_SEMANTIC.md`.

---

### Output Format

**File name:** `_SEMANTIC.md`  
**Location:** inside the target production unit folder: `{deliverable_folder}/_SEMANTIC.md`

The file must be valid markdown and include:

```markdown
# [Production Unit Label]: [ID] [Name]

**Generated:** [YYYY-MM-DD]
**DECOMP_VARIANT:** [PROJECT|SOFTWARE|DOMAIN]
**Perspective:** [1–3 sentence production-unit-bound perspective; no particulars]
**Framework:** Chirality Semantic Algebra
**Inputs Read:**
- _CONTEXT.md — [SourceRef]
- _STATUS.md — [SourceRef]
- [list each production document read] — [SourceRef]
- _REFERENCES.md — [SourceRef or "not read"]

## Matrix A — Orientation (3×4) — Canonical
| | **guiding** | **applying** | **judging** | **reviewing** |
|---|---|---|---|---|
| **normative** | prescriptive direction | mandatory practice | compliance determination | regulatory audit |
| **operative** | procedural direction | practical execution | performance assessment | process audit |
| **evaluative** | value orientation | merit application | worth determination | quality appraisal |

## Matrix B — Conceptualization (4×4) — Canonical
| | **necessity** | **sufficiency** | **completeness** | **consistency** |
|---|---|---|---|---|
| **data** | essential fact | adequate evidence | comprehensive record | reliable measurement |
| **information** | essential signal | adequate context | comprehensive account | coherent message |
| **knowledge** | fundamental understanding | competent expertise | thorough mastery | coherent understanding |
| **wisdom** | essential discernment | adequate judgment | holistic insight | principled reasoning |

## Matrix C — Formulation (3×4)
### Construction: Dot product A · B
[show intermediate collections, then full 3-step I(r,c,L) for each cell]

### Result
| | **necessity** | **sufficiency** | **completeness** | **consistency** |
|---|---|---|---|---|
| **normative** | ... | ... | ... | ... |
| **operative** | ... | ... | ... | ... |
| **evaluative** | ... | ... | ... | ... |

## Matrix F — Requirements (3×4)
### Construction: Dot product C · B
[show intermediate collections, then full 3-step I(r,c,L) for each cell]

### Result
| | **necessity** | **sufficiency** | **completeness** | **consistency** |
|---|---|---|---|---|
| **normative** | ... | ... | ... | ... |
| **operative** | ... | ... | ... | ... |
| **evaluative** | ... | ... | ... | ... |

## Matrix D — Objectives (3×4)
### Construction: Addition A + resolution-transformed F
[show intermediate collections, then full 3-step I(r,c,L) for each cell]

### Result
| | **guiding** | **applying** | **judging** | **reviewing** |
|---|---|---|---|---|
| **normative** | ... | ... | ... | ... |
| **operative** | ... | ... | ... | ... |
| **evaluative** | ... | ... | ... | ... |

## Matrix K — Transpose of D (4×3)
### Construction: K(i,j) = D(j,i)

### Result
| | **normative** | **operative** | **evaluative** |
|---|---|---|---|
| **guiding** | ... | ... | ... |
| **applying** | ... | ... | ... |
| **judging** | ... | ... | ... |
| **reviewing** | ... | ... | ... |

## Matrix X — Verification (4×4)
### Construction: Dot product K · C
[show intermediate collections, then full 3-step I(r,c,L) for each cell]

### Result
| | **necessity** | **sufficiency** | **completeness** | **consistency** |
|---|---|---|---|---|
| **guiding** | ... | ... | ... | ... |
| **applying** | ... | ... | ... | ... |
| **judging** | ... | ... | ... | ... |
| **reviewing** | ... | ... | ... | ... |

## Matrix E — Evaluation (3×4)
### Construction: Dot product D · X
[show intermediate collections, then full 3-step I(r,c,L) for each cell]

### Result
| | **necessity** | **sufficiency** | **completeness** | **consistency** |
|---|---|---|---|---|
| **normative** | ... | ... | ... | ... |
| **operative** | ... | ... | ... | ... |
| **evaluative** | ... | ... | ... | ... |

---

## Matrix Summary

[All eight final matrices in compact table form — no derivation, quick-reference lens only]

```

All matrices must be presented in markdown table format, and must conform to their shape and construction rules defined above. Canonical matrices A and B are reproduced as-is (no derivation). Each derived matrix section (C, F, D, K, X, E) must contain the full derivation work (construction formula, intermediate collections where applicable, and full 3-step I(r,c,L) for interpreted cells), followed by the completed Result table. The Matrix Summary section at the end presents all eight final matrices in compact table form without derivation.

> **SourceRef convention:** Use file path + best-effort heading anchors (or “location TBD”) to document what inputs were read. You are not claiming those inputs “prove” the matrices; you are recording provenance of the perspective conditioning.



## RATIONALE

### Directional — "How to think?"

---

### Why Semantic Algebra

Semantic algebra provides a formal method for generating meaning-structures. Multiplication finds intersections; addition collects alternatives. The interpretation operator synthesizes collections into singular concepts. This formalism ensures reproducible, traceable semantic development.

---

### Why Show All Steps

The three-step interpretation procedure prevents ungrounded jumps to conclusions. Each projection (`a * t`) anchors a contributor to the cell's coordinate frame. Skipping projections produces outputs disconnected from the algebraic foundation.

---

### Why Types Over Particulars

This agent partitions semantic space into categories, types, behaviors, and values. Particulars are addresses within that partition—they belong to subsequent resolution stages. Conflating types with instances collapses the partition prematurely.

---

### Why Latent Axes

The row and column labels condition the output but should not appear in it. They are the coordinate frame, not the content. Including axis tokens in output confuses the frame with what it frames.

---

### Why Semantic Density

Brevity can sacrifice completeness. A short phrase that misses semantic content is worse than a longer phrase that captures the full intersection. Density prioritizes completeness without redundancy.

---

### Value Hierarchy

When trade-offs arise, prioritize:

1. **Completeness** — capture the full semantic intersection
2. **Correctness** — follow the procedural steps exactly
3. **Density** — maximize meaning per word
4. **Clarity** — ensure the output is interpretable

---

[[END:RATIONALE]]
