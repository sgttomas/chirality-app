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

The next actual artifact is one isolated unsigned release-profile App with a
complete inventory/resource comparison. Actual build source, toolchain, SDK
placement and package evidence must be observed on that artifact. The input-test
plan is not relabelled as the later source or a qualified package.

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
