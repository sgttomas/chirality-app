# App v4 development entry

Work in `projects/chirality-app-v4` relative to the repository root. Read Root
`AGENTS.md`, the assigned role, `docs/PRD.md` and its named companions, and the
affected deliverables under `execution/PKG-*/1_Working/DEL-*/`. ScopeOfWork and
Design hold commitments; `Dependencies.csv` holds needs until the pilot
migration. Query only the relevant neighbourhood; the deliverable CLI will
replace manual dependency discovery when it lands. Build and test entry points
are in `app/README.md`. Use `coordinated-knowledge-work` for coordination.
The current objective comes from the init prompt and subsequent owner steering.

Decisions edit the current source they govern. Interface changes are named,
reviewed and propagated to their consumers in the same change. The PR is the
change record; do not maintain progress, receipt or decision registers.

Hard boundaries:
- The owner assesses stage gates and reserves commitment and acceptance changes.
- SWBPIPE, PEC and Domains implementation remains in its owning project; the
  interface basis is `execution/_Coordination/HANDOFF_SWBPIPE_DOMAINS.md`.
- App v3 is `projects/chirality-app-dev`; its product tools and decisions do not
  apply to App v4. Leave `foundation/thesis/` unchanged.
- Development or test Codex uses a scratch home made with `mktemp -d`, never
  `~/.codex`; configure it as `app/README.md` describes.
- Do not sign in or use credentials without the owner.
- Downloads require explicit owner permission; identify the file, source and
  size first. Build offline by default.
