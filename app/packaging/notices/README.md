# Notices the macOS arm64 package ships

These checks are not built to resist deliberately forged, mutually consistent inputs
(an account, a table, an association and a review record changed together to agree).
The review of the pull request that changes a curated file covers that boundary
([What these checks withstand](#what-these-checks-withstand); the per-collection lists
are under [What is enforced and what review covers](#what-is-enforced-and-what-review-covers),
whose by-site table is the authority, and in `../supplier_notices/README.md`).

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
  belong to exactly one `compiled-dependencies` component. A component that a lockfile
  association names must be such a component and have at least one executable member;
  which executable is built from which lockfile is a review duty (the table below).
  Such a component is covered only by
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
  committed under `../supplier_notices/crates/manifests/`, every explicit declaration of
  the package that the checker finds by parsing that manifest sits under a target key, in
  a closed set of forms, that is false for that target, and no key inherited from the
  workspace can be the package (rule (i) or (ii) in `../supplier_notices/README.md`). No
  resolver was run and nothing was read from the binaries; the account lists every such
  package with its evidence and the rule that admitted it under `excluded_packages`.
  Nothing is left out on any other ground. The 23 packages awaiting the owner's objc2
  reading are a closed, named list in `crates.py` and stay held whatever route, spelling
  or text their rows give them. The table's standing for the component must agree.
- **Voice rows.** A voice row is any component with a member or text in the voice
  library folders of the supplier tree (`codex-resources/voice/lib/`, `plugins/`,
  `licenses/`), however its row is written. Membership is decided before any other
  route: a voice row cannot be a compiled-dependencies, reading or deferred row, a voice
  member belongs to one component, and only a voice row names supplier-tree texts, each
  under `codex-resources/voice/licenses/`. It is covered only when the supplier's own
  voice records for the declared pin, committed under
  `../supplier_notices/voice_records/<pin>/` and bound to their members' digests in the
  distribution record, establish its version and source URL
  (`../supplier_notices/voice.py`; a disagreement refuses, and each native-library entry
  establishes exactly one row), and only with its texts from the supplier tree, carrying
  its source statement; no exception or other text covers it. These are the supplier's
  statements about its bundle; the libraries' contents are not inspected. Which licence
  file in the tree is a row's notice is not stated by those records; it is curated in
  `components.json`, a review duty.
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
  archives (the expected checksum taken from the lockfile). The
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

This table is the authority on how a standing can move toward covered. It has one row
for every place in `coverage.py` where a component can be added as covered, and every
place in `../supplier_notices/crates.py` where a locked package can become `text` or
`not-in-macos-package`. For each, it lists the conditions under which that place
yields that standing. **E** marks a condition the checker enforces, with the test
that shows it. **R** marks a review duty: the reviewer of the pull request that changes
the curated input checks it from the held evidence named. A row that did not change in
the change that introduced this table still has its row. Where a condition is
pre-existing curated judgment, the row says so.

Every row also rests on three conditions:

- each curated file that `coverage-review.json` names must have its bound SHA-256 (E:
  `test_curated_input_changes_refuse_without_the_review_record`). Rebinding is the
  reviewer's act (R);
- `check` regenerates the account and requires it unchanged (E:
  `test_stale_account_refuses`, `test_committed_account_is_current_and_counts_add_up`);
- anything not covered keeps `check --strict` non-zero and a public production
  preparation refused (E: `test_strict_mode_exits_non_zero_naming_each_open_component`,
  and the strict tests in `production_inputs_test.py`).

The per-collection lists in `../supplier_notices/README.md` spell out the E and R
items of the crate and voice rows below.

### `coverage.py`, `build` and its helpers: where a component is added as covered

| Site | Conditions for covered |
|---|---|
| `build`: the App row | The App component of the direct index, with its `LICENSE.md` notice mapped into the package. E: the direct index check (`notice_resources_test.py` `test_saved_scope_is_app_and_exact_direct_runtime_set`, `test_changed_notice_bytes_refuse`). R (pre-existing curated judgment): that the App's own licence is its notice. |
| `build`: App icons | A provenance entry in `app_assets` for each declared icon, with equal SHA-256 and size. Without one, the icon stands uncovered. E: `test_bundled_icon_needs_provenance`. R (pre-existing curated judgment): that the entry's provenance statement is true, from the repository history at `added_by_commit`. |
| `build`: Library content | The licence digest equals the App's `LICENSE.md`. The source record lies inside the bundle and has its reviewed digest. It names the same repository (by the one repository identity), commit and licence, or the same `basisCommit`. The folder holds exactly the members that record lists. E: `test_library_content_must_match_its_bundle_source_record`, `test_an_added_or_changed_file_in_a_bundled_library_folder_is_open`, `test_a_foreign_selection_under_a_named_destination_folder_is_open`. R (pre-existing): that the record's source is the Library's at that revision, as reviewed in the change that bundled it. |
| `build`: a Cargo row that needs a reading | A row needs a reading when its text was received as an upstream text or its repository is the objc2 repository (one repository identity). It ships its held text, and the owner's reading is recorded in the closed form. A reading for any other crate refuses. E: `test_a_pending_or_missing_reading_is_pending_and_strict_refuses`, `test_a_reading_cannot_be_extended_to_a_crate_that_needs_none`. R: the reading's date and relay, bound by the review record. |
| `build`: a Cargo archive-member row | The transitive index row has kind `archive-member`, and the index agrees with its shipped texts. E: `notice_transitive_test.py` `test_text_kind_must_match_members_and_received_text`, `test_changed_missing_extra_or_linked_text_refuses`, `test_general_crate_extraction_verifies_the_lock_checksum`. R: that the index is what the generator makes from the archives: rerun `transitive.py check --cargo-home` (CI does not hold the cache). |
| `build`: a Cargo root-text row | It ships texts, and either its kind is `retained-root-texts` or it is a received subject. E: `test_received_text_must_be_at_the_revision_its_crate_names`, `test_root_row_cannot_choose_path_revision_scope_or_downgrade`, `test_unlisted_crate_cannot_inherit_root_association`, `test_partial_root_texts_remain_unqualified_in_summary`. R (pre-existing curated judgment, which the project's Agent 0 accepted as mechanical matches): that the root text at the named revision is the crate's notice. |
| `build`: an npm row | The index row's kind is `direct-index-archive` or `lock-tarball`. E: `test_npm_rows_are_recomputed_from_the_lock_even_when_the_receipt_is_rebound`, `test_cargo_text_kinds_cannot_hide_unverified_npm_packages`. R: that the index is what the generator makes from the tarballs: rerun with `--npm-cache`. |
| `build`: a font row | The upstream is verified, with its package and integrity, and a tarball member for the licence and for every file. E: `test_unverified_fonts_are_uncovered`, `font_notice_test.py` `test_index_shape_provenance_and_notice_list_refuse`, `test_upstream_recheck_refuses_a_tarball_that_is_not_the_pinned_one`. R: rerun `font_notice/check.py --npm-cache`. |
| `build`: SQLite | The header text's bytes equal its index asset. E: `notice_resources_test.py` `test_sqlite_supplement_matches_lock_and_exact_saved_assets`. R (pre-existing curated judgment): that the header is the public-domain dedication; rerun `sqlite_notice/check.py --archive`. |
| Every supplier row (before the routes below) | The table is reviewed for the declared pin, or every row stands uncovered and an open table row is added. A row in `DEFERRED` stays uncovered. Every member and text is a file of the distribution record, and every member is claimed. Component ids and text paths do not repeat. A repeated file in the distribution record also refuses; no test covers that, because the record is a frozen snapshot bound by its digest. E: `test_a_repeated_supplier_identifier_refuses`, `test_a_table_reviewed_for_another_pin_covers_no_supplier_row`, `test_another_declared_pin_is_named_as_an_open_review_not_assumed`, `test_deferred_rows_stay_uncovered_whatever_the_table_says`, `test_supplier_table_must_claim_every_member_and_justify_gaps`, `test_distribution_record_drift_refuses`. **Voice membership is decided before any route.** A row with a member or text under `codex-resources/voice/lib/`, `plugins/` or `licenses/` takes the voice route only. It cannot be compiled-dependencies, a reading row, deferred or carry a reading. A voice member belongs to one component. Only a voice row names supplier-tree texts, each under `codex-resources/voice/licenses/`. E: `test_a_voice_member_takes_only_the_voice_route` (to compiled, to a reading row, twice), `test_supplier_tree_texts_belong_only_to_voice_components`. |
| `compiled_group`, from `build` for a compiled-dependencies row | The row is reviewed and not deferred. A lockfile association names it. The lockfile's source is the component's repository and revision (the one repository identity). A Codex component is at the distribution record's source commit, whatever the letter case of its repository. Each crate text is mapped and equals its package account. No package stands `gap`, `no-publisher-text` or `held`; every package is `text` or `not-in-macos-package` (the `crates.py` rows below). The table's standing equals the computed one. A component a lock association names is compiled-dependencies, covered only by its crate group, and has at least one executable member. Every executable belongs to exactly one compiled-dependencies component; one that belongs to none gets an uncovered `compiled-in:` row, and one that belongs to two refuses. The executable rule fits the record's Mach-O count. E: `test_compiled_dependency_rows_are_covered_only_by_their_crate_group`, `test_a_locked_component_is_compiled_and_has_an_executable`, `test_the_codex_commit_check_ignores_repository_case`, `test_deleting_compiled_dependency_rows_leaves_every_executable_uncovered`, `test_no_publisher_text_alone_keeps_the_account_open_and_strict_refuses`, `test_empty_workspace_texts_cannot_leave_ripgrep_covered`, `test_executable_rule_must_fit_the_record_macho_count`. R (pre-existing curated judgment in `components.json`): which executable is built from which lockfile. The evidence is the supplier source's build files at the pinned commit: the `codex-rs` workspace members at d32063f9 that declare `codex`, `codex-exec-server`, `codex-code-mode-host` and `codex-voice-host`, and, for `codex-path/rg`, the supplier package script's rg selector, which names the ripgrep 15.2.0 release. The 0.160.0 selector is kept under `../supplier_notices/codex-0.160.0/scripts/codex_package/`, and `ripgrep_0167.py` recomputes the 0.167.0 association. The d32063f9 copies are not held in this repository. |
| `voice_route`, from `build` for a voice row | The row is reviewed and not deferred. Its source URL is present (no revision is invented). The table says covered. The pin's voice records are held. The row names no committed text and no exception, and at least one tree text, each under the licences folder. The records establish the row: exactly one native-library entry, with equal version and URL. Its members and texts are files the supplier manifest lists. The account row carries its source statement. E: `test_a_voice_component_is_covered_only_through_the_voice_records`, `test_a_supplier_tree_row_needs_its_source_url_but_no_invented_revision`, and the voice tests in `supplier_crate_notices_test.py` (`test_file_identity_must_equal_the_distribution_record`, `test_manifest_must_agree_with_the_pin_commit_target_and_inventory`, `test_the_record_must_be_for_the_pin_and_supported_target`, `test_each_row_is_established_by_exactly_one_native_library_entry`, `test_one_native_library_entry_cannot_establish_two_rows`, `test_a_row_member_must_be_listed_by_the_supplier_manifest`, `test_repeated_keys_or_invalid_json_refuse`). With `--vendor`, `check_vendor` keeps main's refusal (E: `test_the_vendor_check_keeps_main_s_refusal`). R: which licence file in the tree is which library's (neither record says); the distribution record's truth, from the change that brought it. |
| `build`: a supplier row covered by an owner reading (`SUPPLIER_READINGS`) | Not voice and not compiled. Its identity is complete. No text is foreign. The table says covered, and the reading is in the closed form exactly. E: `test_icu_is_covered_only_by_the_owners_closed_form_reading`. R: the reading's date and relay, bound by the review record. |
| `build`: a supplier row covered by its committed texts | Reviewed, not deferred, not voice and not compiled. Its repository and revision are present. It ships at least one text. Each text is at the component's own repository and revision (by the one repository identity), or at an `also_at` identity for the same blob, or is a named exception with a non-empty reason. The table says covered, and the row is not a reading row. E: `test_supplier_texts_must_match_their_component`, `test_also_at_identities_bind_a_text_to_another_revision_only_for_its_blob`, `test_empty_exception_reason_and_absent_identity_refuse`, `test_a_component_whose_every_text_is_an_exception_still_needs_its_own_identity`, `test_expected_supplier_components`, `test_removing_a_v8_text_needs_the_review_record`. R (pre-existing curated judgment): that the component is in that member (the supplier's statement in its source), that each text is its notice, that a listing names each blob and `also_at` identity, and each exception's reason. |
| `build`: App content | Each `app_resources` entry has the exact shape. Every mapping is a single file whose source is a regular non-link file, and the mapping exists in what the bundle selects. E: `test_app_content_names_exact_mappings_only`, `test_an_app_file_claim_refuses_a_directory_or_link`, `test_the_shipped_limitations_list_is_app_content_by_its_exact_mapping`, `test_a_claim_on_a_mapping_that_does_not_exist_refuses`. R (pre-existing curated judgment): that each named file is the App's own content. |
| `build`: the notices row | The index and account files the bundle maps, plus the selected supplement's fixed destination. Every claim names an existing mapping; an unnamed mapping is an uncovered row. E: `test_every_current_mapping_is_named`, `test_a_mapped_resource_the_account_does_not_name_is_open`, `test_the_vendor_tree_must_be_named`. R (pre-existing): the supplement's contents are checked when it is staged (`receipts.py check_stage`, `notice_receipts_test.py`). |

### `../supplier_notices/crates.py`, `entries`: where a package becomes `text` or `not-in-macos-package`

`associations.json` is first loaded through one typed shape check. A repeated lock id,
lock component, workspace lock, manifest id or manifest path refuses (E:
`test_a_repeated_identifier_refuses`), and a workspace entry must name a lock. Every
repository comparison in both checkers goes through `crates.repository_key`: it refuses
`.git` in any letter case and compares without regard to case (E:
`test_one_repository_identity_for_every_comparison`,
`test_the_codex_commit_check_ignores_repository_case`). After every route, the objc2
guard (`hold_for_reading`) holds a listed package, a package carrying the overview text,
and a package whose route gives a repository that is the objc2 repository (rows below).

| Site | Conditions for the standing |
|---|---|
| Registry, archive route (`text`) | The index row of that name, version and lockfile checksum has notice members. There is no other route and no open or absent mark. Each text is in `texts/` with its digest. The objc2 guard sees only the text digest, because an archive row carries no repository. E: `test_committed_group_checks_and_covers_every_locked_package`, `test_a_missing_or_extra_index_row_refuses`, `test_an_index_digest_drift_refuses`, `test_a_missing_changed_extra_or_linked_text_refuses`, `test_changed_checksum_unused_and_conflicting_associations_refuse`, `test_an_unlisted_package_carrying_the_overview_text_or_from_objc2_is_held`. R: that `index.json` is what `crates.py index` makes from the archives (checksum first, header checks, notice members only); rerun it with the archives. |
| Registry, App route (`text`) | An `app_texts` association with the locked identity. There is no other route. `reading_required` equals the objc2 rule, and the guard runs with the association's repository. E: `test_app_held_texts_are_a_reviewed_association_not_a_read_of_the_app_tree`, `test_moving_a_listed_package_to_the_app_route_cannot_release_it`. R: that each App text is the same archive's text in the App's reviewed account (`transitive-index.json`, that crate and checksum). |
| Registry, publisher route (`text`) | A `registry_sources` association with the locked identity, and no other route. The archive's recorded VCS revision equals the association's. Its recorded repository is the same repository, or is null with `repository_basis`. `path_in_vcs` is a folder or the root `""`, or null with `path_basis` (and only then). Each text is notice-named, has its listing blob and size, and its bytes are held. The guard runs with the association's repository. E: `test_a_publisher_association_needs_its_provenance`, `test_a_changed_publisher_text_or_source_identity_refuses`, `test_a_publisher_text_association_needs_a_held_text_bound_to_its_listing`, `test_an_omitted_archive_path_is_null_with_its_basis`, `test_an_omitted_path_needs_its_basis`, `test_a_stated_path_carries_no_basis`, `test_a_manifest_spelling_of_the_same_repository_is_accepted_and_an_inferred_one_needs_its_basis`, `test_publisher_texts_ship_with_their_basis_and_objc2_ones_stay_held`. R: that the recorded archive values (`.cargo_vcs_info.json`, `Cargo.toml`, their sizes and digests, `path_in_vcs` or its absence, the repository) are the archive's. Also that the listing names each blob at its path, that the texts are the folder's complete selection (every folder with a `Cargo.toml` where the path is null), and that each name, version and checksum belong together. `review_publisher_texts.py` reproduces this comparison. |
| Git route (`text`) | A Git association for the locked package. Its repository and revision are the lock source's (one repository identity). At least one text, whose blob equals its listing blob and the stored bytes. The guard runs after it. E: `test_git_association_must_match_the_lock_and_its_listing`, `test_git_text_must_be_its_listing_blob`, `test_a_locked_git_package_without_association_refuses`, `test_the_overview_text_guard_applies_after_the_git_route`. R: that the listing names that blob at that path. |
| Workspace route (`text`) | The lock's single workspace entry. At least one text, whose bytes equal its identity and whose blob is in the listing's. The guard runs after it. E: `test_workspace_text_must_equal_its_identity_and_listing`, `test_empty_text_associations_refuse_before_account_generation`. R: that the codex-rs or ripgrep listing named states the blobs. |
| `absence`, from `entries` (`not-in-macos-package`) | A `not_in_macos_package` entry for the locked identity, with no text route and no other mark. Its recorded reverse dependencies equal the lockfile's. Each parent manifest is committed, a regular file equal to its identity, cited, and names that package; it is the locked archive's `Cargo.toml` or the workspace file at the lock's repository and revision. Every explicit declaration (parsed: every table, rename and kind) is under a closed-form target key false for `aarch64-apple-darwin`. A registry manifest inherits nothing. A workspace member satisfies rule (i) or rule (ii). The recorded declarations, licence and notice equal the parse. E: the tests listed under `not_in_macos_package` in `../supplier_notices/README.md`, among them `test_recorded_exclusion_evidence_must_match_the_manifest`, `test_a_false_excerpt_cannot_exclude_an_unconditional_dependency` with its control `test_control_a_truthful_linux_only_parent_excludes`, and `test_each_exclusion_records_the_rule_that_admitted_it`. R: run `crates.py verify-manifests --archives` for registry manifests; compare the workspace manifests with the codex-rs listing; and check rule (ii)'s premise, that the lockfile is bound to the revision. |
| `hold_for_reading` after every route (keeps open; never yields `text`) | A listed identity stays held whatever its text, spelling or route. An unlisted package carrying the overview text, or with a route repository equal to objc2's, is held. A listed identity no lockfile locks refuses. E: `test_the_named_list_is_exactly_the_held_packages`, `test_a_listed_package_with_another_text_stays_open`, `test_a_listed_package_with_no_overview_text_stays_open`, `test_a_repository_spelling_cannot_release_a_listed_package`, `test_the_objc2_repository_guard_ignores_letter_case`, `test_a_listed_identity_no_lockfile_locks_refuses`. R: the list is code; an identity leaves it only with the owner's reading recorded. |

`gap`, `no-publisher-text` and `held` are open. They cannot cover, and they keep the
group, and so the compiled-dependencies row, open (E:
`test_no_publisher_text_packages_ship_nothing_and_stay_open`,
`test_unused_open_or_absent_associations_refuse`). An item whose standing rests on a
review duty that has not been completed is returned to an open standing.

## Limits

The account describes what the package is built to carry, from committed inputs;
it is not read from a built package, and Tauri's resource mapper has not been run
against the overlay here. A notice text is the publisher's text at the version or
revision named; the account decides no licence question except where an owner
reading is recorded. The upstream toml `LICENSE-APACHE` ends with a blank line;
its bytes are kept as published.
