# SWBPIPE fact sheet for the App v4 relay questions SQ-01…SQ-32

Prepared 2026-09-28 by a Type 2 TASK (read-only researcher) for ROOT, the SWBPIPE HELP_HUMAN session. It is research input for ROOT's answers. It is not an answer, commitment, intention or delivery by the SWBPIPE owner, and nothing here was relayed to the App.

## 0. Basis, standing labels and abbreviations

**Question source.** `projects/chirality-app-v4/execution/PKG-09_Candidate examination and connected journeys/1_Working/DEL-09-06_Connected activity contract and workflow round trip/Design/RELAY_QUESTIONS_SWBPIPE.md` (RELAY-v0.3, 1,135 lines, read in full). Vocabulary: `projects/chirality-app-v4/execution/_Coordination/HANDOFF_SWBPIPE_DOMAINS.md` and `projects/chirality-app-v4/docs/HOST_INTEGRATION.md` §2, §11 (read-only).

**SWBPIPE basis.** Main `24dea2dae` (merge of PR #1042). Product files were read from the K5 worktree after verifying that K5 changes only solver files and T3 records relative to `24dea2dae`; every record cited below was either read with `git show 24dea2dae:` or verified unchanged by K5. PR #885 was read with `gh pr view` / `gh pr diff --name-only`, and its head files with local `git show 12907f393:` (read-only, the local object equals the PR head).

**Standing labels used on every fact.**

| Label | Meaning |
|---|---|
| **[MAIN]** | Product source or schema on main `24dea2dae`: exists and runs as written. |
| **[MAIN-REC]** | Governance, decision or design record on main. It states a rule, ruling, plan or design; it is not product behaviour. |
| **[DESIGN]** | Design-programme record on main (UX spec, operations map). Designed, **not implemented**. |
| **[PR885-OPEN]** | Draft PR #885, head `12907f393`, **open, unmerged, not on main**. Evidence of in-progress work only. |
| **[PLANNED]** | A work-graph row or proposal that is planned or deferred, **not delivered**. |

**Abbreviations (repo-relative).**

| Short | Path |
|---|---|
| `P/` | `projects/chirality-piping/` |
| `DESK/` | `P/apps/desktop/` |
| `APPLIER/` | `P/core/model_operations/operation_applier/src/` |
| `WG` | `P/execution/_Coordination/WorkGraphs/HELP-HUMAN-PIPING-20260918-UI-IMPLEMENTATION/WORK_GRAPH.md` |
| `AR/` | `P/execution/_Coordination/AgentRuns/HELP-HUMAN-PIPING-20260918-UI-IMPLEMENTATION/` |
| `C24/` | `AR/instances/CONTINUATION_2026-09-24/` |
| `C19/` | `AR/instances/ROOT/CONTINUATION_2026-09-19_CODEX/` |
| `SD` | `P/execution/_Decomposition/SOFTWARE_DECOMP.md` (§12 decision log; §-level OI table) |
| `REG` | `P/execution/_Coordination/_DECISIONS/_REGISTER.md` |
| `OPMAP` | `P/execution/_Coordination/AgentRuns/HELP-HUMAN-PIPING-20260916-UI-DESIGN-PROGRAM/instances/UX-SPEC/OPERATIONS_MAP.md` (UX spec V1.2 operations map) |
| `PKG16/` | `P/execution/PKG-16_Model Operation and Agent Proposal Framework/1_Working/` |
| `PR885:` | a file at PR #885 head `12907f393` |

---

## 1. Cross-cutting facts (cited once, used by many SQs)

**X-1. No live agent binding exists on main.** [MAIN]
- The desktop's agent strip and toggle are disabled with the reason "Agent: not available yet"; the code comment names the live binding as host gap G-19 (`DESK/src/features/workspace/shellLayout.ts:146-147`; `DESK/src/features/workspace/shell/AgentStrip.tsx:5-9`).
- Proposals arrive only as a pasted or opened JSON batch in the offline intake panel, which states that author attribution is file-supplied, not verified, and that the workflow has "no connected agent provider" (`DESK/src/features/offline-proposal-intake/OfflineProposalIntakePanel.tsx:17-26`).
- The exported capability reference says the live provider is held (`DESK/src/App.tsx:493-497`); the toolkit entry `review.agent` is `partial`, "Live provider integration remains held" (`DESK/src/features/toolkit/capabilityCatalog.ts:366-372`).
- The "Design Agent" workbench's Propose button calls the Tauri command `sample_agent_proposal`, which builds a fixed, review-only `attach_design_knowledge` proposal from the current solve result (`DESK/src-tauri/src/lib.rs:1851-1952`). Its Accept button is permanently disabled, "Review-only until accepted mutation is implemented" (`DESK/src/features/agent-proposals/AgentProposalPanel.tsx:116-119`).
- No model-provider client, MCP server, OpenAI/Anthropic client or chat loop exists in `P/apps`, `P/core`, `P/api`, `P/tools` or `P/schemas` (word-boundary search for mcp, openai, ollama, llama, llm, completions, codex; only `api_key` appears, as a redaction key name in `P/core/security/*/controls.py` and `DESK/src/features/redaction-controls/redactionExportControls.ts:273`).
- No Chirality Runtime or harness package is bound into the piping product (search of `P/apps`, `P/core`, `package.json` files for harness-contract, chirality-runtime, application-tools, `@chirality/`: none).

**X-2. One operation route (the "one route").** [MAIN]
- All model edits go through `operation_applier` (Rust), exposed as Tauri commands `validate_model_operation`, `apply_model_operation`, `validate_model_operation_batch`, `apply_model_operation_batch` (`DESK/src-tauri/src/lib.rs:1953-1988`, registered at `:4731`), and as the same crate compiled to wasm for browser mode (`APPLIER/lib.rs:876-1000`; ADR-0001 / DEC-020, `P/docs/architecture/adr/ADR-0001_operation_seam_engine_unification.md`).
- 27 change kinds are accepted, mapped to operation kinds create/connect/delete/insert/modify (`APPLIER/lib.rs:2176`, `check_kinds`). There is one crate version `OPERATION_APPLIER_VERSION = "0.1.0"` (`APPLIER/lib.rs:33`); no per-operation identity-and-version catalog.
- The input model is never mutated in place; apply returns a new model document (`APPLIER/lib.rs:1-15`, `:866-874`).
- Batches are atomic: all steps apply or none (`simulation_disposition` = `committed_as_one_batch` / `rolled_back_no_model_published` / `validation_only_discarded`, `APPLIER/atomic_batch.rs:1-16`, `:184`).

**X-3. Content identity is whole-model only.** [MAIN]
- The model hash is SHA-256 over RFC 8785/JCS canonical JSON of the whole `model_payload`, carried as `{algorithm, canonicalization, payload_scope, payload_ref, value, hash_status:"computed_local_preview"}` (`DESK/src-tauri/src/lib.rs:2050-2059`; `APPLIER/atomic_batch.rs:18-25`).
- An optional `claimed_model_hash` is compared with the backend hash; a mismatch blocks as stale (`OP-CLAIMED-MODEL-HASH-MISMATCH`, `APPLIER/lib.rs:7847-7948`). Without a claim, the per-field before-value check is the staleness guard (`OP-STALE-BEFORE-VALUE`, `APPLIER/lib.rs:7422`, `:7450`; `binding_status` text at `:7834`). Batches require a claimed hash (`OP-BATCH-MODEL-HASH-REQUIRED`, `APPLIER/atomic_batch.rs:90`) and may carry a `source_model_hash` bound to the plan's source model (`:95-105`).
- No per-row or per-object subject content identity is returned by any read or outcome.

**X-4. Acceptance on main is the person's local Apply; receipts are session-only.** [MAIN]
- An applied outcome records `acceptance_basis: "user_initiated_apply_in_local_session"`, `acceptance_is_professional_approval: false`, `persistence_status: "session_state_only_not_yet_saved"` (`APPLIER/lib.rs:2018-2030`; batch form `APPLIER/atomic_batch.rs:192-196`).
- Session receipts (`AppliedOperationReceipt`: receipt_id, sequence, operation/change ids, target, field, before/after, route, applied model hash, acceptance, diagnostics) live in React session state (`DESK/src/types.ts:1013-1028`; `DESK/src/features/workspace/operationsSessionState.ts:28-33`; constructed at `DESK/src/features/workspace/workspaceSession.ts:1373-1388`).
- The saved project envelope carries the model, pending intents, one `proposal` slot and hashes, but no applied receipts (`DESK/src/types.ts:1198-1210`). The ledger panel lists as unresolved TBD: durable audit persistence, the "final actor identity model" and durable receipt persistence (`DESK/src/features/operations/OperationLedgerPanel.tsx:175-179`).
- A Python reference audit-record constructor for DEL-16-03 exists (decision status accepted / rejected / held, actor, `decided_at`, record hash; accepted records need `actor_type == user` and a current model-state hash), but it is not wired to the desktop (`P/core/model_operations/audit_trail/engine.py:1-6`, `:137-236`; only `agent_rationale/engine.py` references it). DEL-16-03's scope says durable persistence remains a delivery obligation and the final actor identity model is TBD (`PKG16/DEL-16-03_User acceptance and operation audit trail/ScopeOfWork.md:69`, `:77`, `:79`).

**X-5. PR #885 is the only external-control seam, and it is open and deferred.** [PR885-OPEN] [PLANNED]
- `gh pr view 885`: draft, OPEN, base `main`, head `12907f393`, 191 files, created 2026-09-24, last updated 2026-09-25, title "Connect a private live-control CLI to reviewed Piping operations". Non-record files: native bridge `DESK/src-tauri/src/live_control.rs`, wire `live_control_wire.rs`, CLI `live_control_cli/swbpipe-control.rs`, capability `DESK/src-tauri/capabilities/live-control.json`, controller `DESK/src/features/workspace/liveControlController.ts`, bridge service, tests, wire fixture, and `P/docs/LIVE_CONTROL_DEVELOPMENT.md`.
- Its description lists unfinished qualification: recheck against the merge candidate, clean DEC-025 sweep, actual native single/batch workflows I1/I2, final independent review, actual-human review/Apply witnesses H1/H2.
- The work graph moved LIVE-INTEGRATE, LIVE-HUMAN and LIVE-FINAL into the deferred `UI-SUCCESSOR` on the owner's 2026-09-25 route direction (`WG:12`, `:46-60`, `:120-122`; `C24/OWNER_ROUTE_DIRECTION_2026-09-25.md`). The successor starts when the owner directs (`WG:60`). The graph states it governs over earlier checkpoint text (`WG:21`); the PR description's note that the owner reconfirmed finishing qualification is older standing text within the same day.

**X-6. Governing records on agents (all [MAIN-REC]).**
- **OI-016** (`SD:599`): agent operation autonomy level is TBD; default scope requires user acceptance and an audit trail. Owner column: PKG-16 / security-privacy / human product decision.
- **PRD §5.3 and FR-AGENT-001…005** (`P/docs/PRD.md:140-144`, `:538-542`): agent changes are structured operations, validated, shown, applied only through the engine; FR-AGENT-003 requires user acceptance "unless the user configures another workflow"; R7 exit criteria include accept/reject and auditable, reversible operations (`:1597-1611`).
- **OPS-K-AGENT-4** (`P/docs/CONTRACT.md:50`): agent outputs are drafts until a human gate accepts them.
- **DEC-041 / D-22** (`SD:646`; `REG:55`): historical ruling to consume the chirality-app-dev harness as packages with a Node Agent-SDK sidecar at live binding. **D-58 / DEC-091** (`REG:95`; `SD:696`): current reliance on that mechanism retired; Piping kept outside the Root-runtime and App-harness client sets; no successor mechanism adopted; automation-condition mechanism unresolved.
- **DEC-042** (`SD:647`): harness-independent preparation is sanctioned, but no live agent binding proceeds under it (it stays behind D-21 and the DEC-041 automation condition). **DEC-103** item 8 (`SD:708`) says a live agent remains a separate stage act under DEC-042, and fixes five class words for agent cards on the Review page. The 2026-09-24 activation below is recorded as the act these rows held.
- **Bounded live-controller activation, 2026-09-24** (`C24/OWNER_DECISIONS.md`, "Bounded live-controller activation"): owner authorized the bounded CLI tranche: inspect/preview/submit/status, Node coordinate single and atomic-batch edits, human Apply, same-controller-session recovery, real human witnesses; external tools cannot Apply; no embedded Runtime, CAEPIPE, new result schemas, engineering acceptance or release.
- **Owner directions 2026-09-20** (`C19/OWNER_CODEX_VALIDATION_CONTROLLER_2026-09-20.md`; `C19/OWNER_MVP_AGENT_CORRECTION_2026-09-20.md`; `C19/OWNER_CLI_PROTOCOL_DISPOSITION_PEER_2026-09-20.md`): a development Codex controller first, embedded agent later; agent control of SWBPIPE is an enabling step for planned CAEPIPE validation via Computer Use; a small JSON CLI is the first adapter; any MCP adapter must meet the owner's modern stateless 2026-07-28 condition; the tested bundled Codex client used a legacy handshake and is unqualified for MCP.
- **DEC-051 / D-24** (`SD:656`; `REG:57`; `P/docs/SPEC.md:378-390`; `P/docs/CONTRACT.md:41`): open residency. An owner-configured model provider (local, Anthropic or other) for an embedded agent may receive the owner's private data with no app-side guard, opt-in gate or indicator; framed "for now", revisiting is a human decision.
- **DEC-104** (`P/execution/_Coordination/_DECISIONS/D-71_RULING_ADDENDUM_2026-09-18.md`, item 7): the "Checked" mark is a PRD §16.3 tag, not an acceptance record (details in SQ-01). Storage is gap G-08; no implementation is authorized by the ruling.

**X-7. No SWBPIPE record acknowledges App v4.** A search of main (`git grep` over `P/`) for app-v4, "App v4", HTML-D05, OI-021, HANDOFF_SWBPIPE and RELAY_QUESTIONS finds only incidental mentions: a review note counting App v4 files in a diff, and a receipt noting a rebase over App v4-only commits. No receipt, acknowledgement, answer, owner direction or decision concerns the App v4 handoff, the relay questions, OI-021 or the Domains increment. "Domains" in the App's sense is not found; the only related record is DEC-043 (`SD:648`; `P/AGENTS.md:23-30`) on the `domains/piping-design/` retrieval corpus (prose usable, extracted equations unreviewed and never authoritative).

**X-8. The caller named in SWBPIPE records is "development Codex".** The live-control records name a development Codex session using its command tool (`C24/COORDINATION.md`, "Current agreement"; `C19/PIPING_LIVE_CONTROL_CONTRACT_DRAFT.md` "Purpose"). They do not name the Chirality App v4 or its Codex as a caller.

---

## 2. Per-question facts

### SQ-01 Capture-evidence reference for captured acts (P1)

**Exists on main.** [MAIN]
- The only person's act the product captures on the operation route is **Apply** (single or batch) in the local UI. Its outcome carries an acceptance record with basis, a professional-approval flag set false and a persistence status; there is no act identity, no decision-actor identity, no bound content identity with method designation, and no time field in that record (`APPLIER/lib.rs:123-127`, `:2018-2030`; `DESK/src/types.ts:983-987`).
- The session receipt adds receipt_id, sequence, target, before/after and the applied whole-model hash (`DESK/src/types.ts:1013-1028`). It is in memory only and is lost on restart or project open (X-4; applied and batch receipts are reset on project create and open, `DESK/src/features/workspace/workspaceSession.ts:1789-1792`, `:1859-1862`).
- Surfaces: the desktop UI only. Nothing is readable by an external caller on main.
- There is no rejection record: "Clear pending changes and batches" discards queued batches without a record (`DESK/src/features/toolkit/BatchReviewPanel.tsx:30-38`; OPMAP gap G-18 at `OPMAP:464`, "no rejection record").
- No act-declined event, and no mark-checked, approve, rely or set-grant act exists in the product.

**Designed, planned or in progress (not delivered).**
- [PR885-OPEN] A committed receipt readable through CLI `status`: ticket, workspace, identity {app_instance_id, controller_session_id, workspace_id, project_generation, project_id}, batch_id, operation_ids, origin {actor_type:"agent", source_channel:"local_json_cli", request_id}, acceptance {route:"local_review_apply", identity_verification:"not_performed", professional_approval:false}, before/after {model_revision, model_hash}, publication {undo_checkpoint_id, applied_receipt_id, batch_receipt_id, …}, persistence status (`PR885:DESK/src/features/workspace/liveControlController.ts:508-540`). It names no person, and it does not survive a controller restart (`PR885:P/docs/LIVE_CONTROL_DEVELOPMENT.md:53`, `:57`).
- [DESIGN] The "Checked" mark (DEC-104): human-authored, per row, records who and when and a hash of the row's content; shown stale on content change; set and cleared by the engineer only; kept in project interface state, never in the model payload, a status, an export, a run record or a report (`P/execution/_Coordination/_DECISIONS/D-71_RULING_ADDENDUM_2026-09-18.md`, "Adopted bounded effect"). Gap G-08, not implemented (`OPMAP:457`; no implementation found in `DESK/src`).
- [DESIGN] UX spec rows 211-217 design per-row accept/reject, a rejection record and an accepted record that "survives reopen", all as gap G-18 (`OPMAP:292-298`, `:464`).

**Not decided, and who decides.**
- Final actor identity model: TBD (DEL-16-03 scope `:79`; ledger TBD list). Owner not named beyond the deliverable.
- Storage and invalidation of human acceptance records: `PB-TBD-002`, owner "future persistence/report/governance deliverables" (`P/docs/PROFESSIONAL_BOUNDARY.md:182`). PRD §21.3: any future acceptance record is separate, and the MVP requires no formal acceptance workflow (`P/docs/PRD.md:1340-1344`). `ENGINEER_ACCEPTED` stays reserved with no display form (`P/docs/claims_registry.md:156-159`, `:183-185`).
- Durable receipts for the live route: the contract draft lists "any required durable receipt carrier" as a current hold (`C19/PIPING_LIVE_CONTROL_CONTRACT_DRAFT.md:77`); owner-level choice per that record.
- Checked-mark implementation: needs an owner-authorized tranche (D-71 addendum).

**Elicitation / prompt capture.** Not found as a design. What exists: the PR #885 CLI exposes no Apply or accept method, and Apply is only in the app review UI (`PR885:…/live_control_cli/swbpipe-control.rs:13`). Records state that agent-driven Apply, browser tests and CUA clicks are not human acceptance (`PR885` description; `C19/PIPING_LIVE_CONTROL_CONTRACT_DRAFT.md:47`). MCP elicitation is not addressed anywhere found.

**Not found.** A capture-evidence reference with act identity, actor, kind, bound content, scope, purpose and time; any act-declined event; restart-durable act records. Searched: `APPLIER/`, `DESK/src`, `DESK/src-tauri/src`, `P/schemas/model_operation.schema.json`, `P/core/model_operations/*`, PR #885 head, PKG-16 scope files, OPMAP.

**Terminology.** App A5 "accept" ≈ SWBPIPE "Apply" (the Apply is the acceptance; there is no separate accepted-not-applied state). App A4 "mark checked" ≈ SWBPIPE "Checked" mark, classified as a §16.3 tag, not an acceptance record. App A10 "reject" has no SWBPIPE record on main ("Clear" discards). App A6/A7 have no software counterpart; `OPS-K-AUTH-1` forbids software approval claims (`P/docs/CONTRACT.md:29`).

### SQ-02 Governing checkpoint constraint (P1)

**Exists on main.** Nothing: SWBPIPE has no workflow run, workflow declaration, checkpoint concept, run association or hold machine in the product. Operation intents and batches have no field for a constraint (`P/schemas/model_operation.schema.json`; batch preflight's exact field list `APPLIER/atomic_batch.rs:285-303`). Unknown fields in a batch operation are rejected (`exact_object`, `APPLIER/atomic_batch.rs:213-231`), so an extra constraint field would be refused, not honoured.

**Designed / planned.** Not found. The PR #885 route has no constraint parameter; its params are exact-key objects (`PR885:…/liveControlController.ts:231-233`, `:347-348`).

**Related fact.** On main and in PR #885, **no route applies directly**: every change waits for the person's Apply (X-4, X-6). In App terms, every host operation reached externally is resolved as *propose* today, regardless of any checkpoint. That is a property of the current route, not a checkpoint evaluation.

**Not decided.** Not found as an open item in SWBPIPE records. The App's D6 has no SWBPIPE counterpart.

**Not found.** Options (i)–(iii) for question (a)–(b), "not permitted" naming a constraint (c), host holds before dispatch (d), refusal after an arrival (f). Searched: product source, schemas, PR #885, WG, SD decision log, REG, OPMAP.

**Terminology.** SWBPIPE "checkpoint" means an **undo checkpoint** (session model snapshot, `DESK/src/features/workspace/workspaceSession.ts:1391-1398`) or a work-graph execution checkpoint in development records. Neither is a workflow checkpoint.

### SQ-03 Content identities used to bind acts (P1)

**Exists on main.** [MAIN]
- (a) No. Reads (the model tree, the host `load_preview_model` command) do not return per-row identities; the only identity is the whole-model hash (X-3).
- (b) Not applicable. Nothing is decided about what a support's identity would cover; the App's fixture assumption FXA-2 has no host counterpart.
- (c) An Apply is bound to its operation by id and to the model by the optional claimed whole-model hash plus per-field before-values. The Python audit constructor (unwired) requires a hash-bound diff-preview reference and the current model-state hash (DEL-16-03 REQ-010, `PKG16/DEL-16-03…/ScopeOfWork.md:156`).
- (d) A single-operation outcome names `target_ref`, diff rows and the new whole-model hash (`APPLIER/lib.rs:130-153`). A batch outcome lists each step's `target_ref` and diff rows, plus the final whole-model hash (`APPLIER/atomic_batch.rs:124-143`, `:170-190`). Created objects appear as the target ids of `create_*` operations. There are no per-object post-application identities.
- (e) The whole-model hash is a content hash, so identical model content gives an identical hash value.

**Designed / in progress.**
- [PR885-OPEN] / [MAIN-REC] The live basis adds a model revision that advances on every commit, including Undo. Equal canonical content after Undo does **not** revive an old revision, so an old proposal stays stale (`C19/PIPING_LIVE_CONTROL_CONTRACT_DRAFT.md:45`; `C24/LIVE_MANAGER/WIRE_PROPOSAL.md:58`).
- [DESIGN] The Checked mark binds to "a hash of the row's content" (DEC-104). The hash method and row scope are not specified; not implemented.

**Not decided.** Per-object subject identity: not found as an open item. Row-content hash method for the Checked mark: left to the implementation tranche (G-08).

**Not found.** A subject-identity method designation distinct from the read-level identity. Searched: `APPLIER/`, `DESK/src/types.ts`, `P/schemas/model.schema.yaml`, `P/schemas/model_operation.schema.json`, PR #885.

**Terminology.** App "content identity with method designation" ≈ SWBPIPE `ModelHashEvidence` {algorithm `sha256`, canonicalization `rfc8785_jcs`, payload_scope `model_payload`}. App "subject content identity" has no SWBPIPE counterpart.

### SQ-04 First connected activity: operation, check and environment (P2, OI-021)

**Exists on main.** No selection in response to OI-021 (X-7). Candidate host pieces that exist on main [MAIN]:
- Change operations: 27 change kinds (X-2).
- Non-mutating checks: validate-only preview (`validate_model_operation`, `validate_model_operation_batch`), the mechanics solve (`run_preview_mechanics`, and background `start/poll/cancel_preview_mechanics_job`, `DESK/src-tauri/src/lib.rs:1574`, `:1800-1848`), and user rule-pack checks (`run_rule_checks`, `:2739`), which emit statuses from the six-token vocabulary such as `USER_RULE_CHECKED` (`P/docs/claims_registry.md:171-178`).
- A stable headless CLI `openpipestress-runner` for validate-input, solve, run-benchmark, run-regression and export-results (DEC-065 / D-33; `P/core/runner/headless/src/bin/openpipestress-runner.rs:1-6`; `P/core/runner/headless/src/lib.rs:60-68`). It takes file/stdin requests; it is not connected to the live workspace and does not apply operations.

**Designed / in progress.**
- [PR885-OPEN] [MAIN-REC] The first owner-activated external journey: inspect → preview (no mutation) → submit → **human** Apply in the app → status, using only `Node position.x` modify/set_field, single and ordered atomic batch, on invented fixtures (`C24/OWNER_DECISIONS.md`; `C19/PIPING_LIVE_CONTROL_CONTRACT_DRAFT.md`, "First proof"; `PR885:P/docs/LIVE_CONTROL_DEVELOPMENT.md:39`). An intervening edit expires the proposal as stale (SQ-07). No check operation is exposed on that CLI: the preview is validate-only.
- [MAIN-REC] Later extensions named, not scoped: after the CLI loop, prove the same Codex controller can reach the Windows CAEPIPE UI through Computer Use; only then extend to case preparation, solve/status, result inspection and export for invented-case correlation (`C19/PIPING_LIVE_CONTROL_CONTRACT_DRAFT.md`, "First proof and subsequent extension").
- Expression: SWBPIPE records select a **development Codex controller first, embedded agent later** (X-6). The App's Codex is not named (X-8).
- Environment: macOS only (other hosts return `unsupported_host`); a development desktop started with `SWBPIPE_LIVE_CONTROL=1`; the CLI built with `--features live-control-cli` (`PR885:P/docs/LIVE_CONTROL_DEVELOPMENT.md:9-13`). Candidate: PR head `12907f393`, unmerged. Readiness per the records: implementation reviewed; clean sweep, native I1/I2, human H1/H2 and final review outstanding; deferred to `UI-SUCCESSOR` (X-5).

**Not decided.** Operation, check, autonomy and environment for App v4's OI-021: not found in SWBPIPE records. Resumption of the live-control branch: the owner directs (`WG:60`).

**Not found.** Any SWBPIPE nomination of a first activity for App v4, or an answer to the HANDOFF "Return list". Searched: WG, REG, SD, `C24/`, `C19/`, `P/execution/_Coordination/*.md` notices, `git grep` for App v4 terms.

**Terminology.** App "catalog identity" ≈ SWBPIPE `change_kind` (+ `operation_kind`). App "host-named check" ≈ SWBPIPE rule check / mechanics solve / validate-only preview.

### SQ-05 Policy for the selected operation (P2)

**Exists on main.**
- (a) No human-act classes. Every change needs the person's Apply; the batch envelope hard-codes `requires_user_acceptance: true` and `direct_model_mutation_allowed: false` (`APPLIER/atomic_batch.rs:203-208`; single form `APPLIER/lib.rs:2060-2066`).
- (b) Not found.
- (c) No named reserved-act list. Related rules: FR-AGENT-003; OPS-K-AGENT-4; OPS-K-AUTH-1; DEC-104 (Checked set/cleared by the engineer only; design); `ENGINEER_ACCEPTED` reserved; the activation's "external tools cannot Apply" (X-6). Against the App's five D2 acts: marking checked is engineer-only by design (not implemented); accepting a proposal requires the person's Apply (implemented); engineering approval and professional reliance are not software acts (no acceptance workflow in the MVP); changing an autonomy grant has no counterpart (no grants exist); enabling external access is a launch environment variable, not a captured act (SQ-13).
- (d)–(f) Not found: no settings reference, grant states or consequence vocabulary.
- (g) Main has no withdraw or reject operation; "Clear" discards queued batches. [PR885-OPEN] A person's clear of a published queued proposal is reported as `withdrawn` with reason `cleared_in_review` (`PR885:…/liveControlController.ts:471-473`); there is no agent-side withdraw method, and "Withdrawn by the agent" is host gap G-19 (`OPMAP:297`, `:474`).
- (h) Not applicable: no grants. Apply always revalidates through the engine (SQ-07 (e)).
- (i) Not decided (OI-016).

**Designed / planned.** None beyond the bounded live activation.

**Not decided, and who decides.** OI-016 agent autonomy level: TBD, owner column "PKG-16 / security-privacy / human product decision" (`SD:599`). Unattended or automatic apply is a "separate bounded choice" and a current hold (`C19/PIPING_LIVE_CONTROL_CONTRACT_DRAFT.md:47`, `:77`). DEL-16-06 lists "actor policy" as open (`PKG16/DEL-16-06_Controlled model operation application/ScopeOfWork.md:59`).

**Not found.** Classes, reserved lists, grant display, a settings reference, a consequence vocabulary. Searched: product source and schemas for autonomy, grant, reserved, direct apply; PRD; CONTRACT; SD; REG; OPMAP.

**Terminology.** App "grant / autonomy setting" ≈ SWBPIPE "autonomy level" (OI-016, TBD) and PRD FR-AGENT-003's "another workflow". App "withdrawn" (proposer's act) ≠ PR #885 `withdrawn` (the person cleared the queue).

### SQ-06 Direct application on the external channel (P2)

**Exists on main.** No external channel (X-1).

**Designed / in progress.**
- [PR885-OPEN] The PR description sentence the App quotes is accurate. The CLI's methods are inspect, preview, submit and status only; Apply is available only in the app review UI (`PR885:…/live_control_cli/swbpipe-control.rs:9-13`).
- A direct-apply request is **not a method**. It is refused before transport as `unsupported_method` (`swbpipe-control.rs:65-66`), and the controller answers other methods with `unsupported_method`, "Only inspect, preview, submit and status are supported." (`PR885:…/liveControlController.ts:140`). It is not reported as "not permitted" naming a rule.
- Records describe the no-Apply rule both as a property of the channel ("External operations are inspect/preview/submit/status; no external Apply", `C24/COORDINATION.md`) and as a property of the first journey, with later automatic apply a "separate bounded choice" (`C19/PIPING_LIVE_CONTROL_CONTRACT_DRAFT.md:47`; `C24/OWNER_DECISIONS.md`).

**Not decided, and who decides.** Whether any later external or automatic apply exists: an owner choice per the contract draft's current holds (`:77`) and OI-016.

**Not found.** A class assignment for Node `position.x`, and a host-stated "governing treatment" object. Searched: PR #885 head, `C24/`, `C19/`.

**Terminology.** The App's options (a) class / (b) channel rule / (c) first-increment policy: SWBPIPE records contain wording supporting (b) and (c); none supports (a). Choosing the label is ROOT's or the owner's call.

### SQ-07 Read basis, generation and staleness (P3)

**Exists on main.** [MAIN]
- (a) The host read `load_preview_model` returns the model; hash evidence is computed separately (`computed_model_hash`, `DESK/src-tauri/src/lib.rs:2050-2059`). There is no workspace identity or generation on main.
- (b) Not found on main.
- (c) The offline intake captures the basis **at queue time**: model copy, hash and revision at the moment the batch is queued (`DESK/src/features/workspace/workspaceSession.ts:1046-1057`). A batch may carry `source_model_hash`, which must equal the hash of the initial model at validate/apply (`APPLIER/atomic_batch.rs:95-105`). That is how an earlier plan basis can be carried.
- (d) Whole-model, not per item. A queued batch is marked stale, and its Validate and Apply buttons are disabled, whenever the model revision differs from its basis revision: "The model changed. Prepare a new batch from the current model." (`DESK/src/features/toolkit/BatchReviewPanel.tsx:41-48`). Applying one batch therefore stales every other queued batch. The engine additionally checks per-field before-values.
- (e) Yes. Apply runs the full engine validation again with a claimed hash (X-3), and `handleRunOperationBatch` returns without acting if the revision changed (`DESK/src/features/workspace/workspaceSession.ts:1069-1070`).
- (f) Any model commit (edit, apply, undo, redo, project open/create). Selection changes are not model changes.
- (g) Not found.
- (h) Solve and rule checks run on the current model. Computed results are cleared on any model change (`clearComputedModelState`, `DESK/src/features/workspace/workspaceSession.ts:1462-1464`, `:1493-1502`). Not found: a cited-versus-evaluated basis statement.

**Designed / in progress.**
- [PR885-OPEN] (a) `inspect` returns `basis` (opaque) and `basis_identity` {app_instance_id, controller_session_id, workspace_id, project_generation, project_id, model_revision, model_hash} (`PR885:P/docs/LIVE_CONTROL_DEVELOPMENT.md`, invented exchanges).
- (b) A new workspace id and generation are minted when the published project generation changes (`PR885:…/liveControlController.ts:86-104`). Cross-workspace reuse is rejected even when bytes and revision match (`C19/PIPING_LIVE_CONTROL_CONTRACT_DRAFT.md:43-45`). Archive restore is not addressed.
- (c) The preview freezes the inspected model snapshot, hash and revision, and submit keeps that basis (`liveControlController.ts:231-330`). This differs from main's queue-time capture.
- (d) Still whole-model: `fresh()` fails `stale_basis` if revision or hash changed (`:106-112`), and queued tickets expire with reason `stale_basis` on any revision change (`:453-456`).
- (f) Stale inspection bases are retired, and the controller keeps one current basis (`PR885:P/docs/LIVE_CONTROL_DEVELOPMENT.md:72`).

**Not decided.** Per-item staleness (the App's R2-13): not found as a SWBPIPE item. Multi-read reliance (g): not found.

**Not found.** Archive or generation semantics beyond workspace replacement; per-item stale checks; basis statements on checks. Searched: `APPLIER/`, `DESK/src/features/workspace`, PR #885 controller and doc, the contract draft, WIRE_PROPOSAL.

**Terminology.** App "generation" ≈ PR #885 `project_generation` (workspace replacement counter). App "model revision" ≈ SWBPIPE `model_revision` (in-session commit counter). App "canonical content identity" ≈ `model_hash`.

### SQ-08 Proposal identity and repeated submission (P3)

**Exists on main.** The submitter supplies `batch_id`; `operation_id` and `change_id` must be unique within a batch (`APPLIER/atomic_batch.rs:258-281`). There is no de-duplication across submissions; each queue action adds an entry keyed by a session counter (`DESK/src/features/workspace/workspaceSession.ts:1056`). A proposal's state cannot be read by identity outside the UI.

**Designed / in progress.** [PR885-OPEN]
- (a) Two identities: the controller mints `preview_ref` at preview, before any submission, and the caller supplies a stable `idempotency_key` at submit; the controller returns a `ticket` (`PR885:P/docs/LIVE_CONTROL_DEVELOPMENT.md:41-49`).
- (b) Yes. The key lookup runs **before** the basis check, so a retry recovers the original ticket even after its own commit advanced the revision (`liveControlController.ts:347-360`: `keys.get(key)` precedes `this.fresh(preview)`). The same key with different content returns `idempotency_conflict`.
- (c) No. Associations live in the running controller only; restart or remount expires handles or yields `outcome_unknown`; no durable replay (`PR885:P/docs/LIVE_CONTROL_DEVELOPMENT.md:57`; `C19/LIVE_CONTROL_ACTIVATION_PROPOSAL.md:19`).
- (d) Yes, within the session: `status` by ticket (`:49`).
- (e) Records name the evidence as the committed receipt binding one model/history transition (before/after revision and hash) with one undo checkpoint per batch (`C19/PIPING_LIVE_CONTROL_CONTRACT_DRAFT.md`, "First proof"). Duplicate-submission witnesses are listed as required, not yet performed (X-5).

**Not decided, and who decides.** Durable de-duplication across restart: a current hold, "any required durable receipt carrier" (`C19/PIPING_LIVE_CONTROL_CONTRACT_DRAFT.md:77`); DEL-16-06 retention policy open (`ScopeOfWork.md:59`).

**Not found.** A persisted proposal registry. Searched: `DESK/src/types.ts` envelope, `APPLIER/`, PR #885.

**Terminology.** App "proposal identity" ≈ PR #885 `idempotency_key` (caller) plus `preview_ref` and `ticket` (controller); main `batch_id`.

### SQ-09 Outcome statements, errors and unknown outcomes (P3)

**Exists on main.** [MAIN]
- Single-operation outcome: validation states (schema, reference, unit, before-state, diff preview) and `application_status` ∈ {`not_applied`, `applied_to_session_model`, `blocked`} with coded diagnostics (`APPLIER/lib.rs:1995-2016`).
- Batch outcome: `batch_validation_status`, `application_status` and `simulation_disposition` (X-2).
- Transport status is separate from these outcomes (Tauri `Result`, or a wasm input-error envelope `WASM-ENGINE-INPUT-JSON-INVALID`, `APPLIER/lib.rs:876-947`).
- (b) Atomic: a failed batch applies nothing.
- (c) No durable receipt (X-4).
- (d) Validation failure is a blocking diagnostic; nothing is queued as a record.
- (e) The same engine codes at validate and at apply; apply reports `blocked`.
- (f) One batch = one application and one undo checkpoint.

**Designed / in progress.** [PR885-OPEN]
- Ticket states `queued`, `committed`, `rejected`, `withdrawn`, `expired`, `outcome_unknown` (`PR885:P/docs/LIVE_CONTROL_DEVELOPMENT.md:59`), with reasons such as `validation_rejected` (human Apply's validation failed), `cleared_in_review`, `stale_basis`, `workspace_replaced`, `cancelled_before_publication`, `controller_retired`, `application_publication_pending`, `application_publication_unconfirmed`, `observed_commit_hash_unavailable` (`liveControlController.ts:81-82`, `:398-399`, `:450-497`, `:545-548`).
- Errors: `unsupported_host`, `controller_unavailable`, `stale_basis`, `wrong_workspace`, `unsupported_change`, `idempotency_conflict`, `unknown_preview`, `unknown_ticket`, `busy`, `capacity`, `not_ready`, `expired`, `cancelled_before_publication`, `unauthorized`, `wrong_app`, `frame_too_large`, `invalid_request`, `unsupported_method`, `unsupported_protocol`, `internal_error`, `outcome_unknown` (wire and controller string sets). Each error carries code, message, retryable and next_action.
- A timeout or disconnect "does not prove the proposal never happened" (`:59`). The records ask that queued/committed be reported only on observed publication, never on engine success or scheduled React state (`C19/PIPING_LIVE_CONTROL_CONTRACT_DRAFT.md`, "Publication and cancellation boundary").

**Not decided.** Durable receipts (SQ-08).

**Not found.** Partial application with receipts (atomic only). An "application error" distinct from a validation refusal at apply: at apply, a failure is `rejected: validation_rejected` in PR #885 and `blocked` on main.

**Terminology.**

| App term | SWBPIPE term |
|---|---|
| refused (invalid) | `blocked` / blocking diagnostics |
| refused (stale) | `OP-STALE-BEFORE-VALUE`, `OP-CLAIMED-MODEL-HASH-MISMATCH`, `stale_basis`, `expired` |
| queued | `queued` (PR #885, only after observed publication) |
| applied with receipt | `applied_to_session_model` / `committed` |
| rejected | no main record; PR #885 `rejected` means the engine rejected at Apply, not a person's rejection |
| withdrawn | PR #885 `withdrawn` = the person cleared the queue |
| channel not enabled | no code; appears as `controller_unavailable` or an attachment failure |
| not exposed on this surface | `unsupported_change` / `unsupported_method` |
| outcome unknown | `outcome_unknown` |

### SQ-10 Undo and publication (P3)

**Exists on main.** [MAIN]
- Undo and Redo are session stacks of whole-model snapshots, up to 25 deep. Undo restores the prior snapshot, clears computed results and says Save is still required (`DESK/src/features/workspace/workspaceSession.ts:1447-1468`, `:1470-1489`).
- Undo is **not** an operation through the engine; it produces no receipt and no link to the reversed receipt. Treatment is not policy-governed: it is a UI control available to the person. The stacks are cleared on project open or create (`:1787`, `:1857`).
- A batch is one undo checkpoint (`OPMAP:293`, `App.tsx` one checkpoint per batch).

**Designed / in progress.**
- [PR885-OPEN] The receipt records `undo_checkpoint_id` (`liveControlController.ts:538-543`). Undo is not exposed on the CLI. Undo advances the revision even when content returns to an earlier state (`C24/LIVE_MANAGER/WIRE_PROPOSAL.md:58`).
- [DESIGN] UX row 217 "Undo while reversible" in the accepted record (G-18).

**Publication.** SWBPIPE uses "publication" in two unrelated senses: (1) in PR #885, a controller-observed queue or commit becoming visible in the live UI state ("published", `cancelled_before_publication`); (2) in governance, public-repository release gates (`P/docs/PRD.md:1356`). Neither changes the standing of an applied change.

**Not decided.** Not found as an open item.

**Not found.** A reversal receipt; undo scope beyond whole-snapshot restore; undo across restart. Searched: `workspaceSession.ts`, `operationsSessionState.ts`, `APPLIER/`, PR #885.

**Terminology.** App "undo route / reversal receipt" ≈ SWBPIPE session "Undo" (snapshot restore, no receipt). App "publication" has no SWBPIPE equivalent.

### SQ-11 Exposure per surface and entries offered (P3)

**Exists on main.** No per-surface exposure element exists. The toolkit capability catalog is the UI vocabulary (SCA-009), with `status` ∈ supported / partial / unavailable / gated, describing executable UI routes only (`DESK/src/features/toolkit/capabilityCatalog.ts:10-22`). The offline-authoring reference exports that catalog plus the operation schema and a provider status (`DESK/src/App.tsx:493-497`; `OfflineProposalIntakePanel.tsx:41-46`).

**Designed / in progress.** [PR885-OPEN] The one entry offered on the CLI is Node `position.x` modify/set_field in the inspected length unit, as the `supported` block of `inspect` and `describe` (`PR885:…/swbpipe-control.rs:16-20`). Everything else is refused as `unsupported_change`.

**Not decided.** Not found as an open item.

**Not found.** Any "exposed on surface X" field, and any embedded-tool surface. Searched: capabilityCatalog.ts, schemas, PR #885.

**Terminology.** App "catalog entry exposure" ≈ nothing. The closest analogues are the toolkit capability `status` (UI only) and PR #885's `supported` object.

### SQ-12 External seam and native surface derivation (P4)

**Exists on main.** None (X-1).

**Designed / in progress.**
- [PR885-OPEN] The seam is a local JSON CLI `swbpipe-control`, invoked through Codex's existing command tool (`C24/COORDINATION.md`).
- [MAIN-REC] MCP is not selected. It may be a later thin adapter only if the actual Codex client meets the owner's modern stateless 2026-07-28 condition; the tested bundled Codex (0.155.0-alpha.9.2) used a 2025-06-18 handshake and failed that qualification (`C19/PIPING_LIVE_CONTROL_CONTRACT_DRAFT.md`, "Transport and ownership", "Modern MCP condition"; `C24/COORDINATION.md`, evidence PR #827).
- Derivation: hand-built and narrow. The preview calls the same atomic engine (`validateOperationBatch`) as the UI (`liveControlController.ts:320-323`); the CLI's method set is fixed in code, not generated from a catalog.

**Not decided, and who decides.** Any MCP adapter: the owner's condition. If the client speaks only legacy MCP, "return the transport choice to the owner" (contract draft, "Modern MCP condition").

**Not found.** A tool-to-catalog mapping with operation identity and version. Searched: PR #885 head, `C19/`, `C24/`.

**Terminology.** App "external interface" ≈ SWBPIPE "live control" / "development live control carrier" / "local JSON CLI". The source role value is `external_agent_proposal`.

### SQ-13 Enablement behaviour of external access (P4)

**Exists on main.** None.

**Designed / in progress.** [PR885-OPEN]
- Off by default: normal startup unchanged, and the bridge is disabled without the exact opt-in (`PR885:P/docs/LIVE_CONTROL_DEVELOPMENT.md:13`).
- The "opt-in" is a **launch environment variable** `SWBPIPE_LIVE_CONTROL=1` on the development desktop, and the CLI binary is a **build feature** `live-control-cli`, excluded from normal packaging (`:9-13`, "Development checks and boundaries").
- When off there is no descriptor and no socket, so the CLI fails at attachment or connect (`controller_unavailable`, `swbpipe-control.rs:76-106`); non-macOS hosts return `unsupported_host`. There is no explicit "channel not enabled" code.
- Enablement state readable over the interface: not found.
- Disable while proposals are queued: not found. Restart expires handles or reports `outcome_unknown`.

**Not decided.** Not found as an open item.

**Not found.** A person's enablement act or its record (see SQ-28). Searched: PR #885, WIRE_PROPOSAL, activation proposal.

**Terminology.** App A13 "enable external access" ≈ SWBPIPE `SWBPIPE_LIVE_CONTROL=1` (an environment variable, not an act).

### SQ-14 Origin and caller identity (P4)

**Exists on main.** [MAIN]
- Batch operations must carry `author_type` ∈ {user, agent}; agent operations require `source` {source_ref, source_channel, source_role} (`APPLIER/atomic_batch.rs:322-341`).
- The schema allows `user`, `agent`, `import_adapter`, `project_template`, `TBD` (`P/schemas/model_operation.schema.json:306`).
- The batch envelope states `source_identity_verification: "not_performed_asserted_metadata_only"` and `agent_runtime_binding: "held_D58"` (`APPLIER/atomic_batch.rs:207-208`).
- Offline intake: attribution is file-supplied and not verified (`OfflineProposalIntakePanel.tsx:26`).

**Designed / in progress.** [PR885-OPEN]
- The controller assigns `author_type:"agent"` and `source` {`source_ref: local_json_cli:<controller session>:<request id>`, `source_channel: local_json_cli`, `source_role: external_agent_proposal`}; caller-supplied author, source and acceptance fields are rejected (`liveControlController.ts:246-258`; `LIVE_CONTROL_DEVELOPMENT.md:39`).
- None of these is verified: "not verified Codex identity", and MCP clientInfo "is not authentication" (`C24/LIVE_MANAGER/WIRE_PROPOSAL.md:9`; `C19/PIPING_LIVE_CONTROL_CONTRACT_DRAFT.md:49`).
- Authentication: a random local capability in a 0600 descriptor inside a 0700 private directory; the native side validates the app and registration identity (`LIVE_CONTROL_DEVELOPMENT.md:13-15`).
- Multiple callers: any holder of the descriptor. The native side admits up to 16 connections or requests (`:61-70`, limits table).
- Conversation and workflow run: not recorded. The receipt's `origin.request_id` identifies the preview invocation (`:53`).

**Not decided.** The final actor identity model is TBD (X-4).

**Not found.** Verified identity; conversation or workflow-run origin elements.

**Terminology.** App "origin mark" ≈ SWBPIPE `author_type` + `source` {source_ref, source_channel, source_role}; the receipt `origin` {actor_type, source_channel, request_id}.

### SQ-15 Locality and sandbox reach (P4)

**Designed / in progress.** [PR885-OPEN] Strictly local: a macOS Unix domain socket and descriptor in a randomly named private directory under the macOS system temporary directory (`private/tmp`) (directory 0700, entries 0600); no network listener; native event permission limited to listen/unlisten on the main webview (`LIVE_CONTROL_DEVELOPMENT.md:13-15`; `DESK/src-tauri/capabilities/live-control.json`).

**Not found.** Whether a Codex sandbox needs, or is granted, access to the socket or descriptor path: no record addresses it. Searched: PR #885 docs and source; `AR/` records for "sandbox" together with socket, CLI or Codex (hits concern agent write scopes, not socket reach).

### SQ-16 Host restriction of its own channel by model destination (P4)

**Exists on main.** No external channel.

**Designed / in progress.** [PR885-OPEN] The wire has no destination field and no destination-based refusal (wire and controller string sets).

**Related governing record.** [MAIN-REC] DEC-051 / D-24 open residency: for the **embedded agent's** model-provider channel, the app does not enforce residency and adds no guard, opt-in gate or indicator (X-6). This record does not address the external CLI channel.

**Not decided.** Not found as an open item.

**Not found.** Any host restriction by caller model destination. Searched: PR #885, `C19/`, `C24/`, SD, SPEC §4.4, CONTRACT.

### SQ-17 Receiving App workflows (P5)

**Exists on main.** None. The product has no workflow library, no workflow reader and no declaration parser. No `.chirality/`, `workflows/`, `instructions/`, `.agents/` or `skills/` tree exists under `P/` outside execution records (`git ls-tree` of `P/` at main).

**Designed / planned.** Not found for the product. The piping development loop uses Root workflows (for example `construct-local-work-graph`, `WG:10`); that is development process, not product.

**Not decided.** Not found as an open item. Later embedded adoption is planned as a separate scope (SQ-20).

**Not found.** (a)–(d) entirely. Searched: `P/` tree, product source, WG, SD, OPMAP.

**Terminology.** App "workflow" ≠ SWBPIPE product "workflow". In product code and tests, "workflow" means a user journey (for example `DESK/src/features/offline-proposal-intake/workflows.test.tsx`); in records it means Root development workflows.

### SQ-18 Adaptation, host workflows and library identity (P5)

**Exists on main.** No host workflows, no library identity and no adaptation. No version-compatibility statements between operation versions; there is one crate version (X-2). A request naming an entry version: not applicable, because intents carry no operation version.

**Not found.** (a)–(e). Searched as for SQ-17.

### SQ-19 Host run records and supplied guidance (P5)

**Exists on main.** No host loop, so no per-turn guidance records. SWBPIPE "run records" are analysis (solver) run records (DEL-14-02; `P/schemas/analysis_run*.schema.json`), not agent runs.

**Designed / planned.** [DESIGN] The UX spec designs one agent column with Conversation, Proposals, Checks and Accepted tabs (`OPMAP:289`, row 208); persistence of that column is gap G-17 (`OPMAP:463`).

**Not found.** (a)–(c); and (d) any "seat" or role-meaning concept. The question's premise that SWBPIPE "has a single agent seat" is not established by SWBPIPE records: no embedded agent exists, and the design has one agent panel. Searched: product source, OPMAP, WG, SD.

### SQ-20 Host-side placement (informational) (P5)

**Exists on main.** No loop and no hold machine. PR #885's placement [PR885-OPEN]: native bridge in Rust (`DESK/src-tauri/src/live_control.rs`); controller registry in the frontend (`liveControlController.ts`); domain validation in the shared engine.

**Designed / planned.**
- [PLANNED] `RUNTIME-ADOPT — later embedded Runtime` (`WG:123`): a companion task owns Runtime/App configuration. It requires "immutable catalog registration before first turn", rebind/resume and descendant qualification, with the modern MCP condition if selected; "live Piping integration unqualified".
- [MAIN-REC] Later embedded adoption also needs an owning authenticated host client, handler rebind after restart, no replay and a separate adoption brief (`C24/COORDINATION.md`, "Existing and later dependencies").
- Historical placement: a Node Agent-SDK sidecar (DEC-041), whose current reliance is retired by D-58 / DEC-091.

**Not decided, and who decides.** The successor embedded mechanism is unresolved under D-58 (owner). The UX design names a persisted agent column (G-17). The checkpoint hold machine and required-tool check: not found.

### SQ-21 Host faithful-record operation (P6)

**Exists on main.** No. The only related constructors are the unwired Python audit record (DEL-16-03), which records user decisions and holds agent-only acceptance, and the DEL-16-04 agent-rationale record, which binds agent reasoning metadata as decision support and does not accept work (`P/core/model_operations/agent_rationale/engine.py:1-24`). Neither is a host operation available to agents.

**Not found.** An operation storing an agent's faithful record of a person's act. Searched: product source, schemas, PKG-16 scopes.

### SQ-22 Proposal views (P6)

**Exists on main.** [MAIN]
- Operations section, Review tab: **Batch review** shows each queued batch, its step diff rows (`field_path: before → after`), diagnostics and the submitted JSON including rationale and source (`DESK/src/features/toolkit/BatchReviewPanel.tsx:24-84`).
- Other views: Operation apply panel; Operation ledger (session actor and decision counts, `DESK/src/features/operations/OperationLedgerPanel.tsx`); Diff preview panel (`DESK/src/features/diff-preview/DiffPreviewPanel.tsx`); the sample Agent proposal panel (review-only).
- Referencing: internal DOM element and test ids only (for example `batch-review`, `batch-<key>`, used by the toolkit focus route). There is no stable external reference scheme.

**Designed.** [DESIGN] Proposal cards with banded rows, and ghosts in tables and canvas (`OPMAP:291`, G-18, G-16).

**Not found.** A panel-referenceable position scheme.

### SQ-23 Display of lapse, supersession, stale-after-acceptance, reversal (P6)

**Exists on main.** [MAIN]
- A stale batch shows "The model changed. Prepare a new batch from the current model." (`BatchReviewPanel.tsx:42-43`).
- Undo shows "Undid <op> in the local session; previous solve results were cleared…" (`workspaceSession.ts:1466`); nothing persistent.
- Grant supersession: not applicable. "Accepted, not applied, stale": not applicable on main, because Apply is the acceptance.

**Designed.** [DESIGN]
- Checked-mark stale wording "the row changed since · Check again or Clear" (DEC-104).
- Stale-proposed row with "superseded by" (`OPMAP:295`, G-18).
- Stale runs kept readable on Historical terms (G-11).

**Not found.** A reversal marker.

### SQ-24 Where agent examination findings are held (P6)

**Exists on main.** No findings storage.

**Designed.** [DESIGN] Agent cards on the Review page and a Checks tab carrying "Check", "Open issue" and "Evidence summary" by reference, with open / resolved states, persisted with the project: gaps G-19 and G-21 (`OPMAP:301`, `:466`, `:474`). DEC-103 item 8 fixes five class words for agent cards: "Check", "Open issue", "Draft", "Proposal", "Evidence summary" (`SD:708`).

**Not decided.** Whether storing a finding is a change through the operation route: not found.

**Terminology.** The SWBPIPE agent-card class word "Check" ≠ the Checked mark ≠ App A4. The nearest carrier named is `StateNote` (G-21).

### SQ-25 Acts on host content captured through the App (P6)

**Exists on main / designed.** Records say the bridge or controller assigns actor = agent and records the actual human acceptance separately in the app; external tools cannot Apply; CUA clicks are not human acceptance (`C19/PIPING_LIVE_CONTROL_CONTRACT_DRAFT.md:47-49`; `C24/OWNER_DECISIONS.md`).

**Not found.** Any proxy control or App-captured act on host content. Searched: `C19/`, `C24/`, PR #885.

### SQ-26 The one new operation for the catalog-extension trace (P7)

**Exists on main.** No catalog editions, and no edition-addition event.

**Designed.** [DESIGN] Engine and typed-interface gaps list candidate additions (for example G-01 node renumbering, G-02 translate-chain; `OPMAP:436-469`). None is selected for an extension trace.

**Not found.** A selected operation; per-surface generated / checked / hand-built statements; participation in the App's OI-003. Searched: OPMAP, WG, SD, REG.

**Terminology.** ID collision: App **OI-003** (extension disposition) ≠ SWBPIPE **OI-003** (legal review of public component and material data, `SD:585`).

### SQ-27 Candidates, host examination evidence and relay of returns (P7)

**Exists on main.** [MAIN-REC] SWBPIPE identifies candidates by commit SHA and PR merge commit, hosted CI run ids, the DEC-025 five-surface local sweep, native witness records and executable hashes, kept under `AR/…/_run_records` with custody JSON (for example `WG:101-103`; `C24/COORDINATION.md`). Checks include the operation contract corpus (81 invented cases, `P/fixtures/model_operations/contract_corpus/`) and PR #885's focused live-control tests (`LIVE_CONTROL_DEVELOPMENT.md`, "Development checks").

**Designed / in progress.** [PR885-OPEN] [PLANNED] Actual-human witnesses H1/H2 on invented material are required, and LIVE-HUMAN is "BLOCKED until live implementation and owner participation" (`WG:121`), deferred to UI-SUCCESSOR.

**Not decided.** The next App-side decision or input SWBPIPE needs: not found (X-7).

**Not found.** A relay form agreed with the App.

### SQ-28 Enablement facility for A13 and its capture-evidence reference (P4)

**Exists / designed.** None on main. In PR #885, enablement is the environment variable (SQ-13). No person's act is captured, no reference exists, the state is not readable over the interface, and disabling is not recorded.

**Not decided.** Not found as an open item.

**Not found.** Searched: PR #885, WIRE_PROPOSAL, activation proposal and contract draft, OPMAP.

### SQ-29 The host loop's model interface and fixture basis (P8)

**Exists on main.** None (X-1).

**Designed / planned.**
- [MAIN-REC] Historical: Claude Agent SDK in a Node sidecar (DEC-041), retired as current reliance (D-58).
- Owner-reported local model availability "oMLX" on the Mac, with "I may change the model". A later authorized check records the actual model, with "no silent cloud fallback" (`C19/OWNER_CLI_PROTOCOL_DISPOSITION_PEER_2026-09-20.md`).
- Peer-reported: local-agent operation central to a premium feature after the MVP (same record).

**Not decided, and who decides.** Interface, server, version and recorded-exchange fixtures: not selected. The embedded mechanism is unresolved under D-58 (owner); RUNTIME-ADOPT is planned (`WG:123`).

**Not found.** Tool-call, truncation and malformed-output handling; recorded exchanges. Searched: product source (X-1), WG, `C19/`, `C24/`.

### SQ-30 Endpoint and key boundary in the host's native layer (P8)

**Exists on main.** No endpoint configuration and no key custody. `api_key` appears only as a key name to redact in exports and telemetry (X-1).

**Governing records.** [MAIN-REC]
- DEC-051 / D-24 open residency (X-6): owner-configured provider "local, Anthropic, or other"; no guard, gate or indicator. SPEC §4.4 lists "key management, secret storage, provider/egress configuration surfaces" as separate TBD decisions (`P/docs/SPEC.md:386-390`).
- The fence F-PIP-1 reads "local-only operation — no cloud…" but remains subject to owning rulings (`P/loop/WORKPLAN_2026-07-18b_piping_loop.md:161-164`; `P/AGENTS.md:34-40`), and DEC-051 amended the runtime posture.

**Not decided, and who decides.** Endpoint enforcement layer, local default, fallback, the definition of "user-controlled local", permitted cloud destinations, tool traffic: all not decided. DEC-051 revisiting is "a human decision"; key management and egress surfaces are TBD (SPEC §4.4).

**Not found.** (a)–(e). Searched: product source, SPEC, CONTRACT, SD, `C19/`.

### SQ-31 Malformed and truncated tool calls; validation order (P8)

**Exists on main.** No loop. The analogous engine-side facts [MAIN]:
- Strict batch preflight: exact object keys; required fields; unknown fields rejected; `operation_status` must be `proposed`; unsupported kinds refused. This runs before engine simulation (`APPLIER/atomic_batch.rs:39-48` runs preflight first; rules at `:213-360`).
- Malformed JSON into wasm returns a structured error envelope, "never a silent fallback" (`APPLIER/lib.rs:876-947`).

**In progress.** [PR885-OPEN] Unknown or missing params are refused (`invalid_request`, `liveControlController.ts:19-22`). Changes outside Node `position.x` are refused (`unsupported_change`). There is no repair or defaulting.

**Not found.** Sibling-call handling (c) and held-at-checkpoint (d).

### SQ-32 Responsiveness during loop work (P8)

**Exists on main.** No loop. Solve runs as a background job with poll and cancel (`DESK/src-tauri/src/lib.rs:1800-1848`). Performance acceptance criteria exist for the redesigned UI (D-72, `REG:109`), not for agent streaming.

**Not found.** Placement of streaming and parsing, stream cancel, relayed observations, and a numeric criterion (R-OPEN-1). Searched: WG, REG, SD, product source.

---

## 3. Items that look like owner decisions (per SWBPIPE records)

| Item | Record | Bears on |
|---|---|---|
| Agent operation autonomy level (grants, classes, direct apply) | OI-016, `SD:599` ("human product decision") | SQ-05, SQ-06 |
| Later automatic or unattended apply; durable receipt carrier | Contract draft current holds, `C19/PIPING_LIVE_CONTROL_CONTRACT_DRAFT.md:77` | SQ-06, SQ-08, SQ-09 |
| When UI-SUCCESSOR (including live control) resumes | `WG:60` | SQ-04, SQ-12…SQ-15, SQ-27 |
| Actual-human witnesses H1/H2 (owner participation) | `WG:121` | SQ-27, SQ-01 |
| Any MCP adapter (modern-client condition) | `C19/OWNER_CLI_PROTOCOL_DISPOSITION_PEER_2026-09-20.md` | SQ-12 |
| Successor embedded-agent mechanism | D-58 / DEC-091, `REG:95`, `SD:696` | SQ-19, SQ-20, SQ-29…SQ-32 |
| Revisiting open residency | DEC-051, `SD:656` | SQ-16, SQ-30 |
| Checked-mark implementation tranche | D-71 addendum (DEC-104) | SQ-01, SQ-03, SQ-05 |
| Acceptance-record storage (PB-TBD-002) | `P/docs/PROFESSIONAL_BOUNDARY.md:182` | SQ-01 |

## 4. Facts that contradict or qualify assumptions in the question file

1. **Direct-apply refusal form (SQ-06).** The App expects a direct external request to return *not permitted* naming the rule. In PR #885, Apply is not a method, and a request for it returns `unsupported_method`.
2. **Per-item staleness (SQ-07 (d); App ruling R2-13).** SWBPIPE stales or expires proposals on **any** whole-model revision change, on main (`BatchReviewPanel.tsx:42`) and in PR #885 (`liveControlController.ts:106-112`, `:453-456`). Applying one proposal makes every other queued proposal stale.
3. **Subject identities (SQ-03).** There is no per-row or per-object content identity; only the whole-model hash. The only per-row hash is designed, for the Checked mark, and not implemented.
4. **"Opt-in" (SQ-13, SQ-28).** It is a launch environment variable plus a build feature, not a person's captured act. No "channel not enabled" code exists, and the enablement state is not readable.
5. **Queue-time basis (HOST_INTEGRATION §11; SQ-07 (c)).** True on main's offline intake (`workspaceSession.ts:1046-1057`). PR #885 freezes the inspected basis instead, but that is unmerged.
6. **Caller identity (all P4).** SWBPIPE records name "development Codex", not the App's Codex (X-8).
7. **Embedded direction (SQ-20, SQ-29).** SWBPIPE records plan a later "embedded Runtime" adoption (Chirality Runtime; `WG:123`). D-58 keeps Piping outside the Runtime and App-harness client sets with the successor unresolved. The App HANDOFF's "minimal host loop" does not appear in SWBPIPE records.
8. **Local-only expectation (SQ-30; V4-HOST-02).** SWBPIPE's DEC-051 rules open residency with no app-side guard, gate or indicator for an owner-configured provider, including cloud.
9. **"Single agent seat" (SQ-19 (d)).** Not established by SWBPIPE records. There is no agent; the design has one agent panel.
10. **"withdrawn" (SQ-05 (g), SQ-09).** In PR #885 this is the person clearing the queue, not the proposer withdrawing.
11. **PR #885 readiness.** Its description's "reconfirmed proceeding" predates the work graph's deferral of LIVE-* to UI-SUCCESSOR (2026-09-25 route direction), which governs.
12. **HOST_INTEGRATION §11 "Runtime catalog/binding/call transport".** No Runtime or harness binding exists in the piping product on main. The Runtime application tools live in the Runtime project (PR #824, per `C24/COORDINATION.md`).

## 5. Terminology map (App → SWBPIPE)

| App concept | SWBPIPE name(s) | Note |
|---|---|---|
| Human act A5 accept | "Apply" (review Apply); `acceptance_basis: user_initiated_apply_in_local_session`; PR #885 `acceptance.route: local_review_apply` | Apply is the acceptance |
| A4 mark checked | "Checked" mark (DEC-104; PRD §16.3 tag) | Not an acceptance record; not implemented (G-08) |
| A10 reject | none on main ("Clear" discards); DEL-16-03 Python status `rejected` | PR #885 `rejected` = engine rejection at Apply |
| A6 approve / A7 rely | none; `ENGINEER_ACCEPTED` reserved; OPS-K-AUTH-1 | No acceptance workflow in the MVP |
| A12 grant / autonomy | "autonomy level" (OI-016, TBD); FR-AGENT-003 "another workflow" | No grants exist |
| A13 enable external access | `SWBPIPE_LIVE_CONTROL=1` (PR #885) | Not an act |
| Workflow checkpoint | none; "checkpoint" = undo checkpoint or work-graph checkpoint | — |
| Receipt | `AppliedOperationReceipt`, `BatchReceipt` (session); PR #885 committed receipt; also solver source receipts (`P/core/product_physics/src/source_receipt.rs`), save receipts, loop receipts | Multiple unrelated meanings |
| Content identity + method | `ModelHashEvidence` {sha256, rfc8785_jcs, model_payload}; `claimed_model_hash`; `source_model_hash`; PR #885 `basis_identity` | Whole-model only |
| Catalog entry | `change_kind` / `operation_kind`; toolkit capability (UI vocabulary); `OperationSet` schema | No per-entry identity + version |
| Surfaces | desktop UI (native Tauri and browser wasm routes); no embedded tools; PR #885 CLI | — |
| Proposal | operation batch / editor intent (`operation_status: proposed`); `AgentProposal` (sample); PR #885 preview/ticket | — |
| Proposal identity | `batch_id`; PR #885 `idempotency_key` + `preview_ref` + `ticket` | — |
| Origin | `author_type` + `source` {source_ref, source_channel, source_role} | Unverified |
| Host-named check | rule check (`USER_RULE_CHECKED` / `USER_RULE_FAILED`), mechanics solve, validate-only preview | ≠ agent-card class word "Check" |
| Lapse | "stale" | — |
| Embedded loop | "embedded agent" (SPEC §4.4), "embedded Runtime" (WG), "live agent binding" (G-19) | — |
| External channel | "live control", local JSON CLI `swbpipe-control` | — |
| Generation / revision | PR #885 `project_generation` / `model_revision` | — |
| Decision ids | App D2/D5/D6, OI-003, OI-021 | SWBPIPE D-nn, DEC-nnn, OI-nnn are separate namespaces; OI-003 collides |
| "captured" | SWBPIPE "captured entry" / "typed entry" are **solver invocation entries** | Not act capture |

## 6. Search log (where "not found" was searched)

- Product source at main: `P/apps/desktop/src`, `P/apps/desktop/src-tauri/src`, `P/core/**`, `P/api/api_boundary_contract.yaml` (transport and endpoint fields all `TBD`), `P/schemas/*`, `P/tools/*`. Searched with `/usr/bin/grep -rniw` for mcp, openai, ollama, llama, llm, api_key, completions, codex, autonomy, grant, reserved, direct apply, capability reference, operation catalog, Checked, receipt, undo.
- Records at main: WG (all 416 lines, every row), REG (all rows D-05…D-78 scanned; D-22, D-24, D-30, D-31, D-58, D-60…D-78 read), SD §12 decision log and OI table, `C24/` (OWNER_DECISIONS, COORDINATION, OWNER_ROUTE_DIRECTION, DESIGN_MANAGER/RETURN, LIVE_MANAGER/*), `C19/` (the contract draft rev 3, the activation proposal rev 2 and owner direction records), OPMAP (sections M and the gap list), D-71 ruling addendum, PKG-16 scopes (DEL-16-03, DEL-16-06, and DEL-16-04 status), PRD, SPEC, CONTRACT, claims registry, PROFESSIONAL_BOUNDARY, `P/AGENTS.md`, loop fences.
- `git grep` over `P/` at main for app-v4, App v4, HTML-D05, OI-021, HANDOFF_SWBPIPE, RELAY_QUESTIONS, chirality-app-v4 and Domains.
- GitHub (read only): `gh pr view 885` (metadata and body), `gh pr diff 885 --name-only`. PR head files were read locally at `12907f393`.
