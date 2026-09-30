# Accounting — DAG-003 candidate

Every ACTIVE EXECUTION row of the 41 in-scope registers at the frozen basis (`8cd783d8d`, manifest `d0fc611d…40c5`) appears in exactly one of `DependencyEdges.csv`, `CandidateEdges.csv` or `ExcludedRows.csv`. Keys are `SourceRegister` + `DependencyID` + `SourceRecord`. No row is in two files and none is missing; no register has a duplicate ID. Generated from `RegisterAccounting.csv` and `AssemblyChecks.json`, which `assemble_graph.py` writes and checks.

## Totals

| Account | DAG-001 | DAG-002 | DAG-003 |
|---|---:|---:|---:|
| All register rows | 759 | 822 | 826 |
| ACTIVE ANCHOR (outside the execution graph) | 355 | 355 | 355 |
| RETIRED (outside the execution graph) | 1 | 5 | 6 |
| ACTIVE EXECUTION (denominator) | 403 | 462 | 465 |
| Rows with a Deliverable target | 201 | 254 | 258 |
| Representative arcs | 161 | 198 | 202 |
| Admitted: DependencyEdges.csv | 109 | 124 | 124 |
| Held: CandidateEdges.csv (SCC_UNRESOLVED) | 52 | 74 | 78 |
| Excluded: NOT_TOPOLOGICAL | 202 | 208 | 207 |
| Excluded: MIRROR | 38 | 54 | 54 |
| Excluded: SAME_ARC | 2 | 2 | 2 |

Balance: 124 + 78 + 263 = 465 = ACTIVE EXECUTION 465.

Non-topological targets: EXTERNAL 149 (one fewer than DAG-002: DEP-01-04-014 retired), PACKAGE 18, DOCUMENT 26, UNKNOWN 14. RequiredMaturity: TBD 214, INITIALIZED 251 (INITIALIZED is defined-contract maturity only). SatisfactionStatus: TBD 304, PENDING 161; none SATISFIED, none promoted.

## Byte fidelity

All 202 admitted and candidate rows equal their source record in all 29 core columns, byte for byte. That includes the 15 representatives whose `EvidenceQuote` was re-quoted since DAG-002; the version copies the current bytes. Every excluded row matches its source in the ten identity columns. `all_execution_rows.csv` preserves the 29 core columns of all 465 ACTIVE EXECUTION rows with their layer. `Explicitness`, `SatisfactionStatus` and `Confidence` are non-blank canonical values on every admitted and candidate row (SPEC §5.4).

## Closure consistency

The SCCs computed by `audit_dag.py` on the 202 admissible arcs equal the six member sets in `_Evaluation/DepClosure/CLOSURE_APP_V4_SCA002_2026-09-29_2056/Evidence/scc_summary.csv` exactly, and equal DAG-002's and DAG-001's. The closure ran on the same frozen manifest. No difference needs explaining by SR-3, SR-4, SR-5 or a normalization (none is declared). The admitted arc set is identical to DAG-002's.

| SCC | Case | Members | Source rows (DAG-002) | Held arcs (DAG-002) | Excluded intra-SCC rows |
|---|---|---:|---:|---:|---:|
| SCC-001 | SCC-CASE-001 | 2 | 4 (4) | 2 (2) | 2 |
| SCC-002 | SCC-CASE-002 | 13 | 80 (76) | 66 (62) | 14 |
| SCC-003 | SCC-CASE-003 | 2 | 2 (2) | 2 (2) | 0 |
| SCC-004 | SCC-CASE-005 | 3 | 8 (8) | 4 (4) | 4 |
| SCC-005 | SCC-CASE-006 | 2 | 3 (3) | 2 (2) | 1 |
| SCC-006 | SCC-CASE-007 | 2 | 3 (3) | 2 (2) | 1 |

## Per register

| Deliverable | Rows | ANCHOR | RETIRED | ACTIVE EXECUTION | Admitted | Candidate | Excluded |
|---|---:|---:|---:|---:|---:|---:|---:|
| DEL-01-01 | 24 | 15 | 0 | 9 | 0 | 1 | 8 |
| DEL-01-02 | 21 | 17 | 0 | 4 | 3 | 0 | 1 |
| DEL-01-03 | 18 | 10 | 0 | 8 | 2 | 0 | 6 |
| DEL-01-04 | 19 | 6 | 1 | 12 | 3 | 2 | 7 |
| DEL-01-05 | 16 | 11 | 0 | 5 | 1 | 1 | 3 |
| DEL-01-06 | 12 | 5 | 0 | 7 | 1 | 0 | 6 |
| DEL-02-01 | 29 | 16 | 0 | 13 | 2 | 7 | 4 |
| DEL-02-02 | 19 | 11 | 1 | 7 | 2 | 4 | 1 |
| DEL-02-03 | 27 | 8 | 2 | 17 | 2 | 8 | 7 |
| DEL-02-04 | 16 | 9 | 0 | 7 | 2 | 2 | 3 |
| DEL-03-01 | 31 | 21 | 0 | 10 | 1 | 3 | 6 |
| DEL-03-02 | 27 | 15 | 0 | 12 | 1 | 2 | 9 |
| DEL-03-03 | 14 | 5 | 0 | 9 | 2 | 3 | 4 |
| DEL-03-04 | 23 | 4 | 0 | 19 | 18 | 0 | 1 |
| DEL-04-01 | 29 | 11 | 0 | 18 | 0 | 0 | 18 |
| DEL-04-02 | 25 | 6 | 0 | 19 | 1 | 8 | 10 |
| DEL-04-03 | 33 | 10 | 0 | 23 | 2 | 6 | 15 |
| DEL-05-01 | 25 | 13 | 0 | 12 | 1 | 7 | 4 |
| DEL-05-02 | 20 | 4 | 2 | 14 | 1 | 7 | 6 |
| DEL-06-01 | 13 | 6 | 0 | 7 | 4 | 0 | 3 |
| DEL-06-02 | 16 | 7 | 0 | 9 | 3 | 0 | 6 |
| DEL-07-01 | 15 | 8 | 0 | 7 | 0 | 1 | 6 |
| DEL-07-02 | 15 | 9 | 0 | 6 | 1 | 2 | 3 |
| DEL-08-01 | 16 | 7 | 0 | 9 | 1 | 1 | 7 |
| DEL-08-02 | 12 | 4 | 0 | 8 | 2 | 0 | 6 |
| DEL-09-01 | 30 | 12 | 0 | 18 | 6 | 2 | 10 |
| DEL-09-02 | 31 | 8 | 0 | 23 | 12 | 0 | 11 |
| DEL-09-05 | 13 | 5 | 0 | 8 | 6 | 0 | 2 |
| DEL-09-06 | 34 | 11 | 0 | 23 | 12 | 0 | 11 |
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
| **Total** | 826 | 355 | 6 | 465 | 124 | 78 | 263 |

`ANCHOR` here counts every ANCHOR row; all 355 are ACTIVE. Compared with DAG-002: DEL-02-01 +1 row (candidate), DEL-02-03 +3 rows (candidate), DEL-01-04 −1 ACTIVE EXECUTION row (DEP-01-04-014 retired; its excluded count falls by one); every other register is unchanged in count.
