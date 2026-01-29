# DOMAIN

## Purpose

Instructions for Claude on what a domain-level DOMAIN contains and how to produce one.

A DOMAIN is a structured representation of domain knowledge — what the domain IS. It captures invariants that are true across all tasks within that domain.

The human does not read or fill out this document. Claude populates it through conversation.

---

## What DOMAIN Captures

DOMAIN answers the question: **"What is it?"**

It is descriptive — facts, attributes, structure. It describes the engineering domain, not how to work in it.

DOMAIN captures **domain-level invariants** — things that are true across all tasks within a domain.

---

## 1. Domain Context

Claude must discover and record:

| Field | What to Elicit |
|-------|----------------|
| Domain | The engineering discipline (mechanical, process, electrical, etc.) |
| Industry | The sector (O&G, power, pharma, infrastructure, etc.) |
| Role | What the engineer does (design, project management, operations, etc.) |
| Organization | Company or project context, if relevant |

### How to Elicit

Ask:
- "What kind of engineer are you?"
- "What industry do you work in?"
- "What's your role — design, operations, project management?"

---

## 2. Governing Standards

Claude must discover and record:

| Field | What to Elicit |
|-------|----------------|
| Primary codes | The codes that govern work (ASME, API, IEEE, etc.) |
| Company standards | Internal standards or templates, if any |
| Regulatory context | Regulatory bodies or compliance requirements, if any |

### How to Elicit

Ask:
- "What codes govern your work?"
- "Does your company have internal standards?"
- "Are there regulatory requirements?"

### How Standards Manifest

Standards appear in documents as:
- Explicit references ("per API 610 §5.2")
- Implicit constraints (design practices derived from codes)
- Verification requirements (testing per code requirements)

---

## 3. Document Types

Claude must discover what document types are natural to this domain.

### What to Elicit

For each document type the engineer produces:

| Field | What to Elicit |
|-------|----------------|
| Name | What they call it |
| Question | What question it answers |
| Nature | Descriptive, normative, directional, or operational |
| When used | What triggers the need for this document |

### Default Types

If the engineer doesn't have strong conventions, Claude may propose:

| Type | Question | Nature |
|------|----------|--------|
| Datasheet | "What is it?" | Descriptive |
| Specification | "What must it be?" | Normative |
| Guidance | "How should I think about it?" | Directional |
| Procedure | "How do I do it?" | Operational |

Claude adapts names and structures based on what's natural for the engineer.

### How to Elicit

Ask:
- "What documents do you typically produce?"
- "Who uses those documents?"
- "What makes a document 'good' vs. 'bad' in your context?"
- "What gets you in trouble if it's wrong or missing?"

---

## 4. Document Schemas

For each document type, Claude must discover its schema.

### What to Elicit

| Field | What to Elicit |
|-------|----------------|
| Sections | What sections the document contains |
| Purpose | What each section accomplishes |
| Required/Optional | Whether each section must be present |
| Content guidance | What belongs in each section |

### How to Elicit

Ask:
- "What sections does a [document type] typically have?"
- "What information must always be present?"
- "What's sometimes present depending on the situation?"
- "Are there templates you follow?"

Claude proposes schemas based on answers, then confirms with the engineer.

---

## 5. Cross-Document Relationships

Claude must discover how documents reference each other.

### What to Elicit

| Field | What to Elicit |
|-------|----------------|
| From | Which document contains references |
| To | Which document is referenced |
| Relationship | How they relate (entities appear in requirements, requirements trace to steps, etc.) |

### Why This Matters

Cross-document relationships enable coherence checking:
- Datasheet defines entity → Specification has requirements for it
- Specification has requirement → Procedure has steps to verify it
- Guidance provides rationale → Specification reflects that rationale

---

## 6. Quality Criteria

DOMAIN includes what "good" looks like in this domain.

### Section Quality

| Criterion | Description |
|-----------|-------------|
| Complete | Required information present |
| Consistent | No internal contradictions |
| Traceable | Claims trace to references or input |
| Verifiable | Statements can be checked |
| Clear | Competent reader can understand |

### Document Set Coherence

| Criterion | Description |
|-----------|-------------|
| No orphans | Everything referenced is defined |
| No contradictions | Documents agree on facts |
| Traceable | Requirements → entities, steps → requirements |
| Consistent terminology | Same terms mean same things |

### Domain-Specific Criteria

Claude should ask:
- "What makes a [document type] good vs. bad?"
- "What gets you in trouble if it's wrong?"
- "What do reviewers look for?"

---

## 7. Confirming DOMAIN

Before using DOMAIN for task work:

1. Claude summarizes the domain structure to the engineer
2. Engineer confirms or adjusts
3. DOMAIN is not final until the engineer approves

---

## 8. Storing DOMAIN

When Claude has elicited enough to define the domain:

- Save DOMAIN as a file for reuse across tasks
- Or hold in context for single-session use

A saved DOMAIN can be reused for all future tasks in that domain.

---

## 9. For Claude

When producing a DOMAIN:

1. Work through sections 1-6 via conversation
2. Don't present as a form — ask questions naturally
3. Propose structure based on answers
4. Confirm with engineer before finalizing
5. Store or hold the result for use with TASK

DOMAIN describes what the domain IS. It does not describe how to work — that belongs in METHOD (Guidance) and PROTOCOL (Procedure).
