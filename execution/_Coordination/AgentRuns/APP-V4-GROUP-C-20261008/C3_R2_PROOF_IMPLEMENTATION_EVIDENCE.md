# R2-PROOF-01-B2 implementation candidate

Author-tested dormant proof; independent exact-code review remains required. This is not an App recovery feature, production policy, native/actor qualification or PM05/90% closure.

## Exact basis and reachability

Parent explicitly released brief8ca467cb40b16ec9e7209ada85cee9e32e29cf8b, SHA25644421a4cffe1ec5ac47eb1cd4b7b15a2aabde27ca1169cff5532159e7bf53717, after independent READY and storage B2 CONCUR. The exact brief/basis, selected21case source, original storage concurrence, retained B1 bootstrap finding, B2 backcheck and code release were read from the manager's supplied worktree. Their actual byte hashes and origins are in the accompanying basis. Source headers retaining earlier PROPOSED status are historical; release comes from the explicit parent direction.

The existing isolated author worktree received current mainf028d12edcd23c8aaf6a1b67e6efc66a3cfda19b. Only private src/r2_snapshot_proof.rs and dedicated tests/r2_snapshot_proof.rs implement code. The test entry includes the private module by path; the module is also cfg(test) and macOS/Linux gated. No lib.rs declaration, command, opener, startup hook, feature/environment activation, Cargo dependency, schema, Host/AA-CAP allocator, role/WR/RS, CRP/CAM, graph or actual journal path was changed. Unsupported OSes have no compiled proof module, not a runtime fallback. No App was launched to test this static reachability boundary.

## Mechanism and state meaning

Closed typed test-1 structs serialize compact JSON in declared serde field order with no newline. SHA256 binds actual original bytes, not a cross-library canonicalization claim. Control, immutable admission, descriptor and snapshot identities/policy/revision/predecessor are checked. All payloads are inert constructed/recorded data. Required artifacts embed exact text/length/hash; successor checks preserve prior required IDs, same-ID bytes and unresolved attempts. Existing full constructed0.4 fixture bytes, answer/review text, injected intent/unknown outcome and injected definite account-reference facts survive a third commit and old-slot reuse without actual CRP or supplier operations.

The full-buffer structural scanner allocates nothing and counts each colon outside strings, including the first member. It enforces depth16/members512 before typed parsing. Typed deny_unknown_fields and bounded sequence seeds refuse duplicate/unknown fields, item33/item65 before decoding that next item, malformed/trailing JSON, invalid UTF8/numbers and overflow. IDs/text are checked as decoded UTF8 bytes. Decoding can temporarily allocate from the already bounded raw input; no pre-allocation per-string guarantee is claimed.

Explicit TestBudget values are N2/S32768/D4096/T0/Q262144 with the named subordinate ceilings. There is no Default or deserialization into a production policy, and no initializer lacking an explicit TestBudget argument. Zero/overflow/inconsistent values refuse. Logical reservation is checked N*(2*S+3*D)+2*D=163840; actual known-file sizes and entries are checked under the same lock. Admission reserves four upcoming entries and descriptor staging one before mutation; a low entry ceiling cannot be exceeded by the core then noticed only afterwards. Unknown/orphan/ambiguous entries block accounting, never supply free quota. No terminal/cancel retirement or ID reuse exists.

Every child openat uses O_NOFOLLOW/O_CLOEXEC/O_NONBLOCK before regular/single-link fstat checks; directory opens additionally require O_DIRECTORY without a directory nlink1 requirement. This avoids ordinary FIFO open waiting before type refusal. Device-specific and hostile same-user behavior is not qualified. Root final symlinks refuse. Stable lock creation is exclusive; independently opened reader/writer sessions acquire exclusive nonblocking flock and report Busy. No duplicated lock fd, stale-PID override or upgrade is used.

Bootstrap and admission have named before/after cuts around exclusive creation, file/parent sync, strict readback and acknowledgment. Pre-mutation refusal has no attempt. After a mutation attempt, IncompleteOrUncertain bootstrap/admission retains an attempt and bounded observed entry names; incomplete state blocks or remains occupied, with no initialization fallback. New test-only confirm-existing resynchronizes a complete observed set, compares identities/metadata and does not reconstruct an old acknowledgment. Known occupied admissions and a live blocked failure are not erased by that step.

Commit reads only the descriptor-selected old snapshot for validation, then drops that transient old validation value before streaming the borrowed new candidate to the inactive file. It syncs/readbacks bounded bytes, creates one exclusive descriptor.tmp, streams/syncs it, rechecks old descriptor hash and identity, admission/root/lock/inactive identities, atomically replaces, syncs the directory and reads back the exact selected pair before confirmation. Before replacement attempt, failures are NotCommitted for the new revision; after attempt they are Uncertain. Actual leftovers/attempts remain, no retry/rollback/unlink occurs, and old active bytes are not selected by timestamp or newest revision. Fresh reopen returns SelectedStateObserved with acknowledgment/freshness limitations; coherent rollback remains unprovable without an external anchor.

## Actual checks and measured allocation account

The author requested the serial Rust window before any Rust build. Host held its builds; all commands reused the same owned private target and approved offline Cargo cache with CARGO_NET_OFFLINE=true, CARGO_INCREMENTAL=0 and CHIRALITY_SKIP_CODEX=1. No new target, download, native/supplier/child-process helper or other-session cleanup occurred. Test teardown removes only each exclusively created owned temporary fixture root after observations. Existing artifacts, App-data and capture locks were untouched.

Initial candidate7e110557 commands, all offline/locked (subsequent independent repair below):

- cargo test --test r2_snapshot_proof -- --nocapture:30 passed.
- Same focused integration binary with --features distribution-successor:30 passed.
- cargo check --lib --features distribution-successor:passed with the existing production-library warnings. The proof is absent from that non-test library graph.

The30 test functions cover all21 selected case families, B2 bootstrap/admission cuts, actual duplicate keys in all four record types, exact first-member1 and512/513 structural counts, escaped punctuation, before-item33/65 sequence bounds, and additional observed-identity/entry-reservation regressions. The case mapping names exact maintained tests; NO_ACTIVATION uses source reachability and non-test compilation, not native startup. No missing-policy runtime default is available by type; zero/overflow policies are executed refusals.

A separate System-backed test allocator is enabled only for the measured test thread; cumulative allocation requests never subtract frees during an operation, and retained input/handle capacities are added. No allocator warm-up hides required parser/hash work. Streaming serialization avoids a second serialized new-payload cache. The measured boundary fixture has exact S32768 bytes,32 artifacts,64 unresolved attempts and64 gaps under N2 policy; temporary raw/parsed validation and borrowed new-candidate ownership are counted. It is one current working candidate, not independent editable old/new working sets. Measurements are upper bounds for these counted heap operations, not equality to live peak, OS/RSS, physical blocks or a universal workload theorem. Native C directory/OS buffers are outside this Rust allocator meter.

| Operation | Retained capacities + cumulative requested bytes |
|---|---:|
| Bootstrap | 5460 |
| Admission | 100116 |
| Exact-S first commit | 294788 |
| Exact-S successor commit | 413909 |
| Independent cold open | 9425 |
| Exact-S selected read | 129925 |
| Cold confirm-existing | 260152 |

Both feature configurations produced these values, all below1MiB. No physical power-loss/F_FULLFSYNC assurance, cross-process flock qualification, universal device behavior, rollback freshness, hostile replace/restore exclusion, product capacity/retirement or actual authorship follows.

## First results and repairs retained

The first implementation run passed24 tests. Static audit then produced four concrete maintained regressions, all failing before repair: root aliases were followed; confirm-existing forgot known occupied admissions; byte-identical descriptor and admission inode substitutions were accepted. Repairs reject root symlinks, retain occupied/live-failure knowledge, bind admission receipts to directory/file identity and raw hash, compare old descriptor identity as well as bytes, and verify postreplacement descriptor/snapshot identities. A resync substitution case also verifies file identity/metadata across confirmation. The repaired28-test run passed, then the expanded29-test runs passed with the full0.4 artifact and final boundary measurements.

A final independent-entry-budget audit reproduced a real failure: entries5 admitted a six-entry initial journal. Preflight reservations now reject admission/staging before mutation at5/6, first commit fits7 and successor staging requires8. One scripted edit stopped before writing due to a formatting assertion; its subsequent unchanged-code run correctly still failed29pass/1fail and is not presented as a repaired result. After the actual repair, final30/30 passed in both configurations. Original first-pass, four-failure, entry-failure and final logs remain locally hashed in the basis.

The source's original B1 missing-bootstrap-protocol finding remains separately retained; source B2 concurrence does not stand in for code review. Rust work is now quiescent and the build window was explicitly released. Final observed free space2.8GiB; no cleanup was performed to manufacture capacity. Independent review must assess these exact code bytes and limitations before integration.

## Maintainability and reuse standing

This is a private proof implementation, not a proposed reusable production journal. Its size includes the closed codec, actual bootstrap/admission/commit/read protocols, named fault boundaries and a dedicated allocator/test harness. The independent review should assess whether a simpler equivalent proves the same obligations and whether any part should later be reused or retired. No production reuse, activation or shared-helper extraction is claimed or selected here. The original failing WIP was not separately committed/hashed; exact failure logs and the applied identity-repair recipe are retained and hashed, while final source hashes identify the reviewable candidate. No unnecessary full historical source copies were created.

## Independent P2 final-admission repair

Independent static review of frozen7e1105579cfff5c22d12177cc64964184fb34c3f identified a missing final immutable-admission guard. SelectionRecheck checked admission identity/hash, but CommitReadback compared the selected pair to a cached Admission. Two maintained tests were added before changing the core: substitute admission with byte-identical, mode-identical bytes on a new inode at CommitDirectorySync After or CommitReadback Before. Both reproduced the defect:0passed/2failed, each returning Confirmed revision2. The exact frozen core hash, red-test source/patch and log hashes were retained before repair; small patches preserve the red test and code delta without full source copies.

The minimal repair calls the existing check_admission after exact selected-pair readback and before acknowledgment. Observed substitution now returns Uncertain with the original revision2 Attempt. The tests verify no rollback/unlink, refusal of another commit through the blocked live state, and that a fresh reader may observe selected revision2 only with original acknowledgment unavailable. This does not eliminate a later unobserved hostile replace/restore race or create a stronger continuous-path guarantee.

Affected default and distribution-successor focused suites each passed32/32. The additional bounded admission read raises measured first-commit upper bound to298969 and successor upper bound to418090 bytes; other rows above are unchanged, and both configurations match. The prior non-test library check remains applicable because the production module graph, lib.rs and Cargo configuration did not change. This repair stays proof-only and introduces no production reuse, activation, policy or native act. The serial Rust window was explicitly released after checks; last observed free space3.0GiB. Independent exact repair backcheck remains required.
