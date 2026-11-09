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

## 2026-11-09 current supplier subject: Codex 0.167.0

The selected supplier is now the canonical Codex 0.167.0 package: 42 files with
manifest `158dd670…`, from the release asset at 166,340,155 B, `af45ed45…`. The
supplier statements in the 2026-11-04 section below describe the 0.160.0
subject (manifest `327effb9…`) and stay as that subject's record. The 0.167.0
associations were derived offline from retained bytes and public metadata
responses by
[`associate_0167.py`](../../../../app/packaging/supplier_notices/associate_0167.py).
Its outputs, and the command to recheck them, are in
[supplier-notice-associations/codex-0.167.0](supplier-notice-associations/codex-0.167.0/README.md).
Nothing was downloaded, built or executed. The only network reads were six
public tree-metadata responses: root, `third_party`, `third_party/v8`, the
recursive `codex-rs` tree, `scripts` and `scripts/codex_package`. Together with
the two retained release responses, their hashes are recorded with the outputs.

| 0.167.0 component | Change from 0.160.0 | Current association standing |
|---|---|---|
| Main `bin/codex` `030316ec…` | Changed | The voice manifest binds it to build commit `086ccc83`, and release tag `rust-v0.167.0` names that commit. Root `LICENSE` (10,926 B, blob `4606e72e`) and `NOTICE` (242 B, blob `2805899d`) at that commit equal the committed [supplier texts](../../../../app/packaging/supplier_notices/codex-0.160.0), so the root-text association carries with no new text. Dependency notices remain open (edge 3) |
| `bin/codex-exec-server` `385736a6…` | **New** | Not manifest-bound. It embeds `codex-exec-server0.167.0`, 143 `exec-server/src` paths and 3,319 crates.io registry paths (231 distinct crate directories). The main binary also embeds 225 `exec-server/src` paths. The root texts are a **candidate** association only; its dependency closure belongs to edge 3 |
| `bin/codex-code-mode-host` `5cc29d14…` | Changed | Not manifest-bound. It now shows `icudt78l` (ICU 78) together with the V8, Unicode-terms and libc++ clues. At the commit, `third_party/v8` names rusty_v8 **152.2.0** (edge 4) |
| `codex-path/rg` `13424ef2…` | Re-signed only | Same size and code-signature offset as 0.160.0; every byte before the signature blob is equal. It embeds ripgrep `15.2.0` followed by revision `e89fff89ac`, and `16.0.0` beside PCRE2 `10.46 2025-08-27`. The [2026-11-02 receipt](supplier-notice-associations/approved-receipt-20261102-four/SCOPE.md) identifies that `16.0.0` as PCRE2's Unicode version, not a ripgrep version. At `086ccc83` the release selector `scripts/codex_package/rg` (blob `3b7c3484`) and `ripgrep.py` (blob `155c5d32`) equal the received 0.160.0 texts, so 0.167.0 still selects the ripgrep 15.2.0 archive (edge 5). These are string and selector clues plus a binary-to-binary comparison, not a byte join |
| `codex-resources/voice/**` | Libraries and host rebuilt | `NOTICE.md`, the seven `licenses/` texts and `sources.json` are byte-identical to 0.160.0, so the declared upstream versions and archive digests are unchanged. The manifest binds every voice file to `086ccc83`. The supplier-provided voice notices carry as before |
| `codex-resources/zsh/bin/zsh` | **Removed** | The 0.160.0 zsh edge does not apply to 0.167.0 |

These associations bind bytes to source locators. They do not establish build
equivalence, linked contents or notice applicability, and they make no
compliance claim.

## 2026-11-07 local association successor

On App main `85505f95`, ten of the twelve missing-root rows still had no
maintained association despite previously verified local byte matches. The
explicit `chirality.app.transitive-runtime-notices/3` successor now records
those ten **root candidates**, with source origins and unresolved scope kept in
its rows. Historical `/2` indexes retain their reader/meaning. The original
Cargo/npm member-set digests, graph generation receipt, manifests and locks
are unchanged; `transitive.py associate-local` derives only this source-text
join from the checked earlier graph, without running Cargo.

| Current preparation piece | Count | Standing |
|---|---:|---|
| Locked crates with archive notice members | 173 | Unchanged input-archive facts |
| Earlier received objc2 overview associations | 7 | Unchanged; overview is not full licence terms |
| Newly associated retained root candidates | 10 | alloc-stdlib (1), jsonschema-regex/value (2), objc2-encode/exception-helper (2), five UNIC crates (5); all remain unqualified |
| Rows with no retained root text | 2 | uuid-simd/vsimd; outref's same-size text has a different blob |
| scheduler | 1 npm package | Installed-copy-only text remains unverified; sole approved HEAD gave no archive size |

The four already-available distinct bodies are Dropbox LICENSE (from the exact
alloc-no-stdlib locked archive), jsonschema LICENSE, and UNIC's Apache/MIT
texts (reused existing uuid/serde notice assets). The existing objc2 overview
also matches the additional source revision. This is content correspondence
through retained public root metadata, not a new upstream download or a licence
election. Exact roots, archive/index/asset identities and limits are in the
[local association receipt](supplier-notice-associations/retained-root-associations-20261107/README.md)
and its `proof.json`. UNIC COPYRIGHT.md is still missing, its crate VCS paths
are absent, and objc2's full-terms/SDK caveat remains. Every new row remains in
`missing_or_unverified`; no row is labelled archive-provided or fully covered.

The fixed association manifest is source-hash-bound before any reference is
opened. Each new row must equal its exact package/version/archive/declared-licence
subject and fixed root/source/bytes/scope record. Source text uses the maintained
no-follow regular-file reader and must match size, SHA-256 and Git blob. Wrong
paths/revisions, altered limits, unknown subjects, links and text drift refuse.
The new source file is prepared input only: no resource overlay or built
candidate was changed. Existing historical bundle subjects remain untouched.

The dated 2026-11-04 graph findings below keep their original evidence basis;
the current remaining-input list at the end reflects this local advance.

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

Agent 0's provenance inspection reproduced the earlier corrupt-index cases and
confirmed their refusals on `e2dec838`. It also found that the npm check accepted
the Cargo-only `archive-member` and `received-upstream-text` labels, which could
hide `scheduler` from the unverified list without establishing archive provenance.
The npm check now accepts only its own three text kinds. A regression first
failed for both Cargo labels on `scheduler` and `react`, then passed with the
restriction. The inventory and retained texts are unchanged; `scheduler` remains
unverified and P6 remains open. All 58 notice tests pass, including 13 transitive
cases. Both the default check and the offline prepared-Cargo-home check pass;
the latter independently reproduces the member set and archive notice members.

## Supplier binaries at 0.160.0: marker observations, not content determinations

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

1. **Remaining root bodies: two files, 1,670 bytes; owner deferred acquisition.**
   - `Nugine/simd@d74c030d9dc4f3cae02146d1f497ff62726ef09a/LICENSE`,
     1,062 B, blob `2c7eabb59093ea117d73b20effdd0414f87b2af2`, for
     uuid-simd/vsimd. The retained outref member is blob `2ca354be…`, so it
     cannot substitute.
   - `open-i18n/rust-unic@5878605364af97a3358368a6eaef02104af2e016/COPYRIGHT.md`,
     608 B, blob `0322ceec0b8f15aa2d74a6173c07cc8c6f3764b3`; the same blob/size
     appears at `8a6ce83063d90b91ae2ce59eddb803edd393fca9`. Receive once if
     approved; retain both revision correspondences.
   - The ten retained root candidates now have maintained byte/source
     associations, not full applicability/coverage. UNIC's absent crate paths,
     copyright account and the objc2 overview/full-terms/Apple-SDK caveat remain
     explicit. None of these is a new licence election.
2. **npm `scheduler` 0.27.0 only.** The direct package texts remain
   archive-verified. Its lock tarball is
   `https://registry.npmjs.org/scheduler/-/scheduler-0.27.0.tgz`, integrity
   `sha512-eNv+WrVbKu1f3vbYJT/xtiF5syA5HPIMtf9IgY/nKg0sWqzAUEvqY/xm7OcZc/qafLx/iO9FgOmeSAp4v5ti/Q==`.
   The sole permitted 2026-11-05 HEAD returned 200 without Content-Length.
   Exact archive size remains unknown; no new metadata/body request or receipt
   has occurred. Its installed text stays unverified.
Items 3–6 name the current 0.167.0 supplier edges. Their 0.160.0 forms remain
in the [0.160.0 source-graph proposal](supplier-notice-associations/codex-source-graph-proposal.json)
(159 files, 562,794 B at `a956835d`) and in this file's Git history.

3. **Main, exec-server and code-mode-host Rust dependency inputs: 173 files,
   604,854 bytes.** The [exact 0.167.0 source-text list](supplier-notice-associations/codex-0.167.0/source-graph-proposal.json)
   lists each path, immutable-commit URL, size and Git blob from the complete
   recursive `codex-rs` tree `c98bbd63` at `086ccc83`. It covers
   `codex-rs/Cargo.lock` (409,810 B, blob `2eae72da`) and all 172 `Cargo.toml`
   manifests, including `exec-server/Cargo.toml` (3,655 B). None of these blobs is
   held locally. The proposal prepares a source-graph investigation; it is not an
   observed linked set or a binary-to-source join. Dependency archives,
   target/feature resolution and notice applicability remain separate. The
   list is public source text under the standing read-only inspection
   authority; no row is held until its bytes are read and match size and blob.
   The alternative is a supplier-provided third-party notice or attestation for
   0.167.0.
4. **code-mode-host V8 stack (potential edges from the clues above).** At
   `086ccc83` this is rusty_v8 **152.2.0**, with ICU 78 data observed. It needs
   the `v8` 152.2.0 crate's licence files and the V8/ICU/libc++ terms (sizes
   unknown), plus confirmation of what is actually linked. The commit's
   `third_party/v8/rusty_v8_152_2_0_release_manifests.sha256` (1,040 B, blob
   `814e018a`) identifies the prebuilt inputs. A host **byte join** would need the
   release asset `codex-code-mode-host-aarch64-apple-darwin.tar.gz`
   (25,262,553 B, `sha256:876a3e26…`).
5. **rg: ripgrep 15.2.0 (revision `e89fff89ac`) with PCRE2 10.46, unchanged
   code since 0.160.0.** Known: the selector names
   `ripgrep-15.2.0-aarch64-apple-darwin.tar.gz` (1,764,284 B, `3750b2e9…`), and
   the binary's version, revision and PCRE2 strings. Unknown: a byte join of that
   archive's `rg` member with the shipped binary, the ripgrep 15.2.0 licence
   files, and the PCRE2 licence for the linked version through ripgrep 15.2.0's
   `pcre2-sys`, whose version and size are not established. The archive is a
   binary download needing its own permission; the licence and lock files are
   public source text. Version strings alone do not establish the join.
6. **exec-server (new).** Its root-text candidate and dependency inputs are
   covered by item 3 and the exec-server row above. A standalone byte join would need
   `codex-exec-server-aarch64-apple-darwin.tar.gz` (22,746,226 B,
   `sha256:82bb1c4d…`). It is not needed for the notice association itself.

Placing the prepared texts in a bundle (a notices overlay or the production
mapping) is a later packaging step with its own build verification. P6 stays
open until the edges above are closed or each is explicitly resolved before release.
