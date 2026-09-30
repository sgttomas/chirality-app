# DAG-003 — successor graph candidate

**Standing: an unaccepted candidate, assembled and strictly audited, prepared for owner checkpoint C.** The independent review by a separate TASK instance has not happened yet. Nothing here accepts a graph, moves `_DAG/_LATEST.md`, satisfies a dependency, changes lifecycle or passes a gate.

## Identity

| Field | Value |
|---|---|
| Graph | DAG-003 (next unused number) |
| Trigger | `SUCCESSOR` |
| Predecessor | DAG-002, accepted 2026-09-29 ([ACCEPTANCE_RECORD](../../DAG-002/ACCEPTANCE_RECORD.md), covering project-dag checkpoints 1 and 2) |
| Change event | The accepted scope change SCA-V4-002 (run `APP-V4-SCA002-20260929`, DECISION-2 and DECISION-3), applied by `scope-of-work` REVISE to 9 SoWs with the B-06a reading-rule note on `_LATEST_ACCEPTED.md`, then `dependency-extract` UPDATE of 11 registers (node DX) |
| Currency audit | [`CURRENCY_APP_V4_SCA002_2026-09-29_2057`](../../../_Evaluation/DAGCurrency/CURRENCY_APP_V4_SCA002_2026-09-29_2057/CURRENCY_REPORT.md): `DEPARTURE`, 4 arcs added, 0 removed, SCCs and inventory unchanged, 5 deliverables `DAG pending` |
| Departures this candidate decides | The 4 added arcs, listed in [Evidence/DepartureAccount.csv](Evidence/DepartureAccount.csv): N-18, N-21, N-24 and X-1 |
| Run | `APP-V4-SCA002-20260929`, node D1 ([ASSEMBLY_RUN.md](ASSEMBLY_RUN.md)) |

## Carried forward from DAG-002 (not re-decided)

These stand from DAG-002 ([GRAPH_BASIS](../../DAG-002/GRAPH_BASIS.md); [ACCEPTANCE_RECORD](../../DAG-002/ACCEPTANCE_RECORD.md), "Qualifications carried from DAG-001") and, through it, from DAG-001 ([BASIS_DECISION](../../_Candidates/DAG-001/BASIS_DECISION.md) DECISION-1). The departure does not touch their rows, arcs or warrants.

- **Objective.** Production-order and route-selection relationships in this App project. Not a cross-project graph and not a schedule.
- **Edge semantics.** The consumer requires the supplier's stated contribution, at the stated maturity or condition, before the stated part of its work. Not whole-deliverable completion.
- **Direction.** Consumer → supplier ("depends on"): UPSTREAM is From → Target, DOWNSTREAM is Target → From. Source `Direction` is preserved.
- **Tracking and completeness.** FULL_GRAPH (`_Coordination/_COORDINATION.md`; all 41 `_DEPENDENCIES.md`). Completeness **FULL for the selected semantics**, with the explicit unresolved-input and candidate qualifications below.
- **Inventory.** GROUP3-20260928T001055Z `canonical/Deliverables.csv`, through `_Decomposition/checkpoint_snapshots/_LATEST_ACCEPTED.md`. The register is unchanged; the pointer file's bytes changed (B-06a reading-rule note, SCA-V4-002 Q-12) but it names the same snapshot. 41 nodes in 11 packages, all `PRESENT`, no exemptions. [DeliverableNodes.csv](DeliverableNodes.csv) was re-derived from the register and is byte-equal to DAG-002's and DAG-001's.
- **Case home.** `_DAG/cases/`.
- **Selection rules.** SR-1…SR-7 as confirmed: all canonical DependencyTypes admitted (SR-3); no cut or merge ruling (SR-4); no confirmation hold (SR-5); one representative per arc, consumer UPSTREAM first, then DECLARED, then lowest DependencyID (SR-6); every intra-SCC representative held (SR-7).
- **Rulings.** None new. CP1-20260928 (case tracking) carries forward; the N-12/N-B8 withholding remains a register-level decision (predecessor DECISION-6), not an SR-4 cut.
- **Maturity reading.** `INITIALIZED` is defined-contract maturity only. SatisfactionStatus is never promoted by the graph.
- **DEL-01-01 as supplier and DEL-09-06 as consumer** (DAG-002 C2-3 and C2-4), with the DEL-09-06 reverse-arc guard as a standing note. Unchanged: the guard held (DX_SCC-CHECK; [Evidence/DepartureAccount.json](Evidence/DepartureAccount.json) `scc002_members_consuming_del_09_06: []`).
- **Reliance boundary.** Unchanged in kind. Acceptance would satisfy no dependency, advance no lifecycle, lift no hold, pass no gate and release nothing.
- **Tool strictness.** `audit_dag.py --canonical --strict` must exit 0. No strictness exception is taken.

## Reopened decisions (checkpoint 1, limited to these)

The arc set was decided at the SCA-V4-002 checkpoint A (OWNER_DECISIONS.md DECISION-2: "accept the remaining items as recommended", with OWNER_ITEMS Q-4 "Keep all four, with the drafted sentences"), following the predecessor's DECISION-10 option A ("add wording in SCA-V4-002"). Group 3 was accepted at checkpoint B (DECISION-3), which authorized the register refresh, the currency audit and this candidate.

| Decision | Recorded answer | Result in the evidence |
|---|---|---|
| The four arcs N-18, N-21, N-24, X-1 as the departure scope (Q-4) | Keep all four | All four present, one consumer-side row each ([Evidence/DepartureAccount.csv](Evidence/DepartureAccount.csv)); none extra, none missing |
| X-1 narrowly (ARC_EFFECT §1 "Keep, narrowly") | Kept, tied to the App-side positive capture fixtures | DEP-02-03-027 quotes the fixture-scoped sentence; its Notes record the narrow scope (DX return) |
| N-12 and N-B8 (predecessor DECISION-6) | Not proposed | Absent from every register |
| E-1…E-5 and K-1…K-12 stay out; DEL-04-01 gains no supplier (the DX guards) | Guarded in the DX briefs | None present; DEL-04-01 has 0 suppliers |
| CASE-002 continues, gaining held arcs | Carried as case tracking under CP1-20260928 | The closure's SCC-002 has the same 13 members; CASE-002 updated with evidence only (section "Successor observation, 2026-09-29 (DAG-003 candidate; evidence update only)") |
| B-06a reading-rule note on `_LATEST_ACCEPTED.md` (Q-12 option a) | Add the note | Applied; bound in this manifest so that it falls inside this one departure (BASIS_AMENDMENT "Timing of B-06a"). Evidence drift, not an inventory or arc change |
| Re-quoting of 34 evidence cells (ASC-ISS-008; V12 F1) | Included in the DX UPDATE | 34 cells now exact; 15 of them on representatives, copied byte for byte here. No arc effect |

No cut, merge, confirmation hold or type exclusion is proposed. No SCC needs a ruling. Checkpoints 1 and 2 may therefore be decided together (method: "a small undertaking with no SCC needing a ruling"); the acceptance record must state that it covers both.

## Basis

| Item | Value |
|---|---|
| Source revision | `8cd783d8d7493fbfe663fb108449e4ceda04a00b`, clean tree |
| Manifest | [SOURCE_MANIFEST.sha256](SOURCE_MANIFEST.sha256), SHA-256 `d0fc611d95ee80ba64b86ea5b0eaa1a1ba90e85e461fb18459dd8162df6a40c5`, 130 entries: the same paths as DAG-001 and DAG-002, of which 32 changed since DAG-002 (9 `ScopeOfWork.md`, 11 `Dependencies.csv`, 11 `_DEPENDENCIES.md`, `_LATEST_ACCEPTED.md`) |
| Closure snapshot | [`CLOSURE_APP_V4_SCA002_2026-09-29_2056`](../../../_Evaluation/DepClosure/CLOSURE_APP_V4_SCA002_2026-09-29_2056/Dependency_Closure_Report.md), computed on this manifest (input basis matches; [SOURCE_BASIS.json](SOURCE_BASIS.json)). Coverage PASS; six SCCs; raw acyclic closure BLOCKER, as for DAG-001 and DAG-002 |
| Provenance | [SOURCE_BASIS.json](SOURCE_BASIS.json): revision, manifest, closure, currency, cases, tools, decisions and returns, with hashes |

## Result

| Account | DAG-002 | DAG-003 | Change |
|---|---:|---:|---|
| Nodes | 41 | 41 | none (byte-equal) |
| ACTIVE EXECUTION rows | 462 | 465 | +4 added, −1 retired (EXTERNAL) |
| Admitted arcs ([DependencyEdges.csv](DependencyEdges.csv)) | 124 | **124** | **same arc set and same 124 representative rows**; 7 rows carry re-quoted or re-referenced bytes (2 EvidenceQuote, 3 SourceRef, 2 Notes) and 18 a `LastSeen` refresh |
| Held arcs ([CandidateEdges.csv](CandidateEdges.csv)) | 74 | **78** | +4, all in SCC-002 |
| Excluded rows ([ExcludedRows.csv](ExcludedRows.csv)) | 264 | 263 | NOT_TOPOLOGICAL 207, MIRROR 54, SAME_ARC 2 |
| SCCs | 6 | 6 | identical member sets |
| Arcs removed | — | 0 | — |
| Representative or layer changes on existing arcs | — | 0 | — |

The balance is 124 + 78 + 263 = 465, with no row missing or placed twice. All 202 admitted and candidate rows equal their source rows in the 29 core columns, byte for byte, and carry non-blank canonical `Explicitness`, `SatisfactionStatus` and `Confidence`. Per-register balance and closure consistency: [Evidence/Accounting.md](Evidence/Accounting.md).

**Strict audit.** `python3 tools/coordination/audit_dag.py --dag-dir projects/chirality-app-v4/execution/_DAG/_Candidates/DAG-003 --canonical --strict --json-out …/Evidence/dag_audit.json`, run from the repository root: **exit 0**. 124 edges, 41 nodes, 0 canonical findings, 0 endpoint issues, 0 SCCs, 0 duplicates, 0 bidirectional pairs, 0 ragged rows ([Evidence/dag_audit.json](Evidence/dag_audit.json); [Evidence/Tool_Run.json](Evidence/Tool_Run.json)). The admissible set (202 arcs) and the candidate layer (78) were audited without `--strict`: both exit 0 with the expected cyclic subjects and six SCCs.

### Admitted arcs added (0)

None. The departure touches the held layer only. From acceptance on, no blocker verdict changes for any deliverable.

### Held arcs added (4)

All four are `SCC_UNRESOLVED` inside the unchanged SCC-002, citing [SCC-CASE-002](../../cases/SCC-CASE-002/Case_Datasheet.md). They are the arcs DAG-002 recorded as "accepted but not produced"; SCA-V4-002 supplied the consuming sentences and the DX run extracted them.

| Label | Consumer → supplier | Representative | What it carries (ARC_EFFECT §1) |
|---|---|---|---|
| N-18 | DEL-02-01 → DEL-03-02 | DEP-02-01-029 (INITIALIZED / PENDING) | DEL-03-02's change-item content identities, per-item dispositions, all-items-decided indication, item-left events and applied-outcome object identities, for checkpoint subject binding and item-level decisions. Reciprocal with N-B3 |
| N-21 | DEL-02-03 → DEL-03-02 | DEP-02-03-025 (INITIALIZED / TBD) | The same DEL-03-02 outputs plus applied outcomes with resulting objects, for checkpoint recording and interrupted or replayed history (REQ-002, REQ-003) |
| N-24 | DEL-02-03 → DEL-03-03 | DEP-02-03-026 (INITIALIZED / TBD) | DEL-03-03's observations of checkpoint arrivals and act records on the external channel, which DEL-02-03 records. Reciprocal with N-27 |
| X-1 | DEL-02-03 → DEL-01-04 | DEP-02-03-027 (INITIALIZED / TBD) | DEL-01-04's App act control and person identity, narrowly for the App-side positive capture fixtures (OUT-003, VER-003), which await that later undertaking |

Holding them changes no verdict: held arcs drive no blocker queue, wave, schedule, dispatch readiness or readiness claim, and holding one makes no work ready. Their contributions remain live obligations read from the registers.

### Candidate layer

All 78 held arcs are `SCC_UNRESOLVED` and cite their case. Each held row carries DAG-002's `OpenQuestion` text for its case, unchanged. No case opens or closes. All cases stay EVIDENCE_ACCUMULATING with the CP1-20260928 tracking record; only CASE-002 was written (evidence rows E4-*, finding F-047, a datasheet section, QA note and run record; validator PASS, exit 0).

| SCC | Case | Members | Held arcs (DAG-002) | Source rows | What would resolve it, and the work lacking input |
|---|---|---:|---:|---:|---|
| SCC-001 | [SCC-CASE-001](../../cases/SCC-CASE-001/Case_Datasheet.md) | 2 | 2 (2) | 4 | As DAG-001: the selected pin/protocol and embedding contribution |
| SCC-002 | [SCC-CASE-002](../../cases/SCC-CASE-002/Case_Datasheet.md) (CASE-004 history) | 13 | **66 (62)** | 80 | As DAG-002, plus the 4 new held interfaces. Definition proceeds on provisional versions; DEL-02-01's subject binding and DEL-02-03's checkpoint recording wait for DEL-03-02's dispositions and identities at their stated maturity; DEL-02-03's external-channel recording waits for DEL-03-03's observations; DEL-02-03's App-side positive capture fixtures wait for DEL-01-04's act control (a later undertaking), and are AWAITING INPUT on that account (EXEC §5, CH-23) |
| SCC-003 | [SCC-CASE-003](../../cases/SCC-CASE-003/Case_Datasheet.md) | 2 | 2 (2) | 2 | Unchanged |
| SCC-004 | [SCC-CASE-005](../../cases/SCC-CASE-005/Case_Datasheet.md) | 3 | 4 (4) | 8 | Unchanged |
| SCC-005 | [SCC-CASE-006](../../cases/SCC-CASE-006/Case_Datasheet.md) | 2 | 2 (2) | 3 | Unchanged |
| SCC-006 | [SCC-CASE-007](../../cases/SCC-CASE-007/Case_Datasheet.md) | 2 | 2 (2) | 3 | Unchanged |

### Exclusions

- **NOT_TOPOLOGICAL (207):** 149 EXTERNAL, 26 DOCUMENT, 18 PACKAGE, 14 UNKNOWN. They remain inputs at their own points of need ([Evidence/NonTopologicalInputs.csv](Evidence/NonTopologicalInputs.csv)). DAG-001's A/B/C account, as carried by DAG-002, is carried by row identity: 191 rows unchanged apart from `LastSeen`, 16 with edited fields (named per row), 0 new. One EXTERNAL row was retired since DAG-002 (DEP-01-04-014, an OI-002 constraint, `source_revised`).
- **MIRROR (54) and SAME_ARC (2):** each names its representative. No comparison is new since DAG-002. [Evidence/MirrorAssessment.md](Evidence/MirrorAssessment.md) carries every assessment and lists the 17 comparisons whose evidence text was re-quoted; the two maturity differences from DAG-002 stand.

## Findings routed to owners (not blocking)

| Finding | Owner route |
|---|---|
| **Closed by this change:** V12 F1 (34 quotes dropped inline-code backticks). All 34 cells are now exact substrings of their SoWs (ASC-ISS-008; DX_SCC-CHECK sweep 820/820) | None; recorded here so the handoff can drop it |
| **Closed by DAG-002's publication:** the pointer form. `_DAG/_LATEST.md` is in SPEC §11.2 form and the registered analyzer reads it (`DEPARTURE` against DAG-002 with the same 5 pending; `NO_DEPARTURE_FOUND` against this candidate installed as DAG-003 in scratch, [Evidence/successor_currency_precheck.json](Evidence/successor_currency_precheck.json)) | None; [PROPOSED_LATEST.md](PROPOSED_LATEST.md) is the prepared §11.2 pointer for DAG-003 |
| Mirror RequiredMaturity differences: DEL-03-03 → DEL-04-01 (DEP-03-03-008 TBD / DEP-04-01-023 INITIALIZED) and DEL-09-06 → DEL-04-03 (DEP-09-06-015 TBD / DEP-04-03-031 INITIALIZED). Unchanged by SCA-V4-002 | Both register owners, via `dependency-extract` |
| SatisfactionStatus TBD/PENDING convention (P2 O-6). The four new rows use PENDING (1) and TBD (3), so the inconsistency persists | Register owners |
| V12 F8: OI-001/OI-002 constraint rows. Now retired in DEL-01-04 (DEP-01-04-014), DEL-02-03 and DEL-05-02; amended and kept in DEL-04-01, DEL-04-02, DEL-04-03 and DEL-09-06. Off-arc; a consistency point | Register owners |
| V12 F6: N-05 and N-07 rest on the supplier's statement only. ARC_EFFECT §5 left consumer-side wording out of SCA-V4-002 as outside its decided scope. Both arcs are held in SCC-002; no arc would change | Advice only; a later SoW amendment if the owner wants it |
| RS §10 DEL-03-02 cell and ADAPTER header wording (behind N-12/N-B8); deferred supplier-side mirror rows (P2 O-3) | DEL-04-03 and DEL-03-03 owners; register owners (unchanged from DAG-002) |
| `Open_Issues.csv` OI-001/OI-002 kept OPEN (DECISION-2, option A); the SoW text in DEL-09-07, DEL-01-04 and DEL-02-02 now aligned by SCA-V4-002. `Coverage_Telemetry.json` still STALE_REBUILD_REQUIRED | Owner / decomposition owner (carried) |
| SCA-V4-002 `audit-scope-closure` (step 5 of the owner's accepted order) and the confirmation of ASC-ISS-001's closure for SCA-V4-001 | `scope-change`, after this checkpoint |

## Limitations and open questions

- The candidate is not independently reviewed yet. A separate TASK instance must review it before checkpoint C decides it (method Stage 4; predecessor SUCCESSOR_PLAN §7 gives the brief outline).
- The semantic content of each added arc rests on the DX returns (DX_DEL-02-01, DX_DEL-02-03) and ARC_EFFECT §1, which used the Design files as corroboration only. This assembly does not re-certify the SoWs.
- The four arcs carried only by a supplier-side DOWNSTREAM row (N-05, N-06, N-07, N-20) are valid under SR-6; V12 read their consumer SoWs and found them warranted.
- Candidate arcs are non-gating. An acyclic admitted layer neither resolves the SCCs nor supplies their contributions. X-1 in particular records that DEL-02-03's App-side positive capture fixtures wait for a later undertaking; holding the arc does not make them ready.
- Unknowns stay `TBD` in the registers: RequiredMaturity TBD on 214 rows, SatisfactionStatus TBD on 304.

## Reproduction

From the repository root:

```text
python3 projects/chirality-app-v4/execution/_DAG/_Candidates/DAG-003/Evidence/assemble_graph.py
```

The script checks the manifest against the working bytes and the frozen commit, re-derives the nodes, applies SR-1…SR-7, runs the three `audit_dag.py` audits, checks accounting and fidelity, asserts that the added arcs are exactly the expected four and the admitted arc set equals DAG-002's, and asserts that no protected input (DAG-001, DAG-002, `_DAG/_LATEST.md`, registers, SoWs, `_STATUS.md`, the closure and currency snapshots) changed. Its hash and exact arguments are in [Evidence/Tool_Run.json](Evidence/Tool_Run.json). The follow-up currency audit after acceptance is expected to be `CURRENT` ([Evidence/successor_currency_precheck.json](Evidence/successor_currency_precheck.json)).

No `--markdown-out` report is published: its title and front matter are DEV-001-specific, and the JSON `dev001_projection` section is not relied on.
