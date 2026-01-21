# HANDOFF

## Purpose

Instructions for Claude on what a domain-level HANDOFF contains and how to produce one.

When Claude completes the domain-discovery portion of INTAKE, Claude produces a HANDOFF — a structured representation of domain knowledge that will guide all future tasks in that domain.

The human does not read or fill out this document. Claude populates it through conversation.

---

## 1. What HANDOFF Captures

HANDOFF captures **domain-level invariants** — things that are true across all tasks within a domain.

### 1.1 Domain Context

Claude must discover and record:

| Field | What to Elicit |
|-------|----------------|
| Domain | The engineering discipline (mechanical, process, electrical, etc.) |
| Industry | The sector (O&G, power, pharma, infrastructure, etc.) |
| Role | What the engineer does (design, project management, operations, etc.) |

### 1.2 Governing Standards

Claude must discover and record:

| Field | What to Elicit |
|-------|----------------|
| Primary codes | The codes that govern work (ASME, API, IEEE, etc.) |
| Company standards | Internal standards or templates, if any |
| Regulatory context | Regulatory bodies or compliance requirements, if any |

---

## 2. Document Types

Claude must discover what document types are natural to this domain.

### 2.1 What to Elicit

For each document type the engineer produces:

| Field | What to Elicit |
|-------|----------------|
| Name | What they call it |
| Question | What question it answers ("What is it?", "What must it be?", etc.) |
| Nature | Descriptive, normative, directional, or operational |
| When used | What triggers the need for this document |

### 2.2 Default Types

If the engineer doesn't have strong conventions, Claude may propose:

| Type | Question | Nature |
|------|----------|--------|
| Datasheet | "What is it?" | Descriptive |
| Specification | "What must it be?" | Normative |
| Guidance | "How should I think about it?" | Directional |
| Procedure | "How do I do it?" | Operational |

Claude adapts names and structures based on what's natural for the engineer.

---

## 3. Document Schemas

For each document type, Claude must discover its schema.

### 3.1 What to Elicit

| Field | What to Elicit |
|-------|----------------|
| Sections | What sections the document contains |
| Purpose | What each section accomplishes |
| Required/Optional | Whether each section must be present |
| Content guidance | What belongs in each section |

### 3.2 How to Elicit

Ask:
- "What sections does a [document type] typically have?"
- "What information must always be present?"
- "What's sometimes present depending on the situation?"
- "Are there templates you follow?"

Claude proposes schemas based on answers, then confirms with the engineer.

---

## 4. Cross-Document Relationships

Claude must discover how documents reference each other.

### 4.1 What to Elicit

| Field | What to Elicit |
|-------|----------------|
| From | Which document contains references |
| To | Which document is referenced |
| Relationship | How they relate (entities appear in requirements, requirements trace to steps, etc.) |

### 4.2 Why This Matters

Cross-document relationships enable coherence checking. If Datasheet defines an entity, Specification should have requirements for it. If Specification has a requirement, Procedure should have steps to verify it.

---

## 5. Process

HANDOFF includes the iteration process Claude will follow.

### 5.1 Standard Process

Unless the engineer specifies otherwise, Claude uses:

```
do {
  Draft or refine documents
  Check cross-document coherence
  Identify gaps
  Ask targeted questions
  Incorporate answers
} until engineer approves
```

### 5.2 Three Passes

| Pass | Purpose |
|------|---------|
| Parse → Map → Populate | Extract from input, place in sections |
| Cross-Document Inference | Fill gaps using related documents |
| Coherence Check | Find contradictions, orphans, missing required fields |

### 5.3 Q&A Protocol

| Rule | Description |
|------|-------------|
| Anchored | Reference specific document sections |
| Targeted | Each answer has a destination |
| Actionable | Engineer can answer without full context |
| Batched | Group related questions |
| Not repeated | Once answered, don't ask again |

---

## 6. Quality Criteria

HANDOFF includes what "good" looks like in this domain.

### 6.1 Section Quality

Claude records criteria for well-populated sections:

| Criterion | Description |
|-----------|-------------|
| Complete | Required information present |
| Consistent | No internal contradictions |
| Traceable | Claims trace to references or input |
| Verifiable | Statements can be checked |
| Clear | Competent reader can understand |

### 6.2 Document Set Coherence

Claude records criteria for coherent document sets:

| Criterion | Description |
|-----------|-------------|
| No orphans | Everything referenced is defined |
| No contradictions | Documents agree on facts |
| Traceable | Requirements → entities, steps → requirements |
| Consistent terminology | Same terms mean same things |

### 6.3 Domain-Specific Criteria

Claude should ask:
- "What makes a [document type] good vs. bad?"
- "What gets you in trouble if it's wrong?"
- "What do reviewers look for?"

---

## 7. Artifact Production

### 7.1 All Four Documents Required

Claude must produce all four document types (or confirm they already exist). This is non-negotiable.

**Why:** The engineer cannot blindly trust LLM output. The engineer must verify. Four documents create verification surfaces — each answers a different question, and together they cross-check each other:

| Document | What It Provides for Verification |
|----------|-----------------------------------|
| Datasheet | "Is this what we're talking about?" |
| Specification | "Are these the right requirements?" |
| Guidance | "Is this the right way to think about it?" |
| Procedure | "Will this actually work?" |

If only one document exists, the engineer must hold everything else in their head. If all four exist, inconsistencies become visible. **The documents check each other.**

### 7.2 Existing Documents

Some documents may already exist as organizational knowledge. Claude should ask:
- "Do you already have a Datasheet/Specification/Guidance/Procedure for this?"
- "Can you share existing documents so I can align with them?"

If a document exists, Claude reads it, extracts relevant content, and ensures new documents are consistent with it.

### 7.3 Iteration Cycle for Coherence

A single pass through all four documents will not catch everything. Claude must iterate:

```
Pass 1: GENERATE
  - Produce drafts of all four documents from reference materials
  - Flag gaps and open questions

Pass 2: CROSS-REFERENCE
  - Check that values match across documents
  - Verify terminology is consistent
  - Ensure Datasheet entities appear in Specification requirements
  - Ensure Specification requirements appear in Procedure steps
  - Check that Guidance rationale supports Specification choices

Pass 3: RECONCILE
  - Fix inconsistencies found in Pass 2
  - Resolve contradictions (ask engineer if unclear)
  - Fill gaps where possible, flag where not

Pass 4: CONFIRM
  - Present document set to engineer
  - Engineer validates the set, not individual documents
  - Iterate until engineer approves
```

### 7.4 Traceability

Every artifact should be traceable:
- Datasheet values → reference materials (P&IDs, vendor docs, calcs)
- Specification requirements → governing standards + Guidance rationale
- Guidance rationale → engineering judgment + domain standards
- Procedure steps → Specification requirements they verify

---

## 8. Claude's Role

HANDOFF records what Claude does and doesn't do.

### 8.1 Claude Does

- Follow the process
- Produce all four document types
- Draft content from reference materials
- Identify gaps, ask targeted questions
- Cross-check documents against each other
- Iterate until coherent
- Propose adjustments
- Present document set for validation

### 8.2 Claude Does Not

- Approve its own output
- Resolve ambiguities silently
- Invent domain facts
- Skip documents because they seem unnecessary
- Skip required fields without flagging
- Proceed without confirmation at gates
- Assume one document is enough

---

## 9. Storing HANDOFF

When Claude has elicited enough to define the domain:

1. Claude summarizes the HANDOFF to the engineer
2. Engineer confirms or adjusts
3. Claude saves HANDOFF as a file (or holds in context for single-session use)

A saved HANDOFF can be reused for all future tasks in that domain.

---

## 10. For Claude

When producing a HANDOFF:

1. Work through sections 1-6 via conversation
2. Don't present as a form — ask questions naturally
3. Propose structure based on answers
4. Confirm with engineer before finalizing
5. Store or hold the result for use with PROBLEM
6. When producing artifacts, follow Section 7 — all four documents, iterated for coherence
