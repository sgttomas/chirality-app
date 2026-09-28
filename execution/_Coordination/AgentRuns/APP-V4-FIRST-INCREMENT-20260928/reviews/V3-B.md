# V3-B — final bounded consistency check (App/host contract half)

- Node: V3-B, run `APP-V4-FIRST-INCREMENT-20260928`. Reviewer: independent
  Type 2 (Claude Code subagent). I wrote none of the reviewed files and
  delegated nothing. I used read-only git and no network.
- Candidate: commit `9fc77baa3`. Every file was read with `git show` into a
  private scratch folder (`<scratchpad>/v3-b/`).
- Scope (BRIEFS "V3", V3-B): DEL-03-01 C-v0.4, DEL-03-02 P-v0.4, DEL-03-03
  ADAPTER-v0.2, DEL-03-04 GUIDE-v0.1, DEL-01-01 HOSTING-v0.4 (PIN_SPIKE-v0.1
  as context only), DEL-09-06 CA-v0.2 and RELAY-v0.2, and DEL-09-09 XT-v0.2.
  R5 items Y-1, Y-7, Y-8 and Y-9. I also checked that RELAY-v0.2 covers the
  host items named in all 17 files. I read the other files (ACT, AS, RS, WD,
  WD-EX, EXEC, LOOP, PANEL) only where a join, a carriage term or a host item
  required it. Their own conformance is V3-A's.
- Method: I read C, P, ADAPTER, RELAY, CA, XT and GUIDE in full. For HOSTING I
  read the header, the change table, §6 and §8.3. I read every R4 ruling
  against the text it names. I also ran grep sweeps across all 17 files for
  carriage-assurance terms, hold-support values, fixture identifiers, SQ
  citations, host-owned UNRESOLVED rows and claim language.
- Rulings verified by sha256. The copies at `9fc77baa3`, at `f05c7e4cd` and in
  the working tree are identical:
  - R1 `2f9c7e72…`
  - R2 `77cfb845…`
  - R3 `202d52c7…`
  - R4 `50a009b2…`
  - OWNER_DECISIONS `a9869129…`
- Candidate count: `git ls-tree` lists **17** non-generated Design files at
  `9fc77baa3`. That is the 16 the brief names plus GUIDE-v0.1 (see m-12).

## Verdict

**MERGE AS DRAFTS.**

| Severity | Count |
|---|---|
| BLOCKING | 0 |
| MAJOR | 5 |
| MINOR | 13 |

No file in my half does any of the following:
- claims implementation, qualification, host delivery or adoption;
- claims a performed human act;
- claims relay delivery.

RELAY is correctly marked PREPARED FOR HUMAN RELAY — not delivered, and its
ledger is empty.

The five MAJOR residuals are consistency defects. None of them overstates
evidence. They should be fixed before RELAY is handed to the owner for relay,
and before GUIDE is used as the integrated index.

---

## 1. R4 rulings against the text (my files, plus other files on the same subject)

| Ruling | File and place | Result | Evidence / note |
|---|---|---|---|
| R4-1 (D5) | ADAPTER S-X11, §3.1, §3.4, E-6, XF-36, U-X2 closed | holds | Destination is shown and recorded; no gate; V4-HOST-02 kept for the embedded agent; SQ-16 is host-side only |
| R4-1 | C §4.1 note; HOSTING §8.3 (per thread and turn, requested / effective / re-route); CA S-12, DI-5; XT S-9, IN-14; RELAY SQ-16 | holds, with m-1 | Several files credit the *record-and-show* element to D5 as SETTLED. DECISION-2 marks it as the recorder's reading, and HOSTING §8.3 says so correctly |
| R4-2 (D6) | ADAPTER S-X12, §2, GC-3, GC-5, §7.7, OC-2, OC-11; HOSTING §6.7; CA S-13, §2.2; XT S-10; RELAY SQ-02; GUIDE B-7 | holds | No App hold is claimed; HP-1 and HP-2 are not adopted; HP-3 is best effort only; action during hold is recorded |
| R4-2 | P §4.4 ("the run holds after application for the A4"; "any other declared checkpoint holds the run") | partial (m-3) | Unqualified for App runs. P's body never cites `UNRESOLVED{D6}` |
| R4-3 | P §4.3 ("A5 never re-holds"); CA S-14, W14-06 | holds | — |
| R4-4 | P §10 run-ended row; CA S-14, W14-07 | holds | — |
| R4-5, R4-6 | P §10 rules; CA S-14, W14-05; XT S-12, XC-10; C T15 "control confirms" | holds | — |
| R4-7 | P §4.3 | partial (m-2) | The confirmation is cited, but the same bullet still reads "PROPOSED; DEL-02-03 confirms at W7". The UNRESOLVED row "Mixed item decisions … DEL-02-03 confirms at W7" was not closed |
| R4-8 | ADAPTER GC-3, XF-26; CA WR-11; GUIDE M8.3 | holds | — |
| R4-12 | HOSTING R9, §6.1 kinds table, §6.8 (MCP config, status, OAuth, agent call, App-initiated `mcpServer/tool/call` and `resource/read`, elicitation, event stream, dynamic tools); ADAPTER §3.5, §7.6, XF-33; P §10 | holds | The App-initiated call is App-origin and is never used to act as the agent or for anyone's act |
| R4-13 | ADAPTER E-2, E-3, E-4, OC-4, VC-X-02; C §4.1; HOSTING §6.8 (`disabled` is never A13) | holds | — |
| R4-14 | ADAPTER §5.1–§5.3, S-X13; C §4.1; GUIDE M4.1, M6.4, M9.5 | holds | — |
| R4-14 | **P §3.3** carriage-assurance element | **partial (MAJOR-1)** | P defines *App-assured* as including "the host loop per DEL-05-01 §6.2". ADAPTER §5.1, ACT §4.4, EXEC §3.6 / F-18, RELAY SQ-02 and LOOP C-6 / G-1 all differ |
| R4-15 | P §3.3 author identity *unverified*; ADAPTER §5.4, XF-37 | holds | — |
| R4-16 | C §4.1 reporter column; ADAPTER §3.2; P §9 (defers to C §4.1) | holds | — |
| R4-18 | C T15 (P-03, {FX-W1; {S-4}}, ⟨set-2⟩); CA §2.4, W14-04; XT XC-10, CMP-07 | holds | — |
| R4-19 | C FA-n → FXA-n with alias, FXA-5, K-7; P m-3 / m-9 / m-11 | holds, with m-6 | — |
| R4-20 | C LIB-A1, LIB-A2, AF-1, e1/e2, V-ED1; ADAPTER L-ADAPTER-11/12, PI-5, PI-6, XF-40, XF-41; XT L-XT-1 retired; CA L-CA-1 retired | holds, with m-11 | — |
| R4-21 | GUIDE M8.3; ADAPTER GC-5 (kind (a) on X *not enforceable* unless the host holds the call) | holds | — |

## 2. Checks (a)–(f)

**(a) Vocabulary.**
- Consistent in my half:
  - act names A1–A14;
  - the five class values, with the no-policy-basis reason;
  - the six dispositions (ADAPTER §7.7 lists them exactly);
  - the events act-lapsed, act-declined and run-ended;
  - the lapse states (C §6.2 = RS §7).
- Two vocabularies are not consistent:
  - **Carriage:** the meaning of *App-assured* differs between P and the rest (MAJOR-1).
  - **Hold support:** ADAPTER uses names and a mapping that differ from EXEC §3.6, the owner of the value set (MAJOR-5).

**(b) Fixture identifiers.**
- Every OP-C, T, V-, PR-, RC-, S-n, ⟨set-n⟩ and FXA/FA identifier cited
  anywhere resolves to C-v0.4 §10.
  - FA-n resolves through C's alias. ⟨set-T15⟩ appears only in change tables.
  - ⟨rev-A2⟩ / ⟨rev-A3⟩ are DEL-02-03's labels, which C §10.1 states.
- The local labels in my half are all declared:
  - L-ADAPTER-1…13, each with a reason;
  - L-XT-2 and L-XT-3 (L-XT-3's reason is carried by ADAPTER L-ADAPTER-12);
  - L-CA-1, now retired.
- For V3-A: EXEC still treats L-EXEC-19, ⟨fx-app-import⟩ and U-E21 as local
  "because C lacks them". C-v0.4 now supplies AF-1 and LIB-A2.

**(c) Claims.** None found. PR #885 is cited only as evidence in ADAPTER and RELAY.

**(d) D5 and D6.**
- D5 is applied faithfully: no gate, cloud allowed, host-side restriction
  relayed. The files do over-credit the record-and-show element as "SETTLED
  by D5" (m-1).
- D6 is applied faithfully as a deferral. It is not over-credited as a ruling.
- One framing is overstated. RELAY SQ-02 says the SWBPIPE answer "decides
  whether any checkpointed workflow can run supported on the App/external
  surface". That holds only for checkpoints on host operations. See MAJOR-4.

**(e) Cross-file citations.** Much of my half still cites sibling v0.3 / v0.1 /
RELAY-v0.1 texts. Most of this is mechanical (Y-7). Several items are not
mechanical, because the cited text is now false (MAJOR-2, m-4, m-5). The
section numbers of WD, LOOP, PANEL, RS and AS are stable between v0.3 and
v0.4 (headings checked), so a mechanical re-point is feasible for the rest.

**(f) R5 items.** See §4.

---

## 3. Relay coverage (RELAY-v0.2 against host items in all 17 files)

**Covered.** Every source the W9 brief named maps to an SQ in RELAY §3, and I
spot-checked each against the question text:
- LOOP Q-1…Q-7;
- PANEL Q-1…Q-9;
- ADAPTER XQ-1…XQ-12;
- ACT U-04 (a)–(f);
- EXEC U-E1, U-E2, U-E9, U-E11…U-E15, TR-6…TR-8 and HP-H;
- R2-20;
- the OI-021 items from HANDOFF.

The additions from the sweep are also covered:
- SQ-28 for A13 capture (ACT U-04 (e));
- SQ-29…SQ-32 for GUIDE G-3 and LOOP-v0.4 N-OPEN, T-OPEN-1, HS-0 and R-OPEN-1;
- C V-ED1 (SQ-26).

The following UNRESOLVED host rows are covered too:
- C: U-C2, U-C3, U-C5, U-C7, U-C9, U-C11, the constraint receipt, the destination restriction and the edition event;
- P: U-P1…U-P5 and U-P7…U-P10;
- AS: U-05, U-06, U-07, U-12 and U-18;
- RS: U-09, U-11, U-14, U-15, U-19, U-21 and U-27;
- WD: U-19, U-05b and U-23;
- PANEL: "who evaluates required-tool outcomes" (SQ-17 (c)).

**Not covered.** These host-owned items have neither an SQ nor a reason
under "Not included" (MAJOR-3):

| Item | File | Nearest SQ | Suggested home |
|---|---|---|---|
| U-C4 multi-read reliance: which cited bases must still hold | C | SQ-07 | New SQ-07 (g) |
| U-C6 host behavior on an entry-version mismatch | C | SQ-09 / SQ-18 (d) | New SQ-18 (e) |
| U-C10 non-mutating operations citing a basis are never refused stale; both bases stated | C | SQ-07 | New SQ-07 (h) |
| U-P6 operation-specific withdraw/reject rules beyond R-1 | P | SQ-05 (b), partly | Add to SQ-05 |
| U-04 host enforcement of *unconfirmed*; re-resolution at application | AS | SQ-05 (d), partly | Add to SQ-05 |
| U-12 content returning to c₀ after an observed lapse | RS | SQ-03 / SQ-23 | Add to SQ-03 |
| U-09 host single seat → role-meaning mapping (with the SWB implementation owner) | WD | SQ-19, partly | Add to SQ-19, or a new P5 item |
| U-06 defaults for other consequential classes | ACT | SQ-05 | Add to SQ-05 |
| U-10 host origin in precedence (DEL-02-02, later undertaking) | WD, WD-EX | — | "Not included" with a D1 reason |

**"App assumes meanwhile" against current rulings.** Consistent with R4 and
DECISION-2 for SQ-01, SQ-03…SQ-08, SQ-10…SQ-15, SQ-17…SQ-32. Exceptions:
- **SQ-02.**
  - The assumption is right: "only host-held counts", host-loop runs are
    unaffected, and App-assured needs interposed code.
  - It contradicts P-v0.4 §3.3, which counts the host loop as App-assured.
    P is the side to change (MAJOR-1).
  - "Why it matters" overstates what the answer decides (MAJOR-4).
- **SQ-16.** The record-and-show element is credited to D5 as decided. It is
  the recorder's reading and R4-1 (m-1).
- **SQ-09.** "A result without a stated outcome is *outcome unknown*" is
  applied to reads as well. ADAPTER M-3 makes such a read *error as
  observed* (m-8).

---

## 4. R5 items assigned to V3-B

| # | Position | Reason and required amendment |
|---|---|---|
| **Y-1** | **AMEND** | I agree that a host loop's own evaluation counts as *host-held*. Three amendments:<br>1. P-v0.4 §3.3 currently puts "the host loop per DEL-05-01 §6.2" under *App-assured*. The host loop is SWBPIPE-built (OI-013), not an App process. P must remove it there, not only add a sentence (MAJOR-1).<br>2. The proposed definition says "received or derived". A constraint *received* in a request from a caller outside the host keeps its source's assurance (model-supplied, or App-assured). Suggested text: *host-held* = the constraint originates on the host side, from a declaration copy or run association the host holds — evaluated by the host route, or derived by the host loop from the resolved declaration it evaluates.<br>3. LOOP C-6 / G-1 and CA F-12 then close. RELAY SQ-02 needs no change |
| **Y-7** | **AMEND** | I agree with a mechanical re-point for version labels and sections. The pass must also cover these non-mechanical items, where the old citation is now wrong in substance:<br>- GUIDE (MAJOR-2);<br>- ADAPTER §3.1 SQ-13 → SQ-28, §12 map, §7.7 v0.1 hold values (m-4, MAJOR-5);<br>- HOSTING §6.7's withdrawn EXEC U-E20 and missing HP-4 (m-5);<br>- P §4.3 / UNRESOLVED "confirms at W7" (m-2);<br>- C §4.1 "as of C-v0.3 / P-v0.3", §9 "P-v0.3 locus", VC-C-04 "P-v0.3 §11", and the §10.1 note on DEL-04-03 FA-n, now OF-n (m-6);<br>- XT IN-07 "ACT-v0.3" against its own header's ACT = v0.4 (m-10);<br>- RELAY "SQ count 28" (m-7);<br>- for V3-A: ACT FX-50 still cites the retired ADAPTER U-X3.<br>The consumed-input headers of C, P, HOSTING and ADAPTER cite EXEC/ADAPTER/XT-v0.1. That is historically true, but it should gain a note that the v0.2 texts were read, or were not read |
| **Y-8** | **AMEND** | I agree with stating it, but only together with Y-1. With P §3.3 as it stands, "App-assured: not available" would also deny the embedded route. Attribute it to **R4-2** (HP-1 not adopted while D6 is deferred), not to "D6", which is a deferral. Suggested text for P §3.3 and ACT §4.4: "App-assured requires App code on the dispatch path; none is adopted in this increment (R4-2; D6 deferred), so only host-held carriage can satisfy R2-12. A host loop's derived constraint is host-held (Y-1)." ADAPTER §5.1 / S-X12, EXEC F-18 and RELAY SQ-02 already say this |
| **Y-9** | **AMEND** (one-line text change) | Surface this with the relay. State it precisely:<br>1. **SQ-28** gates the whole external channel: every live CA/X and XC case, including V4-EXM-25. Without it the channel stays *not enabled*.<br>2. **SQ-02** gates checkpointed workflows on the App/external surface, but only for checkpoints on **host operations** (EXEC HP-H: "host operations only").<br>3. **App-only checkpointed workflows** (App content, e.g. A4 on AF-1; kinds (b)/(c) run halts) stay *not enforceable*, and so *unsupported*, **whatever SWBPIPE answers** (EXEC §3.6, F-17). D6's deferral target cannot resolve them. The owner needs to see this as a separate D6 follow-up.<br>RELAY SQ-02 "Why it matters" should read "…for checkpoints on host operations" (MAJOR-4) |

---

## 5. Residuals

### MAJOR

- **MAJOR-1 Carriage assurance: P defines App-assured differently from the rest of the set.**
  - P-v0.4 §3.3: *App-assured* = "an App process on the dispatch path — the
    host loop per DEL-05-01 §6.2, or an App adapter".
  - ADAPTER §5.1 and ACT §4.4 use "App code on the dispatch path". ADAPTER
    limits it to the interposed families only.
  - EXEC §3.6 / F-18 and RELAY SQ-02 say App-assured needs interposed code
    and is unavailable. RELAY adds that host-loop runs are unaffected.
  - LOOP C-6 / G-1 reads the host loop as host-held.
  - P §4.4 ("carried App-assured or held by the host") inherits the ambiguity.
  - Under P's reading, embedded runs would be App-assured and Y-8's proposed
    text would be false for them.
  - **Side:** P §3.3 and §4.4, with the Y-1 and Y-8 micro-ruling. LOOP C-6
    then names *host-held*.
- **MAJOR-2 GUIDE-v0.1 is stale against the swept set, and several of its statements are now false.**
  - GUIDE was pinned to `f05c7e4cd` inputs: RELAY-v0.1 (SQ-01…SQ-27), ADAPTER-v0.1, CA/XT-v0.1.
  - M2.4, M7.2, M7.3, M7.5, HC-2.4, HC-7.2…HC-7.4 and the row-7 summary say
    "no relay question exists (G-3)". SQ-29…SQ-32 now exist.
  - CC-4 reads "27/27" and CC-5 reads "fail". G-3, G-4, F-2 and F-3 are open,
    but RELAY-v0.2 and the CA/XT sweep closed them.
  - M9.1 and HC-9.1 cite SQ-13 for A13 capture; that is now SQ-28.
  - Row 9, M6.4 and UNRESOLVED carry the retired ADAPTER U-X3, which is now
    `UNRESOLVED{D6}`.
  - M5.6 cites RS FA-1…FA-9, which are now OF-1…OF-9.
  - Every matrix line cites v0.3 / v0.1 sections.
  - This review is also GUIDE's first independent read (GUIDE F-9).
  - **Side:** GUIDE → v0.2 against the `9fc77baa3` set.
- **MAJOR-3 Relay coverage gaps.** See the §3 table: nine host-owned items
  have no SQ and no "Not included" reason.
  - **Side:** RELAY, before the owner relays it. Add sub-questions, or list
    the items under "Not included" with reasons.
- **MAJOR-4 The D6 deferral framing overstates what SQ-02 can decide.**
  - RELAY SQ-02 "Why it matters" says the answer "decides whether any
    checkpointed workflow can run supported on the App/external surface".
  - HP-H covers host operations only (EXEC §2, §3.6), so App-only
    checkpointed workflows stay unsupported whatever SQ-02 returns.
  - EXEC F-17 and CA F-10 raise the strength of this consequence, but not its
    independence from SQ-02.
  - **Side:** RELAY SQ-02 wording (one line). Surface it to the owner as a
    separate D6 follow-up with Y-9 and EXEC F-17.
- **MAJOR-5 Hold-support vocabulary is not EXEC's.** EXEC §3.6 owns the
  values: *enforced by the host loop* · *host-enforced for host operations* ·
  *not enforceable* · *not established*. The mismatches:
  - ADAPTER GC-3, GC-5 and XF-25 use "enforced on the host route".
  - ADAPTER §7.7 still names the v0.1 values "enforced before dispatch" and
    "held after observation" (ADAPTER F-16 raised this, and EXEC-v0.2 has
    since removed them).
  - ADAPTER XF-26 maps model-supplied carriage to *not enforceable →
    unsupported*. EXEC §3.6 (iii) maps it to *not established* (check does not
    pass; AWAITING INPUT).
  - XT XC-10 and IN-25 mix the two. RELAY SQ-02 and CA §2.2 say "not
    enforceable or not established", which is acceptable.
  - **Side:** ADAPTER (GC-3, GC-5, §7.7, XF-25, XF-26); XT XC-10 / IN-25 to follow.

### MINOR

- **m-1 D5 over-credit** (C §4.1, ADAPTER S-X11, CA S-12, XT S-9, RELAY SQ-16).
  - Problem: "records each run's model destination and shows it in the
    channel status" is credited to D5 as SETTLED. DECISION-2 marks it as the
    recorder's reading, and HOSTING §8.3 is correct.
  - **Side:** the files. Attribute it to R4-1 (recorder's reading), and keep
    "no gate, cloud allowed" as D5.
- **m-2 P §4.3 and UNRESOLVED still show WD §4.3.7 as "PROPOSED; DEL-02-03 confirms at W7"**, although R4-7 confirmed it.
  - **Side:** P.
- **m-3 P §4.4 hold statements are unqualified for App runs.**
  - Problem: "the run holds after application for the A4"; "any other
    declared checkpoint holds the run".
  - **Side:** P. Add "where hold support allows; App runs `UNRESOLVED{D6}`
    (R4-2)".
- **m-4 ADAPTER relay citations.**
  - §3.1's "Host enablement record" cites SQ-13 instead of SQ-28.
  - §12 maps XQ → SQ from RELAY-v0.1 and omits SQ-28.
  - The §9 column is headed "Relay (RELAY-v0.1)".
  - **Side:** ADAPTER.
- **m-5 HOSTING §6.7 misses EXEC-v0.2 changes.**
  - It cites EXEC U-E20, which EXEC-v0.2 withdrew.
  - It does not mention EXEC HP-4 (the App initiates nothing, including an
    App-initiated `mcpServer/tool/call`, for a holding run). HOSTING §6.8
    classifies exactly that call. ADAPTER likewise omits HP-4 and HP-H.
  - **Side:** HOSTING and ADAPTER.
- **m-6 Double rename.**
  - C §10.1 renamed FA-n → FXA-n "to end the collision with DEL-04-03's
    FA-1…FA-9". RS-v0.4 also renamed its own to OF-1…OF-9.
  - Harmless, but C's note is stale, and GUIDE M5.6 cites RS FA-n.
  - **Side:** C note; GUIDE.
- **m-7 RELAY change table** says "SQ count 28" in one row and "32" at the end.
  - **Side:** RELAY.
- **m-8 RELAY SQ-09 assumption** generalizes "no stated outcome → *outcome unknown*" to reads (ADAPTER M-3: read → *error as observed*).
  - **Side:** RELAY.
- **m-9 XF-42 state mismatch.**
  - XT XC-10 marks XF-42 HELD on `UNRESOLVED{D6}`. ADAPTER gives XF-42 no
    state, and it is a recording case that needs no D6 ruling.
  - **Side:** XT, or ADAPTER to state XF-42 as DESIGNED, with the hold itself
    `UNRESOLVED{D6}`.
- **m-10 XT version labels.**
  - IN-05 / IN-07 / IN-08 / IN-22 / IN-29 cite P / ACT / RS / LOOP / AS at
    v0.3.
  - IN-07's "ACT-v0.3" contradicts XT's own header (ACT = v0.4).
  - **Side:** XT.
- **m-11 V-ED1 branching is ambiguous.**
  - C §10.4 and XT §4.1 say V-ED1 branches "before T16, on edition e1", while
    the main timeline T1–T17 runs on e2.
  - **Side:** C. State that V-ED1 replays T1–T15 on e1 and publishes e2 before T16.
- **m-12 Candidate count.**
  - The brief says 16 Design files; `9fc77baa3` has 17 (GUIDE included).
  - GUIDE's own CC-8 "16/16" counts the pre-GUIDE set.
  - **Side:** the coordinator's record.
- **m-13 GUIDE's completeness results are self-review.**
  - GUIDE §4.1 CC-1…CC-11 are self-review (F-9). CC-4 and CC-5 are
    superseded (MAJOR-2).
  - **Side:** GUIDE v0.2 records this V3-B review as its first independent check.

### Notes for V3-A's side (observed while checking joins; not scored here)

- EXEC CH-23, the local-fixture note and U-E21 still treat L-EXEC-19,
  ⟨fx-app-import⟩ and ⟨rev-A3⟩ as local "because C lacks them". C-v0.4 AF-1
  and LIB-A2 now exist.
- ACT FX-50 still holds "on SQ-02 and ADAPTER U-X3". U-X3 is retired to
  `UNRESOLVED{D6}`.
- WD-EX's change table says "C §10 itself declares only V-CP1's `CP-accept`
  (FA-5)". C-v0.4 FXA-5 now declares both `CP-accept` and `CP-check` from
  WD-EX E1.
