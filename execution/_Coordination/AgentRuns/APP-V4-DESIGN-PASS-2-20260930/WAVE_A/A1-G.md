# A1-G — GUIDE alignment and final re-pin: return

Node A1-G of run `APP-V4-DESIGN-PASS-2-20260930`, last in Wave A. One Type 2
TASK executor (Claude Code subagent; parent HELP_HUMAN). No delegation.
Read-only git; no network; scratch under `$TMPDIR/a1g/`. Working tree on
`d1a6d13e53` (clean at start).

**Read whole first:** `BRIEFS.md` ("Common rules", "A1 — alignment wave",
"A1-G"), `R9_RESOLUTIONS.md`, `R10_RESOLUTIONS.md`, `OWNER_DECISIONS.md`
(DECISION-K1), `WAVE_A/A3.md`, `SURVEY/S1-E.md` part D (D.1–D.8), and
GUIDE-v0.3 (sha256 `c36e2eef…2e64`, equal to S1-E's value). Also read: the
DEL-03-04 ScopeOfWork (`895f004e…`) and Dependencies.csv (`977d8712…`); the
amended requirement texts in `docs/`; `git diff 6e18505e3 HEAD --
docs/HOST_INTEGRATION.md` (§10 and §11 unchanged); SCA-V4-001 OWNER_ITEMS
O-4…O-6, O-9, O-10, O-13, O-17, O-25; RV-3 for DEL-03-04; V9/V9b and
V10/V10b (verdicts, scope, the GUIDE lines); `Open_Issues.csv` OI-001/OI-002;
DAG-003 `DependencyEdges.csv` and `HANDOFF_STATE.md` for rows 021…023; and in
the siblings, each passage GUIDE cites for a changed item (EXEC §2.1, §3.6,
§4.5 SP-6/SP-6F, §9.1 DEL-01-04 row, U-E1…U-E23; C §5.2 and V-CP1; ADAPTER
RD-2 and XF-25; LOOP NW-8, FX-C9, UNRESOLVED; PANEL PC-24; WD VC-11 and the
R10-10 rows; RS §4–§4.3, R15, L-13; ACT U-02, U-03, U-06). Each survey item
was checked against the current source before it was applied.

**Method.** Each edit replaced one exact passage and failed unless it occurred
exactly once (scripted). Version labels in §0 onward were replaced by a
bounded regex over the fourteen current labels (194 replacements; history
labels CA-v0.3 in F-11 and WD-v0.5 in G-11 left). History rows are unchanged.

## 1. Result

- **GUIDE:** DEL-03-04/GUIDE-v0.4, sha256
  **`40afb93ea9e77b70affe778038c9c0a281e05c8ab82c83455fa54d7069f8eb55`**
  (`git diff --numstat`: 262 added, 174 removed lines; most removals are
  matrix rows whose only change is sibling labels).
- **Pins:** 18/18 match after re-pin (3/18 before). Script and both outputs
  in §3.
- **Sibling citations:** 880 section/identifier citations in §0 onward checked
  against the siblings' Wave A text by script; the 7 flagged are GUIDE's own
  references read by the script as sibling ones (EXEC "(§2.14)" l.390; SPIKE
  "§2.11", "§0" l.688; RELAY "F-3", "F-11", "F-4" l.854; P "§2.15" l.897). All
  resolve. Header citations: every flagged one is GUIDE-own or in a history
  table.
- **Fence:** `git status --short` shows only `HOST_INTEGRATION_GUIDE.md`
  (M) before this return file was written; with it, the two fenced files.

## 2. Changes (item → location)

All are rows of GUIDE's new "Changes from v0.3" table.

| Item | Change | Location |
|---|---|---|
| R9-11; R9-3 | v0.3 → v0.4; "the current phase (Phase 1)" on first use | Header |
| R9-5; D.8 item 1 (D.1 pins 1, 2, 3, 5) | New v0.4 Basis line: HOST_INTEGRATION `d4331c39…` (was `08c8fc7d…`), PRD `bb6e786f…`, ARCHITECTURE `317d5789…`, EXAMINATION `471798bc…`, naming SCA-V4-001/002; SoW `895f004e…` (was `203c0928…`); register `977d8712…` rows 001…023 (was `b41eacd0…`, …020); `_REFERENCES.md` `1279ea22…` unchanged; `_DAG/_LATEST.md` `4d381ba4…` → DAG-003; OWNER_DECISIONS of all four predecessor runs and this run (`35d65463…`), OWNER_ITEMS `2b90eb4a…`; R1…R8 by file and sha256; R9 `a64e2415…`, R10 `ad3b6caa…`; BRIEFS `c201c6df…`; S1-E `e0e95522…`; A3 `dcb8e9e9…`; V9 `bbc3366d…`, V10 `ace8df79…`, RV-3 `2216a144…`; state `d1a6d13e53`. v0.3 basis bullets kept verbatim as history | Header Basis |
| R9-5; D.8 item 1 | 18-row table re-pinned by script; labels at Wave A; "Wave A re-pin" note | Header table; §4.5 |
| R9-1; K1-1; D.3; D.4 item 13 | R9-1 summary sentence; requester SETTLED by K1-1; recording required where the arrival is observed; "flagged…" and "first half" removed from live text | Header; §0; B-7; §2.0 row 6 |
| R9-2; R9-4 (O-25) | R8-11 item 2 restated; the D2 reading SETTLED; "declared checkpoints override autonomy" removed | §0; B-4; M6.4; HC-6.3 |
| R10-1 | Direct application: *proposal queued* checkpoint *not reached*; reached checkpoint *waiting* | M6.4; VC-G-03 |
| R9-4; R10-11 (O-10) | "DECISION-2 reading" → record-and-show SETTLED; per-turn detail INTEGRATION | B-6; M5.6; M9.7; HC-9.5 |
| R9-1/R9-4; D.3; D.4 items 15, 17 | V4-HOST-01/02, V4-ARC-11/12 cited as amended; M7.3 cites V4-ARC-11/12 by ID | Header; B-6; B-11; §2.0 row 7; M7.3; M7.9; HC-7.3; §4.3 SQ-30; UNRESOLVED |
| D.8 item 3 (D.3 V4-HI-70; D.6) | RS R15 added; R1–R14 → R1–R15 | M5.6; HC-5.5 |
| K1-2 | SP-6 (earlier act on current content counts, cited); SP-6F governance option; "prior act not counted" limited; U-E4 closed | §0; M5.3; M5.6; M8.4; VC-G-03; UNRESOLVED |
| K1-3 | Joint answer (EXEC §4.7 JA-1; ACT §4.3); ACT U-03 / RS U-07 closed | §0; §2.0 row 5; M5.5; M8.4; UNRESOLVED |
| K1-4 | Person identity SETTLED (EXEC CAP-8; U-E8 closed); act-control proposal sentence | M5.3; G-1 |
| K1-5 | Allow-list combination; N-OPEN-4 closed | Header; B-11; §2.0 row 7; M7.9; HC-7.7; UNRESOLVED |
| D.8 item 2 | CC-1…CC-11 rerun (§4 below); §4.2 rows 3, 4, 6, 7 quote the revised SoW; §2.13 TBD-001/002; gaps, findings and UNRESOLVED closed (§5 below); VC-G-06 | §2.13; §4; §6; UNRESOLVED; VC-G-06 |
| D.8 item 4; D.4 item 23; D.7 | RV-3 checker result and its rerun; V9/V9b, V10/V10b with scope | Header Receivers; CC-7; CC-10; F-9; UNRESOLVED |
| V6 m-6 (R9-8) | M8.1 default scoped (governance phase; R7-3; R10-10) | M8.1 |
| V6 m-7 (R9-8; R10-10) | Partition sentence follows EXEC-v0.5 §3.6 / WD-v0.7 §4.3.1; HS-5 row | Header note; §2.14 |
| R10-2 | "Constraint not carriable on this host" a record fact in either phase | §2.15 SW-5 |
| R10-5 (carried) | Note where GUIDE relies on RD-2 | §2.15 SW-2; CC-11 |
| R9-6 | Receivers rebuilt: no register row has DEL-03-04 as supplier (DEP-03-02-021 and DEP-04-01-024 are mirrors); suppliers by rows 005…009, 011…015, 021…023 | Header Receivers |
| R9-11; R10-11 | Body labels to Wave A; citations checked by script | Whole body |
| V9 N-7 (R9-8) | Record row for the V9 re-pin at `1650a5a06` (added to the v0.3 table, not the v0.2 one) | Changes from v0.3 |
| — | "post-R8" live references → Wave A | §0 table; §4 lead; F-1; F-15 |

## 3. Pin script and output

Row definition (GUIDE header): each row names a consumed input by short name,
contribution/version and **File** basename; the sha256 is computed from the
working-tree bytes after the other Design files are final for the pass and
before GUIDE's re-pin (GUIDE cannot pin itself); SWBPIPE's two files are pinned
as data. The script resolves each basename to exactly one path under
`projects/chirality-app-v4/execution` outside `_Coordination`.

```python
#!/usr/bin/env python3
"""GUIDE input-table pin check (node A1-G). Usage: pins.py [--write]
Reads the consumed-input table of HOST_INTEGRATION_GUIDE.md (rows '  | **Short** | version | `File` | sha256 |'),
resolves each File basename to exactly one path under projects/chirality-app-v4/execution
(excluding _Coordination), computes `shasum -a 256`, and compares (or, with --write, writes the value)."""
import re, subprocess, sys, os
ROOT='<repository root>/projects/chirality-app-v4/execution'
G=ROOT+'/PKG-03_Host capability and operation contracts/1_Working/DEL-03-04_Host boundary and integration guide/Design/HOST_INTEGRATION_GUIDE.md'
row=re.compile(r'^(  \| \*\*(?P<short>[A-Z-]+)\*\* \| (?P<ver>.*?) \| `(?P<file>[^`]+)` \| )(?P<sha>[0-9a-f]{64})( \|)$')
def locate(name):
    hits=[]
    for d,_,fs in os.walk(ROOT):
        if '/_Coordination' in d: continue
        if name in fs: hits.append(os.path.join(d,name))
    return hits
lines=open(G).read().split('\n'); out=[]; n=ok=0
for l in lines:
    m=row.match(l)
    if not m: out.append(l); continue
    n+=1; hits=locate(m['file'])
    if len(hits)!=1: print(f"{m['short']:8} {m['file']}: {len(hits)} paths — FAIL"); out.append(l); continue
    cur=subprocess.run(['shasum','-a','256',hits[0]],capture_output=True,text=True).stdout.split()[0]
    same=cur==m['sha']; ok+=same
    print(f"{m['short']:8} {m['file']:42} pinned {m['sha'][:16]}… current {cur[:16]}… {'match' if same else 'DIFFERS'}")
    out.append(m.group(1)+cur+' |' if '--write' in sys.argv else l)
if '--write' in sys.argv: open(G,'w').write('\n'.join(out))
print(f"rows {n}; match {ok}/{n}" + (" (before write)" if '--write' in sys.argv else ""))
```

**Run 1 (check, before re-pin):**

```
C        CATALOG_AND_READ_BASIS.md                  pinned 8282c003024e5470… current 45c5eb5b9c78ff58… DIFFERS
P        PROPOSAL_LIFECYCLE_AND_OUTCOMES.md         pinned 410fb289e16177e1… current 4321359c327e3f4c… DIFFERS
ADAPTER  ADAPTER_ENABLEMENT_AND_RECEIVING.md        pinned 6e13ab117271b125… current 45690943a4aeee41… DIFFERS
ACT      ACT_AND_POLICY_CONTRACT.md                 pinned 6889003e6c1c2dd6… current 828a9052edccda92… DIFFERS
AS       AUTONOMY_AND_STANDING_EXCHANGE.md          pinned 52d1341bb475f0a7… current 531e043ad9a7c9f6… DIFFERS
RS       RECORD_SEMANTICS.md                        pinned 96b1aeeb120be597… current 35d7457ea7bffa87… DIFFERS
WD       WORKFLOW_DECLARATION.md                    pinned 43a9962f025de384… current c5a496089a311c85… DIFFERS
WD-EX    EXAMPLES.md                                pinned 8d60ed7850e6935b… current 4f95cd9e057455de… DIFFERS
EXEC     EXECUTION_COMPATIBILITY.md                 pinned 092f248682447df7… current 8c162ecac661e01c… DIFFERS
LOOP     LOOP_RECEIVING_CONTRACT.md                 pinned 246f4636166c6725… current 75b4af0fb284e4f3… DIFFERS
PANEL    PANEL_RECEIVING_CONTRACT.md                pinned dd71e11dbe0d9872… current ee51210addd04670… DIFFERS
HOSTING  HOSTING_BOUNDARY.md                        pinned d11d4c574aa3c342… current 3cb686ee1cffe17a… DIFFERS
SPIKE    PIN_SPIKE_0.158.0.md                       pinned 0e090a4ca14e3ec3… current 0e090a4ca14e3ec3… match
CA       CONNECTED_ACTIVITY_CONTRACT.md             pinned 1a7e2ac993e327bf… current a7d19b7f34f9ae20… DIFFERS
RELAY    RELAY_QUESTIONS_SWBPIPE.md                 pinned c93f8cc52da81b5f… current ce7c9e57814d7848… DIFFERS
XT       EXTERNAL_TRACE_CASES.md                    pinned fde79bb3170c4508… current f383856b2915c0c7… DIFFERS
ANS      RELAY_ANSWERS_SWBPIPE.md                   pinned afb6e063e7e5dfcc… current afb6e063e7e5dfcc… match
FACTS    FACTS_SQ01_SQ32.md                         pinned 733fb88a701317be… current 733fb88a701317be… match
rows 18; match 3/18
```

Run 2 was `pins.py --write` (after the 15 version labels in the table were set
to the Wave A labels). **Run 3 (check, after all GUIDE edits, final bytes):**

```
C        CATALOG_AND_READ_BASIS.md                  pinned 45c5eb5b9c78ff58… current 45c5eb5b9c78ff58… match
P        PROPOSAL_LIFECYCLE_AND_OUTCOMES.md         pinned 4321359c327e3f4c… current 4321359c327e3f4c… match
ADAPTER  ADAPTER_ENABLEMENT_AND_RECEIVING.md        pinned 45690943a4aeee41… current 45690943a4aeee41… match
ACT      ACT_AND_POLICY_CONTRACT.md                 pinned 828a9052edccda92… current 828a9052edccda92… match
AS       AUTONOMY_AND_STANDING_EXCHANGE.md          pinned 531e043ad9a7c9f6… current 531e043ad9a7c9f6… match
RS       RECORD_SEMANTICS.md                        pinned 35d7457ea7bffa87… current 35d7457ea7bffa87… match
WD       WORKFLOW_DECLARATION.md                    pinned c5a496089a311c85… current c5a496089a311c85… match
WD-EX    EXAMPLES.md                                pinned 4f95cd9e057455de… current 4f95cd9e057455de… match
EXEC     EXECUTION_COMPATIBILITY.md                 pinned 8c162ecac661e01c… current 8c162ecac661e01c… match
LOOP     LOOP_RECEIVING_CONTRACT.md                 pinned 75b4af0fb284e4f3… current 75b4af0fb284e4f3… match
PANEL    PANEL_RECEIVING_CONTRACT.md                pinned ee51210addd04670… current ee51210addd04670… match
HOSTING  HOSTING_BOUNDARY.md                        pinned 3cb686ee1cffe17a… current 3cb686ee1cffe17a… match
SPIKE    PIN_SPIKE_0.158.0.md                       pinned 0e090a4ca14e3ec3… current 0e090a4ca14e3ec3… match
CA       CONNECTED_ACTIVITY_CONTRACT.md             pinned a7d19b7f34f9ae20… current a7d19b7f34f9ae20… match
RELAY    RELAY_QUESTIONS_SWBPIPE.md                 pinned ce7c9e57814d7848… current ce7c9e57814d7848… match
XT       EXTERNAL_TRACE_CASES.md                    pinned f383856b2915c0c7… current f383856b2915c0c7… match
ANS      RELAY_ANSWERS_SWBPIPE.md                   pinned afb6e063e7e5dfcc… current afb6e063e7e5dfcc… match
FACTS    FACTS_SQ01_SQ32.md                         pinned 733fb88a701317be… current 733fb88a701317be… match
rows 18; match 18/18
```

The 16 Design pins equal A3's reported hashes (ADAPTER and RELAY unchanged by
A3). Full values are in GUIDE's table.

## 4. CC-1…CC-11, old → new

| Check | v0.3 result | v0.4 result |
|---|---|---|
| CC-1 | pass 10/10 | pass 10/10; the map still has ten rows, four revised in wording by SCA-V4-001 |
| CC-2 | pass with limits (G-1, G-2; rows 6 and 7 SoW wording, G-12, G-6) | pass with limits (G-1, G-2 only); rows 3, 4, 6, 7 re-read in revised wording and quoted in table 4.2; no SoW wording conflicts with a line |
| CC-3 | pass 10/10 + HC-0 | same; HI §10 unchanged by SCA-V4-001 (git diff); HC-5.5 adds R15 |
| CC-4 | pass 32/32 | same (RELAY §0–§3 byte-identical per A1-E/A3) |
| CC-5 | pass | same (M7.9 still has no SQ) |
| CC-6 | pass; TBD-001/002 SoW text "still reads open" (F-5) | pass; TBD-003…009 literals compared with the SoW by script, all equal (TBD-006 carries both timings); TBD-001/002 revised, no owner or point of need named; `Open_Issues.csv` literals recorded; F-5 closed |
| CC-7 | pass; checker **not run** | pass; checker **run**: RV-3 status OK, 0 findings; rerun here (`check_boundary_owner_resolution.py … --json`): status OK, 1 checked, 0 not checkable, 0 without claim, report sha256 `72737740d8482d2ba7821d5aeed872b37df3faa118210f041fb84ba256ec3f58`, equal to RV-3's |
| CC-8 | pass 16/16 | pass 16/16; citations script-checked (§1) |
| CC-9 | pass (R4…R8) | pass (R4…R10 and DECISION-K1; §5 rows added) |
| CC-10 | pass (self-check); v0.3 not reviewed | pass (self-check); no requester other than the agent, no *performed* without the act; V9/V10 recorded; v0.4 not reviewed |
| CC-11 | 3 remain (G-6, G-7, G-12) | 0 between GUIDE and SoW/basis (G-6, G-7, G-12 closed); 1 between inputs carried to Wave B (R10-5: C §5.2 rule 1 vs ADAPTER RD-2) |

## 5. Items closed, each with its record

- **G-6** (SCA-V4-001 E-0304-04; O-5, O-6), **G-7** (E-0304-02, -03),
  **G-12** (E-0304-05; O-4). Rows kept, marked closed.
- **F-4 withdrawn:** rows DEP-03-04-021…023 in `977d8712…`, admitted in DAG-003
  as N-B9…N-B11 (O-13; C1 S-04-6). **F-5** (E-0304-01), **F-6** (with G-6, G-7),
  **F-16** (O-4, O-5, O-6) closed.
- **UNRESOLVED:** V4-WF-05 / SoW row 6 (S1-E l.786), V4-HOST-02 (l.788),
  V4-HOST-01 / V4-ARC-11 (l.791) closed; findings row (l.796) narrowed to
  F-12; the VER-007 part of l.797 closed; ACT U-03, EXEC U-E4 and LOOP
  N-OPEN-4 marked closed where GUIDE carries them (K1-3, K1-2, K1-5).
- S1-E D.4 NOW items 13, 15, 17, 22 (except F-12), 23, 24. V6 m-6, m-7; V9
  N-7; C1-B §4.2 and §4.5 (as recorded facts).

## 6. Not applied, with reason

1. **D.8 items 5 and 6** (matrix refresh for the other files' changes; naming
   the N-18/N-21/N-24/X-1 contributions; §3 order of use; reviewer action on
   *answered without evidence*): Wave B (node B8), outside this node.
2. **V6 m-1:** the "Changes from v0.2" row still reads "Unchanged against
   `2f42fba02`: … PANEL". It is a history row; left as it is.
3. **D.1 pin 10** (intake BRIEFS `3e33ba26…`, now `6f32809d…`): stays in the
   v0.3 basis bullets kept as history; v0.4 does not rely on that file.
4. **Pre-existing table defect, not fixed:** three rows of "Changes from v0.2"
   ("SWBPIPE answers revised", "R8-13 close", "V10 S-1…S-4") have three cells
   in a four-column table. History rows; left.
5. **D.6 receiver statements:** C, RS, LOOP and PANEL still name DEL-03-04 only
   in their headers. Their files are outside this fence (CA and XT now list
   DEL-03-04, A1-E).
6. **G-1 / D.4 item 25 (LATER):** only the K1-4 wording applied; nothing
   designed for DEL-01-04 or DEL-02-04.

## 7. R10 candidates

None new. The A3-returned CH-20 / WD-EX R-9b scope difference is not cited by
GUIDE. R10-5 is recorded as carried (CC-11; SW-2 note).

## 8. Proposed ScopeOfWork, register or basis items

None new from GUIDE. GUIDE G-1 cites A3's proposed DEL-01-04 item (K1-4).
Observation only: `Open_Issues.csv` OI-001/OI-002 keep the former owner and
point of need while the revised SoW TBD-001/002 name none; O-17 decided that
status stays OPEN, so nothing is proposed.

## 9. Wave B items found beyond the survey

- B3 (R10-5) will decide whether SW-2 and M3.1 change.
- WD's element for taking up SP-6F is undefined (A3 §3 item 3); M8.4 cites
  SP-6F and follows WD when it is defined.
- M5.6 names R15 but not the other R8 and R8-13 element additions (RS §4.2,
  §4.3); for the B8 matrix refresh.

## 10. Grep account (final bytes, case-insensitive)

| Phrase | Hits | Each hit |
|---|---|---|
| "flagged for the next accepted-basis update" | 1 | l.752 G-6, closed row, the "At v0.3:" text (history) |
| "first half" | 4 | l.90 "Changes from v0.2" R8-1 row (history); l.757 G-12 closed row "At v0.3"; l.803 §5 R8-1 row (record of the R8 application); l.852 F-16 closed row "At v0.3" |
| "second half" | 0 | — |
| "override autonomy" | 1 | l.61 "Changes from v0.3" row recording its removal |
| "act not performed" | 0 | — |
| "DECISION-2 reading" | 5 | l.63 and l.827 change / §5 rows recording the relabel; l.119 "Changes from v0.1" R5-4 row (history); l.251 B-6 and l.392 M9.7 in the SETTLED citation form "the DECISION-2 reading confirmed by the owner, OWNER_ITEMS O-10" (as ADAPTER) |
| "N-OPEN-4" | 6 | l.69 change row, l.256 B-11, l.272 §2.0 row 7, l.359 M7.9, l.831 §5 K1-5 row, l.883 UNRESOLVED: each says closed by DECISION-K1 K1-5 |

`git status --short` at the end: the two fenced files only.
