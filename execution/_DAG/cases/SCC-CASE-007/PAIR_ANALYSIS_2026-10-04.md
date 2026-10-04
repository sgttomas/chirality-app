# SCC-CASE-007 — pair analysis of SCC-006, DEL-11-01 ↔ DEL-11-03 (2026-10-04)

- **Standing.** Case evidence update under `workflows/scc-resolution-case`, written to `CASE_BRIEF_COMMON.md`. It is evidence for the owner's checkpoint, not a ruling. No row, register, ScopeOfWork, Design file, DAG version or existing case file is changed. Every move below is a **proposal**. Cut and merge are the owner's (`docs/CYCLE_DRIVEN_RESOLUTION.md` §2 rule 3). Any ScopeOfWork revision is applied by `scope-of-work` under an amendment the owner accepts. CaseState stays EVIDENCE_ACCUMULATING. The CP1-20260928 ruling carries forward unchanged.
- **Run.** `APP-V4-GRAPH-CLOSURE-20261004`. Author: design agent O-F, a Type 2 TASK agent (Claude Opus 5.5) dispatched by HELP_HUMAN, which does not delegate. O-F wrote both Designs this case concerns (DEL-11-01 CA, DEL-11-03 RP), so this is not an independent review of them. Branch `claude/app-v4-graph-closure`, HEAD `b459b4f2d1`. Only read-only git was used.
- **Paths.** `E/` is `projects/chirality-app-v4/execution/`. "Owner" means the person; agents are called agents.

## 0. Basis and checks

| File | sha256 |
|---|---|
| `E/_Coordination/AgentRuns/APP-V4-GRAPH-CLOSURE-20261004/CASE_BRIEF_COMMON.md` | `c83e0f86ca55c26ddc6abd2cfa817256fd6ed42f6013a926b72016825c703468` |
| `E/_Coordination/AgentRuns/APP-V4-GRAPH-CLOSURE-20261004/SURVEY/G1.md` (r3) | `3d6543bc2a05e5e62cb9673c1d3177386f484de38d9058a0b396eee9299f0a45` |
| `E/_Coordination/AgentRuns/APP-V4-GRAPH-CLOSURE-20261004/GC_RULINGS.md` | `27265cc9245fd7c2d93096dd8f2978376b51c48daf0e77fc110ced4c7c3318dc` |
| `E/_Coordination/AgentRuns/APP-V4-GRAPH-CLOSURE-20261004/reviews/RVG-G1.md` | `0dd4ae6dd491c9183736c7b3b3ecdb5124f42a73618ec7607ee82fe4e06f8257` |
| `E/_Coordination/AgentRuns/APP-V4-GRAPH-CLOSURE-20261004/reviews/RVG-C2.md` | `0736ec4cf9bf47d3a3a82eb40230b566403e8d98f85b77dae702cbc7377e6629` |
| `E/_DAG/cases/SCC-CASE-002/PAIR_ANALYSIS_2026-10-04.md` (method example) | `ad196971250aacb14f1eb5b8381549014615e23f606b06b96a7c8c44588f8250` |
| `E/_DAG/cases/SCC-CASE-002/MOVES_PROPOSED_2026-10-04.csv` (column set) | `c9bd426b90c2b54426c3321c673bfbfe1016596a484dcb2af2eec7187bba31c9` |
| `E/_DAG/DAG-004/CandidateEdges.csv` | `2bfff10e3094d7fd86da563006c965694563ec10d0fc78e9b1d9958fefa42025` |
| `E/_DAG/DAG-004/DependencyEdges.csv` | `c43033742df768a6fb493701d25b1d73240366172c05b1d0caa143650690966e` |
| `E/_DAG/DAG-004/ExcludedRows.csv` | `45f55e76ecf7c9aac3bd923838eee8c302d6b2776e4fa3c221e51f9cf465664e` |
| `docs/CYCLE_DRIVEN_RESOLUTION.md` | `bbd41a8d091c7fa81fce6462c1d5e976832e5879b6ab8c3c74147e2df55e514f` |
| DEL-11-01 `ScopeOfWork.md` | `272f76221dd429a52143e51ef4898ce290669b7be1d773a8fba3476282f04309` |
| DEL-11-03 `ScopeOfWork.md` | `0177354357b07ea177491cffc2b1c75ffac578e179ba96e63e91d6ba34dcf5b6` |
| DEL-11-01 `Design/CONTINUITY_ACCOUNT.md` (CA-v0.4) | `ea171162a236043ef625bf6716242e051240122a28195017034ff9a6abd84e64` |
| DEL-11-01 `Design/ca.continuity-account.schema.json` | `b575dd4e7c182e1d65b3370b32435638a5702d66a96ed9c6353f8612ed54dbfe` |
| DEL-11-03 `Design/REPLACEMENT_PACKET.md` (RP-v0.6) | `42eef807a5fbcecb256495b9f1a2e0797f97ed83c5b0142c7d733396106e3d02` |
| DEL-11-03 `Design/rp.disposition.schema.json` | `d5a69bc24d9ca346f4210c1a2ad9dee1407c6fb9f96af650f003258badbc99cf` |
| `E/_Coordination/AgentRuns/APP-V4-DESIGN-PASS-4-20261003/R23_RESOLUTIONS.md` (F-R8, l.413) | `21b2ccfa0f63d61671eddcebe5c2a41dccd2fc5f901e529808605bd017b3fc11` |
| `E/_Coordination/AgentRuns/APP-V4-DESIGN-PASS-4-20261003/SURVEY/S2-F.md` (F-R8 row) | `ed1c20b0999ab1dd730b486191393dec2ca8c7914491804f34fb79503c3dea62` |

**Checks run.** The script is a scratch file under `$TMPDIR`, not in the repository.

| Check | Result |
|---|---|
| Live fidelity | DEP-11-03-015 and DEP-11-03-008 equal their live register rows in every field. The DEL-11-03 register hashes to `96d3e9326705fc5d…`, its recorded `SourceRegisterSHA256`. The mirror DEP-11-01-011's register hashes to `523c702c824c0fd4…`, as `ExcludedRows.csv` records. Each `EvidenceQuote` occurs in the `ScopeOfWork.md` beside its register (whitespace, `` ` `` and `*` normalised) |
| Mirrors | DEP-11-01-011 is the mirror of DEP-11-03-008 (`ExcludedRows.csv`, SR-6). No row is represented by DEP-11-03-015 |
| Kinds | G1 r3's kinds, read from G1's own tables for all 212 arcs (129 admitted, 83 held). DEP-11-03-015 is L (L/E); DEP-11-03-008 is P |
| Baseline | Tarjan over all 212 arcs, filtered by option, reproduces G1 §1.3: 6, 4, 2 and 2 SCCs under O-1…O-4. **SCC-006 is present under O-1 and O-2 only.** Under O-3 and O-4 it is already absent, because DEP-11-03-015's primary kind L leaves the objective |
| Closure with the move | §6 |

**A correction to the assignment message.** The message says G1 r3 "finds the component persists under O-1…O-3". G1 r3 §1.3 lists O-3's remaining SCCs as "002 (12), 004 (3)", and my script agrees: SCC-006 persists under **O-1 and O-2**, not O-3. That is also the arithmetic G1's kind for DEP-11-03-015 (L, changed from E in r2; G1 §6) implies.

## 1. The reciprocal exchange

**Rows** (arcs read consumer → supplier).

| Row | Arc | Direction, type | EvidenceQuote | Statement | SourceRef | Kind (G1 r3) | Mirror |
|---|---|---|---|---|---|---|---|
| DEP-11-03-008 | DEL-11-03 → DEL-11-01 | UPSTREAM, PREREQUISITE | "remaining scope/evidence and the App DEL-11-01 continuity account." | "Consume the current App continuity account and continuing obligations in the exact owner replacement decision package." | DEL-11-03 SoW OUT-003 | P | DEP-11-01-011 |
| DEP-11-03-015 | DEL-11-01 → DEL-11-03 | DOWNSTREAM, HANDOVER (written by DEL-11-03, the supplier) | "returns the disposition and continuing obligations to the App continuity owner and affected consumers." | "Return the faithfully recorded later owner disposition and continuing obligations to the App continuity owner." | DEL-11-03 SoW Praxeology opening paragraph | L (secondary E) | — |

DEP-11-01-011 (DEL-11-01's own DOWNSTREAM row): "DEL-11-01 supplies continuity obligations and the continuing-obligation disposition account to the separately owned DEL-11-03 replacement evidence package." EvidenceQuote "supplies continuity obligations to `DEL-11-03`" (DEL-11-01 CLM-002).

DEP-11-03-015's Notes: "This is a later evidence handoff distinct from the upstream continuity account; it does not itself authorize consumer adoption or retirement."

**ScopeOfWork sentences.**
- DEL-11-03 OUT-003: "Exact owner replacement decision package and actual disposition record, presenting OUT-001 and OUT-002 distinctly, relevant practitioner observations, remaining scope/evidence and the App DEL-11-01 continuity account."
- DEL-11-03 Praxeology, opening paragraph: "The coordinator incorporates a later owner's response faithfully and returns the disposition and continuing obligations to the App continuity owner and affected consumers."
- DEL-11-01 CLM-002: "It consumes PKG-10 historical applicability and active-consumer maps, adoption status from `DEL-11-02`, and supplies continuity obligations to `DEL-11-03`."
- DEL-11-01 REQ-006: "A faithful record may report an actually performed adoption, retirement or replacement act with its actor, identified subject, scope, source and custody limits; the recorder is not the decision actor."
- DEL-11-01 REQ-005: "preparation of candidate replacement qualification and the owner's replacement decision under `DEL-11-03` remain with CLM-005."

**What the consumer side states.** DEL-11-01's ScopeOfWork names no input from DEL-11-03. CLM-002 lists what it consumes (PKG-10 maps, DEL-11-02's adoption status). Its register has no UPSTREAM row targeting DEL-11-03 (rows DEP-11-01-001…012 read). The arc DEL-11-01 → DEL-11-03 rests only on the supplier's DOWNSTREAM row, read from the supplier's "returns" clause. The original case datasheet records the same fact: "There is no matching 11-01 upstream local row."

**Design text, consumer side (DEL-11-01 CA-v0.4).**
- §2 O-2: "The owner's replacement disposition, returned | from DEL-11-03 | DEP-11-03-015, held | After an attributable owner act | Standing stays "pending; v3.0.1 retained"".
- §5: "**Replacement standing (F-R8, SCC-CASE-007 R1).** The standing is "pending" and "v3.0.1 retained", with no disposition reference. When DEL-11-03 returns an attributable disposition, the next account version records it (`decided`, with its reference). Even then the account retires nothing: P-4's acts remain separate."
- §5 also records owner acts directly from their records: OD-09 from `conceptual/DECISIONS.md` and "Direction item 2 of this run (OWNER_DECISIONS.md)", each with its exact text and `recorder_stated_by_record`.
- Schema `replacement_standing`: `state` (`pending`, `decided`), `fallback`, `disposition_ref` (string or null, **no pattern**); `pending` forces `fallback` "v3.0.1 retained" and a null reference. No DEL-11-03 field, state value or identity scheme appears in the schema (a scripted search finds no `ALT-`, `presented_no_decision`, `not_presented` or `lapsed`).

**Design text, supplier side (DEL-11-03 RP-v0.6).**
- §2 I-3: "Continuity hand-over (DEL-11-01 CA `$defs/continuity_handoff`; from RP-v0.4, replacing the first cut) | DEL-11-01 | DEP-11-03-008, held (SCC-006; F-R8: SCC-CASE-007 R1) | Packet assembly".
- §2 O-2: "Disposition record | DEL-11-01 and affected consumers | DEP-11-03-015 (held), DEP-11-03-016 | After an attributable owner act".
- §6.2: "The owner's act is recorded in the project's OWNER_DECISIONS form (F-R4), and the disposition references it." Its last RP-R7 bullet: "The disposition returns to DEL-11-01 as the next continuity-account version (SCC-CASE-007 R1)."
- §6.3 step 7: "Return the disposition to DEL-11-01 and the affected consumers."
- RP consumes CA's hand-over rule-bearingly: the packet repeats its thesis and archive results, and `check_rp.py` A-7 and A-21 validate and compare against DEL-11-01's `$defs/continuity_handoff`.

## 2. Real contradiction or projection artefact?

**Part order shown by both Designs.** CA version N (standing "pending") → packet assembled from CA N's hand-over → package presented → the owner's act, recorded in the OWNER_DECISIONS form → disposition `decided` → CA version N+1 records the act.

- The part of DEL-11-03 that DEL-11-01's return comes from (the disposition, RP §6.2) depends on CA version N.
- The part of DEL-11-01 that receives the return (the replacement standing of version N+1) is not the part DEL-11-03 consumed (version N's hand-over).

No part depends on itself through the other deliverable. **Verdict: projection artefact.** It is version feedback (CA N → packet → act → CA N+1) projected onto one node per deliverable, the pattern G1 names for SCC-005 and SCC-006 (§1.3, O-5 row).

**Which side can yield.**
- **DEP-11-03-008 is rule-bearing.** RP's validity depends on CA's values (RP §3.3; A-7, A-21; DEL-11-03 REQ-005, VER-005). Reversing it would move definitional ownership. Not proposed.
- **DEP-11-03-015's content is not DEL-11-03's.**
  - The disposition's substance is the **owner's act**. RP §6.2 already records it "in the project's OWNER_DECISIONS form (F-R4)", a project record whose recorder is HELP_HUMAN, not DEL-11-03. DEL-11-03's disposition record references that act.
  - DEL-11-01 already records owner acts **from their own records** (CA §5: OD-09, Direction item 2), as its REQ-006 allows ("A faithful record may report an actually performed … replacement act with its actor, identified subject, scope, source and custody limits").
  - The "continuing obligations" returned are DEL-11-01's own account (CLM-002: "supplies continuity obligations to `DEL-11-03`"), which flows the other way.
  - The consumer's ScopeOfWork already states no requirement for this input (RVG-C2 C2-M1 condition (c) holds on the consumer side today).

So DEP-11-03-015 is a carry-only return of content the consumer can read from its owner source. It can be withdrawn as a contract input without moving ownership.

## 3. The move (M-01): invert by withdrawal (IV), no ownership move

**Move.** Withdraw DEP-11-03-015 as a contract input of DEL-11-01. DEL-11-01 records the owner's replacement act faithfully **from the act's own record** (the OWNER_DECISIONS entry RP §6.2 already requires). It may cite DEL-11-03's disposition record by an uninterpreted identifier, resolved by DEL-11-03, but never needs it for its standing. DEP-11-03-008 stays as the sequencing row.

It needs three changes, each proposed here and applied by its own owner later:

**1. S1 ScopeOfWork wording, one clause** (DEL-11-03 Praxeology, opening paragraph; applied by `scope-of-work` under an owner-accepted SCA). Draft:
> The coordinator incorporates a later owner's response faithfully and returns the disposition and continuing obligations to affected consumers. The App continuity owner records the owner's act from the act's own record; the disposition record is available to it by reference and is not an input to its account.

- What it keeps: DEP-11-03-016 (affected consumers) is unchanged. DEL-11-03 still records the disposition (REQ-004, OUT-003, AC-004, VER-004), and DEL-11-01 still records owner acts (REQ-006, AC-006).
- **No OUT, AC, VER or ownership moves (S1).** DEL-11-01's ScopeOfWork needs no change.

**2. Design rewording, DEL-11-01 CA** (design agent O-F; reviewed):
- **§2, row O-2** becomes: "The owner's replacement act | the owner, through its record in the project's OWNER_DECISIONS form (F-R4) | none (an owner act, not a deliverable row) | After the act | Standing stays "pending; v3.0.1 retained"".
- **§5 "Replacement standing"** becomes: "When an attributable owner replacement act exists, the next account version records it faithfully from the act's own record (REQ-006), as OD-09 and Direction item 2 are recorded: exact text, actor, recorder as the record states it, custody, and `decided`. `disposition_ref` may hold DEL-11-03's disposition record identifier. It is an uninterpreted string: the account neither constructs, parses nor validates it, and compares it only whole. DEL-11-03 resolves it (GC-3). The standing never waits for it. `fallback` records what the act's own words say, or, where they say nothing about it, "as the act states; see its record", and is never derived from the package's alternatives. Even then the account retires nothing: P-4's acts remain separate."
- **§5 heading** citation "(F-R8, SCC-CASE-007 R1)" becomes "(F-R8 as amended; SCC-CASE-007 M-01)".

**3. Design rewording, DEL-11-03 RP** (design agent O-F; reviewed):
- **§2, row O-2:** "Other end" becomes "Affected consumers (DEP-11-03-016). DEL-11-01 records the owner's act from its own record and may cite this record by reference"; "Arc" becomes "DEP-11-03-016".
- **§6.2:** the last RP-R7 bullet becomes "DEL-11-01 records the owner's act from the act's own record in its next continuity-account version, and may cite this disposition by an uninterpreted identifier, which DEL-11-03 resolves (SCC-CASE-007 M-01)."
- **§6.3 step 7** becomes "Return the disposition to the affected consumers. The disposition is available to DEL-11-01 by reference."

**GC-1 and GC-3 test of the carried identifier (after the rewording).**

| Condition | Today | After the rewording |
|---|---|---|
| GC-1 (a) / GC-3 1: typed as an uninterpreted string, no supplier pattern, format, enumeration or structure | Holds: schema `disposition_ref` is `["string","null"]` with no pattern; no DEL-11-03 state value or alternative id in CA's schema | Holds |
| GC-3 1: not constructed, parsed or validated; whole-string equality only | Holds in the prototype (`build_ca.py` sets it to null; nothing reads it). Not stated in the Design | Stated |
| GC-3 1: the Design names the resolver (supplier or third party) | **Fails: not stated** | Holds: "DEL-11-03 resolves it" |
| GC-3 2: the rewording says the identifier is uninterpreted and names its resolver | — | Holds (the §5 text above) |
| GC-1 (b): conformance checked outside the consumer | Not applicable to the act: CA checks its own recording against the owner's record (K-9 rule: exact text in its record), not against DEL-11-03's. The disposition record's conformance is DEL-11-03's (RP-R7, `rp.disposition.schema.json`) | Same |
| RVG-C2 (c): the consumer's ScopeOfWork states no requirement | Holds already (DEL-11-01 CLM-002 names no DEL-11-03 input) | Holds |

**Residual.** None that sequences. The owner's record is not a deliverable, so it creates no arc. The optional disposition identifier is a citation, not a need; the standing is recorded without it. If a later revision made CA *require* the identifier, that would be an E row (runtime instance, CA-defined format), which sequences under O-1…O-3. The rewording forbids it.

**What the move does not do.**
- It does not change DEP-11-03-008, DEP-11-01-011, DEP-11-03-013, -014 or -016.
- It moves no ScopeOfWork-assigned ownership: DEL-11-03 keeps the disposition record (REQ-004), DEL-11-01 keeps faithful recording (REQ-006), and the owner keeps the decision (CLM-005).
- It changes no built record: CA-1 v3's standing is `pending` with a null reference, and FX-RP1-6's disposition is `not_presented`.

## 4. Integrator rulings the move would amend (GC-4)

| Ruling | Text | Effect | Who amends |
|---|---|---|---|
| R23-32 **F-R8** (`APP-V4-DESIGN-PASS-4-20261003/R23_RESOLUTIONS.md` l.413: "SCC-006 is treated by SCC-CASE-007 R1 for design"; S2-F §E2 row: "SCC-CASE-007 R1: versioned account → package → disposition → next version; "replacement pending" until then; no row change") | Amended | The sequence becomes "versioned account → package → **the owner's act (OWNER_DECISIONS)** → next version"; "no row change" no longer holds, because DEP-11-03-015 is re-resolved after the S1 wording | HELP_HUMAN, at application, listed in the owner-facing checkpoint (GC-4 item 2) |
| R23-43 (the packet may be put to the owner at any time) | Not affected | — | — |
| CP1-20260928 (owner's basis ruling) | Not amended. It records no cut or merge and does not bar later rulings (G1 §1.3) | — | — |

## 5. Fallback (M-02): owner cut, only if M-01 is not accepted

If the S1 wording is not accepted, or the register owner's re-extraction still yields a DEL-11-01-targeted row:
- **Under O-1 and O-2:** an owner **cut** of DEP-11-03-015 as version feedback (G1 §2.6's candidate; RVG-G1 G1-m6's reading for the SCC-005 analogue). It covers no mirror rows.
- **Under O-3 and O-4:** no act is needed; the row already leaves the objective as L.

## 6. Closure under O-1…O-4 (G1 r3 kinds)

Script: Tarjan over all 212 DAG-004 arcs (admitted ∪ held; DOWNSTREAM reversed, as `dag_reach.py` reads them), filtered by each option's kinds, read from G1 r3's tables.

| Scenario | O-1 | O-2 | O-3 | O-4 |
|---|---|---|---|---|
| Baseline, no move | SCC-006 present (arcs -015, -008); 6 SCCs graph-wide | SCC-006 present; 4 SCCs | **SCC-006 absent** (-015 out as L); 2 SCCs (002, 004) | **SCC-006 absent**; 2 SCCs |
| **M-01** (DEP-11-03-015 withdrawn) | **Acyclic** for this pair; 5 SCCs remain graph-wide (none with DEL-11-01 or DEL-11-03) | **Acyclic**; 3 remain | Acyclic; 2 remain | Acyclic; 2 remain |
| M-02 (cut of -015) | Same as M-01 | Same as M-01 | No act needed | No act needed |
| Reversing -008 instead (not proposed) | Acyclic | Acyclic | Acyclic | Acyclic |

The last row shows only that either arc closes the 2-cycle (G1's two minimum sets). -008 is not proposed: it is rule-bearing, and moving it would move ownership (§2).

**What remains under each option after M-01:** nothing in this component. The graph-wide remainders (SCC-001…005 under O-1, and so on) are other cases'.

## 7. Summary

| Pair | Verdict | Smallest move | Owner acts needed |
|---|---|---|---|
| DEL-11-01 ↔ DEL-11-03 (DEP-11-03-015 / DEP-11-03-008) | **Projection artefact** (version feedback). The return carries the owner's act and DEL-11-01's own obligations, which DEL-11-01 can read from their sources | **M-01, IV** of DEP-11-03-015. This is one S1 clause in DEL-11-03's Praxeology, plus Design rewordings of CA §2 O-2 and §5 and RP §2 O-2, §6.2 and §6.3 by design agent O-F (GC-3 stated). F-R8 is amended by HELP_HUMAN (GC-4) | **O-1, O-2:** no cut or merge; only the owner's acceptance of the S1 wording through an SCA, as for SCC-002's moves. If declined: one cut (M-02). **O-3, O-4:** none; the component is already absent |

**Does the component close?** Under O-1 and O-2, yes with M-01 (or M-02). Under O-3 and O-4 it is already closed, and M-01 changes nothing there.

## 8. Not established

| Item | Why |
|---|---|
| That the register owner's re-extraction, after the S1 wording, yields no DEL-11-01-targeted row | `dependency-extract` was not run. The wording names DEL-11-01 only as reading the owner's own record, which I read as stating no requirement. If a row is still extracted, M-02 applies |
| That the owner's OWNER_DECISIONS entry will identify the decision subject (the package) | REQ-006 asks for the "identified subject". RP §6.2 requires the record and exact text, but not that the owner's words name the package. If they do not, CA records the subject "as the record states it", or cites the disposition identifier, which stays optional |
| Whether the owner accepts an SCA carrying one S1 clause for this pair alone, or batches it with other cases | An owner and HELP_HUMAN question |
| Independent review of the proposed rewordings | O-F designed both files and wrote this analysis. RVG or another reviewer should test M-01 against GC-1, GC-3 and RVG-C2's condition (c) |
| Kinds | G1 r3's, not re-decided. DEP-11-03-015's L/E boundary (G1 §5) decides only whether SCC-006 is present under O-3; M-01 removes the row under every reading |
