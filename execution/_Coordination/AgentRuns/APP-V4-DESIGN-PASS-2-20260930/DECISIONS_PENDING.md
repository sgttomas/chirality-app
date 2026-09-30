# Decisions pending — APP-V4-DESIGN-PASS-2-20260930 (checkpoint K1)

Prepared by HELP_HUMAN from [DECISIONS_DRAFT.md](DECISIONS_DRAFT.md) (node K0,
27 choices with options, examples and costs) and the six survey reports. The
draft states options evenly; the recommendations here are the integrator's.
Nothing in this file is decided until the owner's answer is recorded in
[OWNER_DECISIONS.md](OWNER_DECISIONS.md).

Six choices are put to the owner now, because the design text of Wave B
differs by the answer. The rest are either taken by the integrator (listed in
part 2, and open to being overruled), prepared in this pass for the phase
review (part 3), or already deferred (part 4).

## Part 1 — asked now

### K1-1 Who asks the person for the act when a run reaches a checkpoint

The accepted requirement says that at a checkpoint "the required human act is
requested" and is recorded as done only when the person performs it. No
accepted text says who asks.

- **A. The agent asks; the product records (recommended; ruling R9-1).** The
  agent carrying out the workflow asks the person, because the checkpoint is
  part of the plan it was given. The product gives the agent the checkpoint,
  offers the person the means to act, and records what it observes. If the
  agent does not ask, nothing in the product asks; the record shows the
  checkpoint reached and the act not performed.
- **B. The product also prompts.** As A, and the App shows its own
  non-blocking notice when it sees the arrival.
- **C. Only the product prompts.**

*Why A:* it is the owner's own wording of 28 September ("I don't want
checkpoints in workflows to be programmed into the app to respond in a certain
manner … any pause or hold point or gate are the agents to manage their own
behaviour accordingly"). B and C are product behaviour on arrival, which that
answer declined. *Cost of A:* a checkpoint can be passed without anyone being
asked, and only the record shows it.

*Waits on it:* the current-phase recorder (EXEC), the record's request
element (RS), and the checkpoint sections of LOOP and PANEL.

### K1-2 Does an act performed before the checkpoint was reached count

Example: the workflow says "before the agent changes the load case, the
engineer sets the grant that allows that class of change". The grant was set
ten minutes ago and is still in force.

- **A. No (the rule in the files, PROPOSED).** The checkpoint shows "prior
  act, not counted"; the person sets the same grant again.
- **B. Yes, when the earlier act is of the required kind and the content it
  was made on is still current (recommended for the current phase).** The
  checkpoint shows the act as performed and cites the earlier act. A workflow
  that takes up the governance phase may require a fresh act.
- **C. By act kind**, or **D. declared per checkpoint.** Larger; new
  declaration elements.

*Why B:* the record stays truthful, because it cites the earlier act and its
time, and the act is already bound to its content, so an edit lapses it
either way. A adds a repeated act for an unchanged setting every time a grant
precedes its checkpoint, which is the kind of impediment the phased approach
set out to avoid. The stricter reading has a natural home in the governance
phase. *Cost of B:* a mechanical change to one rule and the expected results
of about a dozen cases across the files.

### K1-3 One act covering several items, when only some change afterwards

Example: supports S-2 and S-3 are marked checked in one act; S-3 is then
edited.

- **A. A new check on S-3 alone is enough (recommended).** The checkpoint is
  answered by two acts: the earlier one for S-2, the new one for S-3.
- **B. A new act over both supports is required.**

*Why A:* each act is bound to the content of each item, so the earlier act is
still true of S-2. B makes the person repeat a check on content that did not
change. *Cost of A:* one rule saying that two acts together can answer one
arrival; two held cases are released.

### K1-4 The App's own act control, and how the App names the person

Seven design files assume that a later App deliverable (DEL-01-04) builds the
control a person uses to perform an act on App content. That deliverable's
contract does not mention it. Separately, no file says how the App identifies
the person it records as the actor.

**The control:**

- **A. Leave it.** The gap stays in seven files.
- **D. Put the obligation into DEL-01-04's contract at the next amendment; no
  design work on it in this pass (recommended).** This pass collects the
  wording with its other proposed contract items.
- **B. Bring DEL-01-04 into this pass, for the act control only.** Needs an
  amendment first, and rests on the App's process division, which is not
  decided.

*Why D:* the requirement is already written from the consumer's side (nine
capture rules in EXEC), so the missing piece is the supplier's obligation, not
more design. B would design a control whose key property, that no automation
can operate it, depends on a process division that is still only a proposal.

**The person's identity:**

- **Record what the App can observe, and say it is not verified
  (recommended):** the name the person sets in the App, the operating-system
  account, and the Codex account when Codex reports one. Example: "marked
  checked by Ryan (name set in the App; macOS user `ryan`; identity not
  verified)".
- **Verified identity** (a Chirality sign-in or signing key): new scope, and
  it reads as governance-phase work.

*Why:* for one person on their own machine it is truthful and needs no new
mechanism; a verified identity can be added when a workflow needs it.

### K1-5 Allow list: does a category switch that is off suspend its named entries

Example: "MCP servers" is off; the list names one server, M-1.

- **A. No: a named entry is allowed on its own (recommended; the loop
  design's interim reading).** The switch means "allow everything in this
  category". With it off, only the named entries are allowed.
- **B. Yes: the switch is a master switch.** M-1 is suspended while the
  category is off.

*Why A:* it matches the requirement text ("by category … or by named
destination") and lets a person allow exactly one destination without opening
a whole category. Under B there is no way to do that.

### K1-6 What a prototype or observation may use in this pass

Today the rule is: nothing beyond the repository. Three things the design
needs cannot be had that way.

| Step | What it would settle | What it needs |
|---|---|---|
| Read two published specifications | The exact tool-call representation the host-loop test cases are written against; what evidences a stateless MCP server | Read-only network access to the two published texts |
| One live Codex turn that calls a test tool | What the App actually sees from Codex around a tool call, which is what "the App observed the arrival" has to be defined on; what a command run looks like | A model: either a chat model downloaded into LM Studio (installed on this machine; only an embedding model is present, so a download of a few GB), or the owner's Codex sign-in |

- **Recommended:** allow the read-only fetch of the two specifications now;
  for the live turn, allow a local model in LM Studio first, and ask again
  for the Codex sign-in only if the local route cannot produce a tool call.
  Every observation is a dated record at one version, not qualification. The
  content sent to the model is invented example material.
- **Alternative:** repository-only. The observation interface of an App run,
  the adapter's unobserved behaviours and the loop's representation rows then
  stay open at the phase review.

## Part 2 — taken by the integrator in this pass (open to being overruled)

| Matter | What the integrator does | Why it is not an owner question |
|---|---|---|
| Workflow registration as a recorded human act | Adds it as a named act with its own record kind | An accepted contract already requires it (DEL-02-02 AC-006) |
| The first connected operation (OI-021) | Prepares an option sheet that sets each step of the designed activity against what SWBPIPE's answers say exists. Selects nothing; claims no join | It prepares the owner's later choice |
| Which external path the design is developed against | Develops the observation-to-record mapping for both the MCP path and the command-line path, and one simulated host that offers both | The accepted basis leaves the choice to the host, and the only host on record uses a command-line tool |
| The model interface the host-loop cases are written against | Names the published Chat Completions reference as a fixture basis only, labelled as not a product selection (needs K1-6) | The loop contract forbids selecting a product protocol version; a fixture basis is not one |
| Where shared parts live (OI-014) | Writes every format as a schema with conformance fixtures, which each placement option needs; leaves placement for the phase review | The choice does not change what is written in this pass |
| Evidence route from hosting to the record; the wording after a direct application at a checkpoint | Rulings R9-7 and R9-2 | Derived from accepted texts |

## Part 3 — prepared in this pass, decided at the phase review

The consequence vocabulary for operation classes (a draft is written); the
catalog-extension promise (OI-003); the App's Rust/TypeScript division and
reference output (OI-008, U-15); the Codex account home (OI-009); the
supplier's start-up fetch and its experimental surface; whether allowing a
network destination is the same act as setting a grant (the integrator's
mapping stands meanwhile); the panel's network-destination surfaces against
DEL-05-02's contract; custody of the shared example; the PROPOSED rules as a
set; any essential host beyond the App and SWBPIPE.

## Part 4 — already deferred

The selection of the first connected operation; whether a launch setting
counts as enabling external access; where a host's loop lives; the governance
phase and how a workflow opts in; the next relay to SWBPIPE.
