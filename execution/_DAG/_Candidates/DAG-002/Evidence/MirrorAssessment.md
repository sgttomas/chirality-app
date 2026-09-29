# Mirror and same-arc assessment — DAG-002

`MirrorComparisons.csv` lists all 56 comparisons: 54 counterpart-register mirrors and 2 same-register rows. The 40 carried from DAG-001 keep DAG-001's assessment (`DAG-001/Evidence/MirrorAssessment.csv`); their rows and fields are unchanged apart from the four representatives that changed (below). The 16 comparisons new since DAG-001 are assessed in `MirrorAssessment.csv`.

## Changed representatives (SR-6, consumer UPSTREAM first)

The new consumer-side rows take over as representative on four existing arcs. This is evidence drift on an arc already in DAG-001, not a departure; no arc changes layer.

| Arc | DAG-001 representative | DAG-002 representative | Layer |
|---|---|---|---|
| DEL-04-02 → DEL-03-02 | DEP-03-02-018 (DOWNSTREAM HANDOVER) | DEP-04-02-015 (UPSTREAM INTERFACE) | candidate |
| DEL-04-03 → DEL-03-02 | DEP-03-02-019 (DOWNSTREAM HANDOVER) | DEP-04-03-024 (UPSTREAM INTERFACE) | candidate |
| DEL-04-03 → DEL-04-01 | DEP-04-01-016 (DOWNSTREAM HANDOVER) | DEP-04-03-021 (UPSTREAM INTERFACE) | admitted |
| DEL-04-03 → DEL-04-02 | DEP-04-02-009 (DOWNSTREAM INTERFACE) | DEP-04-03-022 (UPSTREAM INTERFACE) | candidate |

Each former representative is now a MIRROR. The type differences are the supplier/consumer sides of one transfer, as P2 anticipated (ARC_ANALYSIS §5).

## The 16 new comparisons

- **14 show no material contradiction** in this bounded comparison. They differ in DependencyType (HANDOVER or INTERFACE at the supplier, PREREQUISITE or INTERFACE at the consumer), in Statement, and in 9 cases in SatisfactionStatus (TBD against PENDING, neither asserting fulfilment). Maturity matches.
- **2 differ in RequiredMaturity** and are routed to both owners as non-blocking findings:

| Arc | Representative | Counterpart | Difference |
|---|---|---|---|
| DEL-03-03 → DEL-04-01 (admitted) | DEP-03-03-008, UPSTREAM PREREQUISITE, RequiredMaturity **TBD** | DEP-04-01-023, DOWNSTREAM HANDOVER, **INITIALIZED** | Supplier-side row added by DX-1 states INITIALIZED; consumer row keeps TBD |
| DEL-09-06 → DEL-04-03 (admitted) | DEP-09-06-015, UPSTREAM INTERFACE, **TBD** | DEP-04-03-031, DOWNSTREAM INTERFACE, **INITIALIZED** | Supplier-side row added by DX-1 states INITIALIZED; consumer row keeps TBD |

TBD means the maturity is not yet stated; it does not contradict INITIALIZED. The representative is still chosen by rule, and the arc stays admitted. The owners of DEL-03-03 and DEL-04-01, and of DEL-09-06 and DEL-04-03, may align the values through `dependency-extract`. The owner may also direct at checkpoint C that either arc be held; no warrant for a hold is found here.

## Arcs carried only by a supplier-side row

Four new arcs have no consumer UPSTREAM row, so the supplier's DOWNSTREAM row is the representative: N-05 (DEP-04-02-021), N-06 (DEP-04-02-022), N-07 (DEP-04-02-023) and N-20 (DEP-02-01-027). N-07 is the case the DX-2 return for DEL-02-03 names: DEL-02-03's SoW states no consumption of DEL-04-02, and the arc rests on DEL-04-02's handover statement. This is valid under SR-6 and DAG-001's convention (DAG-001 already admits supplier-side representatives). It is noted for the independent review's semantic check.

This is not a full semantic certification of the source SoWs. A contradiction found by the independent review stays a finding routed to both endpoint owners.
