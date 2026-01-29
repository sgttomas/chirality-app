---
doc_id: CF-SPEC
doc_kind: governance.spec
layer: build
status: draft

refs:
  - rel: governed_by
    to: CF-CHANGE
  - rel: implements
    to: CF-CHARTER
  - rel: implements
    to: CF-PROBLEM
  - rel: depends_on
    to: CF-TYPES
  - rel: constrained_by
    to: CF-CONTRACT
---

# CF-SPEC: Governance Substrate Agent Specification

## 1. Overview

### 1.1 What This Document Is

This specification defines the mechanics of the Governance Substrate Agent—how it works, what it produces, and how a Claude instance should execute it.

### 1.2 The Core Realization

The execution interface for governed knowledge work already exists: Claude with file access, iterating on documents with human approval. Building a separate execution platform is unnecessary.

What's missing is the **intake layer**: a structured process that transforms messy human problem statements into documentation that Claude can execute against effectively.

**The Governance Substrate Agent is that intake layer.**

It solves two skill gaps that prevent non-technical domain experts from using LLMs effectively:

1. **Prompting effectively** — Knowing what context to provide and how to structure requests
2. **Multi-step problem tracking** — Keeping coherent state across complex, iterative work

The pipeline produces structured documentation. That documentation becomes the work surface for any capable LLM.

### 1.3 Relationship to Execution

```
┌─────────────────────────────────────────────────────────────┐
│                  GOVERNANCE SUBSTRATE AGENT                  │
│                        (This Tool)                           │
│                                                              │
│   Problem Statement                                          │
│         ↓                                                    │
│   Stage 1: Intermediate Documents                            │
│   (Datasheet, Specification, Guidance, Procedure)            │
│         ↓                                                    │
│   Stage 2: Strongly-Typed Substrate                          │
│   (CHARTER, TYPES, CONTRACT, SPEC, DIRECTIVE, PLAN, CHANGE)  │
│         ↓                                                    │
│   Output: Governed Documentation                             │
└─────────────────────────────────────────────────────────────┘
                           ↓
                    (handoff point)
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                    EXECUTION INTERFACE                       │
│                  (Claude with file access)                   │
│                                                              │
│   Input: Governed documentation from substrate               │
│   Process: Iterative work with human review                  │
│   Output: Approved artifacts with evidence                   │
└─────────────────────────────────────────────────────────────┘
```

The substrate documents become the work surface for execution. This spec focuses on producing the substrate.

---

## 2. Core Concepts

### 2.1 Task

The unit of work through the pipeline. One problem statement produces one substrate.

```
Task
  id: string
  problem_statement: string | Reference (the human's initial input)
  stage: stage_1 | stage_2 | completed
  created_at: timestamp
  completed_at: timestamp | null
```

### 2.2 Reference

A pointer to external content.

```
Reference
  type: file | url | inline
  path: string (file path, URL, or content directly)
  description: string (what this reference contains)
```

### 2.3 Intermediate Documents

Human-facing forms familiar to heavy industry.

```
IntermediateDocumentSet
  datasheet: Document      # "What is it?"
  specification: Document  # "What must it be?"
  guidance: Document       # "How should I think about it?"
  procedure: Document      # "How do I do it?"

Document
  id: string
  content: structured markdown
  gaps: Gap[] (fields that need human input)
  status: draft | approved
```

### 2.4 Substrate Documents

Strongly-typed governance documentation.

```
SubstrateDocumentSet
  charter: Document    # Axiology — what matters
  types: Document      # Ontology — what exists
  contract: Document   # Epistemology — what must be true
  spec: Document       # Syntax — how it's structured
  directive: Document  # Praxeology — how to operate
  plan: Document       # Instance — what to do now
  change: Document     # Governance — how to evolve
```

### 2.5 Gap

A field that requires human input.

```
Gap
  document_id: string
  section: string
  field: string
  question: string (targeted question for human)
  context: string (why this matters)
  answer: string | null
```

### 2.6 Iteration

One pass through the pipeline loop.

```
Iteration
  id: string
  task_id: string
  stage: stage_1 | stage_2
  sequence: integer

  # What the agent produced
  documents: IntermediateDocumentSet | SubstrateDocumentSet
  gaps_identified: Gap[]
  coherence_issues: CoherenceIssue[]

  # Human response
  decision: pending | approved | rejected
  feedback: string | null
  gap_answers: GapAnswer[]
  decided_by: string
  decided_at: timestamp | null
```

### 2.7 CoherenceIssue

A contradiction or misalignment across documents.

```
CoherenceIssue
  id: string
  documents_involved: string[] (which documents conflict)
  description: string
  severity: warning | error
  resolution: string | null (how it was resolved)
```

### 2.8 GapAnswer

Human's response to a targeted question.

```
GapAnswer
  gap_id: string
  answer: string
  destination: string (which document.section.field receives this)
```

---

## 3. Pipeline Definition

### 3.1 Two-Stage Structure

**Stage 1: Problem Statement → Intermediate Documents**

- Input: Raw problem statement, references, artifacts
- Output: Datasheet, Specification, Guidance, Procedure
- Gate: Human approval

**Stage 2: Intermediate Documents → Substrate**

- Input: Approved intermediate documents
- Output: CHARTER, TYPES, CONTRACT, SPEC, DIRECTIVE, PLAN, CHANGE
- Gate: Human approval

### 3.2 Three-Pass Pattern

Each stage follows the same iterative pattern:

| Pass | Name | Purpose |
|------|------|---------|
| **Pass 1** | Parse → Map → Populate | Extract content from input, place in appropriate fields |
| **Pass 2** | Cross-Document Inference | Use populated content to fill gaps—documents inform each other |
| **Pass 3** | Coherence Check | Find contradictions and misalignments across documents |

**Flow within a stage:**

```
Input documents
       ↓
   [Pass 1: Parse → Map → Populate]
       ↓
   [Pass 2: Cross-Document Inference]
       ↓
   [Pass 3: Coherence Check]
       ↓
   Gaps or coherence issues found?
       ↓ yes                    ↓ no
   [Q&A with human]         [Present for approval]
       ↓                        ↓
   [Incorporate answers]    Human approves?
       ↓                        ↓ yes        ↓ no
   [Pass 2]                  Stage complete  [Incorporate feedback]
       ↓                                          ↓
   [Pass 3]                                   [Pass 2]
       ↓                                          ↓
   Loop until stable ←──────────────────────  [Pass 3]
                                                  ↓
                                              Loop
```

### 3.3 Cross-Document Inference Rules

**Stage 1 (Intermediate Documents):**

- Datasheet entities → Specification must have requirements for them
- Specification constraints → Procedure must have steps to verify them
- Guidance principles → Specification priorities should reflect them
- Procedure steps → Datasheet should define things being acted upon

**Stage 2 (Substrate):**

- CHARTER values → propagate to all documents
- TYPES entities → CONTRACT invariants must reference defined types
- CONTRACT invariants → SPEC schemas must support verification
- SPEC schemas → DIRECTIVE policies must operate on defined structures
- DIRECTIVE policies → PLAN must respect execution semantics

### 3.4 Q&A Protocol

Questions are:

1. **Anchored** — "Datasheet §2.3 defines X, but Specification has no requirements for X. Is this intentional?"
2. **Targeted** — Each answer has a specific destination (document.section.field)
3. **Actionable** — The human can answer without needing to understand the full system
4. **Batched** — Related questions are grouped to reduce round-trips

Questions are NOT:

- "Tell me about your project"
- Open-ended discovery (that's what the problem statement is for)
- Repeated across iterations (track what's been asked)

### 3.5 Termination Conditions

**Within-stage loop terminates when:**

- Pass 3 finds no coherence issues, AND
- No gaps remain that require human input, AND
- Human approves the document set

**Stage 1 terminates when:**

- Intermediate documents are approved
- Human may edit documents before proceeding to Stage 2

**Stage 2 terminates when:**

- Substrate documents are approved
- Documents are saved as the governed substrate

---

## 4. Invariants

These rules must hold for any implementation.

### 4.1 Pipeline Invariants

1. **Sequential stages** — Stage 2 cannot begin until Stage 1 is approved
2. **Human approval required** — Each stage gate requires explicit human approval
3. **No silent resolution** — Ambiguities surface as questions, never resolved silently
4. **Answers have destinations** — Every Q&A answer maps to a specific document field
5. **Documents are immutable after approval** — Approved documents are not modified (start new task if changes needed)

### 4.2 Document Invariants

6. **Cross-document consistency** — Entities referenced in one document must be defined in another
7. **No orphan requirements** — Specification requirements must trace to Datasheet entities
8. **No orphan procedures** — Procedure steps must trace to Specification requirements
9. **Substrate ordering** — Documents are developed in order: CHARTER → TYPES → CONTRACT → SPEC → DIRECTIVE → PLAN → CHANGE

### 4.3 Q&A Invariants

10. **Questions are scoped** — Every question references a specific document and section
11. **No repeated questions** — Once answered, a question is not asked again
12. **Gaps are explicit** — Unpopulated required fields are tracked as gaps, not ignored

---

## 5. Document Schemas

### 5.1 Intermediate Document Schemas

#### Datasheet

```markdown
# Datasheet: [Name]

## 1. Overview
[What this thing is at a high level]

## 2. Entities
### 2.1 [Entity Name]
- Description:
- Attributes:
- Relationships:

## 3. Architecture
[How entities relate, system structure]

## 4. Terminology
| Term | Definition |
|------|------------|

## 5. References
[Source materials, standards, prior work]
```

#### Specification

```markdown
# Specification: [Name]

## 1. Scope
[What this specification covers]

## 2. Requirements
### 2.1 [Requirement ID]
- Statement:
- Rationale:
- Verification:
- Traces to: [Datasheet reference]

## 3. Constraints
[Boundaries, limitations, non-negotiables]

## 4. Acceptance Criteria
[What "done" looks like]
```

#### Guidance

```markdown
# Guidance: [Name]

## 1. Context
[Why this guidance exists]

## 2. Principles
### 2.1 [Principle Name]
- Statement:
- Rationale:
- Implications:

## 3. Priorities
[How to make tradeoffs]

## 4. Anti-patterns
[What to avoid and why]
```

#### Procedure

```markdown
# Procedure: [Name]

## 1. Purpose
[What this procedure accomplishes]

## 2. Prerequisites
[What must be true before starting]

## 3. Steps
### Step 1: [Name]
- Action:
- Inputs:
- Outputs:
- Verification:

## 4. Completion Criteria
[How to know you're done]
```

### 5.2 Substrate Document Schemas

Substrate documents follow the patterns established in CF-CHARTER and CF-PROBLEM. Each includes:

- Frontmatter with doc_id, doc_kind, layer, status, refs
- Structured sections appropriate to the document type
- Cross-references to sibling documents

Detailed schemas for TYPES, CONTRACT, SPEC, DIRECTIVE, PLAN, CHANGE to be defined in their respective documents.

---

## 6. Execution Instructions

### 6.1 For a Fresh Claude Instance

When starting a new session to continue this work:

1. **Read these documents in order:**
   - CF-README.md (orientation)
   - CF-PROBLEM.md (problem statement)
   - CF-CHARTER.md (scope and values)
   - CF-SPEC.md (this document—mechanics)

2. **Identify current state:**
   - Which stage? (Stage 1 or Stage 2)
   - Which pass? (Pass 1, 2, or 3)
   - Any pending gaps or coherence issues?
   - Any pending human approval?

3. **Execute the appropriate pass:**
   - Follow the three-pass pattern
   - Surface questions via Q&A protocol
   - Wait for human input at gates

4. **Maintain coherence:**
   - When modifying one document, check siblings
   - Track gaps explicitly
   - Never resolve ambiguity silently

### 6.2 Running the Pipeline

**To start Stage 1:**

```
Human provides: Problem statement, references, artifacts
Agent executes: Pass 1 → Pass 2 → Pass 3 → Q&A loop → Approval gate
Output: Approved intermediate documents (Datasheet, Specification, Guidance, Procedure)
```

**To start Stage 2:**

```
Input: Approved intermediate documents (may have human edits)
Agent executes: Pass 1 → Pass 2 → Pass 3 → Q&A loop → Approval gate
Output: Approved substrate (CHARTER, TYPES, CONTRACT, SPEC, DIRECTIVE, PLAN, CHANGE)
```

**After Stage 2:**

The substrate documents are complete. They can be handed to any capable LLM for execution work. The execution interface is Claude with file access—no additional tooling required.

### 6.3 Handoff to Execution

When the substrate is complete, execution works as follows:

1. Human creates a **task** (what they want to accomplish)
2. Human provides the **substrate documents** as context
3. Claude produces **candidate output** (documents, artifacts, analysis)
4. Claude self-critiques with **observations** (assumptions, deviations, concerns)
5. Human **reviews** the candidate with observations as orientation
6. Human **approves** or **rejects with feedback**
7. If rejected, Claude iterates with feedback
8. If approved, work is complete

This execution pattern requires no special tooling—it's standard Claude interaction with file access.

---

## 7. What This Specification Does NOT Cover

Explicitly out of scope:

1. **Execution platform** — Claude is the execution interface
2. **UI/UX design** — Conversational interface is sufficient
3. **Infrastructure** — Files and git are sufficient
4. **Orchestration** — Human directs the agent through stages
5. **Domain-specific content** — Schemas are domain-agnostic; content comes from human

---

## 8. Success Criteria

The Governance Substrate Agent succeeds when:

1. A human can provide a problem statement and receive structured intermediate documents
2. Intermediate documents can be transformed into a strongly-typed substrate
3. The substrate is internally coherent (documents reference each other consistently)
4. A fresh Claude instance can execute work against the substrate without additional context
5. The human did not need to understand prompt engineering or LLM mechanics

---

## 9. Next Steps

After this specification:

1. **CF-TYPES.md** — Define the domain model and terminology
2. **CF-CONTRACT.md** — Define invariants and verification requirements
3. **Test the pipeline** — Run Stage 1 on a real problem statement
4. **Iterate** — Refine based on what works and what doesn't

The goal is a working pipeline, not a perfect specification. Build, test, learn.
