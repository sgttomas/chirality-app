# Portable workflow declaration — readable examples
- Contribution: DEL-02-01/WD-EX-v0.2 (companion to DEL-02-01/WD-v0.2, `WORKFLOW_DECLARATION.md`; supersedes WD-EX-v0.1, file sha256 `69ac3dbfc5f97e2982418b918996df9b4a6abc674588c627e3e96fb4c133d55a`)
- Status: DRAFT DEFINITION — proposed, unsupplied, not implemented, not accepted
- Serves: OUT-001, OUT-002 (explanatory examples); OUT-004 (fixture subjects, designed only); REQ-001, REQ-002, REQ-003, REQ-004; VER-001…VER-004, VER-007
- Basis: repo 6e18505e3; ScopeOfWork.md sha256 080d7f5a8e55d93c06f51e5332b53954deb03e0877b1ee49be3011e3de14a294; PRD V4-WF-01…06, V4-HOST-05/06, V4-AUT-01/03/05, V4-EXE-03; HOST_INTEGRATION V4-HI-11, V4-HI-20…25, V4-HI-30…33, V4-HI-40…42, V4-HI-70/71; DECISION_BRIEF #d3, #d5; owner decision `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` (D2, D3); Root `workflows/WORKFLOW_TEMPLATE.md`, `workflows/create-workflow/WORKFLOW.md`, `workflows/project-dag/execution.json`
- Consumed inputs: R1_RESOLUTIONS.md (sha256 `2f9c7e72aa8362624ad830377a70077b27a27bf03871f8e87811a28e6e177ec4`) R-1, R-3, R-4, R-5, R-6, R-7, R-9; V1-A.md and V1-C.md items addressed to DEL-02-01. The shared fixture FX-PIPE-01 and its entries are DEL-03-01 §10's, per R1_RESOLUTIONS R-9; to be confirmed at IR1 (C v0.2 not read). Act names A1–A14 per R-1; P §9 outcomes per R-7; content identities per R-6.
- Receivers: as WD-v0.2 (DEL-02-03, DEL-05-01, DEL-05-02, DEL-02-01 OUT-004 self-check; DEL-02-02 and DEL-02-04 in a later undertaking per D1)

## Changes from v0.1

| V1 item | Change |
|---|---|
| V1-B D-20, R-9 | Re-labelled to the shared fixture FX-PIPE-01 (DEL-03-01 §10). The workflow now adds a support through OP-C4 "Add support" and checks with OP-C3 "Check support spacing", so it uses catalogue entries known from R1/V1 text. The v0.1 spring-rate adjustment and stress-results read are dropped. Read-entry and row identifiers not stated in R1/V1 text are placeholders (U-26). |
| V1-C D-01 (R-5) | Every checkpoint has a **reached-when**. |
| V1-C D-02 (R-5, R-6) | Every checkpoint subject is a run-observable referent class. |
| V1-A D-01, V1-C D-17 (R-1) | Canonical act names A4/A5/A10 used; "Not declared" line now names A6 *approve* and A7 *rely*. |
| V1-A D-12 (R-4) | "agent-checked" → "agent-examined (non-mutating)"; host results "host checks passed: ‹named checks›". |
| V1-A D-09, V1-C D-07 (R-5, R-3) | E2 R-5 rewritten as R-5a/R-5b/R-5c; new variant E1c. |
| V1-A D-10, V1-C D-03/D-04 (R-5) | Dispositions use the shared vocabulary; negative decisions shown separately (R-11, R-12). |
| V1-A D-11, V1-C D-06 (R-5) | Capturing-surface evidence shown (R-2, R-9). |
| V1-C AB-01 (R-6) | Mixed item decisions (R-13). |
| V1-C D-05 (R-5) | Lapse after passing the checkpoint recorded; re-hold left to DEL-02-03 (R-4). |
| V1-C D-09 (R-9) | New E7 for exposure outcomes. |
| V1-C D-10 (R-9) | E3 adds the carried-unadapted case. |
| V1-A §5 (D2) | New R-10: agent attempt at A4 through OP-C6 is not permitted. |

**Everything below is fixture subject material.** The model FX-PIPE-01, its
rows, values, people, revisions and runs are invented. Nothing here is a
SWBPIPE operation, catalog identity, receipt, human act or the selected first
connected operation (`UNRESOLVED{OI-021}`).

**Rendering note.** Declared parts are shown as Markdown tables for
readability. This is an illustrative rendering, not a selected carriage or
wire format (WD U-01, U-02). Revisions such as `rev A2` are labels for
content identities whose algorithm is unselected (U-03).

**Fixture references (per R1_RESOLUTIONS R-9; to be confirmed at IR1).**

| Label used here | FX-PIPE-01 meaning | Source of the label |
|---|---|---|
| `OP-C3` | Check support spacing (non-mutating check) | Named in V1-A/V1-C text |
| `OP-C4` | Add support (model change) | Named in V1-C text |
| `OP-C6` | Mark row checked (records A4; reserved to the person, R-2) | Named in V1-A/V1-C/R-2 text |
| `‹read supports›` | The §10 read entry returning the support table for a run | Placeholder; identifier to be aligned (U-26) |
| model revisions | g1 fixed; an intervening person edit moves r12 → r13 | R-9; V1-C D-14 |
| `row N1`, `row N2`, `row E` | New support rows created by a receipt; an existing row | Placeholders for §10 row identifiers (U-26) |

---

## E1 — App-authored workflow: add a support with acceptance and Checked mark

Authored in the Chirality App, reviewed and registered in the project library
(registration is DEL-02-02's; shown only as the resulting identity).

**Identity.** {kind *workflow*, origin *project*, source root *fixture
project FX-PROJ*, name `support-adjustment-check`, revision `rev A2`};
derived-from *none*. (`rev A1` was the v0.1 example's content.)

**`WORKFLOW.md` — front matter and prose (illustrative).**

```markdown
---
name: support-adjustment-check
description: On one piping run with a support-spacing finding, propose adding
  support(s), wait for the engineer to accept or reject each proposed item,
  re-run the spacing check after application, and ask the engineer to mark the
  new support rows checked.
---
# Add support(s) for a spacing finding

Use this when the engineer names a run whose support spacing the host check
reports as exceeded, and wants it resolved by adding supports.

## Inspect
Read the run's support table and run the host's support-spacing check on the
current model revision. Keep the read basis you rely on. If the host reports
no spacing issue on this revision, stop and say so.

## Propose
Draft one proposal adding the support(s) needed, one change item per support,
showing old and new values, rows affected and why. The proposal is queued
until the engineer accepts or rejects each item; never describe it as
approved. If the host refuses it as stale, re-read and re-draft on the current
basis; never retarget the old proposal.

## Wait for acceptance  [checkpoint CP-accept]
The engineer accepts or rejects items in the host's own proposal view. If all
are rejected, return to Propose once with the engineer's reason, or stop if
they ask. If some are accepted and some rejected, continue with the accepted
items and report the rejected ones.

## Re-check
After the host applies accepted items, run the support-spacing check again
and report the host's results. Your summary is an examination, not the
engineer's Checked mark.

## Ask for the Checked mark  [checkpoint CP-check]
Ask the engineer to mark the new support rows checked in the host. If they
decline, stop and report. If they later edit a row, that row's mark lapses.

## Return
Summarize what changed (host receipt reference), host check results, which
acts the engineer performed, and what is unknown.
```

**Declared part (illustrative rendering).** *Declaration contract version:*
WD-v0.2 (fixture).

*Expected inputs*

| input name | meaning | kind | necessity | quality/basis requirement | stage |
|---|---|---|---|---|---|
| `run` | The run the engineer wants resolved | person-supplied choice | required | One run in the open model | Inspect |
| `support-table` | Current supports on the run | host read via `‹read supports›` | required | Read on the current revision; read-basis descriptor retained | Inspect |
| `spacing-finding` | The host's support-spacing result for the run | host result via `OP-C3` | required | Same basis as `support-table` | Inspect |

*Required tools*

| tool reference | class | purpose of use | necessity | version compatibility | stage |
|---|---|---|---|---|---|
| `‹read supports›` | host operation | read supports on the run | required | exact version (U-07) | Inspect |
| `OP-C3` | host operation | check support spacing, before and after the change | required | exact version | Inspect, Re-check |
| `OP-C4` | host operation | propose added supports. Derived: **checkpoint-forced treatment = propose** because `CP-accept` requires A5 on its result (WD I-7) | required | exact version | Propose |

*Checkpoints*

| checkpoint | required act kind | reached-when | subject (referent class) | scope | purpose | actor | on negative decision | on mixed decision | expected act evidence |
|---|---|---|---|---|---|---|---|---|---|
| `CP-accept` | A5 accept | observed host outcome *queued* for a proposal this run submitted through `OP-C4` | the change items of that proposal | per item; one A5 may list several items | engineer decides whether each added support goes into the model | the person | all items rejected (A10): return to Propose once, else stop | continue with accepted items; report rejected items | human-act record from the host's act facility (capturing surface) |
| `CP-check` | A4 mark checked | observed production of output `check-report` | the rows created or changed by the receipt of output `adjustment` | those rows | engineer records their own checking of the new supports | the person | decline/stop event: stop and report | — | human-act record from the host's act facility |

Not declared: A6 *approve* (engineering approval) and A7 *rely*. Reliance on
the model belongs to the accountable professional outside this workflow
(V4-AUT-05).

*Returned outputs*

| output | meaning | form | destination | promised standing | gating checkpoint |
|---|---|---|---|---|---|
| `adjustment` | the added supports | host change via proposal (V4-HI-23) | host support table | *queued*; *applied (receipt)* per accepted item after the host applies it | `CP-accept` |
| `check-report` | spacing results after application | report by reference | conversation + host results view | host results as reported (*host checks passed: support spacing* only where the host says so, with evaluated basis); agent summary *agent-examined (non-mutating)* | — |
| `checked-rows` | the engineer's A4 on the new rows | human-act standing | host support table | *marked checked by the person*, conditional on `CP-check` | `CP-check` |
| `summary` | what changed, acts performed, unknowns | message | conversation | *agent-prepared* | — |

*Returned evidence*

| evidence | kind | supports |
|---|---|---|
| `EV-basis` | relied-on read-basis reference (V4-HI-11/21) | `adjustment` |
| `EV-receipt` | host receipt reference per applied item (link, not copy) | `adjustment` |
| `EV-check` | host check result reference with evaluated basis | `check-report` |
| `EV-accept-act` | human-act record reference(s), A5/A10 per item | `CP-accept` only |
| `EV-checked-act` | human-act record reference(s), A4 per row | `CP-check` only |

*Compatible roles:* TASK, WORKING_ITEMS (fixture choice; host seat per WD §5
and U-09). *Tool restriction:* none declared.

## E1b — Review-only workflow (demonstrates I-3)

{workflow, project, FX-PROJ, `spacing-review`, `rev B1`}. Method: run `OP-C3`
on a run the engineer names, report findings, and ask the engineer to mark the
examined rows checked. No proposal is ever made.

| checkpoint | act | reached-when | subject | on negative decision |
|---|---|---|---|---|
| `CP-review` | A4 mark checked | observed production of output `findings` | the rows `OP-C3` reported on | decline/stop event: stop |

Outputs: `findings` (*agent-examined (non-mutating)*, host results by
reference). No A5 appears anywhere in this workflow.

## E1c — Variant with direct application and a later A4 (supports VC-11 R-5c)

{workflow, project, FX-PROJ, `support-add-direct`, `rev C1`}: the same method
as E1, but with **no** `CP-accept`. `OP-C4` is then not checkpoint-forced, so
its treatment follows the grant. `CP-check` (A4; reached-when: observed
production of `check-report`; subject: rows created or changed by the
`adjustment` receipt) remains.

---

## E2 — Run readings (fixture runs)

"Observed" facts are invented fixture facts, not host evidence. Dispositions
use the shared vocabulary (WD §4.3.4). Outcomes use P §9 per R-7.

| Run | Workflow | Invented observed facts | `CP-accept` | `CP-check` | `adjustment` | Incompatible reading exposed |
|---|---|---|---|---|---|---|
| R-1 success only | E1 | `OP-C4` returns success; proposal *queued* (items N1, N2); no act record | waiting | not reached | queued | "accepted" or "applied" inferred from success (I-2) |
| R-2 acceptance only | E1 | Person accepts N1 and N2 in one A5 listing both items (host act facility); host applies with receipt; `OP-C3` re-run; `check-report` produced | performed | waiting | applied (receipt) for N1, N2 | `CP-check` treated as satisfied by acceptance (I-1) |
| R-3 | — | *(v0.1's independent check moved to E1b; see R-E1b below)* | | | | |
| R-4 partial lapse | E1 | After R-2, person performs A4 on rows N1 and N2; later edits row N2's elevation (model r12 → r13) | performed (applying N1/N2 did not lapse A5, R-6) | **lapsed** for N2; N1 still performed | applied (receipt) | carrying A4 onto edited N2; asserting a re-hold (owned by DEL-02-03, U-22); lapsing A5 because the item was applied |
| R-5a forced proposal | E1 | Person has granted *direct* for model changes. Agent submits `OP-C4` as a proposal because `CP-accept` forces *propose* | waiting → performed on A5 | as R-2 | queued → applied (receipt) | direct application under the grant (D2: no grant widens past a declared checkpoint) |
| R-5b direct request | E1 | Same grant; agent requests `OP-C4` as direct application | not reached (no proposal queued) | not reached | **not permitted**, naming the checkpoint-forced treatment; nothing applied | silently converting the request into a proposal (R-3.3); applying then holding |
| R-5c direct then A4 | E1c | Grant *direct* is effective; agent applies `OP-C4` directly with origin and undo; `check-report` produced | — (not declared) | waiting for A4 on the applied rows | applied (receipt), direct under grant | treating direct application or its receipt as A4 |
| R-6 interruption | E1 | Proposal submitted; the loop loses observation before any host outcome | not reached or unknown (whether *queued* was observed decides which) | not reached | **outcome unknown**, reported by the loop (the observer) | reporting applied or failed without observation (S-K) |
| R-7 stale | E1 | Intervening person edit r12 → r13 before acceptance; host refuses the proposal as **stale** with both bases; agent re-reads and re-drafts a new proposal (new identity, lineage) | waiting; first arrival's items left the subject on refusal; second arrival binds the new proposal's items (RW-4) | not reached | first: stale refusal; second: queued | retargeting the stale proposal |
| R-7′ ends early | E1 | Run ends before any proposal is queued | not reached | not reached | not produced | reporting `CP-accept` as satisfied |
| R-8 wrong subject | E1 | Person accepts an item of a *different* proposal in the host | waiting | not reached | queued | counting an A5 on other content (SB-3) |
| R-9 capturing surface | E1 | (i) Agent writes "the engineer accepted in chat". (ii) Person accepts N1/N2 in the host; the App faithfully records it, citing the host act facility's evidence | (i) waiting; (ii) performed on the host evidence | — | (ii) applied (receipt) | (i) resuming on an agent-authored record (I-5) |
| R-10 reserved act | E1 | After `check-report`, agent calls `OP-C6` to mark N1 checked | — | waiting | — | `OP-C6` by the agent → **not permitted** (reserved to the person, R-2); treating the attempt as A4 |
| R-11 all rejected | E1 | Person rejects N1 and N2 (A10) | **resolved negatively**; on-negative path: return to Propose once | not reached | items rejected | counting A10 as "performed" |
| R-12 decline | E1 | After R-2, person declines to mark rows checked; decline/stop event recorded | performed | **resolved negatively** (decline event; not an A4) | applied (receipt) | recording the decline as an A4 |
| R-13 mixed | E1 | A5 on N1, A10 on N2 | **resolved negatively (partial)**; on-mixed path: continue with N1 | reached after `check-report`; subject = rows from N1's receipt | N1 applied (receipt); N2 rejected | treating the checkpoint as performed, or withholding N1's application |
| R-14 stale after acceptance | E1 | A5 on N1; before application an edit moves r12 → r13 affecting N1's basis; host refuses at application as stale | performed for N1's item content (not lapsed) | not reached | stale refusal; not applied | calling this a lapse of A5 (R-6: stale rule applies) |
| R-15 tool permission (App) | E1 run from the App through an external surface | The user's Codex mode auto-answers a tool-permission request (A14) for a shell command | unchanged | unchanged | unchanged | treating A14 as any checkpoint act (D3) |
| R-E1b independent A4 | E1b | `OP-C3` runs; `findings` produced; person marks rows checked in the host | — | `CP-review` performed | — | requiring a prior A5 (I-3) |

---

## E3 — Carried into a host, unadapted and adapted (fixture)

E1 is carried into the fixture host application `FX-HOST` (transfer
procedure is DEL-02-03's; U-18).

| | Original in App project | Carried **unadapted** into FX-HOST | **Adapted** in FX-HOST | Reopened in App after refinement |
|---|---|---|---|---|
| kind | workflow | workflow | workflow | workflow |
| origin | project | **project** (unchanged, R-9) | **host** | host (opening does not change it) |
| source root | FX-PROJ | FX-PROJ | FX-HOST workflow library | FX-HOST library |
| name | `support-adjustment-check` | same | same | same |
| revision | `rev A2` | `rev A2` | `rev H2` | a refinement is a DEL-02-02 draft until reviewed and registered; the host copy stays `rev H2` |
| derived-from | none | none | {workflow, project, FX-PROJ, `support-adjustment-check`, `rev A2`} | {workflow, host, FX-HOST, …, `rev H2`} if registered as a new App workflow |
| holding library (not identity; U-24) | FX-PROJ | FX-HOST workflow library | FX-HOST workflow library | App library where registered |

Adaptation in `rev H2` (fixture): `CP-accept` scope limited to whole-proposal
acceptance (one A5 listing all items). Checkpoint names, act kinds and
reached-when conditions are kept, so interruption/replay history stays
traceable. A consumer comparing `rev A2` and `rev H2` reports the changed
scope; matching names do not make them the same content.

---

## E4 — Same-name collision (fixture)

In the App, project FX-PROJ has {…, project, FX-PROJ, `support-adjustment-check`, `rev A2`}.
The person explicitly selects the host-supplied {…, host, FX-HOST, …, `rev H2`}.

| Step | Discovery shows | Selection holds | Required consumer behavior |
|---|---|---|---|
| 1 | project `rev A2`; host `rev H2`; collision reported | host / FX-HOST / `rev H2` (explicit) | Both origins listed (C-1). |
| 2 | A user-library copy `rev U1` appears | unchanged | Three origins listed; no rebinding despite Root ordering (C-2, C-5). |
| 3 | Host library changes to `rev H3` | `rev H2` selected; whether the run follows `rev H3` is DEL-02-02/host policy (U-10) | The chain shows which revision was resolved and supplied (C-4). |
| 4 | Person explicitly reselects project `rev A2` | project / FX-PROJ / `rev A2` | Recorded as a new selection event, not a rebinding (C-3). |

---

## E5 — A Root prose-only workflow read under v4 (real bytes, repo 6e18505e3)

Root's bundled `create-workflow` has front matter `name`/`description`,
prose, and no `execution.json` or declared part.

| Category | Reading |
|---|---|
| Expected inputs, outputs, evidence | **undeclared** |
| Required tools | **undeclared** → check **not established** |
| Checkpoints | **undeclared**. The prose's human review before registration is not product-held: it has no reached-when, subject or act kind. A consumer may report the prose (FB-07 style) but shall not synthesize a checkpoint. |
| Identity | {workflow, bundled, `chirality-root`, `create-workflow`, revision per U-03} |

This is expected: Root packages predate the declared part.

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

## E7 — Exposure outcomes (fixture; per R1_RESOLUTIONS R-9)

E1 is selected in the App and run against FX-HOST through its external
surface.

| Situation (invented) | Outcome for the requirement | Not to be reported as |
|---|---|---|
| FX-HOST's catalog has no `OP-C4` | **missing** | not exposed; unavailable |
| `OP-C4` is in the catalog; C's per-surface exposure element says it is not exposed on the external surface | **not exposed on this surface** | missing |
| Exposure element value for `OP-C4` on this surface is "unagreed" | **not established** | present |
| External access on FX-HOST is off (A13 not performed) | **channel not enabled** for every requirement on that surface | missing; unavailable |
| `OP-C3` present and exposed, but no run is selected in the host UI | **present, currently unavailable**, with the catalog's unavailable reason | missing |

---

## UNRESOLVED

Same register as WD-v0.2 §12. Items that shape these examples:

| item | owner | point of need | effect on these examples |
|---|---|---|---|
| U-01/U-02 carriage and wire names | DEL-02-01 with consumers | before OUT-002 schema / OUT-004 fixtures | Tables are illustrative renderings |
| U-03 revision algorithm | DEL-02-01 with DEL-04-03 | before revision comparisons | `rev A2`, `rev H2` are labels |
| U-26 FX-PIPE-01 identifiers | DEL-03-01 §10 | IR1 | `‹read supports›`, rows N1/N2/E are placeholders |
| U-07 version relation | DEL-03-01 | before DEL-02-03 required-tool fixtures | Exact versions only |
| U-09 host seat role mapping | DEL-02-01 with SWB owner and DEL-02-04 | before host role guidance | E1 compatible roles are a fixture choice |
| U-10 precedence and revision following | DEL-02-02 with host owner | before host-origin discovery | E4 step 3 left open |
| U-15 `UNRESOLVED{OI-021}` first operation | owner via outside SWB session | before connected-activity SoW | E1 uses FX-PIPE-01 entries, not the selected operation |
| U-19 forced treatment reaching the host route | DEL-04-01 with DEL-05-01, DEL-03-02, host | before W7 and loop fixtures | R-5b's "not permitted" assumes the host route knows the forced treatment |
| U-20 item-level rule | DEL-02-01; DEL-02-03, DEL-03-02 confirm | W7 | R-13 applies the proposed rule |
| U-21 run end while waiting / emptied subject | DEL-02-03 | W7 | R-7 shows rebinding on re-arrival |
| U-22 re-hold after post-pass lapse | DEL-02-03 | W7 | R-4 records lapse only |
| U-24 holding library | DEL-02-01 with DEL-02-03, host owner | IR1 | E3 shows it as a non-identity fact |
| U-05 `UNRESOLVED{OI-021}` operation-specific reserved additions | owner via outside SWB session | before connected-activity SoW | R-10 relies only on the D2 list (A4 via OP-C6) |

## Verification cases

These examples are inputs for WD-v0.2 §13; none has been run.

| Example | Used by | Expected result summary | VER |
|---|---|---|---|
| E1 | VC-01, VC-03, VC-05 | Categories incl. reached-when and subject recovered; roles readable in App and host seat; references compared to C v0.2 | VER-001, VER-002, VER-003 |
| E1b | VC-08 | A4 performed without any A5 | VER-003 |
| E1c + E2 R-5a/b/c | VC-11 | Forced proposal; direct request not permitted; direct then A4 | VER-003 |
| E2 R-1, R-2, R-4, R-6, R-7′, R-8, R-9, R-10, R-11, R-12, R-13, R-14, R-15 | VC-07, VC-09, VC-10, VC-15, VC-20, VC-21, VC-22, VC-16, VC-23, VC-24, VC-27, VC-28 | Only evidenced acts counted; shared dispositions as tabulated; unknown stays unknown | VER-003, VER-004 |
| E3 | VC-02, VC-14, VC-26 | Unadapted keeps origin; adapted has derived-from; holding library separate | VER-001, VER-004 |
| E4 | VC-13 | No rebinding; all origins exposed | VER-004 |
| E5 | VC-04 | All categories undeclared; no synthesized checkpoint | VER-002 |
| E6 | VC-06 | Restriction not read as requirement | VER-002 |
| E7 | VC-25 | Four distinct exposure-related outcomes | VER-002 |
| Inventory | VC-19 | Examples identified by WD-EX-v0.2; all "designed, not run" | VER-007 |
