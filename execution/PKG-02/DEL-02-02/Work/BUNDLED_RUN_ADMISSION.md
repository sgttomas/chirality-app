# BUNDLED-RUN-01 — closed LS-5 run admission for the App's included workflow

## Why

[PUBLICATION_JOURNEYS.md](PUBLICATION_JOURNEYS.md) J1 requires that a person can
select an existing workflow and run it without first creating or registering one.
WR (this folder's [WORKSPACE_AND_REGISTRATION.md](WORKSPACE_AND_REGISTRATION.md))
already settles the meaning:
- §3 says bundled workflows are "Origin *bundled*; runnable without A15".
- LS-5 says "Shipped in the App release … Yes".
- TT-1 and TX-1 admit LS-5 selections for runs.
- TX-7 (c) supplies a bundled revision's other files as a project supply copy.

The App previously ran only hot registered revisions. `run_admission` refused
every production-bundle selection, and the root snapshot reported the included
workflow with `runnable:false`. This clause implements LS-5 for exactly one
subject. It changes no WR, WD or ScopeOfWork commitment.

## Selected subject (Agent 0, 2026-11-03)

Agent 0 selected the existing pinned production package as the first bundled
workflow input:

| Item | Value |
|---|---|
| Manifest | `app/src-tauri/resources/production_workflows/MANIFEST.json`, SHA-256 `5eb8ab6d6259c47ef8d270597d9323f0399e2f668ff2defc37159faa05f71dc3` |
| Release subject (WD source root) | `chirality-app-v4:APP-V4-BUNDLE-INPUTS-20261008` |
| Package | `coordinated-knowledge-work`, `chirality.app.workflow-package.sha256/v1` revision `3730d84debb5d77582a0c26211a5f380cdb1a44c7e26eeb537f334db43fdd881` (`WORKFLOW.md`, `REVIEW-NOTES.md`), source revision `f3c0a1df…` |
| Installed location | `Contents/Resources/workflows/` (PACKAGING P-2, `tauri.conf.json` `resources/production_workflows/` → `workflows/`) |

The manifest's own standing is unchanged: "production bundle candidate; not a
published release". It still lists no historical shipped revisions and does not
recognize v3. No newer shared-library content is adopted. No public release,
shipped history or qualification is claimed.

## Admission rule (source)

- **Compiled subject.** `workflow_catalog.rs` pins
  `SELECTED_BUNDLED_MANIFEST_SHA256` and `SELECTED_BUNDLED_REVISION`.
  `ProductionCatalog::bundled_run_admission(selection)` admits only a
  `ProductionBundle` selection that:
  - came from `select_bundle_package`, so it has a bundle root and no holding
    library;
  - carries the selected manifest digest, the compiled manifest bytes and the
    release subject;
  - has the catalog's exact identity, and a snapshot revision equal to the
    selected revision.

  Changing the manifest or package bytes needs a reviewed change to these
  constants.
- **Location binding.** Native startup records `resource_dir()/workflows` once
  per process in the catalog (`record_installed_root`, through
  `configure_installed_bundle`). A different later root is refused.
  `bundled_run_admission` itself requires the selection's bundle root to equal
  that recorded root, so every consumer inherits the binding:
  - session run admission;
  - the catalog entry;
  - publication.

  A byte-identical bundle at any other path is refused, and so is a process
  with no recorded root. `select_production_bundle` resolves only that root.
- **Recheck at use.** `verify_store` rechecks the location, the root
  `MANIFEST.json` bytes and the package revision at selection, prepare
  (`prepare_run_with`, `PreparedRunText::start`, `PreparedRunPublication::new`)
  and send. `PreparedRunPublication` keeps the admitted selection, so
  `publish()` reruns `verify_store` and `bundled_run_admission` on its first
  attempt and on every retry, immediately before any record is written. A
  manifest or package change after preparation therefore publishes no
  `selection_record` or `run_text`.
- **Records.** `PreparedRunPublication::new` accepts a registered revision, or a
  selection that passes `bundled_run_admission`, and refuses every other
  admission even if a caller bypassed the session. The `selection_record`
  standing is `bundled`, already in the schema's enum. `holding_library` is the
  installed workflows root. `identity.origin` is `bundled`. When a reopened run
  is ended after relaunch, its end notice uses an internal
  `RegisteredRevision` label. That label confers no admission or registration,
  and the recorded selection keeps its own standing.
- **Files line.** A bundled selection always uses `bundled_files_folder`: a
  project supply copy (TX-7 c), wherever the App is installed, including
  beneath the opened project or the home folder. No path into the App bundle
  appears in the run text.

## Still refused (unchanged)

These keep their existing refusal (WR TT-1/TX-1, WP-6):
- the embedded catalog copy;
- library holding copies, because LS-8 lists no shipped revision;
- development-catalog selections;
- unknown, renamed or tampered bundles;
- caller-provided locations.

This adds no forged A15, no automatic registration, no permission or capability
change and no cold-file authority. A15 registration, RC-2 and every other WR
behavior are unchanged.

## Consumer contract

Coordinated with the frontend lane (PR #107); no field or command change:
- **Catalog entry.** `workflowRoot.productionCatalog.entries[]` keeps `{name,
  revision, origin, sourceRoot, revisionMethod, identity, runnable, runLimit}`.
  - `runnable` is true only when the recorded installed root currently verifies
    the closed subject.
  - Otherwise `runLimit` gives a readable cause: the existing TT-1/TX-1
    candidate text when the root is unknown, or "This App's included workflow
    could not be verified: …".
  - `bundledStanding` is new and display-only.
- **Selection.** `workflow_select_production_bundle {name}` is unchanged. The
  selection view's standing is "bundled with this App build (WR LS-5); runs
  without A15; this build is a release candidate, not a published release",
  with `runnable` true.
- **Packaging.** It needs nothing new beyond the existing P-2 mapping. The
  package bytes are part of the signed bundle tree.

## Checks

Focused Rust tests, offline and locked, in a fresh scratch `CODEX_HOME` and target.
Independent Astra-medium review of `a02183cd` found three P2 boundary gaps, all
repaired here: publication lacked installed-root authority, publication did not
recheck the manifest, and a supply copy was not forced inside the project.
- `bundled_run_admission_is_closed_to_the_selected_installed_subject`: embedded
  and holding copies are refused. An unknown or different recorded root is
  refused, and so is rebinding. The installed resolution is admitted only under
  the recorded root.
- `bundled_ls5_requires_this_apps_installed_resources`: an unknown root, a
  rebinding and a byte-identical caller location are all refused; the catalog
  entry becomes runnable only once the root is recorded.
- `bundled_ls5_selection_prepares_and_sends_through_the_guarded_lifecycle`:
  prepare and send succeed. The run text has the pinned begin marker and the
  supply-copy files line, and no bundle path. The `selection_record` standing is
  `bundled`.
- `bundled_ls5_mutation_after_selection_refuses_prepare_and_send_without_effects`:
  a package edit refuses prepare with no records or turn, and the entry stops
  offering the workflow. A manifest change after prepare refuses send.
- `typed_publication_retains_prepared_text_and_refuses_lost_source_or_development`:
  now also refuses a forged bundle admission at publication.
- `bundled_publication_requires_this_apps_installed_root_and_rechecks_at_publish`:
  - an exact copy at another root is refused at direct publication;
  - a manifest change after `new()` refuses `publish()` and its retry;
  - once restored, the run publishes with standing `bundled`.
- `bundled_ls5_inside_the_project_still_uses_a_supply_copy`.
- The lifecycle test also ends the bundled run from its records in a fresh
  process, after relaunch.
- The mutation test also confirms that no WR or RS record is published when
  send is refused after a manifest change.
- The existing holding-copy, development and registered-revision tests are
  unchanged.

## Limits and remaining observation

These are source fixtures. The owner-visible J1 journey on an identified candidate
remains DEL-09-02's actual observation: an included workflow selected, run and
completed in a real project. That observation must name the candidate, its
installed `workflows/` digest closure and the actual run records. Useful work,
completion and model behavior are not established by these tests. The build
remains a release candidate, not a published release.
