# Accepted DAG-004 handoff

For `construct-local-work-graph` and every other consumer of the App v4 project graph. The owner's decision, its provenance and the reliance boundary are in [ACCEPTANCE_RECORD.md](ACCEPTANCE_RECORD.md).

## Identity and pointer

| Item | Value |
|---|---|
| Accepted version | `_DAG/DAG-004/`, accepted 2026-10-03 (DECISION-3 of run `APP-V4-SCA003-20261002`, checkpoint K3), covering project-dag checkpoints 1 and 2 |
| Pointer | `_DAG/_LATEST.md`, in SPEC §11.2 form: `Latest: DAG-004`, `Supersedes: DAG-003` |
| Supersedes | DAG-003, kept unchanged as history in `_DAG/DAG-003/`; DAG-002 and DAG-001 likewise |
| Change event | SCA-V4-003 (accepted at DECISION-1 and DECISION-2), applied by `scope-of-work` REVISE to 19 SoWs and `dependency-extract` UPDATE of 20 registers; departure reported by `_Evaluation/DAGCurrency/CURRENCY_APP_V4_SCA003_2026-10-03_1937` |
| Basis | commit `75764184b99ab006cd46c1d1c328cf7d5c4d0c8d`; [SOURCE_MANIFEST.sha256](SOURCE_MANIFEST.sha256) (130 entries, the same paths as DAG-001…003) |
| Inventory | GROUP3-20260928T001055Z `canonical/Deliverables.csv`, through `_Decomposition/checkpoint_snapshots/_LATEST_ACCEPTED.md`. 41 nodes, no exemptions |
| Integrity | [MANIFEST.sha256](MANIFEST.sha256); check it from this folder |
| Candidate record | `_DAG/_Candidates/DAG-004/` (byte-equal to the 33 presented files; staged originally in the run's `DAG_PREP/DAG-004/`) |
| Closure snapshot | `_Evaluation/DepClosure/CLOSURE_APP_V4_SCA003_2026-10-03_1936/` |
| Case home | `_DAG/cases/` |

## Objective, semantics, direction and completeness

- **Objective:** production-order and route-selection relationships within the App v4 project. It is not a cross-project graph and not a schedule.
- **Edge semantics:** the consumer requires the supplier's stated contribution, at the stated maturity or condition, before the stated part of its own work. An edge does not mean whole-deliverable completion.
- **Direction:** consumer → supplier. `UPSTREAM` rows read From → Target and `DOWNSTREAM` rows read Target → From.
- **Completeness:** `FULL` for the selected semantics, under `FULL_GRAPH` tracking, with the unresolved-input and candidate qualifications carried from DAG-001 through DAG-003.
- **Layers:**
  - 129 admitted arcs ([DependencyEdges.csv](DependencyEdges.csv)): DAG-003's 124 plus five;
  - 83 held, non-gating candidate arcs in six SCCs ([CandidateEdges.csv](CandidateEdges.csv));
  - 355 exclusions ([ExcludedRows.csv](ExcludedRows.csv)).

## Reading rule

1. **Blockers.** Dependency blockers come only from the admitted edges of the accepted, current version.
2. **Contributions and satisfaction.** Required contributions and their satisfaction are read from the live local `Dependencies.csv` and `_DEPENDENCIES.md`. That includes rows this version lists as `MIRROR` or `SAME_ARC`, and the non-topological inputs. The graph promotes no `SatisfactionStatus` or `RequiredMaturity`. `INITIALIZED` means only that a contract is defined.
3. **Candidate edges** are held and non-gating. They drive no blocker queue, wave, schedule, dispatch readiness or readiness claim, and holding one makes no work ready.
4. **`DAG pending`.** A deliverable the latest currency audit lists as `DAG pending` gets no ready or blocked verdict from dependencies until the owner decides its departure. Report the departure and the decision awaited instead.
5. **Scope of an edge.** A missing input constrains the stated part of the work that needs it, not the whole deliverable and not every member of an SCC.

## The 11 released deliverables

The acceptance of DAG-004 decided the departure that made these `DAG pending` under DAG-003. They are released and read their blockers from DAG-004's admitted layer:

DEL-01-02, DEL-01-03, DEL-01-04, DEL-01-05, DEL-02-01, DEL-02-02, DEL-02-03, DEL-02-04, DEL-03-03, DEL-04-02 and DEL-04-03.

For seven of them, release changes no verdict: DEL-01-02, 01-03, 01-05, 02-01, 02-04, 04-02 and 04-03 gained only new consumers or held arcs. **For the other four, DAG-004 adds admitted waits** (next section).

## The four new sequencing waits

These are admitted arcs. Each consumer is an SCC-002 member and each supplier lies outside SCC-002 and does not reach it, so the admitted layer stays acyclic.

| Arc | Consumer → supplier | Representative | What the stated part of the consumer waits for |
|---|---|---|---|
| NR-05 | DEL-01-04 → DEL-01-03 | DEP-01-04-020 (INITIALIZED / TBD) | DEL-01-03's collaboration mode, plan-mode element, item anchors and delegation availability, when composing the turns DEL-01-04 sends |
| NR-07 | DEL-01-04 → DEL-01-05 | DEP-01-04-021 (INITIALIZED / TBD) | DEL-01-05's model-selection state (no model shown as selected until the person chooses) and the reported Codex account (the person's identity at act capture) |
| NR-04 | DEL-02-02 → DEL-01-02 | DEP-02-02-020 (INITIALIZED / TBD) | DEL-01-02's definitions of ending a run and its App-start reconciliation event, for chained runs and interrupted registration attempts |
| NR-01 | DEL-02-03 → DEL-01-02 | DEP-02-03-028 (INITIALIZED / TBD) | DEL-01-02's custody events and run-reference tag and look-up, so an interrupted run is recovered as the same run with its checkpoint history (REQ-002) |
| NR-02 | DEL-03-03 → DEL-01-02 | DEP-03-03-015 (INITIALIZED / PENDING) | DEL-01-02's in-flight item state and relaunch fact for an external request interrupted by a Codex stop or an App relaunch |

- **Waiting deliverables:** DEL-01-04 (two suppliers), DEL-02-02, DEL-02-03 and DEL-03-03.
- **Scope of the wait:** only the stated part of each waits, for the named contribution at INITIALIZED. The rest of each deliverable is not constrained by these arcs.
- **Satisfaction:** read from the live registers. All five rows are TBD or PENDING today.
- **Suppliers:** DEL-01-02, DEL-01-03 and DEL-01-05 gain admitted consumers; their own blockers do not change.

## Route re-examination (a light check; V25 O-1)

Ten deliverables reach one of the four consumers through admitted arcs: DEL-03-04, DEL-09-02, DEL-09-06, DEL-09-07, DEL-09-11, DEL-10-03, DEL-10-04, DEL-11-01, DEL-11-02 and DEL-11-03. currency.md lists such work as advice; it is not `DAG pending`.

**The consequence is small.** Recomputed at publication over the admitted layers of DAG-003 and DAG-004:

- each of the ten already reached DEL-01-02 and DEL-01-05 under DAG-003;
- DEL-03-04, 09-02, 09-06, 09-07, 09-11 and 11-03 also already reached DEL-01-03;
- the new arcs add paths, not suppliers, to their routes.

New transitive admitted reach is limited to three deliverables:

- DEL-01-04 gains DEL-01-03 and DEL-01-05;
- DEL-02-03 and DEL-03-03 each gain DEL-01-02.

NR-04 gives DEL-02-02 a direct wait but no new reach. When one of the ten next relies on a route through these arcs, a glance at the new waits above is enough.

DAG-003's advice list (deliverables that consume DEL-04-03, DEL-02-01 and others) stands as written there.

## The five new held arcs, and X-1's narrow scope

| Arc | Consumer → supplier | Representative | What the consumer waits for |
|---|---|---|---|
| NR-08 | DEL-01-04 → DEL-04-02 | DEP-01-04-022 | The checkpoint overlay and standing facets DEL-04-02 defines, which DEL-01-04 places in the App (OUT-002) |
| NR-09 | DEL-01-04 → DEL-02-03 | DEP-01-04-023 | The checkpoint display meanings DEL-02-03 defines, whose App behaviour DEL-01-04 owns. Reciprocal with X-1: two arcs carrying different contributions |
| NR-4 | DEL-01-04 → DEL-02-04 | DEP-01-04-024 | The role list for the new-conversation role offer |
| R2-04-03-e | DEL-04-03 → DEL-02-01 | DEP-04-03-034 | The workflow identity tuple and checkpoint disposition vocabulary for the run record. Reciprocal with DEP-02-01-019 |
| R20-10 | DEL-04-03 → DEL-02-02 | DEP-04-03-035 | The run-start text and run-end line with content identity and supply-check record, the selection record and the A15 descriptor relations, as supplied-workflow evidence. Reciprocal with DEP-02-02-017 |

All five are `SCC_UNRESOLVED` inside the unchanged SCC-002 and cite SCC-CASE-002. Their contributions are live obligations, read from the registers.

**Standing note: X-1 is narrow (carried).** X-1 (DEL-02-03 → DEL-01-04, DEP-02-03-027) applies only to DEL-02-03's App-side positive capture fixtures (OUT-003, VER-003), which wait for DEL-01-04. It is not a whole-deliverable wait. Holding it does not make the fixtures ready. NR-09 now runs the other way between the same pair, carrying a different contribution; it does not widen X-1.

## Representatives changed by rule (no arc or layer change)

Seven existing arcs gained the consumer's own UPSTREAM row, which SR-6 selects:

- **held:** DEL-02-03 → DEL-04-02 (DEP-02-03-029), DEL-03-02 → DEL-04-02 (DEP-03-02-034), DEL-03-03 → DEL-02-01 (DEP-03-03-017), DEL-03-03 → DEL-04-02 (DEP-03-03-016), DEL-04-03 → DEL-02-04 (DEP-04-03-036);
- **admitted:** DEL-05-01 → DEL-01-05 (DEP-05-01-026), DEL-09-06 → DEL-09-01 (DEP-09-06-035).

The former representatives are MIRROR rows and keep their obligations. On the two admitted arcs the old and new representatives carry the same maturity and satisfaction, so no verdict changed.

**V25 m-1, for the register owners: DEL-05-01 → DEL-01-05.**

- **The gating row disclaims a requirement.** The new representative, DEP-05-01-026 (UPSTREAM INTERFACE, INITIALIZED / PENDING), quotes the accepted P1-10 sentence. That sentence receives DEL-01-05's capability handoff "as information" and takes "no requirement of this contract" from it.
- **The supplier row says the opposite.** The former representative, DEP-01-05-014, says DEL-01-05 supplies requirements to DEL-05-01.
- **The arc still gates.** It was already admitted in DAG-003, and its verdict is unchanged.
- **Reading until reconciled:** read both rows. Treat the stated part of DEL-05-01 that needs DEL-01-05's capability handoff as waiting at INITIALIZED, as before.
- **Reconciliation:** the DEL-05-01 and DEL-01-05 register owners reconcile the type or the statement through `dependency-extract`. If that turns the arc into a non-requirement, it is a departure for a later successor.

## Standing note: DEL-01-01 as supplier (carried)

DEL-01-01 (Stock Codex hosting and supplier contract) remains an admitted supplier through the arcs DAG-002 admitted. SCA-V4-003 added mirror rows on its side (R-11-1) but no arc. It stays in SCC-001 with DEL-01-05 (SCC-CASE-001), whose two held arcs are unchanged.

**Guard.** A reverse row in which DEL-01-01 consumes one of its consumers would merge SCCs (ARC_ANALYSIS §4.2, K-3…K-5). None is in any register.

## Standing note: the DEL-09-06 reverse-arc guard (carried)

The guard held through SCA-V4-003. Across both layers of DAG-004, recomputed at publication:

- DEL-09-06 reaches the same 20 deliverables as under DAG-003: DEL-01-01…01-06, DEL-02-01…02-04, DEL-03-01…03-03, DEL-04-01…04-03, DEL-05-01, DEL-05-02, DEL-09-01 and DEL-09-09;
- it is consumed only by DEL-03-04 and DEL-09-07.

A new ACTIVE row is an **SCC-forming departure** if it:

- makes any of those 20 consume DEL-09-06, or consume a deliverable that consumes it; or
- makes DEL-09-06 consume DEL-03-04, DEL-09-07, or anything that consumes them.

Such a departure is decided by the owner and routed to `scc-resolution-case`. The tested citations E-1, K-11, E-5 and K-7 (ARC_ANALYSIS §4.1–4.2) remain absent. K-6 (DEL-09-06 → DEL-09-09) would form no SCC but would still be an added-arc departure.

**Other guards carried and holding:**

- R17-10: DEL-01-02 reaches only DEL-01-01, 01-05 and 04-01; DEL-01-03 reaches those three and DEL-01-02.
- DEL-04-01 has no supplier.
- N-12, N-B8, NR-03, NR-06 and NR-10 are absent.

## Candidate edges held, and the work lacking their inputs

All 83 held arcs are `SCC_UNRESOLVED` and cite their case. No case opened or closed with DAG-004. CASE-002's evidence update for this version is drafted (`_Coordination/AgentRuns/APP-V4-SCA003-20261002/DAG_PREP/CASE-002_EVIDENCE_UPDATE.proposed.md`) and is applied separately through `scc-resolution-case`.

| SCC | Case | Members | Held arcs | Work lacking input |
|---|---|---:|---:|---|
| SCC-001 | SCC-CASE-001 | 2 | 2 | DEL-01-01 ↔ DEL-01-05: the work that needs the selected pin/protocol and the embedding contribution |
| SCC-002 | SCC-CASE-002 (CASE-004 as history) | 13 | 71 (66 in DAG-003, plus the 5 new) | Definition proceeds on provisional versions; each dependent part that needs a named contribution waits for it at its stated maturity. **New with DAG-004:** DEL-01-04's App placement of checkpoint overlays, display meanings and the role offer waits for DEL-04-02, DEL-02-03 and DEL-02-04. DEL-04-03's run record waits for DEL-02-01's identity tuple and vocabulary and for DEL-02-02's run text and selection record. **Carried:** DAG-003's waits (N-18, N-21, N-24, X-1; R8-A, R8-B) |
| SCC-003 | SCC-CASE-003 | 2 | 2 | Unchanged |
| SCC-004 | SCC-CASE-005 | 3 | 4 | Unchanged |
| SCC-005 | SCC-CASE-006 | 2 | 2 | Unchanged |
| SCC-006 | SCC-CASE-007 | 2 | 2 | Unchanged |

SCC-002's 13 members are DEL-01-04, DEL-02-01, DEL-02-02, DEL-02-03, DEL-02-04, DEL-03-01, DEL-03-02, DEL-03-03, DEL-04-02, DEL-04-03, DEL-05-01, DEL-05-02 and DEL-09-09.

## Exclusions still relevant to readiness

- **NOT_TOPOLOGICAL (208):** 151 EXTERNAL, 26 DOCUMENT, 17 PACKAGE and 14 UNKNOWN rows. They are not graph arcs, but they remain inputs at their own points of need ([Evidence/NonTopologicalInputs.csv](Evidence/NonTopologicalInputs.csv)). Since DAG-003, two EXTERNAL rows were added (DEP-04-01-033, DEP-05-01-027) and one PACKAGE row was retired (DEP-03-01-022).
- **MIRROR (145) and SAME_ARC (2):** each names its arc's representative and keeps its own obligation, read from the live register ([Evidence/MirrorAssessment.md](Evidence/MirrorAssessment.md)).
- **Mirror maturity differences.** The two DAG-003 differences are reconciled (both rows INITIALIZED). Three new ones remain, each with the consumer at TBD and the supplier at INITIALIZED:
  - DEL-06-01 → DEL-01-01 (DEP-06-01-013 / DEP-01-01-030);
  - DEL-09-01 → DEL-01-01 (DEP-09-01-019 / DEP-01-01-031);
  - DEL-08-02 → DEL-02-01 (DEP-08-02-006 / DEP-02-01-037).

  Until the register owners reconcile them, read both rows.

## Coordination concentrations (V25 m-2)

These are not defects. Degree is counted across both layers, from the closure snapshot's `Evidence/hubs.csv` at threshold 20:

| Deliverable | DAG-003 | DAG-004 | Why |
|---|---:|---:|---|
| DEL-04-03 | 27 | 29 | R2-04-03-e and R20-10 (held) |
| DEL-02-03 | 23 | 25 | NR-01 (admitted) and NR-09 (held) |
| DEL-02-01 | 20 | 21 | R2-04-03-e (held) |
| DEL-04-01 | 20 | 20 | 20 admitted dependents, still no suppliers |

DEL-01-04 gains five outgoing arcs (NR-05, NR-07, NR-08, NR-09, NR-4) but stays below the threshold.

## Open matters and carried obligations, with owners

Closed since DAG-003, and dropped from this list:

- the two mirror maturity differences;
- V12 F6, and the note on arcs carried only by a supplier-side row: N-05, N-06, N-07 and N-20 now have consumer rows.

| Matter | Owner and route |
|---|---|
| **DEL-01-03 absolute TargetLocation.** 14 rows of DEL-01-03's register record a location under a personal home folder: DEP-01-03-001…010 are ANCHOR rows; DEP-01-03-011 and -012 are admitted representatives, copied byte for byte here as in DAG-002 and DAG-003; DEP-01-03-013 is a MIRROR; DEP-01-03-014 is NOT_TOPOLOGICAL. V25 O-2 adds that analyzer outputs (`closure_summary.json`, the currency `analyzer.stdout.json`) also carry absolute paths, as in earlier snapshots | DEL-01-03 register owner, `dependency-extract`, **after acceptance** (DECISION-3 effect 4). The repair changes bytes, not arcs; the next currency audit is then expected to read `CURRENT_WITH_EVIDENCE_DRIFT` |
| **Five expected mirror rows not extracted:** DEL-01-01 → DEL-02-04 and → DEL-04-03; DEL-01-05 → DEL-01-01; DEL-03-02 → DEL-03-01; DEL-03-03 → DEL-02-03. Each arc exists through the consumer's row; no graph effect | Owner: a receivers sentence in a later revision, or a declared entry in the supplier's `_DEPENDENCIES.md` (SCA-V4-003 Q-15 alternative) |
| **V25 m-1:** the DEL-05-01 → DEL-01-05 representative (above) | DEL-05-01 and DEL-01-05 register owners, `dependency-extract` |
| The three new mirror maturity differences listed under exclusions | Both register owners, `dependency-extract` |
| **SatisfactionStatus TBD/PENDING convention** (P2 O-6; R-02-4 held at SCA-V4-003 Q-14). The ten new representatives use TBD (7) and PENDING (3) | Register owners |
| **OI-001/OI-002 constraint rows** (V12 F8). SCA-V4-003 refreshed DEP-01-03-017 to the OI-001 residue (R3-01-03-e). Rows naming OI-001 or OI-002 stay ACTIVE in nine registers. Off-arc; a consistency point | Register owners |
| The RS §10 DEL-03-02 cell and the ADAPTER header wording behind N-12/N-B8 | DEL-04-03 and DEL-03-03 owners |
| **CASE-002 evidence update** (drafted, not applied) | `scc-resolution-case`, a later bounded brief |
| **`Coverage_Telemetry.json` is stale** (STALE_REBUILD_REQUIRED, carried from SCA-V4-001) | Decomposition owner, by a later bounded brief |
| **The 17 Design re-pins** (carried from SCA-V4-001; deferral record `APP-V4-BASIS-ALIGN-20260928` DECISION-8). No graph arc rests on a Design file | Owner, separately governed; not a graph matter |
| **SCA-V4-003 derivative closure.** `_ScopeChange/_LATEST.md` reads `OPEN_PENDING_DERIVATIVE_CLOSURE`; this accepted graph is one of its derivative packages and does not itself close the amendment | `scope-change` / `audit-scope-closure` |
| Unknowns stay `TBD` in the registers: RequiredMaturity on 212 ACTIVE EXECUTION rows, SatisfactionStatus on 357 | Register owners, as work proceeds |

## Currency

**Latest result.** `_Evaluation/DAGCurrency/_LATEST.md` locates the latest currency audit. The follow-up audit after this acceptance reports `CURRENT`, with nothing `DAG pending`. The audit `CURRENCY_APP_V4_SCA003_2026-10-03_1937` was run against DAG-003 and is now historical.

**Commands.** Run the first from this folder and the second from the execution root, `projects/chirality-app-v4/execution`:

```text
shasum -a 256 -c MANIFEST.sha256
shasum -a 256 -c _DAG/DAG-004/SOURCE_MANIFEST.sha256
```

Then check that `_Decomposition/checkpoint_snapshots/_LATEST_ACCEPTED.md` still names GROUP3-20260928T001055Z. If any source failed, re-apply the accepted selection rules as a scratch assembly and compare the arc sets, the SCCs and the inventory (`workflows/project-dag/resources/currency.md`).

**Cross-check.** The registered closure analyzer, run from the repository root, reads the §11.2 pointer:

```text
python3 tools/coordination/analyze_dep_closure.py projects/chirality-app-v4/execution --scope ALL --filter-active-only true --normalize-ids true --dependency-class EXECUTION --target-type DELIVERABLE --hub-threshold 20 --max-cycles 200 --include-declared true
```

Its `accepted_dag` section reports the comparison.

**When to audit:**

- before relying on DAG-004 for a route or a blocker verdict when the local files may have changed since its basis or since the latest audit;
- after `dependency-extract` runs on any in-scope deliverable (including the DEL-01-03 repair), or after a human changes declarations;
- after an accepted scope change or decomposition revision;
- when a consumer finds the graph and a local file disagree;
- after the owner decides a departure.

A new session is not, by itself, a reason to rebuild. The CASE-002 evidence update and the SCA-V4-003 closure audit change none of this version's sources, so they are not, by themselves, a reason to audit.
