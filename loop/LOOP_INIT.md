# App v4 development entry

The current release pathway and continuing Type 1 owners are in
`execution/_Coordination/CURRENT_EXECUTION_BASIS.md`. Read local `AGENTS.md`
for shared-library selection and current constraints. HELP_HUMAN coordinates
the dedicated manager sessions through T3 chat; managers retain delivery
ownership through repairs, reconciliation, review and cleanup.

Use the actual current PRs and assigned manager routes in that execution basis.
The platform baseline, project authority and protected boundaries are in
`AGENTS.md`; historical sessions are not active dispatch routes.

Chirality makes a general agent act within and for a host application; its own
workflow-authoring App is the exemplar. Work at this repository root.
Start from the affected `execution/PKG-nn/DEL-nn-nn/` and its ScopeOfWork,
Work and dependency conditions. Consult `docs/PRD.md` and its companions for
requirements and interfaces involved in this slice, not as a compulsory census.

From the repository root:

```sh
python3 -m tools.deliverables --project . neighborhood DEL-10-01
```

Use `impact <DEL>` for downstream reach and `touches <rev|PR:n>` to locate
relevant deliverables. `dag-diff app-v4/deps-baseline-1` compares with the
reproducible migration baseline; it does not imply separate owner acceptance of
the generated YAML. Update needs only when their conditions change. An interface
change identifies affected consumers and coordinates adoption across repositories.

Each implementation return must reconcile its affected `ScopeOfWork.md`,
`Work/` and dependency conditions in `deliverable.yaml` against the implemented
behaviour and verification evidence before integration. Update changed meaning
in the same change; leave unchanged declarations alone. The return identifies
the reconciliation and any remaining conditions or reserved choices.
References written before 2026-10-30 to a deliverable's `Design/` mean its `Work/`.

Resolve shared methods through the edition selected in `AGENTS.md`, retaining
its exact revision with dependent results. The local `workflows/` directory
holds project methods and retained test inputs; a matching name does not replace
the selected Library source. Use the coordination method only when related
contributions need it. An opted-in session sends summaries and pre-merge
consultations to its existing INTERLOCUTOR child; independent reviews are separate.

Build/test entry points and scratch Codex configuration are in `app/README.md`.
Choose checks for the changed behaviour under this repository's verification rule; CI
selection is in `docs/CI_SELECTION.md`.

Apply the standing Git grant, verification tiers, scratch-home rules and holds
in `AGENTS.md`. App v3 remains frozen in its release tags; its product tools do
not select v4 behavior. The cross-project interface basis is
`execution/_Coordination/HANDOFF_SWBPIPE_DOMAINS.md`; PEC is retired and is not
an App prerequisite.
