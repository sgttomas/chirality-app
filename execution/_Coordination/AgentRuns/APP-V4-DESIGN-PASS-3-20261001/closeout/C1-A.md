# C1-A — bounded closeout: DEL-01-02, DEL-01-03, DEL-01-04

- Node C1-A of run `APP-V4-DESIGN-PASS-3-20261001`. Executor: Type 2 TASK
  (Claude Code subagent, Claude Opus 5.5; does not delegate), dispatched by
  HELP_HUMAN.
- Method: `chirality-root:bundled:workflow:bounded-reconciliation`
  (`workflows/bounded-reconciliation/WORKFLOW.md`, sha256 `c7798c0ae59860f1…`,
  read whole), applied read-only under [BRIEFS.md](../BRIEFS.md) "Common
  rules" and "Closeout (after PR #1072)" → "C1" (BRIEFS sha256
  `a0befb8c4871e43d…`). Owner direction: [OWNER_DECISIONS.md](../OWNER_DECISIONS.md)
  (sha256 `8a5d11149045770d…`; "yes, run the closeout"). Precedent: pass 2's
  `closeout/C1-A.md` and `CLOSEOUT_ACCOUNT.md`.
- **Candidate:** branch head `b10a04b5bb` (after PR #1072). `git diff
  65f1d36f5a HEAD` over the three deliverable folders is empty, so the Design
  files compared are the bytes V21b-A rechecked (MERGE AS DRAFTS). C0 was
  editing in parallel; its working-tree changes touch HOSTING, ACCESS, WD,
  WR, EXEC and CA only (`git status`), none of the files compared here. C0's
  edits are wording, not commitments (BRIEFS). While this node ran, C0
  (`61e7a0afec`) and C1-B (`1cc5d5e736`) were committed. `git diff
  b10a04b5bb 1cc5d5e736` over the three deliverable folders is empty, so
  every comparison below holds at the new head. C1-B's overlapping rows
  (NR-07, NR-4) are listed in both records for the integrator's
  deduplication.
- **Boundary (binding).** DAG-003's `SOURCE_MANIFEST.sha256` binds every
  `ScopeOfWork.md`, `Dependencies.csv` and `_DEPENDENCIES.md`
  (`shasum -a 256 -c`: 130/130 OK at this node). No ScopeOfWork,
  register, `_STATUS.md`, `_CONTEXT.md`, `_REFERENCES.md`, MEMORY or Design file
  was edited. Every warranted change below is a **proposal** for SCA-V4-003
  and a later `dependency-extract` run. This is the only file written.
- Rulings read as binding: R1–R16 (common rules); DECISION-K3 as revised,
  DECISION-L, the SIWC reading, the closeout direction; R17
  (`b0af81bcbad9bc52…`), R18 (`abf5eee6324647ff…`), R19
  (`16930ecdcead7511…`), R20 with R21-1…R21-6 (`a9102712e0fb3c35…`).
- Proposal sources searched: `D/D1.md` (`df731fa3…`), `D/D2.md`
  (`943d5140…`), `D/D3.md` (`5c0fdcda…`), each round 1, round 2 and any
  addendum; `D/D4.md`, `D5.md`, `D6.md` by grep for items naming these three
  deliverables; `F/F0_JOINS.md` §3–§4 (`e93608be…`); `F/F-A…F-E2`, `RX`,
  `RV21-A`, `RV21-B`; `reviews/V21-A` (`04656905…`), `V21-B` (`8bbbd7c7…`),
  `V21b-A` (`b3507bac…`), `V21b-B` (`cd0c9c87…`); surveys `S1-A`, `S1-B`
  (§1.2–1.3, §2.2–2.3, A.2–A.3); pass 2 `closeout/C1-A.md` (`e2cb79e2…`),
  `C1-B.md` (`c819ba9b…`), `C1-C.md` (`9c4b9a37…`), `CLOSEOUT_ACCOUNT.md`
  (`703cd4bf…`).

## Inputs (sha256 at the candidate, first 16 hex)

| DEL | ScopeOfWork.md | Dependencies.csv | `_DEPENDENCIES.md` | `_STATUS.md` | Design file(s) |
|---|---|---|---|---|---|
| DEL-01-02 | `057ae2fdf4c3e98c` | `84451e124cf27185` | `2f40aa30435a6654` | `76353a510b0de5d5` (INITIALIZED) | RECOVERY-v0.2 `EXECUTION_AND_RECOVERY.md` `678042beae0327e6` |
| DEL-01-03 | `b5d533cb3dbea97b` | `9ac820166dd07dde` | `fe49681791ad749e` | `52ea2e2fa6506ad3` (INITIALIZED) | NPTD-v0.2 `NATIVE_PLANS_TOOLS_DELEGATION.md` `6eed39dcee4acf4b` |
| DEL-01-04 | `0cdb44e297010b70` | `20ce3808597bf283` | `18cbcd7342c3f06c` | `12de2a18b4016880` (INITIALIZED) | NIR-v0.2 `NATIVE_INTERACTION_RECEIVING.md` `7144aebd4a72522d`; AAC-v0.2 `APP_ACT_CONTROL.md` `062ce28c8a4ec0bc` |

Each Design header pins its ScopeOfWork and register by these bytes (checked
by reading the headers against the recomputed hashes). The register and SoW
hashes equal the DAG-003 `SOURCE_MANIFEST` lines 4–12. The four Design
hashes equal V21b-A's table. The schemas, examples and prototypes were read
where a claim depended on them, and the three prototypes were rerun (see
"Checks").

## Reading conventions

As pass 2's C1-A:

- **Status at the 60% level** (`loop/LOOP_INIT.md`: interfaces, states, data,
  operating sequences, failure behaviour, verification): *developed*,
  *partial* (a definition element missing, named), *named only*, *absent*.
- AC and VER items take the status of the requirement they verify, because
  every one has a designed case. That no case has run against an App
  candidate is stated once per deliverable and does not lower the status.
- **Registers follow the ScopeOfWork.** Each `_DEPENDENCIES.md` records
  CONSERVATIVE extraction from `ScopeOfWork.md` only. A new or mirror row
  therefore needs a SoW sentence naming the other end, and the register items
  below name the SoW item they follow.
- **Arc classes** (consumer → supplier; DAG-003): *mirror only*, *new arc*
  (admitted, or held when both ends are in SCC-002), *non-topological*.
  SCC-002 has 13 members, among them DEL-01-04. DEL-01-02 and DEL-01-03 are
  in no SCC.
- **IDs.** Source IDs are kept: SC3-…, F0 NR-/M-/ST-, D3 NR-4, R3-…. Items
  first raised here are marked **(C1-A)** and numbered after the source
  series. Items amended here are marked **(amended at C1-A)**.

---

## Summary

| DEL | Commitments (OUT+REQ+AC+VER) | Developed / partial / named / absent | SoW items (of which new / amended here) | Register items in its own register | Lifecycle |
|---|---|---|---|---|---|
| DEL-01-02 | 4+9+9+9 = 31 | 31 / 0 / 0 / 0 | 11 (1 new; 3 completed) | 8 (4 of them conditional) | INITIALIZED; IN_PROGRESS would be truthful |
| DEL-01-03 | 3+8+7+7 = 25 | 25 / 0 / 0 / 0 | 8 (1 new) | 6 | INITIALIZED; IN_PROGRESS would be truthful |
| DEL-01-04 | 4+7+7+7 = 25 (+ the proposed act-control obligation) | 25 / 0 / 0 / 0 | 12 (1 new; 4 amended) | 9 | INITIALIZED; IN_PROGRESS would be truthful |

**Totals:** **31 ScopeOfWork items** (28 from D1–D3, 3 first raised here; 7
D-items amended or completed here); **23 register items** in these three
registers: 12 mirror only (4 of them conditional), 5 new arcs (2 admitted, 3
held) and 6 non-topological. A further **4 consumer-side rows** in other
registers name DEL-01-02 (F0 NR-01…NR-04, new admitted arcs). **0 basis
items.**

**Main result.** Every OUT, REQ, AC and VER of the three INIT contracts now has
a defined answer in the Design files. The contracts themselves lag: much of
what was designed rests on owner decisions and rulings the ScopeOfWork
predates (R17-3 stops, K-3, K-4, K-5, K-8, K-10, L-1, L-2, R19-2, R19-7). The
largest result with no commitment is the App act control, which stays
PROPOSED until SCA-V4-003 carries SC3-01-04-1.

The structural question still open is the same for all three: OI-008, the
Rust/TypeScript process division. Each file states its requirements apart from
the R17-5 placement, so another answer would move code, not obligations.
Everything else open is a number, an implementation means, an observation or
a person's act. No case has run against an App candidate.

The three prototypes reran from an archive of the candidate with the same
results the files record:

- RECOVERY: 16/16;
- NPTD: 18/18;
- NIR with AAC: 151 checks, 0 failed.

---

## DEL-01-02 — Durable execution and request recovery (RECOVERY-v0.2)

### 1. Commitment → result

| Item | Where RECOVERY answers | Status | Still missing (definition) |
|---|---|---|---|
| OUT-001 custody code incl. answer/decline handling and unknown-request errors (CODE) | §1 (one process per App-owned home, L-1; reconciliation with HOSTING §6.5), §3.5 RQ-01…RQ-09, §4.1 offered operations, §6 U-10, U-11 | developed (definition) | Code; placement (OI-008, U-R8) |
| OUT-002 interrupt, reconnect, relaunch code (CODE) | §2 DEF-1…DEF-7, §3.1 AS, §3.2 CV, §3.3 OA, §3.4 SR, §5 SQ-W, SQ-I, SQ-Q, SQ-R, SQ-X, SQ-S | developed (definition) | As OUT-001 |
| OUT-003 candidate-bound fixtures (TEST) | §11.1 VC-R-01…VC-R-18; §11.2 prototype (16 results) | developed (designed) | Recorded-exchange fixtures X-04…X-10 wait for HOSTING §9 captures; VC-R-12…14 need a candidate and the person |
| OUT-004 unknown-outcome and reuse documentation (DOC) | §7 ledger and source standing, §8 formats and handoff map, §10 reuse account, §12 act boundary, UNRESOLVED | developed | — |
| REQ-001 main-process custody; window loss is not a stop | §2 DEF-1, §3.3 OA-01…OA-05, SQ-W (zero frames sent, C-01) | developed | — |
| REQ-002 explicit interrupt; request, transmission and result apart; descendants | DEF-3, §3.4 SR-01…SR-12 with labels and causes (incl. *codex-stop*, *cancel-answer*), SQ-I, §3.4 "Descendants" | developed | A child's interrupt and a cascade from the parent are not observed. Children were observed only through an adapter (U-R1; R18-9). The rule "report what was observed" is defined |
| REQ-003 answer or decline; never from silence | §3.5 RQ (custody view over HOSTING §6.2), §6 U-10 (no App decline at stop), U-11 (no automatic decline, R17-9) | developed | — |
| REQ-004 explicit error for unknown requests; settlement ≠ acknowledgment | §1 (DEL-01-01 writes the error, HOSTING §6.5 accepted; RQ-08), SQ-U, SQ-A, RQ-05, RQ-09, §6 U-09 | developed | U-09 closed for the interrupt trigger only; other before-reply triggers unobserved |
| REQ-005 recover from Codex; continue after quit/relaunch | §2 DEF-6/DEF-7 (K-4), SQ-Q, SQ-R, SQ-X, CV-11…CV-15, §7 ledger index | developed | Numbers (U-R4, TEST VALUES); persistence technology (U-R7 = TBD-002); ledger loss (U-R2), retention (U-R3) |
| REQ-006 observed events and unknown outcomes handed over; no stronger claim | §8.1 three PROPOSED schemas (no place for an act, approval or run end; C-08); §8.2 handoff map; §7 "never kept" | developed | Receiver side done in RS-v0.9 R13/R11 and EXEC CE-13/14 (F-C, F-B) |
| REQ-007 required behaviour regardless of reuse | §10 (v3 assessed; none reused) | developed | — |
| REQ-008 fixtures and candidate-bound evidence | §11 (Needs column: D, F, P, C, O) | developed (designed) | As OUT-003 |
| REQ-009 no act owned by another deliverable | §12 | developed | — |
| AC-001…AC-009 / VER-001…VER-009 | VC-R-01…VC-R-18 (VC-R-14 is the V4-EXM-11 native witness) | developed (designed) | VER-008 (VC-R-12), VER-009 (VC-R-13) not run; native witness not run |

Run state: the model cases ran on the prototype (rerun here: "16 results, 16
as expected, 0 not"; C-17 takes every one of the 58 table rows). None ran
against a candidate.

### 2. Result → commitment

| Element | Authority | Supported by the ScopeOfWork? |
|---|---|---|
| Three stop operations and the DEF table (§2) | R17-3 (INTEGRATION; Part 2 not objected to) | REQ-002 says "explicit stop" ambiguously; read as DEF-3 (header reading 1) → SC3-01-02-1, -2 |
| Quit asks first; "interrupted by quit"; resume offer (SQ-Q) | K-4 (SETTLED) | REQ-005 predates it → SC3-01-02-3 |
| One Codex process per App-owned home; generation identity {session, home, counter} | L-1 (SETTLED), R19-4 | REQ-001/CLM-002 assume one child → SC3-01-02-9 |
| Stop Codex / Restart Codex (DEF-5a, cause *codex-stop*) | R18-1 C-12 (INTEGRATION) | Not named; optional clause on SC3-01-02-3 (D1 R2.4, left to the integrator) |
| App ledger: pointers and App-observed facts only | R17-4 (DERIVED from ARCH §3) | REQ-006/OUT-004 → SC3-01-02-7 |
| No automatic decline; pending at stop ends unanswered | R17-9 (INTEGRATION) | REQ-003 → SC3-01-02-4 |
| Ordered receiver tags for runs that follow one another (R19-2); `assess live work` for DEL-01-05 (C-23) | R19-2; C-23 | Offered interfaces. The tag consumers have no row (NR-01…NR-04, proposed). DEL-01-05 gets a runtime value with no row, because a row would form an SCC (F0 §3) |
| *cancel-answer* cause; items "not completed (turn ended)"; graceful-stop note shown (G-5) | R18-1 C-13; R18-7 G-4, G-5 | Follow from REQ-002/REQ-006; optional SC3-01-02-10 |

Unsupported additions: none found. The DEF-2 reading of "reconnect" holds
that no third connection exists. The SoW wording admits that reading, so no
proposal is made.

### 3. What the 60% description still lacks

- **Structure:** OI-008 placement (U-R8; R17-5 PROPOSED). The phase review
  owns it.
- **Implementation means the SoW leaves open (TBD-002):**
  - the persistence technology and location (U-R7);
  - ledger retention and deletion (U-R3);
  - whether the fallback list after a lost ledger is filtered by project
    (U-R2);
  - deleting a conversation that has forks (U-R12).
- **Numbers:** quit wait, stop wait, journal size and overlap wait (U-R4, with
  HOSTING U-05). They are TEST VALUES by the SoW's own rule.
- **Observations:**
  - a child's interrupt and a cascade from the parent (U-R1);
  - whether App and CLI share a session store (O-6);
  - whether `turn/interrupt` writes a history note;
  - every supplier statement is at 0.158.0 (U-R13, R19-5).
- **Residuals in the file (returned, §"Returned to the graph"):**
  - U-R6 is still listed open, although RS-v0.9 §10 now answers it ("a turn
    interrupt is not recorded in format 0.1").
  - U-R5 (two windows on one conversation) is answered for cards by NIR WI-4
    but not for the stop control.
- **Verification:** an App candidate, the person, and recorded HOSTING §9
  fixtures.

### 4. Register observations

| Row | Observation | Proposal |
|---|---|---|
| DEP-01-03-012 (DEL-01-03 → here) | No DOWNSTREAM mirror here (checked by script over all registers) | R3-01-02-a (M-1) |
| DEP-09-02-010 (DEL-09-02 → here) | No mirror here | R3-01-02-b (M-2) |
| DEP-01-02-021 (→ DEL-04-01) | Statement: "OI-001/OI-002 choices remain with the owner and App/SWB contract owners". This is stale for this scope: D2 and D3 rule them, ACT V-21 carries them, and RECOVERY §4.2 consumes P-04 | R3-01-02-c (with SC3-01-02-5) |
| DEP-01-02-018 (→ DEL-01-01) | Notes: "OI-012 supplier pin … remain open as stated". D4 has since selected 0.158.0 for definition | R3-01-02-d (optional, with SC3-01-02-6) |
| DEP-01-02-019, -020 | Agree with RECOVERY §4.1 and §8.2. DEL-01-02 writes nothing in DEL-04-03's format (R17-10), so -020 stays truthful as a handover of custody facts the receiver maps | None |
| New consumers with Design reliance and no row | DEL-02-03 (tags, custody events; EXEC §2.7, AE-6, RE-4); DEL-03-03 (ADAPTER PI-6, XF-41); DEL-09-09 (XT XC-06, optional); DEL-02-02 (WR SQ-X, optional) | F0 NR-01…NR-04 in the consumers' registers; supplier-side mirrors R3-01-02-e…h, conditional |
| EXTERNAL rows | This register has none (`_DEPENDENCIES.md`: "0 EXTERNAL"). TBD-001/-003 name OI-008, OI-012, DEP-005, OI-001 and OI-002, folded into DEP-01-02-018 and -021 by CONSERVATIVE extraction | Not proposed. RECOVERY names the owners (U-R4, U-R7, U-R8) |
| Supplier-side mirror DEL-04-01 → here (DEP-01-02-021); DEL-04-03 counterpart of -020 | Pass-2 C1-A: "Outside mirrors noted, not proposed (D1)" | Unchanged; those registers' owners |

### 5. Lifecycle

INITIALIZED since 2026-09-27. "Selected production contract exists and
validates" is still true. But the deliverable has had active human-directed
agent work since 2026-10-01 (owner: "Proceed as recommended"; Design at
v0.2). The truthful state is therefore **IN_PROGRESS**
(SPEC §3.2–§3.3: INITIALIZED → IN_PROGRESS by the Human or WORKING_ITEMS,
as the first increment's owner DECISION-6 recorded for its deliverables).
CHECKING is not warranted: production obligations are open and the SoW lags.
SEMANTIC_READY does not apply (`_SEMANTIC.md` is a placeholder). No change
is made here.

---

## DEL-01-03 — Native plans, tools and delegation views (NPTD-v0.2)

### 1. Commitment → result

| Item | Where NPTD answers | Status | Still missing (definition) |
|---|---|---|---|
| OUT-001 views (CODE) | §3 item scope and split, §4 experimental surfaces, §5 plans, §6 tools and goals, §7 delegation, §8 version line, §9 truthful actor, §12 sequences, §13 four transition tables (41 rows) | developed (definition) | Code; placement (OI-008, U-P7) |
| OUT-002 fixtures (TEST) | §15.1 fixture method (`constructed` now, `recorded` from OBS-2 logs later); §15.2 NV-01…NV-11; §15.3 PC-01…PC-18 | developed (designed) | Recorded fixtures; candidate; WebKit, Chromium and packaged witness |
| OUT-003 feature and reuse map (DOC) | §14.1 features, owners, basis, standing; §14.2 v3 assessed | developed | — |
| REQ-001 plans and revisions | §5.1 two surfaces, §5.2 RV-1…RV-6, §5.3 PS-1…PS-6, §5.4 plan-mode element, PL/CL tables | developed | The checklist surface was never produced at 0.158.0 (U-P1); it stays designed and labelled. Whether the model gives plan mode precedence over role text is open (U-P3) |
| REQ-002 tool activity and outcomes, unknown stays unknown | §6.1 display states (incl. `not-completed`, G-4), §6.2 TR-1…TR-6, §6.3, TI-01…TI-15; goals §6.4 (G-3) | developed | MCP items unobserved (OB-1); a goal tool call unobserved (U-P9) |
| REQ-003 delegation visible, fleet seam, no inference from parent completion | §7.1 availability (R21-1 order; this section is the reference), §7.2 identity, §7.3 DR-1…DR-6, §7.4, §7.6, §7.7 export schema, DS table | developed | Delegation observed only through an adapter (R18-9). Stock LM Studio drops `namespace` tools. NV-04 (parent completed, child running) and a child's interrupt are not observed (U-P4); U-P8 is open |
| REQ-004 selected version and experimental supplements | §8 VR-1…VR-3; §4 EX-1…EX-3 | developed | — |
| REQ-005 truthful actor | §9 TA-1…TA-5 | developed | — |
| REQ-006 map and reuse | §14 | developed | — |
| REQ-007 act and owner boundary | §16 | developed | — |
| REQ-008 evidence binding | §15.1, §15.2 "Runnable now?" column | developed (designed) | As OUT-002 |
| AC-001…AC-007 / VER-001…VER-007 | NV-01…NV-11 | developed (designed) | VER-006, VER-007 are review-only; nothing on a candidate |

Run state: PC-01…PC-18 reran here ("SUMMARY 18/18"; PC-15 reached 41/41 rows
equal to the model's; PC-16 checked all 64 signal combinations against R21-1).
None ran against a candidate.

### 2. Result → commitment

| Element | Authority | Supported? |
|---|---|---|
| Plan-mode element offered to DEL-01-04, which composes `collaborationMode` and sends `default` to leave (§5.3–§5.4) | K-5 (SETTLED); R18-1 C-05, C-06 (INTEGRATION); OBS-2 O-8 | REQ-001 (plan creation interaction); the "experimental, fully usable without" rule → SC3-01-03-6; the receiver needs a row and SoW anchor (NR-05; SC3-01-03-8 (C1-A), SC3-01-04-10) |
| Checklist revisions not copied; "not recoverable" after restart or relaunch | R17-4; R18-1 C-03 | REQ-001 leaves durability open → SC3-01-03-4 (with "or a supplier restart") |
| Delegation availability rule (§7.1) | R18-1 C-04; R21-1 | REQ-003 |
| Task-agent delegation shown with the standing DEL-02-04 hands (DR-4) | K-10 (SETTLED); C-07, C-08 | → SC3-01-03-5 (duplicate in substance of SC3-02-04-4, C1-B's) |
| Goals line (§6.4) | R18-7 G-3; R20-8 | REQ-002 (native activity); no proposal |
| Run-boundary labels from markers handed in (§5.7) | R19-2 | Display only; REQ-005 and §16. No proposal (a row would form an SCC; a runtime value instead) |
| Children's roles shown as reported; guidance "not known" without a role type (DR-5) | R18-4 | REQ-003; no proposal |
| "Carry out this plan" is ordinary input (§5.5) | R17-9 | → SC3-01-03-7 |

Unsupported additions: none found.

### 3. What the 60% description still lacks

- **Structure:** OI-008 placement (U-P7).
- **Data:** the content-identity method of a plan revision (RV-3, a TEST
  VALUE; U-P6 with HOSTING U-08). This is what DEL-02-02 receives through
  DEP-01-03-013.
- **Receivers:** DEL-06-01 (the fleet receiver of the export) has no Design
  file, so the export seam is defined from this side only.
- **Observations:**
  - checklists never produced (U-P1);
  - plan-mode precedence (U-P3);
  - child interrupt and NV-04 (U-P4);
  - `namespaceTools` for local providers (U-P8);
  - a goal tool call (U-P9);
  - delegation on any stock route (adapter-only, R18-9).
- **Verification:** an App candidate; recorded fixtures; the WebKit,
  Chromium and packaged witnesses (REQ-008).

### 4. Register observations

| Row | Observation | Proposal |
|---|---|---|
| DEP-06-01-007, DEP-09-02-011, DEP-09-05-008 (consumers → here) | No DOWNSTREAM mirror here. DEP-01-03-014 names only PKG-06 (package-level, not topological) | R3-01-03-a…c (F0 M-3); the package row may stay |
| DEL-01-04 consumes the plan-mode element, item anchors and availability | No row on either side; adopted by R18-1 C-06 | F0 NR-05 (row in DEL-01-04's register) and mirror R3-01-03-d here |
| DEP-01-03-017 (OI-001;OI-002) | Statement still "Retain owner … decisions on exact always-reserved acts and classifier permissions before …". SCA-V4-002 refreshed DEL-01-04's twin rows (DEP-01-04-013 refreshed to the OI-001 residue, -014 retired as ruled by D3), but not this one | R3-01-03-e (with SC3-01-03-2) |
| DEP-01-03-011 Notes | "OI-012 selected pin remains App implementation owner choice". D4 has since selected 0.158.0 for definition | R3-01-03-f (optional, with SC3-01-03-1) |
| DEP-01-03-012, -013, -015, -016, -018 | Agree with NPTD §10.1, §5.6, U-P7, §14, §7.6 | None |
| DEP-01-03-015 owner name | "App implementation owner". Under L-7 the Owner is that owner. The name stays correct | None (C1-B carries DEL-01-05's L-7 reading) |

### 5. Lifecycle

INITIALIZED since 2026-09-27. As for DEL-01-02, **IN_PROGRESS** would be
the truthful state (active work, NPTD at v0.2), and CHECKING is not
warranted. No change is made.

---

## DEL-01-04 — Native requests, outcomes and attachments (NIR-v0.2, AAC-v0.2)

### 1. Commitment → result

| Item | Where NIR / AAC answer | Status | Still missing (definition) |
|---|---|---|---|
| OUT-001 cards and responses (CODE) | NIR §4.1 eleven kinds, §4.2 FO/LB, §4.3 DM-1…DM-6, §4.4 CS over every register row, §4.5 answer submission and SE-1…SE-3, §4.6 SQ-R, §4.7 anchors, §4.8 waiting indicator | developed (definition) | Code; placement (OI-008) |
| OUT-002 turn/outcome and attachment presentation (CODE) | NIR §5.1 TO-0…TO-9, §5.2 three stop operations plus Stop and Restart Codex, §5.3 SQ-V, §5.4 start display, §5.5 descendants, §5.6 turn composition, §5.7 runs, §5.8 Continue as / Fork; §6 carriers (R21-2), AT-1…AT-10, SQ-A, supply-record schema 0.2 | developed (definition) | Attachment storage AO-1/AO-2 (TBD-003, U-NIR-2); text-element bound and image route (U-NIR-10) |
| OUT-003 fixtures (TEST) | NIR §13.1 VC-NIR-01…25; AAC §8 VC-AAC-01…15; prototype 151 checks | developed (designed) | VC-NIR-11, -15, -17, -18 and VC-AAC-13, -14 not run (candidate, person) |
| OUT-004 receiving contract (DOC) | NIR §2 IF-1…IF-15, §7 draft receiving, §10 reuse, §11 exclusions, §12 open choices | developed | — |
| REQ-001 native semantics; grant, deny, answer, explicit decline; unknown-request errors; no answer from silence | NR-1…NR-3, §4.1–§4.4 | developed | Effect of the PROPOSED empty-answer and empty-grant declines (DM-4, DM-5) is not observed (U-NIR-1) |
| REQ-002 observed outcomes only; settlement ≠ acknowledgment; descendants; recovered view | §5.1–§5.3, §5.5; CS-2…CS-7 | developed | "Primary completed, child running" not observed (NV-04) |
| REQ-003 supplied-content identity | §6 (carriers, AT-1…AT-10, SQ-A); supply-record schema | developed | Identity method open by design (RS U-04, HOSTING U-08; VER-003 prescribes none) |
| REQ-004 draft receiving; draft until registration; collisions | §7 (D5's names; C-02 read side; refusals) | developed | — |
| REQ-005 act distinctions; faithful display; lapse | §8 AP-1…AP-10; §9 PD-1…PD-7; AAC | developed | The positive case needs a person (DEP-01-04-019) |
| REQ-006 no act owned elsewhere | §11 | developed | — |
| REQ-007 required interactions independent of reuse; open choices at owner and point of need | §10, §12, UNRESOLVED | developed | — |
| AC-001…AC-007 / VER-001…VER-007 | VC-NIR and VC-AAC cases | developed (designed) | Display and real-App reload cases not run |

Run state: rerun here, "151 checks, 0 failed". K-16: all 11 RS entries the
act control wrote are valid against RS's schema. K-17: WR's two descriptor
examples pass through offer and capture into RS. Nothing ran against a
candidate.

### 2. Result → commitment

| Element | Authority | Supported by the ScopeOfWork? |
|---|---|---|
| **The App act control** (AAC whole: A4, A6, A7, A15; standing facility; NA-1…NA-6; P-2 native confirmation; SEAL-2; identity per K1-4) | K1-4, K-8 (SETTLED); R17-6 (INTEGRATION); L-4, L-5; R21-3 | **No anchor** (`grep` of the SoW for "act control" returns 0). PROPOSED until SCA-V4-003 carries SC3-01-04-1, which supersedes SC2-01-04-1 |
| Checkpoint overlay and standing facets placed in the App (§9) | R17-7 | Not named → SC3-01-04-5 |
| Start display: no model selected, last choice offered (§5.4 ST-1…ST-3) | K-3; R18-2 | REQ-002 silent → SC3-01-04-6 (amended at C1-A to name DEL-01-05) |
| Role element, role fixed, Continue as, start offer, End-run offer (§5.4 ST-5/6, §5.7, §5.8) | R17-9, L-2, R19-2, R19-3, R19-8, R20-1, R20-5, R20-6, R20-9, R20-11 | → SC3-01-04-11 (amended at C1-A for the finished line) |
| Turn composition: plan mode, run-start text, run-end line (§5.6) | C-06, R19-7, R20-3 | → SC3-01-04-10 |
| Stop Codex / Restart Codex (§5.2) | C-12 | SC3-01-04-7 (optional C-12 clause at C1-A) |
| Waiting indicator (§4.8) | C-24 | → SC3-01-04-12 |
| Attachment carriers and standings (§6, R21-2) | R21-2 (INTEGRATION) | REQ-003 already asks exactly this; no proposal |
| Secret answers kept out of records (SE-1…SE-3) | PROPOSED | REQ-001 (native semantics) and REQ-003 in spirit; no proposal (design detail; HOSTING join J-H4) |

### 3. What the 60% description still lacks

- **Contract standing:** the act control is PROPOSED until SCA-V4-003
  (U-AAC-7).
- **Structure:** OI-008. The capture placement P-2 under O-1 (U-AAC-1); the
  rest of NIR §1.1 PL-1…PL-5.
- **Record provenance:** SEAL-2 and DEL-04-03's reader rule (U-AAC-3; RS
  U-32, conditional).
- **Identity:** the home of "the name set in the App" is assigned here as
  INTEGRATION (U-AAC-5). A signed-in Codex account's report is not observed
  (U-AAC-6; L-6).
- **Card effects:** DM-4/DM-5 (U-NIR-1).
- **Attachments:**
  - AO-1 or AO-2 (U-NIR-2; TBD-003);
  - the text-element bound and the image route (U-NIR-10);
  - `thread/attachment/*` is not used (U-NIR-4).
- **Wording:** the buttons' wording and placement stay PROPOSED (U-NIR-8,
  U-NIR-9).
- **Join residual:** WR TT-3 against NIR AT-8 (V21b-A N-2). NIR already
  follows R21-5; C0 aligns WR's side.
- **Verification:**
  - the person's positive act case (DEP-01-04-019);
  - the candidate's native confirmation (VC-AAC-13) and provenance
    (VC-AAC-14);
  - display cases.

### 4. Register observations

| Row | Observation | Proposal |
|---|---|---|
| DEP-02-03-027 (X-1; DEL-02-03 → here) | No mirror here | F0 M-7 = pass-2 R2-01-04-a (kept) |
| DEP-09-02-012 (DEL-09-02 → here, admitted) | **No mirror here, and no pass-3 item proposes one.** Found by the script over all registers; NIR IF-12 relies on the row | R3-01-04-b **(C1-A)**, anchored by SC3-01-04-13 (C1-A) |
| DEP-01-04-009 (→ DEL-02-02) | The statement names draft identity and transitions only. NIR IF-4, IF-5 and IF-14 also receive the A15 descriptor (one per act, R21-3) and the run-start text and run-end line. D3 R2.5 proposed "A15 descriptors per entry", which R21-3 made stale | R3-01-04-a (D3, corrected at C1-A) |
| DEP-01-04-010 (DOWNSTREAM → DEL-02-02) | Omits the act control that captures A15 | ST-1 = SC3-01-04-9 (pair of ST-2 on DEP-02-02-013, C1-B's) |
| New inputs NIR names with no row | DEL-01-03 (IF-13), DEL-01-05 (IF-10), DEL-04-02 (IF-8), DEL-02-03 (IF-9), DEL-02-04 (IF-15) | F0 NR-05, NR-07, NR-08, NR-09 and D3 NR-4 (§"Register items") |
| DEP-01-04-009, -011, -012 supplier-side | No counterpart in DEL-02-02, DEL-04-01 or DEL-04-03 | Not proposed here. DEL-02-02's counterpart is C1-B's R3-02-02-a (new there). DEL-04-01/04-03 are pass-2 "outside mirrors noted, not proposed", unchanged |
| D3 NR-4 against ROLE | ROLE-v0.2 §7.2 O-8 hands the role list to DEL-01-04 as a runtime value with no row; NIR IF-15 proposes NR-4. C1-B §3.4 records the disagreement and a conditional mirror R3-02-04-c | Keep NR-4 (NIR's need is a production interface: the role list, the Continue-as composition and the guidance-changed signal). ROLE O-8 is aligned if NR-4 is adopted |
| DEP-01-04-013, -015…-019; -014 RETIRED | Agree with NIR §12 and AAC §9 (D2/D3/D4 refreshed by SCA-V4-002) | None |

### 5. Lifecycle

INITIALIZED since 2026-09-27. The ScopeOfWork was revised under SCA-V4-002;
`_STATUS.md` was not touched. **IN_PROGRESS** would be the truthful state
(active work; NIR and AAC at v0.2), and CHECKING is not warranted. No change
is made.

---

## Proposed ScopeOfWork items (none applied)

Each amendment that applies these adds its AX line naming the decision
records (DECISION-K1 of pass 2; DECISION-K3 as revised and DECISION-L of this
run) and the rulings R17–R21. Quoted "old" texts were copied from the
current SoW files.

### DEL-01-02

| ID | Location | Old (excerpt) → new | Reason | Source | Disposition here |
|---|---|---|---|---|---|
| SC3-01-02-1 | REQ-002, first sentence | "Support native interruption as an explicit act and preserve its actual observed result." → "Support the person's interruption of a turn as an explicit act and preserve its actual observed result. Interrupting a turn, ending a workflow run and stopping the Codex process are distinct operations; an interrupt, a quit or a supplier exit never ends a run." | "Stop" is ambiguous against EXEC AE-7 and RS's run end | R17-3; R20-1; RECOVERY §2 | Kept (pairs SC3-01-04-7) |
| SC3-01-02-2 | AC-002, VER-002 first sentences | "An explicit native stop is distinguishable from observation loss…"; "Invoke native stop deliberately…" → "An explicit turn interrupt is distinguishable from observation loss and from a run end…"; "Interrupt a turn deliberately…" | As -1 | R17-3 | Kept |
| SC3-01-02-3 | REQ-005 after the second sentence; AC-006; VER-006 | Append: "When the person quits with live turns or pending requests, the App asks first and lists them; on confirmation the live turns are interrupted and recorded as interrupted by quit, and after relaunch they are shown with an offer to resume." AC-006: "…including turns interrupted by a confirmed quit." VER-006: "Quit with live work, confirm the question, relaunch…" | K-4 | DECISION-K3 K-4 | Kept. **Completed at C1-A (optional clause D1 left to the integrator):** add "The same applies when the person stops or restarts Codex from the App." C1-A recommends taking it so that it pairs SC3-01-04-7's C-12 clause (R18-1 C-12; RECOVERY §2 DEF-5a) |
| SC3-01-02-4 | REQ-003, last sentence | Append: "No pending request is declined automatically after a period; a request still pending when the Codex process stops ends unanswered and is never answered afterwards." | R17-9; U-10, U-11 | R17-9; RECOVERY §6 | Kept (pairs SC3-01-04-3) |
| SC3-01-02-5 | CLM-004 last sentence; TBD-003 | "…and no blanket reserved-act/classifier policy has been settled." → "…the reserved acts (first-increment DECISION-1 D2) and the person's own tool-permission and sandbox modes (D3) are adopted for this scope and carried by App-v4 `DEL-04-01`; no App rule answers a tool-permission request affirmatively." TBD-003: add "For this scope D2 and D3 apply (ACT §10.1 V-21); OI-001/OI-002 stay open beyond it." | Overtaken (SCA-V4-002 Impact V-4) | S1-A §1.1; ACT V-21 | Kept; enables R3-01-02-c |
| SC3-01-02-6 | TBD-001 | Append: "Owner decision D4 selected Codex 0.158.0 as the definition and generation pin, not a qualification; OI-008's main-process division is proposed as HOSTING §12 O-1 (R17-5)." | D4 | S1-A §1.1; R17-5 | Kept. **Completed at C1-A:** add, as SC3-01-03-1 does, "the Owner is also the App implementation owner (DECISION-L L-7)". This keeps one wording across the D4-pin class (SC3-01-02-6, SC3-01-03-1, P-3, SC3-02-04-7). Enables R3-01-02-d |
| SC3-01-02-7 | REQ-006 first sentence; OUT-004 last sentence | Append: "Supplier facts (supplied guidance, model destination, tool-permission settlements) reach `DEL-04-03` directly from `DEL-01-01`; this slice hands its own custody observations in its own format and keeps across relaunch only references and App-observed facts, never a copy of conversation content." | R9-7, R17-4 | RECOVERY §7, §8 | Kept |
| SC3-01-02-8 | CLM-001, interfaces sentence | "…serve App-v4 `DEL-01-04`, and hand compact evidence to PKG-04…" → "…serve App-v4 `DEL-01-04`, `DEL-01-03` and `DEL-09-02` (each declares it upstream in its own register), and hand compact evidence to PKG-04…" | Enables R3-01-02-a, -b | S1-A §1.2–1.3 | Kept. **Completed at C1-A (conditional):** if the amendment adopts F0 NR-01…NR-04, also name "`DEL-02-03` (run tags and custody events), `DEL-03-03` (in-flight items and the relaunch fact)" and, where adopted, "`DEL-09-09`" and "`DEL-02-02`". This enables R3-01-02-e…h |
| SC3-01-02-9 | CLM-002 first sentence; REQ-001 | "Main-process ownership of the Codex child, protocol session and outstanding-request register is fixed." → "…of each Codex child (one per App-owned Codex home), its protocol session and outstanding-request register…"; REQ-001 likewise | L-1 | DECISION-L L-1; R19-4 | Kept |
| SC3-01-02-10 (optional) | REQ-002, after -1's sentence | "A turn ended by Codex after the person's cancel answer to a tool-permission request is recorded with that cause; items a turn opened and did not complete are stated as not completed." | C-13, G-4 | R18-1 C-13; R18-7 G-4 | Kept as optional |
| **SC3-01-02-11 (C1-A, optional clarification)** | REQ-004, after the first sentence | "Return an explicit error for an unknown server request using the supplied protocol boundary." → append: "The explicit error is written at receipt by App-v4 `DEL-01-01`'s boundary; this slice records its result and keeps it in custody across observation loss and relaunch." | The Design accepts HOSTING §6.5's split and writes no error of its own (RECOVERY §1). As written, REQ-004 and OUT-001 ("including … unknown-request errors") read as if this slice wrote it, and REQ-009's owner list does not say otherwise. Lift to the stable claim; no requirement is weakened | RECOVERY §1 (U-14/F-01 closed); HOSTING-v0.9 §6.5; pass-2 C1-B §5.1 (U-14) | New |

### DEL-01-03

| ID | Location | Old → new | Reason | Source | Disposition |
|---|---|---|---|---|---|
| SC3-01-03-1 | TBD-001 | Append: "Owner decision D4 selected Codex 0.158.0 as the definition and generation pin, not a qualification; qualification remains with the Owner, who is also the App implementation owner (DECISION-L L-7), through DEL-01-01 (OI-012)." | D4, L-7 | D2 §6 and R2.4 | Kept (with D2's round-2 clause); enables R3-01-03-f |
| SC3-01-03-2 | CLM-004, AX-002, TBD-003 | "OI-001/002 remain open" → "decided for this scope by owner decisions D2 (reserved acts) and D3 (routine tool permission is the person's Codex setting); the rows stay OPEN for wider scope" | Overtaken | D2, D3 | Kept; enables R3-01-03-e |
| SC3-01-03-3 | REQ-005 | Add: "An act the App captures names the person as observed, marked 'identity not verified'." | K1-4 | NPTD §9 TA-4 | Kept (class of SC3-01-04-4, P-6) |
| SC3-01-03-4 | REQ-001, AC-001 | Add: "Plan revisions Codex does not keep in its history are not copied; after a relaunch or a supplier restart they are shown as not recoverable, while plan items are recovered from Codex history." | R17-4, C-03 | NPTD RV-4, CL-06/07 | Kept (with D2's round-2 clause) |
| SC3-01-03-5 | REQ-003 | Add: "Delegation by a task agent is recorded and shown, labelled 'stated, not enforced'; the App does not override the person's Codex configuration to prevent it." | K-10 | NPTD DR-4 | Kept. Duplicate in substance of SC3-02-04-4 (C1-B); keep one wording in each SoW |
| SC3-01-03-6 | REQ-004 (or a new REQ) | Add: "Experimental supplier surfaces the views use (at 0.158.0, plan mode) are labelled 'experimental' where they appear; the App remains fully usable without them, the corresponding views being absent." | K-5 as narrowed by C-05 | NPTD §4 | Kept |
| SC3-01-03-7 | REQ-005 | Add: "An instruction to carry out a plan is ordinary conversation input, not a reserved act, unless a workflow checkpoint names an act." | R17-9 | NPTD §5.5 | Kept |
| **SC3-01-03-8 (C1-A)** | CLM-003, after "…it owns work-graph, return, waiting and decision views." | Append: "This slice's plan-mode element, item anchors and delegation availability are received by App `DEL-01-04`, which composes turns and request cards from them; its delegation identities are received by App `DEL-06-01`; and its views and checks are received by `DEL-09-02` and `DEL-09-05` before their witnesses. Each declares it upstream in its own register." | Registers follow the SoW. NR-05's DOWNSTREAM mirror and the M-3 mirrors need a sentence naming the receivers; CLM-003 names PKG-06 only. D2 proposed the rows without an anchor | NPTD §10.2, §16.3; F0 §3 NR-05, M-3; S1-A §2.3 | New; enables R3-01-03-a…d |

### DEL-01-04

| ID | Location | Old → new | Reason | Source | Disposition |
|---|---|---|---|---|---|
| **SC3-01-04-1 (amended at C1-A)** | New REQ, with matching OUT, AC, VER | (none; supersedes pass-2 SC2-01-04-1) → see the text below | K-8 adds A15 and DEL-02-02; R17-6; L-4 as R21-3 rules it | DECISION-K1 K1-4; DECISION-K3 K-8; R17-2, R17-6; R21-3; AAC §1, §1.2, AI-2, AK-d | Kept, **with D3 round 2's L-4 clause corrected**. D3 R2.4 reads "on one or several reviewed workflow drafts in one act, each presented from the workflow workspace's descriptor". R21-3 withdrew that reading: one act is composed from one descriptor; several drafts are several acts (AAC AK-d); L-4's multi-entry act covers library entries registered in place. EXEC-v0.7 CAP-1/CAP-2 and ACT-v0.9's L-4 row already say so |
| SC3-01-04-2 | REQ-006 DEL-02-02 clause; CLM-004 | "the complete workflow-making workspace, reviewed registration and catalog selection belong to App `DEL-02-02` in CLM-004" → "the complete workflow-making workspace, the registration of a reviewed revision into the library and catalog selection belong to App `DEL-02-02` in CLM-004; the person's registration act (A15) is captured by this slice's App act control" | K-8 | AAC §4.2 | Kept (pairs SC3-02-02-4, C1-B) |
| SC3-01-04-3 | REQ-001, append | "Where a request lists the answer forms it accepts, only those are offered. The explicit decline is the request's own negative form or, for a kind that has none, the native empty answer this slice's design names. No App rule declines a waiting request after any period, and a request the supplier resolves itself is shown as resolved by the supplier, never as an answer." | R17-9; two kinds lack a negative form | NIR §4.2–§4.4 | Kept (pairs SC3-01-02-4) |
| SC3-01-04-4 | REQ-005, append | "The agent carrying out a workflow asks the person for a checkpoint's act; this slice offers the means to act as a standing facility and raises nothing because an arrival was recorded. An earlier act of the required kind on still-current content is shown as counting, with its time, and several acts may answer one arrival together. The person who acted is shown as the App observes them, marked identity not verified." | DECISION-K1 | NIR §8, §9; AAC | Kept |
| SC3-01-04-5 | OUT-002 append; CLM-001 | "…and the App's placement of the checkpoint overlay and standing facets defined by App `DEL-04-02`, with the checkpoint display meanings of App `DEL-02-03`, whose behaviour in the App this slice owns." | R17-7; anchors NR-08, NR-09 | NIR §9 | Kept |
| **SC3-01-04-6 (amended at C1-A)** | REQ-002, append | D3 R2.4: "A new conversation shows that no model is selected until the person chooses one; the person's last explicit choice for the project may be offered, and is never applied without the person's choice. A workflow run that cannot start for want of a model reads 'run not started — no model selected'; an ordinary conversation reads 'not started — no model selected'." → add after "chooses one": ", from the selection state App `DEL-01-05` reports"; and append: "The Codex account App `DEL-01-05` reports is the one used for the person's identity at act capture." | K-3, R18-2. **Amendment:** NR-07 (DEL-01-04 → DEL-01-05) needs a SoW sentence naming DEL-01-05; no D3 item names it | NIR §5.4, IF-10; AAC §7; F0 NR-07 (= D3 NR-3 = D4 NR-1) | Kept, amended (duplicate in substance of P-4 on DEL-01-05's side, C1-B) |
| SC3-01-04-7 | REQ-002, append | "Interrupting a turn, ending a run and stopping the Codex process are shown as distinct, as App `DEL-01-02` defines them; an interrupted turn is never shown as an ended run." | R17-3 | NIR §5.2 | Kept. **Optional clause at C1-A:** "The App offers Stop Codex and Restart Codex, each asking first when work is live." (R18-1 C-12; pairs the SC3-01-02-3 completion) |
| SC3-01-04-8 | VER-005, positive case | "…the person actually performs the act on identified content…" → "…the person actually performs the act on identified App content through the App act control…" | Names the construction | AAC; EXEC CH-23 | Kept |
| SC3-01-04-10 | OUT-001 / REQ-001, append | "This slice composes the turns it sends, including the collaboration mode supplied by App `DEL-01-03` (sent explicitly after plan mode was used) and the run-start text supplied by App `DEL-02-02`." | C-06, R19-7; anchors NR-05 | NIR §5.6 | Kept. Consider also naming "the run-end line" (R20-3; NIR TC-2), which `DEL-02-02` words |
| **SC3-01-04-11 (amended at C1-A)** | REQ-002, append | D3 R2.4: "A new conversation offers the roles App `DEL-02-04` lists, with the registry's default preselected and clearable and no role allowed; the role is fixed for the conversation, and a different role opens a new conversation with a handoff summary the person can edit. An agent's proposal of the next workflow is offered for the person to confirm and starts nothing by itself." → append: "An agent's report that the workflow finished is offered as the person's 'End run' and ends nothing by itself." | C-15, R19-2 (b), R19-3, L-2. **Amendment:** R20-1 and R20-9 added the finished line and its offer after D3 wrote the item (NIR RN-7, RX) | NIR §5.4, §5.7, §5.8 | Kept, amended; anchors D3 NR-4 |
| SC3-01-04-12 | REQ-001, append | "The App shows how many requests wait for the person's answer, also when no conversation window is open." | C-24 | NIR §4.8 | Kept |
| **SC3-01-04-13 (C1-A)** | CLM-001, after "…with the plan/tool/delegation contribution assigned to App `DEL-01-03`." | Append: "This slice's native interaction view and scoped request/outcome checks are received by App `DEL-09-02` before its joined request witness, as `DEL-09-02` declares in its own register." | DEP-09-02-012 has no mirror and no SoW sentence here (§4 above) | Register script; NIR §2 IF-12; S1-B A.2.2 | New; enables R3-01-04-b |

**SC3-01-04-1, full text as amended here** (the new REQ; OUT, AC and VER
follow it, as SC2-01-04-1 asked):

> Provide the App act control: a dedicated control that only the person can
> operate — no agent tool, MCP operation, App rule, supplier request or
> interface script can operate it or produce its record — for one act kind at
> a time on App content. It covers App files and outputs, and A12 where an App
> control establishes the setting. It also covers A15 (register workflow
> revision), either on one reviewed workflow draft or on two or more library
> entries registered in place in one act. A15 is presented from one descriptor
> of the workflow workspace and bound to the exact reviewed content of each
> entry, so that a draft or entry changed after review needs a new review. The
> control shows the act kind in its canonical wording, the bound subject with
> its content identity, the declared scope and purpose, the actor requirement
> and the arrival it answers. It offers the decline where an act-declined event
> exists. Operating it produces capture evidence and a direct-capture
> human-act record in `DEL-04-03`'s format. It is a standing facility,
> available whether or not an arrival has been recorded, and no arrival raises
> it. It records the person's identity from what the App can observe (the name
> set in the App, the operating-system account, and the Codex account when
> Codex reports one), marked *identity not verified*. Presenting or operating
> it answers no pending supplier request. Consumers: `DEL-02-02` (A15),
> `DEL-02-03` (App-side positive capture fixtures), `DEL-04-03`, `DEL-04-01`.

The process placement that makes "not operable by automation" true stays with
OI-008 (AAC §6.2 P-2 PROPOSED; P-3 not adopted, L-5).

## Proposed register items (none applied)

| ID | Register | Row / change | Class | Follows |
|---|---|---|---|---|
| R3-01-02-a (M-1) | DEL-01-02 | DOWNSTREAM INTERFACE → DEL-01-03 (mirror of DEP-01-03-012) | mirror only | SC3-01-02-8 |
| R3-01-02-b (M-2) | DEL-01-02 | DOWNSTREAM HANDOVER → DEL-09-02 (mirror of DEP-09-02-010) | mirror only | SC3-01-02-8 |
| **R3-01-02-c (C1-A)** | DEL-01-02 | DEP-01-02-021 Statement: "…; OI-001/OI-002 choices remain with the owner and App/SWB contract owners." → "…; for this scope OI-001 and OI-002 are ruled by APP-V4-FIRST-INCREMENT-20260928-DECISION-1 D2 and D3 (no App rule answers a tool-permission request affirmatively; ACT V-21), and matters beyond those rulings remain with the owner and App/SWB contract owners." | non-topological | SC3-01-02-5 |
| **R3-01-02-d (C1-A, optional)** | DEL-01-02 | DEP-01-02-018 Notes, append an UPDATE: D4 selected 0.158.0 as the definition and generation pin; the qualification pin stays open (OI-012) | non-topological | SC3-01-02-6 |
| **R3-01-02-e…h (C1-A, conditional)** | DEL-01-02 | DOWNSTREAM rows mirroring F0 NR-01 (DEL-02-03), NR-02 (DEL-03-03) and, if adopted, NR-03 (DEL-09-09) and NR-04 (DEL-02-02) | mirror only (each on a new admitted arc) | SC3-01-02-8 completion |
| R3-01-03-a…c (M-3) | DEL-01-03 | DOWNSTREAM rows mirroring DEP-06-01-007, DEP-09-02-011, DEP-09-05-008; DEP-01-03-014 (package) may stay | mirror only (3) | SC3-01-03-8 |
| R3-01-03-d (NR-05 mirror) | DEL-01-03 | DOWNSTREAM INTERFACE → DEL-01-04 (plan-mode element, item anchors, availability) | mirror only (of NR-05) | SC3-01-03-8 |
| **R3-01-03-e (C1-A)** | DEL-01-03 | DEP-01-03-017: give it SCA-V4-002's treatment of DEL-01-04's twin rows. Refresh it in place to the OI-001 residue ("any reserved-act matter DECISION-1 D2 does not cover; OI-021 additions"). Record OI-002 as ruled by D3: split and retire, or note it, at extraction's choice | non-topological | SC3-01-03-2 |
| **R3-01-03-f (C1-A, optional)** | DEL-01-03 | DEP-01-03-011 Notes: D4 pointer, as R3-01-02-d | non-topological | SC3-01-03-1 |
| F0 NR-05 | DEL-01-04 | UPSTREAM INTERFACE → DEL-01-03 (plan-mode element, item anchors, delegation availability) | **new arc**, admitted, SCC-free (R18-1 C-06) | SC3-01-04-10 |
| F0 NR-07 | DEL-01-04 | UPSTREAM INTERFACE → DEL-01-05 (selection state for the start display; Codex account for K1-4) | **new arc**, admitted, SCC-neutral (= D3 NR-3 = D4 NR-1) | SC3-01-04-6 (amended) |
| F0 NR-08 | DEL-01-04 | UPSTREAM INTERFACE → DEL-04-02 (K-5/K-6 components and display meanings) | **new arc**, held (SCC-002), membership unchanged; AS-v0.9 §12 already names DEL-01-04 (FS-02) | SC3-01-04-5 |
| F0 NR-09 | DEL-01-04 | UPSTREAM INTERFACE → DEL-02-03 (SD-1…SD-5, arrival references) | **new arc**, held, membership unchanged | SC3-01-04-5 |
| D3 NR-4 | DEL-01-04 | UPSTREAM INTERFACE → DEL-02-04 (role list with `default_for_new_chat`, role composition for Continue as, the guidance-changed signal) | **new arc**, held, membership unchanged (after F0; checked by V21-A, V21-B and here) | SC3-01-04-11 |
| F0 M-7 = pass-2 R2-01-04-a | DEL-01-04 | DOWNSTREAM HANDOVER → DEL-02-03 (mirror of DEP-02-03-027, X-1, held) | mirror only | SC3-01-04-1 (consumer list) |
| **R3-01-04-b (C1-A)** | DEL-01-04 | DOWNSTREAM HANDOVER → DEL-09-02 (mirror of DEP-09-02-012) | mirror only | SC3-01-04-13 |
| F0 ST-1 = SC3-01-04-9 | DEL-01-04 | DEP-01-04-010 Statement: "Supply native attachment and draft-transition receiving interactions, together with the receiving contract, to App DEL-02-02 …" → add "and the App act control that captures workflow registration (A15)" | non-topological | SC3-01-04-1, -2 |
| R3-01-04-a (D3 R2.5, corrected at C1-A) | DEL-01-04 | DEP-01-04-009 Statement: "Receive source-qualified draft identity and actual draft/registration/collision/refusal transitions from the workflow workspace for native presentation." → append "the A15 descriptor from which the App act control composes a registration offer (one per act: one reviewed draft, or two or more library entries registered in place), and the run-start text and run-end line placed in the turns this slice composes." D3's "A15 descriptors per entry" is replaced (R21-3) | non-topological | SC3-01-04-1, -10 |

Counts: 23 items in these three registers. 12 are mirror only (4 of them
conditional), 5 are new arcs (NR-05 and NR-07 admitted; NR-08, NR-09 and D3
NR-4 held) and 6 are non-topological.

**Rows in other registers that name these deliverables** (owners elsewhere;
listed for deduplication):

- F0 NR-01: DEL-02-03 → DEL-01-02, new admitted arc.
- F0 NR-02: DEL-03-03 → DEL-01-02, new admitted arc.
- F0 NR-03 (optional): DEL-09-09 → DEL-01-02, new admitted arc.
- F0 NR-04 (optional): DEL-02-02 → DEL-01-02, new admitted arc (C1-B's
  register).
- F0 ST-2: the DEP-02-02-013 statement (C1-B).
- Pass-2 SC2-02-03-5 and R2-02-03-j: DEL-02-03's act-control and identity
  wording, which SC3-01-04-1 makes true.
- Pass-2 SC2-04-03-1: DEL-04-03 REQ-005 names DEL-01-04 among its consumers.

**SCC and guard, recomputed here** (Tarjan over DAG-003
`DependencyEdges.csv` 124 admitted and `CandidateEdges.csv` 78 held arcs,
ACTIVE deliverable targets, consumer → supplier):

- **Base:** six SCCs, sizes 2, 2, 2, 2, 3, 13. The admitted layer alone is
  acyclic.
- **With NR-01…NR-05, NR-07…NR-09 and D3 NR-4:** singly, in all 36 pairs and
  all together, the SCC set is unchanged. The admitted layer plus the six
  admitted proposals stays acyclic.
- **Guard (R17-10):** DEL-01-02 reaches only DEL-01-01, DEL-01-05 and
  DEL-04-01; DEL-01-03 reaches those three and DEL-01-02. Neither reaches
  DEL-01-04, DEL-02-02, DEL-02-03, DEL-04-02, DEL-04-03 or DEL-06-01.
- **Mirrors:** no mirror or statement item adds an arc. A new admitted arc is
  a `project-dag` departure.

## Basis items

None proposed. Considered:

- **R17-3's three stop operations against V4-EXE-01** ("stopping work is an
  explicit act"). DEF-3 and DEF-6 are both explicit, so the basis reads
  without change.
- **K-10's doctrine notice** (Root `AGENTS.md`, "does not veto the user's
  Codex configuration"). It no longer applies after the revision (no
  override), and it is not these deliverables'.
- **OI-001/OI-002 rows in `_Decomposition/Open_Issues.csv`.** They stay OPEN
  for wider scope, as SC3-01-02-5 and SC3-01-03-2 say.

## Pass-2 proposals naming these deliverables: superseded, kept or changed

| Pass-2 item | Source | This run's disposition |
|---|---|---|
| **SC2-01-04-1** (DEL-01-04 act control; C1-B X-1 dropped as its duplicate) | C1-A; CLOSEOUT_ACCOUNT | **Superseded by SC3-01-04-1** (changed). It adds A15 on reviewed content from one workflow-workspace descriptor (K-8; L-4 as R21-3 rules it), DEL-02-02 as consumer, "interface script" among the excluded operators, and "presenting or operating it answers no pending request". It also replaces SC2-01-04-1's parenthetical "(and A12 where an App control establishes the setting)" with the enumerated subjects (App files and outputs; A12; A15). D5's SC3-02-02-8 (consumer list and A15 added to SC2-01-04-1) is subsumed. ACT §2.6, EXEC and GUIDE name it "SC2-01-04-1 as amended by SC3-01-04-1" (RV21-B m-9 row 10) |
| R2-01-04-a (DEL-01-04 DOWNSTREAM → DEL-02-03, mirror of X-1) | C1-A | **Kept** = F0 M-7 |
| "Outside mirrors noted, not proposed (D1)": DEL-04-01 → DEL-01-02, 01-04; DEL-04-03 → DEL-01-04 | C1-A | **Kept as noted.** Both sides are now defined (RECOVERY §4.2; NIR IF-6, IF-7), but the rows sit in DEL-04-01's and DEL-04-03's registers, outside this node |
| SC2-02-03-5, R2-02-03-j (DEL-02-03 statements of the act control and K1-4 identity) | C1-A | **Kept**, related; SC3-01-04-1 makes the statement true |
| SC2-04-03-1 (DEL-04-03 REQ-005 consumers incl. DEL-01-04) | C1-A | **Kept**, related |
| C1-B §5.3 "Seams S-1…S-4 have no receiving comparison" | C1-B | **Resolved for S-1…S-3.** S-1 is RECOVERY-v0.2 §1 and §4.2, S-2 NPTD §2, S-3 NIR §4–§6 with AAC. HOSTING-v0.9 F-15 is closed (FH-19; V21-B m-8 relabelled S-1) |
| C1-B §5.1 U-14 (unknown-request split "waits for DEL-01-02") | C1-B | **Resolved** by RECOVERY §1 (HOSTING §6.5 accepted) and HOSTING-v0.9; the SoW pointer is SC3-01-02-11 (optional) |
| C1-C "DEL-01-04 act-control obligation … C1-A's" | C1-C | Same item as SC2-01-04-1, now SC3-01-04-1 |

## Raised in this run and not proposed (with disposition)

| Item | Source | Disposition |
|---|---|---|
| DEL-01-05 → DEL-01-02 (live-work list for sign-out and key removal) | D4; D1 §9 | Not proposed: it forms {DEL-01-01, DEL-01-02, DEL-01-05} (F0 §3; recomputed). It is a runtime value instead (`assess live work`, RECOVERY §4.1; ACCESS AE-12) |
| DEL-02-04 → DEL-01-03 (F0 NR-06) | D2 round 1 | Dropped by R18-1 C-07; the K-10 label is a runtime value |
| DEL-01-03 → DEL-02-04, DEL-01-02 → DEL-02-04, DEL-01-02/01-03 → DEL-01-04 | D1, D2, D6 | Not proposed: each changes an SCC (F0 §3; V21-B check 6) |
| DEL-01-04 SoW sentence on attachment carriers and standings (R21-2) | V21-A M-2 | Not warranted: REQ-003 already requires the identity carried and the observation available; the carriers are design detail (lift rule) |
| SoW reading of "reconnect" (RECOVERY DEF-2: no third connection) | RECOVERY §2 | Not warranted: AC-005's wording admits it |
| `_CONTEXT.md` of the three lack an "as amended" sentence | this comparison | No change: SCA-V4-002 edited `_CONTEXT.md` only where the Deliverables row changed (pass-2 C1-A precedent) |

## Returned to the graph (Design residuals, not proposals)

- **G-A1 — RECOVERY U-R6 is stale.** U-R6 ("Whether RS records a turn
  interrupt in an App run") is still listed open, point of need "Node F or
  later". RS-v0.9 §10's DEL-01-02 row now answers it: "a turn interrupt is
  not recorded in format 0.1 (§3)". The §8.2 stop-request row should cite
  that. **Fix:** close U-R6 at RECOVERY's next touch. Wording only.
- **G-A2 — RECOVERY U-R5 is partly answered.** Its point of need was "before
  DEL-01-04's design". NIR §4.8 WI-4 now settles several windows for request
  cards (the first answer written settles; another window's answer is
  refused `already-settled`). No file says whether two windows may both show
  the stop control. **Owner:** DEL-01-04 (NIR §5.2), with RECOVERY SR-11,
  which already refuses a second stop. A one-line NIR rule closes it.
- **G-A3 — V21b-A N-2 (WR TT-3 vs NIR AT-8): closed by C0.** NIR AT-8
  already followed R21-5. C0 (committed at `61e7a0afec` while this node ran)
  rewrote WR TT-3 to attach the draft's `WORKFLOW.md` as a text element "exactly
  as NIR-v0.2 §6 AT-8 says" (`closeout/C0.md`). Nothing further for these
  deliverables.
- **G-A4 — The new rows into DEL-01-02 have no SoW anchor on the consumer
  side.** F0 NR-01…NR-04 are proposed rows in DEL-02-03's, DEL-03-03's,
  DEL-09-09's and DEL-02-02's registers, and those registers follow their
  SoWs. No ScopeOfWork item in this run names DEL-01-02 in those four SoWs.
  EXEC §2.7, ADAPTER PI-6, XT XC-06 and WR SQ-X rely on it in Design only.
  **Needed at the SCA-V4-003 node:** a SoW sentence for each adopted row (DEL-02-02's
  is C1-B's to propose; DEL-02-03, DEL-03-03 and DEL-09-09 are outside both C1
  nodes), or drop the row and keep the Design reliance labelled as such.
- **G-A5 — Bookkeeping.** DEL-01-02 and DEL-01-03 have no `MEMORY.md`. The
  MEMORY step creates them with this run's entry (DEL-01-04's exists).

Every other open item has a home: an UNRESOLVED row with its owner and point
of need, OI-008 at the phase review, the version-advance check (R19-5, not
scheduled), or a proposal above. No Task Management intake.

## Pointers for the MEMORY run entries (final PR)

One terse entry per deliverable, e.g. "2026-10-02 — APP-V4-DESIGN-PASS-3-20261001
(third design pass): first Design files, developed to ‹version› with PROPOSED
schemas and local prototypes; draft definitions only — no implementation,
lifecycle, register or SoW change. Receipt: ‹run RECEIPT›; proposed SoW and
register changes in `closeout/C1-A.md`."

- DEL-01-02: RECOVERY-v0.2. New `MEMORY.md`.
- DEL-01-03: NPTD-v0.2. New `MEMORY.md`.
- DEL-01-04: NIR-v0.2 and AAC-v0.2. Add a row to the existing `MEMORY.md`.

## Checks performed and limits

- **Method.** Each OUT, REQ, AC and VER of the three ScopeOfWork files was
  traced into the Design sections, and each structure the Design adds was
  traced back to its ruling or decision. The Design headers' SoW and register
  pins equal the current bytes. DAG-003 `SOURCE_MANIFEST.sha256` checks
  130/130 OK.
- **Design files compared.** RECOVERY and NPTD were read whole. NIR and AAC
  were read whole. The D returns were read in their proposal, row, join and
  round-2 sections. F0 §3–§4 were read whole. V21-A, V21b-A and V21b-B were
  read in full for these files; V21-B by grep. F-A…F-E2, RX and RV21-A/B were
  read by grep for these deliverables. The first-increment joins were
  spot-checked in HOSTING-v0.9, EXEC-v0.7, RS-v0.9, AS-v0.9 and ACT-v0.9:
  DEF-3/4/5/6 cited, U-10 closed, R13's two settlements, AS §12's DEL-01-04
  receiver, ACT FA-01/FA-02 and the L-4 row.
- **Registers.** All ACTIVE rows of the three registers were printed. Mirror
  coverage was computed by script over every `Dependencies.csv` in the
  project; it found DEP-09-02-012's missing mirror. SCC and reachability were
  recomputed (above).
- **Prototypes.** The three prototypes were rerun on 2026-10-02 from `git
  archive HEAD` into a scratch folder, with Python 3.13.7, `-B` and
  `PYTHONDONTWRITEBYTECODE=1`:
  - RECOVERY `run_cases.py`: "16 results, 16 as expected, 0 not";
  - NPTD `run_cases.py`: "SUMMARY 18/18";
  - NIR/AAC `run_cases.py`: "151 checks, 0 failed".

  All three exited 0. No file in the worktree was written by the reruns. At
  the end, `git status` shows only this file, untracked; C0 and C1-B had been
  committed meanwhile.
- **Not done.**
  - No re-review of design content beyond these comparisons.
  - No check that the proposed wording is final.
  - The coverage ratings are this reader's at the 60% definition level; no
    case has run against an App candidate, and nothing here is
    qualification.
  - Read-only git; no network; no Codex or model run. No file other than this
    one was written.
