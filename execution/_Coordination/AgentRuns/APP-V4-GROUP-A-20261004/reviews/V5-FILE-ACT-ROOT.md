# V5 File-act Root consumer independent review

## Initial source review — 2026-10-05

**NOT READY: FR-1 blocks this five-path consumer.** This is a read-only source review, not an executed backcheck. Type 2 TASK `/root/group_a_execution_astra/file_act_root_review`, parent `/root/group_a_execution_astra`, delegated-harness-native, supplied gpt-6-astra / low. No delegation, Cargo, test execution, Git, native/supplier/auth/model/network/download/credential action or product-source edit. Sole write is this review.

Reviewed original private `/private/tmp/chirality-file-act-root-in82xerc/app`; independently recomputed patch SHA-256 `a45847281f3b55f886019e399215cb13719160c0d00bbeaa238518e8526cf9a5` and all five changed-source pins in its `freeze.json`. Baseline comparison independently found only original `src-tauri/src/lib.rs` and `src/App.tsx` changed; 248 original files unchanged. Three additions are `file_act_root.rs`, `file_act_view.rs`, `FileActPanel.tsx`. Core V5-R2 bounded review/verification is retained, not reopened. Parent reports initial exact consumer lib compilation passed; this review has not independently executed or sealed that result.

### FR-1 — blocking P2: continuing a different hot offer changes the current preview's controls and outcome

Location: `src/FileActPanel.tsx:19`, `:43–49`, original hash `f2b485e10e2017af1e025afd04dfee45369a3740181b27b7ea6837b7206b88f5`.

Trigger: offer A has a durable pending or uncertain capture; read the log so A has a hot continuation button; select file B and obtain a new unattempted preview; continue A from its hot row. `run` unconditionally calls `setStatus(result); setAttempted(true)` for every continuation. Consequently B's confirm/dismiss buttons become disabled, A's outcome is displayed in the current preview context, and the preview continuation button derives its availability from A's capture but sends `preview.reference` (B). B then fails continuation despite never being attempted. The hot A row itself remains stale until a separate read. This is concrete cross-offer association failure, not native custody forgery: Rust still refuses B without its own capture.

Criterion: AAC AK-d and §3's per-offer transition table; AAC §4.1 steps 6–7 / AS missing-in-record display. Original capture results and continuation must stay associated with their original offer; operating A cannot make B appear attempted or consume B's available control.

Repair: retain status/attempted by opaque offer reference, update the current preview's state only when the command target equals it, label outcomes with the matching subject/reference, and update or refresh the corresponding hot row. An explicit reference-bearing command result is preferable to an unassociated global status. Preserve original Rust custody and never switch the continuation target to fit the displayed status. Add an actual frontend control covering A pending → B selected → A continued, asserting A outcome remains A and B can still confirm/dismiss. Preserve an original-negative result before applying the fix, then backcheck the same criterion.

### Receiving trace and non-findings

- AAC §1.2 / AK-c / AI-1: `file_act_select` gets its path from the native picker; `FileActRoot::compose` keeps the actual opaque core offer, immutable preview and bytes. UI displays full offer JSON and exact UTF-8/hex, and explains that field edits require a new offer. No renderer-provided path/actor/context/native-source DTO can manufacture this consumer's confirmation event. Existing core native producer and byte checks remain separately reviewed.
- AAC AI-5/§7 and native context: `file_act_observe` reads original active HomeSession, native Host observation, runtime actor revision, configured App name and OS account plus workspace identity. Equality with original context is required by the callback. Root/home/runtime locks use fail-fast acquisition; map locks are dropped before offer-owner acquisition. The prior WRC-1 repair is present in runtime; no opposing blocking Root acquisition was established. This is source reasoning, not native execution evidence.
- AAC AX-05/06/08/09 and §4.1 failures: original offer owner survives native operation; attempted flag prevents repeated native attempt; errors do not relabel uncertain publication as AC-8. Definite capture errors remain visible in error detail. Continue uses original offer and historical capture, without substituting today's actor; dismiss cannot erase an attempted operation. No new core replay authority is introduced.
- RS record-out/corrections and AS comparison: reader uses contained regular-file snapshots, schema validation, explicit capture correspondence, shared correction projection, raw identity conflicts and source limits. Read path contains no record/lapse writer. Comparison labels separate current match, difference, subject absence, unavailable and incomparable identity, with recorded lapse claims explicitly qualified. Cold files remain claims without native-origin proof. No claim of checkpoint counting or complete historical lapse interval is established.
- AAC AK-a/AK-b and NIR placement: persistent standalone act/log panel, every existing NativeRequestCard (including question/elicitation), workflow-review entry and saved-native-output link are connected. Links require a person click and create no act/request settlement. General file/output browsing and actual arrival-row source/request linkage do not exist here; accepted AK-a/AI-3 coverage therefore remains unfinished in its owning graph. Existing links truthfully state standing/no arrival; these omissions are not a reason to fabricate references or claim full NIR completion.

### Verification and successor boundary

Original five written Rust tests are source-inspected, not executed by this reviewer. They do not cover connected native seam → capture → record → view, stale actor/content returns, uncertain/missing/mismatched evidence and correction/lapse inverse cases. The author already identifies these gaps. Parent authorized the author to use the sole Cargo lane and subsequently authorized a private `file_act_native.rs` expansion: a private production choice adapter and cfg(test)-only wrapper. The original pins above remain the reviewed initial candidate; the successor's complete changed boundary and ordinary-build absence checks require independent review. Final executed backcheck must follow actual compiled return and explicit lane release; it is not implied by this report.

No whole-Group-A READY, human/native act, SEAL-2, acceptance or release is claimed. The missing native person-use evidence remains separate from source-based custody conclusions.

### Actual context custody

Root AGENTS supplied; TASK, software-code-review and v4 Loop read. Current manual README and Agent User Manual headings through three levels read; Field Book read (initial combined output truncated, remaining sections read separately). Graph read selectively; AAC §§1.2–4.1, RS record-out, AS failure/display clauses, core V5/R1/R2 and WRC-1 original/backcheck, actual bounded consumer and core call paths consulted. No workflow or other role body activated. An initial path search mistakenly opened App v3 `AGENTS.md`; v4 Loop explicitly excludes those instructions, and no v3 tool/gate was applied. This wider consultation is recorded rather than hidden.

| Instruction/manual origin | SHA-256 |
|---|---|
| `AGENTS.md` | `f96feb19d297c74e10048c506805b2fe3622c50cfefd6078f599724556113977` |
| `agents/AGENT_TASK.md` | `1a13a5b00b3ce01ff8519efe6b46bcbe0cd6a5b7985e24282fa7efa2c57c8fb7` |
| `.agents/skills/software-code-review/SKILL.md` | `ee085d589c44f912d11a59eead8edac214f0343761d26b0d33e886a979888bca` |
| `projects/chirality-app-v4/loop/LOOP_INIT.md` | `c2e88f81439ed03578fee13fd7563082fefdfe11096d9134a59531eba3b985bd` |
| `projects/chirality-app-dev/AGENTS.md` (inapplicable, accidental consultation) | `41995dfe123041e1d0235a73e532fddb913f2c2124a9e8ec43857a87d7e5822c` |
| `docs/alignment-manual/README.md` | `5eee30d902c57a251bf885f91bfa0481a7834ec6945c3382baf15d2e2980c63d` |
| `docs/alignment-manual/CHIRALITY_AGENT_USER_MANUAL_v3.md` | `2535efe547f2368e06d965d189efc47c7c46f28c2d6fd4777b0b8cece9003fa7` |
| `docs/alignment-manual/Project_Management_for_Human_Agent_Teams_Field_Book_v1.md` | `02d53a3966220001318aacf3f46e1b63b8695a098c81b20f4e3e1531b93024d3` |

## V5-ROOT-R1 — repaired successor and independent executed backcheck

**READY for bounded parent fan-in of this seven-path consumer. FR-1 is closed on the exact successor below; no unresolved blocking finding remains in this review scope.** Parent explicitly released the author lane and authorized independent execution of retained immutable artifacts, without Cargo/shared-target writes. Reviewer ran no Cargo or compiler, changed no product source, and exercised no native dialog/supplier/auth/network operation. All reviewer subprocesses completed; no reservation or process remains held.

### Exact candidate and evidence binding

Author return independently hashes to `6431bcfd0f3e86e20a8f6be9d4b6ba739b17689ff8c5419225d6492e1ad60ed1`. Recomputed successor patch `321b28d2f52eac19b5a338a3d5c8dcbdde266d96643910e68e5a998baed2baee`, source manifest `386c79006dec8e1be77587aa048ed7d13942568f631291854c289e8c86c5da2f`, and all 254 source manifest entries before and after independent execution. All seven freeze pins match. Baseline comparison confirms only three originals changed (lib.rs, App.tsx, file_act_native.rs), four additions and 247 originals unchanged; other reviewed core and runtime sources retain their prior warrants.

All five archived binary/rlib hashes match `freeze-r1.json`. Every retained command metadata log/source hash recomputes; final selected-run source manifests match every final source entry. Preliminary first compile/tests, connected-first and integrated-compile are not silently treated as final-candidate evidence. Author SUMMARY hash `7dcc24c217d5f2fa8b8198d056ba1c044bd7537ee5bcf76cd63098c49b88e7c6` reports 76 distinct ordinary tests, with repeated observer deducted and four FIFO workers separate. This reviewer did not rebuild the artifacts: source association rests on the retained controlled-build records and unchanged source, not reproducible binary attestation.

### Repair and expanded boundary

FR-1 repair uses reference-keyed outcomes and attempts. Current-preview status/attempted derives only from its opaque reference; a continuation updates its own reference, and each hot row renders its matching outcome. Selection dismissal has separate state. The same actual-component hook/event harness reproduces the original failure on archived original source and passes against repaired source. It verifies B confirm/dismiss remain enabled, no B continuation is invented, actual continuation target is A, and A's row displays AC-7. The oracle is unchanged; the test uses the actual component handler with synthetic React state scheduling, not a reimplementation of its transition logic. This is frontend state evidence, not browser rendering/accessibility or native person evidence.

The authorized native adapter factor preserves production order: actual observer → freeze original offer/text/digest → actual native dialog closure → closed act/decline/cancel result → actual observer again → actor/context equality → privately constructed event → original consume. The production closure retains the same title, warning, three buttons and blocking result API. `confirm_with_adapter` is private in the native module; the synthetic inherent method exists only under `#[cfg(test)]`. Root's private shared helper retains original owner/control guards and original context callback; the Tauri command always supplies the real native producer. There is no ordinary-build renderer-choice entry or public mint added. Archived ordinary rlib positive ActControl probe exits 0; synthetic method probe produces E0599 absence, rather than merely private-access E0603. These logs/rlib were inspected and hash-bound, not independently recompiled. Source review additionally establishes the private in-crate adapter boundary.

Connected consumer tests now run actual Root confirmation ownership and the same native adapter sequence through production core/store/reader. They cover all three kinds with both act and decline, once-only original continuation, actor versus recorder, byte comparison after modification/deletion, full-tree read census, cancel and changed actor/content/root during the choice callback, uncertain capture versus durable record pending, and missing/mismatched capture correspondence without native-origin upgrade. The continuation fixture directly calls the same core API with the retained original Root offer; it does not execute a Tauri IPC/native picker. The unchanged actual continuation command was source traced. Reader code remains unchanged from initial review; shared correction integration tests exercise its reused projector but do not constitute an exhaustive new file-act-specific historical lapse fixture suite.

### Independent execution

**21 selected Rust tests passed, zero failures.** Selections include all nine consumer tests (four connected functions, two Root tests, two reader tests, one actual observer), core definite capture failure and uncertain-publication controls, both original WRC-1 lock controls, retained A15 publication behavior, A16 cold-authority refusal, connected decide/view, and all five general correction tests. Each command selected at least one actual test. FR-1 actual-component original-negative exits 1 at the specified B-disabled assertion; the identical repaired control exits 0. No expected failure was counted as a passing Rust test.

Independent commands, exit statuses, result lines and SHA-256-bound logs are in `/private/tmp/chirality-root-independent-97yswahi/RESULTS.json`, SHA-256 `28f1ab561c453dc73e7426885356a0590e6bec4e724c54e4833fb770a3c19f08`. Executables ran directly from the frozen validation directory, with `CHIRALITY_SKIP_CODEX=1` and supplier/workspace overrides removed. The Node harness wrote transpiled artifacts only to that independent scratch directory. Reusing author tests is independent selection/execution and criterion backchecking, not independent test authorship.

### Fan-in limits and pins

Apply only this reviewed patch's bounded hunks against the actual receiving candidate; do not replace the whole private App snapshot or concurrent hosting work. Integration checks must cover the resulting source. Retain original FR-1 failure and successor evidence. Native three-button/picker/actual actor interaction, visual/keyboard operation, general-file/arrival entry joins, checkpoint counting, trustworthy cold provenance (SEAL-2), complete lapse-history evidence, Group A acceptance and release remain separate unfinished obligations. They do not invalidate the bounded source/synthetic results and are not claimed complete here.

| Successor changed path | SHA-256 |
|---|---|
| `src-tauri/src/file_act_consumer_tests.rs` | `07a1bf70e07aaf7d7e28fbc1ce528d6ccbc1885f51e87590ea100e50bfdb29db` |
| `src-tauri/src/file_act_native.rs` | `0f13bb5c2a8aaa396a2622226edfe69ebc8204b7e22d445e340f5b010f854aa1` |
| `src-tauri/src/file_act_root.rs` | `33afb4b1b00324d29f2382515ae9fed0ae02312ab0ad77287ee3bc55ced8e507` |
| `src-tauri/src/file_act_view.rs` | `b3c0fda673079b4644fecf7d79b16922e706523215b9c56bc4354450dea07170` |
| `src-tauri/src/lib.rs` | `aca501453e1897245fb3b53b37e7d28e5e330983594771c3d7816e935d7980cf` |
| `src/App.tsx` | `e542116a6270783432e0d9724b4c6676888ca0c244492ab9140a360ac8b6a4cb` |
| `src/FileActPanel.tsx` | `d3e9faa7c55c84ece5ca4da4f17ff45e44e69ea5a369cf0d23c9fbe02308d043` |

## Final integrated-candidate preservation and README claim check

**Bounded READY preserved; no actionable mismatch found.** On the manager's receiving `0329f8fe6b1530eb4f084587dc46c908ba2436ed` candidate, independently recomputed all 12 maintained App source hashes against the combined reviewed core and Root pins. All match exactly, with the native adapter correctly taking the separately reviewed Root successor hash. Read both CORE-INTEGRATION and ROOT-INTEGRATION JSON records; the former's older head and “Root consumer not integrated” describe its earlier six-path operation, while the successor records the later completed consumer integration. No code dependency on dated AgentRuns, the run ID or private scratch paths was found in those 12 files.

The maintained `validation/FILE_ACT_INTEGRATION/source.json` hash is `83c0a12f7906cbd53ff280eb5b55975e01a5f005958665250e6dae7577dd4b7a` and its 12 entries match current reviewed bytes. Independently verified both log hashes against metadata: actual maintained Rust output reports 22 passed/0 failed/1 ignored plus four executed one-test FIFO workers; frontend reports `tsc --noEmit && vite build` success. These are inspected manager executions; this preservation check reran no tests or compiler and does not claim a new correctness proof.

README SHA-256 `18c756aadf5ca54fdb91126ce28b9f060d5573efe50d48af0e3454c5bef0dfaf` describes implemented A4/A6/A7 standing controls, separate reader, original continuation and workflow integration within their established source warrants. It expressly distinguishes synthetic checks from actual person/native registration, provider uptake and workflow completion; retains general file/arrival surface, lapse-history, cold trust and native witness limits. Its run citations are documentation context, not product source dependencies. The graph's I3-FILE-ACTS row agrees with bounded integration and outstanding obligations. No unintended product change appears in the reviewed 12-path set. Earlier READY scope and all native/acceptance limitations remain unchanged. Sole write is this appended review; no resources or processes acquired or held.
