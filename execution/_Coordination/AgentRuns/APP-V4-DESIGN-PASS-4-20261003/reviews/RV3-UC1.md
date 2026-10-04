# RV3-UC1 — review of DEL-10-02 UC-v0.1 (owner O-E)

- **Reviewer:** RV3, a Type 2 TASK running as Claude Opus 5.5 (`claude-opus-5-5`). It was dispatched within the HELP_HUMAN session and did not author the unit; same-session review is the owner's accepted practice for design units (B-18). The review was written 2026-10-04. Method: `coordinated-knowledge-work` §3, which asks whether the unit is correct.
- **Unit:** `PKG-10_…/DEL-10-02_…/Design/UNDERTAKING_CONTROLS.md` `e25fbe9b…337f`, re-hashed. It is committed in `d0e88a52f1` and the working tree is clean there. It was frozen together with EB-v0.3, which is reviewed in the RV3-EB1 addendum.
- **Basis read:**
  - DEL-10-02 `ScopeOfWork.md` (`d93ec4c0…`, which matches the pin);
  - the DEL-10-02 row of `Deliverables.csv`;
  - Field Book §2 and §5 (subsections 1–4);
  - User Manual §3 and §10;
  - Consolidated §1.5 and §5.4;
  - SPEC §3.2, §5.4 and §9.8;
  - `construct-local-work-graph` §§2–4;
  - OPERATING_METHOD V4-OPS-20…34;
  - RECEIPT, DISPATCH (its capability account), `RR-EB1/DISPATCH_RECORD.md`, `E/RR-E/RESULT.md`;
  - `OWNERS/O-E.md` (both "Brief received" entries and the freeze);
  - the current pass-4 work graph;
  - R23-31…R23-44.
- **Reader's result read first (P-E6).** `RR-EB1/account.json` and `eb1/EB1_COMPARISON.md`; see the RV3-EB1 addendum.

## Verdict: **REPAIR**

There is 1 MAJOR finding, about G-1 and VER-002. There are also 3 MINOR findings and 4 NOTEs.

Several parts stand and can be kept:
- the controls map, whose five rows match the SoW's reader/use table and whose "Settled by" texts do settle their rows;
- G-2 and G-3, correctly identified;
- the capability-account form;
- the seed notes' facts and evidence;
- the stage disposition, which stays with the owner;
- VER-001, VER-003, VER-006 (with UC1-R3 and UC1-R4) and VER-008, as claimed.

## Findings

### UC1-R1 — MAJOR — the G-1 convention does not close G-1. SPEC §9.8 requires the run record to hold the launch briefs; a receiver's summary is a transcription and does not preserve "the actual supplied basis". VER-002's worked case lacks fields the convention itself requires (§3.3; §10 VER-002; REQ-002, AC-002)

- **Claim.**
  - §3.3: the receiving owner records "a faithful summary" of each unit brief in its own `OWNERS/O-x.md`, which "preserves the 'actual supplied basis' REQ-002 asks for".
  - §10 VER-002: "**Done** for both cases", the second being "O-E's G-1 record of the R23-38 brief … with its frozen return".
- **Evidence.**
  - SPEC §9.8: "Record versioned plans, work graphs …, **launch briefs**, actual instance parentage, source hashes, scopes, notices, amendments, returns … under `{EXECUTION_ROOT}/_Coordination/AgentRuns/<RunID>/` … Distinguish runtime-persisted records from an authorized agent's factual transcription of native execution. Read-only callers return records to an authorized writer."
  - REQ-002: bounded assignments identify the "actual supplied basis and context, parent and mechanism, authority/tools, exact writes, checks, expected return and recipient".
  - O-E's second G-1 record (`O-E.md` "Brief received, 2026-10-04 (G-1)") holds the sender, the EB-v0.3 content, a commit and "Next". It has no write grant, no exclusions, no escalation conditions and no expected return, which are four of §3.3's six fields.
  - The first record has the write grant and escalation conditions but no expected return.
- **Consequence.**
  - The verbatim unit briefs, including write fences, exclusions and read prohibitions such as RV3's "do not read rr-eb1", still exist only in the session. The summary loses them.
  - G-1 remains open, and AC-002's "actual parentage … and receiving ownership" is not established for unit briefs.
  - VER-002 is not done for the second case.
- **Repair.**
  - State that SPEC §9.8 settles G-1: the launch brief as sent belongs in the run record, written by its maintainer. Propose to HELP_HUMAN (P-E7) that each unit brief is appended verbatim to `BRIEFS.md`, or to a per-unit file under the run, at dispatch.
  - Keep the receiver's record as a labelled transcription and a cross-check, not as the preserved basis.
  - Re-mark VER-002's second case as partial until a verbatim brief exists, or complete O-E's records to the six fields.

### UC1-R2 — MINOR — §4.2's worked instance names the wrong branch

- **Evidence.**
  - UC §4.2: "One worktree on branch `claude/dgov52-agents-md-app-v4`".
  - That branch belongs to PR 1079 (`9d82ed12ea`).
  - `git branch --show-current` gives `claude/app-v4-design-pass-4-t2`. Tranche 1 ran on `claude/app-v4-design-pass-4` (PR 1077).
  - DISPATCH's adopted copy corrects it.
- **Repair.** Correct the instance, or point to DISPATCH as the maintained copy.
- **NOTE for HELP_HUMAN: the adopted DISPATCH row upgrades the standing.**
  - UC §4.2 says write and network limits "were not observed to be host-enforced", **unknown** beyond that. DISPATCH l.94 says "they are instruction-only".
  - The records do not establish that. In RV3's own session the host-reported Bash tool runs sandboxed unless a call disables it. I report the tool description only; I did not probe it.
  - REQ-004 and U §3 ask for "unknown or untested" here, not a negative claim. Restore "not observed; unknown".

### UC1-R3 — MINOR — the note `Class` mixes how the guidance fitted with whether practice followed it (§5 Fields; §6 PN-1, PN-2, PN-7, PN-8)

- **Evidence.**
  - V4-OPS-20 / REQ-006 classify the *practice* (the selected guidance) as useful, ill-fitting or ambiguous.
  - In PN-1, PN-7 and PN-8, the cited guidance fitted and was simply not followed: F §5.4 "Preserve the actual inputs"; F §2 "Carry routine work forward within existing authority"; F §5.4 "Update the graph at meaningful returns". Yet each is classed `ill-fitting`.
  - PN-2 is the same situation (U §10 "preserve the supplied basis"; V4-OPS-11), but is classed `useful`.
  - SPEC §9.8 ("AgentRuns evidence links that graph … rather than maintaining a second current copy") makes PN-8 a lapse against an existing Root rule.
- **Consequence.** At the stage discussion, `ill-fitting` points to a manual revision (OI-020) where the evidence shows a lapse in applying guidance that fitted. The owner would be asked the wrong question.
- **Repair.** Classify the guidance, and record "practice did not apply it" in Conditions and Consequence. Alternatively add a separate field, for example `applied: yes | no | partly`. Reclass PN-1, PN-7 and PN-8 consistently with PN-2, and add SPEC §9.8 to PN-8's loci.

### UC1-R4 — MINOR — PN-1's User Manual locus is an analogy, not what the passage addresses (§6 PN-1; VER-006)

- **Evidence.**
  - U §10 reads: "A changed file on disk does not prove that a running child received amended instructions." That concerns delivering an amended brief to a running child.
  - PN-1 is an author's stale reading of bytes it had hashed.
  - The other two loci fit directly: F §5.4 "Preserve the actual inputs …", and M §5.4 "a stale summary that is treated as authority increases the cost of later correction".
- **Repair.** Drop U §10 from PN-1, or label it an analogy. VER-006's sentence "each cited passage says what the note attributes to it" then holds without qualification.

## Notes

- **N1.** §7 says "None of PN-1…PN-7 is a consequential gap". There are eight notes, so this should read PN-1…PN-8.
- **N2.** The pass-4 graph's T2 nodes are now updated (PN-8 taken; nodes T2-S…T2-D). Its title still reads "…, tranche 1". This is for HELP_HUMAN.
- **N3.** P-E4 was not taken. DISPATCH says "UC §5 holds the notes; linked from the graph". UC §5 still names `RUN/PRACTICE_NOTES.md` as the run's note file, and §11 still proposes it. The convention and the maintainer's choice should agree on where notes live.
- **N4.** The controls map's "Settled by" column checks out row by row:
  - **graph:** SPEC §9.8 (Git-tracked `WORK_GRAPH.md`), `construct-local-work-graph` §4 ("Keep one current account of the ready work, holds and next safe action", verified) and LOOP_INIT §1;
  - **brief:** F §5.3, whose six brief fields are as stated (verified), plus U §10 and SPEC §9.8;
  - **capability:** V4-OPS-30/34 and U §3 ("Never describe the host as mechanically enforcing a restriction merely because the agent followed it");
  - **Git:** V4-OPS-31;
  - **practice notes:** V4-OPS-20/21. This row is DERIVED under R23-31.4, correctly marked as gap G-3.

## What I checked and how

- **Manual loci.** I read each one against the bound editions; their hashes are unchanged (EB §3.1; BASIS_BINDING). Every quotation in PN-1…PN-8 appears verbatim, or with marked ellipsis, in:
  - F §2, §5.1, §5.3 and §5.4;
  - U §3 and §10;
  - M §1.5 and §5.4.
- **Note evidence.**
  - RECEIPT l.56–66 (the early path: R23-18 item 3 superseded by R23-24; the digest serialisation);
  - RECEIPT l.101–102 ("Later checkpoints were taken at quiet points");
  - `E/RR-E/RESULT.md` (RC-6 and RC-9 fail, traced to the checker);
  - `RR-EB1/DISPATCH_RECORD.md` ("Enforcement limit: the host does not restrict reads").
- **VER-003 negative case.** RECEIPT l.75–89 reports verdicts and "Nothing is implemented, built, signed or qualified". It does not claim acceptance from a check.
- **Stage disposition.**
  - ResponsibleParty "human at applicable stage decisions" (`Deliverables.csv`) and the REQ-007 quote were both verified.
  - §7 asks the owner for every disposition and lists the PN-4 and PN-7 dispositions for information only, so the decision stays the owner's.
  - OI-019 and OI-020 are carried with their owners and points of need.
- **VER-008.** I reran `check_boundary_owner_resolution.py` (`22ef57e0…`) on all four PKG-10 SoWs. Each gives 1 boundary requirement checked, 0 failing and 0 citing no claim, as claimed. In the semantic follow-up I found no sibling act performed.
- **VER-001.** The graph was stale as walked. Since then it has been updated (N2).

## What I did not check

- VER-004 beyond UC1-R2's note.
- VER-005 and VER-007, which are open as declared.
- DEL-10-03 and DEL-10-04's drafts, which are outside this freeze.

---

# Addendum — UC-v0.2 (refrozen with DA-v0.1 and EB-v0.4; committed `68f83d6b20`), 2026-10-04

- **Subject.** `UNDERTAKING_CONTROLS.md` `da0176cb…b533`, re-hashed. It equals its blob in `68f83d6b20`.
- **Method.** Word diff of UC-v0.1 (`d0e88a52f1`) against UC-v0.2. I checked each change against R23-46/47 and its records.

## Verdict on UC-v0.2: **READY**

All four findings and all four notes are **resolved**. UC1-R1 is settled by `BRIEFS_AS_SENT.md` (R23-46).

| Finding | Resolved by | Checked against |
|---|---|---|
| UC1-R1 MAJOR (G-1) | §3.3 is restated as SETTLED by SPEC §9.8: the launch briefs as sent are the run's record. Owners' records are labelled transcriptions and cross-checks. UC-v0.1's convention is withdrawn. VER-002's unit-brief case is re-marked **partial**, to be completed against the verbatim entries | `RUN/BRIEFS_AS_SENT.md`: 109 entries, verbatim, in send order with time, mechanism and recipient. O-E's are entries 65, 71, 80, 91 and 100, as UC says. The only `/Users/` strings are the placeholder `/Users/<name>` inside brief texts, so the redaction claim holds |
| UC1-R2 (branch; standing) | Tranche 1 `claude/app-v4-design-pass-4` (PR 1077); tranche 2 `claude/app-v4-design-pass-4-t2`. Write and network limits "not observed to be host-enforced; unknown". Host-reported Bash sandboxing is "not probed". DISPATCH is named the maintained copy | `git branch --show-current`; R23-47 |
| UC1-R3 (class mixes fit with compliance) | A new `Applied` field. PN-1, PN-7 and PN-8 are reclassed `useful; applied: no`, consistently with PN-2. Only PN-3 is about the guidance itself (`ambiguous`). SPEC §9.8's "second current copy" sentence is added to PN-8 | SPEC §9.8 text (verbatim) |
| UC1-R4 (PN-1 locus) | U §10 is dropped from PN-1. The F §5.4 quote is now complete ("Preserve the actual inputs, candidate, relevant observations, and limitations"), and the M §5.4 quote is verbatim | F §5.4, M §5.4 |
| N1–N4 | §7 reads PN-1…PN-9. §5 and §6 hold the notes in §6, by the maintainer's choice (P-E4 not taken). The graph title now reads "tranches 1 and 2", and its T2 nodes are current | `WORK_GRAPH.md` l.1 and its T2 rows |

**New: PN-9.** Its loci check out:
- SPEC §9.8: "Record … launch briefs …";
- U §10: "Record actual parentage and mechanism … Retain the actual supplied role, sources …", verbatim with ellipses;
- F §5.3, the brief fields.

Its disposition, "applied locally by R23-46", matches the record. Stage disposition stays the owner's: §7 asks only about PN-1, PN-2, PN-3, PN-5 and PN-6, and lists PN-4, PN-7, PN-8 and PN-9 for information.

**Still open, as declared:**
- VER-002's unit-brief case;
- VER-005 for UC (this addendum provides the reviewer's confirmation it waits on);
- VER-007 at the stage discussion.
