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
| `init/init-prompt.md` | Who am I here, and where do I go next? | Rarely |
| `AGENTS.md` (with `CLAUDE.md` = `@AGENTS.md`) | What authority, boundaries and standing rules apply? | When authority or a standing rule changes |
| `loop/LOOP_INIT.md` | What is the current course, and how do I find and carry work? | When the course or the operating route changes |
| `docs/` | What is the product meant to be? (PRD and companions) | Through the project's commitment process |
| `execution/` | What work is allocated, and in what state? (`PKG-nn/DEL-nn-nn/`, `_Decomposition/`, `_Coordination/`, `_ScopeChange/`) | With the work |
| `tools/`, `workflows/` | What mechanical checks and local methods exist? | With the tool or method |

The first three are the instruction entry layer: how an agent enters and keeps operating.
The next two are what it works on; the last row is what it works with. Keep the
entry layer at the top level, separate from the execution record, so "how do I
work here now" is in the same place in every project.

## `init/init-prompt.md`

A short, reusable prompt the owner sends to start an Agent 0 session. It:

1. resolves `REPO_ROOT` and verifies the checkout's identity (`owner/repo`);
2. reads `AGENTS.md`;
3. resolves the selected Library from `AGENTS.md` (or this repository's own
   source when maintaining the Library) and reads the entry role
   (`agents/AGENT_HELP_HUMAN.md`);
4. names the role and capacity (`HELP_HUMAN` as Agent 0 for this project);
5. reads and follows `loop/LOOP_INIT.md`;
6. ends: “Orient. Briefly report your understanding of the current basis and
   boundaries. Await the owner's steering.”

A project may add its own report subject, such as the Library's consumers or
SWBPIPE's release target.

Keep the prompt free of current status; that belongs in the loop. An optional `init/README.md` tells the owner how to
use it (send the prompt, then send steering separately).

## `AGENTS.md`: standing authority and boundaries

`AGENTS.md` holds what stays true whatever the current course is. Use these
sections as a suggested skeleton, adapting their order and headings to the
project's accepted instructions and existing links:

1. **Identity and entry.** "This repository owns *X*." Enter through
   `loop/LOOP_INIT.md`. *(Local: the one-line product identity.)*
2. **Where things are** *(optional)*. A short map of local surfaces when the
   layout is not self-evident.
3. **Shared roles and methods.** The Library selection, the role table, and how
   roles and methods load. *(Shared text, plus the local Library selection.)*
4. **Coordination between projects.** One Agent 0 per project, messaging in
   T3 Code, and what a message does and does not carry. *(Shared text.)*
5. **Root relationship.** What Root may and may not do in this repository.
   *(Shared text; Root states the reverse side in its own file.)*
6. **Work and verification.** Deliverable localities, same-change
   reconciliation, deliverable queries, and the three verification tiers.
   *(Shared text, plus the local high-consequence list and query invocation.)*
7. **Standing Git grant and Git conventions.** *(Shared text, scoped to this
   repository, with the owner's grant quoted.)*
8. **Local boundaries.** Holds, private data, IP, hardware, release
   reservations and other limits that apply only here. *(Local.)*

Within a project, `AGENTS.md` and the loop do not repeat each other. A rule
lives in one of them, and the other links to it where a reader needs it.

### Shared text

This resource is the single source of shared wording for project `AGENTS.md`,
`init/init-prompt.md` and `loop/LOOP_INIT.md`, including the Library's own entry
documents. Record an optional reconciliation basis using
[document metadata](../../../docs/document-metadata.md#library-derivation)
after the corresponding comparison has been completed.

Preserve source identity and relied-on section anchors when adapting names,
scope and arrangement. Apply grants, delegations and reservations from the
project's own instructions. Submit shared-wording changes through Library
review and coordinate adoption with each affected project's Agent 0. Follow the
[consumer route](../../../README.md#obtain-and-use-the-library) and
[Discovery and reliance](../../../docs/alignment-manual/README.md#discovery-and-reliance)
for adoption and source distinctions.

- **Shared roles and methods.** The Library location on this workspace and,
  elsewhere, an owner-selected checkout or release archive of
  `sgttomas/chirality-library`. Identify the Library edition or tracked line the
  project relies on and record the resolved revision with dependent results.
  Choose pinning or tracking under the project's authority; a checkout path alone
  identifies neither. Use the role table (HELP_HUMAN 0, HELPS_HUMANS 1,
  WORKING_ITEMS 1, TASK 2, INTERLOCUTOR 2) and the selected source's exact
  [`agents/AGENT_INTERLOCUTOR.md`](../../../agents/AGENT_INTERLOCUTOR.md)
  for INTERLOCUTOR instructions. When session steering selects it, Agent 0
  starts one INTERLOCUTOR session and continues it by message for the life of
  the Agent 0 session; a replacement starts only if that session is lost or the
  owner asks. The owner-facing agent holds Agent 0's
  responsibilities whatever role it entered through. Load the active role file; other roles and methods
  on demand. Use `coordinated-knowledge-work` for related contributions,
  `workflows/index.json` to select others, `create-workflow` before authoring a
  reusable method. Retain source identity and expose collisions. Roles grant no
  host permissions; model and effort come from session steering. Give a
  dispatched agent its brief in full in the dispatch, referring only to
  repository files and host facts. Use plain prose with spaced identifiers in
  messages to delegates. Lead owner updates with the result or decision needed.
  The selected coordination method supplies
  the assignment contents, including objective, basis, writes, integration
  ownership and review/decision rights.
- **Coordination between projects.** Each project has one top-level Agent 0 in
  its own T3 Code session. When work needs another project, this Agent 0
  messages that one directly, after reading its session to confirm it is
  current. A message states the need, the revision and files, and whether it
  blocks. The recipient decides within its own authority; a message carries no
  owner authority and changes nothing elsewhere. Agreed decisions are recorded
  by editing the governing text where it lives; reserved choices go to the
  owner. Do not message a project the work does not affect.
- **Root relationship.** Root reads session telemetry read-only, segregated by
  repository; the owner reviews every finding; Root changes no files, branches
  or PRs here and may only open an issue for an owner-approved finding cleared
  for publication. Routine adherence checks of this project's deliverables are
  run by this project's Agent 0 through a Library workflow.
- **Work and verification.** `execution/PKG-nn/DEL-nn-nn/` holds
  `ScopeOfWork.md` (commitments) and `deliverable.yaml` (needs and pointers).

  `Work/` holds the current account: findings with their reasons, working artifacts and outputs. Revise it in place rather than appending history; never rewrite fidelity copies, frozen snapshots or accepted evidence. How the work went (approval quotes, review rounds, retries, run IDs, check results) belongs in the PR description, which states what changed, why, what was checked and what remains open. Cite SHAs or hashes only where they pin something a result relies on. State a fact once and link to it.

  Reconcile changed
  meaning and dependency conditions in the same change; leave unchanged declarations
  alone. Verification is proportionate: routine reversible changes are
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
  needed to review, use or recover it. A record needs a concrete consumer,
  acceptance requirement or recovery need. Decisions edit the text they govern,
  not append registers. No routine receipts, notices, run records or handoff
  chains; never hand-maintain derived progress or lifecycle state. Keep one
  replaceable recovery note only where continuity needs it. Roles and methods
  come from repository files, never host-side agent definitions or harness
  configuration. Session routes are ephemeral: find current sessions by listing
  T3 threads. Agents save no memories; durable knowledge lives in Chirality.
  Scratch holds evidence, outputs and logs, never instructions. Once work is
  integrated, delete its scratch, worktrees, branches and build output unless an
  open review, named consumer or recovery need still uses them.
- **Standing Git grant.** Record the owner's actual repository-scoped grant with their words; never write one by copying.

### Packaged product instructions

For an application that bundles agent instructions with its product, assign
those instructions to a named deliverable. Maintain their source in that
locality's `Work/`, generate the shipped copy from it, and list both source and
shipped paths in `deliverable.yaml`. For example, SWBPIPE DEL-16-06 maintains
`Work/agent-capability-catalog.json`, generates it through
`tools/agent_catalog_resource.py`, and ships
`apps/desktop/src-tauri/resources/agent-capability-catalog.json`.
Keep product build, test and CI independent of a sibling Library checkout.

The Library publishes the documents themselves for consumers to read and
identifies its edition; maintain its published documents in their Library source
homes.

### Local content

Each project fills these in for itself: the product identity; the
high-consequence list for its verification tier (for example numerical
meaning, measure definitions, persistence, permissions, destructive
operations); its query invocation; its governance overlap paths; and its local
boundaries. Owner delegations that extend authority (for example a standing
delegation to decide wording or scope within limits) are standing authority and
belong in `AGENTS.md`, with the owner's wording. When relocating an existing
delegation, preserve its scope, conditions, reservations and owner wording, and
link to it from the loop.

## `loop/LOOP_INIT.md`: current course and operating route

The loop is where an initialized Agent 0 learns what the project is doing now
and how work is found and carried. Typical parts:

1. **Course and basis.** One paragraph: the product, the accepted PRD and
   decomposition, and the current standing in a sentence (for example a release
   target, or "edition N is published; work comes from new steering"). Link
   to the record that holds the detail instead of narrating gate history.
2. **Locate the selected work.** From the steering to the owning
   `DEL-nn-nn`: its `ScopeOfWork.md`, `Work/`, `deliverable.yaml`, then the PRD
   clauses this slice needs. Give the query commands with a worked example. A
   failed query is not an empty result.
3. **Select methods.** How to resolve Library workflows from this project,
   retaining qualified source identity and exposing collisions with local methods.
   Keep a top-level `workflows/` for local methods; obtain shared methods from
   the selected Library. Do not infer a different selection from a matching name.
4. **Carry it through.** Agent 0 and implementation-owner responsibilities,
   ordering constraints, reconciliation in the same PR, check selection and the
   hosted merge check. An opted-in session sends consultations to its existing
   INTERLOCUTOR session.
5. **Project-specific cycle.** What is distinctive here: a release climb,
   platform lanes, a review rule, a publication route, how contributions from
   other projects enter.

Keep it as short as its content allows. Status that changes weekly belongs in a
coordination record the loop links to (for example
`execution/_Coordination/CURRENT_EXECUTION_BASIS.md`), not in the loop or in
`AGENTS.md`. Git and accepted snapshots preserve earlier loops; an archive
folder needs a named consumer.

## Checking a project

When reviewing a project that has selected this convention, examine the
following. A difference is an observation to assess against that project's
accepted basis. Preserve that basis until the project authorizes a change:

- `init/init-prompt.md` covers the bootstrap steps above and leads to
  `loop/LOOP_INIT.md`;
- `CLAUDE.md` contains only `@AGENTS.md`;
- `AGENTS.md` covers the standing subjects above under the project's authority,
  retaining the selected shared meaning and identifying local adaptations;
- standing authority, including any Git grant and owner delegations, is in
  `AGENTS.md` with the owner's words; relocated delegations retain their scope,
  conditions and reservations, and the loop links to them;
- neither `AGENTS.md` nor the loop narrates session or gate history;
- the loop's commands work from the stated working directory with their stated
  prerequisites, and links resolve from the containing document. Distinguish
  inspection or a constructed walkthrough from an observed execution result.

Report differences to the project's Agent 0 as observations; the project
decides what to change.
