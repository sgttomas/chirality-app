# change — method

## Method

A WORKING_ITEMS session follows a short flow; the mechanics of each step are ordinary Git competence and left to agent judgment.

1. **Initialize.** Resolve `EXECUTION_ROOT` and the session identity, note whether the `_Change/` tool roots exist (do not create directories without approval), and record the defaults/assumptions used.
2. **Collect state evidence (read-only).** Gather current branch and HEAD, upstream, staged/unstaged/untracked summaries, renames/deletions, ahead/behind status, existing worktrees, relevant task branches, and any in-progress Git operation. Do not fetch or mutate state.
3. **State Report.** Produce a decision-ready report with strict separation of Observations, Interpretations, Risks, and Options (see STRUCTURE). Default to low noise; show full diffs only when needed.
4. **Plan (if requested).** Write a Change Plan (files, edits, why; flag any destructive operation). For concurrency, classify `SHARED_MONOREPO` vs `ISOLATED_WORKTREE` and, when isolating, produce a Worktree Lane Plan recording purpose, owner, base ref + SHA, scope paths, and expected closure/checks; check for name collisions and never base a new lane on a dirty worktree without explicit approval. For merges, summarize readiness in the existing PR, classifying each lane `READY` / `CONDITIONAL` / `BLOCKED` (never propose a merge for a `BLOCKED` lane except as a deliberate human-approved exception with risks stated). When the work reveals a workflow or tool design need, describe the observed friction and required behavior for HELPS_HUMANS. WORKING_ITEMS implements an accepted design only within its authorized undertaking.
5. **Execute within authorization.** For Chirality, stage only scoped changes and commit, push, open/update the PR, and merge under the standing grant in `docs/PRD_ROOT.md` §5.3.1. Inspect required CI and independent review for the actual candidate, reassess affected checks after changes, and verify source HEAD at merge. Explicit holds and unresolved blocking findings prevent merge. Use the owner's configured authenticated identity and report the PR/source/merge revisions with truthful attribution. Actions outside the grant require separate explicit authorization; covered Git operations require no approval token.
6. **Optional session log.** If a log path under `{EXECUTION_ROOT}/_Change/` is provided, record session identity, assumptions, state report, any lane plan / readiness report / merge result / design handoffs, approved actions executed, and resulting state.

---
