# Checkpoint C — the successor dependency graph DAG-004

- **For:** the owner. Prepared by node D1 of run `APP-V4-SCA003-20261002`, 2026-10-03.
- **Basis:** commit `75764184b9`, after the 19 ScopeOfWork revisions and the 20 register updates of SCA-V4-003.
- **What you are asked to decide:** whether DAG-004 replaces DAG-003 as the accepted project dependency graph.

**Before you decide.** A separate reviewer, who did not build the candidate, still has to check it. Present this page with that review and its findings. Nothing on this page accepts anything. `_DAG/_LATEST.md` has not been moved, and nothing has been written under `_DAG/` or `_Evaluation/`.

**One sitting.** As with DAG-002 and DAG-003, the method lets you settle both graph checkpoints (the basis and the acceptance) at once, because no cycle needs a ruling. Everything not touched by the ten new links carries forward from DAG-003; §3 lists it so you can see it is not being re-decided. `REVIEW_PACKET.md` is already written, before this checkpoint. If you decide both checkpoints together, the acceptance record must say so.

## 1. The short version

- The ten links you accepted under SCA-V4-003 (Q-4) are now in the registers as **ten new "needs input from" relationships**. They are exactly the ten predicted, none extra and none missing.
- **Five of them are ordinary sequencing links.** This is the difference from last time. DEL-01-04, DEL-02-02, DEL-02-03 and DEL-03-03 now formally wait, for the stated part of their work, on DEL-01-02, DEL-01-03 or DEL-01-05. Those three suppliers sit outside the large cycle and do not lead back into it, so the sequencing layer stays free of cycles.
- **The other five sit inside the 13-member cycle CASE-002 already tracks.** They are held and gate nothing.
- **Unchanged:**
  - all 124 existing sequencing links;
  - no link was removed;
  - the six cycles have the same members;
  - all 41 deliverables are the same.
- The currency check against DAG-003 says `DEPARTURE`. Until you decide, **11 deliverables are "DAG pending"**: they get no ready or blocked verdict from dependencies.
- The candidate passes the strict audit (exit 0), and every register row is accounted for (567).
- In scratch, the analyzer reports **no departure** once DAG-004 is installed. The follow-up audit after acceptance is therefore expected to say `CURRENT`.
- **Recommendation:** accept DAG-004 as one successor for all ten links, once the independent review has no unresolved blocking finding.

## 2. What DAG-004 changes compared with DAG-003

| | DAG-003 | DAG-004 |
|---|---:|---:|
| Deliverables (nodes) | 41 | 41, byte-identical |
| Sequencing links (admitted) | 124 | **129** (+5) |
| Held links inside cycles (non-gating) | 78 | **83** (+5, all in the 13-member cycle, CASE-002) |
| Links removed | 0 | 0 |
| Cycles | 6 | 6, same members |
| Register rows accounted for | 465 | 567, each placed exactly once |

### The ten new links

Read "A → B" as "A needs a contribution from B, at the stated maturity (INITIALIZED, a defined contract), before the stated part of its own work".

**Sequencing links (admitted; they produce blocker verdicts once accepted):**

| Link | Meaning | Row |
|---|---|---|
| NR-05 | DEL-01-04 (native requests) needs DEL-01-03's plan-mode element, item anchors and delegation availability to compose the turns it sends | DEP-01-04-020 |
| NR-07 | DEL-01-04 needs DEL-01-05's model-selection state and reported Codex account (no model shown until chosen; identity at act capture) | DEP-01-04-021 |
| NR-01 | DEL-02-03 (workflow execution) needs DEL-01-02's custody events and run-reference look-up, so an interrupted run is recovered as the same run | DEP-02-03-028 |
| NR-02 | DEL-03-03 (receiving adapter) needs DEL-01-02's in-flight item state and relaunch fact | DEP-03-03-015 |
| NR-04 | DEL-02-02 (workflow-making workspace) needs DEL-01-02's definition of ending a run and its App-start reconciliation | DEP-02-02-020 |

**Held links (inside the 13-member cycle; gate nothing):**

| Link | Meaning | Row |
|---|---|---|
| NR-08 | DEL-01-04 needs DEL-04-02's checkpoint overlay and standing facets, which it places in the App | DEP-01-04-022 |
| NR-09 | DEL-01-04 needs DEL-02-03's checkpoint display meanings. With X-1 it forms a reciprocal pair: two links with different contributions | DEP-01-04-023 |
| NR-4 | DEL-01-04 needs DEL-02-04's role list for the new-conversation role offer | DEP-01-04-024 |
| R2-04-03-e | DEL-04-03 (run records) needs DEL-02-01's workflow identity and checkpoint vocabulary | DEP-04-03-034 |
| R20-10 | DEL-04-03 needs DEL-02-02's run text, supply-check and selection records as supplied-workflow evidence | DEP-04-03-035 |

### The 11 deliverables that are DAG pending

DEL-01-02, DEL-01-03, DEL-01-04, DEL-01-05, DEL-02-01, DEL-02-02, DEL-02-03, DEL-02-04, DEL-03-03, DEL-04-02 and DEL-04-03: the ends of the ten new links. While pending, they get no dependency verdict at all. Your decision clears all eleven.

- **Accept:** DEL-01-04, DEL-02-02, DEL-02-03 and DEL-03-03 then read the new sequencing links as blockers for the stated parts only. All five new rows have satisfaction TBD or PENDING, which is read from the live registers.
- **Reject:** the eleven return to DAG-003's verdicts.

### Other changes that are not a departure

- **Seven links keep their place but now have the consumer's own row as their representative.** SCA-V4-003 added consumer-side rows where only the supplier's row existed before, and the graph's rule picks the consumer's row. No link or layer changes. This also closes an old advice item, V12 F6: N-05, N-06, N-07 and N-20 now have consumer wording.
- **91 new mirror rows** (the supplier side of existing links), 2 new external inputs and 1 retired package row.
- The text of 19 ScopeOfWork files.

DAG-004's source manifest binds all of these bytes.

## 3. Carried forward from DAG-003 (not re-decided)

- **Objective and meaning.** Production order and route selection within this project. A link means the consumer needs the supplier's stated contribution, at the stated maturity, before the stated part of its own work.
- **Direction.** Consumer → supplier.
- **Scope.** FULL_GRAPH completeness with the same qualifications; the same 41 deliverables; no exemptions.
- **Selection rules.** SR-1…SR-7: all dependency types count; no cuts or merges; no confirmation hold; one representative row per link; links inside a cycle are held.
- **Cases.** 001, 002 (004 as history), 003, 005, 006, 007, all still gathering evidence.
- **Standing notes.** DEL-01-01 as supplier and the DEL-09-06 reverse-link guard. The guard held: DEL-09-06 is still consumed only by DEL-03-04 and DEL-09-07, and reaches the same 20 deliverables. X-1's narrow scope (DEL-02-03's App-side capture fixtures) is unchanged.
- **Maturity.** "INITIALIZED" means only that a contract is defined.
- **What acceptance does not do.** It satisfies no dependency, changes no lifecycle state (Q-13 was a separate act), lifts no hold, passes no gate and schedules nothing.

Already decided by you, and reflected in the evidence:

| Decision | Result |
|---|---|
| The 10 links (Q-4); NR-03 dropped | All 10 present in their predicted layers; DEL-09-09 → DEL-01-02 absent |
| REQ-008 adjusted so DEL-04-01 gains no supplier (Q-5) | DEL-04-01 has no suppliers; the two source-wording links are absent |
| R17-10 cycle guard; NR-06 and NR-10 withdrawn | DEL-01-02 and DEL-01-03 reach none of the guarded deliverables; NR-06 and NR-10 absent |
| Receivers sentences (Q-15) and 15 further mirror rows (Q-17) | Extracted, except the 5 rows in §5 |

## 4. The checkpoint items, with recommendations

| # | Item | Now | Recommendation |
|---|---|---|---|
| **C-1** | Accept DAG-004 | 41 nodes; 129 admitted and 83 held links; 6 unchanged cycles; DAG-003's qualifications carried. Strict audit exit 0 | **Accept**, provided the independent review has no unresolved blocking finding |
| **C-2** | Decide the ten links together or apart | All ten come from one accepted amendment, and each is in its predicted layer. Splitting them would decide nothing new and keep deliverables pending longer | **Accept all ten as one successor** |
| **C-3** | The admitted layer grows | 4 deliverables gain sequencing suppliers. Ten more deliverables reach those consumers through sequencing links: DEL-03-04, 09-02, 09-06, 09-07, 09-11, 10-03, 10-04, 11-01, 11-02 and 11-03. They are not pending | **Note in the handoff:** the four consumers wait for the named contribution only in the stated part; list the ten for route re-examination when they next rely on those inputs |
| **C-4** | Mirror maturity | DAG-003's two differences are reconciled. Three new ones: DEL-06-01 → DEL-01-01, DEL-09-01 → DEL-01-01 and DEL-08-02 → DEL-02-01 (consumer TBD, supplier INITIALIZED) | **Note as open matters**, routed to both register owners; drop the two reconciled ones |
| **C-5** | Open matters | Closed: the two old maturity differences, V12 F6. Still open: TBD/PENDING convention, OI-001/002 rows, RS §10 and adapter-header wording, and the carried obligations in §5 | **Note as open matters** with their owners, in the handoff |
| **C-6** | The pointer | Prepared in §11.2 form: `DAG-004/PROPOSED_LATEST.md` (`Supersedes: DAG-003`). It cites the currency audit at its `_Evaluation/DAGCurrency/` home | **At publication, write the prepared pointer** with the acceptance date, after the currency snapshot is placed there |
| **C-7** | Where the files go | Because of this node's write fence, the candidate, its closure and currency snapshots, and the CASE-002 update are staged in `DAG_PREP/` | **Authorize the integrator** to place them as §6 lists. The candidate goes in `_DAG/_Candidates/DAG-004/` and, on acceptance, `_DAG/DAG-004/`, byte for byte against `REVIEW_PACKET.md` |

## 5. Carried obligations (not decided here; none blocks the graph)

| Obligation | What it is | Owner and route | Recommendation |
|---|---|---|---|
| **5 mirror rows not extracted** | DEL-01-01 → DEL-02-04 and → DEL-04-03; DEL-01-05 → DEL-01-01; DEL-03-02 → DEL-03-01; DEL-03-03 → DEL-02-03. The revised text names the receiver only as owner or supplier, and careful extraction takes no row from that. Each link already exists through the consumer's row. **No graph effect** | You: a receivers sentence in a later ScopeOfWork revision, or a declared entry in the supplier's `_DEPENDENCIES.md` (the Q-15 alternative) | Carry to the next amendment. Not needed for DAG-004 |
| **DEL-01-03 absolute TargetLocation** | 14 rows in DEL-01-03's register record a file location under a personal home folder instead of a project-relative path. 10 are anchor rows; 2 are admitted representatives (DEP-01-03-011, -012), which DAG-002 and DAG-003 already copy byte for byte; 2 are excluded rows (DEP-01-03-013, a mirror; DEP-01-03-014, a package-target input). The graph must copy register bytes, so DAG-004 carries them too | DEL-01-03 register owner, `dependency-extract`. Fixing it changes bytes, not links | Repair after acceptance. The next currency audit would then read `CURRENT_WITH_EVIDENCE_DRIFT`, and no new graph is needed. If you prefer the path not to appear in DAG-004 at all, repair first; the candidate is then re-frozen, rebuilt and re-reviewed |
| **The 17 Design re-pins** | Carried from SCA-V4-001, deferred by APP-V4-BASIS-ALIGN DECISION-8. No graph link rests on a Design file | You, separately governed | Unchanged; not a graph matter |
| **`Coverage_Telemetry.json`** | Stale (STALE_REBUILD_REQUIRED). It keeps SCA-V4-001's closure, and so SCA-V4-003's (`OPEN_PENDING_DERIVATIVE_CLOSURE`), open | Decomposition owner, by a later bounded brief | Unchanged; not a graph matter |
| CASE-002 evidence update | Drafted (`CASE-002_EVIDENCE_UPDATE.proposed.md`), not applied because of the fence. Evidence only | Integrator, through `scc-resolution-case` | Apply at publication |
| Currency observation pointer | `_Evaluation/DAGCurrency/_LATEST.md` still shows the 2026-09-29 `CURRENT` result. The departure is visible to the analyzer but not to someone reading only that pointer | Integrator | Place the currency snapshot and move the pointer as soon as authorized, even before your decision |
| SCA-V4-003 closure | The accepted DAG is one of SCA-V4-003's derivative packages | `scope-change`, after this checkpoint | As planned |

## 6. After you decide

**If you accept:**

1. The integrator copies the closure and currency snapshots to `_Evaluation/DepClosure/` and `_Evaluation/DAGCurrency/`, verified against `REVIEW_PACKET.md`, and moves those pointers (if not already done). It then applies the CASE-002 update through `scc-resolution-case`.
2. The integrator copies the candidate byte for byte to `_DAG/_Candidates/DAG-004/` (as the candidate record) and `_DAG/DAG-004/`, verifies both against `REVIEW_PACKET.md`, and adds to `_DAG/DAG-004/`:
   - `ACCEPTANCE_RECORD.md`: your words as given, stating whether the decision covers both checkpoints;
   - `HANDOFF_STATE.md`: how to read blockers; the 11 released deliverables; the four consumers' new sequencing waits and the ten for re-examination; X-1 and the DEL-09-06 guard carried; open matters; the currency command;
   - `INDEPENDENT_REVIEW.md`, a copy of `REVIEW_PACKET.md`, and `MANIFEST.sha256`.
3. The integrator writes `_DAG/_LATEST.md` from `PROPOSED_LATEST.md`, naming DAG-003 as superseded. DAG-003, DAG-002 and DAG-001 stay unchanged as history.
4. **A follow-up currency audit** runs against DAG-004. It is expected to report `CURRENT`, with nothing DAG pending.

**If you reject the change:**

1. The integrator writes `REJECTION_RECORD.md` in the candidate folder, and DAG-003 stands.
2. The ten rows go back to the register owners. Removing them means undoing ScopeOfWork sentences you accepted at Q-4.
3. A follow-up currency audit records the rejection and clears the pending flags.

**If you accept with qualifications or return parts:** the affected checks reopen and the changed parts come back to you.

## 7. Where things are (under `_Coordination/AgentRuns/APP-V4-SCA003-20261002/`)

| Item | Path |
|---|---|
| Candidate | `DAG_PREP/DAG-004/` (`GRAPH_BASIS.md` first) |
| Currency audit | `DAG_PREP/CURRENCY_APP_V4_SCA003_2026-10-03_1937/CURRENCY_REPORT.md` |
| Closure | `DAG_PREP/CLOSURE_APP_V4_SCA003_2026-10-03_1936/Dependency_Closure_Report.md` |
| Case update (draft) | `DAG_PREP/CASE-002_EVIDENCE_UPDATE.proposed.md` |
| Review packet | `DAG_PREP/REVIEW_PACKET.md` (every file with its SHA-256) |

The graph files as presented:

| File | SHA-256 |
|---|---|
| `DeliverableNodes.csv` | `102eee1a6a409ae4babefa674546c5111848e90ba5fb7447dc5cc240a31b93e8` (identical to DAG-001…003) |
| `DependencyEdges.csv` | `c43033742df768a6fb493701d25b1d73240366172c05b1d0caa143650690966e` |
| `CandidateEdges.csv` | `2bfff10e3094d7fd86da563006c965694563ec10d0fc78e9b1d9958fefa42025` |
| `ExcludedRows.csv` | `45f55e76ecf7c9aac3bd923838eee8c302d6b2776e4fa3c221e51f9cf465664e` |
| `SOURCE_MANIFEST.sha256` | `03aa668b88cb1cb32e1d26a15fb64afdf85e0af6fbb61ec89f833eaf5893a8ef` |
| `Evidence/dag_audit.json` | `0f4fca923d18beb7a5889facd7108f587949b59a7e6c83c1821ce9d4d6d9ba22` |

## 8. The questions, in one place

1. Accept DAG-004 as presented, as one successor for all ten added links, deciding project-dag checkpoints 1 and 2 together? **Recommended: yes**, once the independent review has no unresolved blocking finding.
2. Record in the handoff:
   - the four new sequencing waits and the ten deliverables to re-examine;
   - X-1's narrow scope;
   - the carried DEL-09-06 guard;
   - the open matters and carried obligations of §4–§5.

   **Recommended: yes.**
3. Authorize the integrator to place the staged files (candidate, closure, currency, CASE-002 update) in their method homes and to write the prepared pointer at publication? **Recommended: yes.** The currency observation can be placed now, before your decision.
4. The DEL-01-03 absolute path: repair after acceptance, as evidence drift, or before, which means rebuilding the candidate? **Recommended: after.**
