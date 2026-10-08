# Incomplete development App bundle route

This overlay is a build configuration, not a package or a production identity.
It leaves the default `src-tauri/tauri.conf.json` untouched. The CLI merges it
when explicitly selected. Use the exact locked App source and the installed
Tauri CLI 2.11.1. No dependency download, App launch or supplier execution is
part of this route.

The product label is `Chirality App v4 (development candidate)`. Version
`0.0.0` and identifier `dev.chirality.app-v4.skeleton` come from the current
source configuration; they make no release claim. Minimum macOS `15.0` is a
proposal for this experiment, not a resolution of U-PKG-5. The proposed final
identifier `dev.chirality.app-v4` is not selected by this overlay.

From an isolated copy of `app/`, with prepared offline npm dependencies and a
private writable Cargo home backed by the approved registry cache, run:

```sh
CARGO_NET_OFFLINE=true CARGO_TARGET_DIR=/absolute/private-target \
  node node_modules/@tauri-apps/cli/tauri.js build \
  --debug --no-sign --bundles app \
  --config packaging/unsigned/tauri.development.conf.json \
  -- --offline --locked
```

Set `CARGO_HOME` to the isolated cache view. Use an environment with no Apple
signing/notary or Tauri signing variables; the run evidence lists the actual
allowlisted environment. The before-build command runs the existing TypeScript
and Vite build. `--debug` identifies this as a development binary, never a
release/qualification build. `--bundles app` creates an App bundle only; no DMG.

`--no-sign` is required, even with `signingIdentity: null`: null alone does not
prove no automatic signing. CLI help and the installed binary's explicit skip
messages were inspected before use. Apple Silicon's linker adds an automatic
ad-hoc signature by default (local ld(1), `-adhoc_codesign`). The parent expressly
allowed that incidental compiler artifact on 2026-10-08. It is not Developer ID
signing, SIGN-1 reliance, FP-1(b), or an owner account act. No manual signing,
entitlement mutation, notarisation or native launch is authorized by this file.

## Optional identified supplier input

The checked run separately supplied the approved cached complete 0.160.0
vendor directory through a second, scratch-only JSON overlay. Supply an
absolute vendor path deliberately; do not put local cache paths in the
maintained Tauri configuration:

```json
{"bundle":{"resources":{"/absolute/identified/vendor/":"codex/"}}}
```

After the build, the actual run re-bundled the existing binary with:

```sh
node node_modules/@tauri-apps/cli/tauri.js bundle \
  --debug --no-sign --bundles app \
  --config packaging/unsigned/tauri.development.conf.json \
  --config /absolute/supplier.development.conf.json
```

Use the same isolated cache, target and clean environment as the build.
Inventory the selected source before relying on its published identity and
compare the entire bundled `Contents/Resources/codex` tree afterward, including
modes, links and extra/missing entries. This is an actual post-bundling
comparison, unlike Python staging. The development selection of 0.160.0 is
not qualification-pin selection and does not create A-IN/S1 verified standing.

## Composition and limits

| Place | This overlay supplies | Remaining input |
|---|---|---|
| P-0 | Current source's debug Tauri executable, once build succeeds | Production/release identity and examination |
| P-1 | Optional explicit supplier overlay; checked run used cached complete 0.160.0 | Applicable qualified identity/adoption; no supplier binary is executed or replaced here |
| P-2 | Nothing | Production workflows plus shipped-revision manifest; embedded `development_workflows` remains explicitly development content |
| P-3 | Current `resources/instructions/` copied to `Contents/Resources/instructions/` | `roles.json` is absent; guidance/roles alone are partial P-3 |
| P-4 | Tauri-generated Info.plist, if build succeeds | Production bundle identity/minimum OS decisions; no microphone usage string is requested |

An actual `.app` from this route is an **incomplete development candidate**.
Its existence does not support a complete PKG identity record. In the checked
run, the optional P-1 mapping did pass the post-bundling content/mode/link
comparison on this incomplete development candidate; no production pin or
signature-validity conclusion follows. FP-1(b), FP-2/W-4, FP-3, FP-4, FP-5, M2/M3,
installation and launch remain unrun. Qualification pin selection remains
R23-22's newest passed version-advance check at candidate-build time; cached
0.160.0 availability does not select a qualification pin.

Future complete resource mapping must take P-1/P-2/P-3 from their owning
suppliers and bind their actual identities. Do not substitute the development
catalog or invent a role-set file to make the inventory look complete. This
configuration does not alter hosting, S1 or any Design interface.
