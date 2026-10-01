# C1-B — bounded closeout comparison: DEL-03-01, DEL-03-02, DEL-03-03, DEL-03-04, DEL-01-01

- Node C1-B of run `APP-V4-DESIGN-PASS-2-20260930`. Method:
  `chirality-root:bundled:workflow:bounded-reconciliation`
  (`workflows/bounded-reconciliation/WORKFLOW.md`, sha256 `c7798c0ae598…`,
  read whole). Executor: Type 2 TASK (Claude Code subagent, Claude Opus 5.5),
  no delegation, read-only git, no network. Scratch under `$TMPDIR/c1b`.
- Brief: `BRIEFS.md` "Common rules" and "C1 — bounded closeout" (read in the
  working tree, sha256 `843142224351…`; the C1 section is the one committed
  at `41899194c4`). Owner direction: `OWNER_DECISIONS.md` `b2fa81871cbf…`
  (DECISION-K1; executor model; OBS-1 and OBS-1b answers). Precedent read:
  `../APP-V4-FIRST-INCREMENT-20260928/closeout/C1-B.md` and
  `CLOSEOUT_ACCOUNT.md`.
- **Candidate: commit `a9046631c0`.** Every deliverable file below was read
  with `git show a9046631c0:<path>`. HEAD moved to `41899194c4` during this
  node (PR-2 merged as `d01ad98a75`; node C0 committed). `git diff
  a9046631c0 41899194c4` touches, among my files, only HOSTING (§6.8
  preamble and first row, a change row) and GUIDE (pin provenance, §4.5,
  F-17 wording, the 18-row pins). No ScopeOfWork, register, `_STATUS.md`,
  schema or prototype changed. The commitments compared below are the same at
  both commits.
- **Boundary (BRIEFS "C1", binding).** DAG-003's `SOURCE_MANIFEST` binds every
  `ScopeOfWork.md`, `Dependencies.csv` and `_DEPENDENCIES.md`. This node
  applies **no change** to them, to `_STATUS.md`, `_CONTEXT.md` or
  `_REFERENCES.md`, or to any Design file. Every warranted change is returned
  as a proposal (file, locus, old → new, reason, source) for a later amendment
  and a `dependency-extract` run. Nothing here is applied.
- **Labels used.** *States* = the file says it. *Inference* = my reading.
  *Developed* = the 60% definition is present and what remains is
  implementation, qualification, a host input or a witness. *Partial* = a
  definitional choice or agreement the definition must carry is still open.
  Arcs are written consumer → supplier, as in DAG-003.

| DEL | ScopeOfWork.md | Dependencies.csv | `_STATUS.md` | Design files at `a9046631c0` (sha256, 12) |
|---|---|---|---|---|
| DEL-03-01 | `9ada531b59a6` (SCA-V4-001) | `930796b5f1b8` | IN_PROGRESS (2026-09-28) | C-v0.8 `CATALOG_AND_READ_BASIS.md` `118f48108287` (1,497 lines); schemas `catalog` `24d7db75d66f`, `edition_change_event` `c0244a57a696`, `read_result` `5f71d7184bd3`; 13 instances; `prototype/` (SH-1) |
| DEL-03-02 | `3560915142eb` (SCA-V4-001) | `226380332f36` | IN_PROGRESS | P-v0.8 `PROPOSAL_LIFECYCLE_AND_OUTCOMES.md` `f432356d054c` (1,276); schemas `proposal` `2c81bab4a725`, `proposal_state` `222de733c7df`; 7 instances; `prototype/proposal_states.py` |
| DEL-03-03 | `93faf918ce5d` (SCA-V4-001, SCA-V4-002) | `be53fc728070` | IN_PROGRESS | ADAPTER-v0.6 `ADAPTER_ENABLEMENT_AND_RECEIVING.md` `7cad04c873c0` (1,783); schemas `channel_status` `49f3475c10b4`, `checkpoint_observation` `5d17aa548789`, `external_dispatch_record` `726d8787d1b9`; 8 instances; `prototype/observe_map.py` |
| DEL-03-04 | `895f004e4d0f` (SCA-V4-001) | `977d8712e02b` | IN_PROGRESS | GUIDE-v0.5 `HOST_INTEGRATION_GUIDE.md` `4b4d43b9563e` (1,045) |
| DEL-01-01 | `9945e72b04b4` (SCA-V4-001, SCA-V4-002) | `9fdb3ce3d8c1` | IN_PROGRESS | HOSTING-BOUNDARY-v0.8 `9018828b31f3` (1,773); `PIN_SPIKE_0.158.0.md` `0e090a4ca14e` (unchanged since 2026-09-28); `OBS_1_0.158.0.md` `85707703e97b` (dated record, OBS-1 and OBS-1b); three `hosting.*.schema.json`; `prototype/` (supplier double; `obs1/` harnesses); `generated/0.158.0/` |

**Checks run by this node (2026-09-30, Python 3.13.7, macOS).**

- Prototypes rerun from the candidate bytes (`git archive a9046631c0` into
  scratch; nothing written in the repository): C `run_fixture.py` **22 of 22**
  checks passed; `validate_all.py` "all checks passed" (30 host documents, 6
  change requests); P `proposal_states.py --check` "all checks passed"; ADAPTER
  `observe_map.py` "all checks passed" (34 dispatch, 11 checkpoint
  observations, 14 channel statuses; 48 of 48 RS entries valid); HOSTING
  `run_cases.py` **TOTAL 35, pass (model) 35, FAIL 0**. All are *test-double*
  or *model* evidence (the files say so); none is host, candidate or Codex
  evidence.
- Register joins computed by script over all 41 `Dependencies.csv` at the
  candidate (ACTIVE EXECUTION rows; counterpart = the opposite-direction row
  in the other register). Arcs checked against `_DAG/DAG-003/CandidateEdges.csv`
  and `DependencyEdges.csv`.
- Term checks by `grep -c` on the five SoWs (for example: "edition" 0 in all
  five; "destination" 0 in DEL-03-01 and DEL-03-02; "harness" in DEL-01-01
  only as "third-party harness" and "second harness").
- Every run file named in the brief was searched for proposed ScopeOfWork,
  register or basis items (`WAVE_A/*`, `WAVE_B/*`, `comparisons/*`,
  `reviews/*`, `SURVEY/*`, and the R9–R15 rulings for decisions that bear on
  the contracts). Sources are cited per item in §8.

## Summary

| DEL | OUT developed / partial | SoW proposals | Register proposals (mirror rows in brackets) | Lifecycle (no change made) |
|---|---|---|---|---|
| DEL-03-01 | 2 / 1 (OUT-002 partial) | 5 (3 need an owning decision) | 3 (11 rows) | IN_PROGRESS; truthful |
| DEL-03-02 | 3 / 0 | 2 (1 optional) | 4 (7 rows; 1 optional row) | IN_PROGRESS; truthful |
| DEL-03-03 | 2 / 1 (OUT-001 partial) | 5 (2 optional) | 6 (4 rows; 2 optional rows) | IN_PROGRESS; truthful |
| DEL-03-04 | 2 / 1 (OUT-002 partial) | 3 (1 optional) | 2 | IN_PROGRESS; truthful |
| DEL-01-01 | 2 / 2 (OUT-002, OUT-003 partial) | 2 (1 optional pointer) | 3 (10 rows) | IN_PROGRESS; truthful |
| Cross-deliverable (DEL-01-04, raised in GUIDE G-1) | — | 1 | — | — |
| **Total** | 11 / 5 | **18** | **18** (32 mirror rows) | — |

Basis items: 3, none with proposed text (§7). New arcs: **none**. Every
proposed row lies on an arc DAG-003 already holds or admits (checked).
Returned to the graph as missing work, not as a proposal: **one** stale
statement in GUIDE, and one redaction point in DEL-01-01's observation
record (§9).

Against the first increment's C1-B, SCA-V4-001 and SCA-V4-002 applied all 24
of its SoW corrections and its arcs N-B3, N-B4, N-B7, N-B9, N-B10 and N-B11
(states: SoW AX-004/AX-005/AX-006; registers DEP-03-02-027, DEP-03-03-013,
-014, DEP-03-04-021…023). N-B1 was applied as DEP-03-01-031. N-B2 (DEL-03-02 →
DEL-04-02), N-B5 (DEL-03-03 → DEL-04-02) and N-B6 (DEL-03-03 → DEL-02-01)
exist only as supplier rows (DEP-04-02-021, DEP-04-02-022, DEP-02-01-027). N-B8 is
absent by decision (BASIS-ALIGN DECISION-6). Its 33 mirror rows are still
mostly absent (DAG-003 HANDOFF_STATE open matter "Deferred supplier-side
mirror rows").

---

## 1. DEL-03-01 — Capability catalog and read-basis contract (C-v0.8)

### 1.1 Commitment → result

| SoW item | Design sections | Standing | What remains (kind) |
|---|---|---|---|
| OUT-001 CONFIG catalog and read-basis schemas | §2, §2.1 (CI-1…CI-5), §2.2, §3, §3.1–§3.5, §4, §5, §6; three PROPOSED JSON Schemas with valid and invalid instances | **Developed** | Wire names, identity algorithm and placement stay unselected by design (TBD-003; U-C1; OI-014). Host adoption of the catalog-level interface (U-C15) is a host input |
| OUT-002 DOC three-surface responsibility map | §8 | **Partial** | Every H/E/X cell is still *unagreed* (states §8; GUIDE F-8). Needs host agreement (DEP-03-01-025, deferred by DECISION-3) and `UNRESOLVED{OI-003}`, `{OI-014}`, `{OI-013}` |
| OUT-003 TEST fixtures and comparison evidence | §9, §10 (FX-PIPE-01), §10.8 (SH-1), VC-C-01…10 | **Developed** (designed; part run on a test double) | VC-C-04, -09, -10 and the X-path parts of VC-C-02/-03 run on SH-1 (*test-double*). H and E channels not run; no App candidate, so AC-004 stays **held** (states VC-C-04, U-C8) |
| REQ-001 one catalog, three consumers | §2 invariants; §2.1 CI-1 per surface; SQ-C1 | Developed | Host conformance |
| REQ-002 entry fields; class; exposure | §3 (nine elements), §3.1, §3.4, §3.5 | Developed | Consequence vocabulary is a PROPOSED draft in ACT §8.5, assigned to no record (ACT U-02); OI-021 additions |
| REQ-003 read and unavailable parity | §4.1–§4.4; §2.3 CF-1…CF-5; §6.1 | Developed | Host evidence |
| REQ-004 full basis; subject identity; relied-on basis | §5.1–§5.4; schema `basis_descriptor` | Developed, **with one result beyond the text** (R13-1, §1.2) | Host definitions U-C2, U-C3; SWBPIPE has whole-model identity only (U-C12) |
| REQ-005 standing; act separation | §6.2–§6.4 | Developed | — |
| REQ-006 map; extension promise kept | §8 | Partial (as OUT-002) | Owner disposition OI-003 |
| REQ-007 no foreign acts | §1 | Developed | — |
| AC-001…AC-008 / VER-001…VER-008 | VC-C-01…VC-C-10, one to one plus VC-C-09/-10 | Designed; four partly run | VER-001's "candidate schema identity" now has an object (`$id` URNs of the three PROPOSED schemas), but no adopted candidate. AC-004 held |

### 1.2 Result → commitment

| Result in C-v0.8 | Where | Authority the file cites | Supported by a commitment? |
|---|---|---|---|
| Catalog as an interface: discovery, edition identity rules, edition-change event, offering record, basis profile | §2.1 CI-1…CI-5, EI-1…EI-5; §2.2; `edition_change_event.schema.json` | PROPOSED (S1-B C 5; R12-1) | **Not named.** Neither the SoW nor V4-HI-02 names a catalog edition (grep: 0). Four consumers rely on it (WD §4.2, EXEC §3.2, LOOP, XT §4; S1-B C25) and DEP-05-01-014 asks for "catalog identity". Proposal S-01-3 |
| External-contact declaration (element 5) and the *destination request* entry kind; two non-success rows "destination not allowed" and "destination not allowed by the person" | §3.4, §3.5, §4.1; `catalog.schema.json` | PROPOSED (node B5), resting on PRD V4-HOST-02 as amended (DECISION-5) and LOOP §5.3 | **Not named.** The SoW does not mention network destinations or DECISION-5 (grep 0); AX-004 cites DECISION-1 only. Proposal S-01-2 (B5 §7 proposed it) |
| A read lacking workspace identity or generation is citable when the host declares it supplies neither, with the limit "basis lineage not supplied" | §5.2 rule 1 exception; schema `not_supplied` marker | R13-1 (INTEGRATION) | **In tension with REQ-004 and AC-004**: REQ-004 says every read "shall carry the workspace identity, generation, model revision and canonical content hash"; AC-004 says "carry all four basis elements for every fixture read". *Inference:* R13-1 is receiving behaviour for a host that does not meet V4-HI-11 (SWBPIPE main, SQ-07), parallel to REQ-004's existing whole-model clause. That clause is in the SoW; this one is not. Proposal S-01-4 (owning decision) |
| JSON Schemas as conformance fixtures of meaning | §0; three schemas | R12-1, R12-2 | Within OUT-001 ("schemas"); the SoW does not say they select no wire. Proposal S-01-1 (clarification) |
| Simulated host SH-1, one test double for C, P, ADAPTER, XT, CA | §10.8; `prototype/` | R12-4 (integration assignment) | Like FX-PIPE-01, an integration assignment the file says "does not extend DEL-03-01's SoW scope". Custody is an owner item (DECISIONS_PENDING Part 3, "custody of the shared example"). Proposal S-01-5 |
| Read-result content model (RR-1…RR-4), named host checks (element 6), "accepts a requested basis" (element 3), currency transitions, historical reads | §6.1, §3.4, §6.3, §6.4 | PROPOSED (S1-B C 4, C 5) | Supported: REQ-003/REQ-005 (tables, results, diagnostics, standing) and OUT-003 ("current and historical reads"). Sub-elements of existing REQ-002 elements; no SoW change |
| Catalog-level failure rows CF-1…CF-5; sequences SQ-C1…SQ-C6 | §2.3, §7.1 | PROPOSED | Supported by REQ-003 and OUT-001 |

Every result is labelled with its authority; none is presented as accepted.

### 1.3 What the 60% description still lacks

LOOP_INIT asks for interfaces, states, data, sequences, failure behaviour,
verification, and a route to completion with no further structural change
anticipated. At C-v0.8 the first five are present (PROPOSED). What is still
missing:

- **The responsibility map has no values** (OUT-002; §8 cells *unagreed*). It
  records host agreement, and host joins are deferred (DECISION-3).
- **Structural choices still open**: OI-014 placement of the schemas and any
  shared checker; OI-003 extension promise (a narrowing would act through
  element 9 and §8); custody of FX-PIPE-01 and SH-1. All three are owner
  phase-review items (DECISIONS_PENDING Part 3).
- **First host has no catalog** (U-C13): no editions, no per-operation
  identity, no exposure element. The catalog-level interface is exercised on
  SH-1 only (U-C15).
- **Verification**: H and E channels not run; AC-004 held until a
  candidate-bound M3-CP return exists.
- OP-C10's class form is unresolved (§3.5 NOTE, V18-3 n-2); nothing relies on
  it yet.

### 1.4 Proposed ScopeOfWork changes (`DEL-03-01/ScopeOfWork.md`)

| # | Locus | Current text | Proposed text | Grounds; route |
|---|---|---|---|---|
| S-01-1 | OUT-001, last sentence | "The schema contract supplies the later-action basis reference meaning without choosing an unsupported wire representation." | Keep, and add: "Schemas may be written as conformance fixtures of these meanings (for example JSON Schema with valid and invalid instances); such a fixture selects no host or supplier wire field, transport, identity algorithm or placement (TBD-003; OI-014)." | R12-2; B3 §6; A1-B #7. Clarification, no scope change |
| S-01-2 | OUT-001 element list; REQ-002 element list; AX (new entry) | REQ-002: "…human-act/autonomy class drawn from the adopted operation policy; and host-declared exposure per consumer surface, independent of class." | REQ-002: "…; host-declared exposure per consumer surface, independent of class; and, for an entry through which a host's embedded agent reaches a network destination, a host-declared external-contact declaration (destination category and form). The catalog also carries the host's destination-request entry, through which its agent asks the person for a destination, and the non-success results for a destination that is not allowed." OUT-001 gains the same two items. New AX entry naming `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-5` and PRD V4-HOST-02 / ARCHITECTURE V4-ARC-12 as amended by SCA-V4-001 | C §3.4, §4.1 (node B5); B5 §7 ("Proposed later items: DEL-03-01 OUT-001 to name the external-contact declaration and the destination request entry kind"); LOOP §5.3 relies on it. **Scope addition: owning decision** |
| S-01-3 | OUT-001 opening; REQ-001 | OUT-001: "CONFIG: catalog and read-basis schemas expressing stable operation identity/version, …" | OUT-001: "CONFIG: catalog and read-basis schemas expressing the identity of the catalog edition a consumer discovered and the event by which a host reports a new edition, stable operation identity/version, …". REQ-001 adds: "Consumers resolve operation references against an identified catalog edition." | C §2.1 EI-1…EI-5, CI-4; S1-B C25 and A1-B #8 (four consumers rely on the edition); DEP-05-01-014 "catalog identity". **Scope addition: owning decision** |
| S-01-4 | REQ-004, after the whole-model sentence; AC-004 | REQ-004: "…where a host supplies only a whole-model identity, that identity is received as the identity of every subject it covers, and the App never computes identities itself." AC-004: "OUT-001 and OUT-003 carry all four basis elements for every fixture read and preserve…" | REQ-004 adds: "Where a host declares that it supplies no workspace identity or generation, a read is received with each such element marked as declared absent and carries the evidence limit 'basis lineage not supplied'; comparisons across a possible lineage change are reported as unknown, and the App supplies neither element. An element a host supplies but omits leaves the read basis incomplete." AC-004: "…carry all four basis elements, or the host's declared absence of workspace identity or generation marked as such, for every fixture read and preserve…" | R13-1 (INTEGRATION); C §5.2 rule 1; ADAPTER RD-2, OM-9; RS R11; V18-3 M-3. Touches a protected criterion: **owning decision**. Alternative: keep REQ-004 and record R13-1 as receiving behaviour for a non-conformant host only |
| S-01-5 | OUT-003, or the owner's custody record | OUT-003: "TEST: contract fixtures and comparison evidence …" | If the owner keeps custody of the shared fixtures with DEL-03-01: add "including the shared fixture catalogue FX-PIPE-01 and the simulated host SH-1 that other deliverables cite (an integration assignment)". Otherwise no SoW change; record the custody decision | B3 §6; C §10, §10.8; first-increment CLOSEOUT_ACCOUNT ("custody of the shared fixture FX-PIPE-01"); DECISIONS_PENDING Part 3. **Owner decision first** |

Considered, not proposed: REQ-002 wording for "named host checks" and
"accepts a requested basis" (sub-elements of elements 6 and 3, already within
REQ-002); a VER-001 change (its "candidate schema identity" is now
satisfiable).

### 1.5 Proposed register changes (`DEL-03-01/Dependencies.csv`)

| # | Change | Rows | Source |
|---|---|---|---|
| R-01-1 | **Mirror only.** Add DOWNSTREAM rows for the 11 consumers whose UPSTREAM rows target DEL-03-01 and have no counterpart here | DEL-02-01 (DEP-02-01-017), DEL-02-03 (DEP-02-03-011), DEL-03-03 (DEP-03-03-006), DEL-03-04 (DEP-03-04-005), DEL-04-02 (DEP-04-02-016), DEL-04-03 (DEP-04-03-023), DEL-05-01 (DEP-05-01-014), DEL-05-02 (DEP-05-02-006), DEL-09-06 (DEP-09-06-027), DEL-09-09 (DEP-09-09-007), DEL-10-03 (DEP-10-03-011) | A1-B #1; first-increment M-01-1…M-01-8; C UNRESOLVED "Register" row; DAG-003 open matter "Deferred supplier-side mirror rows". Verified by script |
| R-01-2 | Retire or retarget DEP-03-01-022 (DOWNSTREAM HANDOVER → **PKG-02**, package level); the deliverable-level consumers are DEP-02-01-017 and DEP-02-03-011 | DEP-03-01-022 | A1-B #1; first-increment M-01-3/-4 |
| R-01-3 | **Notes only, conditional on S-01-3/S-01-4.** DEP-03-01-025 (host input) Notes add: the host also supplies its basis profile (including any declared absence of workspace identity or generation, R13-1) and its catalog edition identity and edition-change event (C U-C15). No new edge | DEP-03-01-025 | C §2.1, §5.2, U-C15 |

### 1.6 Lifecycle observation

`_STATUS.md`: IN_PROGRESS since 2026-09-28 (owner direction DECISION-6,
relayed). Active development continues in this run; the state is truthful.
No change made or proposed.

---

## 2. DEL-03-02 — Proposal, validation and outcome contract (P-v0.8)

### 2.1 Commitment → result

| SoW item | Design sections | Standing | What remains (kind) |
|---|---|---|---|
| OUT-001 CONFIG proposal/basis/origin/outcome schemas | §3.1–§3.5, §9, §9.1; `proposal`, `proposal_state` schemas | **Developed** | Identity representation, encoding, de-duplication enforcement and recovery mechanics stay open (TBD-002; U-P1, narrowed at v0.8 to mechanism only) |
| OUT-002 DOC lifecycle, one route, parity, seams | §1, §2, §4.1–§4.7, §5–§8, §10, §13 | **Developed** | Host route, views, receipts, capture (U-P2…U-P8) are host inputs |
| OUT-003 TEST fixtures and expected observations | §11, §14, VC-P-01…16 | **Developed** (designed; part run on SH-1) | VC-P-15, -16 and parts of -07, -09, -12 run (*test-double*); joined witness DEL-09-09 |
| REQ-001…REQ-013 | as the first increment, plus §3.5 PM-1…PM-7, §4.6 PT-1…PT-19 and DS-1…DS-5, §4.7 SQ-P1…SQ-P6 | Developed | Host evidence; REQ-008's one effect stays a host obligation to be evidenced (§7) |
| AC-001…AC-014 / VER-001…VER-014 | VC-P-01…VC-P-16 | Designed; VC-P-14 records one checker run (Wave A) | Execution on a candidate; the governance-phase constraint fixtures wait on U-P10 |

### 2.2 Result → commitment

| Result | Where | Authority | Supported? |
|---|---|---|---|
| Proposal identity and observation as interface meaning: who mints, host handles, *observe proposal*, *refused — identity conflict*, *not known to host*, de-duplication scope, host-assigned item identity, application as a host step | §3.5 PM-1…PM-7; §9 rows | PROPOSED (S1-B P 4) | Yes: OUT-001 (identity), REQ-004 (refusals are *refused*), REQ-005 (unknown outcome), AC-009 (retain unknown) and TBD-002 (mechanics open) |
| Per-item transition table, derived proposal state *mixed*, per-item validation | §4.6, §4.7 | PROPOSED (S1-B P 5) | Yes: REQ-004 ("States and dispositions apply per change item") |
| Destination results are C §4.1 rows, not proposal outcomes; a V-D refusal is never queued; a refusal at contact during application is an *application error* | §9 note | node B5 | Yes (consequence of C's rows under REQ-005/REQ-011); follows S-01-2 if adopted |
| JSON Schemas | `proposal`, `proposal_state` | R12-1, R12-2 | Within OUT-001; S-02-1 clarifies |

### 2.3 What the 60% description still lacks

- Mechanisms (TBD-002) and every host facility (U-P2…U-P8) wait on host
  agreement, deferred by DECISION-3.
- **Acceptance unit against the first host** (S1-B §2.5, still true): the
  change item has no SWBPIPE counterpart (per-batch Apply, no A10 record).
  Per-item acceptance, accepted-then-stale and mixed dispositions can be
  exercised only on SH-1. A risk for the joined witness, not a P defect.
- Governance-phase constraint receipt (U-P10): LATER by DECISION-4.
- No structural change is anticipated in P itself; OI-014 placement remains.

### 2.4 Proposed ScopeOfWork changes (`DEL-03-02/ScopeOfWork.md`)

| # | Locus | Current text | Proposed text | Grounds; route |
|---|---|---|---|---|
| S-02-1 | OUT-001, last sentence | "Reuse the catalog and policy meanings at the interfaces in CLM-003 and CLM-004; do not select unagreed wire formats or storage topology." | Keep, and add: "Schemas may be written as conformance fixtures of these meanings; such a fixture selects no wire format, storage topology or placement (TBD-002; OI-014)." | R12-2; B3 §6. Clarification |
| S-02-2 (optional) | CLM-004, last sentence | "This contract supplies proposal origin, basis and outcome semantics to those interfaces." | Add: "It consumes `DEL-04-02`'s visible autonomy state (grant display states, grant value and scope, settings version identities) for origin and standing at drafting." | P §3.3, §13 "Expect from DEL-04-02"; A1-B #6; DAG-003 open matter V12 F6 (advice; arc N-05 held, supplier row DEP-04-02-021 only). **Owner's choice** (advice only) |

### 2.5 Proposed register changes (`DEL-03-02/Dependencies.csv`)

| # | Change | Rows | Source |
|---|---|---|---|
| R-02-1 | **Mirror only.** DOWNSTREAM INTERFACE → DEL-03-01, mirroring DEP-03-01-026 (the M3-CP return) | 1 row | A1-B #2; first-increment M-02-1; C §9; verified (no counterpart) |
| R-02-2 | **Mirror only.** DOWNSTREAM rows for DEL-02-01 (DEP-02-01-029, arc N-18), DEL-02-03 (DEP-02-03-025, N-21), DEL-05-01 (DEP-05-01-015), DEL-05-02 (DEP-05-02-007), DEL-09-06 (DEP-09-06-028), DEL-10-03 (DEP-10-03-012) | 6 rows | A1-B #2; P UNRESOLVED "Register" row; verified |
| R-02-3 (optional, with S-02-2) | UPSTREAM INTERFACE → DEL-04-02 (visible autonomy state), the consumer-side row of the held arc whose only row is DEP-04-02-021 | 1 row | A1-A #5; A1-B #4; V12 F6 |
| R-02-4 | **Value normalization.** This register's execution rows carry SatisfactionStatus `TBD`, as do DEL-03-04's and DEL-01-01's; DEL-03-01's and DEL-03-03's carry `PENDING`. One convention, applied across registers in one pass | DEP-03-02-016…027 (and the two other registers) | A1-B #2; DAG-003 open matter "SatisfactionStatus TBD/PENDING convention (P2 O-6)" |

### 2.6 Lifecycle observation

IN_PROGRESS since 2026-09-28; truthful. No change.

---

## 3. DEL-03-03 — Local external-agent receiving adapter (ADAPTER-v0.6)

### 3.1 Commitment → result

| SoW item | Design sections | Standing | What remains (kind) |
|---|---|---|---|
| OUT-001 CODE App-side native MCP/CLI configuration and adapter "as needed" | §2, §3.5, §3.6, §4.1–§4.6, §5, §9 OC-1…OC-12 | **Partial** | Nothing selected (TBD-007: the host chooses its seam, V4-HI-50). App-side design questions still open: configuration locus (OC-3; per-thread option now observed), local transport reachable under the person's sandbox (OC-5; see §6), caller authentication (OC-6), carriage (OC-7). No code (the file states "definition only") |
| OUT-002 DOC enablement and operation-policy interface | §1, §3, §6, §7, §9, UNRESOLVED | **Developed** | Host enablement facility (SQ-28: none on SWBPIPE) |
| OUT-003 TEST consumer fixtures and candidate results | §10 (XF-01…42), §10.3, VC-X-01…09 | **Developed** (designed; mapping run on SH-1) | No App candidate; host variants AWAITING INPUT; DEL-09-09 join deferred |
| REQ-001 native receiving; identity, availability, standing, basis | §4.1–§4.6 (both paths) | Developed as definition | Native-to-catalog mapping is *not established* without a host mapping (NM-2; SQ-12: hand-built); MCP path not usable on the observed local route (§6) |
| REQ-002 off unless enabled; D5 destination | §3.1–§3.6 | Developed | SQ-28 (no A13 facility on SWBPIPE) |
| REQ-003 same route and policy; current-phase checkpoint | §5.3, §6, §7.7 (CO-1…CO-11) | Developed | — |
| REQ-004 outcomes; acts not fabricated | §7.1–§7.6 | Developed | Capture-evidence reference (SQ-01: none) |
| REQ-005 owner/act map | §1 (now including host adoption of its reserved list) | Developed | — |
| REQ-006 identification and handoff | §9–§12 | Developed | Endpoint and candidate identities exist only at implementation |
| AC-001…AC-007 / VER-001…VER-007 | VC-X-01…VC-X-09 | Designed; VC-X-09 and parts of -01…-04 run on SH-1 | AC-001 needs an "identified App candidate" and a selected boundary |

### 3.2 Result → commitment

| Result | Where | Authority | Supported? |
|---|---|---|---|
| Both native paths developed to equal depth (N-MCP, N-CLI), neither selected; N-CLI supplier facts at 0.158.0 (`commandExecution` item, approval requests, `aggregatedOutput`) | §3.5; §4.6 OM-1…OM-10 | R12-4; DECISIONS_PENDING Part 2 ("which external path") | Yes for the design (TBD-007 leaves the choice open). **But** the consumption from DEL-01-01 that CLM-002 and DEP-03-03-013 name is "supplier MCP/dynamic-tool surfaces and channel-status facts"; the command-execution surface is not named. Proposals S-03-5, R-03-6 |
| Observation-to-record mapping; checkpoint observations CO-1…CO-11 passed to DEL-02-03 | §4.6, §7.7; schemas | PROPOSED (S1-B ADAPTER 4); arc N-24 (DEP-02-03-026) | Yes (REQ-003, REQ-006; consumer row DEP-02-03-026) |
| Channel-state transitions CT-1…CT-12 and the channel-status element list; sequences S-6…S-10 | §3.6, §8 | PROPOSED | Yes (REQ-002, OUT-002) |
| Evidence limits new at v0.6 ("host result not isolated", "dispatch recognized from compound command", "basis lineage not supplied") | §4.6 OM-4, OM-1, OM-9; RS R11 | PROPOSED; R13-1, R13-2 | Yes (REQ-006 "evidence limits"); "basis lineage not supplied" follows S-01-4 |
| The required-tool check read in the current phase (ADAPTER §1 row: DEL-02-03 "records and checks (Phase 1)") | §1; §7.7; HOSTING §6.8 | EXEC PH-3 (check in force in both phases) | **SoW places the check under the governance phase** (CLM-002; DEP-03-03-014). Proposals S-03-2, R-03-3 |

### 3.3 What the 60% description still lacks

- **The seam is not chosen**, by design: V4-HI-50 gives the host the choice,
  and the only seam on record is SWBPIPE's CLI in an unmerged, deferred draft
  (SQ-12). The route to completion therefore has two branches.
- **OBS-1 and OBS-1b narrowed both branches at pin 0.158.0 on the local
  route** (§6): the MCP path could not be exercised; the CLI path ran but the
  read-only sandbox denied the local-socket connect a SWBPIPE-style CLI needs.
  OC-5 (reachability under the person's sandbox) is now a concrete open App
  design question. The MCP-call A14 path, App-added call metadata and MCP-call
  failure and retry remain unobserved.
- **Live cases cannot run against the first host**: no A13 facility (SQ-28);
  R8-Q4b deferred. SH-1 is the only verification route this increment has.
- Interposed families (OC-2) stay registered options tied to D6 and the
  governance phase.
- Which App surface displays the channel status is unallocated (S1-B §3.5
  item 4; B3 §4 PANEL row); a later-undertaking deliverable.

### 3.4 Proposed ScopeOfWork changes (`DEL-03-03/ScopeOfWork.md`)

| # | Locus | Current text | Proposed text | Grounds; route |
|---|---|---|---|---|
| S-03-1 | VER-002, second sentence | "Confirm no host call while disabled, truthful unavailability and no implicit remote/data/autonomy expansion." | "Confirm no App-originated host request while disabled, that the host's refusal is recorded as the authoritative off for agent-originated requests, truthful unavailability and no implicit remote/data/autonomy expansion." | AC-002 as revised under SCA-V4-001 ("no App-originated host request; the host's refusal is the authoritative 'off'"); A1-B #5; S1-B §3.1 (ADAPTER E-2 reading). Aligns a VER with its AC; ordinary revision |
| S-03-2 | CLM-002, consumption of DEL-02-03 | "…and App `DEL-02-03`'s checkpoint statement for the current phase and, for the governance phase, its hold machine, hold-support values and required-tool check;" | "…and App `DEL-02-03`'s checkpoint statement and required-tool check for the current phase and, for the governance phase, its hold machine and hold-support values;" | A1-C #5; EXEC PH-3 and C §0 ("The required-tool check is unchanged"); ADAPTER §1. The check is in force in both phases |
| S-03-3 (optional) | CLM-002, consumption list | — | Add: "…, App `DEL-04-02`'s visible autonomy state (grant display states and settings references), and, for the governance phase, App `DEL-02-01`'s declared checkpoint constraints" | ADAPTER §5.3, §5.5, §11; A1-B #4, #6; A1-A #5; V12 F6 (advice). Arcs held; supplier rows DEP-04-02-022, DEP-02-01-027 only. **Owner's choice** |
| S-03-4 (optional) | REQ-003, current-phase sentence | "In the current phase a checkpoint on this channel is plan guidance: its act is recorded only when the person performs it and the App claims no hold (`APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4` D4-1);" | "In the current phase a checkpoint on this channel is plan guidance: the agent carrying out the workflow requests its act, the App records the request where it can identify it and the act only when the person performs it, and the App claims no hold (`APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4` D4-1; `APP-V4-DESIGN-PASS-2-20260930-DECISION-K1` K1-1);" | Amended V4-HI-42 ("the required human act is requested"); DECISION-K1 K1-1 (SETTLED); ADAPTER §7.7; A1-A #8 (proposed a sentence once the reading was confirmed). Applies a decided ruling; amendment route |
| S-03-5 | CLM-002, consumption of DEL-01-01 | "…App `DEL-01-01`'s supplier MCP/dynamic-tool surfaces and channel-status facts at the definition pin 0.158.0…" | "…App `DEL-01-01`'s supplier MCP, dynamic-tool and command-execution surfaces and channel-status facts at the definition pin 0.158.0…" | ADAPTER §3.5 (N-CLI facts "consumed from DEL-01-01 (CLM-002; DEP-03-03-013)"); B3 ADAPTER 3; R12-4; HOSTING §8.4 HCG-A02, §10.1 OB-2 |

Considered, not proposed: TBD-007's identifier collision with DEL-03-04's
TBD-007 (GUIDE F-12; see §4.4); any change to AC-001 after OBS-1 (the
requirement stands; the observation limits one route, see §6).

### 3.5 Proposed register changes (`DEL-03-03/Dependencies.csv`)

| # | Change | Rows | Source |
|---|---|---|---|
| R-03-1 | **Mirror only.** DOWNSTREAM rows for DEL-02-03 (DEP-02-03-026, arc N-24), DEL-03-04 (DEP-03-04-007), DEL-04-03 (DEP-04-03-026), DEL-09-06 (DEP-09-06-029) | 4 rows | A1-B #3; first-increment M-03-1; ADAPTER UNRESOLVED "Register rows (F-11)"; verified |
| R-03-2 | **Maturity.** DEP-03-03-008 RequiredMaturity `TBD` against its mirror DEP-04-01-023 `INITIALIZED`; set one value in both | DEP-03-03-008 | A1-A #4; A1-B #3; DAG-003 open matter "two mirror maturity differences" |
| R-03-3 | **Statement**, with S-03-2. DEP-03-03-014: "…consumes App DEL-02-03's checkpoint statement for the current phase and, for the governance phase, its hold machine, hold-support values and required-tool check; …" → "…consumes App DEL-02-03's checkpoint statement and required-tool check for the current phase and, for the governance phase, its hold machine and hold-support values; …" | DEP-03-03-014 | A1-C #5 |
| R-03-4 (optional, with S-03-3) | UPSTREAM INTERFACE rows → DEL-04-02 (visible autonomy state; supplier row DEP-04-02-022) and → DEL-02-01 (declared checkpoint constraints, governance phase; supplier row DEP-02-01-027). Both arcs are held in DAG-003 (`CandidateEdges.csv`); no topology change | 2 rows | A1-B #4; V12 F6 |
| R-03-5 | **Notes only.** DEP-03-03-009 (EXTERNAL Codex native-tool capability) Notes add: "At pin 0.158.0 on one local Responses route (LM Studio 0.4.16, one model), MCP tools did not reach the model (OBS-1) and a model-issued command ran through Codex (OBS-1b), whose read-only sandbox denied a local-socket connect; dated observations recorded in DEL-01-01 `Design/OBS_1_0.158.0.md`, not qualification." SatisfactionStatus unchanged | DEP-03-03-009 | OBS-1, OBS-1b; HOSTING §10.1 OB-1, OB-2, OB-6; R13-6 |
| R-03-6 | **Statement**, with S-03-5. DEP-03-03-013: "…supplier MCP/dynamic-tool surfaces and channel-status facts…" → "…supplier MCP, dynamic-tool and command-execution surfaces and channel-status facts…" | DEP-03-03-013 | As S-03-5 |

### 3.6 Lifecycle observation

IN_PROGRESS since 2026-09-28; truthful. No change.

---

## 4. DEL-03-04 — Host boundary and integration guide (GUIDE-v0.5)

### 4.1 Commitment → result

| SoW item | Design sections | Standing | What remains (kind) |
|---|---|---|---|
| OUT-001 DOC new-host checklist | §3 HC-0…HC-10, order of use | **Developed** | HC-9, HC-10 conditional by design |
| OUT-002 DOC responsibility/interface matrix | §2.0–§2.15 | **Partial** | Row 8 (role supply, DEL-02-04; App act control, DEL-01-04) and row 10 (DEL-07/08) rest on SoW meaning only: definitions owed by deliverables outside this undertaking (G-1, G-2) |
| OUT-003 TEST completeness checks and recorded comparison | §4.1 CC-1…CC-11, §4.2–§4.5 | **Developed** | Rerun at v0.5; VER-007 checker run (CC-7: status OK, recorded in RV-3 and rerun at v0.4 and v0.5); pins 18/18 by script (re-pinned again at C0). **Its review-status text is stale** (§9, item G-1). Evidence standing *illustrative* only |
| REQ-001…REQ-008 | §2, §3, §4 | Developed (REQ-005 row 8, REQ-006 row 10 limited by D1) | Host column is *answered*, never agreed; DECISION-5 host obligations not relayed (M7.9; no SQ) |
| AC-001…AC-008 / VER-001…VER-008 | VC-G-01…VC-G-08 | Designed; CC rerun and VER-007 checker run | Candidate-bound result only for this guide |

### 4.2 Result → commitment

| Result | Where | Authority | Supported? |
|---|---|---|---|
| Use of HOSTING beyond "native surfaces for optional external access": §6.7 run holds, §8.2 supplied guidance, §8.3 model destination, §11 owner/act map, for rows 5, 6 and 8 | §2.5, §2.6, §2.8, §2.11 | GUIDE inputs table | **Narrower in the SoW**: CLM-003 and DEP-03-04-021 name only "native surfaces for optional external access" (S1-E D.6). Proposals S-04-1, R-04-1 |
| Use of DEL-09-06's CA (step map, staging, evidence ladder), not only RELAY and the answers | M1.8, M8.5, M10.3, §2.11 | GUIDE inputs table | **Narrower in the SoW**: CLM-003 and DEP-03-04-022 name "relay questions and recorded SWBPIPE answers" (A1-E #2; S1-E D.6). Proposals S-04-2, R-04-2 |
| DECISION-5 host obligations (M7.9; HC-7.7…HC-7.9); hold-support map (governance phase, §2.14); SWBPIPE receiving mappings (§2.15); order of use (§3) | as named | R8-13; R5-1/R6-1; R8; S1-E D.8 item 6 | Yes: REQ-005 (as revised), receiving-map row "Autonomy", OUT-001 |

### 4.3 What the 60% description still lacks

- Rows 8 and 10 cannot be completed until DEL-02-04, DEL-01-04, DEL-07-xx and
  DEL-08-xx are defined (later undertaking, D1).
- Every host-column cell is *answered*, nothing agreed; the DECISION-5 host
  obligations have no relay question (next relay not selected, DECISIONS_PENDING
  Part 4).
- Placement (OI-013, OI-014) and the external seam (03-03/TBD-007) could
  change which file defines a line, not the matrix shape (S1-E D.5); no
  structural change of the guide is anticipated.

### 4.4 Proposed ScopeOfWork changes (`DEL-03-04/ScopeOfWork.md`)

| # | Locus | Current text | Proposed text | Grounds; route |
|---|---|---|---|---|
| S-04-1 | CLM-003, last sentence, DEL-01-01 part | "The guide also consumes App v4 DEL-01-01's supplier boundary (native surfaces for optional external access), …" | "The guide also consumes App v4 DEL-01-01's supplier boundary (native surfaces for optional external access, and the supplier facts on run holds, supplied guidance and model destination that rows 5, 6 and 8 cite), …" | S1-E D.6 (DEP-03-04-021 row); GUIDE §2.11. Same arc N-B9 (admitted) |
| S-04-2 | CLM-003, last sentence, DEL-09-06 part | "…DEL-09-06's relay questions and recorded SWBPIPE answers (the host-contribution column) …" | "…DEL-09-06's relay questions and recorded SWBPIPE answers (the host-contribution column) and its connected-activity contract (step map, staging and evidence ladder) …" | A1-E #2; S1-E D.6. Same arc N-B10 (admitted). The DAG-003 guard against DEL-09-06 → DEL-03-04 (E-5) is unaffected |
| S-04-3 (optional) | Receiving map, row "Autonomy", column 4 | "…declared checkpoints are plan guidance in the current phase — their acts are recorded only when performed and no hold is claimed — and hold only for a workflow that takes up the governance phase…" | "…declared checkpoints are plan guidance in the current phase — their acts are requested by the agent carrying out the workflow and recorded only when performed, and no hold is claimed — and hold only for a workflow that takes up the governance phase…" (citing `APP-V4-DESIGN-PASS-2-20260930-DECISION-K1` K1-1) | As S-03-4; GUIDE §0 already states it |

**GUIDE F-12 (two "TBD-007"), routed to this closeout by GUIDE's UNRESOLVED
row: no change proposed.** DEL-03-03's TBD-007 is a local, un-numbered
interface matter (its own text says it is "not an invented accepted OI
identifier"); DEL-03-04's is OI-022. GUIDE's prefixing rule (§0) suffices, as
the first closeout found.

### 4.5 Proposed register changes (`DEL-03-04/Dependencies.csv`)

| # | Change | Source |
|---|---|---|
| R-04-1 | **Statement**, with S-04-1. DEP-03-04-021: "…supplier boundary (native surfaces for optional external access) at the optional external catalog access entry and completeness comparison…" → "…supplier boundary (native surfaces for optional external access; supplier facts on run holds, supplied guidance and model destination) at the optional external catalog access, human-act, autonomy and host-method entries and completeness comparison…" | S1-E D.6 |
| R-04-2 | **Statement**, with S-04-2. DEP-03-04-022: add "and its connected-activity contract (step map, staging, evidence ladder)" | A1-E #2 |

DEL-03-04 has no consumers, so it needs no mirror rows of its own. Its
suppliers lack DOWNSTREAM mirrors of DEP-03-04-005, -007…-010, -012…-019 and
-021…-023. Those in my five registers are in R-01-1 (DEP-03-04-005), R-03-1
(-007) and R-11-1 (-021); the rest belong to C1-A, C1-C or later
undertakings.

### 4.6 Lifecycle observation

IN_PROGRESS since 2026-09-28; truthful. No change.

---

## 5. DEL-01-01 — Stock Codex hosting and supplier contract (HOSTING-BOUNDARY-v0.8; PIN-SPIKE-v0.1; OBS-1 record)

### 5.0 Observation records

- `PIN_SPIKE_0.158.0.md` (v0.1, `0e090a4c…`) is unchanged since 2026-09-28 and
  remains the W11 record under D4. SoW TBD-002 names it.
- `OBS_1_0.158.0.md` (`85707703…`) states its standing: "a dated observation
  at one version (Codex 0.158.0, LM Studio 0.4.16+2, one model). **Not
  qualification** … no App candidate was involved." It holds OBS-1 (one turn,
  MCP path, 2026-09-30 18:45 UTC) and the OBS-1b addendum (one turn,
  command-line path, 19:15 UTC). Authority: DECISION-K1 K1-6 and the owner's
  two later answers. HOSTING §10.1 takes it as OB-1…OB-12 (R13-6). The SoW
  does not name it (S-11-1).

### 5.1 Commitment → result

| SoW item | Design sections | Standing | What remains (kind) |
|---|---|---|---|
| OUT-001 CODE App-owned stock child/protocol boundary | §1, §3 H1–H11, §4 (incl. §4.6 operations, §4.7 LT-01…LT-23), §5 (§5.1, §5.2 CR-01…CR-08), §6 (§6.2.1 RT-01…RT-13), §6.6–§6.8 | **Developed** as definition | Code is implementation. DEL-01-01/DEL-01-02 split on the unknown-request error waits for DEL-01-02 (U-14) |
| OUT-002 CONFIG pin, generated types, supplement, version identity, plan/revision seam | §7.1–§7.3; S-2; SPIKE §3–§4; `generated/0.158.0/` | **Partial** | Reference generator output O-R1/O-R2/O-R3 (U-15) and hence the supplement; distribution-identity composition (U-17); all owner or App implementation owner choices (DECISIONS_PENDING Part 3 names OI-008 and U-15) |
| OUT-003 DOC responsibility account | §8 (S-1…S-7, §8.1 L-1…L-6, §8.2, §8.3, §8.4 harness-capability account), §11, §12 | **Partial** | OI-008 Rust/TS division is a proposal only (U-02); OI-009 account home open (U-03). L-2 and L-3 now observed at one pair (OB-1, OB-2, OB-8), not qualified |
| OUT-004 TEST qualification and upgrade evidence | §9.1–§9.6; VC-01…VC-30; supplier double; SPIKE transcripts; OBS record | **Developed** (method; model-run 35/35) | Everything left is qualification on an App candidate, the U-19 observations and a first upgrade comparison. Reclassified from the first closeout's "partial": a recorded-exchange double now runs the cases the file marks runnable |
| REQ-001 stock child, stdio, unknown-request error | §3, §4, §5, §6.3 | Developed | Candidate |
| REQ-002 generated types; small supplement; native items | §7.3 | Partial | U-15 |
| REQ-003 version identity; plan/revision seam | §7.1, §7.2; S-2 | Developed | At 0.158.0 plan updates carry no revision identity (P-10); DEL-01-03 derives one |
| REQ-004 Rust/TS record; priorities; reuse | §12 | Partial | OI-008 |
| REQ-005 qualify embedding; local-provider requirements | §8.1; §10.1 | Partial | Qualification needs a candidate; see §6 for what OBS-1 adds |
| REQ-006 pin and qualification; deliberate upgrades | §7, §9.5, §10; D4 | Developed (method) | U-01 re-examination; qualification pin |
| REQ-007, REQ-008 no foreign acts | §11 | Developed | — |

### 5.2 Result → commitment

| Result | Where | Authority | Supported? |
|---|---|---|---|
| Harness-capability account at 0.158.0: every supplier surface in one group (HCG-A01…A17, B01…B10) with standing labels; WD's portable names resolve to it (F-27 closed at RP-3) | §8.4 | PROPOSED; DEP-02-01-025 (arc N-16, admitted) | **Supported only from the consumer side.** DEL-02-01's register and SoW say DEL-01-01 supplies the capability "meaning" (DEP-02-01-025) or "inventory" (DEL-02-01 CLM-002); DEL-01-01's SoW names no harness-capability contribution (grep). A1-C #6: "No SoW says which deliverable produces the names." Proposal S-11-2 |
| Lifecycle, client-request and register operations and transition tables; three PROPOSED schemas; supplier double seeded from the eight committed transcripts | §4.6, §4.7, §5.1, §5.2, §6.2.1; §9.6 | PROPOSED (R12-1…R12-3) | Yes: OUT-001, OUT-004 ("recorded protocol exchanges") |
| OBS-1 and OBS-1b as dated observations | §10.1; `OBS_1_0.158.0.md` | DECISION-K1 K1-6; owner answers; R13-6 | Yes: REQ-005, VER-005, VER-006 ("live checks only where they establish a required fact"); no qualification claimed |
| Per-turn effective destination reading (U-27) | §8.3 | PROPOSED; D5 | Yes, via the consumers DEL-03-03 (REQ-002) and DEL-04-03 (DEP-04-03-027) |
| Direct evidence route to DEL-04-03 (S-7; F-26) | §6.4, §8, §8.2 | R9-7 | Yes (DEL-04-03 CLM-004; DEP-04-03-027) |

### 5.3 What the 60% description still lacks

- **Structural choices still open**: OI-008 Rust/TypeScript division, U-15
  reference output, OI-009 account home. All three are owner or App
  implementation owner items for the phase review (DECISIONS_PENDING Part 3).
  Any of them can still restructure the boundary's placement and the
  configuration identity.
- **Seams S-1…S-4 have no receiving comparison**: DEL-01-02…DEL-01-05 are a
  later undertaking (D1; F-15).
- **Live supplier behaviour**: after OBS-1 and OBS-1b, still unobserved: a
  model-issued MCP tool call, its item order and whether it raises an A14
  request; `serverRequest/resolved` before a reply; an answer the request
  does not offer; `turn/interrupt`; post-restart reads; resume-override
  adoption. No further live turn is authorized (work graph "Holds"); a cloud
  MCP turn needs the owner's sign-in and a new answer.
- **No App-side rule on the supplier's start-up traffic** (U-18; widened by
  OB-9). Owner phase review (basis item B-1).
- The supplier labels app-server and its generators `[experimental]` (U-21).

### 5.4 Proposed ScopeOfWork changes (`DEL-01-01/ScopeOfWork.md`)

| # | Locus | Current text | Proposed text | Grounds; route |
|---|---|---|---|---|
| S-11-1 (optional pointer) | TBD-002, first sentence | "OI-012: 0.158.0 selected for definition and generation by `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D4; observations recorded in `Design/PIN_SPIKE_0.158.0.md`." | "…; observations recorded in `Design/PIN_SPIKE_0.158.0.md` and, for one local provider route, in `Design/OBS_1_0.158.0.md` (OBS-1, OBS-1b; dated observations, not qualification)." | OBS record; HOSTING §10.1; R13-6. Navigation pointer |
| S-11-2 | CLM-005, new last sentence (or OUT-003) | — | "This deliverable supplies the harness-capability meaning of the selected pin (the supplier's item kinds, server requests and client methods grouped by capability, with their standing) to `DEL-02-01`, which owns the portable capability names that resolve to it." | HOSTING §8.4, F-27; DEP-02-01-025; DEL-02-01 CLM-002 ("supplies the harness capability inventory"); A1-C #6; A1-D #5; V18-2 J7. Clarifies an existing admitted arc; the owner of the DEL-02-01 side wording is C1-A |

No change proposed to CLM-003's Responses sentence ("the selected Codex
requirements must be qualified rather than assuming all local servers satisfy
them"): OBS-1 is an instance of exactly that risk (§6).

### 5.5 Proposed register changes (`DEL-01-01/Dependencies.csv`)

| # | Change | Rows | Source |
|---|---|---|---|
| R-11-1 | **Mirror only.** DOWNSTREAM rows for the ten consumers with no counterpart here: DEL-02-01 (DEP-02-01-025, N-16), DEL-02-03 (DEP-02-03-023, N-23), DEL-02-04 (DEP-02-04-010), DEL-03-03 (DEP-03-03-013, N-B4), DEL-03-04 (DEP-03-04-021, N-B9), DEL-04-03 (DEP-04-03-027, N-15), DEL-09-06 (DEP-09-06-032, N-C5), and outside the 14: DEL-06-01 (DEP-06-01-013), DEL-09-01 (DEP-09-01-019), DEL-09-02 (DEP-09-02-009) | 10 rows | A1-D #4; B6 §6; HOSTING F-16, F-26; first-increment M-11-1…M-11-4; DAG-003 standing note C2-3; verified |
| R-11-2 | **Notes only.** DEP-01-01-018 (DEP-005) Notes add: "OBS-1 and OBS-1b (2026-09-30): at Codex 0.158.0 against LM Studio 0.4.16+2 with one local model, the Responses wire worked, a flat function tool was called, and MCP tools were not delivered (`namespace` tool type dropped by the server); dated observations, not qualification; DEP-005 unchanged." | DEP-01-01-018 | HOSTING §10.1 OB-1, OB-2, OB-8; F-31 |
| R-11-3 | **Notes only.** DEP-01-01-022 (→ DEL-01-05) Notes add that the local-provider requirement account now carries the observed route limit (a provider that drops `namespace` tools cannot receive a host's MCP tools at this pin; F-31 routed to DEL-01-05) and the approval-setting carrier quirk (F-32) | DEP-01-01-022 | HOSTING §8.1 L-3, F-31, F-32 |

Considered, not proposed: a register row for DEL-01-01's use of the D3 value
(A1-A #3). The first closeout confirmed from this side that HOSTING carries D3
directly and DEP-01-01-021/-022/-024 suffice (its §5.5, V1-A RF-03); nothing
in this run changed that. Also noted, outside my registers:
DEP-01-01-024 (UPSTREAM to DEL-01-05) has no counterpart in DEL-01-05's
register (verified); DEL-01-05 is a later-undertaking deliverable.

### 5.6 Lifecycle observation

IN_PROGRESS since 2026-09-28; truthful. No change.

---

## 6. What OBS-1 and OBS-1b mean for the commitments of DEL-01-01 and DEL-03-03

Observed facts (from `OBS_1_0.158.0.md` and HOSTING §10.1). Two turns on
2026-09-30, Codex 0.158.0 vendor binary (sha256 as SPIKE §3), LM Studio
0.4.16+2 on loopback, `qwen/qwen3.5-9b` (installed; no download), a custom
provider with `wire_api = "responses"`, no sign-in, invented material.
Every supplier request was answered by the harness (origin
`observation-harness`), never a person's act. No App candidate.

| Observation | Bears on | Meaning for the commitment |
|---|---|---|
| **MCP path could not be exercised on the local route.** LM Studio logged "Ignoring unsupported tool type(s): namespace."; the MCP test tool never reached the model; no `mcpToolCall` item (OB-1). That Codex offers MCP tools as a `namespace` tool is the record's **inference** (the request body in the log is truncated) | DEL-03-03 REQ-001, AC-001, VER-001 (N-MCP branch); OC-12; DEL-01-01 REQ-005 (L-3) | AC-001 ("use the selected native Codex MCP or CLI boundary") **cannot be evidenced over MCP on that route at this pin**. It stays a requirement. Evidence for the MCP branch needs another route: a provider that accepts that tool form, a Codex setting that sends flat tools (not observed), or a cloud model (needs the owner's sign-in and a new answer). The MCP-call A14 path, App-added call metadata (OC-7) and call failure and retry stay unobserved (ADAPTER UNRESOLVED). For DEL-01-01, the local-provider requirement account (REQ-005, to DEL-01-05) gains an observed limit: a provider that drops that tool type cannot carry a host's MCP tools (F-31) |
| **Command-line path ran.** `exec_command` called; one `item/commandExecution/requestApproval`; shell-wrapped `command`; `source` `agent` at start and `unifiedExecStartup` at completion; `aggregatedOutput` the tool's JSON line; no output deltas (OB-2, OB-3) | DEL-03-03 REQ-001 (N-CLI branch), OM-1…OM-4; DEL-01-01 REQ-005 (L-3) | L-3 positive for a flat function tool at this pair. OM-1 (read `source` at `item/started`, remove one wrapper) rests on this one observation and is PROPOSED. Stdout/stderr ordering in `aggregatedOutput` and compound commands are unobserved |
| **Read-only sandbox denied the local-socket connect** of an approved command (OB-6) | DEL-03-03 REQ-002 (machine-local), OC-5; DEL-01-01 H9, D3 | A host CLI that bridges over a local Unix socket (SWBPIPE's DRAFT #885 design, SQ-15) is **not shown reachable** from that sandbox. The App may not change the person's approval or sandbox setting (D3; H9), so reachability is an open App design question (OC-5), not a configuration the App may assume. AC-001 against such a host depends on it |
| Per-thread MCP configuration by a dotted `config` key on `thread/start` (OB-10) | DEL-03-03 OC-3 | Supports option (b): a channel can be configured per thread without writing the person's shared Codex configuration. Not selected |
| `approval_policy = "untrusted"` refused in the configuration file but accepted on `thread/start`; the approval offered no `decline` (OB-5) | DEL-01-01 H9, F-32; DEL-03-03 M-6 | The boundary carries the person's setting unchanged and records a start-up refusal as a handshake failure. Which carrier the App uses is DEL-01-05's. An answer is limited to what the request offers |
| `serverRequest/resolved` arrived 8 ms after a written accept (OB-4) | DEL-01-01 U-09 | Consistent with the PROPOSED RT-12 reading; the before-reply trigger is unobserved |
| Responses wire worked against LM Studio (OB-8); requested = reported model and provider, no re-route (OB-7) | DEL-01-01 L-2, U-22, U-27 | L-2 observed at one pair; not qualification (DEP-005 unchanged) |
| Start-up traffic to chatgpt.com (remote control; featured plugins, 401) and github.com (plugin sync) with analytics off and no sign-in (OB-9) | DEL-01-01 U-18, L-4; DEL-03-03 REQ-002 (read narrowly) | Not App-added and not a model destination, so DEL-03-03 REQ-002 ("adds no other destination") is not breached by the channel. *Inference:* the supplier's own traffic is outside every accepted text (basis item B-1) and is the owner's phase-review item |

Standing: none of this is qualification of the pin, the provider or the
model, and none is App candidate evidence. No commitment changes because of
it. It narrows the route to completion for DEL-03-03 OUT-001 and records
inputs for DEL-01-01 REQ-005 and DEL-01-05.

---

## 7. Basis items (none proposes text)

| # | Item | Source | Disposition |
|---|---|---|---|
| B-1 | No accepted text decides the App supplier's own start-up traffic. ARCHITECTURE §1 priority 3, as amended, speaks of a host's agent; OBS-1 and OBS-1b show the traffic is not stopped by the analytics setting and occurs without sign-in | A1-D #6; HOSTING U-18, L-4, §10.1 OB-9; first-increment CLOSEOUT_ACCOUNT ("Codex fresh-home plugin fetch") | Owner, at the phase review (DECISIONS_PENDING Part 3, "the supplier's start-up fetch and its experimental surface"). No text proposed |
| B-2 | HOST_INTEGRATION V4-HI-02 lists eight entry fields. The revised DEL-03-01 REQ-002 adds per-surface exposure; four consumers rely on a catalog edition that neither text names | A1-B #8 (observation) | Observation only. If S-01-3 is adopted, the basis owner may consider whether V4-HI-02 should name the edition; nothing is proposed here |
| B-3 | V4-HI-11 requires every read to return workspace identity, generation, model revision and content hash. R13-1 receives a read from a host that declares it has no workspace identity or generation | R13-1; C §5.2 | No basis change. Recorded as a host's non-conformance to V4-HI-11 (SWBPIPE main, SQ-07), as R8-4 recorded V4-HI-32. The SoW question is S-01-4 |

Seen, belonging elsewhere: A1-D #8 (the four basis docs' headers name only
SCA-V4-001; SCA-V4-002 changed only HOST_INTEGRATION's line layout). Not a
matter for these five deliverables.

---

## 8. Consolidated proposal index (deduplicated, with sources)

| ID | Kind | File and locus | Sources in this run (and earlier) | Route |
|---|---|---|---|---|
| S-01-1 | SoW clarification | DEL-03-01 OUT-001 | B3 §6; A1-B #7; R12-2 | SoW revision |
| S-01-2 | SoW scope addition | DEL-03-01 OUT-001, REQ-002, new AX | B5 §2, §7; C §3.4, §4.1 | Owning decision (DECISION-5 scope) |
| S-01-3 | SoW scope addition | DEL-03-01 OUT-001, REQ-001 | S1-B C25, §1.5; A1-B #8; B3 (C 5) | Owning decision |
| S-01-4 | SoW, protected criterion | DEL-03-01 REQ-004, AC-004 | R13-1; B3 §3; V18-3 M-3 | Owning decision |
| S-01-5 | SoW or custody record | DEL-03-01 OUT-003 | B3 §6; DECISIONS_PENDING Part 3; S1-B owner choice 1; first CLOSEOUT_ACCOUNT | Owner decision first |
| S-02-1 | SoW clarification | DEL-03-02 OUT-001 | B3 §6; R12-2 | SoW revision |
| S-02-2 | SoW, optional | DEL-03-02 CLM-004 | A1-B #6; A1-A #5; DAG-003 V12 F6 | Owner's choice |
| S-03-1 | SoW alignment | DEL-03-03 VER-002 | A1-B #5; S1-B §3.1 | SoW revision |
| S-03-2 | SoW correction | DEL-03-03 CLM-002 | A1-C #5 | SoW revision |
| S-03-3 | SoW, optional | DEL-03-03 CLM-002 | A1-B #4, #6; A1-A #5; V12 F6 | Owner's choice |
| S-03-4 | SoW, optional (applies K1-1) | DEL-03-03 REQ-003 | A1-A #8; DECISION-K1 K1-1 | SoW revision applying a decision |
| S-03-5 | SoW correction | DEL-03-03 CLM-002 | B3 (ADAPTER 3); R12-4; ADAPTER §3.5 | SoW revision |
| S-04-1 | SoW correction | DEL-03-04 CLM-003 | S1-E D.6 | SoW revision |
| S-04-2 | SoW correction | DEL-03-04 CLM-003 | A1-E #2; S1-E D.6 | SoW revision |
| S-04-3 | SoW, optional (applies K1-1) | DEL-03-04 receiving-map row "Autonomy" | as S-03-4 | SoW revision applying a decision |
| S-11-1 | SoW pointer, optional | DEL-01-01 TBD-002 | OBS record; R13-6 | Ordinary pointer correction in the next revision |
| S-11-2 | SoW clarification | DEL-01-01 CLM-005 (or OUT-003) | A1-C #6; A1-D #5; HOSTING F-27; V18-2 J7 | SoW revision, coordinated with C1-A (DEL-02-01) |
| X-1 | SoW, other deliverable | **DEL-01-04** ScopeOfWork (no Design folder; outside the 14) | DECISION-K1 K1-4; A3 §4; B2 §6 (EXEC RC-6); A1-C #2; V18-4 J13; GUIDE G-1 ("collected at this run's closeout") | Next amendment, per K1-4. See text below |
| R-01-1 | Register mirror (11 rows) | DEL-03-01 | A1-B #1; first M-01-x; DAG-003 open matter | `dependency-extract` |
| R-01-2 | Register retarget | DEP-03-01-022 | A1-B #1; first M-01-3/-4 | `dependency-extract` |
| R-01-3 | Register Notes (conditional) | DEP-03-01-025 | C §2.1, §5.2 | With S-01-3/-4 |
| R-02-1 | Register mirror (1) | DEL-03-02 ← DEP-03-01-026 | A1-B #2; first M-02-1 | `dependency-extract` |
| R-02-2 | Register mirror (6) | DEL-03-02 | A1-B #2 | `dependency-extract` |
| R-02-3 | Register row, optional | DEL-03-02 → DEL-04-02 | A1-A #5; A1-B #4 | With S-02-2 |
| R-02-4 | Register value normalization | DEL-03-02 (and DEL-03-04, DEL-01-01) | A1-B #2; DAG-003 P2 O-6 | Register owners, one pass |
| R-03-1 | Register mirror (4) | DEL-03-03 | A1-B #3; first M-03-1 | `dependency-extract` |
| R-03-2 | Register maturity | DEP-03-03-008 | A1-A #4; DAG-003 open matter | Both register owners |
| R-03-3 | Register statement | DEP-03-03-014 | A1-C #5 | With S-03-2 |
| R-03-4 | Register rows, optional (2) | DEL-03-03 → DEL-04-02, → DEL-02-01 | A1-B #4 | With S-03-3 |
| R-03-5 | Register Notes | DEP-03-03-009 | OBS-1, OBS-1b; R13-6 | `dependency-extract` |
| R-03-6 | Register statement | DEP-03-03-013 | as S-03-5 | With S-03-5 |
| R-04-1 | Register statement | DEP-03-04-021 | S1-E D.6 | With S-04-1 |
| R-04-2 | Register statement | DEP-03-04-022 | A1-E #2 | With S-04-2 |
| R-11-1 | Register mirror (10) | DEL-01-01 | A1-D #4; B6 §6; HOSTING F-16, F-26 | `dependency-extract` |
| R-11-2 | Register Notes | DEP-01-01-018 | HOSTING §10.1 | `dependency-extract` |
| R-11-3 | Register Notes | DEP-01-01-022 | HOSTING F-31, F-32 | `dependency-extract` |
| B-1…B-3 | Basis items | §7 | as listed | Owner / observation |

**X-1 — DEL-01-04 act control (DECISION-K1 K1-4), wording collected.** Target:
DEL-01-04 ScopeOfWork, which names no act control or person identity (A1-C
#2: grep empty; V18-4 J13). Proposed obligation: "DEL-01-04 provides the App
act control: a dedicated control that only the person can operate, through
which the person performs an act on App content, producing the capture
evidence DEL-02-03 records (EXEC §5 CAP-1…CAP-9). It is a standing facility,
available whether or not a checkpoint arrival has been recorded (EXEC
RC-6)." Companion, settled by K1-4 for the App: the App records the person's
identity from what it can observe (the name set in the App, the
operating-system account, and the Codex account when Codex reports one),
marked "identity not verified" (EXEC CAP-8). Register: no row toward DEL-01-04
is proposed here; the arc X-1 (DEP-02-03-027) is DEL-02-03's (C1-A). C1-A is
likely to collect the same item from EXEC; the integrator should keep one
copy.

**The brief's other named items** (DEL-05-02 destination surfaces;
DEL-04-01 contract and DECISION-5; DEL-09-09 REQ-001's TBD range) do not fall
in these five deliverables; they belong to C1-C and C1-A (sources: A1-D #1,
B5 §7, B9 §7; A1-A #1; A1-E #1).

**Raised in this run about my deliverables, belonging to another register or
SoW** (for the integrator's dedup): DEL-04-03 REQ-005's consumer list omits
DEL-03-04 (A1-A #6, C1-A); DEL-04-02's register lacks a mirror for
DEP-03-04-012 (A1-A #5, C1-A); DEP-02-01-025 "meaning" against DEL-02-01
CLM-002 "inventory" (A1-D #5, C1-A; S-11-2 is DEL-01-01's side);
DEP-05-01-014 asks for "the adopted capability-catalog/read-basis schemas and
catalog identity": C now offers PROPOSED schemas and an edition identity, not
adopted ones (C1-C; Notes only if anything).

---

## 9. Returned to the graph (missing work, not proposals)

| # | Finding | Evidence | Why it is graph work |
|---|---|---|---|
| G-1 | **GUIDE's review-status statements are false at the candidate.** The Receivers line says "GUIDE-v0.5 has not been independently reviewed; V19 is next (F-9)"; CC-10 says "v0.5 is not independently reviewed (F-9; V19 is next)"; F-9 says "**v0.5 (Wave B)** is self-reviewed", with disposition "Independent review of v0.5 (V19) before merge"; the UNRESOLVED row "Independent review of v0.5 (F-9; V19)" is open. V19-A (`reviews/V19-A.md`, scope line 1: "PKG-04, PKG-03, GUIDE") reviewed GUIDE-v0.5, and V19b rechecked the RQ repairs (MERGE AS DRAFTS). The text is unchanged at HEAD `41899194c4` (grep: lines 53, 808, 999) | Lines 49, 800, 984, 1026 at `a9046631c0` | A warranted Design-text correction in DEL-03-04's OUT-003 record. C0's fence did not include it. It needs a small edit in GUIDE, with the 18-row pin table untouched (GUIDE does not pin itself), before or in the final PR |
| G-2 | **The OBS record's redaction statement is not fully true.** Its redaction lines say the host's time zone "is left out" (lines 8, 226), but §B.7 names the raw rollout `rollout-2026-09-30T13-15-13-…` for a turn at 19:15 UTC, which reveals the offset (V19-B n-2). DISPATCH records a disposition for the brief path only | `OBS_1_0.158.0.md` lines 226, 359; `reviews/V19-B.md` n-2; V19b "n-2 Not done" | Integrator's disposition: either redact the file name or qualify the redaction line. Low severity; a DEL-01-01 Design record |

No missing implementation or evidence was found that the closeout needs
before it can complete. Every remaining item above is implementation,
qualification, a host input, a later-undertaking definition or an owner
decision, and each has a named home.

---

## 10. Completion of this node

- **Written:** only this file. No ScopeOfWork, register, `_DEPENDENCIES.md`,
  `_STATUS.md`, `_CONTEXT.md`, `_REFERENCES.md`, Design file or other file was
  edited. Scratch under `$TMPDIR/c1b` (candidate copies, prototype runs).
- **Git and network:** read-only git (`show`, `ls-tree`, `archive`, `diff`,
  `log`, `status`); no network.
- **Proposals:** 18 ScopeOfWork items (S-01-1…S-11-2 and X-1; S-01-2,
  S-01-3, S-01-4 need an owning decision and S-01-5 an owner custody
  decision first; five are optional), 18 register items (5 mirror items
  covering 32 rows; 2 optional items adding 3 consumer-side rows on held
  arcs; 4 statement and 4 Notes changes; one retarget, one maturity and one
  value-normalization item), 3 basis items with no text, **no new arc**. All unapplied. Routes: SoW revision under the next amendment;
  `dependency-extract` for register rows; owner phase review for S-01-5, B-1
  and the open structural choices.
- **Lifecycle:** all five IN_PROGRESS since 2026-09-28; truthful; no change.
- **Limits:**
  - Design files were compared at their 60% depth and against cited
    sections; they were not reread line by line (C, P, ADAPTER, GUIDE and
    HOSTING total about 935 KB). Commitment coverage rests on each file's
    structure, its UNRESOLVED and verification tables, the S1-B/S1-D/S1-E
    surveys and the Wave B returns, checked against the files at the loci
    cited.
  - The C0 edits after the candidate were checked by diff only (wording in
    HOSTING §6.8 and GUIDE); they change no commitment.
  - C1-A and C1-C were not present when this file was written, so cross-node
    deduplication (X-1, S-11-2, the "belonging elsewhere" items) is left to
    the integrator.
