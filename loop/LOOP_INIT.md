# Chirality App v4 development loop

Resolve `REPO_ROOT` from the active checkout and set `WORKING_ROOT` to
`{REPO_ROOT}/projects/chirality-app-v4`. Paths below are relative to `WORKING_ROOT`.
Enter through `init/dev-loop-init-prompt.md` with the selected role and the
human's steering. This file owns the recurring development-loop procedure;
Root `AGENTS.md`, the active role, and the accepted App v4 basis supply
applicable responsibilities and boundaries. Read project `AGENTS.md` if one
is subsequently established; do not substitute another project's instructions.
Keep this file evergreen: undertaking selection and graph references come from
the init steering and subsequent human directions; execution state lives in the
selected work graph.

## Loop contract

Repeat the following cycle within the human-selected undertaking:

1. Recover actual state and steering; establish or update the current work graph.
2. Select contributions whose required inputs and write ownership permit work.
3. Commission and execute bounded work, examine returns, repair and integrate.
4. Update the graph with actual results, changed inputs and remaining work.
5. Continue with the next ready contribution. Prepare reserved human decisions
   while independent authorized work proceeds; pause dependent work at its
   actual boundary and resume it when the required decision or input arrives.
6. Once the promised production and evidence are integrated, perform the
   planned bounded closeout and final review. Findings that reveal missing
   required work return to the graph and repeat the affected cycle.
7. Merge the final PR when its conditions hold, report the result and stop the
   undertaking. Starting another undertaking requires applicable human steering.

An intermediate PR, child return or session boundary does not end the loop.
On interruption, preserve the graph, active operations, evidence and next safe
action so the next session can resume. The sections below define this recurring
procedure; they are not a one-time reading checklist.

## Manual-led v4 practice

This project loop applies the owner's instruction to base v4 practice on:

- [Project Management for Human–Agent Teams, Consolidated v7](../../../docs/alignment-manual/Project_Management_for_Human_Agent_Teams_Consolidated_v7.md): management purpose, phase transitions, production relationships and examination.
- [Chirality Agent User Manual v3](../../../docs/alignment-manual/CHIRALITY_AGENT_USER_MANUAL_v3.md): operational application, selective context, delegation, records and recovery.
- [Field Book v1](../../../docs/alignment-manual/Project_Management_for_Human_Agent_Teams_Field_Book_v1.md): a useful summary and navigation aid to the fuller explanations.

Consult the sections needed for the undertaking: PM Manual §§1.7, 3.12 and
chapter 4; Agent User Manual §§2–5, 7–13 and 18; Field Book §§4–5. Read the
manuals with the project's actual accepted basis and subsequent human steering.
Their examples and dated App-v3 entry pointers are not v4 product requirements
or automatic adoption of another project's controls. A guide describes practice;
actual decisions, selected methods, briefs and host permissions bound execution.

Keep the undertaking proportionate. A small correction does not require a new
PRD, decomposition, project-wide audit or full agent hierarchy. Proceed on
routine authorized work and prepare concrete alternatives for consequential
human decisions. Do not add a checkpoint after every contribution or PR.

## Project pointers

- Purpose and accepted seed: `docs/PRD.md` and its companion documents, read
  through `execution/_Coordination/Acceptances/APP-V4-BASIS-20260926/ACCEPTANCE.md`
  and subsequent actual owner decisions. `conceptual/DECISIONS.md` preserves
  originating decisions; it does not override later accepted directions.
- Decomposition: `execution/_Decomposition/checkpoint_snapshots/_LATEST_ACCEPTED.md`.
  Follow accepted scope amendments if subsequently established; do not assume
  an `execution/_ScopeChange/_LATEST.md` exists.
- Project graph: `execution/_DAG/_LATEST.md`, its accepted version and handoff,
  and `execution/_Evaluation/DAGCurrency/_LATEST.md`. Read actual input
  satisfaction from local `Dependencies.csv` and `_DEPENDENCIES.md`.
- Deliverables: `execution/PKG-*/1_Working/DEL-*/ScopeOfWork.md`, dependencies,
  `_STATUS.md` and any existing local run indexes. INITIALIZED establishes
  checked-contract maturity, not delivered inputs or completed implementation.
- Operating basis: `execution/_Coordination/CURRENT_EXECUTION_BASIS.md` and
  `_COORDINATION.md`, with later actual decisions. The selected PM Manual,
  Field Book and Agent User Manual are located through that basis. Preserve
  `foundation/thesis/` unchanged.
- Initial development handoff: `execution/_Coordination/HANDOFF_30_PERCENT.md`.
  It records the completed 30% gate and the originating session's restriction
  to closeout. The receiving session needs its own human steering to start
  work toward 60%; these files do not select that undertaking.
- External coordination: `execution/_Coordination/HANDOFF_SWBPIPE_DOMAINS.md`.
  SWBPIPE implementation stays with its owning session; PEC is optional and
  Domains joins later under their actual receiving conditions.
- Checks: the affected ScopeOfWork verification methods, actual candidate
  tooling and repository CI. A v4 `software-workflow.json` is not yet present;
  do not borrow v3 commands or report unconfigured checks as performed.
- Task Management: use the selected workflow's federation preflight and actual
  register discovery when a qualifying concern arises. No App v4 register is
  assumed to exist and no register or routine sweep is created by this entry.

`chirality-app-dev` remains a historical exemplar and fallback, not this loop's
working root or an automatic source of product commitments. Recover current
owner decisions through their real records rather than assuming the v3
`_DECISIONS/_REGISTER.md` structure exists here.

## 0. Read the steering and recover the situation

The init steering and subsequent human directions establish the purpose, phase,
priorities and limits. Recover the graph for that undertaking from the supplied
references and relevant project records. Read it, relevant deliverable contracts,
MEMORY run pointers, dependencies, implementation and evidence. Give a concise
reading of the intended outcome and proceed where the direction is clear.

Verify branch/worktree state, partial edits, active workers and prior integration
before repeating work. Recover the actual graph and its accepted basis when
continuing an undertaking. Preserve unrelated edits and transfer shared-file or
test-resource ownership explicitly. Missing or stale pointers require recovery
from their sources; they are not permission to restart completed work.

## 1. Construct or revise the work graph

Use `chirality-root:bundled:workflow:construct-local-work-graph` when no graph
exists or its route needs substantial revision. Relate the intended outcome to
the project DAG, deliverables and present work. Before the first DAG exists,
follow the phase steering and applicable dependency/cycle-resolution method.
For an accepted graph, establish currency before reliance when sources may
have changed. Preserve characterized SCCs as non-gating candidates; identify
the actual missing input for dependent work without holding whole groups.
Graph revision is driven by changed relationships or scope, not session entry.

Create the Git-tracked graph at
`execution/_Coordination/WorkGraphs/<undertaking>/WORK_GRAPH.md`. Return its
path for continuation and commit it in the undertaking's PR sequence early
enough for handoff. Keep the graph current across sessions and preserve
historical graphs at their existing locations.

Plan substantive implementation and evidence through PRs, each carrying the
documentation, reconciliation and conditional Task Management work its slice
needs. Then plan one final bounded documentation/governance closeout stage:
reconciliation, conditional Task Management, one central loop receipt, terse
MEMORY entries and the final PR. Steps 2–6 supply the mechanics; no formal
reconciliation pass is required
after every node.

## Develop the detail appropriate to the phase

For work toward 60%, develop how the selected Deliverables meet their
requirements and interact: interfaces, states, data, operating sequences,
failure behavior and verification. Read the local ScopeOfWork and fixed
choices before selecting a solution. Identify the exchanged contribution,
supplier, receiver, conditions of use and behavior when the exchange fails.
Place technical details in their maintained artifacts; keep the ScopeOfWork
at the level of obligations, depended-on interfaces and examination.

Use bounded implementation and connected tests when they can resolve a design
question. Definitions, prototypes and observed behavior have different standing.
Revisit source commitments and the project DAG only when findings warrant it,
through the applicable decisions and affected checks. Coordinate coupled work
until its inputs permit independent progress; missing inputs limit the specific
work that needs them. Do not require every SCC to be resolved before useful
work starts or silently delete inconvenient relationships.

The human assesses the 60% position from developed design/interfaces and a
route to completion for which further structural changes are no longer
anticipated. Closing one undertaking or merging a PR does not pass that gate.
Present the actual result, unresolved matters, reliance limits and proposed
continuation when a phase review is requested. Stage, lifecycle, task completion,
acceptance and release remain separate.

## 2. Advance implementation and evidence

Use Agent 0/1/2 responsibilities to maintain alignment, manage connected work and
execute bounded contributions. Supply each executor with the intended output,
accepted basis, needed inputs, write boundary, examination and return path.
Record actual delegation and supplied context; a prepared brief is not proof
of execution. Type 2 does not delegate. Managers integrate their children's returns and
advance independent ready work. Size concurrency to actual review and integration
capacity, with one owner for shared writes.

Implement, verify, validate where applicable, review, repair and integrate via
PRs under the graph and project requirements. Each PR carries the document,
reconciliation and governance consequences needed for that slice, including a
qualified Task Management transfer when needed under Step 4. Exercise meaningful connected behavior and
record the actual candidate and evidence. Prepare consequential decisions for
the human while unaffected work proceeds. Keep required production work in the
graph until its conditions are satisfied; an intermediate merge does not finish
the undertaking.

## 3. Perform the bounded documentation and governance closeout

After integrating the intended implementation and evidence work—normally the
penultimate merge—perform one planned documentation/governance closeout stage.
Use `chirality-root:bundled:workflow:bounded-reconciliation` for bounded
per-deliverable comparisons as needed within that stage. The closeout precedes
the final PR. Compare the delivered result and evidence with the actual
Scope of Work, dependency and governance records; apply warranted edits and
accepted decisions. Preserve future requirements and owning authority for scope,
lifecycle, protected criteria and issued baselines.

This closeout is bounded to the undertaking. A supported no-change result is
sufficient. If it finds missing required implementation or evidence, return that
work to the graph and repair it before completing closeout. Recheck affected
comparisons after a change; do not declare required work complete through a
report or transfer.

## 4. Route exceptional concerns

For a substantive PR or the final closeout, first resolve a concern through
authorized graph work,
a warranted document amendment, or the owning decision/scope-change route.
Work already allocated to an identified successor stays there. Ordinary future
requirements remain in their governing scope.

Only a material, evidenced concern without a current or identified successor
home qualifies for bounded Task Management intake. Give it to WORKING_ITEMS
selecting `chirality-root:bundled:workflow:task-management`, with the source,
significance, missing home and proposed treatment. Perform that workflow's
federation preflight; no general harvest is required. Promotion, disposition
and external assignment remain actual human acts. Retain the outcome or pending
intake in Task Management and link it from the originating PR/graph node and
final closeout as applicable. Routing does not
satisfy an unmet requirement or permit graph completion that depends on it.

## 5. Write the central receipt and affected MEMORY entries

`loop/LOOP_RECEIPTS.md` is a reset compatibility pointer, not a receipt chain
or recovery cursor. The selected work graph carries ongoing execution.

Near final PR preparation, write one receipt for the undertaking at
`execution/_Coordination/AgentRuns/<RunID>/RECEIPT.md`, using the graph's stable
run identity. It is a concise, derivative account of what landed, affected
deliverables, actual PRs, checks and evidence, decisions or Task Management
transfers, and material limits. Use its result/checks/limits account for the
final PR description, adjusting links for the PR surface. Keep detailed logs at
their sources and link the graph; the receipt is neither a second execution
graph, a future-work list nor decision authority. A graph node or Task
Management invocation does not create another loop receipt.

For development undertakings using this loop, add a terse entry to each
affected deliverable's `MEMORY.md` (create it only when first needed): run/date,
what this run did there, and a link to the central receipt. Add the relevant PR,
decision, scope-change or transfer pointer when useful. MEMORY is a local run
index, not a decision record or future assignment. Preserve existing history.
This prospective development practice does not retroactively add MEMORY work
to the completed setup undertaking, which excluded it.
Include the receipt and MEMORY changes in the final PR; use a stable run/branch
link until its PR URL exists, then bind that URL before final checks. Do not
claim a pending merge as complete. Root SPEC §9.8 still governs required
multi-agent execution provenance.

## 6. Complete the graph and merge the final PR

Complete the graph's promised work, bounded closeout, central receipt and
memory entries, and prepare the final PR with the integrated result and
evidence. Review and required checks must cover the actual final candidate;
resolve blocking findings and
obtain the decisions reserved to the human. Record readiness for final merge and
the PR URL in the candidate graph. Verify the actual merged state afterward
through Git or the PR service; do not assert a future merge SHA in the candidate or require a later completion-record commit.

The loop ends when the completed work graph's final PR merges under standing
Git authority. A review hold, unfinished required node or unmerged final PR
means it remains open. On interruption, retain the candidate, open checks,
active operations and next safe action in the graph. Final integration does not
itself issue a deliverable, accept a product or authorize release.
