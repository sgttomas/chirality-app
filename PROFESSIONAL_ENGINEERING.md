# Professional Engineering with Agentic AI in Regulated Practice

Chirality AI
February 9, 2026
Date: 2026-02-09, Revision 0, Issued for Use

**Standard for the Design, Use, and Governance of AI Systems in High-Stakes Engineering**

A companion governance standard to the implementation standard for designing agents, available here: https://github.com/sgttomas/chirality-app/blob/main/agents/AGENT_HELPS_HUMANS.md

---

## Preamble

This document defines the professional practice standard for designing and using AI (including agentic workflows) inside regulated engineering practice: work that can affect public safety, the environment, property, critical infrastructure, and public trust.

It is written to keep one fact unambiguous:

> AI can accelerate engineering work. It cannot inherit professional responsibility.

Professional engineering is a duty-of-care practice: commitments to reality under uncertainty, made by accountable professionals, supported by evidence that can withstand review.

AI changes the cost of drafting, searching, reconciling, and summarizing. AI does not change what regulators, clients, insurers, courts, and the public require: competence, independent judgment, verification, assumption of responsibility, and a durable project record.

---

## 1. Definitions and Scope

### 1.1 What Is an "Agent"?

An agent is a controlled system architecture in which decisions are made:

Agent = Model + Instructions + Tools + Files Access + Governance

- Model: The cognitive engine (e.g., an LLM) that generates interpretations, candidates, and communication.
- Instructions: The written operating contract that constrains and shapes the model’s behavior, such as role, scope, invariants, required inputs/outputs, evidence rules, stop conditions, and permitted write actions. For Chirality AI this is the AGENT_*.md spec that makes behavior repeatable and auditable.
- Tools: The bounded action interface between the agent and the world that the model itself is in control of (primarily) and may use at the behest of the user (secondarily). This includes: file reads/writes, validators, calculators, extractors, APIs, build/test commands.
- Files Access: The agent’s governed ability to read and (optionally) write to the project’s authoritative artifacts in the filesystem.
- Governance: The control layer that orchestrates what is allowed and how agents and humans interact. The decision points and workflows are engineered for validation of outputs and assumption of professional responsibility.

The model provides the cognitive substrate (reasoning, perception). The architecture provides the agency (control, memory, safety). "Agentic" is therefore not a property of a model but of the system it operates within: state, control loops, tool access, environment, and constraints.

### 1.2 Agency Is a System Property

Models generate candidates. Systems decide what candidates are allowed, what actions can be taken, what evidence is required, and when to stop and ask a human.

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

No AI system may claim to certify, approve, sign, seal, or issue engineering work for reliance.

We practice Human-at-the-Gate: agents may execute work within bounded states, but only a human professional engineer can open the gate that transitions a draft to a deliverable.

### 2.3 Competence Includes Tool Competence

An engineer must not use an agent to perform work they are not competent to verify manually. Using AI you cannot adequately verify is a competence failure. "An AI said so" is never a defensible basis of design.

### 2.4 Evidence Over Plausibility

Engineering does not accept "sounds right." Engineering accepts:

- Inputs and sources
- Assumptions
- Methodology
- Verification evidence
- Uncertainty and limitations

### 2.5 Hierarchy of Authority

Agents cannot assume responsibility for professional outputs. Engineers follow a hierarchy of authority in technical matters as follows:

1. Laws/regulations
2. Codes/standards
3. Project specifications / design basis (approved for use)
4. Verified engineering analysis + published literature
5. Professional judgment

#### 2.5.1 Role of Agents in the Hierarchy of Authority

Agent outputs carry no professional authority for reliance. They are drafts/decision support unless explicitly accepted and issued by an accountable professional.

Unknowns are explicit. Agents must output TBD or UNKNOWN rather than guess a plausible value. Any gap filled by the agent must be logged in an Assumptions_Register.

Conflicts are surfaced. If Source A says "100 MPa" and Source B says "120 MPa," the agent's job is not to pick the average or choose one silently. It is to halt and report the conflict with pointers to the disagreeing sources.

Sources and constraints are organized for people to validate.

### 2.6 Provenance Is Mandatory

Every extraction, summary, or parameter value should cite its source file and section. Every output artifact must trace back to a specific set of input constraints and a specific version of the agent instructions. "Trust me" is not an engineering concept. The Engineer needs a validation record to assume responsibility for the output.

### 2.7 Assume Failure Over Time

Agentic failure modes are trajectory failures: drift, compounding errors, silent corruption. Monitoring, verification, and recovery are part of the architecture, not add-ons.

## 3. The Human–AI Contract

Humans (accountable professionals) are responsible for:

- Defining intent, scope, and acceptance criteria
- Choosing codes, standards, and key assumptions
- Deciding what "done" means and what is safe to rely on
- Approving changes that affect deliverables
- Performing or commissioning independent review where required
- Accepting residual risk

AI systems may:

- Draft and format deliverables under explicit templates
- Extract, normalize, cross-reference, and summarize evidence
- Generate candidate alternatives and tradeoff tables
- Surface gaps, inconsistencies, and interface conflicts
- Run bounded, checkable transformations (with validators)


AI outputs are drafts and decision support. Human acceptance is what makes them engineering work product.

## 4. Cognitive Boundaries

Before any agent runs, the type of behaviors the agent can engage in and the focus of its attention for domain awareness must be defined. We do not ask agents to "figure it out." We define what is deterministic and what is genuinely probabilistic. This is defined further in AGENT_HELPS_HUMANS.md.

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

Rule of thumb: If you can write a validator for it, structure it. Reserve agent cognition for what you cannot.

## 5. Architecture Requirements

### 5.1 The Filesystem Is the System of Record

In professional practice, State = Liability. Deliverables and logs live as files under version control.

- Artifact-First: Agents must read from and write to the filesystem.
- No Hidden Memory: If a decision is not in a versioned file, does not exist for purposes of reliance.

Git History Is the Development Record: Version control enables meaningful diffs for review, reproducibility, rollback, and audits that do not depend on vendor systems or transient chats.

### 5.2 State Must Be First-Class and Inspectable

Minimum state artifacts (risk-proportionate):

- Scope Ledger: What is in scope and what is out.
- Assumptions Register: Every assumption, its source, and its status.
- Decisions Log: Who decided, when, why, and what alternatives were considered.
- Requirements / Traceability Matrix: Requirements linked to verification evidence.
- Hazards / Risk Register: Identified hazards, controls, and residual risk (as applicable).
- Verification Log: Checks run, results, and sign-offs.
- Change Log: What changed, why, and its impact.

### 5.3 Typed Actions and Gated Writes

- Do not give AI "do anything" powers.
- Define a limited action vocabulary (read, extract, propose, write-draft, etc.)
- Enforce preconditions and postconditions on every action
- Validate outputs (schemas, linters, tests, cross-file consistency)
- Require explicit human approval for risky operations (writes to controlled areas, deletions, scope expansion)

For an implementation of this agent design standard, see AGENT_HELPS_HUMANS.md https://github.com/sgttomas/chirality-app/blob/main/agents/AGENT_HELPS_HUMANS.md

### 5.4 Verification and Validation

Verification (mechanized where possible): Automate checks — schemas, math, linting, consistency, unit tests, cross-references.
Validation (human judgment): Confirm the right problem is being solved and the solution is fit-for-purpose, supported by evidence.

Where practice requires it, enforce independent review and separation of duties.

### 5.5 Instruction Governance Is Release Engineering

Agent operating instructions are part of the system. Treat them like controlled software:

- Versioned and auditable
- Reviewed before release
- No silent behavior changes
- Clear release notes for material changes
- Test coverage for high-risk workflows

Any change to AGENT_*.md that alters write scope, tool access, or outputs requires review and a recorded release note.

## 6. The Three-Layer Governance Model

To maintain control across complex projects, decompose agency into three distinct roles with clear boundaries of authority:

- The Type 0 layer, acting as the Director, is responsible for governance. It defines the "rules" of the project, including standards, schemas, templates, safety rules, and the boundaries within which all other agents operate. This layer is analogous to the role of a Principal or Chief Engineer.

- The Type 1 layer, functioning as the Manager, handles orchestration. It plans workflows, decomposes tasks, routes information, assembles evidence packages, and monitors progress against acceptance criteria. This role is similar to that of a Project Manager or Lead.

- The Type 2 layer, serving as the Specialist, focuses on execution. It performs narrow, stateless, checkable tasks such as "Extract Loads from Document X" or "Format Specification per Template Y." This layer is comparable to the role of a Junior Engineer or Designer.

A Type 2 agent cannot modify the rules set by Type 0. A Type 1 agent cannot approve deliverables for external reliance. Authority flows downward; escalation flows upward.

## 7. Review Gates for Reliance (Risk-Proportionate)

Every deliverable passes through a repeatable gate sequence before it is relied upon. AI can assemble the evidence pack. Humans pass or fail the gate.

Gate A: Completeness
Gate B: Traceability
Gate C: Verification
Gate D: Approval/Issuance

## 8. Professional Competence

Train for competence: how to review AI outputs, how to detect hallucination and omission, how to maintain independent judgment, and how to operate within the governance model.

Engage stakeholders early: regulators, clients, insurers, and QA leads — align expectations around auditability, record-keeping, and reliance.

## 9. Closing Principle

Engineer a harness that allows judgment to scale.

AI becomes compatible with regulated professional engineering when it is engineered into a controlled system: structure first, bounded actions, evidence and auditability, monitoring and recovery, humans retaining decision rights and responsibility.

If we cannot make it auditable, we cannot rely on it.

Use AI to widen and organize the field of consideration; use professional judgment to narrow, accept, and issue.

That preserves what professional work outputs mean: a competent person warrants this under duty of care, backed by an auditable record.

## 10. Responsible Member

I take responsibility for adopting this standard internally and ensuring it’s used appropriately at Chirality AI, as part of the Professional Practice Management Plan (PPMP.

-Ryan Tufts, P.Eng. (APEGA 78780 | Feb 9, 2026. |. Chirality AI (APEGA P17007)