# Chirality UI Polish Execution Plan

## 1) Objective

Deliver a professional, high-clarity visual polish of the Chirality UI while preserving:

- Existing color palette tokens in `frontend/app/globals.css`
- Existing Portal hexagon row/column color semantics
- Existing Portal hexagon labels/content taxonomy

The goal is a cleaner, more intentional interface with stronger hierarchy, better readability, better interaction states, and production-level consistency across all views (`home`, `workbench`, `pipeline`, `direct`).

## 2) Non-Negotiable Constraints

1. Keep current palette values and semantic meaning.
2. Keep current Portal hexagon coloring and label text unchanged.
3. Preserve current harness/SSE behaviors and data flow contracts.
4. Maintain existing information architecture (Portal -> Workbench/Pipeline/Direct paths).
5. Keep desktop and mobile behavior functional throughout.

## 3) Current-State Audit Summary

Observed issues to address:

- Visual density is high; too many simultaneous effects (glows, borders, heavy uppercase labeling).
- Inconsistent spacing scale and radius usage across components.
- Typography hierarchy is present but not systematic.
- Panel chrome and metadata styling vary by view/component.
- Interaction states (hover/focus/disabled/loading) are inconsistent.
- Some components use noisy or placeholder-like visual language that weakens professional finish.

## 3.1) Delta From Latest Cosmetic Pass (2026-02-08)

Recent UI updates already established a stronger baseline:

- Light mode surface/background treatment was refreshed in `frontend/app/globals.css`.
- Root directory selection was centralized into `frontend/components/ResizableLayout.tsx`.
- `frontend/components/ChatPanel.tsx` moved to compact status-text loading feedback.
- `frontend/app/page.tsx` now initializes `projectRoot` client-side to avoid hydration drift.

Planning implication:

- Focus polish work on consistency and hardening of this direction, not visual reset.

## 3.2) Incremental UI Updates Since Baseline (2026-02-21)

Recent refinements after the original polish pass:

- Chat bubbles now use role-structured presentation with calmer, low-contrast surfaces:
  - assistant bubbles left-aligned and near-neutral with subtle role tint
  - user bubbles right-aligned with stronger but still restrained role tint
- Assistant responses in chat now render GitHub-flavored markdown for readability (lists, code blocks, tables, blockquotes), with ANSI fallback retained for terminal-style tool output.
- Header status noise was reduced by removing static fallback copy (`SYSTEM_RECOVERY: SUCCESS`); update messaging now appears only when an update is actually available.

Planning implication:

- Future polish changes should preserve this lower-noise chat hierarchy and markdown readability baseline.

## 4) Design Direction

Use the current aesthetic (glass + command-center) but reduce noise and increase precision:

- Fewer competing accents, clearer content hierarchy.
- Strong but restrained typography.
- Uniform panel system with predictable spacing and state behavior.
- Motion only where it communicates state/intent.

## 5) Workstreams

## A. Foundation System (Tokens + Rules)

Scope:

- Standardize design primitives in `frontend/app/globals.css`:
  - spacing scale
  - radius scale
  - border/opacity scale
  - shadow/elevation levels
  - typography roles (`display`, `title`, `body`, `meta`, `mono-meta`)
- Keep current color tokens; add semantic aliases only (no palette value change).

Deliverables:

- New token section and usage guide comments in `globals.css`
- Removal of ad-hoc repeated values where practical

Acceptance:

- No new hard-coded one-off spacing/radius/shadow values in touched components.

## B. Global Shell Polish (Page Frame + Header + Navigation)

Scope:

- Refine top control bar + header in `frontend/app/page.tsx`.
- Tighten layout rhythm:
  - consistent vertical spacing
  - uniform control sizing
  - less visual crowding in top chrome
- Improve selector visual clarity in Workbench/Pipeline header contexts.
- Keep browser-storage initialization SSR-safe (no server/client text mismatch).

Deliverables:

- Header/control styling pass with unified control classes.

Acceptance:

- Header feels calmer and more legible without changing navigation behavior.

## C. Portal Surface (Home View)

Scope:

- Preserve HexGrid labels/colors exactly.
- Improve supporting surfaces:
  - `frontend/components/DashboardList.tsx`
  - spacing, card rhythm, status readability, empty/loading states
- Keep hex visual identity but reduce incidental glare/competing effects around it.

Deliverables:

- Portal side panel polish and consistent card treatment.

Acceptance:

- Hex grid visual semantics unchanged.
- Dashboard appears production-grade and less “prototype-like.”

## D. Workbench/Direct/Pipeline Layout System

Scope:

- Normalize panel chrome and structure in:
  - `frontend/components/ResizableLayout.tsx`
  - `frontend/components/WorkbenchView.tsx`
  - `frontend/components/PipelineView.tsx`
  - `frontend/components/DirectLinkView.tsx`
- Unify sidebar headers, footer actions, pane paddings, and divider treatments.
- Keep project-root selection as a shared footer-level control (single source of interaction).

Deliverables:

- A shared pane style language applied across all three modes.

Acceptance:

- Switching modes feels like one coherent product, not separate pages.

## E. Chat Experience Polish

Scope:

- Refine message presentation and session metadata in `frontend/components/ChatPanel.tsx`:
  - clearer assistant/user grouping
  - improved metadata hierarchy (session/model/cwd/cost)
  - status-text-first tool event presentation (non-verbose by default)
  - stable, clear in-flight/interrupt affordances
- Preserve SSE event interpretation contract.

Deliverables:

- Updated message/event visuals and interaction states.

Acceptance:

- Chat is easier to scan under long conversations/tool-heavy runs.

## F. File Surfaces + Utility Components

Scope:

- Polish consistency for:
  - `frontend/components/FileTree.tsx`
  - `frontend/components/FilePreview.tsx`
  - `frontend/components/SystemFileTree.tsx`
  - `frontend/components/DirectoryPicker.tsx`
  - `frontend/components/SettingsModal.tsx`
- Standardize empty/loading/error visual patterns.

Deliverables:

- Unified utility surface styling and state components.

Acceptance:

- Secondary tooling panels match the same visual quality as chat/portal.

## G. Accessibility and Interaction Quality

Scope:

- Ensure keyboard focus visibility on all actionable controls.
- Improve contrast where needed to meet AA intent.
- Ensure predictable hover/focus/disabled states.
- Respect reduced motion preference in non-essential animations.

Deliverables:

- Focus ring standard and control state coverage.

Acceptance:

- Keyboard-only pass is usable and obvious.

## H. QA + Hardening

Scope:

- Cross-view responsive pass (desktop + common tablet/mobile widths).
- Visual regression sanity checks (manual snapshots or checklist-driven verification).
- Confirm no behavioral regressions in harness flows.

Deliverables:

- Short verification checklist and signoff notes.

Acceptance:

- No functional regression in runtime workflows.

## 6) Execution Phases (Recommended)

## Phase 0: Baseline and Freeze

- Capture screenshots of current `home/workbench/pipeline/direct`.
- Define “do-not-change” assets (palette + hex colors/labels).
- Create utility class strategy for reusable controls/panels.

## Phase 1: Foundation Layer

- Implement token/rule normalization in `globals.css`.
- Introduce consistent control and panel primitives.

## Phase 2: Structural Surfaces

- Apply shell + layout system updates (`page.tsx`, `ResizableLayout`, view wrappers).
- Keep root-directory selection unified in `ResizableLayout` while polishing affordances.
- Polish Dashboard and file surfaces.

## Phase 3: Chat and High-Usage UX

- Refine `ChatPanel` messaging and status surfaces.
- Tighten tool event readability and streaming affordances.

## Phase 4: Accessibility + Responsive + QA

- Focus/keyboard/contrast pass.
- Responsive refinements and final visual tune.

## 7) Component-by-Component Task Matrix

| Component/File | Primary Changes | Priority |
| --- | --- | --- |
| `frontend/app/globals.css` | token normalization, spacing/radius/shadow/typography scales, utility cleanup | P0 |
| `frontend/app/page.tsx` | top chrome hierarchy, control consistency, spacing rhythm, SSR-safe browser-storage init patterns | P1 |
| `frontend/components/HexGrid.tsx` | minimal touch; preserve semantics, only micro-polish wrappers if needed | P2 |
| `frontend/components/DashboardList.tsx` | card hierarchy, project-root selector polish, loading/empty states | P1 |
| `frontend/components/ResizableLayout.tsx` | pane chrome consistency, shared project-root selector polish, footer action cleanup, responsive behavior | P1 |
| `frontend/components/ChatPanel.tsx` | message hierarchy, status-text event readability, composer and in-flight states | P1 |
| `frontend/components/WorkbenchView.tsx` | sidebar/header polish consistency | P2 |
| `frontend/components/PipelineView.tsx` | sidebar/header polish consistency | P2 |
| `frontend/components/DirectLinkView.tsx` | sidebar/header polish consistency | P2 |
| `frontend/components/FileTree.tsx` | tree readability and row interaction states | P2 |
| `frontend/components/FilePreview.tsx` | content header/readability/loading state polish | P2 |
| `frontend/components/SystemFileTree.tsx` | compact utility-panel visual consistency | P3 |
| `frontend/components/DirectoryPicker.tsx` | modal hierarchy and action affordances | P3 |
| `frontend/components/SettingsModal.tsx` | settings form clarity and control consistency | P2 |

## 8) Acceptance Criteria

Functional:

- No change to harness API contracts and chat behavior semantics.
- No regression in session creation, turn streaming, interrupt, resume.
- No hydration mismatch warnings from browser-storage-backed UI state.

Visual:

- Consistent spacing/typography across all primary surfaces.
- Reduced visual noise while preserving brand identity.
- Portal hexagon colors/labels remain unchanged.

Interaction:

- All interactive controls have complete state coverage.
- Loading/empty/error states are visually intentional.

Accessibility:

- Focus-visible treatment exists for all actionable controls.
- Contrast remains legible in dark and light modes.

## 9) Delivery Strategy

- Implement as small PR slices aligned to phases.
- Keep each slice behavior-safe (style-first, minimal logic coupling).
- Validate each slice with:
  - `npm run lint`
  - `npx tsc --noEmit`
  - quick manual smoke across `home/workbench/pipeline/direct`

## 10) Suggested Slice Order

1. `globals.css` foundation + reusable classes (preserve current gradient/frosted baseline)
2. `page.tsx` shell + `ResizableLayout.tsx` shared root-selector consistency
3. `DashboardList.tsx` + primary utility surfaces
4. `ChatPanel.tsx` status language and readability polish
5. file/system/utility components
6. accessibility + responsive cleanup + hydration sanity checks

## 11) Out of Scope (for this polish plan)

- Major IA/navigation restructuring.
- New feature additions unrelated to UI quality.
- Color palette redesign.
- Changing Portal hex taxonomy content.
