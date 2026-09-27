# Source inventory

Standing: **source identification (agent).** What the v4 conceptual
undertaking examined, where it is, and what each source can and cannot
support. Paths are at the investigation revision `2b0572fe0` unless marked
`ORIG/` (Git-ignored archives, see [`archives/ARCHIVES.md`](archives/ARCHIVES.md))
or given as a GitHub reference. "Examined by" names the preserved TASK return
([`tasks/`](../execution/_Coordination/AgentRuns/V4-CONCEPT-20260925/tasks/))
or HELPS_HUMANS directly (HH). Pinned revisions are in
[`REFERENCES.md`](REFERENCES.md).

## How to weigh a source

| Kind | Can support | Cannot support |
|---|---|---|
| The owner's recorded words (verbatim or hash-bound transcription) | What the owner intended, preferred or decided at that time and in that scope | That the intention worked; a scope wider than the words |
| Accepted requirement or ruling in a project | What that project committed to, on its revision | A v4 requirement (OD-10), or that it was built |
| Described design, plan, review or survey | The reasoning and the options considered | That the design exists or works |
| Code | That a mechanism exists on that revision | That it runs, is reachable, or is used |
| Test definition | What someone intended to check | That the check passed on a given revision |
| Executed check with a record | That the check passed or failed on the recorded candidate and conditions | Behaviour on other revisions, hosts, or with real users |
| Agent-drafted conceptual text (thesis, manuals) | The argument and its sources; practices worth trying | That a practice is effective (no empirical study exists) |
| Agent returns in this run | Where to look; a reading of the sources | Anything on their own: rely on the cited source |

## 1. The owner's direction

| Source | What it is | Examined by |
|---|---|---|
| Opening brief, 2026-09-25 ([`OPENING_BRIEF.md`](../execution/_Coordination/AgentRuns/V4-CONCEPT-20260925/OPENING_BRIEF.md)) | The v4 assignment and directions OD-01…OD-13 | HH |
| `plans/evidence/2026-08-01_accountability_thesis.md` §1 | Owner theses: bedrock claim, build/run governance asymmetry, alignment by presence, release stance, background | HH, T1 |
| `plans/evidence/2026-09-19_owner_words_four_graph_structures.md` | Owner's four-structure claim and attention measure, hash-bound | T1 |
| `plans/steers/chirality_app_v3_codex_host_replatform_direction_2026-09-11.md` | Owner's v3 replatform direction, including the embedding intent (2026-09-12) | HH, T3 |
| `projects/chirality-app-dev/execution/_Coordination/AgentRuns/APP_V3_CODEX_HOST_REPLATFORM_20260912/PERSPECTIVE.md` | Owner's note on v3's purpose and simplification | HH, T3, T5 |
| `projects/chirality-app-dev/execution/_Coordination/_DECISIONS/D-APP-87_RULING_…_2026-08-02.md` | Owner ruling: two delivery targets; domain applications as the primary delivery vehicle | HH, T3, T4 |
| `projects/chirality-piping/execution/_Coordination/AgentRuns/HELP-HUMAN-PIPING-20260916-UI-DESIGN-PROGRAM/instances/ROOT/DIRECTION_DECISION_2026-09-17.md` | Owner's SWBPIPE collaboration direction, hash-bound | HH, T6 |
| `projects/chirality-piping/execution/_Coordination/AgentRuns/HELP-HUMAN-PIPING-20260918-UI-IMPLEMENTATION/instances/ROOT/CONTINUATION_2026-09-19_CODEX/OWNER_*.md` | Owner steers for the SWBPIPE agent path (controller first, CLI first, computer use for the external prover, local models reported by a peer) | HH (two files), T6 |
| `projects/pec/execution/_Coordination/_DECISIONS/D-PEC-57_coordination_plane_pivot.md`, `D-PEC-90_RULING_2026-09-25.md` | PEC's redirection toward coordinating an agent fleet; agents may query PEC by tool calls later | HH, T5 |

## 2. Foundation and practice

| Source | Standing | Examined by |
|---|---|---|
| `docs/thesis/` (19 files) — carried forward to [`../foundation/thesis/`](../foundation/thesis/) | Agent-drafted under owner direction; CITED/REVIEWED, not AUTHENTICATED; nonbinding | HH (README), T1 (all) |
| `docs/alignment-manual/Project_Management_for_Human_Agent_Teams_Consolidated_v7.md` | Owner-directed, largely externally drafted; owner-signed authorship section; "does not establish that every practice … has been proved effective" | T2 |
| `docs/alignment-manual/Project_Management_for_Human_Agent_Teams_Field_Book_v1.md` | Agent abridgement for a human reader | HH, T2 |
| `docs/alignment-manual/CHIRALITY_AGENT_USER_MANUAL_v3.md` | Agent-facing repository manual; not an App end-user guide | T2 |
| `plans/evidence/2026-09-2{2,3}_*`, `2026-09-19_manual_theory/` | How the manuals were produced | T2 |

## 3. Root governance (applies to v4 — OD-10)

| Source | Relevance | Examined by |
|---|---|---|
| Root `AGENTS.md` | Roles, skills and workflows, briefs, delegation, merge authority; also App-specific clauses (Codex sole engine for the App MVP; stock Codex App Server, D-GOV-43) | HH, T5 |
| `docs/PRD_ROOT.md` | Root as control plane; project roots own products; merge policy §5.3.1; run evidence E-1 | T5 |
| `docs/AGENT_WORKFLOW_RUNTIME.md`, `docs/WORKFLOW_COMPONENT_STANDARD.md` | Operational meaning of role, workflow, skill, tool, brief; self-described as prospective | T5 |
| `docs/DIRECTIVE.md`, `CONTRACT.md`, `SPEC.md`, `TYPES.md` | Root invariants (human-only binding approval, content-bound approval, file-native authority, domain engines own truth) | T5 (partial), T1 via thesis |
| `docs/governance_harness/_DECISIONS/` (D-GOV-01, -12, -20, -35, -42, -43) | Rulings on projections, orchestration, shared runtime, delegation classes, four roles, stock Codex host | T3, T4, T5 |
| `workflows/reverse-engineer-software/` | The workflow selected for this undertaking | HH |

## 4. Chirality App v3 (the fallback line)

| Source | What it can support | Examined by |
|---|---|---|
| Release notes v3.0.0, v3.0.1 (`sgttomas/chirality-app`) | What was shipped and claimed | T3, T4 |
| `projects/chirality-app-dev/README.md`, `instructions/AGENTS.md` | Current product description; shipped guidance | T3 |
| `projects/chirality-app-dev/docs/` (PRD, SPEC, TYPES, CONTRACT, DIRECTIVE) | The older governed harness design with a Codex-only overlay; many claims stale (1,044 of 3,217 in the 2026-09-21 concordance) | T3 |
| `projects/chirality-app-dev/frontend/` (Electron, Next.js; ~52.6k source lines, 222 test files) | What exists in v3 code | T3 |
| `execution/_Coordination/AgentRuns/APP_V3_*` (replatform, trial completion, user journeys, UI refinement, day-1 maintenance) | Executed checks S-1…S-8, journey results, trial findings, owner refinements | T3 |
| `execution/_Reconciliation/DeliverableConcordance/RUN_D128_…` | Post-release claim-versus-implementation census and v3 "done" candidate | T3 |
| GitHub issues on both repositories | None filed; no external user feedback on record | T3 |
| Installed `/Applications/Chirality.app` | **v3.0.0** (not the 3.0.1 fallback) | HH |

## 5. Earlier App generations

| Source | Generation | Examined by |
|---|---|---|
| Release notes v1.0.1 – v2.0.0 | v1.x (Feb 2026), v2.0 (Jul 2026) | T4 |
| `ORIG/.archive/frontend/`, `ORIG/.archive/*.md` (PRD_CANDIDATE, WHAT-IS-AN-AGENT) | v1 desktop app and founding definitions | T4 |
| `ORIG/projects/chirality-app-dev/.archive/` | First governed App decomposition (2026-02-21) and its execution, including a development-history analysis | T4 |
| `ORIG/projects/chirality-app-dev/execution/_Decomposition/.archive/` | vNext decompositions (May 2026) | T4 |
| `ORIG/plans/.archive/` | Task-management harness evaluation and handoff; chirality-app-test plans | T4 |
| `plans/*.html` (2026-07-25 … 2026-08-22) | Program architecture review, tandem comparison, maturity survey, five investigations, v3 release plans; non-governing | T3, T4, T5 |

## 6. Chirality Runtime

| Source | What it can support | Examined by |
|---|---|---|
| `projects/chirality-runtime/README.md`, `docs/APPLICATION_TOOLS.md`, `docs/APPLICATION_CONSUMER_GUIDE.md`, `docs/CODEX_MVP_INTEGRATION.md` | The host-owned service, application-owned tools, and how a second application would consume them | HH (tools section), T5, T6 |
| `projects/chirality-runtime/packages/` | Implementation; `engine-claude` and `engine-pi-omlx` present but not wired into the service | T5 |
| `execution/_Coordination/AgentRuns/APPLICATION_DYNAMIC_TOOLS_20260920/` | Owner direction and records for application tools; controlled tests only | T5, T6 |

## 7. SWBPIPE (`projects/chirality-piping`)

| Source | What it can support | Examined by |
|---|---|---|
| `docs/PRD.md`, `INTENT.md`, `PROFESSIONAL_BOUNDARY.md`, `IP_AND_DATA_BOUNDARY.md`, `claims_registry.md` | Product purpose, personas (including an "agent-enhanced user"), professional and data boundaries | T6 |
| `schemas/`, `core/`, `apps/desktop/` | Objects, operations, results, diagnostics and recovery that a human and agent would share; exposure through headless runner, Tauri commands, or GUI only | T6 |
| Branch `origin/codex/piping-live-control-20260924` (unmerged; not an ancestor of the investigation revision) | The live-control seam: inspect, preview, submit, status; basis binding; no external Apply | T6 |
| UI design and implementation run records (2026-09-16 …) | Owner's collaboration direction and implementation steers | HH, T6 |
| `ORIG/projects/chirality-piping/.archive/` (TP-MAC-02/03, TP-PER-01) | Result interpretation and review workflow plans; persistence and run history | T6 |
| `_DomainEngines/` | Domain-engine profile for SWBPIPE (manual bridge; proposal level as destination) | T5, T6 |

## 8. PEC

| Source | What it can support | Examined by |
|---|---|---|
| `projects/pec/README.md`, `docs/PRD.md` (v2.2), `docs/STATUS.md` | Coordination-plane purpose and principles; early implementation | T5 |
| `plans/chirality-task-management/`, `plans/chirality_task_management_architecture_review_2026-07-31.html` | Evidence on how concerns and notices close (or do not) at agent scale | T5 |

## 9. Outside the repository

| Source | What it can support | Examined by |
|---|---|---|
| Supplier documentation, release notes and third-party reports for agent harnesses (Codex App Server and SDK, Claude Agent SDK, Copilot SDK, OpenAI Agents SDK, ADK and Gemini CLI, Pi, goose, OpenHands, OpenCode, frameworks), embedding protocols (MCP 2026-07-28, MCP Apps, ACP, AG-UI, A2A) and computer use; 80+ sources listed in T7 with retrieval dates | Current capabilities, interfaces, terms and limits as published — each to be tested locally before any fitness claim; credential terms need vendor confirmation | T7 |

## 10. Not examined in this pass

Held for Stage E if a question needs them: the full App PRD body and ruling
records A1–A15 / R1–R18; individual control-loop pass files; the contents of
the two archived zip files; the SWBPIPE UX specification and external-prover
format research; PEC's feed-model design note; `ORIG/.archive/domains/` and
`ORIG/domains/` corpora; the app's local session records
(`ORIG/projects/chirality-app-dev/frontend/.chirality/sessions`), which may
contain private content and would be read only for a specific question.
