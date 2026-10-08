# Reviewed committed-source export renewal

Exact source `127d48f61d91b70d00d0670d2150c79b8ac26d1f` in clean `/private/tmp/hosting-secondary-manager`. Fresh default offline compilation finished in14.37s. No maintained files changed; all earlier cohorts preserved.

Harness `/private/tmp/hosting-s2-target/debug/deps/chirality_app_v4_lib-007aa6e39be0839b`
SHA256 `90f76ee159433fd4b41439b38e5ec40badd3709e39ef3030d03673f2690d3feb`. Both unchanged ignored export helpers passed1 test each from this SAME executable, selected and unselected cases. Formats only LT09v1 and LT09+LT23terminalv1; no LT20 or new format claim. Explicit invented App candidate fields unchanged.

All89 declared raw artifact members (93 exported files including four exchange markers) across four cases verified against exact path sets, hashes and sizes, including selected-source originals. Unselected source directory absent; terminal actualLT09/LT23 share fullH5. Source src and successor resources byte-equal exactcommit in SOURCE_MEMBERS.json. Separate lt09-receipt.json and terminal-receipt.json retain exact executable/source/argv/env and every exported file digest. VERIFICATION.json retains marker hashes.

Build command cargo test --offline --lib --no-run --message-format=json with CARGO_HOME=/Users/ryan/Library/Caches/chirality-dev/cargo-home-group-a, CARGO_TARGET_DIR=/private/tmp/hosting-s2-target, CARGO_INCREMENTAL=0, CHIRALITY_SKIP_CODEX=1. Logs and invocation scripts retained. No new checkout/target, supplier/native App, download, credentials, S3/SEAL2 or qualification claim. Disk10GiB before build. Target released after both helpers and verification.

Verification bookkeeping: initial count assertion incorrectly treated93 total export files as93 declared artifact members; it observed89 and stopped. Corrected distinction89 artifact members+4 markers=93 total. Exports were neither rewritten nor rerun; all byte/digest checks passed before and after. This was a verifier counting assumption, not an export failure.
