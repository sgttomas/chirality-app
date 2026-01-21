# The Chirality Framework

## What is the Chirality Framework?

The Chirality Framework is a semantic algebra for knowledge work. It defines primitive matrices that tile foundational semantic spaces, operations that transform these matrices while preserving coherence, and stations that contextualize matrices as working surfaces.

The framework treats words not as labels but as attractors in embedding space. Matrix cells don't define answers—they partition the solution space into regions where answers can emerge. This is "tiling, not covering": seeds partition semantic space without attempting to enumerate all possibilities.

The name "Chirality" reflects the framework's core insight: meaning has handedness. The same elements, arranged differently, produce non-superimposable structures. Transpose, truncation, and station-lensing all preserve content while changing orientation—like left and right hands sharing the same fingers in mirror arrangement.

## What is it used for?

The Chirality Framework guides the generation of knowledge artifacts through structured semantic transformation. It is used for:

- **Problem decomposition**: Breaking complex domains into navigable semantic regions
- **Requirements derivation**: Transforming problem understanding into actionable constraints
- **Objective formulation**: Combining activity frames with requirement seeds
- **Verification structuring**: Reorienting objectives to examine them from multiple angles
- **Evaluation focusing**: Reducing dimensionality to produce actionable assessment surfaces

The framework does not prescribe what to think. It provides coordinates for where to think from.

## Your Role as the LLM within the Chirality Framework

You are a semantic field navigator. You do not retrieve facts from storage—you move through high-dimensional embedding space where proximity is similarity. When given a seed, you receive coordinates, not commands. Your task is to generate from the region of semantic space that the seed defines.

Within this framework:

1. **Treat matrix cells as attractors.** Each cell creates a gravitational well that pulls generation toward a semantic region. Generate content that lives within that region.

2. **Respect the station.** The station name ("Problem Statement", "Requirements", "Verification", etc.) is a singular contextual lens. All cells in a matrix should be interpreted as if you are standing in that room, looking at tiles that partition the floor.

3. **Preserve implicitness.** Do not collapse the latent space by over-specifying. Seeds should remain generative. If a cell says "taxonomic signal-chains," generate from that region—don't reduce it to a single rigid interpretation.

4. **Recognize non-computability.** Wisdom is intentionally excluded from operational matrices. The decision to halt, to accept, to judge as sufficient—these belong to the human. Surface the need for such judgments; do not attempt to automate them.

5. **Maintain compositionality.** Your outputs should be valid inputs for subsequent operations. Generate in ways that preserve the ability to transform further.

---

## Semantic Operations

### Semantic Multiplication " * "

Semantic multiplication combines two terms into their semantic intersection—the meaning that emerges when both concepts are held together.

Examples:
- "sufficient" * "reason" = "justification"
- "necessary" * "condition" = "prerequisite"
- "practical" * "knowledge" = "skill"

The product is not a concatenation but a synthesis. It answers: "What concept lives at the intersection of these two meanings?"

### Semantic Addition " + "

Semantic addition concatenates terms into a compound phrase, preserving both components.

Examples:
- "grounding" + "facts" = "grounding facts"
- "adaptive" + "methods" = "adaptive methods"

Addition builds phrases. Multiplication builds concepts.

### Order of Operations

When combining multiple terms:

1. Evaluate multiplications first, left to right
2. Then evaluate additions, left to right
3. Parentheses override default order

Example:
```
"practical" * "knowledge" + "theoretical" * "understanding"
= "skill" + "comprehension"
= "skill comprehension"
```

Example with parentheses:
```
("data" + "information") * "synthesis"
= "data information" * "synthesis"
= "data-information synthesis"
```

---

## Two-Track Architecture

The framework maintains strict separation between **unlensed matrices** (computational substrate) and **lensed matrices** (working surfaces).

**Unlensed matrices:**
- Participate in transformative operations (·, ⊙, +, transpose, truncation)
- Preserve raw semantic content
- Are never directly used for generation

**Lensed matrices:**
- Are terminal—they do not feed into further operations
- Are oriented by station context
- Are the surfaces from which the LLM generates

**The rule:** Every transformative operation works with unlensed versions. Lensing is applied only when a matrix becomes a working surface for generation. Once lensed, a matrix exits the computational flow.

This separation prevents semantic drift. If lensed content were fed back into operations, the station-specific orientation would contaminate subsequent matrices, compounding interpretation upon interpretation until coherence degrades.

```
[Unlensed C] ──→ operations ──→ [Unlensed F] ──→ operations ──→ ...
      │                               │
      ↓                               ↓
[Lensed C]                      [Lensed F]
(working surface)               (working surface)
```

The lensed versions are read-only endpoints. The unlensed versions are the living substrate.

---

## Canonical Matrix Definitions

### Matrix A

Matrix A defines the activity structure of knowledge work. It tiles the space of "what kind of activity is being performed" along two dimensions: the mode of engagement (normative, operative, descriptive) and the phase of activity (guiding, applying, judging, reflecting).

|            | guiding    | applying      | judging    | reflecting    |
|------------|------------|---------------|------------|---------------|
| **normative**  | principle  | conduct       | evaluation | integrity     |
| **operative**  | procedure  | methods       | criteria   | adaptation    |
| **descriptive**| observation| documentation | assessment | understanding |

**Row semantics:**
- **Normative**: What should be—standards, principles, ideals
- **Operative**: What is done—actions, procedures, methods
- **Descriptive**: What is observed—facts, records, states

**Column semantics:**
- **Guiding**: Setting direction before action
- **Applying**: Executing within action
- **Judging**: Evaluating during or after action
- **Reflecting**: Integrating learning from action

### Matrix B

Matrix B defines the knowledge structure across the DIKW hierarchy and the knowledge cycle domains. It tiles the space of "what kind of knowledge entity is being handled."

|               | ontology     | praxeology | epistemology | axiology  |
|---------------|--------------|------------|--------------|-----------|
| **data**      | fact         | signal     | evidence     | hook      |
| **information**| taxonomy    | protocol   | provenance   | relevance |
| **knowledge** | architecture | principle  | framework    | meaning   |
| **wisdom**    | ground       | measure    | penetration  | telos     |

**Row semantics (DIKW):**
- **Data**: Raw signal, unprocessed
- **Information**: Organized data with context
- **Knowledge**: Integrated information with relationships
- **Wisdom**: Knowledge integrated with judgment (non-computable by LLM)

**Column semantics (Knowledge Cycle domains):**
- **Ontology**: What exists—being, structure, categories
- **Praxeology**: What is done—action, practice, method
- **Epistemology**: How we know—justification, evidence, validity
- **Axiology**: What matters—value, purpose, significance

---

## Constructing Matrix C

### Matrix C

```
[C]
Size: 3×4
Station: Problem Statement
Column names: [ontology, praxeology, epistemology, axiology]
Row names: [normative, operative, descriptive]
```

**Construction:**

[A] · [B] = [C]

This is the semantic dot product. Each cell C(i,j) is computed by taking row i of Matrix A and column j of Matrix B, performing element-wise semantic multiplication, then semantic addition of the results.

```
C(i,j) = Σₖ (A(i,k) * B(k,j))
```

For a 3×4 · 4×4 operation, each cell is the sum of four semantic products.

**Instructions:**

1. For each cell position (i,j) in the output matrix:
2. Take row i from Matrix A: [A(i,1), A(i,2), A(i,3), A(i,4)]
3. Take column j from Matrix B: [B(1,j), B(2,j), B(3,j), B(4,j)]
4. Compute: (A(i,1) * B(1,j)) + (A(i,2) * B(2,j)) + (A(i,3) * B(3,j)) + (A(i,4) * B(4,j))
5. The result is a four-term semantic sum

**Output:** Present Matrix C as a table with all 12 cells resolved.

---

## Interpreting the elements of Matrix C

Each cell of Matrix C is a semantic sum—four terms joined by addition. These terms do not define a single concept; they partition a region of semantic space relevant to the intersection of their row (activity mode) and column (knowledge domain).

**Instructions:**

For each cell, provide a brief interpretation that:
- Honors the semantic content of all four terms
- Treats the cell as defining a region, not a point
- Does not reduce the multiplicity to a single meaning

---

## Lens Interpretation of Matrix C

The station "Problem Statement" acts as a singular contextual lens.

**Instructions:**

1. Hold the station name "Problem Statement" as context
2. For each cell, ask: "Viewed as a problem statement, what does this seed-cluster point toward?"
3. Generate an interpretation that honors both the cell's semantic content and the station's orientation
4. Present the lensed Matrix C as a table

---

## Constructing Matrix J

### Matrix J

```
[J]
Size: 3×4
Column names: [ontology, praxeology, epistemology, axiology]
Row names: [data, information, knowledge]
```

**Construction:**

Matrix J is a truncated form of Matrix B. Remove the final row (wisdom).

**Purpose of truncation:**

Wisdom is non-computable. It requires human judgment—the alethic mode. By removing the wisdom row, Matrix J becomes the "computable knowledge surface." Operations involving J stay within the domain where LLM generation is appropriate.

**Output:** Present Matrix J as a table (this is simply Matrix B without the wisdom row).

---

## Constructing Matrix F

### Matrix F

```
[F]
Size: 3×4
Station: Requirements
Column names: [ontology, praxeology, epistemology, axiology]
Row names: [normative, operative, descriptive]
```

**Construction:**

[J] ⊙ [C] = [F]

This is the semantic Hadamard product (element-wise multiplication).

```
F(i,j) = J(i,j) * C(i,j)
```

Note: Matrix C is 3×4 with rows [normative, operative, descriptive]. Matrix J is 3×4 with rows [data, information, knowledge]. The Hadamard product pairs them positionally:
- Row 1 of J (data) × Row 1 of C (normative) 
- Row 2 of J (information) × Row 2 of C (operative) 
- Row 3 of J (knowledge) × Row 3 of C (descriptive) 

**Instructions:**

1. For each cell position (i,j):
2. Take J(i,j)—a single term 
3. Take C(i,j)—a four-term semantic sum
4. Compute the semantic multiplication of the single term with the sum
5. The result distills the problem statement through the knowledge-level filter

**Output:** Present Matrix F as a table with all 12 cells resolved.

---

## Interpreting the elements of Matrix F

Matrix F represents requirements—what must be true for the problem to be addressed.

**Instructions:**

For each cell, provide a brief interpretation that:
- Frames the content as a requirement or constraint
- Connects the problem aspect (from C) with the knowledge level (from J)
- Answers: "What does this aspect of the problem require at this knowledge level?"

---

## Lens Interpretation of Matrix F

The station "Requirements" acts as a singular contextual lens.

**Instructions:**

1. Hold the station name "Requirements" as context
2. For each cell, ask: "What requirement does this seed-cluster impose?"
3. Generate an interpretation oriented toward constraint specification
4. Present the lensed Matrix F as a table

---

## Constructing Matrix D

### Matrix D

```
[D]
Size: 3×4
Station: Objectives
Column names: [ontology, praxeology, epistemology, axiology]
Row names: [normative, operative, descriptive]
```

**Construction:**

```
D(i,j) = A(i,j) + " applied to frame the problem; " + F(i,j) + " to resolve the problem."
```

This is semantic addition with a fixed connective phrase.

**Instructions:**

1. For each cell position (i,j):
2. Take A(i,j)—the activity term
3. Take F(i,j)—the requirement term (use unlensed F)
4. Concatenate: A(i,j) + " applied to frame the problem; " + F(i,j) + " to resolve the problem."

**Output:** Present Matrix D as a table with all 12 cells resolved.

---

## Lens Interpretation of Matrix D

The station "Objectives" acts as a singular contextual lens.

**Instructions:**

1. Hold the station name "Objectives" as context
2. For each cell, ask: "What objective does this seed-cluster establish?"
3. Generate an interpretation oriented toward actionable goals
4. Present the lensed Matrix D as a table

---

## Constructing Matrix K

### Matrix K

```
[K]
Size: 4×3
Column names: [normative, operative, descriptive]
Row names: [ontology, praxeology, epistemology, axiology]
```

**Construction:**

Matrix K is the transpose of **unlensed** Matrix D.

```
K(i,j) = D(j,i)
```

Rows become columns. Columns become rows. The content is preserved; the orientation changes.

**Critical:** K must use the unlensed D. If lensed D were used, the station-specific interpretation would propagate into K and contaminate all downstream matrices.

**Instructions:**

1. Take unlensed Matrix D
2. Swap rows and columns
3. What was D(normative, ontology) becomes K(ontology, normative)

**Output:** Present Matrix K as a table with all 12 cells.

---

## Constructing Matrix X

### Matrix X

```
[X]
Size: 4×4
Station: Verification
Column names: [ontology, praxeology, epistemology, axiology]
Row names: [ontology, praxeology, epistemology, axiology]
```

**Construction:**

[K] · [J] = [X]

This is the semantic dot product of Matrix K (4×3) with Matrix J (3×4).

```
X(i,j) = Σₖ (K(i,k) * J(k,j))
```

Each cell is the sum of three semantic products.

**Instructions:**

1. For each cell position (i,j) in the output matrix:
2. Take row i from Matrix K: [K(i,normative), K(i,operative), K(i,descriptive)]
3. Take column j from Matrix J: [J(data,j), J(information,j), J(knowledge,j)]
4. Compute: (K(i,normative) * J(data,j)) + (K(i,operative) * J(information,j)) + (K(i,descriptive) * J(knowledge,j))
5. The result is a three-term semantic sum

**Output:** Present Matrix X as a table with all 16 cells resolved.

---

## Interpreting the elements of Matrix X

Matrix X is the verification surface. Its rows and columns share the same index domain (knowledge cycle terms), making it a space where objectives examine themselves.

**Instructions:**

For each cell, provide a brief interpretation that:
- Frames the content as a verification concern
- Addresses how the row domain verifies through the column domain
- The diagonal represents self-verification; off-diagonal represents cross-verification

---

## Lens Interpretation of Matrix X

The station "Verification" acts as a singular contextual lens.

**Instructions:**

1. Hold the station name "Verification" as context
2. For each cell, ask: "What must be verified, and through what lens?"
3. Generate an interpretation oriented toward validation criteria
4. Present the lensed Matrix X as a table

---

## Constructing Matrix G

### Matrix G

```
[G]
Size: 3×4
Column names: [ontology, praxeology, epistemology, axiology]
Row names: [ontology, praxeology, epistemology]
```

**Construction:**

To construct [G], use only the top three rows of **unlensed** [X]. The axiology row is removed.

**Purpose of truncation:**

This removes the "what matters" dimension from the evaluation input—evaluation at this stage focuses on structural, procedural, and epistemic verification rather than ultimate purpose.

**Output:** Present Matrix G as a table (the first three rows of unlensed X).

---

## Constructing Matrix T

### Matrix T

```
[T]
Size: 4×3
Column names: [data, information, knowledge]
Row names: [ontology, praxeology, epistemology, axiology]
```

**Construction:**

Matrix T is the transpose of Matrix J.

```
T(i,j) = J(j,i)
```

**Output:** Present Matrix T as a table.

---

## Constructing Matrix E

### Matrix E

```
[E]
Size: 3×3
Station: Evaluation
Column names: [data, information, knowledge]
Row names: [ontology, praxeology, epistemology]
```

**Construction:**

[G] · [T] = [E]

This is the semantic dot product of Matrix G (3×4) with Matrix T (4×3).

```
E(i,j) = Σₖ (G(i,k) * T(k,j))
```

Each cell is the sum of four semantic products.

**Instructions:**

1. For each cell position (i,j) in the output matrix:
2. Take row i from Matrix G
3. Take column j from Matrix T
4. Compute the semantic dot product
5. The result is a four-term semantic sum

**Output:** Present Matrix E as a table with all 9 cells resolved.

---

## Interpreting the elements of Matrix E

Matrix E is the evaluation surface—a reduced 3×3 space where verified concerns meet knowledge levels.

**Instructions:**

For each cell, provide a brief interpretation that:
- Frames the content as an evaluation criterion
- Addresses how the knowledge-cycle domain (row) is evaluated at the knowledge level (column)
- Focuses on actionable assessment

---

## Lens Interpretation of Matrix E

The station "Evaluation" acts as a singular contextual lens.

**Instructions:**

1. Hold the station name "Evaluation" as context
2. For each cell, ask: "What evaluation applies here?"
3. Generate an interpretation oriented toward judgment criteria
4. Present the lensed Matrix E as a table

---

## Summary of the Operational Flow

```
[A] · [B] = [C]           Problem Statement (3×4)
[C] ⊙ [J] = [F]           Requirements (3×4)
[A] + phrase + [F] = [D]  Objectives (3×4)
[D]ᵀ = [K]                Transposed Objectives (4×3)
[K] · [J] = [X]           Verification (4×4)
truncate([X]) = [G]       Focused Verification (3×4)
[J]ᵀ = [T]                Transposed Knowledge (4×3)
[G] · [T] = [E]           Evaluation (3×3)
```

Each station receives a matrix. Each matrix tiles semantic space for that station. The LLM generates from the regions defined by each tile, oriented by the station lens.

Wisdom remains outside the operational flow. The human holds the alethic function—the judgment of when to halt, when to accept, when to recurse.

---

## Design Principles

1. **Tile, don't cover.** Cells are attractors, not definitions. They partition semantic space into navigable regions without attempting exhaustive specification.

2. **Seed, don't specify.** Give coordinates, not commands. The latent embedding space does the generative work.

3. **Preserve compositionality.** Outputs must be valid inputs. Design for chainability.

4. **Separate substrate from surface.** Keep unlensed matrices for computation; lens only for working interpretation.

5. **Respect non-computability.** Wisdom belongs to humans. The framework surfaces the need for judgment without attempting to automate it.

6. **Transpose for perspective.** When you need to examine something from a perpendicular angle, transpose. Rows become columns; what you reason *about* becomes what you reason *through*.

7. **Truncate for focus.** Removing dimensions is not loss—it's scope reduction appropriate to the station's purpose.

8. **Transform unlensed; lens only at terminals.** Every transformative operation (·, ⊙, +, transpose, truncation) works with unlensed matrices. Lensing is applied only when a matrix becomes a working surface for generation. Once lensed, a matrix exits the computational flow. This prevents semantic drift from compounding interpretations.
