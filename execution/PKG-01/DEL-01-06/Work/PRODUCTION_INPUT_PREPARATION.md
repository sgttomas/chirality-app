# Unsigned release-profile input assembly

The parent-maintained CURRENT_EXECUTION_BASIS at integrated
`16f7b5a1f31e13a81332888efe99587b422f7543` records the owner's separate v4
identity route, minimum macOS 15 and package version 4.0.0. Exact identifier/team
remain a later private input. Historical drafts and native candidates keep their
original subjects; no signing, migration, OS qualification or release is inferred.

`app/packaging/production_inputs/prepare.py` implements OUT-001 CF-2/3/5 input
preparation: an explicit test namespace/default None or the existing closed
publisher input, exact resource mappings, vendor/reference correspondence,
isolated-build requirements and a digest-checked completion marker. It never
builds or signs. Its README contains the exact CLI, retained input-plan identities
and signing/installed-witness collection sequence using the existing packet formats.

Independent review found no blocker for initial plan-only use and identified
pre-build corrections. Those are implemented: device/inode ancestry separation
(including case/firmlink aliases), no publisher/vendor embedding in source,
mapped S2 reference/attestation plus full vendor equality, disposable source
export, explicit environment allowlist, exclusive private files and final
completion marker, complete tool identities, production/test namespace separation,
and refusal of empty/glob/colliding resource mappings. Sixteen source-fixture
tests pass. The corrected frozen-export/durable-vendor plan is retained at
`/Users/ryan/dev/chirality-t3/scratch/app-package-inputs-frozen-b42vohmf/plan`;
its fifty resource mappings and completion hashes were checked. No App was built.
The prior live-worktree plan at `app-package-inputs-wgel4r51` is historical only
and must not be executed. Preserve both input accounts and reviewer inputs.

An actual isolated unsigned release-profile App has now been built from exact
source `12d26b8db5f251be97d83d4f574196697df40a70`, tree
`a56efd947626ffb2fc15e2092631c6bcaee41036`. The preserved
[build and comparison evidence](unsigned-release-input-build/12d26b8db5-278899dad62e/build-observation.json)
binds bundle-tree v2
`278899dad62ebbc6dd701490f71b20bd04e1329bca4dbefbd5d88eecd83e31f0`
and App executable SHA-256
`1b3c6c2ec345845122322134cd6f9b59e60d32c78ef0795a5e2b4e5cf26796b8`.
All fifty mappings match: full P1/P2/P3 tree modes/bytes and 47 individually
mapped files. The complete Resources namespace has 101 files and 60 directories,
with no extras or omissions beyond the explicitly identified generated icon.
All mapped file modes match their source; 3,504 tracked export files match Git.
Info.plist is version 4.0.0/minimum 15.0, and the App's Mach-O declares 15.0.
This is a declaration/build observation, not a run on that minimum OS.

The bundle is retained at
`/Users/ryan/dev/chirality-t3/scratch/app-release-input-build-hmhzn4b2/target/release/bundle/macos/Chirality App v4 (package input test hmhzn4b2).app`.
It used one offline shared slot, jobs2, fresh target/home and copied prepared
dependencies; `--no-sign` explicitly skipped signing. Generated publisher
binding/projection are null and compiled values None. No App or supplier was
launched and no signature identity inspected. No v3 debug-only identification
record is fabricated for this release-profile artifact; the existing raw
bundle-tree method identifies it without a new receiving cohort. The earlier
input plan and native debug candidate retain their own source identities.
“Unsigned” here means no Developer ID/notarisation or owner signing act; any
incidental linker ad-hoc signature is unqualified compiler output, not a publisher
selection or installed-integrity witness.

The next production subject requires the actual owner identifier/team and
settled signer/keychain inputs, then a separately identified production build,
signing/notarisation and quarantined installed witness. This unsigned input-test
artifact is not relabelled as that subject or handed over as a qualified package.

Historical G-8/SIGN-3 discussion of proposed SEAL-2 entitlements does not adopt
SEAL-2. The required SEAL-C transition has separate runtime ownership and a
signing join under `SEAL_C_KEYCHAIN_SIGNING_JOIN.md` when integrated: receive the
exact compiled service/account/access-group, controlled first enrollment,
continuity behavior and actual entitlement/profile compatibility. Do not infer
empty entitlements, development-key migration, regeneration or exclusive-agent
protection. This contribution performs no real keychain or signing operation.

ScopeOfWork commitments and dependency conditions remain unchanged; code/tests
are registered in deliverable.yaml. Supplier notice/source gaps remain as stated
in CACHED_SHIPPED_NOTICE_INPUTS; SQLite source availability is not complete legal,
transitive or shipped coverage. No supplier pin or distribution decision changes.
