# AA-CAP protocol-class repair R1

Frozen staged/uncommitted in `/private/tmp/aa-cap-core`, branch codex/app-v4-aa-cap-core, basis7c8c2190e70333e8d3f9b131aee708d493f15b63. Exact four-file manifest and staged patch are alongside this return. No commit/PR/export/B pin change. Existing target is released; no build/test remains active.

Independent original red retained verbatim: server_request_negative.rs supplied original response plus item/completed(id999) and turn/completed(id998); old core incorrectly reached ConsistentThroughReceipt(3,3), and the assertion failed with exit101. Copies here are original-server-request-vector.rs and original-red.log; original exact-core/source packet remains with reviewer and `/private/tmp/aa-cap-evidence/`. Do not relabel the earlier17-test passes as coverage of this defect.

Repair follows existing Host envelope classification before accepting core facts: object/no observation marker; notifications have no id; responses have id and result/error without method. Matching original RPC ID is insufficient when Host calls the frame a server request or malformed. The ordinary Host classification/reply/journal path is unchanged, and later actual uncorrelated response envelopes still reach the core. No full native-schema validation was added. hosting.rs bytes are unchanged from initial AA-CAP freeze; only the new core, its tests and support clarification changed in this repair.

Final same-byte matrix:

* default-r3.log:20 passed,0 failed.
* production.log:20 passed,0 failed with distribution-successor,custom-protocol.

Both commands are filtered `cargo test --offline --manifest-path projects/chirality-app-v4/app/src-tauri/Cargo.toml --lib [--features distribution-successor,custom-protocol] aa_cap -- --test-threads=1 --nocapture`, same existing target/private cache, incremental0, skip supplier1. No process/native/supplier/group actions. Original actual-pipe and explicitly simulated-settlement distinctions remain unchanged. Budget measurements still show1944 inline,52224 fixed sort-reference scratch and0 measured heap allocation for tested PF1/bind cases.

Three maintained controls were added: item-id-only/terminal-id-only/both cases with paired actual mandatory error replies and identical ordinary records/journal; observation markers on response/item/terminal remain malformed and cannot supply facts; matching original RPC ID with method or bare ID still cannot act as a response, while a later genuine response and notifications can complete provisionally. The marker/response-envelope refinement is the same released protocol-class blocker, confirmed by manager, not a schema expansion.

Intermediate default.log18-pass and default-final.log19-pass results are retained separately; final default-r3/production20 cover the complete repaired bytes. No repaired-run test failure occurred. Official staged private check4files/3terms/0 findings and staged diff check pass.

Independent unchanged-vector backcheck remains required before fan-in. Parent Group B option B keeps current-source S4 positives held and historical cohorts intact; no repin/export is implied. Dormant-only/no production constructor, limited native-schema standing and no attribution/mint/role/account authority remain the boundary.
