# S1-B — scoping survey: DEL-01-04 and DEL-01-05

- Run `APP-V4-DESIGN-PASS-3-20261001`, node S1-B. Executor: Type 2 TASK
  (Claude Code subagent, Claude Opus 5.5, high effort; does not delegate),
  dispatched by HELP_HUMAN.
- Brief: [BRIEFS.md](../BRIEFS.md) "Common rules" and "S1 — scoping survey"
  (sha256 `7ac504fb23ca97f3…`); owner direction
  [OWNER_DECISIONS.md](../OWNER_DECISIONS.md) (`ce37656640b824fd…`).
- Deliverables: **DEL-01-04** Native requests, outcomes and attachments;
  **DEL-01-05** Native OAuth/sign-in, API-key and local-provider access.
- Boundary: read-only on project state; read-only git; no network. This is
  the only file written. Paths are relative to
  `projects/chirality-app-v4/execution` unless they start with `docs/`
  (`projects/chirality-app-v4/docs/`) or name the App v3 exemplar
  (`projects/chirality-app-dev/`).
- Two kinds of statement are kept apart. **States:** what a file says, with
  its location. **Inference:** what I conclude. Unlabelled table cells
  summarise what the cited file states.

## 0. What was read, and how

Repository HEAD when read: `bdba4771c4`. `git status --porcelain` was empty
before writing.

| Item | sha256 (first 16) | How used |
|---|---|---|
| Run BRIEFS.md, OWNER_DECISIONS.md, DISPATCH.md; `WorkGraphs/APP-V4-DESIGN-PASS-3-20261001/WORK_GRAPH.md` | `7ac504fb…`, `ce376566…` | Whole |
| Pass-2 `OWNER_DECISIONS.md` (DECISION-K1 K1-1…K1-6, executor-model, model download, host-loop interface, OBS-1/OBS-1b directions) | `b2fa81871cbf44b9` | Whole |
| Pass-2 `DECISIONS_PENDING.md` (K1-4 options; Parts 2–4) and `DECISIONS_DRAFT.md` (choices 2, 3, 11, 17, 18; "already decided"; "where the records disagree") | —, `4b34c24f52a63d59` | Sections named |
| Intake `APP-V4-SWBPIPE-INTAKE-20260928/OWNER_DECISIONS.md` (DECISION-4 D4-3; DECISION-5 scope note) | — | Sections on D4 and D5 |
| DEL-01-04: `ScopeOfWork.md`, `Dependencies.csv`, `_DEPENDENCIES.md`, `_CONTEXT.md`, `_REFERENCES.md` (also `MEMORY.md`, `_STATUS.md`) | `0cdb44e297010b70`, `20ce3808597bf283`, `18cbcd7342c3f06c`, `0143a0d5b5cb0890`, `1c6d5c2a653be294` | Whole |
| DEL-01-05: the same five files | `baf68c79b5b8fdf0`, `3b038c98f97cd685`, `7f9f3f8101ccbdcd`, `9ccd902e890faed0`, `2d29a9c222160cf1` | Whole |
| `_DAG/DAG-003/HANDOFF_STATE.md`; `DependencyEdges.csv`; `CandidateEdges.csv`; `ExcludedRows.csv`; `GRAPH_BASIS.md` (X-1 row) | `56d849b6d078d8d5`, `4716ca287d23835c`, `07b969209e273310` | HANDOFF whole; edge files grepped for both IDs. `MANIFEST.sha256` 37/37 OK from its folder; `SOURCE_MANIFEST.sha256` 130/130 OK from the execution root |
| All 41 live `Dependencies.csv` | — | Parsed by script: every row whose `TargetDeliverableID` is DEL-01-04 or DEL-01-05 from another register |
| `_Decomposition/Open_Issues.csv` | `a11782181531ce77` | Whole |
| Pass-2 closeout `C1-A.md`, `C1-B.md`, `C1-C.md`, `CLOSEOUT_ACCOUNT.md`; `SURVEY/S1-F.md` | `e2cb79e2…`, `c819ba9b…`, `9c4b9a37…`, `703cd4bf…`, `a504772d…` | CLOSEOUT_ACCOUNT, C1-A and S1-F §§1–2, 4–5 whole; C1-B and C1-C by grep for both IDs, OI-009, sign-in and API key, with the surrounding sections read |
| First-increment Design files (`PKG-*/1_Working/DEL-*/Design/*.md`, 20 files) | HOSTING `3cf0381c42358fec`; OBS_1 `7b984b541edca0b1`; PIN_SPIKE `0e090a4ca14e3ec3`; EXEC `64e732d502d0b91d`; RS `b25cc90e9e252f50`; LOOP `f8b7776c82614738` | Counted per file (`grep -c`); every passage naming DEL-01-04 or DEL-01-05 read with its heading. Read as blocks: HOSTING §1, §2, §4.1–§4.5, §6, §7, §8, §8.1, §8.3, §10, §10.1, §11, §12, UNRESOLVED; EXEC §2.4, §2.5.2, §2.7, §5, §9; RS §6.1, §6.2, §10, §10.1; ACT §2.6, §10.1; AS §3.2, §13; LOOP §1, §5.1; OBS_1 §2 and its HOSTING rows |
| `docs/PRD.md`, `docs/ARCHITECTURE.md`, `docs/EXAMINATION.md` | `bb6e786f7a6c01dc`, `317d5789272c5206` | V4-APP-01…04, V4-HOST-01/02, V4-WF-02…05, V4-EXE-01…04, V4-AUT-03…05; ARCH §1 priority 3, §3, §6; V4-EXM-10…12 |
| Spike scratch `…/scratchpad/codex-0.158.0/` (the folder HOSTING names; present in this session's scratchpad) | — | `gen/ts-experimental/run1` and `run1/v2` read for account, attachment, user-input, turn and answer types; client-method and notification lists grepped; five files checked against the committed `generated/0.158.0/MANIFEST.sha256` (Account, LoginAccountParams, ThreadAttachment, ToolRequestUserInputParams, UserInput: all five hashes equal) |
| App v3 exemplar `projects/chirality-app-dev/frontend` | — | `request-card.tsx`, `server-request-answer.ts`, `permission-requests.tsx`, `turn-phase.ts`, `attachment-resolver.ts`, `ui-attachments.ts`, `native-attachments.ts`, `workflow-drafts.ts`, `workflow-draft-review.tsx`, `account-consent-settings.tsx`, `omlx-provider-config.ts`, `hosted-bootstrap/login/start/route.ts` (heads and greps). Evidence only |

`git log` on each deliverable folder: DEL-01-04 has commits through
`877b63b385` (SCA-V4-002 propagation); DEL-01-05 has only `ddd721a90a`
(initialize) and `c1038ae5ac` (first extraction). DEL-01-05's register rows
carry `LastSeen 2026-09-27`; it was not re-extracted in the BASIS-ALIGN or
SCA-V4-002 runs.

---

# Part A — DEL-01-04 Native requests, outcomes and attachments

## A.1 Obligations (25: OUT 4, REQ 7, AC 7, VER 7)

Source keys are the SoW's own (N, R, W, H, C, O, D). "Basis" names the
accepted texts each item rests on; **(am.)** marks a text amended by
SCA-V4-001 or a SoW item revised by SCA-V4-002 (AX-004).

| ID | Obligation (one line) | Basis | Overtaken or lagging |
|---|---|---|---|
| OUT-001 | CODE: native approval/question cards; route grant, deny, answer, explicit decline through the execution owner's interface | V4-APP-01, V4-APP-04; V4-ARC-01/05; V4-EXE-02 | Answer forms at 0.158.0 are per kind and per request (`availableDecisions`); see A.4 O-04-5 |
| OUT-002 | CODE: turn/outcome and attachment presentation with observed standing and supplied-content identity, incl. local attachment/draft transition surface | V4-EXE-03/04; ARCH §3 properties; SOW-129 | — |
| OUT-003 | TEST: request/attachment fixtures incl. outcome, draft-transition and act-attribution cases, tied to supplier and candidate | V4-EXM-10/11; H | Positive act case needs DEP-01-04-019 (a person's act) |
| OUT-004 | DOC: receiving contract for workflow-draft UI (inputs, identity, transitions, request/outcome standing, ownership, open choices, reuse disposition) | V4-WF-02/03; C; D row DEL-02-02 | — |
| REQ-001 | Preserve native approval/question semantics; grant/deny/answer/explicit decline via CLM-003; expose unknown-request errors; silence/time/closing never an answer; no translated vocabulary | V4-EXE-02; V4-APP-04; ARCH §3 | **Lagging (inference):** the generated `ToolRequestUserInputParams` carries `isBlocking` and a deprecated `autoResolutionMs`; a supplier auto-resolution is a supplier act the SoW does not name. HOSTING RT-10 covers it as `resolved-by-supplier` |
| REQ-002 | Turn/outcome shows only observed events; unknown stays unknown; rendered/provider/settlement/write/acknowledgment distinct; primary ≠ descendants; reload renders recovered state from DEL-01-02 | V4-EXE-01…04; V4-EXM-11 | — |
| REQ-003 | Attachment and draft interactions preserve and expose identity of content actually supplied; no same-name substitution; local selection claims no provider adoption | SOW-129; R; W | — |
| REQ-004 | Draft receiving interface carries source-qualified identity and explicit transitions from DEL-02-02; draft until actual registration; collision/refusal without silent overwrite | V4-WF-02/03 | Registration is now act A15 (pass-2 R12-5; ACT §2.6; RS HA-10), recorded through DEL-02-02's registration control. REQ-004 does not name A15 (inference: display of the A15 record is REQ-005's) |
| REQ-005 | Keep execution, acceptance, checking, approval, reliance distinct; "accept" wording; tool permission keeps native semantics; faithful display/recording of performed acts; show lapse | V4-AUT-03…05; V4-HI-30…33; V4-WF-05 (am., phased); CLM-005 (am.) | **Overtaken in part:** DECISION-K1 K1-1 (the agent asks; the product offers the means and records), K1-2 (earlier act counts; cited with time), K1-3 (joint answer after partial lapse), K1-4 (person identity "identity not verified"). None is in the SoW. The App act control itself is absent (SC2-01-04-1, collected) |
| REQ-006 | Perform no act owned by DEL-01-01/01-02/01-03/02-02/04-01/04-03, Owner, host, person | D; H; O | If the act control is added, REQ-006 should say the control produces a record through DEL-04-03's format, not DEL-04-03's act (inference) |
| REQ-007 | Required interactions independent of optional legacy reuse; reuse checks; TBD-001…005 kept at owner/point of need; no claimed pin/input/component | C; O | TBD-001/002/004 revised under SCA-V4-002 (am.); TBD-004 still names the implementation/qualification pin open |
| AC-001 | Candidate renders native requests; actual meanings; unknown errors explicit; silence/closure not a response | REQ-001 | As REQ-001 |
| AC-002 | Outcome and recovered-view cases distinguish observation, settlement, acknowledgment, unknown, descendants | REQ-002 | — |
| AC-003 | Attachment/draft cases preserve identity, detect substitution, no adoption claim | REQ-003 | — |
| AC-004 | Draft contract preserves source-qualified identity; draft vs registration; collision/refusal carried | REQ-004 | As REQ-004 (A15) |
| AC-005 | Act-presentation cases: separate acts, "accept", faithful display with actor ≠ recorder, lapse, fabrication negatives | REQ-005 | As REQ-005 |
| AC-006 | Receiving contract assigns every excluded act; local contribution; reuse; open pairs retained | REQ-006, REQ-007 | — |
| AC-007 | Fixture artifact covers AC-001…005, names candidate and supplier basis, reports limits | OUT-003 | — |
| VER-001 | Exercise grant/deny/answer/decline/unknown error/silence/closure on candidate; attempt ≠ acknowledgment | AC-001 | Live supplier behaviour for error replies and never-answered requests is not observed (PIN_SPIKE P-08) |
| VER-002 | Drive presentation with outcomes, unknowns, outstanding requests, missing acknowledgment, reload, active descendant | AC-002 | — |
| VER-003 | Follow attachment/draft content through selection, handoff, rendered reference; changed and same-named content | AC-003 | "No hash algorithm prescribed" stays consistent with RS U-04 |
| VER-004 | Inspect receiving document and transitions against DEL-02-02 evidence | AC-004 | DEL-02-02 has no Design file (later undertaking until this pass) |
| VER-005 | Compare labels against PKG-04; positive faithful recording, lapse, negatives; D2/D3 as adopted (am.) | AC-005 | Positive case requires a construction (the act control) the SoW does not oblige |
| VER-006 | Review receiving document against D, C, H, O; trace exclusions | AC-006 | — |
| VER-007 | Run fixture suite against candidate; report simulated vs observed | AC-007 | — |

## A.2 Joins

Arc direction is consumer → supplier. Layer from DAG-003 (`DependencyEdges.csv`
= admitted; `CandidateEdges.csv` = held; `ExcludedRows.csv` = MIRROR /
NOT_TOPOLOGICAL).

### A.2.1 ACTIVE rows in DEL-01-04's register (18)

| Row | Direction / type | Other end | Arc and layer |
|---|---|---|---|
| DEP-01-04-001…006 | ANCHOR | PKG-01; SOW-005, SOW-014, SOW-129; OBJ-001, OBJ-002 | Not arcs |
| DEP-01-04-007 | UPSTREAM PREREQUISITE | DEL-01-01 (hosting boundary, identity, types, qualification) | DEL-01-04 → DEL-01-01, **admitted** (representative) |
| DEP-01-04-008 | UPSTREAM INTERFACE | DEL-01-02 (session/request interface, recovered state) | DEL-01-04 → DEL-01-02, **admitted** (representative) |
| DEP-01-04-009 | UPSTREAM INTERFACE | DEL-02-02 (draft identity and transitions) | DEL-01-04 → DEL-02-02, **held** SCC-002 |
| DEP-01-04-010 | DOWNSTREAM HANDOVER | DEL-02-02 (native attachment/draft interactions) | DEL-02-02 → DEL-01-04, **held** SCC-002; MIRROR of DEP-02-02-013 |
| DEP-01-04-011 | UPSTREAM INTERFACE | DEL-04-01 (adopted policy and act distinctions) | DEL-01-04 → DEL-04-01, **admitted** |
| DEP-01-04-012 | UPSTREAM INTERFACE | DEL-04-03 (act/run record, lapse standing) | DEL-01-04 → DEL-04-03, **held** SCC-002 |
| DEP-01-04-013 | CONSTRAINT EXTERNAL | OI-001 residue (OI-021 additions) | NOT_TOPOLOGICAL |
| DEP-01-04-015…017 | CONSTRAINT EXTERNAL | OI-008, OI-012 (implementation/qualification pin), OI-014 | NOT_TOPOLOGICAL |
| DEP-01-04-018 | PREREQUISITE EXTERNAL | DEP-005 suppliers | NOT_TOPOLOGICAL |
| DEP-01-04-019 | PREREQUISITE EXTERNAL | Person performing the positive act case, and a separate recorder | NOT_TOPOLOGICAL |

DEP-01-04-014 (OI-002) is RETIRED (successor DEP-01-04-011).

### A.2.2 ACTIVE rows in other registers naming DEL-01-04 (5)

| Row | Register | Contribution | Arc and layer |
|---|---|---|---|
| DEP-01-01-021 | DEL-01-01, DOWNSTREAM HANDOVER | Stock supplier boundary | MIRROR of DEP-01-04-007 (admitted) |
| DEP-01-02-019 | DEL-01-02, DOWNSTREAM INTERFACE | State/request interfaces, observed events, unknown outcomes | MIRROR of DEP-01-04-008 (admitted) |
| DEP-02-02-013 | DEL-02-02, UPSTREAM INTERFACE | Native requests, outcomes, attachments, draft-UI receiving interface | DEL-02-02 → DEL-01-04, **held** SCC-002 (representative) |
| DEP-02-03-027 | DEL-02-03, UPSTREAM INTERFACE | "App act control and person identity", for the App-side positive capture fixtures only | **X-1**, held SCC-002, **narrow** (HANDOFF standing note) |
| DEP-09-02-012 | DEL-09-02, UPSTREAM PREREQUISITE | Native interaction view and scoped request/outcome checks before the joined request witness | DEL-09-02 → DEL-01-04, **admitted** |

No row in DEL-04-01's or DEL-04-03's register names DEL-01-04 (C1-A lists
both as "outside mirrors noted, not proposed").

### A.2.3 What first-increment Design files assume of DEL-01-04 (states)

DEL-01-04 occurs in HOSTING (18 lines), EXEC (18), ACT (8), RS (8), CA (7),
GUIDE (6), EXAMPLES (5), WD (4), PIN_SPIKE (1), ADAPTER (1).

**DEL-01-01 (HOSTING-v0.8; arc admitted, DEP-01-04-007):**

- §1 diagram: the register interface receives "A14 answers via DEL-01-04".
- §6.1 settlement origin `person-via-interaction` — "A14 by the person,
  actor supplied by DEL-01-04".
- §6.4: DEL-01-04 is a caller of *observe entries*, *list outstanding* and
  *answer* "(person path, any valid form)".
- R7: affirmative A14 answers come "only from the person through DEL-01-04
  … or from the user's own Codex mode"; no App rule answers A14
  affirmatively. R9: person-input kinds are answered with content "only by
  the person via DEL-01-04"; such answers "are not act evidence"; "the App
  may answer it by presenting its own act control (EXEC CAP-2), which
  settles no pending supplier request".
- R5: answer content must be valid for the method; "A request may offer
  fewer" forms (OB-5: under `untrusted`, `accept`,
  `acceptWithExecpolicyAmendment`, `cancel` only).
- §8 S-3 seam: supplied "Register operations; refusal reasons incl.
  `origin-not-permitted`; settlement; supplier-internal decision
  notifications (§6.6)"; not supplied "Request cards, answer UX,
  attachments, outcome presentation". §6.6: receivers present a
  supplier-internal decision with origin `supplier-internal`, never as the
  person's answer.
- H9: settings carried "through the owning interface (DEL-01-05 for
  settings; DEL-01-04 for answers)".
- U-20: the 0.158.0 request-kind partition is a "PROPOSAL for the App
  implementation owner with DEL-01-04/01-05". U-26: refusal order is the App
  implementation owner's "with DEL-01-04 (answer path)". §11 row: request
  cards, answers, outcomes, attachments are DEL-01-04's.
- §6.5/F-15: seams S-1…S-4 have "no receiving comparison" yet.

**DEL-02-03 (EXEC-v0.6; arc X-1 held, DEP-02-03-027):**

- §5 CAP-1…CAP-9: scope App content (and A12 where an App control
  establishes the setting); CAP-2 dedicated control, one act kind at a time,
  showing kind with R-4 wording, bound subject with content identity, scope,
  purpose, actor requirement, arrival; offers the decline; CAP-3
  direct-capture record with capture-evidence reference {act identity,
  actor, kind, bound content identity with method, scope, purpose, time,
  surface "App interface", arrival reference}; CAP-4 "No agent tool, MCP
  operation, App rule or supplier request can operate the control or produce
  its record"; CAP-5…CAP-7 not evidence (A14, user-input/elicitation
  answers, conversation); CAP-8 identity per K1-4; CAP-9 presenting is not
  answering. "Construction of the control is DEL-01-04's".
- RC-6: the control is "a standing facility, available whether or not an
  arrival was recorded … An arrival changes neither facility."
- **§2.4.4: "The display is built by the App's interface owner (DEL-01-04,
  later)"** — SD-1…SD-5 (checkpoint list, per-arrival labels with person
  "identity not verified", where the act is performed, what is never shown,
  "continued past" as information). SD-4: never a prompt, dialog or
  notification raised by an arrival.
- §2.5.2 AE-2 "AWAITING INPUT (DEL-01-04's control)"; CH-23 (ii), CH-31
  (ii), CH-32 positive capture AWAITING INPUT; §9.1 row: contribution "named
  by DEP-02-03-027 and not yet defined by the supplier".
- §10: "App act control construction | DEL-01-04 (later, D1)".

**DEL-04-01 (ACT-POLICY-v0.8; arc admitted, DEP-01-04-011):** §2.6 "A4, A6,
A7 on App content | The App interface's act control (EXEC CAP-1…CAP-3). The
control is built by DEL-01-04"; §10.1 values carried to DEL-01-04: V-01
(A1–A15, record kinds, act-declined/run-ended events, lifecycle), V-05
(outcome map), V-07 (label rules §9), V-08 (no professional standing from
agent output), V-21 (P-04 routine tool permission); §10.3 row DEP-01-04-011.

**DEL-04-03 (RS-v0.8; arc held, DEP-01-04-012):** §6.1 *Decision actor* per
K1-4, *Evidence limits* "identity not verified"; capture evidence "App
interface per EXEC CAP-1…CAP-9"; §10 row: DEL-01-04 takes "R3/R4/R7/R13; act
display" and supplies "App capture control"; §10.1: "the act control's
construction stays with DEL-01-04, and its obligation is proposed for
DEL-01-04's contract".

**Others:** WD U-25 (closed as a decision; construction DEL-01-04), VC-53/54
App capture AWAITING INPUT; EXAMPLES E1e (App act control "which DEL-01-04
builds later"); GUIDE M5.3 and G-1 ("DEL-01-04's ScopeOfWork does not name
the act control"); CA §5 allocation row, CAF-30 ("The App act control does
not exist yet"), W14-03 "Not run: display to the person (DEL-01-04)",
W14-05; ADAPTER §1 row (DEL-01-01 "with DEL-01-04/01-05 in a later
undertaking"); PIN_SPIKE receivers (answer forms via DEP-01-01-021).

**AS-v0.8 (DEL-04-02; no register join with DEL-01-04):** §13 K-5
"Checkpoint overlay" and K-6 "Standing facets" with options CS-1…CS-4,
"none chosen"; CS-3 "The App builds K-1…K-7 for App surfaces". Inference:
this overlaps EXEC §2.4.4's assignment of the App's checkpoint display to
DEL-01-04 (see D.3).

## A.3 Proposed contract changes already collected

| ID | Source | What | Status |
|---|---|---|---|
| **SC2-01-04-1** | C1-A (kept); duplicate C1-B X-1 dropped (CLOSEOUT_ACCOUNT) | New REQ (and matching OUT, AC, VER) in DEL-01-04's SoW: the App act control — dedicated, person-only (no agent tool, MCP operation, App rule or supplier request can operate it or produce its record), one act kind at a time on App content (and A12 where an App control establishes the setting); shows kind (canonical wording), bound subject and content identity, scope, purpose, actor requirement, arrival; offers the decline; produces a direct-capture record with capture-evidence reference in DEL-04-03's format; standing facility, no arrival raises it; records identity per K1-4 marked *identity not verified*; presenting it answers no supplier request. Consumers DEL-02-03, DEL-04-03, DEL-04-01. "Process placement that makes 'not operable by automation' true stays with OI-008" | Proposed for SCA-V4-003 (K1-4) |
| R2-01-04-a | C1-A | DEL-01-04 DOWNSTREAM HANDOVER → DEL-02-03, mirror of DEP-02-03-027 (X-1) | Proposed, mirror only |
| SC2-02-03-5 / R2-02-03-j | C1-A (DEL-02-03 side) | DEL-02-03 CLM-002 and DEP-02-03-027: "App act control and person identity" → "App act control, which records the person's identity as DECISION-K1 K1-4 sets it" | Proposed |
| SC2-04-03-1 | C1-A (DEL-04-03 side) | DEL-04-03 REQ-005 names DEL-01-04 among consumers "in their own registers" | Proposed |
| "Outside mirrors noted, not proposed (D1)" | C1-A | DEL-04-01 → DEL-01-04 and DEL-04-03 → DEL-01-04 DOWNSTREAM mirrors | Not proposed; now in reach of this pass |

**Inference (not collected anywhere):** EXEC §2.4.4 assigns the App's
checkpoint display (SD-1…SD-5) to DEL-01-04, and ACT V-07 assigns label
rules to it; DEL-01-04 REQ-005 covers act presentation generally but names
neither the checkpoint display nor A15 display. If the design pass keeps
that assignment, a matching SoW sentence would belong in SCA-V4-003 beside
SC2-01-04-1.

## A.4 Open items and owner choices

"Shapes" = the design text differs by answer.

| # | Item | Owner / point of need (as stated) | Shapes the design now? | Options (as files state; inference marked) |
|---|---|---|---|---|
| O-04-1 | **OI-008** App process division | App implementation owner; before architecture production contracts (TBD-003; HOSTING U-02, §12 proposal O-1 "Recommended") | **Yes.** CAP-4 ("not operable by automation") depends on where capture is produced; the answer path (webview → main-process register) and refusal handling follow from it | HOSTING O-1 (Rust envelope core; TS composes and presents) / O-2 (Rust fully typed); O-3, O-4 set aside. Inference: under O-1 the act control's record must still be produced or sealed in the main process so a webview script cannot forge it — a sub-choice the files do not state. **Owner-level per DECISIONS_DRAFT choice 17** (left for the phase review) |
| O-04-2 | Act control in this pass ahead of its contract | Owner (K1-4 said no design in pass 2; pass-3 direction lists "the act control") | **Yes** | (a) design it now in DEL-01-04's Design, labelled PROPOSED until SCA-V4-003 carries SC2-01-04-1; (b) wait for the amendment. Inference: the owner's pass-3 direction already selects design; the label is the remaining point |
| O-04-3 | **OI-014** shared component placement | App/shared contract owners; before structural/production allocation (TBD-005) | **Yes, for display ownership.** Who builds the App's checkpoint overlay and standing facets: DEL-01-04 (EXEC §2.4.4) or DEL-04-02 components (AS §13 K-5/K-6, CS-1…CS-4) | Files offer CS-1…CS-4 for AS; EXEC does not consider AS's K-5. Inference: decide which deliverable's Design defines App-side display behaviour; placement of code can stay open |
| O-04-4 | Person identity "name set in the App" | Owner decided the scheme (K1-4) | **Yes, small.** No file says which deliverable offers the setting where the person sets the name, or how the Codex account is read | Inference: DEL-01-05 (account surfaces; `account/read` returns `{type: "chatgpt", email}` or `{type: "apiKey"}` with no identity) or DEL-01-04. Integrator can assign |
| O-04-5 | Explicit decline per request kind | HOSTING U-20 (App implementation owner with DEL-01-04/01-05) | **Yes.** REQ-001's "explicit decline" has no native form for `item/tool/requestUserInput` (answers map only) or `item/permissions/requestApproval` (grant profile + scope); under `untrusted` a command approval offered no `decline`, only `cancel` (OB-5) | Options (inference): explicit JSON-RPC error by named rule (R2/R9 permit decline/error); an empty grant for permissions; offering only what the request offers and labelling `cancel` natively. Error-reply effect is not observed (P-08) |
| O-04-6 | Supplier auto-resolution of questions | Not in any file | **Yes, small.** Generated `ToolRequestUserInputParams` has `isBlocking` and deprecated `autoResolutionMs` (scratch TS, manifest-matched) | Present as `resolved-by-supplier` (HOSTING RT-10) with cause as reported, never as answered; behaviour not observed |
| O-04-7 | **OI-012** implementation/qualification pin | App implementation owner; before protocol generation and qualification (TBD-004) | No (design at 0.158.0) | — |
| O-04-8 | **OI-001** residue / **OI-021** operation-specific additions | Owner with App/SWB contract owners; before operation-policy production contracts | No (labels come from ACT V-07; additions fill slots) | — |
| O-04-9 | DEL-01-02 split (HOSTING F-01/U-14) and recovered-state interface | DEL-01-02 with DEL-01-01 (S1-A's) | **Yes, at the seam.** REQ-002's reload/recovery rendering consumes DEL-01-02's interface | Coordinate with S1-A's DEL-01-02 scope |
| O-04-10 | DEL-02-02 draft transitions and A15 | DEL-02-02 (S1-C's); R12-5 made registration A15 | **Yes, at the seam** | Coordinate with S1-C |
| O-04-11 | Attachment content identity and provider adoption | Content-identity algorithm is RS U-04 / HOSTING U-08 | **Yes.** At 0.158.0 `UserInput` passes files by path (`localImage`, `mention`, `skill`) or by `image` URL/`fileId`; the supplier reads paths itself, so the bytes it read are not observable from the App. `thread/attachment/add|list|remove` (stable) persists `{attachmentType, identityKey, payload}`; semantics not observed | Inference: identity is taken at the local interface at submission; "provider adoption not observed" is the default label (REQ-003 expects this). Algorithm stays RS's |
| O-04-12 | DEP-01-04-019: a person's act for the positive VER-005 case | Not assigned | No (verification input) | — |

**Owner flags:** O-04-1 (OI-008, phase-review item); O-04-2 (label only,
probably settled by the pass-3 direction); O-04-3 (OI-014, phase-review
item, if the owner wants to settle display ownership). The others are
integrator or App-implementation-owner items.

## A.5 What exists to build on

**Supplier facts (DEL-01-01).**

- HOSTING §6 register: entry elements, classification, states, RT-01…RT-13
  transition table, R1–R9, refusal reasons and order (U-26), §6.4
  operations, §6.6 supplier-internal decisions; PROPOSED schema
  `hosting.server-request-entry.schema.json`; supplier double and boundary
  model `prototype/` (§9.6). This is the request card's data source almost
  entirely.
- PIN_SPIKE P-08 answer forms for every kind; §4 inventory (11
  server-request kinds, 85 notifications).
- OBS-1/OBS-1b: OB-3 order (`item/started` before the approval request),
  OB-4 `serverRequest/resolved` 8 ms after a written reply, OB-5
  `availableDecisions` restricted and arriving without the opt-in.
- Generated types (scratch, manifest-matched): `TurnStatus` =
  `completed | interrupted | failed | inProgress`; `Turn.error` only when
  failed; `turn/completed`, `thread/status/changed`, `error`, `warning`,
  `serverRequest/resolved`; `CommandExecutionApprovalDecision` (accept,
  acceptForSession, two amendment forms, decline, cancel);
  `FileChangeApprovalDecision`; `McpServerElicitationAction`
  (accept/decline/cancel); `ToolRequestUserInputQuestion` with `isSecret`
  and `isOther`; `UserInput` forms; `thread/attachment/*`.

**First-increment consumers already define the receiving side:** EXEC §5
(nine capture rules), §2.4.4 (display meanings), RC-5/RC-6; RS §6.1 record
elements, HA-1…HA-10, §7 lapse rule, format 0.1 schema; ACT V-07 label
rules, §2.6 capturing surfaces; AS §3, §4, §9 display rules.

**App v3 exemplar (evidence only).**

- `request-card.tsx` / `server-request-answer.ts`: cards for approval,
  user-input and elicitation; answers translated to `{kind: 'approval',
  verdict: 'allow'|'deny'|'allowForSession'}` (a Chirality vocabulary that
  REQ-001 and V4-APP-04 now exclude); user input requires every question
  answered and offers no decline; `acceptForSession` offered only when
  `availableDecisions` contains it.
- `turn-phase.ts`: phases `idle | preparing | working | waiting |
  reconnecting | stopping`; outcomes `completed | interrupted | failed |
  unknown`, "a turn the log cannot settle ends as unknown" — close to
  REQ-002.
- Attachments: path-based picker restricted to project root and nine
  extensions, 10 MiB/18 MiB limits; no content hashing found (`grep` for
  hash/sha/digest/identity returned nothing).
- Drafts: `WorkflowDraft` carries `reviewToken`, per-file `sha256` and size,
  `destinationExists`; registration posts the `reviewToken` — evidence of a
  content-bound draft/registration handshake.

## A.6 Design scope for this pass (to reach the LOOP_INIT 60% description)

1. **`Design/NATIVE_INTERACTION_RECEIVING.md`** (OUT-004, with OUT-001/002
   behaviour):
   - parties and seams: S-3 (HOSTING §6.4) consumed, DEL-01-02 recovered
     state, DEL-02-02 draft transitions, DEL-04-01 values V-01/05/07/08/21,
     DEL-04-03 records; each with the failure behaviour of the exchange;
   - a request-card model per 0.158.0 kind: the native answer forms the
     request offers, origin rules (R7/R9), the explicit-decline mapping
     (O-04-5), secret questions, non-blocking questions and supplier
     resolution (O-04-6), unfamiliar and app-unsupported kinds shown as
     explicit errors;
   - card states mapped one-to-one onto register states RT-01…RT-13, with
     display labels that keep write attempt, written, acknowledgment
     observed, resolved by supplier and ended-unanswered apart;
   - turn/outcome states (supplier `TurnStatus` plus *unknown* from
     observation loss), descendant display rule, reload/reopen sequence;
   - attachment and draft content identity: what is carried at the local
     interface, "provider adoption not observed", substitution detection;
   - draft receiving transitions (draft, changed draft, registered (A15
     record), collision, refusal);
   - act presentation rules (REQ-005) using ACT V-07 and RS §6.1, including
     K1-2/K1-3 citations and lapse;
   - optional-reuse disposition against the v3 files in A.5;
   - verification cases for VER-001…007 and fixture inputs; what needs a
     candidate.
2. **`Design/APP_ACT_CONTROL.md`** (or a section of 1), labelled PROPOSED
   pending SCA-V4-003: accept or amend CAP-1…CAP-9; inputs and outputs
   (direct-capture record, act-declined event); states (offered, operated,
   declined, record write failed); identity elements and their sources
   (K1-4); the placement requirement CAP-4 sets for OI-008, stated as a
   requirement, not a choice; standing facility (RC-6), never raised by an
   arrival (K1-1, SD-4).
3. **Schemas and a local prototype**: PROPOSED card/answer and act-control
   record-input schemas; a card-state walk against HOSTING's supplier double
   and RS's schema (no candidate).
4. **Receivers table** for the five incoming rows and the outside mirrors,
   and a findings list of SoW lags (A.1, A.3) for SCA-V4-003.

**Leave out:** visual layout and component styling (no requirement asks);
Rust/TS allocation (OI-008) and shared placement (OI-014) beyond stating
requirements; DEL-01-02's custody and persistence; DEL-01-03's plan, tool
and delegation views; DEL-02-02's workspace journey; candidate fixtures,
qualification and any live supplier turn (no authority in this brief).

---

# Part B — DEL-01-05 Native OAuth/sign-in, API-key and local-provider access

## B.1 Obligations (33: OUT 4, REQ 9, AC 10, VER 10)

DEL-01-05's SoW was revised by neither amendment (git log; S1-F §4.2). Its
sources: S2 (Deliverables, ScopeLedger SOW-009…012, 132, 133, 149, 150), S3
(original seed V4-APP-02, V4-ARC-04, ARCH §§3, 4, 6), S4 (OI-009, OI-010,
OI-012; DEP-001, DEP-005), S5 (current PRD §§0, 2.1; ARCH §§3, 6).

| ID | Obligation (one line) | Basis | Overtaken or lagging |
|---|---|---|---|
| OUT-001 | CODE: App receiving for native ChatGPT sign-in/OAuth and API-key access through Codex account methods; Codex credential custody | V4-APP-02; V4-ARC-04 | — |
| OUT-002 | Local-provider settings; account/provider selection; modes kept together; per-conversation choice | V4-APP-02; V4-ARC-04 (`modelProvider` on `thread/start`) | See REQ-004 |
| OUT-003 | Account-home and API-key definition records; open decisions retained | ARCH §3 "Left to the implementation session"; OI-009, OI-010 | — |
| OUT-004 | Candidate-bound qualification, substitution config and checks; capability requirements for DEL-05-01 | ARCH §6; SOW-149/150 | OBS-1/1b add one dated route observation (not qualification) |
| REQ-001 | Offer ChatGPT sign-in/OAuth via the Codex flow; start an account-backed conversation; Codex holds credentials | V4-APP-02 | At 0.158.0 `account/login/start` `chatgpt` returns an `authUrl` for the browser and `chatgptDeviceCode` a code; `account/login/completed` reports the result (generated types) |
| REQ-002 | Offer API-key access via Codex account methods per REQ-006 | V4-APP-02 | At 0.158.0 `{type: "apiKey", apiKey}` passes the key through the App to Codex; inference: the App holds key bytes transiently, so "held by Codex" needs a no-retention rule |
| REQ-003 | Offer supported local servers as Codex providers at the chosen pin | V4-ARC-04; ARCH §6 | Provider definition is not in the generated types (P-11); OBS-1 used `config.toml` `[model_providers.*]` with `wire_api = "responses"` |
| REQ-004 | Keep account, API-key and local configured together; select per conversation; selecting one preserves the others | V4-APP-02; V4-EXM-12 ("switches between them") | **Lagging (inference):** `account/read` returns one `Account` (`apiKey` · `chatgpt` · `amazonBedrock`) per Codex home; whether a ChatGPT sign-in and an API key can coexist in one home and be chosen per thread is not observed. **No default:** DECISION-4 D4-3 / V4-HOST-01 (am.) states "no default" for a **host's** agent; V4-APP-02 states per-conversation choice and no default rule (A.4/B.4 O-05-3) |
| REQ-005 | Account-home record presents separated/shared state and records the Owner + App implementation owner's choice before account integration; OI-009 explicit until then | SOW-132; OI-009 | Still open; Part 3 of pass-2 DECISIONS_PENDING put it to the phase review |
| REQ-006 | App implementation owner defines supported API-key behaviour against the pinned protocol before dependent work; OI-010 explicit | SOW-133; OI-010 | **Lagging:** TBD-003 says "the unidentified supplier pin"; D4 selected 0.158.0 for definition/generation (OI-012 consequence column) |
| REQ-007 | Qualify account/provider and local-server interfaces against the pin; compliant server substitutable; identify candidate, server, interface, result | SOW-149/150; DEP-005 | OBS-1/1b observed L-2 and a flat-function L-3 at one pair; MCP tools dropped on that route (F-31) |
| REQ-008 | Hand capability requirements and limits to DEL-05-01, distinguishing App Codex-provider interface from host model/loop interface | SOW-149; CLM-004; V4-ARC-10 (unchanged, owner's host-loop interface decision) | DEL-05-01 has no consuming row and LOOP §10.3 says "not consumed by this file" |
| REQ-009 | No act of DEL-01-01, DEL-05-01 or the host owner | S2, S4 | — |
| AC-001 | Candidate completes native sign-in, starts account-backed conversation, Codex custody | REQ-001 | Needs the person's own sign-in |
| AC-002 | Candidate API-key flow per definition, Codex custody | REQ-002, REQ-006 | Needs the person's key |
| AC-003 | Configured local server starts a provider conversation; pin and interface identified | REQ-003 | — |
| AC-004 | All three configured; each selectable and started; others preserved | REQ-004 | As REQ-004 |
| AC-005 | Account-home record shows alternatives, choice, participants, timing | REQ-005 | — |
| AC-006 | API-key definition with pinned evidence before dependent work | REQ-006 | — |
| AC-007 | Qualification links DEL-01-01 embedding input; observed outcomes and limits | REQ-007 | — |
| AC-008 | Compliant replacement server substituted and started | REQ-007 | — |
| AC-009 | Handoff to DEL-05-01 with interface distinctions and limits; no host conformance claimed | REQ-008 | — |
| AC-010 | Boundary assigns REQ-009 acts | REQ-009 | — |
| VER-001 | Exercise sign-in on candidate; no credential reproduced | AC-001 | Person-performed |
| VER-002 | Exercise API-key flow; no key reproduced | AC-002 | Person-performed |
| VER-003 | Configure a local server and start; record endpoint/model identity | AC-003 | — |
| VER-004 | Per-conversation selection scenario with all three configured | AC-004 | — |
| VER-005 | Review account-home record against SOW-132/OI-009 | AC-005 | — |
| VER-006 | Review API-key definition against pin and OI-010 | AC-006 | — |
| VER-007 | Compare qualification record, exchanges and DEL-01-01 input | AC-007 | — |
| VER-008 | Check and substitute a replacement server | AC-008 | — |
| VER-009 | Review handoff to DEL-05-01 | AC-009 | — |
| VER-010 | Compare REQ-009 acts with owners | AC-010 | — |

Not in the SoW but bearing on it: K1-4 names "the Codex account when Codex
reports one" as an identity source (an account-surface read); the
supplier's start-up traffic (HOSTING U-18, "Owner with DEL-01-05"); OI-007
distributed sign-in terms, which belong to DEL-01-06 (its TBD-002), not
here.

## B.2 Joins

### B.2.1 ACTIVE rows in DEL-01-05's register (16)

| Row | Direction / type | Other end | Arc and layer |
|---|---|---|---|
| DEP-01-05-001…011 | ANCHOR | PKG-01; SOW-009…012, 132, 133, 149, 150; OBJ-002, OBJ-004 | Not arcs |
| DEP-01-05-012 | UPSTREAM PREREQUISITE | DEL-01-01 (selected protocol/pin) | DEL-01-05 → DEL-01-01, **held** SCC-001 (representative) |
| DEP-01-05-013 | UPSTREAM PREREQUISITE | DEL-01-01 (embedding-qualification input) | SAME_ARC as 012 |
| DEP-01-05-014 | DOWNSTREAM HANDOVER | DEL-05-01 (capability requirements and limits) | DEL-05-01 → DEL-01-05, **admitted** (representative; supplier-side row only) |
| DEP-01-05-015 | CONSTRAINT DOCUMENT | OI-009 account-home record | NOT_TOPOLOGICAL |
| DEP-01-05-016 | CONSTRAINT DOCUMENT | OI-010 API-key definition | NOT_TOPOLOGICAL |

### B.2.2 ACTIVE rows in other registers naming DEL-01-05 (3)

| Row | Register | Contribution | Arc and layer |
|---|---|---|---|
| DEP-01-01-022 | DEL-01-01, DOWNSTREAM HANDOVER | Embedding-protocol qualification and local-provider protocol requirement account | MIRROR of DEP-01-05-012 (held, SCC-001) |
| DEP-01-01-024 | DEL-01-01, UPSTREAM INTERFACE | Native sign-in and server-substitution evidence "when needed" for DEL-01-01's qualification witness; "not an unconditional prerequisite" | DEL-01-01 → DEL-01-05, **held** SCC-001; no counterpart in DEL-01-05's register (C1-B, verified) |
| DEP-09-02-013 | DEL-09-02, UPSTREAM PREREQUISITE | Account/provider inputs and focused sign-in/concurrent-mode checks before V4-EXM-12 | DEL-09-02 → DEL-01-05, **admitted** |

SCC-001 = {DEL-01-01, DEL-01-05} (SCC-CASE-001; R2 candidate remedy: a
narrow objective-scoped cut of DEP-01-01-024).

### B.2.3 What first-increment Design files assume of DEL-01-05 (states)

DEL-01-05 occurs in HOSTING (29 lines), PIN_SPIKE (5), ADAPTER (1), LOOP (1);
nowhere else.

**DEL-01-01 (HOSTING-v0.8):**

- §4.2 step 3: "The account-home/environment element is
  `UNRESOLVED{OI-009}` (DEL-01-05 owns the choice's integration). On a fresh
  home the supplier performs a network fetch at start (§8.1 L-4, U-18)."
- §7.2: "Which home the label probe uses (the account home or a separate
  probe home) is part of U-03/OI-009."
- H9: settings carried "through the owning interface (DEL-01-05 for
  settings …)"; "The account-home element remains `UNRESOLVED{OI-009}`."
- §8 S-4: supplied "Carriage of supplier account methods and
  per-conversation provider selection (`modelProvider` on thread start and
  resume; `modelProvider/capabilities/read`); observed model destination per
  thread/turn; §8.1 account; recorded-exchange evidence; the fresh-home
  network observation"; not supplied "Sign-in (including OAuth) and API-key
  flows, offered as options with no default between local and cloud
  (DECISION-4 D4-3; R8-9); account home (OI-009), provider configuration,
  server-substitution checks".
- §8.1 L-1…L-6 requirement account "to DEL-01-05": L-2 observed at one pair
  (Responses to LM Studio 0.4.16); L-3 flat function tool called, MCP tools
  not delivered (F-31); L-4 start-up traffic (chatgpt.com remote control and
  featured plugins 401; github.com plugin sync; analytics off does not stop
  it); L-5 "login variants incl. API key and ChatGPT account sign-in;
  credential store modes `file`/`keyring`/`auto`/`ephemeral` … This boundary
  selects no default … Whether the supplier's sign-in variant serves D4-3's
  OAuth option for a given cloud provider is not-observed. Which flows the
  App offers is DEL-01-05's (S-4)"; L-6 each interface qualified separately.
- §8.3: requested provider and model "carried from the person's choice
  through DEL-01-05"; "The destination **class** (local or cloud) is derived
  from the provider configuration the person chose (DEL-01-05)".
- §6.1 partition: `account/chatgptAuthTokens/refresh` "known-app-unsupported
  unless DEL-01-05 adopts external-token login"; U-20 "with DEL-01-04/01-05".
- §11 row: sign-in, API key, local provider, "options the person chooses
  among, no default: DECISION-4 D4-3", substitution checks are DEL-01-05's;
  "any sign-in, which is the person's own".
- U-03 (OI-009; "Owner with App implementation owner (DEL-01-05)"), U-18
  ("Owner with DEL-01-05"), U-22 (L-2/L-3; DEL-01-05), F-14 ("a separate App
  account home would be 'fresh' at least once per home"), F-24, F-31, F-32
  ("which carrier the App uses for the person's setting is DEL-01-05's").
- §1 Reading: the boundary carries; it does not choose (H9, D3).

**PIN_SPIKE:** P-11, P-12 (account methods "feeds OI-009/OI-010 at
DEL-01-05"); S-F-10 and S-F-17 routed to "the owner and DEL-01-05".

**OBS_1:** §2 configuration (`CODEX_HOME` copy; `model_providers.obs1_lmstudio`;
`wire_api = "responses"`); OB-5 `approval_policy = "untrusted"` refused in
`config.toml`, accepted on `thread/start`; OB-9 start-up traffic without
sign-in; OB-11 time zone in model context, "for … DEL-01-05; recorded, not
decided".

**DEL-05-01 (LOOP-v0.8; arc admitted, DEP-01-05-014):** §10.3 "Local-server
capability requirements … DEL-01-05 … Not supplied, and not consumed by this
file". §1: App credentials "Held by Codex (V4-ARC-04)"; App model interface
is Codex's protocol with an "unobserved" Responses assumption; "A local
server that serves both interfaces does not join them". §5.1 NW-1…NW-7 and
F-2 (no model selected → run not started) govern **the host loop only**.

**DEL-03-03 (ADAPTER):** §1 row "App DEL-01-01 (with DEL-01-04/01-05 in a
later undertaking)"; OC-3 configuration locus (user's Codex config,
per-thread `config`, plugin, none).

## B.3 Proposed contract changes already collected

| ID | Source | What | Status |
|---|---|---|---|
| R-11-3 | C1-B | DEP-01-01-022 Notes: the requirement account now carries the observed route limit (F-31, "routed to DEL-01-05") and the approval-setting carrier quirk (F-32) | Proposed (DEL-01-01 register) |
| R-0501-4 | C1-C | DEL-05-01 UPSTREAM INTERFACE → DEL-01-05, a declared mirror of DEP-01-05-014; **alternative:** record why no consumer row is kept (LOOP §10.3) | Proposed |
| (observation) | C1-B §5.5 | DEP-01-01-024 has no counterpart in DEL-01-05's register | Noted, not proposed |
| B-1 | C1-B §7 | Basis item: no accepted text decides the App supplier's own start-up traffic (U-18) | Owner, phase review |
| S1-F §4.2 | pass-2 survey | DEL-01-05's SoW lags D4 (TBD-003 "unidentified supplier pin") | Inference only; no wording collected |

No ScopeOfWork item for DEL-01-05 was collected in pass 2. **Inference —
candidates for SCA-V4-003 from this survey:** TBD-003 re-pinned to D4's
0.158.0 (definition/generation) with OI-012's remainder; a statement of
whether "no default" applies to the App's per-conversation choice (after
O-05-3); the K1-4 Codex-account identity read as a DEL-01-05 supply (if
assigned here); a mirror row for DEP-01-01-024 or a recorded reason for
none.

## B.4 Open items and owner choices

| # | Item | Owner / point of need (as stated) | Shapes the design now? | Options (files; inference marked) |
|---|---|---|---|---|
| O-05-1 | **OI-009** account home | Owner with App implementation owner; before account integration (TBD-001; HOSTING U-03) | **Yes, most.** Changes where credentials and provider settings live, the start sequence, the version-probe home, whether the App sees the person's existing sign-in, MCP and provider config, and the fresh-home fetch (F-14) | Files: shared; separated (OI-009; DECISIONS_DRAFT 11). Inference (DECISIONS_DRAFT): a middle form, "shared configuration, with sign-in kept separate", which Root `AGENTS.md` describes for the v3 App (D-GOV-43: "against the user's shared Codex configuration … with authentication separated for Chirality"); OI-009 says not to carry v3 or Root behaviour silently. v3 evidence: a root-private, app-owned `CODEX_HOME` per working root ("never reads, copies, or links your ambient `~/.codex`"). **Owner** (pass-2 Part 3, phase review) |
| O-05-2 | **OI-010** API-key behaviour, and coexistence of the three modes | App implementation owner; before API-key implementation/qualification (TBD-002) | **Yes.** At 0.158.0 one account per home (`Account` union; `account/login/start` per process). Per-conversation choice between a ChatGPT sign-in and an API key may need: (a) login switching per conversation (global; effect on other live threads not observed); (b) the key expressed as a provider credential rather than an account login (provider definition not in the generated types; not observed); (c) one supplier child per account home (HOSTING U-12 assumes one); (d) a reading of V4-APP-02 / V4-EXM-12 as "switch" rather than "concurrent" (a basis question) | Options are inference from the generated types; none observed. **Owner-level if (c) or (d)**: (c) restructures HOSTING; (d) touches accepted basis |
| O-05-3 | "No default" in the App | Not stated for the App | **Yes.** State of a new conversation when the person has not chosen; whether Codex's own `model`/`model_provider` config default or `Model.isDefault` may preselect | Files: D4-3 and V4-HOST-01 (am.) cover a host's agent; HOSTING L-5 "for the App path, D5 already leaves the model to the person … This boundary selects no default". Inference: (i) apply no-default to the App (no conversation starts until a mode is chosen; LOOP F-2(a)'s pattern); (ii) last-used or Codex-config default with the choice always shown. **Owner** |
| O-05-4 | Live observation of account flows | Owner (K1-6 pattern: the owner's sign-in "only if the local route cannot produce a tool call") | **Partly.** Without one, REQ-001/002 cases stay designed on generated types; coexistence (O-05-2) stays unobserved | (a) no live account observation; (b) the owner signs in himself once, with invented material; (c) also an API-key observation the owner configures. No agent enters a credential. **Owner** |
| O-05-5 | Supplier start-up traffic (U-18; B-1) | Owner, phase review | **Partly.** A separated home triggers the plugin fetch per home; a signed-in home enables the remote-control loop to chatgpt.com (OB-9 shows it tries without sign-in) | Accept and show; require prevented (needs an observation with network; may not be achievable). **Owner** |
| O-05-6 | **OI-008** process division | App implementation owner (phase review) | **Yes, small.** Where the API key and OAuth URL pass (main process vs webview); where config writes (`config/value/write`) are issued | HOSTING §12 O-1 |
| O-05-7 | External-token login (`chatgptAuthTokens`, refresh request) and other variants (`chatgptDeviceCode`, Bedrock, `account/gatewayOAuth/*`) | DEL-01-05 (HOSTING §6.1, U-20) | **Yes, small.** Which variants the App offers; `gatewayOAuth` may be the route for "cloud model by OAuth" from a non-OpenAI provider (inference; not observed) | Offer `chatgpt` (browser OAuth) and `apiKey` only; add device code; keep others unsupported (explicit error per R2) |
| O-05-8 | **OI-012** implementation/qualification pin | App implementation owner | No | — |
| O-05-9 | F-31 local Responses route drops MCP `namespace` tools | DEL-01-05 (routed) | **Yes, small.** The App must say, for a local provider, whether MCP tools reach the model; `modelProvider/capabilities/read` returns `namespaceTools` | Show the capability per provider; no gate (inference) |
| O-05-10 | F-32 setting carriers | DEL-01-05 | **Yes, small.** Which carrier (config file vs `thread/start`) the App uses to carry the person's approval/sandbox and provider settings | Carry unchanged (H9); choose carrier per element |
| O-05-11 | SCC-001 resolution (R2 cut of DEP-01-01-024) | WORKING_ITEMS / case | No (held arcs are non-gating) | — |
| O-05-12 | OI-007 distributed sign-in terms | Owner and supplier; before public release (DEL-01-06) | No | — |

**Owner flags:** O-05-1, O-05-3, O-05-4, O-05-5; O-05-2 if options (c) or
(d) are in play.

## B.5 What exists to build on

**Generated types at 0.158.0** (scratch `gen/ts-experimental/run1`,
manifest-matched; all named methods are in the stable client-request list):

- Client methods: `account/login/start`, `account/login/cancel`,
  `account/logout`, `account/read`, `account/rateLimits/read`,
  `account/usage/read`, `account/gatewayOAuth/login|read|cancel`,
  `account/bedrock/*`, `config/read`, `config/value/write`,
  `config/batchWrite`, `model/list`, `modelProvider/capabilities/read`,
  `thread/start` (`model`, `modelProvider`, `allowProviderModelFallback`,
  `approvalPolicy`, `sandbox`, `config`, …), TS-only `getAuthStatus`.
- `LoginAccountParams`: `apiKey {apiKey}` · `chatgpt
  {codexStreamlinedLogin?, useHostedLoginSuccessPage?, appBrand?}` ·
  `chatgptDeviceCode` · `chatgptAuthTokens {accessToken, chatgptAccountId,
  chatgptPlanType?}` · `amazonBedrock` · `amazonBedrockAccessKeys`.
  `LoginAccountResponse`: `chatgpt {loginId, authUrl}`, `chatgptDeviceCode
  {loginId, verificationUrl, userCode}`.
- `Account`: `apiKey` (no identity) · `chatgpt {email | null, planType}` ·
  `amazonBedrock`. `GetAccountResponse {account | null, requiresOpenaiAuth,
  workspaceRouting}`.
- Notifications: `account/login/completed {loginId, success, error}`,
  `account/updated {authMode, planType}`,
  `account/gatewayOAuth/changed`, `modelProvider/authRecoveryStarted|Completed`,
  `model/rerouted`, `configWarning`.
- `AuthMode` (8 values); `ForcedLoginMethod` `chatgpt | api`;
  `CliAuthCredentialsStoreMode` `file | keyring | auto | ephemeral`;
  `Model` includes `isDefault`; `ModelProviderCapabilitiesReadResponse
  {namespaceTools, imageGeneration, webSearch}`.
- Not in the generated types: the provider definition form (P-11; L-2).

**Observations:** PIN_SPIKE P-11, P-12, S-F-10, S-F-17 (version probe writes
into the home); OBS-1/1b OB-5, OB-7, OB-8, OB-9, OB-11; a working local
provider configuration (OBS_1 §2). No sign-in or API-key flow has ever been
observed.

**DEL-01-01 definitions:** S-4, §8.1 L-1…L-6 (the requirement account
DEL-01-05 consumes), §8.3 destination facts (requested vs effective, class
from DEL-01-05's configuration), §6.1 partition for the account server
request, §7 version identity record (configuration identity per
generation).

**DEL-05-01 definitions (host side, for the REQ-008 handoff):** LOOP §1
comparison table, §4 Chat Completions capability (FB-CC-1 fixture basis),
§5.1 settings states and NW rules — the host counterpart that DEL-01-05's
handoff must stay distinct from. Owner decision: the host loop keeps Chat
Completions; the App's Codex uses Responses to reach its model.

**App v3 exemplar (evidence only):** root-private app-owned `CODEX_HOME` per
working root; "One account for the app. Consent and permissions are per
folder" (presentation variant); `hosted-bootstrap/login/start|cancel`,
`logout`, `status`; the account panel shows identities "as digest suffixes
or epochs", never key material, tokens, device codes or emails; an oMLX
provider helper with a `DEFAULT_OMLX_BASE_URL` constant and its own API-key
store (a Chirality-held key, which v4's "credentials held by Codex" would
not carry over without a decision).

## B.6 Design scope for this pass

1. **`Design/ACCOUNT_AND_PROVIDER_ACCESS.md`** (OUT-001, OUT-002, REQ-001…004,
   REQ-009):
   - parties: the person (performs every sign-in and key entry), the App
     (receiving and selection), Codex (credentials), DEL-01-01 (S-4
     carriage), DEL-04-03 (model destination via HOSTING §8.3), DEL-01-04
     (if the Codex-account identity read is assigned here);
   - the three modes as configuration states per mode (not configured,
     configured, signed in / key present / server reachable, failed, signed
     out) and the per-conversation selection state, following the answer to
     O-05-3;
   - sequences with failure behaviour: ChatGPT browser sign-in (start →
     `authUrl` → completed or failed → cancel), device code, API-key entry,
     logout, local provider configuration, conversation start with a
     selected mode, token refresh/auth recovery notifications, provider
     unreachable, F-31 capability shown, no silent switch;
   - credential custody rules: no key or token in App storage, logs,
     records, errors or UI after hand-off (inference from REQ-001/002 and
     v3's practice); what the App may show of an account;
   - the coexistence model chosen or prepared under O-05-2, with the
     HOSTING consequences named;
   - the receivers table (DEP-01-01-022/024, DEP-09-02-013, DEL-05-01).
2. **OUT-003 records:** `Design/ACCOUNT_HOME_DECISION_RECORD.md` (options,
   consequences for HOSTING §4.2/§7.2/H9/F-14, the person's existing Codex
   setup, start-up traffic; the decision when made) and an API-key
   definition section (supported behaviour at 0.158.0 with standing labels;
   what remains not observed).
3. **REQ-008 handoff** to DEL-05-01: L-1…L-6 restated as App-provider
   requirements, F-31 and F-32, the distinction from the host's Chat
   Completions interface, and the explicit statement that host credentials
   and endpoints are the host native layer's.
4. **Verification design:** VER-001…010 as designed cases with what each
   needs (the person's sign-in, a key, an identified server, a candidate);
   a local prototype only where no credential is involved (for example the
   selection-state walk and a configuration-writing dry run in a scratch
   home).

**Leave out:** any sign-in or key entry by an agent (prohibited; the
person's own act); live account observations unless the owner authorises
one (O-05-4); qualification and substitution evidence (needs a candidate);
packaging and distribution terms (DEL-01-06, OI-007); host-loop credentials
(DEL-05-01, host native layer).

---

# C. Owner choices across both deliverables, ranked by design text that depends on them

| Rank | Choice | Deliverables and files affected | Why this rank |
|---|---|---|---|
| 1 | **OI-009 account home** (shared / separated / shared configuration with separate sign-in; and the probe home) | DEL-01-05 throughout; HOSTING §4.2, §7.2, H9, F-14, U-03; K1-4's Codex-account identity source (RS §6.1, EXEC CAP-8) | Every account, provider and configuration sequence depends on it; it is also the one item here that can restructure a first-increment file |
| 2 | **Coexistence of ChatGPT sign-in and API key per conversation** (O-05-2), where options (c) one child per home or (d) a basis reading are in play | DEL-01-05 REQ-004 design; HOSTING U-12 and the generation model; V4-APP-02/V4-EXM-12 | Without it the per-conversation selection cannot be written; option (c) changes HOSTING's single-child assumption. Options (a)/(b) are App-implementation-owner choices |
| 3 | **OI-008 process division** (phase review) | DEL-01-04 act control (CAP-4), answer path; DEL-01-05 key hand-off path; HOSTING §12 | Fixes where the act record and credential pass; the act control's key property depends on it |
| 4 | **"No default" for the App's per-conversation model access** (O-05-3) | DEL-01-05 selection states and new-conversation sequence; possibly DEL-01-04 conversation start display | A clear rule for hosts exists; none for the App; the caller's stated rule reads as covering both |
| 5 | **App display ownership: DEL-01-04 vs DEL-04-02 components** (OI-014; O-04-3) | DEL-01-04 Design scope; EXEC §2.4.4; AS §13 K-5/K-6 | Decides whether DEL-01-04 designs the checkpoint overlay and standing facets or only consumes them |
| 6 | **Live account observation** (O-05-4) | DEL-01-05 REQ-001/002/004 standing labels | Changes whether the sign-in and coexistence designs rest on observation or generated types only |
| 7 | **Supplier start-up traffic** (U-18; B-1) | DEL-01-05 (separated-home fetch, signed-in remote control); HOSTING L-4 | Affects disclosure text and the account-home record, not structure |
| 8 | Act control designed ahead of its contract (O-04-2) | DEL-01-04 | Label only, if the pass-3 direction already selects it |

Integrator or App-implementation-owner items (not ranked as owner choices):
explicit-decline mapping (O-04-5), supplier auto-resolution display
(O-04-6), the name-set-in-App setting's home (O-04-4), login variants
offered (O-05-7), F-31/F-32 handling (O-05-9, O-05-10).

# D. Structural questions that could force a later restructuring of a first-increment Design file

1. **HOSTING single child and account home (strongest).** HOSTING assumes
   one supplier child (U-12) and leaves the home element open (§4.2 step 3,
   §7.2, H9). If per-conversation choice between a ChatGPT sign-in and an
   API key needs separate Codex homes (O-05-2 (c)), HOSTING's lifecycle,
   generation numbering, register keying (by generation and thread),
   configuration identity (§7.1) and descendant rule (H11, U-16 "same home")
   need a per-home dimension. OI-009's answer alone changes text, not
   structure; the combination with O-05-2 can restructure.
2. **Who builds the App's checkpoint and standing display.** EXEC §2.4.4
   assigns SD-1…SD-5 to DEL-01-04; AS §13 offers K-5/K-6 as DEL-04-02
   components built by "the App" under CS-3; ACT V-07 sends label rules to
   DEL-01-04. If DEL-04-02 is chosen, EXEC §2.4.4 and §9.2 re-point (wording);
   if DEL-01-04, AS §13's options narrow. Not a restructure of either file,
   but it should be settled before DEL-01-04's Design is written.
3. **Act control placement under OI-008.** EXEC CAP-4 is written as a
   property, not a placement. If OI-008 puts capture in the main process,
   EXEC §2.7's component table and RS §14 writer sequence gain a capture
   step upstream of the writer (an addition). If the act control obligation
   lands outside DEL-01-04 (DECISIONS_DRAFT option E), seven files' citations
   change (ACT, EXEC, RS, WD, EXAMPLES, GUIDE, CA) — relabelling only.
4. **HOSTING §6.1 request-kind partition (U-20).** DEL-01-05's choice on
   external-token login moves `account/chatgptAuthTokens/refresh` from
   known-app-unsupported into an answerable class with no origin class in R9
   (neither A14, person-input nor named service). Adding an R9 class is an
   addition, not a restructure.
5. **Person identity sources (RS §6.1, EXEC CAP-8).** `Account` of type
   `apiKey` carries no identity and `chatgpt.email` is nullable; with a
   separated home the Codex account is the App's own sign-in. The K1-4
   wording "when Codex reports one" already covers this; no restructure
   expected.
6. **HOSTING R9 person-input kinds.** `isBlocking` and `autoResolutionMs`
   are not named in HOSTING; RT-10 `resolved-by-supplier` absorbs supplier
   auto-resolution. An addition to §6.1 or R3, not a restructure.

No question found that would restructure LOOP, PANEL, WD, P, C, ADAPTER, XT
or CA from these two deliverables: LOOP keeps the host and App interfaces
apart (§1) and does not consume DEL-01-05.

# E. Limits

- The generated types were read from the spike's scratch output (TS
  experimental, run1), with five files checked against the committed
  manifest. Every supplier fact above that is not in OBS_1 or PIN_SPIKE is
  `observed-in-generated-types` only. Coexistence of accounts, login
  behaviour, auto-resolution and attachment semantics are not observed.
- The Design files were read by search and by the sections listed in §0,
  not line by line. A passage that assumes these deliverables' contribution
  without naming them (for example "the App's account" or "request cards")
  outside those sections could have been missed.
- DEL-01-02, DEL-02-02 and DEL-04-02 ScopeOfWork files were read only where
  they name DEL-01-04 or DEL-01-05; their scoping belongs to S1-A and S1-C.
- The v3 exemplar was sampled by file heads and greps; statements about v3
  describe those files only.
- No SWBPIPE join, witness or adoption is claimed. No register, SoW, status,
  graph or Design file was changed.
