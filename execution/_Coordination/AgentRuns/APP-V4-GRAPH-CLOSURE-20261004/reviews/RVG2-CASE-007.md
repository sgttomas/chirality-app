# RVG2 review of SCC-CASE-007 (SCC-006, DEL-11-01 ↔ DEL-11-03) — APP-V4-GRAPH-CLOSURE-20261004

- **Reviewer:** RVG2, a second standing independent reviewer. Type 2 TASK executor, Claude Opus 5.5 (`claude-opus-5-5`), dispatched by HELP_HUMAN on 2026-10-04. No delegation. I authored none of the subject or its Designs. Read-only git, no network.
- **Subject** (committed at `cfce008835`, unchanged at HEAD `c5ca7ee0c9`), by design agent O-F:
  - `E/_DAG/cases/SCC-CASE-007/PAIR_ANALYSIS_2026-10-04.md`, sha256 `8f8dbb294c773e27717d54e21634b37521b3ff93f59a2d7e06addfc7a384aafa`;
  - `E/_DAG/cases/SCC-CASE-007/MOVES_PROPOSED_2026-10-04.csv`, sha256 `86d24752d13af9620703a7e8d3f214c094e3c0311f267d132e844254990bcd03`.
- **Question put by the coordinator.** Is DEP-11-03-015 only version feedback that DEL-11-01 can take from the owner's act record (its REQ-006), or does the account need DEL-11-03's disposition content?
- **Basis read:** as in `RVG2-CASE-006.md`. GC-5 postdates the subject and is applied as current basis.
- **Sources checked at their hashes (equal to the subject's §0):** DEL-11-01 and DEL-11-03 `ScopeOfWork.md` and `Dependencies.csv`; CA-v0.4 (`ea171162…`) and `ca.continuity-account.schema.json` (`b575dd4e…`); RP-v0.6 (`42eef807…`) and `rp.disposition.schema.json` (`d5a69bc2…`); `R23_RESOLUTIONS.md` (`21b2ccfa…`; F-R4, F-R5, F-R8 at l.413); `SURVEY/S2-F.md` (`ed1c20b0…`; F-R8 row l.382).
- **Scripts:** `$TMPDIR/rvg2/`.

## 1. What holds

- **Rows and quotes.** DEP-11-03-015, DEP-11-03-008 and mirror DEP-11-01-011 match DAG-004 and the live registers. All ScopeOfWork, CA and RP quotes in §1 occur at source. DEL-11-01's register has no UPSTREAM row to DEL-11-03 (checked: DEP-11-01-008…012), and CA's schema contains no `ALT-`, `presented_no_decision`, `not_presented` or `lapsed` (checked).
- **Kinds.** DEP-11-03-015 L (secondary E) and DEP-11-03-008 P follow G1 r3.
- **The correction to the assignment message is right.** SCC-006 exists under O-1 and O-2 only; under O-3 and O-4 the L row leaves (computed).
- **Closure arithmetic.** §6 reproduces: removing DEP-11-03-015 closes the pair under O-1 and O-2, and no G2 item touches the pair.
- **GC-4.** F-R8 is quoted correctly (R23-32 item 7, l.413; S2-F l.382 "no row change") and its amendment is assigned to HELP_HUMAN at application.
- **Projection verdict.** The part order CA vN → packet → owner act → CA vN+1 is real; the pair is version feedback at deliverable resolution.

## 2. Answer to the coordinator's question

**The account needs DEL-11-03's disposition content. The owner's act record does not carry it.** RP §6.2 and `rp.disposition.schema.json` give the disposition four things that an OWNER_DECISIONS entry does not:

1. **Whether the response is a decision, and on which alternative.** `decided` means "an attributable owner act chose one of the package's alternatives"; RP-R7: "A decided record names an alternative the package names"; RF-6: an ambiguous response stays `presented_no_decision` and "no alternative is ever inferred from the response". The alternatives (ALT-OWN-USE, ALT-PUBLISHED, ALT-DEFER, ALT-DECLINE) are RP §6.1's.
2. **The bound subject.** The package binds the act to `packet manifest sha256:<hex>` (RP §6.1 `subject[1]`), and the disposition carries `package_file.sha256`. DEL-11-03 OUT-003 assigns this binding to DEL-11-03 ("Bind the decision subject, evidence standing, owner's actual response and custody"). DEL-11-01 REQ-006 requires the act's "identified subject".
3. **Lapse.** "A package whose sha256 differs from the presented one makes the disposition *lapsed*" (RP-R7); "a decided disposition on it lapses" (RF-4). An owner record never changes when the package does.
4. **What the act does to v3.0.1.** The disposition's required `fallback_status` ("Plain statement of v3.0.1's standing after this record"), grounded in RP §6.1's column "v3.0.1 remains the fallback without a further act" (yes for all four alternatives; release is the separate P-5). DEL-11-01 needs exactly this: OUT-001 records "the retained v3.0.1 fallback"; REQ-001 keeps it "until the owner's replacement decision"; and CA's own preservation rests on OD-09, "Preserve the old projects and archives until I decide v4 has replaced the fallback."

So the return is version feedback in its timing, but not content DEL-11-01 can rebuild from its own sources. DEL-11-01 can avoid it only by re-applying RP's rules with RP's alternative set (a K-2 interface need on DEL-11-03, so an I row under GC-5 item 1), or by recording less. The rewording takes the second route (C7-M2).

## 3. Findings

### C7-M1 — MAJOR. M-01 leaves a residual on DEL-11-01 → DEL-11-03, so the component does not close under O-1 and O-2 without an owner act

- **Evidence.** §2 above. M-01's Residual reads "None that sequences", and §3 says the standing "never waits for" the disposition. Points 1, 3 and 4 are needed for a true `decided` standing and fallback statement in the next CA version; point 2 for REQ-006's identified subject. The subject's own §8 concedes point 2 ("If they do not, CA records the subject 'as the record states it'").
- **Kind of the residual.** It is needed "after an attributable owner act", and its condition governs the whole need, so L under K-6 with secondary E (as the current row). If CA re-applied RP-R7/RF-6 itself, the residual would instead be I (RP's alternatives and states).
- **Computed.** With DEP-11-03-015 kept as L: 2-cycle under O-1 and O-2, 1 row; absent under O-3 and O-4. As E: O-1…O-3. As I: every option.
- **Consequence.** §7's "O-1, O-2: no cut or merge" is not established. The smallest honest act under O-1/O-2 is M-02, the owner cut as version feedback, which is G1 r3 §2.6's candidate; under O-3/O-4 nothing is needed. F-R8's "no row change" then stays true.
- **Repair.** Present M-02 as the closing act under O-1/O-2 (or the option choice), with DEP-11-03-015 kept as a register obligation at its point of need. If M-01 is kept, record the L/E residual and the four content items it carries.

### C7-M2 — MAJOR. To make the return unnecessary, the rewording narrows DEL-11-01's own account. The design agent of CA is softening its own output

- **Evidence.**
  - Proposed CA §5: `fallback` "records what the act's own words say, or, where they say nothing about it, 'as the act states; see its record', and is never derived from the package's alternatives". An owner who answers "ALT-PUBLISHED" says nothing about the fallback, so CA would no longer state that v3.0.1 remains the fallback (RP §6.1: it does, until P-5).
  - §8: the subject is recorded "as the record states it" when the owner's words do not name the package.
  - Neither weakening is listed as a change to an output, and both reverse O-F's own CA-v0.4 §5 ("When DEL-11-03 returns an attributable disposition, the next account version records it (`decided`, with its reference)").
  - CA's own hand-over enum keeps "replacement decided; see disposition" (`$defs/continuity_handoff/replacement_standing`), so CA would still send its readers to the disposition it says it does not need.
- **Consequence.** The move would reduce DEL-11-01 OUT-001 ("recording the retained v3.0.1 fallback") and REQ-006 ("identified subject") to pointers, at the point OD-09's preservation condition turns. Restoring them inside DEL-11-01 would duplicate the subject binding DEL-11-03 OUT-003 assigns to DEL-11-03. The brief asks for moves that narrow no check and move no ownership; this one does the first and risks the second.
- **Repair.** Withdraw the CA §5 fallback and subject wording, or keep it only with M-02 (the cut), where CA can still record the disposition's content when it arrives.

### Minor findings

| ID | Severity | Finding | Evidence | Consequence |
|---|---|---|---|---|
| C7-m1 | MINOR | The S1 clause puts DEL-11-01's recording method into DEL-11-03's ScopeOfWork: "The App continuity owner records the owner's act from the act's own record; the disposition record is available to it by reference and is not an input to its account." A ScopeOfWork states its own deliverable's scope; DEL-11-01's method belongs in DEL-11-01's ScopeOfWork or Design. "Available to it by reference" also reads as a handover to DEL-11-01 | §3 item 1; DEL-11-03 CLM-003 already names DEL-11-01's ownership | If M-01 survives, confine the clause to what DEL-11-03 does |
| C7-m2 | MINOR | M-01 is labelled "invert by withdrawal (IV)". Nothing reverses and no contract is interposed; the move withdraws the return | §3 heading; CSV MoveCode `IV` | Present it as a withdrawal through an owner-accepted SCA (which §7 does), not as an agent-only refinement |

### Notes

| ID | Note |
|---|---|
| C7-n1 | The "continuing obligations" half of the return is plausibly DEL-11-01's own account flowing back (CLM-002; RP I-3 consumes CA's hand-over). I found nothing that contradicts §2 on that half |
| C7-n2 | DEP-11-03-016 (affected consumers) is unaffected; its EvidenceQuote would need a refresh, because the shared sentence changes |
| C7-n3 | The subject is candid that O-F wrote both Designs and the analysis (header; §8). The finding in C7-M2 is the kind of self-review risk it flags |

## 4. Verdict

**REPAIR.** Rows, kinds, the O-3 correction, the arithmetic and the GC-4 entry hold. The central premise does not: DEP-11-03-015 carries disposition content (decision on a named alternative, bound subject, lapse, fallback standing) that DEL-11-01 cannot take from the owner's act record. M-01 therefore either leaves an L/E residual (C7-M1) or narrows DEL-11-01's account (C7-M2). Under O-1/O-2 the closing act is the owner cut M-02; under O-3/O-4 nothing is needed.

**Counts.** BLOCKING 0, MAJOR 2, MINOR 2, NOTE 3.
