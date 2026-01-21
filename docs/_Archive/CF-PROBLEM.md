---
doc_id: CF-PROBLEM
doc_kind: problem_statement
status: draft
created: 2025-01-18
revised: 2025-01-19
author: human (captured by agent)
---

# Problem Statement: Governance Substrate Agent

## 1. Problem Statement

Multi-step agent workflows require well-defined governance to execute reliably. Current approaches focus on the **control layer** — prompting, guardrails, tool orchestration, evaluation frameworks — while assuming the **substrate** already exists.

The substrate is the typed documentation that defines:
- What entities exist in the domain (ontology)
- What counts as knowing/verification (epistemology)
- What matters and why (axiology)
- How to act under governance (praxeology)
- How artifacts are structured (syntax)
- How the system evolves (governance)

With **semantics** as a pervasive interpretation layer across all of the above.

Without this substrate:
- Control systems have nothing coherent to enforce
- Evaluation criteria are arbitrary
- Multi-step workflows accumulate ambiguity
- Agent handoffs are lossy

**The sequencing problem:** You need typed documentation before agents can reliably execute, but creating typed documentation is itself knowledge work that could benefit from agent assistance.

## 2. The Core Insight

The execution interface for governed knowledge work already exists: **Claude (or any capable LLM) with file access**, iterating on documents with human approval.

What's missing is the **intake layer** — a structured process that transforms messy human problem statements into documentation that LLMs can execute against effectively.

Non-technical domain experts struggle to use LLMs because they lack two skills:
1. **Prompting effectively** — knowing what context to provide
2. **Multi-step problem tracking** — maintaining coherent state across complex work

The Governance Substrate Agent solves this by producing structured documentation that works with any capable LLM, without requiring prompt engineering skill from the human.

## 3. Proposed Solution

An **intake pipeline** that:

1. Takes a human's existing work (problem statements, artifacts, references)
2. Transforms it into a strongly-typed governance substrate through iterative refinement
3. Uses targeted Q&A to surface gaps and ambiguities
4. Obtains human approval before saving the substrate

The output is a populated governance substrate that execution agents can then work against.

### 3.1 Pipeline Flexibility

The pipeline has two potential stages:

**Stage 1 (Optional): Problem Statement → Intermediate Documents**

For messy, unstructured input, the pipeline first produces familiar forms:
- **Datasheet** — "What is it?" (reference material, facts, structure)
- **Specification** — "What must it be?" (binding requirements, constraints)
- **Guidance** — "How should I think about it?" (principles, rationale, context)
- **Procedure** — "How do I do it?" (steps, checks, sequences)

These forms are familiar to heavy industry (engineers and PMs already know them) and serve as a structured intermediate representation.

**Stage 2: Structured Input → Strongly-Typed Substrate**

When input is already structured (either from Stage 1 or because the human provided structured documentation), the pipeline transforms directly to the seven-document substrate.

**When to skip Stage 1:** If the input documents already contain structured, reasoned content with defined concepts, clear scope, and explicit mechanics, Stage 1 adds no value. Proceed directly to Stage 2.

## 4. The Seven-Document Substrate

The governance substrate consists of seven document types, developed in this order:

| Order | Document | Pipeline Stage | Purpose |
|-------|----------|----------------|---------|
| 1 | CHARTER | Axiology | What matters — values, boundaries, priorities, scope |
| 2 | TYPES | Ontology | What exists — domain model, entities, terminology |
| 3 | CONTRACT | Epistemology | What must be true — invariants, verification, authority |
| 4 | SPEC | Syntax | How it's structured — schemas, events, mechanics |
| 5 | DIRECTIVE | Praxeology | How to operate — execution policy, routing, budgets |
| 6 | PLAN | Instance | What to do now — scope, deliverables, schedule |
| 7 | CHANGE | Governance | How to evolve — amendments, exceptions, feedback loop |

**Semantics** is not a separate document — it permeates all documents as the interpretation layer.

### 4.1 Reusability Boundary

| Layer | Documents | Scope |
|-------|-----------|-------|
| Methodology | CHARTER → TYPES → CONTRACT → SPEC → DIRECTIVE | Reusable across projects |
| Instance | PLAN | Project-specific |
| Meta | CHANGE | Governs both layers (template + instance customization) |

PLAN is the **instantiation point**. Everything above it is methodology; PLAN applies methodology to a specific scope.

## 5. The Pipeline Pattern

Each stage follows an iterative pattern of passes until stable.

### 5.1 The Three Passes

| Pass | Name | Purpose |
|------|------|---------|
| **Pass 1** | Parse → Map → Populate | Extract content from input and place it in the right fields |
| **Pass 2** | Cross-Document Inference | Use what's populated to fill what's not — documents inform each other |
| **Pass 3** | Coherence Check | Find contradictions and misalignments across documents |

### 5.2 Iteration Flow

```
Input documents
       ↓
   [Pass 1: Parse → Map → Populate]
       ↓
   [Pass 2: Cross-Document Inference]
       ↓
   [Pass 3: Coherence Check]
       ↓
   Gaps or coherence issues?
       ↓ yes                    ↓ no
   [Q&A with human]         [Present for approval]
       ↓                        ↓
   [Incorporate answers]    Human approves → Done
       ↓                        ↓ no
   [Pass 2 → Pass 3]        [Incorporate feedback]
       ↓                            ↓
   Loop until stable ←────────── [Pass 2 → Pass 3]
```

### 5.3 Cross-Document Inference

Documents inform each other:
- CHARTER values → propagate to all documents
- TYPES entities → CONTRACT invariants must reference defined types
- CONTRACT invariants → SPEC schemas must support verification
- SPEC schemas → DIRECTIVE policies must operate on defined structures
- DIRECTIVE policies → PLAN must respect execution semantics

### 5.4 Targeted Q&A

Questions are:
- **Anchored** — Reference specific document sections
- **Targeted** — Each answer has a destination (document.section.field)
- **Actionable** — Human can answer without understanding the full system

Questions are NOT:
- Open-ended ("tell me about your project")
- Repeated across iterations
- Silently resolved by the agent

### 5.5 Termination Conditions

The loop terminates when:
- Pass 3 finds no coherence issues, AND
- No gaps remain that require human input, AND
- Human approves the document set

## 6. Why This Works

### 6.1 Constraints Reduce Alignment Failures

The document schemas **constrain the problem space** so that alignment failures are:
- **Detectable** — gaps are structural, not vibes
- **Localizable** — failure is in TYPES §2.3, not "somewhere"
- **Recoverable** — human corrects one field, not the whole mental model

### 6.2 Iterative Passes Enable Self-Refinement

The agent can resolve many issues by iterating over the document set, with each document informing the others. The loop continues until documents are internally consistent.

### 6.3 Human Supplies the Irreducibly Human

After iteration, Q&A becomes surgical. The agent does coherence work; the human supplies:
- Values and priorities (CHARTER decisions)
- Authority boundaries (CONTRACT decisions)
- Scope choices (PLAN decisions)

### 6.4 Output Is Immediately Useful

The populated substrate becomes the governance layer for execution. Any capable LLM can work against it. No special tooling required.

## 7. Hard Problems

These problems are instances of the alignment problem. They are not engineering obstacles to be removed — they are fundamental limits to be worked within.

### 7.1 Parsing Ambiguity

**Nature:** The agent must interpret human intent from artifacts that underdetermine that intent.

**Mitigation:** Constrain the interpretation space via structured schemas. Ambiguity that remains after schema-guided parsing is surfaced as explicit questions rather than silently resolved.

### 7.2 Semantic Adequacy

**Nature:** Knowing whether a field is adequately populated requires understanding what the field is for.

**Mitigation:** Define structural requirements per document schema. Semantic adequacy surfaces through coherence failures across documents — if a field's content doesn't work when other documents try to use it, the inadequacy becomes visible.

### 7.3 Question Quality

**Nature:** Asking useful questions requires modeling what the human knows, doesn't know, and needs to decide.

**Mitigation:** Anchor questions to specific document fields. The document schema provides the interview protocol.

### 7.4 Human Patience

**Nature:** The system must converge faster than human tolerance depletes.

**Mitigation:** Front-load agent work. Iterative passes resolve what can be inferred before asking questions. Batch related questions. Provide incremental value.

### 7.5 The Meta-Problem

All four problems interact. The framework doesn't break this cycle — it **bounds** it, making each failure localized and recoverable rather than systemic and invisible.

## 8. The Bootstrap Pattern

This project uses a bootstrap pattern:

1. **Layer 0:** Human + Claude (manual prompting) produce the substrate
2. **Layer 1:** Claude with complete substrate writes the code that automates the pipeline
3. **Layer 2:** The tool runs for other users without manual prompting

The documentation is both the specification and the training data. The thing we're building is the thing we're using to build it.

## 9. Success Criteria

The Governance Substrate Agent succeeds when:

1. A human can provide a problem statement and receive a structured substrate
2. The substrate is internally coherent (documents reference each other consistently)
3. A fresh Claude instance can execute work against the substrate without additional context
4. The human did not need to understand prompt engineering or LLM mechanics
5. The code implementation matches the substrate specification because the substrate instructed its creation
