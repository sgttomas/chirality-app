# Professional Engineering (Agentic Workflows)

This document defines the professional practice standard for building and operating Chirality-style agentic systems in real projects.

**Core thesis:** agentic behavior is an architectural property of a *system* (state + control + tools + environment), not a magic property of a model.

---

## Framing (from WHAT-IS-AN-AGENT.md)

```
agent = LLM + instructions + access to files + use of tools
```

Professional engineering starts when you decide what the agent is allowed to touch, how it proves what it did, and who is accountable for the outcomes.

---

## Why This Exists

Chirality can read and write a user-selected working folder on a real filesystem. That is powerful, and it carries professional obligations:

- **Safety:** incorrect output can cause real-world harm when it becomes a drawing, spec, procedure, estimate, schedule input, or contract artifact.
- **Security & privacy:** file access means you are one misstep away from leaking secrets, PII, or regulated data.
- **Reliability over time:** agentic failure modes are trajectory failures (drift, compounding errors, silent corruption), not single bad answers.
- **Auditability:** engineering work must be explainable and reviewable by humans and organizations.

This is not optional polish. It is the minimum bar for using agents in professional settings.

---

## Ethics and Professional Duty (Software + Engineering)

This project treats "professional engineering" as a standard of care, not a credential claim.

Non-negotiables:

- **Public welfare first.** If there is a tradeoff, safety and harm reduction win.
- **Honesty about capability.** No "it will work" claims without verification pathways and known limits.
- **Competence boundaries.** If the system cannot validate a class of outputs, it must say so and/or require human review.
- **Accountability.** Every automated action must be attributable (who triggered it, what it changed, why).
- **Least privilege.** Default to the smallest action surface and smallest write scope that can do the job.
- **Respect for data.** Minimize data sent to model providers; avoid collecting data you do not need.
- **Human-in-the-loop at decision points.** The system accelerates work; it does not replace responsibility.

---

## Architecture-Level Choices That Matter

The critical architectural decision is how you carve the cognitive space:

```
structured_space + bounded_actions + validators + feedback = controllable_agents
```

### 1) Define the cognitive boundary

Decide what is pre-structured vs open-ended.

- **Pre-structured:** schemas, folder layouts, lifecycle states, dependency registers, allowed file types, naming conventions, templates, validators.
- **Open-ended:** interpretation, proposing candidates, resolving ambiguity, prioritizing tradeoffs, exception handling.

Rule of thumb: if you can write a validator for it, you can usually structure it.

### 2) Treat state as a first-class artifact (not chat history)

Agentic systems are closed-loop controllers. They require inspectable state:

- task state (goals, scope, acceptance criteria)
- world state (facts + uncertainty + provenance)
- execution state (what ran, tool outputs, diffs)
- commitments (what the system promised the user)

In Chirality, state lives in **files** (the filesystem is the state). That is a feature: it enables auditability and review.

### 3) Make actions typed and gated

Do not give the model "do anything" powers.

- define a limited tool/action vocabulary
- enforce preconditions (what must be true before an action)
- enforce postconditions (what must be true after an action)
- validate outputs (schema checks, lint/tests, cross-file coherence checks)
- require explicit approval for risky operations (writes, deletes, cross-root access)

### 4) Separate deterministic transforms from agent cognition

Use agents for uncertainty and combinatorics; use deterministic code for stable transforms.

- deterministic: parsing, normalization, ID assignment, diffing, rendering, schema validation
- agentic: interpretation, candidate generation, planning under tradeoffs, prioritization, reconciliation of ambiguity

This reduces both cost and risk.

### 5) Choose an explicit control model

High-level patterns:

- **Planner-led:** plan -> execute -> monitor -> replan
- **Policy-led:** continuous reactive decisions with monitoring
- **Hybrid:** planner for milestones, reactive controllers for local steps

In dynamic environments, hybrid + strong monitoring is usually the safest.

### 6) Coordination comes from structure, not hand-wired flows

Instead of "Agent A then Agent B", design the shared space:

- clear roles (Type 0/1/2)
- clear write scopes (project-level vs tool-root vs deliverable-local)
- explicit contracts (inputs, outputs, validators, evidence)
- shared representations (stable IDs, lifecycle states, dependency graphs)

Interactions then emerge from the space and constraints.

### 7) Monitoring, verification, and recovery are part of the design

Agentic systems must assume failure:

- observability (logs, traces, diffs)
- internal checks (policy compliance, consistency)
- external checks (schema validators, tests, human review)
- recovery (retry, alternate tool, rollback, ask user)

The goal is stable trajectories, not perfect steps.

### 8) Memory governance: what persists vs what must not

Treat memory like a governed database:

- durable: task state, evidence, decisions, provenance, artifacts
- ephemeral: scratch reasoning, intermediate candidates
- forbidden: secrets and sensitive data unless explicitly required and secured

If you cannot defend storing it, do not store it.

---

## The 0/1/2 Layer Model as Responsibility Boundaries

The layer model is not just an org chart; it is how professional responsibility is enforced.

| Layer | Name | Professional responsibility |
|-------|------|----------------------------|
| Agent 0 | The Architect | Defines boundaries, safety policy, and contracts; maintains instruction integrity |
| Agent 1 | The Manager | Orchestrates work within contracts; enforces gates; produces reviewable briefs and evidence |
| Agent 2 | The Specialist | Executes bounded tasks; returns checkable outputs + proofs; never "goes rogue" |

If something goes wrong:

- bad output -> fix Agent 2 tooling/validators
- wrong task attempted -> fix Agent 1 orchestration/contracts
- misunderstood goal -> fix Agent 0 alignment and boundary definition

---

## Operational Requirements (Minimum Bar)

### For product and release engineering

- **Reproducible builds where feasible.** Pin versions, lock dependencies, document build steps.
- **Supply-chain hygiene.** Track dependencies, review high-risk packages, patch known critical issues.
- **Code signing and platform trust.** Ship signed/notarized artifacts for real end users; unsigned binaries are for dev/testing.
- **Update transparency.** Users should be able to determine version, see release notes, and obtain updates from a trustworthy source.
- **No silent behavior changes.** When the instruction root changes, treat it like a software update (versioned, released, auditable).

### For runtime behavior on a user's filesystem

- **Explicit working root selection.** Never assume a project root; never default to "whole disk".
- **Visible write intent.** For any write, show what will change (diff/preview) when practical.
- **Scoped access.** Default to operating inside the working root; crossing root boundaries requires explicit user intent.
- **Fail safe.** If the system is unsure, it asks; it does not guess and write.
- **Evidence-first outputs.** Prefer outputs that are auditable: diffs, tables with IDs, references, and run logs.

---

## Red Lines

The system must not:

- write or delete outside the working root without explicit user intent
- exfiltrate file contents or metadata beyond what is necessary to fulfill the user request
- claim compliance, certification, or professional sign-off it cannot actually provide
- hide uncertainty: if validation is missing, say so and require review
- create irreversible changes without a clear recovery path (diffs, backups, or rollback strategy)

---

## Practical Review Standard (When Work Is "Done")

A deliverable is not "done" when text exists. It is "done" when it is reviewable:

- acceptance criteria are explicit
- outputs are checkable (schema/tests/validators where possible)
- provenance exists (sources and rationale)
- changes are diffable and attributable
- unresolved uncertainties are listed (not buried)

That is what makes agent acceleration compatible with professional engineering practice.

