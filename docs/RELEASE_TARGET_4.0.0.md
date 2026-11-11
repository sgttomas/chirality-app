---
name: chirality-app-release-target-4-0-0
description: Propose the App 4.0.0 exit criteria, owner rulings and reserved decisions.
metadata:
  kind: proposal
  surface: requirements
---
# Chirality App 4.0.0 (macOS): release target

**Status: draft for the owner's acceptance.** Nothing in this document is
accepted. The exit criteria and their values are the owner's to accept, change
or strike. Until then the [publication punchlist](../execution/_Coordination/PUBLICATION_PUNCHLIST.md)
and the [execution basis](../execution/_Coordination/CURRENT_EXECUTION_BASIS.md)
remain the working definition. Meeting the criteria is evidence for the
owner's decisions, not the decisions: publication, replacement of v3.0.1 and
professional reliance are separate owner acts.

The exit criteria are the only definition of done. Each names the deliverables
that own it, so an agent goes from the objective to the place where the work
and its standing live. This document never records status.

Marks: *(lifted)* restates an existing statement in the cited record;
*(inferred)* was drawn from the records without an existing statement that
says it. Paths are relative to the repository root.

## Direction

**Target.** Public Chirality App v4, version 4.0.0, on macOS: minimum
macOS 15, bundle identifier `com.chirality.app`, including the live SWBPIPE
journey (execution basis, "Release target and authority").

**Scope for the climb.** Both standalone journeys are in the release (owner,
2026-11-03: "both journeys now before 4.0.0 ships"). Outside this climb:
Windows, which follows the initial macOS release and adds no gate to it;
Domains, which follows in a later increment; any new v3 comparison campaign,
VM work, key-rotation implementation or unrelated polish (execution basis;
punchlist, "How this constrains work").

**Opening duty.** At session start, Agent 0 states the path from the current
state to this target and the work that can proceed independently. After the
owner's steering, it runs that work in parallel in standalone Type 1 sessions
(`AGENTS.md`).

**Working posture.** The owner's standing instruction (2026-11-09 00:29 UTC,
as recorded in `AGENTS.md`): "This is just a standing instruction for you: Your
top priority is to keep productive work moving forward. Don't stall out in
repetitive cycles of testing and documenting of work. Some of that is
necessary but easy to get absorbed in. Keep development moving towards the
publication goals. Tell your interlocutor this is important for them to remind
you of too, when relevant circumstances arise."

Each unit is carried to a usable, verified result (owner, 2026-10-26: "we are
nearing a level of maturity where there needs to be a concerted drive towards
goals and finishing things to a practical level. Continuous improvement goes
after.").

**Testing.** Agents perform development testing. The owner's product testing
starts after Agent 0 recommends publication readiness (owner correction,
2026-11-05, recorded in the punchlist without quoted words). Ordinary builds
and tests run concurrently and are not serialised for caution (owner,
2026-11-09 04:51 UTC: "Do you need to be so cautious?"; 05:46 UTC: "you ought
to be able to continue testing as you wanted.").

## Exit criteria

A criterion is met only by the owning deliverable's reconciled result on the
identified candidate. A merged change, a source check or a component pass is a
step toward a criterion and does not meet it (punchlist, "How this constrains
work"). Work that would change a criterion or add one goes to the owner.

1. **Use an existing workflow (J1).** *(lifted: punchlist P1; DEL-02-02
   J1)* Through the App, a person sets up a
   project, selects an existing workflow, supplies its inputs, runs it to
   completion and finds the results, without an agent interpreting the
   application's engineering controls. The workflow does useful work with real
   execution. Threshold: the journey is observed on the identified candidate;
   no time or step limit is set.
   - Owning: DEL-02-02 (journey and product), DEL-09-02 (examination on the
     candidate); contributions from DEL-01-04 and DEL-01-05.
2. **Create, save, return and reuse (J2).** *(lifted: punchlist P2; DEL-02-02
   J2)* Through the App, a person does useful
   work, turns it into a workflow draft, trials, reviews and registers it,
   returns to unfinished work after closing and reopening, and later runs the
   saved workflow with new inputs under their workflow approval policy.
   Threshold: the sequence is observed on the identified candidate; no time or
   step limit is set.
   - Owning: DEL-02-02, DEL-09-02.
3. **Requests, interruption, recovery and access.** *(lifted: punchlist P3;
   execution basis release list item 1)* On the candidate: request and
   approval, cancellation, interruption and recovery, close, reopen and Quit,
   and each access mode in the active scope produce their applicable results.
   Each failure is repaired or returned to the owner for disposition.
   Threshold: the set of access modes is not settled between the records: the
   punchlist says three; DEL-01-05 records account and local only.
   - Owning: DEL-09-02, DEL-01-01 to DEL-01-05.
4. **Installed custody and keychain protection.** *(lifted: punchlist P4)* On
   the installed candidate, supplier custody holds, and the person's in-App
   act "Protect registered workflows with your keychain" enrolls protection,
   stores the approval policy in the keychain and admits a sealed workflow
   after a cold start.
   - Owning: DEL-01-04, DEL-01-06, DEL-09-02.
5. **Live SWBPIPE journey.** *(lifted: punchlist P5; PRD V4-REP-01;
   `docs/EXAMINATION.md` §7, V4-EXM-20)* One live embedded journey in SWBPIPE
   runs from a person's request to that person's acceptance, with the actual
   host, model and configuration, controlled application, truthful outcomes
   and the applicable lifecycle and recovery evidence.
   - Owning: DEL-09-07, DEL-09-06; SWBPIPE's side belongs to SWBPIPE's own
     Agent 0.
6. **Supplier and notices.** *(lifted: punchlist P6)* The selected supplier
   pin is qualified, and every applicable shipped component has its notice and
   source association. No coverage gap is left unresolved at release.
   Threshold: complete coverage of the applicable shipped set.
   - Owning: DEL-01-01, DEL-01-06.
7. **Final candidate.** *(lifted: punchlist P7; execution basis release list
   item 3)* The package built from the finished source has verified resource,
   profile and supplier identity, is signed, notarized and stapled, and passes
   a quarantined install and launch on that same subject.
   - Owning: DEL-01-06.
8. **Terms position.** *(lifted: execution basis release list item 4; PRD
   OQ-08)* The approved supplier terms position still applies to the candidate
   as offered: free, locally run, open source, with unchanged stock sign-in.
   - Owning: DEL-01-06.
9. **Limitations.** *(lifted for key rotation: DEL-01-06; inferred for the
   rest)* The release
   states that key rotation is unavailable, as the owner accepted. Every other
   limitation remaining in criteria 1 to 8 is listed with the release and
   accepted by the owner.
   - Owning: DEL-01-06; each limitation's own deliverable.
10. **Owner product testing.** *(inferred from the 2026-11-05 correction and
    DEL-09-12's scope)* Agent 0 has recommended publication readiness, the
    owner has tested the candidate, and each finding has a disposition.
    Threshold not yet set: the records do not say which findings must close
    before publication.
    - Owning: DEL-09-12.
11. **Core loop at v3.0.1's level.** *(inferred as a 4.0.0 criterion; the
    statement is PRD V4-REP-01 and `docs/EXAMINATION.md` §7, V4-EXM-10 and
    V4-EXM-11, written for the replacement decision)* The candidate supports
    plan, execute, save a workflow, reuse it, approvals, interruption and
    restart at least at v3.0.1's level. The records do not say whether this
    gates publication or only replacement.
    - Owning: DEL-09-02, DEL-11-03.
12. **Decision packet.** *(lifted: punchlist P8; execution basis release list
    item 5)* The owner has the exact final candidate, the joined results for
    criteria 1 to 11, the limits and the continuing obligations, with unrun,
    failed, blocked and limited results shown as such, for the publication
    decision and the separate replacement decision.
    - Owning: DEL-11-03, with DEL-09-12, DEL-11-01 and DEL-01-06.

## Owner rulings

Cross-cutting decisions that shape the release, as recorded in App.

- **Both journeys before shipment** (2026-11-03). The primary journey is "set
  up a project, select an existing workflow, run it through completion."; the
  owner confirmed "both journeys now before 4.0.0 ships" (DEL-02-02).
- **Production identity** (2026-11-02). "1. keep the app ID. Figure out a
  feasible testing strategy." (DEL-01-06).
- **v4-focused testing** (2026-11-02). "Actually I don't want to do a lot of
  testing compared to v3. It was an ephemeral version, setting us up for v4.
  I will just test v4." (DEL-01-06).
- **Key rotation** (2026-11-02). "leave it unavailable for 4.0.0." (DEL-01-06).
- **Registered workflows across sessions** (2026-11-09). "an unchanged
  registered revision must stay usable across sessions once its identity is
  checked."; then "A. I accept your recommendation.", "B. I accept your
  recommended choice." and "C. I agree with your proposal." (DEL-02-02).
- **Thesis** (2026-11-10). "The thesis can be exported in the App that's fine,
  but it then otherwise lives in Library. Point to that version. That's what
  will be maintained." (`docs/PRD.md` §11).

Recorded without the owner's quoted words, so not listed above as rulings:
the 2026-10-28 selection of the full public release including the SWBPIPE
journey; Windows after the initial macOS release (2026-10-30); the free,
locally run, open-source offering and the approved terms disposition
(2026-10-30); the omission of standalone API-key access; v3's overall visual
form as the UI reference; and development testing by agents (2026-11-05).

## Reserved to the owner

- Acceptance of this target, and any change to its criteria or values.
- The publication decision, the replacement of v3.0.1 and professional
  reliance: three separate acts (PRD §8; execution basis).
- Acceptance of each release limitation, and the disposition of failures
  returned under criterion 3.
- Changes to PRD commitments and acceptance criteria, releases and lifting
  holds (`AGENTS.md`).
- Sign-in and any use of credentials; confirmation of the bundle, service,
  account and keychain group; the Apple App ID and profile; signing and
  notarization (execution basis, "Owner inputs that keep lanes moving").
- Exact approval of each deferred notice download, naming the file, source and
  size (`AGENTS.md`; DEL-01-06).
- Whether each pending interpretation gates 4.0.0: LOOP (DEL-05-01), ACT
  (DEL-04-01), record store (DEL-04-03) and PANEL F-12 (DEL-05-02).
- Any acquisition or spend, and repository settings, protections and required
  checks.
