# RV return — DEL-09-07 (scope-of-work MODE=REVISE, closing MODE=VERIFY)

Run `APP-V4-SCA002-20260929`, node AK2 (propagation stage 1), Type 2 TASK (no delegation). Basis commit `851ec3d88` (working tree carries the uncommitted group-3 application).

## Result

**PASS.** Every F-block for DEL-09-07 in `AMENDMENT_PACKET/SOW_REVISIONS.md` applied exactly; the revised contract validates and the closing VERIFY passes.

## Bound inputs

- **Deliverable path:** `projects/chirality-app-v4/execution/PKG-09_Candidate examination and connected journeys/1_Working/DEL-09-07_Local host candidate qualification/`
- **MODE:** REVISE, closing with VERIFY.
- **SOURCE_STATE:** `INITIALIZED` (from `_STATUS.md`, "Current State"); REVISE admits it.
- **AMENDMENT_REF:** `SCA-V4-002`; accepted snapshot `projects/chirality-app-v4/execution/_ScopeChange/SCA-V4-002_2026-09-29_1901/` (group 3 accepted, DECISION-3; groups 1–2, DECISION-2); `Amendment_Actions.csv` ActionSeq 4, `MODIFY` `DELIVERABLE` DEL-09-07 (register sha256 `158702bf610777e008e304268fcbd967756f9186ded946942430a391957c579d`; `ScopeChanging` NO).
- **REVISION_SCOPE source:** `AMENDMENT_PACKET/SOW_REVISIONS.md` sha256 `440d4d50abd4d6bd2a639cfb2bcaa8bcc83a6c94061a27f9fc91e67c6a12d00d` (bound by the group-2 and group-3 manifests).
- **REVISION_SCOPE:** CLM-002 (policy clause); TBD-002; TBD-003; new AX-005.
- **Conditional edits:** none of this deliverable's F-blocks is conditional on an owner item.
- **Tokens filled from the accepted records:** `{AMENDMENT_ID}` = `SCA-V4-002`; `{AMENDMENT_SNAPSHOT}` = `SCA-V4-002_2026-09-29_1901` (`_ScopeChange/_LATEST.md`, `Latest:` line). No other byte was supplied by this run.
- **Status policy:** `NO_STATUS_TOUCH`. `_STATUS.md` was not touched.

## Hashes

- **PRIOR_CONTRACT_SHA256:** `53b51d309d060089a6a88dae565867a92348789ee01430927e7464c7c2d3cba0`. It equals the prior hash SOW_REVISIONS records for DEL-09-07 and the bytes at `HEAD` (`851ec3d88`).
- **Revised ScopeOfWork.md sha256:** `813ef0f3ebcbc000df3a54093f15a0cfe9b2a75c8f6bb69a6648b1eec8e0395a`
- **`_STATUS.md` sha256 (unchanged, byte-identical to `HEAD`):** `ea0503bb7119d51c858f7b168e7100bb6882d5ef9a9a9879ea75cc36d413786e`

## F-blocks applied (in listed order)

| F-block | Replacements | `old` occurrences at application |
|---|---|---|
| F-0907-01 · CLM-002, policy clause · item 3 | 1 | 1 |
| F-0907-02 · TBD-002 · item 3 | 1 | 1 |
| F-0907-03 · TBD-003 · item 3 | 1 | 1 |
| F-0907-04 · new AX-005 (amendment reference) · acceptance-conditional | 1 | 1 |

4 blocks, 4 old → new replacements. No block failed; no wording was improvised.

- **Revised:** CLM-002, TBD-002, TBD-003 (per REVISION_SCOPE).
- **Added IDs:** AX-005 (amendment reference).
- **Removed IDs:** none. No ID renumbered or reused; frontmatter unchanged.

## Validation

- `validate_scope_of_work.py` on the prior contract (REVISE precondition): valid, format `SOW_V1`, issues 0.
- `validate_scope_of_work.py --json` on the revised contract: valid `True`, format `SOW_V1`, issues 0.
- `derive_review_checklist.py`: 8 `AC-*` items (8 defined in the contract, same order), bound to sha256 `813ef0f3ebcbc000df3a54093f15a0cfe9b2a75c8f6bb69a6648b1eec8e0395a`; checklist JSON sha256 `f3a1b4eb5c626a5bd3f10da7b6941a1c8b8d6cdc34b38836307cb4124a6f83e3`; repeated derivation byte-identical: True.
- `check_boundary_owner_resolution.py --json`: status OK; findings 0; requirements checked 1, not checkable 0 (report sha256 `81210a9c51aae436846dc69fe1fdd21bff31b96bf703706c8e474faec9b73195`).
- Checklist and boundary JSON are in the task scratch folder, outside this write scope; both are deterministic and regenerable from the revised contract.

## MODE=VERIFY (read-only)

| Check (checks.md) | Result |
|---|---|
| 3 — `_STATUS.md` byte-identical to `HEAD`, state `INITIALIZED` unchanged | PASS |
| 4 — frontmatter, headings, IDs, references and matrix validate | PASS |
| 8 — every `OUT-*` maps to scope/objective refs (validator; matrix ID columns unchanged) | PASS |
| 9 — every `AC-*` maps to a `VER-*` (checklist: every item has a verification) | PASS |
| 13, 18 — checklist has every `AC-*` once, in order, hash-bound; repeat byte-identical | PASS |
| 16 — findings separated: schema none; project content none; execution substrate none | PASS |
| 19 — no bare upstream local IDs introduced (validator; new text cites deliverables by `DEL-NN-NN` and decisions by full identity) | PASS |
| 20 — matrix grouping: matrix ID columns unchanged (evidence cells changed: 0), so no row grouping changed | PASS |
| 21 — boundary-owner resolution: no `UNRESOLVED_OWNER` or `UNDEFINED_CLAIM` | PASS |
| 22 — amendment accepted at group 3 and names DEL-09-07 `MODIFY`; state admitted and unchanged; reverse-applying every `new` → `old` on the revised file reproduces the prior bytes exactly (REVERSE_EQUALS_PRIOR 4 pairs), so nothing outside REVISION_SCOPE and the AX line changed; no ID removed, renumbered or reused; AX reference present and the snapshot path exists | PASS |
| 1 — pilot variance | Recorded: the validator resolves the contract as `SOW_V1` without any migration variance; none is needed for a `SOW_V1` REVISE |
| 2, 5–7, 10–12, 14, 17 | NOT_APPLICABLE (CONVERT only) |
| 15 | NOT_APPLICABLE (no HTML requested) |

**Write footprint:** in the deliverable folder only `ScopeOfWork.md` is modified (`git status`: ['projects/chirality-app-v4/execution/PKG-09_Candidate examination and connected journeys/1_Working/DEL-09-07_Local host candidate qualification/ScopeOfWork.md']); `_STATUS.md`, `Dependencies.csv`, `_DEPENDENCIES.md` and all other files are untouched.

## Diff, prior → revised (for the independent check)

```diff
--- prior
+++ revised
@@ -51 +51 @@
-- **CLM-002** — External SWBPIPE construction belongs to the outside SWB implementation session: model/domain store, catalog and views, validation/application/solve route, local loop/panel, native endpoint enforcement, origins/undo and host receipts. The host offers, records and presents human acts; the person actually performs the act. The person sets operation autonomy, while unresolved reserved-act/classifier policy remains with the owner and App/SWB contract owners. App/shared feature owners retain workflow/catalog/record/receiving-contract construction and local checks within PKG-02/03/04/05. Sources: HOST §§1,3–6,9,11; ARC §4; PRD V4-AUT-01…05; OPEN OI-001/002; OWNER J/O.
+- **CLM-002** — External SWBPIPE construction belongs to the outside SWB implementation session: model/domain store, catalog and views, validation/application/solve route, local loop/panel, native endpoint enforcement, origins/undo and host receipts. The host offers, records and presents human acts; the person actually performs the act. The person sets operation autonomy. Reserved acts and classifier treatment are ruled for the first increment's App/shared contracts (`APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2/D3); any reserved-act or classifier matter those rulings do not cover stays with the owner and App/SWB contract owners, with operation-specific additions under OI-021. App/shared feature owners retain workflow/catalog/record/receiving-contract construction and local checks within PKG-02/03/04/05. Sources: HOST §§1,3–6,9,11; ARC §4; PRD V4-AUT-01…05; OPEN OI-001/002; OWNER J/O.
@@ -102,0 +103 @@
+- **AX-005** — Revised under scope-change amendment `SCA-V4-002` (accepted snapshot `projects/chirality-app-v4/execution/_ScopeChange/SCA-V4-002_2026-09-29_1901`), applying `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2/D3 (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-FIRST-INCREMENT-20260928/OWNER_DECISIONS.md`). Revised: CLM-002, TBD-002 and TBD-003. Added: AX-005. Removed: none.
@@ -104,2 +105,2 @@
-- **TBD-002** — OI-001: choose always-reserved acts by concrete operation and consequence; owner is **Owner with App/SWB contract owners**; point of need is **Before operation-policy production contracts**. False attribution is already prohibited. PRD OQ-02 additionally requires the affected operation/permission contract and examination criterion to await the policy disposition. This deliverable consumes the adopted choice; it does not decide it.
-- **TBD-003** — OI-002: distinguish routine tool permissions from professional acts and settle App/host classifier treatment; owner is **Owner with App/SWB contract owners**; point of need is **Before permission-policy implementation**. No classifier behavior is selected here. As PRD OQ-02 states, the dependent examination criterion is fixed only after the applicable disposition; unrelated verification and definition remain possible.
+- **TBD-002** — OI-001 — ruled for the first increment's App/shared contracts by `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2: marking checked; accepting a proposal where the autonomy requires one; engineering approval; professional reliance; changing the grant or enabling external access. The host names and enforces its own list (HOST V4-HI-30; DEP-001). Operation-specific additions for the examined activity remain OPEN under OI-021 (TBD-001). Any matter the ruling does not cover stays with the **Owner with App/SWB contract owners**, point of need **Before operation-policy production contracts**. False attribution is already prohibited. PRD OQ-02 still requires an examination criterion that depends on such an uncovered operation to await its disposition. This deliverable consumes the adopted choice; it does not decide it.
+- **TBD-003** — OI-002 — ruled by `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D3: in the App, routine tool-permission and sandbox modes (including classifier-based modes) remain the user's own Codex setting and never stand in for a reserved or professional act; hosts have no classifier permission mode in the first increment, and the SWB default proposal mode applies (HOST V4-HI-41). Host adoption remains under DEP-001. No classifier behavior is selected here. As PRD OQ-02 states, a dependent examination criterion outside that ruling is fixed only after its disposition; unrelated verification and definition remain possible.
```
