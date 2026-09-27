# Chirality thesis and owner notes: conceptual foundation for the v4 PRD

**Investigation basis.** I read REPO_ROOT = `/Users/ryan/ai-env/projects/chirality/.claude/worktrees/chirality-app-v4-architecture-9f35c4` at main@2b0572fe0. I changed nothing.

- All thesis files were read in full: README, 00, 01, 03–06, 08–10, CHIRALITY_FRAMEWORK, App A, App C §C.1/C.3–C.5, App D and the glossary.
- Chapter 7 was read in full except §7.8.2–7.8.4 (formal types and state machine).
- `SE_Design_Analysis.md` was checked for headings, opening, closing assessment and naming drift only.
- Chapter 2 was skimmed for its argument structure (intro, gap subsections, §2.5 intro, §2.6).
- `references.md` was checked for structure only.

**Abbreviations used below:**
- `T/` = `REPO_ROOT/docs/thesis/`
- **CF** = `T/CHIRALITY_FRAMEWORK.md`
- **OW** = `REPO_ROOT/plans/evidence/2026-09-19_owner_words_four_graph_structures.md`
- **FG** = `REPO_ROOT/plans/four_graphs_agent_orientation_2026-09-19.md`
- **AT** = `REPO_ROOT/plans/evidence/2026-08-01_accountability_thesis.md`

Chapter references look like "Ch4 §4.3.5 L146", where L is the line number.

**Evidence labels:**
- [owner words]
- [agent-drafted, cited]
- [agent-drafted, uncited]
- [described design]
- [executed check with record]
- [agent inference]

---

## 0. Standing of the corpus

- **Every chapter was drafted by an agent** (Opus, Sonnet or Fable) under the owner's direction (`T/README.md` L9–26, L34–35).
- **What the thesis claims about itself.** It stands at CITED/REVIEWED, not AUTHENTICATED. Under K-CLAIM-1 it "binds nothing and is not a governance surface"; on any disagreement the governed record in `docs/` governs (README L36–44).
- **Revision 3 is still a candidate.** Its prose (knowledge in the knower, relational authentication, the accountability gap as the sole chirality) was approved as a *basis* under D-GOV-19. The prose itself "remains a candidate pending separate owner review" (README L46–56). CF's header still reads "Revision 3, Candidate for Owner Review" (CF L4).
- **The 2026-09-19 additions are UNWARRANTED.** These are §4.1 ¶, §4.2.1 note, §4.3.5, §4.10 ¶, §9.3.7 and §9.4.8. They were agent-drafted by Claude Fable 5.1, carry no citations, and are UNWARRANTED; the independent agent review "confers no warrant state" (README L58–84). The *observation* in them is the owner's (OW).
- **The later revision passes are the agent's words.** The 2026-07-24 passes state explicitly that "the prose of this pass is the agent's, not the owner's words" (README L96–110, L112–129).
- **Owner-words custody varies by record:**
  - OW holds verbatim owner messages with SHA-256 hashes. Its sketch transcription is the agent's lettering, which the owner confirmed "100% correct" (OW L3, L61–69).
  - AT §1 records owner theses "as close to the owner's words as fidelity allows", with some direct quotes and no hashes. AT §2 is explicitly the model's elaboration, to be superseded by re-derivation (AT L14–16, L75–81).
- **No executed check records.** The subject corpus contains no [executed check with record]. Chapter 8 names scripts, CI jobs and example roots, but reproduces no run records, results or hashes (see §2.3).

---

## 1. Core propositions

| # | Proposition | Where | Standing |
|---|---|---|---|
| P1 | **Information vs knowledge.** Information is an externalizable substrate. Knowledge is a *situated achievement of a knower* and need not be factive: one may "know wrongly … and revise". `Claim`/`Warrant` make a knower's basis inspectable but are not knowledge. | CF §2.1 L24–40; Ch3 §3.6.1 L322–342 | [agent-drafted, cited]: Polanyi and Smith as principal resources (Ch3 §3.6.4 L385–432). D-GOV-19 candidate prose. |
| P2 | **Configurational multiplicity.** Identical information may occasion different knowledge across knowers, contexts, purposes and times. Schemas, Knowledge Types, lenses and knowledge graphs are "scaffolding … not exhaustive state spaces". | CF §2.2 L43–55; Ch3 §3.6.3 L359–381 | [agent-drafted, uncited] as a coined concept. The chemistry/quantum analogy is cited but explicitly "not a warrant for the architecture" (App D §D.7 L211–237). |
| P3 | **The accountability gap is the "sole primary chirality of knowledge."** It is the permanent non-identity between information and accountable knowing. It is distinct from operational `Gap` (a remediable missing warrant). "Permanent, but … workable." | CF §2.4 L76–102; Ch3 §3.6.2 L344–357, §3.6.5 L457–462 | [agent-drafted, cited] (Smith 1996/2019). D-GOV-19 candidate. |
| P4 | **Authentication is an attributable, scoped act bound to content/SHA and purpose.** It confers *accountable-reliance status* and does not create knowledge or establish truth. REVIEWED→AUTHENTICATED is a change in *normative*, not evidential, standing: "the epistemology hands off to the axiology". | CF §2.3 L57–74, §3.3.3 L260–264; Ch3 L160–171, §3.6.7 L489–494; Ch6 §6.5.5 L219–223 | [agent-drafted, cited] (APEGA standards). The "double commitment" reading is App D only, as an interpretive aid (CF L71–74). |
| P5 | **Agents have "bounded operative agency, but not accountable agency."** They are among the "others" whose work a licensed professional relies on under APEGA *Relying on the Work of Others*, because the standard's obligations are defined by what the *professional* must do. | CF §2.5 L106–115; Ch6 §6.3.1 L59–68, §6.3.2 L74–84 | [agent-drafted, cited]. Explicitly "an interpretation, not a regulatory ruling" (Ch6 §6.9.1 L394–402). APEGA's own AI guidance leans toward treating AI output as *tool* output (Ch6 §6.2.3 L49; §6.9.3 L410–416). |
| P6 | **Six epistemic primitives and a warrant lifecycle.** The primitives are claim, warrant, status, gap, conflict and ruling. Status labels are FACT, ASSUMPTION, PROPOSAL and TBD. The warrant lifecycle UNWARRANTED→CITED→REVIEWED→AUTHENTICATED is interleaved with the production lifecycle. Thorough review = "auditing warrant sufficiency." | CF §3.3.1–3.3.3 L201–264; Ch3 L111–171; Ch5 §5.5 L174–209 | [agent-drafted, cited] (Toulmin, W3C PROV). Normatively owned by `docs/TYPES.md` §10, which is outside the thesis. Labeling has no producer-side enforcing invariant; it is assessed at audit time under D-GOV-08 (Ch5 L144). |
| P7 | **Four pillars as accountability questions.** Ontology, epistemology, praxiology and axiology. Epistemology is *architecturally* load-bearing; axiology is *justificatory* ("thin in the document because it is thick in the knower"). The "fractal property" is only the recurrence of the four questions across levels. | CF §3.2 L170–191, §3.4 L266–280; Ch3 §3.2.4 L206–218, §3.3, §3.4 L256–280 | [agent-drafted, cited] (Bunge, Wand–Weber, INCOSE). |
| P8 | **Detection over prevention.** "The system does not try to prevent hallucination; it makes unsupported claims structurally visible." Verification relates artifacts to artifacts, never model to world. | Ch1 §1.3 L48; Ch5 §5.4 L170 | [agent-drafted, cited] (Smith 1985). |
| P9 | **The authority boundary does not depend on capability.** Authority is indexed to answerability, not capability. The claim is stated as falsifiable: zero capability-triggered K-* amendments across model generations. Caveat: the *practice at the gate* is "capability-stressed" (rubber-stamping risk). | Ch9 §9.3.5 L126–161 | [agent-drafted, cited] (Smith 2019, Collins 2010). |
| P10 | **Align the system of use, not the model.** | Ch9 §9.3.6 L167–188 | [agent-drafted, cited]. |
| P11 | "Productivity tools optimize for output quality. Professional engineering tools optimize for knowing what you can rely on." | CF §5 L336–348; Ch3 L284; Ch10 §10.3 | [agent-drafted, uncited]. |
| P12 | **Four graph structures.** "the invariants are the stable graph structures that underlie knowledge work as-such (was always my claim)." The fourth structure is named "Attention". This is how humans tackle large projects "and many distinct agents (human agents, but they are the OG agents afterall)." | OW L10, L26, L34 | [owner words]. |
| P13 | **Measure of quality.** Quality = "how much warranted confidence it produces per unit of your attention, and the toggle sets how much of that confidence a given piece of work needs." | OW L18 | An agent sentence the owner adopted ("Pretty much this, yes") [owner words]. |
| P14 | **Owner's founding theses (AT §1):** | AT L19–73 | [owner words], recorded close to verbatim, no hashes. |
| | Harnessing agents "with capabilities far beyond humans, but lacking the accountability of human judgment … at scale, reliably" is the bedrock for the future of professional work. | AT L63–66 | |
| | "everyone else is porting software culture into agents"; we already have the model in professional/capital-projects delivery. | AT L49–53 | |
| | Professionals lack a "strong grasp on what their knowledge actually is and how it is grounded and why". | AT L68–73 | |
| | Build-time vs run-time governance asymmetry (§5 below). | AT L19–24 | |

---

## 2. Architectural ideas: purpose-level or tied to a historical mechanism

Classification: **(a)** a purpose-level commitment that could survive any implementation; **(b)** tied to a specific historical mechanism.

### 2.1 Classification table

| Idea | Problem addressed | Class | Thesis evidence |
|---|---|---|---|
| Mandatory provenance, no-invention, conflict surfacing, epistemic labeling | LLM output carries no intrinsic warrant, so review would become re-derivation (Ch1 §1.1 L18; Ch5 §5.2) | (a) as commitments. (b) in concrete form: `Dependencies.csv` v3.1 with 29 columns and `EvidenceFile`/`SourceRef`/`EvidenceQuote`; Conflict Table with `HumanRuling=TBD` (Ch5 §5.3 L58–129) | [described design] with worked examples (Ch5 L68–101, L117). Enforcement is mainly agent instructions and audits (Ch8 §8.6.2 L311). No conformance or error-rate data: "[TODO: Characterize the actual error rates…]" (Ch8 L375). |
| Human-only binding approval (K-AUTH-1); humans rule | Output mistaken for authority | (a) | [described design]. Enforced by instruction constraints and human review (App A L74). |
| Content-bound approval (K-AUTH-2, K-VAL-1) | Approved ≠ relied-upon artifact | (a) as "bind acceptance to identified content"; (b) as git SHA | SHA comparison is "future tooling", not automated (Ch8 §8.6.2 L329; App A L75, L104). |
| Filesystem-as-state / git as event store / "no hidden memory" | Auditability, reproducibility, independence from vendors and chat context (Ch4 §4.2.2 L44–56) | Purpose (a): relied-upon state must be in an identified, versioned record. Mechanism (b): git plain files, no DB. | The thesis calls it "load-bearing" (Ch1 L32; Ch4 L19). It is softened by D-GOV-01: rebuildable, gitignored projections are allowed but never authority (Ch4 §4.3.5 L148). Engine-owned domain stores are exempt (App A L152). |
| Agent 0/1/2 runtime hierarchy | Authority must not grow through delegation; escalation flows upward; Agent 2 does not delegate | (b) mechanism; (a) purpose ("authority and capability do not increase through delegation") | [described design] (Ch4 §4.5, §4.8.1). Contribution #4 is stated in mechanism terms (README L136). |
| Write-scope fault containment ("write quarantine") | Bound the blast radius of a failing probabilistic agent | (a) purpose; (b) mechanism: WRITE_SCOPE header enum, tool roots, TASK-shell ScopePath check (K-WRITE-2) | Mostly declared contract plus diff review. The thesis deliberately chose declaration in agent instructions over OS permissions (Ch4 L394). Ch8 §8.6.4 L362–368 says runtime hooks reject out-of-scope writes, but gives no record. |
| Three invariant layers (R1–R17, I1–I10, K-*) with a four-layer enforcement map | Make constraints binding across layers; defense in depth | (b) | [described design]. "Instruction-layer constraints still depend on model conformance" (Ch8 L320). Five K-* invariants rely on future tooling (Ch8 L329). |
| Four structures: tree, production DAG, network, attention | Composition, precedence, relevance, synthesis. Each fails recognizably when neglected (Ch4 L160). | Owner claims (a): "underlie knowledge work as-such" (OW L10). Today's realization is (b) files. | [agent-drafted, uncited], UNWARRANTED (Ch4 L135; Ch9 L192–195). The intended development (decomposition of the app directory, graph structuring, BM25 plus vector search via workflow/skill) is **not built** (Ch4 L148). |
| Micro lifecycle vs macro stage gate | Category error common in PM tooling (Ch4 §4.4.3 L206–216) | (a) as distinction; (b) as the specific six states | [described design] |
| Deterministic vs probabilistic boundary | Keep non-determinism where judgment is needed; algorithmic checks go to tools | (a) | [described design] (Ch6 §6.7.3 L304–308; Ch8 §8.3.2 L201–207) |
| Domain-engine boundary (K-DOMAIN-1..4) | Agent output must not become engineering truth; solver/model state owned by the engine | (a) purpose; (b) OperationProposal, profiles, `protected_write_paths` | [described design] (App A L147–150) |
| Immutable snapshots, brief contracts, `FAILED_INPUTS` fail-fast | Reproducible, auditable runs; safe reruns | (a) purpose; (b) INIT-TASK format and snapshot folder layout | [described design] (Ch4 §4.9) |
| Consequence-calibrated oversight | Ceremony without safety benefit | (a) | K-GATE-1 "dynamic per project instance" (App A L110). Ch4 §4.8.4 L544 lowers per-action overhead where consequence is low. Coordination modes SCHEDULE_FIRST/DEPENDENCY_TRACKED/HYBRID (Ch7 §7.9.3 L488–494). Owner's validation-level "toggle" (OW L18; FG L47–50). |
| Instruction root vs working root | Stable governing rules separated from a mutable project | (a) purpose; (b) v1 "bundled with the application … requires a new application release" (Ch8 §8.4.1 L223) | [described design] |
| Session handoff files (`NEXT_INSTANCE_*`), human-triggered sessions only | No memory across sessions | (b) | "does not run agents autonomously between human interactions" (Ch4 §4.8.3 L531) |
| 3×4 agent matrix UI | Navigation | (b), explicitly legacy | "not the runtime delegation hierarchy" (Ch8 §8.2.3 L71–75) |
| Runtime as "institutional machinery"; one per-user daemon (D-GOV-20) | Competing sessions and permission systems | (b), the v2 shared runtime | CF L394–406. The purpose clause — "the seat's authority contract remains stable when the model changes" — is (a). |

### 2.2 Two of the five headline contributions are mechanisms

README contributions #4 (Agent 0/1/2 plus write scope) and #5 (R/I/K plus four-layer enforcement) are framed as mechanisms (README L136–137). Contributions #1 to #3 are purpose-level.

### 2.3 What Chapter 8 says was executed versus described

**Claimed as fully implemented** (Ch8 §8.6.1 L289–303):
- the agent suite and toolset
- the 7-gate decomposition protocol
- the evaluation subsystem
- AUDIT_DEP_CLOSURE with `analyze_dep_closure.py`
- the desktop app — Next.js/Electron, SSE, 3×4 matrix — which is the v1 app (Ch8 §8.4)
- harness CI validation scripts (Ch8 §8.5.2)

**The evidence cited is a set of pointers, not records:**
- Example roots `execution-6a/b/c` and `AB-2026-01424…` serve as regression cases (Ch8 §8.5.3 L273–281). They "belong to the application's pre-monorepo repository layout and are preserved in repository history" (Ch8 L13).
- No test results, conformance rates or hashes appear.

**Acknowledged not automated:** K-STALE-1, K-VAL-1, K-MERGE-1, K-AUTH-2 and K-DEP-2. A first slice exists at the monorepo root (`write_status.sh`, harness `status`/`drift`/`self-check`) (Ch8 L329–331).

**Internal inconsistencies in Chapter 8:**
- AUDIT_AGENTS is described as a D-GOV-13 candidate whose "named execution fails closed" pending owner approval (Ch8 §8.5.1 L247–251). §8.6.1 says the suite's "conformance [is] verified by AUDIT_AGENTS" (L293, L300).
- The R-series is called "Candidate" (Ch8 L386; Ch7 L346) but "ratified" elsewhere (Ch8 L357–360; App A L5–8).
- The chapter cross-references in Ch8 §8.1 L7 and §8.7 L396 point to the wrong chapters.

**Only observational evidence for the four structures:** one session in which the agent committed three of the four failure types. The same agent classified them, and it notes that one session cannot distinguish the explanations (Ch9 §9.3.7 L256–268, L286–291).

---

## 3. Product expression

**Category.** "Chirality is best categorized as a governed application environment for agent-assisted professional work. The agent operating system is one contained component." The enclosure also holds deterministic tools, governed records, "domain applications where a discipline requires deterministic computation", and human gates. "The thesis's claims attach to the environment, not to any single component" (Ch1 §1.2 L40; repeated in Ch10 §10.5 L90). The positioning pass was owner-directed, but the prose is the agent's (README L90).

**Division of labor.** "agents propose; deterministic tools and domain engines compute; humans rule; the record binds." Chirality "governs the work around a domain application without becoming the solver or the source of accepted engineering truth" (Ch4 §4.10 L605).

**Domain engines (App A §A.3.12 L147–150):**
- K-DOMAIN-1: engines own model files, analysis runs and solver outputs.
- K-DOMAIN-2: protected domain paths are write-quarantined.
- K-DOMAIN-3: domain operations require an OperationProposal, validation by a declared deterministic tool, human acceptance, and an engine-controlled apply.
- K-DOMAIN-4: a green PASS is "structural evidence only". "Validation-passed is necessary, not sufficient."

**Solver truth versus agent output.** Ch3 §3.2.1 L34–48 separates *descriptive* records ("a claim about a pipe's stress state is answerable to the pipe, and the record can be wrong") from *constitutive* records (rulings, approvals, ISSUED). The hierarchy of authority places "verified engineering analysis" above professional judgment. "Agent outputs carry no professional authority" (Ch6 §6.6.5 L270).

**Software-vendor analogy.** The LLM provider is like "the provider of structural analysis software". The "agent" for professional purposes is the governed architecture around the model, not the model (Ch6 §6.3.3 L88–92). APEGA §3.1.2.1's "relevancy and accuracy of … tools" applies (Ch6 L201). Professionals need tool competence (Ch6 §6.6.3). AT §2 item 5 (model elaboration, not owner words): CAE licenses disclaim fitness, and reliance rests on "validation evidence plus the using professional's stamp" (AT L108–114).

**Human decision rights under shared access.**
- *Reserved to the professional:* scope and boundaries, codes and standards, hazard and residual-risk acceptance, conflict adjudication, and approval, issuance, seal and transmittal (Ch6 §6.6.2 L243; Ch7 §7.9.1 L455–460).
- *Agents may:* draft, extract, generate alternatives, surface gaps and conflicts, run checkable transformations, and maintain records — "Agents widen the field of consideration; professionals narrow, accept, and issue" (Ch6 §6.8.2 L360–369).
- CF's normalization table gives a capability matrix by entity: agents may produce claims, attach warrants and classify status, but not issue rulings or authenticate (CF §2.8 L146–153).
- Generated harness output "may not claim acceptance in its own voice" (Ch3 §3.6.5 L453).

**APEGA mapping.**
- Direct supervision and control is mapped to gate-controlled orchestration, agent declarations and versioned records.
- Thorough review is mapped to the REVIEW 5-gate protocol plus labels and provenance.
- Authentication is mapped to a SHA-bound human gate.
- Sources: Ch6 §6.4–6.5; App C §C.1–C.3; the definition mapping is App C §C.4.
- The architecture is "necessary but not sufficient"; the sufficiency condition is competent judgment at each gate (Ch6 §6.9.4 L418–422).

**What the thesis does not say** [agent inference, from absence]:
- nothing on UI or interaction design inside host applications
- no shared object/operation/result vocabulary for human–agent co-work inside an app
- no recovery semantics beyond git rollback and safe reruns (Ch4 §4.9.3 L595)
- no treatment of SWBPIPE by name

It assumes filesystem-native agent execution by "any compliant LLM runtime capable of reading and writing files", plus "direct integration with existing engineering document management workflows" (Ch4 §4.2.3 L60–64). Portability to other agent platforms, including Claude Code, is untested future work: "currently coupled to the Chirality desktop application" (Ch9 §9.4.7 L336).

**What the owner adds on product.**
- *Build versus run (AT L19–24).* "Operational Piping will NOT be approvals-heavy: agents will have near-parity autonomy with human users except at certain prescribed workflow gates. The heavy governance exists for the BUILD." [owner words, near-verbatim]
- *Release (AT L55–61).* The owner will not publish publicly relied-upon software without human accountability for the code, and would open-source once the paradigm is established: "My product is as someone who can use the tool to do the thing."
- *Where the insight arose.* OW was written in "the SWBPIPE implementation session" (OW L3), so the four-structures insight surfaced during engineering-application work. [agent inference] AT does not name SWBPIPE, but "Operational Piping" plausibly refers to it.

---

## 4. Project management and coordinating many agents

**Agent teams become project management.** "Once many agents are arranged into bounded roles, gates, dependencies, and handoffs … It becomes a form of project management. This is not metaphorical." The structures "are the filesystem itself". The recurring governance pattern — normative, operative, evaluative — is analogous to rule-setting, administration and adjudication (CF §2.6 L117–132). [agent-drafted, uncited]

**Large-project delivery as prior art** (Ch9 §9.3.7 L190–299; [agent-drafted, uncited], UNWARRANTED; the observation is the owner's).

The four structures map to delivery practice:

| Structure | Delivery-practice counterpart |
|---|---|
| Tree | WBS and its dictionary |
| DAG | Logic-tied network schedule |
| Network | Document control: decision log, technical queries, deviations, transmittals |
| Attention | Front-end definition |

Further correspondences:
- Two readings of the graph (owner sketch): "blocker sub-set analysis is execution sequencing truth"; "full graph closure = audit truth" (OW L67).
- Independent review ≈ inter-discipline check.
- Scope change ≈ management of change.
- Validation level ≈ ITP hold/witness points set by consequence, "never lowered by whoever performs the work".
- Authentication ≈ the engineer-of-record stamp (Ch9 L221–239).

Three differences make the architecture necessary:
1. "forgetting is total" for agents.
2. "the economics of attention invert": synthesis is abundant, and the accountable person's understanding is scarce.
3. The failure modes coincide (L241–268).

Software practitioners "recover the mechanics without the accountability layer" (L270–276).

The section states its own limits: a "third language" vocabulary, a single accountable professional, and one project and session with self-classified failures (L281–291).

**The loop** (Ch4 §4.3.5 L158; FG L28–32):
- Decomposition → tree → production graph → evidence and decisions → memory → the next decomposition.
- The human owns two edges: acceptance into memory, and steering from memory into the next decomposition.
- If the human deliberately defers an edge (production ahead of the tree, reconciled like as-built records), agents record provisional links and do not repair the edge themselves.

**Operational advice to agents (FG).** FG is a draft orientation note ("Not governance and not an instruction", FG L3) giving usage rules and violation signatures per structure (FG L16–39):
- "a node is not a log"
- state in the work graph, not handoff prose
- "Never write your inference in the owner's voice"
- query memory before decomposing

**Coordination mechanics** ([described design], mostly (b)):
- spawning graph and supervised many-to-many, parent-mediated coordination (Ch4 §4.8.1; Ch7 §7.7.3 L309–326)
- control loop with "Human authority … the halting condition" (Ch7 §7.7.1, §7.7.4 L330–332)
- no central dependency graph, with on-demand aggregation (K-DEP-1; Ch7 §7.10.2 L521–529)
- flat package→deliverable hierarchy, justified by machine-checkable completeness (Ch4 §4.3.1 L93)
- 7-gate decomposition protocol shared across PROJECT/SOFTWARE/DOMAIN variants (Ch8 §8.2.4 L81–99)
- lifecycle vs stage gate (Ch4 §4.4.3)

**Scale limits the thesis acknowledges:**
- sequential, single-user execution; multi-user concurrency is future work (Ch9 §9.4.6)
- a second accountable professional, outside software, is the "most informative available test" (Ch9 §9.4.8)
- the owner's single-human model is "chosen, not forced" (AT L26–31) [owner words]
- "coordination arbitrage" (hub-and-spoke briefs replacing n(n−1)/2 channels) is model elaboration (AT L102–106)

---

## 5. Future work, limitations, tensions, and what the owner's words add

**Acknowledged limitations:**
- no controlled empirical study (Ch1 §1.5; Ch9 §9.2.1)
- the regulatory mapping is an interpretation, specific to Alberta (Ch9 §9.2.2–9.2.3; Ch6 §6.9)
- instruction-level enforcement is soft (Ch9 §9.2.4)
- dependence on current LLM behavior (Ch9 §9.2.5)
- over-proceduralization displacing attention onto the record: "the orientation of attention itself is not architecturally enforceable" (Ch9 §9.2.6 L57–80)
- the architecture is necessary but not sufficient (Ch6 §6.9.4)

**Future work (Ch9 §9.4):**
- empirical validation
- a runtime enforcement engine
- empirical validation of the warrant lifecycle
- formal verification of invariants
- mapping to other jurisdictions
- multi-user concurrency
- extension to other agent platforms
- a second professional
- Ch8 §8.6.3 also lists seven hardening candidates, including staleness tooling.

**Appendix D is explicitly non-foundational.** "Deleting it changes no thesis conclusion" (App D L235–237). §D.8 records the owner's originating conviction (reflection on Ayat al-Kursi), explicitly not required by the thesis (L255).

**Internal tensions I found** [agent inference, each grounded in the cited lines]:
1. **Novelty claims exceed the thesis's own calibration.** Ch2 claims "first complete operationalization … enforced uniformly across all agents" (Ch2 §2.5.8 L515) and "No published architecture provides…" (§2.1.6). This outruns K-CLAIM-1 (App A L127), Ch8's enforcement model, and D-GOV-08 (labeling has no producer-side enforcement).
2. **Files-only state versus the owner's graph and search direction.** "External databases … precluded" (Ch4 §4.2.3 L66–70) sits against the sketch labelling the network quadrant "posgres/neo4j" (OW L68). The "rebuildable projection, never authority" constraint is the agent's application of D-GOV-01 (Ch4 L148), not the owner's words in OW L58.
3. **Human-triggered sessions versus run-time autonomy.** "Human-triggered at each session … does not run agents autonomously" (Ch4 L531) and "human … at every control cycle" (Ch7 L332) conflict with the owner's run-time "near-parity autonomy" (AT L19–24).
4. **"The folder structure is the project structure" (Ch3 L28) versus weak native support.** §4.3.5 concedes the network has "the least native support" and that mapping is "redone in every session" with unconfirmable completeness (Ch4 L146, L154).
5. **Record-keeping inconsistencies:**
   - the Ch8 AUDIT_AGENTS and R-series standing contradictions (§2.3 above)
   - HELPS_HUMANS listed under both NONE and REPO-WIDE, with "six" categories followed by seven (Ch4 L299–305)
   - `SE_Design_Analysis.md` uses PROJECT_SETUP where Ch7 uses ORCHESTRATOR (SE L160, L231, L435)
   - CF's header says Revision 3 while its history table lists Revision 4 (CF L4, L392)
6. **Conservative classification versus the regulator's framing.** The conservative "others" choice imposes a heavier burden than APEGA's "tool" framing (Ch6 §6.9.3 L416).
7. **The v1 app is presented as current implementation.** Ch8 §8.4 describes the v1 Electron/Next app. No later App generation (v3 Codex host) is described in the thesis.
8. **The owner's scepticism about written alignment.** "Alignment is maintained by presence, not prose": the owner is "not confident that writing about it achieves anything" (AT L32–35). A thesis whose first enforcement layer is instruction text sits in tension with this.

**What the owner's words add beyond the thesis prose:**
- the four structures as properties of knowledge work as such
- the attention-efficiency measure
- the build-time versus run-time governance asymmetry
- the capital-projects delivery paradigm
- the professional's own under-articulated knowledge grounding (AT L68–73)
- the release posture

AT §2 elaborations — "capability scales with compute; accountability does not scale", "double deficit", "delegation compels the professions' self-audit" (AT L88–138) — are model inductions. They should not be cited as owner words.

---

## 6. Glossary for a v4 discussion

| Term | Meaning (short) | Defined |
|---|---|---|
| Information | Externalizable substrate; may occasion knowledge | CF §2.1; glossary L41 |
| Knowledge | Situated, possibly mistaken or revisable achievement of a knower | CF §2.1; Ch3 §3.6.1 |
| Configurational multiplicity | Same information → different situated knowledge | CF §2.2; Ch3 §3.6.3 |
| Accountability gap / chirality of knowledge | Permanent non-identity of information and accountable knowing | CF §2.4; Ch3 §3.6.2 |
| `Gap` (primitive) | Remediable record of a missing warrant | CF §3.3.1; TYPES §10.1 |
| Claim / Warrant / Status / Conflict / Ruling | The epistemic primitives; warrant is always extrinsic; ruling is a human decision | CF §3.3.1 L203–214 |
| FACT / ASSUMPTION / PROPOSAL / TBD | Epistemic labels | CF L216–223; Ch5 §5.3.4 |
| Warrant lifecycle | UNWARRANTED→CITED→REVIEWED→AUTHENTICATED | CF §3.3.3; Ch3 L136–171 |
| Authentication / accountable-reliance status | Attributable act bound to content, scope and purpose | CF §2.3; Ch6 §6.5.5 |
| Accountable vs operative agency | Agents act but cannot bear duty of care | CF §2.5 |
| "Others" (APEGA RWO) | Agents whose work the professional relies on | Ch6 §6.3 |
| Direct supervision and control / thorough review | The two APEGA §3.1 routes to authentication | Ch6 §6.4–6.5; App C |
| PWP | Professional work product; authentication does not create it | Ch6 §6.2.2 |
| Four pillars | Ontology, epistemology, praxiology, axiology as accountability questions | CF §3.2; Ch3 §3.2 |
| Mandatory provenance / no-invention / conflict surfacing | K-PROV-1 / K-INVENT-1 / K-CONFLICT-1 | Ch5 §5.3; App A §A.3.9 |
| K-CLAIM-1 | Claims must not overstate their warrant | App A L127 |
| Content-addressed approval | Approval voided by content change | K-AUTH-2; Ch7 §7.3.2 |
| Write quarantine | Declared write scopes; tool roots isolated from source truth | Ch4 §4.6; glossary L88 |
| Domain engine | Owns authoritative domain truth; Chirality governs around it | K-DOMAIN-1..4, App A §A.3.12 |
| Descriptive vs constitutive record | Answerable to the world vs constituting the fact | Ch3 §3.2.1 L34–48 |
| Four structures | Tree, production DAG, network (long-term memory), attention | Ch4 §4.3.5; OW; FG |
| Blocker subset vs full closure | Sequencing truth vs audit truth | OW L67; Ch4 L152 |
| Acceptance and steering edges | The human's two edges of the loop | Ch4 L158; FG L32 |
| Reckoning vs judgment | Calculation vs committed, answerable thought | Ch3 §3.6.4; glossary L45, L63 |
| Governed application environment | The whole-system category | Ch1 §1.2 L40; Ch10 L90 |
| Warranted confidence per unit of attention | The owner-adopted quality measure | OW L18; FG L43 |

---

## 7. Candidate implications for v4 [agent inference]

1. **The thesis's category inverts under the v4 direction.** The thesis places Chirality as the *enclosure* containing domain applications (Ch1 L40; Ch10 L90). The owner's primary v4 expression is Chirality capability *embedded within* host applications such as SWBPIPE.
   - K-DOMAIN-1's "Chirality governs the work around it; it is not the solver" (App A L147) survives the inversion.
   - The enclosure framing and filesystem-as-sole-state (Ch4 §4.2) may not survive it: the host owns its model and store (App A L152 exemption).
   - A PRD would need to restate "governed application environment" in purpose terms rather than assume the enclosure.
2. **Carry purpose-level commitments; treat mechanisms as historical realizations.** Section 2 marks Agent 0/1/2, R/I/K layering, the four-layer enforcement map, WRITE_SCOPE headers, `NEXT_INSTANCE_*`, the 3×4 matrix, the v1 app and the D-GOV-20 daemon as mechanisms. Building on an existing harness means the thesis's instruction-layer enforcement (Ch8 L311, L320) would be supplied, or not, by the host harness's real permissions. Ch9 §9.4.7 names this portability as untested. Tension: README contributions #4 and #5 are mechanism-level, so carrying the thesis "unchanged" also carries mechanism-level contribution claims.
3. **Run-time autonomy versus the thesis's gate density.** The owner's build/run asymmetry (AT L19–24) conflicts with "human-triggered at each session" (Ch4 L531) and "human … at every control cycle" (Ch7 L332). Purpose-level hooks for reconciling them already exist: K-GATE-1 dynamic gates, consequence-calibrated authorization (Ch4 §4.8.4), and the owner-adopted validation-level toggle (OW L18; FG L47–50).
4. **Shared understanding of objects, state, operations, results and recovery is only partly supplied.**
   - Partial vocabulary exists: claim/warrant/status/gap/conflict/ruling; the OperationProposal→validate→accept→engine-apply pattern (K-DOMAIN-3); immutable snapshots and safe reruns (Ch4 §4.9.3); and the entity-capability table (CF §2.8).
   - No UI, object-model or recovery semantics for co-work inside an application are given. This is a gap for the PRD, not something to inherit.
5. **Decision rights under shared access** can be taken nearly verbatim at purpose level: Ch6 §6.6.2 L243 plus K-AUTH-1, K-DOMAIN-4 ("PASS is structural evidence only"), and "no acceptance in its own voice" (Ch3 L453).
6. **Project-management capability.** §9.3.7 and §4.3.5 offer a PM vocabulary (WBS/dictionary, logic network with blocker vs closure views, document control and decision provenance, front-end definition) and the two human-owned edges.
   - Its standing is owner claim plus UNWARRANTED agent prose, with one observational session.
   - The intended graph projections and BM25+vector search are unbuilt, and their "never authority" constraint is the agent's reading of D-GOV-01.
7. **Evaluation.** The owner-adopted measure (warranted confidence per unit of attention) and Ch9 §9.4.1/§9.4.8 (empirical review study; a second professional outside software) could anchor a v4 evaluation plan. SWBPIPE work is non-software, which fits §9.4.8's call.
8. **An embedded Chirality becomes itself a reviewed tool.** Under APEGA §3.1.2.1 as read in Ch6 L201 and §6.3.3, Chirality embedded in SWBPIPE is part of the tool whose "relevancy and accuracy" the stamping professional must review. The owner's release stance (AT L55–61) bears on this.
9. **Citation discipline for the PRD.** Because the thesis is nonbinding CITED/REVIEWED (README L36–44) and contains the drift listed in §5, the PRD should cite it for purpose-level propositions (P1–P13) and verify any mechanism claim against current governed records before relying on it. The owner-revision backlog `plans/consistency_audit_2026-07-01.md` (README L86) was outside this scope and was not read.
10. **Harness and attention.** The sketch assigns the attention quadrant to "llm + files + tools + instructions" (OW L68). This suggests a natural split: a supplier harness provides attention, and v4's distinctive contribution is the discipline of the tree, graph and network plus the human acceptance and steering edges (FG L26). This division is my reading, not stated by the owner.
