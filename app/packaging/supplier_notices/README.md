# Supplier notice texts and associations

The checkers here (`crates.py`, `voice.py`, and `../notices/coverage.py` reading them) are
not built to resist deliberately forged, mutually consistent inputs: a listing entry, an
archive record, a manifest and a review record changed together to agree. The review of
the pull request that changes a curated file covers that boundary. What the checkers
enforce, site by site, is listed under "What is enforced and what
review covers" in `../notices/README.md`. The sections below describe the inputs and give
each one's review duties. A coverage decision that rests on a review
duty nobody has completed stays open.

`components.json` lists, for the supplier tree of the declared pin, the components
known inside each member, the committed text that is each component's notice
(repository, revision, path, size and digests) and its standing. The tree itself is
read from the declared pin's `CANONICAL_DISTRIBUTION.json` (the pin is
`DECLARED_PIN` in `app/src-tauri/src/hosting.rs`); its executables are the files
with an execute bit that are neither libraries nor data, a rule that fits this record
(checked against its Mach-O count), not a general proof. The table is a reviewed
input: `../notices/coverage-review.json` binds its digest and lists each component's
standing and exact texts, and its reviewer updates that record. `reviewed_for_pin` names
the pin the table was reviewed against; when the declared pin differs,
`../notices/coverage.py` lists the table as an open component rather than assume
the old associations. Every non-voice repository field of the component table
(components, texts, also_at) is either `https://github.com/<owner>/<repository>`, each
of owner and repository one or more letters, digits, `_`, `.` or `-`, neither of them `.`
or `..`, with no `.git` suffix in any letter case, or begins with exactly
`https://chromium.googlesource.com/`; anything else refuses, naming the field. This is a
check of form, not that such a repository exists. The
googlesource values are compared exactly wherever they are compared and are otherwise not
constrained in form (`../notices/coverage.py`, `check_repository_forms`). Every
committed text here is mapped into the package under `third-party-notices/supplier/`;
the voice libraries' licences ship inside the supplier tree itself.

The folders are the components' root texts at the revisions `components.json`
names: `codex/` (the supplier's root LICENSE and NOTICE, equal at 0.160.0 and
0.167.0), `codex-skills-086ccc83/` (the two skill samples embedded in
`bin/codex`), the ripgrep chain (`ripgrep-15.2.0/`, `pcre2-sys-0.2.10/`,
`pcre2-10.46/`, `sljit-e51eabbf/`) and the V8 stack behind
`bin/codex-code-mode-host` (`v8-15.2.124.1/` with V8's 16 `third_party/` LICENSE
files at the same revision, `rusty_v8-350c5a85/`, ICU, libc++, libc++abi,
llvm-libc, and highway, fast_float, simdutf, dragonbox, FP16 and abseil-cpp as
Codex's `third_party/v8` build files pin them). Each row's `below_root` says what
was examined below the root. The libc++ and libc++abi root texts point to
`CREDITS.TXT` and to licences in subdirectories. The two `CREDITS.TXT` are held at the
blobs the complete LLVM listings name and ship with their rows; the libc++, libc++abi
and llvm-libc subdirectory rows are covered because, as their `below_root` records, the
complete listings show no other licence-named file below the root (per-file terms are
not excluded). Which component is in which binary is the supplier's statement in its
source, not read from the binary.

The table is reviewed for 0.169.0 (proposed, pending an independent reading) from the
supplier's source at d32063f9 and the distribution record; of the distributed archive
only the two voice records were read. A committed text keeps the identity it was
received with and lists, under `also_at`, the same blob at the 0.169.0 revision where a
listing names it (the Codex root texts, the two skill samples and the rusty_v8 fork's
LICENSE). The libc++ and libc++abi `CREDITS.TXT` are held at the blobs the complete
LLVM listings name. The imagegen and openai-docs skill samples and the vendored
bubblewrap are open rows for texts not held.

## Voice records (`voice_records/<pin>/`, `voice.py`)

`sources.json` and `manifest.json` are byte-faithful copies of
`codex-resources/voice/sources.json` and `codex-resources/voice/manifest.json`, read as
two single members of the held 0.169.0 distribution archive after its size and digest
were checked. They are maintained checker inputs, not run evidence; the originals ship
inside the supplier tree, so the copies are not mapped into the package. These are the
supplier's own statements about its bundle: the libraries are not inspected and no
source archive was read. `coverage.py check --vendor DIR` and `coverage.py generate
--vendor DIR` apply the same comparison to an extracted tree's two files.

A voice row is a `components.json` row with a member or a supplier-tree text under
`codex-resources/voice/lib/`, `plugins/` or `licenses/` (`voice.is_voice`). The voice
folder's other files (the voice host, `NOTICE.md` and the two records) belong to the
Codex row. A voice row's `revision` is present and null: its source is the release URL
the supplier states. The conditions under which a voice row is covered, with their
tests, are the `voice_route` and "Every supplier row" rows of the table in
`../notices/README.md`.

Review duties (the reviewer of a change to `components.json`'s voice rows or to the
records):
- **Which licence file is which library's.** Neither record says. For each voice row,
  compare the name of each `supplier_tree_texts` file with the library its
  native-library entry names, and, where reading the held distribution archive is
  permitted, the file's own text.
- **Which member file is which library's.** Neither record lists a library's files:
  `sources.json` gives each entry's name, version, role, archive, root, URL, digest and
  provenance, and `manifest.json` gives digests by path. For each voice row, verify that
  each member belongs to that row's native-library entry, from the member file names
  (for example `libopus.0.dylib` for opus and `libz.1.dylib` for zlib), the
  distribution record and the 0.167.0 table reviewed in pull request 243.
- **The distribution record is the supplier's tree.** `CANONICAL_DISTRIBUTION.json` is
  bound by `coverage-review.json`; its truth is the review of the change that brought it.

## Supplier crates (`crates/`)

Every package the supplier's Codex lockfile (`codex-rs/Cargo.lock` at d32063f9) and
ripgrep 15.2.0's lockfile lock, with its notice or an explicit gap. The set is a
superset: a lockfile locks packages for every platform and feature, so some may not be
compiled into the macOS executables; which are is not established beyond the packages
recorded absent by declared target condition (below), and no resolver, Cargo or Bazel
is run.

- `locks/` holds the two lockfiles; `associations.json` binds each to its source
  revision by blob, gives each Git-sourced package's licence files at the locked
  revision (with the listing that names each blob, and the symbolic links resolved to
  them) and the workspace texts for path packages.
- `index.json` is made by `crates.py index` from the held archives through
  `crate_notices.py`, the notice-only route: the archive's SHA-256 equals the lockfile
  checksum before it is opened; its tar headers are inventoried without reading other
  members' contents; links, repeated or case-ambiguous names, traversal and unsupported
  types refuse; the members selected by name, at any depth, are the only contents read.
  A name-based selection does not show that no other file in a package carries its own
  terms.
- `texts/<sha256>` holds each crate text once (`crates.py extract`, which requires every
  archive to equal its index row); `packages.json`, generated by `crates.py generate`, is
  the shipped per-package account.
- `crates.py check` needs no archive and refuses the disagreements listed in the
  `crates.py` part of the table in `../notices/README.md`.

Each locked package has one standing:

- **`text`**: its texts ship, from one route: the archive's notice members; the App's
  copy of the same archive (`app_texts`); the publisher's licence files at the revision
  the archive's VCS record names (`registry_sources`); a Git-sourced package's files
  (`git_sources`); or a path package's workspace texts (`workspaces`).
- **`held`**: open for an owner licence reading. The 23 packages awaiting the owner's
  reading of the objc2 repository's `LICENSE.md` (a licensing overview) are a named list
  in `crates.py` (`HELD_FOR_READING`), by name, version and lockfile checksum. The
  overview text's digest identifies the text awaiting the reading (`awaiting_reading`
  on the row). No supplier reading is recorded here.
- **`gap`**: no text ships, with its reason from `gap_reasons` or the default reason.
- **`no-publisher-text`**: a licence is stated and no publisher text was found at the
  examined revision. It ships nothing and stays open until a text exists or the owner
  decides what may serve as its notice.
- **`not-in-macos-package`**: absent from `aarch64-apple-darwin` by declared target
  condition.

`text` and `not-in-macos-package` are the standings that do not hold the
compiled-dependencies component open (`../notices/README.md`).

Repository fields of `associations.json` other than `archive_repository` have the form
`https://github.com/<owner>/<repository>`, each of owner and repository one or more
letters, digits, `_`, `.` or `-`, neither of them `.` or `..`, with no `.git` suffix in any
letter case (`crates.canonical_form`, a check of form, not that such a repository
exists). `archive_repository` records what the
archive's own `Cargo.toml` states, or null. Where these values are compared with each
other or with a lock, the comparison is as written, except where `crates.repository_key`
is used: the objc2 guard in `crates.py` (which the App-text reading flag also applies),
the App's Cargo reading rule and the Codex membership of a compiled row in
`../notices/coverage.py`, and `archive_repository` against its association. Those
sites, with their tests, are in the table.

### Review duties by collection

- **`registry_sources`** (publisher texts), from held evidence (the checker reads neither
  the archives' metadata nor the listings):
  - *The archive's own record.* Read the archive the lockfile locks (through the archive
    map, checksum-verified) and confirm that its `.cargo_vcs_info.json` names the
    recorded revision and `path_in_vcs` (or has no `path_in_vcs` key where null is
    recorded), its `Cargo.toml` names the recorded repository, and both members' sizes
    and SHA-256 equal those recorded.
  - *The listing.* Open the saved listing of that repository and revision; confirm its
    SHA-256 is `response_sha256` and its entry count `entries`; confirm each text is the
    blob and size the listing names at `source_path`; and confirm the texts are the
    whole selection (the notice-named files of the package folder and of a licence
    folder directly below it, or of the root where the folder holds none).
  - *The identity.* Confirm each association's name, version and checksum belong
    together.
  - *A null `path_in_vcs`* (schemafy_core 0.5.2, schemafy_lib 0.5.2 and wasite 0.1.0):
    read the `path_basis` against the listing. The listing gives paths only, not the
    package each `Cargo.toml` declares, so the texts must be the selection of every
    folder holding a `Cargo.toml` file.

  `review_publisher_texts.py` is a reviewer's aid, not a CI check:

  ```sh
  python3 -I -B app/packaging/supplier_notices/review_publisher_texts.py --archives MAP.json --listings DIR
  ```

  `MAP.json` maps each `<name>-<version>.crate` to its archive, and `DIR` holds the saved
  listings. It reads each archive through `crate_notices.read_member` after its SHA-256
  equals the lockfile checksum, reading `.cargo_vcs_info.json` and `Cargo.toml` only. It
  compares the archive's stated values (a recorded null path must be a VCS record with no
  `path_in_vcs` key), the listing's blob and size at each selected path, the selection
  (for a null path, the listing must hold at least one `Cargo.toml` file, an entry of type
  blob, and each such folder must give the same selection) and the stored bytes. It does
  not read a `path_basis`, which is prose the reviewer reads against the listing. After
  its inputs load and its member reads verify, it reports one comparison per package,
  `OK` or `MISMATCH` with what differs; an input error ends the run before any package
  line. Its comparisons are
  tested on invented inputs (`test_the_reviewer_s_aid_compares_what_it_states` and the
  three tests after it in `app/tests/supplier_crate_notices_test.py`).
- **`app_texts`**: that each App text is the same archive's text in the App's own
  reviewed account (`../notices/transitive-index.json`, that crate and checksum).
- **`git_sources`** and **`workspaces`**: that each listing named states the recorded
  blob at the recorded path.
- **The objc2 holds** (`HELD_FOR_READING`): the list is code; an identity leaves it only
  with the owner's reading recorded.
- **`not_in_macos_package` and `manifests/`.** The parent manifests that declare each
  excluded package are committed byte for byte under `crates/manifests/`, each with an
  entry in `manifests` (size, SHA-256, Git blob, binding, the licence it states, its
  source and the notice it ships under). The account records which rule admitted each
  parent: socks5-protocol by rule (i), winsplit by rule (ii), and the four packages
  excluded through the three registry parent manifests (keyring 3.6.3,
  rustls-platform-verifier 0.7.0 and winapi 0.3.9) by having no inheritance
  (`test_each_exclusion_records_the_rule_that_admitted_it`). Rule (i): every inherited
  key is under a condition false for macOS. Rule (ii): the inherited keys equal in number
  the lockfile dependencies the manifest does not name explicitly, so none can be the
  excluded package (`crates.admission`). Review duties:
  - *Registry manifests*: that each is the `Cargo.toml` of the archive the lockfile
    locks: run `crates.py verify-manifests --archives MAP.json`, which takes the expected
    checksum from the lockfile and reads that member. CI does not hold the archives.
  - *Workspace manifests*: that each is the file at its path at the lockfile's revision:
    compare its Git blob and size with the saved recursive listing of `codex-rs` at that
    revision, which is not in the repository.
  - *Rule (ii)* rests on the lockfile recording every dependency the parent's manifest
    declares; the lockfile's binding to its revision is the review of `locks`.
- **`no_publisher_text` and `gap_reasons`**: that each reason states what the held files
  show (the saved listing at the examined revision, the files named) and decides no
  licence question; which terms apply, and whether they are met, is the owner's.
- **`locks` and `index.json`**: that each lockfile's blob is the source file's at the
  recorded revision, and that `index.json` is what `crates.py index` makes from the
  archives (CI does not hold them).

No resolver was run and nothing was read from the binaries.

`codex-0.160.0/scripts/codex_package/` keeps the received rg release selector.

## Association readers

The 0.167.0 readers below are kept as that pin's evidence. All three read retained inputs offline, execute nothing and draw no licence
conclusion. `--write DIR` / `--check DIR|FILE` compare against records the caller
keeps outside the repository; none is committed.

- `associate_0167.py` recomputes the Codex 0.167.0 root-text and inventory
  association from the canonical 0.167.0 tree, the frozen 0.160.0 tree and retained
  public metadata. It checks `codex/LICENSE` and `codex/NOTICE` against the
  `rust-v0.167.0` tree and reads its executables from the 0.167.0 record.
- `ripgrep_0167.py` recomputes the rg → ripgrep 15.2.0 → pcre2-sys → PCRE2/sljit
  association.
- `v8_0167.py` recomputes the code-mode-host V8-stack association.
- `observe.py` remains the 0.160.0 reader.

```sh
python3 -m pytest -q app/tests/supplier_notice_observations_test.py app/tests/supplier_notice_selectors_test.py \
  app/tests/supplier_crate_notices_test.py
PYTHONDONTWRITEBYTECODE=1 python3 app/packaging/supplier_notices/crates.py check
```
