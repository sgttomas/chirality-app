# SWBPIPE as the principal host for embedded agent/workflow capability: evidence report

**Basis.** This is a read-only investigation at `main@2b0572fe0`. I made no writes, builds, tests or network calls, and ran only read-only git commands. I also read the unmerged remote branch `origin/codex/piping-live-control-20260924` through `git show`/`git diff`. Its commits `1811d70a1` and `de52a7cfc` are **not** ancestors of `2b0572fe0`.

**Path abbreviations:**
- `P/` = `projects/chirality-piping/`
- `R/` = `projects/chirality-runtime/`
- `AD/` = `projects/chirality-app-dev/`
- `UI/` = `P/execution/_Coordination/AgentRuns/HELP-HUMAN-PIPING-20260918-UI-IMPLEMENTATION/instances/`
- `DP/` = `P/execution/_Coordination/AgentRuns/HELP-HUMAN-PIPING-20260916-UI-DESIGN-PROGRAM/`
- `LCB` = the live-control branch
- `ARCH` = ORIG_PIPING_ARCHIVE

**Standing labels:** [accepted requirement], [described design], [implemented (path)], [test defined], [executed check (record)], [owner feedback], [agent inference], [unrealised intention].

---

## 1. What SWBPIPE is and does

**Identity and positioning.**
- SWBPIPE (formerly OpenPipeStress, renamed by DEC-101 on 2026-09-18) is described as a "free and open-source, local-first, analysis-grade piping design engine". Its core is a 3D centerline/beam flexibility and stress solver, operating *earlier* in design than authenticated commercial tools [accepted requirement] (`P/docs/PRD.md` header lines 3–7, §1 lines 22–40).
- The governing distinction is "SWBPIPE computes and helps design. The external prover tool validates for reliance. The responsible engineer accepts." [accepted requirement] (PRD §1).
- The stance is "Open the mechanics; protect the standards; empower the engineer": the solver is code-neutral, and users supply code data (allowables, SIFs, load combinations) through private rule packs [accepted requirement] (`P/README.md` line 14; `P/docs/INTENT.md` lines 7–13, 105, 185).

**Users.** The PRD names six personas (PRD §9, lines 298–379):
- piping designer/layout engineer
- piping stress engineer
- owner-operator reviewer
- engineering-company administrator
- open-source contributor
- "Agent-Enhanced User", who needs "agent proposals as structured operations; visible diffs; user review gates; schema validation; undo/redo; audit trail" [accepted requirement].

The owner has since said the stress engineer is the user around whom the interface is built [owner feedback] (`DP/instances/ROOT/DIRECTION_DECISION_2026-09-17.md` §1.1, §2).

**Activities** [accepted requirement unless marked] (PRD §10 lines 381–438; INTENT lines 187–216; `P/docs/user_guide/index.md` §§6–11):
- Model building: nodes, pipes, bends, components, supports, materials and sections.
- Load cases and combinations, including self-weight, wind and seismic equivalent-static inputs.
- Solve.
- Result inspection.
- User rule checks.
- Model-state and analysis-run comparison.
- Handoff/export to an external prover.
- Report assembly.
- Review.

The designed iteration loop is: issue identified, then GUI edit or agent proposal, then structured operation, then validation and diff, then accept/reject, then new state and rerun (PRD §10.3). The external-prover loop exports to the prover, the user interprets its results outside SWBPIPE, edits the SWBPIPE model, reruns and compares (PRD §16.2, lines 1043–1059). The UI is organised as four stages — Model, Loads, Results, Review — with Table/Model/Both views [implemented (`P/apps/desktop/src/features/workspace/shellLayout.ts` lines 26–29)].

**Professional boundary.**
- Software may state "mechanics solved", "user-rule checked", diagnostics and hashes. It must never state or imply certification, sealing, approval, authentication or code compliance for reliance [accepted requirement] (PRD §4.3, §21.1–21.2; `P/docs/PROFESSIONAL_BOUNDARY.md` §§3–6).
- Agent output may be "Drafts, proposals, evidence summaries, checks, and open issues", never accepted work "without a human gate" (`PROFESSIONAL_BOUNDARY.md` §3 table, line 66).
- Six automatic statuses exist (`MODEL_INCOMPLETE` … `HUMAN_REVIEW_REQUIRED`). `HUMAN_APPROVED_FOR_PROJECT` / `ENGINEER_ACCEPTED` is reserved for an external, hash-bound human record that "invalidate[s] on bound-hash changes" (`P/docs/SPEC.md` §4.3; `PROFESSIONAL_BOUNDARY.md` §7; `P/docs/claims_registry.md` §2.1).
- No acceptance workflow exists in the MVP (PRD §21.3).
- The owner removed repeated boundary disclaimers from product surfaces: the boundary is carried by status display forms with authority domains plus the PRD §19.3 report notice [owner feedback / accepted requirement] (`claims_registry.md` BS-ACCEPT, lines 60–100; SOFTWARE_DECOMP DEC-100/DEC-107).
- There is a human-authored, content-hash-bound "Checked" row mark that lapses when the row changes. It is explicitly *not* an acceptance record [accepted requirement] (`P/execution/_Decomposition/SOFTWARE_DECOMP.md` DEC-104, line 705).

**Data/IP boundary.**
- The public repository ships only open mechanics and invented examples. Protected standards content is quarantined [accepted requirement] (`P/docs/IP_AND_DATA_BOUNDARY.md` §§2–5).
- Under D-T0-04/DEC-051 ("open residency"), an embedded agent worker may read the owner's private model and "Class-B inputs (allowables, SIFs, design basis)". Once the owner configures a provider (local, Anthropic, other), that data may be transmitted "with no further app-side guard" [accepted requirement] (`IP_AND_DATA_BOUNDARY.md` §6.1 line 103; `P/docs/CONTRACT.md` OPS-K-PRIV-1 line 41; SPEC §4.4).
- Telemetry stays off by default (OPS-K-PRIV-2).
- Agent-facing invariants: agents must not invent engineering values, must surface conflicts, and their outputs remain drafts until a human gate (`CONTRACT.md` OPS-K-AGENT-1..4, lines 47–50).
- DEC-043 bars any future embedded agent from presenting unreviewed OCR equation artifacts from the `domains/piping-design/` corpus as authoritative (`P/AGENTS.md` lines 23–30; SOFTWARE_DECOMP line 644).
- The product license is MIT (D-74, 2026-09-22) (`user_guide/index.md` lines 24–27).

**Maturity.**
- The project has about 1,982 commits touching `P/` since 2026-05-18 (git log).
- Desktop version is 0.1.0, targeting Apple Silicon macOS first (`P/apps/desktop/src-tauri/tauri.conf.json`; `UI/ROOT/CONTINUATION_2026-09-19_CODEX/MVP_PUBLISHING_DISCUSSION.md` line 40).
- The owner's stated progression is "a dependable design workbench, then an agent-controlled validation workbench, then a publishable bounded MVP" [owner feedback] (`UI/CONTINUATION_2026-09-24/OWNER_STEER.md` line 15).
- An owner-commissioned review raised 38 solver findings (M-01–M-38). Several are "serious live-path defect[s]": pressure, mechanisms, linear+nonlinear restraint loss, imposed displacement, SIF misuse and nonlinear combinations. They are under an active correctness programme [executed check (record): `UI/CONTINUATION_2026-09-24/SOLVER_FINDINGS_ASSESSMENT/ASSESSMENT.md` table; `CORRECTNESS_ACTIVATION.md` lines 5–13].
- Desktop comparison is only "single-run load-basis" comparison. Save replaces one project payload, so no immutable named states are kept. The Python two-state/two-run comparison engines are unwired [executed check (record): `UI/ROOT/CONTINUATION_2026-09-19_CODEX/_run_records/MVP_COMPARISON_CAPABILITY_RETURN.md`].
- PRD R7 (agent-assisted design and candidate generation) remains HELD under DEC-042. That ruling sanctions only harness-independent embedded-agent *preparation* (SOFTWARE_DECOMP line 643; PRD §24 R7 lines 1597–1613).

---

## 2. Inventory of shared objects, state, operations, results, errors and recovery

The exposure key used in the last column of each table:
- **H** = external headless CLI `openpipestress-runner`
- **T** = Tauri command, callable only from the app's own webview
- **L** = live-control CLI (LCB, unmerged)
- **S** = schema only
- **G** = GUI only
- **Py** = Python library, not wired to the desktop

**Objects** [implemented unless marked]

| Object | Evidence | Exposure |
|---|---|---|
| Project (units, privacy class, storage policy, models, rule-pack refs, reports, hashes) | `P/schemas/model.schema.yaml` `Project` properties | T (create/open/list/save_local_project), S |
| Model: nodes, elements, components, materials, sections, supports, load_cases, combinations, results, diagnostics, unresolved_assumptions, traceability links, operation/state/run/comparison/handoff refs | `model.schema.yaml` `Model`; `$defs` include SpringHanger, Wind/SeismicEquivalentStaticInput | T/G. L only for Node `position.x` |
| Design knowledge and constraints | `schemas/design_knowledge.schema.json`, `schemas/constraint.schema.json`; SPEC §3.1 | T (load_design_knowledge), S |
| Rule pack (required inputs, typed-AST expressions, allowables, checksum) | `schemas/rule_pack.schema.yaml`; `core/rules/*`; `examples/rule_packs/invented_demo.yaml` | T (validate/save/open/list/delete_local_rule_pack, run_rule_checks) |
| Libraries (material, section, component, hanger) | `core/library_import`; `schemas/hanger.schema.yaml` | T (validate_library_import, save/open/list/delete_local_library) |
| Model state (immutable, hashed) | `schemas/model_state.schema.json`; SPEC §3.2 | S/Py. The desktop keeps no named states (MVP_COMPARISON return) |
| Analysis run | `schemas/analysis_run.v0.2.schema.json`; `core/analysis_runs/records.py` | T (result/run carried in save), H |
| Handoff and exports (native JSON, `.mbf` model batch, PCF, stress-neutral, glTF review geometry, external-prover-run evidence) | `core/handoff/*`; `schemas/caepipe_mbf_export.schema.json`, `caepipe_external_run.schema.json`, `handoff_package.schema.json` | G (panels), S |
| Report package | `core/reporting/*`; T (render_calculation_report, save_report_package); H (export-results) | T/H |
| Model operation / operation batch | `schemas/model_operation.schema.json` | T, WASM, L (subset) |

**State**
- The live workspace model, selection, pending review queue, undo/redo checkpoints, solve job and result standing are all held in the **React frontend session**. Tauri engine commands are stateless model-in/model-out functions [implemented (`P/apps/desktop/src/features/workspace/workspaceSession.ts` lines 938–1070, 1373–1420; `src-tauri/src/lib.rs` lines 1931–1965)].
- The live-control contract states the controller had to be "evolve[d]" to expose basis and publication acknowledgements because queue/apply ran through "multiple React setters without an external completion receipt" [described design] (`UI/ROOT/CONTINUATION_2026-09-19_CODEX/PIPING_LIVE_CONTROL_CONTRACT_DRAFT.md` line 55).
- Persistence is a local SQLite-backed store holding canonical JSON/JCS bytes behind application-service boundaries. Direct SQL is prohibited [accepted requirement] (SPEC §4.4; SCA-003).
- Undo/redo checkpoints are session-only. Redo is capped at 25 entries, and undo clears computed results ("Save is still required") [implemented (workspaceSession.ts lines 1373–1394)].
- Reopened projects restore stored operation records as "acceptance unknown". They do not restore "batch grouping, receipts or undo checkpoints" [implemented (`src/App.tsx` line 434)].
- A reopened result is Historical; a new solve is required for current report readiness (MVP_COMPARISON return, citing `workspaceSession.ts` lines 1760–1797).

**Operations**
- The structured operation engine is `core/model_operations/operation_applier`, a Rust crate compiled both natively (Tauri) and to WASM (the "sole browser-mode operation engine"). It validates without mutating, emits diff-preview rows and returns a *new* document on apply. Blocked operations are findings, with "no invented values, no ungoverned unit conversion, no geometry defaults" [implemented (`operation_applier/src/lib.rs` lines 1–15; `apps/desktop/src/services/wasmEngine/loadWasmEngine.ts` lines 1–10)].
- Change kinds include `set_field`, `create_node`, `create_support`, `create_material`, `create_section`, `assign_section`, `create_load_case`, `create_primitive_load`, `update_load`, `update_support`, `create_combination(_term)`, `connect_pipe_run`, `split_pipe_run`, `transform_pipe_run`, `insert_component_symbol` and the corresponding `delete_*` operations. Atomic batches publish all or none, with one Undo checkpoint [implemented (grep of `operation_applier/src/*.rs`; contract draft line 63)].
- Schema enums [S]: `author_type` ∈ {user, agent, import_adapter, project_template}; `operation_status` ∈ {proposed, schema_validated, blocked_by_diagnostics, ready_for_user_review, rejected}; `professional_boundary` has `human_review_required: const true` and all five claim flags `const false` (`model_operation.schema.json` `$defs`). The outcome envelope distinguishes `validate_only`/`apply` and `tauri_backend_apply`/`local_wasm_engine` (`operation_outcome.schema.json`).
- Engine-generated plans: a self-weight operation-plan generator produces drafts that enter the same review queue [implemented (`src/services/selfWeightPlanService.ts`; T `generate_self_weight_operation_plan`)].
- Solve runs as an asynchronous job: T start/poll/cancel_preview_mechanics_job (`lib.rs` lines 1777–1820).
- The headless runner has verbs `solve`, `validate-input`, `export-results`, `run-benchmark` and `run-regression`. It runs one foreground local process, reads JSON from stdin, writes JSON to stdout, and has no network, daemon or telemetry [implemented (`core/runner/headless/src/bin/openpipestress-runner.rs` lines 1–6, 823–832); accepted requirement DEC-065 (SOFTWARE_DECOMP line 666)].
- The desktop's Tauri surface is about 37 commands (`lib.rs` lines 4615–4653). None is reachable from outside the webview except through the LCB bridge.

**Results.**
- Result families include nodal displacements and rotations; element-local axial/shear forces, torsion and bending moments; axial, bending and torsional-shear stresses; reaction resultants; displacement magnitude; open-formula stress summary; combination/modulus-basis records; and review items for curved bends, expansion-joint thrust and component stiffness/stress multipliers [implemented (`core/product_physics/src/*.rs` result kinds)].
- Each result carries metadata: component, coordinate system, endpoint, recovery basis, sign convention and entity_ref. The desktop derives a `ResultInterpretation` view linking a result to its model entity, diagnostics and audit context [implemented (ARCH `TP-MAC-02` lines 27–37; `TP-MAC-03` closeout lines 84–116; `src/features/results/resultInterpretation.ts`)].
- Rule-check results are per-check outcomes plus a worst-of aggregate (`schemas/rule_check_run_result.schema.json`).

**Errors and diagnostics.**
- Warning classes: `SOLVE_BLOCKING`, `RULE_CHECK_BLOCKING`, `PROVENANCE_WARNING`, `ASSUMPTION_WARNING`, `NONLINEAR_WARNING`, `IP_BOUNDARY_WARNING`. The runner adds `UNIT_WARNING`, `RUNNER_BLOCKING`, `EXPORT_BLOCKING` and `PRIVACY_WARNING` [accepted requirement SPEC §8; implemented `core/runner/headless/src/lib.rs` lines 34–46].
- Missing inputs are explicit findings and are never defaulted (SPEC §4.3).
- Every UI capability returns a disabled reason ("Select a load case in the model tree first") [implemented (`src/features/toolkit/capabilityCatalog.ts` lines 404–480)].

**Recovery.**
- Stale-basis rejection: batches capture a basis model and hash at queue time [implemented (workspaceSession.ts lines 972–993)].
- Queue clearing invalidates in-flight callbacks (lines 955–970).
- Cancelling a solve is supported.
- The LCB defines states queued/committed/rejected/withdrawn/expired/outcome_unknown, same-key idempotent retry, and an explicit "restart expires handles … never replay" rule [implemented on LCB (`docs/LIVE_CONTROL_DEVELOPMENT.md` §"Recovery and limits")].

**Observed asymmetry** [agent inference]: nearly all authoring, rule-check, library, persistence, comparison and export operations are reachable only via **G/T**. The only external structured routes are **H** (solve, validate, export report package, benchmarks) and **L** (Node `position.x` only, unmerged).

---

## 3. Current and planned agent integration

**3a. In-product "Design Agent" workbench and proposal panel** [implemented, review-only].
- An "Agent" tab offers Run / Propose / Review / Inspect buttons and shows selection, target, queue and boundary (`src/App.tsx` lines 1277–1374).
- "Propose" calls T `sample_agent_proposal` or falls back to the fixture `fixtures/product_preview/invented_agent_proposal.json`. Both deterministically build an `attach_design_knowledge` review note from the current mechanics result. **No LLM is involved** (`src/services/previewService.ts` lines 473–491, 641–700; `lib.rs` lines 1919–1929).
- The panel shows "Accept disabled — Review-only until accepted mutation is implemented" (`src/features/agent-proposals/AgentProposalPanel.tsx` lines 116–119).
- The right-hand agent strip and toolbar toggle are disabled with "Agent: not available yet", marked as host gap G-19 (`src/features/workspace/shell/AgentStrip.tsx` lines 5–9; `shellLayout.ts` lines 146–147).

**3b. Offline proposal intake** [implemented].
- The user pastes or opens an operation-batch JSON. The shared engine validates it and it enters the normal review/apply queue. The panel states: "Author attribution is supplied by the file and is not verified identity. This workflow has no connected agent provider."
- A downloadable capability/schema reference is offered for offline authoring (`src/features/offline-proposal-intake/OfflineProposalIntakePanel.tsx` lines 17–48).
- The capability catalog marks "Agent validate / preview / apply" as `partial`: "Live provider integration remains held" (`capabilityCatalog.ts` lines 365–373).
- The Runtime plan notes this path "silently captures queue-time basis and is not itself the live adapter" (`R/execution/_Coordination/AgentRuns/APPLICATION_DYNAMIC_TOOLS_20260920/PLAN.md` line 11).

**3c. Development live control (CLI → private bridge → live controller)** [implemented on the LCB only; unmerged].
- The owner authorised the bounded tranche on 2026-09-24 (`UI/CONTINUATION_2026-09-24/OWNER_DECISIONS.md` lines 21–29). It covers `inspect`, `preview`, `submit` and `status`, for Node `position.x` single edits and atomic batches only. **External tools cannot Apply**; the human Apply stays in the app. Recovery is limited to the same controller session.
- LCB sources: `src-tauri/src/live_control.rs` (863 lines), `live_control_wire.rs`, the `swbpipe-control` CLI, `src/features/workspace/liveControlController.ts` (560 lines) and `src/services/liveControlBridge.ts`.
- The bridge is opt-in via `SWBPIPE_LIVE_CONTROL=1` and works on macOS only, over a private 0700 Unix-socket directory with an attachment descriptor and capability. Only the main webview can register.
- Every call carries an explicit workspace and an opaque basis bound to app instance, controller session, project generation, model revision and JCS SHA-256 model hash.
- Proposals are stamped `author_type: agent` with `source_role: external_agent_proposal` and `submitted_operations_trust: untrusted_submitted_metadata_not_validation_evidence`.
- Receipts carry `acceptance route local_review_apply`, "identity verification not performed", and "professional approval false" (LCB `P/docs/LIVE_CONTROL_DEVELOPMENT.md` lines 3–59, 127).
- Checks on record [executed check (record)]: TypeScript passed; 37 focused frontend tests; native library 8; transport 7; CLI 4+3. An independent-review backcheck returned PASS. **Actual native I1/I2 and real-human H1/H2 witnesses remain open** (LCB `…/LIVE_MANAGER/IMPLEMENTATION/IMPLEMENTATION_RETURN.md`, "Actual validation" and "Boundaries still requiring execution/review"; `RESUMPTION_20260924/RETURN.md`).
- Contract commitments [described design] (`PIPING_LIVE_CONTROL_CONTRACT_DRAFT.md` lines 30–51):
  - A later selection must not retarget a proposal.
  - "Equal canonical contents after Undo do not revive an old revision."
  - "An agent-generated CUA click is not human acceptance."
  - "Queued is not committed."
- Transport history:
  - A strict modern-MCP route failed with the bundled Codex client.
  - The owner accepted "CLI first"; any future MCP adapter must meet the stateless 2026-07-28 protocol condition [owner feedback] (`UI/ROOT/CONTINUATION_2026-09-19_CODEX/OWNER_CLI_PROTOCOL_DISPOSITION_PEER_2026-09-20.md` lines 5–10; contract draft lines 13, 19–23).

**3d. Chirality Runtime application-owned dynamic tools** [implemented in Runtime; SWBPIPE not a consumer].
- Runtime registers an immutable per-session tool catalog before the first turn and routes Codex dynamic-tool calls to the owning host. The host validates, applies domain semantics and completes the call. Runtime does "not implement full JSON Schema or Piping semantic validation" (`R/docs/APPLICATION_TOOLS.md` lines 3–5, 9–48, 69–76).
- `success` reports tool execution, "not human acceptance". A submit must report "queued" until committed (lines 91–93).
- Proposed SWBPIPE tools are inspect selection, preview operations, submit proposal and get proposal status, with "no agent-facing Apply" (lines 126–139).
- Evidence covers controlled composition tests and an offline stock-Codex probe only: "No live model turn, native descendant inheritance, or SWBPIPE mutation is established" [executed check (record)] (lines 146–153; `PLAN.md` line 41).
- Embedding constraints: Runtime is a Node service over a Unix socket. "There is no Tauri sidecar distribution yet"; "A Rust host must implement the same wire or host the existing client in its Node sidecar" (`R/docs/APPLICATION_CONSUMER_GUIDE.md` lines 20–22).
- The owner chose "Codex controller first; embedded agent follows" [owner feedback] (`UI/ROOT/CONTINUATION_2026-09-19_CODEX/OWNER_CODEX_VALIDATION_CONTROLLER_2026-09-20.md` lines 5–11).
- Piping remains "outside the Root-runtime and App-harness client sets" (DEC-091, SOFTWARE_DECOMP line 692).

**3e. Earlier App-era domain-engine surfaces** [implemented historically; not Codex-live].
- `_DomainEngines/profiles/open_pipe_stress.yaml` is ADOPTED at integration level `MANUAL_BRIDGE` (L0), with L3 the ruled destination. It lists deterministic tools (operation_applier.validate/apply, completeness_checker, rule_check_runner, headless_runner "L2 PROVEN").
- Agent-writable paths are limited to `_DomainEngines/proposals/open_pipe_stress/**`, which is empty ("L3 not reached") (profile lines 24–27, 55–120; `DOMAIN_ENGINE_INDEX.md`).
- The App harness had `mcp__chirality__domain_headless_preview_run` live for `open_pipe_stress` through a SHA-pinned local runner (`AD/frontend/docs/harness/tool_catalog.md` lines 25–36).
- DEL-10-05 records that such "retained implementation is compatibility evidence, not proof of live Codex exposure" (`AD/execution/PKG-10_Domain_Engine_Future_Boundary/1_Working/DEL-10-05_…/ScopeOfWork.md` CLM-004).
- The only live-LLM propose/validate demonstration (D-APP-52, claude-sonnet-5) targeted **pec**, not SWBPIPE (`…/DEL-10-03_…/Evidence_DAPP52_LIVE_LLM_DEMO_2026-07-18.md`).

**3f. Computer use.**
- The owner plans CAEPIPE validation with the agent "in control of SWBPIPE and using Computer Use to interface with CAEPIPE", on this Mac through a Windows VM [owner feedback] (`OWNER_MVP_AGENT_CORRECTION_2026-09-20.md` lines 5–6, 21–25).
- The owner noted "we can do both with Computer Use", but the adopted plan is SWBPIPE via typed tools and CAEPIPE via Computer Use. Guest controllability "remain[s] to be witnessed" [unrealised intention].

**Standing on proposal versus execution, human gates, solver truth and provenance** [accepted requirement / implemented as cited above]:
- Every mutation passes through one applier route.
- Agent output is a proposal until the human applies it.
- Solver and rule outputs carry the fixed boundary flags.
- Human acceptance is external and hash-bound.
- Rationale records are guarded by `core/model_operations/agent_rationale/engine.py` (flags such as `software_can_accept_engineering_work: False`).
- DEL-10-05 separately states that Chirality must never represent domain output as solver truth it owns.

---

## 4. Engineering-analysis workflow examples

| Workflow | Source | Standing |
|---|---|---|
| Agent-controlled external-prover correlation. Prepare an invented case in SWBPIPE, solve, export the `.mbf` model batch, operate CAEPIPE through Computer Use, compare results and dispose of discrepancies. Fields to record: model/export hashes, tool version, manual changes, load-case/support mapping, tolerance basis, disposition. | PRD §22.5 lines 1410–1427; contract draft lines 61–69 ("extend … for supported case preparation, solve/status, result inspection and model-batch/report export"); OWNER_MVP_AGENT_CORRECTION | accepted requirement (posture); unrealised intention (agent loop). Correlation is owner-gated on lawful access. |
| Delegated model edits: the agent produces a batch; the engineer checks it in node-row tables, accepts row by row, multi-row or whole batch, and marks rows Checked | DP `DIRECTION_DECISION_2026-09-17.md` §1.2 Q5, §2 items 5–7; DEC-104 | owner feedback / accepted requirement (Checked mark). Row-level agent acceptance and per-cell origin marks are not observed in code (agent inference from grep). |
| Agent checks the engineer's work "without altering the tables", with feedback attached to rows, results and report text on a shared Review page that keeps prior iterations | Same record, Q6 and §2 item 6; DEC-103 item 8 (agent cards use only "Check", "Open issue", "Draft", "Proposal", "Evidence summary"); `src/design/tokens.json` lines 586–592 | owner feedback / described design. Only the tokens exist; no Review-page agent cards are implemented. |
| Result interpretation: select a result or diagnostic, get linked entity/diagnostic/knowledge context and a non-mutating review narrative | ARCH TP-MAC-03 lines 21–39, 84–116 | implemented (deterministic, fixture-driven narrative) |
| Iterate after issue identification: displacement, reaction, terminal load, clearance | PRD §10.3; §13.3 example `add_support` operation with rationale, constraints considered and unresolved assumptions | accepted requirement (R7 held) |
| Route/support candidate generation and ranking | PRD §6.2 item 3, §13.3, R7 | unrealised intention (held under DEC-042) |
| Baseline versus alternative comparison | PRD §10.5, §15; MVP_COMPARISON return "smallest honest next proposal" | accepted requirement; not implemented in the desktop |
| Self-weight / hanger plan generation into the review queue | `selfWeightPlanService.ts`; `HangerSelectionPanel` | implemented (deterministic generator plus human review) |
| Report assembly: inputs, versions, hashes, provenance, warnings, results, rule-pack refs, §19.3 notice | PRD §19; T `render_calculation_report`; H `export-results` | implemented (bounded) |
| Pre-reliance review checklist: 7 steps covering identity/units, geometry/loads, provenance, diagnostics, rule inputs, manifest/hashes, external records | `user_guide/index.md` §11 lines 256–269 | described design (a natural reusable-workflow candidate — agent inference) |
| Validation reproduction by an actor-neutral (maintainer or agent) procedure | PRD R6 exit criterion | accepted requirement |

---

## 5. Host-integration constraints

- **Stack.** Tauri 2 (Rust) plus React 19/TypeScript/Vite/three.js. The Rust core crates are reached both via Tauri and via WASM. There is no root Cargo workspace [implemented (`apps/desktop/package.json`; `plans/evidence/2026-09-22_alignment_manual/project-piping-notes.md` lines 47–49)].
- **Where live state lives.** Authoritative live state is in the webview's React controller. Any agent path must reach it through a controller seam with publication acknowledgements, not by calling stateless engine commands (contract draft line 55) [agent inference from implemented code].
- **Runtime packaging.** Runtime needs Node plus a pinned stock Codex (0.154.0) and a per-app private instance. Tauri sidecar packaging is unbuilt (`APPLICATION_CONSUMER_GUIDE.md` lines 20–22, 32–35, 69–71, 173).
- **Platform.** macOS Apple Silicon first. The live bridge exists only on macOS; other hosts return `unsupported_host`. Tauri `security.csp` is `null` (`tauri.conf.json`) [implemented].
- **Local-first and offline.** Modeling, solve, rule checks, reporting, comparison and export must work without cloud [accepted requirement PRD §20.4, §7 item 8]. The provider channel is owner-configured with no app guard (DEC-051). The owner's longer-term intent is local-model operation (oMLX) as a premium feature after the MVP, and he rejected an off-prem API path [owner feedback] (`OWNER_CLI_PROTOCOL_DISPOSITION_PEER_2026-09-20.md` lines 12–17).
- **Determinism.** Canonical JSON/JCS hashing, stable IDs, deterministic comparison and report reproducibility (PRD §5.6–5.7, §22.4). Agent actions must bind to coherent hashes, and there is "no success inferred from scheduled React state or engine computation alone" (`LIVE_CONTROL_ACTIVATION_PROPOSAL.md`).
- **Professional accountability.** Accept means acceptance of a proposed edit, never engineering approval ("the interface says 'accept', never 'approve'") (DP direction §5). Agent-driven checks "do not lift independent practitioner-usability holds" (`P/AGENTS.md` lines 138–140).
- **Licensing and IP.**
  - MIT project license.
  - No protected standards content in public artifacts.
  - "CAEPIPE" must not appear in the product or user guide (DEC-103 item 9).
  - Export must not bundle commercial solvers or bypass licenses (`user_guide` §12).
  - Codex/Computer Use for a licensed Windows tool requires lawful access (PRD §22.5).
- **Governance weight.** Every mergeable slice needs independent review, the DEC-025 sweep and native witnesses (`P/AGENTS.md` lines 107–153).

---

## 6. Candidate v4 implications and open questions

**All items in this section are [agent inference].**

1. **SWBPIPE already has the right mutation primitive; the gap is perception and transport breadth.**
   - One applier route, `author_type: agent`, atomic batches, basis/hash binding and an idempotent queue→human-Apply→receipt lifecycle already exist or are proven on the LCB. An embedded v4 capability could treat "inspect / preview / submit / status" as the core application-tool contract and grow it by operation family rather than inventing a parallel agent model.
   - *Settling evidence:* LCB native I1/I2 and human H1/H2 witnesses; merge of the LCB; extension to a second operation family.

2. **The owner's interaction model is shared tables, not a chat side-panel.**
   - The owner's words are "no agent-private surface", "equivalent action at the direction of the human", tables as the model, row-level acceptance, a human Checked mark, and agent checks as annotations on a Review page.
   - This implies the shared human–agent interface is largely the application's own typed tables plus a proposal overlay (ghost rows/cells, origin marks). A generic Chirality chat UI would at most be the conversation/queue pane.
   - *Open question:* should v4's embedded interface be a host-rendered component inside SWBPIPE's panel/strip, with Chirality supplying conversation, workflow state and evidence, or a separately rendered surface? *Settles it:* an owner ruling plus a mock of the G-19 agent column.

3. **Structured tools versus computer use, by activity.**
   - Within SWBPIPE, typed tools are preferred and feasible because the tables are the model.
   - Computer use is needed for external tools without APIs (CAEPIPE in a Windows VM), and possibly for visual verification of canvas/report rendering.
   - *Open questions:* does v4 need a first-class pattern for workflows that span typed host tools and computer use on a third-party app under one evidence record? What is the evidence standing of screenshots/OCR from CAEPIPE compared with parsed files? *Settles it:* the planned guest-controllability witness and the first invented-case correlation run.

4. **Workflow capability maps onto engineering review, not only authoring.**
   - Candidate bundled workflows: pre-reliance review (user guide §11), external-prover correlation (PRD §22.5 fields), baseline/alternative comparison, missing-input remediation, and report assembly with the §19.3 notice.
   - Each would need the host to expose read tools for results, diagnostics, rule-check outcomes and manifests. Those are currently G/T-only.
   - *Settles it:* a capability-to-journey inventory of which T commands can safely become agent-readable.

5. **The evidence/provenance model should be the host's.**
   - SWBPIPE already mints receipts, hashes and origin tags. An embedded capability should reference them rather than duplicate them (`APPLICATION_CONSUMER_GUIDE.md` lines 26–28 says the same).
   - *Open question:* where do workflow-run evidence and conversation records live relative to the SWBPIPE project store (the SQLite project store, sidecar files, or a Runtime instance directory)? Save/reopen currently drops receipts and undo checkpoints.

6. **Packaging is a hard host constraint.**
   - A Node+Codex sidecar inside a signed Tauri macOS app, a Rust re-implementation of the Runtime wire, or a local-model path (oMLX) each carry different offline/local-first implications.
   - *Settles it:* a sidecar packaging spike and a qualified local tool loop (`APPLICATION_CONSUMER_GUIDE.md` lines 173–177).

7. **Solver truth is currently weak, so the agent must not amplify it.**
   - With M-01–M-38 open, agent narratives about results carry a heightened risk of misleading confidence.
   - *Open question:* should v4 require result-standing (evidence status, historical vs current, known-limitation flags) to be part of every agent-readable result? The display-forms rule — label always with its authority domain — suggests yes.

8. **Identity and authority.**
   - The LCB records that no Codex or human identity is verified.
   - *Open question:* does v4 need verified human actor identity for Apply and Checked in professional contexts, and how does that interact with PB-TBD-002 (acceptance-record storage)?

---

## 7. Gaps and limits

- **Not inspected in depth:**
  - Solver internals and the theory/validation manuals, which I only skimmed.
  - The full UX specification (`DP/instances/UX-SPEC/UX_SPEC_V1.md`).
  - The CAEPIPE format research (`DP/instances/RESEARCH/E_caepipe_format.md`).
  - Most of the 102 deliverable folders.
  - LCB source bodies beyond the development guide and returns.
- **Stale sources:**
  - `P/docs/SPEC.md` §8 still says "the repository has no frontend application scaffold yet". It is superseded by the implemented app, and SPEC is not a reliable current-state source.
  - Several index docs are stale, per the traps in `project-piping-notes.md` lines 99–110.
- **Record-based claims:** test counts and review verdicts for the LCB come from its records. I did not re-execute them. The 38-finding assessment likewise was not re-verified.
- **Absence searches:** absence claims (no LLM in the in-app proposal, no per-cell origin marks, no Review-page agent cards, desktop not wired to comparison engines) rest on bounded greps and the cited inventory. A differently named implementation could have been missed.
- **Owner-quote custody:** owner quotations come from agent transcriptions with recorded hashes. Their custody is as stated in those records.
- **Unestablished:** no evidence establishes any live model turn against SWBPIPE, CAEPIPE guest control, Tauri-sidecar Runtime packaging, local-model tool loops, or practitioner usability of agent-assisted journeys.
- **Unsettled decisions:** PRD R7, the formal human-acceptance workflow (PB-TBD-002) and MVP publication scope remain owner-held.
