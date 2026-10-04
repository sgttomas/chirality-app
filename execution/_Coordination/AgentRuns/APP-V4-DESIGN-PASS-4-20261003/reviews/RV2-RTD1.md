# RV2-RTD1: review of DEL-08-02 RTD-v0.1 (research to design candidate)

- **Reviewer:** RV2 (Type 2 TASK), Claude Opus 5.5 (`claude-opus-5-5`). Run `APP-V4-DESIGN-PASS-4-20261003`, 2026-10-04. Method: `coordinated-knowledge-work` §3.
- **Unit:** owner O-D, `OWNERS/O-D.md` "CURRENT" → "FROZEN: DEL-08-02 RTD-v0.1", committed at `8525b7fa53` (branch `claude/app-v4-design-pass-4-t2`).
- **Hashes:** all three match.

  | File | sha256 |
  |---|---|
  | `RESEARCH_TO_DESIGN.md` | `586c4a3e…` |
  | `research.context-account.schema.json` | `af3b1c15…` |
  | `prototype/check_rtd.py` | `66b58f30…` |

  All three are tracked (`git ls-files`), and `git status --short --ignored` on PKG-08 prints nothing.
- **Basis read:**
  - DEL-08-02 ScopeOfWork (`43a76970…`, matches the pin): OUT-001…003, REQ-001…007, VER-001…005;
  - R23-34 items 4, 5, 6 and 8; R23-27;
  - ACT-POLICY §2.1 (L346–347) and F-2;
  - WD L895 (the §4.3.1 "required act kind" row);
  - S2-D §0.1 F-3;
  - CFB-v0.2 and EU-D1's evidence records.

## Verdict: **READY**

There is no BLOCKING or MAJOR finding. There is 1 MINOR and 2 NOTEs. All four points the coordinator asked about hold:

**CA-1…9 stay a PROPOSED definition with no shared row (R23-34.4).**
- §4 is headed "PROPOSED definition; R23-34 item 4" and says "**No row is added to ACT, RS, CE or GUIDE now**".
- Git shows no commit touching PKG-04, PKG-02 or DEL-03-04 between `25054b04df` and `8525b7fa53`.
- Neither RS's record schema nor DEL-02-03's checkpoint schema names a candidate-approval act.
- §9 proposes no register row. Its reach statements (rows to DEL-04-01 or DEL-04-03 would form no cycle; DEL-04-01 must never consume DEL-08-02) agree with S2-D F-3's table.

**No checkpoint is declared (WD §4.3.1).**
- §5's Checkpoints row reads "**None declarable now**".
- WD L895 says design-candidate approval "is a separate later-increment act and cannot be required here", which RTD quotes correctly.
- ACT L346–347 says "Design-candidate approval … is a separate act in a later increment. It is **not** A6", also quoted correctly.
- CA-9 keeps Phase 1 to prose: the agent asks, the act is recorded only when performed, and no hold is enforced. This follows DECISION-4 D4-1.

**The host questions are prepared, not relayed.**
- §7 says "They are not sent, and a written question is not an agreement (OPS §6)", and §1 lists "relay to the outside session" among the things the file does not do.
- REQ-004 asks for proposed questions and received answers with their standing. None has been received, and §12 lists the answers as open with the SWBPIPE owner via the person.
- I found no relay record carrying HQ-1…6. The run's other "HQ-" hits are LHQ identifiers.

**DEL-08-02 consumes DEL-08-01's records as frozen.**
- `check_rtd.py` reads EU-D1's committed `evidence/records/DR-DM-1.json` and `DR-DM-2.json` and checks RCA-1's evidence uses against DM-1's standings (C-0, C-1):
  - r1, admitted but stale → `limited`;
  - r2, located → `located_only`.
- RC-4's use rule follows CFB CS-R1 for Domains (reliable tier `admitted`).
- DRC is cited and nothing in it is redefined. See RTD1-R1 on how these inputs are pinned.

**Substance.**
- The method M-1…M-8 traces question, query, classed evidence, inferences and gaps, candidate with host identity, A8 request, the person's decision, and the separate acts M-8 (REQ-001, REQ-005, REQ-007).
- RC-1…RC-6 give honest account standings (`supported` / `limited` / `held`). `held` forbids a candidate, which the schema enforces.
- CA-2 binds both the candidate's host identity and the account's identity.
- CA-6 lapses on a change to either.
- CA-4 and RD-5 refuse silence, timeout, agent statements, tool success and host receipts as decisions.
- CA-7 keeps A2, A4, A5, A6 and A7 separate, and neither prerequisite nor consequence.
- §8's V4-EXM-32 design declares ST-D1…ST-D6 under R23-27. It keeps parts `not-run` until inputs exist, and does not require a favourable decision (REQ-006).
- §6 records owners and points of need without choosing a provider. PEC plays no part.

## Findings

### RTD1-R1 — MINOR: suppliers are pinned by reference to O-D's notes, and the check reads them without hash checks

**Evidence.**
- The header says DRC-v0.1 and CFB-v0.2 are read "at the hashes in `OWNERS/O-D.md`". That is a mutable owner note, not a pin in the file.
- `check_rtd.py` reads `RUN/D/evidence/records/DR-DM-1.json` and `DR-DM-2.json`, and DEL-07-02's standing schema, by path, with no sha256 check.
- Since `25054b04df`, "CFB-v0.2" names two byte states (`cf805bb8…` and `457a9d20…`; EUD1-R16).

**Consequence.**
- Every input is O-D's own, so R23-44's cross-owner vendoring does not strictly apply.
- But RTD's evidence (18/18) would follow any rebuild of EU-D1's evidence silently, and the label alone does not name the bytes relied on (R23-21).

**Repair.**
- Pin DRC, CFB, the standing schema and DR-DM-1/2 by sha256 in RTD's header.
- Have `check_rtd.py` verify those hashes before use.

### RTD1-R2 — NOTE: when CA-4's decline gets its shared row, it should follow ACT §2.3's event form

CA-4's "decision pair: approve or decline" is sound as a requirement. When the shared rows are added, the decline should be recorded as ACT §2.3's act-declined event for this kind, not as a second act kind. A16 and AAC follow the same pattern. This is for the act owners at that point; no change is needed now.

### RTD1-R3 — NOTE: VER-001's rehearsal is not the verification

`check_rtd.py`'s RCA-1, RCA-2 and RCA-3 are invented accounts over EU-D1's constructed Domains cases. ScopeOfWork VER-001 says "do not substitute a test fixture for an admitted source contract". RTD §11 labels the rehearsal as such, and VER-003 and VER-004 wait for real inputs. A future dossier should carry the same wording.

## What I checked and how

- **Rerun, not rebuilt:** `python3 -B prototype/check_rtd.py` gave **18/18**:
  - C-0…C-2;
  - RCA-1/2/3 schema-valid, keeping their rules and standings;
  - N-1…N-6 refused.

  No `__pycache__` was left behind.
- **Quotations:** I checked ACT L346–347 and WD L895 against RTD §0 and §5 by grep.
- **No shared row:**
  - `git log 25054b04df..8525b7fa53` shows no commit on PKG-04, PKG-02 or DEL-03-04;
  - grep of RS's and DEL-02-03's schemas finds no candidate-approval kind.
- **ScopeOfWork coverage:**

  | Obligation | Where RTD covers it |
  |---|---|
  | OUT-001 | §2, §3, §6 |
  | OUT-002 | §4, §7, §9 |
  | OUT-003 | §8 |
  | REQ-001 | M-1…M-8, RC-1…RC-6 |
  | REQ-002 | RC-2, RC-6, RD-2…RD-4 |
  | REQ-003 | §6 |
  | REQ-004 | §7 |
  | REQ-005 | CA-1…CA-7, RD-5, RD-6 |
  | REQ-006 | §8 |
  | REQ-007 | §1 |
  | VER-001…005 | §11 |

- **Not done:**
  - I did not run probes against the schema beyond `check_rtd.py`'s negatives.
  - I did not read DEL-08-02's `Dependencies.csv` rows beyond §9's arcs.

## Repair confirmation: RTD-v0.2 (commit `8f5c41348a`; 2026-10-04)

**Reviewer:** RV2, Claude Opus 5.5 (`claude-opus-5-5`).

### Verdict: **READY.** RTD1-R1 is confirmed

**The supplier table is pinned by sha256.** Every pin equals the current file:

| Supplier | sha256 (prefix) |
|---|---|
| ACT-POLICY-v0.11 | `597f13bd…` |
| RS-v0.10 | `2e7afb1b…` |
| WD-v0.9 | `262c9e54…` |
| DRC | `7bfa7fc4…` |
| CFB | `69c1f10e…` |
| Standing schema | `bf4cef4d…` |
| DR-DM-1 | `075f0aad…` |
| DR-DM-2 | `277def89…` |

- The quoted text is still present in ACT v0.11: "It is **not** A6" (L347) and F-2 (L1952).

**Check before use.**
- `check_rtd.py` (`e2231509…`) checks the five pins it reads (P-0) before anything else, and gives **19/19**.
- I confirmed the refusal myself on a clean `git archive 8f5c41348a` extract. Appending one byte to DR-DM-1 gave `FAIL P-0 supplier pins hold … DR-DM-1.json: 80d9d885f7a3… != pinned 075f0aadb9de…` and exit status 1. The unaltered extract gave 19/19.

**Notes carried.** RTD1-R2 and RTD1-R3 are carried as open notes in §12, with their owners.

### RTD1-R4 — NOTE: ACT, RS and WD are pinned in text only

`check_rtd.py` does not read ACT, RS or WD, so their pins are recorded but not verified at run time. That is acceptable for quoted text. Re-checking the quotes against the pins belongs at RTD's next revision.
