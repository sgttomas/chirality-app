# App development verification

`harness` remains the required check on every PR. Repository checks always run:
deliverable structure and utility tests, selection regressions, and the existing
conflict, credential and private-term checks. The workflow itself has no PR path
filter. This standalone repository does not execute SWBPIPE checks.

## Change selection

`tools/ci/select_checks.py` reads the complete committed change between the PR
merge base and head. It reports the base/head identities and a reason for every
path in the selection job's output and GitHub step summary. No GitHub files-list
pagination or extension-wide skip is used.

Only additions and modifications of ordinary non-executable files at these
exact documentary paths select repository checks without product verification:

- `AGENTS.md`
- `README.md`
- `init/README.md`
- `init/init-prompt.md`
- `loop/LOOP_INIT.md`
- `docs/CI_SELECTION.md`
- `execution/_Coordination/CURRENT_EXECUTION_BASIS.md`
- `execution/_Coordination/WINDOWS_UNDERTAKING.md`

Everything else retains the existing App product verification. This includes
Rust and frontend code, dependencies/locks, workflows, the selector and its
tests, schemas, packaging resources, examination/evidence/Work inputs,
packaged Markdown and unknown paths. Mixed changes select the union: one
product-relevant path selects the product workflow. Deletions, executable-mode
changes, symlinks and other file-type changes select product checks even at an
allowlisted path. Renames are examined as deletion plus addition, so neither
side can be hidden. An empty change set selects product checks. Invalid or
missing commit input, an unavailable or ambiguous merge base, and malformed Git
output fail selection and block the aggregate.

This is the first conservative selection increment. Other prose remains on the
product route until its consumers are examined and its path deliberately added.
There is no new partial frontend/Rust/schema test mapping in this increment.

## Required result

The macOS reusable product workflow is called only when explicitly selected.
`harness` runs with `always()` and requires successful repository checks and
valid selection outputs. It accepts `app-v4: skipped` only for the explicit
`prose` selection. A product selection requires `app-v4: success`; failures,
cancellations, unexpected skips and missing/inconsistent outputs block merging.
No branch-rule change or product-check removal is needed.

The App workflow runs the focused build, Rust, Node and Python checks, plus
frozen-source regression checks. On PRs they run as three
parallel macOS jobs sharing `.github/actions/app-v4-setup`. Each job builds
its own artifacts. The first compiles every default-feature test target in one
pass, replacing the separate check pass; the second rebuilds the lib test
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

Frozen examination sources are verified locally without Git fetches. Toolchain
and package setup in hosted CI retain their existing versions. Local checks use
offline caches by default. A fresh clone needs the documented toolchains and
dependencies, not a sibling Chirality checkout.

Credential/conflict checks are retained. Same-repository PRs require the
`PRIVATE_TERMS` repository secret; its value is private and never committed.

The PR `sources-packaging` job explicitly runs `installed_custody::tests` and
`hosting::successor::tests::installed_s4` with `distribution-successor` enabled.
These source fixtures cover the None/debug/platform gates, synthetic signing
facts, exact S4 reader/Store joins, historical refusal, non-Codex resource
mutation and successor-only standing compatibility. They supply no signed-App
or packaged native witness. Existing `s2_` coverage remains selected separately.
