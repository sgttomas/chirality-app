# RV return — DEL-02-03 (scope-of-work MODE=REVISE, closing MODE=VERIFY)

Run `APP-V4-SCA002-20260929`, node AK2 (propagation stage 1), Type 2 TASK (no delegation). Basis commit `851ec3d88` (working tree carries the uncommitted group-3 application).

## Result

**PASS.** Every F-block for DEL-02-03 in `AMENDMENT_PACKET/SOW_REVISIONS.md` applied exactly; the revised contract validates and the closing VERIFY passes.

## Bound inputs

- **Deliverable path:** `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-03_Workflow execution compatibility and round-trip support/`
- **MODE:** REVISE, closing with VERIFY.
- **SOURCE_STATE:** `IN_PROGRESS` (from `_STATUS.md`, "Current State"); REVISE admits it.
- **AMENDMENT_REF:** `SCA-V4-002`; accepted snapshot `projects/chirality-app-v4/execution/_ScopeChange/SCA-V4-002_2026-09-29_1901/` (group 3 accepted, DECISION-3; groups 1–2, DECISION-2); `Amendment_Actions.csv` ActionSeq 3, `MODIFY` `DELIVERABLE` DEL-02-03 (register sha256 `158702bf610777e008e304268fcbd967756f9186ded946942430a391957c579d`; `ScopeChanging` NO).
- **REVISION_SCOPE source:** `AMENDMENT_PACKET/SOW_REVISIONS.md` sha256 `440d4d50abd4d6bd2a639cfb2bcaa8bcc83a6c94061a27f9fc91e67c6a12d00d` (bound by the group-2 and group-3 manifests).
- **REVISION_SCOPE:** CLM-002 (one appended sentence); new AX-005.
- **Conditional edits:** the Q-4 arc sentence; Q-4 accepted, all four arcs kept (DECISION-2).
- **Tokens filled from the accepted records:** `{AMENDMENT_ID}` = `SCA-V4-002`; `{AMENDMENT_SNAPSHOT}` = `SCA-V4-002_2026-09-29_1901` (`_ScopeChange/_LATEST.md`, `Latest:` line). No other byte was supplied by this run.
- **Status policy:** `NO_STATUS_TOUCH`. `_STATUS.md` was not touched.

## Hashes

- **PRIOR_CONTRACT_SHA256:** `a4ffcd8711ad0ee50d9ca6876d0b19972f9f3ba9a7a129578068c4a918c24c0e`. It equals the prior hash SOW_REVISIONS records for DEL-02-03 and the bytes at `HEAD` (`851ec3d88`).
- **Revised ScopeOfWork.md sha256:** `0006521b9bd96ea7ec98ecc5d9e6db794ecb331440c276006b444e7ee319726d`
- **`_STATUS.md` sha256 (unchanged, byte-identical to `HEAD`):** `237e0982346f75a9d33417c212d6e8b7097cf2f34066f884ea01d647122a9b86`

## F-blocks applied (in listed order)

| F-block | Replacements | `old` occurrences at application |
|---|---|---|
| F-0203-01 · CLM-002 (consumption sentence) · item 2, arcs N-21, N-24, X-1 · conditional (Q-4, per clause) | 1 | 1 |
| F-0203-02 · new AX-005 (amendment reference) · acceptance-conditional | 1 | 1 |

2 blocks, 2 old → new replacements. No block failed; no wording was improvised.

- **Revised:** CLM-002 (per REVISION_SCOPE).
- **Added IDs:** AX-005 (amendment reference).
- **Removed IDs:** none. No ID renumbered or reused; frontmatter unchanged.

## Validation

- `validate_scope_of_work.py` on the prior contract (REVISE precondition): valid, format `SOW_V1`, issues 0.
- `validate_scope_of_work.py --json` on the revised contract: valid `True`, format `SOW_V1`, issues 0.
- `derive_review_checklist.py`: 7 `AC-*` items (7 defined in the contract, same order), bound to sha256 `0006521b9bd96ea7ec98ecc5d9e6db794ecb331440c276006b444e7ee319726d`; checklist JSON sha256 `1f67aacda581299acfeaa0f3a845c8c8a138090fcfb97825bd407b54baba1fa1`; repeated derivation byte-identical: True.
- `check_boundary_owner_resolution.py --json`: status OK; findings 0; requirements checked 1, not checkable 0 (report sha256 `ca5fc808737fa863fe1ca0863d138fb064ac8e5ea0ba0fe96dd2c761d73e37ae`).
- Checklist and boundary JSON are in the task scratch folder, outside this write scope; both are deterministic and regenerable from the revised contract.

## MODE=VERIFY (read-only)

| Check (checks.md) | Result |
|---|---|
| 3 — `_STATUS.md` byte-identical to `HEAD`, state `IN_PROGRESS` unchanged | PASS |
| 4 — frontmatter, headings, IDs, references and matrix validate | PASS |
| 8 — every `OUT-*` maps to scope/objective refs (validator; matrix ID columns unchanged) | PASS |
| 9 — every `AC-*` maps to a `VER-*` (checklist: every item has a verification) | PASS |
| 13, 18 — checklist has every `AC-*` once, in order, hash-bound; repeat byte-identical | PASS |
| 16 — findings separated: schema none; project content none; execution substrate none | PASS |
| 19 — no bare upstream local IDs introduced (validator; new text cites deliverables by `DEL-NN-NN` and decisions by full identity) | PASS |
| 20 — matrix grouping: matrix ID columns unchanged (evidence cells changed: 0), so no row grouping changed | PASS |
| 21 — boundary-owner resolution: no `UNRESOLVED_OWNER` or `UNDEFINED_CLAIM` | PASS |
| 22 — amendment accepted at group 3 and names DEL-02-03 `MODIFY`; state admitted and unchanged; reverse-applying every `new` → `old` on the revised file reproduces the prior bytes exactly (REVERSE_EQUALS_PRIOR 2 pairs), so nothing outside REVISION_SCOPE and the AX line changed; no ID removed, renumbered or reused; AX reference present and the snapshot path exists | PASS |
| 1 — pilot variance | Recorded: the validator resolves the contract as `SOW_V1` without any migration variance; none is needed for a `SOW_V1` REVISE |
| 2, 5–7, 10–12, 14, 17 | NOT_APPLICABLE (CONVERT only) |
| 15 | NOT_APPLICABLE (no HTML requested) |

**Write footprint:** in the deliverable folder only `ScopeOfWork.md` is modified (`git status`: ['projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-03_Workflow execution compatibility and round-trip support/ScopeOfWork.md']); `_STATUS.md`, `Dependencies.csv`, `_DEPENDENCIES.md` and all other files are untouched.

## Diff, prior → revised (for the independent check)

```diff
--- prior
+++ revised
@@ -35 +35 @@
-- **CLM-002** — PKG-03, specifically `DEL-03-01`, owns capability/catalog semantics; the external host owner implements the host catalog and actual operations. PKG-04 `DEL-04-01` defines and carries adopted operation policy, while the owner and host policy owner decide unresolved classes. PKG-04 `DEL-04-03` owns content-bound act/run-file meaning and App record writing/reading. The human performs a human act; a host offers, records and presents that act and supplies receipt evidence without becoming its decision actor. `DEL-03-02` owns proposal item dispositions, item-left events and the governing checkpoint constraint (governance phase); `DEL-04-02` owns grant display states; `DEL-03-03` owns external-channel receiving, including the governance-phase carriage assurance; `DEL-05-01` supplies arrival observation, subject binding and loop events from host loops (its host-loop hold is governance phase); `DEL-01-01` supplies observed supplier facts; `DEL-01-04` (later undertaking) constructs the App act control. Source: G3 Deliverables.csv DEL-01-01, DEL-01-04, DEL-03-01, DEL-03-02, DEL-03-03, DEL-04-01/02/03, DEL-05-01; current HOST_INTEGRATION.md §1, V4-HI-30/31/32; PRD.md V4-AUT-03, V4-REC-03/05.
+- **CLM-002** — PKG-03, specifically `DEL-03-01`, owns capability/catalog semantics; the external host owner implements the host catalog and actual operations. PKG-04 `DEL-04-01` defines and carries adopted operation policy, while the owner and host policy owner decide unresolved classes. PKG-04 `DEL-04-03` owns content-bound act/run-file meaning and App record writing/reading. The human performs a human act; a host offers, records and presents that act and supplies receipt evidence without becoming its decision actor. `DEL-03-02` owns proposal item dispositions, item-left events and the governing checkpoint constraint (governance phase); `DEL-04-02` owns grant display states; `DEL-03-03` owns external-channel receiving, including the governance-phase carriage assurance; `DEL-05-01` supplies arrival observation, subject binding and loop events from host loops (its host-loop hold is governance phase); `DEL-01-01` supplies observed supplier facts; `DEL-01-04` (later undertaking) constructs the App act control. This slice consumes, and does not define: `DEL-03-02`'s per-item dispositions, item-left events, all-items-decided indication, change-item content identities and applied outcomes with their resulting objects, for checkpoint recording and interrupted or replayed history (REQ-002, REQ-003); `DEL-03-03`'s observations of checkpoint arrivals and act records on the external channel, which this slice records (REQ-002, REQ-003); and `DEL-01-04`'s App act control and person identity, for the App-side positive capture fixtures (OUT-003, VER-003), which await that later undertaking. Source: G3 Deliverables.csv DEL-01-01, DEL-01-04, DEL-03-01, DEL-03-02, DEL-03-03, DEL-04-01/02/03, DEL-05-01; current HOST_INTEGRATION.md §1, V4-HI-30/31/32; PRD.md V4-AUT-03, V4-REC-03/05.
@@ -75,0 +76 @@
+- **AX-005** — Revised under scope-change amendment `SCA-V4-002` (accepted snapshot `projects/chirality-app-v4/execution/_ScopeChange/SCA-V4-002_2026-09-29_1901`), applying `APP-V4-BASIS-ALIGN-20260928-DECISION-10` (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-BASIS-ALIGN-20260928/OWNER_DECISIONS.md`), which routed this slice's statement of the proposal, external-channel and App act-control inputs it consumes to this amendment. Revised: CLM-002. Added: AX-005. Removed: none.
```
