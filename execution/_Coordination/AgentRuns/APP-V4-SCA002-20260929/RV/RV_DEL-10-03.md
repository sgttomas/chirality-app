# RV return — DEL-10-03 (scope-of-work MODE=REVISE, closing MODE=VERIFY)

Run `APP-V4-SCA002-20260929`, node AK2 (propagation stage 1), Type 2 TASK (no delegation). Basis commit `851ec3d88` (working tree carries the uncommitted group-3 application).

## Result

**PASS.** Every F-block for DEL-10-03 in `AMENDMENT_PACKET/SOW_REVISIONS.md` applied exactly; the revised contract validates and the closing VERIFY passes.

## Bound inputs

- **Deliverable path:** `projects/chirality-app-v4/execution/PKG-10_Project definition and manual-led practice/1_Working/DEL-10-03_Shared commitments and consumer responsibility account/`
- **MODE:** REVISE, closing with VERIFY.
- **SOURCE_STATE:** `INITIALIZED` (from `_STATUS.md`, "Current State"); REVISE admits it.
- **AMENDMENT_REF:** `SCA-V4-002`; accepted snapshot `projects/chirality-app-v4/execution/_ScopeChange/SCA-V4-002_2026-09-29_1901/` (group 3 accepted, DECISION-3; groups 1–2, DECISION-2); `Amendment_Actions.csv` ActionSeq 1, `MODIFY` `DELIVERABLE` DEL-10-03 (register sha256 `158702bf610777e008e304268fcbd967756f9186ded946942430a391957c579d`; `ScopeChanging` YES).
- **REVISION_SCOPE source:** `AMENDMENT_PACKET/SOW_REVISIONS.md` sha256 `440d4d50abd4d6bd2a639cfb2bcaa8bcc83a6c94061a27f9fc91e67c6a12d00d` (bound by the group-2 and group-3 manifests).
- **REVISION_SCOPE:** REQ-005; new AX-005.
- **Conditional edits:** none of this deliverable's F-blocks is conditional on an owner item.
- **Tokens filled from the accepted records:** `{AMENDMENT_ID}` = `SCA-V4-002`; `{AMENDMENT_SNAPSHOT}` = `SCA-V4-002_2026-09-29_1901` (`_ScopeChange/_LATEST.md`, `Latest:` line). No other byte was supplied by this run.
- **Status policy:** `NO_STATUS_TOUCH`. `_STATUS.md` was not touched.

## Hashes

- **PRIOR_CONTRACT_SHA256:** `4e16817e71f1df39afd3e3dd8175a04e9d4cc2384bf42065e91e16a5452b5f92`. It equals the prior hash SOW_REVISIONS records for DEL-10-03 and the bytes at `HEAD` (`851ec3d88`).
- **Revised ScopeOfWork.md sha256:** `31bc607defa42914520959234f2400858d4c1d5272ac5fa523fcea39d1b94166`
- **`_STATUS.md` sha256 (unchanged, byte-identical to `HEAD`):** `d7e7b4408d8c3a0056615453132356a6ddf5ebdd232d60e5eb6cd3b17fb91a83`

## F-blocks applied (in listed order)

| F-block | Replacements | `old` occurrences at application |
|---|---|---|
| F-1003-01 · REQ-005 · item 1 ("local-first") | 1 | 1 |
| F-1003-02 · new AX-005 (amendment reference) · acceptance-conditional | 1 | 1 |

2 blocks, 2 old → new replacements. No block failed; no wording was improvised.

- **Revised:** REQ-005 (per REVISION_SCOPE).
- **Added IDs:** AX-005 (amendment reference).
- **Removed IDs:** none. No ID renumbered or reused; frontmatter unchanged.

## Validation

- `validate_scope_of_work.py` on the prior contract (REVISE precondition): valid, format `SOW_V1`, issues 0.
- `validate_scope_of_work.py --json` on the revised contract: valid `True`, format `SOW_V1`, issues 0.
- `derive_review_checklist.py`: 6 `AC-*` items (6 defined in the contract, same order), bound to sha256 `31bc607defa42914520959234f2400858d4c1d5272ac5fa523fcea39d1b94166`; checklist JSON sha256 `b0bee29477010b308731683bb80f264a0d1cfe96bae38a791ded4167e8d578ef`; repeated derivation byte-identical: True.
- `check_boundary_owner_resolution.py --json`: status OK; findings 0; requirements checked 1, not checkable 0 (report sha256 `877d43b063a4ea04becf18feb85a0ec75b7540fe4273772940af37ee665b8ac2`).
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
| 22 — amendment accepted at group 3 and names DEL-10-03 `MODIFY`; state admitted and unchanged; reverse-applying every `new` → `old` on the revised file reproduces the prior bytes exactly (REVERSE_EQUALS_PRIOR 2 pairs), so nothing outside REVISION_SCOPE and the AX line changed; no ID removed, renumbered or reused; AX reference present and the snapshot path exists | PASS |
| 1 — pilot variance | Recorded: the validator resolves the contract as `SOW_V1` without any migration variance; none is needed for a `SOW_V1` REVISE |
| 2, 5–7, 10–12, 14, 17 | NOT_APPLICABLE (CONVERT only) |
| 15 | NOT_APPLICABLE (no HTML requested) |

**Write footprint:** in the deliverable folder only `ScopeOfWork.md` is modified (`git status`: ['projects/chirality-app-v4/execution/PKG-10_Project definition and manual-led practice/1_Working/DEL-10-03_Shared commitments and consumer responsibility account/ScopeOfWork.md']); `_STATUS.md`, `Dependencies.csv`, `_DEPENDENCIES.md` and all other files are untouched.

## Diff, prior → revised (for the independent check)

```diff
--- prior
+++ revised
@@ -56 +56 @@
-- **REQ-005** — The shared account shall start from compatible workflow/checkpoint, identity, human-act, catalog and evidence contracts across the owners in CLM-002 through CLM-004, retaining stock Codex/App-owned hosting, Tauri and the minimal local-first host loop. Each proposed shared implementation shall identify the repeated responsibility and consuming owners that justify it; placement remains open under TBD-001. Compatibility of meanings or matching formats alone shall not establish shared execution or qualified interoperability. Sources: SOW-234, HTML d2, ARCH V4-ARC-01–05/10–14/20.
+- **REQ-005** — The shared account shall start from compatible workflow/checkpoint, identity, human-act, catalog and evidence contracts across the owners in CLM-002 through CLM-004, retaining stock Codex/App-owned hosting, Tauri and the minimal host loop, which runs on a local or cloud model the person chooses, with no default; a cloud model is reached by OAuth sign-in or an API key (PRD V4-HOST-01 and ARCH V4-ARC-11 as amended by `SCA-V4-001`; `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4` D4-3). Each proposed shared implementation shall identify the repeated responsibility and consuming owners that justify it; placement remains open under TBD-001. Compatibility of meanings or matching formats alone shall not establish shared execution or qualified interoperability. Sources: SOW-234, HTML d2, ARCH V4-ARC-01–05/10–14/20.
@@ -89,0 +90 @@
+- **AX-005** — Revised under scope-change amendment `SCA-V4-002` (accepted snapshot `projects/chirality-app-v4/execution/_ScopeChange/SCA-V4-002_2026-09-29_1901`), applying `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4` D4-3 (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-SWBPIPE-INTAKE-20260928/OWNER_DECISIONS.md`) as routed by `APP-V4-BASIS-ALIGN-20260928-DECISION-8` (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-BASIS-ALIGN-20260928/OWNER_DECISIONS.md`). Revised: REQ-005. Added: AX-005. Removed: none.
```
