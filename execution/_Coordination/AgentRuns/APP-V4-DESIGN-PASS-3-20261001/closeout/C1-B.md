# C1-B — bounded closeout: DEL-01-05, DEL-02-02, DEL-02-04

- Run `APP-V4-DESIGN-PASS-3-20261001`, node C1-B. Executor: Type 2 TASK
  (Claude Opus 5.5, high effort), dispatched by HELP_HUMAN; no delegation.
- Method: `chirality-root:bundled:workflow:bounded-reconciliation`
  (Root `workflows/bounded-reconciliation/WORKFLOW.md`, read whole, sha256
  prefix `c7798c0ae59860f1`). Brief: `BRIEFS.md` "Common rules" and
  "Closeout (after PR #1072)" → "C1" (sha256 prefix `a0befb8c4871e43d`).
- **Write fence kept.** This file only. No ScopeOfWork, `Dependencies.csv`,
  `_DEPENDENCIES.md`, `_STATUS.md`, `_CONTEXT.md`, `_REFERENCES.md`,
  `MEMORY.md`, Design file, decomposition or DAG file was written. DAG-003's
  `SOURCE_MANIFEST.sha256` binds every ScopeOfWork and register, so every
  warranted change below is a **proposal** (file, location, old → new,
  reason, source), none applied. Read-only git; no network; no Codex or model
  run.
- **Candidate compared.** Branch `claude/chirality-app-v4-60-percent-a41fd5`
  at HEAD `b10a04b5bb`, plus the C0 executor's in-progress working-tree edits
  seen on 2026-10-02 (ACCESS §20 attribution, V21b-A N-1; WR §4.2 TT-3, R21-5;
  each with a "C0" change row). Read with `git diff`: both are wording or
  carrier-description changes; neither changes a commitment, interface or
  standing. Comparisons below hold for both byte states.

| File | sha256 (HEAD) | sha256 (working tree, with C0) |
|---|---|---|
| DEL-01-05 `Design/ACCOUNT_AND_PROVIDER_ACCESS.md` (ACCESS-v0.2) | `929bd07b32f40fc6…` | `f4b34741c889d9da…` |
| DEL-01-05 `Design/ACCOUNT_HOME_DECISION_RECORD.md` (v0.2) | `f77f87927558ca73…` | same |
| DEL-02-02 `Design/WORKSPACE_AND_REGISTRATION.md` (WR-v0.2) | `5b522ce626dcaadd…` | `f7e0b21e0d65d0f3…` |
| DEL-02-04 `Design/ROLE_SUPPLY.md` (ROLE-v0.2) | `45a748697cf8fca8…` | same |
| ScopeOfWork DEL-01-05 / 02-02 / 02-04 | `baf68c79b5b8fdf0…` / `5814116909db8120…` / `3acfaa62a3bbf003…` | same (unchanged since INIT / SCA-V4-002) |
| Dependencies.csv DEL-01-05 / 02-02 / 02-04 | `3b038c98f97cd685…` / `be14a079c872695e…` / `0cb255b3270dfe61…` | same |

Other inputs read (sha256 prefix): `OWNER_DECISIONS.md` `8a5d11149045770d`;
R17 `b0af81bcbad9bc52`; R18 `abf5eee6324647ff`; R19 `16930ecdcead7511`;
R20 (with R21) `a9102712e0fb3c35`; `ASSESSMENT_SIWC.md` `e7d009373086c951`;
`F/F0_JOINS.md` `e93608be1c6e3eb0` (§3, §4, §5, §7.4–§7.6, §2 rows naming
these deliverables); `D/D4.md` `c2c7e74d91f2d121`; `D/D5.md`
`332bc81ff1851551`; `D/D6.md` `e47dd56f75289368`; `D/D3.md` (rows naming
these deliverables: SC3-01-04-1, -2, -6, -10, -11; NR-3, NR-4); `F/*.md`
(grep for proposals, then the relevant passages of F-A, F-C §4, F-E1, F-E2,
RX, RV21-A, RV21-B); `reviews/V21-A.md`, `V21-B.md`, `V21b-A.md`,
`V21b-B.md`; pass-2 `closeout/C1-A.md` `e2cb79e22ea5cf75`, `C1-B.md`
`c819ba9be9b92577`, `C1-C.md` `9c4b9a37a738740a`, `CLOSEOUT_ACCOUNT.md`
`703cd4bf5a7f280c`; `loop/LOOP_INIT.md` `3790159b4f60bb4f` ("Develop the
detail appropriate to the phase"); `docs/PRD.md` V4-APP-02/03, V4-WF-02/03,
V4-ROLE-01…03; `docs/ARCHITECTURE.md` V4-ARC-04; `_Decomposition/Open_Issues.csv`
OI-009, OI-010, OI-012, OI-018; DAG-003 `DependencyEdges.csv` (124) and
`CandidateEdges.csv` (78).

**Standing of everything below.** "Developed" means the Design files say
how the commitment is met and verified at the 60% description of
`loop/LOOP_INIT.md`. It is not evidence: no App candidate exists, no VER
case has run on one, and every prototype result is a "pass (model)". The
deliverables' Design files are DRAFT and PROPOSED.

---

## 1. DEL-01-05 Native OAuth/sign-in, API-key and local-provider access

### 1.1 Commitments → Design

| Item | Where answered (ACCESS-v0.2 unless named; AHR = account-home record) | Class |
|---|---|---|
| OUT-001 sign-in and API-key receiving, Codex custody | §5.1, §5.2, Q-2…Q-7, CR-1…CR-10, I-1 | developed |
| OUT-002 local-provider settings; all modes together; per-conversation choice | §2, §3, §4 (K2-1), §5.3, §5.4, Q-8…Q-11, NS-1, NS-2; schemas `access.state`, `access.conversation-selection` | developed |
| OUT-003 account-home and API-key definition records | AHR (choice K-1, mechanism M-A observed, OBS-2 O-6); §10 AK-1…AK-10 (types and strings only; OI-010 open) | partial (API-key half) |
| OUT-004 qualification, substitution, capability handoff | §11 CH-1…CH-8 with schema and fixture (developed); §12 method only (no qualification record format, no candidate) | partial |
| REQ-001 ChatGPT sign-in through Codex | Q-2, Q-3, AE-1…AE-20, CR-3 | developed |
| REQ-002 API key through Codex account methods | K2-1 (adopted, L-1), Q-6, Q-7, KE-1…KE-18; premise "one account per process" is `inference` (U-A2, deferred by L-6) | developed (premise labelled) |
| REQ-003 local servers as Codex providers | LP-1…LP-3, §5.3, Q-8, Q-9; per-entry capabilities and local model listing open (F-A2, U-A7) | developed (limits stated) |
| REQ-004 together; per-conversation selection; others preserved | §2, §4, §5.4 CS-1…CS-21, NS-1, NS-2 | developed |
| REQ-005 account-home record before integration | AHR §1–§6 (participants read per L-7) | developed |
| REQ-006 API-key behaviour defined against the pin | §10; OI-010 stays OPEN (AK-5, AK-6, AK-10 need a keyed observation the owner deferred, L-6) | partial |
| REQ-007 qualification and substitution | §12, VC-A07, VC-A08 (method; "model: routing only") | partial |
| REQ-008 capability requirements and limits to DEL-05-01 | §11, I-8, `access.capability-handoff`; read by LOOP-v0.9 §10.3 as information | developed |
| REQ-009 act boundary | §0, §14 | developed |
| AC-001 / VER-001 | VC-A01 (needs the person's sign-in and a candidate), VC-A13 custody scan (model) | developed |
| AC-002 / VER-002 | VC-A02; rests on REQ-006, so on OI-010 | partial |
| AC-003 / VER-003 | VC-A03 | developed |
| AC-004 / VER-004 | VC-A04, VC-A12, VC-A15, VC-A20 | developed |
| AC-005 / VER-005 | VC-A05 (review, runnable now) | developed |
| AC-006 / VER-006 | VC-A06; OI-010 open | partial |
| AC-007 / VER-007 | VC-A07, VC-A18 (S-4 receiving review); no qualification record design | partial |
| AC-008 / VER-008 | VC-A08 (routing model only) | partial |
| AC-009 / VER-009 | VC-A09, VC-A17 | developed |
| AC-010 / VER-010 | VC-A10, §14 | developed |

**Coverage: 33 items — 21 developed, 12 partial, 0 named only, 0 absent.**

### 1.2 Results without a commitment

| Result | Where | Disposition |
|---|---|---|
| Start-up traffic turned off where Codex's settings allow, plugin traffic following the person's setting, the rest shown and recorded (K-12, L-3, R18-3) | §9; schema `access.network-observation` | No SoW item: SC3-01-05-5 (D4 P-5) |
| No model until the person chooses; last choice offered, never applied; two refusal wordings (K-3, R18-2) | §5.4 | REQ-004 has no default rule: SC3-01-05-4 (P-4) |
| Codex account supplied for App act identity, RS `codexAccount` form (K1-4, C-10) | §8, I-6 | No SoW line: SC3-01-05-6 (P-6) |
| API key in a second App-owned home H-key (K2-1, L-1) | §3, §4 | REQ-002 reading: SC3-01-05-7 (P-7) |
| Inputs and focused checks to DEL-09-02 (I-9; DEP-09-02-013) | §1, §13 | Consumer row exists; this SoW names no DEL-09-02 handoff: SC3-01-05-12 and R3-01-05-b (new, §4) |
| Global `AGENTS.md` and `skills/` linked into App homes (R18-6, PROPOSED) | §3; AHR §4.1 | Integrator ruling, mechanism; no SoW change (K-1's wording "settings, providers and MCP servers" stays) |
| Probe home H-probe; S-4 receiving comparison (§19); SIWC alternative considered (§20) | §3, §19, §20 | Serve DEL-01-01 and the decision record; no SoW change. SIWC stays not adopted (P-11 conditional only) |
| Content sent to the chosen provider (installation id, thread/session/turn ids, time zone) shown | §9 | Within P-5's "shows and records"; optional mention in SC3-01-05-5 |

### 1.3 What the 60% description still lacks

- API-key behaviour unobserved (OI-010; AK-5, AK-6, AK-10) and K2-1's premise
  `inference` (U-A2, deferred by L-6). If a keyed observation or a later Codex
  version contradicts "one account per process", §4 is re-examined (§18
  version-bound list): the one structural risk left on the route to
  completion.
- No qualification record format and no substitution check beyond routing
  (REQ-007, AC-007, AC-008); no candidate.
- Local providers: per-entry capabilities and model listing (U-A7, F-A2);
  reachability check (U-A6).
- Linked configuration: writes through the link (AHR U-R3) and whether Codex
  follows linked `AGENTS.md` and `skills/` (U-A14) not observed.
- K-12 cells: update-check key (U-A13), `experimentalFeature/list` and
  plugins (U-A15), signed-in remote-control behaviour (not observed, L-6),
  analytics turn-back (U-A9, doctrine); socket-sampling mechanism unselected
  (§9 item 2).
- Login option elements (U-A4); H-key fate on removal (U-A5); email or digest
  in act records (U-A8, DEL-04-03); network observations in run records
  (U-A10, DEL-04-03); placement OI-008 (R17-5 PROPOSED).

### 1.4 Register: wrong, missing or stale (verified by script over all registers and DAG-003)

| Row | Observation | Proposal |
|---|---|---|
| Arc DEL-01-01 → DEL-01-05 (DEP-01-01-024, held, SCC-001) | No DEL-01-05 counterpart | R3-01-05-a (D4 P-9 = F0 M-4) |
| Arc DEL-09-02 → DEL-01-05 (DEP-09-02-013, admitted) | **No DEL-01-05 counterpart; not proposed by any node** (ACCESS §13 lists the row without noting it) | R3-01-05-b (new) |
| Arc DEL-05-01 → DEL-01-05 (DEP-01-05-014, admitted) | No DEL-05-01 counterpart | F0 M-5 (= pass-2 R-0501-4 = D4 NR-3), DEL-05-01's register |
| DEP-01-05-015 (OI-009 constraint) | TargetLocation "TBD"; Notes "OI-009 remains OPEN; record path and choice are unresolved" — the choice is made (K-1, L-7) and the record exists | R3-01-05-c (new) |
| DEP-01-05-016 (OI-010 constraint) | TargetLocation "TBD"; the definition record now exists (ACCESS §10); OI-010 still open | R3-01-05-d (new) |
| DEP-01-05-012 Notes | "OI-012/DEP-005 supplier identity … remain unresolved": lags DECISION-1 D4 (0.158.0 definition pin) | R3-01-05-e (new; pairs with SC3-01-05-3) |
| (none) DEL-01-04 consumes access state and the Codex account | ACCESS I-5, I-6, §13 | F0 NR-07 (new admitted arc) |

All other rows agree with ACCESS §13 (layers checked: -012/-013 held SCC-001;
-014 admitted; DEP-09-02-013 admitted).

---

## 2. DEL-02-02 Workflow-making workspace and registration

### 2.1 Commitments → Design (WR-v0.2)

| Item | Where answered | Class |
|---|---|---|
| OUT-001 one journey: plan, trial, draft, review, register, reuse, refine | §3–§6 (SQ-J, SQ-D, SQ-R, SQ-G, SQ-S), §16 (run text, chaining) | developed |
| OUT-002 source-qualified selection; collisions | §4.1 SP-1…SP-7, §4.4 SL-1…SL-7, §4.6 LS-1…LS-8 | developed |
| OUT-003 fixtures with candidate-bound results | §12 WR-VC-01…15; prototype 99/99; no candidate; WR-VC-04, -06 designed only; HY-1, HY-5, HY-7 designed only | partial |
| OUT-004 receiving and reuse account | §7, §10, §11 | developed |
| REQ-001 journey (K-7 reading) | §4.2 TT-1…TT-7, SQ-J, §16.3 | developed |
| REQ-002 draft until review and explicit registration | §4.3 RB-1…RB-8, §4.7, §9; A15 via DEL-01-04's act control (K-8) | developed |
| REQ-003 no silent overwrite | §4.1 (K-6 slot policy), DS-1…DS-7, G-1…G-5 | developed |
| REQ-004 source-qualified identity; no rebinding | §2.2 ID-1…ID-4, SL-1…SL-4; host listing deferred (U-WR-5, DECISION-3) | developed (host part deferred) |
| REQ-005 receive declaration, capability, checkpoint; distinguish resolved, supplied, observed | §16.4, §16.6 (supply check, "supplied — not verified"); RB-2 compatibility report beside review; WR-VC-04 designed only | partial |
| REQ-006 review/registration distinct from other acts; faithful record | RB-7, §9, RB-4a (RS-v0.9 form), AAC K-17 cross-check | developed |
| REQ-007 reuse account; stock Codex; open placement explicit | §10, §11, U-WR-2 | developed |
| REQ-008 no foreign acts | §0, §7, §16.1 | developed |
| AC-001 / VER-001 | WR-VC-01 (library steps on prototype; candidate needed) | developed |
| AC-002 / VER-002 | WR-VC-02, WR-VC-13 | developed |
| AC-003, AC-004 / VER-003 | WR-VC-03, WR-VC-10 (doubles; host side awaiting) | developed |
| AC-005 / VER-004 | WR-VC-04 designed only; WR-VC-14 on constructed frames | partial |
| AC-006 / VER-005 | WR-VC-05, WR-VC-12; positive case awaits DEL-01-04's control | developed |
| AC-007 / VER-006 | WR-VC-06 (inspection of §7, §10) | developed |
| AC-008 | §7 DEL-09-02 row; no candidate-bound results | partial |

**Coverage: 26 items — 21 developed, 5 partial, 0 named only, 0 absent**
(OUT 3/1, REQ 7/1, AC 6/2, VER 5/1).

### 2.2 Results without a commitment

| Result | Where | Disposition |
|---|---|---|
| Trial in an ordinary conversation, not a run (K-7) | §4.2 | SC3-02-02-1 |
| Revision series per slot; nothing overwritten (K-6) | §4.1 | REQ-003 says no policy is selected: SC3-02-02-2 |
| A15 captured by DEL-01-04's act control (K-8) | §4.3, §7 | SC3-02-02-3, -4 |
| Shipped workflows registered by the release; byte-equal library copies recognized (LS-8); the rest registered in place, several per act (§4.7) (DECISION-L L-4 A) | §4.6, §4.7 | **Owner decision with no SoW pointer; not proposed by D5**: SC3-02-02-11 (new) |
| Run-start text composed here, its identity recorded and checked against Codex's history; DEL-02-03 starts the run (R19-7, R21-4) | §16 | **Relied-on interface (DEL-02-03, DEL-01-04, DEL-04-03) with no SoW text**; D5 proposed only a register statement (SC3-02-02-9), which CONSERVATIVE extraction cannot ground without SoW text: SC3-02-02-12 (new) |
| Chaining (a) and (b), one run at a time (L-2, R19-2, R20-1, R20-11) | §16.3, §16.5 | SC3-02-02-10 |
| Hygiene HY-1…HY-7, published copy, pinned selection, agent line forms | §4.4, §4.5, §16.5 | Mechanism (claim granularity: code and tests); no SoW change |

### 2.3 What the 60% description still lacks

- Revision identity algorithm (U-WR-1; WD U-03), on which K-8's byte binding
  rests; act-record location outside a run (U-WR-3; RS U-05); placement
  (U-WR-2; OI-008); shared types (U-WR-8; OI-014).
- Host listing, relay and precedence (U-WR-5; DECISION-3).
- Integrator values: hygiene bounds (U-WR-7), published copy kept or dropped
  (U-WR-10), draft bases across machines (U-WR-12), pinned selection
  (U-WR-13), shipped-revision manifest contents incl. App v3 (U-WR-18).
- Supplier facts not observed: byte-exact echo of text elements (U-WR-14),
  `clientId` echo (U-WR-15, inference), context cost of carried run texts
  (U-WR-16, with DEL-01-05), dropping the earlier workflow on other models
  (U-WR-19).
- Designed, not run: WR-VC-04, WR-VC-06, HY-1/HY-5/HY-7, offer lifetimes
  (PR-5). (D5 R2.5's "End ‹A› and start ‹B›" not prototyped is superseded:
  RX2 P-64 runs it.) Positive A15 awaits DEL-01-04's control.
- No further structural change is anticipated: R19-7 already moved
  run-start supply here during the pass.

### 2.4 Register: wrong, missing or stale

| Row | Observation | Proposal |
|---|---|---|
| DEP-02-02-013 Statement | Names no act control | SC3-02-02-6 (F0 ST-2) |
| DEP-02-02-016/-017 Statements | Do not name A15 or its RS record kind | SC3-02-02-7 (F0 ST-3 = pass-2 C1-A note) |
| DEP-02-02-015 (and DEL-02-03's DEP-02-03-010) | No run-start text | SC3-02-02-9 (D5 R2.4) |
| Arc DEL-01-04 → DEL-02-02 (DEP-01-04-009, held) | No DEL-02-02 counterpart | R3-02-02-a (new) |
| Arc DEL-02-03 → DEL-02-02 (DEP-02-03-010, held) | No DEL-02-02 counterpart | R3-02-02-b (new) |
| Arc DEL-09-06 → DEL-02-02 (DEP-09-06-026, admitted) | No DEL-02-02 counterpart | R3-02-02-c (new) |
| (none) DEL-04-03 consumes run-text, supply-check and A15 relation records | RS-v0.9; WR §7 | R20-10 (F-C §4), held, SCC-neutral; DEL-02-02 mirror R3-02-02-d (new) |
| (none) DEL-02-02 → DEL-01-02 | WR §7 (SQ-X at App start) | F0 NR-04 (= D5 NR-1), optional, new admitted arc |
| Supplier-side mirrors in DEL-02-01, 02-03, 04-01, 04-03 for DEP-02-02-014…017 | One side only (checked) | Owned by those registers; pass-2 C1-A "outside mirrors noted, not proposed" and SC2-02-01-2, SC2-02-03-6, SC2-04-03-1 stand; not re-proposed here |

WR §7's layer labels agree with DAG-003 for every row (checked by script).

---

## 3. DEL-02-04 Additive role selection and supply

### 3.1 Commitments → Design (ROLE-v0.2)

| Item | Where answered | Class |
|---|---|---|
| OUT-001 four-role selection, additive supply, TASK restriction | §3, §4, §5 | developed |
| OUT-002 identity and limit account | §6.1–§6.4; schemas `role-supply-record` 0.2, `role-limit-account` 0.2 | developed |
| OUT-003 fixtures with candidate-bound results | §10, §11; prototype 36/0; no candidate | partial |
| REQ-001 exactly four; identities kept; no fifth | SL-1…SL-8 ("No role" is not a fifth role, SL-2) | developed |
| REQ-002 additive supply; harness instructions intact; role configuration | §5.1, §5.2 (developerInstructions at `thread/start` only), §4.3; child roles §5.3 with the **carrier unobserved** (CR-1a, U-R3) | partial |
| REQ-003 TASK does not delegate; enforcement stated truthfully; others keep delegation | L-TASK-1, LA-1…LA-5, DL-1…DL-6 (observed through an adapter, R18-9) | developed |
| REQ-004 source identity and bytes; five facts apart; evidence to record/adoption interfaces | §6.1, §6.4, O-2, O-3 | developed |
| REQ-005 reuse or replacement | §9 (text largely in v0.1; see §3.3) | developed |
| REQ-006 no foreign acts | §1, §15 | developed |
| AC-001 / VER-001 | VC-R1 (RC-01, -03, -04) | developed |
| AC-002 / VER-002 | VC-R2, VC-R12 (one role observed, OBS-2 O-5) | developed |
| AC-003 / VER-003 | VC-R3 (B-18 through an adapter; not provokable on stock LM Studio) | developed |
| AC-004 / VER-004 | VC-R4 (RC-13, IL-1) | developed |
| AC-005 / VER-005 | VC-R5: negative offline; positive awaits DEP-006 / OI-024 | partial |
| AC-006 / VER-006 | VC-R6 | developed |

**Coverage: 21 items — 17 developed, 4 partial, 0 named only, 0 absent**
(OUT 2/1, REQ 5/1, AC 5/1, VER 5/1).

### 3.2 Results without a commitment

| Result | Where | Disposition |
|---|---|---|
| No-role conversations; preselection as data; role fixed for life; "Continue as ‹role›" with a handoff summary (R17-9, L-2, R19-3, R20-6) | §3 | SC3-02-04-5 (amended) |
| Guidance store, seeding, release upgrade, "guidance changed since this conversation started" (K-9 as amended by L-2) | §4 | SC3-02-04-2 (amended) |
| Task limit "stated, not enforced"; delegation recorded and shown (K-10) | §6.2, §6.3 | SC3-02-04-4 |
| Native child roles with product guidance in each file; a child with no role type has unknown guidance (R18-4) | §5.3 | SC3-02-04-6 (amended) |
| Shipped guidance states the two agent lines (GS-7; R20-5, R20-9, R20-11) | §4.2 | App content; the line forms are WR §16.5's and NIR §5.7's; no SoW change |
| Fork as a same-role copy; supply-record log | §3.3 F-1; §6.1 | Mechanism; no SoW change |

### 3.3 What the 60% description still lacks

- **ROLE-v0.2 is not self-contained.** It defers to v0.1 text that exists
  only in git history (`63a6e0fa47`): "As v0.1" for §4.1 role set, §4.2
  GS-1…GS-5, the T-1 table, CO-1/CO-2/CO-5/CO-6, §6.4, §8, §9 (the reuse
  table AC-006 reviews), §15, F-R1…F-R8, and v0.1's input table (checked:
  `git show 63a6e0fa47:…/ROLE_SUPPLY.md` holds them; the working tree does
  not). A reader of the current file cannot see the GS rules, T-1 states or
  the reuse dispositions. **Returned to the graph as Design production work**
  (fold the v0.1 text into ROLE in place), not a proposal; V21-A did not
  raise it.
- Child-role carrier (U-R3, CR-1a): per-thread `config` or `-c` session flags,
  neither observed for `agents.*`; with session flags every conversation of
  that process (TASK and no-role included) would see the child roles. The
  one item here that could still change §5.3's structure.
- Non-empty `instructionSources` (U-R14, B-6) and Codex following linked
  global guidance (ACCESS U-A14); delegation facts observed only through an
  adapter (R18-9).
- Content-identity algorithm (U-R1); size bound (U-R4); OI-008/OI-014
  placement (U-R5, U-R6); host seat mapping (U-R7, deferred); adoption
  evidence (U-R8; OI-024, DEP-006); release upgrade (U-R9); compatible-roles
  display (U-R10); shipped default (U-R11); fork dependence (U-R13).

### 3.4 Register: wrong, missing or stale

| Row | Observation | Proposal |
|---|---|---|
| DEP-02-04-010 Statement | Carriage only; ROLE reads status, delegation items (child discovery by completed `spawnAgent` and `thread/read`) and `config/read` | SC3-02-04-8 (F0 ST-4, amended by D6 R2.3) |
| Arc DEL-02-04 → DEL-01-01 (DEP-02-04-010, admitted) | No DEL-01-01 counterpart | F0 M-6 = pass-2 C1-B R-11-1 (DEL-01-01's register) |
| Arc DEL-03-04 → DEL-02-04 (DEP-03-04-010, admitted) | **No DEL-02-04 counterpart** | R3-02-04-a (new) |
| Arc DEL-10-03 → DEL-02-04 (DEP-10-03-010, admitted) | **No DEL-02-04 counterpart** | R3-02-04-b (new) |
| DEP-02-04-012 (→ DEL-04-03, held) and -013 (→ DEL-11-02, admitted) | No consumer-side row in DEL-04-03 or DEL-11-02 | Owned by those registers (DEL-04-03 is C1-A's); returned, not proposed here |
| DEP-02-04-016 (OI-018 constraint) | Answered for the App by K-9 as amended by L-2; Notes silent | R3-02-04-d (new, Notes only) |
| **ROLE §7.2 O-8 vs NIR IF-15** | ROLE: DEL-01-04 receives the preselection and fixed-role display as a runtime value, "none" row. NIR-v0.2 IF-15 and D3 R2.5 propose **NR-4** (DEL-01-04 → DEL-02-04, held, SCC-neutral) for the role list with `default_for_new_chat`, the "Continue as" composition and the guidance-changed signal; D3's SC3-01-04-11 grounds it in DEL-01-04's SoW. The two Design files disagree | Keep NR-4 (a design-time format exchange is a production interface, as NR-07 is for ACCESS I-5); ROLE §7.2 O-8 and §7.3 should cite NR-4: **Design edit returned to the graph**; mirror R3-02-04-c conditional on NR-4 |
| NR-06 (DEL-02-04 → DEL-01-03), NR-10 (DEL-02-04 → DEL-02-02) | Dropped (R18-1 C-07; R19-7) | Withdrawn; ROLE §7.3 says so |

---

## 4. Proposals collected (none applied)

IDs: D4's P-n are renamed SC3-01-05-n as F0 §4.1 suggests. "New (C1-B)"
marks items this comparison raises; everything else was raised earlier in the
run and is deduplicated here with its sources.

### 4.1 ScopeOfWork

| ID | File, location | Old → new (substance; full text at source) | Reason | Source | Status |
|---|---|---|---|---|---|
| SC3-01-05-1 | DEL-01-05 TBD-001 | "OI-009 remains OPEN…" → decided by DECISION-K3 K-1 (shared settings, providers and MCP servers; separate sign-in custodied by Codex in an App-owned home), by the Owner, who is also the App implementation owner (DECISION-L L-7); mechanism observed to work at Codex 0.158.0 (OBS-2 O-6); fallback (own settings) if a pinned version cannot, said so | Owner decided | D4 P-1 and R2.4; K-1, L-7 | keep, amended |
| SC3-01-05-2 | DEL-01-05 CLM-001 last sentence | "This does not choose a v4 account home." → "The account home is chosen under TBD-001." | Follows -1 | D4 P-2 | keep |
| SC3-01-05-3 | DEL-01-05 TBD-003 | "unidentified supplier pin" → 0.158.0 definition/generation pin (DECISION-1 D4); qualification pin, protocol and endpoint evidence stay under OI-012, DEP-005 | Lags D4 | D4 P-3; F0 class of SC3-01-02-6 | keep |
| SC3-01-05-4 | DEL-01-05 REQ-004, AC-004, VER-004 | Add: no mode or model applied until the person chooses; last explicit choice per project may be offered, never applied silently; refusal wordings "not started — no model selected" / "run not started — no model selected" | K-3; R18-2 | D4 P-4; = SC3-01-04-6 (amended) in substance for DEL-01-04's display | keep, amended (two wordings) |
| SC3-01-05-5 | DEL-01-05 new REQ-010, AC-011, VER-011 | Turn off the start-up traffic Codex's settings allow, plugin traffic following the person's plugin setting; show and record the rest per supplier version, naming which is which (optionally: and the identifiers and time zone Codex sends to the chosen provider) | K-12, L-3, R18-3; HOSTING U-18 names DEL-01-05 | D4 P-5 and R2.4; supersedes pass-2 C1-B §7 B-1 | keep, amended |
| SC3-01-05-6 | DEL-01-05 OUT-002 or new REQ-011 | Supply the Codex account as reported (the reported email, or "ChatGPT account (no email reported)"; plan type not recorded) for App act identity, marked identity not verified | K1-4; C-10 | D4 P-6; related pass-2 SC2-04-03-3, SC2-02-03-5 | keep, amended (C-10 form) |
| SC3-01-05-7 | DEL-01-05 REQ-002 | Add: where the pinned protocol keeps one account per Codex home, the API key is held by Codex in a separate App-owned home | K2-1 adopted (L-1 A) | D4 P-7, R2.4 | keep, now unconditional |
| SC3-01-05-10 | DEL-01-05 REQ-005, **and TBD-001 "Responsible participants"** | "the Owner with the App implementation owner" → "the Owner, who is also the App implementation owner (DECISION-L L-7)" | L-7 | D4 R2.4 P-10; extended here to TBD-001 | keep, extended (C1-B) |
| SC3-01-05-12 | DEL-01-05 CLM-004 or OUT-004, end | Add: "DEL-09-02 receives the account/provider inputs and the focused sign-in and concurrent-mode checks for V4-EXM-12 and declares them upstream in its own register." | Grounds mirror R3-01-05-b; DEP-09-02-013 exists, the SoW is silent | ACCESS I-9, §13; DEP-09-02-013 | **new (C1-B)** |
| SC3-01-05-13 (optional) | DEL-01-05 TBD-002 | Append: "The definition record is DEL-01-05 Design ACCESS §10 (draft); OI-010 stays open until supported behaviour is observed (deferred by the owner, DECISION-L L-6)." | Navigation pointer, like -1 | ACCESS §10; L-6 | **new (C1-B)**, optional |
| SC3-02-02-1 | DEL-02-02 REQ-001 | Add: a draft is tried in an ordinary conversation, not a run; only registered revisions run | K-7 | D5 | keep |
| SC3-02-02-2 | DEL-02-02 REQ-003 last sentence | "…does not select a new overwrite policy." → K-6's revision series, refusal with a request for a new name, nothing overwritten | K-6 | D5 | keep |
| SC3-02-02-3 | DEL-02-02 REQ-002 | Add: registration by the person through DEL-01-04's App act control, bound to the exact reviewed content; changed after review needs a new review | K-8 | D5 | keep |
| SC3-02-02-4 | DEL-02-02 CLM-002; REQ-008 | Name the App act control under DEL-01-04 | K-8 | D5; pairs SC3-01-04-2 | keep |
| SC3-02-02-5 (optional) | DEL-02-02 OUT-002, REQ-004, AC-004, VER-003 | "host-supplied" → "host (origin `host`)" | Terminology | D5 | **recommend drop**: the basis V4-WF-03 itself says "host-supplied"; WR's header reading 4 already maps it (lift, not rewrite) |
| SC3-02-02-10 | DEL-02-02 REQ-001 / OUT-001 | Add: workflows chained within one conversation, one run at a time, sequentially or on the agent's proposal with the person confirming | L-2 | D5 R2.4 | keep |
| SC3-02-02-11 | DEL-02-02 REQ-002 (append) or REQ-004 | Add: "Workflows shipped with an App release are registered by the release (origin bundled); a library entry byte-equal to a shipped revision is recognized as that revision; other library content without a registration record is registered in place by the person's act, several entries per act allowed, each entry's bytes bound (DECISION-L L-4)." | Owner decision; LS-8 and §4.7 have no SoW pointer, and REQ-002 reads as if every runnable workflow needs the person's registration | DECISION-L L-4 A (clarified); R19-4; WR §4.6, §4.7 | **new (C1-B)** |
| SC3-02-02-12 | DEL-02-02 CLM-003 (append) | Add: "For each run `DEL-02-03` starts, this workspace composes the run-start text from the selected registered revision, records its content identity and checks it against Codex's history; the run text and its supply-check record are received by `DEL-02-03`, `DEL-01-04` (turn composition) and `DEL-04-03` (supplied-workflow evidence), and the workspace's draft, registration and selection contract by `DEL-01-04`, `DEL-02-03` and `DEL-09-06`, each of which declares it upstream in its own register." | R19-7 moved supply ownership here; grounds SC3-02-02-9, R20-10 and mirrors R3-02-02-a…d | R19-7, R20-3, R20-10, R21-4; WR §7, §16 | **new (C1-B)** |
| SC3-02-04-1 | DEL-02-04 open-matter table, OI-001/002/012/017 rows | Ruled (D2/D3); 0.158.0 definition pin (D4); OI-017 resolved for the definition run | Lags | D6 | keep |
| SC3-02-04-2 | DEL-02-04 OI-018 row | Answered for the App by K-9 as amended by L-2: shipped defaults, seeded editable copy, changes reach new conversations, open ones show the guidance changed, recorded by content; open for hosts | K-9, L-2 | D6, R2.3 | keep, amended |
| SC3-02-04-4 | DEL-02-04 REQ-003, AC-003 | Add K-10: "stated, not enforced"; delegation recorded and shown; no override of the person's configuration | K-10 | D6; = SC3-01-03-5 in substance (different deliverable; keep both) | keep |
| SC3-02-04-5 | DEL-02-04 REQ-001, AC-001 | Add: no-role conversations (not a fifth role); preselection as data, shown and clearable; role fixed for the conversation's life; another role is a new conversation | R17-9, L-2 | D6, R2.3 | keep, amended |
| SC3-02-04-6 | DEL-02-04 REQ-002 or CLM-004 | Add: children receive product guidance and their role through native agent-role configuration where supported, added without replacing the person's definitions; a child spawned without a role type has unknown guidance, said so | R17-9 as amended by R18-4 | D6, R2.3 | keep, amended |
| SC3-02-04-7 | DEL-02-04 TBD-001 | Add: OI-018 answered for the App (K-9 as amended by L-2); pin 0.158.0 for definition (D4) | Consistency (SCA-V4-002 precedent) | D6 | keep, amended (L-2) |
| SC3-02-04-9 | DEL-02-04 CLM-002 (append) | Add: "Its role-guidance semantics are received by `DEL-03-04` and its supply obligations by `DEL-10-03`[, and its role list and guidance-changed signal by `DEL-01-04`], each of which declares it upstream in its own register." (bracket only if NR-4 is adopted) | Grounds mirrors R3-02-04-a…c | DEP-03-04-010, DEP-10-03-010; ROLE §7.2 O-4, O-5; NIR IF-15 | **new (C1-B)** |

Withdrawn or superseded: SC3-02-04-3 (workflow supply in REQ-002; withdrawn
by D6 under R19-7); SC3-02-02-8 (subsumed by DEL-01-04's SC3-01-04-1, which
amends pass-2 SC2-01-04-1); SC3-01-05-11 (D4 P-11, the SIWC SoW and
OBJ-002 changes) is **not proposed** — conditional on reopening (ACCESS §20
triggers T-1…T-4).

Related items in other deliverables' SoWs that name these three (C1-A
collects them): SC3-01-04-1 (A15, consumer DEL-02-02), SC3-01-04-2,
SC3-01-04-6, SC3-01-04-10 (run-start text from DEL-02-02), SC3-01-04-11
(roles from DEL-02-04; agent proposals).

### 4.2 Open_Issues (`_Decomposition/Open_Issues.csv`; scope-change route)

| ID | Row | Old → new | Source | Status |
|---|---|---|---|---|
| SC3-01-05-8 | OI-009 Status / Consequence | OPEN → decided at choice level (K-1; owner who is also the App implementation owner, L-7); mechanism observed at Codex 0.158.0 (O-6); separation with a credential not observed (L-6) | D4 P-8, amended | keep, amended |
| OI-018 (optional) | OI-018 Consequence, append | "For the App, answered by DECISION-K3 K-9 as amended by DECISION-L L-2 (APP-V4-DESIGN-PASS-3-20261001); hosts and other instruction owners remain open." | K-9, L-2; SOW-220 is wider than the App, so the issue stays OPEN | **new (C1-B)**, optional |

### 4.3 Registers

| ID | Register | Change | Class | Source | Status |
|---|---|---|---|---|---|
| R3-01-05-a | DEL-01-05 | DOWNSTREAM HANDOVER → DEL-01-01, mirror of DEP-01-01-024 (sign-in and substitution evidence when needed) | mirror (held arc, SCC-001) | D4 P-9 = F0 M-4; pass-2 C1-B §5.5 observed it | keep |
| R3-01-05-b | DEL-01-05 | DOWNSTREAM HANDOVER → DEL-09-02, mirror of DEP-09-02-013 | mirror (admitted) | this comparison; with SC3-01-05-12 | **new (C1-B)** |
| R3-01-05-c | DEL-01-05 | DEP-01-05-015: TargetLocation TBD → `Design/ACCOUNT_HOME_DECISION_RECORD.md`; TargetName "…Owner and App implementation owner choice" → "…the Owner's choice (also App implementation owner, L-7)"; Notes: decided at choice level (K-1), mechanism observed (O-6). Satisfaction left to the amendment's extraction | non-topological | follows SC3-01-05-1, -8, -10 | **new (C1-B)** |
| R3-01-05-d | DEL-01-05 | DEP-01-05-016: TargetLocation TBD → ACCESS §10; Notes: OI-010 open (L-6) | non-topological | follows SC3-01-05-13 | **new (C1-B)** |
| R3-01-05-e | DEL-01-05 | DEP-01-05-012 Notes: 0.158.0 is the definition/generation pin (D4); qualification pin open | non-topological | follows SC3-01-05-3 | **new (C1-B)** |
| M-5 | DEL-05-01 | UPSTREAM INTERFACE → DEL-01-05, mirror of DEP-01-05-014 | mirror (admitted) | pass-2 C1-C R-0501-4 = D4 NR-3; LOOP-v0.9 §10.3 G-10 | keep (the "not consumed" alternative is weaker now that LOOP reads the handoff) |
| NR-07 | DEL-01-04 | UPSTREAM INTERFACE → DEL-01-05 (access and selection state; Codex account) | **new admitted arc** (DAG departure) | D3 NR-3 = D4 NR-1 | keep |
| R-11-3 | DEL-01-01 | DEP-01-01-022 Notes: namespace route limit (F-31) and approval-carrier quirk (F-32) | non-topological | pass-2 C1-B | keep, extended: delegation tools travel in the same `namespace` tool (OBS-2 O-4, via an adapter); the account is now at ACCESS §11 CH-1…CH-8 |
| SC3-02-02-6 | DEL-02-02 | DEP-02-02-013 Statement: add the App act control and capture evidence | non-topological | D5 = F0 ST-2; pairs DEL-01-04's SC3-01-04-9 | keep |
| SC3-02-02-7 | DEL-02-02 | DEP-02-02-016/-017 Statements: name A15 and its RS record kind | non-topological | D5 = F0 ST-3 = pass-2 C1-A note | keep |
| SC3-02-02-9 | DEL-02-02 / DEL-02-03 | DEP-02-02-015 and DEP-02-03-010 Statements: add the run-start text, its identity and supply check | non-topological (held arc) | D5 R2.4; needs SC3-02-02-12 for grounding | keep |
| R3-02-02-a…c | DEL-02-02 | DOWNSTREAM rows → DEL-01-04 (mirror of DEP-01-04-009), DEL-02-03 (DEP-02-03-010), DEL-09-06 (DEP-09-06-026) | mirror (held, held, admitted) | this comparison; with SC3-02-02-12 | **new (C1-B)** |
| R20-10 | DEL-04-03 | UPSTREAM INTERFACE → DEL-02-02 (run text, supply check, A15 relations) | new arc, held (SCC-002), SCC-neutral | F-C §4; R20-10 | keep |
| R3-02-02-d | DEL-02-02 | DOWNSTREAM HANDOVER → DEL-04-03, mirror of R20-10's row | mirror | with SC3-02-02-12 | **new (C1-B)** |
| NR-04 (optional) | DEL-02-02 | UPSTREAM INTERFACE → DEL-01-02 (stop definitions; App-start reconciliation) | **new admitted arc** (DAG departure) | D5 NR-1 = F0 NR-04 | keep, optional |
| SC3-02-04-8 | DEL-02-04 | DEP-02-04-010 Statement: add status, delegation-item (completed `spawnAgent`, `thread/read`) and configuration-read surfaces | non-topological | D6 = F0 ST-4, amended R2.3 | keep, amended |
| M-6 | DEL-01-01 | DOWNSTREAM → DEL-02-04, mirror of DEP-02-04-010 | mirror (admitted) | pass-2 C1-B R-11-1 | keep |
| R3-02-04-a, -b | DEL-02-04 | DOWNSTREAM rows → DEL-03-04 (mirror of DEP-03-04-010), DEL-10-03 (DEP-10-03-010) | mirror (admitted) | this comparison; with SC3-02-04-9 | **new (C1-B)** |
| NR-4 | DEL-01-04 | UPSTREAM INTERFACE → DEL-02-04 (role list, "Continue as" composition, guidance-changed signal) | new arc, held (SCC-002), SCC-neutral | D3 R2.5; NIR IF-15 | keep; ROLE O-8 to be aligned (§3.4) |
| R3-02-04-c (conditional) | DEL-02-04 | DOWNSTREAM → DEL-01-04, mirror of NR-4 | mirror | only if NR-4 is adopted | **new (C1-B)** |
| R3-02-04-d | DEL-02-04 | DEP-02-04-016 Notes: OI-018 answered for the App (K-9 as amended by L-2); open for hosts | non-topological | follows SC3-02-04-2 | **new (C1-B)** |

Withdrawn: NR-06 (DEL-02-04 → DEL-01-03; R18-1 C-07), NR-10
(DEL-02-04 → DEL-02-02; R19-7).

**Graph check (script over DAG-003, consumer → supplier, Tarjan).** Base
SCC sizes 2, 2, 2, 2, 3, 13. Adding NR-07, NR-04, NR-4 and R20-10, singly
or together, changes no SCC, and the admitted layer stays acyclic; mirror
rows add no arc. DEL-01-05 → DEL-01-02 would change an SCC (confirms ACCESS
§1's runtime-value treatment of `assess live work`). Agrees with F0 §3 and
V21-B check 6. NR-07 and NR-04 are new admitted arcs, so the amendment needs
a `project-dag` departure; the rest move only source currency.

### 4.4 Basis

None proposed. Considered:

- **Custody amendment for the ChatGPT plan grant** (V4-ARC-04: "custodied by
  Codex, or, for a ChatGPT plan grant made to Chirality, by the App in
  protected OS storage"): conditional on reopening SIWC (ACCESS §20 CA-2;
  ASSESSMENT_SIWC recommendation 3, superseded in part); not proposed.
- **Start-up traffic** (pass-2 C1-B §7 B-1): answered by the owner (K-12, L-3);
  the SoW route is SC3-01-05-5; no basis text needed.
- **V4-WF-02 and L-4.** "A new or changed workflow is a draft until the person
  reviews it and registers it explicitly" is not contradicted by shipped
  workflows registered by the release (they are neither new nor changed by
  the person); SC3-02-02-11 suffices.
- **Root `AGENTS.md`** (not the v4 basis): "Instruction changes take effect at
  a verified idle boundary" vs L-2 (new conversations only; ROLE F-R9), and
  "does not veto the user's Codex configuration" vs the App's analytics-off
  session flag (ACCESS U-A9). Instruction-change notice candidates for the
  integrator, outside SCA-V4-003.

### 4.5 Counts

Live total: 48 items (25 ScopeOfWork, 2 Open_Issues, 21 register), of which
15 are new from this comparison.


| Kind | Live | of which new (C1-B) | Optional or conditional | Withdrawn / superseded / not proposed |
|---|---:|---:|---:|---:|
| ScopeOfWork (DEL-01-05 10, DEL-02-02 8, DEL-02-04 7) | 25 | 5 (SC3-01-05-12, -13; SC3-02-02-11, -12; SC3-02-04-9) | 2 (SC3-01-05-13; SC3-02-02-5, recommended drop) | 3 (SC3-02-04-3, SC3-02-02-8, SC3-01-05-11) |
| Open_Issues | 2 | 1 (OI-018) | 1 | 0 |
| Register items (table rows; 15 in these three registers, 6 in other registers naming them) | 21 | 9 items, 12 rows (R3-01-05-b…e; R3-02-02-a…c, -d; R3-02-04-a, -b, -c, -d) | 2 (NR-04; R3-02-04-c) | 2 (NR-06, NR-10) |
| New arcs among them | 4 (NR-07, NR-04 admitted; NR-4, R20-10 held) | 0 | 1 (NR-04) | — |
| Basis | 0 | — | 1 conditional (custody) | — |

## 5. Pass-2 proposals naming these deliverables

| Pass-2 item | Disposition in this run |
|---|---|
| C1-A SC2-01-04-1 (= C1-B X-1), consumer list | **Superseded (amended)** by DEL-01-04's SC3-01-04-1 (adds A15 and DEL-02-02, multi-entry per L-4); SC3-02-02-8 is subsumed |
| C1-A SC2-04-01-4 (DEL-04-01 REQ-002 names registration, citing DEL-02-02 REQ-002, AC-006) | **Kept**; optional change: add "captured through DEL-01-04's App act control (K-8)" |
| C1-A SC2-04-03-1 (DEL-04-03 consumers incl. DEL-02-02) | **Kept** |
| C1-A SC2-02-01-2 (DEL-02-01 receivers incl. DEL-02-02, DEL-02-04) | **Kept** (DEP-02-02-014 and DEP-02-04-011 still consume DEL-02-01) |
| C1-A SC2-02-03-6 (DEL-02-03 receivers incl. DEL-02-02) | **Kept**; the reverse flow (DEL-02-03 receiving DEL-02-02's run text) is SC3-02-02-9/-12 |
| C1-A note "DEL-02-02's register should name A15 and its RS record kind" | **Kept** as SC3-02-02-7 (F0 ST-3) |
| C1-A "outside mirrors noted, not proposed" (DEL-04-01, 04-03, 02-01, 02-03 → DEL-02-02; DEL-02-01 → DEL-02-04) | **Kept** as noted, for those registers; not re-proposed |
| C1-B R-11-1 (DEL-01-01 mirrors incl. DEL-02-04) | **Kept** (F0 M-6) |
| C1-B R-11-3 (DEP-01-01-022 Notes → DEL-01-05) | **Kept, changed**: extended to delegation (O-4) and pointed at ACCESS §11 |
| C1-B §5.5 observation (DEP-01-01-024 has no DEL-01-05 counterpart) | **Changed**: now proposed as R3-01-05-a (D4 P-9) |
| C1-B §6 "which approval carrier the App uses is DEL-01-05's" (F-32) | **Answered in Design** (ACCESS Q-1 step 3: a refusal caused by the person's configuration is shown, never "fixed"); no proposal |
| C1-B §7 B-1 (start-up traffic, basis) | **Superseded** by K-12/L-3 and SC3-01-05-5 |
| C1-B §3 OUT-002 note (GUIDE row 8 rests on SoW meaning for DEL-02-04) | **Superseded** by ROLE-v0.2 and GUIDE-v0.6 (G-1 closed, F-E2) |
| C1-C R-0501-4 (DEL-05-01 mirror of DEP-01-05-014) | **Kept** (F0 M-5) |
| CLOSEOUT_ACCOUNT ("DEL-01-04's App act control … SC2-01-04-1") | As SC2-01-04-1 above |

## 6. Lifecycle observation (no change made)

`_STATUS.md` of all three reads **INITIALIZED** (2026-09-27; history OPEN →
INITIALIZED by WORKING_ITEMS). Under `_COORDINATION.md` INITIALIZED means
"a checked contract exists", which stays true; nothing here is false.
It no longer describes the work, though: each deliverable now has v0.2
Design files, schemas and prototypes from this run's active design work,
which Root `docs/SPEC.md` §3.2 describes as IN_PROGRESS ("Active human + agent
work"; transition INITIALIZED → IN_PROGRESS by the Human or WORKING_ITEMS).
The precedent is the owner's direction to record IN_PROGRESS for the 14
first-increment deliverables when their design work began
(`APP-V4-BASIS-ALIGN-20260928` OWNER_DECISIONS). Recording it here is a
human or WORKING_ITEMS act, returned to the integrator; CHECKING is not
warranted (no candidate, no VER evidence). Separately: DEL-01-05 and
DEL-02-04 have no `MEMORY.md` (DEL-02-02 has one); the MEMORY-rows node
creates or appends them.

## 7. Returned to the graph (Design production work, not proposals)

1. **ROLE-v0.2 self-containment** (§3.3): fold the v0.1-only text (§4.1,
   GS-1…GS-5, T-1, CO rules, §6.4, §8, §9, §15, F-R1…F-R8, input table) into
   ROLE in place.
2. **ROLE §7.2 O-8 / §7.3 vs NR-4** (§3.4): cite NR-4 (or the integrator
   rules the role list a runtime value and NIR IF-15 drops NR-4).
3. **ACCESS §13**: add DEP-09-02-013's missing supplier-side counterpart
   (R3-01-05-b) to its register table, once decided.
4. Supplier-side rows owed by other registers: DEL-04-03 for DEP-02-04-012,
   DEL-11-02 for DEP-02-04-013 (C1-A / outside).
5. Lifecycle question (§6).

## 8. How checked

- Commitments: every OUT, REQ, AC, VER of the three ScopeOfWork files read in
  full and mapped against the Design files read in full (ACCESS 1 054 lines,
  AHR, WR 592 lines, ROLE 566 lines).
- Registers: a script read every `Dependencies.csv` in the execution tree
  (ACTIVE EXECUTION DELIVERABLE rows), formed consumer → supplier arcs and
  compared each arc touching these three deliverables with DAG-003's two edge
  files: layer and which side holds a row. Findings in §1.4, §2.4, §3.4.
- Prototypes rerun on 2026-10-02 at HEAD `b10a04b5bb` with C0's working-tree
  edits, Python 3, `-B`, `PYTHONDONTWRITEBYTECODE=1`, no record or
  example-writing flags: ACCESS `run_cases.py` TOTAL 9, FAIL 0, exit 0; WR
  `wrproto.py` 99 checks, 99 passed; ROLE `run_cases.py` pass=36 fail=0.
  `git status --porcelain --untracked-files=all` identical before and after.
- ROLE's v0.1 dependence: `git show 63a6e0fa47:<ROLE path>` contains GS-1,
  GS-5, T-1, CO-1…CO-6, §6.4, §8, §9 and F-R1…F-R8; the working-tree file
  cites them as "As v0.1".
- Quotes of ScopeOfWork, register and basis text were copied from the files
  at the hashes above. What the files state is separated from inference;
  inferences are marked ("recommend", "the one structural risk").
- Nothing here claims qualification, a host join, a SWBPIPE adoption, a
  human act, or that any proposal is accepted.
