# Professional Engineering with Artificial Intelligence in Regulated Contexts
_Date: 2026-02-09_

This document defines the **professional practice standard** for designing and using AI (including agentic workflows) inside **regulated, high‑stakes engineering**: work that can affect public safety, the environment, property, critical infrastructure, and public trust.

It is written to keep one fact unambiguous:

> **AI can accelerate engineering work. It cannot inherit professional responsibility.**

---

## 1) The core stance

Professional engineering is a **duty-of-care practice**: commitments to reality under uncertainty, made by accountable professionals, supported by evidence that can withstand review.

AI changes the cost of drafting, searching, reconciling, and summarizing.  
AI does **not** change what regulators, clients, insurers, courts, and the public require:

- **competence**
- **independent judgment**
- **traceability**
- **verification**
- **responsible charge / decision rights**
- **a durable project record**

If the workflow cannot produce an auditable record and a defensible basis for decisions, it is not acceptable for regulated engineering reliance.

---

## 2) Definitions we use (so we can govern them)

### 2.1 What is an “agent” here?

```
agent = model + operating instructions + access to files + use of tools
```

An “agentic” system is not a personality. It is a **closed-loop controller** operating over time with state, actions, feedback, and constraints.

### 2.2 “Agency is a system property”
Models generate candidates.  
**Systems** decide what candidates are allowed, what actions can be taken, what evidence is required, and when to stop and ask a human.

If you want safe agentic behavior, you do not “prompt harder”; you **engineer the control surface**.

---

## 3) Non‑negotiables (regulated engineering constraints)

These are not “nice to have.” They are the minimum bar for professional reliance.

### 3.1 Public welfare is the first constraint
When tradeoffs exist, safety and harm reduction win. Commercial pressure does not override this.

### 3.2 Responsible charge stays human
A licensed professional (Engineer‑of‑Record or equivalent) retains decision rights for:

- scope and boundary decisions
- selection of governing codes/standards and design basis
- hazard/risk acceptance and residual risk statements
- conflict adjudication where judgment is required
- approval/issuance/signature/seal/transmittal for reliance

**No AI system may claim to certify, approve, sign, seal, or “issue” engineering work for reliance.**

### 3.3 Competence includes tool competence
Using AI you cannot adequately verify is a competence failure.  
“An AI said so” is never a defensible basis of design.

### 3.4 Evidence over plausibility
Engineering does not accept “sounds right.” Engineering accepts:

- inputs and sources
- assumptions (clearly labeled)
- method
- verification evidence
- clear uncertainty and limits

### 3.5 No invention / no silent conflict resolution
- Unknowns must remain **UNKNOWN/TBD** until resolved.
- Conflicts must be **surfaced** (with pointers to the disagreeing sources), not silently “picked.”

### 3.6 Auditability is a design requirement
The project record must be durable and reviewable years later.  
Chat transcripts are not a controlled record.

### 3.7 Least privilege, privacy, and security by default
Access to files is power and risk. Defaults must be conservative:

- smallest write scope that can do the job
- data minimization (send/store only what is necessary)
- separation between draft space and issued space

### 3.8 Assume failure over time
Agentic failure modes are trajectory failures: drift, compounding errors, silent corruption.  
Monitoring, verification, and recovery are part of the architecture, not add‑ons.

---

## 4) The Human–AI contract

### Humans (accountable professionals) do:
- define intent, scope, and acceptance criteria
- choose codes/standards and key assumptions
- decide what “done” means and what is safe to rely on
- approve changes that affect deliverables
- perform (or commission) independent review where required
- accept residual risk

### AI systems may:
- draft and format deliverables under explicit templates
- extract, normalize, cross-reference, and summarize evidence
- generate candidate alternatives and tradeoff tables
- surface gaps, inconsistencies, and interface conflicts
- run bounded, checkable transformations (with validators)

**AI outputs are drafts and decision support. Human acceptance is what makes them engineering work product.**

---

## 5) Architecture requirements for AI in regulated practice

### 5.1 Define cognitive boundaries first
Before any “agent” runs, decide what is:

**Pre‑structured (validator-friendly):**
- schemas, naming, lifecycle states
- registers (assumptions, decisions, requirements, hazards, interfaces)
- deterministic transforms (parse → normalize → check → render)
- permission maps and write zones
- checklists and runbooks

**Left open (agent cognition):**
- interpreting ambiguous text
- proposing candidate decompositions/options
- reconciling tradeoffs (explicitly)
- exception investigation

Rule of thumb: **if you can write a validator for it, you can structure it.**

### 5.2 State must be first‑class and inspectable
Regulated engineering requires a durable record. Treat state as artifacts, not “memory”:

Minimum state artifacts (risk-proportionate):
- **Scope ledger** (what’s in/out)
- **Assumptions register**
- **Decisions log** (who decided, when, why)
- **Requirements / traceability matrix**
- **Hazards / risk register** (as applicable)
- **Verification log** (checks run, results, sign-offs)
- **Change log** (what changed, why, impact)

### 5.3 The filesystem is the system of record
Deliverables and logs live as files under version control. This enables:

- meaningful diffs for review
- reproducibility and rollback
- audits without relying on vendor systems or transient chats

### 5.4 Typed actions and gated writes
Do not give AI “do anything” powers.

- define a limited action vocabulary (read, extract, propose, write-draft, etc.)
- enforce preconditions/postconditions
- validate outputs (schemas, linters, tests, cross-file consistency)
- require explicit approval for risky operations (writes to controlled areas, deletes, scope expansion)

### 5.5 Verification is mechanized where possible; validation stays human
- **Verification:** automate checks (schemas, math, linting, consistency, unit tests, cross-references).
- **Validation:** confirm the right problem is being solved and the solution is fit-for-purpose (human judgment, supported by evidence).

Where practice requires it: enforce **independent review** and **separation of duties**.

### 5.6 Monitoring and recovery are part of “done”
Minimum expectations:
- observable logs (what ran, with what inputs, what changed)
- bounded retries (no infinite loops)
- safe failure mode (“stop + ask human”)
- recovery paths (diffs, backups, rollback)

### 5.7 Instruction governance is release engineering
Agent operating instructions are part of the system. Treat them like software:

- versioned and auditable
- reviewed before release
- no silent behavior changes
- clear release notes for material changes
- test coverage for high-risk workflows

---

## 6) Review gates for reliance (risk‑proportionate)

A simple, repeatable gate model:

- **Gate A — Completeness:** scope stated; required sections present; TBDs listed.
- **Gate B — Traceability:** claims map to sources; assumptions labeled; conflicts surfaced.
- **Gate C — Verification:** appropriate checks/tests/calcs exist and pass.
- **Gate D — Approval:** accountable professional review/sign-off for reliance.

AI can assemble the evidence pack. Humans pass/fail the gate.

---

## 7) Practical “stop rules” (when the correct answer is to halt)

The system must stop and escalate when:
- an output could affect safety/regulatory compliance and evidence is incomplete
- requirements are ambiguous or contradictory without a clear authority
- the task requires judgment outside declared competence boundaries
- tool outputs cannot be validated
- the requested action would expand scope, change commitments, or issue work for reliance

Fail safe. Ask. Record the uncertainty.

---

## 8) Path forward (what to implement next)

1. **Write the jurisdiction addendum**
   - regulator(s), applicable codes/standards
   - sealing/signature rules and record retention
   - confidentiality, privacy, and data handling
   - required review and independence rules

2. **Stand up the minimum artifact set**
   - scope, assumptions, decisions, requirements, hazards (if applicable), verification, change control

3. **Build validators and evidence tooling**
   - schemas, linters/tests, cross-file checks, traceability reports

4. **Define decision rights and gates**
   - who decides what; what requires review; what cannot be automated

5. **Train for competence (including AI/tool competence)**
   - how to review AI outputs
   - how to detect hallucination and omission
   - how to maintain independent judgment

6. **Engage stakeholders early**
   - regulators, clients, insurers, QA leads
   - align expectations around auditability and record

---

## Closing

AI becomes compatible with regulated professional engineering when it is **engineered into a controlled system**:

- structure first
- bounded actions
- evidence and auditability
- monitoring and recovery
- humans retain decision rights and responsibility

If we cannot make it auditable, we cannot rely on it.
