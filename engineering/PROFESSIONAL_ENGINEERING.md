# Professional Engineering with Agentic AI in Regulated Practice
_Date: 2026-02-09_
Revision 0
Issued for Use
Chirality AI (APEGA P17007)

**Standard for the Design, Use, and Governance of AI Systems in High-Stakes Engineering**

A companion governance standard to the implementation standard for designing agents, called `AGENTS_HELPS_HUMANS.md` 

---

## Preamble

This document defines the **professional practice standard** for designing and using AI (including agentic workflows) inside **regulated engineering practice**: work that can affect public safety, the environment, property, critical infrastructure, and public trust.

It is written to keep one fact unambiguous:

> **AI can accelerate engineering work. It cannot inherit professional responsibility.**

Professional engineering is a **duty-of-care practice**: commitments to reality under uncertainty, made by accountable professionals, supported by evidence that can withstand review.

AI changes the cost of drafting, searching, reconciling, and summarizing. AI does **not** change what regulators, clients, insurers, courts, and the public require: competence, independent judgment, verification, assumption of responsibility, and a durable project record.

This document rests on a single axiom:

> **AI can accelerate engineering work. It cannot inherit professional responsibility.**

In regulated, high-stakes environments — where failure harms life, public safety, or critical infrastructure — Artificial Intelligence is not a replacement for engineering judgment. It is a material that must be engineered.

---

## 1. Definitions and Scope

### 1.1 What Is an "Agent"?

An agent is not a model. It is a **controlled system architecture**:

```
Agent = Model + Instructions + Tools + State + Governance
```

The model provides the cognitive substrate (reasoning, perception). The *architecture* provides the agency (control, memory, safety). "Agentic" is therefore not a property of a model but of the **system** it operates within: state, control loops, tool access, environment, and constraints.

### 1.2 Agency Is a System Property

Models generate candidates. **Systems** decide what candidates are allowed, what actions can be taken, what evidence is required, and when to stop and ask a human.

---

## 2. Non-Negotiables

These are the minimum bar for professional reliance. They are not aspirational; they are binding constraints on any workflow that produces work product for regulated engineering.

### 2.1 Public Welfare Is the First Constraint

When tradeoffs exist, safety and harm reduction win. Commercial pressure, schedule, and convenience do not override this obligation.

### 2.2 Responsible Charge Stays Human (The Engineer-of-Record Principle)

Professional liability is personal and non-transferable. A licensed professional (Engineer-of-Record or equivalent) retains decision rights for:

- Scope and boundary decisions
- Selection of governing codes, standards, and design basis
- Hazard and risk acceptance, including residual risk statements
- Conflict adjudication where judgment is required
- Approval, issuance, signature, seal, and transmittal for reliance

**No AI system may claim to certify, approve, sign, seal, or issue engineering work for reliance.**

We practice **Human-at-the-Gate**: agents may execute work within bounded states, but only a human professional engineer can open the gate that transitions a draft to a deliverable.

### 2.3 Competence Includes Tool Competence

An engineer must not use an agent to perform work they are not competent to verify manually. Using AI you cannot adequately verify is a competence failure. "An AI said so" is never a defensible basis of design.

### 2.4 Evidence Over Plausibility

Engineering does not accept "sounds right." Engineering accepts:

- Inputs and sources (cited)
- Assumptions (clearly labeled)
- Method (stated and appropriate)
- Verification evidence (checks run, results recorded)
- Uncertainty and limits (explicit)

### 2.5 Hierarchy of Authority

Agents cannot assume responsibility for professional outputs. Engineers follow a hierarchy of authority in technical matters as follows:
1. Laws and Regulation
2. Codes and Standards
3. Specifications (stamped / approved for use)
4. Published technical literature and professional judgment
5. Project / task needs

#### 2.5.1 Role of Agents in the Hierarchy of Authority

Agents and the outputs they produce carry no authority at all.  

- **Unknowns are explicit.** Agents must output `TBD` or `UNKNOWN` rather than guess a plausible value. Any gap filled by the agent must be logged in an `Assumptions_Register`.
- **Conflicts are surfaced.** If Source A says "100 MPa" and Source B says "120 MPa," the agent's job is not to pick the average or choose one silently. It is to **halt and report the conflict** with pointers to the disagreeing sources.
- **Sources and constraints are organized** for people to validate.

### 2.6 Provenance Is Mandatory

Every extraction, summary, or parameter value should cite its source file and section. Every output artifact must trace back to a specific set of input constraints and a specific version of the agent instructions. "Trust me" is not an engineering concept.  The Engineer needs a validation record to assume responsibility for the output.

### 2.7 Assume Failure Over Time

Agentic failure modes are trajectory failures: drift, compounding errors, silent corruption. Monitoring, verification, and recovery are part of the architecture, not add-ons.

---

## 3. The Human–AI Contract

### Humans (accountable professionals) are responsible for:

- Defining intent, scope, and acceptance criteria
- Choosing codes, standards, and key assumptions
- Deciding what "done" means and what is safe to rely on
- Approving changes that affect deliverables
- Performing or commissioning independent review where required
- Accepting residual risk

### AI systems may:

- Draft and format deliverables under explicit templates
- Extract, normalize, cross-reference, and summarize evidence
- Generate candidate alternatives and tradeoff tables
- Surface gaps, inconsistencies, and interface conflicts
- Run bounded, checkable transformations (with validators)

**AI outputs are drafts and decision support. Human acceptance is what makes them engineering work product.**

---

## 4. Cognitive Boundaries

Before any agent runs, the cognitive space must be pre-structured. We do not ask agents to "figure it out." We define what is deterministic and what is genuinely probabilistic.

### 4.1 The Deterministic Layer (Validator-Friendly)

If a task can be validated by a schema, it must be constrained by a schema. This layer includes:

- Schemas, naming conventions, and lifecycle states
- Registers (assumptions, decisions, requirements, hazards, interfaces)
- Deterministic transforms (parse → normalize → check → render)
- Permission maps and write zones
- Checklists and runbooks

### 4.2 The Probabilistic Layer (Agent Cognition)

Agents are reserved for work that genuinely requires inference under uncertainty:

- Interpreting ambiguous or unstructured text
- Proposing candidate decompositions and options
- Reconciling tradeoffs (explicitly, with rationale)
- Exception investigation and anomaly flagging
- Combinatorial search (sorting, matching, drafting)

**Rule of thumb:** If you can write a validator for it, structure it. Reserve agent cognition for what you cannot.

---

## 5. Architecture Requirements

### 5.1 The Filesystem Is the System of Record

In professional practice, **State = Liability**. Deliverables and logs live as files under version control.

- **Artifact-First:** Agents must read from and write to the filesystem.
- **No Hidden Memory:** If a decision is not in a versioned file, it does not exist.
- **Git History Is the Legal Record:** Version control enables meaningful diffs for review, reproducibility, rollback, and audits that do not depend on vendor systems or transient chats.

### 5.2 State Must Be First-Class and Inspectable

Minimum state artifacts (risk-proportionate):

| Artifact | Purpose |
| :--- | :--- |
| **Scope Ledger** | What is in scope and what is out |
| **Assumptions Register** | Every assumption, its source, and its status |
| **Decisions Log** | Who decided, when, why, and what alternatives were considered |
| **Requirements / Traceability Matrix** | Requirements linked to verification evidence |
| **Hazards / Risk Register** | Identified hazards, controls, and residual risk (as applicable) |
| **Verification Log** | Checks run, results, and sign-offs |
| **Change Log** | What changed, why, and its impact |

### 5.3 Typed Actions and Gated Writes

Do not give AI "do anything" powers.

- Define a limited action vocabulary (read, extract, propose, write-draft, etc.)
- Enforce preconditions and postconditions on every action
- Validate outputs (schemas, linters, tests, cross-file consistency)
- Require explicit human approval for risky operations (writes to controlled areas, deletions, scope expansion)

See `AGENT_HELPS_HUMANS.md` for an implementation of this agent design standard.

### 5.4 Verification and Validation

- **Verification (mechanized where possible):** Automate checks — schemas, math, linting, consistency, unit tests, cross-references.
- **Validation (human judgment):** Confirm the right problem is being solved and the solution is fit-for-purpose, supported by evidence.

Where practice requires it, enforce **independent review** and **separation of duties**.

### 5.5 Instruction Governance Is Release Engineering

Agent operating instructions are part of the system. Treat them like controlled software:

- Versioned and auditable
- Reviewed before release
- No silent behavior changes
- Clear release notes for material changes
- Test coverage for high-risk workflows

---

## 6. The Three-Layer Governance Model

To maintain control across complex projects, decompose agency into three distinct roles with clear boundaries of authority:

| Layer | Role | Scope | Responsibility | Human Equivalent |
| :--- | :--- | :--- | :--- | :--- |
| **Type 0** | **Architect** | Governance | Defines the "rules" of the project: standards, schemas, templates, safety rules, and the boundaries within which all other agents operate. | Principal / Chief Engineer |
| **Type 1** | **Manager** | Orchestration | Plans workflows, decomposes tasks, routes information, assembles evidence packages, and monitors progress against acceptance criteria. | Project Manager / Lead |
| **Type 2** | **Specialist** | Execution | Performs narrow, stateless, checkable tasks (e.g., "Extract Loads from Document X," "Format Specification per Template Y"). | Junior Engineer / Designer |

A Type 2 agent cannot modify the rules set by Type 0. A Type 1 agent cannot approve deliverables for external reliance. Authority flows downward; escalation flows upward.

---

## 7. Review Gates for Reliance (Risk-Proportionate)

### 7.1 The Gate Model

Every deliverable passes through a repeatable gate sequence before it is relied upon:

| Gate | Question | Who Can Pass It |
| :--- | :--- | :--- |
| **Gate A — Completeness** | Is the scope stated? Are required sections present? Are TBDs listed? | Type 1 agent or human |
| **Gate B — Traceability** | Do claims map to sources? Are assumptions labeled? Are conflicts surfaced? | Type 1 agent or human |
| **Gate C — Verification** | Do appropriate checks, tests, and calculations exist and pass? | Automated + human review |
| **Gate D — Approval** | Has the accountable professional reviewed and signed off for reliance? | **Human only (EoR)** |

AI can assemble the evidence pack. Humans pass or fail the gate.

---

## 8. Path Forward (Implementation Sequence)

### Phase 1 — Foundations
1. **Write the jurisdiction addendum:** governing regulators, applicable codes and standards, sealing and signature rules, record retention requirements, confidentiality and data handling, required review and independence rules.
2. **Stand up the minimum artifact set:** scope, assumptions, decisions, requirements, hazards (if applicable), verification, and change control.

### Phase 2 — Tooling
3. **Build validators and evidence tooling:** schemas, linters, cross-file consistency checks, traceability reports, and automated gate evidence assembly.
4. **Define the action vocabulary:** typed agent actions with preconditions, postconditions, and permission boundaries.

### Phase 3 — Governance
5. **Define decision rights and gates:** who decides what, what requires review, what cannot be automated, and what constitutes adequate independent review.
6. **Establish instruction governance:** versioning, review, testing, and release process for all agent operating instructions.

### Phase 4 — Capability
7. **Train for competence:** how to review AI outputs, how to detect hallucination and omission, how to maintain independent judgment, and how to operate within the governance model.
8. **Engage stakeholders early:** regulators, clients, insurers, and QA leads — align expectations around auditability, record-keeping, and reliance.

---

## 9. Closing Principle

AI becomes compatible with regulated professional engineering when it is **engineered into a controlled system**: structure first, bounded actions, evidence and auditability, monitoring and recovery, humans retaining decision rights and responsibility.

If we cannot make it auditable, we cannot rely on it.

Use AI to widen and organize the field of consideration; use professional judgment to narrow, accept, and issue. 

That preserves what professional work outputs mean: a competent person warrants this under duty of care, backed by an auditable record. 

Engineer a harness that allows judgment to scale.


