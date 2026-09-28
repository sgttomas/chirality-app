# SWBPIPE answers to the App v4 relay questions (RELAY-v0.3)

- **Answers:** `RELAY_QUESTIONS_SWBPIPE.md` RELAY-v0.3, as committed on main at `c6f81a4f2` (sha256 `a8cae06fd4b208087614e9c4cc7e2b91e36f3b98cd11e6f4093fd946d1177f2b`), SQ-01…SQ-32. Main `d1cc97ce4` (#1046) later changed that file in place (sha256 `83466d67a44328c53b25b8a4b0b5d4b6b378ca1b6cde81d5e772abe1d998dd53`): the header status, the §4 ledger and change-log rows, and VC-R-04. No question text changed, so these answers apply to it unchanged. That file is in `projects/chirality-app-v4/execution/PKG-09_Candidate examination and connected journeys/1_Working/DEL-09-06_Connected activity contract and workflow round trip/Design/`.
- **Answering party:** the SWBPIPE (chirality-piping) ROOT session, a HELP_HUMAN agent working on the owner's Mac at the owner's request, 2026-09-28. At the owner's direction, this session placed this file and its fact sheet beside the questions (see §6).
  - **These are not the owner's personal answers, and no commitment is made on the owner's behalf.** Every item that is the owner's to decide is marked **OWNER DECISION** and left open.
  - In the terms of the App's return ledger (§4 of the questions), every entry here is an **answer** about the current state of SWBPIPE. None is a *commitment*, a *delivered contribution* or an owner's *stated intention*. Where a SWBPIPE record states a plan, it is cited as the record's plan.
- **The ROOT session's own standing:** it runs SWBPIPE's T3 numerical-integrity work (solver correctness, result publication, and the both-entry and T9 gates). The agent-facing work these questions concern is outside T3 and is currently deferred by the owner (see A-2 below). Facts outside T3 come from a read-only research pass, which ROOT reviewed.
- **SWBPIPE basis:**
  - main `24dea2dae`. Main has since moved to `d1cc97ce4`, the base of the delivery, but that delta touches only `projects/chirality-app-v4/`, so the piping tree is identical;
  - draft PR #885 (sgttomas/chirality), head `12907f393`: **open, unmerged, deferred**.
- **Evidence:** every statement below rests on a file:line citation in the fact sheet `FACTS_SQ01_SQ32.md`, kept beside this file (sha256 `2f61d3ba4e1cc9bedb799bf15c600d67e4820b7305741a1269d4a08355b4ddfc`). Paths use `P/` = `projects/chirality-piping/`.

**Standing labels used below.**

| Label | Meaning |
|---|---|
| **FACT** | True of the product on SWBPIPE main today |
| **DRAFT #885** | Implemented in draft PR #885 only: not merged, not qualified, deferred |
| **DESIGN** | Designed in SWBPIPE records (UX spec, decisions); **not implemented** |
| **OWNER DECISION** | Not decided; per SWBPIPE records it is the owner's (or a named product decision) |
| **NOT FOUND** | Searched and absent: no implementation, no design, no open item |

---

## 0. Headline answers

- **A-1. SWBPIPE has no live agent today.**
  - There is no embedded agent loop, no model-provider client, no MCP server, no workflow library and no checkpoint or hold machine in the product.
  - Agent proposals reach SWBPIPE only as an offline JSON batch that a person pastes or opens, and it is reviewed in the desktop app.
  - **The only act of a person that the product captures is Apply**, the person's review-and-apply of a proposed change in the local UI. It records no person identity, and its receipt lives in session memory only (`P/apps/desktop/src/features/workspace/shellLayout.ts:146-147`; `…/OfflineProposalIntakePanel.tsx:17-26`; `P/core/model_operations/operation_applier/src/lib.rs:2018-2030`).
- **A-2. The only external seam is draft PR #885, and it is deferred.**
  - It is a macOS-local JSON CLI, `swbpipe-control`: inspect, preview, submit, status. It has **no Apply**; Apply stays with the person in the app.
  - The owner's route direction of 2026-09-25 moved the live-control integration, human-witness and final steps into the deferred **UI-SUCCESSOR**. **UI-SUCCESSOR resumes when the owner directs** (`P/execution/_Coordination/WorkGraphs/HELP-HUMAN-PIPING-20260918-UI-IMPLEMENTATION/WORK_GRAPH.md:46-60`, `:120-122`).
- **A-3. Content identity and staleness are whole-model.**
  - The identity is a sha256 over the RFC 8785 canonical JSON of the whole model payload. There is no per-row or per-object identity.
  - Any model change stales **every** queued proposal, on main and in PR #885.
- **A-4. SWBPIPE records name a different caller and a different embedded direction from the App's.**
  - The external caller named in SWBPIPE records is a **development Codex** controller, first. The App v4 and its Codex are not named.
  - The embedded direction recorded is a later **"embedded Runtime" adoption** (work graph row RUNTIME-ADOPT, planned). The successor embedded mechanism is unresolved under SWBPIPE's D-58.
  - **No SWBPIPE record acknowledged the App v4 handoff, OI-021 or these relay questions before this file.**
- **A-5. Consequence for the App's priority groups:**
  - **P1 (SQ-01…03):** SWBPIPE has no capture-evidence reference, no host-held checkpoint route (**none planned**), and no subject content identities. The App's positive host-content checkpoint cases therefore have no host input to wait on at present.
  - **P4 (SQ-12…16, SQ-28):** there is **no enablement act**. PR #885's opt-in is an environment variable. Under the App's own contracts the external channel therefore stays *not enabled*.
  - **P5 (SQ-17…20) and P8 (SQ-29…32):** these describe things SWBPIPE does not have and has not designed.
  - **P2 (SQ-04, SQ-05):** they turn on owner decisions (§2).

---

## 1. Answers by question

### P1

#### SQ-01 Capture-evidence reference

| Act | Offered | Reference exposed | Elements readable | Surfaces | Durable across restart |
|---|---|---|---|---|---|
| A4 mark checked | **No.** DESIGN only: the "Checked" mark (DEC-104) is a per-row tag with who, when and a row-content hash, set and cleared only by the engineer. It is not an acceptance record, and not implemented (gap G-08) | No | none | none | none |
| A5 accept | **Yes, as "Apply"** in the local UI. Apply *is* the acceptance: there is no accepted-but-not-applied state | **No** on main: a session receipt in memory, with basis `user_initiated_apply_in_local_session` and `acceptance_is_professional_approval: false`. **DRAFT #885:** a committed receipt readable through CLI `status` within one controller session | main: none externally. #885: ticket, workspace, identity {app instance, controller session, workspace, project generation, project}, batch and operation ids, origin, acceptance {route `local_review_apply`, `identity_verification: not_performed`}, before and after {model revision, model hash}, undo checkpoint id. **No person is named, and no time field** | desktop UI; #885 CLI `status` | **No** (lost on restart or project open; #885 is within the controller session only) |
| A10 reject | **No.** "Clear" discards queued batches without a record. A rejection record is DESIGN (gap G-18) | No | — | — | — |
| A12 set grant | **No**: there are no grants (SQ-05) | No | — | — | — |
| A6 approve / A7 rely | **No.** Not software acts in SWBPIPE: `OPS-K-AUTH-1` forbids software approval claims, `ENGINEER_ACCEPTED` is reserved, and the MVP has no acceptance workflow | No | — | — | — |
| Act-declined | **No** | No | — | — | — |

- **Sample record (invented material):** DRAFT #885 `P/docs/LIVE_CONTROL_DEVELOPMENT.md`, "invented exchanges", at `12907f393`.
- **Elicitation or prompt capture: No.** No such capture exists or is designed.
  - SWBPIPE records state that agent-driven Apply, browser tests and computer-use clicks are **not** human acceptance, and PR #885's CLI exposes no Apply.
  - MCP elicitation is not addressed in any record.
  - Whether that ever changes is an **OWNER DECISION** (the actor identity model is TBD in DEL-16-03; acceptance-record storage is `PB-TBD-002`).

#### SQ-02 Governing checkpoint constraint

**Route: option (iv), none planned.** SWBPIPE has no workflow run, workflow declaration, checkpoint concept, run association or hold machine. No SWBPIPE record plans options (i), (ii) or (iii). Whether to plan one is an **OWNER DECISION**; no open item exists for it today.

- **(a):** not applicable. An extra constraint field sent today would be **refused as an unknown field**: batch preflight accepts exact objects only (`…/operation_applier/src/atomic_batch.rs:213-231`). It would not be honoured.
- **(c):** No. **(d):** No on the embedded surface (there is none), No on the external surface. **(f):** No, No. **(e):** none.
- **Related fact, not an answer to D6.** Today every change reached externally (DRAFT #885) or offline waits for the person's Apply. No route applies directly, so every host operation is resolved as *propose*. That is a property of the current route, not a checkpoint evaluation, and it should not be counted as host-held carriage under R2-12.

#### SQ-03 Content identities used to bind acts

- **(a) No.** No read returns a per-row or per-object subject identity. The only identity is `ModelHashEvidence` {`sha256`, `rfc8785_jcs`, scope `model_payload`} over the whole model (`P/apps/desktop/src-tauri/src/lib.rs:2050-2059`).
- **(b) Not applicable.** No per-object identity exists, so nothing is decided about what one would cover. FXA-2 has no host counterpart.
- **(c) Partly.**
  - An Apply is bound to its operation by id, and to the model by an optional claimed whole-model hash plus per-field before-values. A stale claim is refused: `OP-CLAIMED-MODEL-HASH-MISMATCH` and `OP-STALE-BEFORE-VALUE`.
  - Batches require a claimed hash.
- **(d) Partly.**
  - A single outcome names `target_ref`, the diff rows (field, before and after) and the new whole-model hash. A batch outcome lists each step's target and diffs plus the final hash.
  - Created objects appear as the target ids of `create_*` operations.
  - **No post-application per-object identities.**
- **(e) Same identity value**, because the whole-model hash is a pure content hash.
  - However, in DRAFT #885 the model **revision** advances on every commit, Undo included, and equal content does not revive an old revision, so an earlier proposal stays stale.
- **A separate identity from T3, for results only:** solver results carry their own receipts (`P/core/product_physics/src/source_receipt.rs`: receipt and publication sha256 over the published result envelope). These identify **analysis results**, not model rows or objects.
- **Samples:** outcome shape at `…/operation_applier/src/lib.rs:130-153`; DRAFT #885 invented exchanges.

### P2

#### SQ-04 First connected activity

- **Selection: none.** No SWBPIPE record selects an activity for OI-021 or answers the HANDOFF "Return list". **Choosing it is an OWNER DECISION**, as the questions say, with the App/shared owner.
- **Candidates that exist on main:**
  - **(a) Change operations:** 27 change kinds through the one engine route (`operation_applier`; create, connect, delete, insert and modify).
    - One operation is external-wired, in DRAFT #885 only: **Node `position.x` modify/set_field**, single and ordered atomic batch, on invented fixtures. That is the owner-activated first journey: inspect → preview → submit → the person's Apply in the app → status. An intervening edit expires the proposal as stale.
  - **Reads:** the model read, and in DRAFT #885, `inspect`.
  - **Non-mutating checks:**
    - validate-only preview;
    - the mechanics solve, whose published result carries **host-named integrity standing**: Passed, Sensitive, or refused with a named `NUMERICAL_INTEGRITY_*` diagnostic (T3's work);
    - user rule checks (`USER_RULE_CHECKED` / `USER_RULE_FAILED`).
    - PR #885 exposes only the validate-only preview as a check.
- **(b)** Host-named checks exist: rule checks and solve integrity standing. PR #885's first journey uses validation only.
- **(c)** SWBPIPE records select **a development Codex controller through the CLI first, and an embedded agent later**. The App's Codex is not named.
- **(d) Candidate environment:**
  - macOS only (other hosts return `unsupported_host`);
  - PR #885 head `12907f393`, unmerged;
  - the development desktop started with `SWBPIPE_LIVE_CONTROL=1`;
  - the CLI built with the feature `live-control-cli`.
  - **Readiness, in SWBPIPE's words:** implementation reviewed. A clean DEC-025 sweep, the native witnesses I1/I2, the actual-human witnesses H1/H2 and a final review are outstanding. It is deferred to UI-SUCCESSOR. There is no date.

#### SQ-05 Policy for the selected operation (answered for Node `position.x`, and generally)

- **(a)** No class system. Every change requires the person's Apply: `requires_user_acceptance: true` and `direct_model_mutation_allowed: false` are hard-coded in the operation envelope.
- **(b)** None.
- **(c) No named reserved-act list.** Against the owner's five D2 acts:

  | D2 act | SWBPIPE today |
  |---|---|
  | Marking work checked | Engineer-only by design, not implemented |
  | Accepting a proposal | The person's Apply, implemented |
  | Engineering approval | Not a software act |
  | Professional reliance | Not a software act |
  | Changing the autonomy grant | No grants exist |
  | Enabling external access | A launch environment variable, not a captured act |

- **(d)** No settings reference. **(e)** No grant states.
- **(f)** Not decided. Autonomy is **OWNER DECISION** OI-016 ("human product decision").
- **(g)** None on main: there is no withdraw or reject operation. In DRAFT #885, `withdrawn` means **the person cleared the queue** (`cleared_in_review`), not the proposer withdrawing; there is no agent-side withdraw.
- **(h)** Not applicable: there are no grants. Apply always revalidates through the engine.
- **(i)** Not decided (OI-016).

#### SQ-06 Direct application on the external channel

- **Answer: not (a).** There is no class assignment. SWBPIPE records word the no-Apply rule both as **(b) a channel rule** ("no external Apply") and as **(c) a property of the first journey**, with later automatic apply "a separate bounded choice". Which label governs is an **OWNER DECISION**.
- **Outcome of a direct external request (DRAFT #885):** Apply is not a method. The request is refused as **`unsupported_method`** ("Only inspect, preview, submit and status are supported"). It is **not** *not permitted* naming a rule.

### P3

#### SQ-07 Read basis, generation and staleness

- **(a)** Main: no. The model read and its hash are separate, and there is no workspace identity or generation. **DRAFT #885:** yes. `inspect` returns `basis_identity` {app instance, controller session, workspace, project generation, project, model revision, model hash}.
- **(b)** DRAFT #885: a new workspace id and generation are minted when the published project changes, and **cross-workspace reuse is rejected** even when bytes and revision match. Archive restore is not addressed. Bases are not comparable across generations; they are rejected.
- **(c)** Main: **no**. The offline intake captures the basis at queue time. **DRAFT #885: yes**: preview freezes the inspected basis, and submit keeps it.
- **(d) No; staleness is whole-model.** Any revision change stales every queued proposal, on main and in #885. **The App's R2-13 per-item rule does not hold for SWBPIPE.** The engine additionally checks per-field before-values.
- **(e)** Yes. Apply re-runs full engine validation against the claimed hash.
- **(f)** Any model commit: edit, apply, undo, redo, project open or create. Selection changes do not stale.
- **(g)** Not found: there is no multi-read reliance concept.
- **(h)** Solve and rule checks run on the current model, and computed results are cleared on any model change. There is no cited-versus-evaluated basis statement.

#### SQ-08 Proposal identity and repeated submission

- **Main:** the submitter supplies `batch_id`. There is no de-duplication across submissions, and a proposal's state cannot be read outside the UI.
- **DRAFT #885:**
  - **(a)** The controller mints `preview_ref` at preview, before any submission. The caller supplies an `idempotency_key` at submit, and the controller returns a `ticket`.
  - **(b) Yes.** The key lookup runs **before** the basis check, so a retry recovers its ticket even after its own commit. The same key with different content returns `idempotency_conflict`.
  - **(c) No.** Associations live only in the running controller. A restart expires handles or yields `outcome_unknown`.
  - **(d)** Yes, within the session: `status` by ticket.
  - **(e)** The committed receipt binds one model transition (before and after revision and hash), with one undo checkpoint per batch. Duplicate-submission witnesses are required but **not yet performed**.
- **Durable de-duplication across restart:** a current hold ("durable receipt carrier"), an **OWNER DECISION** per SWBPIPE's live-control contract draft.

#### SQ-09 Outcome statements, errors and unknown outcomes

**(a) The mapping,** main and DRAFT #885:

| App term | SWBPIPE |
|---|---|
| refused (invalid) | `blocked` with blocking diagnostics (main); #885 `invalid_request`, `unsupported_change` |
| refused (stale) | `OP-STALE-BEFORE-VALUE`, `OP-CLAIMED-MODEL-HASH-MISMATCH` (main); #885 `stale_basis`, `expired` |
| queued | #885 `queued`, only after the controller observes publication |
| applied with receipt | `applied_to_session_model` (main); #885 `committed` |
| rejected | no record on main. #885 `rejected: validation_rejected` means **the engine** rejected at the person's Apply, not a person's rejection |
| withdrawn | #885 `withdrawn`: the person cleared the queue |
| channel not enabled | **no code.** The attempt appears as `controller_unavailable` or an attachment failure |
| not exposed on this surface | `unsupported_change` / `unsupported_method` |
| outcome unknown | #885 `outcome_unknown` |
| unavailable / not permitted / error | #885 `busy`, `capacity`, `not_ready`, `unauthorized`, `wrong_app`, `wrong_workspace`, `internal_error`, and others; each carries `retryable` and `next_action` |

- **Transport status is separate from these outcomes.**
- **(b)** Batches are atomic: all or nothing. There is no partial application.
- **(c)** There is no durable receipt. In #885, a timeout or disconnect "does not prove the proposal never happened", and a later `status` read resolves it only within the controller session.
- **(d)** A validation failure before queueing is a blocking result, and nothing is queued.
- **(e)** The same engine codes apply at validate and at Apply. #885 distinguishes `rejected: validation_rejected` (at Apply) from preview and submit errors.
- **(f)** Items are applied as groups: one batch is one application and one undo checkpoint.

#### SQ-10 Undo and publication

- **Undo route:** yes, but only as a **session** Undo/Redo stack of whole-model snapshots (25 deep).
  - It is **not** an operation through the engine. It writes **no receipt**, does not reference the reversed change, and is not governed by operation policy.
  - It reverses one checkpoint, and a batch is one checkpoint. It is cleared on project open or create.
  - DRAFT #885 records `undo_checkpoint_id` in its receipt. Undo is not exposed on the CLI.
- **"Publication"** has two unrelated SWBPIPE meanings:
  - in #885, a controller observing a queue or commit becoming visible in the UI;
  - in governance, public-repository release.
  - Neither affects an applied change's standing.

#### SQ-11 Exposure per surface

- **No:** there is no per-surface exposure element. The desktop toolkit's capability `status` (supported, partial, unavailable, gated) describes UI routes only.
- **First-activity entries:** DRAFT #885 offers exactly one on the CLI, Node `position.x` modify/set_field. Everything else is refused as `unsupported_change`. There is no embedded surface.
- "Not exposed" is reported through `unsupported_change` or `unsupported_method`, not through a distinct exposure element.

### P4

#### SQ-12 External seam and derivation

- **Seam:** the CLI (DRAFT #885), not MCP.
- **MCP:** SWBPIPE records allow an MCP adapter later **only if** the actual Codex client meets the owner's modern stateless MCP condition of 2026-07-28. The tested bundled client used a legacy handshake and failed it. Any MCP choice returns to the owner: **OWNER DECISION**.
- **Derivation: hand-built and narrow.** The preview calls the same atomic engine as the UI, but the CLI's method set is fixed in code, not generated from or checked against a catalog.
- **Mapping to catalog operation identity and version: No.** No per-operation identity or version exists; there is one engine crate version.

#### SQ-13 Enablement behaviour

- **Off by default:** yes (DRAFT #885).
- **The opt-in** is a **launch environment variable** (`SWBPIPE_LIVE_CONTROL=1`) plus a **build feature** (`live-control-cli`). It is **not** a person's act.
- **When off:** there is no descriptor and no socket, and the CLI fails as `controller_unavailable`. There is **no explicit "channel not enabled" code**. Non-macOS hosts return `unsupported_host`.
- **Enablement state readable:** no.
- **Queued proposals when access is disabled:** not addressed. A restart expires handles or yields `outcome_unknown`.

#### SQ-14 Origin and caller identity

- **Recorded (DRAFT #885), all assigned by the controller.** Caller-supplied author, source and acceptance fields are rejected.
  - `author_type: agent`;
  - `source` {`source_ref: local_json_cli:<controller session>:<request id>`, `source_channel: local_json_cli`, `source_role: external_agent_proposal`};
  - the receipt's `origin` {actor type, channel, request id}.
- **Verified: none.** Records state the caller is "not verified Codex identity", and that MCP clientInfo "is not authentication".
- **Main:** the batch envelope carries `source_identity_verification: "not_performed_asserted_metadata_only"`.
- **Conversation and workflow run:** not recorded.
- **Authentication:** a random local capability in a 0600 descriptor inside a 0700 private directory. The native side validates the app and registration identity.
- **Callers:** any holder of the descriptor, up to 16 concurrent connections or requests.

#### SQ-15 Locality and sandbox

- **Transport: strictly local** (DRAFT #885). A macOS Unix domain socket and descriptor in a randomly named private directory under the macOS system temporary directory (`private/tmp`) (directory 0700, entries 0600). There is no network listener.
- **Sandbox:** not addressed in any SWBPIPE record.
  - By construction, the caller must read the descriptor file and connect to the socket in that directory. So a sandbox that forbids that path would block the CLI.
  - That is an inference from the design, **not observed**.

#### SQ-16 Host restriction by the caller's model destination

- **No restriction.** The #885 wire has no destination field and no destination-based refusal. **The App need state nothing.**
- **Related, for the App's awareness:** SWBPIPE's DEC-051 (open residency) says that an owner-configured provider for SWBPIPE's **embedded** agent ("local, Anthropic, or other") gets no app-side guard, gate or indicator, "for now". Revisiting it is an **OWNER DECISION**. It does not address the external CLI.

#### SQ-28 Enablement facility for A13

- **Facility exists: No.** Not on main, not in PR #885, and no plan found.
- **Reference exposed: No.** **State readable over the interface: No.** **Disable captured: No.**
- **So under the App's contracts, the external channel stays *not enabled*.**
- Whether SWBPIPE builds such a facility is an **OWNER DECISION**; no open item exists.

### P5

- **SQ-17 Receiving App workflows.** **(a) No. (b) No.**
  - The SWBPIPE product has no workflow library, reader or declaration parser. In SWBPIPE product code, "workflow" means a user journey.
  - (c) Not applicable: there are no host runs. (d) Not decided.
- **SQ-18 Adaptation and library identity.** (a) No host workflows exist. (b)–(d) No. (e) Not applicable: operation intents carry no operation version.
- **SQ-19 Host run records and supplied guidance.**
  - (a)–(c) **No.** There is no host loop. SWBPIPE's "run records" are solver analysis run records.
  - (d) **The premise is not established.** SWBPIPE records do not define an agent "seat" or role meanings. The UX design has one agent panel with Conversation, Proposals, Checks and Accepted tabs (persistence is gap G-17). Not decided.
- **SQ-20 Host-side placement.** **Not decided**, for the loop, panel assembly, persistence, the hold machine and the required-tool check.
  - **Recorded direction:** a later "embedded Runtime" adoption (RUNTIME-ADOPT, planned). It requires immutable catalog registration before the first turn, rebind and resume, and the modern MCP condition if selected.
  - **The successor embedded mechanism is unresolved under D-58: OWNER DECISION.**
  - **PR #885's placement:** a native bridge in Rust; the controller in the desktop frontend; validation in the shared engine.

### P6

- **SQ-21 Faithful-record operation.** **No.**
- **SQ-22 Proposal views.**
  - **Batch review** (Operations → Review) shows each proposal's steps as `field: before → after`, with diagnostics and the submitted JSON, including rationale and source. The Operation apply, Operation ledger and Diff preview panels are also available.
  - **Referencing:** only internal element and test ids. There is **no stable external reference scheme**.
  - Proposal cards and table and canvas "ghosts" are DESIGN.
- **SQ-23 Display.**
  - **What exists:** a stale batch shows "The model changed. Prepare a new batch from the current model." Undo shows a session message.
  - **Not applicable:** grant supersession (there are no grants); "accepted, not applied: stale" (Apply is the acceptance).
  - **DESIGN only:** stale wording for the Checked mark, and "superseded by" rows.
  - **Not designed:** a reversal marker.
- **SQ-24 Findings.**
  - No findings storage on main.
  - DESIGN: agent cards (Check, Open issue, Evidence summary) held by reference, with open and resolved states, persisted with the project (gaps G-19, G-21).
  - Whether storing a finding is a change through the route: not decided.
- **SQ-25 Acts on host content captured through the App.** **Host facility only.**
  - SWBPIPE records: the bridge assigns actor = agent, the human acceptance is recorded separately in the app, external tools cannot Apply, and computer-use clicks are not human acceptance.
  - There is no proxy.

### P7

- **SQ-26 The extension-trace operation.**
  - **Not chosen.** SWBPIPE has no catalog editions and no edition-addition event. Per surface: not applicable.
  - Participation in the App's OI-003 decision: **OWNER DECISION**.
  - **Id collision:** SWBPIPE's own OI-003 is a different item (legal review of component and material data).
- **SQ-27 Candidates, examination evidence and relay.**
  - **(a)** SWBPIPE identifies a contribution by commit SHA and PR merge commit, and records with it:
    - hosted CI run ids, with the full-SHA E2E dispatch;
    - the DEC-025 local sweep;
    - T9 byte identity (Mac-only on the owner's Mac);
    - native witness records and executable hashes;
    - all of it in AgentRuns `_run_records` with SHA256SUMS.
  - **(b) Checks for the first-activity kind of work:** the operation contract corpus (81 invented cases) and PR #885's focused live-control tests.
    - Outstanding: the clean sweep, native I1/I2 and actual-human H1/H2.
    - For any solve or check in an activity: T3's frozen references, the both-entry gate and T9.
  - **(c)** No relay form is agreed. SWBPIPE evidence is files in the repository with hashes, relayed by the human.
  - **(d) Later:** the human witness step (LIVE-HUMAN) is blocked until live implementation and owner participation, and it is deferred.
  - **(e) What SWBPIPE needs from the App side: nothing at present.** What moves these answers is the **owner's** direction (§2), not an App input.

### P8

- **SQ-29 Model interface.** **None exists, and none is selected.**
  - Historically, a Claude Agent SDK Node sidecar (DEC-041) was chosen. Its current reliance is retired by D-58.
  - The owner has reported a local model available on the Mac (oMLX), with "no silent cloud fallback" noted for a later check.
  - Recorded exchanges: none.
  - The successor is an **OWNER DECISION**.
- **SQ-30 Endpoint and key boundary.**
  - **(a)** No endpoint configuration and no key custody exist. `api_key` appears only as a key name to redact.
  - **(b)–(e)** Not decided.
  - **Conflict for the App to note:** SWBPIPE's **DEC-051 open residency** allows an owner-configured provider, cloud included, with no app-side guard, gate or indicator ("for now"). SPEC §4.4 lists key management, secret storage and provider and egress configuration as TBD. That differs from the App's V4-HOST-02 local-only expectation. **Reconciling them is an OWNER DECISION.**
  - Endpoint-redirect refusal: not decided.
- **SQ-31 Malformed calls and validation order.** There is no loop, so (a)–(d) are not decided for a loop.
  - **Engine-side analogues (FACT):**
    - strict preflight (exact keys, required fields, unknown fields rejected, unsupported kinds refused) runs **before** simulation;
    - malformed input returns a structured error, "never a silent fallback";
    - nothing is repaired or defaulted.
  - DRAFT #885 refuses unknown or missing params (`invalid_request`) and any change other than `position.x` (`unsupported_change`).
- **SQ-32 Responsiveness.**
  - Placement: not decided.
  - **FACT:** the solve already runs as a background job with poll and cancel.
  - Relaying observations: possible when a loop exists.
  - Numeric threshold: not decided. The owner decides R-OPEN-1.

---

## 2. Owner decisions these answers turn on

| Decision | SWBPIPE record | Moves |
|---|---|---|
| Whether and when UI-SUCCESSOR, including live control, resumes; and whether the App v4 (its Codex) becomes a named caller of that channel | work graph `:60` (resumes on the owner's direction) | SQ-04, SQ-12…16, SQ-27, SQ-28 |
| Agent autonomy level: classes, grants, direct or automatic apply | OI-016, "human product decision" | SQ-05, SQ-06 |
| A durable receipt carrier and durable de-duplication | the live-control contract draft, "current holds" | SQ-01, SQ-08, SQ-09 |
| Acceptance-record storage, and the actor identity model | `PB-TBD-002`; DEL-16-03 TBD | SQ-01, SQ-03 |
| The Checked-mark implementation tranche | DEC-104 (D-71 addendum) | SQ-01, SQ-03, SQ-05 |
| Any MCP adapter (the modern-client condition) | the owner's 2026-09-20 CLI and protocol disposition | SQ-12 |
| The successor embedded-agent mechanism | D-58 / DEC-091 | SQ-19, SQ-20, SQ-29…32 |
| Open residency versus local-only | DEC-051 ("for now") | SQ-16, SQ-30 |
| Whether SWBPIPE plans any host-held checkpoint route (none planned today) | none exists | SQ-02 |
| An A13 enablement facility (none exists) | none exists | SQ-28 |

## 3. Assumptions in the questions that SWBPIPE facts contradict or qualify

1. **Direct external apply** returns `unsupported_method`, not *not permitted* naming a rule (SQ-06).
2. **Staleness is whole-model.** Applying one proposal stales all the others, so R2-13's per-item rule does not hold (SQ-07 (d)).
3. **No per-row or per-object subject identities** exist; there is only the whole-model hash (SQ-03).
4. **"Opt-in"** is an environment variable plus a build feature. It is not a person's act, it has no "channel not enabled" code, and its state is not readable (SQ-13, SQ-28).
5. **The queue-time basis** is true of main's offline intake. PR #885 freezes the inspected basis, but it is unmerged (SQ-07 (c)).
6. **The caller:** SWBPIPE records name a development Codex, not the App's Codex.
7. **The embedded direction:** SWBPIPE plans a later "embedded Runtime" adoption, with its successor unresolved. The App HANDOFF's "minimal host loop" does not appear in SWBPIPE records (SQ-20, SQ-29).
8. **Local-only:** SWBPIPE's DEC-051 allows cloud providers with no guard ("for now") (SQ-30).
9. **"Single agent seat"** is not a SWBPIPE concept (SQ-19 (d)).
10. **`withdrawn`** in PR #885 is the person clearing the queue, not the proposer withdrawing (SQ-05 (g), SQ-09).
11. **PR #885's readiness:** its description's "reconfirmed proceeding" predates the work graph's deferral, which governs.
12. **Id collision:** SWBPIPE's OI-003 is a different item from the App's OI-003 (SQ-26).

## 4. What would change these answers

- The owner directs UI-SUCCESSOR, or live control, to resume. PR #885 is then qualified and merged.
- The owner decides OI-016, the durable receipt carrier, `PB-TBD-002`, the Checked-mark tranche, an MCP adapter, the D-58 successor, or DEC-051.
- A SWBPIPE work item is created to receive App workflows, or to host a checkpoint route.

When any of these happens, SWBPIPE records it in its own work graph and decision register, and a revised answer file can be relayed.

## 5. Limits of these answers

- **Research method:** read-only, over product source and schemas at main, SWBPIPE decision and design records, and PR #885's head files. Nothing was run to produce these answers, and no candidate was built.
- **Standing of draft facts:** "DRAFT #885" facts describe unmerged code, which may change before any merge.
- **No existing App file was changed.** This file and the fact sheet were added as two new files beside the questions (§6). The App project records returns in its own ledger.

## 6. Delivery and SWBPIPE-side record

- **Delivered:** 2026-09-28, at the owner's direction, as two new files in this `Design/` folder beside `RELAY_QUESTIONS_SWBPIPE.md`: this file and the fact sheet `FACTS_SQ01_SQ32.md`. The main commit that adds them is the delivery's revision (`git log -- RELAY_ANSWERS_SWBPIPE.md`).
- **Fact sheet:** delivered as the researcher prepared it, unchanged. Its opening line says nothing in it was relayed to the App; that describes it when it was prepared.
- **SWBPIPE-side record:** identical copies of both files are kept in SWBPIPE's records under `projects/chirality-piping/execution/_Coordination/AgentRuns/HELP-HUMAN-PIPING-20260918-UI-IMPLEMENTATION/instances/CONTINUATION_2026-09-24/APP_V4_RELAY_2026-09-28/`, with SHA256SUMS, on the SWBPIPE records branch `codex/piping-numerical-integrity-20260926`. They reach main with SWBPIPE's next records PR. This is the first SWBPIPE record of the App v4 relay.
