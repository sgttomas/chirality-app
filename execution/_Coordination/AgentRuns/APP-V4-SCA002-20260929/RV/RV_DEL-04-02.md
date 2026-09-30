# RV return — DEL-04-02 (scope-of-work MODE=REVISE, closing MODE=VERIFY)

Run `APP-V4-SCA002-20260929`, node AK2 (propagation stage 1), Type 2 TASK (no delegation). Basis commit `851ec3d88` (working tree carries the uncommitted group-3 application).

## Result

**PASS.** Every F-block for DEL-04-02 in `AMENDMENT_PACKET/SOW_REVISIONS.md` applied exactly; the revised contract validates and the closing VERIFY passes.

## Bound inputs

- **Deliverable path:** `projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-02_Visible autonomy and result standing/`
- **MODE:** REVISE, closing with VERIFY.
- **SOURCE_STATE:** `IN_PROGRESS` (from `_STATUS.md`, "Current State"); REVISE admits it.
- **AMENDMENT_REF:** `SCA-V4-002`; accepted snapshot `projects/chirality-app-v4/execution/_ScopeChange/SCA-V4-002_2026-09-29_1901/` (group 3 accepted, DECISION-3; groups 1–2, DECISION-2); `Amendment_Actions.csv` ActionSeq 8, `MODIFY` `DELIVERABLE` DEL-04-02 (register sha256 `158702bf610777e008e304268fcbd967756f9186ded946942430a391957c579d`; `ScopeChanging` NO).
- **REVISION_SCOPE source:** `AMENDMENT_PACKET/SOW_REVISIONS.md` sha256 `440d4d50abd4d6bd2a639cfb2bcaa8bcc83a6c94061a27f9fc91e67c6a12d00d` (bound by the group-2 and group-3 manifests).
- **REVISION_SCOPE:** CLM-004 (first sentence); new AX-005.
- **Conditional edits:** the Q-6 blocks for this deliverable; Q-6 accepted (DECISION-2, "accept the remaining items as recommended").
- **Tokens filled from the accepted records:** `{AMENDMENT_ID}` = `SCA-V4-002`; `{AMENDMENT_SNAPSHOT}` = `SCA-V4-002_2026-09-29_1901` (`_ScopeChange/_LATEST.md`, `Latest:` line). No other byte was supplied by this run.
- **Status policy:** `NO_STATUS_TOUCH`. `_STATUS.md` was not touched.

## Hashes

- **PRIOR_CONTRACT_SHA256:** `e077f20a95efc193e4de5489824e84278449b64dda615fb913c9dbd6070122f9`. It equals the prior hash SOW_REVISIONS records for DEL-04-02 and the bytes at `HEAD` (`851ec3d88`).
- **Revised ScopeOfWork.md sha256:** `f16ffa8a33cbfb2e78a8e916e90aff9fb44ad20adf94fe61a559a213f5564460`
- **`_STATUS.md` sha256 (unchanged, byte-identical to `HEAD`):** `b429eebf9e8962c6c2be8057b0fad6b72908d17887043847baee175ecc69c609`

## F-blocks applied (in listed order)

| F-block | Replacements | `old` occurrences at application |
|---|---|---|
| F-0402-01 · CLM-004, first sentence · conditional (Q-6) | 1 | 1 |
| F-0402-02 · new AX-005 (amendment reference) · conditional (Q-6), acceptance-conditional | 1 | 1 |

2 blocks, 2 old → new replacements. No block failed; no wording was improvised.

- **Revised:** CLM-004 (per REVISION_SCOPE).
- **Added IDs:** AX-005 (amendment reference).
- **Removed IDs:** none. No ID renumbered or reused; frontmatter unchanged.

## Validation

- `validate_scope_of_work.py` on the prior contract (REVISE precondition): valid, format `SOW_V1`, issues 0.
- `validate_scope_of_work.py --json` on the revised contract: valid `True`, format `SOW_V1`, issues 0.
- `derive_review_checklist.py`: 7 `AC-*` items (7 defined in the contract, same order), bound to sha256 `f16ffa8a33cbfb2e78a8e916e90aff9fb44ad20adf94fe61a559a213f5564460`; checklist JSON sha256 `e9bb5616317515f8af8d37cc0519fb8bf569d4089f4823ae032de2bbf27c8dfd`; repeated derivation byte-identical: True.
- `check_boundary_owner_resolution.py --json`: status OK; findings 0; requirements checked 1, not checkable 0 (report sha256 `9ed911c8329d315151c3c21cf9dd681625885cd2958f424cdd575a2a02de74ae`).
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
| 22 — amendment accepted at group 3 and names DEL-04-02 `MODIFY`; state admitted and unchanged; reverse-applying every `new` → `old` on the revised file reproduces the prior bytes exactly (REVERSE_EQUALS_PRIOR 2 pairs), so nothing outside REVISION_SCOPE and the AX line changed; no ID removed, renumbered or reused; AX reference present and the snapshot path exists | PASS |
| 1 — pilot variance | Recorded: the validator resolves the contract as `SOW_V1` without any migration variance; none is needed for a `SOW_V1` REVISE |
| 2, 5–7, 10–12, 14, 17 | NOT_APPLICABLE (CONVERT only) |
| 15 | NOT_APPLICABLE (no HTML requested) |

**Write footprint:** in the deliverable folder only `ScopeOfWork.md` is modified (`git status`: ['projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-02_Visible autonomy and result standing/ScopeOfWork.md']); `_STATUS.md`, `Dependencies.csv`, `_DEPENDENCIES.md` and all other files are untouched.

## Diff, prior → revised (for the independent check)

```diff
--- prior
+++ revised
@@ -51 +51 @@
-- **CLM-004** — The Owner with App/SWB contract owners decides the unresolved reserved-act and routine-classifier choices in OI-001 and OI-002. The Shared contract owner with SWB implementation owner resolves OI-013; App/shared contract owners resolve OI-014. Their distinct points of need remain in TBD-001 through TBD-004. The person sets the applicable autonomy scope; carrying or rendering policy does not transfer these decisions to a component or record owner. [I; H V4-HI-40; S d2/d3]
+- **CLM-004** — The owner ruled OI-001 and OI-002 for the first increment's App/shared contracts (`APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2/D3; TBD-001, TBD-002); the Owner with App/SWB contract owners decides any reserved-act or routine-classifier matter those rulings do not cover, with operation-specific additions under OI-021. The Shared contract owner with SWB implementation owner resolves OI-013; App/shared contract owners resolve OI-014. Their distinct points of need remain in TBD-001 through TBD-004. The person sets the applicable autonomy scope; carrying or rendering policy does not transfer these decisions to a component or record owner. [I; H V4-HI-40; S d2/d3]
@@ -107,0 +108 @@
+- **AX-005** — Revised under scope-change amendment `SCA-V4-002` (accepted snapshot `projects/chirality-app-v4/execution/_ScopeChange/SCA-V4-002_2026-09-29_1901`), applying `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2/D3 (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-FIRST-INCREMENT-20260928/OWNER_DECISIONS.md`). Revised: CLM-004. Added: AX-005. Removed: none.
```
