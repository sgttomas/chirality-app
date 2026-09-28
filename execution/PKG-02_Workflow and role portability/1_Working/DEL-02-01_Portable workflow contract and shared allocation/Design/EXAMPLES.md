# Portable workflow declaration — readable examples
- Contribution: DEL-02-01/WD-EX-v0.4 (companion to DEL-02-01/WD-v0.4, `WORKFLOW_DECLARATION.md`; supersedes WD-EX-v0.3 incl. R3 in-place edits, committed at `f05c7e4cd`, file sha256 `0f1058d7f0990e766b3effc3d3de24fc16383197874cced1f5b4212419cf018d`; WD-EX-v0.2 sha256 `50b7600de8503f51f440e5947ebd4ea7a559781e2497d5d880a8d683f7a9c43e`; WD-EX-v0.1 sha256 `69ac3dbfc5f97e2982418b918996df9b4a6abc674588c627e3e96fb4c133d55a`)
- Status: DRAFT DEFINITION — proposed, unsupplied, not implemented, not accepted
- Serves: OUT-001, OUT-002 (explanatory examples); OUT-004 (fixture subjects, designed only); REQ-001, REQ-002, REQ-003, REQ-004; VER-001…VER-004, VER-007
- Basis: repo 6e18505e3; ScopeOfWork.md sha256 080d7f5a8e55d93c06f51e5332b53954deb03e0877b1ee49be3011e3de14a294; PRD V4-WF-01…06, V4-HOST-05/06, V4-AUT-01/03/05, V4-EXE-01/03; HOST_INTEGRATION V4-HI-11, V4-HI-20…25, V4-HI-30…33, V4-HI-40…42, V4-HI-70/71; DECISION_BRIEF #d3, #d5; owner decisions `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` (D2, D3) and `-DECISION-2` (D5, D6; OWNER_DECISIONS.md at `f05c7e4cd` sha256 `a9869129753631b865cbbb00a138c0f497d5ac8a4b67f5746169d1f9a668ad2c`); Root `workflows/WORKFLOW_TEMPLATE.md`, `workflows/create-workflow/WORKFLOW.md`, `workflows/project-dag/execution.json`
- Consumed inputs: R4_RESOLUTIONS.md at `f05c7e4cd` sha256 `50a009b2ef487bad6ef5e89b5c4493095f18f83149fcb83b00050de485032a24` (R4-2, R4-3, R4-4, R4-5, R4-6, R4-7, R4-9, R4-12, R4-14, R4-18, R4-19, R4-20, R4-21); reviews/V2.md sha256 `75ba1dff8a0c4fa2eb294471127147cbd19a0925daf9169b32ddc88727dde6ef` (MAJOR-1; m-3, m-8, m-9, m-12, m-13); R3_RESOLUTIONS.md sha256 `202d52c7d688382336cddb0d6c31be27969a9e667c5800b734428a090f05afbf` (R3-1, R3-3, R3-4); R2_RESOLUTIONS.md sha256 `77cfb845ec305365f12218f83f332069155de5f362139b7a6fe2bf12cdebd088`; R1_RESOLUTIONS.md sha256 `2f9c7e72…77ec4`; IR1-A/B/C (items addressed to DEL-02-01). **Shared fixture:** DEL-03-01 C-v0.3 §10 FX-PIPE-01, read at `f05c7e4cd` (`CATALOG_AND_READ_BASIS.md` sha256 `ba45e7393ee0b16780f36605ddeecb95ba1f181488e36a46b4b495b69fd67c26`). **Siblings read at `f05c7e4cd`:** DEL-02-03 EXEC-v0.1 (`EXECUTION_COMPATIBILITY.md` sha256 `e0ede76ebf08003511755afc666be2466a867fd3256837ee94300cd0dfe518e8`); DEL-09-06 CA-v0.1 (`CONNECTED_ACTIVITY_CONTRACT.md` sha256 `685349b25981ca8333929207890514120d63753cdedd67ae0bad986fc5d45e62`, §3.2 L-CA-1). P §4.3/§9 terms as in P-v0.2/v0.3 (unchanged for these uses).
- Receivers: as WD-v0.4 (DEL-02-03, DEL-05-01, DEL-05-02, DEL-03-02, DEL-09-06, DEL-02-01 OUT-004 self-check; DEL-02-02 and DEL-02-04 in a later undertaking per D1)

## Changes from v0.3

Earlier change tables are in the committed WD-EX-v0.3 and v0.2 (hashes above).

| R4 ID (source) | Change |
|---|---|
| R4-18 (V2 MAJOR-1) | R-5a/R-5b re-pointed to C **V-CP1**; R-5c to C **T15/⟨set-2⟩** (class P-03, scope {FX-W1; {S-4}}). Local L-WDEX-2 and the "C's T15 covers labels only" statement removed. |
| R4-19 (V2 m-3) | OP-C10 class per R3-4: governed by the policy record of the operation whose receipt it reverses. |
| R4-19 (V2 m-8) | Framing stated: the E2 runs read the host workflow ⟨rev-3⟩ **as WD-EX declares it** (E1's checkpoints kept by adaptation). C §10 itself declares only V-CP1's `CP-accept` (FA-5); the meanings agree. |
| R4-19 (V2 m-12, m-13) | Re-pointed to C-v0.3 §10: FA-1…FA-5, OP-C10…OP-C12, T4a, T12's S-5, T16a, V-S1, V-CP1, V-NP1, V-R1, V-X1, V-OU1. "C-v0.3 to add" markers and the *unagreed ×3* divergence row closed. L-WDEX-1 kept (reason stated); L-WDEX-2 and the v0.3 local cases now covered by C (V-S1, V-R1, V-X1, V-NP1, V-OU1) removed; remaining local cases renumbered, each with its reason. |
| R4-20 (W9 CA F-5) | E1 adopts **optional OP-C12** host-check steps at Inspect and Re-examine and an output `host-check-result` (was DEL-09-06 L-CA-1). |
| R4-3 | R-4 shows the re-hold after resume and the withdrawn interim display. |
| R4-4 | R-12b shows "after run end" and a continuation run. |
| R4-5 | R-16 repaired against C's T15→T16 order (T15's A12 precedes the arrival: "prior act, not counted"); new R-9b. |
| R4-6 | R-16 covers established, pending, refused and lost-confirmation A12. |
| R4-7 | New R-6b (MX-3), R-7 (MX-6 "replaced"), R-13b (MX-8 via V-OU1). |
| R4-9 | E1d names its setting content (⟨set-2⟩ content); a variant naming none is invalid. |
| R4-2, R4-8, R4-21 | New **E8**: hold support per checkpoint and surface, App runs *not enforceable* pending D6; harness-capability kind (a). |
| R4-12 | R-9 (iv): elicitation answer is not act evidence. |
| R4-14 | R-5b records the constraint's carriage assurance. |

**Everything below is fixture subject material.** FX-PIPE-01, its rows,
values, people, revisions and runs are invented (C §10). Nothing here is a
SWBPIPE operation, catalog identity, receipt, human act or the selected first
connected operation (`UNRESOLVED{OI-021}`).

**Rendering note.** Declared parts are shown as Markdown tables for
readability. This is an illustrative rendering, not a selected carriage or
wire format (WD U-01, U-02). Revisions such as ⟨rev-A2⟩ are labels for
content identities whose algorithm is unselected (U-03).

**Fixture references (C-v0.3 §10).**

| Label | Meaning | Source |
|---|---|---|
| FA-1 | Every entry exposed on H, E and X (fixture assumption); non-exposure only via V-X1 | C §10.1 |
| FA-2 | A support row's subject content identity covers location, type, stiffness **and display label** | C §10.1 |
| FA-3 / FA-4 / FA-5 | Relied-on targets of an added support; ⟨set-1⟩ (P-03, *effective (policy default)*, propose) and ⟨set-2⟩ (after T15); V-CP1 declares `CP-accept` | C §10.1 |
| OP-C1 v1 / OP-C2 v1 | Read supports table / Read sustained-load results | C §10.2 |
| OP-C3 v1 | Examine support spacing — requester's **findings (A3)**, never "host checks passed" | C §10.2 |
| OP-C4 v1 / OP-C5 v1 / OP-C9 v1 | Add support / Set support stiffness / Set support label — class P-03, *may apply within granted autonomy* (DERIVED), default propose | C §10.2 |
| OP-C6 / OP-C7 / OP-C8 | Mark row checked (A4) / Accept items (A5) / Reject items (A10) — reserved to the person; the host act facility | C §10.2 |
| OP-C10 v1 | Undo (reverse a receipt); **governed by the policy record of the operation whose receipt it reverses** (R3-4) | C §10.2 |
| OP-C11 v1 | Renumber nodes; class **no policy basis** (reason pending OI-021) | C §10.2 |
| OP-C12 v1 | Run support-spacing **host check** ("host checks passed/failed: support spacing", evaluated basis) | C §10.2 |
| T1…T17, T4a, T16a, Tg | Timeline r12…r17 in g1; B1 = r12, B2 = r13; PR-1 (stale at T7, both items), PR-2 (lineage PR-1); RC-1 at T12 (S-5 created), RC-2 at T16, RC-3 reverses RC-2 at T17 | C §10.3 |
| V-S1, V-CP1, V-NP1, V-R1, V-X1, V-OU1 | Named variants | C §10.4 |
| `supports-adjust` ⟨rev-3⟩, run 12 | The host-origin workflow and run in C §10.1 | C §10.1; here the adaptation of E1 (E3) |
| ⟨fx-proj⟩ | App project library source root (local value label; C-v0.4 is to add an App-side library per R4-20) | This file |

**Framing (V2 m-8).** E2 reads runs of ⟨rev-3⟩ **as WD-EX declares it**:
the adaptation keeps E1's `CP-accept` and `CP-check`. C §10 declares no
checkpoint of its own except V-CP1's `CP-accept` (FA-5), which has the same
meaning.

---

## E1 — App-authored workflow `supports-adjust` (the origin of C's host workflow)

Authored in the Chirality App, reviewed and registered in the project library
(registration is DEL-02-02's; shown only as the resulting identity).

**Identity.** {kind *workflow*, origin *project*, source root ⟨fx-proj⟩, name
`supports-adjust`, revision ⟨rev-A2⟩}; derived-from *none*. Its host
adaptation is C §10.1's ⟨rev-3⟩ (E3). In WD-EX-v0.4 the fixture content of
⟨rev-A2⟩ includes the optional OP-C12 steps (R4-20; formerly DEL-09-06
L-CA-1).

**`WORKFLOW.md` — front matter and prose (illustrative).**

```markdown
---
name: supports-adjust
description: On one piping run with a support-spacing exceedance, examine the
  spacing (and, where the host offers it, run the host's spacing check),
  propose support changes as one proposal with one item per change, wait for
  the engineer to accept or reject each item, re-examine after application,
  and ask the engineer to mark the changed support rows checked.
---
# Adjust supports for a spacing exceedance

Use this when the engineer names a run and a spacing limit, and wants an
exceedance resolved by adding supports or changing support stiffness.

## Inspect
Read the run's supports table on the current model revision and keep its read
basis. Examine the support spacing against the stated limit. Your findings are
an examination, not the engineer's Checked mark and not a host check. If the
host offers its named support-spacing check, run it too and report its result
as the host states it. If neither shows an exceedance, stop and say so.

## Propose
Draft one proposal, one change item per support added or changed, showing old
and new values, affected rows and why, relying on the basis you read. It is
queued until the engineer accepts or rejects each item; never describe it as
approved. If the host refuses it as stale, re-read and re-draft a new
proposal on the current basis; never retarget the old one.

## Wait for acceptance  [checkpoint CP-accept]
The engineer accepts or rejects each item in the host's own proposal view. If
all items are rejected, return to Propose once with the engineer's reason, or
stop if they ask. If some are accepted and some rejected, continue with the
accepted items and report the rejected ones.

## Re-examine
After the host applies the accepted items, re-read the supports table,
examine the spacing again and, where offered, re-run the host check. Report
your findings and the host result by reference.

## Ask for the Checked mark  [checkpoint CP-check]
Ask the engineer to mark the support rows the application changed as checked,
in the host. If they decline, stop and report.

## Return
Summarize what changed (receipt references), your findings, any host check
result, which acts the engineer performed, and what is unknown.
```

**Declared part (illustrative rendering).** *Declaration contract version:*
WD-v0.4 (fixture).

*Expected inputs*

| input name | meaning | kind | necessity | quality/basis requirement | stage |
|---|---|---|---|---|---|
| `run` | The run the engineer wants resolved (e.g., R-100) | person-supplied choice | required | One run in the workspace | Inspect |
| `spacing-limit` | The spacing limit to examine against | person-supplied value | required | Stated with units | Inspect |
| `supports-table` | Current supports on the run | host read via OP-C1 | required | Complete five-element read basis; per-row subject content identities | Inspect, Re-examine |

*Required tools*

| tool reference | class | purpose of use | necessity | version compatibility | stage |
|---|---|---|---|---|---|
| OP-C1 | host operation | read supports on the run | required | v1 | Inspect, Re-examine |
| OP-C3 | host operation | examine spacing against the limit (A3 findings) | required | v1 | Inspect, Re-examine |
| OP-C12 | host operation | run the host's named "support spacing" check | optional (fallback: examination only; report "host check not run") | v1 | Inspect, Re-examine |
| OP-C4 | host operation | propose added supports. **Governing checkpoint constraint** {run, `CP-accept`, A5, OP-C4}, recorded with its carriage assurance (WD §4.2.2) | required | v1 | Propose |
| OP-C5 | host operation | propose stiffness changes. Constraint {run, `CP-accept`, A5, OP-C5} | optional (fallback: propose added supports only) | v1 | Propose |

OP-C6/OP-C7/OP-C8 are not required tools: they are the person's act facility
and reserved to the person.

*Checkpoints*

| checkpoint | act | reached-when | subject class | scope | purpose | actor | on negative decision | on mixed decision | expected act evidence |
|---|---|---|---|---|---|---|---|---|---|
| `CP-accept` | A5 accept | (c) observed host outcome *queued* for the proposal this run submits with OP-C4/OP-C5 items | change items of the named proposal (that queued proposal) | per item; one A5 may list several items | engineer decides whether each support change goes into the model | the person | all items A10: return to Propose once, else stop | continue with accepted items; report rejected items | host act record (OP-C7/OP-C8 capture) with capture-evidence reference, captured at or after arrival |
| `CP-check` | A4 mark checked | (b) observed production of output `examination-report` | objects changed by a named outcome: the objects the **applied (receipt)** outcomes of `CP-accept`'s items identify | those objects | engineer records their own checking of the changed supports | the person | act-declined event: stop and report | — | host act record (OP-C6 capture) with capture-evidence reference, bound to each object's post-application subject content identity, captured at or after arrival |

Not declared: A6 *approve* (engineering approval) and A7 *rely*. Reliance on
the model belongs to the accountable professional outside this workflow
(V4-AUT-05).

*Returned outputs*

| output | meaning | form | destination | promised standing | gating checkpoint |
|---|---|---|---|---|---|
| `adjustment` | the support changes | host change via proposal (V4-HI-23) | host supports table | *queued*; per accepted item *applied (receipt)* after host application | `CP-accept` |
| `examination-report` | spacing findings after application | report citing OP-C3 results and the OP-C1 basis by reference | conversation + host results view | *agent-examined (non-mutating)* — A3 findings | — |
| `host-check-result` (optional) | the host's named spacing check, before and after | host result by reference (OP-C12) | host results view | as the host states it: "host checks passed: support spacing" or "host check failed: support spacing", each with evaluated basis | — |
| `checked-rows` | the engineer's A4 on the changed rows | human-act standing | host supports table | *marked checked by the person*, conditional on `CP-check`; shown *lapsed* for affected rows if `CP-check` re-holds (WD I-4) | `CP-check` |
| `summary` | what changed, acts performed, unknowns | message | conversation | *agent-prepared* | — |

*Returned evidence*

| evidence | kind | supports |
|---|---|---|
| `EV-basis` | relied-on read basis (e.g., B1, B2) | `adjustment` |
| `EV-receipt` | host receipt reference per applied item (link, not copy) | `adjustment` |
| `EV-exam` | OP-C3 result reference (A3 findings) with evaluated basis | `examination-report` |
| `EV-host-check` | OP-C12 result reference with evaluated basis (T4a) | `host-check-result` |
| `EV-accept-act` | human-act record references, A5/A10 per item, with capture-evidence references | `CP-accept` only |
| `EV-checked-act` | human-act record references, A4 per object, with capture-evidence references | `CP-check` only |

*Compatible roles:* TASK, WORKING_ITEMS (fixture choice; host seat per WD §5
and U-09). *Tool restriction:* none declared.

## E1b — Review-only workflow (demonstrates I-3)

{workflow, project, ⟨fx-proj⟩, `spacing-review`, ⟨rev-B1⟩}. Method: read
OP-C1, examine with OP-C3, produce output `findings`, and ask the engineer to
mark the examined rows checked. No proposal is ever made.

| checkpoint | act | reached-when | subject class | on negative decision |
|---|---|---|---|---|
| `CP-review` | A4 mark checked | (b) observed production of `findings` | objects a named output concerns: the rows `findings` identifies, bound through their subject content identities as read (R3-1) | act-declined event: stop |

Along T3–T4 the findings name the span S-2→S-3, so `CP-review` binds S-2 and
S-3 through ⟨S-2@r12⟩ and ⟨S-3@r12⟩ from B1 (R3-1, INTEGRATION).

## E1c — Direct application with a later A4 (supports R-5c)

{workflow, project, ⟨fx-proj⟩, `supports-label`, ⟨rev-C1⟩}: labels a support
with OP-C9. **No** A5 checkpoint, so OP-C9 carries no governing checkpoint
constraint and its treatment follows the grant in force.

| checkpoint | act | reached-when | subject class |
|---|---|---|---|
| `CP-check` | A4 mark checked | (c) observed host outcome *applied (receipt)* of OP-C9 | objects changed by a named outcome (the OP-C9 receipt) |

By FA-2 a support's subject content identity covers its display label, so an
A4 bound after the label change lapses when the label changes again (R-17).

## E1d — Grant checkpoint (supports R-16)

{workflow, project, ⟨fx-proj⟩, `label-with-grant`, ⟨rev-D1⟩}: as E1c, plus

| checkpoint | act | reached-when | subject class | declared setting content (R4-9) |
|---|---|---|---|---|
| `CP-grant` | A12 set grant | (a) before dispatch of OP-C9 | grant setting | class P-03; grant value *direct*; scope {model/workspace FX-W1; object set {S-4}} (the content of ⟨set-2⟩) |

A variant of `CP-grant` naming no setting content is **invalid** (WD FB-17).

---

## E2 — Run readings along the FX-PIPE-01 timeline

The runs read ⟨rev-3⟩ (E3) in FX-W1, run 12, with Engineer A, in the host
(embedded loop), unless another workflow or surface is named. "Observed"
facts are C's timeline or a named variant; local cases are `L-WDEX-n` with a
reason. Dispositions use WD §4.3.4; outcomes P §9. Every act counts only if
captured at or after its arrival (WD I-8).

| Run | Steps | Invented observed facts | `CP-accept` | `CP-check` | `adjustment` | Incompatible reading exposed |
|---|---|---|---|---|---|---|
| R-1 success only | T10 | PR-2 validated → *queued*; no act record | waiting (arrival 2, bound to PR-2 items 1, 2) | not reached | items 1, 2 *queued* | "accepted" or "applied" inferred from success (I-2) |
| R-2 mixed | T11–T12, then re-examination | Engineer A accepts item 1 (OP-C7; A5) and rejects item 2 (OP-C8; A10); host applies item 1 → RC-1 (r14), S-5 created, R-100 changed; agent re-reads OP-C1, runs OP-C3 → `examination-report` | **resolved negatively**, annotated "partial: item 1 A5, item 2 A10"; on-mixed path: continue with item 1 | waiting; bound to S-5 and R-100 via ⟨S-5@r14⟩, ⟨R-100@r14⟩ | item 1 *applied (RC-1)*; item 2 *rejected* | showing `CP-accept` as performed or "all accepted"; withholding item 1's application |
| R-3 both accepted | L-WDEX-1 (variant of T11: one A5 lists items 1 and 2 — needed because C's T11 rejects item 2) | Host applies both → receipt L-WDEX-1-RC changing S-5 (created) and S-3 | **performed** (A5 not lapsed by application) | waiting; bound to S-5, R-100 and S-3 | items 1, 2 *applied* | `CP-check` treated as satisfied by acceptance (I-1) |
| R-4 lapse and re-hold | L-WDEX-1 continued; T14 as control | Engineer A marks the bound rows checked (OP-C6; A4) → `CP-check` performed. Then Engineer A edits S-3: (i) before the loop's resume point; (ii) after resume, while the agent is writing `summary`; (iii) after the run ended. Control: T14 edits S-2 (not bound here) | performed (never re-held, R4-3) | (i) **waiting — lapsed at ‹t›**; (ii) **waiting — re-held, lapsed at ‹t› after resume**: the run stops at its next action, `summary` drafting done so far stays recorded, `checked-rows` shows *lapsed* for S-3, the A4 is requested again for the whole scope with S-3 marked; (iii) **lapsed** for S-3 only; control: unchanged | applied | carrying A4 onto edited S-3; the withdrawn "performed + act-lapsed" display; undoing actions already taken; re-holding `CP-accept` |
| R-5a forced proposal | C V-CP1 | Variant T15 grants *direct* for P-03 on R-100 and its supports; `CP-accept` declared (FA-5). After R-5b's refusal the agent submits OP-C4 as a proposal | waiting on the queued proposal | not reached | *queued* | direct application under the grant (D2: no grant widens past a declared checkpoint) — **AWAITING INPUT** (U-19) |
| R-5b direct request | C V-CP1 | The agent requests OP-C4 directly in run 12; constraint {run 12, `CP-accept`, A5, OP-C4} recorded with its carriage assurance (host-held or App-assured; *model-supplied* alone would not satisfy R2-12) | not reached (nothing queued) | not reached | **not permitted**, naming the governing checkpoint constraint; nothing applied | silent conversion into a proposal (R-3.3; R2-12) — **AWAITING INPUT** |
| R-5c direct then A4 | C T15–T16, T16a, with E1c | ⟨set-2⟩: P-03 *direct*, scope {FX-W1; {S-4}}, effective. Agent applies OP-C9 directly (S-4 label "G-4") → RC-2, origin mark, undo route. T16a: Engineer A marks S-4 checked | — (none declared) | waiting from RC-2's *applied* outcome; **performed** by T16a (captured after arrival) | *applied (RC-2)*, direct under ⟨set-2⟩ | treating the direct application or RC-2 as A4 |
| R-6 interruption before queue | L-WDEX-3 (C has no loss before *queued*) | PR-2 submitted; the loop loses observation before any host outcome | **unknown** (the deciding observation was lost) | not reached | **outcome unknown**, reporter: the loop | reporting queued, applied or failed without observation (S-K) |
| R-6b lost decision | L-WDEX-4 (variant of T11: item 1 A5 observed; item 2's decision observation lost) | Host later reports nothing observable for item 2 | **unknown** (MX-3), item 2 annotated unknown | not reached | item 1 accepted; item 2 last observed *queued* | resolving the checkpoint from item 1 alone |
| R-7 stale then re-draft | T5–T10 | PR-1 relies on B1; T6 edit of S-3 (r13); T7 PR-1 both items **refused — stale** (relied B1, current B2); T9 PR-2 (lineage PR-1); T10 PR-2 *queued* | PR-1 never reached *queued*, so no arrival until T10; arrival at T10 binds PR-2's items | not reached | PR-1 refused — stale; PR-2 *queued* | retargeting PR-1; binding `CP-accept` to PR-1 |
| R-7b all items left, replaced | L-WDEX-16 (C has no withdrawal of a queued proposal): after T10 the agent withdraws PR-2 (A11) before any decision, re-reads and submits a new proposal (local label L-WDEX-16-P) that is *queued* | Arrival 2 (PR-2): both items leave → **waiting** "no items remain"; at the new *queued*, arrival 2 is closed "replaced by arrival 3" (final *waiting*) and arrival 3 binds the new items (MX-6) | not reached | PR-2 withdrawn; new proposal *queued* | treating arrival 2 as resolved or performed; carrying any decision across proposals |
| R-7′ run ends early | L-WDEX-5 (run stops after T7) | Run-ended event before any re-draft | **not reached** | not reached | PR-1 refused — stale | reporting `CP-accept` as satisfied |
| R-8 wrong subject | L-WDEX-6 (a second proposal outside this run) | After T10, Engineer A accepts an item of the L-WDEX-6 proposal | waiting | not reached | PR-2 *queued* | counting an A5 on other content (SB-2) |
| R-9 capturing surface | T11 | (i) The agent writes "Engineer A accepted item 1". (ii) Engineer A's A5/A10 captured by the host facility (OP-C7/OP-C8) with a capture-evidence reference; the App faithfully records it, citing that reference. (iii) As (ii), but the host exposes no capture-evidence reference. (iv) The App's Codex asks through an MCP elicitation "accept item 1?" and Engineer A answers yes | (i) waiting; (ii) resolved negatively as R-2; (iii) waiting (U-05b); (iv) waiting | — | as R-2 in (ii) | (i) resuming on an agent-authored record; (iii) resuming without capture evidence (I-5); (iv) treating an elicitation answer as A5 (R4-12) |
| R-9b prior act | T2 with E1b variant L-WDEX-7 (`CP-review` binding S-2) | T2's A4 on S-2 (r12) was captured before `CP-review` arrives at T4 | — | `CP-review`: S-2 "prior act on this subject, not counted"; **waiting** until a new A4 after arrival (I-8); if T2's order against the arrival cannot be established, "act order unknown" | — | counting T2's A4 at an arrival it did not answer |
| R-10 reserved call | C V-R1 | The agent calls OP-C6 on S-1 | — | — | — | OP-C6 by the agent → **not permitted** (reserved, P-02); an A8 request is *offered*, not recorded unless issued (R2-4); treating the attempt as A4, *not exposed* or *unavailable* |
| R-11 all rejected | L-WDEX-8 (variant of T11 rejecting both items) | A10 on items 1 and 2 | **resolved negatively**; on-negative path: return to Propose once (a later *queued* is a new arrival) | not reached | items *rejected* | counting A10 as performed |
| R-12 act declined | after R-2 | Engineer A declines to mark the bound rows checked → act-declined event with capture evidence | as R-2 | **resolved negatively** (not an A4); on-negative path: stop | as R-2 | recording the decline as A4 |
| R-12b run end and continuation | after R-2; continuation L-WDEX-9 | Engineer A stops the run while `CP-check` waits → run-ended event. Later Engineer A marks S-5 checked. Then Engineer A starts a new run that records *continues ⟨run 12⟩* | as R-2 | run 12: final **waiting** with run-ended event; the later A4 shown **"after run end"**, changing nothing. Continuation: `CP-check` *not reached* until its own arrival; the earlier A4 is "prior act, not counted" there (I-8) | as R-2 | resuming run 12; carrying any arrival or act into the continuation |
| R-13 retry | T13 | Acknowledgment of RC-1 lost; agent resubmits PR-2 (same identity) | unchanged | unchanged | de-duplicated by identity first: the repeat reports RC-1, never refused stale by its own effect; if unobservable, **outcome unknown** by the observer (R2-13) | a second application; a stale refusal caused by RC-1 |
| R-13b application outcome lost | C V-OU1 | Neither T12 nor T13 report observed | unchanged (decided), item 1 annotated "accepted — application outcome unknown (observer loop)" (MX-8) | not reached for item 1's objects | item 1 **outcome unknown**, last observed *accepted* | re-holding `CP-accept`; inferring application |
| R-14 accepted, then stale | C V-S1 | After T11, Engineer A edits S-2 before T12 (r14′); item 1 (relies on S-2) refused at application — stale | unchanged (decided; MX-7) | not reached for item 1's objects (no applied outcome) | item 1 "accepted by Engineer A — not applied: refused — stale (relied B2, current ⟨B-r14′⟩)"; A5 not lapsed | calling this a lapse of A5; showing item 1 as applied or merely "accepted" |
| R-15 tool permission (App) | L-WDEX-10 (App-side run through the external surface) | The user's Codex mode auto-answers a tool permission (A14) for a shell command | unchanged | unchanged | unchanged | treating A14 as any checkpoint act (D3) |
| R-16 A12 rules | E1d along C T15–T16; L-WDEX-11 for (ii)–(v) | (i) **C order:** T15's A12 (⟨set-2⟩) is captured before `CP-grant` arrives when the agent is about to dispatch OP-C9 at T16. (ii) After arrival, Engineer A performs A12 with the declared setting content; the control **establishes** it. (iii) Later, an established A12 narrows the scope. (iv) Instead of (ii), the A12 is **refused** by the control. (v) Instead of (ii), the A12 is **pending**, then its confirmation observation is lost | — | `CP-grant`: (i) **waiting**, "prior act on this subject, not counted" (I-8); the held OP-C9 call stays undispatched. (ii) **performed**; the held call is dispatched unchanged. (iii) stays **performed**, "superseded by ‹act›". (iv) **waiting**, "A12 refused by control: ‹reason›"; ⟨set-2⟩ stays in force, not superseded. (v) **waiting** "awaiting control confirmation", then **unknown** | (ii): RC-2 as T16 | counting T15's A12 at a later arrival; counting or superseding with a refused A12 |
| R-17 undo | T16–T17 with E1c | T16a: Engineer A marks S-4 checked after RC-2; run ends; T17 undo RC-3 *reverses RC-2* (OP-C10, governed by P-03 per R3-4) | — | **lapsed** (run ended; FA-2 covers the label) | RC-2 applied, then reversed by RC-3 | treating the undo as leaving the A4 intact (R2-15) |
| R-E1b independent A4 | E1b, T3–T4 | OP-C1 read (B1); OP-C3 findings name S-2→S-3; `findings` produced; Engineer A marks S-2 and S-3 checked in the host (OP-C6 capture) after the arrival | — | `CP-review` **performed** | — | requiring a prior A5 (I-3) |
| R-E1b′ binding | E1b, T3–T6 (L-WDEX-12: variant marking only the findings, then T6) | (i) Engineer A marks the `findings` output checked, not the rows. (ii) After R-E1b, T6 edits S-3 before the run resumes | — | (i) `CP-review` **waiting** (wrong referent, SB-2); (ii) act-lapsed event for S-3 → **waiting — lapsed at ‹t›**; S-2 still bound | — | binding to the output's own content; lapsing S-2 on an S-3 edit |

---

## E3 — Carried into a host, unadapted and adapted

E1 is carried into the fixture host's workflow library ⟨fx-root⟩ by the
DEL-02-03 carriage procedure (EXEC §6.3 TR-1…TR-8).

| | Original in App project | Carried **unadapted** | **Adapted** (C §10.1) | Reopened in App after refinement |
|---|---|---|---|---|
| kind | workflow | workflow | workflow | workflow |
| origin | project | **project** (unchanged, R-9) | **host** | host (opening does not change it) |
| source root | ⟨fx-proj⟩ | ⟨fx-proj⟩ | ⟨fx-root⟩ | ⟨fx-root⟩ |
| name | `supports-adjust` | same | same | same |
| revision | ⟨rev-A2⟩ | ⟨rev-A2⟩ (recomputed on receipt; else "revision not verified", EXEC TF-1) | ⟨rev-3⟩ | a refinement is a DEL-02-02 draft until reviewed and registered; the host copy stays ⟨rev-3⟩ |
| derived-from | none | none | {workflow, project, ⟨fx-proj⟩, `supports-adjust`, ⟨rev-A2⟩} | {workflow, host, ⟨fx-root⟩, `supports-adjust`, ⟨rev-3⟩} if registered as a new App workflow |
| holding library (listed/selected/resolved; not identity; confirmed EXEC §6.2) | ⟨fx-proj⟩ | ⟨fx-root⟩ (received link); ⟨fx-proj⟩ at the exported link | ⟨fx-root⟩ | App library where registered |

Adaptation in ⟨rev-3⟩ (fixture): `spacing-limit` becomes optional with the
fallback "use the host project's stated limit"; the prose refers to the
host's own proposal view by name. Checkpoint names, act kinds, reached-when
conditions and subject classes are unchanged, so each is **preserved** with a
derived-from checkpoint link (EXEC AD-2, AD-4). Runs of ⟨rev-A2⟩ and ⟨rev-3⟩
never share acts or dispositions (EXEC AD-5).

---

## E4 — Same-name collision in the host library

After E3, ⟨fx-root⟩ holds two workflows named `supports-adjust`: the unadapted
copy {…, project, ⟨fx-proj⟩, …, ⟨rev-A2⟩} and the adapted {…, host,
⟨fx-root⟩, …, ⟨rev-3⟩}.

| Step | Discovery shows | Selection holds | Required consumer behavior |
|---|---|---|---|
| 1 | Two entries, each with origin and holding library ⟨fx-root⟩; collision reported | Engineer A explicitly selects host ⟨rev-3⟩ | Both origins listed with holding library (C-1); the panel shows "project-origin, held in ⟨fx-root⟩" for the copy. |
| 2 | A user-library copy ⟨rev-U1⟩ appears in the App | unchanged | Three origins listed; no rebinding despite Root ordering (C-2, C-5). |
| 3 | The host library registers ⟨rev-4⟩ of the host workflow | ⟨rev-3⟩ selected; whether the run follows ⟨rev-4⟩ is host/DEL-02-02 policy (U-10) | The chain shows which revision was resolved and supplied (C-4); replay reads the revision recorded for the run (EXEC RP-5). |
| 4 | Engineer A explicitly reselects the project-origin copy | {…, project, ⟨fx-proj⟩, …, ⟨rev-A2⟩}, held in ⟨fx-root⟩ | New selection event, not a rebinding (C-3). Identity equality ignores the holding library (C-6). |

---

## E5 — A Root prose-only workflow read under v4 (real bytes, repo 6e18505e3)

Root's bundled `create-workflow` has front matter `name`/`description`,
prose, and no `execution.json` or declared part.

| Category | Reading |
|---|---|
| Expected inputs, outputs, evidence | **undeclared** |
| Required tools | **undeclared** → check **not established**; selectable, never "runnable" by check |
| Checkpoints | **undeclared**. The prose's human review before registration is not product-held: it has no reached-when, subject class or act kind. A consumer may report the prose (FB-07 style) but shall not synthesize a checkpoint. |
| Identity | {workflow, bundled, `chirality-root`, `create-workflow`, revision per U-03} |

---

## E6 — Root restriction misread as requirement (negative fixture)

Root `workflows/project-dag/execution.json` (repo 6e18505e3) declares
`compatible_roles: [WORKING_ITEMS]` and `tools.capabilities: [read, write,
bash, delegate_agent, report_coordination_notice, send_agent_update,
ack_agent_update]`.

| Reading | Verdict |
|---|---|
| "The workflow requires these seven tools; check them against the host" | **Incompatible.** They are a restriction ceiling, not V4-WF-01 required host tools (WD §4.2.3). |
| "Required tools undeclared; restriction retained; compatible role WORKING_ITEMS; a host seat without delegation reports **unsupported**" | **Compatible** (FB-05; WD §4.7). |

---

## E7 — Compatibility outcomes and the pass rule (FA-1 base)

| Case | Situation | Outcome per requirement | Pass? |
|---|---|---|---|
| Base | E1 ⟨rev-3⟩ on the embedded surface: OP-C1, OP-C3, OP-C4, OP-C5, OP-C12 exposed (FA-1) | all **present** | passes on requirements (hold support: E8) |
| L-WDEX-13 (no C entry is absent) | OP-C4 absent from the catalog edition | OP-C4 **missing** | does not pass (required) |
| L-WDEX-13b | OP-C12 absent | OP-C12 **missing** | passes (optional; "host check not run" shown) |
| C V-X1 | E1c on the external surface X: OP-C9 element 9 = *not exposed on this surface* | OP-C9 **not exposed on this surface** | does not pass on X; unaffected on E |
| C §10.6 (T8) | A workflow requiring OP-C2, checked at r13 | OP-C2 **present, currently unavailable** ("No current solve for LC-1 at this revision", basis B2) | passes; shown as a run-time hold with the reason |
| External access off | Any workflow on X while A13 is not performed: the App reports **channel not enabled** if its own configuration is off, the host if the host channel is off (R4-16) | **channel not enabled** for every requirement on X | does not pass on X; never shown as missing |
| C V-NP1 | A workflow requiring OP-C11 (*no policy basis*, pending OI-021) | OP-C11 **present**; direct is *not permitted*, proposing confers no permission (R2-9) | passes the requirement check; dependent production reported **held** |
| E5 reading | Root prose-only package | **not established** (undeclared) | selectable; never "runnable" by check |

---

## E8 — Hold support per checkpoint and surface (R4-2, R4-8, R4-21)

The compatibility report (DEL-02-03 EXEC §3.6) states hold support for each
checkpoint on the acting surface (WD §4.3.8).

| Workflow / surface | Checkpoint | Hold support | Workflow result |
|---|---|---|---|
| E1 ⟨rev-3⟩, embedded host loop (E) | `CP-accept` (A5, kind (c)) | **enforced on the host route** — AWAITING INPUT (U-19) | passes on requirements; AWAITING INPUT shown |
| | `CP-check` (A4, kind (b)) | **held after observation** by the host loop (DEL-05-01) | — |
| E1 ⟨rev-A2⟩ run from the App via X (L-WDEX-14) | `CP-accept` | **enforced on the host route** (if the host evaluates the constraint; AWAITING INPUT) | — |
| | `CP-check` | **not enforceable**: App-side holds are `UNRESOLVED{D6}`; neither interposed App code (HP-1) nor `turn/interrupt` (HP-2) is relied on | **unsupported** — "checkpoint hold not enforceable on this surface: CP-check"; check does not pass. If Engineer A runs it anyway, each arrival records "hold not enforceable" and, e.g., a file Codex writes while `CP-check` waits is recorded as **action during hold** |
| E1d from the App via X | `CP-grant` (A12, kind (a) on host operation OP-C9) | **not enforceable** (no adopted App hold point before dispatch, D6) | **unsupported** |
| L-WDEX-15: a workflow whose checkpoint is kind (a) before a Codex **harness capability** (e.g., a shell command), App run | that checkpoint | **not enforceable** (R4-21; tools the user's mode auto-settles never reach the App) | **unsupported** (WD FB-18) |
| Any of the above | — | HP-3 (an App named-rule *decline* of a tool-permission request that reaches the App) may be used as a best effort under D3; it does not make a hold *enforced* | — |

---

## UNRESOLVED

Same register as WD-v0.4 §12. Items that shape these examples:

| item | owner | point of need | effect on these examples |
|---|---|---|---|
| U-01/U-02 carriage and wire names | DEL-02-01 with consumers | before OUT-002 schema / OUT-004 fixtures | Tables are illustrative renderings |
| U-03 revision algorithm | DEL-02-01 with DEL-04-03 | before revision comparisons | ⟨rev-A2⟩, ⟨rev-3⟩ are labels |
| U-30 App-side holds `UNRESOLVED{D6}` (SWBPIPE SQ-02) | Owner after the SWBPIPE answer | before any App-run hold is claimed | E8 App rows *not enforceable* / unsupported |
| U-19 constraint carriage assurance on the host route (SQ-02) | host owner via W9; DEL-03-02 element | before host-side fixtures | R-5a/R-5b and E8 `CP-accept` rows **AWAITING INPUT** |
| U-05b capture-evidence reference (relay) | host owner via W9 | before host act-recording integration | R-9 (iii) stays waiting |
| U-31 capture after arrival vs counting prior acts | Owner with DEL-02-01, DEL-04-01 | before hold-machine fixtures run | R-9b, R-12b, R-16 (i) apply I-8 as PROPOSED |
| U-05c multi-row A4 purpose after partial lapse | DEL-04-01 with Owner (C1) | at its point of need | R-4 re-requests the whole scope, valid under every option |
| U-25 App act control construction | DEL-01-04 (later) | before App capture fixtures | App-side positive capture not shown |
| U-09 host seat role mapping | DEL-02-01 with SWB owner and DEL-02-04 | before host role guidance | E1 compatible roles are a fixture choice |
| U-10 precedence and revision following | DEL-02-02 with host owner | before host-origin discovery | E4 step 3 left open |
| U-15 / U-05 `UNRESOLVED{OI-021}` | owner via outside SWB session | before connected-activity SoW | FX-PIPE-01 entries are not the selected operation; OP-C11's reason cites it |
| App-side library and App-file subject in C | DEL-03-01 (C-v0.4, R4-20) | C-v0.4 | ⟨fx-proj⟩ stays a local value label |

## Verification cases

These examples are inputs for WD-v0.4 §13; none has been run.

| Example | Used by | Expected result summary | VER |
|---|---|---|---|
| E1 | VC-01, VC-03, VC-05, VC-29, VC-30 | Categories incl. subject class and optional OP-C12 recovered; references compared to C §10; invalid A5 variants rejected; `CP-check` binds applied objects | VER-001, VER-002, VER-003 |
| E1b | VC-08, VC-36 | A4 performed without any A5; binding to the examined rows | VER-003 |
| E1c + E2 R-5a/b/c | VC-11 | AWAITING INPUT (host side) for V-CP1; R-5c designed on T15–T16a | VER-003 |
| E1d + E2 R-16 | VC-32, VC-41 | Prior act not counted; established/pending/refused/lost; supersession; FB-17 variant | VER-003 |
| E2 R-1, R-2, R-3, R-4, R-6, R-6b, R-7, R-7b, R-7′, R-8, R-9, R-9b, R-10, R-11, R-12, R-12b, R-13, R-13b, R-14, R-15, R-17 | VC-07, VC-24, VC-09, VC-10, VC-15, VC-40, VC-20, VC-40, VC-20, VC-21, VC-22/VC-42, VC-39, VC-16, VC-23, VC-23, VC-31, VC-34, VC-40, VC-27, VC-28, VC-35 | Only evidenced acts counted; shared dispositions, annotations and events as tabulated; unknown stays unknown | VER-003, VER-004 |
| E3 | VC-02, VC-14, VC-26 | Unadapted keeps origin; adapted has derived-from; holding library separate | VER-001, VER-004 |
| E4 | VC-13 | No rebinding; all origins with holding library | VER-004 |
| E5 | VC-04 | All categories undeclared; no synthesized checkpoint | VER-002 |
| E6 | VC-06 | Restriction not read as requirement | VER-002 |
| E7 | VC-25, VC-33 | Distinct outcomes; pass rule | VER-002 |
| E8 | VC-37, VC-38 | Hold support per surface; App runs unsupported pending D6; no App hold claimed | VER-001, VER-003 |
| Inventory | VC-19 | Examples identified by WD-EX-v0.4; all DESIGNED, AWAITING INPUT or HELD | VER-007 |
