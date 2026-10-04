# Fleet views: return-review queue and waiting causes

- Contribution: DEL-06-02/FV-v0.1 (new). Covers OUT-001 (queue and waiting
  views), OUT-003 (their fixtures; prototype only) and the OUT-004 derivation
  boundary for these views. The decision-package view is
  [DECISION_VIEW.md](DECISION_VIEW.md) (DV-v0.1); the two files together are
  DEL-06-02's design.
- Status: DRAFT DEFINITION — proposed, unsupplied, not implemented, not
  accepted. The prototype in `prototype/` is not product code; no App
  candidate exists.
- Run and owner: `APP-V4-DESIGN-PASS-4-20261003`, owner O-A, unit E-2;
  written 2026-10-03.
- Basis (sha256): this deliverable's `ScopeOfWork.md`
  3f6bb7b8344a83158530758dea6c7f69e797c30147458a8ae506359589c8ded7 (INIT
  contract; no SCA-V4-001/002/003 block changed it). Basis clauses:
  `docs/PRD.md` V4-PM-03, 05, 06, V4-REC-02/03; `docs/ARCHITECTURE.md` §3;
  `docs/HOST_INTEGRATION.md` V4-HI-61…63 and the §8 fallback;
  `docs/EXAMINATION.md` V4-EXM-13; `docs/OPERATING_METHOD.md` V4-OPS-30…32.
  Rulings: R23-2, R23-4, R23-8, R23-9, R23-21.
- Supplier read: DEL-06-01/FR-v0.1 (`FLEET_RECORDS.md` §3, §5, §6) and its
  reader `prototype/fleet_store.py`, consumed through DEP-06-02-008
  (admitted). It is a pass-4 file of the same owner, so this file pins it by
  label.
- **Repairs after RV-E2 (in place, same label FV-v0.1, before acceptance).**
  - E2-R1: FV-8a, and VER-006 probes P1 and P2 that lose a real record.
  - E2-R2: P3, a torn RS line.
  - E2-R3: FV-4a.
  - E2-R4: the qualified label and first cause, with a check that no
    qualified row renders as bare *ready*.
- Pin (R23-3): no Codex fact is relied on directly. The views show Codex's
  status values unchanged, as DEL-06-01 records them.

## 1. What the views are

Two derived views over DEL-06-01's records (V4-PM-03, V4-PM-06), beside the
decision view:

- the **return-review queue**: returned work awaiting examination or
  integration, with who returned it and who examines it;
- the **waiting view**: every selected item of the current graph, with its
  category and the cause its records evidence, or an explicit gap.

They hold nothing of their own. A rebuild from the same files gives the same
rows, and writes nothing (X-18: deleting the views degrades throughput, never
correctness).

## 2. Inputs

| Input | Owner | Used for | Missing |
|---|---|---|---|
| DEL-06-01 reader facts: per item, the selected, brief, dispatch, observed, return, review, integration, needs, basis-change, related and external facets (FR §5), and the child index | DEL-06-01 | Every row | No current graph → no rows, with the reason |
| RS `act_request` and `human_act` records, read by DEL-06-01's decision-need rule (FR RF-6) | DEL-04-03 | Decision waits | "cause not established", never ready |
| The brief's `preparedBy` | DEL-06-01 | Who examines and integrates a return | "not recorded" |

Not inputs (**SETTLED** by REQ-005, V4-REC-03, CAP-7): conversation text,
including an agent saying work is done; native running status other than as
DEL-06-01 recorded it; PEC.

## 3. Return-review queue (REQ-001; AC-001; PROPOSED rules)

- **FV-1 Membership.** An item enters only on a `return_recorded` record
  (FR §3.3). It leaves only on an `integration_recorded` record on that
  return. A child's `completed`, an observation ending, a success message or
  a rebuild never moves an item in or out.
- **FV-2 Row.** The row shows:
  - the item and its outcome;
  - its state: *awaiting review*, *reviewed — findings to repair*, *review
    not concluded*, or *reviewed — awaiting integration*;
  - who returned it and who recorded the return;
  - the examiner, once a review is recorded;
  - **who examines it**: the brief's preparer, as the brief records it;
  - the source records.
- **FV-2a No invented examiner (owner O-A's decision, 2026-10-03).** When no
  brief records who prepared it, the row says "examiner not established". The
  work graph's item owner is not used as a fallback: in practice that owner is
  usually the executor (in FX-FL1, the TASK child), and naming the executor as
  the examiner would invent an examination owner the records do not give
  (V4-PM-03; managers keep review ownership, CLM-003). A manager who wants a
  named examiner records a brief, or a review once it is done.
- **FV-3 No promotion.** "Reviewed" is not "integrated". Neither is checking
  (A4), acceptance (A5) or approval (A6), which appear only from RS human-act
  records and are labelled per ACT §9.

## 4. Waiting view (REQ-002; AC-002; PROPOSED rules)

**FV-4 Categories.** Each selected item falls into exactly one:

| Category | When (from DEL-06-01's facts) | Cause shown |
|---|---|---|
| done | Integration recorded, or an external result recorded | "integrated" · "external result (‹owner›)" |
| returned | A return recorded, not integrated | "in the return queue" or the review's verdict |
| in progress | Dispatch observed and the last observation is a running status | "Codex reports ‹status› (‹source›)" |
| unknown | The child's observation ended; or Codex reports the child completed and no return is recorded; or a need cannot be established | "observation ended (‹cause›); last observed ‹status›; outcome unknown" · "Codex reports the child completed; no return recorded" · "cause not established: …" |
| waiting | A need is outstanding, or an external owner has not returned | "waits for ‹item› (not integrated)" · "waits for the person's decision: decision pending on ‹request›" · "waits for input ‹file›" · "waits for the external owner ‹owner›" |
| ready · ready (qualified) | All needs are satisfied, with no dispatch, return or integration; *ready (qualified)* while an unassociated or orphaned child exists (FV-4a) | "ready: inputs satisfied" (plus "brief prepared, no dispatch observed" where it applies), with FV-4a's qualifier first when qualified |

**Annotations, under any category except done:**
- **FV-4a Ready, qualified (RV E2-R3).** While the child index holds a child
  with no brief reference, or an orphaned observation (DEL-06-01 RF-12),
  every *ready* row is labelled **ready (qualified)**. Its **first** cause is
  "‹n› child(ren) observed without a brief reference or dispatch record
  (‹threads›); a dispatch for this item may be unrecorded", and it carries
  `readinessQualified` (RV E2-R4: no display of the label, or of the label
  and first cause, can read as bare *ready*). It is not made *unknown*,
  because no record ties that child to this item. Making every not-done item
  *unknown* for any unassociated child would hide all readiness behind one
  unreferenced spawn. The qualifier keeps the claim honest instead.
- **FV-5** "basis changed since: ‹record›";
- "related conversation: ‹thread› (continued from / forked from ‹source›)".
  It is shown as related work, never as a dispatch (R23-9).

**Further rules:**
- **FV-6 Decisions.** A satisfied decision need is shown as recorded, with
  the act and the chosen alternative, for example "decision recorded:
  rec:… (A16, ALT-2)". What the chosen alternative means for the work is not
  interpreted by the view. The manager reflects it in the next graph
  revision.
- **FV-7 No invented taxonomy** (VER-002). The categories describe what the
  records support; each cause quotes its source. A cause the records do not
  give is shown as "cause not established", never filled in.
- **FV-8 Missing input never implies.** No current graph, a torn log line or
  absent RS records produce limits and *unknown* rows. They never produce an
  empty queue, readiness or permission (V4-HI-62; REQ-006).
- **FV-8a Incomplete log (RV E2-R1).** While any coordination-log line is
  unread (DEL-06-01 RF-10), an unread line could be any record of any item.
  Therefore:
  - every row that is not *done* becomes *unknown*, with "coordination log
    incomplete: line(s) ‹n› unread; this item's state cannot be
    established", followed by what the readable records show;
  - no row is *ready*;
  - the queue is marked **not complete** (`queueComplete` false), so an
    empty or short queue is never presented as the whole.

  The queue is also not complete when an observation is orphaned (RF-12) or
  no current graph exists. *Done* rows stay done: their integration or
  external-result record was read.
- **FV-9 Derived only.** A rebuild writes nothing, and the input hashes are
  equal before and after.

## 5. Sequences and failure behaviour

| Sequence | Steps | Failure → behaviour |
|---|---|---|
| Open the views | 1 read the current graph through DEL-06-01; 2 read the log and briefs; 3 read RS records for decisions; 4 derive the rows | 1: no selector, or the selected revision changed → no rows and the reason shown (FR RF-1). 2: a torn or nonconformant line → listed limit, not used. 3: absent → decision waits *unknown* |
| Rebuild after relaunch or in another session | The same steps from the files | Identical rows (VER-005). A conversation recovered from Codex adds nothing (ARCH §3) |
| A return arrives | The manager records `return_recorded`; the next build queues it | No record → not queued, whatever the conversation says |
| Interrupted observation | DEL-06-01 records `observation_ended` | The row moves to *unknown*; nothing is promoted or cleared |
| The basis changes | DEL-06-01 records `basis_changed` naming items | The annotation appears; the category does not change by itself |

## 6. Interfaces

| Direction | With | What | Failure |
|---|---|---|---|
| Consumed (DEP-06-02-008, admitted) | DEL-06-01 | The reader's facts and records | As §5 |
| Consumed (DEP-06-02-010, admitted) | DEL-04-03 | Act records, through DEL-06-01's decision rule; labels | As §5 |
| Consumed (DEP-07-02-015, admitted, PENDING) | DEL-07-02 | The source-file recovery route and connector limitation states, once DEL-07-02 is designed | Not yet available: no connector state is shown; nothing else changes |
| Offered (DEP-06-02-011 / DEP-09-05-007) | DEL-09-05 | The views and FX-FL1 rows for the joined witness | — |
| Runtime value (no row; R23-2) | DEL-01-04 | From a pending decision row, the package to the act control (DECISION_VIEW §5) | — |

## 7. Verification (designed; `prototype/run_views.py` over DEL-06-01's FX-FL1 and FX-DP1's RS records)

| VER | Cases |
|---|---|
| VER-001 | W8's return queued *awaiting review* with returner and examiner; a return on an item with no brief shows "examiner not established" (FV-2a); W7's child completed and an agent claims it done, but it is not queued and stays *unknown*; W1 left the queue only on its integration record |
| VER-002 | Ready rows are labelled *ready (qualified)*, with the unassociated child `thr-cx` as their first cause; no qualified row renders as bare *ready* (FV-4a). With every line read, the queue is complete. W3 waits for W2, with basis-change and related-conversation annotations; W5 waits for the person's decision on PKG-2; W4 is ready with the A16 decision shown; W2 is *unknown* after quit; W9 is ready once W6's external result and its input exist; no item has a blank cause |
| VER-005 | A separate process rebuilds identical views; input hashes unchanged |
| VER-006 | Without RS records, decision waits are "cause not established". An extra torn line is a limit and marks the queue incomplete. **P1:** W8's return line is truncated: the queue is not complete, W8 is *unknown* (never *in progress*), and no item is *ready*. **P2:** W2's dispatch line is truncated: W2 is *unknown* (never "ready … no dispatch observed") and its orphaned observation is a limit. **P3:** the A16's RS line is truncated: no crash, a limit, and W4's decision need is *unknown*. With no graph selected, no rows and the reason. No PEC input |
| VER-003, VER-004 | The decision view (DECISION_VIEW §8; run folder `E/`) |
| VER-007 | §6 and DECISION_VIEW §7: inputs, owners, the runtime value, the handoff to DEL-09-05 without a joined claim |

Result on 2026-10-03, after the RV-E2 repairs (with E2-R4): 23/23.

## 8. Open matters

| Matter | Owner | Point of need |
|---|---|---|
| Connector limitation states in waiting causes (DEP-07-02-015) | DEL-07-02 (tranche 2) | When DEL-07-02 is designed |
| Layout and notification are not designed here: no notification exists (AAC AK-b; OI-006) | — | — |
| Content-identity method (TEST VALUE, RS U-04) | Owner with DEL-04-03 | Before reliance |
