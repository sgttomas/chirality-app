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
The candidate checker binds the release standing to a faithfully generated plan;
it does not independently defend the notice gap count or the coverage digest
against a consistent forgery of the candidate and plan. The recorded date and
relay of an owner reading are bound by the curated review record.

## What ships and where

| Inputs | Generator | Package path under `Contents/Resources/` |
| --- | --- | --- |
| Direct runtime dependencies and the App (`index.json`, `assets/`) | hand-kept, `check.py` | `third-party-notices/index.json`, `assets/` |
| Transitive runtime closure (`transitive-index.json`) | `transitive.py` | `third-party-notices/transitive-index.json` |
| Transitive texts (`transitive/<cargo or npm>/<package>/<version>/`) | `package_texts.py extract` | `third-party-notices/transitive/` |
| Supplier component texts (`../supplier_notices/`, listed in `components.json`, with what was examined below each root) | hand-kept table | `third-party-notices/supplier/` |
| Supplier crate texts (`../supplier_notices/crates/texts/<sha256>`) and the per-package account (`crates/packages.json`) | `../supplier_notices/crates.py` | `third-party-notices/supplier/crates/` |
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
- **ICU** is covered only by the owner's licence reading of 2026-11-15, recorded on
  its row in `../supplier_notices/components.json` in the closed form
  `coverage.SUPPLIER_READINGS` fixes: the question as put, the answer the owner
  selected ("ICU's licence text as published is complete") and that answer's
  description, exactly, with the decider, date and relay. Without it, or with any
  other words, ICU is pending. Nothing is added to the ICU notice. The row's
  `reading_context` keeps the facts examined; the two files' build-system status is as
  the answer's description states it, not established here. A reading for any other
  supplier row refuses.
- **Repository root texts** at the revision a crate names count as covered with that
  basis (the project's Agent 0 accepted them as mechanical matches), distinct from
  licence files inside the crate's archive.
- **Compiled programs.** For this distribution record, a regular file with an
  execute bit that is neither a `.dylib` library nor `.json` data is taken as a
  compiled program. The rule fits this record: executables plus `.dylib` members must
  equal the record's Mach-O count, and every one of them must belong to a component.
  It is not a general proof that a file is a compiled program. Each executable must
  belong to a `compiled-dependencies` component. Such a component is covered only by
  the supplier crate group (`../supplier_notices/crates.py`): its lockfile, bound by
  blob to the component's own repository and revision (the Codex lockfile to the
  distribution record's source commit), and every package that lockfile locks with its
  text. A package with no text (`gap`), one that states a licence for which no
  publisher text was found (`no-publisher-text`), or one awaiting an owner reading
  (`held`) keeps the component open, and the account names each such package; none of
  them ever counts as covered, so `--strict` and a public preparation refuse while any
  remains. The lockfiles are a superset: they lock packages for every platform and
  feature, and some may not be compiled into the macOS executables. The only package
  left out of what the component needs is one standing `not-in-macos-package`: absence
  from the macOS target (`aarch64-apple-darwin`) by declared target condition. It is
  admitted only when every reverse dependency the lockfile gives has its manifest
  committed under `../supplier_notices/crates/manifests/`, and every declaration of the
  package that the checker finds by parsing that manifest sits under a target key, in a
  closed set of forms, that is false for that target (see
  `../supplier_notices/README.md`). No resolver was run and nothing was read from the
  binaries; the account lists every such package with its evidence under
  `excluded_packages`. Nothing is left out on any other ground. The 23 packages awaiting
  the owner's objc2 reading are a closed, named list in `crates.py` and stay held whatever
  route, spelling or text their rows give them. The table's standing for the component
  must agree.
- **Voice rows.** A voice row (a component whose texts are members of the supplier
  tree) is covered only when the supplier's own voice records for the declared pin,
  committed under `../supplier_notices/voice_records/<pin>/` and bound to their members'
  digests in the distribution record, establish its version and source URL
  (`../supplier_notices/voice.py`; any disagreement refuses, and each native-library
  entry establishes exactly one row). These are the supplier's statements about its
  bundle; the libraries' contents are not inspected. Which licence file in the tree is a
  row's notice is not stated by those records; it is curated in `components.json` and
  reviewed, not checked.
- **Table reviewed for another pin.** When the declared pin differs from the table's
  `reviewed_for_pin`, no association is carried forward: every table row stands
  uncovered (the deferred rows with their own reason), and a "Supplier component
  table" row names the vendor tree. Re-associating the table for the declared pin is a
  reviewed change to `components.json` that sets `reviewed_for_pin`, updates
  `coverage-review.json` and states the open table row's removal in
  `removed_components`.
- **Supplier texts are bound to their component.** Each committed text records its
  repository and revision, and may record `also_at` identities: the same blob at another
  repository and revision, each with the listing that names it; a voice text is a member of the supplier tree with the
  record's digest. A component is covered only when each committed text's repository
  and revision equal the component's own, or the text is a named exception with its
  reason (pcre2-sys ships two texts blob-equal to its own, kept once under ripgrep).
- **Fonts** are covered only with recorded upstream evidence (package, integrity and
  a tarball member for every file and the licence); otherwise uncovered.
- **Reviewed inputs.** `../supplier_notices/components.json` and
  `coverage-inputs.json` are curated judgments, not facts a check can prove, as is
  `../supplier_notices/crates/associations.json`; `crates/index.json` is made from
  archives CI does not hold, and the committed registry parent manifests' equality with
  their archives' `Cargo.toml` is checked only by `crates.py verify-manifests` with the
  archives. The
  direct, transitive, font and SQLite indexes are made by generators from caches CI
  does not hold, so CI can check texts only against them. The declared pin's
  `CANONICAL_DISTRIBUTION.json` is bound too, because the account copies the voice
  licence digests from it. `coverage-review.json` binds those nine files' SHA-256
  and lists every supplier component with its standing, version, revision and exact
  texts, and `coverage.py` checks it first. The record states what a reviewer
  examined; it is not a proof. The reviewer of the pull request that changes any of
  those files updates it, after rerunning the cache-reading checks for a changed
  index. **A supplier pin move changes which distribution record is bound, so it
  must update `coverage-review.json` in the same change.**
- **Deferred rows.** `coverage.DEFERRED` lists supplier rows with no route to
  covered, whatever the table or the review record says; each must stay in the table.
  It is empty at 0.169.0: the five rows it held for 0.167.0 were each established and
  removed (the two crate groups by the lockfile, index and text correspondence above,
  the libc++ and libc++abi CREDITS texts at their listed blobs, and those two and
  llvm-libc's subdirectories by complete listings with no licence file below the root;
  per-file terms are not excluded). A row with no route is added back here.
- **Identities.** Every committed supplier text needs a non-empty repository and
  revision; an exception needs a non-empty reason. Each supplier component's own
  identity is checked before its texts or exceptions: a component with committed
  texts needs its repository and revision, and one with supplier-tree texts needs the
  source URL the supplier's `sources.json` states (no revision is recorded for those,
  and none is invented); otherwise it stands uncovered. The Library content rows must
  match the source each bundle names in its own record (`MANIFEST.json`,
  `ROLE_SET_SOURCE_BINDING.json`), whose digest `coverage-inputs.json` records.
- **Removals.** `generate` refuses to drop a component the committed account has
  unless `removed_components` in `coverage-inputs.json` states it with a reason;
  `check --base-account FILE` applies the same rule against an earlier account.
- **Every bundle mapping is named, exactly.** The mappings are read, not listed:
  what a production preparation selects (`../production_inputs/bundle_resources.py`,
  which `prepare.py` uses: the resources of `app/src-tauri/tauri.conf.json`, both
  overlays, the SQLite and font notices), plus the two it adds from its inputs, the
  vendor tree at `codex/` and an explicitly selected supplement under
  `third-party-notices/upstream/`. Each mapping must be named by its exact source and
  destination: in a row's `mappings`, or as the repository path and package path of a
  text a row ships. A destination folder names nothing below it. A folder mapping is
  named only with a membership record: each Library bundle's folder must hold exactly
  the files its reviewed source record lists, with their digests (an added, changed or
  missing file leaves the row uncovered), and the vendor tree's members are the
  distribution record's. The App's own content is named in `app_resources` by exact
  file mappings, with the App's licence as its notice; the account binds those paths,
  not their bytes. A mapping no row names becomes an uncovered "Unnamed bundle
  resource" row, which `--strict` names and a public preparation refuses; a claim on a
  mapping that does not exist refuses. `prepare.py` requires every mapping of its
  final plan to be named the same way. A change that maps a new resource adds its row
  in the same change (the shipped limitations list needs an `app_resources` entry
  naming `docs/RELEASE_LIMITATIONS_4.0.0.md` to `release/LIMITATIONS.md`, and a
  review-record update).
- **Copy routes.** Only `bundle.resources` (as an object) and `bundle.icon` are
  supported in the base configuration. A platform or alternate Tauri configuration
  beside `tauri.conf.json` (`tauri.macos.conf.json`, `Tauri.toml`,
  `tauri.conf.json5` and the like, which the bundler would merge or read instead), or
  any other `bundle` or `bundle.macOS` key (such as `macOS.files`, `macOS.frameworks`
  or `externalBin`), refuses rather than being accounted for. `prepare.py` merges its
  plan into the base as the bundler does and requires the same, allowing
  `bundle.macOS.files` only for the validated provisioning profile of a production
  plan, which is the publisher's Apple-issued file and is not a notice component.
  Frontend assets the build embeds in the executable are not a copy route; the fonts
  among them have their own rows.
- **Bundled icons** declared in `tauri.conf.json` need a provenance entry
  (`app_assets`); one without stands uncovered.

## Limits

The account describes what the package is built to carry, from committed inputs;
it is not read from a built package, and Tauri's resource mapper has not been run
against the overlay here. A notice text is the publisher's text at the version or
revision named; the account decides no licence question except where an owner
reading is recorded. The upstream toml `LICENSE-APACHE` ends with a blank line;
its bytes are kept as published.
