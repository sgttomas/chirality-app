# Appendix C — APEGA Regulatory Mapping

This appendix provides a detailed mapping between the requirements of the APEGA practice standard *Relying on the Work of Others and Outsourcing* (May 2021, v4.0) and the Chirality agent instruction architecture. For each requirement, the table identifies the specific Chirality mechanism — agent, invariant, file, or governed process — that satisfies it, together with the governing document and section or invariant identifier. The intent is to enable a regulator, auditor, or reviewing professional to trace compliance from the regulatory text to the architectural implementation.

The regulatory framework applied here is established in `PROFESSIONAL_ENGINEERING.md` §1.3: AI agents that produce work under the direction of a licensed professional are "others" within the meaning of APEGA §3.0, and the firm's obligations engage two mechanisms — direct supervision and control (APEGA §3.1.1) and thorough review (APEGA §3.1.2). Authentication obligations engage APEGA §3.1 and the companion standard *Authenticating Professional Work Products*.

---

## C.1 Direct Supervision and Control (APEGA §3.1.1)

APEGA §3.1.1 requires that a licensed professional who relies on work performed by others must provide direct supervision and control over that work — defined as directing, monitoring, and controlling engineering work throughout its lifespan, including making all decisions related to the practice of engineering. The Chirality architecture satisfies this obligation through its gate-controlled orchestration model, its three-type agent hierarchy, and its invariant contract system.

### C.1.1 Active Involvement (APEGA §3.1.1.1)

APEGA §3.1.1.1 identifies five specific obligations constituting active involvement. The following table maps each obligation to the Chirality mechanisms that give it architectural force.

| APEGA Requirement | Chirality Mechanism | Governing Document |
|---|---|---|
| Directing, monitoring, and controlling work throughout its lifespan | HELP_HUMAN may supervise several Agent 1 managers; each manager governs a bounded scope and delegates sealed Agent 2 work. Parent-mediated notices, versioned amendments, validated fan-in, and human consequential gates keep delegated work visible and controlled. | `docs/CONTRACT.md` §1.7 (K-GATE-1); `docs/CONTRACT.md` §1.3 (K-SEAL-1); `docs/DBM_Agent_Instruction_Architecture.md` §6; `PROFESSIONAL_ENGINEERING.md` §4.1 |
| Establishing and documenting scope, duties, responsibilities, authorities, and limitations | Every agent instruction file (`agents/AGENT_*.md`) declares the agent's type, class, interaction surface, write scope, blocking behavior, primary outputs, and non-negotiable invariants. Write scope is enforced architecturally: no agent writes outside its declared zone. The runtime hierarchy establishes clear delegation boundaries; human authority does not flow to agents. | `docs/CONTRACT.md` §1.10 (K-WRITE-1); `docs/TYPES.md` §4; `docs/DBM_Agent_Instruction_Architecture.md` §§2, 6; `PROFESSIONAL_ENGINEERING.md` §4.1 |
| Maintaining regular and ongoing communication | Agent 0/1 sessions present decisions to the professional; Agent 2 receives sealed briefs and returns evidence. Versioned plans, notices, amendments, acknowledgments, returns, and handoffs maintain continuity without hidden state. | `docs/DBM_Agent_Instruction_Architecture.md` §§6, 8–9; `docs/SPEC.md` §8; `PROFESSIONAL_ENGINEERING.md` §4.1 |
| Identifying and rectifying gaps in competencies | AUDIT_AGENTS evaluates instruction conformance against the ratified workflow-component standard and K-* invariants. The evaluation framework provides systematic assessment while consequential remediation remains human-governed. | `docs/WORKFLOW_COMPONENT_STANDARD.md`; `docs/DECOMPOSITION_STANDARD.md`; `docs/CONTRACT.md`; `docs/DBM_Agent_Instruction_Architecture.md` §§3–5; `PROFESSIONAL_ENGINEERING.md` §4.1, §6.2 |
| Completing periodic reviews to ensure PWPs are accurate and reliable | REVIEW implements lifecycle review. EVALUATION performs generic cross-deliverable coherence assessment; activated RECONCILIATION aligns deliverable-local and project-wide corpus truth. Accepted artifacts are git-versioned and delegated runs retain durable evidence. | `agents/AGENT_REVIEW.md`; `agents/AGENT_EVALUATION.md`; `agents/AGENT_RECONCILIATION.md`; `docs/CONTRACT.md`; `PROFESSIONAL_ENGINEERING.md` §4.1 |

### C.1.2 Responsibility in Decision Making (APEGA §3.1.1.2)

APEGA §3.1.1.2 requires that the licensed professional be responsible for all technical engineering decisions. The following table maps the specific decision-making obligations to Chirality mechanisms.

| APEGA Requirement | Chirality Mechanism | Governing Document |
|---|---|---|
| Licensed professional considers and documents relevant issues | Structured deliverable context files record identity and traceability (`_CONTEXT.md`), dependency summary (`_DEPENDENCIES.md`), and source document pointers (`_REFERENCES.md`) for every deliverable. These are not optional; they are required structural elements of the project filesystem. | `docs/SPEC.md` §4 (`_CONTEXT.md`), §5 (`_DEPENDENCIES.md`), §7 (`_REFERENCES.md`); `PROFESSIONAL_ENGINEERING.md` §4.2 |
| Technical direction provided through formal means | Technical direction is provided through agent briefs, explicit gate decisions, and conflict adjudication at human gates. Licensed professionals are the mandatory decision authority; agents propose but do not declare human outcomes. | `docs/CONTRACT.md` §§1.3, 1.7; `docs/DBM_Agent_Instruction_Architecture.md` §§2, 6; `PROFESSIONAL_ENGINEERING.md` §4.2 |
| Licensed professional available to review and approve decisions | Agent 0/1 decision interfaces and gate-controlled workflows require the licensed professional at defined consequential decisions. Agent 2 launch cites prior human run approval; outputs cannot advance lifecycle state without human authorization. | `docs/CONTRACT.md` §§1.3, 1.7; `docs/TYPES.md` §5; `PROFESSIONAL_ENGINEERING.md` §4.2 |
| All decisions recorded in durable project record | Every decision is recorded in versioned files: Decision Logs, `_MEMORY.md` (working memory per deliverable), and `_STATUS.md` (lifecycle history). If a decision is not in a versioned file, it does not exist for purposes of reliance. Agents are prohibited from maintaining hidden state that diverges from the filesystem. | `docs/SPEC.md` §3 (`_STATUS.md`), §8 (`_MEMORY.md`); `docs/DIRECTIVE.md` §2.2 (Git Is the Event Store), §2.5 (No Hidden Memory); `docs/CONTRACT.md` §1.5 (K-STATUS-1); `PROFESSIONAL_ENGINEERING.md` §4.2 |

### C.1.3 Documentation of Due Diligence (APEGA §3.1.1 — Record Keeping Requirement)

APEGA §3.1.1 requires that the process for direct supervision and control and the associated record keeping be described in the PPMP.

| APEGA Requirement | Chirality Mechanism | Governing Document |
|---|---|---|
| Process description in PPMP | The complete direct supervision and control framework for AI agents is documented in `PROFESSIONAL_ENGINEERING.md`, which is referenced by the firm's PPMP. | `PROFESSIONAL_ENGINEERING.md` §4 (Direct Supervision and Control of AI Agents) |
| Agent instruction documentation | Agent instruction files (`agents/AGENT_*.md`) provide documented scope, duties, authorities, and constraints for each agent. These are part of the firm's controlled quality system: versioned, reviewed, and subject to no silent behavior changes. | `agents/AGENT_*.md` (all agent instruction files); `PROFESSIONAL_ENGINEERING.md` §6.2 |
| Governance documentation | The `docs/` directory contains the firm's full governance framework: design philosophy (`DIRECTIVE.md`), physical specifications (`SPEC.md`), domain vocabulary (`TYPES.md`), invariant contracts (`CONTRACT.md`), and agent architecture design basis (`DBM_Agent_Instruction_Architecture.md`). | `docs/DIRECTIVE.md`, `docs/CONTRACT.md`, `docs/SPEC.md`, `docs/TYPES.md`, `docs/DBM_Agent_Instruction_Architecture.md`; `PROFESSIONAL_ENGINEERING.md` §4.3 |
| Complete development record | Git history provides the complete development record of all project state, including every agent output, human decision, and lifecycle transition, with full diff-based traceability. | `docs/DIRECTIVE.md` §2.2 (Git Is the Event Store); `PROFESSIONAL_ENGINEERING.md` §4.3 |
| Immutable audit trail | Timestamped, append-only snapshot folders preserve all analysis outputs. No snapshot folder may be modified after creation. | `docs/CONTRACT.md` §1.10 (K-SNAP-1); `docs/SPEC.md` §11 (Snapshot and Pointer Conventions); `PROFESSIONAL_ENGINEERING.md` §4.3 |

---

## C.2 Thorough Review (APEGA §3.1.2)

APEGA §3.1.2 requires thorough review before authentication of professional work products that were prepared by others. Thorough review is defined as an evaluation of outputs sufficient to verify their reliability, validity, and technical accuracy, and to accept professional responsibility for them. The Chirality architecture satisfies this obligation through the REVIEW agent's 5-gate protocol, the system's epistemic labeling framework, and the authentication gate structure.

### C.2.1 Reliability, Accuracy, and Validity (APEGA §3.1.2.1)

APEGA §3.1.2.1 specifies the substantive content of thorough review. The following table maps each item to Chirality mechanisms.

| APEGA Requirement | Chirality Mechanism | Governing Document |
|---|---|---|
| Review of scope of the work, including work done by any agent | Scope of work is formally captured in `_CONTEXT.md` (scope items and objectives) per deliverable, and confirmed at Gate 1 (Precondition Check) of the REVIEW agent's 5-gate protocol. The scope record is a required structural element and must be present before a review may proceed. | `docs/SPEC.md` §4 (`_CONTEXT.md`); `agents/AGENT_REVIEW.md` (Gate 1 — Precondition Check); `PROFESSIONAL_ENGINEERING.md` §5.2 |
| Review of relevant design and operational conditions, including risk assessments and mitigation strategies | Risk assessments, operational conditions, and mitigation strategies are captured as governed deliverable content. Findings related to risk adequacy are surfaced during Gate 3 (Findings Capture) of the review protocol with severity classification. CRITICAL findings must have human-resolved dispositions before an IN_PROGRESS to CHECKING transition is permitted. | `agents/AGENT_REVIEW.md` (Gate 3 — Findings Capture; transition readiness criteria); `docs/TYPES.md` §5 (Lifecycle State Machine); `PROFESSIONAL_ENGINEERING.md` §5.2 |
| Review of assumptions, limitations, and expressed caveats | The system's epistemic labeling framework requires all non-trivial claims to be classified as FACT (directly observed in source with citation), ASSUMPTION (reasonable inference requiring validation), PROPOSAL (agent suggestion requiring human decision), or TBD (unknown, requiring resolution). Assumptions are structurally visible — not hidden in prose — enabling targeted review. | `docs/TYPES.md` §10 (Epistemic Labels); `docs/DIRECTIVE.md` §2.4 (Evidence Over Plausibility); `docs/CONTRACT.md` §1.9 (K-PROV-1, K-INVENT-1); `PROFESSIONAL_ENGINEERING.md` §5.2 |
| Suitability of work for intended purpose and compliance with local conditions | Suitability and local compliance are confirmed through the REVIEW agent checklist (Gate 2 — Checklist Generation), which derives review items from the deliverable's specifications, decomposition records, and declared dependencies. The licensed professional confirms checklist completeness at Gate 2 before review proceeds. | `agents/AGENT_REVIEW.md` (Gate 2 — Checklist Generation); `PROFESSIONAL_ENGINEERING.md` §5.2 |
| Health, safety, and environmental implications | HSE findings are captured as CRITICAL severity findings in the REVIEW gate protocol. CRITICAL findings must be resolved (not merely deferred) before a deliverable may advance to CHECKING status. The hierarchy of authority places laws and regulations — including HSE regulatory requirements — as the first constraint, overriding all other considerations. | `agents/AGENT_REVIEW.md` (Gate 3 — Findings; CRITICAL severity definition); `docs/DIRECTIVE.md` §3.4 (Hierarchy of Authority); `PROFESSIONAL_ENGINEERING.md` §3.1, §5.2 |
| Integrity and validity of all work products, including cross-deliverable consistency | EVALUATION performs generic coherence and dependency assessment. Activated RECONCILIATION aligns objectives, claims, artifacts, implementation evidence, lifecycle state, and remaining work across the corpus. Dependency registers remain authoritative deliverable-local records with provenance. | `agents/AGENT_EVALUATION.md`; `agents/AGENT_RECONCILIATION.md`; `docs/CONTRACT.md` §1.4 (K-DEP-1, K-DEP-2); `PROFESSIONAL_ENGINEERING.md` §5.2 |
| Applicable tasks related to the work (calculations, analyses, evaluations, interpretations) | Task-level outputs are captured in governed snapshots or managed child-run records with briefs, returns, status, and handoff evidence. | `docs/SPEC.md` §11; `docs/DBM_Agent_Instruction_Architecture.md` §§8–9; `docs/CONTRACT.md` §1.10; `PROFESSIONAL_ENGINEERING.md` §5.2 |
| Applicable materials and methods of construction, inspection, maintenance, or operation | Materials, methods, and construction requirements are captured within deliverable document kits and traced through accepted project/decomposition state. | `docs/SPEC.md` §2; `docs/DBM_Agent_Instruction_Architecture.md` §8; `PROFESSIONAL_ENGINEERING.md` §5.2 |
| Relevancy and accuracy of the applicable tools used in PWP preparation, including software, hardware, firmware, applications, and other technologies | The licensed professional must understand what each agent is instructed to do, what its outputs represent, how to verify them, and the failure modes of LLM-based systems (hallucination, omission, plausible-sounding error). The system enforces tool competence as a prerequisite to reliance. Technology provider due diligence — including evaluation of model capabilities, limitations, safety practices, and the impact of model updates — is a documented firm obligation. The deterministic/probabilistic boundary ensures that tasks admitting algorithmic validation are implemented as deterministic tools, not left to LLM reasoning; the tool registry indexes all such tools. | `PROFESSIONAL_ENGINEERING.md` §3.3 (Competence Includes Tool Competence), §6.3 (Deterministic and Probabilistic Boundary), §6.4 (Technology Provider Due Diligence); `tools/REGISTRY.md` |
| Interdisciplinary reviews where the work crosses discipline boundaries | REVIEW surfaces cross-discipline obligations at Gate 2. EVALUATION identifies interface conflicts; activated RECONCILIATION determines their corpus-wide concordance effect. | `agents/AGENT_REVIEW.md`; `agents/AGENT_EVALUATION.md`; `agents/AGENT_RECONCILIATION.md`; `docs/SPEC.md` §5; `docs/CONTRACT.md` §1.4; `PROFESSIONAL_ENGINEERING.md` §5.2 |

**5-Gate Review Protocol Summary.** The REVIEW agent (`agents/AGENT_REVIEW.md`) implements the following structured review sequence. Every lifecycle transition from IN_PROGRESS to CHECKING or from CHECKING to ISSUED must traverse all five gates.

| Gate | Function | Authority |
|---|---|---|
| Gate 1 | Precondition check (lifecycle state, context validity) | Agent validates; human confirms scope |
| Gate 2 | Checklist generation from specifications, decomposition records, and declared dependencies | Agent derives; human confirms completeness |
| Gate 3 | Findings capture (iterative) | Human provides findings; agent records with evidence and severity classification |
| Gate 4 | Disposition review | Human rules on all findings |
| Gate 5 | Lifecycle transition decision | Agent recommends; human approves |

**Transition readiness criteria** (defined in `docs/SPEC.md` §3; `docs/TYPES.md` §5):

- *IN_PROGRESS to CHECKING:* All CRITICAL findings must have a non-TBD human disposition.
- *CHECKING to ISSUED:* All CRITICAL findings RESOLVED; all MAJOR findings RESOLVED or DEFERRED with documented rationale.

### C.2.2 Adherence to Regulatory Requirements (APEGA §3.1.2.2)

APEGA §3.1.2.2 requires that thorough review verify compliance with the *Engineering and Geoscience Professions Act*, the *General Regulation*, applicable APEGA practice standards, bulletins, and guidelines, and any contractual requirements to meet regulatory approvals or permit requirements.

| APEGA Requirement | Chirality Mechanism | Governing Document |
|---|---|---|
| Compliance with the EGP Act and the General Regulation | The hierarchy of authority (laws and regulations as the first constraint) is enforced through agent instruction invariants. Agents cannot override applicable legislation. Regulatory compliance obligations flow to the licensed professional who authenticates the PWP. | `docs/DIRECTIVE.md` §3.4 (Hierarchy of Authority); `PROFESSIONAL_ENGINEERING.md` §3.5 (Hierarchy of Authority), §1.1 (Governing Legislation) |
| Compliance with APEGA practice standards, bulletins, and guidelines | The firm's practice standard (`PROFESSIONAL_ENGINEERING.md`) is grounded in the APEGA practice standards identified in §1.1 and maps the firm's architecture to their requirements. Adherence to this standard is a condition of authentication. | `PROFESSIONAL_ENGINEERING.md` §1.1, §5.3 |
| Compliance with contractual requirements for regulatory approvals or permits | Project-specific regulatory requirements are captured in the deliverable's `_CONTEXT.md` (scope items and objectives) and `_REFERENCES.md` (applicable regulatory documents). Compliance with these requirements is a checklist item at Gate 2 of the review protocol. | `docs/SPEC.md` §4 (`_CONTEXT.md`), §7 (`_REFERENCES.md`); `agents/AGENT_REVIEW.md` (Gate 2); `PROFESSIONAL_ENGINEERING.md` §5.3 |

### C.2.3 Adherence to Quality Control and Assurance (APEGA §3.1.2.3)

APEGA §3.1.2.3 requires that thorough review verify that PWPs are produced following the quality control and assurance processes defined in the PPMP, and that deliverables are clear, readable, consistent, and complete.

| APEGA Requirement | Chirality Mechanism | Governing Document |
|---|---|---|
| PWPs produced following QC/QA processes defined in the PPMP | The firm's complete QC/QA framework is defined in `PROFESSIONAL_ENGINEERING.md` §6. Architectural controls include DIRECTIVE, CONTRACT, SPEC, TYPES, the workflow-component standard, and the decomposition standard. Conformance is checked by AUDIT_AGENTS under EVALUATION. | `PROFESSIONAL_ENGINEERING.md` §6.1; `docs/CONTRACT.md`; `docs/WORKFLOW_COMPONENT_STANDARD.md`; `docs/DECOMPOSITION_STANDARD.md` |
| Deliverables are clear, readable, consistent, and complete | Clarity and completeness are structural properties enforced through the document kit format (Datasheet, Specification, Guidance, Procedure), required metadata files (`_CONTEXT.md`, `_STATUS.md`, `_DEPENDENCIES.md`, `_REFERENCES.md`), and the REVIEW agent's checklist. Epistemic labeling ensures that all assumptions and TBD items are conspicuously identified rather than hidden. | `docs/SPEC.md` §2 (Document Kit), §3–§7 (required metadata structures); `agents/AGENT_REVIEW.md` (Gate 2 checklist); `docs/TYPES.md` §10 (Epistemic Labels); `PROFESSIONAL_ENGINEERING.md` §5.4, §6.1 |
| Agent instruction governance treated as controlled documentation | Agent instruction files are versioned, reviewed before release, subject to no silent behavior changes, and audited against ratified invariants plus candidate standards whose acceptance state is explicit. | `PROFESSIONAL_ENGINEERING.md` §6.2 |
| Clear boundary between deterministic and probabilistic operations | Tasks admitting algorithmic validation are implemented as deterministic tools, not left to LLM probabilistic reasoning. This ensures that the probabilistic layer (LLM-based agents) is confined to work that genuinely requires inference. | `PROFESSIONAL_ENGINEERING.md` §6.3 (Deterministic and Probabilistic Boundary); `tools/REGISTRY.md` |

---

## C.3 Authentication (APEGA §3.1 and *Authenticating Professional Work Products*)

Authentication is defined in the APEGA framework as the act by which a licensed professional represents that they have completed, performed a thorough review of, or directly supervised and controlled the work, and accepts professional responsibility for it. The Chirality architecture implements authentication as a controlled gate — the final and irreversible human action in the lifecycle state machine.

| APEGA Requirement | Chirality Mechanism | Governing Document |
|---|---|---|
| Authentication requires prior direct supervision and control, OR thorough review | Authentication is permitted only when either: (a) the licensed professional provided direct supervision and control over AI-assisted work per §4 of the professional practice standard, or (b) the licensed professional conducted a thorough review per §5.1–5.4. In either case, the additional conditions below must also be satisfied. | `PROFESSIONAL_ENGINEERING.md` §5.5 |
| Licensed professional must be competent to verify the work | The licensed professional must not use an AI agent to perform work they are not competent to verify manually. "An AI said so" is never a defensible basis of design. This competence requirement is non-delegable. | `PROFESSIONAL_ENGINEERING.md` §3.3; `docs/DIRECTIVE.md` §3.3 |
| Validation by Responsible Member per the PPMP | The PWP must be validated by the Responsible Member (Ryan Tufts, P.Eng., APEGA 78780) per the firm's PPMP before authentication. | `PROFESSIONAL_ENGINEERING.md` §5.5, §11 |
| Authentication binds to a specific content version | Authentication binds to a specific git SHA. Content change after authentication voids the authentication. A deliverable is considered dirty if any governed input has changed since its last approved SHA. Merge to main is permitted only when branch HEAD equals the approved SHA. | `docs/CONTRACT.md` §1.2 (K-AUTH-2), §1.6 (K-VAL-1), §1.8 (K-MERGE-1); `PROFESSIONAL_ENGINEERING.md` §5.5 |
| No agent may authenticate or claim to authenticate work | Only humans author binding approval records. No agent may claim to certify, approve, sign, seal, or issue work for reliance. This prohibition is an architectural invariant, not merely a policy statement. | `docs/CONTRACT.md` §1.2 (K-AUTH-1); `PROFESSIONAL_ENGINEERING.md` §3.2, §9.3 |
| Seal and signature apply to a specific version | The licensed professional's seal and signature apply to the specific version of the work identified by the authentication SHA. Content addressed approval makes the integrity of the authentication relationship mechanically verifiable. | `docs/CONTRACT.md` §1.2 (K-AUTH-1, K-AUTH-2); `docs/DIRECTIVE.md` §2.3 (Human Authority at Every Gate); `PROFESSIONAL_ENGINEERING.md` §5.5 |

---

## C.4 Definition Mapping

The following table reproduces, from `PROFESSIONAL_ENGINEERING.md` §2, the mapping between APEGA statutory terms and their equivalents in the Chirality agent system. This mapping establishes the terminological basis on which the compliance analysis in §§C.1–C.3 rests. All terms defined in the APEGA practice standard *Relying on the Work of Others and Outsourcing* (§1.3) apply throughout the professional practice standard; the following definitions identify how each term maps to the firm's AI agent architecture.

| APEGA Term | Definition | Chirality System Equivalent |
|---|---|---|
| **Licensed Professional** | An individual entitled by the EGP Act to practise engineering in Alberta | The P.Eng. operating the agent system and authenticating PWPs |
| **Permit Holder** | A partnership, association, or corporation holding a Permit to Practice under the EGP Act | Chirality AI Ltd. (APEGA P17007) |
| **Responsible Member** | An APEGA licensed professional responsible for oversight of the practice of engineering by the permit holder | The firm's Responsible Member as registered with APEGA (Ryan Tufts, P.Eng., APEGA 78780) |
| **Professional Work Product (PWP)** | An output of professional services with technical information relied upon by others to make a decision or take action | Authenticated deliverables issued for reliance (lifecycle state: ISSUED) |
| **Authentication** | A licensed professional has completed, performed a thorough review of, or directly supervised and controlled the work and accepts professional responsibility | Human approval, seal, and signature at the issuance gate, binding to a specific git SHA |
| **Validation** | A Responsible Member has reviewed the PWP to ensure it meets QC/QA measures in the PPMP | Responsible Member review per the firm's PPMP |
| **Direct Supervision and Control** | Directing, monitoring, and controlling engineering work, including making all decisions related to the practice | Gate-controlled agent orchestration under the Agent 0/1/2 runtime hierarchy with human authority at every gate |
| **Thorough Review** | An evaluation of the outputs of professional services prepared by others to verify their reliability, validity, and technical accuracy | REVIEW agent 5-gate protocol (`agents/AGENT_REVIEW.md`) plus the licensed professional's authentication decision |
| **Due Diligence** | The level of judgement, care, forethought, and determination a person reasonably uses to avoid harming oneself, other people, property, or the environment | The licensed professional's exercise of judgment at every gate, supported by the system's evidence trail (provenance, epistemic labels, immutable snapshots, git history) |
| **AI Agent** | A controlled system architecture (model + instructions + tools + file access + governance) that performs bounded work under the direction of a licensed professional | An `AGENT_*.md` instruction file instantiated at runtime within the Chirality agent operating system |
| **Agent Instruction Architecture** | The firm's documented framework of agent instruction files, governance documents, invariant contracts, and deterministic tools that constitutes the direct supervision and control structure for AI agents | The `agents/`, `docs/`, and `tools/` directories as governed by the firm's release engineering process (`PROFESSIONAL_ENGINEERING.md` §6.2) |

---

## C.5 Invariant Cross-Reference

The following table consolidates the K-* invariants cited throughout this appendix, identifying the regulatory obligation each invariant serves. This cross-reference enables a regulator to verify that every invariant in the catalog has an identified regulatory function. The table reflects the live `docs/CONTRACT.md` catalog as of 2026-07-02; the mappings for the K-CLAIM-1/K-WRITE-2/K-AGENTS-1/K-DOMAIN-* additions are the firm's proposed alignments, offered with the same interpretive status as the rest of this appendix.

| Invariant | Statement (abbreviated) | APEGA Obligation Served |
|---|---|---|
| **K-AUTH-1** | Only humans author binding approval records. No agent may claim to certify, approve, sign, seal, or issue work for reliance. | Authentication — APEGA §3.1; *Authenticating Professional Work Products* |
| **K-AUTH-2** | Approvals bind to a specific git SHA. Content change after approval voids the approval. | Authentication integrity — APEGA §3.1 |
| **K-BIND-1** | Approvals are always binding and only binding. | Authentication scope — APEGA §3.1 |
| **K-SEAL-1** | Agent 2 context is sealed and the launch cites approval at the applicable human gate; runtime metadata does not substitute for that act. | Direct supervision and control — APEGA §3.1.1 |
| **K-GHOST-1** | Agent 2 context is limited to declared files/references and sealed brief content. | Scope documentation — APEGA §3.1.1.1 |
| **K-DEP-1** | Deliverable-local dependency files are authoritative. | Cross-deliverable integrity — APEGA §3.1.2.1 |
| **K-DEP-2** | Dependency references must resolve to existing deliverable IDs. | Traceability — APEGA §3.1.2.1 |
| **K-STATUS-1** | `_STATUS.md` is the canonical lifecycle state file for each deliverable. | Record keeping — APEGA §3.1.1 |
| **K-STALE-1** | Upstream changes propagate staleness to all transitive dependent deliverables. | Change impact tracking — APEGA §3.1.2.1 |
| **K-STALE-2** | Stale items must be triaged by a human before being considered current. | Human decision authority — APEGA §3.1.1.2 |
| **K-VAL-1** | A deliverable is dirty if any governed input has changed since its last approved SHA. | Authentication integrity — APEGA §3.1 |
| **K-GATE-1** | Gates are dynamic per project instance. Minimum: seal transition + pipeline run approval. | Ongoing human involvement — APEGA §3.1.1.1 |
| **K-MERGE-1** | Merge to main allowed only when branch HEAD equals the approved SHA. | Authentication integrity — APEGA §3.1 |
| **K-PROV-1** | Every non-trivial governed claim must cite evidence (source path + best-effort section reference) or carry explicit `location TBD`; dependency rows are a schema-specific instance. | Reliability, accuracy, and validity — APEGA §3.1.2.1 |
| **K-INVENT-1** | Unknown values become TBD, not guessed. | Reliability, accuracy, and validity — APEGA §3.1.2.1 |
| **K-CONFLICT-1** | Conflicts between sources must be surfaced, not silently resolved. | Reliability, accuracy, and validity — APEGA §3.1.2.1; decision-making responsibility — APEGA §3.1.1.2 |
| **K-WRITE-1** | Every agent has an explicit write scope. No agent writes outside its declared zone. | Scope and authority documentation — APEGA §3.1.1.1 |
| **K-SNAP-1** | Task agent output snapshots are immutable. | Audit trail — APEGA §3.1.1 (record keeping) |
| **K-HIER-1** | Projects are decomposed as packages containing deliverables. | Scope documentation — APEGA §3.1.1.1 |
| **K-ID-1** | Deliverable IDs are stable and persist across path changes. | Traceability — APEGA §3.1.2.1 |
| **K-CLAIM-1** | Claims, conclusions, and characterizations must not overstate what the available warrant supports. | Reliability, accuracy, and validity — APEGA §3.1.2.1; honest reporting under the duty of care |
| **K-WRITE-2** | Agent writes must be path-contained within the active checkout; out-of-tree targets are rejected deterministically. | Scope and authority documentation; fault containment — APEGA §3.1.1.1 |
| **K-AGENTS-1** | `AGENTS.md` is an authoritative governance surface; live registries govern over narrative. | QC/QA process adherence — APEGA §3.1.2.3; scope documentation — APEGA §3.1.1.1 |
| **K-DOMAIN-1** | Domain engines own authoritative domain truth; Chirality governs the work around them. | Tool relevancy and accuracy — APEGA §3.1.2.1 |
| **K-DOMAIN-2** | Protected domain paths are write-quarantined; domain-controlled writes occur only through declared deterministic tools. | Tool relevancy and accuracy; QC processes — APEGA §3.1.2.1, §3.1.2.3 |
| **K-DOMAIN-3** | Domain operations require an OperationProposal record and explicit human acceptance. | Responsibility in decision making — APEGA §3.1.1.2 |
| **K-DOMAIN-4** | Domain-engine outputs must not be represented as professional approval; validation-passed is necessary, not sufficient. | Authentication reservation — APEGA §3.1; reliability review — APEGA §3.1.2.1 |

---

*This appendix was prepared as part of the thesis examining the Chirality agent instruction architecture as a framework for AI governance in APEGA-regulated professional engineering practice. The source for all APEGA requirements is the practice standard* Relying on the Work of Others and Outsourcing *(May 2021, v4.0). The source for all Chirality mechanism citations is* PROFESSIONAL_ENGINEERING.md *(Revision 1, 2026-03-29) and the governance documents in the `docs/` and `agents/` directories of the Chirality agent operating system.*
