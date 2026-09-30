# S1-C — scoping survey: DEL-02-01 (WD, WD-EX) and DEL-02-03 (EXEC)

- Run `APP-V4-DESIGN-PASS-2-20260930`, node S1-C. Type 2 TASK executor (Claude Code subagent). No delegation, no git write, no network. The only file written is this one.
- Brief: `BRIEFS.md` of this run ("Common rules", "S1 — scoping survey"), sha256 `20673794…` as read.
- Repository state read: working tree at `4698471d9` (branch `claude/chirality-app-v4-60-percent-a41fd5`).
- Surveyed files (sha256 recomputed with `shasum -a 256`):

| Short | File | Version in header | sha256 (current bytes) | Lines |
|---|---|---|---|---|
| WD | `PKG-02…/DEL-02-01…/Design/WORKFLOW_DECLARATION.md` | DEL-02-01/WD-v0.6 | `43a9962f025de384e1cdaedea9a648da74e20216476a04f2394cfa3851f47eb9` | 1105 |
| WD-EX | `PKG-02…/DEL-02-01…/Design/EXAMPLES.md` | DEL-02-01/WD-EX-v0.6 | `8d60ed7850e6935b8410217c8867c59554c7de9aec28c60514e88ff5f0cff36e` | 504 |
| EXEC | `PKG-02…/DEL-02-03…/Design/EXECUTION_COMPATIBILITY.md` | DEL-02-03/EXEC-v0.4 | `092f248682447df74e93915527930f4b90367fac46b867dad18daef3c5c608ff` | 1347 |

  All three equal the pins in GUIDE-v0.3's input table (`HOST_INTEGRATION_GUIDE.md` lines 24–26), so none has changed since GUIDE's last re-pin.

## Method and limits

**Read in full:** the three Design files; both `ScopeOfWork.md`; both `Dependencies.csv` (every EXECUTION row) and `_DEPENDENCIES.md`; `_DAG/DAG-003/HANDOFF_STATE.md`; `R3`…`R8_RESOLUTIONS.md`; the four runs' `OWNER_DECISIONS.md`; first-run `reviews/V6.md`, `closeout/CLOSEOUT_ACCOUNT.md`, `RECEIPT.md` and the DEL-02-01 / DEL-02-03 parts of `closeout/C1-A.md`; intake `reviews/V9.md`; `loop/LOOP_INIT.md` "Develop the detail appropriate to the phase".

**Read in part:** R1 (R-5) and R2 (checkpoint section); `reviews/V10.md`, V11–V16 and the RV records (searched for the three files by name; the DEL-02-01 RV-2 diff read); `SCA-V4-001…/Propagation_Plan.md` §5 and `Handoff_State.md`; `AMENDMENT_PACKET/OWNER_ITEMS.md` (O-4 note, O-25). Supplier Design files (C, P, ACT, RS, LOOP, PANEL, HOSTING, PIN-SPIKE, ADAPTER, CA) were read only at the sections the joins cite. `C1-B.md` and `C1-C.md` were not read.

**Direct checks made:**

- Every 64-hex sha256 and every abbreviated hash in the three files was classified by script against (a) current working-tree bytes and (b) an index of all project blobs over the 109 commits that touch `projects/chirality-app-v4/{execution,docs}`.
- Basis-doc changes: `git diff 6e18505e3..HEAD -- projects/chirality-app-v4/docs`.
- SoW changes: `git diff --word-diff 6e18505e3..HEAD` on both SoWs.
- Quoted requirement texts: `grep` of the quoted phrase in the current source.
- DAG arcs: `DependencyEdges.csv`, `CandidateEdges.csv`, `ExcludedRows.csv` filtered by script; `shasum -c` of the six DEL-02-01/02-03 entries of `DAG-003/SOURCE_MANIFEST.sha256` (all OK).

**Convention.** "States" means the file says it. "Inference" marks my reading. Line numbers are `L<n>` in the current bytes. A "stale pin" is a pin or version reference that is meant to identify the current basis and no longer matches it; pins that record what an earlier pass read are "historical" and are counted separately.

---

# Part A — DEL-02-01 `WORKFLOW_DECLARATION.md` (WD-v0.6)

## A.1 Pins

Counts for WD: 43 full sha256 values and 13 abbreviated ones. **None equals the current bytes of any Design file or SoW.** 15 of the full values equal current run-record bytes (rulings, reviews, INTAKE_MAP, the first-run owner decisions). Every other value resolves to a historical blob, as the file says it should, with one mistyped abbreviation.

| # | Pin (WD location) | Status | How checked | Current value |
|---|---|---|---|---|
| A1-1 | Basis "repo 6e18505e3" for `P/docs/PRD.md`, `ARCHITECTURE.md`, `HOST_INTEGRATION.md`, `EXAMINATION.md` (L6) | **STALE** | `git diff 6e18505e3..HEAD -- docs`: 4 files, 103 insertions, 37 deletions, from SCA-V4-001 (`230bf1e64`, `a0af39f8c`) and SCA-V4-002 (`70376aff2`, a line break only) | PRD `bb6e786f…49bd`, ARCHITECTURE `317d5789…828c`, HOST_INTEGRATION `d4331c39…8d9f`, EXAMINATION `471798bc…57d0`; last doc commit `70376aff2f` |
| A1-2 | `ScopeOfWork.md sha256 080d7f5a…a294` (L6) | **STALE** | recomputed; `080d7f5a` is the SoW at `6e18505e3`, `bcc25624d` and `7a1508452` | `ef360edf28f5f463ae961495e04e566ab9ec9d56c0a4fd4f35e67b87adb82f17` (after SCA-V4-001 and SCA-V4-002) |
| A1-3 | `R8_RESOLUTIONS.md sha256 d4c34233…e7af` "R8-12, items 1 and 7" (L8) | **STALE** | `d4c34233` is the file at `7a1508452`; R8-13 was added at `1528a5033` | `44bc9a8df4fe73e3f41711e7d9593a065734b054400f12bb01695a30e7b30e6b` (R8-1…R8-13). WD consumed nothing of R8-13 |
| A1-4 | `R8_RESOLUTIONS.md sha256 9877da07…1234` (L9, A1 pass) | historical | equals the file at `bcc25624d` | superseded by A1-3 inside the file |
| A1-5 | Intake `OWNER_DECISIONS.md` "at `bcc25624d`, sha256 a5ccab0d…e776" (L6) | **STALE** | matches at `bcc25624d`; DECISION-5 and its confirmation were added later | `5fd780bf90a4d51751d2c2fa632b92111a52cd0d9445a0870be9d28bcb4f40b2` |
| A1-6 | Intake `BRIEFS.md sha256 3e33ba26…7517` (L9) | **STALE** (brief of a closed pass) | matches `bcc25624d`…`3733b1421` | `6f32809d…03b4` |
| A1-7 | `RELAY_ANSWERS_SWBPIPE.md … sha256 6f01add3…61c7` and "unchanged" (L8, L9, L930) | **STALE** | current file differs; SWBPIPE revised it at `a999f4ba1` (3 lines: integrity standing list, evaluated-basis sentence, T9 source) | `afb6e063e7e5dfccf8986206f888cf1e2e1c4e7fc3430fdf86db670714fc0e74`. The three changed lines are not answers WD cites (my diff) |
| A1-8 | EXEC-v0.4 "working tree after the A1 edit, sha256 d32be377…76d4" (L9, L923) | **STALE** as bytes; version label current | `d32be377` is EXEC at `7a1508452`; A6 then edited it in place | EXEC-v0.4 `092f2486…08ff` |
| A1-9 | "Current sibling versions after R8, as committed at `7a1508452` with A6's in-place R8-12 edits (their byte pins are in GUIDE-v0.3's input table)" (L8) | labels current; **byte state STALE** | all 15 version labels equal the current headers. GUIDE's table now holds the bytes "after the R8-13 pass (node B1)"; C, ADAPTER, ACT, AS, RS, LOOP, PANEL and HOSTING changed after the state WD names | GUIDE-v0.3 input table, lines 16–35 (all 18 pins match current bytes) |
| A1-10 | First-run `OWNER_DECISIONS.md` `a9869129…ad2c` (L6) | current | recomputed | same |
| A1-11 | First-run `OWNER_DECISIONS.md` `f3f8e5f3…1f2e` (DECISION-1, L6) | historical | file at `be8bb46dd`…`e20a3ae8d` | superseded by A1-10 |
| A1-12 | R1 `2f9c7e72`, R2 `77cfb845`, R3 `202d52c7`, R4 `50a009b2`, R5 `254d0b93`, R6 `8703e85a` (L10–L16) | current | recomputed | same. R7 is cited without a hash (L11); current `1f6ab3b2…a1ea` |
| A1-13 | `INTAKE_MAP.md 3cc18295…ea33` (L9) | current | recomputed | same |
| A1-14 | Reviews V4-A `121deafc`, V3-A `f25f5af1`, V3-B `5662fbd0`, V2 `75ba1dff`, IR1-A `31b3c7f8`, IR1-B `70e4a4f6`, IR1-C `295e96b3`, V1-C `8d46258a…94a6` (L10–L17) | current | recomputed | same |
| A1-15 | V1-A `` `01811533…c04c09` `` (L17) | **mistyped** | the only blob with prefix `01811533` is `comparisons/V1-A.md`, which ends `…cfe04c09` | `01811533bf0aedad…cfe04c09` |
| A1-16 | WD's own earlier versions v0.1…v0.5 (L2) | historical, all verified | each hash found at the commit the file names | — |
| A1-17 | Sibling byte pins of earlier passes: EXEC-v0.1/0.2/0.3, C-v0.2…v0.5, ACT-v0.2…v0.5, LOOP-v0.2/0.4/0.5, P-v0.2/0.4/0.5, CA-v0.1/0.2, WD-EX-v0.5 (L10–L18) | historical, all verified | each found in the blob index at the named commit | — |
| A1-18 | Root reuse sources "read (not adopted)" at `6e18505e3`: `workflows/WORKFLOW_TEMPLATE.md`, 66 `execution.json`, `catalog.yaml`, `catalog.schema.json`, `index.json`, `create-workflow/WORKFLOW.md`, `docs/SPEC.md`, `docs/AGENT_WORKFLOW_RUNTIME.md` (L6) | current | `git diff --stat 6e18505e3..HEAD` on those paths is empty; 66 `execution.json` today | unchanged |
| A1-19 | `Open_Issues.csv` OI-003, -013, -014, -018, -021 (L6) | current | the diff since `6e18505e3` touches only the OI-001, OI-002 and OI-012 rows; the five cited rows are OPEN and unchanged | — |
| A1-20 | `DECISION_BRIEF.html` #d2, #d3, #d5 (L6) | current | no diff under `_Coordination/Acceptances` since `6e18505e3` | — |
| A1-21 | Basis section numbers: PRD §2.2, §2.4, §4.1, §4.2, §4.3, §4.5, §4.7; ARCH §1, §4, §5; HI §1–§6, §9 (L6) | section numbers current | headings listed by `grep` | — |

**Stale requirement texts quoted or paraphrased in WD.**

| WD text and location | Text WD assumes (at `6e18505e3`) | Current text |
|---|---|---|
| S-F (L163); header Phase line (L4); CG-7 (L366–L371); U-33 (L1038): "V4-WF-05's first half ('the product holds a workflow's declared checkpoints … the run waits') is phased to the governance layer, not withdrawn, and is flagged for the next accepted-basis update" | PRD V4-WF-05: "The product holds a workflow's declared checkpoints: when a run reaches one, the required human act is requested, and the run does not record the act as done until the person performs it." | PRD L254, V4-WF-05: "When a run reaches a workflow's declared checkpoint, the required human act is requested, and the run does not record the act as done until the person performs it. Holding the checkpoint — the run waits until the act is performed — is **phased to the governance layer**, not withdrawn (DEC-4): in the current phase, declared checkpoints are plan guidance that the person and the agents manage, and neither the App nor a host's embedded loop enforces a hold, blocks a run, or reports a workflow unsupported because a hold cannot be enforced. Enforced holds are applied later to the workflows that need them; the declared checkpoint and the definitions that enforcement needs are kept so that every such workflow can be served. Reserved human acts (§4.5) are unaffected." `grep -c "product holds a workflow" docs/PRD.md` = 0 |
| S-F (L163): "checkpoints override autonomy", cited to HI V4-HI-42; I-7 (L504–L506) and U-34 (L1039): "V4-HI-42 [is] guidance in Phase 1" | HI V4-HI-42: "A workflow's declared checkpoints override autonomy: at a checkpoint the run waits for the person's act (V4-WF-05)." | HI L139, V4-HI-42: "Autonomy does not override a workflow's declared checkpoints: whatever the autonomy setting, a checkpoint's required act is requested and recorded as done only when the person performs it. Holding the run at the checkpoint until then is phased to the governance layer (V4-WF-05): in the current phase a checkpoint is plan guidance that the person and the agents manage, and the reserved acts (V4-HI-30) still bind." "override autonomy" no longer occurs in `docs/` |
| S-P (L173), cited to HI V4-HI-70/71 (no quotation) | V4-HI-70 ended "…the human acts performed, and the model used (D-07)." | HI L219: "…the human acts performed, the model used and, for a host's agent, each network destination contacted (D-07; V4-HOST-02)." S-P's own statement is unaffected |
| Basis list "EXAMINATION.md V4-EXM-10, -14, -21, -22" (L6; no quotation) | V4-EXM-22: "A workflow checkpoint stops the run for a human act." | EXM L147: "A workflow checkpoint requests a human act, and the act is recorded only when the person performs it, whatever the autonomy; stopping the run at the checkpoint is examined only for a workflow that takes up the governance phase (V4-WF-05)." |

**Stale-pin count for WD: 10** (A1-1, -2, -3, -5, -6, -7, -8, -9, and the two stale requirement texts V4-WF-05 and V4-HI-42). Plus one mistyped abbreviation (A1-15).

## A.2 ScopeOfWork alignment

Current SoW: `ef360edf…2f17`, revised by SCA-V4-001 (CLM-002, CLM-003, REQ-002, REQ-003, REQ-006, VER-003, TBD-003; added TBD-004, AX-005) and SCA-V4-002 (CLM-002 consumption sentence; added AX-006). Source of the wording: `RV/RV-2_DEL-02-01.md` and `RV/RV_DEL-02-01.md`.

| SoW item | Where WD answers | Standing of the answer |
|---|---|---|
| CLM-001 (API_CONTRACT; four artifact classes) | §1 (L125–L150); EXAMPLES; §9; §13 | developed for the document, examples and map; the "open declared-part schemas" and "parser/consumer fixtures" do not exist (see OUT-002, OUT-004) |
| CLM-002 (owners; DEL-03-02 outputs consumed; DEL-01-01 supplies the harness capability inventory; DEL-03-03 receives the constraints) | §8 (L906–L930), §10 (L964–L980), §4.2.1 (L244–L259), §4.3.6–§4.3.7 | **partial.** DEL-03-02 consumption is developed (§4.3.6 L576, L579; §4.3.7 L614–L617). DEL-01-01 is named only in the §8 supplier table (L929) and in U-08; §4.2.1 still says the supplier of harness-capability meaning is `UNRESOLVED` (L249). DEL-03-03 appears only in §9 A-11 and A-12 (L955–L956) and in U-30 (L1034) |
| CLM-003 (host owner; person performs acts) | S-Q (L174), §4.3.2, §10 | developed |
| CLM-004 (no common service; OI-014, OI-013) | S-O (L172), §9 | developed |
| CLM-005 (four roles; seat; source identity) | §5, §6 | developed; seat mapping open (U-09) |
| OUT-001 contract | §2–§7 | developed |
| OUT-002 "Open declared-part schemas and explanatory examples" | §4.1–§4.7; EXAMPLES | **partial.** Meanings are developed. No schema exists: carriage is `UNRESOLVED` (R-4, L207–L209; U-01), wire names and schema language are unselected (U-02), and L208–L209 calls the schema "a required, deferred obligation" |
| OUT-003 responsibility map | §9 (L943–L956) | developed; every Confirmation cell "None" (U-17) |
| OUT-004 parser and consumer fixtures "with results bound to the actual contract/examples" | §13 (L1048–L1105) | **only named as designed cases.** L1050: "None has been executed; no parser, consumer or host exists." |
| REQ-001 | §3.2, §5, §6 | developed |
| REQ-002 (five categories; host-operation requirements refer to DEL-03-01; harness-capability requirements refer to meaning supplied through DEL-01-01) | §4.1–§4.5; §4.2.1 | **partial**; see lag 1 below |
| REQ-003 (act recorded only when performed; holding is the governance-phase definition, TBD-004) | §4.3.0 (L327–L371), I-1…I-9, §4.3.8 | developed |
| REQ-004 (promised vs observed; origins and revisions) | §4.6, §6 | developed; revision untestable (U-03) |
| REQ-005 (allocation) | §9 | developed |
| REQ-006 (excluded acts, now including "proposal/outcome definition by `DEL-03-02`, external-channel constraint carriage by `DEL-03-03`") | §10 (L966–L980) | **partial**; see lag 2 |
| AC-001, AC-002, AC-004, AC-005 | VC-01…VC-06, VC-13…VC-15, VC-17, VC-25, VC-26, VC-33 | designed |
| AC-003 ("distinguish execution, proposal acceptance, checking, approval and professional reliance; each claimed act has its own actor/subject/evidence") | VC-07…VC-12, VC-16, VC-20…VC-24, VC-27…VC-32, VC-35…VC-45 | **partial.** No case exercises an A6 (engineering approval) or A7 (reliance) checkpoint. "A6" and "A7" do not occur in §13 (grep; VC-12, L1068, tests only that a design-candidate approval is invalid). See B.2 |
| AC-006 | VC-18 "§10 vs SoW REQ-006" (L1074) | designed; the comparison would now fail on the DEL-03-03 act (lag 2) |
| AC-007 | VC-19 (L1075) | designed only |
| VER-001…VER-007 | §13 "Serves" column | cases designed, none run |
| TBD-001 (OI-014), TBD-002 (OI-013) | U-12, U-13 | carried |
| TBD-003 (OI-001/002 ruled; OI-021; OI-018) | S-Q, S-R; U-05, U-14 | developed |
| TBD-004 (phased checkpoints; "This contract consumes `DEL-02-03`'s statement of the current phase and, for the governance phase, its hold-support values; it does not define them") | §4.3.0 (L329–L331), §4.3.8 (L662–L666), U-30 | developed. WD does not cite TBD-004 by ID |
| AX-001…AX-006 | §2, §9 | AX-005 and AX-006 are not cited; the SoW pin predates them |

**Places where WD lags or contradicts the revised SoW wording.**

1. **REQ-002 / CLM-002 vs §4.2.1 (L249).** SoW: "harness-capability requirements shall refer to capability meaning supplied through `DEL-01-01` (CLM-002)". WD: the supplier of meaning for a harness capability requirement is "`UNRESOLVED` (U-08)". WD names DEL-01-01 only as an input to naming (L1021).
2. **REQ-006 vs §10 (L966–L980).** The SoW list now includes external-channel constraint carriage by DEL-03-03. §10 has no DEL-03-03 row. (It has the DEL-03-02 row, L969.)
3. **CLM-002 vs §8 (L908–L916) and header Receivers (L20).** The SoW says DEL-03-03 receives the declared checkpoint constraints. Neither the receiver table nor the Receivers line names DEL-03-03. DEL-03-04 and DEL-09-06, which hold admitted arcs from WD (A.6), are named only as "Later" in L20 and have no §8 row.
4. **Terminology.** SoW and amended basis say "current phase" and "governance phase". WD says "Phase 1 (this increment)". Same meaning; different term.
5. **SoW hash.** The header pin is the pre-amendment SoW (A1-2). C1-A's statement "Every Design header's SoW hash equals the candidate SoW bytes" was true at `d3cebd1cc` and is no longer.
6. **U-33 (L1038)** and the Phase line (L4) still flag V4-WF-05 "for the next accepted-basis update". That update is done (SCA-V4-001, accepted 2026-09-29). `Propagation_Plan.md` §5 lists "WD U-33" among the notes to close.

No WD rule contradicts the revised SoW's meaning. The lags are in citations, tables and standings.

## A.3 Amended basis

| Amended item | Where WD touches it | Agreement |
|---|---|---|
| V4-WF-05 | L4, L38, S-F L163, CG-4 L349–L352, CG-7 L366–L371, U-33 L1038 | Intent agrees: §4.3.0 CG-1…CG-7 matches the amended sentence clause by clause (guidance; no hold; no *unsupported* for a hold reason; definitions kept; reserved acts stand). **Wording lags:** WD speaks of a "first half" and "second half". In the amended text the request-and-record clause comes first and the phased holding clause second, so "first half … phased" now points at the wrong half. The quoted phrase no longer exists. "Flagged for the next accepted-basis update" is obsolete |
| V4-HI-42 | S-F L163; S-S L177; I-7 L489–L506; FB-14 L1001; U-34 L1039; VC-11 L1067 | **Wording disagrees.** WD, following R8-11 item 2, says V4-HI-42 is "guidance in Phase 1" and "binds only for governed checkpoints in the governance phase". The amended V4-HI-42 has a part that binds in the current phase ("whatever the autonomy setting, a checkpoint's required act is requested and recorded as done only when the person performs it") and a phased part (holding). WD's CG-4 already carries the binding part, so the rule content agrees; the sentences about V4-HI-42 do not. The owner confirmed the R8-11 reading of D2's "or a declared checkpoint" at BASIS-ALIGN DECISION-7 (OWNER_ITEMS O-25); WD still labels it INTEGRATION only |
| V4-HI-70 | S-P L173; Basis L6 | WD does not restate the record content. No conflict. WD has no evidence kind for "network destination contacted" (§4.5 L737); none is required of a declaration |
| V4-EXM-22 | Basis L6 only | No text depends on it. VC-37 and VC-44 agree with the amended scenario |
| V4-HOST-01, V4-HOST-02, V4-ARC-11, V4-ARC-12, V4-EXM-23, "local-first" | not cited; `grep` for `V4-HOST-0[12]`, `V4-ARC-1[12]`, `local-first`, `local by default`, `local operation`, `cloud`, `DECISION-5`, `R8-13`, `allow list` returns nothing | WD does not touch them. One consequence is not addressed anywhere in WD: R8-13 made "network-destination grant" an A12 subclass (ACT-v0.6 §2.7). WD's A12 checkpoint and "grant setting" subject class (L378, L400, L581) still describe only operation-class grants. See A.6 D-6 |

## A.4 Open items

Owner and point of need are as the file states them (§12, L1012–L1040, unless another line is given).

| ID | What is open | Owner (file) | Point of need (file) | Class |
|---|---|---|---|---|
| U-01 | Physical carriage of the declared part: front matter, delimited body section, or companion file | DEL-02-01, with consumer confirmation | Before OUT-002 schema and OUT-004 parser fixtures | **SPIKE** — render E1, E1d, E5 and E6 in each carriage and parse them against R-1…R-3 (L198–L206). The inputs the file waited for now exist: EXEC-v0.4 §6.3 TR-4, §6.7 TF-4, §4.12 RP-5; LOOP-v0.6 §2.4 |
| U-02 | Wire field names, value encodings, schema language | DEL-02-01 with consumers | Before OUT-002 schema | **SPIKE** (same prototype; depends on U-01 and on C's representation, C U-C1) |
| U-03 | Revision algorithm and multi-file canonicalization | DEL-02-01 with DEL-04-03 | Before revision comparison claims | **LATER** for the algorithm (it is shared with HOSTING U-08 and RS, and the contract already carries a method designation). The file-set and canonicalization rule should be stated with U-01 |
| U-05 | Operation-specific reserved additions (`UNRESOLVED{OI-021}`) | Owner via outside SWB session | Before connected-activity SoW | **HOST** (owner decision made with the SWB session; deferred with the host joins) |
| U-05b | Host capture-evidence reference per act kind | SWBPIPE owner decision | Before host act-recording integration | **HOST** (SQ-01 answered: none) |
| U-05c | Multi-row A4 purpose after partial lapse | DEL-04-01 with Owner | At its point of need | **OWNER** — does an A4 on only the lapsed rows satisfy, with the earlier act still covering the unchanged rows, or is a new act over the whole scope required |
| U-07 | Operation version ordering or range | DEL-03-01 | Before DEL-02-03 required-tool fixtures | **HOST** (needs a host that publishes compatibility statements; SQ-18 (d): none) |
| U-08 | Portable naming of harness capability requirements | DEL-02-01 with DEL-01-01 and DEL-02-03 | Before App-side required-tool check | **NOW** — `PIN_SPIKE_0.158.0.md` §4 inventory; the committed `Design/generated/0.158.0/json-schema/` bundles (item kinds such as `commandExecution`, `fileChange`, `mcpToolCall`, `webSearch`, `collabAgentToolCall`, `dynamicToolCall` are present, by my grep); HOSTING-v0.6 §8 closing paragraph (L748–L751) |
| U-09 | Host seat → role mapping (SEAT-2 options a/b/c, L797–L801) | DEL-02-01 with SWB implementation owner and DEL-02-04 | Before host role-guidance supply | **HOST** (SQ-19 (d): SWBPIPE has no seat concept; DEL-02-04 is outside the increment) |
| U-10 | Host origin in unqualified precedence; whether a selection follows new revisions | DEL-02-02 (later undertaking) | Before host-origin discovery in App | **LATER** (DEL-02-02 is outside the 14, D1) |
| U-11 | Record fields for identity tuple, holding library, seat role, dispositions, events, referents, capturing surface | DEL-04-03 | Next comparison | **NOW** — RS-v0.6 §4 R1, R2, R8, R11, R14 and §6.1. WD states RS was "Not read" (L926) |
| U-12 | Placement of shared parts (`UNRESOLVED{OI-014}`) | App/shared contract owners | Before structural/production contract allocation | **OWNER** — per §9 row: shared type or library, local implementations with conformance fixtures, or a service |
| U-13 | Host loop placement, parsing, persistence, panel assembly (`UNRESOLVED{OI-013}`) | Shared contract owner with SWB implementation owner | Before shared/host implementation boundary contracts | **HOST** |
| U-14 | Guidance distribution and adoption (`UNRESOLVED{OI-018}`) | Owner with instruction owners | Before instruction changes or dependent supply | **LATER** (needed by DEL-02-04 supply, outside the increment); owner-held |
| U-15 | First connected operation (`UNRESOLVED{OI-021}`) | Owner via outside SWB session | Before connected-activity SoW | **HOST** |
| U-16 | Automatic catalog extension (`UNRESOLVED{OI-003}`, App v4) | Owner with host contract owner | Before claiming extension capability | **OWNER** — whether a new catalog operation is promised on all three surfaces without separate work. No effect on WD until decided |
| U-17 | Owner confirmations for §9 rows; SWBPIPE consumer needs | DEL-02-03, DEL-05-01, DEL-05-02, DEL-03-02; SWBPIPE via relay | Next comparison; relay | **NOW** for the four internal consumers (their v0.6/v0.4 Design files state what they consume; a comparison can return confirm-or-object per row). The SWBPIPE part is HOST |
| U-19 | SQ-02: can the host hold the constraint | SWBPIPE owner decision | Before governance-phase host-side fixtures | **HOST** (answered: route (iv), none planned) |
| U-23 | Real per-surface exposure agreement | DEL-03-01 with host owner | Before exposure claims | **HOST** |
| U-25 | App act control and App person identity | DEL-01-04 (later undertaking) with DEL-04-03 | Before App capture fixtures | **LATER** |
| U-29 | Per-turn supplied-guidance identity in host loops | Host owner | Before host supplied-link evidence | **HOST** |
| U-30 | App-side run holds `UNRESOLVED{D6}` | Owner | When the governance phase is taken up | **LATER** (closed for the current phase by DECISION-4) |
| U-31 | Capture-after-arrival (I-8) vs counting a prior act bound to current content | Owner, with DEL-02-01 and DEL-04-01 | Before hold-machine fixtures run | **OWNER** — keep SP-6 (the person may have to repeat a grant whose content is already in force, R-16 (i)) or count a prior act on current content |
| U-32 | Whether a declaration carries an "on subject absent" path | DEL-02-01 | Before a subject-absent fixture runs | **NOW** — DEL-02-01's own choice; the default exists (EXEC §4.7 L726–L729, CH-24) |
| U-33 | V4-WF-05 flagged for the next accepted-basis update | Owner | Next accepted-basis update | **NOW** — done: PRD L254 as amended by SCA-V4-001 (`_ScopeChange/SCA-V4-001_2026-09-28_2155/`); close |
| U-35 | Per-subject content identity not met by SWBPIPE | SWBPIPE | Before host act-binding integration | **HOST** |
| `governed` (L389; FB-19 L1006) | New optional flag, "PROPOSED, R8-1" | — (integrator ruling R8-1) | — | **LATER**, with an owner-level choice inside it (A.5) |
| Standing labels | I-4 (L438), I-8 (L507), SB-4 (L596), run end (L544), §6.4 (L855) read "PROPOSED (W7)"; CG-6 (L359–L365) reads "PROPOSED (A1)" for PH-6 and PH-8 | — | — | **NOW** — R4-3 and R4-6 adopted the first and third; R4-4 and R4-5 keep standing PROPOSED; R8-11 item 1 confirmed PH-6 and PH-8 |
| "Not repaired here (routed to closeout C1)" (L120–L121): V1-C RF-3, RF-7, X-16 | register findings | — | — | **NOW** — RF-7 is answered by DEP-02-01-025 (N-16). RF-3's mirror rows are deferred to the register owners (DAG-003 HANDOFF, "Deferred supplier-side mirror rows (P2 O-3)"). Neither is a design item |

U-34 is closed in the file (L1039). VC-11's governance-phase AWAITING INPUT (L1067) is U-19, not counted twice.

**WD counts: NOW 7, OWNER 4, HOST 10, SPIKE 2, LATER 6. Total 29.**

## A.5 Design depth against the 60% description

WD exchanges seven contributions: (1) declared-part meaning; (2) checkpoint declaration meaning, dispositions, binding and the item rule; (3) compatibility outcome vocabulary and pass rule; (4) identity tuple, chain and holding library; (5) roles and the host seat; (6) the governing checkpoint constraint derivation (governance phase); (7) the responsibility map.

| Dimension | What WD has | What is missing |
|---|---|---|
| Interfaces | Semantic element tables for all five categories (§4.1 L230–L237, §4.2.2 L263–L270, §4.3.1 L375–L389, §4.4 L724–L730, §4.5 L734–L739); receivers and suppliers (§8); promised-vs-observed owners (§4.6) | (1) No carriage and no schema (U-01, U-02): consumers cannot parse anything. (2) No element by which a consumer observes production of a declared output of form "report or message to the person" (§4.4 L727), though reached-when kind (b) depends on it (L379, RW-2 L563–L565) and RW-1 forbids inference from model text (L557). (3) Harness-capability names (U-08). (4) Minor: tool references have no local name; a checkpoint names "a named required tool reference" (L379) by the operation identity only |
| States | Declared-part status: undeclared, declared empty, not established (§3.4 L218–L222). Compatibility outcomes (§4.2.4). Six dispositions with annotations (§4.3.4 L535–L542). Identity chain links (§6.2) | Declaration contract version handling beyond "newer → preserve and report" (§3.3 is two lines, L211–L214): no statement for an older version or for mixed elements. `governed` has values "yes" or absent only |
| Data | Every element has a meaning sentence; identity tuple (§6.1); binding table (§4.3.6) | No consolidated required/optional/cardinality table per category; no complete declared part in a selected representation; revision computation undefined (U-03); duplicate names (two checkpoints or outputs with one name) have no rule |
| Operating sequences | Reached-when rules RW-1…RW-4; the identity chain order; E2 run readings in WD-EX | No validation order for a declared part: which of FB-01…FB-19 is evaluated first and which wins when several apply. EXEC EV-1…EV-11 orders the tool check only. No author → register → select → check → run sequence at declaration level (registration is DEL-02-02's, later) |
| Failure behaviour | §11 FB-01…FB-19 (L986–L1006), each with required behaviour in both phases | Precedence among FB rows; duplicate-name and dangling-reference cases beyond FB-13; behaviour when the declared part and a Root `execution.json` disagree on compatible roles |
| Verification | §13: 45 designed cases, each tied to a VER and an example | None run and none runnable: there is no parser, schema or fixture format (L1050). No A6 or A7 case (A.2) |

**Structural choices still open that could force restructuring.**

1. **Carriage (U-01), with U-02 and U-03.** It decides what a parser reads, what "revision of the exact package content" covers (L820), what the EXEC carriage manifest summarizes (EXEC TR-4 L989), what TF-4 and TF-8 mean, and how DEL-02-02 registers a package. A companion file changes the package file set and therefore the revision; a delimited body section changes the prose file. Every consumer's parse step depends on it.
2. **Where the governance opt-in lives.** `governed` is PROPOSED as a per-checkpoint element authored in the declaration (L389). SoW TBD-004 names as owner "the owner, when a workflow needs enforced checkpoints", and the amended V4-WF-05 says "Enforced holds are applied later to the workflows that need them"; neither names a declaration flag. OWNER_ITEMS O-4 told the owner the flag "is still PROPOSED". Inference: an opt-in applied by the person, a host or an organization outside the declaration is a different structure from an authored flag. The cost of leaving it PROPOSED is small now, because an unrecognized element is preserved and reported (§3.4 L222) and LOOP, RS R8 and EXEC CR-9 only display the flag in the current phase.
3. **I-8 / SP-6 (U-31).** It changes which act satisfies which arrival, so it changes the expected results of R-9b, R-12b, R-16 (i) and every consumer's case that cites them.
4. **Harness-capability names (U-08).** Until they exist, every declared harness-capability requirement evaluates to *not established* (EXEC EV-3 L325), and in the current phase that is the only thing that can make an App-authored workflow fail its check on a capability it has.
5. **Placement (U-12, OI-014).** Open by design; it decides whether the reading types in §9 A-1…A-6 are shared code or parallel implementations.

## A.6 Joins (ACTIVE rows of DEL-02-01's `Dependencies.csv` whose other end is one of the 14)

Admitted or held is read from `DAG-003/DependencyEdges.csv` and `CandidateEdges.csv`. All held arcs are `SCC_UNRESOLVED` in SCC-002 and non-gating.

| Row (arc) | Direction; other end | Contribution named | DAG-003 | Supplier's Design content | Consumer's use | Finding |
|---|---|---|---|---|---|---|
| DEP-02-01-017 | consumer WD → DEL-03-01 | Open capability-catalog tool descriptors for required-tool declarations and VER-002 | held | C-v0.6 §3 elements 1–9 (L134–L150), §3.2 version equality (L205), §4.1 results (L224), §4.2 (L294), §5.1–§5.4 (L330–L400), §10 fixture (L615) | WD §4.1 L236, §4.2.1–§4.2.2 L248/L266, §4.2.4 L290–L296, §4.3.6 L578–L580, WD-EX fixture table | Present and used. Both sides are semantic only; C selects no serialization (C U-C1), so WD U-02 cannot settle the tool-reference encoding alone. WD's "State" column cites C-v0.5 at `d3cebd1cc` and says only "Current: C-v0.6" (L924); WD-EX cites "C-v0.4 §10" (WD-EX L76) |
| DEP-02-01-018 | consumer WD → DEL-04-01 | Adopted human-act distinctions incl. the D2/D3 rulings | **admitted** | ACT-v0.6 §2.1 A1–A14 (L235–L254), §4.1 closed list (L613), §4.2 referents (L623–L662), §2.3 act-declined | WD L145, L378, L414–L417, S-Q/S-R, §8 L922 | Present and used; the closed list and subject classes agree word for word. **Disagreement D-6:** ACT §2.7 (L464–L506) adds the A12 subclass "network-destination grant" with its own setting content (category or named destination, and scope). ACT ND-A1: "An operation-class A12 grants no destination". WD and ACT §4.2 both define the checkpoint "grant setting" subject as "classes, grant values, scope" only. Neither file says whether a declared A12 checkpoint may require a network-destination grant |
| DEP-02-01-019 | consumer WD → DEL-04-03 | Human-act and run record semantics | held | RS-v0.6 §4 R1, R2, R8, R11, R14 (L179–L194), §6.1 (L310), L-12 (L378), run-resumed event (L154), continues ⟨run⟩ (L167) | WD §4.3.1 "expected act evidence" L387, §4.5, §4.6, U-11 | The supplier has the contribution. **WD has not read it:** "Not read; via IR1-A and R2. Current: RS-v0.6" (L926). U-11 is therefore answerable now |
| DEP-02-01-020 | consumer WD → DEL-05-01 | Minimal-loop consumer requirements | held | LOOP-v0.6 §2.4 element table (L471–L498), §2.4.0 LP-1…LP-10 (L510), §2.4.1 (L555), §2.4.2 (L603), §6.2 (L1150), §10.1–§10.2 (L1328–L1349) | WD §8 L911, L927; §9 A-1, A-9 | Present. WD read LOOP-v0.2 (§9 A-1 L945 still says "LOOP-v0.2 §2.4 read at `28bd00499`") and checked later headers only (L927). **D-4:** LOOP's "on negative decision" row is phased ("Absent: in Phase 1 the agent follows the plan…; in the governance phase … the run stops", LOOP L491). WD's row for the same element is not: "Absent this element, the run stops at the checkpoint" (L385). **D-5:** LOOP §2.4.1 kind (b) counts "a completed agent message the declaration designates as that output"; WD §4.4 defines no such designation |
| DEP-02-01-021 | consumer WD → DEL-05-02 | Host-panel consumer requirements | held | PANEL-v0.6 §3.2 (L247), §3.5 W-5 (L306), §6 (L620) | WD §8 L912, L928; §9 A-10 | Present. **WD has not read PANEL:** "PANEL-v0.2 needs known through IR1-C J2/J3 (file not read)" (L19); "Via IR1-C. Current: PANEL-v0.6" (L928) |
| DEP-02-01-025 (N-16) | consumer WD → DEL-01-01 | Harness capability meaning, so OUT-002 harness-capability requirements refer to it | **admitted** | HOSTING-v0.6 §8 closing paragraph (L748–L751): "The 0.158.0 inventory in SPIKE §4 (170 client methods, 11 server-request kinds, 85 notifications in the TS experimental output) is the input to harness-capability naming owned by DEL-02-01 (V1-C AB-10); no naming is chosen here." §8.2 supplied-guidance evidence (L767) | WD §4.2.1 L249; U-08 L1021; §8 L929 ("Via IR1-C J6") | **Disagreement D-9.** The supplier supplies a protocol method inventory and assigns the naming to DEL-02-01. The SoW says the meaning is "supplied through DEL-01-01". WD says the supplier is `UNRESOLVED`. No file contains harness capability names. This arc is admitted, so it is a real blocker for the harness-capability part of OUT-002 |
| DEP-02-01-026 | consumer WD → DEL-02-03 | The statement of the current checkpoint phase and the governance-phase hold-support values | held | EXEC §2.1 PH-1…PH-10 (L208–L225), §2.2 GV-1…GV-5 (L235–L243), §3.5 (L340), §3.6 (L381–L484) | WD §4.3.0 (L327–L371), §4.2.4, §4.3.8 (L653–L720) | Present and mirrored rule for rule. WD pins EXEC one byte-state behind (A1-8). **D-1:** WD's pass-rule paragraph says any required reference that is *not established* "means the check does **not** pass" (L309–L311). EXEC §3.5 gives three results, and a required reference *not established* gives the result **not established**, not "does not pass" (L358–L362). **D-3:** standing labels differ (A.4 "Standing labels") |
| DEP-02-01-027 (N-20) | DOWNSTREAM: DEL-03-03 consumes WD | Declared checkpoint constraints, for carriage on X in the governance phase | held (the arc rests on this supplier-side row only) | WD §4.2.2 governing checkpoint constraint (L270); §9 A-12 (L956) | ADAPTER-v0.4 §5.1 and §5.3 cite "WD §4.2.2" and "WD I-7" (ADAPTER L479, L527, L585) | Present on both sides and consistent. WD's §8 receiver table and §10 lack DEL-03-03 (A.2 lags 2 and 3) |
| DEP-02-01-029 (**N-18**, new) | consumer WD → DEL-03-02 | Change-item content identities, per-item dispositions, all-items-decided, item-left events, applied-outcome object identities | held | P-v0.6 §3.1 (L140–L155), §4.3 (L322–L358), §9 applied-outcome association (L568), §13 "Provide to DEL-02-01 / DEL-02-03" (L709) | WD §4.3.6 L576, L579; §4.3.7 L612–L651 | Present and used; P §4.3 names WD §4.3.7 as the rule. WD read P-v0.5 by header only (L925). P's item-left causes add "refused — not permitted (re-resolution at application)", which WD L627 covers only as "host refusal". The reciprocal arc N-B3 (DEP-03-02-027) is in DEL-03-02's register |

Rows to EXTERNAL targets (SWBPIPE, OI-013, OI-014, the TBD-004 owner decision) are outside this section.

## A.7 Carried review items that name WD

| Item | Status | Evidence |
|---|---|---|
| V6 m-7: a **declared** held-actions element on an A5 or kind (a) checkpoint that neither shows "host operations only" nor marks an App-side step matches no HS row (WD §4.3.1, §4.3.8; EXEC HS-5) | **open** | WD L388 and the HS-5 row (L683) apply the default only to "a kind (b)/(c) checkpoint"; EXEC L408 still claims an "exhaustive partition" |
| C1-A residual: §8 and §9 self-citations read "v0.4" | **fixed** | L908 "Receives from WD-v0.6"; L920 "State at v0.5 (R6 in place); … updated at v0.6"; L958 "Allocation result at v0.6" |
| C1-A SC-02-01-1…6 (SoW corrections) | **applied** to the SoW by SCA-V4-001 as E-0201-01…06 (SC-02-01-6 in amended form, TBD-004) | `RV/RV-2_DEL-02-01.md`. WD itself has not followed (A.2) |
| C1-A register proposals R-02-01-g, -h, -i, -k | **applied** as DEP-02-01-025, -026, -029, -027 | `Dependencies.csv` |
| V9 N-1 (LOOP "on negative decision" unphased) | fixed in LOOP; **WD's identical row was left** (V9 judged it plan content) | LOOP L491 vs WD L385 |
| V9 S-1…S-3, N-2…N-7; V10 S-1…S-4, N-1…N-8 | none names WD | V10 N-8 lists the nine deliverables revised by R8-13; DEL-02-01 is not one |
| BASIS-ALIGN V11–V13; SCA002 V14–V16 | name no single Design file; carry "the 17 Design re-pins" as open | V13 L269–L273; V14 L224; `Handoff_State.md` L92 ("Re-pin to the amended texts at the next design pass"); DECISION-8, confirmed at SCA002 DECISION-2 |

## A.8 Recommended work on WD in this pass

1. **Re-pin the header and basis** to the amended docs, the current SoW (`ef360edf…`), R8 through R8-13 (`44bc9a8d…`), the intake decisions (`5fd780bf…`), the revised answers (`afb6e063…`) and the current sibling bytes by reference to GUIDE. Add SCA-V4-001, SCA-V4-002 and BASIS-ALIGN DECISION-7 (O-25) to the basis. Correct the V1-A abbreviation. [A.1]
2. **Re-word against the amended V4-WF-05 and V4-HI-42:** S-F, the Phase line, CG-7, I-7's closing sentences, FB-14, VC-11, U-34. Quote the current texts, drop "first half / second half", close U-33, and use "current phase" beside "Phase 1". [A.1, A.3]
3. **Follow the revised SoW:** name DEL-01-01 in §4.2.1; add DEL-03-03, DEL-03-04 and DEL-09-06 rows to §8; add the DEL-03-03 carriage row to §10; cite TBD-004, AX-005 and AX-006. [A.2, A.6]
4. **Read RS-v0.6, PANEL-v0.6, LOOP-v0.6, P-v0.6 and HOSTING-v0.6 directly** and replace "not read", "via IR1-C" and "header checked" in §8 and §9 A-1 with section citations; close U-11; turn U-17's internal half into a confirm-or-object request to the four consumers. [A.4, A.6]
5. **Decide the carriage and write the declared-part schema** (U-01, U-02) as PROPOSED, with the package file set and canonicalization rule for the revision (the semantic part of U-03). Support it with a bounded prototype that renders and parses E1, E1d, E5 and E6. [A.4, A.5]
6. **Name harness capabilities** (U-08) from the 0.158.0 generated schema and HOSTING §8, as PROPOSED names scoped to the pin. [A.4, A.5, A.6 D-9]
7. **Add the output-production element** that reached-when kind (b) needs, agreed with LOOP §2.4.1 and with EXEC's App-side table (C.8 item 6). [A.5, A.6 D-5]
8. **Settle the four wording disagreements:** the pass-rule sentence against EXEC's three results (D-1); the phase label on "on negative decision" (D-4); standing labels (D-3); the A12 network-destination subclass (D-6). Close V6 m-7 with EXEC. [A.6, A.7]
9. **Add a validation order** over FB-01…FB-19 and rules for duplicate names. [A.5]
10. **Decide U-32** ("on subject absent"). [A.4]

**Not in this pass, and why.**

- The governance-phase definitions (§4.3.8, the constraint carriage, D6, U-30): phased by DECISION-4; re-label only where item 2 requires.
- Host-dependent items (U-05, U-05b, U-07, U-09, U-13, U-15, U-19, U-23, U-29, U-35): host joins are deferred (DECISION-3).
- U-10 and U-25: their owners, DEL-02-02 and DEL-01-04, are outside the 14.
- U-12, U-16, U-31, U-05c and the place of the governance opt-in: owner decisions. Prepare the question; do not choose.
- Running §13: no consumer exists. The prototype in item 5 is a design aid, not OUT-004.

---

# Part B — DEL-02-01 `EXAMPLES.md` (WD-EX-v0.6)

## B.1 Pins

30 full sha256 values and one abbreviation. None equals current Design or SoW bytes; 11 of the full values equal current run-record bytes; the rest are historical and verified.

| # | Pin (WD-EX location) | Status | Current value |
|---|---|---|---|
| B1-1 | Basis "repo 6e18505e3" for PRD V4-WF-01…06 and HOST_INTEGRATION V4-HI-40…42, -70/71 (L6) | **STALE** | as A1-1 |
| B1-2 | `ScopeOfWork.md sha256 080d7f5a…` (L6) | **STALE** | `ef360edf…2f17` |
| B1-3 | R8 `d4c34233…` (L7) | **STALE** | `44bc9a8d…0e6b` |
| B1-4 | Intake `OWNER_DECISIONS.md` `a5ccab0d…` at `bcc25624d` (L7) | **STALE** | `5fd780bf…0b2` |
| B1-5 | `RELAY_ANSWERS_SWBPIPE.md` `6f01add3…` and "unchanged" (L7) | **STALE** | `afb6e063…0e74` |
| B1-6 | EXEC-v0.4 "working tree, sha256 d32be377…" (L7) | **STALE** as bytes | `092f2486…08ff` |
| B1-7 | "Current sibling versions after R8, as committed at `7a1508452` … byte pins are in GUIDE-v0.3's input table" (L7) | labels current; byte state **STALE** | as A1-9 |
| B1-8 | Phase line and change row: "V4-WF-05's first half is phased … flagged for the next accepted-basis update (WD U-33)" (L4, L17) | **STALE** text | as A.1; the basis is amended |
| B1-9 | First-run `OWNER_DECISIONS.md` `a9869129…`; R1…R6; V2, V3-A, V3-B, V4-A; INTAKE_MAP (L6, L7) | current | same |
| B1-10 | "Fixture references (C-v0.4 §10; FXA-n were FA-n in C-v0.3)" (L76) and V-GR1 "C-v0.5 §10.4" (L92) | version label behind; the header says the fixture is "carried in C-v0.6 §10" (L7) | C-v0.6 `8282c003…5ce4`; its §10.1–§10.7 headings exist (C L627–L801) |
| B1-11 | Root sources at `6e18505e3`: `workflows/create-workflow/WORKFLOW.md`, `workflows/project-dag/execution.json` (L6, E5 L366, E6 L382) | current | no diff since `6e18505e3` |
| B1-12 | WD-EX's own v0.1…v0.5 hashes (L2); sibling hashes of earlier passes (L7) | historical, all verified | — |

WD-EX quotes no requirement text beyond the V4-WF-05 phrase. **Stale-pin count for WD-EX: 8** (B1-1…B1-8).

## B.2 ScopeOfWork alignment

WD-EX serves OUT-001, OUT-002 (explanatory examples), OUT-004 (fixture subjects) and REQ-001…REQ-004 (L5).

| SoW item | Where WD-EX answers | Standing |
|---|---|---|
| OUT-002 "explanatory examples expressing expected inputs, required host tools, checkpoints requiring human acts, returned outputs and evidence alongside prose method guidance" | E1 (L103–L230): prose, inputs, tools, checkpoints, held actions, outputs, evidence, roles | developed for one workflow. "Illustrative rendering, not a selected carriage or wire format" (L71–L74). E1b, E1c and E1d show only a checkpoint table each |
| REQ-001 / AC-001 (roles, seat, host guidance, origins) | E3 (L327–L347), E4 (L351–L362) | developed; seat role is a "fixture choice" (L229) |
| REQ-002 / AC-002 (five categories; open schemas; supplier identified) | E1; E5 (L366–L376); E6 (L380–L390); E7 (L394–L405) | developed as meaning. No example declares a harness-capability requirement as a declared part (L-WDEX-15 is one row of E8, L436). Input kinds "file or document supplied to the run" and "output of another identified workflow run" (WD L234) have no example |
| REQ-003 / AC-003 (execution, acceptance, checking, approval, reliance distinct; each with actor, subject, evidence) | E2 runs R-1…R-E1b′ (L295–L323), E1b | **partial.** A5, A4, A10, A12, A14 and act-declined are exercised. **A6 (engineering approval) and A7 (professional reliance) are not**: the only mention is "Not declared: A6 *approve* (engineering approval) and A7 *rely*" (L204). FX-PIPE-01 has no operation that captures A6 or A7 (OP-C6 A4, OP-C7 A5, OP-C8 A10; L86) |
| REQ-004 / AC-004 (origin and revision across App and host; promised vs observed) | E3, E4, R-6, R-13 | developed |
| VER-003 "for a checkpoint in the governance phase, any actual hold" | E8 governance-phase columns (L427–L438) | designed "as if declared `governed`"; "no fixture declares the flag" (L4, L200–L202). VC-45's three variants are not written out as examples |
| TBD-004 | E8 two-part statement (L411–L425) | developed |

Lags against the revised SoW: the SoW pin (B1-2); "Phase 1" against "current phase"; nothing else.

## B.3 Amended basis

| Amended item | Where WD-EX touches it | Agreement |
|---|---|---|
| V4-WF-05 | L4, L17, L288–L293, E8 L411–L417 | Intent agrees. The "first half … flagged" wording is obsolete (B1-8) |
| V4-HI-42 | R-5a (L301), R-5b (L302), by way of WD I-7 and "D2: no grant widens past a declared checkpoint" | Agrees in content: the current phase reads the constraint as plan guidance and records what the host does. The phrase "R8-11 item 2, WD U-34 closed" should also cite the amended V4-HI-42 and O-25 |
| V4-EXM-22 | not cited | R-5c and the E8 phase split agree with the amended scenario |
| V4-HI-70 | Basis L6 only | no dependent text |
| V4-HOST-01/02, V4-ARC-11/12, V4-EXM-23, "local-first" | not cited (grep) | not touched. R-15 (L319) concerns the App's Codex tool permission, which DECISION-5 leaves alone |

## B.4 Open items

The file's UNRESOLVED table (L473–L485) says "Same register as WD-v0.6 §12" and lists the items that shape the examples. Classes follow A.4.

| ID | Effect on the examples (file) | Class |
|---|---|---|
| U-01 / U-02 | tables are illustrative renderings | SPIKE |
| U-03 | ⟨rev-A2⟩, ⟨rev-3⟩ are labels | LATER |
| U-30 | E8 governance-phase rows | LATER |
| U-19 | R-5a, R-5b governance phase AWAITING INPUT (L301–L302) | HOST |
| U-05b | R-9 (iii) stays waiting | HOST |
| U-31 | R-9b, R-12b, R-16 (i) apply I-8 as PROPOSED | OWNER |
| U-05c | R-4 re-requests the whole scope | OWNER |
| U-25 | App-side positive capture not shown | LATER |
| U-09 | E1 compatible roles are a fixture choice | HOST |
| U-10 | E4 step 3 left open | LATER |
| U-15 / U-05 | FX-PIPE-01 entries are not the selected operation | HOST |
| `governed` not declared by any fixture (L200–L202) | hold readings are "as if" | LATER |

**WD-EX counts: NOW 0, OWNER 2, HOST 4, SPIKE 1, LATER 5. Total 12.** All repeat WD items.

## B.5 Design depth

| Dimension | What WD-EX has | What is missing |
|---|---|---|
| Interfaces | One full declared part (E1) and three checkpoint fragments; the fixture reference table to C §10 (L78–L94) | A declared part in the selected carriage; a harness-capability requirement; the two unexemplified input kinds; an output whose production is a message, with the element that marks it (A.5) |
| States | 27 run readings in E2 giving dispositions per checkpoint; E7 outcomes; E8 two-part values | A6 and A7 arrivals; a `governed` variant |
| Data | Identity table E3 (L332–L340) | Real revision values (U-03) |
| Operating sequences | The E1 prose method; E2 rows read along C's timeline | A current-phase App-run sequence (the default surface of E2 is "the host (embedded loop)", L284–L285); only R-15 and E8 rows run from the App |
| Failure behaviour | Negative readings ("Incompatible reading exposed" column); E5, E6, E7 | — |
| Verification | The example-to-VC map (L491–L504) | Nothing runnable |

Structural dependence: every table will be re-rendered once U-01 is decided. L-WDEX numbering is cited by EXEC (L29–L30), so labels must stay stable.

## B.6 Joins

WD-EX carries no register of its own. It is the fixture half of three joins in A.6:

- **DEP-02-01-017 (DEL-03-01).** WD-EX uses C §10.1–§10.4 identifiers (FXA-1…FXA-5, OP-C1…OP-C12, T1…T17, V-S1, V-CP1, V-NP1, V-R1, V-X1, V-OU1, V-ED1, V-GR1). C-v0.6 §10 has those headings. I did not compare every identifier's content against C-v0.6.
- **DEP-02-01-026 (DEL-02-03).** E8's governance-phase values (L429–L438) equal EXEC's fixture classification (EXEC L425–L430) and MT-2, MT-15, MT-16; V9 Check 3 found the same. EXEC cites the WD-EX local cases "by content" with WD-EX-v0.4 labels (EXEC L1073–L1075).
- **DEP-02-01-029 (DEL-03-02, N-18).** R-2, R-7, R-7b, R-13, R-13b and R-14 use P's per-item dispositions, item-left events and applied outcomes; P §14 uses the same timeline.

## B.7 Carried review items that name WD-EX

| Item | Status | Evidence |
|---|---|---|
| V6 m-5: the E8 note states the derivation and the kind (b)/(c) default without the A5-precedence clause | **open** | L452–L456 is unchanged in substance; the clause "(an A5 checkpoint takes the derivation above, per EXEC §3.6's definition)" exists only in WD L388 |
| EXEC F-25 / C1-A: adopt an "optional host operation absent" case for OP-C5, or keep OP-C12 as the single example | **open, not dispositioned** | WD-EX E7 has only L-WDEX-13b for OP-C12 (L400); EXEC MT-4 keeps L-EXEC-26 (EXEC L1095); EXEC F-25 has no disposition (EXEC L1282) |
| V4-A m-3 / R6-2 (R-16 (iv): ⟨set-1⟩ stays in force) | fixed | L320 |
| V9, V10, V11–V16 | none names WD-EX | — |

## B.8 Recommended work on WD-EX in this pass

1. Re-pin the header as for WD; re-word L4 and L17; re-point the fixture table to C-v0.6 §10 after reading it. [B.1, B.3]
2. After WD item 5: render E1 (and the E1b, E1c, E1d checkpoints) in the selected carriage as the normative example, keeping the tables as explanation. [B.5]
3. Add an A6 and an A7 checkpoint example with run readings. This needs fixture operations that capture A6 and A7, which is DEL-03-01's fixture (C §10); until C has them, use `L-WDEX-n` local cases with reasons. [B.2]
4. Write out the `governed: yes`, absent and unrecognized variants (VC-45), a harness-capability requirement as a declared part, and one example each for the two missing input kinds. [B.2, B.5]
5. Close V6 m-5 and disposition F-25. [B.7]

**Not in this pass:** recomputing governance-phase values (nothing changed them); SWBPIPE-shaped examples (host joins deferred); running anything.

---

# Part C — DEL-02-03 `EXECUTION_COMPATIBILITY.md` (EXEC-v0.4)

## C.1 Pins

40 full sha256 values and 21 abbreviated ones. The only value equal to current bytes under a `Design/` folder is the generated schema `34f28a48…f458`. 11 equal current run-record bytes. The rest are historical and verified, with two mistyped abbreviations.

| # | Pin (EXEC location) | Status | How checked | Current value |
|---|---|---|---|---|
| C1-1 | "Basis: repo 6e18505e3 (accepted basis)" for PRD, HOST_INTEGRATION, EXAMINATION, ARCHITECTURE (L6) | **STALE** | as A1-1 | as A1-1 |
| C1-2 | `ScopeOfWork.md sha256 9a921ba5…b7fb` (L6) | **STALE** | `9a921ba5` is the SoW at `6e18505e3`…`7a1508452` | `0006521b9bd96ea7ec98ecc5d9e6db794ecb331440c276006b444e7ee319726d` |
| C1-3 | SCC-CASE-002 `Case_Datasheet.md sha256 6acdc6c4…71a6` (L6) | **STALE** bytes | current file has 54 added lines ("Successor observation" sections from DAG-002 and DAG-003); no line removed | `a12abfaf…4d5c`. The M1 rows EXEC relies on are unchanged (diff shows additions only) |
| C1-4 | R8 `d4c34233…` (L8) | **STALE** | as A1-3 | `44bc9a8d…0e6b` |
| C1-5 | R8 `9877da07…` (L9) | historical | at `bcc25624d` | — |
| C1-6 | Intake `OWNER_DECISIONS.md` `a5ccab0d…` at `bcc25624d` (L6) | **STALE** | as A1-5 | `5fd780bf…0b2` |
| C1-7 | Intake `BRIEFS.md` `3e33ba26…` (L9) | **STALE** (closed pass) | as A1-6 | `6f32809d…03b4` |
| C1-8 | `RELAY_ANSWERS_SWBPIPE.md` `6f01add3…61c7`, "unchanged" (L8, L9, L22) | **STALE** | as A1-7 | `afb6e063…0e74` |
| C1-9 | "Current sibling versions after R8, as committed at `7a1508452` with A6's in-place R8-12 edits" incl. WD-v0.6 and WD-EX-v0.6 (L8) | labels current; byte state **STALE** | WD at `7a1508452` is `fce565ed…`, now `43a9962f…`; eight other siblings changed at R8-13 | GUIDE-v0.3 input table |
| C1-10 | First-run `BRIEFS.md` "(working copy, sha256 58de4a2c…)" (L10) | historical | blob at `1c36b6d97`…`e20a3ae8d` | current `35cbc974…` |
| C1-11 | First-run `OWNER_DECISIONS.md` `a9869129…8ad2c` (L6, L25); R1…R6; V3-A, V3-B, V4-A; INTAKE_MAP | current | recomputed | same |
| C1-12 | Generated `codex_app_server_protocol.v2.schemas.json` `34f28a48…f458` (L21) | current | recomputed | same |
| C1-13 | "ADAPTER-v0.3 977d6a26…1f44" (L34) | **mistyped** | the only blob with that prefix is ADAPTER at `375c3970c`/`2f42fba02`, ending `…46f44` | `977d6a262b40…be1846f44` |
| C1-14 | "PANEL-v0.4 cb71bc4b…4c84419" (L32) | **mistyped** | the only blob with that prefix is PANEL at `cc58211c5`/`8fb51f07f`, ending `…ce84419` | `cb71bc4bd3d8…573ce84419` |
| C1-15 | EXEC's own v0.1…v0.3 (L2); Wave-1 v0.3 set at `ba0b37123` (L11–L21); v0.4 set at `8fb51f07f` (L32); R6 and R7 working states (L33–L34) | historical, all verified | each found at the named commit | — |
| C1-16 | §9.1 supplier "State" cells (L1193–L1204): "WD-v0.4 and WD-EX-v0.4 read at `8fb51f07f` … Current: WD-v0.6"; likewise C, P, ACT, AS, RS, LOOP, HOSTING, ADAPTER | labels current | each "Current:" label equals the current header | EXEC records that WD-v0.6 was written "after this file in the same A1 pass" (L1193): EXEC has not read the final WD-v0.6 §4.3.0 and §4.3.1 |
| C1-17 | §3.6 fixture table heading "Declared held actions (WD-EX-v0.5; unchanged in WD-EX-v0.6)" (L425); §7 "From C-v0.4 §10 … carried in C-v0.6 §10", "From WD-EX-v0.4 (carried in WD-EX-v0.6 …)" (L1059–L1070) | version labels behind, carried by statement | the WD-EX E1, E1c and E1d held-action lines (WD-EX L195–L198, L256–L258, L276–L278) match the table | — |

**Stale requirement and SoW texts quoted in EXEC.**

| EXEC text and location | Text EXEC assumes | Current text |
|---|---|---|
| PH-10 (L225): "Its first half ('the product holds a workflow's declared checkpoints … the run waits') is **phased to the governance layer, not withdrawn**. … Flagged for the next accepted-basis update"; header Phase line (L5); change row (L49); E-B (L170) | old PRD V4-WF-05 (quoted in A.1) | amended PRD L254 V4-WF-05 (quoted in A.1). The quoted phrase no longer exists; the update has happened |
| E-B (L170): "checkpoints override autonomy", cited to V4-HI-42; U-E24 (L1319): "V4-HI-42 [is] guidance in Phase 1"; §4.7 (L706–L707): "V4-WF-05's first half … and V4-HI-42 make the run wait for the person's act" | old HI V4-HI-42 (quoted in A.1) | amended HI L139 V4-HI-42 (quoted in A.1): the run's waiting is itself phased |
| §4.7 (L708–L709): "SoW AC-002 keeps it waiting 'until evidence shows that required act actually occurred'" | old AC-002: "A declared checkpoint requests its named human act and remains waiting despite direct-operation autonomy, interruption or replay until evidence shows that required act actually occurred." | current AC-002: "A declared checkpoint requests its named human act, and the act is not recorded as done — despite direct-operation autonomy, interruption or replay — until evidence shows that the required act actually occurred. In the current phase no hold is claimed or enforced; for a workflow that takes up the governance phase, the checkpoint also keeps the run waiting until that evidence." |
| F-29 (L1291): "The DEL-02-03 SoW wording assumes the run waits at a checkpoint … No SoW text is changed here" | SoW at `9a921ba5` | the SoW was revised by SCA-V4-001 (E-0203-01…13; RV-2 return lists each block as "EXEC F-29"). The finding is met |
| VC-E-10 (L1340): "against SoW CLM-001…003, REQ-006/007, TBD-001…005" | five TBDs | the SoW has TBD-001…TBD-006. (The SoW's own REQ-007 and VER-006 still say "TBD-001 through TBD-005"; that is a SoW matter, not written in this run) |
| Basis list "EXAMINATION.md V4-EXM-14, V4-EXM-22" (L6) | old V4-EXM-22 | amended EXM L147 (quoted in A.1) |

**Stale-pin count for EXEC: 12** (C1-1, -2, -3, -4, -6, -7, -8, -9; the texts V4-WF-05 and V4-HI-42; the AC-002 quotation with F-29; the TBD range in VC-E-10). Plus two mistyped abbreviations (C1-13, C1-14).

## C.2 ScopeOfWork alignment

Current SoW: `0006521b…726d`. SCA-V4-001 revised the Purpose sentence, the SOW-052 row, OUT-003, CLM-002, CLM-003, REQ-002, REQ-006, AC-002, AC-007, VER-002, one matrix cell, TBD-001, TBD-002, and added TBD-006 and AX-004. SCA-V4-002 appended the "consumes, and does not define" sentence to CLM-002 and added AX-005.

| SoW item | Where EXEC answers | Standing |
|---|---|---|
| OUT-001 "Required-tool and checkpoint receiving behavior in code" | §3 (L272–L516), §2.1 (L208–L233), §4 (L520–L914), §5 (L918–L937) | **partial: definition only**, as the header says ("definition only, no code", L4). The required-tool report is developed. The current-phase checkpoint behaviour is defined by subtraction from the governance-phase machine (C.5) |
| OUT-002 transfer and adaptation contract | §6.1–§6.7 (L943–L1052) | developed |
| OUT-003 "Missing-tool, checkpoint-recording (with governance-phase hold cases retained) and source-preserving round-trip fixtures with local candidate evidence" | §7.1 MT-1…MT-16, §7.2 CH-1…CH-30, §7.3 RT-1…RT-11 | **designed only.** "No code, fixture runner, host or act exists" (L1326). The two-column form matches the revised wording |
| CLM-001 | §2 table (L195–L206), §9.1 L1193 | developed |
| CLM-002 (owners; the three "consumes" statements) | §9.1 (L1191–L1204), §4.4 (L589–L602), §5 | **partial.** (a) DEL-03-02 outputs: developed (§4.4 L593, L598; §4.11). (b) "DEL-03-03's observations of checkpoint arrivals and act records on the external channel, which this slice records": §9.1 lists "§7.7 checkpoint observation on X" (L1201), but §4.4 names the arrival supplier as "App observation / loop (LOOP §2.4.1); host outcome (P §9)" (L591) and does not name ADAPTER §7.7. (c) DEL-01-04's act control and person identity: developed as requirements (CAP-2 L927, CAP-8 L933), AWAITING INPUT (CH-23 (ii)) |
| CLM-003 (no App-side hold point needed in the current phase; D6 re-opens with the governance phase) | §2.3 lead (L247–L253), HD-4 (L554–L561), U-E1 | developed |
| REQ-001 | §3.1–§3.8 | developed; harness capabilities unresolved (EV-3 L325) |
| REQ-002 ("request the required human act and record it as done only when the person performs it"; "Interrupted or replayed history must preserve the checkpoint's identity and actual disposition") | PH-4 (L219), PH-6 (L221), §4.1, §4.12 | **partial**; see lags 1 and 2 |
| REQ-003 (faithful recording; distinct acts; lapse) | §4.5 SP-1…SP-8 (L609–L618), §5 CAP-1…CAP-9, PH-8 (L223), §4.7 RH-1 | developed |
| REQ-004 | §6.1–§6.4, §6.6, §6.7 | developed; host links AWAITING INPUT |
| REQ-005 | §6.5 HR-1…HR-7 | developed as definition; registration is DEL-02-02's |
| REQ-006 (excluded acts, now including "grant display definition to `DEL-04-02`", "supplier observation to `DEL-01-01`", "proposal/outcome semantics to `DEL-03-02`", "external adapter construction and carriage to `DEL-03-03`", "App act control construction to `DEL-01-04`") | §10 (L1221–L1235) | **partial**; see lag 3 |
| REQ-007 (open decisions at their points of need) | §8 (L1169–L1183), UNRESOLVED (L1299–L1320) | developed |
| AC-001 | VC-E-01 | designed |
| AC-002 | VC-E-02, VC-E-03, VC-E-13 | designed; agrees with the revised two-part wording |
| AC-003 ("Execution, acceptance, checking, approval and reliance remain independently attributable") | VC-E-05, VC-E-06, VC-E-07 | **partial**: no case has an A6 or A7 checkpoint ("A6"/"A7" do not occur in §7, by grep). VER-003 asks for "independently evidenced checking/approval/reliance" |
| AC-004, AC-005 | VC-E-08, VC-E-09 | designed |
| AC-006 | VC-E-10 | designed; stale TBD range and lag 3 |
| AC-007 | VC-E-11, RT-11 | designed |
| VER-002 "Hold cases … are exercised only for a workflow that takes up the governance phase" | governance-phase columns of §7.1 and §7.2 | designed for fixtures read "as if declared `governed`"; "No FX-PIPE-01 fixture declares the flag" (GV-5 L243). No fixture workflow takes up the governance phase |
| TBD-001…TBD-005 | E-I, E-J (L177–L178); U-E2, U-E17 | developed |
| TBD-006 | §2.2 GV-3 (L241); U-E1 (L1301) | developed; not cited by ID |

**Places where EXEC lags or contradicts the revised SoW wording.**

1. **Recording modality (REQ-002 vs PH-6).** The SoW requires that history "must preserve the checkpoint's identity and actual disposition" and AC-002 requires that the act "is not recorded as done … until evidence shows" it occurred. PH-6 says a checkpoint's arrival and answering act "**may** be recorded" (L221), and the closing paragraph of §2.1 lists what Phase 1 "keeps" without saying it is required (L227–L233). Inference: a disposition cannot be preserved for an arrival that was not recorded, so the SoW implies "shall record"; EXEC does not say so.
2. **Who requests the act (REQ-002 "request the required human act").** The transition table issues the request at arrival ("act request issued; run holds (governance phase…)", L634). §2.1 and the case tables put the request with the agent in the current phase (CH-1 "the agent pauses as its plan says", L1118; CH-7 "The agent re-requests A4 as its plan requires", L1124). No rule states which party issues the request in the current phase or what the App shows.
3. **REQ-006 vs §10.** §10 has no row for the grant display definition (DEL-04-02) and none for supplier observation (DEL-01-01). Both suppliers appear in §9.1 (L1197, L1200).
4. **F-29, F-10 and F-11 are recorded as open or carried** (L1257–L1258, L1291). The SoW now answers all three: CLM-003's new sentence (F-10), TBD-001/TBD-002 (F-11; rows DEP-02-03-015 and -016 are RETIRED), and the REQ-002/AC-002/VER-002/OUT-003 rewording (F-29).
5. **§4.7 "Why re-hold"** quotes the old AC-002 (C.1).
6. **Terminology** "Phase 1" against the SoW's "current phase".

## C.3 Amended basis

| Amended item | Where EXEC touches it | Agreement |
|---|---|---|
| V4-WF-05 | L5, L49, E-B L170, PH-3 L218, PH-4 L219, PH-10 L225, §4.7 L706, F-29 L1291 | Intent agrees: PH-1…PH-10 states the amended sentence clause by clause. Wording lags as in A.3 ("first half / second half"; obsolete quotation; "flagged") |
| V4-HI-42 | E-B L170; change rows L61–L62; §4.7 L707; CH-27 L1144; F-30 L1292; U-E24 L1319 | **Wording disagrees** in the same way as WD: EXEC calls V4-HI-42 "guidance in Phase 1"; the amended text has a binding current-phase part that EXEC carries as PH-4. §4.7's use of V4-HI-42 as a reason the run waits no longer matches the text, which phases the waiting |
| V4-EXM-22 | Basis L6; SoW citations | EXEC's two-part cases (CH-1, VC-E-02) match "stopping the run … is examined only for a workflow that takes up the governance phase" |
| V4-HI-70 | Basis "-70/71" (L6); HR-6 cites V4-HI-71 (L1029) | No conflict. The §6.1 "observed behavior" link for host runs (L960) does not mention the destinations a host agent contacted, which V4-HI-70 now puts in the run record; that element is RS R15's and LOOP's |
| V4-HOST-01, V4-HOST-02, V4-ARC-11, V4-ARC-12, V4-EXM-23, "local-first" | not cited (grep). "Model destination" appears at CR-14 (L315), §6.1 *supplied* (L958) and RT-5 (L1157) | Not touched, and not in conflict: CR-14 and RT-5 concern the App's own Codex under D5, which the amended V4-ARC-12 property leaves with "the person's Codex configuration". Not addressed anywhere in EXEC: in a host loop, a required tool whose use needs a network destination depends on the person's allow list (LOOP §5.1.1); the compatibility outcomes have no value for that, and no file in this row says whether the check should report it. Inference: outside V4-WF-04 as written; worth one sentence |

## C.4 Open items

Owner and point of need are as the file states them (L1299–L1320 unless another line is given).

| ID | What is open | Owner (file) | Point of need (file) | Class |
|---|---|---|---|---|
| U-E1 | App-side run holds `UNRESOLVED{D6}` | The owner; then App/shared owners (OI-014) | When the governance phase is taken up | **LATER** |
| U-E23 | App-only checkpoints in App runs (HS-5) | The owner, with D6 | Before any governed checkpoint with an App-side held action is offered as enforced | **LATER** |
| U-E2 | Placement of the hold machine and required-tool check (`{OI-013}`, `{OI-014}`) | Shared contract owner with SWB implementation owner; App/shared owners | Before shared/host implementation boundary contracts | **OWNER** for the App-side and sharing half (OI-014); the host half is HOST |
| U-E3 | Multi-row A4 after partial lapse (CH-8 HELD) | DEL-04-01 with the Owner | Before re-hold and lapse fixtures run | **OWNER** (same choice as WD U-05c) |
| U-E4 | SP-6 vs counting a prior act on current content; cost F-23 | The owner, with DEL-02-01 and DEL-04-01 | Before hold-machine fixtures run | **OWNER** (same choice as WD U-31) |
| U-E7 | "On subject absent" path in the declaration | DEL-02-01 | Next comparison | **NOW** (WD U-32) |
| U-E8 | App person identity scheme; App act control construction | DEL-01-04 (later) with DEL-04-03 | Before App capture fixtures | **LATER** |
| U-E9 | Proxy control for host-content acts through the App | Host owner, SQ-25 | Before any App proxy is offered | **HOST** (answered: none) |
| U-E10 | Harness capability names | DEL-02-01 with DEL-01-01 | Before App-side required-tool check | **NOW** (WD U-08; same records) |
| U-E11 | Version compatibility statements | Host owner with DEL-02-01 | Before version fixtures against a real host | **HOST** |
| U-E12 | Host capture-evidence reference | SWBPIPE owner decision | Before host act-recording integration | **HOST** |
| U-E13 | Constraint receipt on the host route (governance phase) | Host owner with DEL-03-02 | Before CH-27's governance-phase host case | **HOST** |
| U-E14 | Host library receipt, adaptation evidence, run records | SWBPIPE owner decision | Before RT host-side cases | **HOST** |
| U-E15 | Per-turn supplied guidance in host loops | Host owner | Before host supplied-link evidence | **HOST** |
| U-E16 | Carriage of the declared part; carriage-manifest representation; revision algorithm | DEL-02-01 with DEL-04-03 | Before OUT-002 schema and transfer code | **SPIKE** (the WD U-01 prototype; the manifest, TR-4, should be rendered in the same exercise) |
| U-E17 | First connected operation (`{OI-021}`); MT-13 and CH-11 production HELD | Owner via outside SWB session | Before connected-activity SoW | **HOST** |
| U-E18 | Extension promise (`{OI-003}`) and real exposure | Owner with host contract owner; SQ-11 | Before exposure claims | **HOST** |
| U-E19 | Selection slot policy and host precedence; registration as an act | DEL-02-02 (later) with DEL-02-01, DEL-04-01 | Before host-origin discovery in the App | **LATER** |
| U-E25 | Per-subject content identity not met by SWBPIPE | SWBPIPE | Before host act-binding integration | **HOST** |
| F-10 (L1257) | "Carried to C1 as a SoW gap" | — | — | **NOW** — closed by SoW CLM-003 (SCA-V4-001 E-0203-05) |
| F-11 (L1258) | "Carried to C1": OI-001/002 still called open | — | — | **NOW** — closed by SoW TBD-001/TBD-002; DEP-02-03-015/-016 RETIRED |
| F-12 (L1259) | Changed-draft return to DEL-02-02 uncompared | DEL-02-02 (later) | — | **LATER** |
| F-24 (L1281) | RS R11 should carry the turn initiator | DEL-04-03 | — | **NOW** — adopted: RS-v0.6 change row R6-5 (RS L58) and R11 (RS L190, L299–L303) |
| F-25 (L1282) | Optional-absent case choice in WD-EX E7 | DEL-02-01 | — | **NOW** (B.7) |
| F-27 (L1284) | LOOP §2.4.4 residual after-observation limit to be an evidence limit; EXEC CR-12 to list it | DEL-05-01; EXEC | — | **NOW** — LOOP-v0.6 change row R5-1 says "with residual limits stated per kind" (LOOP L150); CR-12 (L313) does not list it |
| F-28 (L1285) | The declaration has no element naming held actions | DEL-02-01 | — | **NOW** — the element exists (WD L388, R6-1); the finding is not marked closed |
| F-29 (L1291) | SoW wording assumes the run waits | — | — | **NOW** — closed by SCA-V4-001 |
| F-31 (L1293) | PH-6 and PH-8 "for the integrator to confirm or amend" | integrator | — | **NOW** — R8-11 item 1 confirms both; PH-8 is updated (L223), PH-6 still reads "PROPOSED (A1)" (L221) |
| Standing labels | "PROPOSED (W7)": HP-4 (L260), the HS-5 default (L415), §4.12 principle (L871), §5 (L918), §6.3 (L982), §6.5 (L1020); standing PROPOSED: §4.9 (L745), SP-6 (L616) | consumers and the integrator ("open to comparison and to owner revision", L153–L154) | — | **NOW** — a comparison by the receivers named in §9.2 can confirm or object |

F-14 equals U-E3 and F-23 equals U-E4; not counted twice. AWAITING INPUT and HELD case states (CH-8, CH-11, CH-23 (ii), CH-27 on E, CH-28, MT-13, RT-1, RT-2, RT-4, RT-5) each rest on an item above.

**EXEC counts: NOW 11, OWNER 3, HOST 9, SPIKE 1, LATER 5. Total 29.**

## C.5 Design depth against the 60% description

EXEC exchanges six contributions: (1) the compatibility report; (2) current-phase checkpoint recording (arrivals, acts, lapses, labels); (3) the governance-phase hold machine and hold support (retained); (4) App act-capture requirements; (5) the transfer trace and carriage manifest; (6) the fixture evidence account for DEL-09-06.

| Dimension | What EXEC has | What is missing |
|---|---|---|
| Interfaces | Report elements CR-1…CR-14 (L302–L315); inputs consumed (§3.2 L288–L296); events consumed with suppliers (§4.4 L589–L602); trace links with evidence owners (§6.1 L948–L960); supplier and receiver tables (§9) | (1) **No App-run evaluation of reached-when.** WD assigns it: "the loop evaluates it in hosts (DEL-05-01), DEL-02-03 in the App" (WD L379). LOOP has the host table (LOOP §2.4.1 L561–L565; kind (b) at L564). EXEC has only "App observation" (L591) and the arrival-event definition (L536). It does not say which native item delivered by HOSTING (HOSTING §6.7 L570–L573) or which ADAPTER §7.7 observation is the arrival for kinds (a), (b) and (c). (2) No App-side component interface: which App part computes the report, which records arrivals, and what each hands to DEL-01-02 and to the RS writer. EXEC "selects no … process/thread placement or shared-component placement" (L142–L144) |
| States | Per-arrival dispositions and a full transition table (§4.3 L575–L582, §4.6 L632–L651); run end and continuation (§4.9); report currency (§3.7); A12 control relations (§4.10) | The current-phase model has no table of its own. It is "What Phase 1 keeps from §4" (L227–L233) plus parentheticals in governance-phase rows (for example L634, L642, L645). A reader must subtract HD-1…HD-4, RH-2…RH-7, AR-2, RP-4 and part of RP-5 and MA-3 to obtain what is built first |
| Data | Identities (§4.1 L531–L538); capture-evidence reference fields (CAP-3 L928); carriage manifest contents (TR-4 L989); report elements | Cardinalities and optionality of report elements; where a report is kept (RS R14 holds only a reference); manifest representation (U-E16) |
| Operating sequences | CK-1…CK-4 (L276–L281); EV-1…EV-11 (L321–L333); TR-1…TR-8 (L986–L993); HR-1…HR-7 (L1024–L1030); RP-1…RP-8 (L880–L887) | No end-to-end current-phase sequence for an App run on X: selection → CK-1 → CK-2 → agent proposes → *queued* observed → arrival recorded → request → person acts in the host → capture evidence → faithful record → resume point → lapse. The steps exist only inside cases (CH-1, CH-7, CH-22, CH-27) |
| Failure behaviour | CF-1…CF-5 (L512–L516); TF-1…TF-8 (L1045–L1052); §4.12; §4.14 | Failure of recording itself (the record cannot be written; the run record is unavailable); loss of the X observation path in the current phase beyond *unknown* |
| Verification | 16 MT, 30 CH and 11 RT cases with current-phase and governance-phase columns; VC-E-01…VC-E-13; the W14 map for DEL-09-06 (RT-11 L1163) | Nothing runnable and no runner defined. No A6 or A7 case. No fixture that declares `governed`. The report has no worked instance (no filled CR-1…CR-14 for MT-1) |

**Structural choices still open that could force restructuring.**

1. **The App-run observation interface** (Interfaces (1)). It decides what §4.4, §4.12 and CH-22 can promise, and it is the consumer side of N-24. Part of it needs an observation that does not exist: PIN-SPIKE ran no model turn (HOSTING §8.1 L-3: "not-observed (no model turn in the spike)"), so the order and content of the native items around a tool call on X at 0.158.0 are unobserved.
2. **Current-phase modality and request** (C.2 lags 1 and 2). Whether recording is required, and whether the App itself responds to an arrival (shows a request or its CAP-2 control) or only records while the agent asks. The owner's DECISION-4 words bear on it: "I don't want checkpoints in workflows to be programmed into the app to respond in a certain manner." R8-1 reads this as no enforcement and recording as observation. Inference: a product-issued request at arrival is a programmed response of the kind the owner named, so the split between "the App records" and "the agent requests" should be written as a rule, and confirmed with the owner if the App is to do more than record.
3. **SP-6 (U-E4)** and **partial-lapse satisfaction (U-E3)**: both change the satisfaction predicate and the expected results of CH-8, CH-12 (iii), CH-20.
4. **Carriage and revision (U-E16)**: changes TR-2, TR-4, TF-1, TF-4, TF-8 and RP-5.
5. **Placement (U-E2, OI-014)**: open by design.

## C.6 Joins (ACTIVE rows of DEL-02-03's `Dependencies.csv` whose other end is one of the 14, plus X-1)

| Row (arc) | Direction; other end | Contribution named | DAG-003 | Supplier's Design content | Consumer's use | Finding |
|---|---|---|---|---|---|---|
| DEP-02-03-009 | consumer EXEC → DEL-02-01 | Portable workflow/role/checkpoint declarations and shared allocation | held | WD §3.4, §4.2, §4.2.4, §4.3.0–§4.3.8, §4.6, §6; WD-EX E1–E8 | EXEC §3.2 L290, §3.5 L342, §4 (L182–L189), §6.1, §7; §9.1 L1193 | Present and used. **EXEC has not read the final WD-v0.6** (C1-16). **D-1** (pass rule, A.6). **D-2:** EXEC says the independence rules consumed are "I-1…I-7 (WD §4.3.3)" (L185) and, in §9.1, "I-1…I-8" (L1193); WD has I-1…I-9. **D-3:** EXEC marks §4.7 and §4.10 ADOPTED (R4-3, R4-6); WD marks the same rules PROPOSED (W7). **D-4:** NG-2 "Absent path → stop" (L735–L739) is unphased, as is WD L385; LOOP's row is phased |
| DEP-02-03-011 | consumer EXEC → DEL-03-01 | Capability/catalog semantics for required-tool checks | held | C-v0.6 §2 (L85), §3 #1, #4, #9 (L140–L148), §3.2 (L205), §4.1–§4.2 (L224–L294), §5.3 (L360), §8 (L529), §10 | EXEC §3.2 L291–L295, §3.4 EV-4…EV-10, §7 | Present and used. EXEC read C-v0.4 and the C-v0.5 V-GR1 variant (L1194) |
| DEP-02-03-012 | consumer EXEC → DEL-04-01 (CONSTRAINT) | Only the identified adopted operation policy for dependent cases | **admitted** | ACT-v0.6 §2.1, §2.5 (L351), §2.6 A13 capture (L423–L434), §4.1–§4.5, U-03 | EXEC E-I, E-J; §4.5; §4.10; CAP-1 (L926); §9.1 L1196 | Present and used. EXEC read ACT-v0.4. Not reflected: ACT §2.7 (R8-13), which bears on §4.10's A12 rules only if a checkpoint may require a network-destination grant (D-6) |
| DEP-02-03-013 | consumer EXEC → DEL-04-03 | Act-binding and run-record format | held | RS-v0.6 R1 (continues ⟨run⟩), R2 (transfer links, carriage-manifest reference), R8 (arrivals, ordinals), R11 (action during hold with turn initiator; "continued past"), R14 (report reference), L-12, run-resumed event (RS L154–L194, L378) | EXEC §4.1, §4.4, §4.7, §4.12 (L876), §6.1; §9.1 L1198 | Present and used; RS adopted EXEC's requested elements (R4-10, R4-11, R6-5). EXEC read RS-v0.4. F-24 should be closed |
| DEP-02-03-014 | DOWNSTREAM HANDOVER: DEL-09-06 consumes EXEC | Local transfer/adaptation fixture results and identity trace | MIRROR of DEP-09-06-013, which is **admitted** | EXEC §6, §7.3, RT-11 W14 map (L1163) | CA-v0.4 W14-00…W14-10 cite EXEC RT-1…RT-3, TR-1…TR-6, AD-1…AD-6, MT-2, MT-16, CH cases (CA L463–L473) | Present on both sides. The contribution is "fixture results"; only designs exist |
| DEP-02-03-022 | consumer EXEC → DEL-05-01 | Arrival observation, subject binding and loop events from host loops | held | LOOP-v0.6 §2.3 (L390), §2.4.1 (L555–L565), §2.4.2 (L603), §2.4.4 (L800), §6.2 (L1150), §6.3 (L1165) | EXEC §4.4 L591, §9.1 L1199 | Present and used; EXEC read LOOP-v0.4. F-27 (the residual limit in §2.4.4) is not yet in EXEC CR-12 |
| DEP-02-03-023 (N-23) | consumer EXEC → DEL-01-01 | Observed stock-Codex supplier facts | **admitted** | HOSTING-v0.6 §6.1 request kinds and R9 (L396–L430), §6.7 (L559–L573), §8.2 (L767), §8.3 (L785), §8 closing paragraph | EXEC §2.3 HP-2/HP-4 (L258–L260), §3.2 L296, §5 CAP-6 (L931), §6.1 L958; §9.1 L1200 | Present and used for request kinds, guidance evidence and model destination. Missing on both sides: the native item sequence the App observes for arrivals (C.5). HOSTING §6.7 says it "delivers, unchanged, the native items and notifications from which DEL-02-03 records arrivals"; EXEC does not say which |
| DEP-02-03-025 (**N-21**, new) | consumer EXEC → DEL-03-02 | Per-item dispositions, item-left events, all-items-decided, change-item content identities, applied outcomes with resulting objects | held | P-v0.6 §4.3 (L322–L358), §9 (L568), §5, §3.1, §13 L709 | EXEC §4.4 L593, L598; §4.11 MX-1…MX-8, MC-1…MC-4 (L819–L845); §4.12 | Present and used; P cites the MX rules by ID. EXEC read P-v0.4 (L1195) |
| DEP-02-03-026 (**N-24**, new) | consumer EXEC → DEL-03-03 | Observations of checkpoint arrivals and act records on X, which EXEC records | held | ADAPTER-v0.4 §7.7 (L819–L840): "the App observes *queued* and later the host-captured item decisions through host reads over X and passes them to DEL-02-03 (for recording in Phase 1…)" | EXEC §9.1 L1201 lists "§7.7 checkpoint observation on X", used in "§3.6, CH-22, CH-27" | **Partial.** The supplier describes the A5 kind (c) case and a general Phase-1 sentence. The consumer names the section but does not wire it into §4.4 (L591) or §4.12, and neither file covers kinds (a) and (b) on X. **D-7.** The reciprocal arc N-27 (DEP-03-03-014) is in DEL-03-03's register |
| DEP-02-03-027 (**X-1**, new; supplier outside the 14) | consumer EXEC → DEL-01-04 | App act control and person identity, for the App-side positive capture fixtures only | held | DEL-01-04 has no `Design/` folder. Its SoW and folder contain neither "act control" nor "person identity" (`grep -rni`). Its REQ-005 covers faithful display or recording "through the designated recording interface" | EXEC §5 CAP-2, CAP-8; CH-23 (ii) AWAITING INPUT; U-E8 | **D-8.** EXEC's requirements exist; the supplier's contract does not name the contribution. The arc is narrow (HANDOFF "X-1 is narrow") and does not constrain the rest of EXEC |

**Not in DEL-02-03's register but touching it:** N-07 (DEL-02-03 consumes DEL-04-02's visible autonomy state) rests only on the supplier-side row DEP-04-02-023 (DAG-003 HANDOFF, V12 F6). EXEC §9.1 has the AS supplier row (L1197); §10 lacks the matching excluded act (C.2 lag 3). DEL-09-09 (DEP-09-09-023, held) and DEL-03-04 (DEP-03-04-009, admitted) consume EXEC's report, and neither is a receiver in §9.2 (L1208–L1215) or in the header (L35).

## C.7 Carried review items that name EXEC

| Item | Status | Evidence |
|---|---|---|
| V6 m-4: HP-H and U-E1 cite "SQ-02 (a)–(d)" without (f) | **fixed** | "(a)–(d)" no longer occurs; HP-H reads "(a) No, (c) No, (d) No/No, (f) No/No" (L261) |
| V6 m-7: hole in the HS partition for a declared, malformed held-actions element on an A5 or kind (a) checkpoint | **open** | HS-5 (L415) and "exhaustive partition" (L408) unchanged |
| C1-A: F-25 not dispositioned | **open** | L1282 |
| C1-A: F-26, re-verify CH-12…CH-14 against V-GR1 | **closed** in the file | L1283 "Closed (R6-4)" |
| C1-A SC-02-03-1…5 (SoW) | **applied** by SCA-V4-001 (E-0203-01…13), in the phased form | `RV/RV-2_DEL-02-03.md` |
| C1-A register proposals R-02-03-d, -e, -g, -h | **applied** as DEP-02-03-025, -022, -023, -026 | `Dependencies.csv` |
| CLOSEOUT_ACCOUNT: DEL-02-03 partial for "App-side hold unallocated (D6; U-E23)" | superseded for the current phase | SoW CLM-003: "In the current phase no App-side hold point is needed" |
| V9 Check 1 and Check 3 | passed for EXEC §2.1, §3.5, §3.6, §7 | V9 "Pass" rows; no residual names EXEC |
| V10; V11–V16 | none names EXEC; "17 Design re-pins" carried | as A.7. `Propagation_Plan.md` §5 lists "EXEC F-29" among the notes to close |

## C.8 Recommended work on EXEC in this pass

1. **Re-pin the header and basis** (docs, SoW `0006521b…`, R8 `44bc9a8d…`, decisions `5fd780bf…`, answers `afb6e063…`, case datasheet `a12abfaf…`, WD and WD-EX current bytes through GUIDE). Correct the two mistyped abbreviations. [C.1]
2. **Re-word against the amended texts:** PH-10, E-B, the §4.7 rationale and its AC-002 quotation, U-E24, CH-27's closing sentence; VC-E-10's TBD range; "current phase". [C.1, C.2, C.3]
3. **Follow the revised SoW:** add the DEL-04-02 and DEL-01-01 rows to §10; add DEL-09-09 and DEL-03-04 to §9.2; cite TBD-006, AX-004, AX-005. [C.2, C.6]
4. **Close findings from records:** F-10, F-11, F-24, F-28, F-29, F-31; disposition F-25 and F-27; mark PH-6 confirmed. [C.4, C.7]
5. **Write the current-phase recorder as its own definition:** one transition table and event list for the current phase; state whether recording is required; state who issues the request and what the App shows. Keep §4 as the governance-phase overlay. [C.2, C.5]
6. **Add the App-run reached-when table** (the counterpart of LOOP §2.4.1), naming for each kind the HOSTING-delivered item or the ADAPTER §7.7 observation that is the arrival event, and wire it into §4.4 and §4.12. It needs a bounded observation at the pin: one model turn calling a test-double MCP tool, recording the native item sequence. [C.5, C.6 D-7]
7. **Add one end-to-end current-phase sequence** for an App run on X and one for the App → host transfer. [C.5]
8. **State the App-side component responsibilities** at semantic level (checker, recorder, transfer tracer; their inputs, outputs and receivers) and prepare the OI-014 question for the owner. [C.5]
9. **Extend the designed cases:** A6 and A7 checkpoint cases (SoW VER-003); a fixture that declares `governed` for the hold cases (SoW VER-002); one worked report instance for MT-1. A bounded prototype of the required-tool check over a test-double catalog built from C §10 would test §3.3–§3.5. [C.2, C.5]
10. **Re-read WD-v0.6 §4.3.0 and §4.3.1** and fix D-1…D-4 together with WD; close V6 m-7. [C.6, C.7]

**Not in this pass, and why.**

- Changes to the governance-phase hold machine, hold support or D6 (U-E1, U-E23): phased by DECISION-4; TBD-006's point of need is "before any App or host checkpoint hold is claimed enforced".
- Host-side RT and CH cases (U-E9, U-E11…U-E15, U-E17, U-E18, U-E25): host joins deferred.
- App act control and person identity (U-E8; X-1) and the registration side of §6.5 (U-E19; F-12): their owners are outside the 14.
- U-E3, U-E4 and OI-014: owner decisions.
- OUT-001 "in code" and running OUT-003: implementation, after the design gate.

---

# Closing table

| File | NOW | OWNER | HOST | SPIKE | LATER | Open items (file-declared) | Stale pins | Mistyped hash abbreviations |
|---|---|---|---|---|---|---|---|---|
| WD `WORKFLOW_DECLARATION.md` | 7 | 4 | 10 | 2 | 6 | 29 | 10 | 1 |
| WD-EX `EXAMPLES.md` | 0 | 2 | 4 | 1 | 5 | 12 (all repeat WD items) | 8 | 0 |
| EXEC `EXECUTION_COMPATIBILITY.md` | 11 | 3 | 9 | 1 | 5 | 29 | 12 | 2 |
| **Row total** | 18 | 9 | 23 | 4 | 16 | 70 | **30** | 3 |

Items shared across files are counted once per file. Distinct owner choices across the row: five (below).

**Gaps found by this survey that no file marks open** (each is a NOW item unless stated): WD §10 and §8 missing DEL-03-03 (A.2); WD §4.2.1 supplier of harness-capability meaning (A.2); the pass-rule sentence against EXEC's three results (D-1); unphased "on negative decision" (D-4); no output-production element for kind (b) (D-5); A12 network-destination subclass (D-6); WD not having read RS, PANEL and HOSTING (A.6); no A6 or A7 example or case in any of the three files (A.2, B.2, C.2); EXEC §10 missing DEL-04-02 and DEL-01-01 (C.2); EXEC "may be recorded" against SoW REQ-002 (C.2); who issues the current-phase request (C.2; possibly OWNER); no App-run reached-when table (C.5; SPIKE); X-1's contribution absent from DEL-01-04's SoW (D-8; LATER, for S1-F).

**The three most consequential gaps.**

1. **The declared part has no carriage and no schema** (WD R-4 L207–L209; U-01, U-02, U-03; EXEC U-E16). OUT-002's "open declared-part schemas" do not exist, OUT-004 cannot be built, and every consumer's parse, the revision identity and the carriage manifest depend on the choice. It is the open structural choice most able to force later restructuring of WD, EXEC, LOOP and DEL-02-02. A bounded prototype can settle it in this pass.
2. **The current-phase behaviour of an App run is defined by subtraction and lacks its observation interface** (EXEC §2.1 L227–L233; §4.4 L591; WD L379; ADAPTER §7.7; HOSTING §6.7). EXEC has no App-side counterpart of LOOP §2.4.1, WD has no element for observing a message-form output, recording is "may" while the revised SoW REQ-002 and AC-002 require a preserved disposition, and no rule says whether the App or the agent issues the request. This is the part of OUT-001 that is built first.
3. **Harness capabilities are unnamed, and the three records point at each other** (WD §4.2.1 L249, U-08; EXEC EV-3 L325, U-E10; HOSTING §8 L748–L751; SoW REQ-002). The arcs to DEL-01-01 are admitted (N-16, N-23), so this is a real blocker. Until named, every declared harness-capability requirement makes the check *not established* (MT-8, MT-15, L-WDEX-15), which in the current phase is the only checkpoint-adjacent cause of a failed check for an App-authored workflow.

The re-pin itself (30 stale pins, the obsolete V4-WF-05 and V4-HI-42 sentences, the two lagging §10 tables, six findings to close) is required and mechanical. It should be done first, because items 1–3 edit the same passages.

**Owner-level choices found.**

1. **SP-6** (WD U-31, EXEC U-E4): count only acts captured at or after arrival, or also a prior act bound to current content. The files state the cost of the first (a repeated grant, F-23).
2. **Partial lapse** (WD U-05c, EXEC U-E3, with DEL-04-01): whether an act on only the lapsed referents satisfies.
3. **Placement of shared parts** (OI-014; WD U-12, EXEC U-E2): shared types or library, local implementations with conformance fixtures, or a service, per §9 row; and where the App-side checker and recorder live.
4. **Automatic catalog extension** (App v4 OI-003; WD U-16). No effect on these files until decided.
5. **Where the governance opt-in lives.** The `governed` declaration flag is PROPOSED by R8-1 and was reported to the owner as "still PROPOSED" (OWNER_ITEMS O-4 note). It can wait for the governance phase.

One further point may need the owner, by my inference rather than by any file's statement: whether, in the current phase, the App itself responds when it observes an arrival (shows a request or an act control), given DECISION-4's wording. R8-1 and PH-1 can be read to settle it as "the agent asks; the App records"; the files do not say so as a rule.
