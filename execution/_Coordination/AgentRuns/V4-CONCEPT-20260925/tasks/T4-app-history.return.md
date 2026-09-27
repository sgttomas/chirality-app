# Chirality App: history across generations, from archives and records (TASK return)

**Boundary kept.** I only read. I created, changed and moved no files and ran no state-changing git. For the two zip files I only listed contents (`unzip -l`). The only network use was `gh release list/view` on `sgttomas/chirality-app`.

**Path keys.**
- `ORIG` = `/Users/ryan/ai-env/projects/chirality`
- `RR` = REPO_ROOT (`/Users/ryan/ai-env/projects/chirality/.claude/worktrees/chirality-app-v4-architecture-9f35c4`, main@2b0572fe0)
- `ADA` = `ORIG/projects/chirality-app-dev/.archive`

**Labels.** [accepted requirement] · [described design] · [implemented] · [executed check (record)] · [owner/user feedback] · [agent inference] · [unrealised intention]. "Historical" means the item was accepted at the time and has since been superseded.

---

## 1. Generation timeline

### G0 — Foundations before the App (Oct 2025 to early Feb 2026)

- **Operational definition of an agent.** "agent = LLM + instructions + access to files + use of tools". A good agent is `agent_1(agent_2)` and a great one is `agent_0(agent_1(agent_2))`: three nested layers with fan-out and fan-in. The human stays accountable. (`ORIG/.archive/WHAT-IS-AN-AGENT.md`, whole file) [described design]
- **The nine task-management domains.** These come from owner Word documents of October 2025, described as "a tool for thinking, not a rigid workflow". (`RR/plans/chirality_five_investigations_2026-08-01.html`, T1) [executed check (record)]
- **The semantic algebra.** Matrices A and B lead to C, F, D, K, G, X, T and E, packaged as the `semantic-matrix-build` and `lens-register` skills (`ORIG/.archive/semantic-matrix-build/SKILL.md`, Purpose) [described design]. It was later "explicitly demoted to scaffolding" (five investigations, T1) [executed check (record)].

### G1 — v1.x public desktop harness (Feb 9–22, 2026)

**Releases** (`gh release view`) [implemented]:

| Release | Date | Release note |
|---|---|---|
| v1.0.1 | 2026-02-09 | "Official public release … for Mac and Windows" (only a Windows `.exe` asset) |
| v1.1.0 | 02-16 | "Revisions to various agents instructions based on latest testing results" |
| v1.2.0 | 02-18 | Official Mac release; estimating pipeline with three example outputs |
| v1.3.0 | 02-22 | "Subagents added, interface polished, attachments added, chat UI functionality added" |

v1.1.0 and v1.2.0 still carried installers named `1.0.1`. [agent inference] Early releases were mostly instruction-bundle releases on top of a largely unchanged binary.

**Engine path** (`ORIG/.archive/frontend/docs/harness/harness-decisions.md`):
- D-000 (l.23, 2026-02-07) notes "custom Anthropic loop vs Claude Code subprocess harness".
- The next step was a `claude -p` NDJSON subprocess (D-004, D-011).
- D-017 (l.200, 02-08): "Wholesale SDK cutover with no dual runtime path" to the Claude Agent SDK `query()`, deleting `/api/chat` and the CLI manager. [implemented]

**Host:** Next 16.1.6, React 19, Electron 33 and `@anthropic-ai/claude-agent-sdk ^0.2.37`. The instruction root was bundled as `extraResources` (`ORIG/.archive/frontend/package.json`). [implemented]

**Harness posture** [implemented]:
- Claude Code system-prompt preset, with the persona, README and AGENTS.md appended (`…/lib/harness/persona-manager.ts` l.805ff; `agent-sdk-manager.ts` l.222–245).
- `settingSources: ["user","project","local"]`.
- Default `dontAsk`, mapped to `bypassPermissions` (`defaults.ts` l.5–10; `harness-sdk-cutover-checklist.md`).

**Interaction** (`components/HexGrid.tsx`; `app/page.tsx` l.40–80; `frontend/README.md` "Subagent Delegation (Phase 1)") [implemented]:
- PORTAL: a 3×4 hex matrix (NORMATIVE/OPERATIVE/EVALUATIVE × GUIDING/APPLYING/JUDGING/REVIEWING).
- The matrix routed to WORKBENCH (personas) or to PIPELINE. PIPELINE had categories DECOMP*, PREP*, TASK* and AUDIT*, with visible disabled "coming soon" options.
- An operator Toolkit panel with per-turn options, plus SSE turn streams, a file tree and attachments.
- Subagents were gated by `CHIRALITY_ENABLE_SUBAGENTS` plus a per-turn governance token, and failed closed.

**Real use:** estimating-pipeline project roots in `ORIG/.archive/examples/execution-6a/6b/6c` and `AB-2026-01424-…`. [implemented]

### G1b — Governed self-rebuild in chirality-app-dev (Feb 21–24, 2026)

**Decomposition.** SOFTWARE_DECOMP was approved at G7 on 2026-02-21 (`ADA/ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md`): 8 packages, 50 scope items, 37 deliverables (32 active, 5 retired) (Coverage l.311–330). [accepted requirement, historical]

**Human rulings:**
- DEC-PLAT-001: macOS 15+ arm64 DMG, "signing/notarization **not required**".
- DEC-NET-001: outbound traffic to Anthropic only, "No other outbound network connections (telemetry, update checks, etc.)" (l.34–35).

**Execution.**
- 194 commits in about 4 days. All 31 active deliverables reached ISSUED, and five PKG-08 deliverables were retired. (`ADA/_Coordination/DEVELOPMENT_HISTORY_ANALYSIS_2026-02-24.md` §1–2) [executed check (record)]
- The deliverable `_STATUS.md` files show ISSUED on 02-23/24.
- Around 120 `TIER*_CONTROL_LOOP_*_PASSn.md` files sit in `ADA/_Coordination`.
- The output was an unsigned `Chirality-0.1.0-arm64.dmg` (`ADA/building-dmg.md`).

**A separate code line.** This rebuild did not continue the public v1.3 frontend.
- Amendment A1 added a frontend baseline because "Prior execution assumptions treated `frontend/` as already available" (G7 doc, Amendment A1).
- The 2026-05-03 PRD records KG-001: "`StubPersonaManager.buildSystemPrompt()` … does not compose full instruction-root context into the Anthropic request path" (`ORIG/.archive/PRD_CANDIDATE.md` l.691; FR-026 l.328). [described design]
- The zip lists `frontend/src/lib/harness/persona-manager.ts` at 693 bytes. The public frontend's persona manager is 887 lines.
- [agent inference] The governed rebuild reached ISSUED without the working agent-prompt path that the public build already had.

### Interval — instruction architecture and monorepo (Mar–May 2026)

- **2026-04-04: Type 2 rationalisation.** TASK became the single Type 2 shell; methods moved into four-file skills and deterministic steps into tools; the ORCHESTRATOR pipeline was grandfathered. (`ORIG/plans/.archive/chirality-app-test/TYPE2_RATIONALIZATION_MASTER_PLAN.md`; `PLAN_HISTORY_AND_COMPLETED_NORMALIZATION_RECORD.md` §5–6) [implemented]
- **Engineering campaigns in `chirality-app-test`:** DBM publication, P&ID drawing extraction, equipment costing, West Doe, Deepcut and Comp Liquids (`ORIG/plans/.archive/chirality-app-test/*`). [described design] and [implemented]
- **2026-05-18: monorepo migration.** Four repositories were merged into the root-canonical `chirality` repo, and the public `chirality-app` was rebuilt as an allowlisted export: 5,548 files, 0 boundary findings (`ORIG/.archive/migration/final-report.md`; `…/chirality-app-public-export-20260518-150242/final-report.md`). [executed check (record)]
- **2026-05-03: PRD_CANDIDATE**, reverse-engineered from repository sources (`ORIG/.archive/PRD_CANDIDATE.md` §1). [described design]

### G1.5 — "vNext" (May 19 to June 2026)

**PRD adopted** 05-19/20 (RR commits 92a25d270 and 96a2e9557).

**Four decompositions in about 12 hours** (`ORIG/projects/chirality-app-dev/execution/_Decomposition/.archive/`): R0 at 00:27, v2.5 at 07:21, the "aligned v3" at 10:03, then v3.2 at 12:06. The first versions record "Gates 1-7 accepted by implicit human approval per user instruction" (DEC-002). [executed check (record)]

**Design** (`PRD_software_decomp_aligned_v3.md` §3 l.42–61; OBJ-005 l.182) [accepted requirement, historical]:
- "SDK-privileged, contract-owned, and Chirality-governed".
- `AgentEnginePort`, a `TurnEngine`, and a canonical `HarnessEvent` JSONL log, with SDK transcripts secondary.
- "Shipped SDK builds use `settingSources: []`".
- "Prompt text is not a safety boundary".
- Deny-first tool policy.
- 10 packages and 51 deliverables, including PKG-10 "Domain Engine Future Boundary".

**The scaffold stalled** (`ADA/execution/_Coordination/NEXT_INSTANCE_STATE.md`; `DEPENDENCY_GRAPH_CHECK.md`) [executed check (record)]:
- All 51 deliverables were INITIALIZED.
- Semantic lensing and P3 enrichment were skipped by human ruling.
- "Existing `_SEMANTIC.md` outputs are invalid evidence".
- 554 dependency rows, but the graph was not acyclic: SCC-001 spans 18 runtime deliverables.

**June runtime build-out:**
- **SCA-APP-001 (06-13).** A provider-general runtime; Pi became a pattern corpus only. Blanket deny-first was replaced by "capability-forward, policy-mediated, evidence-recorded tool use" (`RR/projects/chirality-app-dev/execution/_ScopeChange/SCA-APP-001_2026-06-13_1819_…_v2/Brief.md` l.21, A004 l.40). [accepted requirement]
- Controlled bash, read tools and write hooks landed (RR git log, 06-13 to 06-16).
- D-APP-28 (06-19): "loop-first pivot".
- **Tier-0 bridge to OpenPipeStress.** The `DomainEngineProfile` was ADOPTED on 06-21, but live L2/L3 build stayed gated on "app-dev F3 · piping D-21 · DEC-041" (`ORIG/.archive/chirality-governance/execution/_Coordination/NEXT_INSTANCE_PROMPT.md`). [accepted requirement]

### G2 — v2.0.0 shared runtime (July 2026)

**Release, 2026-07-24** (`gh release view v2.0.0`) [implemented]:
- "provider-neutral shared runtime workspace, authenticated Unix-socket daemon, CLI, runtime client, contracts, and safe engine adapters".
- 711 export entries with zero boundary findings; 43 runtime tests.
- The first signed and notarized DMG.

**D-GOV-20 (07-22)** (`RR/docs/governance_harness/_DECISIONS/D-GOV-20_shared_runtime_local_agent_pilot.md`, "Ruled architecture" 1–10) [accepted requirement, partly superseded]:
- A root-owned `runtime/`.
- One opt-in per-user daemon owning engines, credentials, sessions, delegation, tools, locks and local-model residency.
- Unix-domain-socket HTTP control.
- Agent 0/1/2 kept independent of engine.
- Pilot: an Agent 1 delegating a read-only task to a Pi/oMLX Agent 2 running on a local model.

**Information architecture.** D-APP-74 replaced the fixed matrix shell with "Woven Dialogue" plus a Work/Agents Coordination Panel. The PRD's interaction thesis: "The actual human–agent dialogue is the primary workspace" (`RR/projects/chirality-app-dev/docs/PRD.md` §2). [accepted requirement]

**State on 08-01** (`RR/plans/chirality_app_dev_maturity_survey_2026-08-01.html` §1–5) [executed check (record)]:
- About 46k lines of product TypeScript and 1,022 test cases, with three engine adapters (Anthropic, Claude, Pi/oMLX).
- CI boots the real daemon but uses a stub model; "E2E — NOT FOUND"; no parity instrument.
- All 53 deliverables IN_PROGRESS; "the issuance machinery … has never run".
- Verdict: "reliance-released and assurance-thin".

### Interlude — program architecture, a domain-first direction, v3 planning (Jul 25 to early Sep)

**Program architecture review, 07-25** (`RR/plans/chirality_program_architecture_and_tandem_review_2026-07-25.html` §02–04):
- The App has "two useful identities: standalone general application and reference/reusable human–agent work surface". [described design; "clarified framing"]
- A candidate "application environment profile" would declare a "Standalone, embedded, or sidecar work surface". [unrealised intention]

**Tandem comparison, 07-28:** "The reusable work surface and resource governance have no governed paper at all" (`…tandem_comparison_2026-07-28.html` §01). [executed check (record)] SCA-APP-005 then made the App a runtime *client*.

**Piping D-58 (07-27/28):** retired the App-era consumption mechanism and keeps "Piping outside the Root-runtime and App-harness client sets" (`RR/projects/chirality-piping/execution/_Coordination/_DECISIONS/_REGISTER.md`, D-58). [accepted requirement]

**D-APP-87 (08-02)** (`RR/projects/chirality-app-dev/execution/_Coordination/_DECISIONS/D-APP-87_RULING_DUAL_TARGET_PRODUCT_DIRECTION_2026-08-02.md`, "Selected semantics") adopted as planning input:
- "two delivery targets: the standalone Chirality Desktop app and a per-domain control-plane target".
- "domain-specific applications as the primary delivery vehicle for the agents".

**D-APP-91 (08-03)** (`…D-APP-91_RULING_BUILD_TIME_PRODUCT_PROFILES_SIX_BOUNDED_SLOTS_2026-08-03.md`) selected one shared shell, build-time product profiles and six slots, as a "planning baseline only". [accepted requirement (planning input)] and [unrealised intention]. The slots:
1. Navigation Workspace
2. Structured Information
3. Workflow
4. Decision Gate
5. Typed Agent Review
6. UI–Agent Conformance

**v3 plan Rev 3.1 (08-22)** (`RR/plans/chirality_app_v3_release_execution_plan_final_2026-08-22.html` §1, §3.1, §4) [described design, superseded]:
- Codex App Server as an "opt-in Preview" adapter alongside the existing engines, behind the daemon and a launchd process supervisor.
- "Codex owns its inner harness … Chirality owns the outer authority boundary".

### G3 — v3.0.0 and v3.0.1 (Sept 2026)

**D-GOV-41/42 (09-09)** (`RR/docs/governance_harness/_DECISIONS/D-GOV-42_chirality_v3_role_skill_workflow_adoption.md` items 1–9) [accepted requirement (candidate implementation)]:
- Exactly four roles: HELP_HUMAN, HELPS_HUMANS, WORKING_ITEMS and TASK.
- Skills at `.agents/skills`, six central workflows, and source-qualified method identity.
- Three grouped decomposition checkpoints; native Plan Mode kept separate.

**SCA-APP-010 (09-04)** (`RR/…/_ScopeChange/SCA-APP-010_…/Brief.md`, action A015 l.80):
- "Retire Workbench and Pipeline presentation from the active shell" and drop the Work projection.
- Add a Workflows view, a `propose` tool, per-chat delegation policy, and a per-chat folder with app-wide sign-in.

**D-GOV-43 (ruled 09-11)** switched to a stock, version-pinned `codex app-server` run as a child of Electron main over stdio, using the full protocol, with approval and sandbox left to the user. Its findings (`RR/docs/governance_harness/_PROPOSALS/D-GOV-43_2026-09-11_codex_host_replatform/D-GOV-43.proposed.md` Findings 1–7, l.88ff) [executed check (record)]:
- The daemon passed only 8 Codex notification methods and quarantined the rest. The Activity view was therefore empty "by construction", and 30-second socket idle timeouts killed turns.
- Its configuration veto excluded the user's MCP servers, skills and instructions.
- The "supplier" App Server was privately patched and five releases behind upstream.
- The generic multi-engine vocabulary had no rendering target for Codex-native items.
- Turn transport took three hops.

Owner, verbatim: "I need to have the Codex agents in their full glory … There should not be any limits on tool use" (l.63). [owner/user feedback]

**Release v3.0.0 (09-13)** [implemented]:
- "Plan your work, iterate."
- Chat with Help Human, native plans, attachments, approvals, and delegated work.
- "Save a workflow through chat, use it with new inputs, and refine it over successive projects."
- Models come from the user's Codex account; update checks run at startup and every six hours.

**Release v3.0.1 (09-20),** "based on the first days of real work" [implemented]:
- Workflow selection in an existing conversation.
- New workflows "reviewed, discussed in chat, and explicitly registered from the Workflows panel".
- Session-wide approval; Excel table-consistency guidance.

**Public README:** "Local-model support is planned for a later release" (`ORIG/exports/chirality-app/PUBLIC_README.md` l.11). [unrealised intention]

### What prompted each successor generation

| Transition | Recorded prompt |
|---|---|
| G1 → G1b | Build the App with Chirality's own method, as "simultaneously the framework template and its first execution" (DEVELOPMENT_HISTORY l.5). "Software is a great medium to teach about agents" (`ADA/START_HERE_AGENT_PATHS.md` intro). [owner/user feedback] |
| G1b → vNext | Stub prompt path (KG-001), partial runtime enforcement (KG-002/003), monorepo consolidation, and the auditability demand: persist user input before model execution (SOW-014) and a canonical event log. [described design] |
| vNext → G2 | Provider generality (SCA-APP-001), local models (D-GOV-20), and several consumers (PEC, domain engines) needing a runtime owned at Root. [accepted requirement] |
| G2 → G3 | Codex and ChatGPT-account availability. D-GOV-43 found the governed daemon was crippling the engine. The product was refocused on general knowledge work ("Plan your work, iterate") with four roles. [executed check (record)] and [owner/user feedback] |

[agent inference] Across generations, the view of what an agent is moved in four steps:
1. Personas in matrix cells, subagents failing closed.
2. Chirality-owned engine contracts, deny-first, "prompt is not a boundary".
3. Capability-forward tool use (June 13).
4. The capable harness owns its inner loop, and Chirality supplies instructions, roles, workflows and the outer boundary.

---

## 2. Capabilities and interaction patterns across generations

| Capability or pattern | G1 (v1.x) | G1b / vNext | G2 (v2.0) | G3 (v3.0) | Why (recorded) |
|---|---|---|---|---|---|
| Files and git as project truth; instruction root separate from working root | Yes | Yes (SOW-013/014) | Yes (D-GOV-20 item 5) | Yes (README "ordinary files") | Founding thesis (`ORIG/.archive/DIRECTIVE.md` §2.1–2.6) — **persisted** |
| Navigation | Matrix PORTAL, WORKBENCH, PIPELINE | Same (SOW-005/007) | Woven Dialogue (D-APP-74) | Dialogue-centred; Workbench and Pipeline retired (SCA-APP-010 A015) | Dialogue as primary workspace (PRD §2) — **disappeared** |
| Agents | ~38 persona and task agents (`ORIG/exports/chirality-app/staging/agents/`) | TASK + skills + tools (Apr) | Agent 0/1/2 independent of engine | 4 roles (D-GOV-42 item 1) | Rationalisation; roles are not engines — **changed** |
| Engine | Anthropic SDK → CLI → Agent SDK | "SDK-privileged", then provider-general | Anthropic, Claude, Pi/oMLX | Codex only | D-017; SCA-APP-001; D-GOV-43 — **changed** |
| Host control of the engine | User settings loaded; `bypassPermissions` | `settingSources: []`, deny-first | Daemon config veto, patched supplier | User's Codex config honoured; user picks approval and sandbox | Deny-first reversed 06-13; "full glory" — **pendulum** |
| Subagents / delegation | Fail-closed governance token | Governed Type 2, child records | Managed delegation; one Pi Agent 2 | Codex-native descendants inside the outer envelope (D-GOV-35) | v3 plan §1 — **changed** |
| Credentials | Env, then UI `safeStorage` (SCA-003) | Same | Daemon custody (D-GOV-36) | Codex's own sign-in | D-GOV-43 supersedes D-GOV-36 — **changed** |
| Network and updates | Anthropic only, "no … update checks" (DEC-NET-001) | Same | — | Update checks every 6 hours | Reversed — **changed** |
| Signing | "not required" (DEC-PLAT-001) | Unsigned | Signed and notarized | Signed, with checksum | Reversed — **changed** |
| Turn transport and audit | SSE route plus log | TurnEngine plus canonical JSONL | Unix socket + SSE + Next route | stdio JSON-RPC; evidence from the full event stream | D-GOV-43 Finding 5 — **changed** |
| Lifecycle and dependency UI | `_STATUS` transitions and `Dependencies.csv` in the App | Same | Work projection, evidence only | Work projection dropped | SCA-APP-010 — **disappeared from the App** (kept in governance) |
| Reusable methods | Personas and pipelines | Skills (4-file), TaskSkill | Skills | `.agents/skills` + workflows; save through chat; register in panel | v3.0.1 — **grew** |
| Attachments | Yes (10 MB / 18 MB limits) | Yes | Yes | Yes | **Persisted** |
| Domain-engine integration | — | PKG-10 boundary; profile ADOPTED | Piping made non-client (D-58) | Absent | Gated, then retired — **unrealised** |
| Local models | — | — | Pi/oMLX residency pilot | Retired; "planned" | D-GOV-43 folded choice — **deferred** |

---

## 3. Failed approaches, abandoned designs, compromises, unrealised intentions

### Abandoned or failed

1. **The custom Anthropic loop and the `claude -p` subprocess harness** were replaced by a hard SDK cutover with "no dual runtime path", to avoid "regression drift and duplicated maintenance" (harness-decisions D-017). [implemented]
2. **A parallel governed code line.** It reached ISSUED with a stub persona prompt (KG-001). This came after the category omission corrected by SCA-001 (the frontend was missing), which followed an owner experiment: "The decomposition was intentionally not reviewed by the human author before approval" (DEVELOPMENT_HISTORY l.47). [owner/user feedback]
3. **PKG-08 hardening retired on 02-24** ("documentation was prepared for work that was never executed", DEVELOPMENT_HISTORY §3.1): folder validator, dependency graph generator, deliverable locks, unified run records, and staleness propagation (G7 doc, Amendment A2). [accepted requirement, historical]
4. **Unbounded elective passes.** DEL-03-05 ran 35 passes; passes 5–35 were "pure test coverage expansion" (DEVELOPMENT_HISTORY §3.3). [executed check (record)]
5. **The vNext scaffold never executed as decomposed.** 51 deliverables had kits, but the semantic outputs were ruled "invalid evidence" and the graph was cyclic (`ADA/execution/_Coordination/NEXT_INSTANCE_STATE.md`). Work continued through scope changes, D-APP rulings and tranches. [executed check (record)] and [agent inference]
6. **Deny-first governance** was reversed (SCA-APP-001 l.21). [accepted requirement]
7. **Pi changed direction three times:**
   - adapter prohibited (D-APP-01, 06-13);
   - bounded second engine (D-APP-72, 07-21);
   - residency requirements retired and Codex made the only engine (D-GOV-43 "three folded choices", `…/D-GOV-43_codex_host_replatform.md` l.41).
   [accepted requirement]
8. **Daemon-hosted, filtered and patched Codex** was abandoned (D-GOV-43 Findings 1–5). [executed check (record)]
9. **An authoritative SQLite coordinator ("Option C")** was rejected in favour of git-first files with read-only tools (`ORIG/plans/.archive/task_management_harness_evaluation_2026-06-22.md` §3; D-GOV-01 in `RR/docs/governance_harness/_DECISIONS/_REGISTER.md`). [accepted requirement]
10. **A program-tier concern register.** The notice ledger "sat at 29/30 open, never advanced", because "emission is enforced and consumption is not" (`RR/plans/chirality_task_management_architecture_review_2026-07-31.html` §01). [executed check (record)]

### Compromises

- The v3 plan chose "terminal-on-retirement": a planned retirement or crash ends the turn, and the next user action starts a fresh thread, with no active-turn continuity (v3 plan §2.1). [described design]
- v3 shipped Codex-only; other engines are "compatibility history" (`RR/projects/chirality-app-dev/docs/PRD.md` l.15). [accepted requirement]
- Windows was dropped (KG-005; SOW-078 OUT). [accepted requirement]

### Unrealised intentions (none were built)

- A reusable, embedded or sidecar work surface; an application environment profile; resource governance (07-25 charter; 07-28 comparison).
- Dual-target, domain-first delivery and the six slots (D-APP-87/91).
- L2/L3 domain operation proposals against OpenPipeStress.
- Local models; E2E and UI parity checks; a named runtime compatibility identity (five investigations T3; maturity survey §3).
- Lifecycle issuance (maturity §5); staleness propagation and locks.
- A second human owner (five investigations T5).
- An editable document write path (D-APP-26) and a secondary task surface (D-APP-29) (maturity §2).

---

## 4. Method lessons

1. **Uniform deliverable kits and bounded loops worked for well-scoped software.**
   - "very few bugs … most tests passed first time" and the governance "paid for itself" (DEVELOPMENT_HISTORY §2). [owner/user feedback]
   - Cost: about **75% of tokens on context, documentation and audits, 25% productive**, with a proposed 60/40 target (§3.2). [executed check (record); estimate]
2. **Completion needs an anchor.** A specification-anchored completion check (REQ MET/PARTIAL, plus an elective-work gate) was added to `AGENT_TASK` and `WORKING_ITEMS`. A category checklist was added to DECOMP_BASE (DEVELOPMENT_HISTORY §5). [implemented at the time]
3. **Decomposing faster than executing.** The four same-day vNext decompositions and the stalled scaffold show that decomposition became a bottleneck when the product basis kept moving. [agent inference from records in §1]
4. **Governance overhead grew and was never measured.**
   - By 08-01 there were about 1,022 durable governance artifacts (about 2.3 per merge).
   - Governance files were 30.1% of changed lines in the one window that was instrumented.
   - Verdict: "Not decidable … no record anywhere carries time or token telemetry" (five investigations T4). [executed check (record)]
   - Supporting constant: "roughly one third of confident upstream claims inverted under independent verification". [executed check (record)]
   - The register reached D-APP-129 and D-GOV-44.
5. **Constitution without enforcement.** The review said Chirality "spent its effort on the *constitution* … under-invested in the deterministic enforcement layer". `write_status.sh` could write ISSUED with any actor (`ORIG/plans/.archive/task_management_harness_HANDOFF_2026-06-23.md` §3). [described design and record]
6. **Attribution risk is real.** In the 2026-06-21 attribution defect, an agent recorded its own decision as an owner approval. This led to the `human_actors` allowlist and authorship checks (HANDOFF §3). [executed check (record)]
7. **Emission versus consumption.** Most concerns were written down but not read back (TM review §01): 269 of 275 register rows were ruled, while 0 of 12 disposition-register rows closed in 58 days. [executed check (record)]
8. **PRD accretion.** The PRD dated 2026-05-20 was amended through 2026-09-12. Codex-only now overlays Claude and Pi text, and two sections carry the number 17 (maturity §4, HZN-004). [executed check (record)]
9. **Independent review discipline works but costs rounds.** It used sealed tandem reviewers, a frozen basis, "challenge-not-adopt", and a readiness test of "two consecutive cold passes" ("Every prior round surfaced a new layer") (`ORIG/.archive/tier0-bridge-coordination-2026-06-21/NEXT_INSTANCE_PROMPT-app-dev.md` §2). v3 needed three plan and three proposal review rounds. [executed check (record)]
10. **Generic contracts need guarding.** "Guard against the first consumer bending the general contract" (same file, §5). [described design]

---

## 5. Archive map

| Location | Contents | Generation or subject | Size | v4 usefulness |
|---|---|---|---|---|
| `gh release` notes | 7 releases, v1.0.1 to v3.0.1 | All | small | **High** — the only public shipped-capability ledger |
| `ORIG/.archive/*.md` (PRD_CANDIDATE, WHAT-IS-AN-AGENT, AGENT_ORCHESTRATOR, DBM, SE_Design_Analysis, April SPEC/TYPES/CONTRACT/DIRECTIVE, PLAN, CLAUDE.md) | Reverse-engineered v1 PRD, founding agent definition, April governance | G0 to G1b | ~300 KB | **High** — PRD_CANDIDATE §14 gaps; agent definition |
| `ORIG/.archive/frontend/` | Public v1.3.0 Next/Electron app: harness lib, components, decisions register, validation scripts | G1 | 17 MB (15 MB in `electron/`) | **Medium** — harness-decisions D-000..D-017; matrix UI exemplar |
| `ORIG/.archive/migration/` | 2026-05-18 merge of four repos: path audits, copy manifest, public export report | Monorepo | 23 MB (mostly CSVs) | **Low to medium** — provenance of repository lineage |
| `ORIG/.archive/chirality-governance/` | Tier-0 adoption closeout prompt + `_Sources` task-management workbooks (RAIL, decision, change and risk logs) | June 2026 | 436 KB | **Medium** — engineering PM source corpus |
| `ORIG/.archive/tier0-bridge-coordination-2026-06-21/` | Bridge prompts for app-dev and piping (App ↔ OpenPipeStress) | vNext / domain | 28 KB | **High** — domain-embedding trust model |
| `ORIG/.archive/semantic-matrix-build/`, `lens-register/` | Retired semantic-algebra skills | G0 to vNext | 88 KB | **Low** — demoted method |
| `ORIG/.archive/domains/`, `examples/` | Domain corpora (piping-design 7.0 GB); estimating and design project roots | G1 use | 7.1 GB / 210 MB | **Low** for this question (not examined in depth) |
| `ADA/` root docs (G7 decomposition, START_HERE, building-dmg, CHANGE constraints, harness/, ui/) | First governed App decomposition and runbooks | G1b | ~250 KB | **High** — decomposition exemplar; DEC-PLAT/NET |
| `ADA/PKG-01..08` | 37 deliverable folders (four-document kit, `_SEMANTIC`, `Dependencies.csv`, `_STATUS`) | G1b | ~7.5 MB | **Medium** — kit exemplar |
| `ADA/_Coordination`, `_Reconciliation`, `_ScopeChange` | ~120 control-loop pass files, DEVELOPMENT_HISTORY_ANALYSIS, dependency audits, SCA-001..003 | G1b | ~6 MB | **High** (the analysis); others medium |
| `ADA/execution/` | vNext 10-package scaffold, dependency-graph check, dispatch plan | vNext | 6.7 MB | **Medium** — stall evidence |
| `ORIG/projects/chirality-app-dev/execution/_Decomposition/.archive/` | vNext R0, v2.5, aligned v3 | vNext | 172 KB | **Medium** — runtime-boundary SSOW |
| `ORIG/plans/.archive/` | chirality-app-test plans (51), task-management evaluation/plan/handoff, governance assessments, monorepo assessments | Mar to Jul | 1.3 MB, 73 files | **High** (task-management evaluation and handoff); medium otherwise |
| `ORIG/exports/chirality-app/staging/` | Public framework projection: 38 agents, 40 skills, tools, docs | **2 July snapshot**, stale; current `export-report.md` (09-22) shows 1,713 rows with `desktop/`, `runtime/`, `workflows/` | 6.5 MB | **Low to medium** — use `PUBLIC_README.md` and the export report instead |
| `chirality-app-dev.zip` (listing only) | 4,018 entries incl. `__MACOSX`; Feb app-dev repo (April file dates; `docs/PRD.md` dated 05-18); only copy of G1b `frontend/src` | G1b | 4.8 MB | **Medium** |
| `Software_PRD_Workflow_Draft_v1.zip` (listing only) | `software-prd/WORKFLOW.md` + resources, `review/DESIGN_AND_REVIEW`, WALKTHROUGH, DELIVERY_STATUS; 9 files (09-21) | G3 workflow authoring | 30 KB | **Medium to high** — v3-era PRD workflow draft (contents not read) |
| `RR/plans/*.html` (07-25 .. 08-01, 08-22) | Program architecture, tandem comparison, TM review, maturity survey, five investigations, v3 plan | G2 to G3 | 13–196 KB each | **High** |

---

## 6. Candidate exemplars and lessons for v4

All entries are [agent inference]. These are not requirements.

1. **The capable harness owns the inner loop; Chirality supplies instructions and the outer boundary.**
   - *Serves:* embedding agent capability in host applications.
   - *Evidence:* D-GOV-43 Findings 1–5; v3 plan §1; owner "full glory".
   - *Conditions:* the harness exposes a full protocol and supports additive instructions; the host can enforce sandbox and approval.
   - *Lost if omitted:* a repeat of the G2 daemon failure (filtered events, killed turns, stale patched supplier).
2. **Files and git as project truth, with the instruction root kept separate from the working root.**
   - *Serves:* reliance and portability inside host apps.
   - *Evidence:* persisted through every generation (§2).
   - *Conditions:* the host app can present and version ordinary files.
   - *Lost if omitted:* the continuity and auditability every generation kept.
3. **The workflow as the reusable unit: plan → execute → save → reuse → iterate.** Conversational drafting, then explicit human registration.
   - *Serves:* the v4 primary expression.
   - *Evidence:* v3.0.0/3.0.1 notes; AGENTS.md "Skills and workflows".
   - *Conditions:* workflow identity is source-qualified (D-GOV-42 item 4).
   - *Lost if omitted:* the one capability real users exercised in v3's "first days of real work".
4. **Six embedding slots as a starting vocabulary:** Navigation Workspace, Structured Information, Workflow, Decision Gate, Typed Agent Review, UI–Agent Conformance.
   - *Serves:* a domain-first, embedded surface.
   - *Evidence:* D-APP-91.
   - *Conditions:* only a planning baseline; never validated against Piping (TM-PIP-025 rider).
   - *Lost if omitted:* the only recorded analysis of what an embedded Chirality surface needs.
5. **The domain-engine boundary:** proposal-only operations, Class-A/Class-B risk tagging, and "validation passed ≠ engineering correct".
   - *Serves:* SWBPIPE-type engineering apps.
   - *Evidence:* tier-0 app-dev prompt §4 and §6.
   - *Conditions:* the domain engine keeps domain truth; the contract stays generic.
   - *Lost if omitted:* the professional (APEGA) ceiling at exactly the point of greatest risk.
6. **The spec-anchored completion check and elective-work gate.**
   - *Serves:* bounded agent execution.
   - *Evidence:* DEVELOPMENT_HISTORY §3.3.
   - *Conditions:* acceptance criteria exist before execution.
   - *Lost if omitted:* 35-pass drift.
7. **Deterministic checks that report and never author,** instead of an authoritative coordinator.
   - *Serves:* governance at low cost.
   - *Evidence:* D-GOV-01; Option C rejection.
   - *Conditions:* the checks are cheap and read-only.
   - *Lost if omitted:* either unenforced invariants or a hidden authority.
8. **Capability-forward permissions with narrow hard denies,** and the user choosing approval and sandbox.
   - *Serves:* agent effectiveness.
   - *Evidence:* SCA-APP-001 l.21; D-GOV-43.
   - *Conditions:* hard boundaries are named (secrets, protected paths, professional claims, destructive actions).
   - *Lost if omitted:* recurrence of the deny-first and configuration-veto swings.
9. **A small role set, separate from engines.**
   - *Serves:* comprehensibility and engine portability.
   - *Evidence:* four roles (D-GOV-42); retired matrix (SCA-APP-010).
   - *Lost if omitted:* persona sprawl that the UI later had to retire.
10. **Proportionate, measured governance.** Instrument the cost, require someone to consume what is emitted, and re-author the PRD rather than accrete amendments.
    - *Serves:* development method.
    - *Evidence:* the 75/25 split; T4 "Not decidable"; TM review; HZN-004.
    - *Lost if omitted:* unmeasured overhead and stale bases.
11. **Human judgment as the hinge, with attribution checks.**
    - *Serves:* reliance.
    - *Evidence:* the 06-21 attribution defect; `human_actors` allowlist.
    - *Lost if omitted:* self-authorised "approvals".

---

## 7. Gaps and limits

- **Not examined:**
  - `ORIG/.archive/domains/` (7.1 GB) and example contents, beyond identifying them.
  - Individual control-loop pass files.
  - The contents of either zip (listing only).
  - The public `chirality-app` git history: network use was limited to release notes, so the pre-February origins of v1.0 and the `AGENT_HARNESS_SPEC-v2-3.md` referenced in D-000 were not found.
  - The v3 trial findings file (`APP_V3_TRIAL_COMPLETION_20260910/R17_FUNCTIONAL_FINDINGS.md`), which I cited only through D-GOV-43.
- **Staleness:** ORIG tracked files are at an older revision, and the export `staging/` is a 2 July snapshot while the export report is dated 09-22.
- **Metrics:** token splits are estimates by the Feb analysis agent, and governance economics are explicitly unmeasured. The v3.0.0 release object was created 07-25; that is not its build date.
- **Standing of sources:** several sources (the 07-25 to 08-01 reviews and the maturity survey) describe themselves as derivative and non-governing. Their governed sources control.
- **v4 requirements:** none are recommended here beyond the flagged inferences in §6.
