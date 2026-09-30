# S1-B — scoping survey: DEL-03-01, DEL-03-02, DEL-03-03

- Run `APP-V4-DESIGN-PASS-2-20260930`, node **S1-B**. Type 2 TASK executor (Claude Code subagent); no delegation. Read-only on project state; this file is the only write.
- Survey basis: working tree at `4698471d9e` (branch `claude/chirality-app-v4-60-percent-a41fd5`), 2026-09-30.
- Files surveyed (all under `PKG-03_Host capability and operation contracts/1_Working/`):

| Short | Deliverable | Design file | Version | Lines | sha256 (recomputed) |
|---|---|---|---|---|---|
| **C** | DEL-03-01 | `Design/CATALOG_AND_READ_BASIS.md` | C-v0.6 | 968 | `8282c003024e54708f3b9842e04b6b0dc8c4e1c496027afae582eb6387675ce4` |
| **P** | DEL-03-02 | `Design/PROPOSAL_LIFECYCLE_AND_OUTCOMES.md` | P-v0.6 | 878 | `410fb289e16177e11190db45be37e02b5d82ebf7a9fcff8676e938bb23a51af9` |
| **ADAPTER** | DEL-03-03 | `Design/ADAPTER_ENABLEMENT_AND_RECEIVING.md` | ADAPTER-v0.4 | 1352 | `6e13ab117271b12512f64aab82e99839d1884abb4a43481f7382b67faf253043` |

All three hashes equal GUIDE-v0.3's input-table pins (`HOST_INTEGRATION_GUIDE.md` L18–L20).

## Method and limits

- **Read in full:** the three Design files; the three `ScopeOfWork.md`, `Dependencies.csv`, `_DEPENDENCIES.md`, `_STATUS.md`; `_DAG/DAG-003/HANDOFF_STATE.md`; this run's `BRIEFS.md` and `OWNER_DECISIONS.md`; `R8_RESOLUTIONS.md`; both earlier runs' `OWNER_DECISIONS.md`; `reviews/V6.md`, `V9.md`, `V10.md`; `closeout/CLOSEOUT_ACCOUNT.md` and `C1-B.md` §§1–3; `APP-V4-BASIS-ALIGN-20260928/OWNER_DECISIONS.md` and `RV/RV-3_DEL-03-01.md`; `APP-V4-SCA002-20260929/OWNER_DECISIONS.md`; `loop/LOOP_INIT.md` "Develop the detail appropriate to the phase".
- **Read in part (targeted sections, by grep and line range):** sibling Design files ACT, AS, RS, WD, EXEC, HOSTING, XT, GUIDE (the anchors the three files cite, and their interface tables); reviews V11–V16 (grep for Design-file mentions); RV-3 for DEL-03-02/03 and the SCA-002 RV for DEL-03-03 (E-block tables and notes); `AMENDMENT_PACKET/BASIS_AMENDMENT.md` A12; `_DAG/DAG-003/DependencyEdges.csv`, `CandidateEdges.csv`, `ExcludedRows.csv` (rows touching DEL-03-01/02/03).
- **Checks run:** `shasum -a 256` on every pinned file that exists at HEAD; `git show <commit>:<path> | shasum` for pins the files attribute to a commit; `git diff 6e18505e3 HEAD` on the four basis docs and the three SoWs; whitespace-normalised string match of the quoted V4-HOST-02 text against `docs/PRD.md`.
- **Not checked:** the state of SWBPIPE PR #885 (no network; the commit object `12907f393f5e…` exists locally). Sibling Design files were not read whole, so a join disagreement outside the sections I opened can exist.
- **Counting rule for "stale pin".** A pin or version reference is *stale* when the value the file presents as its operative basis or input differs from the current source. Pins the file itself labels as an earlier state (for example "v0.2 texts read at `28bd00499`") are history: I sample-verified them and do not count them. I mark each stale pin **S** (cited content changed) or **A** (bytes changed, cited content unchanged or changed only by additions).
- Where a line says **States**, the file says it. Where it says **Inference**, it is my reading.

## What changed under the three files since they were written

| Source | Pinned state | Current | Change that matters here |
|---|---|---|---|
| `docs/PRD.md` | `657593ce…` at `6e18505e3` | `bb6e786f7a6c01dc5ce2f16f58e6c600989a12808ff47ce4fd87924bcc6c49bd` | V4-WF-05, V4-HOST-01, V4-HOST-02, "local-first" (§1 quote, §3 lead), OQ-03; DEC-4/DEC-5 row (SCA-V4-001) |
| `docs/ARCHITECTURE.md` | `c3ae766e…` | `317d5789272c5206599936fa9b4e68551b30016d226b88039f0153afa02d828c` | V4-ARC-11, V4-ARC-12, priority 3, the host-agent destination bullet list |
| `docs/HOST_INTEGRATION.md` | `08c8fc7d…60da` | `d4331c39db7f452cd3ba72fdfa4bad540a6053931218359a93646971acb28d9f` | V4-HI-42, V4-HI-70, the Domains sentence in §8; header (SCA-V4-001); one line break (SCA-V4-002) |
| `docs/EXAMINATION.md` | `1b156553…` | `471798bc2f2dc0202ae40d9d5cf033a22ae41af2a0afdf58032cf37a687957d0` | V4-EXM-22, V4-EXM-23 |
| DEL-03-01 SoW | `179a6d35…` | `9ada531b59a6efc007c273f131a8d51df390994ef5f379b1d523d635d3849449` | CLM-002, OUT-001, REQ-002, REQ-004, VER-004, TBD-001 revised; AX-004 added (SCA-V4-001, `340ecf341f`) |
| DEL-03-02 SoW | `42328987…` | `3560915142ebfbf3fa7197008ea3b0660584665c9d86260b22b550c5c2354d0f` | CLM-003, OUT-001, REQ-004, REQ-008, REQ-012, AC-009, AC-013, TBD-001 revised; AX-004 added (SCA-V4-001) |
| DEL-03-03 SoW | `5ac5db97…` | `93faf918ce5d2d4eb14f0ecd1b20831a164a8c55a8b47cad26880818251b1a93` | CLM-002, REQ-002, REQ-003, REQ-004, AC-002, VER-003, TBD-001, TBD-002 revised, AX-004 added (SCA-V4-001); CLM-002 tail and REQ-005 revised, AX-005 added (SCA-V4-002, `1efd4bcdad`) |

The pinned hashes were true at `6e18505e3`, `ba0b37123` and `94aa9181b` (recomputed with `git show`). The Design files were last edited on 2026-09-28 (`f5ceef164a` for P; `caa4334ca1` for C and ADAPTER), before both amendments.

---

# File 1 — DEL-03-01 `CATALOG_AND_READ_BASIS.md` (C-v0.6)

## 1.1 Pins

| # | Pin (where) | Pinned value | Check | Result |
|---|---|---|---|---|
| 1 | Predecessor C-v0.5 (L2, L813) | `72ac4f0f…eacf` at `c6f81a4f2`, unchanged at `94aa9181b` | `git show` at both commits | True (history) |
| 2 | ScopeOfWork.md (L6) | `179a6d35…3b84` | shasum | **Stale (S).** Current `9ada531b…9449` |
| 3 | `repo 6e18505e3` as the state of PRD, ARCHITECTURE, EXAMINATION sections (L6) | commit | `git diff 6e18505e3 HEAD` | **Stale (S).** All three docs amended; of the IDs C cites only V4-HOST-02 changed (see 1.3) |
| 4 | HOST_INTEGRATION.md (L6) | `08c8fc7d…60da` | shasum | **Stale (S).** Current `d4331c39…8d9f`; of the IDs C cites, V4-HI-42 changed |
| 5 | SCC-CASE-002 `Case_Datasheet.md` (L6) | `6acdc6c4…a71a6` | shasum; `git diff 0139b067dc HEAD` | **Stale (A).** Current `a12abfaf…4d5c`; additions only (DAG-002 and DAG-003 successor observations); rows M1-C, M3-CP, M4-X still present (L142, L145, L147 of the datasheet) |
| 6 | First-increment OWNER_DECISIONS.md, DECISION-1 (L6) | `f3f8e5f3…81f2e` | shasum; diff `be8bb46dd3..b4030fe4b1` | **Stale (A).** Current `a9869129…ad2c`; DECISION-2 appended, DECISION-1 text unchanged |
| 7 | R1…R5_RESOLUTIONS.md (L6) | `2f9c7e72…`, `77cfb845…`, `202d52c7…`, `50a009b2…`, `254d0b93…` | shasum | Current |
| 8 | Reviews V3-A, V3-B, V2; comparisons V1-A/B/C; IR1-A/B/C (L6) | abbreviated hashes | shasum, prefix and suffix | Current (all nine) |
| 9 | R6_RESOLUTIONS.md (L851) | `8703e85a…b841` | shasum | Current |
| 10 | Intake OWNER_DECISIONS.md, DECISION-5 state (L7) | `5fd780bf…40b2` | shasum; history | Current. The sentence places it "at `1528a5033`", where the file was `9903bfe0…`; the hash is the later state `3733b14218` (V10 N-1, still worded this way) |
| 11 | R8_RESOLUTIONS.md: R8-13 `44bc9a8d…`; R8-12 `d4c34233…`; R8-1…11 `1770c96e…` (L7) | three states | shasum; `git show` at `1528a50334`, `7a15084523`, `94aa9181b7` | Latest pin current; the two earlier are true history |
| 12 | Intake OWNER_DECISIONS.md, DECISION-3/4 state (L7) | `a5ccab0d…e776` | `git show bcc25624d8` | True history |
| 13 | Intake BRIEFS.md (L7, twice) | `3e33ba26…7517` | shasum | **Stale (A).** Current `6f32809d…`; a "B1" section was appended at `caa4334ca1` |
| 14 | INTAKE_MAP.md (L7) | `3cc18295…ea33` | shasum | Current |
| 15 | `RELAY_ANSWERS_SWBPIPE.md` (L7) | `6f01add3…61c7`; and "are unchanged" | shasum; `git show a999f4ba16` | **Stale (S, small).** Current `afb6e063e7e5dfccf8986206f888cf1e2e1c4e7fc3430fdf86db670714fc0e74`. Three lines changed (main's outcomes state an evaluated basis; `not_assessed` standing; the T9 source). V9 found no App statement contradicted. `FACTS_SQ01_SQ32.md` is `733fb88a…` and was not pinned by C |
| 16 | EXEC-v0.4 (L7) | `d32be377…76d4` at `94aa9181b` | shasum | **Stale (A).** Current `092f2486…08ff`; same version label; 25/23 lines changed in place at `f5ceef164a` (R8-12 closing pass) |
| 17 | WD-v0.6 (L7) | `fce565ed…2f28` | shasum | **Stale (A).** Current `43a9962f…7eb9` (22/18 lines, same pass) |
| 18 | WD-EX-v0.6 (L7) | `950b70b2…ba3d` | shasum | **Stale (A).** Current `8d60ed78…f36e` (4/3 lines) |
| 19 | "Current sibling versions after R8" (L7) | sixteen labels | first `Contribution:` line of each file | Current (all labels match) |
| 20 | Standing statement: V4-WF-05 "flagged for the next accepted-basis update" (L4) | — | PRD at HEAD | **Stale (S).** The basis was amended by SCA-V4-001, accepted 2026-09-29 |
| 21 | Standing statement: V4-HOST-02 "flagged for the next accepted-basis update" (L286; change rows L834) | — | PRD at HEAD | **Stale (S).** Same |
| 22 | "adopt both **as of C-v0.5 / P-v0.5** unchanged" (L230) | version label | file's own header | **Stale (S, label).** §4.1 changed at v0.6; P §0 (L24–25) says "as of C-v0.5; carried in C-v0.6" |
| 23 | Earlier sibling pins (v0.1–v0.5 texts, L7) | abbreviated | sampled: C-v0.2, C-v0.3, C-v0.4, P-v0.2, P-v0.3, P-v0.4 by `git show` | True history |

**Stale pins in C: 13** (S: #2, 3, 4, 15, 20, 21, 22; A: #5, 6, 13, 16, 17, 18).

**Quoted requirement texts.**

- V4-HOST-02 block quote (L289). Matches current `docs/PRD.md` V4-HOST-02 word for word; the PRD adds the source tag "(D-18; DEC-5)". Not stale as text; its "flagged" label is (pin 21).
- V4-HI-02 example reason "Select a load case in the model tree first" (L304), V4-HI-41 "the person may widen it" (L173), V4-HI-32 "a row's content hash" (L379): each still present in current HOST_INTEGRATION.md.
- C quotes no SoW text. It makes two statements about the SoW that are now false (1.2).

## 1.2 ScopeOfWork alignment

SoW read whole at `9ada531b…`. C's header claims OUT-001…003, REQ-001…007, AC-001…008, VER-001…008 (L5); the SoW has exactly those.

| SoW item | Where C answers | Standing |
|---|---|---|
| CLM-001 host/App ownership | §1 (L67–83) | Developed |
| CLM-002, incl. the new sentence "consumes the `DEL-04-03` act field set and lapse vocabulary" | §1 table; §6.2 rows "Human-act evidence" and "Lapse state" (L479–480) | Developed. C cites RS by section, read at RS-v0.2 (L7); not compared with RS-v0.6 (see 1.6) |
| CLM-003 PKG-02 descriptors; OI-003; OI-021 | §8 (L529–580); §2 SWBPIPE paragraph (L122–132) | Developed as a skeleton |
| OUT-001 CONFIG "catalog and read-basis schemas" | §2–§7 | **Partial.** Meanings only; every name is "a semantic label" (L17–18). No schema artifact and no required/optional or cardinality statement |
| OUT-002 DOC responsibility map | §8 | **Partial.** Every H/E/X cell is *unagreed* (L536–540) |
| OUT-003 TEST fixtures and comparison evidence | §10; VC-C-01…08 (L944–968) | **Partial.** Designed, "not run" (L946); no comparison evidence; no test double defined |
| REQ-001 one catalog, three consumers | §2 invariants 1–2 (L95–101) | Developed |
| REQ-002, revised: adds "host-declared exposure per consumer surface, independent of class" and "(no policy basis)" | §3 element 9 (L149); §2 inv. 5 (L112–120); §3.1 (L155–156, L189–194) | Developed. The Design led the SoW; it still cites R-9/R2-4/R2-1 as its authority, not REQ-002 |
| REQ-003 read and unavailable parity | §4.1–§4.4; §6.1 | Developed |
| REQ-004, revised: subject content identity per object/row; whole-model identity; "the App never computes identities itself" | §5.1–§5.4 (L328–453), esp. §5.3 (L360–398) | Developed. Cites R-6/R8-4, not REQ-004 |
| REQ-005 standing; act separation | §6.2 (L466–502) | Developed |
| REQ-006 map; extension promise preserved under TBD-002 | §8 | **Partial** (as OUT-002) |
| REQ-007 no foreign acts | §1 (L81–83) | Developed |
| AC-001 | §10.2, §10.5; VC-C-01 | Designed |
| AC-002, AC-003, AC-005 | VC-C-02, -03, -05 | Designed |
| AC-004 | VC-C-04; §9 | **Held** by the file itself until "an actual, candidate-bound return exists" (L610–611; U-C8) |
| AC-006, AC-007 | §8; VC-C-06, -07 | Designed; map values absent |
| AC-008 owner / point of need / reliance consequence per open input | UNRESOLVED table (L914–942) | Developed; the column is "Effect on this definition" |
| VER-001 "Record the candidate schema identity" | VC-C-01 | **Only named.** No candidate schema exists to identify |
| VER-002…VER-008 | VC-C-02…08, one to one | Designed |
| AX-004 (amendment reference) | — | **Absent.** C never names SCA-V4-001 |
| TBD-001 (revised), TBD-002, TBD-003, TBD-004 | S-C10/S-C11 (L61–62); §8; U-C1; U-C7 and OI-021 rows | Developed |

**Places where C contradicts or lags the revised SoW.**

1. L942 (UNRESOLVED): "SoW text (REQ-002, TBD-001) still calls OI-001/OI-002 open | Closeout C1 via owning route". False since `340ecf341f`: REQ-002 and TBD-001 now record the D2/D3 ruling.
2. L8 (Receivers): "DEL-04-03 (… unregistered join, V1-B RF-04); DEL-04-02 (standing facets — unregistered join, V1-B RF-05)". Both joins are now registered on the consumer side (DEP-04-03-023, DEP-04-02-016, first seen 2026-09-29).
3. L941 (UNRESOLVED register row): lists "unregistered C → DEL-04-02/04-03 joins" and the missing mirrors. The joins exist; the C-side DOWNSTREAM mirrors and the DEL-03-02 mirror of DEP-03-01-026 are still absent (DAG-003 HANDOFF "Deferred supplier-side mirror rows").
4. L6 SoW hash, and no mention of AX-004 / SCA-V4-001.
5. L136–137 and L149 give R-9 as the ground for element 9, and L624–625 says the shared fixture "does not extend DEL-03-01's SoW scope". The second is still true. The first should now cite REQ-002.
6. L931 (U-C8): "reconciliation with DEL-04-01 v0.3". ACT is v0.6.

No statement in C conflicts in meaning with the revised SoW.

## 1.3 Amended basis

| Amended text | Where C touches it | Agreement |
|---|---|---|
| **V4-WF-05** | L4; §0 Phase paragraph (L27–39); L820 | **Meaning agrees; wording and status lag.** C L28–30 matches the amended sentence nearly word for word. Lags: (a) "is flagged for the next accepted-basis update" (L4); (b) "first half" no longer maps to the amended text, which is one sentence on request and record followed by "Holding the checkpoint … is **phased to the governance layer**, not withdrawn (DEC-4)"; (c) C says "Phase 1", the basis and all three SoWs say "the current phase"; (d) the amended text keeps "the required human act is requested" in force now. C's Phase-1 results (FXA-5 L680–684; V-CP1 L757; V-GR1 L762) say arrivals and acts "are recorded" and never say the act is requested |
| **V4-HOST-02** | §4.1 (L285–292); L7 | **Agrees.** Quote exact. "governs the host's embedded agent, not the App's external channel" matches the amended ARCHITECTURE bullet ("This property governs a host's embedded agent; the App's own Codex keeps the person's Codex configuration…"). Lag: the "flagged" label (L286) |
| **V4-HI-42** | S-C10 (L61); class rule 3 (L176–188); L830 | **Lags.** C says D2's declared-checkpoint half is "guidance" in Phase 1, and L830 says "V4-HI-42 [is] guidance in Phase 1". The amended V4-HI-42 has a clause in force now ("whatever the autonomy setting, a checkpoint's required act is requested and recorded as done only when the person performs it") and phases only the hold. C should say which clause binds and which is phased |
| V4-HOST-01, V4-ARC-11, V4-ARC-12, V4-HI-70, V4-EXM-22, V4-EXM-23, "local-first" | not cited (grep: none) | Not applicable. C cites V4-EXM-20/21/24/25 and V4-ARC-20–21, which did not change |

**Inference (cross-file; C is silent).** R8-12 item 2 says that when the grant lets the host apply directly "no proposal arises and no A5 is required". The amended V4-HI-42 and the revised DEL-02-03 REQ-002 say the checkpoint's act is requested "even where the applicable operation autonomy otherwise allows direct application". C's V-CP1 Phase-1 result (L757) stops at "A direct request, if made, meets the host's own treatment and is recorded as observed" and does not say what `CP-accept` then shows. The integrator should rule which reading the fixtures state; see the owner-level list at the end.

## 1.4 Open items

Owner and point of need are as the file states them. Class is mine.

| ID | Where | What is open | Owner (file) | Point of need (file) | Class |
|---|---|---|---|---|---|
| C1 `UNRESOLVED{OI-021}` | L918 | Operation-specific reserved additions; first connected operation, autonomy, environment | Owner via outside SWB session and App/shared owner | Before connected SoW / live examination | **HOST** |
| C2 `UNRESOLVED{OI-003}` | L919; §8 L569–580 | Retain, narrow or defer the extension promise | Owner with host contract owner | Before claiming extension or fixing AC-007 | **OWNER** — the three options are stated; "defer" can be chosen today |
| C3 `UNRESOLVED{OI-014}` | L920; §8 L556 | Shared contract/component placement | App/shared contract owners | Before structural/production allocation | **OWNER** — common shared package, per-consumer copies, or host-owned |
| C4 `UNRESOLVED{OI-013}` | L921; §8 L547 | Loop-side argument checking: shared checker or per host | Shared contract owner with SWB implementation owner | Before shared/host implementation boundary | **HOST** |
| C5 host adoption of D2/D3/R2 | L922 | Whether the host adopts and enforces | Host owner (DEP-001) | Before host conformance | **HOST** |
| C6 consequence vocabulary (ACT U-02) | L923; §3.1 L159; T15 L746 | Vocabulary undefined; OP-C5-on-S-4 expectation held | DEL-04-01 with host policy owner | Before class assignment for connected operations | **NOW** for the vocabulary itself (record: the four d3 dimensions in ACT §5.1 L988 and DECISION_BRIEF #d3); assigning values to real operations is HOST |
| C7 U-C1 | L924 | Serialization, identity algorithm, designation scheme, placement, adapter realization (TBD-003) | App/shared owner with host/consumer owners | Before dependent schema implementation | **LATER** — wire and algorithm choices need the host agreement; see 1.5 for the part that does not |
| C8 U-C2 | L925; Tg L750 | Host definition of generation; lapse and stale across a generation change | Host owner with DEL-04-03 | Before basis conformance | **HOST** |
| C9 U-C3 | L926 | Host confirmation of the per-item stale rule and subject-identity scope | Host owner | Before stale and lapse conformance | **HOST** (answered for SWBPIPE: whole model) |
| C10 U-C4 | L927; §5.4 L411–412 | Multi-read reliance: which cited bases must hold | Host owner with DEL-03-02 | Before stale implementation | **NOW** — *inference:* R2-13 as amended by R8-3 (§5.4 L413–427) already decides it per relied-on target, whichever read supplied the identity; only host confirmation is HOST |
| C11 U-C5 | L928 | Where agent findings are held; whether storing one is a change | Host owner | Before V4-EXM-21 fixture binding | **HOST** |
| C12 U-C6 | L929 | Host behaviour on entry-version mismatch | Host owner | Before adapter implementation | **HOST** |
| C13 U-C7 | L930 | Actual host catalog, tables, exposure, identities | Host owner | Before host conformance claim | **HOST** |
| C14 U-C8 | L931; §9 L606–613 | Actual M3-CP executable return; AC-004 held | DEL-03-02; DEL-04-01 | AC-004 closure | **SPIKE** — run §11/VC-C-04 on a test double, candidate-bound |
| C15 U-C9 | L932; §3.2 | Whether hosts publish version compatibility statements | Host owner with DEL-02-01 | Before DEL-02-03 required-tool fixtures | **HOST** |
| C16 U-C10 | L933; §5.4 L434–439 | Host confirmation of non-mutating basis handling (PROPOSED) | Host owner | Before V4-EXM-21 binding | **HOST** |
| C17 U-C11 | L934 | Whether a host offers a faithful-record operation | Host owner | Before host act-recording integration | **HOST** |
| C18 constraint receipt (R2-12) | L935; V-CP1 L757 | Host receipt of the governing constraint | Host owner with DEL-03-02 | Before governance-phase V-CP1 execution | **LATER** — governance phase; not taken up (R8-1, R8-2) |
| C19 SP-6 cost | L936; V-GR1 L762 | The person may repeat a grant already in force | Owner (U-E4/U-31) | Before the capture-after-arrival rule is fixed | **OWNER** — require capture at or after arrival, or count a prior act bound to current content |
| C20 V-ED1 event | L938 | Host confirmation that an edition addition is an identified event | Host owner | Before DEL-09-09 TS-1 | **HOST** |
| C21 U-C12 | L939 | Per-subject identity not met by SWBPIPE | SWBPIPE owner | Before host act-binding integration | **HOST** |
| C22 U-C13 | L940; L122–132 | No capability catalog on SWBPIPE | SWBPIPE owner; owner notice | When UI-SUCCESSOR resumes | **HOST** |
| C23 register row | L941 | Missing mirrors | Register owner at C1 | C1 | **NOW** — record: current registers and DAG-003 HANDOFF; mostly a wording update (1.2 item 3) |
| C24 SoW-text row | L942 | — | C1 | C1 | **NOW** — closed by SCA-V4-001; delete |
| C25 catalog edition | §2 L90 | PROPOSED; "not a V4-HI-02 field" | — | — | **NOW** — EXEC §3.2 (L291), WD §4.2 (L291), ADAPTER §4.1 and XT §4 already rely on it; an integration ruling can settle its standing |
| C26 open description | §2 inv. 4 L107–111 | Extends V4-SHR-02 to catalog descriptors (F-C9) | — | — | **OWNER** — it widens a PRD requirement's reach; adopt it, or leave it resting on V4-HI-50/V4-ARC-21 |
| C27 *superseded* for A12/A13 | §6.2 L480 | PROPOSED (R2-7) | — | — | **NOW** — RS §7 L-0 and the RS lapse-state line now define "current · superseded" |
| C28 R8-Q4b | §4.1 L271–273 | Whether a launch variable the person sets counts as A13 evidence | Owner, deferred | When UI-SUCCESSOR resumes | **OWNER** (deferred by R8-6) |

The closed row (L937, model-destination host restriction) is not counted. Count: **NOW 6, OWNER 5, HOST 14, SPIKE 1, LATER 2** (28).

## 1.5 Design depth against the 60% description

Contributions C exchanges: (a) entry meaning, §3; (b) non-success results, §4; (c) read basis and subject identities, §5; (d) standing, §6; (e) responsibility map, §8; (f) the shared fixture, §10; (g) the evidence-label mapping (L949–955).

| Aspect | What C has | What is missing |
|---|---|---|
| **Interfaces** | Element tables for the entry (§3, nine elements), class (§3.1), change extras (§3.3), results (§4.1), unavailable reason (§4.2), basis descriptor (§5.1), standing (§6.2); the forward and return tables with P (§9) | (1) **The catalog as something a consumer calls.** "discover entry" is one line in the §7 diagram (L507). No discovery or offering operation, no statement of how a consumer learns the edition, and the edition-addition event exists only inside fixture variant V-ED1 (L763). (2) **No schema form.** OUT-001 is "schemas"; C gives labels with no required/optional or cardinality. DEP-05-01-014 asks for "the adopted capability-catalog/read-basis **schemas** and catalog identity for loop argument validation"; C offers neither a schema nor an adopted edition. (3) **No entry element for named host checks.** §6.2 says only a named host check yields "host checks passed" (L468–472); nothing in §3 lets an entry declare which named checks its result can carry. OP-C3 versus OP-C12 differ only in fixture prose |
| **States** | Value sets: results (§4.1), class (§3.1), exposure (L149), currency (L476), lapse (L480), map cells (L536) | No state or transition account for: a catalog edition (published, superseded, a consumer holding an older one); an entry version; a read result's currency (what turns *current* into *historical*: any revision advance, or a change to what was read; T6 L737 shows one case and gives no rule) |
| **Data** | Basis descriptor (five elements), subject content identity, unavailable reason, class sub-elements, standing elements | **Read-result content.** §6.1 is one paragraph (L457–464). "tables, results and diagnostics" (REQ-003) have no element table: rows, columns, units, what a diagnostic is, how a finding attaches. Also unspecified: what identifies a catalog edition and when two are the same; the kinds of "affected objects" (element 5) |
| **Operating sequences** | One diagram, discover → read → change (§7 L506–517) | Discovery and offering per surface; edition change mid-run; **historical reads** (OUT-003 requires "current and historical reads"; C never says whether a historical result is requested or is only a standing mark on a result that aged); multi-read reliance (C10); generation change (Tg is a one-row fixture branch) |
| **Failure behaviour** | The five results kept distinct, with reporters (§4.1); precondition versus validation error (§4.4); five seam rows (§7 L521–527); basis-incomplete and incomparable rules (§5.2) | A catalog that cannot be read or is partial (ADAPTER §3.5 maps `toolsError` to *not established*; C has no such result); a host with no catalog (L129–131 defers to EXEC EV-4, and C defines no receiving behaviour); a read that lacks workspace identity or generation (true of SWBPIPE main, ADAPTER L399–400) against §5.2 rule 1 |
| **Verification** | Twelve fixture entries, T1–T17, seven variants, eight VC rows mapped to VER-001…008, one evidence-label mapping | Nothing is run. No definition of the test double the *test-double* label presumes. VER-001's "candidate schema identity" has no object. AC-004 is held |

**Structural choices still open that could force a later restructuring.**

1. **Catalog edition and per-operation identity against a first host that has neither** (C22, C25). If the catalog for such a host is to be described by someone other than the host, or not at all, §2, the §8 map, ADAPTER NM-2 and EXEC EV-4 all change. HOST; the App-side receiving rule is decidable now.
2. **Where FX-PIPE-01 lives.** §10 is about 200 of C's 968 lines, serves every file, and by its own statement is "an R1/R2 integration assignment", not SoW scope (L622–625). The closeout routed its custody to the owner (CLOSEOUT_ACCOUNT "Consequences routed"; C1-B §1.5). I found no decision in the later runs' records. Moving it re-points every "C §10" citation in fourteen files.
3. **OI-014 placement** (C3): where the schemas and any shared checker live. It does not change C's meanings; it does change the route to completion that the 60% gate asks about.
4. **OI-003** (C2): a narrowed promise would be expressed through element 9 and the §8 cells.
5. **Schema form for argument and result schemas** (C7 in part): loop-side argument validation (DEP-05-01-014, §8 L546–547) cannot be designed until a form is chosen.

## 1.6 Joins

ACTIVE rows of `DEL-03-01/Dependencies.csv` whose other end is one of the 14, plus arcs that reach C through another register.

| Row | Arc (consumer → supplier) | Contribution | DAG-003 | Supplier text ↔ consumer text | Disagreement |
|---|---|---|---|---|---|
| DEP-03-01-023 (DOWNSTREAM HANDOVER) | DEL-03-02 → DEL-03-01 | Operation identity and original relied-on read basis | **Held**, SCC-002; this row is MIRROR of DEP-03-02-016 | C §9 Forward (L588–592), §3 #1, §5.1, §5.3, §5.4 ↔ P §3.2 (L169–179), §3.4, §5. Present and used | Label only: C L230 "as of C-v0.5 / P-v0.5" |
| DEP-03-01-024 (UPSTREAM PREREQUISITE) | DEL-03-01 → DEL-04-01 | Adopted operation-policy and human-act classes | **Admitted** (representative) | ACT §8.1 (L1216–1233), §8.3 P-01…P-06, §5.3 ↔ C §3.1 (L151–203) | C's "Value standing" list (L158) omits **PROPOSED**, which ACT §8.1 "decision standing" includes. C records ACT as read at v0.2 (L7). Consequence vocabulary open on both sides |
| DEP-03-01-026 (UPSTREAM INTERFACE) | DEL-03-01 → DEL-03-02 | M3-CP return: refusal and application behaviour for the basis comparison | **Held** | P §11 (L641–674) ↔ C §9 Return (L606–613), VC-C-04 (L964). Present as a design; illustrative only | P's register still has no DOWNSTREAM mirror (C L611–613 says so) |
| DEP-03-01-030 (UPSTREAM INTERFACE; maturity TBD) | DEL-03-01 → DEL-09-09 | Candidate-bound extension trace and work account | **Held** | XT §4 (TS-0, TS-1, TR-01), §5 ↔ C §8 extension paragraph (L569–580), V-ED1 (L763), VC-C-07. Present as a plan; TR-01 is AWAITING INPUT | None found |
| DEP-03-01-031 (UPSTREAM INTERFACE; added under SCA-V4-001) | DEL-03-01 → DEL-04-03 | Act field set and lapse vocabulary carried as standing | **Held** | RS §6.1 (L310–329), §7 and its lapse-state line ↔ C §6.2 (L479–480) | C says "act name", RS says "Act kind". C's "at least" list omits RS's act identity, act class, governing policy reference, relations and order. RS gives A12/A13 "current · superseded"; C gives only *superseded* and marks it PROPOSED. C read RS at v0.2 |
| DEP-03-01-022 (DOWNSTREAM HANDOVER → PKG-02) | package target; not a graph arc. The deliverable arcs are DEP-02-01-017 (DEL-02-01 → DEL-03-01) and DEP-02-03-011 (DEL-02-03 → DEL-03-01) | Capability descriptors for workflow tool requirements | Row NOT_TOPOLOGICAL; both deliverable arcs **held** | C §2, §3 #1, #9, §3.2, §4.1–§4.2 ↔ WD §4.2 (L248, L266, L291–295); EXEC §3.2 (L291–295). Present and used | Both consumers rely on *catalog edition*, which C marks PROPOSED |
| (other registers) DEP-05-01-014; DEP-05-02-006; DEP-04-02-016; DEP-04-03-023; DEP-09-09-007; DEP-03-04-005; DEP-09-06-027 | consumers → DEL-03-01 | as each row states | held ×5; **admitted**: DEL-03-04, DEL-09-06 | Other survey rows own these | DEP-05-01-014 asks for "schemas and catalog identity"; C supplies meanings and a PROPOSED edition |

N-18, N-21, N-24 and X-1 do not touch DEL-03-01.

## 1.7 Carried review items that name C

| Item | State | Evidence |
|---|---|---|
| V6 m-1, m-3…m-7 | None names C (GUIDE, RELAY, EXEC, WD-EX, GUIDE, EXEC/WD) | V6 §7. V6's check of R7-4 m-3 in C still holds: V-GR1's last sentence (L762) carries the E1d `CP-check` clause |
| C1-B S-01-1…S-01-5 (SoW corrections) | **Applied** by SCA-V4-001 | SoW diff `6e18505e3..HEAD`; RV-3_DEL-03-01 |
| C1-B N-B1 (DEL-03-01 → DEL-04-03) | **Applied** as DEP-03-01-031 | register |
| C1-B M-01-1…M-01-8 (mirror rows; retire DEP-03-01-022) | **Open** | C's register still has two DOWNSTREAM rows (022, 023); DAG-003 "Deferred supplier-side mirror rows" |
| C1-B §1.5 / CLOSEOUT: custody of FX-PIPE-01 | **Open**; no decision found | grep of the four later run folders' top-level records |
| V9 N-2 (V4-HOST-02 marker in §4.1) | **Fixed**, then superseded by R8-13 | L833–834 |
| V9 N-3, N-7 | Do not name C | — |
| V10 S-2 (attribution of the revised V4-HOST-02) | **Fixed** in C | §4.1 L285–289 carries no "owner's wording"; L834 reads "the recorder's wording confirmed by the owner" |
| V10 N-1 (consumed-input sentence reads as if both hashes were at `1528a5033`) | **Open** | L7, unchanged |
| V10 N-6 | No action asked | — |
| "The 17 Design re-pins" (V13 F4; V15; DAG-003 open matters) | **Open**; this pass | 1.1 |

## 1.8 Recommended work on C in this pass

1. **Re-pin and restate the basis.** New SoW hash; the four docs as amended by SCA-V4-001 and SCA-V4-002; current RELAY_ANSWERS, Case_Datasheet, EXEC, WD, WD-EX bytes; name AX-004. Remove the two "flagged" labels. State V4-WF-05 and V4-HI-42 in the amended wording, saying which clause is in force and which is phased, and adopt "current phase" beside "Phase 1". [1.1, 1.3]
2. **Align to the revised SoW.** Cite REQ-002 for element 9 and *no policy basis*, REQ-004 for subject and whole-model identity; delete L942; rewrite L941 and the L8 "unregistered join" notes against the current registers; fix L931 and L230. [1.2, 1.6]
3. **Compare the two PKG-04 joins at current versions.** RS-v0.6 §6.1 and §7 (names, "current · superseded"); ACT-v0.6 §8.1 (add PROPOSED to value standing). [1.6]
4. **Develop the read-result content model** (§6.1): an element table for table, row, column and unit, result, diagnostic and finding, and an entry element naming the host checks a result can carry. [1.5]
5. **Develop the catalog-level interface, states and sequences:** discovery and offering; edition identity and the edition-change event, moved from V-ED1 into §2; historical-read meaning; currency transitions; failure rows for an unreadable or absent catalog and for a read lacking basis elements. [1.5]
6. **State required/optional and cardinality** for the entry, basis descriptor, unavailable reason and standing tables, with no wire names (inside TBD-003). [1.2, 1.5]
7. **Close the NOW items:** C10, C23, C24, C25, C27; carry C6 to the DEL-04-01 node. [1.4]
8. **With P and ADAPTER, specify the test double** that VC-C-02…05 presume, then produce the M3-CP return on it as a bounded spike (C14). [1.4, 1.5]

Not in this pass, and why: wire names, hash and canonicalization algorithm (TBD-003 needs the host agreement); values for the §8 map cells (they record host agreement; joins are deferred by DECISION-3); OI-003's disposition (owner); the host confirmations C8, C9, C11–C13, C15–C17, C20–C22; the governance-phase constraint receipt (C18); moving §10 out of C, unless the owner decides custody first.

---

# File 2 — DEL-03-02 `PROPOSAL_LIFECYCLE_AND_OUTCOMES.md` (P-v0.6)

## 2.1 Pins

| # | Pin (where) | Pinned value | Check | Result |
|---|---|---|---|---|
| 1 | Predecessor P-v0.5 (L2, L750) | `6ab94fd1…37e0` at `375c3970c`, unchanged at `94aa9181b` | `git show` | True (history) |
| 2 | ScopeOfWork.md (L6) | `42328987…128a` | shasum | **Stale (S).** Current `35609151…4d0f` |
| 3 | `repo 6e18505e3` for PRD, ARCHITECTURE, EXAMINATION (L6) | commit | `git diff` | **Stale (S).** Of the IDs P cites, V4-EXM-22 changed |
| 4 | HOST_INTEGRATION.md (L6) | `08c8fc7d…60da` | shasum | **Stale (S).** Of the IDs P cites, V4-HI-42 and V4-HI-70 changed |
| 5 | SCC-CASE-002 `Case_Datasheet.md` (L6) | `6acdc6c4…a71a6` | shasum | **Stale (A).** Rows M1-P, M3-CP still present |
| 6 | First-increment OWNER_DECISIONS.md (L6) | `f3f8e5f3…81f2e` | shasum | **Stale (A).** P also relies on DECISION-2 D5/D6 (L6), which exists only in the later state `a9869129…`, not pinned by hash |
| 7 | R1…R5; V3-A, V3-B, V2; V1-A/B/C; IR1-A/B/C; R6 (L6, L783) | as C | shasum | Current |
| 8 | R8_RESOLUTIONS.md, latest pin (L7) | `d4c34233…e7af` (R8-12) | shasum | **Stale (A).** Current `44bc9a8d…`; R8-13 was added later and changes nothing addressed to P |
| 9 | R8_RESOLUTIONS.md `1770c96e…` (L7) | R8-1…11 | `git show 94aa9181b7` | True history |
| 10 | Intake OWNER_DECISIONS.md (L7) | `a5ccab0d…e776` (DECISION-3/4) | shasum | **Stale (A).** Current `5fd780bf…`; DECISION-5 and its confirmation appended |
| 11 | Intake BRIEFS.md (L7) | `3e33ba26…7517` | shasum | **Stale (A)** |
| 12 | INTAKE_MAP.md (L7) | `3cc18295…ea33` | shasum | Current |
| 13 | `RELAY_ANSWERS_SWBPIPE.md` (L7) and "are unchanged" | `6f01add3…61c7` | shasum | **Stale (S, small).** Current `afb6e063…0e74` |
| 14 | EXEC-v0.4, WD-v0.6, WD-EX-v0.6 (L7) | `d32be377…`, `fce565ed…`, `950b70b2…` | shasum | **Stale (A) ×3** |
| 15 | Sibling version labels (L7); "C-v0.6" throughout the body | labels | file headers | Current. §0 L24–25 reconciles "as of C-v0.5; carried in C-v0.6" |
| 16 | Standing statement: V4-WF-05 "flagged for the next accepted-basis update" (L4) | — | PRD | **Stale (S)** |

**Stale pins in P: 13** (S: #2, 3, 4, 13, 16; A: #5, 6, 8, 10, 11, and three in #14).

**Quoted requirement texts.** P quotes no basis or SoW text at length. The V4-HI-33 words "accept", never "approve" (L60, L547) are still in HOST_INTEGRATION.md. S-P13 (L64) opens "Workflow checkpoints override autonomy", the old heading-level claim of V4-HI-42; see 2.3.

## 2.2 ScopeOfWork alignment

SoW read whole at `35609151…`. P's header claims REQ-001–013, AC-001–014, VER-001–014 (L5); the SoW has exactly those.

| SoW item | Where P answers | Standing |
|---|---|---|
| CLM-001, CLM-002 (ownership; host facilities) | §1 (L68–89) | Developed |
| CLM-003, revised: identity designation; subject identities; whole-model identity; **consumes DEL-02-01 workflow identity and checkpoint declarations with the item rule; constraint only in the governance phase** | §3.2 (L169–179); §3.3 workflow identity (L190), constraint rows (L195–196); §4.3 (L339–351); §13 (L702) | Developed |
| CLM-004, CLM-005, CLM-006 | §1; §13; §4 | Developed |
| OUT-001, revised: adds "the change-item content identity; and, for a checkpoint in the governance phase, the governing checkpoint constraint with its carriage assurance" | §3.1 (L147), §3.3, §3.4, §9 | Developed as meaning. No schema artifact |
| OUT-002 lifecycle, route, parity, seams | §1, §2, §4–§8, §10, §13 | Developed |
| OUT-003 fixtures and expected observations | §11, §14, VC-P-01…14 | **Partial.** Designed, "not run" (L859) |
| REQ-001 one route | §2 (L91–136) | Developed |
| REQ-002 host truth | §1; VC-P-03 | Developed |
| REQ-003 origin and basis | §3.2, §3.3 | Developed |
| REQ-004, revised: per change item; *rejected* only A10, *withdrawn* only A11; a host refusal is *refused*; "a host's own outcome term of the same name is mapped as the host reports it" | §4.1 (L269–283), §4.2 (L310–311), §9.1 (L589–591) | Developed; the Design led |
| REQ-005 outcome unknown | §4.1 rule 3 (L292–296); §9 | Developed; recovery mechanics open |
| REQ-006 stale and re-draft | §5 (L455–498) | Developed |
| REQ-007 no retargeting | §6 | Developed |
| REQ-008, revised: "at most one application effect per change item"; host obligation; each submission recorded separately | §7 (L509–527) | Developed; wording already matches |
| REQ-009 host views | §8 | Developed |
| REQ-010, REQ-011 | §9, §10; §4.1 rules 1–2 | Developed |
| REQ-012, revised: D2/D3 adopted; OI-021 open | S-P14, S-P15 (L65–66); §10 | Developed |
| REQ-013 no foreign acts | §1, §13 | Developed |
| AC-001…AC-014 | VC-P-01…14, one to one (L865–878) | Designed |
| AC-009, revised: "an observed second effect is recorded as a failed host obligation, not hidden" | VC-P-09 (L873) | Designed; wording matches |
| VER-001 "validate the produced schemas using their declared representation when agreed" | VC-P-01 | **Only named.** No schema, no representation |
| VER-014 "run the registered boundary-owner checker" | VC-P-14 "when available" (L878) | **Partial.** The checker exists at `tools/scope_of_work/check_boundary_owner_resolution.py` and was run during the SCA-V4-001 REVISE |
| AX-004 | — | **Absent** |
| TBD-001 (revised), TBD-002, TBD-003, TBD-004 | UNRESOLVED L838–842 | Developed |

**Places where P contradicts or lags the revised SoW.**

1. L855: "SoW text (AC-013, TBD-001) still calls OI-001/OI-002 open". False since SCA-V4-001.
2. L854 (register row): "UPSTREAM row from DEL-04-02", "DOWNSTREAM mirror of DEP-03-01-026", "mirrors to DEL-05-01/05-02" are still absent from P's register. P gained DEP-03-02-027 (DEL-02-01), which the row does not mention. "SatisfactionStatus TBD vs PENDING" persists (P's execution rows are all TBD).
3. L6 SoW hash; no AX-004.
4. L878: "when available".

No statement in P conflicts in meaning with the revised SoW.

## 2.3 Amended basis

| Amended text | Where P touches it | Agreement |
|---|---|---|
| **V4-WF-05** | L4; §0 (L28–40); L757 | Meaning agrees. Same lags as C: the "flagged" label, "first half", "Phase 1" versus "current phase", and no statement that the act is requested |
| **V4-HI-42** | S-P13 (L64); §4.4 heading "DERIVED from V4-HI-42 + D2b" (L387–388); Phase-1 sentence "V4-HI-42 and WD I-7 are guidance" (L388–392); L765 | **Lags.** (a) S-P13's first sentence, "Workflow checkpoints override autonomy", is the pre-amendment wording; the amended text reads "Autonomy does not override a workflow's declared checkpoints". (b) "V4-HI-42 [is] guidance" is no longer exact: its act-request-and-record clause is in force now and only the hold is phased. (c) The derivation of the forced-*propose* treatment cited the old clause "at a checkpoint the run waits"; in the amended text that ground is "Holding the run at the checkpoint … is phased to the governance layer (V4-WF-05)". The governance-phase rule is unchanged; its citation needs re-grounding |
| **V4-HI-70** | §3.3 workflow-run row (L191); header L6 | Agrees. P uses it only as the source of the workflow-run element. The amendment adds "for a host's agent, each network destination contacted", which P does not touch |
| **V4-EXM-22** | header L6 only | Agrees in meaning. The amended text ("A workflow checkpoint requests a human act, and the act is recorded only when the person performs it, whatever the autonomy; stopping the run … only for a workflow that takes up the governance phase") matches §4.4 "Other checkpoints" (L408–421) except for "requests" |
| V4-HOST-01, V4-HOST-02, V4-ARC-11, V4-ARC-12, V4-EXM-23, "local-first" | not cited | Not applicable ("R5-4: Not applicable: P states no destination text", L782) |

**Inference.** The R8-12 item 2 question raised under 1.3 sits most naturally in P §4.4: after a direct application at a declared A5 checkpoint in the current phase, does the checkpoint's A5 stay requested and unrecorded, or is it not required? P's E-2 row for V-CP1 Phase 1 (L739) covers only the case where the agent proposes.

## 2.4 Open items

| ID | Where | What is open | Owner (file) | Point of need (file) | Class |
|---|---|---|---|---|---|
| P1 `UNRESOLVED{OI-021}` | L838 | Operation-specific additions; first connected operation | Owner via outside SWB session and App/shared owner | Before connected SoW/execution | **HOST** |
| P2 host adoption | L839 | D2, D3, R2 treatments | Host owner | Before host conformance | **HOST** |
| P3 `UNRESOLVED{OI-003}` | L840 | Extension promise | Owner with host contract owner | Before extension claim | **OWNER** (as C2) |
| P4 `UNRESOLVED{OI-014}` | L841 | Placement | App/shared contract owners | Before structural allocation | **OWNER** (as C3) |
| P5 U-P1 (TBD-002) | L842 | Identity representation, encoding, de-duplication enforcement, outcome recovery | Contract and host owners | Before dependent implementation | **LATER** for the mechanisms. The meaning-level parts are gaps P does not list (2.5) |
| P6 U-P2 | L843 | Actual host route, views, receipts, act capture, settings at application | Host owner | When integration relies on them | **HOST** |
| P7 U-P3 | L844 | Host evidence of re-check after acceptance | Host owner | Before application-path conformance | **HOST** |
| P8 U-P4 | L845; §4.2 L306 | Validation failure before queueing stays *drafted* (PROPOSED) | Host owner | Before adapter implementation | **NOW** — an App receiving meaning; SQ-09 (d) is on record as consistent; settle its standing |
| P9 U-P5 | L846 | Whether the host distinguishes refusal at application | Host owner | Before outcome recording | **HOST** |
| P10 U-P6 | L847 | Operation-specific withdraw/reject rules | Host owner; OI-021 | Before withdrawal implementation | **HOST** |
| P11 U-P7 | L848; §4.3 L327–328 | Item application grouping | Host owner | Before application-path implementation | **HOST** |
| P12 U-P8 | L849 | Undo mechanism and availability | Host owner | Before undo implementation | **HOST** |
| P13 U-P9 | L850; §3.1 rule 5 L162–167 | Sibling-draft grouping (PROPOSED; = LOOP T-OPEN-1) | DEL-05-01 with DEL-03-02 and host owner | Before FX-M8 | **NOW** — P rule 5 and LOOP MC-8 already agree; an integration ruling fixes it |
| P14 U-P10 | L851; §3.3 L221–237 | Host receipt of the governing constraint | Host owner with DEL-03-02, DEL-05-01, DEL-03-03 | Before governance-phase fixtures | **LATER** (governance phase) |
| P15 U-C2/U-C3/U-C4/U-C12 | L853 | Shared with C | Host owner | Before stale implementation | **HOST** (U-C4 is NOW in C; see C10) |
| P16 register row | L854 | Missing mirrors; TBD vs PENDING | Register owner | C1 | **NOW** (wording; 2.2 item 2) |
| P17 SoW-text row | L855 | — | C1 | C1 | **NOW** — closed; delete |
| P18 "constraint not carriable on this host" | §3.3 L218–220; L764 | Marked PROPOSED (I2 R8-Q12) | — | — | **NOW** — R8-12 item 5 adopted the label in RS R11; ADAPTER GC-4 says so; P was not updated (2.6) |
| P19 withdrawal before queueing | §4.2 L309 | PROPOSED | — | — | **NOW** |
| P20 capture at or after arrival | §10 L633–635 | R4-5, PROPOSED | — (U-E4/U-26 elsewhere) | — | **OWNER** (as C19) |
| P21 A12 supersession | §10 L620 | R2-7, PROPOSED | — | — | **NOW** — RS §7 L-0, ACT §2.5 and R4-6 define it |
| P22 no resumption; "continues ⟨run⟩" | §10 L623 | R4-4, PROPOSED | — | — | **NOW** — EXEC §4.9 is headed "ADOPTED (R4-4), standing PROPOSED"; the standing should be settled in EXEC and echoed here |
| P23 R8-Q4b | §10 L621 | Launch variable as A13 evidence | Owner, deferred | UI-SUCCESSOR | **OWNER** |
| P24 D6, App-run holds | §4.4 L418–421 | Closed for Phase 1; re-opens with the governance phase | Owner | Governance phase | **LATER** |
| P25 receiving risks ×4 | §12 L685–690 | Queue-time basis; no durable one-effect; route parity; workflow resolution | Joined witness (DEL-09-09) | Actual host | **HOST** |
| P26 boundary-owner checker | VC-P-14 L878 | "when available" | — | VER-014 | **NOW** — the tool exists |
| P27 executable M3-CP return | §11 L671–674 | "The first executable return is a candidate-bound test-double observation"; none exists | DEL-03-02 | AC-004 of DEL-03-01; VER-004/007 here | **SPIKE** (same spike as C14) |

The closed row (L852) is not counted. Count: **NOW 9, OWNER 4, HOST 10, SPIKE 1, LATER 3** (27).

## 2.5 Design depth against the 60% description

Contributions P exchanges: (a) change-request elements, §3; (b) lifecycle, direct branch and undo, §4; (c) stale, re-draft, retry, no retargeting, one effect, §5–§7; (d) host view information, §8; (e) the outcome taxonomy, §9, and the received SWBPIPE vocabulary, §9.1; (f) the acts table, §10; (g) the M3-CP return, §11.

| Aspect | What P has | What is missing |
|---|---|---|
| **Interfaces** | Element tables for identities (§3.1), consumed catalog meaning (§3.2), origin and constraint (§3.3), item content (§3.4); view information (§8); the provide/expect table (§13) | **The route is not described as operations.** (1) **Who mints the proposal identity.** §3.1 (L144) says "stable identity … from drafting onward"; ADAPTER §5.1 (L505) says "Minted before the first submission" and proposes a host-issued identity for direct application; SWBPIPE's draft has a caller key, a preview reference and a ticket (L842). P is silent. (2) **No read of recorded state by proposal identity.** ADAPTER PI-2 and S-4 (L663–666, L888–891) and LOOP R-d "seek observation first" need one. P defines only what a *resubmission* returns (L457–465); its one mention of a read is SWBPIPE's `status` (L599). (3) **Same identity, different content** has no App outcome; SWBPIPE's `idempotency_conflict` is mentioned (L465) and is not in the §9.1 table. (4) No statement of who triggers application after A5, or when |
| **States** | Per-item states and dispositions with actor and evidence (§4.1 L272–283); transitions beyond the source (§4.2); the direct branch (§4.4); item-left events and "all items decided" (§4.3) | No transition table (from, event, actor, to); the diagram at L257–267 carries it. **The derived proposal state is given by example only** ("never stronger than its items", L325–326). Whether some items of one proposal may queue while others are refused at validation is not stated; U-P7 covers grouping only at application |
| **Data** | Item-left event tuple (L331–333); applied-outcome association (L568); refusal content (L483–488); settings references | The receipt reference and the capture-evidence reference are opaque; only the item-left event carries a time. Adequate otherwise |
| **Operating sequences** | §11, T3–T13 (L648–658); the two branch diagrams | Withdrawal; application after acceptance; a direct-branch failure; follow-up after an application error with *partial* effect (the item's state afterwards is not said); a person-origin change (L134–136 leaves it to "host practice") |
| **Failure behaviour** | The strongest area: refusals, stale with both bases, retry precedence, outcome unknown with observer, one effect as a host obligation, undo | The partial-effect follow-up; two queued proposals sharing a target (it follows from §5 and is not a stated case) |
| **Verification** | Fourteen VC rows mapped to VER-001…014; the §11 comparison; E-1/E-2 examples | Nothing is run; no test double defined; VC-P-14's checker not run |

**Structural choices still open that could force a later restructuring.**

1. **Identity minting and observation** (P5 and the gaps above). A host-issued identity or handle changes §3.1, §5, §7, LOOP §6.3 and ADAPTER §5.6. The meaning can be decided App-side now; the mechanism is LATER.
2. **The acceptance unit against the first host.** P's unit is the change item (§3.1 rule 1). SWBPIPE's Apply accepts and applies a whole batch in one step, with no A10 record (L315–320, L352–357). P records "no SWBPIPE counterpart" in five places. *Inference:* per-item acceptance, accepted-then-stale and mixed dispositions cannot be exercised against the first host as it stands, so their verification rests entirely on a test double. Not a defect in P; a risk for DEL-09-06 and DEL-09-09.
3. **The `governed` flag** (WD §4.3.1, PROPOSED). P §3.3 and §4.4 attach the constraint to "governed" checkpoints. If the flag is not adopted, those passages are relabelled; no structure changes.

## 2.6 Joins

| Row | Arc (consumer → supplier) | Contribution | DAG-003 | Supplier text ↔ consumer text | Disagreement |
|---|---|---|---|---|---|
| DEP-03-02-016 (UPSTREAM PREREQUISITE) | DEL-03-02 → DEL-03-01 | Catalog and read-basis definition | **Held** (representative) | C §3, §4.1, §4.4, §5 ↔ P §3.2, §5, §9, §13 (L699) | None in meaning |
| DEP-03-02-017 (UPSTREAM PREREQUISITE) | DEL-03-02 → DEL-04-01 | Adopted policy and act distinctions | **Admitted** | ACT §2.1, §2.3, §5.3, §6, §8.3 ↔ P §2 (L105–123), §4.4, §10, §13 (L700) | P read ACT at v0.2 (L7); none found at the anchors checked |
| DEP-03-02-018 (DOWNSTREAM HANDOVER) | DEL-04-02 → DEL-03-02 | Standing and direct-autonomy origin semantics | **Held**; MIRROR of DEP-04-02-015 | P §4.4 entry condition (L361–370), §9 ↔ AS §3 (L178–200), §7, §8 | P L192 names the first grant state "effective"; AS §3 and P's own L362 name it "effective (person-set)" |
| — (DEP-04-02-021, in DEL-04-02's register) | DEL-03-02 → DEL-04-02 | Visible autonomy state | **Held** | AS §3 ↔ P §3.3 (L192–194), §13 "Expect from DEL-04-02" (L701) | P's register has no UPSTREAM row and its SoW no consumption sentence; the arc rests on the supplier's statement (DAG-003 open matter, V12 F6: advice only) |
| DEP-03-02-019 (DOWNSTREAM HANDOVER) | DEL-04-03 → DEL-03-02 | Outcome semantics and receipt links | **Held**; MIRROR of DEP-04-03-024 | P §9, §3.1, §4.3, §4.5 ↔ RS §5, §7 L-1/L-10, §10 (row DEL-03-02) | (1) RS §10 says DEL-03-02 "Consumes §5 evidence rules"; P §13 has no "Expect from DEL-04-03" row, and arc N-12 is absent by owner decision (DAG-003 open matter, DEL-04-03 owner). (2) **"constraint not carriable on this host"**: RS R11 (L190) labels it "(governance phase; R8-10)"; P places it under the Phase-1 bullet and marks it PROPOSED (L212–220); ADAPTER GC-4 (L588–591) places it in Phase 1 and says "adopted in RS R11" |
| DEP-03-02-020 (DOWNSTREAM HANDOVER) | DEL-03-03 → DEL-03-02 | This contract for the external channel | **Held**; MIRROR of DEP-03-03-007 | P §13 (L706), §3.3, §9.1 ↔ ADAPTER §4.5 M-7, §5, §7, §11 (L1053) | Item (2) above |
| DEP-03-02-021 (DOWNSTREAM HANDOVER) | DEL-03-04 → DEL-03-02 | Responsibility map | **Admitted**; MIRROR of DEP-03-04-006 | P §1, §13 ↔ GUIDE (pins P's current bytes) | Not examined further (S1-E) |
| DEP-03-02-022 (DOWNSTREAM HANDOVER) | DEL-09-09 → DEL-03-02 | Fixtures and outcome expectations | **Held**; MIRROR of DEP-09-09-008 | P §11, §12, VC-P ↔ XT §3.2 XC-02…XC-08 | None found |
| DEP-03-02-027 (UPSTREAM INTERFACE; added under SCA-V4-001; "N-B3") | DEL-03-02 → DEL-02-01 | Workflow identity; checkpoint declarations; the item rule | **Held** | WD §6.1 (L809–820), §4.3.1, §4.3.7 (L612–632) ↔ P §3.3 (L190), §4.3 (L339–351), §13 (L702) | See N-18 |
| **N-18** (DEP-02-01-029) | DEL-02-01 → DEL-03-02 | Change-item content identities, per-item dispositions, all-items-decided, item-left events, applied-outcome object identities | **Held**; reciprocal with N-B3 | P §3.1 (L147), §4.1, §4.3 (L329–338), §9 (L568) ↔ WD §4.3.7 (L614–617), subject-binding rows (L578–580). Present and used | WD §4.3.7 lists item-left causes as "(stale refusal, A11 withdrawal, host refusal)" (L627). P's fifth cause, "cleared by the person with no decision record" (R8-5; L332–333), is missing there. EXEC has it (L859) |
| **N-21** (DEP-02-03-025) | DEL-02-03 → DEL-03-02 | The same, plus applied outcomes with resulting objects | **Held** | P §4.3, §9 ↔ EXEC §4.4 (L591–598), §4.11, §9.1 (L1195). Present and used | EXEC §9.1 records "P-v0.4 read. Current: P-v0.6": the consumer has not recorded a reading of P-v0.6 |
| (other registers) DEP-05-01-015; DEP-05-02-007; DEP-09-06-028; DEP-10-03-012 | consumers → DEL-03-02 | — | held ×2; **admitted**: DEL-09-06, DEL-10-03 (outside the 14) | Other survey rows | — |

N-24 and X-1 do not touch DEL-03-02.

## 2.7 Carried review items that name P

| Item | State | Evidence |
|---|---|---|
| V6 m-1, m-3…m-7 | None names P; P was byte-identical across R7 | V6 header |
| C1-B S-02-1…S-02-5 | **Applied** by SCA-V4-001 | SoW diff; RV-3_DEL-03-02 |
| C1-B N-B3 | **Applied** as DEP-03-02-027 | register |
| C1-B N-B2 (DEL-03-02 → DEL-04-02) | Present only as the supplier row DEP-04-02-021 | 2.6 |
| C1-B M-02-1…M-02-4 (mirror rows) | **Open** | register |
| C1-B disagreement with N-12 | **Decided**: not proposed (BASIS-ALIGN DECISION-6). The RS §10 cell behind it is **open**, with the DEL-04-03 owner | DAG-003 open matters |
| V9, V10 | No residual names P. V9 Check 2 confirmed §5 and §9.1 against the answers | — |
| R8-12 item 5 (evidence-limit labels adopted) | **Not applied in P** | L218–220 and L764 still say PROPOSED; R8-12's own text and P L767 say only item 7 was applied here |
| "The 17 Design re-pins" | **Open**; this pass | 2.1 |

## 2.8 Recommended work on P in this pass

1. **Re-pin and restate the basis.** As C item 1. Re-word S-P13 to the amended V4-HI-42; re-ground the §4.4 derivation; say "requested". [2.1, 2.3]
2. **Align to the revised SoW.** Delete L855; rewrite L854; name AX-004; cite REQ-004, REQ-008 and AC-009 where P's text is now the SoW's. [2.2]
3. **Apply R8-12 item 5** at L218–220, and settle with RS and ADAPTER which phase the "constraint not carriable" limit belongs to. [2.4, 2.6]
4. **Define identity and observation as interface meaning:** who mints the proposal identity and how a host-issued handle relates to it; a named read of recorded state by proposal identity; the outcome for the same identity with different content; the scope within which de-duplication is evidenced. No mechanism. [2.5]
5. **Add a per-item transition table and the derived proposal-state rule;** say whether validation may queue some items and refuse others; add the four missing sequences. [2.5]
6. **Close the NOW items:** P8, P13, P19, P21, P22, P26 (run the checker); fix the L192 state name. Return the WD §4.3.7 item-left cause to the DEL-02-01 node. [2.4, 2.6]
7. **With C and ADAPTER, the test double and the M3-CP return** (P27). [2.4, 2.5]

Not in this pass, and why: identity and de-duplication mechanisms, encoding, recovery (TBD-002 needs host agreement); host facilities (P6–P12); evidence for the governance-phase constraint (P14, P24); any class for a connected operation (OI-021); the supplier mirror rows (registers are not written in this run).

---

# File 3 — DEL-03-03 `ADAPTER_ENABLEMENT_AND_RECEIVING.md` (ADAPTER-v0.4)

## 3.1 Pins

| # | Pin (where) | Pinned value | Check | Result |
|---|---|---|---|---|
| 1 | Predecessors v0.3, v0.2, v0.1 (L2) | `8ef2126d…` at `c6f81a4f2`; `a2905dda…` (1,015 lines) at `cc58211c5`; `58b2409c…` (944 lines) at `e20a3ae8d` | `git show`, hash and `wc -l` | True (history) |
| 2 | ScopeOfWork.md (L6) | `5ac5db97…b1b6` | shasum | **Stale (S).** Current `93faf918…1a93`; revised twice |
| 3 | HOST_INTEGRATION.md (L6) | `08c8fc7d…60da` | shasum | **Stale (S).** Of the IDs cited, V4-HI-42 changed |
| 4 | PRD.md (L6) | `657593ce…8573` | shasum | **Stale (S).** Of the IDs cited, V4-HOST-02 changed |
| 5 | ARCHITECTURE.md (L6) | `c3ae766e…e533` | shasum | **Stale (A).** V4-ARC-20/21, the IDs cited, did not change |
| 6 | EXAMINATION.md (L6) | `1b156553…ee19` | shasum | **Stale (S).** V4-EXM-23 was retitled and rewritten |
| 7 | SCC-CASE-002 `Case_Datasheet.md` (L6) | `6acdc6c4…a71a6` | shasum | **Stale (A).** Rows M1-C, M1-P, M2-A present |
| 8 | First-increment OWNER_DECISIONS.md (L6) | `f3f8e5f3…81f2e` (D1–D4) and `a9869129…ad2c` (D5, D6) | shasum | First is history (**A**); second is current |
| 9 | R1…R5; V3-A, V3-B (L6) | full hashes | shasum | Current |
| 10 | First-increment BRIEFS.md (L6) | `58de4a2c…698f` | shasum; history | **Stale (A).** Current `35cbc974…`; true at `1c36b6d975` |
| 11 | Intake OWNER_DECISIONS.md (L8) `5fd780bf…`; R8 `44bc9a8d…` (L8) | — | shasum | Current; the sentence has the ambiguity V10 N-1 describes |
| 12 | Intake BRIEFS.md (L8, L10) | `3e33ba26…7517` | shasum | **Stale (A)** |
| 13 | R8 `d4c34233…` (L9), `1770c96e…` (L10); OWNER_DECISIONS `a5ccab0d…` (L10); INTAKE_MAP (L10) | — | `git show`; shasum | History true; INTAKE_MAP current |
| 14 | `RELAY_ANSWERS_SWBPIPE.md` (L10) and "are unchanged" (L9) | `6f01add3…61c7` | shasum | **Stale (S, small).** Current `afb6e063…0e74` |
| 15 | EXEC-v0.4, WD-v0.6, WD-EX-v0.6 (L10) | as C | shasum | **Stale (A) ×3** |
| 16 | RELAY-v0.3 (L1072–1074) | `89b6b9c9…8bdd7`, read at `816c917f0` | `git show`; shasum | **Stale (A).** True at that commit; current `c93f8cc5…`. Later edits are ledger and metadata; V9 hashed §0–§3 as unchanged |
| 17 | DEL-01-01 generated bundles (L17) | `aa5cb3fb…dcd0f`, `34f28a48…8f458` | shasum | Current |
| 18 | PIN-SPIKE-v0.1 (L16) | `0e090a4c…b115` | shasum | Current |
| 19 | Sibling pins at `ba0b37123` and `8fb51f07f` (L12–L19) | full hashes | sampled: C-v0.3, C-v0.4, P-v0.3, P-v0.4, RELAY-v0.2 by `git show` | True history |
| 20 | PR #885 head `12907f393f5e…` (L21) | commit | `git cat-file -t` | The commit exists locally; PR state not checked (no network) |
| 21 | Standing statement: V4-WF-05 "flagged for the next accepted-basis update" (L4) | — | PRD | **Stale (S)** |
| 22 | Standing statement: V4-HOST-02 "flagged for the next accepted-basis update" (L299–300; L1303) | — | PRD | **Stale (S)** |
| 23 | Sibling version labels (L9); body citations | labels | file headers | Current. E-4 (L239) cites "ACT-v0.4 §2.6" as closure history |

**Quoted requirement texts.**

| Where | Text as quoted in ADAPTER | Current text | Result |
|---|---|---|---|
| §3.4 L303 | V4-HOST-02 block quote | `docs/PRD.md` V4-HOST-02 | Exact (the PRD adds "(D-18; DEC-5)") |
| E-2 L225–227 | 'SoW AC-002 "no host request" is read as the App's own requests' | AC-002: "Disabled access produces an explicit disabled result and no **App-originated** host request; the host's refusal is the authoritative "off" for agent-originated requests" | **Stale.** The SoW now states the reading. VER-002 still says "Confirm no host call while disabled", so the reading still serves VER-002 |
| F-13 L1136–1141 | 'VER-003 asks to exercise a "checkpoint wait"' | VER-003: "a checkpoint case whose act is recorded only when performed, with no hold claimed (a hold case only for a workflow in the governance phase)" | **Stale.** The REQ-003 sentence quoted beside it ("Workflow checkpoints retain their required human act") is still exact |
| F-14 L1148–1152 | REQ-002 asks the adapter to "carry the selected local/privacy data boundary without treating enablement as permission for another data destination" | REQ-002: "Host content read over the channel may flow to the model the person selected for the App conversation, cloud included; the App gates neither enablement nor requests on that destination and adds no other destination …" | **Stale** |
| §2 L136–137; OC-2 L939 | the SoW's "as needed"; OUT-001 "without prescribing … a new server" | OUT-001 | Exact |

**Stale pins in ADAPTER: 19** (S: #2, 3, 4, 6, 14, 21, 22, and the three stale SoW quotes; A: #5, 7, 8, 10, 12, 16, and three in #15).

## 3.2 ScopeOfWork alignment

SoW read whole at `93faf918…`. ADAPTER's header claims REQ-001…006, AC-001…007, VER-001…007 (L5); the SoW has exactly those. (The "REQ-008; VER-008" in L23 are DEL-09-09's identifiers.)

| SoW item | Where ADAPTER answers | Standing |
|---|---|---|
| CLM-001 ownership | §1 (L74–99) | Developed |
| CLM-002, revised: consumes DEL-01-01's supplier surfaces and channel-status facts at pin 0.158.0, and DEL-02-03's checkpoint statement for the current phase and governance-phase hold machine; D2/D3 ruled; OI-021; DEP-001 | §3.5 (L311–326); §5.3 (L521–627); §7.7 (L819–861); §11 (L1056–1057) | Developed |
| CLM-003, CLM-004 | §1; §7.5–§7.6; §12 | Developed |
| OUT-001 CODE: "App-side native Codex MCP/CLI configuration and receiving adapter as needed" | §2, §4, §5; §9 OC-1…OC-12 | **Partial.** "definition only, no code" (L5); "Nothing here is selected" (L902) |
| OUT-002 DOC | §1, §3, §6, §7, §9, UNRESOLVED | Developed |
| OUT-003 TEST fixtures "and their identified candidate results" | §10 (XF-01…XF-42) | **Partial.** Inventory designed; no result; the "simulated endpoint" is not specified |
| REQ-001 native receiving; identity, availability, standing, basis preserved | §4.1–§4.5 | **Partial.** Mapping is PROPOSED and *not established* without a host mapping (NM-2) |
| REQ-002, revised to the D5 wording | §3.1–§3.4 | Developed; the Design led |
| REQ-003, revised: "*not permitted* — never silently converted"; current-phase plan guidance; "the App claims no hold"; hold support is DEL-02-03's governance-phase definition | §6 RP-3 (L718–730); §5.3 phase paragraph (L523–534); §7.7 | Developed |
| REQ-004, revised: "at-most-one-effect-per-item … a host obligation to be evidenced" | §7.1–§7.6 | Developed |
| REQ-005, revised under SCA-V4-002: operation-specific additions with the owner via the SWB session and App/shared owner; "host adoption and enforcement of its reserved list with the external host owner" | §1 owner/act map | **Partial.** §1 says it lists every excluded act "one for one" (L76–77). It has the OI-021 row (L95). It has no row for host adoption and enforcement of the host's reserved list; that appears only in UNRESOLVED (L1328) |
| REQ-006 identification and handoff | §9, §10, §11, §12 | Developed as definition |
| AC-001 "An identified App candidate can use the selected … boundary" | — | **Only named.** No candidate, nothing selected |
| AC-002 (revised) | §3.2, §3.3 E-2; XF-01…07 | Designed |
| AC-003 | §6; XF-22…29, 34, 42 | Designed |
| AC-004, AC-005 | §7; XF-14…21, 30…33, 38, 40, 41 | Designed; positive faithful recording AWAITING INPUT (SQ-01) |
| AC-006, AC-007 | §1, §9, §12; VC-X-06, -07 | Developed |
| VER-001…VER-007 | VC-X-01…08 (L1345–1352) | Designed, "not run" (L1336) |
| VER-003, revised | XF-25, XF-26, XF-42 in two parts; VC-X-03 | Designed; matches |
| AX-004, AX-005 | — | **Absent** |
| TBD-001, TBD-002 (revised); TBD-003…TBD-007 | §1 (L94–98); UNRESOLVED (L1313, L1325–1327) | Developed |

**Places where ADAPTER contradicts or lags the revised SoW.**

1. F-10 (L1130), F-13 (L1136–1147), F-14 (L1148–1152) and the UNRESOLVED row at L1330 treat SoW text as still to be corrected. The corrections were made by SCA-V4-001 (C1-B S-03-1, S-03-2, S-03-4 applied as E-0303-01, -02, -04) and SCA-V4-002.
2. E-2 (L225–227): see the quote table.
3. L23 (Receivers): "By join, not registered here: … DEL-02-03 …, DEL-01-01 (supplier surfaces)". Both are now registered: DEP-03-03-014 and DEP-03-03-013.
4. F-11 (L1131) "register rows — carried to C1": partly done (3.7).
5. §1: no host-adoption row for the revised REQ-005.
6. L6 SoW hash; no AX-004 or AX-005.
7. Terms: the SoW says "the current phase"; ADAPTER says "Phase 1".

No statement in ADAPTER conflicts in meaning with the revised SoW.

## 3.3 Amended basis

| Amended text | Where ADAPTER touches it | Agreement |
|---|---|---|
| **V4-WF-05** | L4; S-X12 (L69); L1291 | Meaning agrees. Same lags as C and P |
| **V4-HOST-02** | S-X11 (L68); §3.4 (L299–309); L6 | **Agrees.** Quote exact. "It is neither extended to App conversations nor waived" matches the amended ARCHITECTURE bullet. Lags: the "flagged" label (L299–300), and "The owner's revised wording:" (L301), which is the V10b S-2 residual |
| **V4-HI-42** | S-X10 (L67); L1300 | **Lags**, as P: "Checkpoints override autonomy" is the old claim; "WD I-7 and V4-HI-42 are guidance" omits the clause in force now |
| **V4-EXM-23** | header L6; §3.4 heading (L269) | **Citation lags.** At `6e18505e3` V4-EXM-23 was "Privacy in local operation … no request goes anywhere but the configured model server". It is now "Host-agent network destinations" and verifies V4-HOST-02 on the host's traffic. §3.4 itself says V4-HOST-02 governs the host's embedded agent and not this channel. *Inference:* the heading's V4-EXM-23 citation no longer supports a section about the App channel; keep it only as a pointer to what the joined examination observes |
| **V4-HI-70** | not cited in the Design; the SoW's REQ-004 sources cite it | Agrees by content: §3.4 records the model destination per turn (RS R5), which is "the model used"; the new host-agent destination element is LOOP's |
| V4-HOST-01, V4-ARC-11, V4-ARC-12, V4-EXM-22 | not cited | Not applicable |
| "local-first" | not used. L1303 records that "the 'in local operation' qualifier is dropped" | Agrees |

## 3.4 Open items

| ID | Where | What is open | Owner (file) | Point of need (file) | Class |
|---|---|---|---|---|---|
| A1 OC-1 | L938 | Transport family the host offers | Host owner with App owner agreement | Before App receiving implementation; before DEL-09-09 qualification | **HOST** (SQ-12 answered: a CLI, in a deferred draft PR) |
| A2 OC-2 | L939; §2 L122–150 | App realization family | App owner | same | **NOW** — R4-2 and S-X12 already exclude the interposed families for this increment; the native family follows the host's seam. The text still says "neither is selected" |
| A3 OC-3 | L940 | App-side configuration locus | App owner with DEL-01-01 | same | **SPIKE** — whether a per-thread `config` accepts an MCP-server entry is `not-observed` (L320) |
| A4 OC-4 | L941 | Enablement loci | DEL-04-01 with owner and host owner | same | **HOST** for the facility; the App side is ruled (R4-13) |
| A5 OC-5 | L942 | Local transport and locality | Host owner with App owner | same | **HOST** (SQ-15 answered; sandbox reach falls under A21) |
| A6 OC-6 | L943; L1320 | Caller authentication and identity | Host owner with App owner | Before origin conformance | **HOST** |
| A7 OC-7 | L944 | Carriage mechanism for origin, constraint, grant, proposal identity | Host owner with App owner and DEL-03-02 | same | **HOST** |
| A8 OC-8 | L945; L1322 | Native surface derivation and native-to-catalog mapping | Host owner | Before AC-001 claim | **HOST** |
| A9 OC-9 | L946 | Result and outcome encoding | Host owner with App owner and DEL-03-02 | same | **HOST** |
| A10 OC-10 | L947 | Outcome read-back by proposal identity | Host owner | same | **HOST**; its App-side meaning is the P gap in 2.5 |
| A11 OC-11 | L948 | Checkpoint hold on X | DEL-02-03 with host owner | Governance phase | **LATER** |
| A12 OC-12 | L949 | Tool-permission interplay; MCP-call approval path `not-observed` | App implementation owner | same | **SPIKE** |
| A13 SQ-28 | L1314 | Host enablement facility for A13 and its capture-evidence reference | SWBPIPE owner decision | Before any live external case | **HOST** |
| A14 R8-Q4b | L204–205; L1314 | Whether a launch variable the person sets counts as A13 evidence | Owner, deferred | When UI-SUCCESSOR resumes | **OWNER** |
| A15 `UNRESOLVED{D6}` | L1315 | App-side run holds on X | Owner | Governance phase | **LATER** |
| A16 U-P10 | L1317 | Host receipt of the governing constraint | Host owner | Governance phase | **LATER** |
| A17 capture-evidence reference (SQ-01) | L1318 | None on SWBPIPE | SWBPIPE owner decision | Before XF-18 positive case | **HOST** |
| A18 proposal identity and durable de-duplication (SQ-08) | L1319; PI-4, PI-5 PROPOSED | — | SWBPIPE owner decision with DEL-03-02 | Before direct application over X | **HOST** |
| A19 enablement read; disable with queued proposals (SQ-13) | L1321; E-8 PROPOSED | — | Host owner | Before XF-35 | **HOST** |
| A20 App restart custody | L1323; PI-6 | In-flight native item across relaunch | DEL-01-02 (later undertaking, D1) | Before XF-41 | **LATER** (outside the 14) |
| A21 supplier behaviours `not-observed` at 0.158.0 | L1324 | Per-thread MCP configuration; App-added call metadata; MCP-call A14 path; failure and retry; sandbox effect | DEL-01-01 with App implementation owner | Before implementation; at pin re-examination | **SPIKE** — a bounded observation at the pin |
| A22 `UNRESOLVED{OI-003}` | L1325 | — | Owner with host contract owner | — | **OWNER** |
| A23 `UNRESOLVED{OI-021}` | L1326 | — | Owner via SWB session | — | **HOST** |
| A24 `UNRESOLVED{OI-013}` | L1327 | — | Shared contract owner with SWB owner | — | **HOST** |
| A25 `UNRESOLVED{OI-014}` | L1327 | — | App/shared contract owners | — | **OWNER** |
| A26 host adoption on X | L1328 | — | Host owner | Before any host-enforcement claim | **HOST** |
| A27 consequence vocabulary | L1329 | — | DEL-04-01 with host policy owner | — | **NOW** (as C6) |
| A28 register and SoW rows | L1330 | F-10, F-11, F-13, F-14 | Register owner / C1 | C1 | **NOW** — closed or changed (3.2, 3.7) |
| A29 PROPOSED rule set | §2 L136; E-4 L234; §4.1 L332; §4.2 L370; RD-5 L407; M-1…M-6 L424; §5.1 "Assurance required" L496 | App-side rules not yet ruled | — | — | **NOW** — each is an App receiving rule; settle its standing |
| A30 F-21 | L1195–1199 | Per-turn destination depends on supplier facts not observed live | DEL-01-01 (HOSTING U-19) | Before the record is relied on | **SPIKE** |
| A31 F-17 | L1165–1169 | Observation before resubmission cannot be enforced on X; XT XC-06 should admit the recorded violation | — | — | **NOW** — a check of XT's expected result |

The closed row (L1316, SQ-16) is not counted. Rows L1320 and L1322 repeat OC-6 and OC-8 and are counted once. Count: **NOW 5, OWNER 3, HOST 15, SPIKE 4, LATER 4** (31).

## 3.5 Design depth against the 60% description

Contributions ADAPTER exchanges: (a) the enablement account and channel states, §3; (b) receiving rules and native-tool mapping, §4; (c) dispatch carriage, §5; (d) same-route rules and checkpoint observation, §6 and §7.7; (e) the fixture inventory, §10; (f) evidence-limit labels and record inputs for RS, §11.

| Aspect | What ADAPTER has | What is missing |
|---|---|---|
| **Interfaces** | Element tables for enablement (§3.1), channel states (§3.2), mapping (§4.1), the dispatch record (§5.1), carriage by family (§5.2); supplier facts at the pin (§3.5); the provide/expect table (§11) | (1) **No mapping from what the App observes to what it records.** §3.5 lists the fields of an `mcpToolCall` item; §5.1 lists dispatch-record elements; nothing connects them, nor maps them to RS R7/R9/R11/R13. (2) **The CLI path is not described at the supplier level.** §3.5 has the approval requests for command execution (L324) and no fact about the command-execution item the App would read (command, exit status, output). SWBPIPE's only answered seam is a CLI (SQ-12). (3) **§7.7 "observations"** passed to DEL-02-03 have no element list and no mapping to EXEC §4.4's events |
| **States** | Four channel states and one qualifier, with condition, result and reporter (§3.2 L172–185) | No transition table: which event moves the channel between states (A13 enable or disable, endpoint start or stop, configuration change, relaunch). The E-rules carry it in prose. A dispatch has no stated states (submitted, observed, outcome unknown, later observation) |
| **Data** | Dispatch record with required assurance; the evidence-limit list (L1062) | What the channel status shows, as a list; the identity of an "App candidate" |
| **Operating sequences** | S-1…S-5, five short sequences (§8 L867–896) | Discovery and mapping; relaunch and reconnect (E-9, PI-6 are rules, not sequences); the faithful-recording sequence (§7.6); the current-phase checkpoint observation sequence (§7.7 is prose) |
| **Failure behaviour** | Strong: §3.2, §4.5, §5.6 PI-1…PI-6, §7.1–§7.4 | A host read without workspace identity or generation (L399–400 states the fact for SWBPIPE main; the consequence under C §5.2 rule 1 is not stated) |
| **Verification** | 42 XF cases with AC/VER mapping; 13 local subjects; 8 VC rows | **The simulated endpoint is never specified.** "Every case below runs against a simulated endpoint (test double)" (L955); no file says what that double implements. Nothing is run. With joins deferred and no A13 facility on SWBPIPE (F-20, L1190–1194), the double is the only verification route this increment has |

**Structural choices still open that could force a later restructuring.**

1. **Which seam the App designs against** (A1–A3). Both families are kept and none is selected (L122, L902). The only seam on record is a CLI in a deferred, unmerged draft; the supplier facts in §3.5 are mostly MCP. *Inference:* developing the CLI path to the same depth as MCP, or choosing to stay neutral, is a choice this pass must make before items (1)–(2) above can be written. It affects §3.5, §4.1, §4.5 and §5.2.
2. **A13 on the first host** (A13, A14). With no facility, the channel is *disabled* in every SWBPIPE case (L183–185). If R8-Q4b is answered "yes", §3.1–§3.3, XF-01…05 and ACT §2.6 change; if "no", every live case waits for a SWBPIPE decision.
3. **Interposed families** (OC-2) remain "registered options". Adopting one later would change carriage assurance (§5.2), holds (GC-3, GC-5) and the fixtures. This is tied to D6 and the governance phase: LATER.
4. **Who displays the channel status.** ADAPTER "shows it in the channel status" (L164, L285); AS says the status "is DEL-03-03's" (AS L30, L130). *Inference:* the App surface that carries it belongs to a later-undertaking deliverable (DEL-01-04 or a sibling); not allocated in any file I read.

## 3.6 Joins

| Row | Arc (consumer → supplier) | Contribution | DAG-003 | Supplier text ↔ consumer text | Disagreement |
|---|---|---|---|---|---|
| DEP-03-03-006 (UPSTREAM PREREQUISITE) | DEL-03-03 → DEL-03-01 | Catalog and read-basis definitions; availability and standing expectations | **Held** (representative) | C §3, §4.1, §5, §6, §8 X column, §10 ↔ ADAPTER §4.2 (L360–382), §4.3 RD-1…RD-5, §3.2, §11 (L1052) | **RD-2 against C §5.2 rule 1.** R8-12 item 6 lets a whole-model identity satisfy RD-2, and ADAPTER says "C §5.2 rule 1 is not amended here" (L1217–1223). C §5.3 covers the whole-model case; C §5.2 rule 1 (L345–347) still makes a read lacking *any* element *basis incomplete*, and ADAPTER L399–400 records that SWBPIPE main has no workspace identity or generation. Neither file states the result for that read |
| DEP-03-03-007 (UPSTREAM PREREQUISITE) | DEL-03-03 → DEL-03-02 | Proposal, validation and outcome definitions | **Held** (representative) | P §2–§9.1, §13 (L706) ↔ ADAPTER §4.5, §5, §6, §7, §11 (L1053) | The phase and standing of "constraint not carriable on this host" (2.6) |
| DEP-03-03-008 (UPSTREAM PREREQUISITE; maturity TBD) | DEL-03-03 → DEL-04-01 | Adopted operation-policy distinctions | **Admitted**. Mirror DEP-04-01-023 says INITIALIZED: one of the two maturity differences DAG-003 lists | ACT §2.6 (L423), §4.4, §5.3, §6, V-10 (L1382), FX-24/25/42/47/50 ↔ ADAPTER §3.1, §3.3, §6 RP-3, §11 (L1054) | None found at the anchors checked |
| DEP-03-03-012 (DOWNSTREAM HANDOVER) | DEL-09-09 → DEL-03-03 | Fixture results, candidate basis, remaining external requirements | **Held**; MIRROR of DEP-09-09-009 | ADAPTER §10, §9, §12 ↔ XT L42, XC-01…XC-12 (cite L-ADAPTER-n and XF-nn) | None found |
| DEP-03-03-013 (UPSTREAM INTERFACE; "N-B4") | DEL-03-03 → DEL-01-01 | Supplier MCP/dynamic-tool surfaces and channel-status facts at pin 0.158.0 | **Admitted** | HOSTING §6.7 (L559), §6.8 (L631), §8.3 (L785), H1/H6/H8/H9 (L201–241), U-19; PIN-SPIKE §4–§6 ↔ ADAPTER §3.5 (L311–326), S-X8, §3.4 | ADAPTER records HOSTING as read at v0.3 and v0.4 (L16, L19); the body cites v0.6 by label (R8-12 item 7). No command-execution item facts in ADAPTER §3.5 (3.5) |
| DEP-03-03-014 (UPSTREAM INTERFACE; "N-27") | DEL-03-03 → DEL-02-03 | Checkpoint statement for the current phase; governance-phase hold machine, hold-support values, required-tool check | **Held** | EXEC §2.1 PH-1…PH-10 (L208–224), §2.2, §3.6 (L381) ↔ ADAPTER S-X12, §5.3, §7.7 | None in meaning |
| **N-24** (DEP-02-03-026) | DEL-02-03 → DEL-03-03 | "observations of checkpoint arrivals and act records on the external channel" | **Held**; reciprocal with N-27 | ADAPTER §7.7 (L819–837) ↔ EXEC §9.1 (L1201: "§7.7 checkpoint observation on X"), §4.4 events | Present as prose. No element list for an observation and no mapping to EXEC §4.4. EXEC records "ADAPTER-v0.2 read; v0.3 relayed; Current: v0.4" |
| — (DEP-04-02-022, in DEL-04-02's register) | DEL-03-03 → DEL-04-02 | Visible autonomy state | **Held** | AS §3 ↔ ADAPTER §5.5, §11 (L1055) | No UPSTREAM row in ADAPTER's register; supplier statement only |
| — (DEP-02-01-027, in DEL-02-01's register; maturity TBD) | DEL-03-03 → DEL-02-01 | Declared checkpoint constraints for carriage, governance phase | **Held** | WD §4.2.2 ↔ ADAPTER §5.3 GC-4, §11 (L1057) | No UPSTREAM row in ADAPTER's register |
| — (DEP-04-03-026, in DEL-04-03's register) | DEL-04-03 → DEL-03-03 | External dispatch entries | **Held** | ADAPTER §5.1, §11 (L1062) ↔ RS §10 (row DEL-03-03) | RS §10 says DEL-03-03 "Consumes R5 destination; R7 external entries; R9; R11; R13". ADAPTER L18 lists RS "for joins only" among its inputs and L23 says "By join, not registered here: … DEL-04-03 (record entries R7/R9/R11/R13)". Arc N-B8 (DEL-03-03 → DEL-04-03) is absent by owner decision; the wording is an open DAG-003 matter with the DEL-03-03 owner |
| (other registers) DEP-03-04-007; DEP-09-06-029 | consumers → DEL-03-03 | — | **Admitted** | S1-E | — |

N-18, N-21 and X-1 do not touch DEL-03-03.

## 3.7 Carried review items that name ADAPTER

| Item | State | Evidence |
|---|---|---|
| V6 (R7-1 check; minors) | R7-1 holds; no minor names ADAPTER | GC-5 HS-5 bullet, L611–618 |
| C1-B S-03-1…S-03-5 | **Applied** by SCA-V4-001 | SoW diff; RV-3_DEL-03-03 |
| RV-3_DEL-03-03 observation (CLM-002 tail) | **Applied** by SCA-V4-002 | SoW AX-005 |
| C1-B N-B4, N-B7 | **Applied** as DEP-03-03-013, -014 | register |
| C1-B N-B5, N-B6 | Present only as supplier rows DEP-04-02-022, DEP-02-01-027 | 3.6 |
| C1-B N-B8 | **Decided**: not proposed (BASIS-ALIGN DECISION-6). The ADAPTER header wording behind it is **open** | DAG-003 open matters; L18, L23 |
| C1-B M-03-1 (mirror → DEL-03-04) | **Open** | register; L23 "no DOWNSTREAM mirror in this register — F-11" |
| C1-B §3.5 / GUIDE G-9 (§12 header said RELAY-v0.2) | **Fixed** | L1069; GUIDE F-13 "Closed" |
| V9 N-2 (V4-HOST-02 marker in §3.4) | **Fixed**, then superseded by R8-13 | L1302–1303 |
| V10 S-2 (attribution) | **Open in the body.** L301 still reads "The owner's revised wording:"; V10b carried it | L301 |
| V10 N-1 (consumed-input sentence) | **Open** | L8 |
| V10 N-6 | No action asked | — |
| "The 17 Design re-pins" | **Open**; this pass | 3.1 |

## 3.8 Recommended work on ADAPTER in this pass

1. **Re-pin and restate the basis.** New SoW hash and the four doc hashes; remove both "flagged" labels; fix L301 and the L8 sentence; re-word S-X10 to the amended V4-HI-42; review the V4-EXM-23 citation in the §3.4 heading. [3.1, 3.3, 3.7]
2. **Align to the revised SoW.** Close F-10, F-13, F-14 and the L1330 row; re-word E-2 against the revised AC-002; add the host-adoption row to §1 (REQ-005); update L23 for DEP-03-03-013/-014; re-word L18 and L23 so they read as supply to DEL-04-03, not consumption; name AX-004 and AX-005. [3.2, 3.6, 3.7]
3. **Settle the design target for the seam** (owner or integrator): develop the CLI path to the same depth as MCP, or stay neutral. Then add the supplier facts for the chosen path to §3.5. [3.5]
4. **Add the observation-to-record mapping:** native item fields → dispatch-record elements → RS R7/R9/R11/R13; and the element list of a §7.7 observation mapped to EXEC §4.4 events (N-24). [3.5, 3.6]
5. **Add a channel-state transition table** and the relaunch, reconnect and discovery sequences. [3.5]
6. **Specify the simulated endpoint** XF-01…42 run against, once, shared with C, P and XT. [3.5]
7. **One bounded spike at pin 0.158.0** with the DEL-01-01 node: command-execution item content for a JSON CLI; per-thread MCP configuration; the MCP-call A14 path; per-turn destination facts (A3, A12, A21, A30). [3.4]
8. **State the result for a host read that lacks workspace identity or generation** (with C). [3.6]
9. **Settle the standing of the PROPOSED App-side rules** (A29) and mark OC-2 as decided for this increment (A2). [3.4]

Optional: move the superseded input lists (L11–L20, about 9 KB) into a history note; the header is hard to check as it stands.

Not in this pass, and why: selecting the transport as binding (V4-HI-50 gives the host the choice, and joins are deferred); interposed families and App-side holds (D6, governance phase); live host variants (no A13 facility; DECISION-3); in-flight custody across relaunch (DEL-01-02, outside the 14); any code (OUT-001 stays a definition here); register rows.

---

# Closing table

| | C (DEL-03-01) | P (DEL-03-02) | ADAPTER (DEL-03-03) | Total |
|---|---:|---:|---:|---:|
| Stale pins | 13 | 13 | 19 | **45** |
| — cited content changed (S) | 7 | 5 | 10 | 22 |
| — bytes only (A) | 6 | 8 | 9 | 23 |
| Open items, NOW | 6 | 9 | 5 | 20 |
| Open items, OWNER | 5 | 4 | 3 | 12 |
| Open items, HOST | 14 | 10 | 15 | 39 |
| Open items, SPIKE | 1 | 1 | 4 | 6 |
| Open items, LATER | 2 | 3 | 4 | 9 |
| Open items, all | 28 | 27 | 31 | 86 |

Several items recur across the files (OI-003, OI-014, OI-021, host adoption, R8-Q4b, the capture-after-arrival question, the consequence vocabulary, U-C2/U-C3, U-P10, the M3-CP spike). Counted once each, the OWNER class holds **five** distinct choices (rows 2–6 of the owner-level table below).

**The three most consequential gaps.**

1. **The catalog is defined as meanings, not as an interface (C).** There is no discovery or edition interface, no edition or currency states, no read-result content model, no meaning for a historical read, and no schema form. Four consumers already rely on the *catalog edition*, which C still marks PROPOSED; DEL-05-01's register row asks for "schemas and catalog identity"; and the first host has no catalog at all (U-C13). (1.5, 1.6)
2. **Proposal identity and outcome observation are not an interface (P; consumed by LOOP and ADAPTER).** P does not say who mints the identity, offers no read of recorded state by identity, and has no outcome for the same identity with different content. Retry, lost-acknowledgment recovery and PI-1…PI-6 depend on all three. Beside it: P's acceptance unit (the change item) has no counterpart on the first host, whose Apply accepts and applies a batch in one step. (2.5)
3. **Nothing in the three files can be executed (all three; sharpest in ADAPTER).** No test double or simulated endpoint is specified, although 42 XF cases and 22 VC cases presume one. ADAPTER selects nothing for OUT-001, records no supplier facts for the CLI path that is the only seam on record, and A13 cannot be evidenced on the first host. AC-004 of DEL-03-01 is held for the same reason. (1.5, 2.5, 3.5)

**Owner-level choices found** (none is settled by this survey).

| # | Choice | Where it arises | Standing |
|---|---|---|---|
| 1 | Custody and home of the shared fixture FX-PIPE-01 | C §10 L622–625; CLOSEOUT_ACCOUNT "Consequences routed"; C1-B §1.5 | Routed to the owner at the first closeout; no decision found in later run records |
| 2 | OI-003: retain, narrow or defer the extension promise | C L919; P L840; ADAPTER L1325 | Open; "defer" can be chosen now |
| 3 | OI-014: placement of shared contracts and components | C L920; P L841; ADAPTER L1327 | Open; bears on "no further structural change anticipated" |
| 4 | Capture at or after arrival, versus counting a prior act bound to current content (SP-6; U-E4/U-31/U-26) | C L936; P L633–635 | Routed to the owner at the first closeout; PROPOSED in the files |
| 5 | R8-Q4b: whether a launch variable the person sets counts as A13 evidence | C L271–273; P L621; ADAPTER L204–205 | Deferred by R8-6 until UI-SUCCESSOR resumes; it decides whether any live case against SWBPIPE can run |
| 6 | Open description of catalog descriptors as an extension of V4-SHR-02 | C L107–111 | PROPOSED (F-C9) |
| 7 | *(my inference)* The design target for the external seam in this pass: CLI path developed to MCP depth, or transport-neutral | ADAPTER §2, §3.5, §9 | Not raised in any file |
| 8 | *(my inference)* After a direct application at a declared A5 checkpoint in the current phase: is the A5 still requested (amended V4-HI-42; DEL-02-03 REQ-002 "even where the applicable operation autonomy otherwise allows direct application") or "no A5 is required" (R8-12 item 2)? | silent in C L757, P L388–392, L739, ADAPTER XF-25 | The owner confirmed the R8-11 item 2 reading at SCA-V4-001 (OWNER_ITEMS, "Confirm the reading"); R8-12 item 2 was not put to the owner. May be settled by an integration ruling if the two are read as consistent |
