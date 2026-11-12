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

**What the release is judged on.** App v4 is examined and released on working
through the user interface it ships with. Two standalone journeys carry that:

- **J1, use an existing workflow.** A person sets up a project, selects an
  existing workflow, supplies its inputs, runs it to completion and finds the
  results.
- **J2, create, save, return and reuse.** A person does useful work, turns it
  into a workflow, registers it, returns to unfinished work after closing and
  reopening, and later runs the saved workflow with new inputs.

Both are in the release: J1 is the primary journey, and J2 is the complete
workflow-making loop the App exists to provide (PRD §2.1).

**Outside this release.**

- **A live SWBPIPE journey.** It is a requirement of SWBPIPE and not of App
  v4. DEL-09-07 and DEL-09-11, which examine that journey, are held outside
  4.0.0; they may be worked on in support of SWBPIPE, and nothing in this
  target waits on them. App Agent 0 answers SWBPIPE's Agent 0 on the App's
  receiving side when asked.
- **Windows.** It follows the macOS release and adds no gate to it.
- **Domains.** It follows in a later increment and is no condition of release
  or of replacement. PEC adds no delivery prerequisite.
- **Standalone OpenAI API-key access.** The access modes are the ChatGPT
  account and a local model server (PRD V4-APP-02).
- **Key rotation.** It is unavailable in 4.0.0, and the release says so.
- **A comparison, regression or migration campaign against v3.** v3 was the
  interim version that prepared v4, so v4 is tested as v4. Because 4.0.0 keeps
  the existing production identifier, a person's existing data under that
  identity is preserved: nothing imports, resets or reseals it.
- **Improvements beyond these criteria.** They are taken up after the release.

**Fallback.** v3.0.1 stays the published fallback until the owner decides that
v4 has replaced it.

**Testing.** Agents do the development testing. The owner's product testing
begins once Agent 0 has recommended that the candidate is ready. The two are
different things: agents' testing verifies behaviour, and only the owner's own
use judges whether the product is fit for real work (DEL-09-12). A control
operated by an agent establishes no act of the owner.

## Exit criteria

Every criterion is met on one identified candidate: an App source revision, a
build identity and the supplier pin. A criterion is met only by the owning
deliverable's result on that candidate. A merged change, a source check, a
component pass or a result on an earlier candidate is a step toward a
criterion and does not meet it, and a changed candidate reopens the steps the
change affects. This is what lets the owner decide on what was actually
observed.

1. **Use an existing workflow (J1).** Through the App alone, a person sets up
   a project, selects an existing workflow, supplies its inputs, runs it to
   completion and finds the results, with real execution doing useful work and
   without an agent interpreting or operating the App's controls. No time or
   step limit applies.

   *Owning deliverables:* DEL-02-02 (the journey as product), DEL-09-02 (its
   observation on the candidate).
2. **Create, save, return and reuse (J2).** Through the App alone and as one
   sequence, a person does useful work, turns it into a workflow draft,
   trials, reviews and registers it, returns to unfinished work after closing
   and reopening, and in a later session runs the saved workflow with new
   inputs under their workflow approval policy. No time or step limit applies.

   *Owning deliverables:* DEL-02-02, DEL-09-02.
3. **Requests, interruption and recovery.** On the candidate, a turn is
   stopped, the window is closed and reopened with a request waiting, one
   request is denied and a later one granted, the App is quit with live work
   and relaunched, and the conversation continues. Work and outstanding
   requests survive the closed window, and what the App shows at each recovery
   point agrees with the supplier's actual events. A failure is repaired or
   brought to the owner for disposition; it is never passed over.

   *Owning deliverables:* DEL-09-02 (the observation), with DEL-01-02,
   DEL-01-03 and DEL-01-04 (the behaviour observed).
4. **Access.** On the candidate, the ChatGPT account and a local model server
   are configured together, a new conversation has no model until the person
   chooses, one conversation runs with each, and no credential appears in
   anything the App wrote.

   *Owning deliverables:* DEL-01-05, DEL-09-02.
5. **Installed custody and keychain protection.** On the installed, signed
   candidate, the App verifies its own Codex before running it, and the
   person's act "Protect registered workflows with your keychain" enrols the
   key, stores the approval policy in the keychain and admits a sealed
   registered workflow after a cold start. A development build cannot show
   this, because the act needs the signed installed identity.

   *Owning deliverables:* DEL-01-04 (the act and its result), DEL-01-01 (the
   installed check), DEL-01-06 (the signed identity it relies on).
6. **Supplier and notices.** The supplier pin the candidate is built with is
   qualified, and every component shipped in the package has its notice. The
   package is not offered for public release while a component is uncovered.

   *Owning deliverables:* DEL-01-01 (the pin), DEL-01-06 (the notices).
7. **Final candidate.** The package built from the finished source contains
   the supplier's tree and the bundled resources byte for byte, is signed with
   the publisher identity, notarized and stapled, and from a quarantined
   download installs and launches through to a Codex child reported ready and
   verified.

   *Owning deliverables:* DEL-01-06.
8. **Terms position.** The supplier's written position on distributing the
   offering is held with the owner's statement that it applies, and the
   candidate's offering and sign-in flow are the ones that statement covers.
   A changed offering or sign-in flow reads as unresolved.

   *Owning deliverables:* DEL-01-06.
9. **Limitations.** Every limitation the owner accepted for the release is
   stated in what a person receives with the package, including that key
   rotation is unavailable.

   *Owning deliverables:* DEL-01-06, and for each limitation the deliverable
   whose behaviour it limits.
10. **The owner's product testing.** Agent 0 has recommended that the candidate
    is ready, the owner has used it, and each of the owner's observations has
    a disposition.

    *Owning deliverables:* DEL-09-12.
11. **Decision packet.** The owner has, for the exact final candidate, the
    owning deliverable's result for each criterion above, the release's
    limitations and the continuing obligations, with every unrun, failed,
    blocked or limited result shown as such. Publication and replacement are
    put as two separate decisions. For replacement, the packet shows whether
    the candidate supports the core loop (plan, execute, save a workflow,
    reuse it, approvals, interruption, restart) at least at v3.0.1's level,
    which is the condition under which v4 may replace it (PRD §8, V4-REP-01).

    *Owning deliverables:* DEL-11-03, with DEL-09-02 (the core-loop results),
    DEL-09-12, DEL-11-01 (continuing obligations) and DEL-01-06.

## Open choices

These bear on a criterion and nothing accepted settles them. Each is carried
by the scope named.

- Whether the journeys of criteria 1 to 4 must be observed on the installed
  package, or may be observed on an identified development build (DEL-09-02).
- Which of the owner's findings must be closed before publication, and the
  period and activities of the owner's testing (DEL-09-12).
- Whether the core loop at v3.0.1's level is a condition of publishing 4.0.0
  or only of replacing v3.0.1, and what replacing the fallback changes once
  4.0.0 is published (DEL-11-03).
- Which workflows the release ships, and which role, if any, a new
  conversation preselects (DEL-02-02, DEL-02-04).
- Where the release's list of accepted limitations is kept, and what it holds
  beyond key rotation (DEL-01-06).

## What stays the owner's

- Publishing the release, including the decision to distribute it publicly.
- Replacing v3.0.1, and the verdict on the product that the owner's testing
  gives.
- Licence, legal and professional sign-off: the statement that the supplier's
  terms position applies to the offering, and professional approval of and
  reliance on any result.
- Credentials: sign-in, and signing and notarization with the owner's
  Developer ID.
- Spending money, and repository protections and settings.

Who decides a change to a criterion is stated in `AGENTS.md`. A decision edits
the text it governs; this document is not a log, and Git keeps its history.
