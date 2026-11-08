---
name: chirality-app-standing-instructions
description: Apply repository authority, roles, verification and protected boundaries.
metadata:
  kind: instruction
  surface: standing
  upstream:
    source: workflows/project-setup/resources/project-entry.md
    edition: library-v3.3.0
---
# Chirality App repository instructions

This repository owns App v4. Work follows the owner's current steer and the
applicable product commitments. Commitment changes, acceptance and releases
remain owner decisions.

Current release pathway, delivery owners and remaining evidence are in
`execution/_Coordination/CURRENT_EXECUTION_BASIS.md`. HELP_HUMAN retains Agent 0
responsibility; Type 1 managers own delivery through repairs, reconciliation and
integration preparation.

macOS is the release baseline; App Agent 0 owns shared code and design.
Windows contributes at native boundaries in the same project loop while
preserving macOS checks. Assignment lanes and their recorded state live in the
execution basis linked above.

Enter through `loop/LOOP_INIT.md`. Requirements and interfaces live in `docs/`;
deliverables retain their `execution/PKG-nn/DEL-nn-nn/ScopeOfWork.md`, `Work/`
and `deliverable.yaml` conventions.

`Work/` holds the current account: findings with their reasons, working artifacts and outputs. Revise it in place rather than appending history; never rewrite fidelity copies, frozen snapshots or accepted evidence. How the work went (approval quotes, review rounds, retries, run IDs, check results) belongs in the PR description, which states what changed, why, what was checked and what remains open. Cite SHAs or hashes only where they pin something a result relies on. State a fact once and link to it.

Code that runs (implementation, tests, generators, harnesses) lives outside `execution/`, in the project's code locations, and deliverables link to it; `Work/` may keep documentation-only examples that are never run. Reconcile changed implementation meaning with affected `ScopeOfWork.md`, `Work/`
and dependency conditions in `deliverable.yaml` in the same PR before integration;
its description states the reconciliation and any remaining conditions or reserved
choices. Leave unchanged commitments and historical evidence alone.
Do not modify `foundation/thesis/`.

## Shared roles and methods

| Role | Type | Contribution |
|---|---|---|
| HELP_HUMAN | 0 | Purpose, alignment and continuity with the owner |
| HELPS_HUMANS | 1 | Design workflows, tools and projects with the owner |
| WORKING_ITEMS | 1 | Own implementation, assignments and integration |
| TASK | 2 | Execute one bounded assignment; does not delegate |
| INTERLOCUTOR | 2 | Opt-in advice to Agent 0 on its effectiveness and direction |

The agent working with the owner holds Agent 0's responsibilities for purpose,
continuity and reserved choices, whatever role it entered through. Use only the
hierarchy the undertaking needs. Managers retain ownership through repairs and
integration preparation; TASKs return their bounded contributions to the caller.

Agent 0 delegates a Type 1 role (HELPS_HUMANS or WORKING_ITEMS) to its own
standalone session or thread, never as a child within Agent 0's session or
thread. A Type 1 agent delegates to children within its own session or thread.
A WORKING_ITEMS agent may call in a HELPS_HUMANS agent directly, which like
every Type 1 runs in its own standalone session or thread; other engagements
between Type 1 agents go through Agent 0. Peers do not own one another; Agent 0
keeps them aligned. Any Type 2 role can run as a child in any session or
thread, whether Agent 0 or a Type 1 delegates it. Agent 0 gives each Type 1 its
full assignment at the start, including how to reach Agent 0. A Type 1 reports
to Agent 0 by message when it calls in a HELPS_HUMANS agent, reaches a result,
has a PR ready to merge, is blocked or meets a reserved choice, stating the
result, links to its evidence (with the reviewed head SHA for a PR), limits and
the next actor. Agent 0 checks a report against the artifacts it names and reads
the Type 1's session only when a report is missing or disagrees with them. If
the host cannot start a standalone session, Agent 0 tells the owner rather than
nesting the role.

INTERLOCUTOR is opt-in per session; it is never a direct entry or default role.
When session steering selects it, Agent 0 starts one INTERLOCUTOR session and
continues it by message for the life of the Agent 0 session; a replacement
starts only if that session is lost or the owner asks. It delegates nothing.
Agent 0 sends periodic activity summaries and consults it at least before every
PR merge, as `agents/AGENT_INTERLOCUTOR.md` describes. Independent implementation
reviews remain separate contributions. Its advice
carries no sign-off, veto, permission or override of checks, holds or owner
decisions. After three rounds without convergence on a matter, Agent 0 explains
its own view and proceeds within its authority. It needs no method for its
advisory brief; a method serves it only when that method's `compatible_roles`
name it. Writes still need explicit brief targets and actual host permission.
Selection, models and effort are not inferred.

The selected shared Library edition is `library-v3.3.0` pinned at
`ec3ee2d1b398eba1fb3227ccf93e2569df95bacd`
(`reference/library-v3.3.0/README.md`). Verify the tag and instruction source
resolve to this revision before relying on it, and record the resolved revision
with dependent results. If the shared working checkout is on another edition,
read an isolated export of the selected Git revision as that README describes;
do not read the moving checkout as the selected source. Later tags or checkout
movement do not change this selection.
The shared Chirality Library for this workspace is `/Users/ryan/dev/chirality-library`.
`CHIRALITY_LIBRARY` is the selected instruction source: that checkout only when
its HEAD resolves to the pinned revision, otherwise the verified isolated export
described in `reference/library-v3.3.0/README.md`.
On another machine, use an explicitly selected checkout or release archive of
`https://github.com/sgttomas/chirality-library`. Resolve the shared `agents/`, `workflows/`
and `.agents/skills/` references in this section against that selected source, not this
App repository. Load the active role's `agents/AGENT_<ROLE>.md`; other role,
workflow and skill bodies are on demand.
Roles grant no host permissions; model/effort choices come from session steering.

Use the library's `workflows/coordinated-knowledge-work/WORKFLOW.md` when
coordinating related contributions into a usable result. Select staffing and
completion/recovery mechanisms for the actual contribution and supported host;
a single bounded contributor needs no management hierarchy. Other methods are
indexed in its `workflows/index.json`; load only the selected method and the
resources needed for the current stage. Before creating or revising a reusable
workflow, follow its `workflows/create-workflow/WORKFLOW.md`. Load applicable
shared skills by their explicit path and respect their stated scope. Retain the
selected source identity and expose collisions rather than silently switching
between shared, project-local or packaged sources. If the selected library is
unavailable, make that limitation explicit and resolve the source before relying
on its instructions; do not silently substitute a bundled product snapshot.

Give a dispatched contribution its complete assignment in the dispatch:
objective, exact input basis, allowed reads and writes, integration owner,
review route, decision rights and stop conditions. Establish the context the
host route actually delivers or makes retrievable; carry missing applicable
rules in the brief. Recheck an established route only when relevant conditions
change, and follow host restrictions on polling or timers. Inspect actual
returns and retain responsibility for how they fit together.

Lead owner updates with the result or decision needed. Use plain prose with
spaced identifiers in messages to delegates.

This App repository owns its work, commitments and Git lifecycle. The work
locality, backlog, repository-specific duties and standing Git grant of the
Library or Root do not transfer here. Shared-library consultation does not
authorize changing the Library, Root, SWBPIPE or another consumer, and adopting
a shared method does not expand the authorized App scope.

The Library (`sgttomas/chirality-library`), Root (`sgttomas/chirality`,
private), App v4 and SWBPIPE each have their own top-level Agent 0. When work
needs another project, read its session to confirm the current Agent 0, then
message its session or thread with the need, revision/files and whether it
blocks. The recipient owns changes in its repository. A message transfers no
owner authority and changes nothing in another project. Do not message
unaffected projects.

Root measures and improves how agents deliver work across the Chirality
projects and hosts shared services. Its agents may evaluate App from session
telemetry, read-only; the owner reviews every finding. Root never changes App's
files, branches or PRs; its only action here is opening a GitHub issue for an
owner-approved finding cleared for publication. Routine adherence checks of
App's deliverables stay with App's Agent 0 under these standing instructions.
Records written before 2026-11-05 use "Root" for the former combined repository that
held the Library; its old content is in Root's Git history, not on its `main`.

## What the repository keeps

Produce the work and the minimum information needed to review, use or recover
it. A record needs a concrete consumer, acceptance requirement or recovery need.
Decisions edit the text they govern, not append registers. No routine receipts,
notices, run records or handoff chains; never hand-maintain derived progress or
lifecycle state. Keep one replaceable recovery note only where continuity needs
it. Roles and methods come from these repository instructions and the selected
Library, never host-side agent definitions or harness configuration. Session
routes are ephemeral: find current sessions by listing current sessions or
threads; the owner names sessions at each restart. Agents save no memories;
durable knowledge lives in Chirality. Scratch holds evidence, outputs and logs, never instructions.
Preserve unfinished work in reviewable PRs or an explicitly authorized durable
recovery home. Inspect exposure and CI triggers before publishing a held candidate;
keep its head unchanged unless its undertaking authorizes changes. Integrate and
reconcile contributions before cleaning up their owned branches, worktrees and scratch.
Once work is integrated, delete its scratch, worktrees, branches and build output
unless an open review, named consumer or recovery need still uses them. Keep
named recovery inputs and evidence still needed by consumers.

## Product assets and local tools

Agent instructions for work on this project are separate from the instructions
packaged into the App. DEL-02-04 maintains the versioned sources in
`execution/PKG-02/DEL-02-04/Work/instructions-v1/`; `tools/instruction_resources.py`
generates the shipped instruction copies and checks freshness. Both are declared
in that deliverable. `app/src-tauri/resources/` and the local
`workflows/coordinated-knowledge-work/` test input retain their pinned source
identities. Reading a newer shared role or method does not update those assets
or establish product adoption; such changes require their own authorized work.
Ordinary build and test execution must not require a sibling Chirality checkout.
Shared input and migration provenance lives in `reference/migration/`.

Use `python3 -m tools.deliverables --project . check`, `neighborhood <DEL>`,
`impact <DEL>` or `touches <revision>` from this repository. Build/test setup
is in `app/README.md`.

## Verification and authority

Work within the owner's current steer. Inspect routine reversible changes;
use focused checks for ordinary implementation changes;
changes affecting persistence, permissions or destructive operations require
targeted regression checks and independent scrutiny. Preserve truthful source
identity and report unrun checks as limitations. Commitments, acceptance,
releases and lifting holds remain owner decisions.

When an owner instruction overrides a standing rule, note the exception in the
PR and ask once whether the standing rule should change. Retain standing grants
and adopted rule changes in their governing instructions.

### Standing Git grant

The owner, 2026-11-07: "App must also receive the standing git grant as the
others have."

For `sgttomas/chirality-app` only, agents may commit, push, open and update PRs
within authorized work. The Agent 0 of the session that opened a PR, directly
or through its delegates, merges it after the review its change requires and
with required checks green on the exact head. Delegated agents report a PR ready
to merge and wait for Agent 0 to merge it. Explicit holds and reserved decisions
apply.
This grant excludes protection bypasses, history rewrites, force pushes,
permission changes and releases. It grants no authority in another repository.

Use isolated branches and PRs, integrate with merge commits, and preserve
existing release tags.

### Continuing boundaries

SWBPIPE is a separate project in `sgttomas/SWBPIPE`; its implementation is outside
this repository's scope. Historical Chirality commits and catalog provenance
retain their original identities.

Use a fresh scratch Codex home for development/tests, never `~/.codex`.
Do not sign in or use credentials without the owner. Build offline by default;
downloads require explicit permission identifying the file, source and size.

The existing Parallels guest is the owner's CAEPIPE validation VM and is
permanently off-limits to Windows development: no guest-targeted discovery,
sessions, probes, scratch, installation, configuration, Tools, power or reset
operations. Do not clone/migrate it or use its private data, settings or exchange
surfaces. Never auto-select an existing guest or publish guest identifiers.

The owner's corrected Windows route on 2026-10-29 supersedes the earlier
separate-build-guest/image approval: no second-local-instance acquisition,
media retrieval, setup, boot or provisioning is active or authorized to resume.
Preserve the dormant hardware and private target binding; do not alter or
publish them. Media availability or an exclusive-window CLEAR does not lift
this hold. Hosted CI is the current sufficient route for the P-03 fixture,
not product App, namespace, SQLite or durability qualification. A future exact
capability missing from hosted CI, including any cloud option, needs an owner
decision before acquisition or spend; no cloud provisioning is authorized.
The VS metadata integrity hold remains. Licensing, purchases, activation and
account sign-in remain owner acts. No guest identifiers belong in repository
files or public logs.
