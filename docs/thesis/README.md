# Thesis — Systems Engineering of LLM Agent Governance for Regulated Professional Practice

## Research Question

*How can systems engineering principles be applied to govern LLM-based agent systems such that their outputs can be relied upon in regulated professional engineering practice?*

## Status

| Chapter | File | Status |
|---------|------|--------|
| Front Matter | `00_front_matter.md` | Draft (Opus) |
| 1. Introduction | `01_introduction.md` | Draft (Opus) |
| 2. Literature Review | `02_literature_review.md` | Draft (Sonnet + Opus synthesis) |
| 3. Philosophical Framework | `03_philosophical_framework.md` | Draft (Opus) |
| 4. Architecture | `04_architecture.md` | Draft (Sonnet) |
| 5. Epistemic Architecture | `05_epistemic_architecture.md` | Draft (Opus) |
| 6. Professional Practice Integration | `06_professional_practice.md` | Draft (Sonnet + Opus) |
| 7. SE Design Analysis | `07_se_design_analysis.md` | Draft (Sonnet) |
| 8. Implementation and Validation | `08_implementation.md` | Draft (Sonnet) |
| 9. Discussion | `09_discussion.md` | Draft (Opus) |
| 10. Conclusion | `10_conclusion.md` | Draft (Opus) |
| Appendix A — Invariant Catalog | `appendix_a_invariant_catalog.md` | Draft (Sonnet) |
| Appendix C — APEGA Mapping | `appendix_c_apega_mapping.md` | Draft (Sonnet) |
| Appendix D — A Conjecture on the Nature of Being and Knowing | `appendix_d_framework_s.md` | Draft (Opus) |
| References | `references.md` | Draft (verified pass 2026-07-02) |
| Glossary | `glossary.md` | Draft (Sonnet) |

There is no Appendix B: the agent index is maintained as the live `AGENTS.md` registry at the repository root rather than as a static appendix. The `bigger-picture/` subdirectory contains supporting planning artifacts, not thesis chapters — see `bigger-picture/README.md`.

## Warrant Status

*Note dated 2026-07-01.*

Every chapter is agent-drafted (as the Status table records), directed by the
owner, drawing from the cited governed sources in the Source Material table.
Applying the system's own warrant lifecycle (`docs/TYPES.md` §10.4,
UNWARRANTED → CITED → REVIEWED → AUTHENTICATED) to this document set: the
thesis stands at CITED/REVIEWED. It has NOT been AUTHENTICATED. That transition
would require the owner's attributable act binding acceptance to identified
content, scope, and purpose, and it has not occurred. Appendix D offers
"double commitment" only as a non-foundational interpretation of such an act.
Per K-CLAIM-1 the thesis therefore binds nothing and is not a governance
surface; on any disagreement, the governed record (root `docs/`, decision
records) governs.

*Revision note dated 2026-07-23 (D-GOV-19 candidate).* The owner approved
`D-GOV-19` at candidate commit
`981149df247fb6564768f8451e3b12dd591d9197` as the basis for a concordant
Revision 3 of `CHIRALITY_FRAMEWORK.md` and this thesis. The revision locates
knowledge in a situated knower; treats authentication as an attributable,
scoped, SHA-bound act conferring accountable-reliance status; and makes the
permanent accountability gap the sole primary chirality of knowledge.
Identical information may occasion different, mistaken, or revisable
knowledge—a property termed configurational multiplicity. This prose remains
a candidate pending separate owner review. The approval of D-GOV-19 did not
authenticate the thesis, which remains CITED/REVIEWED and nonbinding.

An owner-revision backlog for the thesis is catalogued in `plans/consistency_audit_2026-07-01.md` (2026-07-01).

*Revision note dated 2026-07-02.* An owner-directed reconciliation pass was applied across the document set: Appendix A regenerated from the live `docs/CONTRACT.md` (27 K-* invariants); mutable registry counts removed from prose; APEGA and Engineers Canada AI-guidance currency updates (Chapters 2, 6, 9); claim-strength language normalized to Chapter 8's stated enforcement model; epistemic-labeling attribution aligned with D-GOV-08; Chapter 2 vocabulary and citation-binding corrections; glossary and cross-reference fixes. The thesis remains CITED/REVIEWED, not AUTHENTICATED.

*Revision note dated 2026-07-02 (positioning pass).* A second owner-directed pass stated the whole-system category — a governed application environment for agent-assisted professional work — in Chapters 1, 4, and 10; added §9.3.6 on the relationship to the AI alignment problem (align the system of use, not the model); named Smith and Polanyi as the principal philosophical pair (now recalibrated in §3.6.4); added an Author's Note and Appendix D §D.8 recording the origin of the conjecture; added glossary entries for reckoning, judgment, chirality of knowledge, and the accountability gap; and repaired stale `PLAN.md` section pointers in Chapters 8 and 9. The thesis remains CITED/REVIEWED, not AUTHENTICATED.

*Revision note dated 2026-07-18.* Owner-directed maintenance pass under the architecture-evaluation remediation program: the workflow-requirement range was corrected from R1–R12 to R1–R17 in this README and Chapter 4 (Appendix A already cataloged R1–R17; narrative had drifted behind the live registry, and per K-AGENTS-1 the registry governs on disagreement). The thesis remains CITED/REVIEWED, not AUTHENTICATED.

*Revision note dated 2026-07-18 (completion pass).* Owner-directed follow-up extending the range correction to the remaining chapters: R1–R12 → R1–R17 in Chapter 1 (two occurrences), Chapter 2, Chapter 9, and Chapter 10. In the same Chapter 2 sentence, the series names "Runtime Invariants" and "Interaction Invariants" were corrected to the catalog's canonical "Workflow Design Requirements" and "Decomposition Invariants" (Appendix A §A.1–A.2) — the same narrative-behind-registry drift class. No other content changed. The thesis remains CITED/REVIEWED, not AUTHENTICATED.

## Five Novel Contributions

1. **Epistemic architecture** — mandatory provenance, no-invention, conflict surfacing, epistemic labeling as a response to the LLM reliability problem
2. **Regulatory mapping** — APEGA "Relying on the Work of Others" maps directly to AI agent governance; AI agents are "others" whose work the professional relies on
3. **Four-pillar philosophical framework** — ontology/epistemology/praxiology/axiology with fractal instantiation through the document kit
4. **Fault containment through write scope** — Agent 0/1/2 runtime hierarchy with formal blast radius containment
5. **Three-layer invariant system** — R1–R17, I1–I10, K-* with four-layer enforcement map

## Source Material

All thesis content draws from the Chirality project governance documents. Primary sources:

| Document | Thesis Chapters |
|----------|----------------|
| `CHIRALITY_FRAMEWORK.md` | 1, 3, 5, 10, Appendix D |
| `docs/DIRECTIVE.md` | 1, 3, 5 |
| `docs/DBM_Agent_Instruction_Architecture.md` | 4, 8 |
| `docs/SE_Design_Analysis.md` | 7 |
| `docs/CONTRACT.md` | 4, 5 |
| `docs/SPEC.md` | 4 |
| `docs/TYPES.md` | 4 |
| `PROFESSIONAL_ENGINEERING.md` | 6 |
| `agents/AGENT_HELPS_HUMANS.md` | 4, 5 |
| `docs/DECOMPOSITION_STANDARD.md` | 4 |
