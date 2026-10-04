# RV-E2 — review of E-2 (owner O-A): DEL-06-01 fleet records and DEL-06-02 queue and waiting views

- **Reviewer and method:** RV (Type 2 TASK, Claude Opus 5.5), run `APP-V4-DESIGN-PASS-4-20261003`, 2026-10-03. Method: `coordinated-knowledge-work` §3.
- **Basis:** R23-2, R23-4, R23-8, R23-9, R23-21 and R23-25, cited by ID.
- **Bytes reviewed:** recomputed with `shasum -a 256`; all match `OWNERS/O-A.md` "CURRENT":
  - `FLEET_RECORDS.md` (FR-v0.1) `c37edc599ad775a00afcb457d77fb659319b08ebb1f8500c8db1b0b626003fa4`
  - `fleet.record.schema.json` `e4dd5100…`
  - `fleet_store.py` `fa9590c1…`
  - `run_fleet.py` `5b1f6ec8…`
  - FX-FL1 `MANIFEST.sha256` `0489bc61…`
  - `FLEET_VIEWS.md` (FV-v0.1) `5d88a2a64ee67df5bd68c3c3aba0536633f9ff0e5585cb8f8e06420df98b0239`
  - `fleet_views.py` `b79ae183…`
  - `run_views.py` `d04d2c83…`
  - ScopeOfWork pins: DEL-06-01 `50c88c9f…`, DEL-06-02 `3f6bb7b8…`, both matching.
- **Owner checks rerun, not rebuilt:** `run_fleet.py` "all expectations held (32/32)"; `run_views.py` "all expectations held (16/16)".
- **Probes:** written to scratch under `$TMPDIR/rv/` (copies of FX-FL1). Nothing was written in the unit.

## Verdict: **REPAIR**

Counts: 1 MAJOR, 2 MINOR, 2 NOTE. Nothing is BLOCKING.

The record design is sound and keeps its facts apart. The single MAJOR: the views do not keep FV-8's promise when a torn line replaces a real record.

## Findings

### E2-R1 — MAJOR — a torn log line can empty the queue and make an item "ready" (FV-8; FR §6; VER-006)

- **What the design says.**
  - FV-8: "a torn log line … produce[s] limits and *unknown* rows. They never produce an empty queue, readiness or permission (V4-HI-62; REQ-006)."
  - FR §6: "A torn or nonconformant log line is a limit and is not used."
- **What the code does.** The reader drops the line and lists a view-wide limit, and nothing more. Rows are derived as if the dropped record never existed.
- **Probe P1.** I truncated the existing `return_recorded` line for W8 (log line 16) in a copy of FX-FL1.
  - The queue became **empty**.
  - W8 moved from *returned* to *in progress* ("dispatched; no status observed since").
  - The only trace was the limit "coordination log line 16: partial entry (not read)".
- **Probe P2.** I truncated the `dispatch_observed` line for W2's child (line 4).
  - W2 became **"ready: inputs satisfied, brief prepared, no dispatch observed"**, although its child had run.
  - The `observation_ended` entry for that child (line 15) was left orphaned and unused.
- **Why the owner's check missed it.** `run_views.py` VER-006 appends an *extra* partial line after the complete log (L106). Its check "adds no return and removes none" therefore never tests losing a record.
- **Consequence.**
  - A manager reading the view could re-dispatch work that a child already did, or miss a return awaiting review.
  - This breaks V4-HI-62, which forbids readiness from a missing feed, and REQ-006.
  - It is the property the two views exist to protect.
- **Repair.**
  - While any coordination-log line is unread, do not show *ready*, and do not present the queue as complete. For example: every row that is not *done* (integration and external results are still read) becomes *unknown* with "coordination log incomplete: line ‹n› unread", and the queue carries that limit.
  - Also flag orphans, such as a `child_observed` or `observation_ended` entry whose child has no `dispatch_observed`, as a limit.
  - Add cases that truncate an existing return line and an existing dispatch line.

### E2-R2 — MINOR — a torn RS line crashes the reader (FR §6 failure table; RF-6)

- **What FR §6 states.** "Read | Torn line; missing RS records | Limit; decision needs *unknown*."
- **What the code does.** `Reader.__init__` parses the RS file with `json.loads` on every line, with no error handling.
- **Probe.** With FX-DP1's third RS entry (the A16) truncated, `Reader(...)` raised an uncaught `JSONDecodeError`.
- **Comparison.** The coordination log, and DEL-06-02's `decision_view.read_log`, both turn a torn line into a limit. This reader should do the same.
- **Repair.** Treat an unparsable RS line as a limit. Make the decision needs that could depend on it *unknown*, not *outstanding*. Add a case.

### E2-R3 — MINOR — an unassociated child can sit behind a "ready" row (FR AS-1…AS-3; FV-4)

- **The documented gap.** AS-1 (putting the brief reference in the spawn) is guidance, not enforcement. O-A lists this in FR §11. A child spawned without the reference is indexed but associated with no item (AS-3).
- **The consequence.** The waiting view still shows that work's item as "ready: … no dispatch observed". In FX-FL1, `thr-cx` is such a child while W9 shows *ready*. "No dispatch observed" is literally true, but *ready* is a readiness claim the records do not support while an unassociated child exists in the same undertaking.
- **Repair.** Whenever the child index holds unassociated children, annotate *ready* rows with "‹n› child(ren) observed without a brief reference; a dispatch for this item may be unrecorded". Alternatively, state in FV-4 why *ready* stays unqualified.

### E2-N1 — NOTE — the brief's limit standing adds a value ROLE does not have

- FR §3.1 allows `enforced-by-host` for a brief's tool and write-scope limits.
- ROLE's `role-limit-account` and NPTD's export use only `stated-not-enforced · enforced-by-supplier · unknown`.
- The fleet schema keeps the delegating-role limit to `stated-not-enforced · unknown`, which is consistent with LA-5.
- The extra value is reasonable for a host-enforced tool, but FR should say it is FR's own (PROPOSED) and not a value handed from ROLE.

### E2-N2 — NOTE — HOSTING §6.1 citation

FR-D1 cites "HOSTING §6.1 … 'none defined'". The words are in HOSTING's §6.1 table at L783 ("App-offered tool … none defined in this increment"). The citation is right; a line reference would make it quicker to find.

## Probes the coordinator named

| Probe | Result | How |
|---|---|---|
| **R23-9:** delegation is native children only; related conversations and outside work come from files | **Holds** | FR-D5. `dispatch_observed` carries the mechanism "Codex native subagent". `related_conversation` ("continued from" or "forked from") is App-only and "never a dispatch". `external_result` is written by the manager or the person, from files, with "no execution claimed". In the views, related conversations are an annotation, never a dispatch (FV-5), and an external result only satisfies a need. Schema probe: an agent recording `related_conversation` is refused |
| **R23-4:** DEL-06-01 holds the child index | **Holds** | FR-D4 and RF-8: `item_facts` returns `childIndex` with every `dispatch_observed`, associated or not (`thr-cx` included). RECOVERY's ledger is untouched: `git diff --stat cec590c5c3` over DEL-01-02 `Design/` is empty |
| **Ordinary file tools; the App writes only what it observes; HOSTING not reopened** | **Holds** | FR-D1. Schema probes against `fleet.record.schema.json` with DEL-04-03's validator: the App as recorder of `return_recorded`, `review_recorded`, `integration_recorded`, `external_result` or `basis_changed` → refused. An agent recording `related_conversation`, or a person recording `child_observed` → refused. INV-FL-2 (an agent recording a dispatch) is in `run_fleet.py`. HOSTING, DEL-01-03 and DEL-02-04 `Design/` are unchanged since `cec590c5c3` (`git diff --stat`). The OBS-2 facts FR §4 relies on (the completed spawn's `receiverThreadIds`; `thread/list` omitting children; `thread/loaded/list` including them; LM Studio 0.4.16 dropping the namespace) are in `OBS_2_0.158.0.md` L159–166 and L269 |
| **Views derive from files and can be rebuilt (V4-PM-06)** | **Holds** | `fleet_views.py` imports only `fleet_store.Reader` and opens nothing for writing. Each row carries its sources. `run_views.py` VER-005 rebuilds the views in a separate process with input hashes unchanged |
| **FV-2a:** no invented examiner | **Holds** | `examiner_owner` returns the brief's `preparedBy`, or "examiner not established". The item owner is never used as a fallback. VER-001 covers a return without a brief |
| **Missing or torn records give limits or "unknown", never "ready"** | **Partly** | Holds for: a missing log (no current graph → no rows, with the reason); a changed graph (RF-1, not used); absent RS records (decision needs *unknown*, "cause not established"); an extra torn line. **Fails** for a torn line that *replaces* a record (E2-R1) and for a torn RS line, which crashes (E2-R2) |

## Also checked

- **Fact separation (FR §1, §5).** `item_facts` derives brief, dispatch, observation, return, review and integration each only from its own record kind (RF-2…RF-4). A child's `completed` without a return goes to *unknown*, not *returned* (W7 in the base fixture). "Reviewed" is never "integrated" (FV-3).
- **Decision needs (RF-6, R23-25).** `_decision_state` counts only a `human_act` of the requested kind citing the request, with a named alternative for A16. It drops corrected entries, then takes the latest, which matches DV-6, ACT §2.1/§2.5 and RS HA-11 (see `reviews/RV-E1.md`, repair confirmation). In the base fixture, W4 is *ready* with "decision recorded: rec:app:coord:0003 (A16, ALT-2)" and W5 waits on PKG-2. This holds on FX-DP1 at `9501ef81…`.
- **Base fixture rows.** These agree with FV VER-001 and VER-002 as stated:
  - W1 done; W2 unknown after quit; W3 waits for W2, with its annotations; W5 waiting; W6 done (external); W7 unknown; W8 returned and queued; W9 ready.

## Not checked

- Operation through a real Codex delegation. FR states that delegation is observed only through the OBS-2 adapter, and there is no candidate.
- The PEC compatibility path (OI-022). None is adopted.
- DEL-07-02 connector states. They are deferred, as FV §6 says.

## Repair confirmation (2026-10-03)

**Bytes reviewed.** Each hash was recomputed with `shasum -a 256` and matches the CURRENT section of `OWNERS/O-A.md`:

| File | sha256 |
|---|---|
| `FLEET_RECORDS.md` | `3e3ba16c9c73f941…` |
| `fleet.record.schema.json` | `e4dd5100…` (unchanged) |
| `fleet_store.py` | `c88c13444b735555…` |
| `run_fleet.py` | `eac21c3b78e239ad…` |
| FX-FL1 `MANIFEST.sha256` | `0489bc61…` (unchanged) |
| `FLEET_VIEWS.md` | `5620d8bd0bd35061…` |
| `fleet_views.py` | `fee4b24ae15d0fb2…` |
| `run_views.py` | `f2a1de95f3c99b99…` |
| `RECORD_SEMANTICS.md` | `2e7afb1bb8b872c0ba30a514a034b1aa7174e63ee782505438c95d7cd78430ff` |

**Checks rerun, not rebuilt:**

| Check | Result |
|---|---|
| `run_fleet.py` | 34/34 |
| `run_views.py` | 22/22 |
| DEL-04-03 `run_prototype.py` | "all expectations held" |
| `E/run_e.py` | 56/56 |

**My probes rerun independently** on fresh scratch copies of FX-FL1, against the repaired code:

| Probe | What was damaged | Result |
|---|---|---|
| P1 | W8's return line truncated | `queueComplete` false. W8 is *unknown*. No row is *ready*. Each not-done row leads with "coordination log incomplete: line(s) [16] unread …" |
| P2 | W2's dispatch line truncated | W2 is *unknown*. The limit "child thr-c2 observed with no dispatch_observed …" is reported. The queue is not complete |
| P3 | The A16's RS line truncated | No crash. Limit "RS records line 3: partial entry". W4's need, and W5's, become *unknown* (RF-11) |
| P4 (added) | W1's integration line truncated | W1 is no longer *done* but *unknown*. The queue is not complete. *Done* is kept only where its record was read |

### Verdict: **CONFIRMED — READY**

No BLOCKING or MAJOR finding is open. One new MINOR, E2-R4, concerns how the qualifier is presented. It is not blocking.

| Finding | Status | Confirmed against |
|---|---|---|
| E2-R1 MAJOR | **Repaired** | FR RF-10 and RF-12 (L236, L244) and FV-8a, implemented in `fleet_store` (`logIncomplete`, `orphanChildren`) and `fleet_views`. While a log line is unread, every not-done row is *unknown* and the queue is marked incomplete. P1, P2 and P4 above. VER-006 now covers lost records (P1, P2) |
| E2-R2 MINOR | **Repaired** | RF-11 (L241). P3 above. A torn RS line is a limit, and a decision need with no satisfying act becomes *unknown* while any RS line is unread |
| E2-R3 MINOR | **Repaired as FV-4a**, which the coordinator accepted on its stated reason | While an unassociated or orphaned child exists, every *ready* row carries `readinessQualified: true` and the cause "‹n› child(ren) observed without a brief reference or dispatch record (thr-cx); a dispatch for this item may be unrecorded". In FX-FL1, W4 and W9 carry it. The category is *ready* only in waiting rows, and every *ready* row has the flag and the cause. No other view shows *ready*: FR facts have no readiness, and the decision view and queue have no *ready* state. Under FV-8a, *ready* never appears (P1, P2). **But see E2-R4** |
| E2-N1 NOTE | **Adopted** | FR §3.1 (L118–120): `enforced-by-host` is "FR's own value" |
| E2-N2 NOTE | **Adopted** | FR-D1 (L60) cites the `item/tool/call` row at L783 |

**RS-v0.10 L-0 (A16).** `git diff HEAD` of `RECORD_SEMANTICS.md` changes exactly two lines (`--stat`: 2 insertions, 2 deletions). HEAD is `09ca67d094`, whose bytes are `75a32e55…`, the version I confirmed for E-1.

- The L4 change note adds "§7 L-0 (A16 supersession, R23-25)".
- The L-0 row adds one sentence. A16 is lapse-evaluated like any App-file act (L-1, L-6). A later A16 on the same package supersedes the earlier one for current standing, and the record shows *superseded by ⟨act⟩* (HA-11). An A16 on another package supersedes nothing. A correction (OF-5) is not a supersession.
- This agrees with ACT §2.1/§2.5, HA-11, DV-6 and FR RF-6.
- **Every other E-1 row (§6.1, HA-11, §13.3, §13.6) is byte-identical.**

### New item

- **E2-R4 — MINOR — the qualifier is last, so a ready row can still read as plain ready (FV-4a; `fleet_views.waiting`).**
  - **The code.** The flag and its sentence are appended *after* the other causes. The category label stays the bare `ready`.
  - **W9.** The first cause shown is "ready: inputs satisfied", and the qualifier is the last line.
  - **W4.** The first cause is "decision recorded: …", then "ready: inputs satisfied", and the qualifier is last.
  - **Consequence.** A presentation that shows the category, or the category and the first cause, would show plain *ready*. That is what the coordinator asked to rule out.
  - **Repair.** Put the qualifier on the readiness statement itself, for example "ready (qualified: ‹n› unassociated child(ren) …)". Or make it the first cause, and state in FV-4a that *ready* is never displayed without `readinessQualified` when it is set. Add a check that the qualified wording is part of the readiness cause.

## E2-R4 confirmation (2026-10-03)

- **Bytes reviewed** (`shasum -a 256`; they match the coordinator's note):
  - `FLEET_VIEWS.md` `15e25a24…1b85`
  - `fleet_views.py` `207de7a7…75d3`
  - `run_views.py` `dc49bff0…0724`
- **Owner check rerun:** `run_views.py`, "all expectations held (23/23)".

### Verdict: **E2-R4 repaired. E-2 is READY**, with no open finding.

**The specification.**
- FV-4's category table (L95) now lists *ready (qualified)*, with its condition, and the qualifier first.
- FV-4a (L98–100) states that the label is **ready (qualified)** and that the qualifier is the **first** cause.

**The code.** `fleet_views.waiting` (L130–136) puts the qualifier first (`causes.insert(0, …)`) and sets the label to `ready (qualified)` together with `readinessQualified`.

**Checked on FX-FL1, independently of the owner's test.**
- W4 and W9 are labelled `ready (qualified)`, with `readinessQualified: true`.
- Each one's first cause is "1 child(ren) observed without a brief reference or dispatch record (thr-cx); a dispatch for this item may be unrecorded".
- No other key of the built view (queue, notes, limits, graph) carries a readiness state.
- The new check, `renders_bare_ready`, together with the flag–label equality, enforces both directions: no qualified row is labelled bare `ready` or lacks the qualifier as its first cause, and no unqualified row carries the label.

**Downstream.** A grep over the DEL-06-01, DEL-06-02 and DEL-09-05 prototypes finds no other comparison with the string `"ready"` outside the view's own guard. So no consumer silently treats *ready (qualified)* as a different category. When DEL-09-05's joined witness consumes these rows, it should match both labels.
