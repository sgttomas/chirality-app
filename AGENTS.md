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
`execution/_Coordination/CURRENT_EXECUTION_BASIS.md`.

There is the work, which is the code, and what expresses its goal, which is
the scopes of work; the scope leads (the Library's
`workflows/scope-of-work/WORKFLOW.md`, "What a scope says").

Start with what you are trying to accomplish. Read the scopes you think
relevant and what you find along the way. Plan. Implement and learn. Reconcile
a scope only if the thing being made, or its description within the six parts,
materially changed; correct an affected need in the same PR. Describe the
change at a high level in the PR. The session ends there and discovery starts
anew next session.

If you conclude that a criterion is wrong, cannot be met or no longer serves
its purpose, do not change it, weaken its check or build around it. Say what
you found and what you would change. Decide it only within an explicit
delegation; otherwise it goes to the owner. The other criteria stay in force.

Never rewrite fidelity copies, frozen snapshots or accepted evidence. How the work went (approval quotes, review rounds, retries, run IDs, check results) belongs in the PR description, which states what changed, why, what was checked and what remains open. Cite SHAs or hashes only where they pin something a result relies on. State a fact once and link to it.

Code that runs (implementation, tests, generators, harnesses) lives outside `execution/`, in the project's code locations, and deliverables link to it. Leave unchanged commitments and historical evidence alone.

## Direction

The target is public App v4, version 4.0.0, defined in the execution basis
([Release target and authority](execution/_Coordination/CURRENT_EXECUTION_BASIS.md#release-target-and-authority))
and the [publication punchlist](execution/_Coordination/PUBLICATION_PUNCHLIST.md).
After the owner's steering, Agent 0 runs the work that can proceed
independently in parallel through standalone Type 1 sessions.

The owner's standing instruction (2026-11-09 00:29 UTC): "This is just a
standing instruction for you: Your top priority is to keep productive work
moving forward. Don't stall out in repetitive cycles of testing and documenting
of work. Some of that is necessary but easy to get absorbed in. Keep
development moving towards the publication goals. Tell your interlocutor this
is important for them to remind you of too, when relevant circumstances arise."

- Testing and documenting serve the next step.
- When something outside Agent 0's authority blocks work, Agent 0 brings it to
  the owner at once as one decision with a recommendation, and keeps the other
  lanes moving.
- Agent 0 acts on authority already given and does not re-ask settled decisions.
- Budgets, caps and gates that Agent 0 sets itself are its own to change, and
  Agent 0 labels them as its own.

Session routes are ephemeral: find current sessions by listing T3 threads;
repository lane records are not live dispatch routes. App and host boundaries
with SWBPIPE are in `execution/_Coordination/HANDOFF_SWBPIPE_DOMAINS.md`.

## Shared roles and methods

Use the selected Chirality Library (the Library) edition: Chirality library
3.3.0, tag `library-v3.3.0`, commit `ec3ee2d1b398eba1fb3227ccf93e2569df95bacd`
of `https://github.com/sgttomas/chirality-library`. Read it from the
release's source archive, or from an owner-selected copy of that edition
elsewhere; do not read another revision as this edition.
`reference/library-v3.3.0/README.md` records the archive digest and how to
prepare an isolated export. Shared `agents/` and `workflows/` paths in this
section resolve against that source, not this repository. Changing the
edition is a deliberate App change.

| Role | Type | Contribution |
|---|---|---|
| HELP_HUMAN | 0 | Purpose, alignment and continuity with the owner |
| HELPS_HUMANS | 1 | Design workflows, tools and projects with the owner |
| WORKING_ITEMS | 1 | Own implementation, assignments and integration |
| TASK | 2 | Execute one bounded assignment; does not delegate |
| INTERLOCUTOR | 2 | Opt-in advice to Agent 0 on its effectiveness and direction |

Use only the hierarchy the undertaking needs. 

Agent 0 delegates a Type 1 role (HELPS_HUMANS or WORKING_ITEMS) to its own
standalone session or thread, never as a child within Agent 0's session or
thread. A Type 1 agent delegates to children within its own session or thread.
A WORKING_ITEMS agent may call in a HELPS_HUMANS agent directly, which like
every Type 1 runs in its own standalone session or thread; other engagements
between Type 1 agents go through Agent 0. Peers do not own one another; Agent 0
keeps them aligned. A Type 2 role runs as a child within the session or
thread of the agent that delegates it, whether Agent 0 or a Type 1; it never
gets a standalone session. Agent 0 gives each Type 1 its
full assignment at the start, including how to reach Agent 0. A Type 1 reports
to Agent 0 by message when it calls in a HELPS_HUMANS agent, reaches a result,
has a PR ready to merge, is blocked or meets a reserved choice, stating the
result, links to its evidence (with the reviewed head SHA for a PR), limits and
the next actor. Agent 0 checks a report against the artifacts it names and reads
the Type 1's session only when a report is missing or disagrees with them. If
the host cannot start a standalone session, Agent 0 tells the owner rather than
nesting the role.

INTERLOCUTOR is opt-in per session; it is never a direct entry or default role.
When session steering selects it, Agent 0 starts one INTERLOCUTOR as a child
within its own session and continues that same child by message for the life of
the Agent 0 session; a replacement starts only if it is lost or the owner asks.
Agent 0 sends periodic activity summaries and consults it at least before every
PR merge, as `agents/AGENT_INTERLOCUTOR.md` describes. Independent implementation
reviews remain separate contributions. Its advice carries no sign-off, veto,
permission or override of checks, holds or owner decisions. A method serves it
only when that method's `compatible_roles` name it.

Use the Library's `workflows/coordinated-knowledge-work/WORKFLOW.md` when coordinating related
contributions, its `workflows/index.json` to select other methods, and its
`workflows/create-workflow/WORKFLOW.md` before creating/revising a reusable
workflow. Retain selected source identity and expose collisions instead of
silently switching sources. Roles grant no host permissions; model/effort
choices come from session steering. Give delegated work an input basis, scope,
read/write boundaries, integration/review route and reserved decisions.

Use plain prose with spaced identifiers in messages to delegates.

The Library's own work locations, duties and Git grants do not transfer to
this project. Shared-method consultation does not authorize changes to another
repository. Ordinary product build/test/CI uses this repository's maintained
tools and fixtures and must not require the Library checkout. 

## Coordination between projects

The Library (`sgttomas/chirality-library`), Root (`sgttomas/chirality`,
private), App v4 and SWBPIPE each have their own top-level Agent 0. When work
needs another project, read its session to confirm the current Agent 0, then
message it in T3 Code with the need, revision/files and whether it blocks.
The recipient owns changes in its repository. A message transfers no owner
authority and changes nothing in another project. Do not message unaffected
projects.

Root measures and improves how agents deliver work across the Chirality
projects and hosts shared services. Its agents may evaluate App from session
telemetry, read-only; the owner reviews every finding. Root's Agent 0 and its
delegates may change App's files within work the owner has authorised, through
a PR here under these instructions, and tell App's Agent 0. Root may also open
a GitHub issue for an owner-approved finding cleared for publication. Routine adherence checks of
App's deliverables stay with App's Agent 0 under these standing instructions.

## Work and verification

- **What the repository keeps.** Produce the work and the minimum information
needed to review, use or recover it. A record needs a concrete consumer,
acceptance requirement or recovery need. Decisions edit the text they govern,
not append registers. No routine receipts, notices, run records or handoff
chains; never hand-maintain derived progress or lifecycle state or manufacture
acceptance, lifecycle advancement or standing from old records. Preserve
unrelated work and accepted historical evidence. Keep one replaceable recovery
note only where continuity needs it. Roles and methods come from repository
files, never host-side agent definitions or harness configuration. Agents save
no memories; durable knowledge lives in Chirality. Scratch holds evidence,
outputs and logs, never instructions. Once work is integrated or abandoned,
each contributor deletes its scratch, worktrees, branches and build output
unless an open review, named consumer or recovery need still uses them, or the
owner asks to keep them. Before removal, check for wanted uncommitted work;
remove worktrees with `git worktree remove` so Git's records stay consistent.
  
## Standing delegation to HELP_HUMAN

- **Wording.** HELP_HUMAN may edit acceptance-criterion wording that must
change only to describe consequences of decisions the owner has already made,
with every protected fact unchanged (owner, 2026-10-19). It may also replace
ScopeOfWork, Design and acceptance wording as it recommends, without asking
first, once an independent review has examined the exact old and new text and
HELP_HUMAN is clear in the matter (owner, 2026-10-23: "You can continue to
replace wording as you recommend without asking me any more so long as an
independent review has been done and you're clear in the matter."). The PR
quotes the old and new text and the review.

Work within the owner's current steer. Inspect routine reversible changes;
use focused checks for ordinary implementation changes;
changes affecting persistence, permissions or destructive operations require
targeted regression checks and independent scrutiny. Preserve truthful source
identity and report unrun checks as limitations. Commitments, acceptance,
releases and lifting holds remain owner decisions.

When an owner instruction overrides a standing rule, note the exception in the
PR and ask once whether the standing rule should change.

### Standing Git grant

The owner, 2026-11-07: "App must also receive the standing git grant as the
others have."

For `sgttomas/chirality-app` only, agents may commit, push, open, update and merge PRs
within authorized work after the verification above and required checks pass on
the exact head. The Agent 0 of the session that opened a PR, directly or
through its delegates, merges it after the review its change requires and with
required checks green on the exact head, having first triaged any open issue
labelled `nightly` (the PR that repairs one may merge). If that session has ended, the current
Agent 0 takes that duty. Agent 0 may arm GitHub
auto-merge instead of merging by hand. It arms only after the review and any
INTERLOCUTOR consultation are done and the last push is made, against the
reviewed head, and it triages `nightly` issues when arming. It disarms before
any further push to the branch. `main` does not require an up-to-date branch:
before merging or arming, Agent 0 updates the branch and waits for a fresh run
when a PR merged since the branch's base touched the same files or the same
deliverable. Open PRs that overlap this way merge in turn: the later one stays
unarmed until the earlier has landed and the later has been updated. Delegated agents report a PR ready to
merge and wait for Agent 0 to merge it. Explicit holds and reserved decisions
apply. This grant excludes protection bypasses, history rewrites, force pushes,
permission changes and releases. Use [Git conventions](#git-conventions) below.

Preserve existing release tags.

## Git conventions

- Treat `main` as Chirality App's integration branch. Name task branches with a prefix that identifies the authoring agent, such as `codex/` or `claude/`, unless the user specifies otherwise. Integrate a PR with a merge commit (no fast-forward) unless the PR chooses otherwise.
- Use a separate worktree when the user requests isolation or when concurrent sessions make isolation proportionate, such as overlapping writes to governance surfaces, risky refactors, or tool interference. Do not require a worktree for every change. High-risk overlap paths here include `AGENTS.md`, governance documents under `docs/`, accepted snapshots, generated derivative packages, and shared control roots such as `execution/_Coordination/`; warn when two lanes overlap on them.
- Close authorized work through a PR. No separate commit, push, PR or merge approval is needed when its conditions hold. Use the configured authenticated identity and retain truthful authorship; agent review is not personal owner review.
- Verify in proportion to consequence and confirm required checks pass on the exact head. Obtain independent scrutiny where the grant requires it. Clear blocking findings and reassess affected checks after candidate changes; a passing rerun does not establish that a known defect was repaired. Verify the source HEAD when merging.
- Git integration, human acceptance and product release remain distinct.
- Update affected live consumers and references in the change itself.

For implementation and closeout in this repository:

- Separate maintained source and test fixtures from run evidence. Permanent tests and public packaging should not depend on a dated agent-run directory. Keep useful regression cases in the maintained test suite; preserve one-time migration evidence as history rather than requiring the migration to be re-proved forever.
- Keep working summaries revisable until a real review or acceptance boundary. Format authored documents and generate derived files before binding their bytes for review. Preserve raw tool output verbatim when needed; do not make it an editable, style-normalized source artifact. A later correction needs evidence for the affected change, not another full copy of the previous packet.
- Cosmetic whitespace is not a commit or merge blocker. Use formatting diagnostics only when helpful; preserve intentional Markdown hard breaks and raw evidence rather than creating repair cycles for their appearance.
- Judge a check by the failure it prevents. Keep behavioral, permission, containment, compatibility, and reproducibility checks. Remove obsolete migration assertions, incidental wording/order assertions, and duplicate evidence checks when they protect no current requirement. When a governing instrument requires such a check, propose the corresponding amendment rather than silently bypassing it or adding another workaround.
- Match preflight to the actual candidate and affected CI entrypoints. Scope candidate checks to files being submitted, and run required range checks against the complete PR diff. Re-run affected checks after repairs; repeat broader suites only when the change or an unresolved concern warrants it.

## Working locality

Work at this repository root. Start from the affected
`execution/PKG-nn/DEL-nn-nn/`, which is two files: `ScopeOfWork.md` and the
dependency conditions in `deliverable.yaml`. Consult `docs/PRD.md` and its
companions for requirements and interfaces involved in this slice, not as a
compulsory census.

From the repository root:

```sh
python3 -m tools.deliverables --project . neighborhood DEL-nn-nn
```

`tools/deliverables/README.md` gives the other queries (`impact`, `touches`,
`check`, `dag-diff`). Update needs only when their conditions change.

Each implementation return must reconcile its affected `ScopeOfWork.md` and
dependency conditions in `deliverable.yaml`. The implementation
manager owns this reconciliation: it carries the rule into every brief and
names the affected deliverables, and TASKs report the effects of their slices.
Update changed meaning in the same PR; leave unchanged declarations alone, and
say so briefly when nothing needs editing. The return identifies the
reconciliation and any remaining conditions or reserved choices. Agent 0
checks that the implementation and its declarations agree before integration.

Carry each unit to a usable, verified result. Record improvements found along
the way as remaining items, and take them up after the unit unless they correct
a wrong output or block the goal.

## Build and verification

**Windows development.** macOS is the release baseline and leads. App Agent 0 owns shared code, schemas and design and decides changes to them; Windows work runs as a WORKING_ITEMS manager in this project's Agent 0 loop, adds platform implementations at the native boundaries recorded in `execution/_Coordination/WINDOWS_UNDERTAKING.md` and does not change shared behaviour without Agent 0's agreement. Where a Windows change overlaps macOS work, the macOS work integrates first and the Windows change merges main and regenerates generated files with their generators, never by hand. A Windows change must pass the macOS checks unchanged. Local host resources go to macOS work first; Windows evidence comes from hosted Windows runners (`.github/workflows/windows-process-fixtures.yml`, `.github/workflows/windows-stop-fixtures.yml`). Coordinate through draft PRs that list the shared files they touch before editing; record agreed shared-design decisions by editing the governing text. The guest and acquisition holds are in [Continuing boundaries](#continuing-boundaries).

`tools/ci/select_checks.py` selects checks from the committed change, as
`docs/CI_SELECTION.md` describes. From the repository root, with full commit
SHAs:

```sh
python3 tools/ci/select_checks.py select --event pull_request --base <base-sha> --head <head-sha>
python3 tools/ci/select_checks.py inventory
```

The repository checks are the
commands of the `repository-checks` job in
`.github/workflows/governance-harness.yml`; run locally the ones a change
affects, for example `python3 -m pytest -q tools/ci tools/validation`. The
hosted `harness` result on the exact PR head is the merge check. Broad suites
run for an identified need or release preparation; the nightly full suite
covers main.

Ordinary builds and tests run concurrently across isolated worktrees; do not
serialise them for caution. App has no shared memory guard or slot prerequisite
for them. Rust tests stay
serial inside one Cargo run because they share process state
(`app/README.md`). Isolation belongs to a measurement whose evidence concurrent
load would disturb.

## Product assets and local tools

Agent instructions for work on this project are separate from the instructions
packaged into the App. DEL-02-04 maintains the shipped instructions in
`app/src-tauri/resources/instructions/`, declared
in that deliverable. `app/src-tauri/resources/` retains its pinned source
identities. Reading a newer shared role or method does not update those assets
or establish product adoption; such changes require their own authorized work.
Shared input and migration provenance lives in `reference/migration/`.
Build/test setup is in `app/README.md`.

### Continuing boundaries

Use a fresh scratch Codex home for development/tests, never `~/.codex`.
Do not sign in or use credentials without the owner. Build offline by default;
downloads, including binaries and archives, require explicit permission
identifying the file, source and size. Routine read-only inspection of public
source code and documentation text is authorized.

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
