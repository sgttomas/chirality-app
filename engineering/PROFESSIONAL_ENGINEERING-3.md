# Professional Engineering (Regulated, High-Stakes)

This project assumes **professional engineering is a regulated practice**: the work can affect life, safety, the environment, and property. In that context:

- **Accountability is personal and non-transferable.**
- **Judgement is exercised by the Professional.**
- **Tools can assist. Tools cannot hold responsibility.**

This file makes those boundaries explicit for *Chirality App* and for any agentic workflow used inside a professional engineering company.

---

## Framing: What Is an Agent?

From `WHAT-IS-AN-AGENT.md`:

**agent = LLM + instructions + access to files + use of tools**

Agents are *architectural components* in a system. They are not “engineers.” They do not practice engineering. They produce **artifacts** that must be verified and accepted by a Professional before they become engineering work product.

---

## The Core Claim

**Agentic systems are not new. We forgot that.**

Classical multi-agent systems studied: beliefs, goals, intentions, coordination, negotiation, and control under uncertainty.  
Modern LLMs reduce the cost of perception, reasoning, and communication, but **they do not redefine what an agent is**.

Agentic AI remains:

- a **system-level property**, not a model
- about **control, coordination, and goals over time**
- **architecturally inside AI**, not beyond it

The key architectural choice is the **cognitive space** the system operates in: what is **pre-structured** vs what is left **open**.  
Decompose before agents appear: isolate stable constraints and known transformations; leave only genuine uncertainty/combinatorics to agents.  
Design **cognitive boundaries**, not hand-wired flows.

---

## Professional Engineering Adds Non-Negotiables

Agentic architecture in regulated engineering must satisfy constraints that are *not optional*:

### 1) Responsible Charge (Decision Rights)
A Professional Engineer (or appropriately licensed professional) must retain:

- scope definition and boundary decisions
- selection of governing codes/standards and design bases
- hazard/risk acceptance criteria
- sign-off on calculations, drawings, specifications, and deliverables
- adjudication of conflicts between sources, requirements, or stakeholders
- approval of anything that could be construed as “final” engineering judgement

**Agents do not “approve.”** Agents may recommend, summarize, or propose—never decide.

### 2) Competence and Use-of-Tool Limits
Professional duty includes practicing only within competence and using tools appropriately.

For agentic systems this means:

- constrain tools to tasks where correctness can be validated
- prohibit agents from operating beyond the declared scope
- require escalation when uncertainty exceeds predefined thresholds
- document limitations: what the agent can and cannot be trusted to do

### 3) Traceability and Record
High-stakes engineering requires durable evidence:

- inputs (sources, versions, assumptions)
- transformations (methods, tool calls, intermediate artifacts)
- outputs (deliverables)
- verification (checks performed, by whom, when, with what results)

An agentic system must produce **audit-ready artifacts**, not merely “answers.”

### 4) Verification, Validation, and Independent Checking
Engineering is not “generate then ship.” It is:

- **verification**: did we build the thing right?
- **validation**: did we build the right thing?

For agentic workflows:

- verification must be **mechanized** where possible (validators, schemas, unit checks)
- validation remains a **human judgement** activity, supported by evidence

Where required, enforce **independent review** (second set of eyes) and **separation of duties**.

### 5) Safety Culture: Conservative, Explicit, and Explainable
In safety-critical domains:

- prefer conservative defaults
- represent uncertainty explicitly (ranges, confidence, known-unknowns)
- avoid “smooth talk” in lieu of evidence
- require explainability in terms of **artifacts and sources**, not rhetoric

---

## How Chirality Uses Agents in Professional Engineering Work

### The Human–Agent Contract

**Humans:**
- own intent, scope, acceptance, and accountability
- define constraints and success criteria
- decide what is “final”

**Agents:**
- execute bounded transformations
- generate candidate options and organize evidence
- surface inconsistencies, missing information, and risk
- produce structured artifacts for review

This maps cleanly onto the 3-layer agent model:

| Layer | Name | In Professional Practice |
|------:|------|--------------------------|
| Agent 0 | Architect | encodes practice boundaries, definitions, and governance rules |
| Agent 1 | Manager | decomposes work, routes tasks, enforces constraints, assembles evidence |
| Agent 2 | Specialist | performs narrow, checkable transformations and returns artifacts |

---

## Architecture Choices That Matter in Regulated Engineering

### 1) Define the Cognitive Boundary as a *Safety Boundary*
Treat the boundary like a safety function:

- **allowed actions** (tooling, file writes, communications)
- **forbidden actions** (final approvals, issuing external commitments)
- **required checks** (validators, peer review gates, sign-off)
- **escalation triggers** (ambiguous requirements, safety impact, missing inputs)

### 2) Make State First-Class and Inspectable
Do not rely on chat history as “the record.”

Maintain explicit state artifacts:
- scope ledger / SSOW
- assumptions register
- requirements & traceability matrix
- hazards register (as applicable)
- decisions log (who decided what, when, and why)
- verification log (checks, results, sign-offs)

### 3) Typed Actions and Gated Writes
The safest agent is one with a narrow action space:

- typed inputs/outputs (schemas)
- preconditions/postconditions
- write permissions constrained to specific directories
- “draft vs final” separation enforced by folder structure and naming

### 4) Pre-Structure Everything You Can Validate
If you can write a validator for it, you can structure it.

- deterministic transforms first (parsing, normalization, extraction)
- agentic reasoning reserved for open-ended parts (tradeoffs, exploration, synthesis)
- every agentic output must include: **source evidence + assumptions + uncertainty**

### 5) Monitoring and Recovery Are Part of the Design
Failures will happen. Your design must include:

- observability (logs, diffs, tool traces)
- rollback / revert strategy
- retry policies with bounded budgets
- “ask a human” as a defined control action

---

## What “Engineering” Means Here

Professional engineering is not merely producing content. It is:

- making commitments to reality under constraints
- managing risk under uncertainty
- producing defensible, reviewable work products
- being able to explain decisions and evidence years later

Agentic systems can amplify this—**if** they are built as *controlled systems* with explicit boundaries, evidence, and human decision rights.

---

## Operational Rules of Thumb

1. **Agents draft; Professionals decide.**
2. **No evidence → no acceptance.**
3. **Structure first; agents last.**
4. **Every output names assumptions and cites sources.**
5. **If safety, compliance, or public risk is plausible: escalate to human review by default.**

---

## Next Steps for This Repo

- Encode the above as **Agent 0 constraints** (governance + boundaries).
- Build Agent 1 workflows that enforce:
  - decomposition before execution
  - artifact-first outputs (ledgers, matrices, logs)
  - gating and sign-off points
- Keep Agent 2 roles narrow and testable.

This is how agentic systems become compatible with regulated engineering practice: **architecture + control + evidence**, with the Professional holding responsibility end-to-end.
