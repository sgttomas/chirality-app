# Shipped notice/source coverage for macOS arm64 — P6 account (2026-11-04)

This account advances PUBLICATION_PUNCHLIST P6 from main `e549c655` using only
retained inputs and prepared offline caches. Nothing was downloaded, built,
executed or sent. It distinguishes **prepared inventory** (texts identified and
digest-bound) from **bundled coverage** (texts actually placed in a candidate),
which a later build must still verify. No licence election, legal approval,
supplier pin qualification or "complete compliance" claim is made here.
The earlier [direct-runtime account](CACHED_SHIPPED_NOTICE_INPUTS.md) and the
[supplier association investigation](supplier-notice-associations/README.md)
remain the record of their own dates.

## App: actual runtime dependency graph

[`app/packaging/notices/transitive.py`](../../../../app/packaging/notices/transitive.py)
derives the shipped Rust graph with an offline `cargo tree`. It uses the release
recipe's features (`custom-protocol,distribution-successor`), target
`aarch64-apple-darwin`, and `--edges normal,no-proc-macro`. That excludes
build-dependencies, dev-dependencies and proc-macros, which run at compile time
and are not shipped, and drops other-platform crates. The prepared Cargo home
holds every locked archive; each archive's SHA-256 equals its `Cargo.lock`
checksum. The committed [transitive-index.json](../../../../app/packaging/notices/transitive-index.json)
records each crate's declared licence, exact root licence/notice members
(size and SHA-256), bundled native-source paths and upstream VCS locators.

| Runtime piece | Count | Text standing |
|---|---:|---|
| Rust crates, registry | 192 | 173 with licence/notice files inside the exact locked archive |
| objc2-family crates | 7 of the 192 | Covered by the received objc2 `LICENSE.md` (blob `540ae4c8`): same VCS revisions, README links `../../LICENSE.md`. This adds `objc2-core-foundation` and `objc2-web-kit` to the five already associated |
| Rust crates with no text | 12 of the 192 | Missing; see the remaining edges below |
| npm runtime packages | 4 | `@tauri-apps/api`, `react`, `react-dom` and transitive `scheduler` 0.27.0. Texts are taken from the prepared installed tree only; lock tarballs are not re-verified here |

The direct index (22 components) remains a subset; `check` enforces that. The
only compiled-in native source is SQLite via `libsqlite3-sys` (its own prepared
[notice](../../../../app/packaging/sqlite_notice/README.md)). The `.c` files in
`fancy-regex` (`tests/oniguruma/`) and `walkdir` (`compare/nftw.c`) are test and
benchmark sources, not built. Fonts are covered by the
[font notice](../../../../app/packaging/font_notice/README.md). The default
`check` needs no Cargo and fails closed whenever the manifests or locks move;
regenerate with
`python3 app/packaging/notices/transitive.py generate --cargo-home <prepared> --node-modules <prepared>`.

## Supplier binaries: what the shipped bytes contain

Read-only byte searches of the four retained 0.160.0 subjects are recorded in
[binary-component-observations-20261104.json](supplier-notice-associations/binary-component-observations-20261104.json).
These are clues with offsets, not byte joins.

- **Main `codex`** (`112fae7a…`): the bundled skill samples `skill-creator` and
  `skill-installer` are embedded, together with two copies of the full Apache
  2.0 text. That is consistent with their `LICENSE.txt` files at the commit
  (11,358 B, blob `d6456956…`). `imagegen` and `openai-docs` are not embedded.
  - bubblewrap's C code is absent. There is no usage text; `bwrap` appears only
    as option tokens. The vendored `codex-rs/vendor/bubblewrap` (LGPL `COPYING`
    25,383 B) is Linux-only and does not apply to this macOS binary.
  - `wezterm` appears only as a terminal name.
  - Root `LICENSE`/`NOTICE` at the declared commit `a956835d` are exactly
    available locally (10,926 B `d17f227e…` and 242 B `9d71575e…`); this edge
    was already established.
- **`codex-code-mode-host`** (`679eedae…`) statically contains:
  - V8 through the `v8` crate 150.4.0 (source paths `v8-150.4.0/src/`, 63 `v8::internal` strings);
  - ICU 77 data (`icudt77l`) with "Unicode, Inc. and others" terms strings;
  - Chromium's libc++ (2,311 `NSt4__Cr` symbols).

  This adds concrete notice obligations: the V8 BSD-3-Clause terms, ICU (the
  Unicode licence), libc++/libc++abi (Apache-2.0 WITH LLVM-exception), and the
  `v8` crate's own licence. None of those texts is local.
- **`rg`** and **`zsh`**: unchanged from the
  [four-file receipt](supplier-notice-associations/approved-receipt-20261102-four/SCOPE.md).
  The release selectors are resolved; the byte joins and licence texts are not.

## Exact remaining edges and minimal next inputs

No retrieval is authorized by this account. Each item names the exact input;
"size unknown" means not established locally.

1. **App Rust crates without text (12).** The need is each upstream
   repository's root licence file at the crate's recorded revision. File names
   and sizes are unknown; public tree metadata for these six repo revisions
   would establish them before any body request:
   - `dropbox/rust-alloc-no-stdlib@6032b6a9` (alloc-stdlib, BSD-3-Clause: copyright notice required);
   - `Stranger6667/jsonschema@21a061d6` (jsonschema-regex/-value);
   - `madsmtm/objc2@8d214f54` (objc2-encode, objc2-exception-helper);
   - `open-i18n/rust-unic@58786053` and `@8a6ce830` (the five unic crates);
   - `Nugine/simd@d74c030d` (uuid-simd, vsimd).
2. **npm texts.** Re-verifying the four installed texts needs the four lock
   tarballs (integrity known, size unknown), or an explicit acceptance of the
   prepared installed tree.
3. **Main and code-mode-host Rust dependencies.** These need `codex-rs/Cargo.lock`
   at `a956835d` (406,552 B, blob `19885ae9…`) plus the 160 workspace
   `Cargo.toml` manifests (178,197 B in total). Those resolve the linked macOS set;
   the dependency archives' count and size follow only from that set.
   The alternative is a supplier-provided third-party notice or attestation for
   0.160.0.
4. **code-mode-host V8 stack.** This needs the `v8` 150.4.0 crate's licence files
   and V8/ICU/libc++ terms (size unknown). The commit's
   `third_party/v8/rusty_v8_150_4_0_release_manifests.sha256` (1,040 B) identifies
   the prebuilt inputs. The host **byte join** still needs the release asset
   `codex-code-mode-host-aarch64-apple-darwin.tar.gz` (23,825,926 B,
   `sha256:dc70fbc7…`).
5. **rg.** This needs `ripgrep-15.2.0-aarch64-apple-darwin.tar.gz`
   (1,764,284 B, `3750b2e9…`): it carries ripgrep's licence files and the
   unsigned member for comparison. The PCRE2 licence needs ripgrep 15.2.0's
   `pcre2-sys` source; its version and size are unknown.
6. **zsh.** This needs the `codex-zsh-v0.1.0` manifest (digest `c534eab8…`, size
   unknown), the archive it names, and zsh's licence at `77045ef8`
   (`git.code.sf.net/p/zsh/code`, size unknown).

Placing the prepared texts in a bundle (a notices overlay or the production
mapping) is a later packaging step with its own build verification. P6 stays
open until the edges above are closed or each is explicitly resolved before release.
