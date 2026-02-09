# PROFESSIONAL_ENGINEERING.md
_Date: 2026-02-09_

This document states the **professional engineering posture** for the Chirality App project: how we design and use agentic workflows in a **regulated, high-stakes, high-risk** engineering context.

It is written to be compatible with this project’s conception of agents and the standards articulated by `AGENT_HELPS_HUMANS.md`, and it uses `WHAT-IS-AN-AGENT.md` as the framing definition of “agent”.

---

## 0) Framing: what an “agent” is (in this repo)

> **agent = LLM + instructions + access to files + use of tools**

In this project, “agentic” is not magic; it is **architecture**: a closed-loop system operating over time, with explicit state and controlled actions.

The repository uses a three-layer view (from `WHAT-IS-AN-AGENT.md`):
- **Agent 0 (Compiler):** defines standards and writes/maintains instructions.
- **Agent 1 (Runtime):** manages flow/state, dispatches bounded work, synthesizes decisions.
- **Agent 2 (Thread):** executes a narrow task, straight-through, producing auditable artifacts.

---

## 1) What “professional engineering” means here

In regulated engineering practice, we treat work as **accountable engineering**:
- decisions must be **defensible**,
- evidence must be **traceable**,
- risks must be **identified and controlled**,
- outputs must be **reviewed** before reliance,
- and the process must be **auditable**.

Agents are **tools** and **assistants**. They are not professionals of record.

### 1.1 Engineer-of-Record (EoR) principle
For any high-stakes output, there is a human **Engineer-of-Record** (or equivalent accountable professional role) who:
- owns the engineering judgement,
- reviews/approves outputs before use,
- and accepts professional responsibility within their jurisdiction and competence.

**No agent may claim to approve, certify, sign, seal, or act as EoR.**

---

## 2) Core commitments (non-negotiable)

### 2.1 Public safety, legal compliance, and ethics are “first constraints”
We treat safety, legal/regulatory compliance, and professional ethics as **primary design constraints**, not optional “non-functional requirements”.

### 2.2 Competence boundary
Agents may assist across domains, but the system must enforce:
- **scope boundaries**,
- **explicit uncertainty** (`TBD/UNKNOWN`),
- and **escalation** when competence/risk boundaries are reached.

### 2.3 Due diligence = evidence + verification + review
Any engineering-relevant claim must be tied to:
- a source (reference, code, standard, calculation),
- a method (procedure/checklist),
- and a verification posture (test/inspection/review).

### 2.4 “No invention” posture for high-stakes work
In high-stakes contexts, “making something up” is not a creativity feature; it is a defect.
- Unknowns stay unknown.
- Assumptions are labeled as assumptions.
- Conflicts are surfaced, not resolved silently.

---

## 3) How the theory maps to architecture choices

The project’s stance aligns with classical agent theory:
- **Agency is a system property**, not a model capability.
- LLMs change the **cognitive substrate** (cost and expressiveness), not the definition of agency.
- The architectural priority is **control and closed-loop stability** over time.

### 3.1 Cognitive boundaries (the main architectural move)
We prefer to design the **cognitive space** before “agents appear”:

**Pre-structured (deterministic / enforceable):**
- schemas, IDs, registers, validators,
- known transforms (extract → normalize → route),
- permission maps and write zones,
- checklists and runbooks.

**Left open (agent cognition):**
- interpreting ambiguous text,
- proposing candidate solutions,
- reconciling tradeoffs with explicit reasoning,
- exception handling and investigation.

Rule of thumb:
- If you can write a validator, you can usually structure it.
- Agents are reserved for uncertainty and combinatorics.

### 3.2 Control model: hybrid by default
- Use **deliberative planning** for milestones and gating decisions.
- Use **bounded, straight-through** execution for task steps.
- Use **monitoring + recovery** to manage drift and failure over time.

### 3.3 State is an artifact, not a chat
We treat state as:
- inspectable files (deliverables, registers, logs),
- with stable IDs and explicit provenance,
not an ungoverned conversational memory.

---

## 4) Governance model: who does what

### 4.1 Human roles
- **Engineer-of-Record / Accountable Professional:** approves high-stakes outputs; sets safety posture.
- **Project/Package Owner:** defines objectives, scope, priorities, and acceptance criteria.
- **Reviewer(s):** independent review where required (risk-based).

### 4.2 Agent roles (repository pattern)
- **Type 0 (standards):** defines/maintains instruction standards and audit criteria.
- **Type 1 (managers):** orchestrate; do not “do everything”; request human decisions; dispatch Type 2 tasks.
- **Type 2 (tasks):** produce bounded outputs; never expand scope; write only to allowed zones.

### 4.3 Change control
File-state changes that impact deliverables are handled via explicit **change requests** and a controlled editor role (e.g., CHANGE).
High-stakes changes require review gates before reliance.

---

## 5) Risk management expectations (high-stakes posture)

When stakes are high, we expect explicit risk work products, proportionate to risk:
- hazard identification (what can go wrong),
- risk estimation (likelihood × consequence, qualitatively or quantitatively),
- controls/mitigations (prevent, detect, limit),
- verification evidence (tests, inspections, analyses),
- residual risk statement and acceptance authority,
- operational monitoring where applicable.

Agents can help draft, organize, and cross-check these artifacts, but **risk acceptance remains human-owned**.

---

## 6) Minimum requirements for agent instructions in regulated engineering work

Any `AGENT_*.md` that operates in or near regulated engineering outputs SHOULD include:

1) **Scope and boundaries** (what is in/out)
2) **Write permissions** (write zones + explicit edit gates)
3) **Brief schema** (what inputs are required)
4) **Deterministic outputs** (where artifacts go; naming; `_LATEST` pointers if used)
5) **Provenance rules** (how claims tie to evidence)
6) **QA contract** (what is checked; how conflicts are surfaced)
7) **Failure/recovery posture** (when to stop; when to escalate; how to report UNKNOWN)

For high-stakes tasks, prefer:
- stepwise execution,
- explicit checkpoints,
- and conservative defaults (read-only unless authorized).

---

## 7) Deliverables-first practice (how we “engineer” in this repo)

The repository is organized so that:
- deliverables are the primary unit of engineering work,
- dependencies are explicit artifacts (not implicit conversations),
- and reconciliation is an evidence-based process.

### 7.1 Deliverable-local helpers (e.g., `AGENT_TASK.md`)
A deliverable-local helper agent is expected to:
- self-initialize from the deliverable folder,
- propose changes with evidence,
- apply edits only when authorized,
- and surface dependency/interface issues without “fixing other deliverables”.

Semantic lensing (if present) is treated as **optional** and **explicitly invoked**, not mandatory.

---

## 8) Review gates (risk-proportionate)

For work that will be relied upon in real decisions, we use gates such as:

- **Gate A — Completeness:** key sections present; TBDs identified; scope stated.
- **Gate B — Traceability:** claims map to sources; assumptions labeled; conflicts surfaced.
- **Gate C — Verification:** checks/tests/calcs exist and are appropriate.
- **Gate D — Approval:** EoR/reviewer sign-off (human).

Agents may prepare gate checklists and evidence packs. Humans pass/fail the gate.

---

## 9) “Engineer’s questions” to force clarity (a practical checklist)

When in doubt, we ask:

1) What is the objective and intended use of this artifact?
2) What are the acceptance criteria? (How do we know it’s correct?)
3) What are the assumptions? Are they acceptable and documented?
4) What are the hazards and failure modes?
5) What is the verification method and evidence?
6) What is out of scope?
7) Who must approve before we rely on it?

If an agent cannot answer these using evidence, the correct output is:
- `UNKNOWN/TBD` + the smallest next check + who should decide.

---

## 10) Jurisdictional addendum (TODO by the organization)

Because professional engineering is jurisdiction-specific, this project SHOULD maintain an addendum that captures:
- the governing regulator(s),
- applicable codes/standards,
- documentation/sign-off requirements,
- record retention and confidentiality policies,
- and any “must-do” ethics rules that apply to the organization.

This file is intentionally principles-first; the addendum makes it enforceable.

---

## Closing stance

This project treats agentic workflows as **engineering systems**:
- explicitly structured where possible,
- carefully bounded where not,
- continuously observed and verified,
- and ultimately accountable to human professional judgement.

If we cannot make it auditable, we cannot rely on it.
