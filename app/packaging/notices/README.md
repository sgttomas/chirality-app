# Notices the macOS arm64 package ships

Every component shipped in the package has an entry in `coverage.json`, with its
version, its source, where its notice text ships and one standing: `covered`,
`held-pending-owner-licence-reading` or `uncovered` (with the reason and what
would close it). `coverage.py check --strict` exits non-zero while any component is
not covered, naming each. `production_inputs/prepare.py` records the account's
digest and counts in every plan and refuses a production plan while the strict
check fails, unless `--not-for-public-release` names the plan as not for public
release, which the plan then states.

From the repository root (Python 3.11+, no additional packages):

```sh
PYTHONDONTWRITEBYTECODE=1 python3 app/packaging/notices/coverage.py check            # reporting
PYTHONDONTWRITEBYTECODE=1 python3 app/packaging/notices/coverage.py check --strict   # refuses open components
PYTHONDONTWRITEBYTECODE=1 python3 app/packaging/notices/coverage.py generate         # after any input changes
```

`check` regenerates the account and requires the committed file to be identical; it
runs the direct, transitive, shipped-text and font checks on the way. No cache,
supplier tree or network is read.

## What ships and where

| Inputs | Generator | Package path under `Contents/Resources/` |
| --- | --- | --- |
| Direct runtime dependencies and the App (`index.json`, `assets/`) | hand-kept, `check.py` | `third-party-notices/index.json`, `assets/` |
| Transitive runtime closure (`transitive-index.json`) | `transitive.py` | `third-party-notices/transitive-index.json` |
| Transitive texts (`transitive/<cargo or npm>/<package>/<version>/`) | `package_texts.py extract` | `third-party-notices/transitive/` |
| Supplier component texts (`../supplier_notices/`, listed in `components.json`) | hand-kept table | `third-party-notices/supplier/` |
| Coverage account (`coverage.json`) | `coverage.py generate` | `third-party-notices/coverage.json` |
| Font licences and SQLite notice | `../font_notice/`, `../sqlite_notice/` | `third-party-notices/fonts/`, `sqlite-preparation/` (mapped by `prepare.py`) |
| Voice library licences | the supplier ships them in its tree | `codex/codex-resources/voice/licenses/` |

`../unsigned/tauri.notices.conf.json` is written by `package_texts.py overlay`: the
development configuration plus every resource above except fonts, SQLite and the
vendor tree. `check.py` refuses an overlay that differs. Ordinary routes do not map
notices.

## Transitive texts

`transitive.py` records the target- and feature-selected runtime graph (Cargo
`aarch64-apple-darwin`, release features, normal edges, no proc-macros) and the
npm runtime closure of `package-lock.json`. Its npm rows are derived from the
locked tarballs:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 app/packaging/notices/transitive.py associate-npm --npm-cache /absolute/npm-cache-root
```

`package_texts.py extract` reads each locked `.crate` file from a Cargo cache folder
(the one holding `<name>-<version>.crate`), requires its SHA-256 to equal
`Cargo.lock`, takes exactly the notice members the index names and requires each
to match the index; npm members come from the locked tarball, checked against its
lock integrity. Held texts are copied from their committed files after their
digests are checked: `retained/` (unchanged evidence), the direct assets the root
associations name, and `received/`, which holds texts fetched with the owner's
permission and listed in `coverage-inputs.json` with repository, revision, URL,
size and digests. Each received text must be at the revision its crates name, or
be the root blob the retained root metadata names at that revision. Extraction
only reads the caches; it never runs Cargo or npm.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 app/packaging/notices/package_texts.py extract \
  --cargo-cache "$CARGO_HOME/registry/cache/index.crates.io-1949cf8c6b5b557f" --npm-cache /absolute/npm-cache-root
PYTHONDONTWRITEBYTECODE=1 python3 app/packaging/notices/package_texts.py overlay
```

For any other lockfile, `package_texts.py crates --lock L --cargo-cache DIR --out NEW_DIR
--rows ROWS.json` extracts the root notice members of every registry package the lock
names (archives verified against the lock) and writes one row per package:
`archive-member`, `missing` (with the repository and revision the archive names) or
`not-in-registry` for Git- and path-sourced packages.

## Standings

The nine objc2-family crates ship the objc2 repository's root `LICENSE.md`, a
licensing overview with no copyright line. They stand covered on the owner's
licence reading of 2026-11-12, recorded in `coverage-inputs.json` and on each row;
no other component rests on that reading. The account says for each covered row
whether its text is a licence file of the locked archive, a root text of the
repository at the revision the crate names, or that reading.

## Limits

The account describes what the package is built to carry, from committed inputs;
it is not read from a built package, and Tauri's resource mapper has not been run
against the overlay here. A notice text is the publisher's text at the version or
revision named; the account decides no licence question except where an owner
reading is recorded. The upstream toml `LICENSE-APACHE` ends with a blank line;
its bytes are kept as published.
