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
entry, or two rows for one entry, refuses; nothing is collapsed. Neither record states
which licence file belongs to which library, so which tree text is a row's notice is a
curated association in `components.json`, reviewed and not checked. Only then is a voice row covered (PCRE2 in the
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

Each locked package has one standing.

- **`text`**: its texts ship, from exactly one route: the archive's notice members; the
  App's copy of the same archive (`app_texts`); or the publisher's licence files at the
  revision the archive's VCS record names (`registry_sources`).
- **`held`**: open for an owner licence reading. The 23 packages awaiting the owner's
  reading of the objc2 repository's `LICENSE.md` (a licensing overview) are a closed,
  named list in `crates.py` (`HELD_FOR_READING`), by name, version and lockfile checksum,
  not in the curated associations. A listed package stays held whatever text, repository
  spelling or route its row gives it. If its row does not carry the overview text, it
  stays held with a reason saying so: nothing in this change establishes another text
  for it. A listed identity that no lockfile locks refuses. The overview text's digest
  only identifies the text awaiting the reading (`awaiting_reading` on the row). As an
  independent guard, an unlisted package whose texts include the overview text, or
  whose repository is the objc2 repository, is held too. No supplier reading is recorded
  and none can be accepted here.
- **`gap`**: no text ships, with a specific reason from `gap_reasons`: the files each
  package waits on, or why its revision is not established.
- **`no-publisher-text`**: a licence is stated and no publisher text was found at the
  examined revision. It ships nothing and stays open until a text exists or the owner
  decides what may serve as its notice. Where a row records a further provenance question
  (crc32c's zlib notice, debugserver-types' schema, deno_core_icudata's ICU data), its
  `would_close` includes it.
- **`not-in-macos-package`**: absent from `aarch64-apple-darwin` by declared target
  condition (below).

Every repository field of every association must be exactly
`https://github.com/<owner>/<repository>`, with no `.git`, path or trailing slash.
Anything else refuses.

A `registry_sources` association is keyed by the archive's name, version and checksum,
and names the publisher repository and revision.

- Each package records:
  - the size and SHA-256 of the archive's `Cargo.toml` and `.cargo_vcs_info.json`;
  - the revision the VCS record names, which must equal the association's revision;
  - the repository the archive's manifest names (in any spelling of the same GitHub
    repository). An archive that names none needs the association's stated
    `repository_basis`, as for pagable_derive.
- The listing identity is required: `read`, `entries` and the response SHA-256.
- Each text:
  - must have a notice name by the rule the archive route uses, so a README refuses;
  - records the blob and size the saved listing of that revision gives;
  - must already be in `texts/` through another route with that blob. Nothing is
    received for it.

**Review boundary.** The tool cannot see the saved listings, the archives' metadata
files or the publisher's tree. A well-formed but wrong revision recorded consistently
in both places, another held text with consistent digests, or a lock identity moved
between associations is caught only by the review of `associations.json`, which
`coverage-review.json` binds. The tool does not prevent these.

### Absence from the macOS target (`not_in_macos_package`, `manifests/`)

The parent manifests that declare each excluded package's edges are committed byte for
byte under `crates/manifests/` as checker inputs. Each has an entry in
`associations.json` `manifests` with:
- its size, SHA-256, Git blob and binding;
- the licence the crate or repository declares;
- its source: a registry archive's `Cargo.toml` by crate, version, archive checksum and
  member path, or a workspace file by repository, revision and source path;
- the notice under which it ships, already in the account.
  - For keyring 3.6.3, rustls-platform-verifier 0.7.0 and winapi 0.3.9: the crate's own
    row must stand `text` with exactly the recorded licence texts.
  - For the two codex-rs files: the Codex workspace's root LICENSE and NOTICE.

`crates.py check` reads each committed manifest. It must be a regular file equal to its
recorded identity, and must be the locked archive's `Cargo.toml` (by checksum) or the
workspace file at the lockfile's repository and revision. The check parses the manifest
with `tomllib` and finds every declaration of the excluded package:
- in every dependency table (normal, dev and build);
- whether target-specific or not;
- by key or by `package =` rename.

Each declaration must sit under a target key that is false for `aarch64-apple-darwin`:
- `cfg(target_os = "...")`;
- `cfg(windows)`;
- a literal triple from the closed list `KNOWN_TRIPLES`.

Any other form refuses, and so does a declaration with no target condition.

The recorded reverse dependencies must equal the lockfile's exactly. The recorded edge
lines are a cross-check: each must equal the manifest's own lines, and together they
must equal the declarations found.

`crates.py verify-manifests --archives MAP.json` requires each committed registry
manifest to equal the `Cargo.toml` member of its checksum-verified archive. CI does not
hold the archives, so that binding is a reviewed input like the index. The workspace
manifests were read as pinned raw files at the full commit. Their blob and size equal
the recursive codex-rs listing at d32063f9, the listing that binds the lockfile; that
listing is not in the repository. No resolver was run and nothing was read from the
binaries.

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
