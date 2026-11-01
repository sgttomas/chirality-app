# Unsigned release-build input preparation

This helper prepares configuration and an exact resource/input account; it does
not build, copy the supplier, sign, notarise, install, launch or read account state.
The owner-selected basis is the parent-maintained
`execution/_Coordination/CURRENT_EXECUTION_BASIS.md`: separate v4 identity,
macOS 15 minimum and package version 4.0.0. These choices do not select an exact
production identifier/team or qualify OS support. The historical publisher draft
and native candidates are not rewritten.

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

After the parent obtains actual owner input privately, replace the test identifier
argument with `--publisher-input /private/selected.json --publisher-sha256
<independently-selected-exact-input-digest>`. That file uses only the existing
closed publisher-build-selection.s1 shape (format, production identifier, team).
No requirement logic, certificate, key, password, notary or keychain-policy field
is accepted. The helper sets the exact effective identifier and build-only
production-v1 controls; source/build validation remains in the existing publisher
selector. It performs no signing and does not authenticate the owner's selection.
Never put real values in command-line literals, chat or public logs.
Publisher input must be outside both source and vendor; vendor must be outside
source. Output/input separation checks filesystem device/inode ancestry, including
case aliases and macOS firmlinks. Private inputs cannot be bundled accidentally.
Test namespaces are refused in production mode.

Outputs, in a new private directory:

- `tauri.package-inputs.conf.json`: 4.0.0, minimum15.0, App-only target, signing
  identity null, existing P2/P3 + twelve attested-reference mappings + bounded
  direct notices + separate SQLite source-input resources + complete vendor P1.
- `input-inventory.json`: exact selected resources/files/vendor hashes and modes,
  declared source revision, all three loaded tool-module hashes and jsonschema
  version, with limits. The source
  revision is a caller claim; actual export provenance is separately checked.
- `build-recipe.json`: argv array and allowlisted build inputs, explicit offline/
  jobs2/no-sign controls and required host slot/cache/scratch admission. This is
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

## Actual input-test artifact and next production subject

One coordinated unsigned release-profile input-test App has been built from
exact `12d26b8db5f251be97d83d4f574196697df40a70` in a separate target/build directory;
the owning Work's `unsigned-release-input-build/12d26b8db5-278899dad62e/` retains
its actual source, command, inventory and complete resource comparison.
Do not rebuild or mutate any retained native candidate or state. A default-None
input-test bundle can establish actual P1/P2/P3/notice/attested-resource placement
and release-profile build behavior before private publisher values arrive.
It cannot establish production publisher matching, installed S4 or signing.

Before invoking the recipe, the build owner binds the exact source export,
prepared dependency caches, private target and toolchain, and admits one offline
slot under the shared host controls. Fill every `required_environment` entry,
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

## Signing and installed-witness intake — prepared, not authorised execution

1. Receive exact production identifier/team from the parent secure card, then
   build and retain the original publisher binding, public projection and
   requirement from the existing selector. Bind actual source/configuration,
   compiled selection, final executable and build identity. Ordinary test output
   or a default-None build is not a substitute.
2. The signer separately supplies CF-1's Developer ID Application certificate
   identity for the already selected team and the reviewed App entitlement/
   profile basis. No certificate private-key export or keychain enumeration is
   required from this lane. The approved SEAL-C transition adds an exact compiled
   service/account/access-group subject under a separate None gate: receive its
   typed selection/enrollment/cache/rotation contract and actual signing-side
   `application-identifier`/`keychain-access-groups` and profile compatibility.
   Do not guess a team-derived group or claim empty entitlements. Parent allocated
   this implementation to the runtime owner; no real keychain action is performed
   here. Keychain storage alone does not establish deferred SEAL-2 entry-seal,
   exclusive-agent or native-origin guarantees, or import development keys.
   The settled runtime interface uses separate compiled KEYCHAIN_SELECTION and
   explicit `allow_first_enrollment`; the host-only `enroll_initial(app_data)`
   operation is not startup, IPC, UI, seal, verify or rotate. Receive the actual
   controlled enrollment procedure before activation. Ordinary operations never
   provision or regenerate missing keys; no plan here calls enrollment or SecItem.
3. Retain FP-0 and P1 equality before signing. Under the owner's later signing
   direction, sign P-0 then the outer App using CF-4, never `--deep` for signing.
   Recompare the complete P1 tree for FP-1(b) and perform deep strict verification.
   Record exact entitlement/configuration bytes, signature facts/cdhash, actors
   and observations privately as needed. No pass is inferred from this recipe.
4. Construct/sign the DMG from that signed App, retain its pre-notary SHA,
   submit using the owner's separately managed notary profile, preserve the
   actual accepted/rejected log, staple and retain the separate post-staple SHA.
   Each rebuild changes the package subject. Nothing in the preparation authorises
   that submission, purchase, account act or publication.
5. For W-0…W-6, use an explicitly authorised quarantine transfer/attribute
   procedure and isolated installation subject: record installer quarantine,
   mounted App Gatekeeper result, installed App quarantine, first launch/version,
   actual S4 observation/custody and supplier ready handshake, installed signature/
   entitlements and cdhash. No conversation is needed. Missing quarantine is
   blocked; Gatekeeper refusal is failure. Native lifecycle/cleanup evidence is
   still a separate actual result; old synthetic cohorts are not installed proof.
6. Assemble the existing `static-package-input/2` plus distinct outer
   `packaged-s4-binding/1` request under one evidence root. Include approved terms
   closure, exact pre/post installer bytes, legacy+S1 package/full inventory and
   supplier selection/reference/attestation, S4 observation/custody/full generation,
   original/private publisher input/binding/requirement, public derivative,
   effective Tauri config and exact App source/build/version/id/executableSHA/cdhash.
   The receiver selects the trusted publisher binding digest independently; never
   take trust from the packet. Wrapper ID and inner package ID remain distinct.

```sh
python3 app/packaging/successor/check.py /private/packet/binding.json \
  --evidence-root /private/packet \
  --trusted-publisher-sha256 <from-independent-receiving-configuration>
```

The explicit EXP/SQ package-witness adapter consumes the same request with its
separately pinned receiving configuration. It retains errors/gaps and nonauthority
flags; do not create another cohort or convert a consistency result into release.

## Precise remaining inputs

- Owner: exact production identifier and Developer ID team (parent's private card).
- Signing stage: CF-1 certificate identity/owner signing act, actual notary profile
  and the settled SEAL-C access-group/service/account plus entitlement/profile
  compatibility. Private keys/passwords do not enter this preparation.
- Supplier/component evidence: exact source/notice associations for the retained
  Codex main, code-mode-host, rg and zsh hashes in CACHED_SHIPPED_NOTICE_INPUTS.md.
  The cached tree has voice notices and archive-level metadata, not those missing
  associations. SQLite's exact source input is now prepared separately. No legal
  approval, transitive completeness or scope waiver follows. No acquisition is
  requested without an exact file/source/size and purpose.

Current source-fixture checks: `python3 -m pytest -q
app/tests/production_inputs_test.py` (16 tests, including actual case/firmlink
alias refusal on this filesystem). A corrected unqualified plan is retained at
`/Users/ryan/dev/chirality-t3/scratch/app-package-inputs-frozen-b42vohmf/plan`:
config SHA `389a8e491d84fe7517f8aea483761e2dc511f1376ef0ef8f27b64c8c96fd2287`.
It has fifty resource mappings, a validated completion marker, a disposable
22,190,080-byte Git App export of exact `e7a21ddb9b61de8d2e8d8b27b9c69f10d03cc8f7`
and a full mode/byte-equal durable copy of the retained vendor. Its adjacent
`source-export.json` binds the export and comparison. No build or signing ran;
actual building will select the then-current integrated source and prepared
tool/cache/environment values rather than silently relabel this plan.

The earlier `app-package-inputs-wgel4r51/plan` is retained as a historical input
test only. It lacks the new completion marker and names a live checkout and
volatile `/private/tmp` vendor. Do not execute that earlier recipe. Preserve both
input accounts until their consumers release them; neither is an App artifact.
