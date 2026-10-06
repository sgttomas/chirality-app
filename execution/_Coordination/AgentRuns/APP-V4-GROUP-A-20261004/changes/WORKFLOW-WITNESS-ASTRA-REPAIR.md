# Private workflow witness preparation repair

2026-10-05. TASK `/root/group_a_execution_astra/workflow_witness_repair`, delegated-harness-native child of `/root/group_a_execution_astra`, gpt-6-astra/low, no descendants. Parent retains supplier/native execution and Cargo release. This report plus private scratch are the only authored targets.

**Standing: LT-24 correction independently cleared for preparation and freshly no-run compiled; exact successor artifact awaits original independent backcheck. First actual run remains FAIL; no native retry performed.** The original a515 Host archive failure is not repaired by this work. The manager separately owns its source disposition and corrected candidate; this helper must later bind that exact corrected committed candidate.

## Preserved inputs and private outputs

Original `/private/tmp/chirality-parent-workflow-witness-lncXTF` remains unchanged. Its input file hashes are retained in `original-manifest.json` and were rechecked after this work. New private directory: `/private/tmp/chirality-wf-astra-repair-tvtlaytf`. Existing HANDOFF files copied into it remain historical input, not this repaired preparation's current standing. `repair-manifest.json`, this report and the reviewer return identify the repaired candidate.

Original independent findings: `reviews/V5-WORKFLOW-WITNESS-PREPARATION.md`. Manager explicitly authorized the proposed copy-only spawn instrumentation: preserve the real sender/page path, use async-signal-safe bounded pre-exec registration and ACK, explicit FD ownership, and show the exact changed spawn boundary. No maintained Rust source, instruction, authority schema, receipt factory, fake native page, or production spawn replacement was edited.

## Repairs and limits

1. **Owned process cleanup.** `ownership_hook.rs` is injected only into a copied Host source. The version probe joins its own group; both version and app-server commands run a pre-exec hook. It uses only fixed-size stack data and libc `fcntl/getpid/getpgrp/write/poll/read/close/_exit`, with a five-second ACK bound. The supplier cannot exec before the Parent channel records its PID/group and stage. Both inherited channel FDs are close-on-exec and explicitly closed before exec. The launcher starts with a minimal environment and passes exactly the two channel FDs. Parent cleanup marks the channel closing (new records receive refusal), terminates owned groups while leaving the harness a chance to reap its direct children, escalates to kill, bounds harness termination/reap, drains late registration and verifies owned groups absent. `cleanup.json` records outcomes; failure prevents success. The Parent cannot `waitpid` grandchildren on macOS: direct-child reaping remains Host/harness work, while orphan reaping belongs to the OS. The result explicitly does not claim Parent reaping of nonchildren. No process-name killing is used. Process-group containment remains the stock supplier/Host group contract; this is not OS network containment or proof against arbitrary supplier descendants deliberately escaping groups.

2. **Actual run and artifact binding.** The launcher consumes a reviewed `compiled-binding.json`, verifies retained binary and emitted compiler artifact hashes, exact sole libtest compiler-artifact line, source/copy manifests, reconstructed bounded injection, copied fixture and helper hashes. It requires `running 1 test`, `1 passed; 0 failed; 0 ignored`, successful exit, and `witness-result.json` containing the exact unique invocation (UUID, root, candidate, binary, fixture, launcher, supplier manifest, holding manifest and test filter). An omitted witness, zero-match filter, missing/stale/foreign result or source drift cannot produce successful witness standing. The Rust result reads the unique launch binding in its owned root. This is source/build custody evidence, not cryptographic attestation of hostile binaries.

3. **HTTP400 causal standing.** Every provider response carries a unique per-invocation marker. The Parent records whether the 400 body was successfully sent; it then checks the matching native failed terminal's error for that marker. Only both observations establish the bounded HTTP400 cause. Otherwise a valid native source comparison is explicitly `cause unknown`; neither fixture nor launcher labels a generic failure HTTP400. No retries were added. Native terminal/error and provider observations are retained. Synthetic JSON tests exercise this classifier only and mint no native authority.

4. **Source and package custody.** `prepare_compile.py` resolves the supplied Git commit, archives its tracked App tree, compares the supplied source before copy, checks copied pre-injection equality and rechecks source drift. It retains full manifests and exact unified injection diff. Changes are confined to appended runtime test declaration, the copied witness fixture, and the explicit Host ownership hook/calls. Later compile output must preserve every input file. Four known Tauri generated schema paths may be added, are individually hashed/retained and are checked again by the launcher; other new outputs fail. No generated files are silently accepted as original candidate source. Source archival uses `git archive` and runs no supplier.

The approved supplier manifest is pinned to SHA `04898a5adac06aecba185c2e313b4758292c2c20c24e3da441da2b6fd617791e` (`probes/CODEX_0160_COMPLETE_DEVELOPMENT_INSTALL.json`). Launcher checks all 44 file paths, hashes, byte sizes and modes including sibling executable inputs; extra/missing files or symlinks fail. A read-only validation here matched all 44 files/332972398 bytes, without executing a supplier. Historical archive provenance and `qualifiedDistribution:false` remain separate from this witness.

5. **Failure evidence.** The Rust watchdog writes an atomic latest Host snapshot; Guard retains before-stop, stop result, after-stop and panic standing. Timeout can prevent Guard from running, so launcher cleanup evidence remains independent. Full test output and invocation, provider observations, compiler output and failure result are retained. No assertion was relaxed on the production workflow send or native source comparison.

## Checks actually performed

`python3 -m py_compile /private/tmp/chirality-wf-astra-repair-tvtlaytf/*.py` passed. `python3 /private/tmp/chirality-wf-astra-repair-tvtlaytf/test_repairs.py` passed **9 tests** (0.596s), using only owned inert local children and files. No network listener, supplier, native/auth/model operation, credentials, download or Cargo was invoked.

Final raw synthetic root: `/private/tmp/chirality-wf-synthetic-u5z0svmp`; log is `synthetic-test.log`. Earlier raw roots p3bn9vlj, x6fpfp6i and gdma2kt5 are retained as historical runs. Controls:

- Original exit-status-only predicate accepts inert `/usr/bin/true` with the witness filter and no executed test; repaired validator rejects zero-test output. This is a predicate reproduction, not an execution of the original HTTP launcher.
- Original timeout handler (unchanged handler, shortened inert initial wait) terminates/reaps the harness but leaves its explicitly owned separate child group alive. The control records that original-negative observation and then kills and verifies the group's absence.
- Repaired timeout cleanup passes separately for version-stage and app-stage groups, and for a group ignoring SIGTERM with an inert descendant. Harness reaping and group absence are recorded.
- Closing-channel registration is denied before exec; no inert exec marker is written.
- Missing/stale result rejected; HTTP400 cause stays unknown with no response or an unrelated native error; matching response plus unique native-error marker satisfies only the classifier.
- Copy injection check limits actual changes to three named files and retains exact diff at the synthetic root's `injection/injection.diff`.

Preparation-only negative: supplying the previously built a515 archive refused four extra Tauri `gen/schemas` outputs before copy/injection. Failure and exact delta remain in `/private/tmp/chirality-wf-bound-compile-xomdm_nd` and `preparation-only.log`. This is expected source-drift refusal, not a compile failure. Using its freshly extracted exact Git archive source passed preparation at `/private/tmp/chirality-wf-bound-compile-m4zt9vvj`; `preparation-clean-control.log` records the root. This validates only copying/manifests/injection against historical a515. It does not establish the future corrected candidate or compile viability. The four generated schema additions are explicitly treated as postcompile outputs, never candidate source inputs.

## Remaining execution prerequisites

- Original independent reviewer backcheck of these exact helpers, source diff, negative controls and limits; any findings repaired and returned through that reviewer.
- Corrected committed candidate from Parent; unchanged source input extracted fresh from that commit. The old a515 preparation control is not eligible for supplier execution.
- Explicit manager/Parent Cargo lane release. Invoke `prepare_compile.py` with the corrected candidate context/commit/repository and `--compile-approved`. This compiles a private copy only, offline/locked and skip-supplier, never runs tests. Tauri build prerequisites and actual Rust compile validity remain unverified. Retain any first failure; do not silently change prerequisites or permit unexpected generated drift.
- Review actual compiler-artifact binding and copied source/fixture/hook diff before Parent-only launcher execution. A helper source review alone cannot certify an uncompiled future binary.
- Parent alone runs the exact bound executable using the complete supplier record, fresh owned homes and holding copy. Native GUI/A15, model adoption/completed workflow execution and supplier distribution qualification remain separate and unperformed.

## Frozen private file hashes

- `owned_processes.py` — `6e0f8265b65dc0f60a926fefb6ad561ec83be8c95c447bc4ad2394ceaf3e3281`
- `ownership_hook.rs` — `f5b7a8315f60038107b00b054f452b4aec20096497560017ee32f8e489ce01bc`
- `parent_launch.py` — `a0bdfbe57a5e870cd27cb8401d3cf7d16eeefc31e897e0729b983f6e6447f52f`
- `parent_stock_workflow_witness.rs` — `2e9ff62673c5bb4f6dcabbb671063ee985bf1a5cf83985dba4ef32e9bb6f40b6`
- `preparation-clean-control.log` — `478ed0f82b26f5f87a4310e3def2ee4aa9be98fee0985b46de3496afb79c664a`
- `preparation-only.log` — `204523008c18d1e4ff265ad172194772f1881488a8a1e47c377dc778e851b174`
- `prepare_compile.py` — `4cbc4f0e214eff30ff3d79f4adc5e1c236fce2d58f58d5c4a39402304f929ff8`
- `supplier-read-only-validation.json` — `3a83176f8e93beb94b4616ea001930e794851841426744236ba8280289572027`
- `synthetic-test.log` — `a8d495151a39ad5aa95fe40dbe003b850c3f608a13db60cbf1886f2306bae9a9`
- `test_repairs.py` — `23c826eedc6b1938f987e3b88a91aded69de06f98d6b9544ce5374ddad68f9ff`
- `witness_common.py` — `a11444d3b43e322dcc64a4ed17af67c35d78d59c84bd7e54613fad8b610680f7`

## Consulted instruction and evidence origins

Root supplied by parent/user; TASK and Loop read; manual index, User Manual headings, Field Book and work graph consulted. Manager and reviewer reports read in full. Product hosting spawn/verify and build/config sections read selectively. No wider role or unselected workflow/skill body loaded.

- `AGENTS.md` — `f96feb19d297c74e10048c506805b2fe3622c50cfefd6078f599724556113977`
- `agents/AGENT_TASK.md` — `1a13a5b00b3ce01ff8519efe6b46bcbe0cd6a5b7985e24282fa7efa2c57c8fb7`
- `projects/chirality-app-v4/loop/LOOP_INIT.md` — `c2e88f81439ed03578fee13fd7563082fefdfe11096d9134a59531eba3b985bd`
- `docs/alignment-manual/README.md` — `5eee30d902c57a251bf885f91bfa0481a7834ec6945c3382baf15d2e2980c63d`
- `docs/alignment-manual/CHIRALITY_AGENT_USER_MANUAL_v3.md` — `2535efe547f2368e06d965d189efc47c7c46f28c2d6fd4777b0b8cece9003fa7`
- `docs/alignment-manual/Project_Management_for_Human_Agent_Teams_Field_Book_v1.md` — `02d53a3966220001318aacf3f46e1b63b8695a098c81b20f4e3e1531b93024d3`
- `projects/chirality-app-v4/execution/_Coordination/WorkGraphs/APP-V4-GROUP-A-20261004/WORK_GRAPH.md` — `7cc819947c5b187ba0371778a135f18f9f529c73c002ff0db4a6e1a172e3cd80`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/MANAGER_ASTRA_HANDOFF.md` — `843bafc599fb5729ec3cc546399e3bef65c620bacc27b3015b78439f6ea05806`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/reviews/V5-WORKFLOW-WITNESS-PREPARATION.md` — `fcd89c3bbf356c733e8a5e48e21d4da83d365d2fc3c20d941de2f8c34b6f4e9b`

## Independent R1 syntax finding and repair

Reviewer identified an extra closing brace in repaired Guard::drop (private fixture line 8). Confirmed with actual `rustfmt --check`: unexpected closing delimiter. First failure is `rustfmt-first-failure.log`; exact prior fixture/manifest/test log are retained under `review-r1-preimage/`. This was a real preparation blocker; the nine Python controls did not establish Rust syntax validity. Historical fixture-syntax files copied from original preparation are not checks of this repaired fixture.

Removed exactly the extra brace, then ran rustfmt on both private Rust files for readability. Actual `rustfmt --check` on repaired `parent_stock_workflow_witness.rs` and `ownership_hook.rs` passes (exit 0; empty `rustfmt-repaired-check.log`). The intermediate check parsed both but reported formatting differences, retained in `rustfmt-format-check.log`. Nine synthetic controls were rerun after the actual Rust syntax repair and pass; latest root is recorded in `synthetic-test.log`. No Cargo or typecheck performed, so compile viability remains unverified. The previous a515 preparation copy and first synthetic roots retain the failed fixture and are historical, not the repaired candidate. A new preparation/compilation must use the current hashes below.

Current replacement hashes after R1 syntax repair (supersede corresponding frozen-file hashes above only; old preimage retained):

- `ownership_hook.rs` — `dc0f1ed914748a3cd834161fbdc7919248274ffd19fbe78777c57aae7b744e3a`
- `parent_stock_workflow_witness.rs` — `55259658b63ac4040533eb740480d5886583d11ddb258143285a6d240fe1f735`
- `synthetic-test.log` — `a81d4e220402c4fcd9b5d4ae9b517aff4550dd5b6abb809d0d5f69efd0ab7c5e`
- `rustfmt-first-failure.log` — `22c24c25ebb2308e9fc74dab0d9f9c9a459533c7f7cb27e65cda1b74c8a8b573`
- `rustfmt-format-check.log` — `615222d795551cc8466666b15ae5e394ff55460bcb99d7d2e1bc63828450fa7d`
- `rustfmt-repaired-check.log` — `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

## Independent closure and corrected candidate preparation

Original reviewer `/root/group_a_execution_astra/workflow_witness_review` returned **READY for compile preparation** after independently checking the corrected Rust parser result and exact brace-plus-format delta. `reviews/V5-WORKFLOW-WITNESS-REPAIR.md` SHA `1f2b22167e90ccf417bee61e1ac2f45c73f1d064858a5b8ec831299019424dc9`. Its independent nine synthetic checks also reproduced the original negative predicates; no further actionable helper findings remained. This closes the helper preparation review blocker only, not compilation or native execution.

Manager supplied corrected committed candidate `832ec9de93f9d2f28bf536a323bef2d93e06d9f7`. Fresh exact Git archive input is retained at `/private/tmp/chirality-wf-corrected-source-bptn5jyr`; preparation-only execution passed with current reviewed helpers at `/private/tmp/chirality-wf-bound-compile-66gtm0gp`. `corrected-preparation-only.log` retains the run root. Source-before, copied-before, copied fixture, exact injection diff and final input manifests bind this revision. No Cargo ran, no executable was produced, and Parent still holds the shared Cargo lane. A later source successor requires a new preparation.

Corrected preparation evidence hashes:

- `/private/tmp/chirality-wf-bound-compile-66gtm0gp/source-before-copy.json` — `4eec1c12ec174eaf795e87d6d4bce06163f423166eabbbc0ee51f478758c1b03`
- `/private/tmp/chirality-wf-bound-compile-66gtm0gp/copied-pre-injection.json` — `4eec1c12ec174eaf795e87d6d4bce06163f423166eabbbc0ee51f478758c1b03`
- `/private/tmp/chirality-wf-bound-compile-66gtm0gp/injection.diff` — `a44482b88fed01995510bfeba3449553a8ad124436adf126f4458d02e35d6289`
- `/private/tmp/chirality-wf-bound-compile-66gtm0gp/injected-manifest.json` — `f618b3598db1d4875bbab6eab83f579753659d75ebb71a66eb95f23f6a5f8b4e`
- `/private/tmp/chirality-wf-bound-compile-66gtm0gp/preparation-binding.json` — `ae08386ce0955698179e41ff6dfbd50e944e71d6b787a3abc3787b25ced9da7b`

No active child processes, Cargo session or resource reservation remains with this TASK. Parent/manager owns the explicit compile release and subsequent exact compiled-artifact review/native execution boundary.

## Released no-run compilation — 2026-10-05

Parent completed the corrected832ec9 full archive checks and explicitly released the sole Cargo lane to this TASK. No maintained source or branch changes were permitted. The command used the same fresh exact Git archive input `/private/tmp/chirality-wf-corrected-source-bptn5jyr/projects/chirality-app-v4`, resolved the exact commit again, created fresh preparation and ran `--compile-approved` with offline/locked, `CHIRALITY_SKIP_CODEX=1`, lib no-run and JSON compiler-artifact output.

**First failure preserved:** `/private/tmp/chirality-wf-bound-compile-sh8m_x16` retains source/binding and complete output. Rustup's Cargo shim could not choose a version because the fresh build HOME had no default toolchain. No compiler/typecheck ran in that attempt. The helper log is `compile-first-attempt.log`. The manager authorized only a private build-runtime binding to the existing installed toolchain. No rustup setting, source/fixture repair, download or user configuration change was made.

`prepare_compile.py` now uses `/Users/ryan/.rustup/toolchains/stable-aarch64-apple-darwin/bin/{cargo,rustc,rustdoc}` explicitly, puts that installed toolchain in PATH, and records each executable's path/hash/version in `toolchain-binding.json` and the compiled binding. Exact old helper is `prepare_compile-before-toolchain.py`; exact successor diff is `toolchain-helper.diff`. Cargo/rustc/rustdoc report 1.92.0. This is the only helper semantic change after preparation review.

**Retry succeeded:** `/private/tmp/chirality-wf-bound-compile-dxb5u0js`, session11379 exit0. No source or fixture syntax/type change was needed. The helper verified unchanged original/injected source files; only the four explicitly named Tauri schema outputs were added and retained with hashes. The exact sole compiler-artifact executable was copied to `reviewed-tests` (mode0500). No test executable, supplier or Parent launcher was executed.

Read-only `parent_launch.validate_compiled` passed against this result, including reconstructed injection/candidate manifests, all required helper and fixture hashes, sole compiler-artifact path and emitted/copied executable equality. Evidence is `compile-binding-validation.json`; this does not replace independent review or execute the binary. The shared Cargo lane was explicitly released on successful return; no active process/resource reservation remains.

Compiled successor identifiers:

- `/private/tmp/chirality-wf-bound-compile-dxb5u0js/compiled-binding.json` — `5a927f50d61f60dbc48fd610272b52979567b9ef63adac82141038b514930df1`
- `/private/tmp/chirality-wf-bound-compile-dxb5u0js/reviewed-tests` — `d9a02ece0f053805f5a2bde7732965af24484784a279d407804f82d5c2c0067a`
- `/private/tmp/chirality-wf-bound-compile-dxb5u0js/toolchain-binding.json` — `9115d3e33070a16af369b191138842c4bece03727ea1e3e8930976fdcf133dff`
- `/private/tmp/chirality-wf-bound-compile-dxb5u0js/compile.stdout.jsonl` — `9167bf449e9e6b6f69830081ab9bf10f89d468d87866bc52f8c37eb4ab774ba8`
- `/private/tmp/chirality-wf-bound-compile-dxb5u0js/compile.stderr.log` — `b8e25f80654d66b455c088b881672912baed785011bdb1ca83449bcdd9ed44d9`
- `/private/tmp/chirality-wf-bound-compile-dxb5u0js/compile-outcome.json` — `776ebb5753166bf1a42dd3b2f93b4db021a5842967ce27fe52269b3075662173`
- `/private/tmp/chirality-wf-bound-compile-dxb5u0js/injection.diff` — `a44482b88fed01995510bfeba3449553a8ad124436adf126f4458d02e35d6289`
- `/private/tmp/chirality-wf-bound-compile-dxb5u0js/injected-manifest.json` — `f618b3598db1d4875bbab6eab83f579753659d75ebb71a66eb95f23f6a5f8b4e`
- `/private/tmp/chirality-wf-bound-compile-dxb5u0js/intentional-generated-outputs.json` — `f25e83e3e9b8bd7c09f73dd4f655a4fb4526d1012bd21b7afac90207d4509a90`
- Current `prepare_compile.py` — `2d9d7cadf30874f5d53a5d5a562e2a1c1412a4bec84a64c915c7426b96e04a2e`
- Current private `repair-manifest.json` — `63cecf2ba81b247aba8092f5153f9a564314eccb69516782fb700da627f2399b`

Original independent reviewer must backcheck the explicit toolchain helper delta and actual emitted-artifact/source/fixture binding. Parent alone retains the native execution boundary. Earlier compile-pending statements describe their preparation-time standing; this no-run result supersedes that limit only for this exact private832ec9 artifact. No native failed-turn or workflow source-comparison observation has yet occurred.

## Parent final isolation requirements — Python-only successor

The original reviewer completed compiled-artifact backcheck READY (`reviews/V5-WORKFLOW-WITNESS-REPAIR.md`, then SHA `13526b7705c41ea367e40a384671625cbe7491baf6e1f2cc26c29ede27d3c4a7`). Parent subsequently required two private launcher adjustments before execution: actual `mktemp -d` creation of both Codex homes per Loop, and `cli_auth_credentials_store = "file"` to avoid keychain fallback. This is a new bounded Python-only successor, not a retroactive claim about the prior launcher.

`create_codex_homes` now invokes `/usr/bin/mktemp -d` for each of codex-home/probe-home inside the unique owned run root, with a minimal environment. It checks successful creation, physical empty directories, mode0700 and same-filesystem identity, then renames each to the unchanged Rust fixture's expected path. Device/inode equality before/after confirms that the moved directory is the actual mktemp-created directory. Commands, actual returned paths, moves and physical identities are retained in `home-creation.json` and the invocation. `os-home`/other scratch directories remain ordinary owned scratch. Stand-in config adds the explicit file credential store; all other config values remain unchanged. No credential file or keychain was read or used.

Original launcher and compiled binding remain unchanged in `parent-final-preimage/` and the original compile root respectively. The retained Rust source, injected Host hook, compiler log, compiled binary and fixture hashes are unchanged. No Cargo was run and no rebuild is implied. The new `launcher-successor-binding.json` names and hashes its exact original `compiled-binding.json`, updates only `helperHashes.parent_launch.py`, and records the Python-only succession. The validator checks that removing the succession field and restoring the original launcher hash yields the exact original binding; it verifies the original compiled launcher preimage and performs every previous source/fixture/compiler-artifact check. Any unrelated field change fails. The Parent must pass the **new successor path and new checksum**, not the old compiled-binding checksum. This explicitly separates compiler custody from the later launcher-only repair.

Five focused controls passed, `parent-final-controls.log`, raw root `/private/tmp/chirality-wf-final-controls-50gtoap_`:

- Actual mktemp creation/mode and same-device/inode move; reusing a home destination refused.
- Old config lacked explicit file store; new config has exactly that added value (TOML parsed without running the launcher or opening a listener).
- Original compiled binding rejects the changed launcher.
- Explicit successor validates against unchanged compiled artifact/Rust inputs, with a different binding hash.
- Successor with an unrelated candidate change is rejected.

Python parsing also passed. No supplier, launcher main, native/auth/model/network/download or Cargo operation occurred. No active process or resource hold remains. Original independent reviewer must backcheck this exact Python delta, actual controls and explicit unchanged-artifact binding succession before Parent execution.

Exact successor inputs:

- `/private/tmp/chirality-wf-astra-repair-tvtlaytf/parent_launch.py` — `d23f869af818acda66579054caa804156a4fa1208dc9b7daf2ca4fe6966eca44`
- `/private/tmp/chirality-wf-astra-repair-tvtlaytf/parent-final-launcher.diff` — `408ba054a38953c998f9cc436e1730085351942b151701b067604c734986e546`
- `/private/tmp/chirality-wf-astra-repair-tvtlaytf/test_parent_final_adjustments.py` — `aeb048cfb9ff9544e2f812d699b2e231befdc89b0de9beef55fe93b086bda58d`
- `/private/tmp/chirality-wf-astra-repair-tvtlaytf/parent-final-controls.log` — `4b40a29addfa9b0916db1265f0486e0823048452e85ef0687c1f1a23bf76d989`
- `/private/tmp/chirality-wf-astra-repair-tvtlaytf/repair-manifest.json` — `5f368e17cc97977b70883a37b9ccd91b19b073f226aa21ba2aca21b0469bde30`
- `/private/tmp/chirality-wf-bound-compile-dxb5u0js/compiled-binding.json` — `5a927f50d61f60dbc48fd610272b52979567b9ef63adac82141038b514930df1`
- `/private/tmp/chirality-wf-bound-compile-dxb5u0js/launcher-successor-binding.json` — `4ff42e8c6c30e3ad5fdde7869d78a8a534441b77be8315aa93b4082c27639e9c`
- `/private/tmp/chirality-wf-bound-compile-dxb5u0js/reviewed-tests` — `d9a02ece0f053805f5a2bde7732965af24484784a279d407804f82d5c2c0067a`

Parent invocation uses `--compiled-binding /private/tmp/chirality-wf-bound-compile-dxb5u0js/launcher-successor-binding.json --reviewed-binding-sha256 4ff42e8c6c30e3ad5fdde7869d78a8a534441b77be8315aa93b4082c27639e9c` with the reviewed successor launcher. The prior supplier manifest, holding-copy and fresh evidence destination requirements remain applicable. This record does not authorize or perform the Parent invocation.

## First actual Parent run and missing LT-24 fixture precondition

Parent's final Python successor was independently READY (review SHA `9537a1cf38bc0418cc10ce8ca4fa300c025173d192a940fc836585830828c296`). Parent then executed the exact reviewed pair. Original actual result is **FAIL**, preserved without edits at `/private/tmp/chirality-workflow-native-witness-832ec9-run1` and original owned root `/private/tmp/chirality-parent-stock-wf-04hi5b44`. Only named noncredential observation files were read/copied; home contents/authentication material were not read. Exact paths and SHA-256 of those files are in new private `run1-evidence-origins.json` and independently rechecked unchanged by the focused controls.

The real libtest failed at fixture line138 `host.start(...).unwrap()`: `main binary matches development assertion; qualified full distribution identity absent`. Host snapshot retains LT-01→LT-05, state refused, verification `unverifiable`, null generation/supplier standing. Only the version-probe stage1 process was registered; Parent cleanup records harness reaped, group absent, channel closed, no errors, clean=true. There was no app-server stage2, workflow thread/send/source page, provider observation, model prediction, auth, native capture or A15. Host Guard's stop attempt returned `stop not accepted in state refused`; independent Parent cleanup still verified owned process absence.

**Diagnosis: private fixture omitted an existing required development-start choice; this is not a Host product defect.** `HostConfig::new` defaults `allow_unverified_dev=false`. The fixture set only `expected_sha256`, which Host deliberately treats as a main-binary development assertion, not full qualified distribution identity. `Host::start` permits existing LT-24 only when the caller explicitly opts in, result is `unverifiable` and a matching observed label exists; mismatches still refuse. With the default false, LT-05 was the correct behavior. The complete 44-file launcher manifest check does not manufacture qualified Host distribution identity.

Authority/source basis: OWNER_DECISIONS “Observed latest supplier and provider result” records approved development supplier evidence, expressly not supplier qualification; README's development startup requires the explicit option and label. Accepted HOSTING_BOUNDARY §7.2/LT-24 preserves unverifiable and `unverified-development`, no production/release reliance. Manager confirmed the approved development supplier basis permits Parent to select that existing route and explicitly authorized this private correction. No new authority, automatic fallback or weakening of verification is proposed.

## LT-24 private correction, prepared only

New disjoint helper directory `/private/tmp/chirality-wf-lt24-repair-6j6d7nyu` preserves the previously run helper directory `/private/tmp/chirality-wf-astra-repair-tvtlaytf` unchanged. `lt24-preimage/` retains the exact run1 launcher/fixture. `lt24-correction.diff` is the complete correction:

- Launcher requires Parent to pass `--allow-unverified-development` in addition to `--execute-reviewed`; omission fails before input reads or supplier activity. The explicit choice becomes invocation `developmentStart` with allowUnverifiedDev=true, transition LT-24, supplierStanding unverified-development and qualifiedDistribution=false.
- Fixture reads that invocation before Host creation/start, requires the exact development standing/nonqualification and explicit true choice, and sets only the existing `cfg.allow_unverified_dev`. Host code, verify rules, expected main hash and pinned source remain untouched.
- After successful start, fixture requires returned `supplierStanding=unverified-development`, unchanged `verification.result=unverifiable`, and actual LT-24 development-start-authorized lifecycle observation. It retains those fields in the result. No fake lifecycle/native page is injected. The production sender/page consumer, provider causality checks, cleanup and home isolation are unchanged.

`rustfmt --check` on actual successor fixture/hook passes. Five Python/read-only controls pass: explicit option produces the exact bounded declaration; CLI omission refuses before nonexistent input reads; original run proves correct LT-05 refusal and clean stage1-only cleanup; old artifact binding rejects changed helpers/fixture; all named original actual-run files remain byte-identical. These controls do not execute the Rust fixture or supplier.

Fresh preparation-only source/copy/injection binding to exact `832ec9de93f9d2f28bf536a323bef2d93e06d9f7` passed at `/private/tmp/chirality-wf-bound-compile-uitqs0ds`. No Cargo ran: Root file-act owner holds that lane. **Rust fixture changed, so a new no-run compile and independently reviewed emitted artifact are mandatory.** Neither prior binaryd9a02ece nor launcher-successor binding4ff42e8c is relabelled as this correction. Prior private manifests/HANDOFF files copied into the new directory remain historical; `lt24-repair-manifest.json` is this prepared successor's inventory.

Current exact preparation identifiers:

- `/private/tmp/chirality-wf-lt24-repair-6j6d7nyu/parent_launch.py` — `8651b50db2385dc43b2404275cba79d248e305599294b2682f0c99eb6084cb21`
- `/private/tmp/chirality-wf-lt24-repair-6j6d7nyu/parent_stock_workflow_witness.rs` — `9409a7461dfcf579a6154e9186b7d59bc7da78e36075b238c9fe73fe7e3fe355`
- `/private/tmp/chirality-wf-lt24-repair-6j6d7nyu/prepare_compile.py` — `2d9d7cadf30874f5d53a5d5a562e2a1c1412a4bec84a64c915c7426b96e04a2e`
- `/private/tmp/chirality-wf-lt24-repair-6j6d7nyu/ownership_hook.rs` — `dc0f1ed914748a3cd834161fbdc7919248274ffd19fbe78777c57aae7b744e3a`
- `/private/tmp/chirality-wf-lt24-repair-6j6d7nyu/owned_processes.py` — `6e0f8265b65dc0f60a926fefb6ad561ec83be8c95c447bc4ad2394ceaf3e3281`
- `/private/tmp/chirality-wf-lt24-repair-6j6d7nyu/witness_common.py` — `a11444d3b43e322dcc64a4ed17af67c35d78d59c84bd7e54613fad8b610680f7`
- `/private/tmp/chirality-wf-lt24-repair-6j6d7nyu/lt24-correction.diff` — `4d3d6f796d5b9005a0d896b869d304e35b75d1f7f50b8c7ed0ed3caf1d8b9b7f`
- `/private/tmp/chirality-wf-lt24-repair-6j6d7nyu/lt24-rustfmt-check.log` — `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `/private/tmp/chirality-wf-lt24-repair-6j6d7nyu/lt24-controls.log` — `97fec459eaed3777fdb8ac591f0a4df1d56b6f9796760298d17ddb3455b5bc06`
- `/private/tmp/chirality-wf-lt24-repair-6j6d7nyu/test_lt24_preparation.py` — `d6123ce5550fa13884fd70cc716dd5c6c9b93c96f0a87e6e6b3e27c11b7e6b8d`
- `/private/tmp/chirality-wf-lt24-repair-6j6d7nyu/lt24-preparation-only.log` — `e6a0bd4ee6903c5276c9b7d8c44e4a2c6fdd80f5b568943ce118050ebc419564`
- `/private/tmp/chirality-wf-lt24-repair-6j6d7nyu/run1-evidence-origins.json` — `db764b1e822fca1f080f8bd8ae7a9c018d7c389de90743605098013c5327027c`
- `/private/tmp/chirality-wf-lt24-repair-6j6d7nyu/lt24-repair-manifest.json` — `48616fe2794b67c6ee8c87a1e113c71fb6c68bcdb858464ab91f696d0022a3b2`
- `/private/tmp/chirality-wf-bound-compile-uitqs0ds/preparation-binding.json` — `5a6e96b492c8098ed9fdfa905cab78a7a81c0404accd4c930a63d26a5f2f1bd6`
- `/private/tmp/chirality-wf-bound-compile-uitqs0ds/injection.diff` — `c035b11ba594a1b92171a20a69944507368c68e5a8966255761ac8b8cbb41c03`
- `/private/tmp/chirality-wf-bound-compile-uitqs0ds/injected-manifest.json` — `2ee93ae516bac7ccea75f2146846a1fc0dd58a0c2711b566653878e0d7ac2e68`

Selective source origins read for this diagnosis:

- `projects/chirality-app-v4/app/src-tauri/src/hosting.rs` — `c8fcbfa53c7e3db24fc771c9dc883d8bfd6481512f6d06ecc39164bff71a92f3`
- `projects/chirality-app-v4/app/README.md` — `d0448fc360820b51509308e707ffea9bf440ef7b869547a97ef8c8dc35c386e4`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/OWNER_DECISIONS.md` — `7af629c9c83df4f866d13f923f15352c0b947fa6f15d4a23b03c7f6e3576a535`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-01_Stock Codex hosting and supplier contract/Design/HOSTING_BOUNDARY.md` — `9839cb38310ff55045657e51f7bb7dcfcb2024eb43ec3bab364959e33e5c1e85`

Next boundary: original independent reviewer checks the precise precondition/correction and omission/standing assertions; manager later grants Cargo for a fresh artifact if accepted. Parent alone retries with the newly reviewed binary/binding and explicit development flag, preserving run1 as failure. No test or supplier execution, network/auth/model/credential operation, product edit or resource hold occurred in this diagnosis/preparation turn.

## LT-24 fresh no-run compile

Original reviewer returned READY for fresh compile preparation (review SHA `e530448c13f51df24a61fe97efd0686aeeea3a391e911a24ef02e859973e33fe`), with five independent controls and syntax checks passed. Root released Cargo; manager explicitly assigned this TASK the sole lane for the exact832ec9 private LT-24 successor.

Fresh compilation at `/private/tmp/chirality-wf-bound-compile-5jdyk4f7` succeeded on its first attempt, session44179 exit0, with the existing bound toolchain, scratch build HOME, offline/locked, skip supplier and `--lib --no-run --message-format=json`. Reviewed fixture/launcher and all other helpers were unchanged during compilation. Original sources, copied sources, bounded injection and emitted sole test executable are retained; only the named Tauri generated schemas were added. No additional build failure or repair occurred. Read-only `validate_compiled` on the new original compiled binding passed all source/helper/fixture/compiler-artifact checks. No binary/test/supplier/Parent launcher execution occurred.

The Cargo lane was explicitly released immediately on successful result, with no process/resource hold. Original artifactd9a02ece and both Parent run1 roots remain unchanged historical inputs. New LT-24 artifact582ed82b is a genuinely new no-run executable, not a relabelled earlier binding. Original reviewer must examine this new exact artifact/binding before Parent retry; Parent must use `--allow-unverified-development` with the new launcher and compiled-binding checksum.

Exact new compile evidence:

- `/private/tmp/chirality-wf-bound-compile-5jdyk4f7/compiled-binding.json` — `a68848f47fa463aee8c33ddf4ff1489090de4363b4d2ae8b7468afbf306c7d1b`
- `/private/tmp/chirality-wf-bound-compile-5jdyk4f7/reviewed-tests` — `582ed82be49823dab078736a31af89fc7f5cdb32bf80fa47e77a1b3b1ab2a74b`
- `/private/tmp/chirality-wf-bound-compile-5jdyk4f7/compile.stdout.jsonl` — `557d10a3c10bc2e32c3860267330f042080a79b44679273daa9e4c0b8bf69baa`
- `/private/tmp/chirality-wf-bound-compile-5jdyk4f7/compile.stderr.log` — `a0b832d72082a0c7fe467279d4204da3642edee34397639592ab400bcad92004`
- `/private/tmp/chirality-wf-bound-compile-5jdyk4f7/compile-outcome.json` — `dcdef1ac5fc1d657de53ff59e741514da023817aa76097e5e4652a3a64e295d0`
- `/private/tmp/chirality-wf-bound-compile-5jdyk4f7/toolchain-binding.json` — `9115d3e33070a16af369b191138842c4bece03727ea1e3e8930976fdcf133dff`
- `/private/tmp/chirality-wf-bound-compile-5jdyk4f7/injection.diff` — `c035b11ba594a1b92171a20a69944507368c68e5a8966255761ac8b8cbb41c03`
- `/private/tmp/chirality-wf-bound-compile-5jdyk4f7/injected-manifest.json` — `2ee93ae516bac7ccea75f2146846a1fc0dd58a0c2711b566653878e0d7ac2e68`
- `/private/tmp/chirality-wf-bound-compile-5jdyk4f7/intentional-generated-outputs.json` — `f25e83e3e9b8bd7c09f73dd4f655a4fb4526d1012bd21b7afac90207d4509a90`
- `/private/tmp/chirality-wf-lt24-repair-6j6d7nyu/lt24-compile.log` — `26e6a1a161bdd2db3ea9c0fdf561f88f723eaf61e03f4307469e9c5ca89c8f62`
- `/private/tmp/chirality-wf-lt24-repair-6j6d7nyu/lt24-compile-return.json` — `0d038011eb9d151aa47e572b707dd4ecf0e6cb5f3fb4784592fa30c6cccbf05a`
