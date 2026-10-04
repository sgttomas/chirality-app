# RVG2 review of SCC-CASE-003 (SCC-003, DEL-01-06 ↔ DEL-09-01) — APP-V4-GRAPH-CLOSURE-20261004

- **Reviewer:** RVG2, a second standing independent reviewer. Type 2 TASK executor, Claude Opus 5.5 (`claude-opus-5-5`), dispatched by HELP_HUMAN on 2026-10-04. No delegation. I authored none of the subject or its Designs. Read-only git, no network.
- **Subject** (committed at `c9885b8f71`, unchanged at HEAD `c5ca7ee0c9`), by design agent O-B:
  - `E/_DAG/cases/SCC-CASE-003/PAIR_ANALYSIS_2026-10-04.md`, sha256 `2e2e7cc38a7392d5b459d222ad5fdf1dddba24c9edd66fc72017c9b8dfaf4de0`;
  - `E/_DAG/cases/SCC-CASE-003/MOVES_PROPOSED_2026-10-04.csv`, sha256 `07f106857b401872db99f0c9f791a89b7da6ca706564b7ffe6f32aab4cbd6e4f`.
- **Basis read:** as in `RVG2-CASE-006.md` (doctrine §2, common brief, GC-1…GC-5, G1 r3, RVG-C2 with addenda, `dependency-extract`). GC-5 postdates the subject and is applied as current basis.
- **Sources checked at their hashes (equal to the subject's §0):** DEL-09-01 `ScopeOfWork.md`, `Dependencies.csv`, EXP-v0.2 (`ff0187da…`); DEL-01-06 `ScopeOfWork.md`, `Dependencies.csv`, PKG-v0.2 (`0d8d14d2…`), `pkg.identity-record.schema.json` (`efb0de35…`); DEL-09-02 SQ (consumers of DEL-01-06's witness); R23-1, R23-13, R23-20, R23-33; `APP-V4-DESIGN-PASS-4-20261003/BRIEFS_AS_SENT.md` l.89.
- **Scripts:** `$TMPDIR/rvg2/` (`g.py`, `g2.py` with G1 §2b.1's design-stated items at their kinds, `q.py`).

## 1. What holds

- **Rows and quotes.** DEP-09-01-016 and DEP-09-01-021 match DAG-004 in Direction, Type, Statement, EQ and SourceRef. The EQ of DEP-09-01-021 is shared by 9 ACTIVE rows (DEP-09-01-021…029; checked), so K-1's Statement reading is right. DEL-01-06's register has no row naming DEL-09-01 (checked). Every Design and ScopeOfWork quote in §1–§2 occurs at source.
- **Kinds.** DEP-09-01-016 V (G1 r3 V/P; §3.2 case 6; RVG G1-m2) and DEP-09-01-021 I follow G1 r3.
- **Projection verdict.** EXP §10's order (support revision → witness → package → smoke; "M1 does not wait for M2 …") is quoted correctly and supports a projection artefact.
- **The move is a genuine invert.** Before: DEL-01-06 consumes EXP's record form (I, 01-06 → 09-01). After: DEL-09-01 maps DEL-01-06's own witness form (09-01 → 01-06, on the existing arc). The contract direction reverses, and no ScopeOfWork-assigned ownership moves: the witness stays DEL-01-06 OUT-003; EXP stays DEL-09-01's. GC-1 (a) holds in the strong form once `support_revision` and the EXP citations go; GC-1 (b) holds because DEL-09-01 checks conformance at mapping. R23-1 and R23-20 make HOSTING §9.3's labels and their meanings integrator-level, so DEL-01-06 can use them without DEL-09-01 (GC-5 item 2).
- **Withdrawal claim.** The S1 sentence removes DEL-01-06 from REQ-008's supply sentence. DEP-09-01-021 has no mirror, so under UPDATE it is unseen and RETIRED (`dependency-extract` Function 3; `checks.md` item 7). The receipt clause lands on the existing arc 09-01 → 01-06.
- **Closure.** Every cell of §4.2 reproduces from my code: on DAG-004, M3-01 or M3-02 closes O-1 and O-2…O-4 need no move; with all G2 items, 21 members under O-1 (both in), 20 with M3-02; with N08, N26 or N27 alone, 19 (both in), 18 with M3-02. The reading that M3-01 is sufficient under O-1 only while N08/N26/N27 stay unregistered or are inverted is correct, and DEL-09-01's membership in that case depends on those items' moves.
- **Owner acts.** The SCA acceptance and the conditional M3-02 cut are the owner's and are labelled so; M3-03 (decomposition) is correctly shown as not proposed. GC-4: I found no integrator ruling on the witness form; EXP §10 M1 came from a brief ("make SCC-003's R1 milestones concrete", BRIEFS_AS_SENT l.89), not a ruling.
- **No other consumer is affected.** DEL-09-02's SQ consumes the package and identity record only (I-6), not the witness.

## 2. Findings

| ID | Severity | Finding | Evidence | Consequence |
|---|---|---|---|---|
| C3-m1 | MINOR | "No check is removed, narrowed or bypassed" is overstated. Two DEL-01-06 checks leave DEL-01-06 and reappear at DEL-09-01's mapping: PKG-VC-03's expected result "as an EXP record" (EXP-schema conformance at write), and PKG §8's gate that N-2 automation is used only "once the tool version has passed EXP-DC-N2". After M3-01, an automation-operated witness without EXP-DC-N2 satisfies DEL-01-06's AC-003 and maps to `not-run` at DEL-09-01 (EXP F-5a). The check survives, but relocated and later | PKG-v0.2 §8, §11 PKG-VC-03; EXP F-5a (l.609); DEL-01-06 OUT-003 "usable by App PKG-09" | This is the relocation GC-1 (b) asks for, so the move stands. State it as a relocation, and say in PKG §8 how DEL-01-06 keeps OUT-003 "usable by App PKG-09" (for example a person-operated witness, or the risk stated) |
| C3-m2 | MINOR | The rewording list misses EXP uses in PKG that GC-5 item 3 would otherwise force into the ScopeOfWork as an I row 01-06 → 09-01, re-forming the cycle under every option: §6 PS-10 ("as EXP records citing the identity record … EXP outcome"); §8 "Outcome by EXP §3.1 (R23-20)" (cite R23-20 itself); the header's basis line "Examination support (SCC-003 M1): DEL-09-01 EXAMINATION_PROTOCOL.md"; §1's table row "DEL-09-01 support" | PKG-v0.2 l.35–36, l.99, l.364, l.451 | The intent is unambiguous and the rewording is not yet applied; add these to the list so the applied rewording is complete |
| C3-m3 | MINOR | M3-01 changes what the kept arc carries. Under the S1 sentence DEL-09-01 "maps" DEL-01-06's witness "in its own form", which needs DEL-01-06's record definition (K-2). A refreshed DEP-09-01-016, or a new same-arc row, then reads I/V, not V. The CSV Residual "None" omits this | §4.1 S1 sentence and "Register" paragraph; G1 K-5 last sentence | No effect on SCC-003's closure (computed: the 2-cycle needs DEP-09-01-021). It does mean (a) under O-2…O-4 the arc 09-01 → 01-06 now sequences where it previously left with V, and (b) M3-02's rationale "the only row whose kind makes a cut natural" is weaker after M3-01: the cut would remove an arc carrying an interface need. State both |

### Notes

| ID | Note |
|---|---|
| C3-n1 | K-5 sensitivity. DEP-09-01-016's SourceRef includes CLM-005, and K-5's letter makes a CLM in SourceRef primary P or I. G1 r3 reads CLM-005 as an allocation clause and keeps V; I follow G1. If it were read P, SCC-003 would persist under O-2…O-4 without a move; M3-01 still closes it under every option (computed). M3-01 is therefore robust to this reading; "optional under O-2…O-4" is not |
| C3-n2 | Self-review. O-B reverses its own EXP §10 M1 and PKG I-5 ("Those recorded without EXP form; not usable by PKG-09"), both written at HELP_HUMAN's request in pass 4, and says so (§4.4). The reversal relocates rather than removes checks (C3-m1); I found no softening beyond that |
| C3-n3 | The 3 rows the author's parser missed (DEP-02-01-020, -021, DEP-05-01-020) are I/R in G1, so the default I is right. My parser read all 212 |
| C3-n4 | GC-5 item 4: the "no row is added" conclusion is provisional until G2b reports |

## 3. Verdict

**READY.** The rows, quotes, kinds, invert, withdrawal claim, closure and conditional scenarios all hold, and the owner acts are complete and correctly attributed. The three minors should be applied when the rewordings are drafted: state the relocated checks, complete the PKG rewording list (otherwise GC-5 would bring the arc back), and record the kind change on DEP-09-01-016.

**Counts.** BLOCKING 0, MAJOR 0, MINOR 3, NOTE 4.
