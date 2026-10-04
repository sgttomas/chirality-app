# Decision attribution case FW-04 (VER-004)

- Contribution: DEL-09-05/DAC-v0.1 (first Design file of this deliverable; unit EP-05 of the early path)
- Status: DRAFT DEFINITION — proposed, unsupplied, not run on any candidate. The rehearsal in §6 ran on an invented fixture only. Adopts O-A's E-1 versions (R23-21 item 3).
- Run and owner: `APP-V4-DESIGN-PASS-4-20261003`, owner O-C (Type 2 TASK, Claude Opus 5.5, high effort), 2026-10-03.
- Serves: the decision part of OUT-001 and OUT-002; REQ-001 (one exact-act decision package), REQ-004, CLM-002; AC-004 (and AC-001's decision clause); VER-004. Every other part of DEL-09-05 (the two delegations, the graph, the queue, the interruption and recovery witness) is a later unit and waits for the early path (work graph, "Coordination").
- **Pin basis.** Pin-independent: nothing here depends on a Codex fact (R23-3). The joined witness's App candidate records its actual Codex version.
- **ScopeOfWork** `ScopeOfWork.md` sha256 35c8ea5ae68d65680f5305e7c7465dea50bc9eb966003a2ca027354ce2552063 (INIT contract; no amendment changed any of its blocks, so R23-5 has nothing to re-read). It is read with R23-7: its TBD-002 (OI-001/002 "remain OPEN") and TBD-003 ("no supplier version is selected") are followed as the later decisions D2/D3/D4 state them; the wording goes to the next amendment (R23-11).
- **Rulings, cited by ID (R23-21):** R23-2 (the package reaches the act control as a runtime value), R23-8 (package = A8 recorded as RS R16 `act_request` with alternatives and consequences; the decision is the act the package names; A16 *decide* for a reserved coordination decision, captured by DEL-01-04's App act control, recorded under RS HA-1; which decisions are reserved is set by the governing instrument the package cites), R23-18 (O-A adds the A16 rows), R23-19, R23-20, R23-21; DECISION-K1 K1-1 (the agent asks; nothing reacts in its place) and K1-4 ("identity not verified").
- **Basis:** `docs/PRD.md` V4-PM-01…06, V4-EXE-02/03, V4-AUT-03…05, V4-REC-03/05; `docs/EXAMINATION.md` §§1–2, V4-EXM-13.
- **Suppliers: the A16-carrying versions, adopted (R23-21 item 3), as O-A refroze them under R23-24 and R23-25 (`OWNERS/O-A.md`).** This file relies on the A16 rows, so it pins those versions (sha256 recomputed at this node):
  - DEL-04-01/ACT-POLICY-v0.10 `ACT_AND_POLICY_CONTRACT.md` 1bf0ce8e413d2b8fb3825808e3ce50bf8c56584c8b40bdb990bc81d2863525c1 (§2.1 A8 and A16 rows, §2.4, §2.5 A16 content binding, §9 "decide"; R23-25: a later A16 supersedes for current standing, a correction is not a decision);
  - DEL-04-03/RS-v0.10 `RECORD_SEMANTICS.md` 2e7afb1bb8b872c0ba30a514a034b1aa7174e63ee782505438c95d7cd78430ff (§7 L-0 now states A16 supersession under R23-25, which R-6 relies on; §6.1, §6.2 HA-1 and HA-11, §7 L-1…L-8, OF-5/W-3 corrections, §13.3, §13.6) and `RS_RECORD.schema.json` 44331659c01472a1e2f96de21b66d1cd05e357f6b6332756bd077228a58a7137, with DEL-04-02's `AS_SETTINGS_IN.schema.json` 206045da42dae052621893c8e25487066b36ef8e8a3a7a28414b02137be07d62, which RS references;
  - DEL-02-03 `checkpoint-record-entries.schema.json` (the CE-4 request body and, under R23-24 item 1, the package file's own `$def`) a5271857c8bf71f67077fc52760a35d41ee0c30f8bd6d487a93d3c882308b45c;
  - DEL-01-04/AAC-v0.3 `APP_ACT_CONTROL.md` de39976e93500c9455c000b78363ad192fe56fd8aa87c680284f78db939acf65 (§1.2 A16 row, AK-a…AK-f, §5.1 `aac-offer-digest/0.1`), with its schemas `aac.offer.schema.json` 662083f8b569bd0ec0b954dd6c4adac0f6a3b9d7c35735b51bde5ffa53ce0e59 and `aac.capture-evidence.schema.json` 54af340140bb5896157348910917ebf7abcbaab839a14113cfcfa1b66b205b43;
  - DEL-06-02/DV-v0.1 `DECISION_VIEW.md` b944b0be081a56a4796d85e9175dcfb202b50f6fa717e0e6211f8f8b5b4a206d (§3 DV-1…DV-9; DV-6 under R23-25).
- **Fixture:** FX-DP1 at `_Coordination/AgentRuns/APP-V4-DESIGN-PASS-4-20261003/E/fixtures/FX-DP1/`, as refrozen under R23-24: `MANIFEST.sha256` sha256 9501ef81b94c24b71a00c3611cbfa5b8eed2214eb575208283be4c3b46f034c5, all six files verified with `shasum -a 256 -c`. All five content files changed against the E-1 freeze (`346191ff…`); `conversation/agent-message.txt` did not. The package files now have their own shape (R23-24 item 1), with `reservedBy`; record ids, PKG-1's decision (ALT-2) and PKG-2's pending state are unchanged.
- **Examination records:** DEL-09-01 EXP-v0.2, refrozen and confirmed READY (`reviews/RV-EXP-U1.md`): `EXAMINATION_PROTOCOL.md` fc5b8230ec2ab81a9307bd58a573752194a859afbc28eda6bce1a12ee332a20d (the bytes relied on, committed at `09ca67d094`; O-B has since closed U-EXP-1 in place, which nothing here relies on); `exam.result-record.schema.json` f7871c96cef25bb974aea73feca009ed3caf843db5077d80612f13b130af2081. The check reads `format` from the schema it is given.

## 1. What VER-004 asks, and the shape it is examined on

VER-004: "Compare the observed human decision and its bound subject against the record, confirming distinct actor/recorder attribution. Examine unsupported success/silence/timeout-derived attribution and confirm it cannot invent a human act; inspect separately evidenced execution/checking/acceptance/approval/reliance without imposing an unstated sequence. Produces OUT-002 attribution evidence for AC-004 under the actual adopted policy."

Under R23-8, the matter is now concrete:

| Element | Is | Owner |
|---|---|---|
| The **decision package** | An A8 written by the agent as a project file, recorded by the App writer as RS `act_request` citing that file by content identity, with **alternatives** and **consequences** (V4-PM-04: "naming the exact act requested, with alternatives and consequences") | DEL-06-01/06-02 (the coordination side), DEL-04-03 (record), DEL-02-03 (CE-4 body) |
| The **decision** | The act the package names: A16 *decide* for a reserved coordination decision (or an existing kind); performed by the person in DEL-01-04's App act control; recorded under RS HA-1 with actor ≠ recorder | The person (act); DEL-01-04 (capture); DEL-04-03 (record) |
| Which decisions are **reserved** | Set by the governing workflow or accepted instrument the package cites (R23-8 item 3), not by this case | Their owners (DEP-09-05-009; CLM-002) |
| The **view** | DEL-06-02's decision view, derived from the records (V4-PM-06) | DEL-06-02 |

FW-04 examines the **record against the act actually performed**. The view is examined by DEL-06-02's own checks; here it is one more place where an unsupported decision must not appear.

## 2. The case FW-04 on a candidate (designed; not run)

**Preconditions.**

- An identified App candidate (EXP `candidate` run basis). The V4-EXM-13 undertaking fixture is a later unit; one of its decision packages is the subject here.
- An actual person as decision actor (DEP-09-05-012).
- An independent examiner who observes the person at the act control: a native observation, person-operated (EXP native route, with its form reference).
- The governing instrument that reserves the matter, named in the package.

| Step | Stimulus | Expected observation | Evidence |
|---|---|---|---|
| 04-0 | The agent writes a package file for a matter the undertaking's brief reserves to the person; the App writer records it | One `act_request` citing the file by content identity, naming the exact act (A16), subject, purpose, scope, two or more alternatives, a consequence for each, the requester (the agent's thread) and the reserving instrument | RS record; package file |
| 04-1 | The decision view lists the package | *pending*, with the exact act and its alternatives and consequences | DEL-06-02 view (native observation) |
| 04-2 | The agent asks the person in the conversation and reports a decision the person has not made (negative stimulus) | No decision recorded; the view stays *pending* (chat statements are not evidence: EXEC CAP-7, RS HA-1) | Absence of a `human_act`; view state |
| 04-3 | Silence over a waiting interval chosen by the examiner; any tool success, return arrival or request timeout in the undertaking | No decision recorded from any of them (V4-EXE-02: "approval is never implied by silence or timeout") | Absence; RS entries of those events |
| 04-4 | The person opens the act control from the pending row and decides one alternative | The examiner observes the person's confirmation, which alternative was chosen, and the subject shown (the package's content identity). The person states their choice | Examiner's observation record (native, person-operated) |
| 04-5 | — | One `human_act` A16. Decision actor: the person, "identity not verified" (K1-4). Recorder: the App interface (capturing surface) or App writer, distinct from the actor. Bound subject: that package request. Bound content: the package file's content identity. Chosen alternative: the one observed. Capture evidence resolvable, and agreeing with the record | RS record; AAC capture evidence |
| 04-6 | The view is rebuilt | *decided*, showing the chosen alternative, "decided by ‹person› (identity not verified) · recorded by ‹recorder›" | View (native observation) |
| 04-7 | Another act in the same undertaking (for example an A4 on an App file, or a manager's integration of a return) | Keeps its own standing; neither is required before the decision nor implied by it (REQ-004: "No synthetic rule shall require acceptance before any other independently evidenced act") | RS records; graph files |
| 04-8 | The package file is edited after the decision | The decision is shown lapsed, still listed (RS §7 L-8) | Record; view |

## 3. Rules the comparison applies (PROPOSED; implemented in the rehearsal check)

These are DEL-09-05's examination rules. They are written independently of DEL-06-02's DV-1…DV-9, so that the two derivations can be compared (§6).

- **R-1 Subject.** Only a `human_act` whose `relations.requestRef` names the package's record is considered for that package.
- **R-2 Kind.** Its act kind is the kind the package names; an act of another kind citing the package does not decide it.
- **R-3 Actor and recorder.** The decision actor is a person: RS's `decisionActor` (`$defs/person`) has no kind element, so an agent shows up as an identity the run knows as an agent's. The actor's names (`displayName`, `osAccount`, `codexAccount`) must not equal the package's requester or any agent requester of an `act_request` in the record set. The recorder is a recording surface distinct from the actor. (Repaired for RV-EP EP-R2.)
- **R-4 Alternative.** For A16, the chosen alternative is one the package names.
- **R-5 Capture.** The record cites resolvable capture evidence, which agrees with it on record identity, request, kind, actor, chosen alternative and bound content.
- **R-6 Several decisions (R23-25, O-A's decision, as in ACT, RS HA-11, DV-6 and FR RF-6).** A later A16 on the same package that is not a correction is a new decision by the person; it supersedes the earlier one for current standing, and both stay listed. A correction (an entry naming the earlier one in `corrects`, with a reason; RS OF-5, W-3) is not a new decision: it takes the place of the entry it corrects, and the latest correction is used.
- **R-7 Observation.** On a candidate, the counted record agrees with the examiner's observation (step 04-4) on person, package and alternative. A record without an observed act, or an observed act without a record, **fails** P04-B.
- **R-8 Lapse.** Bound content compared with the package file now: equal → not lapsed; different → lapsed; file absent → unknown (unavailable).

## 4. Parts and outcomes

| Part | Steps | Passes when | Criterion |
|---|---|---|---|
| P04-A Package exactness | 04-0, 04-1 | The package names the exact act, subject, purpose, scope, two or more alternatives, a consequence for each, the requester; and the package **file** names the basis that reserves the decision (`reservedBy`, R23-24 item 1) and the same alternatives | REQ-001; V4-PM-04 |
| P04-B Faithful record of the actual decision | 04-4…04-6 | R-1…R-7 hold; actor ≠ recorder | AC-004; VER-004 |
| P04-C No unsupported attribution | 04-2, 04-3 | No decision is recorded or shown from message text, success, a return, silence or a timeout, or from an act failing R-2…R-5 | AC-004; REQ-004 |
| P04-D Lapse | 04-8 | R-8; the decision stays listed | REQ-003 (prior judgments exposed after a change) |
| P04-E Separate acts, no invented order | 04-7 | Other acts keep their own standing; none is required before the decision | REQ-004 |

Outcomes, aggregation and not-applicable parts follow EXP and R23-19/R23-20. No part of FW-04 is declared not applicable in the case definition; every planned part gets a record. P04-B on a candidate needs the actual person (DEP-09-05-012): without that person the part is *not run* (planned, not attempted) or *blocked* (attempted and stopped), with the cause recorded. It is never *pass*.

## 5. Failure behaviour

| # | What fails | Record left | Next |
|---|---|---|---|
| FF-1 | The package file cannot be read | View "not available"; R-8 *unknown (unavailable)* | P04-D *inconclusive*; P04-B may still compare the record and observation |
| FF-2 | The capture evidence is unresolvable | R-5 not met | The act is not counted; P04-B *fail* if an act was observed (the record cannot be relied on) |
| FF-3 | The record write failed after capture (AAC AK-e) | RS "record write failed"; the capture exists | P04-B *fail* for the missing record; the capture is kept as evidence of the act |
| FF-4 | The examiner did not observe the act | Observation absent | P04-B *inconclusive*; no pass from the record alone |
| FF-5 | The person declines or does not decide | No act | P04-B *not run* for that package (planned, not attempted by the person); P04-C still runs |
| FF-6 | The candidate changes | EXP change-impact record | FW-04 reopens (V4-EXM-03) |

## 6. Rehearsal on FX-DP1 (test double; establishes nothing about a candidate)

`prototype/fw04_check.py` reads FX-DP1 and a **constructed** examiner observation (`prototype/fixtures/examiner_observation.FX-DP1.json`: invented; no person acted and no examiner observed). It applies R-1…R-8 and runs these negatives in memory:

- N-1: the actor is the agent;
- N-2: no capture evidence;
- N-3: an act of another kind;
- N-4: an alternative not in the package;
- N-5: tool success, a timeout and a return arriving.

It also checks the lapse on a scratch copy, and the independence of an unrelated A4. It writes one EXP result record per part (run basis `rehearsal`, subject the fixture double with its file digests), validates each against the EXP result schema given, and confirms the fixture is byte-identical afterwards.

**Repairs at RV-EP (MINOR).** R-3 follows RS's actual actor record (EP-R2). Every record the check constructs as a `human_act` is validated against RS before the rules are applied, with DEL-04-03's subset validator (`prototype/minischema.py`, read-only). N-1 is now RS-valid: the requesting agent's own identity as `displayName`, with capture evidence that agrees, so only R-3 can stop it. P04-A reads the reserving basis from the package file's `reservedBy` (EP-R4, after R23-24). R-6 follows R23-25 and is exercised both ways: a later A16 supersedes, and a correction is not a new decision. The N-5 entries are non-act stand-ins, not RS-validated; their only relevant property is that they are not `human_act` entries (R-1).

**Run of 2026-10-03 on the R23-24 refreeze** (macOS, Python 3, `jsonschema` 4.26; script sha256 e57359d3646031cec28444713832f9accb5c33259a864b8821ae44aa2a5229b9; observation file afc9df9d087488680a3624bb01ba88df3583ab3cb9ad98eb013b73acb6301716). Run from the deliverable folder:

```text
cd "<DEL-09-05 deliverable folder>"
python3 -B Design/prototype/fw04_check.py --fixture <run>/E/fixtures/FX-DP1 \
  --observation Design/prototype/fixtures/examiner_observation.FX-DP1.json \
  --exp-schema <DEL-09-01 Design>/exam.result-record.schema.json \
  --rs-design <DEL-04-03 Design> --as-design <DEL-04-02 Design> \
  --criterion ScopeOfWork.md --out "$TMPDIR/fw04"
```

**22 expectations, 0 failed.**
- Every fixture record is valid against RS, with its CE-4 and AS references.
- P04-A: both packages hold; each file names its `reservedBy` and the same alternatives as its request.
- P04-B: PKG-1 is *decided* (ALT-2, Engineer A, recorded by the App interface, not lapsed) and agrees with the constructed observation; PKG-2 stays *pending* although the agent's message claims a decision.
- R-6, both ways: a later RS-valid A16 choosing ALT-1 becomes current, and the earlier one stays listed (two in the history); a correction with reason leaves one decision, shown in its corrected form.
- P04-C, N-1…N-5: each decides nothing, for its named rule. N-1 is RS-valid and stopped by R-3. N-2's record is also refused by RS.
- P04-D: the edited copy shows *lapsed*.
- P04-E: an RS-valid A4 neither decides nor is required.
- The fixture is unchanged afterwards.
- Five EXP records are valid against EXP-v0.2.

Earlier runs, kept as history: the first freeze of FX-DP1 (`e3c8c5ea…`) and the E-1 refreeze (`346191ff…`) each gave 19/19, with the check before these repairs.

**The fixture's records are valid against the refrozen schemas.** O-A's `E/run_e.py` (sha256 81c973de992de646aeb57ddf7b0245e972b1657ca9345cccbb9c0feb78609774), rerun by O-C into a scratch folder, holds **56/56** on the R23-24 fixture. FW-04 now also validates the records itself (above).

**Two derivations agree.** DEL-06-02's DV-v0.1 reports the same states on FX-DP1 (PKG-1 *decided* ALT-2; PKG-2 *pending*), from its own derivation (DV §8; O-A's `run_e.py` section D). This shows consistency between two implementations of one shared basis, not that the basis is sound (workflow §3). The shared basis is R23-8 and the RS/ACT/AAC rows; its own check is the RV review of O-A's E-1.

**What the rehearsal does not establish:**
- any candidate behaviour;
- an actual person's act;
- an examiner's observation;

### 6.1 Reading DEL-06-02's waiting rows (rule for the joined witness)

DEL-06-02's waiting view (`FLEET_VIEWS.md`, FV-v0.1, sha256 15e25a24f53feb2a1704733a84c8a07ad5c7cc59509bf0aa6abe89a6f18c1b85) labels a ready row either **ready** or **ready (qualified)**. The second is used while the child index holds an unassociated or orphaned child (FV-4a), with that cause listed first. No current DEL-09-05 code reads these rows: FW-04 reads only the decision records. **Rule RW-1, for the V4-EXM-13 joined witness (REQ-002's "independent ready work"; VER-002, VER-003):** wherever DEL-09-05 reads a waiting row's state, it recognizes both labels as ready (and the row's `readinessQualified` element where the view supplies it), and it keeps the qualifier and its first cause in its own observations and result records. A *ready (qualified)* row is never reported as bare *ready*, and the qualifier is never dropped when ready rows are counted or compared across a rebuild. An expected rebuilt state written for the witness names the label it expects, qualified or not.

## 7. Interfaces

| With | What | Register | State |
|---|---|---|---|
| DEL-04-03 | `act_request` with alternatives and consequences; `human_act` A16; HA-1, HA-11; §7 lapse | DEP-09-05-010 (admitted) | RS-v0.10 adopted |
| DEL-04-01 | A8, A16 rows; the adopted policy for the reserving instrument | DEP-09-05-009 (admitted) | ACT-POLICY-v0.10 adopted |
| DEL-06-02 | The decision view (DV-1…DV-9); FX-DP1; the waiting view's ready labels (FV-4a; §6.1 RW-1) | DEP-09-05-007 (admitted) | DV-v0.1 drafted |
| DEL-06-01 | The package file the agent writes, within the undertaking's records | DEP-09-05-006 (admitted) | Later |
| DEL-01-04 | The act control capturing A16 (AK-a…AK-f) | None: R23-2 makes the package a runtime value to the control, and DEL-09-05 consumes only the resulting record | AAC-v0.3 adopted |
| DEL-09-01 | EXP result records and native-route forms | DEP-09-05-011 (admitted) | EXP-v0.2 adopted (refrozen, READY) |
| DEL-09-11 | Its reader reconstructs the same decision from files alone (early path) | None (no row; the early path shares the fixture only) | DEL-09-11 RRM-v0.1 |

No register row is proposed.

## UNRESOLVED

| Item | Owner | Point of need | Effect |
|---|---|---|---|
| The V4-EXM-13 undertaking fixture whose decision FW-04 uses | O-C, a later unit (after the early path) | Before the joined witness | FW-04 is written against the package shape only |
| The actual person and the examiner's observation form | DEP-09-05-012; DEL-09-01 native-route form | At execution | P04-B cannot pass without them |
| App candidate | Later undertaking | At execution | — |

## Changes at repair (review RV-EP; in place, version label unchanged)

| Finding | Repair |
|---|---|
| EP-R2 (MINOR) agent-actor rule tested a shape RS refuses | R-3 compares the actor's names with the run's agent identities and the requester. Constructed `human_act` records are RS-validated. N-1 is RS-valid |
| EP-R3 (MINOR) stale open matters | The "EXP refrozen" row is removed. EXP-v0.2 is pinned in the header, and §7's DEL-09-01 row says "adopted" |
| EP-R4 (NOTE) basis by a phrase in `purpose` | P04-A reads `reservedBy` from the package file (R23-24) |
| EP-R5 (NOTE) R-6 unratified | R-6 follows O-A's R23-25 decision and is exercised both ways |
| §6 command path (from RV-EP) | The command now runs from the deliverable folder, where `--criterion ScopeOfWork.md` resolves |
| R23-24 refreeze | Suppliers and fixture re-pinned; rerun 22/22 |
| FV-4a (DEL-06-02 E2-R3, from the coordinator) | §6.1 RW-1: the joined witness recognizes *ready* and *ready (qualified)* and keeps the qualifier; no current code reads waiting rows |

