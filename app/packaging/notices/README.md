# Notices the macOS arm64 package ships

These checks are not built to resist deliberately forged, mutually consistent inputs
(an account, a table, an association and a review record changed together to agree).
The review of the pull request that changes a curated file covers that boundary
([What these checks withstand](#what-these-checks-withstand)). [What is enforced and
what review covers](#what-is-enforced-and-what-review-covers) lists, site by site, what
the checkers enforce, with the test for each, and what review covers.

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
  distribution record's source commit), and every package that lockfile locks standing
  `text` or `not-in-macos-package` (absence from `aarch64-apple-darwin` by declared
  target condition). A package standing `gap`, `no-publisher-text` or `held` keeps the
  component open, and the account names each such package. The lockfiles are a
  superset: they lock packages for every platform and feature, and some may not be
  compiled into the macOS executables. The table's standing for the component must
  agree. The conditions, with their tests, and the review duty of which executable is
  built from which lockfile, are under [What is enforced and what review
  covers](#what-is-enforced-and-what-review-covers).
- **Voice rows.** A voice row is a component with a member or a supplier-tree text
  under the voice library folders of the supplier tree (`codex-resources/voice/lib/`,
  `plugins/`, `licenses/`; `voice.is_voice`). It is covered only
  through the supplier's own voice records for the declared pin, committed under
  `../supplier_notices/voice_records/<pin>/`, with its licence texts from the supplier
  tree. The conditions, with their tests, and the review duties are under [What is
  enforced and what review covers](#what-is-enforced-and-what-review-covers).
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
  their archives' `Cargo.toml` is checked by `crates.py verify-manifests` with the
  archives (the expected checksum taken from the lockfile;
  `test_archive_reading_mode_takes_the_checksum_from_the_lockfile`), which `check` does
  not read. The
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

## What is enforced and what review covers

This section lists, site by site, how a standing can move toward covered: each place in
`coverage.py` where a component can be added as covered, and each place in
`../supplier_notices/crates.py` where a locked package can become `text` or
`not-in-macos-package`. Each condition carries one mark:

- **E**: the checker enforces it, and the named test changes that input and sees the refusal
  or the open standing;
- **C**: the code checks it, and no test in these suites changes that input alone;
- **R**: a review duty of the reviewer of the pull request that changes the curated input.

These apply to every site:

| Condition | Mark | Test or duty |
|---|---|---|
| Each curated file `coverage-review.json` names has its bound SHA-256 | E | `test_curated_input_changes_refuse_without_the_review_record` |
| Rebinding the review record after a change | R | the reviewer of the change rebinds it |
| `check` regenerates the account and requires the committed one unchanged | E | `test_stale_account_refuses` |
| A component that is not covered makes `check --strict` exit 1, naming it | E | `test_strict_mode_exits_non_zero_naming_each_open_component` |
| A component that is not covered refuses a public production plan | E | `production_inputs_test.py` `test_production_plan_refuses_open_notice_coverage_unless_named_not_for_public_release` |

### `coverage.py`: where a component is added as covered

| Site | Condition | Mark | Test or duty |
|---|---|---|---|
| App row | its notice bytes equal the direct index's | E | `notice_resources_test.py` `test_changed_notice_bytes_refuse` |
| App row | its notice is mapped into the package | C | `shipped` in `build` |
| App row | the App's licence is its notice | R | pre-existing curated judgment |
| App icons | a declared icon without a provenance entry stands uncovered | E | `test_bundled_icon_needs_provenance` |
| App icons | the icon's bytes equal the entry's SHA-256 and size | E | `test_bundled_icon_needs_provenance` |
| App icons | the entry's provenance is true | R | pre-existing; from the repository history at `added_by_commit` |
| Library content | the bundle's record names the entry's revision | E | `test_library_content_must_match_its_bundle_source_record` |
| Library content | the bundle's record has its reviewed digest | E | `test_an_added_or_changed_file_in_a_bundled_library_folder_is_open` |
| Library content | the folder holds exactly the record's members, or the row stands uncovered | E | `test_an_added_or_changed_file_in_a_bundled_library_folder_is_open` |
| Library content | the licence digest equals the App's `LICENSE.md`; the record lies inside the bundle; for workflow manifests, its repository and licence equal the entry's as written; a role-set binding contributes its basis commit | C | `build` |
| Library content | the record's source is the Library's at that revision | R | pre-existing; the review of the change that bundled it |
| Cargo row needing a reading | a row with a received upstream text, or whose text's repository is the objc2 repository, is covered only by a reading in the closed form, and otherwise stands held | E | `test_a_pending_or_missing_reading_is_pending_and_strict_refuses` |
| Cargo row needing a reading | the objc2 repository is matched in any letter case | C | `READING_REQUIRED_REPOSITORIES` with `same_repository` |
| Cargo row needing a reading | a reading for a crate that needs none refuses | E | `test_a_reading_cannot_be_extended_to_a_crate_that_needs_none` |
| Cargo row needing a reading | the reading's date and relay | R | bound by the review record |
| Cargo archive-member row | the transitive index's kind agrees with the row's members | E | `notice_transitive_test.py` `test_text_kind_must_match_members_and_received_text` |
| Cargo archive-member row | the shipped texts equal the planned tree | E | `test_changed_missing_extra_or_linked_text_refuses` |
| Cargo archive-member row | the index is what the generator makes from the archives | R | rerun `transitive.py check --cargo-home` |
| Cargo root-text row | a received text is at the revision its crates name, or is the root blob the retained root metadata names at that revision, with its committed bytes | E | `test_received_text_must_be_at_the_revision_its_crate_names` |
| Cargo root-text row | a root row keeps its revision, unresolved list, kind and licence | E | `notice_transitive_test.py` `test_root_row_cannot_choose_path_revision_scope_or_downgrade` |
| Cargo root-text row | a crate not on the root list cannot take a root association | E | `notice_transitive_test.py` `test_unlisted_crate_cannot_inherit_root_association` |
| Cargo root-text row | the root text at the named revision is the crate's notice | R | pre-existing; the project's Agent 0 accepted them as mechanical matches |
| npm row | unknown npm text kinds refuse; only `direct-index-archive` and `lock-tarball` can yield covered | E | `notice_transitive_test.py` `test_cargo_text_kinds_cannot_hide_unverified_npm_packages` |
| npm row | the index is what the generator makes from the tarballs | R | rerun `transitive.py check --npm-cache` |
| Font row | with the upstream evidence removed, each family stands uncovered | E | `test_unverified_fonts_are_uncovered` |
| Font row | altered upstream evidence in the font index refuses | E | `font_notice_test.py` `test_index_shape_provenance_and_notice_list_refuse` |
| Font row | the index is what the generator makes from the tarballs | R | rerun `font_notice/check.py --npm-cache` |
| SQLite | the header text's bytes equal its index asset | C | `build` (`SQLite notice bytes differ`) |
| SQLite | the header is the public-domain dedication | R | pre-existing; rerun `sqlite_notice/check.py --archive` |
| Every supplier row | a table reviewed for another pin covers no row, and an open table row is added | E | `test_a_table_reviewed_for_another_pin_covers_no_supplier_row`, `test_another_declared_pin_is_named_as_an_open_review_not_assumed` |
| Every supplier row | a row in `DEFERRED` stays uncovered | E | `test_deferred_rows_stay_uncovered_whatever_the_table_says` |
| Every supplier row | when the table is reviewed for the declared pin, each member is a file of the distribution record | E | `test_supplier_table_must_claim_every_member_and_justify_gaps` |
| Every supplier row | when the table is reviewed for the declared pin, each supplier-tree text is a file of the distribution record | C | `build` |
| Every supplier row | when the table is reviewed for the declared pin, each file of the distribution record is claimed by a row | E | `test_supplier_table_must_claim_every_member_and_justify_gaps` |
| Every supplier row | the distribution record repeats no file | E | `test_a_distribution_record_that_repeats_a_file_refuses` |
| Every supplier row | the distribution record has its bound digest | E | `test_distribution_record_drift_refuses` |
| Every supplier row | component ids and text paths do not repeat | E | `test_a_repeated_supplier_identifier_refuses` |
| Every supplier row | a committed text is a repository file whose bytes equal the size and digests the table records; the table is bound by the review record | C | `package_texts.supplier_texts` (`committed text differs`) |
| Every supplier row | every non-voice repository field of the component table (components, texts, also_at) is either `https://github.com/<owner>/<repository>`, each of owner and repository one or more letters, digits, `_`, `.` or `-`, neither of them `.` or `..`, with no `.git` suffix in any letter case, or begins with exactly `https://chromium.googlesource.com/`; anything else refuses, naming the field (for example `texts[<path>].also_at[0].repository`). This is a check of form, not that such a repository exists. The googlesource values are compared exactly wherever they are compared and are otherwise not constrained in form. A null or missing field is not a form and is left to main's checks: a text's or also_at identity's refuses, a component's null repository goes to its identity and lock checks (a row with committed texts stays uncovered), and a component's missing key stops the build with a KeyError | E | `test_a_repository_field_has_one_of_the_two_accepted_forms` |
| Every supplier row | a voice row's `revision` key is present and null; an absent key refuses before the review record's entries are read, and any value refuses after the voice-route checks | E | `test_a_supplier_tree_row_needs_its_source_url_but_no_invented_revision` |
| Every supplier row | a row with a member or a supplier-tree text under `codex-resources/voice/lib/`, `plugins/` or `licenses/` (a voice row) cannot be compiled-dependencies or a reading row | E | `test_a_voice_member_takes_only_the_voice_route` |
| Every supplier row | nor deferred, nor carry an owner reading | C | `build` |
| Every supplier row | a voice member belongs to one component | E | `test_a_voice_member_takes_only_the_voice_route` |
| Every supplier row | only a voice row names supplier-tree texts, each under `codex-resources/voice/licenses/` | E | `test_supplier_tree_texts_belong_only_to_voice_components` |
| `compiled_group` | a compiled-dependencies row with no lockfile association stands uncovered | C | `compiled_group` |
| `compiled_group` | the lockfile's repository and revision equal the component's as written (`.git`, `.GIT`, another letter case or a trailing `/` refuses with main's message) | E | `test_a_compiled_component_s_repository_is_compared_as_written`, `test_compiled_dependency_rows_are_covered_only_by_their_crate_group` |
| `compiled_group` | a component whose repository is Codex's, in any letter case, is at the distribution record's source commit | E | `test_the_codex_commit_check_ignores_repository_case` |
| `compiled_group` | each crate text is mapped and equals its package account | C | `compiled_group` |
| `compiled_group` | a package standing `gap` or `no-publisher-text` keeps the row uncovered | E | `test_compiled_dependency_rows_are_covered_only_by_their_crate_group`, `test_no_publisher_text_alone_keeps_the_account_open_and_strict_refuses` |
| `compiled_group` | a package standing `held` keeps the row open | C | `compiled_group` |
| `compiled_group` | the table's standing equals the computed one | E | `test_compiled_dependency_rows_are_covered_only_by_their_crate_group` |
| `compiled_group` | a component a lockfile association names is compiled-dependencies with an executable member, and an executable in two compiled-dependencies rows refuses | E | `test_a_locked_component_is_compiled_and_has_an_executable`, `test_deleting_compiled_dependency_rows_leaves_every_executable_uncovered` |
| `compiled_group` | an executable in no compiled-dependencies row gets an uncovered `compiled-in:` row | E | `test_deleting_compiled_dependency_rows_leaves_every_executable_uncovered` |
| `compiled_group` | the executable rule fits the record's Mach-O count | E | `test_executable_rule_must_fit_the_record_macho_count` |
| `compiled_group` | which executable is built from which lockfile | R | pre-existing curated judgment in `components.json`. Evidence: the `codex-rs` workspace members at d32063f9 that declare `codex`, `codex-exec-server`, `codex-code-mode-host` and `codex-voice-host`, and for `codex-path/rg` the supplier package script's rg selector naming the ripgrep 15.2.0 release (the 0.160.0 selector is kept under `../supplier_notices/codex-0.160.0/scripts/codex_package/`; the d32063f9 copies are not held here) |
| `voice_route` | without the pin's voice records, the row is not covered | E | `test_a_voice_component_is_covered_only_through_the_voice_records`, `test_a_supplier_tree_row_needs_its_source_url_but_no_invented_revision` |
| `voice_route` | a missing or mismatched source URL refuses with the records held, and leaves a row tagged covered open without them | E | `test_a_supplier_tree_row_needs_its_source_url_but_no_invented_revision` |
| `voice_route` | a row naming a committed text stands uncovered (by its identity check, which runs first) | E | `test_a_voice_component_is_covered_only_through_the_voice_records` |
| `voice_route` | a row with no supplier-tree text stands uncovered | E | `test_a_voice_component_is_covered_only_through_the_voice_records` |
| `voice_route` | exactly one native-library entry of `sources.json` states the row's version and URL, and one entry establishes one row | E | `test_each_row_is_established_by_exactly_one_native_library_entry`, `test_one_native_library_entry_cannot_establish_two_rows`, `test_a_supplier_tree_row_needs_its_source_url_but_no_invented_revision` |
| `voice_route` | each member is a file the supplier manifest lists | E | `test_a_row_member_must_be_listed_by_the_supplier_manifest` |
| `voice_route` | the record copies equal their distribution-record members; the manifest's commit, version and targets are the pin's; repeated keys and invalid JSON refuse | E | `test_file_identity_must_equal_the_distribution_record`, `test_manifest_must_agree_with_the_pin_commit_target_and_inventory`, `test_the_record_must_be_for_the_pin_and_supported_target`, `test_repeated_keys_or_invalid_json_refuse` |
| `voice_route` | with `check --vendor DIR`, a row with tree texts whose version differs from the tree's `sources.json` refuses (main's refusal) | E | `test_the_vendor_check_keeps_main_s_refusal` |
| `voice_route` | which licence file, and which member, is which native library's | R | neither record says. Evidence: the file names, the distribution record and the 0.167.0 table reviewed in pull request 243 |
| Reading row (`SUPPLIER_READINGS`) | covered only with the reading in the closed form exactly; otherwise held | E | `test_icu_is_covered_only_by_the_owners_closed_form_reading` |
| Reading row (`SUPPLIER_READINGS`) | a reading on any other row refuses | C | `build` |
| Reading row (`SUPPLIER_READINGS`) | the reading's date and relay | R | bound by the review record |
| Committed-text row | a text at another repository or revision than the component's (as written), not an `also_at` identity of the same blob and not a named exception, leaves the row uncovered | E | `test_supplier_texts_must_match_their_component`, `test_also_at_identities_bind_a_text_to_another_revision_only_for_its_blob` |
| Committed-text row | without its repository and revision, the row stands uncovered | E | `test_empty_exception_reason_and_absent_identity_refuse`, `test_a_component_whose_every_text_is_an_exception_still_needs_its_own_identity` |
| Committed-text row | an exception needs a non-empty reason | E | `test_empty_exception_reason_and_absent_identity_refuse` |
| Committed-text row | a covered row ships at least one text | C | `build` |
| Committed-text row | the component is in that member, each text is its notice, a listing names each blob and `also_at` identity, and each exception's reason holds | R | pre-existing curated judgment |
| App content | each entry names exact single-file mappings | E | `test_app_content_names_exact_mappings_only` |
| App content | each source is a regular non-link file | E | `test_an_app_file_claim_refuses_a_directory_or_link` |
| App content | each mapping exists in what the bundle selects | E | `test_a_claim_on_a_mapping_that_does_not_exist_refuses` |
| App content | each named file is the App's own content | R | pre-existing curated judgment |
| Notices row | a mapping no row names becomes an uncovered row | E | `test_a_mapped_resource_the_account_does_not_name_is_open`, `test_a_foreign_selection_under_a_named_destination_folder_is_open` |
| Notices row | only the vendor tree may be named by `accounts_for` | E | `test_the_vendor_tree_must_be_named` |
| Notices row | the supplement's contents | R | pre-existing; checked when staged (`receipts.py check_stage`) |

### `../supplier_notices/crates.py`, `entries`: where a package becomes `text` or `not-in-macos-package`

| Site | Condition | Mark | Test or duty |
|---|---|---|---|
| All routes | `associations.json` has its typed shape | E | the shape cases of `test_a_publisher_association_needs_its_provenance`, `test_a_changed_publisher_text_or_source_identity_refuses`, `test_registry_manifest_identity_and_notice`, `test_recorded_exclusion_evidence_must_match_the_manifest`, `test_empty_text_associations_refuse_before_account_generation` |
| All routes | a repeated lock id, lock component, workspace lock, manifest id or manifest path refuses | E | `test_a_repeated_identifier_refuses` |
| All routes | a workspace entry naming no lockfile refuses | E | `test_a_workspace_entry_naming_no_lockfile_refuses` |
| All routes | a package with two text routes, a text route and an open or absent mark, or an association naming no locked package refuses | E | `test_changed_checksum_unused_and_conflicting_associations_refuse`, `test_unused_open_or_absent_associations_refuse`, `test_an_excluded_package_named_twice_or_also_open_refuses` |
| Archive route (`text`) | the index has exactly the locked registry packages, with its bound digests | E | `test_a_missing_or_extra_index_row_refuses`, `test_an_index_digest_drift_refuses` |
| Archive route (`text`) | each text is in `texts/` with its digest | E | `test_a_missing_changed_extra_or_linked_text_refuses` |
| Archive route (`text`) | an archive row carries no repository, so for a package not on the named list only the text digest guards it for the objc2 hold | C | `hold_for_reading` |
| Archive route (`text`) | the index is what `crates.py index` makes from the archives | R | rerun it with the archives |
| App route (`text`) | `reading_required` equals main's rule (the repository, as written, is the objc2 repository) and the guard's | E | `test_app_held_texts_are_a_reviewed_association_not_a_read_of_the_app_tree`, `test_an_app_text_repository_in_another_case_refuses_as_on_main` |
| App route (`text`) | a listed package moved to the App route stays held, unless the input refuses | E | `test_moving_a_listed_package_to_the_app_route_cannot_release_it` |
| App route (`text`) | each App text is the same archive's text in the App's account | R | `transitive-index.json`, that crate and checksum |
| Publisher route (`text`) | the archive's recorded VCS revision equals the association's | E | `test_a_publisher_association_needs_its_provenance` |
| Publisher route (`text`) | the archive's recorded repository is the association's GitHub repository (owner and name compared without regard to case, a `.git` suffix or a path), or null with `repository_basis`; another repository, or null without a basis, refuses | E | `test_a_publisher_association_needs_its_provenance` |
| Publisher route (`text`) | `path_in_vcs` is null exactly when `path_basis` is present | E | `test_an_omitted_path_needs_its_basis`, `test_a_stated_path_carries_no_basis`, `test_a_publisher_association_needs_its_provenance` |
| Publisher route (`text`) | each text is notice-named, at an accepted path, with its recorded listing blob and size, and its bytes held | E | `test_a_changed_publisher_text_or_source_identity_refuses`, `test_a_publisher_text_association_needs_a_held_text_bound_to_its_listing` |
| Publisher route (`text`) | a text carrying the objc2 overview is held | E | `test_an_unlisted_package_carrying_the_overview_text_or_from_objc2_is_held` |
| Publisher route (`text`) | the recorded archive values are the archive's; the listing names each blob; the texts are the folder's whole selection; each identity triple belongs together; a null path's basis | R | `review_publisher_texts.py` compares the first three and the stored bytes; a `path_basis` is prose the reviewer reads against the listing |
| Git route (`text`) | the association's repository and revision are the lock source's, as written | E | `test_git_association_must_match_the_lock_and_its_listing`, `test_a_git_association_is_compared_with_the_lock_as_written` |
| Git route (`text`) | a locked Git package without an association refuses | E | `test_a_locked_git_package_without_association_refuses` |
| Git route (`text`) | each text's blob equals its recorded listing blob | E | `test_git_text_must_be_its_listing_blob` |
| Git route (`text`) | a text carrying the objc2 overview is held | E | `test_the_overview_text_guard_applies_after_the_git_route` |
| Git route (`text`) | the listing names that blob at that path | R | the Git listing named |
| Workspace route (`text`) | the workspace's repository and revision are its lockfile's, as written | E | `test_a_workspace_association_is_at_its_lockfile_s_source` |
| Workspace route (`text`) | each text's bytes equal its identity, and its blob is in its recorded listing blobs | E | `test_workspace_text_must_equal_its_identity_and_listing` |
| Workspace route (`text`) | an empty text list refuses | E | `test_empty_text_associations_refuse_before_account_generation` |
| Workspace route (`text`) | the listing names the blobs | R | the codex-rs or ripgrep listing named |
| `absence` (`not-in-macos-package`) | the recorded reverse dependencies equal the lockfile's, and the entry names its lockfile and target | E | `test_recorded_exclusion_evidence_must_match_the_manifest` |
| `absence` (`not-in-macos-package`) | each parent manifest is a regular file at its stated path equal to its recorded identity, cited, and naming that package | E | `test_a_committed_manifest_must_equal_its_recorded_identity`, `test_a_committed_manifest_that_is_a_link_refuses`, `test_an_uncited_parent_manifest_refuses`, `test_recorded_exclusion_evidence_must_match_the_manifest` |
| `absence` (`not-in-macos-package`) | its source claim's name, version and checksum equal the lock's, or its repository and revision equal the workspace lock's as written | E | `test_registry_manifest_identity_and_notice`, `test_workspace_manifest_identity_and_notice` |
| `absence` (`not-in-macos-package`) | every explicit declaration is under a closed-form target key false for `aarch64-apple-darwin` | E | `test_unknown_target_keys_refuse`, `test_a_declaration_the_record_leaves_out_is_found_in_the_manifest`, `test_any_further_declaration_in_the_manifest_is_judged`, `test_a_false_excerpt_cannot_exclude_an_unconditional_dependency` (control `test_control_a_truthful_linux_only_parent_excludes`) |
| `absence` (`not-in-macos-package`) | a registry manifest inherits nothing; a workspace member satisfies rule (i) or (ii) | E | `test_a_registry_manifest_with_workspace_inheritance_refuses`, `test_an_inherited_key_that_could_be_the_excluded_package_refuses`, `test_an_inherited_dependency_that_also_names_a_package_refuses` (control `test_control_an_inherited_key_under_a_condition_false_for_macos_keeps_rule_i`) |
| `absence` (`not-in-macos-package`) | the recorded declarations and licence equal the parse | E | `test_recorded_exclusion_evidence_must_match_the_manifest`, `test_registry_manifest_identity_and_notice`, `test_workspace_manifest_identity_and_notice` |
| `absence` (`not-in-macos-package`) | the recorded notice is compared not with the parse but with the shipped texts: a registry manifest's crate stands `text` with exactly the recorded texts, and a workspace manifest's notice is its workspace's texts | E | `test_registry_manifest_identity_and_notice`, `test_workspace_manifest_identity_and_notice` |
| `absence` (`not-in-macos-package`) | each registry manifest is its archive's `Cargo.toml`; each workspace manifest is the file at its revision; rule (ii)'s premise | R | `crates.py verify-manifests --archives MAP.json`; the codex-rs listing; the review of `locks` |
| `hold_for_reading` (keeps open; never yields `text`) | a listed identity stays held whatever its text, spelling or route, unless the input refuses | E | `test_a_listed_package_with_another_text_stays_open`, `test_a_listed_package_with_no_overview_text_stays_open`, `test_a_repository_spelling_cannot_release_a_listed_package`, `test_moving_a_listed_package_to_the_app_route_cannot_release_it` |
| `hold_for_reading` | an unlisted package whose route gives the objc2 repository, in any letter case, is held | E | `test_the_objc2_repository_guard_ignores_letter_case` |
| `hold_for_reading` | a listed identity no lockfile locks refuses | E | `test_a_listed_identity_no_lockfile_locks_refuses` |
| `hold_for_reading` | on the committed inputs, the named list equals the held packages | E | `test_the_named_list_is_exactly_the_held_packages` |
| `hold_for_reading` | an identity leaves the list only with the owner's reading recorded | R | the list is code |
| Open standings | a `no-publisher-text` package ships nothing and keeps the group open | E | `test_no_publisher_text_packages_ship_nothing_and_stay_open`, `test_no_publisher_text_alone_keeps_the_account_open_and_strict_refuses` |

## Limits

The account describes what the package is built to carry, from committed inputs;
it is not read from a built package, and Tauri's resource mapper has not been run
against the overlay here. A notice text is the publisher's text at the version or
revision named; the account decides no licence question except where an owner
reading is recorded. The upstream toml `LICENSE-APACHE` ends with a blank line;
its bytes are kept as published.
