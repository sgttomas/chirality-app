# PRD - Chirality Desktop Harness

**Status:** Draft  
**Date:** 2026-05-03  
**Product:** Chirality desktop harness and bundled agent operating system  
**Primary repository:** `chirality-app-dev`  
**Primary audience:** product owner, engineering, agent-instruction maintainers, reviewers, and release operators

---

## 1. Source Basis

This PRD is derived from repository-local sources only. Primary inputs:

- `README.md`
- `AGENTS.md`
- `INIT.md`
- `docs/DIRECTIVE.md`
- `docs/SPEC.md`
- `docs/TYPES.md`
- `docs/CONTRACT.md`
- `docs/PLAN.md`
- `docs/DBM_Agent_Instruction_Architecture.md`
- `docs/SE_Design_Analysis.md`
- `docs/harness/*`
- `docs/ui/UI_POLISH_EXECUTION_PLAN.md`
- `execution/_Decomposition/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md`
- `frontend/`
- `tools/REGISTRY.md`
- `PROFESSIONAL_ENGINEERING.md`

Where documents and implementation disagree, this PRD states the product requirement and records the implementation note under "Known Gaps and Risks."

---

## 2. Product Summary

Chirality is a desktop harness for running governed AI agents against a user-selected local filesystem workspace. It packages a release-managed instruction root (`AGENTS.md`, `agents/`, `docs/`, and framework files) inside the desktop app while keeping all project execution state in a user-selected working root (`projectRoot`).

The product exists to accelerate deliverable-heavy professional work while preserving human authority, provenance, auditability, and filesystem-native state. Agents decompose scope, scaffold package/deliverable folders, draft document kits, extract dependencies, run semantic analysis, reconcile across deliverables, support estimates/schedules, and manage change. Outputs remain drafts or decision support until accepted by an accountable human.

Core product thesis:

> Project truth lives in git-tracked plain files. If a decision is not in a versioned file, it does not exist for purposes of reliance.

---

## 3. Goals

### 3.1 Product Goals

1. Provide a local desktop application that runs agent workflows against a selected working root without requiring an external database.
2. Preserve strict separation between bundled instruction root and mutable working root.
3. Make agent work auditable through plain files, git diffs, lifecycle files, dependency registers, and immutable snapshots.
4. Provide matrix-based navigation into two execution surfaces: WORKBENCH for interactive persona agents and PIPELINE for operative task categories.
5. Support streaming chat turns with session persistence, runtime options, interrupts, multimodal attachments, and Anthropic provider integration.
6. Enforce safety and governance boundaries: human authority at gates, no automated issuance, no hidden project memory, fail-closed subagent delegation, and Anthropic-only outbound network policy.
7. Provide deterministic tools and validation workflows for scaffolding, schema checks, dependency closure, harness runtime validation, and release packaging.
8. Ship a macOS 15+ Apple Silicon unsigned DMG build path with instruction-root integrity verification.

### 3.2 Non-Goals

The product must not:

- Replace professional judgment or produce binding approval records autonomously.
- Sign, seal, certify, approve, issue, transmit, or otherwise release professional work for reliance.
- Make safety-critical decisions without human review.
- Conduct financial transactions or binding commitments.
- Depend on an external project database.
- Persist project truth in hidden app state, chats, caches, or vendor systems.
- Allow outbound network access beyond the Anthropic API path required for provider execution.
- Treat local UI preferences, API keys, or chat drafts as authoritative project state.

---

## 4. Users and Personas

### 4.1 Professional Operator

The primary user is a licensed professional, project lead, or accountable reviewer who needs AI-assisted production while retaining decision rights. They select the working root, approve gates, review evidence, and decide what can be relied upon.

### 4.2 Project Orchestrator

A user who converts a scope of work into packages, deliverables, lifecycle records, document kits, dependency registers, and coordination artifacts. They use ORCHESTRATOR, WORKING_ITEMS, RECONCILIATION, CHANGE, and PIPELINE lanes.

### 4.3 Specialist Contributor

A user or workflow that executes bounded deliverable-local work through TASK, DEPENDENCIES, CHIRALITY_FRAMEWORK, CHIRALITY_LENS, ESTIMATING, or audit agents.

### 4.4 Governance Maintainer

A maintainer responsible for agent instruction conformance, invariant consistency, deterministic tooling, and release-managed instruction root changes.

### 4.5 Release Operator

A maintainer who builds, validates, packages, and distributes local unsigned desktop builds.

---

## 5. Product Principles

1. **Filesystem is the database.** Project state is represented as human-readable files under the working root.
2. **Git is the event store.** Review, audit, rollback, and approvals bind to git-tracked content.
3. **Human authority at every gate.** Agents propose; humans approve, issue, sign, seal, and decide.
4. **Evidence over plausibility.** Claims require provenance. Unknowns become `TBD`, not guesses.
5. **No hidden memory for project truth.** Runtime convenience state is allowed only when it is explicitly non-authoritative.
6. **Instruction root and working root are separate.** Release-managed agent OS files must not be modified by project execution.
7. **Write quarantine.** Each agent has an explicit write scope. Derived outputs live in tool roots; source truth lives in deliverable folders.
8. **Immutable snapshots.** Snapshot-producing runs create timestamped folders that are not overwritten. `_LATEST.md` pointers may move.
9. **Least structure that works.** Rigor scales with stakes; structure is added when it reduces error, rework, or ambiguity.

---

## 6. Scope

### 6.1 In Scope

- Desktop shell built with Next.js and Electron.
- Working-root selection, validation, file tree browsing, and deliverable scanning.
- Matrix navigation across PORTAL, WORKBENCH, and PIPELINE.
- Session lifecycle APIs and turn execution via SSE.
- Anthropic SDK provider path with local UI key storage and environment fallback.
- Stub provider mode for deterministic local tests.
- Server-side attachment resolution for supported file types.
- Operator Toolkit for per-turn runtime options and local presets.
- Execution-root scaffolding from decomposition markdown.
- Deliverable status and dependency contract APIs.
- Lifecycle transition enforcement for `_STATUS.md`.
- Dependency register read/write support for `Dependencies.csv` v3.1.
- Subagent governance evaluation and fail-closed delegation behavior.
- Deterministic tool registry for scaffolding, validation, reporting, coordination, PDF-to-markdown, and evaluation.
- Harness validation scripts and CI premerge workflow.
- Instruction-root integrity verification in packaged builds.
- macOS Apple Silicon unsigned DMG packaging workflow.

### 6.2 Current Release Target

The current release target is:

- macOS 15+
- Apple Silicon (`arm64`)
- Unsigned, unnotarized local-builder DMG
- Node.js `>=20` for development/build

README references Windows packaging, but the current build config and runbook define macOS arm64 as the concrete release target.

### 6.3 Out of Scope for Current Release

- Automated staleness propagation and dirty-state SHA comparison.
- Deliverable-level lock mechanism.
- Unified pipeline run record persistence across all task agents.
- Project-level dependency graph visualization output.
- Automated merge gates beyond documented/human CHANGE constraints.
- Windows release packaging unless separately scoped.
- Runtime enforcement monitor that intercepts every agent file write.

---

## 7. User Journeys

### 7.1 Select and Validate a Working Root

1. User opens Chirality.
2. User enters an absolute path or chooses a folder via native Electron directory picker.
3. App validates that the path exists, is a directory, is readable/writable, and is not inside the instruction root.
4. App stores the selected root as local UI state and uses it for file tree, scan, chat session, scaffold, and contract APIs.

Acceptance:

- Relative paths are rejected.
- Missing or inaccessible directories show actionable errors.
- Instruction-root conflicts are blocked.
- Clearing the root disables runtime actions that require `projectRoot`.

### 7.2 Navigate the Agent Matrix

1. User enters PORTAL.
2. User selects a NORMATIVE or EVALUATIVE cell and routes to WORKBENCH with agent context.
3. User selects an OPERATIVE cell and routes to PIPELINE with category context.
4. If deliverables are present, user can click a deliverable row to route to PIPELINE `TASK*` with that deliverable preselected.

Acceptance:

- NORMATIVE and EVALUATIVE route to WORKBENCH.
- OPERATIVE routes to PIPELINE.
- Disabled or unsupported variants remain visible as coming soon rather than silently disappearing.

### 7.3 Scaffold an Execution Root

1. User selects a working root.
2. User opens PIPELINE.
3. User enters a decomposition markdown path and coordination mode.
4. App calls `POST /api/harness/scaffold`.
5. Runtime parses package/deliverable tables, creates tool roots, copies decomposition, writes `INIT.md`, writes `_Coordination/_COORDINATION.md`, creates packages and deliverable folders, and returns validation summaries.

Acceptance:

- Scaffolding is idempotent for existing directories/files.
- Failures are fail-fast and include stage, target path, and created paths for recovery.
- PREPARATION compatibility is reported before the user proceeds.

### 7.4 Run a Workbench Persona Session

1. User routes to WORKBENCH with an agent persona.
2. Chat panel resolves persona aliases to instruction-file names.
3. User sends a prompt with optional runtime options and attachments.
4. App creates/boots a harness session if needed.
5. Runtime streams turn events to the UI.
6. User may interrupt the turn.

Acceptance:

- Session identity is preserved across turns for the same root/persona/mode.
- Runtime errors preserve the draft and attachments for retry.
- Interrupt returns a terminal `process:exit` event and updates UI state.

### 7.5 Run an Operative Pipeline Intent

1. User opens PIPELINE.
2. User selects one of `DECOMP`, `PREP`, `TASK`, or `AUDIT`.
3. User selects a category-specific agent or lane.
4. For `TASK`, user selects scope mode and dynamic scope from the working root.
5. User inspects deliverable status/dependency contract snapshots and may apply allowed lifecycle transitions.

Acceptance:

- Deliverable selections reset when the project root or scan results become stale.
- `KNOWLEDGE_TYPES` mode is shown only when a knowledge decomposition marker is detected.
- Lifecycle transitions enforce authorized actors and approval SHA requirements for human gate states.

### 7.6 Attach Files to a Turn

1. User opens file picker from Chat Panel.
2. User selects supported files by absolute path.
3. UI previews attachments as non-authoritative client metadata.
4. Server validates, classifies, and reads attachments.
5. Turn proceeds if user text exists or at least one valid attachment resolves.

Acceptance:

- Allowed extensions: `.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`, `.pdf`, `.txt`, `.md`, `.csv`.
- Symlinks, directories, special files, unsupported extensions, unreadable files, files over 10 MB, and total raw bytes over 18 MB are rejected.
- Partial attachment failure is non-fatal when executable content remains.
- If all attachments fail and text is empty, request fails with `ATTACHMENT_FAILURE`.

### 7.7 Store and Use an Anthropic API Key

1. User opens API key settings.
2. User stores a key through Electron IPC.
3. Electron encrypts key material with `safeStorage` outside the working root.
4. Server runtime reads UI key from process global; if absent, uses `ANTHROPIC_API_KEY` or `CHIRALITY_ANTHROPIC_API_KEY`.

Acceptance:

- Key material is never written to working-root files.
- UI key takes precedence over env keys.
- API key status can report source as `ui`, `env`, or `none`.
- If secure storage is unavailable, UI reports an error.

### 7.8 Validate and Package a Release

1. Release operator installs dependencies in `frontend/`.
2. Operator runs tests/typecheck/harness validation.
3. Operator runs desktop distribution build.
4. Build packages app resources and verifies instruction-root integrity.

Acceptance:

- `frontend/dist/Chirality-0.1.0-arm64.dmg` is produced for macOS arm64.
- App bundle includes `agents/` and `docs/`.
- App minimum macOS target is `15.0.0` or later.
- Build is unsigned/adhoc by design.

---

## 8. Functional Requirements

Priority:

- `P0`: required for current release usefulness and safety.
- `P1`: important for current release quality or governed operation.
- `P2`: desirable or future hardening.

### 8.1 Desktop Shell and Navigation

| ID | Priority | Requirement | Acceptance |
|---|---:|---|---|
| FR-001 | P0 | The app shall provide a desktop shell with PORTAL, PIPELINE, and WORKBENCH navigation. | Header nav routes to `/`, `/pipeline`, and `/workbench`; active route is visually indicated. |
| FR-002 | P0 | The app shall expose working-root selection globally. | User can type a path, choose folder in Electron, apply, and clear root. |
| FR-003 | P0 | The app shall validate working roots before use. | Non-absolute, missing, inaccessible, non-directory, or instruction-root-contained paths fail with typed errors. |
| FR-004 | P0 | The app shall show a file tree for the selected working root. | Tree API skips `.git`, `.next`, `node_modules`, `dist`, `dist-electron`, and `out`; depth is bounded; inaccessible directories mark truncation. |
| FR-005 | P1 | The shell shall support resizable/collapsible File Tree, Toolkit, and Chat panes. | Drag and keyboard resize work; Home collapses; End expands; widths are persisted locally. |
| FR-006 | P1 | The UI shall preserve a calm, professional, dense-but-readable interface. | UI polish acceptance from `docs/ui/UI_POLISH_EXECUTION_PLAN.md` remains applicable; no regression in harness behavior. |

### 8.2 Matrix, Workbench, and Pipeline

| ID | Priority | Requirement | Acceptance |
|---|---:|---|---|
| FR-007 | P0 | PORTAL shall render the 3x4 agent matrix using canonical rows and columns. | Rows: `NORMATIVE`, `OPERATIVE`, `EVALUATIVE`; columns: `GUIDING`, `APPLYING`, `JUDGING`, `REVIEWING`. |
| FR-008 | P0 | Matrix routing shall follow the docs/SPEC contract. | NORMATIVE/EVALUATIVE cells open WORKBENCH; OPERATIVE cells open PIPELINE categories. |
| FR-009 | P0 | WORKBENCH shall present active agent context. | Selected agent, row, and column are shown from query params with sensible defaults. |
| FR-010 | P1 | WORKBENCH shall consume deliverable contract APIs for read-only checks and permitted lifecycle transitions. | Status/dependency summaries load for selected deliverables; transition controls are disabled for unsupported agents. |
| FR-011 | P0 | PIPELINE shall expose `DECOMP`, `PREP`, `TASK`, and `AUDIT` category controls. | Each category has documented options; unsupported options are visible and disabled as coming soon. |
| FR-012 | P0 | PIPELINE `TASK` shall use split selectors for task agent and scope. | Scope mode is `DELIVERABLES` or `KNOWLEDGE_TYPES`; target deliverable is required for knowledge-type mode. |
| FR-013 | P1 | Dynamic scope scan shall reset invalid selections. | Root changes, removed deliverables, disabled knowledge markers, and stale knowledge targets clear invalid selection state. |

### 8.3 Harness Sessions and Turns

| ID | Priority | Requirement | Acceptance |
|---|---:|---|---|
| FR-014 | P0 | The app shall create, list, resume, save, and delete harness sessions. | Session records are JSON files under `.chirality/sessions` or `CHIRALITY_SESSION_ROOT`; sessions are filtered by normalized project root. |
| FR-015 | P0 | Session creation shall bind `projectRoot`, `persona`, and `mode`. | Missing persona/mode use defaults; invalid project root is rejected. |
| FR-016 | P0 | Session boot shall accept runtime options. | `POST /api/harness/session/boot` accepts `opts` and records boot metadata. |
| FR-017 | P0 | Turn execution shall stream Server-Sent Events. | `POST /api/harness/turn` returns `text/event-stream`; events include `session:init`, `chat:delta`, `chat:complete`, `session:complete`, `tool:result`, `turn:error`, and `process:exit`. |
| FR-018 | P0 | Only one active turn may run per session. | Concurrent turn attempts return `TURN_IN_PROGRESS`. |
| FR-019 | P0 | Users shall be able to interrupt active turns. | `POST /api/harness/interrupt` aborts the active provider request and yields interrupted `process:exit`. |
| FR-020 | P1 | Runtime errors shall be typed and actionable in UI. | UI maps harness errors to title/message/next-step text and preserves drafts for retry. |

### 8.4 Runtime Options and Personas

| ID | Priority | Requirement | Acceptance |
|---|---:|---|---|
| FR-021 | P0 | Runtime option fallback chains shall be deterministic. | Model: `opts.model` -> `CHIRALITY_GLOBAL_MODEL` or AGENTS frontmatter -> default; tools: `opts.tools` -> persona frontmatter -> default; max turns: `opts.maxTurns` -> persona frontmatter -> default. |
| FR-022 | P0 | Unknown option keys shall be ignored with warnings. | Unknown fields do not break turns or silently mutate behavior. |
| FR-023 | P0 | Persona names shall resolve to `agents/AGENT_*.md`. | Missing personas return `PERSONA_NOT_FOUND`. |
| FR-024 | P0 | Persona aliases shall map UI labels to canonical agents. | `HELP -> HELP_HUMAN`, `ORCHESTRATE -> ORCHESTRATOR`, `AGGREGATE -> AGGREGATION`, `RECONCILING -> RECONCILIATION`, `AGENTS -> HELPS_HUMANS`. |
| FR-025 | P0 | Production provider mode shall support Anthropic SDK. | `CHIRALITY_HARNESS_PROVIDER=anthropic` uses the Anthropic SDK path; default/stub mode remains testable. |
| FR-026 | P1 | The runtime shall compose real agent instruction context into turns. | Provider requests include the selected agent instruction/root context and working-root constraints. See Known Gap KG-001. |

### 8.5 Anthropic Provider and Network Policy

| ID | Priority | Requirement | Acceptance |
|---|---:|---|---|
| FR-027 | P0 | Anthropic API key resolution shall follow `ENV+UI`. | UI safeStorage key first; then `ANTHROPIC_API_KEY`; then `CHIRALITY_ANTHROPIC_API_KEY`. |
| FR-028 | P0 | Key material shall remain non-project-truth convenience state. | No key is written to working root, docs, logs, or git-tracked execution files. |
| FR-029 | P0 | Anthropic base URL shall be allowlisted. | Only `https://api.anthropic.com` with no credentials and port empty/443 is accepted. |
| FR-030 | P0 | Electron renderer outbound traffic shall be blocked except loopback and Anthropic API. | `webRequest.onBeforeRequest` cancels non-allowlisted outbound requests and logs policy metadata. |
| FR-031 | P1 | Provider errors shall be classified. | Auth, rate limit, timeout, API error, network error, invalid base URL, and policy violation produce typed `SDK_FAILURE` details with key redaction. |

### 8.6 Attachments

| ID | Priority | Requirement | Acceptance |
|---|---:|---|---|
| FR-032 | P0 | UI shall allow file attachments from the selected working root. | File picker supports navigation, multi-select, preview chips, remove, and clear. |
| FR-033 | P0 | Server shall treat client attachment metadata as non-authoritative. | Server revalidates path, extension, file type, readability, symlink status, and size. |
| FR-034 | P0 | Attachment resolver shall enforce supported file types and budgets. | Extension, regular-file, per-file 10 MB, and total 18 MB raw-byte rules are enforced. |
| FR-035 | P0 | Anthropic provider shall map supported files to content blocks. | Images use base64 image blocks; PDFs use document blocks; text/markdown/csv use text document blocks. |
| FR-036 | P1 | Attachment failure handling shall be resilient. | Partial failures prepend a warning; total failure without text rejects the turn; UI preserves draft/attachments on failed send. |

### 8.7 Operator Toolkit and Local UI State

| ID | Priority | Requirement | Acceptance |
|---|---:|---|---|
| FR-037 | P1 | Toolkit panel shall expose per-turn options. | UI can set model/tools/max turns/mode/persona/governance metadata as supported by runtime. |
| FR-038 | P1 | Toolkit settings shall persist locally and remain non-authoritative. | Local presets do not override governance enforcement or project truth. |
| FR-039 | P1 | Chat drafts and attachment selections shall persist locally per root/persona/mode. | Malformed records are dropped; storage failures warn without breaking chat. |

### 8.8 Filesystem Execution Model

| ID | Priority | Requirement | Acceptance |
|---|---:|---|---|
| FR-040 | P0 | Execution roots shall follow the `docs/SPEC.md` layout. | Root contains `INIT.md`, package folders, and tool roots such as `_Aggregation`, `_Change`, `_Coordination`, `_Decomposition`, `_Estimates`, `_Reconciliation`, `_Archive`, `_Scripts`, `_Sources`. |
| FR-041 | P0 | Package folders shall follow flat `PKG-XX_Label` or `PKG-XXX_Label` structure. | Required subfolders are created or validated. No nested packages are introduced. |
| FR-042 | P0 | Deliverable folders shall follow `DEL-XX-YY_Label` or `DEL-XXX-YY_Label` structure. | Deliverable scan detects folders with `_STATUS.md` and valid DEL prefix. |
| FR-043 | P0 | Deliverable metadata files shall be canonical. | `_STATUS.md`, `_CONTEXT.md`, `_DEPENDENCIES.md`, `_REFERENCES.md`, `_SEMANTIC.md`, and `MEMORY.md` expectations follow SPEC. |
| FR-044 | P1 | Document kit files shall be supported as first-class knowledge buckets. | Datasheet, Specification, Guidance, and Procedure are detected for knowledge-type scope. |

### 8.9 Lifecycle and Dependency Contracts

| ID | Priority | Requirement | Acceptance |
|---|---:|---|---|
| FR-045 | P0 | `_STATUS.md` shall be the canonical lifecycle state file. | Status parser reads `Current State`, `Last Updated`, and history. |
| FR-046 | P0 | Lifecycle transitions shall be forward-only and actor-authorized. | Allowed transitions follow SPEC; unauthorized actors and backward transitions fail. |
| FR-047 | P0 | Human gate transitions shall require approval SHA evidence. | Transitions to `CHECKING` or `ISSUED` require a 7-64 char hex SHA-like token. |
| FR-048 | P0 | `Dependencies.csv` v3.1 shall be parsed and validated. | Required headers, enum values, identity rules, and warnings are exposed by contract APIs. |
| FR-049 | P0 | Dependency rows shall preserve provenance. | Active extracted rows require `EvidenceFile` and `SourceRef` or explicit `location TBD`. |
| FR-050 | P1 | Dependency writes shall preserve lifecycle behavior. | Rows are serialized with schema version, host deliverable consistency, and warnings for legacy/invalid data. |

### 8.10 Agents, Tools, and Governance

| ID | Priority | Requirement | Acceptance |
|---|---:|---|---|
| FR-051 | P0 | The instruction root shall include the indexed core agent suite and governance docs. | Packaged resources contain `agents/`, `docs/`, `AGENTS.md`, `README.md`, `WHAT-IS-AN-AGENT.md`, and `PROFESSIONAL_ENGINEERING.md`. |
| FR-052 | P0 | Agent instruction files shall declare type/class/surface/write-scope/blocking/output metadata. | Conformance is auditable against `AGENT_HELPS_HUMANS.md` and `docs/SPEC.md`. |
| FR-053 | P0 | Type 2 subagent injection shall fail closed. | Requires `CHIRALITY_ENABLE_SUBAGENTS=true`, persona allowlist, `contextSealed=true`, `pipelineRunApproved=true`, non-empty `approvalRef`, and Type 2 candidate files. |
| FR-054 | P1 | Deterministic tools shall remain indexed and callable by agents. | `tools/REGISTRY.md` lists tools by category with inputs/outputs; validation scripts remain executable. |
| FR-055 | P1 | Snapshot-producing workflows shall write immutable snapshot folders and mutable `_LATEST.md` pointers. | Reruns create new timestamped folders; prior snapshots are not overwritten. |
| FR-056 | P1 | CHANGE/publication workflows shall require explicit approval tokens and SHA checks. | Approval records include candidate SHA/action list; CHANGE rechecks HEAD before approved actions. |

### 8.11 Validation and Release

| ID | Priority | Requirement | Acceptance |
|---|---:|---|---|
| FR-057 | P0 | Unit and API tests shall cover runtime, workspace, lifecycle, dependency, scaffold, attachment, key storage, network policy, and packaging behavior. | `frontend/src/__tests__` remains comprehensive and `npm run test` passes. |
| FR-058 | P0 | TypeScript typecheck shall pass for Next.js and Electron code. | `npm run typecheck` exits zero. |
| FR-059 | P0 | Harness premerge validation shall be repeatable locally and in CI. | `npm run harness:validate:premerge` creates `frontend/artifacts/harness/section8/latest/summary.json` with required SDK test IDs. |
| FR-060 | P0 | Desktop distribution build shall include instruction-root integrity verification. | `npm run desktop:dist` runs build, packages DMG, and runs `instruction-root:integrity`. |
| FR-061 | P1 | CI shall upload stable harness summary artifact. | `.github/workflows/harness-premerge.yml` validates server readiness and uploads summary JSON. |

---

## 9. API Requirements

### 9.1 Harness APIs

| Endpoint | Method | Purpose |
|---|---|---|
| `/api/harness/session/create` | POST | Create a session bound to `projectRoot`, persona, and mode. |
| `/api/harness/session/boot` | POST | Boot a session and persist boot metadata. |
| `/api/harness/session/list` | GET | List sessions for a normalized project root. |
| `/api/harness/session/[id]` | GET/DELETE | Retrieve or delete a session. |
| `/api/harness/turn` | POST | Execute a turn and stream UI events over SSE. |
| `/api/harness/interrupt` | POST | Interrupt active turn for a session. |
| `/api/harness/scaffold` | POST | Scaffold execution root from decomposition markdown. |

### 9.2 Workspace APIs

| Endpoint | Method | Purpose |
|---|---|---|
| `/api/working-root/validate` | POST | Validate and normalize a working root. |
| `/api/working-root/tree` | GET | Return bounded file tree for the selected root. |
| `/api/working-root/scope` | GET | Scan deliverables and knowledge-type directories. |
| `/api/project/deliverables` | GET | Return deliverables plus knowledge decomposition metadata. |
| `/api/working-root/deliverable/status` | GET | Read `_STATUS.md` snapshot for a deliverable. |
| `/api/working-root/deliverable/status/transition` | POST | Apply an allowed lifecycle transition. |
| `/api/working-root/deliverable/dependencies` | GET/PUT | Read/write `Dependencies.csv` snapshot rows. |

### 9.3 SSE Event Contract

The turn stream shall emit named SSE events with JSON payloads:

- `session:init`
- `chat:delta`
- `chat:complete`
- `tool:result`
- `session:complete`
- `turn:error`
- `process:exit`

The stream must always terminate with a process-level completion/error signal unless the client disconnects and cancel cleanup runs.

---

## 10. Data and File Requirements

### 10.1 Instruction Root

Required entries:

- `AGENTS.md`
- `README.md`
- `agents/`
- `docs/`
- `docs/DIRECTIVE.md`
- `docs/CONTRACT.md`
- `docs/SPEC.md`
- `docs/TYPES.md`
- `docs/PLAN.md`

Instruction root may be overridden by `CHIRALITY_INSTRUCTION_ROOT`; packaged builds set it to `process.resourcesPath`.

### 10.2 Working Root

Requirements:

- Must be an absolute existing readable/writable directory.
- Must not be inside instruction root.
- Contains project execution state, packages, deliverables, and tool roots.
- Is the only location where agents write project truth.

### 10.3 Session Store

Default location:

- `{frontend cwd}/.chirality/sessions/*.json`

Override:

- `CHIRALITY_SESSION_ROOT`

Session record fields:

- `sessionId`
- `projectRoot`
- `persona`
- `mode`
- `createdAt`
- `updatedAt`
- `claudeSessionId`
- `bootFingerprint`
- `bootedAt`
- `model`

### 10.4 API Key Store

Electron storage:

- `app.getPath('userData')/credentials/api-key.enc`

Rules:

- Encrypted with Electron `safeStorage`.
- Process-global value is used by server runtime in packaged same-process builds.
- Not project truth.
- Not logged.

### 10.5 Execution Root Layout

Required or expected root entries include:

- `INIT.md`
- `PKG-XX_Label/`
- `_Aggregation/`
- `_Change/`
- `_Coordination/_COORDINATION.md`
- `_Decomposition/`
- `_Estimates/`
- `_Reconciliation/`
- `_Archive/`
- `_Scripts/`
- `_Sources/`

### 10.6 Deliverable Folder Layout

Required metadata:

- `_STATUS.md`
- `_CONTEXT.md`
- `_DEPENDENCIES.md`
- `_REFERENCES.md`

Minimum PREPARATION fileset also includes:

- `_SEMANTIC.md`

Document kit:

- `Datasheet.md`
- `Specification.md`
- `Guidance.md`
- `Procedure.md`

Additional expected/optional:

- `Dependencies.csv`
- `MEMORY.md`
- `_SEMANTIC_LENSING.md`
- `HASH_VERIFICATION_BYPASS.jsonl`

Disabled in this project profile:

- `_MEMORY.md`

### 10.7 Dependency Register

`Dependencies.csv` must follow schema version `v3.1` with 29 required core columns plus optional extension columns. Rows are append/lifecycle aware:

- Rows are not deleted when retired.
- `FirstSeen`, `LastSeen`, `Status`, and `SatisfactionStatus` track extraction and closure state.
- `ANCHOR` rows connect deliverables to definition/traceability nodes.
- `EXECUTION` rows capture information flow, prerequisites, handoffs, and constraints.

---

## 11. Non-Functional Requirements

### 11.1 Security and Privacy

| ID | Priority | Requirement | Acceptance |
|---|---:|---|---|
| NFR-001 | P0 | No project data shall require external storage. | All authoritative state is local files under working root. |
| NFR-002 | P0 | API keys shall not be written to project files or logs. | Key redaction is applied to provider errors; key storage stays under Electron userData. |
| NFR-003 | P0 | Renderer outbound traffic shall be allowlisted. | Non-loopback/non-Anthropic renderer requests are canceled. |
| NFR-004 | P0 | Attachment paths shall not follow symlinks. | Symlink attachments are rejected before provider execution. |
| NFR-005 | P0 | Working root shall not be inside instruction root. | Runtime rejects conflicting root selection. |

### 11.2 Reliability

| ID | Priority | Requirement | Acceptance |
|---|---:|---|---|
| NFR-006 | P0 | Harness turns shall be cancellable. | Interrupt/cancel aborts provider request and releases session lock. |
| NFR-007 | P0 | Runtime operations shall expose typed errors. | Harness and workspace errors include type, status, message, and details where applicable. |
| NFR-008 | P1 | Scaffolding shall be idempotent and recoverable. | Existing paths are preserved; failures include stage and created path inventory. |
| NFR-009 | P1 | File scans shall avoid runaway traversal. | Tree and scope scan depth/count limits are enforced. |

### 11.3 Performance

| ID | Priority | Requirement | Acceptance |
|---|---:|---|---|
| NFR-010 | P1 | Working-root scans shall remain responsive on large repos. | Scope scan caps directories at 2500 and depth at 8; tree limits entries per directory to 60 and depth to 6. |
| NFR-011 | P1 | Provider streams shall time out. | Anthropic stream timeout defaults to 90 seconds and can be overridden by env. |
| NFR-012 | P1 | Attachment budgets shall protect request size. | Per-file and per-turn raw-byte limits are enforced before provider call. |

### 11.4 Accessibility and UX Quality

| ID | Priority | Requirement | Acceptance |
|---|---:|---|---|
| NFR-013 | P1 | Keyboard users shall be able to resize/collapse panes. | Resize handles are focusable separators with arrow/Home/End behavior. |
| NFR-014 | P1 | Controls shall expose disabled/loading/error states. | Primary surfaces avoid silent failure and show typed feedback. |
| NFR-015 | P1 | UI shall avoid hydration mismatch from local browser state. | Browser-backed state initializes client-side and does not render conflicting server text. |

### 11.5 Auditability and Compliance

| ID | Priority | Requirement | Acceptance |
|---|---:|---|---|
| NFR-016 | P0 | Human approval remains non-delegable. | No automated endpoint can sign/seal/issue for reliance without human actor/approval evidence. |
| NFR-017 | P0 | Approval SHA evidence shall be captured for checking/issued transitions. | Status transition metadata includes SHA fields for human gate states. |
| NFR-018 | P1 | Validation artifacts shall be stable and reviewable. | Harness summary artifact path is deterministic and uploaded in CI. |

---

## 12. Validation Plan

### 12.1 Required Local Checks

From `frontend/`:

```bash
npm run test
npm run typecheck
npm run harness:validate:premerge
npm run instruction-root:integrity
```

Packaging check:

```bash
npm run desktop:dist
```

Expected packaging outputs:

- `frontend/dist/Chirality-0.1.0-arm64.dmg`
- `frontend/dist/mac-arm64/Chirality.app`
- `frontend/artifacts/harness/instruction-root-integrity/latest/summary.json`

### 12.2 Harness Validation Acceptance

The Section 8 harness validation shall verify:

- Server reachable.
- Session CRUD.
- Smoke stream ordering.
- Session persistence and resume continuity.
- Permissions behavior under `dontAsk`.
- Interrupt behavior.
- SDK-native stream handling with no legacy parser regressions.

### 12.3 CI Acceptance

The GitHub workflow shall:

1. Checkout repository.
2. Setup Node.js 20.
3. Install dependencies with `npm ci`.
4. Preflight validation script presence.
5. Start Next server.
6. Poll readiness.
7. Run `npm run harness:validate:premerge`.
8. Verify stable summary artifact.
9. Upload summary artifact.

### 12.4 Manual Release Verification

For macOS DMG:

- Binary is arm64.
- `LSMinimumSystemVersion` is `15.0.0` or later.
- Codesign reports no developer TeamIdentifier and adhoc signature.
- App resources contain `agents/` and `docs/`.
- App launches and working-root selector is available.

---

## 13. Success Metrics

1. A first-time operator can select a working root, inspect the file tree, and start a WORKBENCH chat turn within one app session.
2. A decomposition markdown can be used to scaffold a SPEC-conformant execution root without manual folder creation.
3. A deliverable can be scanned, inspected, and transitioned according to lifecycle rules with approval SHA enforcement for human gate states.
4. Harness premerge validation passes in CI and produces a stable summary artifact.
5. Desktop DMG builds locally and passes instruction-root integrity checks.
6. No API key or project truth is written outside its approved storage zone.
7. Unsupported PIPELINE variants remain visible as disabled options, preserving operator awareness of roadmap scope.

---

## 14. Known Gaps and Risks

| ID | Area | Risk / Gap | Product Decision |
|---|---|---|---|
| KG-001 | Persona prompting | Current `StubPersonaManager.buildSystemPrompt()` validates persona existence but does not compose full instruction-root context into the Anthropic request path. | P0 before production reliance: provider turns must include selected agent instructions and working-root governance context. |
| KG-002 | Runtime enforcement | Several K-* invariants are enforced by instructions and human review, not by a runtime guard that blocks non-compliant writes. | Accept for current governed-human use; track runtime guardrails as future hardening if risk profile increases. |
| KG-003 | Staleness/dirty state | K-STALE-1, K-VAL-1, K-MERGE-1, K-AUTH-2 automated enforcement is partial or future-scoped. | Keep human CHANGE constraints active; do not claim complete automated enforcement. |
| KG-004 | Registry ownership | Current membership belongs in the source registries, not mutable count prose. | Treat `AGENTS.md`, `skills/README.md`, `tools/REGISTRY.md`, and generated test discovery output as the active registry surfaces. |
| KG-005 | Release target ambiguity | README mentions Windows packaging, but current runbook/build config targets macOS 15+ Apple Silicon DMG. | PRD current release scope is macOS arm64 only; Windows requires explicit scope amendment. |
| KG-006 | Optional hardening | Deliverable lock, project graph generation, unified run records, and staleness tooling are retired/out-of-scope in current decomposition. | Do not include in current release commitments except as future roadmap. |
| KG-007 | Professional reliance | App supports auditability but does not make outputs professionally reliable by itself. | Product copy and UI must preserve "draft/decision support until human review" posture. |

---

## 15. Traceability Summary

| Product Area | Source Requirements |
|---|---|
| Desktop build/package | SOW-001, SOW-002, SOW-044, SOW-047, OBJ-001, OBJ-008 |
| UI workflow | SOW-022 through SOW-027, SOW-046, SOW-050, OBJ-005 |
| Harness runtime | SOW-003 through SOW-006, SOW-011, SOW-012, SOW-045, OBJ-002 |
| Attachments | SOW-007 through SOW-010, OBJ-003 |
| Filesystem model | SOW-013 through SOW-018, OBJ-004 |
| Agent/governance | SOW-017, SOW-019 through SOW-021, SOW-030, SOW-031, SOW-039 through SOW-043, OBJ-006 |
| Validation/examples | SOW-028, SOW-029, SOW-048, SOW-049, OBJ-006 |
| Integrity hardening | SOW-032, SOW-033 in scope; SOW-034 through SOW-038 retired/out in current decomposition |

---

## 16. Approval and Change Control

This PRD is a product requirements artifact. It does not supersede:

- `docs/DIRECTIVE.md`
- `docs/SPEC.md`
- `docs/TYPES.md`
- `docs/CONTRACT.md`
- `AGENTS.md`
- Active decomposition and scope-change records under `execution/_Decomposition/`

Changes to this PRD that alter scope, release targets, safety posture, data contracts, or professional responsibility boundaries should be handled as governed product changes and traced back to stable SOW/OBJ/DEL identifiers or a new approved decomposition amendment.

---
