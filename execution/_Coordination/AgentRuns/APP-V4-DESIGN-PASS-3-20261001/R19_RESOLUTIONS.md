# R19 rulings — after DECISION-L

Integrator: HELP_HUMAN. Inputs: DECISION-L (OWNER_DECISIONS.md), R18, the
SIWC assessment. R1–R18 stand except where amended here.

## R19-1 Workflow supply is per run, not per conversation — amends R17-8

R17-8 composed the selected workflow into the conversation's starting
instructions. OBS-2 O-5 showed those are fixed for the conversation's life,
which would bind a workflow to a conversation; the owner requires chaining
(DECISION-L). Therefore:

- **Role guidance** (product guidance + the conversation's role) is composed
  into `developerInstructions` at conversation start, as R17-8 said, and
  stays for the conversation's life (L-2). `baseInstructions` is never set.
- **A workflow** is supplied to Codex with the turn that starts its run, by
  a per-turn input. The route is chosen after OBS-3 (R19-6): the native
  `skill` input (`{type:"skill", name, path}`, stable at 0.158.0) is the
  candidate; a text input carrying the bytes, and the experimental
  `thread/settings/update` developer instructions, are the alternatives.
  The App records the exact bytes and content identity it supplied, per run.
- The new register row DEL-02-04 → DEL-02-02 proposed under R17-8 is
  re-examined: if DEL-02-04 no longer composes workflows, the supplier of
  per-run supply is the run starter (DEL-02-03 with DEL-02-02), and the row
  is dropped or re-pointed. D5, D6 and F state it.

## R19-2 Chaining — SETTLED scope (DECISION-L), INTEGRATION design

Within one conversation, runs follow one another:

- **(a) Sequential.** The person ends run A (DEL-01-02 DEF-4) or it
  completes, then selects workflow B, which starts run B in the same
  conversation. B's run record cites the prior run in that conversation as
  context (a relation, not a dependency of its identity).
- **(b) Agent-proposed.** The agent may propose the next workflow in its
  message; the App offers "Start ‹workflow›" for the person to confirm. The
  agent's proposal is never a selection; nothing starts until the person
  confirms. The confirmation is ordinary input, not a reserved act (R17-9).
- One run at a time per conversation; a run is never nested inside another
  in this pass. (c) declared chaining (a workflow naming its successor or
  calling another) is DEL-02-01's later work.
- The conversation view marks each run's start and end; the model is told
  when a run ends and which workflow, if any, is in force (the wording is
  designed after OBS-3).

## R19-3 Roles and forks (L-2)

A conversation's role is fixed for its life. "Continue as ‹role›" opens a
new conversation with that role's guidance, carrying the history by
Codex's fork where OBS-3 shows the fork takes the new guidance; otherwise it
starts fresh with a handoff summary the person sees. Root `AGENTS.md`: a
full-history fork alone does not establish a different role, so the new
conversation is always supplied its role guidance. K-9's "next idle point"
becomes "new conversations" for role guidance edits; open conversations show
"guidance changed since this conversation started" (C-17, OBS-K9 closed).

## R19-4 The other L answers, by file

- **L-1 (A):** DEL-01-05 K2-1 stands; C-11 and the home part of C-20
  resolve: one Codex process per App-owned home; DEL-01-02's DEF-5/DEF-6 and
  quit apply to each; generation identity = {App session, App home, spawn
  counter}; F records HOSTING U-12's per-home dimension.
- **L-3 (A):** DEL-01-05 reads the person's plugin setting; plugins on →
  start-up connections shown and recorded; plugins off → the App's Codex runs
  with `plugins = false` and the connections stop.
- **L-4 (A, clarified):** DEL-02-02 LS-5 stands; add recognition of entries
  byte-equal to a shipped revision and a multi-entry registration act (each
  entry's bytes bound; DEL-01-04's act control offers it for A15).
- **L-5 (A), L-6 (A), L-7 (A):** no change beyond recording; DEL-01-05 REQ-005
  reads "the Owner, who is also the App implementation owner (DECISION-L L-7)".
- **SIWC:** DEL-01-05 records the ChatGPT plan grant as an alternative
  considered, with its four triggers (ASSESSMENT_SIWC.md); the host-billing
  point joins the next-relay list.

## R19-5 Codex version drift — INTEGRATION (owner remark)

Owner: "Codex frequently updates its version in significant ways.  Pinning
can only last so long." Every design statement that rests on a supplier fact
names its version; where Codex reports a capability at run time the App reads
it rather than inferring it from the version. A version-advance check
(regenerate types, diff, rerun the OBS harnesses, list affected statements)
is proposed as a later node; its scheduling is open.

## R19-6 OBS-3 — local check (K-11 scope; owner direction "run the local check")

Same limits as OBS-2 (R17-16), and S-9 means stop and report. Items in
BRIEFS "OBS-3".

## R19-7 The workflow supply route — INTEGRATION (after OBS-3)

OBS-3 (`DEL-01-01/Design/OBS_3_0.158.0.md`) found: a `skill` input is
honoured only for a `SKILL.md` in a discovered skill root at the exact
canonical path, and is otherwise accepted and silently ignored; `mention`
supplies nothing; plain text reaches the model and `thread/read` returns its
bytes; the experimental settings update persists for the conversation and
piles up. Ruling:

- The App supplies a workflow as **a text element of the turn that starts
  the run**, carrying the registered revision's exact bytes, framed by
  App-written lines that name the workflow and revision and, when chaining,
  say the previous run ended. The framing wording is PROPOSED in DEL-02-02
  and fixed in its schema.
- The App records the bytes and their content identity per run, and checks
  them against `thread/read` (the supply evidence; R3 in RS).
- The `skill` route is a recorded alternative, with OBS-3's five mitigations,
  not used now. `thread/settings/update` is not used for workflows.
- Workflows are not placed in any discovered skill root by the App, so the
  model is not shown other registered workflows (R19-2 (b)).
- Owner of composition: DEL-02-02 composes the run-start text (it holds the
  registered revision); DEL-02-03 starts the run. DEL-02-04 composes role
  guidance only. The proposed row DEL-02-04 → DEL-02-02 is dropped.

## R19-8 Forks — DERIVED (OBS-3 W-6)

At 0.158.0 `thread/fork` ignores new instructions; a fork keeps the source's
role. "Continue as ‹role›" therefore opens a new conversation with that
role's guidance and a handoff summary the person sees and can edit before it
is sent. Forking stays available as a same-role copy of a conversation.
