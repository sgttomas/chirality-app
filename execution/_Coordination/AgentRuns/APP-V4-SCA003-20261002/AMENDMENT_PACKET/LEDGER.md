# Ledger — SCA-V4-003, node P1

**Status: PROPOSED; repaired at node RP1 after review V23 (see IMPACT_ASSESSMENT "Repair (RP1)").** Nothing here is applied. This is the readable view of
[LEDGER.csv](LEDGER.csv) (216 rows, one per proposal; the CSV carries the full
target paths, sources and superseded-by links). Amendment: `SCA-V4-003` (run
`APP-V4-SCA003-20261002`). Companion files:
[IMPACT_ASSESSMENT.md](IMPACT_ASSESSMENT.md), [ARC_EFFECT.md](ARC_EFFECT.md),
[OWNER_ITEMS.md](OWNER_ITEMS.md), [BASIS_AMENDMENT.md](BASIS_AMENDMENT.md).

## How to read it

- **One row per proposal**, under the ID its source gave it. Aliases (F0 `M-n`, `ST-n`,
  `NR-n`, D-node `P-n` and `NR-n`) are in the CSV `Aliases` column, so a proposal
  restated by a later node is not counted twice. Grouped IDs (for example
  `R2-02-01-a..f`) are one row; `RowCount` gives the register rows they stand for.
- **Pass.** `2` = design pass 2 closeout (`P2RUN/closeout/C1-A/B/C.md`, read with
  `CLOSEOUT_ACCOUNT.md`); `3` = design pass 3 closeout (`P3RUN/closeout/C1-A/B.md`,
  with `F/F0_JOINS.md` §3–§4, `D/*.md` and R17…R22); `2+3` = a pass-2 item that
  pass 3 extended; `P1` = raised by this node, where an INCLUDE row needs a
  ScopeOfWork sentence no source proposes (registers follow the ScopeOfWork), or, at
  the RP1 repair, mirror rows the revised receivers sentences ground (V23 m-1).
- **Disposition** is this node's recommendation. INCLUDE = carry in SCA-V4-003;
  DEFER = keep for a later amendment or decision (named); DROP = superseded,
  duplicate, withdrawn at source or not warranted. The owner decides each one
  ([OWNER_ITEMS.md](OWNER_ITEMS.md) column "Owner item").
- `P2RUN` = `E/_Coordination/AgentRuns/APP-V4-DESIGN-PASS-2-20260930`; `P3RUN` =
  `…/APP-V4-DESIGN-PASS-3-20261001`; `E` = `projects/chirality-app-v4/execution`.

## Counts

| Kind | INCLUDE | DEFER | DROP | Total |
|---|---:|---:|---:|---:|
| ScopeOfWork | 102 | 3 | 7 | 112 |
| register | 86 | 4 | 5 | 95 |
| Open_Issues | 2 | 0 | 0 | 2 |
| basis | 0 | 3 | 3 | 6 |
| decomposition | 1 | 0 | 0 | 1 |
| **Total** | **191** | **10** | **15** | **216** |

| Pass | ScopeOfWork | register | Open_Issues | basis | decomposition | Total |
|---|---:|---:|---:|---:|---:|---:|
| 2 | 43 | 47 | 0 | 5 | 0 | 95 |
| 2+3 | 0 | 1 | 0 | 0 | 0 | 1 |
| 3 | 60 | 43 | 2 | 1 | 0 | 106 |
| P1 | 9 | 4 | 0 | 0 | 1 | 14 |

INCLUDE register items by graph class: new arc 10 items / 10 rows, mirror 35 items / 96 rows, non-topological 41 items / 50 rows (total 86 items, 156 rows).

Reconciliation with the sources:

- Pass-2 ScopeOfWork: 43 rows = the 42 distinct items of `P2RUN/closeout/CLOSEOUT_ACCOUNT.md` plus C1-B `X-1`, kept as a DROP row (duplicate of SC2-01-04-1).
- Pass-2 register: 48 items (C1-A 16, C1-B 18, C1-C 14 table rows; source row counts 33, about 46 and 14). `R-11-3` is shown once, as pass `2+3`.
- Pass-2 basis: the 5 items (C1-B B-1…B-3, C1-C B-1, B-2). The one held arc is `R2-04-03-e`.
- Pass-3 ScopeOfWork: 60 rows = R22-7-SoW plus the 56 live items of `P3RUN/closeout/CLOSEOUT_ACCOUNT.md` (C1-A 31, C1-B 25) plus 3 withdrawn or not-proposed items kept as DROP rows (SC3-02-04-3, SC3-02-02-8, SC3-01-05-11).
- Pass-3 register: 43 items = R22-7-reg and R22-7-open, plus C1-A's 23 rows (M-7 is pass-2 R2-01-04-a) and NR-01…NR-04, C1-B's 21 rows less aliases (M-5 = R-0501-4, M-6 within R-11-1, R-11-3, NR-07, NR-04, NR-4 shown once), plus NR-06 and NR-10 (withdrawn) as DROP rows. SC3-01-04-9, SC3-02-02-6, -7, -9 and SC3-02-04-8 are register statements, as both C1 records class them.
- Pass-3 Open_Issues: 2 (OI-009, OI-018). Pass-3 basis: 1 (the SIWC custody change, not proposed).
- P1: 9 grounding sentences, 1 decomposition entry (the Change Register entry) and, at RP1, 4 register rows (RP1-MX-*, 15 mirror rows; V23 m-1).
- RP1 also added design pass 3's R22-7 rows (R22-7-SoW, R22-7-reg, R22-7-open; V23 M-1): P2-B wrote block G-0403-03 for them.

## ScopeOfWork (112)

### DEL-01-01

| ID | Pass | Location | Change (summary) | Disp. | Why | Superseded by | Owner item |
|---|---|---|---|---|---|---|---|
| S-11-1 | 2 | TBD-002, first sentence (optional pointer) | Add pointer to Design/OBS_1_0.158.0.md (OBS-1, OBS-1b; observations, not qualification) | **INCLUDE** | Note for P2: OBS_2_0.158.0.md and OBS_3_0.158.0.md now also exist in DEL-01-01/Design (checked); the pointer may name all three | — | Q-11 |
| S-11-2 | 2 | CLM-005, new last sentence (or OUT-003) | DEL-01-01 supplies the harness-capability meaning of the selected pin to DEL-02-01, which owns the portable names | **INCLUDE** | Clarification, coordinated with SC2-02-01-1 | — | Q-2 |
| P1-09 | P1 | CLM receivers sentence (with S-11-2) | Name DEL-02-03, 03-03, 03-04, 09-06, 06-01, 09-01, 09-02 (unnamed today, checked) | **INCLUDE** | Wording to be drafted by P2 from the cited Design sections; route alternative is a human-declared row in _DEPENDENCIES.md | — | Q-15 |

### DEL-01-02

| ID | Pass | Location | Change (summary) | Disp. | Why | Superseded by | Owner item |
|---|---|---|---|---|---|---|---|
| SC3-01-02-1 | 3 | REQ-002, first sentence | Interruption of a turn as an explicit act; interrupt a turn, end a run, stop the Codex process are distinct; an interrupt, quit or supplier exit never ends a run | **INCLUDE** | Pairs SC3-01-04-7 | — | Q-2 |
| SC3-01-02-2 | 3 | AC-002, VER-002 | "explicit native stop" -> "explicit turn interrupt ... and from a run end"; "Invoke native stop" -> "Interrupt a turn" | **INCLUDE** | With -1 | — | Q-2 |
| SC3-01-02-3 | 3 | REQ-005; AC-006; VER-006 | Quit with live work asks first, lists, interrupts as "interrupted by quit", offers resume after relaunch; C1-A completion: same for Stop/Restart Codex | **INCLUDE** | Include with the C1-A completion clause (pairs SC3-01-04-7's C-12 clause) | — | Q-2 |
| SC3-01-02-4 | 3 | REQ-003, last sentence | No automatic decline; a request pending when Codex stops ends unanswered | **INCLUDE** | Pairs SC3-01-04-3 | — | Q-2 |
| SC3-01-02-5 | 3 | CLM-004; TBD-003 | OI-001/OI-002 "not settled" -> D2/D3 adopted for this scope, carried by DEL-04-01; open beyond it | **INCLUDE** | Enables R3-01-02-c | — | Q-2 |
| SC3-01-02-6 | 3 | TBD-001 | D4 pin 0.158.0 for definition, not qualification; OI-008 per R17-5; C1-A completion: Owner is also App implementation owner (L-7) | **INCLUDE** | One wording across the D4-pin class | — | Q-2 |
| SC3-01-02-7 | 3 | REQ-006; OUT-004 | Supplier facts reach DEL-04-03 directly from DEL-01-01; this slice keeps only references and App-observed facts | **INCLUDE** | Grounded in a ruling or owner decision | — | Q-2 |
| SC3-01-02-8 | 3 | CLM-001, interfaces sentence | Name DEL-01-03 and DEL-09-02 as consumers; C1-A completion: also DEL-02-03, DEL-03-03 and, where adopted, DEL-09-09, DEL-02-02 | **INCLUDE** | Include naming DEL-02-03, DEL-03-03 and DEL-02-02 (NR-01, NR-02, NR-04 INCLUDE); omit DEL-09-09 (NR-03 DROP) | — | Q-4 |
| SC3-01-02-9 | 3 | CLM-002 first sentence; REQ-001 | One Codex child per App-owned Codex home, each with its session and request register | **INCLUDE** | Grounded in a ruling or owner decision | — | Q-2 |
| SC3-01-02-10 | 3 | REQ-002 (optional) | Turn ended after the person's cancel answer recorded with that cause; opened-not-completed items stated as not completed | **INCLUDE** | Optional; small and grounded | — | Q-11 |
| SC3-01-02-11 | 3 | REQ-004, after first sentence (optional clarification) | The explicit unknown-request error is written by DEL-01-01's boundary; this slice records and keeps it | **INCLUDE** | Optional; removes a misreading without weakening | — | Q-11 |

### DEL-01-03

| ID | Pass | Location | Change (summary) | Disp. | Why | Superseded by | Owner item |
|---|---|---|---|---|---|---|---|
| SC3-01-03-1 | 3 | TBD-001 | D4 pin 0.158.0 for definition; qualification with the Owner, also App implementation owner (L-7), through DEL-01-01 (OI-012) | **INCLUDE** | Enables R3-01-03-f | — | Q-2 |
| SC3-01-03-2 | 3 | CLM-004; AX-002; TBD-003 | "OI-001/002 remain open" -> decided for this scope by D2/D3; rows stay OPEN for wider scope | **INCLUDE** | Enables R3-01-03-e | — | Q-2 |
| SC3-01-03-3 | 3 | REQ-005 | An act the App captures names the person as observed, "identity not verified" | **INCLUDE** | Grounded in a ruling or owner decision | — | Q-2 |
| SC3-01-03-4 | 3 | REQ-001; AC-001 | Plan revisions not kept by Codex are not copied; after relaunch or supplier restart shown not recoverable; plan items recovered from history | **INCLUDE** | Grounded in a ruling or owner decision | — | Q-2 |
| SC3-01-03-5 | 3 | REQ-003 | Task-agent delegation recorded and shown, "stated, not enforced"; no override of the person's Codex configuration | **INCLUDE** | Duplicate in substance of SC3-02-04-4 (different SoW; keep both) | — | Q-2 |
| SC3-01-03-6 | 3 | REQ-004 (or new REQ) | Experimental supplier surfaces (at 0.158.0, plan mode) labelled experimental; App fully usable without them | **INCLUDE** | Grounded in a ruling or owner decision | — | Q-2 |
| SC3-01-03-7 | 3 | REQ-005 | "Carry out this plan" is ordinary input, not a reserved act unless a checkpoint names one | **INCLUDE** | Grounded in a ruling or owner decision | — | Q-2 |
| SC3-01-03-8 | 3 | CLM-003, append | Receivers: DEL-01-04 (plan-mode element, anchors, availability), DEL-06-01 (delegation identities), DEL-09-02 and DEL-09-05 | **INCLUDE** | New at C1-A | — | Q-2 |

### DEL-01-04

| ID | Pass | Location | Change (summary) | Disp. | Why | Superseded by | Owner item |
|---|---|---|---|---|---|---|---|
| SC2-01-04-1 | 2 | New REQ with OUT, AC, VER | The App act control obligation (K1-4) | **DROP** | Superseded by SC3-01-04-1 (adds A15, DEL-02-02 consumer, interface-script exclusion; R21-3) | SC3-01-04-1 | Q-5 |
| C1-B X-1 | 2 | New obligation | Act control wording (duplicate) | **DROP** | Duplicate; P2RUN CLOSEOUT_ACCOUNT keeps the C1-A wording (43 listed, 42 distinct) | SC2-01-04-1 (then SC3-01-04-1) | — |
| SC3-01-04-1 | 3 | New REQ with OUT, AC, VER | The App act control: person-only, one act kind at a time on App content (files/outputs, A12 where set in the App, A15 on one reviewed draft or several library entries in one act from one descriptor), canonical wording, bound subject, scope, purpose, arrival, decline, direct-capture record in DEL-04-03 format, standing facility, K1-4 identity; consumers DEL-02-02, DEL-02-03, DEL-04-03, DEL-04-01 | **INCLUDE** | Supersedes SC2-01-04-1; owner-directed (K1-4, K-8); full text in P3RUN C1-A | — | Q-5 |
| SC3-01-04-2 | 3 | REQ-006 DEL-02-02 clause; CLM-004 | Registration of a reviewed revision belongs to DEL-02-02; the person's registration act (A15) is captured by this slice's act control | **INCLUDE** | Pairs SC3-02-02-4 | — | Q-2 |
| SC3-01-04-3 | 3 | REQ-001, append | Only offered answer forms; explicit decline per kind (own negative or named empty answer); no App auto-decline; supplier self-resolution shown as such | **INCLUDE** | Pairs SC3-01-02-4 | — | Q-2 |
| SC3-01-04-4 | 3 | REQ-005, append | Agent asks; standing facility raises nothing on arrival; earlier act counts with its time; several acts answer together; actor shown as observed, not verified | **INCLUDE** | Grounded in a ruling or owner decision | — | Q-2 |
| SC3-01-04-5 | 3 | OUT-002; CLM-001 | Placement of DEL-04-02's checkpoint overlay and standing facets, with DEL-02-03's display meanings | **INCLUDE** | Grounds NR-08, NR-09 | — | Q-4 |
| SC3-01-04-6 | 3 | REQ-002, append (amended at C1-A) | No model selected until the person chooses, from the selection state DEL-01-05 reports; last choice offered never applied; two refusal wordings; the Codex account DEL-01-05 reports is used for act identity | **INCLUDE** | Amended to ground NR-07; duplicate in substance of SC3-01-05-4 on the supplier side | — | Q-4 |
| SC3-01-04-7 | 3 | REQ-002, append | Interrupt, run end, Codex stop shown distinct as DEL-01-02 defines; C1-A optional clause: Stop Codex and Restart Codex, each asking first | **INCLUDE** | Include with the optional clause (pairs SC3-01-02-3 completion) | — | Q-2 |
| SC3-01-04-8 | 3 | VER-005, positive case | "...on identified content..." -> "...on identified App content through the App act control..." | **INCLUDE** | Grounded in a ruling or owner decision | — | Q-2 |
| SC3-01-04-10 | 3 | OUT-001 / REQ-001, append | This slice composes the turns it sends, incl. collaboration mode from DEL-01-03 and run-start text from DEL-02-02 | **INCLUDE** | Grounds NR-05; P2 to consider adding "the run-end line" (R20-3; NIR TC-2) as C1-A suggests | — | Q-4 |
| SC3-01-04-11 | 3 | REQ-002, append (amended at C1-A) | Roles from DEL-02-04 with default preselected and clearable, no role allowed; role fixed; another role opens a new conversation with an editable handoff summary; agent proposals and finished reports offered, never acted alone | **INCLUDE** | Grounds NR-4 (R22-1 adopted it) | — | Q-4 |
| SC3-01-04-12 | 3 | REQ-001, append | The App shows how many requests wait, also with no window open | **INCLUDE** | Grounded in a ruling or owner decision | — | Q-2 |
| SC3-01-04-13 | 3 | CLM-001, append | Receivers: DEL-09-02 (native interaction view and scoped checks) declares it upstream | **INCLUDE** | New at C1-A; grounds R3-01-04-b | — | Q-2 |
| SC3-02-02-8 | 3 | SC2-01-04-1 consumer list | Add DEL-02-02 and A15 to SC2-01-04-1 | **DROP** | Subsumed by SC3-01-04-1 | SC3-01-04-1 | — |

### DEL-01-05

| ID | Pass | Location | Change (summary) | Disp. | Why | Superseded by | Owner item |
|---|---|---|---|---|---|---|---|
| SC3-01-05-1 | 3 | TBD-001 | OI-009 decided by K-1 (shared settings, providers, MCP servers; separate sign-in custodied by Codex in an App-owned home) by the Owner, also App implementation owner (L-7); mechanism observed (OBS-2 O-6); fallback stated | **INCLUDE** | Grounded in an owner decision | — | Q-2 |
| SC3-01-05-2 | 3 | CLM-001, last sentence | "This does not choose a v4 account home." -> "The account home is chosen under TBD-001." | **INCLUDE** | Grounded in an owner decision | — | Q-2 |
| SC3-01-05-3 | 3 | TBD-003 | "unidentified supplier pin" -> 0.158.0 definition/generation pin (D4); qualification pin under OI-012, DEP-005 | **INCLUDE** | Grounded in an owner decision | — | Q-2 |
| SC3-01-05-4 | 3 | REQ-004; AC-004; VER-004 | No mode/model applied until chosen; last choice offered, never silently applied; two refusal wordings | **INCLUDE** | Supplier side of SC3-01-04-6 | — | Q-2 |
| SC3-01-05-5 | 3 | New REQ-010, AC-011, VER-011 | Turn off start-up traffic Codex settings allow; plugins follow the person's setting; show and record the rest per version, naming which is which | **INCLUDE** | Supersedes pass-2 basis item C1-B B-1 | — | Q-2 |
| SC3-01-05-6 | 3 | OUT-002 or new REQ-011 | Supply the Codex account as reported (email, or "ChatGPT account (no email reported)"; plan type not recorded) for act identity, not verified | **INCLUDE** | Grounds NR-07 on the supplier side | — | Q-2 |
| SC3-01-05-7 | 3 | REQ-002 | Where the pinned protocol keeps one account per Codex home, the API key is held by Codex in a separate App-owned home | **INCLUDE** | Now unconditional | — | Q-2 |
| SC3-01-05-10 | 3 | REQ-005 and TBD-001 "Responsible participants" | "the Owner with the App implementation owner" -> "the Owner, who is also the App implementation owner (DECISION-L L-7)" | **INCLUDE** | Grounded in an owner decision | — | Q-2 |
| SC3-01-05-12 | 3 | CLM-004 or OUT-004, end | DEL-09-02 receives the account/provider inputs and focused sign-in and concurrent-mode checks (V4-EXM-12) | **INCLUDE** | New at C1-B | — | Q-2 |
| SC3-01-05-13 | 3 | TBD-002 (optional) | Definition record is ACCESS §10 (draft); OI-010 stays open (L-6) | **INCLUDE** | Optional, new at C1-B | — | Q-11 |
| SC3-01-05-11 | 3 | SoW and OBJ-002 | Sign in with ChatGPT plan grant as an access mode | **DROP** | Not proposed: conditional on reopening SIWC (ACCESS §20 triggers T-1..T-4); owner saw no pressing need | — | Q-12 |

### DEL-02-01

| ID | Pass | Location | Change (summary) | Disp. | Why | Superseded by | Owner item |
|---|---|---|---|---|---|---|---|
| SC2-02-01-1 | 2 | CLM-002, DEL-01-01 clause | "supplies the harness capability inventory" -> inventory plus capability-group meanings and availability signals; "this contract names those requirements" | **INCLUDE** | Still accurate after pass 3 (HOSTING-v0.9 §8.4; R21-1 availability reading) | — | Q-2 |
| SC2-02-01-2 | 2 | CLM-002, end | Add receivers DEL-02-03, 03-02, 03-04, 05-01, 05-02, 09-06 and, outside this undertaking, DEL-02-02, 02-04, 08-02, 09-02, 10-03 | **INCLUDE** | Kept by P3RUN C1-B §5; same "outside this undertaking" rewording note as SC2-04-03-1 for DEL-02-02 and DEL-02-04 | — | Q-2 |

### DEL-02-02

| ID | Pass | Location | Change (summary) | Disp. | Why | Superseded by | Owner item |
|---|---|---|---|---|---|---|---|
| SC3-02-02-1 | 3 | REQ-001 | A draft is tried in an ordinary conversation, not a run; only registered revisions run | **INCLUDE** | Grounded in an owner decision | — | Q-2 |
| SC3-02-02-2 | 3 | REQ-003, last sentence | "...does not select a new overwrite policy." -> K-6 revision series; same name without origin refused; nothing overwritten | **INCLUDE** | Grounded in an owner decision | — | Q-2 |
| SC3-02-02-3 | 3 | REQ-002 | Registration by the person through DEL-01-04's act control, bound to exact reviewed content | **INCLUDE** | Grounded in an owner decision | — | Q-2 |
| SC3-02-02-4 | 3 | CLM-002; REQ-008 | Name the App act control under DEL-01-04 | **INCLUDE** | Pairs SC3-01-04-2 | — | Q-2 |
| SC3-02-02-5 | 3 | OUT-002, REQ-004, AC-004, VER-003 (optional) | "host-supplied" -> "host (origin `host`)" | **DROP** | Source recommends drop: basis V4-WF-03 itself says "host-supplied"; WR header reading 4 maps it | — | Q-11 |
| SC3-02-02-10 | 3 | REQ-001 / OUT-001 | Workflows chained within one conversation, one run at a time, sequentially or on the agent's proposal with the person confirming | **INCLUDE** | P1-03 adds the DEL-01-02 consumption at the same place | — | Q-2 |
| SC3-02-02-11 | 3 | REQ-002 (append) or REQ-004 | Shipped workflows registered by the release (origin bundled); byte-equal library entries recognized; other content registered in place by the person, several entries per act | **INCLUDE** | New at C1-B; owner decision with no SoW pointer | — | Q-2 |
| SC3-02-02-12 | 3 | CLM-003, append | Run-start text composed here per run, identity recorded and checked against Codex's history; receivers DEL-02-03, DEL-01-04, DEL-04-03; draft/registration/selection contract received by DEL-01-04, DEL-02-03, DEL-09-06 | **INCLUDE** | New at C1-B; grounds SC3-02-02-9 and mirrors R3-02-02-a..d | — | Q-4 |
| P1-03 | P1 | CLM-003 or the SC3-02-02-10 chaining sentence | Add that run ending and App-start reconciliation follow DEL-01-02's definitions (DEF-4; WR SQ-X; R19-2 (a)) | **INCLUDE** | Wording to be drafted by P2 from the cited Design sections; route alternative is a human-declared row in _DEPENDENCIES.md | — | Q-4 |

### DEL-02-03

| ID | Pass | Location | Change (summary) | Disp. | Why | Superseded by | Owner item |
|---|---|---|---|---|---|---|---|
| SC2-02-03-1 | 2 | REQ-007, VER-006 | "TBD-001 through TBD-005" -> "TBD-001 through TBD-006" | **INCLUDE** | Pointer correction | — | Q-2 |
| SC2-02-03-2 | 2 | Purpose; SOW-052 traceability row; REQ-002; AC-002; VER-002 | The slice no longer "requests" the act: the act is requested (in the current phase by the agent, K1-1); App and host loop give the checkpoint, offer the means, record arrival/request/act, never request in the agent's place | **INCLUDE** | Applies a settled owner decision; condition A1-A set is met | — | Q-2 |
| SC2-02-03-3 | 2 | CLM-002 "consumes, and does not define" list | Add DEL-04-02's grant display states for recording A12 checkpoints | **INCLUDE** | Consumer-side sentence on an existing held arc | — | Q-2 |
| SC2-02-03-4 | 2 | TBD-006, append | Earlier act counts (K1-2), joint answer (K1-3); governance-phase fresh act declared through DEL-02-01 | **INCLUDE** | Settled owner decisions | — | Q-2 |
| SC2-02-03-5 | 2 | CLM-002, DEL-01-04 clause | "App act control and person identity" -> "App act control, which records the person's identity as K1-4 sets it" | **INCLUDE** | Made true by SC3-01-04-1 (P3RUN C1-A: kept, related) | — | Q-2 |
| SC2-02-03-6 | 2 | CLM-003, end | Add receivers DEL-02-01, 03-03, 03-04, 04-02, 04-03, 05-01, 05-02, 09-06, 09-09 and, outside, DEL-02-02, 09-02, 10-03 | **INCLUDE** | Kept by P3RUN C1-B §5; "outside this undertaking" rewording note for DEL-02-02 | — | Q-2 |
| P1-01 | P1 | CLM-002 "This slice consumes, and does not define:" list | Add DEL-01-02's custody events and run-tag lookup (EXEC-v0.7 §2.7, AE-6, RE-4) as a consumed input | **INCLUDE** | Wording to be drafted by P2 from the cited Design sections; route alternative is a human-declared row in _DEPENDENCIES.md | — | Q-4 |

### DEL-02-04

| ID | Pass | Location | Change (summary) | Disp. | Why | Superseded by | Owner item |
|---|---|---|---|---|---|---|---|
| SC3-02-04-1 | 3 | Open-matter table rows OI-001/002/012/017 | Ruled (D2/D3); 0.158.0 definition pin (D4); OI-017 resolved for the definition run | **INCLUDE** | Grounded in an owner decision or ruling | — | Q-2 |
| SC3-02-04-2 | 3 | Open-matter table row OI-018 | Answered for the App by K-9 as amended by L-2 (shipped defaults, seeded editable copy, changes reach new conversations, open ones show the change); open for hosts | **INCLUDE** | Grounded in an owner decision or ruling | — | Q-2 |
| SC3-02-04-4 | 3 | REQ-003; AC-003 | K-10: "stated, not enforced"; delegation recorded and shown; no override | **INCLUDE** | Duplicate in substance of SC3-01-03-5 (keep both) | — | Q-2 |
| SC3-02-04-5 | 3 | REQ-001; AC-001 | No-role conversations (not a fifth role); preselection as data, clearable; role fixed for the conversation; another role is a new conversation | **INCLUDE** | Grounded in an owner decision or ruling | — | Q-2 |
| SC3-02-04-6 | 3 | REQ-002 or CLM-004 | Children receive product guidance and their role through native agent-role configuration where supported; a child with no role type has unknown guidance | **INCLUDE** | Grounded in an owner decision or ruling | — | Q-2 |
| SC3-02-04-7 | 3 | TBD-001 | OI-018 answered for the App (K-9 as amended by L-2); pin 0.158.0 for definition (D4) | **INCLUDE** | Grounded in an owner decision or ruling | — | Q-2 |
| SC3-02-04-9 | 3 | CLM-002, append | Receivers: DEL-03-04 (role-guidance semantics), DEL-10-03 (supply obligations) and DEL-01-04 (role list, guidance-changed signal) | **INCLUDE** | New at C1-B; bracketed clause included because R22-1 adopted NR-4 | — | Q-2 |
| SC3-02-04-3 | 3 | REQ-002 | Workflow supply composed with guidance and role (R17-8) | **DROP** | Withdrawn by D6 under R19-7 (DEL-02-02 composes run-start text; DEL-02-04 role guidance only) | R19-1, R19-7 | — |

### DEL-03-01

| ID | Pass | Location | Change (summary) | Disp. | Why | Superseded by | Owner item |
|---|---|---|---|---|---|---|---|
| S-01-1 | 2 | OUT-001, last sentence | Add: schemas may be conformance fixtures of meaning; such a fixture selects no wire field, transport, identity algorithm or placement (TBD-003; OI-014) | **INCLUDE** | Clarification, no scope change | — | Q-2 |
| S-01-2 | 2 | OUT-001 and REQ-002 element lists; new AX | Add the host-declared external-contact declaration and the destination-request entry and its non-success results; AX names SWBPIPE-INTAKE DECISION-5 and V4-HOST-02/V4-ARC-12 as amended | **INCLUDE** | Scope addition (owning decision): aligns the contract with an accepted owner decision the Design already relies on | — | Q-6 |
| S-01-3 | 2 | OUT-001 opening; REQ-001 | Name the catalog edition identity and the edition-change event; consumers resolve operation references against an identified edition | **INCLUDE** | Scope addition (owning decision); recommended because four consumers rely on it | — | Q-6 |
| S-01-4 | 2 | REQ-004; AC-004 | Receive a read whose host declares no workspace identity/generation with "basis lineage not supplied"; AC-004 admits declared absence | **DEFER** | Protected acceptance criterion; basis V4-HI-11 requires all four elements (P2RUN C1-B B-3 records a host non-conformance instead); point of need is a host join, deferred by DECISION-3 | — | Q-7 |
| S-01-5 | 2 | OUT-003 (or a custody record) | If custody stays with DEL-03-01: add the shared fixture catalogue FX-PIPE-01 and the simulated host SH-1 as an integration assignment | **INCLUDE** | Recommended with the owner's custody decision: SH-1 and FX-PIPE-01 already live in DEL-03-01 Design and pass-3 CA, XT, ADAPTER rely on them | — | Q-8 |
| P1-06 | P1 | CLM or OUT receivers sentence (as SC2-02-01-2) | Name the 11 consumers that declare DEL-03-01 upstream (9 are unnamed today, checked) | **INCLUDE** | Wording to be drafted by P2 from the cited Design sections; route alternative is a human-declared row in _DEPENDENCIES.md | — | Q-15 |

### DEL-03-02

| ID | Pass | Location | Change (summary) | Disp. | Why | Superseded by | Owner item |
|---|---|---|---|---|---|---|---|
| S-02-1 | 2 | OUT-001, last sentence | Add the conformance-fixture clarification (TBD-002; OI-014) | **INCLUDE** | Clarification | — | Q-2 |
| S-02-2 | 2 | CLM-004, last sentence (optional) | Add: consumes DEL-04-02's visible autonomy state for origin and standing at drafting | **INCLUDE** | Optional; consumer-side wording on an existing held arc, no topology change; makes the register two-sided | — | Q-11 |
| P1-07 | P1 | CLM-004 receivers sentence | Name DEL-02-03, 05-01, 05-02, 09-06, 10-03 (unnamed today, checked) | **INCLUDE** | Wording to be drafted by P2 from the cited Design sections; route alternative is a human-declared row in _DEPENDENCIES.md | — | Q-15 |

### DEL-03-03

| ID | Pass | Location | Change (summary) | Disp. | Why | Superseded by | Owner item |
|---|---|---|---|---|---|---|---|
| S-03-1 | 2 | VER-002, second sentence | Align VER-002 with AC-002 as revised (no App-originated host request; host refusal is the authoritative off) | **INCLUDE** | Alignment | — | Q-2 |
| S-03-2 | 2 | CLM-002, DEL-02-03 clause | Required-tool check moves to the current phase; hold machine and hold-support values stay governance phase | **INCLUDE** | Correction | — | Q-2 |
| S-03-3 | 2 | CLM-002 consumption list (optional) | Add DEL-04-02's visible autonomy state and, for the governance phase, DEL-02-01's declared checkpoint constraints | **INCLUDE** | Optional; existing held arcs, no topology change | — | Q-11 |
| S-03-4 | 2 | REQ-003, current-phase sentence (optional) | The agent requests the act; the App records the request where identifiable and the act only when performed; cites K1-1 | **INCLUDE** | Applies a settled decision | — | Q-11 |
| S-03-5 | 2 | CLM-002, DEL-01-01 clause | "MCP/dynamic-tool surfaces" -> "MCP, dynamic-tool and command-execution surfaces" | **INCLUDE** | Correction | — | Q-2 |
| P1-02 | P1 | CLM-002 consumption list | Add DEL-01-02's in-flight item state and relaunch fact (ADAPTER-v0.7 PI-6, XF-41) as a consumed input | **INCLUDE** | Wording to be drafted by P2 from the cited Design sections; route alternative is a human-declared row in _DEPENDENCIES.md | — | Q-4 |
| P1-08 | P1 | CLM receivers sentence | Name DEL-03-04, 04-03, 09-06 (unnamed today, checked) | **INCLUDE** | Wording to be drafted by P2 from the cited Design sections; route alternative is a human-declared row in _DEPENDENCIES.md | — | Q-15 |

### DEL-03-04

| ID | Pass | Location | Change (summary) | Disp. | Why | Superseded by | Owner item |
|---|---|---|---|---|---|---|---|
| S-04-1 | 2 | CLM-003, DEL-01-01 part | Add supplier facts on run holds, supplied guidance and model destination | **INCLUDE** | Correction | — | Q-2 |
| S-04-2 | 2 | CLM-003, DEL-09-06 part | Add DEL-09-06's connected-activity contract (step map, staging, evidence ladder) | **INCLUDE** | Correction | — | Q-2 |
| S-04-3 | 2 | Receiving map row "Autonomy", column 4 (optional) | Acts requested by the agent carrying out the workflow (K1-1) | **INCLUDE** | Applies a settled decision | — | Q-11 |

### DEL-04-01

| ID | Pass | Location | Change (summary) | Disp. | Why | Superseded by | Owner item |
|---|---|---|---|---|---|---|---|
| SC2-04-01-1 | 2 | CLM-002, last sentence | Receiver list adds `DEL-09-06` (declares DEP-09-06-030 upstream) | **INCLUDE** | Mechanical receiver sentence; grounds a mirror on an admitted arc | — | Q-2 |
| SC2-04-01-2 | 2 | AC-007, VER-007; new AX | AC-007 admits the DECISION-5 person-only destination grant "carried as an A12 subclass"; VER-007 names it | **DEFER** | Its stated condition (owner confirms the A12 mapping) has not occurred: pass 3 DECISION-K3 covered the standalone-App items only. Include only if the owner confirms the mapping at this checkpoint | — | Q-9 |
| SC2-04-01-3 | 2 | Axiology, new TBD-005 | New TBD-005: consequence dimension has no adopted vocabulary; PROPOSED draft (ACT §8.5) awaits the owner phase review; owner and point of need named | **INCLUDE** | Records an open item; decides nothing; ACT-v0.9 still lists U-02 open (checked) | — | Q-2 |
| SC2-04-01-4 | 2 | REQ-002, after first sentence (optional) | Append: registering a workflow revision is a person's act with its own actor, subject and evidence (DEL-02-02 REQ-002, AC-006) | **INCLUDE** | Kept by P3RUN C1-B §5 with an optional addition "captured through DEL-01-04's App act control (K-8)"; recommend including that addition (P2 to word) | — | Q-11 |

### DEL-04-02

| ID | Pass | Location | Change (summary) | Disp. | Why | Superseded by | Owner item |
|---|---|---|---|---|---|---|---|
| SC2-04-02-1 | 2 | CLM-002, receivers sentence | Append: `DEL-03-04`, `DEL-09-06` and `DEL-09-09` also declare it upstream | **INCLUDE** | Mechanical; note for P2: DEL-01-04 now also consumes DEL-04-02 (NR-08; AS-v0.9 §12 names it); naming it here is optional and would need a mirror row not proposed by any source | — | Q-2 |

### DEL-04-03

| ID | Pass | Location | Change (summary) | Disp. | Why | Superseded by | Owner item |
|---|---|---|---|---|---|---|---|
| SC2-04-03-1 | 2 | REQ-005, after first sentence | Name deliverable-level consumers DEL-02-01, DEL-02-03, DEL-03-01, DEL-03-04 and, "outside this undertaking", DEL-01-04, DEL-02-02, DEL-09-02, DEL-09-05, DEL-10-03 | **INCLUDE** | Kept by P3RUN C1-A and C1-B; note for P2: DEL-01-04 and DEL-02-02 now have Design files (pass 3), so the phrase "outside this undertaking" needs rewording | — | Q-2 |
| SC2-04-03-2 | 2 | CLM-004, supplier list | Add "act request (where it can be identified)" from DEL-02-03, and "the workflow identity tuple and the checkpoint disposition vocabulary from `DEL-02-01`" | **INCLUDE** | Grounds the one pass-2 new arc. P1-05 adds DEL-02-02 at the same locus (R20-10) | — | Q-4 |
| SC2-04-03-3 | 2 | REQ-003, after first sentence | Append the K1-4 App actor identity (name set in the App, OS account, Codex account when reported), marked identity not verified | **INCLUDE** | Settled owner decision. Note for P2: R18-1 C-10 fixes the Codex-account form (reported email, or "ChatGPT account (no email reported)"; plan type not recorded) | — | Q-2 |
| P1-05 | P1 | CLM-004 supplier list (with SC2-04-03-2) | Add DEL-02-02's run-start text, supply-check records and A15 relation elements (RS-v0.9; WR §7) as received inputs | **INCLUDE** | Wording to be drafted by P2 from the cited Design sections; route alternative is a human-declared row in _DEPENDENCIES.md | — | Q-4 |
| R22-7-SoW | 3 | CLM-004 supplier list | Add DEL-02-04's role-supply records (supply record, limit account, limit observations; RS-v0.9 §4 R3 (a), R5a) as a received input | **INCLUDE** | Consumer-side sentence on an existing held arc (DEL-04-03 -> DEL-02-04, SCC-002); grounds R22-7-reg. Block written by P2-B (G-0403-03), added to the ledger at RP1 (V23 M-1) | — | Q-15 |

### DEL-05-01

| ID | Pass | Location | Change (summary) | Disp. | Why | Superseded by | Owner item |
|---|---|---|---|---|---|---|---|
| S-0501-1 | 2 | TBD-003 append; optional OUT-002 edit | Name FB-CC-1 as a fixture basis, not a product selection (R12-8); OUT-002 "adopted ... model-interface basis" -> "model-interface basis (adopted, or until one is adopted a named fixture basis)" | **INCLUDE** | Include both parts: without the OUT-002 edit the fixtures cannot satisfy OUT-002 as written; no requirement relaxed | — | Q-2 |
| P1-10 | P1 | CLM-002 or REQ-005 consumption sentence | Add DEL-01-05's capability handoff (ACCESS §11 CH-1..CH-8; LOOP-v0.9 §10.3) as received information | **INCLUDE** | Wording to be drafted by P2 from the cited Design sections; route alternative is a human-declared row in _DEPENDENCIES.md | — | Q-15 |

### DEL-05-02

| ID | Pass | Location | Change (summary) | Disp. | Why | Superseded by | Owner item |
|---|---|---|---|---|---|---|---|
| S-0502-1 | 2 | CLM-002 sentences 4-5 and OUT-001 (option A); option B no change | A: name DEL-05-01's destination rules/flow and DEL-04-02's destination displays; OUT-001 adds the in-work destination prompt and receiving of the displays | **DEFER** | Its trigger (A12 mapping confirmed) has not occurred; option B stands meanwhile. Include option A only if the owner confirms the mapping now | — | Q-9 |

### DEL-09-06

| ID | Pass | Location | Change (summary) | Disp. | Why | Superseded by | Owner item |
|---|---|---|---|---|---|---|---|
| S-0906-1 | 2 | TBD-003 (c), append | Resumption of UI-SUCCESSOR alone does not make the witness completable; list the further SWBPIPE owner decisions (CA §2.6) | **INCLUDE** | Pointer; no criterion changes | — | Q-2 |
| S-0906-2 | 2 | OUT-003, after "...received host evidence." | Name the PROPOSED W14 result-record schema; rehearsals never count | **INCLUDE** | Pointer | — | Q-2 |
| S-0906-3 | 2 | CLM-003; REQ-008 exclusion list | Add DEL-09-01 as supplier of examination support and the evidence protocol | **INCLUDE** | Grounds a consumer row on an admitted arc | — | Q-2 |
| S-0906-4 | 2 | REQ-007 (optional (a) or (b)) | (a) name each network destination contacted in observed behaviour; (b) no change | **DROP** | Source itself finds (b) supportable: REQ-002 "observed behavior" already covers it and V4-EXM-23 sits with DEL-09-07 | — | Q-11 |

### DEL-09-09

| ID | Pass | Location | Change (summary) | Disp. | Why | Superseded by | Owner item |
|---|---|---|---|---|---|---|---|
| S-0909-1 | 2 | REQ-001, second-to-last sentence | "TBD-001 through TBD-004" -> "TBD-001 through TBD-005" | **INCLUDE** | Pointer correction | — | Q-2 |
| S-0909-2 | 2 | OUT-001; OUT-003 | Name the PROPOSED result-record and work-account schemas; rehearsals never count | **INCLUDE** | Pointer | — | Q-2 |

## register (95)

### DEL-01-01

| ID | Pass | Location | Change (summary) | Disp. | Why | Superseded by | Owner item |
|---|---|---|---|---|---|---|---|
| R-11-1 | 2 | 10 new DOWNSTREAM rows | Mirrors for DEL-02-01, 02-03, 02-04, 03-03, 03-04, 04-03, 09-06, 06-01, 09-01, 09-02 (10 rows) [mirror only (admitted)] | **INCLUDE** | DEL-01-01 SoW names 3 of the 10 (checked); grounded by P1-09. Includes F0 M-6 | — | Q-15 |
| R-11-2 | 2 | DEP-01-01-018 Notes | Add OBS-1/OBS-1b facts (Responses wire worked; MCP tools not delivered); DEP-005 unchanged [non-topological] | **INCLUDE** | Notes | — | Q-2 |
| R-11-3 | 2+3 | DEP-01-01-022 Notes | Add the namespace route limit (F-31) and approval-carrier quirk (F-32); pass 3 extends: delegation tools travel in the same namespace tool (OBS-2 O-4, via an adapter); account now at ACCESS §11 CH-1..CH-8 [non-topological] | **INCLUDE** | As extended in pass 3 | — | Q-2 |

### DEL-01-02

| ID | Pass | Location | Change (summary) | Disp. | Why | Superseded by | Owner item |
|---|---|---|---|---|---|---|---|
| R3-01-02-a | 3 | new DOWNSTREAM INTERFACE row | -> DEL-01-03 (mirror of DEP-01-03-012) [mirror only (admitted)] | **INCLUDE** | With SC3-01-02-8 | — | Q-2 |
| R3-01-02-b | 3 | new DOWNSTREAM HANDOVER row | -> DEL-09-02 (mirror of DEP-09-02-010) [mirror only (admitted)] | **INCLUDE** | With SC3-01-02-8 | — | Q-2 |
| R3-01-02-c | 3 | DEP-01-02-021 Statement | OI-001/002 "remain with the owner" -> ruled by D2/D3 for this scope; beyond them with the owner [non-topological] | **INCLUDE** | With SC3-01-02-5 | — | Q-2 |
| R3-01-02-d | 3 | DEP-01-02-018 Notes (optional) | UPDATE: D4 selected 0.158.0 for definition; qualification pin open [non-topological] | **INCLUDE** | With SC3-01-02-6 | — | Q-11 |
| R3-01-02-e | 3 | new DOWNSTREAM row (conditional) | Mirror of NR-01 (DEL-02-03) [mirror of new admitted arc] | **INCLUDE** | NR-01 INCLUDE | — | Q-4 |
| R3-01-02-f | 3 | new DOWNSTREAM row (conditional) | Mirror of NR-02 (DEL-03-03) [mirror of new admitted arc] | **INCLUDE** | NR-02 INCLUDE | — | Q-4 |
| R3-01-02-g | 3 | new DOWNSTREAM row (conditional) | Mirror of NR-03 (DEL-09-09) [—] | **DROP** | NR-03 DROP | — | Q-4 |
| R3-01-02-h | 3 | new DOWNSTREAM row (conditional) | Mirror of NR-04 (DEL-02-02) [mirror of new admitted arc] | **INCLUDE** | NR-04 INCLUDE | — | Q-4 |

### DEL-01-03

| ID | Pass | Location | Change (summary) | Disp. | Why | Superseded by | Owner item |
|---|---|---|---|---|---|---|---|
| R3-01-03-a..c | 3 | 3 new DOWNSTREAM rows | Mirrors of DEP-06-01-007, DEP-09-02-011, DEP-09-05-008; package row DEP-01-03-014 may stay (3 rows) [mirror only (admitted)] | **INCLUDE** | With SC3-01-03-8 | — | Q-2 |
| R3-01-03-d | 3 | new DOWNSTREAM INTERFACE row | -> DEL-01-04 (plan-mode element, anchors, availability) [mirror of new admitted arc] | **INCLUDE** | With SC3-01-03-8; mirror of NR-05 | — | Q-4 |
| R3-01-03-e | 3 | DEP-01-03-017 | Refresh to the OI-001 residue; record OI-002 as ruled by D3 (split/retire or note, at extraction's choice) [non-topological] | **INCLUDE** | With SC3-01-03-2 (SCA-V4-002 treatment of the DEL-01-04 twin rows) | — | Q-2 |
| R3-01-03-f | 3 | DEP-01-03-011 Notes (optional) | D4 pointer [non-topological] | **INCLUDE** | With SC3-01-03-1 | — | Q-11 |

### DEL-01-04

| ID | Pass | Location | Change (summary) | Disp. | Why | Superseded by | Owner item |
|---|---|---|---|---|---|---|---|
| R2-01-04-a | 2 | new DOWNSTREAM HANDOVER row | -> DEL-02-03 (mirror of DEP-02-03-027, X-1) [mirror only (held)] | **INCLUDE** | Kept by P3RUN C1-A as F0 M-7; grounded by SC3-01-04-1's consumer list | — | Q-2 |
| NR-05 | 3 | new UPSTREAM INTERFACE row | -> DEL-01-03 (plan-mode element, item anchors, delegation availability) [NEW ARC admitted DEL-01-04->DEL-01-03] | **INCLUDE** | Adopted by R18-1 C-06; grounded by SC3-01-04-10 | — | Q-4 |
| NR-07 | 3 | new UPSTREAM INTERFACE row | -> DEL-01-05 (selection state; Codex account) [NEW ARC admitted DEL-01-04->DEL-01-05] | **INCLUDE** | Grounded by SC3-01-04-6 as amended (also listed by C1-B) | — | Q-4 |
| NR-08 | 3 | new UPSTREAM INTERFACE row | -> DEL-04-02 (K-5/K-6 components and display meanings) [NEW ARC held DEL-01-04->DEL-04-02] | **INCLUDE** | Grounded by SC3-01-04-5; AS-v0.9 §12 already names DEL-01-04 | — | Q-4 |
| NR-09 | 3 | new UPSTREAM INTERFACE row | -> DEL-02-03 (SD-1..SD-5, arrival references) [NEW ARC held DEL-01-04->DEL-02-03] | **INCLUDE** | Grounded by SC3-01-04-5 | — | Q-4 |
| NR-4 | 3 | new UPSTREAM INTERFACE row | -> DEL-02-04 (role list with default_for_new_chat, Continue-as composition, guidance-changed signal) [NEW ARC held DEL-01-04->DEL-02-04] | **INCLUDE** | Adopted by R22-1; grounded by SC3-01-04-11 (also listed by C1-B) | — | Q-4 |
| R3-01-04-b | 3 | new DOWNSTREAM HANDOVER row | -> DEL-09-02 (mirror of DEP-09-02-012) [mirror only (admitted)] | **INCLUDE** | With SC3-01-04-13 | — | Q-2 |
| SC3-01-04-9 | 3 | DEP-01-04-010 Statement | Add "and the App act control that captures workflow registration (A15)" [non-topological] | **INCLUDE** | Pairs SC3-02-02-6 | — | Q-2 |
| R3-01-04-a | 3 | DEP-01-04-009 Statement | Append the A15 descriptor (one per act: one reviewed draft, or several library entries) and the run-start text and run-end line [non-topological] | **INCLUDE** | Corrected to R21-3 | — | Q-2 |

### DEL-01-05

| ID | Pass | Location | Change (summary) | Disp. | Why | Superseded by | Owner item |
|---|---|---|---|---|---|---|---|
| R3-01-05-a | 3 | new DOWNSTREAM HANDOVER row | -> DEL-01-01 (mirror of DEP-01-01-024) [mirror only (held, SCC-001)] | **INCLUDE** | DEL-01-05 SoW names DEL-01-01 (checked) | — | Q-2 |
| R3-01-05-b | 3 | new DOWNSTREAM HANDOVER row | -> DEL-09-02 (mirror of DEP-09-02-013) [mirror only (admitted)] | **INCLUDE** | With SC3-01-05-12 | — | Q-2 |
| R3-01-05-c | 3 | DEP-01-05-015 | TargetLocation TBD -> Design/ACCOUNT_HOME_DECISION_RECORD.md; TargetName to the Owner's choice (L-7); Notes: decided at choice level, mechanism observed [non-topological] | **INCLUDE** | Follows SC3-01-05-1, -8, -10 | — | Q-2 |
| R3-01-05-d | 3 | DEP-01-05-016 | TargetLocation TBD -> ACCESS §10; Notes: OI-010 open (L-6) [non-topological] | **INCLUDE** | Follows SC3-01-05-13 | — | Q-2 |
| R3-01-05-e | 3 | DEP-01-05-012 Notes | 0.158.0 is the definition/generation pin (D4); qualification pin open [non-topological] | **INCLUDE** | Follows SC3-01-05-3 | — | Q-2 |

### DEL-02-01

| ID | Pass | Location | Change (summary) | Disp. | Why | Superseded by | Owner item |
|---|---|---|---|---|---|---|---|
| R2-02-01-a..f | 2 | 6 new DOWNSTREAM HANDOVER rows | Mirrors of DEP-02-03-009, DEP-03-02-027, DEP-03-04-008, DEP-05-01-016, DEP-05-02-005, DEP-09-06-025 (6 rows) [mirror only (4 held, 2 admitted)] | **INCLUDE** | With SC2-02-01-2 | — | Q-2 |
| R2-02-01-g | 2 | DEP-02-01-025 Statement | Align with SC2-02-01-1 (inventory, group meanings, availability signals) [non-topological] | **INCLUDE** | Statement refresh | — | Q-2 |
| R2-02-01-h | 2 | DEP-02-01-027 RequiredMaturity, SatisfactionStatus | TBD -> INITIALIZED; TBD -> PENDING, as the other deliverable rows in this register [non-topological] | **INCLUDE** | Local to one register; the cross-register convention is R-02-4 (DEFER) | — | Q-2 |
| RP1-MX-0201 | P1 | 5 new DOWNSTREAM rows | Mirrors for DEL-02-02 (DEP-02-02-014), DEL-02-04 (DEP-02-04-011), DEL-08-02 (DEP-08-02-006), DEL-09-02 (DEP-09-02-015), DEL-10-03 (DEP-10-03-008) (5 rows) [mirror only (2 held, 3 admitted)] | **INCLUDE** | Grounded by SC2-02-01-2 (P2-B G-0201-02); extraction reads the sentence as DOWNSTREAM rows, so leaving them out would make register and SoW disagree. Existing arcs, no topology change | — | Q-17 |

### DEL-02-02

| ID | Pass | Location | Change (summary) | Disp. | Why | Superseded by | Owner item |
|---|---|---|---|---|---|---|---|
| NR-04 | 3 | new UPSTREAM INTERFACE row (optional) | -> DEL-01-02 (stop and run-end definitions; App-start reconciliation WR SQ-X) [NEW ARC admitted DEL-02-02->DEL-01-02] | **INCLUDE** | R22-4: add the consuming sentence (P1-03). Chaining rests on DEL-01-02's run-end definition. Admitted, SCC-free | — | Q-4 |
| SC3-02-02-6 | 3 | DEP-02-02-013 Statement | Add the App act control and capture evidence [non-topological] | **INCLUDE** | Pairs SC3-01-04-9 | — | Q-2 |
| SC3-02-02-7 | 3 | DEP-02-02-016/-017 Statements | Name A15 and its RS record kind (2 rows) [non-topological] | **INCLUDE** | = the pass-2 C1-A note (B4 §7) | — | Q-2 |
| R3-02-02-a..c | 3 | 3 new DOWNSTREAM rows | -> DEL-01-04 (DEP-01-04-009), DEL-02-03 (DEP-02-03-010), DEL-09-06 (DEP-09-06-026) (3 rows) [mirror only (2 held, 1 admitted)] | **INCLUDE** | With SC3-02-02-12 | — | Q-2 |
| R3-02-02-d | 3 | new DOWNSTREAM HANDOVER row | -> DEL-04-03 (mirror of R20-10) [mirror of new held arc] | **INCLUDE** | With SC3-02-02-12 | — | Q-4 |

### DEL-02-02; DEL-02-03

| ID | Pass | Location | Change (summary) | Disp. | Why | Superseded by | Owner item |
|---|---|---|---|---|---|---|---|
| SC3-02-02-9 | 3 | DEP-02-02-015 and DEP-02-03-010 Statements | Add the run-start text, its identity and supply check (2 rows) [non-topological (held arc)] | **INCLUDE** | Grounded by SC3-02-02-12 | — | Q-2 |

### DEL-02-03

| ID | Pass | Location | Change (summary) | Disp. | Why | Superseded by | Owner item |
|---|---|---|---|---|---|---|---|
| R2-02-03-a | 2 | new UPSTREAM INTERFACE row | -> DEL-04-02 (mirror of DEP-04-02-023) [mirror only (held)] | **INCLUDE** | With SC2-02-03-3 | — | Q-2 |
| R2-02-03-b..i | 2 | 8 new DOWNSTREAM HANDOVER rows | Mirrors of DEP-02-01-026, DEP-03-03-014, DEP-03-04-009, DEP-04-02-017, DEP-04-03-025, DEP-05-01-017, DEP-05-02-020, DEP-09-09-023 (8 rows) [mirror only (7 held, 1 admitted)] | **INCLUDE** | With SC2-02-03-6 | — | Q-2 |
| R2-02-03-j | 2 | DEP-02-03-027 Statement | "App act control and person identity" -> "App act control (person identity as K1-4 sets it)" [non-topological] | **INCLUDE** | Statement refresh | — | Q-2 |
| NR-01 | 3 | new UPSTREAM INTERFACE row | -> DEL-01-02 (custody events, run-tag lookup; EXEC §2.7, AE-6, RE-4) [NEW ARC admitted DEL-02-03->DEL-01-02] | **INCLUDE** | R22-4: add the consuming sentence (P1-01). Admitted, SCC-free | — | Q-4 |
| RP1-MX-0203 | P1 | 3 new DOWNSTREAM rows | Mirrors for DEL-02-02 (DEP-02-02-015), DEL-09-02 (DEP-09-02-017), DEL-10-03 (DEP-10-03-009) (3 rows) [mirror only (1 held, 2 admitted)] | **INCLUDE** | Grounded by SC2-02-03-6 (P2-B G-0203-06); extraction reads the sentence as DOWNSTREAM rows, so leaving them out would make register and SoW disagree. Existing arcs, no topology change | — | Q-17 |

### DEL-02-04

| ID | Pass | Location | Change (summary) | Disp. | Why | Superseded by | Owner item |
|---|---|---|---|---|---|---|---|
| SC3-02-04-8 | 3 | DEP-02-04-010 Statement | Add status, delegation-item (completed spawnAgent, thread/read) and configuration-read surfaces [non-topological] | **INCLUDE** | Statement refresh | — | Q-2 |
| R3-02-04-a..b | 3 | 2 new DOWNSTREAM rows | -> DEL-03-04 (DEP-03-04-010), DEL-10-03 (DEP-10-03-010) (2 rows) [mirror only (admitted)] | **INCLUDE** | With SC3-02-04-9 | — | Q-2 |
| R3-02-04-c | 3 | new DOWNSTREAM row (conditional) | -> DEL-01-04 (mirror of NR-4) [mirror of new held arc] | **INCLUDE** | NR-4 adopted (R22-1) | — | Q-4 |
| R3-02-04-d | 3 | DEP-02-04-016 Notes | OI-018 answered for the App (K-9 as amended by L-2); open for hosts [non-topological] | **INCLUDE** | Follows SC3-02-04-2 | — | Q-2 |
| NR-06 | 3 | new UPSTREAM row | -> DEL-01-03 [—] | **DROP** | Withdrawn (R18-1 C-07): the K-10 standing is a runtime value | R18-1 C-07 | — |
| NR-10 | 3 | new UPSTREAM row | -> DEL-02-02 [—] | **DROP** | Withdrawn (R19-7): DEL-02-04 composes role guidance only | R19-7 | — |

### DEL-03-01

| ID | Pass | Location | Change (summary) | Disp. | Why | Superseded by | Owner item |
|---|---|---|---|---|---|---|---|
| R-01-1 | 2 | 11 new DOWNSTREAM rows | Mirrors for DEL-02-01, 02-03, 03-03, 03-04, 04-02, 04-03, 05-01, 05-02, 09-06, 09-09, 10-03 (11 rows) [mirror only (8 held, 3 admitted)] | **INCLUDE** | DEL-03-01's SoW names only 2 of the 11 consumers (checked); grounded by P1-06 | — | Q-15 |
| R-01-2 | 2 | DEP-03-01-022 | Retire or retarget the PKG-02 package-level DOWNSTREAM row (deliverable-level consumers are DEP-02-01-017, DEP-02-03-011) [non-topological] | **INCLUDE** | Register hygiene; retire with source_revised or retarget at extraction | — | Q-2 |
| R-01-3 | 2 | DEP-03-01-025 Notes (conditional) | Host also supplies its catalog edition identity and edition-change event; (with S-01-4) its basis profile incl. declared absence [non-topological] | **INCLUDE** | Edition part only (follows S-01-3); the R13-1 part follows S-01-4 (DEFER) | — | Q-6 |

### DEL-03-02

| ID | Pass | Location | Change (summary) | Disp. | Why | Superseded by | Owner item |
|---|---|---|---|---|---|---|---|
| R-02-1 | 2 | new DOWNSTREAM INTERFACE row | -> DEL-03-01 (mirror of DEP-03-01-026) [mirror only (held)] | **INCLUDE** | DEL-03-02 SoW names DEL-03-01 (checked) | — | Q-2 |
| R-02-2 | 2 | 6 new DOWNSTREAM rows | Mirrors for DEL-02-01 (N-18), 02-03 (N-21), 05-01, 05-02, 09-06, 10-03 (6 rows) [mirror only (4 held, 2 admitted)] | **INCLUDE** | DEL-03-02 SoW names 1 of the 6 (checked); grounded by P1-07 | — | Q-15 |
| R-02-3 | 2 | new UPSTREAM INTERFACE row (optional) | -> DEL-04-02 (visible autonomy state) [mirror only (held)] | **INCLUDE** | With S-02-2 | — | Q-11 |

### DEL-03-02; DEL-03-04; DEL-01-01

| ID | Pass | Location | Change (summary) | Disp. | Why | Superseded by | Owner item |
|---|---|---|---|---|---|---|---|
| R-02-4 | 2 | SatisfactionStatus values | One TBD/PENDING convention across registers [non-topological] | **DEFER** | A cross-register convention for the register owners' pass named in DAG-003 HANDOFF_STATE; choosing the value here would be a new convention | — | Q-14 |

### DEL-03-03

| ID | Pass | Location | Change (summary) | Disp. | Why | Superseded by | Owner item |
|---|---|---|---|---|---|---|---|
| R-03-1 | 2 | 4 new DOWNSTREAM rows | Mirrors for DEL-02-03 (N-24), 03-04, 04-03, 09-06 (4 rows) [mirror only (2 held, 2 admitted)] | **INCLUDE** | DEL-03-03 SoW names 1 of the 4 (checked); grounded by P1-08 | — | Q-15 |
| R-03-3 | 2 | DEP-03-03-014 Statement | Required-tool check in the current phase (as S-03-2) [non-topological] | **INCLUDE** | Statement refresh | — | Q-2 |
| R-03-4 | 2 | 2 new UPSTREAM INTERFACE rows (optional) | -> DEL-04-02 and -> DEL-02-01 (governance-phase constraints) (2 rows) [mirror only (held)] | **INCLUDE** | With S-03-3 | — | Q-11 |
| R-03-5 | 2 | DEP-03-03-009 Notes | Add the OBS-1/OBS-1b dated observations (not qualification) [non-topological] | **INCLUDE** | Notes; P2 may also cite OBS-2/OBS-3 where they bear on the row | — | Q-2 |
| R-03-6 | 2 | DEP-03-03-013 Statement | Add command-execution surfaces (as S-03-5) [non-topological] | **INCLUDE** | Statement refresh | — | Q-2 |
| NR-02 | 3 | new UPSTREAM INTERFACE row | -> DEL-01-02 (in-flight items, relaunch fact; ADAPTER PI-6, XF-41) [NEW ARC admitted DEL-03-03->DEL-01-02] | **INCLUDE** | R22-4: add the consuming sentence (P1-02). Admitted, SCC-free | — | Q-4 |

### DEL-03-03; DEL-04-01

| ID | Pass | Location | Change (summary) | Disp. | Why | Superseded by | Owner item |
|---|---|---|---|---|---|---|---|
| R-03-2 | 2 | DEP-03-03-008 RequiredMaturity | Reconcile TBD with mirror DEP-04-01-023 INITIALIZED [non-topological] | **INCLUDE** | Value set at extraction; both register owners | — | Q-2 |

### DEL-03-04

| ID | Pass | Location | Change (summary) | Disp. | Why | Superseded by | Owner item |
|---|---|---|---|---|---|---|---|
| R-04-1 | 2 | DEP-03-04-021 Statement | Add supplier facts on run holds, supplied guidance, model destination (as S-04-1) [non-topological] | **INCLUDE** | Statement refresh | — | Q-2 |
| R-04-2 | 2 | DEP-03-04-022 Statement | Add the connected-activity contract (as S-04-2) [non-topological] | **INCLUDE** | Statement refresh | — | Q-2 |

### DEL-04-01

| ID | Pass | Location | Change (summary) | Disp. | Why | Superseded by | Owner item |
|---|---|---|---|---|---|---|---|
| R2-04-01-a | 2 | new DOWNSTREAM HANDOVER row | Mirror of DEP-09-06-030 (-> DEL-09-06) [mirror only (admitted DEL-09-06->DEL-04-01)] | **INCLUDE** | With SC2-04-01-1 | — | Q-2 |
| R2-04-01-b | 2 | new UPSTREAM CONSTRAINT EXTERNAL row | DECISION-5 destination grant (conditional) [non-topological] | **DEFER** | Follows SC2-04-01-2 (DEFER) | — | Q-9 |
| R2-04-01-c | 2 | new UPSTREAM CONSTRAINT EXTERNAL row | Owner decision on the consequence vocabulary [non-topological] | **INCLUDE** | With SC2-04-01-3 | — | Q-2 |
| RP1-MX-0401 | P1 | 2 new DOWNSTREAM rows | Mirrors for DEL-01-04 (DEP-01-04-011), DEL-02-02 (DEP-02-02-016) (2 rows) [mirror only (admitted)] | **INCLUDE** | Grounded by SC2-04-01-4 (P2-B G-0401-02; optional, Q-11); extraction reads the sentence as DOWNSTREAM rows, so leaving them out would make register and SoW disagree. Existing arcs, no topology change | — | Q-17 |

### DEL-04-02

| ID | Pass | Location | Change (summary) | Disp. | Why | Superseded by | Owner item |
|---|---|---|---|---|---|---|---|
| R2-04-02-a..c | 2 | 3 new DOWNSTREAM HANDOVER rows | Mirrors of DEP-03-04-012, DEP-09-06-031, DEP-09-09-022 (3 rows) [mirror only (2 admitted, 1 held)] | **INCLUDE** | With SC2-04-02-1 | — | Q-2 |

### DEL-04-03

| ID | Pass | Location | Change (summary) | Disp. | Why | Superseded by | Owner item |
|---|---|---|---|---|---|---|---|
| R2-04-03-a..d | 2 | 4 new DOWNSTREAM INTERFACE rows | Mirrors of DEP-02-01-019, DEP-02-03-013, DEP-03-01-031, DEP-03-04-013; DEP-04-03-011/-012 may stay as package rows (4 rows) [mirror only (3 held, 1 admitted)] | **INCLUDE** | With SC2-04-03-1 | — | Q-2 |
| R2-04-03-e | 2 | new UPSTREAM INTERFACE row | Receive the workflow identity tuple and checkpoint disposition vocabulary from DEL-02-01 [NEW ARC held DEL-04-03->DEL-02-01] | **INCLUDE** | The one pass-2 new arc; both ends in SCC-002, so held and SCC-neutral (recomputed) | — | Q-4 |
| R2-04-03-f | 2 | DEP-04-03-025 Statement | Add "act request (where it can be identified)" [non-topological] | **INCLUDE** | Statement refresh | — | Q-2 |
| R2-04-03-h | 2 | Run Notes label | "...DEP-04-03-031 (DEL-09-06 consuming this record contract, N-08, ...)" -> "...(the arc of DEP-09-06-015, ...)" [non-topological] | **INCLUDE** | Label correction | — | Q-2 |
| R20-10 | 3 | new UPSTREAM INTERFACE row | -> DEL-02-02 (run text, supply check, A15 relations) [NEW ARC held DEL-04-03->DEL-02-02] | **INCLUDE** | Grounded on the consumer side by P1-05 (no source proposes it) | — | Q-4 |
| R22-7-reg | 3 | new UPSTREAM INTERFACE row | -> DEL-02-04 (mirror of DEP-02-04-012) [mirror only (held)] | **INCLUDE** | With R22-7-SoW; arc exists (held), no topology change | — | Q-15 |
| RP1-MX-0403 | P1 | 5 new DOWNSTREAM rows | Mirrors for DEL-01-04 (DEP-01-04-012), DEL-02-02 (DEP-02-02-017), DEL-09-02 (DEP-09-02-019), DEL-09-05 (DEP-09-05-010), DEL-10-03 (DEP-10-03-014) (5 rows) [mirror only (2 held, 3 admitted)] | **INCLUDE** | Grounded by SC2-04-03-1 (P2-B G-0403-05); extraction reads the sentence as DOWNSTREAM rows, so leaving them out would make register and SoW disagree. Existing arcs, no topology change | — | Q-17 |

### DEL-04-03; DEL-09-06

| ID | Pass | Location | Change (summary) | Disp. | Why | Superseded by | Owner item |
|---|---|---|---|---|---|---|---|
| R2-04-03-g | 2 | DEP-04-03-031 / DEP-09-06-015 RequiredMaturity | Reconcile INITIALIZED vs TBD (one value in both) (2 rows) [non-topological] | **INCLUDE** | Value set by extraction from the revised SoWs; both register owners | — | Q-2 |

### DEL-05-01

| ID | Pass | Location | Change (summary) | Disp. | Why | Superseded by | Owner item |
|---|---|---|---|---|---|---|---|
| R-0501-1 | 2 | DEP-05-01-024 Notes | FB-CC-1 is a fixture basis, not a product selection; TargetType stays UNKNOWN, PENDING [non-topological] | **INCLUDE** | Notes | — | Q-2 |
| R-0501-2 | 2 | DEP-05-01-014 Notes | Destination flow also consumes the external-contact declaration and the destination-request entry kind [non-topological] | **INCLUDE** | Notes; consistent with S-01-2 | — | Q-2 |
| R-0501-3 | 2 | DEP-05-01-025 Notes | Grant in force per dispatch now defined (AS §12.1; LOOP §6.2) [non-topological] | **INCLUDE** | Notes | — | Q-2 |
| R-0501-4 | 2 | new UPSTREAM INTERFACE row | -> DEL-01-05 (mirror of DEP-01-05-014) [mirror only (admitted)] | **INCLUDE** | Kept in pass 3 (C1-B: LOOP-v0.9 §10.3 now reads the handoff). DEL-05-01 SoW does not name DEL-01-05 (checked): grounded by P1-10 | — | Q-15 |
| R-0501-5 | 2 | new DOWNSTREAM HANDOVER EXTERNAL row | -> DEP-001: loop receiving questions via human file relay (mirrors DEP-05-02-018) [non-topological] | **INCLUDE** | EXTERNAL; non-topological | — | Q-2 |

### DEL-05-02

| ID | Pass | Location | Change (summary) | Disp. | Why | Superseded by | Owner item |
|---|---|---|---|---|---|---|---|
| R-0502-1 | 2 | Statements of DEP-05-02-005..-010, -019 | "checked" -> "identified, independently compared" (meaning unchanged) (7 rows) [non-topological] | **INCLUDE** | Wording; 7 rows | — | Q-2 |
| R-0502-2 | 2 | DEP-05-02-010, -019 Statements (conditional) | Add destination rules/flow and destination displays (2 rows) [non-topological] | **DEFER** | Follows S-0502-1 (DEFER) | — | Q-9 |

### DEL-09-06

| ID | Pass | Location | Change (summary) | Disp. | Why | Superseded by | Owner item |
|---|---|---|---|---|---|---|---|
| R-0906-1 | 2 | DEP-09-06-019 Notes | Option-sheet result: 0 of 10 steps examinable against SWBPIPE [non-topological] | **INCLUDE** | Notes | — | Q-2 |
| R-0906-2 | 2 | DEP-09-06-027 Notes | Rehearsals run on SH-1; test-double evidence only [non-topological] | **INCLUDE** | Notes | — | Q-2 |
| R-0906-3 | 2 | new UPSTREAM INTERFACE row | -> DEL-09-01 (mirror of DEP-09-01-024) [mirror only (admitted)] | **INCLUDE** | Consumer row on an admitted arc | — | Q-2 |
| R-0906-4 | 2 | DEP-09-06-015 RequiredMaturity | Reconcile with DEP-04-03-031 [non-topological] | **DROP** | Duplicate: R2-04-03-g covers both rows | R2-04-03-g | — |

### DEL-09-09

| ID | Pass | Location | Change (summary) | Disp. | Why | Superseded by | Owner item |
|---|---|---|---|---|---|---|---|
| R-0909-1 | 2 | DEP-09-09-014 Statement | Add host fixture set-up and reset (XT IN-30) [non-topological] | **INCLUDE** | EXTERNAL statement refresh | — | Q-2 |
| R-0909-2 | 2 | DEP-09-09-007 Notes | Rehearsals run on SH-1; test-double evidence only [non-topological] | **INCLUDE** | Notes | — | Q-2 |
| R-0909-3 | 2 | DEP-09-09-010 Notes | Replace pre-ruling OI-001/002 owner text with D2/D3 rulings; OI-021 and DEP-001 remain [non-topological] | **INCLUDE** | Notes | — | Q-2 |
| NR-03 | 3 | new UPSTREAM INTERFACE row (optional) | -> DEL-01-02 (XT XC-06) [—] | **DROP** | R22-4: drop the row; XC-06's reliance stays a labelled cross-reference, carried through ADAPTER (NR-02). Optional at source; avoids a third admitted arc into DEL-01-02 for a witness | — | Q-4 |

### DEL-11-02

| ID | Pass | Location | Change (summary) | Disp. | Why | Superseded by | Owner item |
|---|---|---|---|---|---|---|---|
| R22-7-open | 3 | DEP-02-04-013 supplier side | No row proposed: the consumer-side counterpart owed by DEL-11-02 stays open with DEL-11-02's owner (0 rows) [—] | **DEFER** | DEL-11-02 is outside the design passes; R22-7 records it open with its owner; no SoW block | — | Q-15 |

## Open_Issues (2)

### DEL-01-05

| ID | Pass | Location | Change (summary) | Disp. | Why | Superseded by | Owner item |
|---|---|---|---|---|---|---|---|
| SC3-01-05-8 | 3 | OI-009 Status and Consequence | OPEN -> decided at choice level (K-1; Owner also App implementation owner, L-7); mechanism observed at 0.158.0 (O-6); separation with a credential not observed (L-6) | **INCLUDE** | Status token not fixed by any source: owner chooses at Q-10 (option A keeps OPEN with a pointer, SCA-V4-002 precedent) | — | Q-10 |

### DEL-02-04

| ID | Pass | Location | Change (summary) | Disp. | Why | Superseded by | Owner item |
|---|---|---|---|---|---|---|---|
| OI-018-ptr | 3 | OI-018 Consequence, append (optional) | Answered for the App by K-9 as amended by L-2; hosts and other instruction owners remain open (status stays OPEN) | **INCLUDE** | Pointer only; status unchanged | — | Q-11 |

## basis (6)

### DEL-01-01

| ID | Pass | Location | Change (summary) | Disp. | Why | Superseded by | Owner item |
|---|---|---|---|---|---|---|---|
| P2-C1-B-B-1 | 2 | §1 priority 3 | No accepted text decides the supplier's own start-up traffic | **DROP** | Answered by the owner (K-12 as revised, L-3); SoW route SC3-01-05-5; no basis text needed (P3RUN C1-B §4.4) | SC3-01-05-5 (K-12, L-3) | Q-12 |

### DEL-01-05

| ID | Pass | Location | Change (summary) | Disp. | Why | Superseded by | Owner item |
|---|---|---|---|---|---|---|---|
| SIWC-custody | 3 | V4-ARC-04 custody rule | "custodied by Codex, or, for a ChatGPT plan grant made to Chirality, by the App in protected OS storage" | **DROP** | Recommendation superseded (2026-10-02); conditional on reopening SIWC (four triggers); not proposed by C1-B | — | Q-12 |

### DEL-03-01

| ID | Pass | Location | Change (summary) | Disp. | Why | Superseded by | Owner item |
|---|---|---|---|---|---|---|---|
| P2-C1-B-B-2 | 2 | V4-HI-02 | Whether V4-HI-02 should name the catalog edition | **DEFER** | Observation for the basis owner if S-01-3 is adopted; no text proposed | — | Q-12 |
| P2-C1-B-B-3 | 2 | V4-HI-11 | No basis change; R13-1 recorded as a host non-conformance (SWBPIPE SQ-07) | **DROP** | Source proposes no change | — | Q-12 |

### DEL-05-01

| ID | Pass | Location | Change (summary) | Disp. | Why | Superseded by | Owner item |
|---|---|---|---|---|---|---|---|
| P2-C1-C-B-1 | 2 | §4 host-agent property, allow-list bullet (optional) | Add the K1-5 rule (named destination allowed on its own; category switch allows all; off -> only named entries) | **DEFER** | Optional; no contradiction; a basis edit here would force a Consolidated_Coverage recompute of ARCHITECTURE rows. Carry to the next basis update | — | Q-12 |
| P2-C1-C-B-2 | 2 | V4-HI-70 / V4-HOST-02 as amended | Whether boundary-refused destination requests are also recorded (a person's decline is now SETTLED by DEL-04-03 CLM-004, R16-1) | **DEFER** | Owner phase-review question; narrowed by R16-1 to refusals the loop makes without asking | — | Q-12 |

## decomposition (1)

### —

| ID | Pass | Location | Change (summary) | Disp. | Why | Superseded by | Owner item |
|---|---|---|---|---|---|---|---|
| DC-01 | P1 | ## Decision Log | Append the SCA-V4-003 amendment entry (ID, date, description, requested by the owner) | **INCLUDE** | Acceptance-conditional (applied after group 3), as SCA-V4-002 B-04 | — | Q-3 |

## Checks

- Every proposal ID in both passes' C1 records and in pass 3's `D/*.md`, `F/*.md` and `reviews/*.md` was matched by script to a row ID or alias. The only unmatched tokens are D-node local numbers recorded with their node prefix as aliases (D3 `NR-1`…`NR-3`, D4 `NR-1`…`NR-3`, D5 `NR-1`/`NR-2`, D1 `NR-D1-1`…`-3`) and `NR-L1`, which is an item on the SWBPIPE next-relay list (F-E1, RV21-B), not a register or ScopeOfWork proposal. IDs are unique in the CSV.
- At RP1 every block heading in `SOW_REVISIONS_A.md` and `SOW_REVISIONS_B.md` that cites a ledger row was matched by script to an INCLUDE ScopeOfWork row, and every INCLUDE ScopeOfWork row to a block (G-0403-03 now carries R22-7-SoW).
- "Names X (checked)" means a script counted the deliverable ID in the current ScopeOfWork bytes at HEAD `897a107cc9`.
- Arc classes and SCC effects: [ARC_EFFECT.md](ARC_EFFECT.md).
