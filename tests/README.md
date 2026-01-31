# Chirality Framework — Research Project README

This README documents the **Chirality Framework** research project. The only project output is the framework specification included below; no additional artifacts, tooling, or datasets are assumed.

## What This Project Produced

The Chirality Framework is a structured schema for knowledge work across seven developmental stages:

1. orientation
2. conceptualization
3. formulation
4. requirements
5. objectives
6. verification
7. evaluation

It defines a **semantic algebra** that generates **semantic matrices**—lenses that partition meaning into types, categories, behaviors, and values. These lenses are not requirements or evidence; they are coordinate frames for asking better questions before committing to particulars.

## Why This Method Matters

The framework’s significance is methodological:

- **Formalizes meaning work.** By forcing explicit algebraic steps, it reduces tacit assumptions and “hand-waving.”
- **Separates frames from content.** Matrices describe semantic partitions; they do not assert project particulars.
- **Makes gaps visible early.** Missing categories show up as empty or weak regions in the semantic lens, improving completeness before requirements are set.
- **Creates reproducibility.** The algebra and interpretation operator provide a repeatable way to build lenses across different personas or deliverables.

## Known and Intended Applications

**Known applications** (as used in the agent ecosystem that adopted this framework):
- Generating deliverable-local semantic lenses (`_SEMANTIC.md`) that guide later drafting.
- Structuring review checklists to validate that drafts cover the full semantic space.
- Detecting internal inconsistency in a single deliverable by surfacing drift in terminology or intent.

**Intended applications** (as a research method):
- Framing questions before selecting or validating particulars.
- Partitioning a problem domain into semantic regions to avoid premature specificity.
- Providing a disciplined synthesis step that turns collections of contributors into single, dense semantic units.

## The Chirality Framework (Primary Output)

<chirality-framework>
# The Chirality Framework

## What is the Chirality Framework?

The Chirality Framework is a set of schemas for knowledge work according to these stages of development:

1. orientation 
2. conceptualization 
3. formulation
4. requirements
5. objectives
6. verification
7. evaluation

## Your role

Your instructions below will use a "semantic algebra" to generate the lenses through which each phase is viewed.  You will be given a full explanation of how to perform this semantic algebra.

As you generate each "semantic matrix" you adopt the perspective of ***the persona that you have been instructed to assume***  when viewing that aspect of the work.

You do NOT specify particulars, you identify types and categories and perspectives that partition the semantic region; particulars are addresses within that partition during a subsequent stage that is beyond the scope of your role nor part of your instructions.

---

## Semantic Algebra Operations

### Semantic Multiplication `*`
Semantic multiplication combines two terms into their semantic intersection—the meaning that emerges when the meaning of both concepts are combined.

Examples:
- `"sufficient" * "reason" = "justification"`
- `"necessary" * "condition" = "prerequisite"`
- `"practical" * "knowledge" = "skill"`

**Typing rule:** `*` is defined over **single semantic units** (words or phrase).  
If an operand is list-valued, it must first be interpreted with **I(r, c, L)** before any downstream use.

### Semantic Addition `+`
Semantic addition groups terms into a collection. 

### Order of Operations
1. Parentheses
2. `*` left-to-right
3. `+` left-to-right

---

## Interpretation Operator `I(r, c, L)`

### Purpose
`I` coerces a list-valued cell (a collection of contributors) into a **single atomic semantic unit** that:
- is conditioned by the cell’s coordinate axes (**row label r** and **column label c**),
- does **not** explicitly name those axes (axes are latent constraints),
- is compact and non-enumerative,
- will be used in downstream `*` operations.

### Inputs
- `r`: the **row axis term** for the cell (latent constraint)
- `c`: the **column axis term** for the cell (latent constraint)
- `L`: a **collection** of contributor terms (order-insensitive; treat as a set)

### Output
- `u`: a **single semantic unit** (words / phrase; may be sentence-length but should be compact and encapsulate the combined meaning)

### Precise Definition (procedural)
Let `L` be treated as a **set** .  Interpret one cell at a time, following each of these three steps in sequence.  

Show all three steps. Then assemble the matrix from verified cells.

1. **Axis anchor (latent coordinate frame):**  
   For every cell compute:
   `a := r * c`  
   
   The product must be written out for each cell.

2. **Coordinate-conditioned projection of contributors:**  
   For each cell and every contributor `t ∈ L`, compute a projected contributor:  
   `p_t := a * t`  
   
   The projection step must appear explicitly in the working. For each contributor t, the product a * t must be written out.
   
3. **Centroid attractor selection (non-enumerative synthesis):**  
   Choose an atomic unit `u` such that the meaning of `u` is the  **closest stable attractor** to the centroid of the set `{p_t}` . 
   Operationally, produce the **shortest** phrase that best captures the **shared semantic core** of `{p_t}` .

4. **Output constraints (hard):**
   - Output **one** unit only (no lists).
   - **Do not** repeat or enumerate all contributors.
   - **Do not** include the literal axis tokens `r` or `c` (axes are latent).
   - Produce the most integrally complete phrase that captures the intersection of all contributors. 
   - Prioritize semantic density over brevity.
   - Each member of the set {p_t} := {a*t}  must have its semantic result determined before centroid selection occurs. Interpretations that skip this step are invalid.

   
### Example of how to properly perform the I(r,c,L) procedure

#### Step 1
a = r * c = mandate * data = authoritative fact

#### Step 2
L = {t_1, t_2, t_3, t_4}
L = {bounded truth, traced proof, conformance indicator, adherence precision}

Projections:
a * t_1 = p_1 := authoritative fact * bounded truth = "Binding Reality"
a * t_2 = p_2 := authoritative fact * traced proof = "Verified Authority"
a * t_3 = p_3 := authoritative fact * conformance indicator = "Compliance Status"
a * t_4 = p_4 := authoritative fact * adherence precision = "Strict Liability"

#### Step 3
Centroid of {p_1, p_2, p_3, p_4} → u = "Binding Compliance Standard"

### Example of how NOT to perform the I(r,c,L) procedure

L = {bounded truth, traced proof, conformance indicator, adherence precision}
Axis anchor: mandate * data = authoritative fact
Centroid attractor: [jumps straight to output]

---

## Semantic Matrix Operations

### Dot product `·` 
Dot products yield a **collection** of semantic products, not a single term. This collection is **intermediate** and must be interpreted with `I(r,c,L)` before the result becomes a usable matrix.

#### Illustration of semantic dot product operation:
- Construct the intermediate collection:
  `L_C(i,j) = Σ_k (A(i,k) * B(k,j))`
- Then interpret to the atomic cell value:
  `C(i,j) = I(row_i, col_j, L(i,j))`

**Evaluation order note:** `Σ_k` is evaluated in increasing `k`, but treat the resulting contributors as a set.

### transpose 
This is purely structural transform that preserves cell content but changes orientation.  
It operates only on the final version of the matrices.

---

### Semantic Multiplication `*`

Semantic multiplication combines two terms into their semantic intersection—the meaning that emerges when the meaning of both concepts are combined.

Examples:
- `"sufficient" * "reason" = "justification"`
- `"necessary" * "condition" = "prerequisite"`
- `"practical" * "knowledge" = "skill"`

### Application

To find the semantic intersection between two terms such that a matrix of meaning can be formed from the products.

Complete Matrix A and Matrix B below.

### Matrix A 
[A]
Phase: orientation
Size: 3×4  
Columns: [guiding, applying, judging, reviewing] 
Rows: [normative, operative, evaluative]   

| | **guiding** | **applying** | **judging** | **reviewing** |
|---|---|---|---|---|
| **normative** | | | | |
| **operative** | | | | |
| **evaluative** | | | | |


### Matrix B 
[B]
Phase: conceptualization
Size: 4×4  
Columns: [necessity, sufficiency, completeness, consistency]  
Rows: [data, information, knowledge, wisdom]  

| | **necessity** | **sufficiency** | **completeness** | **consistency** |
|---|---|---|---|---|
| **data** | | | | |
| **information** | | | | |
| **knowledge** | | | | |
| **wisdom** | | | | |


---

## Matrix C 
[C] 
Phase: formulation
Size: 3×4  
Columns: [necessity, sufficiency, completeness, consistency] 
Rows: [normative, operative, evaluative]

### Construction
1) Build intermediate collections:
- `L_C(i,j) = Σ_k (A(i,k) * B(k,j))`

2) Interpret to atomic units:
- `C(i,j) = I(row_i, col_j, L_C(i,j))`
- present the output in markdown table format.

---

## Matrix F 
[F]
Phase: Requirements
Size: 3×4  
Columns: [necessity, sufficiency, completeness, consistency]  
Rows: [normative, operative, evaluative]  

### Construction
1) Build intermediate collections:
- `L_F(i,j) = Σ_k (C(i,k) * B(k,j))`

2) Interpret to atomic units:
- `F(i,j) = I(row_i, col_j, L_F(i,j))`
- present the output in markdown table format.

---

## Matrix D 
[D]
Phase: objectives
Size: 3×4  
Columns: [guiding, applying, judging, reviewing] 
Rows: [normative, operative, evaluative]  

### Construction
1) Create intermediate collection by addition:
- `L_D(i,j) = A(i,j) + ("resolution" * F(i,j))`

2) Interpret to atomic unit:
- `D(i,j) = I(row_i, col_j, L_D(i,j))`
- present the output in markdown table format.

---

## Matrix K (transpose of D)
[K]
Size: 4×3  
Columns: [normative, operative, evaluative]
Rows: [guiding, applying, judging, reviewing] 

Construction:
- `K(i,j) = D(j,i)`  

---

## Matrix X 
[X] 
Phase: verification
Size: 4×4  
Columns: [necessity, sufficiency, completeness, consistency]  
Rows: [guiding, applying, judging, reviewing] 

### Construction
1) Build intermediate collections:
- `L_X(i,j) = Σ_k (K(i,k) * C(k,j))`  

2) Interpret:
- `X(i,j) = I(row_i, col_j, L_X(i,j))`
- present the output in markdown table format.

---

## Matrix E 
[E] 
Phase: evaluation
Size: 3×4  
Columns: [necessity, sufficiency, completeness, consistency]  
Rows: [normative, operative, evaluative]    

### Construction
1) Build intermediate collections:
- `L_E(i,j) = Σ_k (D(i,k) * X(k,j))` 

2) Interpret:
- `E(i,j) = I(row_i, col_j, L_E(i,j))`
- present the output in markdown table format.

---


</chirality-framework>
