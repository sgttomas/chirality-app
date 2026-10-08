# C3-P independent persistence review

Reviewer: harness-native TASK `/root/group_c_successor/cfb_design_review`, under WORKING_ITEMS `/root/group_c_successor`; no descendants. Review method: project `software-code-review` skill, origin and instruction basis retained in C3_DESIGN_REVIEW.md. Exact author candidate `e660d7431de637da7e8dbe9d9bddc0c6847838c8` versus `fbf16537a2502f15bc1a0a8ae07ce508e9bdbbe7`; independent compilation/tests used combined candidate `03cfa1e77dc542ce356ab5eaa071620bdd50195b` on receiving base `ce2d7adaed`.

**NOT READY: one blocking correctness finding, reproduced independently.** This is a code review, not product acceptance or a source-contract amendment.

## F1 — Temporary pathname substitution can publish foreign bytes and delete an unowned entry (blocking)

Location: `app/src-tauri/src/connector_route_store.rs`, publication lines 481–504 and error cleanup lines 527–539. The temporary file is created exclusively and its descriptor retained, but `linkat` publishes by the mutable temporary pathname. Both success and error cleanup call `unlinkat` on that pathname without binding deletion to the original file identity.

Trigger reproduced through the existing `TempSynced` hook: rename the writer's temporary aside and create an unrelated entry at its former name. If the hook returns an error, cleanup deletes that replacement even though this attempt never created it. If the hook continues, the writer links foreign schema-valid account bytes into the canonical final account name; readback subsequently detects the mismatch and returns uncertainty, but the foreign publication and temporary deletion have already occurred. This violates CRP §3's publication of the prepared bytes and removal of only the attempt's own temporary. Later detection does not repair those effects.

Required repair direction: bind publication and cleanup to owned file identity using supported primitives/ownership arrangements, and refuse on substitution without deleting the replacement. Retain regressions for both observed cases. A path identity check followed by unprotected unlink/publication does not eliminate the final-check race; if the supported host cannot provide the intended ownership guarantee, return the exact capability limit for named source treatment instead of silently narrowing the contract. No specific unverified primitive is prescribed by this review.

## Independent verification and scope

Inspected all eight changed paths, including complete production code and tests, exact embedded schemas, registration and evidence/basis. Compared the author's diff to the integrated candidate: all seven non-registration files are byte-identical; registration is the one module declaration against the new base. Three embedded resource files equal their maintained Design bytes. Both author and combined diff checks passed. Existing validator compilation denies retrieval and selects exact declared schema versions.

The manager explicitly extended the review write boundary for an isolated disposable test harness only. Candidate and repository source were not edited. One private copy-on-write build-target clone and a Git-exported combined source were used; no full target copies, other workers' writes or deletions. Added two independent tests only to the disposable harness, using existing `write_inner` stage hooks. Offline Cargo compilation used the prepared approved cache with supplier launch disabled. The first harness build lacked three unchanged compile-time test resources; those exact candidate resources were exported and the build repeated. An initial guessed cache path could not resolve jsonschema offline; the manager supplied the approved existing cache. No download occurred.

Command: `cargo test --offline --locked connector_ --lib -- --nocapture`.
Result: **25 existing checks passed; 2 added independent safety checks failed**. The original two abrupt-exit child witnesses also ran. Independent failed checks:

- `independent_cleanup_must_not_delete_substituted_temporary`: asserts the unrelated replacement remains after a definite prepublication failure; observed deleted.
- `independent_publication_must_not_publish_substituted_temporary`: asserts foreign bytes are not the published final account; observed exact foreign bytes published, followed by uncertain-commit error.

Reproduction algorithm is fully stated in F1; scratch harness source and log were returned directly to manager/author for retained regressions. These failures are against the existing contract, not newly relaxed or substituted criteria.

## Other reviewed behavior and qualification limits

No additional actionable findings in the examined version dispatch, directory-relative child operations, retained directory identities, selected rename residual, no-replace destination collision handling, post-write readback, cold duplicate/version/error visibility or reference checking. Passing operation-boundary injections are not actual fsync-error or mid-stream readdir-error observations. Error branches preserve uncertainty after possible publication; those platform failure paths remain unexercised. Successful sync calls and abrupt process exits do not prove physical power-loss durability. Linux was not run; unsupported platforms refuse. These declared limits are truthful and cannot be converted into qualification claims.

Actual source recovery, semantic/reference truth, actor performance, UI presentation, provider joins and consumer adoption remain outside this persistence seam. The review does not weaken CRP-v0.2 or authorize native/supplier/credential/person acts. SEAL-2 remains held. Repair and affected exact-candidate review are required before integration.

## Exact inspected source identities

Hashes identify entire files; inherited Root/TASK/loop/manual/skill reading identity remains recorded in C3_DESIGN_REVIEW.md. Production and test files below were read in full; unchanged schema semantics were traced through the already-reviewed source definitions and exact byte comparisons.

| File | SHA-256 |
|---|---|
| `projects/chirality-app-v4/app/src-tauri/src/connector_route_store.rs` | `d2a90218452a815e982b5851fc257e70db3f830f0ab013cfce3457cc7921187b` |
| `projects/chirality-app-v4/app/src-tauri/src/connector_route_store_tests.rs` | `d760aaf09eb526de1cd6fd02b5c7797c4befc0511a9c43e6a93cf50eafc1cfae` |
| `projects/chirality-app-v4/app/src-tauri/src/schema_validation.rs` | `42545d9d544f0a8ac7be84814bc9285d987888e6c7ef2ca0201041458c2eb3a9` |
| `projects/chirality-app-v4/app/src-tauri/src/lib.rs` | `a1e09192b6aba1641e49d518ba3553914705220a4d8d6a5c4883596a5376b315` |
| `projects/chirality-app-v4/app/src-tauri/resources/connector_route/connector.route-account.schema.json` | `a6823eebb2872d0d563b7e77589a0cc2f7cd2545abe654e5b427af7d79365286` |
| `projects/chirality-app-v4/app/src-tauri/resources/connector_route/connector.route-account.v0.2.schema.json` | `4b82115a5d280fd4059925f1f5e50c20cc726be2d3266caf8b68873ad1c665d4` |
| `projects/chirality-app-v4/app/src-tauri/resources/connector_route/connector.standing.schema.json` | `bf4cef4df1ef16bc4a2a8e8fbb341798a90a48abbbe3689d68d5ce9019650719` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-C-20261008/C3_PERSISTENCE_BASIS.json` | `b55636e7f95414f06ba07dc878c2fa9a43b476f27f16d703b304a5292fdc3026` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-C-20261008/C3_PERSISTENCE_EVIDENCE.md` | `b20a4405fab790a87a406dc63517d6d07fcd62962c700106b2c122d5f9854dd3` |

## CRP-R2 repaired implementation and combined-candidate backcheck

Exact repair author: `8f1195761d6f88dcb4c52b9d4ba9215aa0d60cd4`; exact integrated candidate: `f1ff1699e094bb526dcef6f7a3dc47f002da837a`, reviewed against receiving main `00ce2e1074`. **READY for bounded persistence integration under adopted CRP-v0.3. F1 is resolved against that expressly revised contract.** The original NOT READY assessment above remains true for its original candidate. The new result does not claim the old unconditional publication guarantee was implemented.

Inspected the complete 16-path combined contribution, including unchanged schema copies, registration, the complete production/maintained-test repair, source successor, amended fleet concurrence, technical adoption, graph and author evidence/basis. Exact CRP-v0.3 remains `e52f5ed0b9c3be99a50a834101470ecfc67078aab0e5dc90e9bc201706a6598e`; source selection and affected concurrence bind those bytes. The four integrated repair files are byte-identical to the author revision. Tested-output hashes were checked against the author revision, successor-source hashes against their declared revisions; combined diff check passed. The one module registration preserves receiving-main changes.

The repair removes automatic unlink entirely and replaces link publication with exclusive no-replace rename. An observed substituted temporary now refuses before publication, leaves the foreign replacement and original moved-aside bytes intact, and records the recovery name. No error or success cleanup can delete a reappearing entry at that name. Before successful binding, the retained original inode and intended content/version/ID are checked; the directory sync and identity comparison remain. Unsupported operation refuses without weaker fallback; ambiguous outcomes preserve intended and observed/absent/unreadable details for reconciliation.

The AFTER-final-precheck source-name race is deliberately retained by the reviewed successor. A foreign entry can move to final, but original-inode comparison rejects success even for identical bytes. The writer neither rolls back nor retries, and later discovery does not establish successful publication. This is an explicit change in the source guarantee, separately reviewed/adopted, not an assertion that checks exclude all races.

### Independent execution and finding backcheck

Reused the same private copy-on-write target; exported exact combined candidate sources into the disposable harness and added three independent tests. Production/repository source remained unchanged. Offline command and supplier-disabled cache settings were those of the original independent run. Result: **34 passed, 0 failed: 31 maintained checks plus 3 independent checks**; the two deliberate abrupt-exit child witnesses also ran. No downloads, supplier/native App launch or extra target copy.

- Original cleanup sequence repeated: at `TempSynced`, rename the owned temporary aside, write an unrelated replacement under its name, then inject failure. The replacement bytes survive, no final file exists, and the outcome is definite failure. This directly reverses the originally observed deletion.
- Original publication sequence repeated: the same substitution at `TempSynced`, followed by continuation. It now returns ChangedContent before attempting publication; the foreign entry survives and no final file exists. The original harness previously read final bytes to demonstrate the bug; this backcheck asserts the stronger corrected outcome, no final target at all, rather than requiring a target to exist merely to compare it.
- Independent late identical-byte/new-inode sequence: substitute at `TempChecked`, after the final check. Exclusive rename moves those bytes to final; the call returns uncertain ChangedContent, original and observed file identities differ, intended reconciliation fails, original moved-aside bytes survive, and the directory has exactly one final record with no retry. This tests the successor's disclosed residual, not the superseded stronger criterion.

Maintained tests additionally exercise late foreign accounts, symlink and directory entries, identical-byte inodes, existing destination collisions, same-name reappearance after successful rename, actual syscall invalid-flag refusal and injected ambiguous EIO. All passed through the integrated code. The invalid-flag test is not a separately mounted unsupported filesystem; injected EIO is not device failure. Physical power loss, actual fsync failure, induced midstream readdir failure and Linux execution remain unperformed, as the author reports. No durability qualification beyond the observed calls is inferred.

No remaining actionable findings in this bounded reviewed contribution. The selected directory/source-name residuals remain. Full source reconstruction, UI, consumer adoption, provider work, qualification, release and Group C completion are not established. Manager graph/readiness updates and required CI must bind the actual integration head; a later content change requires an affected backcheck.

### Repaired code identities

- `projects/chirality-app-v4/app/src-tauri/src/connector_route_store.rs`: `ace6a925fe32d49754f3a7fbd30eebf1bf144292ef2104e48a9886663b99f160`.
- `projects/chirality-app-v4/app/src-tauri/src/connector_route_store_tests.rs`: `4ec5ceb945f01f89ecdc5ae778a3a443824521c4131f90a636ca51bf76636334`.
