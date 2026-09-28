# Portable workflow declaration — readable examples
- Contribution: DEL-02-01/WD-EX-v0.3 (companion to DEL-02-01/WD-v0.3, `WORKFLOW_DECLARATION.md`; supersedes WD-EX-v0.2, committed at `c387730fb`, file sha256 `50b7600de8503f51f440e5947ebd4ea7a559781e2497d5d880a8d683f7a9c43e`; WD-EX-v0.1 sha256 `69ac3dbfc5f97e2982418b918996df9b4a6abc674588c627e3e96fb4c133d55a`)
- Status: DRAFT DEFINITION — proposed, unsupplied, not implemented, not accepted
- Serves: OUT-001, OUT-002 (explanatory examples); OUT-004 (fixture subjects, designed only); REQ-001, REQ-002, REQ-003, REQ-004; VER-001…VER-004, VER-007
- Basis: repo 6e18505e3; ScopeOfWork.md sha256 080d7f5a8e55d93c06f51e5332b53954deb03e0877b1ee49be3011e3de14a294; PRD V4-WF-01…06, V4-HOST-05/06, V4-AUT-01/03/05, V4-EXE-01/03; HOST_INTEGRATION V4-HI-11, V4-HI-20…25, V4-HI-30…33, V4-HI-40…42, V4-HI-70/71; DECISION_BRIEF #d3, #d5; owner decision `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` (D2, D3); Root `workflows/WORKFLOW_TEMPLATE.md`, `workflows/create-workflow/WORKFLOW.md`, `workflows/project-dag/execution.json`
- Consumed inputs: R3_RESOLUTIONS.md sha256 `202d52c7d688382336cddb0d6c31be27969a9e667c5800b734428a090f05afbf` (R3-1, R3-3; in place, no version bump); R2_RESOLUTIONS.md sha256 `77cfb845ec305365f12218f83f332069155de5f362139b7a6fe2bf12cdebd088` (R2-4, R2-5, R2-7, R2-9, R2-12, R2-13, R2-14, R2-15, R2-16, R2-17, R2-18, R2-19, R2-20, R2-21); R1_RESOLUTIONS.md sha256 `2f9c7e72…77ec4`; IR1-C sha256 `295e96b3…26b9`, IR1-A sha256 `31b3c7f8…8284`, IR1-B sha256 `70e4a4f6…2846` (items addressed to DEL-02-01). **Shared fixture:** DEL-03-01 C-v0.2 §10 FX-PIPE-01, read at commit `28bd00499` (`CATALOG_AND_READ_BASIS.md` sha256 `358182b18b1fe13f9af6e6f5a61c9ed57f91b6ab29ea0c9adab06fe0081d6d82`), plus OP-C10/OP-C11 and fixture exposure values fixed by R2-21 ahead of C-v0.3. Proposal and outcome terms from P-v0.2 at `28bd00499` (sha256 `942c1a3ab5ad7bda865640067f0fd550d7cfd1acd8f6ee228f6906452adf8c89`) §4.3, §9.
- Receivers: as WD-v0.3 (DEL-02-03, DEL-05-01, DEL-05-02, DEL-03-02, DEL-02-01 OUT-004 self-check; DEL-02-02 and DEL-02-04 in a later undertaking per D1)

## Changes from v0.2

| Item | Change |
|---|---|
| R2-21; IR1C-15; IR1-B B-M8, B-M9 (X-6) | All fixture material re-pointed to C-v0.2 §10: workspace FX-W1, generation g1, run R-100, supports S-1…S-4, nozzles N-1/N-2, LC-1, Engineer A, OP-C1…OP-C9, steps T1…T17, bases B1/B2, proposals PR-1/PR-2, receipts RC-1…RC-3; plus OP-C10 (undo) and OP-C11 (no policy basis) fixed by R2-21. Local labels N1/N2/E, `‹read supports›`, "elevation" and the r12 → r13 post-application edit removed. Local cases are `L-WDEX-n`, each saying why. |
| R2-21; IR1-B B-M8 | OP-C3 is **Examine support spacing** (A3 findings). The E1 output is now an examination report (*agent-examined (non-mutating)*), never "host checks passed". Host checks appear only where a host result names them (OP-C1/OP-C2 results, T1). |
| R2-21; IR1-B B-M10 | Exposure: "exposed on all three surfaces (fixture assumption, R2-21)". C-v0.2 still lists *unagreed ×3*, which under WD §4.2.4 would make every requirement *not established*; stated as a divergence pending C-v0.3. |
| R2-17; IR1C-01, IR1C-05 | Every checkpoint declares a **subject class**. `CP-accept` uses kind (c) *queued* with "change items of the named proposal". `CP-check` binds "objects changed by a named outcome", not the examination output. |
| R2-18; IR1C-02 | T11 mixed decision shown with per-item annotation (R-2). |
| R2-19; IR1C-07 | Lapse shown as act-lapsed event → "waiting — lapsed at ‹t›" before resume; *lapsed* only after run end (R-4). |
| R2-5; IR1C-08 | Act-declined event (R-12) and run-ended while waiting (R-12b). |
| R2-12; IR1C-03 | R-5a/R-5b carry the governing checkpoint constraint; VC-11 **AWAITING INPUT**. |
| R2-7 | New E1d and R-16: A12 checkpoint with supersession. |
| R2-13, R2-14, R2-15, R2-16 | R-13 retry de-duplication (T13); binding by applied-outcome objects; R-17 undo lapses normally (T17); R-14 accepted-then-stale display. |
| R2-20; IR1C-09 | Holding library at listed/selected/resolved (E3, E4); capture-evidence reference case R-9 (iii). |
| R2-4 | R-10: reserved call → *not permitted*, A8 *offered*, not recorded automatically. |
| IR1-B B-m11 | E7 remedies stated as precondition meanings (T8), not UI gestures. |
| IR1C-13 | E7 applies the pass rule. |
| R3-1 | E1b now binds `CP-review` to **objects a named output concerns** (the rows the OP-C3 findings name), not the findings output; new run R-E1b′; VC-36. |
| R3-3 | R-14 (accepted-then-stale) marked adopted per R3-3, PROPOSED until W7. |

**Everything below is fixture subject material.** FX-PIPE-01, its rows,
values, people, revisions and runs are invented (C §10). Nothing here is a
SWBPIPE operation, catalog identity, receipt, human act or the selected first
connected operation (`UNRESOLVED{OI-021}`).

**Rendering note.** Declared parts are shown as Markdown tables for
readability. This is an illustrative rendering, not a selected carriage or
wire format (WD U-01, U-02). Revisions such as ⟨rev-A2⟩ are labels for
content identities whose algorithm is unselected (U-03).

**Fixture references (C-v0.2 §10 unless marked).**

| Label | Meaning | Source |
|---|---|---|
| OP-C1 v1 | Read supports table (per-row subject content identity; host checks passed; limitations) | C §10.2 |
| OP-C2 v1 | Read sustained-load results (precondition "a current solve exists") | C §10.2 |
| OP-C3 v1 | Examine support spacing — findings authored by the requester (A3); no human-act standing | C §10.2 |
| OP-C4 v1 / OP-C5 v1 | Add support / Set support stiffness — class *may apply within granted autonomy* (DERIVED), default propose | C §10.2 |
| OP-C6 / OP-C7 / OP-C8 | Mark row checked (A4) / Accept proposal items (A5) / Reject proposal items (A10) — reserved to the person; the person's host act facility | C §10.2 |
| OP-C9 v1 | Set support label (direct-branch fixture) | C §10.2 |
| OP-C10 | Undo (reverse a receipt), class *may apply within granted autonomy* | R2-15/R2-21 (C-v0.3 to add) |
| OP-C11 | Entry whose class is *no policy basis* (reason: pending OI-021) | R2-21 (C-v0.3 to add) |
| Exposure | Exposed on H, E and X for every entry — fixture assumption | R2-21 (C-v0.2 shows *unagreed ×3*) |
| T1…T17, Tg | Revision timeline r12…r17 in generation g1; B1 = r12, B2 = r13; PR-1 (stale), PR-2 (lineage PR-1); RC-1 (T12), RC-2 (T16), RC-3 reverses RC-2 (T17) | C §10.3 |
| `supports-adjust` ⟨rev-3⟩ | The host-origin workflow in C §10.1: {workflow, host, ⟨fx-root⟩, `supports-adjust`, ⟨rev-3⟩} | C §10.1; here the adaptation of E1 (E3) |
| ⟨fx-proj⟩ | App project library source root (local value label; no C counterpart) | This file |

---

## E1 — App-authored workflow `supports-adjust` (the origin of C's host workflow)

Authored in the Chirality App, reviewed and registered in the project library
(registration is DEL-02-02's; shown only as the resulting identity).

**Identity.** {kind *workflow*, origin *project*, source root ⟨fx-proj⟩, name
`supports-adjust`, revision ⟨rev-A2⟩}; derived-from *none*. Its host
adaptation is C §10.1's ⟨rev-3⟩ (E3).

**`WORKFLOW.md` — front matter and prose (illustrative).**

```markdown
---
name: supports-adjust
description: On one piping run with a support-spacing exceedance, examine the
  spacing, propose support changes as one proposal with one item per change,
  wait for the engineer to accept or reject each item, re-examine after
  application, and ask the engineer to mark the changed support rows checked.
---
# Adjust supports for a spacing exceedance

Use this when the engineer names a run and a spacing limit, and wants an
exceedance resolved by adding supports or changing support stiffness.

## Inspect
Read the run's supports table on the current model revision and keep its read
basis. Examine the support spacing against the stated limit. Your findings are
an examination, not the engineer's Checked mark. If you find no exceedance,
stop and say so.

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
After the host applies the accepted items, re-read the supports table and
examine the spacing again. Report your findings by reference.

## Ask for the Checked mark  [checkpoint CP-check]
Ask the engineer to mark the support rows the application changed as checked,
in the host. If they decline, stop and report.

## Return
Summarize what changed (receipt references), your findings, which acts the
engineer performed, and what is unknown.
```

**Declared part (illustrative rendering).** *Declaration contract version:*
WD-v0.3 (fixture).

*Expected inputs*

| input name | meaning | kind | necessity | quality/basis requirement | stage |
|---|---|---|---|---|---|
| `run` | The run the engineer wants resolved (e.g., R-100) | person-supplied choice | required | One run in the workspace | Inspect |
| `spacing-limit` | The spacing limit to examine against | person-supplied value | required | Stated with units | Inspect |
| `supports-table` | Current supports on the run | host read via OP-C1 | required | Complete five-element read basis (workspace, generation, model revision, content identity, method designation); per-row subject content identities | Inspect, Re-examine |

*Required tools*

| tool reference | class | purpose of use | necessity | version compatibility | stage |
|---|---|---|---|---|---|
| OP-C1 | host operation | read supports on the run | required | v1 | Inspect, Re-examine |
| OP-C3 | host operation | examine spacing against the limit (A3 findings) | required | v1 | Inspect, Re-examine |
| OP-C4 | host operation | propose added supports. **Governing checkpoint constraint** {run, `CP-accept`, A5, OP-C4} carried with every change request (WD I-7) | required | v1 | Propose |
| OP-C5 | host operation | propose stiffness changes. Constraint {run, `CP-accept`, A5, OP-C5} | optional (fallback: propose added supports only) | v1 | Propose |

OP-C6/OP-C7/OP-C8 are not required tools: they are the person's act facility
and reserved to the person.

*Checkpoints*

| checkpoint | act | reached-when | subject class | scope | purpose | actor | on negative decision | on mixed decision | expected act evidence |
|---|---|---|---|---|---|---|---|---|---|
| `CP-accept` | A5 accept | (c) observed host outcome *queued* for the proposal this run submits with OP-C4/OP-C5 items | change items of the named proposal (that queued proposal) | per item; one A5 may list several items | engineer decides whether each support change goes into the model | the person | all items A10: return to Propose once, else stop | continue with accepted items; report rejected items | host act record (OP-C7/OP-C8 capture) with capture-evidence reference |
| `CP-check` | A4 mark checked | (b) observed production of output `examination-report` | objects changed by a named outcome: the objects the **applied (receipt)** outcomes of `CP-accept`'s items identify | those objects | engineer records their own checking of the changed supports | the person | act-declined event: stop and report | — | host act record (OP-C6 capture) with capture-evidence reference, bound to each object's post-application subject content identity |

Not declared: A6 *approve* (engineering approval) and A7 *rely*. Reliance on
the model belongs to the accountable professional outside this workflow
(V4-AUT-05).

*Returned outputs*

| output | meaning | form | destination | promised standing | gating checkpoint |
|---|---|---|---|---|---|
| `adjustment` | the support changes | host change via proposal (V4-HI-23) | host supports table | *queued*; per accepted item *applied (receipt)* after host application | `CP-accept` |
| `examination-report` | spacing findings after application | report, citing OP-C3 results and the OP-C1 basis by reference | conversation + host results view | *agent-examined (non-mutating)* — A3 findings; any host checks shown only as the OP-C1 result names them ("host checks passed: ‹named checks›", with evaluated basis) | — |
| `checked-rows` | the engineer's A4 on the changed rows | human-act standing | host supports table | *marked checked by the person*, conditional on `CP-check` | `CP-check` |
| `summary` | what changed, acts performed, unknowns | message | conversation | *agent-prepared* | — |

*Returned evidence*

| evidence | kind | supports |
|---|---|---|
| `EV-basis` | relied-on read basis (e.g., B1, B2) | `adjustment` |
| `EV-receipt` | host receipt reference per applied item (link, not copy) | `adjustment` |
| `EV-exam` | OP-C3 result reference (A3 findings) with evaluated basis | `examination-report` |
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
constraint and its treatment follows the grant.

| checkpoint | act | reached-when | subject class |
|---|---|---|---|
| `CP-check` | A4 mark checked | (c) observed host outcome *applied (receipt)* of OP-C9 | objects changed by a named outcome (the OP-C9 receipt) |

Whether a support's subject content identity covers its label is a host input
(C §5.3, U-C3). If it does not, the A4 binds to content the label change did
not alter; the fixture states this dependency rather than assuming either.

## E1d — Grant checkpoint (supports R-16)

{workflow, project, ⟨fx-proj⟩, `label-with-grant`, ⟨rev-D1⟩}: as E1c, plus

| checkpoint | act | reached-when | subject class |
|---|---|---|---|
| `CP-grant` | A12 set grant | (a) before dispatch of OP-C9 | grant setting (setting content: classes, grant value, scope) |

---

## E2 — Run readings along the FX-PIPE-01 timeline

The runs read the host workflow ⟨rev-3⟩ (E3), which keeps E1's declared
checkpoints, in workspace FX-W1 with Engineer A, unless another workflow is
named. "Observed" facts are C's invented timeline or a named `L-WDEX-n`
variant. Dispositions use the shared vocabulary (WD §4.3.4); outcomes P §9.

| Run | Steps | Invented observed facts | `CP-accept` | `CP-check` | `adjustment` | Incompatible reading exposed |
|---|---|---|---|---|---|---|
| R-1 success only | T10 | PR-2 validated → *queued*; no act record | waiting (bound to PR-2 items 1, 2) | not reached | items 1, 2 *queued* | "accepted" or "applied" inferred from success (I-2) |
| R-2 mixed | T11–T12, then re-examination | Engineer A accepts item 1 (OP-C7; A5) and rejects item 2 (OP-C8; A10); host applies item 1 → RC-1 (r14); agent re-reads OP-C1 and runs OP-C3 → `examination-report` | **resolved negatively**, annotated "partial: item 1 A5, item 2 A10"; on-mixed path: continue with item 1 | waiting; bound to the objects RC-1 identifies (the new support), post-application subject identity | item 1 *applied (RC-1)*; item 2 *rejected* | showing `CP-accept` as performed or "all accepted"; withholding item 1's application |
| R-3 both accepted | L-WDEX-1 (variant of T11: one A5 lists items 1 and 2 — needed because C's T11 rejects item 2) | Host applies both → receipt (local label L-WDEX-1-RC) changing the new support and S-3; `examination-report` produced | **performed** (A5 not lapsed by application) | waiting; bound to the new support and S-3 | items 1, 2 *applied* | `CP-check` treated as satisfied by acceptance (I-1) |
| R-4 lapse sequence | L-WDEX-1 continued; T14 as control | Engineer A marks both rows checked (OP-C6; A4). (i) Before the loop resumes, Engineer A edits S-3 again → act-lapsed event. (ii) Instead, after the run ended, Engineer A edits S-3. Control: T14 edits S-2 (not bound here) | performed | (i) **waiting — lapsed at ‹t›** (new A4 needed on S-3's current content); (ii) **lapsed** for S-3 only, new support still performed; control: unchanged | applied | carrying A4 onto the edited S-3; lapsing unbound rows on T14; re-holding after resume (DEL-02-03, U-22) |
| R-5a forced proposal | L-WDEX-2 (variant of T15 with scope "support additions on R-100" — C's T15 scope covers labels only, IR1-B B-m10) | Grant *direct* effective for the OP-C4 class on R-100. Agent submits OP-C4 as a proposal carrying the constraint {run, `CP-accept`, A5, OP-C4} | waiting on the queued proposal | not reached | *queued* | direct application under the grant (D2: no grant widens past a declared checkpoint) — **AWAITING INPUT** (U-19) |
| R-5b direct request | L-WDEX-2 | Same grant; agent requests OP-C4 as direct application; constraint carried | not reached (nothing queued) | not reached | **not permitted**, naming the governing checkpoint constraint; nothing applied | silent conversion into a proposal (R-3.3; R2-12) — **AWAITING INPUT** |
| R-5c direct then A4 | T15–T16 with E1c | Grant *direct* effective for OP-C9 scope (T15); agent applies OP-C9 directly: S-4 label "G-4" → RC-2, origin mark, undo route | — (none declared) | waiting for A4 on S-4 (objects changed by RC-2) | *applied (RC-2)*, branch direct under grant | treating the direct application or RC-2 as A4 |
| R-6 interruption | L-WDEX-3 (C has no pre-*queued* loss) | PR-2 submitted; the loop loses observation before any host outcome | **unknown** (the deciding observation was lost) | not reached | **outcome unknown**, reporter: the loop | reporting queued, applied or failed without observation (S-K) |
| R-7 stale then re-draft | T5–T10 | PR-1 relies on B1 (r12); T6 edit of S-3 (r13); T7 PR-1 **refused — stale** (relied B1, current B2); T9 PR-2 (lineage PR-1) drafted on B2; T10 PR-2 *queued* | not reached until T10; then waiting bound to PR-2 items | not reached | PR-1: refused — stale; PR-2: *queued* | retargeting PR-1; binding `CP-accept` to PR-1 |
| R-7′ run ends early | L-WDEX-4 (run stops after T7) | Run-ended event before any re-draft | **not reached** | not reached | PR-1: refused — stale | reporting `CP-accept` as satisfied |
| R-8 wrong subject | L-WDEX-5 (a second proposal outside this run) | After T10, Engineer A accepts an item of the L-WDEX-5 proposal | waiting | not reached | PR-2 *queued* | counting an A5 on other content (SB-2) |
| R-9 capturing surface | T11 | (i) The agent writes "Engineer A accepted item 1". (ii) Engineer A's A5/A10 captured by the host facility (OP-C7/OP-C8) with a capture-evidence reference; the App faithfully records it, citing that reference. (iii) As (ii), but the host exposes no capture-evidence reference | (i) waiting; (ii) resolved negatively as R-2; (iii) waiting (U-05b) | — | as R-2 in (ii) | (i) resuming on an agent-authored record; (iii) resuming without capture evidence (I-5) |
| R-10 reserved call | after R-3 | The agent calls OP-C6 to mark the new support checked | — | waiting | — | OP-C6 by the agent → **not permitted** (reserved, DERIVED R2-2); an A8 request is *offered*, not recorded automatically (R2-4); treating the attempt as A4 |
| R-11 all rejected | L-WDEX-6 (variant of T11 rejecting both items) | A10 on items 1 and 2 | **resolved negatively**; on-negative path: return to Propose once | not reached | items *rejected* | counting A10 as performed |
| R-12 act declined | after R-2 | Engineer A declines to mark the new support checked → act-declined event with capture evidence | as R-2 | **resolved negatively** (not an A4); on-negative path: stop | as R-2 | recording the decline as A4 |
| R-12b run ended while waiting | after R-2 | Engineer A stops the run while `CP-check` waits → run-ended event; later Engineer A marks the row checked | as R-2 | final **waiting** with run-ended event; the later A4 is recorded and shown against the bound subject, but the ended run's disposition does not change (U-21) | as R-2 | reporting the ended run's checkpoint as performed |
| R-13 retry | T13 | Acknowledgment of RC-1 lost; agent resubmits PR-2 (same identity) | unchanged | unchanged | de-duplicated by identity first: the repeat reports RC-1, never refused stale by its own effect; if unobservable, **outcome unknown** by the observer (R2-13) | a second application; a stale refusal caused by RC-1 |
| R-14 accepted, then stale (adopted per R3-3; PROPOSED until W7) | L-WDEX-7 (variant: A5 on both items at T11; before item 2 is applied Engineer A edits S-3 again) | Item 1 applied (distinct targets, not staled, R2-13); item 2 refused at application — stale | unchanged (decided) | waiting; bound to objects changed by item 1's receipt only | item 1 applied; item 2 "accepted by Engineer A — not applied: refused — stale (relied B2, current ‹B′›)"; A5 not lapsed | calling this a lapse of A5; showing item 2 as applied or merely "accepted" |
| R-15 tool permission (App) | L-WDEX-8 (App-side run through the external surface) | The user's Codex mode auto-answers a tool permission (A14) for a shell command | unchanged | unchanged | unchanged | treating A14 as any checkpoint act (D3) |
| R-16 A12 supersession | T15 with E1d; L-WDEX-9 | `CP-grant` reached before OP-C9 dispatch; Engineer A performs A12 (T15) → **performed**. Later Engineer A performs a new A12 narrowing the scope | — | — | — | `CP-grant` stays **performed**, shown "superseded by ‹later A12›"; not lapsed (R2-7). Refused-A12 case held (U-27) |
| R-17 undo | T16–T17 with E1c | Engineer A marks S-4 checked after RC-2; run ends; T17 undo RC-3 *reverses RC-2* | — | **lapsed** (run ended) if S-4's subject identity covers the label (U-C3) | RC-2 applied, then reversed by RC-3 | treating the undo as leaving the A4 intact when bound content changed (R2-15) |
| R-E1b independent A4 | E1b, T3–T4 | OP-C1 read (B1); OP-C3 findings name S-2→S-3; `findings` produced; Engineer A marks S-2 and S-3 checked in the host (OP-C6 capture) | — | `CP-review` **performed** | — | requiring a prior A5 (I-3) |
| R-E1b′ binding | E1b, T3–T6 (L-WDEX-15: variant marking only the findings, then T6) | (i) Engineer A marks the `findings` output checked, not the rows. (ii) After R-E1b, T6 edits S-3 before the run resumes | — | (i) `CP-review` **waiting** (wrong referent, SB-2); (ii) act-lapsed event for S-3 → **waiting — lapsed at ‹t›**; S-2 still bound | — | binding to the output's own content; lapsing S-2 on an S-3 edit |

---

## E3 — Carried into a host, unadapted and adapted

E1 is carried into the fixture host's workflow library ⟨fx-root⟩ (transfer
procedure is DEL-02-03's; U-18).

| | Original in App project | Carried **unadapted** | **Adapted** (C §10.1) | Reopened in App after refinement |
|---|---|---|---|---|
| kind | workflow | workflow | workflow | workflow |
| origin | project | **project** (unchanged, R-9) | **host** | host (opening does not change it) |
| source root | ⟨fx-proj⟩ | ⟨fx-proj⟩ | ⟨fx-root⟩ | ⟨fx-root⟩ |
| name | `supports-adjust` | same | same | same |
| revision | ⟨rev-A2⟩ | ⟨rev-A2⟩ | ⟨rev-3⟩ | a refinement is a DEL-02-02 draft until reviewed and registered; the host copy stays ⟨rev-3⟩ |
| derived-from | none | none | {workflow, project, ⟨fx-proj⟩, `supports-adjust`, ⟨rev-A2⟩} | {workflow, host, ⟨fx-root⟩, `supports-adjust`, ⟨rev-3⟩} if registered as a new App workflow |
| holding library (listed/selected/resolved; not identity; PROPOSED) | ⟨fx-proj⟩ | ⟨fx-root⟩ | ⟨fx-root⟩ | App library where registered |

Adaptation in ⟨rev-3⟩ (fixture): `spacing-limit` becomes optional with the
fallback "use the host project's stated limit"; the prose refers to the
host's own proposal view by name. Checkpoint names, act kinds, reached-when
conditions and subject classes are unchanged, so interruption/replay history
stays traceable. A consumer comparing ⟨rev-A2⟩ and ⟨rev-3⟩ reports the
changed input necessity; matching names do not make them the same content.

---

## E4 — Same-name collision in the host library

After E3, ⟨fx-root⟩ holds two workflows named `supports-adjust`: the unadapted
copy {…, project, ⟨fx-proj⟩, …, ⟨rev-A2⟩} and the adapted {…, host,
⟨fx-root⟩, …, ⟨rev-3⟩}.

| Step | Discovery shows | Selection holds | Required consumer behavior |
|---|---|---|---|
| 1 | Two entries, each with origin and holding library ⟨fx-root⟩; collision reported | Engineer A explicitly selects host ⟨rev-3⟩ | Both origins listed with holding library (C-1); the panel shows "project-origin, held in ⟨fx-root⟩" for the copy. |
| 2 | A user-library copy ⟨rev-U1⟩ appears in the App | unchanged | Three origins listed; no rebinding despite Root ordering (C-2, C-5). |
| 3 | The host library registers ⟨rev-4⟩ of the host workflow | ⟨rev-3⟩ selected; whether the run follows ⟨rev-4⟩ is host/DEL-02-02 policy (U-10) | The chain shows which revision was resolved and supplied (C-4). |
| 4 | Engineer A explicitly reselects the project-origin copy | {…, project, ⟨fx-proj⟩, …, ⟨rev-A2⟩}, held in ⟨fx-root⟩ | New selection event, not a rebinding (C-3). Its holding library differs from the App's copy; identity equality ignores it (C-6). |

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

## E7 — Compatibility outcomes and the pass rule

E1 ⟨rev-3⟩ is checked against FX-W1's catalog edition. The base case uses the
R2-21 fixture exposure (exposed on all three surfaces); each variant is local
and says what it changes.

| Case | Situation | Outcome per requirement | Pass? |
|---|---|---|---|
| Base | OP-C1, OP-C3, OP-C4, OP-C5 in the edition, exposed on the acting surface | all **present** | passes |
| L-WDEX-10 | OP-C4 absent from the edition | OP-C4 **missing** | does not pass (required) |
| L-WDEX-11 | OP-C5 absent from the edition | OP-C5 **missing** | passes (OP-C5 optional; fallback shown) |
| L-WDEX-12 | Element 9 for OP-C4 on the external surface is *not exposed on this surface* | OP-C4 **not exposed on this surface** (external run) | does not pass on X; unaffected on E |
| C-v0.2 as committed | Element 9 is *unagreed ×3* for every entry | every requirement **not established** | does not pass — divergence from R2-21 pending C-v0.3 (U-23) |
| L-WDEX-13 | External access on FX-W1 is off (A13 not performed) | **channel not enabled** for every requirement on X | does not pass on X; never shown as missing |
| T8 analogue | A workflow requiring OP-C2 checked at r13, where OP-C2's precondition "a current solve exists" fails (reason "No current solve for LC-1 at this revision", evaluated basis B2) | OP-C2 **present, currently unavailable** | passes; shown as a run-time hold with the reason |
| L-WDEX-14 | A workflow requiring OP-C11 (class *no policy basis*, reason pending OI-021) | OP-C11 **present**; at run time a direct request is *not permitted* and proposing confers no permission (R2-9) | passes the requirement check; fixtures depending on OP-C11's production report **held**, never a pass |
| E6 reading | Root prose-only package | **not established** (undeclared) | selectable; never "runnable" by check |

---

## UNRESOLVED

Same register as WD-v0.3 §12. Items that shape these examples:

| item | owner | point of need | effect on these examples |
|---|---|---|---|
| U-01/U-02 carriage and wire names | DEL-02-01 with consumers | before OUT-002 schema / OUT-004 fixtures | Tables are illustrative renderings |
| U-03 revision algorithm | DEL-02-01 with DEL-04-03 | before revision comparisons | ⟨rev-A2⟩, ⟨rev-3⟩ are labels |
| U-23 fixture exposure values | DEL-03-01 (C-v0.3, R2-21) | C-v0.3 | Base cases assume "exposed ×3"; C-v0.2 would give *not established* |
| U-19 constraint receipt by the host (relay) | host owner via W9; DEL-03-02 element | before host-side fixtures | R-5a/R-5b **AWAITING INPUT** |
| U-05b capture-evidence reference (relay) | host owner via W9 | before host act-recording integration | R-9 (iii) stays waiting |
| U-20 item-level rule | DEL-02-01; DEL-02-03 confirms at W7 | W7 | R-2, R-11, R-14 apply the PROPOSED rule |
| U-21 ended-run resumption | DEL-02-03 | W7 | R-12b keeps the ended disposition |
| U-22 re-hold after resume | DEL-02-03 | W7 | R-4 records the event only after resume |
| U-24 holding library | DEL-02-01 with DEL-02-03, host owner | W7 | E3/E4 show it as PROPOSED |
| U-27 control-refused A12 | DEL-02-03 with DEL-04-01/DEL-04-02 | before A12 fixtures | R-16 covers supersession only |
| U-C3 subject identity coverage (C) | host input via DEL-03-01 | before E1c/R-17 execution | label coverage decides R-5c/R-17 lapse |
| U-09 host seat role mapping | DEL-02-01 with SWB owner and DEL-02-04 | before host role guidance | E1 compatible roles are a fixture choice |
| U-10 precedence and revision following | DEL-02-02 with host owner | before host-origin discovery | E4 step 3 left open |
| U-15 / U-05 `UNRESOLVED{OI-021}` | owner via outside SWB session | before connected-activity SoW | FX-PIPE-01 entries are not the selected operation; OP-C11's reason cites it |

## Verification cases

These examples are inputs for WD-v0.3 §13; none has been run.

| Example | Used by | Expected result summary | VER |
|---|---|---|---|
| E1 | VC-01, VC-03, VC-05, VC-29, VC-30 | Categories incl. subject class recovered; references compared to C §10; invalid A5 variants rejected; `CP-check` binds applied objects | VER-001, VER-002, VER-003 |
| E1b | VC-08, VC-36 | A4 performed without any A5; binding to the examined rows | VER-003 |
| E1c + E2 R-5a/b/c | VC-11 | AWAITING INPUT (host side); designed expectations as tabulated | VER-003 |
| E1d + E2 R-16 | VC-32 | Supersession, not lapse | VER-003 |
| E2 R-1, R-2, R-3, R-4, R-6, R-7′, R-8, R-9, R-10, R-11, R-12, R-12b, R-13, R-14, R-15, R-17 | VC-07, VC-24, VC-09, VC-10, VC-15, VC-20, VC-21, VC-22, VC-16, VC-23, VC-23, VC-31, VC-34, VC-27, VC-28, VC-35 | Only evidenced acts counted; shared dispositions and events as tabulated; unknown stays unknown | VER-003, VER-004 |
| E3 | VC-02, VC-14, VC-26 | Unadapted keeps origin; adapted has derived-from; holding library separate | VER-001, VER-004 |
| E4 | VC-13 | No rebinding; all origins with holding library | VER-004 |
| E5 | VC-04 | All categories undeclared; no synthesized checkpoint | VER-002 |
| E6 | VC-06 | Restriction not read as requirement | VER-002 |
| E7 | VC-25, VC-33 | Distinct outcomes; pass rule | VER-002 |
| Inventory | VC-19 | Examples identified by WD-EX-v0.3; all DESIGNED or AWAITING INPUT | VER-007 |
