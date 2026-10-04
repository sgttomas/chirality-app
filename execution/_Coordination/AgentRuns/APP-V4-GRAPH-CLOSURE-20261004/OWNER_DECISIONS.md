# Owner decisions — APP-V4-GRAPH-CLOSURE-20261004

These are the owner's chat messages, transcribed verbatim by HELP_HUMAN from
the HELP_HUMAN session of 2026-10-04 (custody: session transcript). They
record direction only. No owner review of any file is implied.

## The 60% criterion (owner, exact, 2026-10-04)

HELP_HUMAN had reported tranche 2 complete (PR #1081). The position
statement (`APP-V4-DESIGN-PASS-4-20261003/POSITION_60/POSITION_STATEMENT.md`)
answered "not yet" and asked how the SWBPIPE host side should count at 60%.

> It's a qualitative judgment passing from 60% to 90% where you believe the DAG won't change and all SCCs have been resolved, so that work can proceed enmass in parallel and build things out without many or any conflicting outcomes.

HELP_HUMAN replied with a graph-closure continuation. The owner then wrote:

> With this new awareness, scrutinize your proposal for any further changes you want.

HELP_HUMAN revised the proposal against `docs/CYCLE_DRIVEN_RESOLUTION.md` §2.
The revision had six steps:
1. confirm the objective and edge semantics;
2. bring the registers current with the designs;
3. resolve SCCs by named moves, proving the method on CASE-002 first;
4. check each open structural matter for its effect on arcs;
5. confirm interface agreement on admitted edges;
6. the two project-dag checkpoints, with DAG-005's acceptance as the 60%
   judgment.

## Continuation approved (owner, exact, 2026-10-04)

> Good.  And consider the `coordinated-knowledge-work` workflow for additional guidance in your execution and delegation.

## Build-oriented direction (owner, exact, 2026-10-04)

G2b had found 29 more Design-to-Design dependencies, and HELP_HUMAN had said
that pair-by-pair rewording kept finding more coupling. The owner wrote:

> We're not trying to play games here, we're trying to build software.  What approach is productively and effectively moving in that direction?

HELP_HUMAN proposed four steps:
1. stop the rewording chase and keep its findings as records;
2. treat the co-designed contract core as one merged unit under change
   control, so its contracts are frozen and changed only through named,
   reviewed and propagated changes;
3. build a walking skeleton through the core: the App hosting stock Codex,
   a person's decision through the act control, the record written and
   validated, and the decision shown in the view;
4. then fan out along the contract boundaries.

HELP_HUMAN asked for a yes to the merge with change control and to starting
the skeleton. The owner replied:

> Yes you can take this approach and monitor its effectiveness in actually delivering the required content.

## What the DAG and the 60% gate are for (owner, exact, 2026-10-04)

HELP_HUMAN had redirected the work graph toward the walking skeleton, with
a one-page merge member list still pending (B0). The owner wrote:

> the graph will never stop changing in minute details, but that's the job of the work graphs to resolve that level of detail.  The DAG is supposed to direct work towards completion.  The 60% gate marks an arbitrary point where the LOOP_INIT.md instructions to create a local work graph takes prominence.
