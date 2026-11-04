# Shipped notice/source coverage for macOS arm64 — P6 account (2026-11-04)

This account advances PUBLICATION_PUNCHLIST P6 from main `e549c655` using only
retained inputs and prepared offline caches. Nothing was downloaded, built,
executed or sent. It distinguishes **prepared inventory** (texts identified and
digest-bound) from **bundled coverage** (texts actually placed in a candidate),
which a later build must still verify. No licence election, legal approval,
supplier pin qualification or "complete compliance" claim is made here.
The earlier [direct-runtime account](CACHED_SHIPPED_NOTICE_INPUTS.md) and the
[supplier association investigation](supplier-notice-associations/README.md)
remain the record of their own dates. The 2026-11-04 repair of the index checks
is described below. The manifests and locks are unchanged through main
`f9dd4ef7`, and the regenerated member set equals the original one.

## App: target/feature-selected dependency input graph

[`app/packaging/notices/transitive.py`](../../../../app/packaging/notices/transitive.py)
derives the Rust dependency **input** graph with an offline `cargo tree`. It uses
the release recipe's features (`custom-protocol,distribution-successor`), target
`aarch64-apple-darwin`, and `--edges normal,no-proc-macro`. That excludes
build-dependencies, dev-dependencies and proc-macros, which run at compile time,
and drops other-platform crates. The result is what Cargo selects to compile for
that target and feature set. It is not an observation of the final linked or
shipped contents; dead-code elimination and linking are not examined. The
prepared Cargo home holds every locked archive, and each archive's SHA-256
equals its `Cargo.lock` checksum. The committed
[transitive-index.json](../../../../app/packaging/notices/transitive-index.json)
records each crate's declared licence, its exact root licence/notice members
(size and SHA-256), its native-source paths and its upstream VCS locators. It
also records a generation receipt: the exact command, the Cargo version and
canonical member-set digests (cargo `dd7a3d7c…`, npm `9ddedcc0…`).

| Input-graph piece | Count | Text standing |
|---|---:|---|
| Rust crates, registry | 192 | 173 with licence/notice files inside the exact locked archive |
| objc2-family crates | 7 of the 192 | Associated with the received objc2 `LICENSE.md` (blob `540ae4c8`): same VCS revisions, and the READMEs link `../../LICENSE.md`. This adds `objc2-core-foundation` and `objc2-web-kit` to the five already associated |
| Rust crates with no text | 12 of the 192 | Missing; see the remaining edges below |
| npm runtime, direct | 3 | `@tauri-apps/api` 2.11.0, `react` and `react-dom` 19.2.7. These reuse the direct index's existing provenance: four licence files matched against the exact locked tarballs in [CACHED_SHIPPED_NOTICE_INPUTS](CACHED_SHIPPED_NOTICE_INPUTS.md). `check` requires unchanged versions, integrity and text digests (`0d542e0c`/`9dd42ea9`, `da6d3703`) |
| npm runtime, transitive | 1 | `scheduler` 0.27.0, reached through `react-dom`. Its `LICENSE` digest (`da6d3703`) comes from the prepared installed tree only. It stays **unverified**: no lock tarball for it is held locally |

How far each check reaches:

- **Cargo-free `check` (CI).** This check cannot re-resolve the graph. It fails
  closed when any of these hold:
  - the manifests or locks move;
  - the rows no longer reproduce the receipt's member-set digests (a dropped,
    added or altered row);
  - a row contradicts `Cargo.lock` in version, checksum or registry/path source
    kind (only the workspace package may be `path`);
  - a row is unreachable from the workspace root through lock edges;
  - the npm rows differ from the closure recomputed from `package-lock.json`
    (dependencies and required peers, flat lookups only; nested, optional,
    bundled or missing lookups refuse);
  - a received-text row names anything but the one allowed retained file and a
    known revision-to-blob association. Both are checked before the file is
    opened.
- **What it cannot catch.** Lock edges cover every dependency kind and platform.
  A row dropped *together with* a rebound receipt therefore still passes the
  Cargo-free check.
- **`check --cargo-home <prepared>`** re-resolves the exact member set offline
  and re-reads every archive. It is reproducible only with the same lock, the
  same features and target, and a Cargo whose resolver gives the same selection
  (the receipt records the version used).

The direct index (22 components) remains a subset; `check` enforces that. By
crate source and build reasoning, not binary observation, the only native code
in the input graph that a build compiles is SQLite, through `libsqlite3-sys`
with its bundled feature (its own prepared
[notice](../../../../app/packaging/sqlite_notice/README.md)). The archive also
carries `sqlcipher/` and a wasm32 VFS source that this feature and target selection does not
build. The `.c` files in `fancy-regex` (`tests/oniguruma/`) and `walkdir`
(`compare/nftw.c`) are test and benchmark sources. Fonts are covered by the
[font notice](../../../../app/packaging/font_notice/README.md). Regenerate with
`python3 app/packaging/notices/transitive.py generate --cargo-home <prepared> --node-modules <prepared>`.

## Supplier binaries: marker observations, not content determinations

Read-only regex byte searches of the four retained 0.160.0 subjects are recorded
with counts and first offsets in
[binary-component-observations-20261104.json](supplier-notice-associations/binary-component-observations-20261104.json).
A marker present is a concrete clue. A marker absent shows only that this exact
byte pattern does not occur. It does not show that the corresponding code is
absent, because code can be compressed, stripped or renamed. These are not byte
joins.

- **Main `codex`** (`112fae7a…`).
  - **Present:**
    - `name: skill-creator` (1 hit at 186,397,252) and `name: skill-installer`
      (1 at 186,451,022);
    - `APPENDIX: How to apply the Apache License` (2 at 186,194,686);
    - `bwrap` (9 at 182,781,768).

    The embedded skill samples are consistent with their `LICENSE.txt` files at
    the commit (11,358 B, blob `d6456956…`).
  - **Absent (exact patterns only):**
    - `name: imagegen` and `name: openai-docs` (0 each);
    - `usage: %s \[OPTIONS|--unshare-user|bubblewrap\.c` (0);
    - `v8::internal` and `icudt\d+l` (0 each).
  - **Separate source/target reasoning, not a binary observation.** The vendored
    `codex-rs/vendor/bubblewrap` (LGPL `COPYING` 25,383 B) is built for Linux
    targets. Whether any of it reaches this macOS binary is not established by
    the absent markers, and remains a supplier-source question.
  - `wezterm` appears as a terminal name.
  - Root `LICENSE`/`NOTICE` at the declared commit `a956835d` are exactly
    available locally (10,926 B `d17f227e…` and 242 B `9d71575e…`); this edge was
    already established.
- **`codex-code-mode-host`** (`679eedae…`). **Present:**
  - `v8::internal` (63 at 37,797,617);
  - `v8-150\.4\.0/src/` (18 at 37,561,974);
  - `icudt77l` (2,330 at 37,720,709);
  - `Unicode, Inc\. and others\. License & terms of use` (52 at 38,417,719);
  - `NSt4__Cr` (2,311 at 50,167,573).

  These are concrete clues that V8 through the `v8` crate 150.4.0, ICU 77 data
  and Chromium's libc++ namespace are present. They name **potential** notice
  edges: the V8 terms, ICU/Unicode terms, libc++/libc++abi, and the `v8` crate's
  own licence. They are not an independently complete static-link or licence
  determination, nor an exact binary-to-source join. None of those texts is
  local.
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
2. **npm `scheduler` 0.27.0 only.** The three direct packages already have
   archive-verified texts. Verifying `scheduler`'s text needs its one lock
   tarball (integrity `sha512-eNv+WrVb…`, size not established locally). Until
   then it stays explicitly unverified.
3. **Main and code-mode-host Rust dependencies.** These need `codex-rs/Cargo.lock`
   at `a956835d` (406,552 B, blob `19885ae9…`) plus the 160 workspace
   `Cargo.toml` manifests (178,197 B in total). Those resolve the linked macOS set;
   the dependency archives' count and size follow only from that set.
   The alternative is a supplier-provided third-party notice or attestation for
   0.160.0.
4. **code-mode-host V8 stack (potential edges from the clues above).** This
   needs the `v8` 150.4.0 crate's licence files and the V8/ICU/libc++ terms
   (size unknown), plus confirmation of what is actually linked. The commit's
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
