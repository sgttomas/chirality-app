# DAG-002 — successor graph candidate

**Standing: an unaccepted candidate, assembled and strictly audited, prepared for owner checkpoint C.** The independent review by a separate TASK instance has not happened yet. Nothing here accepts a graph, moves `_DAG/_LATEST.md`, satisfies a dependency, changes lifecycle or passes a gate.

## Identity

| Field | Value |
|---|---|
| Graph | DAG-002 (next unused number) |
| Trigger | `SUCCESSOR` |
| Predecessor | DAG-001, accepted 2026-09-28 ([ACCEPTANCE_RECORD](../../DAG-001/ACCEPTANCE_RECORD.md)) |
| Change event | The accepted scope change SCA-V4-001 (DECISION-7, DECISION-8), applied by `scope-of-work` REVISE to 16 SoWs, then `dependency-extract` UPDATE of 18 registers (DECISION-9 plan) |
| Currency audit | [`CURRENCY_APP_V4_BASISALIGN_2026-09-29_0856`](../../../_Evaluation/DAGCurrency/CURRENCY_APP_V4_BASISALIGN_2026-09-29_0856/CURRENCY_REPORT.md): `DEPARTURE`, 37 arcs added, 0 removed, SCCs and inventory unchanged, 15 deliverables `DAG pending` |
| Departures this candidate decides | The 37 added arcs, listed in [Evidence/DepartureAccount.csv](Evidence/DepartureAccount.csv) |
| Run | `APP-V4-BASIS-ALIGN-20260928`, node D1 ([ASSEMBLY_RUN.md](ASSEMBLY_RUN.md)) |

## Carried forward from DAG-001 (not re-decided)

These stand from DAG-001 ([GRAPH_BASIS](../../DAG-001/GRAPH_BASIS.md); [BASIS_DECISION](../../DAG-001/BASIS_DECISION.md) DECISION-1; [ACCEPTANCE_RECORD](../../DAG-001/ACCEPTANCE_RECORD.md)). The departure does not touch their rows, arcs or warrants.

- **Objective.** Production-order and route-selection relationships in this App project. Not a cross-project graph and not a schedule.
- **Edge semantics.** The consumer requires the supplier's stated contribution, at the stated maturity or condition, before the stated part of its work. Not whole-deliverable completion.
- **Direction.** Consumer → supplier ("depends on"): UPSTREAM is From → Target, DOWNSTREAM is Target → From. Source `Direction` is preserved.
- **Tracking and completeness.** FULL_GRAPH (`_Coordination/_COORDINATION.md`; all 41 `_DEPENDENCIES.md`). Completeness **FULL for the selected semantics**, with the explicit unresolved-input and candidate qualifications below.
- **Inventory.** GROUP3-20260928T001055Z `canonical/Deliverables.csv`, through `_Decomposition/checkpoint_snapshots/_LATEST_ACCEPTED.md` (both unchanged). 41 nodes in 11 packages, all `PRESENT`, no exemptions. [DeliverableNodes.csv](DeliverableNodes.csv) was re-derived from the register and is byte-equal to DAG-001's.
- **Case home.** `_DAG/cases/`.
- **Selection rules.** SR-1…SR-7 as confirmed: all canonical DependencyTypes admitted (SR-3); no cut or merge ruling (SR-4); no confirmation hold (SR-5); one representative per arc, consumer UPSTREAM first, then DECLARED, then lowest DependencyID (SR-6); every intra-SCC representative held (SR-7).
- **Maturity reading.** `INITIALIZED` is defined-contract maturity only. SatisfactionStatus is never promoted by the graph.
- **Reliance boundary.** Unchanged in kind. Acceptance would satisfy no dependency, advance no lifecycle, lift no hold, pass no gate and release nothing.
- **Tool strictness.** `audit_dag.py --canonical --strict` must exit 0. No strictness exception is taken.

## Reopened decisions (checkpoint 1, limited to these)

The arc set was decided at checkpoint A (OWNER_DECISIONS.md DECISION-6: "Accept the 41; keep X-1 (Recommended)"), with the OWNER_ITEMS records O-27…O-30:

| Decision | Recorded answer | Result in the evidence |
|---|---|---|
| The refreshed 41 arcs as the departure scope (P2 O-1) | Accepted | 37 of the 41 are in the registers; see "Accepted but not produced" |
| X-1 (DEL-02-03 → DEL-01-04) (O-28) | Keep | **Not produced.** The kept clause is a construction statement; DX-2 did not read it as consumption |
| N-12 and N-B8 (O-27; P2 O-4) | Not proposed | Absent from every register |
| N-15 direct (O-29) | Keep | Present, admitted |
| Grounding route for the nine P2 arcs (O-30) | Route (a), SoW sentences | All nine present (N-11, N-17, N-20, N-22, N-27, N-B3, N-B4, R8-A, R8-B) |
| CASE-002 continues, gaining held arcs (P2 O-7) | Recommended "confirm"; carried as case tracking under CP1-20260928 | The closure's SCC-002 has the same 13 members; CASE-002 updated with evidence only |
| E-1…E-5 and K-1…K-12 stay out (P2 O-8) | Recommended "confirm"; guarded in the DX briefs | None present |

### Accepted but not produced (for checkpoint C)

| Arc | Consumer → supplier | Would sit in | Why it is not in the registers |
|---|---|---|---|
| N-18 | DEL-02-01 → DEL-03-02 | SCC-002 (candidate) | DEL-02-01's SoW names DEL-03-02 only as an owner; this register's convention reads ownership lists as non-edges ([DX-2_DEL-02-01](../../../_Coordination/AgentRuns/APP-V4-BASIS-ALIGN-20260928/DX/DX-2_DEL-02-01.md)) |
| N-21 | DEL-02-03 → DEL-03-02 | SCC-002 (candidate) | Ownership sentence only ([DX-2_DEL-02-03](../../../_Coordination/AgentRuns/APP-V4-BASIS-ALIGN-20260928/DX/DX-2_DEL-02-03.md)) |
| N-24 | DEL-02-03 → DEL-03-03 | SCC-002 (candidate) | Ownership sentence only (same return) |
| X-1 | DEL-02-03 → DEL-01-04 | SCC-002 (candidate) | "constructs the App act control" is a construction statement (same return) |

All four would be non-gating candidate arcs inside the unchanged SCC-002. Adding or omitting them changes no SCC, no admitted arc and no readiness verdict. The graph copies rows; it does not create them. Wording or declarations belong to the register and SoW owners, and a later row is a new departure. The owner's options are in `DAG_PREP/CHECKPOINT_C.md`.

## Basis

| Item | Value |
|---|---|
| Source revision | `b585e5ebead38f8ece442c80cd3bec5be8363cf3`, clean tree |
| Manifest | [SOURCE_MANIFEST.sha256](SOURCE_MANIFEST.sha256), SHA-256 `6d1021f1c78fea023c2089aa29a2bc60f5ae498f56068eeddbfa376467793250`, 130 entries: the same paths as DAG-001, of which 52 changed |
| Closure snapshot | [`CLOSURE_APP_V4_BASISALIGN_2026-09-29_0855`](../../../_Evaluation/DepClosure/CLOSURE_APP_V4_BASISALIGN_2026-09-29_0855/Dependency_Closure_Report.md), computed on this manifest (input basis matches; [SOURCE_BASIS.json](SOURCE_BASIS.json)). Coverage PASS; six SCCs; raw acyclic closure BLOCKER, as for DAG-001 |
| Provenance | [SOURCE_BASIS.json](SOURCE_BASIS.json): revision, manifest, closure, cases, tools, decisions and returns, with hashes |

## Result

| Account | DAG-001 | DAG-002 | Change |
|---|---:|---:|---|
| Nodes | 41 | 41 | none |
| ACTIVE EXECUTION rows | 403 | 462 | +63 added, −4 retired (all EXTERNAL) |
| Admitted arcs ([DependencyEdges.csv](DependencyEdges.csv)) | 109 | **124** | +15 |
| Held arcs ([CandidateEdges.csv](CandidateEdges.csv)) | 52 | **74** | +22, all in SCC-002 |
| Excluded rows ([ExcludedRows.csv](ExcludedRows.csv)) | 242 | 264 | NOT_TOPOLOGICAL 208, MIRROR 54, SAME_ARC 2 |
| SCCs | 6 | 6 | identical member sets |
| Arcs removed | — | 0 | — |

The balance is 124 + 74 + 264 = 462, with no row missing or placed twice. All 198 admitted and candidate rows equal their source rows in the 29 core columns, byte for byte, and carry non-blank canonical `Explicitness`, `SatisfactionStatus` and `Confidence`. Per-register balance and closure consistency: [Evidence/Accounting.md](Evidence/Accounting.md).

**Strict audit.** `python3 tools/coordination/audit_dag.py --dag-dir projects/chirality-app-v4/execution/_DAG/_Candidates/DAG-002 --canonical --strict --json-out …/Evidence/dag_audit.json`, run from the repository root: **exit 0**. 124 edges, 41 nodes, 0 canonical findings, 0 endpoint issues, 0 SCCs, 0 duplicates, 0 bidirectional pairs, 0 ragged rows ([Evidence/dag_audit.json](Evidence/dag_audit.json); [Evidence/Tool_Run.json](Evidence/Tool_Run.json)). The admissible set (198 arcs) and the candidate layer (74) were audited without `--strict`: both exit 0 with the expected cyclic subjects and six SCCs.

### Admitted arcs added (15)

| Label | Consumer → supplier | Representative |
|---|---|---|
| N-15 | DEL-04-03 → DEL-01-01 | DEP-04-03-027 |
| N-16 | DEL-02-01 → DEL-01-01 | DEP-02-01-025 |
| N-23 | DEL-02-03 → DEL-01-01 | DEP-02-03-023 |
| N-B4 | DEL-03-03 → DEL-01-01 | DEP-03-03-013 |
| N-B9 | DEL-03-04 → DEL-01-01 | DEP-03-04-021 |
| N-B10 | DEL-03-04 → DEL-09-06 | DEP-03-04-022 |
| N-B11 | DEL-03-04 → DEL-09-09 | DEP-03-04-023 |
| N-C5 | DEL-09-06 → DEL-01-01 | DEP-09-06-032 |
| N-19 | DEL-09-06 → DEL-02-01 | DEP-09-06-025 |
| N-C1 | DEL-09-06 → DEL-02-02 | DEP-09-06-026 |
| N-C2 | DEL-09-06 → DEL-03-01 | DEP-09-06-027 |
| N-C3 | DEL-09-06 → DEL-03-02 | DEP-09-06-028 |
| N-C4 | DEL-09-06 → DEL-03-03 | DEP-09-06-029 |
| N-28 | DEL-09-06 → DEL-04-01 | DEP-09-06-030 |
| N-08 | DEL-09-06 → DEL-04-02 | DEP-09-06-031 |

What changes for sequencing, from acceptance on:

- **DEL-01-01 becomes an admitted supplier** to DEL-02-01, DEL-02-03, DEL-03-03, DEL-03-04, DEL-04-03 and DEL-09-06. Their stated parts wait for DEL-01-01's stated contribution (HOSTING-BOUNDARY) at its stated maturity. DEL-01-01 stays in SCC-001; that SCC's two held arcs are unchanged.
- **DEL-09-06 becomes an admitted consumer** of 8 suppliers. It stays outside SCC-002 **only while** no reverse arc is added (E-1, E-5, K-6, K-7 and K-11 guards; ARC_ANALYSIS §4.1–4.2). A later extraction of any of these is an SCC-forming departure to be decided, not absorbed.
- **DEL-03-04 becomes an admitted consumer** of DEL-01-01, DEL-09-06 and DEL-09-09.
- DEL-04-01 now has 20 admitted dependents and no suppliers; DEL-04-03 has degree 27 across both layers. These are coordination concentrations, not defects.

### Candidate layer

All 74 held arcs are `SCC_UNRESOLVED` and cite their case. They are non-gating: they drive no blocker queue, wave, schedule, dispatch readiness or readiness claim, and holding them does not make the affected work ready.

| SCC | Case | Members | Held arcs (DAG-001) | Source rows | What would resolve it, and the work lacking input |
|---|---|---:|---:|---:|---|
| SCC-001 | [SCC-CASE-001](../../cases/SCC-CASE-001/Case_Datasheet.md) | 2 | 2 (2) | 4 | As DAG-001: the selected pin/protocol and embedding contribution |
| SCC-002 | [SCC-CASE-002](../../cases/SCC-CASE-002/Case_Datasheet.md) (CASE-004 history) | 13 | **62 (40)** | 76 | As DAG-001, plus the 22 new held interfaces (datasheet section "Successor observation, 2026-09-29"). Definition proceeds on provisional versions; each dependent part that needs a named contribution (for example DEL-04-02's display of network-destination grants from DEL-05-01, R8-A, or DEL-04-03's R15 events, R8-B) waits for that contribution at its stated maturity |
| SCC-003 | [SCC-CASE-003](../../cases/SCC-CASE-003/Case_Datasheet.md) | 2 | 2 (2) | 2 | Unchanged |
| SCC-004 | [SCC-CASE-005](../../cases/SCC-CASE-005/Case_Datasheet.md) | 3 | 4 (4) | 8 | Unchanged (DEL-08-01's SoW was revised; its intra-SCC rows were not) |
| SCC-005 | [SCC-CASE-006](../../cases/SCC-CASE-006/Case_Datasheet.md) | 2 | 2 (2) | 3 | Unchanged |
| SCC-006 | [SCC-CASE-007](../../cases/SCC-CASE-007/Case_Datasheet.md) | 2 | 2 (2) | 3 | Unchanged |

Each held row carries DAG-001's `OpenQuestion` text for its case, unchanged. No case opens or closes. All cases stay EVIDENCE_ACCUMULATING with the CP1-20260928 tracking record; only CASE-002 was written (evidence rows, finding F-046, a datasheet section, QA note and run record; validator PASS).

### Exclusions

- **NOT_TOPOLOGICAL (208):** 150 EXTERNAL, 26 DOCUMENT, 18 PACKAGE, 14 UNKNOWN. They remain inputs at their own points of need ([Evidence/NonTopologicalInputs.csv](Evidence/NonTopologicalInputs.csv)). DAG-001's A/B/C account of the 32 PACKAGE/UNKNOWN rows is carried by row identity. 172 rows are unchanged apart from `LastSeen`, 26 carry edited fields (named per row), and 10 are new EXTERNAL rows, left unclassified.
- **MIRROR (54) and SAME_ARC (2):** each names its representative. [Evidence/MirrorAssessment.md](Evidence/MirrorAssessment.md) covers the 16 new comparisons and 4 changed representatives.

## Findings routed to owners (not blocking)

| Finding | Owner route |
|---|---|
| The four accepted arcs not produced (N-18, N-21, N-24, X-1) | Owner at checkpoint C; wording to SCA-V4-002, or declarations by the owner |
| Mirror RequiredMaturity differences: DEL-03-03 → DEL-04-01 (DEP-03-03-008 TBD / DEP-04-01-023 INITIALIZED) and DEL-09-06 → DEL-04-03 (DEP-09-06-015 TBD / DEP-04-03-031 INITIALIZED) | Both register owners, via `dependency-extract` |
| RS §10 DEL-03-02 cell and ADAPTER header wording (behind N-12/N-B8) | DEL-04-03 and DEL-03-03 owners (P2 §3.3) |
| Deferred supplier-side mirror rows (P2 O-3) and the SatisfactionStatus TBD/PENDING convention (P2 O-6) | Register owners |
| `Open_Issues.csv` OI-001/OI-002 still OPEN; SoW text in DEL-09-07 (TBD-002/003), DEL-01-04 and DEL-02-02 still calls OI-001/002/012 open; DEL-03-03 CLM-002 tail; A17b line join | SCA-V4-002 (DX and RV returns) |
| `_DAG/_LATEST.md` has no SPEC §11.2 `Latest:` line, so the registered analyzer reads the accepted DAG as INCOMPLETE | Publication: [PROPOSED_LATEST.md](PROPOSED_LATEST.md) is the §11.2 pointer prepared for DAG-002 |

## Limitations and open questions

- The candidate is not independently reviewed yet. A separate TASK instance must review it before checkpoint C decides it (method Stage 4; SUCCESSOR_PLAN §7).
- The semantic content of each added arc rests on the extraction returns (DX-1/2/3) and P2's analysis. This assembly does not re-certify the SoWs.
- Four arcs that rest only on a supplier-side DOWNSTREAM row (N-05, N-06, N-07, N-20) are valid under SR-6; the review should read their consumer SoWs.
- Candidate arcs are non-gating. An acyclic admitted layer neither resolves the SCCs nor supplies their contributions.
- Unknowns stay `TBD` in the registers: RequiredMaturity TBD on 215 rows, SatisfactionStatus TBD on 302.

## Reproduction

From the repository root:

```text
python3 projects/chirality-app-v4/execution/_DAG/_Candidates/DAG-002/Evidence/assemble_graph.py
```

The script checks the manifest against the working bytes and the frozen commit, re-derives the nodes, applies SR-1…SR-7, runs the three `audit_dag.py` audits, checks accounting and fidelity, and asserts that no protected input (DAG-001, `_DAG/_LATEST.md`, registers, SoWs, `_STATUS.md`, the closure snapshot) changed. Its hash and exact arguments are in [Evidence/Tool_Run.json](Evidence/Tool_Run.json). [Evidence/pointer_form_check.json](Evidence/pointer_form_check.json) records a scratch run of the closure analyzer with a §11.2 pointer: `DEPARTURE` (the same 15) against DAG-001, and `NO_DEPARTURE_FOUND` against this candidate installed as DAG-002. The follow-up currency audit after acceptance is therefore expected to be `CURRENT`.

No `--markdown-out` report is published: its title and front matter are DEV-001-specific, and the JSON `dev001_projection` section is not relied on.
