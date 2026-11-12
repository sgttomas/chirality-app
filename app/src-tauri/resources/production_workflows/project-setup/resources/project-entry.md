# Project entry and standing instructions

A Chirality project repository gives its agents one predictable route in. The
same few surfaces answer the same questions in every project, so an agent, the
owner or another project's Agent 0 can orient without learning a new layout.

Use this convention when standing up a project, revising its entry or standing
instructions, or reviewing its entry arrangement. Preserve a project's accepted
layout until its own authority changes it. Adapt the suggested arrangement to
that project's purpose and accepted basis.

## The surfaces

| Surface | Question it answers | Changes |
| --- | --- | --- |
| `init-prompt.md` | Who am I here, and where do I go next? | Rarely |
| `AGENTS.md` (with `CLAUDE.md` = `@AGENTS.md`) | What authority, boundaries and standing rules apply, what is the current course, and how do I find and carry work? | When authority, a standing rule, the course or the phase changes |
| `docs/` | What is the product meant to be? (PRD and companions) | Through the project's commitment process |
| `execution/` | What is each part of the product, and what must it achieve? (`PKG-nn/DEL-nn-nn/`, `_Decomposition/`) | When the product's definition changes |
| `tools/`, `workflows/` | What mechanical checks and local methods exist? | With the tool or method |

The first two are the instruction entry layer: how an agent enters and keeps
operating. There is no `init/` folder and no `loop/LOOP_INIT.md`. The next two
say what the product is; the last row is what an agent works with.

## `init-prompt.md`

A short, reusable prompt the owner sends to start an Agent 0 session. It:

1. resolves `REPO_ROOT` and verifies the checkout's identity (`owner/repo`);
2. confirms that the checkout's `AGENTS.md` is the one on the repository's
   default branch, and reports any difference before relying on it. A
   deliberately older task branch can be right; a silently stale checkout is
   not;
3. reads `AGENTS.md`;
4. resolves the selected Library from `AGENTS.md` (or this repository's own
   source when maintaining the Library) and reads the entry role
   (`agents/AGENT_HELP_HUMAN.md`);
5. names the role and capacity (`HELP_HUMAN` as Agent 0 for this project);
6. ends: “Orient. Briefly report your understanding of the current basis and
   boundaries. Await the owner's steering.”

A project may add its own report subject, such as the Library's consumers. A
project working toward a release target also asks the first report for the path
from the current state to that target, any independent lanes it would open, and
what it needs from the owner to keep the work moving: decisions, credentials and
host conditions.

Keep the prompt free of current status. The owner sends the prompt, then sends
steering separately.

## `AGENTS.md`: standing authority and boundaries

`AGENTS.md` holds standing authority and the route into the work. The way these
projects organise work and agents is the same in every project, and an agent
does not find it unaided, so every project's file carries the same two
[common passages](#the-common-passages) near the top. Use this order of
sections, adapting the other headings to the project's accepted instructions
and existing links:

1. **Identity and course.** "This repository owns *X*", the accepted PRD and
   decomposition, and the current standing in a sentence, such as a release
   target linked to where it is defined. *(Local.)*
2. **Where things are.** A short map of local surfaces when the layout is not
   self-evident. *(Local, optional.)*
3. **Posture for this phase.** *(A selected [posture](#posture-for-the-phase),
   or none; local slots.)*
4. **How the work is organised.** *(Common passage; local slots.)*
5. **How agents are organised.** *(Common passage.)*
6. **The selected Library and methods.** *(Shared text, local selection.)*
7. **Coordination between projects.** One Agent 0 per project, messaging in
   T3 Code, and what a message does and does not carry. *(Shared text.)*
8. **Root relationship.** What Root may and may not do in this repository.
   *(Shared text; Root states the reverse side in its own file.)*
9. **Verification and authority.** *(Shared tiers; local high-consequence list,
   grants, delegations and reservations.)*
10. **Standing Git grant and Git conventions.** *(Scoped to this repository.)*
11. **What the repository keeps.** *(Shared text.)*
12. **Local boundaries.** Holds, private data, IP, hardware, release
    reservations and other limits that apply only here. *(Local.)*

A local rule stays beside the action it governs; it is not moved under one
"local" heading. Anything distinctive in how work is carried in a project, such
as platform lanes or a publication route, stays with the section it bears on.

### The common passages

The two passages are the same words in every project. A project fills the
named local slots and changes nothing else. A change to the wording is made
here first and adopted by each project deliberately; no check enforces
byte-equality.

Copy everything inside the fence below, from `## How the work is organised` to
the sentence on models and effort. The fence here uses four backticks because
the first passage contains a three-backtick block; that inner block is part of
the passage and is copied with it. `<query>` and `DEL-nn-nn` in the inner
block are written as shown, not replaced. The slots are the two bracketed
`[LOCAL: ...]` entries, both in the first passage:

- **The list of deliverables**, in the bullet "From a purpose": where this
  project lists its deliverables, such as a deliverable register, or its
  decomposition where it keeps no register.
- **The query**, in the last paragraph of the first passage: what `<query>` is
  in this project and what it needs to run.

The second passage has no slot. The Library is its own source and selects no
edition; its file keeps the passage as written and says so in the section that
follows it.

````markdown
## How the work is organised

- A **package** (`execution/PKG-nn/`) groups related deliverables; the
  decomposition names each package and what it covers.
- A **deliverable** (`execution/PKG-nn/DEL-nn-nn/`) is one identifiable,
  composable part of the product.
- Its **scope of work** (`ScopeOfWork.md`) states what the part must achieve,
  under what conditions, and what would show that it is adequate. The scope
  leads. Code is measured against it, and where the two disagree, the
  difference is either the work to do or a finding to report.
- Its **needs** (`deliverable.yaml`) state what it relies on: the source
  (another deliverable, a document, an outside party, or one not yet known),
  what the input must provide for this use, and when that applies. A need
  describes what this part consumes; it commits no one to supply it.
- Its **code paths** (the same file) point to the code, tests and other
  artifacts that bear on it. They show relevance, not exclusive ownership, and
  an empty list means none are declared. Keep them accurate.

A locality is its `ScopeOfWork.md` and `deliverable.yaml`; it has no `Work/`
folder. Code, tests, schemas,
fixtures and validation references live in the project's code locations, not
under `execution/`.

There are two ways in, and neither proves you have found everything:

- From a purpose: find the part in [LOCAL: this project's list of
  deliverables], open its scope, then ask what surrounds it.
- From changes already committed: ask which deliverables they bear on.

```sh
<query> neighborhood DEL-nn-nn    # its declared inputs, and the deliverables that consume it
<query> touches HEAD              # deliverables whose locality or code paths match that one commit
<query> touches main...HEAD       # the same for a whole branch
```

Read the scope and its needs, then the code. An input can be used when its
need's condition is met; it does not wait for the whole neighbour to be
finished. The queries show what is declared, not whether an input is fit for
your use: read the condition. A query that fails is not an empty answer: read
the files and say the check was unavailable.

Correct a scope's description only when the thing being made has materially
changed or the description is materially wrong, and correct a need the work
showed to be wrong, missing or no longer applicable in the same pull request. A changed commitment or criterion
is the owner's, unless an explicit delegation covers it. If a criterion looks wrong, cannot be met or no longer serves its purpose, say
what you found and what you would change. Decide the correction only within an
explicit delegation; otherwise it goes to the owner. Never weaken its check,
build around it or present an unmet criterion as passed. Carry on with what it
does not affect; the other criteria stay in force. Treat an
assumption you were given that turns out false the same way, taking it and its
consequence to whoever integrates your work.

[LOCAL: what `<query>` is here and what it needs to run.]

## How agents are organised

- **Agent 0** has the perspective of the whole project: its purpose, the
  choices the owner has reserved, and how the undertakings in progress fit
  together. Where the owner works with one agent and no other holds that
  perspective, that agent does, whatever role it entered through.
- A **Type 1** agent has the perspective of the locality of its assignment:
  the deliverables it concerns, what they need and who relies on them. It
  works in a new thread of its own, at the same level as Agent 0's thread and
  any other Type 1 thread, so that the owner can start one or work with it
  directly, as with Agent 0; that does not change its type. Type 1 agents are
  peers: none owns another's work, and Agent 0 keeps them aligned.
- A **Type 2** agent has one bounded assignment and deliberately limited
  means. It is a child of the agent that delegated it, reports back to that
  agent and starts no other agent.

Two words are kept apart here and in every assignment: a Type 1 is **started
in a new thread**, and a Type 2 is **delegated** as a child. What either is
given is its **assignment**.

How much of the work to give to other agents, and to how many, is the judgment
of the agent holding it. Agent 0 may start a Type 1 in a new thread or
delegate to Type 2 agents. A Type 1 may delegate to Type 2 agents or start
another Type 1 in a new thread. Any agent may message any other; assignments
and returns usually follow the line of assignment, which is what lets an
assigner examine a result and Agent 0 keep the undertakings aligned. A script
suits mechanical work; it does not replace an agent that holds an assignment
and answers for a result. If the host cannot start a new thread, Agent 0 tells
the owner; it does not run a Type 1 as a child.

**An assignment travels whole.** It gives the role to load, what is wanted and
why, what it rests on, what may be read and written, who integrates the
result, how it will be reviewed, which choices are not the assignee's, and how
to reach the assigner.

**A return leads with the result.** It links the evidence (for a pull request,
the reviewed head), states its limits and names who acts next. The assigner
checks it against the artifacts, and reads the assignee's session only when a
return is missing or disagrees with them. A Type 1 also tells its assigner as
it goes: when it starts another Type 1, is blocked, meets a reserved choice
or has a pull request ready. When the owner's steering changes an
undertaking's scope or how it fits with other work, it tells Agent 0 and
whoever integrates the affected work. Whoever owns a result owns its repair.

**An independent review** is made by an agent that did not write the work and
examines the artifacts and what governs them directly, not the author's
account. It says what it read and what it did not. Each review is a fresh
reviewer: a view of the work as it stands at that moment. One reading is
enough when it answers the question. When a matter takes more rounds, give
the next reviewer the earlier findings and what was done about them. Aim to
resolve within two rounds, continue past three only while still converging,
and stop at six. Unresolved findings return to whoever integrates the work,
to decide within its authority; ending the rounds waives no required check or
reserved choice.

**The INTERLOCUTOR** advises Agent 0 on direction in a session the owner opts
in; it is never an entry or default role. Agent 0 keeps the same one as
its child through the session, continued by message; a replacement starts only
if it is lost or the owner asks. It is worth most early: bring it a
consequential proposal while its advice can still change it, and carry on with
unaffected work while it answers. It also carries the continuity that a fresh
reviewer does not. In each review round it examines the findings and the
proposed response against the undertaking's purpose and the earlier rounds,
before the response is settled. That includes rounds a Type 1 runs: the
reviewer's return and the Type 1's proposed response reach it through Agent 0,
or directly where the assignment says so. Tell it how the work develops, and
consult it before a merge. Agent 0 keeps the decision; the advice needs no
sign-off and changes no reserved choice, hold or required check. It does not
replace independent review.

Each agent loads its own role text once, at the start of its session, from the
selected Library: `agents/AGENT_<ROLE>.md`.

| Relationship | Role text |
| --- | --- |
| Agent 0 | `HELP_HUMAN` |
| Type 1 | `WORKING_ITEMS`, `HELPS_HUMANS` |
| Type 2 | `TASK`, `INTERLOCUTOR` |

Which models and effort serve in each relationship comes from the owner's
steering for the session, never from a file.
````

### Posture for the phase

What changes as a project moves between phases is posture and authority, not
how the work or the agents are organised. A project selects one posture, or
none, and replaces the section whole when its phase changes.

#### Finishing toward a target

The posture is reusable; the grant is not. A project selects this posture
only where its owner has delegated the decisions it describes for that project, and it inserts
that grant itself, in the owner's words, with the project it covers. An agent does
not select it by copying another project's grant.

```markdown
## Posture for this phase: finishing toward [LOCAL: the target]

[LOCAL: one sentence on where the product stands, linked to where the target
is defined.]

[LOCAL: the owner's grant for this project, in the owner's words, and the
project it covers.]

What that means here, within the extent, conditions and reservations of that
grant, including any limit on passing those decisions on:

- Decisions follow perspective. Agent 0 decides what the target needs,
  including changes to scopes, criteria and holds, and records each decision
  by changing the text it governs. A Type 1 decides how the work within the
  locality of its assignment is done, and takes to Agent 0 a changed
  commitment, criterion or hold and whatever reaches beyond that locality. A
  Type 2 uses its judgment within its bounded assignment and does not change objectives,
  commitments or holds.
- Before deciding, look for the owner's intention in the PRD, the scopes and
  the product itself. Where it is not there, ask the owner about the
  intention, not for the decision.
- Each pull request says what was decided and why, so that the owner can
  reverse a decision without having been asked first.
- Where a scope still names the owner as the decider of a matter this grant
  transfers, the grant settles who may decide. The record names the agent
  that decided, never the owner, and a criterion that requires the owner as
  actor is corrected in its scope, with its review, before it is relied on.
- The delegation transfers project decisions. It does not supply the evidence
  a hold waits on, perform an act that belongs to another person, or reach
  resources outside the undertaking. Verification, required checks and
  independent review are unchanged, and an expected value is changed only on
  independent grounds, never to fit the implementation.
- These stay the owner's: publishing a release; licence, legal and
  professional sign-off; spending money; credentials; repository protections
  and settings. So does the verdict on the product: [LOCAL: the owner's test
  and what follows from it, such as the use cases and the owner's yes or no,
  or replacing an earlier version].
```

#### Pruning and honing

```markdown
## Posture for this phase: pruning and honing

Development is paused. The work is to remove what is wrong, misleading or
distracting, and to state the goals clearly, before the next target is set.

- Every change names, in one line, the concrete problem it removes for the
  reader of that file. A pointer that resolves is legitimate navigation.
- A removal is proposed first, as a class with examples and what refers to
  it, and made once the owner agrees.
- Work proceeds in small units, each independently reviewed and shown to the
  owner before it widens.
- Development does not resume under this posture.
```

### Rules and grants

A rule in `AGENTS.md` states what applies and why, and stands on its own: no
approval quotes, dates or decision labels beside it. The owner's exact words
are kept only where they are the grant itself and define its extent or
conditions, as with a Git grant or a delegation of decisions. Every grant says
in plain terms who may do what, in which repository or undertaking, and under
which conditions and reservations. Removing a quote changes no one's authority
to change the rule.

### Shared text

This resource is the single source of shared wording for project `AGENTS.md`
and `init-prompt.md`, including the Library's own entry documents. Record an optional reconciliation basis using
[document metadata](../../../docs/document-metadata.md#library-derivation)
after the corresponding comparison has been completed.

Preserve source identity and relied-on section anchors when adapting names,
scope and arrangement. Apply grants, delegations and reservations from the
project's own instructions. Submit shared-wording changes through Library
review and coordinate adoption with each affected project's Agent 0. Follow the
[consumer route](../../../README.md#obtain-and-use-the-library) and
[Discovery and reliance](../../../docs/alignment-manual/README.md#discovery-and-reliance)
for adoption and source distinctions.

The common passages say how work and agents are organised, what an assignment
and a return hold, how review runs, which role text each relationship loads,
and when a scope, a need or a criterion is corrected or taken to the owner.
The text below covers the rest and repeats none of it.

- **The selected Library and methods.** The Library location on this workspace and,
  elsewhere, an owner-selected checkout or release archive of
  `sgttomas/chirality-library`. Identify the Library edition or tracked line the
  project relies on and record the resolved revision with dependent results.
  Choose pinning or tracking under the project's authority; a checkout path alone
  identifies neither. Resolve shared `agents/` and `workflows/` paths against
  the selected source; load other roles and methods on demand. Use
  `coordinated-knowledge-work` for related contributions,
  `workflows/index.json` to select others, `create-workflow` before authoring a
  reusable method. Retain source identity and expose collisions. Roles grant no
  host permissions. An assignment refers only to repository files and host
  facts. Use plain prose with spaced identifiers in assignments and messages
  to other agents. Lead owner updates with the result or decision needed.
- **Coordination between projects.** Each project has one top-level Agent 0 in
  its own T3 Code session. When work needs another project, this Agent 0
  messages that one directly, after reading its session to confirm it is
  current. A message states the need, the revision and files, and whether it
  blocks. The recipient decides within its own authority; a message carries no
  owner authority and changes nothing elsewhere. Agreed decisions are recorded
  by editing the governing text where it lives; reserved choices go to the
  owner. Do not message a project the work does not affect.
- **Root relationship.** Root reads session telemetry read-only, segregated by
  repository: session metadata in any repository, to attribute sessions, and
  message and tool content only for the repositories a query selects, leaving
  out a session that spans several repositories unless the owner selects it by
  name. The owner reviews every finding before it reaches this project. Root's Agent 0 and agents working under its assignment may change
  this project's files within work the owner has authorised, through a PR here
  under these instructions, this project's checks and its Git grant, and tell
  this project's Agent 0. What Root writes in a public repository is cleared
  for publication first. Root may also open an issue for an owner-approved
  finding cleared for publication. Routine adherence checks of this project's deliverables are
  run by this project's Agent 0 through a Library workflow.
- **Verification and authority.** Verification is proportionate: routine reversible changes are
  inspected; ordinary implementation gets a focused check; high-consequence
  changes get targeted regression checks and independent scrutiny by a separate
  agent. Never change an expected result merely to silence a failure. Owner
  reservations (commitments, acceptance criteria, risk acceptance, holds,
  releases) apply subject to applicable, unrevoked owner delegations recorded in
  the project, within their scope and conditions. Present remaining reserved
  decisions and settings/protection changes to the owner. When an owner
  instruction overrides a standing rule, note the exception in the PR and ask
  once whether the standing rule should change.
- **What the repository keeps.** Produce the work and the minimum information
  needed to review, use or recover it. Describe the change at a high level in
  the PR; the session ends there and discovery starts anew next session. A
  record needs a concrete consumer,
  acceptance requirement or recovery need. Decisions edit the text they govern,
  not append registers. No receipts, notices, run records, accounts of the
  work, recovery notes or handoff chains; never hand-maintain derived progress
  or lifecycle state. Roles and methods
  come from repository files, never host-side agent definitions or harness
  configuration. Session routes are ephemeral: find current sessions by listing
  T3 threads. Agents save no memories; durable knowledge lives in Chirality.
  Scratch holds evidence, outputs and logs, never instructions. Once work is
  integrated, delete its scratch, worktrees, branches and build output unless an
  open review, named consumer or recovery need still uses them.
- **Standing Git grant.** Record the owner's actual repository-scoped grant with their words; never write one by copying.

### Packaged product instructions

For an application that bundles agent instructions with its product, assign
those instructions to a named deliverable. Maintain canonical runtime assets in
the product's source locations. List the actual maintained and shipped paths in
`deliverable.yaml`. For generated copies, identify the maintained source and
generator.

For example, SWBPIPE DEL-16-06's canonical catalog is
`apps/desktop/src-tauri/resources/agent-capability-catalog.json`.
`tools/agent_catalog_resource.py` validates that resource against its witness
pin; the deliverable's scope governs its requirements.
Keep product build, test and CI independent of a sibling Library checkout.

The Library publishes the documents themselves for consumers to read and
identifies its edition; maintain its published documents in their Library source
homes.

### Local content

Each project fills these in for itself: the product identity; the two slots of
the common passages; the
high-consequence list for its verification tier (for example numerical
meaning, measure definitions, persistence, permissions, destructive
operations); its governance overlap paths; and its local
boundaries. Owner delegations that extend authority (for example a standing
delegation to decide wording or scope within limits) are standing authority and
belong in `AGENTS.md`, stated as [Rules and grants](#rules-and-grants) says.
When relocating an existing delegation, preserve its scope, conditions and
reservations, and the owner's words where they are the grant itself.

## Checking a project

When reviewing a project that has selected this convention, examine the
following. A difference is an observation to assess against that project's
accepted basis. Preserve that basis until the project authorizes a change:

- a root `init-prompt.md` covers the bootstrap steps above; there is no `init/`
  folder or `loop/LOOP_INIT.md`;
- `CLAUDE.md` contains only `@AGENTS.md`;
- `AGENTS.md` carries the two common passages in the words given here, with
  only the named slots filled, and says nothing elsewhere that repeats or
  contradicts them;
- `AGENTS.md` covers the other standing subjects above under the project's
  authority, retaining the selected shared meaning and identifying local
  adaptations;
- standing authority, including any Git grant and owner delegations, is in
  `AGENTS.md`, each grant saying who may do what, where and under which
  conditions and reservations, with the owner's words only where they are the
  grant itself; relocated delegations retain their scope, conditions and
  reservations;
- `AGENTS.md` narrates no session or gate history and carries no status, and
  names no model;
- its commands work from the stated working directory with their stated
  prerequisites, and links resolve from the containing document. Distinguish
  inspection or a constructed walkthrough from an observed execution result.

Report differences to the project's Agent 0 as observations; the project
decides what to change.
