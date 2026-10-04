# SCC-CASE-003 — pair analysis of DEL-01-06 ↔ DEL-09-01 (2026-10-04)

- **Standing.** This is a case evidence update under `workflows/scc-resolution-case`. It is evidence for the owner's checkpoint, not a ruling.
  - Nothing is changed by it: no row, register, ScopeOfWork, Design file, DAG version or existing case file.
  - Every move below is a **proposal**. Cut and merge are the owner's (`docs/CYCLE_DRIVEN_RESOLUTION.md` §2 rule 3).
  - Any ScopeOfWork revision is applied by `scope-of-work` under an amendment the owner accepts.
  - CaseState stays EVIDENCE_ACCUMULATING. The CP1-20260928 ruling carries forward unchanged.
- **Run.** `APP-V4-GRAPH-CLOSURE-20261004`, case brief `CASE_BRIEF_COMMON.md` (committed at `b459b4f2d1`).
  - Author: O-B, a Type 2 TASK agent (Claude Opus 5.5) dispatched by HELP_HUMAN. It does not delegate.
  - O-B is the design agent of both members' Design files: DEL-01-06 PKG-v0.2 and DEL-09-01 EXP-v0.2.
  - Branch `claude/app-v4-graph-closure`, read at HEAD `0c815a8cdf`. Read-only git; no network.
- **Paths.** `E/` is `projects/chirality-app-v4/execution/`.

## 0. Basis and checks

| File | sha256 |
|---|---|
| `docs/CYCLE_DRIVEN_RESOLUTION.md` | `bbd41a8d091c7fa81fce6462c1d5e976832e5879b6ab8c3c74147e2df55e514f` |
| `E/_DAG/DAG-004/CandidateEdges.csv` | `2bfff10e3094d7fd86da563006c965694563ec10d0fc78e9b1d9958fefa42025` |
| `E/_DAG/DAG-004/DependencyEdges.csv` | `c43033742df768a6fb493701d25b1d73240366172c05b1d0caa143650690966e` |
| `E/_DAG/DAG-004/ExcludedRows.csv` | `45f55e76ecf7c9aac3bd923838eee8c302d6b2776e4fa3c221e51f9cf465664e` |
| `E/_DAG/DAG-004/GRAPH_BASIS.md` | `21835c7be4b2d1c65f38dc492aee28f936a31bd5f58d7df9e3ba7cc48c1aad79` |
| `E/_Coordination/AgentRuns/APP-V4-GRAPH-CLOSURE-20261004/CASE_BRIEF_COMMON.md` | `c83e0f86ca55c26ddc6abd2cfa817256fd6ed42f6013a926b72016825c703468` |
| `…/GC_RULINGS.md` (GC-1…GC-4) | `27265cc9245fd7c2d93096dd8f2978376b51c48daf0e77fc110ced4c7c3318dc` |
| `…/SURVEY/G1.md` (r3; §2.3, §2b, §3) | `3d6543bc2a05e5e62cb9673c1d3177386f484de38d9058a0b396eee9299f0a45` |
| `…/SURVEY/G2.md` | `24cc2a6fcb00e466775647ce14590cb91914b6132aab6a441e79576c22efa87b` |
| DEL-09-01 `ScopeOfWork.md` / `Dependencies.csv` | `8e53669468bd5885739ceaeb633dc5a3b134a04f1bf862235d8d2272dd5f658a` / `96ea447bba37f1225d305569226e822123ab52d9aa2e2e5c8f48e5200e5352f9` |
| DEL-09-01 `Design/EXAMINATION_PROTOCOL.md` (EXP-v0.2, at HEAD) | `ff0187dafd9e1f0268a19f9266914bdba64f39e0c8befdcaf20d3da7a7206a93` |
| DEL-01-06 `ScopeOfWork.md` / `Dependencies.csv` | `08e30b97baeb06ae57b6166d6358f5c68ad1d934102df7ea094ce6cc57abd795` / `19c3eb3574e9bdf263cac37a4f7bb2ff0328fc239180c3f72c2e32c6d0037f86` |
| DEL-01-06 `Design/PACKAGING_AND_DISTRIBUTION.md` (PKG-v0.2, at HEAD) | `0d8d14d2ce08d859ec3b304f5c8c250afa7f0a6fe95eae3a61920f71d2a442b4` |
| DEL-01-06 `Design/pkg.identity-record.schema.json` | `efb0de357efc3cfc0a193a8ffdcb9b08d93908b99d51ece614c4c2d6b94e008a` |
| `E/_DAG/cases/SCC-CASE-003/Case_Datasheet.md` | `3e5277f6535597eb39e0a750dcb16d11712b738065ece2275b9b33b599a364e2` |
| Method example `E/_DAG/cases/SCC-CASE-002/PAIR_ANALYSIS_2026-10-04.md` | `ad196971250aacb14f1eb5b8381549014615e23f606b06b96a7c8c44588f8250` |

**Checks run.** All scripts are in `$TMPDIR/ob_scc003/close.py`, not in the repository.

| Check | Result |
|---|---|
| Live fidelity | DEP-09-01-016 and DEP-09-01-021 in `CandidateEdges.csv` equal their live register rows in every field (SCC-003, case `_DAG/cases/SCC-CASE-003`). Both `EvidenceQuote`s occur verbatim in DEL-09-01's ScopeOfWork |
| Mirrors | Neither row has a mirror or same-arc row (G1 §2.3; `ExcludedRows.csv`). DEL-01-06's register has no row naming DEL-09-01 |
| Baseline | Tarjan over all 212 DAG-004 arcs, with G1 r3's kinds parsed from G1's tables (209 of 212; the 3 unparsed are SCC-002 rows, defaulted to I). It reproduces G1 §1.3: O-1 gives 6 SCCs including {01-06, 09-01}; O-2 gives 4 and O-3/O-4 give 2, none with 01-06 or 09-01 |
| G2 items | With G1 §2b.1's design-stated items added at their kinds, it reproduces G1 §2b.2: O-1 21 members; O-2…O-4 17; 16 without N26/N27 |
| Closure with moves | §4 |

## 1. The reciprocal exchange (brief step 1)

Arcs read consumer → supplier.

| Row | Arc | Direction / type | EvidenceQuote | Statement | ScopeOfWork sentence | G1 r3 kind |
|---|---|---|---|---|---|---|
| **DEP-09-01-016** | 09-01 → 01-06 | UPSTREAM PREREQUISITE | "Require identified packaging evidence from its owner before relying on that witness" | "Consume the actual targeted App package for native smoke examination and identified packaging evidence before relying on a packaged distribution witness." | DEL-09-01 TBD-001, OI-011 row, "Local consequence" column. SourceRef also VER-008 ("…the actual targeted packaged applications for native smoke checks") and CLM-005 | **V** (K-5: DEL-09-01's smoke verifies its own OUT-004 harness; RVG G1-m2 agrees) |
| **DEP-09-01-021** | 01-06 → 09-01 | DOWNSTREAM HANDOVER | "It supplies reusable support and evidence interfaces to those owners." (generic: shared verbatim by 9 rows of this register, so K-1 reads the Statement) | "Supply reusable examination support and evidence interfaces to the named owner of DEL-01-06 for its own scoped work." | DEL-09-01 REQ-008: "The harness shall perform no act owned by another deliverable: package production/distribution by `DEL-01-06`; … It supplies reusable support and evidence interfaces to those owners." | **I** |

**What the consumer side says.**
- DEL-01-06's ScopeOfWork has **no sentence that consumes DEL-09-01's support**. Its OUT-003 is a witness "usable by App PKG-09 without substituting for its joined checks". Its CLM-001 says "App PKG-09 consumes the packaged candidate for joined examination".
- So DEP-09-01-021 rests on one supplier-side sentence (REQ-008's generic offer to "those owners"). The consumption itself comes from DEL-01-06's Design (§2 below).

**Minimum.** 1 row; the minimum sets are {DEP-09-01-016} and {DEP-09-01-021} (G1 §2.3).

## 2. Current Design text on both sides (brief step 2)

**DEL-09-01, EXP-v0.2 §10** ("SCC-003 R1 milestones … made concrete"):
- M1: "This file's support revision (§4.4): schemas, rules, native-step form N-1, route identities | DEL-09-01 → DEL-01-06 (DEP-09-01-021) | … | DEL-01-06 writes its install/launch witness (its OUT-003) as an EXP result record under that revision".
- M2: "A package and its OUT-002 identity record … with DEL-01-06's own install/launch witness | DEL-01-06 → DEL-09-01 (DEP-09-01-016)".
- M3: "EXP route `native_packaged` on that package | DEL-09-01 → journey owners and reviewer".
- Rules: "M1 does not wait for M2, and DEL-01-06's configuration work does not wait for M1 (no finish-before-start order)."
- Also §2.2 OUT-4 and OUT-6 list DEL-01-06 as receiver via DEP-09-01-021, and the header lists "DEL-01-06 (held, SCC-003)" among receivers.

**DEL-01-06, PKG-v0.2:**
- §4.2 I-5: "Examination support | DEL-09-01 → here | DEP-09-01-021, held (SCC-003 M1) | EXP result record for FP-2, FP-4, FP-5 and the witness (§7, §8)".
- §7.1: "FP-2, FP-4, FP-5 and the witness run on the finished package and are EXP result records (`run_basis: candidate`, packaged subject citing the identity record, `route: native_packaged`; EXP-R2)."
- §8: "Written as a DEL-09-01 EXP result record (SCC-003 M1) … N-1 person-operated with the native-step form (EXP §8.2), or N-2 UI automation once the tool version has passed EXP-DC-N2 on this candidate (EXP §8.3)."
- §5.3: "As EXP §8.4: files, no service … its EXP records (FP-2, FP-4, FP-5, the witness) go under `Evidence/EXP/<candidate key>/` per EXP §8.4."
- `pkg.identity-record.schema.json`:
  - `support_revision` has `"pattern": "^EXP-v[0-9]+\\.[0-9]+$"` ("SCC-003 M1: the DEL-09-01 revision the witness records use");
  - the check outcome is described as "EXP / HOSTING §9.3 labels".

## 3. Verdict: projection artefact (brief step 3)

**Part order.** The Designs order the parts with no internal dependency running back:
1. DEL-09-01's support revision (EXP schemas, rules, routes). It needs nothing from DEL-01-06: "M1 does not wait for M2".
2. Then DEL-01-06's witness records, which use that support.
3. Then the package and identity record (M2).
4. Then DEL-09-01's native packaged smoke (M3), the only part of DEL-09-01 that needs the package (VER-008).

**Inside each deliverable.**
- DEL-09-01's support does not depend on its smoke.
- DEL-01-06's package does not depend on the form its witness record takes.

**Conclusion.** The deliverable-level 2-cycle is a projection of the order *support → witness form → package → smoke*. It is not a real ordering contradiction.

**Why it still closes a cycle at deliverable level.** O-1 keeps every kind, including V. Under O-1 both rows sequence:
- DEL-09-01 needs the package before its smoke (V);
- DEL-01-06 needs EXP's form before its witness (I).

Under O-2…O-4, DEP-09-01-016 leaves with the V class, and the component dissolves with no move (G1 §1.3; reproduced, §4).

## 4. The smallest move under O-1 that needs no owner cut (brief step 4)

### 4.1 Move M3-01: invert DEP-09-01-021 (IV; no ownership moves)

**The move.** Withdraw DEP-09-01-021 as a contract input. DEL-01-06 records its install/launch witness and its first-package checks FP-2, FP-4 and FP-5 in **its own** identity record, not in DEL-09-01's EXP record form. DEL-09-01 receives that witness through the arc that already exists (DEP-09-01-016, "identified packaging evidence"), maps it into an EXP record when it relies on it, and applies its own checks then. Ownership is unchanged:
- the witness remains DEL-01-06's OUT-003;
- the support and its checks remain DEL-09-01's OUT-001…004.

**Why this is an invert in SCC-CASE-002's sense (§1, code IV).**
- The contract stays with the owner its ScopeOfWork names.
- The withdrawn row's content is owned by the consumer: the witness is DEL-01-06's OUT-003.
- The reverse arc already exists and carries the witness the other way.
- The remaining edge is DEL-09-01 → DEL-01-06 only.

**Design rewordings (step (i); design agent: O-B, who designs both files; each is reviewed).**

| File | Section | Rewording |
|---|---|---|
| DEL-01-06 `PACKAGING_AND_DISTRIBUTION.md` | §4.2 I-5 | Withdraw the row. DEL-01-06 receives nothing from DEL-09-01 |
| | §7.1 | FP-2, FP-4, FP-5 become identity-record elements, like FP-0, FP-1 and FP-3 |
| | §8 | The witness is DEL-01-06's own record. Steps W-0…W-6 are kept with: quarantine evidence; the WKWebView/WebKit and OS identity; the operator (a person, or an automation tool and its version); outcome by recorded cause (§7.3). EXP §8.2/§8.3 are no longer cited |
| | §5.3 | Placement stated on its own terms, without "As EXP §8.4" |
| | §11 PKG-VC-03 | Expected: "a DEL-01-06 witness record", not "an EXP record" |
| DEL-01-06 `pkg.identity-record.schema.json` | `support_revision` | Removed. This also drops its `^EXP-v…` pattern, so GC-3 is not needed |
| | `first_package_checks` | Gains `fp2`, `fp4`, `fp5` and a `witness` element |
| | Check outcome | Described as HOSTING §9.3's labels only. They come from DEL-01-01, an existing admitted supplier (DEP-01-06-006); DEL-01-01 does not reach DEL-01-06, so no cycle |
| DEL-09-01 `EXAMINATION_PROTOCOL.md` | §10 | M1 is withdrawn as a contribution to DEL-01-06; M2 includes DEL-01-06's witness "in that deliverable's own form"; M3 maps it into an EXP record (route `native_packaged`, `package_record` = the identity record) and applies EXP-R2, the WKWebView requirement and, for an automation-operated witness, EXP-DC-N2 before relying on it |
| | §2.2 OUT-4, OUT-6; header "Receivers" | DEL-01-06 and DEP-09-01-021 removed |
| | §2.1 IN-5 | Names the witness in DEL-01-06's form |

**GC-1 and GC-3.**
- After the rewording, DEL-01-06's Design uses no field, state value or identity scheme that DEL-09-01 defines. That is GC-1 (a), in the strong form: nothing is carried by reference at all.
- Conformance of DEL-01-06's witness to EXP is checked outside DEL-01-06, by DEL-09-01 at its mapping. That is GC-1 (b).
- GC-3 is not relied on, because the `^EXP-v` identifier is removed rather than kept opaque.

**No check is removed, narrowed or bypassed.**
- Every element the EXP form required stays in DEL-01-06's witness record: candidate, package record, quarantine, WebKit identity, operator, outcome, cause.
- Every EXP check applies at DEL-09-01's mapping. An automation-operated witness without EXP-DC-N2 does not count when DEL-09-01 relies on it (EXP F-5a).
- DEL-01-06's AC-003 and DEL-09-01's VER-008 are unchanged.

**ScopeOfWork (S1, one sentence).** DEL-09-01 REQ-008, last-but-two sentence, "It supplies reusable support and evidence interfaces to those owners." becomes, for example:

> "It supplies reusable support and evidence interfaces to those owners other than `DEL-01-06`; from `DEL-01-06` it receives the package and packaging evidence, including that deliverable's install/launch witness in its own form, which this harness maps into its own records and checks before relying on it (VER-008)."

- No owner, OUT, AC or VER obligation moves.
- DEL-01-06's ScopeOfWork needs no change: it has no consuming sentence.
- It is applied by `scope-of-work` under the next owner-accepted amendment, the same one SCC-CASE-002's S1 wordings need. That acceptance is an owner act, but it is **not a cut or a merge**.

**Register.** `dependency-extract` UPDATE retires DEP-09-01-021, which has no mirror. It may refresh DEP-09-01-016's Statement to name the witness, on the same arc. DEP-01-06-006's Statement may also name HOSTING §9.3's labels, on the same admitted arc. No row is added.

**Effect on the graph.** It removes one held arc and adds none. DEL-01-06 then reaches only DEL-01-01 and DEL-01-05; DEL-09-01 reaches DEL-01-06, DEL-01-01 and DEL-01-05.

### 4.2 Closure under each option (brief step 6)

Computed with `$TMPDIR/ob_scc003/close.py` over DAG-004's 212 arcs with G1 r3's kinds. An option removes its kinds from all arcs (G1 §1.3).

| Basis | Option | Without a move | With M3-01 | With an owner cut of DEP-09-01-016 instead |
|---|---|---|---|---|
| DAG-004 rows (the case's basis) | O-1 | {01-06, 09-01} | **Acyclic** (neither in any SCC) | Acyclic |
| | O-2 | Acyclic | Acyclic | Acyclic |
| | O-3 | Acyclic | Acyclic | Acyclic |
| | O-4 | Acyclic | Acyclic | Acyclic |
| DAG-004 plus G1 §2b's design-stated items, if registered as G1 classes them | O-1 | Both in the 21-member component | **Both still in it** (21) | DEL-01-06 out; DEL-09-01 in (20) |
| | O-2…O-4 | Neither in any SCC | Neither | Neither |
| Plus N08 alone, or N26 alone | O-1 | Both in the 19-member component | Both still in it (19) | DEL-01-06 out; DEL-09-01 in (18) |

**Reading.**
- On the case's basis, M3-01 closes SCC-003 under O-1 and leaves it closed under O-2…O-4. Under O-2…O-4 no move is needed at all; M3-01 is then optional, a simplification.
- **The condition (an inference, from the computation).** M3-01 is sufficient under O-1 only while DEL-01-01 and DEL-01-05 stay outside SCC-002. G2's N08 brings in DEL-01-05; N26 and N27 bring in DEL-01-01 (G1 §2b.2 reading 1). If any of them becomes a row without its own inversion, then under O-1:
  - DEL-09-01 joins the large component through DEP-09-01-019 (P, to DEL-01-01) and DEP-09-09-012 / DEP-09-06-035 into DEL-09-01. **No SCC-003 move can change that.** It is closed only by those items' own moves (G1 §2b.1 proposes invert for all three) or by SCC-001's case.
  - DEL-01-06 then joins it only through DEP-09-01-016 (V). The smallest owner act that keeps DEL-01-06 out is the per-edge cut of that one row (§4.3).

### 4.3 If an owner act is needed: the smallest one

**M3-02 (conditional fallback): cut DEP-09-01-016.**
- Only under O-1.
- Only if N08, N26 or N27 enter the registers uninverted.
- One per-edge cut ruling, recorded in this case's `Ruling_Register.csv` and entering the next DAG version through SR-4. It needs no ScopeOfWork and no Design change.
- The row stays a register obligation at its point of need, "before relying on that witness" (VER-008). It is a witness input (V, K-5), the doctrine's "test" example of an out-of-objective edge.
- It is smaller than any decomposition or merge, and is the only row in SCC-003 whose kind makes a cut natural.

**Not proposed.**
- **Decomposing DEL-09-01 into support and native packaged smoke** (G1 §2.3's alternative). It needs `scope-change` and is larger than M3-01 or M3-02.
- **A merge.**
- **Rewording DEP-09-01-016 away under O-1.** It is DEL-09-01's own VER-008 need for the actual package. Removing it would narrow a check, which this assignment forbids without escalation.

### 4.4 Integrator rulings the moves would amend (brief step 5; GC-4)

None.
- R23-1 is unchanged: EXP still maps to HOSTING §9.3, and DEL-01-06 now uses those labels directly.
- R23-13 is unchanged: the N-1/N-2 route choice stays EXP's and governs DEL-09-01's reliance on the witness.
- R23-19, R23-20 and R23-21 are unchanged.
- CP1-20260928 is basis-only and is not amended.
- **Superseded, but not a ruling.** M3-01 supersedes, as a design proposal:
  - SCC-CASE-003's candidate remedy R1 ("coordinated contribution milestones"), as a graph treatment;
  - EXP §10's M1 row, which HELP_HUMAN asked O-B to "make concrete" in pass 4.

  Neither is a ruling. This case's existing files are not edited; the supersession is recorded here and in the moves file.

## 5. Summary

- **Pair verdict.** DEL-01-06 ↔ DEL-09-01 is a projection artefact. The parts order as support → witness → package → smoke (EXP §10).
- **Under O-1.**
  - The smallest move with no owner cut is **M3-01**: invert DEP-09-01-021 by two design rewordings (PKG, EXP; agent O-B) plus one S1 sentence in DEL-09-01 REQ-008 under the next owner-accepted amendment.
  - It closes SCC-003 on DAG-004's rows.
  - It stays sufficient while N08, N26 and N27 are not registered uninverted. Otherwise the owner cut of DEP-09-01-016 (M3-02) is the smallest owner act, and DEL-09-01's membership in the large component then depends on those items' own moves.
- **Under O-2, O-3 and O-4.** No move and no owner act is needed: DEP-09-01-016 leaves with the V class. M3-01 is optional.
- **Owner acts per option.**
  - O-1: the acceptance of the amendment that carries M3-01's S1 sentence (shared with SCC-002's), plus M3-02 only in the conditional case.
  - O-2…O-4: none for this case.

## 6. Not established

| Item | Why |
|---|---|
| Whether `dependency-extract`, on its own reading, would drop DEP-09-01-021 once DEL-01-06's Design no longer consumes EXP, without the S1 sentence | REQ-008 still offers support "to those owners", and the extraction recorded it as a positive handoff. The S1 sentence removes the doubt; a register-only route is the register owner's call |
| Whether HOSTING §9.3's labels fall within DEP-01-06-006's stated contribution ("the identified stock Codex binary and App hosting basis") | Read as within it. A Statement refresh is suggested on the same admitted arc |
| The 3 SCC-002 rows whose kind my parser did not find in G1 (DEP-02-01-020, -021, DEP-05-01-020) | Defaulted to I. They cannot affect SCC-003's members, which no SCC-002 arc reaches in DAG-004 (checked: no SCC contains 01-06 or 09-01 except their own) |
| Whether N08, N26 and N27 will be registered, and with what moves | Other cases and owners (G1 §2b) |
| The rewordings themselves | Proposed here, not applied. Each is a design-agent task with its own review |
