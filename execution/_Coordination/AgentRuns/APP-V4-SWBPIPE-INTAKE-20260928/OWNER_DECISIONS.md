# Owner decisions — APP-V4-SWBPIPE-INTAKE-20260928

Decision ID: `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-3`. Owner: Ryan.
Recorder: HELP_HUMAN (Claude Code session).

**Custody.** The owner's chat messages in the active Claude Code session,
transcribed by the recorder on 2026-09-28. This is not a raw platform export
and carries no platform timestamp.

## Context presented

After the SWBPIPE answers were received (`RELAY_ANSWERS_SWBPIPE.md`, sha256
`64ea4e59…0689`), the recorder recommended three things:

1. Record the answers as received in the RELAY §4 ledger, with no values
   changed.
2. Run a bounded intake undertaking. It traces each answer into its dependent
   files, applies the SQ-02 consequence (no host-held checkpoint route) and the
   SQ-28 consequence (no enablement facility), and settles the 12 assumptions
   the answers contradict.
3. Defer the host joins. App v4's 60% work continues on App-side contracts and
   fixtures, and the SWBPIPE joins wait until the owner resumes SWBPIPE's
   UI-SUCCESSOR.

## Owner's answer (exact)

> "yes, do 1 and 2, and defer the host joins"

## Earlier owner messages in this sequence (exact)

- "I've sent the questions to the SWBPIPE session and that agent is working on
  answering."
- "I've asked the other agent to commit and merge their answers from their
  local worktree"

## Effects, stated at the scope decided

- **Receipt.** The answers are recorded as a SWBPIPE *answer* about SWBPIPE's
  current state. They are not a commitment, a delivered contribution or an
  adoption. The source is the SWBPIPE ROOT session (HELP_HUMAN), and the owner
  relayed them.
- **Intake.** Each answer is traced into the App/shared definitions that
  depend on it. Values change only where the App's own rules say an answer
  moves them. The intake rulings (R8) decide the contradicted assumptions.
- **Deferral of host joins.** The following wait until the owner resumes
  SWBPIPE UI-SUCCESSOR (the SWBPIPE work-graph row that resumes on the owner's
  direction):
  - the DEL-09-06 joined witness and every live XC/XT case against SWBPIPE;
  - SWBPIPE-side examination;
  - naming the App's Codex as a caller of SWBPIPE's channel.

  App v4's 60% work continues on App-side contracts, receiving definitions and
  fixtures. This defers the joins; it does not withdraw SWBPIPE as the first
  host.
- **Not decided here** (these remain SWBPIPE owner decisions, listed in the
  answers' §2):
  - resuming UI-SUCCESSOR;
  - OI-016 autonomy;
  - the durable receipt carrier;
  - PB-TBD-002;
  - the Checked-mark tranche;
  - an MCP adapter;
  - the D-58 successor;
  - DEC-051 residency;
  - a host-held checkpoint route;
  - an A13 enablement facility.

---

# Owner answers to the intake questions (2026-09-28): DECISION-4, recorded, being clarified

**Custody:** the owner's answers to a structured question in the active chat,
transcribed by the recorder. The questions were raised from
[INTAKE_MAP.md](INTAKE_MAP.md) (I2).

| Question presented | Owner's answer (exact) |
|---|---|
| D6: SWBPIPE has no host-held checkpoint route and no host loop, so no checkpoint can be enforced when an App workflow runs against SWBPIPE. How should App-run checkpointed workflows against SWBPIPE be treated? | "I don't want checkpoints in workflows to be programmed into the app to respond in a certain manner.  There too many reasons and ways for that to unnecessarily impede work.  I want the human and agent to work out the plan and any pause or hold point or gate are the agents to manage their own behaviour accordingly." |
| SWBPIPE's "embedded Runtime" direction (D-58) vs the App's minimal host loop (V4-ARC-10): what should LOOP/PANEL do? | "I don't know what the distinction is, but SWBPIPE is working from the old paradigm.  Let's discuss further." |
| SWBPIPE DEC-051 (open residency) vs V4-HOST-02 (local-only): how should this be handled? | "I can't really tell what the implications of this are without further discussion" |

## Recorder's notes

- **D6.** The answer is a direction. It amends the accepted PRD requirement
  **V4-WF-05** ("The product holds a workflow's declared checkpoints …") and
  the hold-support machinery built on it:
  - EXEC §3.6;
  - WD §4.3;
  - LOOP §2.4.4;
  - R4-2, R4-8, R5-1, R6-1 and R7-3.

  An accepted-basis amendment follows `scope-change`. Its reach is being
  clarified with the owner before R8 is written.
- **The loop and residency questions are open for discussion.** No ruling is
  made yet.

## DECISION-4 clarification (owner, exact, 2026-09-28)

The recorder asked three things:

- whether its reading of the D6 direction was right;
- whether reserved acts stand, and whether the principle applies to a host's
  embedded loop;
- for the loop and residency questions, it gave an explanation and a
  recommendation.

The owner replied:

> "1. Yes that's right.  Yes reserved acts should stand.  Yes the principle should also apply to a host's own embedded loop.  My objective is get the basic workflow and agent behaviours worked out before adding in governance layers in addition.  You may not need to do a full scope change if we consider this phased development approach, with an aim to eventually implement the more rigorous controls when it's called for.  Not all workflows should have such governance, but every workflow that needs such governance will have to be served by what we build.
> 2. keep the App's loop and panel contracts (DEL-05-01 and DEL-05-02) as the v4 direction. Add a note for SWBPIPE that its embedded plan predates D-20 and should be updated to the v4 loop when UI-SUCCESSOR resumes.
> 3. The cloud model should work using OAuth too, not just an API key.  There doesn't need to be a "default" there should just be options.  I don't know what you mean by "stray network destinations""

## Effects, stated at the scope decided

- **D4-1 Phased checkpoints.**
  - **Phase 1 (now).** A workflow's declared checkpoints are plan guidance.
    The person and the agent work out the plan, and the agents manage any
    pause, hold point or gate themselves. Neither the App nor a host's
    embedded loop enforces a hold, blocks a run, or reports a workflow
    *unsupported* because a hold cannot be enforced.
  - **In force now.** A human act is recorded as done only when the person
    performs it (the second half of V4-WF-05).
  - **Reserved acts stand.** DECISION-1 D2 (OI-001) is unchanged: the five
    reserved acts stay the person's, and a host enforces its own list through
    its operations (V4-HI-30).
  - **Governance phase (later).** Enforced checkpoints are a later layer,
    applied when a workflow needs them. Not every workflow will have them. The
    Phase-1 design must keep a path to serve every workflow that needs them:
    - declarations keep the checkpoint fields (required act, reached-when,
      subject, held actions);
    - the hold machinery and hold-support values are retained as the
      governance-phase definition, not deleted.
  - **Route.** The owner judged that a full scope change may not be needed
    under this phasing. V4-WF-05's first half ("holds … the run waits") is
    **phased to the governance layer**, not withdrawn. The recorder notes the
    phasing in the affected Design files and flags it for the next
    accepted-basis update.
- **D4-2 Loop and panel.** DEL-05-01 and DEL-05-02 keep the v4 direction:
  V4-ARC-10, the minimal Chirality loop, per D-20. A note for SWBPIPE records
  two things: SWBPIPE's embedded plan (the "embedded Runtime" adoption, and
  D-58) predates D-20, and it should be updated to the v4 loop when
  UI-SUCCESSOR resumes. That note is SWBPIPE's to act on.
- **D4-3 Model access.**
  - A cloud model works through OAuth sign-in as well as an API key.
  - There is no default between local and cloud, only options the person
    chooses among. This revises V4-HOST-01's "local by default" and its
    "API key" wording at the next accepted-basis update.
  - The "no other destination" property (V4-HOST-02) is being clarified with
    the owner.

---

# DECISION-5: V4-HOST-02, host-agent network destinations (owner, 2026-09-28)

**Custody.** The owner's chat messages, transcribed by the recorder.

**Context presented:** the V4-HOST-02 context and options A–D. The recorder
recommended B ("you-control-the-list", phased), then gave an assessment in six
points with proposed wording.

**Owner (exact):**

> "For V4-HOST-02, yes I want option B, and it should be that it can both be done proactively as an allow list (and it should allow some broad categories, like web access or not, MCP, other kinds of APIs, etc.) but also with permissions that are sought in the course of the agent's work.  At least I think I do.  What's your assessment and feedback?"

> "I would only allow MCP V2 which is stateless."

**Recorder's reading of "MCP V2".** This is the owner's existing condition
(2026-09-20): any MCP use must follow the **stateless MCP revision
2026-07-28**. It is recorded in SWBPIPE's records as the "statelessV2"
condition, with exact-client evidence in PR #827.

## Effects, stated at the scope decided

- **Revised V4-HOST-02**, for the next accepted-basis update. It replaces
  "In local operation, a host's agent sends no data to any destination other
  than the configured model server":

  > A host's agent sends data only to the model service the person selected and to destinations the person has allowed — in advance in an allow list (by category, such as web access, MCP servers or other APIs, or by named destination) or when the agent asks during its work. Nothing else is contacted: no analytics, silent provider switch or background download unless the person turns it on. Every destination contacted is recorded and shown.

- **Allow list.** It works at two levels: a category switch (web access, MCP
  servers, other APIs, …) and named destinations within each category. The
  selected model service, and its sign-in service for a chosen cloud model, are
  always allowed by the person's model choice.
- **MCP.** An MCP server is allowed only if it follows the stateless MCP
  revision 2026-07-28. A server that does not is not offered and cannot be
  allowed.
  - **Limit, stated plainly:** an MCP server or other outside process can make
    its own network calls. Unless it is sandboxed, the host can only decide
    whether to start it and record what it declares.
- **In-work permission.**
  - The agent asks; only the person grants. The agent never grants itself a
    destination.
  - A grant is scoped **once**, **this run** or **always**, for the
    destination or the category.
  - Only the requesting call waits; the agent continues other work.
  - A decline is reported to the agent as "destination not allowed by the
    person".
- **Always off unless the person turns it on:** analytics or usage reporting,
  a silent switch to another model or provider, and background downloads or
  updates.
- **Record and show.** Every destination contacted is recorded and shown, in
  any model mode. The "in local operation" qualifier is dropped.
- **Phasing** (the DECISION-4 principle):
  - **Phase 1:** the allow list (categories and named entries), in-work
    requests with scopes, nothing hidden, record and show.
  - **Governance phase:** allow lists locked by an organization, and enforced
    sandboxing of MCP and other outside processes.
- **Scope.** This governs a host's embedded agent (V4-HOST). The App's own
  Codex keeps the person's Codex configuration, approval and sandbox choices
  (Root AGENTS.md; D-GOV-43); this decision does not veto them.
- **Open to the owner's correction:**
  - point 3's person-only grant;
  - the recorder's reading of "MCP V2" above.
