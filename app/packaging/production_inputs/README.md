# Unsigned release-build input preparation

This helper prepares configuration and an exact resource/input account; it does
not build, copy the supplier, sign, notarise, install, launch or read account state.
The current owner selection: on 2026-11-02 the owner kept
the existing production identifier `com.chirality.app` (same-ID), superseding the
earlier separate-v4 route, with macOS 15 minimum and package version 4.0.0. The
identifier/team enter through the closed publisher input file, which
`release/build.py` generates from the compiled keychain selection in
`app/src-tauri/src/capture_seal_keychain.rs` unless a file is supplied. These
choices do not select keychain service/account/group values, qualify OS support or
authorize signing. The historical publisher draft and native candidates are not
rewritten.

From repository root, with a disposable frozen source export (never a live Git
checkout), stable vendor tree in durable task storage, explicit expected vendor
manifest and a new output directory whose physical parent already exists:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 app/packaging/production_inputs/prepare.py \
  --source-root /absolute/selected/source \
  --revision <exact-40-hex-source-revision> \
  --vendor /absolute/selected/complete/vendor \
  --expected-manifest <exact-64-hex-vendor-manifest> --pin <selected-pin> \
  --test-identifier dev.chirality.app-v4.package-test.example \
  --output /absolute/new-private-scratch/plan
```

The test namespace is explicitly unqualified and never the production default.
This route clears publisher controls and preserves the compiled `None` gate.
It prepares a release-profile, `--no-sign`, custom-protocol/distribution-successor
build, not a synthetic runtime trust anchor or an installed-custody pass.

For a production plan, replace the test identifier argument with
`--publisher-input <file> --publisher-sha256 <digest>`. `release/build.py`
writes that file from the bundle identifier and team already published in
`app/src-tauri/src/capture_seal_keychain.rs`; the values hold no credential and
are not private. That file uses only the existing
closed publisher-build-selection.s1 shape (format, production identifier, team).
No requirement logic, certificate, key, password, notary or keychain-policy field
is accepted. The helper sets the exact effective identifier and build-only
production-v1 controls; source/build validation remains in the existing publisher
selector. It performs no signing.

In production mode only, `--provisioning-profile /private/profile.provisionprofile
--provisioning-profile-sha256 <exact-digest>` embeds the selected private Developer ID
profile at `Contents/embedded.provisionprofile` through `bundle.macOS.files`. The
helper requires the exact digest and parses the definite-length CMS SignedData
structure down to its single encapsulated `id-data` OCTET STRING. That content must be
exactly one XML property list with no duplicate keys, and the profile must be valid at
preparation time (recorded as `validity_checked_at`). It also checks that the
metadata matches the publisher input: the profile prefix plus the bundle
identifier equals the `com.apple.application-identifier` grant, team and platform
match, all devices are provisioned and no development grant is present. This is
structure and consistency only; the CMS signature and Apple authentication belong to the separate intake, and
actual placement is verified only by the post-build inventory. The profile stays
outside source, vendor and the repository.
Publisher input must be outside both source and vendor; vendor must be outside
source. Output/input separation checks filesystem device/inode ancestry, including
case aliases and macOS firmlinks. Private inputs cannot be bundled accidentally.
Test namespaces are refused in production mode.

Outputs, in a new private directory:

- `tauri.package-inputs.conf.json`: 4.0.0, minimum15.0, App-only target, signing
  identity null, existing P2/P3 + twelve attested-reference mappings + bounded
  direct notices + separate SQLite source-input resources + the IBM Plex font
  notice (`third-party-notices/fonts/`, refused if its index is stale) + complete vendor P1.
- `input-inventory.json`: exact selected resources/files/vendor hashes and modes,
  declared source revision, every loaded tool-module hash (four, or five with an
  upstream supplement) and jsonschema
  version, with limits. The source
  revision is a caller claim; actual export provenance is separately checked.
- `build-recipe.json`: argv array and allowlisted build inputs, explicit offline/
  jobs2/no-sign controls and current owner-selected host/cache/scratch admission. This is
  data, not a shell script or an automatic build runner. Use prepared tools/caches
  and a fresh scratch CODEX_HOME; never execute it by concatenating shell strings.
- `PLAN_COMPLETE.json`: written last, identifying the exact three plan files.
  The initial `INCOMPLETE.txt` remains on any interrupted/failed write. Before
  use, require `check_plan(output)` to pass (no incomplete marker and all completion
  hashes match), not merely the presence of config or recipe files.

Files are created exclusively with no-follow opens in a new private directory.
The mapped S2 selection's expected-reference and attestation bytes are digest-
checked, and vendor pin/manifest/full tree are compared with that expected
reference. Empty vendor/resource directories, glob source paths and colliding
resource destinations refuse instead of relying on surprising bundler behavior.

The emitted summary contains output paths/digests, not publisher values. Private
handling does not make the shipped identifier/team or compiled requirement secret.
Preserve exact private originals and separately identified redacted derivatives.
All old resource/source pins stay separate; mapping a closure does not adopt a
new pin, grant runtime authority or prove actual Tauri SDK/bundle inclusion.

## Explicit Cargo input for the measured macOS toolchain

`--cargo-build-input macos-arm64-rust-1.97.1-no-strip` adds an opt-in
`cargo_build_input` contract inside `build-recipe.json`; the completion marker
still binds the same three files. The default plan has no strip override. This
preset applies only to the measured arm64 host/target, macOS 27.2 / SDK 27.2,
Rust/Cargo 1.97.1 and exact compiler/linker binary digests in the contract. It
does not establish macOS 15 runtime qualification or apply to other toolchains.

The contract contains the exact UTF-8 Cargo config text and SHA-256
`82651ddc167d78065e4af475e439cd0c2fa0855b601f8fdda9a81ab263de42fc`:

```toml
[net]
offline = true
[build]
jobs = 2

[profile.release.build-override]
strip = "none"

[profile.release]
strip = "none"
```

The host build override covers build dependencies and proc-macros. The release
override also changes shipped target stripping; source release optimization
remains level 3. No bit-identical shipped-output claim follows. The measured
toolchain produced malformed LINKEDIT string-pool alignment with
`strip=debuginfo`: the host-only override allowed compilation but left the App
executable malformed. Both explicit overrides produced a candidate accepted by
Apple's static validator. This is a scoped workaround, not a diagnosis of every
possible compiler/linker defect.

Before a later authorized build, materialize `contract['text'].encode('utf-8')`
unchanged at the task-owned `CARGO_HOME/config.toml`, outside source and shared
caches. Do not overwrite another consumer's config. From the build driver call
`verify_cargo_build_input(plan, cargo_home, observed_scope, resolved_tool_paths)`
on this module. The scope keys are `host`, `target`, `macos`, `sdk`; resolved tool
paths must name `rustc`, `cargo`, `clang`, `ld`. The verifier reads and hashes
those files without executing them and refuses scope, tool or config mismatch.
The driver must establish the observed scope and use those same selected tools;
the helper cannot authenticate caller metadata or rule out other Cargo config
layers. Retain the empty allowlisted environment and confirm no source/ancestor
Cargo config adds overrides. Bind actual config/toolchain digests, original plan,
source and artifact together; the repository revision alone is not the recipe.
After building, require `dyld_info -validate_only` success on the actual main
executable and every actual bundled Mach-O as well as the normal resource,
profile and publisher static checks. A resource match cannot substitute for this.

## Actual input-test artifact and next production subject

One coordinated unsigned release-profile input-test App has been built from
exact `12d26b8db5f251be97d83d4f574196697df40a70` in a separate target/build directory.
Do not rebuild or mutate any retained native candidate or state. A default-None
input-test bundle can establish actual P1/P2/P3/notice/attested-resource placement
and release-profile build behavior without a publisher selection.
It cannot establish production publisher matching, installed S4 or signing.

Before invoking the recipe, the build owner binds the exact source export,
prepared dependency caches, private target and toolchain, and applies the current
owner-selected host controls. The present ordinary offline build direction does
not require a shared slot/guard; this helper grants no build authority. Fill every `required_environment` entry,
including a new absolute `CARGO_TARGET_DIR` outside all inputs, and start from an
empty environment, adding only listed allowlist entries. Do not inherit
TAURI_CONFIG, RUSTFLAGS, encoded Rust flags or signing variables. Tauri may set
its own child-build configuration from the explicitly selected overlay. The
planned deployment-target environment and overlay both select 15.0. The source
is disposable because frontend/SDK generation writes dist/gen output into it;
the target and caches remain separately located. Record the actual argv/environment overlay
hashes and build result. Inspect the complete resulting bundle and compare P1
against the exact source tree, P2/P3 against the selected source, and every mapped
notice/attested resource. Retain the build identity, executable and Info.plist
hashes. The existing candidate-identification/v3 producer is debug-only; do not
relabel a release build as that development profile. Its standalone bundle
inventory method can still supply raw inventory for the actual PKG identity.

## Signing, notarization and the package record

`app/packaging/release/` holds the runnable procedure:
[`build.py`](../release/build.py) builds the unsigned candidate from this
plan, [`owner_sign.py`](../release/owner_sign.py) is the owner's signing,
notarization and stapling run, and [`record.py`](../release/record.py) writes
and checks the package identity record. The owner's page is
[`release/README.md`](../release/README.md).

## Optional upstream notice supplement

Optional upstream notice inclusion uses `--upstream-notices` with a completed
`packaging/notices/receipts.py stage` directory. The helper validates exact
metadata/index/asset joins, adds only the public manifest and license resource,
and records them separately from archive-member notices. Default preparation
and `check_plan` remain unchanged. No actual receipt, applicability or completeness
is inferred from the invented tests.
