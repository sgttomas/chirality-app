# RV-EXP-U1 — review of DEL-09-01 EXP-v0.1 (examination protocol, schemas, prototype)

- Reviewer: RV (Type 2 TASK, Claude Opus 5.5), run `APP-V4-DESIGN-PASS-4-20261003`, 2026-10-03. Method: `coordinated-knowledge-work` §3.
- Unit: `PKG-09_Candidate examination and connected journeys/1_Working/DEL-09-01_Candidate examination infrastructure and evidence protocol/Design/`. All five expected hashes match (`shasum -a 256`):
  - `EXAMINATION_PROTOCOL.md` `dc6b6a0c…ecbc0`
  - `exam.result-record.schema.json` `7c994445…7cd66`
  - `exam.review-record.schema.json` `c1c7b770…c55f0`
  - `exam.change-impact.schema.json` `b6f2d355…e7dc91`
  - `prototype/check_exp.py` `a9f13e1e…54c1e3`

  The nine example-set files also match the hashes in `OWNERS/O-B.md`.
- Owner record read: `OWNERS/O-B.md` (U1 claims 1–7, checks, open items).

## Verdict: **REPAIR**

There are 4 MAJOR findings (two of them cross-owner, which need a HELP_HUMAN ruling), 7 MINOR and 2 NOTE. There is no BLOCKING finding. The structure can be kept as it is: the vocabulary mapping, the three records, the case states, the reopening and repair sequences, the review protocol, the routes and the M1–M3 milestones.

## Findings

### EXP-R-A — MAJOR, cross-owner — EXP-R1 cannot represent a part excluded as not applicable (§3.1 EXP-R1; OUT-1)

- **Evidence.**
  - EXP §3.1 (EXP-R1): "`not-run` if no part ran; otherwise `inconclusive`", with no exclusion. The prototype's `aggregate()` (`check_exp.py`) implements exactly that.
  - DEL-09-07 LHQ-v0.1 §6.2 LR-4 (O-C, frozen at `2668d955…`): "Parts that are *not run* only because their phase or optional subject is absent (P22-G, P23-E) are excluded from aggregation and listed."
  - DEL-09-07 consumes EXP's record (DEP-09-01-025, admitted; EXP §2.2 OUT-1).
  - Probe: `aggregate()` over four `pass` parts and one `not-run` part (P22-G, "phase not taken up") returns `inconclusive` (scratch `$TMPDIR/rv/probe_exp.py`, P3).
- **Consequence.** A journey record that conforms to both files cannot `pass` LHQ-22 in the current phase. That contradicts REQ-005/V4-EXM-22, under which the hold is examined only for a governance-phase workflow. CA W-R6, which both sides cite, is silent on optional parts.
- **Route.** This is a shared-basis conflict, so it goes to HELP_HUMAN for one ruling (workflow §5). One way to resolve it: EXP adds a part-level `not_applicable` reason (or an `excluded_from_aggregation` marker that must state its reason), which EXP-R1 skips and lists. Alternatively, LHQ drops such parts from the record. It is also raised in RV-LHQ-U1 as LHQ-R14.

### EXP-R-B — MAJOR, cross-owner — the `blocked` meaning is narrower than REQ-002 and is labelled SETTLED; at case start the receivers differ (§3.1; §6.1; F-1; NB-2)

- **Evidence.**
  - ScopeOfWork REQ-002 says: "blocked records the preventing condition; not-run states that execution has not occurred".
  - EXP §3.1 gives `blocked` the meaning "Execution started or was attempted and a named condition prevented the evaluation". It introduces the table with "Their meanings are EXAMINATION §1 and ScopeOfWork REQ-002 (SETTLED)", but "started or was attempted" appears in neither text.
  - EXP §6.1: "No result record is written for DESIGNED, AWAITING INPUT or HELD cases".
- **Receivers.**
  - CA W-R3 says "A result that is *not run* or *blocked* names what is missing (input, supplier, relay question)", and XT X-R2 says the same. Both allow either outcome for a missing input.
  - LHQ LF-1 and CI-3 record *blocked* for a CIR element not supplied "before any case".
  - XT's rehearsal table records *not run* records for missing surfaces (XC-04, TR-02…).
- **Where the rules agree.** Mid-case, EXP F-2 ("That part `blocked`; parts needing its end state `not-run`, 'blocked by ‹part›'") agrees with CA W-R5 and XT SR-4, which I compared word for word. The edge cases at case start are where the rules diverge.
- **Consequence.** The same condition (an input missing before the first step) is recorded as no record, `not-run` or `blocked` depending on the journey. That defeats §3.1's stated purpose, "so that every receiver applies them the same way" (AC-003), and the SETTLED label claims an authority the refinement does not have.
- **Repair.**
  - Label "started or attempted" PROPOSED, or remove it.
  - State one rule for a missing input at case start: no record while the case is AWAITING INPUT, and `not-run` with `missing_inputs` once a run is due on a named subject. Otherwise keep `blocked`, with the attempt as its boundary.
  - Put the rule to HELP_HUMAN together with EXP-R-A so that LHQ, CA and XT can adopt it.

### EXP-R-C — MAJOR — a packaged-route `pass` without a package record passes the schema and every rule (§9 NB-3; §10 M2; VER-008)

- **Evidence.** NB-3 says "a packaged witness needs the DEL-01-06 package record (schema)". The schema requires `package_record` only `if packaged: true` (`candidate_subject.app_candidate`). Nothing ties `configuration.route.kind: native_packaged` to `packaged: true`.
- **Probe P1.** I took valid example EXP-EX-04, set `outcome: pass`, and removed `packaged` and `package_record`. The schema accepts it and `rule_violations()` returns `[]`. The invalid example EXP-INV-08 tests only the `packaged: true` case.
- **Consequence.** A development build can be recorded as a `native_packaged` `pass` with no M2 package, which is the substitution NB-3 and AC-008 forbid. The control is claimed but not present.
- **Repair.** Add a schema conditional: if `route.kind` is `native_packaged`, then the subject must be a candidate with `packaged: true` and a `package_record`. Add an invalid example for it.

### EXP-R-D — MAJOR — R23-17 is not adopted, and the "definition check" it relies on is not defined (§8 N-2, interface runner; §13 U-EXP-1…4)

- **Evidence.** R23-17 (appended after freeze; R23 now `e4be2c2a…`):
  - U-EXP-4 digest: "sha256 … DERIVED".
  - U-EXP-1: "HELP_HUMAN names it when VC returns".
  - U-EXP-2: runner and tool "chosen by the implementer against EXP §8's definition check, and recorded".
  - U-EXP-3: "O-B's ordinary decision, within OI-013/OI-014's constraint".

  EXP §13 still assigns U-EXP-1, 2 and 4 to "App implementation owner (= owner, L-7)" and U-EXP-3 to the examination owner, open. EXP §8 N-2 says only "once that tool has its own definition check on the candidate". The check has no content, and the interface runner has no definition check at all.
- **Consequence.** At the 60% level an implementer cannot select or admit a runner or an N-2 tool, because the criterion R23-17 points to does not exist. Record placement and the native-step form layout remain undecided, although they are now O-B's to decide.
- **Repair.**
  - Define the definition check for the interface runner and the N-2 tool: what each must show on the candidate before its results count, and how it is recorded.
  - Decide U-EXP-3 (placement, form layout).
  - Restate U-EXP-1, U-EXP-2 and U-EXP-4 per R23-17. sha256 becomes the digest, so "notation only" in U-EXP-4 goes.
  - Re-pin R23.

### EXP-R-E — MINOR — EXP-R2 is referenced but never defined, and the rule set is nowhere stated as one list (§2.2 OUT-1; §6.4 step 4)

- **Evidence.** OUT-1 says "EXP-R1…R5, R9", and SQ-3 step 4 says "EXP-R1…R5 (the prototype's checks)". A grep of the `.md`, the schemas and `check_exp.py` finds no EXP-R2. The other rules are defined in passing across §3.1, §3.2, §4.1, §6.2, §7 and §9.
- **Consequence.** A receiver cannot read the rule set it must satisfy without reading the prototype.
- **Repair.** Add one rule table (EXP-R1…R9) with a statement of each, and either define EXP-R2 or retire it.

### EXP-R-F — MINOR — EXP-R6 counts an honest `not_separate` review as a violation (§7 RV-2; F-6; F-11)

- **Evidence.** F-6 says "Review recorded `not_separate`; not reported as independent". `review_violations()` adds EXP-R6 whenever `separation == "not_separate"` (probe P4: a valid example changed only in that field returns `['EXP-R6']`). F-11 then says such a record is "Not relied on until repaired". The schema has no element that claims independence.
- **Consequence.** Truthfully reporting non-separation makes the record invalid. That pushes writers away from the honest value.
- **Repair.** Add an explicit independence claim, or a standing such as `reported_as_independent`, and make EXP-R6 fire only when that claim is made with `not_separate`, or with the reviewer among the authors.

### EXP-R-G — MINOR — the review record admits reviewer kinds that V4-OPS-34 / R23-12 do not provide for (§7; review schema `preference.used`)

- **Evidence.** V4-OPS-34 (`docs/OPERATING_METHOD.md`): "a Codex reviewer and the stated different-model Claude fallback". R23-12: "SETTLED by V4-OPS-34 as written".
  - The schema's `used` enum includes `other`. Probe P5: `used: other` with `fallback_reason: "preferred"` is accepted.
  - `person` is forced through `fallback_reason` ("the actual unavailability"), while §7 says a person "may also review", that is, in addition.
- **Repair.**
  - Drop `other`, or state its standing. As I read the basis, it is not a V4-OPS-34 review.
  - Separate an additional person review from the fallback, so that `fallback_reason` is required only when a Claude fallback replaces Codex.

### EXP-R-H — MINOR — EXP-R3 checks only `pass` (§3.2; EXP-VC-11)

- **Evidence.** §3.2 says "Only a `candidate` record can stand for a scenario (V4-EXM-nn) or a VER criterion". The prototype flags only `outcome == "pass"`. Probe P2: a `definition_check` record with `scenario: V4-EXM-20` and `outcome: fail` passes both the schema and the rules.
- **Repair.** Apply EXP-R3 to every outcome other than `not-run`, or forbid `case.scenario` on non-candidate bases unless a marker makes clear the record does not stand for the scenario.

### EXP-R-I — MINOR — HELD and READY wording for packaged-smoke cases (§6.1; §10 M2; IN-5)

- **Evidence.**
  - §6.1 gives "SCC-003" as an example of HELD, "READY when released".
  - §10 M2 says "Native packaged smoke becomes READY" once the package arrives.
  - DAG-004 `HANDOFF_STATE.md` §3 says held candidate edges "drive no blocker queue, wave, schedule, dispatch readiness or readiness claim, and holding one makes no work ready".
  - The SCC-CASE-003 Datasheet calls the milestones "contribution milestones, not newly imposed gates".
- **What the milestones get right.** I checked these against the datasheet's (a)–(c) and R1: M1–M3 keep both held arcs held (no register or graph change), impose no finish-before-start order ("M1 does not wait for M2 …") and keep the two witnesses separate.
- **Consequence.** The §6.1 example implies that the cases wait for the SCC to be resolved, while §10 implies that they wait only for the package.
- **Repair.** Say that SCC-003's held arcs place no case in HELD, and that packaged-smoke cases are AWAITING INPUT for the actual package (IN-5).

### EXP-R-J — MINOR — two pins are stale because files changed after freeze (header)

- **Evidence.**
  - AAC is pinned at `062ce28c…`. That equals the `HEAD` bytes (`git show HEAD:… | shasum`), but the working file is now `eca9a079…`. `git diff` shows that O-A added two lines: the pass-4 header bullet and the A16 row. NA-3 and VC-AAC-03 are unchanged.
  - R23 is pinned at `eaadee6e…` and is now `e4be2c2a…`, because R23-17 was added.
  - The other 17 of the 19 distinct pins match the files they name (script over the project tree).
- **Repair.** Re-pin both, and cite R23-17.

### EXP-R-K — MINOR — native routes do not record the macOS WebKit (WKWebView) identity (§8; result schema `route`; REQ-007; AC-008)

- **Evidence.** REQ-007 asks for coverage of WebKit and Chromium "including the macOS WebKit environment", and AC-008 asks for "macOS WebKit and in-scope native identities distinguished". EXP §8 rightly says the browser runner's WebKit "is not the macOS WKWebView … the WKWebView is covered by the native routes". However, the schema requires `engine` and `platform` only for `interface_*` routes, so a native record carries no WebKit identity.
- **Repair.** Require or allow the WKWebView/WebKit identity (OS and WebKit version) on `native_development` and `native_packaged` records.

### EXP-R-L — NOTE — the AAC NA-3 citation creates no unrecorded reliance (§8 N-1 reason 1; §14 O-4)

N-1 stands on REQ-003, which forbids manufacturing acts, and on V4-EXM-10/11/12, which contain acts only the person performs. AAC NA-3, "Capture follows only the person's confirmation in a surface the interface's scripts cannot operate" (`APP_ACT_CONTROL.md` line 284), and VC-AAC-03 only corroborate it. If NA-3 changed, the N-1 choice would still follow from REQ-003. No register row is implied. I did not recompute O-B's reach statement (that DEL-01-04 and DEL-04-03 reach DEL-09-01).

### EXP-R-M — NOTE — R23-1 and R23-3 are respected

- **R23-1.** HOSTING is not edited. The EXP outcome and fixture labels equal HOSTING §9.3 and §9.2, which EXP-R9 checks by reading `HOSTING_BOUNDARY.md` itself (regex on §9.2 and §9.3; HOSTING `ce235650…`, current). HOSTING §9.3 states the labels without meanings, so EXP maps to them and does not govern them. W14 and XT keep their own enums, mapped one to one (EXP-R9).
- **R23-3.** Examples exist at both pins (prototype check). The only HOSTING facts used are definitions, not Codex behaviour.

## What was checked and how

- **Hashes.** All five expected unit hashes and the nine example sets match.
- **Prototype rerun, not rebuilt.** I ran `PYTHONDONTWRITEBYTECODE=1 python3 check_exp.py` in `prototype/`: **TOTAL 52, FAIL 0**, as O-B reported.
- **Missing assertions.** I added these only as scratch probes. `$TMPDIR/rv/probe_exp.py` imports the prototype's own functions and validators, and nothing was written in the unit:
  - P1, packaged route without a package record → EXP-R-C;
  - P2, a non-candidate `fail` standing for a scenario → EXP-R-H;
  - P3, aggregation with an optional `not-run` part → EXP-R-A;
  - P4, an honest `not_separate` review → EXP-R-F;
  - P5, `used: other` → EXP-R-G;
  - P6, a record-level `needs_native` is refused by the schema, which is correct;
  - P7, EXP-R4 is detected on a browser-route `needs_native` pass, which is correct.

  These are the assertions to add to `check_exp.py` at repair: P1, P2, P4 and P5 as rule or invalid examples, and P3 once the ruling is made.
- **Pins.** I matched all 19 distinct 64-hex values in `EXAMINATION_PROTOCOL.md` against `shasum -a 256` of the project's `.md`, `.json` and `.csv` files. 17 match; the 2 stale ones are explained in EXP-R-J.
- **ScopeOfWork.** I read DEL-09-01 `ScopeOfWork.md` (at the pinned `8e536694…`, confirmed) and mapped OUT-001…004, REQ-001…008, AC-001…009 and VER-001…009 to the EXP sections and VC-01…12. Coverage is complete, apart from EXP-R-B (AC-003 meanings) and EXP-R-K (REQ-007/AC-008 macOS WebKit).
- **Probes requested by the coordinator.**
  - R23-1: EXP-R-M.
  - `blocked` and `not-run` against CA W-R5 and XT SR-4: EXP-R-B. I read CA §8.4 W-R1…W-R7, and XT §3.4 X-R1…X-R5 and §3.5 SR-4. Mid-case they agree; at case start they diverge.
  - AAC NA-3: EXP-R-L.
  - R23-12: EXP-R-F and EXP-R-G, against `docs/OPERATING_METHOD.md` V4-OPS-34 and ScopeOfWork CLM-004 and REQ-006.
  - R23-17: EXP-R-D.
  - SCC-003: EXP-R-I, against `_DAG/cases/SCC-CASE-003/Case_Datasheet.md` (R1; milestones (a)–(c)) and `_DAG/DAG-004/HANDOFF_STATE.md` §3.
- **HOSTING §9.1–§9.3** were read directly to confirm the label lists and that HOSTING gives no meanings.

## Not checked

- O-B's DAG-004 reach computations. The reach script was not rerun.
- `w14-result-record.schema.json` beyond its outcome enum, which the prototype reads.
- The change-impact schema beyond what the prototype exercises.
- O-B's DEL-01-06 K-4 facts in `O-B.md`, which belong to a later unit.
- `SURVEY/S1-B.md` beyond its hash.

## Repair confirmation (2026-10-03)

- **Repaired unit:** DEL-09-01 EXP-v0.2.
  - `EXAMINATION_PROTOCOL.md` `fc5b8230ec2ab81a9307bd58a573752194a859afbc28eda6bce1a12ee332a20d`.
  - All 14 files match the hashes O-B lists under "U1 repair" in `OWNERS/O-B.md` (`shasum -a 256`).
- **Basis.** Rulings R23-17, R23-19, R23-20 and R23-21, cited by ID.
- **Checks rerun.**
  - `check_exp.py` gives **TOTAL 77, FAIL 0**.
  - My original probes (`probe_exp.py`) rerun unchanged:
    - P1: refused by the schema (it is now EXP-INV-09);
    - P2: refused, and EXP-R3 also fires;
    - P5: refused;
    - P6: refused;
    - P7: refused, and EXP-R4 still fires.
- **Adapted probes.** I accept O-B's reading of P3 and P4:
  - Under R23-19 item 3, an applicable part that is not run must keep the case from passing.
  - P4 left `reported_as_independent: true`.

  The adapted probes are in `$TMPDIR/rv/probe_exp2.py`. They reuse the prototype's functions and write nothing in the unit:
  - **P3a:** EXP-EX-08 (four parts pass; P22-G under `parts_not_applicable` with `declared_in`) is valid, with no rule violation → `pass`.
  - **P3b:** a declaration without a `sha256:` digest is refused by the schema.
  - **P3c:** a declared not-applicable part that is also run → EXP-R1 fires.
  - **P3d:** an applicable `not-run` part with `outcome: pass` → EXP-R1 fires.
  - **P4a:** an honest `not_separate` review with `reported_as_independent: false` is valid, with no violation.
  - **P4b:** the same review with `true` → EXP-R6 fires.
  - **P8:** `blocked` without `blocked_by` is refused.
- **Pins.**
  - 17 of the 19 distinct 64-hex values match current files.
  - `dc6b6a0c…` is the superseded v0.1 hash, cited as history.
  - `062ce28c…` is AAC-v0.2, the version relied on. It equals the `HEAD` bytes. `git diff HEAD` shows that AAC-v0.3 adds only the header, the A16 row and AI-9. NA-3 (line 287) and VC-AAC-03 are unchanged, so the pin conforms to R23-21 item 3.

### Verdict: **CONFIRMED — READY** (no BLOCKING or MAJOR open)

| Finding | Status | Confirmed against |
|---|---|---|
| EXP-R-A MAJOR | **Repaired** (R23-19) | §3.1 and the `parts_not_applicable` schema element (part, reason, `declared_in` with the case-definition digest). EXP-R1 aggregates applicable parts only. Probes P3a–P3d behave as R23-19 items 1–3 require. "Before the run" cannot be checked mechanically; the case-definition digest lets a reviewer check it, which is adequate |
| EXP-R-B MAJOR | **Repaired** (R23-20) | §3.1 meanings now carry the INTEGRATION label, and the SETTLED label is gone. §6.1 adds PLANNED and "every planned case gets a record". F-1a and F-1b added. `blocked_by` is required (P8). Before a candidate is named there is no subject, so the journey lists the case instead (F-1). This is consistent with R23-20 item 1 ("planned for the candidate") |
| EXP-R-C MAJOR | **Repaired** | A schema conditional applies to `native_packaged` results other than `not-run` (EXP-R2). P1 is EXP-INV-09 and is refused. EXP-EX-04 is now `not-run` with the package as its missing input, which matches R23-20 |
| EXP-R-D MAJOR | **Repaired** (R23-17) | §8.3 EXP-DC-RUNNER (DC-R1…R5) and EXP-DC-N2 (DC-N1…N5) each have content and an admitting record, which later results cite (EXP-R2, schema). U-EXP-3 is decided (§8.2 form layout, §8.4 path convention, no service). U-EXP-2 and U-EXP-4 are restated or closed per R23-17. U-EXP-1 is restated per R23-17 item 2; see the note below |
| EXP-R-E MINOR | **Repaired** | §3.5 has one rule table EXP-R1…R9 with what enforces each. EXP-R2 is defined. The prototype checks that the table lists each rule once |
| EXP-R-F MINOR | **Repaired** | `reported_as_independent` is required. EXP-R6 fires only when it is true and separation fails (P4a, P4b). F-6 is reworded |
| EXP-R-G MINOR | **Repaired** | `other` is removed (P5 refused). `review_kind` distinguishes `v4_ops_34` (preference required) from `additional_person`, which never replaces the V4-OPS-34 review (EXP-RX-04 valid) |
| EXP-R-H MINOR | **Repaired** | The schema forbids `case.scenario` on `rehearsal` and `definition_check` records. The prototype's EXP-R3 covers every outcome except `not-run` (P2 refused) |
| EXP-R-I MINOR | **Repaired** | §6.1: held arcs place no case in HELD (DAG-004 reading rule 3). Packaged smoke is AWAITING INPUT for the package. §10 M2 is reworded |
| EXP-R-J MINOR | **Repaired** | Rulings are cited by ID. The AAC pin is kept as the relied-on version, with the v0.3 diff checked (above) |
| EXP-R-K MINOR | **Repaired** | Native routes require `webview` (WKWebView, WebKit version and OS version). §8.1 gives the reason. Covered by EXP-INV-13 |
| EXP-R-L NOTE | No change needed | — |
| EXP-R-M NOTE | No change needed | — |

**Note for O-B's next touch.** U-EXP-1 (§13) says "HELP_HUMAN names both when VC returns". R23-22, appended after this repair, now settles both points:
- the qualification pin is the newest version to have passed a version-advance check when a candidate is built;
- 0.160.0 is recorded as checked and design-compatible, while 0.158.0 stays the definition pin.

U-EXP-1 can cite R23-22 and close. This is not a finding against the repair.
