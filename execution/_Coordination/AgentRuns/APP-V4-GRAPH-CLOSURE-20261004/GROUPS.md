# Development groups accepted at the 60% gate

The owner accepted the 60% gate on 2026-10-04 (OWNER_DECISIONS.md, "The 60%
gate"), and with it HELP_HUMAN's grouping approach: "your intended approach
is a valid decision to start grouping items together and solving them".

These groups are **groupings for development**. They are not a merge ruling
under the cycle-resolution doctrine. Held rows stay `SCC_UNRESOLVED`, the
cases stay open, and each loop's work graph orders the parts of its group.

Basis: DAG-004 (`_DAG/DAG-004/DependencyEdges.csv` and
`CandidateEdges.csv`). Each arc runs consumer → supplier; a DOWNSTREAM row is
reversed.

| Group | Name | Deliverables |
|---|---|---|
| A | Runtime and contract core | DEL-01-01, 01-02, 01-03, 01-04, 01-05, 02-01, 02-02, 02-03, 02-04, 03-01, 03-02, 03-03, 04-01, 04-02, 04-03, 05-01, 05-02, 09-09 |
| B | Packaging and qualification | DEL-01-06, 09-01, 09-02 |
| C | Connectors and research | DEL-07-01, 07-02, 08-01, 08-02 |
| D | Fleet, journeys and witnesses | DEL-03-04, 06-01, 06-02, 09-05, 09-06, 09-07, 09-10, 09-11 |
| E | Practice and continuity | DEL-09-12, 10-01, 10-02, 10-03, 10-04, 11-01, 11-02, 11-03 |

**Group order (suppliers first): A → {B, C} → D → E.** HELP_HUMAN's own
check found that:
- all 83 held rows lie within groups;
- every arc between groups follows this order, except one admitted arc,
  DEL-09-09 → DEL-09-01 (A uses B), which forms no deliverable cycle.

The independent reproduction is in `SURVEY/GROUP_SORT.md`.

**Regrouped 2026-10-04 (owner: "Yes to both moves.").** DEL-09-12 moved from
D to E, and DEL-09-10 moved from C to D, as GROUP_SORT recommended. The
membership above shows the result. With these moves:
- every held row stays within a group;
- every cross-group admitted arc follows the order, except DEP-09-09-012
  (A uses B's examination protocol). That arc is a real need and forms no
  cycle on DAG-004.

There are also three reading choices for the design agents to reword:
- D07: EXEC → CA §8.2, per R10-11;
- D49: XT cites DEL-09-06 OUT-004;
- U08: RS drops the CAF-24 citation.

Two items stay recorded:
- U10, an optional rehearsal running from B to C;
- under objective O-1, the A–B cycle through DEP-09-09-012, which the P16
  cut removes.

**Recording relationships found later.** See GC-7. Within a group, the
group's work graph records them. Across groups, they are recorded in the work graph of each
affected loop (GC-8); no separate list is kept. Bring the human in at
once when something seems to run against the order, forms a cycle across
groups, changes the deliverable set, would make another group's finished
work wrong, or suggests the grouping is wrong. In doubt, ask (GC-7). A
ready or blocked verdict read from the DAG does not cover relationships
recorded only in work graphs.
