# F-D — first-increment edits: WD, WD-EX, CA (return)

- Run `APP-V4-DESIGN-PASS-3-20261001`, node **F-D**. Executor: Type 2 TASK
  (Claude Opus 5.5), dispatched by the HELP_HUMAN session; no delegation.
  2026-10-02, working tree at HEAD `e4e14d6ae6`.
- Fence kept. Files written: `DEL-02-01/Design/WORKFLOW_DECLARATION.md`
  (WD-v0.8 → v0.9), `DEL-02-01/Design/EXAMPLES.md` (WD-EX-v0.8 → v0.9),
  `DEL-09-06/Design/CONNECTED_ACTIVITY_CONTRACT.md` (CA-v0.6 → v0.7) and this
  file. No `FACTS_*`, `RELAY_*`, schema, example instance, prototype,
  ScopeOfWork, register or `_STATUS.md` was edited. Read-only git; no
  network; no Codex or model run. Scratch: `$TMPDIR/fd/` (replacement helper)
  and `$TMPDIR/fd-w14-*` (rehearsal outputs).
- Brief: `BRIEFS.md` "Common rules" and "F — first-increment edits" (sha256
  `316ea293…`); rows from `F/F0_JOINS.md` (`e93608be…`) §1.6–§1.8, §1.14,
  §2; rulings R17 (`b0af81bc…`), R18 (`abf5eee6…`), R19 (`16930ecd…`);
  `OWNER_DECISIONS.md` (`ea96c557…`, DECISION-K3 revised, DECISION-L).
- How checked: the three files were read whole before editing; their v0.8 /
  v0.6 sha256 equal F0's inputs (`517821d1…`, `275ea54d…`, `58167f7a…`).
  Each edit was a scripted exact-string replacement that failed unless the
  old text occurred exactly once. Table column counts were compared with
  HEAD by script (no new malformed row). A grep sweep found no remaining
  "later" / "(D1)" / "no Design file" pointer to DEL-02-02, DEL-02-04 or
  DEL-01-04 outside change tables and history lines. Supplier facts used in
  FW-10 were checked in the committed generated types (below).

## 1. Rows applied

### WD-v0.9 (`WORKFLOW_DECLARATION.md`)

| Row | Applied as | Where |
|---|---|---|
| FW-01 | OS-1 → WR-v0.2 §3, §4.2. OS-2 → A15 captured by DEL-01-04's act control bound to the reviewed content (K-8; AAC-v0.2 §4.2; WR §4.3); non-regular entry refused before review (WR HY-3); next revision of the slot, nothing overwritten (K-6). **Added from L-4 / R19-4:** shipped workflows registered by the release (origin *bundled*); byte-equal recognition; several entries in one act, each entry's bytes bound | §3.9 |
| FW-02 | OS-3: draft not selectable (K-7; WR TT-1, SL-5); selection stays on its revision (WR SL-2) | §3.9 |
| FW-03 | Registration refuses OS files, naming them (WR HY-4, PROPOSED) | §6.1 |
| FW-04 | C-4: App side pinned / newer shown / following = new selection event (WR SL-2; U-WR-13); host side unchanged. C-4 stands (K-6) | §6.3 |
| FW-05 | C-5 and U-10: App side WR SL-3; host part open (DECISION-3) | §6.3; §12 |
| FW-06 | §6.4 row 3: next revision of the App slot its lineage reaches (SP-3, DS-2); DS-1 empty slot; DS-3 refusal | §6.4 |
| FW-07 | §7 drafts row → WR §3, §4; K-6, K-8 | §7 |
| FW-08 | §8 receiver rows split (DEL-02-02 ← WR-v0.2 §7; DEL-02-04 ← ROLE-v0.2 §3.1); new "New at v0.9" join table | §8 |
| FW-09 | §13.1: App-side library and selection doubles in WR's `wrproto.py` (P-22…P-29; checked by grep) | §13.1 |
| FW-10 | `agent-delegation` standing cell per **C-04/C-05 (R18-1)**: `multiAgentMode` deprecated-ignored, not a signal; availability = model `multiAgentVersion` ≠ `disabled` and provider `namespaceTools`; effective `features.multi_agent = false` reads missing; stable surface, not labelled experimental; OBS-2 O-4 with R18-9's adapter label. `plan-update`: only plan mode labelled experimental (K-5; C-05); O-8 noted. Text placed in the standing column so S-11's group check is unaffected | §4.2.5 |
| FW-11 | §5.2 App column: role or none (R17-9; ROLE §3.1 SL-2, SL-3); role fixed for the conversation (L-2); seeded editable copy (K-9; ROLE §4.2), composed at conversation start (§5.1); edits reach new conversations (R19-3 replaces K-9's idle point); OI-018 answered for the App, open for hosts | §5.2 |
| FW-12 (CR-7 part) | CR-7: "when it is supplied (OS-7) or when it reads the file"; a read is a tool item, not supply evidence | §3.5 |
| FW-12 (OS-7 part) | **Applied as R19-1/R19-7 rule, not as F0 wrote it** (see §2) | §3.9 OS-7; §6.2 |
| FW-13 | §7 role-files row → ROLE §4.2; §9 A-6 → ROLE-v0.2; U-14 narrowed to hosts | §7; §9; §12 |
| §1.14 (L1491, L1492, L1495, L1496, L1523, L1524, L1580, L1583) | Pointers → WR-v0.2, ROLE-v0.2, AAC-v0.2; A-2 adds "DEL-02-04 no longer carries a workflow identity (R19-7)" | §9; §10; §12 U-17, U-25 |
| R19-2 (brief key consequence) | New paragraph after the OS table: (a) sequential, (b) agent-proposed with the person confirming, one run at a time, never nested, prior run cited as context; **(c) recorded as open item U-36** in UNRESOLVED (DEL-02-01's later work) | §3.9; §12 U-36 |
| R17-11 (brief key consequence) | derived-from row: App-registered revision → draft base (WR ID-1, SP-6); prior revision named by the A15, never derived-from | §6.1 |
| R19-5 | HC-1: supplier statements name their version; run-time-reported capability is read | §4.2.5 HC-1 |

### WD-EX-v0.9 (`EXAMPLES.md`)

| Row | Applied as | Where |
|---|---|---|
| FX-01 | E3: ⟨rev-A3⟩ = revision 2 of LIB-A1's `supports-adjust` (K-6; WR SP-3, DS-2), derived-from host ⟨rev-3⟩ (draft base, SP-6); prior revision ⟨rev-A2⟩ named by the A15 (R17-11); last column separates the opened host copy (LIB-A2) from ⟨rev-A3⟩ (LIB-A1) | E3 |
| FX-02 | E4 step 3: App side pinned (WR SL-2); host side open (U-10); UNRESOLVED U-10 row follows | E4; UNRESOLVED |
| §1.14 (L10, L948, L1259) | Receivers line; E1e "builds later" → AAC-v0.2, not built; U-25 construction → designed, not built. E1 intro names ⟨rev-A2⟩ as revision 1, registered by A15 at the act control | Header; E1; E1e; UNRESOLVED |

No fixture block (`wd-proto` marker), declared part or L-WDEX label changed;
L-WDEX-33a's row notes it is unchanged at WD-v0.9.

### CA-v0.7 (`CONNECTED_ACTIVITY_CONTRACT.md`)

| Row | Applied as | Where |
|---|---|---|
| FC-01 check list L29, L47, L109, L308, L513, L559, L562, L629, L709, L713, L717, L878, L1217 | Each "later" pointer → "designed in WR-v0.2 / AAC-v0.2, not built"; L29 (history) annotated, not rewritten; §4 *registered*: ⟨rev-A3⟩ revision 2 of LIB-A1's slot, derived-from ⟨rev-3⟩, A15 names reviewed draft and prior revision ⟨rev-A2⟩ (R17-11); W14-09 names the next revision of the slot | header, §0, §2.1, CAF-30, §3.1, §4, §6, §8.2, §10, UNRESOLVED |
| FC-01 §12 F-1 (L957) | New §12.12: F-1's first reason narrowed to "not built"; SWBPIPE reason stands. The v0.1 finding row is history, not edited | §12.12 |
| FC-01 UNRESOLVED (L1210) | Registration designed (WR-v0.2) with the act control (AAC-v0.2), not built; OUT-003 cannot complete until built | UNRESOLVED |
| FC-01 §3.2 (with FX-01) | ⟨rev-A2⟩/⟨rev-A3⟩ = revisions 1 and 2 of the slot | §3.2 |
| Sweep, same meaning, not in F0's list | §5 rows "Review, registration, drafts" and "App act control" (v0.6 L608, L609); §11.1 DEL-02-02 row (L917, "no Design file"); §11.1 WD row notes WD-v0.9/WD-EX-v0.9; §10 human-acts row names A15 | §5; §10; §11.1 |

No rule, case state, outcome or identifier changed; Changes from v0.6 says so.

### Added on the coordinator's two messages (D round 2; R20)

Read: `D/D1.md` (df731fa3…), `D/D2.md` (943d5140…), `D/D4.md` (c2c7e74d…),
`D/D6.md` (9c6044c7…) "Round 2" sections; `R20_RESOLUTIONS.md` (516d0fe0…,
which gained R20-5 and R20-6 while this node ran); ROLE-v0.2, NPTD-v0.2 and
the partly written WR-v0.2 in the working tree. D1 and D4 round 2 name no
WD, WD-EX or CA item.

| Item | Applied | Where |
|---|---|---|
| D2 J-6 | Delegation cell cites NPTD-v0.2 §7.1; "read at run time (R19-5)"; "otherwise not established" added to C-04's rule | WD §4.2.5 |
| D6 FW-11 | §5.2: ROLE-v0.2 SL-8 (fixed for life), §3.3 ("Continue as ‹role›" with an edited handoff summary), §4.4 GC-1; delegation row: ROLE §5.3, carrier not observed (CR-1a), a child without a role type has unknown guidance, never inherited | WD §5.2 |
| D6 FW-12 | Already superseded by R19-7 as applied; OS-7 now cites WR-v0.2 section "run-start supply" (§16 "Run text, supply check and chaining" at reading; framing WR-FRAME-1; supply check), never ROLE, for the workflow. OS-2 cites WR-v0.2 LS-8 and §4.7 for L-4. CA §4 *supplied* row cites WR-v0.2 "run-start supply" | WD §3.9; CA §4 |
| R20-1 | Chaining (a): a run ends only by the person's end or the run owner's; "End run" / "End ‹A› and start ‹B›" offered when the agent reports it finished, cause `completed`; nothing from the agent's words alone (replaces "or it completes") | WD §3.9 |
| R20-3 | App-written run-ended line before the person's next turn when no run starts, worded by DEL-02-02 | WD §3.9 |
| R20-4 | New §4.7 paragraph: no role + declared compatible roles → *unsupported*, shown and recorded, the person may proceed (EXEC CC-3; ROLE SL-7); omission of compatible roles is not this ground; host seat stays SEAT-1 / FB-12. §4.2.4's *unsupported* row names it | WD §4.7, §4.2.4 |
| R20-5 | Chaining (b): the proposal is one exact line `Next workflow: ‹origin›:‹name›`, read only in that form (EXEC RC-5); "Start ‹workflow› (proposed by the agent)" | WD §3.9 |
| R20-6 | §5.2: handoff summary drafted by the source conversation's agent in a visible turn, edited by the person | WD §5.2 |

WD's change table carries these as rows "D round 2", "R20-1, R20-3",
"R20-5, R20-6" and "R20-4"; the v0.9 inputs line pins R20 and the D returns.

## 2. Rows not applied, or applied otherwise, with reason

| Row | What F0 asked | Done instead | Reason |
|---|---|---|---|
| **FW-12** (OS-7) | Registered `WORKFLOW.md` composed into `developerInstructions` after product guidance and role, re-verified at composition (ROLE CO-3, CO-4; R17-8) | OS-7 states R19-7's route: a text element of the run-start turn carrying the revision's exact bytes, framed by App lines (framing PROPOSED in WR-v0.2); not `developerInstructions`, not `skill` (recorded alternative), not `thread/settings/update`; DEL-02-02 composes, DEL-02-03 starts the run, DEL-02-04 composes role guidance only; per-run record checked against `thread/read`. Role guidance fixed for the conversation; resume carries no new instructions (C-17, R19-3); fork keeps the source's (R19-8) | **R19 wins** (BRIEFS F; R19-1 amends R17-8; R19-7 rules the route after OBS-3). Stated in WD's change table |
| FW-12 (O-5 note) | "Composition reaches a thread only at start/fork (resume ignored)" | "Resume carries no new instructions (O-5); at 0.158.0 a fork keeps the source's (W-6)" | R19-8 / OBS-3 W-6: fork ignores new instructions, so "or fork" would be wrong |
| CA W14-08, CAF-7 | (no F0 row) | Unchanged | Their wording ("supplied guidance per thread/turn") already covers per-run turn text; changing them is beyond FC-01. Only CA §4's *supplied* row was brought to R19-7 (see §3) |
| Schema, examples, prototypes of WD and CA | (no F0 row) | Unchanged | Outside the fence; no declared-part change needs them (§3, item 1) |

## 3. Choices made inside the fence (for the integrator to confirm)

1. **Declared-part contract value stays `WD-v0.8`** (WD §3.3, new bullet,
   PROPOSED). WD-v0.9 changes no declared-part meaning; the schema
   (`const "WD-v0.8"`), fixtures and prototype (which tests "WD-v0.9" as an
   unknown version, L-WDEX-33a) are outside the fence. The value now names
   the declared-part meaning, not the document label. If the integrator
   prefers the value to track the label, the schema, both example
   instances, four fixtures, the `wd-proto` blocks and `wdproto.py` must
   change together (a later node).
2. **CA §4 *supplied* row brought to R19-7** (not an F0 row; brief "key
   consequences"): run-start text composed by DEL-02-02, checked against
   `thread/read`; role guidance separate.
3. **WD §5.2 Workflows and Delegation rows** (consistency with FW-11): L-4,
   R19-1/R19-2; R18-4 (children's roles via native agent-role
   configuration) and K-10 ("stated, not enforced").
4. **CA §10** human-acts row names A15.

## 4. Citations that F-E must check (v0.2 labels cited by v0.1 numbering)

- WR-v0.2: §2.2 ID-1; §3; §4.1 SP-3, SP-6, DS-1…DS-3; §4.2 TT-1; §4.3;
  §4.4 SL-2, SL-3, SL-5; §4.5 HY-3, HY-4, HY-6; LS-5, LS-8; §4.7; RB-2; §6
  SQ-H; §7; §12; §13; U-WR-13; section "run-start supply" (cited by name;
  §16 "Run text, supply check and chaining" in the partly written WR-v0.2 at
  reading).
- ROLE-v0.2 (now written; checked): §3.1 SL-1, SL-2, SL-3, SL-7, SL-8;
  §3.3; §4.2; §4.4 GC-1; §5.1 (role guidance only, confirmed); §5.3 CR-1a;
  §6.1; §6.3. NPTD-v0.2 §7.1 (checked).
- AAC-v0.2: §4.1; §4.2 (assumed to offer the multi-entry A15 per R19-4); §8.
- RECOVERY-v0.2 DEF-4 (ending a run, in WD's chaining paragraph).

## 5. Supplier facts verified (generated types at 0.158.0, committed bundle)

By script over `DEL-01-01/Design/generated/0.158.0/json-schema/experimental/codex_app_server_protocol.v2.schemas.json`:
`multiAgentMode` description is "@deprecated Ignored…" on `ThreadStartParams`,
`TurnStartParams` and `ThreadSettingsUpdateParams` (and "@deprecated Always
`explicitRequestOnly`" on the responses and `ThreadSettings`; F0's "Ignored"
holds for the start parameters); `MultiAgentVersion` enum `disabled`, `v1`,
`v2`, a property of `Model`; `namespaceTools` (boolean) in
`ModelProviderCapabilitiesReadResponse`. OBS-2 §6 states `multi_agent` stable
and on by default; O-4 not provoked on the stock pairing; O-8 plan item, no
`turn/plan/updated`.

## 6. New sha256

| File | Before | After |
|---|---|---|
| `DEL-02-01/Design/WORKFLOW_DECLARATION.md` (WD-v0.9) | `517821d18fc958301d3adaeb63caf11ab50f7e1ca3ec5a644a3bb4ec78b25b0e` | `a53a1be461ff634a8cde8089851c690015987052a7ee72a6d9e29ff98c3e1696` |
| `DEL-02-01/Design/EXAMPLES.md` (WD-EX-v0.9) | `275ea54d32cd8f487ec9a0f017aaa33b01ee43c79d7a675b53a7652c3519e2fd` | `50efea247c08abb0e6816dface33bbe67e59b70658d7b458b079ff7d83b73c7d` |
| `DEL-09-06/Design/CONNECTED_ACTIVITY_CONTRACT.md` (CA-v0.7) | `58167f7accaf356e1e9b0d8f14c004bcc89918b06be56b15d47e52f439cfe6ce` | `7eda8d31e2fa81703e405fd9e7ba7a30825c283572030e3e190c7f46048b5303` |
| `RUN/F/F-D.md` (this file) | — | reported in the hand-back |

## 7. Prototype reruns

Both prototypes ran before the edits (baseline) and after them; outputs are
identical to the baseline (WD: line for line after trailing spaces; CA:
apart from the run-directory line). macOS, Python 3.13.7, node v24.5.0,
2026-10-02.

**DEL-02-01** — in `DEL-02-01/Design/prototype/`:
`PYTHONDONTWRITEBYTECODE=1 python3 wdproto.py selftest` (final run 18:49 UTC);
exit 0; no `__pycache__` left. S-11 read HOSTING-BOUNDARY-v0.9 in the working
tree while F-A was editing it (sha256 at the 18:46 run
`7924a6f3e5bb768073ff09323fd6eae29de07b4c0e785c10aa70ec26319fea9f`): 27 groups,
the same ten mappings.

```text
PASS S-1a…S-1c (5)   schema, invalid example (nine errors), E1b/E1d/E1e fixtures
PASS S-2a…S-2e (5)   E1 render/extract/round trip/reading; EXAMPLES E1 byte-identical; RV-1…RV-5
PASS S-3a…S-3c (4)   E1d reading; EXAMPLES E1d byte-identical; E1b and E1e equal fixtures
PASS S-4             E1e reading
PASS S-5a, S-5b      E5 real bytes; declared-empty variant
PASS S-6a…S-6c       E6 real bytes; carriage; FB-22
PASS S-7 (33)        L-WDEX-18a…18e, 19a…19d, 20, 21a…21c, 22…28, 37, 38, 29…36, 42 (33a: "WD-v0.9" not established)
PASS S-8             invalid example read element by element
PASS S-9             node extract.mjs gives the same canonical JSON for E1
PASS S-10 (6)        workflow identity: 3 valid, 3 invalid
PASS S-11            10 names -> shell-command HCG-A02, file-change HCG-A03, web-search HCG-A10,
                     agent-delegation HCG-A08, mcp-tool-call HCG-A05, dynamic-tool-call HCG-A06,
                     person-input-request HCG-A07, image-view HCG-A11, image-generation HCG-A11,
                     plan-update HCG-A09; 27 groups read from HOSTING
62 checks, 62 passed, 0 failed
```

**DEL-09-06** — in `DEL-09-06/Design/`:
`python3 -B prototype/run_w14_rehearsals.py --out "$TMPDIR/fd-w14-final"`; exit 0.

```text
PASS w14-result-record.schema.json uses only the validator subset
case     phase      outcome      parts (passed/not run/failed)
W14-00   current    inconclusive 1/2/0
W14-01   current    not_run      0/1/0
W14-02   current    not_run      0/1/0
W14-03   current    inconclusive 2/2/0
W14-03   governance passed       1/0/0
W14-04   current    inconclusive 3/1/0
W14-04   governance inconclusive 1/2/0
W14-05   current    inconclusive 5/2/0
W14-06   current    inconclusive 3/3/0
W14-07   current    inconclusive 3/3/0
W14-08   current    not_run      0/1/0
W14-09   current    not_run      0/1/0
W14-10   current    not_run      0/1/0
PASS (39) per record: validates; no part failed; counts toward OUT-003: no
PASS every evidence limit is an RS R11 label in RS's spelling (2 distinct)
PASS every cited act names an actor different from its recorder
PASS w14-result-record.example.valid.json validates and equals the regenerated W14-05 record (date aside)
PASS w14-result-record.example.invalid.json is rejected (3 errors)
ALL CHECKS HOLD: 0 failure(s)     (44 PASS lines)
```

### Last runs (18:58 UTC), after parallel nodes changed shared inputs

Rerun after the round-2 / R20 edits (same commands, `--out
"$TMPDIR/fd-w14-final2"`). Each prototype now has **one failure, caused
outside this fence**; no WD, WD-EX or CA text is read by either check.

- **DEL-02-01: exit 1, 62 checks, 61 passed, 1 failed.**
  `FAIL S-11 … 10 names -> (same ten groups); 28 groups read from HOSTING;
  problems []`. HOSTING-BOUNDARY-v0.9 (working tree, sha256
  `4ae0cad41f024301dcfdd14ff0f6f6dc41faed452ebbf00314c9a570edb17e31`) added
  **HCG-A18 Goals** (G-3); `wdproto.py` line 662 requires `len(groups) == 27`.
  The mapping itself holds. Repair: the constant (or "≥ 27"), in DEL-02-01's
  prototype, outside this node's fence. **Returned.**
- **DEL-09-06: exit 1, "FAILED: 1 failure(s)".**
  `FAIL w14-result-record.example.valid.json validates and equals the
  regenerated W14-05 record (date aside)`. Structural diff of the example
  against the regenerated record: only `record_id`/`date` (expected) and
  `subject_of_run.files[4].sha256`, the pin of DEL-02-03's
  `prototype/run_all.py` (`42c0b496…` → `b770bb42…`), which F-B changed
  under R20-2. Outcomes and the twelve records are unchanged. Repair:
  `python3 -B prototype/run_w14_rehearsals.py --write-examples` once F-B's
  prototype is final (examples are outside this fence). **Returned.**

Both are recorded in WD §13.1 and CA §8.5.

## 8. UNRESOLVED / for the integrator

- §3 item 1 (contract value `WD-v0.8` at WD-v0.9) needs confirming.
- WD U-36 (new): declared chaining (R19-2 (c)), DEL-02-01's later work.
- The WR-v0.2 sections for the run-start framing and the L-4 additions do
  not exist yet; F-E fills the numbers.
- The CA W14 examples pin other prototypes' file digests; F-A…F-C are
  changing those prototypes in parallel, so a later rerun may need
  `--write-examples` (outside this fence).
