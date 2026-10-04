# Proposed LOOP_INIT.md (draft for HELP_HUMAN)

Drafted by a Type 2 TASK (LI) for HELP_HUMAN, run
`APP-V4-GRAPH-CLOSURE-20261004`. It is a proposal: the live
`loop/LOOP_INIT.md` is unchanged. The basis is the last two sections of
`OWNER_DECISIONS.md`. `LOOP_INIT_MAPPING.md` accounts for every paragraph
of the current file.

Drafting notes. They are not part of the proposed text.
- Revised in place to follow HELP_HUMAN's ruling GC-9 (`GC_RULINGS.md`):
  - change control now covers every deliverable's agreed interfaces, not a
    "group A" core;
  - `GROUPS.md` stays in this run's folder, and a later regrouping run
    updates the pointer;
  - the decision line now only says where decisions are recorded, because
    A5 adds the general rule to the Agent User Manual §13.

  The receipt location is unchanged.
- Repaired in place for MR's review (`reviews/MR-LOOPINIT.md`):
  - L1: entry step 2 now reads the other groups' graphs for relationships
    recorded against your group (GC-8);
  - L2: the App v3 line no longer names AUM §14, which now also holds the
    App v4 entry;
  - L3: one "Owner decisions" bullet replaces the two statements;
  - L4: Conventions keeps only the MEMORY grant and LOOP_RECEIPTS, because
    the Methods adoption line already binds the graph and receipt
    locations;
  - L5: the Codex constraint is scoped to development and test runs.
- The proposed text runs from the next heading to the end of the file. It is
  4,698 characters, about 1,236 tokens (characters / 3.8). The current file
  is 15,570 characters, about 4,100 tokens.

---

# Chirality App v4 development loop

Resolve `REPO_ROOT` from the active checkout and set `WORKING_ROOT` to
`{REPO_ROOT}/projects/chirality-app-v4`. Paths below are relative to
`WORKING_ROOT` unless they begin with `{REPO_ROOT}`.

This file binds App v4 to Root `AGENTS.md`, the active role, the bundled
workflows and the manuals. It states only what is specific to App v4. The
human's steering selects the undertaking, and its work graph carries the
state.

## Entry reading

1. Take the current editions from
   `{REPO_ROOT}/docs/alignment-manual/README.md`. Read the Agent User
   Manual's headings to three levels (`grep -nE '^#{1,3} '` on its
   Markdown), then read the Field Book in full.
2. Read the work graph of the undertaking the steering names. If it has
   none, construct one. When you construct or resume a group's graph, read
   the other groups' graphs under `execution/_Coordination/WorkGraphs/` for
   relationships recorded against your group (GC-8).

## When to read further

Go to a section:
- when you are about to make a choice it addresses;
- when something contradicts what you expected;
- before you prepare a decision for the human;
- when you enter unfamiliar work.

Read the section, not the chapter. Instructions and the human's decisions
govern; the manuals explain. Record what you read in the run evidence. If you
are unsure whether something matters, ask the human.

## Methods

Load each workflow when it is needed, as
`chirality-root:bundled:workflow:<name>`:
- `construct-local-work-graph`: App v4 adopts its graph, closeout, receipt
  and MEMORY conventions;
- `coordinated-knowledge-work`, for coordination and delegation, applied in
  proportion to the work;
- `bounded-reconciliation`, for the closeout comparisons;
- `task-management`: App v4 permits bounded intake, through WORKING_ITEMS, of
  a material, evidenced concern that has no current or identified successor
  home;
- `scope-change`, `dependency-extract`, `audit-dep-closure` and
  `project-dag`, when a change reaches the decomposition, the registers or
  the DAG.

## App v4 records

- **Basis.** `docs/PRD.md` and its companions, read through
  `execution/_Coordination/Acceptances/APP-V4-BASIS-20260926/ACCEPTANCE.md`
  and later owner decisions.
- **Owner decisions.** They are in `execution/_Coordination/Acceptances/`
  and in each run's
  `execution/_Coordination/AgentRuns/<RunID>/OWNER_DECISIONS.md`. Record new
  ones in the run's file. There is no central register.
- **Decomposition.**
  `execution/_Decomposition/checkpoint_snapshots/_LATEST_ACCEPTED.md`, as
  amended through `execution/_ScopeChange/_LATEST.md`.
- **DAG.** `execution/_DAG/_LATEST.md` and its handoff. Currency is in
  `execution/_Evaluation/DAGCurrency/_LATEST.md`. The setup rules are in
  `execution/_Coordination/_COORDINATION.md`.
- **Groups.** Groups A–E and their order are in
  `execution/_Coordination/AgentRuns/APP-V4-GRAPH-CLOSURE-20261004/GROUPS.md`.
  A later regrouping decision is recorded by its own run, and this pointer
  is then updated. Rulings GC-7 and GC-8, in that run's `GC_RULINGS.md`,
  govern relationships found later.
- **Deliverables.** `execution/PKG-*/1_Working/DEL-*/`: `ScopeOfWork.md`,
  `Design/`, `Dependencies.csv`, `_DEPENDENCIES.md`, `_STATUS.md` and
  `MEMORY.md`.
- **Code.** The code is in `app/`. Its `README.md` gives the offline build
  and the tests. App v4 has no `software-workflow.json`.
- **Change control.** Agreed interfaces in any deliverable's Design change
  only through named, reviewed changes that are propagated to their
  consumers. Log each contract issue found in implementation in
  `app/CONTRACT_ISSUES.md`.
- **SWBPIPE, PEC and Domains.** See
  `execution/_Coordination/HANDOFF_SWBPIPE_DOMAINS.md`. Their implementation
  stays with their own sessions, and the owner coordinates them.
- **App v3.** `projects/chirality-app-dev` belongs to App v3, as do its
  tools, checks and decision register. Do not apply them here.
- **Thesis.** Leave `foundation/thesis/` unchanged.

## Conventions

- **MEMORY.** Add a terse Runs entry to each affected deliverable's
  `MEMORY.md`, and create the file the first time it is needed.
- **LOOP_RECEIPTS.** `loop/LOOP_RECEIPTS.md` is a reset pointer. It is not a
  receipt chain or a recovery cursor.

## Standing constraints

- The owner assesses each stage gate.
- When you run Codex for development or tests, use a scratch home made by
  `mktemp -d`, never `~/.codex`. Configure it as `app/README.md` describes.
- Do not sign in or use credentials without the owner.
- Download nothing without the owner's explicit yes. Before asking, name
  the file, its source and its size.
- Build offline by default.
