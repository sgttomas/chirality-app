# Current unsigned App and ZIP — execution brief awaiting independent READY

## Objective and exact source

Produce one actual current-source unsigned development App and its actual app_zip,
plus a separate truthful unsigned-artifact observation. This is not a PKG-v0.2
identity record: that schema's required signing identity/actor meanings cannot
be filled by fake signers or placeholder account acts. Full static-distribution
consumer and S4 remain held; no synthetic trust anchor is authorized.

Selected source: 9a82cbcf29c46bb6f722c074b5854de7ef470450, matching locally observed
origin/main at freeze. The delta from previously proposed 56403d6e is Group C
proposal/graph evidence only; App bytes do not change. Verify current main again
before execution release. A newer revision needs an explicit source update,
changed-input assessment and affected review before it replaces this selection.
The brief's own later evidence commit is not a different compiled source.

Reuse the existing lane worktree. Copy only the selected committed app tree to
new private scratch after release; no new worktree, agent, download or rebuild
of historical candidates. Preserve the original complete-content scratch and
historical manifest cd0e8f7216d6c85b1b1cee96300e3b1f4aeaea15bbc6185214345290bdb83c15.

## Input selection and offline readiness

INPUT_CHECK.json hashes Cargo/package locks, configuration, full P1/P2/P3 files
and modes, source roots and cached CLI/ditto. P1 is the approved complete cached
0.160.0 development vendor tree, manifest
327effb91a5854eccb388321b4b160e059795f0402c553f594e85365189d8d12.
P2 production_workflows manifest is
8cace852d4b72aea955613a0b2ea3de73f674059e43d17e6b87679692f39c119;
P3 instructions manifest is
387fee872193655b95ac2736d85cf905e012343ae220adf7e87e50768fc083cc.
P2 contains MANIFEST.json; P3 contains roles.json and ROLE_SET_SOURCE_BINDING.json.
This is source availability, not observed completeness of an unbuilt artifact.

Existing prepared npm dependencies and private read-through Cargo registry view
are selected. Both lockfiles equal the prior successful Apple Silicon build.
All 265 registry packages compiled by that run remain present. Some entries for
the all-platform Cargo lock are absent from cache; they are listed honestly and
are not treated as an Apple Silicon dependency failure. This is a filesystem
presence check, not a new resolver/build pass. If the offline build reports a
missing required package, stop and return its exact name/version; never download
or bypass offline/locked mode. No install or Cargo operation ran for this brief.

The source has custom-protocol, distribution-successor and synthetic-distribution-
anchor features. Enable only custom-protocol; retain default legacy distribution
behavior. Explicitly record that neither successor nor synthetic anchor is enabled.
Do not alter Cargo/configuration/source pins to obtain a different result.

## Execution release conditions

Do not build until independent brief/input review returns READY and the manager
releases execution. Parent reports cleanup complete; observed free capacity is
about 18.9 GiB. Repeat physical-filesystem df immediately before work: require at
least 4 GiB available (4,194,304 KiB), a planning allowance based on the earlier
2.23 GiB compilation directories plus executable/resource staging, App and ZIP.
It is not a guaranteed maximum. Stop if space approaches 1 GiB during compilation
or packaging; preserve outputs and report, do not clean another lane to continue.

Group C manager has confirmed the serial Rust window and will coordinate before
its next Rust start. Reconfirm that reservation at execution release, inspect
process names only for cargo/rustc/linkers, and use CARGO_BUILD_JOBS=1. A process
snapshot alone is not the reservation. No Rust process has been started here.

## Physical scratch and output ownership

Reserve `/private/tmp/chirality-b2-current-9a82cbcf/` (confirmed absent at brief).
It will contain app/, cargo-home/, home/, target/, supplier.development.conf.json,
logs/ and artifacts/. This lane owns only that newly created scratch. Refuse an
unexpected existing directory instead of overwriting it. Keep source/evidence
path-neutral in committed records; the local artifact path may be reported.

Final App: target/debug/bundle/macos/Chirality App v4 (development candidate).app.
Final ZIP: artifacts/Chirality-App-v4-development-9a82cbcf.app.zip.
No old artifact/target is reused or overwritten. The new private Cargo home may
link only its registry to the existing approved cache; node_modules may link to
the existing approved dependency tree. These shared link destinations are not
owned and must never be removed or modified. No cache cleanup is part of this
brief. Later scratch cleanup requires an explicit list after review/evidence
retention and preserves the App, ZIP, inputs and needed recovery evidence.

## Build and archive commands — proposed, not executed

Use an allowlisted environment created from empty. Supply only PATH for selected
Node/Rust/system tools, scratch HOME/TMPDIR, approved RUSTUP_HOME, private
CARGO_HOME/CARGO_TARGET_DIR, CARGO_NET_OFFLINE=true, CARGO_BUILD_JOBS=1,
CHIRALITY_SKIP_CODEX=1, CI=true and LANG. Record actual selected tool versions,
hashes, logical paths and exact arguments. Inherit no Apple, notary, Tauri signing,
credential, Cargo feature or RUSTFLAGS variables. Do not inspect keychains or
signing identities. The existing before-build script builds TypeScript and Vite.

From scratch/app:

```sh
node node_modules/@tauri-apps/cli/tauri.js build \
  --debug --no-sign --bundles app --features custom-protocol \
  --config packaging/unsigned/tauri.development.conf.json \
  --config ../supplier.development.conf.json \
  -- --offline --locked
```

The scratch supplier overlay maps the exact approved physical vendor directory
to codex/. Maintained overlay maps production_workflows to workflows/ and
instructions to instructions/. Keep existing development product name, version
0.0.0, dev.chirality.app-v4.skeleton identifier and proposed minimum macOS 15.0.
These are recorded development choices, not production defaults or owner decisions.

After build success, explicit signing-skip evidence and physical comparisons:

```sh
/usr/bin/ditto -c -k --sequesterRsrc --keepParent \
  "target/debug/bundle/macos/Chirality App v4 (development candidate).app" \
  "artifacts/Chirality-App-v4-development-9a82cbcf.app.zip"
```

Run the archive command from scratch root, not app/. The actual directory/file
must be selected explicitly, never by an unbounded glob or latest pointer.
No DMG, notary/stapling, signing or native/supplier launch. Incidental linker
ad-hoc signing is allowed unqualified compiler output; no manual signing.

## Required artifact observation and verification

Freeze before-build source/config/resource entries and hashes. Confirm scratch
source equality after build, except declared generated outputs. Record Cargo's
actual compiled feature fingerprint and forwarding to tauri/custom-protocol;
assert no distribution-successor or synthetic-distribution-anchor feature.
Retain build exit/log and tool identities; a compiler pass is not a runtime pass.

Inventory the full actual App with root separately included: path, kind, mode,
size/hash for regular files, literal target for links, counts with and without
root, and deterministic file manifest. Bind P0 executable hash, architecture,
Info.plist bytes and decoded actual values. Read-only signature display may record
incidental signing, with no cryptographic verification or qualified-signing claim.
Compare all actual P1/P2/P3 entries and root modes against exact selected sources,
including no extras/missing entries, manifest and role-set bindings. Preserve
physical presence and candidate/non-runnable workflow standing separately.

Hash and size the actual ZIP; inventory its entries, types, modes and contents.
Check archived App payload equals the pre-archive App inventory, allowing only
identified ditto resource-fork metadata entries under __MACOSX. Reject unexplained
extra/missing payload, changed file bytes, modes or link targets. Streaming ZIP
reads avoid another large extraction copy. Document metadata limits rather than
claiming installation validity. Rehash ZIP and rescan original App/resources after
archive checks; confirm source/scanner/tool identities unchanged. A failed check
stops handoff and returns the exact difference; no evidence is silently rewritten.

Retain in this run: BUILD_INPUTS, command/environment receipt, tool identities,
build log/exit, full App/resource inventories and comparisons, P0/plist/feature
records, ZIP identity and payload comparison, before/after guards, unsigned
observation and concise RETURN. Include actual source revision and distinct build
identity; do not emit PKG-v0.2, fabricated signer, S1 attestation, S3 anchor, runtime
event or package_complete/qualification claims. A separate independent reviewer
must inspect exact sealed files and retained App/ZIP before fan-in.

The unsigned observation remains development-only. Current-source physical App
and actual archive remove an artifact gap, not signing/identity-contract, S4,
qualified pin, native FP2/W4/M2/M3, LS5/LS8 admission or release obligations.
A later signing decision must use the actual reviewed artifact and then address
concrete candidate/config/owner inputs; this brief asks no owner point-action.
