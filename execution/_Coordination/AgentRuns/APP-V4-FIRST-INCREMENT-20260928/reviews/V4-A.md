# V4-A — independent review of the final Wave-2 candidate (policy, records, workflow, execution, loop, panel)

- Node: V4-A, run `APP-V4-FIRST-INCREMENT-20260928`. Reviewer: independent
  Type 2 (Claude Code subagent). I authored none of the reviewed files and
  delegated nothing.
- Candidate: commit `c7f5513db` (branch `claude/chirality-app-v4-60-percent-a41fd5`).
  The 17 Design files (`git ls-tree -r --name-only c7f5513db -- … | grep
  /Design/ | grep -v generated/`) were read with `git show c7f5513db:<path>`
  into a private scratch folder. Read-only git only; no network.
- Scope, per BRIEFS.md "V4" (working copy, sha256 c85c3519…d0ee7b): DEL-04-01,
  DEL-04-02, DEL-04-03, DEL-02-01 (WD and EXAMPLES), DEL-02-03, DEL-05-01,
  DEL-05-02. Other files (C, P, ADAPTER, GUIDE, HOSTING, CA, RELAY, XT) were
  read only where an R5 ruling or a pass-through ruling touches my subjects.
  GUIDE-v0.2's full first review (V4 item 3) belongs to V4-B (DEL-03-04 is in
  V4-B's list); I checked only its hold-support row, which inherits MAJOR-1.
- Rulings: R5_RESOLUTIONS.md (254d0b93…dd6f1), R4_RESOLUTIONS.md
  (50a009b2…032a24), OWNER_DECISIONS.md (a9869129…68ad2c; DECISION-1 and -2);
  all three byte-identical at the candidate and in the working tree. History:
  reviews/V3-A.md (f25f5af1…21d87).
- Method: full read of EXEC-v0.3, WD-v0.5 (§§1–4, 8, 11–13), WD-EX-v0.5, ACT
  §§1–4, §10–§14; AS-v0.5 and RS-v0.5 in full; LOOP §§0–2, 11–13 and registers;
  PANEL §§0–3, 7–8 and registers; C-v0.5 §10.4 V-GR1 and its change rows; P
  §3.3/§4.4; HOSTING §6.7, F-22, U-25; CA §2.2, WR-11, W14-03/04; RELAY SQ-02;
  GUIDE §2.14 row. Grep sweeps over all 17 files for hold-support values,
  retired values, carriage terms, D5 labels, V-GR1, L-labels, stale citations
  and claim language.

## Inputs (sha256, as committed at `c7f5513db`)

| File | Version | sha256 |
|---|---|---|
| DEL-02-03 `EXECUTION_COMPATIBILITY.md` | EXEC-v0.3 | 889e48819baa21ec112c4878e4e38004dcbaa9eb3645a31c24221ac116ee548e |
| DEL-02-01 `WORKFLOW_DECLARATION.md` | WD-v0.5 | 32acdd27b9d19f1e224a0dd914ef4c986f32b708e204a648745b50725145e7c9 |
| DEL-02-01 `EXAMPLES.md` | WD-EX-v0.5 | 296875c9aba92be6a3ef86c3ce9d658a9b6ba1d102db71a12f5f0c5c44a4702f |
| DEL-04-01 `ACT_AND_POLICY_CONTRACT.md` | ACT-POLICY-v0.5 | 86975a90567b35916464946a736687268bd532a4a1fdb02fe1a3ee07f35380e7 |
| DEL-04-02 `AUTONOMY_AND_STANDING_EXCHANGE.md` | AS-v0.5 | c49be8bb4d8e4b38c9a5f9692c40e0da61636eb688ed41dec5b64eb8666729e1 |
| DEL-04-03 `RECORD_SEMANTICS.md` | RS-v0.5 | 37bc586e247181fcf850fa2aadfd1a06cd787988e8e27f7711d093d0369c27ea |
| DEL-05-01 `LOOP_RECEIVING_CONTRACT.md` | LOOP-v0.5 | 43e039aaae9c0c45d3775b606adbae59930caba7c9d8e9be9c03d39321701ca4 |
| DEL-05-02 `PANEL_RECEIVING_CONTRACT.md` | PANEL-v0.5 | e7d62beea0d8e9d4609c23af0d5fcff52b5af26b2f99d8260e7717633fbbed88 |
| Context: DEL-03-01 C-v0.5 | | a6306bd477decad22d4405fb86ca6212fb189e4865c68dbbcba90e1335be7a29 |
| Context: DEL-03-02 P-v0.5 | | a5ee4946046cf3fb2356872f5972892272e0dfb533c0317bcb5801773edcd1b7 |
| Context: DEL-01-01 HOSTING-v0.5 | | 873e76f693975242893f74d4243b01a48cab54a91f434fb01e37ec70fb5b0eaa |
| Context: DEL-09-06 CA-v0.3 / RELAY-v0.3 | | 28a5cb80…fb14ce4 / 89b6b9c9…68bdd7 |
| Context: DEL-03-04 GUIDE-v0.2 | | 5a9507e9…49b36d8 |

Line numbers below refer to the files at `c7f5513db`.

## Verdict

**MERGE AS DRAFTS.**

- No BLOCKING residual. Every file carries "DRAFT DEFINITION — proposed,
  unsupplied, not implemented, not accepted" (PIN_SPIKE: "OBSERVATION RECORD
  … not qualification"). No file claims implementation, qualification, host
  delivery or adoption, a performed human act, or relay delivery (§4).
- All ten R5 rulings are applied in substance in my seven files. V3-A's five
  MAJORs are resolved (hold-support vocabulary, RS E10, CH-12…14, L-WDEX
  re-points, shared A12 fixture).
- Only the four R5-1 values are used anywhere in the 17 files; retired values
  appear only in retirement notes and historical change rows (§5).
- Four MAJOR residuals remain. None creates a hold claim; each makes a fixture
  or definition report a *weaker-than-ruled* or *different* check result, or
  leaves a case without a deterministic value. They should be the content of a
  small follow-up micro-pass (or fixed before merge if an edit pass happens
  anyway). MAJOR-1 needs an integrator decision.

Counts: **BLOCKING 0 · MAJOR 4 · MINOR 14.**

---

## 1. R5 rulings against the text

| Ruling | Verdict | Evidence | Residual |
|---|---|---|---|
| **R5-1** one value set | **partial** | EXEC §3.6 (l.282–330) publishes the four values with HS-1…HS-5 and §3.5 precedence; WD §4.3.8 (l.518–543), ACT §4.6 (l.613–659), AS §4 (l.155–170), RS R8 (l.139), LOOP §2.4.4 (l.613–652), PANEL §3.2 all use them. E1-over-X consequence (`CP-accept` *not established*, App-only *not enforceable*, workflow *unsupported*) stated in EXEC MT-2, WD-EX E8, WD VC-37, ACT FX-48(b), CA §2.2, RELAY SQ-02 | HS-5 definition vs its examples (MAJOR-1); E1d-over-X result (MAJOR-2); C V-GR1 `CP-grant` via X (MAJOR-3); AS F18 variant (MAJOR-4); LOOP gives invalid declarations a value (m-5) |
| **R5-2** carriage final | holds | EXEC §2 HP-H, §3.6; WD §4.2.2 (l.228), I-7; ACT §4.4 (l.549–568); AS §2; RS §5; LOOP C-6; WD-EX R-5b; P §3.3 (l.165) removes the host loop from App-assured and states "not available in this increment" | — |
| **R5-3** grant-setting subject | holds | WD §4.3.1 grant-setting row (l.306), §4.3.6 (l.463), FB-17; ACT §4.2 (l.456, l.467–471) unconditional (fixes V3-A m-5); LOOP §2.4.2; PANEL W-5a; EXEC §4.10 (l.602–613), CH-29; AS §4; ACT FX-52 | WD VC-41 and ACT FX-44 citations (m-9) |
| **R5-4** destination; attribution | holds | RS R5 per turn, set, no new run, INTEGRATION (DECISION-2 reading); EXEC CR-14 at report time, §6.1 *supplied*/*observed behavior*, RT-5; AS S15; RS D16; ACT header l.27, V-10; LOOP §1 item 5 and §2.1; PANEL (nothing to relabel, checked). No "SETTLED" remains on record-and-show in my files | — |
| **R5-5** undo re-holds | holds | EXEC RH-8/RH-9 (l.510–524), CH-30; ACT §4.3 (l.523–530), FX-39; AS §4 lapse, F6, VC-10; RS L-12, OE-8, R11, E6, VC-26; LOOP C-4; PANEL W-5e | — |
| **R5-6** person's own operations | holds | ACT §2.4 (l.287–301), FX-53; RS §3, §5, E1/E2, VC-27; AS DS-6; EXEC RH-8 | — |
| **R5-7** V-GR1 | holds, one fixture slip | C-v0.5 §10.4 l.620 adds V-GR1 (run 13, GR-1…GR-3, GR-P/R/S, main-order negative, SP-6 cost). EXEC CH-12…14; WD-EX R-16 (ii)–(v); ACT FX-41/46/51; LOOP FX-C11/C11b; PANEL PC-21f/i; AS F14–F16; RS E7/VC-13 all agree that T15-before-arrival does not count. Owner-visible cost recorded under U-E4 / U-31 / U-14 / U-17 / U-26 | WD-EX R-16 (iv) names the wrong setting in force (m-3); stale "V-GR1 not yet in C" markers (m-1); stale L-EXEC-13/14 reasons (m-2) |
| **R5-8** RS E10/VC-17 | holds | RS E10 (l.474–490): *not enforceable* (App-only) → *unsupported*; arrival recorded; action during hold; "no stop is claimed/recorded"; (vii) *not established*. VC-17 matches | — (E10 illustrates MAJOR-1's ambiguity) |
| **R5-9** citations | holds (substantive items), minor lag | EXEC L-WDEX re-points by content verified row by row (MT-3 → L-WDEX-13, MT-4 → L-EXEC-26, MT-13 → V-NP1, MT-14 → E7 row, CH-7/CH-10 → R-4 (ii)/(iii), CH-18 → V-S1, CH-19 → L-WDEX-4, CH-20 → L-WDEX-7); L-EXEC-19 → AF-1; LIB-A1/LIB-A2; FXA-n everywhere (FA-n only in history rows); ACT FX-50 drops ADAPTER U-X3; P "confirmed by DEL-02-03" | Headers cite siblings at `8fb51f07f` and mark R5 elements "pending/being added" that are now present (m-1) |
| **R5-10** relay framing (consequences in my files) | holds | EXEC F-17, U-E23; WD §4.3.8 last paragraph, U-30; ACT F-16; AS §1; RS §1, U-25 | — |

## 2. Integrator pass-through rulings

| Ruling | Verdict | Evidence / residual |
|---|---|---|
| **HP-4 and person-directed turns** (EXEC §2) | holds | EXEC HP-4 (l.171): App-initiated turns and App-as-caller calls only; a person's turn is not blocked, carried *person-directed*, disposition unchanged, governed agent actions are *action during hold*; closes HOSTING U-25; CH-22 exercises it. Consistent with HOSTING §6.7 interim text and F-22. RS OE-8/R11 (the person's own operations never *during hold*) do not conflict, since the flagged actions are the agent's. Residuals: HOSTING still lists U-25 open (m-12, V4-B side); RS R11 does not yet carry the turn initiator EXEC F-24 proposes (m-13) |
| **Multi-checkpoint precedence** (EXEC §3.5) | **partial** | EXEC §3.5 (l.251–263), WD §4.3.8 (l.534–536), WD-EX E8 (l.372), CA §2.2, GUIDE apply "any *not enforceable* → unsupported; else any *not established* → not established". Misapplied in AS F18 variant (MAJOR-4) and in the E1d-over-X rows (MAJOR-2) |
| **App-only (HS-5)** | **partial** | The definition and the examples in HS-5 disagree (MAJOR-1) |
| **SQ-02-status mapping (HS-3)** | holds | EXEC HS-3 (a)/(b)/(c) (l.302) and the §3.6 GC-3/GC-5 paragraph; WD §4.3.8 rows; ACT FX-50 (*not established* before SQ-02, *not enforceable* after a "no host-held route" answer); EXEC MT-16, CH-27. LOOP G-5 (l.1075) still reports an EXEC-v0.2 divergence that v0.3 removed (m-6) |
| **E1 via X is unsupported** (CA §2.2; RELAY SQ-02) | holds | EXEC MT-2, WD-EX E8, WD VC-37, ACT FX-48(b), CA l.123–127, RELAY SQ-02 "App assumes meanwhile" agree: `CP-accept` *not established*, `CP-check` *not enforceable*, workflow *unsupported* whatever SQ-02 returns. AS F18 variant contradicts it (MAJOR-4) |

## 3. GUIDE-v0.2

Assigned to V4-B (DEL-03-04 is in V4-B's list). The only GUIDE text on my
subjects is its §2.14 HS-5 row (l.316). It copies both HS-5 wordings, so it
inherits MAJOR-1 and should re-point after the EXEC fix. GUIDE CC-11 (l.473)
independently flags CA-H's surface-unqualified "run holds" wording.

## 4. No-over-claim sweep (all 17 files)

- Status lines: 16 files carry the DRAFT DEFINITION status; PIN_SPIKE is an
  "OBSERVATION RECORD … not qualification", and its observed facts are spike
  observations authorized by D4, not qualification.
- RELAY: "PREPARED FOR HUMAN RELAY — not delivered"; delivery, answer and
  adoption "not observed" (l.3, l.1015).
- A claim-language sweep (implemented / qualified / delivered / relayed /
  adopted / confirmed by SWBPIPE / owner approved) found only negations,
  "not observed" ledger entries and designed-case expectations.
- Every "Engineer A performs …" is fixture material under an explicit
  "invented; no act was performed" framing (RS §12, WD-EX, ACT §13, AS §11).
- No App hold is claimed: every App-run case uses *not enforceable* or *not
  established* and records action during hold. One nuance: RS L-12 and AS §4
  say "the run stops at its next action" under *enforced on the host route*,
  though HP-H holds host operations only (m-4). No value today reaches that
  state, so it is not an active over-claim.

## 5. Hold-support values

Only *enforced by the host loop*, *enforced on the host route*, *not
established* and *not enforceable* appear as values anywhere. "Enforced before
dispatch", "held after observation" and "host-enforced for host operations"
appear only in retirement statements (EXEC l.286–287, ACT l.627–628, ADAPTER
l.471/986, LOOP l.633) and historical change rows (LOOP l.104; GUIDE and RS
change rows). CA WR-11's "enforceable on the host route" is descriptive prose,
not a value. The only divergence is in assignment, not vocabulary: LOOP gives
invalid declarations *not established* (m-5), and the assignments in
MAJOR-1…MAJOR-4.

---

## 6. Residuals

### MAJOR

**MAJOR-1 — HS-5's definition of "App-only" contradicts its own examples, and
HS-3 and HS-5 together are not exhaustive.**

Side to change: **EXEC** (§3.6 HS-3/HS-5), after an **integrator ruling**.
Then re-point CA §2.2 bullet and WR-11, RELAY SQ-02, GUIDE §2.14 and WD
§4.3.8.

- The definition (EXEC HS-5, l.304) says a checkpoint is App-only when "its
  arrival **and** the actions it holds involve no host operation". The same
  row's example includes "**any kind (b) or (c) run halt other than an A5
  constraint**".
- These disagree for non-A5 kind (b)/(c) checkpoints whose arrival is a host
  outcome, or whose held actions include host operations. Examples in the set:
  - E1c/E1d `CP-check` (A4, kind (c) on OP-C9 *applied*);
  - AS F6c (A4 on T16's applied outcome, App run on X);
  - RS E10 `CP-row-check` (arrives on T4a's OP-C12 output and holds T5, a
    host proposal);
  - ACT `CP-L4`.
- By the example, these are *not enforceable*. That is how AS F6c and RS E10
  read them.
- By the definition they are not App-only. HS-3 covers only A5 constraints
  and kind (a) before dispatch of a host operation, so no row assigns them a
  value. That breaks "exactly one value" (R5-1) and VC-E-12's "each case gets
  exactly one value per HS-1…HS-5".
- The neighbouring texts follow the definition, not the example:
  - CA §2.2 (l.118–120) and RELAY SQ-02 (l.153) describe App-only run halts
    as "a run halt **after an App-side output**";
  - CA WR-11 (l.216) tells authors that "a workflow meant to run in the App
    declares its checkpoints on host operations (enforceable on the host
    route once SQ-02 is evidenced)". That invites exactly the kind (c)-on-a-host-outcome
    checkpoints that HS-5's example makes *not enforceable*.
- This is load-bearing: it decides whether SQ-02 can ever make E1c/E1d
  supported from the App.
- Fix: the integrator rules which reading holds. Options:
  - **(a) Conservative, matching R5-1's "never claim a hold".** Every App-run
    checkpoint that is not an HS-3 host-operation checkpoint is *not
    enforceable*. HS-5 is restated as "any other checkpoint in an App run",
    and CA/RELAY say "any run halt other than an A5 constraint".
  - **(b) Widened.** HS-3 also covers non-A5 run halts whose held actions are
    host operations, as *enforced on the host route* for those operations
    only, with App-side actions recorded as *action during hold*. This needs
    SQ-02 wording to ask it.
- Either way, the HS rows become an exhaustive partition.

**MAJOR-2 — E1d from the App via X is given workflow result *not established*;
E1d also carries E1c's `CP-check`.**

Side to change: **EXEC** (MT-16, l.888), **WD-EX** (E8 row l.374; E1d
l.226–237 is "as E1c, plus `CP-grant`"), **WD** (VC-37, l.911).

- E1d = E1c plus `CP-grant`. So an App run of E1d over X has two checkpoints:
  - `CP-grant` (kind (a) on OP-C9): *not established*, HS-3 (b). Correct.
  - `CP-check` (A4, kind (c) on OP-C9 *applied*): omitted from every E1d
    row.
- Under HS-5's example (and AS F6c, which values the same shape), `CP-check`
  is *not enforceable*. The §3.5 precedence then makes the workflow
  **unsupported**, not *not established*.
- MT-16 ("check not established"), E8 ("not established (never a pass, never
  *unsupported*)") and VC-37 all state the weaker result.
- Under the definition reading, `CP-check` has no value (MAJOR-1).
- Fix after MAJOR-1:
  - add the `CP-check` row to E8 and MT-16 with its value;
  - state the workflow result by the precedence;
  - or narrow MT-16/E8 to a variant of E1d without `CP-check`, with an
    `L-‹file›-n` label.

**MAJOR-3 — C-v0.5 values `CP-grant` via X *not enforceable*, contradicting
HS-3 (b).**

Side to change: **C** (DEL-03-01; V4-B's file, reported here because EXEC owns
the values).

- C §10.4 V-GR1 (l.620, last sentence) says "From the App via X, `CP-grant`
  hold support is **not enforceable** (R5-1; D6)". The C R5-1 change row
  (l.657) says the same.
- `CP-grant` is kind (a) before dispatch of host operation OP-C9, which is an
  HS-3 host-operation checkpoint. Before SQ-02 it is **not established**
  (EXEC HS-3 (b), MT-16; WD-EX E8 l.374; WD §4.3.8 "not established" row,
  which names "a kind (a) checkpoint on a host operation the host would have
  to hold").
- C is the fixture authority, so consumers citing V-GR1 for the App surface
  would inherit the wrong value. The error is conservative (no over-claim),
  but it contradicts the ruled assignment.
- Fix: C states `CP-grant` via X *not established* (HS-3, awaiting SQ-02), and
  the E1d workflow result per MAJOR-2.

**MAJOR-4 — AS F18's variant gives E1 on X the check result *not
established*.**

Side to change: **AS** (F18, l.390; VC-03 l.421 lists F18's result).

- The variant reads "`CP-accept` in an App run of E1 on X … requirement check
  *not established*, not *unsupported*".
- E1 on X also has `CP-check`, which is App-only and *not enforceable*. The
  ruled result is therefore **does not pass — unsupported** (R5-1
  consequence; EXEC §3.5, MT-2; WD-EX E8; ACT FX-48(b); CA §2.2; RELAY
  SQ-02).
- Fix: either state both checkpoints and the *unsupported* result, or recast
  the variant as a workflow declaring only `CP-accept` (local label with its
  reason).

### MINOR

| # | Where | Residual | Side |
|---|---|---|---|
| m-1 | EXEC header l.30, §7 l.855, §9.1 C row, F-26; WD-EX fixture table l.69, change row l.19; ACT header l.23, §13 l.1131; AS/RS headers ("C v0.5 variant V-GR1 … not read"); LOOP UNRESOLVED last row; PANEL UNRESOLVED last row; WD §8 supplier states l.745–750 ("pending its v0.5"), §8 "Receives from WD-v0.4", §9 "Allocation result at v0.4" | V-GR1, the R5-1 values and P §3.3 are now present in C-v0.5, EXEC-v0.3 and P-v0.5. This review re-verified V-GR1 against every consumer (§1 R5-7): all agree except m-3. Close EXEC F-26 and the "pending"/"not yet in sibling text" rows | All seven files (mechanical) |
| m-2 | EXEC CH-12 (ii) L-EXEC-13 ("V-GR1 fixes only the established outcome"); CH-13 L-EXEC-14 ("C has no refused A12 on P-03"); CH-14 | C-v0.5 now has GR-P (pending, then lost), GR-R (refused on P-03 at arrival) and GR-S (later established A12 narrowing). The local cases remain distinct (pending then *established*; refused *after* performance), but their stated reasons are stale. CH-14 can cite GR-S directly | EXEC |
| m-3 | WD-EX R-16 (iv) (l.274) | For V-GR1's refused sub-variant it says "⟨set-2⟩ stays in force, not superseded". In V-GR1 the refused A12 is T15's own, so ⟨set-2⟩ never takes effect and ⟨set-1⟩ stays in force (C GR-R l.620; ACT FX-46(b)) | WD-EX |
| m-4 | RS L-12 (l.301), OE-8, R11; AS §4 lapse (l.199) and "Action during hold" bullet; WD I-9 | These say the run "stops at its next action" under *enforced on the host route*, and record action during hold only where "the hold was not enforced". EXEC §3.6 (l.316–318) records action during hold under **any value other than *enforced by the host loop***, because HP-H holds host operations only and App-side actions continue (R5-10). Align RS/AS/WD to EXEC | RS, AS, WD |
| m-5 | LOOP §2.4.4 table (l.628) | Gives an invalid or not-established declaration the hold-support value *not established*. EXEC HS-1/F-22 and WD §4.3.8 (l.532–534) assign **no** value. The check result is the same. Also, R5-1 says "each checkpoint … exactly one value" and does not cover invalid declarations. The integrator should confirm F-22 ("no value") | LOOP; HELP_HUMAN to confirm F-22 |
| m-6 | LOOP Findings G-5 (l.1075) | Reports that EXEC-v0.2 §3.6 values model-supplied carriage *not established*. EXEC-v0.3 HS-3 (c) now gives *not enforceable* after SQ-02 and *not established* only before, matching R5-1. Close G-5 | LOOP |
| m-7 | LOOP §2.4.4 HS-0…HS-4 vs EXEC §3.6 HS-1…HS-5 | The same label family is used for different things. "HS-3" now means "App-side holds are not this contract's" in LOOP and "host-operation checkpoint assignment" in EXEC, and other files cite EXEC HS-n. Rename LOOP's to, e.g., HL-n or LH-n | LOOP |
| m-8 | EXEC HS-1 vs "exactly one value per checkpoint" (§3.6 opening l.284; VC-E-12) | The opening sentence and VC-E-12 should say "each valid checkpoint", matching HS-1 | EXEC |
| m-9 | ACT FX-44 (l.1200) cites "EXEC VC-41"; WD VC-41 (l.915) cites only R4-9 | EXEC has no VC-41 (its cases are VC-E-nn; the case is EXEC CH-29 / WD VC-41). WD VC-41 should cite R5-3 and include "even with an A8 presenting a setting" (as FB-17 does) | ACT, WD |
| m-10 | AS VC-03 (l.421) | "not established → not established" is listed as F18's expectation. It follows MAJOR-4 | AS |
| m-11 | CA W14-03 (l.363) vs EXEC RT-11 and §9.2 | EXEC maps W14-03 ← MT-1, MT-2, MT-3, MT-10, MT-15, MT-16, and §9.2 expects "W14-03/W14-04 values match MT-2 and MT-16". CA W14-03 cites MT-1, MT-3, MT-10, MT-15 only | CA (V4-B) |
| m-12 | HOSTING U-25 (l.1074), §6.7 HP-4 bullet | EXEC-v0.3 states the HP-4 scope and records HOSTING U-25 as closed. HOSTING still lists U-25 open, with "DEL-02-03's to state" | HOSTING (V4-B) |
| m-13 | RS R11 / OE-8 vs EXEC F-24 | EXEC proposes that an action-during-hold entry carry the turn initiator, so an agent action in a *person-directed* turn is distinguishable. RS-v0.5 does not carry it yet. This is a proposal, not a ruling; route it to DEL-04-03 | RS (optional) |
| m-14 | GUIDE §2.14 row (l.316) | Copies both HS-5 wordings; re-point after MAJOR-1 | GUIDE (V4-B) |

---

## 7. Prioritized follow-up

1. **MAJOR-1**: the integrator rules the App-only / host-operation partition
   (option (a) or (b)). EXEC restates HS-3/HS-5 exhaustively. CA §2.2, CA
   WR-11, RELAY SQ-02 and GUIDE §2.14 re-point before the relay file is
   handed to the owner, since SQ-02's "App assumes meanwhile" text depends on
   it.
2. **MAJOR-2 / MAJOR-3**: E1d over X. Add `CP-check`; `CP-grant` is *not
   established*; the workflow result follows the precedence. Apply in EXEC
   MT-16, WD-EX E8, WD VC-37 and C V-GR1 with its R5-1 row.
3. **MAJOR-4**: AS F18 variant and VC-03.
4. m-3 and m-4 (substantive minors), then m-5 (confirm F-22), then the
   mechanical currency pass (m-1, m-2, m-6…m-9), and the V4-B-side items
   m-11, m-12, m-14.

The set is fit to merge as v0.5/v0.3/v0.2 **drafts**. None of the residuals
creates a hold claim, changes an owner ruling or asserts external evidence.
They should be cleared before any fixture is designed from the App-run
hold-support rows, and before RELAY is relayed.
