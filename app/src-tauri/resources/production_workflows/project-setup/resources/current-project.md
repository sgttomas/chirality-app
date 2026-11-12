# Current PROJECT/SOFTWARE setup

Use this route for the adopted `execution/PKG-nn/DEL-nn-nn/` locality. The project
owns its commitments, paths and authority. Preserve any existing accepted layout
until a move is explicitly authorized; do not infer conversion from reading this
method. The phase/control-file and DOMAIN routes are the separate, explicitly
selected `project-setup-retained` workflow.

## Basis and selection

Read the accepted decomposition and selected activation scope. Preserve identifiers,
names, objective/scope references, anticipated outputs, constraints and unresolved
conditions. Where the decomposition states them, also preserve each deliverable's
expected examination, objective checks with their carriers, the thin end-to-end
path and any coupled core. Apply already-authorized decisions without asking again. A changed
commitment needs its actual owner decision before dependent setup; a formal
scope-change project uses its accepted amendment as that source. Do not manufacture
an amendment or lifecycle gate for ordinary factual reconciliation.

Inspect the relevant existing localities before writing. Classify each as absent,
structurally prepared, authored, or inconsistent from its actual files; these are
observations for this operation, not persisted lifecycle states. An existing empty
file is existing work. Preserve unrelated files, accepted evidence and explicit
holds. A conflicting identity or source stops the affected operation; continue
unaffected work where its inputs permit it.

## Entry instructions when selected

For authorized creation or revision of a project's entry, consult
[project entry and standing instructions](project-entry.md). Preserve the
project's accepted layout until its own authority changes it, and record only
actual owner grants.

## Structural preparation

Apply the selected library's `preparation` instructions. Current helper calls are:

```sh
zsh tools/scaffolding/scaffold_package.sh --current <execution-root> <PKG-ID> <accepted-name>
zsh tools/scaffolding/scaffold_deliverable.sh --current <package-path> <accepted-DEL-ID> <accepted-name>
zsh tools/validation/check_min_viable_fileset.sh --current --prepared <DEL-path> <accepted-DEL-ID>
```

Use actual values rather than the illustrative placeholders. Python 3/PyYAML
are required; `PYTHON` selects an interpreter with those dependencies.

The package helper creates only the numeric package folder. The deliverable helper
creates its numeric folder and an initial `deliverable.yaml` with the
accepted identity/name and `needs: []`. It preserves existing content and reports
only paths it created. A suffix-bearing accepted description remains in the
decomposition; it does not create another directory level or duplicate suffix.

These helpers create no `_STATUS.md`, `_CONTEXT.md`, `_REFERENCES.md`, `_SEMANTIC.md`,
phase directories, memory file or blank `ScopeOfWork.md`. No need completeness,
readiness, lifecycle or acceptance follows from an empty needs list or a pass.

## Production authoring and needs

For a missing contract, use `scope-of-work` `MODE=INIT` with accepted decomposition,
scope/objective references, allowed writes and `STATUS_POLICY: NO_STATUS_TOUCH`.
Author the real `ScopeOfWork.md` directly, then validate its format and content
with the method's tools. An absent lifecycle file remains absent. Existing
contracts are read and reconciled; never rerun initialization over them.

Each verification entry that setup authors states its kind as `scope-of-work`
defines it, drawing on the decomposition's expected examination where one is
stated. Setup does not relabel entries in contracts it did not author.

Where the project's standing instructions call for independent scrutiny of a
class of change, for example numerical meaning, persistence, permissions or
destructive operations, someone who did not write the entry asks whether it
could pass while the criterion is unmet, before dependent implementation
relies on it. This is proportionate examination under the project's own
rules. It is not a setup gate and names no standing reviewer.

After authoring, check the current locality without `--prepared`; this checks
presence and identity, separately from substantive ScopeOfWork validation:

```sh
zsh tools/validation/check_min_viable_fileset.sh --current <DEL-path> <accepted-DEL-ID>
python3 tools/scope_of_work/validate_scope_of_work.py <DEL-path>/ScopeOfWork.md --json
```

Once local scope exists, use `dependency-extract` to author actual inputs/use
conditions in each consumer's `deliverable.yaml`, retaining source references,
cases, unknown bindings and technical holds. Preserve unchanged needs. Update
code/check pointers when their useful bindings change. Queries derive reverse
links and relevant neighborhoods; there is no second dependency register.

Use `python3 -m tools.deliverables --project <project> check` and a bounded
`neighborhood`, `impact` or `touches` query where applicable. The current query
CLI requires Git/HEAD and PyYAML. If unavailable, inspect sources directly and
state the limit. A successful query cannot decide suitability or acceptance.

## Reconciliation before integration

The implementation owner names affected deliverables in each assignment; TASK
returns identify changes in meaning, evidence and remaining conditions. Compare
the actual result with its ScopeOfWork and needs before integrating it.
Use `bounded-reconciliation` for this comparison, including ordinary factual
ScopeOfWork updates within already-given authority. Preserve commitments and
acceptance criteria unless their actual decision owner has authorized a change.

If no edit is warranted, say so briefly in the return or PR. Agent 0/the
integration owner checks that the implementation and declarations agree before
merge.

Describe the change at a high level in the PR. Existing explicitly adopted
acceptance snapshots keep their standing.

## Changes and resumption

For added scope, repeat preparation and authoring only for the selected additions.
For existing scope, update meaning where authorized and verify the result. Derive
affected neighbors from actual conditions. Retiring or moving a source requires
its own authority and inspection of consumer uses; do not automatically delete
or redirect a need because a producer changes status.

After interruption, inspect actual source files and PRs to resume
the unfinished operation. A missing run log is not a blocker. Do not treat an
accepted checkpoint, file existence or an old activity record as new authority
to continue work, publish or release.

## Accepted scope amendments

When `scope-change` hands an accepted current-project amendment back, this is
the incremental setup route; the `INCREMENTAL` control-file profile of
`project-setup-retained` is not selected implicitly. Bind the exact group-3 accepted amendment and its
propagation decisions before setup. Prepare only accepted ADD localities, then
use `scope-of-work INIT` for their missing contracts. For deferred MODIFY or
scope-changing RECLASSIFY contract edits, use current-project `REVISE` with the
accepted named actions, prior valid contract/hash and exact revision scope.
If the amendment already made the contract edit, verify it rather than repeat it.

For retirement or remapping, preserve the accepted historical source and IDs,
check affected consumers, and implement only the accepted disposition. Do not
create status/control files or infer a reopening from an issued library edition.
Use `dependency-extract` for affected native needs and `audit-dep-closure` for a
bounded query over the resulting declarations. For implementation and
propagation closure, use the current-project route of `audit-scope-closure`.
Report remaining obligations explicitly. Obtain the required product acceptance
and release decisions separately, and keep changes within the authorized scope.
