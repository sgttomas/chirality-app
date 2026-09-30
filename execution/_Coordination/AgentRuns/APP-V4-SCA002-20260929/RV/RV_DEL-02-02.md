# RV return — DEL-02-02 (scope-of-work MODE=REVISE, closing MODE=VERIFY)

Run `APP-V4-SCA002-20260929`, node AK2 (propagation stage 1), Type 2 TASK (no delegation). Basis commit `851ec3d88` (working tree carries the uncommitted group-3 application).

## Result

**PASS.** Every F-block for DEL-02-02 in `AMENDMENT_PACKET/SOW_REVISIONS.md` applied exactly; the revised contract validates and the closing VERIFY passes.

## Bound inputs

- **Deliverable path:** `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-02_Workflow-making workspace and registration/`
- **MODE:** REVISE, closing with VERIFY.
- **SOURCE_STATE:** `INITIALIZED` (from `_STATUS.md`, "Current State"); REVISE admits it.
- **AMENDMENT_REF:** `SCA-V4-002`; accepted snapshot `projects/chirality-app-v4/execution/_ScopeChange/SCA-V4-002_2026-09-29_1901/` (group 3 accepted, DECISION-3; groups 1–2, DECISION-2); `Amendment_Actions.csv` ActionSeq 6, `MODIFY` `DELIVERABLE` DEL-02-02 (register sha256 `158702bf610777e008e304268fcbd967756f9186ded946942430a391957c579d`; `ScopeChanging` NO).
- **REVISION_SCOPE source:** `AMENDMENT_PACKET/SOW_REVISIONS.md` sha256 `440d4d50abd4d6bd2a639cfb2bcaa8bcc83a6c94061a27f9fc91e67c6a12d00d` (bound by the group-2 and group-3 manifests).
- **REVISION_SCOPE:** TBD-001; TBD-002 (OI-012 clause); new AX-004. AX-003
- **Conditional edits:** none of this deliverable's F-blocks is conditional on an owner item.
- **Tokens filled from the accepted records:** `{AMENDMENT_ID}` = `SCA-V4-002`; `{AMENDMENT_SNAPSHOT}` = `SCA-V4-002_2026-09-29_1901` (`_ScopeChange/_LATEST.md`, `Latest:` line). No other byte was supplied by this run.
- **Status policy:** `NO_STATUS_TOUCH`. `_STATUS.md` was not touched.

## Hashes

- **PRIOR_CONTRACT_SHA256:** `b0a1a8a4aa6f53057c8db4bb33c65c5e697f45ae509088a570a70ff8cee295ec`. It equals the prior hash SOW_REVISIONS records for DEL-02-02 and the bytes at `HEAD` (`851ec3d88`).
- **Revised ScopeOfWork.md sha256:** `5814116909db8120c1fe888ba021ca60ad139ea0b36cc89fe7e93ed00235924a`
- **`_STATUS.md` sha256 (unchanged, byte-identical to `HEAD`):** `a4efafd9d06802f6b1d9ac62401c7592443af35580c9795f42f6cd9f7f34ccd1`

## F-blocks applied (in listed order)

| F-block | Replacements | `old` occurrences at application |
|---|---|---|
| F-0202-01 · TBD-001 · item 3 | 1 | 1 |
| F-0202-02 · TBD-002, OI-012 clause · item 3 | 1 | 1 |
| F-0202-03 · new AX-004 (amendment reference) · acceptance-conditional | 1 | 1 |

3 blocks, 3 old → new replacements. No block failed; no wording was improvised.

- **Revised:** TBD-001, TBD-002 (per REVISION_SCOPE).
- **Added IDs:** AX-004 (amendment reference).
- **Removed IDs:** none. No ID renumbered or reused; frontmatter unchanged.

## Validation

- `validate_scope_of_work.py` on the prior contract (REVISE precondition): valid, format `SOW_V1`, issues 0.
- `validate_scope_of_work.py --json` on the revised contract: valid `True`, format `SOW_V1`, issues 0.
- `derive_review_checklist.py`: 8 `AC-*` items (8 defined in the contract, same order), bound to sha256 `5814116909db8120c1fe888ba021ca60ad139ea0b36cc89fe7e93ed00235924a`; checklist JSON sha256 `84722c83935d33c283a63f9b43c2a45c7928bd668093f251853a6b758ee899bd`; repeated derivation byte-identical: True.
- `check_boundary_owner_resolution.py --json`: status OK; findings 0; requirements checked 1, not checkable 0 (report sha256 `8d17c809690bdaa4bc687f7caaefcfc71bfc3e08504e42c0db596e1a10f84ea1`).
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
| 22 — amendment accepted at group 3 and names DEL-02-02 `MODIFY`; state admitted and unchanged; reverse-applying every `new` → `old` on the revised file reproduces the prior bytes exactly (REVERSE_EQUALS_PRIOR 3 pairs), so nothing outside REVISION_SCOPE and the AX line changed; no ID removed, renumbered or reused; AX reference present and the snapshot path exists | PASS |
| 1 — pilot variance | Recorded: the validator resolves the contract as `SOW_V1` without any migration variance; none is needed for a `SOW_V1` REVISE |
| 2, 5–7, 10–12, 14, 17 | NOT_APPLICABLE (CONVERT only) |
| 15 | NOT_APPLICABLE (no HTML requested) |

**Write footprint:** in the deliverable folder only `ScopeOfWork.md` is modified (`git status`: ['projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-02_Workflow-making workspace and registration/ScopeOfWork.md']); `_STATUS.md`, `Dependencies.csv`, `_DEPENDENCIES.md` and all other files are untouched.

## Diff, prior → revised (for the independent check)

```diff
--- prior
+++ revised
@@ -83,2 +83,3 @@
-- **TBD-001** — OI-001 retains broader operation-level reserved-act decisions with the owner and affected App/SWB contract owners, with PointOfNeed "Before operation-policy production contracts". OI-002 retains classifier-permission decisions with those owners, with PointOfNeed "Before permission-policy implementation". DEL-04-01 defines/carries adopted policy; this workspace consumes that result. The settled review/registration rule and false-attribution prohibition remain usable now. [I1; CLM-004]
-- **TBD-002** — OI-008 leaves detailed Rust/TypeScript process allocation with the App implementation owner before architecture production contracts; OI-012 leaves the supplier version pin with that owner before generation/qualification. Receive the identified native interfaces and candidate when needed; this contract supplies no version or wire-field guess. [I1; A1 §3; X1 DEP-005]
+- **AX-004** — Revised under scope-change amendment `SCA-V4-002` (accepted snapshot `projects/chirality-app-v4/execution/_ScopeChange/SCA-V4-002_2026-09-29_1901`), applying `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2, D3 and D4 (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-FIRST-INCREMENT-20260928/OWNER_DECISIONS.md`). Revised: TBD-001 and TBD-002. Added: AX-004. Removed: none.
+- **TBD-001** — OI-001 and OI-002 were ruled for the first increment's App/shared contracts by `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2 (five reserved acts) and D3 (in the App, routine tool-permission and sandbox modes, including classifier-based modes, remain the user's own Codex setting and never stand in for a reserved or professional act); record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-FIRST-INCREMENT-20260928/OWNER_DECISIONS.md`. Broader operation-level reserved-act decisions that D2 does not cover remain with the owner and affected App/SWB contract owners, with PointOfNeed "Before operation-policy production contracts"; operation-specific additions are made under OI-021. DEL-04-01 defines/carries adopted policy; this workspace consumes that result. The settled review/registration rule and false-attribution prohibition remain usable now. [I1; CLM-004]
+- **TBD-002** — OI-008 leaves detailed Rust/TypeScript process allocation with the App implementation owner before architecture production contracts; For OI-012, `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D4 selected Codex 0.158.0 as the definition and generation pin; re-examination before implementation and the pin used for qualification remain with that owner before generation/qualification. Receive the identified native interfaces and candidate when needed; this contract supplies no version or wire-field guess. [I1; A1 §3; X1 DEP-005]
```
