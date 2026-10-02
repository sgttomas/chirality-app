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

## DECISION-K3, revised (owner, exact, 2026-10-01)

**Custody:** the owner's chat message to HELP_HUMAN, after HELP_HUMAN's
reservations above (committed at `c258af7931`).

> Never mind for K-10 and K-12 I will accept your previous recommendations.  Go forward with K-7 as instructed.  You may proceed.

**Effects, replacing the K-10 and K-12 bullets of DECISION-K3:**

- **K-10:** the option marked "recommended". The task role's guidance states
  that a task agent does not delegate, labelled "stated, not enforced"; any
  delegation a task agent makes is recorded and shown; the App does not
  override the user's Codex configuration to enforce it.
- **K-12:** the option marked "recommended". The App turns off whatever
  Codex's settings allow, shows the rest in its network view, and records
  it; the design names which is which.
- **K-7:** unchanged: only registered revisions run; drafts are tried out in
  conversation.
- "You may proceed": the design nodes start.

So, finally: K-1…K-6 and K-8…K-12 as recommended; K-7 the owner's
alternative. HELP_HUMAN's K-10 and K-12 reservations no longer apply; the
K-12 point that Codex does not report its own connections remains a design
matter for DEL-01-05.

## Sign in with ChatGPT (owner exchange, 2026-10-01/02)

Owner: "This is a brand new development and is relevant here.  Assess and
report back with recommendations before I attend to your seven follow-up
choices: https://help.openai.com/en/articles/20001410-sign-in-with-chatgpt";
then "what about the dependencies management.  How does this "sign-in with
ChatGPT" approach compare to what we were currently doing with the Codex
instance."; then "Well, there's no pressing need to go ahead with this
alternative sign-in or do you see any?"; then "btw Codex frequently updates
its version in significant ways.  Pinning can only last so long."

HELP_HUMAN's answers are in [ASSESSMENT_SIWC.md](ASSESSMENT_SIWC.md). The
recommendation the owner then accepted with L-1 and L-6 (below) is: no
pressing need; DEL-01-05 records the plan grant as an alternative considered,
with its triggers; the host-billing point goes on the next-relay list.

## DECISION-L (owner, exact, 2026-10-02)

**Custody:** the owner's chat messages to HELP_HUMAN, after the package was
presented as [DECISIONS_PENDING_2.md](DECISIONS_PENDING_2.md) (sha256 prefix
`0ecbf87aae8d4350`, committed at `7447e0f821`) and as the review page https://claude.ai/artifact/N44DW6RVzVjvrLGxpL2ris (Version 2,
with L-4 clarified at the owner's question "Regarding decision L-4 why can't
the existing workflows be declared as "registered" when they are the default
workflows I ship with the product?").

On L-2 the owner wrote:

> For L-2 I don't see much need to be able to switch from HELP_HUMAN to WORKING_ITEMS between turns.  For the most part its just HELP_HUMAN that will interface with the user.  A direct WORKING_ITEMS conversation would be done in a new conversation only.  We could consider ways to make that process easy and allow forking the conversation to do so (as is possible in Codex in general).  So I'm going to take the "New conversations only" option unless you see something I'm missing and a risk I haven't considered?

After HELP_HUMAN noted that the same constraint would confine workflow
selection to new conversations (under R17-8):

> No that's not acceptable.  We need a way to chain workflows.  If we need to go back to square one then that's what we need to do.

After HELP_HUMAN proposed supplying workflows per turn and asked what
chaining should mean ((a) sequential, (b) agent-proposed with the person
confirming, (c) declared in the workflow):

> design (a) and (b) now, run the local check.  Then for the App Design Follow-ups I will go with your recommendations for the other six of the seven decisions put to me.

**Effects:**

- **L-1:** A — a second App-owned Codex home for API-key conversations,
  sharing the person's settings; one Codex process per App home.
- **L-2 (owner's choice):** a conversation's role is fixed for its life; a
  different role is a new conversation, which the App makes easy, including
  by forking the conversation where Codex supports it. Edited guidance applies
  to new conversations. **Workflows are not bound to the conversation:** they
  can be chained within one conversation, (a) sequentially, the person
  starting the next after one ends, and (b) on the agent's proposal, the
  person confirming. (c) declared chaining is left for DEL-02-01. The local
  check runs first.
- **L-3:** A — follow the person's own plugin setting.
- **L-4:** A as clarified — shipped workflows are registered by the release;
  entries byte-equal to a shipped revision are recognized; the rest are
  registered in place, several per act allowed.
- **L-5:** A — no OS password or Touch ID check per act now.
- **L-6:** A — no sign-in or API-key observation now.
- **L-7:** A — the App implementation owner is the owner; K-1 covers both.
