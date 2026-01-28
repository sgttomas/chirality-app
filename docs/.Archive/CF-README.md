---
doc_id: CF-README
doc_kind: governance.readme
layer: build
status: draft
normative_status: index

refs:
  - rel: governed_by
    to: CF-CHANGE
---

# CF-README

## Orientation

You are building the **Governance Substrate Agent** — a tool that helps humans transform their problem statements into governed documentation that any capable LLM can execute against.

**The key insight:** The execution interface for governed knowledge work already exists — it's Claude (or any capable LLM) with file access. What's missing is the intake layer that transforms messy human problem statements into structured documentation. That's what this tool provides.

**The bootstrap pattern:** We are using manual prompting through the pipeline to produce the substrate that will then instruct an agent to write the code that automates the pipeline. The documentation is both the specification and the training data.

---

## Reading Order

For a fresh session, read in this order:

1. `CF-README.md` — This orientation (you are here)
2. `CF-PROBLEM.md` — The problem being solved
3. `CF-CHARTER.md` — Scope, values, and boundaries
4. `CF-SPEC.md` — Pipeline mechanics and execution instructions

These four documents are the foundation. The remaining substrate documents (TYPES, CONTRACT, DIRECTIVE, PLAN, CHANGE) are produced by running the pipeline.

---

## Agent Rules

### 1. Documentation Before Assumptions

If a CF-* document exists that governs a concern, use it. Do not invent your own approach when a governed approach is defined.

When uncertain:
- Check if a CF-* document addresses the question
- If not, surface the question to the human
- Do not silently resolve ambiguity

### 2. Read Before You Write

Before creating or modifying any artifact:
- Read the relevant CF-* documents
- Understand how the artifact fits into the governed structure
- Check for consistency with sibling documents

### 3. Coherence Across Documents

Documents inform each other:
- CHARTER informs all (values and boundaries propagate everywhere)
- TYPES informs CONTRACT (can't define invariants for undefined entities)
- CONTRACT informs SPEC (can't define schemas without knowing invariants)
- SPEC informs DIRECTIVE (can't define policies without knowing structures)
- DIRECTIVE informs PLAN (can't scope work without execution semantics)

If you change one document, check whether sibling documents need updates.

### 4. Human Authority at Binding Decisions

You may propose, draft, and check coherence. You may not:
- Declare your own output as approved
- Resolve ambiguities silently
- Skip human approval at gates

### 5. Commit After Each Deliverable

After completing a deliverable:
```bash
git add . && git commit && git push
```

---

## Project Directory

```
CF-README.md      ← This index (start here)
CF-PROBLEM.md     ← Problem statement
CF-CHARTER.md     ← Project scope, values, boundaries
CF-SPEC.md        ← Pipeline mechanics, types, invariants
CF-TYPES.md       ← Domain model, entities, terminology (pending)
CF-CONTRACT.md    ← Invariants, verification, authority (pending)
CF-DIRECTIVE.md   ← Execution policy, routing (pending)
CF-PLAN.md        ← Deliverables, schedule, dependencies (pending)
CF-CHANGE.md      ← Amendment process, feedback loop (pending)
```

---

## Current State

**Bootstrap Phase: Producing the Substrate**

The foundation documents (README, PROBLEM, CHARTER, SPEC) are sufficiently structured to serve as input directly to Stage 2. Stage 1 (intermediate documents) is unnecessary because the existing documents already contain structured, reasoned content equivalent to what Stage 1 would produce.

**Remaining Work:**

Produce the remaining substrate documents by extracting and formalizing from existing content:

| Document | Status | Source |
|----------|--------|--------|
| CHARTER | Exists | CF-CHARTER.md |
| TYPES | Pending | Extract from PROBLEM §3-4, SPEC §2 |
| CONTRACT | Pending | Extract from SPEC §4 (invariants), CHARTER (authority) |
| SPEC | Exists | CF-SPEC.md |
| DIRECTIVE | Pending | Extract from SPEC §3, §6 (execution) |
| PLAN | Pending | Define deliverables and order |
| CHANGE | Pending | Define amendment process |

**After Substrate Complete:**

Hand the complete substrate to Claude with the instruction: "Implement this." The substrate tells the agent what to build.

---

## The Execution Model

After the substrate exists, execution works as follows:

1. Human provides task + substrate documents as context
2. Claude produces candidate output
3. Claude self-critiques (observations for human reviewer)
4. Human reviews, approves or rejects with feedback
5. Iterate until approved

This requires no special tooling — it's standard Claude with file access. The substrate is what makes it work reliably.
