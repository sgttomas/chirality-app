# Dependency closure — APP_V4_SCA003 (2026-10-03 19:36 MDT)

**Run status: COMPLETE. Subject: FAIL on the six known SCCs (unchanged), as for every earlier closure of this project.** 41 registers, 929 rows, 212 arcs. Coverage passes. Against the accepted DAG-003 the analyzer reports `DEPARTURE`: 10 arcs added, 0 removed, 11 deliverables `DAG pending`.

- **Run and node:** `APP-V4-SCA003-20261002`, node D1 (Type 2 TASK). Registered analyzer `tools/coordination/analyze_dep_closure.py` (sha256 `2b8de3cb…a9adc`), with the project closure arguments and `--prior-summary` set to the SCA-V4-002 closure. Exact command, exit code and output hashes: [Tool_Run.json](Tool_Run.json).
- **Input basis:** commit `75764184b99ab006cd46c1d1c328cf7d5c4d0c8d`, clean tree. Every Dependencies.csv and `_DEPENDENCIES.md` read here is bound by the DAG-004 candidate's `SOURCE_MANIFEST.sha256` (sha256 `03aa668b…a8ef`), so this snapshot is comparable with the candidate (graph-version rules, "Accounting and fidelity").
- **Placement:** in the run folder, because the D1 brief allows writes only under `DAG_PREP/`. Its contract home is `_Evaluation/DepClosure/`. Copying it there and moving that folder's `_LATEST.md` is left to an authorized node. This snapshot is an observation, not an accepted graph.

## Results

| Check | Result | Against SCA-V4-002 closure (`CLOSURE_APP_V4_SCA002_2026-09-29_2056`) |
|---|---|---|
| Schema | 41/41 valid; 0 misplaced fields; 0 ID normalizations | unchanged |
| Rows | 929 total; 929/929 with evidence populated | +103 |
| Graph | 41 nodes, 212 arcs | +10 arcs |
| Orphans, isolated, declared-only, declared disagreements, outside scope | 0 each | unchanged |
| SCCs | 6: sizes 2, 13, 2, 3, 2, 2 | `scc_summary.csv` byte-identical |
| Bidirectional pairs | 27 | +3: DEL-01-04/DEL-02-03, DEL-02-01/DEL-04-03, DEL-02-02/DEL-04-03 |
| Hubs (degree ≥ 20) | DEL-04-03 29, DEL-02-03 25, DEL-02-01 21, DEL-04-01 20 | was 27, 23, 20, 20 |
| `dag_currency` | WARNING: `DEPARTURE` against DAG-003 | was PASS against DAG-003 at its acceptance |
| `circular_dependencies` | BLOCKER (the six SCCs) | unchanged |

**SCCs, matched to their cases by member set** (no case opens, closes or changes membership):

| SCC | Members | Case |
|---|---|---|
| SCC-001 | DEL-01-01, DEL-01-05 | SCC-CASE-001 |
| SCC-002 | DEL-01-04, 02-01, 02-02, 02-03, 02-04, 03-01, 03-02, 03-03, 04-02, 04-03, 05-01, 05-02, 09-09 | SCC-CASE-002 (CASE-004 history) |
| SCC-003 | DEL-01-06, DEL-09-01 | SCC-CASE-003 |
| SCC-004 | DEL-07-01, 07-02, 08-01 | SCC-CASE-005 |
| SCC-005 | DEL-10-02, DEL-10-04 | SCC-CASE-006 |
| SCC-006 | DEL-11-01, DEL-11-03 | SCC-CASE-007 |

**Arcs added** (`Evidence/dag_pending.csv`; consumer → supplier): DEL-01-04 → DEL-01-03, → DEL-01-05, → DEL-02-03, → DEL-02-04, → DEL-04-02; DEL-02-02 → DEL-01-02; DEL-02-03 → DEL-01-02; DEL-03-03 → DEL-01-02; DEL-04-03 → DEL-02-01; DEL-04-03 → DEL-02-02. These are exactly the 10 arcs of `AMENDMENT_PACKET/ARC_EFFECT.md` §1.1, and the same result as node DX's recomputation (`DX/DX_SCC-CHECK.md`).

The coverage defects the method separates from topology findings: none.
