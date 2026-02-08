You are taking over UI polish implementation in `/Users/ryan/ai-env/projects/chirality-app`.

Source of truth:
- `frontend/docs/ui/UI_POLISH_EXECUTION_PLAN.md` (latest cosmetic-pass notes dated 2026-02-08).

Current baseline already completed:
- Slice #1 (`globals.css` foundation + reusable classes) is done in `878872d`.
- Slice #2 (`page.tsx` shell polish + `ResizableLayout.tsx` shared footer/root-selector polish) is done in `ddfc3ab` and `474a023`.

Implement now:
- Continue with Suggested Slice Order #3 only.
- Primary target: `frontend/components/DashboardList.tsx`.
- Keep this batch style-first, minimal, reversible, and focused.
- Do not jump ahead into ChatPanel or broad cross-component rewrites.

Hard constraints:
1. Preserve palette values and semantic meaning.
2. Preserve Portal hexagon colors and labels.
3. Preserve harness/SSE behavior contracts.
4. Keep project-root picker centralized in `frontend/components/ResizableLayout.tsx`.
5. Keep SSR-safe browser-storage init pattern in `frontend/app/page.tsx` (no hydration mismatch regressions).
6. Keep ChatPanel status-text-first loading/tool feedback direction.

Execution protocol:
1. Confirm repo status first (do not discard existing local changes).
2. Implement Slice #3 scope only.
3. Validate with:
   - `npm run lint`
   - `npx tsc --noEmit`
   - quick manual smoke for `home/workbench/pipeline/direct`
4. Report:
   - Completed slice tasks
   - Files changed
   - Validation outcomes
   - Risks/blockers
   - Next recommended slice
5. Commit with a concise message for this slice.
