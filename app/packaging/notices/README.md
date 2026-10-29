# Optional direct-runtime notice inputs

This preparation contains the App MIT text and 29 unchanged license/notice
artifacts from the 13 direct Cargo runtime dependencies and three direct npm
runtime dependencies selected by the saved manifests/locks. Provided alternative
texts are retained without electing a license. `index.json` names each
package/version, locked archive identity, exact source member/path, manifest
digest and notice byte digest/size. The App text is bound to its Git source.
Paths contain no private cache locations.

This is not complete transitive coverage or a legal/compliance/release finding.
Bundled SQLite and the exact Codex main/code-mode-host/rg/zsh notice inputs remain
unverified; the index and owning DEL-01-06 Design retain those bounded inputs.
Existing P1 voice notices and stock supplier bytes are unchanged. Build/dev
dependencies (including tauri-build) are outside this runtime input.

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
