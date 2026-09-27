# Report: what the alignment manuals say about managing human–agent project work, and what v4 could try again

Basis: `main@2b0572fe0`, read-only. No files were changed. Short paths are used below:

- **CV7** = `docs/alignment-manual/Project_Management_for_Human_Agent_Teams_Consolidated_v7.md`
- **FB** = `…/Project_Management_for_Human_Agent_Teams_Field_Book_v1.md`
- **UM3** = `…/CHIRALITY_AGENT_USER_MANUAL_v3.md`
- **REV1** = `…/MANUAL_REVIEW_v1.md`
- **EV/** = `plans/evidence/`

Line numbers refer to those files at this revision.

**What I read:**
- In full: CV7 (all 3,521 lines), FB, UM3, README, REV1.
- Skimmed evidence: the 09-19 theory directory (OWNER_DIRECTION, CLOSEOUT, COHERENCE_REVIEW, SOURCE_RETURN), the 09-22 alignment-manual BRIEF, WORK_GRAPH and project-app-runtime-notes, and the briefs for v4, v5, v7 and the field book. I also read the field book's RECORD and REVIEW, and the v1 source map.
- Outside the listed subject (labelled wherever used): `docs/ai_software_project_management/01_theory.md` and README; `EV/2026-09-19_owner_words_four_graph_structures.md`; the development-loop amendment; `plans/proposals/local-work-graph-loops/README.md`; `projects/chirality-app-dev/instructions/AGENTS.md`.
- Earlier editions (v1, v2, User Manual v1): heading comparisons and targeted passages only.

**Evidence tags:**
- **[D]** described practice
- **[O]** reported by the owner
- **[R]** observed in a cited record
- **[I]** my own inference

---

## 1. Purpose, audience, standing and authorship

**Purpose.** CV7 covers managing projects in which people work with artificial agents to produce a product, "from shared intention through an accepted basis, decomposition, execution definition, detailed development, completion, and delivery" (CV7 44–46).
- Its premise is humanist. Judgment is reserved for people; the agent's work is called "reckoning" (after Brian Cantwell Smith). The agent is treated as an "other" whose work must be examined before anyone relies on it (CV7 50, 75–77, 190–200).
- It adapts Alberta oil-and-gas project practice from the 1970s–2010s: packages and deliverables, the design basis memorandum (DBM), management of change, and project records (CV7 81).

**Audience.**
- CV7: programmers starting to manage delegated work, and engineering project managers meeting agents for the first time (CV7 48).
- FB: an "abbreviated human reference." The owner confirmed that the primary reader is a human working with agents (README table; EV/2026-09-23_field_book/RECORD.md) **[O]**.
- UM3: explicitly agents. It is "an operational companion… for agents developing projects in the Chirality repository" (UM3 5). It is not an end-user guide to the App (see §4).

**Standing.** None of these documents governs work.
- The README says: "Applicable instructions, accepted decisions, and current source records govern actual project work… Reading either manual does not amend those instructions or adopt a new execution basis."
- UM3's status line says it "does not amend instructions, adopt a workflow, activate project work, change a lifecycle state, accept a product, or authorize release" (UM3 7).
- The four roles, six phases and loop are "choices of this manual's approach," to be applied "in proportion to the undertaking" (CV7 64).

**Authorship (owner-signed section, CV7 10–24).**
- The owner, Ryan Tufts, directed the work and chose its purpose, readership and philosophy. "ChatGPT wrote much of the text… Its contribution included developing the argument."
- A separate Codex agent reviewed how the book treats repository practice.
- The owner states: "The preparation of this book does not establish that every practice it describes has been proved effective… Publication is my decision."

The evidence trail confirms a mixed chain **[R]**:
- **v1:** supplied by the owner.
- **v2:** Codex HELP_HUMAN review, with three TASK readers on disjoint ranges (REV1 23–25).
- **v3:** revised externally (ProtonDrive copy plus an external editorial-review PDF; EV/2026-09-22_manual_publication_edit/BRIEF.md).
- **v4:** a Codex publication edit that removed "notes to self." The owner's style direction was: "exemplary technical reference… 1960s and 1970s" (same BRIEF).
- **v5:** added the authorship front matter.
- **v6:** body revised externally.
- **v7:** the v6 body plus the approved authorship section (EV/2026-09-22_manual_v7/BRIEF.md, approved-authorship.md).
- **User Manual v1–v3 and the field book:** drafted by agents and reviewed by independent TASKs.

Acceptance status:
- The evidence briefs repeatedly state that owner direction "does not assert owner acceptance of the resulting text" (EV/2026-09-22_alignment_manual/BRIEF.md) **[R]**.
- For v7, the owner approved the authorship section in chat and directed that it be inserted into his externally revised body (v7 BRIEF) **[R]**.

**Precursor.** `docs/ai_software_project_management/` (09-19) is an agent-authored, non-binding theory draft with eight propositions, P1–P8. Its planned Chirality case study is a "study design, not completed case findings" (README, lines ~18–21; outside subject) **[R]**.

---

## 2. Practice catalogue

Each entry covers:
- (a) the purpose;
- (b) the conditions under which it applies;
- (c) the mechanism;
- (d) evidence of use or results;
- (e) whether it is tied to a past tool, repository layout or engine (historical) or to a lasting purpose.

**P1. Reliance on the work of an "other"; verification versus validation.**
- (a) Receiving an answer does not show that it embodies your intention or was done adequately (CV7 168).
- (b) Always. How much and how deep the examination goes depends on the proposed use and the cost of error (CV7 75, 184–186).
- (c) Plan the examination when the assignment is prepared. Verification checks against stated requirements; validation checks fitness for use. Keep the claim separate from its warrant (grounds). The APEGA "Relying on the Work of Others" standard is the professional analogue (CV7 170–188).
- (d) [D]. APEGA is cited as an external standard, not as evidence that the practice works.
- (e) Purpose-level. Directly relevant to professional engineering tools such as SWBPIPE **[I]**.

**P2. Four roles, types and proportionate delegation.**
- (a) Keep alignment, design, managed execution and bounded contribution recognisable (CV7 321).
- (b) Use only the roles the work needs. A small undertaking need not stand up the whole hierarchy (FB 58; CV7 335–337, table 1807–1810).
- (c) The roles:
  - HELP_HUMAN (Type 0): alignment and continuity.
  - HELPS_HUMANS (Type 1): conception and design.
  - WORKING_ITEMS (Type 1): owns the integrated return.
  - TASK (Type 2): bounded work; does not delegate.
  - Specialisation lives in briefs, context, workflows and tools, never in new roles.
  - Model and reasoning effort are chosen per task, independently of role (CV7 321–341, 1816–1856; §7.3 3261–3271).
- (d) [R]. The manuals' own production used this arrangement: HELP_HUMAN at root, TASK readers, a fresh reviewer, and a WORKING_ITEMS closeout manager as the only Git writer (EV/2026-09-22_alignment_manual/BRIEF.md, WORK_GRAPH.md). The 09-19 theory run dispatched Type 2 directly, with no Type 1 layer, for read-only tasks (OWNER_DIRECTION "Agent 0 execution decision"). Owner's direction: "parallel agent swarms, managed by several Type 1 instances" once ordering is settled (OWNER_DIRECTION "dependencies_and_entry") [O].
- (e) The purpose (who owns integration; executors that do not delegate) is lasting. The role names and the registry ceilings (UM3 138) are historical.

**P3. Steering and recovering intent.**
- (a) The graph shows possible routes but supplies neither priorities nor purpose (CV7 3257).
- (b) Throughout, and especially at 60–90% (CV7 1609, 1667).
- (c) Five subjects of steering: objective and scope; priorities; approach; execution strategy; continuation and decision points (table, CV7 1625–1631). These can be given in ordinary conversation, without node IDs (CV7 1623). Keep the human's words separate from the agent's interpretation (CV7 1619). Ask focused questions only where the answer would materially change the work (CV7 1663; UM3 300).
- (d) [R, O]. The first local-graph draft "assumed a sufficiently defined objective." The owner then "selected **infer and clarify material gaps**" (plans/proposals/local-work-graph-loops/README.md, "What changed after feedback"; outside subject).
- (e) Purpose-level.

**P4. An accepted basis (PRD/DBM), the standing of statements, and open questions.**
- (a) Give participants who were absent from the conversation something definite to work from (CV7 204–218).
- (b) Needed for product formation. Not needed for routine maintenance or repair (CV7 484). Depth should follow novelty and consequence (CV7 220–224, 789).
- (c) Six authoring steps and two human checkpoints: A, direction; B, the identified document (CV7 509–534). Additional mechanisms:
  - Triage what each source is allowed to support (table, CV7 559–565).
  - Keep requirement, assumption, proposal and open question distinct (CV7 721–745).
  - One open-question record per question: the commitment that shapes the answer, the alternatives, the affected work, and the point by which an answer is needed (fig 2.3, CV7 756–783).
  - Six review-finding types: incorrect, unsupported, missing, flattened, outdated, incomplete (CV7 870–877).
  - Bind acceptance to preserved bytes (CV7 930–958).
- (d) [D]. The software-PRD procedure "remained a proposal awaiting adoption and examination in use" (CV7 18). No `software-prd` workflow is registered (UM3 209).
- (e) The purpose is lasting. The checkpoint ceremony should be tested for proportion.

**P5. Decomposition and the production contract.**
- (a) Give each obligation one accountable home, and give each deliverable a result that can be assessed (CV7 1019–1021).
- (b) FEED, before production (CV7 265–275). For small, reversible work the three checkpoints may be combined into one (CV7 1189).
- (c) Mechanisms:
  - Scope items: included, excluded or unresolved; one package home each (CV7 1041–1085).
  - Context Envelope sizing, S/M/L/XL (CV7 1119–1130).
  - A scope ledger read in both directions (CV7 1144–1150).
  - Scope of Work with an Output and Evaluation Matrix: one row per identical method set (CV7 1321–1352).
  - Excluded acts must each have a named owner (CV7 1356–1364).
  - Claim-granularity tests: would changing the claim require a decision; does anything else depend on it; can named verification check it (CV7 1305, 2644).
- (d) [R]. The Scope of Work standard and ID catalogue exist and have tools (UM3 229–262). Effectiveness is not reported.
- (e) The purposes (one home; criterion–method pairing; excluded-act ownership) are lasting. The file formats (`SOW_V1` front matter, the `REQ-017` three-digit IDs, the `_CONTEXT.md` fileset; UM3 221, 235–248) are historical.

**P6. Dependencies, the project DAG, and resolving cycles.**
- (a) Establish production order and find coupled decisions early (CV7 1023).
- (b) Toward the 30% gate; revise on material change, not because a new session started (CV7 1582–1590).
- (c) Mechanisms:
  - Fix the graph's objective and edge meaning (CV7 1410).
  - Two extraction passes (CV7 1436).
  - Check coverage before topology (CV7 1476–1486).
  - SCC condensation for diagnosis only (CV7 1494–1496).
  - Four resolution moves: decompose, invert, merge, cut. Merge and cut are human-gated (CV7 1500–1508).
  - An unresolved cycle cannot establish readiness (CV7 1539).
  - Warnings: "An acyclic selection can still be incomplete" (FB 124). Do not claim a critical path from an unweighted graph (CV7 2514).
- (d) [O]. Owner: dependencies are "mapped from the original PRD through decomposition and scopes of work… Then through resolution or dissolution of SCCs the DAG is formed" (OWNER_DIRECTION). There is no reported measure of outcomes.
- (e) The analysis purpose is lasting. The `Dependencies.csv` v3.1 columns and DepClosure snapshots (UM3 278–292) are historical.

**P7. The phased route with human stage gates.**
- (a) Change what the project is organised to establish as it matures (CV7 244).
- (b) New product development. Existing projects enter at their verified position (FB 5; UM3 180).
- (c) Conceptual → FEED → 30% (initial DAG) → 60% (no further structural change expected) → 90% (produced deliverables, then testing and debugging) → 100% (delivery) (CV7 248–255; FB 33–40). Percentages are positions, not effort measures (CV7 257). Maturity may be uneven across the project (CV7 309–315). A gate is a human judgment presented as "established / unresolved / relied upon / proposed" (FB 44).
- (d) [O]. The owner's engineering-execution model (CV7 246). No record in the repository shows the gates being run on a software project.
- (e) The purpose (the character of the work changes; gates are human) is lasting. The percentage vocabulary is domain-specific **[I]**.

**P8. Local work graph and the six-step loop.**
- (a) Carry one undertaking across sessions and agents without relying on a single uninterrupted context (CV7 2356).
- (b) After the DAG exists. Before that, the owner-directed cycle-resolution work comes first (CV7 1719). Owner: in early phases "loops are not the right agent meta-workflow… an Agent 0 working closely with the human" (OWNER_DIRECTION) **[O]**.
- (c) The six steps: orient and recover; construct or revise; advance ready work; execute and verify; close the records; complete. Each node carries a result, prerequisites, write boundary, completion check, and state with evidence or blocker (CV7 419–458, 1733–1786; fig 4.3). One maintainer integrates updates to the graph (CV7 1782).
- (d) [R]. The App and Piping loops adopted this through the 09-22 amendment (UM3 64–76). Both loop headers read "none selected for a successor undertaking" (UM3 72, 102). No post-adoption performance record is cited.
- (e) The purpose is lasting. The exact path `execution/_Coordination/WorkGraphs/<undertaking>/WORK_GRAPH.md`, LOOP_INIT pointers and PR-merge terminus (CV7 1676, 1780–1784) are historical.

**P9. Bounded briefs and effective permissions.**
- (a) Give the executor enough purpose to make choices, and enough boundary not to invent authority (UM3 344).
- (b) Every delegation. A small read-only task can use the launch message itself as the brief (CV7 1919).
- (c) A brief carries: purpose, basis, context, authority and tools, write scope, and return (FB 163–170; fig 4.5). Preserve the brief as supplied. Record the actual parentage and mechanism. Effective permission is the intersection of host, role, method and brief (CV7 1921–1962). "Claim sandbox enforcement only for a boundary the host actually enforces" (CV7 1958).
- (d) [R]. Every evidence brief records that role and write limits were "instruction-based… not a claimed per-agent filesystem sandbox" on hosts with unrestricted access (alignment BRIEF; publication-edit BRIEF; field-book RECORD).
- (e) Purpose-level. The mechanism depends on the harness.

**P10. Parallel work.**
- (a) Parallel work is useful only if the contributions can be combined (CV7 1968).
- (b) When inputs are settled and writes and resources can be separated (CV7 1978, 2479–2483).
- (c) Three relationships to check: technical dependence, write ownership, resource use. This includes a shared desktop, pointer and focus under Computer Use (CV7 1970, 2483). Findings pass through the parent with their standing intact (CV7 1984–2009). Concurrency is limited by review and integration capacity (CV7 1864, 2516–2524). Diagnose waiting work by its cause (CV7 2512).
- (d) [D]. Figures are constructed. The 09-22 manual production used disjoint reading ranges [R].
- (e) Purpose-level.

**P11. Examination, evidence and independent review.**
- (a) A passing check must mean what it claims (CV7 2173).
- (b) Every mergeable slice. Exercise connected and native routes as soon as they work (CV7 2111–2125).
- (c) Mechanisms:
  - Keep outcome kinds distinct: failed, blocked, unavailable, skipped, interrupted (CV7 2145).
  - Bind evidence to the candidate (CV7 2135–2141).
  - Protect criteria and oracles during repair (CV7 2167–2173).
  - Independent review of a frozen diff with backchecks. A same-model reviewer adds no model diversity (CV7 2163–2197, 854).
  - Agent-operated testing (Computer Use) with a controlled starting state (CV7 3005–3060). It does not replace practitioner validation (CV7 3066).
- (d) [R]. In the 09-19 theory run, a parent inspection caught a source-check TASK citing incorrect headings (COHERENCE_REVIEW "Source fan-in"; SOURCE_RETURN items 8–9). Visual HTML review "NOT VERIFIED" because of tool-policy limits (alignment WORK_GRAPH; field-book REVIEW).
- (e) Purpose-level. `HOST_RERUN_REQUIRED` and the App check IDs (UM3 394, 536) are historical.

**P12. Decision packages and human acts.**
- (a) Spend human attention on real choices (CV7 3237, 3305).
- (b) Consequential or reserved decisions only. Routine work goes ahead (UM3 47).
- (c) Present the issue, grounds, alternatives, recommendation and effects. "Name the actual act requested… Do not smuggle several different acts into a generic 'approve'" (UM3 449). Silence is not a ruling (CV7 2045). An agent may transcribe a human act but cannot originate it (CV7 958). Resolve a shared question once for all affected cases (CV7 2578, 2814).
- (d) [R]. The owner's actual acceptance of the development-loop amendment was "this is approved. You can continue with your plan," bound by the agent to a hashed package (AMENDMENT_2026-09-22…md; outside subject).
- (e) Purpose-level.

**P13. Change, amendment and propagation.**
- (a) Revise without restarting; preserve the reasons behind changes (CV7 3255).
- (b) When accepted scope or an interface changes (FB 243).
- (c) Present three subjects together: the change and its impact; the exact amendment and propagation plan; the independently examined resulting state (CV7 1003, 2055). Reopen only the decisions that are affected (CV7 357; FB 248). Keep a local repair separate from a scope change (CV7 3491).
- (d) [D]. Constructed (Appendix A.6).
- (e) Purpose-level. The `scope-change` package and "D-" numbering are historical.

**P14. Closeout of records and run memory.**
- (a) Keep commitments, work and evidence in agreement (CV7 2376).
- (b) v7: once per undertaking, after implementation and evidence are integrated, before the final PR (CV7 454, 1745, 2776). v2 instead said "Reconcile continuously and at meaningful boundaries" (v2 §5.8 heading; v1 line 3040: "can proceed beside independent implementation").
- (c) Compare in both directions (commitment to result, result to commitment), classify each difference, and make the warranted edits (CV7 2247–2287). Add a terse MEMORY Runs row (CV7 2722).
- (d) [R]. The cadence was changed by an owner-accepted amendment on 09-22 (UM3 66–68; AMENDMENT). Owner "retrospective run feedback" described "uneven record drift, mechanism-level claims, incomplete decision propagation, missing evidence for off-code events, variation in agent verdicts." The underlying ledgers were not supplied, and the citation was removed from the published text (v1 3046, 3466; EV/2026-09-22_manual_publication_edit/editor-original-source-mapping.md, around line 231) [O].
- (e) The purpose is lasting. The cadence tied to PRs and the MEMORY.md format are historical.

**P15. Remaining obligations and deferred work.**
- (a) An unmet obligation must not disappear (CV7 2706).
- (b) Last resort only: when there is no graph home and no identified successor (CV7 2674).
- (c) Record the affected commitment, why it could not be allocated, the needed owner or precursor, and a checkable condition for reconsideration (CV7 2676–2694). Deferral grants no acceptance and no scope reduction.
- (d) [R]. The earlier standing Task Management sweep was narrowed to conditional intake (UM3 457–514; guide-source-comparison.md).
- (e) The purpose is lasting. Federation, harvest modes and Remaining retirement are historical.

**P16. Continuity, handoff and interruption recovery.**
- (a) Actual state and recorded state diverge (CV7 228–232).
- (b) At every entry and after every interruption.
- (c) Compare the record with branches, worktrees, unmerged work and evidence. Confirm earlier workers have stopped, or transfer ownership. A handoff is only for facts the graph lacks (CV7 436, 1707–1715, 2301–2305). UM3 gives a "useful first return" template (UM3 106).
- (d) [R]. Project entry notes list many stale pointers and dated assertions that agents must reconcile (project-app-runtime-notes.md §4).
- (e) Purpose-level. The Git-centred mechanics are historical in form.

**P17. Completion judgment, product examination and delivery.**
- (a) Keep completion, formal checking, acceptance and publication distinct (FB 229).
- (b) From 90% through 100%.
- (c) Three coverages: scope, relationships, evaluation (CV7 2842–2848; FB 211–215). "An empty graph… does not establish that coverage" (CV7 2882). Freeze claims during formal checking (CV7 2890). Handover names the result, basis, permitted use, limits, next owner and means of recovery (FB 261).
- (d) [D]. Appendix A is constructed.
- (e) Purpose-level.

**P18. Reducing the recurring cost of the loop.**
- (a) Cut repeated agent work (CV7 2530).
- (b) Over long horizons.
- (c) Use tools for defined operations, with a table of what the tool contributes versus what still needs examination (CV7 2538–2544). Calibrate on a varied sample before scaling (CV7 2564–2572). Suggested measures: elapsed time to integration, spend, wait by input type, review and correction effort (CV7 2580). "Do not convert a single run's capacity limit… into a permanent staffing rule" (CV7 2572).
- (d) [D]. "Tool availability, qualification, and savings remain unverified" (v1 source [14], via editor-original-source-mapping.md).
- (e) Purpose-level.

**P19. Notices between loops and adoption boundaries.**
- (a) Propagate a shared change without overwriting another loop's basis.
- (b) A monorepo with pinned sibling loops.
- (c) "A notice communicates a change; the receiver decides adoption" (UM3 455; Root AGENTS).
- (d) [R]. Runtime and PEC did not adopt the v7 route (UM3 74, 579, 610).
- (e) The purpose (receiver-owned adoption) is lasting. The pins, mirrors and receipts are historical.

**Estimation and risk: what is absent.**
- The manuals give no scheduling, duration, estimation or risk-register practice. Risk appears only as depth of examination scaled to consequence (CV7 184), the risk carried by an open question (CV7 224, 789), and a warning against inferring a critical path (CV7 2514).
- "A dependency graph is also not automatically a schedule" (UM3 223).
- This is a gap for v4 project-management capabilities **[I]**.

---

## 3. Project-management needs specific to coordinating many agents

The manuals themselves identify these needs. Mapping them to v4 is **[I]**.

1. **More returns than can be examined.** "Review and integration capacity constrain useful concurrency"; returns waiting for examination "remain unfinished project work" (CV7 1864, 2518). The useful measure is "the rate at which required, examined contributions become available… Counts of running agents or closed nodes describe activity" (CV7 2524).
2. **Integration nobody was assigned.** Otherwise "the human receives separate completions and must reconstruct an integration assignment that nobody was given" (CV7 333). The remedy is a named integration owner in the original arrangement (CV7 1980).
3. **Collisions from concurrency.** Technical dependence, write ownership and resource use (CV7 1970). Disjoint files can still embody incompatible assumptions (CV7 1976). Generated indexes, test databases and application windows need care, and Computer Use on a shared desktop needs coordination with the human at that machine (CV7 2483).
4. **Divergent interpretations across parallel workers.** Three contributions built on three readings of one open question (CV7 791). The remedies are an open-question record carried through briefs (CV7 791) and a named shared question ruled on once (CV7 2578, 2814).
5. **Context limits.** Context Envelope sizing (CV7 1117–1130); focused context rather than whole-history copies (CV7 1917); replacing a manager whose context "has become too broad" after preserving its state (CV7 2572); graphs that carry work "without relying on the uninterrupted context of one agent" (CV7 2356).
6. **Continuity across instances.** Confirm that earlier workers have stopped before reassigning (CV7 436, 1709). An edited file does not prove that a running child received an amendment (CV7 2009; UM3 354).
7. **Volume of evidence and records.** The graph should "explain the next action without becoming a second archive" (CV7 462). Give each kind of information one maintained home (CV7 2722). Keep child returns verbatim and separate from the parent's conclusions (CV7 2157).
8. **Drift.** Records drift unevenly when long delivery runs lack maintenance (CV7 2784) [O-derived, via v1 3046]. Stale derived indexes can be mistaken for authority (CV7 2550). Claim granularity reduces the churn refactors cause (CV7 2648).
9. **Repeated failed attempts.** "Several repeated attempts with no new evidence suggest that the diagnosis or division of work needs reconsideration" (CV7 2019, 3082).
10. **Calibration before scale-out.** "Agreement between workers is useful evidence about repeatability; both can still share an unsupported interpretation" (CV7 2568).
11. **Human attention as the binding constraint.** Prepared, grouped decisions (CV7 534, 3305). The owner-endorsed aim: "how much warranted confidence it produces per unit of your attention" (EV/2026-09-19_owner_words_four_graph_structures.md; outside subject) **[O]**.
12. **Execution provenance.** Record the actual model, harness, parentage and substitutions (CV7 1854, 1956). A brief being written is a different fact from a child actually running (UM3 54).
13. **Multiple parallel loops.** Changes are propagated by notice and adopted by the receiver (UM3 455). This is also the source of much of the observed friction (§5).

---

## 4. What User Manual v3 says about day-to-day use

**It is not an App end-user manual.**
- It is written for agents developing inside the Chirality repository (UM3 5).
- Its references to the App user interface are limited to:
  - workflow drafts, which "the human inspects… requests changes in chat, and registers the reviewed bytes through the Workflows panel" (UM3 651);
  - a note that `instructions/AGENTS.md` is "the guidance shipped to App users" (UM3 520).
- Most of UM3 covers entry recipes, file formats, CLI tools and per-project adoption boundaries for App, Piping, Runtime and PEC (UM3 518–610).
- **Gap:** the manuals describe no day-to-day panels, sessions, recovery user interface or App interaction flows. Flag this for v4.

**Interaction patterns worth keeping [I on value]:**
- **Three proportionality questions:** what decision or operation is next; what could make its result unusable; what must another participant recover (UM3 41–47).
- **Four distinctions:** description versus authority; preparation versus execution; evidence versus acceptance; integration versus release (UM3 49–56).
- **A "useful first return" on entry:** "The selected undertaking is X, based on Y. The working tree contains Z. A is ready…; B waits for the named owner act" (UM3 106). This is a compact shared-state summary.
- **Naming the requested act** rather than asking for a generic "approve"; attaching the proposed artifact (UM3 449).
- **Honest reports of partial results.** "Implementation and focused regression checks complete; native recovery witness remains" (UM3 197; example at 700–702).
- **The draft → inspect → chat feedback → Register workflow loop,** without silently registering or running anything (UM3 651). This is an existing embedded pattern for human-controlled creation of methods.
- **An applied example of human-control user interface in CV7:** in the editor example, a proposal is bound to a source revision; rejecting it leaves live state untouched; a stale proposal is refused with a reason and a fresh one offered (CV7 94–124, 598–600, 1881; Appendix A). CV7 5.12 adds that the user needs to know "which input produced a result, whether it remains current, and what will be changed by accepting it" (CV7 3041). Also: "A technically correct intermediate calculation can still be difficult to use if its input basis or result status cannot be understood" (CV7 2999).

**App-shipped guidance** (outside subject; `projects/chirality-app-dev/instructions/AGENTS.md`, about 1,100 words) is a lightweight version of the same doctrine:
- "Ordinary conversation is sufficient for many requests";
- "without manufacturing additional approval ceremonies";
- "Keep the experience simple… Judge progress by the usefulness of the result" (lines 46–62, 89–103, 140–145).

**Friction reported or observed:**
- Agents must work through stale launchers, graph blocker strings that are out of date, dated authority-corpus claims, a Node version mismatch, Runtime status headers that cannot express retirement ("lifecycle vocabulary has no retirement state"), and pointers that under-describe accepted changes (project-app-runtime-notes.md §2 and the §4 "Trap" table) **[R]**.
- UM3 needs a separate adoption-boundary table because the v7 route applies only to App and Piping (UM3 64–76) **[R]**.
- HELP_HUMAN's registry ceiling is `write_scope: none`, so continuity writes must be routed through others (UM3 138). Yet the native root sessions recorded as HELP_HUMAN did write the setup files, the field book and the evidence (alignment BRIEF: "native parent performed setup writes"; field-book RECORD) **[R]**. My reading is that the declared ceiling and native practice diverge **[I]**.
- Browser visual inspection was repeatedly unavailable under tool policy (field-book RECORD; alignment WORK_GRAPH) **[R]**.

---

## 5. Tensions, overheads, failure modes and disagreements

**Cautions the manuals record themselves:**
- **Forms displacing the product:** "A project can become occupied with maintaining its forms while the product and its use receive too little attention… A repeated report that serves no decision, dependency, recovery, or examination should be questioned" (CV7 3289).
- **Structures must earn their cost:** "Its structures should continue to earn their cost… Its controls should preserve consequential distinctions without multiplying empty ceremony" (CV7 3321).
- **Benefits are expectations, not results:** "These are reasoned expectations to examine in use… do not establish a fixed productivity gain" (CV7 3307).
- **Theory precursor:**
  - P7: "More documentation can worsen reconstruction if it multiplies contradictory entry points or hides the operative basis among historical copies."
  - P8: "Process earns its cost by improving the work or its assessability."
  - The case study must allow the finding that "a proposed discipline added ceremony without improving the work" (01_theory.md P7, P8, §12; outside subject).
- **Guards against review theatre:**
  - "A count of requirements does not show that the right behaviours were specified" (CV7 858).
  - "Before adding another complete pass, identify what it would establish" (CV7 2808).
  - A same-model reviewer "supplies no model diversity" (CV7 854, 2181).
- **Guards against approval ceremony:** "Do not manufacture a new permission ceremony" (UM3 348); approval of every routine act "would consume the attention needed for choices that determine the product" (CV7 3237).
- **Guards against misleading proxies:** percentages misread as effort (CV7 257); an empty queue or acyclic graph taken as completion (CV7 311, 385, 2882); deferral used to hide an unmet obligation (CV7 2706).

**Overheads observed in the manuals' own production [R]:**
- Evidence directories: the v4 publication edit has 68 files (1.5 MB); the alignment review 45 files (888 KB); the v7 production, which replaced only the authorship section plus the User Manual update, 27 files (632 KB); the field book 3 files (16 KB).
- The owner asked for an abridgment of CV7 (69k words) into a 2.6k-word field book "omitting justification and elaboration" (field-book RECORD) **[O]**.
- UM3 repeats adoption and standing caveats in nearly every section.
- The project-entry notes show P7's failure mode in practice: multiple contradictory entry points, with the operative basis buried among historical copies (project-app-runtime-notes.md §4).

**Where the manuals disagree:**
1. **Reconciliation cadence.** v1/v2 said reconcile "continuously and at meaningful boundaries," beside implementation. v7 says one planned closeout per undertaking, which "does not recur after each ordinary graph node" (CV7 1745). v7 keeps the drift warning (CV7 2784), relying on "preserve the relationship at the time it changes" (CV7 2786).
2. **General versus repository-specific.** The README separates general practice (CV7) from repository procedure (UM3). Yet CV7 embeds the exact repository path, LOOP_INIT, MEMORY.md, Task Management and "merge the final PR" (CV7 430, 1676, 1780–1784, 2722, 3297). The FB is more generic ("In a software undertaking using pull requests," FB 199).
3. **Scope of the loop.** CV7 presents one development loop. UM3 says Runtime and PEC keep receipts and Remaining-based selection (UM3 74, 104, 610). The published practice is not uniformly in use.
4. **Thesis overstatements.** The source check flagged "eliminates," "architecturally enforced," "fully explicit" and "fully auditable" as exceeding the bounded account. It also found that thesis §3.2.3 conflicts with direct Type 0 → Type 2 dispatch (SOURCE_RETURN items 7, 8, 12 and closing). CV7 avoids these claims.
5. **The PRD procedure.** It is described in detail (CV7 ch. 2) but has not been adopted (CV7 18; UM3 209).
6. **Terminology.** Role files use "judgment" in its ordinary sense, while CV7 reserves the word for humans (UM3 733).

**Enforcement gap [R]:** every evidence brief records that role, write and non-delegation limits are asserted by instruction on hosts with broad permissions. CV7 1958 and UM3 140 require that this be disclosed. The governance model therefore relies on compliance rather than enforcement **[I]**.

**Evidence of effectiveness [R]:**
- No project record cites CV7, the FB or UM3 as a working basis after publication. A search at `2b0572fe0` found references only in the manual folder, tranche manifests, the root README and the current v4 successor note.
- The owner's retrospective accounts were not supplied for reconstruction.
- REV1 84 recommends a separate empirical study if claims of effectiveness are wanted.

---

## 6. Candidates for v4 — all [I]

**Worth trying again, each with the feedback that would show whether it helps:**

1. **A proposal/live-state contract for agent changes inside host apps** (CV7 editor example; 1881; 3041). Proposals are bound to a source revision; rejecting leaves live state untouched; stale proposals are refused with a reason; apply is explicit.
   - Feedback: engineers in SWBPIPE sessions can say, before applying, what apply will change; count incidents of lost or overwritten work, and stale applies.
2. **Visible standing for statements** (observation, assumption, proposal, decision, open question) on the objects the human sees (CV7 721–745; UM3 49–56).
   - Feedback: rate of "flattened" findings in review (CV7 874); cases where the human mistook a proposal for a decision.
3. **Decision packages that name the act** and bind it to an identified candidate; silence is not a ruling (UM3 449; CV7 930–958).
   - Feedback: owner time per decision; decisions reopened because the referent or scope was ambiguous.
4. **Proportionate delegation:** only the roles needed, Type 2 does not delegate, a named integration owner (FB 58; CV7 333, 1980).
   - Feedback: unowned integration defects; rework caused by returns that could not be assessed.
5. **Concurrency governed by review and integration capacity,** with waiting work diagnosed by cause (CV7 1864, 2512–2524).
   - Feedback: backlog of unexamined returns; time to examined result versus number of agents.
6. **Recovering against actual state, plus a "useful first return"** (CV7 436; UM3 106).
   - Feedback: duplicated work or clobbered resources after interruption; time to resume.
7. **Candidate-bound evidence with explicit outcome kinds; protected criteria; independent review of a frozen candidate** (CV7 2135–2197).
   - Feedback: claims later found to rest on stale evidence; false repairs caught; defects that escaped review.
8. **Open-question records carried through briefs; shared questions ruled on once** (CV7 756–791, 2578).
   - Feedback: incompatible interpretations found at integration.
9. **Claim-granularity tests** for maintained commitments (CV7 2644).
   - Feedback: reconciliation churn caused by refactors.
10. **Verification versus validation, with practitioner examination kept distinct from agent-operated tests; source admission for engineering knowledge.** Examples: the APEGA reliance standard (CV7 170–188), and Piping's rule that unreviewed OCR equations "may not supply authoritative equations" (UM3 554).
    - Feedback: issues practitioners find after agent passes; the provenance of equations and limits the agent used.
11. **Calibration before scale-out** (CV7 2564–2572).
    - Feedback: rework rate after scale-out compared with before.
12. **"Warranted confidence per unit of attention" as a design aim, not a metric** [O source].
    - Feedback: routine prompts versus consequential prompts per session.
13. **Estimation and risk as a gap to fill,** since the manuals are silent on both.
    - Feedback: whether coordinating many agents creates questions about schedule or risk that the owner actually asks.

**Historical mechanisms to set aside, with reasons:**

- **Repository file layouts and formats:** the WorkGraphs path, LOOP_INIT, `_STATUS/_CONTEXT/_REFERENCES`, `SOW_V1` IDs, `Dependencies.csv` v3.1 columns, MEMORY Runs rows. They are tied to a file-carried monorepo; v4 embedded apps will have their own object models. Keep the purposes (one home for each information type; stable identities).
- **The machinery of pins, adoption, receipts and mirrors across sibling loops:** D-GOV numbering, authority corpora, the PEC and App hold CLIs, per-iteration receipts. These produce the observed stale-pointer and dated-assertion friction (project notes §4). Keep receiver-owned adoption as a principle only.
- **Task Management federation and harvest modes; formal corpus concordance** (R6 multiset equality, migration profiles; UM3 441, 477–514). These are heavy mechanisms for repairing an accumulated corpus. Keep last-resort handling of unallocated obligations and claim-level comparison.
- **Git and PR merge as the completion terminus** (CV7 430, 3297). This is specific to software repositories; completion in an engineering app is a different act.
- **Engine- and host-specific statements:** the Codex-only MVP, stock Codex App Server, `delegate_agent` versus native descendants (UM3 140, 538). v4 has no chosen supplier.
- **Instruction-asserted role ceilings and per-file hashing manifests** as the main provenance mechanism. The purpose (reconstruct what was supplied and done) is sound. The observed evidence volume suggests preferring traces native to the harness and permissions the host enforces.
- **The six-phase percentage gates as a mandatory frame for embedded workflows.** They are purpose-level for large projects but should be optional orientation (CV7 64 already says "choices of this approach"). Test whether they help inside SWBPIPE-scale work.

---

## 7. Gaps and limits

- I did not read the full earlier editions (v1, v2, v4, v5); I compared headings and targeted passages. v3 and v6 exist only outside the repository.
- I did not read the evidence JSON files, the three chapter reviews in full, or the thesis.
- The owner's retrospective run accounts, the original ZIP source bundles and the external editorial-review PDF were not available.
- There is no empirical record of the manuals' practices improving outcomes. Evidence of use consists of their application in producing the manuals themselves and in the loops' adopted instructions.
- The 09-19 Chirality case study was never carried out.
- UM3 gives little on how a person uses the App; `instructions/AGENTS.md` was read only because it is short. Actual App user-interface behaviour (panels, sessions, recovery) is not established by these sources.
