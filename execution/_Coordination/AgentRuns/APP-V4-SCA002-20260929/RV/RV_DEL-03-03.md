# RV return — DEL-03-03 (scope-of-work MODE=REVISE, closing MODE=VERIFY)

Run `APP-V4-SCA002-20260929`, node AK2 (propagation stage 1), Type 2 TASK (no delegation). Basis commit `851ec3d88` (working tree carries the uncommitted group-3 application).

## Result

**PASS.** Every F-block for DEL-03-03 in `AMENDMENT_PACKET/SOW_REVISIONS.md` applied exactly; the revised contract validates and the closing VERIFY passes.

## Bound inputs

- **Deliverable path:** `projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-03_Local external-agent receiving adapter/`
- **MODE:** REVISE, closing with VERIFY.
- **SOURCE_STATE:** `IN_PROGRESS` (from `_STATUS.md`, "Current State"); REVISE admits it.
- **AMENDMENT_REF:** `SCA-V4-002`; accepted snapshot `projects/chirality-app-v4/execution/_ScopeChange/SCA-V4-002_2026-09-29_1901/` (group 3 accepted, DECISION-3; groups 1–2, DECISION-2); `Amendment_Actions.csv` ActionSeq 7, `MODIFY` `DELIVERABLE` DEL-03-03 (register sha256 `158702bf610777e008e304268fcbd967756f9186ded946942430a391957c579d`; `ScopeChanging` NO).
- **REVISION_SCOPE source:** `AMENDMENT_PACKET/SOW_REVISIONS.md` sha256 `440d4d50abd4d6bd2a639cfb2bcaa8bcc83a6c94061a27f9fc91e67c6a12d00d` (bound by the group-2 and group-3 manifests).
- **REVISION_SCOPE:** CLM-002 (last clause and its Sources); REQ-005 (the policy
- **Conditional edits:** none of this deliverable's F-blocks is conditional on an owner item.
- **Tokens filled from the accepted records:** `{AMENDMENT_ID}` = `SCA-V4-002`; `{AMENDMENT_SNAPSHOT}` = `SCA-V4-002_2026-09-29_1901` (`_ScopeChange/_LATEST.md`, `Latest:` line). No other byte was supplied by this run.
- **Status policy:** `NO_STATUS_TOUCH`. `_STATUS.md` was not touched.

## Hashes

- **PRIOR_CONTRACT_SHA256:** `fdd22e25a0a43c55d31ca38f3fcb44931af8ebee6d34da62ff1f214013fb2881`. It equals the prior hash SOW_REVISIONS records for DEL-03-03 and the bytes at `HEAD` (`851ec3d88`).
- **Revised ScopeOfWork.md sha256:** `93faf918ce5d2d4eb14f0ecd1b20831a164a8c55a8b47cad26880818251b1a93`
- **`_STATUS.md` sha256 (unchanged, byte-identical to `HEAD`):** `94239785ea51127384dc7fdbdbd71d5cbc7438a786dd0c2ff6792d050ceab566`

## F-blocks applied (in listed order)

| F-block | Replacements | `old` occurrences at application |
|---|---|---|
| F-0303-01 · CLM-002 tail · item 4 | 1 | 1 |
| F-0303-02 · REQ-005, policy clause · item 4 (consequential) | 1 | 1 |
| F-0303-03 · new AX-005 (amendment reference) · acceptance-conditional | 1 | 1 |

3 blocks, 3 old → new replacements. No block failed; no wording was improvised.

- **Revised:** CLM-002, REQ-005 (per REVISION_SCOPE).
- **Added IDs:** AX-005 (amendment reference).
- **Removed IDs:** none. No ID renumbered or reused; frontmatter unchanged.

## Validation

- `validate_scope_of_work.py` on the prior contract (REVISE precondition): valid, format `SOW_V1`, issues 0.
- `validate_scope_of_work.py --json` on the revised contract: valid `True`, format `SOW_V1`, issues 0.
- `derive_review_checklist.py`: 7 `AC-*` items (7 defined in the contract, same order), bound to sha256 `93faf918ce5d2d4eb14f0ecd1b20831a164a8c55a8b47cad26880818251b1a93`; checklist JSON sha256 `7013f4956f6f383cfddd80ef0875812965aaec65eea8a5beb27f8232b47b1f5e`; repeated derivation byte-identical: True.
- `check_boundary_owner_resolution.py --json`: status OK; findings 1; requirements checked 1, not checkable 1 (report sha256 `cd28544a65e53b009aeacdbab60d9dee910aed5136d36bd0f42aadc92f2d94ec`).
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
| 22 — amendment accepted at group 3 and names DEL-03-03 `MODIFY`; state admitted and unchanged; reverse-applying every `new` → `old` on the revised file reproduces the prior bytes exactly (REVERSE_EQUALS_PRIOR 3 pairs), so nothing outside REVISION_SCOPE and the AX line changed; no ID removed, renumbered or reused; AX reference present and the snapshot path exists | PASS |
| 1 — pilot variance | Recorded: the validator resolves the contract as `SOW_V1` without any migration variance; none is needed for a `SOW_V1` REVISE |
| 2, 5–7, 10–12, 14, 17 | NOT_APPLICABLE (CONVERT only) |
| 15 | NOT_APPLICABLE (no HTML requested) |

**Write footprint:** in the deliverable folder only `ScopeOfWork.md` is modified (`git status`: ['projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-03_Local external-agent receiving adapter/ScopeOfWork.md']); `_STATUS.md`, `Dependencies.csv`, `_DEPENDENCIES.md` and all other files are untouched.

## Diff, prior → revised (for the independent check)

```diff
--- prior
+++ revised
@@ -33 +33 @@
-- **CLM-002** — App `DEL-03-01` owns the shared capability catalog/read-basis contract and its availability/read-standing fixtures; App `DEL-03-02` owns proposal, validation and outcome meanings, including original basis, stale refusal, no retargeting, duplicate one-effect and unknown outcomes. This adapter consumes these definitions with adopted PKG-04 operation-policy distinctions, App `DEL-01-01`'s supplier MCP/dynamic-tool surfaces and channel-status facts at the definition pin 0.158.0 (`APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D4), and App `DEL-02-03`'s checkpoint statement for the current phase and, for the governance phase, its hold machine, hold-support values and required-tool check; the actual Owner with App/SWB contract owners retains unresolved reserved-act and classifier decisions. Sources: Group3 Deliverables DEL-03-01/02/03, Packages PKG-04 and Open_Issues OI-001/OI-002; consolidated HOST_INTEGRATION §§2–6.
+- **CLM-002** — App `DEL-03-01` owns the shared capability catalog/read-basis contract and its availability/read-standing fixtures; App `DEL-03-02` owns proposal, validation and outcome meanings, including original basis, stale refusal, no retargeting, duplicate one-effect and unknown outcomes. This adapter consumes these definitions with adopted PKG-04 operation-policy distinctions, App `DEL-01-01`'s supplier MCP/dynamic-tool surfaces and channel-status facts at the definition pin 0.158.0 (`APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D4), and App `DEL-02-03`'s checkpoint statement for the current phase and, for the governance phase, its hold machine, hold-support values and required-tool check; the first-increment reserved acts and classifier treatment are ruled (`APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2/D3; TBD-001, TBD-002); the owner via the outside SWB session and the App/shared owner retain operation-specific reserved-act additions (OI-021, TBD-006), and the external host owner retains adoption and enforcement of its own reserved list (DEP-001). Sources: Group3 Deliverables DEL-03-01/02/03, Packages PKG-04 and Open_Issues OI-001/OI-002/OI-021; consolidated HOST_INTEGRATION §§2–6.
@@ -47 +47 @@
-- **REQ-005** — This deliverable shall perform no act owned by another deliverable or external owner: catalog/read-basis contract authorship belongs to App `DEL-03-01` and proposal/outcome contract authorship to App `DEL-03-02` (CLM-002); joined external-control and catalog-extension examination belongs to App `DEL-09-09` (CLM-003). Endpoint/server construction, catalog/domain implementation, host validation, host application, receipt issuance and host-view/human-act presentation belong to the external host owner (CLM-001, CLM-003). Actual human decisions and professional reliance belong to the person/accountable professional (CLM-003); unresolved reserved/classifier policy decisions remain with the Owner with App/SWB contract owners (CLM-002), and extension-promise decisions remain with the Owner with host contract owner (CLM-003). The App receiver may consume, link and faithfully record supplied evidence within its assigned contribution.
+- **REQ-005** — This deliverable shall perform no act owned by another deliverable or external owner: catalog/read-basis contract authorship belongs to App `DEL-03-01` and proposal/outcome contract authorship to App `DEL-03-02` (CLM-002); joined external-control and catalog-extension examination belongs to App `DEL-09-09` (CLM-003). Endpoint/server construction, catalog/domain implementation, host validation, host application, receipt issuance and host-view/human-act presentation belong to the external host owner (CLM-001, CLM-003). Actual human decisions and professional reliance belong to the person/accountable professional (CLM-003); operation-specific reserved-act additions remain with the owner via the outside SWB session and the App/shared owner, and host adoption and enforcement of its reserved list with the external host owner (CLM-002), and extension-promise decisions remain with the Owner with host contract owner (CLM-003). The App receiver may consume, link and faithfully record supplied evidence within its assigned contribution.
@@ -75,0 +76 @@
+- **AX-005** — Revised under scope-change amendment `SCA-V4-002` (accepted snapshot `projects/chirality-app-v4/execution/_ScopeChange/SCA-V4-002_2026-09-29_1901`), applying `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2/D3 (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-FIRST-INCREMENT-20260928/OWNER_DECISIONS.md`). Revised: CLM-002 and REQ-005. Added: AX-005. Removed: none.
```
