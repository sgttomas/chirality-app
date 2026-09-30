# Owner decision package — DRAFT for the integrator (node K0)

Run `APP-V4-DESIGN-PASS-2-20260930`. Executor: Type 2 TASK (Claude, model
`claude-fable-5-1`), no delegation. This file is the only file written.
Read-only git; no network.

**Status: DRAFT. Nothing here is decided and nothing is recommended.** The
integrator checks it, adds recommendations and puts it to the owner. Every
choice below is stated with its options, costs and consequences; the sorting
into three groups is my reading of the six surveys and is itself open to the
integrator's correction.

## How to read this

- **The design set.** "The first increment" is the 14 deliverables you
  selected on 28 September (the App/host spine). Their design lives in 17
  design files. "This pass" is the second design pass on them, which aims at
  the 60% level: interfaces, states, data, sequences, failure behaviour and
  verification developed far enough that no further structural change is
  expected.
- **Two kinds of statement.** Where a line says **Files state**, a record says
  it and the place is given. Where it says **Inference**, it is my conclusion
  from those records, or a survey executor's conclusion that I repeat and
  name. Options that no file states are listed separately as "Not in the
  files".
- **IDs.** The prose avoids internal identifiers. Each choice ends with a
  "Where it sits" line that carries them.
- **Line numbers.** Other executors are editing the design files while this is
  written (wording alignment only). I cite sections and rule names, not
  lines. Version labels will be one step higher after that wave.

### Words used throughout

| Word | Meaning here |
|---|---|
| The App | The Chirality desktop application, which runs stock Codex as its agent |
| Host | An engineering application that integrates with Chirality. SWBPIPE (the piping application) is the first and only named host. Its own work on this integration is paused until you resume it |
| Embedded agent | An agent running inside a host, through a small Chirality agent loop. SWBPIPE has none today |
| External channel | The App's Codex operating a host from outside, through an interface the host offers |
| Checkpoint | A point a workflow declares, where a named act by the person is required (for example "the engineer marks these rows checked") |
| Arrival | The moment a run reaches a checkpoint |
| Human act | Something only a person does and that is recorded as theirs: mark checked, accept a proposal, approve, rely on a result, set a grant, enable external access |
| Reserved act | One of the five acts you reserved to the person on 28 September. No agent setting widens past them |
| Grant | The person's setting that lets an agent apply a class of operations directly instead of proposing them |
| Capture evidence | The trace left by the surface where the person actually performed an act. Without it a record may not say "performed" |
| Lapse | A performed act stops covering its subject because the content changed afterwards |
| Current phase / governance phase | Your phasing of 28 September. Now: checkpoints are plan guidance; nothing stops a run. Later, for workflows that need it: enforced holds |
| Catalog | A host's published list of the operations it offers |
| Fixture | An invented example used to state test cases. All 17 files share one: a pipe run with four supports, one engineer and a 17-step timeline |
| Spike | A bounded observation or prototype that answers a design question; it proves nothing about the product |
| Contract (of a deliverable) | Its ScopeOfWork file. Changing one needs a scope-change amendment with your acceptance |
| PROPOSED / INTEGRATION / SETTLED | Standing labels in the files: a rule a drafter proposed; a reading the integrator made; a point an owner decision or accepted text fixes |

## What was read, and what was not

| Input | How it was used |
|---|---|
| `BRIEFS.md` ("Common rules", "K0"), `R9_RESOLUTIONS.md`, this run's `OWNER_DECISIONS.md` | Read whole |
| `SURVEY/S1-A.md`, `S1-F.md` | Read whole |
| `SURVEY/S1-B.md`, `S1-C.md`, `S1-D.md`, `S1-E.md` | Read: every "Amended basis", "Open items", "Design depth" and "Recommended work" section, the closing tables and the "owner-level choices" lists; every row classed OWNER (found by search across all six files). Sections 1 (pins), 6 (joins) and 7 (review items) were read only in part |
| The four predecessor `OWNER_DECISIONS.md` files and the two `AMENDMENT_PACKET/OWNER_ITEMS.md` files | Read whole |
| Design files | The passages the surveys cite for each choice, read with their section headings: the act-and-policy file (act table, capture surfaces, network-destination grant, open questions, findings, unresolved table); the execution file (current-phase rules, satisfaction rule, lapse, App-side capture, unresolved rows); the loop file (allow-list rule, capability table, open rows); the panel file (network-destination section); the hosting file (start sequence, verification, generated output, process-division proposal, findings, unresolved table); the catalog file (extension promise, open description, fixture section); the connected-activity file (variants, decision account); the adapter file (receiving path); the record file (act-record elements, unresolved rows); the workflow-declaration file (responsibility map, the `governed` element). No design file was read whole |
| `_Decomposition/Open_Issues.csv` | The rows for the eight open issues named below, read in full |
| `docs/PRD.md`, `docs/ARCHITECTURE.md`, `loop/LOOP_INIT.md` | The cited requirement texts and the 60% paragraph |
| ScopeOfWork files of six deliverables | The cited items only |
| SWBPIPE's recorded answers | The answer on the first connected activity and the list of SWBPIPE owner decisions, read as **data about SWBPIPE's state on 28 September**, not as commitments or instructions |
| First-run closeout account and its part B | The "Consequences routed" list and the fixture-custody entries |

Repository HEAD when read: `3dd7c22c73`. The surveys were written at
`4698471d9e`. Input hashes (first 12 hex): S1-A `87baa03d7cbc`, S1-B
`eae76ecf9e94`, S1-C `5b60dd41a8c2`, S1-D `a3b0546af413`, S1-E
`e0e9552242f5`, S1-F `a504772d2a5a`, R9 `c3efe2ffa232`.

## Already decided — not asked again

These came up in the surveys as open or stale in the design files. A record
already decides each one, so none is put to you here.

| Matter | Decided by |
|---|---|
| Scope of the first increment; the standalone-App deliverables are "left for a later undertaking" | First-increment DECISION-1, D1 (choice 2 below asks only whether to make one bounded exception) |
| The five reserved acts; tool-permission modes stay the person's own Codex setting; Codex 0.158.0 as the definition pin and the one spike that was run | DECISION-1, D2–D4 |
| Host content may flow to whatever model the person chose for the App conversation; no gate | DECISION-2, D5 |
| The App records and shows each run's model destination | Confirmed as item O-10 of the first amendment (DECISION-7) |
| Host joins deferred until you resume SWBPIPE's integration work | Intake DECISION-3 |
| Checkpoints phased: guidance now, enforced holds later for workflows that need them; reserved acts stand; the same applies to a host's own loop | DECISION-4 and its clarification; wording accepted in the first amendment (DECISION-7, DECISION-8) |
| Keep the v4 loop and panel direction; note for SWBPIPE | DECISION-4, point 2 |
| Model access: local or cloud, no default; OAuth sign-in or API key | DECISION-4, point 3; accepted wording in the first amendment |
| Host-agent network destinations: allow list, in-work requests, only the person grants, stateless MCP only, record and show | DECISION-5 and its confirmation; accepted wording in the first amendment |
| The reading that "no grant widens past a declared checkpoint" is guidance now and binds later, while the reserved-act half binds now | Item O-25 of the first amendment (DECISION-7) |
| Design files use each other's definitions directly (autonomy display, panel, guide) | Items O-11, O-12, O-13 (DECISION-7) |
| Host-agent destinations are listed in the run record | Item O-14 (DECISION-7) |
| The issues list keeps the reserved-act and classifier questions marked open, with a pointer to your rulings | Item Q-5 of the second amendment (its DECISION-2) |
| The four added dependency links, including the one from the execution deliverable to the App act control | DECISION-6 and DECISION-10 of the first amendment run; Q-4 of the second |
| The dependency graph now in force (DAG-003) | Second amendment run, DECISION-4 |
| Re-pinning the 17 design files was deferred to "the next design pass" | DECISION-8; confirmed as Q-15. It is being done now |
| After a host applies a change directly at a checkpoint: the act is still requested, none is recorded, the checkpoint stays "act not performed" | Integrator ruling R9-2 in this run, derived from the accepted wording (a survey had listed it as a possible owner question) |
| Supplier evidence goes from the hosting deliverable to the record deliverable directly | Integrator ruling R9-7, from the record deliverable's contract and DECISION-6 (a survey had listed it as a disagreement between two files) |

## The choices at a glance

| # | Choice | Group | Standing in the records |
|---|---|---|---|
| 1 | Who asks the person for the act when a run reaches a checkpoint | 1 | Integrator reading; to be confirmed |
| 2 | The App's own act control: define it now, and in whose contract | 1 | Your scope decision defers the deliverable; one contract names it, the other does not |
| 3 | How the App identifies the person who performs an act | 1 | Unresolved; no options in the files |
| 4 | Does an act performed before the checkpoint was reached count | 1 | PROPOSED rule; routed to you at the first closeout; never asked |
| 5 | One act covering several items, when only some change afterwards | 1 | Open owner question carried since the first run |
| 6 | Where the shared parts live (App side) | 1 | Open issue; no placement agreed for any part |
| 7 | Is allowing a network destination the same act as setting the grant | 1 | Integrator reading; you deferred its contract wording |
| 8 | Allow list: does switching a category off suspend its named entries | 1 | Open; two accepted texts word it differently |
| 9 | Who names the model interface that the host-loop test cases are written against | 1 | Supplier unknown in the register |
| 10 | Workflow registration as a recorded human act | 1 | Open; two surveys class it differently |
| 11 | The Codex account home: shared or separate | 1 | Open issue; two surveys class it differently |
| 12 | Prepare an option sheet for the first connected operation against SWBPIPE's actual journey | 1 | New in this run |
| 13 | Which external seam the design is developed against (command-line, MCP, or neutral) | 1 | Not raised in any design file; a survey inference |
| 14 | What a spike may use in this pass: a credential, a local model server, the network | 1 | Run rule today: none |
| 15 | The consequence vocabulary for operation classes | 2 | Open; a draft can be prepared in this pass |
| 16 | The catalog-extension promise: retain, narrow or defer | 2 | Open issue |
| 17 | The App's Rust/TypeScript division and the reference protocol output | 2 | Open issue; a proposal exists |
| 18 | The supplier's start-up fetch and its "experimental" surface | 2 | Routed to you at the first closeout; never asked |
| 19 | The panel's network-destination surfaces and the panel deliverable's contract | 2 | You deferred the contract wording (tied to choice 7) |
| 20 | Custody of the shared example | 2 | Routed to you at the first closeout; no decision found |
| 21 | Proposed rules to confirm as a set, with two that widen accepted wording | 2 | PROPOSED or INTEGRATION in the files |
| 22 | Any essential host beyond the App and SWBPIPE | 2 | Open issue |
| 23 | Selecting the first connected operation, its autonomy and environment | 3 | Open issue; tied to the deferred joins |
| 24 | Whether a launch setting the person makes counts as enabling external access | 3 | Deferred by integrator ruling until SWBPIPE work resumes |
| 25 | Where a host's loop lives and what it persists | 3 | Open issue; needs SWBPIPE's implementation owner |
| 26 | Taking up the governance phase, and how a workflow opts in | 3 | Deferred by your phasing decision |
| 27 | What the next relay to SWBPIPE carries, and whether to list it now | 3 | The relay was not selected for this run |

---

# Group 1 — shapes the design now

A choice is placed here when the design text being written in this pass
differs by option, so that writing without the decision means writing both
branches or reworking later.

## 1. Who asks the person for the act when a run reaches a checkpoint

**The choice.** In the current phase a checkpoint does not stop a run. The
accepted requirement still says that at a checkpoint "the required human act
is requested" and is recorded as done only when the person performs it. No
accepted text says *who* does the requesting. The integrator has read your
words of 28 September ("I don't want checkpoints in workflows to be programmed
into the app to respond in a certain manner … any pause or hold point or gate
are the agents to manage their own behaviour accordingly") as follows, and
asks you to confirm or correct it:

- the **agent** carrying out the workflow asks the person, because the
  checkpoint is part of the plan it was given;
- the **product** gives the agent the checkpoint with the workflow, offers the
  person the means to perform the act, and records what it observes: the
  checkpoint, the request where it can be identified, and the act only when
  the person performs it;
- neither the App nor a host's loop issues the request in the agent's place,
  pauses the run, or otherwise reacts.

**Example.** A workflow says: "before the summary is returned, the engineer
marks supports S-2 and S-3 checked."

- *Option A (the integrator's reading).* When its work reaches that point the
  agent writes: "The workflow asks you to mark S-2 and S-3 checked before I
  return the summary." The record shows the checkpoint reached, the agent's
  request, and "act not performed" until you mark them. If the agent does not
  ask, nothing in the product asks; the run carries on, and the record shows
  the checkpoint reached with the act not performed.
- *Option B (the product also prompts).* As A, and in addition, when the App
  sees the arrival it shows its own notice or act control ("this workflow asks
  you to mark S-2 and S-3 checked"). The run is still not stopped.
- *Option C (only the product prompts).* The App shows the notice; the agent
  is not relied on to ask.

**Options as the files state them.** Option A only, as an integrator reading
"put to the owner for confirmation" (R9-1). **Files state** also that the
execution design lets the App "respond by presenting its own" act control
when the agent asks through a Codex question prompt (a "may", in the
App-side capture rules). **Not in the files (inference):** B and C as named
alternatives. One survey executor infers that "a product-issued request at
arrival is a programmed response of the kind the owner named" and says the
split should be confirmed with you "if the App is to do more than record".

**Cost and what changes.**

- A: the alignment wave already writes it. The next wave defines, in the
  execution design, how an App run observes an arrival and a request, and the
  record design gains one element for the request (it has none today). One
  sentence each in about ten other files. Consequence: a checkpoint can be
  passed without anyone being asked; only the record shows it.
- B or C: a product behaviour on arrival. It needs an App surface that
  belongs to a deliverable outside this increment (see choice 2), and an
  observation that does not exist yet (what the App actually sees from Codex
  around a tool call; see choice 14). It changes the execution, panel, loop
  and hosting designs. **Inference:** B and C sit closer to the behaviour your
  28 September answer declined.

**Can the design reach 60% without it?** The alignment wave proceeds on A. If
you later choose B or C, the current-phase recorder in the execution design,
the panel and loop checkpoint sections and the record design are reworked.

**Already decided or deferred?** The phasing and the wording: yes (see the
table above). Who requests: no.

**Depends on.** Nothing outside the project for A.

**Where it sits.** R9-1 (this run). PRD V4-WF-05; HOST_INTEGRATION V4-HI-42;
EXAMINATION V4-EXM-22; DEL-02-03 REQ-002, AC-002. EXEC §2.1 (PH-1, PH-4,
PH-6), §4.6, §5 CAP-6. Surveys: S1-A §1.3 and §4 gap 2; S1-C C.2 lag 2, C.5
structural 2; S1-D LOOP §3 finding; S1-E closing list. Intake DECISION-4.

## 2. The App's own act control: define it now, and in whose contract

**The choice.** An *act control* is a dedicated control in the App that only
the person can operate. It shows exactly which act, on which content, for what
purpose, and operating it produces the capture evidence that lets a record say
"performed". It is for acts on App content (files and outputs in an App
project); acts on a host's content are captured by the host.

**Files state:**

- Seven design files assign building this control to the App deliverable for
  native requests, outcomes and attachments, which your first scope decision
  left "for a later undertaking".
- The execution deliverable's contract, as revised by the second amendment,
  says that deliverable "constructs the App act control" and that its own
  positive capture cases "await that later undertaking".
- That other deliverable's contract does not contain the words "act control",
  "person identity" or "capture" (checked by search: 0 each). Its nearest text
  is that an actually performed act "may be faithfully displayed or recorded
  through the designated recording interface".
- SWBPIPE's answer is that it exposes no capture evidence for acts on its
  content, and host joins are deferred.

**Inference (survey S1-F, which I repeat):** the App act control is therefore
the only route by which *any* act can be recorded as performed in the current
phase. Without it the increment's central positive case has no executable
route on either side, and the requirement exists only on the consumer's side.

**Example.** You review an App file, `findings.md`, and the workflow needs it
marked checked.

- *If the control is defined now:* at the phase review you can trace "the
  person presses *mark checked* on `findings.md` at this content → a record
  naming you, the content and the purpose → the checkpoint shows performed →
  the file is edited → the act shows lapsed".
- *If it is left:* the design shows that case as "awaiting input (later
  deliverable)". What can be shown are the negatives: a chat reply of "yes" is
  not an act; a tool-permission answer is not an act.

**Options as the files state them (S1-F §5).**

- A. Open no design outside the 14. Record the person-identity choice only
  (choice 3). The dependency stays as it is.
- B. One bounded exception: that deliverable, limited to the act control and
  person identity. Its contract is revised first (it does not state the
  control); then a short interface note: it accepts or amends the nine
  capture rules the execution design already wrote, says what the control
  takes in and puts out, and where it runs so that no automation can operate
  it.
- C. B, and also the durable-execution deliverable, limited to the split of
  the outstanding-request register and the evidence handoff.

**Not in the files (inference).**

- D. State the obligation in that deliverable's contract now (one amendment)
  but do no design on it in this pass. This closes the one-sided requirement
  without widening the pass.
- E. Move the obligation into a first-increment deliverable's contract
  instead. Also an amendment.

**Cost and what changes.**

- A: no new work. The same open item stays in seven files. The 60% review has
  no positive "performed" path to show.
- B: one scope-change amendment (a third one), with its checkpoints; one new
  small design file; an exception to your scope decision for one deliverable.
  The "cannot be operated by automation" property depends on the App's
  process division (choice 17), for which only a proposal exists.
- C: a second outside node. It would close five open items in the hosting
  design and one in the record design. **Files state** (S1-F) that this
  deliverable's contract was not revised by either amendment and still reads
  rulings of yours as open (the reserved-act and classifier questions; the
  Codex pin), so it would need its own revision first.
- D: one amendment, no design work. E: one amendment and a re-allocation.

**Can the design reach 60% without it?** **Inference (S1-F, both sides
given):** *for* — the consumer side already carries the requirements, and the
held dependency is narrow; *against* — the 60% test is "no further structural
change anticipated", a one-sided requirement can be wrong, and the central
positive case stays without a route.

**Already decided or deferred?** Your scope decision (D1) says this
undertaking "does not start" that deliverable. You kept the dependency link
twice. Whether to make an exception has not been asked.

**Depends on.** Choice 3; choice 17 for option B; the scope-change route for
B–E.

**Where it sits.** EXEC §5 (CAP-1…CAP-9), U-E8, case CH-23; ACT §2.6; RS
U-28; WD U-25; GUIDE M5.3, G-1; CA W14-05. DEL-02-03 CLM-002; DEL-01-04
ScopeOfWork (REQ-005, VER-005). Register row DEP-02-03-027 (arc X-1). S1-F
I-12, §2.3 N-2, §5; S1-C D-8. DECISION-1 D1; DECISION-6; Q-4.

## 3. How the App identifies the person who performs an act

**The choice.** Every human-act record names a "decision actor". For acts the
App captures, how does the App know who the person is, and how strongly is
that established?

**Files state:** this is unresolved ("How the App identifies and verifies the
person is UNRESOLVED"). A record of professional reliance is kept "as the
person's own statement, with an evidence limit". The record design lists "App
person identity scheme" as an evidence limit on App-captured acts. **The
files state no options.**

**Not in the files — my inference of the plausible set.**

- A. *Self-declared.* The person sets a name in the App. No verification.
- B. *The operating-system account* on this machine.
- C. *The Codex sign-in.* The account Codex reports (a ChatGPT sign-in, or an
  API key, which names no person; a person using only a local model may have
  no sign-in at all).
- D. *A Chirality identity of its own* (its own sign-in or a signing key).
- A combination: record what is available and state the limit.

**Example.** A week later someone reads the record of a check.

- A: "marked checked by *Ryan* (self-declared on this machine; identity not
  verified)".
- B: "… by macOS user `ryan`".
- C: "… by the ChatGPT account *r…@…* as reported by Codex"; with an API key
  or a local model the record falls back to A or B.
- D: "… by *Ryan*, verified by Chirality sign-in".

**Cost and what changes.** A, B, C: small edits to the actor element and the
evidence-limit wording in the record design, one rule in the execution design
and one row in the workflow-declaration design. C also ties the record to the
account-home choice (choice 11) and to Codex account behaviour that has not
been observed live (choice 14). D is new scope (an identity mechanism) and
would need an amendment; it reads like governance-phase work.

**Can the design reach 60% without it?** Yes: the files carry an evidence
limit. **Inference (S1-F):** it is a data-definition choice inside the 14,
because it sets one element of every App-captured act record.

**Already decided or deferred?** No. (How SWBPIPE identifies an actor for acts
on its own content is a SWBPIPE owner decision and is not this choice.)

**Depends on.** Choice 2 (the control that uses it); choice 11 if C.

**Where it sits.** EXEC CAP-8, U-E8; RS §6.1 ("Decision actor", "Evidence
limits"), U-28; WD U-25. S1-F §2.3 N-1.

## 4. Does an act performed before the checkpoint was reached count

**The choice.** The files carry a PROPOSED rule: an act answers a checkpoint
only if it was captured at or after the arrival. An earlier act on the same
subject is shown as "prior act on this subject, not counted", and the person
repeats it knowingly. The alternative is to count an earlier act when the
content it was made on is still current.

**Example.** A workflow says: "before the agent changes the load case, the
engineer sets the grant that allows that class of change to be applied
directly." You set that grant ten minutes ago and it is still in force.

- *Option A (the rule in the files).* The checkpoint shows "prior act, not
  counted". You set the same grant again. The record holds two acts for one
  unchanged setting.
- *Option B (count a prior act on current content).* The checkpoint shows
  "performed", citing your earlier act.

The same applies to checking: you mark two supports checked, and a later
stage's checkpoint asks for exactly that check on unchanged rows.

**Files state** the reason for A: an act is bound to its purpose, and "an act
captured before the arrival was not made in answer to that request, so its
purpose is not the checkpoint's". They state its cost: "visible friction
every time a grant precedes its checkpoint". In the current phase nothing is
held either way; the choice changes a record label and what the agent is
expected to ask for. In the governance phase it decides whether the run waits.

**Options as the files state them.** A and B. Under A the files also mention a
presentation that would soften the cost ("re-affirm current setting"; still an
act); it has not been applied.

**Not in the files (inference).**

- C. By act kind: count a prior act for grant settings, where what matters is
  the setting in force, and not for checking or approval, where purpose
  matters.
- D. Let each checkpoint declare whether a prior act counts.

**Cost and what changes.** A: nothing changes; the rule's label moves from
PROPOSED to settled. B: the rule changes in the execution, workflow,
act-and-policy and record designs, and the expected results of about a dozen
cases change across roughly a dozen of the 17 files; mechanical. C or D: a
new element in the workflow declaration and more cases; larger.

**Can the design reach 60% without it?** Yes, carried as PROPOSED. Two surveys
list it among the choices that can still restructure their files.

**Already decided or deferred?** The first closeout routed it "to the owner
(next steering)". I found no question and no answer in any owner-decision
record.

**Depends on.** Nothing outside the project.

**Where it sits.** EXEC §4.5 SP-6, U-E4, F-23, cases CH-12 and CH-20; WD I-8,
U-31; ACT §4.5, U-14, F-17; AS U-17; RS L-13, U-26; LOOP (U-E4 row; FX-C4b,
FX-C11b); PANEL W-5c, PC-21i; C variant V-GR1; P §10; CA row 9. Rulings R4-5,
R5-7. First-run `CLOSEOUT_ACCOUNT.md`, "Consequences routed".

## 5. One act covering several items, when only some change afterwards

**The choice.** You mark supports S-2 and S-3 checked in one act. Later S-3 is
edited. The check has lapsed for S-3. What does the checkpoint then need?

- *Option A.* A new check on S-3 alone is enough; the earlier act still stands
  for S-2.
- *Option B.* The earlier act no longer serves its purpose as a whole; a new
  act over both supports is required.

**Files state** that the question is "does the act's purpose survive for the
other rows", that the request shown to the person covers the whole scope with
the lapsed items marked, and that a new act over the whole scope satisfies
under either option. Until it is ruled, an act on the lapsed rows alone "is
recorded and shown, and the arrival stays waiting", and one case is held.

**Example.** After the edit to S-3:

- A: you mark S-3 checked. The checkpoint shows performed, answered by two
  acts (the earlier one for S-2, the new one for S-3).
- B: you mark S-3 checked. The checkpoint still shows waiting: "S-2 and S-3
  required; S-3 checked at ‹time›; earlier act lapsed". You mark both.

**Not in the files (inference).** A per-kind answer (for example: a check
survives row by row; an engineering approval does not).

**Cost and what changes.** Either option is small: the lapse section of the
execution design, one held case released there and one in the
connected-activity design, and a sentence each in the act-and-policy, record,
workflow and autonomy-display designs. A needs a rule for two acts together
answering one arrival. B is what the files' conservative carry already does.

**Can the design reach 60% without it?** Yes; the held cases stay held.

**Already decided or deferred?** No. It has been carried as an open owner
question since the first run.

**Where it sits.** ACT U-03, §4.3; EXEC §4.7 ("Partial lapse"), U-E3, case
CH-8; WD U-05c; RS U-07; AS U-19; CA DI-7; LOOP and PANEL open rows.

## 6. Where the shared parts live (App side)

**The choice.** Several things must be read the same way by the App, by a
host's agent loop and by a host's panel: the workflow declaration, the
checkpoint meaning, workflow identity, the act and run record, the policy
records, the catalog schema check, and some display components. The open
issue asks where each lives and who owns it.

**Options as the files state them**, per part:

- a shared type or library used by every consumer;
- a local implementation in each consumer, kept in agreement by conformance
  fixtures;
- a service.

**Files state** the trade-off in the accepted decision brief's terms: "local
implementations need conformance work; a library couples releases; a service
adds process, availability and upgrade coordination". The issues register
adds: "No common service presumed from shared meaning" and "agree ownership
before any common implementation". The workflow design lists twelve parts
with a candidate for each; the confirmation cell of every row reads "None".

**Example.** SWBPIPE's panel must show "reached; act not yet recorded".

- *Shared library:* SWBPIPE imports the Chirality piece and shows identical
  wording and rules; a Chirality release can force a SWBPIPE release.
- *Local implementation:* SWBPIPE writes its own reader and passes the shared
  fixtures; the two can drift between fixture runs.
- *Service:* both ask a running process; one more thing to start and upgrade.

**Not in the files (inference).** Decide only the App-side half now (what the
App's own parts share) and leave App-to-host sharing until a second real
consumer exists. The register's wording ("against actual consumer
responsibilities") is compatible with that.

**Cost and what changes.** A placement per part lets this pass write: the
component structure of the autonomy display, the representation of policy
records, where records are kept and who reads and writes them, and where
schemas live.

**Can the design reach 60% without it?** The surveys differ, and I report
both. **S1-A:** the autonomy display's components "cannot be designed past
meanings until it is chosen", and the absence of any data representation is
its first gap against "no further structural change". **S1-B:** it does not
change the catalog's meanings but "does change the route to completion".
**S1-D:** *later* for the loop and panel, because there is one identified
consumer and the "other hosts" question is open.

**Already decided or deferred?** No. The issues register names "App/shared
contract owners" as the owner; the files do not say who holds that role.

**Depends on.** The host half is choice 25. Choice 22 (other hosts) bears on
how much sharing is worth.

**Where it sits.** Open issue OI-014. WD §9 and U-12; EXEC U-E2; ACT U-12; AS
U-08; RS U-05, U-16; C, P, ADAPTER unresolved rows; LOOP §10.2; PANEL §6;
GUIDE. S1-A §4 gap 1; S1-B 1.5 item 3; S1-C A.5 item 5; S1-D LOOP item 29.

## 7. Is allowing a network destination the same act as setting the grant

**The choice.** Your decision on host-agent network destinations made granting
a destination a person-only act. The integrator mapped that grant onto the
existing reserved act "set grant", as a sub-kind, because your fifth reserved
act is "changing the autonomy grant or enabling external-agent access". The
person-only rule is settled. The mapping is an integrator reading that "the
owner may revisit at any time".

**Options.**

- A. Confirm: a destination grant is a sub-kind of "set grant".
- B. Give it its own act kind ("allow destination").

**Example.**

- A: the record reads "set grant (network destination): web access on". A
  workflow checkpoint that requires "set grant" raises a question no file
  answers: could a destination grant satisfy it? The grant display shows
  destination grants beside operation grants (the files already forbid
  merging them into one "allowed" signal).
- B: the record reads "allowed destination: web access on". A checkpoint that
  requires "set grant" cannot be met by it. Your list of reserved acts gains
  a sixth entry, or its fifth is reworded to include it.

**Cost and what changes.** A: the label moves to settled; the workflow design
needs one sentence on checkpoints. B: edits in five files (the act table and
destination section, the autonomy display, the record, the loop, the panel)
and an extension of your reserved-act ruling. **Either way (files state,
S1-A):** the act-and-policy deliverable's own contract does not carry your
destination decision, and one of its acceptance criteria says its policy
"supplies no reserved list … beyond" your first ruling; a confirmation "would
call for" one contract sentence, which this run may not write.

**Can the design reach 60% without it?** Yes. The destination content is then
developed end to end on the integrator's mapping.

**Already decided or deferred?** Partly. When you accepted the first
amendment you accepted an item that said: no further contract change for this
"now"; "revisit when the A12 mapping is confirmed or at implementation" (A12
is the files' label for the act "set grant").

**Where it sits.** ACT §2.7, F-22, act table row A12; DEL-04-01 AC-007,
AX-005. Ruling R8-13. OWNER_ITEMS O-15 (DECISION-7). S1-A §1.2 item 4 and
closing; S1-C D-6. Intake DECISION-5; DECISION-1 D2 (e).

## 8. Allow list: does switching a category off suspend its named entries

**The choice.** The allow list has category switches (web access, MCP servers,
other APIs) and named destinations. If a category is off and a named entry in
it exists, is that entry still allowed?

**Example.** "MCP servers" is off. The list names one server, M-1.

- *Option A (independent; the loop design's interim reading).* M-1 may be
  started and contacted. The record says it was allowed by "named entry".
- *Option B (subordinate).* M-1 is suspended while the category is off. The
  agent must ask during its work, or the contact is refused.

**Files state** two wordings, both from your decision of 28 September. The
requirement text (your words): "in an allow list (by category … or by named
destination)". The decision's effects and the architecture text: "a category
switch … and named destinations within each category". The loop design reads
the first as alternatives and has written one case on option A.

**Consequences.** A lets a person allow exactly one destination without
opening a whole category. B makes the switch a master switch: "off" means
off.

**Cost and what changes.** Small either way: one rule and two cases in the
loop design, two panel cases, the allow-list rows of the autonomy display.

**Can the design reach 60% without it?** Yes, on the interim reading; two
panel cases wait.

**Already decided or deferred?** The decision is yours of 28 September; this
point was not addressed in it.

**Where it sits.** LOOP N-OPEN-4, NW-8, cases MS-15, MS-18; PANEL ND-1, PC-30,
PC-34; AS U-21. PRD V4-HOST-02; ARCHITECTURE §4 host-agent properties. Intake
DECISION-5.

## 9. Who names the model interface that the host-loop test cases are written against

**The choice.** The accepted architecture has a host's agent loop talk to its
model over "OpenAI-compatible Chat Completions with tool calls". To write
test cases that can run, the design needs the exact form of four things: how
a tool call arrives in fragments, the values that say why a response ended,
several tool calls in one response, and how "no arguments" is expressed. The
dependency register lists the supplier of that basis as UNKNOWN. SWBPIPE's
answer is that no model interface exists or is selected there.

**Options as the files state them (S1-D).**

- A. The App/shared side names a published Chat Completions basis for its own
  fixtures now.
- B. The fixtures stay unexecutable until SWBPIPE decides its embedded-agent
  mechanism.

**Not in the files (inference).**

- C. Name the basis from observation of one local server (the architecture
  lists oMLX, LM Studio and Ollama as candidates). Needs choice 14.
- D. Wait for the App's local-provider deliverable, which is to hand over
  "local-server capability requirements" after it qualifies a server. That
  deliverable is outside the increment.

**Files state a constraint:** the loop deliverable's contract requires it to
"leave exact protocol versions and payload details unselected until their
actual basis is available". So a basis named now is a *fixture* basis, not a
product selection, and would be labelled as such.

**Example.** The case "the model returns two tool calls in one response, and
one is malformed".

- A or C: the case is written in the named representation and can run against
  a test double. If SWBPIPE later selects a server that behaves differently,
  the cases are revised.
- B or D: the case stays prose ("several calls per response: unresolved").

**Cost and what changes.** A/C: three open rows of the loop design's
capability table close as PROPOSED; three malformed-call rules and the
fixture inventory follow. Reading a published reference needs network access
or the text supplied by you (choice 14). B/D: nothing now; S1-D names this its
second most consequential gap ("every LOOP fixture is a case design").

**Can the design reach 60% without it?** Definitions yes. The loop design's
verification aspect stays at designed cases.

**Depends on.** SWBPIPE's embedded-agent decision (its own); choice 14.

**Where it sits.** Register row DEP-05-01-024. LOOP §4, §10.1, §10.3, MC-6,
MC-7, MC-8. DEL-05-01 REQ-002. S1-D LOOP items 11 and 27; S1-F I-2.

## 10. Workflow registration as a recorded human act

**The choice.** A new or changed workflow stays a draft until the person
reviews it and explicitly registers it. Is that registration a named human
act with its own record, like a check or an approval?

**Files state:**

- The workflow-workspace deliverable (outside the increment) has an
  acceptance criterion that an actual review and registration "is faithfully
  recorded and presented with the human actor distinct from any recorder and
  bound to its content, scope and purpose".
- The act-and-policy design lists registration among acts that "have no
  canonical name here". The record design says: "Not recorded here".

**Options.**

- A. Name it now: a fifteenth entry in the act table, a record kind, and a
  ruling on whether a checkpoint may require it.
- B. Leave it until the workspace deliverable is defined.

**Not in the files (inference).** C. Record it as an entry in the run's
operation list without a human-act record. The files keep those two kinds of
record apart, so this would need its own justification.

**Example.** A workflow refined in the host comes back to the App and you
register it.

- A: the record reads "registered by ‹you›, revision ‹r›, derived from ‹r−1›,
  purpose: make available in this project". A later reader can see who
  registered which revision.
- B: the design shows the link "draft → registered, derived from" with no act
  record; the two round-trip cases that pass through registration stay
  "awaiting input".

**Cost and what changes.** A: the act table and its closed list, the record
kinds, the round-trip section of the execution design, a row in the workflow
and connected-activity designs. Small to moderate. If A is chosen later, the
same edits are made after other text has been built on a closed table.

**Can the design reach 60% without it?** Yes. The surveys class it
differently: **S1-A: later** (the workspace deliverable is outside the 14);
**S1-F: needed now as a decision**, one that can be made without a design
file for the workspace deliverable, because a later "yes" changes two
first-increment files.

**Already decided or deferred?** No.

**Where it sits.** ACT §2.1 (closing list), U-08, §12 item 6; RS U-08; EXEC
U-E19; WD U-10. DEL-02-02 REQ-006, AC-006. CA F-1, W14-01, W14-09. S1-F I-3,
§2.3 N-3; S1-A §1.4.

## 11. The Codex account home: shared or separate

**The choice.** Codex keeps its sign-in and configuration in a home folder.
Does Chirality's Codex use the home your other Codex clients use, or one of
its own?

**Files state:** the issues register asks to "choose separated versus shared
Codex account state" and adds "do not silently carry current v3 overlay or
Root behavior into new product choice". The architecture leaves it "to the
implementation session". The hosting design carries it as an open element of
the start sequence and notes two observed facts: even the version check
writes temporary files into the home it runs against; and on a *fresh* home
Codex fetches about 24 MB from `github.com/openai/plugins` at start.

**Options as the files state them.** Shared; separated.

**Not in the files (inference).** A middle form, which is what the repository
doctrine describes for the current v3 App: shared configuration, with sign-in
kept separate. And a sub-choice: whether the version check runs against the
account home or a throw-away one.

**Example.**

- *Shared:* you are already signed in with the Codex CLI, so the App is signed
  in and sees the same settings and MCP servers. The App's version check
  leaves temporary files in your home.
- *Separate:* you sign in again inside Chirality; settings are not shared;
  the first start of that new home triggers the fetch at least once.

**Cost and what changes.** The start sequence, the verification rule and the
configuration-identity record in the hosting design; one finding. Small in
text.

**Can the design reach 60% without it?** The hosting design carries it as
unresolved. The surveys differ: **S1-F** lists it under "needs now", "if
HOSTING is to be structurally settled in this pass"; **S1-D** lists it under
"not in this pass".

**Already decided or deferred?** No. The register names "Owner with App
implementation owner".

**Depends on.** Choice 18 (the fetch); choice 3 if identity is taken from the
sign-in. Its integration belongs to a deliverable outside the increment.

**Where it sits.** Open issue OI-009. HOSTING U-03, §4.2 step 3, §7.2, F-14.
ARCHITECTURE §3 ("Left to the implementation session"). DEL-01-05 TBD-001.
S1-F I-11, §2.3 N-5; S1-D HOSTING item 5.

## 12. Prepare an option sheet for the first connected operation

**The choice.** The first connected activity is the first real piece of work
done across the App and a host. Its operation, autonomy and environment are
unselected (choice 23). The design's example assumes a host with per-item
accept and reject, grants, an identity for each object, and a catalog.

**Data about SWBPIPE (its answer of 28 September, not a commitment):** its one
wired journey is *inspect → preview → submit → the person's Apply in the
application → status*, for one field (a node's x position). Apply accepts and
applies a whole batch in one step. There is no reject record, no grant, one
identity for the whole model, no enablement act, and the first caller it
names is a development Codex over a command-line tool, not the App's Codex.
That journey sits in an unmerged draft that is deferred.

The choice for this pass is only whether to **prepare** a sheet that sets each
step of the designed activity against what SWBPIPE has, so that the later
selection is made on a concrete comparison.

**Options.** A: prepare it. B: do not; the files keep recording "no SWBPIPE
counterpart" step by step, as now.

**Example of one sheet row.** "Step: the person accepts item 2 of 3 and
rejects item 3. SWBPIPE today: Apply takes the whole batch; no reject record.
Examinable against SWBPIPE: no. Examinable on a test double: yes."

**Cost and what changes.** A: one table in the connected-activity design and
notes in the external-trace design; one bounded task; it uses SWBPIPE's
answers as data and claims no join. **Files state (S1-E):** it "changes what
'develop toward 60%' means" for those two files. B: nothing now; **inference
(S1-E):** your later selection "could restructure" the connected-activity and
trace designs and the guide rows that index them.

**Can the design reach 60% without it?** Yes.

**Already decided or deferred?** The selection is open and the joins are
deferred. Whether to prepare the sheet is new.

**Where it sits.** CA §2.2, §2.5 (DI-1…DI-3), §2.4; XT XC-02, XC-08, XC-10.
S1-E A.5, A.8 item 9, closing list item 1 and gap 1. SWBPIPE answer SQ-04.

## 13. Which external seam the design is developed against

**The choice.** On the external channel the App's Codex reaches a host in one
of two native ways: the host offers an MCP server whose tools the model
calls, or the host offers a command-line tool that Codex runs. The accepted
basis lets the host choose. The adapter design keeps both and selects
neither. **Files state:** the only seam on record at SWBPIPE is a
command-line tool in a deferred draft, while the facts recorded about Codex
at the pinned version are mostly about MCP and say nothing about what the App
can read from a command run.

**Options (S1-B, as an inference; "not raised in any file").**

- A. Develop the command-line path to the same depth as MCP.
- B. Stay neutral: meanings only, no path developed.

**Not in the files (inference).** C. Develop MCP only, as the better-observed
path.

**Example.** The App must record "operation sent to the host, its arguments
and its outcome".

- *MCP path:* the App reads a structured item: tool name, arguments, result,
  status.
- *Command-line path:* the App reads a command line, an exit status and
  output text, and must parse that text to know the outcome.
- *Neutral:* the design says "the App observes the native item" and does not
  say which fields become which record elements.

**Cost and what changes.** A: four sections of the adapter design, an
observation-to-record mapping, and a bounded observation of a command run at
the pinned version (choice 14). The evidence in the external-trace design
differs by path. B: the mapping gap stays, and the simulated host that 42
designed cases presume cannot be specified concretely.

**Can the design reach 60% without it?** **Inference (S1-B):** it is "a choice
this pass must make" before the missing interface text can be written.

**Already decided or deferred?** App code sitting on the dispatch path is not
adopted in this increment (recorded under your second decision of
28 September and applied by an integrator ruling). Your standing
condition that any MCP use follows the stateless revision is on record.
Which path to design against has not been asked of anyone; S1-B says "owner
or integrator".

**Depends on.** SWBPIPE (the seam is the host's to choose); choice 14.

**Where it sits.** ADAPTER §2, §3.5, §9 (OC-1…OC-3); DEL-03-03 TBD-007; XT
structural choice 1. Ruling R4-2; first-increment DECISION-2 (D6 effects);
intake DECISION-5 (the stateless-MCP condition). S1-B 3.5, closing table
row 7.

## 14. What a spike may use in this pass

**The choice.** Several open items can only be closed by observing real
behaviour. The run's rule for executors is: no network. Live Codex behaviour
needs a model turn, which needs either your sign-in or a local model server.

**What is waiting, by what it needs (from the surveys).**

| Needs | Would settle |
|---|---|
| Nothing beyond the repository | How a workflow's declared part is carried in a file (render and parse four examples); a first record format written and read back; a simulated host and a simulated Codex built from the eight recorded transcripts |
| Network, read-only | The text of a published Chat Completions reference (choice 9); the text of the stateless MCP revision, to name what evidences conformance |
| Running Codex with no sign-in | Three handshake questions. **Files state:** starting Codex on a fresh home causes the 24 MB fetch (choice 18) |
| A local model server on this machine | How a local server represents tool calls (choice 9); the Codex provider interface for local servers |
| A model turn (your sign-in, or a local server) | What the App actually sees from Codex around a tool call on the external channel; what a command run looks like (choice 13); whether an MCP call raises a tool-permission prompt; whether the requested and the effective model can differ; how outstanding requests settle |

**Options.**

- A. None: repository-only prototypes.
- B. A, plus read-only network for published specifications.
- C. B, plus a local model server (which one is part of the choice).
- D. C, plus a Codex sign-in for live turns with a cloud model.

**Example.** Under A the execution design says "the arrival is observed from
the native items Codex delivers" and cannot say which. Under C or D it can
name the item sequence, observed once at the pinned version and recorded as
an observation.

**Cost and consequences.** B, C and D relax the no-network rule for a named
task. C needs a server installed and named. D needs you: **inference** — a
sign-in is performed by you, not by an agent, and fixture text would go to a
cloud model (the content is invented example material). Any run of Codex
touches an account home (choice 11). Each observation is a dated record at one
version; it is not qualification.

**Can the design reach 60% without it?** Partly. **Files state** that the
observation interface of an App run (S1-C gap 2), the adapter's unobserved
supplier behaviours and the loop's representation rows stay open without it.

**Already decided or deferred?** You authorized one spike on 28 September
(install the pinned Codex in a scratch folder, generate its protocol types,
record what was seen). It was run. Nothing further is authorized.

**Where it sits.** HOSTING U-19, U-09, U-22, §10 "Still to observe"; LOOP
items 27, 28 (N-OPEN-5); ADAPTER OC-3, OC-12 and the not-observed rows; EXEC
recommended item 6; C/P executable M3-CP return; WD U-01; RS U-04. S1-D
closing list; S1-B 3.8 item 7; S1-C C.8 item 6. DECISION-1 D4.

---

# Group 2 — can wait for the phase review

A choice is placed here when this pass can prepare it (a draft, options, an
observation) and the design text does not fork on it yet.

## 15. The consequence vocabulary for operation classes

**The choice.** Each class of host operation is to carry a statement of its
consequence, along four dimensions named in the decision brief you accepted:
effect, reversibility, available examination and intended delegation. No
values exist for any of them.

**Options.** A: adopt a fixed App/shared value set. B: leave each dimension as
free text until a host assigns its classes. **Not in the files (inference):**
C: each host defines its own values, since a host names its own classes.

**Example.** For "change a support's stiffness": with A the record says
"changes results · reversible by undo · examinable by re-solve · delegable",
and a grant can be scoped "apply directly only what is reversible and
examinable". With B the same is a sentence, and a grant can name classes but
not properties.

**Cost and what changes.** A adds one axis to the policy-class record, the
grant scope and the catalog entry (about four files), and releases one held
case.
**Files state (S1-A, S1-B):** a PROPOSED vocabulary can be drafted in this
pass from the four dimensions; assigning values to SWBPIPE's real operations
waits for the host.

**60% without it.** Yes, with the draft. **Decided?** No; the files name "the
act-and-policy deliverable with the host policy owner".

**Where it sits.** ACT U-02, §5.1, §8.1, §8.4; C row C6; AS U-02; RS U-02.
`DECISION_BRIEF.html#d3`. S1-A §1.8 item 8.

## 16. The catalog-extension promise: retain, narrow or defer

**The choice.** The original promise: when a host adds an operation to its
catalog, it becomes available to the person, the embedded agent and the
external agent "without separate work". **Files state** it is "preserved and
not claimed".

**Options as the files state them.** Retain; narrow to the surfaces generated
from the catalog; defer.

**Example.** SWBPIPE adds "rotate support".

- *Retain:* the design must show the panel, the loop's tool list and the
  external tools all picking it up from the catalog, and an examination must
  trace that on a real candidate.
- *Narrow:* promised only for the agents' generated tool lists; the human
  interface may need its own work.
- *Defer:* nothing is promised; the operation means the same thing wherever
  it does appear.

**Cost and what changes.** **Files state (S1-C):** "no effect on these files
until decided"; (S1-B) "defer can be chosen today". A narrowed promise would
be written through the catalog entry's per-surface exposure element and the
responsibility map, and would set the criterion the external trace examines.
SWBPIPE has no catalog and no catalog editions today; its part in the
decision is its own owner decision.

**Decided?** No. **Where it sits.** Open issue OI-003 (App v4). C §8
(extension paragraph), element 9, variant V-ED1; XT §5.2; CA DI-8; WD U-16.

## 17. The App's Rust/TypeScript division and the reference protocol output

**The choice.** The App has a Rust main process and a TypeScript interface.
Which side owns which part of the Codex protocol handling? And, because the
pinned Codex generates two type outputs that differ, which is the reference?

**Options as the files state them.**

- Division: (1) Rust holds the envelope (process, framing, correlation, the
  outstanding-request register) and TypeScript composes typed payloads — the
  hosting drafter's recommendation; (2) Rust fully typed. Two further options
  are "set aside" by the file as violating the accepted architecture.
- Reference output: the TypeScript output; the JSON Schema bundles (the only
  ones committed; they need a supplement for six elements); or the union with
  the source of each element recorded.

**Example.** Not visible to a user directly. On a Codex upgrade, under (1)
most changes land in TypeScript; under (2) Rust changes with every schema
change (170 client methods at the pin). The place that makes an act control
"not operable by automation" (choice 2) follows from the division.

**60% without it.** **Files state** the hosting design fixes the invariants
and carries the division as "a proposal only"; the deliverables that would
receive it are outside the increment. S1-D lists both among choices that can
still restructure the hosting design.

**Decided?** No. The register names the "App implementation owner"; the files
do not say who holds that role.

**Where it sits.** Open issue OI-008; HOSTING §12, U-02; §7.3, U-15. S1-D
HOSTING items 4 and 6.

## 18. The supplier's start-up fetch and its "experimental" surface

**Files state (observed at the pinned version):** on a fresh home Codex
fetched about 24 MB from `github.com/openai/plugins` at start, with no
sign-in and no turn; processes it starts can outlive it; whether a setting
turns it off was not observed. Codex labels the embedding surface the App
uses "experimental", and four features the App needs are available only
under an experimental opt-in.

**Two choices.**

- *The fetch.* Accept Codex's own start-up traffic for the App, or require
  that it be prevented. **Not in the files (inference):** accept and show it,
  as the App already shows the model destination. **Files state** that your
  network-destination decision governs a host's agent, not the App's Codex,
  and that your flexibility answer on model destinations "does not settle"
  this either.
- *The experimental label.* A visibility item. The file's route is to accept
  the exposure and re-examine at each version; it says the label "does not
  reopen the chosen supplier direction".

**Example.** First launch on a new machine: 24 MB is downloaded before you do
anything. Offline first launch: not observed.

**Cost.** "Require it prevented" needs an observation with network access
(choice 14) and may not be achievable. **Decided?** Routed to you at the
first closeout; never asked. **Depends on.** Choice 11.

**Where it sits.** HOSTING U-18, U-21, F-12, F-13, F-14, F-21, §8.1 row L-4;
PIN_SPIKE findings S-F-10, S-F-18. S1-D HOSTING items 7, 8, 12.

## 19. The panel's network-destination surfaces and the panel deliverable's contract

**Files state:** the panel design has a section for the allow-list settings,
the in-work prompt, the decline and the list of destinations contacted. The
panel deliverable's contract contains the word "destination" zero times. The
scope item that carries "recorded and shown" is assigned to the loop
deliverable only. The autonomy-display deliverable's contract says *it* shows
the allow list, the in-work grants and the contacted-destination record; its
design has no display for the third; the loop design assigns that display to
the autonomy-display design; the panel design has it.

**Options (S1-D).** A: a later amendment gives the panel deliverable the
display of destinations. B: no contract change; the section stands as the
panel receiving the loop's "shown" obligation. **Not in the files
(inference):** C: move the content to the autonomy-display design, whose
contract names it, and have the panel refer to it.

**Example.** No difference in what a person sees. The difference is which
deliverable is examined for "every destination contacted is shown".

**Decided?** Deferred by you, in an item of the first amendment: no other
contract change for the act-and-policy or panel deliverables "now … Revisit
when the A12 mapping is confirmed or at implementation." So it follows
choice 7.

**Where it sits.** PANEL §3.8 (ND-1…ND-5), cases PC-30…PC-37; AS §3;
DEL-04-02 CLM-002; LOOP §10.1 networking row; ScopeLedger SOW-017.
OWNER_ITEMS O-15 (DECISION-7). S1-D PANEL §2 item 5, item 13; S1-A §2.2
item 3.

## 20. Custody of the shared example

**Files state:** the one invented example that all 17 files cite lives in a
section of the catalog design (about a fifth of that file). The section says
holding it "is an integration assignment … it does not extend" the catalog
deliverable's scope. The first closeout routed its custody to you, with the
point of need "before the next undertaking reuses it". I found no decision.
**Inference:** this pass is that reuse.

**Options.** A: leave it where it is, as an assignment. B: give it a file and
an owner of its own. C: treat it as design scaffolding that is not maintained
afterwards. (The files pose the question; they list no options.)

**Cost.** B re-points every citation of that section in fourteen files
(S1-B), and more once a simulated host is built on it in this pass. A keeps a
non-scope section inside one deliverable.

**Where it sits.** C §10; first-run `closeout/C1-B.md` §1.2, §1.5;
`CLOSEOUT_ACCOUNT.md`. S1-B 1.5 item 2, closing table row 1.

## 21. Proposed rules to confirm as a set, with two that widen accepted wording

**Files state** that several rules stand as PROPOSED or INTEGRATION and are
"open to review". The surveys class them "owner, at the phase review (no
separate prompt)". They are: an ended run is never resumed (a continuation is
a new run); how a later grant setting supersedes an earlier one; App-side
configuration never counts as evidence of enabling external access; the rule
for proposals whose items get different decisions; the App-side capture
rules; the grant display for network destinations; the idea of a "catalog
edition". You can confirm them as a set at the review, or pull any out.

Two are different in kind, because they widen an accepted text:

- **Disabling external access.** Your ruling reserves *enabling* it. The
  files also reserve *disabling* it, as an integrator reading the file says
  "the owner may wish to confirm". *Example:* an agent notices the channel is
  open and turns it off. Reserved: it may only ask you. Not reserved: it may
  do so, and the record shows it.
- **Open description of catalog entries.** The accepted requirement says
  workflows and skills must be readable without Chirality-specific software.
  The catalog design proposes the same for a host's catalog entries.
  *Adopting it* widens that requirement's reach (a wording amendment);
  *leaving it* rests the point on the external-interface requirements.

**Where it sits.** ACT F-11, F-14; AS and RS "standing labels" rows; C §2
invariant 4 (F-C9), "catalog edition"; EXEC §4.9, §5. S1-A §1.4, §2.4, §3.4;
S1-B rows C25, C26.

## 22. Any essential host beyond the App and SWBPIPE

**Files state:** "Identify any essential host beyond the named App and
SWBPIPE", owner: you; point of need: "before examination scope is frozen";
meanwhile "no other host is presumed". It bears on choice 6: with one
consumer, shared code has less to justify it.

**Where it sits.** Open issue OI-005; XT IN-13. S1-E C.4 item 3.

---

# Group 3 — already deferred with the host joins or the governance phase

Listed so that the package is complete. Each is parked by a record; none needs
an answer for this pass.

## 23. Selecting the first connected operation, its autonomy and environment

**The choice.** Which operation, which non-mutating check, what autonomy, what
additions to the reserved acts, which candidate environment, and which acting
surface (embedded agent or external channel).

**Example.** If the choice is SWBPIPE's existing journey: the agent proposes
moving a node; you press Apply; status comes back; there is no per-item
decision and no grant. If it is an operation like the design's example: the
agent proposes three changes; you accept two and reject one; a grant lets a
later change apply directly.

**Files state:** the issues register names the owner as "Owner via outside SWB
session and App/shared owner". SWBPIPE's answer: "Selection: none … an owner
decision". **A point to check:** your deferral of the host joins (DECISION-3)
lists three deferred things — the joined witness and live cases, SWBPIPE-side
examination, and naming the App's Codex as a caller. It does not name this
selection. The surveys *infer* that the selection waits with the joins
because it is exercised through the SWBPIPE session. **Inference:** the
records would allow a selection on paper before the joins resume; choice 12
prepares for that.

**Where it sits.** Open issue OI-021. CA §2.5; ACT U-01; every file's
unresolved table. Intake DECISION-3; DECISION-1 D2 closing sentence.

## 24. Whether a launch setting the person makes counts as enabling external access

**Files state:** enabling external access is a reserved act and needs capture
evidence from the host. SWBPIPE has no enablement facility; its opt-in is an
environment variable at launch plus a build feature. The integrator ruled that
the channel therefore shows "not enabled", and deferred to you "whether a
launch environment variable the person sets counts" as the act, to be
revisited when SWBPIPE work resumes.

**Example.** You start SWBPIPE with the variable set. *Counts:* the channel
shows enabled by you, and live external cases can run. *Does not count:*
the channel shows "not enabled — host reachable without evidenced enabling",
and every live external case waits for SWBPIPE to add a facility.

**Where it sits.** Ruling R8-6 (R8-Q4b). ACT §2.6, U-16; ADAPTER §3; CA DI-9;
XT, GUIDE, RELAY rows. S1-B closing table row 5.

## 25. Where a host's loop lives and what it persists

**Files state:** "choose loop placement, parsing, persistence and panel
assembly without transferring SWB ownership by implication"; owner: "shared
contract owner with SWB implementation owner". It needs SWBPIPE's side and so
waits with the joins. It is the host half of choice 6.

**Where it sits.** Open issue OI-013. LOOP, PANEL, WD (U-13), GUIDE rows.

## 26. Taking up the governance phase, and how a workflow opts in

**Files state:** your phasing decision keeps enforced checkpoints as a later
layer "applied when a workflow needs them". Open under it: when, and for
which workflows; whether the App itself can hold a run; allow lists locked by
an organization; enforced sandboxing of outside processes.

One structural point is inside it. The files carry a PROPOSED per-checkpoint
flag, authored in the workflow, that marks a checkpoint as one the governance
phase will enforce. **Inference (S1-C):** an opt-in applied by the person, a
host or an organization *outside* the workflow file would be a different
structure. The first amendment told you the flag "is still PROPOSED". The
cost of leaving it so is small now: in the current phase the flag is only
displayed.

**Example.** *Authored flag:* the workflow's author decides which checkpoints
are enforceable. *Outside opt-in:* the same workflow file runs as guidance in
one project and enforced in another, by a project or organization setting.

**Where it sits.** Intake DECISION-4 D4-1. WD §4.3.1 (`governed`), EXEC §2.2;
the unresolved `D6` rows carried in most of the design files; LOOP §5.1.1
phasing. OWNER_ITEMS O-4
note. S1-C A.5 item 2, closing list item 5.

## 27. What the next relay to SWBPIPE carries, and whether to list it now

**Files state:** the relayed question set is frozen and cannot be corrected in
place. Since it was sent: your network-destination decision created host
obligations no question asks about; three questions carry premises that are
now superseded; the handoff note still says "local-first" in one line and
does not mention model access or network destinations. You decided on
29 September that the "local-first" note "carries forward with the next
relay". The relay was not selected for this run.

**The choice (S1-E).** Whether the list of what the next relay must carry is
written down now (as a note beside the frozen questions), or left until the
relay is taken up. Writing it changes no question and relays nothing.

**Where it sits.** RELAY §0–§3 (frozen), unresolved table; GUIDE M7.9;
`HANDOFF_SWBPIPE_DOMAINS.md`. First-amendment DECISION-8. R9-10. S1-E B.8
item 3, E.1, closing list item 3.

### Also parked (one line each)

- How guidance and instruction files are distributed and adopted: open issue
  OI-018, owner-held; needed by a role-supply deliverable outside the
  increment.
- A numeric responsiveness criterion for the host loop: "Owner, if wanted";
  the loop deliverable's contract forbids an unsourced threshold (LOOP
  R-OPEN-1).
- How the grant display reads for a host that has no grants (proposed
  wording: "host fixed treatment: every change waits for Apply"): deferred
  with the joins by integrator ruling R8-10.
- The product-level list of reserved acts beyond the first increment (PRD
  open question OQ-02): left "for a later basis update" by item O-26.

---

# Matters the surveys raise that are not put to you here

These are structural and open, but the surveys class them as design work, an
integrator ruling or a spike. They are listed so the integrator can promote
any of them.

| Matter | Survey | Why not an owner choice here |
|---|---|---|
| The loop design has rules for network destinations but no kind of tool that reaches one: either such tools are host catalog entries, or a second tool source beside the catalog | S1-D, first gap | Classed as design work with the catalog and proposal owners. **Inference:** the second answer would sit against the accepted "tools from the host's capability catalog"; if the integrator finds that, it becomes an owner question |
| How the declared part of a workflow is carried in its file | S1-C, first gap | A prototype in this pass can settle it |
| Names for Codex's own capabilities, so a workflow can require them | S1-C, third gap | Answerable from committed records |
| Who creates a proposal's identity, and how its recorded outcome is read back | S1-B, second gap | App-side meaning decidable now; mechanism later |
| Whether the record carries an element for a request (for an act, or for a destination) | S1-A | Follows choice 1 |
| Whether network-destination grants travel in the settings exchange between the autonomy display and the record | S1-A | Design work after choice 7 |

# Where the records disagree

For the integrator. Each is reported as found; I have not resolved any.

1. **The App act control (choice 2).** The execution deliverable's contract
   says another deliverable "constructs the App act control". That
   deliverable's contract does not mention it, and its dependency notes say
   no sentence names the consumer.
2. **Category and named entries (choice 8).** Requirement text: "by category …
   or by named destination". Architecture text and the decision's recorded
   effects: "named destinations within each category". The loop design's one
   case follows the first.
3. **Who shows the destinations contacted (choice 19).** The autonomy-display
   contract says that deliverable shows them; its design does not; the panel
   design does; the panel contract does not mention destinations; the loop
   design assigns the display to the autonomy-display design.
4. **Registration (choice 10).** One deliverable's acceptance criterion
   requires a faithful record of registration; the act and record designs
   offer none. Surveys S1-A and S1-F class the same item "later" and "needed
   now".
5. **The account home (choice 11).** The architecture leaves it "to the
   implementation session"; the issues register names "Owner with App
   implementation owner". Surveys S1-F and S1-D class it "needs now" and "not
   in this pass".
6. **Shared placement (choice 6).** Surveys S1-A and S1-B treat it as bearing
   on the 60% test; S1-D classes it "later" for its files.
7. **The first connected operation (choice 23).** The surveys describe the
   selection as deferred with the host joins. The deferral record lists three
   deferred things and does not name the selection.
8. **The destination grant and the act-and-policy contract (choice 7).** The
   design carries the destination grant as a sub-kind of a reserved act; the
   deliverable's own contract cites three of your decisions and not the one
   that created it, and one acceptance criterion limits its reserved list to
   your first ruling.
9. **The prior-act rule's label (choice 4).** The execution design marks it
   "ADOPTED (R4-5) with standing PROPOSED"; the workflow design marks the
   same rule "PROPOSED (W7)". A label difference only.
10. **Owner roles.** For choices 6, 17 and 11 the register names "App/shared
    contract owners" or "App implementation owner". No record I read says who
    holds those roles, so I cannot state from the files that these are yours
    to decide alone; the surveys list them as owner-level.

# Limits of this draft

- Four of the six surveys were not read whole (see "What was read"). An
  owner-level matter stated only in a pins, joins or review-items section
  could have been missed; the search for every row classed OWNER reduces that
  risk but does not remove it.
- No design file was read whole. Each choice rests on the passages cited.
- The design files were being edited while this was written. Section and rule
  names should be stable; wording quoted from them may have been realigned.
- Options marked "Not in the files" are mine. They are there so the set is
  complete, not because any record proposes them.
- Cost statements are the surveys' file counts and my reading of them; none
  is an estimate of effort in time.
- This file claims no SWBPIPE join, witness or adoption, and changes no
  contract, register, status, graph or design file.
