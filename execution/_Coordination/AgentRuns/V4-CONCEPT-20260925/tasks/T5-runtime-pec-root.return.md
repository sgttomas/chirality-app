# Reverse-engineering report: Chirality Runtime, PEC, and the Root program context (input to App v4)

**Basis.** `main@2b0572fe0` in the worktree `…/chirality-app-v4-architecture-9f35c4`. I only read files. I ran no builds or tests, made no network calls, and wrote nothing except scratch text I extracted from the HTML plans. Paths are relative to the repo root, and line numbers refer to this basis.

**Evidence labels.** [accepted requirement], [described design], [implemented (code path)], [test defined], [executed check (record)], [owner feedback], [agent inference], [unrealised intention].

---

## 0. Summary

- **Runtime today.** Runtime is a single Node service that an application owns. It hosts a stock `codex app-server`, pinned by version (0.154.0), over stdio. It exposes HTTP/JSON and SSE over a private Unix socket, with a typed Node client and a CLI. The Chirality App is its only production consumer. The service replaced a heavier per-user daemon on 2026-09-11/12. That daemon ran a patched Codex, filtered the event stream and vetoed configuration, and it broke ordinary work. That replacement is the most important supplier lesson in this corpus.
- **Application tools.** Application-owned "dynamic tools" were added on 2026-09-19/20 with SWBPIPE as the intended first consumer. They are implemented and exercised against a controlled (fake) Codex transport. They have **not** been proven with a live model turn, with native descendants, or with a real SWBPIPE mutation.
- **Engines.** `engine-claude` and `engine-pi-omlx` still compile and have tests, but nothing in the service wires them in. They are history from the Claude Agent SDK and Pi/oMLX periods.
- **PEC.** PEC is a coordination plane that "doesn't need to exist": a projection of Git-tracked file truth that can be rebuilt, plus a presence layer that expires. The design is extensive. The implementation is early P1 work (store, guard, API schema, loop registry). It is being rebaselined (SCA-005) to the new shared loop file shapes and to the per-application Runtime topology.
- **Root.** Root is the repository's control plane and steward of shared instructions. It carries the operational definitions (role, workflow, skill, tool, brief, run evidence) and the rule that human judgment is the hinge. Root text also carries several choices that are specific to the App, most notably "Codex is the sole engine for the App MVP."

---

## 1. Chirality Runtime (`projects/chirality-runtime/`)

### 1.1 Purpose and current identity

- **What it is.** Runtime is "an application-owned service. The Chirality App starts, owns and stops it as a child process; the service owns the stock, version-pinned `codex app-server` child. The App is the only production consumer." (`projects/chirality-runtime/README.md` lines 8–14) [described design; implemented in `packages/daemon/src/app-owned-composition.ts`, `standalone-bin.ts`]
- **Built for reuse beyond the App.** It stays independent of Electron and Next "so a later Chirality application can run it as a sidecar." That is a constraint Root recorded across products (`docs/governance_harness/_DECISIONS/D-GOV-43_supplement_topology_A2.md`, "Cross-product constraint recorded now"; `docs/SPEC.md` §14, lines ~890–899) [accepted requirement].
- **Ownership split.** Runtime owns its product scope. Shared instructions and tools remain Root governance, and client integration stays with the owning project (`projects/chirality-runtime/AGENTS.md`) [accepted requirement].
- **Governance posture.** Two layers apply.
  - The PRD text (`docs/PRD.md`) still carries the label `GATE3_REVIEW_NOT_ACCEPTED` and describes the daemon era. Its approval is recorded in `docs/PRD_AUTHORITY.md` and in `execution/_Coordination/MIGRATION_ACCEPTANCE_2026-09-06.md`.
  - Since D-GOV-43 the PRD is read through `execution/_Coordination/AgentRuns/RUNTIME_DGOV43_HOLD_CLOSURE_20260912/PRD_REVISION.md`. That revision retired DEL-02-07 through DEL-02-12 (supervisor, exact supply pinning, hosted account/consent, closed event schema, retirement/restart, conformance fan-in) and kept only DEL-02-06, stewardship and release assurance [accepted requirement].
  - [agent inference] What the Runtime project is currently accountable for is much thinner than its PRD reads.

### 1.2 What it provides to an application

**Process and transport** (`README.md` §Architecture; `docs/SPEC.md` §14.1) [implemented (code path)]
- One process composes `RuntimeService`, `SessionStore`, `TurnCoordinator`, `DelegatedRuntime`, `CodexSupervisor` and `CodexLogin`.
- It prints one JSON ready line on stdout.
- Routes are HTTP/1.1 and SSE on a Unix socket with a 0600 socket file inside a 0700 directory. Per-launch client tokens stay private to the owning host. There is no TCP listener.
- Route map: `packages/contracts/src/protocol.ts` lines 19–87 (health, projects, roles, methods, sessions, application tools, and legacy `models`/`credentials`).

**Stock Codex with a pinned version** [implemented; accepted requirement]
- The composition refuses any `codex --version` other than `expectedVersion` (`app-owned-composition.ts`, the `AppOwnedRuntimeConfig` comment).
- The current basis is 0.154.0 (`docs/APPLICATION_CONSUMER_GUIDE.md` line 53).
- No patched supplier is used.

**Effective Codex home with separate authentication** [implemented in `packages/daemon/src/codex-effective-home.ts`; described design]
- Runtime shares the user's config, skills, plugins, MCP definitions and sessions store by reference.
- It keeps `auth.json` and the models cache private. Sign-in and sign-out go through Codex's own account methods.
- The consumer guide warns that "a separate overlay alone does not prove every credential backend … is isolated" (lines 72–77).

**Faithful stream**
- Upstream method names and payloads are preserved. Every server request is answered; unfamiliar requests get an explicit JSON-RPC error (`README.md` lines 34–39) [described design; implemented in `codex-supervisor.ts`].

**Execution separate from observation**
- Runtime owns the active turn. Closing a client's stream does not interrupt it; an explicit Stop does.
- Resume, fork and compaction come from Codex. Runtime keeps its own session index (`README.md` lines 40–48) [implemented].

**Supplying roles and instructions** [implemented (code path)]
- `thread/start` and `thread/resume` carry `developerInstructions` (`packages/daemon/src/codex-supervisor.ts` lines ~191, ~219).
- Each Chirality role is materialized as a Codex native-agent config file (`agents.<ROLE>.config_file`) built from captured, hash-checked bytes (`packages/core/src/product-native-role-config.ts`).
- `docs/AGENT_WORKFLOW_RUNTIME.md` lines 167–180 records that loaded Codex 0.154.0 threads can ignore instruction overrides, so changed guidance needs an idle unload, a cold resume and injected history [described design].

**Method catalog**
- The catalog discovers workflows and skills and exposes list, inspect and selected-context operations (`packages/core/src/method-catalog.ts`; routes `roles`, `methods`) [implemented; test defined `tests/method-catalog.test.ts`].

**Managed delegation code**
- Present: `packages/core/src/agent1-run-coordinator.ts` (`Agent1ManagerHooks.delegate({sealedBrief})`), `delegated-runtime.ts`, `descendant-tracker.ts` [implemented].
- Its use on the Codex path now sits beside Codex-native delegation. D-GOV-35 made that a separate delegation class (§3.2).

### 1.3 Application-owned (dynamic) tools

**Origin.** The owner directed on 2026-09-20: "we need to work on those dynamic tools now. They will be application specific. SWBPIPE is the first app to receive tools" (`execution/_Coordination/AgentRuns/APPLICATION_DYNAMIC_TOOLS_20260920/PLAN.md` line 3) [owner feedback].

**Interface** (`docs/APPLICATION_TOOLS.md`)
- **Registration.** The owning host (not an ordinary project client) calls `registerApplicationTools(projectId, sessionId, {applicationId, workspaceId, workspaceGeneration, timeoutMs, tools[]})` after `createSession` and before the first turn (lines 9–28).
- **Dispatch.** Host-only routes let it list pending calls and complete them with `{bindingId, result:{success, contentItems}}` (lines 50–88) [implemented in `packages/daemon/src/application-tools.ts`, `packages/contracts/src/application-tools.ts`, `packages/client/src/client.ts`].

**Constraint imposed by the supplier**
- Stock Codex 0.154.0 accepts `dynamicTools` only on `thread/start`, never on `thread/resume`. The catalog is therefore immutable for a conversation, and a changed catalog needs a new conversation (lines 36–41) [described design; implemented].
- Handler bindings do not survive a restart, so the host must rebind after one (lines 43–48).

**Division of responsibility**
- Runtime supplies transport, lifecycle, deduplication, cancellation and caller identity.
- The application owns argument/domain validation, live state, human review and commits.
- Runtime validates only bounded JSON. It does not run full JSON Schema checks (lines 1–5, 69–76) [described design].

**Limits.** 256 KiB of canonical JSON, 128 descriptors, timeouts from 1 second to 1 hour, and at most 1,024 calls retained per turn (lines 119–124) [implemented].

**Semantics that matter for SWBPIPE**
- `success` reports that the tool ran, not that anyone accepted the result.
- A submit tool must report "queued" until the application actually commits.
- The application must deduplicate its own domain operations.
- Replay never re-runs handlers (lines 90–117) [described design].

**Review and repair.** An independent review found one P1: a cancellation race in which a request could dispatch late, after the turn was adopted. It was repaired, with six regression tests on the real registry (`PLAN.md` lines 48–52) [executed check (record)].

**What is actually verified**
- The full Runtime suite recorded 42 files and 401 tests passing (`PLAN.md` line 41) [executed check (record)].
- An offline probe of stock 0.154.0 accepted a function descriptor on `thread/start` (line 42) [executed check (record)].
- Explicitly **not** established: "No live model turn, native descendant inheritance, or SWBPIPE mutation" (`APPLICATION_TOOLS.md` lines 146–153).

**Related negative observation (MCP).** The desktop-bundled Codex `0.155.0-alpha.9.2` used the legacy MCP `2025-06-18` handshake and failed against a server that accepts only the modern protocol. This is configuration-specific and not a universal result (`execution/_Coordination/AgentRuns/MCP_V2_COMPATIBILITY_20260920/README.md`) [executed check (record)].

### 1.4 How SWBPIPE is meant to consume Runtime

**Two paths are documented.**
1. **First selected path (no embedded Runtime).** A development Codex session calls the Piping JSON CLI, which uses a private bridge to Piping's live workspace controller. "That path does not require this embedded Runtime setup" (`docs/APPLICATION_CONSUMER_GUIDE.md` lines 9–14). Piping's coordination note confirms this route and that no Runtime or App configuration change is needed (`projects/chirality-piping/execution/_Coordination/AgentRuns/HELP-HUMAN-PIPING-20260918-UI-IMPLEMENTATION/instances/CONTINUATION_2026-09-24/COORDINATION.md` lines 7–8, 21) [described design; the path is in progress on the Piping side].
2. **Later embedded path.** Piping, a Tauri app with a Rust core, runs its own Runtime instance with a private data directory. It must either host the Node client in a sidecar or reimplement the wire protocol in Rust ("there is no Tauri sidecar distribution yet", guide lines 20–21, 30–35). Setup order: register or initialize the project, check status, create the conversation (HELP_HUMAN by default), register the tool catalog, then run turns and dispatch calls to Piping's existing handlers (lines 99–129) [unrealised intention].

**Proposed first SWBPIPE tools**
- `inspect_selection`, `preview_operations`, `submit_proposal`, `get_proposal_status`.
- There is **no agent-facing Apply**. The human applies through Piping's controller.
- The inspection basis is workspace generation + identity + revision + canonical model hash (`APPLICATION_TOOLS.md` lines 126–139; `PLAN.md` line 11) [described design].

**Recorded integration gaps**
- Tauri sidecar packaging.
- Rebinding tool handlers at restart.
- Qualifying the native path (tool request and result, denial/Stop, restart and resume, descendant inheritance).
- Isolation of account and UI state.
- Local providers. The composition "couples default session/model selection to hosted account status" (guide lines 165–177).

[agent inference] The embedded integration exists today as a reviewed interface and a set of controlled fixtures. No second application has run it.

### 1.5 Engines: `engine-claude` and `engine-pi-omlx`

**`engine-claude`** (`packages/engine-claude/src/index.ts`, 59 lines)
- A thin `AgentEnginePort` adapter over the adapter IDs `anthropic-direct` and `claude-agent-sdk`, driven by an injected runtime port and an Anthropic API key.

**`engine-pi-omlx`**
- Pins `@earendil-works/pi-coding-agent` and `pi-ai` 0.82.0 (package.json).
- Contains an oMLX client, a turn runtime and a read-only tool (`packages/engine-pi-omlx/src/*`).

**Current status**
- Both remain in the TypeScript build graph (`tsconfig.json` references).
- `engine-pi-omlx` is still exercised by `tests/pi-turn-runtime.test.ts`, `omlx-client.test.ts` and `pi-packaging.test.ts`.
- Neither is imported by any core, daemon or CLI source file (grep at this basis) [implemented but unwired].
- The README's package list omits both (lines 90–106).
- The 2026-09-12 topology comparison called `engine-claude` "dead code" and said `engine-pi-omlx` was "registered only on the local-model path" (`projects/chirality-app-dev/execution/_Coordination/AgentRuns/APP_V3_CODEX_HOST_REPLATFORM_20260912/TOPOLOGY_COMPARISON.md` F8). That local-model path was then retired from the composition (A2 supplement, item 13) [accepted requirement].

**Why they remain**
- They are "preserved as reference without release obligations"; preserving them "creates no obligation to keep unused implementations compiling" (`README.md` lines 128–141).
- The same section records that a live Pi/oMLX validation passed: client → daemon → Pi → oMLX inference, a bounded read, and a durable child record with its parentage [executed check (record), historical].
- The App-facing engine registry "contains Codex only for the MVP" (`docs/AGENT_WORKFLOW_RUNTIME.md` lines 220–226) [accepted requirement].

### 1.6 Tests

- About 42 test files (`tests/*.test.ts` plus the client and CLI package tests).
- Coverage areas:
  - app-owned composition and standalone startup;
  - the Codex App Server client, supervisor and effective home;
  - application tools: registry, supervisor and composition;
  - delegated runtime, worker retirement and descendant tracking;
  - method catalog, instruction basis and method transitions;
  - native steering, plan admission and role config;
  - turn hardening and the v3 API;
  - legacy Pi/oMLX.
- They run against `tests/fake-codex-transport.ts`, a controlled Codex [test defined].
- The consumer guide states the boundary explicitly: "Controlled transports do not establish these facts" for native behavior (line 175).

### 1.7 Maturity: what is proven and what is only described

| Capability | Standing |
|---|---|
| App-owned service + stock Codex; S-1…S-8 (Plan Mode, real tool use past 30 s, save/reuse a workflow, delegated child gets its role, quit/relaunch continuation, interrupt/denied approval, sign-in/out scoped to Chirality) | [executed check (record)] PASS on the App run from source, 2026-09-12 (`…/APP_V3_CODEX_HOST_REPLATFORM_20260912/RUN_LOG.md` lines 145–164); signed build evidence at lines 210–225; App v3.0.0 released (`projects/chirality-app-dev/README.md` line 7) |
| Dynamic tools | [test defined] controlled; [executed check (record)] offline descriptor probe; live turn **unproven** |
| Embedding in a second app (Tauri) | [unrealised intention] |
| Local models via Codex model providers | [unrealised intention] (D-GOV-43 item 13) |
| PEC as a Runtime client | "compatibility is unverified and is not an MVP prerequisite" (`README.md` lines 104–105) |

---

## 2. PEC coordination plane (`projects/pec/`)

### 2.1 Purpose and the principle that it "doesn't need to exist"

**Definition.** PEC is "a deterministic, rebuildable projection of governed file truth, plus an ephemeral presence layer." It embodies Step 0 (Discover) and the deterministic parts of Step 1 (gate review, decision slate) of the development loop. It is "the coordination plane that doesn't need to exist: … deleting PEC degrades throughput, never correctness" (`projects/pec/docs/PRD.md` §1.1; `README.md` lines 3–11) [accepted requirement, PRD v2.2 adopted by D-PEC-58/61/67/68].

**Problem it addresses** (PRD §2) [accepted requirement, as the adopted problem statement]
- Step 0 is "the most expensive, most repeated computation": more than 1,200 `_STATUS.md` files and about 230 decision records are re-derived from prose each iteration.
- "Sessions cannot see each other."
- There is no join between "a run happened" and "a deliverable moved."

**Permanent non-goals** (PRD §4.2) [accepted requirement]
- Not a system of record, a ruling surface, an orchestrator, a lock manager, a Git actor, or "a human project-management tool."

**Invariants** (PRD §6) [accepted requirement]
- PEC-K-01: graceful absence.
- PEC-K-02: files govern.
- PEC-K-03: pull-oriented, used as each consumer chooses.
- PEC-K-04: staleness is a SHA comparison.
- PEC-K-05: two trust tiers.
- PEC-K-06: observation, not participation.
- PEC-K-08: everything derived is explainable.
- PEC-K-10: content-minimal.
- PEC-K-11: modes are available but never forced.

**Falsifiability.** If uptake stays negligible after P3, "PEC is deleted and, by PEC-K-01, nothing breaks" (PRD §11) [accepted requirement].

### 2.2 Capabilities (designed)

**Record tier (reconciled; citable with sources, PRD §7.1)**
- Loop, workplan and gate, receipt, decision row, fence, package and deliverable census, dependency edge, run record, candidate brief, orientation snapshot, drift finding.

**Presence tier (operational, expires on a TTL, never citable, PRD §7.2)**
- Session, worktree/Git ref, presence record, parent→child hierarchy edge, scope claim (with overlap detection).

**Functional requirements** (PRD §9)
- Orientation with per-claim citations (PEC-ORI).
- Incremental reconciliation driven by Git deltas, parity-checked against the practitioner harness (PEC-RCN).
- Advisory evaluation of gate preconditions and a cross-loop decision slate, "Waiting on you" (PEC-GAT, PEC-DSH-004).
- Presence board and advisory overlap warnings (PEC-PRS).
- Idempotent ingest; the record tier never rests on a stream event alone (PEC-STR).
- Local Unix-socket API, ≤100 ms at p95 (PEC-API).
- Dashboards (PEC-DSH).

### 2.3 Users and agent access

- Users are the human owner through dashboards, and harnesses as machine consumers when they are explicitly enabled. Under the current access classes, agents "never call PEC directly by instruction" (PRD §8) [accepted requirement].
- On 2026-09-25 the owner ruled D-PEC-90 R-A. Agents may act on PEC record-tier data as true as of its examined-through commit, within stated bounds, and authority stays file-native. Reliance begins only at a PEC release whose gates prove parity and coverage. The owner added, verbatim: "agents may eventually query PEC directly, yes. Through tool calls." (`execution/_Coordination/_DECISIONS/D-PEC-90_RULING_2026-09-25.md`) [owner feedback; accepted as product direction; implementation deferred].

### 2.4 Status

- **Implementation.** The P1 code under `projects/pec/v2/` is:
  - an API v1 JSON Schema (`contracts/api/v1/schema.json`);
  - a loop registry adapter;
  - a SQLite store with a content-minimal guard (`src/pec_v2/core/content_minimal_guard.py`, `adapters/storage/sqlite_store.py`);
  - scanner and enforcement tests.
  
  No reconciler, orientation service, presence or dashboards exist yet (`docs/STATUS.md` "Current state"; D-PEC-90 clarification) [implemented, partial].
- **Lifecycle census.** Of 64 deliverables: 32 OPEN, 26 INITIALIZED, 4 CHECKING, 2 IN_PROGRESS, none ISSUED (`STATUS.md`) [executed check (record)].
- **Recent work.** Store and guard correction slices merged on 2026-09-24/25 (PRs #893, #897, #903) with independent verifier PASS. "Hosted CI still runs no v2 Python check" (`STATUS.md` carried residuals) [executed check (record)].
- **SCA-005** (opened 2026-09-23, D-PEC-86) rebaselines the feed model on the new shared App/Piping loop shapes and on the A2 per-application Runtime.
  - Mismatch table: `execution/_Coordination/ASSESSMENT_2026-09-23_APP_PIPING_PEC_UNISON.md`, for example `WORK_GRAPH.json` → `WORK_GRAPH.md`, and per-loop receipt ledgers → one `RECEIPT.md` per run.
  - Checkpoint 2 was accepted on 2026-09-25 (D-PEC-92); checkpoint 3 remains.
  - Selected presence option P-β: presence comes from Git plus hooks only. Runtime SSE bridges and live hierarchy are deferred behind an explicit trigger, because under A2 no shared daemon remains to observe, and reading Codex/Runtime user-data was rejected (`execution/_Coordination/SCA-005_PREP_2026-09-23/FEED_MODEL_V2_DESIGN_NOTE.md` §5.3, lines 525–565, 675–715) [accepted checkpoint; described design].

### 2.5 History as a precedent for agents embedded in an application

- **Before 2026-07-24.** PEC was a human-facing engineering execution-control app: MDL, RAIL, decisions, risks, approvals, a 14-role RBAC scheme, and SQLite. This v0.4 prototype is now a frozen reference corpus (PRD §13; `plans/pec_bridge_integration_plan_2026-07-04.md`).
- **Its agent sidecar** was reduced to a deterministic project adapter. It logs in as an owner-provisioned, non-admin "PEC agent person" and calls only PEC's RBAC HTTP API. Its dispatch table omits accept/apply, approval, decision and check outcomes, waiver, issue, and access changes. "The shared runtime decides which adapter acts, if any, a governed session receives" (`projects/pec/agent-sidecar/README.md`; commit `7d4d3e407`, 2026-07-23) [implemented, frozen].
- **The pivot (D-PEC-57, 2026-07-24).** The owner direction was summarized, not verbatim, as "as a human-used project-management tool it has no interest." The understood user changed "from a multidiscipline human team to the owner plus an agent fleet across concurrent sessions" (`execution/_Coordination/_DECISIONS/D-PEC-57_coordination_plane_pivot.md`) [owner feedback (summarized)].

### 2.6 What PEC says about coordinating many agents

- **The modes ladder** (PRD §5) grades usefulness by concurrency. It runs from pipeline and conversation (zero contact) through a workbench (WORKING_ITEMS with TASK children) to "Agent 0s, concurrent" with overlapping scope, where PEC is "essential for throughput when adopted (not for soundness — file fallback remains)." The doctrine note says concurrent Agent 0s "have no common parent below the human" [accepted requirement].
- **The Runtime/PEC seam is unresolved.** The event-contract home, auth reuse and the daemon's global event feed remain open owner decisions (PRD §16 items 2, 6, 9) [unrealised intention].

### 2.7 Adjacent evidence: Task Management at agent scale

- **Adoption.** D-GOV-32 adopted the Task Management PRD, Rev 2 (`plans/chirality-task-management/PRD_CANDIDATE_2026-07-31.md`) [accepted requirement].
- **Owner direction**, verbatim in its §1: "The task manager shouldn't be dispatching tasks for working in deliverables. Those should be discovered via the development loop. But as matters arise … that can't or shouldn't be resolved in that session need to have a means of being identified and worked on later" [owner feedback].
- **Measured findings** from the architecture review (`plans/chirality_task_management_architecture_review_2026-07-31.html` §01–02):
  - Emission of concerns is enforced but consumption is not: 22 concern-generating mechanisms, and only 5 gates that read them back.
  - Decision registers close (269 of 275 ruled); registers filed beside the flow do not (29 of 30 routed notices open; 0 of 12 disposition rows closed).
  - "What actually closes items … is adoption into a loop's own instruments." The design became a disposition ledger per loop, bound into each loop's entry procedure [executed check (record), measured at `a7371ed94`].

---

## 3. Root program architecture

### 3.1 How the pieces relate

**Root**
- "The human-governed repository control plane and the steward of shared instructions, tools and governance. Project roots own their product contracts, implementations, delivery scope and product evidence" (`docs/PRD_ROOT.md` §1.1 "ID-1 replacement") [accepted requirement per the file's status banner; the migration clauses are marked PROSPECTIVE, so standing is mixed].
- Truth lives in Git-tracked plain files. Domain engines own authoritative domain truth, and "Chirality governs the work *around* the engine" (§5.1 N-1, K-DOMAIN-1) [accepted requirement].

**Runtime**
- Owned by `projects/chirality-runtime` (§5.2 O-2, O-11, marked PROSPECTIVE).
- "Runtime transport executes and carries work but never grants project authority; user-data runtime state remains operational rather than project truth" (O-2).

**App** — a Runtime client, and the only production consumer (Runtime `README.md`).

**PEC** — optional coordination; never authority (§2).

**Piping (SWBPIPE / OpenPipeStress)** — a situated domain application with its own UI, engine and truth. The program charter calls it "neither a plugin nor an Agent 2" (`plans/chirality_program_architecture_and_tandem_review_2026-07-25.html` §02) [described design, non-governing].

**`_DomainEngines/`** — the tier-0 control area for domain-engine integration (`_DomainEngines/DOMAIN_ENGINE_INDEX.md`) [accepted requirement]:
- Adopted profiles: `profiles/open_pipe_stress.yaml` (ADOPTED, MANUAL_BRIDGE L0, with L3 operation proposals as the ruled destination) and `profiles/pec.yaml` (READ_ONLY).
- A profile declares:
  - authoritative artifacts, readable artifacts, and protected versus agent-writable paths;
  - deterministic tools with modes and `requires_human_confirmation`;
  - an operation-proposal lifecycle `draft → ready_for_review → accepted/rejected → applied`;
  - `professional_boundary.agent_must_not_claim` ("certified", "code compliant", "validation-passed implies engineering correctness", …).
- The generic method is `workflows/domain-engine/` (integration levels `MANUAL_BRIDGE | READ_ONLY | DOMAIN_CONTROLLED_WRITE | OPERATION_PROPOSAL | EXTERNAL_RESULT_STATE`; `resources/contract.md`).

**Program framing** [described design; explicitly non-governing]
- The 2026-07-25 charter reads the program as a "capability wheel": "a situated application is a declared composition, not a leaf in a hierarchy."
- It proposes an "application environment profile" as a candidate.
- It names the App's possible second identity as a "reusable human–agent work surface."
- The 2026-07-28 tandem review found both the reusable work surface and resource governance with "no governed home." It also named a pattern of "code first, carrier later" for Runtime (`plans/chirality_program_architecture_tandem_comparison_2026-07-28.html` §01, §03, §04 Q4–Q5).

### 3.2 Operational definitions

| Term | Definition and source |
|---|---|
| Agent | "An LLM operating with instructions, supplied context, available tools, and actual host permissions" (`AGENTS.md`) |
| Role | A persistent way of contributing: HELP_HUMAN (Type 0), HELPS_HUMANS and WORKING_ITEMS (Type 1), TASK (Type 2). Each has `agents/AGENT_<ROLE>.md` with PROTOCOL/SPEC/STRUCTURE/RATIONALE (`docs/WORKFLOW_COMPONENT_STANDARD.md` §Components, §Role instructions). The machine inventory `agents/registry.json` declares type, `direct_entry`, `delegates_to`, tool ceiling and write-scope ceiling. TASK has `delegates_to: []` |
| Skill | "Reusable bounded contextual instruction with a canonical `SKILL.md`." In the App, availability follows Codex's native `skills/list` (`docs/AGENT_WORKFLOW_RUNTIME.md` lines 43–82) |
| Workflow | "Reusable coordination or method guidance" at `WORKFLOW.md`, looked up project → user → bundled. Selection keeps a source-qualified identity and never silently rebinds. An optional `execution.json` can only restrict tools (lines 63–110). Loading one "never creates another role, launches execution, or grants additional capabilities" (`WORKFLOW_COMPONENT_STANDARD.md` lines 22–25) |
| Tool | "Performs a deterministic operation with explicit inputs, outputs, scope, errors, and repeat-execution behavior." "A documented command is not evidence that a host exposes it" (`AGENT_WORKFLOW_RUNTIME.md` line 210) |
| Brief | Run-specific instructions: purpose, basis, context, permissions, targets, outputs, checks, return path. The effective boundary is host ∩ role ∩ workflow ∩ brief (`AGENTS.md`; `AGENT_WORKFLOW_RUNTIME.md` lines 189–197) |
| Plan | An optional ad hoc plan, "not … a reusable or accepted workflow"; native Plan Mode is a separate `interactionMode` (lines 228–245) |
| Run evidence | A durable tree at `_Coordination/AgentRuns/<RunID>/` (plan, briefs, returns, notices, handoff) and a work graph at `execution/_Coordination/WorkGraphs/<undertaking>/WORK_GRAPH.md` for the App and Piping. Placeholder runs are prohibited (`docs/PRD_ROOT.md` §5.4 E-1). Actual supplied origins and hashes are recorded; loading done by instruction is labelled "instruction-asserted" (`AGENT_WORKFLOW_RUNTIME.md` lines 182–216) |
| Delegation classes | "Chirality-managed" (`delegate_agent`, sealed brief, governed child) and "delegated-harness-native" (Codex's native descendants inside a hard outer envelope; no child allowlist or fan-out cap; not automatically classed as Agent 2) (`docs/governance_harness/_DECISIONS/D-GOV-35_delegated_harness_native_class.md` items 1–4) |
| Orchestration | Fan-out/fan-in and supervised many-to-many patterns; the recorded work graph governs execution; sibling writes are disjoint or serialized; siblings use no undeclared direct messaging (`D-GOV-12`) |

All rows are [accepted requirement], except that `WORKFLOW_COMPONENT_STANDARD.md` and `AGENT_WORKFLOW_RUNTIME.md` describe themselves as "prospective … authorized for Root implementation … do not establish final acceptance" (their status lines).

### 3.3 Root governance v4 inherits vs choices specific to the App product

Root `AGENTS.md` says: "Applicable project instructions may specialize shared instructions but may not weaken Root governance."

**Root governance** (in `docs/DIRECTIVE.md`, `CONTRACT.md`, `SPEC.md`, `TYPES.md`, `PRD_ROOT.md`) [accepted requirement]:
- Only humans author binding approvals, and approvals bind to a SHA (K-AUTH-1/2, N-3).
- File-native authority, with gitignored projections allowed (N-1, D-GOV-01).
- Domain engines own domain truth (K-DOMAIN-1).
- Provenance, TBD-not-guess and conflict surfacing (N-4).
- Write containment (N-5).
- Capability never confers authority (O-4).
- The four-role hierarchy with no delegation below TASK.
- The two delegation classes (D-GOV-35).
- Run evidence (E-1…E-8).
- Evaluation, iteration and release as distinct human judgments (§4.2).
- The standing Git merge grant (§5.3.1).

**Choices specific to the App, recorded in Root text** [accepted requirement, scoped to the App MVP]:
- "For the App MVP, Codex is the sole engine qualification and release target."
- The App hosts a stock Codex App Server, does not filter notifications, and does not pin approval or sandbox policy.
- Skill browsing is hidden in v3.0.0.
- Workflow drafts go under `.chirality/workflow-drafts/`, registered through the Workflows panel.
- A seeded editable product `AGENTS.md` (`projects/chirality-app-dev/instructions/AGENTS.md`).

These appear in Root `AGENTS.md`, in `docs/AGENT_WORKFLOW_RUNTIME.md` lines 72–82, 138–165 and 220–226, and in D-GOV-43.

[agent inference] By their own wording these App clauses are scoped to "App MVP" and to D-GOV-43. On their face they are not Root-wide doctrine a v4 must inherit. Retiring them would still require the governed M2/G4 change route, because they sit on Root instruction surfaces.

### 3.4 Merge policy (§5.3.1)

- Standing owner authorization since 2026-09-12. Agents may commit, push, open or update PRs and merge within authorized scope when required CI passes and independent review, covering the actual candidate, has no unresolved blocking findings.
- It grants no acceptance of governed content, no release, no force-push and no protection bypass. Agent review must not be described as personal owner approval (`docs/PRD_ROOT.md` §5.3.1) [accepted requirement].
- This replaced "never self-merge" (D-8), which the 2026-07-28 tandem review had found in procedural conflict with an umbrella delegation (tandem comparison §07 HINGE-2).

---

## 4. Supplier and engine history

| When | Supplier / decision | What it provided | Problems / why it changed |
|---|---|---|---|
| 2026-06-13 | Claude Agent SDK / Anthropic, the "first concrete adapter"; SCA-APP-001, D-APP-18 key-aware default (`projects/chirality-app-dev/docs/CONTRACT.md` line 212; `DIRECTIVE.md` line 117) | Model/tool loop, file tools, bash, permission modes, hooks, MCP, transcripts, subagents, compaction. K-SDK-1 isolated shipped builds from ambient Claude settings (`CONTRACT.md` line 69) | Strategy was "provider-adapter generality", with Chirality as a layer "over provider harness mechanics", not feature parity (`docs/PLAN.md` line 67). The v3 release-plan review reported that Anthropic does not allow third-party products to offer claude.ai login, so Claude would stay on API keys (`plans/chirality_app_v3_release_plan_review_2026-08-22.html` line 145, F-08) [agent inference: a recorded review finding; I did not re-verify the external source] |
| 2026-07-22 | D-GOV-20: shared runtime plus a pilot with Pi (0.80.10, later 0.82.0) over a local oMLX server as a read-only Agent 2 | Local inference with rules for model residency (at most one resident model, no automatic switching or fallback) | By 2026-08-01, "the promoted runtime turn-engine factory has no caller" (`plans/chirality_five_investigations_2026-08-01.html` T3). Residency requirements were retired in D-GOV-43 item 13, and local models were redirected to Codex model providers |
| 2026-08-22 | v3 RC plan: Codex App Server as an opt-in "Preview" delegated-harness adapter with ChatGPT login; D-GOV-35 native delegation | Native multi-agent delegation, account login, rate limits | Built behind a hard outer envelope, a patched supplier and admission machinery (`plans/chirality_app_v3_release_execution_plan_final_2026-08-22.html` §§4–5) |
| ~2026-09-10 | Codex made the sole MVP engine (`projects/chirality-app-dev/execution/_Coordination/AgentRuns/CODEX_MVP_PACKAGING_20260910/amendment-candidate.md`; Runtime `NOTICE_2026-09-10_ROOT_APP_METHOD_AND_ENGINE_POLICY.md`) | — | The rationale in these records is only "owner direction … sole Codex MVP engine"; I found no fuller comparison |
| 2026-09-11 | D-GOV-43: stock App Server, no patches | Codex "in their full glory" [owner feedback, `D-GOV-43.proposed.md` line 63] | See the findings below |
| 2026-09-12 | A2 supplement: keep Runtime as a service the App owns, so later Chirality apps can embed it; stock Codex inside | Same service for the App and future sidecars | S-1…S-8 PASS; v3.0.0 released |

**D-GOV-43 findings** (`D-GOV-43.proposed.md` lines 88–140) [executed check (record) in proposal findings]:
1. The daemon accepted only 8 notification methods, so tool work produced no stream bytes and a 30-second idle timeout killed turns.
2. A configuration veto excluded the user's MCP servers, skills and instructions.
3. The Codex 0.149.0 supplier was patched with private protocol extensions and had to be re-patched on every upstream release.
4. A generic multi-engine vocabulary "retained from the Claude SDK and Pi eras" left Codex items with nothing to render them.
5. A three-hop transport re-derived state that Codex already persists.

T3 Code (MIT) was cited as a reference Electron client. Pi was noted as a complete harness that "informs UX only."

**Owner perspective** (`…/APP_V3_CODEX_HOST_REPLATFORM_20260912/PERSPECTIVE.md`) [owner feedback]: "Codex should provide the agent capabilities. Chirality contributes the conversational interface, four role relationships, reusable workflows, inspectable plans and useful access to artifacts." The accumulated control machinery "restricted useful Codex behavior and made ordinary work fragile." The same note asks that no requirements be recreated "under new names."

**Why A2 over an in-process host.** "A Node in-process library cannot be embedded in a Tauri main process," so the reusable unit is "the service composition plus a protocol-first Chirality layer." Under A2 the flagship App "exercises the embedding path every day" (`TOPOLOGY_COMPARISON.md` §8) [agent inference recorded, then owner-accepted in the A2 supplement].

**Open supplier question.** The review record left open whether OpenAI permits a commercial third-party app to embed Codex with ChatGPT login ("written answer from OpenAI", review line 327) [unrealised intention: open question].

---

## 5. Candidate exemplars and lessons for v4 — all [agent inference]

**1. Build around a stock harness through its published protocol.** The strongest lesson in the corpus is the move from a patched, filtered, configuration-vetoed Codex to a stock one, and the owner's statement of why. Useful exemplars:
- the effective home that shares configuration and keeps authentication separate;
- "every server request receives an answer";
- execution kept separate from observation;
- Runtime owning the turn.

**2. Application-embedded capability has a worked contract.** `APPLICATION_TOOLS.md` and `APPLICATION_CONSUMER_GUIDE.md` together define a clean split: Runtime owns transport and lifecycle; the application owns domain validation, live state, human Apply and receipts. Supporting points:
- The SWBPIPE design (inspect, preview, submit proposal, status; no agent Apply; a basis token checked again at acceptance) is a concrete template for letting agents see shared objects and state while humans keep decision rights.
- Supplier constraints shape it: immutable catalogs per thread (Codex 0.154.0) and tool inheritance by descendants that has not been qualified.
- A future supplier evaluation could test those constraints directly.

**3. Domain-engine profiles are a ready vocabulary for embedding.** The `_DomainEngines` profile schema maps closely onto "meaningful objects, operations, results" in an engineering app: authoritative versus readable artifacts, protected paths, deterministic tools with confirmation flags, a proposal lifecycle, and claims agents must not make. It predates the dynamic-tool API and is not yet connected to it.

**4. The old PEC sidecar is a precedent for agent identity in an app.** It acted as an owner-provisioned non-admin "agent person" through the app's own RBAC API, with human-only acts removed from its dispatch table.

**5. Coordinating many agents.**
- PEC's modes ladder, two trust tiers, SHA-based staleness and graceful absence are coherent design exemplars. They remain mostly unimplemented after two months.
- A2 removed the single observable daemon, so presence across applications now has no source (P-β deferral).
- Task Management evidence shows that ledgers nobody is obliged to read do not close. Items close when adopted into each loop's entry instruments.
- D-GOV-12 supplies ruled orchestration safety rules: disjoint writes, work graphs recorded before dispatch, relays that preserve claim status.

**6. What stayed Chirality's and what the supplier provides.**
- **Supplier (Codex):** agent loop, tools, sandbox and approvals, native delegation topology, thread persistence and compaction, credential custody, skill discovery, MCP.
- **Chirality:** role and product guidance as additive developer instructions, workflows as files plus a catalog, the thread index and metadata, evidence recording, UI presentation of the full stream, answering every request, transport for application tools, and the human-gate doctrine.
- **Application:** domain truth, validation, commits and Apply.

**7. Governance weight is itself a finding.**
- Five-investigations T4: about 1,022 governance artifacts and 30.1% of changed lines in one sampled window, with the net verdict "not decidable" for lack of telemetry.
- The tandem review found code-first/carrier-later sequencing.
- D-GOV-43 made simplification "a primary deliverable."

A v4 PRD may want to decide how much of this machinery it carries forward. That is a flagged inference, not a recommendation.

**8. Identity across seams is a recurring gap.** Five-investigations names "the unnamed-identity pattern": runtime compatibility epoch, parity instrument, tolerance policy and ruling authentication all lack a ruled definition of "the same." The dynamic-tool basis (generation + revision + hash) is one working instance of such a definition.

---

## 6. Gaps and limits

- **Nothing was executed.** All test and PASS statements are records, not my observation. The test count (~42 files) is approximate; the 401-test and 312-test figures are quoted from run logs.
- **Mixed status labels.** The Runtime PRD bytes are daemon-era and must be read through PRD_REVISION.md. Several Root clauses are marked PROSPECTIVE, and `AGENT_WORKFLOW_RUNTIME.md` and `WORKFLOW_COMPONENT_STANDARD.md` call themselves prospective. "Accepted" status is layered, and I did not reconcile every clause.
- **Codex-only rationale.** I found no document that compares suppliers when Codex was made the sole MVP engine (~2026-09-10). The recorded reasons are owner direction, capability ("full glory") and account-login considerations from the review. The OpenAI licensing and embedding question is recorded as open.
- **Not deeply read:**
  - `docs/PRD_ROOT.md` §§9.1, 9.3 and 10;
  - PEC PRD v2.3 successor candidate and SCA-005 amendment actions;
  - the full `FEED_MODEL_V2_DESIGN_NOTE.md` (~7.7k words);
  - Task Management federation plan;
  - `_DomainEngines/_DECISIONS/*`;
  - the Runtime `SCA005_*` and historical `RUNTIME_*` run records;
  - `AGENT_*` role bodies beyond the registry;
  - `docs/DIRECTIVE.md`, `CONTRACT.md`, `SPEC.md` (only §14 read) and `TYPES.md`.
- **Not verified:**
  - whether the App currently calls any application-tool route (the grep found no App source consumer; the only non-Runtime hits are Piping coordination notes and CI logs);
  - live Piping CLI progress;
  - whether `engine-pi-omlx` builds in hosted CI at this basis.
- **External claims** (Anthropic login policy, T3 Code behavior, Codex protocol counts) are as recorded in repository documents and were not re-checked against current external sources.
- **Other suppliers.** No harness was investigated for suitability beyond what these records contain: Claude Agent SDK, Pi, Codex App Server and T3 Code as a reference client.

Key files:
- `projects/chirality-runtime/{README.md, docs/APPLICATION_TOOLS.md, docs/APPLICATION_CONSUMER_GUIDE.md}`
- `projects/chirality-runtime/packages/daemon/src/{app-owned-composition.ts, codex-supervisor.ts, application-tools.ts}`
- `docs/governance_harness/_DECISIONS/D-GOV-43_*.md`
- `projects/chirality-app-dev/execution/_Coordination/AgentRuns/APP_V3_CODEX_HOST_REPLATFORM_20260912/{PERSPECTIVE.md, TOPOLOGY_COMPARISON.md, RUN_LOG.md}`
- `projects/pec/{README.md, docs/PRD.md, docs/STATUS.md}`
- `_DomainEngines/profiles/open_pipe_stress.yaml`
- `docs/{PRD_ROOT.md, AGENT_WORKFLOW_RUNTIME.md, WORKFLOW_COMPONENT_STANDARD.md}`
