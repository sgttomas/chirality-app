# Owner decisions — APP-V4-DESIGN-PASS-3-20261001

Exact owner text, as given in the chat session with HELP_HUMAN. Custody: the
session transcript; recorded here by HELP_HUMAN. A record here is not a claim
that the owner reviewed any file.

## Start direction (2026-10-01)

> Proceed as recommended.

What HELP_HUMAN recommended, in the message the owner answered (after
`APP-V4-DESIGN-PASS-2-20260930` closed with PR #1069):

1. "A short decision sitting first": the phase-review items that would
   shape a design pass on the standalone App deliverables, brought as a
   decision page with recommendations.
2. "Design pass on the standalone App deliverables": "request recovery, the
   act control, sign-in and model access, workflow registration and roles",
   planned through DAG-003.
3. "Apply this pass's contract proposals as a third amendment … folded in
   when it's cheapest, since the amendment can also carry contract changes
   from the next pass."

"My recommendation is 2 then 1, with 3 folded in when it's cheapest".

**Reading (HELP_HUMAN's interpretation, not owner text):**

- The deliverables are the standalone-App set that first-increment
  DECISION-1 D1 left "for a later undertaking": DEL-01-02, DEL-01-03,
  DEL-01-04, DEL-01-05, DEL-02-02 and DEL-02-04. This direction starts them.
- The decision sitting comes first; the design pass follows its answers.
- The amendment (SCA-V4-003) carrying the second pass's 42 ScopeOfWork
  proposals and this pass's is a later node of this run, placed where it
  costs least, with its own owner checkpoints.

## Standing directions that apply

- Git: monitor PRs and merge once CI is green, after an independent review
  of the candidate finds nothing blocking.
- Executors: "Ensure you are using `opus-5.5` models on `high` reasoning for
  your Type 1 and Type 2 agent instances."
- Host joins deferred (DECISION-3 of `APP-V4-SWBPIPE-INTAKE-20260928`).
- The decisions of the earlier runs, including DECISION-K1 of
  `APP-V4-DESIGN-PASS-2-20260930`.

## DECISION-K3 (owner, exact, 2026-10-01)

**Custody:** the owner's chat message to HELP_HUMAN, after the package was
presented as [DECISIONS_PENDING.md](DECISIONS_PENDING.md) (sha256 prefix
`431ec4eb22a0b913`, committed at `876a9d7254`) and as the review page
https://claude.ai/artifact/Kfh49j4xbKi9sqZsf8XSGx (Version 1).

> I accept 1-6, 8-9, and 11 as recommended.  For 7 only registered, drafts are conversations.  For 10 enforce with config override. For 12 accept and record it.  And reservations about my direction that differs from your recommendations?

**Effects** (numbers are DECISIONS_PENDING.md Part 1's K-1…K-12):

- **K-1, K-2, K-3, K-4, K-5, K-6, K-8, K-9, K-11:** the option marked
  "recommended" in DECISIONS_PENDING.md, at the scope stated there.
- **K-7 (owner's alternative).** Only registered revisions run. A draft is
  tried out in an ordinary conversation, which is not a run of any workflow
  identity. The existing statements that a draft cannot be selected for a run
  (EXEC HR-3, TR-1/T-1; WD OS-2/OS-3) stand.
- **K-10 (owner's alternative).** "A task agent does not delegate" is
  enforced by a per-conversation Codex configuration override for task-role
  conversations, not by guidance alone.
- **K-12 (owner's alternative).** Codex's start-up traffic is accepted as the
  supplier's behaviour and recorded; the App does not turn it off.
- **Part 2:** not objected to; the integrator takes those matters as listed.

**The owner asked for reservations.** HELP_HUMAN's answer (not owner text):

- **K-7:** none of substance. It matches three existing files, so less
  changes. A trial in conversation leaves no workflow-run record, and each
  refinement that needs a recorded run becomes a registered revision (K-6
  keeps them all).
- **K-10:** (a) Root `AGENTS.md` says the App does not "veto the user's Codex
  configuration". An override scoped to task-role conversations, shown and
  recorded, leaves the user's own configuration untouched, but the doctrine
  sentence does not say so; the design records this as an instruction-change
  notice, not a change it makes. (b) No mechanism is observed at 0.158.0:
  `multiAgentMode` is marked "@deprecated Ignored", no client method controls
  delegation, and a task agent is a child Codex starts itself, so the
  override must reach the child (for example through the task role's native
  agent configuration). The design proposes the override, an observation
  under K-11 tests it, and if Codex offers no working lever the App says "not
  enforced" and records any delegation, rather than claiming enforcement.
- **K-12:** (a) Codex does not report its own connections in its event
  stream, so "record" needs the App's own observation of its Codex process,
  or a per-version list taken from an observation; the design names which.
  (b) A person using only a local model, not signed in, may expect nothing
  to leave the machine; the record should be visible to them, not only kept.
  (c) The App holds itself to less than DECISION-5 asks of a host's agent
  (only the chosen model service and allowed destinations), though that
  decision covers the agent's sending, not the supplier's own traffic.
