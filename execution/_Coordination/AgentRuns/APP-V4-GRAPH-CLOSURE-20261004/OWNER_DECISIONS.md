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

## The 60% gate (owner, exact, 2026-10-04)

The owner asked for HELP_HUMAN's judgment:

> You're in a better place than me to judge the gestalt passing through the 60% gate.  I do suspect we're close to that point but it's impossible for me to verify fully.  I can only ask you about the state of maturity and if there's now a clear path to completion at the DAG level such that we can bring this session to a close and implement the development loops via local work graphs that traverse part of the DAG (or several parts) to bring to the deliverables to completion (which means your intended approach is a valid decision to start grouping items together and solving them rather than trying to define away dependencies).

HELP_HUMAN's assessment, which is recorded in the session transcript:
- all 41 deliverables have reviewed Design files;
- the 83 dependencies that lie inside cycles all fall within five working
  groups, A–E;
- between the groups, dependencies run one way, A → {B, C} → D → E,
  except for one sequencing dependency (09-09 needs 09-01) that does not
  form a cycle.

Residual risks are contained within single groups: the SWBPIPE host
joins, placement OI-013/014, DEL-04-01's reach, and roughly 60
design-level dependencies not yet registered. HELP_HUMAN said that
LOOP_INIT reserves the 60% assessment to the owner, and asked for a yes.

The owner wrote:

> I am accepting the 60% gate cleared.

**Effect.** Under LOOP_INIT the 60% position is passed. DAG-004 directs
the work. Development continues through local work graphs, each taking one
group or several. Completion of individual deliverables, acceptance and
release remain separate.

## Manual revisions and renderer download (owner, exact, 2026-10-04)

> Can you add to the richness and accuracy of the Project Management manual and Agent User Manual around this transitionary phase and how to discern it, what criteria to watch for, and how to pass through it and handoff to the 90% phase?

HELP_HUMAN asked to download the renderer's pinned dependencies,
markdown_it_py-4.2.0 (about 90 KB) and mdurl-0.1.2 (about 10 KB), from
PyPI into a throwaway venv at /tmp/chirality-manual-renderer. The owner
replied:

> download what you need for this.

They were installed into that venv (`pip install -r
docs/alignment-manual/requirements.txt`). `--check` against the committed
v3 HTML confirmed that the renderer reproduces it.

## Close-out and development-loop handoff (owner, exact, 2026-10-04)

> When that work lands and the PR is merged, then proceed with the "Close out this session" steps you outlined earlier.  I will then start the development loops in a new session with the handoff you provide.  Review the init-prompt and LOOP_INIT text before finalizing your handoff.  We should incorporate the `coordinated-knowledge-work` workflow into the LOOP_INIT instructions too.

## Correction to HELP_HUMAN's recorded assessment (2026-10-04)

The "60% gate" entry above summarises HELP_HUMAN's assessment as
"Residual risks are contained within single groups". That overstates it.
The SWBPIPE host joins touch two groups, the core (A) and the fleet group
(D). These are in group order, so the joins do not reverse the order
(LESSONS_60PCT §3; MR-MANUAL ruling 2). Placement OI-013/014 and
DEL-04-01's reach do lie within group A. The owner's quoted words are
unchanged.

## Structure versus detail after 60% (owner, exact, 2026-10-04)

The owner proposed:

> Here's a proposal and you can push back and offer something better: the DAG itself doesn't change, the work graphs just fill in details of interconnecting webs.  If one of the edges in the DAG does change then it's necessary to go through that change process as usual.  Thoughts?

HELP_HUMAN refined it by group. A relationship within a group, or across
groups in the group order, is detail. A relationship that reverses the
order, forms a cross-group cycle or changes the deliverable set goes
through the change process. The owner then asked:

> well this maybe requires some nuance.  Maybe it is the case that new edges are acquired but if we stop to reconstruct the DAG every time that will be too much governance and not enough development.  Is there a way to define this clearly or is there a murky zone that once entered the agents need the human decision for when it's done and the next begins?

HELP_HUMAN proposed three tiers: absorb, batch, and stop and decide, with a
regrouping trigger. The owner asked:

> could this get us into trouble by obscuring something or making declarations that aren't supported so attention is not given to what matters?

HELP_HUMAN named four risks and proposed a narrower form:
1. Absorb only within a group.
2. A shared, live list for every cross-group relationship.
3. Classification by script against the committed group map, sampled by
   a reviewer; any tier 3 reaches the owner.
4. Before the handoff, commit the groups, reproduce the grouping test
   independently, and sort the inventory's 62 dependencies.

The owner replied:

> Then make the necessary revisions to the texts.  It's probably better to leave some things underdefined and seek human judgment in the moment than take your limited experience too far and overconstrain things in the future leading to a problem that builds and isn't recognized.

## Regrouping after the independent check (owner, exact, 2026-10-04)

RVG's SURVEY/GROUP_SORT.md reproduced the grouping test and found two
exceptions. HELP_HUMAN recommended two moves:
- DEL-09-12 to group E, because D57 (09-12 uses 10-02) is a real need
  that runs against the order;
- DEL-09-10 to group D, so that B and C run in parallel (DEP-09-01-027).

The owner replied:

> Yes to both moves.  Record that then let's discuss the LOOP_INIT further.

## How LOOP_INIT steers agents through the guidance (owner, exact, 2026-10-04)

> Consider how the LOOP_INIT points to these instruction documents and propose a more effective way to steer the agent through the information it needs without dumping everything into context at once.  You don't need to make any changes here, I just want to discuss it with you first.

HELP_HUMAN proposed a situation router. The owner replied:

> No routers.  You can't possibly imagine all the scenarios up front and any categorization scheme will be incomplete and probably woefully so.  But each document has a topical structure.  The Table of Contents, two or three layers deep ought to be loaded into context and then the agent decides when to visit it (and here guidance can be given around this level of decision making if done right).

HELP_HUMAN asked two questions: whether the 90% handoff should serve as a
"current phase" card, and whether LOOP_INIT should pin manual editions. The
owner replied:

> I don't want to create a new type of record that needs to be updated to maintain current state.  The handoff is ephemeral.  The present forms of governance presumed sufficient until shown otherwise.  No don't pin to editions. No to both.
