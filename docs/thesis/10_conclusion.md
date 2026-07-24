# Chapter 10 — Conclusion

---

## 10.1 Research Question

This thesis asked: *How can systems engineering principles be applied to govern LLM-based agent systems such that their outputs can be relied upon in regulated professional engineering practice?*

One answer developed and implemented in this thesis is the Chirality architecture — a formally specified agent operating system in which SE disciplines are not compliance artifacts applied to an agent system, but the mechanisms by which agents coordinate, failures are contained, and humans maintain authority.

---

## 10.2 Contributions

The thesis presented five novel contributions:

**1. An epistemic architecture for LLM reliability transparency (Chapter
5).** Model outputs carry no intrinsic epistemic warrant; correct and
incorrect claims may be indistinguishable by surface inspection alone.
Chirality's response is to require represented claim states and grounds to be
inspectable through mandatory provenance (K-PROV-1), no invention
(K-INVENT-1), conflict surfacing (K-CONFLICT-1), and epistemic labeling
(FACT/ASSUMPTION/PROPOSAL/TBD). These controls make specified gaps and
nonconformance detectable within their declared coverage; they do not
guarantee that every claim or failure is captured.

**2. A regulatory mapping grounding AI agent governance in existing professional obligations (Chapter 6).** The thesis argued that APEGA's practice standard *Relying on the Work of Others and Outsourcing* can be interpreted to govern AI agent use because the professional's obligations are defined by what the professional must do, not by what the worker is. The Chirality architecture maps APEGA §3.1.1 (direct supervision and control) and §3.1.2 (thorough review) to specific, traceable architectural mechanisms. This contribution shows that existing regulatory frameworks may govern AI agents without requiring entirely new AI-specific regulation, though the interpretation remains jurisdiction- and regulator-dependent.

**3. A four-pillar philosophical framework with fractal instantiation
(Chapter 3).** The thesis identified ontology, epistemology, praxiology, and
axiology as the four accountability questions organizing the architecture and
argued that the epistemology is load-bearing within this design. The
epistemology retains its six operational primitives (claim, warrant, status,
gap, conflict, ruling) and the warrant lifecycle (UNWARRANTED → CITED →
REVIEWED → AUTHENTICATED). The philosophical account distinguishes
externalizable information from the situated, potentially mistaken or
revisable knowledge of a knower. Identical information may occasion different
knowledge—a configurational multiplicity that schemas can scaffold but not
exhaust. Authentication records one attributable, scoped, content-bound
relation of accountable reliance. The permanent accountability gap between
information and accountable knowing is the sole primary chirality of
knowledge. The fractal property is the recurrence of the four accountability
questions across governance, agent instructions, and production documents,
not recurrence of chiral dualities.

**4. A fault containment architecture through write scope quarantine (Chapter 4, §4.6).** The Agent 0/1/2 runtime hierarchy combined with declared write scopes creates formal fault containment zones. Under the declared write-scope contract, a Type 2 agent failure is contained away from source truth. Cross-deliverable operations are explicit, opt-in, and write to isolated tool roots. This adapts classical SE fault containment to the specific challenge of governing probabilistic agents.

**5. A three-layer invariant system with four-layer enforcement (Chapter 4, §4.7; Chapter 7).** The workflow design requirements (R1–R17), the decomposition invariants (I1–I10), and the system-wide K-* catalog maintained in `CONTRACT.md` are enforced through agent instructions, runtime orchestration, human gates, and deterministic tooling. The invariant system constitutes a formal specification of agent behavior constraints applied to a domain — LLM agent governance — where formal methods have not previously been deployed.

---

## 10.3 The Central Insight

The thesis rests on a single insight: **productivity tools optimize for output quality; professional engineering tools optimize for knowing what you can rely on.**

This distinction determines the architecture. A productivity tool asks: how can we make the agent's output better? A professional engineering tool asks: how can we make the epistemic status of the agent's output transparent, so that a competent professional can determine what to rely on? The first question leads to model-level improvements (RLHF, RAG, fine-tuning). The second leads to architectural enforcement (mandatory provenance, epistemic labeling, conflict surfacing, content-addressed approval).

Both questions are valid and complementary. The second directly supports
professional authentication—the attributable act by which a licensed
professional accepts responsibility for reliance on identified work within a
stated scope and purpose. Authentication requires evidence, not just quality.
It confers accountable-reliance status; it does not create knowledge or
guarantee truth.

---

## 10.4 Implications for Practice

**For engineering firms using AI:** The Chirality architecture demonstrates one credible way that AI agents can be directed within existing professional regulatory frameworks. The key is governance architecture, not model capability alone. An engineering firm adopting AI may not need to wait for AI-specific regulation, but it does need a governance framework that can be defended under the existing "relying on the work of others" standard.

**For regulators:** The thesis suggests that existing professional practice standards — supervision, review, authentication — may be sufficient to govern AI agent use, provided the AI system is architected to make compliance structurally supportable and auditable. The four-pillar framework offers a checklist for assessing whether a firm's AI governance is coherent: does it define what exists (ontology)? does it enforce epistemic transparency (epistemology)? does it bound agent action (praxiology)? does it articulate and enforce professional values (axiology)?

**For the AI agent research community:** The thesis identifies a gap between agent capability and agent governability. Current research focuses on making agents more capable. The Chirality architecture shows that capability without governance is insufficient for professional practice. The epistemic architecture — mandatory provenance, no-invention, conflict surfacing, epistemic labeling — is a contribution that other agent frameworks could adopt without adopting Chirality wholesale.

---

## 10.5 Closing

> *AI can accelerate engineering work. It cannot inherit professional responsibility.*

The Chirality architecture is an answer to the question of how to hold these
two facts together. It engineers a harness that widens and organizes the
field of consideration while preserving the human professional's authority
to interpret, narrow, accept, and issue. Authentication records that a
competent person accepts responsibility for reliance on identified content
under duty of care, backed by an auditable record. The person may still be
mistaken and may later revise what they know; the record makes the accountable
relation inspectable.

Taken whole, what this thesis describes is not an agent harness with governance attached. It is a governed application environment for agent-assisted professional work — an enclosure in which agents, deterministic tools, domain applications, project records, and human authority coexist without output being confused with authority. The boundary the environment maintains is not a limitation on what AI-assisted work can become; it is what creates the territory: AI may extend reckoning — wider perception, sharper comparison, deeper preparation, better memory — but it must not inherit judgment. Most of professional work is not the final act of commitment; it is preparation, discernment, comparison, and correction, and all of that can be transformed while the final act stays where duty of care places it.

If we cannot make it auditable, we cannot rely on it. This system makes it auditable.

The deeper question—what a knower may find in information, and how committed
practice shapes that knowing—is not settled by the architecture. Appendix D
offers a non-foundational existential conjecture and a bounded configurational
analogy. Neither is required for the thesis conclusions, governance
requirements, or architectural recommendations.
