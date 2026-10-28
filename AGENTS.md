# Chirality App repository instructions

This repository owns App v4. Development is on hold at the owner's direction;
only the currently authorized migration and its verification may proceed. No
feature work, qualification advancement or release is authorized by migration.

Enter through `loop/LOOP_INIT.md`. Requirements and interfaces live in `docs/`;
deliverables retain their `execution/PKG-nn/DEL-nn-nn/ScopeOfWork.md`, `Design/`
and `deliverable.yaml` conventions. Reconcile changed implementation meaning
with those documents; leave unchanged commitments and historical evidence alone.
Do not modify `foundation/thesis/`.

Use `python3 -m tools.deliverables --project . check`, `neighborhood <DEL>`,
`impact <DEL>` or `touches <revision>` from this repository. Build/test setup
is in `app/README.md`. Shared methods may be consulted from an explicitly
selected Chirality library, such as `https://github.com/sgttomas/chirality`;
ordinary build and test execution must not require a sibling checkout. The
local `workflows/coordinated-knowledge-work` copy is a pinned App test input.
Shared input and migration provenance lives in `reference/migration/`.

Work within the owner's current steer. Use focused checks for ordinary changes;
changes affecting persistence, permissions or destructive operations require
targeted regression checks and independent scrutiny. Preserve truthful source
identity and report unrun checks as limitations. Commitments, acceptance,
releases and lifting holds remain owner decisions.

Use isolated migration branches and PRs. The migration must preserve existing
release tags and imported ancestry through merge commits; do not squash it.
No force pushes, protection bypasses, permission changes or release actions.
SWBPIPE remains in `sgttomas/chirality` and is outside this repository's scope.

Use a fresh scratch Codex home for development/tests, never `~/.codex`.
Do not sign in or use credentials without the owner. Build offline by default;
downloads require explicit permission identifying the file, source and size.
No live examination is authorized merely to verify this repository migration.
