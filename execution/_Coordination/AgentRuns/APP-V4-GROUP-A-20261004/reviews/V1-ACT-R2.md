# V1-ACT-R2 — final same-reviewer connected-order backcheck

2026-10-04. **READY for repaired P0-ACT scope fan-in at the frozen R2/R1 hashes below.** ACT-6-R1's independently reproduced ordering defect is repaired and backchecked. Earlier ACT-1/2/3/4/5/7/8 warrants remain valid. No unresolved blocking finding in this bounded repaired scope. This is not whole-Group-A completion, trustworthy persistent replay, a stage gate, supplier/native authenticity qualification or release.

Independent TASK `/root/group_a_execution/contract_reviewer`, native descendant of WORKING_ITEMS `/root/group_a_execution`; supplied Codex gpt-6.1-sol/medium, no substitution/diversity claim or descendants. Applied already-loaded software-code-review skill and kept prior source/authority context in V1-ACT/R1 and V0-CUST. Read exact R2 return, changed queue/confirm/recovery and IPC integration, and targeted regression tests. Three successor hashes matched before/after; the other seven R1 files remained unchanged. No product/Design/Git edits, network, auth, credential or live supplier/model execution. Only this durable review written; reviewer-owned temporary harness/workspace removed after execution.

## Repair assessment

Fresh native confirmation first publishes its actual captured facts and obtains writer-owned submission metadata, then drains earlier admitted native work before its own append. Blocked older work retains the fresh event and its reserved identity as pending rather than losing or overtaking it. Queue order uses Rust admission ordinal, not timestamps/UUID encoding. Existing pending batch semantics preserve acts before delay limits; fresh continuation follows both the earlier acts and required delay account. Retained writer `written` status prevents re-appending a formerly recorded but now unresolvable submission. Backlink-only failure remains recorded and does not create a new act.

`refresh_recording` reconciles under the same ActControl path before ordinary identify_packages writes; lib.rs decision_view invokes that boundary under its Rust mutex. Genuinely unwritten hot submissions gate new recorder requests/limits. Malformed/unverified cold files receive visible origin-held diagnostics but never enter hot native custody or authorize a human-act append; their errors no longer unnecessarily stop unrelated valid recorder work.

This preserves W-1, atomic durable capture publication, writer-owned post-capture ID minting, exact original snapshot/facts/time, sequence completeness, identity/refusal safeguards, legacy no-duplication and recursive no-write coverage from the preceding backcheck. No new schema/Cargo asset changes or frontend JSON shape changes require repeating the original validation suite. Physical process-kill, OS fsync failures, native person interaction and nonlocal filesystem qualification remain outside these synthetic witnesses.

Trustworthy persistent replay of legitimate captured-but-unwritten native events is still **required unfinished work**, pending the concrete custody/seal choice and its actual witness under CC-CUST. Cold containment is not fulfillment, narrowing or transfer of that obligation. SEAL-2 remains unselected and unsigned recorded claims keep their provenance limits.

## Independent focused checks

Parent granted exclusive build-resource use and reviewer released it after these checks. All run from repository root, offline, without CHIRALITY_CODEX_BIN.

1. Recompiled and reran the **exact unchanged** failing reviewer harness preserved in V1-ACT-R1.md (SHA-256 `a3ec482c37c4e500036035b8abf154dbebf74c0cbc4d7cfe010929f8d089155e`) with that record's rustc/dependency command and canonical temporary workspace. Compile exit 0, test exit 0, **1/1 passed**. Observed A,B now equals expected A,B:

```text
actual act order: ["rec:app:560420a1-3a61-453e-8dcf-037a4a745ce7","rec:app:fb48367b-63e2-4c67-8e0e-c6fd37c3f090"]
expected original native-event order: ["rec:app:560420a1-3a61-453e-8dcf-037a4a745ce7","rec:app:fb48367b-63e2-4c67-8e0e-c6fd37c3f090"]
```

Linked current App rlib SHA-256 `1a914dadab783f51f473aefb1a150a7cfc94c92662be51bb67e260948330ddaf`. No hosting function was called by the harness; no hosting verdict inferred.

2. Independently ran each focused Cargo case using:

```sh
CARGO_HOME=/tmp/chirality-app-v4-group-a-cargo-home \
  cargo test --offline --locked \
  --manifest-path projects/chirality-app-v4/app/src-tauri/Cargo.toml \
  --test act_storage <filter>
```

| Filter | Observed result |
|---|---|
| older_pending_act_precedes | exit 0; 1/1 passed; fresh B follows older A and delay account; latest decision stays latest |
| fresh_confirmed_facts_remain | exit 0; 1/1 passed; blocked fresh B retains original facts/ID for ordered retry |
| refresh_flushes_pending | exit 0; 1/1 passed; older native act/delay account precede new recorder request/limit |
| unverified_cold_files_neither | exit 0; 1/1 passed; cold errors remain visible with no act grant and unrelated recorder continuation |

3. Same offline/locked manifest command with `--lib equal_observed_times_keep`: exit 0; **1/1 passed**, exercising both fresh confirmation and recorder continuation with equal original timestamps. Production clock behavior is unchanged. Shared test-helper dead-code warning is informational.

No blanket W-1/original suite repetition performed. Author's reported 13 library/21 act_storage/4 decide/6 schema checks remain their broader observation; this review independently establishes only the focused results listed above plus source backcheck.

## Exact successor and retained repair identities

| File | SHA-256 |
|---|---|
| `projects/chirality-app-v4/app/src-tauri/src/act_control.rs` | `1d55ff94ad08cf17673dfdae9a16e5ca7d9a98f52a1fe99a9f6101ea30a8876e` |
| `projects/chirality-app-v4/app/src-tauri/src/lib.rs` | `90b96bacfdbfa42d1337084ba50aadd82bcbb464193b5872c3efd468bb83bf15` |
| `projects/chirality-app-v4/app/src-tauri/tests/act_storage.rs` | `f66187eea1c9e7a60c9224a332a3ab7caffa6933d42e741ff227eb76002260bc` |
| `projects/chirality-app-v4/app/src-tauri/src/recorder.rs` | `96e6c17a34aae58928d7f9339b5e5af7205265c856fc8dd077253ae8f9604ad4` |
| `projects/chirality-app-v4/app/src-tauri/src/records.rs` | `cc61f735ab8dfa987081b5f50d37bd0a8b93c340c80cc5bd72266a307c588fea` |
| `projects/chirality-app-v4/app/src-tauri/src/decision_view.rs` | `051dab738e09895d9b81b3e65891aab843681b585922b0572ac959a309f7762c` |
| `projects/chirality-app-v4/app/src-tauri/src/storage.rs` | `ae8439c47b86a3225bf46e893bfa1159a2189d0cc8579692d468a78ea9267d77` |
| `projects/chirality-app-v4/app/src-tauri/src/util.rs` | `3033b37e0f360ccc2f43e4cd1d55d0d7d8305b19479e741693fd5d772f9f6d5c` |
| `projects/chirality-app-v4/app/src-tauri/tests/decide_flow.rs` | `7b0297fc11fdaf008f84264053a3939db95da947b1486039e42ae48087b57cd7` |
| `projects/chirality-app-v4/app/src/App.tsx` | `9c80295a3eab50970bc9ba5e668cdc36ca0acf347cc6c4c356b964477e8f415a` |

Successor P0-ACT-R2.md `3d46e1ff086f5f7ce8d202f9bbd395e177694aad8edd5fa7ecc4476c227ccfcd`; original P0-ACT/R1 and V1-ACT/R1 remain historical evidence. Manager must preserve the explicit cold-custody unfinished obligation and complete its planned connected Node/hosting/integration checks on the final combined candidate.
