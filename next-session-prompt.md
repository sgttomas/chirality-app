You are taking over the next UI pass in `/Users/ryan/ai-env/projects/chirality-app`.

## Goal for this session
Move the interface away from an IDE/VS Code look while preserving behavior.

Primary design direction:
1. Break the “three equal editor panes” feel with a more intentional asymmetric layout.
2. Reduce hard box-grid chrome (fewer heavy separators, more layered surfaces/depth).
3. Keep the existing functional wins:
   - Diff mode (with full-document context and Changes Only collapse behavior).
   - Git state indicators in Project Directory.
   - Chat waiting/streaming/tool activity animations.
4. Keep the Portal identity visible in working views (subtle hex/command-center language), not an editor clone.

## Current functional baseline to preserve
1. Harness + SSE event contract must remain stable.
2. Project root selection must work in both places:
   - Session views via footer `DIR` flow.
   - Portal `Project` control (dashboard) opening `DirectoryPicker`.
3. Diff view supports:
   - `File` / `Diff` toggle
   - VS Code-style line rendering
   - full-file unified context
   - `Changes Only` collapse toggle
4. ChatPanel supports:
   - braille spinner while waiting
   - streaming cursor
   - tool run chips
   - `prefers-reduced-motion` fallbacks

## Hard constraints
1. Preserve palette semantics and Portal hex colors/labels.
2. Do not break existing API routes or SSE event typing.
3. Keep SSR-safe browser storage initialization in `frontend/app/page.tsx`.
4. Keep reduced-motion behavior functional for all new animations.
5. No destructive git actions and do not discard unrelated local changes.

## Branch-first workflow (required)
Before editing:
1. Check status and current branch:
   - `git status --short`
   - `git branch --show-current`
2. Create an experiment branch from current HEAD:
   - `git switch -c ui/non-vscode-polish-pass`
   - If that branch already exists, create a dated variant (example: `ui/non-vscode-polish-pass-2026-02-08`).
3. Keep commits small and thematic (layout/chrome, then motion/chips, then cleanup).

After implementation:
1. Validate:
   - `npm run lint` (in `frontend`)
   - `npx tsc --noEmit` (in `frontend`)
   - `npm run harness:validate:premerge` (in `frontend`)
   - quick manual smoke in `home/workbench/pipeline/direct`
2. Report:
   - what changed
   - files changed
   - visual impact summary
   - validation results
   - any known regressions/risks

## Merge / reversal instructions
If accepted:
1. Merge with history preserved:
   - `git switch <target-branch>`
   - `git merge --no-ff ui/non-vscode-polish-pass`

If rejected before merge:
1. Drop experiment safely:
   - `git switch <target-branch>`
   - `git branch -D ui/non-vscode-polish-pass`

If merged and later needs rollback:
1. Revert merge commit:
   - `git revert -m 1 <merge-commit-sha>`
