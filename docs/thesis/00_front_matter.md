# Systems Engineering of LLM Agent Governance for Regulated Professional Engineering Practice

**The Chirality Thesis**

---

Ryan Tufts, P.Eng.
Chirality AI Ltd. (APEGA P17007)

2026

---

## Abstract

Large language models can accelerate engineering work, but their outputs
carry no intrinsic epistemic warrant—correct and incorrect claims may be
indistinguishable by surface inspection alone. This thesis presents
Chirality, a formally specified agent operating system that governs LLM-based
agents for use in regulated professional engineering practice. Rather than
attempting to improve model reliability, the architecture requires
represented claim states and grounds to be inspectable through four
mechanisms: mandatory provenance, no-invention rules, conflict surfacing, and
epistemic labeling. The contribution is developed at three levels: a
philosophical framework for professional accountability, an architectural
pattern for governed agent execution, and a concrete filesystem-native
implementation.

The architecture rests on four philosophical pillars — ontology,
epistemology, praxiology, and axiology — with the epistemology identified as
the load-bearing pillar within this design because its removal most directly
defeats the system's ability to support professional reliance. The
epistemology has its own formal ontology: six primitives (claim, warrant,
status, gap, conflict, ruling) whose relationships constitute the substrate
of the epistemic layer, and a warrant lifecycle (UNWARRANTED → CITED →
REVIEWED → AUTHENTICATED) that tracks claim states interleaved with the
deliverable production lifecycle. The four pillars are a compact framework
for accountability rather than an exhaustive categorization of knowing.

The thesis locates knowledge in a situated knower, who may know wrongly or
revise what they know. Information is an externalizable substrate that may
occasion different knowledge across knowers, contexts, purposes, and times.
Authentication does not create knowledge or establish truth; it is an
attributable, scoped, content-bound act conferring accountable-reliance
status. The permanent non-identity between information and accountable
knowing is the sole primary chirality of knowledge. The four-document
production kit (Datasheet, Specification, Guidance, Procedure) exhibits a
different fractal property: the same four accountability questions recur at
the deliverable, agent, and governance levels.

The thesis argues that the APEGA practice standard *Relying on the Work of Others and Outsourcing* can be interpreted to govern AI agent use through the same professional obligations that govern reliance on other human-prepared work, because those obligations are defined by what the professional must do, not by what the worker is. The Chirality architecture maps direct supervision and control (APEGA §3.1.1) and thorough review (APEGA §3.1.2) to specific, traceable architectural mechanisms, offering a conservative and professionally grounded interpretation rather than a regulatory ruling.

The system has been implemented with a governed suite of agent instruction files, deterministic tools, a three-layer invariant system (R-, I-, and K-series invariants under a four-layer enforcement map), and a desktop application. Active membership is maintained in the source registries rather than mutable count prose. Classical systems engineering disciplines — architecture, configuration management, verification and validation, safety engineering, requirements engineering, control theory, formal methods, and human factors — are not treated here as compliance artifacts applied after the fact, but as the primary mechanisms by which this implementation coordinates agents, contains failures, and preserves human authority.

**Keywords:** systems engineering, LLM agents, professional engineering, epistemic architecture, epistemic ontology, warrant lifecycle, chirality of knowledge, accountability gap, configurational multiplicity, agent governance, formal invariants, APEGA, professional work products, provenance, write quarantine

---

## Author's Note

The originating intuition behind Chirality was that meaning is not manufactured — not by the machine, and not by the professional. It is encountered, already intelligible and already significant, under conditions of responsibility. The architecture developed in this thesis is a practical attempt to preserve that encounter in AI-assisted professional work: to let AI widen what the professional can perceive, compare, and prepare, while keeping the acts of judgment, commitment, and answerability where they have always lived — with the person. The main argument asks no assent beyond professional and philosophical grounds. The deeper layer, for readers who want it, is developed in Appendix D, which also records the origin of the conjecture (§D.8).

---

## Table of Contents

1. [Introduction](01_introduction.md)
2. [Literature Review](02_literature_review.md)
3. [Philosophical Framework](03_philosophical_framework.md)
4. [Architecture](04_architecture.md)
5. [Epistemic Architecture](05_epistemic_architecture.md)
6. [Professional Practice Integration](06_professional_practice.md)
7. [SE Design Analysis](07_se_design_analysis.md)
8. [Implementation and Validation](08_implementation.md)
9. [Discussion](09_discussion.md)
10. [Conclusion](10_conclusion.md)

**Appendices**

- [A — Invariant Catalog](appendix_a_invariant_catalog.md)
- B — Agent Index: maintained as the live registry `AGENTS.md` at the repository root; not reproduced as a static appendix
- [C — APEGA Regulatory Mapping](appendix_c_apega_mapping.md)
- [D — A Conjecture on the Nature of Being and Knowing](appendix_d_framework_s.md)

**Reference Material**

- [References](references.md)
- [Glossary](glossary.md)
