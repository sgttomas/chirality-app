# Workflow-making workspace and registration

- **Contribution:** DEL-02-02/WR-v0.2 (supersedes DEL-02-02/WR-v0.1, committed at `63a6e0fa47`, file sha256 `0b51ee6c7ea9c57120b5a7654d2888266bf409b8914f02cb32c2a1dcd25dfb27`).
- **Status:** DRAFT DEFINITION — proposed, not implemented, not accepted. Nothing here is built, qualified or owner-reviewed.
- **Run / node:** `APP-V4-DESIGN-PASS-3-20261001`, node D5. v0.1: round 1 (BRIEFS.md "D — design nodes, round 1", row D5), 2026-10-01 at HEAD `dc031b5bec`. **v0.2: "D round 2"**, 2026-10-02 at HEAD `037063ce09` (branch `claude/chirality-app-v4-60-percent-a41fd5`). Type 2 TASK executor, harness-native descendant of the HELP_HUMAN session; no delegation.
- **v0.2 inputs (binding additions; sha256 by `shasum -a 256` at `037063ce09`):** `R18_RESOLUTIONS.md` `abf5eee6324647ff…` (R18-1: C-01, C-02, C-14, C-21, C-22); `R19_RESOLUTIONS.md` `16930ecdcead7511…` (R19-1, R19-2, R19-4 L-4, R19-5, R19-7); `OWNER_DECISIONS.md` `ea96c55710af41c9…` (DECISION-L: L-2 as the owner chose it, L-4 A as clarified); `DECISIONS_PENDING_2.md` `0ecbf87aae8d4350…` (L-4 text as clarified); `BRIEFS.md` `316ea29325a0d450…` ("D round 2"); `R20_RESOLUTIONS.md` `9ab9af81d37f0711…` (R20-1 run end only by the person or the run owner; R20-3 the run-end line; sent by HELP_HUMAN during round 2); `F/F0_JOINS.md` `e93608be1c6e3eb0…` (§2 C-01, C-02, C-14, C-21, C-22; §6 "Not F's"; §7.5); `DEL-01-01/Design/OBS_3_0.158.0.md` `554ac4451d112824…` (W-1…W-6, §11) and `OBS_2_0.158.0.md` `61cc34ffb811eb27…` (no WR cell depended on it; F0 §7.5); the generated 0.158.0 bundle `generated/0.158.0/json-schema/experimental/codex_app_server_protocol.v2.schemas.json` `34f28a486d00fbd2…` (`TurnStartParams`, `Turn`, `ThreadItem`, `UserInput`) and the session's stable TypeScript output (`v2/TurnStartParams.ts`, `v2/ThreadItem.ts`), read only.

## Changes from v0.1

| Ruling / item | Change | Where |
|---|---|---|
| R19-7, R19-1, R19-2 (DECISION-L L-2) | **New owner of run-start supply.** DEL-02-02 composes the text element that starts a workflow run: the registered revision's exact `WORKFLOW.md` bytes framed by App-written lines (framing WR-FRAME-1, PROPOSED) naming workflow and revision and, when chaining, saying the previous run ended; an end notice when a run ends without a successor; its content identity; the check against `thread/read`. Chaining (a) sequential and (b) agent-proposed with the person confirming; one run at a time per conversation | new §16; §1; §3; §7; §8 (`run_text`, `supply_check`); §12 WR-VC-12…15 |
| R19-7 | The proposed row DEL-02-04 → DEL-02-02 (R17-8; v0.1 NR-2) is dropped: DEL-02-04 composes role guidance only. DEL-02-03 starts the run; DEL-02-02 supplies the run text to it | §7 DEL-02-04 and DEL-02-03 rows; SQ-S S-4 |
| C-01 (R18-1) | The persisted A15 form is RS's (FR-06): `relations.reviewedDraft {draft: ID-3 string, content}` and `priorRevision` = RS `workflowTuple` or null. WR keeps its internal `a15_descriptor` object and writes through the RS writer | §2.2 ID-3; §4.3 RB-4; §8 |
| C-02 (R18-1) | `draft_transition` gains optional `a15_record` and `revision`, on *registered* (both) and *registration not completed* (`a15_record` only) | §5.1; §8; schema |
| C-14 (R18-1) | Confirmed: a draft reaches a trial only as a message or attachment the person sends; no guidance carriage | §4.2 TT-3 |
| L-4 A as clarified (R19-4) | Library entries byte-equal to a shipped revision are recognized as that revision and run at once (new LS-8); the rest are registered in place, several per act (new §4.7, `a15_multi_descriptor`). U-WR-4 closed | §4.6; §4.7; §15 |
| C-21, C-22 (R18-1) | Notes only: the act record carries reviewed draft and prior revision; WD's derived-from stays in the tuple. D5.md §2.1's mapping table is superseded (D3 adopted WR's names) | — |
| R20-1, R20-3 | A run ends only by the person (DEL-01-02 DEF-4) or the run owner; when the agent reports the workflow finished the App offers "End run" and, with a proposal, "End ‹A› and start ‹B›" (cause *completed*); the agent's words alone end nothing. When a run ends and no run starts with the next turn, that turn is prefixed by one App-written line naming workflow and revision (worded here, same schema). The framing's third line now also tells the model how to report a finished workflow | §16.2 line 3; §16.3 CH-2; §16.5 FN-1…FN-3; TX-5; schema `proposal_line`; U-WR-17 closed |
| R19-5 | Every supplier fact in §16 names its version (Codex 0.158.0); OBS-3's results are dated observations at that version | §16 |
| OBS-2 | No WR cell was marked "OBS-2 pending" (F0 §7.5: no change) | — |
| Prototype | Extended: C-01 form against RS's schema projected with FR-06; C-02; L-4 recognition and multi-entry act; run text composition, chaining A→B→C, end notice, agent proposal, supply check against constructed `thread/read` turns validated against the generated 0.158.0 types; R20-1 finished report and R20-3 run-end line. 92 checks (was 58) | §13 |
| Section numbering | §1–§15 keep their numbers; §16 is new and placed after §15 so that join rows citing §1–§15 stay valid | — |
| RX (residual sweep, in place, no version step; R20-9, R20-5) | The two agent lines name the workflow by origin and name, each alone on its own line: `Next workflow: ‹origin›:‹name›` and `Workflow finished: ‹origin›:‹name›`; the App reads only these exact forms. The run-start text's third line repeats both for the run in force (its finished line names the run's own origin and name). A proposal resolves within the named origin to exactly one registered workflow, else a notice and no Start (aligned with NIR-v0.2 §5.7 RN-3, RN-5). Schema: `proposal_line` is a pattern (was a constant) and `proposal.proposed_name` takes the `‹origin›:‹name›` form; invalid instances INV-16, INV-17 added. Prototype: line forms, resolution by origin, P-58 extended (a line without an origin is no proposal), P-60 finished line by origin, new P-62. U-WR-20 closed (ROLE-v0.2 GS-7 carries both lines) | §16.2 line 3; §16.5 PR-1…PR-3, FN-1; §8; §12 WR-VC-11, WR-VC-15; §13; §15 U-WR-20; schema; examples; `prototype/wrproto.py` |
| RX2 (residual sweep 2, in place, no version step; R20-11, R19-7) | R20-11 (1): during a run a proposal is offered only as "End ‹A› and start ‹B›"; a plain "Start ‹B›" only with no run in force. R20-11 (2): the proposal line is the last non-empty line; the finished line is the last non-empty line or the one immediately before the proposal line; each at most once. R20-11 (3): an *unreadable* check reads "supplied — not verified" (the App observed its own send; Codex's copy could not be read). R20-11 (4): "End ‹A› and start ‹B›" records A ended by the person with cause "ended to start ‹B›" (EXEC's wording), except on a finished report, where R20-1's *completed* stands (this file's reading of R20-11 (4) beside R20-1); the chain line and the `ended` values gain that cause. To match (2), §16.2 line 3 now tells the model to end the message with the finished line and, when both are written, to put it just before the proposal line (schema pattern, examples and ROLE GS-7 follow). Header Receivers line and §1 row R17-8 no longer carry what R19-7 superseded. The valid run_text example now carries real identities computed from fixture bytes (`prototype/fixtures/review-pack/`); new prototype checks P-63 (example identities recomputed), P-64 (End ‹A› and start ‹B›), P-65 (line placement) | Header; §1; §16.2 line 1; §16.3 CH-1, CH-2; §16.5 PR-1, PR-4, FN-1, FN-2; §16.6 SC-4; §12; §13; schema; examples; prototype |
| F-E2 (design-pass-3 citation check; in place, no version step; R19-7) | §8's receivers: DEL-02-04 is removed from `library_entry` and `selection_record`. R19-7 dropped the row DEL-02-04 → DEL-02-02 (R17-8) and DEL-02-04 composes role guidance only (§1; §7's DEL-02-04 row: nothing flows for workflows; ROLE-v0.2 §7.1, C-6 withdrawn). The schema's `selection_record` description still names DEL-02-04 (workflow supply, R17-8); it is outside F-E2's write fence and is returned (F/F-E2.md). No record kind, field, rule or identifier changes | §8 |
| RV21 (repairs from V21; in place, no version step) | **R21-3 (V21-A M-1, item 6):** RB-4a's stale sentence is replaced: RS-v0.9 admits both `draft:` and `entry:` and AAC-v0.2 (RV21) adopts this file's `a15_multi_descriptor` as one descriptor per act, with the plural wording; ME-3 cites it. **R21-4 (V21-B m-4):** the supply check reads with `thread/items/list {threadId, turnId}` (HOSTING-v0.9 §4.4 "Recovery reads"), following its pages, not `thread/read {includeTurns: true}`; *unreadable* now means a failed read or page. **V21-A MINOR 13:** §7's DEL-01-03 row follows R18-1 C-05 (only the plan-mode element needs the experimental opt-in); §8's stale paragraph on the RS-v0.8 form is rewritten. **V21-B m-9 (F-E2 §4.3 row 7; in this fence):** the schema's `selection_record` description no longer names DEL-02-04 (R19-7). Prototype: P-50a new, P-51/P-52 read pages; 99 checks | RB-4a; §4.7 ME-3; §7; §8; §15 U-WR-14; §16.4; §16.6 SC-3; §16.7 RN-5; §13; schema descriptions (`supply_check`, `selection_record`); `prototype/wrproto.py` |
| C0 (closeout; in place, no version step) | **R21-5 (V21b-A N-2):** TT-3's pre-fill now attaches the draft's `WORKFLOW.md` as a text element, following NIR-v0.2 §6 AT-8 (other text files AT-9, other files named AT-10); once sent it is the person's own attachment: no run, no workflow supply, no run-start text. The earlier "a message naming the draft's path and content identity" is withdrawn. Prototype rerun 2026-10-02 (no change needed: it models the trial pointer, TT-4, not the pre-fill): `wrproto.py` 99 checks, 99 passed (`closeout/C0.md`) | §4.2 TT-3 |
| CC-WR-RECONFIRM (named change; in place, no version step; owner decision "A15 re-confirmation now (Recommended)", 2026-10-07, run `APP-V4-GROUP-A-20261004` `OWNER_DECISIONS.md`; change record `changes/CC-WR-RECONFIRM.md` of that run, revision 2 after review V13) | After the App process that held a revision's registration result is gone (for example after a relaunch), a new genuine A15 may **re-confirm** a draft whose reviewed bytes equal registered revision ‹k› with LS-1 standing: new disposition DS-8; no new revision, sequence or identity; ledger outcome *re-confirmed* citing the new A15 and ‹k›'s registered line; the result is selectable in that process only. DS-4 stands while ‹k› is selectable in this process or is not LS-1; K-6 (SP-3, DS-3) is decided first, unchanged (SP-4a). Refine of an LS-1 revision needs no selection (RF-1), so a draft for DS-8 can be made after a relaunch. Trust rests on the new act, never on a replay of the earlier act or receipt; SEAL-2 stays deferred; CI-10 and I3-CUST stay open. Answers `app/CONTRACT_ISSUES.md` CI-21 (b) | §4.1 SP-4 (DS-4, DS-8), SP-4a; §4.3 RB-3, RB-4, RB-8; §4.6 LS-1 row, note, RF-1; new §4.8 RC-1…RC-10; §5.1–§5.4; §6 SQ-R R-3, SQ-G, SQ-X X-2, X-4; §7; §8; §9; §12 WR-VC-16…WR-VC-20; §15 U-WR-21…U-WR-23; schema (`reconfirmed_revision`; `registration_disposition`, `draft_transition`, `a15_descriptor` including its `freshness` description, `library_entry`) |
- **Serves:** OUT-001, OUT-002 (design of the CODE), OUT-003 (fixture design and a design prototype), OUT-004 (receiving and reuse account, §7, §10); REQ-001…REQ-008; AC-001…AC-008 by designed verification (§12); VER-001…VER-006 (cases designed; library-side parts run on the prototype only).
- **Labels** (as R9 and R17): **SETTLED** (an accepted text or owner decision says it), **DERIVED** (follows from those), **INTEGRATION** (an integrator ruling, open to the owner), **PROPOSED** (a design structure of this file, decided by no one). Supplier facts carry `observed`, `observed-in-generated-types` or `inference` (R17-13).
- **Basis (binding):** the accepted basis as amended by SCA-V4-001 and SCA-V4-002; DAG-003 (`_DAG/DAG-003/HANDOFF_STATE.md` sha256 `56d849b6d078d8d5…`; held arcs non-gating); DECISION-K3 as revised (`OWNER_DECISIONS.md` sha256 `9d18c40dd7d894dc…`): K-6, K-7 (owner's alternative), K-8 bind this file; DECISION-K1 K1-1…K1-4; R1–R16; R17-1…R17-16 (`R17_RESOLUTIONS.md` sha256 `b0af81bcbad9bc52…`); DECISION-3 (host joins deferred).
- **Consumed inputs** (sha256 by `shasum -a 256` in the working tree at `dc031b5bec`; full values in the return file `D/D5.md`): `BRIEFS.md` `b261394112d7264e…`; `DECISIONS_PENDING.md` `431ec4eb22a0b913…`; `SURVEY/S1-C.md` `06a8a6667ca7c64d…` (Part A whole; Part C); this deliverable's `ScopeOfWork.md` `fe9f9bd923f94ed3…` (SCA-V4-003 revision; re-pinned at pass-4 closeout C1 under R23-5, was `58141169…924a`; SCA-V4-003 blocks read: G-0202-01…09, none requiring a change to this file's design text) and `Dependencies.csv` `be14a079c872695e…`; WD-v0.8 `WORKFLOW_DECLARATION.md` `517821d18fc95830…` (§3.5–§3.9, §6, §7, §8, §9, §12, §13.1); WD-EX-v0.8 `EXAMPLES.md` `275ea54d32cd8f48…` (E1 intro, E3, E4, E5); EXEC-v0.6 `EXECUTION_COMPATIBILITY.md` `64e732d502d0b91d…` (§2.6, §2.7, §3.1, §5, §6, §7.3, §9, §10, U-E19); ACT-POLICY-v0.8 `ACT_AND_POLICY_CONTRACT.md` `6fb6b9e883fa8d20…` (§2.1 A15, §2.4, §2.5, §2.6, §2.8, §4.7, §10.3, FX-56); RS-v0.8 `RECORD_SEMANTICS.md` `b25cc90e9e252f50…` (§4 R2, §6.1, §6.2 HA-10, §10, U-05) and `RS_RECORD.schema.json` `b63a7e421b885854…`; CA-v0.6 `CONNECTED_ACTIVITY_CONTRACT.md` `58167f7accaf356e…` (§2.1 parties, §3, §4, §6, §8.2); HOSTING-BOUNDARY-v0.8 `HOSTING_BOUNDARY.md` `3cf0381c42358fec…` (§8 seams S-6, §8.2, §11, §12); `loop/LOOP_INIT.md` `3790159b4f60bb4f…` ("Develop the detail appropriate to the phase"); DAG-003 `DependencyEdges.csv` `4716ca287d23835c…` and `CandidateEdges.csv` `07b969209e273310…` (arcs naming DEL-02-02, by script). Read in progress, not pinned as a basis: DEL-01-04's node-D3 schemas `aac.offer.schema.json` (`4f1be0814168cf58…`) and `nir.draft-transition.schema.json` (`da2f57c1122d3578…`) and DEL-01-04 `ScopeOfWork.md` `0cdb44e297010b70…` (OUT-004, REQ-003, REQ-004). Historical exemplar (evidence only, never a v4 commitment): App v3 `projects/chirality-app-dev/frontend/src/app/api/working-root/workflow-drafts/workflow-draft-store.ts` `185532db8cddcb39…`, `route.ts` `567789715473356c…`, `components/woven-dialogue/workflow-draft-review.tsx` `b5f4bcfad3429a78…`; Root `AGENTS.md` and `workflows/create-workflow/WORKFLOW.md` as current Root practice (read via the survey, S1-C §A.5).
- **ScopeOfWork reading (R17-15).** The ScopeOfWork lags the owner's answers in four places. This file reads it as follows; precise SCA-V4-003 proposals are in the return file.
  1. REQ-001, OUT-001, AC-001, VER-001 "trial through real native Codex tool execution": read per **K-7** as trial **in an ordinary conversation** with real tools, which is not a run of any workflow identity; only registered revisions run.
  2. REQ-003 "this contract does not select a new overwrite policy": **K-6** has since chosen one (a revision series per library slot; nothing overwritten), which §4.1 designs.
  3. REQ-002, REQ-006, AC-006, CLM-004, REQ-008: registration (A15) is captured by **DEL-01-04's App act control** (K-8; R17-6), bound to the exact reviewed bytes; this deliverable supplies what the control presents (§4.3) and performs the registration that follows.
  4. OUT-002, REQ-004 "host-supplied": the origin value is `host` (WD §6.1, S-D); "host-supplied" is not a value (terminology only).
- **Receivers:** DEL-01-04 (DEP-01-04-009, held), DEL-02-03 (DEP-02-03-010, held), DEL-09-02 (DEP-09-02-016, admitted), DEL-09-06 (DEP-09-06-026, admitted), Suppliers: §7. (The row DEL-02-04 → DEL-02-02 that R17-8 proposed was dropped by R19-7: DEL-02-04 composes role guidance only.)

Beside this file (PROPOSED, R17-1): the schema [workspace-registration.schema.json](workspace-registration.schema.json) with its conformance instances [workspace-registration.valid.examples.jsonl](workspace-registration.valid.examples.jsonl) and [workspace-registration.invalid.examples.json](workspace-registration.invalid.examples.json), and the design prototype [prototype/wrproto.py](prototype/wrproto.py) (not product code; §13).

---

## 0. Reading this file

- The ScopeOfWork states the obligations; this file says how the deliverable meets them at the 60% description of `loop/LOOP_INIT.md`: interfaces, states, data, sequences with failure behaviour, and verification.
- First-increment files have already designed most of this deliverable's interfaces from the consumer side (S1-C §A.2.2): the identity tuple (WD §6.1), the trace links (EXEC §6.1), host → App refinement (EXEC §6.5), the A15 act (ACT §2.1) and its record (RS HA-10). They are **consumed unchanged** and cited by section. What this file adds is the library and draft model itself: slot and revision policy, draft identity and storage, review binding, the registration sequence, collision dispositions, package hygiene, selection, and the joins with DEL-01-03 and DEL-01-04. Edits that the other side now needs are returned as a join list, never made here (R17-14).
- **Not in this file** (and why): visual components and the native draft view (DEL-01-04 OUT-002/OUT-004); plan revision identity (DEL-01-03); the revision digest algorithm (WD U-03, with DEL-04-03); construction and placement of the act control (DEL-01-04; OI-008); shared-type placement (OI-014); host libraries and host precedence evidence (DECISION-3); a checkpoint that requires A15 (ACT §4.1, a possible later extension); the joined V4-EXM-10 witness (DEL-09-02).

## 1. What binds this design

| Source | What it fixes here | Label |
|---|---|---|
| K-6 | A draft made from a registered workflow registers as a **new revision** of it; earlier revisions are kept; every run cites the revision it used; a same-name draft with no such origin is **refused with a request for a new name**; nothing is overwritten | SETTLED |
| K-7 | **Only registered revisions run.** A draft is tried out in an ordinary conversation, which is not a run of any workflow identity. EXEC HR-3, TR-1/T-1 and WD OS-2/OS-3 stand unchanged | SETTLED |
| K-8 | Registration (A15) is performed through **DEL-01-04's person-only act control**, bound to the exact reviewed bytes; a draft changed after review needs a new review | SETTLED |
| R17-4 | Conversation content is read back from Codex; the App keeps only its own records and the pointers it needs, labelled App-observed | DERIVED |
| R17-5 | The Rust host owns record writing; act capture is produced in the host from a native interface event, so no agent tool can operate it | INTEGRATION (PROPOSED placement) |
| R17-8 as amended by R19-1, R19-7 | DEL-02-04 composes **role guidance only** into `developerInstructions` at conversation start; the workflow is supplied per run as a text element of the turn that starts the run, composed by DEL-02-02 (§16); an agent's own read of the file is a tool item, not evidence of supply | INTEGRATION |
| R17-9 | No automatic decline; plan acceptance is ordinary input; untyped sessions are allowed | INTEGRATION |
| R17-11 | WD §6.1 and EXEC HR-4 keep *derived-from* for the parent workflow identity. The A15 record names its subject by the **reviewed draft content** and, for a new revision, the **prior revision** | INTEGRATION |
| K1-1, K1-4 | The agent asks (A8); the product never asks in its place. The person is recorded as the App observes them, "identity not verified" | SETTLED |
| ACT §2.1, §2.6; RS HA-10 | A15 is the person's act; never evidenced by draft creation, a trial, an agent's recommendation, a review of other content, an earlier revision's registration, or a file an agent wrote into a catalog | INTEGRATION (R12-5) |
| WD §6.1 RV-1…RV-5; §6.3 C-1…C-6; §7 | Revision file set and canonicalization; collisions exposed, never rebound; Root package and name conventions kept | PROPOSED in WD; consumed unchanged |
| D3 (DECISION-1) | Tool permission and sandbox modes stay the user's own Codex setting, so the App cannot stop an agent writing into a library folder; it can only make the standing of such content truthful (§4.6) | SETTLED |
| DECISION-3 | Host joins deferred: host listing, relay and precedence are designed only as far as App-side behaviour needs | SETTLED |
| DECISION-L L-2; R19-1, R19-2 | A conversation's role is fixed for its life; **workflows are not bound to a conversation**: runs follow one another in one conversation, (a) sequentially and (b) on the agent's proposal with the person confirming; one run at a time; (c) declared chaining is DEL-02-01's later work | SETTLED scope, INTEGRATION design |
| R19-7 | A workflow is supplied as a text element of the turn that starts its run, carrying the registered revision's exact bytes framed by App-written lines; DEL-02-02 composes it; DEL-02-03 starts the run; the bytes and their identity are recorded per run and checked against Codex's history (`thread/items/list`, R21-4); no workflow is placed in a discovered skill root; `thread/settings/update` is not used | INTEGRATION (after OBS-3) |
| DECISION-L L-4 A (clarified); R19-4 | Shipped workflows are registered by the release; entries byte-equal to a shipped revision are recognized; the rest are registered in place, several per act, each entry's bytes bound | SETTLED |
| R18-1 C-01, C-02 | The persisted A15 form is RS's; `draft_transition` carries the A15 record and revision | INTEGRATION |

## 2. Objects and identities

### 2.1 Vocabulary

| Term | Meaning in this file |
|---|---|
| **Library** | A place that holds registered workflows for one origin and source root: a project library (origin *project*, the project root), the user library (origin *user*), the App bundle (origin *bundled*, per release), a host library (origin *host*, deferred). WD §6.1 "source root" |
| **Slot** | {origin, source root, name}: one workflow name in one library. A tuple without revision names a slot, not content (WD §6.1) |
| **Revision** | The exact content registered in a slot, identified by its content identity (WD §6.1 RV-1…RV-5; algorithm U-03). A slot holds an ordered **series** of revisions (K-6), numbered 1, 2, … by the App (the *sequence*, a display aid; identity is the revision value) |
| **Revision store** | Where every registered revision's bytes are kept, immutable (§3) |
| **Published copy** | A copy of a slot's latest revision at the Root location `…/workflows/<name>/`, kept for portability. Never authority (§3, LS-3) |
| **Draft** | A package folder under `…/workflow-drafts/<name>/`. It has **no workflow identity** (EXEC TR-1, HR-3). It is named by its *draft key* {draft location (*project* · *user*), draft root, name} and its content by a **draft content identity**, computed over the folder by the same RV-1…RV-5 rules as a revision |
| **Draft base** | The full tuple (with revision) of the workflow a draft was made from, recorded **by the App** when the App made the draft (Refine, Open and refine, Review to register). A draft the agent or person wrote from scratch has none (SP-3) |
| **Target slot** | The slot a draft would register into: the library of the draft's location, under the draft's folder name (SP-2) |
| **Review snapshot** | A copy of the draft's regular files taken when a review is shown; the bytes the person reviews and the bytes registration publishes (RB-1, RB-6) |
| **A15 descriptor** | What the workspace hands DEL-01-04's act control so it can present and capture A15 (RB-4) |
| **Registration ledger** | The library's append-only list of registration outcomes, each citing its A15 record (§3; `library_entry`) |
| **Selection** | The person's explicit interface choice of a full tuple with revision (SL-1) |
| **Trial** | Trying a draft in an ordinary conversation (K-7; TT-1…TT-6) |

### 2.2 Identity rules

- **ID-1 (DERIVED, K-6 with WD §6.1).** A registered revision's tuple is {workflow, origin of the library, source root of the library, name, revision} with `revision_method`, plus **derived-from = the draft base** when the draft had one (SP-6). The tuple is WD's `$defs/workflow_identity`, referenced by its `$id` from this file's schema; RS spells it `workflowTuple`.
- **ID-2 (DERIVED).** Because the revision value is a content identity over the package's files (RV-1…RV-5), and a draft's content identity is computed over the draft folder by the same rules, **the revision registered from a draft equals the reviewed draft content identity**. This is what makes K-8's "bound to the exact reviewed bytes" checkable: the A15 binds one value that is both.
- **ID-3 (PROPOSED; used by C-01).** A draft is referred to as `draft:<location>:<name>@<content identity>` wherever a string is needed. A library entry reviewed in place without a draft (§4.7) is `entry:<location>:<name>@<content identity>`. This string is `relations.reviewedDraft.draft` in the persisted A15 form RS defines (R18-1 C-01; F row FR-06). A reference without a content identity names a folder, not content.
- **ID-4 (DERIVED, EXEC §6.6).** Lineage is followed through derived-from links; a link that cannot be resolved is shown as "lineage incomplete at ‹tuple›", never guessed.

## 3. Layout and data placement (PROPOSED; RS U-05 stays open; OI-008 ruled by the owner for the draft workspace, §11)

| Item | Where (project library; the user library has the same layout under `~/.chirality/`) | Written by | Standing |
|---|---|---|---|
| Drafts | `<project>/.chirality/workflow-drafts/<name>/` (Root convention, AGENTS.md "Skills and workflows") | The agent (Codex file tools), the person, or the App (Refine, Open and refine, Review to register) | Work in progress; not a workflow identity |
| Draft bases | App data folder, keyed by draft key | The App only | App-kept pointer (R17-4); lost if the App data is lost — then the draft has no base (U-WR-12) |
| Review snapshots, staging | `<project>/.chirality/.workflow-staging/` | The App | Temporary; removed after the attempt closes |
| Revision store | `<project>/.chirality/workflow-revisions/<name>/<revision key>/<name>/` | The App's registration writer | Immutable once committed; the source of every resolution (SL-4) |
| Registration ledger | `<project>/.chirality/workflow-registry.jsonl` | The App's registration writer | App-written record of outcomes; "registered" standing needs it **and** the A15 record **and** bytes that recompute (LS-1) |
| A15 records | The library's act log, `<project>/.chirality/records/acts.jsonl` in the prototype; the location is RS U-05's | DEL-01-04's act control through the RS writer | Human-act record (RS §6.1) |
| Published copy | `<project>/.chirality/workflows/<name>/` (Root convention) | The App, after commit | Derived convenience for portability and Root-compatible readers; never authority; differences are reported (LS-3) |
| Kept-aside unrecorded content | `<project>/.chirality/workflow-unrecorded/<name>/<content key>/` | The App, when publishing would otherwise replace unrecorded content | Preserved, never deleted by the App (REQ-003) |
| Selection records | Handed to DEL-02-03 and DEL-04-03 at run start (RS R2 *selected*); the App keeps the current selection per conversation as a pointer | The App | RS's record once written |
| Trial pointers | App data folder (the App writes each as one create-once WR `trial_pointer` file under `runtime/wr/trial-pointers/`, beside the draft bases in `runtime/wr/draft-bases/`) | The App (Rust host, §11) | App-observed pointer; not a run record (TT-4) |
| Bundled workflows | Inside the App bundle, per release, read-only | The release | Origin *bundled*; runnable without A15 (LS-5) |
| Shipped-revision manifest (v0.2, L-4) | Inside the App bundle | The release | Name and revision of every workflow revision any v4 release shipped; used only to recognize library copies (LS-8) |
| Run texts and supply checks (v0.2, R19-7) | `run_text` and `supply_check` records handed to DEL-02-03 and DEL-04-03 (RS R3); the composed text itself is not stored twice: it is recomputable from the record's lines and the revision's bytes in the store, and Codex keeps it in its history (read back with `thread/items/list`, R21-4) | The App | App records (R17-4); the text in Codex's history is Codex's |
| Host workflows held in the App | An import holding library (CA's LIB-A2 ⟨fx-app-import⟩), `<project>/.chirality/workflow-imports/<host source root>/<name>/` | The person's relay (DEP-001) | Origin *host*; listing and relay deferred (DECISION-3) |

Project-library records travel with the project folder, as RS OF-9 asks of App run records. The App cannot stop an agent writing into these folders (D3). It therefore never treats the presence of files as registration, and it computes standing from the ledger, the act record and the bytes together (§4.6).

## 4. Policies

### 4.1 Slot and revision policy (K-6)

- **SP-1 (SETTLED, K-6).** A slot holds a series of registered revisions. The App never overwrites or deletes a revision; every earlier revision stays resolvable and selectable.
- **SP-2 (PROPOSED).** A draft's target slot is the library of its location (project drafts → that project's library; user drafts → the user library) under its folder name. To register elsewhere or under another name, the person moves or renames the draft, which the review then shows.
- **SP-3 (PROPOSED; reading of K-6 "made from").** A draft is *made from* the target slot when its App-recorded draft base is a revision of that slot, **or** the base's derived-from lineage (ID-4) reaches a revision of that slot. The second limb is the round trip: a host adaptation of ⟨rev-A2⟩, refined in the App, registers back into LIB-A1 as its next revision, as CA §4, EXEC RT-6 and WD-EX E3 already assume. A base claimed by the draft's own files, or written by an agent, is not a draft base.
- **SP-4 Dispositions** (`registration_disposition.disposition`):

| Code | Condition | Effect | Message (substance) |
|---|---|---|---|
| **DS-1 new workflow** | The target slot has no registered revision and no unrecorded content | First revision; prior revision none | "Registers a new workflow ‹origin›:‹name›" |
| **DS-2 new revision** | The slot has registered revisions and SP-3 holds | Next revision; prior revision = the slot's **latest** revision at review | "Registers revision ‹n+1›; earlier revisions are kept" |
| **DS-3 refused: name taken** | The slot is not empty and SP-3 fails (no base, a base elsewhere, or lineage not established) | Nothing registered; library unchanged | "A workflow named ‹name› already exists in this library and this draft was not made from it. Choose a new name for the draft." (K-6) |
| **DS-4 refused: identical content** | The reviewed content equals a revision ‹k› already registered in the slot, and ‹k› is selectable in this App process or its standing is not LS-1 (§4.8 RC-1, RC-2; CC-WR-RECONFIRM) | Nothing registered | "Identical to revision ‹k›; select it instead". When ‹k› is not LS-1 the message names its standing and exact cause instead (for LS-4, "registration record incomplete: ‹cause›"), and LS-4's route applies: the record or bytes are restored (§5.3), after which DS-8 applies |
| **DS-5 refused: draft not valid** | A refusing hygiene finding (HY-1…HY-5, HY-7) | Nothing registered | The findings |
| **DS-6 refused: changed since review** | The live draft changed while the snapshot was taken | Nothing registered | "Review again" |
| **DS-7 in place** | The slot holds content with no registration record (LS-2) and the draft is identical to it | First revision; the slot's bytes unchanged | "Registers the content already in this slot" |
| **refused: slot moved on** | Between review and publication another revision was registered in the slot (§6 G-1) | Not completed; the A15 stands, recorded as not effective | "Another revision was registered after this review; review again" |
| **DS-8 re-confirmation** (CC-WR-RECONFIRM) | The reviewed content equals revision ‹k› registered in the slot, ‹k› has LS-1 standing as read (§4.6), and ‹k› is **not** selectable in this App process (§4.8 RC-1, RC-2) | No new revision; on a new A15, revision ‹k› is re-confirmed for use in this App process (§4.8) | "Identical to revision ‹k›, registered earlier (not verified in this session). Re-confirm revision ‹k› for use in this App session; no new revision is registered" |

- **SP-4a Order (CC-WR-RECONFIRM; PROPOSED).** A review decides DS-5 and DS-6 first. For a slot with registered revisions it then applies SP-3, unchanged: when SP-3 fails the disposition is DS-3 (K-6), whatever the content. Only then is identical content decided (DS-4, or DS-8 per §4.8), and otherwise DS-2. For a slot with no registered revision, DS-1 and DS-7 apply as before. This keeps K-6's refusal of a same-name draft with no such origin for identical content too (U-WR-23, closed: the route is Refine, RF-1).

- **SP-5 (PROPOSED).** Every review also lists the same name in **other** libraries and origins, each with its holding library and standing (C-1). This is a notice ("shadows bundled create-workflow"), not a refusal: a selection holds a full tuple, so a new same-name entry rebinds nothing (C-2).
- **SP-6 (PROPOSED; R17-11).** A new revision's derived-from is its **draft base** (none when there is no base). The prior-revision link is separate: it is the slot's latest revision at review, recorded in the A15 relations and the ledger. For a refinement made from the latest revision the two name the same tuple; for a stale base or a round trip they differ, and both are shown.
- **SP-7 (PROPOSED).** A draft made from an earlier revision than the slot's latest (a stale base) may still register as DS-2. The review states "made from revision ‹i›; the latest is revision ‹j›; changes in ‹j› are not in this draft" and shows the difference against both. Nothing is lost, because ‹j› stays.

### 4.2 Drafts and trials (K-7)

- **TT-1 (SETTLED).** Only registered revisions (and bundled or host-listed workflows, LS-5, LS-6) are selectable for a run. Selecting a draft is refused with EXEC T-1's words, "draft only — not a workflow identity", and the offer to review it.
- **TT-2 (DERIVED).** A draft is tried in an **ordinary conversation**: no workflow is selected, no run is opened (no RS `run_opened`), DEL-02-04 composes no workflow into the conversation's instructions (R17-8), and EXEC's recorder records no checkpoint arrival, because there is no run. The agent works with real native tools, which is V4-EXM-10's "trial"; its reading of the draft file is a tool item.
- **TT-3 (PROPOSED; confirmed by R18-1 C-14).** The workspace offers **Try in a conversation** on a draft. It opens a new conversation with no workflow selected; the role and model are chosen as for any conversation (DEL-02-04; K-3: no model until the person chooses; the conversation reads "not started — no model selected" until then, R18-2). The App pre-fills, and does not send, the person's message with the draft's `WORKFLOW.md` attached as a text element, exactly as NIR-v0.2 §6 AT-8 says (any other text file of the draft also as a text element, AT-9; any other file named, AT-10; each with its NIR supply record, AT-3, shown as "not a registered workflow; this conversation is not a workflow run"); the person edits and sends it (R21-5). Once sent, the message and its attachments are the person's own: no run is opened, no workflow is supplied and no run-start text is composed. A draft reaches a trial only as a message or attachment the person sends; it is never composed into guidance and never framed as a run text (§16 applies to registered revisions only). **Pending owner decision: the App departs from this confirmed text (U-WR-24).** The text above stands as confirmed (R18-1 C-14; R21-5); it has not been rewritten. The App currently does the following instead:
  - **Try in a conversation** opens no new conversation. It adds the draft's text files to the person's attachment list, each with its AT-8 draft element. The person then starts or chooses an ordinary conversation, choosing role and model as for any conversation (K-3), and sends.
  - The host refuses draft files for a conversation that has a workflow run in force in this App process (TT-2).
  - A non-text file of the draft is listed "not attached". It is not named under AT-10.

  The reasons are as follows. The App has no conversation that exists before `thread/start`, so a "not started — no model selected" conversation (R18-2) would be a new conversation state owned by DEL-01-04 and DEL-01-02. The AT-10 named-path carrier is not yet supplied by DEL-01-04's attachment producer and custody, which carry text elements only.
- **TT-4 (PROPOSED).** The workspace keeps a **trial pointer** {draft key, draft content identity at the time, conversation, time}, labelled "draft tried in conversation; not a run of any workflow identity". It is not a run record, not compatibility evidence and not A15 evidence (ACT §2.6 lists "a successful trial run" among non-evidence; under K-7 there is no trial run at all).
- **TT-5 (DERIVED).** A human act performed during a trial conversation (for example A4 on an App file through the act control) is recorded outside any run, in the act log, as for any conversation.
- **TT-6 (DERIVED).** Checkpoints declared in a draft are not evaluated in a trial. The review shows the declared part's reading (WD VO-1…VO-10); a run of the registered revision is where checkpoints are recorded (EXEC §2.4).
- **TT-7 (PROPOSED).** Each refinement that needs a recorded run is registered first, as a new revision (K-6); "refine twice" (V4-EXM-10) is two registered revisions, each run on new inputs.

### 4.3 Review binding and the registration act (K-8; R17-11)

- **RB-1 Snapshot.** Opening a review copies the draft's regular files into staging, computes the content identity of the copy, recomputes the live draft's identity after copying, and compares both with the identity shown in the draft list. Any difference: DS-6, "the draft changed while it was read; review again". (App v3 made the same check; §10.)
- **RB-2 Review package** (what the review view shows; DEL-01-04 presents it, §7): the target slot and disposition (SP-4) with its message; the reviewed content identity and method; the file list with per-file sizes and digests; `WORKFLOW.md`; the declared part's reading with its FB findings (WD §3.7), shown as information; hygiene findings; the difference against the prior revision and, when it differs, against the draft base; lineage; the same name elsewhere (SP-5); and the sentence "Registering makes this revision available in ‹library›. It is not a check that the workflow can run here." A compatibility report (EXEC CK-1) may be shown beside it, labelled as a check of this environment (REQ-005).
- **RB-3 Freshness.** The review stays current while (a) the live draft's content identity equals the snapshot's and (b) the slot's latest revision is still the prior revision bound (or the slot is still empty). The workspace watches both. When either fails it withdraws the A15 descriptor, the act control stops offering it, and the draft shows "changed since review — review again" (K-8). For DS-8, (b) compares the slot's latest revision with the descriptor's `freshness.slot_latest`, not with its prior revision, and two more conditions apply (§4.8 RC-5; CC-WR-RECONFIRM).
- **RB-4 A15 descriptor** (`a15_descriptor`), handed to the act control for a registrable disposition (DS-1, DS-2, DS-7): act kind A15; wording "register workflow revision"; subject = the target tuple with the revision (ID-1); bound content = the snapshot's content identity (equal to the subject's revision, ID-2; a reader check); relations {reviewed draft (draft key and content identity), prior revision (tuple or none), derived-from (tuple or none)}; disposition; scope = the library; purpose "make it available in the project library" or "make it available in the user library" (ACT's single "in the project" wording does not fit the user library; join J-15); review reference; freshness values; and the agent's A8 request record, where one was recorded (RS R16). For DS-8 the descriptor takes the re-confirmation form of §4.8 RC-4 (CC-WR-RECONFIRM): its own wording and purpose, subject the registered revision ‹k›, and `reconfirms`.
- **RB-4a Persisted form (R18-1 C-01).** The A15 record itself is RS's: `relations.reviewedDraft` = {`draft`: the ID-3 string, `content`: the reviewed content identity} and `relations.priorRevision` = the prior revision as RS's `workflowTuple` (camelCase), or null for a new workflow or an in-place registration. WR's descriptor keeps its snake_case object; the act control's writer maps it (WD §3.6's one-to-one spelling). WD's derived-from stays in the subject tuple and is not an act relation (C-21). For a multi-entry act (§4.7) RS-v0.9 carries `relations.registeredEntries`, one {subject, reviewedDraft, priorRevision} per entry in the order of `boundSubject`; WR writes it so. RS-v0.9's `reviewedDraft.draft` pattern, `^(draft|entry):(project|user):[^@]+@.+$`, admits both ID-3 forms, and DEL-01-04's act control (AAC-v0.2 §4.2, schemas 0.3, RV21) takes this file's descriptors as they are, one per act, with `entry:` strings and the plural wording (R21-3; its prototype check K-17 runs this file's two descriptor examples through the offer and the capture into RS's writer).
- **RB-5 Capture (DEL-01-04).** The act control captures A15 only from the person's native interface event (R17-5; CAP-4). The agent may ask the person to register (A8; K1-1); an answer to a supplier user-input or elicitation request is never A15 (CAP-6); a chat statement is not either (CAP-7). The control records the person as the App observes them, "identity not verified" (K1-4).
- **RB-6 Publication uses the snapshot.** The registration writer publishes the snapshot's bytes, never the live draft's, after re-checking the slot (G-1). The bytes registered are therefore the bytes reviewed, whatever happens to the draft afterwards.
- **RB-7 Review is not an act.** Showing a review is an App presentation, recorded as a `review shown` transition. It is never recorded as a human act (ACT §2.1: "a draft's review is not A15"). REQ-002's "the person reviews the identified content" is evidenced by the A15's binding to the content the review showed (S1-C §A.4 item 5, option (a); INTEGRATION), not by a separate act kind.
- **RB-8 One act, the revisions it names (PROPOSED; v0.2 widened for L-4).** An A15 completes at most the registrations its descriptor names: one for an `a15_descriptor`, one per entry for an `a15_multi_descriptor` (§4.7). An act whose registration did not complete is recorded as not effective and is never reused for other content or a later attempt (FX-56 (c); VER-002). The only continuation is §6 SQ-X, which finishes the same attempt after an interruption when nothing has changed, and never a re-confirmation (§4.8 RC-7). A re-confirmation (§4.8; CC-WR-RECONFIRM) is one such attempt: its A15 completes at most the re-confirmation of the one revision it names.

### 4.4 Selection (WD C-1…C-6; U-10)

- **SL-1 (DERIVED, C-2, C-3).** A selection is the person's explicit interface choice of a full tuple **with revision**, with its holding library. It is an ordinary interface choice, not a reserved act. An agent's mention or suggestion of a workflow is not a selection.
- **SL-2 Pinned (PROPOSED; answers WD C-4 for the App).** A selection stays on its revision. When a newer revision is registered in the slot, the selection shows "newer revision ‹n› available"; following it is a new selection event citing the one it replaces (C-3). The chain therefore always shows which revision was resolved and supplied (C-4), and every run cites its revision (K-6).
- **SL-3 Unqualified names (PROPOSED; answers WD C-5 / U-10 for the App).** A name typed without origin gives a candidate list ordered project → user → bundled → host (host last). When more than one origin holds the name the person picks; nothing is resolved silently. Host listing waits with the host joins (DECISION-3).
- **SL-4 (DERIVED, C-2; EXEC RF-2, FB-08).** Discovery changes after selection (new same-name entries, a new revision, an edited or removed published copy) never change the selection. A selection is resolved from the **revision store**, never from the published copy (v0.2 exception: an LS-8 copy recognized as a shipped revision is resolved from its holding library and verified against that revision, as any holding library is); if its bytes cannot be found or do not recompute, the result is "selected revision not resolvable" or "revision not verified", never a substitute.
- **SL-5 (SETTLED, K-7).** Content without registered standing (a draft; LS-2, LS-3, LS-4) is refused for selection with its standing and the offer **Review to register**.
- **SL-6 (DERIVED).** Reuse on new inputs is a run of a selected revision, started through DEL-02-03 (EXEC SQ-A A-1, A-2); the inputs are conversation inputs.
- **SL-7 Selection for a chained run (v0.2; R19-2).** Selecting the next workflow in a conversation whose earlier run has ended records `prior_run` {run, workflow, how it ended} as a relation; it is not part of the selected identity. A selection made by confirming an agent's proposal records `how` = "agent proposal confirmed by the person" and the `proposal` (conversation, agent message item, proposed name); the proposal alone is never a selection (§16.5).

### 4.5 Package hygiene at review (WD RV-2 and "Whether registration refuses them is DEL-02-02's")

| ID | Rule | Effect | Label |
|---|---|---|---|
| HY-1 | A regular `WORKFLOW.md` at the package root | Refused without it | DERIVED (WD §7, package convention) |
| HY-2 | Folder name follows WD's name rule (1–64 lowercase letters or digits in hyphen-separated segments) and equals the front-matter `name` | Refused otherwise | PROPOSED (WD §7 keeps both conventions; WD's prototype only notes a mismatch) |
| HY-3 | No symbolic link or other non-regular entry anywhere in the package | Refused (the revision is not established, RV-2) | DERIVED |
| HY-4 | No operating-system files (`.DS_Store`, `._*`, `Thumbs.db`, `desktop.ini`, `Icon\r`, `.localized`, `.Spotlight-V100`, `.Trashes`, `.fseventsd`, `__MACOSX`) | Refused, naming them; the person removes them and reviews again. Other hidden files are allowed and listed | PROPOSED |
| HY-5 | At most 16 MiB and 1 000 files | Refused above the bound | PROPOSED (App v3 bounded its listing at 16 MB) |
| HY-6 | Declared-part findings (FB codes) | Shown in the review; **never** refuse registration (registration is not compatibility, REQ-005; WD E5 shows a prose-only workflow is valid) | DERIVED |
| HY-7 | `WORKFLOW.md` is UTF-8 | Refused otherwise (WD CR-5 reads the block as UTF-8) | PROPOSED |

### 4.6 Library standing

| ID | Standing | Condition at read | Runnable | Offered |
|---|---|---|---|---|
| **LS-1** | registered | A ledger entry *registered*, its A15 record found with the same bound content, and store bytes that recompute to the revision | Yes, in an App process that holds its registration or re-confirmation result (§4.8 RC-2; CC-WR-RECONFIRM) | Select (in such a process); Refine (in any process, RF-1); in another process, re-confirmation through a draft with its bytes (DS-8) |
| **LS-2** | present without registration record | Content in the published-copy location of a slot with **no** registered revision (an agent or the person wrote it; a Root-era or App v3 library) | **No** (K-7) | Review to register (DS-7 in place) |
| **LS-3** | library copy changed outside registration | The published copy differs from the slot's latest revision | The registered revisions stay runnable; the changed copy is not | Review the change (a draft with base = the latest revision, DS-2). On the next publication the changed copy is kept aside, never overwritten |
| **LS-4** | registration record incomplete | A ledger entry whose A15 record is missing or bound to other content, or whose store bytes do not recompute | No; "revision not verified" | Review to register |
| **LS-5** | bundled | Shipped in the App release | Yes | Select; Refine into the user or a project library (a new workflow with derived-from the bundled tuple) |
| **LS-6** | host-listed | Listed from a host library or held in the import holding library | Per host rules (deferred) | Open read-only; Refine (EXEC HR-1…HR-4) |
| **LS-7** | not established | A non-regular entry in the store or published copy (RV-2) | No | — |
| **LS-8** (v0.2; L-4 A) | shipped revision held in this library | Content in a slot with no registered revision whose content identity equals a revision of the **same name** that an App release shipped (the release's shipped-revision manifest, which lists the revisions every v4 release shipped; PROPOSED) | Yes, at once: selected as the **bundled tuple** of that revision (origin *bundled*, source root the shipping release), with this library as the holding library (WD C-6: the same content located twice). No A15: the release registered it | Select. Editing the copy makes it LS-2 |

LS-2's "not runnable" follows K-7's "only registered revisions run". **Settled by DECISION-L L-4 A as clarified:** shipped workflows are registered by the release and are not affected (LS-5); entries byte-equal to a shipped revision are recognized (LS-8); the rest are registered in place, several per act allowed (§4.7). U-WR-4 is closed.

**LS-1 after a relaunch (CC-WR-RECONFIRM; INTEGRATION).** LS-1 is read from the ledger, the A15 record and the bytes, and is shown as read. While SEAL-2 is deferred, a revision is selectable only from a registration or re-confirmation result held in this App process (§4.8 RC-2). After a relaunch an LS-1 revision is listed "registered — re-confirm to use in this App session"; a draft with its bytes that SP-3 admits reviews as DS-8: the registered draft left unchanged (§5.1), or a draft made by Refine (RF-1) and left unchanged. The standing value stays *registered*.

- **RF-1 Refine without a selection (CC-WR-RECONFIRM; INTEGRATION: HELP_HUMAN ruling on U-WR-21, 2026-10-07).** Refine is offered on any LS-1 revision, whether or not it is selectable in this process, including a revision registered in place (§4.7). It needs no selection and makes none. It recomputes the revision's store bytes, copies its regular files from the revision store into a new draft (SQ-D D-1), and the App records the revision as the draft's base. That base is an App-recorded fact read from the ledger at that time, not authority: the review shows it as App-recorded and freezes it (RB-2). Left unchanged, the draft reviews as DS-8 (or DS-4, RC-1); changed, as DS-2. Store bytes that do not recompute give no draft (LS-4). Re-confirmation from the listing without a draft is deferred (U-WR-21).

### 4.7 Registering several library entries in one act (v0.2; L-4 A; PROPOSED)

- **ME-1.** **Review library entries** lists the LS-2 entries of one library. The person picks two or more; each must pass HY-1…HY-5, HY-7 (refusing findings exclude the entry, named). An entry that is LS-8 is not offered (it already runs).
- **ME-2.** One review shows every picked entry with its own review package (RB-2, without a draft or base: the reviewed content is the entry's own bytes, ID-3 `entry:` form). Snapshots are taken per entry (RB-1).
- **ME-3.** One `a15_multi_descriptor` goes to DEL-01-04's act control (AAC-v0.2 §1.2, §4.2: one descriptor per act, R21-3), wording "register workflow revisions", listing each entry with its subject tuple and bound content; purpose "make them available in the project library" (or user library). The control presents the list and captures one A15 whose `boundSubject` and `boundContent` hold one item per entry, in order (RS §6.1 already allows lists), with `relations.registeredEntries` (RB-4a).
- **ME-4 Freshness.** While the descriptor is offered, any entry whose bytes change, or which gains a registration, makes the whole descriptor stale: the control refuses capture and asks for a new review (K-8).
- **ME-5 Per-entry publication.** After capture, each entry goes through G-1 (still the bound bytes and still unregistered), G-2/G-3 from its snapshot, and G-4: a `library_entry` *registered* (disposition *in place*, sequence 1, `reviewed_entry`) or *not completed* with its reason, every line citing the one A15. An entry changed between capture and publication is *not completed* and needs its own review; the others register. The published copy is left as it is (it equals the registered bytes).
- **ME-6.** The A15 is never extended to entries it did not list, and an entry's not-completed line is never completed later by the same act (RB-8).

### 4.8 Re-confirming a registered revision for use (CC-WR-RECONFIRM; PROPOSED)

The owner chose **"A15 re-confirmation now (Recommended)"** on 2026-10-07 (run `APP-V4-GROUP-A-20261004`, `OWNER_DECISIONS.md`, "Rerunning an unchanged workflow after relaunch"): a new genuine A15 may re-confirm identical bytes after the original in-process registration is gone; trust rests on the new act, not on a replay; SEAL-2 stays deferred. That choice is SETTLED; the design below is PROPOSED. It answers `app/CONTRACT_ISSUES.md` CI-21 (b).

- **RC-1 When it is offered.** A review (SQ-R) of a **draft** has disposition **DS-8 re-confirmation** when SP-3 holds for the slot (SP-4a), the reviewed content identity equals the revision value of a *registered* ledger line ‹k› of the target slot, ‹k› has **LS-1 standing** as read (its A15 record found with the same bound content, and store bytes that recompute; §4.6), and ‹k› is **not selectable in this App process** (RC-2). While ‹k› is selectable in this process, DS-4 stands ("Identical to revision ‹k›; select it instead"). When ‹k› is not LS-1 (LS-4: the act record missing or bound to other content, or the store bytes missing or not recomputing), DS-4 stands with ‹k›'s standing and exact cause: a re-confirmation never repairs a record or a store, and LS-4's route applies (the record or bytes are restored, §5.3; then DS-8). ‹k› may be any registered revision of the slot, not only the latest (SP-1). One draft per act, through an `a15_descriptor`. A draft with ‹k›'s bytes can be made by Refine (RF-1), also for a revision registered in place (§4.7); re-confirmation from the listing without a draft is deferred (U-WR-21).
- **RC-2 Selectable in this process (INTEGRATION: the owner's SEAL-2 deferral of 2026-10-05; AAC §4.4, §5.2a; `I2-SELECTION-AUTHORITY-ROUTE.md`).** A registered revision is selectable (SL-1, TT-1) in an App process only while the App holds, in that process, the result of its registration (G-4) or of its re-confirmation (G-4R), whose A15 the act control captured in that process (AAC §4.2). The App holds that result in memory. It ends with the process and is never rebuilt from the ledger, the act log, a capture or any other record read from disk. LS-1 is still read and shown (§4.6), but while SEAL-2 is deferred it gives no selection after a relaunch. If a custody mechanism that establishes native capture origin across a relaunch is adopted later (SEAL-2 or another; AAC U-AAC-3; RS U-32), a revision whose standing it verifies counts as selectable and DS-4 applies; re-confirmation stays the route whenever that verification is absent or fails.
- **RC-3 Same revision, no new identity.** A re-confirmation registers nothing new: no tuple, revision value, sequence, store folder or published copy. Its subject is ‹k›'s tuple exactly as ‹k›'s registered ledger line records it, derived-from included. The revision value is the content identity of the package's files, and the reviewed bytes are ‹k›'s, so a "new revision" would carry ‹k›'s identity a second time (ID-1, ID-2; §2.1 "identity is the revision value"). A slot holds a series of distinct revisions, never overwritten (SP-1), which DS-4 already protects. The selection, the run and their records then cite ‹k› exactly as after the original registration (SL-1, SL-2; K-6 "every run cites the revision it used"; EXEC A-1, §6.1 *selected*, *resolved*; RS R2), so no consumer of selection or revision identity sees a change. A recorded draft base is shown in the review and does not change ‹k›'s tuple.
- **RC-4 The act.** A genuine A15 at DEL-01-04's act control, captured only from the person's native interface event (K-8; RB-5), composed from one `a15_descriptor` with: disposition *re-confirmation*; wording "re-confirm workflow revision for use"; subject ‹k›'s tuple; bound content the reviewed content identity, equal to ‹k›'s revision (ID-2); relations {reviewed draft: this draft, ID-3 `draft:` form; prior revision: ‹k›'s own prior revision as its registered line records it, null for a first revision; derived-from: ‹k›'s}; `reconfirms` {‹k›'s tuple, the registered line's `ledger_seq` and `sequence`}; purpose "make it available again in this App session from the project library" (or "… from the user library"); scope, review reference and freshness as RB-4. The descriptor's prior revision is ‹k›'s own, not the slot's latest, because RS reads it as "the revision this one follows in its slot"; SP-6's prior-revision link (the slot's latest at review) does not apply, since a re-confirmation follows nothing. The slot's latest at review is carried in `freshness.slot_latest`, against which RB-3 (b) and G-1R compare (RC-5). The review's `registration_disposition.prior_revision` keeps its meaning for every review, the slot's latest revision at review; the revision re-confirmed is named in its `reconfirms`. The control's statement names ‹k› and says that no new revision is registered, in substance: "Re-confirm revision ‹k› of ‹origin›:‹name› for use in this App session. This registers no new revision." (the statement's placement is DEL-01-04's).
- **RC-5 Freshness.** RB-3 (a) applies unchanged. For DS-8, RB-3 (b) is read against `freshness.slot_latest`: the descriptor stays current while the slot's latest revision is still the one recorded there at review (or the slot still has the same latest), never against the descriptor's `relations.prior_revision`, which is ‹k›'s own prior (RC-4). A DS-8 descriptor is also current only while (c) the registered line ‹ledger_seq› still reads with ‹k›'s tuple and ‹k› still has LS-1 standing, and (d) ‹k› has not become selectable in this process. When any condition fails the descriptor is withdrawn and the act control captures nothing (AAC AX-06).
- **RC-6 Re-confirmation sequence** (SQ-G's steps, reused), after the act control reports a capture naming the descriptor:

| Step | Action | Failure · record · next |
|---|---|---|
| G-0 | As SQ-G G-0 | As G-0: nothing happens |
| G-1R | Under the ledger lock, held to G-4R: the slot's latest is still `freshness.slot_latest`; the registered line ‹ledger_seq› still reads with ‹k›'s tuple, and its A15 record is still found with the same bound content; ‹k› is still not selectable in this process | Slot moved on → *not completed* "slot moved on"; line changed or missing → *not completed* "registered line ‹ledger_seq› no longer reads as reviewed"; act record no longer found → *not completed* "revision ‹k› registration record incomplete: ‹cause›"; ‹k› became selectable → *not completed* "revision ‹k› already selectable in this App session"; each citing the A15 · review again, or select ‹k›. Ledger unreadable or malformed → the attempt stays pending with the exact cause (new WR text, adopting the App's existing pending behaviour) |
| G-2R, G-3R | ‹k›'s store folder still recomputes to ‹k›; the attempt is then *stored* (attempt journal, §5.2) | Recomputes → continue. Otherwise (absent, other bytes, or not recomputing) → *not completed* "revision ‹k› store no longer recomputes" (LS-4). A re-confirmation never creates, rewrites or repairs a store folder |
| G-4R | Under the same lock, append `library_entry` *re-confirmed*: ‹k›'s identity, sequence, prior revision and store path; disposition *re-confirmation*; `reconfirms`; the reviewed draft; the new A15 record and capture-evidence references | **Commit point.** As G-4, a lock held by another writer waits. New WR text, adopting the App's existing behaviour: an uncertain write keeps the intended line in this process and rereads it without appending a duplicate; nothing is selectable until the line is durable |
| G-5 | Does not apply: a re-confirmation publishes no copy | A stale published copy is X-3's |
| G-6R | Transition *re-confirmed* with `a15_record` and `revision` (‹k›); DEL-01-04 informed; the App records ‹k› as the draft's base; the App holds the result, so ‹k› is selectable in this process (RC-2) | — |

- **RC-7 Failure behaviour.** Bytes changed between review and act: the act control captures nothing (AAC AX-06; K-8); review again. The person closes or dismisses the control: nothing is captured, the attempt is *withdrawn* and nothing is inferred (AAC §4.2 step 3; A15 has no decline). The A15 record write fails: AAC §4.2 step 6 (a late write from the capture kept in this process); G-0 waits for the capture report. A failure at G-1R, G-2R or G-3R: *not completed* citing the A15; the act stands and had no effect (AAC AK-f). The process is lost **before the attempt is *stored*** (from capture to G-3R): WR has no attempt journal for it and writes nothing at relaunch; AAC §4.4 governs the capture. The process is lost **after the attempt is *stored* and before G-4R is known durable**: at relaunch SQ-X X-2 first rereads the ledger for a line citing the attempt's A15. If one exists it writes nothing and closes the attempt; otherwise it writes *not completed* "process lost before re-confirmation committed", citing the A15. Either way ‹k› is not selectable in the new process, and one act never has two ledger lines (RC-9). X-2 never completes a re-confirmation, because its only effect, selectability in that process, ended with the process. A re-confirmation that did not complete is never completed later by the same act (RB-8); re-confirming again needs a new review and a new A15.
- **RC-8 What it is not.** It is not cold replay. The earlier registered line, its act reference and its capture are read only as disclosed facts, labelled "registered earlier; not verified in this session", and are never authority. Nothing makes the earlier act, its capture or any receipt trusted, now or after a later relaunch, and a *re-confirmed* line read from disk after a relaunch is itself an ordinary record read cold (RC-2). It does not satisfy CI-10 or I3-CUST (trustworthy persistent replay stays required), does not change SEAL-2 (deferred) or AAC §4.4 and §5.2a, does not carry an earlier A15 to any content (RB-8; RS HA-10 "an earlier A15 never carries over"), and is not acceptance, checking, approval, reliance or a compatibility check (§9).
- **RC-9 Ledger series.** The *registered* lines of a slot alone form its series (SP-1; G-4): sequence 1, 2, … in ledger order, each naming the previous registered revision as its prior, no revision twice. A *re-confirmed* line, and a *not completed* line with disposition *re-confirmation*, add nothing to the series and never change the slot's latest (SP-4, RB-3, G-1). Reader checks on a *re-confirmed* line: `reconfirms.ledger_seq` names an earlier *registered* line of the same slot; `identity`, `reconfirms.identity`, `sequence`, `prior_revision` and `store_path` equal that line's; `reviewed_draft.content` equals the revision; the A15 it cites (`act.record_id`) is cited by no other ledger line (one single-descriptor act, one effect; RB-8). On a *not completed* re-confirmation line, `reconfirms` names an earlier *registered* line of the slot. Several *re-confirmed* lines may cite one registered line. A breach makes the ledger ambiguous at that line, which is named, as for other series breaks.
- **RC-10 Review package.** For DS-8 the review (RB-2) shows ‹k›'s sequence and LS-1 standing as read, the ledger's registration time and act reference labelled "registered earlier; not verified in this session", the slot's latest revision when it is not ‹k› (as SP-7), the draft base, and the sentence "Re-confirming makes revision ‹k› available in this App session. It registers no new revision, and it is not a check that the workflow can run here."

## 5. States (one table per stateful thing this file owns)

### 5.1 Draft (per draft folder)

| From | Event | To | Record left |
|---|---|---|---|
| absent | Files appear (agent, person, or App action) | *draft*, or *not valid* when a refusing HY finding exists | `draft_transition` *written* with attribution (§8) |
| *draft* / *not valid* | Files change | *draft* or *not valid* (re-evaluated) | *changed* |
| *draft* | Review opened; snapshot consistent; disposition registrable | *under review* | `registration_disposition`; `a15_descriptor`; *review shown* |
| *draft* | Review opened; disposition refusing (DS-3…DS-6) | *draft* (or *not valid*) | `registration_disposition`; *registration refused* |
| *under review* | Live content changes, or the slot's latest revision changes (RB-3) | *changed since review* | *review stale*; descriptor withdrawn |
| *changed since review* | Review opened again | *under review* or refused, as above | as above |
| *under review* | Review closed without an act | *draft* | none (no act, nothing inferred) |
| *under review* | A15 captured and registration committed | *registered, unchanged since*; the App records the new revision as the draft's base | *registered* with `a15_record` and `revision` (C-02); `library_entry` *registered* |
| *under review* | A15 captured; registration not completed | *draft* | *registration not completed* with `a15_record` (C-02); `library_entry` *not completed* |
| *under review* (DS-8; CC-WR-RECONFIRM) | A15 captured and re-confirmation committed (G-4R) | *registered, unchanged since*; the App records ‹k› as the draft's base | *re-confirmed* with `a15_record` and `revision` = ‹k›; `library_entry` *re-confirmed* |
| *under review* (DS-8) | A15 captured; re-confirmation not completed (§4.8 RC-7) | The state the review began from: *registered, unchanged since*, or *draft* | *registration not completed* with `a15_record` and disposition *re-confirmation*; `library_entry` *not completed*, disposition *re-confirmation* |
| *under review* (DS-8, begun from *registered, unchanged since*) | Review closed without an act | *registered, unchanged since* | none |
| *under review* (DS-8, begun from *registered, unchanged since*) | RB-3 or RC-5 fails while the live draft is unchanged | *registered, unchanged since* (a changed live draft goes to *changed since review*, as above) | *review stale*; descriptor withdrawn |
| *registered, unchanged since* | Files change | *draft* (a refinement of that revision) | *changed* |
| *registered, unchanged since* | Review opened (CC-WR-RECONFIRM) | *under review* (DS-8), or unchanged on a refusal (DS-3, DS-4) | as for *draft* |
| any | Folder removed | *removed* | *removed*; the App's base pointer is dropped |

### 5.2 Registration attempt (per review)

| From | Event | To | Record left |
|---|---|---|---|
| — | Review shown with a registrable disposition | *offered* | descriptor at the act control |
| *offered* | RB-3 fails | *withdrawn* | *review stale* |
| *offered* | The person closes the control without acting | *withdrawn* | nothing |
| *offered* | The person operates the control (native event) | *captured* | A15 human-act record (RS §6.1) by the act control's writer |
| *captured* | G-1 finds the slot moved on, or G-2/G-3 fail | *not completed* | `library_entry` *not completed* citing the A15 and the reason |
| *captured* | G-2 reservation and G-3 verified copy | *stored* | attempt journal (App-kept) |
| *stored* | G-4 ledger append | *committed* | `library_entry` *registered* |
| *stored* | The App process is lost | *stored* (found at relaunch) | — |
| *stored* (relaunch) | SQ-X: slot unchanged | *committed* | as G-4 |
| *stored* (relaunch) | SQ-X: slot moved on | *not completed* | as above; the store folder is left, standing "not registered" |
| *committed* | G-5 published copy written, or not | *committed* (a failed copy is repaired at the next reconciliation; not a registration failure) | — |

A re-confirmation attempt (§4.8; CC-WR-RECONFIRM) has the same states, with G-1R…G-4R in place of G-1…G-4 and no G-5. At relaunch a *stored* re-confirmation attempt ends *not completed* (RC-7), never *committed*.

### 5.3 Library entry (per revision) and published copy

| From | Event | To |
|---|---|---|
| — | G-4 | *registered* (LS-1 when read) |
| *registered* | At read, the A15 record is missing or the store bytes do not recompute | *registration record incomplete* (LS-4); not runnable |
| *registration record incomplete* | The record or bytes are restored | *registered* |
| *registered* | Nothing removes it in this design (no withdrawal; U-WR-6) | — |
| *registered* | A re-confirmation of this revision commits (G-4R; CC-WR-RECONFIRM) | *registered*, unchanged; a *re-confirmed* line cites it (§4.8 RC-9) |
| Published copy equals the latest revision | Files in it change | *library copy changed outside registration* (LS-3) |
| *library copy changed outside registration* | A new revision is published (G-5) | The changed copy is moved to the kept-aside location; the new latest is published |
| Slot with content and no registration | — | *present without registration record* (LS-2) → DS-7 → *registered* |

### 5.4 Selection (per conversation)

| From | Event | To |
|---|---|---|
| none | The person selects a tuple with revision whose standing is LS-1 and selectable in this process (§4.8 RC-2; CC-WR-RECONFIRM), LS-5 or LS-6 | *selected* (pinned) |
| none | The person tries to select a draft or LS-2/LS-3/LS-4 content | none; refusal with standing and "Review to register" |
| none | The person tries to select an LS-1 revision that is not selectable in this process (§4.8 RC-2; CC-WR-RECONFIRM) | none; "registered — re-confirm to use in this App session", with Review where a draft holds its bytes (DS-8), or Refine (RF-1) to make one |
| *selected* | A newer revision is registered in the slot | *selected*, "newer revision available" shown |
| *selected* | The person selects another tuple | *selected* (a new event that cites the one it replaces) |
| *selected* (its run ended) | The person selects the next workflow, or confirms an agent's proposal (R19-2) | *selected* for the next run, with `prior_run` (SL-7); the run starts by §16 |
| *selected* | Same-name discovery changes | *selected* unchanged; collision notice (C-1) |
| *selected* | Resolution finds the bytes missing or not recomputing | *selected*, "selected revision not resolvable" / "revision not verified"; nothing substituted |

## 6. Operating sequences with failure behaviour

**SQ-J — the journey** (V4-EXM-10; REQ-001). Owners in brackets.

| Step | What happens | Failure · reported by · then |
|---|---|---|
| J-1 Plan | The person and the agent plan in conversation; plan items appear when Codex's experimental plan mode is on (DEL-01-03; K-5), and the journey works without them | Plan view absent (experimental off) · DEL-01-03 · planning continues in prose |
| J-2 Try | The agent does the work with real tools in an ordinary conversation | Ordinary turn failures (interrupted, unknown) · DEL-01-02, DEL-01-04 · the person continues or retries |
| J-3 Draft | The person asks the agent to write the method as a draft (or writes it); the workspace lists it (SQ-D) | Not valid (HY) · the workspace · fix and re-list |
| J-4 Try the draft | Try in a conversation (TT-3) | As J-2; nothing is recorded as a run |
| J-5 Review | SQ-R | DS-3…DS-6 · the workspace · as the message says |
| J-6 Register | The person registers at the act control; SQ-G | Not completed · the workspace · review again |
| J-7 Reuse | Select the revision (SQ-S); run it on new inputs (DEL-02-03) | Not resolvable or not verified · the resolver · choose again |
| J-8 Refine | Refine the revision (a draft with that base), try, review, register: revision 2 | As J-3…J-6 |
| J-9 Refine again | As J-8: revision 3, then reuse | As above |

**SQ-D — create a draft.**

| Step | Action | By | Failure · reported by · record · next |
|---|---|---|---|
| D-1 | Files written under `workflow-drafts/<name>/` | Agent or person; or the App's Refine / Open and refine / Review to register, which copies a revision's regular files | App action into an existing draft name · the workspace · refused "a draft named ‹name› already exists" · rename or remove the draft |
| D-2 | The workspace observes the folder, computes its content identity and hygiene | Workspace | Content identity not obtainable (a link, an unreadable file) · the workspace · *not valid* with the finding · the person fixes it |
| D-3 | Attribution from a supplier `fileChange` item naming the path, where one exists (`observed-in-generated-types`, 0.158.0 `FileChangeThreadItem`); otherwise "not observed" (a shell write or the person's editor) | Workspace | No item · — · attribution "not observed" · nothing inferred |
| D-4 | `draft_transition` handed to DEL-01-04 for the native draft view | Workspace | Receiver not available · — · the draft list still shows it · — |

**SQ-R — review.** RB-1…RB-4.

| Step | Action | Failure · record · next |
|---|---|---|
| R-1 | Hygiene; refusing finding → DS-5 | `registration_disposition` refused · fix |
| R-2 | Snapshot and the two recomputations (RB-1) | Mismatch → DS-6 · review again |
| R-3 | Disposition (SP-4, in SP-4a's order), lineage, same name elsewhere | DS-3 / DS-4 · as the message says. DS-8 · re-confirmation is offered (§4.8; CC-WR-RECONFIRM) |
| R-4 | Review package shown (RB-2); A15 descriptor handed to the act control | The act control is not available (not built) · the review shows "registration control not available"; nothing is registered (EXEC CH-23 analogue) |
| R-5 | Freshness watched (RB-3) | Stale → descriptor withdrawn · review again |

**SQ-G — register** (after the act control reports a capture for this descriptor).

| Step | Action | Failure · record · next |
|---|---|---|
| G-0 | The capture names this descriptor and binds this snapshot's content identity | Otherwise nothing happens: no act, or an act on other content · the draft stays a draft (FX-56 (b), (c)) |
| G-1 | The slot's latest revision is still the prior revision bound (or the slot is still empty) | Moved on → `library_entry` *not completed* "slot moved on", citing the A15 · review again |
| G-2 | Exclusive reservation of the store folder for this revision (create-if-absent) | Exists with identical bytes → continue (idempotent); with other bytes → *not completed* "store conflict" |
| G-3 | Copy the **snapshot** into the store; recompute | Mismatch → remove the reservation; *not completed* "copy verification failed" |
| G-4 | Under an exclusive ledger lock, append `library_entry` *registered* with the sequence | **Commit point.** Lock held by another writer → wait; process lost before G-4 → SQ-X |
| G-5 | Publish the copy at `workflows/<name>/`: write a new copy to staging, move any unrecorded content aside (LS-3), swap by rename | Failure → the published copy is stale; the revision is registered; repaired at the next reconciliation |
| G-6 | Transitions: draft *registered*; DEL-01-04 informed; the draft's base becomes the new revision | — |

The A15 record itself is written by the act control's writer at capture (ACT LC-2 → LC-3), before G-0. A registration that does not complete therefore leaves a true record of the person's act together with a ledger line saying it had no effect, and why.

**Re-confirmation (CC-WR-RECONFIRM).** A capture of a DS-8 descriptor runs G-0, G-1R…G-4R and G-6R (§4.8 RC-6) in place of G-1…G-6.

**SQ-S — select and hand off a run.**

| Step | Action | Failure · next |
|---|---|---|
| S-1 | Listing with standings (§4.6) and collisions (C-1) | Library unreadable · listed as *not established* |
| S-2 | The person selects (SL-1…SL-3); `selection_record` | Draft or no registered standing → refused (SL-5) |
| S-3 | Hand-off to DEL-02-03 (EXEC A-1 CK-1 check; A-2 run start) with the selection record; the resolver reads the store (EXEC §6.1 *resolved*) | Not resolvable or not verified → EXEC's wording; the person may choose again |
| S-4 | (v0.2, R19-7) DEL-02-02 composes the run-start text from the resolved bytes (§16.2); DEL-02-03 starts the run with it as the first text element of the run's first turn; DEL-02-04 composes role guidance only (at conversation start) | Text not composed (bytes not UTF-8, not resolvable) → the run does not start; supply check not *verified* → *supplied* not verified (§16.6) |

**SQ-H — host-origin workflow opened and refined in the App** (EXEC HR-1…HR-7, consumed unchanged; App-side steps only, DECISION-3).

| Step | Action | Identity | Failure |
|---|---|---|---|
| H-1 | Relayed host files are held in the import holding library and listed with origin *host* (HR-1) | Host tuple | Bytes do not recompute to the claimed revision → "revision not verified" (TF-1), not listed as that revision |
| H-2 | Open read-only (HR-2) | Host tuple | — |
| H-3 | Open and refine: a draft in the project (or user) drafts with base = host tuple (HR-3) | None (a draft) | Draft name exists → rename |
| H-4 | Review and register (HR-4): DS-2 when the host tuple's lineage reaches the target slot (the round trip, SP-3), DS-1 when the slot is empty, DS-3 otherwise | New tuple, origin *project* or *user*, derived-from = host tuple | As SQ-R, SQ-G |
| H-5 | Collisions expose every origin with its holding library (HR-7) | — | — |

**SQ-X — reconcile at App start** (after a quit or a loss of the App process; the turns themselves are DEL-01-02's, R17-3).

| Step | Action | Failure |
|---|---|---|
| X-1 | Read each library's attempt journal and store | Library unreadable → its standings *not established* until read |
| X-2 | For an attempt in *stored*: if the slot is unchanged, complete G-4 and G-5 citing the **same** A15 (the act bound this content and this prior revision, and nothing changed); otherwise write *not completed*. A re-confirmation attempt is never completed here: first reread the ledger for a line citing its A15; if one exists write nothing and close the attempt, otherwise write *not completed* "process lost before re-confirmation committed", citing the same A15 (§4.8 RC-7; CC-WR-RECONFIRM) | — |
| X-3 | Re-publish a stale published copy from the store when it equals neither the latest revision nor content kept aside | — |
| X-4 | Review packages are not restored: an *under review* draft returns to *draft* (a DS-8 review begun from *registered, unchanged since* returns there; CC-WR-RECONFIRM), and its descriptor is withdrawn | — |

## 7. Interfaces

Arc layer per DAG-003 (`admitted` / `held` in SCC-002). Direction is consumer → supplier. Where this deliverable is the supplier, the interface is **offered**; R17-10's cycle guard is respected (DEL-01-02 and DEL-01-03 consume nothing from here).

| Other side | Row · arc · layer | What flows | Condition of use | When the exchange fails |
|---|---|---|---|---|
| DEL-01-03 native plans, tools, delegation | DEP-02-02-012 · admitted | Plan items and revisions, tool items, delegation items shown in journey conversations (J-1, J-2) | Plan items, tool items and delegation are stable and shown without any opt-in; only the plan-mode element (choosing Plan) needs Codex's experimental opt-in (K-5 as narrowed by R18-1 C-05; NPTD-v0.2 §4 EX-1, EX-3); plan revision identity is DEL-01-03's | Views absent: the journey works in prose; nothing in the workspace depends on a plan item. Plan acceptance is ordinary input (R17-9) |
| DEL-01-04 native requests, outcomes, attachments, draft view | DEP-02-02-013 (receive) and DEP-01-04-009 (offer) · held, SCC-002 | **Offered:** `draft_reference`, `draft_transition` (with `a15_record` and `revision`, C-02), `registration_disposition` (collision and refusal standing), the review package (RB-2); v0.2: the run-start and end-notice text elements for the turn it composes (R18-1 C-06: DEL-01-04 composes `turn/start`), the agent-proposal offer "Start ‹workflow›" with its candidates (§16.5), and the run start and end marks the conversation view shows (R19-2). **Received:** the native draft view and review presentation (DEL-01-04 OUT-002, OUT-004, REQ-004); attachments into conversations | DEL-01-04 shows a draft as a draft until a *registered* transition arrives (its REQ-004) | Draft view not built: the workspace list is the only view; no transition is invented by the receiver |
| DEL-01-04 App act control (K-8; SC2-01-04-1, PROPOSED until SCA-V4-003) | DEP-02-02-013 (statement to be revised, return file) · held | **Offered:** `a15_descriptor` (RB-4) and its withdrawal (RB-3); CC-WR-RECONFIRM: the DS-8 re-confirmation form of the same descriptor (§4.8 RC-4) and its withdrawal (RC-5). **Received:** the capture {A15 record identity, capture-evidence reference, bound content, descriptor identity} | Capture only from a native event (CAP-4; R17-5); the control refuses capture while the descriptor is stale | Control not built: nothing is registered; the review says so (R-4). Capture refused as stale: review again |
| DEL-02-01 portable contract | DEP-02-02-014 · held | Identity tuple (`$defs/workflow_identity`), RV-1…RV-5, name rule, the declared-part reader (VO-1…VO-10) for the review, collision and rebinding rules (C-1…C-6) | Consumed unchanged | Reader finding: shown, never refusing (HY-6). Algorithm open (U-03): the prototype's illustrative digest stands in |
| DEL-02-03 execution, compatibility, round trip | DEP-02-02-015 (receive) and DEP-02-03-010 (offer) · held | **Offered:** `selection_record` (with `prior_run`, `proposal`); v0.2: the composed run text and its `run_text` record for the run DEL-02-03 opens, the `supply_check` after the turn (§16; R19-7: "DEL-02-02 composes …; DEL-02-03 starts the run"); resolution from the store (the resolver reads the revision store; EXEC §6.1 *resolved*); the drafted / registered link (EXEC §6.1 *opened / drafted / registered*); the HR-1…HR-4 App steps (SQ-H). **Received:** the compatibility report (shown beside a review or a selection, labelled), T-1's refusal wording, run start | EXEC's run start is the only place a workflow runs (TT-1) | Report not established: shown so (EXEC CR-3); nothing is gated by it (CC-3) |
| DEL-02-04 role guidance | none (v0.2: the R17-8 row is **dropped** by R19-7) | Nothing flows for workflows: DEL-02-04 composes product guidance and the conversation's role only. Runtime value only: the conversation's role is fixed for its life (L-2); a run text never changes it | — | — |
| DEL-04-01 operation policy and human acts | DEP-02-02-016 · admitted | A15's act table entry, binding (not lapse-evaluated), capturing surface, non-evidence list, request → capture → record sequence (ACT §2.1, §2.5, §2.6, §4.7), FX-56 | Consumed with the edits K-8 and R17-11 require (join list) | — |
| DEL-04-03 records | DEP-02-02-017 · held | The A15 human-act record (RS §6.1, HA-10) in the persisted form of C-01 (single and multi-entry), the act log outside a run, R2 trace links (*listed*, *selected* with holding library), R16 act requests; v0.2: per-run supplied-workflow evidence (RS R3) from `run_text` and `supply_check`, and the relation "follows ‹run› in this conversation" (R19-2) | The A15 record is written by the act control's writer; the ledger cites it by record identity | Record write fails: ACT LC-2 (late write, "record write failed"); registration waits for G-0 until the capture is reported |
| DEL-09-02 standalone qualification | DEP-09-02-016 / DEP-02-02-018 · admitted | Candidate-bound fixture results and remaining limits (OUT-003), the §12 case inventory | Supplied after a candidate exists | Nothing is claimed before then |
| DEL-09-06 connected activity | DEP-09-06-026 (N-C1) · admitted | Registration for the round trip (CA §4 *opened / drafted / registered*; ST-5; W14-01, W14-09, W14-10) and the workflow-maker party's App steps | Host side waits for SQ-17/SQ-18 and the host joins (DECISION-3) | W14-01/W14-09 stay AWAITING INPUT on the host side |
| DEL-01-02 execution and recovery | Proposed row NR-1 (return file) · would be admitted, no SCC | The stop definitions (R17-3) and the App-start event at which SQ-X runs; interrupted trial conversations are shown by DEL-01-02 / DEL-01-04 | — | Without it, SQ-X runs at App start on its own; no recovery of conversations is claimed here |
| DEL-01-05 account and model access | none (runtime value only) | A trial conversation starts with no model chosen until the person chooses (K-3) | — | — |
| DEL-01-01 supplier boundary | none direct | The `fileChange` item used for draft attribution (D-3), via DEL-01-03/01-04's item delivery. v0.2: the supplier facts §16 rests on at Codex 0.158.0 (OBS-3 W-1…W-6; the generated `TurnStartParams`, `Turn`, `ThreadItem`, `UserInput`); S-6 carries role guidance only (R19-7) | `observed` (OBS-3, dated, one local model) and `observed-in-generated-types` | Attribution "not observed"; for §16, a fact that changes at a later Codex version reopens the cell (R19-5) |

## 8. Data formats (PROPOSED; R17-1)

One schema, [workspace-registration.schema.json](workspace-registration.schema.json) (`$id` `urn:chirality:app-v4:del-02-02:workspace-registration:WR-v0.2`, JSON Schema 2020-12), with ten record kinds (seven at v0.1) told apart by `record_kind`. Names are Chirality's, snake_case as WD's schema. Workflow tuples reference WD's `$defs/workflow_identity` by WD's `$id`; RS spells the same tuple in camelCase (`workflowTuple`), a one-to-one mapping (WD §3.6 spelling table).

| Kind | Receiver(s) | Content | Reader checks beyond the schema |
|---|---|---|---|
| `draft_reference` | DEL-01-04 (DEP-01-04-009); cited by A15 descriptor and ledger | Draft key, state (§5.1), content identity or "not established", file count, App-recorded base, findings | `base` present only when `base_recorded_by` is *app* (schema); content identity recomputes over the folder |
| `draft_transition` | DEL-01-04 | Event (CC-WR-RECONFIRM adds *re-confirmed*), from/to states, content identity, disposition, cause, time, attribution (*file change item* with thread and item · *app action* · *not observed*) | The workspace never emits a *registered* transition without a matching ledger line |
| `registration_disposition` | DEL-01-04; the review | Occasion (*registration review* · *discovery*), target slot, reviewed content, disposition (SP-4), prior revision, base, lineage, stale-base flag, same name elsewhere with holding libraries and standings, findings, message; CC-WR-RECONFIRM: `reconfirms` with DS-8, whose `prior_revision` is, as for every review, the slot's latest revision at review | DS-2 names a prior revision and DS-1 none (schema); DS-8 names `reconfirms` and no other disposition does (schema) |
| `a15_descriptor` | DEL-01-04 act control | RB-4; for DS-8 the re-confirmation form of §4.8 RC-4 (CC-WR-RECONFIRM) | `subject.revision` equals `bound_content.value` (ID-2; prototype P-39); for DS-8, `subject` equals `reconfirms.identity`, and the re-confirm wording, the re-confirm purpose and `reconfirms` go together (schema); its RB-3 (b) compares the slot's latest with `freshness.slot_latest` (RC-5) |
| `library_entry` | DEL-02-03 resolver; DEL-09-02 evidence | Ledger line: outcome (*registered* · *not completed*; CC-WR-RECONFIRM adds *re-confirmed*), tuple, sequence, disposition (adds *re-confirmation*), prior revision, reviewed draft, A15 record and capture-evidence references, store path, reason, evidence limits; `reconfirms` on re-confirmation lines | LS-1 needs the A15 record and recomputing bytes as well; re-confirmation lines add nothing to the series and pass §4.8 RC-9 |
| `selection_record` | DEL-02-03 (CK-1, A-1), DEL-04-03 (R2 *selected*) | Tuple with revision, holding library, standing, "the person (App interface)", how (*explicit* · *from unqualified name* with candidates), replaces, conversation, time | The tuple's standing is runnable (TT-1) |
| `trial_pointer` | App-kept only | Draft key, content identity, conversation, time, the fixed standing sentence | Carries no workflow identity (schema: `additionalProperties` false) |
| `a15_multi_descriptor` (v0.2) | DEL-01-04 act control | §4.7: library, entries (subject tuple, bound content, `entry:` ID-3 string), scope, purpose, review | Each entry's subject revision equals its bound content |
| `run_text` (v0.2) | DEL-02-03 (run start); DEL-01-04 (turn composition); DEL-04-03 (RS R3) | §16.2: purpose (*run start* · *run end notice*), framing `WR-FRAME-1`, run, conversation, workflow tuple and holding library, `WORKFLOW.md` identity and size, other files, chain, origin of start, selection, the framing lines (each fixed by a pattern), text identity and size | The text recomputes from the lines and the revision's bytes (TX-6; prototype P-48); the proposal line's finished line names the run's own origin and name (RX; prototype P-62) |
| `supply_check` (v0.2) | DEL-04-03 (RS R3); DEL-02-03 | §16.6: expected text and workflow identities, state, observed text identity, turn, item, how located, time, evidence limits | Never relabelled; a later read is a new check |

Conformance instances (v0.2): fourteen valid instances covering all ten kinds and seventeen invalid instances (INV-16 and INV-17 added at RX: a proposal line in the form without origins; a confirmed proposal whose `proposed_name` names no origin). v0.2 adds: a *registered* transition with `a15_record` and `revision`; a two-entry multi descriptor; a chained run start; an end notice; a verified supply check; a selection confirming an agent proposal; and the invalid INV-10…INV-15 (a revision on a *written* event; a multi descriptor with one entry; a chain without a chain line; a start line outside WR-FRAME-1; *verified* without the observed identity; a confirmed proposal without the proposal). At v0.1: eight valid instances covering seven kinds and nine invalid instances, one named error each (`.invalid.examples.json`): a valid-state draft with a bad name; a base not recorded by the App; an invented *auto-registered* event; a new revision without its prior revision; another act kind presented as registration; a registration line citing no A15; a selection of a slot without revision; origin `host-supplied`; a trial pointer naming a workflow identity.

**The A15 record (RS's format, consumed).** The act control's writer produces an RS `human_act` with act kind A15 in RS-v0.9's form (R18-1 C-01; RB-4a; prototype P-11, P-38, P-47): bound subject the revision (one per entry), bound content its identity, purpose per library, and the relations **reviewed draft** (`relations.reviewedDraft` {`draft`: the ID-3 string, `draft:` or `entry:`; `content`}) and **prior revision** (`relations.priorRevision`, RS `workflowTuple` or null), or `relations.registeredEntries` for a multi-entry act. RS-v0.8's single `derivedFrom` string is refused (P-36). WD's derived-from stays in the subject tuple (C-21).

**The A15 record of a re-confirmation (CC-WR-RECONFIRM; RS's format, no RS schema change).** The act control's writer produces the same RS `human_act` A15: bound subject ‹k›, bound content ‹k›'s content identity, `relations.reviewedDraft` {this draft's ID-3 string, content} and `relations.priorRevision` = ‹k›'s own prior revision as its registered line records it ("the revision this one follows in its slot", RS), with the re-confirm purpose of §4.8 RC-4. The *re-confirmed* ledger line cites the record (`act.record_id`) and names ‹k›'s registered line (`reconfirms`). RS's text adoption (HA-10's purposes) is named in the change record. CC-WR-RECONFIRM adds no instance to the two conformance files; its schema cases are WR-VC-20's.

## 9. What is never registration, and what is never review

| Situation | Outcome | Source |
|---|---|---|
| The agent says "registered" or "ready", or writes into `workflows/` or the ledger | No A15; files without a matching record are LS-2/LS-4 | ACT §2.6; FX-56 (b); prototype P-08, P-35 |
| An answer to a supplier user-input or elicitation request, or a chat statement | Not A15 | CAP-6, CAP-7 |
| The review was shown | A presentation, not an act (RB-7) | ACT §2.1 |
| A successful trial conversation | Not A15 and not a run (TT-4) | ACT §2.6; K-7 |
| An earlier revision's A15 | Never carried to new content (RB-8) | FX-56 (c); prototype P-15 |
| A draft changed after review | The control refuses capture; review again | K-8; prototype P-09 |
| Registration of a revision | Not acceptance, checking, approval or reliance, and not execution compatibility | REQ-005, REQ-006; ACT §2.1 alias exclusions |
| A re-confirmation (§4.8; CC-WR-RECONFIRM) | Makes revision ‹k› selectable in this App process only; registers no new revision; makes no earlier act, capture or receipt trusted; not cold replay (CI-10 and I3-CUST stay open) | RC-2, RC-3, RC-8; owner decision 2026-10-07 |

## 10. Reuse account (OUT-004; REQ-007; AC-007)

Prior code is optional reuse, assessed against the receiving contracts above (ARCHITECTURE §3; clarification C1). App v3 is a historical exemplar (evidence of what was built, never a v4 commitment); its Next.js route is not a v4 target (V4-ARC-03; the Tauri/Rust shell).

| App v3 behaviour (`workflow-draft-store.ts`, `route.ts`, `workflow-draft-review.tsx`) | Disposition | Gap against this design |
|---|---|---|
| Drafts listed from project and user `.chirality/workflow-drafts/`, with bounds | **Keep the behaviour** (§3) | Bounds become HY-5 |
| Review token = sha256 over root, source, name and captured bytes; re-captured and compared at register (`DRAFT_CHANGED`) | **Adapt**: the binding becomes the WD content identity (ID-2) carried in the A15 descriptor and checked by RB-3 and G-0 | The token was presented to an HTTP caller; any local caller holding it could register (inference from reading the code) |
| Staging, then exclusive `mkdir` reservation; `WORKFLOW_EXISTS` → "Choose a new name" | **Keep** the reservation (G-2); **replace** the refusal of every existing name by K-6's revision series, keeping "Choose a new name" for DS-3 | v3 had no revisions |
| Hard-linked publish with `WORKFLOW.md` last; never overwrite bytes | **Replace** with an immutable store plus a published copy swapped by rename (G-3, G-5); keep "never overwrite" | v3 published one copy per name |
| "Ready for review" · "Request changes in chat" · "Register workflow" (disabled when stale or the name exists) | **Keep the wording** for the first two; "Register workflow" becomes the act control's A15 offer (K-8) | — |
| Registration by local HTTP POST; no act record, no actor | **Not reused** | Not a CAP-4 control; no A15 record; no ledger |

Root's current practice (`create-workflow`; Root `AGENTS.md`) agrees on drafts in `.chirality/workflow-drafts/`, review of the exact bytes, no overwrite and no auto-run; it differs in offering an "explicit authorized replacement with the prior copy kept outside discovery". K-6's revision series covers the same need without replacement.

## 11. Process placement (R17-5; OI-008 ruled by the owner for the draft workspace; otherwise PROPOSED)

Requirements, stated apart from placement: (a) no agent tool, MCP operation, App rule or supplier request can produce an A15 capture or a ledger line *registered* (CAP-4); (b) no registration is reachable through a local network endpoint; (c) publication reads only the snapshot (RB-6); (d) the ledger is appended under an exclusive lock (G-4).

**Owner ruling for the draft workspace (OI-008; SETTLED).** For the workflow draft workspace, the owner decided: "A, proceed with the Rust host." The ruling covers the draft workspace only. Draft observation (SQ-D D-2…D-4), draft content identity, hygiene (§4.5), the §5.1 draft states and the trial pointer (TT-4) run in the Rust host. The TypeScript interface only lists and presents the drafts, states, findings, attribution and trial pointers the host reports. It names a draft back to the host only by its listed name. The ruling does not decide any other process-division question.

Placement under R17-5's O-1 (PROPOSED except where the ruling above settles it): the Rust host owns the library writer (store, ledger, published copy, kept-aside content), content-identity computation, hygiene, the freshness watch and SQ-X; DEL-01-04's act control capture is produced in the host from a native interface event; the Rust host composes the draft list, and the TypeScript interface presents it, the review package and the selection. Because D3 leaves the sandbox to the user, an agent with full file access could still write a forged ledger line and act record together; the App reports standing from what it can check (LS-1, LS-4) and claims no prevention.

## 12. Verification (designed; the library side runs on the prototype only)

| Case | VER (AC) | What it exercises | Needs | State |
|---|---|---|---|---|
| WR-VC-01 Journey from an empty folder | VER-001 (AC-001) | J-1…J-9 with real tools, two refinements, reuse on new inputs; native transitions and identities recorded | A candidate App with Codex 0.158.0 or the qualified pin; the person; DEL-01-04's act control and draft view; DEL-02-03 run start; DEL-02-04 supply | DESIGNED. Library steps ran on the prototype (P-07…P-16) |
| WR-VC-02 New and changed definitions | VER-002 (AC-002) | Review absent; registration absent; both; a changed definition needing its own A15; no carried act | Library double and act-control double (prototype); for the positive case on a candidate, the person | Library side **ran** (P-08, P-09, P-10, P-13, P-15, P-16) |
| WR-VC-03 Collisions and four origins | VER-003 (AC-003, AC-004) | DS-3, DS-4; same-name additions after selection; discovery across project, user, bundled, host; unqualified names; no overwrite and no rebinding checked separately | Library, bundle and host-listing doubles; host listing on a real host waits (DECISION-3) | **Ran** on doubles (P-17, P-18, P-22…P-27, P-33, P-34) |
| WR-VC-04 Receiving conditions | VER-004 (AC-005) | Missing capability, a declared checkpoint, unknown outcome shown truthfully beside a selection; registration never offered as compatibility | EXEC's checker and recorder doubles; WD reader | DESIGNED (the review shows the WD reading; the report comes from DEL-02-03) |
| WR-VC-05 Faithful act and negatives | VER-005 (AC-006) | Positive A15 with actor and recorder separate; negatives: no act, an act on other content, a stale review, a trial, an agent's claim, a forged ledger line | Act-control double; on a candidate, the person at DEL-01-04's control | Negatives and the record shape **ran** (P-08, P-09, P-11, P-15, P-35, P-38); the positive case on a candidate is AWAITING INPUT (DEL-01-04 not built) |
| WR-VC-06 Receiving and reuse account | VER-006 (AC-007, AC-008) | §7 and §10 against the row, sources and owners | Inspection | DESIGNED |
| WR-VC-07 Interruption | REQ-001 (OBJ-001 "recoverable") | Slot moved on between capture and publication; process loss after the store copy; reconciliation with the same act | Library double with fault injection | **Ran** (P-20, P-21) |
| WR-VC-08 Hygiene | REQ-003, REQ-004 | HY-1…HY-7: refusals, and HY-6 not refusing | Library double | HY-2, HY-3, HY-4 and the refused review **ran** (P-02…P-04); HY-6 runs in every review (the declared-part note); HY-1, HY-5, HY-7 DESIGNED on the prototype. App draft listing: HY-1…HY-5 and HY-7 **ran** in `app/src-tauri/src/workflow_drafts_tests.rs` |
| WR-VC-09 Drafts never run | K-7 | Draft selection refused; a trial leaves only a pointer; changed library copy not selectable | Library double | **Ran** (P-05, P-06, P-29). App: trial pre-fill sends nothing, only a send leaves a pointer, the pointer survives a new process, and a conversation with a run in force is refused (`runtime_session.rs` draft workspace tests) |
| WR-VC-10 Round trip, App side | REQ-004 (CA W14-09, EXEC RT-6) | A host tuple whose lineage reaches LIB-A1 registers as LIB-A1's next revision with derived-from = host tuple; one whose lineage does not is refused | Host-listing double | **Ran** (P-32, P-33); host side AWAITING INPUT (SQ-17, SQ-18) |
| WR-VC-11 Formats | R17-1 | Every record produced conforms; static instances; reader checks | Schema, validators | **Ran** (S-1, S-2, INV-1…INV-17, P-37…P-39; P-63 recomputes the run_text example's identities, RX2) |
| WR-VC-12 Persisted A15 form and transitions (v0.2) | VER-005 (AC-006) | C-01: single and multi-entry A15 against RS's schema projected with FR-06; the old `derivedFrom` form and a free-string prior revision refused; C-02 elements | RS writer double; F-C's RS v0.9 for the real schema | **Ran** on the projection (P-11, P-36, P-38, P-40, P-41, P-47); against RS v0.9 when F-C lands |
| WR-VC-13 Shipped and multi-entry (v0.2) | VER-002, VER-003 (L-4) | LS-8 recognition (current and earlier release), edited copy not recognized; one act over three entries with a stale entry before and after capture | Library and act-control doubles; on a candidate, the person | **Ran** on doubles (P-42…P-47) |
| WR-VC-14 Run text and supply check (v0.2) | VER-001, VER-004 (AC-001, AC-005) | Composition exact and deterministic; no other workflow named; turn/start and turn shapes against the 0.158.0 types; verified, and each mismatch state | Constructed turns, read back as `thread/items/list` pages (R21-4); on a candidate, Codex 0.158.0 or the qualified pin and a model | **Ran** on constructed frames (P-48…P-52, P-50a); live check AWAITING a candidate (OBS-3 W-4 observed the text route at 0.158.0 with one local model) |
| WR-VC-15 Chaining (v0.2) | VER-001 (AC-001; R19-2) | One run at a time; (a) A→B with the chain line; end notice once; (b) proposal → offer → confirmation → chained start; proposals not on the last line, naming no origin, of drafts or unknown names give no Start; the finished line names origin and name (RX, R20-9); during a run only "End ‹A› and start ‹B›", recorded *ended to start ‹B›*; line placement and at-most-once (RX2, R20-11) | RunDesk double (stands in for DEL-02-03's run start and end) | **Ran** (P-53…P-65; P-60, P-61 for R20-1 and R20-3; P-62 for R20-9; P-64, P-65 for R20-11) |
| WR-VC-16 Re-confirm after relaunch, then run (CC-WR-RECONFIRM) | VER-001, VER-002 (AC-001, AC-002) | Register ‹k› in process 1; relaunch; the registered draft, unchanged, reviews as DS-8, and so does a draft made by Refine without a selection (RF-1); A15 at the act control; G-4R *re-confirmed* line citing the new A15 and ‹k›'s registered line; ‹k› selectable in process 2 only; the selection record and the run text name ‹k› (TX-1); after another relaunch ‹k› needs a new re-confirmation | Library and act-control doubles with a modelled native event; on a candidate, the person at DEL-01-04's control | DESIGNED |
| WR-VC-17 Revision selectable in this process: DS-4 (CC-WR-RECONFIRM) | VER-003 (AC-003) | After a registration or a re-confirmation of ‹k› in the same process, a draft with ‹k›'s bytes reviews as DS-4 "select it instead", with no descriptor; a DS-8 descriptor offered before ‹k› became selectable is withdrawn (RC-5 (d)); a capture after that is *not completed* "already selectable" (G-1R); a draft with the bytes of an LS-4 revision (act record missing, or store not recomputing) reviews as DS-4 with that exact cause, never DS-8, and Refine gives no draft from a store that does not recompute | Library and act-control doubles | DESIGNED |
| WR-VC-18 Changed bytes take the ordinary route (CC-WR-RECONFIRM) | VER-002 (AC-002) | After a relaunch a draft differing from ‹k› by one byte reviews as DS-2 (base reaching the slot) or DS-3, never DS-8; a draft with ‹k›'s bytes whose SP-3 fails reviews as DS-3, not DS-8 (SP-4a) | Library double | DESIGNED |
| WR-VC-19 Dismissal, staleness and loss have no effect (CC-WR-RECONFIRM) | VER-005 (AC-006) | Control closed: nothing captured, ledger unchanged, ‹k› not selectable. Bytes changed between review and act: AX-06, nothing captured. Slot moved on or registered line changed after capture: *not completed* citing the A15. A DS-8 descriptor stays current while the slot's latest equals `freshness.slot_latest`, when ‹k›'s own prior differs from it (RC-5). Process lost before the attempt is *stored*: WR writes nothing at relaunch (AAC §4.4 governs). Process lost after *stored* and before G-4R: *not completed* at relaunch, never completed and never selectable. Process lost after a durable G-4R but before the journal says *committed*: X-2 finds the *re-confirmed* line, writes nothing, and the ledger stays unambiguous. An abandoned DS-8 review begun from *registered, unchanged since* returns there. A not-completed re-confirmation is not completed later by the same act | Library double with fault injection; act-control double | DESIGNED |
| WR-VC-20 Ledger series with re-confirmation lines (CC-WR-RECONFIRM) | R17-1; VER-003 | Registered lines 1 and 2 with *re-confirmed* lines citing 1 (twice) and 2: series and latest unchanged, and 2 is still the prior for the next DS-2. Refused, naming the line: a *re-confirmed* line citing a later line, another slot's line or a *not completed* line; a differing identity, sequence, prior revision or store path; an A15 cited by another line. Refused by the schema: a re-confirmation line without `reconfirms`; a *registered* line with disposition *re-confirmation*; `reconfirms` on a registration; a re-confirmation of an entry reviewed in place; the re-confirm wording with a registration purpose | Schema; ledger reader | Schema cases checked during the change (change record); reader checks DESIGNED |

## 13. Prototype

[`prototype/wrproto.py`](prototype/wrproto.py) (R12-3; not product code) models §3–§6 over invented packages in a temporary folder, with a double for DEL-01-04's act control whose only capture path is a modelled native event. It imports two sibling prototypes read-only: DEL-02-01's `wdproto.py` (revision file set and the illustrative digest `proto-sha256-list-0`, the declared-part reader, the name rule) and DEL-04-03's `minischema.py` (a JSON Schema subset validator whose registry resolves WD's and RS's `$id`). Workflow tuples are also checked with WD's own validator, because `minischema` does not check `maxLength`.

**Run (v0.2):** `PYTHONDONTWRITEBYTECODE=1 python3 wrproto.py`, in `Design/prototype/`, on 2026-10-02 (19:00 UTC), Python 3.13.7: **92 checks, 92 passed, 0 failed**, exit status 0. It also loads Codex 0.158.0's generated v2 JSON Schema bundle (read only) to check constructed `turn/start` params and `thread/read` turns, and builds in memory RS's schema projected with FR-06 (C-01), because F-C edits RS in parallel; the on-disk RS outcome is printed as information. v0.1's run (2026-10-01, 58 of 58) is recorded in D/D5.md. The full output, with the sha256 of every input it read, is in the return file `D/D5.md`. It writes nothing outside its temporary folder and leaves no `__pycache__` (checked with `find` afterwards). **Rerun at RX** (in place, 2026-10-02, same command, Python 3.13.7): **95 checks, 95 passed, 0 failed**, exit status 0 (new: INV-16, INV-17, P-62; P-56, P-58 and P-60 now use the R20-9 line forms); output in `F/RX.md` of this run. **Rerun at RX2** (in place, 2026-10-02, same command): **98 checks, 98 passed, 0 failed**, exit status 0 (new: P-63 recomputes the valid run_text and end-notice examples' identities from `prototype/fixtures/review-pack/`; P-64 and P-65 for R20-11); output in `F/RX.md` (RX2). **Rerun at RV21** (in place, 2026-10-02, same command): **99 checks, 99 passed, 0 failed**, exit status 0 (new: P-50a, the supply check reads `thread/items/list` pages, R21-4; P-51 and P-52 read pages, P-52's "items not loaded" case becomes "a later page failed"); output in `F/RV21-A.md` of this run.

What it does not show: any Codex behaviour, any native view, the real act control, a real person, a candidate, or a host.

## 14. Joins (summary; the full list with old → new text is in the return file)

- **WD:** OS-1/OS-2 now point here and to DEL-01-04's control; §6.1's OS-file question is answered by HY-4; C-4 and C-5/U-10 get the App-side answers SL-2 and SL-3; §7's drafts row and §8's DEL-02-02 row point here; §13.1's "library and selection doubles (DEL-02-02, later)" exist in the prototype.
- **WD-EX:** E3's last column ("if registered as a new App workflow") becomes a new revision of LIB-A1 (K-6, SP-3); E4 step 3 gets the App-side pin (SL-2).
- **EXEC:** HR-4's "new tuple" reads per SP-4 (DS-2 for the round trip); RT-6/RT-7 cite K-6 and this file; U-E19's "AP U-08" half is stale (R12-5) and its slot half is answered; §9.1/§9.2/§10 DEL-02-02 rows point here; CAP-2's wording list gains A15.
- **ACT:** A15's capturing surface becomes DEL-01-04's act control (K-8) in §2.1, §2.6, §4.7 RC-3 and FX-56; content names per R17-11; purpose per library; §10.3's "Not mapped in detail (U-08)" row is filled.
- **RS:** §6.1 relations and HA-10 per R17-11, with `RS_RECORD.schema.json`'s A15 rule and the act-log example; capturing surface; purpose per library; §10 rows; U-05 for act records outside a run.
- **CA:** §3.1, §4, ST-5, W14-01/W14-09, F-1 and its UNRESOLVED row: registration is designed (PROPOSED), not built.
- **DEL-01-04 (node D3, in parallel):** v0.1's vocabulary reconciliation is done (C-22: D3 adopted WR's names). v0.2 asks D3 for: the multi-entry A15 offer (§4.7), the "Start ‹workflow›" offer for agent proposals (§16.5), run start and end marks in the conversation view, and placing the run text as the first text element of the `turn/start` it composes (C-06).
- **v0.2 (R19-7):** EXEC A-3, §6.1 *supplied*; WD §3.9 OS-7 and §6.2 *supplied*; HOSTING S-6, §8.2 and §11; RS R3 and R1 (a "follows ‹run›" relation); RS §6.1 for C-01's multi-entry list. Rows in the return file, Round 2.

## 15. UNRESOLVED

| ID | Item | Owner | Point of need | Effect here |
|---|---|---|---|---|
| U-WR-1 | Revision identity algorithm and method designation | DEL-02-01 with DEL-04-03 (WD U-03; HOSTING U-08) | Before implementation of the store and the A15 binding | The design needs *a* content identity with a method; the prototype uses WD's illustrative digest |
| U-WR-2 | Process placement of the library writer and of A15 capture | App implementation owner (OI-008) | Before architecture production contracts | Requirements §11 hold for any placement. **Draft workspace ruled:** The owner decided: "A, proceed with the Rust host." For the draft workspace only, draft observation, content identity, hygiene and the trial pointer run in the Rust host, and the TypeScript interface only lists and presents (§11). For anything else, R17-5's placement is still PROPOSED here |
| U-WR-3 | Location of act records outside a run, per library | DEL-04-03 (RS U-05) | Before writer implementation | The prototype keeps a per-library act log |
| U-WR-4 | *Closed (DECISION-L L-4 A as clarified, 2026-10-02).* Library content without a registration record | The owner (decided) | — | Shipped workflows registered by the release (LS-5); byte-equal copies recognized (LS-8); the rest registered in place, several per act (§4.7) |
| U-WR-5 | Host listing, relay and host position in unqualified names | Host owner and DEL-02-01 (WD U-10); DECISION-3 | Before host-origin discovery in the App | SL-3 places host last, PROPOSED; host steps AWAITING INPUT |
| U-WR-6 | Withdrawing or retiring a revision or a workflow | Not obligated by the ScopeOfWork | If the owner asks | Nothing is ever removed by the App |
| U-WR-7 | *Resolved (integrator, 2026-10-10, draft workspace implementation).* Hygiene values (OS-file list, 16 MiB, 1 000 files, UTF-8) | Integrator (decided) | — | The §4.5 values stand. HY-4 uses the exact names listed there plus any name beginning `._`. HY-5 allows at most 1 000 regular files and 16 MiB of regular-file bytes per package. It is checked from metadata before any byte is read, and the package read enforces it again with a running byte budget. HY-7 requires `WORKFLOW.md` to be UTF-8. The same values apply when drafts are listed (D-2) and at review (R-1) |
| U-WR-8 | Shared types for identity, collision report and selection | App/shared contract owners (OI-014; WD §9 A-2, A-5) | Before structural allocation | The schema references WD's identity by `$id`; no placement proposed |
| U-WR-9 | A checkpoint that requires A15 | DEL-04-01 (ACT §4.1) | Later | Not designed |
| U-WR-10 | Keep the published copy at `workflows/<name>/` (portability) or drop it (store only) | Integrator | Before implementation | Kept, PROPOSED; LS-3 exists only because of it |
| U-WR-11 | *Resolved (integrator, 2026-10-10).* Vocabulary of draft transitions and the A15 offer shared with DEL-01-04 | DEL-01-04 with DEL-02-02 (decided) | — | One vocabulary, WR's own: the host emits `draft_reference` and `draft_transition` with §5.1 and §8 names and values, validated against this file's schema. NIR §7 already restates those names (C-22) and supplies the display words the interface shows. Draft listing emits *written*, *changed*, *removed*, *review shown* and *review stale*. *Registered* and *re-confirmed* stay with the registration flow, which carries the A15 record (C-02). The A15 offer vocabulary is unchanged (RB-4, §4.8) |
| U-WR-12 | *Resolved (integrator, 2026-10-10).* Draft bases are App-kept, so a draft moved to another machine loses its origin and K-6 refuses its same-name registration | Integrator (decided) | — | Bases stay App-kept in the App data folder (`runtime/wr/draft-bases/`), and no base is ever read from a draft's own files. A draft without one is listed "no App-recorded base". Its same-name registration is refused (DS-3), and the route is Refine (RF-1), which records a base |
| U-WR-13 | Selection pinned rather than following (C-4) | Integrator; owner if a following default is wanted | Before implementation | PROPOSED pin, always visible |
| U-WR-14 (v0.2) | Whether Codex returns a text element byte for byte for every text the App may send (CR LF line endings, a trailing newline, NUL or other control characters, very long texts). OBS-3 W-4 observed it through `thread/read` for one LF, UTF-8 text at 0.158.0; that `thread/items/list` (R21-4) returns the same `ThreadItem` is `observed-in-generated-types` (`ThreadItemEntry.item`), not itself observed | A later observation (not OBS-2/OBS-3's scope) | Before qualification | Until then a mismatch reads "supply not verified", never "supplied" (SC-4) |
| U-WR-15 (v0.2) | Whether `turn/start`'s `clientUserMessageId` is echoed as the `userMessage` item's `clientId` (same concept by name in the generated types; inference, not observed) | A later observation | Before implementation | SC-3 falls back to "first user message of the turn" |
| U-WR-16 (v0.2) | Context cost of a large workflow carried in a turn, and repeated in history at every later turn of the conversation (OBS-3 W-2: nothing is removed from history) | Integrator with DEL-01-05 (model context) | Before implementation | HY-5's 16 MiB bound is far above any context window; a separate run-text bound may be needed |
| U-WR-17 (v0.2) | *Closed (R20-1).* How a run *completes* | Integrator (decided) | — | Only the person or the run owner ends a run; *completed* is the cause when the person ends it on the agent's finished report (FN-1…FN-3) |
| U-WR-18 (v0.2) | Contents of the shipped-revision manifest: every v4 release's shipped revisions; whether App v3's shipped workflows are included | Integrator; owner if v3 copies should be recognized | Before the first release | LS-8 recognizes what the manifest lists |
| U-WR-19 (v0.2) | Earlier run texts stay in history; dropping the earlier workflow rests on the chain line and recency. OBS-3 W-2 saw a 9B local model follow B and drop A (2/2 replies); other models not observed | Later observation; DEL-09-02 for qualification | Before qualification | The chain line states it explicitly; nothing more is claimed |
| U-WR-20 (v0.2) | *Closed (R20-5, R20-9; RX).* The agent-proposal convention was told to the model only in run texts | DEL-02-04 (product guidance) | — | The shipped product guidance states both lines, `Next workflow: ‹origin›:‹name›` and `Workflow finished: ‹origin›:‹name›` (ROLE-v0.2 §4.2 GS-7); the run text repeats them for the run in force (§16.2 line 3) |
| U-WR-21 (CC-WR-RECONFIRM; revision 2) | Re-confirmation from the listing without a draft (option (b)) | Integrator (WR owner with DEL-01-04) | Deferred | Not designed. Option (a) is adopted by HELP_HUMAN's ruling (2026-10-07) as RF-1: Refine of an LS-1 revision from the revision store needs no selection, which gives a draft for DS-8, also for revisions registered in place |
| U-WR-22 (CC-WR-RECONFIRM) | Whether RS marks a re-confirmation A15 with a structured relation, beside its purpose | DEL-04-03 | RS adoption of CC-WR-RECONFIRM | The WR ledger line is the structured link (`reconfirms`, `act.record_id`); the A15 record carries the re-confirm purpose |
| U-WR-23 (CC-WR-RECONFIRM) | *Closed (revision 2; HELP_HUMAN ruling, 2026-10-07).* A draft with ‹k›'s bytes but no App-kept base reaching the slot | — | — | K-6 unchanged: DS-3 (SP-4a). The route is Refine (RF-1), which gives the draft an App-recorded base |
| U-WR-24 (draft workspace, 2026-10-10) | TT-3 as confirmed (R18-1 C-14, R21-5) says Try opens a new conversation, not started until the person chooses a model, with the composer pre-filled, and AT-8 names other files under AT-10. The App pre-fills the attachment list for a conversation the person starts or chooses, and lists non-text files "not attached" (§4.2 TT-3) | Owner: accept the departure, or have DEL-01-04 supply a not-started conversation and the AT-10 carrier | Before the save-a-workflow journey is witnessed (WR-VC-01) | Until decided, the departure stays visible here and in the App's Try wording; a trial remains ordinary input, not a run or registration |

---

## 16. Run text, supply check and chaining (v0.2; R19-1, R19-2, R19-7; DECISION-L L-2)

Supplier facts in this section are at **Codex 0.158.0** (R19-5): OBS-3 (`OBS_3_0.158.0.md`, dated 2026-10-02, one local model `qwen/qwen3.5-9b`, labelled `observed`) and the generated types (`observed-in-generated-types`). A later Codex version reopens each such cell; where Codex reports a capability at run time the App reads it.

### 16.1 Ownership and route (R19-7; INTEGRATION)

| Part | Owner | Note |
|---|---|---|
| Role guidance (product guidance + the conversation's role), in `developerInstructions` at conversation start, for the conversation's life | DEL-02-04 | R19-1; L-2. Never a workflow |
| The run text: composition, framing, identity | **DEL-02-02** (this section) | It holds the registered revision (§3) |
| Opening and ending the run; the run record | DEL-02-03 (EXEC); ending by the person is DEL-01-02's definition (R17-3) | DEL-02-03 asks DEL-02-02 for the text after it opens the run, so the run identity is in the text |
| Composing `turn/start` and sending it | DEL-01-04 (R18-1 C-06) | The run text is the first text element of the input; the person's own text, if any, follows as a separate element |
| Supply check (§16.6); the RS R3 evidence | DEL-02-02 writes `supply_check`; DEL-04-03 records it | — |

**Route chosen: a text element** (OBS-3 W-4: the model received exactly the text and followed it; `thread/read` returned the full bytes in the `userMessage` text; `observed` at 0.158.0). **Recorded alternative, not used:** the stable `skill` input, which Codex honoured only for a `SKILL.md` in a discovered skill root at the exact canonical path and otherwise accepted and silently ignored (W-1); a discovered root also advertises every skill in it to the model on every turn (W-1 side effect), which R19-7 excludes. `mention` supplies nothing (W-3). The experimental `thread/settings/update` persists for the conversation, piles up and replaces plan mode's text (W-5): not used for workflows. `TurnStartParams.additionalContext` exists in the generated types and was not examined (not observed).

### 16.2 Composition (framing WR-FRAME-1; PROPOSED, fixed by the schema's patterns)

The run-start text is, in this order, each line ended by a line feed:

1. **Chain line**, only when the conversation has an earlier run (TX-5): `[Chirality] Previous workflow run ended: ‹name› revision ‹rev12› (run ‹run id›, ‹ended by the person | completed | ended to start ‹B››). Its instructions no longer apply.` (RX2: R20-11 (4) adds the third cause)
2. **Start line:** `[Chirality] Workflow run start: ‹name› from the ‹origin› library "‹source root›", revision ‹rev12›, run ‹run id›. Follow the workflow between the two markers below for this run, until the person ends the run.`
3. **Proposal line:** `[Chirality] When you judge this workflow finished, end the message with a line of its own "Workflow finished: ‹origin›:‹name›". To propose that another registered workflow runs next, end the message with a line of its own "Next workflow: <origin>:<name>", where <origin> is project, user, bundled or host; when you write both, the finished line comes just before it. The person decides; nothing ends or starts until they confirm.` (v0.2 with R20-1; RX with R20-9; RX2 with R20-11 (2): the line now tells the model the placement the App reads). ‹origin› and ‹name› are the run's own, from its tuple (a shipped revision held in a library reads `bundled`, LS-8); `<origin>:<name>` is written as shown. The line repeats, for the run in force, the two agent lines the shipped product guidance states (ROLE-v0.2 §4.2 GS-7; R20-9).
4. **Files line**, only when the revision has files besides `WORKFLOW.md`: `[Chirality] Other files of this revision, in the folder "‹folder›": ‹path› (sha256 ‹12 hex›); …` — paths relative to the package, ordered by their UTF-8 bytes; ‹folder› is project-relative for a project library and `~`-relative for the user library, so no user name is written (OBS-3 noted absolute paths reaching the model).
5. **Begin marker:** `<<<chirality-workflow ‹name›@‹rev12› begin>>>`
6. **The body:** `WORKFLOW.md`'s bytes **exactly** (UTF-8, HY-7), with nothing added or removed.
7. A line feed, then the **end marker** `<<<chirality-workflow ‹name›@‹rev12› end>>>`, with nothing after it.

‹rev12› is the first twelve characters of the revision value; ‹run id› is DEL-02-03's run identity.

- **TX-1** Only a selected revision with standing LS-1, LS-5, LS-6 or LS-8 is composed. A draft is never composed (K-7; TT-3).
- **TX-2** A `"` in a source root is written as `'` in the start line; nothing else is escaped.
- **TX-3 Extraction.** The body is the text between the begin-marker line (and its line feed) and the **last** occurrence of a line feed followed by the end marker. Because the marker carries the revision, a workflow would have to contain its own revision value to collide with it.
- **TX-4 Identity (CC-WR-TEXT-METHOD-ADOPTION, 2026-10-05).** New App writers designate the whole run-start/end text element's exact UTF-8 bytes and `workflow_file.content`'s exact stored `WORKFLOW.md` bytes with `chirality.app.exact-bytes.sha256/v1`: lowercase 64-hex SHA-256, no normalization or excluded bytes. Framing belongs to composed text; source bytes, composed text and whole-package revision remain separate scopes. This adopts CC-CONTENT-IDENTITY and EXEC TR-4's selected text method, not a new algorithm. Historical `sha256 over UTF-8 text` and other incoming method/value objects remain unchanged opaque inputs. Only the same method and subject/scope permit comparison; equal digest characters under different methods do not verify supply, body equality, registration or A15. The schema accepts a nonempty opaque method and the existing lowercase-hex value shape; schema validity establishes neither source authority nor actual supply.
- **TX-5 End notice (the run-end line of R20-3).** When a run ends and no run starts with the next turn, the App prefixes the person's next turn with one App-written line, sent as the turn's first text element before the person's own text: `[Chirality] Workflow run ended: ‹name› revision ‹rev12› (run ‹run id›, ‹how›). No workflow is in force.` once. If the next turn starts a run instead, its chain line says the same and no separate notice is sent.
- **TX-6 Determinism.** The same selection, run identity, chain and revision bytes give the same text (prototype P-48). The `run_text` record keeps the lines and identities, not a second copy of the bytes (the store holds them; Codex's history holds the text).
- The model is not shown other registered workflows: the text names only this workflow and, on a chain line, the previous one (R19-7; prototype P-49).

### 16.3 Chaining (R19-2; DECISION-L L-2)

- **CH-1 One run at a time.** A conversation has at most one run in force. Starting another while one is in force is refused ("end it first"). The person may confirm **End ‹A› and start ‹B›** in one step: the App records run A ended by the person (DEF-4) with cause *ended to start ‹B›* (R20-11 (4), EXEC's wording; on a finished report the cause is *completed*, FN-2), then starts B. While a run is in force, a proposal or a selection of B is offered only as this one step; a plain **Start ‹B›** is offered only when no run is in force (R20-11 (1)).
- **CH-2 (a) Sequential.** After run A ends — only by the person (DEL-01-02 DEF-4) or by the run owner, recorded *ended by the person*, *ended to start ‹B›* (CH-1), or *completed* when the person ended it on the agent's finished report (R20-1; FN-2) — the person selects workflow B; its selection carries `prior_run` (SL-7); B's run text opens with the chain line; B's run record cites A as the run it follows in this conversation (a relation, not part of B's identity; join for RS).
- **CH-3 (b) Agent-proposed.** See §16.5. Nothing starts until the person confirms.
- **CH-4** Runs are never nested in this pass. (c) declared chaining is DEL-02-01's later work.
- **CH-5** The conversation view marks each run's start and end (DEL-01-04); the marks come from the run's open and end, not from the text.
- **CH-6** Earlier run texts stay in Codex's history and are resent on every later turn (OBS-3 W-2, W-2b: nothing is removed; a recorded text is replayed as recorded, even after the file changes). The chain line is what tells the model the earlier workflow no longer applies (U-WR-19).

### 16.4 States (one table per stateful thing)

**Workflow in force, per conversation.**

| From | Event | To | Record |
|---|---|---|---|
| none | The person selects a revision (or confirms a proposal) and DEL-02-03 opens run A | *starting A* | `selection_record`; `run_text` (run start, chain if any) |
| *starting A* | `turn/start` accepted with the run text as its first element | *A in force* | supply check pending |
| *starting A* | `turn/start` refused or fails before the item is recorded | none (run start not confirmed; DEL-02-03 decides the run's standing) | `supply_check` *not found* |
| *A in force* | The person selects B | *A in force* (refused, CH-1) or, on "End ‹A› and start ‹B›", *starting B* via A ended | — |
| *A in force* | The person (or the run owner) ends run A (R20-1) | *A ended, notice pending* | run end by DEL-02-03 |
| *A ended, notice pending* | Next turn without a run start | none | `run_text` (run end notice) on that turn |
| *A ended, notice pending* / none after A | A run B starts | *starting B* (chain line names A) | as above, with chain |

**Supply check, per run text** (never relabelled; each read is a new check).

| State | Condition |
|---|---|
| *verified* | The turn's user message holds a text element whose identity equals the composed text's |
| *text differs, workflow bytes equal* | The text differs under the same method, but the extracted body (TX-3) has the same method/scope and equals `WORKFLOW.md`: framing changed |
| *text differs, workflow bytes differ* | Neither matches (for example line endings converted) |
| *incomparable* | Observed text exists, but its method differs from the preserved expected text method, or a required body comparison has a different method. Preserve both identities and an explicit limit; no equality or changed-byte inference. Historical checks remain historical |
| *not found* | The turn, its user message or a text element is absent |
| *unreadable* | The `thread/items/list` read failed, or one of its pages could not be read (SC-3; R21-4); read again later |

### 16.5 Agent proposals (R19-2 (b); PROPOSED)

- **PR-1** A proposal is the **last non-empty line** of a completed agent message (R20-11 (2)), appearing at most once in the message (a message with two such lines has no proposal), alone on its line and exactly `Next workflow: ‹origin›:‹name›`, with ‹origin› one of `project`, `user`, `bundled`, `host` and ‹name› a WD name (R20-5, R20-9; the form the proposal line of §16.2 and the product guidance tell the model). Any other mention of a workflow, including a line that names no origin, is not a proposal.
- **PR-2** The App resolves ‹origin›:‹name› among the registered workflows of that origin (SL-3's candidates, restricted to the named origin). When exactly one workflow matches, it offers **Start ‹workflow›** showing it (origin, source root, revision, standing); nothing is selected until the person confirms. (RX: before R20-9 the name was unqualified and the person picked among candidates; R20-5 asks for a line naming one registered workflow, as NIR-v0.2 §5.7 RN-3 reads it.)
- **PR-3** A pair whose name is only a draft gives the notice "proposed workflow ‹origin›:‹name› is a draft only — not a workflow identity"; an unknown pair "proposed workflow ‹origin›:‹name› is not registered"; a pair that matches several workflows (for example two host source roots) "proposed workflow ‹origin›:‹name› names more than one registered workflow". None offers Start (NIR-v0.2 §5.7 RN-5).
- **PR-4** The proposal is never a selection and never starts anything. Confirming it is ordinary input (R17-9), recorded as a selection with `how` = "agent proposal confirmed by the person" and the `proposal` reference; the run text records `origin_of_start` accordingly. If a run is in force, the offer is only "End ‹A› and start ‹B›" (CH-1); a plain "Start ‹B›" is offered only when no run is in force (R20-11 (1)).
- **PR-5** A newer proposal or the person's own selection supersedes an open offer; offers are not kept across relaunch.
- **FN-1 Finished report (R20-1, R20-9, R20-11 (2)).** A line alone on its line, exactly `Workflow finished: ‹origin›:‹name›`, that is the last non-empty line of a completed agent message or the line immediately before its proposal line (PR-1), and appears at most once in the message, naming the workflow of the run in force (its tuple's origin and name), is a finished report. A report naming another workflow, or naming no origin, is ignored.
- **FN-2** On a finished report the App offers **End run**; with a proposal (PR-1) in the same message it also offers **End ‹A› and start ‹B›**. Choosing either ends run A with cause *completed* (R20-1); ending a run at any other time is *ended by the person*, or *ended to start ‹B›* when the person confirms the one step without a finished report (CH-1; R20-11 (4)).
- **FN-3** Nothing ends a run from the agent's words alone: the run stays in force until the person chooses (prototype P-60). The App never ends, opens or focuses anything because of the report (R18-5's rule for arrivals applies alike).

### 16.6 Supply check against Codex's history (R19-7; R21-4; PROPOSED)

- **SC-1** Before sending, the App records the `run_text` (expected text identity and `WORKFLOW.md` identity).
- **SC-2** `turn/start` carries `clientUserMessageId` = an App identifier for this run start (stable `TurnStartParams` field, `observed-in-generated-types`), and `text_elements: []` on the text element.
- **SC-3** When the turn's user message item completes, or at the latest at turn end, the App reads the turn's items with `thread/items/list {threadId, turnId}`, following `nextCursor` to the last page (R21-4: the history read HOSTING-v0.9 §4.4 "Recovery reads" recommends; `thread/read {includeTurns: true}` drew a `deprecationNotice` at 0.158.0, OBS-2 §11), and finds the `userMessage` item whose `clientId` equals the identifier sent (that `clientId` echoes `clientUserMessageId` is an **inference** from the generated names, U-WR-15); failing that, the turn's first `userMessage`. It takes the first `text` element of its `content`.
- **SC-4** It computes the identity of that text and sets the state (§16.4). Only *verified* lets the run record say the workflow was **supplied**; every other state reads "supplied — not verified" with the state; for *unreadable* that means the App observed its own send and Codex's copy could not be read (R20-11 (3); EXEC §6.1 and RS R3 use this value). Whether the model followed it stays unknown (*supplied* is not *adopted*; WD §6.2).
- **SC-5** The check is written as a `supply_check` and handed to DEL-04-03 as the R3 evidence for that run and turn; HOSTING §8.2's per-turn tap record, where it exists, is separate evidence of the request.
- **SC-6** After a relaunch or a lost observation the App may read again; each read is a new check (the earlier one is kept).

### 16.7 Sequences with failure behaviour

**SQ-RUN — start a run.**

| Step | Action | By | Failure · reported by · then |
|---|---|---|---|
| RN-1 | The person selects (or confirms a proposal); `selection_record` | Person; DEL-02-02 | Not runnable (SL-5) · refused · review to register |
| RN-2 | DEL-02-03 opens the run (run identity); CH-1 checked | DEL-02-03 | A run in force · refused, or "End ‹A› and start ‹B›" |
| RN-3 | Resolve the revision (SL-4) and compose the run text (§16.2) | DEL-02-02 | Not resolvable or not verified · the run does not start (EXEC A-1 wording); `WORKFLOW.md` not UTF-8 · cannot occur after HY-7, reported if it does |
| RN-4 | `turn/start` with [run text, person's text] | DEL-01-04 | Refused or failed · `supply_check` *not found*; DEL-02-03 records the run start as not confirmed |
| RN-5 | Supply check (SC-3, SC-4; `thread/items/list`) | DEL-02-02 | *unreadable* · read again later; mismatch · recorded, shown "supplied — not verified" |

**SQ-END — end a run without a successor.** EN-1 the person ends the run (cause *completed* when on a finished report, FN-2; otherwise *ended by the person*), recorded by DEL-02-03; EN-2 the next turn carries the end notice first (TX-5); EN-3 supply check of the notice. If no further turn comes, nothing more is sent.

**SQ-CHAIN — (b) proposal.** CP-1 an agent message completes with a proposal line (PR-1); CP-2 offer (PR-2, PR-3); CP-3 the person confirms (PR-4) or ignores it; CP-4 SQ-RUN from RN-2 with `prior_run` and the chain line.

### CC-WR-TEXT-METHOD-ADOPTION receiving boundary

Bounded 2026-10-05 source adoption; historical fixture identities remain intact. Receiver fields remain `run_text.text_identity`, `run_text.workflow_file.content`, and `supply_check.expected_text/expected_workflow/observed_text`, each `{method,value}`; `supply_check.state` adds `incomparable`. WR package identity/ID-2/RB-1…RB-4 and native supply/registration evidence remain independent. Product I2 must separately adopt the reviewed schema/semantics. No human gate, authentication, act, registration or model adoption is inferred.

### 16.8 Immutable App supplier publication (CC-WR-RECORD-PUBLICATION)

This bounded App allocation completes §8 and SC-1/SC-5 under RS §13.7's
App-local Rust/project ownership. It does not allocate an external host service.

**WP-1 Location and identity.** The Rust WR publisher writes one immutable UTF-8
JSON envelope per selection_record, run_text or supply_check at the explicitly
opened owning project's `.chirality/records/workflow/<record-key>.json`.
`record-key` is a newly minted lowercase UUID; the reference is exactly
`wr-record:v1:<record-key>`. It is a supplier record identity, separate from
body selection/check/run identities and every native identifier. The filename
is only its safe mapping. No source-root, library, cwd or user-data inference
can establish the owning project. Unknown or unwritable project means recording
unavailable, visibly pending/missing; there is no fallback store.

**WP-2 Envelope.** `workflow-record-envelope.schema.json` defines the versioned
container. `record_id`, `writer`, `observed_at`, typed `body`, `basis_records`
and `source_references` are immutable. `observed_at` is the producer's original
observation/preparation time, not retry time. Body run/conversation and all
source-qualified workflow identities remain unchanged. Selection may precede
run opening; publication never creates a run. A run-start run_text cites exactly its
published selection in basis_records. A run-end-notice run_text cites exactly
the original published run-start run_text for the same run and conversation;
that start must resolve through its original selection. Its different purpose
is the explicit start-to-end source relation, not a disagreement. The end-notice
body remains unchanged: no workflow tuple or source bytes are copied into it.
A supply_check cites exactly its published run_text, matching that text's
purpose, run, conversation and expected text identity. When that run_text is a
run start and the check carries expected_workflow, its method and value must
equal the run-start workflow_file.content method and value; never compare only
digest characters or substitute the whole-package revision. This adds no
workflow_file or expected_workflow requirement to a genuine end notice or its
check. Selection has no WR basis.
For start-to-selection compare conversation, selection identifier, workflow
identity and holding library; for end-to-start compare conversation and run,
and require the basis purpose to be run start. Resolve every link through the
same explicit owning-project handle. Only the cited original start supplies
the end notice's workflow source identity to RS; the end text's own identity
remains the R3 content identity. Missing, wrong-scope or unresolvable original
start leaves source receiving incomplete, never repaired by parsing framing or
copying a tuple from another run. No duplicate coordinate fields in the
envelope supersede those bodies.

**WP-3 Content boundary.** Existing WR bodies retain their meaning: run_text is
App-composed guidance metadata and framing, with source bytes linked in the
immutable revision store, not copied into a new cache. The exact composed text
is recomputed and checked against text_identity/text_bytes before send. This
allocation stores neither Codex transcript/items/pages nor generated supplier
prompts, user messages, model output, credentials or native response bodies.
supply_check preserves opaque native turn/client/item identities, comparison
identities, read time and limits. source_references are opaque references to
actual source observations/receipts; references do not imply their source is
still available. Do not manufacture a durable receipt from an in-memory token.
The published check remains a historical observation when a source reference
later becomes unresolvable; fresh verification requires a new native read/check.

**WP-4 Publish and resolve.** Validate the envelope and body using locally
registered WR/WD schemas; check WP-2 relations. Serialize once, create a staging
file in the same owning directory, write and sync it, publish without replacing
an existing destination, and sync the directory before returning `published`.
Staging files are never resolvable records. If an identity already exists,
byte-identical serialized bytes are an idempotent retry; different bytes are
an identity collision, never overwrite. Retain the original serialized bytes
for retry. After an uncertain publication result, resolve that same identity
and verify bytes/durability before declaring success; never mint a replacement
identity just to hide a failed attempt. The resolver accepts an explicit owning
project handle and reference, parses only the UUID mapping, enforces containment
and refuses symlink escapes, validates the complete file and exact record_id,
and returns resolved/missing/unreadable/invalid/conflicting status. Historical
unknown envelope versions are preserved and reported unsupported, never coerced.
No recursive search of other projects or libraries is permitted.

**WP-5 Ordering and failure.** Publish selection then run_text before invoking
the sender (SC-1). Failed required pre-send publication leaves this prepared
workflow submission unsent and visibly pending; it neither ends the run nor
pauses unrelated work or adds a human permission gate. A retry only publishes
the same pending original records; dispatch remains a separate once-only step
under the existing native submission/client correlation owner. After dispatch,
check or RS write failure must never cause resend. Each reread creates a new
check identity (SC-6); retrying a check's publication preserves its original
identity, bytes and read_at. R3 is recorded only after its supplier references
resolve. WR publication and RS append are separate commits: a published WR
object without R3 is visible missing-in-record, not a supplied-guidance entry.
Retained RS entries follow W-0…W-2 in original order/time with failure evidence.
A stopped writer loses unpersisted pending observations; a later run cannot
back-fill them or reconstruct them from guesses. Restart may resolve existing
objects and original pending custody only; it does not infer delivery, run end,
adoption or permission to resend.

**WP-6 Lifetime and handoff.** WR records live with the owning project and are
not garbage-collected or rewritten by this allocation. Moving the whole project
preserves references through the explicit new project handle; copying a record
alone establishes no new provenance. Revision-store/source reference loss is
reported separately and never repaired by native transcript mirroring. The WR
publisher returns the durable reference and resolution status to EXEC/Root and
RS; RS R3 uses supplyRecord for run_text and supplyCheckRecord for the immutable
check. The RS receiver owns nativeTurn/incomparable admission. Native UUIDs stay
opaque; no ordinal is fabricated. Publication gives no A15, registered, run-open,
run-end, model-adoption or product-qualification standing. Selected-development
evidence cannot be laundered into a registered selection_record.

**WP-7 Required receiving checks.** Before implementation is claimed, exercise
process-loss reopen; selection→run_text→send ordering; unknown-project refusal;
no-replace collision and byte-identical retry; torn/staging/sync failures;
wrong-project, escaping and unsupported references; two rereads versus one
publication retry; post-send check/R3 failure without resend; source-store loss;
and native thread/turn/item/client and content correlation for every check state.
Preserve the existing source-owned native-page comparison path. Lifecycle
opening/ending/chaining remains EXEC-owned and separately examined.
