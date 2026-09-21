# D-GOV-43 Proposed Impact and Conformance Assessment

Status: `CANDIDATE IMPACT ANALYSIS — NO AUTHORITY OR APPLICATION` (revision 3, after the round-2 review in `REVIEW_FEEDBACK_R2.md`)

Basis: `main@a75adecf13f055c092ffa92809f66e7817c44242`; preparation HEAD
`03a4b41c3b0e6996c9c8e4b89c95ea25b5e3cb86` on `claude/chirality-v3-mvp-trial-ab05cb`.

## Authority and artifact classification

`D-GOV-43.proposed.md` and `AGENTS.proposed.patch` are candidate governed
records. This impact analysis is derivative assessment. None is authoritative
unless and until the owner rules and the owning application workflow lawfully
changes the live surfaces. The proposal changes no live instruction, standard,
contract, deliverable, lifecycle, pointer, product source, project loop, hold,
pin, installation or trial evidence. The proposed patch is intentionally
inactive and was verified with `git apply --check` against the `AGENTS.md`
at the preparation basis. Packet integrity is the Git history of the
branch; no hash table or self-hash is maintained.

## Evidence basis for the findings

- Source read at the preparation basis: `projects/chirality-runtime/packages/daemon/src/codex-session.ts`
  (notification whitelist at the `quarantine` dispatch; effective-config
  checks; `initialize` with `chiralityAdmissionAuthority`;
  `account/identitySnapshot`; `policyParameters`), `runtime-daemon.ts` (SSE
  writer without keepalives; close handler interrupting the turn),
  `codex-containment.ts` (private `CODEX_HOME`, `-c` overrides),
  `packages/client/src/client.ts` (30 s default socket timeout on the stream
  path), and the App's `frontend/src/lib/runtime-client/runtime-daemon-harness-port.ts`,
  `frontend/src/app/api/harness/turn/route.ts`, `frontend/electron/*.ts`.
- Trial evidence: `projects/chirality-app-dev/execution/_Coordination/AgentRuns/APP_V3_TRIAL_COMPLETION_20260910/R17_FUNCTIONAL_FINDINGS.md`
  (R17-F1, R17-F2 and the plan/execute/workflow demonstration).
- Upstream: `openai/codex` release `rust-v0.154.0` (2026-09-09), npm
  `@openai/codex` 0.154.0, and the schema under
  `codex-rs/app-server-protocol/schema/json` (`ClientRequest.json`,
  `ServerRequest.json`, `ServerNotification.json`, `v2/*`), which contains no
  `chirality*` member and no `permissions` thread-start parameter.
- References consulted: T3 Code (`pingdotgg/t3code`, MIT, Electron,
  `packages/effect-codex-app-server` generated from the upstream schema,
  `apps/server/src/provider/Drivers/CodexHomeLayout.ts` shared-config auth
  overlay, `docs/user/permission-modes.md`); Pi (`badlogic/pi-mono`, MIT, own
  agent loop and provider layer, not a Codex client).

## Root surfaces (M2/G4 application tranche after ruling)

| Surface | Location | Current clause | Proposed change |
|---|---|---|---|
| `AGENTS.md` | Skills paragraph (lines 45–56), context paragraph (line 62), Execution and governance (after line 135) | "only the App-supplied reviewed bundled skill library is trusted for agent context" | Codex native skill discovery with displayed origins; host-owned stock App Server paragraph (shared configuration, separated Codex-custodied authentication, additive role instructions, every server request answered). Exact delta: `AGENTS.proposed.patch`. |
| `docs/CONTRACT.md` §1.13 | K-RUNTIME-1 (161) | "One opt-in per-user daemon is the exclusive production owner of engines, credentials, sessions…" | App host process is the sole owner of its App Server child; credentials custodied by Codex. |
| | K-CONTROL-1 (162) | control socket, accepted supervisor socket, "No third socket and no TCP control listener" | Renderer access through the preload bridge only; no network control listener; daemon and supervisor sockets retired. |
| | K-RESIDENCY-1 (165) | daemon manages one primary local LLM | Retire (ruling item 13). History preserved; local models re-specified as Codex model providers when taken up. |
| | closing paragraph (170–174), enforcement-map row (208) | daemon socket, credentials, tokens | Codex home and App index are operational state; row re-titled "App host and App Server child". |
| `docs/SPEC.md` §14 | 14.1 (873–915) | `--runtime-daemon`, `control.sock`, LaunchAgent, HTTP/SSE routes, shutdown generations | Replace with the host-owned child description: launch, stdio protocol, generated bindings, relaunch and `thread/resume`, exit handling. |
| | 14.2 (917–935) | sessions under `{userData}/runtime/projects/<id>/sessions` | Threads live in the Codex home; App keeps an index keyed by thread ID; `chirality.project.json` unchanged. |
| | 14.3, 14.4 (936–974) | oMLX residency, initial governed run and CLI | Retire to history (ruling item 13). |
| `docs/DIRECTIVE.md` | §5 row (296), §7 (318–333) | "opt-in per-user Chirality runtime daemon is a local process over a Unix-domain socket"; daemon ownership | App host owns the App Server child; no external server; local control by IPC. |
| `docs/TYPES.md` §12 (530–546) | `RuntimeClientCredential`, `RuntimeDaemonStatus`, `RuntimeBackend`, residency types | Retire all four groups; add `CodexHostStatus`, `CodexThreadIndexEntry`, `PolicySelection`, `ApprovalRecord`. |
| `docs/AGENT_WORKFLOW_RUNTIME.md` | 36–39, 46–49, 72–87, 212–218 | bundled-only skills; `permissionMode` | Align to ruling items 4, 8 and 10. |
| `docs/PLAN.md` 145–156; `docs/PRD_ROOT.md` 424–433, 869–872 | D-GOV-20 transcriptions | Read with D-GOV-43 per their own amendment rules; PRD by superseding instrument bound to a git SHA. |
| `docs/WORKFLOW_COMPONENT_STANDARD.md` §4.1, `docs/DBM_Agent_Instruction_Architecture.md` §2 | D-GOV-35 item 7 propagation still pending | Unchanged by this ruling; noted for the same tranche. |
| `.github/workflows/harness-premerge.yml`, `tools/validation/validate_candidate_whitespace.py` | whitespace guard is a CI gate | Advisory or removed (ruling item 11). |

## Decision records

- Superseded in part, never edited: D-GOV-20 items 2, 3, 4 (App MVP Codex
  path); D-GOV-36 daemon custody exception and bootstrap namespace.
- Read with this ruling: D-GOV-28 (runtime stewardship), D-GOV-35 (delegation
  class recognized; envelope re-expressed), D-GOV-37 through D-GOV-40 (runtime
  successor adoptions), D-GOV-41, D-GOV-42 (roles, skills, workflows).
- `_REGISTER.md` gains a navigational row after ruling.

## Root execution carriers

- `execution/_Decomposition/chirality_root_deliverable_register_v1_0.csv`
  rows DEL-02-07 through DEL-02-12: already `RETIRED — SCA-005`; disposition
  confirmed, no re-edit.
- `execution/_ScopeChange/SCA-005_*` requirement traces and
  `RUNTIME_METADATA_BINDINGS.csv`: historical.
- `execution/_Coordination/LOOP_INIT.md`, `HANDOFF_STATE.md`,
  `CURRENT_WORKPLAN.md`: successor entry after ruling.

## Runtime loop (`projects/chirality-runtime`) — changes authorized with this ruling (item 11)

| Path | Status | Architecture-bound content | Disposition |
|---|---|---|---|
| `README.md` | living checkpoint | daemon sole owner; supervisor socket; hosted-validation 0.149.0 payload; 18 conformance limbs; patched-candidate narrative | rewrite to the App-host architecture; keep the Pi/oMLX validation notes as reference |
| `docs/CODEX_MVP_INTEGRATION.md` | living design | supervisor owns transport; "adapter does not launch a supplier directly"; `workspaceWrite` only; native-plan REST routes; `nativeAddonPath` | retire; the App's host design document replaces it |
| `docs/PRD.md`, `docs/PRD_AUTHORITY.md` | Gate3 not accepted / hash index | seven-carrier partition; hashes of the seven contracts | revise; re-issue hashes once |
| `execution/PKG-02_Runtime_Product/1_Working/DEL-02-07` (supervisor socket) | INITIALIZED | sole runtime broker, private second socket, two-job launchd | retire (family 1) |
| `DEL-02-08` (exact supply pin) | INITIALIZED | pin-drift refusal | retire (family 1); the lockfile pin is ordinary dependency integrity |
| `DEL-02-09` (hosted account boundary) | INITIALIZED | root-private `CODEX_HOME`, ambient home excluded | retire (family 3 adapts its purpose into the App's effective home) |
| `DEL-02-10` (closed event union v2) | INITIALIZED | four terminal identifiers, no fifth | retire (family 2); generated bindings replace it |
| `DEL-02-11` (retirement, restart, reconciliation) | INITIALIZED | `thread/resume` only under recorded continuity | retire (family 2) |
| `DEL-02-12` (conformance and release fan-in) | INITIALIZED | nine held bindings against the supply model | retire (family 1); ordinary release checks replace it |
| `DEL-02-06` (stewardship) | INITIALIZED | supplier snapshot, lease, version-mismatch refusal | revise those clauses; stewardship of the pin remains |
| `execution/_Decomposition/*` (SOURCE_SCOPE_REQUIREMENTS, DECOMP, registers, `HOLD_SUCCESSOR_MAP.csv`, `GATE_READINESS.md`) | frozen basis | seven-carrier partition; nine `HELD_UNAVAILABLE` | one `scope-change` amendment closing the nine holds with a concise rationale |
| `execution/_Coordination/HANDOFF_STATE.md`, `MIGRATION_APPLICATION.md`, `MIGRATION_ACCEPTANCE_2026-09-06.md` | current | supplier candidates, SOW hashes | supersede entry; re-hash once |
| `tools/codex-supplier/*` (patch, build recipe, provenance) | live recipe | upstream delta, Seatbelt rule | retire (family 1) |
| `tools/native-admission/*` | prepared probes | admission ABI | retire (family 1) |
| `execution/_Coordination/AgentRuns/RUNTIME_*` | historical | limbs, packaging, hosted status | keep unchanged as history |

## App loop (`projects/chirality-app-dev`) — changes authorized with this ruling (item 11)

| Path | Status | Architecture-bound content | Disposition |
|---|---|---|---|
| `execution/_Coordination/AgentRuns/APP_V3_TRIAL_COMPLETION_20260910/NEXT_AGENT_HANDOFF.md` | frozen checkpoint | restart admission, daemon retention, supplier correction | add a successor section; earlier text unchanged |
| `…/CONSOLIDATED_REVIEW.md` | ACCEPT | criteria (0)–(8) | executed record preserved unchanged; the successor review uses the new procedure's criteria |
| `…/R15|R16|R17_NATIVE_CHECKLIST.md` | executed | guarded launcher, LaunchAgent, admission fence, stale rejection | preserved unchanged; a new short native checklist supersedes their applicability |
| `…/R14..R17_FUNCTIONAL_FINDINGS.md`, `RUN_LOG.md` | evidence | admission events, LaunchAgent pids | keep unchanged as history |
| `…/L_STAGE16..26_PACKAGING/*` | Stage26 PASS | observer, payload bind, governance, seal, supplier signing | preserved unchanged; superseded by the new packaging procedure |
| `…/R14_TOOL_HOST_PROPOSAL/*` | executed | code-mode host 0.149.0 admission | retire; preserved as history |
| `…/R16_RESTART_ADMISSION/*` | completed | host-lease renewal across relaunch | preserved as history; the defect class disappears |
| `AgentRuns/APP_V3_DIRECT_TRIAL_20260910/{HANDOFF,REBUILD_PLAN,TRIAL_FINDINGS}.md` | current | Stage 9–13 packaging spine; harness-port defect | preserved unchanged; superseded by the new procedure |
| `AgentRuns/CODEX_MVP_PACKAGING_20260910/*` | prepared | native addon, carrier patches | retire the addon line; carrier patch re-authored for the stock dependency |
| `NOTICE_CODEX_MVP_PACKAGING_CARRIERS_20260910.md` | adoption required | supplier/native layout | supersede |
| `NOTICE_2026-09-10_ROOT_APP_METHOD_AND_ENGINE_POLICY.md` | authorized | Codex-only ruling; controlled-Runtime CI clause | keep the ruling; revise the CI clause |
| `PKG-09/DEL-09-04` (DMG packaging) | IN_PROGRESS | "admitted Codex supplier subprocess" | revise to the bundled stock dependency |
| `PKG-09/DEL-09-05` (CI release verification) | IN_PROGRESS | admitted supplier and native layout | revise: signature, notarization and pin verification only |
| `PKG-09/DEL-09-06` (network, key, renderer checks) | IN_PROGRESS | containment and credential evidence | revise: keep the ordinary network, key and renderer checks (family 4); drop supplier containment evidence |
| `PKG-09/DEL-09-07` (two-job installer) and `APP_HOLD_REGISTER.csv` `APP-HOLD-1` | OPEN, held | LaunchAgent staging via runtime-control IPC | retire with the hold (family 1) |
| `PKG-09/DEL-09-03/_STATUS.md` V3-02 | gated on G6a | signed-build identity | keep; re-point |
| `PKG-03/DEL-03-03` (harness API and SSE adapter) | IN_PROGRESS | `/api/harness/*` SSE | replace with the IPC channel |
| `PKG-03/DEL-03-01, 03-02, 03-04`, `PKG-05/DEL-05-02`, `PKG-02/DEL-02-05` | IN_PROGRESS | port, lifecycle, event schema, API-key UI | revise |
| `docs/harness/reliance_boundary_register.md` | live | `RB-DAEMON`, `RB-CONTROL-SOCKET`, `RB-ROLE-MODEL` | revise |
| `docs/RELEASE_QUALITY_GATES.md` | live | "Desktop and CLI use one daemon" | revise one clause |
| `docs/{PRD,SPEC,CONTRACT,PLAN,TYPES,VALIDATION_STRATEGY,BUILD_AND_RELEASE}.md` | corpus-hashed | daemon, admission, supplier, harness port, SSE | clause-level SCA and one corpus re-hash |
| `frontend/docs/harness/*` | live | public UI event names, adapter boundary | revise for pass-through |
| `execution/_ScopeChange/SCA-APP-008_*` | AWAITING_OWNER_ACCEPTANCE | seats hosted consent port, two-job installer, K-CONTROL-1 | revise before acceptance; accepting as-is would re-ratify the retired architecture |
| `execution/_ScopeChange/SCA-APP-010_*` | open | shell IA | keep; architecture-neutral |
| `_DECISIONS/D-APP-125` item 3, `D-APP-126`, `D-APP-122`, `D-APP-100`, `D-APP-88`, `D-APP-107` | RULED | isolated homes, daemon custody, host-gated settings, packaged daemon, helper bundle, DEL-09-07 | supersede by one App decision record under this ruling; never silently drop |
| notices `NOTICE_2026-09-07_ROOT_D-GOV-36_*`, `NOTICE_D-GOV-35_*`, `NOTICE_2026-09-03_APP_TM-ROOT-122_*`, `NOTICE_ROOT_RUNTIME_*` | adopted | account-only Unix authority, delegation class, Electron authority | supersede |

## PEC loop (`projects/pec`)

`docs/PRD.md`, `execution/_Coordination/PRD_V2_CANDIDATE_2026-07-24_coordination_plane.md`,
`NOTICE_ROOT_RUNTIME_PROJECT_MIGRATION_2026-09-05.md` and the migration
return classify PEC as a Runtime client. The classification target changes;
a notice records it and PEC revises its own text.

## Load-bearing chains handled deliberately

1. The nine held bindings (`HOLD_SUCCESSOR_MAP.csv`, DEL-02-12) gate a
   shared release and are named against the supply model. They are retired as
   a family, not re-seated or mapped onto the spike checks. Release readiness
   of the App is established by ordinary checks: lockfile-pinned dependency,
   bundle signature and notarization, the spike acceptance evidence, and
   independent source review.
2. `APP-HOLD-1`, DEL-09-07 and SCA-APP-008 action 5 are one chain seating the
   LaunchAgent. Retiring the daemon retires the chain; SCA-APP-008 is revised
   before any acceptance.
3. The trial's consolidated-signed-build spine (Stage 9–13, steps 0a–25) is
   superseded by a new short procedure: build, sign, notarize, verify the
   signature and the Codex pin, run the distinct packaged checks of ruling
   item 12. The executed Stage records are preserved unchanged.

## Purpose test by family (ruling item 11)

Families group checks and gates by shared purpose. Members are listed so the
application tranche can act on them without a further register; the tranche
records a concise rationale and the reviewed Git changes are the evidence.

| Family | Members | Actual purpose | Disposition |
|---|---|---|---|
| 1. Private supplier admission and certification | hosted admission and identity binding; `chiralityAdmissionAuthority`, `account/identitySnapshot`, `chiralityRuntime`; native admission addon; packaged-basis and payload hashing; restart admission (R16 repair); exact supply pin with drift refusal (DEL-02-08); supplier patch, build recipe and provenance (`tools/codex-supplier`); supplier conformance limbs; the nine held release bindings (DEL-02-12, `HOLD_SUCCESSOR_MAP.csv`); packaging observer, payload-bind, governance, seal and supplier-signing steps; two-job installer and `APP-HOLD-1` (DEL-09-07) | Prove that a privately built Codex binary, the daemon and the signed-in account match an accepted basis | Retire the whole family. Nothing is re-created under another name. Ordinary software integrity (family 4) replaces it. |
| 2. Fixed-policy control of Codex | effective-configuration veto (`config/read` table checks); notification whitelist and quarantine; closed HarnessEvent union v2 (DEL-02-10); continuity gate on `thread/resume` (DEL-02-11); per-chat model and effort freeze; SSE relay and its timeouts | Keep the agent inside a fixed, projected contract | Retire the whole family. Policy is the user's choice, shown and recorded; the full stream is carried through generated bindings plus the declared experimental augmentation; unfamiliar notifications are inspectable; every server request is answered. |
| 3. Credential and home separation | root-private `CODEX_HOME` (DEL-02-09, D-APP-125 item 3); daemon custody exception and bootstrap namespace (D-GOV-36) | Keep Chirality sign-in separate from the user's other Codex clients | Adapt: the effective home with private `auth.json` and shared configuration, credentials custodied by Codex, backend verified in S-8. |
| 4. Ordinary software integrity | lockfile-pinned dependency; App code signing and notarization; renderer isolation, validated IPC and no credential material in the renderer; the network, key and renderer checks of DEL-09-06; request and session correctness tests | Normal product integrity and security | Retain. |
| 5. Process hygiene | candidate whitespace guard; README self-hash convention; duplicate test execution across stages | Cosmetic hygiene; packet integrity without a consumer; re-establishing the same fact per stage | Retire as gates. Whitespace advisory at most; Git history is packet integrity; a test runs once per distinct condition. |
| 6. Human accountability | owner ruling; owner native trial; explicit publishing approval; independent source review | Decisions reserved to the human; defects caught before packaging | Retain the three human decisions. Independent source review is retained as an engineering responsibility before the consolidated build, not a human approval prompt. Material scope changes and consequential findings return to the owner. |

## Existing trial chats and executed records

Daemon-era chats (R6 trial project, R14 to R17 sessions) exist as Runtime
JSON/JSONL session records under the trial user-data directory and as Codex
thread records in the trial's private Codex home. They are preserved
unchanged in place. If the App's existing session reader renders them
without new work they remain viewable; otherwise they remain an accessible
archive alongside their evidence files. No history-import feature is a
release prerequisite and no continuation is promised.

Executed native checklists, packaging stage records, consolidated reviews and
findings are likewise preserved unchanged. The tranche creates the new
procedures and supersedes the applicability of the old ones; it does not edit
historical evidence.

## Coordinated tranche and notices after ruling

Under ruling item 11 the Runtime and App changes above are authorized with
the Root amendments and applied in one coordinated tranche. The notices below
record that application to each loop; they do not reopen approval of this
decision, and the arrangement is bounded to this decision.

- `projects/chirality-runtime/execution/_Coordination/NOTICE_<date>_ROOT_D-GOV-43_CODEX_HOST_REPLATFORM.md`
- `projects/chirality-app-dev/execution/_Coordination/NOTICE_<date>_ROOT_D-GOV-43_CODEX_HOST_REPLATFORM.md`
- `projects/pec/execution/_Coordination/NOTICE_<date>_ROOT_D-GOV-43_CODEX_HOST_REPLATFORM.md`

## Non-effects and blockers

- No live surface changes. No installation, trial evidence, R17 App or
  daemon, or Codex home is modified or deleted.
- No supplier, package, release, publication or merge is authorized.
- Blockers to application: the owner ruling; the coordinated application
  tranche's own M2/G4 manifest.
