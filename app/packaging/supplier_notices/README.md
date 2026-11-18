# Supplier notice texts and associations

The checkers here (`crates.py`, `voice.py`, and `../notices/coverage.py` reading them) are
not built to resist deliberately forged, mutually consistent inputs: a listing entry, an
archive record, a manifest and a review record changed together to agree. The review of
the pull request that changes a curated file covers that boundary. Each curated
collection below lists what the checker enforces, with a test for each, and what its
reviewer must check from held evidence; a coverage decision that rests on a review duty
nobody has completed stays open. The by-site table in `../notices/README.md` (What is
enforced and what review covers) is the authority; these lists spell out its crate and
voice rows.

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
the old associations. Every committed text here is mapped into the package under
`third-party-notices/supplier/`; the voice libraries' licences ship inside the
supplier tree itself.

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
`CREDITS.TXT` and to licences in subdirectories: the two `CREDITS.TXT` are held at the
blobs the complete LLVM listings name and ship with those rows, and the complete
listings show no licence file below the root in the libc++, libc++abi or llvm-libc
subdirectories, so those rows are covered (per-file terms are not excluded). Which component is in which binary is the supplier's
statement in its source, not read from the binary.

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
source archive was read. `coverage.py --vendor DIR` applies the same comparison to an
extracted tree's two files.

A **voice row** is any `components.json` row with a member or text in the voice
library folders (`codex-resources/voice/lib/`, `plugins/` or `licenses/`), however the
row is written. The voice folder's other files (the voice host, `NOTICE.md` and the two
records) are the supplier's own and belong to its Codex row. Voice membership is decided
before any other route: a voice row cannot be a compiled-dependencies row, a reading row
or a deferred row, and a voice member belongs to one component. Only a voice row may
name `supplier_tree_texts`, and each must be under `codex-resources/voice/licenses/`.

Enforced (`coverage.py` with `voice.establish`, on every generate and check):
- each copy is a regular non-link file whose size and SHA-256 equal its member in the
  declared pin's `CANONICAL_DISTRIBUTION.json`;
- both records have exact JSON types and closed shapes (`true` is not the schema
  version 1), with no repeated key;
- the manifest's `buildCommit`, `appVersion` and targets equal the record's source
  commit, the pin and `aarch64-apple-darwin`, and every digest it lists equals the
  record's;
- each voice row is established by exactly one native-library entry of `sources.json`
  (its version and source URL), and every native-library entry establishes exactly one
  row; each row's members and texts are files the manifest lists. A repeated or
  conflicting entry, or two rows for one entry, refuses;
- a voice row is covered only then, only with texts from the supplier tree, and with
  its source statement on the account row. A voice row that names another text, a text
  exception or no tree text, or whose records are not held, stands uncovered;
- with `--vendor DIR`, `check_vendor` refuses any row with tree texts whose version is
  not the one the tree's `sources.json` states for its URL (`voice component differs
  from sources.json`), and also applies the comparison above to the tree's
  `sources.json` and `manifest.json`.

Review boundary (the reviewer of a change to `components.json`'s voice rows or to the
records):
- **Which licence file is which library's.** Neither record says. For each voice row,
  compare the name of each `supplier_tree_texts` file with the library its
  native-library entry names, and, where reading the held distribution archive is
  permitted, the file's own text.
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
- `crates.py check` needs no archive and refuses the disagreements listed below.

Each locked package has one standing.

- **`text`**: its texts ship, from exactly one route: the archive's notice members; the
  App's copy of the same archive (`app_texts`); the publisher's licence files at the
  revision the archive's VCS record names (`registry_sources`); a Git-sourced package's
  files (`git_sources`); or a path package's workspace texts (`workspaces`).
- **`held`**: open for an owner licence reading. The 23 packages awaiting the owner's
  reading of the objc2 repository's `LICENSE.md` (a licensing overview) are a closed,
  named list in `crates.py` (`HELD_FOR_READING`), by name, version and lockfile checksum.
  The overview text's digest only identifies the text awaiting the reading
  (`awaiting_reading` on the row). No supplier reading is recorded and none can be
  accepted here.
- **`gap`**: no text ships, with a specific reason from `gap_reasons`.
- **`no-publisher-text`**: a licence is stated and no publisher text was found at the
  examined revision. It ships nothing and stays open until a text exists or the owner
  decides what may serve as its notice.
- **`not-in-macos-package`**: absent from `aarch64-apple-darwin` by declared target
  condition.

`text` and `not-in-macos-package` are the only standings that do not hold the
compiled-dependencies component open (`../notices/README.md`).

### What `crates.py check` enforces for every collection

`associations.json` is loaded once through one typed shape check
(`crates.ASSOCIATIONS_SHAPE`), before any other use, and refuses:
- a value of another Python type: a string must be a `str`, a size or count a positive
  `int` and never a `bool`, a digest a `str` of its hexadecimal pattern;
- a missing or unknown key, an empty list or string where one is required;
- a repository field not exactly `https://github.com/<owner>/<repository>` (no `.git` in
  any letter case, no path and no trailing slash);
- a repeated lock id, lock component, workspace lock, manifest id or manifest path, and a
  workspace entry that names no lock (no keyed collection lets a later entry win);
- a repository-relative path that is empty, absolute, or has a backslash or an empty,
  `.` or `..` segment (the archive route's member rule, `crate_notices.safe_relative`).

Every repository comparison in `crates.py` and `../notices/coverage.py` goes through
one function, `crates.repository_key`: two GitHub repositories are the same when their
owner and name are equal without regard to case, ignoring a `.git` suffix and any path.

Across collections, a package named twice, named by an association that applies to no
locked package with that name, version and checksum, given two text routes, or given a
text route and an open or absent standing, refuses.

### `registry_sources`: publisher texts (can make a package `text`)

Enforced:
- the package's recorded archive VCS revision equals the association's revision;
- the archive's recorded repository is the same GitHub repository (compared without
  regard to case), or the archive names none and the association states its
  `repository_basis`;
- `path_in_vcs` is a folder or `""` for the root, or `null` where the archive's VCS
  record states none, and then only with `path_basis` (what the listing shows and which
  folder's selection the texts are);
- each text's path is a notice name by the archive route's rule (a README refuses);
- each text's blob and size equal the recorded listing entry, and its bytes are already
  in `texts/` through another route with that blob;
- the objc2 holds below.

Review boundary (from held evidence; the tool reads neither the archives' metadata nor
the listings):
- **The archive's own record.** Read the archive the lockfile locks (through the archive
  map, checksum-verified) and confirm that its `.cargo_vcs_info.json` names the recorded
  revision and `path_in_vcs` (or states none where `null` is recorded), its `Cargo.toml`
  names the recorded repository, and both members' sizes and SHA-256 equal those
  recorded.
- **The listing.** Open the saved listing of that repository and revision; confirm its
  SHA-256 is `response_sha256` and its entry count `entries`; confirm each text is the
  blob and size the listing names at `source_path`; and confirm the texts are every file
  the selection takes (the notice-named files of the package folder, or of the root
  where the folder holds none), so none is left out.
- **The identity.** Confirm each association's name, version and checksum belong
  together (an identity moved between associations stays well-formed).
- **Where `path_in_vcs` is `null`** (schemafy_core 0.5.2, schemafy_lib 0.5.2 and wasite
  0.1.0 at present), confirm the `path_basis`. The listing gives folder names and file
  paths only, not the package each `Cargo.toml` declares, so the texts must be the
  selection of every folder holding a `Cargo.toml`.

`review_publisher_texts.py` is a reviewer's aid, not a CI check. It reproduces these
comparisons for every `registry_sources` package and prints one line each, `OK` or
`MISMATCH` with what differs:

```sh
python3 -I app/packaging/supplier_notices/review_publisher_texts.py --archives MAP.json --listings DIR
```

`MAP.json` maps each `<name>-<version>.crate` to its archive, and `DIR` holds the saved
listings. Each archive is read through `crate_notices.read_member` only after its SHA-256
equals the lockfile checksum, and only `.cargo_vcs_info.json` and `Cargo.toml` are read.
Nothing is extracted, executed or fetched. CI holds neither the archives nor the
listings.

### `app_texts`, `git_sources`, `workspaces` (can make a package `text`)

Enforced: the shape; for `app_texts`, the locked identity, a single route and
`reading_required` equal to the objc2 rule; for `git_sources`, the lock's repository and
revision, and each text's blob equal to its listing blob and to the stored bytes; for
`workspaces`, each text's bytes equal to its identity and its blob in the listing's.
Review boundary: that each App text is the same archive's text in the App's own
reviewed account, and that each listing names the recorded blob at the recorded path.

### The objc2 holds (`HELD_FOR_READING`, can only keep a package open)

Enforced: a listed package stays held whatever text, repository spelling or route its
row gives it, and is never covered by substitution (with another text, or none, it stays
held and the reason says what it carries); a listed identity no lockfile locks refuses;
after every route (archive, App text, publisher text, Git and workspace), an unlisted
package whose texts include the overview text is held, and so is one whose route gives a
repository that is the objc2 repository in any letter case. An archive row carries no
repository, so on the archive route only the text digest guards it. Review boundary: the list is code; an identity
leaves it only with the owner's reading recorded.

### `not_in_macos_package` and `manifests/` (can exclude a package)

The parent manifests that declare each excluded package are committed byte for byte
under `crates/manifests/`. Each has an entry in `manifests` with its size, SHA-256,
Git blob, binding, the licence it states, its source (a registry archive's `Cargo.toml`
by crate, version, archive checksum and member path, or a workspace file by repository,
revision and source path) and the notice it ships under.

Enforced:
- the recorded reverse dependencies equal the lockfile's exactly, and the entry's
  lockfile is the one being read;
- each manifest is a regular file equal to its recorded identity, is cited by a reverse
  dependency, names that package, and is the locked archive's `Cargo.toml` (by name,
  version and lockfile checksum) or the workspace file at the lockfile's repository and
  revision;
- the manifest is parsed with `tomllib`. Every explicit declaration of the package, in
  every dependency table (normal, dev and build; target-specific or not; by key or by
  `package =`), must sit under a target key false for `aarch64-apple-darwin`: one of
  `cfg(target_os = "...")`, `cfg(windows)` or a literal triple from `KNOWN_TRIPLES`. Any
  other form, or no condition, refuses;
- a registry manifest that uses workspace inheritance (`workspace = true`) refuses. For a
  workspace member, whose inherited keys name their packages only in the root manifest
  (not held), the exclusion stands only by rule (i), every inherited key under a
  condition false for macOS, or rule (ii), the inherited keys equal in number the
  lockfile dependencies the manifest does not name explicitly, so none can be the
  excluded package (the argument is in `crates.admission`). Otherwise it refuses, saying
  the root manifest would be needed. The account records which rule admitted each
  parent: socks5-protocol by (i), winsplit by (ii), the four registry parents' packages
  by having no inheritance;
- the recorded declarations equal those the parse finds; cited lines are not accepted;
- the recorded licence equals what the manifest states (or says it is inherited from
  the workspace when it is); a registry manifest's notice names its own crate, whose row
  stands `text` with exactly the recorded texts; a workspace manifest's notice is its
  workspace's texts.

Review boundary:
- **Registry manifests.** That each is the `Cargo.toml` of the archive the lockfile
  locks: run `crates.py verify-manifests --archives MAP.json`, which takes the expected
  checksum from the lockfile and reads only that member. CI does not hold the archives.
- **Workspace manifests.** That each is the file at its path at the lockfile's revision:
  compare its Git blob and size with the saved recursive listing of `codex-rs` at that
  revision. The listing is not in the repository.
- **Rule (ii)** rests on the lockfile recording every dependency the parent's manifest
  declares, which holds for the supplier's own lockfile at the same revision; the
  lockfile's binding to that revision is the review of `locks`.

No resolver was run and nothing was read from the binaries.

### `no_publisher_text` and `gap_reasons` (open; cannot cover)

Enforced: the shape, the locked identity, and that no such package also has a text
route or another standing; both standings are open, so `--strict` and a public
production preparation refuse while any remains. Review boundary: that each reason
states what the held files show (the saved listing at the examined revision, the files
named) and decides no licence question; which terms apply, and whether they are met, is
the owner's.

### `locks` and `index.json`

Enforced: each lockfile equals its recorded identity, and the index has exactly the
locked registry packages. Review boundary: that each lockfile's blob is the source
file's at the recorded revision, and that `index.json` is what `crates.py index` makes
from the archives (CI does not hold them).

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
