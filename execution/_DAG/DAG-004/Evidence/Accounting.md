# Accounting — DAG-004 candidate

Every ACTIVE EXECUTION row of the 41 in-scope registers at the frozen basis (`75764184b9`, manifest `03aa668b…a8ef`) appears in exactly one of `DependencyEdges.csv`, `CandidateEdges.csv` or `ExcludedRows.csv`. Keys are `SourceRegister` + `DependencyID` + `SourceRecord`. No row is in two files and none is missing; no register has a duplicate ID. Generated from `RegisterAccounting.csv` and `AssemblyChecks.json`, which `assemble_graph.py` writes and checks.

## Totals

| Account | DAG-002 | DAG-003 | DAG-004 |
|---|---:|---:|---:|
| All register rows | 822 | 826 | 929 |
| ACTIVE ANCHOR (outside the execution graph) | 355 | 355 | 355 |
| RETIRED (outside the execution graph) | 5 | 6 | 7 |
| ACTIVE EXECUTION (denominator) | 462 | 465 | 567 |
| Rows with a Deliverable target | 254 | 258 | 359 |
| Representative arcs | 198 | 202 | 212 |
| Admitted: DependencyEdges.csv | 124 | 124 | 129 |
| Held: CandidateEdges.csv (SCC_UNRESOLVED) | 74 | 78 | 83 |
| Excluded: NOT_TOPOLOGICAL | 208 | 207 | 208 |
| Excluded: MIRROR | 54 | 54 | 145 |
| Excluded: SAME_ARC | 2 | 2 | 2 |

Balance: 129 + 83 + 355 = 567 = ACTIVE EXECUTION 567.

Non-topological targets: EXTERNAL 151 (+2: DEP-04-01-033, DEP-05-01-027), PACKAGE 17 (−1: DEP-03-01-022 retired), DOCUMENT 26, UNKNOWN 14. RequiredMaturity: TBD 212, INITIALIZED 355 (INITIALIZED is defined-contract maturity only). SatisfactionStatus: TBD 357, PENDING 210; none SATISFIED, none promoted.

## Byte fidelity

All 212 admitted and candidate rows equal their source record in all 29 core columns, byte for byte. Every excluded row matches its source in the ten identity columns. `all_execution_rows.csv` preserves the 29 core columns of all 567 ACTIVE EXECUTION rows with their layer. `Explicitness`, `SatisfactionStatus` and `Confidence` are non-blank canonical values on every admitted and candidate row (SPEC §5.4).

**Copied defect (not repaired here).** Four ACTIVE EXECUTION rows of DEL-01-03 carry an absolute `TargetLocation` under a personal home path: DEP-01-03-011 and DEP-01-03-012 (admitted representatives, as in DAG-002 and DAG-003) and DEP-01-03-013 (excluded as a MIRROR) and DEP-01-03-014 (excluded as NOT_TOPOLOGICAL, PACKAGE target). Ten ANCHOR rows of the same register (DEP-01-03-001…010) carry the same defect but are outside the execution graph. Byte fidelity requires the version to copy the value; the repair belongs to the register owner (`dependency-extract`), after which the basis is re-frozen.

## Closure consistency

The SCCs computed by `audit_dag.py` on the 212 admissible arcs equal the six member sets in `DAG_PREP/CLOSURE_APP_V4_SCA003_2026-10-03_1936/Evidence/scc_summary.csv` exactly, and equal DAG-003's, DAG-002's and DAG-001's. The closure ran on the same frozen manifest. No difference needs explaining by SR-3, SR-4, SR-5 or a normalization (none is declared). The admitted arc set is DAG-003's 124 plus the five expected admitted arcs (NR-01, NR-02, NR-04, NR-05, NR-07).

| SCC | Case | Members | Source rows (DAG-003) | Held arcs (DAG-003) | Excluded intra-SCC rows |
|---|---|---:|---:|---:|---:|
| SCC-001 | SCC-CASE-001 | 2 | 4 (4) | 2 (2) | 2 |
| SCC-002 | SCC-CASE-002 | 13 | 128 (80) | 71 (66) | 57 |
| SCC-003 | SCC-CASE-003 | 2 | 2 (2) | 2 (2) | 0 |
| SCC-004 | SCC-CASE-005 | 3 | 8 (8) | 4 (4) | 4 |
| SCC-005 | SCC-CASE-006 | 2 | 3 (3) | 2 (2) | 1 |
| SCC-006 | SCC-CASE-007 | 2 | 3 (3) | 2 (2) | 1 |

SCC-002 gains 48 internal rows, all new since DAG-003: its held arcs rise by 5 (the five new held arcs) and its excluded intra-SCC rows by 43 (mirror rows, including the five former representatives that SR-6 now places as mirrors of the new consumer-side rows on DEL-02-03 → DEL-04-02, DEL-03-02 → DEL-04-02, DEL-03-03 → DEL-02-01, DEL-03-03 → DEL-04-02 and DEL-04-03 → DEL-02-04). SCC-002 now has 21 internal reciprocal pairs (was 18); the 3 new ones come from NR-09, R2-04-03-e and R20-10.

## Per register

| Deliverable | Rows | ANCHOR | RETIRED | ACTIVE EXECUTION | Admitted | Candidate | Excluded |
|---|---:|---:|---:|---:|---:|---:|---:|
| DEL-01-01 | 32 | 15 | 0 | 17 | 0 | 1 | 16 |
| DEL-01-02 | 26 | 17 | 0 | 9 | 3 | 0 | 6 |
| DEL-01-03 | 22 | 10 | 0 | 12 | 2 | 0 | 10 |
| DEL-01-04 | 26 | 6 | 1 | 19 | 5 | 5 | 9 |
| DEL-01-05 | 17 | 11 | 0 | 6 | 0 | 1 | 5 |
| DEL-01-06 | 12 | 5 | 0 | 7 | 1 | 0 | 6 |
| DEL-02-01 | 40 | 16 | 0 | 24 | 2 | 6 | 16 |
| DEL-02-02 | 24 | 11 | 1 | 12 | 3 | 4 | 5 |
| DEL-02-03 | 40 | 8 | 2 | 30 | 3 | 9 | 18 |
| DEL-02-04 | 19 | 9 | 0 | 10 | 2 | 1 | 7 |
| DEL-03-01 | 42 | 21 | 1 | 20 | 1 | 3 | 16 |
| DEL-03-02 | 34 | 15 | 0 | 19 | 1 | 3 | 15 |
| DEL-03-03 | 20 | 5 | 0 | 15 | 3 | 5 | 7 |
| DEL-03-04 | 23 | 4 | 0 | 19 | 18 | 0 | 1 |
| DEL-04-01 | 33 | 11 | 0 | 22 | 0 | 0 | 22 |
| DEL-04-02 | 28 | 6 | 0 | 22 | 1 | 5 | 16 |
| DEL-04-03 | 45 | 10 | 0 | 35 | 2 | 9 | 24 |
| DEL-05-01 | 27 | 13 | 0 | 14 | 2 | 7 | 5 |
| DEL-05-02 | 20 | 4 | 2 | 14 | 1 | 7 | 6 |
| DEL-06-01 | 13 | 6 | 0 | 7 | 4 | 0 | 3 |
| DEL-06-02 | 16 | 7 | 0 | 9 | 3 | 0 | 6 |
| DEL-07-01 | 15 | 8 | 0 | 7 | 0 | 1 | 6 |
| DEL-07-02 | 15 | 9 | 0 | 6 | 1 | 2 | 3 |
| DEL-08-01 | 16 | 7 | 0 | 9 | 1 | 1 | 7 |
| DEL-08-02 | 12 | 4 | 0 | 8 | 2 | 0 | 6 |
| DEL-09-01 | 30 | 12 | 0 | 18 | 5 | 2 | 11 |
| DEL-09-02 | 31 | 8 | 0 | 23 | 12 | 0 | 11 |
| DEL-09-05 | 13 | 5 | 0 | 8 | 6 | 0 | 2 |
| DEL-09-06 | 35 | 11 | 0 | 24 | 13 | 0 | 11 |
| DEL-09-07 | 25 | 10 | 0 | 15 | 1 | 0 | 14 |
| DEL-09-09 | 24 | 6 | 0 | 18 | 2 | 7 | 9 |
| DEL-09-10 | 11 | 4 | 0 | 7 | 3 | 0 | 4 |
| DEL-09-11 | 10 | 4 | 0 | 6 | 2 | 0 | 4 |
| DEL-09-12 | 14 | 6 | 0 | 8 | 2 | 0 | 6 |
| DEL-10-01 | 22 | 11 | 0 | 11 | 1 | 0 | 10 |
| DEL-10-02 | 13 | 10 | 0 | 3 | 1 | 1 | 1 |
| DEL-10-03 | 20 | 7 | 0 | 13 | 10 | 0 | 3 |
| DEL-10-04 | 14 | 4 | 0 | 10 | 2 | 1 | 7 |
| DEL-11-01 | 12 | 7 | 0 | 5 | 3 | 0 | 2 |
| DEL-11-02 | 22 | 7 | 0 | 15 | 2 | 0 | 13 |
| DEL-11-03 | 16 | 5 | 0 | 11 | 3 | 2 | 6 |
| **Total** | 929 | 355 | 7 | 567 | 129 | 83 | 355 |

`ANCHOR` counts every ANCHOR row; all 355 are ACTIVE. Count changes since DAG-003 (18 registers; DEL-05-02 and DEL-09-09 changed bytes without a count change, and DEL-09-01's counts changed without a byte change): DEL-01-01 (rows +8, ACTIVE EXECUTION +8, excluded +8); DEL-01-02 (rows +5, ACTIVE EXECUTION +5, excluded +5); DEL-01-03 (rows +4, ACTIVE EXECUTION +4, excluded +4); DEL-01-04 (rows +7, ACTIVE EXECUTION +7, admitted +2, candidate +3, excluded +2); DEL-01-05 (rows +1, ACTIVE EXECUTION +1, admitted -1, excluded +2); DEL-02-01 (rows +11, ACTIVE EXECUTION +11, candidate -1, excluded +12); DEL-02-02 (rows +5, ACTIVE EXECUTION +5, admitted +1, excluded +4); DEL-02-03 (rows +13, ACTIVE EXECUTION +13, admitted +1, candidate +1, excluded +11); DEL-02-04 (rows +3, ACTIVE EXECUTION +3, candidate -1, excluded +4); DEL-03-01 (rows +11, RETIRED +1, ACTIVE EXECUTION +10, excluded +10); DEL-03-02 (rows +7, ACTIVE EXECUTION +7, candidate +1, excluded +6); DEL-03-03 (rows +6, ACTIVE EXECUTION +6, admitted +1, candidate +2, excluded +3); DEL-04-01 (rows +4, ACTIVE EXECUTION +4, excluded +4); DEL-04-02 (rows +3, ACTIVE EXECUTION +3, candidate -3, excluded +6); DEL-04-03 (rows +12, ACTIVE EXECUTION +12, candidate +3, excluded +9); DEL-05-01 (rows +2, ACTIVE EXECUTION +2, admitted +1, excluded +1); DEL-09-01 (admitted -1, excluded +1); DEL-09-06 (rows +1, ACTIVE EXECUTION +1, admitted +1). A falling admitted or candidate count in a register (DEL-01-05, DEL-02-01, DEL-02-04, DEL-04-02, DEL-09-01) is a representative moving to the consumer's register under SR-6; no arc is lost. Every other register is unchanged in count.
