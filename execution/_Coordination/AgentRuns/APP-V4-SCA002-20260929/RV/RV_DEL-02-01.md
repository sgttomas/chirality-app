# RV return — DEL-02-01 (scope-of-work MODE=REVISE, closing MODE=VERIFY)

Run `APP-V4-SCA002-20260929`, node AK2 (propagation stage 1), Type 2 TASK (no delegation). Basis commit `851ec3d88` (working tree carries the uncommitted group-3 application).

## Result

**PASS.** Every F-block for DEL-02-01 in `AMENDMENT_PACKET/SOW_REVISIONS.md` applied exactly; the revised contract validates and the closing VERIFY passes.

## Bound inputs

- **Deliverable path:** `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-01_Portable workflow contract and shared allocation/`
- **MODE:** REVISE, closing with VERIFY.
- **SOURCE_STATE:** `IN_PROGRESS` (from `_STATUS.md`, "Current State"); REVISE admits it.
- **AMENDMENT_REF:** `SCA-V4-002`; accepted snapshot `projects/chirality-app-v4/execution/_ScopeChange/SCA-V4-002_2026-09-29_1901/` (group 3 accepted, DECISION-3; groups 1–2, DECISION-2); `Amendment_Actions.csv` ActionSeq 2, `MODIFY` `DELIVERABLE` DEL-02-01 (register sha256 `158702bf610777e008e304268fcbd967756f9186ded946942430a391957c579d`; `ScopeChanging` NO).
- **REVISION_SCOPE source:** `AMENDMENT_PACKET/SOW_REVISIONS.md` sha256 `440d4d50abd4d6bd2a639cfb2bcaa8bcc83a6c94061a27f9fc91e67c6a12d00d` (bound by the group-2 and group-3 manifests).
- **REVISION_SCOPE:** CLM-002 (one appended sentence); new AX-006.
- **Conditional edits:** the Q-4 arc sentence; Q-4 accepted, all four arcs kept (DECISION-2).
- **Tokens filled from the accepted records:** `{AMENDMENT_ID}` = `SCA-V4-002`; `{AMENDMENT_SNAPSHOT}` = `SCA-V4-002_2026-09-29_1901` (`_ScopeChange/_LATEST.md`, `Latest:` line). No other byte was supplied by this run.
- **Status policy:** `NO_STATUS_TOUCH`. `_STATUS.md` was not touched.

## Hashes

- **PRIOR_CONTRACT_SHA256:** `6ccc860ba48aee9392fbf90fef323577c7599655164442e6f3fb0b78fe36f0dc`. It equals the prior hash SOW_REVISIONS records for DEL-02-01 and the bytes at `HEAD` (`851ec3d88`).
- **Revised ScopeOfWork.md sha256:** `ef360edf28f5f463ae961495e04e566ab9ec9d56c0a4fd4f35e67b87adb82f17`
- **`_STATUS.md` sha256 (unchanged, byte-identical to `HEAD`):** `9e05735edd3c742dc542614e5c0cce27619b07d80a676b679ad1392cca48e7cb`

## F-blocks applied (in listed order)

| F-block | Replacements | `old` occurrences at application |
|---|---|---|
| F-0201-01 · CLM-002 (consumption sentence) · item 2, arc N-18 · conditional (Q-4) | 1 | 1 |
| F-0201-02 · new AX-006 (amendment reference) · acceptance-conditional | 1 | 1 |

2 blocks, 2 old → new replacements. No block failed; no wording was improvised.

- **Revised:** CLM-002 (per REVISION_SCOPE).
- **Added IDs:** AX-006 (amendment reference).
- **Removed IDs:** none. No ID renumbered or reused; frontmatter unchanged.

## Validation

- `validate_scope_of_work.py` on the prior contract (REVISE precondition): valid, format `SOW_V1`, issues 0.
- `validate_scope_of_work.py --json` on the revised contract: valid `True`, format `SOW_V1`, issues 0.
- `derive_review_checklist.py`: 7 `AC-*` items (7 defined in the contract, same order), bound to sha256 `ef360edf28f5f463ae961495e04e566ab9ec9d56c0a4fd4f35e67b87adb82f17`; checklist JSON sha256 `8e9eb8a1c5d89fb2aac3dc08f936ed029d8d62e30a36142f0e42a1b8d8a71ee1`; repeated derivation byte-identical: True.
- `check_boundary_owner_resolution.py --json`: status OK; findings 0; requirements checked 1, not checkable 0 (report sha256 `c3d6a380842fb14d63e7b377305297210fe882e9f5da522ee810ccba1aacec15`).
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
| 22 — amendment accepted at group 3 and names DEL-02-01 `MODIFY`; state admitted and unchanged; reverse-applying every `new` → `old` on the revised file reproduces the prior bytes exactly (REVERSE_EQUALS_PRIOR 2 pairs), so nothing outside REVISION_SCOPE and the AX line changed; no ID removed, renumbered or reused; AX reference present and the snapshot path exists | PASS |
| 1 — pilot variance | Recorded: the validator resolves the contract as `SOW_V1` without any migration variance; none is needed for a `SOW_V1` REVISE |
| 2, 5–7, 10–12, 14, 17 | NOT_APPLICABLE (CONVERT only) |
| 15 | NOT_APPLICABLE (no HTML requested) |

**Write footprint:** in the deliverable folder only `ScopeOfWork.md` is modified (`git status`: ['projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-01_Portable workflow contract and shared allocation/ScopeOfWork.md']); `_STATUS.md`, `Dependencies.csv`, `_DEPENDENCIES.md` and all other files are untouched.

## Diff, prior → revised (for the independent check)

```diff
--- prior
+++ revised
@@ -60 +60 @@
-- **CLM-002** — Within the App v4 project, `DEL-03-01` owns capability-catalog/read-basis semantics and supplies required-tool capability descriptors; `DEL-04-01` defines and carries adopted operation policy and human-act distinctions, including the first-increment OI-001/OI-002 rulings (`APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2/D3); operation-specific additions remain with the owner via the outside SWB session (OI-021); `DEL-03-02` owns proposal/outcome semantics, including item dispositions, item-left events and the governing checkpoint constraint (governance phase); `DEL-01-01` supplies the harness capability inventory and supplied-guidance identity evidence; `DEL-03-03` receives the declared checkpoint constraints, for carriage on the external channel in the governance phase; `DEL-04-03` owns human-act/run record fields and App record handling; `DEL-05-01` owns minimal-loop receiving requirements and `DEL-05-02` owns host-panel receiving requirements. `DEL-02-02` owns App workflow authoring/review/registration experience, `DEL-02-03` owns workflow execution compatibility and transfer behavior, and `DEL-02-04` owns App role selection and additive supply. These are receiving interfaces, not transferred implementation assignments. Source: Accepted decomposition, Deliverables.csv corresponding rows, Packages.csv PKG-02 through PKG-05 and Open_Issues.csv OI-001/OI-002.
+- **CLM-002** — Within the App v4 project, `DEL-03-01` owns capability-catalog/read-basis semantics and supplies required-tool capability descriptors; `DEL-04-01` defines and carries adopted operation policy and human-act distinctions, including the first-increment OI-001/OI-002 rulings (`APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2/D3); operation-specific additions remain with the owner via the outside SWB session (OI-021); `DEL-03-02` owns proposal/outcome semantics, including item dispositions, item-left events and the governing checkpoint constraint (governance phase); `DEL-01-01` supplies the harness capability inventory and supplied-guidance identity evidence; `DEL-03-03` receives the declared checkpoint constraints, for carriage on the external channel in the governance phase; `DEL-04-03` owns human-act/run record fields and App record handling; `DEL-05-01` owns minimal-loop receiving requirements and `DEL-05-02` owns host-panel receiving requirements. `DEL-02-02` owns App workflow authoring/review/registration experience, `DEL-02-03` owns workflow execution compatibility and transfer behavior, and `DEL-02-04` owns App role selection and additive supply. These are receiving interfaces, not transferred implementation assignments. Checkpoint subject binding and item-level decisions consume `DEL-03-02`'s change-item content identities, per-item dispositions, all-items-decided indication, item-left events and applied-outcome object identities; this contract does not define them. Source: Accepted decomposition, Deliverables.csv corresponding rows, Packages.csv PKG-02 through PKG-05 and Open_Issues.csv OI-001/OI-002.
@@ -126,0 +127 @@
+- **AX-006** — Revised under scope-change amendment `SCA-V4-002` (accepted snapshot `projects/chirality-app-v4/execution/_ScopeChange/SCA-V4-002_2026-09-29_1901`), applying `APP-V4-BASIS-ALIGN-20260928-DECISION-10` (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-BASIS-ALIGN-20260928/OWNER_DECISIONS.md`), which routed this contract's statement of the proposal-contract outputs it consumes to this amendment. Revised: CLM-002. Added: AX-006. Removed: none.
```
