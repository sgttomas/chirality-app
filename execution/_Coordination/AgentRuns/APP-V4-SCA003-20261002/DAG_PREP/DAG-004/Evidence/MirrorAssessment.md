# Mirror and same-arc assessment — DAG-004

`MirrorComparisons.csv` lists all 147 comparisons: 145 counterpart-register mirrors and 2 same-register rows. **91 are new since DAG-003.** They are the 91 mirror rows SCA-V4-003 added (node DX): 81 mirror-group rows and the 15 Q-17 rows, less the 5 DX did not extract. `MirrorAssessment.csv` gives every comparison a standing. Carried comparisons keep their DAG-001, DAG-002 or DAG-003 assessment where the set of differing fields is unchanged.

## Standings

| Standing | Count | Basis |
|---|---:|---|
| NO_MATERIAL_CONTRADICTION_IDENTIFIED_IN_BOUNDED_COMPARISON | 54 | Carried from DAG-001/002/003; differing-field set unchanged |
| MATURITY_DIFFERENCE_RECONCILED_SINCE_DAG003 | 2 | DAG-003's two routed differences; both rows now INITIALIZED |
| MATURITY_DIFFERENCE_ROUTED_TO_BOTH_OWNERS | 3 | New pairs; see below |
| NEW_MECHANICAL_COMPARISON_ONLY | 88 | New pairs with equal RequiredMaturity; bounded reading below |

### The two DAG-003 differences, now reconciled

| Arc | Rows | Now |
|---|---|---|
| DEL-03-03 → DEL-04-01 (admitted) | DEP-03-03-008 / DEP-04-01-023 | both INITIALIZED (DEP-03-03-008 was TBD) |
| DEL-09-06 → DEL-04-03 (admitted) | DEP-09-06-015 / DEP-04-03-031 | both INITIALIZED (DEP-09-06-015 was TBD) |

DAG-003's open matter "the two mirror maturity differences" can be dropped from the handoff.

### Three new maturity differences, routed to both owners (not blocking)

| Arc (layer) | Representative (consumer) | Counterpart (supplier) | Source of the counterpart |
|---|---|---|---|
| DEL-06-01 → DEL-01-01 (admitted) | DEP-06-01-013 PREREQUISITE, **TBD** | DEP-01-01-030 HANDOVER, **INITIALIZED** | R-11-1 (P1-09) |
| DEL-09-01 → DEL-01-01 (admitted) | DEP-09-01-019 CONSTRAINT, **TBD** | DEP-01-01-031 HANDOVER, **INITIALIZED** | R-11-1 (P1-09) |
| DEL-08-02 → DEL-02-01 (admitted) | DEP-08-02-006 INTERFACE, **TBD** | DEP-02-01-037 HANDOVER, **INITIALIZED** | RP1-MX-0201 (Q-17) |

Each is the same pattern as DAG-003's two: the consumer row leaves the threshold unresolved and the new supplier row states the local contract threshold. The representative is still chosen by rule, and both rows stay live; read both until the owners reconcile them (`dependency-extract`).

## The 88 new pairs with equal maturity

The differing fields are DependencyType and Statement (76, of which 36 also SatisfactionStatus), Statement only (12, 6 also SatisfactionStatus). The type pairs are the expected sides of one handoff: INTERFACE/HANDOVER 58, PREREQUISITE/HANDOVER 17, INTERFACE/INTERFACE 12, PREREQUISITE/INTERFACE 3, CONSTRAINT/HANDOVER 1 (all 91, including the three above).

**Bounded reading (this node).** 15 comparisons were read side by side: the 6 new pairs on new arcs (NR-05, NR-4, NR-04, NR-01, NR-02, R20-10), 6 drawn at random from the other 85 (Python `random.seed(4)`, `random.sample`), and the 3 maturity differences. Each supplier row describes the same contribution the consumer row requires, from the supplier's side. Several state only part of it, for example DEP-01-02-026 against DEP-02-02-020, or DEP-02-02-024 against the fuller list of DEP-04-03-035. **No contradiction was found.** The other 76 are compared mechanically only. This is not a semantic certification of the source SoWs; the independent review should sample further.

## Representatives that moved under SR-6 (7)

Seven existing arcs were carried in DAG-003 by the supplier's DOWNSTREAM row alone. SCA-V4-003 added the consumer's UPSTREAM row on each, and SR-6 selects it. The former representative is now a MIRROR of it:

| Arc (layer) | DAG-003 representative | DAG-004 representative | Ledger |
|---|---|---|---|
| DEL-02-03 → DEL-04-02 (held) | DEP-04-02-023 | DEP-02-03-029 | R2-02-03-a (N-07) |
| DEL-03-02 → DEL-04-02 (held) | DEP-04-02-021 | DEP-03-02-034 | R-02-3 (N-05) |
| DEL-03-03 → DEL-02-01 (held) | DEP-02-01-027 | DEP-03-03-017 | R-03-4 (N-20) |
| DEL-03-03 → DEL-04-02 (held) | DEP-04-02-022 | DEP-03-03-016 | R-03-4 (N-06) |
| DEL-04-03 → DEL-02-04 (held) | DEP-02-04-012 | DEP-04-03-036 | R22-7-reg |
| DEL-05-01 → DEL-01-05 (admitted) | DEP-01-05-014 | DEP-05-01-026 | R-0501-4 (F0 M-5) |
| DEL-09-06 → DEL-09-01 (admitted) | DEP-09-01-024 | DEP-09-06-035 | R-0906-3 |

No arc or layer changes. **This closes DAG-003's "arcs carried only by a supplier-side row" note:** N-05, N-06, N-07 and N-20 each now have a consumer-side row, and so does V12 F6 (consumer wording for N-05 and N-07). DEP-05-01-026's Notes record that its sentence is informational and takes no requirement from DEL-01-05. The row is still an UPSTREAM INTERFACE row, so by rule it is the representative of an admitted arc. Its consumer's verdict depends on DEL-01-05 exactly as under DAG-003, where the arc was already admitted.

## Changed fields on carried comparisons (10)

In 8 of them the differing-field set is unchanged, so the carried assessment stands; the changes are evidence text (`EvidenceQuote` and `SourceRef` on 6 DEL-04-01 rows; `Statement` on DEP-02-02-013/DEP-01-04-010 and three DEL-05-02 rows), The other 2 are the maturity reconciliations above.

## Not extracted (carried obligation)

Five expected mirror rows were not extracted (DX_SCC-CHECK "Not extracted"): DEL-01-01 → DEL-02-04 and → DEL-04-03 (R-11-1), DEL-01-05 → DEL-01-01 (R3-01-05-a), DEL-03-02 → DEL-03-01 (R-02-1) and DEL-03-03 → DEL-02-03 (R-03-1). Each lies on an arc a consumer row already carries, so no arc, layer or representative depends on them. Whether they are added is a register matter for the owner (a receivers sentence in a later revision, or a declared entry in the supplier's `_DEPENDENCIES.md`, OWNER_ITEMS Q-15); the graph is unaffected either way.
