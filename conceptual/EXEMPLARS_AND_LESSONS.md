# Exemplars and lessons — first cut

Standing: **interpretation (agent).** HELPS_HUMANS's synthesis of the
first reading of the reference (Stage B). Each entry names its sources and
their evidence standing; the "stance" in each entry is a **proposal** for
discussion, not a v4 requirement. Revised as the conversation proceeds.

Sources are paths at the investigation revision `2b0572fe0` unless marked
`ORIG/` (the original checkout's Git-ignored archives). `T1`–`T6` are the
preserved TASK returns in the run record
([`tasks/`](../execution/_Coordination/AgentRuns/V4-CONCEPT-20260925/tasks/)),
which cite line-level locations. Evidence labels: **owner** (the owner's
recorded words), **executed** (a recorded run or check), **implemented**
(code exists), **described** (documented design), **unrealised** (intended,
never built), **inference** (agent reading).

## 1. What the owner has said the product is for

Read together, the owner's own words across the last two months describe one
product with a consistent nucleus. The v4 brief moves its centre of gravity
into host applications.

| Date | Owner's words | Source |
|---|---|---|
| 2026-08-01 | "The practice of harnessing agents with capabilities far beyond humans, but lacking the accountability of human judgment, and doing so at scale, reliably, is my bedrock for the future of professional work." Build-time versus run-time asymmetry: "Operational Piping will NOT be approvals-heavy: agents will have near-parity autonomy with human users except at certain prescribed workflow gates. The heavy governance exists for the BUILD." "My product is as someone who can use the tool to do the thing." | `plans/evidence/2026-08-01_accountability_thesis.md` §1 (recorded "as close to the owner's words as fidelity allows") |
| 2026-08-02 | Approved "two delivery targets: the standalone Chirality Desktop app and a per-domain control-plane target" and "domain-specific applications as the primary delivery vehicle for the agents" | `projects/chirality-app-dev/execution/_Coordination/_DECISIONS/D-APP-87_RULING_…_2026-08-02.md` |
| 2026-09-11 | "This is a tool to give the Codex agents to the user for planning work, and using and creating workflows that can be used again and iterated over. … I need to have the Codex agents in their full glory, so to speak. There should not be any limits on tool use or the useful features that come baked in to the Codex agents." | `plans/steers/chirality_app_v3_codex_host_replatform_direction_2026-09-11.md` |
| 2026-09-12 | "the same agents and agent server is intended to be imbedded in subsequent applications from Chirality, like the SWBPIPE … and I want to be able to integrate local models with Codex" | same steer, topology decision |
| 2026-09-12 | "Chirality helps people direct and validate knowledge work. Its core experience should be simple: plan your work, execute it, save useful methods as workflows, reuse them, and iterate. Mastery comes from learning to direct and validate increasingly demanding work while remaining able to take responsibility for the results." "Codex should provide the agent capabilities. Chirality contributes the conversational interface, four role relationships, reusable workflows, inspectable plans and useful access to artifacts." | `projects/chirality-app-dev/execution/_Coordination/AgentRuns/APP_V3_CODEX_HOST_REPLATFORM_20260912/PERSPECTIVE.md` (owner's note, drafted with the reviewer, reproduced verbatim) |
| 2026-09-17 | "A surface on which humans and agents can collaborate, but the human should not feel demoted in any way or part of the process. So the app is built around the human's needs, with the agent being able to take equivalent action at the direction of the human." | `projects/chirality-piping/execution/_Coordination/AgentRuns/HELP-HUMAN-PIPING-20260916-UI-DESIGN-PROGRAM/instances/ROOT/DIRECTION_DECISION_2026-09-17.md` §1.1 (hash-bound transcription) |
| 2026-09-19 | The four structures (tree, production graph, network, attention) are "the stable graph structures that underlie knowledge work as-such"; quality as "how much warranted confidence it produces per unit of your attention" (an agent sentence the owner adopted) | `plans/evidence/2026-09-19_owner_words_four_graph_structures.md` |
| 2026-09-20 | "we need to work on those dynamic tools now. They will be application specific. SWBPIPE is the first app to receive tools" | `projects/chirality-runtime/execution/_Coordination/AgentRuns/APPLICATION_DYNAMIC_TOOLS_20260920/PLAN.md` |

**Inference.** The v3 nucleus (direct and validate knowledge work; plan →
execute → save → reuse → iterate) survives into v4 unchanged in purpose. What
changes is *where* it lives: inside the applications where the work's objects
are, with the agent acting through the same means as the human on those
objects, and the standalone app becoming one host among several — the one
where methods are made.

## 2. Exemplars — directing and validating work

**X-01 Plan → execute → save → reuse → iterate.**
Activity: shaping an uncertain intention into done work and a reusable method.
Mechanism in v3: native plan revisions with history; execute a specific
revision; "Turn into workflow"; reuse with new inputs. Evidence: v3 checks
S-1, S-3, S-4 and a journey reusing a saved workflow over three cycles
(**executed**, T3 §2, §6 E1); v3.0.1 release notes ("based on the first days
of real work"). Limits: the journeys used fictional office work; no
engineering work was exercised; plan mode relies on an experimental harness
field. Lost if removed: the product's stated core experience. Stance: **keep
the purpose; re-express it inside hosts** (a workflow run in SWBPIPE is the
same loop on engineering objects).

**X-02 Conversational workflow authoring, human registration.**
Draft through conversation → inspect and discuss → explicit, non-overwriting
registration; source-qualified identity (project, user, bundled) and no silent
rebinding. Evidence: PR #786 (**implemented**, controlled test; native for
3.0.0 saving, T3); Root `AGENTS.md` "Skills and workflows". Lost if removed:
either workflows become runnable without review, or authors lose the
conversational route. Stance: **keep**; decide whether v4 workflows gain
structure (see Q-03).

**X-03 Execution, observation, interruption and shutdown kept distinct.**
Losing a window stops observation, not work; Stop is explicit; reconnection
recovers actual state and outstanding decisions; outcome states include
"Outcome unknown". Evidence: window-disconnect and SIGSTOP checks
(**executed**, `APP_V3_CODEX_HOST_REPLATFORM_20260912/RUN_LOG.md`; T3 E3).
Counterexample: the earlier daemon killed quiet turns after ~30 s (R17-F2).
Stance: **keep as a product-level contract** — it is the recovery half of
"shared understanding of state and recovery" (OD-05).

**X-04 Every agent request is answered; approval is never implied.**
Request cards for approvals, questions and elicitations; session scope only
when offered; unknown requests get an explicit error. Evidence: denied-then-
renewed approval journey (**executed**, T3 E4). Stance: **keep**.

**X-05 Truthful projection of agent activity.**
Only observed events are shown; missing results stay unknown; model and
instruction digest recorded per turn. Evidence: **implemented / executed**
(T3 E8). Stance: **keep**; it generalises to "no claim of completion or
acceptance the record cannot support".

**X-06 Editable, inspectable product guidance with four roles.**
Shipped default, user copy that survives updates, restore; guidance is
additive to the harness's own instructions; roles are relationships, not
engines. Evidence: **implemented / executed** (T3 E9); four-role adoption
D-GOV-42. Limit: role limits are asserted by instruction only (T2 P9, T3 §3.4).
Stance: **keep the purpose; question whether all four roles are product
concepts or development-method concepts** (Q-09).

## 3. Exemplars — agents inside host applications

**X-07 SWBPIPE's collaborative surface: equivalent action, visible and checkable.**
Owner direction (2026-09-17, above): the tables are the model; every action
either party takes is a row operation through one applier route; agent
proposals land as marked rows and cells with old and new values; acceptance
row by row, multi-row, or whole batch; every row and cell carries its origin;
a human "checked" tag that lapses when the row changes; the agent checks the
engineer's work by attaching feedback without altering the tables; "no
agent-private surface". Evidence: **owner** (confirmed direction record);
applier route, `author_type: agent`, atomic batches and stale-basis rejection
are **implemented**; row-level acceptance UI and Review-page agent cards are
**unrealised** (T6 §2–4). Stance: **adopt as the reference pattern for
semantic parity in hosts** — the clearest statement anywhere in the corpus of
what OD-05 means in practice.

**X-08 Application-owned tools with proposal-only domain actions.**
The host registers typed tools (inspect selection, preview operations, submit
proposal, get proposal status); the agent never applies; the human applies
through the host's own controller; every call binds to a basis (workspace
generation, identity, revision, canonical model hash); stale proposals are
refused; `success` means "the tool ran", not "accepted". Evidence:
Runtime `docs/APPLICATION_TOOLS.md` (**implemented**, controlled tests, 401
Runtime tests; offline probe); SWBPIPE live-control branch
`origin/codex/piping-live-control-20260924` (**implemented, unmerged**; native
and human witnesses open). No live model turn has exercised either (T5 §1.3,
T6 §3c–d). Supplier constraint observed: the incumbent harness accepts tool
catalogs only when a conversation starts. Stance: **adopt the contract shape
as the host integration core; prove it live early.**

**X-09 The domain-engine boundary.**
Hosts own domain truth; agents propose; deterministic tools and engines
compute; humans rule. "Validation passed" is structural evidence only;
profiles list claims agents must not make ("certified", "code compliant").
Evidence: thesis App. A K-DOMAIN-1..4 and Ch. 4 §4.10 (**described**);
`_DomainEngines/profiles/open_pipe_stress.yaml` (**described**, adopted at
manual-bridge level); SWBPIPE `docs/PROFESSIONAL_BOUNDARY.md` (**accepted
requirement** in that project). Stance: **keep** — it survives the move from
enclosure to embedding (T1 §7.1).

**X-10 Typed tools inside the host; computer use for tools without an interface.**
The owner's plan for the first external-prover validation loop: the agent
controls SWBPIPE through typed tools and a third-party Windows program through
computer use. Evidence: **owner** (`…/OWNER_MVP_AGENT_CORRECTION_2026-09-20.md`,
`…/OWNER_CODEX_VALIDATION_CONTROLLER_2026-09-20.md`: "Codex controller first;
embedded agent follows", the owner selecting a recommended option); guest
control **unrealised** (T6 §3f). Stance: **adopt "selection by activity" as the
rule** (OD-05); open question on evidence standing of screen-derived results.

**X-11 A host-owned local service so later applications can embed the same agents.**
v3's topology A2: the application starts, owns and stops a service that hosts
the stock harness and speaks a private protocol, kept independent of the
desktop framework because "A Node in-process library cannot be embedded in a
Tauri main process." Evidence: `TOPOLOGY_COMPARISON.md` §8 (**described**,
owner-accepted); **implemented** for the App only; no Tauri packaging exists
(T5 §1.4). Stance: **candidate architecture**, to test against the supplier
investigation (Q-02, Q-06).

**X-12 Six embedding "slots".**
Navigation workspace, structured information, workflow, decision gate, typed
agent review, UI–agent conformance. Evidence: D-APP-91 planning baseline
(**unrealised**, never validated against a host; T3 E13, T4 §6). Stance:
**use as a checklist when describing hosts; do not adopt as architecture.**

## 4. Exemplars — harness and supplier

**X-13 Build on a stock harness through its published protocol.**
v3's replatform removed a custom daemon, a patched supplier, an eight-method
event whitelist and a configuration veto; the release followed within days.
Evidence: D-GOV-43 findings (**executed**, recorded), S-1…S-8 pass, v3.0.0
published 2026-09-13 (T3 §5, T5 §4). Stance: **adopt as a principle**: the
supplier's capabilities pass through; Chirality adds context, workflows,
presentation and host integration.

**X-14 Separate sign-in, shared configuration.**
An overlay home shares the user's configuration, skills and tool servers but
keeps credentials private to Chirality. Evidence: S-8 (**executed**). Stance:
**keep the purpose** (several hosts, one user's harness setup); the mechanism
is supplier-specific.

## 5. Exemplars — coordinating many agents

**X-15 Bounded delegation with one integration owner.**
Use only the roles the work needs; executors do not delegate; one owner
integrates; briefs carry purpose, basis, context, authority, write scope and
return; record the actual mechanism and parentage. Evidence: manuals
(**described**); used in producing the manuals and in this undertaking
(**executed**, T2 P2, P9). Stance: **keep the purposes**; enforcement should
come from the harness, not instruction alone.

**X-16 Concurrency limited by the capacity to examine and integrate.**
"The rate at which required, examined contributions become available" is the
measure, not agents running. Evidence: Consolidated v7 (**described**, T2 §3).
Stance: **candidate product capability** for coordination views (review
queue, waiting-by-cause).

**X-17 Decision packages that name the act.**
Present issue, grounds, alternatives, recommendation, effects; name the exact
act requested; silence is not a ruling; agents may transcribe but not
originate a human act. Evidence: manuals (**described**); the 2026-06-21
attribution defect, where an agent recorded its own decision as an owner
approval (**executed**, T4 §4.6). Stance: **keep**; it is how "shared access
does not transfer decision rights" becomes an interaction.

**X-18 A coordination plane that does not need to exist.**
Derived, rebuildable views of file truth; presence that expires; deleting it
degrades throughput, never correctness. Evidence: PEC PRD (**accepted** in
PEC; implementation early, T5 §2). Stance: **keep the principle** for any v4
coordination views.

## 6. Exemplars — reliance and knowledge

**X-19 Statement standing, provenance, no invention, conflict surfacing.**
FACT / ASSUMPTION / PROPOSAL / TBD; missing information stays visible; sources
cited; conflicts surfaced for a human ruling. Evidence: thesis Ch. 5
(**described**; labelling assessed at audit, not enforced at production, T1
§1 P6); SWBPIPE never defaults missing inputs (**implemented**, T6 §2).
Stance: **keep**; show standing on the objects people see (T2 §6.2).

**X-20 Authentication as a scoped act bound to identified content.**
Acceptance binds to content, scope and purpose; content change voids it;
SWBPIPE's checked tag lapses on change. Evidence: thesis CF §2.3
(**described**); SWBPIPE DEC-104 (**accepted** there). Stance: **keep**.

**X-21 Warranted confidence per unit of attention.**
A design aim for where to ask the human and what to show. Evidence: **owner**
(adopted sentence). Stance: **adopt as a design aim, not a metric.**

## 7. Lessons

**L-01 Control machinery that restricts the supplier makes ordinary work
fragile.** The daemon era filtered events, vetoed the user's configuration,
patched the supplier and timed out quiet turns; replacing it unblocked release
(T3 §5, T5 §4). The owner asked that removed requirements not be "recreate[d]
… under new names" (PERSPECTIVE).

**L-02 Governance weight grew faster than its use.** About 1,022 governance
artifacts by 2026-08-01 and 30.1 % of changed lines in one measured window;
"not decidable" whether it paid, for want of telemetry (T4 §4.4, T5 §5.7). The
App's 54 deliverables were never issued; 1,044 of 3,217 deliverable claims
were found stale in the post-release concordance (T3 §4–5). An early
analysis estimated ~75 % of tokens went to context, documentation and audits
(agent estimate, T4 §4.1).

**L-03 Decomposing faster than executing.** Four decompositions in a day in
the vNext phase; the scaffold stalled with a cyclic graph (T4 §1, §4.3).
Decomposition helps once the product basis is stable enough to hold still.

**L-04 Constitution without enforcement.** Role, write and non-delegation
limits are asserted by instruction on hosts with broad permissions; every
evidence brief says so (T2 §5). Enforcement belongs where the host can
actually enforce it.

**L-05 Generality before need.** A multi-engine vocabulary retained from
earlier eras left the incumbent harness's items with nothing to render them
(D-GOV-43 finding 4). Unused engine adapters remain in the tree (T3 R3, T5
§1.5).

**L-06 Emission without consumption.** Registers that nobody is obliged to
read do not close (29 of 30 notices open; 0 of 12 disposition rows closed);
items close when adopted into a loop's own working instruments (T5 §2.7).

**L-07 Accreted PRDs mislead.** The App PRD carries a Codex-only overlay on a
Claude-first body; two sections share one number (T3 §1, T4 §4.8). A fresh
basis is cheaper than another amendment layer — the premise of OD-02.

**L-08 Synthetic journeys on the production path find real defects** that
source tests miss (T3 E12) — and synthetic users are not practitioners. No
engineering work was exercised in v3 evaluation (T3 §1).

**L-09 The embedded path has never run live.** Application tools, the Tauri
packaging, native descendant inheritance of tools, and a live model turn
against SWBPIPE are all unestablished (T5 §1.7, T6 §7). The primary v4
expression therefore rests on design evidence, not use.

**L-10 Solver truth is itself under repair.** SWBPIPE has 38 open solver
findings from an owner-commissioned review; an agent narrating results can
amplify misplaced confidence unless result standing travels with every
agent-readable result (T6 §1, §6.7).

## 8. Tensions to resolve in the v4 basis

| # | Tension | Where it shows |
|---|---|---|
| N-1 | **Enclosure versus embedding.** The thesis places Chirality as the environment that contains domain applications; v4 places Chirality inside them. | Thesis Ch. 1 §1.2, Ch. 10; T1 §7.1 |
| N-2 | **Where authoritative records live.** Files and Git are Root doctrine; hosts own domain truth in their own stores (SWBPIPE: SQLite-backed project store). | Thesis Ch. 4 §4.2; SWBPIPE SPEC §4.4; T6 §6.5 |
| N-3 | **Run-time autonomy versus proposal gates.** "Near-parity autonomy … except at certain prescribed workflow gates" (2026-08-01) versus row-by-row acceptance of every agent edit in SWBPIPE (2026-09-17). | §1 above |
| N-4 | **Workflows as prose guidance versus workflows with enforceable gates.** v3 excluded a workflow execution engine; "prescribed workflow gates" in hosts need something the host can observe. | PERSPECTIVE; AT §1 |
| N-5 | **Root text binds an engine.** Root `AGENTS.md`: "For the App MVP, Codex is the sole engine qualification and release target", and the App hosts a stock Codex App Server (D-GOV-43). The v4 brief says no supplier is chosen. | Root `AGENTS.md`; T5 §3.3 |
| N-6 | **Alignment by presence versus by prose.** "Alignment is maintained by presence, not prose"; the owner is "not confident that writing about it achieves anything" — while the method produces much prose. | AT §1 item 3 |
