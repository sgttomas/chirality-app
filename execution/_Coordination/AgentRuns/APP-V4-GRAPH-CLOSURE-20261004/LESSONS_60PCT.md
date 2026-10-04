# Lessons from App v4's passage through the 60% gate

**What this is.** HELP_HUMAN's account, 2026-10-04, of what this run showed
about recognising and passing the 60% gate. It is the source material for
the manual revisions the owner requested: "Can you add to the richness and
accuracy of the Project Management manual and Agent User Manual around this
transitionary phase and how to discern it, what criteria to watch for, and
how to pass through it and handoff to the 90% phase?" Every claim cites the
run's records. Nothing here amends an instruction.

## 1. What the owner said the gate and the DAG are for

These are the owner's words, quoted exactly in `OWNER_DECISIONS.md`:
- "It's a qualitative judgment passing from 60% to 90% where you believe the DAG won't change and all SCCs have been resolved, so that work can proceed enmass in parallel and build things out without many or any conflicting outcomes."
- "the graph will never stop changing in minute details, but that's the job of the work graphs to resolve that level of detail. The DAG is supposed to direct work towards completion. The 60% gate marks an arbitrary point where the LOOP_INIT.md instructions to create a local work graph takes prominence."
- "We're not trying to play games here, we're trying to build software."
- The owner asked HELP_HUMAN to judge the "gestalt", and then accepted:
  "I am accepting the 60% gate cleared."

Read together, these say:
- "The DAG won't change" means it won't change at the level that directs
  work: which deliverables exist, and in what order groups of them can be
  completed.
- "SCCs resolved" means each cycle has a treatment that lets the work
  proceed. That treatment may be grouping the cycle's members into one
  undertaking. It does not mean every cross-reference has been reworded
  away.

## 2. What went wrong first, and the signs that showed it

HELP_HUMAN began graph closure by trying to make the project DAG acyclic at
deliverable level, using the four named moves of
`docs/CYCLE_DRIVEN_RESOLUTION.md`: decompose, invert, merge and cut. Agents
proposed rewordings to invert one dependency at a time. That approach
found more coupling with every pass:
- G1: 83 held rows in six SCCs, with 27 cycle-closing rows at the minimum.
- G2: 30 Design-stated relationships missing from the registers.
- G2b: an abbreviation-aware scan found 10,584 cross-deliverable uses on
  536 pairs. 62 of them were dependencies with no arc.
- Pre-move, the cumulative SCC grew to 16–26 members.

Warning signs that the work was at the wrong level:
- **Each analysis round found more coupling than it removed.** The core
  contracts had been designed together on purpose.
- **Moves left runtime or verification residuals behind.** An invert
  removed the definitional need but not the runtime flow (RVG-C2 B2-M1).
  Every case then needed owner cuts under the broader objectives.
- **Authors narrowed their own designs to close a cycle on paper.**
  RVG2 found this in C7-M2 and C6-M1, and it led to ruling GC-6.
- **Supporting work grew while no usable product advanced.**
  coordinated-knowledge-work §4 warns against exactly this.
- **The case recommendations already gave the work-graph-level answer.**
  "R1: coordinate the contributions under existing owners" was right at
  that level. HELP_HUMAN wrongly dismissed it as no resolution.

## 3. The test that showed the gate was passed

The decisive evidence was a grouping test against the accepted DAG
(DAG-004). It takes minutes to run.
1. **Form working groups from the SCCs.** Put each SCC's members in one
   group, with the deliverables most tightly bound to them. Here that
   gave five groups:
   - A: runtime and contract core, 18 deliverables;
   - B: packaging and qualification;
   - C: connectors and research;
   - D: fleet, journeys and witnesses;
   - E: practice and continuity.
2. **Check that every held (cycle-closing) row is inside one group.**
   Here all 83 were.
3. **Check that between groups the dependencies run one way.** Here they
   gave the order A → {B, C} → D → E. One dependency ran against it
   (09-09 needs 09-01). It formed no cycle at deliverable level, so a work
   graph sequences it.
4. **Check that each residual risk is contained in one group.** Here:
   - SWBPIPE host joins: A and D;
   - placement OI-013/014: A;
   - the policy deliverable's reach into its consumers: A;
   - about 60 design-level dependencies not in the registers: these
     become register updates as each loop touches them.

If all four hold, the DAG directs the remaining work, and finer detail
belongs to the local work graphs. If a held row crosses groups, or groups
depend on each other both ways through a cycle, the structure is not yet
settled at DAG level.

## 4. The other criteria checked

- **Developed design.** Every deliverable has reviewed Design files
  with interfaces. The P60 inventory showed this for all 41.
- **Thin designs.** Each is named with its owner. These are completion
  work within a loop, not structure. Examples: DEL-09-05 covers one VER
  item, and DEL-08-01 §6–§8 are outline.
- **Open matters.** Each is sorted by who closes it: design agents, the
  person, or outside parties. Only the ones that could add or remove a
  deliverable, or reverse an order between groups, bear on the gate.
- **Evidence standing.** This is stated honestly, not inflated: nothing
  is built yet, and all evidence is fixtures and prototypes. That is
  consistent with 60%.

## 5. How the gate was passed

1. HELP_HUMAN prepared a short assessment: the grouping test, the group
   order, the contained residual risks, and what remains as loop-level
   work.
2. The person made the judgment, and HELP_HUMAN recorded their exact words
   with custody. LOOP_INIT reserves the 60% assessment to the person.
   Agent checking does not confer it.

## 6. The handoff to 90%

- **One development loop per group, or per several groups.** Each loop
  builds its local work graph (construct-local-work-graph) from the DAG's
  group order.
- **A walking skeleton through the contract core first.** This is one
  thin path of real code across the co-designed core. It tests the
  frozen contracts against reality before work fans out.
- **Contracts frozen under change control.** An implementation finding
  that a contract is wrong is logged, reviewed and propagated to the
  consumers. It is neither absorbed quietly nor re-litigated.
- **Registers updated as loops touch deliverables.** Design-level
  dependencies found in G2/G2b are carried into ScopeOfWork and register
  rows (GC-5). Each update is reach-checked. The DAG gets a successor
  only on a structural event, under the doctrine's §4 event-driven rule.
- **Effectiveness measured on delivery.** Measure steps running as
  tested code, the time to the first end-to-end path, contract issues
  found, and the share of output that is code against records.

## 7. Rulings from this run worth carrying into guidance

These are in `GC_RULINGS.md`:
- **GC-1 and GC-3:** when a reference is opaque, so that an inversion
  truly removes a dependency.
- **GC-5:** a Design use is a dependency when the consumer needs it to
  define or produce its own part, whether or not a ScopeOfWork states it.
- **GC-6:** never narrow an obligation, input or check to close a cycle.
  That trade belongs to the person.
