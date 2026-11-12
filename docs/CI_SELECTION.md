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

Everything else retains the existing App product verification. This includes
Rust and frontend code, dependencies/locks, workflows, the selector and its
tests, App schema/fixture copies, packaging resources, examination readers,
packaged Markdown and unknown paths. Mixed changes select the union: one
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
positive rules and fails on unmatched paths. Classify such a path deliberately;
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

## Required result

The macOS reusable product workflow is called only when explicitly selected. It
needs only `change-selection`, so product jobs start as soon as the route is
known, not after the slower repository checks. `harness` runs with `always()`
and requires a successful `change-selection` with valid outputs and successful
repository checks. It accepts `app-v4: skipped` only for the explicit `prose`
selection. A product selection requires `app-v4: success`; failures,
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

The publisher-build follow-on also selects `publisher_recipe::` and
`publisher_selection::tests` in `sources-packaging`, with the successor feature.
These exercise the real recipe using isolated synthetic process environments,
generated compiler guards and runtime default-None behavior; no real publisher
input, signing or native/package qualification is part of these cohorts.

The SEAL-C signing transition explicitly selects `capture_seal` in the PR
`sources-packaging` job. It covers existing file-key behavior and the new mock
keychain enrollment/continuity/capture-cache cases. All real SecItem calls are
disabled in test builds; this cohort does not qualify a signed keychain provider.
