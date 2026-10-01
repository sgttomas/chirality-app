# Workflow-making workspace and registration

- **Contribution:** DEL-02-02/WR-v0.1 (first Design file of this deliverable).
- **Status:** DRAFT DEFINITION — proposed, not implemented, not accepted. Nothing here is built, qualified or owner-reviewed.
- **Run / node:** `APP-V4-DESIGN-PASS-3-20261001`, node D5 (BRIEFS.md "D — design nodes, round 1", row D5). Type 2 TASK executor, harness-native descendant of the HELP_HUMAN session; no delegation. Written 2026-10-01 in the working tree at HEAD `dc031b5bec` (branch `claude/chirality-app-v4-60-percent-a41fd5`).
- **Serves:** OUT-001, OUT-002 (design of the CODE), OUT-003 (fixture design and a design prototype), OUT-004 (receiving and reuse account, §7, §10); REQ-001…REQ-008; AC-001…AC-008 by designed verification (§12); VER-001…VER-006 (cases designed; library-side parts run on the prototype only).
- **Labels** (as R9 and R17): **SETTLED** (an accepted text or owner decision says it), **DERIVED** (follows from those), **INTEGRATION** (an integrator ruling, open to the owner), **PROPOSED** (a design structure of this file, decided by no one). Supplier facts carry `observed`, `observed-in-generated-types` or `inference` (R17-13).
- **Basis (binding):** the accepted basis as amended by SCA-V4-001 and SCA-V4-002; DAG-003 (`_DAG/DAG-003/HANDOFF_STATE.md` sha256 `56d849b6d078d8d5…`; held arcs non-gating); DECISION-K3 as revised (`OWNER_DECISIONS.md` sha256 `9d18c40dd7d894dc…`): K-6, K-7 (owner's alternative), K-8 bind this file; DECISION-K1 K1-1…K1-4; R1–R16; R17-1…R17-16 (`R17_RESOLUTIONS.md` sha256 `b0af81bcbad9bc52…`); DECISION-3 (host joins deferred).
- **Consumed inputs** (sha256 by `shasum -a 256` in the working tree at `dc031b5bec`; full values in the return file `D/D5.md`): `BRIEFS.md` `b261394112d7264e…`; `DECISIONS_PENDING.md` `431ec4eb22a0b913…`; `SURVEY/S1-C.md` `06a8a6667ca7c64d…` (Part A whole; Part C); this deliverable's `ScopeOfWork.md` `5814116909db8120…` and `Dependencies.csv` `be14a079c872695e…`; WD-v0.8 `WORKFLOW_DECLARATION.md` `517821d18fc95830…` (§3.5–§3.9, §6, §7, §8, §9, §12, §13.1); WD-EX-v0.8 `EXAMPLES.md` `275ea54d32cd8f48…` (E1 intro, E3, E4, E5); EXEC-v0.6 `EXECUTION_COMPATIBILITY.md` `64e732d502d0b91d…` (§2.6, §2.7, §3.1, §5, §6, §7.3, §9, §10, U-E19); ACT-POLICY-v0.8 `ACT_AND_POLICY_CONTRACT.md` `6fb6b9e883fa8d20…` (§2.1 A15, §2.4, §2.5, §2.6, §2.8, §4.7, §10.3, FX-56); RS-v0.8 `RECORD_SEMANTICS.md` `b25cc90e9e252f50…` (§4 R2, §6.1, §6.2 HA-10, §10, U-05) and `RS_RECORD.schema.json` `b63a7e421b885854…`; CA-v0.6 `CONNECTED_ACTIVITY_CONTRACT.md` `58167f7accaf356e…` (§2.1 parties, §3, §4, §6, §8.2); HOSTING-BOUNDARY-v0.8 `HOSTING_BOUNDARY.md` `3cf0381c42358fec…` (§8 seams S-6, §8.2, §11, §12); `loop/LOOP_INIT.md` `3790159b4f60bb4f…` ("Develop the detail appropriate to the phase"); DAG-003 `DependencyEdges.csv` `4716ca287d23835c…` and `CandidateEdges.csv` `07b969209e273310…` (arcs naming DEL-02-02, by script). Read in progress, not pinned as a basis: DEL-01-04's node-D3 schemas `aac.offer.schema.json` (`4f1be0814168cf58…`) and `nir.draft-transition.schema.json` (`da2f57c1122d3578…`) and DEL-01-04 `ScopeOfWork.md` `0cdb44e297010b70…` (OUT-004, REQ-003, REQ-004). Historical exemplar (evidence only, never a v4 commitment): App v3 `projects/chirality-app-dev/frontend/src/app/api/working-root/workflow-drafts/workflow-draft-store.ts` `185532db8cddcb39…`, `route.ts` `567789715473356c…`, `components/woven-dialogue/workflow-draft-review.tsx` `b5f4bcfad3429a78…`; Root `AGENTS.md` and `workflows/create-workflow/WORKFLOW.md` as current Root practice (read via the survey, S1-C §A.5).
- **ScopeOfWork reading (R17-15).** The ScopeOfWork lags the owner's answers in four places. This file reads it as follows; precise SCA-V4-003 proposals are in the return file.
  1. REQ-001, OUT-001, AC-001, VER-001 "trial through real native Codex tool execution": read per **K-7** as trial **in an ordinary conversation** with real tools, which is not a run of any workflow identity; only registered revisions run.
  2. REQ-003 "this contract does not select a new overwrite policy": **K-6** has since chosen one (a revision series per library slot; nothing overwritten), which §4.1 designs.
  3. REQ-002, REQ-006, AC-006, CLM-004, REQ-008: registration (A15) is captured by **DEL-01-04's App act control** (K-8; R17-6), bound to the exact reviewed bytes; this deliverable supplies what the control presents (§4.3) and performs the registration that follows.
  4. OUT-002, REQ-004 "host-supplied": the origin value is `host` (WD §6.1, S-D); "host-supplied" is not a value (terminology only).
- **Receivers:** DEL-01-04 (DEP-01-04-009, held), DEL-02-03 (DEP-02-03-010, held), DEL-09-02 (DEP-09-02-016, admitted), DEL-09-06 (DEP-09-06-026, admitted), and DEL-02-04 through the row R17-8 proposes. Suppliers: §7.

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
| R17-8 | DEL-02-04 composes the selected workflow into `developerInstructions`; an agent's own read of the file is a tool item, not evidence of supply | INTEGRATION |
| R17-9 | No automatic decline; plan acceptance is ordinary input; untyped sessions are allowed | INTEGRATION |
| R17-11 | WD §6.1 and EXEC HR-4 keep *derived-from* for the parent workflow identity. The A15 record names its subject by the **reviewed draft content** and, for a new revision, the **prior revision** | INTEGRATION |
| K1-1, K1-4 | The agent asks (A8); the product never asks in its place. The person is recorded as the App observes them, "identity not verified" | SETTLED |
| ACT §2.1, §2.6; RS HA-10 | A15 is the person's act; never evidenced by draft creation, a trial, an agent's recommendation, a review of other content, an earlier revision's registration, or a file an agent wrote into a catalog | INTEGRATION (R12-5) |
| WD §6.1 RV-1…RV-5; §6.3 C-1…C-6; §7 | Revision file set and canonicalization; collisions exposed, never rebound; Root package and name conventions kept | PROPOSED in WD; consumed unchanged |
| D3 (DECISION-1) | Tool permission and sandbox modes stay the user's own Codex setting, so the App cannot stop an agent writing into a library folder; it can only make the standing of such content truthful (§4.6) | SETTLED |
| DECISION-3 | Host joins deferred: host listing, relay and precedence are designed only as far as App-side behaviour needs | SETTLED |

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
- **ID-3 (PROPOSED).** A draft is referred to as `draft:<location>:<name>@<content identity>` wherever a string is needed (RS's present `relations.derivedFrom` uses this shape, §8). A draft reference without a content identity names a folder, not content.
- **ID-4 (DERIVED, EXEC §6.6).** Lineage is followed through derived-from links; a link that cannot be resolved is shown as "lineage incomplete at ‹tuple›", never guessed.

## 3. Layout and data placement (PROPOSED; OI-008 and RS U-05 stay open)

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
| Trial pointers | App data folder | The App | App-observed pointer; not a run record (TT-4) |
| Bundled workflows | Inside the App bundle, per release, read-only | The release | Origin *bundled*; runnable without A15 (LS-5) |
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
| **DS-4 refused: identical content** | The reviewed content equals a revision already registered in the slot | Nothing registered | "Identical to revision ‹k›; select it instead" |
| **DS-5 refused: draft not valid** | A refusing hygiene finding (HY-1…HY-5, HY-7) | Nothing registered | The findings |
| **DS-6 refused: changed since review** | The live draft changed while the snapshot was taken | Nothing registered | "Review again" |
| **DS-7 in place** | The slot holds content with no registration record (LS-2) and the draft is identical to it | First revision; the slot's bytes unchanged | "Registers the content already in this slot" |
| **refused: slot moved on** | Between review and publication another revision was registered in the slot (§6 G-1) | Not completed; the A15 stands, recorded as not effective | "Another revision was registered after this review; review again" |

- **SP-5 (PROPOSED).** Every review also lists the same name in **other** libraries and origins, each with its holding library and standing (C-1). This is a notice ("shadows bundled create-workflow"), not a refusal: a selection holds a full tuple, so a new same-name entry rebinds nothing (C-2).
- **SP-6 (PROPOSED; R17-11).** A new revision's derived-from is its **draft base** (none when there is no base). The prior-revision link is separate: it is the slot's latest revision at review, recorded in the A15 relations and the ledger. For a refinement made from the latest revision the two name the same tuple; for a stale base or a round trip they differ, and both are shown.
- **SP-7 (PROPOSED).** A draft made from an earlier revision than the slot's latest (a stale base) may still register as DS-2. The review states "made from revision ‹i›; the latest is revision ‹j›; changes in ‹j› are not in this draft" and shows the difference against both. Nothing is lost, because ‹j› stays.

### 4.2 Drafts and trials (K-7)

- **TT-1 (SETTLED).** Only registered revisions (and bundled or host-listed workflows, LS-5, LS-6) are selectable for a run. Selecting a draft is refused with EXEC T-1's words, "draft only — not a workflow identity", and the offer to review it.
- **TT-2 (DERIVED).** A draft is tried in an **ordinary conversation**: no workflow is selected, no run is opened (no RS `run_opened`), DEL-02-04 composes no workflow into the conversation's instructions (R17-8), and EXEC's recorder records no checkpoint arrival, because there is no run. The agent works with real native tools, which is V4-EXM-10's "trial"; its reading of the draft file is a tool item.
- **TT-3 (PROPOSED).** The workspace offers **Try in a conversation** on a draft. It opens a new conversation with no workflow selected; the role and model are chosen as for any conversation (DEL-02-04; K-3: no model until the person chooses). The App pre-fills, and does not send, a message naming the draft's path and content identity; the person edits and sends it. Pre-filled text is the person's input once sent.
- **TT-4 (PROPOSED).** The workspace keeps a **trial pointer** {draft key, draft content identity at the time, conversation, time}, labelled "draft tried in conversation; not a run of any workflow identity". It is not a run record, not compatibility evidence and not A15 evidence (ACT §2.6 lists "a successful trial run" among non-evidence; under K-7 there is no trial run at all).
- **TT-5 (DERIVED).** A human act performed during a trial conversation (for example A4 on an App file through the act control) is recorded outside any run, in the act log, as for any conversation.
- **TT-6 (DERIVED).** Checkpoints declared in a draft are not evaluated in a trial. The review shows the declared part's reading (WD VO-1…VO-10); a run of the registered revision is where checkpoints are recorded (EXEC §2.4).
- **TT-7 (PROPOSED).** Each refinement that needs a recorded run is registered first, as a new revision (K-6); "refine twice" (V4-EXM-10) is two registered revisions, each run on new inputs.

### 4.3 Review binding and the registration act (K-8; R17-11)

- **RB-1 Snapshot.** Opening a review copies the draft's regular files into staging, computes the content identity of the copy, recomputes the live draft's identity after copying, and compares both with the identity shown in the draft list. Any difference: DS-6, "the draft changed while it was read; review again". (App v3 made the same check; §10.)
- **RB-2 Review package** (what the review view shows; DEL-01-04 presents it, §7): the target slot and disposition (SP-4) with its message; the reviewed content identity and method; the file list with per-file sizes and digests; `WORKFLOW.md`; the declared part's reading with its FB findings (WD §3.7), shown as information; hygiene findings; the difference against the prior revision and, when it differs, against the draft base; lineage; the same name elsewhere (SP-5); and the sentence "Registering makes this revision available in ‹library›. It is not a check that the workflow can run here." A compatibility report (EXEC CK-1) may be shown beside it, labelled as a check of this environment (REQ-005).
- **RB-3 Freshness.** The review stays current while (a) the live draft's content identity equals the snapshot's and (b) the slot's latest revision is still the prior revision bound (or the slot is still empty). The workspace watches both. When either fails it withdraws the A15 descriptor, the act control stops offering it, and the draft shows "changed since review — review again" (K-8).
- **RB-4 A15 descriptor** (`a15_descriptor`), handed to the act control for a registrable disposition (DS-1, DS-2, DS-7): act kind A15; wording "register workflow revision"; subject = the target tuple with the revision (ID-1); bound content = the snapshot's content identity (equal to the subject's revision, ID-2; a reader check); relations {reviewed draft (draft key and content identity), prior revision (tuple or none), derived-from (tuple or none)}; disposition; scope = the library; purpose "make it available in the project library" or "make it available in the user library" (ACT's single "in the project" wording does not fit the user library; join J-15); review reference; freshness values; and the agent's A8 request record, where one was recorded (RS R16).
- **RB-5 Capture (DEL-01-04).** The act control captures A15 only from the person's native interface event (R17-5; CAP-4). The agent may ask the person to register (A8; K1-1); an answer to a supplier user-input or elicitation request is never A15 (CAP-6); a chat statement is not either (CAP-7). The control records the person as the App observes them, "identity not verified" (K1-4).
- **RB-6 Publication uses the snapshot.** The registration writer publishes the snapshot's bytes, never the live draft's, after re-checking the slot (G-1). The bytes registered are therefore the bytes reviewed, whatever happens to the draft afterwards.
- **RB-7 Review is not an act.** Showing a review is an App presentation, recorded as a `review shown` transition. It is never recorded as a human act (ACT §2.1: "a draft's review is not A15"). REQ-002's "the person reviews the identified content" is evidenced by the A15's binding to the content the review showed (S1-C §A.4 item 5, option (a); INTEGRATION), not by a separate act kind.
- **RB-8 One act, one revision (PROPOSED).** An A15 completes at most one registration: the one for its descriptor. An act whose registration did not complete is recorded as not effective and is never reused for other content or a later attempt (FX-56 (c); VER-002). The only continuation is §6 SQ-X, which finishes the same attempt after an interruption when nothing has changed.

### 4.4 Selection (WD C-1…C-6; U-10)

- **SL-1 (DERIVED, C-2, C-3).** A selection is the person's explicit interface choice of a full tuple **with revision**, with its holding library. It is an ordinary interface choice, not a reserved act. An agent's mention or suggestion of a workflow is not a selection.
- **SL-2 Pinned (PROPOSED; answers WD C-4 for the App).** A selection stays on its revision. When a newer revision is registered in the slot, the selection shows "newer revision ‹n› available"; following it is a new selection event citing the one it replaces (C-3). The chain therefore always shows which revision was resolved and supplied (C-4), and every run cites its revision (K-6).
- **SL-3 Unqualified names (PROPOSED; answers WD C-5 / U-10 for the App).** A name typed without origin gives a candidate list ordered project → user → bundled → host (host last). When more than one origin holds the name the person picks; nothing is resolved silently. Host listing waits with the host joins (DECISION-3).
- **SL-4 (DERIVED, C-2; EXEC RF-2, FB-08).** Discovery changes after selection (new same-name entries, a new revision, an edited or removed published copy) never change the selection. A selection is resolved from the **revision store**, never from the published copy; if its bytes cannot be found or do not recompute, the result is "selected revision not resolvable" or "revision not verified", never a substitute.
- **SL-5 (SETTLED, K-7).** Content without registered standing (a draft; LS-2, LS-3, LS-4) is refused for selection with its standing and the offer **Review to register**.
- **SL-6 (DERIVED).** Reuse on new inputs is a run of a selected revision, started through DEL-02-03 (EXEC SQ-A A-1, A-2); the inputs are conversation inputs.

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
| **LS-1** | registered | A ledger entry *registered*, its A15 record found with the same bound content, and store bytes that recompute to the revision | Yes | Select; Refine |
| **LS-2** | present without registration record | Content in the published-copy location of a slot with **no** registered revision (an agent or the person wrote it; a Root-era or App v3 library) | **No** (K-7) | Review to register (DS-7 in place) |
| **LS-3** | library copy changed outside registration | The published copy differs from the slot's latest revision | The registered revisions stay runnable; the changed copy is not | Review the change (a draft with base = the latest revision, DS-2). On the next publication the changed copy is kept aside, never overwritten |
| **LS-4** | registration record incomplete | A ledger entry whose A15 record is missing or bound to other content, or whose store bytes do not recompute | No; "revision not verified" | Review to register |
| **LS-5** | bundled | Shipped in the App release | Yes | Select; Refine into the user or a project library (a new workflow with derived-from the bundled tuple) |
| **LS-6** | host-listed | Listed from a host library or held in the import holding library | Per host rules (deferred) | Open read-only; Refine (EXEC HR-1…HR-4) |
| **LS-7** | not established | A non-regular entry in the store or published copy (RV-2) | No | — |

LS-2's "not runnable" follows K-7's "only registered revisions run". It affects every existing project library written before v4 (Root's panel, App v3), each of whose workflows needs one in-place review and A15 before it runs. That consequence is **flagged for the owner** (U-WR-4); the alternative is to run such content with its standing shown.

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
| *under review* | A15 captured and registration committed | *registered, unchanged since*; the App records the new revision as the draft's base | *registered*; `library_entry` *registered* |
| *under review* | A15 captured; registration not completed | *draft* | *registration not completed*; `library_entry` *not completed* |
| *registered, unchanged since* | Files change | *draft* (a refinement of that revision) | *changed* |
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

### 5.3 Library entry (per revision) and published copy

| From | Event | To |
|---|---|---|
| — | G-4 | *registered* (LS-1 when read) |
| *registered* | At read, the A15 record is missing or the store bytes do not recompute | *registration record incomplete* (LS-4); not runnable |
| *registration record incomplete* | The record or bytes are restored | *registered* |
| *registered* | Nothing removes it in this design (no withdrawal; U-WR-6) | — |
| Published copy equals the latest revision | Files in it change | *library copy changed outside registration* (LS-3) |
| *library copy changed outside registration* | A new revision is published (G-5) | The changed copy is moved to the kept-aside location; the new latest is published |
| Slot with content and no registration | — | *present without registration record* (LS-2) → DS-7 → *registered* |

### 5.4 Selection (per conversation)

| From | Event | To |
|---|---|---|
| none | The person selects a tuple with revision whose standing is LS-1, LS-5 or LS-6 | *selected* (pinned) |
| none | The person tries to select a draft or LS-2/LS-3/LS-4 content | none; refusal with standing and "Review to register" |
| *selected* | A newer revision is registered in the slot | *selected*, "newer revision available" shown |
| *selected* | The person selects another tuple | *selected* (a new event that cites the one it replaces) |
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
| R-3 | Disposition (SP-4), lineage, same name elsewhere | DS-3 / DS-4 · as the message says |
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

**SQ-S — select and hand off a run.**

| Step | Action | Failure · next |
|---|---|---|
| S-1 | Listing with standings (§4.6) and collisions (C-1) | Library unreadable · listed as *not established* |
| S-2 | The person selects (SL-1…SL-3); `selection_record` | Draft or no registered standing → refused (SL-5) |
| S-3 | Hand-off to DEL-02-03 (EXEC A-1 CK-1 check; A-2 run start) with the selection record; the resolver reads the store (EXEC §6.1 *resolved*) | Not resolvable or not verified → EXEC's wording; the person may choose again |
| S-4 | DEL-02-04 composes the resolved bytes with role and product guidance (R17-8) | Supply not observed → *supplied* unknown (HOSTING §8.2) |

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
| X-2 | For an attempt in *stored*: if the slot is unchanged, complete G-4 and G-5 citing the **same** A15 (the act bound this content and this prior revision, and nothing changed); otherwise write *not completed* | — |
| X-3 | Re-publish a stale published copy from the store when it equals neither the latest revision nor content kept aside | — |
| X-4 | Review packages are not restored: an *under review* draft returns to *draft*, and its descriptor is withdrawn | — |

## 7. Interfaces

Arc layer per DAG-003 (`admitted` / `held` in SCC-002). Direction is consumer → supplier. Where this deliverable is the supplier, the interface is **offered**; R17-10's cycle guard is respected (DEL-01-02 and DEL-01-03 consume nothing from here).

| Other side | Row · arc · layer | What flows | Condition of use | When the exchange fails |
|---|---|---|---|---|
| DEL-01-03 native plans, tools, delegation | DEP-02-02-012 · admitted | Plan items and revisions, tool items, delegation items shown in journey conversations (J-1, J-2) | Plan and delegation views exist only with Codex's experimental opt-in (K-5); plan revision identity is DEL-01-03's | Views absent: the journey works in prose; nothing in the workspace depends on a plan item. Plan acceptance is ordinary input (R17-9) |
| DEL-01-04 native requests, outcomes, attachments, draft view | DEP-02-02-013 (receive) and DEP-01-04-009 (offer) · held, SCC-002 | **Offered:** `draft_reference`, `draft_transition`, `registration_disposition` (collision and refusal standing), the review package (RB-2). **Received:** the native draft view and review presentation (DEL-01-04 OUT-002, OUT-004, REQ-004); attachments into conversations | DEL-01-04 shows a draft as a draft until a *registered* transition arrives (its REQ-004) | Draft view not built: the workspace list is the only view; no transition is invented by the receiver |
| DEL-01-04 App act control (K-8; SC2-01-04-1, PROPOSED until SCA-V4-003) | DEP-02-02-013 (statement to be revised, return file) · held | **Offered:** `a15_descriptor` (RB-4) and its withdrawal (RB-3). **Received:** the capture {A15 record identity, capture-evidence reference, bound content, descriptor identity} | Capture only from a native event (CAP-4; R17-5); the control refuses capture while the descriptor is stale | Control not built: nothing is registered; the review says so (R-4). Capture refused as stale: review again |
| DEL-02-01 portable contract | DEP-02-02-014 · held | Identity tuple (`$defs/workflow_identity`), RV-1…RV-5, name rule, the declared-part reader (VO-1…VO-10) for the review, collision and rebinding rules (C-1…C-6) | Consumed unchanged | Reader finding: shown, never refusing (HY-6). Algorithm open (U-03): the prototype's illustrative digest stands in |
| DEL-02-03 execution, compatibility, round trip | DEP-02-02-015 (receive) and DEP-02-03-010 (offer) · held | **Offered:** `selection_record`; resolution from the store (the resolver reads the revision store; EXEC §6.1 *resolved*); the drafted / registered link (EXEC §6.1 *opened / drafted / registered*); the HR-1…HR-4 App steps (SQ-H). **Received:** the compatibility report (shown beside a review or a selection, labelled), T-1's refusal wording, run start | EXEC's run start is the only place a workflow runs (TT-1) | Report not established: shown so (EXEC CR-3); nothing is gated by it (CC-3) |
| DEL-02-04 role and workflow supply | Proposed row (R17-8; D6 proposes it) · would be inside SCC-002 | **Offered:** the selection record and the resolved revision's store path and content identity, from which DEL-02-04 composes the workflow into `developerInstructions` | Supply only for a selected registered revision; never for a draft (TT-2) | Supply not observed: *supplied* unknown (HOSTING §8.2). If the agent reads the workflow file itself, it reads the pinned revision's store path, not the published copy |
| DEL-04-01 operation policy and human acts | DEP-02-02-016 · admitted | A15's act table entry, binding (not lapse-evaluated), capturing surface, non-evidence list, request → capture → record sequence (ACT §2.1, §2.5, §2.6, §4.7), FX-56 | Consumed with the edits K-8 and R17-11 require (join list) | — |
| DEL-04-03 records | DEP-02-02-017 · held | The A15 human-act record (RS §6.1, HA-10), the act log outside a run, R2 trace links (*listed*, *selected* with holding library), R16 act requests | The A15 record is written by the act control's writer; the ledger cites it by record identity | Record write fails: ACT LC-2 (late write, "record write failed"); registration waits for G-0 until the capture is reported |
| DEL-09-02 standalone qualification | DEP-09-02-016 / DEP-02-02-018 · admitted | Candidate-bound fixture results and remaining limits (OUT-003), the §12 case inventory | Supplied after a candidate exists | Nothing is claimed before then |
| DEL-09-06 connected activity | DEP-09-06-026 (N-C1) · admitted | Registration for the round trip (CA §4 *opened / drafted / registered*; ST-5; W14-01, W14-09, W14-10) and the workflow-maker party's App steps | Host side waits for SQ-17/SQ-18 and the host joins (DECISION-3) | W14-01/W14-09 stay AWAITING INPUT on the host side |
| DEL-01-02 execution and recovery | Proposed row NR-1 (return file) · would be admitted, no SCC | The stop definitions (R17-3) and the App-start event at which SQ-X runs; interrupted trial conversations are shown by DEL-01-02 / DEL-01-04 | — | Without it, SQ-X runs at App start on its own; no recovery of conversations is claimed here |
| DEL-01-05 account and model access | none (runtime value only) | A trial conversation starts with no model chosen until the person chooses (K-3) | — | — |
| DEL-01-01 supplier boundary | none direct | The `fileChange` item used for draft attribution (D-3), via DEL-01-03/01-04's item delivery; S-6 carriage is DEL-02-04's | `observed-in-generated-types` only | Attribution "not observed" |

## 8. Data formats (PROPOSED; R17-1)

One schema, [workspace-registration.schema.json](workspace-registration.schema.json) (`$id` `urn:chirality:app-v4:del-02-02:workspace-registration:WR-v0.1`, JSON Schema 2020-12), with seven record kinds told apart by `record_kind`. Names are Chirality's, snake_case as WD's schema. Workflow tuples reference WD's `$defs/workflow_identity` by WD's `$id`; RS spells the same tuple in camelCase (`workflowTuple`), a one-to-one mapping (WD §3.6 spelling table).

| Kind | Receiver(s) | Content | Reader checks beyond the schema |
|---|---|---|---|
| `draft_reference` | DEL-01-04 (DEP-01-04-009); cited by A15 descriptor and ledger | Draft key, state (§5.1), content identity or "not established", file count, App-recorded base, findings | `base` present only when `base_recorded_by` is *app* (schema); content identity recomputes over the folder |
| `draft_transition` | DEL-01-04 | Event, from/to states, content identity, disposition, cause, time, attribution (*file change item* with thread and item · *app action* · *not observed*) | The workspace never emits a *registered* transition without a matching ledger line |
| `registration_disposition` | DEL-01-04; the review | Occasion (*registration review* · *discovery*), target slot, reviewed content, disposition (SP-4), prior revision, base, lineage, stale-base flag, same name elsewhere with holding libraries and standings, findings, message | DS-2 names a prior revision and DS-1 none (schema) |
| `a15_descriptor` | DEL-01-04 act control | RB-4 | `subject.revision` equals `bound_content.value` (ID-2; prototype P-39) |
| `library_entry` | DEL-02-03 resolver; DEL-02-04; DEL-09-02 evidence | Ledger line: outcome (*registered* · *not completed*), tuple, sequence, disposition, prior revision, reviewed draft, A15 record and capture-evidence references, store path, reason, evidence limits | LS-1 needs the A15 record and recomputing bytes as well |
| `selection_record` | DEL-02-03 (CK-1, A-1), DEL-04-03 (R2 *selected*), DEL-02-04 | Tuple with revision, holding library, standing, "the person (App interface)", how (*explicit* · *from unqualified name* with candidates), replaces, conversation, time | The tuple's standing is runnable (TT-1) |
| `trial_pointer` | App-kept only | Draft key, content identity, conversation, time, the fixed standing sentence | Carries no workflow identity (schema: `additionalProperties` false) |

Conformance instances: eight valid instances covering all seven kinds (`.valid.examples.jsonl`) and nine invalid instances, one named error each (`.invalid.examples.json`): a valid-state draft with a bad name; a base not recorded by the App; an invented *auto-registered* event; a new revision without its prior revision; another act kind presented as registration; a registration line citing no A15; a selection of a slot without revision; origin `host-supplied`; a trial pointer naming a workflow identity.

**The A15 record (RS's format, consumed).** The act control's writer produces an RS `human_act` with act kind A15 exactly as RS-v0.8 states it (prototype P-11, P-38): bound subject the revision, bound content its identity, purpose per library, `relations.derivedFrom` the draft string (ID-3). R17-11 asks RS to replace that relation by **reviewed draft** and **prior revision**; RS-v0.8's schema refuses those names today (P-36), so the change is a node-F join (J-21), not something this file does.

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

## 11. Process placement (R17-5; PROPOSED, OI-008 open)

Requirements, stated apart from placement: (a) no agent tool, MCP operation, App rule or supplier request can produce an A15 capture or a ledger line *registered* (CAP-4); (b) no registration is reachable through a local network endpoint; (c) publication reads only the snapshot (RB-6); (d) the ledger is appended under an exclusive lock (G-4).

Placement under R17-5's O-1: the Rust host owns the library writer (store, ledger, published copy, kept-aside content), content-identity computation, hygiene, the freshness watch and SQ-X; DEL-01-04's act control capture is produced in the host from a native interface event; the TypeScript interface composes and presents the draft list, the review package and the selection. Because D3 leaves the sandbox to the user, an agent with full file access could still write a forged ledger line and act record together; the App reports standing from what it can check (LS-1, LS-4) and claims no prevention.

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
| WR-VC-08 Hygiene | REQ-003, REQ-004 | HY-1…HY-7: refusals, and HY-6 not refusing | Library double | HY-2, HY-3, HY-4 and the refused review **ran** (P-02…P-04); HY-6 runs in every review (the declared-part note); HY-1, HY-5, HY-7 DESIGNED |
| WR-VC-09 Drafts never run | K-7 | Draft selection refused; a trial leaves only a pointer; changed library copy not selectable | Library double | **Ran** (P-05, P-06, P-29) |
| WR-VC-10 Round trip, App side | REQ-004 (CA W14-09, EXEC RT-6) | A host tuple whose lineage reaches LIB-A1 registers as LIB-A1's next revision with derived-from = host tuple; one whose lineage does not is refused | Host-listing double | **Ran** (P-32, P-33); host side AWAITING INPUT (SQ-17, SQ-18) |
| WR-VC-11 Formats | R17-1 | Every record produced conforms; static instances; reader checks | Schema, validators | **Ran** (S-1, S-2, INV-1…INV-9, P-37…P-39) |

## 13. Prototype

[`prototype/wrproto.py`](prototype/wrproto.py) (R12-3; not product code) models §3–§6 over invented packages in a temporary folder, with a double for DEL-01-04's act control whose only capture path is a modelled native event. It imports two sibling prototypes read-only: DEL-02-01's `wdproto.py` (revision file set and the illustrative digest `proto-sha256-list-0`, the declared-part reader, the name rule) and DEL-04-03's `minischema.py` (a JSON Schema subset validator whose registry resolves WD's and RS's `$id`). Workflow tuples are also checked with WD's own validator, because `minischema` does not check `maxLength`.

**Run:** `PYTHONDONTWRITEBYTECODE=1 python3 wrproto.py`, in `Design/prototype/`, on 2026-10-01 (20:06 UTC), Python 3.13.7: **58 checks, 58 passed, 0 failed**, exit status 0. The full output, with the sha256 of every input it read, is in the return file `D/D5.md`. It writes nothing outside its temporary folder and leaves no `__pycache__` (checked with `find` afterwards).

What it does not show: any Codex behaviour, any native view, the real act control, a real person, a candidate, or a host.

## 14. Joins (summary; the full list with old → new text is in the return file)

- **WD:** OS-1/OS-2 now point here and to DEL-01-04's control; §6.1's OS-file question is answered by HY-4; C-4 and C-5/U-10 get the App-side answers SL-2 and SL-3; §7's drafts row and §8's DEL-02-02 row point here; §13.1's "library and selection doubles (DEL-02-02, later)" exist in the prototype.
- **WD-EX:** E3's last column ("if registered as a new App workflow") becomes a new revision of LIB-A1 (K-6, SP-3); E4 step 3 gets the App-side pin (SL-2).
- **EXEC:** HR-4's "new tuple" reads per SP-4 (DS-2 for the round trip); RT-6/RT-7 cite K-6 and this file; U-E19's "AP U-08" half is stale (R12-5) and its slot half is answered; §9.1/§9.2/§10 DEL-02-02 rows point here; CAP-2's wording list gains A15.
- **ACT:** A15's capturing surface becomes DEL-01-04's act control (K-8) in §2.1, §2.6, §4.7 RC-3 and FX-56; content names per R17-11; purpose per library; §10.3's "Not mapped in detail (U-08)" row is filled.
- **RS:** §6.1 relations and HA-10 per R17-11, with `RS_RECORD.schema.json`'s A15 rule and the act-log example; capturing surface; purpose per library; §10 rows; U-05 for act records outside a run.
- **CA:** §3.1, §4, ST-5, W14-01/W14-09, F-1 and its UNRESOLVED row: registration is designed (PROPOSED), not built.
- **DEL-01-04 (node D3, in parallel):** reconcile its `nir.draft-transition` and `aac.offer` vocabularies with `draft_transition` and `a15_descriptor` (mapping in the return file).

## 15. UNRESOLVED

| ID | Item | Owner | Point of need | Effect here |
|---|---|---|---|---|
| U-WR-1 | Revision identity algorithm and method designation | DEL-02-01 with DEL-04-03 (WD U-03; HOSTING U-08) | Before implementation of the store and the A15 binding | The design needs *a* content identity with a method; the prototype uses WD's illustrative digest |
| U-WR-2 | Process placement of the library writer and of A15 capture | App implementation owner (OI-008) | Before architecture production contracts | Requirements §11 hold for any placement; R17-5's placement is PROPOSED |
| U-WR-3 | Location of act records outside a run, per library | DEL-04-03 (RS U-05) | Before writer implementation | The prototype keeps a per-library act log |
| U-WR-4 | Library content without a registration record is not runnable (LS-2), so every pre-v4 project library needs one in-place review and A15 per workflow | **Owner** confirmation (consequence of K-7) | Before the first release that opens existing projects | Alternative: run it with its standing shown |
| U-WR-5 | Host listing, relay and host position in unqualified names | Host owner and DEL-02-01 (WD U-10); DECISION-3 | Before host-origin discovery in the App | SL-3 places host last, PROPOSED; host steps AWAITING INPUT |
| U-WR-6 | Withdrawing or retiring a revision or a workflow | Not obligated by the ScopeOfWork | If the owner asks | Nothing is ever removed by the App |
| U-WR-7 | Hygiene values (OS-file list, 16 MiB, 1 000 files, UTF-8) | Integrator | Before implementation | PROPOSED |
| U-WR-8 | Shared types for identity, collision report and selection | App/shared contract owners (OI-014; WD §9 A-2, A-5) | Before structural allocation | The schema references WD's identity by `$id`; no placement proposed |
| U-WR-9 | A checkpoint that requires A15 | DEL-04-01 (ACT §4.1) | Later | Not designed |
| U-WR-10 | Keep the published copy at `workflows/<name>/` (portability) or drop it (store only) | Integrator | Before implementation | Kept, PROPOSED; LS-3 exists only because of it |
| U-WR-11 | Vocabulary of draft transitions and the A15 offer shared with DEL-01-04 | DEL-01-04 with DEL-02-02 (node F or the comparison) | Next comparison | Mapping in the return file |
| U-WR-12 | Draft bases are App-kept, so a draft moved to another machine loses its origin and K-6 refuses its same-name registration | Integrator | Before implementation | The person can re-create the draft with Refine |
| U-WR-13 | Selection pinned rather than following (C-4) | Integrator; owner if a following default is wanted | Before implementation | PROPOSED pin, always visible |
