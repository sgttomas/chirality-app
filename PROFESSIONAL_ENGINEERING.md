# Professional Engineering with Agentic AI in Regulated Practice

Chirality AI Ltd.
Date: 2026-03-29, Revision 1, Issued for Use

**Standard for the Governance of AI Agent Systems in Professional Engineering Practice**

Referenced by the Chirality AI Ltd. Professional Practice Management Plan (PPMP).

---

## Preamble

This document defines the professional practice standard for Chirality AI Ltd. governing the use of AI agent systems in regulated engineering practice. It establishes how the firm satisfies its professional obligations under the *Engineering and Geoscience Professions Act* (EGP Act), the *General Regulation*, and applicable APEGA practice standards when licensed professionals rely on work produced by AI agents. The theoretical foundation for this standard — including the nature of knowledge in professional practice and the structural relationship between AI output and professional accountability — is defined in `CHIRALITY_FRAMEWORK.md`.

> AI can accelerate engineering work. It cannot inherit professional responsibility.

Professional engineering is a duty-of-care practice: commitments to reality under uncertainty, made by accountable professionals, supported by evidence that can withstand review. AI changes the cost of drafting, searching, reconciling, and summarizing. It does not change what regulators, clients, insurers, courts, and the public require: competence, independent judgment, verification, assumption of responsibility, and a durable project record.

---

## 1. Regulatory Basis

### 1.1 Governing Legislation and Standards

This standard is grounded in:

- The *Engineering and Geoscience Professions Act* (EGP Act), Sections 1(q), 1(r), 2(1), 3(2), 3(3), 5(1), 6(2), 6(3)
- The *General Regulation*, Part 7 (Professional Practice Management Plans), Part 8 (Practice Standards), Sections 49 and 54 (Authentication)
- APEGA Practice Standard: *Relying on the Work of Others and Outsourcing* (May 2021, v4.0)
- APEGA Practice Standard: *Authenticating Professional Work Products*
- APEGA Guideline: *Professional Practice Management Plans*

### 1.2 Applicability

This standard applies whenever Chirality AI Ltd. licensed professionals use AI agent systems — including the Chirality agent operating system and any LLM-based agents operating under the firm's agent instruction architecture — to produce, assist in producing, or contribute to professional work products (PWPs) intended for use in Alberta or under APEGA jurisdiction.

### 1.3 Regulatory Framework for AI-Assisted Work

AI agents that produce work under the direction of a licensed professional are "others" whose work the professional relies on, within the meaning of APEGA §3.0 (*Relying on the Work of Others*). The professional's obligations are defined by what the licensed professional must do — not by the nature of the entity producing the work. Whether the worker is a junior engineer, an engineering intern, a contractor, or an AI agent, the professional's obligations are the same.

The firm interprets this framework as applying directly in substance because AI agents assume no professional responsibility. On that interpretation, the entire chain of responsibility flows to the licensed professional who authenticates the resulting professional work product. This is closely analogous to the case of an unlicensed individual working under direct supervision and control: the supervising professional bears full responsibility for the work.

On that interpretation, the APEGA practice standard does not require an AI-specific amendment to govern this use. Its obligations are defined in terms of what the professional must do — supervise, review, authenticate — not in terms of what the worker must be. The governance architecture described in this document is the firm's mechanism for making those existing obligations satisfiable when the work is produced by AI agents whose outputs present a novel epistemic challenge: plausible by construction, with no intrinsic signal distinguishing grounded claims from fabricated ones.

The firm's obligations therefore engage two mechanisms from the APEGA practice standard *Relying on the Work of Others and Outsourcing*:

**Direct supervision and control (§3.1.1).** When a licensed professional directs AI agents through a governed instruction architecture — defining scope, constraints, write boundaries, and review gates — the professional is providing direct supervision and control over the work. The agent instruction architecture is the documented framework for that supervision.

**Thorough review (§3.1.2).** When a licensed professional reviews AI agent outputs before authentication, the professional is conducting thorough review. APEGA §3.1.2.1 explicitly requires review of "the relevancy and accuracy of applicable tools used in the PWPs preparation (including software, hardware, firmware, applications, and other technologies)." AI model-based agent systems are such technologies.

---

## 2. Definitions

Terms defined in the APEGA practice standard *Relying on the Work of Others and Outsourcing* (§1.3) apply throughout this document. The following definitions map APEGA statutory terms to the firm's AI agent system.

| APEGA Term | Definition | Chirality System Equivalent |
|---|---|---|
| **Licensed Professional** | An individual entitled by the EGP Act to practise engineering in Alberta | The P.Eng. operating the agent system and authenticating PWPs |
| **Permit Holder** | A partnership, association, or corporation holding a Permit to Practice under the EGP Act | Chirality AI Ltd. (APEGA P17007) |
| **Responsible Member** | An APEGA licensed professional responsible for oversight of the practice of engineering by the permit holder | The firm's Responsible Member as registered with APEGA |
| **Professional Work Product (PWP)** | An output of professional services with technical information relied upon by others to make a decision or take action | Authenticated deliverables issued for reliance (lifecycle state: ISSUED) |
| **Authentication** | A licensed professional has completed, performed a thorough review of, or directly supervised and controlled the work and accepts professional responsibility | Human approval, seal, and signature at issuance gate |
| **Validation** | A Responsible Member has reviewed the PWP to ensure it meets QC/QA measures in the PPMP | Responsible Member review per the firm's PPMP |
| **Direct Supervision and Control** | Directing, monitoring, and controlling engineering work, including making all decisions related to the practice | Gate-controlled agent orchestration under the Type 0/1/2 hierarchy with human authority at every gate |
| **Thorough Review** | An evaluation of the outputs of professional services prepared by others to verify their reliability, validity, and technical accuracy | REVIEW agent 5-gate protocol + human authentication decision |
| **Due Diligence** | The level of judgement, care, forethought, and determination a person reasonably uses to avoid harming oneself, other people, property, or the environment | The licensed professional's exercise of judgment at every gate, supported by the system's evidence trail |
| **AI Agent** | A controlled system architecture (model + instructions + tools + file access + governance) that performs bounded work under the direction of a licensed professional | An AGENT_*.md instruction file instantiated at runtime within the Chirality agent operating system |
| **Agent Instruction Architecture** | The firm's documented framework of agent instruction files, governance documents, invariant contracts, and deterministic tools that constitutes the direct supervision and control structure for AI agents | The `agents/`, `docs/`, and `tools/` directories as governed by the firm's release engineering process |

---

## 3. Professional Obligations

These obligations are binding constraints on any workflow that produces work product for regulated engineering practice. They derive from the EGP Act, the General Regulation, and APEGA practice standards.

### 3.1 Public Welfare Is the First Constraint

The protection of the public, property, and the environment is the overriding obligation. When tradeoffs exist between public safety and commercial pressure, schedule, or convenience, safety prevails. This obligation is non-delegable to AI systems.

### 3.2 Responsible Charge Remains Human

Professional liability is personal and non-transferable. A licensed professional retains decision rights for:

- Scope and boundary decisions
- Selection of governing codes, standards, and design basis
- Hazard and risk acceptance, including residual risk statements
- Conflict adjudication where engineering judgment is required
- Approval, issuance, signature, seal, and transmittal for reliance

No AI system may claim to certify, approve, sign, seal, or issue engineering work for reliance. AI agent outputs are drafts and structured assistance. Human acceptance is what makes them engineering work product.

This is enforced by invariant K-AUTH-1: "Only humans author binding approval records. No agent may claim to certify, approve, sign, seal, or issue work for reliance." See `docs/CONTRACT.md`.

### 3.3 Competence Includes Tool Competence

A licensed professional must not use an AI agent to perform work they are not competent to verify manually. Using AI to produce work you cannot adequately review is a competence failure under the EGP Act. "An AI said so" is never a defensible basis of design.

APEGA §3.1.2.1 requires thorough review of "the relevancy and accuracy of applicable tools used in the PWPs preparation." For AI agent systems, this means the licensed professional must understand:

- What the agent is instructed to do (its protocol, write scope, and constraints)
- What the agent's outputs represent (drafts requiring verification, not authoritative conclusions)
- How to verify the agent's outputs against source materials and engineering judgment
- The failure modes of LLM-based systems (hallucination, omission, plausible-sounding error)

### 3.4 Evidence Over Plausibility

Engineering does not accept "sounds right." The firm's practice requires:

- Inputs and sources (provenance is mandatory)
- Assumptions explicitly labeled, not hidden in prose
- Methodology documented and reproducible
- Verification evidence traceable to specific checks
- Uncertainty and limitations stated

This is enforced by invariants K-PROV-1 (mandatory provenance), K-INVENT-1 (no invention — unknown values become TBD), and K-CONFLICT-1 (conflicts surfaced, not silently resolved). See `docs/CONTRACT.md`.

### 3.5 Hierarchy of Authority

In technical matters, the firm's licensed professionals and all AI agents follow:

1. Laws and regulations
2. Codes and standards
3. Project specifications / design basis (approved for use)
4. Verified engineering analysis + published literature
5. Professional judgment

AI agent outputs carry no professional authority. They are decision support unless explicitly accepted and issued by an accountable professional. See `docs/DIRECTIVE.md` §3.4 (Hierarchy of Authority).

---

## 4. Direct Supervision and Control of AI Agents

This section establishes how the firm satisfies APEGA §3.1.1 (*Direct Supervision and Control*) requirements when licensed professionals direct AI agents to produce work that will be incorporated into PWPs.

### 4.1 Active Involvement (APEGA §3.1.1.1)

APEGA requires that the licensed professional demonstrate active involvement through ongoing interaction and input. The firm satisfies this through:

**Directing, monitoring, and controlling work throughout its lifespan.**

- Type 1 (Manager) agents operate through gate-controlled workflows where the licensed professional makes consequential decisions at every phase.
- Type 2 (Specialist) agents execute only within bounded briefs defined by the licensed professional or an authorized Type 1 agent.
- Human authority is the halting condition — no agent may autonomously advance workflow stages, approve deliverables, or resolve conflicts. Enforced by K-GATE-1 (dynamic gates with minimum seal + pipeline approval) and K-SEAL-1 (no Type 2 execution before context is sealed and gate-approved). See `docs/CONTRACT.md` §1.7, §1.3.
- Implementation: `docs/DBM_Agent_Instruction_Architecture.md` §6 (Orchestration Architecture).

**Establishing and documenting scope, duties, responsibilities, authorities, and limitations.**

- Every agent instruction file (AGENT_*.md) declares: agent type, class, interaction surface, write scope, blocking behavior, primary outputs, and non-negotiable invariants.
- Write scope is enforced by invariant K-WRITE-1: "Every agent has an explicit write scope declared in its header block. No agent writes outside its declared zone."
- The three-type hierarchy (Type 0 Architect / Type 1 Manager / Type 2 Specialist) establishes clear authority boundaries. Authority flows downward; escalation flows upward. A Type 2 agent cannot modify rules set by Type 0. A Type 1 agent cannot approve deliverables for external reliance.
- Implementation: `docs/TYPES.md` §4 (Agent Roles), §4.3 (Authority Model); `docs/DBM_Agent_Instruction_Architecture.md` §2 (Type Hierarchy), §7 (Write Scope Architecture); `docs/CONTRACT.md` §1.10 (K-WRITE-1).

**Maintaining regular and ongoing communication.**

- Type 1 agents maintain interactive sessions with the licensed professional, presenting structured outputs and awaiting human decisions at gates.
- Type 2 agents receive structured briefs (INIT-TASK) and return structured run reports with PASS/FAIL status and evidence. Brief format defined in `docs/DBM_Agent_Instruction_Architecture.md` §9 (Brief & Output Contracts).
- Session handoff artifacts (NEXT_INSTANCE_STATE.md, NEXT_INSTANCE_PROMPT.md) maintain continuity across sessions without hidden state. Working memory per deliverable is defined in `docs/SPEC.md` §8 (`_MEMORY.md`).
- Implementation: `docs/DBM_Agent_Instruction_Architecture.md` §6.2 (Control Loop).

**Identifying and rectifying gaps in competencies.**

- Agent audit system (AUDIT_AGENTS) verifies conformance of agent instructions against the canonical standard (`agents/AGENT_HELPS_HUMANS.md`). Structural requirements for instruction files defined in `docs/SPEC.md` §9.
- Three layers of contracts govern agent behavior: R1–R9 workflow design requirements (defined in `agents/AGENT_HELPS_HUMANS.md`), I1–I10 decomposition invariants (defined in `agents/AGENT_DECOMP_BASE.md`), and 21 K-* system-wide invariants (defined in `docs/CONTRACT.md`).
- Evaluation framework provides systematic assessment of agent output quality.
- Agent instruction governance follows release engineering discipline: versioned, reviewed, no silent behavior changes (see §6.2 of this standard).
- Implementation: `docs/DBM_Agent_Instruction_Architecture.md` §4 (Contract Framework).

**Completing periodic reviews to ensure PWPs are accurate and reliable.**

- REVIEW agent implements a formal 5-gate review process for lifecycle transitions (see §5 of this standard).
- RECONCILIATION agent performs cross-deliverable coherence analysis.
- All agent outputs are git-committed, enabling diff-based review at any point.
- Implementation: `docs/CONTRACT.md` (invariant system); `agents/AGENT_REVIEW.md` (review protocol).

### 4.2 Responsibility in Decision Making (APEGA §3.1.1.2)

APEGA requires that the licensed professional be responsible for all technical engineering decisions. The firm satisfies this through:

- Licensed professionals consider and document relevant issues through structured deliverable context files: identity and traceability (`_CONTEXT.md`, defined in `docs/SPEC.md` §4), dependency summary (`_DEPENDENCIES.md`, defined in `docs/SPEC.md` §5), and source document pointers (`_REFERENCES.md`, defined in `docs/SPEC.md` §7).
- Technical direction is provided through agent briefs, gate decisions, and conflict adjudication at human gates.
- Licensed professionals are available to review and approve decisions through interactive Type 1 agent sessions and gate-controlled workflows.
- All decisions are recorded in versioned files (Decision Logs, `_MEMORY.md` per `docs/SPEC.md` §8, `_STATUS.md` history per `docs/SPEC.md` §3). If a decision is not in a versioned file, it does not exist for purposes of reliance (`docs/DIRECTIVE.md` §2.2).

### 4.3 Documentation of Due Diligence

APEGA §3.1.1 requires that the process for direct supervision and control and record keeping be described in the PPMP. The firm's documentation includes:

- Agent instruction files (`agents/AGENT_*.md`) — documented scope, duties, authorities, and constraints for each agent
- Governance documents (`docs/`) — design philosophy, physical specifications, domain vocabulary, invariant contracts, and design basis
- Git history — the complete development record of all project state, including agent outputs, human decisions, and lifecycle transitions
- Immutable snapshots — timestamped, append-only audit trail for all analysis outputs. Enforced by K-SNAP-1 (`docs/CONTRACT.md` §1.10); snapshot format defined in `docs/SPEC.md` §11.

---

## 5. Thorough Review and Authentication

This section establishes how the firm satisfies APEGA §3.1.2 (*Thorough Review*) requirements when licensed professionals review AI agent outputs before authentication.

### 5.1 Applicability

Thorough review applies to all AI agent outputs that will be incorporated into PWPs. Even when the licensed professional has provided direct supervision and control throughout the work, thorough review is conducted before authentication.

### 5.2 Reliability, Accuracy, and Validity (APEGA §3.1.2.1)

The licensed professional confirms reliability, accuracy, and validity by reviewing:

- Scope of the work, including work done by any agent
- Relevant design and operational conditions, including risk assessments and mitigation strategies
- Assumptions, limitations, and expressed caveats — aided by the system's epistemic labeling (FACT, ASSUMPTION, PROPOSAL, TBD) as defined in `docs/TYPES.md` §10
- Suitability of the work for its intended purpose and compliance with local conditions
- Health, safety, and environmental implications
- Integrity and validity of all work products, including cross-deliverable consistency
- Applicable tasks related to the work (calculations, analyses, evaluations, interpretations)
- Applicable materials and methods of construction, inspection, maintenance, or operation
- Relevancy and accuracy of the AI agent tools used in the work's preparation
- Interdisciplinary reviews where the work crosses discipline boundaries

The firm's REVIEW agent (`AGENT_REVIEW.md`) implements a structured 5-gate review process:

| Gate | Function | Authority |
|------|----------|-----------|
| Gate 1 | Precondition check (lifecycle state, context validity) | Agent validates; human confirms scope |
| Gate 2 | Checklist generation from specifications, decomposition, and dependencies | Agent derives; human confirms completeness |
| Gate 3 | Findings capture (iterative) | Human provides findings; agent records with evidence |
| Gate 4 | Disposition review | Human rules on all findings |
| Gate 5 | Lifecycle transition decision | Agent recommends; human approves |

Transition readiness criteria are severity-based (lifecycle state machine defined in `docs/SPEC.md` §3, `docs/TYPES.md` §5):

- **IN_PROGRESS to CHECKING:** All CRITICAL findings must have non-TBD human disposition.
- **CHECKING to ISSUED:** All CRITICAL findings RESOLVED; all MAJOR findings RESOLVED or DEFERRED with documented rationale.

### 5.3 Adherence to Regulatory Requirements (APEGA §3.1.2.2)

Thorough review must verify compliance with:

- The EGP Act and the General Regulation
- APEGA practice standards, bulletins, and guidelines
- Contractual requirements to meet project-specific regulatory approvals or permit requirements

The firm's hierarchy of authority (§3.5) is enforced through agent instruction invariants. Agents cannot override codes, standards, or project specifications.

### 5.4 Adherence to Quality Control and Assurance (APEGA §3.1.2.3)

Thorough review must verify:

- That PWPs are produced following the quality control and assurance processes defined in this standard and the firm's PPMP
- That deliverables are clear, readable, consistent, and complete

The firm's quality controls are described in §7 of this standard.

### 5.5 Authentication

Authentication of PWPs follows the APEGA practice standard *Authenticating Professional Work Products*. A licensed professional may authenticate a PWP only when they have:

- Provided direct supervision and control over the AI-assisted work per §4 of this standard, OR
- Conducted a thorough review per §5.1–5.4 of this standard

AND in either case:

- The licensed professional is competent to verify the work per §3.3 of this standard
- The PWP has been validated by a Responsible Member per the firm's PPMP

Authentication binds to a specific git SHA. Content change after authentication voids the authentication (K-AUTH-2, `docs/CONTRACT.md` §1.2). A deliverable is considered dirty if any governed input has changed since its last approved SHA (K-VAL-1, `docs/CONTRACT.md` §1.6). Merge to main is allowed only when branch HEAD equals the approved SHA (K-MERGE-1, `docs/CONTRACT.md` §1.8). The licensed professional's signature and seal apply to the specific version of the work identified by that SHA.

---

## 6. Quality Control and Assurance

### 6.1 Architectural Controls

The firm's quality control and assurance for AI-assisted work is implemented through the agent instruction architecture. The following governance documents define the controls:

| Document | QC/QA Function |
|----------|----------------|
| `docs/DIRECTIVE.md` | Founding constraints: filesystem-as-state, human authority, evidence-first, no hidden memory |
| `docs/CONTRACT.md` | 21 binding invariants (K-*) with enforcement map |
| `docs/SPEC.md` | Physical structures, file formats, schema validation checklists |
| `docs/TYPES.md` | Controlled vocabulary, enumerated types, lifecycle state machine |
| `agents/AGENT_HELPS_HUMANS.md` | Workflow design requirements (R1–R9) binding on all agents |
| `agents/AGENT_DECOMP_BASE.md` | Decomposition invariants (I1–I10) binding on all decomposition agents |

### 6.2 Instruction Governance as Release Engineering

Agent instruction files are part of the firm's controlled quality system. They are treated as controlled documents:

- Versioned in git and auditable
- Reviewed before release
- No silent behavior changes permitted
- Material changes to write scope, tool access, or outputs require review and a recorded release note
- Conformance verified by AUDIT_AGENTS against the canonical standard (`agents/AGENT_HELPS_HUMANS.md`); structural requirements per `docs/SPEC.md` §9 (Agent Instruction File Structure)

### 6.3 Deterministic and Probabilistic Boundary

The firm enforces a clear boundary between deterministic operations (handled by validated tools) and probabilistic operations (handled by LLM-based agents):

- If a task can be validated by a schema or algorithm, it is implemented as a deterministic tool — not left to LLM reasoning
- LLM-based agents are reserved for work that genuinely requires inference under uncertainty: interpreting ambiguous text, proposing decompositions, reconciling tradeoffs, drafting content
- The tool registry (`tools/REGISTRY.md`) indexes all deterministic tools

### 6.4 Technology Provider Due Diligence

The firm uses large language models (LLMs) provided by technology vendors (currently Anthropic) as the cognitive engine within the agent system. The LLM is a technology component — the provider is not providing professional services and does not assume professional responsibility. The firm's licensed professionals bear full responsibility for all work produced using the technology.

The firm exercises due diligence on the LLM technology consistent with APEGA §3.1.2.1 requirements to verify the relevancy and accuracy of tools used in PWP preparation:

- Evaluation of model capabilities and limitations for the professional services the firm provides
- Assessment of model safety practices, alignment research, and responsible deployment policies
- Testing of agent behavior within the firm's instruction architecture before adopting model updates
- Documented assessment of material model changes and their impact on agent behavior
- The agent instruction architecture constrains and governs LLM behavior independent of the provider's controls: R1–R9 workflow requirements (`agents/AGENT_HELPS_HUMANS.md`), 21 K-* system invariants (`docs/CONTRACT.md`), write scope quarantine (`docs/DBM_Agent_Instruction_Architecture.md` §7), and deterministic tool validation (`tools/REGISTRY.md`). The firm does not rely solely on the model provider's safety measures

### 6.5 Evidence and Auditability

The firm's evidence trail is maintained through:

- **Filesystem as state.** All project truth lives in git-tracked plain files. There is no external database or hidden state. If a decision is not in a versioned file, it does not exist for purposes of reliance. See `docs/DIRECTIVE.md` §2.1 (Filesystem Is the Database), §2.5 (No Hidden Memory).
- **Git as development record.** Version control provides meaningful diffs for review, reproducibility, rollback, and audits that do not depend on vendor systems or transient context. See `docs/DIRECTIVE.md` §2.2 (Git Is the Event Store).
- **Immutable snapshots.** Task agent analysis outputs are written to timestamped folders that are never modified after creation. The snapshot trail is the audit trail. Enforced by K-SNAP-1 (`docs/CONTRACT.md` §1.10); format defined in `docs/SPEC.md` §11 (Snapshot and Pointer Conventions).
- **Provenance tracking.** Every extraction, dependency, and parameter value cites its source file and section reference, or carries an explicit `location TBD` marker. Enforced by K-PROV-1 (`docs/CONTRACT.md` §1.9); dependency provenance schema defined in `docs/SPEC.md` §6.5.
- **Epistemic labeling.** All claims are labeled: FACT (observed in source), ASSUMPTION (inferred), PROPOSAL (agent suggestion), or TBD (unknown). The licensed professional does not need to guess whether a value is grounded or inferred. Labels defined in `docs/TYPES.md` §10 (Epistemic Labels).

---

## 7. Record Keeping

### 7.1 Project Records

The firm maintains the following records for AI-assisted work, as required for PPMP compliance:

| Record | Location | Governing Specification | Content |
|--------|----------|------------------------|---------|
| Deliverable lifecycle history | `_STATUS.md` per deliverable | `docs/SPEC.md` §3 | State transitions, dates, actors |
| Design decisions | `_MEMORY.md`, Decision Logs | `docs/SPEC.md` §8 | What was decided, when, why, alternatives considered |
| Dependency register | `Dependencies.csv` per deliverable | `docs/SPEC.md` §6 (v3.1 schema) | Structured dependency tracking with provenance |
| Scope traceability | `_CONTEXT.md` per deliverable | `docs/SPEC.md` §4 | Scope items, objectives, decomposition reference |
| Source references | `_REFERENCES.md` per deliverable | `docs/SPEC.md` §7 | Source document pointers with relevance statements |
| Analysis snapshots | Tool root snapshot folders | `docs/SPEC.md` §11 | Timestamped, immutable records of every analysis run |
| Agent run reports | Snapshot Brief.md, RUN_SUMMARY.md, QA_Report.md | `docs/DBM_Agent_Instruction_Architecture.md` §9.4 | Inputs, outputs, quality checks, warnings |
| Review records | REVIEW gate artifacts | `agents/AGENT_REVIEW.md` | Checklists, finding registers, disposition records, transition decisions |
| Change records | `_Change/` tool root | `agents/AGENT_CHANGE.md` | Change assessments, impact analysis, approval records |
| Version history | Git repository | `docs/DIRECTIVE.md` §2.2 | Complete diff-based record of all project state changes |

### 7.2 Retention

Project records are retained per the firm's PPMP and applicable regulatory requirements. Git history provides indefinite retention of all versioned project state.

---

## 8. Competence and Training

### 8.1 Licensed Professional Competence

Licensed professionals using AI agent systems must be competent to:

- Perform or verify the engineering work manually, without AI assistance
- Review AI agent outputs for technical accuracy, completeness, and fitness for purpose
- Detect LLM failure modes: hallucination, omission, plausible-sounding error, silent conflict resolution
- Understand the agent instruction architecture sufficiently to know what an agent is constrained to do and what it is not
- Exercise independent engineering judgment when AI outputs conflict with professional experience

### 8.2 Training

The firm provides training to licensed professionals on:

- The agent instruction architecture and governance framework
- How to operate within the gate-controlled workflow model
- How to review AI agent outputs and what failure modes to watch for
- How to maintain independent judgment when AI-produced work appears plausible
- Professional obligations under this standard and the firm's PPMP

### 8.3 Maintaining Competence

Licensed professionals must maintain currency with:

- Changes to the agent instruction architecture (release notes, material behavior changes)
- Developments in AI model capabilities and limitations
- Evolving APEGA practice standards and guidance related to AI use in professional practice

---

## 9. The Human-AI Contract

### 9.1 Human Responsibilities

Licensed professionals are responsible for:

- Defining intent, scope, and acceptance criteria
- Choosing codes, standards, and key assumptions
- Deciding what "done" means and what is safe to rely on
- Approving changes that affect deliverables
- Performing or commissioning independent review where required
- Accepting residual risk
- Authenticating PWPs for reliance

### 9.2 AI Agent Permitted Actions

AI agents may, within the constraints of their instruction files:

- Draft and format deliverables under explicit templates
- Extract, normalize, cross-reference, and summarize evidence
- Generate candidate alternatives and tradeoff tables
- Surface gaps, inconsistencies, and interface conflicts
- Run bounded, checkable transformations with deterministic validators
- Maintain structured records (dependency registers, status files, working memory)

### 9.3 AI Agent Prohibitions

AI agents must not:

- Claim to certify, approve, sign, seal, or issue work for reliance — K-AUTH-1 (`docs/CONTRACT.md` §1.2)
- Silently resolve conflicts between sources — K-CONFLICT-1 (`docs/CONTRACT.md` §1.9)
- Invent scope items, parameters, or engineering content; unknowns become TBD — K-INVENT-1 (`docs/CONTRACT.md` §1.9)
- Write outside their declared write scope — K-WRITE-1 (`docs/CONTRACT.md` §1.10)
- Maintain hidden state that diverges from the filesystem — `docs/DIRECTIVE.md` §2.5 (No Hidden Memory)
- Bypass human gates or autonomously advance workflow stages — K-GATE-1 (`docs/CONTRACT.md` §1.7), K-SEAL-1 (`docs/CONTRACT.md` §1.3)

---

## 10. Closing Principle

Engineer a harness that allows judgment to scale.

AI becomes compatible with regulated professional engineering when it is engineered into a controlled system: bounded actions, evidence and auditability, monitoring and recovery, and humans retaining decision rights and professional responsibility.

If we cannot make it auditable, we cannot rely on it.

Use AI to widen and organize the field of consideration; use professional judgment to narrow, accept, and issue. That preserves what professional work outputs mean: a competent person warrants this under duty of care, backed by an auditable record.

---

## 11. Responsible Member

I take responsibility for adopting this standard internally and ensuring it is used appropriately at Chirality AI Ltd., as part of the Professional Practice Management Plan (PPMP).

Ryan Tufts, P.Eng.
APEGA 78780
Chirality AI Ltd. (APEGA P17007)

---

## Document History

| Date | Revision | Description |
|------|----------|-------------|
| 2026-02-09 | 0 | Initial issue |
| 2026-03-29 | 1 | Revised to ground in APEGA regulatory framework; maps direct supervision and control (§3.1.1) and thorough review (§3.1.2) to the agent instruction architecture; restructured for PPMP reference |
