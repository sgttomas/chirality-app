# App v4 development entry

Chirality makes a general agent act within and for a host application; its own
workflow-authoring App is the exemplar. Work in `projects/chirality-app-v4`.
Start from the affected `execution/PKG-nn/DEL-nn-nn/` and its ScopeOfWork,
Design and dependency conditions. Consult `docs/PRD.md` and its companions for
requirements and interfaces involved in this slice, not as a compulsory census.

From the repository root:

```sh
python3 -m tools.deliverables --project projects/chirality-app-v4 neighborhood DEL-nn-nn
```

Use `impact <DEL>` for downstream reach and `touches <rev|PR:n>` to locate
relevant deliverables. `dag-diff app-v4/deps-baseline-1` compares with the
reproducible migration baseline; it does not imply separate owner acceptance of
the generated YAML. Update needs only when their conditions change. An interface
change identifies and updates its affected consumers in the same change.

Build/test entry points and scratch Codex configuration are in `app/README.md`.
Choose checks for the changed behaviour under Root's verification rule; CI
selection is in Root `docs/CI_SELECTION.md`.

Hard boundaries:
- The owner assesses stage gates and reserves commitment and acceptance changes.
- SWBPIPE and Domains implementation remains in its owning project; the
  interface basis is `execution/_Coordination/HANDOFF_SWBPIPE_DOMAINS.md`.
  PEC is retired; App work does not wait on it.
- App v3 is `projects/chirality-app-dev`; its product tools and decisions do not
  apply to App v4. Leave `foundation/thesis/` unchanged.
- Development or test Codex uses a scratch home made with `mktemp -d`, never
  `~/.codex`; configure it as `app/README.md` describes.
- Do not sign in or use credentials without the owner.
- Downloads require explicit owner permission; identify the file, source and
  size first. Build offline by default.
