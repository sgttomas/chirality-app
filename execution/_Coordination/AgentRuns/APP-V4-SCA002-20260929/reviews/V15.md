# V15 — independent review of the DAG-003 candidate and the SCA-V4-002 propagation

**Reviewer:** node V15, a Type 2 TASK (Claude Code subagent; no delegation),
the separate review instance that `project-dag` method Stage 4 step 3 and
graph-version.md "Independent review" require, also covering the SCA-V4-002
propagation that V14 did not see (group-3 acceptance, the 9 REVISEs, the 11
register UPDATEs, closure and currency). V15 wrote none of the reviewed files.
Read-only git; no network. Writes: this file only. Scratch: `scratchpad/V15/`.

**Reviewed:** commit `b547125db` (HEAD, clean tree) against `70376aff2` (V14's
candidate), through the commits `ffdb56e1a`, `851ec3d88`, `af918ee50`,
`1efd4bcda`, `8cd783d8d`, `b547125db`. Every tool run below ran against the
HEAD bytes; historical bytes were read with `git show`.

**Authority read:** `OWNER_DECISIONS.md` (DECISION-2, DECISION-3, exact texts);
`AMENDMENT_PACKET/` at the DECISION-2 hashes (all five re-hashed: equal);
`workflows/scope-of-work` (WORKFLOW, checks), `workflows/dependency-extract`
(checks), `workflows/project-dag` (graph-version.md, currency.md, method.md);
`docs/SPEC.md` §11.2; the SCA-V4-001 closure audit
`ScopeClosure_SCA-V4-001_2026-09-29_1222/` (ASC-ISS-007, ASC-ISS-008);
DAG-002's `GRAPH_BASIS.md`, `ACCEPTANCE_RECORD.md`, `HANDOFF_STATE.md`.

## Verdict

**READY FOR CHECKPOINT C.** No blocking finding. Every mechanical claim in
`DAG_PREP/CHECKPOINT_C.md`, `DAG_PREP/REVIEW_PACKET.md`, the candidate's
`GRAPH_BASIS.md` and `Evidence/`, the closure and currency snapshots, the
group-3 snapshot and the post-acceptance record reproduced from my own scripts.
Five non-blocking observations (O-1…O-5) follow; none requires an edit to a
candidate, accepted or bound byte before the owner decides.

## Counts

| Check | Result |
|---|---|
| **1 · Group-3 acceptance** | DECISION-3 quoted exactly ("Accept (Recommended)") with custody hash `f2dda563…` equal at HEAD and at `851ec3d88`; `851ec3d88` changes only `OWNER_DECISIONS.md`; group-3 manifest 61 of 61 verify at `851ec3d88`; at HEAD the mismatches are exactly the 9 REVISEd SoWs and the 6 disclosed post-act files |
| H-1 (B-04) | Filled block reproduces HEAD `SOFTWARE_DECOMP.md` (`ea3388bc…`) from the candidate bytes (`74340581…`); five clause fills equal the packet slot table 5/5; old block occurred once; unchanged since `af918ee50` |
| H-2 (C-01) | Packet template refilled with the recorded slot values reproduces HEAD `_LATEST.md` byte for byte (`2b7938bc…`); `Latest:`/`Updated:` first; registered parser returns `SCA-V4-002_2026-09-29_1901`, `_pointer_matches` True; the pre-act pointer (`a9a7cdc8…`) returns None from the same parser (V13 F2 was real) |
| Post-acceptance validation | Reproduced 1a–1g, 2a–2f, 3a–3k, 4a, 5a–5e, 6a–6d, 8, 9b; 7a–7d taken from `POSTACCEPT/` whose `INPUT_MANIFEST.sha256` verifies 187 of 187 against `af918ee50`; 9a true at its time (now 98 OK / 32 FAILED, the expected departure). Not independently recomputed: 4b, 4c, 7e (see O-5) |
| Supersession | `accumulate_supersession_map.py --check-map`: 29 rows, 0 findings; regenerated map byte-identical to the accepted snapshot's |
| Over-claim | None: `_LATEST.md` `Closure: OPEN_PENDING_DERIVATIVE_CLOSURE`; accepted `Handoff_State.md` verdict the same; `DerivativePackageState` INCOMPLETE; SCA-V4-001 files 0 changed since `70376aff2`; its `Handoff_State.md` still `OPEN_PENDING_DERIVATIVE_CLOSURE`; CA1 folder unchanged |
| **2 · SoW REVISE** | 26 of 26 packet blocks parsed; 9 of 9 prior hashes equal the packet's and the pre-REVISE bytes (`af918ee50`); each old block occurs once and each new block zero times before; result == HEAD == `1efd4bcda` for 9 of 9; 0 unfilled tokens; frontmatter unchanged 9/9; `_STATUS.md` unchanged 9/9 (0 of 41 changed since `70376aff2`); `validate_scope_of_work.py` 9/9 valid; 0 new deliverable IDs named; RV returns' stated hashes 9/9 equal HEAD |
| B-06a | Old block occurs once in the pre-REVISE `_LATEST_ACCEPTED.md` (`d5d873b3…`); packet block reproduces HEAD; committed with the REVISEs in `1efd4bcda` |
| REVISE commit scope | Touches only the 9 SoWs, `_LATEST_ACCEPTED.md`, `DISPATCH.md` and the 9 RV returns; no SoW changed after it |
| **3 · Registers** | Exactly the 11 expected registers changed in `8cd783d8d`, none after; 4 added rows = N-18 (DEP-02-01-029), N-21 (DEP-02-03-025), N-24 (DEP-02-03-026), X-1 (DEP-02-03-027), UPSTREAM INTERFACE DELIVERABLE, none other; 1 retirement (DEP-01-04-014, `retired_by=source_revised`, successor DEP-01-04-011 named); 0 deletions |
| Quotes | 820 of 820 ACTIVE rows across all 41 registers cite `ScopeOfWork.md`, are exact substrings of their current SoW and are ≤ 30 words; the 34 re-quoted cells are 9 / 12 / 13 in DEL-04-01/02/03 |
| Validators | `validate_dependencies_schema.py` 11/11; `validate_decomposition_registers.py --families EVQ,DRB` over 826 rows: 0 ERROR, 0 WARNING |
| Human-owned sections | `_DEPENDENCIES.md` prefix (mode and declared sections) byte-identical 11/11 |
| DEP-09-07-016 | Notes only changed; the superseded "candidate/run/configured endpoint" sentence is kept as marked history and the Notes restated against the revised SoW (ASC-ISS-007 recommendation met); quote, type, target, maturity unchanged |
| Guards | DEL-04-01 has 0 suppliers; no SCC-002 member consumes DEL-09-06; N-12 and N-B8 absent |
| DX returns | Stated register, `_DEPENDENCIES.md` and source-SoW hashes 11/11 equal HEAD |
| **4 · Closure and currency** | My Tarjan over the 41 live registers at HEAD: 465 ACTIVE EXECUTION rows, 258 with a deliverable target, 202 arcs, 78 held, 124 admitted; six SCCs equal `scc_summary.csv` and DAG-002's (2/13/2/3/2/2), SCC-002 the same 13 members; at `b585e5ebe`: 462 / 254 / 198; at `1efd4bcda` (after REVISE, before UPDATE): 198, so REVISE alone changed no arc |
| Departure | Added arcs exactly the four, each carried by one row; removed 0; reciprocal pairs 24 overall / 18 in SCC-002 (+2: N-18↔N-B3 DEP-03-02-027, N-24↔N-27 DEP-03-03-014); DAG-pending endpoints exactly DEL-01-04, 02-01, 02-03, 03-02, 03-03, equal to `dag_pending.csv` and `closure_summary.json` (DAG-002, DEPARTURE, 4/0/5) |
| `_LATEST_ACCEPTED.md` | Bytes changed (B-06a), names the same GROUP3 snapshot; `DeliverableNodes.csv` byte-identical to DAG-002's and DAG-001's (`102eee1a…`): evidence drift, not an inventory change. Correct |
| DAG-002 manifests | `MANIFEST.sha256` 37/37 OK; `SOURCE_MANIFEST.sha256` from E: 98 OK, 32 FAILED (9 SoW + 11 csv + 11 md + `_LATEST_ACCEPTED.md`); DAG-001 `MANIFEST.sha256` 61/61 OK |
| **5 · DAG-003 candidate** | `audit_dag.py --dag-dir … --canonical --strict` from the repository root: **exit 0**, 124 edges, 41 nodes, 0 canonical findings, 0 endpoint issues, 0 SCCs / duplicates / bidirectional |
| Accounting | 124 + 78 + 263 = 465; each (`SourceRegister`, `DependencyID`) once; the key set equals the 465 ACTIVE EXECUTION rows of the frozen registers exactly; dispositions NOT_TOPOLOGICAL 207 / MIRROR 54 / SAME_ARC 2, each MIRROR/SAME_ARC naming its representative |
| Fidelity | 202 of 202 admitted+candidate rows equal their source in all 29 core columns; `SourceRecord` ordinals and `SourceRegisterSHA256` correct; `Explicitness`, `SatisfactionStatus`, `Confidence` non-blank canonical on all 202 |
| Carried forward | Admitted arc set == DAG-002's, same 124 representative IDs; candidate representatives == DAG-002's 74 + the 4 new rows; no representative or layer change; admitted-row drift 18 `LastSeen` only + 7 (3 SourceRef+Notes, 2 Notes, 2 EvidenceQuote+Notes), as GRAPH_BASIS states; SR-6 holds for the four (consumer UPSTREAM row is the representative); all 78 candidates `SCC_UNRESOLVED` with `SCCRef` and `CaseRef`; the four cite SCC-002 / SCC-CASE-002 |
| Manifest and hashes | `SOURCE_MANIFEST.sha256` verifies 130/130 from E, hash `d0fc611d…`, the same 130 paths as DAG-002; `REVIEW_PACKET.md` 33 rows == the candidate's 33 files, every hash equal to the bytes; `CHECKPOINT_C.md` §5 hashes 6/6 |
| Untouched | `_DAG/_LATEST.md` (`Latest: DAG-002`), `DAG-002/`, `DAG-001/`, `_Candidates/DAG-002/`, `_Candidates/DAG-001/`: 0 files changed since `70376aff2` |
| Pointer and standing | `PROPOSED_LATEST.md` in §11.2 form, `{ACCEPT_DATE}` unfilled, `Supersedes: DAG-002`, basis `8cd783d8d`; the candidate holds no `ACCEPTANCE_RECORD.md`, `HANDOFF_STATE.md`, `MANIFEST.sha256` or `INDEPENDENT_REVIEW.md` |
| CASE-002 | Writes limited to `Case_Datasheet.md`, `Case_QA.md`, `Evidence_Register.csv`, `Task_Findings.csv` and one run record; `Ruling_Register.csv` unchanged; 11 E4-* evidence hashes equal the current files; `validate_scc_resolution_case.py` exit 0 |
| Successor precheck | Reproduced in scratch (rsync of E without `_Evaluation`/`_Coordination`, candidate installed as `_DAG/DAG-003/`, §11.2 pointer): the registered analyzer reports `NO_DEPARTURE_FOUND`, 0 DAG pending, 202 edges, 6 SCCs |
| **6 · CHECKPOINT_C.md** | Every count and claim checked (below); recommendations sound; nothing implies acceptance |

## 1. Group-3 acceptance (AK2 Part 1)

The group-3 `DECISION.md` transcribes DECISION-3 with custody: record path,
section, sha256 `f2dda563…` (equal at HEAD and at `851ec3d88`), commit
`851ec3d88` (25 insertions, that file only), channel, and the earlier acts. It
says what the owner had in front of them (`70376aff2`, `ffdb56e1a`, V14, the
R-3 disclosure) and claims no inspection the owner did not perform. Its
"Interpretation" section is labeled as the recording role's reading. Its
authorizes / does-not-authorize lists match DECISION-3 "Effects" exactly,
including "acceptance of DAG-003, which is owner checkpoint C" under
does-not-authorize.

H-1 and H-2 were re-derived from the accepted `BASIS_AMENDMENT.md`
(`091871fd…`) with the DECISION-3 date and the accepted snapshot name; both
results equal HEAD byte for byte. The C-01 slot values are the right ones:
`{SCA001_CLOSURE}` cites the effective-state record at its committed path
(V14 R-1), `{OPEN_LIST}` carries the SCA-V4-001 items (telemetry, 17 re-pins,
ASC-ISS-001 confirmation) and the SCA-V4-002 `audit-scope-closure`, so moving
the pointer hides nothing. The group-1 and group-2 manifests still verify at
HEAD except the append-only `OWNER_DECISIONS.md`, so no group-bound byte was
rewritten.

**The audit-script adjustments (f) and (g).** I compared
`POSTACCEPT/audit_checks.py` with `POSTCHANGE/audit_checks.py` (which is
byte-identical to `BASELINE/`'s): 34 changed lines, all inside the two
disclosed hunks; severity-literal counts identical (BLOCKER 8, WARNING 26,
INFO 16, EXPECTED_CONSEQUENCE 1); the header documents both changes; the
unchanged script's result on the same state was also run and disclosed in
`COMPARISON.md`. I then applied the base script's `names` regex to the HEAD
pointer myself: over the whole file it yields `['SCA-V4-001_2026-09-28_2155',
'SCA-V4-002_2026-09-29_1901']`; with the `**Accepted predecessor:**` field
line excluded it yields the active snapshot alone, and the file has exactly one
`**Active snapshot:**` line.

Assessment: **(f) and (g) are honest tool-limit workarounds, and the base
script's misreading is a real limitation, not a finding against the state.**
The base heuristic treats any `_ScopeChange/SCA-*` path anywhere in the
pointer as an active snapshot, which the accepted C-01 form (Q-9, DECISION-2)
contradicts by design: a §11.2 pointer under `ACCEPTED_PREDECESSOR` posture
names its predecessor as accepted. Its registered-parser INFO compares the
parser's target with a hard-coded SCA-V4-001 folder and prints "the pointer has
no 'Latest:' line", which is false once the pointer resolves; (f) makes the
comparison against the pointer's own target, which is what the check is for.
(g) is keyed to the exact accepted field label, so it is tailored to the
accepted form and no wider; the rule (exactly one active snapshot, named by
`Latest:` and by `**Active snapshot:**`) is unchanged. See O-2 on where the
fix belongs.

## 2. The 9 SoW REVISEs (independent VERIFY)

`scratchpad/V15/sow_check.py` parsed the 26 F-blocks from the accepted
`SOW_REVISIONS.md` (`440d4d50…`), filled `{AMENDMENT_ID}` and
`{AMENDMENT_SNAPSHOT}` from the accepted records, applied each deliverable's
blocks in order to the pre-REVISE bytes at `af918ee50`, and compared with
HEAD: 9 of 9 equal, and equal to the bytes at `1efd4bcda`. Every old block
occurred once and every new block zero times before application; no
`{AMENDMENT…}` token remains; frontmatter unchanged (O-22). `_STATUS.md` is
byte-identical for all nine (NO_STATUS_TOUCH), and no `_STATUS.md` in the
project changed between `70376aff2` and HEAD. `validate_scope_of_work.py`
returns valid with 0 issues for all nine at HEAD. The mention check holds: no
revised SoW names a deliverable its prior text did not already name, so the
REVISEs could yield no arc beyond the four (confirmed in §4: the arc set after
REVISE and before UPDATE equals DAG-002's 198). The RV returns' stated revised
hashes and `_STATUS.md` hashes equal HEAD 9/9. B-06a matches the packet and
was committed with the REVISEs, as the accepted timing requires.

## 3. The 11 registers

`scratchpad/V15/reg_dag_check.py` diffed each register at HEAD against
`1efd4bcda` by `DependencyID`:

- **Added:** exactly the four rows, one per arc, UPSTREAM INTERFACE with a
  DELIVERABLE target; nothing else added anywhere.
- **Retired:** only DEP-01-04-014 (EXTERNAL OI-002, `retired_by=source_revised`,
  successor DEP-01-04-011 named). Justified: the revised DEL-01-04 TBD-002
  (F-0104-04) now records OI-002 as ruled by DECISION-1 D3 with no residual
  owner-held constraint or point of need, so the row's quoted text no longer
  exists and no narrowed quote is available, unlike DEL-01-04's OI-001 row
  (013, narrowed to uncovered matters) and DEL-09-07's rows 022/023 (each
  revised TBD keeps a residual constraint with a point of need). This is the
  DEP-02-03-016 treatment under SCA-V4-001.
- **Re-quoted:** 34 `EvidenceQuote` cells in DEL-04-01 (9), DEL-04-02 (12),
  DEL-04-03 (13), each with a Notes line; no other column changed on those rows.
  Every one is now an exact substring (ASC-ISS-008 / V12 F1 closed).
- **Other edits:** DEL-09-07 rows 016 (Notes only; see the counts table), 020
  (Notes), 022 and 023 (TargetName, Statement, EvidenceQuote, Notes; targets
  and types unchanged); the remaining rows in the 11 registers changed
  `LastSeen` only.
- **Whole-execution sweep:** 820 of 820 ACTIVE rows in all 41 registers cite
  `ScopeOfWork.md`, quote an exact substring of their current SoW, and stay
  within 30 words. Validators pass. The human-owned prefixes are byte-identical.
- **Guards:** held graph-wide (counts table).

## 4. Closure and currency

My Tarjan recomputation is independent of `arcs.py`, `scc.py`,
`reapply_selection.py` and `analyze_dep_closure.py`: same rule (ACTIVE
EXECUTION rows with a DELIVERABLE target; UPSTREAM From→Target, DOWNSTREAM
Target→From). Six SCCs, identical member sets to the closure snapshot and to
DAG-002; 202 arcs, 78 held; the four added arcs sit with both ends in
SCC-002, so the partition could not change. `DEPARTURE` is the right class:
arcs were added. Exactly five deliverables are pending (the endpoints), and
the currency report names them with the decision awaited. `_LATEST_ACCEPTED.md`
is correctly treated as evidence drift: it names the same GROUP3 snapshot and
the node file is byte-identical, so the inventory did not change; binding the
new bytes in DAG-003's manifest keeps B-06a inside this one departure. The
DAG-002 snapshot itself is intact (37/37) and DAG-001 unchanged (61/61).

## 5. The DAG-003 candidate

The strict audit exits 0 from the repository root. Accounting, fidelity and
the carried-forward rules are verified in the counts table; the only reopened
decisions are the four arcs, as GRAPH_BASIS states, and every other rule,
ruling, exemption and qualification is presented as carried forward, not
re-decided. The CASE-002 update is evidence only (no ruling, no remedy,
`Ruling_Register.csv` unchanged) and validates. `REVIEW_PACKET.md` was
written before this checkpoint and its 33 hashes equal the candidate bytes;
it states that the decision covers both checkpoints, which the method allows
here (no SCC needs a ruling; only held arcs change).

Semantic points the graph-version rules ask a reviewer to examine:

- **Edge semantics fit the objective.** Each of the four rows quotes a
  "consumes … does not define" sentence naming a concrete contribution
  (dispositions, identities, events, observations, act control) used in a
  stated part of the consumer's work. X-1's Notes and Statement keep the
  narrow scope (App-side positive capture fixtures only). No arc rests on an
  ownership sentence.
- **Reciprocal pairs.** N-18↔N-B3 and N-24↔N-27 join different contributions
  in each direction (DEP-03-02-027 is DEL-03-02 consuming DEL-02-01's workflow
  identity; DEP-03-03-014 is DEL-03-03 consuming DEL-02-03's checkpoint
  statement). Two arcs, not a mirror; both held. Correct.
- **Mirror conflicts.** None new; the two maturity differences from DAG-002
  stand and are routed. **Isolated nodes:** 0. **Hubs:** DEL-02-01 newly at
  the threshold (20) and DEL-02-03 up to 23, both from the held arcs; recorded
  in the closure report and to be carried in the handoff.
- **Exclusion patterns.** NOT_TOPOLOGICAL 207 is DAG-002's 208 less the one
  retired EXTERNAL row; no `OUTSIDE_INVENTORY`, `UNRESOLVED_TARGET`,
  `INVALID_ROW` or `TYPE_NOT_SELECTED` rows, so no scope-boundary question
  hides in the exclusions.
- **Candidate reasons and held work.** All 78 are `SCC_UNRESOLVED` citing
  their case; GRAPH_BASIS states what each hold leaves without an input.

## 6. CHECKPOINT_C.md

Every claim was checked against my own results: the 124 admitted arcs are
DAG-002's; 74 → 78 held, all in the 13-member SCC-002; 0 removed; 6 cycles
with the same members; 41 nodes byte-identical; 462 → 465 rows each placed
once; 264 → 263 excluded; the four-arc table matches the rows and their
reciprocals; the five pending deliverables are the endpoints and all already
in SCC-002; strict audit exit 0; the scratch analyzer result (reproduced);
§3 "carried forward" matches DAG-002's GRAPH_BASIS and ACCEPTANCE_RECORD; the
§5 paths exist and the six hashes equal the bytes; §6's publication steps
match method Stage 5 and DAG-002's precedent; the rejection path is stated
honestly (rejecting the rows would mean undoing the accepted Q-4 sentences).
The recommendations are sound: accepting all four as one successor decides
nothing extra and clears the five pending deliverables sooner; no admitted arc
changes, so no verdict changes on acceptance; X-1's narrow scope and the
DEL-09-06 guard belong in the handoff. Nothing on the page, in
`PROPOSED_LATEST.md` (`{ACCEPT_DATE}` unfilled), in `_DAG/_LATEST.md`
(`Latest: DAG-002`) or in the candidate folder implies acceptance.

## Observations (non-blocking)

| # | Observation | Disposition |
|---|---|---|
| O-1 | **V12 F8 count is stale** in CHECKPOINT_C C2-5 ("retired in three registers, kept in four") and GRAPH_BASIS ("amended and kept in DEL-04-01, DEL-04-02, DEL-04-03 and DEL-09-06"). At HEAD, OI-001/OI-002 rows are ACTIVE in seven registers (DEL-04-01, DEL-04-02, DEL-04-03 as one combined row DEP-04-03-019, DEL-06-02, DEL-09-02, DEL-09-06, DEL-09-07), RETIRED in DEL-02-03 and DEL-05-02, and split in DEL-01-04 (OI-001 row 013 kept and narrowed; OI-002 row 014 retired). No arc is affected; the point is an advisory consistency finding for the register owners | Correct the count in DAG-003's `HANDOFF_STATE.md` at publication. No candidate byte needs to change |
| O-2 | **Home of the audit-script fix.** DISPATCH row AK2 Part 1 calls the fix to the base script "Root tooling work". The base script is the run-local inherited script (`APP-V4-BASIS-ALIGN-20260928/POSTACCEPT/audit_checks.py` → this run's `BASELINE/`), not a `tools/` file. The substantive point stands: it is outside this amendment. The fix belongs to the next `audit-decomp` script generation (or to Root if that script is promoted), and the next run under `ACCEPTED_PREDECESSOR` posture will hit the same heuristic without it | Note in the SCA-V4-002 closure-audit brief; no edit now |
| O-3 | **Placement of `INDEPENDENT_REVIEW.md`.** `REVIEW_PACKET.md` says the review "is added to the candidate when returned", which would make the candidate 34 files against the packet's 33. DAG-002's precedent added `INDEPENDENT_REVIEW.md` at publication in the accepted snapshot (MANIFEST 37 = 33 + ACCEPTANCE_RECORD, HANDOFF_STATE, INDEPENDENT_REVIEW, REVIEW_PACKET). This review changes no candidate file, so the packet need not be re-issued | At Stage 5, copy this file as `INDEPENDENT_REVIEW.md` into `_DAG/DAG-003/` and keep `REVIEW_PACKET.md` as the 33-file graph list, as DAG-002 did |
| O-4 | The accepted SCA-V4-002 `Handoff_State.md` says "DAG-002 … CURRENT now (130/130 OK after H-1…H-3)". True at its finalization and now superseded by the currency audit; the same row says "It **will depart**", so the record is not misleading and, being the accepted snapshot, is not edited | None. Consumers read `_Evaluation/DAGCurrency/_LATEST.md` |
| O-5 | Scope of this review's reproduction: post-acceptance validation items 4b, 4c (the B8 recompute rule over 144 rows) and 7e (topology count) were not independently recomputed. 4a's unchanged hash (`36677365…`) makes 4c moot for the applied bytes; 7e is consistent with 41 registers, 41 nodes and DAG-003's `packages: 11`. The `audit-decomp` rerun itself was not re-executed; its input manifest verifies 187/187 against the committed bytes | Disclosure only |

## For the owner

- No blocking finding. The four arcs the owner kept at Q-4 are now carried by
  one register row each, are exactly the departure, and gate nothing; the
  admitted layer is byte-for-byte DAG-002's. Accepting DAG-003 changes no
  ready or blocked verdict; it releases the five pending deliverables and
  records the four contributions as live obligations inside CASE-002.
- The (f)/(g) script adjustments in `POSTACCEPT/` are honest and disclosed;
  the base heuristic they work around is a real limitation for every future
  audit under `ACCEPTED_PREDECESSOR` posture (O-2).
- O-1 is a wording correction for the handoff; O-3 is a packaging note for
  publication. Neither reopens a check.
- Unchanged and still routed: the two mirror maturity differences, the
  TBD/PENDING convention, V12 F6 (N-05/N-07 consumer wording), the RS §10 and
  ADAPTER wording, the deferred supplier mirrors, `Coverage_Telemetry.json`,
  the 17 Design re-pins, and the SCA-V4-002 closure audit with the
  ASC-ISS-001 confirmation for SCA-V4-001.

## Tools and scratch

`scratchpad/V15/sow_check.py` (47 checks: packet parse, 9 SoW reproductions,
B-06a, B-04, C-01, parser, base-script regex, group-3 manifest, custody,
validators, mention check) and `scratchpad/V15/reg_dag_check.py` (62 checks:
register diffs, 820-row quote sweep, validators, human-owned prefixes, Tarjan at
three revisions, guards, DAG-003 accounting and fidelity, manifests, packet
hashes, CASE-002). Two rows my scripts printed as FAIL were my own string
matching (a Notes field truncated before `retired_by=source_revised`; the
validator's "ERROR findings: 0" line); the underlying facts pass, as shown in
the counts table. Also run: `audit_dag.py --canonical --strict` (exit 0),
`accumulate_supersession_map.py --check-map` (29 rows, 0 findings, byte-
identical regeneration), `validate_scc_resolution_case.py` (exit 0), and the
scratch analyzer install of the candidate as DAG-003 (`NO_DEPARTURE_FOUND`).
No repository file other than this one was written.
