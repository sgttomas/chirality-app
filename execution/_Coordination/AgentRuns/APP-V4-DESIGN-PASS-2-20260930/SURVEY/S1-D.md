# S1-D — scoping survey: LOOP, PANEL, HOSTING and PIN_SPIKE

- Run / node: `APP-V4-DESIGN-PASS-2-20260930`, node **S1-D**. Type 2 TASK executor (Claude Code subagent; parent HELP_HUMAN). No delegation. Read-only git, no network. This file is the only file written.
- Date: 2026-09-30. Worktree HEAD `4698471d9e` (branch `claude/chirality-app-v4-60-percent-a41fd5`).
- Subject files (sha256 of the bytes read; line numbers below refer to these bytes):

| Short | File | Lines | sha256 |
|---|---|---|---|
| LOOP | `PKG-05…/DEL-05-01…/Design/LOOP_RECEIVING_CONTRACT.md` (LOOP-v0.6) | 1,585 | `246f4636166c67250f73862de586afef3cad91ba538272880a80c2fd657a5767` |
| PANEL | `PKG-05…/DEL-05-02…/Design/PANEL_RECEIVING_CONTRACT.md` (PANEL-v0.6) | 881 | `dd71e11dbe0d9872727524aef69ef80ba118980533148c2aa7453d1176165658` |
| HOSTING | `PKG-01…/DEL-01-01…/Design/HOSTING_BOUNDARY.md` (HOSTING-BOUNDARY-v0.6) | 1,176 | `d11d4c574aa3c342bfac9c1d1e9bf3746aa885baafd17eaa296a79a523e3d0b9` |
| SPIKE | `PKG-01…/DEL-01-01…/Design/PIN_SPIKE_0.158.0.md` (PIN-SPIKE-v0.1) | 351 | `0e090a4ca14e3ec323e8302ea4bc4e1fefc66bee50d0d3247e1cd0ddc04eb115` |

## Method and limits

- **Read in full:** the four Design files; the three `ScopeOfWork.md`, `Dependencies.csv` and `_DEPENDENCIES.md`; `_DAG/DAG-003/HANDOFF_STATE.md`; `loop/LOOP_INIT.md` "Develop the detail appropriate to the phase"; first-run `reviews/V6.md` and `closeout/CLOSEOUT_ACCOUNT.md`, `C1-C.md` (DEL-05-01, DEL-05-02 sections); intake `reviews/V9.md`, `V10.md`, `OWNER_DECISIONS.md` (DECISION-4 text), `R8_RESOLUTIONS.md` R8-1; `APP-V4-BASIS-ALIGN-20260928/RV/RV-2_DEL-05-01.md`, `RV-2_DEL-05-02.md`, `RV-1_DEL-01-01.md` (diffs) and `APP-V4-SCA002-20260929/RV/RV_DEL-01-01.md`.
- **Read in part (targeted passages, by grep and section):** the sibling Design files C, P, WD, WD-EX, EXEC, ACT, AS, RS, ADAPTER, GUIDE, CA; reviews V11–V16 (grep for these files); `C1-B.md` (headings only); the DAG-003 edge CSVs (rows touching DEL-05-01, DEL-05-02, DEL-01-01). Statements about sibling content are limited to the passages cited.
- **Hashes.** Every sha256 in the four files (full or abbreviated) was resolved by script against (a) `shasum -a 256` of the current file and (b) the sha256 of every committed revision of the same path (`git log` + `git show <commit>:<path> | shasum`). Verdicts below use three values:
  - **current**: equals the file's present bytes;
  - **historical-true**: equals the bytes at the commit the pin names, and the file has changed since;
  - **stale**: the file presents it as its basis or as a present fact, and it no longer holds.
- **Quoted texts.** Compared with `git diff 6e18505e3 HEAD -- projects/chirality-app-v4/docs/` and with grep on the current `docs/*.md` and SoWs.
- **Generated bundle.** `grep -v '^#' MANIFEST.sha256 | shasum -a 256 -c` in `Design/generated/0.158.0/` gives 2 OK, 2,357 not present, 0 mismatched (2,359 entries). The bundle sizes are 862,263 B and 750,395 B. Both agree with SPIKE §4 and `COMMITTED_STATE.md`.
- **What I infer is marked "Inference".** Everything else is what a file states or what a check returned.

## Reference A — requirement texts at the pinned base and now

LOOP and PANEL name `repo 6e18505e3 (accepted basis)`; HOSTING and SPIKE name `branch base 6e18505e3`. The four basis docs have changed since (SCA-V4-001 at `230bf1e64` / `a0af39f8c`; SCA-V4-002 at `70376aff2`).

| Doc | sha256 at `6e18505e3` (prefix) | sha256 now |
|---|---|---|
| `docs/PRD.md` | `657593ce12a9a6da` | `bb6e786f7a6c01dc5ce2f16f58e6c600989a12808ff47ce4fd87924bcc6c49bd` |
| `docs/ARCHITECTURE.md` | `c3ae766ee2d660fb` | `317d5789272c5206599936fa9b4e68551b30016d226b88039f0153afa02d828c` |
| `docs/HOST_INTEGRATION.md` | `08c8fc7db2d74619` | `d4331c39db7f452cd3ba72fdfa4bad540a6053931218359a93646971acb28d9f` |
| `docs/EXAMINATION.md` | `1b156553dec7eb10` | `471798bc2f2dc0202ae40d9d5cf033a22ae41af2a0afdf58032cf37a687957d0` |

| ID | Text at `6e18505e3` | Current text |
|---|---|---|
| V4-HOST-01 | "A host's agent runs against a model server the user controls by default; a cloud model is used only if the user chooses one and provides an API key (D-18)." | "A host's agent runs on a model the person chooses: a model server the user controls, or a cloud model reached by OAuth sign-in or an API key. There is no default between them; they are options the person chooses among (D-18; DEC-4)." (PRD L116–119) |
| V4-HOST-02 | "In local operation, a host's agent sends no data to any destination other than the configured model server (D-18)." | "A host's agent sends data only to the model service the person selected and to destinations the person has allowed — in advance in an allow list (by category, such as web access, MCP servers or other APIs, or by named destination) or when the agent asks during its work. Nothing else is contacted: no analytics, silent provider switch or background download unless the person turns it on. Every destination contacted is recorded and shown (D-18; DEC-5)." (PRD L120–126) |
| V4-WF-05 | "The product holds a workflow's declared checkpoints: when a run reaches one, the required human act is requested, and the run does not record the act as done until the person performs it." | "When a run reaches a workflow's declared checkpoint, the required human act is requested, and the run does not record the act as done until the person performs it. Holding the checkpoint — the run waits until the act is performed — is **phased to the governance layer**, not withdrawn (DEC-4): in the current phase, declared checkpoints are plan guidance that the person and the agents manage, and neither the App nor a host's embedded loop enforces a hold, blocks a run, or reports a workflow unsupported because a hold cannot be enforced. Enforced holds are applied later to the workflows that need them; the declared checkpoint and the definitions that enforcement needs are kept so that every such workflow can be served. Reserved human acts (§4.5) are unaffected." (PRD L254–264) |
| V4-ARC-11 | "**Model: the local model server by default**; a cloud model only if the user chooses one and supplies an API key" | "**Model: local or cloud, as the person chooses, with no default** — a local model server the user controls, or a cloud model reached by OAuth sign-in or an API key" (ARCH L165) |
| V4-ARC-12 | "The loop's requests pass through the host's own native layer, which enforces the configured endpoint and holds any key outside the interface's script" | "The loop's requests pass through the host's own native layer, which allows only the selected model service and the destinations the person has allowed, records every destination contacted, and holds any key or sign-in credential outside the interface's script" (ARCH L166) |
| ARCH §4 host-agent property | "In local operation it makes no network request other than to the configured model server (V4-HOST-02)." | Seven-part property (ARCH L172–190): two-level allow list; model service and its sign-in service always allowed; MCP only if stateless (2026-07-28); in-work grant once / this run / always, only the requesting call waits, decline wording; always-off items; every destination recorded and shown in any model mode; outside-process limit; governance phase later; "This property governs a host's embedded agent; the App's own Codex keeps the person's Codex configuration, approval and sandbox choices." |
| ARCH §1 priority 3 | "the host model defaults to the local server; model traffic stays within the selected local-operation boundary. A cloud model is used only by the user's choice." | "a host's agent runs on a local model server the user controls or on a cloud model the person chooses (OAuth sign-in or API key), with no default between them. It sends data only to the selected model service and to destinations the person has allowed, and every destination contacted is recorded and shown (V4-HOST-01/02; DEC-4, DEC-5)." (ARCH L29–33) |
| V4-HI-42 | "A workflow's declared checkpoints override autonomy: at a checkpoint the run waits for the person's act (V4-WF-05)." | "Autonomy does not override a workflow's declared checkpoints: whatever the autonomy setting, a checkpoint's required act is requested and recorded as done only when the person performs it. Holding the run at the checkpoint until then is phased to the governance layer (V4-WF-05): in the current phase a checkpoint is plan guidance that the person and the agents manage, and the reserved acts (V4-HI-30) still bind." (HI L139–144) |
| V4-HI-70 | "… the human acts performed, and the model used (D-07)." | "… the human acts performed, the model used and, for a host's agent, each network destination contacted (D-07; V4-HOST-02)." (HI L219–223) |
| V4-EXM-22 | "A workflow checkpoint stops the run for a human act." | "A workflow checkpoint requests a human act, and the act is recorded only when the person performs it, whatever the autonomy; stopping the run at the checkpoint is examined only for a workflow that takes up the governance phase (V4-WF-05)." (EXM L150–153) |
| V4-EXM-23 | "**Privacy in local operation.** … *Verifies* V4-HOST-02: no request goes anywhere but the configured model server." | "**Host-agent network destinations.** … requests go only to the selected model service and to destinations the person allowed, in advance or when the agent asked during its work; a declined request reaches no destination and is reported to the agent as "destination not allowed by the person"; nothing else is contacted unless the person turned it on; and every destination contacted is recorded and shown. An outside process that is not sandboxed is examined within that stated limit." (EXM L160–167) |
| "local-first" (PRD intro; §2.2 lead) | "… the agent runs local-first, on a model server the user controls"; "Each host embeds a simpler, local-first agent (D-18)" | "… the agent runs on a model the person chooses — a model server the user controls or a cloud model — with no default"; "Each host embeds a simpler agent (D-18), running on a local or cloud model the person chooses (V4-HOST-01)" |

## Reference B — register rows and DAG-003 layer for the three deliverables

DAG-003 (`DependencyEdges.csv` = admitted; `CandidateEdges.csv` = held, `SCC_UNRESOLVED`).

| Row | Consumer → supplier | Layer |
|---|---|---|
| DEP-05-01-014 | DEL-05-01 → DEL-03-01 | held (SCC-002) |
| DEP-05-01-015 | DEL-05-01 → DEL-03-02 | held (SCC-002) |
| DEP-05-01-016 | DEL-05-01 → DEL-02-01 | held (SCC-002) |
| DEP-05-01-017 | DEL-05-01 → DEL-02-03 | held (SCC-002) |
| DEP-05-01-018 | DEL-05-01 → DEL-04-01 | **admitted** |
| DEP-05-01-019 | DEL-05-01 → DEL-04-03 | held (SCC-002) |
| DEP-05-01-020 | DEL-05-01 → DEL-05-02 | held (SCC-002) |
| DEP-05-01-025 | DEL-05-01 → DEL-04-02 | held (SCC-002) |
| DEP-05-02-005 | DEL-05-02 → DEL-02-01 | held (SCC-002) |
| DEP-05-02-006 | DEL-05-02 → DEL-03-01 | held (SCC-002) |
| DEP-05-02-007 | DEL-05-02 → DEL-03-02 | held (SCC-002) |
| DEP-05-02-008 | DEL-05-02 → DEL-04-01 | **admitted** |
| DEP-05-02-009 | DEL-05-02 → DEL-04-03 | held (SCC-002) |
| DEP-05-02-010 | DEL-05-02 → DEL-05-01 | held (SCC-002) |
| DEP-05-02-019 | DEL-05-02 → DEL-04-02 | held (SCC-002) |
| DEP-05-02-020 | DEL-05-02 → DEL-02-03 | held (SCC-002) |
| (DEL-01-01 register) | No ACTIVE row whose other end is one of the 14. Its deliverable rows go to DEL-01-02…06 (DOWNSTREAM) and DEL-01-05 (UPSTREAM, DEP-01-01-024, held in SCC-001) | — |

Inbound rows from the other first-increment deliverables (read from the consumers' registers):

| Row (arc label where HANDOFF_STATE names one) | Consumer → supplier | Layer |
|---|---|---|
| DEP-02-01-020 | DEL-02-01 → DEL-05-01 | held |
| DEP-02-01-021 | DEL-02-01 → DEL-05-02 | held |
| DEP-02-03-022 | DEL-02-03 → DEL-05-01 | held |
| DEP-04-02-018 (R8-A) | DEL-04-02 → DEL-05-01 | held |
| DEP-04-03-028 (R8-B) | DEL-04-03 → DEL-05-01 | held |
| DEP-09-09-021 (N-C6) | DEL-09-09 → DEL-05-01 | held |
| DEP-03-04-014 / -015 | DEL-03-04 → DEL-05-01 / DEL-05-02 | admitted |
| DEP-09-06-016 / -017 | DEL-09-06 → DEL-05-01 / DEL-05-02 | admitted |
| DEP-02-01-025 (N-16) | DEL-02-01 → DEL-01-01 | admitted |
| DEP-02-03-023 (N-23) | DEL-02-03 → DEL-01-01 | admitted |
| DEP-03-03-013 (N-B4) | DEL-03-03 → DEL-01-01 | admitted |
| DEP-03-04-021 (N-B9) | DEL-03-04 → DEL-01-01 | admitted |
| DEP-04-03-027 (N-15) | DEL-04-03 → DEL-01-01 | admitted |
| DEP-09-06-032 (N-C5) | DEL-09-06 → DEL-01-01 | admitted |

The four new held arcs N-18, N-21, N-24 and X-1 run between DEL-02-01, DEL-02-03, DEL-03-02, DEL-03-03 and DEL-01-04. None has an end in DEL-05-01, DEL-05-02 or DEL-01-01. X-1's supplier DEL-01-04 is a receiver of HOSTING seam S-3 (HOSTING L742); that is an indirect relation only.

---

# File 1 — LOOP_RECEIVING_CONTRACT.md (DEL-05-01)

## 1. Pins

| # | Pin | Where | Verdict | Check and current value |
|---|---|---|---|---|
| 1 | `repo 6e18505e3 (accepted basis)` | L8 | **stale** | Four basis docs differ from that commit (Reference A). Current accepted basis is the docs as amended by SCA-V4-001 and SCA-V4-002 |
| 2 | ScopeOfWork.md `6fbbb580…b568` | L8 | **stale** | Equals the INIT contract at `ddd721a90`. Current `9b2379a14e2c9da4310f62e72d83a6e7506ef37f70c4a38b41d76908bca985ed` (revised at `340ecf341`; RV-2 records prior `6fbbb580…`, revised `9b2379a1…`) |
| 3 | V4-HOST-01 and V4-ARC-11 quoted as "still read 'local … by default; a cloud model only if the user chooses one and provides/supplies an API key'" | L914–916; header L5; UNRESOLVED L1557 | **stale** | Reference A. Both now state no default and OAuth sign-in or API key |
| 4 | "the accepted V4-HOST-02 still reads 'In local operation, a host's agent sends no data to any destination other than the configured model server'" | L928–931; L1044; L1554 | **stale** | Reference A. The accepted text is now the revised text that LOOP quotes at L926. That quote equals PRD L120–126 word for word (script compare; the PRD carries the citation "(D-18; DEC-5)" before the final period) |
| 5 | V4-WF-05 "first half ('holds … the run waits')" and "V4-WF-05 and V4-HI-42 (SETTLED) say the run waits there" | L474–479; header L4; L128; L1558 | **stale** | Reference A. V4-WF-05 now states the phasing itself; V4-HI-42 no longer says the run waits |
| 6 | V4-ARC-12 read as naming only the key ("V4-ARC-12 names the key; applying the same custody to an OAuth sign-in credential is DERIVED") | L934–937 | **stale** | V4-ARC-12 now names "any key or sign-in credential" |
| 7 | SoW REQ-001 quoted "a user-controlled local model server by default … supplied API key" | L1516–1517; L917–918 | **stale** | Current REQ-001 (SoW L52): "local and cloud models as options the person chooses among, with no default … OAuth sign-in or an API key" |
| 8 | SoW AC-001 quoted "local-first selection, explicit person choice plus supplied key" | L1518; L918 | **stale** | Current AC-001 (SoW L60): "the person's choice between local and cloud models with no default, cloud access by OAuth sign-in or an API key …" |
| 9 | "flagged for the next accepted-basis update" (V4-WF-05, V4-HOST-01, V4-HOST-02, SoW wording) | L4, L5, L128, L137, L142, L249, L479, L916–920, L930–931, L1520, L1554, L1557, L1558, L1577 | **stale** (status) | That update is SCA-V4-001, accepted 2026-09-29 (PRD header L10–13) |
| 10 | `RELAY_ANSWERS_SWBPIPE.md` delivered `6f01add3…61c7`; "`RELAY_ANSWERS_SWBPIPE.md` and `FACTS_SQ01_SQ32.md` are unchanged" | L16, L29, L1456; L11 | **stale** | `6f01add3…` is true at `94aa9181b`, `7a1508452` and `f5ceef164`. Current `afb6e063e7e5dfccf8986206f888cf1e2e1c4e7fc3430fdf86db670714fc0e74` (SWBPIPE's `a999f4ba1`, on this branch since `01cb95adb`). The diff is 3 lines (integrity standing adds `not_assessed`; evaluated basis on main; T9 source). V9 Check 2 found no App file stating the superseded wording. FACTS is unchanged (`733fb88a…`) |
| 11 | §10.1 "Grant display states … Register gap (C1)" | L1342 | **stale** | DEP-05-01-025 (DEL-05-01 → DEL-04-02) exists since the 2026-09-29 extraction |
| 12 | VC-04 "C §4.1 and P §9 (v0.3 when supplied)"; VC-09 "Audit every R4-n element against sibling text at the next review" | L1580, L1585 | **stale** | C-v0.6 and P-v0.6 are supplied; the "R4-n elements not yet in sibling text" row was closed at v0.5 (change row L158) |
| 13 | Sibling versions "after R8": EXEC-v0.4, WD-v0.6, WD-EX-v0.6, C-v0.6, P-v0.6, ADAPTER-v0.4, GUIDE-v0.3, ACT-POLICY-v0.6, AS-v0.6, RS-v0.6, PANEL-v0.6, HOSTING-BOUNDARY-v0.6, PIN-SPIKE-v0.1, CA-v0.4, XT-v0.4, RELAY-v0.3, "byte pins in GUIDE-v0.3's input table" | L11 | **current** | Each sibling's line 2 carries that version. GUIDE-v0.3's 18 pins equal today's bytes (all recomputed, including LOOP `246f4636…`) |
| 14 | EXEC-v0.4 `d32be377…76d4`; WD-v0.6 `fce565ed…2f28` | L17 | historical-true | True at `94aa9181b`. Current EXEC `092f248682447df7…`, WD `43a9962f025de384…` (same version labels, edited in place at R8-12) |
| 15 | OWNER_DECISIONS.md `5fd780bf…40b2` "… at `1528a5033`" | L10 | **current**, wording ambiguous | The hash is the file's present bytes and its bytes at `3733b1421`. At `1528a5033` the file was `9903bfe0…` (V10 N-1, still as written) |
| 16 | R8_RESOLUTIONS.md `44bc9a8d…0e6b` | L10 | **current** | Equals present bytes |
| 17 | R8_RESOLUTIONS.md `d4c34233…e7af` (L11), `1770c96e…8d02` (L13) | L11, L13 | historical-true | True at `7a1508452` and `94aa9181b` |
| 18 | INTAKE BRIEFS.md `3e33ba26…7517` | L10, L15 | historical-true | True through `3733b1421`. Current `6f32809d58d150d6…` (B1 section added at `caa4334ca`) |
| 19 | INTAKE_MAP.md `3cc18295…ea33` | L14 | **current** | |
| 20 | INTAKE OWNER_DECISIONS.md `a5ccab0d…e776` at `94aa9181b` | L8 | historical-true | Superseded by pin 15 |
| 21 | FIRST-INCREMENT OWNER_DECISIONS.md `f3f8e5f3…cf81f2e`; at `f05c7e4cd` `a9869129…68ad2c` | L8 | historical-true; **current** | The second equals present bytes |
| 22 | R1…R6 resolutions, V1-A, V1-C, IR1-A/B/C, V2, V3-A, V3-B, V4-A (abbreviated) | L8, L27 | **current** | Prefix and suffix match present bytes of each file |
| 23 | DECISION_BRIEF.html `02d38cb1…4c420e8` | L8 | **defective** | File sha256 is `02d38cb18041c52989d8a2a0b969e6502ce4b25eec85fb0931bbbc100c4420e8`: prefix matches, written suffix `4c420e8` does not (`c4420e8`). Transcription slip; the file has one committed state |
| 24 | LOOP-v0.5 `0ec980b5…d737` at `375c3970c`; LOOP-v0.4 `ffc30483…95934e` | L2 | historical-true | |
| 25 | Older sibling sets at `8fb51f07f` and `c7f5513db` (22 abbreviated hashes) | L21–27 | historical-true | Each matches the named commit; both blocks are marked "superseded for currency" |
| 26 | Run rulings R1…R8-13, DECISION-1…5 | L8–13 | **current** | R1–R7 in `APP-V4-FIRST-INCREMENT-20260928/`, R8 in the intake run. Not cited: the OWNER_DECISIONS of `APP-V4-BASIS-ALIGN-20260928` and `APP-V4-SCA002-20260929`, and the two amendments |
| 27 | Fixture basis "C-v0.4 FX-PIPE-01 (`8fb51f07f`), plus V-GR1, both carried in C-v0.6 §10" | L72–73, L1377–1378 | **current** | C-v0.6 §10 (C L615–801) carries FX-PIPE-01 and V-GR1 |

Stale: **12** (rows 1–12). Defective: 1 (row 23). Ambiguous wording: 1 (row 15).

## 2. ScopeOfWork alignment (SoW `9b2379a1…`)

| SoW item | Where LOOP answers it | State |
|---|---|---|
| OUT-001 receiving contract | §1, §2.1–§2.4, §3, §4, §5.1, §5.1.1, §6, §7, §8, §9 | **Developed** at semantic level. **Partial** for the "native-network destination and credential boundary": rules exist (§5.1.1) but are not joined to the tools subject or the validation order (§5 below) |
| OUT-002 fixtures | §11 (L1390–1430); §5.2; §7 | **Partial.** Case designs only; "no fixture executable" (L1544) because DEP-05-01-024 is UNKNOWN. Revised OUT-002 asks for "allowed, requested and disallowed destinations"; §11's row reads "FX-N1…N13 \| MS-01…MS-13" (L1411) and has no entry for MS-14…MS-22 |
| OUT-003 conformance cases | §5.2 MS-01…22, §7 MC-1…9, §8 RS-1…4, §12, VC-01…09 | **Developed** as definitions; every host observation NOT-OBSERVED |
| OUT-004 allocation account | §10.1–§10.3; UNRESOLVED | **Developed**; one stale cell (pin 11) |
| CLM-001 ownership split | §0 "Who builds what" (L113–116); §10.1 | Developed |
| CLM-002 consumed owners, incl. DEL-04-02 (added by SCA-V4-001) | §10.1, §10.3; O-6 (L1136–1148); §6.2 "Grant in force" | Developed; L1342 still calls it a register gap |
| CLM-003 OI-013 / OI-014 | §10.2; UNRESOLVED L1542–1543 | Developed |
| CLM-004 acts; D2(e), D3 | §9 (L1283–1324) | Developed |
| REQ-001 model choice, destinations, native layer | §5.1 NW-1…NW-7; §5.1.1 NW-8…NW-16; §5.2 | **Developed in rule content.** Every clause of the revised REQ-001 has a rule: no default (NW-1), allow list (NW-8), person-only grant (NW-11), stateless MCP (NW-10), record and show (NW-15), native layer (NW-3, NW-7), outside-process limit (NW-16), governance phase later (L1058–1065) |
| REQ-002 Chat Completions; four subjects; distinct from App path; Pi unselected | §1, §2, §4 | Developed; §4 has six capability rows, three of them open on representation (L890, L891, L893) |
| REQ-003 schema before domain; malformed calls | §6 V-1…V-5, O-1…O-6; §7 | Developed |
| REQ-004 responsiveness, no threshold | §8 | Developed |
| REQ-005 inputs, owners, standing | §10.3 | Developed |
| REQ-006 excluded acts; the sentence on current-phase observation and governance-phase hold machine | §0; §10.1 "Hold machine" row (L1340); §2.4.0; §2.4.4 | Developed; agrees with the revised sentence |
| REQ-007 distinct acts; "a declared workflow checkpoint still requires its specified act" | §2.3, §2.4, §9 | Developed |
| AC-001 / VER-001 | MS-01 (local chosen), MS-12 (signed in), MS-03 (key), MS-04 (no credential), MS-02 (unconfigured), MS-14/15 (allow-listed), MS-16/17/18 (in-work grant), MS-19 (decline), MS-05/06/20 (refusals); VC-01 | Developed. No case is a plain "destination neither allowed nor requested" refusal; the rule is a PROPOSED bullet (L1053–1055). VER-001's "the grants in force" is not named in VC-01's expected result |
| AC-002 / VER-002 | NW-3, NW-6, NW-7; MS-03/06/07/08/12; VC-02 | Developed; labels lag (§3) |
| AC-003 / VER-003 | §1, §2, §4; VC-03 | Developed |
| AC-004 / VER-004 | §6; FX-S1/S2, FX-D1/D1b/D2; VC-04 | Developed |
| AC-005 / VER-005 | §7; FX-M1…M9, FX-V1, FX-U1, FX-O1; VC-05 | Developed; not executable |
| AC-006 / VER-006 | §8; VC-06 | Developed |
| AC-007 / VER-007 | §10; VC-07 | Developed |
| AC-008 / VER-008 | §2.3, §2.4.0–§2.4.4, §9; FX-C1…C15, FX-R1/R2, FX-UNDO; VC-08 | Developed |
| AC-009 / VER-009 | §12; VC-09 | Developed; VC-09 has a stale clause (pin 12) |
| TBD-001, TBD-002 | UNRESOLVED L1542–1543 | Carried |
| TBD-003 (relay route; answers recorded; SQ-29 keeps the basis UNKNOWN; joins deferred) | §13; L1544–1545 | Carried; answer hash lags (pin 10) |

**Places where LOOP contradicts or lags the revised SoW wording:**

1. L8: SoW hash is the INIT contract.
2. L914–920 and G-6 (L1516–1523): quote REQ-001/AC-001 words that are gone and say the SoW wording "is carried to the same update as a proposal". SCA-V4-001 applied it (SoW AX-004).
3. L1557: "SoW REQ-001/AC-001 are carried as a proposal (G-6)".
4. L1342: "Register gap (C1)" for DEL-04-02.
5. §11 L1411: fixture inventory stops at MS-13 while revised OUT-002 names destination fixtures.
6. L30 Receivers: lists DEL-02-01, DEL-05-02, DEL-02-03, the relay file and SWBPIPE. The registers and DAG-003 now also have DEL-04-02 (R8-A), DEL-04-03 (R8-B), DEL-03-04, DEL-09-06 (as consumer of the receiving requirements) and DEL-09-09 (N-C6) as consumers. §10.1's networking row (L1335) names ACT §2.7, AS §3, RS R15 and PANEL §3.8, so the content reaches them; the Receivers line does not say so.

No rule in LOOP contradicts a revised SoW obligation. The lag is in pins, notes and inventory.

## 3. Amended basis

| Requirement | LOOP text | Agreement |
|---|---|---|
| V4-HOST-01 | NW-1 (L911–913), §5.1 states (L902–908), MS-02, MS-12 | **Agrees in rule.** The "Accepted-basis note" (L914–920) and header L5 are now false |
| V4-HOST-02 | NW-2 quote (L926); §5.1.1 | **Agrees; quote is the accepted text.** The note at L928–933 is now false |
| V4-ARC-11 | NW-1 | Agrees |
| V4-ARC-12 | NW-3 (L934–937), NW-6, NW-7 (L946–948), §5.1.1 PROPOSED bullet (L1053–1055) | **Wording lags.** Amended V4-ARC-12 states the native layer "allows only … records every destination contacted, and holds any key or sign-in credential outside the interface's script". LOOP still labels the sign-in custody DERIVED and the enforcement point and credential exclusion PROPOSED |
| ARCH §4 property (amended) | NW-8…NW-16 | Agrees item by item. ARCH says "named destinations within each category"; LOOP reads the two levels as alternatives and holds N-OPEN-4. ARCH's "a silent switch to another model or provider … stay off" covers NW-5, which LOOP labels PROPOSED |
| V4-WF-05 | §2.4 lead (L473–480); §2.4.0 LP-1…LP-10; §2.4.4 | **Intent agrees; wording differs in two places.** (a) L474–479 describes the old sentence order and a pending flag. (b) See the finding below |
| V4-HI-42 | LP-6 (L525), C-1 (L629–635) | Same two points |
| V4-HI-70 | E-4 (L442–463) | Agrees in content: E-4 lists "destinations contacted, destination grants and declines, and outside processes". It cites "R8-13; RS R15", not the amended V4-HI-70 |
| V4-EXM-22 | FX-C1…C15 two-part; VC-08 | Agrees on "stopping … examined only for a workflow that takes up the governance phase". See the finding below for "requests a human act" |
| V4-EXM-23 | MS-01 cites "V4-EXM-01/23" (L1074) | Agrees. MS-14…MS-22 carry no V4-EXM-23 citation although the amended text names their content (decline wording, outside process) |
| "local-first" | Only as a quotation of the old SoW (L918, L1518) | No rule uses it |

**Finding (wording, not intent): the act request at a Phase-1 arrival.**
- The amended basis states three times that, in the current phase, the required act is *requested* at the checkpoint: V4-WF-05 first sentence; V4-HI-42 ("a checkpoint's required act is requested and recorded as done only when the person performs it"); V4-EXM-22 ("A workflow checkpoint requests a human act").
- R8-1 (written before the amendment) puts in force only "A human act is recorded as done only when the person performs it (V4-WF-05, second half)".
- LOOP follows R8-1. LP-1 (L520): the agent "manages any pause … for example by issuing an A8 request … where its plan says so". LP-3 (L522): the loop "records 'checkpoint reached'". LP-5 (L524): "V4-WF-05 second half". TL-5 (L386–387): "The loop records no A8 automatically." §2.3 has no "act requested" event; the change row at L205 names one. In the governance-phase text the request is a fact ("The act request is re-issued", L697).
- So LOOP states no Phase-1 rule that the required act is requested when a checkpoint is reached. EXEC L634 and WD L538 do say "act request issued" / "the act is requested" at arrival, and WD S-F (L163) and EXEC E-B (L170) put only the recording clause in force.
- **Inference:** the amended V4-WF-05 keeps "is requested" in force now, so the Phase-1 rules need one sentence on who requests the act at arrival and how it is recorded. This needs an integrator ruling across LOOP, PANEL, EXEC and WD. It does not require a hold.

## 4. Open items

Counted once each. "Closed by record" means the file still lists it as open.

| # | ID (location) | What is open | Owner / point of need (as the file states) | Class |
|---|---|---|---|---|
| 1 | Revised V4-HOST-02 (L1554) | Accepted text awaiting update | Owner / next accepted-basis update | **NOW** — closed by record: PRD L120–126 (SCA-V4-001) |
| 2 | V4-HOST-01 / V4-ARC-11 wording (L1557) | Same | Same | **NOW** — closed: PRD L116–119; ARCH L165 |
| 3 | V4-WF-05 first half (L1558) | Same | Same | **NOW** — closed: PRD L254–264; HI L139–144 |
| 4 | G-6 (L1516) | SoW REQ-001/AC-001 wording | — | **NOW** — closed: SoW L52, L60 (`340ecf341`) |
| 5 | §10.1 "Register gap (C1)" (L1342) | DEL-04-02 edge | Register owner | **NOW** — closed: DEP-05-01-025 |
| 6 | G-4 (L1509) | "the v0.6 pair needs an independent check" (one executor wrote LOOP and PANEL) | — | **NOW** — V9 and V10 checked the R8 and R8-13 content across files; neither is a pair comparison of the whole v0.6 texts. A reviewer node in this pass can do it |
| 7 | Hold machine confirmation, recording content (L1548) | EXEC §4 is PROPOSED (W7); LOOP adopts C-4, C-7, C-8, §2.4.1 "as proposed" | DEL-02-03, "at the next integration review" / before host-loop implementation | **NOW** for the Phase-1 recording content (EXEC-v0.4 §2.1 closing paragraph, L226–232; R8-11 item 1). Its hold content is item 31 |
| 8 | T-OPEN-1 (L1561), U-P9 (L1552), G-3 (L1507) | Whether valid sibling calls run beside a malformed one; grouping | This owner with DEL-03-02 and host owner / before FX-M8 | **NOW** for the receiving rule: MC-8 (L1241) and P §3.1 rule 5 (P L162–167) already agree and are both PROPOSED. Representation is item 27 |
| 9 | N-OPEN-1 (L950; MS-11 held) | What counts as a "user-controlled local" endpoint | App/shared embedded-integration owner with SWBPIPE owner / before endpoint cases are final | **NOW** — *inference*: under the amended V4-HOST-01/02 the selected model service is allowed whether local or cloud, so the question reduces to the class label in the destination record (as HOSTING §8.3 L820–821 does for the App). The integrator can rule it from PRD L116–126 |
| 10 | PROPOSED labels NW-4…NW-7 (L938–948) and the two §5.1.1 PROPOSED bullets (L1052–1057) | Standing of the rules | This file's proposals | **NOW** — NW-6, NW-7 and the enforcement bullet are stated by amended V4-ARC-12; NW-5 by ARCH §4 (always-off item). NW-4 and the outside-process start rule stay PROPOSED |
| 11 | DEP-05-01-024, supplier (L1544; §10.1 L1344; §10.3 L1371) | No supplier of the model-interface basis is identified (register target UNKNOWN). SWBPIPE: none exists or is selected (SQ-29) | "UNKNOWN supplier; App/shared embedded-integration owner receives or agrees" / at fixture and conformance use | **OWNER** — choice: the App/shared side names a published Chat Completions basis for its own fixtures now, or the fixtures stay unexecutable until SWBPIPE's D-58 decision |
| 12 | N-OPEN-4 (L959; L1006) | Whether switching a category off suspends its named entries | "the owner for N-OPEN-4" / before destination cases are final | **OWNER** — choice: named entries are independent of the switch (LOOP's interim reading, MS-15), or subordinate to it (ARCH: "named destinations within each category") |
| 13 | U-E4 (L1567; L657–660) | SP-6 alternative: count prior acts bound to current content | Owner / before hold-machine implementation | **OWNER** — choice: only acts captured at or after the arrival count (SP-6, adopted as PROPOSED), or a prior act on unchanged content counts. In Phase 1 it changes a record label only (FX-C4b, FX-C11b) |
| 14 | U-03 (L1568; L713–716) | Whether an act on the lapsed referents alone satisfies after a partial lapse | DEL-04-01 with Owner / at its point of need | **OWNER** — choice as stated |
| 15 | OI-021 (L1546; FX-NP1 HELD; A-4 L1307) | First connected operation; operation-specific reserved additions; OP-C11 class | Owner via outside SWB session and App/shared owner / before connected SoW and execution | **OWNER** — choice among SWBPIPE's recorded candidates (SQ-04). Exercised through the SWBPIPE session, so it also waits on DECISION-3 |
| 16 | OI-013 (L1542) | Loop placement, parsing, persistence, panel assembly | Shared contract owner with SWB implementation owner / before shared/host implementation boundary contracts | **HOST** |
| 17 | DEP-001 host evidence, Q-1…Q-7 (L1545); FX-C9 governance value AWAITING INPUT | No candidate, evidence or commitment | SWBPIPE / when the owner resumes UI-SUCCESSOR | **HOST** |
| 18 | C U-C5 (L1549; E-5 L464–466) | Findings location | DEL-03-01 with host owner / before E-5 route (b) | **HOST** |
| 19 | C U-C3 / R2-13 (L1550) | Host confirmation of the staleness rule | Host owner with DEL-03-01/03-02 / before FX-D2, FX-O1 | **HOST** |
| 20 | C U-C6 (L1551) | Entry-version mismatch | Host input / before FX-D series | **HOST** |
| 21 | U-P1 / TBD-002 (L1552) | Resubmission mechanics after outcome unknown | DEL-03-02 with DEL-05-01 and host owner / before FX-O1 | **HOST** |
| 22 | N-OPEN-3 (L955) | Which traffic of a host operation counts as the agent's | App/shared owner with SWBPIPE owner | **HOST** |
| 23 | Seat role mapping U-09 (L1563) | Seat meaning in a host | DEL-02-01 with SWB owner and DEL-02-04 / before record fixtures | **HOST** |
| 24 | SWBPIPE embedded direction, D-58 (L1560) | SWBPIPE's plan predates D-20 | SWBPIPE / when UI-SUCCESSOR resumes | **HOST** |
| 25 | Consequence vocabulary (L1547) | Not defined | DEL-04-01 with host policy owner / before class assignment | **HOST** (ACT's item; S1-A's row) |
| 26 | FX-D3 meaning per C U-C2 (L1401) | Generation-change refusal meaning | — | **HOST** (C's item; S1-B's row) |
| 27 | DEP-05-01-024, representation (§4 L890–893; MC-6 L1239; MC-7 L1240; MC-8) | Fragmented tool-call representation; termination reason values; several calls per response; how "no arguments" is expressed | As item 11 | **SPIKE** — read one published Chat Completions reference and observe one local OpenAI-compatible server for these four points. Needs a local server or network access; neither is available in this run |
| 28 | N-OPEN-5 (L961; L1014–1015) | Evidence that an MCP server follows the stateless revision 2026-07-28 | App/shared owner / before destination cases are final | **SPIKE** — read the published revision and name the element that evidences conformance. Needs the specification text |
| 29 | OI-014 (L1543; §10.2) | Shared placement | App/shared contract owners / before structural/production allocation | **LATER** — §10.2 establishes no repeated responsibility and there is one identified consumer (OI-005 open) |
| 30 | Governance phase taken up (L1559) | When enforced checkpoints apply | Owner, per workflow | **LATER** (DECISION-4 D4-1) |
| 31 | Hold machine hold content (part of L1548); D6 (L1566) | App-side holds; re-hold | Owner / with the governance phase | **LATER** |
| 32 | Network-destination governance phase (L1556) | Organization-locked lists; enforced sandboxing | Owner, when taken up | **LATER** (DECISION-5) |
| 33 | R-OPEN-1 (L1562) | Numeric responsiveness criterion | Owner, if wanted | **LATER** — SoW REQ-004 forbids an unsourced threshold |
| 34 | N-OPEN-2 (L951) | Which endpoints a cloud sign-in service comprises | App/shared owner with SWBPIPE owner | **LATER** — no provider is selected (L895) |

Counts: NOW 10, OWNER 5, HOST 11, SPIKE 2, LATER 6. Total 34.

## 5. Design depth against the 60% description

Contributions LOOP exchanges: to DEL-05-02 (messages, tools, events, checkpoints, settings, destination surfaces); to DEL-02-03 (arrival observation, subject binding, loop events); to DEL-02-01 (host consumer needs); to DEL-04-02 (allow list, in-work grants, contacted-destination record); to DEL-04-03 (destination events, run-record inventory); to DEL-03-04, DEL-09-06, DEL-09-09 (receiving requirements). It consumes C, P, WD, EXEC, ACT, AS, RS.

| Aspect | What the file has | What is missing |
|---|---|---|
| Interfaces | Four-subject boundary with element tables (§2.1 L273–285; §2.2 L302–308; §2.3 L396–432; §2.4 L482–495). Validation order V-1…V-5 (L1104–1110). Dispatch record, ten elements (L1152–1163). Result classes TL-2 (L353–364). Capability table (§4) | (a) No statement of the loop ↔ native-layer exchange for a destination: what the loop presents, what comes back, and where a pending request or a decline sits among TL-2's "four tool-result classes, never collapsed". (b) No place for destination-reaching tools in the tools subject (see "Structural" below). (c) No delivery statement for events to the panel (order across reload, replay) beyond M-1 and E-1…E-5. (d) Model-interface representation (DEP-05-01-024) |
| States | Completion standing (6, L278). Dispositions (6, L497). Grant states (7, L1136–1143). Model setting (5, L902–908). A12 control relations (L783–788). Tool-call progress as events | No state list for an in-work destination request (asked, pending, granted by scope, declined, refused at boundary). No statement of what happens to a pending request at run end, interruption or turn cancel. "This run" expiry is a rule (NW-11) without a state |
| Data | Semantic elements and identities throughout; destination elements table (L988–995) | "Destination" has no identity definition: MS-14…MS-22 use W-1, A-1, M-1, D-1 without saying whether a destination is a host name, an origin or a URL prefix, or how a destination maps to a category. Not listed as open. Scope of correlation-identity uniqueness (MC-7) is PROPOSED |
| Operating sequences | One turn (§3 L865–880). Checkpoint evaluation (§2.4.1). Retry, resubmission, re-draft (§6.3). 22 endpoint cases (§5.2) | The turn sequence places the destination check only on the model request (L867). No sequence for an agent call that reaches an allowed destination, or for the in-work request relative to V-1…V-5 and dispatch. No sequence for turn cancel with calls already dispatched (RS-3 covers the stream only) |
| Failure behaviour | Malformed calls MC-1…MC-9; outcome unknown (class 4); model interface failure event; no fallback (MS-08, MS-09, NW-5); interruption and "interruption not recovered" (L592–599) | Native layer unable to decide or to write the destination record (V4-ARC-12 says it records every contact); host route unreachable before any outcome; no panel attached; event or record write failure |
| Verification | VC-01…VC-09 (review-type); fixture inventory §11; evidence labels §12; two-part checkpoint fixtures | Nothing executable. §11 omits MS-14…MS-22. No test double is described (the label FIXTURE-EXECUTED exists, L1437) |

**Structural choices still open:**

1. **Where destination-reaching tools live (found by this survey; not listed in the file).** *The file states:* a tool offering is "one catalog entry with all C elements 1–9" (L305); "The loop never invents a tool without a catalog entry" (L350); V4-ARC-13 is "Tools from the host's capability catalog". *It also states:* categories "web access, MCP servers and other APIs" (L990), "the agent's tool fetches web destination W-1" (MS-14), MCP servers started for the agent (L995, MS-15, MS-21). *Checks:* §2.2, §3 and §6 do not mention web access, MCP or outside processes (grep); C and P contain neither "destination not allowed" nor "outside process" (grep counts 0); ACT, AS and RS do. *Inference:* the design has rules for destinations but no tool subject that reaches them. Either such tools are host catalog entries (then C needs to say how an entry declares external contact, and C §4.1 / P §9 need the decline and pending outcomes), or they are a second tool source beside the catalog (then TL-1, V-2 and the class element need a counterpart). Either answer changes LOOP §2.2, §3 and §6 and at least C and P. This is the one item in my row that could force a restructuring of a consumer.
2. DEP-05-01-024 (items 11, 27): §4, MC-6, MC-7, MC-8 and every fixture wait on it.
3. OI-013 / OI-014 (items 16, 29): placement and any shared parse or schema checker (§10.2 candidates (a), (b)).
4. SP-6 / U-E4 (item 13): changes FX-C4b, FX-C11b and PANEL W-5c.
5. N-OPEN-4 (item 12): changes NW-8, MS-15, MS-18 and PANEL ND-1.

## 6. Joins (ACTIVE rows to the 14)

| Row | Contribution named by the row | DAG-003 | Supplier's Design holds it, in a form LOOP uses? |
|---|---|---|---|
| DEP-05-01-014 → DEL-03-01 | Catalog/read-basis schemas and catalog identity for argument validation and fixtures | held | **Yes.** C §2 catalog edition (C L90, which names DEL-05-01's term), §3 elements, §3.1 five class values (C L151–156), §4.1 results incl. loop-side *not offered* (C L241–245), §5.3 subject content identity, §10 FX-PIPE-01 and V-GR1. Used at LOOP §2.2, TL-1/TL-2, V-2, §11. No schemas exist in C (semantic only), so "argument validation" has meaning, not a schema |
| DEP-05-01-015 → DEL-03-02 | Proposal/validation/outcome meaning | held | **Yes.** P §9 taxonomy (P L550–573), §3.1 identities and rule 5, §3.3 origin and carriage assurance (P L181–196, naming "DEL-05-01 §6.2"), §4.3 item-left events, §13 "Provide to DEL-05-01" (P L707). Used at LOOP TL-2, §6.2, §6.3, C-6, MC-8 |
| DEP-05-01-016 → DEL-02-01 | Portable workflow/role/checkpoint declarations | held | **Yes.** WD §4.3.0 CG-1…CG-7 (WD L327–372), §4.3.1 incl. `governed`, §4.3.6, §4.3.7, §5.3 SEAT, §6.1, §6.4; WD §8 lists what DEL-05-01 receives (WD L911). Used at LOOP §2.1, §2.4 |
| DEP-05-01-017 → DEL-02-03 | Current-phase recording; governance-phase hold machine and hold-support values | held | **Yes.** EXEC §2.1 PH-1…PH-10, §2.2 GV-1…GV-5, §3.6, §4; EXEC §9.2 "Provided to DEL-05-01" (EXEC L1209). Used at LOOP §2.4.0, §2.4.3, §2.4.4 |
| DEP-05-01-018 → DEL-04-01 | Operation-policy / human-act distinctions | **admitted** | **Yes.** ACT §2.1 A1–A14, §2.3 act-declined, §2.7 network-destination grant (ACT L464), §4.5, §5.3, §6. Used at LOOP §9, O-4, NW-11, C-2 |
| DEP-05-01-019 → DEL-04-03 | Human-act / run-record meanings and format | held | **Yes.** RS §4 inventory incl. R11, R15 (RS L190–194), L-12. Used at LOOP E-4, NW-15, NW-16 |
| DEP-05-01-020 → DEL-05-02 | Panel receiving needs for the allocation account | held | **Implicit.** PANEL has no list of "what the panel needs the loop to emit"; its needs appear as "Consumed definitions" cells (PANEL L242, L255, L272) and §3.8's references to NW-8…NW-16. LOOP §10.3 records "Panel needs \| DEL-05-02 \| PANEL-v0.6, same executor" (L1370) |
| DEP-05-01-025 → DEL-04-02 | Grant display states and standing exchange, as the grant in force per dispatch | held | **Yes.** AS §3 states incl. *effective (policy default)*; AS Receivers name "DEL-05-01 (grant in force per dispatch)" (AS L12). Used at LOOP O-6, §6.2. AS L12 and U-15 (L582) still call the register edges "pending at C1" |

Inbound, where LOOP is the supplier:

| Row | What the consumer asks | Does LOOP offer it? |
|---|---|---|
| DEP-04-02-018 (R8-A) | Allow list, in-work grants, contacted-destination record | Yes: §5.1.1; §2.3 destination events. AS §3 cites "LOOP §5.1.1; PANEL §3.8 ND-5" (AS L214) |
| DEP-04-03-028 (R8-B) | Destination contacted / grant / declined events | Yes: §2.3 L401–406; E-4. RS R15 matches, incl. the three refusal reasons (V10 Check 2) |
| DEP-02-03-022 | Arrival observation, subject binding, loop events | Yes: §2.4.1, §2.4.2, §2.3 |
| DEP-02-01-020 | Minimal-loop consumer requirements | Yes: §2.4 element table and §10.3 |
| DEP-09-09-021 (N-C6) | Embedded-loop receiving contribution for the embedded surface | Yes as definition; no evidence |
| DEP-03-04-014, DEP-09-06-016 | Loop/model receiving requirements | Yes; GUIDE pins LOOP `246f4636…` |

**Disagreements between the two files' statements of one exchange:** none found in rule content. Three lags: RELAY answers "unchanged" in LOOP L11 against GUIDE's `afb6e063…` pin; AS and LOOP both still describe their mutual register edge as pending; C L230 says DEL-05-01 adopts C §4.1 "as of C-v0.5 / P-v0.5" while LOOP cites v0.6.

## 7. Carried review items that name LOOP

| Item | State | Evidence |
|---|---|---|
| V6 m-1, m-3…m-7 | None names LOOP | V6 residual table: GUIDE, RELAY, EXEC, WD-EX, WD |
| Closeout D5-1-1 (EXEC-v0.2 citations) | Fixed | Header L11, L17; §2.4 L501; G-5 closed L1512 |
| Closeout D5-1-2 (stale §10.1/§10.3 standing) | Fixed, one cell left | §10.3 heading "Standing at v0.6 (R8)" L1361; L1342 still "Register gap (C1)" |
| Closeout D5-1-3 (R5-n row; RELAY-v0.2) | Fixed | L1569; §13 L1446–1449 |
| Closeout S5-1-1…S5-1-4, R5-1-1 | Applied by SCA-V4-001 and the register update | SoW CLM-002, REQ-006, CLM-004, TBD-003; DEP-05-01-025 |
| Closeout R5-1-2 (mirror of DEP-01-05-014), R5-1-3 (DOWNSTREAM relay row) | Open, register matters | DEL-05-01 register has 12 EXECUTION rows, none to DEL-01-05 or DOWNSTREAM. Not a Design matter |
| Closeout "independent check of the LOOP/PANEL pair (G-4)" | Open | G-4 L1509 |
| V9 N-1 (§2.4 *on negative decision* row unlabelled) | Fixed | L491; change row L141 |
| V9 N-3, N-7 | Do not name LOOP | INTAKE_MAP; GUIDE |
| V10 S-1 ("confirmed by the owner") | Fixed | L980, L1555 |
| V10 S-2 (attribution of the revised text) | Fixed in the rule | L923 "in the recorder's wording confirmed by the owner". Change row L142 still says "The owner's revised text" (history; V10b noted it) |
| V10 N-1 ("at `1528a5033`") | Open | L10 unchanged; see pin 15 |
| V10 N-4 (MS-15 rests on the interim NW-8 reading) | Open | MS-15 L1088 has no N-OPEN-4 mark |
| V10 N-5 (R4-4 PROPOSED cited under a SETTLED heading) | As written; V10 asked for nothing | L1023–1024 |
| V11–V16 | Name no Design file of this row; they carry "the 17 Design re-pins" as deferred (BASIS-ALIGN DECISION-8; V13 F4; HANDOFF_STATE open matters) | grep |

## 8. Recommended work on LOOP in this pass

1. Re-pin the header: basis as amended (name the amendments and the docs' hashes), SoW `9b2379a1…`, RELAY answers `afb6e063…` with V9's finding, corrected DECISION_BRIEF suffix, unambiguous OWNER_DECISIONS commit. [§1; §7]
2. Replace every "flagged for the next accepted-basis update" with a citation of the amended text; delete the two accepted-basis notes; close UNRESOLVED L1554, L1557, L1558 and G-6; relabel NW-3, NW-5, NW-6, NW-7 and the enforcement bullet from the amended V4-ARC-12 and ARCH §4; cite V4-HI-70 at E-4 and V4-EXM-23 at MS-14…MS-22. [§1; §3; §4 items 1–4, 10]
3. State the Phase-1 act request at arrival, in the amended V4-WF-05 / V4-HI-42 wording, after an integrator ruling shared with EXEC, WD and PANEL. [§3]
4. Align with the revised SoW: L1342; Receivers line; §11 entries for MS-14…MS-22; one case for a destination neither allowed nor requested; VC-01 "grants in force"; VC-04 and VC-09 clauses. [§2; §6]
5. Develop the destination interface: tool subject for destination-reaching tools, position of the destination check in §3 and §6, request states and their relation to TL-2, destination identity, failure rows. Do it with the C and P owners, because the answer may add an entry element or an outcome. [§5]
6. Rule N-OPEN-1 and release MS-11; mark MS-15 per V10 N-4; put N-OPEN-4 to the owner. [§4 items 9, 12; §7]
7. Rule T-OPEN-1 / MC-8 with P §3.1 rule 5 if the integrator agrees. [§4 item 8]
8. Add the missing failure rows and a short state summary for run, turn, tool call and destination request. [§5]
9. Independent pair check of LOOP and PANEL after the edits. [§4 item 6]

**Not in this pass, and why:**
- Host conformance, SWBPIPE joins, relaying the DECISION-5 rules (DECISION-3).
- Developing the governance phase further (DECISION-4 D4-1; it is retained, not advanced).
- Selecting a provider, server, wire field or protocol version (SoW REQ-002; L895).
- Executing fixtures (no model-interface basis).
- OI-013 / OI-014 decisions; any SoW or register edit (brief, common rules).

---

# File 2 — PANEL_RECEIVING_CONTRACT.md (DEL-05-02)

## 1. Pins

| # | Pin | Where | Verdict | Check and current value |
|---|---|---|---|---|
| 1 | `repo 6e18505e3 (accepted basis)` | L8 | **stale** | Reference A |
| 2 | ScopeOfWork.md `5c554956…40cb` | L8 | **stale** | INIT contract at `ddd721a90`. Current `beb9c66c38161cbb00d1040e294aa9dfd04af953f9bf539121fcda44356dc82c` (`340ecf341`) |
| 3 | V4-WF-05 "first half … flagged for the next accepted-basis update" | L4, L95, L854 | **stale** | Reference A |
| 4 | V4-HOST-01 "by default … API key" wording | F-9 L822–825; L104; L856 | **stale** | Reference A |
| 5 | "V4-HOST-02 as revised by DECISION-5, flagged for the next accepted-basis update" | L6, L240, L857 | **stale** (status) | The revised text is the accepted text |
| 6 | RELAY answers delivered `6f01add3…61c7`; "unchanged" | L16, L28, L752; L11 | **stale** | As LOOP pin 10. PANEL cites SQ-01, -02, -05, -07, -09, -10, -18…-24, -28; the three changed lines concern none of the statements PANEL makes (V9 Check 2) |
| 7 | SoW-state statements: "This consumption is not in this SoW's CLM-002 or register" | L480; F-3 L805–807; L864 | **stale** | SoW CLM-002 (L35) names DEL-04-02; DEP-05-02-019 exists |
| 8 | Sibling versions after R8; "byte pins in GUIDE-v0.3's input table" | L11; VC-01 L875 | **current** | As LOOP pin 13; GUIDE pins PANEL `dd71e11d…` |
| 9 | EXEC-v0.4 `d32be377…`, WD-v0.6 `fce565ed…` | L17 | historical-true | As LOOP pin 14 |
| 10 | OWNER_DECISIONS `5fd780bf…` "at `1528a5033`"; R8_RESOLUTIONS `44bc9a8d…` | L10 | **current**; first is ambiguous | As LOOP pins 15, 16 |
| 11 | R8_RESOLUTIONS `d4c34233…`, `1770c96e…`; BRIEFS `3e33ba26…`; INTAKE OWNER_DECISIONS `a5ccab0d…` | L10–15, L8 | historical-true | As LOOP pins 17, 18, 20 |
| 12 | INTAKE_MAP `3cc18295…`; R1…R6, V1-A, V1-C, IR1-A/B/C, V2, V3-A/B, V4-A | L14; L8; L26 | **current** | |
| 13 | DECISION_BRIEF.html `02d38cb1…4c420e8` | L8 | **defective** | Same suffix slip as LOOP pin 23 |
| 14 | PANEL-v0.5 `ac47abf0…ebb4` at `c6f81a4f2`; PANEL-v0.4 `cb71bc4b…e84419` | L2 | historical-true | |
| 15 | Basis list "V4-EXM-20–22" and "V4-HOST-01/04/05/06" | L8 | Incomplete | §3.8 rests on V4-HOST-02 and is examined by V4-EXM-23; neither is in the Basis line |

Stale: **7** (rows 1–7). Defective: 1.

## 2. ScopeOfWork alignment (SoW `beb9c66c…`)

| SoW item | Where PANEL answers it | State |
|---|---|---|
| OUT-001 panel interface and receiving requirements | §1–§5; §3.1–§3.4 tables; §3.5; §3.6; §3.8 | **Developed** |
| OUT-002 allocation account | §6 (L620–648) | **Developed** as an account: six candidates, agreement "None" on each |
| OUT-003 receiving cases, then candidate-bound results | §7, PC-01…PC-37 with sub-cases | **Partial**: "All cases are DESIGNED — UNEXECUTED" (L652) |
| OUT-004 reusable components | §6 "OUT-004 conditional state" (L631–633) | **Only named**: the conditional state, as AC-006 allows |
| CLM-001, CLM-003, CLM-005 | §0; §6 boundary; §8 | Developed |
| CLM-002 (revised: adds DEL-04-02; adds DEL-02-03 recording meanings and governance-phase values, owner item O-12 "Direct") | §3.6 (AS); §3.2 and §3.5 (EXEC) | Developed in content; three places deny the DEL-04-02 part (pin 7) |
| CLM-004 (revised: D2/D3 rule the policy) | §1 permission layer; W-6 (L611–614) | Developed |
| REQ-001 four interactions mapped to "identified, independently compared" definitions | "Consumed definitions" rows (L242, L255, L272); §3.4 table | Developed. §7 preamble still says "The sibling v0.3 elements were confirmed by V2" (L653) |
| REQ-002 host tables and views; no private surface | §2 P-1…P-3; §3.3; §3.4; §4 H-1…H-6 | Developed |
| REQ-003 distinct acts; accept wording; faithful record; lapse; consumes D2/D3 without deciding OI-021 | §3.5 W-5a…W-5g; §5 W-1…W-7; K-1…K-4 | Developed |
| REQ-004 repeated responsibility; OI-013 and OI-014 separate | §6 | Developed |
| REQ-005 cases against identified inputs; claims only on evidence | §7 accounting states (L659–666) | Developed |
| REQ-006 excluded acts (revised: adds DEL-04-02 and DEL-02-03) | "Responsible" rows; §6; VC-07 | Developed; pin 7 contradicts the revised list |
| AC-001 / VER-001 | VC-01 | Developed |
| AC-002 / VER-002 | PC-06, PC-09, PC-12; rejection cases PC-13, PC-14, PC-15; VC-02 | Developed, unexecuted |
| AC-003 / VER-003 | PC-16…PC-29; positive record PC-18; independent act PC-19; VC-03 | Developed, unexecuted; PC-23, PC-28 HELD |
| AC-004 / VER-004 | §6; VC-04 | Developed |
| AC-005 / VER-005 | §7 states; VC-05 | Developed |
| AC-006 / VER-006 | §6; VC-06 | Developed |
| AC-007 / VER-007 | VC-07 | Developed. VER-007's "schema and boundary-owner validation" is a SoW check, not in the Design file |
| TBD-001, TBD-002 | L844–845 | Carried |
| TBD-003 (revised: names SQ-01, SQ-02 and the host loop's behaviour; relay route; joins deferred) | §8; L847 | Carried; answer hash lags |
| TBD-004, TBD-005 (revised: ruled by D2 and D3) | W-6; §1 | Agrees |
| P/OQ-11 paragraph (revised: tracked as OI-021) | L846 | Agrees |

**Contradictions and lags against the revised SoW:**

1. L8: SoW hash.
2. L480, F-3 (L805–807) and L864 say the DEL-04-02 consumption is outside the SoW and register. It is inside both now.
3. F-4 (L808) and F-5 (L809–810) route matters "to C1" that SCA-V4-001 has applied (SoW L87; TBD-003 L83; DEP-05-02-016, DEP-05-02-011).
4. L29 Receivers: names DEL-02-01 and DEL-05-01. The registers also have DEL-03-04 and DEL-09-06 (admitted) as consumers.
5. **§3.8 has no SoW obligation (found by this survey).** *Checks:* the DEL-05-02 SoW contains the word "destination" 0 times; its AX-004 applies DECISION-1, -3 and -4, not DECISION-5; its scope items are SOW-019 and SOW-020; the scope item that carries "recorded and shown" is SOW-017, assigned to DEL-05-01 only (`_Decomposition/ScopeLedger.csv`). *The file states:* §3.8 (ND-1…ND-5), PC-30…PC-37 and F-11 are part of PANEL, serving VER-001/002/003. *Inference:* the panel surfaces for network destinations are design that DEL-05-02's contract does not ask for. They can be read as the panel's receiving of DEL-05-01's loop events under CLM-002 and REQ-001, but the SoW does not say so.

## 3. Amended basis

| Requirement | PANEL text | Agreement |
|---|---|---|
| V4-HOST-01 | §3.1 model setting indicator (L240); PC-03b, PC-03e | Agrees; F-9 and L856 are obsolete |
| V4-HOST-02 | §3.1 (L240); §3.8 | Agrees with the amended text and ARCH §4. PANEL paraphrases and does not quote (V10 Check 1) |
| V4-ARC-11 / V4-ARC-12 | Not cited. ND-1 "Every edit is the person's A12 … captured by the host's control"; "Host owner: the control, capture, native enforcement" (L545) | Agrees |
| V4-WF-05 | §3.2 "Checkpoints as plan guidance" (L252); §3.5 Phase-1 paragraph (L311–325) | Agrees on no hold, no *unsupported* for a hold reason, acts only when performed. Header L4 and L854 are obsolete. **Same act-request gap as LOOP §3:** W-5a (L327–352) shows the arrival with the required act; §3.1 shows "A8 requests, shown only when issued"; no Phase-1 sentence says the required act is requested at arrival. The governance text has "The act request is re-issued" (L413) |
| V4-HI-42 | §3.3 "Direct autonomy and checkpoints" (L271) | Agrees with "reserved acts … still bind"; same request point |
| V4-HI-70 | §3.2 "associated with the selected identity tuple (V4-HI-70)" (L254); ND-4 "References … to the run record (RS R15)" | Agrees; ND-4 does not cite the amended V4-HI-70 |
| V4-EXM-22 | PC-21…PC-21i, PC-22, PC-24 two-part | Agrees on the governance-only stop |
| V4-EXM-23 | Not cited | PC-30…PC-37 cover its content (decline wording PC-35; outside process PC-37) without the citation |
| "local-first" | Not used | — |

## 4. Open items

| # | ID (location) | What is open | Owner / point of need | Class |
|---|---|---|---|---|
| 1 | V4-WF-05 first half (L854) | Basis update | Owner | **NOW** — closed by record (Reference A) |
| 2 | V4-HOST-01 wording (L856); F-9 (L822) | Same | Owner | **NOW** — closed |
| 3 | Revised V4-HOST-02 (L857) | Same | Owner | **NOW** — closed |
| 4 | DEL-04-02 consumption, F-3 (L805; L864; L480) | SoW and register edge | Register owner / C1 | **NOW** — closed: SoW L35, L52; DEP-05-02-019 |
| 5 | F-4 (L808) | OQ-11 and OI-021 are one matter | C1 | **NOW** — closed: SoW L87; DEP-05-02-016 |
| 6 | F-5 (L809) | Register the capture-evidence dependency | C1 | **NOW** — closed: SoW TBD-003 L83; DEP-05-02-011 |
| 7 | F-1 (L800) | Independent check of the v0.6 pair | — | **NOW** — as LOOP item 6 |
| 8 | Hold machine confirmation, recording content (L850) | W-5b/c/e/f/g "follow it as proposed" | DEL-02-03, next integration review | **NOW** — as LOOP item 7 |
| 9 | OI-021 / OQ-11 (L846; PC-23, PC-28 HELD) | First connected activity; reserved additions; OP-C11 class | Owner via outside SWB session and App/shared owner | **OWNER** — as LOOP item 15 |
| 10 | U-E4 (L851; W-5c L380–384) | SP-6 alternative | Owner / before hold-machine implementation | **OWNER** — as LOOP item 13; visible cost PC-21i |
| 11 | U-03 (L852) | Partial-lapse purpose | DEL-04-01 with Owner | **OWNER** |
| 12 | LOOP N-OPEN-4 (L859) | Category switch and named entries | As LOOP | **OWNER** — PC-30, PC-34 wait on it |
| 13 | Scope of §3.8 (found by this survey; §2 item 5) | Whether the network-destination surfaces are DEL-05-02's obligation | Not stated by the file | **OWNER** — choice: a later SoW amendment gives DEL-05-02 the display of destinations, or §3.8 stays as PANEL's receiving of DEL-05-01's "shown" obligation with the SoW unchanged. No SoW edit is allowed in this run |
| 14 | OI-013 (L844) | Panel assembly, host/common boundary, persistence | Shared contract owner with SWB implementation owner | **HOST** |
| 15 | DEP-001 (L847); PC-24 governance value | Panel/views, act capture (Q-2), constraint (Q-1), treatment, list adoption | SWBPIPE / when UI-SUCCESSOR resumes | **HOST** |
| 16 | C U-C5 (L849; §2 L218) | Findings location | DEL-03-01 with host owner / before PC-12 | **HOST** |
| 17 | SWBPIPE embedded direction (L860) | D-58 predates D-20 | SWBPIPE | **HOST** |
| 18 | PN-5 (L516–518; L861) | Grant display for a host without grants (PROPOSED; "may be deferred") | Integrator / when host joins resume | **HOST** |
| 19 | P U-P3 (L862) | Host evidence that application re-checks the basis | Host owner / before PC-09b | **HOST** |
| 20 | Required-tool evaluation in the host (L258; L863) | Which party evaluates outcomes | Host owner; DEL-02-03 only under OI-014 / before PC-05 | **HOST** |
| 21 | Consequence vocabulary (L865) | Not defined | DEL-04-01 with host policy owner | **HOST** |
| 22 | Host view position references (§4 L563–567) | SWBPIPE offers no stable external reference (SQ-22) | Host | **HOST** |
| 23 | LOOP N-OPEN-5 (L859) | Stateless-MCP evidence; PC-36 waits | As LOOP | **SPIKE** — as LOOP item 28 |
| 24 | OI-014 (L845; §6) | Whether a §6 candidate becomes shared; OUT-004 | App/shared contract owners / before structural allocation | **LATER** — three candidates are "Plausible", their second consumers (DEL-04-02 displays; DEL-02-02) are App-side and DEL-02-02 is a later undertaking |
| 25 | DEP-05-02-017 (L848) | Actual human acts for PC-07, PC-18, PC-19, PC-21 | The person / when those cases execute | **LATER** — needs a candidate |
| 26 | D6 (L853) | App-side holds | Owner / governance phase | **LATER** |
| 27 | Governance phase taken up (L855); hold content of L850 | | Owner, per workflow | **LATER** |

Counts: NOW 8, OWNER 5, HOST 9, SPIKE 1, LATER 4. Total 27.

## 5. Design depth against the 60% description

Contributions PANEL exchanges: to the host owner (behaviour requirements for the four interactions, checkpoints, grant, destinations); to DEL-05-01 (panel needs, for its allocation account); to DEL-02-01 (host-panel consumer requirements); to DEL-03-04 and DEL-09-06 (panel receiving requirements). It consumes LOOP, WD, EXEC, C, P, ACT, AS, RS.

| Aspect | What the file has | What is missing |
|---|---|---|
| Interfaces | One table per interaction with "Person does / Panel presents / Host objects / Consumed definitions / Responsible / Must not / Unresolved" (§3.1–§3.3); checks table (§3.4); surfaces ND-1…ND-5 (§3.8); act and wording table (§5) | No list of what the panel passes back: message submit, turn cancel, workflow selection binding, the answer to a destination prompt. The file says decision controls are "host-offered and host-captured acts" (P-3 L229–231) and the host owns "the control, capture" (L545); it does not say what the loop receives from them |
| States | Tool-activity states (L240); seven required-tool outcomes and four workflow-level states (L252); proposal outcomes (L265); six dispositions (L355); seven grant states (§3.6); five model settings; six accounting states (§7) | Destination prompt states are implied by ND-2, not listed. No panel lifecycle (closed, reopened, reloaded while a turn runs) |
| Data | §2 definitions; origin elements (L265); content bindings (W-3); references-not-copies rule | What a "reference to a view position" is (SQ-22: not supplied). Findings location (U-C5) decides P-1 and H-3 |
| Operating sequences | None as sequences. The 37 cases (with sub-cases) follow the FX-PIPE-01 timeline T1–T17 | A sequence per interaction (for example queue → host view → item decision → host capture → application → receipt → panel). What the panel shows when a host outcome arrives after its display was drawn |
| Failure behaviour | Rejected calls by kind; *outcome unknown* with reporter (PC-10); refusals with both bases; no credential (PC-03b); lost observation → *unknown*; "record without capture evidence" (W-2) | Model interface failure and turn failure display (LOOP emits both; §3.1 lists only "Model request refused at boundary" and completion standing); a reference that no longer resolves; missed events; a destination prompt still pending at run end |
| Verification | PC-01…PC-37; rejection cases PC-13…PC-15; VC-01…VC-07; accounting states | No executed case. "EXECUTED (test double)" is a state (L662) without a described double |

**Structural choices still open:** OI-013 (assembly, persistence); OI-014 (three shared-presentation candidates: if agreed, §3.5, §3.6 and §5 become a shared presentation contract with DEL-04-02 and DEL-02-02); findings location (U-C5); the placement of §3.8 (item 13); U-E4; N-OPEN-4; and the LOOP tool-subject question (LOOP §5 structural 1), which changes what ND-2 and ND-4 present.

## 6. Joins (ACTIVE rows to the 14)

| Row | Contribution named | DAG-003 | Supplier's Design holds it, in a form PANEL uses? |
|---|---|---|---|
| DEP-05-02-005 → DEL-02-01 | Portable workflow/checkpoint meaning | held | **Yes.** WD §4.2.4 outcomes and pass rule; §3.4 states; §4.3.4; §4.3.7; §6.1–§6.4; WD §8 row for DEL-05-02 (WD L912). Used at PANEL §3.2, W-5f |
| DEP-05-02-006 → DEL-03-01 | Catalog/read-basis meaning | held | **Yes.** C §4.1, §5, §6 standing, element 9, §10. Used at §3.1, §3.2, §3.4 |
| DEP-05-02-007 → DEL-03-02 | Proposal, validation, outcome meaning | held | **Yes.** P §3.1, §3.3, §4.3, §8, §9; P §13 "Provide to DEL-05-02" (P L708). Used at §3.3 |
| DEP-05-02-008 → DEL-04-01 | Policy and human-act distinctions | **admitted** | **Yes.** ACT §2.1, §2.3, §2.4, §2.7, §4. Used at §3.4, §3.5, §3.8, §5 |
| DEP-05-02-009 → DEL-04-03 | Decision/run-record meaning | held | **Yes.** RS human-act record (§6), lapse rule (§7), R15. Used at W-2, W-3, ND-4 |
| DEP-05-02-010 → DEL-05-01 | Loop messages, tools, events, checkpoints | held | **Yes.** LOOP §2.1, §2.3, §2.4.0, §2.4.4, §5.1, §5.1.1. PC-30…PC-37 name MS-12…MS-22 and the numbers match (V10 Check 2) |
| DEP-05-02-019 → DEL-04-02 | Grant display states and active scope | held | **Yes.** AS §3 (seven states); AS §4 overlay; AS L214, L224 cite PANEL §3.8. Used at §3.6, ND-5 |
| DEP-05-02-020 → DEL-02-03 | Phase-1 recording meanings; governance-phase values | held | **Yes.** EXEC §2.1, §3.3 CR-8/CR-9, §3.6, §4; EXEC §9.2 row "DEL-05-02, DEL-04-02" (EXEC L1214). Used at §3.2, §3.5 |

Inbound: DEP-02-01-021 (held), DEP-03-04-015 and DEP-09-06-017 (admitted) ask for "host-panel consumer requirements" / "panel receiving requirements"; PANEL §3 supplies them. GUIDE pins PANEL `dd71e11d…`.

**Disagreements:** none in rule content between PANEL and its suppliers. Two statements disagree with the SoW and register (pin 7). PANEL §5's act table (L571–588) has no row for the network-destination grant or decline; LOOP §9 (L1298) and ACT §2.7 do. The wording is in ND-3, so this is an omission in one table, not a conflict.

## 7. Carried review items that name PANEL

| Item | State | Evidence |
|---|---|---|
| V6 m-1 | Names PANEL only as the subject of a stale GUIDE sentence; GUIDE's matter | V6 residual m-1 |
| Closeout D5-2-1 (EXEC-v0.2 citations), D5-2-2 (VC-01 "at `28bd00499`"), D5-2-3 (RELAY-v0.2; R5-n row) | Fixed | L11, L17, L308; VC-01 L875; §8 L747–749; L867 |
| Closeout S5-2-1…S5-2-6; R5-2-1, R5-2-2 | Applied by SCA-V4-001 and the register update (S5-2-3 "Direct", owner item O-12) | SoW diff in RV-2_DEL-05-02; DEP-05-02-019, -020; -014 and -015 RETIRED |
| Closeout "independent check of the pair (F-1)" | Open | F-1 L800 |
| V9 (all items) | None names PANEL | V9 residual table |
| V10 S-1 | Fixed | L529, L858 |
| V10 S-3 ("silent" dropped in ND-1) | Fixed | L540 "a silent switch to another model or provider" |
| V10 N-1 | Open | L10 |
| V10 N-4 | PANEL side already marks PC-30, PC-34, PC-36 (L859) | — |
| V11–V16 | No PANEL item; the 17 re-pins are carried as deferred | grep |

## 8. Recommended work on PANEL in this pass

1. Re-pin the header as for LOOP; add V4-HOST-02 and V4-EXM-23 to the Basis line. [§1]
2. Remove the three obsolete UNRESOLVED rows and F-9; close F-3, F-4, F-5, L480 and L864 against the revised SoW and register. [§1; §2; §4 items 1–6]
3. State the Phase-1 act request in W-5a, in step with LOOP item 3. [§3]
4. Record where §3.8 stands against the SoW and carry the scope question to the owner; change no SoW. [§2 item 5; §4 item 13]
5. Add the panel's return inputs, the four missing failure displays, the destination prompt states and a described test double. [§5]
6. Add a network-destination row to the §5 act table; cite V4-EXM-23 on PC-30…PC-37; update the Receivers line. [§2; §3; §6]
7. Follow LOOP item 5 where it changes ND-2 and ND-4. [§5]
8. Independent pair check with LOOP. [§4 item 7]

**Not in this pass, and why:**
- Layout, wording or component choices (SoW CLM-001; §0).
- Any reusable component (OUT-004 is conditional on OI-014).
- Executing cases (no host candidate; DEP-05-02-017).
- Changing the SWBPIPE mappings of §3.7 (they rest on answers; joins deferred).
- SoW or register edits.

---

# File 3 — HOSTING_BOUNDARY.md (DEL-01-01)

## 1. Pins

| # | Pin | Where | Verdict | Check and current value |
|---|---|---|---|---|
| 1 | `branch base 6e18505e3`, with `docs/ARCHITECTURE.md` §1 priorities | L8 | **stale** | ARCH §1 priority 3 is amended (Reference A), and so is the host-model line of the ARCH §2 diagram (now "or a cloud model (OAuth sign-in or API key), as the person chooses; other destinations only if the person allows them", ARCH L91–94). The other sections HOSTING cites (ARCH §3, §6, §7, §8; PRD §2.1, §4.3, §4.5, §4.7, §5, §6; EXM §2, V4-EXM-11/12) have no hunk in `git diff -U0 6e18505e3 HEAD` |
| 2 | ScopeOfWork.md `eddd122c…4773` | L8 | **stale** | INIT contract. Current `9945e72b04b4f45c4c641a5248cca8bc2ac40bf4897d1018c5ab59eba307cc75` after SCA-V4-001 (CLM-003, REQ-006, TBD-002, AX-005) and SCA-V4-002 (source line [N], AX-006) |
| 3 | "DEL-01-02…05, DEL-01-06, DEL-02-04 and DEL-04-01 remain referenced by accepted meaning (ScopeOfWork.md at 6e18505e3)" | L9 (end) | **stale** in part | DEL-04-01's SoW changed at `340ecf341` and DEL-01-04's at `1efd4bcda`. The SoWs of DEL-01-02, -03, -05, -06 and DEL-02-04 are byte-identical to `6e18505e3` |
| 4 | RELAY answers `6f01add3…61c7` | L9 | **stale** | Current `afb6e063…`. HOSTING uses SQ-02 only; its answer is unchanged |
| 5 | "EXEC-v0.2 HP-2 'not adopted'" as a body citation | L589–590 | **stale** | HP-1…HP-4 and HP-H are now EXEC-v0.4 §2.3 (EXEC L245–260); L600–601 already cites v0.4 for HP-4 |
| 6 | PIN_SPIKE "current committed revision" `0e090a4c…b115` | L9, L80 | **current** | |
| 7 | MANIFEST.sha256 `42b95826…569e`; COMMITTED_STATE.md `2cb7f1d2…2608` | L9, L83, L662 | **current** | Manifest check reproduced: 2 OK / 2,357 not committed / 0 mismatched |
| 8 | Sibling versions after R8 (list); "byte pins in GUIDE-v0.3" | L9 | **current** | GUIDE pins HOSTING `d11d4c57…` |
| 9 | OWNER_DECISIONS `5fd780bf…` "at `1528a5033`"; R8_RESOLUTIONS `44bc9a8d…`; INTAKE_MAP `3cc18295…` | L9 | **current**; first is ambiguous | As LOOP pin 15 |
| 10 | EXEC-v0.4 `d32be377…`, WD-v0.6 `fce565ed…`, R8 `1770c96e…` / `d4c34233…`, BRIEFS `3e33ba26…`, OWNER_DECISIONS `a5ccab0d…` | L9 | historical-true | |
| 11 | HOSTING v0.1 `f1da7f76…`, v0.2 `16711a83…`, v0.3 `34c33834…`, v0.4 `201ea320…`, v0.5 `f1a23022…`; EXEC-v0.1/v0.2/v0.3; ADAPTER-v0.1/v0.2; RS-v0.4 | L2, L9, L60 | historical-true | Each matches the named commit |
| 12 | PIN_SPIKE pre-correction `3d66ad28…f3cf` | L9, L80 | Not verifiable | No committed revision has that hash (the file says v0.2 consumed it before commit). IR1-C's `26ea0c2f…0334` matches `c387730fb` |
| 13 | R1…R6, V1-A, V1-C, IR1-C, V3-A, V3-B, DECISION-1/-2 records | L9, L60 | **current** (DECISION-1 state `f3f8e5f3…` historical-true, marked "at that time") | |
| 14 | Supplier facts "at 0.158.0" cited as `SPIKE §n` / `S-F-nn` | throughout | **current** against SPIKE | S-F-01…S-F-18 each have a change row (L104–121). Inventory counts match `_spike/inventory.txt` (104/167 client requests, 10/11 server requests, 83 notifications in JSON Schema) |

Stale: **5** (rows 1–5).

## 2. ScopeOfWork alignment (SoW `9945e72b…`)

| SoW item | Where HOSTING (and SPIKE) answer it | State |
|---|---|---|
| OUT-001 App-owned child/protocol boundary (artifact CODE) | §1, §3 H1–H11, §4, §5, §6 | **Developed as definition.** No code; the file's status is DRAFT DEFINITION |
| OUT-002 pin, generated types, supplement, version identity, plan/revision seam (CONFIG and generated source) | §7.1–§7.3; S-2; SPIKE §3–§4; `generated/0.158.0/` | **Partial.** Two JSON Schema bundles and the manifest are committed; TS is not; the reference output is not chosen (U-15); the supplement is empty |
| OUT-003 responsibility account (DOC) | §12 (OI-008 proposal, optional-reuse table); §8.1 (local-provider account); §11 | **Partial.** REQ-004 asks to "record the … choice when made"; none is made. L-2 and L-3 are not observed |
| OUT-004 qualification and upgrade evidence (TEST) | §9.1–§9.5; X-01…X-14; SPIKE transcripts | **Only designed.** No recorded exchange is an X-fixture (§9.2 L853–856); the upgrade procedure has no second pin |
| CLM-001…CLM-006 | §1, §2, §11 | Developed |
| CLM-003 (revised: D4 selected 0.158.0 for definition and generation) | "Pin" note L20–24; §7.1; U-01 | Agrees |
| REQ-001 | §1; H1–H3; §4; §5; R1–R3 | Developed |
| REQ-002 | §7.3 | Partial (U-15) |
| REQ-003 | §7.1, §7.2; S-2 | Developed |
| REQ-004 | §12 | Partial (OI-008 open; VC-11 says the criterion is "not met") |
| REQ-005 | §8.1 L-1…L-6 | Partial: identifies; does not qualify |
| REQ-006 (revised) | §7; §9.5; §11 row "Select the definition/generation pin" | Developed as method; agrees with the revised wording |
| REQ-007, REQ-008 | §11 | Developed |
| AC-001…AC-007 / VER-001…VER-007 | VC-01…VC-26, each with "Runnable now?" | Designed; "no case can pass a VER criterion yet" (L1146–1147) |
| TBD-001 (OI-008) | U-02; §12 | Carried |
| TBD-002 (revised: observations in PIN_SPIKE; re-examination and qualification pin remain) | U-01; §10 | Agrees |
| Source line [N] (revised by SCA-V4-002) | Pin note | Agrees |

**Contradictions or lags:** the SoW hash (pin 2) and the sibling-SoW statement (pin 3). No HOSTING rule contradicts the revised SoW. F-11 ("No gap in the SoW obligations for this definition", L1041) still holds for the revised text.

## 3. Amended basis

| Requirement | HOSTING text | Agreement |
|---|---|---|
| V4-HOST-01 | L-5 (L761): "D4-3 revises the host-agent wording (V4-HOST-01)"; F-24 (L1100–1106) | Agrees; both can now cite the amended text |
| V4-HOST-02 | §2 scope note (L185–197); header L6; F-25 | Agrees. The amended ARCH §4 now carries the same scope sentence ("This property governs a host's embedded agent; the App's own Codex keeps the person's Codex configuration, approval and sandbox choices"). HOSTING cites DECISION-5, Root AGENTS.md and D-GOV-43 for it, not the accepted text |
| ARCH §1 priority 3 ("local-first" wording) | L-4 "Local-operation boundary (priority 3)" (L760); F-14 "priority 3, local-operation boundary" (L1056); U-18 "acceptability under priority 3 … Before any local-operation claim" (L1133) | **Wording lags.** The amended priority 3 no longer has a "local-operation boundary"; it speaks of a host's agent and person-allowed destinations. *Inference:* U-18 remains a real question (the supplier's start-up fetch in the App), but it is no longer framed by the accepted priority-3 text |
| V4-ARC-11, V4-ARC-12 | Not cited (L-6 cites V4-ARC-10) | Not touched |
| V4-WF-05 / V4-HI-42 | §6.7 Phase-1 statement (L561–574) | Agrees: "No App run is holding"; no `run-holding` refusal, no HP-3 decline, no `turn/interrupt` for a checkpoint. The act-request point (LOOP §3) does not arise here: requests are DEL-02-03's |
| V4-HI-70 | S-7 (L746) | Agrees; not cited |
| V4-EXM-22, V4-EXM-23 | Not cited | Not touched |

## 4. Open items

| # | ID (location) | What is open | Owner / point of need | Class |
|---|---|---|---|---|
| 1 | Harness-capability meaning (L748–751; WD U-08; EXEC L296) | HOSTING offers "the 0.158.0 inventory" and says "no naming is chosen here". DEL-02-01's SoW asks for "capability meaning supplied through DEL-01-01" (DEP-02-01-025) | DEL-02-01 with DEL-01-01 and DEL-02-03 / before the App-side required-tool check | **NOW** — the two committed bundles list 19 native item kinds (v2 bundle, `ThreadItem`: `commandExecution`, `fileChange`, `mcpToolCall`, `dynamicToolCall`, `collabAgentToolCall`, `subAgentActivity`, `webSearch`, `plan`, …), 167 client methods and 11 server-request kinds (counted by script). A capability account can be written from them |
| 2 | F-16 (L1062–1064); Receivers L10 "register row missing" | DEL-01-01 → DEL-02-04 DOWNSTREAM row | C1 | **NOW** — the arc is represented from the consumer side (DEP-02-04-010, admitted). The supplier-side mirror is one of HANDOFF_STATE's "deferred supplier-side mirror rows" |
| 3 | F-24, F-25, L-5 status notes | Basis revision "at the next update" | — | **NOW** — closed by record (Reference A) |
| 4 | U-02, OI-008 (L1117; §12) | Rust/TypeScript division; O-1 recommended | App implementation owner / before architecture production contracts | **OWNER** — choice among O-1…O-4 (O-3 and O-4 set aside by the file) |
| 5 | U-03, OI-009 (L1118) | Account home; which home the label probe writes into | Owner with App implementation owner (DEL-01-05) / before account integration | **OWNER** — separated or shared Codex account state |
| 6 | U-15 (L1130; §7.3) | Reference generator output O-R1 / O-R2 / O-R3 | App implementation owner / before R2, R5 implementation | **OWNER** — three options tabled at L709–713 |
| 7 | U-18, acceptability (L1133; F-14; F-21) | Supplier fetches ≈24 MB from `github.com/openai/plugins` on a fresh home | Owner with DEL-01-05 / before any local-operation claim | **OWNER** — accept the supplier's own start-up traffic for the App, or require it to be prevented |
| 8 | U-21 (L1136; F-12, F-13) | Supplier labels `app-server` and both generators `[experimental]`; App-needed features are experimental-only | Owner visibility; App implementation owner at pin re-examination | **OWNER** — a visibility item for the owner |
| 9 | U-19 (L1134; §10 L944–958) | Unobserved live behaviours | App implementation owner (next spike; needs credential or local provider) | **SPIKE** — two groups: no credential needed (whether `initialized` is required; a known method before initialize; outbound frames without the version member); credential or local provider needed (the rest) |
| 10 | U-09 (L1124) | `serverRequest/resolved` triggers; acknowledgment observation | DEL-01-02 with this deliverable / before settlement fixtures | **SPIKE** (live turn) |
| 11 | U-22 (L1137) | L-2 provider wire interface; L-3 tool calling | DEL-01-05 / before provider qualification | **SPIKE** (identified local server) |
| 12 | U-18, configurability | Whether a setting disables the fetch | — | **SPIKE** — fresh-home start with candidate settings; causes the fetch, so it needs network and owner visibility |
| 13 | U-01 (L1116) | Pin qualification and re-examination | App implementation owner / before implementation | **LATER** |
| 14 | U-05 (L1120) | Restart bound values, grace period | App implementation owner with DEL-01-02 | **LATER** (implementation numbers) |
| 15 | U-06 (L1121) | Running an unverified distribution for development | App implementation owner | **LATER** |
| 16 | U-07 (L1122) | Use of `optOutNotificationMethods` | App implementation owner | **LATER** — the definition uses none (H7) |
| 17 | U-08 (L1123) | Content-identity algorithm | App implementation owner with DEL-04-03 / before qualification records | **LATER** |
| 18 | U-10 (L1125) | Stop-time handling of outstanding entries | DEL-01-02 | **LATER** (D1: later undertaking) |
| 19 | U-11 (L1126) | Automatic decline after a period | App implementation owner with DEL-01-02 | **LATER** |
| 20 | U-12 (L1127) | More than one supplier child | App implementation owner | **LATER** |
| 21 | U-13 (L1128) | Redaction policy details | App implementation owner / before first capture | **LATER** |
| 22 | U-14, F-01 (L1129) | DEL-01-01 / DEL-01-02 split on the unknown-request error | Both owners / when DEL-01-02 is defined | **LATER** (D1) |
| 23 | U-16 (L1131) | Descendant handling on stop, restart, overlap | DEL-01-02 with App implementation owner | **LATER** |
| 24 | U-17 (L1132) | Distribution-identity composition; launcher | App implementation owner with DEL-01-06 | **LATER** |
| 25 | U-20 (L1135) | Partition of the 11 server-request kinds; R9 membership | App implementation owner with DEL-01-04/01-05 / before R2 implementation | **LATER** — the proposal is tabled (L423–434); the deciding receivers are outside the increment |
| 26 | U-23 (L1138) | D6 App-side run holds | Owner / governance phase | **LATER** |
| 27 | U-24 (L1139) | App-initiated `mcpServer/tool/call` on a host channel | DEL-03-03 with App implementation owner | **LATER** — "None defined" in this increment |

Counts: NOW 3, OWNER 5, HOST 0, SPIKE 4, LATER 15. Total 27. U-04 and U-25 are closed in the file.

## 5. Design depth against the 60% description

Contributions HOSTING exchanges: seams S-1…S-7 (L738–746) to DEL-01-02, -03, -04, -05, -06, DEL-02-04, DEL-04-03; §6.7 facts to DEL-02-03; §6.8 MCP surfaces and §8.3 model destination to DEL-03-03; the 0.158.0 inventory to DEL-02-01; evidence to DEL-09-06.

| Aspect | What the file has | What is missing |
|---|---|---|
| Interfaces | Register entry elements (§6.1); register operations with caller and result (§6.4, five operations); seams table with "supplied / not supplied"; version identity record (§7.1); frame rules (§5) | No operations table for lifecycle control and observation (start, stop, explicit restart, state subscription) or for the generic client-request path; they are in prose (§4.1 "Receivers may" column; §5 "Client requests"). The receiver-facing transport is "unselected" (L149) |
| States | Eleven lifecycle states (L265–277); register state diagram (L438–445); client-request outcomes; verification result | No lifecycle transition table; transitions are read from §4.2–§4.5 |
| Data | Semantic records: register entry, client-request record incl. initiator, version identity, supplied-guidance evidence (§8.2), model destination per turn (§8.3) | Representation and persistence are DEL-01-02's (TBD-002). U-08 algorithm |
| Operating sequences | Start (§4.2), unexpected exit (§4.3), restart rules (§4.4), deliberate stop (§4.5), upgrade comparison (§9.5, ten steps) | Answer settlement as a sequence (it is a state diagram plus R4, R5); turn start with guidance carriage (S-6) |
| Failure behaviour | The strongest part: H8, H10, R2–R6, `settle-write-failed`, `unknown-no-response`, malformed and oversize frames, handshake failure, restart bound, descendants (H11), exit status never classifies an end | Failure of the recording tap; the set of `unverifiable(<reason>)` values |
| Verification | VC-01…VC-26 with a "Runnable now?" column; X-01…X-14; SV-01…SV-05 run in the spike | No supplier double exists, so the 10 cases marked "Yes (double)" or "Yes (transcript)" are not run. No App candidate, so no VER can pass |

**Structural choices still open:**
1. OI-008 (U-02): the Rust/TypeScript division. The file fixes the invariant only (L162–163).
2. U-15: the reference output decides notification familiarity and client-request conformance (L715–716).
3. OI-009 (U-03): the account home is an element of the configuration identity (L249).
4. F-15 (L1059–1061): seams S-1…S-4 have no receiving comparison because DEL-01-02…05 are a later undertaking (D1). A receiver's definition could change the register split (§6.5, U-14) and the descendant and stop rules (U-10, U-16).
5. The evidence path to DEL-04-03 (see §6).

## 6. Joins

DEL-01-01's register has no ACTIVE row to one of the 14. The six admitted inbound arcs are checked here from HOSTING's side.

| Arc | Consumer's row says | HOSTING holds it? |
|---|---|---|
| N-16, DEP-02-01-025 (DEL-02-01) | "harness-capability requirements shall refer to capability meaning supplied through `DEL-01-01`" | **Partly.** HOSTING L748–751: the SPIKE §4 inventory "is the input to harness-capability naming owned by DEL-02-01 …; no naming is chosen here". WD L929 and L1021 call it "harness capability inventory" and keep U-08 open. **Disagreement:** the consumer's contract expects capability *meaning* from DEL-01-01; HOSTING supplies an inventory and assigns the naming to DEL-02-01. Neither file defines the capabilities |
| N-23, DEP-02-03-023 (DEL-02-03) | "observed supplier facts" as capability information | **Yes.** §6.1, §6.7, §6.8, §10. EXEC §9.1 names §8.2, §8.3, R9 and the HP-4 scope (EXEC L1200) |
| N-B4, DEP-03-03-013 (DEL-03-03) | Supplier MCP/dynamic-tool surfaces and channel-status facts at 0.158.0 | **Yes.** §6.8 table (L637–647). ADAPTER cites HOSTING-BOUNDARY-v0.6 §8.3 and H8 |
| N-B9, DEP-03-04-021 (DEL-03-04) | Supplier boundary (native surfaces for optional external access) | **Yes.** §6.8; GUIDE cites HOSTING §7, §10, §8 S-6, §8.2 and pins `d11d4c57…` |
| N-15, DEP-04-03-027 (DEL-04-03) | Supplied guidance, model and destination, tool-permission settlements "from `DEL-01-01`" | **Yes in content** (§8.2, §8.3, R8, S-7). **Disagreement on the path:** HOSTING says these records reach "DEL-04-03 (through DEL-01-02)" (L746) and "through DEL-01-02 (S-7)" (L776). RS says "DEL-01-01 observed facts in this undertaking; DEL-01-02 later (D1)" (RS L192) and lists DEL-01-01 as a direct interface (RS L454). DEL-01-02 is not in this increment |
| N-C5, DEP-09-06-032 (DEL-09-06) | App-side supplied-guidance and model-destination evidence | **Yes as definition** (§8.2, §8.3); no evidence exists |

HOSTING's Receivers line (L10) names DEL-02-01, DEL-02-03 and DEL-03-03. It does not name DEL-04-03 as a direct receiver, DEL-03-04 or DEL-09-06. The arcs were admitted at DAG-002, after HOSTING-v0.6 was written.

## 7. Carried review items that name HOSTING

| Item | State | Evidence |
|---|---|---|
| V6 m-1, m-3…m-7 | None names HOSTING (V6: HOSTING byte-identical to `2f42fba02`) | V6 |
| Closeout (C1-B §5) | Not read in full. CLOSEOUT_ACCOUNT routes to the owner "DEL-01-05 matters: the Codex fresh-home plugin fetch (L-4) and the supplier's `[experimental]` labels" | Still open: U-18, U-21 |
| V9 (all items) | None names HOSTING; Check 1 passes it for model access | V9 |
| V10 N-1 | Open | L9 |
| V10 N-6 ("R8-13 close" row claims a marker HOSTING never carried) | As written; V10 called it harmless | L50 |
| V11–V16 | No HOSTING item. RV-1 (BASIS-ALIGN) and RV (SCA002) revised the SoW; both PASS | grep; RV returns |

## 8. Recommended work on HOSTING in this pass

1. Re-pin the header: SoW `9945e72b…` and both amendments; the sibling-SoW statement; RELAY answers; the EXEC-v0.2 body citation. [§1]
2. Cite the amended ARCH §4 scope sentence in the §2 note; restate L-4, F-14 and U-18 against the amended priority 3; close the status notes in F-24, F-25 and L-5. [§3; §4 item 3]
3. Bring Receivers and the seams table in line with the six admitted consumers; reconcile the DEL-04-03 path with RS. [§6]
4. Add a harness-capability account from the committed bundle (supplier item kinds, client methods and server-request kinds grouped by capability, each with its standing label). Leave the portable names to DEL-02-01 unless the integrator rules otherwise. [§4 item 1; §6]
5. Add operations tables for lifecycle and the client-request path, and a lifecycle transition table. [§5]
6. If the integrator wants observed behaviour in this pass: a supplier double seeded from the eight `_spike/transcripts`, to run the cases the file marks runnable with a double (VC-03, -04, -06, -16, -20, -21, -22, -23, -24, -25, and parts of VC-14, VC-26). This is a bounded prototype under LOOP_INIT's "bounded implementation and connected tests". [§5]
7. Prepare the next-spike brief for U-19 in its two groups. Running the credential group needs an owner decision. [§4 items 9–12]

**Not in this pass, and why:**
- Qualification of any pin (D4; DEP-005).
- Deciding OI-008, U-15 or OI-009 (App implementation owner / owner).
- Defining DEL-01-02…05 (D1; S1-F's question).
- Any live run against the supplier: it needs network (the fresh-home fetch) and, for turns, a credential or a local provider.

---

# File 4 — PIN_SPIKE_0.158.0.md (DEL-01-01)

This file is a dated observation record ("Status: OBSERVATION RECORD — spike evidence at pin 0.158.0, not qualification", L3). Sections 2, 5 and 8 are answered on that footing.

## 1. Pins

| # | Pin | Where | Verdict | Check and current value |
|---|---|---|---|---|
| 1 | Repo `be8bb46dd`, branch base `6e18505e3` | L5 | historical-true | Both are commits in this repository. They identify the state at the spike |
| 2 | ScopeOfWork.md `eddd122c…4773` | L5 | **stale** by value; true for its date | Current `9945e72b…`. The spike's authority is D4, which the revised CLM-003 and TBD-002 now record |
| 3 | FIRST-INCREMENT OWNER_DECISIONS.md `f3f8e5f3…1f2e` | L5 | **stale** by value; true for its date | Current `a9869129…ad2c` (DECISION-2 added, 32 lines; the D4 paragraph is unchanged: `git diff be8bb46dd HEAD` shows insertions only) |
| 4 | HOSTING-BOUNDARY-v0.1 `f1da7f76…d728` | L6 | historical-true | Matches `be8bb46dd` |
| 5 | MANIFEST.sha256 `42b95826…569e` | L107 | **current** | |
| 6 | Binary and sibling hashes (`788a818f…35c8` and others); per-variant manifest hashes | L75–77, L96–99, L340 | Not verifiable here | They describe files outside the repository (scratch install). The variant manifests are not committed |
| 7 | Supplier package `@openai/codex@0.158.0` | L54, L73 | Observation | Not re-checked (no network) |

Stale by value: **2** (rows 2, 3). Neither changes an observation.

## 2. ScopeOfWork alignment

The record serves OUT-002, OUT-003 and OUT-004 as evidence (L4) and says no VER is passed. Against the current SoW:

| SoW item | In SPIKE | State |
|---|---|---|
| OUT-002 generated types with provenance | §4 (commands, four variants, determinism, inventory); `generated/0.158.0/` | Partial, as HOSTING §2 |
| OUT-003 local-provider account inputs | §6 P-11, P-12, L-4 row | Inputs only |
| OUT-004 recorded exchanges and regeneration method | §5 transcripts (8); `_spike/generate.sh`; SV-01…SV-05 RUN | First recordings; "Not recorded as an X-01 fixture" (L236–238) |
| TBD-002 (revised) "observations recorded in `Design/PIN_SPIKE_0.158.0.md`" | The file | Agrees |

No contradiction with the revised SoW. One internal lag: §4's "What the spike proposed to commit" and SV-02's expected "1,607 OK" describe the never-committed form; both passages say so (L101, L339).

## 3. Amended basis

The record touches the amended texts in one place: the UNRESOLVED row "Supplier plugin sync network at start (S-F-10): acceptability under priority 3 … Before local-operation claims" (L325), and S-F-10's "priority 3" (L283). ARCH §1 priority 3 is amended (Reference A). As a dated record it is true for its date. It cites none of V4-WF-05, V4-HOST-01/02, V4-ARC-11/12, V4-HI-42/70 or V4-EXM-22/23.

## 4. Open items

| # | Item (L322–330) | Owner / point of need | Class |
|---|---|---|---|
| 1 | Live behaviour of P-08, P-09, P-10, P-13, P-15 | App implementation owner / before settlement fixtures and qualification | **SPIKE** (credential or local provider) |
| 2 | Reference generator output (S-F-03) | App implementation owner / before R2, R5 implementation | **OWNER** — same as HOSTING U-15 |
| 3 | Commit form | — | RESOLVED in the file; not counted |
| 4 | Plugin sync network at start (S-F-10) | Owner with DEL-01-05 / before local-operation claims | **OWNER** — same as HOSTING U-18 |
| 5 | Descendant handling (S-F-06) | DEL-01-02 with App implementation owner | **LATER** |
| 6 | Whether `initialized` is required; known method before initialize; runtime gating without opt-in | Next spike / before handshake implementation | **SPIKE** — the first two need no credential |
| 7 | Relocatability of the vendor binary | DEL-01-06 / before packaging | **LATER** |
| 8 | L-2 wire interface | DEL-01-05 / before provider qualification | **SPIKE** |
| 9 | Re-examination of the pin | App implementation owner / before implementation | **LATER** |

Counts: NOW 0, OWNER 2, HOST 0, SPIKE 3, LATER 3. Total 8. All eight repeat HOSTING items (U-15, U-18, U-19, U-22, U-16, U-17, U-01).

## 5. Design depth

Not a design file. As evidence for the six aspects:
- **Interfaces:** the initialize exchange as sent and received (§5 L180–204); the method and request inventory (§4).
- **States:** exit behaviour on stdin close and `SIGTERM`; descendants outliving the supplier.
- **Data:** answer forms per request kind (P-08, L220); plan update shape (P-10); account and provider elements (P-11, P-12).
- **Sequences:** five handshake scenarios with transcripts.
- **Failure:** unknown method before and after initialize (-32600); second initialize.
- **Verification:** SV-01…SV-05 RUN, SV-06 DESIGNED.

All 18 findings (S-F-01…S-F-18) are carried into HOSTING (HOSTING L104–121). No structural choice rests on this file alone.

## 6. Joins

No register row names this file. It is cited by HOSTING (L9), by GUIDE (pin `0e090a4c…`), ADAPTER (L16) and CA (L23) at the same hash. The consumers' contributions are read from HOSTING (File 3 §6).

## 7. Carried review items

| Item | State | Evidence |
|---|---|---|
| IR1C-19, IR1C-21 (first run; stale UNRESOLVED row; git-operations statement) | Fixed at the current revision | HOSTING L80–86 records the corrected revisions; the row at L324 reads RESOLVED; L24–26 states the read-only git operations |
| V6, V9, V10, V11–V16 | None names PIN_SPIKE. V10 Check 4 confirms it unchanged from `main` | grep |

## 8. Recommended work in this pass

1. **No edit.** Three files pin its bytes. Its two value-stale pins are true for its date and change no observation. [§1; §6]
2. State its standing in HOSTING's re-pinned header: "PIN-SPIKE-v0.1 unchanged; its basis is the INIT SoW and the DECISION-1 state of the owner record". [§1]
3. A new spike produces a new record; it does not revise this one. [§4]

**Not in this pass:** re-running the spike (scratch npm install and a fresh-home start need network and cause the plugin fetch).

---

# Closing table

| File | Stale pins | NOW | OWNER | HOST | SPIKE | LATER | Open items |
|---|---|---|---|---|---|---|---|
| LOOP | 12 (+1 defective, +1 ambiguous) | 10 | 5 | 11 | 2 | 6 | 34 |
| PANEL | 7 (+1 defective, +1 ambiguous) | 8 | 5 | 9 | 1 | 4 | 27 |
| HOSTING | 5 (+1 ambiguous) | 3 | 5 | 0 | 4 | 15 | 27 |
| PIN_SPIKE | 2 (true for its date) | 0 | 2 | 0 | 3 | 3 | 8 |
| **Total** | **26** | **21** | **17** | **20** | **10** | **28** | **96** |

Overlaps in the totals: LOOP and PANEL share 18 items (the three closed basis rows, the pair check, hold-machine confirmation, OI-013, OI-014, OI-021, DEP-001, C U-C5, consequence vocabulary, SWBPIPE's embedded direction, U-E4, U-03, N-OPEN-4, N-OPEN-5, D6, governance phase); all eight PIN_SPIKE items repeat HOSTING items. Counted once, the four files hold 70 distinct items. Of the 21 NOW entries, 12 are already closed by a record and only need the file to say so (LOOP 5, PANEL 6, HOSTING 1).

**The three most consequential gaps:**

1. **LOOP has destination rules but no tool subject that reaches a destination.** Tools are host catalog entries only (LOOP L305, L350; V4-ARC-13), while §5.1.1 and MS-14…MS-22 assume web, MCP and API tools and outside processes. The destination check is not placed in the turn sequence or the validation order, the decline and the pending request have no place among the four result classes, "destination" has no identity, and C and P carry none of it. Settling this may add an entry element or an outcome in C and P and changes PANEL §3.8. (LOOP §5; PANEL §5.)
2. **The model-interface basis has no supplier (DEP-05-01-024).** Every LOOP fixture is a case design, three of the six capability rows are open on representation, and SWBPIPE has selected nothing. It needs an owner choice on who names the basis and a bounded observation of one server. (LOOP §4 items 11, 27.)
3. **HOSTING's admitted consumers ask for things it does not hold in the form asked.** DEL-02-01 expects harness-capability meaning and gets an inventory with naming assigned back to it; DEL-04-03 consumes evidence directly while HOSTING routes it through DEL-01-02, which is outside the increment; the Rust/TypeScript division (OI-008) and the reference output (U-15) are undecided and no receiver of S-1…S-4 has compared the seams. (HOSTING §4 items 1, 4, 6; §5; §6.)

Next in consequence: the Phase-1 act request that the amended V4-WF-05, V4-HI-42 and V4-EXM-22 keep in force and that LOOP and PANEL do not state (LOOP §3; PANEL §3); and PANEL §3.8 having no obligation in DEL-05-02's SoW (PANEL §2 item 5).

**Owner-level choices found:**

| Choice | Where |
|---|---|
| Who names the host model-interface basis while SWBPIPE has none | LOOP item 11 |
| Whether a category switch governs its named entries | LOOP item 12 |
| SP-6 or counting prior acts on unchanged content | LOOP item 13 |
| Partial-lapse purpose (U-03) | LOOP item 14 |
| First connected operation (OI-021) | LOOP item 15 |
| Whether the panel's network-destination surfaces become DEL-05-02 scope | PANEL item 13 |
| Rust/TypeScript division (OI-008); reference output (U-15); account home (OI-009) | HOSTING items 4–6 |
| Acceptability of the supplier's start-up fetch; dependence on an `[experimental]` surface | HOSTING items 7–8 |
| Whether a spike with a credential, a local model server or network access is allowed in this pass | LOOP items 27–28; HOSTING items 9–12 |
