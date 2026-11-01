# macOS arm64 direct-runtime notice inputs (v2)

Current basis is exact native PR69 source
`7fdb470b9bedf3bea9f4369672dd24524a6c799d`, not a built package. The index selects
common direct runtime declarations plus applicable target-specific declarations
for `aarch64-apple-darwin`, retaining each component's declaration targets.
Top-level build/dev-only dependencies remain excluded. Known other-platform
conditions are excluded; unsupported runtime cfg expressions refuse explicitly
rather than silently drop a dependency. This is a bounded explicit target
selector, not a complete Cargo feature/cfg/transitive evaluator.

PR69 promotes objc2 0.6.4, objc2-app-kit 0.3.2, objc2-foundation 0.3.2,
block2 0.6.2 and dispatch2 0.3.1 to direct macOS runtime dependencies. Their five
cached crate archives match exact Cargo.lock checksums. None contains a root
LICENSE/NOTICE file: the README links to ../../LICENSE.md in the upstream
repository. The v2 index retains each declared license, locked archive/manifest,
exact .cargo_vcs_info revision/path and README digests, with `notice_gap` marking
missing upstream text. No generic MIT or other-package license is substituted.
The verifier prints these five missing components and `notice_text_coverage:
incomplete` even when index/asset correspondence passes.

There are now 22 indexed components (App +18 Cargo +3 npm), but still only the
existing 30 exact notice texts (133,902 bytes). The explicit notice overlay
continues to map its 31 existing index/text files; no new missing text is invented.
Actual new-candidate bundle inclusion and legal/transitive completeness remain
unestablished. Retained 12d26 and fdcf candidates keep their original inventories.

The historical v1 representation remains readable only for a matching basis with
no target-specific runtime declarations. It cannot silently describe the new
scope. v2 adds the selected target, per-component declaration targets and explicit
missing-text provenance; no old source snapshot or identity is rewritten.

From the repository root, using Python 3.11+ and no additional packages:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 app/packaging/notices/check.py
PYTHONDONTWRITEBYTECODE=1 python3 app/tests/notice_resources_test.py
```

The default check uses saved assets and this repository's current
manifests/locks; no sibling checkout, source cache, supplier, network or build.
It checks complete indexed assets, bytes, direct-runtime scope and the explicit
overlay. Source/archive provenance can also be checked with **already prepared**
local caches and the selected Git revision available:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 app/packaging/notices/check.py --archives \
  --cargo-home /absolute/private-cargo-home --npm-cache /absolute/npm-cache
```

Missing/changed archives or unavailable selected Git source refuse; no fetch,
download, extraction or fallback occurs. This mode compares archive checksums
against locks, manifest/license metadata, the complete provided root notice set,
exact tar-member bytes and App Git source. This is correspondence, not supplier
origin authentication or a determination of licensing rights.

`../unsigned/tauri.notices.conf.json` explicitly selects unsigned development:
the ordinary development configuration plus exactly 31 per-file mappings for
the index and 30 texts at `resource_dir/third-party-notices/`. Default,
development and attested-reference routes do not automatically select it.
After a separately coordinated future build window, use the ordinary unsigned
command with `--config packaging/unsigned/tauri.notices.conf.json` and the
separately identified supplier overlay. No build was performed here; a later
build needs its own exact source/candidate inventory. Never add these files
to the retained PR15 candidate or rewrite its evidence.

The focused test stages explicit source/destination pairs and checks the saved
namespace. It does **not** execute Tauri's Rust `ResourcePaths` mapper. Its
existing SDK test has no prebuilt private-target runner and needs compilation;
the CLI exposes no standalone mapper API. Actual SDK mapping, bundle inclusion
and native readability remain unrun under the no-build/no-GUI boundary.
No user-facing redesign is included.

The upstream toml `LICENSE-APACHE` ends with a blank line at line 202. Its exact
bytes and indexed archive digest are preserved. The full contribution's
whitespace check reports that one source-text EOF exception; excluding only
that exact asset leaves the code/docs/index diff clean. No broad attributes or
CI exception is supplied.
