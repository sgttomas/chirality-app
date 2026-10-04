# DX return — closure recomputation after the 20 UPDATE runs (SCA-V4-003)

- Node DX (Type 2 TASK). Basis commit 2d5e6845c5 plus this node's 20 register updates (uncommitted working tree at the time of the check).
- Two independent computations:
  1. The registered closure analyzer, from the repository root:
     `python3 tools/coordination/analyze_dep_closure.py projects/chirality-app-v4/execution --scope ALL --filter-active-only true --normalize-ids true --dependency-class EXECUTION --target-type DELIVERABLE --hub-threshold 20 --max-cycles 200 --include-declared true --output-dir $TMPDIR/dx/closure_final`
     (tool sha256 `2b8de3cb…a9adc`; outputs in scratch, not in the repository). The same command over HEAD 2d5e6845c5 before any write (`$TMPDIR/dx/closure_base`) is the baseline.
  2. A scratch script `$TMPDIR/dx/arcs.py` (sha256 prefix `d648739b21f96a4f`), the ARC_EFFECT rule: every live `Dependencies.csv` (41), ACTIVE EXECUTION rows with a DELIVERABLE target; UPSTREAM gives From → Target, DOWNSTREAM gives Target → From; Tarjan. Over HEAD it gives 202 arcs, 124 admitted, 78 held, 24 reciprocal pairs and the six SCCs of DAG-003.

## Result against ARC_EFFECT

| | ARC_EFFECT §2/§4 prediction | Baseline (HEAD) | After DX |
|---|---:|---:|---:|
| Registers | 41 | 41 | 41 |
| Rows (all) | — | 826 | 929 (+103) |
| ACTIVE EXECUTION rows with a deliverable target | — | 258 | 359 (+101) |
| Arcs | **212** | 202 | **212** |
| Admitted | **129** | 124 | **129** |
| Held (inside an SCC) | **83** | 78 | **83** |
| Reciprocal pairs | **27** | 24 | **27** |
| SCCs | 6, identical membership | 6 | 6, identical membership (`scc_summary.csv` byte-identical to the baseline) |
| Admitted layer acyclic | yes | yes | yes |
| DAG pending (analyzer, against DAG-003) | 11 deliverables | 0 | **11**: DEL-01-02, 01-03, 01-04, 01-05, 02-01, 02-02, 02-03, 02-04, 03-03, 04-02, 04-03 |

SCC membership (unchanged): SCC-001 {DEL-01-01, 01-05}; SCC-002 {DEL-01-04, 02-01, 02-02, 02-03, 02-04, 03-01, 03-02, 03-03, 04-02, 04-03, 05-01, 05-02, 09-09}; SCC-003 {01-06, 09-01}; SCC-004 {07-01, 07-02, 08-01}; SCC-005 {10-02, 10-04}; SCC-006 {11-01, 11-03}.

**Arcs added (exactly the 10 of ARC_EFFECT §1.1; none removed):**

| Arc (consumer → supplier) | Ledger | Layer | Consumer row |
|---|---|---|---|
| DEL-01-04 → DEL-01-03 | NR-05 | admitted | DEP-01-04-020 |
| DEL-01-04 → DEL-01-05 | NR-07 | admitted | DEP-01-04-021 |
| DEL-01-04 → DEL-04-02 | NR-08 | held | DEP-01-04-022 |
| DEL-01-04 → DEL-02-03 | NR-09 | held | DEP-01-04-023 |
| DEL-01-04 → DEL-02-04 | NR-4 | held | DEP-01-04-024 |
| DEL-02-03 → DEL-01-02 | NR-01 | admitted | DEP-02-03-028 |
| DEL-03-03 → DEL-01-02 | NR-02 | admitted | DEP-03-03-015 |
| DEL-02-02 → DEL-01-02 | NR-04 | admitted | DEP-02-02-020 |
| DEL-04-03 → DEL-02-01 | R2-04-03-e (K-8) | held | DEP-04-03-034 |
| DEL-04-03 → DEL-02-02 | R20-10 | held | DEP-04-03-035 |

New reciprocal pairs (analyzer `bidirectional_pairs.csv`): DEL-01-04/DEL-02-03, DEL-02-01/DEL-04-03, DEL-02-02/DEL-04-03, as ARC_EFFECT §2 predicts. One row per arc; no arc was split. The supplier-side mirrors of the five admitted arcs (DEL-01-02 ×3, DEL-01-03, and none for NR-07, as proposed) and of NR-4 and R20-10 are present.

**Other analyzer checks:** schema 41/41 valid; orphans 0; isolated 0; declared-only 0; declared disagreements 0; ID normalization 0; `dag_currency` PASS → WARNING (the expected departure); `circular_dependencies` BLOCKER and `subject_status` FAIL are unchanged from the baseline (the six existing SCCs); hubs 4 → 4 (DEL-04-03 27 → 29, DEL-02-03 23 → 25, DEL-02-01 20 → 21, DEL-04-01 20 → 20).

## Rows against the ledger

- New-arc rows: 10 of 10.
- Mirror rows: 91 of the 96 the ledger counts (81 mirror-group rows + the 15 Q-17 RP1-MX rows; R22-7-reg included). All 15 Q-17 rows are present (DEL-02-01 5, DEL-02-03 3, DEL-04-03 5, DEL-04-01 2).
- **Not extracted (5 rows, all mirror-only on arcs that already exist through the consumer's row; no arc effect):**
  - DEL-01-01 → DEL-02-04 and → DEL-04-03 (2 of R-11-1's 10). CLM-005 names both only as owners.
  - DEL-01-05 → DEL-01-01 (R3-01-05-a). DEL-01-01 is named only as owner/supplier, and in AX-004's "joint scope".
  - DEL-03-02 → DEL-03-01 (R-02-1). DEL-03-01 is named only as supplier.
  - DEL-03-03 → DEL-02-03 (one of R-03-1's 4; N-24). DEL-02-03 is named only as supplier or owner.

  In each case the revised ScopeOfWork has no sentence saying the target receives from this deliverable. The ledger's grounding claim was a count of ID mentions ("names 3 of 10", "already named", "names 1 of the 4"). CONSERVATIVE extraction takes no edge from an ownership or exclusion list. Returned to the coordinator. The options are a receivers sentence in a later revision, or a human-declared entry in the supplier's `_DEPENDENCIES.md` Declared Downstream section (the OWNER_ITEMS Q-15 alternative).
- Statement, notes, maturity and label items: all INCLUDE items applied. The items whose content the ScopeOfWork does not restate are R-11-2, R-11-3, R-03-5, R-0501-2, R-0501-3, R-0906-2, R-0909-1, R-0909-2, SC3-02-02-7's "A15" label, SC3-02-04-8's surface names and SC3-02-02-9 on DEP-02-03-010. Each was applied as an owner-accepted annotation and is labelled in the row's Notes with its source. DEFER/DROP items were not applied.
- One retirement: DEP-03-01-022 (R-01-2; PKG-02 package row superseded by deliverable rows; package target, no arc).

## Guards (graph-wide, after the run)

- **R17-10:** DEL-01-02 reaches only DEL-01-01, DEL-01-05 and DEL-04-01. DEL-01-03 reaches those three and DEL-01-02. Neither reaches DEL-01-04, 02-02, 02-03, 04-02, 04-03 or 06-01.
- **DEL-04-01 gains no supplier:** DEL-04-01 has no outgoing arc. Its new rows are DOWNSTREAM rows and one EXTERNAL constraint.
- **DEL-09-06:** no arc runs from an SCC-002 member to DEL-09-06.
- **Absent arcs:** N-12 (DEL-03-02 → DEL-04-03), N-B8 (DEL-03-03 → DEL-04-03), NR-03 (DEL-09-09 → DEL-01-02), NR-06 (DEL-02-04 → DEL-01-03) and NR-10 (DEL-02-04 → DEL-02-02) are all absent.
- **DEL-11-02:** no new row names it. DEL-11-02's own arcs are unchanged.

## Whole-execution evidence report

`python3 tools/validation/validate_decomposition_registers.py projects/chirality-app-v4/execution --families EVQ,DRB` (report-only) found 41 registers and 929 rows: 0 ERROR, 0 WARNING. That means no EVQ-003, EVQ-004 or DRB-006 finding.

## Fence

- **Written:** the 20 registers' `Dependencies.csv` and `_DEPENDENCIES.md`, one new `_run_records/dependency-extract-20261003-sca003.md` per deliverable, and this folder (`DX/`).
- **Not touched:** no ScopeOfWork, `_STATUS.md`, `_DAG`, Design, decomposition or `_ScopeChange` file. Checked with `git status --short`.
