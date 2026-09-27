# Chirality App v3 (3.0.1): reverse-engineering report

**Basis.** Read-only inspection at `main@2b0572fe0`. The published fallback is v3.0.1: desktop source `485051eac`, published 2026-09-20T03:29:16Z (`gh release view v3.0.1 -R sgttomas/chirality-app`). v3.0.0 used source `6f41f93e7` and was published 2026-09-13T05:08:54Z. I did not run the App or any tests. I sampled records and did not read all of them.

**Path keys, all relative to REPO_ROOT:**
- APP = `projects/chirality-app-dev`
- FE = `APP/frontend`
- RT = `projects/chirality-runtime/packages`
- RUNS = `APP/execution/_Coordination/AgentRuns`
- RP = `RUNS/APP_V3_CODEX_HOST_REPLATFORM_20260912`
- TC = `RUNS/APP_V3_TRIAL_COMPLETION_20260910`
- UJ = `RUNS/APP_V3_USER_JOURNEYS_20260912`
- DGOV43P = `docs/governance_harness/_PROPOSALS/D-GOV-43_2026-09-11_codex_host_replatform/D-GOV-43.proposed.md`
- D128 = `APP/execution/_Reconciliation/DeliverableConcordance/RUN_D128_CONCORDANCE_2026-09-21_1614Z`
- DONE = `D128/R0_DONE_DECLARATION/V3_DONE_DECLARATION_CANDIDATE.md`

---

## 1. Product definition as of v3

### Two definitions coexist, and they disagree

**The governing app-dev documents describe the older product.** They present a "governed desktop harness" organized around packages, deliverables, `_STATUS.md` lifecycle files, `Dependencies.csv`, a provider-neutral engine port, and Claude SDK as the first adapter.
- Sources: `APP/docs/DIRECTIVE.md` §1 L29–48; `APP/docs/PRD.md` §2 L31–131, §6.1 L283–337.
- Standing: [described design].
- The PRD carries only a prepended "Current Codex-only MVP release basis" (L13–21). It tells readers to treat the Claude and Pi descriptions as "compatibility history".
- A later record found that 1,044 of 3,217 deliverable claims were STALE_SPECIFICATION (`D128/R3/R3_SUMMARY.md` §2a) [executed check (record path)].

**The shipped v3 is defined by later instruments.** These are D-GOV-43 (DGOV43P items 1–14), the owner-approved intent note (`RP/PERSPECTIVE.md` L11–39), the README (`APP/README.md` L3–15) and the release notes.

### Purpose

- Release notes: "Plan your work, iterate. Chirality helps you direct professional knowledge work with Codex, review its results, and turn useful plans into reusable workflows" (v3.0.0 release notes) [accepted requirement, as published].
- Intent note: "Codex should provide the agent capabilities. Chirality contributes the conversational interface, four role relationships, reusable workflows, inspectable plans and useful access to artifacts" (`RP/PERSPECTIVE.md` L15) [owner/user feedback, owner-approved text].
- Measure of done: plan → execute → save → reuse → iterate, stated as checks S-1 to S-8 (DGOV43P item 12, L277–299) [accepted requirement].

### Users and personas

- The PRD lists eight personas: Professional Operator, Project Orchestrator, Specialist Contributor, Governance Maintainer, Release Operator, Harness Runtime Maintainer, and two "Future Domain" roles (`APP/docs/PRD.md` §4 L195–231) [described design].
- v3 practice targets a professional knowledge worker who signs in with a ChatGPT account. It works with Help Human, Helps Humans or Working Items (`APP/README.md` L5–7; `TC/R14_FUNCTIONAL_FINDINGS.md` "direct-entry menu contains precisely Help Human/Helps Humans/Working Items") [implemented; executed check].
- The v3 journey campaign used fictional office-type work: meeting actions, venue selection, supplier comparison and similar. No engineering design work was tested (`UJ/JOURNEY_RESULTS.md` L15–26) [executed check].
- The professional-responsibility model is carried into the shipped guidance. AI output is a draft, and humans hold decision rights (`APP/docs/DIRECTIVE.md` §3 L187–215; `APP/instructions/AGENTS.md` L105–111, "Represent human acceptance only when it has actually occurred") [described design; implemented as supplied guidance].

### Principal activities

- Converse with a role.
- Use native Plan Mode, including revise, execute, and turn into a workflow.
- Create, register, select and reuse workflows.
- Answer questions and approvals, steer a running turn, and stop it.
- Follow delegated agents.
- Attach and open files.
- Continue chats after restart.
- Update the App.

Sources: v3.0.0 release notes; `UJ/OWNER_TRIAL_NOTES.md` L38–66 [implemented; executed check].

### Explicitly excluded or deferred in v3

All from DONE §2 OOS-01–16, citing the plan, D-GOV-43 and UJ records [accepted requirement unless noted]:
- Multi-engine parity. Claude subscription OAuth, and the Claude engine itself.
- A second platform. The release is macOS arm64 only (G0 B1).
- A Chirality subagent scheduler or child allowlist.
- Apple App Sandbox.
- Local models and residency (DGOV43P item 13).
- A workflow execution engine or a separate workflow editor (`RP/PERSPECTIVE.md` L31).
- Import of chats from the daemon era.
- A shared-authentication opt-in.
- CLI, PEC and Piping integration as MVP prerequisites.
- Skills browsing UI. The owner decided on 2026-09-13 to hide it (agent-recorded in `UJ/PLAN.md`).
- Retired machinery: the LaunchAgent, admission, the closed event vocabulary, and the per-chat model freeze.

Earlier deferrals that still stand as history:
- The editable document write path (D-APP-26).
- The task-management surface (D-APP-29).
- Domain-engine integration (`APP/docs/PRD.md` §6.4 L367–382).

Source: `plans/chirality_app_dev_maturity_survey_2026-08-01.html` §2 [described design].

---

## 2. Connected user activities in 3.0.1

**Legend:**
- **C** = source path exists.
- **T** = unit or integration tests exist.
- **N** = native or real-Codex execution is recorded.
- **D** = described only.

| Activity | Start → action → result | Persistence | Interruption and recovery | Standing |
|---|---|---|---|---|
| Install and update | DMG → drag to Applications. The App checks at startup and every 6 h; the badge shows; install is manual (`FE/electron/app-update.ts`; `UJ/OWNER_TRIAL_NOTES.md` L40–42) | Edited product guidance survives updates (L106–109) | An install over v2 is not recorded (DONE Q-09) | C, T (`__tests__/electron/app-update.test.ts`), N startup check |
| Sign in and out | Account menu → Codex `account/login/start` in the browser → Ready | `auth.json` lives only in the App's effective Codex home. Config, skills and sessions are symlinked from `~/.codex`, excluding `auth*` and the models cache (`RT/daemon/src/codex-effective-home.ts` L5–12, L34–36) | Signing out leaves other Codex clients untouched: S-8 PASS from source (`RP/RUN_LOG.md` 15:50Z). The packaged S-8 is not recorded (DONE Q-04) | C, T, N |
| Open a project | Folder picker, which starts at home → "Use this folder". The Runtime creates a minimal `chirality.project.json` if absent and never overwrites (`CODEX_MVP_PRODUCT_20260910/WORK_RECORD.md` "ordinary folders must work"; `RT/core/src/bootstrap-project.ts`) | Manifest in the folder. Registration in user data | The binding is restored after relaunch (repair in `APP_V3_DIRECT_TRIAL_20260910/TRIAL_FINDINGS.md` L79–83). Concurrent renderers produced one recoverable binding error (`UJ/JOURNEY_RESULTS.md` L92–94) | C, T, N |
| Select a role | Picker offers the three direct-entry roles. TASK is reached only by delegation | Stored per chat | A role change once silently reset the model; repaired (`TC/R14_FUNCTIONAL_FINDINGS.md`) | C, T, N |
| Converse | Composer → `turn/start`. Model and reasoning are chosen per turn from the account catalog (`RT/core/src/delegated-runtime.ts` L146–157) | Codex thread store, plus App `session.json`/`events.jsonl` under user-data `runtime/projects/<id>/sessions` (`RT/core/src/session-store.ts` L1113) | Closing the window does not stop the turn. On reload the App reads `turn/state` and re-attaches (`FE/src/app/api/harness/turn/route.ts` L7–12; `RP/RUN_LOG.md` 15:50Z window-disconnect PASS) | C, T, N |
| Stop and steer | Stop → `/api/harness/interrupt`. Steer → `turn/steer` with a receipt | Receipts are turn-scoped (3.0.1 fix) | Stopped turns show a Stopped chip. The same chat continues (`UJ/JOURNEY_RESULTS.md` J08). A sandboxed child process may outlive an interrupt (`RP/RUN_LOG.md` 15:40Z) | C, T, N |
| Plan Mode | Mode picker → `thread/settings/update collaborationMode` (`RT/daemon/src/codex-supervisor.ts` L232). The plan panel shows the revision; Revise, Execute and "Turn into workflow" are available (`FE/src/components/shell/native-plan-panel.tsx` L126–128) | Revision history and per-revision execution records (`APP_V3_UI_REFINEMENT_20260912/RUN_LOG.md` L22) | Plan and execution were restored across a renderer reload (same log L39) | C, T, N (S-1; J04, J07) |
| Select and reuse a workflow | Library → inspect → select. Mid-chat selection is possible (3.0.1). Resolved text is supplied as developer instructions | Selection is part of the session's recorded instruction basis (`RT/core/src/instruction-basis-store.ts`) | Method replacement after an instruction-basis change failed on Day 1; fixed by CAS against the current session (`RUNS/APP_DAY1_MAINTENANCE/STATUS.md`) | C, T, N (S-4; J05, J07 over three cycles) |
| Create and register a workflow | Chat, following the `create-workflow` method → draft at `.chirality/workflow-drafts/<name>/WORKFLOW.md` → Workflows panel shows the draft for review and feedback → Register. Registration is exclusive, checks for staleness, and never overwrites (`FE/src/components/woven-dialogue/workflow-draft-review.tsx` L74; PR #786) | `.chirality/workflows` in the project or home directory. The catalog refreshes automatically | A stale review is refused | C, T, controlled browser test only for the 3.0.1 draft flow. Saving directly to the catalog was N in 3.0.0 (S-3, J05) |
| Questions and approvals | Codex server requests become request cards: command, file change, permissions, user input, elicitation. "Accept for session" appears when Codex offers it (`FE/src/components/shell/request-card.tsx` L36). Unknown requests get a JSON-RPC error (`RT/daemon/src/codex-supervisor.ts` L40–45, L707–710) | Answers are recorded in the event stream. Other chats show a needs-answer indicator | Deny, then renew: J09 PASS (`UJ/JOURNEY_RESULTS.md` L25). Not every approval variant was exercised live (L88–91) | C, T, N |
| Delegation | Codex native subagents. The Agents tab shows observed children | Replay shows the child's thread identity | Child completion is "unknown" unless observed (`UJ/JOURNEY_RESULTS.md` L95–96) | C, T, N (S-5, J02) |
| Attachments and files | A native picker copies outside files into `.chirality/attachment-inputs`. The viewer refreshes when a file changes | Copies are retained. Removing a chip does not reclaim the copy (`UJ/OWNER_TRIAL_NOTES.md` L119–120) | Same-chat recovery after an attachment failure (`UJ/JOURNEY_RESULTS.md` L73–80) | C, T, N |
| History and replay | Sidebar grouped by folder. Rename, archive and restore. Read-only replay lens; "Continue this chat" | Chat index is persisted in the renderer (`wovenWorkspace v1`) on a stable per-user-data port (`APP_V3_UI_REFINEMENT_20260912/RUN_LOG.md` L22; `APP_V3_DIRECT_TRIAL_20260910/TRIAL_FINDINGS.md` L55–59) | Relaunch uses `thread/resume` (`codex-supervisor.ts` L191). S-6 PASS from source; packaged S-6 not recorded | C, T, N |
| Inspect or edit instructions | Settings → Open or Restore default for the App-owned product `AGENTS.md`, keeping a backup. Each turn has a "recorded instruction basis" | User-data copy. The instruction digest is recorded (`RT/core/src/delegated-engine-adapter.ts` L249) | An instruction change is adopted only at an idle unload followed by a cold `thread/resume`. Until then the state is `INSTRUCTION_ADOPTION_PENDING` (`APP_V3_UI_REFINEMENT_20260912/PRODUCT_GUIDANCE_AND_UPDATES.md` L26–40) | C, T, N |
| Notices | Needs-answer indicators, Plan badge, update badge | Plan read state is held in the shell (3.0.1) | Stale notices were fixed in 3.0.1 | C, T, D for native polling latency |

Not supported in v3:
- Deliverable lifecycle UI. The `/pipeline` and `/workbench` routes still exist, but the right panel's tabs are Files, Plan, Workflows, Agents and Activity (`FE/src/components/woven-dialogue/right-panel.tsx` L20) [implemented (code path)].
- End-to-end automation. CI boots a stub-engine Runtime and never runs live Codex (`.github/workflows/harness-premerge.yml` L94, L195–214) [test defined].
- The agent-driven journeys acted as the real end-to-end check [executed check].

---

## 3. Architecture

### 3.1 Topology (A2) [implemented (code path)]

1. Electron main (`FE/electron/main.ts`, 1,143 lines) serves Next.js pages and 40 API routes.
2. It launches one Runtime service child: `chirality-runtime-service daemon --config`, with bounded restart and deliberate stop (`FE/electron/runtime-service-host.ts` L1–15).
3. The service speaks authenticated HTTP/1.1 over a private Unix socket with per-launch tokens (Root `docs/CONTRACT.md` K-RUNTIME-1, K-CONTROL-1, L168–169).
4. The service owns a stock `codex app-server` child (`@openai/codex` pinned at 0.154.0 in `FE/package.json`) over stdio JSON-RPC (`RT/daemon/src/codex-app-server-client.ts`, `codex-supervisor.ts`).

- Browser SSE carries the Runtime's turn subscription. Cancelling the stream only unsubscribes (`turn/route.ts` L7–12).
- Code sizes:
  - Runtime daemon 3,963 lines; core 8,642; contracts 5,402.
  - Frontend source 52,606 lines; frontend tests 55,876 lines across 222 test files. Measured by `wc`.

### 3.2 Who owns what

| Supplied by Codex, used as-is | Owned by Chirality App and Runtime |
|---|---|
| Agent loop, built-in tools (shell, file edits, web search, MCP), sandbox and approval enforcement | Process lifecycle: App → service → Codex child (K-RUNTIME-1) |
| Native Plan Mode via the experimental `collaborationMode` (DGOV43P finding 6, L128–132) | Effective home overlay with private `auth.json` |
| Native subagents, thread persistence, resume, compaction, model catalog, rate limits | Instruction composition: product guidance + active role + catalog pointers + selected workflow, sent as `developerInstructions` (`delegated-engine-adapter.ts` L37–43; `codex-supervisor.ts` L191, L219). Native role config files for children |
| Account login and credential custody | Workflow catalog (project → user → bundled), selection, drafts and registration (`RT/core/src/method-catalog.ts`) |
| Skills discovery; project `AGENTS.md` discovery | Chat index and session/event store (user data); instruction-basis history |
| Dynamic-tool call protocol (`item/tool/call`) | UI projections: plan panel, request cards, Activity, Agents. Answering every server request |
| | Attachment import, file viewer, update checks. Application dynamic-tool registry (after 3.0.1; §4) |

### 3.3 Evidence recording

- Standing: [implemented] for user-data session records; [agent inference] for the project-contained part.
- The Runtime appends `events.jsonl` and records the instruction digest and model attribution per turn (`delegated-engine-adapter.ts` L205–249), following K-ROLE-2 and K-STORE-2 (`docs/CONTRACT.md` L171–173).
- D-GOV-43 item 9 also calls for evidence in project checkouts "where the governing workflow requires it". The only checkout-writing coordinator is `RT/core/src/agent1-run-coordinator.ts` L926, and it is not referenced from `RT/daemon/src`. Project-contained AgentRun recording therefore looks unwired under A2.
- Codex events are still mapped into the older v1 `HarnessEvent`/`UIEvent` vocabulary through item summaries (`delegated-engine-adapter.ts` L51–77) [implemented]. The "faithful transport" is therefore pass-through plus translation, not native rendering.

### 3.4 Skills, workflows and roles

- Workflows are file packages that are source-qualified and discovered from project, user and bundled locations (Root `AGENTS.md` "Skills and workflows") [accepted requirement; implemented].
- Codex discovers skills natively through the shared home. The Runtime catalog still restricts App skill selection to bundled skills (`method-catalog.ts` L487), and the Skills UI is hidden [implemented].
- The four roles are text contracts (`APP/instructions/AGENTS.md` L11–37). Role delivery to children uses content-addressed native role files and fresh contexts, because "a full-history fork does not by itself establish another role" (`PRODUCT_GUIDANCE_AND_UPDATES.md` L28–33) [implemented; N for S-5].
- The Type 2 non-delegation rule is asserted in instructions only (`CODEX_MVP_PRODUCT_20260910/WORK_RECORD.md` L5) [described design].

### 3.5 Why Codex: alternatives, criteria, rejections, open questions

**Engine sequence** [described design unless noted]:
1. Claude Agent SDK was the first adapter and the key-aware default (`APP/docs/PRD.md` §2 L55–60; D-APP-18). The Claude path allowed API keys only: Chirality "does not advertise, design around, or promise Claude subscription login" without written Anthropic approval (v3 plan final §7.5, text L411–413, `plans/chirality_app_v3_release_execution_plan_final_2026-08-22.html`).
2. Pi 0.80.10 with local oMLX was a bounded, read-only second engine (SCA-APP-002 / D-APP-72; PRD L61–65).
3. A custom runtime was kept as an explicit fallback (PRD L127–129).
4. The 2026-08-22 plan made Codex App Server an opt-in "Preview" inside a hard Chirality envelope, with the native engines kept (plan §3.1–3.2).
5. By 2026-09-10 the MVP was "Codex-only". The only record is agent-written: "The owner's current instruction … limits the MVP to Codex" (`CODEX_MVP_PRODUCT_20260910/WORK_RECORD.md` L3; `APP/execution/_Coordination/NOTICE_2026-09-10_ROOT_APP_METHOD_AND_ENGINE_POLICY.md`). No ruling that first set the rule was found (DONE Q-06) [agent-recorded owner direction].

- [agent inference] Plausible criteria from the records: a supported consumer account login (ChatGPT via App Server) versus Claude API keys only, and native delegation, plan mode and a published protocol in one stock server. No record weighs Codex against Claude explicitly.

**The re-platform (2026-09-11):**
- HELP_HUMAN offered two routes: an in-place seam repair of the daemon, or re-hosting stock Codex (`plans/steers/chirality_app_v3_codex_host_replatform_direction_2026-09-11.md` L13–20).
- The owner chose to re-platform: "I need to have the Codex agents in their full glory … There should not be any limits on tool use" and "This Chirality App was built with a lot of governance oversight resulting in some overly restrictive or naively limited views" (L26–43, L47–49) [owner/user feedback].
- Rejected, with reasons (DGOV43P findings 1–5, L88–114) [accepted requirement]:
  - an eight-method notification whitelist that quarantined tool items;
  - a configuration veto that excluded the user's MCP servers, skills and settings;
  - a privately patched 0.149.0 "supplier";
  - a vocabulary left over from the multi-engine era;
  - a transport of daemon → Unix socket → SSE → Next route with three timeouts and no keepalive.
- T3 Code (MIT, an Electron client of the same protocol) was the reference for the effective-home layout. Pi was ruled a complete harness rather than a Codex client, and "informs UX only" (finding 7, L133–139).

**Topology (2026-09-12)** (`RP/TOPOLOGY_COMPARISON.md`):
- **A1, keep the launchd daemon:** rejected. Its one benefit was not needed, and it caused the defect class, installer hold and PID ambiguity (§7, L229–232).
- **B, in-process host:** recommended first because it removed about 4,000 lines (§4, L157–184).
- **A2, App-owned child service:** selected after the owner added that "the same agents and agent server is intended to be imbedded in subsequent applications … like the SWBPIPE" (direction steer L89–93). The reason: a Node library cannot embed in Tauri, so the reusable unit is a spawnable service plus a protocol-first Chirality layer (§8, L284–302).
- Work common to every topology (C1–C6) was judged to be 70–80% of the effort (§2, L103–104) [agent inference within the record].

**Open after the choice:**
- U1–U7 (§6, L207–225): effort, supervisor wiring, request round-trips, credential backend, dropping Seatbelt, PEC socket, reconnection.
- Local models as Codex model providers (item 13).
- A shared-authentication opt-in (item 3).
- The stability of experimental fields (`collaborationMode`).
- Tauri sidecar distribution: "there is no Tauri sidecar distribution yet" (`projects/chirality-runtime/docs/APPLICATION_CONSUMER_GUIDE.md` §"What can be reused").
- Evidence: [described design].

---

## 4. Post-3.0.1 unreleased work (485051eac..2b0572fe0)

- 83 commits without merges touch `APP/` (`git log --no-merges`).
- The diff adds 2,711 files and about 307k lines under `APP/execution`. Under `FE` it is 26 files, +200/−533 lines (`git diff --stat`) [executed check].
- Why: on 2026-09-19 the owner said, "App has already been published as `v3.0.0` and I'm not doing further development work until a reconciliation phase" (`RUNS/HELP-HUMAN-APP-20260919-LOOP-WORKGRAPH/OWNER_DIRECTION.md`) [owner/user feedback].

The work falls into seven groups:

1. **Whole-corpus deliverable concordance (D-APP-128–131, RUN_D128, about 45 commits, 2026-09-21/22).**
   - Compared 54 deliverables with the implementation: 3,568 claim keys and 107 unmapped capabilities (`D128/HANDOFF_STATE.md`).
   - Final census: 695 ALIGNED, 1,044 STALE_SPECIFICATION, 411 PARTIALLY_IMPLEMENTED, 179 IMPLEMENTED_DIFFERENTLY, 159 AUTHORITY_CONFLICT, 374 NOT_AUDITABLE (`D128/R3/R3_SUMMARY.md` §2a).
   - Built a "v3 done" candidate with 20 criteria, 16 exclusions and 13 owner questions (DONE).
   - Standing: [executed check].
2. **Retiring "Remaining" items into governing scope and task management; loop-instruction changes.** A work graph replaced workplans, and there is now "one central loop receipt" (commits `3f27a4a15`, `6900f7984`, `1fafb0842`). This follows the owner's "separation" direction (OWNER_DIRECTION) [implemented, records].
3. **Harness-contract facade retired (D-APP-118, `9f83708ae`).** This removed `FE/packages/harness-contract` and its checks, about 533 lines [implemented].
4. **Replay boundary repair (`3867a632f`, `ee3786f56`, `d82568bc1`).** The replay lens hides instruction evidence from other sessions and keeps the transcript when instructions conflict (`FE/src/lib/woven-dialogue/selected-session-replay.ts`, +80 test lines) [implemented; test defined]. This is the only product-behaviour change.
5. **CI burden.** Hosted PR checks were scoped to changed inputs (`60ab76e6d`, `5e3cb6623`) [implemented].
6. **Runtime, outside APP, relevant to embedding.**
   - Application-owned dynamic tools (`da95ec194`, `cb08dbe2f`, 2026-09-19). The owner said: "we need to work on those dynamic tools now. They will be application specific. SWBPIPE is the first app to receive tools".
   - The design is proposal-only: first tools are `inspect_selection`, `preview_operations`, `submit_proposal` and `get_proposal_status`, with "no agent-facing Apply" (Runtime `APPLICATION_DYNAMIC_TOOLS_20260920/PLAN.md`; `projects/chirality-runtime/docs/APPLICATION_TOOLS.md`) [implemented; test defined, 401 Runtime tests; no live consumer].
   - A consumer guide (`625b82e9b`) says SWBPIPE's first path is "a development Codex session using the Piping JSON CLI and private bridge", which does not need the embedded Runtime [described design].
7. **v4 preparation.** The `reverse-engineer-software` workflow and successor product bases (`2a546559c`, `cc0207059`) [implemented, records].

---

## 5. Feedback and lessons

### Sources

- No user-filed issues exist on either repository. `gh issue list --state all` returns an empty list for both. The three `chirality-app` items are README PRs [executed check (gh)].
- All feedback therefore comes from the owner, agent-run native trials and synthetic journeys.

### Defects and friction

**Before the re-platform (2026-09-10/12):**
- First-run sign-in was blocked by:
  - a missing hosted-bootstrap token;
  - binding to a fixed development project;
  - loss of drafts on restart because the renderer port changed;
  - "Complete App account host proof is required".
  - Source: `APP_V3_DIRECT_TRIAL_20260910/TRIAL_FINDINGS.md` L5–18, L55–59, L99–105.
- "User challenged full signing on each iteration" (L113) [owner/user feedback].
- The R14 trial found (`TC/R14_FUNCTIONAL_FINDINGS.md`) [executed check]:
  - plans rendered as JSON;
  - routine metadata clutter;
  - Settings panels for Anthropic and oMLX in a Codex-only App;
  - assistant links that did nothing;
  - replay that dropped every user message;
  - interrupts that ended in `ENGINE_UNAVAILABLE`.
- R16: the chat failed after restart and long chats could not be scrolled (`TC/R16_FUNCTIONAL_FINDINGS.md` L44–54).
- R17-F2: any turn that stayed silent for more than about 30 s was interrupted. Plan execution and save-as-workflow succeeded only as "short, read-free turns" (`TC/R17_FUNCTIONAL_FINDINGS.md` L148–151, L153–189) [executed check].
- About 26 packaging stages were run during trial completion (`TC/L_STAGE16…26_PACKAGING` plus earlier stages).
- The owner's reading: "tool activity was discarded, a quiet stream timed out … Repeated packaging and qualification procedures then made repairs expensive" (`RP/PERSPECTIVE.md` L17) [owner/user feedback].

**UI direction:**
- Twelve, then nineteen, owner refinement items (`APP_V3_UI_REFINEMENT_20260912/RUN_LOG.md` L3–8, L22). Among them:
  - separate message types;
  - single-action sign-in;
  - compact activity;
  - a Plan tab;
  - per-chat folders;
  - turn phases and outcome states;
  - preserving user work through updates.
- The owner first withdrew cross-folder chat from the MVP, then had it finished (L27).
- Owner principles (`RP/PERSPECTIVE.md` L27–29) [owner/user feedback]:
  - "Keep primary surfaces concise, with deeper information available through deliberate inspection."
  - "Workflows deserve prominence."

**Day 1 of real use (2026-09-13/14, PR #786):**
- Stale question and steering notices.
- A persistent Plan badge and an Update button that overflowed its label.
- Workflow inspection that did not visibly open.
- Method replacement failing after the instruction basis changed.
- A request to create workflows through a reviewable draft.
- Suspected redundant child-folder permission prompts. No containment defect was found.
- An Excel repair warning traced to mismatched table-column metadata, which led to new guidance.
- Sources: PR #786 body; `RUNS/APP_DAY1_MAINTENANCE/PLAN.md`, `STATUS.md` [owner/user feedback; executed check].

**Carried-forward limits:**
- Child completion stays unknown after the primary turn ends.
- Staged attachment copies are not reclaimed.
- One moderate PostCSS advisory remains.
- Focus contrast needs follow-up.
- Sources: `UJ/OWNER_TRIAL_NOTES.md` L111–128 [described design].

### What worked

- After D-GOV-43 was ruled (2026-09-11), S-1 to S-8 and the disconnect check passed from source on 2026-09-12. Independent review passed at `388de6973`, and v3.0.0 was published on 2026-09-13 (`RP/RUN_LOG.md` L145–220; DONE DONE-12/13/17) [executed check].
  - [agent inference] Removing mechanism turned weeks of blocked trials into about two days to release.
- Eight fictional journeys passed independent artifact review. A saved workflow was reused and refined over three cycles. Denied and renewed approvals, Stop and resume, and steering all worked with real Codex (`UJ/JOURNEY_RESULTS.md` L15–26) [executed check].
- Authentication separation left the ChatGPT desktop client's Codex state untouched (`RP/RUN_LOG.md` 15:50Z) [executed check].

### Method overhead [executed check (counts); agent inference (valuation)]

- `APP/execution`: 15,848 files, 350 MB, 138 AgentRun folders.
- 132 D-APP decisions and 44 D-GOV decisions.
- 53 of 54 deliverables still `IN_PROGRESS` and 1 `OPEN`, with none ever issued. This matches the 2026-08-01 survey's "zero of 53 deliverables has ever left IN_PROGRESS".
- `loop/LOOP_RECEIPTS.md` is 62,436 words.
- 4,267 commits have touched `APP/` since 2026-05-18.
- The 2026-08-01 survey said: "reliance ran ahead of assurance"; "no e2e layer of any kind exists"; "the PRD body contradicts its own §17" (`plans/chirality_app_dev_maturity_survey_2026-08-01.html` §§3–5).
- The owner said: "I think I need to just steer the model through phase transitions" (OWNER_DIRECTION, `phase_steering`) [owner/user feedback].
- Important decisions ended up outside the loop's receipts. There were no App receipts from 2026-09-07 to 2026-09-19, covering D-GOV-43 and the release (DONE Q-05). The retained human acts (trial acceptance, the system-prompt discussion) have no closing record (Q-03) [executed check (record path)].

---

## 6. Candidate exemplars for v4

All value judgements in this section are [agent inference]. Evidence standings are marked in each entry.

**E1. Plan → execute → turn into workflow → reuse.**
- Activity: shaping and repeating work.
- How it works: native Plan Mode revisions with history; Execute prepares a request for the exact revision; execution records per revision; "Turn into workflow" (`native-plan-panel.tsx` L126–128).
- Evidence: S-1, S-3 and S-4, and J07's three cycles [executed check].
- Limits: synthetic users only. It relies on the experimental `collaborationMode`.
- Depends on: a harness with native plans. Workflows kept as files.
- If removed: the product thesis, "plan your work, iterate", is lost.

**E2. Conversational workflow authoring with draft review and explicit registration.**
- How it works: `create-workflow` method → draft → inspect and feedback in chat → exclusive, non-overwriting registration → catalog refresh. Identity is source-qualified: project, user, bundled.
- Evidence: PR #786 [test defined; controlled browser check]. Native end-to-end: [executed check] for 3.0.0 saving only.
- Depends on: the file-based workflow format (`WORKFLOW.md`).
- If removed: workflows silently become executable without human review, or authors lose conversational authoring.

**E3. Separating execution, observation, interruption and shutdown.**
- How it works: a disconnect is loss of observation only; Stop is an explicit interrupt; re-attach through `turn/state`; turn phases (Preparing, Working, Waiting, Reconnecting, Stopping); outcomes (Completed, Stopped, Failed, **Outcome unknown**) (`RP/TOPOLOGY_COMPARISON.md` §9 L326–334; UI refinement RUN_LOG L22).
- Evidence: window-reload and SIGSTOP checks [executed check].
- Value: directly serves shared understanding of state and recovery.
- If removed: the R17-F2 defect class returns.

**E4. Answer every agent request, and never imply approval.**
- How it works: request cards for approvals, questions and elicitations, with a session scope only when offered. Unknown requests get an explicit error (DGOV43P item 2 L156–171; `codex-supervisor.ts` L707–710).
- Evidence: J09 [executed check].
- Limits: not every variant was tried live.
- If removed: a harness can hang silently, or approval can be implied without being given.

**E5. Host a stock harness over its published protocol; treat upstream drift as a dependency update.**
- How it works: pinned `@openai/codex`, no patches, and the user's own approval and sandbox policy (DGOV43P items 1 and 4).
- Evidence: the change delivered the release, where the patched path had blocked it (§5) [executed check].
- Limits: a single supplier. Instruction changes and dynamic tools are bound by supplier behaviour (E10, R5).
- Relevance: this is the most direct evidence on "build from capable existing harnesses".

**E6. Separate authentication while sharing configuration.**
- How it works: an overlay home that symlinks the user's config, skills, MCP and sessions but keeps `auth.json` private (`codex-effective-home.ts`).
- Evidence: S-8 [executed check].
- Relevance to embedding: several host apps could share one user's harness configuration.

**E7. Application-owned dynamic tools with proposal-only domain actions.**
- How it works: the host app registers tools before the first turn. The Runtime routes calls. The app keeps domain validation, basis tokens, human review and Apply (`APPLICATION_TOOLS.md`; Runtime PLAN).
- Standing: [implemented; test defined; no live consumer].
- Prior art: PEC proposal-only MCP tools, where acceptance and apply are "deliberately absent" (maturity survey §2).
- Value: probably the closest existing mechanism to v4's primary target, where agents operate on meaningful objects without taking over human decision rights.
- Limits: `dynamicTools` is accepted on `thread/start` only, so catalog changes require a new conversation. Tauri distribution does not exist yet.

**E8. Truthful projection of agent activity.**
- How it works: the Agents and Activity views show only observed events. Missing results stay unknown; "the UI does not fabricate either" (`UJ/JOURNEY_RESULTS.md` L67–69). Actual model attribution and instruction digest are recorded per turn (K-ROLE-2).
- Standing: [implemented; executed check].
- If removed: completion and responsibility get overstated.

**E9. Editable, inspectable product guidance with four text-defined roles.**
- How it works: a shipped default, a user-data copy that survives updates, Restore with backup, and additive supply that keeps Codex's base instructions (`PRODUCT_GUIDANCE_AND_UPDATES.md` L10–27; `APP/instructions/AGENTS.md`).
- Standing: [implemented; executed check].
- Limits: role limits are enforced by instructions only.

**E10. Professional-responsibility posture as supplied guidance.**
- How it works: outputs are drafts; human acceptance is represented only when it actually happened; format-aware validation of generated documents (`APP/instructions/AGENTS.md` L105–118; `APP/docs/DIRECTIVE.md` §3).
- Standing: [described design; implemented as text].
- Relevance: engineering-design hosts such as SWBPIPE are the high-stakes case this was written for.

**E11. Contained attachment import and live file views.**
- How it works: outside files are copied into the project without widening agent access; open previews refresh when the file changes.
- Standing: [implemented; executed check].

**E12. Real-work evaluation campaign.**
- How it works: agent-simulated professional journeys run against the production path, with artifacts reviewed by an independent evaluator (`UJ/PLAN.md`; `UJ/JOURNEY_RESULTS.md`).
- Evidence: it found real defects (native-child interpretation, attachment wiring) where source tests had passed [executed check].
- Limits: synthetic users are not customers (L9–12).

**E13. D-APP-87 / D-APP-91: a standalone Desktop plus per-domain targets, with six interface slots.**
- The slots: NavigationWorkspace, StructuredInformation, Workflow, DecisionGate, TypedAgentReview, UiAgentConformance (`APP/execution/_Coordination/_DECISIONS/D-APP-91_RULING_…_2026-08-03.md`).
- D-APP-87 adopted "domain-specific applications as the primary delivery vehicle for the agents".
- Standing: [unrealised intention]; planning baseline only.
- Why it matters: the closest earlier statement of v4's primary expression, and still untested.

### Historical mechanism or compromise worth reconsidering

- **R1. Next.js server inside Electron, loopback HTTP/SSE, a Unix socket with tokens, and 40 route files, all for one consumer.**
  - A2 kept about 2,600 lines of transport for future embedders (`TOPOLOGY_COMPARISON.md` §4 A2).
  - One project per Next server lifetime forced cross-folder chats into the renderer, and the chat index lives in origin-scoped localStorage, which needed a stable port (UI RUN_LOG L22; direct trial L55–59) [implemented].
- **R2. The translation layer to v1 `HarnessEvent`/`UIEvent` remains** (`delegated-engine-adapter.ts`) [implemented].
- **R3. Dead multi-engine code.** About 6,000 lines of Anthropic, Claude and Pi managers and the turn engine sit in `FE/src/lib/harness`, reachable only from tests. The Anthropic and Pi SDKs are dev dependencies. The `engine-claude` and `engine-pi-omlx` packages remain (import grep; `FE/package.json`) [implemented; agent inference on reachability].
- **R4. Instruction changes need an idle unload and a cold resume, and dynamic tools are fixed at `thread/start`.** These are supplier constraints the design works around (E9, E7).
- **R5. The App governs itself as a deliverable decomposition.** 54 deliverables were never issued, 32% of claims are stale, and the evidence volume is large (§5). The project documents (PRD, SPEC, CONTRACT) still describe a provider-neutral Claude-first harness (`APP/docs/PRD.md` L37–131) [executed check].
- **R6. Governance-first enforcement was retired.** Admission, the hard envelope, the closed schema and the per-chat freeze were all removed (DONE OOS-14). Keep the lesson rather than the mechanism.
- **R7. The Woven Dialogue compatibility shell and the legacy portal, pipeline and workbench routes remain** (`FE/src/app/page.tsx`) [implemented].
- **R8. Reliance on the experimental `collaborationMode` field** (DGOV43P finding 6).

---

## 7. Gaps

- **Real-user feedback does not exist in records.** There are no issues, and usage metrics were not found.
- **The origin and rationale of the Codex sole-engine rule** has no ruling record (DONE Q-06). Why Codex over Claude is inferred.
- **Packaged S-6 and S-8, the owner's trial acceptance, the system-prompt discussion, an install over v2→v3, and the SBOM and notices obligations** have no recorded outcomes (DONE Q-03, Q-04, Q-08, Q-09).
- **Whether the App writes project-contained AgentRun evidence** under A2 is inferred from grep only (§3.3).
- **Not verified directly:**
  - I executed no tests or builds; "test defined" means the files exist, not that they pass at `2b0572fe0`. CI results cited are from records.
  - The journey artifacts and the independent reviews (`RP/INDEPENDENT_REVIEW.md`, `UJ/returns/`) were not read in full.
  - I sampled from about 16k execution files. The R4 decision book and packets, the R5/R6 applications, and the ruling records A1–A15 and R10–R18 were skimmed or not read.
- **SWBPIPE's integration state** (CLI-first bridge, adoption of dynamic tools) is described only from the Runtime side. The Piping loop owns it.
- **Model identifiers** in the records (gpt-5.6-*, gpt-6-astra, Fable 5.1) are reproduced as recorded, not verified.
