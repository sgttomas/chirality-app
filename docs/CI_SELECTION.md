---
name: chirality-app-development-verification
description: Explain how changed paths select repository and product checks.
metadata:
  kind: instruction
  surface: reference
---
# App development verification

`harness` remains the required check on every PR. The `change-selection` job
decides the route, and repository checks always run in parallel with whatever
it selects: deliverable structure and utility tests, selection regressions, and
the existing conflict and credential checks. The workflow itself has no PR path
filter. This standalone repository does not execute SWBPIPE checks.

## Change selection

`tools/ci/select_checks.py` reads the complete committed change between the PR
merge base and head. It reports the base/head identities and a reason for every
path in the selection job's output and GitHub step summary. No GitHub files-list
pagination or extension-wide skip is used.

Only additions and modifications of ordinary non-executable files at these
exact documentary paths, and all paths under the guarded declarative `execution/` tree, select repository checks without product verification:

- `AGENTS.md`
- `README.md`
- `init-prompt.md`
- `docs/CI_SELECTION.md`
- `docs/OPERATING_METHOD.md`
- `docs/user-manual/README.md`
- `tools/deliverables/README.md`

Two further classes select repository checks without product verification,
because no macOS product job consumes them (see
[Inputs the macOS jobs do not consume](#inputs-the-macos-jobs-do-not-consume)):
governing text, Markdown under `docs/`; and examination tooling, the Python,
JavaScript, JSON and Markdown under `app/examination/standalone/` and the
`app/tests/group_b_*` tests and fixtures, except the four paths in them that a
macOS job reads.

Every narrowing rule, the documentary paths and `execution/` included, applies
only to a path of printable ASCII; any other spelling selects product checks,
because a checkout may fold it onto another file (a macOS volume folds case and
Unicode forms, so `group_b_fixtureſ` with a long s is `group_b_fixtures` there).
The protected paths inside the class roots are compared without regard to case.

Everything else retains the existing App product verification. This includes
Rust and frontend code, dependencies/locks, workflows, the selector and its
tests, App schema/fixture copies, packaging resources, the other examination
readers, packaged Markdown and unknown paths. Mixed changes select the union: one
product-relevant path selects the product workflow. Deletions, executable-mode
changes, symlinks and other file-type changes select product checks even at an
allowlisted path. Renames are examined as deletion plus addition, so neither
side can be hidden. An empty change set selects product checks. Invalid or
missing commit input, an unavailable or ambiguous merge base, and malformed Git
output fail selection and block the aggregate.

The selector names conservative product domains and exact root files, with the
reviewed documentary exceptions taking precedence. Its report distinguishes an
explicit product rule from an unmatched path; both select all existing PR product
checks. The always-run `inventory` command checks every tracked path against
positive rules and fails on unmatched paths. It also fails when two tracked
paths or directories, read from the commit's tree rather than a checkout (which
may already have merged them), fold to the same name, and when a tracked
symbolic link points into a narrowed class. Its folding is Unicode compatibility
normalization, case folding and dropping format characters: at least what a
case- and normalization-insensitive macOS volume folds, without claiming to
model any file system exactly. Classify such a path deliberately;
the full-coverage fallback does not satisfy completeness. New files within a
known product domain keep product coverage without individual allowlisting.

Runnable implementation, tests, generators and harnesses live under `app/` or
`tools/`. `execution/` holds authoring specifications and retained records.
`tools/ci/check_execution_layout.py` rejects code surfaces in that tree and
current imports/interpreter invocations into it. Its one hash-bound exception
is the historical acceptance presentation; it grants no execution permission.
This is a source/layout guard, not a proof
about arbitrary dynamically computed programs. Changes introducing a new
execution mechanism must extend its checks and receive review.

`execution/PKG-nn/DEL-nn-nn/` holds only `ScopeOfWork.md` and
`deliverable.yaml`, and no tool reads or pins scope prose. Schemas, fixtures and
data that product code or a product test reads live once, beside that reader
under `app/`. Always-on repository checks retain the examination pin check
(`app/examination/repin.py --check`), and the Group B examination tests run in
repository checks on every PR, through `tools/ci/examination_tests.py portable`.

The selector regression fixtures replay recorded changes from PRs 169–181,
plus unknown-path, mixed-change, mode, deletion and rename cases. PR178 retains
product verification because its change includes product-selected documentation
outside `execution/`; the others are repository-only.
Path moves and all App/tool/guard/selector edits select full product checks.
Other product domains remain conservative; no partial frontend/Rust mapping is
introduced.

## Inputs the macOS jobs do not consume

A path skips the three macOS product jobs only when no step of theirs reads it,
directly or through what it builds, and every reader it has runs in the
always-run `repository-checks` job. Neither the frontend build (`tsc` includes
only `app/src`; Vite starts at `app/index.html`) nor the Rust code and its tests
read outside `app/src-tauri` except `app/tests/fixtures`,
`app/supplier_checks/recordings`, `app/packaging/unsigned`,
`tools/verify_records_bag.py` and the kept paths below. `build.rs` watches only
`src-tauri` files, and the bundle takes only `resources/instructions` and
`resources/production_workflows`.
The searches were made by reading each consumer and searching all tracked files
for the paths, not by file extension.

| Class and paths | Readers, and where they run | Search |
| --- | --- | --- |
| A: `docs/**/*.md` | `tools/validation/test_document_metadata.py` reads every header, in `repository-checks`. No App source, test, build script, bundle or pin names a `docs/` path. | `git grep` for `docs/`, `../docs/`, `"docs"`, every `docs/` basename and `include_str!`/`include_bytes!` targets in `app`, `tools` and `.github` |
| A: `execution/**` | Already documentary; `tools.deliverables check` and `check_execution_layout.py` in `repository-checks`. | as above, plus `ScopeOfWork`, `deliverable.yaml` |
| B: `app/examination/standalone/**` except `fixtures/` (`.py`, `.mjs`, `.cjs`, `.js`, `.json`, `.md`) | The Group B suites (`app/tests/group_b*test.py`), `repin.py --check` and `examination_repin_test.py` (which copies the standalone pin profiles), all in `repository-checks`; `native_forms/` reads the pre-run inputs and pins and is run only by `group_b_native_forms_test.py`. | every top-level standalone entry name, `standalone`, `group_b` |
| B: `app/tests/group_b_*` except below (same types) | Run only by the `repository-checks` step `examination_tests.py portable` and, for `*_macos_test.py` modules, the `examination-macos` job; no macOS product step names `group_b`. | every `group_b_*` directory and file name |
| Kept product: `app/examination/standalone/fixtures/` | Read at runtime by the lib tests in `group_b_fixture_consumer.rs`; no PR lib cohort runs them today, only the full suite, but a cohort filter change would. | `CARGO_MANIFEST_DIR` joins in Rust |
| Kept product: `app/tests/group_b_fixture_consumer.rs` | Compiled into the lib by `lib.rs` (`#[path]`): the test-target build and clippy in `rust-integration`. | `group_b` in `app/src-tauri` |
| Kept product: `app/tests/group_b_fixtures/` | `packaging/static_distribution/test_s1_value_model.py`, `sources-packaging`. | `group_b_*fixtures` outside the class |
| Kept product: `app/tests/group_b_sq_receiving_fixtures/` | `tests/package_successor_receiving_fixtures.py` through `package_successor_test.py`, `sources-packaging`. | as above |

`examination_repin_test.py` runs in `sources-packaging` and now also in
`repository-checks`, so that a standalone pin change is examined on the route it
takes. It uses only the standard library.

The three pull request product jobs do not run the Group B suites on macOS at
all, and did not before this narrowing: selecting them never supplied macOS
evidence for examination tests. The narrowing removes no macOS coverage from
them; their tests that need macOS itself get their own route, below.
`group_b_runner_test.mjs` is run by no CI route.

Deletions, mode or type changes, renames (each side examined), other file types
in these roots, non-ASCII and case-variant spellings and any change with a
product input keep the full product route.

The table rests on reading each consumer. `tools/ci/test_selection.py` adds a
warning, not a proof: it fails when a tracked code file outside the classes
names one of their paths in its text and is not a reader listed there with its
reason, so a new reader is noticed and placed in this table, or the path it
reads kept as a product input. A path assembled at run time, or reached through
data the search does not read, evades it. The same file fails if
`repository-checks` stops running, or makes conditional, a reader listed here.

## macOS examination tests

Some examination tests need macOS itself: libproc, live bundle metadata, macOS
process behaviour. They cannot run in the Ubuntu `repository-checks`, and the
three product jobs do not run the Group B suites. The `examination-macos` job in
`governance-harness.yml` runs them on `macos-26` with Python only: no setup
action, frontend build, Rust compile or supplier.

- **What it runs.** Every module named `app/tests/group_b_<name>_macos_test.py`
  in the commit's tree, found by that pattern, each in its own pytest run
  through `tools/ci/examination_tests.py macos`. A module that reports no test,
  a test that skips, fails or errors, a missing test report, or a run off macOS
  fails the job. A test skipped on macOS would run nowhere.
- **Disappearance.** The job also fails when the selector's merge base held at
  least one matching module and the head holds none, so removing the last one
  needs a deliberate change to the helper. The selector publishes the merge
  base it used as the `merge_base` output; the job's checkout is shallow, so it
  fetches that one commit (`git fetch --no-tags --depth=1 origin <merge base>`)
  and reads its tree. A merge base that is missing or cannot be inspected fails
  the job; only manual dispatch, which has none, skips this check. It catches the
  disappearance of the last matching module; it does not establish that every
  former test is still covered.
- **When it is selected.** On any change under `app/examination/` or to a path
  starting `app/tests/group_b_` (including deletions and either side of a
  rename); on a change to `tools/ci/examination_tests.py`, the selector or
  `governance-harness.yml`; on an unmatched path; on an empty change set; and on
  manual dispatch. It is selected alongside whatever else the change selects:
  a class B change alone selects repository checks and this job, and no product
  job. The `run_examination_macos` output carries the choice.
- **How a test joins it.** Put a test that needs macOS in a module matching the
  pattern, and make the module skip elsewhere by an explicit platform condition
  (for example `unittest.skipUnless(sys.platform == 'darwin', reason)` on each
  class, or `setUpModule` raising `unittest.SkipTest` off Darwin). The Ubuntu
  route still collects it and skips it there. Portable tests stay in other
  `group_b_*_test.py` modules.
- **The Ubuntu skip rule.** `repository-checks` runs every
  `app/tests/group_b*test.py` through `tools/ci/examination_tests.py portable`
  and judges the test report, not the source: a test may skip only if its module
  matches the macOS pattern or it is the one grandfathered test,
  `group_b_launch_home_test.py::OnlyTheIdentifiedCandidate::test_a_changed_resource_is_refused_and_the_identified_bundle_launches`.
  Any other skip fails the step and is named, including a skip at collection
  time (a module-level skip or `importorskip`) where no test reached execution.
  pytest's own failures and exit status still decide, and a missing or unreadable
  report fails. The rule is for the hosted route and does not forbid a deliberate
  local skip. A dependency newly missing on the runner fails the step, which is
  intended: the alternative is losing the verification silently. A further
  exception must name the route on which its test runs.
- **When there is nothing to run.** With no matching module at the head and
  none at the merge base, the job succeeds and says plainly, in its log, a
  notice annotation and the step summary, that nothing ran. On main when the job
  was added, no module matched. The grandfathered test runs only in the nightly
  full suite until it moves into a matching module.
- **Early warning.** `tools/ci/test_selection.py` also searches the source of
  `group_b` test modules outside the pattern for a Darwin-conditioned skip and
  reports one before CI does. It is a text search; the Ubuntu skip rule above is
  what decides.

`harness` requires `examination-macos` to succeed when selected and to be
skipped when not, exactly as for `app-v4`.

## Required result

The macOS reusable product workflow is called only when explicitly selected. It
needs only `change-selection`, so product jobs start as soon as the route is
known, not after the slower repository checks. `harness` runs with `always()`
and requires a successful `change-selection` with valid outputs and successful
repository checks. It accepts `app-v4: skipped` only for the explicit `prose`
selection, which every documentary, governing-text and examination change
alone receives, and `examination-macos: skipped` only when
`run_examination_macos` is `false`. A product selection requires `app-v4: success`; failures,
cancellations, unexpected skips and missing/inconsistent outputs block merging.
A failing repository check therefore blocks the merge although the product jobs
still run to completion.
No branch-rule change or product-check removal is needed.

The App workflow runs the focused build, Rust, Node and Python checks, plus
frozen-source regression checks. On PRs they run as three
parallel macOS jobs sharing `.github/actions/app-v4-setup`. Each job builds
the repository's own crates itself, on every run. The first compiles every default-feature test target in one
pass, replacing the separate check pass, then runs `cargo clippy --all-targets`
denying only the `clippy::correctness` and `clippy::suspicious` groups (other
lints stay warnings); the second rebuilds the lib test
target, and the third builds the successor feature and packaging example. Each
focused lib cohort filter sits in exactly one of two shards and still runs as
its own serial libtest process, because some tests read process-wide state that
others set. The workflow's `App v4 checks` job
requires all three to succeed. Selection tests execute that gate, check the
event conditions and reject a filter listed twice; they do not detect a removed
filter, so cohort changes need review like any other check change.
Manual App workflow dispatch
retains the broader supplier-dependent route; it is not a release and remains
subject to the owner's authorization and App hold. No release workflow is present.
Manual dispatch of the governance harness also always selects product checks.

## Rust dependency cache

Every macOS product job, including the full route, restores compiled third-party
dependencies in its setup and saves them as its last step. Only
`target/debug/.fingerprint`, `build` and `deps` are cached, under a key made of
the runner OS and architecture, the exact `rustc` build, `Cargo.lock` and the job
id. If that exact key is absent, the newest cache for the same OS, toolchain and
lockfile from another job is restored instead; the full route on main is what
seeds new PRs, because a PR can read only its own caches and main's. Registry
downloads and test results are not cached.

`tools/ci/rust_dep_cache.py` keeps the repository's crates out: it removes their
units before every save and again after every restore, using the package and
target names reported by `cargo metadata`. Cargo reuses a unit only when its
`.fingerprint` directory records it as fresh, so a repository crate without one
is compiled from the checked-out source regardless of file times.
`tools/ci/test_rust_dep_cache.py` demonstrates this with real cargo builds,
including a control run showing that an unpruned target would run stale code.
A cache miss, a failed restore, or restored output that cannot be cleaned becomes
a full build. A failed save never affects the job.

Pull requests from forks use neither this cache nor the npm cache, and always
build from the checkout. A cache archive is trusted as it was written, so an
earlier revision of a PR could otherwise leave a modified dependency, or a
replaced file in the checkout, for a later revision of the same PR to run. PRs
from branches of this repository keep both caches: their authors already hold
write access and control how the required check becomes green.

## Nightly full suite

PR selection can miss a test broken by a change elsewhere, because PR lib
cohorts are named filters, not the whole lib suite, and because a branch need
not be up to date with main when it merges (`AGENTS.md`). `nightly-full-suite.yml`
therefore runs on main at 09:00 UTC and on manual dispatch. It
calls `app-v4.yml` with `full_suite: true`, which takes the same full route as a
manual dispatch: the `product` job, including the full `cargo test` run, and
none of the focused PR jobs.

Its first job, `tools/ci/nightly_gate.py`, skips the suite on a scheduled run
when an earlier run on main, from any trigger, has a suite verdict on the same
commit. A suite verdict is the `App v4 product` job's own conclusion, success or
failure: a run stopped by a gate or runner failure, cancelled, or skipped has
none, whatever the workflow concluded. A manual run always runs, and if
the earlier runs or their jobs cannot be read, the suite runs.

The run tests main as it stands, so merges since the previous run are tested
together: a failure covers every commit since the last verified pass, meaning a
run whose `App v4 product` job succeeded.

A full run is slow: the `product` job took about 54 minutes on its first complete
pass. A bad combination of merges shows at the next nightly run. The `product`
job's limit is 120 minutes; the focused PR jobs keep 45.

The workflow reports a scheduled or manual run on main that fails, is
cancelled or times out: its `report` job, `tools/ci/nightly_report.py`, opens a
GitHub issue labelled `nightly`, or comments on the open one. The issue carries
the run URL and the commit SHA on lines of their own, the jobs that did not
pass, and the commits since the last verified pass with their PR numbers. If no
verified pass is found within the last 200 runs, or they cannot be read, the
issue says the baseline is unknown and lists no range. Only that job can write
issues. Commit subjects and job names are escaped so they cannot mention anyone.
Listing and publishing are retried with backoff; if publishing still fails, the
job fails visibly.

The independent path is portal, an assistant the owner runs outside this
repository, which reads the result at about 15:00 UTC each day and opens a
`nightly` issue on its own. A run that never
starts has no report job, so only that path catches it.

Agent 0 deals with an open `nightly` issue before merging or arming auto-merge.
Until the owner settles what that means, Agent 0's working reading is provisional:
decide, and say in the PR, whether the failure is caused by or affects the change,
and fix or revert one that does before merging, unless the PR is the fix. Agent 0
closes the issue when a later run's `App v4 product` job passes on a commit that
includes the failing change; a scheduled skip does not count. This duty is Agent
0's: the run is not a PR check and no ruleset requires it, so GitHub itself never
holds a merge for it.

Frozen examination sources are verified locally without Git fetches. Toolchain
and package setup in hosted CI retain their existing versions. Local checks use
offline caches by default. A fresh clone needs the documented toolchains and
dependencies, not a sibling Chirality checkout.

Repository checks also run `python app/examination/repin.py --check`, which
fails when examination source pins disagree with current bytes.

Credential/conflict checks are retained. The private-term check and its
validator were removed by owner direction on 2026-11-05.

The PR `sources-packaging` job explicitly runs `installed_custody::tests` and
`hosting::successor::tests::installed_s4` with `distribution-successor` enabled.
These source fixtures cover the None/debug/platform gates, synthetic signing
facts, exact S4 reader/Store joins, historical refusal, non-Codex resource
mutation and successor-only standing compatibility. They supply no signed-App
or packaged native witness. Existing `s2_` coverage remains selected separately.
The existing `production_cannot_be_overridden_by_development_fields` regression
also runs explicitly in that step, preserving its closure-resolution refusal
point as well as the new S4 checks.

The same job runs every `dev_model_address` test with the successor feature.
Built that way, the release-configuration tests show on the arguments a
fixture supplier is actually started with, at ordinary and successor start
and with `CHIRALITY_DEV_OPENAI_BASE_URL` present in the environment, that no
built-in provider address is passed and that the refusals tied to it are
absent. No real supplier is started.

The publisher-build follow-on also selects `publisher_recipe::` and
`publisher_selection::tests` in `sources-packaging`, with the successor feature.
These exercise the real recipe using isolated synthetic process environments,
generated compiler guards and runtime default-None behavior; no real publisher
input, signing or native/package qualification is part of these cohorts.

The SEAL-C signing transition explicitly selects `capture_seal` in the PR
`sources-packaging` job. It covers existing file-key behavior and the new mock
keychain enrollment/continuity/capture-cache cases. All real SecItem calls are
disabled in test builds; this cohort does not qualify a signed keychain provider.
