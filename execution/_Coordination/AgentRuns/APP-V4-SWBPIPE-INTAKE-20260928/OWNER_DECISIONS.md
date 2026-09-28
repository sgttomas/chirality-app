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
