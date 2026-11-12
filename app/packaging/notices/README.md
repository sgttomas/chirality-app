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

## What these checks withstand

They are operator-run checks on stable inputs. They are built so that a component
that was not accounted for, a text that was not verified, or a reading that was not
given cannot come out as covered, and so that drift and mistakes are caught. They are
not built to withstand someone with write access deliberately forging a consistent
account, table and review record together. The review record is a statement of what
was reviewed, bound to exact content; its truth rests on the review of the pull
request that changes it, not on the tool.

## What ships and where

| Inputs | Generator | Package path under `Contents/Resources/` |
| --- | --- | --- |
| Direct runtime dependencies and the App (`index.json`, `assets/`) | hand-kept, `check.py` | `third-party-notices/index.json`, `assets/` |
| Transitive runtime closure (`transitive-index.json`) | `transitive.py` | `third-party-notices/transitive-index.json` |
| Transitive texts (`transitive/<cargo or npm>/<package>/<version>/`) | `package_texts.py extract` | `third-party-notices/transitive/` |
| Supplier component texts (`../supplier_notices/`, listed in `components.json`, with what was examined below each root) | hand-kept table | `third-party-notices/supplier/` |
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

Rules `coverage.py` applies, whatever the tables say:

- **Joins** are by ecosystem, name and version; one version never receives another's text.
- **Owner readings.** The nine objc2-family crates ship the objc2 repository's root
  `LICENSE.md`, a licensing overview. A crate whose held text comes from that
  repository, or was received as an upstream text, is covered only by an owner
  reading in the closed form (`decided_by` owner, a date, an answer from the fixed
  set in `coverage.py` and that answer's exact words); otherwise it is pending, and
  never covered by another route. The owner's reading of 2026-11-12 is recorded in
  `coverage-inputs.json` and on each row. A reading for any other crate refuses.
- **Repository root texts** at the revision a crate names count as covered with that
  basis (the project's Agent 0 accepted them as mechanical matches), distinct from
  licence files inside the crate's archive.
- **Compiled programs.** For this distribution record, a regular file with an
  execute bit that is neither a `.dylib` library nor `.json` data is taken as a
  compiled program. The rule fits this record: executables plus `.dylib` members must
  equal the record's Mach-O count, and every one of them must belong to a component.
  It is not a general proof that a file is a compiled program. Each executable must
  belong to a `compiled-dependencies` component, and those stand uncovered in this
  change whatever the table says. The change that extracts their texts adds the rule
  for covering them: the supplier lockfile bound to the supplier's source commit, and
  every locked package with its own extracted text or a stated basis.
- **Supplier texts are bound to their component.** Each committed text records its
  repository and revision; a voice text is a member of the supplier tree with the
  record's digest. A component is covered only when each committed text's repository
  and revision equal the component's own, or the text is a named exception with its
  reason (pcre2-sys ships two texts blob-equal to its own, kept once under ripgrep).
- **Fonts** are covered only with recorded upstream evidence (package, integrity and
  a tarball member for every file and the licence); otherwise uncovered.
- **Reviewed inputs.** `../supplier_notices/components.json` and
  `coverage-inputs.json` are curated judgments, not facts a check can prove. The
  direct, transitive, font and SQLite indexes are made by generators from caches CI
  does not hold, so CI can check texts only against them. The declared pin's
  `CANONICAL_DISTRIBUTION.json` is bound too, because the account copies the voice
  licence digests from it. `coverage-review.json` binds those seven files' SHA-256
  and lists every supplier component with its standing, version, revision and exact
  texts, and `coverage.py` checks it first. The record states what a reviewer
  examined; it is not a proof. The reviewer of the pull request that changes any of
  those files updates it, after rerunning the cache-reading checks for a changed
  index. **A supplier pin move changes which distribution record is bound, so it
  must update `coverage-review.json` in the same change.**
- **Deferred rows.** `coverage.DEFERRED` lists the five supplier rows with no route
  to covered in this change (the Codex and rg compiled-in crates, and the libc++,
  libc++abi and llvm-libc texts their licences point to). They stand uncovered
  whatever the table or the review record says, and must stay in the table. The
  change that establishes one removes its id from that list.
- **Identities.** Every committed supplier text needs a non-empty repository and
  revision; an exception needs a non-empty reason. The Library content rows must
  match the source each bundle names in its own record (`MANIFEST.json`,
  `ROLE_SET_SOURCE_BINDING.json`).
- **Removals.** `generate` refuses to drop a component the committed account has
  unless `removed_components` in `coverage-inputs.json` states it with a reason;
  `check --base-account FILE` applies the same rule against an earlier account.
- **Bundled icons** declared in `tauri.conf.json` need a provenance entry
  (`app_assets`); one without stands uncovered.

## Limits

The account describes what the package is built to carry, from committed inputs;
it is not read from a built package, and Tauri's resource mapper has not been run
against the overlay here. A notice text is the publisher's text at the version or
revision named; the account decides no licence question except where an owner
reading is recorded. The upstream toml `LICENSE-APACHE` ends with a blank line;
its bytes are kept as published.
