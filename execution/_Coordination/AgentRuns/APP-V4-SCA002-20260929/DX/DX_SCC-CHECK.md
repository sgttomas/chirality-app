# DX return — SCC recomputation after the 11 UPDATE runs

- Node DX (Type 2 TASK). Basis commit 1efd4bcda plus this node's 11 register updates (uncommitted working tree at the time of the check). Scratch script `DX-002/scc.py` (sha256 `330be9415666e0ca32af706af64bd866f38c3ccb4701aaea0b876d3e28c000ea`), same rule as ARC_EFFECT §3 `arcs.py`: every live `Dependencies.csv` (41), ACTIVE EXECUTION rows with a DELIVERABLE target; UPSTREAM gives From → Target, DOWNSTREAM gives Target → From; Tarjan.
- Baseline check: the same script over the HEAD (1efd4bcda) registers gives 198 arcs, reproducing DAG-002 and ARC_EFFECT's "now" column.

| | ARC_EFFECT prediction | Observed after DX |
|---|---:|---:|
| Registers | 41 | 41 |
| ACTIVE EXECUTION rows | — (462 before) | 465 (+4 added, −1 retired) |
| … with a deliverable target | — (254 before) | 258 (+4) |
| Arcs | **202** | **202** |
| Held (inside an SCC) | **78** | **78** |
| Admitted | 124 | 124 |
| SCC-002 internal arcs | **66** | **66** |
| Reciprocal pairs (all / in SCC-002) | **24 / 18** | **24 / 18** |
| SCCs | 6, identical membership | 6, identical membership |

SCC membership (unchanged): SCC-002 = {DEL-01-04, 02-01, 02-02, 02-03, 02-04, 03-01, 03-02, 03-03, 04-02, 04-03, 05-01, 05-02, 09-09}; {07-01, 07-02, 08-01}; {01-01, 01-05}; {01-06, 09-01}; {10-02, 10-04}; {11-01, 11-03}.

The four new arcs are present, one row each: N-18 DEL-02-01 → DEL-03-02 (DEP-02-01-029); N-21 DEL-02-03 → DEL-03-02 (DEP-02-03-025); N-24 DEL-02-03 → DEL-03-03 (DEP-02-03-026); X-1 DEL-02-03 → DEL-01-04 (DEP-02-03-027). All four are held (both ends in SCC-002). No arc was removed; no admitted arc changed.

## Guards (graph-wide, after the run)

- Arcs from an SCC-002 member to DEL-09-06: none. DEL-09-06's own register was not touched; no register gives DEL-09-06 a DOWNSTREAM row to an SCC-002 member.
- N-12 (DEL-03-02 → DEL-04-03): absent. N-B8 (DEL-03-03 → DEL-04-03): absent.
- DEL-04-01 suppliers (arcs DEL-04-01 → x): none. DEL-04-01 keeps 0 suppliers.

## Whole-execution evidence report

`python3 tools/validation/validate_decomposition_registers.py projects/chirality-app-v4/execution --families EVQ,DRB` (report-only): 41 registers, 826 rows, 0 ERROR, 0 WARNING (no EVQ-003, EVQ-004 or DRB-006). A verbatim sweep over all 41 registers: 820 ACTIVE rows quote `ScopeOfWork.md`, 820 are exact substrings of their current SoW (0 not verbatim; the 34 ASC-ISS-008 cells included).
