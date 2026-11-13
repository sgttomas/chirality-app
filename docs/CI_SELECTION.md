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

The `change-selection` job checks out the PR's head and runs that head's own
`select_checks.py`, not main's. A branch cut before a selector change is
therefore judged by the old selector until it takes main.

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
may already have merged them), fold to the same name. Its folding is Unicode
compatibility normalization, case folding and dropping format characters: at
least what a case- and normalization-insensitive macOS volume folds, without
claiming to model any file system exactly.

**An assumption this selector requires: the tracked tree holds no symbolic link
and no gitlink.** The inventory inspects the committed Git modes 120000
(symbolic link) and 160000 (gitlink), resolves no target, and fails on either
anywhere in the tracked tree, dangling links and directory aliases included.
The selector routes by path, and a link lets one path stand for another: a
product reader reaching a class path through a link would lose its product job
on a change to that class path. Generated and untracked links are outside the
inventory's scope. A future legitimate tracked link needs a reviewed change to
this assumption and to the routing. Classify an unmatched path deliberately;
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
repository checks on every PR.

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
| B: `app/examination/standalone/**` except `fixtures/` (`.py`, `.mjs`, `.cjs`, `.js`, `.json`, `.md`) | The Group B suites (`app/tests/group_b*test.py`), `repin.py --check` and `examination_repin_test.py` (which copies the standalone pin profiles), all in `repository-checks`; `native_forms/` reads the pre-run inputs and pins and is run only by `group_b_native_forms_test.py`. `app/examination/scripted_driver/proof.py` reads `operated/first-use-setup.scenario.json` in the scripted driver's own hosted job (`.github/workflows/app-scripted-driver.yml`, whose path trigger names that file), and `group_b_scripted_driver_test.py` reads it in `repository-checks`. | every top-level standalone entry name, `standalone`, `group_b` |
| B: `app/tests/group_b_*` except below (same types) | Run only by the `repository-checks` step `pytest -q app/tests/group_b*test.py`; no macOS product step names `group_b`. | every `group_b_*` directory and file name |
| Kept product: `app/examination/standalone/fixtures/` | Read at runtime by the lib tests in `group_b_fixture_consumer.rs`; no PR lib cohort runs them today, only the full suite, but a cohort filter change would. | `CARGO_MANIFEST_DIR` joins in Rust |
| Kept product: `app/tests/group_b_fixture_consumer.rs` | Compiled into the lib by `lib.rs` (`#[path]`): the test-target build and clippy in `rust-integration`. | `group_b` in `app/src-tauri` |
| Kept product: `app/tests/group_b_fixtures/` | `packaging/static_distribution/test_s1_value_model.py`, `sources-packaging`. | `group_b_*fixtures` outside the class |
| Kept product: `app/tests/group_b_sq_receiving_fixtures/` | `tests/package_successor_receiving_fixtures.py` through `package_successor_test.py`, `sources-packaging`. | as above |

`examination_repin_test.py` runs in `sources-packaging` and now also in
`repository-checks`, so that a standalone pin change is examined on the route it
takes. It uses only the standard library.

The three pull request product jobs do not run the Group B suites on macOS at
all, and did not before this narrowing: selecting them never supplied macOS
evidence for examination tests. Examination tests that need macOS run where
they ran before: in the nightly full suite (`App v4 product` runs
`python -m pytest -q tests`) and in a lane's own local runs. That is unchanged
by this narrowing, neither a gain nor a loss. `group_b_runner_test.mjs` is run
by no CI route.

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

## Required result

The macOS reusable product workflow is called only when explicitly selected. It
needs only `change-selection`, so product jobs start as soon as the route is
known, not after the slower repository checks. `harness` runs with `always()`
and requires a successful `change-selection` with valid outputs and successful
repository checks. It accepts `app-v4: skipped` only for the explicit `prose`
selection, which every documentary, governing-text and examination change
alone receives. A product selection requires `app-v4: success`; failures,
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
event conditions and reject a filter listed twice. The
[library test listing](#library-test-listing) catches a new test module that
no filter selects and most removed filters, with the limits it states; web test
files have the [web test listing](#web-test-listing).
Manual App workflow dispatch
retains the broader supplier-dependent route; it is not a release and remains
subject to the owner's authorization and App hold. No release workflow is present.
Manual dispatch of the governance harness also always selects product checks.

## Web test listing

Each web test file, `app/tests/**/*.test.mjs`, is named on a `node --test` line
of a pull-request job in `app-v4.yml`, or in `tools/ci/web_test_exclusions.txt`
with the reason no pull-request job can run it and where it does run (the full
route's `npm test`, or nowhere). `tools/ci/check_web_test_listing.py`, run by
`repository-checks` through `tools/ci/test_web_test_listing.py`, fails, naming the file,
when a test file is in neither, when a file named on a line it reads or in the
list does not exist, when a file is in both, and when it finds no test files or
no pull-request `node --test` line. A line it reads is a `node --test` command
at the start of a shell command in a step, after any `NAME=value` words. Jobs
are told apart by their `if`: the focused-route condition makes a pull-request
job, a job with no `if` counts as one (it runs on the pull-request call too),
and the full-route condition makes the full route, whose lines do not count. A
job with a `node --test` line and any other condition fails the check, naming
the job. A new web test file therefore needs a line or an exclusion in the same
PR. A file whose test starts `cargo test --lib` belongs in a job that has
already built the default lib test target (`rust-lib-node` after its shard, or
`rust-integration` after its compile step); one that runs an integration test
target belongs in `rust-integration`.

The check reads spelling in a workflow file. It does not show that a listed
test executes or passes, and does not read `app/package.json`'s test script. It
does not see a file reached only through a shell variable, a `node --test` line
that is not at the start of a command, or a web test under a name pattern other
than `*.test.mjs`, such as `group_b_runner_test.mjs`.

## Library test listing

`tools/ci/check_lib_cohorts.py` runs in `rust-integration` right after the
test-target compile. It lists the library's default-feature tests and its
ignored tests from that build and checks them against the workflow and
`tools/ci/lib_cohort_exclusions.txt`, reading the workflow with the Python
standard library (the macOS job has no YAML library). Its logic is tested with
invented lists in `repository-checks` (`tools/ci/test_lib_cohorts.py`), which
also compares its reading of the committed workflow with PyYAML's, job by job
(job ids, conditions, `LIB_COHORTS`, and each step's name, `if`,
`LIB_COHORTS` and run text, exactly) and fails on any difference. Listing a built target
took 0.2 seconds locally on this project's Mac; no hosted figure is recorded.

What it establishes: every test in the supplied default-feature listing is
either matched by name by a default-feature pull-request filter (a
`LIB_COHORTS` entry of a shard whose cohort step's run text is exactly the
cohort loop the check holds as `COHORT_LOOP`, compared by equality, or the one
literal filter of a `cargo test --lib` command in a pull-request job's step),
or ignored, or covered by a line of the
exclusion file with its reason. "Selected" is that name match; it does not show
that the test's body runs. An ignored (`#[ignore]`) test counts as neither
selected nor left to the full route: the full route runs `cargo test` without
`--ignored`, so it does not select ignored tests directly, though a parent test
it runs may start one as a child process. Each has a line saying so, either
opt-in, run by no hosted job unless someone names it, or a child process that a
named parent test starts, running only where that parent runs.

It fails, naming them, on a test in none of those, an ignored test without such
a line, a default-feature pull-request filter that selects no test that is not
ignored, and an exclusion line that covers no test. It refuses, naming the job
and step and giving the line, what it does not read: more than one test
filter, `--skip` or `--ignored` on a library test command; a step-level
`LIB_COHORTS`; a step-level `if` on a step that has a library test command
(it does not evaluate step conditions); a filter containing `$` in any run
text that is not exactly `COHORT_LOOP` (restore the script, or change the
constant with it and say why in the pull request); `LIB_COHORTS` without that
step, or that step without `LIB_COHORTS`; an anchor, alias or merge key
anywhere in the jobs; a
line it does not recognise (including a value on the next line), flow forms
where it reads below, and value forms it does not read exactly.

What it does not establish: that a selected test passes; anything about tests
compiled only with a feature; anything about a reason's text beyond the ignored
marker, such as the named feature step, web fixture, parent test or the full
route's command. A test left to the full route runs on main nightly and on a
product dispatch, not on the pull request that changes it. A module line covers
the tests directly in that module that no filter selects, so a new submodule
needs its own cohort or line, but a new direct test in an excluded module is
covered without notice; and removing a filter that selected a direct test of an
excluded module is absorbed the same way, with the check still passing.

The file is refreshed after cohorts change by the command in its header, which
removes lines that cover no test or name a selected test and adds none.

## Records presence spelling

The records store asks whether something is there through `records_inspect`, which
keeps "not there" apart from "not known" and does not follow a link at the final
entry (a link among the ancestors can still be followed).
`tools/ci/check_records_presence.py`, run by `repository-checks` through
`tools/ci/test_check_records_presence.py`, reads the raw text of every line of the
records modules' files (`app/src-tauri/src/records*.rs`, leaving out only files
named `*_tests.rs`) and finds each line that spells `exists`, `is_dir`, `is_file`
or `is_symlink` as a whole word after a dot or `::`, with or without white space
between: a method call, a path-qualified call (`Path::exists(path)`) or a function
reference (`is_some_and(Path::is_dir)`) alike, whatever follows the name. It does
not interpret the language: a spelling in code, a comment or a
string is found alike. Each such line must be on the reviewed list
`tools/ci/records_presence_list.yaml`, keyed by its file and the line's own text,
with its kind and reason: `metadata`, `path` (which also says what its caller
concludes when it cannot tell), `test`, `comment`, `string`, or `outside`. The check
fails on a new such line and on a listed line no longer found. A kind only
describes: every listed line takes part in the same accounting of exact text and
number of copies, and no kind exempts a line or loosens the count.

The check reads spelling, not meaning. It notices a new spelling, or one more copy
of a listed one. It does not notice a change of meaning around a listed line whose
text stays the same, such as a caller concluding something new from the same call:
that is why each `path` entry carries its `cannot_tell`, and it is what a reviewer
of a change near a listed line still has to read. The kinds `test`, `comment` and `string` are
the reviewer's statement: the check does not verify them. It does not see
a spelling whose dot or `::` and name are divided by a line boundary (any boundary
Python's `splitlines` recognises, a form feed and U+2028 among them), `try_exists()`,
an alias, a wrapper, a macro that does not spell the name, a `use` that renames, or
a module outside `records*.rs` that reads the store. Files named
`*_tests.rs` are left out by name; each such records file is compiled only under a
test configuration (found by searching the crate for each file's name and reading
the attribute or enclosing module of its one declaration). Its passing says only
that no new such spelling appeared in its scope.

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
