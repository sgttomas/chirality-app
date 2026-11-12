---
name: chirality-app-release-target-4-0-0
description: Set the App 4.0.0 release target, its exit criteria and what stays the owner's.
metadata:
  kind: instruction
  surface: requirements
---
# Chirality App 4.0.0 (macOS): release target

This is the target the App is finished toward: a direction, the exit criteria
and what stays the owner's. The exit criteria are the definition of done. Each
names the deliverables that own it, and their `ScopeOfWork.md` states what each
commits to and what is undecided. This document holds no capability and no
status; the scopes and the code do.

Meeting the criteria is evidence for the owner's decisions, not the decisions.
Publishing 4.0.0, replacing v3.0.1 and professional reliance on a result are
three separate acts, and none follows from another or from a criterion being
met.

Paths are relative to the repository root. A deliverable `DEL-nn-nn` is at
`execution/PKG-nn/DEL-nn-nn/`.

## Direction

**Target.** Public Chirality App v4, version 4.0.0, on macOS on Apple Silicon,
minimum macOS 15, bundle identifier `com.chirality.app`. It is offered free,
locally run and open source, with the supplier's Codex inside unmodified and
the supplier's own sign-in unchanged.

**The bar.** The owner's words define it: "you're going to need to use your
judgment to make something good enough that the PRD will feel substantially
complete and the user experience is reliable and would feel good for humans."
This is direction: where the exit criteria leave a judgment open, it is what
the judgment serves. It is not evidence that any criterion is met.

**What the release is judged on.** App v4 is examined and released on working
through the user interface it ships with. Two standalone journeys carry that:

- **J1, use an existing workflow.** A person sets up a project, selects an
  existing workflow, supplies its inputs, runs it to completion and finds the
  results.
- **J2, create, save, return and reuse.** A person does useful work, turns it
  into a workflow, registers it, returns to unfinished work after closing and
  reopening, and later runs the saved workflow with new inputs.

J1 is the primary journey, and J2 is the complete workflow-making loop the App
exists to provide (PRD §2.1). The core loop is necessary for publication and
is not by itself enough: the journeys, the visual design and the owner's
verdict stand beside it.

**What ships with it.** Every workflow of the selected Library ships.
HELP_HUMAN is what a new conversation preselects; a person's explicit
selection, and any specialised workspace, keep their own.

**Outside this release.**

- **A live SWBPIPE journey.** It is a requirement of SWBPIPE and not of App
  v4. DEL-09-07 and DEL-09-11, which examine that journey, are held outside
  4.0.0; they may be worked on in support of SWBPIPE, and nothing in this
  target waits on them. App Agent 0 answers SWBPIPE's Agent 0 on the App's
  receiving side when asked. Workflows of the host origin are a separate
  obligation, held outside 4.0.0 with it (DEL-02-02 AC-013). The undecided
  items of the host loop and panel contracts (DEL-05-01, DEL-05-02) are
  decided at a host's point of need and do not gate this release.
- **Windows.** It follows the macOS release and adds no gate to it.
- **Domains.** It follows in a later increment and is no condition of release
  or of replacement. PEC adds no delivery prerequisite.
- **Standalone OpenAI API-key access.** The access modes are the ChatGPT
  account and a local model server (PRD V4-APP-02).
- **Key rotation.** It is unavailable in 4.0.0, and the release says so.
- **A comparison, regression or migration campaign against v3.** v4 is tested
  as v4. Because 4.0.0 keeps the existing production identifier, a person's
  existing data under that identity is preserved: nothing imports, resets or
  reseals it.
- **Work beyond the PRD's commitments.** It is not part of this release's
  definition of done. A capability the PRD commits to is, unless this section
  names it.

**Fallback.** v3.0.1 stays the published fallback until the owner decides that
v4 has replaced it.

**Testing.** The owner's words direct it: "I expect you to do thorough user
testing via computer use and only when that's worked out the bugs and you
think you're ready for publishing would i then use the app for testing." This
is direction, not evidence that any criterion is met. Agents do the
development testing. The journeys and examinations of criteria 1 to 6 and 15
are carried out by agent-operated journey examination: an agent operates the
built App's shipped controls through the computer-use ability native to its
harness, as a user would. Every journey action goes through the shipped
controls. Preparing invented fixtures, and independent observation (reading
the supplier's actual events, inspecting records and files on disk, verifying
an exported package without the App), are done outside the controls, and each
record names them as such. What is ruled out is help that conceals an unusable
control, not independent scrutiny: a second examiner or a reviewer may take
part. Such an examination establishes that the journey can be completed
through the shipped controls and what the App then shows and records; it is
not evidence of how a first-time person understands the App. Each step's
record says who operated it and by what means, and notes where completing the
step needed knowledge the interface did not give. No criterion reads as met by
a person when no person did it. Findings are repaired and the affected
scenarios run again before Agent 0 recommends the candidate; a result from an
earlier candidate is joined as the exit criteria below state.

Credential acts stay the owner's: sign-in and key entry are performed by the
owner and never by an agent, and a run that needs a signed-in App or the local
model server follows the owner's sign-in. The first human evaluation of the
product is the owner's own use of the candidate, which begins once Agent 0 has
recommended that it is ready (criterion 13). The two are different things:
agents' testing verifies behaviour, and only the owner's own use judges
whether the product is fit for real work (DEL-09-12). A control operated by an
agent establishes no act of the owner.

The product's rule is unchanged: the App never performs for a person an act it
reserves to a person, and only the person's own confirmation captures an act;
an attempt by an agent tool, an MCP operation or an App rule captures nothing
(DEL-01-04 AC-008, DEL-04-01). Apart from that rule, and as a bounded
development-test exception, the examining agent operates the App's own
confirmation controls (review, registration, answers to requests, quit
confirmation) on disposable invented fixtures in a scratch library and a
scratch records store. What those controls then capture is a synthetic
examination artifact: it establishes no person's decision, is kept apart from
any evidence of an actual human act, and is never reused as anyone's act.
Where an owning scope compares a record with an act an examiner watched a
person perform, in such an examination the record is compared with the
confirmation the examining agent made at the control, and the examination
inspects what the product recorded there (actor, content, scope and purpose);
a product record that attributes such an act to an identified person is a
finding (DEL-09-02 REQ-009).

## Exit criteria

Each criterion says in plain words what is observed, and then names the
acceptance criteria that govern it. The named criteria are what is met; the
description narrows none of them.

Every result names the candidate it was observed on: an App source revision, a
build identity and the supplier pin. Criteria 1 to 7 may be observed on an
identified development build, because they concern how the App behaves and
looks. Criteria 8 and 10 are observed on the installed, signed package, because
they concern that package. A merged change, a source check or a component pass
is a step toward a criterion and does not meet it. A result observed on an
earlier candidate is joined to the final one only with an assessment that
covers the difference and names the scenarios the change reopens; those are
observed again, and unchanged observations are not repeated. This is what lets
the owner decide on what was actually observed.

1. **Use an existing workflow (J1).** Through the App alone, a person sets up
   a project, selects an existing workflow, sees its source and revision,
   supplies its inputs, runs it to completion and finds the results, with real
   execution doing useful work, every step taken through the App's shipped
   controls and the words it shows, and no control interpreted or operated by
   any other means. Before the run the App says which of the workflow's
   declared required tools are available and which are missing, and a workflow
   whose requirements are not declared reads as undeclared and is not shown as
   needing none. A file the person selects as an input is sent as selected: if
   it changes between selection and sending it is held and not sent. What the
   agent receives is the selected workflow, byte for byte. No time or step
   limit applies.

   *Governed by:* DEL-02-02 AC-010 (the journey as product) and AC-005 (what
   the agent received); DEL-01-04 AC-011 (the run text reaches Codex
   unchanged); DEL-02-03 AC-001 (the required-tool check); DEL-01-04 AC-003
   (a selected file); DEL-09-02 AC-009 (the journey examined on the
   candidate through the shipped controls).
2. **Create, save, return and reuse (J2).** Through the App alone and as one
   sequence, a person does useful work, turns it into a workflow draft,
   trials, reviews and registers it, returns to unfinished work after closing
   and reopening, and in a later session runs the saved workflow with new
   inputs under their workflow approval policy, the agent receiving that saved
   workflow byte for byte. No time or step limit applies.

   *Governed by:* DEL-02-02 AC-011 and AC-005; DEL-01-04 AC-011; DEL-09-02
   AC-010.
3. **The core loop at least at v3.0.1's level.** A conversation starts in a
   role: HELP_HUMAN is preselected and can be cleared, HELPS_HUMANS,
   WORKING_ITEMS and no role are offered, TASK is not, and the chosen role's
   guidance is added to the supplier's own instructions without replacing
   them. Where the harness cannot enforce a role's limits, the App says so
   and does not imply that they are enforced. In one continuous journey
   from an empty project folder, a person develops and revises a plan with the
   agent, has it carried out with real tools including one delegated sub-task,
   creates a workflow draft, trials and reviews it, registers it, runs it on
   new inputs and refines it twice, each refinement a further registered
   revision. The workflow shows its declared inputs, tools, checkpoints,
   outputs and evidence and its source-qualified identity. Neither a same-name
   entry from another origin nor a revision overwrites or rebinds what was
   selected. Each act is recorded as the person performed it, and where the
   act was not performed (the control left unconfirmed, the agent claiming it,
   a tool reporting success, an act of another kind) the App shows it as not
   performed. Only the person's own confirmation captures an act: an attempt
   by an agent tool, an MCP operation or an App rule does not. Together with criterion 4, this is the condition under which v4
   may replace v3.0.1 (PRD §8, V4-REP-01), and it is also a condition of
   publishing.

   *Governed by:* DEL-09-02 AC-001, AC-002 and AC-003; DEL-02-02 AC-004 (the
   identity a selection keeps, on the project, user and bundled origins);
   DEL-02-04 AC-001 and AC-002 (the roles offered and the guidance supplied)
   and AC-003 and AC-004 (a limit the harness does not enforce shown as not
   enforced);
   DEL-01-04 AC-008 (only the person's confirmation captures).
4. **Requests, interruption and recovery.** Inside that journey, a turn is
   stopped while a delegated child is active, the window is closed and
   reopened with a request waiting, one request is denied and a later one
   granted, a request is cancelled, the App is quit with live work and
   relaunched, and the conversation continues. Work and outstanding requests
   survive the closed window. At each recovery point what the App shows agrees
   with the supplier's actual events: a completed turn does not mark an active
   child done, a reply without acknowledgment is not shown as settled, and an
   unavailable outcome is shown as unknown. When a run reaches a checkpoint
   the workflow declares, its arrival is recorded, and the checkpoint's
   disposition is waiting until evidence of the required human act exists; the
   App does not pause or hold the run. Continued work, a tool's success, an
   interruption or a replay of history does not perform it. After quit and reopen it is the same run,
   and a later run inherits no arrival, disposition or act from it. A failure
   is repaired or given its disposition by Agent 0, which the owner sees in
   the decision packet; it is never passed over.

   *Governed by:* DEL-09-02 AC-004 and AC-005; DEL-01-02 AC-001 to AC-006
   (window loss, interrupt, requests, acknowledgment, restart and quit);
   DEL-02-03 AC-002 and AC-003 (checkpoints and the run they belong to), with
   the views of that behaviour owned by DEL-01-03 and DEL-01-04.
5. **Coordinating delegated work.** A person delegates two bounded pieces of
   work, each with a complete brief, to agents that actually run. The person
   follows them on the undertaking's work graph, examines what they return
   from the return queue, and decides one matter from a decision package; the
   decision is recorded as the person made it and from nothing else. Through
   a change of basis and an interruption, the App keeps apart what is ready,
   what waits and why, what a worker still holds and what has returned and
   awaits review. After the App is closed and reopened, the views are rebuilt
   from the files and show the same ownership, results, waiting causes,
   reviewed and integrated history and pending decisions, with a missing
   observation shown as unknown.

   *Governed by:* DEL-09-05 AC-001 to AC-007.
6. **Access.** A person signs in with their ChatGPT account, and the account
   view shows the account Codex reports. The App offers no standalone OpenAI
   API-key entry. The ChatGPT account and a local model server are configured
   together. A new conversation has no model until the person chooses. One
   conversation runs with each, and switching between them leaves the other's
   configuration in place. The local conversation runs with its required
   credential held by Codex in the dedicated local home, examined apart from
   account sign-in, and the two homes keep their own settings and sign-in. A
   different compliant local server can be substituted through supported
   settings. The start-up connections of the App's Codex are listed, and those
   an App setting stops are absent. No credential appears in anything the App
   wrote. In the examination the owner performs the sign-in and the entry of
   the local server's key, and agents examine what follows.

   *Governed by:* DEL-09-02 AC-006; DEL-01-05 AC-001 to AC-005, AC-008 and
   AC-011.
7. **Visual design.** A person meeting the App's views in the journeys and
   examinations of criteria 1 to 6 finds that they share one visual form,
   drawn from v3.0.1 as installed, that they are consistent with one another,
   and that nothing reads as unfinished or out of place. Function and
   interaction are designed for v4 and are App Agent 0's to decide; the
   reference fixes the form, not v3's tools or behaviour. An examiner who did
   not build the views compares them with the reference on the build those
   journeys and examinations are observed on. Whether the App feels good to
   use is the owner's verdict (criterion 13), not this comparison.

   *Governed by:* DEL-02-02 AC-012.
8. **Installed custody and keychain protection.** On the installed, signed
   package, the App verifies its own Codex before running it and refuses a
   tree that differs from the expected identity. The person's act "Protect
   registered workflows with your keychain" enrols the key and stores the
   approval policy in the keychain, and after a cold start a registered
   workflow sealed under that key is admitted. A development build cannot show
   this, because the act needs the signed installed identity.

   *Governed by:* DEL-01-04 AC-009 (the act and its result); DEL-01-01 AC-006
   (the installed check); DEL-02-02 AC-004 (admission of a registered
   revision under the approval policy); DEL-01-06 AC-002 (the signed identity
   it relies on).
9. **Supplier and notices.** The supplier pin the candidate is built with is
   qualified: it is the newest Codex version that had passed a version-advance
   check when the candidate was built, and the supplier-hosting criteria hold
   on the candidate at that pin. Every component shipped in the package has
   its notice, and the package is not offered for public release while a
   component is uncovered.

   *Governed by:* DEL-01-01 AC-011, which requires AC-001 to AC-010 on the
   candidate (the pin); DEL-01-06 AC-007 (the notices).
10. **Final candidate.** The package built from the finished source contains
    the supplier's tree and the bundled resources byte for byte, and the
    workflows it ships are every workflow of the selected Library. Every signed
    executable of the supplier's tree keeps the supplier's signature and
    entitlements. The App's own code carries the publisher identity, hardened
    runtime and a timestamp, with the entitlements its features need and no
    debugging entitlement, and any provisioning profile names the same
    identity. The bundle is notarized and stapled, and its identity record
    states what an independent reading of the package finds. From a quarantined
    download the operating system accepts it without an override, and it
    installs and launches through to a Codex child reported ready and verified.
    Where data written by v3.0.1 is present under the App's identity, it is
    unchanged after the package has been installed and run.

    *Governed by:* DEL-01-06 AC-001, AC-002, AC-003 and AC-009. That the
    shipped workflows are the selected Library's whole set is governed by this
    criterion as stated, with AC-001 for the inventory comparison.
11. **Terms position.** The supplier's written position on distributing the
    offering is held with the owner's statement that it applies, and the
    candidate's offering and sign-in flow are the ones that statement covers.
    A changed offering or sign-in flow reads as unresolved.

    *Governed by:* DEL-01-06 AC-004 and AC-005.
12. **Limitations.** Every limitation the release carries is listed in
    [`docs/RELEASE_LIMITATIONS_4.0.0.md`](RELEASE_LIMITATIONS_4.0.0.md) with
    its reason, and is stated in what a person receives with the package.

    *Governed by:* this criterion as stated, for the completeness of the list
    and its reasons, which Agent 0 keeps and the owner sees with the request
    for the verdict; DEL-01-06 AC-008 for what accompanies the package.
13. **The owner's verdict.** After Agent 0 has recommended the candidate
    ready, the owner uses it and answers yes or no before it is published.
    What the owner uses it for, and for how long, is the owner's to choose at
    the time. With the recommendation, Agent 0 tells the owner which criteria
    were examined by agents and that no person has yet carried out the
    journeys. Agent 0 gives every observation the owner makes a disposition;
    that is Agent 0's responsibility and not a question returned to the owner.
    The criterion is met on yes. A yes meets this criterion only: any other
    criterion that is unmet stays unmet.

    *Governed by:* this criterion as stated; DEL-09-12 holds the record of the
    owner's use, the answer and the dispositions (AC-007).
14. **Decision packet.** The owner has, for the final candidate, the owning
    deliverable's result for each criterion above, the release limitations and
    the continuing obligations, with every unrun, failed, blocked or limited
    result shown as such. A result from another candidate appears only with
    the assessment that joins it. Publication and replacement are put as two
    separate decisions.

    *Governed by:* DEL-11-03 AC-001, AC-003 and AC-007, with DEL-11-01 for the
    continuing obligations.

## Open choices

Each of these decides whether a criterion can be met, or whether one is
added, and nothing accepted settles it. Every other undecided item stands as
its owning scope states it.

- **Tying a delegated child to its brief (criterion 5).** How a child is tied
  to its brief where the supplier exposes neither the dispatch message nor a
  mark the App can set is undecided (DEL-06-01 TBD-003), and the criterion
  needs each delegation connected to its brief.
- **The records the App keeps (no criterion yet).** The PRD commits to where
  decisions and run records are kept, that they are append-only and report a
  changed line, and that they export as a package that verifies without the
  App and import without overwriting (V4-REC-02, V4-REC-04, V4-REC-06). The
  missing fact is whether the App's records store is implemented; it is
  established from the code. If it is, this becomes a criterion governed by
  DEL-04-03 AC-001, AC-009 and AC-011 at least, observable on a development
  build. If it is not, it is stated as outside this release, with a
  limitations entry for what a person cannot do. Until a signing key is chosen
  (DEL-04-03 TBD-003) an exported package is unsigned, which is a limitation
  to list either way.

## What stays the owner's

- Publishing the release, including the decision to distribute it publicly.
- The verdict on the product (criterion 13), and replacing v3.0.1.
- Licence, legal and professional sign-off: the statement that the supplier's
  terms position applies to the offering, and professional approval of and
  reliance on any result.
- Credentials: sign-in, and signing and notarization with the owner's
  Developer ID.
- Spending money, and repository protections and settings.

Who decides a change to a criterion is stated in `AGENTS.md`. A decision edits
the text it governs; this document is not a log, and Git keeps its history.
