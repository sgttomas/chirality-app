# Chapter 6 — Professional Practice Integration

---

## 6.1 Introduction

The preceding chapters established the philosophical framework, architectural design, and epistemic architecture of the Chirality agent governance system. This chapter examines the regulatory dimension of that architecture: specifically, how a licensed professional engineer in Alberta can direct AI agents within the Chirality framework while satisfying professional obligations under the *Engineering and Geoscience Professions Act* (EGP Act) and APEGA practice standards.

The central argument is precise and bears stating at the outset. The APEGA practice standard *Relying on the Work of Others and Outsourcing* (May 2021, v4.0) defines obligations on the licensed professional when that professional relies on work prepared by others. These obligations — direct supervision and control (§3.1.1) and thorough review (§3.1.2) — are specified entirely in terms of what the professional must do. They are not conditioned on what the worker must be. Therefore, the question of whether a worker is a human subordinate or an AI agent is, from the regulatory standpoint, irrelevant to the professional's obligations. What matters is whether the governance architecture through which the professional directs the work satisfies those obligations in substance.

This chapter argues that the Chirality architecture can satisfy them in substance. Section 6.2 establishes the regulatory framework. Section 6.3 develops the central argument as a logical chain. Sections 6.4 and 6.5 map specific APEGA requirements to Chirality mechanisms for direct supervision and control and for thorough review, respectively. Section 6.6 addresses the professional obligations that remain invariantly human. Section 6.7 examines the quality control and assurance framework. Section 6.8 articulates the human-AI contract that the architecture enforces. Section 6.9 identifies the genuine limitations of the regulatory mapping. Section 6.10 summarizes the contribution.

The APEGA regulatory mapping is developed in detail in Appendix C. This chapter presents the argument and synthesizes the evidence; Appendix C provides the full compliance trace from regulatory text to architectural implementation.

---

## 6.2 Regulatory Framework

### 6.2.1 Governing Legislation and Standards

The professional practice of engineering in Alberta is governed by the *Engineering and Geoscience Professions Act* (EGP Act), specifically Sections 1(q), 1(r), 2(1), 3(2), 3(3), 5(1), 6(2), and 6(3), and by the *General Regulation*, Part 7 (Professional Practice Management Plans), Part 8 (Practice Standards), and Sections 49 and 54 (Authentication). These instruments establish the conditions under which engineering work may be performed, authenticated, and issued for reliance.

APEGA practice standards operationalize these legislative requirements. Three standards are directly engaged by AI-assisted professional practice:

- *Relying on the Work of Others and Outsourcing* (May 2021, v4.0), which defines the professional's obligations when any portion of a professional work product (PWP) is prepared by others — including the obligations of direct supervision and control (§3.1.1) and thorough review (§3.1.2)
- *Authenticating Professional Work Products*, which governs the final act by which a licensed professional accepts professional responsibility for a PWP
- The *Professional Practice Management Plan (PPMP) Guideline*, which requires permit holders to describe their QC/QA processes, including processes for relying on the work of others, in a documented PPMP

These three instruments form a coherent framework. The PPMP defines the firm's practice system. The relying-on-others standard defines the professional's obligations when others contribute to PWPs. The authentication standard defines the act that completes the professional's assumption of responsibility. Together, they establish what a licensed professional must do to lawfully issue an AI-assisted engineering work product for reliance.

The Chirality AI Ltd. professional practice standard (`PROFESSIONAL_ENGINEERING.md`, Revision 1, 2026-03-29), referenced by the firm's PPMP, documents how each of these obligations is satisfied when licensed professionals use the Chirality agent system.

### 6.2.2 Professional Work Products and Reliance

The EGP Act and APEGA define a professional work product (PWP) as an output of professional services containing technical information that others rely upon to make decisions or take actions. In the Chirality system, PWPs correspond to authenticated deliverables that have reached the ISSUED lifecycle state — the final and irreversible state in the deliverable lifecycle state machine. The lifecycle state machine is defined in `docs/SPEC.md` §3 and `docs/TYPES.md` §5.

It is important to distinguish between deliverable outputs in earlier lifecycle states and authenticated PWPs. Agent-produced drafts in the IN_PROGRESS or CHECKING states are not PWPs — they are work in progress that has not yet been accepted by a licensed professional. A deliverable becomes a PWP only when a licensed professional has satisfied either the direct supervision and control standard or the thorough review standard, and has then authenticated the work under the *Authenticating Professional Work Products* standard. This distinction is architecturally enforced: no agent may advance a deliverable to the ISSUED state, and no agent may claim to authenticate work (K-AUTH-1, `docs/CONTRACT.md` §1.2).

### 6.2.3 Applicability to AI-Assisted Work

APEGA has not, as of this writing, issued specific guidance addressing AI agents or large language model (LLM)-based systems in professional practice. [RATIONALE: This is a genuine regulatory gap; the analysis in this chapter represents an interpretation by the firm and the author, not a regulatory determination by APEGA.] The question of how existing practice standards apply to AI-assisted work therefore requires an interpretive analysis — which the Chirality professional practice standard provides by grounding the analysis in the regulatory text itself.

The interpretive move is straightforward: the standard *Relying on the Work of Others and Outsourcing* does not limit its application to human workers. Its obligations are defined by reference to what the licensed professional must do, not by reference to the nature or legal status of the entity performing the work. This interpretation is examined in detail in §6.3.

---

## 6.3 The Central Argument: AI Agents as "Others"

### 6.3.1 Structure of the Argument

The central argument of this chapter can be expressed as a logical chain. The premises are drawn directly from the regulatory text and the architectural record; the conclusion follows from them. The chain is:

1. APEGA §3.0 (*Relying on the Work of Others*) imposes obligations on the licensed professional when that professional relies on work prepared by others.
2. These obligations — direct supervision and control (§3.1.1) and thorough review (§3.1.2) — are specified in terms of what the professional must do: how thoroughly the professional must supervise, how rigorously the professional must review, and how the professional must document that supervision or review.
3. The regulatory text does not condition these obligations on the nature, legal status, or professional standing of the entity that prepared the work. The obligations are the same whether the work was prepared by a licensed professional, an engineering intern, an unlicensed technologist, or a contractor operating under direct supervision.
4. AI agents that produce work under the direction of a licensed professional assume no professional responsibility. The entire chain of responsibility flows to the licensed professional who authenticates the resulting PWP.
5. This makes the AI agent case structurally identical to the case of an unlicensed individual working under direct supervision and control: the supervising professional bears full responsibility for the work, and the obligations of §3.1.1 apply.
6. Therefore, this thesis argues that the existing APEGA framework can be read to apply directly to AI-assisted professional practice, because AI agents are "others" within the meaning of §3.0 and the obligations are defined by what the professional must do.
7. The relevant regulatory question is then: can the Chirality governance architecture satisfy the obligations of §3.1.1 (direct supervision and control) and §3.1.2 (thorough review) in substance?
8. This chapter and Appendix C provide the argument and evidence for answering that question in the affirmative, while recognizing that the result remains an interpretive position rather than a regulatory ruling.

This argument is the structural foundation of the firm's professional practice standard (`PROFESSIONAL_ENGINEERING.md` §1.3) and is the thesis position advanced in this chapter.

### 6.3.2 Why the Framework Applies Directly, Not by Analogy

The distinction between "applies directly" and "applies by analogy" is not merely rhetorical. An analogical application would suggest that AI agents are *like* unlicensed human workers in relevant respects, and that the professional's obligations are *similar* to those that would apply in the human case. A direct application holds that the obligations are the *same*, because the regulatory text makes no distinction that would produce a different result.

The relevant provision of the APEGA practice standard is §3.1, which requires that a licensed professional who relies on work prepared by others satisfy either the direct supervision and control standard or the thorough review standard before authenticating the resulting PWP. The standard defines "direct supervision and control" as directing, monitoring, and controlling engineering work throughout its lifespan, including making all decisions related to the practice of engineering. The standard defines "thorough review" as an evaluation of outputs sufficient to verify their reliability, validity, and technical accuracy, and to accept professional responsibility for them.

Neither definition references the nature of the entity that performed the work. Both are defined entirely in terms of the professional's conduct. An AI agent that drafts a deliverable section, extracts dependencies from source documents, and returns a structured output is performing work that the licensed professional relies upon. The professional's obligation is to have either directed that work through the mechanisms that constitute direct supervision and control, or to have reviewed it through the mechanisms that constitute thorough review — and then to authenticate the result.

There is a potential objection: that "others" in APEGA §3.0 contemplates natural persons capable of bearing some measure of professional responsibility, and that AI agents, being incapable of professional responsibility, are better understood as tools rather than as workers. This objection would support the view that using an AI agent is more like using calculation software than like relying on a subordinate's work. [COMPARE: British Columbia — EGBC Practice Advisory on AI Tools] [COMPARE: Ontario — PEO position statements on AI in engineering] [CITE: professional responsibility theory in engineering regulation]

The firm resolves this question conservatively, in favor of the "others" interpretation, for two reasons. First, the conservative interpretation places more rigorous obligations on the professional — the full supervision and review requirements of §3.1 — rather than treating AI agent outputs as merely tool outputs requiring whatever review the professional deems appropriate. Second, the firm's position is that the distinction between "tool" and "worker" is best understood by reference to the complexity, discretion, and consequentiality of what the system does. An AI agent that interprets ambiguous source documents, proposes decompositions, drafts design rationale, and surfaces conflicts is exercising a form of judgment, even if it bears no responsibility for that judgment. The appropriate regulatory response is not to classify such outputs as mere tool outputs but to require that the professional supervise and review them with the rigor that §3.1 demands.

This conservative interpretation aligns with the regulatory purpose of the APEGA framework: the protection of the public through the accountability of licensed professionals for the work they issue for reliance.

### 6.3.3 The Technology Provider Distinction

The argument requires one further clarification. The LLM technology provider — currently Anthropic — is not providing professional services and does not assume professional responsibility under the EGP Act. The technology provider is a vendor supplying a technology component: a large language model that serves as the cognitive engine within the agent system. This is analogous to the relationship between a firm and the provider of structural analysis software. The software vendor does not bear professional responsibility for the engineer's analysis; the engineer does.

The firm's agents are not the LLM itself but the controlled system architecture — instruction file, tool access, write scope, governance constraints, and runtime context — that the firm has engineered around the LLM. It is this architecture that constitutes the "agent" for purposes of the professional practice standard. The technology provider supplies a cognitive component; the firm supplies the governance architecture that makes that component safe to rely upon in professional practice. The professional's obligations under §3.1 run to the work produced by that governed architecture, not to the underlying technology.

This distinction matters because it clarifies what the firm's due diligence obligations are. The firm must assess the LLM as a technology component — its capabilities, limitations, failure modes, and the impact of model updates on agent behavior (addressed in §6.7) — but the professional's obligations of supervision and review run to the agent outputs, not to the LLM's internal mechanisms, which are not accessible for inspection.

---

## 6.4 Direct Supervision and Control

### 6.4.1 The APEGA Standard

APEGA §3.1.1 requires that a licensed professional who relies on the work of others provide direct supervision and control over that work. The standard defines direct supervision and control as directing, monitoring, and controlling engineering work throughout its lifespan, including making all decisions related to the practice of engineering. Two sets of specific obligations follow from this definition: active involvement obligations (§3.1.1.1) and responsibility-in-decision-making obligations (§3.1.1.2). The standard also requires that the process and record keeping for direct supervision and control be described in the PPMP (§3.1.1 record keeping requirement).

The Chirality architecture satisfies each of these obligations through mechanisms that are architectural — that is, structurally enforced — rather than merely procedural recommendations. The following subsections present the argument for each obligation.

### 6.4.2 Active Involvement (APEGA §3.1.1.1)

APEGA §3.1.1.1 identifies five specific obligations constituting active involvement. For each, the Chirality mechanism is identified and the governing document cited. Appendix C, Table C.1.1, provides the full compliance trace.

**Directing, monitoring, and controlling work throughout its lifespan.** The licensed professional directs, monitors, and controls AI agent work through the gate-controlled orchestration model. Type 1 (Manager) agents operate through interactive sessions in which the licensed professional makes consequential decisions at every phase transition. Type 2 (Specialist) agents execute only within bounded briefs defined by the licensed professional or an authorized Type 1 agent. Human authority is the halting condition for every workflow: no agent may autonomously advance workflow stages, approve deliverables, or resolve conflicts. This is enforced by invariants K-GATE-1 (dynamic gates with minimum seal and pipeline approval requirements) and K-SEAL-1 (no Type 2 execution before context is sealed and gate-approved by a human). The orchestration architecture is defined in `docs/DBM_Agent_Instruction_Architecture.md` §6.

The three-type agent hierarchy (Type 0 Architect / Type 1 Manager / Type 2 Specialist) is directly relevant here. As established in Chapter 4, authority flows downward through this hierarchy and escalation flows upward. A Type 2 agent cannot modify rules set by Type 0; a Type 1 agent cannot approve deliverables for external reliance. The human professional sits above all three types in the authority hierarchy, and every gate in the workflow requires human authorization before the next stage of work proceeds. This is not a policy commitment — it is a structural property of the architecture, enforced by the orchestration model and the invariant contract system.

**Establishing and documenting scope, duties, responsibilities, authorities, and limitations.** Every agent instruction file (`agents/AGENT_*.md`) declares the agent's type, class, interaction surface, write scope, blocking behavior, primary outputs, and non-negotiable invariants. These declarations are the formal record of scope, duties, responsibilities, authorities, and limitations for each agent — equivalent, in structural terms, to a position description for a human subordinate, but with the significant difference that the declarations are machine-enforced at runtime. Write scope enforcement is guaranteed by invariant K-WRITE-1: no agent writes outside its declared zone (`docs/CONTRACT.md` §1.10). The authority model is defined in `docs/TYPES.md` §4.3.

**Maintaining regular and ongoing communication.** Type 1 agents maintain interactive sessions with the licensed professional, presenting structured outputs and awaiting human decisions at gates before proceeding. Type 2 agents receive structured briefs (INIT-TASK) and return structured run reports with PASS/FAIL status and evidence. Session continuity is maintained through handoff artifacts (`NEXT_INSTANCE_STATE.md`, `NEXT_INSTANCE_PROMPT.md`) that preserve project context across sessions without hidden state. Working memory per deliverable is maintained in `_MEMORY.md` (defined in `docs/SPEC.md` §8). The brief and output contract formats are defined in `docs/DBM_Agent_Instruction_Architecture.md` §9.

This "regular and ongoing communication" requirement deserves comment in the AI context. For a human subordinate, ongoing communication involves informal channels — conversation, observation, questions — that may not leave a documentary record. For an AI agent, every interaction is structured and every consequential output is a versioned artifact in the git repository. In this sense, the Chirality architecture satisfies the communication requirement more completely than a comparable human supervision relationship: every agent output, every brief, every gate decision, and every session handoff is committed to version control and subject to diff-based review.

**Identifying and rectifying gaps in competencies.** The AUDIT_AGENTS system verifies conformance of agent instruction files against the canonical standard (`agents/AGENT_HELPS_HUMANS.md`). Three layers of contracts govern agent behavior: workflow design requirements R1–R9 (defined in `agents/AGENT_HELPS_HUMANS.md`), decomposition invariants I1–I10 (defined in `agents/AGENT_DECOMP_BASE.md`), and 20 system-wide K-* invariants (defined in `docs/CONTRACT.md`). The evaluation framework provides systematic assessment of agent output quality. Agent instruction governance follows release engineering discipline: instruction files are versioned, reviewed before release, and subject to no silent behavior changes (§6.7 of the professional practice standard). This is the mechanism by which the firm identifies and rectifies gaps in agent competencies — not through ad hoc review but through a systematic governance process.

**Completing periodic reviews to ensure PWPs are accurate and reliable.** The REVIEW agent (`agents/AGENT_REVIEW.md`) implements a formal 5-gate review process for all lifecycle transitions. The RECONCILIATION agent performs cross-deliverable coherence analysis. All agent outputs are git-committed, enabling diff-based review at any point in the work history. The review protocol is addressed in detail in §6.5.

### 6.4.3 Responsibility in Decision Making (APEGA §3.1.1.2)

APEGA §3.1.1.2 requires that the licensed professional be responsible for all technical engineering decisions. The Chirality architecture satisfies this requirement through four mechanisms:

**Structured context documentation.** Every deliverable has a required set of context files: `_CONTEXT.md` (scope items, objectives, and decomposition reference), `_DEPENDENCIES.md` (dependency summary), and `_REFERENCES.md` (source document pointers). These files are required structural elements of the project filesystem — not optional documents that a professional may or may not produce. They constitute the documented record of what the licensed professional considered in directing the work (defined in `docs/SPEC.md` §4, §5, §7).

**Technical direction through formal mechanisms.** Technical direction is provided through agent briefs, explicit gate decisions, and conflict adjudication at human gates. Agents propose; humans approve. Agents surface conflicts; humans rule. The licensed professional is the mandatory decision authority at every gate — no agent may bypass a gate or autonomously declare an outcome (K-GATE-1, K-SEAL-1).

**Availability to review and approve.** The gate-controlled workflow structure ensures that the licensed professional is a required participant in every consequential decision. Type 2 agents cannot proceed without prior gate approval; outputs cannot advance to a new lifecycle state without human authorization. The architecture guarantees availability by making human participation a structural precondition for progress.

**Decision records in durable project record.** Every decision must be recorded in versioned files: Decision Logs, `_MEMORY.md` (per `docs/SPEC.md` §8), and `_STATUS.md` lifecycle history (per `docs/SPEC.md` §3). Invariant K-STATUS-1 designates `_STATUS.md` as the canonical, human-readable lifecycle state file for each deliverable. Agents are prohibited from maintaining hidden state that diverges from the filesystem (`docs/DIRECTIVE.md` §2.5). As the firm's founding design principle states: if a decision is not in a versioned file, it does not exist for purposes of reliance.

### 6.4.4 Documentation of Due Diligence

APEGA §3.1.1 requires that the process for direct supervision and control and the associated record keeping be described in the PPMP. The Chirality professional practice standard (`PROFESSIONAL_ENGINEERING.md` §4.3) identifies four components of the documentation of due diligence:

- Agent instruction files (`agents/AGENT_*.md`) providing documented scope, duties, authorities, and constraints for each agent
- Governance documents (`docs/`) containing the complete governance framework: design philosophy, physical specifications, domain vocabulary, invariant contracts, and architectural design basis
- Git history providing the complete development record of all project state, including every agent output, human decision, and lifecycle transition
- Immutable snapshots providing a timestamped, append-only audit trail for all analysis outputs (enforced by K-SNAP-1, `docs/CONTRACT.md` §1.10)

The significance of the git history and immutable snapshot trail deserves emphasis. The audit trail for AI-assisted professional practice must be sufficient to enable a regulator, reviewer, or court to reconstruct what happened: what the agent was instructed to do, what it produced, what the professional reviewed, and what the professional decided at each gate. The Chirality architecture generates this record as an intrinsic byproduct of normal operation — not as a separate documentation burden imposed on the professional.

---

## 6.5 Thorough Review and Authentication

### 6.5.1 Applicability

Thorough review applies to all AI agent outputs that will be incorporated into PWPs. The Chirality professional practice standard requires that thorough review be conducted before authentication even when the licensed professional has provided direct supervision and control throughout the work (`PROFESSIONAL_ENGINEERING.md` §5.1). This requirement reflects the additional risk created by LLM failure modes — specifically, the risk that plausible-sounding outputs may contain errors, omissions, or hallucinations that a professional exercising due diligence would identify and resolve. [CITE: LLM reliability and hallucination in professional contexts]

In terms of the epistemic ontology formalized in Chapter 3 (§3.2.2) and developed in Chapter 5 (§5.5), thorough review is the process of auditing warrant sufficiency: the professional examines the claims within the deliverable, checks their warrants (provenance, epistemic labels), resolves gaps and conflicts through rulings, and determines whether the aggregate warrant state — the distribution of claims across the warrant lifecycle (UNWARRANTED → CITED → REVIEWED → AUTHENTICATED) — supports authentication. The epistemic architecture makes this assessment tractable by ensuring that every claim's warrant state is visible, enabling targeted rather than exhaustive review.

### 6.5.2 Reliability, Accuracy, and Validity (APEGA §3.1.2.1)

APEGA §3.1.2.1 specifies ten substantive areas that thorough review must address. The Chirality REVIEW agent (`agents/AGENT_REVIEW.md`) implements a 5-gate protocol that structures the professional's review across each of these areas. The gates are:

| Gate | Function | Authority |
|------|----------|-----------|
| Gate 1 | Precondition check (lifecycle state validity, context completeness) | Agent validates; human confirms scope |
| Gate 2 | Checklist generation from specifications, decomposition records, and declared dependencies | Agent derives; human confirms completeness |
| Gate 3 | Findings capture (iterative, severity-classified) | Human provides findings; agent records with evidence |
| Gate 4 | Disposition review (human ruling on all findings) | Human rules; agent records |
| Gate 5 | Lifecycle transition decision | Agent recommends; human approves |

The 5-gate protocol maps to the ten APEGA §3.1.2.1 areas as follows.

**Scope of the work, including work done by any agent.** Scope is formally captured in `_CONTEXT.md` per deliverable and confirmed at Gate 1. The scope record is a required structural element that must be present before a review may proceed.

**Relevant design and operational conditions, including risk assessments and mitigation strategies.** Risk and operational conditions are captured as governed deliverable content. Findings related to risk adequacy are surfaced during Gate 3 with severity classification. CRITICAL findings must have human-resolved dispositions before a deliverable may advance from IN_PROGRESS to CHECKING.

**Assumptions, limitations, and expressed caveats.** The epistemic labeling framework (Chapter 5) ensures that assumptions are structurally visible — not buried in prose — at the point of review. Every non-trivial claim is classified as FACT (directly observed in source with citation), ASSUMPTION (reasonable inference requiring validation), PROPOSAL (agent suggestion requiring human decision), or TBD (unknown, requiring resolution). The licensed professional reviewing a deliverable can directly identify which claims are grounded and which require validation, without needing to infer epistemic status from context. Epistemic labels are defined in `docs/TYPES.md` §10 and enforced by K-PROV-1 and K-INVENT-1 (`docs/CONTRACT.md` §1.9).

**Suitability for intended purpose and compliance with local conditions.** Suitability and local compliance are confirmed through the Gate 2 checklist, which derives review items from the deliverable's specifications, decomposition records, and declared dependencies. The licensed professional confirms checklist completeness at Gate 2 before the substantive review proceeds.

**Health, safety, and environmental implications.** HSE findings are classified as CRITICAL severity in the review protocol. CRITICAL findings must be resolved — not merely deferred — before a deliverable may advance to CHECKING status. The hierarchy of authority (`docs/DIRECTIVE.md` §3.4; `PROFESSIONAL_ENGINEERING.md` §3.5) places laws and regulations, including HSE requirements, as the first constraint, overriding all other considerations.

**Integrity and validity of all work products, including cross-deliverable consistency.** The RECONCILIATION agent performs cross-deliverable coherence analysis across the project dependency graph. Dependency registers (`Dependencies.csv`) are authoritative, deliverable-local records that capture all inter-deliverable relationships with provenance (K-DEP-1, K-DEP-2, `docs/CONTRACT.md` §1.4).

**Applicable tasks related to the work (calculations, analyses, evaluations, interpretations).** Task-level agent outputs are captured in immutable snapshot folders with structured run summaries (`RUN_SUMMARY.md`, `QA_Report.md`), forming the traceable evidence base for the review (K-SNAP-1, `docs/CONTRACT.md` §1.10; `docs/SPEC.md` §11).

**Applicable materials and methods of construction, inspection, maintenance, or operation.** Materials and methods are documented within deliverable document kits (Datasheet, Specification, Guidance, Procedure). The structured format ensures that all relevant technical content is documented and traceable (`docs/SPEC.md` §2).

**Relevancy and accuracy of the applicable tools used in PWP preparation, including software, hardware, firmware, applications, and other technologies.** This requirement is particularly significant for AI-assisted work. APEGA §3.1.2.1 explicitly names software, hardware, firmware, applications, and other technologies as tools subject to thorough review. The Chirality professional practice standard interprets this as requiring the licensed professional to understand what each agent is instructed to do, what its outputs represent (drafts requiring verification, not authoritative conclusions), how to verify agent outputs against source materials and engineering judgment, and the failure modes of LLM-based systems — specifically hallucination, omission, and plausible-sounding error (`PROFESSIONAL_ENGINEERING.md` §3.3). The deterministic/probabilistic boundary (§6.7) further addresses tool accuracy by ensuring that tasks admitting algorithmic validation are implemented as validated deterministic tools rather than left to LLM probabilistic reasoning.

**Interdisciplinary reviews where the work crosses discipline boundaries.** Interdisciplinary review obligations are surfaced through the Gate 2 checklist when cross-discipline dependencies are declared in the deliverable's `_DEPENDENCIES.md`. The RECONCILIATION agent identifies interface conflicts across discipline boundaries (`docs/CONTRACT.md` §1.4, K-DEP-1).

### 6.5.3 Adherence to Regulatory Requirements (APEGA §3.1.2.2)

APEGA §3.1.2.2 requires that thorough review verify compliance with the EGP Act, the General Regulation, applicable APEGA practice standards, and any contractual requirements for regulatory approvals or permits. The Chirality architecture satisfies this requirement through the hierarchy of authority, which places laws and regulations as the first constraint binding on both agents and professionals. Agents cannot override applicable legislation — this is enforced through agent instruction invariants. Project-specific regulatory requirements are captured in `_CONTEXT.md` and `_REFERENCES.md` and appear as mandatory Gate 2 checklist items.

### 6.5.4 Adherence to Quality Control and Assurance (APEGA §3.1.2.3)

APEGA §3.1.2.3 requires that thorough review verify compliance with QC/QA processes defined in the PPMP and confirm that deliverables are clear, readable, consistent, and complete. The QC/QA architecture is addressed in §6.7. Clarity and completeness are structural properties enforced through the document kit format, required metadata files, and the Gate 2 review checklist. Epistemic labeling ensures that all assumptions and TBD items are conspicuously identified rather than hidden in prose.

### 6.5.5 Authentication

Authentication of a PWP is the act by which a licensed professional represents that they have satisfied the direct supervision and control standard or the thorough review standard, and accepts professional responsibility for the work. The Chirality architecture implements authentication as a controlled gate — the final and irreversible human action in the deliverable lifecycle.

Authentication binds to a specific git SHA. This means that a licensed professional's seal and signature apply to a precisely identified version of the work. Content change after authentication voids the authentication (K-AUTH-2, `docs/CONTRACT.md` §1.2). A deliverable is considered dirty — requiring renewed review before any reliance — if any governed input has changed since its last approved SHA (K-VAL-1, `docs/CONTRACT.md` §1.6). Merge to the main branch is permitted only when branch HEAD equals the approved SHA (K-MERGE-1, `docs/CONTRACT.md` §1.8).

The content-addressed authentication mechanism is a significant architectural contribution to professional practice governance. Traditional professional authentication — seal and signature on a paper or PDF document — binds the professional's approval to a specific physical artifact, but provides limited assurance that the artifact being approved is identical to the artifact being relied upon, particularly after transmittal or electronic distribution. SHA-based authentication provides a mechanically verifiable binding: any change to the authenticated content is detectable, and the integrity of the approval relationship does not depend on process discipline or trust. [CITE: content-addressed integrity in software engineering; merkle trees and commit hashing]

---

## 6.6 Professional Obligations

The preceding sections address how the architecture satisfies the APEGA obligations that govern the professional's use of AI agents. This section addresses the professional obligations that the architecture enforces as invariant: obligations that cannot be delegated, modified, or bypassed by any agent or process, regardless of circumstances.

### 6.6.1 Public Welfare as First Constraint

The protection of the public, property, and the environment is the overriding obligation in professional engineering. The hierarchy of authority places laws and regulations — including safety regulations — as the first constraint binding on technical decisions. When tradeoffs exist between public safety and commercial pressure, schedule, or convenience, safety prevails. This obligation is non-delegable to AI systems (`PROFESSIONAL_ENGINEERING.md` §3.1; `docs/DIRECTIVE.md` §2 — Axiology).

The architecture enforces this obligation through the CRITICAL severity classification in the REVIEW agent protocol. A finding classified as CRITICAL must be resolved — not deferred — before a deliverable may advance. HSE implications are identified in APEGA §3.1.2.1 as a mandatory review item, and the review protocol ensures they are addressed with the most stringent transition criteria. No agent may bypass this requirement.

### 6.6.2 Responsible Charge Remains Human

Professional liability is personal and non-transferable. Invariant K-AUTH-1 (`docs/CONTRACT.md` §1.2) states: "Only humans author binding approval records. No agent may claim to certify, approve, sign, seal, or issue work for reliance." This is not a policy recommendation — it is an architectural invariant enforced through agent instruction constraints and the gate-controlled workflow.

The licensed professional retains decision rights for scope and boundary decisions, selection of governing codes and standards, hazard and risk acceptance including residual risk statements, conflict adjudication where engineering judgment is required, and approval, issuance, signature, seal, and transmittal for reliance (`PROFESSIONAL_ENGINEERING.md` §3.2; `docs/DIRECTIVE.md` §3.2). These are not merely functions that the architecture routes to humans — they are functions that agents are positively prohibited from performing or claiming to perform.

This prohibition is constitutive of what a professional work product is in the Chirality framework. An agent-produced deliverable in the IN_PROGRESS state is not a PWP; it is a draft. It becomes a PWP only when a licensed professional, having satisfied either the direct supervision and control standard or the thorough review standard, authenticates it under their seal and signature. The architecture makes it structurally impossible to skip this step.

### 6.6.3 Competence Includes Tool Competence

A licensed professional must not use an AI agent to perform work that the professional is not competent to verify manually. Using AI to produce work that the professional cannot adequately review is a competence failure under the EGP Act — not merely a process failure (`PROFESSIONAL_ENGINEERING.md` §3.3; `docs/DIRECTIVE.md` §3.3). [CITE: professional competence and tool use in engineering regulation]

The APEGA requirement that professionals review the "relevancy and accuracy of applicable tools used in the PWPs preparation" (§3.1.2.1) implies a specific competence requirement for AI-assisted practice: the licensed professional must understand the agent instruction architecture sufficiently to know what an agent is constrained to do and what it is not; must be able to detect LLM failure modes — hallucination, omission, plausible-sounding error, silent conflict resolution — in agent outputs; and must be able to exercise independent engineering judgment when AI outputs conflict with professional experience.

The architecture supports this obligation through epistemic labeling, mandatory provenance, and conflict surfacing (Chapter 5), which make the epistemological status of agent claims transparent and therefore verifiable by a competent professional. However, the architecture cannot substitute for competence — it can only make the evidence available for a competent professional to evaluate. The professional's competence obligation is irreducible.

### 6.6.4 Evidence Over Plausibility

The firm's practice requires that engineering decisions be based on evidence, not plausibility. This is enforced through three invariants: K-PROV-1 (mandatory provenance for every extracted claim, `docs/CONTRACT.md` §1.9), K-INVENT-1 (unknown values become TBD, not guessed, `docs/CONTRACT.md` §1.9), and K-CONFLICT-1 (conflicts between sources must be surfaced, not silently resolved, `docs/CONTRACT.md` §1.9). Together, these invariants ensure that an agent cannot substitute apparent confidence for documented evidence.

The epistemic architecture described in Chapter 5 is the primary implementation of this principle. Its regulatory significance is that it makes thorough review tractable: because the evidence trail is the workflow, not a byproduct of it, the professional reviewing an agent-produced deliverable has direct access to the evidence basis for every claim, the identity of every assumption, and the location of every unresolved conflict.

### 6.6.5 Hierarchy of Authority

In technical matters, agents and professionals follow the hierarchy of authority defined in `docs/DIRECTIVE.md` §3.4 and `PROFESSIONAL_ENGINEERING.md` §3.5: (1) laws and regulations; (2) codes and standards; (3) project specifications and design basis (approved for use); (4) verified engineering analysis and published literature; (5) professional judgment. Agent outputs carry no professional authority — they are decision support unless explicitly accepted and issued by a licensed professional. The hierarchy is enforced through agent instruction invariants that prohibit agents from overriding codes, standards, or project specifications.

---

## 6.7 Quality Control and Assurance

### 6.7.1 Architectural Controls

The firm's QC/QA framework for AI-assisted work is implemented through the agent instruction architecture (`PROFESSIONAL_ENGINEERING.md` §6.1). This is a significant architectural choice: quality control is not a separate process overlay imposed on agent outputs but an integral property of the architecture that governs agent behavior. Six governance documents constitute the QC/QA framework:

| Document | QC/QA Function |
|----------|----------------|
| `docs/DIRECTIVE.md` | Founding constraints: filesystem-as-state, human authority, evidence-first, no hidden memory |
| `docs/CONTRACT.md` | 20 binding invariants (K-*) with four-layer enforcement map |
| `docs/SPEC.md` | Physical structures, file formats, schema validation |
| `docs/TYPES.md` | Controlled vocabulary, enumerated types, lifecycle state machine |
| `agents/AGENT_HELPS_HUMANS.md` | Workflow design requirements (R1–R9) binding on all agents |
| `agents/AGENT_DECOMP_BASE.md` | Decomposition invariants (I1–I10) binding on all decomposition agents |

The three-layer invariant system — R1–R9 workflow requirements, I1–I10 decomposition invariants, and 20 K-* system-wide invariants — and its four-layer enforcement map are described in Chapter 4. The significance for QC/QA purposes is that compliance is verified at multiple independent levels: at compile time through agent instruction constraints, at runtime through orchestrator enforcement, at human gates through professional review, and through automated tooling for specific invariants (K-STALE-1, K-VAL-1, K-MERGE-1, K-AUTH-2, K-DEP-2). No single point of failure can disable the entire control system.

### 6.7.2 Instruction Governance as Release Engineering

Agent instruction files are part of the firm's controlled quality system. They are treated as controlled documents under a release engineering discipline: versioned in git, reviewed before release, subject to no silent behavior changes, with material changes to write scope, tool access, or agent outputs requiring a recorded release note (`PROFESSIONAL_ENGINEERING.md` §6.2). Conformance of all agent instruction files against the canonical standard is verified by AUDIT_AGENTS; structural requirements for instruction files are defined in `docs/SPEC.md` §9.

This approach addresses a quality risk specific to AI-assisted practice: the risk that changes to agent behavior go undetected and affect the quality of work products without the professional's awareness. By treating agent instruction files as controlled documents subject to formal release engineering, the firm ensures that material behavior changes are visible, reviewed, and documented — and that the professional is informed of changes that may affect the validity of prior review or supervision work.

### 6.7.3 The Deterministic and Probabilistic Boundary

A central QC/QA mechanism is the enforced boundary between deterministic operations and probabilistic (LLM-based) operations (`PROFESSIONAL_ENGINEERING.md` §6.3). If a task can be validated by a schema or algorithm — file format validation, structural completeness checking, ID resolution, SHA comparison — it is implemented as a deterministic tool, not left to LLM reasoning. LLM-based agents are reserved for work that genuinely requires inference under uncertainty: interpreting ambiguous text, proposing decompositions, reconciling tradeoffs, drafting content.

This boundary is significant for professional practice for two reasons. First, it limits the domain of probabilistic outputs that require thorough review — the professional can rely on deterministic tool outputs without the same level of scrutiny that LLM-based outputs require. Second, it prevents LLM reasoning from being applied to tasks where deterministic validation is available, reducing the risk that a plausible but incorrect LLM output substitutes for a verifiably correct deterministic result. The tool registry (`tools/REGISTRY.md`) indexes all deterministic tools.

### 6.7.4 Technology Provider Due Diligence

The firm uses LLMs provided by technology vendors as the cognitive engine within the agent system. As established in §6.3.3, the technology provider is not providing professional services. The firm's licensed professionals bear full responsibility for all work produced using the technology. Consistent with the APEGA §3.1.2.1 requirement to review the relevancy and accuracy of tools used in PWP preparation, the firm's due diligence on LLM technology includes:

- Evaluation of model capabilities and limitations for the professional services the firm provides
- Assessment of model safety practices, alignment research, and responsible deployment policies
- Testing of agent behavior within the firm's instruction architecture before adopting model updates
- Documented assessment of material model changes and their impact on agent behavior

Critically, the firm does not rely solely on the technology provider's safety measures. The agent instruction architecture constrains and governs LLM behavior independent of the provider's controls: R1–R9 workflow requirements, 20 K-* system invariants, write scope quarantine, and deterministic tool validation. This independence is essential: the professional's obligation is to exercise due diligence on the tools used in PWP preparation, and that obligation cannot be satisfied by deferring to the vendor's quality assurance practices.

### 6.7.5 Evidence and Auditability

The firm's evidence and auditability framework (`PROFESSIONAL_ENGINEERING.md` §6.5) rests on five architectural mechanisms addressed in Chapter 5 (Epistemic Architecture) and revisited here for their QC/QA significance:

- **Filesystem as state.** All project truth lives in git-tracked plain files. There is no external database or hidden state. If a decision is not in a versioned file, it does not exist for purposes of reliance.
- **Git as development record.** Version control provides meaningful diffs for review, reproducibility, rollback, and audits that do not depend on vendor systems or transient context.
- **Immutable snapshots.** Task agent analysis outputs are written to timestamped, append-only snapshot folders. The snapshot trail is the audit trail, enforced by K-SNAP-1 (`docs/CONTRACT.md` §1.10).
- **Provenance tracking.** Every extracted claim cites its source file and section reference, or carries an explicit `location TBD` marker, enforced by K-PROV-1 (`docs/CONTRACT.md` §1.9).
- **Epistemic labeling.** All claims are labeled — FACT, ASSUMPTION, PROPOSAL, or TBD — ensuring that the professional does not need to infer epistemic status from context.

The evidentiary completeness of this trail is the foundation on which the claim that "the architecture IS the compliance mechanism" rests. A regulator, auditor, or reviewing professional can, at any point in or after the project, inspect the git history to identify every agent output, every human decision, every gate transition, and every version of every deliverable. This is not a retrospective documentation exercise — it is the normal operational record of every project conducted under the architecture.

---

## 6.8 The Human-AI Contract

The Chirality architecture encodes a contract between licensed professionals and AI agents that is not merely described in policy documents but enforced by the architecture itself (`PROFESSIONAL_ENGINEERING.md` §9). This section articulates the contract and traces each element to its governing invariant or mechanism.

### 6.8.1 Human Responsibilities

Licensed professionals operating under the Chirality framework bear the following responsibilities:

- **Define intent, scope, and acceptance criteria.** The professional defines what the work is, what standards it must meet, and what conditions must be satisfied for the work to be acceptable. Agents cannot define their own scope.
- **Choose codes, standards, and key assumptions.** Selection of governing codes, standards, and design basis is a human decision right (K-AUTH-1; `docs/DIRECTIVE.md` §3.2).
- **Decide what "done" means.** The professional defines the completion criteria for each deliverable and makes the final determination of whether a deliverable is ready for issuance.
- **Approve changes that affect deliverables.** Change impacts are assessed through the CHANGE agent, but approval of changes affecting issued or checked deliverables is a human decision. Staleness propagation (K-STALE-1) and stale triage (K-STALE-2) ensure that the human is presented with all downstream implications before approval.
- **Perform or commission independent review where required.** For work of sufficient consequence, independent review beyond the REVIEW agent protocol may be required. This is a professional judgment call that the architecture supports but cannot make.
- **Accept residual risk.** Residual risk statements — for hazards that have been identified but cannot be fully mitigated — are a human responsibility that no agent may assume.
- **Authenticate PWPs for reliance.** Authentication is the exclusive human act that creates a PWP from an agent-assisted draft (K-AUTH-1, K-AUTH-2).

### 6.8.2 AI Agent Permitted Actions

Within the constraints of their instruction files, AI agents may:

- Draft and format deliverables under explicit templates
- Extract, normalize, cross-reference, and summarize evidence from source documents
- Generate candidate alternatives and tradeoff tables for professional consideration
- Surface gaps, inconsistencies, and interface conflicts for human resolution
- Run bounded, checkable transformations with deterministic validators
- Maintain structured records: dependency registers, status files, working memory

The common thread is that agents prepare information and structure for professional decision-making — they do not make decisions. Agents widen the field of consideration; professionals narrow, accept, and issue.

### 6.8.3 AI Agent Prohibitions

AI agents operating under the Chirality framework are positively prohibited from the following actions. Each prohibition is traced to its governing invariant:

| Prohibited Action | Governing Invariant |
|---|---|
| Claim to certify, approve, sign, seal, or issue work for reliance | K-AUTH-1 (`docs/CONTRACT.md` §1.2) |
| Silently resolve conflicts between sources | K-CONFLICT-1 (`docs/CONTRACT.md` §1.9) |
| Invent scope items, parameters, or engineering content; unknowns become TBD | K-INVENT-1 (`docs/CONTRACT.md` §1.9) |
| Write outside declared write scope | K-WRITE-1 (`docs/CONTRACT.md` §1.10) |
| Maintain hidden state that diverges from the filesystem | `docs/DIRECTIVE.md` §2.5 (No Hidden Memory) |
| Bypass human gates or autonomously advance workflow stages | K-GATE-1 (`docs/CONTRACT.md` §1.7); K-SEAL-1 (`docs/CONTRACT.md` §1.3) |

The architecture does not merely recommend that agents avoid these actions — it enforces the prohibitions through the invariant contract system, the orchestrator, and the write scope constraints. An agent that attempts to authenticate work violates K-AUTH-1 at the agent instruction level; an agent that writes outside its declared scope violates K-WRITE-1 at the orchestration level. The enforcement map in `docs/CONTRACT.md` §2 identifies the specific enforcement point for each invariant.

This catalogue of prohibitions is the architectural expression of the professional practice principle that AI outputs are drafts and structured assistance, not authoritative engineering judgment. Professional acceptance — through either direct supervision and control or thorough review, followed by authentication — is what makes agent-produced outputs into professional work products.

---

## 6.9 Limitations of the Regulatory Mapping

The analysis presented in this chapter is honest about what it claims and what it does not. This section identifies the substantive limitations of the regulatory mapping.

### 6.9.1 The Mapping Is an Interpretation, Not a Regulatory Ruling

[RATIONALE: The following limitation is acknowledged explicitly because the regulatory analysis in this chapter represents the firm's interpretation of existing APEGA standards, not a determination by APEGA itself.]

The APEGA mapping presented in this chapter and in Appendix C represents an interpretation — by the firm and the author — of how existing practice standards apply to AI-assisted professional practice. APEGA has not issued specific guidance on AI agents, LLM-based systems, or the application of the *Relying on the Work of Others* standard to AI-assisted work. There is no regulatory ruling that validates or endorses the interpretation offered here.

The interpretation is grounded in the regulatory text — the obligations of APEGA §3.1 are specified in terms of professional conduct, not worker nature — and the analysis is presented as a structured logical argument from regulatory premises. However, a regulatory body, a reviewing court, or a professional discipline tribunal might interpret the same provisions differently. In particular, APEGA might conclude that the "others" in §3.0 contemplates natural persons capable of bearing professional responsibility, and that AI agents are better classified as tools than as workers, with correspondingly different professional obligations.

If APEGA were to adopt this alternative interpretation, the Chirality architecture would still satisfy the professional's obligations — the architecture's controls on agent outputs are more rigorous than what typical tool use requires — but the specific regulatory mapping presented here would need revision. The substantive practice protections would remain; only the regulatory framing would change.

### 6.9.2 Jurisdiction Specificity

The regulatory analysis in this chapter is specific to Alberta, under the EGP Act and APEGA practice standards. The legal and regulatory framework governing professional engineering varies significantly across Canadian provinces, across national jurisdictions, and between engineering and other regulated professions. [COMPARE: Engineers Canada pan-Canadian guidelines on AI] [COMPARE: NSPE Code of Ethics and emerging AI guidance (United States)] [COMPARE: ICE and Engineering Council AI guidance (United Kingdom)] [COMPARE: ISO/IEC standards on AI system management and its relationship to professional practice]

The structural argument — that the obligations of a professional who relies on the work of others are defined by what the professional must do, not by what the worker must be — is likely to generalize across regulatory regimes that share the same functional structure. The specific mechanism mapping, however, depends on the precise language of the applicable standards in each jurisdiction. Practitioners in other jurisdictions should conduct their own mapping analysis rather than assuming that the APEGA analysis transfers without modification.

### 6.9.3 The "Relying on the Work of Others" and "Using a Tool" Distinction

The firm's interpretation resolves the distinction between "relying on the work of others" and "using a tool" conservatively: AI agents are treated as "others" whose work the professional relies on, triggering the full rigour of APEGA §3.1. As noted in §6.3.2, this is a judgment call. The regulatory text does not explicitly resolve it.

A reasonable contrary argument holds that the "tool" classification is more appropriate, particularly for narrowly scoped AI agents performing tasks with limited discretion — for example, extracting structured data from a document according to an explicit schema. The "others" classification may be most appropriate for AI agents performing tasks that involve genuine inference: interpreting ambiguous requirements, proposing design decompositions, surfacing and characterizing conflicts.

The firm's conservative choice to apply the "others" classification across the board has a practical consequence: the professional is required to satisfy the full supervision and review requirements of §3.1 for all AI agent outputs, including those that might arguably qualify as tool outputs. This is protective from a professional responsibility standpoint — it errs on the side of more rigorous oversight — but it places a heavier documentation burden on the professional than a "tool" classification would. Practitioners who wish to argue for a more graduated approach — applying the "others" standards to high-discretion agent work and a lighter tool-use standard to low-discretion agent tasks — would need to develop that argument in consultation with their regulatory body.

### 6.9.4 The Architecture Is Necessary but Not Sufficient

The Chirality architecture establishes the conditions under which thorough review is tractable and direct supervision is verifiable. It is a necessary condition for professional reliance on AI agent outputs, but not a sufficient one. The sufficiency condition is the licensed professional's competent exercise of judgment at every gate. An architecture that makes evidence available cannot guarantee that the professional uses it well. A professional who treats gates as boxes to check, reviews epistemic labels without engaging their content, or authenticates work they cannot adequately evaluate violates the professional obligations this chapter describes — regardless of what the architecture provides.

This limitation is structural, not correctable by further architectural development. The APEGA framework places the accountability burden on the licensed professional precisely because professional judgment cannot be mechanized. The architecture can structure the professional's task, surface the evidence, eliminate hidden information, and prevent unauthorized actions — but it cannot exercise the professional's judgment on the professional's behalf.

### 6.9.5 Evolving Regulatory Context

The regulatory context for AI in professional practice is evolving rapidly. APEGA and other engineering regulatory bodies are actively considering how to address AI tools in their practice standards and guidelines. [CITE: APEGA's ongoing practice standards review process] [CITE: Engineers Canada work on AI governance for professional practice] The specific interpretations offered in this chapter reflect the regulatory environment as of the writing date (2026-03-29) and may require updating as formal regulatory guidance is issued.

The structural argument presented in §6.3 — that existing obligations apply to AI agents because the obligations are defined by professional conduct, not worker nature — may prove more durable than the specific mapping, because it rests on the logic of the existing regulatory text rather than on interpretations that may be superseded. However, the overall regulatory analysis should be treated as a living document subject to revision as the regulatory context develops.

---

## 6.10 Summary

This chapter has established that the Chirality architecture provides a framework within which a licensed professional engineer in Alberta can direct AI agents while satisfying professional obligations under the EGP Act and APEGA practice standards. The argument rests on four related claims.

First, the thesis argues that the APEGA practice standard *Relying on the Work of Others and Outsourcing* can be interpreted to apply directly — rather than merely by analogy — to AI-assisted professional practice, because AI agents are "others" within the meaning of §3.0 and the obligations that standard imposes are defined by what the licensed professional must do, not by the nature of the entity that prepared the work.

Second, the Chirality architecture provides a strong candidate mechanism for satisfying the direct supervision and control standard (APEGA §3.1.1) through its gate-controlled orchestration model, its three-type agent hierarchy with non-overridable authority boundaries, its structured documentation of agent scope and duties, its interactive session model for ongoing communication, its structured record-keeping in versioned files, and its git-based audit trail. The full compliance trace is in Appendix C, Table C.1.

Third, the architecture provides a strong candidate mechanism for satisfying the thorough review standard (APEGA §3.1.2) through the REVIEW agent's 5-gate protocol, the epistemic labeling framework that makes assumptions structurally visible for review, the content-addressed authentication binding (K-AUTH-2, K-VAL-1, K-MERGE-1), and the provenance and conflict-surfacing mechanisms that make the evidence basis for every claim transparent and verifiable.

Fourth, the professional obligations that remain invariantly human — public welfare as first constraint, responsible charge, competence, evidence over plausibility, hierarchy of authority — are enforced as architectural invariants, not merely recommended in policy. K-AUTH-1 prohibits any agent from authenticating work. K-INVENT-1 prohibits invention. K-CONFLICT-1 prohibits silent conflict resolution. These prohibitions are the architectural expression of the principle that professional responsibility cannot be delegated to an AI system.

The central contribution of this analysis to the thesis is the argument that the Chirality architecture is not merely consistent with existing regulatory requirements but can serve as a compliance mechanism. The architecture does not add professional compliance obligations to an otherwise unconstrained AI system; rather, it attempts to encode the structure of direct supervision and control, the infrastructure of thorough review, and the enforcement of professional prohibitions as properties of the system itself.

The limitations identified in §6.9 are genuine. The mapping is an interpretation, not a ruling; the jurisdiction is Alberta; the firm has resolved the tool-versus-worker classification conservatively; and the architecture is necessary but not sufficient — only competent professional judgment exercised at every gate can fully satisfy the obligations the regulatory framework imposes. These limitations do not undermine the central argument; they define its scope.

Together, Chapters 3 through 6 establish the philosophical, architectural, epistemic, and regulatory foundations of the thesis claim: that the Chirality architecture is one rigorous and professionally grounded way for a licensed professional to direct AI agents under the existing APEGA regulatory framework, without requiring new AI-specific regulation, because the architecture is designed around the obligations that framework imposes. It is a defensible answer to the research question, not the only conceivable one.

---

*Chapter 7 examines the Chirality architecture through a systems engineering design analysis lens, assessing the degree to which it satisfies formal systems engineering design principles and identifying the engineering tradeoffs embedded in its major design decisions.*
