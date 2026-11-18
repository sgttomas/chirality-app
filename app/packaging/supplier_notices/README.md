# Supplier notice texts and associations

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
was examined below the root. Where a root text points to files that are not held
(libc++ and libc++abi `CREDITS.TXT`, and the LLVM subdirectory licences), that is
its own uncovered row. Which component is in which binary is the supplier's
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
inside the supplier tree, so the copies are not mapped into the package.
`notices/coverage.py` calls `voice.establish` on every generate and check: each copy
must be a regular non-link file whose size and SHA-256 equal its member in the declared
pin's `CANONICAL_DISTRIBUTION.json`; a repeated JSON key or another shape refuses; the
manifest's `buildCommit`, `appVersion` and targets must equal the record's source
commit, the pin and `aarch64-apple-darwin`, and every digest it lists must equal the
record's; and each voice row's version and source URL must be stated by exactly one
native-library entry of `sources.json`, with every such entry accounted for by one
row and each row's members and texts listed by the manifest. A repeated or conflicting
entry refuses; nothing is collapsed. Only then is a voice row covered (PCRE2 in the
voice bundle is 10.48 at 0.169.0, as the supplier states). These are the supplier's own
statements about its bundle, not an inspection of the libraries, and no source archive
was read. `coverage.py --vendor DIR` applies the same comparison to an extracted tree's
two files.

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
- `crates.py check` needs no archive and refuses any disagreement among them.

Each locked package has one standing. `text`: its texts ship, from exactly one route
(the archive's notice members; the App's copy of the same archive, `app_texts`; or the
publisher's licence files at the revision the archive's VCS record names,
`registry_sources`). A `registry_sources` association is keyed by the archive's name,
version and checksum and names the publisher repository, revision and paths; each text
records the blob and size the saved listing of that revision gives, and its bytes must
already be in `texts/` through another route with that blob (nothing is received for
it). A byte-identical text is reused only through that package's own source identity,
never by licence name. `held`: the resolved route's text comes from a repository that
needs an owner licence reading (`READING_REPOSITORIES`, the objc2 repository); the
requirement is applied after the route is resolved, so no route avoids it, and no
supplier reading is recorded. `gap`: no text ships, with a specific reason from
`gap_reasons` (the files each waits on, or why its revision is not established).
`no-publisher-text`: a licence is stated and no publisher text was found at the
examined revision; it ships nothing and stays open until a text exists or the owner
decides what may serve as its notice. `not-in-macos-package`: absent from
`aarch64-apple-darwin` by declared target condition (`not_in_macos_package`): the
recorded reverse dependencies must equal the lockfile's exactly, and each records the
manifest that declares its edge (a registry archive's `Cargo.toml`, by checksum, size
and SHA-256; a workspace manifest at the lockfile's repository and revision, by size,
blob and SHA-256) with the table and line. The table's condition must be one of
`cfg(target_os = "...")`, `cfg(windows)` or a literal target triple, and false for
macOS; any other form refuses, and absence is never inferred from a name. No resolver
was run and nothing was read from the binaries. An association naming a package it
cannot apply to (unlocked, another checksum, a package with a text route, or one named
twice) refuses.

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
