# RV return — DEL-01-04 (scope-of-work MODE=REVISE, closing MODE=VERIFY)

Run `APP-V4-SCA002-20260929`, node AK2 (propagation stage 1), Type 2 TASK (no delegation). Basis commit `851ec3d88` (working tree carries the uncommitted group-3 application).

## Result

**PASS.** Every F-block for DEL-01-04 in `AMENDMENT_PACKET/SOW_REVISIONS.md` applied exactly; the revised contract validates and the closing VERIFY passes.

## Bound inputs

- **Deliverable path:** `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/`
- **MODE:** REVISE, closing with VERIFY.
- **SOURCE_STATE:** `INITIALIZED` (from `_STATUS.md`, "Current State"); REVISE admits it.
- **AMENDMENT_REF:** `SCA-V4-002`; accepted snapshot `projects/chirality-app-v4/execution/_ScopeChange/SCA-V4-002_2026-09-29_1901/` (group 3 accepted, DECISION-3; groups 1–2, DECISION-2); `Amendment_Actions.csv` ActionSeq 5, `MODIFY` `DELIVERABLE` DEL-01-04 (register sha256 `158702bf610777e008e304268fcbd967756f9186ded946942430a391957c579d`; `ScopeChanging` NO).
- **REVISION_SCOPE source:** `AMENDMENT_PACKET/SOW_REVISIONS.md` sha256 `440d4d50abd4d6bd2a639cfb2bcaa8bcc83a6c94061a27f9fc91e67c6a12d00d` (bound by the group-2 and group-3 manifests).
- **REVISION_SCOPE:** CLM-005 (policy clause); VER-005 (last sentence but one);
- **Conditional edits:** none of this deliverable's F-blocks is conditional on an owner item.
- **Tokens filled from the accepted records:** `{AMENDMENT_ID}` = `SCA-V4-002`; `{AMENDMENT_SNAPSHOT}` = `SCA-V4-002_2026-09-29_1901` (`_ScopeChange/_LATEST.md`, `Latest:` line). No other byte was supplied by this run.
- **Status policy:** `NO_STATUS_TOUCH`. `_STATUS.md` was not touched.

## Hashes

- **PRIOR_CONTRACT_SHA256:** `7261a58f93d4531ca080c16d7fe088818871c3444085bade2eb2350ace94e60a`. It equals the prior hash SOW_REVISIONS records for DEL-01-04 and the bytes at `HEAD` (`851ec3d88`).
- **Revised ScopeOfWork.md sha256:** `0cdb44e297010b70deb479ab647a165023846aa0943c3f9fc200407c708469cd`
- **`_STATUS.md` sha256 (unchanged, byte-identical to `HEAD`):** `12de2a18b401688c4309e1dde485f6deea721696f0098d232535100c09f06c60`

## F-blocks applied (in listed order)

| F-block | Replacements | `old` occurrences at application |
|---|---|---|
| F-0104-01 · CLM-005, policy clause · item 3 | 1 | 1 |
| F-0104-02 · VER-005 · item 3 | 1 | 1 |
| F-0104-03 · TBD-001 · item 3 | 1 | 1 |
| F-0104-04 · TBD-002 · item 3 | 1 | 1 |
| F-0104-05 · TBD-004 · item 3 (OI-012) | 1 | 1 |
| F-0104-06 · new AX-004 (amendment reference) · acceptance-conditional | 1 | 1 |

6 blocks, 6 old → new replacements. No block failed; no wording was improvised.

- **Revised:** CLM-005, VER-005 (per REVISION_SCOPE).
- **Added IDs:** AX-004 (amendment reference).
- **Removed IDs:** none. No ID renumbered or reused; frontmatter unchanged.

## Validation

- `validate_scope_of_work.py` on the prior contract (REVISE precondition): valid, format `SOW_V1`, issues 0.
- `validate_scope_of_work.py --json` on the revised contract: valid `True`, format `SOW_V1`, issues 0.
- `derive_review_checklist.py`: 7 `AC-*` items (7 defined in the contract, same order), bound to sha256 `0cdb44e297010b70deb479ab647a165023846aa0943c3f9fc200407c708469cd`; checklist JSON sha256 `6d7c6ae9565906f5e4a329dbe6e3ec538c9a651ca66551651f3bee75660688c5`; repeated derivation byte-identical: True.
- `check_boundary_owner_resolution.py --json`: status OK; findings 0; requirements checked 1, not checkable 0 (report sha256 `5245901fdfec8bc8f3b2e8ca800b7fb2ec490043d2217be5cd51c595e8040a42`).
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
| 22 — amendment accepted at group 3 and names DEL-01-04 `MODIFY`; state admitted and unchanged; reverse-applying every `new` → `old` on the revised file reproduces the prior bytes exactly (REVERSE_EQUALS_PRIOR 6 pairs), so nothing outside REVISION_SCOPE and the AX line changed; no ID removed, renumbered or reused; AX reference present and the snapshot path exists | PASS |
| 1 — pilot variance | Recorded: the validator resolves the contract as `SOW_V1` without any migration variance; none is needed for a `SOW_V1` REVISE |
| 2, 5–7, 10–12, 14, 17 | NOT_APPLICABLE (CONVERT only) |
| 15 | NOT_APPLICABLE (no HTML requested) |

**Write footprint:** in the deliverable folder only `ScopeOfWork.md` is modified (`git status`: ['projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/ScopeOfWork.md']); `_STATUS.md`, `Dependencies.csv`, `_DEPENDENCIES.md` and all other files are untouched.

## Diff, prior → revised (for the independent check)

```diff
--- prior
+++ revised
@@ -45 +45 @@
-- **CLM-005** — App `DEL-04-01`, the App/shared human-act contract owner, defines and carries adopted operation policy and act distinctions; the **Owner with App/SWB contract owners** decides unresolved OI-001 and OI-002, rather than this UI slice or the policy deliverable deciding them. App `DEL-04-03`, the App/shared evidence-record owner, owns the content-bound decision and compact run-record format and App reader/writer. The host implementation owner owns offering, presenting and recording host acts and supplies host receipts; the actual person performs the human act, and the accountable professional makes professional reliance or certification judgments. A recorder may faithfully record an evidenced human act without becoming its decision actor. Sources: D rows DEL-04-01/03; H; O.
+- **CLM-005** — App `DEL-04-01`, the App/shared human-act contract owner, defines and carries adopted operation policy and act distinctions; the owner ruled OI-001 and OI-002 for the first increment's App/shared contracts (`APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2/D3), and the **Owner with App/SWB contract owners** decides any matter those rulings do not cover, with operation-specific additions under OI-021, rather than this UI slice or the policy deliverable deciding them. App `DEL-04-03`, the App/shared evidence-record owner, owns the content-bound decision and compact run-record format and App reader/writer. The host implementation owner owns offering, presenting and recording host acts and supplies host receipts; the actual person performs the human act, and the accountable professional makes professional reliance or certification judgments. A recorder may faithfully record an evidenced human act without becoming its decision actor. Sources: D rows DEL-04-01/03; H; O.
@@ -79 +79 @@
-- **VER-005** — Compare UI labels and attribution against the adopted PKG-04 interface. Use separately evidenced execution, proposal acceptance, checking, approval and reliance cases, including an independently evidenced act without a preceding acceptance record. Include a positive faithful-recording case: the person actually performs the act on identified content and a separate recorder preserves it; then a content-change/lapse case. Negative cases include success alone, missing human-act evidence and agent text claiming professional approval. Confirm none is promoted into another act or stronger standing. A concrete unresolved policy-dependent operation remains subject to its own OI-001/OI-002 ruling; test construction does not decide it. Checks AC-005 only.
+- **VER-005** — Compare UI labels and attribution against the adopted PKG-04 interface. Use separately evidenced execution, proposal acceptance, checking, approval and reliance cases, including an independently evidenced act without a preceding acceptance record. Include a positive faithful-recording case: the person actually performs the act on identified content and a separate recorder preserves it; then a content-change/lapse case. Negative cases include success alone, missing human-act evidence and agent text claiming professional approval. Confirm none is promoted into another act or stronger standing. Adopted reserved acts and classifier treatment are those of `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2/D3 as carried through the PKG-04 interface; a concrete policy-dependent operation those rulings do not cover remains subject to its own ruling (OI-021 or a successor); test construction does not decide it. Checks AC-005 only.
@@ -89,0 +90 @@
+- **AX-004** — Revised under scope-change amendment `SCA-V4-002` (accepted snapshot `projects/chirality-app-v4/execution/_ScopeChange/SCA-V4-002_2026-09-29_1901`), applying `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2, D3 and D4 (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-FIRST-INCREMENT-20260928/OWNER_DECISIONS.md`). Revised: CLM-005, VER-005, TBD-001, TBD-002 and TBD-004. Added: AX-004. Removed: none.
@@ -91,2 +92,2 @@
-- **TBD-001** — OI-001, Reserved human acts: **Owner with App/SWB contract owners**; point of need **Before operation-policy production contracts**. Choose always-reserved acts by concrete operation and consequence. This contract carries current non-fabrication and act distinctions and consumes adopted policy; it does not decide a global reserved list. Source: O; H.
-- **TBD-002** — OI-002, Classifier routine permissions: **Owner with App/SWB contract owners**; point of need **Before permission-policy implementation**. Distinguish routine tool permissions from professional acts and settle App/host treatment. No classifier behavior is selected here. Source: O; H.
+- **TBD-001** — OI-001, Reserved human acts — ruled for the first increment's App/shared contracts by `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2 (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-FIRST-INCREMENT-20260928/OWNER_DECISIONS.md`): marking checked; accepting a proposal where the autonomy requires one; engineering approval; professional reliance; changing the grant or enabling external access. Operation-specific additions remain OPEN under OI-021. Any matter the ruling does not cover stays with the **Owner with App/SWB contract owners**, point of need **Before operation-policy production contracts**. This contract carries current non-fabrication and act distinctions and consumes adopted policy through CLM-005; it does not decide a reserved list. Source: O; H.
+- **TBD-002** — OI-002, Classifier routine permissions — ruled by `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D3: in the App, routine tool-permission and sandbox modes (including classifier-based modes) remain the user's own Codex setting and never stand in for a reserved or professional act; hosts have no classifier permission mode in the first increment. Native tool permission keeps its native semantics in this slice (REQ-005). No classifier behavior is selected here. Source: O; H.
@@ -94 +95 @@
-- **TBD-004** — OI-012, Codex version pin: **App implementation owner**; point of need **Before protocol generation and qualification**. Select an identified supported supplier pin. DEP-005 identifies the pinned Codex/Tauri/local-server suppliers' published interfaces and configured endpoints as inputs before their respective implementation/qualification witnesses; no historical pin is adopted here. Source: O; CLM-002.
+- **TBD-004** — OI-012, Codex version pin: `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D4 selected Codex 0.158.0 as the definition and generation pin; it is re-examined before implementation, and upgrades are deliberate. Remaining under OI-012, with the **App implementation owner**: the pin used for implementation and for qualification on an identified App candidate, point of need **Before protocol generation and qualification** for that candidate. DEP-005 identifies the pinned Codex/Tauri/local-server suppliers' published interfaces and configured endpoints as inputs before their respective implementation/qualification witnesses; no historical pin is adopted here. Source: O; CLM-002.
```
