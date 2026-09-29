# SUCCESSOR_PLAN: DAG-002 by project-dag TRIGGER=SUCCESSOR (node P2)

- **Run and node:** `APP-V4-BASIS-ALIGN-20260928`, node P2. This is preparation only; nothing here has been run against a governed file.
- **Basis:** commit `874508f16`.
- **Method:** `chirality-root:bundled:workflow:project-dag`, using `method.md` Stages 0–5 and `currency.md`.
- **Work-graph nodes served:**
  - K1: owner checkpoint A, including project-dag checkpoint 1 limited to the reopened decisions;
  - A*: the register application;
  - D1: the currency audit, candidate, audit and review;
  - K2: owner checkpoint B, which is project-dag checkpoint 2;
  - F: publication.
- **Companions:** [REGISTER_CHANGES.md](REGISTER_CHANGES.md) and [ARC_ANALYSIS.md](ARC_ANALYSIS.md).

## 1. Expected currency-audit result after the register changes: DEPARTURE

**Now.** DAG-001 is **CURRENT**:
- the snapshot and source manifests pass;
- the latest observation is `_Evaluation/DAGCurrency/CURRENCY_APP_V4_ACCEPTANCE_2026-09-28/CURRENCY_REPORT.md`;
- the 130 files in `SOURCE_MANIFEST.sha256` are unchanged at `874508f16`.

**After A\*.** Once `scope-of-work` REVISE and `dependency-extract` have applied the accepted changes, the audit will find the following.

**1. Manifest check.** `shasum -a 256 -c _DAG/DAG-001/SOURCE_MANIFEST.sha256`, run from the execution root, fails for:
- each revised `ScopeOfWork.md`;
- each changed `Dependencies.csv` and `_DEPENDENCIES.md`. These are the 13 registers with added rows, plus DEL-01-01, whose rows are edited in place.

The basis documents (PRD, ARCHITECTURE, HOST_INTEGRATION, EXAMINATION) are not in the manifest, so their wording updates do not affect DAG currency on their own.

**2. Scratch re-application of SR-1…SR-7:**

| Comparison | Result |
|---|---|
| Admitted and candidate arcs | **41 arcs added**, or 32 if only the grounded rows are applied; **0 removed** |
| SCCs | **Unchanged**: the same six member sets, and cases 001 and 003–007 untouched |
| Node inventory | **Unchanged**: GROUP3-20260928T001055Z, 41 nodes, since P1 changes no decomposition register |
| Evidence drift alongside | 14 mirror rows; 4 changed SR-6 representatives; 10 or 11 EXTERNAL rows; 23 row edits; SoW text |

**3. Classification: `DEPARTURE`.** Arcs are added. Drift alone would have been `CURRENT_WITH_EVIDENCE_DRIFT`.

**4. `DAG pending` deliverables.** These are the endpoints of the added arcs. There are 16, and the set is the same with or without the 9 P1-dependent arcs:

| | Deliverables |
|---|---|
| **First increment (14)** | DEL-01-01, DEL-02-01, DEL-02-03, DEL-03-01, DEL-03-02, DEL-03-03, DEL-03-04, DEL-04-01, DEL-04-02, DEL-04-03, DEL-05-01, DEL-05-02, DEL-09-06, DEL-09-09 |
| **Outside the first increment (2)** | DEL-01-04, through X-1 (SC-02-03-4), and DEL-02-02, through N-C1 (S9-6-3) |

The two outside deliverables become pending only because of those two SoW sentences. If the owner prefers them not to be (O-5), P1 moves the SC-02-03-4 DEL-01-04 clause to REQ-006, and C1-C's option to defer the DEL-02-02 row is taken.

The audit may also name, as advice only (`currency.md`), work whose route runs through a changed arc. Examples are DEL-09-07, which consumes DEL-09-06, and DEL-01-02 and DEL-01-03, which reach DEL-01-01. These are not `DAG pending`.

**This was previewed in scratch.** The proposed rows were appended to a scratch copy of the execution root, and the registered `tools/coordination/analyze_dep_closure.py` (sha256 `2b8de3cb…a9adc`) was run with DAG-001's closure arguments:

| Variant | Result | Arcs added | Arcs removed | `DAG pending` | SCCs |
|---|---|---:|---:|---:|---|
| All 69 proposed rows | **DEPARTURE** | 41 | 0 | 16 (list above) | unchanged, 2/13/2/3/2/2 |
| The 59 grounded rows | **DEPARTURE** | 32 | 0 | the same 16 | unchanged, 2/13/2/3/2/2 |
| The unchanged registers | NO_DEPARTURE_FOUND | — | — | — | — |

The preview outputs are in `evidence/currency_preview.json`.

**Finding: DAG-001's accepted pointer cannot be read by the tool.**
- `_DAG/_LATEST.md` is prose. It has no `Latest:` line in the `docs/SPEC.md` §11.2 and `contract.md` pointer form.
- The tool's accepted-DAG comparison therefore returns `INCOMPLETE` ("no `Latest:` line naming a version") against the live tree.
- The preview above used a §11.2-form pointer written **in scratch only**.

**Consequences:**
- **Fix it at publication.** F should write the DAG-002 pointer in §11.2 form: `Latest`, `Updated`, `Acceptance`, `Completeness`, `Basis revision` and `Supersedes: DAG-001`. The human-readable lines can follow.
- **Until then**, the D1 currency audit relies on the project-dag scratch re-application (`currency.md` step 4), not on the tool's pointer read.
- **Or** the recorder rewrites the DAG-001 pointer's header now. That is a separate, small act for the owner or integrator (C2-6).

**Timing.** Run **one** currency audit after every A\* brief has returned and its row set has been compared with REGISTER_CHANGES. An audit taken while only SoWs have changed would report `CURRENT_WITH_EVIDENCE_DRIFT`, and that interim state has no `DAG pending` set. From the first register write until K2, the 16 deliverables get no ready or blocked verdict from dependencies (SPEC §5.4). Unaffected work keeps DAG-001.

## 2. TRIGGER=SUCCESSOR steps

| Step | project-dag stage | Work-graph node | Actor (by the workflows) | Write target | Output |
|---|---|---|---|---|---|
| 0 | Stage 0: precondition and trigger | D1 | TASK under WORKING_ITEMS (here, HELP_HUMAN under the recorded consultation) | none | FULL_GRAPH confirmed from `_COORDINATION.md`. Accepted decomposition GROUP3 confirmed through `_Decomposition/checkpoint_snapshots/_LATEST_ACCEPTED.md`. Accepted DAG-001. No open candidate. Latest currency audit found |
| 1 | Currency audit (`currency.md`) | D1 | TASK | `_Evaluation/DAGCurrency/` | `SNAP=$(tools/scaffolding/create_snapshot_folder.sh projects/chirality-app-v4/execution/_Evaluation/DAGCurrency CURRENCY APP_V4_BASISALIGN)`. Then `CURRENCY_REPORT.md`, `Tool_Run.json`, the manifest-check outputs and the scratch re-application in `Evidence/`. Result `DEPARTURE` with the 16 pending deliverables. `_Evaluation/DAGCurrency/_LATEST.md` moves |
| 2 | Stage 1: frozen inventory and objective | D1 | TASK | `_DAG/_Candidates/DAG-002/` | Open `DAG-002`, the next unused number. Record the predecessor DAG-001, the trigger `SUCCESSOR` and the currency report. `DeliverableNodes.csv` is re-derived from GROUP3 and expected to be byte-equal to DAG-001's |
| 3 | Stage 2: freeze and closure | D1 | TASK + `audit-dep-closure` | `_Evaluation/DepClosure/` (its own `_LATEST.md`), and `SOURCE_MANIFEST.sha256` in the candidate | Freeze the basis: record the Git revision after A\*, and write the manifest over the same file classes as DAG-001 (130 files plus any added). Run `python3 tools/coordination/analyze_dep_closure.py projects/chirality-app-v4/execution --output-dir <SNAP>/Evidence --scope ALL --filter-active-only true --normalize-ids true --dependency-class EXECUTION --target-type DELIVERABLE --hub-threshold 20 --max-cycles 200 --include-declared true --prior-summary <CLOSURE_APP_V4_TARGETS_2026-09-27_2237 closure_summary.json>` (DAG-001's arguments). Expect 6 SCCs and no coverage defect. Route any coverage defect to `dependency-extract` and re-freeze |
| 4 | Checkpoint 1 (reopened decisions only) | **K1**, before A\* | Owner | decision record in the run folder | §4 below. The decisions are made at K1 so that A\* applies the ruled row set. Stage 2 then re-freezes on the applied files |
| 5 | Stage 3: coupled work | D1 | TASK + `scc-resolution-case` | `_DAG/cases/SCC-CASE-002/` only | Update CASE-002 with the 26 (or 18) new held arcs inside its unchanged 13-member set: evidence rows only, no ruling, no closure claim. No case opens or closes. Cases 001 and 003–007 carry forward |
| 6 | Stage 4: assemble | D1 | TASK (assembler) | `_DAG/_Candidates/DAG-002/` | The files in §5, the `audit_dag.py` runs in §6 and accounting. The assembler may reuse `DAG-001/Evidence/assemble_graph.py`, retargeted to DAG-002 and preserved with its hash |
| 7 | Independent review | D1 | A separate TASK instance | `_DAG/_Candidates/DAG-002/INDEPENDENT_REVIEW.md` | §7 below |
| 8 | Review packet | D1 | WORKING_ITEMS / integrator | `REVIEW_PACKET.md` | SHA-256 of every presented graph file |
| 9 | Checkpoint 2 | **K2** | Owner | — | §8 below |
| 10 | Stage 5: publish | **F** | WORKING_ITEMS / integrator | `_DAG/DAG-002/` and `_DAG/_LATEST.md` | Copy the presented bytes. Add `ACCEPTANCE_RECORD.md`, `HANDOFF_STATE.md` and `MANIFEST.sha256`. Move the pointer in §11.2 form, naming DAG-001 as superseded |
| 11 | Follow-up currency audit | F | TASK | `_Evaluation/DAGCurrency/` | `CURRENT` against DAG-002. This clears the 16 `DAG pending` flags |

If the owner **rejects** the change at K2 instead:
- write `_DAG/_Candidates/DAG-002/REJECTION_RECORD.md`;
- DAG-001 stands;
- the departing rows go back to `dependency-extract` for extracted rows, or to the owner for declarations;
- run a follow-up currency audit.

## 3. Carried forward unchanged (not re-decided)

These stand from DAG-001 (`BASIS_DECISION.md` DECISION-1; `GRAPH_BASIS.md`; `ACCEPTANCE_RECORD.md`). The successor departure does not touch their rows, arcs or warrants.

- **Objective:** production-order and route-selection relationships in this App project. It is neither a cross-project graph nor a schedule.
- **Edge semantics:** the consumer requires the supplier's stated contribution, at the stated maturity or condition, before the stated part of its work.
- **Direction:** consumer → supplier. Source Direction is preserved.
- **Tracking and completeness:** FULL_GRAPH, with Completeness **FULL for the selected semantics**, carrying the explicit unresolved-input and candidate qualifications.
- **Inventory:** the GROUP3 register, 41 nodes in 11 packages, no exemptions.
- **Case home:** `_DAG/cases/`.
- **Selection rules:**
  - SR-1…SR-7 as confirmed;
  - all canonical DependencyTypes admitted (SR-3);
  - no cut or merge ruling (SR-4);
  - no confirmation hold (SR-5);
  - consumer UPSTREAM first, then DECLARED, then the lowest ID (SR-6);
  - every intra-SCC representative held (SR-7).
- **SCC tracking:** six characterized groups. CASE-002 covers SCC-002 (13 members), and CASE-004 is kept as constituent history. Cases 001, 003, 005, 006 and 007 are unchanged. No case is closed.
- **Maturity:** `INITIALIZED` means defined-contract maturity only. SatisfactionStatus is never promoted by the graph.
- **Reliance boundary:** unchanged in kind. Acceptance satisfies no dependency, advances no lifecycle, lifts no hold and releases nothing.
- **Standing tool strictness:** `audit_dag.py --canonical --strict` must exit 0, with no strictness exception.

## 4. Reopened decisions for checkpoint 1 (presented at K1)

Each item has a recommendation. The items marked **(DAG)** reopen a project-dag basis decision. The others decide which rows A\* writes.

| # | Decision | Recommendation |
|---|---|---|
| **O-1 (DAG)** | Accept the refreshed arc set as the successor's departure scope. That is the 38 kept C1 arcs (6 with Statements amended for R8-1) and the additions R8-A, R8-B and X-1, with N-12 and N-B8 dropped (ARC_ANALYSIS §2) | **Accept.** SCC-neutral in every variant (ARC_ANALYSIS §4) |
| **O-2** | **Grounding route** for the 9 arcs with no SoW sentence: N-11, N-17, N-20, N-22, N-27, N-B3, N-B4, R8-A and R8-B. The choices are (a) P1 adds consumption sentences (see the hooks in ARC_ANALYSIS §2.3), (b) the owner declares them in `_DEPENDENCIES.md`, or (c) they are left out for now | **(a).** It keeps the accepted rule ("local SoWs and accepted interfaces") and the SoW-sourced registers consistent, and needs no rule change. Allowing the DRAFT Design files as extraction sources is **not** recommended, because they carry runtime-input and citation text that would pull DEL-04-01 or DEL-09-06 into SCC-002 (K-1, K-2, K-11) |
| **O-3** | **Optional rows that no SoW grounds:** 33 mirror rows (5 of them in registers outside the first increment), plus 17 optional rows on new arcs (14 supplier-side, 3 consumer-side) | **Defer.** They add no arc and no obligation, since the consumer rows carry them. The reviewer requests stay open with the register owners |
| **O-4 (DAG)** | The **disputed arc N-12** (DEL-03-02 → DEL-04-03), with N-B8 (DEL-03-03 → DEL-04-03) treated the same way | **Not proposed** (ARC_ANALYSIS §3). The RS §10 and ADAPTER header wording goes to the owners as findings |
| **O-5** | **Conditional arcs:** (i) N-15 as a direct DEL-04-03 → DEL-01-01 arc, not riding DEL-01-02; (ii) N-25 by S5-2-3's main option, not "via DEL-05-01"; (iii) SC-04-02-2's direct-consumption option for N-01, N-02 and N-05…N-07; (iv) X-1 and N-C1, which make DEL-01-04 and DEL-02-02 `DAG pending` | (i) Keep; RS §10 names HOSTING §8.3 directly, and DEL-01-02 is outside D1. (ii) Main option. (iii) Direct; all four designs consume directly. (iv) Keep both; they are evidenced (EXEC §9.1; CA §11.1), and pending only lasts until K2 |
| **O-6** | SatisfactionStatus convention (`TBD` against `PENDING`; V1-B RF-09) | **Defer.** Both values are valid, there is no DAG effect, and the register owner can decide later |
| **O-7 (DAG)** | CASE-002: continue the confirmed tracking, with the new held arcs added to the same 13-member group | **Confirm.** Record the added arcs as evidence (step 5). No ruling is needed |
| **O-8 (DAG)** | Confirm that the five SCC-enlarging arcs (E-1…E-5) and the reverse citations K-1…K-5, K-7 and K-11 stay out of the registers. K-1 is new with R8-13 | **Confirm.** Guard them in the A\* briefs |
| **O-9** | Lifecycle recording (IN_PROGRESS for the 14), carried into "as recommended" | Separate from the DAG. Its handling belongs to K1 on P1's side. Recording it moves no DAG-bound file other than `_STATUS.md`, which is not in the manifest |

## 5. Files DAG-002 needs (`_DAG/_Candidates/DAG-002/`)

These follow `graph-version.md` "Files" and DAG-001's layout.

| File | Content and notes |
|---|---|
| `GRAPH_BASIS.md` | The identity (DAG-002, SUCCESSOR, predecessor DAG-001), the currency report and the departures it decides. The objective and rules as carried forward (§3). The K1 decision references. Rulings: none new, plus the N-12/N-B8 withholding recorded as a register-level ruling, not an SR-4 cut. The candidate-layer summary, exclusions, findings routed, limitations and reproduction |
| `DeliverableNodes.csv` | 41 rows, from GROUP3; expected byte-equal to DAG-001 |
| `DependencyEdges.csv` | Expected 124 admitted rows (123 if only grounded), in 29 core columns plus `SourceRegister`, `SourceRegisterSHA256`, `SourceRecord` and `SelectionRule` |
| `CandidateEdges.csv` | Expected 78 (or 70) rows, with `CandidateReason=SCC_UNRESOLVED`, `SCCRef` and `CaseRef` (the new SCC-002 rows cite `_DAG/cases/SCC-CASE-002`) |
| `ExcludedRows.csv` | Every other ACTIVE EXECUTION row: NOT_TOPOLOGICAL, MIRROR and SAME_ARC with `RepresentedBy` |
| `SOURCE_MANIFEST.sha256` | Every in-scope `Dependencies.csv`, `_DEPENDENCIES.md` and `ScopeOfWork.md`, and the GROUP3 registers, at the frozen revision |
| `SOURCE_BASIS.json` | The Git revision, the manifest hash, the closure snapshot and its input basis, case paths and states, tool paths and hashes, and the parent run and decision records |
| `Evidence/` | `admissible_edges.csv`, `admissible_audit.json`, `dag_audit.json`, `candidate_audit.json`, `Tool_Run.json`, `Accounting.md` (per-register balance of ACTIVE EXECUTION rows = admitted + candidate + excluded), `SCC_Accounting.json`, `MirrorAssessment` (re-run, including the 4 changed representatives), `NonTopologicalInputs.csv`, the assembly script with its hash, and optionally `TopologicalOrder.md` |
| `REVIEW_PACKET.md` | What checkpoint 2 decides, and the hashes of the presented files |
| `INDEPENDENT_REVIEW.md` | From the separate reviewer (§7) |
| Added at F | `ACCEPTANCE_RECORD.md`, `HANDOFF_STATE.md` (the reading rule, the 16 formerly pending deliverables, and advice on renewed examination) and `MANIFEST.sha256` |

Outside the candidate folder:
- the currency snapshot, with `_Evaluation/DAGCurrency/_LATEST.md`;
- the closure snapshot, with `_Evaluation/DepClosure/_LATEST.md`;
- the CASE-002 evidence update;
- at F, `_DAG/_LATEST.md` in §11.2 form.

## 6. The `audit_dag.py` invocation

- **Tool:** `tools/coordination/audit_dag.py`, sha256 `830d0d5390094c12922ab5330e8f512de671a1422f377f32bd4ae7797723449a`. This is the same bytes DAG-001 used (`DAG-001/SOURCE_BASIS.json`); last changed in `8fbe5cd7b`.
- **Run from:** the repository root. Paths are relative to the worktree.

```text
# 1. SCCs on the admissible set (no --strict)
python3 tools/coordination/audit_dag.py \
  --edges projects/chirality-app-v4/execution/_DAG/_Candidates/DAG-002/Evidence/admissible_edges.csv \
  --nodes projects/chirality-app-v4/execution/_DAG/_Candidates/DAG-002/DeliverableNodes.csv \
  --canonical --json-out projects/chirality-app-v4/execution/_DAG/_Candidates/DAG-002/Evidence/admissible_audit.json

# 2. Acceptance check on the admitted layer (exit 0 required)
python3 tools/coordination/audit_dag.py \
  --dag-dir projects/chirality-app-v4/execution/_DAG/_Candidates/DAG-002 \
  --canonical --strict \
  --json-out projects/chirality-app-v4/execution/_DAG/_Candidates/DAG-002/Evidence/dag_audit.json

# 3. Optional evidence on the candidate layer (no --strict)
python3 tools/coordination/audit_dag.py \
  --edges projects/chirality-app-v4/execution/_DAG/_Candidates/DAG-002/CandidateEdges.csv \
  --nodes projects/chirality-app-v4/execution/_DAG/_Candidates/DAG-002/DeliverableNodes.csv \
  --canonical --json-out projects/chirality-app-v4/execution/_DAG/_Candidates/DAG-002/Evidence/candidate_audit.json
```

- **Record every run in `Evidence/Tool_Run.json`:** the tool path and hash, the arguments, the exit code, `run_status` and `subject_status`.
- **Do not publish** `--markdown-out` output.
- **Manifest check:** on macOS, use `shasum -a 256 -c`, as DAG-001's `HANDOFF_STATE.md` does, where the method text says `sha256sum -c`.
- **The strict run will need** Explicitness, SatisfactionStatus and Confidence to be non-blank on every new row. The proposed rows supply `EXPLICIT`, `PENDING`/`TBD` and `HIGH` (REGISTER_CHANGES §3).

## 7. Independent-review brief outline (a separate TASK; it did not assemble)

- **Inputs:**
  - the candidate folder;
  - the confirmed basis (§3), plus the K1 decision record;
  - the currency report;
  - the closure snapshot;
  - REGISTER_CHANGES, ARC_ANALYSIS and this plan, as the prepared expectation;
  - the graph-version rules.
- **Write boundary:** only `INDEPENDENT_REVIEW.md` and its own evidence under `_Candidates/DAG-002/Evidence/IndependentReview/`.
- **Mechanical re-runs:**
  - the source manifest check from the execution root;
  - `audit_dag.py --canonical --strict`, which must exit 0;
  - accounting balance per register, with no row in two files and none missing;
  - 29-column byte fidelity of every admitted and candidate row;
  - the SCC comparison with the closure `scc_summary.csv`, and with DAG-001 (identical membership expected).
- **Departure fidelity:** the added arcs equal the K1-accepted set (41, or as ruled) with none extra; there are 0 removed arcs; N-12 and N-B8 are absent; the E-1…E-5 and K-1…K-12 arcs are absent; X-1 and N-C1 are present or absent exactly as ruled.
- **Representatives:** SR-6 was applied to the 4 changed representatives, and each new arc's representative is the consumer row where one exists. Mirror conflicts are checked for material disagreement (type, maturity, statement) and routed.
- **Semantics:** each added arc is a consumed contribution, not a citation or an ownership statement. Check a sample of at least the 15 admitted additions against the applied SoW text and the Design corroboration.
- **Candidate layer:** every new held row cites SCC-002 and CASE-002. Name the work that lacks inputs, especially for the new admitted consumers DEL-09-06 and DEL-03-04, and for DEL-01-01 as a new admitted supplier.
- **Findings:** a finding is blocking or non-blocking, with evidence pointers. Mechanical findings return for repair. Substantive findings go to K2.

## 8. Owner items for checkpoint 2 (K2)

| # | Item | Recommendation |
|---|---|---|
| **C2-1** | **Accept DAG-002** as presented: 41 nodes, 124 (or 123) admitted and 78 (or 70) candidate arcs, 6 unchanged SCCs, and DAG-001's qualifications carried. Or accept it with stated qualifications, or return parts | **Accept**, if the strict audit exits 0 and the independent review has no unresolved blocking finding. Graph acceptance again passes no gate, satisfies no dependency and advances no lifecycle |
| **C2-2** | **Decide each departure.** Accept all the added arcs as one successor, or have any group decided separately in its own candidate. The groups could be the 15 admitted additions, the 26 held ones, or X-1 and N-C1 | **Accept as one successor.** None changes an SCC. Separate candidates would only prolong `DAG pending` for the 16 deliverables |
| **C2-3** | **The new admitted supply through DEL-01-01** (in SCC-001) to DEL-02-01, 02-03, 03-03, 03-04, 04-03 and 09-06. From DAG-002 on, their dependent parts wait for DEL-01-01's contribution at its stated maturity | **Accept, and state it in `HANDOFF_STATE`.** HOSTING-BOUNDARY-v0.6 is defined, and satisfaction is read from the live registers. SCC-001's own held arcs are unchanged |
| **C2-4** | **DEL-09-06 as a new admitted consumer** of 8 suppliers. It stays outside SCC-002 only while E-1, E-5, K-7 and K-11 stay out | **Accept, and confirm the guard as a standing note in `HANDOFF_STATE`**, so that a later extraction of the reverse citations is caught as an SCC-forming departure, not absorbed |
| **C2-5** | **Findings routed to owners, not blocking acceptance:** the RS §10 DEL-03-02 cell and the ADAPTER header (N-12/N-B8); the deferred supplier-side mirror requests (O-3); SatisfactionStatus convention (O-6); `Open_Issues.csv` OI-001/OI-002 still OPEN | **Note as open matters** in `GRAPH_BASIS` and `HANDOFF_STATE`, with their owners |
| **C2-6** | **The pointer form.** The DAG-001 `_DAG/_LATEST.md` has no §11.2 `Latest:` header, so the registered tool reads the accepted DAG as INCOMPLETE | **At F, write DAG-002's pointer in §11.2 form** (§1), with the prose below it. Whether the DAG-001 pointer text is also corrected before then is the integrator's call; it has no graph effect |
| **C2-7** | **The reliance boundary and handoff to `construct-local-work-graph`:** the 16 formerly pending deliverables are released on acceptance. Changed arcs call for renewed examination of dependent work (e.g., DEL-09-07, DEL-01-02, DEL-01-03), which is listed as advice | **Accept** the handoff as drafted by the integrator, with a follow-up currency audit recording `CURRENT` |
| **C2-8** | **Scope-change group 3** (work graph K2). This is P1's packet. Any SoW or basis change there that alters a register relationship after K1 reopens this plan's affected checks | Present it together. Re-run the scratch re-application if anything in group 3 touches a manifest-bound file |

## 9. What this preparation could not do

- **Grounding rows for the 9 arcs** (O-2). This depends on P1's SoW wording, or on the owner's declaration. REGISTER_CHANGES gives the rows and the fallback declaration text, but not the final SoW sentences. Their `SourceRef` and `EvidenceQuote` are placeholders.
- **Final `EvidenceQuote` values** for grounded rows. The expected text is C1's proposed sentence, and it must be re-quoted from the applied SoW bytes.
- **Final `DependencyID`s and dates.** They are assigned by the extraction run, and the proposed IDs assume the listed order.
- **The DAG-002 files, the closure snapshot, the currency snapshot, the CASE-002 update and the independent review.** They need the post-A\* frozen basis, and their write targets are outside this node's boundary.
- **Material-mirror assessment of the 4 changed representatives.** This is assembly work. Their type differences are noted only (ARC_ANALYSIS §5).
- **The fixed K2 counts.** They depend on O-2 and O-5; both variants are given.
