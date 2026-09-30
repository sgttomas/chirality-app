# S1-A — scoping survey: DEL-04-01, DEL-04-02, DEL-04-03

- Run `APP-V4-DESIGN-PASS-2-20260930`, node **S1-A**. Executor: Type 2 TASK
  (Claude Code subagent; no delegation). Read-only on project state; this file
  is the only write. No git write, no network.
- Read at working tree = `HEAD` `4698471d9e` (the three Design files, SoWs and
  registers are unmodified in the tree).
- Files surveyed (sha256 recomputed with `shasum -a 256`):

| Short | File | Version in header | sha256 (current) | Last commit |
|---|---|---|---|---|
| ACT | DEL-04-01 `Design/ACT_AND_POLICY_CONTRACT.md` (1692 lines) | ACT-POLICY-v0.6 | `6889003e6c1c2dd6d58b7145dd7955651debcc7b705a84e63aa6cd4e596e4815` | `caa4334ca1` |
| AS | DEL-04-02 `Design/AUTONOMY_AND_STANDING_EXCHANGE.md` (614 lines) | AS-v0.6 | `52d1341bb475f0a7de4b986b905e2986aa0e0a4e04e8b1783a6a83174eb6a33d` | `caa4334ca1` |
| RS | DEL-04-03 `Design/RECORD_SEMANTICS.md` (700 lines) | RS-v0.6 | `96b1aeeb120be597c4f35eea13f6a60ce20783e555c918521aacee38c5bcf666` | `caa4334ca1` |

All three hashes equal GUIDE-v0.3's input table (GUIDE lines 21–23).

**Method.** Each Design file was read whole. Also read whole: the three
`ScopeOfWork.md`, `Dependencies.csv` (every EXECUTION row), the three
`_DEPENDENCIES.md`, DAG-003 `HANDOFF_STATE.md`,
`R8_RESOLUTIONS.md`, the four runs' `OWNER_DECISIONS.md`, first-run
`reviews/V6.md`, `closeout/CLOSEOUT_ACCOUNT.md` and `C1-A.md` (the three
PKG-04 sections), intake `reviews/V9.md` and `V10.md` (from the verdict),
`RV-1_DEL-04-01.md`, the diffs and E-block tables of `RV-1_DEL-04-02.md`,
`RV-1_DEL-04-03.md` and SCA002 `RV_DEL-04-02.md`, the OWNER_ITEMS entries
O-4, O-10, O-14, O-15, O-25 and Q-5, Q-11, Q-15, ARC_ANALYSIS §2.2 and §3,
and `loop/LOOP_INIT.md`
"Develop the detail appropriate to the phase". V11–V16 and R1–R7 were searched
for the three files and deliverables, not read whole. Checks used: sha256
recomputation; `git show <commit>:<path> | shasum` for historical pins;
`git diff 6e18505e3 HEAD -- docs/` for the amended requirement texts; a
whitespace-normalised string comparison for quoted requirement text; scripted
lookup of every sibling section number and identifier the three files cite;
DAG-003 `DependencyEdges.csv`, `CandidateEdges.csv` and `ExcludedRows.csv`
parsed for the arcs. Line numbers are lines of the current files.

**Counting rule for "stale pin".** A pin is counted stale when (a) a byte hash
no longer equals the current file and the header gives no later pin for that
file (this includes the EXEC-v0.4, WD-v0.6 and WD-EX-v0.6 hashes, which are
true for `94aa9181b` but are the only byte pins given for versions that are
still current), (b) a basis commit no longer holds the current cited text,
(c) a quoted or characterised requirement text no longer matches the amended
text, or (d) a register or SoW reference no longer matches the current
register or SoW. Pins of superseded versions, and earlier states of a file
for which the header also gives a later, current pin, are true history and
are not counted.

---

# 1. DEL-04-01 — `ACT_AND_POLICY_CONTRACT.md` (ACT-POLICY-v0.6)

## 1.1 Pins

Stale (10):

| # | Pin (line) | Check | File value | Current value |
|---|---|---|---|---|
| A-P1 | Basis "Repo 6e18505e3" for PRD, HOST_INTEGRATION, EXAMINATION (l.8–11; repeated l.509 "checked against the cited bytes at repo 6e18505e3") | `git diff 6e18505e3 HEAD -- docs/` | commit `6e18505e3` | Docs amended by SCA-V4-001 (and a line break by SCA-V4-002). PRD `bb6e786f7a6c…49bd`; HOST_INTEGRATION `d4331c39db7f…8d9f`; EXAMINATION `471798bc2f2d…57d0`. Changed IDs cited here: V4-WF-05, V4-HI-42, V4-HI-70, V4-EXM-22 |
| A-P2 | `ScopeOfWork.md` sha256 `fc1a0503…f5e6` (l.8) | recomputed; `git show ddd721a90a` | the INIT contract | `ac043e54e396f9155e3d1b02d61ca7333350a812c7db3d5bb26c80d6fc3bb875` (SCA-V4-001, commit `340ecf341f`; unchanged by SCA-V4-002) |
| A-P3 | V4-WF-05 characterised by halves and "flagged for the next accepted-basis update" (l.4, 100, 593, 601, 1381, 1609) | text compare with `docs/PRD.md` l.254–264 | see quotes below | basis already amended |
| A-P4 | V4-HI-42 as "Declared checkpoints override autonomy" and as "guidance in Phase 1" (l.109, 521, 548, 598, 749, 1323–1327) | text compare with `docs/HOST_INTEGRATION.md` l.139–144 | see quotes below | amended |
| A-P5 | `RELAY_ANSWERS_SWBPIPE.md` sha256 `6f01add3…61c7` (l.23) and "unchanged" (l.17) | recomputed | true at `94aa9181b` and `f5ceef164a` | `afb6e063e7e5dfccf8986206f888cf1e2e1c4e7fc3430fdf86db670714fc0e74` (SWBPIPE revision `a999f4ba16`, reached this branch in merge `01cb95adba`). V9 Check 2 found no answer the App relies on changed; GUIDE was re-pinned, the three PKG-04 headers were not |
| A-P6 | EXEC-v0.4 sha256 `d32be377…76d4` (l.22) | recomputed; `git show 94aa9181b` | true at `94aa9181b` | `092f248682447df74e93915527930f4b90367fac46b867dad18daef3c5c608ff` (version label unchanged) |
| A-P7 | WD-v0.6 sha256 `fce565ed…2f28` (l.22) | same | true at `94aa9181b` | `43a9962f025de384e1cdaedea9a648da74e20216476a04f2394cfa3851f47eb9` |
| A-P8 | WD-EX-v0.6 sha256 `950b70b2…ba3d` (l.22) | same | true at `94aa9181b` | `8d60ed7850e6935b8410217c8867c59554c7de9aec28c60514e88ff5f0cff36e` |
| A-P9 | Intake `BRIEFS.md` sha256 `3e33ba26…7517` (l.16, 21) | recomputed; `git diff 3733b14218 HEAD` | true through `3733b14218` | `6f32809d58d150d684baa5185c7bd54fe82da5f7173b34eddd2f4ab90cfc03b4`. The only change is an added "B1" section; "Common rules" and "A-wave" are unchanged |
| A-P10 | Receivers: "From `Dependencies.csv` DEP-04-01-012…016" and six consumers "declared upstream in the receivers' own registers" (l.60–67) | register read | five local rows | the register now has eleven DOWNSTREAM rows: 012–016 and 022–027 (added 2026-09-29) |

Stale requirement text, file against current:

- **V4-WF-05.** ACT l.601 (AP-11): "Its first half ("holds … the run waits")
  is **phased to the governance layer, not withdrawn**. Its second half is in
  force (AP-3). Flagged for the next accepted-basis update (EXEC PH-10)".
  Current PRD l.254–264: "When a run reaches a workflow's declared checkpoint,
  the required human act is requested, and the run does not record the act as
  done until the person performs it. Holding the checkpoint — the run waits
  until the act is performed — is **phased to the governance layer**, not
  withdrawn (DEC-4): in the current phase, declared checkpoints are plan
  guidance that the person and the agents manage, and neither the App nor a
  host's embedded loop enforces a hold, blocks a run, or reports a workflow
  unsupported because a hold cannot be enforced. Enforced holds are applied
  later to the workflows that need them; the declared checkpoint and the
  definitions that enforcement needs are kept so that every such workflow can
  be served. Reserved human acts (§4.5) are unaffected." The amended text has
  no "first half / second half"; what ACT calls the second half is now the
  first sentence.
- **V4-HI-42.** ACT l.521 (S9): "Declared checkpoints override autonomy."
  ACT l.598 (AP-8): "D2's "or a declared checkpoint", WD I-7 … and V4-HI-42
  are **guidance** in Phase 1". Current HOST_INTEGRATION l.139–144: "Autonomy
  does not override a workflow's declared checkpoints: whatever the autonomy
  setting, a checkpoint's required act is requested and recorded as done only
  when the person performs it. Holding the run at the checkpoint until then is
  phased to the governance layer (V4-WF-05): in the current phase a checkpoint
  is plan guidance that the person and the agents manage, and the reserved
  acts (V4-HI-30) still bind."

Current or true as stated:

| Pin | Check | Result |
|---|---|---|
| v0.5 sha256 `0057593a…3bd9` at `c6f81a4f2`/`94aa9181b`; v0.4 `d6da05ab…` at `8fb51f07f` (l.2) | `git show` | true |
| `DECISION_BRIEF.html` `02d38cb1…20e8` (l.12) | recomputed | current |
| First-run `OWNER_DECISIONS.md` `a9869129…ad2c` (l.38); `f3f8e5f3…1f2e` "as then committed" at `28bd00499` (l.49) | recomputed; `git show` | first is current; second is true history |
| R1 `2f9c7e72…`, R2 `77cfb845…`, R3 `202d52c7…`, R4 `50a009b2…`, R5 `254d0b93…`; V2 `75ba1dff…`, V3-A `f25f5af1…`, V3-B `5662fbd0…`, IR1-A `31b3c7f8…` | recomputed | all current |
| Intake `OWNER_DECISIONS.md` `5fd780bf…0b2` (l.16) | recomputed; `git show` at `1528a5033`, `3733b14218`, HEAD | current. At `1528a5033` the file was `9903bfe0…`; `5fd780bf…` is the state from `3733b14218`. The sentence can be read as placing the hash at `1528a5033` (V10 N-1, still open) |
| Intake `OWNER_DECISIONS.md` `a5ccab0d…e776` at `94aa9181b` (l.15) | `git show` | true history |
| `R8_RESOLUTIONS.md` `1770c96e…` at `94aa9181b`, `d4c34233…` at `7a1508452`, `44bc9a8d…` at `1528a5033` (l.16–19) | `git show`; recomputed | all true; the last is current |
| `INTAKE_MAP.md` `3cc18295…ea33` | recomputed | current |
| Sibling v0.2–v0.5 byte pins at `28bd00499`, `f05c7e4cd`, `8fb51f07f`, `d3cebd1cc` (l.29–57) | `git show` for C, EXEC, ADAPTER, WD at each | all true history |
| Sibling version labels (EXEC-v0.4, WD-v0.6, WD-EX-v0.6, C-v0.6, P-v0.6, ADAPTER-v0.4, GUIDE-v0.3, AS-v0.6, RS-v0.6, LOOP-v0.6, PANEL-v0.6, HOSTING-BOUNDARY-v0.6, PIN-SPIKE-v0.1, CA-v0.4, XT-v0.4, RELAY-v0.3) (l.17) | header of each file | all current labels |
| Policy revision identity "ACT-POLICY-v0.6" (§8.1, l.1220) | read | current (C1-A's "still says v0.3" residual is fixed) |
| Serves "OUT-001…003; REQ-001…007; VER-001…009 (AC-001…009)" (l.6) | SoW read | IDs exist; the new TBD-004 and AX-005 are not cited anywhere in ACT |
| Every cited sibling section (P §3.3, §9; C §2, §3.1, §10–§10.4; DEL-03-01 §4.1, §5.3; EXEC §2.1, §2.2, §3.6, §4, §4.7, §4.9–§4.12, §4.14; WD §4.3–§4.3.7; LOOP §2.4.4, §5.1.1, §5.2, §6.2; HOSTING §2, §6; ADAPTER §5.1) and 105 cited identifiers (PH-n, GV-n, HS-n, CG-n, FB-n, NW-n, FXA-n, V-GR1 …) | scripted heading and token lookup | every one resolves in the current sibling file. This shows the anchor exists, not that the meaning matches |
| Unchanged cited requirement lines: V4-AUT-01…05, V4-REC-05, V4-EXE-01/02, V4-HI-02, -30…33, -40, -41, -52, -71, V4-EXM-20, -21, -25, -31 | first line at `6e18505e3` against HEAD | identical |

Not counted, but lagging: F-16 (l.1608) says D6 "affects … V4-EXM-22 in App
runs". Amended V4-EXM-22 now reads "stopping the run at the checkpoint is
examined only for a workflow that takes up the governance phase". F-16's R8
disposition already says the same; the citation needs the amended wording.

## 1.2 ScopeOfWork alignment (SoW `ac043e54…`)

| SoW item | Where ACT answers | State |
|---|---|---|
| CLM-001 (artifacts: document, adopted policy-class configuration, fixtures) | whole file; §8; §13 | document developed; configuration only as element meaning (§8.1); fixtures designed |
| CLM-002 (supplies policy meaning to DEL-02-01, 02-03, 03-01, 04-02, 04-03 and, since SCA-V4-001, to DEL-03-02, 03-03, 03-04, 05-01, 05-02, 09-09) | §10.1 consumer column; header l.59–70; §10.3 | **lags**: l.60 still names five register rows; DEL-03-04 sits in §10.3 "not mapped in detail" (l.1404) and has no V-row; DEL-09-06 (admitted consumer, DEP-09-06-030) is named nowhere as a consumer |
| CLM-003, CLM-005 | §11 | developed |
| CLM-004 (OI-001/002 ruled by DECISION-1; OI-021 remainder; Open_Issues updated through its own route) | §3 adopted rulings; §8.2; U-01 | developed. **F-8 and F-10 lag** (below) |
| OUT-001 contract | §1–§7, §9, §11 | developed |
| OUT-002 policy-class representation and decision→consumer map | §8.1–§8.4, §10 | **partial**: element meanings and six records P-01…P-06 exist; no concrete representation ("the method is unselected", l.1220; "selects none of … field names or types", l.77–82); consequence dimension open (U-02); placement open (U-12) |
| OUT-003 fixtures with candidate-bound results | §13 FX-01…FX-55; VC-001…VC-011 | designed only; "No results at v0.6" (VC-009) |
| REQ-001 | §4, §5.3–§5.6 | developed; the consequence part is only named (U-02) |
| REQ-002 | §2.1–§2.6; §3 | developed |
| REQ-003 | §3 S4; §9; FX-03, -05, -14, -15 | developed |
| REQ-004 | §8.3, §8.4, §5.3 rule 5 | developed; OI-021 additions held |
| REQ-005 | §9; FX-11…13, FX-34 | developed |
| REQ-006 | §7; §5.6; P-03 | developed |
| REQ-007 | §11 | developed |
| AC-001…AC-009 / VER-001…VER-009 | VC-001…VC-011 | designed. VER-004's new first clause ("Compare adopted reserved-act cases with … D2 and its DERIVED extensions") is met by VC-004. VER-007's new wording is met by VC-007 |
| AX-001…AX-004 | §3 "Historical, not ruled"; §11 | developed |
| TBD-001, TBD-002 (ruled) | §3; P-01, P-04 | developed |
| TBD-003 (DEP-001) | U-04; §11 | named, host |
| **TBD-004** (new: phased checkpoints; "limits the VER-001 and VER-006 checkpoint cases to recording in the current phase") | §4.0 AP-1…AP-11; VC-001, VC-010 | developed in substance, but TBD-004 is not cited, and **VC-006 (l.1664) is not split by phase**: its expected result "Only host-held constraint carriage satisfies R2-12" is a governance-phase statement with no Phase-1 part |

Places where the Design text contradicts or lags the revised SoW:

1. **F-10 (l.1601)** says "TBD-001/002, AC-004 and VER-004 still read
   OI-001/OI-002 as open. Goes to C1." The SoW was revised (RV-1_DEL-04-01,
   E-0401-05, -08, -09). The finding is closed in fact and open in the text.
2. **F-8 (l.1599)** says Open_Issues still shows OI-001/002 open and routes
   it to C1. The owner decided at SCA-V4-002 DECISION-2 (Q-5, option A) that
   the status stays OPEN with a pointer to DECISION-1. It is settled, not a
   pending reconciliation. §8.2's "Not established … `Open_Issues.csv`
   rewrite (C1)" (l.1250) carries the same stale pointer.
3. **F-1 (l.1593)** "Five downstream rows against eighteen upstream-declared
   consumers" is now eleven rows; the remaining unmirrored consumers are
   DEL-09-06 and the eight outside the 14.
4. **AC-007** says OUT-002 "supplies no reserved list or classifier treatment
   beyond the adopted `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` rulings".
   ACT §2.7 makes a network-destination grant a person-only A12 subclass on
   DECISION-5 plus an INTEGRATION mapping (R8-13). The DEL-04-01 SoW does not
   name DECISION-5 (AX-005 lists DECISION-1, DECISION-2 and DECISION-4 only).
   OWNER_ITEMS O-15 (accepted at DECISION-7) says: "No other SoW change for
   DEL-04-01 … now. … Revisit when the A12 mapping is confirmed or at
   implementation." Inference: §2.7 has no SoW anchor in its own deliverable,
   and sits only under VER-007's "labeled DERIVED/INTEGRATION extensions".
   This is an owner-level item (§1.4, F-22), not something a Design edit
   settles.
5. **VC-009 (l.1667)** reconciles "FX-01…54"; FX-55 exists (l.1587).

## 1.3 Amended basis

| Item | ACT text | Agreement |
|---|---|---|
| V4-WF-05 | l.4, 100, 521, 593 (AP-3 "V4-WF-05 second half"), 601 (AP-11), 1381 (V-09 "first half phased"), 1609 (F-20) | Intent agrees. Wording lags: halves, the `("holds … the run waits")` quote, and four "flagged for the next accepted-basis update" markers. F-20's "No accepted text is changed here" is now overtaken: the accepted text was changed by SCA-V4-001 |
| V4-HI-42 | S9 (l.521); §3 Phase-1 reading (l.545–550); AP-8 (l.598); §4.4 heading "DERIVED from V4-HI-42 + D2b" and its Phase-1 paragraph (l.749–763); §5.3 rule 2 (l.1012–1019); W-b (l.1112); P-05 (l.1319–1327) | **Wording lag of substance.** ACT treats V4-HI-42 as a whole as "guidance in Phase 1". The amended text itself separates what binds now ("whatever the autonomy setting, a checkpoint's required act is requested and recorded as done only when the person performs it"; "the reserved acts (V4-HI-30) still bind") from what is phased (holding the run). ACT has the binding part under AP-3 and AP-4 but does not attribute it to V4-HI-42. The owner confirmed the R8-11 item 2 reading (OWNER_ITEMS O-25, DECISION-7), so this is a re-quote, not a re-ruling |
| "is requested" (V4-WF-05 sentence 1; V4-HI-42; V4-EXM-22 "A workflow checkpoint requests a human act") | AP-1 "the agents manage any pause, hold point or gate themselves"; §4.3 "The agent re-requests the act as its plan requires" (l.707); §5.3 rule 2 "plan guidance for the agent" (l.1015); §6 row 7 "An A8 exists only if the agent actually issues it" | **Gap (my inference).** No ACT sentence says that at a Phase-1 arrival the required act is requested, or by whom. The amended texts state the request without a phase qualifier. R8-1's "in force in Phase 1" list names the recording rule, not the request. The rule belongs with EXEC PH-1…PH-10 (DEL-02-03); those ten rows (EXEC l.216–225) do not contain the word "request". ACT's §5.2 "request the person's act" treatment is the policy side |
| V4-HOST-01, V4-ARC-11, V4-ARC-12 | not cited | not touched. §2.7 "Outside this act: the selected model service and its sign-in service, allowed by the person's model choice" agrees with the amended ARCHITECTURE host-agent properties |
| V4-HOST-02 | l.16 and l.113 only (consumed input and change row) | ACT does not quote it. §2.7's forms, scopes, decline wording, always-off items and the stateless-MCP rule agree with amended PRD V4-HOST-02 and the ARCHITECTURE §4 property list. §2.7 credits DECISION-5; it can now also cite the accepted PRD text |
| V4-HI-70 | basis line only (l.10) | not used beyond V4-HI-71 "linked and not copied" |
| V4-EXM-22 | l.11, 1077, 1608 | l.1077 is unaffected. F-16 see §1.1 |
| V4-EXM-23 | not cited | VC-011 and FX-55 cover the same behaviour ("destination not allowed by the person"; agent-written entry is no act) but do not trace to V4-EXM-23 |
| "local-first" | no occurrence (grep: 0) | not touched. l.254 "Off by default and local" is about external access (V4-HI-52), unchanged |

## 1.4 Open items

Owner and point of need are as the file states them. Classes are mine.

| ID | What is open | Owner / point of need (file) | Class |
|---|---|---|---|
| U-01 (= §12.1, §8.4, V-20/V-22; FX-16, FX-17 held) | First connected operation, its reserved additions and autonomy (OI-021) | Owner via the outside SWB session and App/shared owner / before the connected-activity SoW | **OWNER** — which operation, and its policy. Bound to the deferred host joins (SQ-04: no selection); not for this pass |
| U-02 (= §12.3, F-4, V-23; FX-20 OP-C5 held) | Consequence vocabulary | DEL-04-01 with the host policy owner / before class assignment in DEL-03-01 | **OWNER** — the value set. A PROPOSED App/shared vocabulary can be drafted now from `DECISION_BRIEF.html#d3`, which names four dimensions (consequences, reversibility, available examination, intended delegation) and no values |
| U-03 (= §12.2, V-24) | Multi-row A4 purpose after partial lapse | DEL-04-01 with the owner / at its point of need | **OWNER** — does the act still stand for the unchanged rows |
| U-04 (a)–(f) (= §12.4; FX-29, FX-47(c) AWAITING INPUT; F-15; F-21) | Host capture reference, faithful-record operation, constraint reception, adoption of P-01…P-06, A13 facility, host-held route. All answered "none offered" | SWBPIPE owner decisions / when UI-SUCCESSOR resumes | **HOST** |
| U-05 | Recorded person grant; performed-act evidence (DEP-04-01-020, -021) | the person / VER-001 and VER-002 positive cases | **LATER** — needs a candidate and a real act |
| U-06 (V-23) | Defaults for other consequential classes | SWBPIPE OI-016; host policy owner / before those classes are cataloged | **HOST** |
| U-08 (= §12.6) | Workflow registration as a canonical act | DEL-04-01 with DEL-02-02 / before the DEL-02-02 definition | **LATER** — DEL-02-02 is outside the 14 (unless S1-F's advice brings it in) |
| U-12 | Placement of the policy representation (OI-013, OI-014) | App/shared owners / before production allocation | **OWNER** — where the policy-class records live and who owns the shared part |
| U-D6 (= §12.5, V-26, F-16) | App-side run holds | the owner / when the governance phase is taken up | **LATER** |
| U-14 (= §12.5, V-27, F-17; FX-45, FX-51) | Capture-after-arrival (SP-6) against counting a prior act bound to current content | Owner / before hold-machine fixtures run | **OWNER** — the rule also sets the *performed* record label in the current phase |
| U-15 | Per-subject identity (V4-HI-32) not met by SWBPIPE | SWBPIPE; owner notice / before host act-binding integration | **HOST** |
| U-16 (= §12.7) | Launch environment variable as A13 evidence | the owner (deferred) / when UI-SUCCESSOR resumes | **OWNER**, deferred with the host joins |
| U-17 | CLOSED in the file | — | — |
| F-1 | Register asymmetry | "Goes to C1" | **NOW** — current `Dependencies.csv` rows 012–016, 022–027 |
| F-2 | Design-candidate approval has no canonical name | Domains increment | **LATER** |
| F-6 | D2(b) does not address a voluntary proposal under a direct grant | none stated | **NOW** — no decision needed; S3 already makes every A5 the person's act. Keep as a note |
| F-8 | Open_Issues OI-001/002 still OPEN | "Goes to C1" | **NOW** — SCA002 `OWNER_DECISIONS.md` DECISION-2 (Q-5 option A) |
| F-10 | SoW wording predates DECISION-1 | "Goes to C1" | **NOW** — SoW `ac043e54…`; RV-1_DEL-04-01 |
| F-11 | A13 *disabling* reserved is INTEGRATION; "the owner may wish to confirm" | the owner | **OWNER** — confirm or drop |
| F-14 | Rules carried at PROPOSED standing: no resumption (§2.3, R4-4), A12/A13 setting-content binding and supersession (§2.5), the §2.6 A13 capture ruling (R4-13), the mixed-item rule (§4.3), capture after arrival (§4.5), the `governed` flag (AP-10, WD) | EXEC / WD / DEL-04-01; "open to review" | **OWNER** at the phase review (no separate prompt). R4-3 (resume point, re-hold) is "adopted everywhere" by R4 and can be relabelled now |
| F-18 | Consumers must drop "A8 names the setting" (WD, LOOP, PANEL, EXEC) | consumers | **NOW** — WD l.914/922 and EXEC l.1196 name the R5-3 rule; LOOP and PANEL are for S1-D to confirm |
| F-19 | RS should carry the human-act reference in R7 | DEL-04-03 | **NOW** — RS §3 (l.151) and §5 (l.251) carry it |
| F-20 | S9, D2's checkpoint half and V4-WF-05 flagged for the basis update | next accepted-basis update | **NOW** — done by SCA-V4-001 |
| F-22 | A12 mapping of the destination grant is INTEGRATION; "the owner may revisit it at any time" | the owner | **OWNER** — confirm the mapping; O-15 deferred it |
| INTEGRATION labels since confirmed | "INTEGRATION (DECISION-2 reading)" for recording and showing the model destination (l.38, 122, 1382); "Phase-1 reading (R8-11 item 2; INTEGRATION)" (l.545) | — | **NOW** — BASIS-ALIGN `OWNER_DECISIONS.md` DECISION-7 accepts O-10 and O-25 |
| §2.6 "Still open" (l.460) | A13 for an App-owned external interface | none in this increment | **LATER** |
| §2.1 (l.262–266) | Stopping work and reserved coordination decisions have no canonical name | none stated | **LATER** |
| ND-A4 (l.499) | Organization-locked allow lists | governance phase | **LATER** |
| VC-001…VC-011 | "designed, not run" | — | **LATER** |

Counts: NOW 8 · OWNER 9 (1 at the phase review, 2 deferred with the host
joins) · HOST 3 · SPIKE 0 · LATER 8. U-17 is closed and not counted.

## 1.5 Design depth against the 60% description

Contributions exchanged: act names and record meaning (V-01, V-13 → RS, WD,
AS, LOOP, PANEL); class vocabulary and policy-class records (V-02, V-11, V-14,
V-21 → C, P, LOOP, ADAPTER, HOSTING); resolution order and outcome map (V-03,
V-05 → P, LOOP, EXEC, AS, ADAPTER); grant model (V-04 → AS, RS, LOOP, P);
checkpoint act-policy meaning (V-09 → WD, EXEC, LOOP, PANEL, P, ADAPTER);
binding, lapse, supersession (V-06 → RS, C, P, AS, PANEL, WD); external access
and A13 (V-10 → ADAPTER, XT, RS); network-destination grant (§2.7 → LOOP,
PANEL, AS, RS).

| Aspect | What ACT has | What is missing |
|---|---|---|
| Interfaces | §10.1 value→basis→consumer map; §5.1 inputs with suppliers; §6 treatment→outcome map; §11 boundary table | No statement per consumer of the condition of use or of what the consumer does when a value is missing or held. §10.2 lists "consumers that must hold" but not the held part of each consumer. §2.7 has no V-row in §10.1, so its four consumers are not in the map. DEL-03-04 and DEL-09-06 are unmapped |
| States | Seven grant states (§5.1, §5.4); four A12 control relations (§2.5 table); six dispositions (§4.3); act-declined and run-ended events (§2.3) | No lifecycle for an act record as one table (captured → bound → lapsed / superseded / after run end / not counted); it is spread over §2.3, §2.5, §4.3, §4.5. The network-destination grant has scopes (ND-A2) but no state list of its own (AS says the seven states apply) |
| Data | Element meanings: §2.4 recorded act (7 elements); §8.1 policy-class record (13 elements); §2.7 grant (9 rows) | **No representation of the OUT-002 "adopted policy-class configuration"**: no structure, no identity method for the policy revision identity ("plus its content identity; the method is unselected"), no worked instance of P-01…P-06 as data, no rule for how a catalog entry refers to a record. Consequence dimension empty (U-02) |
| Operating sequences | §5.3 resolution order (8 rules); §5.5 changes during work; §7 walk-through T3–T12; §4.3 lapse order | No sequence for the central path request (A8) → person's act at the capturing surface → capture evidence → record → checkpoint label. No sequence for an in-work destination grant (LOOP §5.1.1 has it; ACT gives forms only). No Phase-1 statement of the request at arrival (§1.3) |
| Failure behaviour | §6 rows 1–11; A12 refused, pending, confirmation lost (§2.5); *unknown* disposition; "act order unknown"; received host terms | Not defined: a consumer citing a superseded policy revision; an unresolvable capture-evidence reference at read time (RS §9 has resolution status; ACT does not say what a checkpoint label becomes); two surfaces reporting different grant states (AS §5 has it; ACT is silent) |
| Verification | 55 fixtures, 11 cases, each mapped to VER IDs; held and AWAITING INPUT kept apart from passes | Nothing executable and no fixture artifact. No Phase-1 part in VC-006. No trace to V4-EXM-23. VC-009 range stale |

Structural choices still open that could force restructuring:

- **Representation and placement of policy-class records (U-12; OI-014).**
  C element 8, P, LOOP and RS cite "policy-class record reference and policy
  revision identity". Whether records live in an App/shared file, in the
  catalog, or host-side changes how every consumer resolves that reference.
- **U-02.** A consequence dimension adds an axis to the class record, the
  grant scope and the catalog element.
- **U-14.** The owner alternative changes §4.5, FX-45, FX-51, RS L-13, AS §4
  and EXEC SP-6.
- **F-22.** If the owner gives destination grants their own act kind, §2.1,
  §2.7, AS §3, RS R9/R15, LOOP §9 and PANEL §3.8 change.
- **Who requests the act at a Phase-1 arrival**, and whether the request is
  recorded (§1.3; RS has no element for it, §3.5).

## 1.6 Joins

All eleven local rows are DOWNSTREAM HANDOVER, RequiredMaturity INITIALIZED,
SatisfactionStatus TBD. DAG-003 lists each as MIRROR of the consumer's row;
every arc is **admitted**. DEL-04-01 has no supplier row.

| Local row | Consumer (representative row) | Contribution | Supplier side (ACT) | Consumer side uses it at | Disagreement |
|---|---|---|---|---|---|
| DEP-04-01-012 | DEL-02-01 (DEP-02-01-018) | act names; closed list; decision pairs; act-declined; A12 binding and referent; reserved-operation rule | §2.1, §4.1, §2.3, §2.5, §4.2, P-02 | WD l.914, 922 (used in WD §4.3); cites ACT §2.1, §4.1, U-03 | WD records "ACT-POLICY-v0.5 at `d3cebd1cc` (header checked …). Current: ACT-POLICY-v0.6": WD's read basis is v0.5 |
| DEP-04-01-013 | DEL-02-03 (DEP-02-03-012, CONSTRAINT) | A1–A14; closed list; act-declined; A12 binding and supersession; grant-setting subject; A13 locus; person's own operations; U-03 ruling | §2.1, §2.3–§2.6, §4.1, §4.2; U-03 open | EXEC l.1196 (used in EXEC §4.5, §4.7, §4.10, §5) | EXEC records "ACT-v0.4 read. Current: ACT-POLICY-v0.6". "U-03 ruling (pending)" is still pending |
| DEP-04-01-014 | DEL-03-01 (DEP-03-01-024) | act names, class vocabulary and records, outcome map, "carried into §3 element 8" | §2.1, §8, §6 | C l.74; C cites ACT §8.1, §5.3, P-02, P-03, P-06, U-02, F-22 | none found |
| DEP-04-01-015 | DEL-04-02 (DEP-04-02-007) | grant model, records | §5, §8 | AS §2 "Received from DEL-04-01 §5 and §8" (l.118) | none found |
| DEP-04-01-016 | DEL-04-03 (DEP-04-03-021) | act kinds and classes | §2.1, §2.4, §8.1, §2.7 | RS §0, §3 (l.151), §6.1 (l.315–317), R15 | none found |
| DEP-04-01-022 | DEL-03-02 (DEP-03-02-017) | A1–A14; P-01…P-06 with revision identity; outcome map; act-declined; OI-021 residue | §2.1, §8.1, §8.3, §6, §2.3, U-01 | P §13 l.700 | none found |
| DEP-04-01-023 | DEL-03-03 (DEP-03-03-008) | A1–A14; P-01…P-06; §5.3; §6; V-10; A13 subject | same sections; §2.6 | ADAPTER §11 l.1054; §2.6 cited 12 times | RequiredMaturity differs: DEP-03-03-008 TBD, DEP-04-01-023 INITIALIZED (HANDOFF open matter) |
| DEP-04-01-024 | DEL-03-04 (DEP-03-04-011) | policy meaning for the guide | §2.6, §2.7, §4.0, §5, §8.3 | GUIDE pins ACT bytes (l.21) and cites ACT §2.6 ×9, §2.7 ×5, §8.3 ×4, §4.0 ×4 | ACT §10.3 lists DEL-03-04 as "not mapped in detail" |
| DEP-04-01-025 | DEL-05-01 (DEP-05-01-018) | act names; decline; treatment map; reserved operations; §2.7 | §2.1, §2.3, §5.3, §6, §2.7 | LOOP l.1341, 1367; cites ACT §2.7 ×7 | none found |
| DEP-04-01-026 | DEL-05-02 (DEP-05-02-008) | act names, labels, record meaning, §2.7 | §2.1, §2.4, §9, §2.7 | PANEL VC-01 (l.875); cites ACT §2.7 ×5 | none found |
| DEP-04-01-027 | DEL-09-09 (DEP-09-09-010) | adopted policy and act distinctions | §3, §2.6, §4.6 | XT IN-07 (l.88) | none found |

No local row: DEL-09-06 → DEL-04-01 (N-28, DEP-09-06-030, admitted; CA l.540
"Cited at `8fb51f07f` (v0.4) … Current: … ACT-POLICY-v0.6"), and the eight
admitted consumers outside the 14 (DEL-01-02, 01-04, 02-02, 06-02, 09-02,
09-05, 09-12, 10-03).

N-18, N-21, N-24 and X-1 have no end at DEL-04-01. X-1's contribution
(DEL-01-04's App act control and person identity) is assumed by ACT §2.6
(l.428: "The control is built by DEL-01-04 in a later undertaking").

## 1.7 Carried review items that name ACT

| Item | State | Evidence |
|---|---|---|
| V6 m-1, m-3…m-7 | none names ACT as the side to change. V6 lists ACT §4.3, §4.6 and FX-39 as "holds" | V6 §7 table. If m-7 (the held-actions partition hole) is fixed in WD/EXEC, ACT §4.6 HS list (l.868–891) must echo it |
| C1-A residual: §8.1 "This revision is … v0.3" | fixed | l.1220 reads v0.6 |
| C1-A SC-04-01-1…-10 | applied to the SoW by SCA-V4-001; SC-04-01-10 amended into TBD-004 | RV-1_DEL-04-01 |
| C1-A register rows R-04-01-a…-f, -h, -i | present as DEP-04-01-022…029 | register |
| C1-A R-04-01-g (DOWNSTREAM to DEL-09-06) | not added; the arc is carried by DEP-09-06-030 | register |
| V9 N-3, N-7 | do not name ACT | V9 residual table |
| V10 S-1, S-3, S-4 | fixed | l.469 ("not objected to and stands"); l.480 ("a silent switch"); l.1614 (F-22) |
| V10 N-1 (hash sentence readable as "at `1528a5033`") | **open** | l.16 unchanged |
| V10 N-5 (ND-A2 cites PROPOSED R4-4 under a SETTLED heading) | open; V10 asked for no change | l.491–496 |
| V11–V16 | no finding names ACT | grep |
| HANDOFF "17 Design re-pins" | **open**; this pass | §1.1 |

## 1.8 Recommended work on ACT in this pass

1. Re-pin the header to the amended basis (three doc hashes), SoW
   `ac043e54…`, ANS `afb6e063…`, and current sibling bytes (or GUIDE's table
   only). Rebuild the Receivers line from rows 012–016 and 022–027. Cite
   SCA-V4-001 and TBD-004. [§1.1, §1.2]
2. Re-quote V4-WF-05 and V4-HI-42 everywhere listed in §1.1 and §1.3. State
   which part of V4-HI-42 binds now and which is phased. Remove the four
   "flagged" markers. [§1.1, §1.3]
3. Settle, with DEL-02-03's file, the sentence on the request at a Phase-1
   arrival. [§1.3, §1.5]
4. Close F-10, F-19 and F-20; rewrite F-1 and F-8; relabel the two
   owner-confirmed INTEGRATION readings (O-10, O-25). [§1.2, §1.4]
5. §10: add a V-row for §2.7, map DEL-03-04, add DEL-09-06. [§1.2, §1.5, §1.6]
6. VC-006 in two parts; VC-009 range to FX-55; trace VC-011 to V4-EXM-23.
   [§1.2, §1.3]
7. Develop OUT-002: a PROPOSED structure for the policy-class record with
   P-01…P-06 written as instances; one act-record lifecycle table; the
   request→capture→record sequence. [§1.5]
8. Draft a PROPOSED consequence vocabulary from d3's four dimensions, for the
   owner. [§1.4 U-02, §1.5]

Not in this pass: OI-021 and every host row (joins deferred); D6 and any
governance-phase development; a SoW sentence for DECISION-5 (SoWs are not
written in this run); deciding U-03, U-14, F-11 or F-22 (owner); running
fixtures (no candidate).

---

# 2. DEL-04-02 — `AUTONOMY_AND_STANDING_EXCHANGE.md` (AS-v0.6)

## 2.1 Pins

Stale (11):

| # | Pin (line) | File value | Current value |
|---|---|---|---|
| S-P1 | "repo 6e18505e3 (accepted basis)" for PRD, HOST_INTEGRATION, ARCHITECTURE §4, EXAMINATION (l.7) | `6e18505e3` | all four amended; ARCHITECTURE `317d5789272c…828c`; §4 now carries the revised V4-ARC-11/12 and the host-agent property list. OPERATING_METHOD is unchanged (`98836b52…`) |
| S-P2 | `ScopeOfWork.md` sha256 `23a28caa…5e21` (l.7) | the INIT contract | `f16ffa8a33cbfb2e78a8e916e90aff9fb44ad20adf94fe61a559a213f5564460` — two revisions later (SCA-V4-001 `e077f20a…` at `340ecf341f`; SCA-V4-002 at `1efd4bcdad`) |
| S-P3 | V4-WF-05 by halves and "flagged for the next accepted-basis update" (l.4, 25, 87, 248) | — | amended (quotes in §1.1) |
| S-P4 | V4-HI-42 at S3 (l.87): "Declared checkpoints override autonomy: the run waits for the person's act." | the pre-amendment sentence | "Autonomy does not override a workflow's declared checkpoints: …" (§1.1) |
| S-P5 | V4-HOST-02 "as revised by DECISION-5 (R8-13; flagged for the next accepted-basis update)" (S15 l.99; l.5, 36) | marker | the PRD now carries the text. The quotation in S15 equals the amended PRD text exactly (normalised compare) |
| S-P6 | ANS sha256 `6f01add3…` (l.10) and "unchanged" (l.9) | true at `94aa9181b` | `afb6e063…` |
| S-P7…S-P9 | EXEC `d32be377…`, WD `fce565ed…`, WD-EX `950b70b2…` (l.10) | true at `94aa9181b` | `092f2486…`, `43a9962f…`, `8d60ed78…` |
| S-P10 | Intake `BRIEFS.md` `3e33ba26…` (l.8, 10) | true through `3733b14218` | `6f32809d…` (B1 section added) |
| S-P11 | Receivers "register edges pending at C1" (l.12) and U-15 (l.582) | pending | DEP-04-02-019…023 are ACTIVE (2026-09-29) |

Current or true: AS-v0.5 `df0e31ea…` at `c6f81a4f2`/`94aa9181b` and AS-v0.4
`774728d0…` at `cc58211c5` (`git show`); first-run `OWNER_DECISIONS.md`
`a9869129…`; R1–R5, V2, V3-A, V3-B hashes (recomputed); intake
`OWNER_DECISIONS.md` `5fd780bf…` and `a5ccab0d…` (as ACT); R8 three hashes;
INTAKE_MAP; sibling v0.2–v0.5 byte pins including HOSTING-BOUNDARY-v0.4
`201ea320…` at `8fb51f07f`, C-v0.5 `a6306bd4…` and EXEC-v0.3 `889e4881…` at
`d3cebd1cc` (`git show`); sibling version labels; "§6 here and RS §8 are
byte-identical" (checked: the two bodies are 2744 characters each and equal);
every cited sibling section and identifier resolves (scripted). Serves line
(REQ-001…007, AC-001…007, VER-001…007) matches the SoW; TBD-006 and AX-004/005
are not cited. The Basis line does not name DECISION-4 or DECISION-5 although
§3 and §4 rest on them (they appear only under consumed inputs).

## 2.2 ScopeOfWork alignment (SoW `f16ffa8a…`)

| SoW item | Where AS answers | State |
|---|---|---|
| CLM-001 (components where justified; host contract; fixtures) | §0, §7, §11; U-08 | contract developed; components absent as design |
| CLM-002 consumes DEL-04-01 policy | §2 | developed |
| CLM-002 consumes DEL-04-03 record | §6, §8 | developed |
| CLM-002 consumes DEL-03-02 proposal/outcome and origin semantics | §7 origin row; §8 route-and-outcome facet | developed |
| CLM-002 consumes DEL-03-01 read-basis and standing facets | §8 temporal and host-check facets | developed |
| CLM-002 consumes DEL-02-03 checkpoint recording annotations | §4 OV-1…OV-7 and bullets | developed |
| CLM-002 "visible autonomy state is received by DEL-05-01, DEL-05-02, DEL-03-02, DEL-03-03 and DEL-02-03" | header l.12 only | **only named**: one clause per receiver; no section states what each receives, when, or on failure |
| CLM-002 consumes from DEL-05-01 "allow list, in-work destination grants and **contacted-destination record**, which … DECISION-5 requires to be shown" | §3 network table (l.211–233) | **partial**: allow list and in-work grants developed; the contacted-destination record is **absent** from AS. PANEL ND-4 (l.543) shows it; LOOP l.1335 assigns "AS §3 (display)" |
| CLM-003, CLM-005, CLM-006 | §7, §9, §8, §10 | developed |
| CLM-004 (revised by SCA-V4-002) | §10 l.520 | developed, with a stale parenthetical (below) |
| OUT-001 components (CODE) | behaviour in §3–§9 | **only named** as design: no component list, no allocation, no interaction structure ("OUT-001 components only 'where justified'", U-08) |
| OUT-002 contract (DOC) | §2, §6, §7, §10 | developed |
| OUT-003 fixtures (TEST) | §11 F1–F21; VC-01…VC-18 | designed only |
| REQ-001 | §3, §4, §5 | developed; "through the agreed control interface" is only named ("source of control (App or host)") |
| REQ-002 | §5, §6 | developed for operation-class grants; network-destination grants are outside the §6 field list |
| REQ-003 | §7 | developed |
| REQ-004 | §8 | developed |
| REQ-005 | §9 DS-1…DS-6 | developed |
| REQ-006 | §0; UNRESOLVED | developed |
| REQ-007 (revised: adds DEL-02-03 and DEL-03-03 ownership) | §10 rows l.517–518 | developed |
| AC-004 / VER-004 (revised: "host-checks-passed (each named check with its evaluated basis)") | §8 host-check facet; F9; VC-09 | developed |
| TBD-001…TBD-005 | §10; U-01, U-08, U-05 | developed |
| TBD-006 (new) | §4 OV-3; U-16 | developed; not cited. The SoW's point of need is "before hold-display fixtures run"; U-16 says "before App-side hold fixtures" |

Contradictions and lags:

1. **§10 l.520**: "(the SoW's TBD-001/002 still read OI-001/002 open — C1
   pointer)". The SoW was revised (RV-1_DEL-04-02 E-0402-05).
2. **U-15 and header l.12**: receivers "pending at C1"; they are registered.
3. **Contacted-destination record** (above): the SoW and DEP-04-02-018 name
   it; AS has no display for it.
4. **§6** has no element for a network-destination grant, an allow-list state
   or a contacted destination, while §3 calls these grants "the person's A12"
   and says the seven states apply to them. REQ-002's comparison of displayed
   against recorded settings therefore has no defined path for them. Whether
   they belong in the exchange is an open design choice, not stated in either
   file (my inference).
5. AS names no admitted consumer other than its five receivers. DAG-003
   admits DEL-03-04 → DEL-04-02 (DEP-03-04-012) and DEL-09-06 → DEL-04-02
   (N-08, DEP-09-06-031), and holds DEL-09-09 → DEL-04-02 (N-09).

## 2.3 Amended basis

| Item | AS text | Agreement |
|---|---|---|
| V4-WF-05 | l.4; S3 (l.87); OV-4 "V4-WF-05 second half" (l.248) | intent agrees; wording by halves and one "flagged" marker lag |
| V4-HI-42 | S3 (l.87) | quotes the superseded sentence. The phased annotation beside it is right; the settled sentence itself is not the current text |
| "is requested" | OV-1 shows a checkpoint "as the plan's expected pause"; no Phase-1 rule shows the request for the act | same gap as ACT §1.3; the request is shown only for grants ("Agent requests …") and, in the governance phase, as re-issued |
| V4-HOST-02 | S15 (l.99) quotes the revised text | exact match with amended PRD l.120–126. Marker "flagged for the next accepted-basis update" stale. "Every destination contacted is recorded and shown" is quoted but AS shows none (§2.2 item 3) |
| V4-HOST-01, V4-ARC-11 | not cited. §3 "Model service: Allowed by your model choice (the selected model service and, for a chosen cloud model, its sign-in service)" | agrees with "no default" and OAuth sign-in |
| V4-ARC-12 | not cited; Basis cites ARCHITECTURE §4 | §3's allow list, in-work scopes, always-off items and "organization-locked lists are governance phase" agree with the amended §4 property list |
| V4-HI-70 | basis line only | the amended clause (each network destination contacted) is not reflected in §6 record-out |
| V4-EXM-22 | basis line | F2, F6, F20 agree with "the act is recorded only when the person performs it, whatever the autonomy" |
| V4-EXM-23 | not cited | F21 and VC-18 do not trace to it |
| "local-first" | none | not touched |

## 2.4 Open items

| ID | What is open | Owner / point of need (file) | Class |
|---|---|---|---|
| U-01 (F3b held) | OI-021 additions and class assignments | Owner via outside SWB session and App/shared owner / before connected-activity SoW | **OWNER**, deferred (as ACT U-01) |
| U-02 (F2 OP-C5 held) | Consequence vocabulary (scope slot) | DEL-04-01 with host policy owner / before class assignment | **OWNER** (as ACT U-02) |
| U-04 | Host enforcement of *unconfirmed*, re-resolution, de-duplication | host owner / before connected integration | **HOST** |
| U-05 | Host origin, undo, later-check route, receipt, resulting objects, host-check basis | SWBPIPE outside session / before connected-journey integration | **HOST** |
| U-06 | Settings version in force at application | host owner | **HOST** |
| U-07 | Host capture requirement and reference | SWBPIPE owner decision / before host act-recording integration | **HOST** |
| U-08 | Component placement and host panel assembly (OI-014, OI-013) | App/shared contract owners; shared contract owner with SWB implementation owner / before allocation | **OWNER** — App-only component, shared component used by host panels, or a contract each host builds to |
| U-10 | Record representation for the exchange | DEL-04-03 (RS U-04) / before writer implementation | **SPIKE** — with RS U-04: serialise settings-in and record-out for F1, F2, F5 and run the §6 comparison |
| U-12 (F6b AWAITING INPUT) | Host receipt or evaluation of the checkpoint constraint (governance phase) | host owner / when UI-SUCCESSOR resumes | **HOST** |
| U-15 | Register edges to five receivers | register owner / closeout C1 | **NOW** — DEP-04-02-019…023 |
| U-16 | App-side run holds (D6) | the owner / when the governance phase is taken up | **LATER** |
| U-17 | SP-6 against counting a prior act; and the unapplied "re-affirm current setting" presentation (C1-A; EXEC F-23) | DEL-02-01 with DEL-04-01; Owner if preferred / before hold-machine fixtures run | **OWNER** (as ACT U-14) |
| U-18 | Caller identity verification over the external channel | App owner with host owner / before origin conformance | **HOST** |
| U-19 | Multi-row A4 purpose after partial lapse | DEL-04-01 with Owner | **OWNER** (as ACT U-03) |
| U-20 | Grant display for a host without a grant model (PROPOSED) | DEL-04-02 with the integrator / when the host joins resume | **HOST**, deferred |
| U-21 | LOOP N-OPEN-4: how a category switch and its named entries combine (the DECISION-5 points in the row are closed) | the owner; App/shared embedded-integration owner / before the §3 network display is implemented | **OWNER** — a named entry works with its category off, or needs it on |
| §10 l.520 parenthetical | stale statement that the SoW still reads OI-001/002 open | "C1 pointer" | **NOW** — SoW `f16ffa8a…`; RV-1_DEL-04-02 |
| S15 "flagged" and "INTEGRATION (DECISION-2 reading)" labels (l.99, 566) | stale standing labels | — | **NOW** — SCA-V4-001; DECISION-7 (O-10) |
| §3 network display "PROPOSED display over SETTLED rules"; OV-7 `governed`; "prior act not counted" PROPOSED | standing labels | "open to review" | **OWNER** at the phase review |
| VC-01…VC-18; "no component or fixture exists" (l.6) | nothing built or run | — | **LATER** |

Counts: NOW 3 · OWNER 7 (1 at the phase review, 1 deferred) · HOST 7 · SPIKE 1
· LATER 2.

## 2.5 Design depth against the 60% description

Contributions exchanged: grant display states (to DEL-05-01, 05-02, 03-02,
03-03, 02-03); settings-in to DEL-04-03 and record-out from it; the host
contribution for direct application (§7, from the host through DEL-03-02);
result-standing facets (from DEL-03-01, 03-02, 04-03); checkpoint overlay
(from DEL-02-03 through RS R8); network-destination display (from DEL-05-01).

| Aspect | What AS has | What is missing |
|---|---|---|
| Interfaces | §6 settings-in and record-out element lists; §7 four host elements with availability states; §2 grant model received | No "provided to receivers" section for the five HANDOVER rows. No interface for the network-destination inputs (which LOOP events or control reads feed §3). No statement of the control interface the person uses (REQ-001) |
| States | Seven grant display states with entry evidence and transitions (§3); dispositions (§4); comparison results (§6); availability states (§7); standing facets with value sets (§8) | In-work destination grant states are asserted by reference ("the seven states … apply to these grants too") without transitions for *once* consumed, *this run* ended, *always* listed |
| Data | Semantic names only (§0; U-10) | No representation. No display-state model for the contacted-destination record. No identity for a "settings version" beyond the name |
| Operating sequences | §5 during-work change (5 steps); §7 undo interaction | No sequence for an in-work destination request and grant as seen by the display; none for the §6 comparison (when it runs, per change or per run end) |
| Failure behaviour | §5 "Failure behaviour" (control unreachable, conflicting reports, record write fails); §7 *missing / mismatch / unknown*; F4, F5, F8 | No failure row for the network inputs (native layer reports nothing: RS has "destinations not observed"; AS has no display for it). No behaviour when record-out carries an unknown format version (RS OF-7) |
| Verification | 27 scenario rows (F1–F21 with their variants), 18 cases mapped to VER-001…VER-007; two-part phase results | No component exists to bind a case to. F21 has no failure variant |

Structural choices still open:

- **OI-014 (U-08).** It decides whether AS is a component design or a
  display-meaning contract that PANEL and the App each implement. OUT-001
  cannot be designed past meanings until it is chosen.
- **Owner of the contacted-destination display** (AS, as the SoW says, or
  PANEL ND-4, as R8-13 and PANEL have it).
- **Whether network-destination grants ride the §6 exchange** (and RS §8,
  which must stay identical) or travel only through RS R15 and R9.
- **N-OPEN-4** changes the allow-list rows of §3.
- **U-17** changes the "prior act not counted" marking.

## 2.6 Joins

| Local row | Other end | Contribution | DAG-003 | Supplier text | Consumer text | Disagreement |
|---|---|---|---|---|---|---|
| DEP-04-02-007 (UP) | DEL-04-01 | adopted policy | admitted | ACT §5, §8 | AS §2 (l.118) | none found |
| DEP-04-02-008 (UP) | DEL-04-03 | record-out: settings, act evidence, lapse | held (SCC-002) | RS §8 | AS §6, §8 human-acts facet | bodies byte-identical |
| DEP-04-02-009 (DOWN) | DEL-04-03 | settings-in | held; MIRROR of DEP-04-03-022 | AS §6 | RS §8; R6 (l.185) | none; neither side carries destination grants |
| DEP-04-02-015 (UP) | DEL-03-02 | proposal/outcome and origin semantics | held | P §13 l.704 "Direct-branch entry condition and origin semantics (§4.4); standing per outcome (§9)" | AS §7 cites DEL-03-02 §3.3 (origin) and §4.5 (undo); §8 cites §9 | P's provide row names §4.4 ("Direct-autonomy branch") and §9; AS also takes the origin elements from P §3.3 ("Origin, attribution and governing constraint") and the undo relation from §4.5, which P's row to DEL-04-02 does not list |
| DEP-04-02-016 (UP) | DEL-03-01 (N-01) | read basis and standing facets | held | C l.75 "consumes §6" | AS §8 cites DEL-03-01 §6.2 and §4.1 | none found |
| DEP-04-02-017 (UP) | DEL-02-03 (N-02) | checkpoint recording annotations | held | EXEC §9.2 l.1215 "Display meanings of the §4.3 annotations, §3.3 report and hold-support values … AS §4 re-pointed" | AS §4 (l.237) | none found |
| DEP-04-02-018 (UP) | DEL-05-01 (R8-A) | allow list, in-work grants, contacted-destination record | held | LOOP §2.3 events l.401–406; §5.1.1; l.1335 "AS §3 (display)" | AS §3 "from the host's control (LOOP §5.1.1; PANEL §3.8 ND-5)" | **AS uses two of the three.** LOOP assigns the destination record's display to AS §3; AS §3 has no such row; PANEL ND-4 has it |
| DEP-04-02-019 (DOWN) | DEL-05-01 (N-03; DEP-05-01-025) | visible autonomy state | held | AS header l.12 "grant in force per dispatch"; §3 | LOOP l.1342, 1368 "Grant states incl. policy default … AS-v0.6"; LOOP l.1342 still says "Register gap (C1)" | AS has no section for "grant in force per dispatch" |
| DEP-04-02-020 (DOWN) | DEL-05-02 (N-04; DEP-05-02-019) | visible autonomy state | held | AS §3, §4 | PANEL ND-5 (l.544) "as AS §3 defines them"; PANEL l.864 "DEL-04-02 consumption (F-3) … C1" | none in content; PANEL's row still reads as pending |
| DEP-04-02-021 (DOWN) | DEL-03-02 (N-05) | visible autonomy state | held; this row is the representative | AS §3, §6 | P §13 l.701 "Expect from DEL-04-02: Grant display states incl. *effective (policy default)*; grant value and scope per class; settings version identities"; P l.192 | none. V12 F6: the arc rests on the supplier SoW's sentence; the consumer SoW is silent |
| DEP-04-02-022 (DOWN) | DEL-03-03 (N-06) | visible autonomy state | held; representative | AS §3 | ADAPTER §11 l.1055 "Grant display states incl. *effective (policy default)*; settings references" | none found |
| DEP-04-02-023 (DOWN) | DEL-02-03 (N-07) | visible autonomy state | held; representative | AS §3 | EXEC l.1197 "AS-v0.4 read. Current: AS-v0.6" | EXEC's read basis is v0.4. V12 F6 applies |

No local row: DEL-03-04 → DEL-04-02 (DEP-03-04-012, admitted); DEL-09-06 →
DEL-04-02 (N-08, admitted); DEL-09-09 → DEL-04-02 (N-09, held; XT IN-29 l.110
still says "not registered in DEL-09-09 Dependencies.csv (F-2)").

N-18, N-21, N-24 and X-1 have no end at DEL-04-02. The per-item dispositions
and item-left events that N-18 and N-21 carry reach AS only through RS
record-out.

All rows: RequiredMaturity INITIALIZED (TBD for the externals),
SatisfactionStatus PENDING. None is satisfied.

## 2.7 Carried review items that name AS

| Item | State | Evidence |
|---|---|---|
| V6 m-1, m-3…m-7 | none names AS; V6 lists AS F6c, F6d as "holds" | V6 §7 |
| C1-A: EXEC F-23 "re-affirm current setting" presentation not applied | **open** (with U-17) | no occurrence of "re-affirm" in AS |
| C1-A SC-04-02-1…-6 | applied to the SoW (SCA-V4-001); SC-04-02-6 amended into TBD-006 | RV-1_DEL-04-02 |
| C1-A "SoW-level decision on direct consumption" (V1-A RF-05) | decided: direct (O-11, DECISION-7) | BASIS-ALIGN `OWNER_DECISIONS.md` |
| V9 N-2 (AS S15 carried the R8-9 marker correctly); N-3, N-7 | do not ask AS to change | V9 |
| V10 S-1 (U-21 wording), S-3 ("silent") | fixed | l.588; l.221 |
| V10 N-1 | **open** | l.8 |
| V12 F6 (N-05, N-07 consumer wording) | open as advice; SCA-V4-002 left it out by decision | HANDOFF open matters |
| HANDOFF "17 Design re-pins" | **open**; this pass | §2.1 |

## 2.8 Recommended work on AS in this pass

1. Re-pin the header (four doc hashes, SoW `f16ffa8a…`, ANS, siblings). Put
   DECISION-4, DECISION-5 and SCA-V4-001/002 in the Basis line. Rebuild the
   Receivers line from rows 019–023; close U-15. [§2.1, §2.2]
2. S3, OV-4 and the header: current V4-HI-42 and V4-WF-05 wording. S15: drop
   the "flagged" marker and cite the PRD; relabel the model-destination
   reading as owner-confirmed. [§2.1, §2.3, §2.4]
3. Add the contacted-destination display, or record in AS which file owns it,
   in agreement with LOOP l.1335 and PANEL ND-4/ND-5. [§2.2, §2.6]
4. With RS: decide and write whether §6 / RS §8 carries network-destination
   grants and contacts; keep the two bodies identical. [§2.2, §2.5]
5. Add "Provided to receivers": for each of the five, the elements, the
   condition of use and the behaviour on *unconfirmed* or *missing*. [§2.2,
   §2.5, §2.6]
6. Remove the §10 parenthetical; cite TBD-006. [§2.2]
7. Add transitions for in-work destination grants and a failure row for
   "destinations not observed". [§2.5]
8. State the OUT-001 component structure as PROPOSED options under OI-014,
   so the owner has something concrete to choose between. [§2.4 U-08, §2.5]

Not in this pass: host elements (U-04…U-07, U-12, U-18); U-20; hold display;
building components or fixtures; choosing OI-014, N-OPEN-4 or U-17 (owner).

---

# 3. DEL-04-03 — `RECORD_SEMANTICS.md` (RS-v0.6)

## 3.1 Pins

Stale (11):

| # | Pin (line) | File value | Current value |
|---|---|---|---|
| R-P1 | "repo 6e18505e3 (accepted basis)" for PRD, HOST_INTEGRATION, ARCHITECTURE §4, EXAMINATION (l.7) | `6e18505e3` | all four amended (hashes in §1.1, §2.1) |
| R-P2 | `ScopeOfWork.md` sha256 `74d42c38…40c1` (l.7) | the INIT contract | `ceecddbb67a86f744b413bb08b08c27017a82ebee8500f7600faf8d880fbaa47` (SCA-V4-001; unchanged by SCA-V4-002) |
| R-P3 | V4-WF-05 by halves (l.4, 115) and "flagged" (l.4) | — | amended |
| R-P4 | V4-HOST-02 "as revised by DECISION-5 (R8-13; flagged for the next accepted-basis update)" (D16 l.109; l.5, 37) | marker | in the PRD. The D16 quotation equals the amended text exactly |
| R-P5 | §4 lead "Every element named in REQ-002 / SOW-186 / V4-HI-70 is present … Elements marked **addition** go beyond the SoW inventory" (l.172), with R15 marked "addition (R8-13; DECISION-5)" (l.194) and R5's destination marked "INTEGRATION, DECISION-2 reading" (l.183) | labels | REQ-002 and CLM-002 now require "model used with its observed destination per turn; for a host's agent, each network destination contacted, with the allowing grant or list entry"; V4-HI-70 now ends "… the model used and, for a host's agent, each network destination contacted (D-07; V4-HOST-02)". Both are inside the SoW inventory |
| R-P6 | ANS `6f01add3…` (l.10) and "unchanged" (l.9) | true at `94aa9181b` | `afb6e063…` |
| R-P7…R-P9 | EXEC `d32be377…`, WD `fce565ed…`, WD-EX `950b70b2…` (l.10) | true at `94aa9181b` | `092f2486…`, `43a9962f…`, `8d60ed78…` |
| R-P10 | Intake `BRIEFS.md` `3e33ba26…` (l.8, 10) | true through `3733b14218` | `6f32809d…` |
| R-P11 | Receivers "`Dependencies.csv` DEP-04-03-011…016 … By join (not registered): DEL-03-03 …, DEL-09-06" (l.12) | six rows | rows 021–033 added 2026-09-29; DEL-03-03 is DEP-04-03-026 and DEL-09-06 is DEP-04-03-031 |

Current or true: RS-v0.5 `2939eb09…` at `c6f81a4f2`/`94aa9181b`, RS-v0.4
`56806b64…` at `cc58211c5`; first-run and intake ruling hashes as in §1.1;
sibling history pins (`git show`); sibling version labels; §8 identical to AS
§6; every cited sibling section and identifier resolves (scripted). Serves
line (REQ-001…006, AC-001…007, VER-001…006) matches the SoW.

## 3.2 ScopeOfWork alignment (SoW `ceecddbb…`)

| SoW item | Where RS answers | State |
|---|---|---|
| CLM-001 / REQ-001 / AC-001 | §2 OF-1…OF-9; VC-01 | developed |
| CLM-002 / REQ-002 / AC-002 | §4 R1–R15; §5; §9; VC-02, -03, -22, -30 | developed in meaning; labels lag (R-P5); VC-02 checks "R1–R14" (l.672) although R15 exists |
| CLM-003 / REQ-003 / AC-003 | §3, §6; VC-04…-06 | developed |
| CLM-004 receives act kinds and classes from DEL-04-01 | §0; §6.1 | developed |
| … settings-in from DEL-04-02 | §8; R6 | developed |
| … subject content identities and method designations from DEL-03-01 | L-1, L-2 | developed |
| … outcomes, change-item content identities, receipt links from DEL-03-02 | §5 | developed |
| … "checkpoint arrival, act and lapse events (with hold events retained for the governance phase) and compatibility reports" from DEL-02-03 | R8, R14, L-12 | developed |
| … external dispatch entries from DEL-03-03 | R7; §10 row | developed |
| … observed supplier facts from DEL-01-01 | R3, R5, R13 | developed |
| … network-destination events from DEL-05-01 | R15; §4.3; E13 | developed |
| CLM-005 | §10 external host row; §11 | developed |
| CLM-006 / REQ-004 / AC-004 | §7 L-0…L-13 | developed; U-07 and U-12 held |
| OUT-001 versioned format (CONFIG) | §3, §4, §6, §9 | **partial**: inventory complete; no serialization, field names, identity form, location or version scheme (U-04, U-05) |
| OUT-002 writer/reader and lapse handling (CODE) | §5 rules, §7 | behaviour rules developed; no writer or reader design |
| OUT-003 fixtures | §12 E1–E13; VC-01…VC-30 | designed only |
| OUT-004 interface documentation | §10, §11 | developed, with the gaps below |
| REQ-005 (revised): consumers PKG-02, PKG-03, **PKG-05 (DEL-05-01, DEL-05-02)**, PKG-06, **PKG-09 (DEL-09-06, DEL-09-09)**; DEL-04-02; DEL-09-11; host-agent runs | §10 | **partial**: **no DEL-09-09 row** (the ID appears only in the sibling-version list, l.9). DEL-09-06 row says it consumes "R2 transfer links" only |
| REQ-006 / AC-007 | §11; VC-25 | developed, with one stale sentence |
| AC-005 / VER-004 | OE-1…OE-7; VC-14…-16, -19, -21 | developed |
| AC-006 / VER-005 | VC-24 | designed |
| TBD-001 (ruled; OI-021) | §11; U-01 | developed |
| TBD-002 (OI-013/014) | U-05, U-06, U-16 | named |

Contradictions and lags:

1. **§11 l.467–468**: "The SoW's TBD-001 still reads OI-001/OI-002 as open — a
   pointer reconciliation for closeout C1." The SoW TBD-001 was revised
   (RV-1_DEL-04-03 E-0403-04).
2. **§10 has no DEL-09-09 row** (REQ-005). XT IN-08 (l.89) consumes RS-v0.6
   for XC-09.
3. **R15 and R5 labels** (R-P5).
4. **VC-02** inventory range.
5. **Header Receivers** (R-P11).

## 3.3 Amended basis

| Item | RS text | Agreement |
|---|---|---|
| V4-WF-05 | l.4; §1 "It records an act only when the person performed it (V4-WF-05 second half)" (l.115) | intent agrees; wording by halves; one "flagged" marker |
| "is requested" | R8 per-arrival elements (l.187) list arrival, referents, disposition, ordinals, satisfying act, annotations and events | **Gap.** There is no element for the request for the required act. "A8" occurs in RS only at l.71, 262, 334, 344, 399, 511, 626, 675, 690, never as a run-record element. An A8 "exists only if issued" (l.262) but has no recorded home. LOOP emits "Destination request issued" (LOOP l.402) and MS-16 expects "Recorded: the A8" (LOOP l.1089); R15 has no element for it |
| V4-HI-42 | not cited; D14 (l.107) carries "No grant widens past a reserved act or declared checkpoint" with the R8-11 reading | agrees with the amended text |
| V4-HOST-02 | D16 (l.109) | exact quote; stale marker. R15 records "every destination contacted … in any model mode" as the text requires |
| V4-HI-70 | l.7, 144, 172 | R15 satisfies the added clause; the "addition" label lags |
| V4-HOST-01, V4-ARC-11 | not cited; R5 "destination class (local model server / user-chosen cloud) from the person's provider configuration" (l.183); E13 "Cloud chosen and signed in" | agrees; no default is assumed |
| V4-ARC-12 | not cited; Basis cites ARCHITECTURE §4 | R15 "Host native layer and control", boundary refusal and the outside-process limit agree with the amended §4 properties |
| V4-EXM-22 | basis line | E10 Phase-1 part agrees |
| V4-EXM-23 | not cited | E13 and VC-30 cover "every destination contacted is recorded"; "An outside process that is not sandboxed is examined within that stated limit" matches R11 "process network not observed". No trace to the ID |
| "local-first" | none; "local model server" once (l.183) | not touched |

## 3.4 Open items

| ID | What is open | Owner / point of need (file) | Class |
|---|---|---|---|
| U-01 (E9 held) | OI-021 | Owner via outside SWB session and App/shared owner | **OWNER**, deferred |
| U-02 | Consequence vocabulary (scope slot) | DEL-04-01 with host policy owner | **OWNER** |
| U-04 (with OF-5 "Proposed; mechanism unselected") | Serialization, field names, identity algorithms, record-identity form, carriage-manifest representation; correction mechanism | DEL-04-03 with DEL-03-01 (TBD-003) and DEL-02-01 / before OUT-001 CONFIG and writer implementation | **SPIKE** — a serialised run record and act records for E1, E4 and E6, written and read back, with the L-0…L-13 comparison run on them |
| U-05 | App record location | DEL-04-03 with OI-014 owners / before writer implementation | **OWNER** |
| U-06 | Host persistence and placement (OI-013) | shared contract owner with SWB implementation owner | **HOST** |
| U-07 | Multi-row A4 purpose after partial lapse | DEL-04-01 with Owner | **OWNER** |
| U-08 | Workflow review/registration as an act kind | DEL-04-01 with DEL-02-02 (later) | **LATER** |
| U-09 | Host re-checks the basis after acceptance | host owner | **HOST** |
| U-11 | Host capture requirement and reference | SWBPIPE owner decision | **HOST** |
| U-12 | Effect of content returning to c₀ after an observed lapse | host owner (U-C2) with DEL-04-03 / before lapse display criteria are fixed | **HOST** as stated. The App-side meaning (does the act count again) has no record that settles it |
| U-14 | Host-stored findings as a change operation | host owner | **HOST** |
| U-15 | Host receipts, origin marks, identities, resulting objects, lapse, settings version, de-duplication | SWBPIPE outside session | **HOST** |
| U-16 | Reader/writer placement (OI-014) | App/shared contract owners | **OWNER** |
| U-19 | Constraint receipt (governance phase) | host owner | **HOST** |
| U-20 | R13 feed beyond DEL-01-01 observed facts | DEL-01-02 (later) | **LATER** |
| U-21 | Host-loop per-turn guidance identities | host owner | **HOST** |
| U-25 | App-side run holds (D6) | the owner / governance phase | **LATER** |
| U-26 | SP-6 against counting a prior act | DEL-02-01 with DEL-04-01; Owner if preferred | **OWNER** |
| U-27 | Caller identity verification | App owner with host owner | **HOST** |
| U-28 | App person identity scheme and App act control (EXEC U-E8) | DEL-01-04 (later) with DEL-04-03 / before App capture fixtures | **LATER** — this is X-1's contribution; DEL-01-04 is outside the 14 |
| U-29 | Per-subject identity not met by SWBPIPE | SWBPIPE | **HOST** |
| U-30 | The host's native destination report (the DECISION-5 points are closed) | host owner (DEP-001) / before R15 writer implementation | **HOST** |
| §10 DEL-01-01 row (l.454) | "whether requested and effective can differ is not observed (HOSTING U-19)" | App implementation owner, next spike (HOSTING l.1134) | **SPIKE** — owned by DEL-01-01; needs a credential or local provider |
| §10 DEL-09-06 row (l.455) | "Host links AWAITING INPUT" | host | **HOST** |
| §10 DEL-03-02 cell (l.449) "Consumes: §5 evidence rules" | HANDOFF open matter: the cell behind the dropped arc N-12 | DEL-04-03 owner | **NOW** — ARC_ANALYSIS §3.3; DECISION-6: restate as "P's outcomes are recorded under §5" |
| §11 sentence; D16 and header "flagged"; R5/D16 "INTEGRATION (DECISION-2 reading)"; R15/R5 "addition" | stale standing text (four items, counted as four) | — | **NOW** — SCA-V4-001; DECISION-7 (O-10, O-14); SoW REQ-002 |
| §3 run finality PROPOSED (R4-4); L-13 PROPOSED; R8 `governed` PROPOSED | standing labels | EXEC / WD | **OWNER** at the phase review |
| VC-01…VC-30; "no writer, reader or fixture exists" (l.6) | nothing built or run | — | **LATER** |

Counts: NOW 5 · OWNER 7 (1 at the phase review, 1 deferred) · HOST 12 · SPIKE 2
· LATER 5.

## 3.5 Design depth against the 60% description

Contributions exchanged: record meaning to DEL-02-01, 02-03, 04-02, 05-01,
05-02, 09-06, 09-09, PKG-06, DEL-09-11 and host run recording; inputs from
DEL-04-01, 04-02, 03-01, 03-02, 02-03, 03-03, 01-01, 05-01.

| Aspect | What RS has | What is missing |
|---|---|---|
| Interfaces | §10 consumer table (consumes / supplies back / held part); §8 exchange; §9 evidence-reference elements | No writer-side interface: what each supplier hands over, in what unit (event, entry, snapshot) and when. No reader-side interface beyond §8 record-out. No DEL-09-09 row. Cells narrower than the consumers' own citations (§3.6) |
| States | Lapse states (8, plus 2 for A12/A13); A12 control effect (4); dispositions as record labels; resolution status at write and read; run finality | No state for a record itself (written, corrected, superseded, unreadable version). OF-5 names correction without a mechanism |
| Data | R1–R15 inventory with supplier and absence handling; §5 entry elements; §6.1 act-record elements; §9 reference elements | **No format.** OUT-001 is "Versioned … format (CONFIG)"; RS selects "no serialization, field spelling, type, file path, persistence, transport, hash or canonicalization algorithm" (l.64–67). No record-identity form, no format-version scheme behind OF-7, no unit of storage (one file per run, per act, or an appended log). No element for A8 requests (§3.3) |
| Operating sequences | L-0…L-13 as an ordered comparison; OE-1…OE-8; E1–E13 narratives | No write sequence (what is written at arrival, at act capture, at run end; ordering against "written-at order"). No read sequence (when c₁ is obtained; whether lapse is evaluated on read or on event). No correction sequence |
| Failure behaviour | R11 evidence limits (18 kinds); L-2/L-3 unknowns; OF-7 "refuses or limits an unknown version"; *not yet evaluated* never shown as *not lapsed* | No writer failure behaviour (AS §5 says a failed write shows *missing in record*; RS does not say what the writer leaves). Nothing on two recorders writing the same act (host facility and App faithful record, E2), partial writes, or a record whose referenced evidence later becomes unresolvable (SWBPIPE receipts are session-only, l.459) |
| Verification | 30 cases mapped to VER-001…VER-006; positive and negative per AC (VC-24) | Nothing executable. VC-02 range stale. No case for an unknown format version or for a correction record |

Structural choices still open:

- **The format itself (U-04)** and the unit of storage. Every consumer's
  reader, DEL-09-11's reconstruction and the AS comparison depend on it.
- **Location and placement (U-05, U-16; OI-014) and host-loop records
  (U-06; OI-013).**
- **Identity method** for content identities and record identity (shared
  with DEL-03-01 TBD-003).
- **Whether requests (A8) are recorded** and where.
- **Whether the network allow list in force is a recorded settings version**
  (R6) or only appears through R15 grants and contacts.
- **U-26** changes L-13.

## 3.6 Joins

| Local row | Other end | Contribution | DAG-003 | Supplier text | Consumer text | Disagreement |
|---|---|---|---|---|---|---|
| DEP-04-03-014 (DOWN) | DEL-04-02 | run evidence for display | held; MIRROR of DEP-04-02-008 | RS §8 | AS §6, §8 | none |
| DEP-04-03-021 (UP) | DEL-04-01 | act kinds and classes | **admitted** | ACT §2.1, §2.4, §8.1 | RS §0, §3, §6.1 | none found |
| DEP-04-03-022 (UP) | DEL-04-02 | settings-in | held | AS §6 | RS §8; R6 | none |
| DEP-04-03-023 (UP) | DEL-03-01 (N-10) | subject content identities and method designations | held | C §5.3 (heading exists); C l.76 | RS L-1 (l.367), L-2 | none found |
| DEP-04-03-024 (UP) | DEL-03-02 | outcomes, change-item content identities, receipt links | held | P §13 l.705 "Provide to DEL-04-03: Canonical §9 taxonomy; per-submission recording and precedence (§5, §7); … origin and constraint (§3.3); act/evidence table (§10); undo relation (§4.5); item-left events (§4.3)" | RS §5 (l.230, 253) | RS §10 l.449 also says DEL-03-02 **consumes** "§5 evidence rules"; P §13 has no "Expect from DEL-04-03" row (N-12, not proposed by decision) |
| DEP-04-03-025 (UP) | DEL-02-03 (N-13) | arrival, act and lapse events; compatibility reports | held | EXEC §9.2 l.1212 "RS v0.6 matches §3.6, §4 and §6" | RS R8, R14, L-12 | EXEC l.1198 records "RS-v0.4 read" in its inputs table and "RS v0.6 matches" in §9.2 |
| DEP-04-03-026 (UP) | DEL-03-03 (N-14) | external dispatch entries | held | ADAPTER §11 l.1062: entries for R7; acts for R9; evidence limits for R11 including "resubmission without prior observation; App-restart interruption"; destination per turn; A14 for R13 | RS R7, R11; §10 l.450 | **RS R11 has no "resubmission without prior observation" and no "App-restart interruption"** (grep: 0 occurrences of either word in RS). The other limits match |
| DEP-04-03-027 (UP) | DEL-01-01 (N-15) | observed supplier facts | **admitted** | HOSTING §8 l.746 "S-7 evidence — DEL-04-03 (through DEL-01-02)"; §8.3 | RS R3, R5, R13; §10 l.454 | HOSTING routes the facts "through DEL-01-02"; the SoW and RS R13 take them from DEL-01-01 "in this undertaking". HOSTING's change table cites RS-v0.4 (l.57) |
| DEP-04-03-028 (UP) | DEL-05-01 (R8-B) | destination contacted, grant, declined | held | LOOP §2.3 l.401–406 (six events); l.459–460 | RS R15 (l.194) | LOOP's "Destination request issued" has no RS element. "Destination refused at boundary" = RS "Boundary refusal", same three reasons |
| DEP-04-03-029 (DOWN) | DEL-05-01 | record format and meaning | held; MIRROR of DEP-05-01-019 | RS §4, §10 l.452 | LOOP l.1343, 1369 "Record inventory … RS-v0.6"; cites R15, R11, L-12 | none found |
| DEP-04-03-030 (DOWN) | DEL-05-02 | record format and meaning | held; MIRROR of DEP-05-02-009 | RS §10 l.453 "Act, act-declined, lapse, supersession, annotation display meanings" | PANEL cites RS R15 four times (ND-4 cases) and R11 | RS's cell omits R15 and R11, which PANEL uses |
| DEP-04-03-031 (DOWN) | DEL-09-06 | record format and meaning | **admitted**; MIRROR of DEP-09-06-015 | RS §10 l.455 "R2 transfer links" | CA cites RS R7, R8, R10, §4, §6; CA l.541 "Cited at `8fb51f07f` (v0.4) … not re-read by A5" | RS's cell is narrower than CA's citations; CA's read basis is v0.4. RequiredMaturity differs: DEP-09-06-015 TBD, DEP-04-03-031 INITIALIZED (HANDOFF open matter) |
| DEP-04-03-032 (DOWN) | DEL-09-09 | record format and meaning | held; MIRROR of DEP-09-09-011 | **no RS §10 row** | XT IN-08 (l.89); cites RS R7, R11, §6 | supplier file does not state the exchange |

Package rows DEP-04-03-011, -012, -013 (PKG-02, PKG-03, PKG-06) are
non-topological. The deliverable arcs DEL-02-01 → DEL-04-03 (DEP-02-01-019,
held; WD l.926 "Not read; via IR1-A and R2. Current: RS-v0.6"), DEL-02-03 →
DEL-04-03 (DEP-02-03-013, held) and DEL-03-01 → DEL-04-03 (N-11,
DEP-03-01-031, held; C l.480 uses "DEL-04-03 §7 vocabulary") have no local
mirror row.

N-18, N-21, N-24 and X-1 have no end at DEL-04-03. N-21's and N-24's
contributions reach RS through DEP-04-03-025 and -026. X-1's contribution is
RS U-28.

All rows: SatisfactionStatus PENDING. None is satisfied (`_DEPENDENCIES.md`:
23 PENDING, 0 SATISFIED). One label slip in that file's Run Notes: it calls
the DEL-09-06 row DEP-04-03-031 "N-08"; in ARC_ANALYSIS N-08 is DEL-09-06 →
DEL-04-02, and the DEL-04-03 arc is the older DEP-09-06-015.

## 3.7 Carried review items that name RS

| Item | State | Evidence |
|---|---|---|
| V6 m-1, m-3…m-7 | none names RS; V6 lists RS E7 as "holds" | V6 §7 |
| C1-A: R11 *action during hold* lacks the turn initiator (EXEC F-24) | fixed (R6-5) | l.190 "turn initiator — person-directed · agent · App rule" |
| C1-A SC-04-03-1…-4 | applied to the SoW; SC-04-03-3's condition met (O-10, O-14) | RV-1_DEL-04-03 |
| V9 N-5 (E7 "passes on required tools") | fixed | l.550 "required tools and channel state (EXEC MT-16, CH-12)" |
| V9 N-3, N-7 | do not name RS | V9 |
| V10 S-1 (U-30 wording) | fixed | l.662 |
| V10 N-1 | **open** | l.8 |
| HANDOFF: "The RS §10 DEL-03-02 cell … behind N-12" | **open** | l.449 unchanged |
| HANDOFF: mirror maturity difference DEL-09-06 → DEL-04-03 | open; a register matter, not a Design edit | DEP-09-06-015 / DEP-04-03-031 |
| HANDOFF "17 Design re-pins" | **open**; this pass | §3.1 |

## 3.8 Recommended work on RS in this pass

1. Re-pin the header (doc hashes, SoW `ceecddbb…`, ANS, siblings); rebuild
   Receivers from rows 014 and 021–032. [§3.1]
2. §4: remove "addition" from R15 and "INTEGRATION (DECISION-2 reading)" from
   R5 and D16, citing revised REQ-002, amended V4-HI-70 and PRD V4-HOST-02;
   drop the "flagged" markers; re-word the V4-WF-05 sentence; VC-02 to
   R1–R15. [§3.1, §3.2, §3.3]
3. §10: add DEL-09-09; restate the DEL-03-02 cell per ARC_ANALYSIS §3.3; widen
   the DEL-09-06 and DEL-05-02 cells to what CA and PANEL cite; settle with
   ADAPTER the two R11 limits it says it supplies. [§3.2, §3.6, §3.7]
4. §11: remove the stale SoW sentence. [§3.2]
5. Decide and write whether an act request (A8) and a destination request are
   record elements, in step with ACT item 3 and LOOP §2.3. [§3.3, §3.5, §3.6]
6. With AS: the §8 / AS §6 treatment of network-destination grants. [§2.2,
   §3.5]
7. Write the writer and reader sequences and their failure behaviour (write
   failure, two recorders, unknown version, correction). [§3.5]
8. Propose a concrete format as PROPOSED, preferably backed by the bounded
   prototype of U-04. [§3.4, §3.5]

Not in this pass: host recording and every host row; final choice of an
identity algorithm if DEL-03-01 TBD-003 is not taken up with it; record
location (OI-014, owner); DEL-09-11's witness; implementation of the writer.

---

# 4. Across the three files

| | ACT (DEL-04-01) | AS (DEL-04-02) | RS (DEL-04-03) | Total |
|---|---:|---:|---:|---:|
| Stale pins | 10 | 11 | 11 | **32** |
| Open items: NOW | 8 | 3 | 5 | 16 |
| Open items: OWNER | 9 | 7 | 7 | 23 |
| — of which decided at the phase review (PROPOSED labels) | 1 | 1 | 1 | 3 |
| — of which deferred with the host joins | 2 | 1 | 1 | 4 |
| Open items: HOST | 3 | 7 | 12 | 22 |
| Open items: SPIKE | 0 | 1 | 2 | 3 |
| Open items: LATER | 8 | 2 | 5 | 15 |

Several OWNER rows are one decision seen from three files: OI-021 (ACT U-01,
AS U-01, RS U-01); consequence vocabulary (U-02 in each); multi-row A4 (ACT
U-03, AS U-19, RS U-07); capture after arrival (ACT U-14, AS U-17, RS U-26);
OI-014 placement (ACT U-12, AS U-08, RS U-05 and U-16). Counted once each, the
distinct owner choices are: OI-021 (deferred); the consequence vocabulary;
multi-row A4 after partial lapse; capture after arrival; OI-014 placement;
A13 disabling (F-11); the A12 mapping of destination grants (F-22); N-OPEN-4;
the launch environment variable (deferred).

Nine stale pins are common to all three files (basis commit, SoW hash,
V4-WF-05 wording, ANS hash, three sibling byte hashes, intake BRIEFS hash,
register reference). The file-specific ones are V4-HI-42 (ACT, AS),
V4-HOST-02 marker (AS, RS) and the V4-HI-70 / REQ-002 inventory labels (RS).

**The three most consequential gaps.**

1. **No data representation in any of the three.** ACT's OUT-002 "adopted
   policy-class configuration" and RS's OUT-001 "versioned … format (CONFIG)"
   exist only as element meanings; AS's OUT-001 components have no structure.
   Placement (OI-013, OI-014), the record format (RS U-04), the policy record
   form (ACT U-12) and the consequence dimension (U-02) are all open. Each can
   still restructure these files and their consumers, so the 60% condition
   "further structural changes are no longer anticipated" is not met here.
2. **The checkpoint wording lags the amended basis, and the request for the
   act has no home.** All three describe V4-WF-05 by halves; ACT and AS call
   V4-HI-42 "override autonomy" or "guidance in Phase 1". The amended texts
   state, without a phase qualifier, that the act is requested and is recorded
   as done only when the person performs it, whatever the autonomy setting. No file says who issues
   the request at a Phase-1 arrival, and RS has no element to record it.
3. **The DECISION-5 content is not joined end to end.** AS has no display for
   the contacted-destination record its SoW and DEP-04-02-018 name. The AS §6 /
   RS §8 exchange carries no destination grant or contact. RS has no element
   for LOOP's "Destination request issued". The A12 mapping is still
   INTEGRATION, and DEL-04-01's own SoW does not carry DECISION-5 (AC-007).

**Owner-level choice to bring forward** (ACT F-22 only says "the owner may
revisit it at any time"): whether to confirm the mapping of a network-destination grant to A12 under
D2 (e) (ACT F-22). OWNER_ITEMS O-15 left it for "when the A12 mapping is
confirmed or at implementation". Until it is confirmed, ACT §2.7 rests on an
integrator reading and has no anchor in the DEL-04-01 ScopeOfWork, and a
confirmation would call for a SoW sentence that this run may not write.
