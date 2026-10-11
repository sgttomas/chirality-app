# Explicit attested-reference resource route

`tauri.attested-reference.conf.json` adds the exact twelve-file compiled S3
closure under `resource_dir/distribution-reference`. It preserves the ordinary
development identity, unsigned settings and P2/P3 mappings. It supplies resource
placement for the `distribution-successor` feature; the default configuration
and synthetic-selection route remain separate.

Use the isolated prepared cache, private target, clean environment and separately
identified complete supplier overlay described in [README](README.md):

```sh
CARGO_NET_OFFLINE=true CARGO_TARGET_DIR=/absolute/private-target \
  node node_modules/@tauri-apps/cli/tauri.js build \
  --debug --no-sign --bundles app \
  --features custom-protocol,distribution-successor \
  --config packaging/unsigned/tauri.attested-reference.conf.json \
  --config /absolute/supplier.development.conf.json \
  -- --offline --locked
```

The build-selection anchor and every referenced file keep their original paths
below `distribution-reference`, exact bytes and digest bindings. Individual file
mappings prevent incidental additions to the source directory from becoming
bundle inputs. The maintained Rust test uses Tauri's actual resource mapper to
stage the closure and check every selected digest at the resolver's namespace:

```sh
cargo test --offline --locked --test attested_reference_packaging
```

This checks SDK placement and byte correspondence without building or launching
an App, executing Codex, signing or installing anything. An actual bundle still
needs its content inventory and applicable package/native checks. A matching
production tree refuses before supplier execution because installed custody is
not supplied; the resource map creates no custody issuer or verified standing.
The qualification pin, OI-011, FP-1(b), FP-2/W-4, owner acts and release remain
at their existing points of need.
