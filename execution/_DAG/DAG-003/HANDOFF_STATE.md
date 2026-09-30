# Accepted DAG-003 handoff

For `construct-local-work-graph` and every other consumer of the App v4 project graph. The owner's decision, its provenance and the reliance boundary are in [ACCEPTANCE_RECORD.md](ACCEPTANCE_RECORD.md).

## Identity and pointer

| Item | Value |
|---|---|
| Accepted version | `_DAG/DAG-003/`, accepted 2026-09-29 (DECISION-4 of run `APP-V4-SCA002-20260929`), covering project-dag checkpoints 1 and 2 |
| Pointer | `_DAG/_LATEST.md`, in SPEC §11.2 form: `Latest: DAG-003` |
| Supersedes | DAG-002, kept unchanged as history in `_DAG/DAG-002/`; DAG-001 likewise in `_DAG/DAG-001/` |
| Change event | SCA-V4-002 (accepted at DECISION-2 and DECISION-3), applied by `scope-of-work` REVISE to 9 SoWs and `dependency-extract` UPDATE of 11 registers; departure reported by `CURRENCY_APP_V4_SCA002_2026-09-29_2057` |
| Basis | commit `8cd783d8d7493fbfe663fb108449e4ceda04a00b`; [SOURCE_MANIFEST.sha256](SOURCE_MANIFEST.sha256) (130 entries, the same paths as DAG-001 and DAG-002) |
| Inventory | GROUP3-20260928T001055Z `canonical/Deliverables.csv`, through `_Decomposition/checkpoint_snapshots/_LATEST_ACCEPTED.md` (its bytes carry the B-06a reading-rule note; it names the same snapshot). 41 nodes, no exemptions |
| Integrity | [MANIFEST.sha256](MANIFEST.sha256); check it from this folder |
| Case home | `_DAG/cases/` |

## Objective, semantics, direction and completeness

- **Objective:** production-order and route-selection relationships within the App v4 project. It is not a cross-project graph and not a schedule.
- **Edge semantics:** the consumer requires the supplier's stated contribution, at the stated maturity or condition, before the stated part of its own work. An edge does not mean whole-deliverable completion.
- **Direction:** consumer → supplier. `UPSTREAM` rows read From → Target and `DOWNSTREAM` rows read Target → From.
- **Completeness:** `FULL` for the selected semantics, under `FULL_GRAPH` tracking, with the unresolved-input and candidate qualifications carried from DAG-001 through DAG-002.
- **Layers:** 124 admitted arcs ([DependencyEdges.csv](DependencyEdges.csv)), the same arc set and representative rows as DAG-002; 78 held, non-gating candidate arcs in six SCCs ([CandidateEdges.csv](CandidateEdges.csv)); 263 exclusions ([ExcludedRows.csv](ExcludedRows.csv)).

## Reading rule

1. **Blockers.** Dependency blockers come only from the admitted edges of the accepted, current version.
2. **Contributions and satisfaction.** Required contributions and their satisfaction are read from the live local `Dependencies.csv` and `_DEPENDENCIES.md`. That includes rows this version lists as `MIRROR` or `SAME_ARC`, and the non-topological inputs. The graph promotes no `SatisfactionStatus` or `RequiredMaturity`. `INITIALIZED` means only that a contract is defined.
3. **Candidate edges** are held and non-gating. They drive no blocker queue, wave, schedule, dispatch readiness or readiness claim, and holding one makes no work ready.
4. **`DAG pending`.** A deliverable the latest currency audit lists as `DAG pending` gets no ready or blocked verdict from dependencies until the owner decides its departure. Report the departure and the decision awaited instead.
5. **Scope of an edge.** A missing input constrains the stated part of the work that needs it, not the whole deliverable and not every member of an SCC.

## The 5 released deliverables

The acceptance of DAG-003 decided the departure that made these `DAG pending` under DAG-002 (`CURRENCY_APP_V4_SCA002_2026-09-29_2057`). They are released, and read their blockers from DAG-003's admitted layer, which is DAG-002's:

DEL-01-04, DEL-02-01, DEL-02-03, DEL-03-02 and DEL-03-03.

**No verdict changed on release.** All five are members of SCC-002, the four arcs they gained are held there, and no admitted arc was added or removed. Their blockers are what they were under DAG-002.

## The four new held arcs, and X-1's narrow scope

| Arc | Consumer → supplier | Representative | What the consumer waits for |
|---|---|---|---|
| N-18 | DEL-02-01 → DEL-03-02 | DEP-02-01-029 | DEL-03-02's change-item content identities, per-item dispositions, all-items-decided indication, item-left events and applied-outcome object identities, for checkpoint subject binding and item-level decisions. Reciprocal with N-B3 (DEP-03-02-027): two arcs carrying different contributions, not a mirror |
| N-21 | DEL-02-03 → DEL-03-02 | DEP-02-03-025 | The same DEL-03-02 outputs plus applied outcomes with their resulting objects, for checkpoint recording and interrupted or replayed history |
| N-24 | DEL-02-03 → DEL-03-03 | DEP-02-03-026 | DEL-03-03's observations of checkpoint arrivals and act records on the external channel, which DEL-02-03 records. Reciprocal with N-27 (DEP-03-03-014); likewise two arcs |
| X-1 | DEL-02-03 → DEL-01-04 | DEP-02-03-027 | DEL-01-04's App act control and person identity |

**Standing note: X-1 is narrow.** It applies only to DEL-02-03's App-side positive capture fixtures (OUT-003, VER-003), which wait for DEL-01-04, a later undertaking; EXEC §5 already marks them AWAITING INPUT on that account. It is not a whole-deliverable wait: the rest of DEL-02-03 is not constrained by X-1, and holding the arc does not make the fixtures ready. Read the row's Statement and Notes for the scope.

All four are `SCC_UNRESOLVED` inside the unchanged SCC-002 and cite SCC-CASE-002, which gained them as evidence only (datasheet section "Successor observation, 2026-09-29 (DAG-003 candidate; evidence update only)"). Their contributions are live obligations, read from the registers.

## Standing note: DEL-01-01 as supplier (C2-3, carried from DAG-002)

DEL-01-01 (Stock Codex hosting and supplier contract) is an admitted supplier to six deliverables through the arcs DAG-002 admitted, unchanged here:

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
- **Guard.** A reverse row in which DEL-01-01 consumes one of its consumers would merge SCCs. ARC_ANALYSIS §4.2 tested three such citations, K-3, K-4 and K-5, and each merges SCC-001, SCC-002 and SCC-003 into 19 members. None is in any register. If one appears, it is an SCC-forming departure.

## Standing note: the DEL-09-06 reverse-arc guard (C2-4, carried from DAG-002)

DEL-09-06 is an admitted consumer of eight deliverables: DEL-01-01, DEL-02-01, DEL-02-02, DEL-03-01, DEL-03-02, DEL-03-03, DEL-04-01 and DEL-04-02 (N-C5, N-19, N-C1, N-C2, N-C3, N-C4, N-28, N-08). The guard held through SCA-V4-002: no reverse row appeared, and no SCC-002 member consumes DEL-09-06 (`Evidence/DepartureAccount.json`).

**DEL-09-06 stays outside SCC-002 only while no reverse arc exists.** Across both layers of DAG-003, recomputed at publication:

- it reaches 20 deliverables: DEL-01-01…01-06, DEL-02-01…02-04, DEL-03-01…03-03, DEL-04-01…04-03, DEL-05-01, DEL-05-02, DEL-09-01 and DEL-09-09;
- it is consumed only by DEL-03-04 (N-B10) and DEL-09-07 (DEP-09-07-011).

A new ACTIVE row forms a cycle if it:

- makes any of those 20 deliverables consume DEL-09-06, or consume a deliverable that consumes it; or
- makes DEL-09-06 consume DEL-03-04, DEL-09-07, or anything that consumes them.

Such a row is an **SCC-forming departure**. It must be decided by the owner and routed to `scc-resolution-case`, not absorbed into the graph.

These reverse citations were tested in ARC_ANALYSIS §4.1–4.2 and are in no register today:

| Label | Row it would take | Effect |
|---|---|---|
| E-1 | DEL-09-09 → DEL-09-06 | SCC-002 grows to 14 |
| K-11 | DEL-03-03 → DEL-09-06 | SCC-002 grows to 14 |
| E-5 | DEL-09-06 → DEL-03-04 | New SCC {03-04, 09-06} |
| K-7 | DEL-09-06 → DEL-09-07 | New SCC {09-06, 09-07} |

K-6 (DEL-09-06 → DEL-09-09) was tested to form no SCC, but it would still be an added-arc departure.

## Candidate edges held, and the work lacking their inputs

All 78 held arcs are `SCC_UNRESOLVED` and cite their case. No case opened or closed with DAG-003. Details are in `GRAPH_BASIS.md` §Candidate layer and each case datasheet.

| SCC | Case | Members | Held arcs | Work lacking input |
|---|---|---:|---:|---|
| SCC-001 | SCC-CASE-001 | 2 | 2 | DEL-01-01 ↔ DEL-01-05. The work that needs the selected pin/protocol and the embedding contribution |
| SCC-002 | SCC-CASE-002 (CASE-004 as history) | 13 | 66 (62 in DAG-002, plus the 4 new held arcs) | Definition proceeds on provisional versions. Each dependent part that needs a named contribution waits for it at its stated maturity. New with DAG-003: DEL-02-01's checkpoint subject binding and DEL-02-03's checkpoint recording wait for DEL-03-02's dispositions and identities (N-18, N-21); DEL-02-03's external-channel recording waits for DEL-03-03's observations (N-24); DEL-02-03's App-side positive capture fixtures wait for DEL-01-04's act control (X-1). Carried: DEL-04-02's display of network-destination grants waits for DEL-05-01 (R8-A), and DEL-04-03's R15 events wait for DEL-05-01 (R8-B) |
| SCC-003 | SCC-CASE-003 | 2 | 2 | Unchanged from DAG-001 |
| SCC-004 | SCC-CASE-005 | 3 | 4 | Unchanged from DAG-001 |
| SCC-005 | SCC-CASE-006 | 2 | 2 | Unchanged from DAG-001 |
| SCC-006 | SCC-CASE-007 | 2 | 2 | Unchanged from DAG-001 |

SCC-002's 13 members are DEL-01-04, DEL-02-01, DEL-02-02, DEL-02-03, DEL-02-04, DEL-03-01, DEL-03-02, DEL-03-03, DEL-04-02, DEL-04-03, DEL-05-01, DEL-05-02 and DEL-09-09.

## Exclusions still relevant to readiness

- **NOT_TOPOLOGICAL (207):** 149 EXTERNAL, 26 DOCUMENT, 18 PACKAGE and 14 UNKNOWN rows. They are not graph arcs, but they remain inputs at their own points of need; see [Evidence/NonTopologicalInputs.csv](Evidence/NonTopologicalInputs.csv). One EXTERNAL row was retired since DAG-002 (DEP-01-04-014, an OI-002 constraint, `source_revised`; successor DEP-01-04-011); none was added.
- **MIRROR (54) and SAME_ARC (2):** each names its arc's representative. Each keeps its own obligation, read from the live register; see [Evidence/MirrorAssessment.md](Evidence/MirrorAssessment.md), which also lists the 17 comparisons whose evidence text was re-quoted under SCA-V4-002.
- **Two mirror maturity differences,** unchanged from DAG-002:
  - DEL-03-03 → DEL-04-01: DEP-03-03-008 says TBD and DEP-04-01-023 says INITIALIZED;
  - DEL-09-06 → DEL-04-03: DEP-09-06-015 says TBD and DEP-04-03-031 says INITIALIZED.

  Until the register owners reconcile them, read both rows.

## Advice: renewed examination (carried from DAG-002)

The four arcs added by DAG-003 are held inside SCC-002, so they gate nothing and no route through an admitted arc changed. **No renewed examination is called for on account of DAG-003.** DAG-002's advice list stands unchanged for the deliverables that consume, or lie on a route to, a deliverable that gained admitted inputs at DAG-002; re-examine their routes when they next rely on those inputs:

- DEL-09-07 (consumes DEL-09-06);
- DEL-10-03 (consumes DEL-02-01, DEL-02-03, DEL-03-01, DEL-03-02, DEL-04-03, DEL-05-01 and DEL-05-02);
- DEL-09-02 (consumes DEL-02-01, DEL-02-03 and DEL-04-03);
- DEL-01-04, DEL-06-01, DEL-06-02, DEL-09-05 and DEL-09-11 (consume DEL-04-03);
- DEL-02-04 and DEL-08-02 (consume DEL-02-01);
- DEL-08-01 (consumes DEL-05-01);
- DEL-01-02 and DEL-01-03 (on the route to DEL-01-01, which gained six admitted consumers).

**Coordination concentrations.** These are not defects (degree counted across both layers):

- DEL-04-03 has degree 27;
- DEL-02-03 has degree 23 (up from 20 or more at DAG-002, from the three held arcs);
- DEL-04-01 has 20 admitted dependents and no suppliers;
- DEL-02-01 is newly at the hub threshold, degree 20, from the held arc N-18.

## Open matters (C2-5), with owners

Closed since DAG-002 and dropped from this list: V12 F1 (the 34 evidence quotes that dropped inline-code backticks are now exact, 820/820 in the DX sweep; ASC-ISS-008) and the pointer form (DAG-002 published the §11.2 pointer, which the registered analyzer reads).

| Matter | Owner and route |
|---|---|
| **OI-001/OI-002 constraint rows (V12 F8; count corrected per V15 O-1).** They are ACTIVE in seven registers: DEL-04-01, DEL-04-02, DEL-04-03 (as one combined row, DEP-04-03-019), DEL-06-02, DEL-09-02, DEL-09-06 and DEL-09-07; RETIRED in DEL-02-03 and DEL-05-02; and split in DEL-01-04 (the OI-001 row DEP-01-04-013 kept and narrowed to uncovered matters; the OI-002 row DEP-01-04-014 retired). `Open_Issues.csv` keeps OI-001 and OI-002 OPEN (DECISION-2, option A). Off-arc; a consistency point | Register owners, through `dependency-extract` |
| The two mirror maturity differences listed under exclusions | Both register owners, through `dependency-extract` |
| **SatisfactionStatus TBD/PENDING convention (P2 O-6).** The four new rows use PENDING (1) and TBD (3), so the inconsistency persists | Register owners |
| **V12 F6 (advice).** N-05 and N-07 rest on the supplier's statement only; ARC_EFFECT §5 left consumer-side wording out of SCA-V4-002 as outside its decided scope. Both arcs are held in SCC-002; no arc would change | Advice only; a later SoW amendment if the owner wants it |
| The RS §10 DEL-03-02 cell and the ADAPTER header wording behind N-12/N-B8. Both arcs are absent by decision (predecessor DECISION-6) | DEL-04-03 and DEL-03-03 owners |
| Deferred supplier-side mirror rows (P2 O-3) | Register owners |
| **`Coverage_Telemetry.json` is stale** (STALE_REBUILD_REQUIRED; carried from SCA-V4-001). The SCA-V4-001 closure verdict stays OPEN_PENDING_DERIVATIVE_CLOSURE for that derivative | Decomposition owner, by a later bounded brief |
| **The 17 Design re-pins** (carried from SCA-V4-001). `APP-V4-BASIS-ALIGN-20260928` DECISION-8 is their deferral record, confirmed at SCA-V4-002 DECISION-2. No graph arc rests on a Design file; the DX returns used Design files as corroboration only | Owner, separately governed; not a graph matter |
| **SCA-V4-002 `audit-scope-closure` pending** (step 5 of the owner's accepted order), and the superseding `audit-scope-closure` snapshot for SCA-V4-001 recording ASC-ISS-001 closed. `_ScopeChange/_LATEST.md` reads `Closure: OPEN_PENDING_DERIVATIVE_CLOSURE` until then. This accepted graph is the derivative package that audit needs; it does not itself close either amendment | `scope-change`, after this publication |
| **V15 O-2.** The inherited `audit-decomp` base script's active-snapshot heuristic misreads a §11.2 pointer under `ACCEPTED_PREDECESSOR` posture; `POSTACCEPT/` worked around it with disclosed adjustments | The next `audit-decomp` script generation; to be noted in the SCA-V4-002 closure-audit brief. Nothing further for the graph |
| Unknowns stay `TBD` in the registers: RequiredMaturity on 214 rows and SatisfactionStatus on 304 | Register owners, as work proceeds |

## Currency

**Latest result.** `_Evaluation/DAGCurrency/_LATEST.md` locates the latest currency audit. The follow-up audit after this acceptance is expected to report `CURRENT` with nothing `DAG pending`. The audit of 2026-09-29_2057 is against DAG-002 and is historical.

**Commands.** Run the first from this folder and the second from the execution root, `projects/chirality-app-v4/execution`:

```text
shasum -a 256 -c MANIFEST.sha256
shasum -a 256 -c _DAG/DAG-003/SOURCE_MANIFEST.sha256
```

Then check that `_Decomposition/checkpoint_snapshots/_LATEST_ACCEPTED.md` still names GROUP3-20260928T001055Z. If any source failed, re-apply the accepted selection rules as a scratch assembly and compare the arc sets, the SCCs and the inventory (`workflows/project-dag/resources/currency.md`).

**Cross-check.** The registered closure analyzer, run from the repository root, reads the §11.2 pointer:

```text
python3 tools/coordination/analyze_dep_closure.py projects/chirality-app-v4/execution --scope ALL --filter-active-only true --normalize-ids true --dependency-class EXECUTION --target-type DELIVERABLE --hub-threshold 20 --max-cycles 200 --include-declared true
```

Its `accepted_dag` section reports the comparison.

**When to audit:**

- before relying on DAG-003 for a route or a blocker verdict when the local files may have changed since its basis or since the latest audit;
- after `dependency-extract` runs on any in-scope deliverable, or after a human changes declarations;
- after an accepted scope change or decomposition revision;
- when a consumer finds the graph and a local file disagree;
- after the owner decides a departure.

A new session is not, by itself, a reason to rebuild. The SCA-V4-002 and SCA-V4-001 closure audits read this version; they do not change its sources, so they are not, by themselves, a reason to audit.
