# V4-B — independent review of the final Wave-2 candidate (App/host contract half)

- Node: V4-B, run `APP-V4-FIRST-INCREMENT-20260928`. Reviewer: independent
  Type 2 (Claude Code subagent). I wrote none of the reviewed files and
  delegated nothing. I used read-only git and no network.
- Candidate: commit `c7f5513db`. Every Design file was read with `git show`
  into a private scratch folder (`<scratchpad>/v4-b/`). `git ls-tree` lists
  **17** non-generated Design files at the candidate.
- Brief: BRIEFS.md "V4 — independent review of the final Wave-2 candidate",
  V4-B. That section is in the working-tree BRIEFS.md (sha256
  `c85c3519aeaa845d…`); it is not in the candidate commit.
- Rulings: R5 (`254d0b93…`), R4 (`50a009b2…`) and OWNER_DECISIONS
  (`a9869129…`). Each is identical at the candidate and in the working tree.
  R1–R3 were taken as recorded by V3-B.
- Scope (V4-B):
  - DEL-03-01 C-v0.5;
  - DEL-03-02 P-v0.5;
  - DEL-03-03 ADAPTER-v0.3;
  - DEL-03-04 GUIDE-v0.2, read in full as its **first independent review**;
  - DEL-01-01 HOSTING-v0.5, with PIN_SPIKE-v0.1 as context;
  - DEL-09-06 CA-v0.3 and RELAY-v0.3;
  - DEL-09-09 XT-v0.3.

  I read EXEC-v0.3 §2, §3.5, §3.6, §7 (MT, CH) and §11 as the owner of the
  value set and of the pass-through rulings. I read the other V4-A files only
  where a join, a fixture or a value required it, and for the sweeps in
  items 4 and 5.
- Method:
  - I read CA, RELAY, XT, ADAPTER and GUIDE in full.
  - For C I read §4, §8–§10, the change tables, UNRESOLVED and the
    verification cases.
  - For P I read §3.3, §4, §10, the change table, UNRESOLVED and the
    verification cases.
  - For HOSTING I read the header, the change tables, §6.5–§6.8 and §8–§8.3,
    and grepped U-25, F-22 and U-E20.
  - I compared each file's blob at `d3cebd1cc` with its blob at the
    candidate. Only GUIDE, CA and RELAY differ; CA and RELAY differ because
    of `816c917f0`.
  - I ran grep sweeps across all 17 files for claim language, hold-support
    values (current and retired), CP-grant values, and D5 attribution.

## Verdict

**MERGE AS DRAFTS.**

| Severity | Count |
|---|---|
| BLOCKING | 0 |
| MAJOR | 1 |
| MINOR | 9 |

- **No-over-claim sweep (item 4).** No file claims implementation,
  qualification, host delivery or adoption, a performed human act, or relay
  delivery.
  - All 17 files carry DRAFT status, except PIN_SPIKE, which is an
    "OBSERVATION RECORD … not qualification".
  - RELAY stays **PREPARED FOR HUMAN RELAY — not delivered**, and its §4
    ledger is empty.
  - PR #885 is cited only as evidence.
- **Hold-support values (item 5).** Only the four R5-1 values are used as
  values. Retired values appear only in retirement notes and change logs.
- **The one MAJOR** is a mis-assigned value in the shared fixture. It is not
  a vocabulary breach or an over-claim. It is a one-line fix in C, which I
  recommend before merge; it does not block merge.

---

## 1. R5 rulings against the text (item 1)

| Ruling | File and place | Result | Evidence / note |
|---|---|---|---|
| R5-1 values | EXEC §3.6 (owner) | holds | Four values; HS-1…HS-5; retired values listed as retired |
| R5-1 | ADAPTER §2, S-X12, GC-3 (three-row table), GC-5, §7.7, OC-11, XF-25, XF-26, XF-42, VC-X-03 | holds (m-4) | GC-3 is exactly HS-3 (a)–(c). XF-26 is defined as the "SQ-02 answered with no host-held route" variant, so *not enforceable* is correct for it |
| R5-1 | CA S-13, §2.2, WR-11, DI-6, ST-4, W14-04 (iii), UNRESOLVED | holds (m-2) | — |
| R5-1 | RELAY SQ-02 "App assumes meanwhile" | holds (m-2) | — |
| R5-1 | XT S-10, IN-25, XC-10 | holds (m-2) | XF-42 is DESIGNED (V3-B m-9 closed) |
| R5-1 | HOSTING §6.7 | holds | "Uses R5-1's four values only"; no raise above *not enforceable* |
| R5-1 | GUIDE §0, §2.14, M7.6, M8.3, HC-6.3, HC-8.3 | holds | §2.14 reproduces HS-1…HS-5 |
| R5-1 | P §4.4 | holds | Qualified "where hold support allows"; App holds `UNRESOLVED{D6}` (V3-B m-3 closed) |
| R5-1 | **C §10.4 V-GR1, last sentence; C "Changes from v0.4" R5-1 row** | **fails (MAJOR-1)** | "From the App via X, `CP-grant` hold support is **not enforceable**." CP-grant is kind (a) before dispatch of **OP-C9, a host operation**, so HS-3 applies: today the value is *not established*. EXEC MT-16, WD-EX E8 row "E1d from the App via X", and WD VC-37 all say *not established* |
| R5-1 | C §10.1 FXA-5 | partial (m-3) | Says only that E1 via X has `CP-accept` *not established*. It omits `CP-check` → *not enforceable* (HS-5) and therefore *unsupported* |
| R5-2 | P §3.3, §3.3 authority limit, §4.4, §13, VC-P-04 | holds | Host loop removed from App-assured; received-then-verified counts as host-held; App-assured not available (V3-B MAJOR-1 closed) |
| R5-2 | ADAPTER S-X13, §5.1, §5.2, constraint row, VC-X-08 | holds (m-4) | — |
| R5-2 | C FXA-5; CA S-13, §2.2; RELAY SQ-02 (a); XT S-10; GUIDE B-9, M4.1 | holds | — |
| R5-3 | GUIDE M8.4, HC-8.1; P §10 A12 row | holds | No other text in my half touches the subject |
| R5-4 | HOSTING §8.3 | holds | Per-turn facts; requested and effective kept separate; unobserved → *unknown*; attribution split |
| R5-4 | ADAPTER S-X11, §3.1, §3.4, VC-X-02 | holds (m-4) | §11 still says "model destination per run (R4-1)" |
| R5-4 | C §4.1; CA S-12, W14-08; RELAY SQ-16; XT S-9, XC-02; GUIDE B-6, M5.6, M9.7, HC-9.5 | holds | — |
| R5-4 | CA DI-5; RELAY header Basis ("D5 settled — the model destination is recorded and shown, not gated"); XT IN-14 | **partial (m-1)** | Residual over-credit of record-and-show to D5 |
| R5-5 | ADAPTER §7.7; P §4.5; CA S-14, W14-06; GUIDE M4.4 | holds | — |
| R5-6 | P §10 rules; GUIDE M5.1 | holds | — |
| R5-7 | C §10.4 V-GR1: arrival at r15; T15's A12 captured after arrival; T16 unchanged; main timeline unchanged; ⟨rev-3⟩ declares no CP-grant; SP-6 cost recorded | holds, except the X value (MAJOR-1) | — |
| R5-7 | CA S-14 and UNRESOLVED; GUIDE M8.4 | holds | XT correctly cites no V-GR1 (XF-23's T15 is outside any checkpoint) |
| R5-8 | GUIDE §2.14 | holds | RS E10 / VC-17 are V4-A's |
| R5-9 | C: §4.1 "as of C-v0.5 / P-v0.5"; §9 P-v0.5; FXA note (OF-n; V3-B m-6); V-ED1 branching (V3-B m-11) | holds | — |
| R5-9 | P "confirmed by DEL-02-03"; mixed-item UNRESOLVED row closed | holds | V3-B m-2 closed |
| R5-9 | ADAPTER: SQ-13 → SQ-28 (§3.1, OC-4, §12); FXA-n | holds | — |
| R5-9 | HOSTING: U-E20 no longer cited (change logs only); HP-4 added | holds | V3-B m-5 closed |
| R5-9 | XT IN-07 → ACT-v0.4 | holds | — |
| R5-9 | GUIDE matrix at GUIDE-v0.2 against the `d3cebd1cc` set | holds | — |
| R5-9 | CA, RELAY, XT, ADAPTER, HOSTING, C and P citations of **siblings** | **partial (m-6)** | These parallel-pass files cite siblings at `8fb51f07f` (Wave-1 v0.4; EXEC, ADAPTER and RELAY v0.2; GUIDE v0.1). Each file declares this. No substantive error was found apart from MAJOR-1, m-3 and m-5 |
| R5-10 | RELAY SQ-02 "Why it matters" (host operations only; App-only is a separate D6 follow-up) | holds | V3-B MAJOR-4 closed |
| R5-10 | RELAY SQ-28 (gates the whole channel, including V4-EXM-25) | holds | — |
| R5-10 | RELAY SQ-16 | holds | m-8 of V3-B closed |
| R5-10 | RELAY SQ-09 ("outcome unknown" not for reads; ADAPTER M-3) | holds | — |
| R5-10 | RELAY coverage | holds | C U-C4 → SQ-07 (g); U-C6 → SQ-18 (e); U-C10 → SQ-07 (h); P U-P6 → SQ-05 (g); AS U-04 → SQ-05 (h); RS U-12 → SQ-03 (e); WD U-09 → SQ-19 (d); ACT U-06 → SQ-05 (i); WD U-10 → "Not included" with its D1 reason; VC-R-08 added. V3-B MAJOR-3 closed |
| R5-10 | CA S-13, §2.2, DI-6, UNRESOLVED; XT S-10, IN-25, §3.3 "Gate"; ADAPTER GC-5, §3.1; GUIDE B-7, §2.13, §2.9 note | holds | — |

## 2. Integrator pass-through rulings (item 2)

| Ruling | Owner text | Other texts in my half | Result |
|---|---|---|---|
| **HP-4 and person-directed turns** (EXEC §2) | HP-4 row: the scope covers only App-initiated turn starts and App-as-caller calls. A person's own message is not blocked; it is carried with initiator *person-directed*; the disposition is unchanged; governed agent actions in it are *action during hold*. The ruling "closes HOSTING U-25" | HOSTING §6.7 already carries such a turn "with initiator `person-directed`" and never presents it as a hold, so its behavior matches. ADAPTER GC-5 and XF-42 limit HP-4 to App-initiated turns and calls. GUIDE B-7 applies HP-4 | **holds.** The one gap is bookkeeping: HOSTING U-25 and F-22 are still open (m-5) |
| **Multi-checkpoint precedence** (EXEC §3.5) | Any *not enforceable* → *unsupported*; else any *not established* → *not established*; else passes | GUIDE M8.3 and the §2.14 worked case. CA §2.2 and RELAY SQ-02 apply the precedence ("E1 via X unsupported whatever SQ-02 returns") | **holds** |
| **App-only (HS-5)** | Arrival **and** held actions involve no host operation. Examples: E1 `CP-check` in an App run; kind (b)/(c) run halts **other than an A5 constraint**; App content; a harness-capability kind (a) | CA §2.2, RELAY SQ-02, GUIDE §2.14 and XT S-10 agree. ADAPTER GC-5 second bullet says "a kind (b)/(c) run halt" without the A5 exception; GC-3 covers A5 separately (m-4) | **holds**, with m-4 |
| **SQ-02-status mapping (HS-3)** | (a) answered and evidenced → *enforced on the host route*; (b) unanswered → *not established*; (c) answered with no host-held route → *not enforceable*. Never assumed | ADAPTER GC-3, GC-5 and F-19 hold; XF-26 is the (c) variant. GUIDE §2.14 and HC-6.3 hold. CA S-13 and §2.2 (third bullet), XT S-10 and IN-25, and RELAY SQ-02 state "a constraint carried only as model-supplied → *not enforceable*" without the (c) condition (m-2). **C V-GR1 fails**: it assigns *not enforceable* to a host-operation kind (a) checkpoint today (MAJOR-1) | **partial** |
| **E1 via X is unsupported** (CA §2.2 and RELAY SQ-02) | EXEC MT-2: `CP-accept` *not established* (HS-3) and `CP-check` *not enforceable* (HS-5) → does not pass, *unsupported* | CA §2.2 (new paragraph), ST-4, W14-04 (iii), DI-6, F-15 and UNRESOLVED hold. RELAY SQ-02 "App assumes meanwhile" holds. GUIDE §2.14 worked case, F-10 and G-8 hold. C FXA-5 is silent on `CP-check` (m-3) | **holds** |

*Observation, not a finding:* E1's `CP-check` requires an A4 on host rows
(S-5, R-100), and the host act facility captures that act. Its **hold** is
App-only only because it arrives on the App agent's report and holds the App
Return step. CA F-15 already proposes the remedy: a reached-when on the host
outcome *applied (receipt)*. The owner may want this beside U-E23 when
choosing the OI-021 acting surface.

## 3. GUIDE-v0.2 — first independent review (item 3)

What I checked, and the results:

- **Header and pinning.**
  - Inputs are pinned at `d3cebd1cc`. I recomputed their sha256 values: 14 of
    the 16 are byte-identical at the candidate.
  - CA-v0.3 and RELAY-v0.3 were then changed in place by `816c917f0` without
    a version bump. GUIDE's CA hash `3bf6653c…` and RELAY hash `82dcaca5…`
    name bytes that the candidate no longer has. The candidate has
    `28a5cb80…` and `89b6b9c9…` (m-7).
  - GUIDE says it follows EXEC HS-3/HS-5 for E1 via X, which is where the
    in-place fix landed, so no guide statement is wrong.
  - The DEL-03-04 SoW sha256 (`203c0928…`) matches the working tree.
- **§1 boundary (B-1…B-9).** Consistent with D2, D3, D4, D5 (split per
  R5-4), D6 (with R5-10 scope) and R5-2.
- **§2 matrix (rows 1–10, M1.1…M10.3).**
  - I spot-checked the cited sections against headings at the candidate:
    - ACT §2.6, §4.4, §4.6, §5.3–§5.6, §8.3;
    - RS §2 (OF-n), §4.1, §6.1–§6.2, §7;
    - AS §3, §7, §8;
    - WD §4.2.4, §4.3.7, §4.3.8, §6.4;
    - LOOP §2.4.4, §4, §5.1–§5.2, §6–§8;
    - PANEL §3.1–§3.6, §4;
    - EXEC §4.8, §4.9, §4.12, §6.2–§6.7;
    - HOSTING §6.7, §6.8, §8.2, §8.3.
    All resolve.
  - Every host need cites an SQ with sub-question letters that exist in
    RELAY-v0.3.
  - The nine R5-10 sub-questions each have a home, as CC-4 claims.
- **§2.13.** Owners and points of need match the SoW TBD-001…TBD-009 text
  literally. The two added D6 rows correctly split EXEC U-E1 (to SQ-02) from
  U-E23 (to the owner).
- **§2.14.** Matches EXEC HS-1…HS-5. The worked case matches MT-1 and MT-2.
- **§3 checklist (HC-0…HC-10).** Complete against HI §10's ten items.
  - HC-1.7 bars a "generated or checked" claim while any cell is
    *unagreed*.
  - HC-6.3 states today's values correctly.
  - HC-9.1 makes SQ-28 the gate.
- **§4 completeness.**
  - CC-1…CC-9 are reproducible from the text.
  - CC-10 (no over-claim) is confirmed by this review: I found no claim of
    relay, answer, commitment, delivery, adoption, host behavior, a human
    act, an App hold, or a selected transport or placement.
  - CC-11 is stale and incomplete (m-9).
- **Representation neutrality.** M7.2 names "OpenAI-compatible Chat
  Completions with tool calls". That is accepted basis (V4-ARC-10, via LOOP
  §1). GUIDE does not select it.
- **Findings and UNRESOLVED.** F-9 and the UNRESOLVED row "Independent review
  of v0.2" are answered by this review. The VER-007 boundary-owner checker is
  still not run; I did not run it either.

GUIDE-v0.2 is fit to serve as the integrated index as a draft. The only
defects I found are m-7 and m-9.

## 4. No-over-claim sweep of all 17 files (item 4)

- Status lines:
  - 16 files: "DRAFT DEFINITION — proposed, unsupplied, not implemented, not
    accepted";
  - PIN_SPIKE: "OBSERVATION RECORD … not qualification";
  - RELAY adds "PREPARED FOR HUMAN RELAY — not delivered".
- Grep for completed-claim phrasing (implemented, qualified, delivered,
  relayed, adopted by, answered, witness passed) found only negations and
  conditionals: "Not yet recorded (no qualification)", "qualified
  separately", "D2 does not show that SWBPIPE has adopted".
- Every human act in the files is either a fixture step (T2, T11, T15, T16a,
  T17, GR-n) or a stated requirement. None is claimed as performed.
- RELAY's ledger shows "not observed" or "none" in every field.
- CA §9 standings are all *prepared* or *open*.
- XT and CA mark every W14 and XC case AWAITING INPUT, DESIGNED or HELD.

Result: **none found.**

## 5. Hold-support values (item 5)

- A grep over all 17 files for *held after observation*, *enforced before
  dispatch*, *host-enforced for host operations* and similar non-canonical
  terms finds them only in retirement statements or change logs:
  - EXEC §3.6 and change tables;
  - ADAPTER GC-3 and F-16/F-18;
  - ACT §4.6;
  - RS, LOOP, WD and GUIDE change tables.
- "Not holdable" (R4-21) always maps to *not enforceable*.
- Every value assignment uses one of the four values.

Result: **holds.** One valid value is **mis-assigned** (MAJOR-1).

---

## 6. Residuals

### MAJOR

- **MAJOR-1 — C V-GR1 gives `CP-grant` via X the wrong hold-support value.**
  - Where:
    - C-v0.5 §10.4 V-GR1, last sentence of the Expected cell: "From the App
      via X, `CP-grant` hold support is **not enforceable** (R5-1; D6)";
    - C "Changes from v0.4", R5-1 row: "`CP-grant` via X **not
      enforceable** (D6)".
  - Why it is wrong:
    - `CP-grant` is reached-when kind (a) *before dispatch of OP-C9*, which
      is a host operation.
    - EXEC-v0.3 HS-3, the owner of the value set, assigns such a checkpoint
      *not established* while SQ-02 is unanswered. It becomes *enforced on
      the host route* once evidenced, or *not enforceable* only if SQ-02 is
      answered "no". EXEC MT-16 states this case explicitly.
    - WD-EX-v0.5 E8 ("E1d from the App via X … **not established**"), WD
      VC-37 and ADAPTER GC-5 (host-operation kind (a) → *not established*
      until SQ-02 (d)) agree with EXEC. C alone differs.
    - R5-1's consequence list names *not enforceable* only for App-only
      checkpoints.
  - Effect:
    - The shared fixture, which every file cites, would make E1d *unsupported*
      on X.
    - It also contradicts R5-10: SQ-02 can move this checkpoint.
    - GUIDE CC-11 did not catch the conflict.
  - **Side: C.** Replace the sentence with: "From the App via X, `CP-grant`
    (kind (a) on host operation OP-C9) is **not established** until SQ-02
    (d) is answered (EXEC HS-3, MT-16; WD-EX E8)." Correct the change-table
    row the same way. This is a one-line fix and needs no ruling.

### MINOR

- **m-1 — Residual D5 over-credit (R5-4).**
  - Where:
    - CA DI-5: "**Settled for the App side**: … destination recorded and
      shown, not gated";
    - RELAY header Basis: "D5 settled — the model destination is recorded
      and shown, not gated";
    - XT IN-14: "the App side is settled: destination recorded and shown,
      not gated".
  - The body texts (S-12, SQ-16, S-9) are split correctly.
  - **Side: CA, RELAY and XT.** Say "no gate: SETTLED (D5); record and show:
    INTEGRATION (DECISION-2 reading)". Fix RELAY before the owner relays it.
- **m-2 — The HS-3 condition is dropped from the general statement.**
  - Where:
    - CA S-13 and §2.2 third bullet;
    - XT S-10 and IN-25;
    - RELAY SQ-02 "App assumes meanwhile".
  - Each says "a constraint carried only as model-supplied → *not
    enforceable*" without the qualifier "once SQ-02 is answered with no
    host-held route". Today every native-family A5 constraint on X is only
    model-supplied, so a literal reading contradicts the same files' "`CP-accept`
    *not established*". ADAPTER F-19 and EXEC §3.6 state the condition.
  - **Side: CA, XT and RELAY.** Add "(after SQ-02 is answered with no
    host-held route; before that, *not established*, EXEC HS-3 (b)/(c))".
- **m-3 — C FXA-5's X sentence is incomplete.**
  - "The same workflow run from the App through X would have `CP-accept`
    **not established**" omits `CP-check` → *not enforceable* (HS-5), so the
    workflow is *unsupported* (EXEC MT-2).
  - CA corrected the same omission in place (CA F-15).
  - **Side: C.**
- **m-4 — ADAPTER precision.** **Side: ADAPTER** (next revision).
  - (a) GC-5's App-only bullet lists "a kind (b)/(c) run halt" without HS-5's
    "other than an A5 constraint". Suggested: "… (GC-3 covers A5)".
  - (b) §11 "Provide to DEL-04-03" still reads "model destination per run
    (R4-1)"; it should read per turn, per R5-4.
  - (c) F-18 and F-19 can be closed: EXEC-v0.3 HS-3 aligned and confirmed
    the reading ("integrator confirmation; ADAPTER-v0.3 F-18/F-19").
  - (d) S-X13 and §5.1 could say explicitly that a received constraint
    **verified against the host's own copy** is host-held (R5-2 wording). P
    §3.3 and XT S-10 already say so.
- **m-5 — HOSTING U-25 and F-22 are still open.**
  - EXEC-v0.3 HP-4 records the integrator's scope ruling (person-directed
    turns are carried, not blocked) and says it "closes HOSTING U-25".
  - HOSTING §6.7 still defers it to DEL-02-03 "until it does". The interim
    behavior is identical, so no meaning changes.
  - **Side: HOSTING.** Close U-25 and F-22 against EXEC-v0.3 §2 HP-4.
- **m-6 — Citation lag from the parallel pass (R5-9, partial).**
  - What lags:
    - CA, RELAY and XT cite siblings at `8fb51f07f` (EXEC-v0.2,
      ADAPTER-v0.2, GUIDE-v0.1, Wave-1 v0.4), but cite EXEC-v0.3 in the body
      after `816c917f0`;
    - CA §5 "Standing now" (EXEC "v0.2 draft", ADAPTER "v0.2 draft", Wave-1
      "v0.4 draft (v0.5 in the R5 pass)") and §11.1 are stale;
    - ADAPTER §12 is headed RELAY-v0.2 (GUIDE G-9);
    - XT §4.1 and F-16 still ask C to state V-ED1's branching, which C-v0.5
      now does.
  - Each file declares the lag (CA F-17, XT F-17, the ADAPTER VC note, the C
    and P headers).
  - **Side: each file**, as a mechanical re-point at its next revision. None
    is substantive beyond MAJOR-1, m-3 and m-5.
- **m-7 — In-place changes without a version bump.**
  - `816c917f0` changed CA-v0.3 and RELAY-v0.3 without a bump. Each version
    label therefore names two byte states:
    - CA: `3bf6653c…` at `d3cebd1cc` and `28a5cb80…` at the candidate;
    - RELAY: `82dcaca5…` at `d3cebd1cc` and `89b6b9c9…` at the candidate.
  - GUIDE-v0.2 pins the earlier bytes.
  - Content is consistent, but identity-by-version is ambiguous for a file
    that is about to be relayed.
  - **Side: coordinator, or CA and RELAY.** Record the post-fix sha256 in the
    change row, or bump to v0.3.1. GUIDE records the candidate hashes at its
    next revision.
- **m-8 — The RELAY ledger misstates its history.**
  - §4 "Prepared" row: "revised to RELAY-v0.3 in sweep A1 (R4; DECISION-2)".
    In fact v0.2 came from A1 (R4) and v0.3 from the R5 pass (plus the
    `816c917f0` in-place fix).
  - The ledger is the relay's custody record.
  - **Side: RELAY**, before relay.
- **m-9 — GUIDE CC-11 and F-11 are stale and incomplete.**
  - (a) F-11 says CA §2.3 CA-H "states 'the run holds at CP-accept and
    CP-check' without the surface qualification". But the same cell ends "in
    App runs the hold is claimed only where hold support says it is
    enforced, otherwise *action during hold* is recorded (S-13)". The
    `816c917f0` correction did not touch CA-H, so "coordinator notes a CA
    correction may follow" is superseded.
  - (b) CC-11 lists three remaining conflicts. It misses MAJOR-1: C V-GR1
    against EXEC MT-16, WD-EX E8 and GUIDE's own §2.14 HS-3 row.
  - (c) F-9, CC-10 and UNRESOLVED should record this review as v0.2's first
    independent check.
  - **Side: GUIDE.** Optionally, CA can add "(on E)" after "the run holds"
    in CA-H to make F-11 moot.

## 7. Items for the owner (no ruling requested here)

- **E1 via X.** E1 via X is *unsupported* whatever SWBPIPE answers, because
  `CP-check` is App-only (EXEC U-E23; CA F-15; GUIDE F-10 and G-8). The
  embedded route is the only one on which the proposed first-activity
  workflow passes hold support in this increment. This bears on the OI-021
  choice of acting surface.
- **SQ-28 is a precondition for the external route.** It gates the whole
  external channel, so every CA/X and XC case waits on it as well as on
  SQ-02.
