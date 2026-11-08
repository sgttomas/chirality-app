---
name: chirality-app-development-verification
description: Explain how changed paths select repository and product checks.
metadata:
  kind: instruction
  surface: reference
---
# App development verification

`harness` remains the required check on every PR. Repository checks always run:
deliverable structure and utility tests, selection regressions, and the existing
conflict and credential checks. The workflow itself has no PR path
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
- `init/README.md`
- `init/init-prompt.md`
- `loop/LOOP_INIT.md`
- `docs/CI_SELECTION.md`
- `docs/OPERATING_METHOD.md`
- `docs/user-manual/README.md`
- `execution/_Coordination/CURRENT_EXECUTION_BASIS.md`
- `execution/_Coordination/PUBLICATION_PUNCHLIST.md`
- `execution/_Coordination/WINDOWS_UNDERTAKING.md`
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
current imports/interpreter invocations into it. Its nine hash-bound exceptions
are fidelity-only supplier receipts and the historical acceptance presentation;
they grant no execution permission. This is a source/layout guard, not a proof
about arbitrary dynamically computed programs. Changes introducing a new
execution mechanism must extend its checks and receive review.

Product consumers read selected App schema/fixture copies. Always-on repository
checks compare those copies with their authoring source, using full bytes or the
existing documentary selector extents, and retain the examination pin checks.
Group B correspondence tests now run in repository checks on every PR, together
with `check_documentary_sources.py`: live projection groups and all their
selectors remain checked against authoring prose. Historical source profiles,
publication identities and frozen bytes retain their distinct subjects. A
selected source change requires reviewed reconciliation of its copy and pins;
this layout does not authorize adoption or repinning historical evidence.

The selector regression fixtures replay the complete recorded changes for
PRs 169–181, plus unknown-path, mixed-change, mode, deletion and rename cases.
Twelve sweep PRs become repository-only; PR178 retains product verification
because its change includes product-selected documentation outside `execution/`.
This PR's moves and all App/tool/guard/selector edits select full product checks.
Other product domains remain conservative; no partial frontend/Rust mapping is
introduced.

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
