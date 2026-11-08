# DAG-004 — successor graph candidate

**Standing: an unaccepted candidate, assembled and strictly audited, prepared for the owner's graph checkpoint.** The independent review by a separate TASK instance has not happened yet. Nothing here accepts a graph, moves `_DAG/_LATEST.md`, satisfies a dependency, changes lifecycle or passes a gate.

**Staged location.** The candidate is staged at `_Coordination/AgentRuns/APP-V4-SCA003-20261002/DAG_PREP/DAG-004/` because the D1 brief fences writes out of `_DAG/`. Its method home is `_DAG/_Candidates/DAG-004/`, and on acceptance `_DAG/DAG-004/`. Paths in this file are given from the execution root `projects/chirality-app-v4/execution/` (written `E/` below) rather than as relative links, so the bytes stay valid after a byte-for-byte copy.

## Identity

| Field | Value |
|---|---|
| Graph | DAG-004 (next unused number; `_DAG/` holds DAG-001…003 and `_Candidates/DAG-001…003`) |
| Trigger | `SUCCESSOR` |
| Predecessor | DAG-003, accepted 2026-09-29 (`E/_DAG/DAG-003/ACCEPTANCE_RECORD.md`, covering project-dag checkpoints 1 and 2) |
| Change event | The accepted scope change SCA-V4-003 (run `APP-V4-SCA003-20261002`, DECISION-1 for groups 1–2 and DECISION-2 for group 3), applied by `scope-of-work` REVISE to 19 ScopeOfWork files (`2d5e6845c5`) and `dependency-extract` UPDATE of 20 registers (`0e3c55eec5`) |
| Currency audit | `DAG_PREP/CURRENCY_APP_V4_SCA003_2026-10-03_1937/CURRENCY_REPORT.md`: `DEPARTURE`, 10 arcs added (5 admitted, 5 held), 0 removed, SCCs and inventory unchanged, 11 deliverables `DAG pending` |
| Departures this candidate decides | The 10 added arcs in `Evidence/DepartureAccount.csv`: NR-05, NR-07, NR-01, NR-02, NR-04 (admitted); NR-08, NR-09, NR-4, R2-04-03-e, R20-10 (held) |
| Run | `APP-V4-SCA003-20261002`, node D1 (`ASSEMBLY_RUN.md`) |

## Carried forward from DAG-003 (not re-decided)

These stand from DAG-003 (`E/_DAG/DAG-003/GRAPH_BASIS.md`, `ACCEPTANCE_RECORD.md`) and through it from DAG-001's BASIS_DECISION. The departure does not touch their rows, arcs or warrants.

- **Objective.** Production-order and route-selection relationships in this App project. Not a cross-project graph and not a schedule.
- **Edge semantics.** The consumer requires the supplier's stated contribution, at the stated maturity or condition, before the stated part of its work. Not whole-deliverable completion.
- **Direction.** Consumer → supplier ("depends on"): UPSTREAM is From → Target, DOWNSTREAM is Target → From. Source `Direction` is preserved.
- **Tracking and completeness.** FULL_GRAPH (`E/_Coordination/_COORDINATION.md`; all 41 `_DEPENDENCIES.md`). Completeness **FULL for the selected semantics**, with the explicit unresolved-input and candidate qualifications below.
- **Inventory.** GROUP3-20260928T001055Z `canonical/Deliverables.csv`, through `E/_Decomposition/checkpoint_snapshots/_LATEST_ACCEPTED.md` (byte-unchanged since DAG-003). 41 nodes in 11 packages, all `PRESENT`, no exemptions. `DeliverableNodes.csv` was re-derived from the register and is byte-equal to DAG-003's (and DAG-001's and DAG-002's).
- **Case home.** `E/_DAG/cases/`.
- **Selection rules.** SR-1…SR-7 as confirmed: all canonical DependencyTypes admitted (SR-3); no cut or merge ruling (SR-4); no confirmation hold (SR-5); one representative per arc, consumer UPSTREAM first, then DECLARED, then lowest DependencyID (SR-6); every intra-SCC representative held (SR-7).
- **Rulings.** None new. CP1-20260928 (case tracking) carries forward. The N-12/N-B8 withholding remains a register-level decision, not an SR-4 cut, and so does NR-03's drop (SCA-V4-003 Q-4).
- **Maturity reading.** `INITIALIZED` is defined-contract maturity only. SatisfactionStatus is never promoted by the graph.
- **DEL-01-01 as supplier and DEL-09-06 as consumer**, with the DEL-09-06 reverse-arc guard as a standing note. The guard held: DEL-09-06 still reaches the same 20 deliverables across both layers and is consumed only by DEL-03-04 and DEL-09-07 (`Evidence/DepartureAccount.json`).
- **Reliance boundary.** Unchanged in kind. Acceptance would satisfy no dependency, advance no lifecycle, lift no hold, pass no gate and release nothing.
- **Tool strictness.** `audit_dag.py --canonical --strict` must exit 0. No strictness exception is taken.

## Reopened decisions (checkpoint 1, limited to these)

The arc set was decided at the SCA-V4-003 checkpoint K1 (`RUN/OWNER_DECISIONS.md` DECISION-1, "accept the remaining items as recommended": Q-4 the 10 new links with NR-01, NR-02 and NR-04's sentences and NR-03 dropped; Q-15 the receivers sentences; Q-17 the 15 further mirror rows). Group 3 was accepted at K2 (DECISION-2), which routed the register UPDATE, the currency audit and a DAG-004 candidate back to the owner.

| Decision | Recorded answer | Result in the evidence |
|---|---|---|
| The 10 arcs as the departure scope (Q-4) | Accepted as recommended | All 10 present, each in its predicted layer, one consumer-side UPSTREAM INTERFACE representative each; none extra, none missing (`Evidence/DepartureAccount.json`) |
| NR-03 dropped (R22-4) | Dropped | DEL-09-09 → DEL-01-02 absent |
| REQ-008 adjusted so DEL-04-01 gains no supplier (Q-5) | Accepted as adjusted | DEL-04-01 → DEL-01-04 and DEL-04-03 → DEL-01-04 absent; DEL-04-01 has 0 suppliers |
| R17-10 cycle guard; NR-06 and NR-10 withdrawn | Guarded | DEL-01-02 reaches only DEL-01-01, 01-05, 04-01; DEL-01-03 those and DEL-01-02; NR-06, NR-10 absent |
| N-12, N-B8 and the DEL-09-06 reverse citations stay out | Carried | All absent |
| CASE-002 continues, gaining held arcs | Carried as case tracking under CP1-20260928 | The closure's SCC-002 has the same 13 members. The case-file evidence update is **drafted, not applied** (`DAG_PREP/CASE-002_EVIDENCE_UPDATE.proposed.md`): the D1 brief fences case writes |
| Mirror rows (Q-15, Q-17) | Included | 91 extracted; 5 not extracted, all on arcs a consumer row already carries (carried obligation) |

**New in kind, compared with DAG-003: the admitted layer changes.** Five arcs enter the sequencing layer, and four SCC-002 members (DEL-01-04, DEL-02-02, DEL-02-03, DEL-03-03) gain admitted suppliers outside the cycle. No SCC needs a ruling and no cut, merge, hold or type exclusion is proposed. Checkpoints 1 and 2 may therefore still be decided together (method: "a small undertaking with no SCC needing a ruling"); the acceptance record must then state that it covers both.

## Basis

| Item | Value |
|---|---|
| Source revision | `75764184b99ab006cd46c1d1c328cf7d5c4d0c8d`, clean tree |
| Manifest | `SOURCE_MANIFEST.sha256`, SHA-256 `03aa668b88cb1cb32e1d26a15fb64afdf85e0af6fbb61ec89f833eaf5893a8ef`, 130 entries: the same paths, in the same order, as DAG-001…003. 59 changed since DAG-003: 19 `ScopeOfWork.md`, 20 `Dependencies.csv`, 20 `_DEPENDENCIES.md` |
| Closure snapshot | `DAG_PREP/CLOSURE_APP_V4_SCA003_2026-10-03_1936/`, computed on this manifest (`SOURCE_BASIS.json`). Coverage PASS; six SCCs, `scc_summary.csv` byte-identical to the SCA-V4-002 closure; raw acyclic closure BLOCKER, as for every earlier version |
| Provenance | `SOURCE_BASIS.json`: revision, manifest, closure, currency, cases, tools, decisions and returns, with hashes |

## Result

| Account | DAG-003 | DAG-004 | Change |
|---|---:|---:|---|
| Nodes | 41 | 41 | none (byte-equal) |
| ACTIVE EXECUTION rows | 465 | 567 | +103 added, −1 retired (DEP-03-01-022, PACKAGE target) |
| Admitted arcs (`DependencyEdges.csv`) | 124 | **129** | **+5**; the other 124 are DAG-003's arcs; 2 of their representatives changed by rule (below) |
| Held arcs (`CandidateEdges.csv`) | 78 | **83** | +5, all in SCC-002; 5 representatives changed by rule |
| Excluded rows (`ExcludedRows.csv`) | 263 | 355 | NOT_TOPOLOGICAL 208, MIRROR 145, SAME_ARC 2 |
| SCCs | 6 | 6 | identical member sets |
| Reciprocal pairs | 24 | 27 | +3, all inside SCC-002 |
| Arcs removed; existing arcs changing layer | — | 0; 0 | — |

The balance is 129 + 83 + 355 = 567, with no row missing or placed twice. All 212 admitted and candidate rows equal their source rows in the 29 core columns, byte for byte, and carry non-blank canonical `Explicitness`, `SatisfactionStatus` and `Confidence`. Per-register balance and closure consistency: `Evidence/Accounting.md`.

**Strict audit.** `python3 tools/coordination/audit_dag.py --dag-dir <candidate> --canonical --strict --json-out <candidate>/Evidence/dag_audit.json`, run from the repository root: **exit 0**. 129 edges, 41 nodes, 0 canonical findings, 0 endpoint issues, 0 SCCs, 0 duplicates, 0 bidirectional pairs, 0 ragged rows (`Evidence/dag_audit.json`, `Evidence/Tool_Run.json`). The admissible set (212 arcs) and the candidate layer (83) were audited without `--strict`; both exit 0 with the expected cyclic subjects and six SCCs.

### Admitted arcs added (5)

Each consumer is an SCC-002 member; each supplier lies outside SCC-002 and does not reach it, so the admitted layer stays acyclic (R17-10 reachability above). With these arcs, DEL-01-02, DEL-01-03 and DEL-01-05 come before SCC-002 in the admitted order.

| Label | Consumer → supplier | Representative (RequiredMaturity / Satisfaction) | Mirror | What the consumer waits for (row Statement, abridged) |
|---|---|---|---|---|
| NR-05 | DEL-01-04 → DEL-01-03 | DEP-01-04-020 (INITIALIZED / TBD) | DEP-01-03-022 | The collaboration mode, plan-mode element, item anchors and delegation availability, when composing the turns it sends |
| NR-07 | DEL-01-04 → DEL-01-05 | DEP-01-04-021 (INITIALIZED / TBD) | — | The model-selection state and the reported Codex account (no model shown as selected until the person chooses; the account used for the person's identity at act capture) |
| NR-01 | DEL-02-03 → DEL-01-02 | DEP-02-03-028 (INITIALIZED / TBD) | DEP-01-02-024 | DEL-01-02's custody events and run-reference tag and look-up, so an interrupted run is recovered as the same run with its checkpoint history (REQ-002) |
| NR-02 | DEL-03-03 → DEL-01-02 | DEP-03-03-015 (INITIALIZED / PENDING) | DEP-01-02-025 | The in-flight item state and relaunch fact for an external request interrupted by a Codex stop or App relaunch |
| NR-04 | DEL-02-02 → DEL-01-02 | DEP-02-02-020 (INITIALIZED / TBD) | DEP-01-02-026 | DEL-01-02's definitions of ending a run and its App-start reconciliation event, for chained runs and interrupted registration attempts |

**Effect on verdicts.** On acceptance, the stated part of each consumer that needs the named contribution reads a blocker from that supplier at INITIALIZED; satisfaction is read from the live registers. The rest of each consumer is not constrained by these arcs. DEL-01-02, DEL-01-03 and DEL-01-05 gain admitted consumers; their own blockers do not change.

### Held arcs added (5)

All `SCC_UNRESOLVED` inside the unchanged SCC-002, citing `E/_DAG/cases/SCC-CASE-002`. Holding them changes no verdict.

| Label | Consumer → supplier | Representative | What it carries | Reciprocal with |
|---|---|---|---|---|
| NR-08 | DEL-01-04 → DEL-04-02 | DEP-01-04-022 (INITIALIZED / TBD) | The checkpoint overlay and standing facets DEL-04-02 defines, placed in the App (OUT-002) | — |
| NR-09 | DEL-01-04 → DEL-02-03 | DEP-01-04-023 (INITIALIZED / TBD) | The checkpoint display meanings DEL-02-03 defines, whose App behaviour DEL-01-04 owns | X-1 (DEP-02-03-027): new pair |
| NR-4 | DEL-01-04 → DEL-02-04 | DEP-01-04-024 (INITIALIZED / TBD); mirror DEP-02-04-019 | The role list for the new-conversation role offer | — |
| R2-04-03-e | DEL-04-03 → DEL-02-01 | DEP-04-03-034 (INITIALIZED / PENDING) | The workflow identity tuple and checkpoint disposition vocabulary for the run record | DEP-02-01-019: new pair |
| R20-10 | DEL-04-03 → DEL-02-02 | DEP-04-03-035 (INITIALIZED / PENDING); mirror DEP-02-02-024 | Run-start text and run-end line with content identity and supply-check record, the selection record and the A15 descriptor relations, as supplied-workflow evidence | DEP-02-02-017: new pair |

### Representatives changed by rule (7; no arc or layer change)

Seven existing arcs gained a consumer-side UPSTREAM row (SCA-V4-003 mirror items), which SR-6 ranks first. Held: DEL-02-03 → DEL-04-02 (DEP-02-03-029), DEL-03-02 → DEL-04-02 (DEP-03-02-034), DEL-03-03 → DEL-02-01 (DEP-03-03-017), DEL-03-03 → DEL-04-02 (DEP-03-03-016), DEL-04-03 → DEL-02-04 (DEP-04-03-036). Admitted: DEL-05-01 → DEL-01-05 (DEP-05-01-026), DEL-09-06 → DEL-09-01 (DEP-09-06-035). The former representatives are now MIRROR rows. Details: `Evidence/MirrorAssessment.md`.

### Candidate layer

All 83 held arcs are `SCC_UNRESOLVED` and cite their case. Each held row carries DAG-003's `OpenQuestion` text for its case, unchanged. No case opens or closes. All cases stay EVIDENCE_ACCUMULATING with the CP1-20260928 tracking record. No case file was written by this node.

| SCC | Case | Members | Held arcs (DAG-003) | Source rows (DAG-003) | What would resolve it, and the work lacking input |
|---|---|---:|---:|---:|---|
| SCC-001 | SCC-CASE-001 | 2 | 2 (2) | 4 (4) | As DAG-001: the selected pin/protocol and embedding contribution |
| SCC-002 | SCC-CASE-002 (CASE-004 history) | 13 | **71 (66)** | 128 (80) | As DAG-003, plus the 5 new held interfaces. Definition proceeds on provisional versions. DEL-01-04's App placement of checkpoint overlays, display meanings and the role offer waits for DEL-04-02, DEL-02-03 and DEL-02-04 at INITIALIZED; DEL-04-03's run record waits for DEL-02-01's identity tuple and vocabulary and for DEL-02-02's run text and selection record. X-1 stays narrow (DEL-02-03's App-side positive capture fixtures) |
| SCC-003 | SCC-CASE-003 | 2 | 2 (2) | 2 (2) | Unchanged |
| SCC-004 | SCC-CASE-005 | 3 | 4 (4) | 8 (8) | Unchanged |
| SCC-005 | SCC-CASE-006 | 2 | 2 (2) | 3 (3) | Unchanged |
| SCC-006 | SCC-CASE-007 | 2 | 2 (2) | 3 (3) | Unchanged |

### Exclusions

- **NOT_TOPOLOGICAL (208):** 151 EXTERNAL, 26 DOCUMENT, 17 PACKAGE, 14 UNKNOWN. They remain inputs at their own points of need (`Evidence/NonTopologicalInputs.csv`). The A/B/C account is carried by row identity: 191 rows unchanged apart from `LastSeen`, 15 with edited fields (named per row), 2 new EXTERNAL rows not classified (DEP-04-01-033, DEP-05-01-027), and 1 retired since DAG-003 (DEP-03-01-022).
- **MIRROR (145) and SAME_ARC (2):** each names its representative. 91 comparisons are new. `Evidence/MirrorAssessment.md` carries every assessment: the two DAG-003 maturity differences are reconciled, three new ones are routed to owners, 88 new pairs are compared mechanically with a bounded reading of 15.

## Findings routed to owners (not blocking)

| Finding | Owner route |
|---|---|
| **Closed by this change:** DAG-003's two mirror maturity differences (DEP-03-03-008/DEP-04-01-023; DEP-09-06-015/DEP-04-03-031), now both INITIALIZED; V12 F6 and the "arcs carried only by a supplier-side row" note (N-05, N-06, N-07, N-20 now have consumer rows) | None; the handoff can drop them |
| **New mirror maturity differences (3):** DEL-06-01 → DEL-01-01, DEL-09-01 → DEL-01-01, DEL-08-02 → DEL-02-01 (consumer TBD, supplier INITIALIZED) | Both register owners, through `dependency-extract` |
| **Five expected mirror rows not extracted** (DX_SCC-CHECK): DEL-01-01 → DEL-02-04, → DEL-04-03; DEL-01-05 → DEL-01-01; DEL-03-02 → DEL-03-01; DEL-03-03 → DEL-02-03. No arc effect | Owner: a receivers sentence in a later revision, or a declared entry in the supplier's `_DEPENDENCIES.md` (Q-15 alternative) |
| **DEL-01-03 absolute `TargetLocation`** under a personal home path on 14 rows (10 ANCHOR; DEP-01-03-011 and -012 admitted representatives, copied byte for byte as in DAG-002/003; DEP-01-03-013, -014 excluded) | DEL-01-03 register owner, `dependency-extract`; then re-freeze. A repair changes bytes, not arcs |
| SatisfactionStatus TBD/PENDING convention (P2 O-6; R-02-4 held at Q-14). The 10 new representatives use TBD (7) and PENDING (3) | Register owners |
| OI-001/OI-002 constraint rows (V12 F8). SCA-V4-003 refreshed DEP-01-03-017 to the OI-001 residue with OI-002 recorded as ruled (R3-01-03-e) and re-referenced DEP-04-03-019. Rows naming OI-001 or OI-002 stay ACTIVE in DEL-01-03, DEL-01-04 (OI-001 only), DEL-04-01, DEL-04-02, DEL-04-03, DEL-06-02, DEL-09-02, DEL-09-06 and DEL-09-07. Off-arc; a consistency point | Register owners |
| RS §10 DEL-03-02 cell and ADAPTER header wording behind N-12/N-B8 | DEL-04-03 and DEL-03-03 owners (unchanged) |
| **The Design re-pins and `Coverage_Telemetry.json`** (STALE_REBUILD_REQUIRED), carried from SCA-V4-001; SCA-V4-003's closure stays `OPEN_PENDING_DERIVATIVE_CLOSURE` | Owner and decomposition owner, separately governed; not graph matters |
| **The accepted DAG is a derivative package of SCA-V4-003** (and of the SCA-V4-002 closure audit) | `scope-change` / `audit-scope-closure`, after this checkpoint |

## Limitations and open questions

- The candidate is not independently reviewed yet. A separate TASK instance must review it before the owner decides (method Stage 4).
- The candidate is staged outside `_DAG/`, and so are its closure and currency snapshots. Publication must place them in their method homes (see `DAG_PREP/CHECKPOINT_C.md` §6). `Evidence/assemble_graph.py` is location-independent and reruns after the copy.
- The semantic content of each added arc rests on the ScopeOfWork sentences the owner accepted (SOW_REVISIONS_A/B), the DX returns and ARC_EFFECT §1. This assembly does not re-certify the SoWs.
- Candidate arcs are non-gating. An acyclic admitted layer neither resolves the SCCs nor supplies their contributions.
- Unknowns stay `TBD` in the registers: RequiredMaturity TBD on 212 rows, SatisfactionStatus TBD on 357.

## Reproduction

From the repository root:

```text
python3 projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-SCA003-20261002/DAG_PREP/DAG-004/Evidence/assemble_graph.py
```

(or the same script at its copied location). It checks the manifest against the working bytes and the frozen commit, re-derives the nodes, applies SR-1…SR-7, runs the three `audit_dag.py` audits, checks accounting and fidelity, asserts that the added arcs are exactly the expected ten in their predicted layers, that the admitted arc set is DAG-003's plus the five, that the seven representative changes are exactly the expected consumer-side rows, and that the guards hold, and asserts that no protected input changed (DAG-001…003, `_DAG/_Candidates/`, `_DAG/cases/`, `_DAG/_LATEST.md`, registers, SoWs, `_STATUS.md`, `_Evaluation/`, and the closure and currency snapshots). Its hash and exact arguments are in `Evidence/Tool_Run.json`. The follow-up currency audit after acceptance is expected to be `CURRENT` (`Evidence/successor_currency_precheck.json`: `NO_DEPARTURE_FOUND`, 0 pending).

No `--markdown-out` report is published: its title and front matter are DEV-001-specific, and the JSON `dev001_projection` section is not relied on.
