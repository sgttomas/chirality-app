# Portable workflow declaration — readable examples
- Contribution: DEL-02-01/WD-EX-v0.1 (companion to DEL-02-01/WD-v0.1, `WORKFLOW_DECLARATION.md`)
- Status: DRAFT DEFINITION — proposed, unsupplied, not implemented, not accepted
- Serves: OUT-001, OUT-002 (explanatory examples); OUT-004 (fixture subjects, designed only); REQ-001, REQ-002, REQ-003, REQ-004; VER-001…VER-004, VER-007
- Basis: repo 6e18505e3; ScopeOfWork.md sha256 080d7f5a8e55d93c06f51e5332b53954deb03e0877b1ee49be3011e3de14a294; PRD V4-WF-01…06, V4-HOST-05/06, V4-AUT-01/03/05, V4-EXE-03; HOST_INTEGRATION V4-HI-11, V4-HI-20…25, V4-HI-30…33, V4-HI-40…42, V4-HI-70/71; DECISION_BRIEF #d3, #d5; Root `workflows/WORKFLOW_TEMPLATE.md`, `workflows/*/execution.json`
- Consumed inputs: accepted basis only; DEL-03-01 operation identities, DEL-04-01 act-kind names and DEL-04-03 record meanings referenced by accepted meaning, to be reconciled at V1
- Receivers: as WD-v0.1 (DEL-02-02, DEL-02-03, DEL-02-04, DEL-05-01, DEL-05-02; DEL-02-01 OUT-004 self-check)

**Everything below is fixture subject material.** The piping model, lines,
supports, values, operation labels, people, revisions and runs are invented.
Nothing here is a SWBPIPE operation, catalog identity, receipt, human act or
the selected first connected operation (`UNRESOLVED{OI-021}`).

**Rendering note.** Declared parts are shown as Markdown tables so they are
readable. This is an *illustrative rendering*, not a selected carriage or wire
format (WD-v0.1 U-01, U-02). Labels such as `‹C: read support table›` are
fixture placeholders for opaque DEL-03-01 operation identities; revisions such
as `rev A1` are fixture labels for content identities whose algorithm is
unselected (U-03).

---

## E1 — App-authored workflow: support adjustment with check (fixture)

Authored in the Chirality App by a workflow maker, reviewed and registered in
the project library (registration is DEL-02-02's journey; shown only as the
resulting identity).

**Identity.** kind *workflow*; origin *project*; source root *fixture project
FX-PROJ*; name `support-adjustment-check`; revision `rev A1`; derived-from
*none*.

**Package contents (illustrative).**

```text
support-adjustment-check/
  WORKFLOW.md          ← prose method + declared part (carriage per U-01)
```

**`WORKFLOW.md` — front matter and prose (illustrative).**

```markdown
---
name: support-adjustment-check
description: Propose a support adjustment on one piping run to relieve a
  sustained-stress exceedance, have the proposal accepted by the engineer,
  run a non-mutating stress check, and ask the engineer to mark the adjusted
  supports checked.
---
# Support adjustment with check

Use this when the engineer names a run and a stress exceedance they want
relieved by adjusting existing supports (position or spring rate), not by
rerouting. The result is an accepted and applied adjustment, a check report,
and the engineer's Checked mark on the adjusted rows — or a clear stop.

## Inspect
Read the run's support table and current sustained-stress results on the
current model revision. Note the read basis you rely on. If the exceedance is
not present on the current revision, stop and say so.

## Propose
Draft one adjustment (e.g., move a spring hanger along the run, or change its
spring rate). Submit it as a proposal showing old and new values, the rows
affected and why. A proposal is queued until the engineer accepts it; never
describe it as approved. If the host refuses it as stale, re-read and
re-draft on the current basis; do not retarget the old proposal.

## Wait for acceptance  [checkpoint CP-accept]
The engineer accepts or rejects the proposal, row by row, several rows, or
as a batch. If rejected, return to Propose once with the engineer's reason,
or stop if they ask.

## Check
After application, run the non-mutating stress check and report results by
reference. Your check is not the engineer's Checked mark.

## Ask for the Checked mark  [checkpoint CP-check]
Ask the engineer to mark the adjusted support rows checked. If they edit
those rows first, the request is for the edited content.

## Return
Summarize what changed (with the host receipt reference), check results,
and which acts the engineer performed. Say what is unknown.
```

**Declared part (illustrative rendering).**

*Declaration contract version:* WD-v0.1 (fixture).

*Expected inputs*

| input name | meaning | kind | necessity | quality/basis requirement | stage |
|---|---|---|---|---|---|
| `run` | The piping run the engineer wants relieved | person-supplied choice | required | Must identify one run in the open model | Inspect |
| `exceedance` | The stress location/case the engineer is concerned about | person-supplied value | required | Must exist on the current model revision | Inspect |
| `support-table` | Current supports on the run | host read via `‹C: read support table›` | required | Read on current revision; basis descriptor retained (DEL-03-01) | Inspect |
| `stress-results` | Current sustained-stress results for the run | host read via `‹C: read stress results›` | required | Same basis as `support-table` | Inspect |

*Required tools*

| tool reference | class | purpose of use | necessity | version compatibility | stage |
|---|---|---|---|---|---|
| `‹C: read support table›` | host operation | read supports on the run | required | U-07 | Inspect |
| `‹C: read stress results›` | host operation | read sustained-stress results | required | U-07 | Inspect |
| `‹C: modify support›` | host operation | draft/submit the adjustment (class and autonomy come from the catalog entry and the person's setting, not from here) | required | U-07 | Propose |
| `‹C: run stress check›` | host operation | non-mutating check after application | required | U-07 | Check |

*Checkpoints*

| checkpoint | required act kind | subject | scope | purpose | actor | position | on negative decision | expected act evidence |
|---|---|---|---|---|---|---|---|---|
| `CP-accept` | *accept a proposed edit* | the queued adjustment proposal: affected support rows, old/new values, reason | per row, several rows, or whole proposal (V4-HI-41 granularity) | engineer decides whether the model change goes ahead | the person | after Propose | on rejection: return to Propose once, else stop | human-act record (DEL-04-03) |
| `CP-check` | *mark checked* | the adjusted support rows as applied, with the check report reference | the adjusted rows | engineer records their own checking of the adjusted supports | the person | after Check | on decline: stop and report | human-act record (DEL-04-03) |

Not declared: *approve* and *accept professional reliance*. Professional
reliance on the model belongs to the accountable professional outside this
workflow (V4-AUT-05); the workflow does not request it.

*Returned outputs*

| output | meaning | form | destination | promised standing | gating checkpoint |
|---|---|---|---|---|---|
| `adjustment` | the support change | host change via proposal (V4-HI-23) | host support table | *proposed (queued)*; *applied with receipt* only after `CP-accept` performed and the host applies | `CP-accept` |
| `check-report` | stress check results after application | report by reference | conversation + host results view | *agent-checked (non-mutating)* | — |
| `checked-rows` | the engineer's Checked mark on adjusted rows | human-act standing | host support table | *checked by the person* — conditional on `CP-check` | `CP-check` |
| `summary` | what changed, acts performed, unknowns | message | conversation | *agent-prepared* | — |

*Returned evidence*

| evidence | kind | supports |
|---|---|---|
| `EV-basis` | read-basis reference relied on for the proposal (V4-HI-11/21) | `adjustment` |
| `EV-receipt` | host receipt reference for application (link, not copy) | `adjustment` |
| `EV-check` | check result reference | `check-report` |
| `EV-accept-act` | human-act record reference | `CP-accept` only |
| `EV-checked-act` | human-act record reference | `CP-check` only |

*Compatible roles:* TASK, WORKING_ITEMS (fixture choice; in a host seat see
WD-v0.1 §5 and U-09). *Tool restriction:* none declared.

---

## E2 — Run readings against E1 (fixture runs)

Each run is read by a consumer comparing declared promises with observed
facts (WD-v0.1 §4.6). "Observed" facts here are invented fixture facts, not
host evidence.

| Run | Invented observed facts | `CP-accept` | `CP-check` | `adjustment` standing | Evidence | Incompatible reading to expose |
|---|---|---|---|---|---|---|
| R-1 success only | `‹C: modify support›` returned success; proposal queued; no act record | awaiting act | not reached | proposed (queued) | `EV-basis` present; `EV-receipt`, `EV-accept-act` missing | "accepted" or "applied" inferred from success (S-G, I-2) |
| R-2 acceptance only | Person accepted rows S-4/S-5 (act record present); host applied with receipt; check run | performed | awaiting act | applied with receipt | `EV-checked-act` missing | `CP-check` treated as satisfied by acceptance (I-1) |
| R-3 independent check | Person marks S-4 row checked with its own act record, having edited S-4 themselves; there is no accepted proposal in this run | awaiting act (or run stopped) | performed for S-4's current content | not produced by this run | `EV-checked-act` present; `EV-accept-act` missing | refusing the Checked act because no proposal acceptance preceded it (I-3) |
| R-4 lapse | After R-2 and `CP-check` performed, person edits S-5 spring rate | performed (unchanged) | lapsed → awaiting act for S-5's new content | applied with receipt | old `EV-checked-act` retained as history | carrying the old Checked act onto edited S-5 (I-4) |
| R-5 widened autonomy | Person granted direct application for support changes; agent applies directly with origin mark and undo | awaiting act (run holds regardless) | not reached | applied with receipt (direct) | `EV-receipt` present; `EV-accept-act` missing | treating direct application as satisfying `CP-accept` (S-F, V4-HI-42) |
| R-6 interruption | Proposal submitted; connection lost; no observation of application | unknown | not reached | outcome unknown | `EV-receipt` missing | reporting applied or failed without observation (S-K) |
| R-7 stale | Intervening edit by person to S-4 before acceptance; host refuses proposal as stale with reason; agent re-reads and re-drafts | awaiting act on the *new* proposal | not reached | first proposal: stale (refused); second: proposed (queued) | two `EV-basis` references | retargeting the stale proposal (V4-HI-23) |

---

## E3 — Carried into a host and adapted (fixture)

The App-authored E1 is carried into the fixture host application
`FX-HOST` and adapted there by the host's workflow maker (transfer procedure
is DEL-02-03's; U-18).

| | Original | Adapted in host | Reopened in App after refinement |
|---|---|---|---|
| kind | workflow | workflow | workflow |
| origin | project | **host** | **host** (unchanged by opening in App) |
| source root | fixture project FX-PROJ | fixture host FX-HOST, its workflow library | FX-HOST library |
| name | `support-adjustment-check` | `support-adjustment-check` | `support-adjustment-check` |
| revision | `rev A1` | `rev H1` | a refinement drafted in App becomes a draft (DEL-02-02) until reviewed and registered; the host copy stays `rev H1` until the host registers a change |
| derived-from | none | project / FX-PROJ / `support-adjustment-check` / `rev A1` | host / FX-HOST / … / `rev H1` if saved as a new App workflow |

Adaptation shown in `rev H1` (fixture): `‹C: modify support›` replaced by the
host's own `‹C: adjust hanger›`; `CP-accept` scope limited to whole-batch.
Checkpoint names are kept, so interruption/replay history stays traceable; the
required act kinds are unchanged. A consumer comparing `rev A1` and `rev H1`
must report the changed tool reference and scope, not treat them as the same
declared content because the names match.

---

## E4 — Same-name collision (fixture)

In the App, project FX-PROJ has `support-adjustment-check` `rev A1`
(project). The person explicitly selects the host-supplied
`support-adjustment-check` `rev H1` (origin host, FX-HOST) for a run.

| Step | Discovery shows | Selection holds | Required consumer behavior |
|---|---|---|---|
| 1 | project `rev A1`; host `rev H1` — collision reported | host / FX-HOST / `rev H1` (explicit) | Both origins listed (C-1). |
| 2 | A user-library copy `rev U1` appears | unchanged | Collision now lists three origins; no rebinding even though project/user precede in Root ordering (C-2, C-5). |
| 3 | Host library changes to `rev H2` | `rev H1` selected; whether the run follows `rev H2` is DEL-02-02/host selection policy (U-10) | The identity chain shows which revision was resolved and supplied (C-4). |
| 4 | Person explicitly reselects project `rev A1` | project / FX-PROJ / `rev A1` | Recorded as a new selection event, not a rebinding (C-3). |

---

## E5 — A Root prose-only workflow read under v4 (fixture reading of real bytes)

Root's bundled `create-workflow` has front matter `name`/`description`, prose,
and no `execution.json` or declared part (repo 6e18505e3). Read by a v4
consumer:

| Category | Reading |
|---|---|
| Expected inputs | **undeclared** (prose describes them) |
| Required tools | **undeclared** → required-tool check **not established** |
| Checkpoints | **undeclared** → the prose's human review before registration is not product-held; a consumer may point to the prose (FB-07 style report) but shall not synthesize a checkpoint |
| Outputs / evidence | **undeclared** |
| Identity | kind workflow; origin bundled; source root `chirality-root`; name `create-workflow`; revision per U-03 |

This is expected, not a defect of Root: Root packages predate the declared
part. It is a receiving fact for DEL-02-03 and for adoption owners.

---

## E6 — Root restriction misread as requirement (negative fixture)

Root `workflows/project-dag/execution.json` (repo 6e18505e3) declares
`compatible_roles: [WORKING_ITEMS]` and `tools.capabilities: [read, write,
bash, delegate_agent, report_coordination_notice, send_agent_update,
ack_agent_update]`.

| Reading | Verdict |
|---|---|
| "The workflow requires these seven tools; check them against the host" | **Incompatible.** These are a restriction ceiling intersecting outer policy (AGENT_WORKFLOW_RUNTIME.md), not V4-WF-01 required host tools (WD-v0.1 §4.2.3). |
| "Required tools undeclared; restriction retained; compatible role WORKING_ITEMS; a host seat without delegation reports it unsupported" | **Compatible** (FB-05; §4.7). |

## UNRESOLVED

Same register as WD-v0.1 §12; items that shape these examples:

| item | owner | point of need | effect on these examples |
|---|---|---|---|
| U-01/U-02 carriage and wire names | DEL-02-01 with consumers | before OUT-002 schema / OUT-004 fixtures | Tables are illustrative renderings only |
| U-03 revision algorithm | DEL-02-01 with DEL-04-03, DEL-02-02 | before revision comparisons | `rev A1`, `rev H1` are labels |
| U-04 act-kind names | DEL-04-01 | V1 | *accept a proposed edit*, *mark checked* to be reconciled |
| U-07 operation identities/versions | DEL-03-01 | V1 | `‹C: …›` placeholders |
| U-09 host seat role mapping | DEL-02-01 with SWB owner, DEL-02-04 | before host role guidance | E1 compatible roles are a fixture choice |
| U-10 precedence and revision following | DEL-02-02 with host owner | before host-origin discovery | E4 step 3 left open |
| U-15 `UNRESOLVED{OI-021}` first operation | owner via outside SWB session | before connected-activity SoW | E1 operations are not the selected operation |
| U-05/U-06 `UNRESOLVED{OI-001}` / `UNRESOLVED{OI-002}` | owner with App/SWB contract owners | policy points of need | No example treats an act as agent-performable or a checkpoint as a permission prompt |

## Verification cases

These examples are the inputs for WD-v0.1 §13 cases; none has been run.

| Example | Used by | Expected result summary | VER |
|---|---|---|---|
| E1 | VC-01, VC-03, VC-05, VC-16 | Five categories and prose recovered; roles readable in App and host seat; references compared to C when received | VER-001, VER-002, VER-003 |
| E2 R-1…R-7 | VC-07…VC-11, VC-15 | Only evidenced acts reported; holds and lapse as tabulated; unknown stays unknown | VER-003, VER-004 |
| E3 | VC-02, VC-14 | New identity with derived-from; changed tool/scope reported | VER-001, VER-004 |
| E4 | VC-13 | No rebinding; all origins exposed | VER-004 |
| E5 | VC-04 | All categories undeclared | VER-002 |
| E6 | VC-06 | Restriction not read as requirement | VER-002 |
| Inventory | VC-19 | Examples identified by this contribution version; all "designed, not run" | VER-007 |
