# Accepted DAG-002 handoff

For `construct-local-work-graph` and every other consumer of the App v4 project graph. The owner's decision, its provenance and the reliance boundary are in [ACCEPTANCE_RECORD.md](ACCEPTANCE_RECORD.md).

## Identity and pointer

| Item | Value |
|---|---|
| Accepted version | `_DAG/DAG-002/`, accepted 2026-09-29 (DECISION-10), covering project-dag checkpoints 1 and 2 |
| Pointer | `_DAG/_LATEST.md`, in SPEC §11.2 form: `Latest: DAG-002` |
| Supersedes | DAG-001, kept unchanged as history in `_DAG/DAG-001/` |
| Basis | commit `b585e5ebead38f8ece442c80cd3bec5be8363cf3`; [SOURCE_MANIFEST.sha256](SOURCE_MANIFEST.sha256) (130 entries) |
| Inventory | GROUP3-20260928T001055Z `canonical/Deliverables.csv`, through `_Decomposition/checkpoint_snapshots/_LATEST_ACCEPTED.md`. 41 nodes, no exemptions |
| Integrity | [MANIFEST.sha256](MANIFEST.sha256); check it from this folder |
| Case home | `_DAG/cases/` |

## Objective, semantics, direction and completeness

- **Objective:** production-order and route-selection relationships within the App v4 project. It is not a cross-project graph and not a schedule.
- **Edge semantics:** the consumer requires the supplier's stated contribution, at the stated maturity or condition, before the stated part of its own work. An edge does not mean whole-deliverable completion.
- **Direction:** consumer → supplier. `UPSTREAM` rows read From → Target and `DOWNSTREAM` rows read Target → From.
- **Completeness:** `FULL` for the selected semantics, under `FULL_GRAPH` tracking, with the unresolved-input and candidate qualifications carried from DAG-001.
- **Layers:** 124 admitted arcs ([DependencyEdges.csv](DependencyEdges.csv)); 74 held, non-gating candidate arcs in six SCCs ([CandidateEdges.csv](CandidateEdges.csv)); 264 exclusions ([ExcludedRows.csv](ExcludedRows.csv)).

## Reading rule

1. **Blockers.** Dependency blockers come only from the admitted edges of the accepted, current version.
2. **Contributions and satisfaction.** Required contributions and their satisfaction are read from the live local `Dependencies.csv` and `_DEPENDENCIES.md`. That includes rows this version lists as `MIRROR` or `SAME_ARC`, and the non-topological inputs. The graph promotes no `SatisfactionStatus` or `RequiredMaturity`. `INITIALIZED` means only that a contract is defined.
3. **Candidate edges** are held and non-gating. They drive no blocker queue, wave, schedule, dispatch readiness or readiness claim, and holding one makes no work ready.
4. **`DAG pending`.** A deliverable the latest currency audit lists as `DAG pending` gets no ready or blocked verdict from dependencies until the owner decides its departure. Report the departure and the decision awaited instead.
5. **Scope of an edge.** A missing input constrains the stated part of the work that needs it, not the whole deliverable and not every member of an SCC.

## The 15 released deliverables

The acceptance of DAG-002 decided the departures that made these `DAG pending` under DAG-001 (`CURRENCY_APP_V4_BASISALIGN_2026-09-29_0856`). They are released, and read their blockers from DAG-002:

DEL-01-01, DEL-02-01, DEL-02-02, DEL-02-03, DEL-03-01, DEL-03-02, DEL-03-03, DEL-03-04, DEL-04-01, DEL-04-02, DEL-04-03, DEL-05-01, DEL-05-02, DEL-09-06 and DEL-09-09.

**DEL-01-04 was never pending.** X-1 is in no register (see the open matters).

## DEL-01-01 as a new supplier (C2-3)

DEL-01-01 (Stock Codex hosting and supplier contract) is now an admitted supplier to six deliverables:

| Arc | Consumer → supplier | Representative row |
|---|---|---|
| N-16 | DEL-02-01 → DEL-01-01 | DEP-02-01-025 |
| N-23 | DEL-02-03 → DEL-01-01 | DEP-02-03-023 |
| N-B4 | DEL-03-03 → DEL-01-01 | DEP-03-03-013 |
| N-B9 | DEL-03-04 → DEL-01-01 | DEP-03-04-021 |
| N-15 | DEL-04-03 → DEL-01-01 | DEP-04-03-027 |
| N-C5 | DEL-09-06 → DEL-01-01 | DEP-09-06-032 |

- **What waits.** The stated part of each consumer waits for DEL-01-01's hosting-boundary contribution at the maturity its row states. Whether that contribution is satisfied is read from the live registers, not from the graph.
- **DEL-01-01's own cycle is unchanged.** It stays in SCC-001 with DEL-01-05 (SCC-CASE-001), and that SCC's two held arcs are unchanged.
- **Guard.** Because six deliverables now consume DEL-01-01, a reverse row in which DEL-01-01 consumes one of them would merge SCCs. ARC_ANALYSIS §4.2 tested three such citations, K-3, K-4 and K-5, and each merges SCC-001, SCC-002 and SCC-003 into 19 members. None is in any register. If one appears, it is an SCC-forming departure.

## Standing note: the DEL-09-06 reverse-arc guard (C2-4)

DEL-09-06 is now an admitted consumer of eight deliverables: DEL-01-01, DEL-02-01, DEL-02-02, DEL-03-01, DEL-03-02, DEL-03-03, DEL-04-01 and DEL-04-02 (N-C5, N-19, N-C1, N-C2, N-C3, N-C4, N-28, N-08).

**DEL-09-06 stays outside SCC-002 only while no reverse arc exists.** Across both layers of DAG-002:

- it reaches 20 deliverables: DEL-01-01…01-06, DEL-02-01…02-04, DEL-03-01…03-03, DEL-04-01…04-03, DEL-05-01, DEL-05-02, DEL-09-01 and DEL-09-09;
- it is consumed only by DEL-03-04 (N-B10) and DEL-09-07 (DEP-09-07-011).

A new ACTIVE row forms a cycle if it:

- makes any of those 20 deliverables consume DEL-09-06, or consume a deliverable that consumes it; or
- makes DEL-09-06 consume DEL-03-04, DEL-09-07, or anything that consumes them.

Such a row is an **SCC-forming departure**. It must be decided by the owner and routed to `scc-resolution-case`, not absorbed into the graph.

These reverse citations were tested in ARC_ANALYSIS §4.1–4.2 and are in no register today (V12 §2):

| Label | Row it would take | Effect |
|---|---|---|
| E-1 | DEL-09-09 → DEL-09-06 | SCC-002 grows to 14 |
| K-11 | DEL-03-03 → DEL-09-06 | SCC-002 grows to 14 |
| E-5 | DEL-09-06 → DEL-03-04 | New SCC {03-04, 09-06} |
| K-7 | DEL-09-06 → DEL-09-07 | New SCC {09-06, 09-07} |

`GRAPH_BASIS.md` also lists K-6 (DEL-09-06 → DEL-09-09). It was tested to form no SCC, but it would still be an added-arc departure.

## Candidate edges held, and the work lacking their inputs

All 74 held arcs are `SCC_UNRESOLVED` and cite their case. No case opened or closed with DAG-002. Details are in `GRAPH_BASIS.md` §Candidate layer and each case datasheet.

| SCC | Case | Members | Held arcs | Work lacking input |
|---|---|---:|---:|---|
| SCC-001 | SCC-CASE-001 | 2 | 2 | DEL-01-01 ↔ DEL-01-05. The work that needs the selected pin/protocol and the embedding contribution |
| SCC-002 | SCC-CASE-002 (CASE-004 as history) | 13 | 62 (40 in DAG-001, plus the 22 new held arcs) | Definition proceeds on provisional versions. Each dependent part that needs a named contribution waits for it at its stated maturity. For example, DEL-04-02's display of network-destination grants waits for DEL-05-01 (R8-A), and DEL-04-03's R15 events wait for DEL-05-01 (R8-B). See the datasheet section "Successor observation, 2026-09-29" |
| SCC-003 | SCC-CASE-003 | 2 | 2 | Unchanged from DAG-001 |
| SCC-004 | SCC-CASE-005 | 3 | 4 | Unchanged from DAG-001 |
| SCC-005 | SCC-CASE-006 | 2 | 2 | Unchanged from DAG-001 |
| SCC-006 | SCC-CASE-007 | 2 | 2 | Unchanged from DAG-001 |

SCC-002's 13 members are DEL-01-04, DEL-02-01, DEL-02-02, DEL-02-03, DEL-02-04, DEL-03-01, DEL-03-02, DEL-03-03, DEL-04-02, DEL-04-03, DEL-05-01, DEL-05-02 and DEL-09-09.

## Exclusions still relevant to readiness

- **NOT_TOPOLOGICAL (208):** 150 EXTERNAL, 26 DOCUMENT, 18 PACKAGE and 14 UNKNOWN rows. They are not graph arcs, but they remain inputs at their own points of need; see [Evidence/NonTopologicalInputs.csv](Evidence/NonTopologicalInputs.csv). Ten EXTERNAL rows are new with DAG-002.
- **MIRROR (54) and SAME_ARC (2):** each names its arc's representative. Each keeps its own obligation, read from the live register; see [Evidence/MirrorAssessment.md](Evidence/MirrorAssessment.md).
- **Two mirror maturity differences:**
  - DEL-03-03 → DEL-04-01: DEP-03-03-008 says TBD and DEP-04-01-023 says INITIALIZED;
  - DEL-09-06 → DEL-04-03: DEP-09-06-015 says TBD and DEP-04-03-031 says INITIALIZED.

  Until the register owners reconcile them, read both rows.

## Advice: renewed examination (C2-7)

These deliverables are **not** `DAG pending`. They consume a deliverable that gained inputs, or lie on a route to one. Re-examine their routes when they next rely on those inputs:

- DEL-09-07 (consumes DEL-09-06);
- DEL-10-03 (consumes DEL-02-01, DEL-02-03, DEL-03-01, DEL-03-02, DEL-04-03, DEL-05-01 and DEL-05-02);
- DEL-09-02 (consumes DEL-02-01, DEL-02-03 and DEL-04-03);
- DEL-01-04, DEL-06-01, DEL-06-02, DEL-09-05 and DEL-09-11 (consume DEL-04-03);
- DEL-02-04 and DEL-08-02 (consume DEL-02-01);
- DEL-08-01 (consumes DEL-05-01);
- DEL-01-02 and DEL-01-03 (on the route to DEL-01-01, which gained six admitted consumers).

**Coordination concentrations.** These are not defects:

- DEL-04-03 has degree 27 across both layers;
- DEL-04-01 has 20 admitted dependents and no suppliers;
- DEL-02-03 also has 20 or more connections.

## Open matters (C2-5), with owners

| Matter | Owner and route |
|---|---|
| **SCA-V4-002 scope (DECISION-10).** The amendment now includes: the DEL-10-03 REQ-005 "local-first" item; "consumes" sentences, where the dependency is real, for N-18 (DEL-02-01 → DEL-03-02), N-21 (DEL-02-03 → DEL-03-02), N-24 (DEL-02-03 → DEL-03-03) and X-1 (DEL-02-03 → DEL-01-04); and the carried text items. The carried items are the DEL-09-07, DEL-01-04 and DEL-02-02 SoW text on OI-001/002/012, the `Open_Issues.csv` OI-001/002 status, the DEL-03-03 CLM-002 tail and the A17b line join | `scope-change` (SCA-V4-002), after SCA-V4-001 closes. It is a new change event. The rows its SoW wording yields are expected to appear in a later currency audit as a small departure, for a later successor. Until then the four arcs are not in the graph and nothing is held on their account |
| **V12 F6 (advice).** N-05 and N-07 rest on the supplier's statement only. The consumer text is an ownership sentence | SCA-V4-002 could also give them consumer-side wording |
| **V12 F1: 34 evidence quotes drop inline-code backticks.** DEL-04-01 has 9 (DEP-04-01-017, -018, -022…-027, -029). DEL-04-02 has 12 (DEP-04-02-011, -012, -015…-023, -025). DEL-04-03 has 13 (DEP-04-03-019, -021…-032). No arc, count or verdict is affected | The three register owners, through `dependency-extract`: re-quote exactly at the next UPDATE (for example with SCA-V4-002), or have the owner record the relaxed convention |
| **Coverage_Telemetry.json is stale** (DECISION-8: STALE_REBUILD_REQUIRED). The SCA-V4-001 closure verdict stays OPEN_PENDING_DERIVATIVE_CLOSURE for that derivative only | Decomposition owner, by a later bounded brief |
| The two mirror maturity differences listed under exclusions | Both register owners, through `dependency-extract` |
| The RS §10 DEL-03-02 cell and the ADAPTER header wording behind N-12/N-B8. Both arcs are absent by decision (DECISION-6) | DEL-04-03 and DEL-03-03 owners |
| Deferred supplier-side mirror rows (P2 O-3), and the SatisfactionStatus TBD/PENDING convention (P2 O-6) | Register owners |
| **V12 F8.** OI-001/OI-002 constraint rows are retired in DEL-02-03 and DEL-05-02 but amended and kept in DEL-04-01, DEL-04-02, DEL-04-03 and DEL-09-06. This is a consistency point | Register owners |
| **V12 F7.** The as-dispatched DEL-09-06 extraction guard wording is recorded in the DX-3 return and the DEL-09-06 Run Notes, but not in BRIEFS.md. The standing note above now records the guard | Run records; nothing further for the graph |
| Unknowns stay `TBD` in the registers: RequiredMaturity on 215 rows and SatisfactionStatus on 302 | Register owners, as work proceeds |

## Currency

**Latest result.** `_Evaluation/DAGCurrency/_LATEST.md` locates the latest currency audit. The follow-up audit after this acceptance is expected to report `CURRENT` with nothing `DAG pending`. The audit of 2026-09-29_0856 is against DAG-001 and is historical.

**Commands.** Run the first from this folder and the second from the execution root, `projects/chirality-app-v4/execution`:

```text
shasum -a 256 -c MANIFEST.sha256
shasum -a 256 -c _DAG/DAG-002/SOURCE_MANIFEST.sha256
```

Then check that `_Decomposition/checkpoint_snapshots/_LATEST_ACCEPTED.md` still names GROUP3-20260928T001055Z. If any source failed, re-apply the accepted selection rules as a scratch assembly and compare the arc sets, the SCCs and the inventory (`workflows/project-dag/resources/currency.md`).

**Cross-check.** The registered closure analyzer, run from the repository root, now reads the §11.2 pointer:

```text
python3 tools/coordination/analyze_dep_closure.py projects/chirality-app-v4/execution --scope ALL --filter-active-only true --normalize-ids true --dependency-class EXECUTION --target-type DELIVERABLE --hub-threshold 20 --max-cycles 200 --include-declared true
```

Its `accepted_dag` section reports the comparison.

**When to audit:**

- before relying on DAG-002 for a route or a blocker verdict when the local files may have changed since its basis or since the latest audit;
- after `dependency-extract` runs on any in-scope deliverable, or after a human changes declarations;
- after an accepted scope change or decomposition revision, **including SCA-V4-002 when it is applied**;
- when a consumer finds the graph and a local file disagree;
- after the owner decides a departure.

A new session is not, by itself, a reason to rebuild.
