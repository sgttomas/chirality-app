# C1-A — bounded closeout comparisons: DEL-04-01, DEL-04-02, DEL-04-03, DEL-02-01, DEL-02-03

- Node: C1-A of run `APP-V4-FIRST-INCREMENT-20260928`. Executor: Type 2 TASK
  (Claude Code `Agent` subagent; does not delegate), dispatched by HELP_HUMAN.
- Method: `chirality-root:bundled:workflow:bounded-reconciliation`
  (`workflows/bounded-reconciliation/WORKFLOW.md`), applied as a read-only
  comparison under the C1 boundary decision in [BRIEFS.md](../BRIEFS.md) §C1
  (working copy, sha256 `c85c3519…0ee7b`). Its C1 section is identical to the
  C1 section committed at `d3cebd1cc`; the working copy adds only a later V4
  section.
- **Candidate:** commit `d3cebd1cc` (R5 final alignment). Every deliverable
  file below was read with `git show d3cebd1cc:<path>` into a private scratch
  folder. The two later commits on the branch (`816c917f0`, `c7f5513db`) touch
  only DEL-09-06 and DEL-03-04 files, so they do not change any input here.
- **Boundary (binding).** This closeout edits no ScopeOfWork.md,
  Dependencies.csv, `_DEPENDENCIES.md`, `_STATUS.md`, `_CONTEXT.md` or
  `_REFERENCES.md`. Every warranted change is returned below as a **proposed**
  change for the owning route in a successor undertaking. Nothing here is
  applied.
- Rulings applied: OWNER_DECISIONS DECISION-1 (D1–D4) and DECISION-2 (D5, D6)
  (sha256 `a9869129…8ad2c`); R1–R5 resolutions as amended.
- Findings sources: V1-A/B/C §register findings; IR1-A/B/C; V2; V3-A/B;
  R2_CANDIDATES X-16; the Design files' findings and UNRESOLVED sections
  (ACT §14; EXEC §11; WD change-table notes and §12; AS and RS UNRESOLVED and
  headers); W8 ADAPTER-v0.1 F-11 and W9 CA-v0.1 F-2 / XT-v0.1 F-2 where they
  name these five deliverables.

## Inputs at the candidate (sha256)

| DEL | ScopeOfWork.md | Dependencies.csv | Design file(s) |
|---|---|---|---|
| DEL-04-01 | `fc1a0503…f5e6` | `1cae4948…a133` | ACT_AND_POLICY_CONTRACT.md (ACT-POLICY-v0.5) `86975a90…80e7` |
| DEL-04-02 | `23a28caa…5e21` | `eb530369…b739` | AUTONOMY_AND_STANDING_EXCHANGE.md (AS-v0.5) `c49be8bb…29e1` |
| DEL-04-03 | `74d42c38…40c1` | `a44e67f4…34e9` | RECORD_SEMANTICS.md (RS-v0.5) `37bc586e…c27ea` |
| DEL-02-01 | `080d7f5a…a294` | `539520b4…5e96` | WORKFLOW_DECLARATION.md (WD-v0.5) `32acdd27…e7c9`; EXAMPLES.md (WD-EX-v0.5) `296875c9…702f` |
| DEL-02-03 | `9a921ba5…b7fb` | `be8c2c02…6f75` | EXECUTION_COMPATIBILITY.md (EXEC-v0.3) `889e4881…548e` |

Each SoW hash equals the hash cited in its Design header. `_DEPENDENCIES.md`
and `_STATUS.md` were also read. No SoW, register or `_DEPENDENCIES.md` file
of any deliverable differs between the DAG-001 dependency source
`85dcc17c3` and `d3cebd1cc`.

## Reading conventions

- **Status of an OUT/REQ** describes definition at the 60% level: *developed*
  (the definable content is present), *partially developed* (a definition
  element is still missing; what remains is named) or *not addressed*.
  Obligations that only implementation, a candidate run, host evidence
  (DEP-001) or a witness can meet are listed separately. They do not lower the
  status.
- **Arc classification** follows DAG-001 `GRAPH_BASIS.md`: canonical arcs are
  consumer → supplier; UPSTREAM rows are From → Target and DOWNSTREAM rows are
  Target → From; the consumer's UPSTREAM row is the representative (SR-6).
  Arc existence was computed over the ACTIVE EXECUTION deliverable-target
  rows of all 41 registers at `d3cebd1cc`.
  - *Mirror only*: the arc already exists through some row; the proposed row
    changes no topology.
  - *New arc*: no row establishes the arc. Adding it is a topology change and
    needs `project-dag` departure (DAG-002).
  - *Non-topological*: a row to an EXTERNAL target (OI, decision record,
    DEP-001), or a pointer update to an existing row. These do not affect
    topology but still move DAG-001 source currency because the registers are
    manifest-bound.
- Row IDs for proposed rows are assigned on application. The next free IDs are
  DEP-04-01-022, DEP-04-02-015, DEP-04-03-021, DEP-02-01-025 and
  DEP-02-03-022.
- SCC-002 (CASE-002) members: DEL-01-04, 02-01, 02-02, 02-03, 02-04, 03-01,
  03-02, 03-03, 04-02, 04-03, 05-01, 05-02 and 09-09. DEL-04-01 and DEL-09-06
  are outside it. DEL-01-01 is in SCC-001 with DEL-01-05.

---

## Summary

| DEL | OUT developed / partial / not addressed | Proposed SoW changes | Proposed register changes: mirror-only / new-arc (+ non-topological) | Lifecycle observation |
|---|---|---|---|---|
| DEL-04-01 | 2 / 1 / 0 (OUT-002 partial) | 10 | 6 / 1 (+2 pointer updates, +2 constraint rows) | INITIALIZED; IN_PROGRESS would be truthful |
| DEL-04-02 | 3 / 0 / 0 | 6 | 2 / 9 (+2 pointer updates, +2 constraint rows) | INITIALIZED; IN_PROGRESS would be truthful |
| DEL-04-03 | 3 / 1 / 0 (OUT-001 partial) | 4 | 10 / 6 (+1 pointer update) | INITIALIZED; IN_PROGRESS would be truthful |
| DEL-02-01 | 3 / 1 / 0 (OUT-002 partial) | 6 | 6 / 5 (+3 constraint rows) | INITIALIZED; IN_PROGRESS would be truthful |
| DEL-02-03 | 2 / 1 / 0 (OUT-001 partial) | 5 | 3 / 11 (+2 pointer updates, +1 constraint row) | INITIALIZED; IN_PROGRESS would be truthful |

New-arc counts are per register. The rows touch 32 arc incidences but only
28 distinct arcs, because four arcs join two C1-A deliverables (N-02, N-07,
N-13, N-17).

### Proposed new arcs (consumer → supplier), de-duplicated

"Rep. row" names the register that holds the representative UPSTREAM row.
The supplier's DOWNSTREAM mirror is optional. "Layer" gives the effect on
DAG-002: *held* means both endpoints are in SCC-002, so the arc goes to the
non-gating candidate layer and SCC membership is unchanged; *admitted* means
the arc does not close a cycle on the current graph.

| # | Consumer → supplier | Grounds | Rep. row | Layer |
|---|---|---|---|---|
| N-01 | DEL-04-02 → DEL-03-01 | V1-B RF-05; AS §8 temporal facet takes read basis from C §6.2 | DEL-04-02 (C1-A) | held |
| N-02 | DEL-04-02 → DEL-02-03 | AS §4 checkpoint overlay uses EXEC §3.6 hold-support values and §4 annotations; EXEC §9.2 row "DEL-05-02, DEL-04-02" | DEL-04-02 (C1-A) | held |
| N-03 | DEL-05-01 → DEL-04-02 | V1-A RF-05; V1-C RF-5/AB-04; X-16; LOOP carries the grant in force per dispatch (R-7, R-8) | DEL-05-01 (C1-C) | held |
| N-04 | DEL-05-02 → DEL-04-02 | V1-A RF-05; V1-C RF-4 (PANEL F-3); X-16; IR1-C §4 (DEL-05-02 row) | DEL-05-02 (C1-C) | held |
| N-05 | DEL-03-02 → DEL-04-02 | V1-B RF-06; P §13 expects the grant in force and during-work changes | DEL-03-02 (C1-B) | held |
| N-06 | DEL-03-03 → DEL-04-02 | W8 ADAPTER-v0.1 F-11 ("grant display"); AS U-15 | DEL-03-03 (C1-B) | held |
| N-07 | DEL-02-03 → DEL-04-02 | EXEC §9.1 AS row (grant display states for §4.10); AS U-15 | DEL-02-03 (C1-A) | held |
| N-08 | DEL-09-06 → DEL-04-02 | W9 CA-v0.1 F-2 | DEL-09-06 (C1-C) | admitted, unless C1-C's XT F-2 arc DEL-09-09 → DEL-09-06 is also added (see note) |
| N-09 | DEL-09-09 → DEL-04-02 | W9 XT-v0.1 F-2 (IN-29 grant states) | DEL-09-09 (C1-C) | held |
| N-10 | DEL-04-03 → DEL-03-01 | V1-B RF-04; RS §7 L-1 takes the subject content identity and method designation from C | DEL-04-03 (C1-A) | held |
| N-11 | DEL-03-01 → DEL-04-03 | V1-B RF-03; C §6.2 consumes act records and lapse state. The only row is the package-level DEP-04-03-012 → PKG-03, which is non-topological | DEL-03-01 (C1-B) | held |
| N-12 | DEL-03-02 → DEL-04-03 | V1-B RF-03; P §4.1 consumes acceptance acts; same package row | DEL-03-02 (C1-B) | held |
| N-13 | DEL-04-03 → DEL-02-03 | EXEC §9.2 DEL-04-03 row; R4-10/R4-11 put EXEC-owned elements into RS R8, R11 and R14 | DEL-04-03 (C1-A) | held |
| N-14 | DEL-04-03 → DEL-03-03 | RS header: "By join (not registered): DEL-03-03"; RS §10 DEL-03-03 row; W8 F-11 | DEL-04-03 (C1-A) | held |
| N-15 | DEL-04-03 → DEL-01-01 | IR1A-19 (R13 fed only by DEL-01-01 in this increment); V1-C RF-6 (S-7); RS R3, R5 and R13 suppliers | DEL-04-03 (C1-A) | admitted. **Conditional:** the alternative is to let S-7 ride the existing DEL-01-01 → DEL-01-02 → DEL-04-03 chain once DEL-01-02 is in scope (V1-C RF-6) |
| N-16 | DEL-02-01 → DEL-01-01 | V1-C RF-7; WD U-08 (harness capability naming from the 0.158.0 inventory) | DEL-02-01 (C1-A) | admitted |
| N-17 | DEL-02-01 → DEL-02-03 | WD §8 "Expected from suppliers" DEL-02-03 row; R4-7, R4-8 and R5-1 make WD adopt EXEC-owned values | DEL-02-01 (C1-A) | held |
| N-18 | DEL-02-01 → DEL-03-02 | WD §8 DEL-03-02 row (P §9, change-item identity, item-left events, governing checkpoint constraint); R2-12, R2-14, R2-18 | DEL-02-01 (C1-A) | held |
| N-19 | DEL-09-06 → DEL-02-01 | W9 CA-v0.1 F-2 | DEL-09-06 (C1-C) | admitted (same note as N-08) |
| N-20 | DEL-03-03 → DEL-02-01 | W8 F-11 ("declarations") | DEL-03-03 (C1-B) | held |
| N-21 | DEL-02-03 → DEL-03-02 | EXEC §9.1 P row; §4.11 | DEL-02-03 (C1-A) | held |
| N-22 | DEL-02-03 → DEL-05-01 | EXEC §9.1 LOOP row (arrival observation, binding, host-loop hold support) | DEL-02-03 (C1-A) | held |
| N-23 | DEL-02-03 → DEL-01-01 | EXEC §9.1 HOSTING row (supplied guidance, per-turn destination, R9, HP-4 scope) | DEL-02-03 (C1-A) | admitted |
| N-24 | DEL-02-03 → DEL-03-03 | EXEC §9.1 ADAPTER row (carriage assurance, GC-1…GC-5, §7.7) | DEL-02-03 (C1-A) | held |
| N-25 | DEL-05-02 → DEL-02-03 | EXEC §9.2 provides PANEL the annotation, report and hold-support display meanings; PANEL W-5b/e/f/g were re-pointed to EXEC by R4-3, R4-4 and R4-6. **Conditional:** V1-C RF-4 had advised a row only if a shared checker were allocated; that advice predates the R4 re-pointing | DEL-05-02 (C1-C) | held |
| N-26 | DEL-09-09 → DEL-02-03 | W9 XT F-2 (IN-25 required-tool outcome and holds on X) | DEL-09-09 (C1-C) | held |
| N-27 | DEL-03-03 → DEL-02-03 | W8 F-11 ("hold, required-tool check") | DEL-03-03 (C1-B) | held |
| N-28 | DEL-09-06 → DEL-04-01 | W9 CA-v0.1 F-2 | DEL-09-06 (C1-C) | admitted (same note as N-08) |

**Note on DEL-09-06.** No SCC-002 member currently consumes DEL-09-06; its
only consumer is DEL-09-07. If C1-C proposes XT F-2's DEL-09-09 → DEL-09-06
together with any of N-08, N-19 or N-28, DEL-09-06 joins SCC-002. That is a
DAG-002 consequence to state explicitly at departure.

**Not proposed.** DEL-01-01 → DEL-04-01 (V1-A RF-03). The preferred repair was
adopted by R-10: D3 reaches DEL-01-01 through DECISION-1 itself, and
DEP-01-01-021/-022/-024 suffice. ACT §10.1 V-21 still lists DEL-01-01 as a
consumer, which is consistent as a meaning map but needs no register arc.
C1-B should confirm this from the DEL-01-01 side.

---

## DEL-04-01 — Operation-policy and human-act distinctions

### 1. Commitment → result

| SoW item | Design section(s) | Status | Remaining definition | Implementation / host / witness only |
|---|---|---|---|---|
| OUT-001 contract | §§1–7, §9, §11 | developed | — | Host enforcement evidence (DEP-001; U-04) |
| OUT-002 policy-class representation and decision→consumer map | §8.1–§8.4, §10 | **partially developed** | The consequence dimension of "by operation class and consequence" (U-02); operation-specific reserved additions and the first operation (U-01, OI-021); defaults for other consequential classes (U-06); concrete configuration representation and placement (U-12; OI-013/OI-014) | Host adoption of P-01…P-06 (DEP-001) |
| OUT-003 fixtures | §13 FX-01…FX-53; VC-001…VC-009 | developed (designed) | — | Candidate-bound runs; recorded grant and performed-act evidence (DEP-04-01-020/-021; U-05); host evidence |
| REQ-001 | §4, §5.3–§5.6 (W-h) | developed (consequence part via U-02) | U-02 | — |
| REQ-002 | §2.1–§2.6; §3 S3, S5, S11 | developed | — | FX-09/FX-20 positive cases need actual acts |
| REQ-003 | §3 S4; §9; FX-03/05/14/15 | developed | — | — |
| REQ-004 | §8.3 P-01…P-06; §8.4; §6 | developed | OI-021 additions held | Host naming and enforcement (U-04) |
| REQ-005 | §9; VC-005 | developed | — | — |
| REQ-006 | §7; §5.6; P-03 | developed | — | Host defaults and enforcement (DEP-001) |
| REQ-007 | §11 | developed | — | — |

### 2. Result → commitment (beyond or outside the SoW)

| Element | Authority | Note |
|---|---|---|
| A1–A14 canonical names, including A8–A14 (§2.1) | R-1 (INTEGRATION/DERIVED) | Extends the REQ-002 act list consistently |
| Act-declined and run-ended events (§2.3) | R2-5 | — |
| Capturing surfaces; never-evidence list; A13 locus (§2.6) | R4-12 (ADOPTED); R4-13 (PROPOSED) | F-15: A13 depends on a host enablement facility |
| Checkpoint rules in §4 (resume point, re-hold, capture after arrival, no resumption, hold support, carriage assurance) | R4-2…R4-6, R4-14, R5-1, R5-2; owned by DEL-02-01/DEL-02-03 | Carried by citation at the owner's standing (F-14). ACT is not their owner |
| Seven grant states (§5.4); two settings references | R-8, R2-6 | Shared with DEL-04-02 §3 |
| Treatment → runtime outcome map (§6) | R-3, R2-4 (INTEGRATION) | — |
| P-02 reserved operations; P-01a A10 reserved | DERIVED (R2-2; R-1) | F-3 |
| P-04 A14; P-05 acceptance constraint; P-06 no policy basis | D3 + INTEGRATION (R-2, R2-8); DERIVED (R-5); INTEGRATION (R2-1, R2-9) | P-06 reconciles with REQ-004 "not treated as permission" by R2-9 (propose confers nothing); open to owner revision |
| A13 *disabling* reserved | INTEGRATION (R2-3) | F-11: owner may confirm |
| V-10 model destination as a record/status element | SETTLED part "may flow, no gating" (DECISION-2 D5); recording and showing is INTEGRATION (DECISION-2 reading, R5-4) | — |

Unsupported additions: none found. Design residual (not a SoW matter): §8.1
still says "This revision is DEL-04-01/ACT-POLICY-v0.3", although the file is
v0.5. This is a stale self-citation for the next Design revision.

### 3. Proposed SoW corrections

| ID | Location | Current text (excerpt) | Proposed text | Grounds |
|---|---|---|---|---|
| SC-04-01-1 | Traceability table, SOW-179 row, "Local contribution" | "…for embedded and external agents; pending global list retained" | "…for embedded and external agents; first-increment reserved list adopted by `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2; operation-specific additions retained (OI-021)" | DECISION-1 D2; ACT §8.2, P-01; F-10 |
| SC-04-01-2 | CLM-002, append | (names DEL-02-01, 02-03, 03-01, 04-02, 04-03 only) | Add: "It also supplies policy meaning to App v4 `DEL-03-02`, `DEL-03-03`, `DEL-03-04`, `DEL-05-01`, `DEL-05-02` and `DEL-09-09`, each of which declares it upstream in its own register." | F-1; V1-A RF-02; ACT §10 V-01…V-14. This grounds the mirror rows in §4, because `_DEPENDENCIES.md` Run Notes say DEL-05-01/05-02 edges were not extracted for want of a positive CLM statement |
| SC-04-01-3 | CLM-004, last sentences | "S/DECISION_BRIEF.html#d3 explicitly leaves both choices open." | Keep, and add: "For the first increment's App/shared contracts, the owner ruled OI-001 and OI-002 in `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` (D2, D3; run folder `OWNER_DECISIONS.md`). Operation-specific additions remain with OI-021; the `Open_Issues.csv` rows are updated through their own route." | DECISION-1; OWNER_DECISIONS "Effects" (C1 reconciles pointers) |
| SC-04-01-4 | REQ-004, third sentence | "A concrete unruled operation shall await the applicable OI-001/OI-002 decision before dependent operation-policy production or permission-policy implementation;" | "A concrete unruled operation shall await its applicable decision (for the first increment: operation-specific additions under OI-021; the App/shared OI-001/OI-002 rulings are DECISION-1 D2/D3) before dependent operation-policy production or permission-policy implementation;" (rest unchanged) | Same; requirement meaning unchanged |
| SC-04-01-5 | AC-004 and VER-004 | AC-004: "unresolved operations identify the applicable OI-001/OI-002 decision, owner and point of need…"; VER-004: "For each unruled case, inspect the OI-001/OI-002 owner and point-of-need hold;" | Replace "OI-001/OI-002" with "open policy decision (OI-021 or a successor), with its". In VER-004, add a first clause: "compare adopted reserved-act cases with DECISION-1 D2 and its DERIVED extensions;" | F-10; ACT VC-004 |
| SC-04-01-6 | AC-007 and VER-007 | AC-007: "…supplies no inferred always-reserved list or classifier treatment."; VER-007: "Compare unresolved entries to OI-001/OI-002 and confirm they select neither a global list nor classifier behavior." | AC-007: "…supplies no reserved list or classifier treatment beyond the adopted DECISION-1 rulings." VER-007: "Compare carried values with DECISION-1 D2/D3 (and their labeled DERIVED/INTEGRATION extensions) and unresolved entries with OI-021 and the other open items; confirm none selects a value without a decision basis." | ACT §8.1 rules, VC-007 |
| SC-04-01-7 | AX-001, second sentence | "…do not resolve the questions explicitly retained in S/DECISION_BRIEF.html#d3 and OI-001/OI-002." | Append: "Those questions were subsequently ruled for the first increment by DECISION-1 D2/D3; the historical texts still do not supply values." | DECISION-1 |
| SC-04-01-8 | TBD-001 | "OI-001 remains OPEN: owner with App/SWB contract owners chooses always-reserved acts…" | "OI-001 — ruled for the first increment (App/shared contracts) by DECISION-1 D2: marking checked; accepting a proposal where the autonomy requires one; engineering approval; professional reliance; changing the grant or enabling external access. The host names and enforces its own list (V4-HI-30; DEP-001). Operation-specific additions remain OPEN under OI-021 (owner via the outside SWB session and App/shared owner; before the connected-activity SoW)." | DECISION-1 D2; ACT U-01 |
| SC-04-01-9 | TBD-002 | "OI-002 remains OPEN: owner with App/SWB contract owners distinguishes routine tool permissions…" | "OI-002 — ruled by DECISION-1 D3: in the App, routine tool-permission and sandbox modes (including classifier-based modes) remain the user's own Codex setting and never stand in for a reserved or professional act; hosts have no classifier permission mode in the first increment. No open part remains for the first increment." | DECISION-1 D3 |
| SC-04-01-10 | Axiology, new TBD-004 | — | "TBD-004 — App-side run holds are deferred by the owner to the SWBPIPE answer to relay SQ-02 (`APP-V4-FIRST-INCREMENT-20260928-DECISION-2` D6). Point of need: before any App-side checkpoint enforcement claim. App-only checkpoints are *not enforceable* in this increment whatever SQ-02 returns (R5-10); that is a separate owner follow-up. It limits the VER-001 checkpoint cases, not the policy meaning." | DECISION-2 D6; ACT F-16, U-D6 |

### 4. Proposed register changes (DEL-04-01 `Dependencies.csv`)

| Proposed row | Direction / type | Target | Mirrors | Class | Grounds |
|---|---|---|---|---|---|
| R-04-01-a | DOWNSTREAM / HANDOVER | DEL-03-02 | DEP-03-02-017 | mirror only | V1-A RF-02; F-1 |
| R-04-01-b | DOWNSTREAM / HANDOVER | DEL-05-01 | DEP-05-01-018 | mirror only | V1-A RF-02 |
| R-04-01-c | DOWNSTREAM / HANDOVER | DEL-05-02 | DEP-05-02-008 | mirror only | V1-A RF-02 |
| R-04-01-d | DOWNSTREAM / HANDOVER | DEL-03-03 | DEP-03-03-008 | mirror only | ACT header receivers; F-1 |
| R-04-01-e | DOWNSTREAM / HANDOVER | DEL-03-04 | DEP-03-04-011 | mirror only | F-1 |
| R-04-01-f | DOWNSTREAM / HANDOVER | DEL-09-09 | DEP-09-09-010 | mirror only | ACT header receivers; F-1 |
| R-04-01-g | DOWNSTREAM / HANDOVER | DEL-09-06 | — (N-28; representative row belongs in DEL-09-06, C1-C) | **new arc** | W9 CA F-2 |
| DEP-04-01-017 (update) | UPSTREAM / CONSTRAINT | OI-001 | — | non-topological pointer | Statement/Notes cite DECISION-1 D2 as the adopted first-increment decision. Retain the row for the OI-021 remainder or retarget it (owner route). SatisfactionStatus stays with the owning route; this record proposes no SATISFIED value |
| DEP-04-01-018 (update) | UPSTREAM / CONSTRAINT | OI-002 | — | non-topological pointer | Statement/Notes cite DECISION-1 D3 |
| R-04-01-h | UPSTREAM / CONSTRAINT | EXTERNAL OI-021 | — | non-topological | ACT U-01, §8.4; no OI-021 row exists |
| R-04-01-i | UPSTREAM / CONSTRAINT | EXTERNAL DECISION-2 D6 / relay SQ-02 | — | non-topological | ACT U-D6, V-26 |

Noted but not proposed now (consumers outside this undertaking, D1; all
mirror only): DEL-01-02 (DEP-01-02-021), DEL-01-04 (DEP-01-04-011), DEL-02-02
(DEP-02-02-016), DEL-06-02 (DEP-06-02-009), DEL-09-02 (DEP-09-02-018),
DEL-09-05 (DEP-09-05-009), DEL-09-12 (DEP-09-12-011) and DEL-10-03
(DEP-10-03-013). Together with the five existing and seven proposed rows,
this accounts for all 18 upstream-declared consumers named in F-1. RF-01
(DEL-04-03 → DEL-04-01) is proposed on the DEL-04-03 side below.

### 5. Open items

| Item | Owner | Point of need |
|---|---|---|
| OI-021 operation-specific additions; first operation (U-01) | Owner via the outside SWB session and App/shared owner | Before the connected-activity SoW |
| Consequence vocabulary (U-02) | DEL-04-01 with the host policy owner | Before class assignment in DEL-03-01 |
| Multi-row A4 purpose after partial lapse (U-03; carried by R4) | DEL-04-01 with the owner | At its point of need (the whole-scope re-request satisfies every option) |
| Relay questions U-04 (a)–(f), including SQ-02 | Host owner (DEP-001) | Before host act-recording integration, enforcement claims or external enablement |
| Recorded person grant; performed-act evidence (U-05) | The person | VER-001; VER-002 positive cases |
| Other consequential-class defaults (U-06) | Host policy owner | Before those classes are cataloged |
| Workflow registration as an act (U-08) | DEL-04-01 with DEL-02-02 (later, D1) | Before the DEL-02-02 definition |
| Representation placement (U-12) | App/shared owners (OI-013/OI-014) | Before production allocation |
| App-side run holds (U-D6); App-only checkpoints | Owner (DECISION-2 D6; SQ-02; separate D6 follow-up) | Before App-side enforcement claims |
| Counting prior acts vs capture after arrival (U-14; SP-6 cost F-17) | Owner | Before hold-machine fixtures run |
| A13 disabling as INTEGRATION (F-11); design-candidate approval name (F-2) | Owner; Domains increment | On owner review; before the Domains increment |
| `Open_Issues.csv` OI-001/OI-002 still OPEN (F-8) | Decomposition owner (owning route, not C1) | Before the next decomposition currency check |

### 6. Lifecycle observation

`_STATUS.md` records **INITIALIZED** (last updated 2026-09-27). Since then,
authorized agent production has run in this deliverable folder:
ACT-POLICY-v0.1…v0.5, with integration rulings and an owner decision applied.
IN_PROGRESS ("active human + agent work underway", docs/TYPES.md; SPEC §3
transition by Human or WORKING_ITEMS) would now be the truthful state. It is
not changed here.

---

## DEL-04-02 — Visible autonomy and result standing

### 1. Commitment → result

| SoW item | Design section(s) | Status | Remaining definition | Implementation / host / witness only |
|---|---|---|---|---|
| OUT-001 receiving components (CODE) | §2–§9 (behavior) | developed (definition) | — | Components; placement OI-014/OI-013 (U-08) |
| OUT-002 host control/origin/undo and receiving contract (DOC) | §2, §6, §7, §10, UNRESOLVED | developed | — | Host elements (U-04…U-07, U-12; DEP-001) |
| OUT-003 fixtures (TEST) | §11 F1–F19; VC-01…VC-16 | developed (designed) | — | Candidate runs; host evidence |
| REQ-001 | §3, §4, §5 | developed | Scope "consequence" slot waits on U-02 (DEL-04-01 owner) | — |
| REQ-002 | §5, §6 (M3) | developed | — | Executable M3 trace needs a candidate writer/reader (U-10) |
| REQ-003 | §7 | developed | — | Host origin, undo, later-check route, receipt (U-05, U-06) |
| REQ-004 | §8 | developed | — | — |
| REQ-005 | §9 | developed | — | — |
| REQ-006 | §0, §10, UNRESOLVED | developed | — | — |
| REQ-007 | §10 | developed | — | — |

### 2. Result → commitment

| Element | Authority | Note |
|---|---|---|
| Grant display states, including *requested by agent*, *set by person, not yet confirmed*, *effective (policy default)* and *refused (reason)* (§3) | R-8, R2-6 | — |
| Checkpoint overlay (§4): dispositions, re-hold, capture after arrival, A12 control relations, hold-support values | R-5, R2-5, R4-3…R4-6, R5-1, R5-3, R5-5 | The SoW asks only that the display not imply discharge (REQ-001); the richer overlay is ruled integration content |
| Consumption of DEL-03-02 outcome vocabulary and origin, and DEL-03-01 read basis (§7, §8) | R-7; V1-B | Outside SoW CLM-002 and source key U (SC-04-02-1/-2) |
| "Applied, then reversed by ⟨receipt⟩" (§7, §8) | R2-15 | — |
| Author identity *unverified* (§7) | R4-15 | — |
| F19 destination shown by DEL-03-03, not here | SETTLED D5 for "no gating"; INTEGRATION (DECISION-2 reading) for "record and show" (R5-4) | — |

Unsupported additions: none. EXEC F-23 suggests that DEL-04-02 may present an
SP-6 repeat A12 as "re-affirm current setting". That is presentation only and
not applied in AS-v0.5; it remains open with U-17.

### 3. Proposed SoW corrections

| ID | Location | Current text (excerpt) | Proposed text | Grounds |
|---|---|---|---|---|
| SC-04-02-1 | Source table, key **U** | "App v4 sibling contracts…: `DEL-04-01…/ScopeOfWork.md` and `DEL-04-03…/ScopeOfWork.md`" | Add `PKG-03…/DEL-03-01…/ScopeOfWork.md` and `PKG-03…/DEL-03-02…/ScopeOfWork.md`, and `PKG-02…/DEL-02-03…/ScopeOfWork.md` | V1-B RF-01, RF-05; AS §4, §7, §8 |
| SC-04-02-2 | CLM-002, last two sentences | "This deliverable consumes those policy and record contributions. Defined and independently checked contracts do not establish…" | Insert before "Defined…": "It also consumes App v4 `DEL-03-02` proposal/outcome and direct-application origin semantics, `DEL-03-01` read-basis and standing facets, and `DEL-02-03` hold-support values and checkpoint annotations. Its visible autonomy state is received by `DEL-05-01`, `DEL-05-02`, `DEL-03-02`, `DEL-03-03` and `DEL-02-03`." — **conditional on the SoW-level decision** V1-A RF-05 asks for (direct consumption vs routing through DEL-04-01/DEL-03-02). All four designs already consume directly, so direct consumption is the recommended option | V1-A RF-05; V1-B RF-06; V1-C RF-4/RF-5; X-16; IR1-C §4 |
| SC-04-02-3 | REQ-007, first sentence | "…defining/carrying adopted operation policy belongs to App `DEL-04-01`; producing the human-act/run-file format… belongs to App `DEL-04-03` (CLM-002)." | Add: "the checkpoint hold machine and its annotations belong to App `DEL-02-03` (host loops: `DEL-05-01` receiving); channel status and model-destination display belong to App `DEL-03-03`;" | AS §10 |
| SC-04-02-4 | AC-004 and VER-004 | AC-004: "Current, historical, checked, limited and lapsed result cases…"; VER-004: "Supply current, historical, checked, limited, content-lapsed…" | Replace "checked" with "host-checks-passed (each named check with its evaluated basis)" in both | R-4 label rule: unqualified "checked" is A4 only; AS §8 host-check facet |
| SC-04-02-5 | TBD-001 and TBD-002 | "OI-001, Reserved human acts, remains OPEN." / "OI-002, Classifier routine permissions, remains OPEN." | As SC-04-01-8 and SC-04-01-9 (DECISION-1 D2/D3 pointer; OI-021 remainder) | IR1A-20; AS §10 note |
| SC-04-02-6 | Axiology, new TBD-006 | — | "TBD-006 — App-side run holds deferred to SWBPIPE SQ-02 (DECISION-2 D6). The display shows the hold-support value and action during hold and never shows an unenforced hold as held. Point of need: before App-side hold fixtures." | DECISION-2 D6; AS U-16 |

### 4. Proposed register changes (DEL-04-02 `Dependencies.csv`)

| Proposed row | Direction / type | Target | Mirrors / arc | Class | Grounds |
|---|---|---|---|---|---|
| R-04-02-a | UPSTREAM / INTERFACE | DEL-03-02 | DEP-03-02-018 | mirror only | V1-B RF-01 |
| R-04-02-b | DOWNSTREAM / HANDOVER | DEL-03-04 | DEP-03-04-012 | mirror only | Found in this comparison; no reviewer raised it |
| R-04-02-c | UPSTREAM / INTERFACE | DEL-03-01 | N-01 | **new arc** | V1-B RF-05 |
| R-04-02-d | UPSTREAM / INTERFACE | DEL-02-03 | N-02 | **new arc** | AS §4; EXEC §9.2 |
| R-04-02-e | DOWNSTREAM / HANDOVER | DEL-05-01 | N-03 (rep. row in DEL-05-01) | **new arc** | V1-A RF-05; X-16 |
| R-04-02-f | DOWNSTREAM / HANDOVER | DEL-05-02 | N-04 (rep. row in DEL-05-02) | **new arc** | V1-A RF-05; X-16 |
| R-04-02-g | DOWNSTREAM / HANDOVER | DEL-03-02 | N-05 (rep. row in DEL-03-02) | **new arc** | V1-B RF-06 |
| R-04-02-h | DOWNSTREAM / HANDOVER | DEL-03-03 | N-06 (rep. row in DEL-03-03) | **new arc** | W8 F-11; AS U-15 |
| R-04-02-i | DOWNSTREAM / HANDOVER | DEL-02-03 | N-07 (rep. row in DEL-02-03) | **new arc** | EXEC §9.1; AS U-15 |
| R-04-02-j | DOWNSTREAM / HANDOVER | DEL-09-06 | N-08 (rep. row in DEL-09-06) | **new arc** | W9 CA F-2 |
| R-04-02-k | DOWNSTREAM / HANDOVER | DEL-09-09 | N-09 (rep. row in DEL-09-09) | **new arc** | W9 XT F-2 |
| DEP-04-02-011 / -012 (update) | UPSTREAM / CONSTRAINT | OI-001 / OI-002 | — | non-topological pointer | DECISION-1 D2/D3 (V1-A RF-04) |
| R-04-02-l | UPSTREAM / CONSTRAINT | EXTERNAL OI-021 | — | non-topological | AS U-01 |
| R-04-02-m | UPSTREAM / CONSTRAINT | EXTERNAL DECISION-2 D6 / SQ-02 | — | non-topological | AS U-16 |

AS U-15 names five pending receivers: DEL-03-02, DEL-05-01, DEL-05-02,
DEL-03-03 and DEL-02-03. All five are covered above (N-03…N-07).

### 5. Open items

| Item | Owner | Point of need |
|---|---|---|
| OI-021 (U-01); consequence vocabulary (U-02) | As DEL-04-01 | As DEL-04-01 |
| Host enforcement of *unconfirmed*, re-resolution at application, de-duplication (U-04); host origin, undo, later-check, receipt and resulting objects (U-05); settings version in force at application (U-06); capture-evidence reference (U-07); constraint receipt (U-12, SQ-02) | Host owner (DEP-001) | Before connected integration |
| Placement (U-08: OI-014, OI-013) | App/shared owners; shared contract owner with SWB implementation owner | Before allocation / boundary contracts |
| Record representation (U-10) | DEL-04-03 | Before writer implementation |
| App-side holds (U-16, D6) | Owner (SQ-02; separate D6 follow-up) | Before App-side hold fixtures |
| SP-6 vs prior acts; repeat-A12 cost and possible "re-affirm" presentation (U-17; EXEC F-23) | Owner, with DEL-02-01 and DEL-04-01 | Before hold-machine fixtures run |
| Caller identity verification (U-18) | App owner with host owner | Before origin conformance |
| Multi-row A4 purpose (U-19) | DEL-04-01 with the owner | At its point of need |
| SoW-level decision on direct consumption by DEL-05-01/05-02 (V1-A RF-05) | Owner of the DEL-04-02 SoW with the DEL-05-01/05-02 owners (successor undertaking) | Before SC-04-02-2 and N-03/N-04 are applied |

### 6. Lifecycle observation

INITIALIZED (2026-09-27). AS-v0.1…v0.5 is authorized production of OUT-002
and design for OUT-001/OUT-003. IN_PROGRESS would be truthful. Not changed.

---

## DEL-04-03 — Content-bound decisions and compact run records

### 1. Commitment → result

| SoW item | Design section(s) | Status | Remaining definition | Implementation / host / witness only |
|---|---|---|---|---|
| OUT-001 versioned format (CONFIG) and record-authority documentation | §2 OF-1…OF-9, §3, §4, §6, §7, §9 | **partially developed** | The semantics are complete. The CONFIG representation is outstanding: serialization, field names, identity algorithm, record-identity form and carriage manifest (U-04), and App record location (U-05). These are deliberately unselected under the brief | — |
| OUT-002 writer/reader and lapse handling (CODE) | §2, §5, §7 (L-rules), §8 | developed (definition) | — | Writer/reader; placement (U-16) |
| OUT-003 fixtures (TEST) | §12 E1–E12; VC-01…VC-28 | developed (designed) | — | Candidate runs; actual-act evidence (DEP-04-03-018) |
| OUT-004 interface documentation (DOC) | §10, §11, UNRESOLVED | developed | — | Host run recording (DEP-04-03-016/-017) |
| REQ-001 | §2 | developed | — | — |
| REQ-002 | §4 R1–R14; §5; §9 | developed | — | Host receipts and hashes (U-15) |
| REQ-003 | §3, §6 | developed | — | — |
| REQ-004 | §7 | developed | U-07 (multi-row A4 purpose); U-12 (return to c₀) | — |
| REQ-005 | §10 | developed (consumer set wider than the SoW; SC-04-03-1/-2) | — | Host adoption |
| REQ-006 | §11 | developed | — | — |

"Hashes" in REQ-002 is read as content identities with a method designation
(OF-3, R-6). This is consistent with the SoW, and no change is warranted.
REQ-004 is also consistent with R-6 (A5 is not lapsed by application) and
R2-7 (supersession of A12/A13 is a relation, not an edit or a lapse). No
change is warranted there either.

### 2. Result → commitment

| Element | Authority | Note |
|---|---|---|
| R1 *continues ⟨run⟩*; run finality (§3) | R4-4 (PROPOSED) | — |
| R2 trace and transfer links, revision verification, holding library | R2-20, R4-11 | — |
| R3 supplied-guidance identity | R-10, R2-20 | — |
| R5 model destination per turn, run-level set | SETTLED "no gating" (D5); record duty INTEGRATION (DECISION-2 reading, R4-1, R5-4) | SoW REQ-002 lists "model used" only (SC-04-03-3) |
| R5a seat role; R13 A14 settlements; R14 compatibility-report reference | R-7; D3 + R2-8; R4-11 | — |
| R8 subject class, hold support (four values), arrival/performance ordinals, annotations; R11 action during hold | R-5, R2-17, R3-1, R4-2, R4-10, R4-11, R5-1, R5-5, R5-8 | — |
| Act-declined, act-lapsed, run-resumed and run-ended record kinds (§3) | R2-5, R2-19, R4-3 | — |
| Consumers and suppliers beyond REQ-005 (§10): DEL-05-01, DEL-05-02, DEL-01-01, DEL-03-03, DEL-09-06; PKG-03 as a supplier | R-7, R-8, R-10; V1-B RF-02 | SC-04-03-1/-2 |

Unsupported additions: none. **Not applied in RS-v0.5:** EXEC F-24 proposes
that the R11 *action during hold* entry carry the turn initiator, so that a
person-directed turn (HP-4) is distinguishable from an unprompted agent
action. RS R11 has no initiator element. This is open work for the next RS
revision.

### 3. Proposed SoW corrections

| ID | Location | Current text (excerpt) | Proposed text | Grounds |
|---|---|---|---|---|
| SC-04-03-1 | CLM-004, second sentence | "PKG-02 workflow definitions/checkpoints, PKG-03 basis/receipts and PKG-06 decisions consume this format;" | Keep, and add a sentence: "This format receives act kinds and classes from App `DEL-04-01`, settings-in from `DEL-04-02`, subject content identities and method designations from `DEL-03-01`, operation outcomes, change-item content identities and receipt links from `DEL-03-02`, hold-machine events and compatibility reports from `DEL-02-03`, external dispatch entries from `DEL-03-03`, and observed supplier facts (supplied guidance, model and destination, tool-permission settlements) from `DEL-01-01`." | V1-A RF-01; V1-B RF-02, RF-04, RF-07; IR1A-19; RS §10; EXEC §9.2 |
| SC-04-03-2 | REQ-005, first sentence | "…identify how PKG-02 definitions/checkpoints, PKG-03 basis/receipts and PKG-06 decisions consume the record meaning…" | "…identify how PKG-02 definitions/checkpoints, PKG-03 basis/receipts, PKG-05 loop and panel receiving (`DEL-05-01`, `DEL-05-02`), PKG-06 decisions and the PKG-09 connected-activity and trace contracts (`DEL-09-06`, `DEL-09-09`) consume the record meaning…" | Existing UPSTREAM rows DEP-05-01-019, DEP-05-02-009, DEP-09-06-015 and DEP-09-09-011; RS §10 |
| SC-04-03-3 | REQ-002 inventory | "…host receipt references, actual human acts and model used." | "…host receipt references, actual human acts, and model used with its observed destination per turn." **Conditional:** the record duty is the recorder's INTEGRATION reading of DECISION-2 (R5-4), so the owner must confirm that reading before the SoW adopts it | DECISION-2 D5; R4-1; R5-4 |
| SC-04-03-4 | TBD-001 | "OI-001/OI-002 retain the exact always-reserved operation classes and classifier-permission policy with the owner and affected App/SWB contract owners." | "OI-001/OI-002 were ruled for the first increment by DECISION-1 D2/D3; DEL-04-01 carries them. Operation-specific additions remain open under OI-021 (owner via the outside SWB session and App/shared owner; before the connected-activity SoW)." (rest unchanged) | IR1A-20; RS §11 note |

### 4. Proposed register changes (DEL-04-03 `Dependencies.csv`)

| Proposed row | Direction / type | Target | Mirrors / arc | Class | Grounds |
|---|---|---|---|---|---|
| R-04-03-a | UPSTREAM / INTERFACE | DEL-04-01 | DEP-04-01-016 | mirror only | V1-A RF-01 |
| R-04-03-b | UPSTREAM / INTERFACE | DEL-03-02 | DEP-03-02-019 | mirror only | V1-B RF-02 |
| R-04-03-c | UPSTREAM / INTERFACE | DEL-04-02 (settings-in) | DEP-04-02-009 | mirror only | V1-B RF-07 |
| R-04-03-d | DOWNSTREAM / INTERFACE | DEL-02-01 | DEP-02-01-019 (today covered only by the package row DEP-04-03-011 → PKG-02) | mirror only | Deliverable-level split of the package row; DEP-04-03-011 may stay as a non-topological row |
| R-04-03-e | DOWNSTREAM / INTERFACE | DEL-02-03 | DEP-02-03-013 (same package row) | mirror only | As above |
| R-04-03-f | DOWNSTREAM / HANDOVER | DEL-05-01 | DEP-05-01-019 | mirror only | RS §10 |
| R-04-03-g | DOWNSTREAM / HANDOVER | DEL-05-02 | DEP-05-02-009 | mirror only | RS §10 |
| R-04-03-h | DOWNSTREAM / HANDOVER | DEL-09-06 | DEP-09-06-015 | mirror only | RS header ("DEL-09-06 (transfer links)") |
| R-04-03-i | DOWNSTREAM / HANDOVER | DEL-09-09 | DEP-09-09-011 | mirror only | — |
| R-04-03-j | DOWNSTREAM / HANDOVER | DEL-03-04 | DEP-03-04-013 | mirror only | — |
| R-04-03-k | UPSTREAM / INTERFACE | DEL-03-01 | N-10 | **new arc** | V1-B RF-04 |
| R-04-03-l | UPSTREAM / INTERFACE | DEL-02-03 | N-13 | **new arc** | EXEC §9.2; R4-10/R4-11 |
| R-04-03-m | UPSTREAM / INTERFACE | DEL-03-03 | N-14 | **new arc** | RS header; W8 F-11 |
| R-04-03-n | UPSTREAM / INTERFACE | DEL-01-01 | N-15 | **new arc** (conditional, see N-15) | IR1A-19; V1-C RF-6 |
| R-04-03-o / -p | DOWNSTREAM / INTERFACE | DEL-03-01; DEL-03-02 | N-11, N-12 (rep. rows in DEL-03-01 / DEL-03-02, C1-B). Proposed as a retarget or split of package row DEP-04-03-012 (→ PKG-03) | **new arcs** | V1-B RF-03 |
| DEP-04-03-019 (update) | UPSTREAM / CONSTRAINT | EXTERNAL (OI-001/OI-002, by TargetName) | — | non-topological pointer | DECISION-1 (V1-A RF-04); OI-021 remainder |

Noted but not proposed (outside this undertaking, D1; mirror only):
UPSTREAM mirrors of DEP-01-02-020 (DEL-01-02) and DEP-02-04-012 (DEL-02-04);
DOWNSTREAM mirrors to DEL-01-04, DEL-02-02, DEL-06-01/06-02 (package row
DEP-04-03-013 → PKG-06), DEL-09-02, DEL-09-05 and DEL-10-03.

### 5. Open items

| Item | Owner | Point of need |
|---|---|---|
| OI-021 (U-01); consequence vocabulary (U-02) | As DEL-04-01 | As DEL-04-01 |
| Representation, identity algorithm, carriage manifest (U-04); App record location (U-05); reader/writer placement (U-16) | DEL-04-03 with DEL-03-01 and DEL-02-01; OI-014 owners | Before OUT-001 CONFIG and writer implementation |
| Host placement (U-06, OI-013) | Shared contract owner with SWB implementation owner | Before shared/host boundary contracts |
| Multi-row A4 purpose (U-07) | DEL-04-01 with the owner | At its point of need |
| Host evidence: basis re-check (U-09), capture requirement (U-11), return to c₀ (U-12), stored findings (U-14), receipts etc. (U-15), constraint receipt (U-19), per-turn guidance (U-21) | Host owner (DEP-001; relay) | Before connected integration |
| R13 feed beyond DEL-01-01 (U-20); App person identity and act control (U-28) | DEL-01-02, DEL-01-04 (later, D1) | Their definitions |
| App-side holds (U-25, D6); SP-6 alternative (U-26); caller identity (U-27) | Owner; owner with DEL-02-01/04-01; App owner with host owner | Before hold fixtures; before origin conformance |
| Turn initiator on R11 (EXEC F-24) | DEL-04-03 | Next RS revision |

### 6. Lifecycle observation

INITIALIZED (2026-09-27). RS-v0.1…v0.5 is authorized production of OUT-001
and OUT-004 semantics and design for OUT-002/OUT-003. IN_PROGRESS would be
truthful. Not changed.

---

## DEL-02-01 — Portable workflow contract and shared allocation

### 1. Commitment → result

| SoW item | Design section(s) | Status | Remaining definition | Implementation / host / witness only |
|---|---|---|---|---|
| OUT-001 portable workflow/role/checkpoint contract | §2, §3, §4.3, §5, §6, §7 | developed | Host seat → role mapping options (SEAT-2, U-09) | Host guidance distribution (OI-018) |
| OUT-002 open declared-part schemas and examples | §3, §4.1–§4.6; EXAMPLES E1–E8 | **partially developed** | Physical carriage of the declared part (U-01, options without a recommendation); wire names, encodings and schema language (U-02); harness-capability naming (U-08); revision algorithm (U-03) | Parser fixtures |
| OUT-003 responsibility map | §9 A-1…A-12 | developed | — | Owner confirmations ("None" in every row; U-17); placement (OI-014/OI-013) stays open by design |
| OUT-004 parser and consumer fixtures | §13 VC-01…VC-42; EXAMPLES | developed (designed) | — | Parser and consumer runs; VC-11 AWAITING INPUT (SQ-02) |
| REQ-001 | §3.2, §5, §6 | developed | U-09 | — |
| REQ-002 | §4.1–§4.5 | **partially developed** | U-01, U-02, U-08 | — |
| REQ-003 | §4.3.1–§4.3.8, I-1…I-9 | developed | — | Host capture-evidence reference (U-05b) |
| REQ-004 | §4.6, §6 | developed | — | — |
| REQ-005 | §9 | developed | — | Owner confirmations |
| REQ-006 | §10 | developed | — | — |

### 2. Result → commitment

| Element | Authority | Note |
|---|---|---|
| Reached-when kinds, subject classes including "objects a named output concerns" and "targets of the held call", validity rules (§4.3.1, §4.3.5, §4.3.6) | R-5, R2-17, R3-1, R3-2, R5-3 | — |
| Item-level decisions at an A5 checkpoint (§4.3.7) | R2-18, R3-3, R4-7 (PROPOSED; confirmed by DEL-02-03) | — |
| Hold support per checkpoint and surface (§4.3.8); FB-18 | R5-1, R4-2, R4-8, R4-21; values owned by DEL-02-03 | EXEC F-22 holds: invalid declarations take no hold-support value |
| Governing checkpoint constraint and carriage assurance (§4.2.2) | R2-12, R4-14, R5-2 | — |
| **Harness capability requirement** tool class (§4.2.1) | Integration design; supplier `UNRESOLVED` (U-08) | Outside SoW REQ-002, which ties tool requirements to the CLM-002 capability supplier (DEL-03-01) (SC-02-01-2) |
| Identity tuple, holding library, derived-from (§6) | R-9, R2-20 (confirmed by EXEC §6.2) | — |
| SEAT-1…SEAT-3 (§5.3) | R-7 | — |
| A12 in the closed checkpoint list | R-1, R2-10 | — |
| Root conventions keep/change/leave (§7) | Reuse source, not v4 authority | IR1-C §4 found this consistent with AX-002 |

Unsupported additions: none. Design residuals for the next WD revision:
- §8 headers still read "Receives from WD-v0.4" and "State at v0.4", and §9
  says "Allocation result at v0.4". These are stale self-citations in v0.5.
- EXEC F-25 (adopt an "optional host operation absent" case in E7, or keep the
  OP-C12 case as the single example) is not yet dispositioned.

### 3. Proposed SoW corrections

| ID | Location | Current text (excerpt) | Proposed text | Grounds |
|---|---|---|---|---|
| SC-02-01-1 | CLM-002 | "`DEL-04-01` defines and carries adopted operation policy and human-act distinctions; the owner and host policy owner retain decisions on unresolved classes (OI-001/OI-002);" | "`DEL-04-01` defines and carries adopted operation policy and human-act distinctions, including the first-increment OI-001/OI-002 rulings (DECISION-1 D2/D3); operation-specific additions remain with the owner via the outside SWB session (OI-021); `DEL-03-02` owns proposal/outcome semantics, including the governing checkpoint constraint, item dispositions and item-left events; `DEL-01-01` supplies the harness capability inventory and supplied-guidance identity evidence; `DEL-03-03` carries constraints on the external channel;" | WD §8, §10; V1-C RF-7; R2-12, R2-18 |
| SC-02-01-2 | REQ-002, second sentence | "Tool requirements shall refer to the capability meaning supplied by CLM-002, and tool schemas shall remain open." | "Host-operation requirements shall refer to the capability meaning supplied by `DEL-03-01`; harness-capability requirements shall refer to capability meaning supplied through `DEL-01-01`. Tool schemas shall remain open." | WD §4.2.1; U-08; V1-C RF-7 |
| SC-02-01-3 | REQ-006, first sentence | "…catalog-semantic definition by `DEL-03-01`, operation-policy contract definition… by `DEL-04-01`,…" | Add "proposal/outcome definition by `DEL-03-02`," and "external-channel constraint carriage by `DEL-03-03`," | WD §10 rows |
| SC-02-01-4 | CLM-003, last sentence | "…PRD V4-AUT-03/05 and V4-REC-05, qualified by HTML-D03 and OI-001/OI-002." | "…qualified by HTML-D03 and the first-increment OI-001/OI-002 rulings in DECISION-1 D2/D3." | DECISION-1 |
| SC-02-01-5 | TBD-003 | "OI-001 and OI-002 retain operation-specific reserved-act and classifier policy choices with the owner and App/SWB contract owners at their stated policy points of need." | "OI-001 and OI-002 were ruled for the first increment by DECISION-1 D2/D3 (carried by DEL-04-01). Operation-specific reserved additions remain with OI-021." (The false-attribution and OI-018 sentences are unchanged.) | IR1A-20 pattern; WD §10 |
| SC-02-01-6 | Axiology, new TBD-004 | — | "TBD-004 — Whether a declared checkpoint can be held on a given surface is reported as hold support (DEL-02-03). App-side run holds are deferred by the owner to SWBPIPE SQ-02 (DECISION-2 D6). App-only checkpoints are *not enforceable* in this increment, and a workflow depending on one is *unsupported* in App runs. Point of need: before any App-run checkpoint is claimed held." | DECISION-2 D6; R5-1, R5-10; WD U-30 |

### 4. Proposed register changes (DEL-02-01 `Dependencies.csv`)

| Proposed row | Direction / type | Target | Mirrors / arc | Class | Grounds |
|---|---|---|---|---|---|
| R-02-01-a…e | DOWNSTREAM / HANDOVER | DEL-02-02; DEL-02-03; DEL-02-04; DEL-05-01; DEL-05-02 | DEP-02-02-014; DEP-02-03-009; DEP-02-04-011; DEP-05-01-016; DEP-05-02-005 | mirror only (5) | V1-C RF-3 (DEL-02-01 has no DOWNSTREAM rows) |
| R-02-01-f | DOWNSTREAM / HANDOVER | DEL-03-04 | DEP-03-04-008 | mirror only | Found in this comparison |
| R-02-01-g | UPSTREAM / INTERFACE | DEL-01-01 | N-16 | **new arc** | V1-C RF-7; WD U-08 |
| R-02-01-h | UPSTREAM / INTERFACE | DEL-02-03 | N-17 | **new arc** | WD §8 |
| R-02-01-i | UPSTREAM / INTERFACE | DEL-03-02 | N-18 | **new arc** | WD §8 |
| R-02-01-j | DOWNSTREAM / HANDOVER | DEL-09-06 | N-19 (rep. row in DEL-09-06) | **new arc** | W9 CA F-2 |
| R-02-01-k | DOWNSTREAM / HANDOVER | DEL-03-03 | N-20 (rep. row in DEL-03-03) | **new arc** | W8 F-11 |
| R-02-01-l | UPSTREAM / CONSTRAINT | EXTERNAL DECISION-1 (D2/D3) and OI-021 | — | non-topological | V1-A RF-04: DEL-02-01 has no OI-001/OI-002 row, although WD carries both |
| R-02-01-m | UPSTREAM / CONSTRAINT | EXTERNAL DECISION-2 D6 / SQ-02 | — | non-topological | WD U-30 |
| R-02-01-n | UPSTREAM / CONSTRAINT | EXTERNAL OI-018 | — | non-topological | SoW TBD-003 names OI-018; the register has no row |

Cross-group note for C1-B: V1-C RF-3 also asks to split DEP-03-01-022
(DEL-03-01 DOWNSTREAM → package PKG-02) into DEL-02-01 and DEL-02-03 rows.
Both arcs already exist (DEP-02-01-017, DEP-02-03-011), so the split is
mirror only. Noted but not proposed (D1): DOWNSTREAM mirrors to DEL-08-02,
DEL-09-02 and DEL-10-03.

### 5. Open items

| Item | Owner | Point of need |
|---|---|---|
| Declared-part carriage, wire names, revision algorithm (U-01, U-02, U-03) | DEL-02-01 with consumers and DEL-04-03 | Before the OUT-002 schema and OUT-004 parser fixtures |
| Harness-capability naming (U-08) | DEL-02-01 with DEL-01-01 and DEL-02-03 | Before the App-side required-tool check |
| Seat → role mapping (U-09); host precedence (U-10) | DEL-02-01 with SWB implementation owner and DEL-02-04; DEL-02-02 (later) | Before host role-guidance supply; before host-origin discovery |
| Operation-version ordering (U-07); real exposure (U-23; OI-003) | DEL-03-01; owner with host contract owner | Before version fixtures; before exposure claims |
| OI-021 (U-05, U-15); OI-003 (U-16); OI-018 (U-14); OI-014/OI-013 (U-12, U-13) | Their owners | As recorded |
| Owner confirmations for §9 rows; SWBPIPE consumer needs (U-17) | DEL-02-03, DEL-05-01, DEL-05-02, DEL-03-02; SWBPIPE owner via relay | Next comparison; relay |
| SQ-02 (U-19); App-side holds (U-30, D6); capture after arrival (U-31) | Host owner; owner | Before App-run checkpoint claims and hold-machine fixtures |
| Capture-evidence reference (U-05b); per-turn guidance in host loops (U-29) | Host owner (DEP-001) | Before host act-recording integration |
| App act control (U-25) | DEL-01-04 (later, D1) with DEL-04-03 | Before App capture fixtures |
| "On subject absent" path (U-32); EXEC F-25 case choice | DEL-02-01 | Before a subject-absent fixture runs; next WD revision |

### 6. Lifecycle observation

INITIALIZED (2026-09-27). WD/WD-EX-v0.1…v0.5 is authorized production of
OUT-001…OUT-003 and design for OUT-004. IN_PROGRESS would be truthful. Not
changed.

---

## DEL-02-03 — Workflow execution compatibility and round-trip support

### 1. Commitment → result

| SoW item | Design section(s) | Status | Remaining definition | Implementation / host / witness only |
|---|---|---|---|---|
| OUT-001 required-tool and checkpoint receiving behavior (CODE) | §3 (report, §3.6 hold support), §4 (hold machine), §5 (App-side capture) | **partially developed** | The App run's hold point is unallocated. `UNRESOLVED{D6}`: HP-1/HP-2 are not adopted; host-operation checkpoints are *not established* pending SQ-02; App-only checkpoints are *not enforceable* in this increment (F-10, F-17, U-E1, U-E23) | Code; App act control (DEL-01-04, later) |
| OUT-002 transfer and adaptation contract (DOC) | §6.1–§6.7 | developed | — | Host library, adaptation and run-record links (SQ-17/18/19; U-E14); registration side by DEL-02-02 (later, D1) |
| OUT-003 fixtures (TEST) | §7 MT-1…MT-16, CH-1…CH-30, RT-1…RT-11; VC-E-01…VC-E-12 | developed (designed) | — | Candidate runs; the joined witness is DEL-09-06's |
| REQ-001 | §3 | developed | Harness-capability names (U-E10) → *not established* | — |
| REQ-002 | §2, §3.6, §4.1–§4.14 | **partially developed** | App-side holding (D6, as above) | Host holds (SQ-02) |
| REQ-003 | §4.5 SP-1…SP-8; §5 CAP-1…CAP-9 | developed | — | Host capture-evidence reference (SQ-01); App act control (U-E8) |
| REQ-004 | §6.1–§6.4, §6.6, §6.7 | developed | — | Host receipt (U-E14) |
| REQ-005 | §6.5 | developed (definition) | — | Registration by DEL-02-02 (later, D1; F-12) |
| REQ-006 | §10 | developed | — | — |
| REQ-007 | §8, UNRESOLVED | developed | — | — |

### 2. Result → commitment

| Element | Authority | Note |
|---|---|---|
| Hold-support value set (§3.6); HP-1…HP-4 and HP-H (§2) | R5-1, R4-2; HP-4 scope INTEGRATION (HOSTING F-22 ruling) | EXEC owns the values |
| SP-6 capture after arrival (§4.5) | R4-5 (standing PROPOSED) | Owner question U-E4; repeat-A12 cost F-23 |
| Re-hold (§4.7); finality and continuation (§4.9); A12 control relations (§4.10); MX rules (§4.11) | R4-3, R4-4 (PROPOSED), R4-6, R4-7; R5-5 | — |
| App-side capture requirements CAP-1…CAP-9 (§5) | PROPOSED (W7); CAP-6 R4-12; CAP-1 R4-13 | Construction belongs to DEL-01-04 (later) |
| Holding library (§6.2); carriage manifest (§6.3) | R2-20; PROPOSED | — |
| Suppliers beyond SoW CLM-001…CLM-003: DEL-03-02, DEL-04-02, DEL-01-01, DEL-03-03, DEL-01-04 (§9.1) | R-rulings above | SC-02-03-4 |

Unsupported additions: none. F-26 (re-verify CH-12…CH-14 against C's V-GR1)
can now be performed: C-v0.5 at `d3cebd1cc` defines V-GR1 (C §10.4), so the
re-verification is an open check for the next EXEC revision. F-27 is LOOP's
(C1-C).

### 3. Proposed SoW corrections

| ID | Location | Current text (excerpt) | Proposed text | Grounds |
|---|---|---|---|---|
| SC-02-03-1 | CLM-003, after "The standalone App continues to execute through stock Codex." | — | Add: "No App-side hold point is currently allocated for App runs. How the App holds its own runs is deferred by the owner to the SWBPIPE answer to relay SQ-02 (DECISION-2 D6). Until it is resolved, the compatibility report states per-checkpoint hold support, action during hold is recorded, and no unenforced hold is claimed." | F-10 (carried to C1 by R4-2 as a SoW gap); R5-1 |
| SC-02-03-2 | REQ-002 (the requirement is kept) and AC-002 | REQ-002: "…hold the run at that checkpoint until the person performs that act…"; AC-002: "A declared checkpoint requests its named human act and remains waiting…" | Keep REQ-002. Append to AC-002: "On a surface whose hold support is *not established* or *not enforceable*, the requirement check reports that value (not a pass), and every run action during the waiting period is recorded as action during hold." **Flag for the owner:** App-only checkpoints cannot meet REQ-002 in this increment whatever SQ-02 returns (R5-10). Narrowing REQ-002 for App runs would be a scope change on the owning route, not a C1 correction | F-10, F-17; R5-10; U-E23 |
| SC-02-03-3 | Axiology, new TBD-006 | — | "TBD-006 — App-side run holds (`APP-V4-FIRST-INCREMENT-20260928-DECISION-2` D6). **Owner:** the owner, on the SWBPIPE answer to SQ-02, then App/shared owners (OI-014). **Point of need:** before any App-side positive hold case and before the App fixes its hold realization. App-only checkpoints are a separate owner follow-up (R5-10)." | U-E1, U-E23 |
| SC-02-03-4 | CLM-002 (append) and REQ-006 | CLM-002 names DEL-03-01, DEL-04-01 and DEL-04-03; REQ-006 lists the matching excluded acts | CLM-002: add "`DEL-03-02` owns proposal item dispositions, item-left events and the governing checkpoint constraint; `DEL-04-02` owns grant display states; `DEL-03-03` owns external-channel carriage and its assurance; `DEL-01-01` supplies observed supplier facts; `DEL-01-04` (later undertaking) constructs the App act control." REQ-006: add the matching excluded acts (proposal/outcome semantics; external adapter construction and carriage; App act control construction) | EXEC §9.1, §10 |
| SC-02-03-5 | TBD-001 and TBD-002 | "OI-001, reserved human acts. **Owner:** Owner with App/SWB contract owners…"; "OI-002, classifier routine permissions…" | As SC-04-01-8 and SC-04-01-9 (DECISION-1 D2/D3 pointer; the OI-021 remainder is already TBD-005) | W7 F-11 (carried to C1) |

### 4. Proposed register changes (DEL-02-03 `Dependencies.csv`)

| Proposed row | Direction / type | Target | Mirrors / arc | Class | Grounds |
|---|---|---|---|---|---|
| R-02-03-a | DOWNSTREAM / HANDOVER | DEL-05-01 | DEP-05-01-017 | mirror only | V1-C RF-8 |
| R-02-03-b | DOWNSTREAM / HANDOVER | DEL-03-04 | DEP-03-04-009 | mirror only | Found in this comparison |
| R-02-03-c | DOWNSTREAM / HANDOVER | DEL-02-02 | DEP-02-02-015 | mirror only | F-12 (CASE-002 M1 workspace row) |
| R-02-03-d | UPSTREAM / INTERFACE | DEL-03-02 | N-21 | **new arc** | EXEC §9.1 |
| R-02-03-e | UPSTREAM / INTERFACE | DEL-05-01 | N-22 | **new arc** | EXEC §9.1 |
| R-02-03-f | UPSTREAM / INTERFACE | DEL-04-02 | N-07 | **new arc** | EXEC §9.1 |
| R-02-03-g | UPSTREAM / INTERFACE | DEL-01-01 | N-23 | **new arc** | EXEC §9.1 |
| R-02-03-h | UPSTREAM / INTERFACE | DEL-03-03 | N-24 | **new arc** | EXEC §9.1 |
| R-02-03-i | DOWNSTREAM / HANDOVER | DEL-02-01 | N-17 (rep. row in DEL-02-01) | **new arc** | WD §8; EXEC §9.2 |
| R-02-03-j | DOWNSTREAM / HANDOVER | DEL-04-03 | N-13 (rep. row in DEL-04-03) | **new arc** | EXEC §9.2 |
| R-02-03-k | DOWNSTREAM / HANDOVER | DEL-04-02 | N-02 (rep. row in DEL-04-02) | **new arc** | EXEC §9.2 |
| R-02-03-l | DOWNSTREAM / HANDOVER | DEL-05-02 | N-25 (rep. row in DEL-05-02) | **new arc** (conditional) | EXEC §9.2; V1-C RF-4 |
| R-02-03-m | DOWNSTREAM / HANDOVER | DEL-09-09 | N-26 (rep. row in DEL-09-09) | **new arc** | W9 XT F-2 |
| R-02-03-n | DOWNSTREAM / HANDOVER | DEL-03-03 | N-27 (rep. row in DEL-03-03) | **new arc** | W8 F-11 |
| DEP-02-03-015 / -016 (update) | UPSTREAM / CONSTRAINT | OI-001 / OI-002 | — | non-topological pointer | W7 F-11; DECISION-1 D2/D3 |
| R-02-03-o | UPSTREAM / CONSTRAINT | EXTERNAL DECISION-2 D6 / SQ-02 | — | non-topological | U-E1 |

Noted but not proposed (D1): DOWNSTREAM mirrors to DEL-09-02
(DEP-09-02-017) and DEL-10-03 (DEP-10-03-009).

### 5. Open items

| Item | Owner | Point of need |
|---|---|---|
| App-side holds (U-E1, D6/SQ-02); App-only checkpoints (U-E23; F-17) | Owner; separate D6 follow-up | Before App-side positive hold cases; before an App-only checkpointed workflow is offered as supported |
| Host placement of the hold machine and check (U-E2; OI-013/OI-014) | Shared contract owner with SWB implementation owner; App/shared owners | Before boundary contracts |
| Multi-row A4 purpose (U-E3; F-14) | DEL-04-01 with the owner | Before re-hold and lapse fixtures run |
| SP-6 vs prior acts (U-E4; F-23) | Owner, with DEL-02-01 and DEL-04-01 | Before hold-machine fixtures run |
| On-subject-absent path (U-E7) | DEL-02-01 | Next comparison |
| App person identity and act control (U-E8) | DEL-01-04 (later) with DEL-04-03 | Before App capture fixtures |
| Host items: proxy control (U-E9, SQ-25), versions (U-E11, SQ-18d), capture reference (U-E12, SQ-01), constraint receipt (U-E13, SQ-02), library, adaptation and run records (U-E14), per-turn guidance (U-E15) | Host owner (DEP-001) | As listed in EXEC UNRESOLVED |
| Harness-capability names (U-E10); declared-part carriage and revision algorithm (U-E16) | DEL-02-01 with DEL-01-01 / DEL-04-03 | Before the App-side check; before OUT-002 schema and transfer code |
| OI-021 (U-E17); OI-003 and exposure (U-E18); slot policy and registration act (U-E19) | Their owners | As recorded |
| Changed-draft return to DEL-02-02 uncompared (F-12) | DEL-02-02 owner (later, D1) | Before the DEL-02-02 definition |
| V-GR1 re-verification (F-26); turn initiator on RS R11 (F-24) | DEL-02-03; DEL-04-03 | Next revisions |

### 6. Lifecycle observation

INITIALIZED (2026-09-27). EXEC-v0.1…v0.3 is authorized production of OUT-002
and design for OUT-001/OUT-003. IN_PROGRESS would be truthful. Not changed.

---

## Checks performed and limits

- Each SoW OUT/REQ was traced into the Design sections, and each Design
  element beyond the SoW was traced back to its ruling. Every Design header's
  SoW hash equals the candidate SoW bytes.
- Row IDs were checked against the actual registers at `d3cebd1cc` (all 41
  registers). Each "mirror only" class names the existing row that already
  establishes the arc. Each "new arc" was confirmed absent in both directions
  of row placement.
- No file other than this one was written. Git was used read-only, and no
  network access was used. No SoW, register, status, context or reference file
  was changed, and no lifecycle state was changed.
- This comparison does not re-review design content, and it does not certify
  that the proposed rows' wording is final. Application follows the owning
  routes:
  - SoW amendments go through the SoW owner.
  - Register rows go through dependency extraction and, for new arcs,
    `project-dag` departure (DAG-002).
  - `Open_Issues.csv` updates go through the decomposition owner.
  - Lifecycle transitions are made by the Human or WORKING_ITEMS.
- C1-B and C1-C hold the representative rows for N-03…N-06, N-08, N-09, N-11,
  N-12, N-19, N-20 and N-25…N-28. Those groups should cite these IDs so that
  each arc is proposed once.
