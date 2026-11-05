# Development build after the product stack, 2026-11-05

Standing: an offline local development build and static resource observations.
The App was not launched or installed. No model, native UI, journey, installed
custody, owner acceptance or release qualification is established.

## Source and artifact

- Source: main `eaf5d057afb82c28a928a5e347ad5749dd5adc96`, after
  #119, #124, #125 and #128. Its tree
  `ce5b122d5ffee5caa81f57518cf89506bde7d4db` equals checked head `d53b334a`.
- Product: `Chirality App v4 (development 20261104-dd4a2a30).app`.
- Bundle identifier: `dev.chirality.app-v4.candidate.20261104-dd4a2a30`.
- Debug version: `0.0.0`; minimum macOS: `15.0`. The planned production
  version and selected production identifier are unchanged.
- Executable SHA-256:
  `b98a30fe2dccba062e35a0c02896b67c4441f2b987016f091ea41e6f56caf4fc`.
- Bundle inventory manifest SHA-256:
  `4daea2fcd8260af0a5ae498a19d7a4689c93c85653aa0ef5f0893cc35064895b`.

## Build and observations

Agent 0 used the retained `build_dev_candidate.py` recipe with an immutable
Git archive export; every exported blob was checked against Git. It used the
prepared Cargo registry and npm tree, Rust/Cargo 1.97.1 and Node 24.18.0,
fresh scratch Cargo and Codex homes, jobs 2, offline/locked Cargo, and ordinary
`t3_slot` admission with memguard running. No download was performed.

The Tauri command selected debug, `custom-protocol`, `--no-sign` and the
development overlay plus the retained supplier overlay. It did not select
`distribution-successor`, a publisher input or a provisioning profile.
The build ran from 01:19:35 to 01:21:00 UTC on 2026-11-05 and exited 0.

Static comparisons established:

- Bundled supplier bytes and modes equal the retained vendor tree, manifest
  `327effb91a5854eccb388321b4b160e059795f0402c553f594e85365189d8d12`.
- Configured `instructions/` matches the exported source, manifest
  `50c82a3c663773b327d7ed84bb27a7d639514062e0d1335f7c47b6f3b0194d18`.
- Configured `workflows/` matches exported `resources/production_workflows/`,
  manifest `cd34f3262ece093f782cf1594063e2fc7681708ef8624899360187367fc73e29`.
- No embedded provisioning profile is present.
- `codesign --display` reports an ad-hoc, linker-signed Mach-O
  (`0x20002`), no team, no sealed resources and an unbound Info.plist. This is
  not a Developer ID signature or production identity/custody evidence.

The normal-account installed App was not changed. Earlier candidates and
their evidence remain retained. The later #126 integration (`5ff04393`)
changes notice preparation, tests, CI and Work only; its `app/src`,
`app/src-tauri`, package manifest and lock are identical to this source. The
build's subject remains **eaf5d057**, not the later main.

## Evidence and remaining work

Private evidence root under `chirality-t3`:
`scratch/app-dev-candidate-20261104-dd4a2a30-lqvrfff8/`. It retains the source
export, overlays, `build.log`, `build-facts.json`, `build-observation.json`,
`build-static-checks.json` and the bundle under `target/debug/bundle/macos/`.

The closed native activation/occlusion loop remains unresolved. Real-model,
native lifecycle/recovery/access, installed S4/SEAL-C and final production
qualification remain open. The runtime owner is preparing the precise
candidate-bound requirements and missing inputs; it has not been authorized
to start a model, read credentials or revive the GUI loop. Existing scripted
joins retain their original execution subjects and do not close J1/J2.
