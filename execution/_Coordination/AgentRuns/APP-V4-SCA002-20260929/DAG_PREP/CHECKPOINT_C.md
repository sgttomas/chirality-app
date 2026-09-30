# Checkpoint C — the successor dependency graph DAG-003

- **For:** the owner. Prepared by node D1 of run `APP-V4-SCA002-20260929`, 2026-09-29.
- **Basis:** commit `8cd783d8d`, after the 9 SoW revisions and the 11 register updates of SCA-V4-002.
- **What you are asked to decide:** whether DAG-003 replaces DAG-002 as the accepted project dependency graph.

**Before you decide.** A separate reviewer, who did not build the candidate, still has to check it. Present this page with that review and its findings. Nothing on this page accepts anything, and `_DAG/_LATEST.md` has not been moved.

**One sitting.** As with DAG-002, the method lets you settle both graph checkpoints (the basis and the acceptance) at once: the change is small and no cycle needs a ruling. Almost everything carries forward from DAG-002 unchanged; §3 lists it so you can see it is not being re-decided. `DAG_PREP/REVIEW_PACKET.md` is already written, before this checkpoint, and says the decision covers both checkpoints. The acceptance record must say so too.

## 1. The short version

- The four "consumes" sentences you accepted under SCA-V4-002 (Q-4, the answer to DAG-002's option A) now exist in the registers as **four new "needs input from" relationships**: N-18, N-21, N-24 and X-1.
- **All four sit inside the 13-member cycle that CASE-002 already tracks.** They are held and gate nothing. Nothing else in the graph changes:
  - the 124 ordinary sequencing arcs are exactly DAG-002's;
  - no relationship was removed;
  - the six cycles have exactly the same members;
  - all 41 deliverables are unchanged.
- The currency check against DAG-002 says `DEPARTURE`, because arcs were added. Until you decide, **5 deliverables are "DAG pending"** and get no ready or blocked verdict from dependencies: DEL-01-04, DEL-02-01, DEL-02-03, DEL-03-02 and DEL-03-03.
- The candidate passes the strict audit (exit 0) and every register row is accounted for.
- In scratch, the analyzer reports **no departure** against DAG-003 once installed, so the follow-up currency audit after acceptance is expected to say `CURRENT`.
- **Recommendation:** accept DAG-003 as one successor for all four arcs.

## 2. What DAG-003 changes compared with DAG-002

| | DAG-002 | DAG-003 |
|---|---:|---:|
| Deliverables (nodes) | 41 | 41, byte-identical |
| Admitted sequencing arcs | 124 | **124**, same arcs |
| Held arcs inside cycles (non-gating) | 74 | **78** (+4, all in the 13-member cycle, CASE-002) |
| Arcs removed | 0 | 0 |
| Cycles (SCCs) | 6 | 6, same members |
| Register rows accounted for | 462 | 465, all placed exactly once |

### The 4 new held arcs

Read "A → B" as "A needs a contribution from B".

| Arc | Meaning | Row |
|---|---|---|
| N-18 | DEL-02-01 (workflow contract) needs DEL-03-02's item dispositions, identities and events for checkpoint subject binding and item-level decisions | DEP-02-01-029 |
| N-21 | DEL-02-03 (execution compatibility) needs the same DEL-03-02 outputs, plus applied outcomes, for checkpoint recording and replayed history | DEP-02-03-025 |
| N-24 | DEL-02-03 needs DEL-03-03's observations of checkpoint arrivals and acts on the external channel | DEP-02-03-026 |
| X-1 | DEL-02-03 needs DEL-01-04's App act control and person identity, only for its App-side positive capture fixtures, which wait for that later undertaking | DEP-02-03-027 |

N-18 and N-24 each form a reciprocal pair with an existing arc in the other direction (N-B3 and N-27). Both directions carry different contributions; this is expected and was predicted in ARC_EFFECT.

### The 5 deliverables that are DAG pending

DEL-01-04, DEL-02-01, DEL-02-03, DEL-03-02 and DEL-03-03. All five are already members of the held cycle, so the arcs they gain are held too; while pending they get no dependency verdict at all, and after your decision their blockers again come from the admitted layer, which has not changed. Your decision here clears all five.

### Changed bytes that are not a departure

The re-quoted evidence in DEL-04-01, DEL-04-02 and DEL-04-03 (the 34 backtick cells from V12 F1, now exact), the SoW text in nine deliverables, one retired external row in DEL-01-04, and the reading-rule note on `_LATEST_ACCEPTED.md` all changed bytes without changing any arc. DAG-003's source manifest binds the new bytes, so they cause no second departure.

## 3. Carried forward from DAG-002 (not re-decided)

- **Objective and meaning.** Production order and route selection within this project. An arc means the consumer needs the supplier's stated contribution, at the stated maturity, before the stated part of its own work.
- **Direction.** Arcs run from consumer to supplier.
- **Scope.** FULL_GRAPH completeness, with the same qualifications. The same 41 deliverables, no exemptions.
- **Selection rules.** SR-1…SR-7: all dependency types count; no cuts or merges; no confirmation hold; one representative row per arc; arcs inside a cycle are held.
- **Cases.** The six cycles are tracked in cases 001, 002 (with 004 as history), 003, 005, 006 and 007, all still gathering evidence. CASE-002 gained the four arcs as evidence only.
- **DEL-01-01 as supplier and DEL-09-06 as consumer**, with the DEL-09-06 reverse-arc guard. The guard held: no reverse row appeared.
- **Maturity.** "INITIALIZED" means only that a contract is defined.
- **What acceptance does not do.** It satisfies no dependency, changes no lifecycle state, lifts no hold, passes no gate and schedules nothing.

Already decided by you, and reflected in the evidence:

| Decision | Result |
|---|---|
| Keep all four arcs (SCA-V4-002 Q-4; DAG-002 option A) | All four present, one row each, none extra |
| X-1 kept narrowly, tied to the capture fixtures | The row quotes the fixture-scoped sentence |
| N-12 and N-B8 not proposed | Absent |
| The DEL-04-01 qualifier and the DEL-09-06 guard | DEL-04-01 has no suppliers; no SCC-002 member consumes DEL-09-06 |
| The reading-rule note on `_LATEST_ACCEPTED.md` (Q-12) | Applied, bound in this manifest |

## 4. The checkpoint items, with recommendations

| # | Item | Now | Recommendation |
|---|---|---|---|
| **C2-1** | Accept DAG-003 | 41 nodes, 124 admitted and 78 held arcs, 6 unchanged cycles, DAG-002's qualifications carried. Strict audit exit 0 | **Accept**, provided the independent review has no unresolved blocking finding |
| **C2-2** | Decide the departures together or apart | 4 added arcs, all held. Splitting them would decide nothing extra and keep deliverables pending longer | **Accept all four as one successor** |
| **C2-3** | The held layer grows; no admitted arc changes | No blocker verdict changes for any deliverable on acceptance. The five pending deliverables are released to the same admitted layer they had under DAG-002 | **Note in the handoff** that acceptance changes no verdict; it records the four contributions as live obligations inside CASE-002 |
| **C2-4** | X-1's meaning | DEL-02-03's App-side positive capture fixtures wait for DEL-01-04, a later undertaking. Holding the arc does not make them ready; EXEC §5 already marks them AWAITING INPUT | **Accept as recorded**; keep the narrow scope in the handoff so it is not read as a whole-deliverable wait |
| **C2-5** | Findings sent to owners, not blocking | Closed: V12 F1 (re-quoting) and the pointer form. Still open, unchanged: the two mirror maturity differences; the TBD/PENDING convention (the new rows use both); V12 F8 (OI-001/002 rows retired in three registers, kept in four); V12 F6 (N-05/N-07 consumer wording, left out of SCA-V4-002 by design); the RS §10 and adapter-header wording; deferred supplier mirrors; Coverage_Telemetry still stale; the SCA-V4-002 closure audit still to run | **Note as open matters** with their owners, in GRAPH_BASIS (done) and the handoff; drop the two closed ones |
| **C2-6** | The pointer | Prepared in §11.2 form: `_DAG/_Candidates/DAG-003/PROPOSED_LATEST.md` (`Supersedes: DAG-002`). The registered analyzer reads §11.2 pointers; in scratch it reports no departure against DAG-003 | **At publication, write the prepared pointer** with the acceptance date |
| **C2-7** | Handoff and reliance | 5 deliverables released on acceptance. No renewed examination is called for: the four arcs are held and no route through an admitted arc changed. DAG-002's advice list stands | **Accept** the handoff as described in §6 |
| **C2-8** | The predecessor's DAG-002 candidate folder | Left in place as the candidate record, as DAG-002's acceptance record says. DAG-003 does not touch it | Nothing to decide |

## 5. Where things are

| Item | Path |
|---|---|
| Candidate | `projects/chirality-app-v4/execution/_DAG/_Candidates/DAG-003/` (GRAPH_BASIS.md first) |
| Currency audit | `…/_Evaluation/DAGCurrency/CURRENCY_APP_V4_SCA002_2026-09-29_2057/CURRENCY_REPORT.md` |
| Closure | `…/_Evaluation/DepClosure/CLOSURE_APP_V4_SCA002_2026-09-29_2056/Dependency_Closure_Report.md` |
| Case update | `…/_DAG/cases/SCC-CASE-002/Case_Datasheet.md`, section "Successor observation, 2026-09-29 (DAG-003 candidate; evidence update only)" |
| Review packet | `DAG_PREP/REVIEW_PACKET.md` (every candidate file with its SHA-256) |

The graph files as presented (SHA-256; the review packet lists every file):

| File | SHA-256 |
|---|---|
| `DeliverableNodes.csv` | `102eee1a6a409ae4babefa674546c5111848e90ba5fb7447dc5cc240a31b93e8` (identical to DAG-001 and DAG-002) |
| `DependencyEdges.csv` | `4716ca287d23835cd5ed490e27c4b7e117c89f08ba19b826f489bf7b2be8e359` |
| `CandidateEdges.csv` | `07b969209e2733105b23da7cb1a10df6601f0de42a56b9f286549452fe878269` |
| `ExcludedRows.csv` | `26576f8cfca0c800a41cb02a3c8b4f83dbe92cd6a0f47b976c281426abd01c82` |
| `SOURCE_MANIFEST.sha256` | `d0fc611d95ee80ba64b86ea5b0eaa1a1ba90e85e461fb18459dd8162df6a40c5` |
| `Evidence/dag_audit.json` | `9318aa6a058b5fc980a8697be35bb57098806936bd620d433fd80f300d905124` |

## 6. After you decide

**If you accept:**

1. The integrator copies the candidate byte for byte to `_DAG/DAG-003/`, verifies it against `REVIEW_PACKET.md`, and adds:
   - `ACCEPTANCE_RECORD.md` (your words as given; it states that the decision covers project-dag checkpoints 1 and 2);
   - `HANDOFF_STATE.md`: how to read blockers, the 5 released deliverables, the X-1 scope note, the DEL-09-06 guard carried, the open matters and the currency command;
   - `INDEPENDENT_REVIEW.md` and `REVIEW_PACKET.md` copies, and `MANIFEST.sha256`.
2. The integrator writes `_DAG/_LATEST.md` from `PROPOSED_LATEST.md`, naming DAG-002 as superseded. DAG-002 and DAG-001 stay unchanged as history.
3. **A follow-up currency audit** runs against DAG-003. It is expected to report `CURRENT` and record that nothing is DAG pending.
4. The SCA-V4-002 closure audit (step 5 of the order you accepted) can then treat the accepted DAG as the derivative package it needs.

**If you reject the change:** the integrator writes `REJECTION_RECORD.md` in the candidate folder and DAG-002 stands. The four rows go back to the register owners for correction or retirement, which means undoing the SoW sentences you accepted at Q-4. A follow-up currency audit records the rejection, which also clears the pending flags.

**If you accept with qualifications or return parts:** the affected checks reopen and the changed parts come back to you.

## 7. The questions, in one place

1. Accept DAG-003 as presented, as one successor for all four added arcs? **Recommended: yes**, once the independent review has no unresolved blocking finding.
2. Record X-1's narrow scope (capture fixtures only) and the carried DEL-09-06 guard in the handoff? **Recommended: yes.**
3. Write the accepted pointer in the prepared §11.2 form at publication? **Recommended: yes.**
