# S1-E — scoping survey: DEL-09-06, DEL-09-09, DEL-03-04

- **Run / node:** APP-V4-DESIGN-PASS-2-20260930, node S1-E. One Type 2 TASK executor (Claude Code subagent; parent HELP_HUMAN). No delegation. Read-only git; no network. This file is the only file written.
- **Date:** 2026-09-30. **Candidate:** working tree at `4698471d9e` on `claude/chirality-app-v4-60-percent-a41fd5` (only `SURVEY/` untracked).
- **Files surveyed:** CA = DEL-09-06 `CONNECTED_ACTIVITY_CONTRACT.md` (CA-v0.4); RELAY = DEL-09-06 `RELAY_QUESTIONS_SWBPIPE.md` (RELAY-v0.3); XT = DEL-09-09 `EXTERNAL_TRACE_CASES.md` (XT-v0.4); GUIDE = DEL-03-04 `HOST_INTEGRATION_GUIDE.md` (GUIDE-v0.3). ANS = `RELAY_ANSWERS_SWBPIPE.md` and FACTS = `FACTS_SQ01_SQ32.md` were read as data about SWBPIPE only.
- **Paths** are relative to `projects/chirality-app-v4/execution` unless they start with `docs/`.

## 0. What I read and how I checked

**Read whole:** this run's BRIEFS.md and OWNER_DECISIONS.md; CA, RELAY, XT, GUIDE; ANS; the three ScopeOfWork.md files; DEL-09-06 `_DEPENDENCIES.md`; `HANDOFF_SWBPIPE_DOMAINS.md`; `_DAG/DAG-003/HANDOFF_STATE.md`; `loop/LOOP_INIT.md` "Develop the detail appropriate to the phase"; intake `R8_RESOLUTIONS.md` and `OWNER_DECISIONS.md` (DECISION-3, -4, -5); first-run `reviews/V6.md` and `closeout/CLOSEOUT_ACCOUNT.md`; `RV/RV-4_DEL-09-06.md`.

**Read in part (stated so the limits are clear):**

- `INTAKE_MAP.md`: method, the STD rules, every Part 1 row whose Dependent cell names CA, RELAY, XT or GUIDE (by script: CA 29 rows, XT 23, GUIDE 33, RELAY 10, some shared), Part 2.0–2.1, Parts 3, 4 and 5. Not the Part 1 rows for other files, nor Part 2.2.
- DEL-09-09 and DEL-03-04 `_DEPENDENCIES.md`: everything except the row tables (the rows were read from the CSVs).
- The three `Dependencies.csv`: every ACTIVE EXECUTION row whose target is one of the 14, in full.
- `closeout/C1-B.md` §4 (DEL-03-04) and `C1-C.md` sections DEL-09-06 and DEL-09-09.
- `reviews/V9.md` (inputs, method, verdict, checks 4–5, residuals, V9b) and `V10.md` (residual table, V10b).
- `APP-V4-BASIS-ALIGN-20260928/reviews/V11–V13` and `APP-V4-SCA002-20260929/reviews/V14–V16`: searched for the four file names, "Design", "re-pin" and the three deliverable IDs; the hits were read. `RV-3_DEL-03-04.md` and `RV-4_DEL-09-09.md`: result, hashes, E-blocks and checker lines.
- FACTS: headings and preamble only.
- The 13 sibling Design files: headings, the lines that name DEL-09-06, DEL-09-09 or DEL-03-04, and EXEC §2.1–§2.2, RS §10, P §9.1, ADAPTER §10 (tail) and §11. Not read whole.
- R1–R7 were not re-read; I rely on the Design files' citations of them.

**Checks run (scratch only):**

- `shasum -a 256` of every current Design file, run-record file, SoW, register and basis doc; every 64-hex string in the four files was extracted and matched against those (202 file/hash pairs).
- Every pinned hash that matches no current file (64 distinct) was matched to a committed blob with `git show <commit>:<path> | shasum`. All 64 resolve. So a "stale" pin below means *true of the commit it names, not the current bytes*.
- `git diff 6e18505e3 HEAD -- docs/` for the amended requirement texts; `git diff 340ecf341^ 340ecf341` for the three SoW revisions.
- Script: every sibling section citation (`X §n.n`) in the four files against the headings of the current sibling file (CA 111, XT 51, GUIDE 568, RELAY 100 citations: all resolve); every sibling-owned identifier (XF-, MT-, CH-, PH-, NW-, PC-, … ) against the current owner file (none missing).
- `tools/scope_of_work/check_boundary_owner_resolution.py` on the three current SoWs: each returns 1 boundary requirement checked, 0 failing.
- DAG-003 `DependencyEdges.csv` / `CandidateEdges.csv` / `ExcludedRows.csv` for every arc with an end in my row.

**Arcs N-18, N-21, N-24, X-1.** None has an end in DEL-09-06, DEL-09-09 or DEL-03-04 (consumers DEL-02-01 and DEL-02-03; suppliers DEL-03-02, DEL-03-03, DEL-01-04). They reach my files only through text: CA cites EXEC MX-5/MX-6 and CH-23 (the item-level decisions and the App act control those arcs carry); XT XC-10 and CA W14-04 (iii′) rest on ADAPTER §7.7 observations (N-24); GUIDE M5.3 and M8.4 index them. See each file's section 6.

---

# A. DEL-09-06 — `CONNECTED_ACTIVITY_CONTRACT.md` (CA-v0.4; last changed at `f5ceef164`, 2026-09-28 18:22)

## A.1 Pins

The file states (l.8) that its "v0.4 inputs" and the R8-12 line are the current basis, and that l.10–24 are "the history of earlier bases". I count only l.2–9 and l.26 as active pins. The 48 hashes in l.2 and l.10–24 and the change tables are history; all resolve to committed blobs.

| # | Line | Pin | Status | How checked | Current value |
|---|---|---|---|---|---|
| 1 | 6 | "repo 6e18505e3 (accepted basis)" | **stale** | `git diff 6e18505e3 HEAD -- docs/`: PRD, ARCHITECTURE, HOST_INTEGRATION, EXAMINATION changed (SCA-V4-001 at `230bf1e64`/`a0af39f8c`; SCA-V4-002 at `70376aff2` for HOST_INTEGRATION) | basis docs at HEAD |
| 2 | 6 | ScopeOfWork.md `511f2c00…9b37` | **stale** | shasum; revised at `340ecf341` | `287d47a1260e7433c3f16578c67345d067472165421c65848bd15e44d92a7923` |
| 3 | 6 | Dependencies.csv `ce3218a2…97ed` "(ACTIVE EXECUTION rows DEP-09-06-012…024)" | **stale** | shasum; CSV read | `0f8ecad83cca72f7c65786ff0cd0252a2b7664c145a6e39193cff332a639f2f6`; rows 012…**034** (025–032 deliverable rows, 033 relay handover, 034 DECISION-3 constraint) |
| 4 | 6 | `docs/PRD.md` `657593ce…8573` | **stale** | shasum | `bb6e786f7a6c01dc5ce2f16f58e6c600989a12808ff47ce4fd87924bcc6c49bd` |
| 5 | 6 | `docs/HOST_INTEGRATION.md` `08c8fc7d…60da` | **stale** | shasum | `d4331c39db7f452cd3ba72fdfa4bad540a6053931218359a93646971acb28d9f` |
| 6 | 6 | `docs/EXAMINATION.md` `1b156553…ee19` | **stale** | shasum | `471798bc2f2dc0202ae40d9d5cf033a22ae41af2a0afdf58032cf37a687957d0` |
| 7 | 6 | `HANDOFF_SWBPIPE_DOMAINS.md` `6e7a2f04…5ef4` | **stale** | shasum (file changed at `948f4a308`, `7a1508452`, `1650a5a06`) | `76edf2361f392a7eb516abb10bf0a91e59f3802388e95b0e4685009f9e0aa405` |
| 8 | 6 | first-run BRIEFS.md "working copy" `77a42f8a…a21f` | **stale** | shasum | `35cbc97437b13b3d237ef7ee1c433fa0f32f4fbea41292ff060eb81b27a9e491` |
| 9 | 6 | first-run OWNER_DECISIONS `f3f8e5f3…1f2e` (DECISION-1 state) and `a9869129…ad2c` (DECISION-2 state) | current (`a986…`); `f3f8…` is an earlier state of the same file | shasum; git | `a9869129…ad2c` |
| 10 | 6 | R1 `2f9c7e72…`, R2 `77cfb845…`, R3 `202d52c7…`, R4 `50a009b2…` | current | shasum | unchanged |
| 11 | 8 | R8_RESOLUTIONS.md `d4c34233…e7af` (R8-12 state) | **stale** | shasum; the file gained R8-13 at `1528a5033` | `44bc9a8df4fe73e3f41711e7d9593a065734b054400f12bb01695a30e7b30e6b` |
| 12 | 8 | Sibling version labels (EXEC-v0.4, WD/WD-EX-v0.6, C/P-v0.6, ADAPTER-v0.4, GUIDE-v0.3, ACT/AS/RS-v0.6, LOOP/PANEL-v0.6, HOSTING-v0.6, PIN-SPIKE-v0.1, XT-v0.4, RELAY-v0.3), "as committed at `7a1508452` with A6's in-place R8-12 edits" | labels current; **bytes moved** for C, ADAPTER, ACT, AS, RS, LOOP, PANEL, HOSTING at the R8-13 pass (GUIDE l.37) | contribution lines of each sibling; GUIDE table | same labels; R8-13 is not mentioned anywhere in CA |
| 13 | 8 | "SWBPIPE's `RELAY_ANSWERS_SWBPIPE.md` and `FACTS_SQ01_SQ32.md` are unchanged" | **stale for ANS** (true for FACTS) | shasum; RELAY §4 l.1047 | ANS was revised in place by SWBPIPE (`a999f4ba1`, #1048) |
| 14 | 9 | INTAKE_MAP.md `3cc18295…ea33` | current | shasum | unchanged |
| 15 | 9 | intake BRIEFS.md `3e33ba26…7517` | **stale** | shasum | `6f32809d58d150d684baa5185c7bd54fe82da5f7173b34eddd2f4ab90cfc03b4` |
| 16 | 9 | intake OWNER_DECISIONS.md `a5ccab0d…e776` | **stale** | shasum; DECISION-5 and its confirmation added later | `5fd780bf90a4d51751d2c2fa632b92111a52cd0d9445a0870be9d28bcb4f40b2` |
| 17 | 9 | EXEC-v0.4 `d32be377…76d4` | **stale** | shasum | `092f248682447df74e93915527930f4b90367fac46b867dad18daef3c5c608ff` |
| 18 | 9 | WD-v0.6 `fce565ed…2f28` | **stale** | shasum | `43a9962f025de384e1cdaedea9a648da74e20216476a04f2394cfa3851f47eb9` |
| 19 | 9 | WD-EX-v0.6 `950b70b2…ba3d` | **stale** | shasum | `8d60ed7850e6935b8410217c8867c59554c7de9aec28c60514e88ff5f0cff36e` |
| 20 | 9, 26 | ANS `6f01add3…61c7` | **stale** | shasum | `afb6e063e7e5dfccf8986206f888cf1e2e1c4e7fc3430fdf86db670714fc0e74` |
| 21 | 23 | PIN_SPIKE-v0.1 `0e090a4c…b115` | current | shasum | unchanged |
| 22 | 540–543 (§11.1) | Body citations of C and ACT "cited at `8fb51f07f` (v0.4)", ADAPTER "cited at v0.2", P/AS/RS/LOOP/PANEL/HOSTING "cited at `8fb51f07f` (v0.4)" | version lag, stated by the file itself (F-17, l.623) | script: every cited section number and identifier exists in the current sibling | sections exist; content not compared line by line |

**Quoted requirement texts.** CA quotes two requirement texts that have since changed, both in F-22 (l.633):

| CA quotes | Current text |
|---|---|
| SoW REQ-003: "A declared checkpoint waits for its required human act even under direct autonomy" | REQ-003: "A declared checkpoint's required human act is requested and recorded only when the person performs it, even under direct autonomy (in the current phase the checkpoint is plan guidance and no hold is exercised; a hold is exercised only for a workflow that takes up the governance phase, TBD-003)" |
| SoW AC-004: "holds a declared checkpoint …" | AC-004: "never records a declared checkpoint's act as performed when the required human act is absent despite direct autonomy (holding the checkpoint only for a workflow in the governance phase)" |

The V4-EXM-14 quote in §8.3 (l.478) still matches `docs/EXAMINATION.md` l.115–116.

**Stale count:** 15 hash or commit pins (rows 1–8, 11, 15–20; row 13 is the same ANS pin as row 20) and 1 quoted-text group = **16**.

## A.2 ScopeOfWork alignment (SoW `287d47a1…`)

| SoW item | Where CA answers | Depth |
|---|---|---|
| CLM-001 staged first activity; acceptance is not completion | §0, §6 | developed |
| CLM-002 integration owner; four user activities | §2.1, §5, §10 "Retained here" | developed |
| CLM-003 (revised: suppliers named by deliverable; DEL-01-01 supplies supplied-guidance and model-destination evidence) | §5 rows, §11.1; §4 "supplied" row; W14-08 | developed; §11.1 still cites v0.4/v0.2 texts (A.1 row 22) |
| CLM-004 external SWBPIPE owner; DEP-001 standing | §5 host row; §9; §10 | developed |
| CLM-005 (revised: OI-001/002 ruled by D2/D3); fallback-replacement decision | S-2, S-8, S-9; §2.5; §10 | developed for policy; the replacement decision is only named (§10 row "replacement packet", VC-CA-08) |
| CLM-006 distinct qualification owners | §5; §10 | developed |
| OUT-001 increment SoW, owner/check allocation, handoff | §2.1–§2.5, §5, §6 | partial by statement: a draft on the fixture; the operation-specific SoW waits for OI-021 |
| OUT-002 reusable workflow | §3.1 WR-1…WR-11; §3.2 fixture WF-1/WF-1c | requirements only; no workflow authored (DEL-02-02, later) |
| OUT-003 joined V4-EXM-14 witness | §4; §8 W14-00…W14-10 | designed, not run; cannot complete (F-1) |
| OUT-004 (revised: names RELAY, ANS, CA §9 and the seven-step ladder; answers stand at *answered*) | §7.2; §9; RELAY §4 | developed |
| REQ-001 | §2 | developed on the fixture |
| REQ-002 | §3, §4 | developed as requirements and link table |
| REQ-003 (revised) | W14-03, W14-04, W14-07, W14-10 | developed in two phases; lags listed below |
| REQ-004 | S-4…S-14; CA-H; W14-04/05/06 | developed |
| REQ-005 | §7.2; §9 | developed |
| REQ-006 | §6 ST-0…ST-5 | developed |
| REQ-007 | §8.1, §8.3, §7.1 | developed (the rule) |
| REQ-008 (revised list) | §10 | developed; "supplier observation belongs to App DEL-01-01" appears as "hosting construction and focused checks" |
| AC-001…AC-008 / VER-001…VER-008 | VC-CA-01…VC-CA-08 | designed, not run. AC-001's "all seven assigned scope items": SOW-236, -237, -240, -241 are named only in VC-CA-01 (l.740); no section is traced to them in the body |
| TBD-001 (OI-021) | §2.5; UNRESOLVED | developed |
| TBD-002 (revised) | S-8, S-9 | consistent; F-3 lags |
| TBD-003 (new) | (a) S-12; (b) S-13, W14-04; (c) header, §8.1 | partial: never cited by ID; W14-09 (l.472) has no phase statement, though TBD-003 (b) says D6 bears on "made usable in App" (W14-09) only in the governance phase |
| AX-004 (amendment reference) | — | absent |

**Where CA contradicts or lags the revised SoW:**

1. l.6: SoW and register hashes and the row range (A.1 rows 2–3).
2. F-22 (l.633) and the UNRESOLVED row at l.724 quote the pre-revision REQ-003 / AC-004 / VER-004 wording and route it to "the next accepted-basis update". The SoW was revised on 2026-09-29 (RV-4 return: E-0906-05).
3. F-3 (l.571) "SoW still calls OI-001/OI-002 open — Carried to C1". TBD-002 and CLM-005 now state the D2/D3 rulings.
4. F-2 (l.570) "Dependencies.csv lacks deliverable-level rows — Carried to C1". Rows DEP-09-06-025…032 exist.
5. l.27 (Receivers) cites DEP-09-06-020 for the OUT-004 relay. The register's relay handover row is DEP-09-06-033; DEP-09-06-034 (DECISION-3 constraint) is not cited anywhere.
6. The header "Serves" line (l.5) names only the question file for OUT-004; the SoW also names ANS.
7. CA's Phase-1 text never says the act "is requested". The SoW (REQ-003) and the amended basis do (A.3).

## A.3 Amended basis

| Requirement | CA text | Agreement |
|---|---|---|
| **V4-WF-05** (amended: act requested; not recorded until performed; holding "phased to the governance layer, not withdrawn"; no enforcement, block or *unsupported* for a hold reason in the current phase; reserved acts unaffected) | Header l.4; S-5 (l.78); S-13 (l.86); W14-04; VC-CA-04 | Intent agrees. **Wording lags:** l.4, F-22 and l.724 say the first half "is flagged for the next accepted-basis update"; the basis now carries it. CA says arrivals "may be recorded" (S-13, PH-6) and never says the required act "is requested" at the arrival; the amended text keeps "the required human act is requested" as a current-phase statement. The nearest CA wording is in S-14, for a lapse: "the agent asks again as its plan requires". Who makes the first request, and what a witness observes of it, is not stated (CA follows EXEC §2.1, whose PH-1…PH-10 do not mention a request either) |
| **V4-HI-42** (amended: "a checkpoint's required act is requested and recorded as done only when the person performs it"; holding phased; reserved acts still bind) | S-5: "its 'or a declared checkpoint' half, WD I-7 and V4-HI-42 are **plan guidance**" | **Wording disagrees.** Under the amended text V4-HI-42 has a binding part in the current phase (request; record only when performed) and a phased part (the hold). CA calls the whole requirement guidance and places the record rule on "V4-WF-05's second half". R8-11 item 2 was written against the old one-sentence V4-HI-42 |
| **V4-EXM-22** (amended: "requests a human act … recorded only when the person performs it, whatever the autonomy; stopping the run … examined only for a workflow that takes up the governance phase") | §2.4 graduated-autonomy branch (l.239); §5 row AS → DEL-09-07 | CA cites V4-EXM-22 only as an overlap; W14-04 (ii′) matches the amended meaning except for "requests" |
| **V4-HI-70** (amended: adds "for a host's agent, each network destination contacted") | Basis line cites V4-HI-70/71; CA-0 evidence "run record R1, R2, R6"; W14-08 | **Not reflected.** For the CA/E variant no step, evidence cell or W14 case mentions destinations contacted (RS R15). CA predates R8-13 |
| **V4-HOST-01, V4-HOST-02, V4-ARC-11, V4-ARC-12, V4-EXM-23** | Not cited. §2.2 CA/E row points to SQ-29…SQ-32 | No conflict in CA's own text. DECISION-5 is not mentioned; the CA/E host contributions (allow list, in-work grants) have no relay question (see B and D) |
| **"local-first"** | Not used in CA | — (the phrase survives in HANDOFF l.22; section E) |

## A.4 Open items (27)

| # | Item (ID in CA) | What is open | Owner / point of need (as CA states) | Class |
|---|---|---|---|---|
| 1 | `UNRESOLVED{OI-021}`; DI-1, DI-2 (autonomy), DI-3; EC-12 | Operation(s), non-mutating check, autonomy, environment, acting-surface variant | Owner via outside SWB session with App/shared owner; before connected-activity SoW and execution | **OWNER** — which operation and check, which autonomy, and which expression (CA/E, CA/X, or the development-Codex CLI journey SWBPIPE names) |
| 2 | UNRESOLVED row 2 | Operation-specific reserved additions | Same owners; before operation-policy production contracts | **OWNER** (follows 1) |
| 3 | UNRESOLVED row 3 | Host adoption of D2/D3 and treatments | SWBPIPE owner (OI-016); before any enforcement claim | **HOST** |
| 4 | DI-4; EC-01…EC-11, EC-13, EC-14 | Host contributions; all *answered*, none committed or delivered | SWBPIPE owner; when UI-SUCCESSOR resumes | **HOST** |
| 5 | UNRESOLVED row 5 (DEP-09-06-024) | Actual human acts for W14-04/05/06 | The person; at witness execution | **HOST** (needs a live candidate) |
| 6 | DI-6; `UNRESOLVED{D6}` | App-side run holds | Owner; when the governance phase is taken up | **LATER** — closed for Phase 1 by DECISION-4 |
| 7 | DI-9; UNRESOLVED row 7 | Host A13 enablement facility | SWBPIPE owner decision | **HOST** |
| 8 | UNRESOLVED row 8 (R8-Q4b) | Whether a person-set launch environment variable counts as A13 evidence | Owner, deferred; when UI-SUCCESSOR resumes | **OWNER** (deferred by R8-6) |
| 9 | UNRESOLVED row 9; F-16 (EXEC U-E4) | Capture-after-arrival (PROPOSED) versus counting prior acts | Owner; before hold-machine fixtures run | **OWNER** — a record rule that also runs in Phase 1 (F-16, l.622) |
| 10 | DI-7; UNRESOLVED row 10 (ACT U-03) | Multi-row A4 purpose after partial lapse | DEL-04-01 with the owner | **OWNER** (W14-06 partial-lapse variant HELD on it) |
| 11 | UNRESOLVED row 11; F-1 | DEL-02-02 registration | DEL-02-02 owner; before W14-01/W14-09 | **LATER** (outside the 14) |
| 12 | UNRESOLVED row 12; F-19 | V4-HI-32 per-subject identity not met by SWBPIPE | SWBPIPE (PB-TBD-002 / DEL-16-03) | **HOST** |
| 13 | UNRESOLVED row 13 (l.724); F-22 | "V4-WF-05's first half and SoW REQ-003 / AC-004 / VER-004 hold wording … next accepted-basis update" | Owner | **NOW** — `docs/PRD.md` V4-WF-05 (amended by SCA-V4-001) and SoW `287d47a1…` REQ-003, AC-004, VER-004 |
| 14 | UNRESOLVED row 14; F-20 | Host joins; naming the App's Codex as a caller | Owner (DECISION-3) | **HOST** |
| 15 | UNRESOLVED row 15; F-4 | DEL-09-01 protocol; DEL-09-07 qualification | Their owners | **LATER** (outside the 14) |
| 16 | UNRESOLVED row 16 | OI-013 / OI-014 placement | Shared contract owner with SWB implementation owner; App/shared owners | **OWNER** |
| 17 | DI-8; UNRESOLVED row 17 | App v4 OI-003 extension promise | Owner with host contract owner | **OWNER** |
| 18 | UNRESOLVED row 18 | Workflow authoring and review (OUT-002 artifact) | Workflow maker with DEL-02-02 | **LATER** |
| 19 | DI-2 tail | Grant display for a host without grants ("host fixed treatment …"), PROPOSED | — (AS U-20: DEL-04-02 with the integrator; when host joins resume) | **LATER** (deferrable by R8-10) |
| 20 | F-2 | Register lacks deliverable rows | C1 | **NOW** — `Dependencies.csv` `0f8ecad8…` rows 025–032 |
| 21 | F-3 | SoW calls OI-001/002 open | C1 | **NOW** — SoW TBD-002, CLM-005 |
| 22 | F-8 | HANDOFF "approval" wording | C1 | **NOW** — HANDOFF `76edf236…`, row "Autonomy and human acts" uses A5/A4/A6/A7 |
| 23 | F-17 (l.623) | §2.3 step citations name the `8fb51f07f` texts; "not re-verified section by section" | next pass | **NOW** — the current sibling files (my script finds every cited section and identifier present) |
| 24 | F-18 | No governed checkpoint examinable as enforced against SWBPIPE on either surface | Owner, with D6 | **LATER** (governance phase) |
| 25 | F-21 | Apply per batch, no A10 record, no undo receipt: no SWBPIPE counterpart for T11, *partial*, "reverses ⟨receipt⟩" | recorded | **HOST** |
| 26 | §7.2 (l.416) | The ladder is labelled PROPOSED (W9) | — | **NOW** — SoW OUT-004 now states the same seven-step ladder |
| 27 | §3.1 (l.279) | WR-1…WR-11 are PROPOSED (W9) | open to owner revision | **LATER** — settled when the workflow is authored and reviewed |

Case states (not counted above): W14-00…W14-10 all AWAITING INPUT with the STD-2 annotation (HOST); W14-06's partial-lapse variant HELD on U-03. No item needs a spike: CA's only executable stage (ST-1, test doubles) needs App construction, which this file places in a later undertaking.

**Counts:** NOW 6 · OWNER 7 · HOST 7 · SPIKE 0 · LATER 7.

## A.5 Depth against the 60% description

Contributions DEL-09-06 exchanges: it consumes eleven first-increment deliverables (A.6), DEL-02-02 and DEL-09-01 (outside), SWBPIPE (DEP-001), the owner's OI-021 choice and a person's acts; it supplies the step map and staging to DEL-09-07, the relay questions and answers to DEL-03-04, and the question set to SWBPIPE.

| Aspect | What CA has | What is missing |
|---|---|---|
| Interfaces | §11.1/§11.2 name each supplier and receiver; §2.3 names the contribution per step by section; §9 names each external contribution with its SQ | (a) No result-record definition for a W14 case (XT §3.4 has one; CA has only labels in §7.1 and outcome words in §8.1). (b) The "supplied to DEL-09-07 / DEL-05-01 / DEL-05-02 / DEL-04-03" rows of §11.2 name topics, not the elements handed over. (c) No statement of the join keys between the App run record (RS) and host evidence for W14-05/08 beyond "capture-evidence reference" |
| States | Case states (DESIGNED / AWAITING INPUT / HELD); the seven ladder standings (§7.2); stages ST-0…ST-5 | No evidence requirement per ladder step beyond one phrase each ("an explicit statement of commitment" and so on); no condition table for the draft contract becoming the operation-specific one (DI-1…DI-3 are listed, the transition is not) |
| Data | Fixture identities (B1/B2, PR-1/PR-2, RC-1…RC-3, ⟨set-1⟩/⟨set-2⟩); W14-00 identification | The data each step leaves is named by label ("Evidence the step yields") and held by reference to RS/P/C; acceptable for an integrating file, but nothing states which RS elements a Phase-1 run must leave when checkpoints are only guidance (arrival records are "may") |
| Operating sequences | One fixture sequence (§2.4) with a graduated-autonomy branch; the link table of the round trip (§4) | (a) §2.4 is written in hold words ("waiting", "waits for A4") with a reading note added after it; there is no sequence written for Phase 1. (b) The round trip has no ordered procedure with actors (EXEC §6.3/§6.5 have it; CA §4 is a link matrix). (c) No sequence maps the steps onto anything SWBPIPE has: the "no counterpart" notes (l.245–257) say what is absent, not what the activity would be on the candidates ANS lists (SQ-04: inspect → preview → submit → the person's Apply → status, on Node `position.x`) |
| Failure behaviour | CA-4 (stale), CA-5 (lost acknowledgment, unknown), channel states (§2.2), §8.3 "what cannot substitute" | The step map has no failure column. For CA-0, CA-1, CA-2, CA-3, CA-H and CA-R the file does not say what the activity does, or what record is left, when the exchange fails (check not established, basis incomplete, refused or not exposed, host check unavailable, act declined, return with unknowns). LOOP_INIT asks for "behavior when the exchange fails" for each exchanged contribution |
| Verification | VC-CA-01…08 (definition checks, not run); W14 cases with their EXEC rehearsal cases ("Built on") | VER-002 asks to compare a reviewed workflow's bytes at App and host: no workflow exists. No VC checks pins or sibling currency. W14 "Built on" lists differ slightly from EXEC RT-11 (A.6) |

**Structural choices still open that could force restructuring of CA or a consumer:**

1. **OI-021.** The step map, §2.4, W14-04/05/06 and the fixture assume per-item A5/A10, grants and subject identities. SWBPIPE's only wired journey has per-batch Apply, no A10, no grants and a whole-model identity (ANS SQ-01, -03, -04, -05). If the owner selects that journey, CA-H, CA-5, the branch at l.239 and three W14 cases change shape, and so do XT XC-02, XC-08, XC-10 and §3.3.
2. **Acting-surface variant.** CA defines CA/E and CA/X. SWBPIPE has no loop (CA/E) and names a development Codex, not the App's Codex, for CA/X. Staging (§6 ST-4) and the DEL-09-07 / DEL-09-09 split depend on which expression comes first.
3. **Whether OUT-003 has a host side at all in this increment.** SWBPIPE has no workflow library (SQ-17). CA records it (§4, §8.1). Nothing says which W14 cases remain examinable App-side meanwhile.
4. **U-E4** (capture at or after arrival): decides which recorded act answers which arrival in W14-05, in both phases.
5. **The `governed` flag** (WD §4.3.1, PROPOSED): WR-5 and WR-11 are written around it.

## A.6 Joins (ACTIVE rows to the 14; all eleven arcs are in DAG-003's admitted layer)

| Row | Arc | Contribution (register statement) | Supplier's Design file has it? | Used in CA | Notes and disagreements |
|---|---|---|---|---|---|
| DEP-09-06-013 | → DEL-02-03 (DAG-001 arc) | Execution compatibility; transfer/adaptation behaviour | Yes. EXEC §9.2 (l.1214) names DEL-09-06 and what it gets; RT-11 (l.1163) maps MT/CH/RT cases to W14 | §2.2, §2.3 CA-0, §4, §8.2 "Built on" | **Small disagreements in the W14 map.** CA W14-05 cites CH-20, which RT-11 does not list; RT-11 lists CH-30 under W14-06, which CA does not cite; CA puts CH-9 under W14-07, RT-11 puts it in W14-06's range (CH-6…CH-10) |
| DEP-09-06-015 | → DEL-04-03 (DAG-001 arc; RequiredMaturity TBD here, INITIALIZED in mirror DEP-04-03-031 — HANDOFF_STATE lists the difference) | "records of actual content-bound acts" | Partly. RS §10 (l.455) says DEL-09-06 consumes "R2 transfer links" | CA-0 (R1, R2, R6), CA-3 (R10), CA-H (R8, R9), CA-5 (R7, R11), §4 "observed behavior" | **Disagreement.** The SoW and CA use act records (R9), arrivals (R8), operation entries (R7) and evidence limits (R11); RS states only R2 transfer links for this consumer |
| DEP-09-06-016 | → DEL-05-01 (DAG-001 arc) | Loop/model receiving requirements | Yes: LOOP §2.2, §2.4, §6; LOOP §10.1 (l.1345) names the joined witness DEL-09-06 as receiver of host evidence | §2.2 CA/E; CA-1, CA-2, CA-4, CA-5 (FX-V1, FX-V2/V3, FX-D2, FX-O1) | CA cites LOOP at v0.4 for the fixtures; identifiers exist in LOOP-v0.6. LOOP's header still pins RELAY-v0.2 for the question map (S1-D's file) |
| DEP-09-06-017 | → DEL-05-02 (DAG-001 arc) | Panel receiving requirements | Content yes (PANEL §3.5, §5). PANEL names DEL-09-06 only as the owner of the relay file (header l.25), not as a receiver | CA-H | No receiver statement on the supplier side |
| DEP-09-06-025 | → DEL-02-01 (N-19) | Portable declaration, identity and revision meaning | Content yes (WD §3.4, §4.1–§4.5, §4.3.0, §4.3.1, §6.1–§6.4; WD-EX E1, E1c, E1d, E8). WD §8 "What each receiver receives" has no DEL-09-06 row; DEL-09-06 appears only in WD's header and change rows | §3.1 WR-1…WR-11; §3.2; §8.2 | No receiver statement on the supplier side |
| DEP-09-06-027 | → DEL-03-01 (N-C2) | Catalog/read-basis meanings | Content yes (C §5, §6, §8, §10). C §1 parties table lists DEL-09-09, not DEL-09-06 | §2.3 (every step), §3.2, §7.1 | No receiver statement |
| DEP-09-06-028 | → DEL-03-02 (N-C3) | Proposal/outcome meanings | Content yes (P §3–§9; §9.1 SWBPIPE vocabulary). P §13 provides to DEL-03-04 and DEL-09-09, not DEL-09-06 | CA-2, CA-4, CA-5 | CA restates the R8-5 outcome mapping itself (l.245–257) and does not cite P §9.1; the two texts agree |
| DEP-09-06-029 | → DEL-03-03 (N-C4) | External-receiving meanings | Content yes (ADAPTER §3–§7, XF inventory). ADAPTER §11 lists DEL-09-06 under "Expect from" (RELAY), not "Provide to" | §2.2 Channel; CA-0…CA-5; W14-04, W14-05 | CA §11.1 says "Cited at v0.2. Current: ADAPTER-v0.4" |
| DEP-09-06-030 | → DEL-04-01 (N-28) | Adopted operation policy and act distinctions | Content yes (ACT §2.6, §4.6, §5.3, §6). ACT §10 names DEL-09-09 and DEL-03-04 as consumers, not DEL-09-06 | S-8, S-9; CA-2, CA-H; §5 | No receiver statement; ACT §2.7 (A12 network-destination subclass, R8-13) is not reflected in CA |
| DEP-09-06-031 | → DEL-04-02 (N-08) | Grant display | Content yes (AS §3, §4, §8; §3 also has the PROPOSED "host fixed treatment" display, U-20). AS names DEL-09-06 only in its header | CA-0; CA-H; CA-R; DI-2 | No receiver statement |
| DEP-09-06-032 | → DEL-01-01 (N-C5) | App-side supplied-guidance and model-destination evidence | Content yes (HOSTING §8.2, §8.3). HOSTING §8 "Seams to receivers" does not name DEL-09-06 (only the header l.9) | §4 "supplied" row; S-12; W14-08 | No receiver statement |

Incoming: **DEP-03-04-022** (DEL-03-04 → DEL-09-06, N-B10, admitted): the guide consumes the relay questions and recorded answers. CA §11.2 has no DEL-03-04 row (it names DEL-09-07, DEL-09-09, DEL-02-03, DEL-05-01, DEL-05-02, DEL-04-03, SWBPIPE, the owner). No reverse row may be added (guard E-5 in HANDOFF_STATE). DEP-09-06-026 (→ DEL-02-02) and DEP-09-01-024 are outside the 14 (S1-F).

## A.7 Carried review items

| Item | Status | Evidence |
|---|---|---|
| V6 m-1, m-3…m-7 | None names CA as the side to change. V6 checked CA §2.2, S-14 and W14-06 and found them holding | V6 §1–§2 |
| Closeout D9-6-1 (CA §5 / §11.1 standing cells) | **Fixed** | §5 l.357–367 and §11.1 l.540–543 name the post-R8 versions (R8-12 item 7) |
| C1-B §4.5 / GUIDE F-11 (CA-H hold statement unqualified by surface) | **Fixed** | CA-H (l.215); GUIDE F-11 "Closed (R6-5)" |
| V9 (intake) | No CA residual. V9 compared CA with EXEC, WD-EX and GUIDE values and found them consistent | V9 check 3 |
| V9 N-4 analogue | **Open in CA, not raised by V9:** the ANS revision (`afb6e063…`) was recorded only in RELAY and GUIDE; CA l.8–9, l.26 still pin `6f01add3…` | A.1 rows 13, 20 |
| BASIS-ALIGN and SCA002 reviews | None names CA. They carry "the 17 Design re-pins" as an open derivative (DECISION-8; V13 F4; DAG-003 HANDOFF_STATE open matters) | grep |

## A.8 Recommended work in this pass

1. **Re-pin the header** to the amended basis docs, SoW `287d47a1…`, register `0f8ecad8…` (rows …034), R8_RESOLUTIONS `44bc9a8d…`, intake OWNER_DECISIONS `5fd780bf…`, the current EXEC/WD/WD-EX bytes and ANS `afb6e063…`; cite SCA-V4-001/002 and DAG-003; bump to CA-v0.5. [A.1]
2. **Replace the "flagged for the next accepted-basis update" statements** (l.4, F-22, l.724) with the amended V4-WF-05 / V4-HI-42 and the revised REQ-003 / AC-004 / VER-004; close F-2, F-3, F-8 and F-22; cite TBD-003 and AX-004; give W14-09 its phase note. [A.2, A.3, A.4]
3. **State the Phase-1 reading of "the act is requested"** in S-5, S-13, CA-H and W14-04 (ii′), and reword S-5's "V4-HI-42 is plan guidance". This follows the EXEC owner's text, so it must come after the EXEC node. [A.3]
4. **Re-verify the §2.3 and §8.2 citations** against the post-R8-13 siblings and drop the v0.4/v0.2 labels (F-17); reconcile the W14 "Built on" lists with EXEC RT-11 (CH-20, CH-30, CH-9). [A.1, A.6]
5. **Add a failure column to the §2.3 step map** (per step: what fails, who reports it, what record is left, what the activity does next) and a **W14 result-record definition**. [A.5]
6. **Rewrite §2.4 as a Phase-1 sequence** with the governance reading as the annotation, not the reverse. [A.5]
7. **Carry amended V4-HI-70** into the CA/E evidence cells (RS R15) and note DECISION-5 where CA/E is described. [A.3]
8. **Fix register citations** (DEP-09-06-033, -034) and add DEL-03-04 to §11.2 as a receiver of the relay files. [A.2, A.6]
9. **Optional, if the integrator wants an owner package:** an OI-021 option sheet in §2.5 that maps CA-0…CA-R onto the candidate operations ANS lists, showing per step what has a SWBPIPE counterpart. It prepares the choice; it does not make it, and it claims no join. [A.4, A.5]

**Not in this pass:** selecting the operation, autonomy or environment (OI-021, owner); authoring the workflow (DEL-02-02 and `create-workflow`); running any W14 case; redesigning the governance-phase parts (retained, D6 closed for Phase 1); editing the SoW or register; editing ANS or FACTS.

---

# B. DEL-09-06 — `RELAY_QUESTIONS_SWBPIPE.md` (RELAY-v0.3; last changed at `1650a5a06`)

The file states (l.3) that the relayed body, §0–§3, "is kept as relayed and is not edited after relay (R8-7)". Only the header, §4, the change tables, UNRESOLVED and the VCs are App metadata. V9 hashed §0–§3 and found them identical to the relayed bytes; I recomputed it: lines from `## 0.` up to `## 4.` hash to `6e399c83…0d4d` both in the working tree and at `c6f81a4f2`, the commit the ledger names as relayed.

## B.1 Pins

| # | Line | Pin | Status | Current value |
|---|---|---|---|---|
| 1 | 5 | "repo 6e18505e3 (accepted basis)" | **stale** (as A.1 row 1) | — |
| 2 | 5 | DEL-09-06 SoW `511f2c00…` | **stale** | `287d47a1…` |
| 3 | 5 | `docs/HOST_INTEGRATION.md` `08c8fc7d…` | **stale** | `d4331c39…` |
| 4 | 5 | `docs/EXAMINATION.md` `1b156553…` | **stale** | `471798bc…` |
| 5 | 5 | `docs/PRD.md` `657593ce…` | **stale** | `bb6e786f…` |
| 6 | 5 | HANDOFF `6e7a2f04…` | **stale** | `76edf236…` |
| 7 | 5 | first-run BRIEFS `77a42f8a…` | **stale** | `35cbc974…` |
| 8 | 7 | R8_RESOLUTIONS `d4c34233…` | **stale** | `44bc9a8d…` |
| 9 | 5 | R1, R2, R3, R4; OWNER_DECISIONS `a9869129…` | current | — |
| 10 | 22, 1047 | ANS `6f01add3…` "revised in place by SWBPIPE to `afb6e063…`" | current (both states recorded) | `afb6e063…` |
| 11 | 22, 1047 | FACTS `733fb88a…` | current | — |
| 12 | 7 | Sibling version labels (post-R8) | labels current; R8-13 not mentioned | — |

Historical byte states of RELAY itself (l.2, l.1045, l.1076, l.1083) and of earlier siblings (l.8–21) all resolve to committed blobs.

**Quoted requirement texts in the relayed body that the amended basis no longer supports (frozen; not editable under R8-7):**

| RELAY text | Current basis text |
|---|---|
| SQ-30 "Why it matters" (l.867–868): "In local operation the host agent's only destination is the configured server (V4-HOST-02); V4-EXM-23 observes all host traffic to verify it." | V4-HOST-02: "A host's agent sends data only to the model service the person selected and to destinations the person has allowed — in advance in an allow list … or when the agent asks during its work. … Every destination contacted is recorded and shown" |
| SQ-30 (b) (l.855–857): "Is a user-controlled local server the default, with cloud used only when the person chooses it and supplies a key" | V4-HOST-01: "a model server the user controls, or a cloud model reached by OAuth sign-in or an API key. There is no default between them" |
| SQ-30 "App assumes meanwhile" (l.873): "NW-1…NW-3 are SETTLED from the accepted basis" | The basis those rules rested on was amended; LOOP-v0.6 rewrote NW-1…NW-7 and added NW-8…NW-16 |
| SQ-16 (l.565): "V4-HOST-02 continues to govern your embedded agent" | True of the amended V4-HOST-02, which now means something different |
| SQ-02 question (l.124–126): "the App contracts require that the operation be resolved as *propose* in that run, even under a direct grant (V4-HI-42; D2)" | V4-HI-42 as amended: request and record only when performed; the hold is phased. In the current phase this is plan guidance (R8-11 item 2) |

**Stale count:** 8 hash or commit pins and 1 frozen group of quoted texts = **9**.

## B.2 ScopeOfWork alignment

| SoW item | Where RELAY answers | Depth |
|---|---|---|
| OUT-004 (revised) question set, recorded answers, account, ladder | §1–§3 (32 questions, priority groups, source map); §4 ledger | developed; the ledger records relay and answers, and "none" for commitments, contributions, adoption and examination |
| REQ-005; AC-005 | §0 "What it is not"; §4; VC-R-04, VC-R-05 | developed |
| VER-005 (trace from questions through received answers to dependent items) | VC-R-04, VC-R-06 | designed, not run. VC-R-06 is "when answers arrive": the answers arrived and the intake run traced them (INTAKE_MAP, R8), but no record says VC-R-06 was run |
| REQ-001 / TBD-001 "decision/input account" | SQ-04, SQ-05 | developed; answered with no selection |

Lags against the revised SoW: the header SoW pin (B.1 row 2); l.23 (Receivers) cites DEP-09-06-018/-019/-020, while the register's row for this file's handover is now DEP-09-06-033. Nothing in the relayed body conflicts with the revised SoW text itself.

## B.3 Amended basis

All disagreement is in the frozen body and is listed in B.1. App-side metadata (header, UNRESOLVED) mentions none of V4-HOST-01/02, V4-ARC-11/12 or V4-EXM-22/23. Two consequences are recorded elsewhere and not here: GUIDE M7.9 and its UNRESOLVED row (l.790) say the DECISION-5 host obligations have no question and "wait for the next relay"; V10 N-7 says SQ-30 keeps the old V4-HOST-02 wording. RELAY's own UNRESOLVED table has no row for either.

## B.4 Open items (10)

| # | Item | What is open | Owner / point of need | Class |
|---|---|---|---|---|
| 1 | UNRESOLVED row 1 | SWBPIPE owner decisions (ANS §2, §4): UI-SUCCESSOR, OI-016, durable receipt carrier, PB-TBD-002 / DEL-16-03, Checked mark, MCP adapter, D-58 successor, DEC-051, a host-held route, an A13 facility, a work item to receive App workflows | SWBPIPE owner; when the owner resumes UI-SUCCESSOR | **HOST** |
| 2 | `UNRESOLVED{OI-021}` | The selection | Owner via outside SWB session and App/shared owner | **OWNER** |
| 3 | `UNRESOLVED{OI-003}` | Extension disposition | Owner with host contract owner | **OWNER** |
| 4 | `UNRESOLVED{D6}` | App-side run holds | Owner; governance phase | **LATER** |
| 5 | R8-Q4b row | Launch environment variable as A13 evidence | Owner, deferred | **OWNER** |
| 6 | l.1133 | "Closeout pointer from HANDOFF … to this file; and the R8-8 note there" | Closeout C1; the HANDOFF's editor | **NOW** — HANDOFF `76edf236…` has both (section "Current detailed question set"; "Note for SWBPIPE (owner direction, DECISION-4 D4-2)") |
| 7 | l.1097 | "nine sub-questions added" | — | **NOW** — the change table above it includes SQ-02 (f) (R7-2): ten (V6 m-3) |
| 8 | §3 "Not included" | WD U-10 (host origin in precedence) | DEL-02-02 with DEL-02-01 and the host owner; when DEL-02-02 is defined | **LATER** |
| 9 | not in RELAY's UNRESOLVED (GUIDE l.790; V10 N-7; intake RECEIPT) | No question asks the DECISION-5 host obligations; SQ-02, SQ-16 and SQ-30 carry superseded premises | App manager via the human; when UI-SUCCESSOR resumes | **HOST** (next relay) |
| 10 | §4 ledger; ANS SQ-27 (c) | "No relay form is agreed"; commitments, contributions, adoption, examination: none | SWBPIPE owner | **HOST** |

**Counts:** NOW 2 · OWNER 3 · HOST 3 · SPIKE 0 · LATER 2.

## B.5 Depth against the 60% description

RELAY is a question set and a ledger, not a design of an exchange, so the six aspects apply narrowly.

| Aspect | Has | Missing |
|---|---|---|
| Interfaces | Each SQ gives question, dependents, reason, point of need, working assumption and an answer form; §3 maps every source item to a question | No question for host-agent network destinations (DECISION-5), for the caller naming, or for how a per-batch host meets the V4-EXM-25 completion rule |
| States | Ledger fields with a standing ladder (answer · stated intention · commitment · delivered contribution) | — |
| Data | §4 per-answer record fields (SQ id, answering party, revision, date, custody, standing, dependents, limits) | The ledger holds one aggregate row for all 32 answers; the per-answer records it defines were not written (the intake map serves that purpose outside this file) |
| Sequences | §0 "Answer handling" | — |
| Failure | Partial answers and "not yet known" accepted; an answer moves a case only when it supplies the named input | — |
| Verification | VC-R-01…VC-R-08 designed, not run | VC-R-06 has no run record although its trigger occurred |

Structural point: the file cannot be corrected in place. Any change of question or premise is a new relay artifact. The owner's start direction for this run did not select the relay.

## B.6 Joins

RELAY adds no arc of its own; its joins are DEL-09-06's. The exchanges that pass through this file:

| Exchange | Supplier side | Consumer side | Agreement |
|---|---|---|---|
| Source questions → RELAY | LOOP §13 Q-1…Q-7; PANEL §8 Q-1…Q-9; ADAPTER §12; ACT U-04; EXEC host items | RELAY §3 map | LOOP (l.26) and PANEL (l.25) headers still pin the RELAY-**v0.2** map; ADAPTER §12 cites RELAY-v0.3 at an older byte state (`89b6b9c9…`). The SQ identifiers they use are unchanged |
| RELAY + ANS → GUIDE (DEP-03-04-022, N-B10, admitted) | RELAY §2, §4; ANS | GUIDE §4.3 (one home and one answer gist per SQ); GUIDE pins RELAY `c93f8cc5…` and ANS `afb6e063…` | current and consistent |
| RELAY → XT | RELAY SQ-12…SQ-16, SQ-26…SQ-28 | XT §2 IN rows | consistent. The revised DEL-09-09 SoW (CLM-004) calls these files "a coordination route, not an input this examination consumes", and the register holds no DEL-09-09 → DEL-09-06 row (guard E-1) |

## B.7 Carried review items

| Item | Status | Evidence |
|---|---|---|
| V6 m-2 (R7 commit "recorded in the WORK_GRAPH") | **Fixed** | §4 "Prepared" row (l.1044) names `c6f81a4f2`; first-run WORK_GRAPH V6 row: "m-2 fixed here" |
| V6 m-3 (sub-question count) | **Open** | l.1097 still reads "nine sub-questions added" |
| Closeout D9-6-2 ("Prepared" row version history) | **Fixed** | l.1044: v0.1, v0.2 (sweep A1), v0.3 (R5 pass) |
| V9 S-1, S-2 (provenance of the ANS revision; splice) | **Fixed** | l.1047; V9b table |
| V9 N-4 (header cites only the delivered hash) | **Fixed** | l.22 |
| V10 N-7 (SQ-30 quotes the old V4-HOST-02) | **Open by design** | "Carry to the next relay" |

## B.8 Recommended work in this pass

1. **Metadata only:** re-pin the header (B.1 rows 1–8), cite DEP-09-06-033, leave §0–§3 byte-identical and re-hash them to prove it. [B.1, B.2]
2. **Correct the sub-question count** (V6 m-3) and **close the UNRESOLVED row at l.1133**. [B.4, B.7]
3. **Add one UNRESOLVED row** (metadata) listing what the next relay must carry: the DECISION-5 host obligations (GUIDE M7.9, HC-7.7…HC-7.9), the superseded premises of SQ-02, SQ-16 and SQ-30, the caller naming and the per-batch completion question (XT F-18). [B.3, B.4]

**Not in this pass:** any edit to §0–§3; drafting or relaying a successor question set (the owner did not select the relay, and host joins are deferred by DECISION-3); recording VC-R-06 as run without a reviewer.

---

# C. DEL-09-09 — `EXTERNAL_TRACE_CASES.md` (XT-v0.4; last changed at `f5ceef164`)

## C.1 Pins

Active pins are l.6, l.8, l.9 and l.17; l.10–16 are stated history (all resolve to committed blobs).

| # | Line | Pin | Status | Current value |
|---|---|---|---|---|
| 1 | 6 | "repo 6e18505e3 (accepted basis)" | **stale** | basis docs at HEAD |
| 2 | 6 | ScopeOfWork.md `082db8fa…862d` | **stale** | `e887a579f75335aa91b59ae195053eabae81ce031fe91136df5c81df2297e53a` |
| 3 | 6 | Dependencies.csv `02d738c7…fbe2` "(ACTIVE EXECUTION rows DEP-09-09-007…020)" | **stale** | `e0e3297adb7350c58694aae88062d1bb35778c4440a5e91374f3d8c7c9663bb8`; rows 007…**024** |
| 4 | 6 | `docs/EXAMINATION.md` `1b156553…` | **stale** | `471798bc…` |
| 5 | 6 | `docs/HOST_INTEGRATION.md` `08c8fc7d…` | **stale** | `d4331c39…` |
| 6 | 6 | `docs/PRD.md` `657593ce…` | **stale** | `bb6e786f…` |
| 7 | 6 | SCC-CASE-002 `Case_Datasheet.md` `6acdc6c4…71a6` (rows M2-A, M4-J, M4-X) | **stale** | `a12abfaf82c34ae1e7c10d8b553d3e1a0da4772b160e02257c0bf70edce04d5c`; the three row labels are still present; the datasheet gained successor observations at DAG-002 and DAG-003 |
| 8 | 6 | first-run BRIEFS `77a42f8a…` | **stale** | `35cbc974…` |
| 9 | 6 | R1–R4; OWNER_DECISIONS `a9869129…` | current | — |
| 10 | 8 | R8_RESOLUTIONS `d4c34233…` | **stale** | `44bc9a8d…` |
| 11 | 9 | INTAKE_MAP `3cc18295…` | current | — |
| 12 | 9 | intake BRIEFS `3e33ba26…` | **stale** | `6f32809d…` |
| 13 | 9 | intake OWNER_DECISIONS `a5ccab0d…` | **stale** | `5fd780bf…` |
| 14 | 9 | EXEC-v0.4 `d32be377…` | **stale** | `092f2486…` |
| 15 | 9 | WD-v0.6 `fce565ed…` | **stale** | `43a9962f…` |
| 16 | 9 | WD-EX-v0.6 `950b70b2…` | **stale** | `8d60ed78…` |
| 17 | 9, 17 | ANS `6f01add3…` | **stale** | `afb6e063…` |
| 18 | 8 | Sibling labels, "SWBPIPE's … files are unchanged" | labels current; ANS claim stale; R8-13 not mentioned | — |
| 19 | §2 IN-04…IN-08, IN-22, IN-29 | C-v0.6, P-v0.6, ADAPTER-v0.4, ACT-POLICY-v0.6, RS-v0.6, LOOP-v0.6, AS-v0.6 | labels current | — |
| 20 | body | Section citations "still name the `8fb51f07f` texts and were not re-verified" (F-17, l.492) | lag stated by the file; my script finds all 51 cited sections and all cited identifiers in the current siblings | — |

XT quotes no requirement text that has changed. The "original promise" in §5.2 paraphrases V4-PAR-05 / V4-HI-03, which the amendments did not touch.

**Stale count:** **15** (rows 1–8, 10, 12–17).

## C.2 ScopeOfWork alignment (SoW `e887a579…`)

| SoW item | Where XT answers | Depth |
|---|---|---|
| CLM-001 | §0, §7 | developed |
| CLM-002 (revised: adds DEL-05-01, DEL-04-02, DEL-02-03 as suppliers) | §2 IN-04…IN-08, IN-22, IN-25, IN-29 | developed; two cells lag (below) |
| CLM-003 | §7 | developed |
| CLM-004 (revised: relay files are a coordination route, not a consumed input) | §0; §2 lead; §7 last row | consistent |
| OUT-001 suite and candidate-bound evidence | §3 (J-1…J-8; XC-00…XC-12; §3.3; §3.4) | suite designed; no evidence (not run) |
| OUT-002 one-operation trace | §4 (TS-0…TS-5; CMP-01…15; TR-01…10) | plan only |
| OUT-003 work account and disposition | §5 | structure only |
| REQ-001 | §2, §8 | developed |
| REQ-002 | XC-01, XC-10, XC-12 | developed |
| REQ-003 (revised: "canonical content identity with its identity-method designation") | J-2 (l.125) | developed; wording matches |
| REQ-004 (revised: host obligation to be evidenced; "one effect unevidenced") | XC-03…XC-08 | developed; XC-05 already uses the phrase |
| REQ-005 | §4 | developed (plan) |
| REQ-006 | §5.2 | developed |
| REQ-007 | XC-09 | developed |
| REQ-008 | §3.4, §6 | developed; the interface-evidence protocol is DEL-09-01's and does not exist |
| REQ-009 (revised: adds three exclusions) | §7 | **partial** — see below |
| AC-001…AC-009 / VER-001…VER-009 | VC-T-01…VC-T-09 | designed, not run |
| TBD-001 (OI-003), TBD-003 (OI-021), TBD-004 (OI-005) | UNRESOLVED | developed |
| TBD-002 (revised) | IN-07 | consistent; F-1 lags |
| TBD-005 (new) | S-9; XC-10; §3.3 Gate; header | content present; never cited by ID |
| AX-005 | — | absent |

**Where XT contradicts or lags the revised SoW:**

1. l.6: SoW and register hashes and the row range.
2. **§7 (l.388–403) lacks three owners that REQ-009 now enumerates:** embedded-loop receiving definition (DEL-05-01), grant display definition (DEL-04-02), compatibility-report and hold-support definition (DEL-02-03). VC-T-09 ("§7 one-for-one against REQ-009") would not pass.
3. IN-22 (l.103) "**Not registered** in DEL-09-09 Dependencies.csv (F-2)" and IN-29 (l.110) "not registered in DEL-09-09 Dependencies.csv (F-2)". Rows DEP-09-09-021 (DEL-05-01), -022 (DEL-04-02) and -023 (DEL-02-03) exist.
4. F-1 (l.438) "SoW still calls OI-001/OI-002 open"; F-2 (l.439; "Stands", l.489). Both are met by the revised SoW and register.
5. F-6 (l.443) "'One domain effect' reading — Unchanged (reading stated)". REQ-004 now states that reading.
6. VC-T-01 (l.600) checks "DEP-09-09-007…020"; the range is now …024 (row 024 is the DECISION-3 constraint).

## C.3 Amended basis

| Requirement | XT text | Agreement |
|---|---|---|
| V4-WF-05 / V4-HI-42 | S-10 (l.68): "WD I-7 and V4-HI-42 are guidance; the host's own treatment decides (R8-11 item 2)"; XC-10 two-part | Intent agrees. Same wording lag as CA: the amended V4-HI-42 has a binding request-and-record part that XT calls guidance as a whole. The header (l.4) does not carry a "flagged for the next basis update" note, so there is less to correct than in CA or GUIDE |
| V4-EXM-22 | not cited | — (XC-10 / TR-05 use the direct branch; the overlap is with DEL-09-07) |
| V4-HI-70 (network destinations in the host run record) | not touched; XT cites 70/71 for "linked, never copied" | no conflict; the E surface of the trace (IN-22) does not mention destination records |
| V4-HOST-01/02, V4-ARC-11/12, V4-EXM-23, "local-first" | not cited or used | — |

XT concerns the external channel and the App's Codex; DECISION-5 governs host agents only, so its absence here is consistent.

## C.4 Open items (22)

| # | Item | What is open | Owner / point of need | Class |
|---|---|---|---|---|
| 1 | `UNRESOLVED{OI-003}`; IN-12; §5.2 | Retain / narrow / defer | Owner with host contract owner; before claiming extension capability | **OWNER** |
| 2 | `UNRESOLVED{OI-021}`; IN-10; XC-10's XF-28 part HELD | Operation, autonomy, environment | Owner via outside SWB session | **OWNER** |
| 3 | OI-005; IN-13 | Additional essential hosts | Owner; before freezing wider scope | **OWNER** |
| 4 | DEL-03-03 TBD-007 | MCP versus CLI; realization family | App external-host integration owner with external host owner | **HOST** (the host selects the seam, V4-HI-50; SWBPIPE has a CLI in DRAFT #885) |
| 5 | DEP-001 inputs IN-02, IN-09, IN-11, IN-15…IN-20, IN-23, IN-24, IN-26…IN-28 | Host contributions; *answered*, none supplied | SWBPIPE owner | **HOST** |
| 6 | DEP-09-09-015/016; IN-21 | The person's A13; the engineer's A5 | The person; at live execution | **HOST** |
| 7 | `UNRESOLVED{D6}`; IN-25 | Holds on X | Owner; governance phase | **LATER** |
| 8 | A13 facility row; IN-15 | No facility exists | SWBPIPE owner decision | **HOST** |
| 9 | R8-Q4b row | Launch variable as A13 evidence | Owner, deferred | **OWNER** |
| 10 | Host joins; caller naming (F-20) | The App's Codex as a named caller | Owner (DECISION-3) | **HOST** |
| 11 | V4-HI-32 / per-item staleness (F-19) | Not met by SWBPIPE | SWBPIPE | **HOST** |
| 12 | DEL-09-01 protocol; IN-03; F-3 | Candidate/date protocol; interface evidence protocol | DEL-09-01 owner | **LATER** (outside the 14) |
| 13 | Host adoption of D2/D3 | — | SWBPIPE owner (OI-016) | **HOST** |
| 14 | F-1 | SoW calls OI-001/002 open | C1 | **NOW** — SoW `e887a579…` TBD-002 |
| 15 | F-2; IN-22; IN-29 | Register lacks rows | C1 | **NOW** — `Dependencies.csv` `e0e3297a…` rows 021–023 |
| 16 | F-6 | "One domain effect" reading | — | **NOW** — SoW REQ-004 as revised |
| 17 | F-17 (l.492) | Section citations not re-verified | next pass | **NOW** — current sibling files |
| 18 | F-18 (l.498); §3.3 | How the completion rule reads for a host whose A5 is per-batch Apply with no A10 | "the integrator when host joins resume" | **HOST**. Not in the UNRESOLVED table |
| 19 | F-22 | No capability catalog, editions or per-operation identity on SWBPIPE: the trace has no counterpart | recorded as evidence for OI-003 | **HOST** |
| 20 | F-8 | V4-EXM-25 / V4-EXM-24 comparison overlap, "noted for DEL-09-07" | — | **LATER** (DEL-09-07 is outside the 14) |
| 21 | IN-01 | App candidate identity | App construction (later undertaking) | **LATER** |
| 22 | IN-29 tail | Grant display for a host without grants, PROPOSED | — | **LATER** (deferrable, R8-10) |

Case states (not counted): XC-00…XC-12 and TR-01…TR-10 all AWAITING INPUT; XC-09 negatives, XF-25, XF-26 and XF-42 parts DESIGNED; XF-28 part HELD. No SPIKE item: the test-double rehearsals are DEL-03-03's XF cases.

**Counts:** NOW 4 · OWNER 4 · HOST 9 · SPIKE 0 · LATER 5.

## C.5 Depth against the 60% description

Contributions DEL-09-09 exchanges: it consumes eight first-increment deliverables (C.6), DEL-09-01, SWBPIPE contributions and two human acts; it supplies the trace and work account to DEL-03-01 (DEP-03-01-030) and the external trace cases to DEL-03-04.

| Aspect | What XT has | What is missing |
|---|---|---|
| Interfaces | J-1…J-8 with an evidence owner each; the input account IN-01…IN-29 with supplier and need; the result record (§3.4); the work-account columns (§5.1); the disposition record (§5.2) | What DEL-03-01 receives under DEP-03-01-030 is named ("trace and work evidence") but not tied to the §5.1 columns and C §8's cells one for one |
| States | Case states; outcome values (passed · failed · blocked · not run · inconclusive); comparison result values (§4.3); completion rule (§3.3) | — |
| Data | Chain elements; comparison categories CMP-01…15; account rows surface × element | For a host like SWBPIPE, no mapping from its identifiers (`preview_ref`, `idempotency_key`, `ticket`, `basis_identity`) to J-2, J-3 and J-6; the "Receiving SWBPIPE" paragraphs (l.133–147, l.278–287) give meanings only |
| Operating sequences | Fixture steps per case; stages TS-0…TS-5 | No run order for the suite on one candidate, no fixture set-up or reset between cases (XC-03 needs r12→r13, XC-08 needs an edit between T11 and T12), and no table of which candidate change reopens which case (§6 says only that changes reopen "affected" cases) |
| Failure behaviour | Expected negative outcomes per case; §3.4 "diagnosis and repair without weakening its criterion"; evidence limits | No rule for a case blocked mid-suite (what the remaining cases may still show); XC-06's recorded-violation path is the only per-case failure treatment |
| Verification | VC-T-01…09; a rehearsal column mapping each XC to ADAPTER XF cases | — (the rehearsals cannot run until DEL-03-03's simulated endpoint exists) |

**Structural choices still open:**

1. **DEL-03-03 TBD-007** (MCP versus CLI, realization family): "XC cases run per family actually selected". The J-1 and J-3 evidence differs by family.
2. **OI-003 disposition:** decides which criterion §5.2 examines and whether the three-surface trace stays three surfaces.
3. **Per-batch Apply versus per-item A5/A10** (F-18): changes XC-02, XC-08 and the completion rule.
4. **No embedded surface on SWBPIPE** (IN-22): V4-EXM-24's "human, embedded and external" comparison has two surfaces at most against the first host.
5. **OI-021:** the operation that XC-02 and TR use.

## C.6 Joins

DAG-003 admits only DEL-09-09 → DEL-04-01 (and → DEL-09-01, outside). The other seven arcs are held candidates inside SCC-002 (non-gating). N-C6, N-09 and N-26 were added at DAG-002.

| Row | Arc; DAG-003 | Contribution | Supplier's Design file has it? | Used in XT | Notes and disagreements |
|---|---|---|---|---|---|
| DEP-09-09-007 | → DEL-03-01; held (SCC-002) | Catalog/read-basis contract, operation/model basis, surface responsibility map | Yes: C §3–§6, §8, §10 (V-ED1, e1/e2). C names DEL-09-09 as receiver (l.78, §8 l.550, l.575, UNRESOLVED l.938) | IN-04; J-2; §4.1; CMP-01…06; §5.1 | consistent. Reciprocal arc DEP-03-01-030 (DEL-03-01 consumes the trace; held): C l.575 "The evidence route is DEL-09-09's" matches XT §5.3 |
| DEP-09-09-008 | → DEL-03-02; held | Proposal, validation and outcome meanings | Yes: P §5–§12; P §13 (l.711) provides "§11 scenario, §12 risks, VC-P cases" to DEL-09-09; mirror DEP-03-02-022 | IN-05; J-3, J-4, J-6; XC-03…XC-08 | consistent; P §4.2 note (l.319) names XT XC-08 as having no SWBPIPE counterpart, as XT says |
| DEP-09-09-009 | → DEL-03-03; held | External receiving contribution and focused fixtures | Yes: ADAPTER §3–§10; §11 (l.1060) provides the inventory and "rehearsals for XT XC-05 and XC-06 (XF-40, XF-41)"; rehearsal map (l.1041): XC-05 → XF-19, XF-40; XC-06 → XF-19, XF-21, XF-41 | IN-06; "Rehearsal" column | **agree** |
| DEP-09-09-010 | → DEL-04-01; **admitted** | Adopted operation policy and act distinctions | Yes: ACT §2, §2.6, §4.6, §5.3, §6, §9; ACT §10.1 lists DEL-09-09 as a consumer of V-08, V-11, V-13, V-14, V-20/V-22 (l.1380–1394) | IN-07; XC-09; XC-10; CMP-07 | consistent |
| DEP-09-09-011 | → DEL-04-03; held | Evidence-record contribution | Content yes (RS R7, R9, R11, §6). RS §10 has **no DEL-09-09 row** (DEL-09-09 appears only in RS's header) | IN-08; J-8; XC-09 | No receiver statement on the supplier side |
| DEP-09-09-021 | → DEL-05-01; held (N-C6) | Embedded-loop receiving for the E surface of the trace | Content yes (LOOP §2.2, §6, §11). LOOP names DEL-09-09 only in its header | IN-22; CMP-03 (LOOP V-3) | No receiver statement; XT still says "Not registered" |
| DEP-09-09-022 | → DEL-04-02; held (N-09) | Grant display states | Content yes (AS §3). AS's receivers line (l.12) does not name DEL-09-09 | IN-29; XC-10; CMP-07 | No receiver statement; XT still says "not registered" |
| DEP-09-09-023 | → DEL-02-03; held (N-26) | Per-surface compatibility report; hold-support values (governance phase) | Content yes (EXEC §3 EV-5, CR-7, §3.6). EXEC §9.2 has no DEL-09-09 row (header only) | IN-25; TS-0; XC-10 | No receiver statement |

Incoming: **DEP-03-04-023** (DEL-03-04 → DEL-09-09, N-B11, admitted): GUIDE M1.6, M9.8 and §2.11 cite XT §2–§5; XT's Receivers line (l.18) does not list DEL-03-04. No DEL-09-09 → DEL-09-06 or → DEL-03-04 row may be added (guards E-1, E-2).

Indirect: XC-10's Phase-1 recording parts (XF-42; "continued past ‹checkpoint› before ‹act›") rest on DEL-03-03's observations on X, the contribution arc N-24 carries to DEL-02-03.

## C.7 Carried review items

| Item | Status | Evidence |
|---|---|---|
| V6 (m-1, m-3…m-7) | None names XT. V6 checked XT F-10 (m-5 echo): holds | V6 §1 |
| Closeout D9-9-1 ("TBD-007" unqualified) | **Fixed** | l.35 "(DEL-03-03 TBD-007)"; UNRESOLVED l.580 |
| Closeout D9-9-2 (F-15, F-16 can close) | **Fixed** | §9.5 l.481–482 |
| V9, V10 | No XT residual | — |
| BASIS-ALIGN / SCA002 reviews | None names XT beyond the 17 re-pins | grep |

## C.8 Recommended work in this pass

1. **Re-pin the header** (15 pins; row range …024); bump to XT-v0.5. [C.1]
2. **SoW alignment:** add the three REQ-009 owners to §7; remove "not registered" from IN-22 and IN-29 and cite DEP-09-09-021…023; close F-1, F-2 and F-6; correct the VC-T-01 range; cite TBD-005 and AX-005. [C.2, C.4]
3. **Reword S-10** on V4-HI-42 once the EXEC reading of "requested" is settled. [C.3]
4. **Re-verify body citations** against the current siblings and close F-17. [C.1]
5. **Add the suite run order, the set-up and reset per case, and a reopen table** (candidate change → cases). [C.5]
6. **Give F-18 an UNRESOLVED row** with owner and point of need. [C.4]
7. **Tie §5.1's account to C §8's cells** so that DEP-03-01-030's contribution is stated element for element; add DEL-03-04 to the Receivers line. [C.5, C.6]

**Not in this pass:** choosing the realization family (DEL-03-03 TBD-007), the OI-003 disposition or the traced operation; running any XC, TR or rehearsal; adding register rows toward DEL-09-06 or DEL-03-04.

---

# D. DEL-03-04 — `HOST_INTEGRATION_GUIDE.md` (GUIDE-v0.3; last changed at `caa4334ca`, 2026-09-28 19:13)

## D.1 Pins

**The input table (l.16–35): all 18 recomputed from the working tree; 18/18 match.**

| Short | File | Pinned = recomputed sha256 |
|---|---|---|
| C | `CATALOG_AND_READ_BASIS.md` | `8282c003024e54708f3b9842e04b6b0dc8c4e1c496027afae582eb6387675ce4` |
| P | `PROPOSAL_LIFECYCLE_AND_OUTCOMES.md` | `410fb289e16177e11190db45be37e02b5d82ebf7a9fcff8676e938bb23a51af9` |
| ADAPTER | `ADAPTER_ENABLEMENT_AND_RECEIVING.md` | `6e13ab117271b12512f64aab82e99839d1884abb4a43481f7382b67faf253043` |
| ACT | `ACT_AND_POLICY_CONTRACT.md` | `6889003e6c1c2dd6d58b7145dd7955651debcc7b705a84e63aa6cd4e596e4815` |
| AS | `AUTONOMY_AND_STANDING_EXCHANGE.md` | `52d1341bb475f0a7de4b986b905e2986aa0e0a4e04e8b1783a6a83174eb6a33d` |
| RS | `RECORD_SEMANTICS.md` | `96b1aeeb120be597c4f35eea13f6a60ce20783e555c918521aacee38c5bcf666` |
| WD | `WORKFLOW_DECLARATION.md` | `43a9962f025de384e1cdaedea9a648da74e20216476a04f2394cfa3851f47eb9` |
| WD-EX | `EXAMPLES.md` | `8d60ed7850e6935b8410217c8867c59554c7de9aec28c60514e88ff5f0cff36e` |
| EXEC | `EXECUTION_COMPATIBILITY.md` | `092f248682447df74e93915527930f4b90367fac46b867dad18daef3c5c608ff` |
| LOOP | `LOOP_RECEIVING_CONTRACT.md` | `246f4636166c67250f73862de586afef3cad91ba538272880a80c2fd657a5767` |
| PANEL | `PANEL_RECEIVING_CONTRACT.md` | `dd71e11dbe0d9872727524aef69ef80ba118980533148c2aa7453d1176165658` |
| HOSTING | `HOSTING_BOUNDARY.md` | `d11d4c574aa3c342bfac9c1d1e9bf3746aa885baafd17eaa296a79a523e3d0b9` |
| SPIKE | `PIN_SPIKE_0.158.0.md` | `0e090a4ca14e3ec323e8302ea4bc4e1fefc66bee50d0d3247e1cd0ddc04eb115` |
| CA | `CONNECTED_ACTIVITY_CONTRACT.md` | `1a7e2ac993e327bfd56c571c1016122baa846efa6ad378630bd3523ecbc4d421` |
| RELAY | `RELAY_QUESTIONS_SWBPIPE.md` | `c93f8cc52da81b5f16040dbaade7acd38fa676c2a81c86a32a7e12862c31056f` |
| XT | `EXTERNAL_TRACE_CASES.md` | `fde79bb3170c450830cf0ca53bba8493328f2f89d47f14fed563f97dad3b2d92` |
| ANS | `RELAY_ANSWERS_SWBPIPE.md` | `afb6e063e7e5dfccf8986206f888cf1e2e1c4e7fc3430fdf86db670714fc0e74` |
| FACTS | `FACTS_SQ01_SQ32.md` | `733fb88a701317be8f0054937eca058774ba5f5f30c7a27233718996e8b2ab7e` |

GUIDE itself is currently `c36e2eefd082afd5c7530c3d58e06520119014b6befb37fc0014f3cddad72e64`. Every one of the 16 Design inputs will change in this pass, so the table must be recomputed last, as before.

**The other header pins:**

| # | Line | Pin | Status | Current value |
|---|---|---|---|---|
| 1 | 9 | "Branch base 6e18505e3 (accepted basis)" | **stale** as a statement of the basis docs | basis docs at HEAD |
| 2 | 10 | ScopeOfWork.md `203c0928…a436` "(… TBD-001…TBD-009)" and "All three unchanged since v0.1 (not re-hashed at this pass)" | **stale**, and the "unchanged" claim is now false | `895f004e4d0f133798f461d8157ac63fff880da09f471be9bae885fe0cfb7c28` (adds AX-004; revises four map rows, CLM-003, REQ-002, REQ-004, REQ-005, TBD-001, TBD-002) |
| 3 | 10 | Dependencies.csv `b41eacd0…ac17` "(DEP-03-04-001…020)" | **stale** | `977d8712e02b4e22eb1191da82013fc974aedf76fc482e63302c5f6512bee32b`; rows 001…**023** |
| 4 | 10 | `_REFERENCES.md` (no hash) | current | `1279ea22…` at both `6e18505e3` and HEAD |
| 5 | 11 | `docs/HOST_INTEGRATION.md` `08c8fc7d…` "§1–§9, §10, §11" | **stale** | `d4331c39…`. §10 and §11 are textually unchanged; V4-HI-42, V4-HI-70, the §8.1 Domains sentence and the header changed |
| 6 | 12 | first-run OWNER_DECISIONS `a9869129…`; R1, R2, R3 (truncated); R4; R5; R6; R7; V3-B; V4-A; V4-B; V5 | current (each matches) | — |
| 7 | 13 | intake OWNER_DECISIONS `a5ccab0d…` (state at `7a1508452`) and `5fd780bf…` (with DECISION-5) | `5fd780bf…` current; the first is an earlier state, labelled as such | — |
| 8 | 13 | R8_RESOLUTIONS `d4c34233…` (R8-12 state) and `44bc9a8d…` (adds R8-13) | `44bc9a8d…` current | — |
| 9 | 13 | INTAKE_MAP `3cc18295…` | current | — |
| 10 | 13 | intake BRIEFS `3e33ba26…` | **stale** | `6f32809d…` |

**Quoted texts:**

| GUIDE text | Status |
|---|---|
| B-11 (l.198): the revised V4-HOST-02, quoted in full | **The quote is current**: it equals `docs/PRD.md` V4-HOST-02 word for word, less the PRD's source tag "(D-18; DEC-5)". The label beside it, "flagged for the next accepted-basis update", is stale |
| l.5, G-6 (l.685), F-16 (l.764), UNRESOLVED l.791: V4-HOST-01's "by default … API key" wording | **stale quote**: the PRD now reads "There is no default between them; they are options the person chooses among" |
| G-12 (l.690): V4-WF-05's first half ("holds … the run waits") | **stale quote**: the PRD now reads "Holding the checkpoint — the run waits until the act is performed — is **phased to the governance layer**, not withdrawn" |
| CC-2 (l.615), CC-11 (l.624), §4.2 row 6 (l.635), G-12: SoW row 6 "checkpoints still wait" | **stale quote**: the SoW row reads "declared checkpoints are plan guidance in the current phase — their acts are recorded only when performed and no hold is claimed — and hold only for a workflow that takes up the governance phase" |
| CC-2, §4.2 row 7 (l.636), G-6: SoW row 7 "local-server default and local-data constraint" | **stale quote**: the SoW row reads "a local or cloud model the person chooses with no default (PRD V4-HOST-01) and data sent only to the selected model service and person-allowed destinations, each recorded and shown (PRD V4-HOST-02 …); App conversations reading host content follow … DECISION-2 D5" |
| §4.2 row 4 (l.633), G-7 (l.686): SoW "duplicate-one-effect" | **stale quote**: the SoW reads "at-most-one-effect per item as a host obligation to be evidenced" (row "Origin…" and REQ-002) |
| §2.13 TBD-001, TBD-002 (l.385–386): "Owner (literal, SoW)" = "Owner with App/SWB contract owners"; "Point of need (literal, SoW)" = "Before operation-policy production contracts" / "Before permission-policy implementation" | **stale as SoW literals**: the revised TBD-001/TBD-002 carry neither phrase. `_Decomposition/Open_Issues.csv` still carries both for OI-001 and OI-002 |

G-7's other phrase, "canonical content hash", is still in the SoW row "Basis", now with "(as a canonical content identity with its method designation)".

**Stale count:** 5 hash or commit pins (rows 1, 2, 3, 5, 10) and 6 quoted texts = **11**. The 18-row table: 0 stale.

## D.2 ScopeOfWork alignment (SoW `895f004e…`)

| SoW item | Where GUIDE answers | Depth |
|---|---|---|
| Minimum receiving map, 10 rows | §2.1–§2.10 (M1.1…M10.3) | developed for rows 1–7 and 9; row 8 partly (role supply and registration are outside the 14); row 10 only named (by design) |
| Rows revised by SCA-V4-001: Basis; Origin, undo and proposal presentation; Autonomy; Loop and panel | M3.1, M3.2; M4.5; M6.4; M7.3, M7.9 | the matrix lines already carry the revised meanings; the completeness section describes the old wording (D.1) |
| CLM-001…CLM-006 | §1 B-1…B-3; §2.12 | developed |
| CLM-003 (revised: the guide also consumes DEL-01-01, DEL-09-06 and DEL-09-09) | header table; §2.11 | developed; F-4 still reports the absence |
| OUT-001 checklist | §3 HC-0…HC-10 | developed |
| OUT-002 matrix | §2 | developed with the limits above |
| OUT-003 completeness checks and recorded comparison | §4 CC-1…CC-11 | recorded, self-run, against the pre-revision SoW |
| REQ-001 | CC-1, CC-3 | developed |
| REQ-002 (revised: at-most-one-effect) | rows 1–4 | developed |
| REQ-003 | row 5 | developed |
| REQ-004 (revised: D2/D3 adopted; remaining decisions at TBD-001, -002, -006) | B-4, B-5; §2.13 | developed; §2.13 lags (D.1) |
| REQ-005 (revised: host agent sends data only to the selected model service and allowed destinations) | M7.3, M7.9; HC-7.7…HC-7.9 | developed |
| REQ-006 | row 10; HC-10 | only named (DEL-07/08 outside the 14) |
| REQ-007 | §0 standings; §2.13; §4.3 | developed |
| REQ-008 | §2.12 X-01…X-19 | developed |
| AC-001…AC-008 / VER-001…VER-008 | VC-G-01…VC-G-08 | designed, not run. VER-007's checker: see D.7 |
| TBD-001, TBD-002 (revised) | §2.13 | lag |
| TBD-003…TBD-009 | §2.13 | literals match |
| AX-004 | — | absent |

**Where GUIDE contradicts or lags the revised SoW:** l.10 (hashes, "unchanged since v0.1", row range); l.385–386 ("SoW text still reads open (F-5)" and the literals); CC-2 (l.615); CC-6 (l.619: "TBD-001/002 SoW text still reads open"); CC-11 (l.624: "3 remain … G-6, G-7, G-12" — all three are SoW or basis wording that has since been revised); §4.2 rows 4, 6, 7 (l.633–636); G-6, G-7, G-12 (l.685–690); F-4 (l.752: "No rows to DEL-01-01, DEL-09-06 … or DEL-09-09" — rows DEP-03-04-021…023 exist); F-5, F-6 (l.753–754); F-16 (l.764); UNRESOLVED l.786, l.788, l.791, l.796; VC-G-06 (l.813) still says "RELAY *prepared*" as a claimed state to inspect.

## D.3 Amended basis

| Requirement | GUIDE text | Agreement |
|---|---|---|
| V4-WF-05 | l.4; §0 (l.136–148); G-12; F-16; UNRESOLVED l.786 | Meaning agrees. "Flagged for the next accepted-basis update" is stale in five places. "Requested" is not stated (as CA) |
| V4-HI-42 | §0 l.146–148; B-4; M6.4; HC-6.3 | Same wording lag as CA: the whole requirement is called guidance in Phase 1 |
| V4-HOST-01 | l.5; B-6; M7.3; HC-7.3 | Meaning agrees (no default; OAuth sign-in or API key). Stale "flagged" labels |
| V4-HOST-02 | B-11 (quote current); M7.9; HC-7.7…HC-7.9 | **Agrees, word for word.** Stale "flagged" labels (l.5, l.198, l.214, l.295, l.623, l.685, l.788) |
| V4-ARC-11 | M7.3; UNRESOLVED l.791 | Agrees ("no default"); the UNRESOLVED row is stale |
| V4-ARC-12 (amended: the native layer allows only the selected model service and allowed destinations, records every destination, holds any key or sign-in credential) | M7.3 "no credential (key or sign-in credential) visible to the script; native layer enforces"; M7.9 | Agrees; M7.3 does not cite V4-ARC-12 by ID |
| V4-HI-70 (amended: each network destination contacted, for a host's agent) | M5.6 (l.274) "Compact run record R1–R14"; HC-5.5 (l.543) "RS §4 (R1–R14); V4-HI-70/71" | **Lags.** RS has R15 (network destinations) since R8-13. GUIDE cites R15 under M7.9 only; row 5, the row that restates V4-HI-70, does not include it |
| V4-EXM-22 | not cited | — |
| V4-EXM-23 (amended) | HC-7.3, HC-7.9 cite it as DEL-09-07's observation | Agrees with the amended scenario |
| "local-first" | not used; §4.2 row 7 says "local default (SoW wording; revised …)" | the SoW wording it describes is gone |

## D.4 Open items (26)

| # | Item (UNRESOLVED row or gap) | What is open | Owner / point of need | Class |
|---|---|---|---|---|
| 1 | `UNRESOLVED{OI-021}` | First operation, check, autonomy, environment, surface; reserved additions | Owner via outside SWB session | **OWNER** |
| 2 | `UNRESOLVED{OI-003}` | Extension promise | Owner with host contract owner | **OWNER** |
| 3 | `UNRESOLVED{OI-013}` | Loop placement and persistence | Shared contract owner with SWB implementation owner | **OWNER** |
| 4 | `UNRESOLVED{OI-014}` | Shared component placement | App/shared contract owners | **OWNER** |
| 5 | 03-04/TBD-007 (OI-022) | PEC receiving envelope | App consumer owner and PEC owner | **LATER** (outside the 14) |
| 6 | 03-04/TBD-008 (OI-023) | Domains receiving | Owner with Domains/SWB/App receiving owners | **LATER** |
| 7 | 03-04/TBD-009 (OI-026) | Domains provider | Owner | **LATER** |
| 8 | `UNRESOLVED{D6}` (U-E1) | Host-operation checkpoints in App runs | Owner; governance phase | **LATER** |
| 9 | D6 follow-up (U-E23); G-8 | App-side held actions | Owner; governance phase | **LATER** |
| 10 | SWBPIPE owner decisions (ANS §2) | — | SWBPIPE owner | **HOST** |
| 11 | V4-HI-32 not met by SWBPIPE | — | SWBPIPE | **HOST** |
| 12 | R8-Q4b | Launch variable as A13 evidence | Owner, deferred | **OWNER** |
| 13 | l.786 | "V4-WF-05 first half phased …; SoW row 6 wording … next accepted-basis update" | Owner | **NOW** — PRD V4-WF-05 and SoW row "Autonomy" as revised |
| 14 | l.787 | Governance phase taken up | Owner, per workflow | **LATER** |
| 15 | l.788 | "Revised V4-HOST-02 … at the next accepted-basis update" | Owner | **NOW** — PRD V4-HOST-02 |
| 16 | l.790; M7.9; HC-7.7…7.9 | DECISION-5 host obligations not asked of SWBPIPE | App manager via the human; when UI-SUCCESSOR resumes | **HOST** |
| 17 | l.791 | "V4-HOST-01 / V4-ARC-11 wording … next accepted-basis update" | Owner | **NOW** — PRD V4-HOST-01; ARCHITECTURE V4-ARC-11 |
| 18 | l.792 | SWBPIPE embedded direction predates D-20 | SWBPIPE | **HOST** |
| 19 | 03-03/TBD-007 | MCP versus CLI (OC-1…OC-12) | App external-host integration owner with external host owner | **HOST** |
| 20 | l.794 | ACT U-02 consequence vocabulary; ACT U-03; EXEC U-E4 | DEL-04-01 with host policy owner; DEL-04-01 with the owner; the owner | **OWNER** |
| 21 | l.795 | DEP-05-01-024 (model interface supplier UNKNOWN); LOOP N-OPEN-1…5, T-OPEN-1, R-OPEN-1 | App/shared embedded-integration owner with SWBPIPE owner; the owner for N-OPEN-4 and R-OPEN-1 | **HOST** (with two owner parts) |
| 22 | l.796 | "Register and SoW-text findings F-4, F-5, F-6, F-12, F-16" | Register owner / closeout C1 | **NOW** — F-4: register rows 021–023; F-5, F-6: SoW `895f004e…`; F-16: amended PRD. F-12 (two "TBD-007") stays, handled by the prefix rule |
| 23 | l.797; F-9; CC-7; CC-10 | "VER-007 checker run; independent review of v0.3" | App manager | **NOW** — checker: `RV/RV-3_DEL-03-04.md` records `check_boundary_owner_resolution.py` status OK on the revised SoW, and my rerun today agrees; review: `reviews/V9.md` (with V9b) covered the intake candidate that contained GUIDE-v0.3, and `reviews/V10.md` (with V10b) the R8-13 candidate. Neither review claims a line-by-line read of the matrix |
| 24 | CC-11; G-6, G-7, G-12 | "3 remain" SoW/basis wording conflicts | Owner, next basis update; C1 | **NOW** — all three revised |
| 25 | G-1 | No Design file for DEL-02-04 (role supply) or DEL-01-04 (App act control); M8.6 and M5.3 rest on SoW meaning | none in this undertaking | **LATER** (S1-F's subject) |
| 26 | G-2 | PEC and Domains receiving not started | by design | **LATER** |

**Counts:** NOW 6 · OWNER 6 · HOST 6 · SPIKE 0 · LATER 8.

## D.5 Depth against the 60% description

DEL-03-04 exchanges one kind of contribution: it consumes definitions from thirteen first-increment deliverables and gives an application builder an index, a checklist and a completeness result.

| Aspect | What GUIDE has | What is missing |
|---|---|---|
| Interfaces | 67 matrix lines, each with definer (file, version, section), host contribution (SQ), open choices and standing; §2.11 supporting contributions; §2.12 excluded acts; §2.15 SWBPIPE receiving mappings | Nothing for the four new arcs' contributions by name (item-level dispositions and identities from DEL-03-02; checkpoint observations on X from DEL-03-03; the App act control). M8.4 and M5.3 cover the ground without naming them |
| States | Standing vocabulary (§0); hold-support values (governance phase); checklist marks (answered with evidence · without evidence · not answered · not applicable) | — |
| Data | None of its own, by design | — |
| Operating sequences | §3 "How to use it" | No order in which a host takes the ten items, and no statement of which items a Phase-1 host can claim without the others (for instance rows 1–4 before row 9) |
| Failure behaviour | "An answer … is not evidence before a claim"; conditional rows 9 and 10 | No statement of what a host or reviewer does with a check marked *answered without evidence*, or how a later candidate change reopens checks |
| Verification | CC-1…CC-11 with a recorded result; the pin check by script (§4.5); VC-G-01…VC-G-08 | The recorded result is bound to the pre-revision SoW and basis (D.2), so it is no longer true of the current candidate. It was produced by the author; F-9's review gap is smaller than the file says (D.4 item 23) |

**Structural choices still open:** the 10-row shape is fixed by the SoW and has absorbed DECISION-5 as M7.9 without change. OI-013 and OI-014 (rows 2, 5, 7) and 03-03/TBD-007 (row 9) could change which file defines a line, not the matrix shape. Rows 8 and 10 cannot be completed until deliverables outside the 14 are defined.

## D.6 Joins (all in DAG-003's admitted layer)

For each row I checked that the sections GUIDE cites exist in the pinned, current supplier file. They do (568 citations, script). "Receiver statement" says whether the supplier's Design file names DEL-03-04 outside its header.

| Row | Arc | Contribution | GUIDE uses it at | Supplier names DEL-03-04? | Notes |
|---|---|---|---|---|---|
| DEP-03-04-005 | → DEL-03-01 | Catalog/read-basis definition | Row 1; row 3; §2.11 | No (header only) | — |
| DEP-03-04-006 | → DEL-03-02 (mirror DEP-03-02-021) | Proposal/validation/outcome definition | Rows 2, 3, 4 | Yes: P §13 (l.710) "§1 authority map and this table" | P offers less than GUIDE uses (GUIDE cites P §1–§12); not a conflict |
| DEP-03-04-007 | → DEL-03-03 | External-agent receiving definition | Row 9 | Yes: ADAPTER §11 (l.1061) "§§1–9 for the guide's 'Optional external catalog access' row" | GUIDE also cites ADAPTER §10 and §12 |
| DEP-03-04-008 | → DEL-02-01 | Workflow / four-role / allocation semantics | Row 8; M1.7 | No (header and change rows) | — |
| DEP-03-04-009 | → DEL-02-03 | Compatibility, checkpoint and transfer semantics | Row 8; §2.14 | No (change rows) | GUIDE §2.14 defers to EXEC §3.6 "which governs where another file differs" |
| DEP-03-04-011 | → DEL-04-01 (mirror DEP-04-01-024) | Adopted policy and act distinctions | Rows 5, 6 | Yes: ACT §10.3 (l.1404) | — |
| DEP-03-04-012 | → DEL-04-02 | Autonomy/standing receiving | Rows 4, 6 | Yes: AS receivers line (l.12) "Host builder via DEL-03-04" | — |
| DEP-03-04-013 | → DEL-04-03 | Act and run-record definitions | Row 5 | No (header only) | **M5.6 and HC-5.5 say R1–R14; RS now has R15** |
| DEP-03-04-014 | → DEL-05-01 | Loop/model receiving requirements | Rows 2, 7 | No (header only) | — |
| DEP-03-04-015 | → DEL-05-02 | Panel receiving requirements | Row 7 | No (header only) | — |
| DEP-03-04-021 | → DEL-01-01 (N-B9) | Supplier boundary (native surfaces for optional external access) | §2.11; M9.3; rows 5, 6, 8 | No (header only) | The row's statement limits the contribution to external access; GUIDE also uses HOSTING §6.7, §8.2, §8.3 and §11 for rows 5, 6 and 8 |
| DEP-03-04-022 | → DEL-09-06 (N-B10) | Relay questions and recorded answers | Host column of every row; §4.3; CA in §2.11, M1.8, M8.5, M10.3 | CA §11.2 has no DEL-03-04 row | The row names RELAY and ANS; GUIDE also consumes CA (step map, staging, ladder) |
| DEP-03-04-023 | → DEL-09-09 (N-B11) | External trace cases | M1.6; M9.8; §2.11 | XT Receivers line does not list DEL-03-04 | — |

DEP-03-04-010 (DEL-02-04) and -016…-019 (DEL-07/08) are outside the 14. DEL-03-04 has no consumer in any register. F-4 (l.752) should be withdrawn: the three rows it asks for exist.

## D.7 Carried review items

| Item | Status | Evidence |
|---|---|---|
| V6 m-1 (comparison sentences list PANEL as unchanged) | Header sentence **replaced** at v0.3 (l.39 now compares against the v0.2 pins). The change row at l.94 **still** reads "Unchanged against `2f42fba02`: SPIKE, HOSTING, P, LOOP, PANEL"; l.95 records the PANEL re-pin | l.39, l.94–95 |
| V6 m-6 (M8.1 "conservative default HS-5; R6-1" unscoped) | **Open** | l.307 unchanged |
| V6 m-7 (the "exhaustive partition" sentence has a theoretical hole after R7-3; owners WD and EXEC) | **Open** | l.411–413 unchanged |
| V9 S-1 (wrong provenance of the ANS revision in the change row) | **Fixed** | l.65: "merged to main in #1048 `56dd72334`" |
| V9 N-7 (no change row for the V9 re-pin of C, ADAPTER, RS, LOOP, RELAY) | **Open** | "Changes from v0.2" has no V9 row; the later R8-13 re-pin note (l.37) covers a different set |
| V10 S-1 (person-only grant "confirmed by the owner") | **Fixed** | l.68; B-11 (l.198); l.301; l.789: "not objected to and stands" |
| V10 N-1 (consumed-input line placed both hashes at `1528a5033`) | **Fixed** | l.13; l.67 |
| C1-B §4.5: independent review; VER-007 checker | Text still says open (F-9, l.757; l.40; CC-7; l.797). Evidence now exists (D.4 item 23) | — |
| C1-B §4.2: consumption of DEL-01-01, DEL-09-06, DEL-09-09 "not in the SoW receiving map" | **Closed by the SoW and register**, not yet in GUIDE's text | SoW CLM-003 last sentence; rows 021–023; F-4 |
| BASIS-ALIGN / SCA002 reviews | None names GUIDE beyond the 17 re-pins. G-6 and G-12 were the stated grounds of SoW edits E-0304-04 and E-0304-05 | RV-3 return |
| V9 N-3 (INTAKE_MAP Part 2 lacks a pointer to R8-1/R8-2) | **Open** (a run record, not a Design file) | INTAKE_MAP bytes unchanged (`3cc18295…`) |

## D.8 Recommended work in this pass (last in the route, as before)

1. **Re-pin last:** the 18-row table after every other file is final, the SoW `895f004e…`, the register `977d8712…` (rows …023), `docs/HOST_INTEGRATION.md`, the base commit; repeat the script check and record it. [D.1]
2. **Rerun CC-1…CC-11 against the revised SoW and amended basis and rewrite what they describe:** CC-2, CC-6, CC-11; §4.2 rows 4, 6, 7; close G-6, G-7, G-12; §2.13 TBD-001/TBD-002; withdraw F-4, close F-5, F-6, F-16; close UNRESOLVED l.786, l.788, l.791 and most of l.796; remove the "flagged for the next accepted-basis update" labels (l.4, l.5, B-11 and the others listed in D.3); fix VC-G-06. [D.2, D.3, D.4]
3. **Add RS R15 to M5.6 and HC-5.5** (amended V4-HI-70). [D.3, D.6]
4. **Record what exists:** the RV-3 checker result and the V9/V10 reviews in F-9, CC-7, CC-10 and l.40, stating their scope; add the V9 re-pin change row (N-7); scope M8.1's default (m-6); follow WD/EXEC on the partition sentence (m-7). [D.4, D.7]
5. **Refresh the matrix for this pass's changes in the other 16 files**, and name the N-18, N-21, N-24 and X-1 contributions where M4.2, M5.3, M8.4 and M9.5 already stand. [0, D.5]
6. **Add a short "order of use" to §3** and what a reviewer does with *answered without evidence*. [D.5]

**Not in this pass:** asking SWBPIPE the DECISION-5 items (no relay); defining rows 8 and 10 content that belongs to deliverables outside the 14; choosing placement (OI-013/OI-014) or the seam (03-03/TBD-007); an independent full-matrix review by the author.

---

# E. `HANDOFF_SWBPIPE_DOMAINS.md` and the intake map

## E.1 HANDOFF (current sha256 `76edf236…`)

The file states that RELAY-v0.3 was relayed and answered, that nothing is adopted or committed, that host joins are deferred (DECISION-3), and it carries the R8-8 note for SWBPIPE with the DECISION-4 sentence on checkpoints. Against current records I observe:

| Line | Text | Observation |
|---|---|---|
| 22 | "The recorded v4 direction remains stock Codex for App, Tauri and a minimal host loop with local-first host operation." | "local-first" was removed from the accepted basis by SCA-V4-001 (PRD: "on a model the person chooses … with no default"). This is the one surviving use I found in the files I read |
| 7 | "…does not choose provider/tool deployment or relax the local/privacy contract" | The contract it refers to (V4-HOST-02) was revised by DECISION-5 |
| 40 | "DAG-001 is accepted and the 30% gate is complete" | `_DAG/_LATEST.md` reads DAG-003 |
| — | No mention of DECISION-4 D4-3 (model access) or DECISION-5 (network destinations) | The note for SWBPIPE covers D4-1 and D4-2 only |

HANDOFF is in no S1 row and is not on this run's not-written list. It is a relayed coordination file that has been edited after the relay (the R8-8 note). Whether it is updated in this pass is for the integrator.

## E.2 Intake-map consequences: applied, unapplied, deferred

**Applied.** I read every Part 1 row that names CA (29 rows), XT (23), GUIDE (33) or RELAY (10; two of them only mention it) against the current text of the four files and found each proposed edit present in the form R8 ruled. Greps find no remaining "relay pending" standing cell in GUIDE, no "Not received" cell in XT §2, and no "prepared" standing in CA §9. Part 2 rows P2.1, P2.4, P2.10, P2.11, P2.13 and P2.16–P2.18 appear in the four files as governance-phase values, as R8-2 ruled.

**Still unapplied or deferred:**

| # | Consequence (source) | State | Where it sits |
|---|---|---|---|
| 1 | R8-Q4b: is a person-set launch environment variable A13 evidence? (Part 3 item 4 (b); Part 5) | Deferred to the owner, "when UI-SUCCESSOR resumes" | CA, RELAY, XT, GUIDE UNRESOLVED rows |
| 2 | R8-Q-D6 options (B) App interposition and (C) asking SWBPIPE to plan a host-held route (Part 5) | Overtaken by DECISION-4: D6 closed for Phase 1. (C) was never asked; no relay question exists for it | CA DI-6; GUIDE §2.13 |
| 3 | Part 4.6: no checkpointed workflow can be examined as enforced against SWBPIPE on either surface | Recorded (CA F-18); the decision is deferred to the governance phase | CA F-18 |
| 4 | R8-Q16 / Part 4.10: grant display for a host with no grant model | PROPOSED and deferred with the host joins | AS §3 and U-20; CA DI-2; XT IN-29; GUIDE SW-5 |
| 5 | Part 3 items 2 and 3, Part 4.7, 4.8: "owner notice" that SWBPIPE does not meet V4-HI-32, R2-13 per-item staleness or the catalog requirement, and that OUT-003 has no host side | Recorded as UNRESOLVED rows and findings (CA F-19, F-1; XT F-19, F-22; GUIDE l.784). I found no separate notice in the intake OWNER_DECISIONS or RECEIPT | the Design files only |
| 6 | Part 3 item 8 / R8-Q8 (V4-HOST-02 versus DEC-051) | Decided after I2 by DECISION-5. Its host obligations are **not asked**: no SQ; RELAY SQ-16 and SQ-30 keep the old wording | GUIDE M7.9, l.790; intake RECEIPT "Open elsewhere" |
| 7 | R8-5 / Part 4.9: per-batch Apply against XT's completion rule | Deferred "for the integrator when host joins resume" | XT F-18 (no UNRESOLVED row) |
| 8 | X.4: consumed-input lines cite the ANS bytes | Applied with the delivered hash `6f01add3…`; the later revision `afb6e063…` reached only RELAY and GUIDE | CA l.9, l.26; XT l.9, l.17 |
| 9 | V9 N-3: Part 2 states phase-agnostic values ("every checkpointed workflow run from the App on X is *unsupported*") with no pointer to R8-1/R8-2 | Open; INTAKE_MAP is unchanged | the run record |
| 10 | Part 4.3 (iii): T3 solver receipts as a possible content identity for a named output, "a note for C §6.2, not a ruling now" | I find no such note in C (grep). It is S1-B's file | — |
| 11 | STD-2: every live W14, XC, TR case keeps AWAITING INPUT | Deferred by design (DECISION-3) | CA §8.2; XT §3.2, §4.4 |

---

# F. Closing table

| File | NOW | OWNER | HOST | SPIKE | LATER | Open items | Stale pins (hash or commit + quoted text) |
|---|---:|---:|---:|---:|---:|---:|---:|
| CA | 6 | 7 | 7 | 0 | 7 | 27 | 16 (15 + 1) |
| RELAY | 2 | 3 | 3 | 0 | 2 | 10 | 9 (8 + 1 frozen group) |
| XT | 4 | 4 | 9 | 0 | 5 | 22 | 15 (15 + 0) |
| GUIDE | 6 | 6 | 6 | 0 | 8 | 26 | 11 (5 + 6); input table 0 of 18 |
| **Total** | **18** | **20** | **25** | **0** | **22** | **85** | **51 (43 + 8)** |

Counts are per file; the same matter recurs across files. The distinct owner-level matters behind the 20 OWNER entries are nine: OI-021 (with its reserved additions), App v4 OI-003, OI-005, OI-013, OI-014, R8-Q4b, EXEC U-E4, ACT U-03 and ACT U-02. Two more owner questions, LOOP N-OPEN-4 and R-OPEN-1, sit inside a GUIDE row classed HOST (D.4 item 21). Case states are not counted: 11 W14, 13 XC and 10 TR cases are AWAITING INPUT on host inputs. No item in these four files calls for a spike.

**The three most consequential gaps**

1. **The first connected activity is designed on a fixture whose shape SWBPIPE's answers do not match, and OI-021 is still unselected.** CA §2.3–§2.4, W14-04/05/06 and XT XC-02, XC-08, XC-10 and §3.3 assume per-item accept and reject, grants and per-subject identities. ANS describes one wired journey with per-batch Apply, no reject record, no grants, a whole-model identity, no enablement act and a different named caller. The files record each mismatch as "no counterpart" and stop there. Nothing maps the activity onto what exists or says what the increment can examine meanwhile. The owner's selection could restructure CA, XT and the GUIDE rows that index them.
2. **The re-pin is not only hashes: the amended texts change what these files must say.** Fifteen or more pins per file are stale in CA and XT; GUIDE's recorded completeness result (CC-2, CC-6, CC-11, §4.2, §2.13) describes SoW wording that no longer exists. The amended V4-WF-05, V4-HI-42 and V4-EXM-22 say the checkpoint's act "is requested"; no file in my row says who requests it in Phase 1 or how a witness sees it. The amended V4-HI-70 puts network destinations in the host run record; CA/E and GUIDE row 5 do not carry it. XT §7 lacks three owners REQ-009 now names.
3. **The joins are stated from one side.** Eight of DEL-09-06's eleven in-set suppliers and four of DEL-09-09's eight do not name the consumer in their interface sections, in most cases because the arcs (N-19, N-C2…N-C6, N-28, N-08, N-09, N-26) were registered after the Design files were written; PANEL (for DEL-09-06) and RS (for DEL-09-09) lack the statement although their arcs date from DAG-001. RS §10 offers DEL-09-06 "R2 transfer links" where the SoW and CA use act records. CA has no failure behaviour per exchange and no W14 result record. CA and XT still cite siblings at the `8fb51f07f` versions. The receiver comparisons this run's work graph asks for cannot be made from the present text.

**Owner-level choices found**

- **Carried, unchanged:** OI-021; App v4 OI-003; OI-005; OI-013/OI-014; U-E4; U-03; R8-Q4b (deferred); taking up the governance phase.
- **New or sharpened by this survey (advice; nothing here is settled):**
  1. Whether this pass should prepare an OI-021 option sheet that sets the first activity against SWBPIPE's actual candidate journey (A.8 item 9). It needs no host join, but it changes what "develop toward 60%" means for CA and XT.
  2. How to read "the required human act is requested" in the amended V4-WF-05 / V4-HI-42 for the current phase. This may be an integrator reading under R8-1 rather than an owner decision; it starts in EXEC (S1-C) and lands in CA, XT and GUIDE.
  3. Whether HANDOFF (E.1) and a list of next-relay items (B.8 item 3) are updated now, given that the relay itself is not part of this run.
