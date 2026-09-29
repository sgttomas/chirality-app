# Checkpoint C — the successor dependency graph DAG-002

- **For:** the owner. Prepared by node D1 of run `APP-V4-BASIS-ALIGN-20260928`, 2026-09-29.
- **Basis:** commit `b585e5ebe`, after all 16 SoW revisions and the 18 register updates.
- **What you are asked to decide:** whether DAG-002 replaces DAG-001 as the accepted project dependency graph.

**Before you decide.** A separate reviewer, who did not build the candidate, still has to check it (SUCCESSOR_PLAN §7). Present this page with that review and its findings. Nothing on this page accepts anything, and `_DAG/_LATEST.md` has not been moved.

**One sitting.** The method lets you settle both graph checkpoints (the basis and the acceptance) at once. The undertaking is small and no cycle needs a ruling. Most of the basis simply carries forward from DAG-001; §3 lists it so you can see it is unchanged rather than re-decided.

## 1. The short version

- The SoW revisions you accepted under SCA-V4-001 made the registers state **37 new "needs input from" relationships**. They change the graph without changing its shape:
  - 15 are ordinary sequencing arcs;
  - 22 fall inside the large cycle that CASE-002 already tracks, so they are held and do not gate anything;
  - no relationship was removed;
  - the six cycles have exactly the same members;
  - all 41 deliverables are unchanged.
- The currency check against DAG-001 therefore says `DEPARTURE`. Until you decide, **15 deliverables are "DAG pending"**: they get no ready or blocked verdict from dependencies.
- The candidate passes the strict audit (exit 0) and every row is accounted for.
- **4 of the 41 arcs you accepted at checkpoint A are missing:** N-18, N-21, N-24 and X-1. The SoWs name the other deliverable only as an owner, and extraction does not read ownership as consumption. All four would sit inside the same held cycle, so leaving them out changes no verdict.
- **Recommendation:** accept DAG-002 as the evidence produces it, and send any consumption wording for the four arcs to the follow-on amendment SCA-V4-002.

## 2. What DAG-002 changes compared with DAG-001

| | DAG-001 | DAG-002 |
|---|---:|---:|
| Deliverables (nodes) | 41 | 41, byte-identical |
| Admitted sequencing arcs | 109 | **124** (+15) |
| Held arcs inside cycles (non-gating) | 52 | **74** (+22, all in the 13-member cycle, CASE-002) |
| Arcs removed | — | 0 |
| Cycles (SCCs) | 6 | 6, same members |
| Register rows accounted for | 403 | 462, all placed exactly once |

### The 15 new admitted arcs

Read "A → B" as "A needs a contribution from B".

- **DEL-01-01 (Codex hosting) becomes a supplier** to DEL-02-01, DEL-02-03, DEL-03-03, DEL-03-04, DEL-04-03 and DEL-09-06. After acceptance, the stated parts of those deliverables wait for the hosting-boundary contribution at its stated maturity.
- **DEL-09-06 (connected activity) becomes a consumer** of 8 deliverables: DEL-01-01, DEL-02-01, DEL-02-02, DEL-03-01, DEL-03-02, DEL-03-03, DEL-04-01 and DEL-04-02.
- **DEL-03-04 (host integration guide) becomes a consumer** of DEL-01-01, DEL-09-06 and DEL-09-09.

### The 22 new held arcs

All 22 are inside the existing 13-member cycle (SCC-002, tracked by SCC-CASE-002):

- N-01…N-07, N-09, N-10, N-11, N-13, N-14;
- N-17, N-20, N-22, N-25, N-26, N-27;
- N-B3, N-C6, R8-A, R8-B.

They say, for example, that the autonomy display (DEL-04-02) takes network-destination events from the loop contract (DEL-05-01). CASE-002 now records them as evidence. No case opens or closes, and no ruling is needed.

### The 15 deliverables that are DAG pending

DEL-01-01, DEL-02-01, DEL-02-02, DEL-02-03, DEL-03-01, DEL-03-02, DEL-03-03, DEL-03-04, DEL-04-01, DEL-04-02, DEL-04-03, DEL-05-01, DEL-05-02, DEL-09-06 and DEL-09-09.

These are the 14 first-increment deliverables plus DEL-02-02 (through N-C1). Your decision here clears all 15. The per-deliverable list is in the currency report.

## 3. Carried forward from DAG-001 (not re-decided)

- **Objective and meaning.** The graph shows production order and route selection within this project. An arc means the consumer needs the supplier's stated contribution, at the stated maturity, before the stated part of its own work.
- **Direction.** Arcs run from consumer to supplier.
- **Scope.** FULL_GRAPH completeness, with the same qualifications. The same 41 deliverables, with no exemptions.
- **Selection rules.** SR-1…SR-7: all dependency types count; no cuts or merges; no confirmation hold; one representative row per arc; arcs inside a cycle are held.
- **Cases.** The six cycles are tracked in cases 001, 002 (with 004 as history), 003, 005, 006 and 007, all still gathering evidence.
- **Maturity.** "INITIALIZED" means only that a contract is defined.
- **What acceptance does not do.** It satisfies no dependency, changes no lifecycle state, lifts no hold, passes no gate and schedules nothing.

Already decided by you at checkpoint A (DECISION-6), and reflected in the evidence:

| Decision | Result |
|---|---|
| The disputed arcs N-12 and N-B8 are not proposed | They are absent |
| N-15 is kept as a direct arc | Present |
| The nine arcs are grounded by SoW sentences (route a) | All nine present |

## 4. The four accepted arcs that were not produced

| Arc | Meaning | Where it would sit |
|---|---|---|
| N-18 | DEL-02-01 (workflow contract) needs DEL-03-02 (proposal contract) | Held, inside the 13-member cycle |
| N-21 | DEL-02-03 (execution compatibility) needs DEL-03-02 | Held, same cycle |
| N-24 | DEL-02-03 needs DEL-03-03 (external-agent adapter) | Held, same cycle |
| X-1 | DEL-02-03 needs DEL-01-04 (native requests) | Held, same cycle |

**Why they are missing.** DEL-02-01's and DEL-02-03's SoWs say the other deliverable *owns* something. They do not say this deliverable *consumes* it. These two registers have always read ownership sentences as non-edges; the extraction returns quote the recorded convention. P2 had assumed the opposite for these clauses, and so did the recommendation behind your "keep X-1" answer. The graph only copies register rows. It cannot add an arc that no register states.

**What difference they make.** None to any verdict today. All four would be held arcs inside a cycle that is already held, and held arcs never gate work. No cycle changes either way.

| Option | What happens | Cost |
|---|---|---|
| **A. Accept DAG-002 as produced; send the wording to SCA-V4-002** (integrator's lean; **recommended**) | DAG-002 has 37 new arcs. SCA-V4-002 adds "consumes" sentences to the DEL-02-01 and DEL-02-03 SoWs where the consumption is real. The next extraction writes the rows, and the next currency audit reports them as a small departure for a later successor | A second, small graph decision later. Nothing is held in the meantime |
| B. Declare the four arcs yourself now, in `_DEPENDENCIES.md` | Extraction mirrors them as DECLARED rows. The freeze, closure and assembly are redone, and DAG-002 grows to 41 arcs. DEL-01-04 becomes DAG pending too | Register writes and a rebuild before you can decide. The 15 pending deliverables wait longer |
| C. Hold checkpoint C until SCA-V4-002 lands | Everything goes in one graph | The 15 deliverables stay DAG pending for the whole follow-on amendment |
| D. Drop some or all four for good | Record that they are not wanted | Only if you now judge the consumption is not real |

**Recommendation: A.** It follows your accepted rule that relationships come from the SoWs. It leaves the 15 deliverables pending for the shortest time. And the four arcs could not gate anything even if present.

## 5. X-1's consequence

X-1 is not in any register, so **DEL-01-04 (native requests, outcomes and attachments) is not DAG pending**. P2 had expected 16 pending deliverables, with DEL-01-04 among them. If you want X-1 recorded, options A or B above bring it in, and DEL-01-04 would be pending only while that later change is decided.

## 6. The checkpoint items C2-1…C2-8, updated

| # | Item | Now | Recommendation |
|---|---|---|---|
| **C2-1** | Accept DAG-002 | 41 nodes, 124 admitted and 74 held arcs, 6 unchanged cycles, DAG-001's qualifications carried. Strict audit exit 0 | **Accept**, provided the independent review has no unresolved blocking finding |
| **C2-2** | Decide the departures together or apart | 37 added arcs: 15 admitted, 22 held. The four not produced are §4 | **Accept all 37 as one successor.** None changes a cycle, and splitting would only keep deliverables pending longer. Route the four as §4 option A |
| **C2-3** | New supply from DEL-01-01 to six deliverables | As P2 expected (N-15, N-16, N-23, N-B4, N-B9, N-C5) | **Accept, and state it in the handoff.** DEL-01-01's own cycle (with DEL-01-05) is unchanged |
| **C2-4** | DEL-09-06 as a new consumer of 8 | Confirmed. DEL-09-06 stays outside the big cycle because no reverse arc exists; none of the guarded reverse citations appeared | **Accept, and keep the guard as a standing note in the handoff**, so that a later reverse row is caught as a cycle-forming change |
| **C2-5** | Findings sent to owners, not blocking | P2's list: the RS §10 and adapter-header wording behind N-12/N-B8; deferred supplier mirrors; the TBD/PENDING convention; OI-001/OI-002 still OPEN. **New:** the four arcs (§4); two supplier/consumer rows that state maturity differently (DEL-03-03 → DEL-04-01 and DEL-09-06 → DEL-04-03, TBD against INITIALIZED); DEL-04-03, DEL-02-03 and DEL-04-01 now have 20 or more connections (coordination hot spots); the carried SCA-V4-002 items (DEL-09-07, DEL-01-04 and DEL-02-02 SoW text on OI-001/002/012; the DEL-03-03 CLM-002 tail; the A17b line join); Coverage_Telemetry still stale | **Note as open matters** with their owners, in GRAPH_BASIS (done) and the handoff |
| **C2-6** | The pointer form | Confirmed: `_DAG/_LATEST.md` has no `Latest:` line, so the registered analyzer reads the accepted DAG as "incomplete". The §11.2 pointer for DAG-002 is prepared (`_DAG/_Candidates/DAG-002/PROPOSED_LATEST.md`). In a scratch run with that pointer form, the analyzer reports the same 15 pending against DAG-001 and **no departure** against DAG-002 | **At publication, write the prepared pointer** with the acceptance date. Correcting DAG-001's pointer beforehand is unnecessary |
| **C2-7** | Handoff and reliance | 15 deliverables are released on acceptance. Worth re-examining when next relied on (advice, not pending): DEL-09-07; DEL-10-03; DEL-09-02; DEL-01-04, 06-01, 06-02, 09-05 and 09-11 (they consume DEL-04-03); DEL-02-04 and 08-02; DEL-08-01; and DEL-01-02 and 01-03 on the route to DEL-01-01 | **Accept** the handoff as described in §7 |
| **C2-8** | Scope-change group 3 | **Closed.** Group 3 was accepted at checkpoint B (DECISION-8). The SoW and register changes it authorized are exactly what this candidate was built from; nothing changed after the freeze | Nothing to decide. SCA-V4-002, when applied, is a new change event with its own currency audit |

## 7. After you decide

**If you accept:**

1. The integrator writes `REVIEW_PACKET.md` with the presented hashes.
2. The integrator copies the candidate byte for byte to `_DAG/DAG-002/`, and adds:
   - `ACCEPTANCE_RECORD.md` (your words as given);
   - `HANDOFF_STATE.md`: how to read blockers, the 15 released deliverables, the DEL-09-06 guard, the advice list, the open matters and the currency command;
   - `MANIFEST.sha256`.
3. The integrator writes `_DAG/_LATEST.md` in the prepared §11.2 form, naming DAG-001 as superseded. DAG-001 stays unchanged as history.
4. **A follow-up currency audit** runs against DAG-002. It is expected to report `CURRENT` and record that nothing is DAG pending. The scratch check above already shows no departure.
5. The accepted graph is handed to `construct-local-work-graph` for the first-increment work.

**If you reject the change:** the integrator writes `REJECTION_RECORD.md` in the candidate folder and DAG-001 stands. The 37 arcs go back to the register owners for correction or retirement. A follow-up currency audit records the rejection, which also clears the pending flags.

**If you accept with qualifications or return parts:** the affected checks reopen and the changed parts come back to you.

## 8. Where things are

| Item | Path |
|---|---|
| Candidate | `projects/chirality-app-v4/execution/_DAG/_Candidates/DAG-002/` (GRAPH_BASIS.md first) |
| Currency audit | `…/_Evaluation/DAGCurrency/CURRENCY_APP_V4_BASISALIGN_2026-09-29_0856/CURRENCY_REPORT.md` |
| Closure | `…/_Evaluation/DepClosure/CLOSURE_APP_V4_BASISALIGN_2026-09-29_0855/Dependency_Closure_Report.md` |
| Case update | `…/_DAG/cases/SCC-CASE-002/Case_Datasheet.md`, section "Successor observation, 2026-09-29" |

Graph files as they stand now (SHA-256). The review packet will restate them for presentation.

| File | SHA-256 |
|---|---|
| `DeliverableNodes.csv` | `102eee1a6a409ae4babefa674546c5111848e90ba5fb7447dc5cc240a31b93e8` (identical to DAG-001) |
| `DependencyEdges.csv` | `5f96240cd75787d556f74fce851db70b2286ed196a8ae7545a795aedb6499f06` |
| `CandidateEdges.csv` | `299cb1a90860cb39879af8ba742af8646f8ce2aca7478ffe7f2e6224f79dd034` |
| `ExcludedRows.csv` | `8ac3ed597e456b5b0f29c969519d584e4335a7bada692348f337c50f7ca2c3e2` |
| `SOURCE_MANIFEST.sha256` | `6d1021f1c78fea023c2089aa29a2bc60f5ae498f56068eeddbfa376467793250` |
| `GRAPH_BASIS.md` | `fdf8450ac5c469135f3b423abf11ad64760fe7f47e8b01ccb620e167f12795b4` |
| `SOURCE_BASIS.json` | `b05af4decfbfdf117af2b398a5865be89e30d3b739ec9b8ce12b8a109e3c5874` |
| `Evidence/dag_audit.json` | `50a300df06614c9cd83856d39c788d4696935fbc34edea1fd71d3e0bdd5a45ca` |

## 9. The questions, in one place

1. Accept DAG-002 as presented, as one successor for all 37 added arcs? **Recommended: yes**, once the independent review has no unresolved blocking finding.
2. The four accepted arcs not in the registers (N-18, N-21, N-24, X-1)? **Recommended: option A**, with the consumption wording routed to SCA-V4-002.
3. Record the DEL-09-06 guard and the open matters in the handoff? **Recommended: yes.**
4. Write the accepted pointer in the prepared §11.2 form at publication? **Recommended: yes.**
