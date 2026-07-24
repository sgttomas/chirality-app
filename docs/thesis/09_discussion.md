# Chapter 9 — Discussion

---

## 9.1 Introduction

The preceding chapters presented a philosophical framework, a technical architecture, an epistemic transparency system, a regulatory mapping, a systems engineering analysis, and a working implementation. This chapter assesses the contributions honestly: what was demonstrated, what was not, what the limitations are, how the work generalizes, and what remains for future investigation.

---

## 9.2 Limitations

### 9.2.1 No Controlled Empirical Validation

The most significant limitation of this work is that the Chirality architecture has not been validated through a controlled empirical study with practicing engineers. The thesis demonstrates that the architecture satisfies the structural requirements of APEGA's professional practice standards, and that it has been implemented as working software with an indexed agent suite and a registered deterministic toolset. However, it does not present empirical evidence that:

- Licensed professionals find the epistemic labeling and provenance mechanisms effective for thorough review in practice
- The review time for AI-assisted work products is measurably reduced compared to unstructured AI outputs
- The invariant system prevents the categories of failure it is designed to prevent (hallucination propagation, silent conflict resolution, scope creep beyond declared write zones) at rates that are statistically significant
- The gate-controlled workflow model is accepted by practitioners as a workable balance between control and productivity

An empirical validation would require a controlled study in which licensed engineers review AI-assisted deliverables — some produced under the Chirality governance framework, some without it — and the accuracy, completeness, and efficiency of their review is measured. Such a study is a natural next step but is beyond the scope of this thesis.

### 9.2.2 Regulatory Interpretation, Not Endorsement

The mapping of the Chirality architecture to APEGA §3.1.1 (direct supervision and control) and §3.1.2 (thorough review) presented in Chapter 6 is a regulatory interpretation by the firm, not a ruling by APEGA. APEGA's guidance on AI tools ("Guidance for Registrants Regarding the Use of Artificial Intelligence Tools," first published July 2025; updated March 23, 2026) addresses registrant conduct — professional responsibility, due-diligence verification of AI results, and competence as a precondition of use — and does not address system architecture or the application of the *Relying on the Work of Others* standard to AI agents. The interpretation — that AI agents are "others" whose work the professional relies on, and that the professional's obligations are defined by what the professional must do rather than by the nature of the worker — is a defensible and conservative reading, but it has not been tested in a disciplinary proceeding or judicial review.

Other interpretations are possible. A regulator might argue that AI agent outputs are not "work prepared by others" but rather "outputs of a tool," which would shift the regulatory framing from §3.0 (Relying on the Work of Others) to the more general obligation to verify tool accuracy under §3.1.2.1. APEGA's AI guidance in fact leans toward this framing: it directs registrants to treat AI results "no differently than results from software, calculators, or lookup tables." The firm's "others" classification is deliberately the more demanding posture — it satisfies the guidance's due-diligence obligations and adds the full supervision-and-review structure on top. The Chirality architecture would satisfy the tool-verification obligation as well, but the conceptual framing would differ. The firm has chosen the "others" interpretation because it is more conservative — it imposes the full suite of supervision and review obligations, not just tool verification — and because the nature of LLM-based agents (judgment-like behavior, natural language interaction, content generation) is structurally more analogous to work prepared by a person than to output from a deterministic calculation tool.

### 9.2.3 Jurisdiction-Specific Regulatory Framework

The regulatory mapping in Chapter 6 is specific to Alberta (APEGA) and the *Engineering and Geoscience Professions Act*. While the structural argument — that professional obligations are defined in terms of what the professional must do, not what the worker is — should generalize to any jurisdiction that defines professional responsibility through supervision and review, the specific practice standards cited (`Relying on the Work of Others and Outsourcing`, `Authenticating Professional Work Products`) are APEGA instruments. Other jurisdictions have their own regulatory frameworks (Chapter 2, §2.4), and the mapping would need to be re-established for each.

### 9.2.4 Instruction-Level Enforcement

The invariant system (R1–R17, I1–I10, K-*) is enforced primarily through agent instruction text and deterministic tools, not through a verified runtime enforcement engine. The enforcement map in `CONTRACT.md` §2 distributes enforcement across layers: agent instructions (design-time), deterministic runtime checks (the TASK shell's path containment, K-WRITE-2), ORCHESTRATOR (runtime), the DOMAIN_ENGINE profile layer, human review (gate), governance audits, and future tooling (automated). The "agent instructions" layer depends on the LLM following its instruction text — a soft constraint, not a hard one.

This is an honest limitation. An LLM may deviate from its instructions. The architectural response is defense in depth: agent instructions are the first layer, but write scope quarantine limits the blast radius of any deviation, human gates catch deviations before they reach authenticated status, and audit agents (AUDIT_AGENTS, AUDIT_DECOMP, AUDIT_DEP_CLOSURE) detect non-conformance after the fact. The system does not claim that instruction-level enforcement is sufficient alone. It claims that the multi-layer enforcement model contains failures to manageable scope.

The "future tooling" enforcement layer — automated checks for staleness calculation (K-STALE-1), content validation (K-VAL-1), merge policy (K-MERGE-1), and approval integrity (K-AUTH-2) — is specified but not yet fully implemented. This means that some invariants currently depend on human review discipline rather than automated enforcement.

### 9.2.5 LLM Capability Evolution

The architecture is designed for the current generation of large language models and their known limitations (hallucination, lack of intrinsic epistemic warrant, inconsistent instruction following). As model capabilities evolve, some architectural constraints may become more or less relevant:

- If future models achieve reliable provenance tracking natively, the mandatory provenance invariant (K-PROV-1) would become redundant as an architectural enforcement but would remain valuable as a verification check.
- If future models achieve near-zero hallucination rates, the no-invention rule (K-INVENT-1) and epistemic labeling would become less operationally important but would not become incorrect — the architecture would simply flag fewer items.
- If future models reliably follow instructions, the instruction-level enforcement layer would become more trustworthy, but the defense-in-depth model (human gates, audit agents, write quarantine) would remain necessary for professional practice because the stakes of failure are not reduced by lower probability alone.

The architecture's longevity depends on the invariant structure remaining
valid regardless of model capability. The thesis claims that the invariants
express professional obligations—not model limitations—and therefore remain
relevant even as models improve. Better models may produce fewer TBDs and
ASSUMPTION labels; the architecture still requires detected uncertainty to be
represented within its declared coverage.

---

## 9.3 Generalizability

### 9.3.1 Across Engineering Domains

The architectural patterns — write quarantine, epistemic labeling, gate-controlled workflows, invariant contracts — are domain-independent. The thesis demonstrates them in the context of EPC and design-build engineering, but the same patterns could govern AI agents producing:

- Regulatory compliance documentation
- Medical device design history files
- Environmental impact assessments
- Financial audit working papers
- Legal contract review deliverables

Any domain where a qualified professional must take responsibility for work and where the evidence trail must support that responsibility is a potential application domain. The four-pillar framework (ontology, epistemology, praxiology, axiology) provides a checklist for assessing whether a given domain's governance needs are fully addressed.

### 9.3.2 Across Regulatory Jurisdictions

The APEGA regulatory mapping generalizes in structure if not in specific citations. The argument — that existing "relying on the work of others" frameworks can govern AI agent use without new AI-specific regulation — should apply wherever professional regulation defines supervision and review obligations in terms of what the professional does. Chapter 2, §2.4 surveyed regulatory approaches in British Columbia (EGBC), Ontario (PEO), the United States (NSPE, ASCE), Australia, and the United Kingdom, finding that none had yet mapped AI agent governance to existing "relying on others" frameworks. The Chirality mapping may serve as a reference for other jurisdictions.

### 9.3.3 The Four-Pillar Framework as an Evaluation Lens

The ontology/epistemology/praxiology/axiology framework could serve as an evaluation instrument for other AI agent governance architectures. For any system, one could ask: Does it define a complete ontology? Does it enforce epistemic transparency? Does it bound agent praxis through formal constraints? Does it articulate and enforce values? A system missing any pillar has a specific, identifiable governance gap. This evaluation use extends beyond the Chirality architecture itself.

The deeper insight — that the four pillars provide a compact and useful ontology for professional accountability (Chapter 3, §3.5) — suggests that this evaluation framework is not arbitrary. It is plausibly portable wherever a professional takes responsibility for work, because the four questions (what exists? what is warranted? how was it done? what values governed?) recur across accountable practice even if different domains instantiate them differently.

The lens is deliberately non-exhaustive. It tests whether four recurring
accountability questions have been addressed; it does not constrain every
category through which a situated knower may understand the work.

### 9.3.4 The Epistemic Ontology and Warrant Lifecycle as Portable Concepts

The six epistemic primitives (claim, warrant, status, gap, conflict, ruling) and the warrant lifecycle (UNWARRANTED → CITED → REVIEWED → AUTHENTICATED) are not Chirality-specific constructs. They formalize concepts that are implicit in any professional review process. An engineer reviewing a colleague's calculation already thinks in terms of claims (what is asserted), warrants (what evidence supports it), gaps (what is missing), and conflicts (where sources disagree). The Chirality contribution is to make these implicit concepts architecturally explicit and enforceable.

Any AI agent framework that aims to support professional practice could adopt the epistemic ontology without adopting the full Chirality architecture. The primitives and the warrant lifecycle are modular — they require only that the system can attach provenance to claims, label epistemic status, surface gaps, and detect conflicts. The AUDIT_EPISTEMIC agent (`AGENT_AUDIT_EPISTEMIC.md`) demonstrates that these properties can be audited systematically.

This portability concerns information governance, not a portable definition
of knowledge. The primitives expose claims, grounds, and workflow status so
that knowers can assess them and accountable actors can record reliance.

### 9.3.5 Capability-Invariance of the Authority Boundary

*Subsection added 2026-07-01.*

The preceding subsections argued that the architecture generalizes across domains and jurisdictions. A third axis of generalization deserves explicit statement: the architecture generalizes across model capability, because the authority boundary is indexed to accountability-status, not to capability. Nothing in the invariant catalog (Appendix A) conditions on how capable a model is. Write scopes attach to roles — the Agent 0/1/2 runtime hierarchy of Chapter 4 (§4.5) — gates attach to positions in the deliverable lifecycle (`SPEC.md` §3.3), and the REVIEWED → AUTHENTICATED transition attaches to being a continuant who can be held to account, a status that no capability level confers. No capability level crosses the boundary, and no capability level renegotiates it. This distinguishes the architecture from capability-indexed governance regimes — autonomy levels, evaluation-gated permission sets, trust tiers — which must be re-litigated at every model generation and which convert each capability gain into a fresh governance argument. The invariance holds in both directions: a degraded or cheaper model requires no amendment either — the gates and the evidence trail simply catch more. The seeds of this argument are already present in the corpus: the authority typing of Chapter 4 asks what a role may write, never how capable the agent is, and the reliance standard mapped in Chapter 6 (§6.3) never conditions the professional's obligations on the competence of the relied-upon party.

A monotonic-benefit implication follows. Because the gates were never
justified by machine incapability — Section 9.2.5 already argued that the
invariants express professional obligations, not model limitations —
capability gains improve drafting, checking, evidence capture, and conflict
detection without automatically reallocating authority. The philosophical
resource for this stability is Smith's reckoning/judgment distinction,
calibrated in Chapter 3 (§3.6.4) [CITE:Smith2019]. Improved information can
change what a person knows and reduce review effort; it does not by itself
perform an attributable act of professional reliance.

The thesis does not need to decide whether a future artificial system could
be a knower or accountable continuant. The current professional and
operational allocation is unambiguous: only authorized humans issue binding
approval records and assume duty of care. Any future reallocation would
require its own regulatory and governance act; it is not implied by model
capability or by this explanatory account.

One caveat is required, and it is the same caveat that runs through this thesis (§6.9.4, §9.2.4). The structure is capability-invariant; the practice at the gate is capability-stressed. As agent outputs improve, the temptation to rubber-stamp them grows, and the architecture cannot compel the professional's commitment to be real — it can only record whether its trace exists. Rising capability therefore makes drift measurement and honest accounting of review effort more important, not less: the better the drafts, the more the integrity of the gate depends on review discipline that the architecture can evidence but cannot enforce.

The claim is falsifiable, and the repository itself is the longitudinal test. Capability-invariance predicts that the invariant catalog requires zero capability-triggered amendments across model generations — only the tooling around it evolves, as §9.2.5 anticipated. A future model improvement that forces a change to a K-* invariant would falsify the claim.

### 9.3.6 Relationship to the AI Alignment Problem

*Subsection added 2026-07-02.*

The generalization argument extends to a problem usually framed at the model
level. Most alignment work asks how to make a model produce behavior
consistent with human values — through training, feedback, or specification
[CITE:Ouyang2022] [CITE:Bai2022]. The governance problem this thesis
addresses is adjacent but distinct: how to prevent machine output from being
mistaken for accountable judgment. The Chirality response aligns the system
of use, not the model. Whatever the model is internally — however it was
trained, and however capable it becomes — its outputs enter professional
practice only through provenance, epistemic labels, review, gates, and a
recorded human commitment.

The two approaches are complementary, and the architectural approach
addresses only its own class of failure. Model-level alignment reduces the
rate of undesirable outputs; use-level alignment ensures that no output,
good or bad, acquires professional authority without an attributable act by
an accountable person. Nothing in this thesis makes a model intrinsically
truthful, corrigible, or safe under arbitrary deployment — §9.2.4 and §9.2.5
state those limits. As Chapter 3 (§3.6.6) argues, integration does not erase
the accountability gap. Smith's reckoning/judgment distinction (§3.6.4)
[CITE:Smith2019] remains a philosophical resource for preserving the
difference between producing information and accepting responsibility for
reliance on it.

---

## 9.4 Future Work

### 9.4.1 Empirical Validation

The highest-priority future work is a controlled study with licensed engineers evaluating AI-assisted deliverables produced under the Chirality framework. The study design should measure:

- Review accuracy (do reviewers catch more errors with epistemic labels than without?)
- Review efficiency (is review time reduced?)
- Review confidence (do reviewers report higher confidence in their assessment?)
- Practitioner acceptance (is the gate-controlled workflow considered workable?)

### 9.4.2 Runtime Enforcement Engine

The "future tooling" enforcement layer should be implemented as automated checks: staleness calculation from the dependency graph and baseline SHAs, content validation against approved SHAs, merge policy enforcement, and approval integrity verification. This would close the gap between the specified invariant system and the implemented enforcement. (At the monorepo root, the `write_status.sh` transition guard and the practitioner harness's `status`/`drift`/`self-check` commands, built under D-GOV-01..08, are a first slice of this direction.)

### 9.4.3 Empirical Validation of the Warrant Lifecycle

The warrant lifecycle model (UNWARRANTED → CITED → REVIEWED → AUTHENTICATED) and the AUDIT_EPISTEMIC agent that operationalizes it should be empirically validated. Specific questions include: does the warrant state distribution correlate with deliverable quality? do deliverables with higher CITED/REVIEWED ratios produce fewer review findings? does the AUDIT_EPISTEMIC agent's conflict detection catch errors that manual review misses? These questions require data from real project executions.

### 9.4.4 Formal Verification of Invariant Preservation

The invariant system could be subjected to formal verification: given the write scope declarations, the gate structure, and the lifecycle state machine, can it be proven that no sequence of agent actions violates the K-* invariants? This is a formal methods contribution that would strengthen the safety argument.

### 9.4.5 Multi-Jurisdiction Regulatory Mapping

The APEGA mapping should be replicated for other jurisdictions (EGBC, PEO, NSPE, Engineers Australia, UK Engineering Council) to validate the generalizability claim and to identify jurisdiction-specific requirements that the architecture may need to accommodate.

### 9.4.6 Multi-User Concurrent Execution

The current architecture assumes sequential agent execution within a single user session. Multi-user concurrent execution — multiple licensed professionals directing agents against the same project simultaneously — would require a lock mechanism (identified as future hardening candidate 5 in Chapter 8, §8.6.3) and conflict resolution protocols for concurrent write operations.

### 9.4.7 Extension to Other Agent Platforms

The governance architecture is currently coupled to the Chirality desktop application and its specific agent runtime. Demonstrating that the same invariant system, write scope model, and epistemic architecture can govern agents on other platforms (e.g., LangChain, AutoGen, Claude Code) would validate the claim that the contribution is architectural, not implementation-specific.

---

## 9.5 Summary

The Chirality architecture is a complete, working implementation of an SE-governed AI agent system for professional engineering practice. Its limitations are honest: no controlled empirical validation, a regulatory interpretation not yet tested by a regulator, jurisdiction-specific framing, instruction-level enforcement that depends on multi-layer defense in depth, and evolution uncertainty as models improve. Some of its patterns appear structurally portable — especially the epistemic architecture, write quarantine, and governance-first framing — but that portability should be treated as a hypothesis to be tested rather than as a settled conclusion. The most important future work is empirical validation — demonstrating that the epistemic architecture measurably improves the quality and efficiency of professional review.
