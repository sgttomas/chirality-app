# Committed synthetic exports

Source: `938d20ef4bf0d07a7cc706d575e74f844d8caccf`; clean `/private/tmp/hosting-secondary-manager` before and after. Default offline Rust test harness freshly compiled from that checkout in the existing shared target. No maintained files changed.

Harness: `/private/tmp/hosting-s2-target/debug/deps/chirality_app_v4_lib-007aa6e39be0839b`
SHA-256: `69d418bb91d6734f3da46812982e6a858369839aeed4532ff86299038abb8bea`

Both unchanged export helpers passed one explicitly ignored test each, producing selected and unselected cases. LT09 v1 and terminal LT09+LT23 v1 only; no LT12 exchange or qualification claim. Explicit invented application candidate inputs remain unchanged.

Exact invocation arrays, environment output roots, executable identity and all output member hashes are in the separate lt09-receipt.json and terminal-receipt.json. Both used this same executable unchanged. Build command: `cargo test --offline --lib --no-run --message-format=json`, with CARGO_HOME=/Users/ryan/Library/Caches/chirality-dev/cargo-home-group-a, CARGO_TARGET_DIR=/private/tmp/hosting-s2-target, CARGO_INCREMENTAL=0 and CHIRALITY_SKIP_CODEX=1.

SOURCE_MEMBERS.json binds all maintained src and successor-resource files to exact commit bytes. VERIFICATION.json records the four marker digests and successful raw member-set/hash/size correspondence, absent unselected source directory, and same-H5 terminal events. Build and invocation logs are retained here. Source files embedded in the terminal helper were additionally checked by its clean-source gate.

No source/API/format edit, new checkout/target, actual supplier/App launch, downloads, credentials, S3, SEAL2 or restored authority. Shared target released after exports and verification.
