# RV3-DA1 — review of DEL-10-04 DA-v0.1 (owner O-E)

- **Reviewer:** RV3, a Type 2 TASK running as Claude Opus 5.5 (`claude-opus-5-5`). It was dispatched within the HELP_HUMAN session and did not author the unit (B-18). The review was written 2026-10-04. Method: `coordinated-knowledge-work` §3, which asks whether the unit is correct.
- **Unit:** `PKG-10_…/DEL-10-04_…/Design/DAG_ACCOUNT.md` `611adec3…a29d`. I re-hashed it; it equals its blob in `68f83d6b20`.
- **Basis read:**
  - DEL-10-04 `ScopeOfWork.md` (`fb62502a…`, which matches the pin): OUT-001/002, REQ-001…009, AC and VER-001…009, CLM-001;
  - SPEC §5.4;
  - `project-dag` WORKFLOW.md and its four resources (hashes `e5db3660`, `a55edc3b`, `4a5566bf`, `ff6b7ba5`, `d2927ed4`, all matching the account);
  - DAG-001…004 `ACCEPTANCE_RECORD.md`, `INDEPENDENT_REVIEW.md` and `MANIFEST.sha256`;
  - DAG-004 `HANDOFF_STATE.md` and `SOURCE_MANIFEST.sha256`;
  - `_Evaluation/DepClosure/` and `_Evaluation/DAGCurrency/`;
  - all seven `_DAG/cases/SCC-CASE-00*`;
  - the frozen and current `External_Dependencies.csv`;
  - the three `DAG_PREP/CHECKPOINT_C.md` files;
  - R23-2, R23-11, R23-22, R23-31.10 and R23-34.
- **Not ruled here.** O-E's two findings for HELP_HUMAN (DA §7 and §8: CASE-002's unapplied update; DEP-005's text) are left to the coordinator, as directed. I checked only that the facts they rest on are true; they are.

## Verdict: **READY**

There are no BLOCKING or MAJOR findings. There are 2 MINOR findings and 2 NOTEs. Every factual claim I checked holds, and the reruns reproduce O-E's results exactly. Acceptance of any successor stays with the person (§5 step 3, quoting SPEC §5.4 and CLM-001).

## Findings

### DA1-R1 — MINOR — §5 step 1 states the cycle test ambiguously

- **Claim.** "Any row that a deliverable already reached by the proposer would consume is an SCC-forming departure."
- **Evidence.**
  - Rows run consumer → supplier (the DAG-004 handoff: "Direction is consumer → supplier").
  - A proposed arc C → S closes a cycle exactly when S already reaches C over DAG-004's two layers. That is R23-2's reach check.
  - The sentence does not say whether "the proposer" is the consumer or the supplier. On the consumer reading (C reaches D and C would consume D) the arc is merely redundant, not cycle-forming. Only the supplier reading is correct.
- **Consequence.** An owner applying the rule literally could miss a real cycle, or flag a harmless arc. This is the procedure the rest of the pass is meant to follow.
- **Repair.** Restate it in arc terms: "A proposed row C → S (C consumes S's contribution) forms a cycle if S already reaches C over DAG-004's admitted and held layers (R23-2). It is then an SCC-forming departure for its owner and `scc-resolution-case`." Name the reach script.

### DA1-R2 — MINOR — §7 marks "R1 recommended" for CASE-006 only, though five datasheets recommend R1

- **Evidence.**
  - "R1 … recommended" appears in the current `Case_Datasheet.md` of SCC-CASE-001, 003, 005, 006 and 007. CASE-002 and CASE-004 recommend other remedies (R-01/R-03; candidate recommendations without enactment).
  - CASE-007's R1 is the treatment R23-32 F-R8 relies on for DEL-11-03 design.
- **Consequence.** The table reads as if only CASE-006 has a recommended treatment.
- **Repair.** Either give each case's recommended treatment, or drop the annotation and leave it to the datasheets. Recommendations remain unruled in every case; only CP1 is recorded.

## Notes

- **N1 — which file carries a case's state.** Each case's `Case_Contract.md` still reads `CaseState: HUMAN_RULINGS_PENDING`. Its `Case_Datasheet.md`, written after CP1, reads `EVIDENCE_ACCUMULATING`. DA reports the later one, which is correct; it would help to name the datasheet as the source of the state.
- **N2 — the two findings for HELP_HUMAN rest on true facts.**
  - CASE-002's last committed change is `b547125dbe` (2026-09-29).
  - `DAG_PREP/CASE-002_EVIDENCE_UPDATE.proposed.md` exists in SCA003's run.
  - DEP-005's current text ("No particular current upstream version … is established") predates D4 and R23-22.

## What I checked and how (rerun, not rebuilt)

| Claim | Rerun | Result |
|---|---|---|
| Manifests pass | `shasum -a 256 -c MANIFEST.sha256` in each `_DAG/DAG-00n/` | 61, 37, 37 and 37 entries; 0 failures |
| Strict audits | `tools/coordination/audit_dag.py` (`830d0d53…`) `--canonical --strict --dag-dir …`, JSON and Markdown to my scratch only | exit 0 on all four. Active edges 109, 124, 124 and 129; 41 nodes each |
| Counts | `csv.DictReader` on DependencyEdges, CandidateEdges, ExcludedRows and DeliverableNodes | 109/52/242/41, 124/74/264/41, 124/78/263/41 and 129/83/355/41, equal to §2. The DAG-004 handoff quotes "129 admitted arcs … 83 held … 355 exclusions" (verified) |
| Owner words and recorders | Each `ACCEPTANCE_RECORD.md` | DAG-001: "I have reviewed …", with the hold quoted exactly; transcribed by `/root`. DAG-002: "Accept DAG-002 (Recommended)" and "A: add wording in SCA-V4-002 (Recommended)", DECISION-10, written by D2, "D2 did not witness the chat". DAG-003: "Accept DAG-003 (Recommended)", DECISION-4, D2. DAG-004: "I accept DAG-004.", DECISION-3, D2 |
| Reviews | Each `INDEPENDENT_REVIEW.md` | DAG-001 "PASS — no unresolved blocking finding …"; DAG-002, 003 and 004 "READY FOR CHECKPOINT C" (DAG-004: no BLOCKING, no MAJOR) |
| Checkpoint packages | `shasum` of each `DAG_PREP/CHECKPOINT_C.md` | `6ff6dd96…`, `f8f63e80…` and `710de584…`, equal to each "Package presented" row |
| Closure and currency | `ls` and each `CURRENCY_REPORT.md` | Five closure snapshots. Eight currency observations: DEPARTURE for BASISALIGN, SCA002 and SCA003, each followed by an accepted successor and a CURRENT observation; latest CURRENT_WITH_EVIDENCE_DRIFT (DEL-01-03) |
| SOURCE_MANIFEST | `shasum -c _DAG/DAG-004/SOURCE_MANIFEST.sha256` from `E/` | 128 OK; 2 FAILED: DEL-01-03 `Dependencies.csv` and `_DEPENDENCIES.md`, the recorded drift |
| External dependencies | Field-by-field script, frozen against current (`055703d9…`) | Only DEP-002 changed (PresentSatisfaction, SourceRef, BoundaryAndFallback) |
| Cases | `Ruling_Register.csv` and `git log -1` per case | One ruling each, `CP1-20260928`. Last change `0139b067dc` (2026-09-27), except CASE-002 at `b547125dbe` (2026-09-29). SCC membership as in the handoff's table |
| Coverage | The SoW's bolded IDs | REQ-001…009, OUT-001/002, 9 AC, 9 VER; §3 maps every REQ |
| Quotes | SoW, SPEC, handoff | "one identified, examined and human-accepted … before the 30% position"; CLM-001 "acceptance or rejection of departures"; SPEC §5.4 "Authority comes from the human's acceptance"; handoff "A new session is not, by itself, a reason to rebuild". All verified, whitespace-normalised |
| Boundary owner | `check_boundary_owner_resolution.py` (`22ef57e0…`) | 1 checked, 0 failing, 0 citing no claim |

## What I did not check

- The fidelity of each edge row to its source register (V25 and earlier reviews cover that).
- The reach computation itself; DA1-R1 concerns only how §5 states it.
