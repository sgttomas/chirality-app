# App v4 development entry

The current release pathway and continuing Type 1 owners are in
`execution/_Coordination/CURRENT_EXECUTION_BASIS.md`. Read local `AGENTS.md`
for shared-library selection and current constraints. HELP_HUMAN coordinates
the dedicated manager sessions through T3 chat; managers retain delivery
ownership through repairs, reconciliation, review and cleanup.

At the owner's 2026-10-30 transition, start the fresh App Agent 0 through this
entry. macOS is the release baseline; Windows is a Type 1 contribution under
the same project Agent 0, who owns shared code and design. Use actual current
PRs and assigned manager routes; do not dispatch to a retired Windows session.

Chirality makes a general agent act within and for a host application; its own
workflow-authoring App is the exemplar. Work at this repository root.
Start from the affected `execution/PKG-nn/DEL-nn-nn/` and its ScopeOfWork,
Work and dependency conditions. Consult `docs/PRD.md` and its companions for
requirements and interfaces involved in this slice, not as a compulsory census.

From the repository root:

```sh
python3 -m tools.deliverables --project . neighborhood DEL-nn-nn
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

Build/test entry points and scratch Codex configuration are in `app/README.md`.
Choose checks for the changed behaviour under this repository's verification rule; CI
selection is in `docs/CI_SELECTION.md`.

Hard boundaries:
- The owner assesses stage gates and reserves commitment and acceptance changes.
- SWBPIPE and Domains implementation remains in its owning project; the
  interface basis is `execution/_Coordination/HANDOFF_SWBPIPE_DOMAINS.md`.
  PEC is retired; App work does not wait on it.
- App v3 is frozen and recoverable through the existing release tags; its product
  tools and decisions do not apply to App v4. Leave `foundation/thesis/` unchanged.
- Development or test Codex uses a scratch home made with `mktemp -d`, never
  `~/.codex`; configure it as `app/README.md` describes.
- Do not sign in or use credentials without the owner.
- Downloads require explicit owner permission; identify the file, source and
  size first. Build offline by default.
