# V8: independent review of the J2 compatibility candidate

2026-10-07. Chirality TASK (Type 2), independent code reviewer, dispatched by
HELP_HUMAN (Claude Opus 5.5, Claude Code) for run `APP-V4-GROUP-A-20261004`.
No delegation. I did not write the code under review. My only write is this
file. I made no commits and used no network, credentials, `~/.codex`, model
calls or UI.

## Candidate

- Branch `claude/app-v4-j2-compatibility`, commit
  `e37045c1236a56307374543d5efff3a38a5c2dc2`. It is one commit on base
  `3d0db214cb`. I treated the worktree
  `.claude/worktrees/agent-af2ce0ad2cee92fc1` as read-only and used only
  `git show`, `git diff` and `git archive` on it.
- Files changed, from `git diff --numstat`:
  - `app/CONTRACT_ISSUES.md`: +34 / -0.
  - `app/src-tauri/src/compatibility_report.rs`: +733 / -3.
  - `app/src-tauri/src/compatibility_report_tests.rs`: +752 / -0.
  - `execution_compatibility.rs` is unchanged.
- SHA-256 of the files at the candidate commit:
  - `compatibility_report.rs`: `83b7834f9c64c0fc69b55c68f323f6cee0cbe66342ec84d868c8c7277f2194f3`
  - `compatibility_report_tests.rs`: `bf9497d655a3fe9f63e1139cf079cc93531afa2d1811ea013afd12c1d9e3d934`
  - `execution_compatibility.rs`: `73fe9cce5f059661fbc59c9e879618f2f3f8fa9bc5c9b5d02b0e8ecea144cf4b`. This is the same hash V6 recorded.
  - `CONTRACT_ISSUES.md`: `4ab54ebc56d52224b2da4244b7a5b64d46e5906ba23f899b25dec4bc4761d43d`
- Write fence: `DISPATCH.md` row J2 allows `execution_compatibility.rs`,
  `compatibility_report.rs`, their tests and a CONTRACT_ISSUES append. The diff
  stays inside that fence.

## Scope

The scope is the six review questions in the brief: correctness against EXEC
§3 and `compatibility-report.schema.json`; the WD §3.4 tightening; test
strength; fabrication; the Root seam; and the CI-18 (J2) entry.

The following are out of scope:
- the J1 wiring;
- a real environment collector;
- storing the report or the RS write;
- the governance-phase hold support;
- CK-4.

## Method actually performed

1. **Instructions read:**
   - Root `AGENTS.md` (`f96feb19…6113977`);
   - `agents/AGENT_TASK.md` (`1a13a5b0…7c8fb7`);
   - `projects/chirality-app-v4/loop/LOOP_INIT.md` (`c2e88f81…985bd`).

   I did not read the alignment manuals. This bounded code review did not need them.
2. **Basis read:**
   - EXEC `EXECUTION_COMPATIBILITY.md` §3 in full, §3.1–§3.8 (`dc7ed825…e39cb`, the same bytes V6 cites);
   - `compatibility-report.schema.json` (`8e2bf4a2…afd24`);
   - WD `WORKFLOW_DECLARATION.md` §3.4, §3.8, §4.2.2–§4.2.4 and §11, together with the WD schema's `required_tool`, `checkpoint`, `held_actions`, `reached_when`, `subject` and `workflow_identity` definitions (`a7a2ce85…fd24`);
   - RS `RS_RECORD.schema.json` `compatibilityReportRef` and `evidenceRef`, and RS RECORD_SEMANTICS R14;
   - `reviews/V6-COMPATIBILITY-CORE.md` (`eeaa183d…403da`);
   - the Group A work graph row J2 and the J2 row in `DISPATCH.md`.

   The Design folder is byte-identical between the candidate and the HELP_HUMAN head `0fb6f4a8bc` (checked with `git diff --quiet`).
3. **Source read in full:** `compatibility_report.rs` (998 lines),
   `execution_compatibility.rs` and `compatibility_report_tests.rs`. I also read
   the relevant parts of `workflow_declaration.rs`, `role_lifecycle.rs`,
   `runtime_session.rs` and `schema_validation.rs` to check the seam's named APIs.
4. **Original tests preserved:** the diff of the test file against base has
   752 insertions and 0 deletions. The first 166 lines are byte-identical to
   base (checked with `cmp`), so all 7 original tests are unchanged.
5. **Full suite in my copy:** I extracted the candidate with
   `git archive e37045c123 projects/chirality-app-v4 | tar -x -C $TMPDIR/j2-review`,
   then ran `npm install --offline` and
   `cargo test --offline --locked` with the brief's environment. The run exited 0.
   - **Counts:** 44 `test result` lines, totalling 611 passed, 0 failed and 3 ignored. Four of those lines are nested `file_act_fifo_worker` subprocess runs ("1 passed; 294 filtered out"). Without them there are **607 top-level passes, 0 failures and 3 ignored**, which matches J2's report.
   - **This module:** `execution_compatibility::report::tests` ran 19 tests and all passed: the 7 original tests and 12 `j2_*` tests.
6. **Mutations:** I ran 21 mutations of my own in the scratch copy, one at a
   time. Each was an exact-string replacement that had to match exactly once. I
   ran the module tests after each and restored the file afterwards. The
   restored bytes were checked with `cmp` against `git show`.
7. **Probes:** I added temporary scratch tests, ran them and removed them. They
   printed the published bodies for these cases:
   - an undeclared workflow;
   - a newer contract version;
   - an omitted category;
   - an optional reference that is present but currently unavailable;
   - a malformed optional reference;
   - an unrecognized `governed` value;
   - an FB-13 invalid checkpoint;
   - duplicate names;
   - malformed roles;
   - stored R14 bytes that contain a duplicate key.

## Mutation results

| ID | Mutation | Result |
|---|---|---|
| M1 | Absence from a partial catalog stays *missing* | Killed (4 tests) |
| M2 | An unobserved or unreadable catalog is read as an empty catalog, so unknown becomes *missing* | Killed (`j2_unknown_inventory_is_never_missing`) |
| M3 | The R14 body says *resolved* without comparing the stored bytes | Killed (`j2_r14_…`) |
| M4 | The WD §3.4 tightening is removed | Killed (`j2_unrecognized_optional_…`) |
| M5 | Pin 0.160.0 borrows the 0.158.0 account | Killed (2 tests) |
| M6 | An unobserved channel is published as `enabled` | Killed (`j2_publication_refused_…`) |
| M7 | A caller-supplied origin is given standing `actual_host` | Killed (2 tests) |
| M8 | `declared` is published as `declared_empty` | **Survived** |
| M9 | Partial and complete catalogs are both published as unreadable | Killed (by the complete-catalog assertion only) |
| M10 | CK-3 accepts an unchanged edition | Killed |
| M11 | An unknown channel no longer demotes a *present* outcome | Killed (original test) |
| M12 | An unreadable catalog is published as `catalog_readable: true` | Killed |
| M13 | An unknown role no longer withholds a pass | Killed (2 tests) |
| M14 | A checkpoint whose declaration is not established is published as `valid` | **Survived** |
| M16 | Only a partial catalog is published as unreadable | **Survived** |
| M21 | CK-3 accepts an empty earlier-report reference | **Survived** |
| M22 | The `validate_report` call is removed from `publish` | **Survived**. The produced bodies are valid, and the independent design-schema assertions would catch an invalid body |
| M24 | `undeclared` is published as `declared_empty` | **Survived** |
| M25 | A not-established category is published as `declared` | **Survived** |
| M26 | `runtime_holds` is dropped | Killed |
| M27 | The fallback is dropped from the purpose line | **Survived** |

The mutations named in the brief are all killed:
- unknown becomes *missing* (M1, M2);
- R14 is produced without a checked resolution (M3).

A preparation cannot produce an R14 body at all. `r14_body` exists only on
`PublishedReport`, whose fields are private to the `report` module, so no code
outside that module can construct one.

## Answers to the review questions

**1. Correctness.**

Occasions:
- CK-1 and CK-2 are labelled correctly, and each call produces a new report with a new opaque ID that is distinct from the preparation ID.
- CK-3 requires a new, non-empty edition that differs from the earlier edition. The earlier body is never rewritten, and currency is a view on the `Basis` (CC-1).

Requirement outcomes:
- They follow EV-4 to EV-11 through the unchanged core.
- A *missing* outcome under a partial catalog becomes *not established*.
- An unobserved channel demotes only *present* and *present, currently unavailable*. Known negatives survive, as V6 requires.
- The 0.160.0 pin gives *not established* for harness rows, with a limitation that names the pin.

CR-3 `declared_part_status`: the probes confirm the mapping is correct.
- Undeclared, or the category omitted, gives `undeclared`.
- An empty array gives `declared_empty`.
- All elements recognized gives `declared`.
- Any element not recognized, a malformed category, or a newer or unreadable contract gives `not_established`.

CR-4 `catalog_readable`:
- It is true for a partial or complete catalog and false only for `Unreadable`.
- `Unobserved` refuses publication.
- This matches V6 item 2: a partial catalog is readable, with unreadable entries omitted.

R14:
- The R14 body is `{report: evidenceRef(kind "compatibility report", ref = report id, resolutionAtWrite), occasion, passResult}`.
- Its pass result is pass, does not pass or not established. *Unsupported* is folded into *does not pass*, which matches RS R14 and R14-3.
- It is validated against the embedded RS `compatibilityReportRef`.
- Tampered values and unreadable bytes are refused, with one gap (F-2).

The deviations I found are F-1 to F-3.

**2. Tightening.** The tightening is warranted. WD §3.4 says that an
unrecognized element in the required-tool category makes "the corresponding
result **not established**, never a pass". It then names the checkpoint case
separately: there the result is the checkpoint's own reading. That contrast
supports reading the required-tool case as the check result. EXEC §3.2
consumes WD §3.4 unchanged.

The change does not alter any earlier assertion:
- all 7 original tests are byte-identical and pass;
- the one original test that sets necessity to `optional` edits the value after reading, so the element's reading stays `Recognized` and is not affected.

See F-8 for the remaining tension with EXEC EV-2 and PS-5, and for the legacy API.

**3. Test strength.** The tests are meaningful for every property the brief
names. Each brief-named defect I introduced made at least one test fail.
However, several published-body mappings are not pinned by any assertion: the
CR-3 values other than `declared_empty`, `catalog_readable` for a partial
catalog, the checkpoint `declaration_status` values other than `valid`, the
fallback in the purpose line, and an empty CK-3 earlier reference (F-4).

**4. Fabrication.** I found no path to `actual_host`:
- `InventoryOrigin` has only `CallerSupplied`, which gives `illustrative`, and `TestDouble`, which gives `test_double`;
- the only occurrence of `actual_host` in either source file is a doc comment.

Publication with missing facts is refused, with a reason for each fact. The
facts covered are:
- host ID;
- edition;
- catalog observation;
- channel state;
- a surface outside H, E and X;
- holding library;
- observation identity;
- identity tuple;
- an unrepresentable element.

Every produced body is also validated against the schema before it is
returned. The one place where a value is stated that the declaration did not
supply is F-3, the `governed` flag.

**5. Seam.** The seam is accurate. These APIs exist and behave as the doc
says:
- `RoleBindings::selected_role`;
- `HistorySession::binding`;
- `RoleBinding::role_in_force`;
- `WorkflowRootSession`;
- `RunScope.holding_library`.

`crate::execution_compatibility::report` is `pub(crate)`, so J1 can reach it.
The seam is not yet complete for wiring (F-5).

**6. CI entry.** Gaps (a)–(c) are real against the schema and the Design. Parts
of the text are inaccurate or understated (F-6), and the number collides (F-7).

## Findings

**F-1. MINOR. CR-11 runtime holds include optional references.**
- **Where:** `compatibility_report.rs:922-926`.
- **Evidence:** `runtime_holds` filters only on `outcome == "present_currently_unavailable"`. EXEC CR-11 defines run-time holds as "Required references *present, currently unavailable*". In the probe, an optional `opt` reference whose precondition does not hold appears in `runtime_holds`.
- **Consequence:** The report and the panel show an optional reference as a run-time hold. The pass result is unaffected. Fix: also filter on `necessity == "required"` and add a test.

**F-2. MINOR. A duplicate key in the stored bytes is accepted as `resolved`.**
- **Where:** `compatibility_report.rs:418-420`.
- **Evidence:** `r14_body` parses the stored bytes with `serde_json::from_slice`, which keeps the last of any duplicate keys. In my probe, the stored bytes began `{"check_result":"does_not_pass","check_result":"passes",…}` and `r14_body` returned `resolutionAtWrite: "resolved"`. A first-wins reader would read *does not pass*. The crate already has `workflow_declaration::parse_unique`, which refuses duplicate keys.
- **Consequence:** A tampered stored copy that is ambiguous between readers can be referenced as resolved. Fix: parse with `parse_unique`, or compare exact bytes when Root stores the canonical serialization, and add a negative test.

**F-3. MINOR. An unrecognized `governed` value is published as `governed: false`.**
- **Where:** `compatibility_report.rs:700`.
- **Evidence:** `"governed": v["governed"] == "yes"`. In the probe, `governed: "maybe"` gave `governed:false` and `declaration_status:"not_established"`. WD FB-19 says to preserve and report such a value, and in the governance phase it is "never assumed either way". The schema requires a boolean. Unrecognized checkpoint fields of other kinds are refused (CI-18 (a)), but this one is defaulted.
- **Consequence:** The Phase-1 effect is small, because the status is shown as not established. Still, the body states a value that was not declared, which is inconsistent with the "nothing guessed" rule J2 applies elsewhere. Fix: refuse publication, as for the other unrepresentable checkpoint fields, and add this case to CI-18 (a).

**F-4. MINOR. Some published-body mappings are not pinned by any test.**
- **Where:**
  - `compatibility_report.rs:519-539`: CR-3;
  - `:733`: partial readability;
  - `:689-693`: checkpoint status;
  - `:594-599`: fallback;
  - `:966`: the CK-3 earlier reference.
- **Evidence:** Mutations M8, M14, M16, M21, M24, M25 and M27 all survived. The probes show that the code is currently correct for each of them.
- **Consequence:** A later regression in these CR-3, CR-4, CR-9 or PS-5 mappings, or in the CK-3 precondition, would pass CI. Fix: add assertions for the following.
  - `declared_part_status` for each of the four values.
  - `catalog_readable: true` for a partial catalog.
  - An `invalid` checkpoint, such as FB-13, and a `not_established` one.
  - The `(fallback: …)` purpose text.
  - CK-3 with an empty `earlier_report`.

**F-5. MINOR. The Root seam leaves J1 obligations unstated.**
- **Where:** `compatibility_report.rs:338-382`.
- **Evidence:** The seam does not state these points.
  - **R14 when publication is refused.** It does not say what Root writes to R14 when `published` is `Err`. This is the normal production case today, because no collector exists, so the catalog, channel and host are unobserved. RS R14 keeps "no report evaluated" explicit, and V6 item 5 forbids using a preparation ID as a report reference.
  - **CK-3 reference.** It does not say what `earlier_report` should be when the earlier evaluation was not published. The preparation ID is reachable through `view()["preparation"]["id"]`.
  - **Same conversation.** `evaluate` does not check that the `role`, `selection` and `holding_library` belong to the `basis` home and conversation. `RoleInForce` carries no home or thread. V6 item 1 makes this Root's check, but the seam only says "all from the same home".
- **Consequence:** J1 could write an R14 reference to a preparation or invent an `earlier_report`, or skip the consistency check. Fix: add these three points to the seam doc. No code change is needed.

**F-6. MINOR. CI-18 (J2) is inaccurate or understated in two places.**
- **Where:** `app/CONTRACT_ISSUES.md:289-290` and `:298-303`.
- **Evidence:**
  - **(a) Preparation claim.** Gap (a) says "the advisory preparation still reports the check as *not established*". That holds for required-tool elements only. For an unrepresentable checkpoint, the Phase-1 check is unchanged, which is correct under PH-3 and WD §3.4: `j2_publication_refused_…` asserts `Compatible` for the A3 checkpoint.
  - **(a) Omitted case.** Gap (a) also omits the `governed` case (F-3).
  - **(c) Missing facts.** Gap (c) names only `host_id` and `catalog_edition`. An App-only run with no external host also has no catalog to observe and no external channel state, so the code also refuses publication for those facts (`catalog_readable` and `channel_state` are required). Today such a run can never be published.
- **Consequence:** The Design owner gets an incomplete statement of the App-only gap. Fix: correct the text when CI-18 is renumbered.

**F-7. NOTE. CI number collision.**
- **Where:** `app/CONTRACT_ISSUES.md:278`.
- **Evidence:** J1 holds CI-18. HELP_HUMAN plans to renumber this entry CI-19, and the cross-reference in `compatibility_report.rs` must not depend on the number. I checked: no source file names CI-18.
- **Consequence:** Renumber at integration.

**F-8. NOTE. Tightening scope.**
- **Where:**
  - `compatibility_report.rs:138-146`;
  - `execution_compatibility.rs:137-154`.
- **Evidence:**
  - **What it covers.** The tightening treats every non-`Recognized` element as not established, including schema-malformed and duplicate-name elements, not only unrecognized ones. That is consistent with CR-3, WD FB-02 and VO-5, and FB-20.
  - **Tension with EXEC.** Read alone, EXEC EV-2 and PS-5 ("optional references never block") would keep a malformed *optional* reference from affecting the result. WD §3.4 governs, because EXEC consumes it unchanged.
  - **Legacy API.** The legacy `Compatibility::check` is not tightened. It is used only inside `report_check` and in `workflow_role_tests`.
- **Consequence:** There is no defect. The Design owner may confirm the reading, and a later consumer should not call the legacy `check` directly.

**F-9. NOTE. Information-only inputs are not checked.**
- **Where:** `compatibility_report.rs:904-906` and `:945`.
- **Evidence:**
  - **Destination.** A model destination that is not supplied is published as `null`, with the limitation "model destination not supplied". The schema allows `null`. CR-14 applies to App runs on X.
  - **Time.** `evaluated_at` is any non-empty caller string.
- **Consequence:** The report states that the destination is unknown rather than inventing it, which is acceptable. Root must pass the observed time.

## Verdict

**READY** for integration. I found no BLOCKING or MAJOR finding. The candidate
meets each brief requirement:
- unknown inventory is never *missing*, and known no-role is distinct from unknown;
- pin 0.160.0 does not borrow the 0.158.0 account;
- V6 known-negative precedence is kept;
- the report is advisory only: no gate, and no reading or editing of Codex configuration;
- publication and R14 come only from supplied facts and are schema-checked, with no path to `actual_host`;
- the seam is documented.

F-1 to F-6 are carried as repairs: a small code change for F-1, F-2 and F-3, added tests for F-4, seam text for F-5, and CI text for F-6. They may be made before or after integration. They do not change the result for any case the brief names.
