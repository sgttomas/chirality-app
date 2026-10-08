# Explicit compiled synthetic-selection debug bundle

This separate opt-in route packages an invented, compiled selection for testing
its fixed development resource namespace. It is default-off, debug-only and
refused by release compilation. It is not a qualified supplier reference,
production Selected/Store route, runtime verification or permission to launch.

The ordinary `tauri.development.conf.json` and its `--features custom-protocol`
command remain unchanged. `custom-protocol` alone does not enable this feature.
Use this separate configuration instead of the ordinary development overlay:

```sh
CARGO_NET_OFFLINE=true CARGO_TARGET_DIR=/absolute/private-target \
  node node_modules/@tauri-apps/cli/tauri.js build \
  --debug --no-sign --bundles app \
  --features custom-protocol,synthetic-distribution-anchor \
  --config packaging/unsigned/tauri.synthetic-selection.conf.json \
  --config /absolute/supplier.development.conf.json \
  -- --offline --locked
```

This documents the selected route; no build, signing, supplier execution or native
launch was performed by the packaging contribution. Use the same isolated
prepared cache, private target, clean environment and separately identified
supplier overlay required by the ordinary development route. Nothing here
selects the `distribution-successor` feature or changes supplier pin choice.
`--debug` and `--no-sign` are required. No release build or manual signing is
part of this route; an incidental compiler ad-hoc signature is not qualification.

If bundling an already built executable separately, use the same debug/feature/
configuration choices and private target. Bundling does not rebuild it or prove
that an existing executable contains the selected feature.

The separate overlay retains the ordinary P2/P3 mappings and adds exactly four
files under `resource_dir/distribution-development-reference`:

| Source below src-tauri | Destination below resource_dir |
|---|---|
| resources/distribution-development-reference/build-selection.s2.json | distribution-development-reference/build-selection.s2.json |
| resources/distribution-successor/synthetic-expected.json | distribution-development-reference/expected.json |
| resources/distribution-successor/synthetic-attestation.json | distribution-development-reference/attestation.json |
| resources/distribution-successor/synthetic-evidence.json | distribution-development-reference/synthetic-evidence.json |

The two destination aliases are intentional: the unchanged attestation refers
to `expected.json`. They preserve exact source bytes and keep the closure at
four files, with no additional aliases or edits to existing synthetic resources.
The Rust startup helper owns the compiled selection and reads this fixed
namespace. It always retains development-unverifiable standing; the production
`distribution-reference` path remains separate. Equal hashes establish byte
correspondence, not real acquisition, independent review, adoption, custody,
observed labels, supplier verification or release authority.

A physical bundle still requires its actual content inventory and the existing
package/native checks at their authorized points of need. This route does not
supply FP-2/W-4, signing/notary/installation outcomes, credentials, or owner acts.
The maintained mapping/closure tests run without building or launching anything:

```sh
python3 -m unittest discover -s tests -p compiled_selection_packaging_test.py
```
