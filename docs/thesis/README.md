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

There is no Appendix B: the agent index is maintained as the live `AGENTS.md` registry at the repository root rather than as a static appendix. Supporting planning artifacts formerly kept in a `bigger-picture/` subdirectory here now live in `plans/bigger-picture/`.

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

*Revision note dated 2026-09-19.* Two subsections were added to Chapter 9 in a working session: §9.3.7, which
records the owner's observation that the four structures of the architecture
are the structures large-project delivery already converged on and which the
owner directed into the thesis, and §9.4.8, an agent-proposed future-work
item that follows from it (a second accountable professional, outside
software). The owner's words are recorded in
`plans/evidence/2026-09-19_owner_words_four_graph_structures.md`. The Status
table above still names the models that first drafted Chapters 4 and 9; the
passages dated 2026-09-19 in them were drafted by Claude Fable 5.1 and were
checked before merge by an independent agent review (Claude Opus 5), which is
an editorial and consistency check and confers no warrant state under
`docs/TYPES.md` §10.4. Both are agent-drafted (Claude Fable 5.1), carry no
citations yet and are UNWARRANTED until a verified pass adds sources; the
observation they record is the owner's. Chapter 4 was revised the same day so that it no
longer describes only two of the four structures: a paragraph in §4.1, a note
in §4.2.1, a new §4.3.5 (the four structures, where each is realized, the two
readings of the dependency graph, provenance as the network's key edges, a
statement that today the folder structure and file versions alone carry all
four, the owner's intended development (a knowledge decomposition over the
file directory, a structuring of its yield into the corresponding graphs, and
a BM25 and vector-store search tool called through a workflow or skill, all
as rebuildable projections of the versioned files), and the loop with the
human on two of its edges) and a paragraph in §4.10. §4.3.4 and
the normative edge classes of `docs/TYPES.md` §3 are unchanged. They do not change the thesis's
status, which remains CITED/REVIEWED and nonbinding. A dated illustrated draft
of the four structures is at `plans/four_graphs_of_knowledge_work_2026-09-19.html`,
with an agent-facing note beside it.

An owner-revision backlog for the thesis is catalogued in `plans/consistency_audit_2026-07-01.md` (2026-07-01).

*Revision note dated 2026-07-02.* An owner-directed reconciliation pass was applied across the document set: Appendix A regenerated from the live `docs/CONTRACT.md` (27 K-* invariants); mutable registry counts removed from prose; APEGA and Engineers Canada AI-guidance currency updates (Chapters 2, 6, 9); claim-strength language normalized to Chapter 8's stated enforcement model; epistemic-labeling attribution aligned with D-GOV-08; Chapter 2 vocabulary and citation-binding corrections; glossary and cross-reference fixes. The thesis remains CITED/REVIEWED, not AUTHENTICATED.

*Revision note dated 2026-07-02 (positioning pass).* A second owner-directed pass stated the whole-system category — a governed application environment for agent-assisted professional work — in Chapters 1, 4, and 10; added §9.3.6 on the relationship to the AI alignment problem (align the system of use, not the model); named Smith and Polanyi as the principal philosophical pair (now recalibrated in §3.6.4); added an Author's Note and Appendix D §D.8 recording the origin of the conjecture; added glossary entries for reckoning, judgment, chirality of knowledge, and the accountability gap; and repaired stale `PLAN.md` section pointers in Chapters 8 and 9. The thesis remains CITED/REVIEWED, not AUTHENTICATED.

*Revision note dated 2026-07-18.* Owner-directed maintenance pass under the architecture-evaluation remediation program: the workflow-requirement range was corrected from R1–R12 to R1–R17 in this README and Chapter 4 (Appendix A already cataloged R1–R17; narrative had drifted behind the live registry, and per K-AGENTS-1 the registry governs on disagreement). The thesis remains CITED/REVIEWED, not AUTHENTICATED.

*Revision note dated 2026-07-18 (completion pass).* Owner-directed follow-up extending the range correction to the remaining chapters: R1–R12 → R1–R17 in Chapter 1 (two occurrences), Chapter 2, Chapter 9, and Chapter 10. In the same Chapter 2 sentence, the series names "Runtime Invariants" and "Interaction Invariants" were corrected to the catalog's canonical "Workflow Design Requirements" and "Decomposition Invariants" (Appendix A §A.1–A.2) — the same narrative-behind-registry drift class. No other content changed. The thesis remains CITED/REVIEWED, not AUTHENTICATED.

*Revision note dated 2026-07-24 (citations-and-meaning pass).* An
agent-authored pass applied under owner direction; the prose of this pass is
the agent's, not the owner's words, and carries the thesis's provisional
status like everything else here. Scope: four adversarially verified
references added to `references.md` and the Chapter 2 local blocks
([Smith1985], [Naur1985], [Collins2010], [MacKenzie2001]); the
limits-of-verification argument added to §2.3.5 and the software-practice
precedents (Naur, Collins) to §2.5; [CITE:Smith1985] attached to Chapter 5's
detection-over-prevention design statement; a positive from–to account of the
record's subsidiary role added to §3.6.5 with a cross-reference from the
Chapter 3 warrant lifecycle to Appendix D's interpretive reading (analogue,
not definition, preserved); §9.2.6 added (over-proceduralization as displaced
attention) and §9.3.5 sharpened with Collins on answerability-as-status. The
thesis remains CITED/REVIEWED, not AUTHENTICATED — informative, not
governance.

*Revision note dated 2026-07-24 (coherence pass).* A second agent-authored
pass applied under owner direction (the prose is the agent's, not the
owner's words), resolving five stress points from a four-pillar coherence
review: (1) the "cannot be mechanized" claim in §6.9.4 clarified as an
institutional claim about answerability, not a speculation about machine
cognition, aligning it with §9.3.5's stated agnosticism; (2) the two kinds
of record — descriptive and constitutive — distinguished explicitly in
§3.2.1, marking the seam the `Claim`/`Ruling` primitives already track;
(3) architectural vs. justificatory priority distinguished in §3.4,
resolving the apparent tension between "pillars serve the epistemology" and
the axiological grounding of Chapter 6; (4) the category shift at
REVIEWED → AUTHENTICATED flagged at the Chapter 3 lifecycle (evidential
standing vs. normative standing), tied to §3.6 and Appendix D; (5) the
"necessary condition" claim in §6.9.4 narrowed to demonstrable satisfaction
of the mapped standards, and the axiology's thin formal treatment stated as
deliberate in §3.2.4 ("thin in the document because it is thick in the
knower"). The thesis remains CITED/REVIEWED, not AUTHENTICATED —
informative, not governance.

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
| `docs/thesis/CHIRALITY_FRAMEWORK.md` | 1, 3, 5, 10, Appendix D |
| `docs/DIRECTIVE.md` | 1, 3, 5 |
| `docs/DBM_Agent_Instruction_Architecture.md` | 4, 8 |
| `docs/thesis/SE_Design_Analysis.md` | 7 |
| `docs/CONTRACT.md` | 4, 5 |
| `docs/SPEC.md` | 4 |
| `docs/TYPES.md` | 4 |
| *Professional Engineering with Agentic AI in Regulated Practice* (firm QMS) | 6 |
| `agents/AGENT_HELPS_HUMANS.md` | 4, 5 |
| `docs/DECOMPOSITION_STANDARD.md` | 4 |

Relocation note (2026-08-02): `CHIRALITY_FRAMEWORK.md` and
`SE_Design_Analysis.md` were moved from the governance root into this thesis
folder. Their operational content is normatively owned by `docs/TYPES.md`,
`docs/CONTRACT.md`, and `docs/DIRECTIVE.md`; the documents here retain the
explanatory derivation. `PROFESSIONAL_ENGINEERING.md` (the firm's professional
practice standard, formerly at the repository root) is now maintained in the
Chirality AI Ltd. quality management system outside this repository; the
pre-relocation text remains available in git history and in the accepted
decomposition source packs under `domains/chirality/_Decomposition/`.
