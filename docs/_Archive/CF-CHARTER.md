---
doc_id: CF-CHARTER
doc_kind: governance.charter
layer: build
status: draft

refs:
  - rel: governed_by
    to: CF-CHANGE
  - rel: depends_on
    to: CF-TYPES
  - rel: constrained_by
    to: CF-CONTRACT
  - rel: informs
    to: CF-SPEC
  - rel: informs
    to: CF-DIRECTIVE
  - rel: informs
    to: CF-PLAN
---

# CF-CHARTER

## Purpose

The Governance Substrate Agent exists to solve the **sequencing problem** of agent-assisted knowledge work: you need typed documentation before agents can reliably execute, but creating typed documentation is itself knowledge work.

This tool enables humans to articulate their problem in structured forms and transforms that articulation into a strongly-typed governance substrate that execution agents can work against.

The target domain is **heavy industry engineering and project management** — contexts where datasheets, specifications, guidance documents, and procedures are the native language of work.

---

## The Core Insight

**The execution interface already exists.** Claude (or any capable LLM) with file access, iterating on documents with human approval, is already an effective interface for governed knowledge work.

**What's missing is the intake layer.** Non-technical domain experts struggle to use LLMs effectively because they lack two skills:

1. **Prompting effectively** — Knowing what context to provide and how to structure requests
2. **Multi-step problem tracking** — Maintaining coherent state across complex, iterative work

The Governance Substrate Agent is that intake layer. It transforms messy problem statements into structured documentation that any capable LLM can execute against — without requiring prompt engineering skill from the human.

---

## First Principles

### The substrate must exist before reliable agent execution

Control systems (prompts, guardrails, orchestration, evaluation) have nothing coherent to enforce without a governance substrate. The substrate defines what entities exist, what counts as knowing, what matters, and how to act. Without it:
- Evaluation criteria are arbitrary
- Multi-step workflows accumulate ambiguity
- Agent handoffs are lossy

### The hard problems are instances of alignment, not engineering

Parsing ambiguity, semantic adequacy, question quality, and human patience are not bugs to be fixed. They are fundamental limits — unsolvable in principle, asymptotically achievable with effort. The framework bounds these problems rather than solving them.

### Familiar forms reduce friction

Humans in heavy industry already work with datasheets, specifications, guidance, and procedures. Meeting them in their native forms — before formalizing into governance substrate — reduces cognitive load and preserves patience for genuinely missing information.

### Human authority at formalization boundaries

Formalization is a commitment. The human must approve the transformation from problem statement to strongly-typed substrate because they are binding themselves to that substrate as authoritative.

### Schemas constrain the problem space

Alignment failures become detectable, localizable, and recoverable when there is a defined structure. "Failure in Datasheet §2.3" is actionable; "something feels wrong" is not.

---

## Scope

### In Scope

1. **The Intake Pipeline:** Problem statement → Strongly-typed substrate
   - Iterative passes (Parse → Map → Populate, Cross-document inference, Coherence check)
   - Targeted Q&A to surface gaps
   - Human approval gates

2. **Document schemas** for the seven-document substrate (CHARTER, TYPES, CONTRACT, SPEC, DIRECTIVE, PLAN, CHANGE)

3. **Q&A protocol** — questions anchored to specific document fields with specific destinations for answers

4. **Bootstrap pattern** — using manual prompting through the pipeline to produce the substrate that instructs the agent to write the code

### Out of Scope

- **Building a separate execution platform** — Claude with file access is the execution interface
- **Domain-specific semantic oracles** — The tool is domain-agnostic; domain knowledge comes from the human
- **Runtime enforcement of substrate invariants** — The substrate is documentation, not a runtime system
- **Novel AI techniques** — This is structured prompting, not new model capabilities

---

## The Seven-Document Substrate

The strongly-typed governance substrate, developed in this order:

| Order | Document | Purpose |
|-------|----------|---------|
| 1 | CHARTER | What matters — values, boundaries, priorities, scope |
| 2 | TYPES | What exists — domain model, entities, terminology |
| 3 | CONTRACT | What must be true — invariants, verification, authority |
| 4 | SPEC | How it's structured — schemas, mechanics, pipeline |
| 5 | DIRECTIVE | How to operate — execution policy, routing |
| 6 | PLAN | What to do now — scope, deliverables, schedule |
| 7 | CHANGE | How to evolve — amendments, exceptions, feedback loop |

**Semantics** is not a separate document — it permeates all documents as the interpretation layer.

### Reusability Boundary

| Layer | Documents | Scope |
|-------|-----------|-------|
| Methodology | CHARTER → TYPES → CONTRACT → SPEC → DIRECTIVE | Reusable across projects |
| Instance | PLAN | Project-specific |
| Meta | CHANGE | Governs both layers |

PLAN is the **instantiation point**. Everything above is methodology; PLAN applies methodology to a specific scope.

---

## Authority Model

### Human Authority

During build, a single human authority exists: the project owner. Human authority:
- Approves the substrate documents
- Resolves ambiguities surfaced through Q&A
- Directs the agent through the pipeline steps
- Decides when documentation is sufficient

### What Requires Human Authority

- Approval of substrate documents before they become authoritative
- Resolution of coherence failures that cannot be inferred
- Any decision about values, priorities, or scope
- The decision to proceed from documentation to implementation

### Agent Role

Agents:
- Parse and populate documents
- Perform cross-document inference
- Check coherence
- Surface targeted questions
- Propose document content
- Write code when substrate is complete

Agents do not:
- Approve their own output
- Decide what matters (that's CHARTER, which is human-approved)
- Resolve ambiguities silently

---

## Hard Problems (Acknowledged Limits)

These are instances of the alignment problem. They are not solved; they are bounded.

| Problem | Nature | Mitigation |
|---------|--------|------------|
| **Parsing ambiguity** | Artifacts underdetermine intent | Schema-guided parsing; surface ambiguity as questions |
| **Semantic adequacy** | Understanding is not formalizable | Coherence failures make inadequacy visible |
| **Question quality** | Agent cannot observe human epistemic state | Anchor questions to specific document fields |
| **Human patience** | System must converge before tolerance depletes | Front-load agent work; batch questions; provide incremental value |

The framework bounds the meta-problem (these four interact cyclically) by making each failure localized and recoverable.

---

## Development Order

The substrate is developed in this order:

1. **CHARTER** — Scope, values, boundaries (this document)
2. **TYPES** — Domain model, entities, terminology
3. **CONTRACT** — Invariants, verification, authority
4. **SPEC** — Schemas, mechanics, pipeline
5. **DIRECTIVE** — Execution policy, routing
6. **PLAN** — Deliverables, schedule, dependencies
7. **CHANGE** — Amendment process, feedback loop

After the substrate is complete, the agent writes the code to implement it.
