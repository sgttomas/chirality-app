# Independent P2/P3 candidate review

Reviewer: Codex TASK `/root/distribution_integration_manager/bundle_review`, harness-native child of WORKING_ITEMS `/root/distribution_integration_manager`; no delegation. Isolated branch `codex/app-v4-bundle-inputs-review`. Review-only contribution, no product edits.

Reviewed integration head: `189cda6d908f50c3685e7d13be7188055429aede`. Read-only delta backcheck found only manager evidence/graph updates and separately owned Group B runner support/records; P2/P3 Rust, UI, assets, Design and source pins are unchanged. No additional affected code checks required.

Frozen code: `80560dd60f0d5870aa0b3a132ab6623b99857ff3`.

**Suitable for bounded candidate-input fan-in. No unresolved blocking findings.** This verdict covers P2/P3 assets, catalog and real inspection/refusal paths, role-set conversation-start gate, native command/UI joins and the proposed CC-WR-PKG-CANDIDATE-01. It does not cover unrelated Group B changes included through main, qualify a package, accept the proposal or establish runnable LS-5/LS-8 standing.

## Findings and repair

One confirmed blocking read-safety defect was reported against 0bd3ade5ee: a FIFO at MANIFEST.json could block ordinary fs::read indefinitely. The producer repaired the manifest and shared ledger reader. At the frozen code both use the regular-file helper: preflight rejects known special files, O_NOFOLLOW/O_NONBLOCK prevents final-component link following or blocking replacement, and descriptor metadata governs regular-file type before reading. Both FIFO tests exercise initial and retained-selection refusal. Finding resolved by source review plus producer regression evidence. This is not a claim of general hostile ancestor-race hardening; existing ancestor checks remain.

## Evidence and conclusions

- Independent byte comparison against Git object 015f9763ead9294b3857038e5d9cbaf2f9816244 passed: both P2 files exactly match their Root sources and manifest sizes/digests; P3 role/guidance digests and all four pinned source bindings match. No development fixture was promoted and original guidance/SOURCE_MAP are unchanged by this scope.
- Closed catalog validates name, full file set, revision method, package content, exact build subject, empty history and no-v3 selection. Physical bundle resolution checks its manifest/package; held-copy resolution checks actual ledger, vacant slot and orphan store, then rechecks at use. Candidate identity remains explicitly candidate; there is no shipping-history evidence.
- Actual Root selection commands are reachable from UI. Candidate inspection preserves truthful non-runnable status. run_admission refuses before preparation/records/send; connected tests cover bundle and held-copy refusal and mutation. Existing actual registered revision route remains distinct.
- Actual thread_start calls prepare_role_entry before claim/history/send. Production mode resolves resource_dir/instructions and compares roles, all guidance and binding with compiled bytes. Development mode is explicit via tauri::is_dev and custom-protocol; production failure has no fallback. Every role choice, including none, traverses validation. Exact role-set identity is preserved in composition/start records/status; edited user guidance remains editable and separately identified.
- ROLE4.1 permits zero defaults. UI obtains exact asset metadata, initializes its all-false default and permits clearing. U-R6/U-R11 remain open. No native child supply, enforcement or supplier adoption is inferred.
- WR does not explicitly require public distribution, but does not explicitly confer registration on a self-described candidate either. CC-WR-PKG-CANDIDATE-01 appropriately remains a proposal with joined authority/consumer adoption outstanding; conservative refusal is correct for this delivered scope.

Verification custody: reviewer independently performed source/Git byte and binding checks and reviewed implementation, caller paths, tests and repair. Producer reports 96 workflow-workspace and 3 connected candidate tests passed after repair. Manager reports final-code80560dd joined workflow_ suite 156 passed, P3 development and custom-protocol suites 8 each passed, TypeScript/Vite checks passed and Node 6 passed with 1 supplier skip. These executions are their evidence, not reviewer reruns. No downloads, native launch, supplier execution, credentials, owner acts or MEMORY writes occurred in this review.

Remaining work: parent retains actual-head evidence-only backcheck and PR/CI integration. Group B retains physical packaging/qualification and examination. Candidate workflow run admission requires separate reviewed adoption or genuine existing A15 registration; LS-5/LS-8 actual release registration/history remains absent. These are explicit receiving boundaries, not satisfied by this review.
