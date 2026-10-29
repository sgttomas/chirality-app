# Chirality App repository instructions

This repository owns App v4. Development resumed by owner direction on
2026-10-28. Work follows the owner's current steer and the applicable product
commitments. Commitment changes, acceptance and releases remain owner decisions;
migration alone does not authorize them.

Current release pathway, delivery owners and remaining evidence are in
`execution/_Coordination/CURRENT_EXECUTION_BASIS.md`. HELP_HUMAN retains Agent 0
responsibility; Type 1 managers work in dedicated T3 sessions and communicate
through T3 chat, owning delivery through repairs, reconciliation and integration
preparation. All Type 2 TASKs/reviewers use `gpt-6.1-sol`, medium effort and
standard service (`reasoningEffort: medium`, `serviceTier: default`). These are
development-agent settings, not product model/provider selections.

Enter through `loop/LOOP_INIT.md`. Requirements and interfaces live in `docs/`;
deliverables retain their `execution/PKG-nn/DEL-nn-nn/ScopeOfWork.md`, `Design/`
and `deliverable.yaml` conventions. Reconcile changed implementation meaning
with those documents; leave unchanged commitments and historical evidence alone.
Do not modify `foundation/thesis/`.

## Shared roles and methods

| Role | Type | Contribution |
|---|---|---|
| HELP_HUMAN | 0 | Purpose, alignment and continuity with the owner |
| HELPS_HUMANS | 1 | Design workflows, tools and projects with the owner |
| WORKING_ITEMS | 1 | Own implementation, assignments and integration |
| TASK | 2 | Execute one bounded assignment; does not delegate |

The agent working with the owner holds Agent 0's responsibilities for purpose,
continuity and reserved choices, whatever role it entered through. Use only the
hierarchy the undertaking needs. Managers retain ownership through repairs and
integration; TASKs return their bounded contributions to the caller.

The shared Chirality library for this workspace is `/Users/ryan/dev/chirality`.
On another machine, use an explicitly selected checkout of
`https://github.com/sgttomas/chirality`. Resolve the shared `agents/`, `workflows/`
and `.agents/skills/` references in this section against that library, not this
App repository. Load the active role's `agents/AGENT_<ROLE>.md`; other role,
workflow and skill bodies are on demand. Roles and methods come from these local
instructions and the selected library, not host-side agent definitions. Roles
grant no additional host permissions; use actual host capabilities and return
mechanisms. Model and effort choices come from session steering.

Use the library's `workflows/coordinated-knowledge-work/WORKFLOW.md` when
coordinating related contributions into a usable result. Other methods are
indexed in its `workflows/index.json`; load only the selected method and the
resources needed for the current stage. Before creating or revising a reusable
workflow, follow its `workflows/create-workflow/WORKFLOW.md`. Load applicable
shared skills by their explicit path and respect their stated scope. Retain the
selected source identity and expose collisions rather than silently switching
between shared, project-local or packaged sources. If the selected library is
unavailable, make that limitation explicit and resolve the source before relying
on its instructions; do not silently substitute a bundled product snapshot.

Give a dispatched contribution its objective, input basis, allowed reads and
writes, integration owner, review route and reserved choices. Inspect actual
returns and retain responsibility for how they fit together. Scratch holds
evidence, outputs and at most one recovery note; governing instructions remain
in repository files and assignment briefs.

This App repository owns its work, commitments and Git lifecycle. Chirality's
Root work locality, backlog, repository-specific duties and standing Git grant
do not transfer here. Shared-library consultation does not authorize changing
Chirality, SWBPIPE or another consumer, and adopting a shared method does not
expand the authorized App scope.

## Product assets and local tools

Agent instructions for work on this project are separate from the instructions
packaged into the App. `app/src-tauri/resources/` and the local
`workflows/coordinated-knowledge-work/` test input retain their pinned source
identities. Reading a newer shared role or method does not update those assets
or establish product adoption; such changes require their own authorized work.
Ordinary build and test execution must not require a sibling Chirality checkout.
Shared input and migration provenance lives in `reference/migration/`.

Use `python3 -m tools.deliverables --project . check`, `neighborhood <DEL>`,
`impact <DEL>` or `touches <revision>` from this repository. Build/test setup
is in `app/README.md`.

## Verification and authority

Work within the owner's current steer. Use focused checks for ordinary changes;
changes affecting persistence, permissions or destructive operations require
targeted regression checks and independent scrutiny. Preserve truthful source
identity and report unrun checks as limitations. Commitments, acceptance,
releases and lifting holds remain owner decisions.

Use isolated migration branches and PRs. The migration must preserve existing
release tags and imported ancestry through merge commits; do not squash it.
No force pushes, protection bypasses, permission changes or release actions.
SWBPIPE remains in `sgttomas/chirality` and is outside this repository's scope.

Use a fresh scratch Codex home for development/tests, never `~/.codex`.
Do not sign in or use credentials without the owner. Build offline by default;
downloads require explicit permission identifying the file, source and size.
No live examination is authorized merely to verify this repository migration.

The existing Parallels guest is the owner's CAEPIPE validation VM and is
permanently off-limits to Windows development: no guest-targeted discovery,
sessions, probes, scratch, installation, configuration, Tools, power or reset
operations. Do not clone/migrate it or use its private data, settings or exchange
surfaces. Never auto-select an existing guest or publish guest identifiers.

On 2026-10-29 the owner authorized a separate Windows build guest, capped at
16 GiB RAM and run only when needed. App Agent 0 owns provisioning and private
target binding; coordinate use with SWBPIPE Windows and suspend the new guest
during exclusive windows announced by the macOS coordinator in
`dev - piping` (thread `73ba979f-d4c4-4e02-a2aa-71fd6dfb04ff`). Only a new,
explicitly identified guest may become the build target. The Windows-image
acquisition is authorized from Microsoft's official source; record the exact
file, source, size and SHA-256 before installation. Other downloads retain
their exact authorization requirements, and the VS metadata integrity hold
remains. Licensing, purchases, activation and account sign-in remain owner acts.
