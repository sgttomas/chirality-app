# RV3-EB1 — review of DEL-10-01 EB-v0.1 (unit EB-1, owner O-E)

- **Reviewer:** RV3, a Type 2 TASK running as Claude Opus 5.5 (`claude-opus-5-5`). It was dispatched within the HELP_HUMAN session and did not author the unit; same-session review is accepted for design units (OWNER_DECISIONS_2.md). The review was written 2026-10-04. Method: `coordinated-knowledge-work` §3, which asks whether the account is correct. Usability is the isolated reader's question, not this review's.
- **Unit**, under `E/PKG-10_…/1_Working/DEL-10-01_…/Design/`. All hashes were checked with `shasum -a 256` and match `OWNERS/O-E.md`:
  - `EXECUTION_BASIS.md` `e24101b2…3baa`;
  - `eb1/IS-EB1-1.input-set.json` `907709e5…91e5`;
  - `eb1/EB1_READER_BRIEF.md` `3a9d2529…491e5`;
  - `eb1/EB1_QUESTION_KEY.md` `0ef83844…2f23`;
  - `prototype/make_input_set.py` `165dd43c…9165`;
  - `prototype/eb1_check.py` `2845775a…9165`.
- **Basis read:**
  - DEL-10-01 `ScopeOfWork.md` (`7a89fc38…9b47`, which matches the account);
  - every primary record behind B-1…B-16;
  - CURRENT_EXECUTION_BASIS;
  - `Open_Issues.csv` and `External_Dependencies.csv`;
  - LOOP_INIT and OPERATING_METHOD (`98836b52…`);
  - Field Book §1, Consolidated §1.7 and User Manual §5/§14;
  - the D-GOV-52 tranche manifest and notice;
  - R23-1…R23-36 and `BASIS_BINDING.md`, received mid-review with the coordinator's note;
  - the tranche-1 review form (`RV2-PKG-U2.md`).
- **Not read:** anything under `RUN/RR-EB1/` or the session's rr-eb1 folder. One filename, `RR-EB1/SUPPLIED.sha256`, appeared in a hash grep; its content was not opened.

## Verdict: **REPAIR**

The verdict rests on 1 BLOCKING and 4 MAJOR findings. There are also 9 MINOR findings and 5 NOTEs.

Several things stand and can be kept:
- the pins (§3.1 and §3.2), all 14 of which I re-derived independently;
- the input-set manifest, which regenerates byte for byte;
- the actor, recorder and subject of B-1, B-5, B-7, B-8…B-11, B-14, B-15 and B-16;
- the §7 joins;
- the §4 handoff;
- most of §6.

The defects concentrate in three places:
- one owner act the account and the key both missed (the owner's 2026-10-04 direction on review independence);
- the actor of "selection" (§3.1);
- the re-pin rule, now superseded by R23-35.

## Findings

### EB1-R1 — BLOCKING — key K7.d, a critical item, contradicts a primary record in the input set (`EB1_QUESTION_KEY.md` Q7)

- **Claim.** K7.d reads: "Not the owner's: HELP_HUMAN's ruling R23-31 item 5, recorded as an observation for the 60% discussion, 'not as a departure'". Its primary record is `R23_RESOLUTIONS.md`.
- **Evidence.** `RUN/OWNER_DECISIONS_2.md`, "Review independence for design units (owner, exact, 2026-10-04)":
  - The owner's words: "Same-session review is acceptable. It's a practical concession to making the logistics easier."
  - The effect: "R23-31.5 is confirmed as the owner's practice for design units … The 60% observation in R23-31.5 is settled by this direction and is not raised again."

  This section is in the input set. The manifest's sha256 for `OWNER_DECISIONS_2.md`, `3a861c52…42d7`, equals the bytes that contain it (`grep -n "Same-session"` gives line 51). The file's mtime (10:29) precedes the account's (10:30) and the key's (10:33).
- **Consequence.** Q7(d) asks whether treating Claude-reviews-Claude as sufficient for design units was the owner's act. The records say:
  - it was first ruled by HELP_HUMAN (R23-31.5);
  - the owner then confirmed it.

  A reader who reads the records correctly would be scored CONTRADICTED or MISS on a critical item. A reader who follows the index would be scored MATCH while wrong. The EB-1 pass/fail result cannot be relied on until the key is corrected.
- **Repair.**
  - K7.d expects: ruling R23-31.5 by HELP_HUMAN, confirmed by the owner on 2026-10-04 ("Same-session review is acceptable"; `OWNER_DECISIONS_2.md`), and not a departure. An answer naming only the owner's confirmation, or only R23-31.5, is PARTIAL.
  - The reader has already returned (R23-35 cites its finding). Record the correction in the key as a pre-scoring correction under this finding, citing a record that predates the run, before the reader's return is compared.

### EB1-R2 — MAJOR — the account omits the same owner act and states the opposite (§2, §2.1 row 4, §6 "Independent review" row)

- **Claim.**
  - §2.1 row 4, "Not to be read as": "An owner-accepted departure. R23-31.5 records it as an observation for the 60% discussion".
  - §6 records it as "**Not a departure** (R23-31.5); recorded as an observation for the 60% discussion".
  - §2 lists 16 owner acts, and this one is not among them.
- **Evidence.** As in EB1-R1. The owner's direction settles the observation: it "is not raised again".
- **Consequence.** The account gets wrong a fact that REQ-006/AC-006 exist to keep straight: whose act it was and what standing it has. O-E's claim 3 ("§2.1 separates acts that are not the owner's: … the review-independence observation") is wrong for this item. The conclusion "no departure awaits the owner" still holds, but now for a different reason.
- **Repair.**
  - Add B-17 (2026-10-04, owner, "Same-session review is acceptable. …", HELP_HUMAN, `OWNER_DECISIONS_2.md`). Its subject is R23-31.5's practice for design units. What it did not decide: V4-OPS-34 for product candidates (EXP §7, R23-12).
  - Rewrite the §2.1 and §6 rows to say "HELP_HUMAN's ruling, confirmed by the owner (B-17)".

### EB1-R3 — MAJOR — §3.1 "States." attributes the selection of the manuals to WORKING_ITEMS; the record says the human selected them and WORKING_ITEMS recorded them (§3.1; REQ-002, REQ-006)

- **Claim.** `EXECUTION_BASIS.md` l.83: "CURRENT_EXECUTION_BASIS records these as selected by WORKING_ITEMS, acting as the owning project-definition manager, 'for this App-v4 definition run/current execution basis only'."
- **Evidence.** `E/_Coordination/CURRENT_EXECUTION_BASIS.md` l.7:
  > The human selected the three manuals as core practice in the accepted basis … WORKING_ITEMS, as the **Owning project-definition manager** named by OI-017, records the following existing edition choices and exact identities … this record makes their selection explicit and recoverable rather than treating a file read as adoption.

  The quoted scope words come from l.9, "HELP_HUMAN confirmed the intended scope in the active coordination: this App-v4 definition run/current execution basis only". They are HELP_HUMAN's confirmation, not WORKING_ITEMS' words.

  The account's own key K1.2 (critical) gives the correct reading. `BASIS_BINDING.md` l.32, written later, agrees with the key: "The owner selected the manuals as core practice in the accepted basis. WORKING_ITEMS recorded the editions".
- **Consequence.** On a critical item, a "States." line in the index disagrees with both the record and the key. A reader who leans on the index will misattribute the selection actor, which is the failure CLM-004/REQ-006 forbid.
- **Repair.** "The human selected the three manuals as core practice (accepted basis). WORKING_ITEMS, as OI-017's owning project-definition manager, recorded the existing edition choices and identities. HELP_HUMAN confirmed the scope: this definition run / current basis only."

### EB1-R4 — MAJOR — key K8.2, a critical item, rests on the account's own inference, and its CONTRADICTED rule penalises answers the records support (`EB1_QUESTION_KEY.md` Q8)

- **Claim.** K8.2 expects:
  - "No departure now awaits the owner. OI-019 and OI-020 are open but not triggered. Naming a specific pending owner departure is CONTRADICTED";
  - primary record "Index §6; `Open_Issues.csv`".
- **Evidence.**
  - No primary record states that no departure awaits the owner, or that OI-019/OI-020 are "not triggered". `Open_Issues.csv` gives only `OPEN`, the owner, and points of need ("When consequential gap affects selected work"; "Before revising manuals from feedback"). Whether either point has arrived is O-E's inference.
  - The input set's R23 file carries wording deliberately left for the owner at the next amendment: R23-7, R23-11 ("the wording is listed for the next amendment, which reaches the owner at its own checkpoints"), R23-18.4 and R23-34.8.
- **Consequence.**
  - The key requires MATCH, which means a primary record cited, on an item only the index states. That is the dependence the brief asked me to rule out.
  - A careful reader who answers `unknown` would be scored MISS.
  - A reader who names carried amendment wording as awaiting the owner would be scored CONTRADICTED, although the records support that answer.
- **Repair.**
  - Make K8.2 non-critical, or restate it from records. The records show:
    - OI-019 and OI-020 OPEN with their owner and point of need;
    - no record presents a manual departure to the owner;
    - ScopeOfWork wording carried to the next amendment reaches the owner at that amendment's checkpoints (R23-11).
  - Score `unknown` or a labelled inference "none" as MATCH.
  - Keep CONTRADICTED only for asserting that an owner decision on a departure has been requested or made when none is recorded.

### EB1-R5 — MAJOR — §3.3 rests on R23-31.3, which R23-35 supersedes. The account says "no new pin record is needed"; no later undertaking cites the pins, and CURRENT_EXECUTION_BASIS requires a binding (§3.3; header "Rulings"; key K1.3; P-E1)

- **Claim.**
  - The header cites "R23-31 (items 1, 2, 3, 5)".
  - §3.3 item 1: "A later undertaking relies on the pins in §3.1 while their bytes are unchanged. Its work graph or briefs cite them; no new pin record is needed."
  - Key K1.3: "Later undertakings rely on the same pins while the bytes are unchanged".
- **Evidence.**
  - `CURRENT_EXECUTION_BASIS.md` l.11: "a later undertaking or changed source must bind its own applicable basis before reliance".
  - R23-35 (appended after the freeze, superseding R23-31.3): "Each later undertaking writes its own short basis binding before reliance. It may bind by reference to the recorded pins after re-hashing them … O-E's account and DEL-10-01's later records follow R23-35."
  - A grep for `CURRENT_EXECUTION_BASIS` or any of the three manual hashes over every `WorkGraphs/*/WORK_GRAPH.md`, `AgentRuns/*/BRIEFS.md` and `AgentRuns/*/DISPATCH.md` matches only `APP-V4-PROJECT-DEFINITION-20260926/WORK_GRAPH.md`. No later undertaking, pass 4 included, cites the pins. They reached the manuals only through LOOP_INIT's "Operating basis" pointer.
- **Consequence.**
  - §3.3 states a rule that is now superseded, and describes a practice ("work graph or briefs cite them") that no later undertaking followed.
  - The §3.3 "Inference" reports that the bytes have not drifted. That is true (EB1 checks below), but it is not the binding CURRENT_EXECUTION_BASIS requires. AC-002's "resolved by its owning record before dependent reliance" was therefore not met for later undertakings until `BASIS_BINDING.md`.
  - K1.3 scores against the superseded reading.
- **Repair.**
  - Rewrite §3.3 to R23-35:
    - each undertaking writes a basis binding, which may be by reference after re-hashing;
    - passes 2–4 had none recorded in their own files;
    - pass 4's is `RUN/BASIS_BINDING.md`;
    - earlier undertakings' reliance was on unchanged bytes, as verified here.
  - Cite R23-35 in the header.
  - K1.3 expects "each later undertaking binds its own basis before reliance (CURRENT_EXECUTION_BASIS l.11; OI-017)". An answer that also reports the tension with R23-31.3 is MATCH. R23-35 is not in IS-EB1-1's bytes, so it cannot be required.
  - Rework P-E1 (see N1).

### EB1-R6 — MINOR — the approval record for LOOP_INIT's v4 text exists (§6 row 4; §9 row 2)

- **Claim.** "The record of who approved LOOP_INIT's text was not located".
- **Evidence.**
  - Commit `afc65e2b22` (2026-09-28 00:13 -0600) has the message "Agent: Codex HELP_HUMAN. Owner-directed manual-led loop adaptation; no development undertaking activated." It adds `docs/governance_harness/tranche_manifests/APP-V4-LOOP-ENTRY-20260928.yaml`, whose `m2_gate` reads:
    - `authorization`: "Owner copied init/ and loop/ from chirality-app-dev, reset receipts, and requested: Revise the documents accordingly for the new project folder.";
    - `authorized_by: Ryan`, `authorization_date: 2026-09-28`;
    - `integration_owner: Codex HELP_HUMAN /root`;
    - `merge_gate: owner-authorized-pr`, `self_merge: true`.
  - LOOP_INIT has not changed since that commit: it is its only commit, and the blob and working bytes are both `3790159b…`.
- **Consequence.** The answer is recoverable. The owner directed the revision; Codex HELP_HUMAN (`/root`) wrote the text and self-merged it under the owner-authorized PR gate. No record shows the owner reviewed or approved the resulting text. That is the standing to state.
- **Repair.**
  - Cite the manifest in §6 row 4.
  - Add the act to §2 (owner, 2026-09-28, recorded by the tranche manifest).
  - Close §9 row 2.

### EB1-R7 — MINOR — "What it did not decide (as the record states)" shows "—" where the records do state limits (§2 B-3, B-4, B-8, B-9, B-10, B-11)

- **Evidence.**
  - Group1 `DECISION.md`: "it does not accept unseen Packages/Deliverables, settle the carried technical choices, activate setup or establish provider readiness".
  - Group2 `DECISION.md`: "The owner accepted the presented/discussed content, not newly generated Candidate2 hashes" and "This is not Group3/final-decomposition acceptance …".
  - The SCA-V4-001/002/003 group-3 `DECISION.md` files each have an "It does not authorize:" list.
  - DAG-004 `ACCEPTANCE_RECORD.md`: "This acceptance does not: satisfy any dependency …".
- **Consequence.** Under that column heading, "—" reads as "the record states none". Group2's limit is the VER-006 positive case itself ("no unseen bytes are claimed as previously hash-approved").
- **Repair.** Give one limit per row, or define "—" as "not summarised; see the record".

### EB1-R8 — MINOR — the "Recorder" column for B-2 and B-6 does not follow §2's stated rule or O-E's claim 2

- **Claim.**
  - §2: "The 'Recorder' column names who wrote the record, as the record says; where a record does not name its writer, the row says so."
  - O-E claim 2: "(Group3, setup), the row says so".
- **Evidence.**
  - B-6: `_COORDINATION.md` says only "HELP_HUMAN relayed the exact owner answer". The row reads "HELP_HUMAN relayed" and does not say that the writer is unnamed.
  - B-2: `DIRECTION.md` names its writer: "WORKING_ITEMS authored this bounded correction". The row names only the transcriber ("Transcribed by HELP_HUMAN for WORKING_ITEMS").
- **Repair.** B-6: add "The record does not name its writer." B-2: add "written by WORKING_ITEMS".

### EB1-R9 — MINOR — the chain omits owner acts that bear on its sections, and two of its facts are imprecise (§2, §5)

- **Omitted acts in the input set:**
  - the DAG-001 record's controlling hold, "DO NOT BEGIN THE WORK TOWARDS 60%. We are handing that off.", and "finish your tasks that were interrupted.". These bear on §5: LOOP_INIT says the receiving session "needs its own human steering to start work toward 60%";
  - `OWNER_DECISIONS.md`'s "yes, download it" (2026-10-03).
- **B-12's subject** is given as "Design pass 4 and a Codex version check". The act also decided items 1–3 (OI-009 wording carried; no history rewrite; prepare the instruction-change package that became B-15).
- **DAG-002 and DAG-003 ordering.** The account says they were "accepted successors between B-9 and B-11". DAG-002 was accepted 2026-09-29 and published at `6dca88de70` (10:54 -0600), before SCA-V4-002 was accepted (`af918ee501`, 20:27 -0600). So DAG-002 falls between B-8 and B-9.
- **§5** does not say which steering act started the work toward 60%. It may lie outside the input set; if so, say that.

### EB1-R10 — MINOR — B-13 and §6 say the owner "selected" the coordination method; the record separates the owner's direction from HELP_HUMAN's selection (§2 B-13; §3.2; §6 last row; key K2.2)

- **Evidence.**
  - `OWNER_DECISIONS.md` "Coordination method", Effect: "HELP_HUMAN selected `bundled:chirality-root/coordinated-knowledge-work` (… sha256 `44049bcd…`)".
  - The account's own K2.2 scores "Owner selected" alone as PARTIAL.
  - The pass-4 `WORK_GRAPH.md` header, which K2.1 names as a primary record, says "(owner's selection …)".
- **Repair.**
  - Account: "owner directed its use; HELP_HUMAN selected and recorded the source-qualified identity with its hash".
  - Key K2.2: note the work graph's wording, and score a reader who reports the two records' wordings as MATCH.

### EB1-R11 — MINOR — critical key items require elements the question does not ask for (K3.1, K4c.2)

- **K3.1 (critical).** It includes "Recorder `/root`", but Q3 asks "by which act and whose", not who recorded it. Under "a required element is missing → PARTIAL", a correct answer would fail a critical item.
- **K4c.2 (critical).** "The tranche manifest also records it" should be marked optional.
- **Repair.** Mark both elements optional.

### EB1-R12 — MINOR — §5 says the DAG "was accepted before the gate"

- **Evidence.**
  - DAG-001 `ACCEPTANCE_RECORD.md`: "This accepts **APP-V4-30PCT-20260928-CANDIDATE-1 / DAG-001** … and completes the **30% gate**". This is one act.
  - Consolidated §1.7: "construct and examine the first project DAG before passage through the 30% gate".
- **Repair.** "Constructed and examined before the gate, and accepted in the act that completed it (B-7)."

### EB1-R13 — MINOR — B-8 and B-9 say the exact words are only in records outside the input set; the in-set records quote them

- **Evidence.** `SCA-V4-001_GROUP-3_2026-09-29/DECISION.md` "The owner's act (verbatim)" gives "Accept (Recommended)" and two further answers. `SCA-V4-002_GROUP-3_2026-09-29/DECISION.md` gives "Accept (Recommended)".
- **Repair.** Quote the words, transcribed by AK2 from the run's OWNER_DECISIONS.

### EB1-R14 — MINOR — §2.1 lists "Rulings R23-1…R23-31"

- **Evidence.** The input-set R23 bytes (`d044bb92…`) already include R23-32…R23-34, and R23-35/36 have been added since. All are HELP_HUMAN's.
- **Repair.** Write "R23 rulings (R23-1 onward)". The file is append-only (R23-21).

## Notes

- **N1 — P-E1** (proposed line for CURRENT_EXECUTION_BASIS). As written, it encodes R23-31.3, which is now superseded (EB1-R5). If HELP_HUMAN still adds a line, it should:
  1. state R23-35: each undertaking writes a basis binding before reliance, which may be by reference after re-hashing;
  2. point to the undertakings' own records (for example `AgentRuns/<run>/BASIS_BINDING.md`) as the place where later methods are recorded, not to a DRAFT Design file. R23-31.1 says outputs live in the existing records; the account can be cited as "see also";
  3. be appended, dated and attributed, leaving the existing sentences unchanged.

  On the bytes: CURRENT_EXECUTION_BASIS's sha256 `99d08009…b013` is bound only by historical manifests:
  - `_DAG/DAG-001/GATE_MANIFEST.json`;
  - `AgentRuns/APP-V4-INITIAL-SETUP-20260927/INTEGRATION_INPUTS.json`;
  - SCC-CASE-006 evidence;
  - the SCA-V4-001 closure `INPUT_MANIFEST.sha256`.

  It is not bound by DAG-004 or the current DAG-currency inputs; a grep by hash finds none. An append leaves those manifests verifiable at their commits, as R23-28.3 reasons for `_STATUS.md`. The waiting condition P-E1 named, the reader's result, has now arrived (R23-35).
- **N2 — lifecycle (R23-28, R23-31.9).**
  - Respected for the unit: all four PKG-10 `_STATUS.md` files record "WORKING_ITEMS (HELP_HUMAN coordinating under consultation 9ae4bea25bd9 …; R23-31.9)". O-E wrote none of them.
  - For HELP_HUMAN: DEL-10-02 and DEL-10-04 were moved to IN_PROGRESS while `O-E.md` says they "wait until EB-1 passes". R23-31.9 says "when design starts". This is outside the unit; it is consistent only if the survey counts as active work (SPEC §3.2).
- **N3 — VER-004 spot check.** I compared §5 with Consolidated §1.7 and User Manual §5. Apart from EB1-R12 I found no conflict: both support uneven maturity, positions that are not effort measures, and the human stage gate. This does not replace O-E's VER-004 record, which remains open, as do VER-005, 007 and 008. The account declares them open honestly.
- **N4 — checker coverage.**
  - `eb1_check.py` P-3 checks only the three manual hashes against CURRENT_EXECUTION_BASIS, not the six method hashes in its "Selected route" table. I compared those six by hand, and all are equal. Adding them is a cheap check placed at the source.
  - The unit's §3 tables now also duplicate `BASIS_BINDING.md`. Once R23-35 is adopted, consider citing that file rather than keeping a third copy of the hashes (R23-31.1).
- **N5 — the input set has moved, as expected.** At my rerun after R23-35 was appended, `eb1_check.py` gives PASS 93, FAIL 1: M-2, `R23_RESOLUTIONS.md`. The reader's evidence stays bound to IS-EB1-1 (`907709e5…`). Any rerun needs a new input-set id (R23-23.4 practice).

## Rulings

- **R23-31 framing** is respected:
  - the account presents PKG-10 as the project's own execution controls, not as App features (DOC_UPDATE);
  - it creates no parallel record set;
  - it writes no coordination record;
  - its proposals go through `O-E.md` (R23-31.2).
- **Thin file.** The account is one Design file, with the test kit in `eb1/` and `prototype/`. §3.1 copies CURRENT_EXECUTION_BASIS's hashes but declares and checks them as an index (see N4). The R23-31.3 item is superseded (EB1-R5).
- **R23-28** is respected (N2).

## What I checked and how

- **Pins.**
  - I ran `python3 prototype/eb1_check.py` against the frozen bytes: PASS 94, FAIL 0. After R23-35 the result is PASS 93, FAIL 1, as in N5.
  - Independently, I computed `shasum -a 256` for all 14 §3 paths today, `git show ffb2b6289d…:<path> | shasum` and `git show HEAD:<path>`. All 13 non-new rows are equal in all three. `coordinated-knowledge-work` is absent at `ffb2b628` (`git cat-file -e` fails), and the commit that adds it, `1b0b1c5469`, is "Add reviewed coordinated knowledge work workflow".
  - `ffb2b628` is an ancestor of HEAD.
  - The nine §3.1 hashes match CURRENT_EXECUTION_BASIS's two tables, and BASIS_BINDING's eleven hashes match mine.
- **Manifest.** `make_input_set.py --out <scratch>` reproduces `IS-EB1-1.input-set.json` byte for byte (`cmp`).
- **Basis chain.** I read each primary record in full and compared actor, words, recorder, subject, limits and custody: ACCEPTANCE/OWNER_DIRECTIONS, DIRECTION, Group1/2/3 DECISION, `_COORDINATION.md`, DAG-001 and DAG-004 ACCEPTANCE_RECORD, the three SCA group-3 DECISIONs, OWNER_DECISIONS, OWNER_DECISIONS_2, and the D-GOV-52 manifest and notice. Root `AGENTS.md` sha256 = `f96feb19…` (working tree and HEAD). The DAG-002 and DAG-003 dates come from their records and `git log`.
- **Coverage.** I compared ScopeOfWork REQ/AC/VER with §2–§9. §7's six join IDs are in their `Dependencies.csv` files; five are in `_DAG/DAG-004/DependencyEdges.csv`, and DEP-10-01-021 is in `ExcludedRows.csv`. DEL-10-04 REQ-007 supports "do not rebuild for a new session". No SCA-V4-001/002/003 `Amendment_Actions.csv` names DEL-10-01, and its ScopeOfWork has a single commit (`ddd721a90a`).
- **Key.** I checked each of the 45 items against its named primary record. Q5 matches `Open_Issues.csv` and `External_Dependencies.csv` exactly.
- **§6.** I checked V4-OPS-10…14, 22, 23 and 34 and §7 in OPERATING_METHOD, LOOP_INIT "Manual-led v4 practice" and §5, and User Manual §14's App-v3 pointers. I also traced LOOP_INIT's history (EB1-R6).
- **P-E1.** I searched every work graph and run's BRIEFS and DISPATCH for citations, and searched for CURRENT_EXECUTION_BASIS's hash across the project.

## What I did not check

- I did not run the reader's test or read its return. Usability is outside this review.
- I did not run VER-005, 007 or 008, or the boundary-owner checker. They remain O-E's open items.
- I did not run a full manual-section comparison for VER-004 (N3 is a spot check).
- I did not read records outside the input set to find which act started the work toward 60% (EB1-R9).
- I reviewed `BASIS_BINDING.md` only for its hashes and its statement of the actor. It is HELP_HUMAN's record, not part of this unit.

---

# Addendum — EB-v0.2 (refrozen after RR-EB1), 2026-10-04

- **Subject:** `EXECUTION_BASIS.md` `f9b8911f…cd61f`, `eb1/EB1_COMPARISON.md` `fa8e7aee…10d1` and `prototype/eb1_check.py` `54ec042d…b3ee`, re-hashed and matching the coordinator's note and `O-E.md` "EB-1 refrozen for RV3". The key, brief, manifest and `make_input_set.py` are unchanged.
- **Bases added:** R23-35, R23-37 and R23-38; `RUN/BASIS_BINDING.md` (`93160e1d…`); O-E's disposition plan in `O-E.md`. R23-38 rules that EB-1 passed as an early path and that the key stays frozen as the record of what was asked. This addendum covers EB-v0.2's correctness and O-E's tracing of the reader's five disagreements.

## Verdict on EB-v0.2: **READY**

No BLOCKING or MAJOR finding remains against EB-v0.2. Every BLOCKING and MAJOR finding on EB-v0.1 is resolved:
- in the account (R2, R3, R5);
- by the comparison record and R23-38.1 (R1);
- or reduced to a key note, with no effect on the score (R4).

Nine MINOR residuals and two new MINOR items remain. O-E's plan (`O-E.md` "RV3-EB1 … disposition plan") already assigns each to EB-v0.3. I checked that plan against the records, and it is correct.

## Status of the EB-v0.1 findings

| Finding | At EB-v0.2 | Evidence I checked |
|---|---|---|
| EB1-R1 BLOCKING (K7.d) | **Resolved by record.** KF-2 in `EB1_COMPARISON.md`; the adjudicated score; R23-38.1 keeps the key frozen. I accept that, after the read, the correction belongs in the comparison rather than the key, since the key is the record of what was asked. This replaces my "pre-scoring correction" | `EB1_COMPARISON.md` §1 and §4 |
| EB1-R2 MAJOR (owner act) | **Resolved.** B-18 is added and the §2.1 and §6 rows are rewritten. The quote matches `OWNER_DECISIONS_2.md` byte for byte, including the double space, and the limits match its Effect | §2 B-18, §2.1 row 4, §6 |
| EB1-R3 MAJOR (selection actor) | **Resolved.** §1 and §3.1 now say: the owner chose the manuals; WORKING_ITEMS recorded the editions; HELP_HUMAN confirmed the scope. Each quote matches CURRENT_EXECUTION_BASIS l.7 and l.9 | §1, §3.1 |
| EB1-R4 MAJOR (K8.2) | **Reduced to a key note.** The reader answered from records, so the score is unaffected. KF-5 is planned. It matters again only if the key is reused | `O-E.md` plan |
| EB1-R5 MAJOR (R23-31.3) | **Resolved.** §3.3 is rewritten to R23-35, BASIS_BINDING is indexed, and the §4 row is added. Residual: item 5 and §9 row 1 still call retroactive bindings "open", but R23-38.5 decides "no retroactive bindings" (EB2-R2) | §3.3, §4, §9 |
| EB1-R6 MINOR (LOOP_INIT) | **Not resolved; the wording got worse.** See EB2-R1 | §6 row, §9 row 2 |
| EB1-R7 MINOR ("—" limits) | Partly. B-11, B-12 and B-13 now state limits. B-3, B-4, B-8, B-9 and B-10 still show "—" against records that state limits | §2 |
| EB1-R8 MINOR (B-2, B-6 writer) | Not resolved. The §2 header now promises the writer, but B-2 and B-6 still do not give it | §2 |
| EB1-R9 MINOR (omissions, ordering) | Partly. B-12 is completed and B-13 (download) is added; both are verified against `OWNER_DECISIONS.md`. Still open: the DAG-001 hold; DAG-002's position (it was accepted before B-9, not "between B-9 and B-11"); the act that started work toward 60% | §2 note after the table, §5 |
| EB1-R10 MINOR (directed vs selected) | **Resolved** in B-14 and §6 | §2 B-14 |
| EB1-R11 MINOR (key optional elements) | A key note only (KF-6 planned); no score effect | — |
| EB1-R12 MINOR (§5 DAG timing) | Not resolved ("accepted before the gate" remains) | §5 |
| EB1-R13 MINOR (SCA verbatim) | Not resolved | §2 B-8, B-9 |
| EB1-R14 MINOR (R23 range) | Essentially resolved (R23-1…R23-36). It is already stale against R23-38, so "R23-1 onward" is better | §2.1 |

## New findings on EB-v0.2

### EB2-R1 — MINOR — O-E's D-5 tracing names a gap in the records that does not exist (`EB1_COMPARISON.md` §2 D-5; account §6 LOOP_INIT row; §9 row 2)

- **Claim.**
  - D-5: "LOOP_INIT's approver: no decision record exists … it is an author's statement, not an owner record".
  - Account §9: "LOOP_INIT's v4 text has no owner decision record; only the commit message's statement exists".
  - `O-E.md` traces this to **Records**.
- **Evidence.** `docs/governance_harness/tranche_manifests/APP-V4-LOOP-ENTRY-20260928.yaml`, added by `afc65e2b22` itself, has an `m2_gate` with:
  - `authorization`: "Owner copied init/ and loop/ from chirality-app-dev, reset receipts, and requested: Revise the documents accordingly for the new project folder.";
  - `authorized_by: Ryan`;
  - `integration_owner: Codex HELP_HUMAN /root`.

  EB-v0.2 treats the same kind of record as a record for B-16. Merged by PR #1037: `6e18505e38`, verified.
- **Consequence.**
  - A reader's correct `unknown` (the file was not in the input set) is relabelled as a gap in the records.
  - HELP_HUMAN is pointed at a non-existent gap.
  - The owner's 2026-09-28 direction is still missing from §2.
- **Repair.** As O-E's plan states for EB1-R6. Also append a dated correction to `EB1_COMPARISON.md` D-5, rather than leave its "Records" trace standing. The reader's `unknown` stays correct for the input set.

### EB2-R2 — MINOR — §3.3 item 5 and §9 row 1 predate R23-38.5

- **Evidence.** R23-38.5: "P-E3: no retroactive bindings. No agreed condition requires them (workflow §6)."
- **Repair.** State R23-38.5's observation in §3.3 item 5, and drop §9 row 1. O-E's plan covers this. Add the grep fact from EB1-R5: no later undertaking's work graph, BRIEFS or DISPATCH cites CURRENT_EXECUTION_BASIS or the manual hashes.

### Note — the checker's two modes

§8 VER-002 says "PASS at refreeze". That holds only in `--post-dispatch` mode; I reproduced PASS 119, FAIL 0. The default mode now reports PASS 115, FAIL 2: M-2 on the account and on R23, which is the drift since the read, as O-E intends. Name the mode in §8 so a later rerun is not taken for a regression.

## O-E's tracing of the five disagreements

| # | O-E's verdict and trace | RV3 |
|---|---|---|
| D-1 | The reader is right; traced to the index and to KF-2 | **Agree.** Same as EB1-R1/R2 |
| D-2 | The reader is right; traced to the index; KF-4 minor | **Agree.** Same as EB1-R3 |
| D-3 | The reader is right; traced to the index and to the records (no binding); KF-1 | **Agree.** Same as EB1-R5. My grep supports "records": only the definition-run work graph cites the pins |
| D-4 | The reader is right on all five; traced to the index and the input-set design | **Agree.** I checked the replacement citation: DAG-004 `HANDOFF_STATE.md` l.230 "A new session is not, by itself, a reason to rebuild" |
| D-5 | Seven correct `unknown`s; LOOP_INIT traced to a gap in the records | **Agree, except LOOP_INIT** (EB2-R1). The other six traces hold |

The root cause O-E names (§3, PN-1: "a hash check does not detect a stale reading") matches what I found: the input-set `OWNER_DECISIONS_2.md` bytes already held the owner's direction at freeze (EB1-R1).

## Checks for this addendum

- `shasum -a 256` on the seven unit files.
- `eb1_check.py` in both modes.
- I read EB-v0.2 in full and compared every changed row with its record:
  - B-12, B-13 and B-14 against `OWNER_DECISIONS.md`;
  - B-16's F-R16 against R23-32 item 14;
  - B-18 against `OWNER_DECISIONS_2.md`;
  - §3.1 against CURRENT_EXECUTION_BASIS;
  - §3.3 against R23-35 and BASIS_BINDING (`93160e1d…`);
  - §4 against DAG-004 `HANDOFF_STATE.md`;
  - the §6 D-12 row against OPERATING_METHOD l.19;
  - the seed carry/port row against `DIRECTION.md` "Settled treatment applied".
- The PR #1037 merge, via `git log --merges --ancestry-path`.
- Not read: `RUN/RR-EB1/*`. I passed `SUPPLIED.sha256` to O-E's checker by path only.

---

# Addendum 2 — EB-v0.3 (frozen with UC-v0.1; committed `d0e88a52f1`), 2026-10-04

- **Subject.** Re-hashed:
  - `EXECUTION_BASIS.md` `e9f7e9a6…04ee` (git blob at `d0e88a52f1` equal);
  - `eb1/EB1_COMPARISON.md` `af3f2d6c…c216`;
  - `prototype/eb1_check.py` `712c6f8f…bff`;
  - the key, brief, manifest and `make_input_set.py`, unchanged.

  The working tree is clean for DEL-10-01.
- **Method.** Word diff of EB-v0.2 (`d43665498d`) against EB-v0.3 (`d0e88a52f1`). I compared each changed row with its record.
- **Reader's result read first (P-E6).** I read `RR-EB1/account.json` (`018ebe7b…`) and `EB1_COMPARISON.md` §§1–6 before confirming.

## Verdict on EB-v0.3: **READY**

All nine residuals are **resolved**: R6, R7, R8, R9, R12, R13, R14, EB2-R1 and EB2-R2. Two NOTEs remain.

| Finding | Resolved by | Checked against |
|---|---|---|
| EB1-R6, EB2-R1 (LOOP_INIT) | B-19, the §6 row and §9, and the comparison's dated §6 | The tranche manifest `APP-V4-LOOP-ENTRY-20260928.yaml` (see below) |
| EB1-R7 (limits) | B-3, B-4, B-8, B-9 and B-10 each quote a stated limit | Group1 and Group2 `DECISION.md`; each SCA group-3 "It does not authorize" list. Quotes and paraphrases match |
| EB1-R8 (writers) | B-2 "written by WORKING_ITEMS"; B-6 "The record does not name its writer." | `DIRECTION.md` l.33; `_COORDINATION.md` |
| EB1-R9 (omissions, order) | B-7 carries the hold, quoted exactly with its double space. DAG-002 is placed between B-8 and B-9, published before SCA-V4-002's act; DAG-003 is placed after B-9. §5 names the first-increment steering | DAG-001 `ACCEPTANCE_RECORD.md` l.17–21. Git: `6dca88de70` at 10:54 and `a254be1606` at 22:22, against `851ec3d88` at 20:01 (-0600). `APP-V4-FIRST-INCREMENT-20260928/OWNER_DECISIONS.md` DECISION-1: "Which scope should this first 60% undertaking take? (Wave 1 is already running …)" → "A: App/host spine (Recommended)", recorder HELP_HUMAN |
| EB1-R12 (DAG timing) | "constructed and examined before the gate, and accepted in the act that completed it (B-7)" | M §1.7; DAG-001 record |
| EB1-R13 (SCA words) | B-8 and B-9 quote "Accept (Recommended)" | Both group-3 records |
| EB1-R14 (R23 range) | "R23 rulings (R23-1 onward; the file is append-only)" | — |
| EB2-R2 (R23-38.5) | §3.3 item 5: no retroactive bindings; my grep fact; the byte-identical observation; §9 row dropped | R23-38.5 |

**B-19 states exactly what the manifest records, and what no record shows.** The manifest `m2_gate` records:
- the authorization text, quoted exactly: "Owner copied init/ and loop/ from chirality-app-dev, reset receipts, and requested: Revise the documents accordingly for the new project folder.";
- `authorized_by: Ryan`;
- `integration_owner: Codex HELP_HUMAN /root`;
- `merge_gate: owner-authorized-pr`;
- `self_merge: true`.

B-19 reproduces each of these. It is committed in `afc65e2b22` and merged by PR #1037 (`6e18505e38`). LOOP_INIT's bytes have not changed since; its only commit is `afc65e2b22`, and its blob and working bytes are both `3790159b…`.

The negative cell, "Not stated by any record: that the owner reviewed or approved the resulting text", matches R23-42.1 and my own reading. "Listed last; it predates B-8" is correct: `afc65e2b22` is 2026-09-28 00:13 -0600, after B-7's recording at 05:57 UTC on 2026-09-28 (23:57 -0600 on 2026-09-27) and before B-8.

**Comparison §6 and KF-5…KF-7.** I checked these against the reader's actual answers, and the claim "no effect on the score" holds:
- **K8.2:** the reader answered "None is recorded as awaiting the owner … open matters, not presented departures", standing `inferred`.
- **K3.1:** the reader named the recorder `/root`.
- **K4c.2:** the reader cited the manifest's `m2_gate` and noted that the manifest does not name its own writer.
- **K2.2:** the reader gave "Directed by the owner (…); HELP_HUMAN selected the source-qualified identity and recorded it with its hash".

The D-5 correction traces the miss correctly, to the index and the input-set design. The reader's `unknown` stays correct for IS-EB1-1.

## Checks

- `eb1_check.py --post-dispatch RUN/RR-EB1/SUPPLIED.sha256`: **PASS 125, FAIL 0**, as claimed.
- Default mode now gives PASS 120, FAIL 3: M-2 on the account, on R23, and now also on the pass-4 `WORK_GRAPH.md`, which HELP_HUMAN updated for PN-8. This is all drift since the read, as intended.

## Notes

- **N-a.** §8 VER-002 says default-mode M-2 reports "the account and R23". It now also reports the work graph. Phrase it as "the input-set items changed since the read" so that later runs are not misread.
- **N-b.** B-19's recorder cell lists the manifest's fields but does not say that the manifest names no writer of its own. B-16's row does say this of the D-GOV-52 manifest. For consistency with §2's own rule, add "the manifest does not name its own writer".
