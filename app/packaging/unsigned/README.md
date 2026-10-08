# Complete-content development App bundle route

This explicit overlay maps the received production workflow candidate and role
resources into an unsigned development bundle. It leaves the default Tauri
configuration unchanged. Physical content does not establish package_complete,
qualification, runnable LS-5/LS-8 registration, signing or release.

Use an isolated copy of the exact App source, existing approved offline npm
and Cargo caches, a private Cargo home and target, and an allowlisted environment
without Apple or Tauri signing/notary variables. No download, supplier execution,
native App launch, credentials or manual signing belongs to this route.

```sh
CARGO_NET_OFFLINE=true CARGO_TARGET_DIR=/absolute/private-target \
  node node_modules/@tauri-apps/cli/tauri.js build \
  --debug --no-sign --bundles app --features custom-protocol \
  --config packaging/unsigned/tauri.development.conf.json \
  --config /absolute/supplier.development.conf.json \
  -- --offline --locked
```

Set CARGO_HOME to the isolated prepared cache view. The explicit
`--features custom-protocol` is required: it selects the packaged resource
consumer, including fail-closed validation of P2 and P3, even for this debug
build. The existing before-build command builds TypeScript and Vite.
`--no-sign` is required, not merely a null signingIdentity. The linker may
produce its incidental arm64 ad-hoc signature; that is unqualified compiler
output, not Developer ID signing or FP-1(b). Do not manually sign it.

Supply the approved complete vendor directory with a scratch-only overlay:

```json
{"bundle":{"resources":{"/absolute/identified/vendor/":"codex/"}}}
```

An optional subsequent bundle command must use the same configurations,
`--debug --no-sign --bundles app --features custom-protocol`, private target
and clean environment. It does not rebuild the executable. Inventory the
actual final bundle, including content hashes, directory/file modes and links;
compare all P1/P2/P3 entries to the exact selected source with no extras or
omissions. Bind source and artifact hashes and preserve the actual commands.

| Place | Physical input | Standing |
|---|---|---|
| P0 Contents/MacOS | Current App debug executable | Production resource feature; development artifact |
| P1 Contents/Resources/codex | Explicit approved cached vendor tree | Content comparison only; qualification pin not selected here |
| P2 Contents/Resources/workflows | Full resources/production_workflows tree including MANIFEST.json | Candidate inventory; LS-5/LS-8 not runnable |
| P3 Contents/Resources/instructions | Full instructions tree including roles.json and ROLE_SET_SOURCE_BINDING.json | Exact received candidate role content; no release default decision |
| P4 Contents/Info.plist | Tauri generated metadata | Existing skeleton identifier/version; minimum macOS 15.0 remains proposed |

The product label is Chirality App v4 (development candidate), version 0.0.0,
identifier dev.chirality.app-v4.skeleton. No microphone usage string is requested.
The production identifier and minimum OS decisions remain with their owners.

A physical P0–P4 candidate remains unsigned and unqualified. The source at this
build basis has no qualified S3 distribution reference and no actual H3B runtime
witness. Do not insert a synthetic anchor. FP-1(b), FP-2/W-4, FP-3/4/5, SIGN-1,
M2/M3, quarantine/install/launch and account acts are not supplied by bundling.
The cached 0.160.0 selection does not apply R23-22 qualification-pin selection.
