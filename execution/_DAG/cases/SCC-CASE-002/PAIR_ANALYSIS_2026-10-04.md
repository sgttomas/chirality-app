# SCC-CASE-002 — pair analysis of the interface–interface pairs (2026-10-04)

- **Standing.** Case evidence update under `workflows/scc-resolution-case`. It is evidence for the owner's checkpoint, not a ruling. No row, register, ScopeOfWork, Design file, DAG version or existing case file is changed. Every move below is a **proposal**. Cut and merge are the owner's (`docs/CYCLE_DRIVEN_RESOLUTION.md` §2 rule 3). Any ScopeOfWork revision is applied by `scope-of-work` under an amendment the owner accepts. A decomposition change goes through `scope-change`. CaseState stays EVIDENCE_ACCUMULATING. The CP1-20260928 ruling carries forward unchanged.
- **Run.** `APP-V4-GRAPH-CLOSURE-20261004`, early path for SCC-002. Author: a Type 2 TASK agent (Claude Opus 5.5) dispatched by HELP_HUMAN. It does not delegate. Branch `claude/app-v4-graph-closure`, HEAD `c1d7eebb83`, clean tree.
- **Paths.** `E/` is `projects/chirality-app-v4/execution/`. Pair labels P1…P21 are G1's (§2.2), in G1's order.
- **Scope.** The 11 pairs G1 marks I–I (P1, P3, P4, P5, P6, P7, P8, P11, P15, P17, P21), and P9 and P12. P9 and P12 were added by the coordinator after RVG's finding G1-M1 (`reviews/RVG-G1.md`), which reads DEL-04-03's received list as interface definitions.

## 0. Basis and checks

| File | sha256 |
|---|---|
| `E/_DAG/DAG-004/CandidateEdges.csv` | `2bfff10e3094d7fd86da563006c965694563ec10d0fc78e9b1d9958fefa42025` |
| `E/_DAG/DAG-004/ExcludedRows.csv` | `45f55e76ecf7c9aac3bd923838eee8c302d6b2776e4fa3c221e51f9cf465664e` |
| `docs/CYCLE_DRIVEN_RESOLUTION.md` | `bbd41a8d091c7fa81fce6462c1d5e976832e5879b6ab8c3c74147e2df55e514f` |
| `E/_Coordination/AgentRuns/APP-V4-GRAPH-CLOSURE-20261004/SURVEY/G1.md` (commit `c1d7eebb83`) | `4e85ac7917178fcb4a87f3b481ac724d17deae9fe438df3c814a63879565973c` |
| `E/_Coordination/AgentRuns/APP-V4-GRAPH-CLOSURE-20261004/SURVEY/G2.md` | `24cc2a6fcb00e466775647ce14590cb91914b6132aab6a441e79576c22efa87b` |
| `E/_Coordination/AgentRuns/APP-V4-GRAPH-CLOSURE-20261004/reviews/RVG-G1.md` | `70c30b56648e29b3ae8881bae51cfbcf1f8c71f83b770a38a157dc98316b9fb3` |
| `E/_Coordination/AgentRuns/APP-V4-SCA003-20261002/DAG_PREP/CASE-002_EVIDENCE_UPDATE.proposed.md` | `5cdf942f49b129f84579f276444781c9a235af99c1bb7728e31b9329fc973ce2` |

Design files were read at HEAD, by section. Their versions are WD-v0.9, WR-v0.2, EXEC-v0.7, NIR-v0.3, C-v0.8, P-v0.8, ACT-POLICY-v0.11, AS-v0.9, RS-v0.10, LOOP-v0.9 and PANEL-v0.9. Every one is "DRAFT DEFINITION" or "PROPOSED". None is accepted.

**Checks run.** The scripts are scratch files under `$TMPDIR`, not in the repository.

| Check | Result |
|---|---|
| Pairs | 71 held arcs of SCC-002 in DAG-004 give exactly 21 reciprocal pairs, matching G1 §2.2 |
| Live fidelity of the 26 rows of the 13 pairs | Each equals its live register row in every field. Each `EvidenceQuote` occurs in the `ScopeOfWork.md` beside its register (whitespace, `` ` `` and `*` normalised) |
| Mirror rows | Read from `ExcludedRows.csv` `RepresentedBy`. They are listed per pair below. A move on an arc must also cover its mirror rows (G1 K-7), because each mirror rests on its own ScopeOfWork sentence |
| Baselines | Without moves, my Tarjan and exact minimum feedback arc set reproduce G1 §1.3: O-1 13 members / 21 rows; O-2 and O-3 12 / 17; O-4 10 / 11. With DEL-04-03's received list read as I (RVG G1-M1), O-4 gives 12 / 13, as RVG reports |
| Closure with moves | §15, computed by exact dynamic programming over member subsets (2^13 states) |

**Quotes.** Quotes are verbatim from the file named. `…` marks an omission inside a quoted sentence.

## 1. How each pair was decided

**Question asked of each pair** (G1 §1.2). Does B's contribution to A depend, inside B, on the part of B that needs A's contribution? And does the same hold the other way? If the Designs show an order of parts with no such dependency, the deliverable-level 2-cycle is a **projection artefact**. Otherwise it is a **real ordering contradiction**.

**One discriminator decides which side can yield.**
- *Rule-bearing* consumption: the consumer's own rules, mappings or validity depend on the supplier's values.
- *Carry-only* consumption: the consumer transports, displays or records the supplier's values without its own rules depending on them.

A rule-bearing row can be reversed only by moving definitional ownership. A carry-only row can be reversed behind a slot.

**Move codes.**

| Code | Move | Ownership moves? | Who |
|---|---|---|---|
| IV | **Invert.** The contract stays with the owner the ScopeOfWork already names. The cycle-closing row is withdrawn as a contract input, because its content is already owned by the consumer, by the accepted basis, or flows the other way. The reverse arc already exists, so the edge in effect reverses | No | Agent proposes; ScopeOfWork wording through an accepted SCA |
| IV-S | **Slot inversion.** The consumer defines a slot and carries the supplier's published values by identity and version. Validation against the supplier's schema becomes a conformance check. Condition: `dependency-extract` must accept that carriage by reference is not a contract input at `INITIALIZED`. If it is still extracted as one, the move fails, and the pair needs DEC or an owner ruling on edge semantics (doctrine §2 rule 1) | No | Agent proposes; conditional as stated |
| RT | **Re-target** to DEL-04-01, which already defines the needed meaning. DEL-04-01 has 0 suppliers (SCA-V4-003 Q-5, `GRAPH_BASIS.md` l.44), so no arc into it can close a cycle. Condition: Q-5 holds. If G2's A2 or A3 became rows read as I, the retargets would fail (§16) | No | Agent proposes; register owner re-resolves |
| IV-O | Invert by moving definitional ownership assigned by a ScopeOfWork. Not a pure design move | **Yes** | Owner, through SCA |
| DEC | Decomposition change | — | Owner, through `scope-change` |
| CUT, MRG | Cut or merge | — | Owner |

**ScopeOfWork effect codes.**
- **S1**: wording revision of a consumption or receivers sentence. No owner or OUT/AC/VER obligation moves.
- **S2**: definitional ownership moves.

**Finding that applies to every pair.** None of the 13 pairs closes by a register-only change. Each cycle-closing row rests on a ScopeOfWork sentence, and most arcs also carry a mirror row that rests on the supplier's "received by … each of which declares it upstream in its own register" sentence. Withdrawing the arc therefore needs S1 wording in one or two ScopeOfWorks.

## 2. P1 — DEL-01-04 ↔ DEL-02-02

**Rows.**

| Row | From → To | EvidenceQuote | Statement (excerpt) | Mirror |
|---|---|---|---|---|
| DEP-01-04-009 | 01-04 → 02-02 | "The native draft receiving interface shall carry source-qualified draft identity and explicit transitions supplied by the workflow workspace." | "Receive source-qualified draft identity and actual draft/registration/collision/refusal transitions from the workflow workspace … the A15 descriptor … and the run-start text and run-end line App DEL-02-02 supplies" | DEP-02-02-021 |
| DEP-02-02-013 | 02-02 → 01-04 | "DEL-02-02 consumes these inputs and retains workflow-making integration responsibility." | "Receive native requests, outcomes, attachments, the draft-UI receiving interface and the App act control that captures registration (with its capture evidence) from DEL-01-04" | DEP-01-04-010 |

**ScopeOfWork.**
- DEL-01-04 REQ-004: "The native draft receiving interface shall carry source-qualified draft identity and explicit transitions supplied by the workflow workspace."
- DEL-01-04 CLM-004: "This slice supplies native attachment and draft-transition receiving interactions to that owner."
- DEL-02-02 CLM-002: "native requests, outcomes, attachments, the draft-UI receiving interface and the App act control that captures registration belong to `DEL-01-04` … DEL-02-02 consumes these inputs and retains workflow-making integration responsibility."

**Design.**
- WR-v0.2 §7 offers the contract: "**Offered:** `draft_reference`, `draft_transition` (with `a15_record` and `revision`, C-02), `registration_disposition` …". It receives "the native draft view and review presentation" and "the capture {A15 record identity, capture-evidence reference, bound content, descriptor identity}". Its failure rule is "Control not built: nothing is registered".
- NIR-v0.3 §7 consumes that contract: "[`nir.draft-transition.schema.json`] restates `draft_transition` **with D5's own element names and values**", and "**Accepted transitions** are WR §5.1's".
- WR RB-4a: "DEL-01-04's act control (AAC-v0.2 §4.2, schemas 0.3, RV21) takes this file's descriptors as they are".

**Kind.** I–I confirmed on content. DEP-02-02-013's point of need is integration ("retains workflow-making integration responsibility").

**Order.**
- DEL-02-02's contribution (WR §5.1, §8, §16) does not depend on what WR receives from DEL-01-04. That intake is a built view, plus a capture report whose fields are WR's own descriptor identity and references.
- DEL-01-04's contribution depends on WR's (NIR §7, AAC).
- The part order is WR contract → NIR/AAC contract → WR integration. **Projection artefact.**

**Move.**
- DEP-02-02-013 with its mirror DEP-01-04-010: **IV-S**.
  - WR owns and publishes the exchanged contract: WR-v0.2 §7 and §8, and `workspace-registration.schema.json`.
  - DEL-01-04 conforms. DEP-01-04-009 stays as the sequencing row.
  - WR carries the capture report by reference.
- **Residual.** DEL-02-02's joined journey uses DEL-01-04's built control. WR-VC-01 needs "DEL-01-04's act control and draft view". That residual is a verification input (V). It still sequences under O-1.
- **ScopeOfWork: S1**, in two ScopeOfWorks: DEL-02-02 CLM-002 ("consumes these inputs") and DEL-01-04 CLM-004 / OUT-004 (the supply sentence). No ownership moves. The receiving interface, the act control (OUT-005, REQ-008) and the native slice stay DEL-01-04's. The workspace vocabularies stay DEL-02-02's.
- **Anchor.** WR-v0.2 §7, §8; `workspace-registration.schema.json`.
- Inverting DEP-01-04-009 instead would move WR's vocabulary to DEL-01-04 (S2). Not proposed.

## 3. P3 — DEL-02-01 ↔ DEL-02-03

**Rows.**

| Row | From → To | EvidenceQuote | Mirror |
|---|---|---|---|
| DEP-02-01-026 | 02-01 → 02-03 | "This contract consumes `DEL-02-03`'s statement of the current phase and, for the governance phase, its hold-support values; it does not define them." | DEP-02-03-030 |
| DEP-02-03-009 | 02-03 → 02-01 | "This slice receives those contracts and preserves selected identity during execution and transfer." | DEP-02-01-031 |

**ScopeOfWork.**
- DEL-02-01 TBD-004 states the current phase itself: "In the current phase a declared checkpoint is plan guidance. … Neither the App nor a host's embedded loop holds a run or reports a workflow unsupported because a hold cannot be enforced." It ends: "**Point of need:** before any checkpoint is claimed held."
- DEL-02-03 REQ-002 states the same phasing from the same source (`APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4` D4-1).

**Design.**
- WD-v0.9 §4.3.0 quotes the amended PRD V4-WF-05 and V4-HI-42 directly, and says "this contract consumes DEL-02-03's statement of the current phase and does not define it".
- EXEC-v0.7 §2.1 PH-1: "The declaration still states each checkpoint's required act, reached-when, subject class and held actions (WD §4.3.1)".
- EXEC §3.6 owns the hold-support values. WD §4.3.8 restates them as "governance-phase definition, retained".

**Kind.** I–I confirmed on content. **Boundary:** TBD-004's point-of-need sentence places DEP-02-01-026 in the governance phase. By K-6 that could make L primary, which would take P3 out of the I–I set under O-3 and O-4. This is for the standing reviewer.

**Order.**
- EXEC's phase statement and values depend on WD §4.3.1 (PH-1, PH-9, §3.6 "per governed checkpoint").
- WD §4.3.1 does not depend on EXEC.
- The part order is WD §4.3.1 → EXEC §2.1/§3.6 → WD §4.3.0/§4.3.8. **Projection artefact.**

**Move.**
- DEP-02-01-026 with its mirror DEP-02-03-030: **IV**.
- The current-phase content is already stated by DEL-02-01's own TBD-004 and REQ-003, from D4-1.
- WD §4.3.8 cites EXEC §3.6 instead of restating it. EXEC's check already consumes WD's `governed` flag through DEP-02-03-009.
- **ScopeOfWork: S1**, in two ScopeOfWorks:
  - DEL-02-01 TBD-004's consuming sentence becomes a citation;
  - DEL-02-03 CLM-003's receivers list ("received by `DEL-02-01`, …").
- No ownership moves. The values stay DEL-02-03's, and "it does not define them" still holds.
- **Anchor.** EXEC-v0.7 §2.1 PH-1…PH-10, §3.6; WD-v0.9 §4.3.0, §4.3.1 `governed`.
- **Caveat.** WD cites EXEC beyond the register row, for example §4.3.4 "Run end and continuation (R4-4; EXEC §4.9 …)" and §6.4. Those passages must become citations too. Otherwise they are design reliance that no register row records.
- A partial cut of the governance-phase part is not a graph move (RVG G1-m4). The fallback is an owner cut of the whole arc.

## 4. P4 — DEL-02-01 ↔ DEL-03-02

**Rows.**

| Row | From → To | EvidenceQuote | Mirror |
|---|---|---|---|
| DEP-02-01-029 | 02-01 → 03-02 | "Checkpoint subject binding and item-level decisions consume `DEL-03-02`'s change-item content identities, per-item dispositions, all-items-decided indication, item-left events and applied-outcome object identities; this contract does not define them." | DEP-03-02-028 |
| DEP-03-02-027 | 03-02 → 02-01 | "It also consumes App v4 `DEL-02-01` workflow identity (kind, origin, source root, name, revision) for proposal origin, and its checkpoint declarations" | DEP-02-01-033 |

**ScopeOfWork.**
- DEL-02-01 CLM-002: "`DEL-03-02` owns proposal/outcome semantics, including item dispositions, item-left events and the governing checkpoint constraint (governance phase)".
- DEL-03-02 CLM-003 adds: "the governing checkpoint constraint derived from them applies only in the governance phase."

**Design.**
- P-v0.8 §3.3 "Workflow identity | {kind, origin, source root, name, revision} … | SoW CLM-003 (DEP-03-02-027); R-9; DEL-02-01 §6.1". The governing constraint: "In Phase 1 the App carries none".
- P §4.3: "the mapping of these data to checkpoint dispositions … is **WD §4.3.7**".
- WD-v0.9 §8 (DEL-03-02 row): "§6.1 identity tuple, for proposal origin; §4.3.1 … §4.3.7 item rule and its needs (item-left events, all-decided)".

**Kind.** I and I/L confirmed.

**Order.**
- WD §6.1 → P §3.3 origin, which is carry-only.
- P §4.3, §4.6 and §9 item data → WD §4.3.6–§4.3.7, which is rule-bearing.
- WD §4.3.1 → P governing constraint, which is governance phase only.
- P points to WD §4.3.7 but defines nothing from it. **Projection artefact**, but the two directions are different concerns, and both are definitional.

**Move.**
- **Under O-3 and O-4:** IV-S on DEP-03-02-027's identity carriage. P carries WD's `$defs/workflow_identity` by reference. The residual, the derivation of the governance-phase constraint, is L and leaves by kind. No ownership moves. S1 in DEL-03-02 CLM-003 and DEL-02-01 CLM-002 (receivers list, mirror DEP-02-01-033).
- **Under O-1 and O-2:** the L residual stays on the same arc, so the arc remains. DEP-02-01-029 is rule-bearing on vocabulary the ScopeOfWork assigns to DEL-03-02. The remaining moves are:
  - **DEC.** Preferred. Split DEL-02-01 into a core (identity tuple §6.1, declared part §3, checkpoint elements §4.3.1, disposition vocabulary §4.3.4) and a part for checkpoint subject binding and item-level decisions (§4.3.6–§4.3.7) together with the shared allocation map (§9, OUT-003). The same split serves P6 and P7. G1 flagged DEL-02-01, which sits in five of the original 11 I–I pairs. An alternative split is DEL-03-02's change request (§3) from its item lifecycle (§4).
  - **IV-O.** Move §4.3.6–§4.3.7 to DEL-02-03, which already consumes P's item data (DEP-02-03-025) and confirmed §4.3.7 (EXEC §4.11). This moves ownership that DEL-02-01 CLM-002 states as "Checkpoint subject binding and item-level decisions consume `DEL-03-02`'s …".
  - **MRG.** Owner.
- **Anchor.** WD-v0.9 §6.1 and `workflow-declaration.schema.json` `$defs/workflow_identity`; P-v0.8 §3.3, §4.3, `proposal_state.schema.json`.

## 5. P5 — DEL-02-01 ↔ DEL-04-03

**Rows.**

| Row | From → To | EvidenceQuote | Mirror |
|---|---|---|---|
| DEP-02-01-019 | 02-01 → 04-03 | "Each act retains its actor, subject and supporting evidence through the PKG-04 receiving contract;" | DEP-04-03-037 |
| DEP-04-03-034 | 04-03 → 02-01 | "the workflow identity tuple and the checkpoint disposition vocabulary from `DEL-02-01`," | — |

**ScopeOfWork and Design.**
- DEL-04-01 REQ-002: "Each asserted act retains its actual actor, subject and supporting evidence."
- ACT-POLICY-v0.11 §2.4: "This is the meaning DEL-04-03 receives. DEL-04-03 owns the format." It lists act kind, decision actor, recorder and recording mode, subject content identity, evidence reference and lapse state.
- ACT §2.6 gives the capturing surfaces.
- WD-v0.9 §4.5 "expected act evidence | The act record expected (DEL-04-03 human-act record meaning), with its capturing surface and capture-evidence reference (I-5)."

**Kind.** I–I confirmed.

**Order.**
- RS's received WD tuple and dispositions are carried in R2 and R8.
- WD needs act meaning, which ACT already defines and which flows ACT → RS.
- **Projection artefact.**

**Move.**
- DEP-02-01-019 with its mirror: **RT** to DEL-04-01 (ACT §2.4, §2.6). DEP-02-01-018 is admitted already.
- The record reference in WD §4.5 becomes a slot (IV-S).
- **ScopeOfWork.** DEL-02-01 REQ-003 already reads "PKG-04 receiving contract", so it needs no change. **S1** in DEL-04-03 REQ-005: "App v4 `DEL-02-01`, `DEL-02-03` and `DEL-03-01` consume it at deliverable level".
- No ownership moves.
- **Caveat (RVG G1-m5).** The row's Notes keep it "separately from DEL-04-01 distinctions", so the register owner must accept merging it into DEP-02-01-018.
- DEP-04-03-034 is in no minimum set (G1), so it is not proposed.

## 6. P6 — DEL-02-01 ↔ DEL-05-01

**Rows.**

| Row | From → To | Quote | Mirror |
|---|---|---|---|
| DEP-02-01-020 | 02-01 → 05-01 | ST: "Receive minimal-loop consumer requirements to define the portable contract and responsibility/allocation map against concrete host receiving needs." EQ, generic: "Receive catalog descriptors, record semantics and host consumer needs from the owners in CLM-002 and CLM-003." | — |
| DEP-05-01-016 | 05-01 → 02-01 | "This deliverable consumes their meanings at the loop boundary." | DEP-02-01-035 |

**ScopeOfWork.**
- DEL-02-01 CLM-002: "`DEL-05-01` owns minimal-loop receiving requirements".
- DEL-05-01 REQ-006 excludes "defining workflow/role/checkpoint declarations or shared allocation of `DEL-02-01`".
- DEL-02-01 AC-005: OUT-003 "records confirmation or its absence".

**Design.**
- WD-v0.9 §8, expected from DEL-05-01: "Evaluation and binding; dispatch record …", used in "§4.3.5, §6.2".
- LOOP-v0.9 §10.3 gives DEL-02-01 as supplier of "Checkpoint elements; subject classes; §4.3.7; identity tuple; holding library".

**Kind.** I/R and I confirmed.

**Order.**
- The loop's needs feed WD as requirements.
- The loop's definitions consume WD.
- The part order is LOOP needs → WD contract → LOOP definitions → WD §9 map. **Projection artefact.**

**Move.**
- DEP-02-01-020: **IV**. The consumer's needs become a requirements input and a conformance return: the loop checks WD, and confirms or withholds confirmation of its map row. AC-005 already allows "its absence".
- **ScopeOfWork: S1** in DEL-02-01's method paragraph ("Receive … host consumer needs"). No mirror.
- No ownership moves.
- **Anchor.** WD-v0.9 §4.3, §6, §8, §9 and the schema.

## 7. P7 — DEL-02-01 ↔ DEL-05-02

**Rows.**

| Row | From → To | Quote | Mirror |
|---|---|---|---|
| DEP-02-01-021 | 02-01 → 05-02 | ST: "Receive host-panel consumer requirements to define the portable contract and responsibility/allocation map against concrete panel receiving needs." EQ is generic, as for P6 | — |
| DEP-05-02-005 | 05-02 → 02-01 | "`DEL-02-01` supplies portable workflow/checkpoint meaning;" | DEP-02-01-036 |

**Design.**
- WD-v0.9 §8, expected from DEL-05-02: "Panel needs", used in "§9" only, the allocation map (OUT-003).
- PANEL-v0.9 §6 is DEL-05-02's own allocation account.

**Kind.** I/R and I confirmed.

**Order.**
- WD OUT-001 and OUT-002 → PANEL OUT-001 → WD OUT-003. **Projection artefact.** It is the cleanest case.

**Move.**
- DEP-02-01-021: **IV**, as in P6.
- **ScopeOfWork: S1** in the same method paragraph.
- No ownership moves.
- **Anchor.** WD-v0.9 §4.2.4, §4.3.4, §4.3.7, §6.

## 8. P8 — DEL-02-02 ↔ DEL-02-03

**Rows.**

| Row | From → To | Quote | Mirror |
|---|---|---|---|
| DEP-02-02-015 | 02-02 → 02-03 | EQ, generic: "Their inputs remain explicit, while this deliverable owns their standalone workspace join." ST: "Receive capability/checkpoint execution and round-trip support from DEL-02-03 … for each run DEL-02-03 starts, this workspace composes the run-start text …" | DEP-02-03-031 |
| DEP-02-03-010 | 02-03 → 02-02 | "routing changed drafts through the existing reviewed-registration contract." | DEP-02-02-022 |

**Design.**
- WR-v0.2 §7, DEL-02-03 row. Offered: "`selection_record` …; v0.2: the composed run text and its `run_text` record for the run DEL-02-03 opens, the `supply_check`". Received: "the compatibility report (shown beside a review or a selection, labelled), T-1's refusal wording, run start". Failure rule: "Report not established: shown so (EXEC CR-3); nothing is gated by it (CC-3)".
- WR §16.1: "DEL-02-03 asks DEL-02-02 for the text after it opens the run".
- EXEC-v0.7 §2.6 A-1 consumes "DEL-02-02's selection record, WR-v0.2 §4.4 SL-1, §8".

**Kind.** I–I confirmed. **Note:** DEP-02-02-015's Statement carries the run-start text, which is DEL-02-02's own output, triggered by DEL-02-03's run start at run time. That content flows WR → EXEC, which is DEP-02-03-010's direction.

**Order.**
- WR selection and run text → EXEC check and run start → WR display of the report, which gates nothing. **Projection artefact.**

**Move.**
- DEP-02-02-015 with its mirror: **IV-S**. WR's join contract is the published interface. WR shows EXEC's report by reference.
- **Residual.** REQ-005 says "Missing capability, required human checkpoint or unknown outcome shall remain visible in the joined journey". That is a V residual for the joined journey.
- **ScopeOfWork: S1** in two ScopeOfWorks:
  - DEL-02-02 CLM-003 / REQ-005. The run-text clause also moves out of the consumption reading;
  - DEL-02-03 CLM-003's receivers list.
- No ownership moves.
- **Anchor.** WR-v0.2 §7, §8 (`selection_record`, `run_text`, `supply_check`), §16.

## 9. P9 — DEL-02-02 ↔ DEL-04-03 (added: RVG G1-M1)

**Rows.**

| Row | From → To | EvidenceQuote | Mirror |
|---|---|---|---|
| DEP-02-02-017 | 02-02 → 04-03 | "The workspace shall receive declaration, capability/checkpoint and content-bound record behavior through CLM-003 and CLM-004." | DEP-04-03-042 |
| DEP-04-03-035 | 04-03 → 02-02 | "the per-run run-start text and run-end line with their content identity and supply-check record, the selection record and the A15 descriptor's reviewed-content and prior-revision relations from `DEL-02-02`," | DEP-02-02-024 |

**Design.**
- WR RB-4a: "The A15 record itself is RS's: `relations.reviewedDraft` = {`draft`: the ID-3 string, …}".
- `RS_RECORD.schema.json` describes `reviewedDraft.draft` as "the reviewed content as WR's ID-3 string … WR keeps its internal draft-key object and writes this string".
- WR §7, DEL-04-03 row: "The A15 record is written by the act control's writer; the ledger cites it by record identity".

**Kind.**
- DEP-02-02-017 is I.
- DEP-04-03-035: G1 says E; RVG says I. **I confirm I.** RS's A15 relations and R3 fields take WR's formats, which RS does not define.
- **P9 is I–I.**

**Order.**
- WR descriptor and ID-3 → RS A15 and R3 fields → WR ledger, which cites RS record identity. **Projection artefact.**

**Move.**
- DEP-02-02-017 with its mirror: **RT** for the A15 act meaning, to DEL-04-01 ACT §2.4 and §2.5. DEP-02-02-016 is admitted already.
- **IV-S** for record identities.
- **ScopeOfWork: S1** in two ScopeOfWorks: DEL-02-02 REQ-005 / CLM-004, and DEL-04-03 REQ-005's list "and `DEL-01-04`, `DEL-02-02`, … do so in their own registers".
- No ownership moves.
- **Caveat.** As G1-m5: the register owner must accept the merge with DEP-02-02-016.

## 10. P11 — DEL-02-03 ↔ DEL-04-02

**Rows.**

| Row | From → To | EvidenceQuote | Mirror |
|---|---|---|---|
| DEP-02-03-029 | 02-03 → 04-02 | "`DEL-04-02`'s grant display states (including *set by person, not yet confirmed*, *unconfirmed* and *refused*), for recording A12 checkpoints (REQ-002, REQ-003);" | DEP-04-02-023 |
| DEP-04-02-017 | 04-02 → 02-03 | "It also consumes App v4 `DEL-03-02` proposal/outcome and direct-application origin semantics, `DEL-03-01` read-basis and standing facets, and `DEL-02-03` checkpoint recording annotations (with the hold-support values retained for the governance phase)." | DEP-02-03-034 |

**Design.**
- ACT-POLICY-v0.11 §2.5 already defines the relation EXEC needs: "**pending** (set by the person, not yet confirmed)", "**refused ⟨reason⟩** … The earlier established setting stays in force", "confirmation observation lost (*unconfirmed*) | Not until it is observed | **unknown**".
- EXEC §9.1 already takes "A12 binding and supersession (R4-6)" from DEL-04-01 through admitted DEP-02-03-012.
- AS-v0.9 §4: "Display meanings of the DEL-02-03 hold machine (EXEC §4), consumed from the record". This is rule-bearing on EXEC's vocabulary.

**Kind.** I and I/L confirmed.

**Order.**
- ACT §2.5 → EXEC §4.10 / SP-6 → AS §4 overlay. **Projection artefact.**

**Move.**
- DEP-02-03-029 with its mirror: **RT** to DEL-04-01 ACT §2.5.
- **ScopeOfWork: S1** in two ScopeOfWorks: DEL-02-03 CLM-002's consumption clause, and DEL-04-02 CLM-002 "Its visible autonomy state is received by … `DEL-02-03`".
- No ownership moves. DEL-02-03 CLM-002's "`DEL-04-02` owns grant display states" stays true.
- **Anchor.** ACT §2.5; EXEC-v0.7 §4.10.

## 11. P12 — DEL-02-03 ↔ DEL-04-03 (added: RVG G1-M1)

**Rows.**

| Row | From → To | EvidenceQuote | Mirror |
|---|---|---|---|
| DEP-02-03-013 | 02-03 → 04-03 | "Receive and faithfully record evidence of an actually performed checkpoint act using PKG-04's content/scope/purpose binding," | DEP-04-03-038 |
| DEP-04-03-025 | 04-03 → 02-03 | "checkpoint arrival, act request (where it can be identified), act and lapse events (with hold events retained for the governance phase) and compatibility reports from `DEL-02-03`," | DEP-02-03-035 |

**Design.**
- EXEC-v0.7 Changes R14-1: "**RS is the one record container.** `checkpoint-record-entries.schema.json` no longer defines a container: it defines the CE-1…CE-19 **bodies**, which RS format 0.1's entry kinds reference by relative path". The bodies are in "RS's camelCase; acts cited by RS record identity".
- `RS_RECORD.schema.json` "$ref"s ten or more EXEC `$defs` by relative path.
- EXEC's schema has no external `$ref`.

**Kind.** I–I confirmed, as RVG reads it. The format of the instances is defined by the supplier, not by the consumer.

**Order.**
- RS container, kinds and record identity → EXEC CE bodies → RS kind catalog (§13.3). **Projection artefact.**

**Move.**
- DEP-04-03-025 with its mirror: **IV**. This completes R14-1 as a registry.
- RS defines the kinds and the container. EXEC's root schema validates {RS kind, observed time, body}, as R14-1 already does. RS drops its `$ref`s into EXEC, and reader validation of bodies becomes a conformance check.
- **ScopeOfWork: S1** in two ScopeOfWorks: DEL-04-03 CLM-004's "receives … from `DEL-02-03`", and DEL-02-03 CLM-003's receivers list.
- No ownership moves. The bodies stay DEL-02-03's and the container stays DEL-04-03's.
- **Extension needed under RVG's readings.** The same registry move on DEP-04-03-022 (`settings_version`, "DEL-04-02's, referenced by $id"), DEP-04-03-026 and DEP-04-03-028. See §15.

## 12. P15 — DEL-03-01 ↔ DEL-04-03

**Rows.**

| Row | From → To | EvidenceQuote | Mirror |
|---|---|---|---|
| DEP-03-01-031 | 03-01 → 04-03 | "This catalog contract consumes the `DEL-04-03` act field set and lapse vocabulary that read results carry as standing (human-act evidence and lapse state)." | DEP-04-03-039 |
| DEP-04-03-023 | 04-03 → 03-01 | "subject content identities and method designations from `DEL-03-01`," | DEP-03-01-037 |

**Design.**
- C-v0.8 §6.2: "Human-act evidence (faithfully carried) | … carried with the whole DEL-04-03 act field set of RS-v0.8 §6.1, which this contract consumes and does not define or subset". "Lapse state | DEL-04-03 §7 vocabulary, consumed and not defined here".
- RS-v0.10 §7 L-1 takes c₁ from "subject content identity (DEL-03-01 §5.3)". L-2 rules on method designations.

**Kind.** I–I confirmed.

**Order.**
- C §5 identities → RS §7 rules and states → C §6.2 standing.
- C's use is carry-only. **Projection artefact.**

**Move.**
- DEP-03-01-031 with its mirror: **IV-S**. The C standing facet carries RS record references and the RS §7 lapse state by reference. Act meaning comes through the admitted DEP-03-01-024 (DEL-04-01).
- **ScopeOfWork: S1** in two ScopeOfWorks: DEL-03-01 CLM-002's sentence quoted above, and DEL-04-03 REQ-005.
- No ownership moves. This is consistent with R10-3's "does not define or subset".
- G1 shows DEP-03-01-031 is in every minimum set.
- **Not recommended:** re-targeting the lapse states to ACT §2.8. Its LC table says "the rules it gathers keep their own standing", so that would be an S2 move.

## 13. P17 — DEL-03-02 ↔ DEL-04-02

**Rows.**

| Row | From → To | EvidenceQuote | Mirror |
|---|---|---|---|
| DEP-03-02-034 | 03-02 → 04-02 | "It consumes `DEL-04-02`'s visible autonomy state (grant display states, grant value and scope, settings version identities) for origin and standing at drafting." | DEP-04-02-021 |
| DEP-04-02-015 | 04-02 → 03-02 | as DEP-04-02-017's quote ("It also consumes App v4 `DEL-03-02` proposal/outcome and direct-application origin semantics, …") | DEP-03-02-018 |

**Design.**
- P-v0.8 §3.3 records "Standing at drafting" and "Settings reference at route decision" as attribution.
- P §4.4 entry condition: "the host resolves, at validation, that the DEL-04-02 display state … is **effective (person-set) with grant value direct**".
- ACT §5.3: "Treatment is resolved on the **host route**".
- AS §12.1, DEL-03-02 row: "P records both references (P §3.3; RS §5)".

**Kind.** I–I confirmed.

**Order.**
- AS §3 → P §3.3 and §4.4 → AS §8 route and outcome facet. **Projection artefact.**

**Move.**
- DEP-03-02-034 with its mirror:
  - **RT** of P §4.4's rule to ACT §5.2 and §5.3 treatments ("apply directly"), which DEL-04-01 owns;
  - **IV-S** of the attribution carriage, or move it to the record (RS §5 and settings-in), linked by request.
- **ScopeOfWork: S1** in two ScopeOfWorks: DEL-03-02 CLM-004's last sentence, and DEL-04-02 CLM-002's receivers. The CLM-004 sentence was an optional item the owner accepted under Q-11 (SCA-V4-003), so the owner sees the reversal.
- No ownership moves.
- **Caveat.** ACT §5.1 itself lists "*grant state* for the class … DEL-04-02 (R-8; R2-6)" as an input. That is G2's A3. If A3 were entered as a row, this re-target would launder the cycle through DEL-04-01.

## 14. P21 — DEL-05-01 ↔ DEL-05-02

**Rows.**

| Row | From → To | EvidenceQuote | Mirror |
|---|---|---|---|
| DEP-05-01-020 | 05-01 → 05-02 | "catalog schemas; shared workflow/role/checkpoint meanings; record and human-act meanings; panel receiving needs; and host-specific native/loop evidence." | — |
| DEP-05-02-010 | 05-02 → 05-01 | "`DEL-05-01` supplies loop messages/tools/events/checkpoints and receiving requirements." | — |

**ScopeOfWork.**
- DEL-05-02 REQ-006 assigns "loop-event receiving definition to App-v4 `DEL-05-01`".
- DEL-05-01 REQ-005 lists the required inputs.

**Design.**
- LOOP-v0.9 §10.5: "DEP-05-01-020 has this deliverable consume DEL-05-02's statement of what the panel needs the loop to emit. That statement is PANEL-v0.8 §3.11 (LN-1…LN-17)". LOOP §10.5 then checks each row as "supplied" or "gap".

**Kind.** I/R and I confirmed.

**Order.**
- PANEL §3.11 needs → LOOP §2.3 events → PANEL OUT-001 receiving cases. **Projection artefact.**

**Move.**
- DEP-05-01-020: **IV**. LOOP owns the events. PANEL checks LOOP against LN-1…LN-17. §10.5 becomes PANEL's conformance check, and gaps revise LOOP by version.
- **ScopeOfWork: S1** in DEL-05-01 REQ-005, and the generic consuming sentence of CLM-002 for DEL-05-02. No mirror.
- No ownership moves.

## 15. Do the moves together make SCC-002 acyclic?

> **2026-10-04 extension.** This section used G1 r1's kinds (sha256 `4e85ac79…`), with RVG's readings as a variant. The recomputation under G1 r2's kinds, with the 17-pair move set, is §20.6, and it supersedes this table for r2.

**Model.**
- The 71 held arcs, with G1's primary kinds.
- Variant "RVG": DEL-04-03's received list read as I. Those rows are DEP-04-03-022, -024, -025, -026, -028, -035 and -036.
- Each option keeps O-1: all kinds; O-2: no V; O-3: no V or L; O-4: P and I only.
- Moves remove an arc. A residual leaves the arc with the residual kind: P1 V, P8 V, P4 L.
- Re-targets point into DEL-04-01. They are cycle-safe because DEL-04-01 has 0 suppliers, which I checked.

**Results.** "Rows" is the minimum number of further cycle-closing rows. "Pairs left" are the reciprocal pairs still inside a component.

| Scenario | O-1 | O-2 | O-3 | O-4 |
|---|---|---|---|---|
| G1 kinds, 11 moves (original brief) | 12 members, 13 rows; pairs left P1 P2 P4 P8 P9 P10 P12 P13 P14 P16 P18 P19 P20 | {02-01, 03-02} 1 + 6 members 6; P4 P9 P10 P12 P13 P18 P19 | 6 members, 6 rows; P9 P10 P12 P13 P18 P19 | **acyclic** |
| G1 kinds, 13 moves | 12 / 12; P1 P2 P4 P8 P10 P13 P14 P16 P18 P19 P20 | 2/1 + 5/5; P4 P10 P13 P18 P19 | 5 / 5; P10 P13 P18 P19 | **acyclic** |
| RVG kinds, 13 moves | 12 / 12; as above | 2/1 + 5/5 | 5 / 5 | 5 members, 1 row: {02-03, 03-03, 04-02, 04-03, 05-01}, through the other RS receive rows |
| RVG kinds, 13 moves + registry move on DEP-04-03-022, -026, -028 (the minimal subset; whole list gives the same) | 12 / 9; P1 P2 P4 P8 P10 P13 P14 P16 P19 | 2/1 + 4/3; P4 P10 P13 P19 | 4 / 3; P10 P13 P19 | **acyclic** |
| The previous row + DEC of P4 (either kinds) | 12 / 8; P1 P2 P8 P10 P13 P14 P16 P19 | 4 / 3; P10 P13 P19 | 4 / 3; P10 P13 P19 | **acyclic** |

**Reading.**
1. **O-4.** The moves close SCC-002. Under G1's kinds the 11 moves alone close it. Under RVG's readings three further registry moves on RS's received list are needed (DEP-04-03-022, -026, -028). They are the same no-ownership pattern as P12.
2. **O-3.** P10 (DEP-02-03-026 E), P13 (DEP-02-03-022 E/L) and P19 (DEP-04-02-018 E/I) remain. P18 also remains without the registry extension. These are G1's non-I–I pairs, with G1's candidate moves of invert or cut.
3. **O-2.** As O-3, plus P4. P4's L residual stays on the same arc, so it needs DEC (or IV-O or MRG).
4. **O-1.** As O-2, plus three groups:
   - the V residuals of P1 and P8;
   - the V and L rows of P2 (DEP-02-03-027), P14 (DEP-03-01-026) and P16 (DEP-03-01-030);
   - P20 without the registry extension.

   Under O-1 these need owner cuts or decomposition. They are not agent moves.
5. **Sensitivity (RVG G1-n2).** DEP-04-02-018 (P19) read as I would stay under O-4, and needs its own move (G1: invert). I did not compute that variant beyond noting it.

## 16. G2's SCC-forming rows that touch SCC-002 (G1 §2b)

Computed over admitted ∪ held (212 arcs), with the moves applied, RVG kinds and the registry extension. Each item was added alone. Admitted arcs are kept, so the results are upper bounds, as in G1 §2b.

| Item | O-1 | O-4 | Effect on the conclusion |
|---|---|---|---|
| N22 (02-01 → 01-04, V) | stays inside the 12-member residual | leaves | None |
| A1 (04-03 → 01-04, E) | inside | leaves | None under G1's kinds. Under RVG's K-3 repair it is another RS receive row: same registry move |
| N26 (01-01 → 02-03, I/R) | 16 members (adds 01-01, 01-02, 01-03, 09-01) | **7-member SCC** (01-01, 01-02, 01-03 with members) | Needs the same move as P6 and P7: EXEC's "which native items … EXEC uses" is consumer-needs feedback (IV). Otherwise `dependency-extract` records it as a reference |
| N27 (01-01 → 03-03, E; RVG G1-m3 reads P or I) | 16 | leaves as E | As P or I it would need its own move. Not analysed here |
| A2, A3 (DEL-04-01 → members, E) | 15 (adds 04-01, 01-02, 01-03) | leave as E | **Could change the conclusion.** Read as I, a 12-member SCC including DEL-04-01 forms under O-4, and the re-targets of P5, P9, P11 and P17 fail. Owner decision Q-5 ("DEL-04-01 gains no supplier") stands against them. ACT §5.1 lists DEL-04-02's grant state as an input, which is A3's content. The re-targets rely on Q-5 continuing to hold |

## 17. The drafted DAG-004 evidence update

`APP-V4-SCA003-20261002/DAG_PREP/CASE-002_EVIDENCE_UPDATE.proposed.md` (not applied) records three things:
- the DAG-004 member-set match (13 members, unchanged);
- the internal account of 128 rows, 71 arcs and 21 pairs;
- the five new held arcs.

This analysis uses the same accepted DAG-004 `CandidateEdges.csv` and agrees with its counts. Its new pairs are mine:
- NR-09 / X-1 is P2;
- R2-04-03-e is P5;
- R20-10 is P9.

The two **neither supersede nor depend on each other**. The drafted update is the membership record that this analysis presupposes. It should be applied first, or together with any case update that cites this file. Nothing here changes its content.

## 18. Summary

> **2026-10-04 extension.** The table and counts below cover the first 13 pairs. §20.7 gives the summary for all 17 I–I pairs of G1 r2, and it supersedes the counts below.

| Pair | Kind confirmed | Contradiction or artefact | Proposed move | ScopeOfWork effect | Anchor contract |
|---|---|---|---|---|---|
| P1 01-04 ↔ 02-02 | I–I (02-02's need is integration) | Artefact | IV-S DEP-02-02-013 (+DEP-01-04-010); V residual | S1 ×2, no ownership move | WR-v0.2 §7, §8, `workspace-registration.schema.json` |
| P3 02-01 ↔ 02-03 | I–I; DEP-02-01-026 boundary L (TBD-004 point of need) | Artefact | IV DEP-02-01-026 (+DEP-02-03-030) | S1 ×2, none | EXEC-v0.7 §2.1, §3.6; WD-v0.9 §4.3.0–§4.3.1 |
| P4 02-01 ↔ 03-02 | I and I/L | Artefact, but two definitional concerns | O-3/O-4: IV-S DEP-03-02-027 with L residual. O-1/O-2: **DEC** of DEL-02-01 (or IV-O, MRG) | S1 ×2 (O-3/O-4); decomposition change (O-1/O-2) | WD-v0.9 §6.1 `$defs/workflow_identity`; P-v0.8 §3.3, §4.3 |
| P5 02-01 ↔ 04-03 | I–I | Artefact | RT DEP-02-01-019 to DEL-04-01 (+DEP-04-03-037) | S1 ×1 (DEL-04-03 REQ-005), none; register-owner caveat G1-m5 | ACT-POLICY-v0.11 §2.4, §2.6 |
| P6 02-01 ↔ 05-01 | I/R and I | Artefact | IV DEP-02-01-020 | S1 ×1, none | WD-v0.9 §4.3, §6, §8, §9 |
| P7 02-01 ↔ 05-02 | I/R and I | Artefact | IV DEP-02-01-021 | S1 ×1, none | WD-v0.9 §4.2.4, §4.3.4, §6 |
| P8 02-02 ↔ 02-03 | I–I (DEP-02-02-015 mixes WR's own output) | Artefact | IV-S DEP-02-02-015 (+DEP-02-03-031); V residual | S1 ×2, none | WR-v0.2 §7, §8, §16 |
| P9 02-02 ↔ 04-03 | I–I (DEP-04-03-035 I, per RVG) | Artefact | RT + IV-S DEP-02-02-017 (+DEP-04-03-042) | S1 ×2, none; G1-m5-type caveat | ACT §2.4–§2.5; RS A15 form (RB-4a) |
| P11 02-03 ↔ 04-02 | I and I/L | Artefact | RT DEP-02-03-029 to DEL-04-01 (+DEP-04-02-023) | S1 ×2, none | ACT §2.5 A12 control relations; EXEC §4.10 |
| P12 02-03 ↔ 04-03 | I–I (DEP-04-03-025 I, per RVG) | Artefact | IV DEP-04-03-025 (+DEP-02-03-035): registry completing R14-1 | S1 ×2, none | EXEC R14-1; `checkpoint-record-entries.schema.json`; RS §13 |
| P15 03-01 ↔ 04-03 | I–I | Artefact | IV-S DEP-03-01-031 (+DEP-04-03-039) | S1 ×2, none | C-v0.8 §6.2; RS-v0.10 §6.1, §7 |
| P17 03-02 ↔ 04-02 | I–I | Artefact | RT + IV-S DEP-03-02-034 (+DEP-04-02-021) | S1 ×2, none; reverses an owner-accepted optional item (Q-11) | ACT §5.2–§5.3; P-v0.8 §3.3, §4.4 |
| P21 05-01 ↔ 05-02 | I/R and I | Artefact | IV DEP-05-01-020 | S1 ×1, none | LOOP-v0.9 §2.3, §10.5; PANEL-v0.9 §3.11 |

**Counts.**
- No pair is a real ordering contradiction. All 13 have a part-level order in the current Designs.
- 12 pairs close by moves that move no definitional ownership: IV (P3, P6, P7, P12, P21), RT (P5, P11), IV-S (P1, P8, P15), RT with IV-S (P9, P17).
- Each needs S1 ScopeOfWork wording in one or two ScopeOfWorks, so each goes through an SCA the owner accepts.
- Five of the 12 are conditional on `dependency-extract` accepting carriage by reference as not a contract input (P1, P8, P9, P15, P17).
- Four rely on Q-5 (P5, P9, P11, P17).
- P1 and P8 leave a V residual.
- **P4 needs a decomposition change (or an ownership-moving inversion, or merge) under O-1 and O-2.** Under O-3 and O-4 it closes by IV-S, because its residual is L.
- G1's flag that "SCC-002 may need a decomposition change" is therefore **confirmed for exactly one pair under O-1 and O-2, and not needed under O-3 and O-4**.

## 19. Not established

| Item | Why |
|---|---|
| Whether `dependency-extract` treats carriage by reference as no contract input | A register-owner judgment. If it does not, P1, P8 and P15 (and parts of P9 and P17) fall back to DEC or an owner ruling on edge semantics |
| Whether WD's further citations of EXEC (§4.3.4 run end, §6.4) are inputs | Read only as far as P3 needs. They are design reliance beyond the register row |
| Kinds of mirror rows beyond the 26 on these arcs | Mirrors were identified, and their sentences read for P1, P3, P5, P9, P11, P12 and P17 only |
| The split line of the P4 decomposition | A proposal for `scope-change`. No sizing or work-unit files are drafted |
| P10, P13, P18, P19, P20 under RVG's readings, and DEP-04-02-018 as I | Outside this brief's pairs. Counted in §15 only |
| Whether the S1 revisions keep every AC and VER intact | Checked against the quoted clauses only (for example DEL-02-01 AC-005). A full trace is `scope-of-work`'s |

## 20. 2026-10-04 extension: G1 r2 and the four added pairs

**Why this section exists.**
- G1 r2 (`SURVEY/G1.md`, sha256 `8afa6093cbd0f09dccc6ef53e1a0c6fb35efbbe17729f5b0ca0407792ffcfc61`, commit `c0a892137a`) applies the repaired K-3 rule to every row.
- It finds 17 I–I pairs in SCC-002: the 13 above, plus P10, P18, P19 and P20.
- This section analyses those four pairs by the method of §1 and recomputes closure under r2's kinds.
- §1–§19 are unchanged, except for one pointer line at §15 and one at §18.
- §15's first table and the counts in §18 were computed with G1 r1's kinds.

**Checks.**
- Under r2, the primary kinds of the 71 SCC-002 held rows are 66 I, 3 V, 1 E and 1 L, parsed from r2's §2.2 table.
- Without moves, my computation reproduces r2: O-1 gives 13 members and 21 rows; O-2 and O-3 give 12 members and 18 rows; O-4 gives 12 members and 17 rows.
- All eight rows of the four pairs were read from the live registers. They are quoted below.

### 20.1 P10 — DEL-02-03 ↔ DEL-03-03

**Rows.**

| Row | From → To | EvidenceQuote | Statement (excerpt) | Mirror |
|---|---|---|---|---|
| DEP-02-03-026 | 02-03 → 03-03 | "`DEL-03-03`'s observations of checkpoint arrivals and act records on the external channel, which this slice records (REQ-002, REQ-003);" | "…; this slice does not define the external-channel receiving." | — |
| DEP-03-03-014 | 03-03 → 02-03 | "and App `DEL-02-03`'s checkpoint statement and required-tool check for the current phase and, for the governance phase, its hold machine and hold-support values;" | "in the current phase a checkpoint on this channel is plan guidance and no hold is claimed" | DEP-02-03-032 |

**ScopeOfWork.**
- DEL-02-03 CLM-002: "`DEL-03-03` owns external-channel receiving, including the governance-phase carriage assurance". The same claim states: "This slice consumes, and does not define: … `DEL-03-03`'s observations of checkpoint arrivals and act records on the external channel".
- DEL-03-03 CLM-002 says the adapter consumes "App `DEL-02-03`'s checkpoint statement and required-tool check for the current phase".

**Design.**
- ADAPTER-v0.7 §7.7: "The adapter passes observations CO-1…CO-11 and writes no checkpoint entry."
- ADAPTER §11 "Provide to | DEL-02-03": "CO-1…CO-11 (§7.7), each naming the EXEC-v0.6 §2.4.2 event it is input to, with `checkpoint_observation.schema.json`".
- That schema's `exec_event` is described as "The EXEC-v0.6 §2.4.2 event this observation is input to". The schema has no external `$ref`.
- EXEC-v0.7 §9.1, DEL-03-03 row: "§2.5 covers kinds (a)–(c) on X for both native paths (R12-4), using ADAPTER §4.1 NM-1/NM-2, §4.5 and OC-9".

**Kind.** Confirmed: DEP-02-03-026 is I (the observation format is the supplier's, and EXEC "does not define" it). DEP-03-03-014 is I/L.

**Order.**
- EXEC §2.4.2's CE events come first. ADAPTER §7.7's CO observations name the CE each feeds. EXEC §2.5's X-path rows come last.
- ADAPTER's observation contract depends on EXEC's event list. EXEC's events do not depend on ADAPTER.
- **Projection artefact.**

**Move.**
- DEP-02-03-026: **IV-S**.
  - EXEC's recorder inputs are the published interface (§2.4.2 and `checkpoint-record-entries.schema.json`).
  - ADAPTER's observations conform to them. They already name `exec_event`.
  - EXEC carries the CO observations by reference.
- **Condition.** EXEC §2.5's X-path rows read ADAPTER's native-path semantics (NM-1/NM-2, §4.5, OC-9), which makes them rule-bearing. They must become citations of ADAPTER §7.7's CO→CE mapping.
  - DEL-03-03 owns external-channel receiving, so this is consistent with DEL-02-03 CLM-002.
  - If EXEC keeps defining the X path from ADAPTER's semantics, the move becomes IV-O.
- **ScopeOfWork: S1**, one sentence: DEL-02-03 CLM-002's "consumes, and does not define" clause. There is no mirror.
- No ownership moves.
- **Anchor.** EXEC-v0.7 §2.4.2, `checkpoint-record-entries.schema.json`; ADAPTER-v0.7 §7.7, `checkpoint_observation.schema.json`.

### 20.2 P18 — DEL-04-02 ↔ DEL-04-03

**Rows.**

| Row | From → To | EvidenceQuote | Statement (excerpt) | Mirror |
|---|---|---|---|---|
| DEP-04-02-008 | 04-02 → 04-03 | "including changed-content lapse received from the record owner" (DEL-04-02 VER-004) | "Receive the App DEL-04-03 run-record contribution, including recorded settings, attributable human-act evidence and changed-content lapse, for comparison and evidence-bounded display." | DEP-04-03-014 |
| DEP-04-03-022 | 04-03 → 04-02 | "settings-in from `DEL-04-02`," | "Receive settings-in from App DEL-04-02 for the run record." | DEP-04-02-009 |

**ScopeOfWork.**
- DEL-04-02 CLM-002: "App v4 `DEL-04-03` … defines the run/human-act format and produces the App reader/writer and content-change lapse handling. This deliverable consumes those policy and record contributions."
- DEL-04-03 CLM-004 lists "settings-in from `DEL-04-02`".
- The mirror DEP-04-02-009 rests on DEL-04-02 REQ-002: "pass/receive the settings needed by the run-record contribution owned in CLM-002".

**Design.**
- AS-v0.9 §6: "Identical to DEL-04-03/RS-v0.8 §8. A data exchange, not an ordering between human acts and not a second authority."
- RS-v0.10 §8: "Identical in DEL-04-02/AS-v0.8 §6."
- `RS_RECORD.schema.json` has `"$ref": "urn:chirality:app-v4:del-04-02:settings-in:0.1#/$defs/settingsVersion"`. This is its only external reference other than EXEC's bodies.
- AS §8 shows the RS §7 lapse states in its human-act facet.

**Kind.**
- DEP-04-03-022 is I: RS carries a body it does not define.
- DEP-04-02-008 is I/V. Its quote sits in VER-004, but its SourceRef includes CLM-002 and its Statement names "display", which is AS's own output. I apply RVG's precedence: the quote decides content, and the Statement or SourceRef decides the point of need. On that reading the kind is I primary. This is a boundary call.

**Order.**
- AS's settings body comes first, then RS's `settings_version` entry, then the record-out that AS compares and displays.
- RS §7's lapse states feed AS §8 independently.
- **Projection artefact.**

**Move.**
- DEP-04-03-022 with its mirror DEP-04-02-009: **IV**.
- This is the registry pattern of P12. RS's container defines the `settings_version` kind. AS's `AS_SETTINGS_IN.schema.json` body conforms to it. RS drops its `$id` reference, and body validation becomes a conformance check.
- §6 and §8 hold one text twice. RS §8 should own the exchange and AS §6 the settings body.
- **ScopeOfWork: S1**, two sentences: DEL-04-03 CLM-004's receives clause and DEL-04-02 REQ-002's supply sentence.
- No ownership moves. The settings-in content stays DEL-04-02's, and the format stays DEL-04-03's.
- **Anchor.** RS-v0.10 §8, §13; AS-v0.9 §6; `AS_SETTINGS_IN.schema.json`.

**Settled: P18 drops with the RS registry move.**
- In this move set, DEP-04-03-022 closes the pair.
- G1 lists DEP-04-02-008 as in every minimum set. That holds for the base graph without moves, not for this move set.
- If DEP-04-02-008 is moved instead (IV-S of the record-out), then under r2 kinds O-4 still leaves a 4-member component that needs DEP-04-03-022 (§20.6, last check). So DEP-04-03-022 is the move. DEP-04-02-008 is not an alternative.

### 20.3 P19 — DEL-04-02 ↔ DEL-05-01

**Rows.**

| Row | From → To | EvidenceQuote | Mirror |
|---|---|---|---|
| DEP-04-02-018 | 04-02 → 05-01 | "It also consumes, from App v4 `DEL-05-01`, a host agent's network-destination allow list, in-work destination grants and contacted-destination record, which `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-5` requires to be shown." | — |
| DEP-05-01-025 | 05-01 → 04-02 | "`DEL-04-02` owns the autonomy-grant display states and standing exchange, which this deliverable consumes as the grant in force carried on each dispatch;" | DEP-04-02-019 |

**Statement.** DEP-05-01-025's Statement ends "this deliverable does not define those states". Its mirror rests on DEL-04-02 CLM-002: "Its visible autonomy state is received by `DEL-05-01`, …".

**Design.**
- AS-v0.9 §3.1 states that the in-work grant rules and the request states "*pending · granted · declined · not granted · unanswered at end*, are DEL-05-01/LOOP-v0.8 §5.3 DF-5 and DF-6". AS's display transitions DG-1…DG-6 map those states. This is rule-bearing.
- AS §12.1, DEL-05-01 row: "**Grant in force per dispatch** (defined here) … The loop carries it on the dispatch record (LOOP §6.2) and relays intent; the host route resolves treatment". This is carry-only.
- `LOOP_DESTINATION_REQUEST.schema.json` is LOOP's own, with no external `$ref`.

**Kind.** Confirmed: both rows are I. Each consumer states that it does not define what it receives.

**Order.**
- LOOP §5.3 DF-5 and DF-6 come first, then AS §3.1, §3.2 and §12.1, then LOOP §6.2's dispatch record.
- **Projection artefact.**

**Move.**
- DEP-05-01-025 with its mirror DEP-04-02-019: **IV-S**. LOOP's dispatch record carries AS's grant in force by settings-version reference, which it already only "relays".
- **ScopeOfWork: S1**, two sentences: DEL-05-01 CLM-002 and REQ-006's consumption clause, and DEL-04-02 CLM-002's receivers list.
- No ownership moves.
- **Alternative.** DEP-04-02-018 also closes the pair under every option (§20.6). It is rule-bearing on LOOP's DF-6 states, so its only clean form is IV-S of AS's display, which is the same condition.
- The meaning of a destination grant is ACT §2.7. LOOP already consumes it through the admitted row DEP-05-01-018.
- **Anchor.** LOOP-v0.9 §5.3, §6.2, `LOOP_DESTINATION_REQUEST.schema.json`; AS-v0.9 §3.1, §12.1.

### 20.4 P20 — DEL-04-03 ↔ DEL-05-01

**Rows.**

| Row | From → To | EvidenceQuote | Statement (excerpt) | Mirror |
|---|---|---|---|---|
| DEP-04-03-028 | 04-03 → 05-01 | "a host agent's network-destination events (destination contacted, destination grant, destination declined) from `DEL-05-01` (`APP-V4-SWBPIPE-INTAKE-20260928-DECISION-5`);" | — | — |
| DEP-05-01-019 | 05-01 → 04-03 | "Review checkpoint/event/evidence examples against adopted workflow, policy and record inputs." (VER-008) | "Receive adopted shared human-act/run-record meanings and format for loop event/checkpoint and record receiving definitions and examples" | DEP-04-03-029 |

**Design.**
- RS-v0.10 header: "element **R15** records, for a host's agent, each destination contacted …".
- RS Changes, B5: "R15 joined to the one destination flow … new PROPOSED element **destination request closed** (`destination_request_closed`: *not granted* with reason, or *unanswered at end* with cause; LOOP DF-6)".
- The entry kinds are RS's, in `RS_RECORD.schema.json` and `RS_RECORD.valid.host-destinations.example.jsonl`. The state values inside them are LOOP's DF-6 values.
- LOOP-v0.9 §10.4, DEL-04-03 row: "§2.3; E-4; §5.3 DF-8 (entry kinds, including `destination_request_closed`, v0.8)".

**Kind.**
- DEP-04-03-028 is I: RS does not define the DF-6 states it records.
- DEP-05-01-019 is I/V. Its quote is VER-008, but its Statement and its SourceRef (CLM-002, REQ-007) name the definitions. This is a boundary call, as RVG noted.

**Order.**
- LOOP §5.3 DF-5 and DF-6 come first, then RS R15 and its kinds, then LOOP DF-8 and its examples.
- **Projection artefact.**

**Move.**
- DEP-04-03-028: **IV**, the registry pattern of P12.
  - RS's container owns the R15 entry kinds.
  - LOOP's destination events are emitted as R15 entries.
  - The DF-6 state values inside `destination_request_closed` are carried by reference (an IV-S element).
- **ScopeOfWork: S1**, one sentence: DEL-04-03 CLM-004's receives clause. There is no mirror.
- No ownership moves.
- **Anchor.** RS-v0.10 §4 R15, §13; LOOP-v0.9 §5.3 DF-6, DF-8.

**Settled: P20 drops with the RS registry move.** DEP-04-03-028 is extension row M-X3 of the first version, now a pair move.

### 20.5 Extension row M-X2 is needed under r2

- DEP-04-03-026 is in no reciprocal pair. It carries "external dispatch entries from `DEL-03-03`", and r2 classes it I.
- With the 17 pair moves but without it, O-4 leaves the 5-member component {02-03, 03-03, 04-02, 04-03, 05-01}, closed by that one row.
- The same registry move (M-X2) closes it. No ownership moves, and the ScopeOfWork effect is S1 in DEL-04-03 CLM-004 and DEL-03-03's supply sentence (mirror DEP-03-03-019).
- I did not read ADAPTER's `external_dispatch_record.schema.json` in detail for this row. That is recorded in §20.8.

### 20.6 Closure under G1 r2's kinds

**Model.**
- As §15, over the 71 held arcs with r2's primary kinds.
- O-1 keeps every kind. O-2 drops V, O-3 drops V and L, and O-4 keeps P and I only.
- r2 applies each option graph-wide. No admitted arc lies inside SCC-002, so the held-only computation is exact for this component.
- Move set: the 13 pair moves of §2–§14, plus P10 (DEP-02-03-026), P18 (DEP-04-03-022), P19 (DEP-05-01-025), P20 (DEP-04-03-028), plus M-X2 (DEP-04-03-026).
- Residuals: P1 and P8 leave V. P4 leaves L on DEP-03-02-027.

| Scenario (r2 kinds) | O-1 | O-2 | O-3 | O-4 |
|---|---|---|---|---|
| No moves | 13 members, 21 rows | 12, 18 | 12, 18 | 12, 17 |
| 17 pair moves, without M-X2 | 12, 8 | {02-01, 03-02} 1 + 5-member 2 | 5-member 2 | 5-member 1 (DEP-04-03-026) |
| **17 pair moves + M-X2** | **12 members, 7 rows**: P1, P2, P4, P8, P13, P14, P16 (rows DEP-02-02-013, -02-02-015, -02-01-029, -02-03-027, -02-03-022, -03-01-026, -03-01-030) | **P4 (DEP-02-01-029) and P13 (DEP-02-03-022)**, two 2-member components | **P13 only**: {02-03, 05-01}, DEP-02-03-022 | **acyclic** |
| + DEC of P4 | 12, 6: P1, P2, P8, P13, P14, P16 | P13 only | P13 only | acyclic |
| + DEC of P4, with P1 and P8's V residuals not entered as rows | 12, 4: P2, P13, P14, P16 | P13 only | P13 only | acyclic |
| Check: P19 by DEP-04-02-018 instead | as the bold row | P4; P13 (3 members) | P13 (3 members) | acyclic |
| Check: P18 by DEP-04-02-008 instead | 12, 8 | P4; 4-member 2 | 4-member 2 | 4-member 1 (DEP-04-03-022): **does not close** |

**Reading.**
1. **O-4: SCC-002 closes.** It needs the 17 pair moves plus M-X2. None moves definitional ownership.
2. **O-3: one row remains.** It is P13's DEP-02-03-022, E/L in r2. It stays E because the consumer, DEL-02-03, defines the format. It is the only IMPLICIT/MEDIUM held row. G1 r2's candidate is an owner cut or confirmation by its register owner.
3. **O-2: as O-3, plus P4.** P4's L residual stays on its arc, so it needs DEC, IV-O or MRG.
4. **O-1: as O-2, plus five rows.** These are the V residuals of P1 and P8, and the V and V/L rows of P2, P14 and P16. Owner cuts, or a decomposition, decide them.
5. **P18 and P20 are settled.** Both drop with the RS registry moves (§20.2, §20.4). P18 must close through DEP-04-03-022, not DEP-04-02-008.

### 20.7 Summary for the 17 I–I pairs (G1 r2)

The rows for P1–P17 except P10 are as in §18. Rows P10, P18, P19 and P20 are added.

| Pair | Kind confirmed | Contradiction or artefact | Proposed move | ScopeOfWork effect | Anchor contract |
|---|---|---|---|---|---|
| P1 01-04 ↔ 02-02 | I–I | Artefact | IV-S DEP-02-02-013 (+DEP-01-04-010); V residual | S1 ×2, no ownership move | WR-v0.2 §7, §8 |
| P3 02-01 ↔ 02-03 | I–I (boundary L) | Artefact | IV DEP-02-01-026 (+DEP-02-03-030) | S1 ×2, none | EXEC-v0.7 §2.1, §3.6; WD-v0.9 §4.3.0–§4.3.1 |
| P4 02-01 ↔ 03-02 | I and I/L | Artefact; two definitional concerns | O-3/O-4: IV-S DEP-03-02-027 (L residual). O-1/O-2: **DEC** of DEL-02-01 (or IV-O, MRG) | S1 ×2 / decomposition change | WD-v0.9 §6.1; P-v0.8 §3.3, §4.3 |
| P5 02-01 ↔ 04-03 | I–I | Artefact | RT DEP-02-01-019 to DEL-04-01 (+DEP-04-03-037) | S1 ×1, none | ACT-POLICY-v0.11 §2.4, §2.6 |
| P6 02-01 ↔ 05-01 | I/R and I | Artefact | IV DEP-02-01-020 | S1 ×1, none | WD-v0.9 §4.3, §6, §8, §9 |
| P7 02-01 ↔ 05-02 | I/R and I | Artefact | IV DEP-02-01-021 | S1 ×1, none | WD-v0.9 §4.2.4, §4.3.4, §6 |
| P8 02-02 ↔ 02-03 | I–I | Artefact | IV-S DEP-02-02-015 (+DEP-02-03-031); V residual | S1 ×2, none | WR-v0.2 §7, §8, §16 |
| P9 02-02 ↔ 04-03 | I–I | Artefact | RT + IV-S DEP-02-02-017 (+DEP-04-03-042) | S1 ×2, none | ACT §2.4–§2.5; WR RB-4a |
| **P10 02-03 ↔ 03-03** | I and I/L | Artefact | IV-S DEP-02-03-026 | S1 ×1, none (IV-O if EXEC keeps defining the X path) | EXEC-v0.7 §2.4.2; ADAPTER-v0.7 §7.7, `checkpoint_observation.schema.json` |
| P11 02-03 ↔ 04-02 | I and I/L | Artefact | RT DEP-02-03-029 to DEL-04-01 (+DEP-04-02-023) | S1 ×2, none | ACT §2.5; EXEC §4.10 |
| P12 02-03 ↔ 04-03 | I–I | Artefact | IV DEP-04-03-025 (+DEP-02-03-035), registry | S1 ×2, none | EXEC R14-1; RS §13 |
| P15 03-01 ↔ 04-03 | I–I | Artefact | IV-S DEP-03-01-031 (+DEP-04-03-039) | S1 ×2, none | C-v0.8 §6.2; RS-v0.10 §6.1, §7 |
| P17 03-02 ↔ 04-02 | I–I | Artefact | RT + IV-S DEP-03-02-034 (+DEP-04-02-021) | S1 ×2, none; reverses Q-11 optional item | ACT §5.2–§5.3; P-v0.8 §3.3, §4.4 |
| **P18 04-02 ↔ 04-03** | I/V and I | Artefact | IV DEP-04-03-022 (+DEP-04-02-009), registry (= M-X1) | S1 ×2, none | RS-v0.10 §8, §13; AS-v0.9 §6; `AS_SETTINGS_IN.schema.json` |
| **P19 04-02 ↔ 05-01** | I–I | Artefact | IV-S DEP-05-01-025 (+DEP-04-02-019); alternative DEP-04-02-018 | S1 ×2, none | LOOP-v0.9 §5.3, §6.2; AS-v0.9 §3.1, §12.1 |
| **P20 04-03 ↔ 05-01** | I and I/V | Artefact | IV DEP-04-03-028, registry (= M-X3) | S1 ×1, none | RS-v0.10 §4 R15, §13; LOOP-v0.9 §5.3 DF-6, DF-8 |
| P21 05-01 ↔ 05-02 | I/R and I | Artefact | IV DEP-05-01-020 | S1 ×1, none | LOOP-v0.9 §2.3, §10.5; PANEL-v0.9 §3.11 |
| Non-pair (r2) | DEP-04-03-026 I | — | IV, registry (M-X2) | S1 ×2, none | RS-v0.10 §13 |

**Counts for the 17 pairs.**
- **None is a real ordering contradiction.**
- **16 close by moves that move no definitional ownership**:
  - IV: P3, P6, P7, P12, P18, P20, P21;
  - RT: P5, P11;
  - IV-S: P1, P8, P10, P15, P19;
  - RT with IV-S: P9, P17.
- Each needs S1 wording in one or two ScopeOfWorks, through an SCA the owner accepts.
- Seven depend on `dependency-extract` accepting carriage by reference as not a contract input: P1, P8, P10, P15 and P19, and parts of P9 and P17.
- Four rely on Q-5: P5, P9, P11 and P17.
- **One, P4, needs a decomposition change (or IV-O, or merge) under O-1 and O-2.** It closes by IV-S under O-3 and O-4.

### 20.8 Not established (extension)

| Item | Why |
|---|---|
| Whether EXEC §2.5's X-path rules can become citations of ADAPTER §7.7 without moving design responsibility | Read at §9.1 and §7.7 level only. If they cannot, P10 is IV-O |
| `external_dispatch_record.schema.json` and RS's R-entry for external dispatch (M-X2) | Only the register row and RS §10.1 were read |
| Whether `RS_RECORD.schema.json` and `AS_SETTINGS_IN.schema.json` can drop the cross-`$id` without loss | Schema structure inspected for `$ref`s only |
| The boundary kinds DEP-04-02-008 (I/V) and DEP-05-01-019 (I/V) | Both quotes are VER sentences. RVG's precedence (quote for content, Statement or SourceRef for point of need) gives I. Neither affects closure in the move set of §20.6 |

## 21. 2026-10-04 repair (RVG-C2, GC-1, GC-2)

**Standing.** This section repairs §1–§20 under review RVG-C2 (`reviews/RVG-C2.md`, sha256 `48db63309c3f057169f2b37390e95a210ae406f2faa0dee6df520d174a155dba`, commit `a0b44aa744`, verdict REPAIR). It also applies HELP_HUMAN's rulings GC-1 and GC-2 (`GC_RULINGS.md`, sha256 `dd92df3686755f340321b8a1b0a57919660221b8d0ad324e9254f0db19a4ed9a`).

Nothing above is deleted. Where this section and an earlier one differ, **this section supersedes** it. The superseded parts are:

| Superseded | By |
|---|---|
| §1: the IV-S condition ("`dependency-extract` must accept …") | GC-1 |
| §1 and §16: RT's "Condition: Q-5 holds" | §21.2 |
| §4 and §20.7: P4's move and its "decomposition change" reading | §21.4 |
| §10: P11's re-target | §21.3 |
| §20.1: P10's move | §21.5 |
| §9, §12, §13, §20.3: the IV-S parts of P9, P15, P17 and P19 | §21.1 |
| §3: P3's residual | §21.6 |
| The registry moves of §11, §20.2, §20.4 and §20.5 | §21.6 |
| The counts of §18 and §20.7, and the closure table of §20.6 | §21.7 and §21.8 |

The artefact verdicts and every closure number computed so far stand; RVG reproduced them.

**Kinds and script.** Kinds are G1 r2's throughout. The closure script is the one used in §20.6, with the repaired move set below.

### 21.1 M1 — the IV-S pairs re-tested against GC-1

**The test (GC-1).** A slot inversion removes the contract input only when both conditions hold:
- **(a) the reference is opaque:** "The consumer's Design uses no field, state value or identity scheme that the supplier defines";
- **(b) conformance is checked outside the consumer's definition:** by the supplier or a third party, or the consumer's own check is recorded as V.

Where (a) fails, the move is IV-O, decomposition or merge, unless the consumer's Design is reworded. A rewording is a design change by that deliverable's design agent, and it is reviewed.

| Pair (row) | (a) today | (b) | Rewording that would make (a) hold, with owner | Result |
|---|---|---|---|---|
| P1 (DEP-02-02-013) | Holds. WR's intake is the built view plus a capture report holding WR's own descriptor identity, a capture-evidence reference, and a record identity from a third party (DEL-04-03) | V residual (WR-VC-01), recorded | None needed | **IV-S holds.** V residual under O-1 |
| P8 (DEP-02-02-015) | Holds. WR shows EXEC's report "labelled"; "nothing is gated by it (CC-3)" | V residual (REQ-005 joined journey) | None needed | **IV-S holds.** V residual under O-1 |
| P9 (DEP-02-02-017) | **Fails.** WR §7: "the ledger cites it by record identity". RB-4a writes RS's `relations.reviewedDraft` and `priorRevision`. The row receives "the record kind for the registration act (A15)" | Would hold: the act control's writer (DEL-01-04) maps to RS's form, and RS validates | **WR-v0.2 §4.3 RB-4a, §7 (DEL-04-03 row) and §8 ledger** — DEL-02-02's design agent. The ledger holds an opaque reference returned in the act control's capture report. The statement of RS's relation names leaves WR; RB-4a already says "the act control's writer maps it" | Design rewording, plus S1 on DEP-02-02-017's Statement ("record kind"). Act meaning stays on the admitted DEP-02-02-016 (§21.2) |
| P10 (DEP-02-03-026) | **Fails.** EXEC §2.5 evaluates reached-when on X with ADAPTER's semantics. EXEC §9.1: "using ADAPTER §4.1 NM-1/NM-2, §4.5 and OC-9" | — | None at design level without moving the evaluation. See §21.5 | **Not IV-S.** Owner-level act (§21.5) |
| P15 (DEP-03-01-031) | **Fails.** C §6.2 is rule-bearing on RS's lapse vocabulary, for example rule 4: "When the bound content changes, the act is shown lapsed (S-C8)". It also has a "Must not be strengthened by" column. It carries RS record references | Would hold: RS and the host check the carried values | **C-v0.8 §6.2** — DEL-03-01's design agent. Withdraw the lapse and act-evidence display rules (rule 4 and the column) to their owners: RS §7 states the rules, AS §8 displays them. Make the record references opaque. C's ScopeOfWork CLM-002 already says it "does not define" them, so no ScopeOfWork ownership moves (RVG C2-M1) | Design rewording, plus S1 (§12) |
| P17 (DEP-03-02-034) | **Fails.** P §3.3 "Standing at drafting" enumerates AS's seven display states. P §4.4's entry condition reads "effective (person-set) with grant value direct" | Would hold: the host route and the record check | **P-v0.8 §3.3 and §4.4** — DEL-03-02's design agent. Remove "Standing at drafting" and "Settings reference" from the change request. They are recorded App-side (RS §5 and settings-in, AS §12.1 "P records both references (P §3.3; RS §5)"), linked by the host request id P already keeps. Restate §4.4's entry as "the host route resolves the treatment *apply directly*" (ACT §5.2 vocabulary, admitted DEP-03-02-017). This revisits integrator rulings R-8 and R2-6, which placed the attribution in P. It also reverses the owner's Q-11 acceptance of the optional consumption sentence, so the owner sees it | Design rewording, plus S1. **Owner decision flagged** (Q-11) |
| P19 (DEP-05-01-025) | **Fails today.** LOOP §6.2's dispatch record: "Grant in force … for the operation's class its grant value, display state (O-6), scope and policy-class record reference" | Would hold: AS and the host route check, and AS §12.1 already says the loop "relays intent" | **LOOP-v0.9 §6.2, the "Grant in force" element** (and the RP-4 text it cites) — DEL-05-01's design agent. Shrink it to an opaque settings-version reference. LOOP's own allow rule uses only its own DF-3 and DF-6 data. A follow-on line in AS-v0.9 §12.1's DEL-05-01 row (DEL-04-02's design agent) says only the reference is carried | Design rewording, plus S1 |
| P4, identity part (DEP-03-02-027; RVG did not test it) | **Fails.** P §3.3 enumerates WD's tuple "{kind, origin, source root, name, revision}". `proposal.schema.json` limits `origin` to WD §6.1's values | Would hold: the record (RS) carries the tuple; RS already consumes it (DEP-04-03-034) | **P-v0.8 §3.3 "Workflow identity" and `proposal.schema.json`** — DEL-03-02's design agent. Carry an opaque workflow-run reference, which REQ-003's "workflow-run attribution" still satisfies. Resolve the tuple through the record, linked by the host request id, as P §3.3 already does for SWBPIPE. This revisits R-9's placement of the tuple in P | Design rewording, plus S1 on DEL-03-02 CLM-003. The governance-phase L residual remains (§21.4) |

**M1 result.**
- **Hold today:** P1 and P8 (IV-S).
- **Close by a named design rewording:** P4's identity part, P9, P15, P17 and P19.
- **Cannot close at design level:** P10 (§21.5).
- **Consequence if the rewordings are not made.** P4, P9, P15, P17 and P19 keep I rows, and P10 is unmoved. The repaired move set then leaves, under O-4, a 10-member component with 6 rows. See §21.8, scenario A0.

### 21.2 M2 — the re-targets without "Q-5"

**What Q-5 decided (GC-2).** The owner's Q-5 accepted "the App act control in DEL-01-04, with REQ-008 as adjusted and the drafted OUT-005, AC-008 and VER-008, as worded" (`APP-V4-SCA003-20261002/OWNER_DECISIONS.md` l.53). It does **not** decide that DEL-04-01 gains no supplier. §1, §16 and §20.7 were wrong to rely on it.

**What the re-targets add.** They add **no new arc**. Each consumer already consumes DEL-04-01 through an admitted row:
- DEP-02-01-018 for P5;
- DEP-02-02-016 for P9;
- DEP-03-02-017 for P17.

The P11 re-target is withdrawn (§21.3). I checked: all of these arcs are admitted, and DEL-04-01 has 20 admitted consumers.

**ACT §5.1's inputs** (ACT-POLICY-v0.11 §5.1 "Inputs (semantic)"):

| Input | ACT's text | Kind under G1 r2's K-3 ("E only where the consumer, or a third party, defines the format") |
|---|---|---|
| *grant state* from DEL-04-02 | "**effective (person-set)** · **effective (policy default)** · requested by agent (A8) · set by person, not yet confirmed · unconfirmed · not set · refused (reason)… \| DEL-04-02 (R-8; R2-6)". §5.3 is rule-bearing on these states | **I.** ACT names DEL-04-02 as the supplier, and the states are AS §3's. Restating them is not defining them. G1 r2's §2b reads A3 as E, because "ACT lists their value sets itself". I disagree for this input: a list attributed to its supplier is a restatement |
| *checkpoint state* from DEL-02-01, DEL-02-03 and DEL-05-01 | "Whether a declared checkpoint applies, the act it requires, and any governing checkpoint constraint \| DEL-02-01; DEL-02-03; DEL-05-01; P §3.3" | **Boundary, I by default.** The act codes are ACT's own. "Whether a declared checkpoint applies" uses WD's declaration and EXEC's or LOOP's arrival. It is E only if ACT §5.3 rule 2 reads nothing but an arrival named in ACT's own act vocabulary |
| *operation identity and class* from DEL-03-01 | "The catalog operation and its host-named class \| DEL-03-01" | **I.** It uses the catalog identity scheme |

**What the SCC becomes if these inputs are registered as I.** Computed over all admitted and held arcs, with the repaired move set of §21.8 scenario C:

| Inputs registered as I | O-4 | O-1 |
|---|---|---|
| None (today) | SCC-002 acyclic | 12 members, 6 rows |
| Grant state only (DEL-04-01 → DEL-04-02) | **12 members**, including DEL-04-01, DEL-01-02 and DEL-01-03. The minimum closing set is that one new row | 15 members, 7 rows |
| Checkpoint state only (three rows) | 11 members; the minimum closing set is the three new rows | 15 members, 9 rows |
| All five ACT §5.1 inputs | 12 members; the minimum closing set is the five new rows | 15 members, 11 rows |

**Plainly.**
1. Re-targets P5 and P9, and P17's citation of ACT §5.2, work only while ACT §5.1's inputs stay unregistered, or are classed E.
2. The same holds for the acyclicity of the whole admitted layer into DEL-04-01. Twenty deliverables consume it.
3. If those inputs are registered as I, they become the cycle-closing rows themselves, and each needs its own move. Inverting them would need ACT §5.3 to stop being rule-bearing on AS's states (GC-1 (a)). That is an ownership question: the alternatives are IV-O, decomposition of DEL-04-01, merge, or cut.
4. **Owner question.** Should DEL-04-01's semantic inputs (ACT §5.1) be registered, and on what basis? This is open (GC-2). G2 lists it as ambiguous item A3.

### 21.3 M3 — P11 as a plain invert (supersedes §10's move)

**Source.** EXEC-v0.7 §4.10, headed "A12 refused by the control … — ADOPTED (R4-6)", owns the A12 control relation and its arrival effects:
- "**established ⟨settings version⟩** … Counts …";
- "**pending** … **waiting**";
- "**refused ⟨reason⟩** … **waiting**; the refused A12 does not satisfy";
- "confirmation observation lost (*unconfirmed*) | **unknown** until observed".

SP-7 adds: "For A12: the control relation is **established** (§4.10)". ACT §2.5's table is headed "(R4-6; EXEC §4.10 AR-1…AR-4)", so ACT restates EXEC; it is not the source. §10 had the order backwards (RVG C2-M3).

**Move.** DEP-02-03-029 with its mirror DEP-04-02-023: **IV**.
- EXEC needs nothing from DEL-04-02 to record A12 checkpoints. Its own §4.10 and SP-6/SP-7 decide them.
- AS's display labels in §4.10 ("display *effective*, person-set"; "*set by person, not yet confirmed*") become citations, or are dropped. That is EXEC-v0.7 §4.10 and the §9.1 DEL-04-02 row, by DEL-02-03's design agent.
- AS-v0.9 §12.1's DEL-02-03 row is withdrawn, by DEL-04-02's design agent.

**ScopeOfWork.**
- **S1**, two sentences: DEL-02-03 CLM-002's consumption clause ("`DEL-04-02`'s grant display states …, for recording A12 checkpoints"), and DEL-04-02 CLM-002's receivers list.
- No ownership moves. DEL-02-03 CLM-002 keeps "`DEL-04-02` owns grant display states", which stays true.
- No reliance on DEL-04-01.

**Anchor.** EXEC-v0.7 §4.10, §4.5 SP-6, SP-7. Closure is unchanged.

### 21.4 M4 — P4 restated (supersedes §4's move and §20.7's P4 entry)

- **Identity part (DEP-03-02-027).** The rewording of P §3.3 (§21.1) makes GC-1 (a) hold. What remains on the arc DEL-03-02 → DEL-02-01 is the governance-phase constraint derivation, an L residual ("In Phase 1 the App carries none", P §3.3). The mirror DEP-02-01-033 needs S1 in DEL-02-01 CLM-002's receivers list.
- **Under O-3 and O-4:** the residual leaves with its kind, and P4 closes by the design rewording.
- **Under O-1 and O-2:** P4 needs **one owner act**. Any of these closes it:
  - **CUT** of the arc's governance-phase residual (doctrine §2 rule 3, SR-4; it covers mirror DEP-02-01-033). This is the smallest. Computed: with P10 also acted on, O-2 then leaves P13 only;
  - DEC of DEL-02-01, as in §4;
  - IV-O, moving WD §4.3.6–§4.3.7;
  - MRG.

  A re-target of the residual to ACT §4.4 ("Acceptance-checkpoint constraint (DERIVED …)") is conceivable but is subject to §21.2.
- **Without the P §3.3 rewording:** DEP-03-02-027 stays I, and P4 needs an owner act under **every** option. Computed: O-4 then leaves P4, 2 members, 1 row.
- **Correction of §18 and §20.7.** G1's decomposition flag is **not** "confirmed". P4 needs one owner act under O-1 or O-2, and the smallest is a cut. Decomposition is one alternative among four.

### 21.5 M5 — P10 is an owner-level act (supersedes §20.1's move)

**Evidence.**
- EXEC §2.5 is the App-run reached-when evaluation, placed in EXEC by binding resolution R12-4 (EXEC Changes l.113).
- On X it uses ADAPTER's native-path semantics (EXEC §9.1).
- ADAPTER's `checkpoint_observation.schema.json` says: "The adapter observes and reports; it evaluates no reached-when, disposition or hold."
- A citation that EXEC's own evaluation rules use is still a requirement of ADAPTER's definition (GC-1 (a)).

**Moves**, each needing an owner-level act:

| Move | Content | Note |
|---|---|---|
| IV-O at Design level | Move X-path reached-when evaluation from EXEC §2.5 to ADAPTER §7.7 | Reverses R12-4 and ADAPTER's stated boundary. It is consistent with DEL-02-03 CLM-002 ("`DEL-03-03` owns external-channel receiving"), so it is not a ScopeOfWork S2. It needs whoever holds R12-4's authority, and the owner if contested |
| DEC | Split EXEC's X-path evaluation into its own unit | Decomposition change through `scope-change` |
| CUT, MRG | — | Owner |

**Effect.** O-4 closure depends on P10. Without a P10 act, O-4 leaves 4 members and 1 row (DEP-02-03-026). The IV-S count falls to six: P1, P8, and P4's identity part, P9, P15 and P19 after rewording.

### 21.6 Minor findings

- **C2-m1 (P3 residual).** WD-v0.9 relies on EXEC beyond DEP-02-01-026. §4.3.4 has "**Run end and continuation (R4-4; EXEC §4.9; PROPOSED (W7))**", §6.4 is headed "confirmed by DEL-02-03 EXEC §6.2", and WD names EXEC on 56 lines (RVG).
  - Required rewording: re-anchor these to the integrator rulings that adopted them (R4-4, R-9, R2-20, …), by DEL-02-01's design agent.
  - Otherwise P3 keeps an I residual. Computed: O-4 then leaves 5 members and 1 row (DEP-02-01-026). The residual of CSV M-02 is corrected below.
- **C2-m2 (registry form).** P12, P18, P20 and M-X2 hold only in **registry form**:
  - RS §13.3 becomes a kind registry into which DEL-02-03, DEL-04-02, DEL-05-01 and DEL-03-03 register their kinds and body schemas;
  - each body is validated against the registering supplier's schema, which satisfies GC-1 (b);
  - RS's enumerated kinds stop listing supplier events.
  
  Rewordings:
  - RS-v0.10 §13.3 and `RS_RECORD.schema.json`, by DEL-04-03's design agent;
  - EXEC R14-1 and `checkpoint-record-entries.schema.json`, by DEL-02-03's;
  - AS §6 and `AS_SETTINGS_IN.schema.json`, by DEL-04-02's;
  - LOOP §5.3 DF-8, by DEL-05-01's.

  If RS's reader keeps body validation, each leaves a V residual on its arc. Computed: O-1 then rises from 6 to 9 rows (P12, P18, P20 back), and O-2…O-4 are unchanged.
- **C2-m3 (P9 format part).** Covered by §21.1's P9 rewording: the A15 record kind is RS format, and WR stops naming it.
- **C2-m4.** Already closed by §20.

### 21.7 Summary (supersedes the move and effect columns of §18 and §20.7 where they differ)

| Pair | Move after repair | Who | Conditions |
|---|---|---|---|
| P1 | IV-S DEP-02-02-013; V residual | Design (none needed) + S1 | — |
| P3 | IV DEP-02-01-026 | DEL-02-01 design agent (WD §4.3.4, §6.4 re-anchoring) + S1 | C2-m1 rewording |
| P4 | Rewording of P §3.3 identity, then the L residual. O-1/O-2: owner **CUT** (or DEC, IV-O, MRG) | DEL-03-02 design agent; owner under O-1/O-2 | Without the rewording, owner act under all options |
| P5 | RT DEP-02-01-019 to DEL-04-01 | Register owner (G1-m5) + S1 | ACT §5.1 unregistered or E (§21.2) |
| P6, P7, P21 | IV | S1 | — |
| P8 | IV-S DEP-02-02-015; V residual | Design (none needed) + S1 | — |
| P9 | RT (act meaning) + IV-S after WR rewording | DEL-02-02 design agent + S1 | ACT §5.1 (§21.2) |
| P10 | **IV-O (R12-4), DEC, CUT or MRG** | **Owner-level** | Required for O-4 closure |
| P11 | **IV** DEP-02-03-029 (EXEC §4.10) | DEL-02-03 and DEL-04-02 design agents + S1 | — |
| P12, P18, P20 (+ M-X2) | IV, registry form | DEL-04-03 design agent, with DEL-02-03, DEL-04-02, DEL-05-01 and DEL-03-03 + S1 | C2-m2; V residuals under O-1 if RS validates bodies |
| P15 | IV-S after C §6.2 rewording | DEL-03-01 design agent + S1 | — |
| P17 | IV-S after P §3.3/§4.4 rewording | DEL-03-02 design agent + S1; owner sees the Q-11 reversal | ACT §5.1 (§21.2) |
| P19 | IV-S after LOOP §6.2 rewording | DEL-05-01 design agent (+ AS §12.1 line) + S1 | — |

### 21.8 Closure, repaired move set (G1 r2 kinds)

**Model.** As §20.6.
- **Always applied:** the IV and RT moves of P3, P5, P6, P7, P11, P12, P18, P20, P21 and M-X2. P1 and P8 leave V residuals.
- **"Rewordings"** adds P9, P15, P17 and P19, and P4's identity part with its L residual.

| Scenario | O-1 | O-2 | O-3 | O-4 |
|---|---|---|---|---|
| A0: today, no rewordings, no owner acts | 12 members, 12 rows | 10 members, 7 rows | 10, 7 | **10 members, 6 rows**: P4, P9, P10, P15, P17, P19 |
| A: all design rewordings, no owner act | 12, 8: P1, P2, P4, P8, P10, P13, P14, P16 | P4 (2/1); P10 and P13 (4/2) | P10 and P13 (4/2) | **P10 only (4/1)** |
| B: A + owner act on P10 | 12, 7: P1, P2, P4, P8, P13, P14, P16 | P4; P13 | P13 | **acyclic** |
| C: B + owner cut of P4's residual | 12, 6: P1, P2, P8, P13, P14, P16 | P13 | P13 | **acyclic** |
| D: C, with P1 and P8's V residuals not entered | 12, 4: P2, P13, P14, P16 | P13 | P13 | acyclic |
| C, P3 not re-anchored (C2-m1) | 12, 7 (+P3) | P3 and P13 (6/2) | P3 and P13 | 5 members, 1 row (P3) |
| C, registry moves with V residuals (C2-m2) | 12, 9 (+P12, P18, P20) | P13 | P13 | acyclic |
| C, ACT §5.1 grant state registered as I | 15, 7 | — | — | 12 members, 1 row (the new row) |

### 21.9 Bottom line for SCC-002

Every move below also needs S1 ScopeOfWork wording, applied by `scope-of-work` under an amendment (SCA) the owner accepts. No S1 wording moves ScopeOfWork-assigned ownership.

**1. Pairs closed by design rewordings alone.** 15 of the 17 I–I pairs, every pair except P4 and P10. P4 also belongs here under O-3 and O-4:
- **No Design change needed:** P1, P8 (IV-S with a V residual), and P6, P7, P21 (IV).
- **After a named Design rewording:**
  - P3 (WD §4.3.4, §6.4 re-anchoring);
  - P11 (EXEC §4.10 citations; AS §12.1);
  - P12, P18, P20 (RS registry form);
  - P9 (WR RB-4a, §7, §8);
  - P15 (C §6.2);
  - P17 (P §3.3, §4.4; the owner sees the Q-11 reversal);
  - P19 (LOOP §6.2).
- **Re-target:** P5 (register-owner caveat G1-m5).
- **Condition.** P5, P9 and P17 hold only while ACT §5.1's inputs stay unregistered or are classed E, and so does the acyclicity of the admitted layer generally (§21.2).

**2. Needing an owner act.**
- **P10, under every option:** IV-O reversing R12-4 (Design-level), DEC of EXEC's X-path evaluation, CUT or MRG.
- **P4, under O-1 and O-2:** CUT of the governance-phase residual, or DEC, IV-O or MRG. Under O-3 and O-4 it is in group 1, given the P §3.3 rewording.
- **The ACT §5.1 registration question.** If the inputs are registered as I, their five rows become cycle-closing and need their own owner-level move.
- **Non-I–I rows:**
  - P13 (DEP-02-03-022, E/L) under O-1…O-3: owner cut, or confirmation by its register owner;
  - P2, P14 and P16 under O-1: V and V/L cuts;
  - the V residuals of P1 and P8 under O-1.

**3. What remains under each option**, after the group-1 rewordings and the owner acts on P10 and P4 (scenario C):
- **O-4:** acyclic. P4 needs no act here, given its rewording. P10 needs one.
- **O-3:** P13 only (1 row).
- **O-2:** P13 only, with the P4 cut. Without it, P4 and P13.
- **O-1:** 6 rows: P1 and P8 (V residuals), P2, P13, P14 and P16. Owner cuts or decomposition decide them.

**No evidence of a broad decomposition.** At most one decomposition is needed: for P10, and only if the owner prefers it to the alternatives. The structural premise now rests on two owner acts (P10, and P4 under O-1/O-2), one owner question (ACT §5.1), and about a dozen reviewed Design rewordings across 11 Design files.

### 21.10 Not established (repair)

| Item | Why |
|---|---|
| Whether the integrator rulings R-8, R2-6, R-9, R12-4 and R14-1 allow the rewordings | Read as cited only. Revisiting them is for their authority |
| Whether ACT §5.3 rule 2 reads anything beyond ACT's own act vocabulary | It decides whether checkpoint state is I or E (§21.2) |
| Whether REQ-003's "carry … workflow-run attribution" is met by an opaque run reference | My reading is that it is. The P §3.3 rewording depends on it |
| Design passages beyond those quoted for each rewording | Each rewording is a design-agent task, with its own review |

## 22. 2026-10-04 narrow repair (RVG-C2 Addendum A; GC-3, GC-4)

**Standing.** This section makes the narrow text repair asked for by RVG-C2 Addendum A (`reviews/RVG-C2.md`, sha256 `07fdc9ddba00e86cbff92d32283f1af0cfbe084c11c71557850ffe0839e213ea`, commit `56566863e9`). It applies HELP_HUMAN's rulings GC-3 and GC-4 (`GC_RULINGS.md`, sha256 `27265cc9245fd7c2d93096dd8f2978376b51c48daf0e77fc110ced4c7c3318dc`).

It is append-only and supersedes:
- §21.1's rows for P4 (identity part), P9, P15, P17 and P19;
- §21.5 (P10);
- the §21.2 table, which gains one row;
- §21.7–§21.9, where they differ.

The analysis method is unchanged. The one new computation is the operation-identity row in §22.5.

### 22.1 GC-3 applied to each identifier the rewordings carry

**The test (GC-3 item 1).** A carried identifier counts as an opaque reference when all three hold:
- it is typed as an uninterpreted string, with no pattern, format, enumeration or structure taken from the supplier;
- the consumer neither constructs, parses nor validates it against the supplier's scheme, though comparing the whole string for equality is allowed;
- the consumer's Design names who resolves it: the supplier or a third party.

Each rewording below must say this in its own text (GC-3 item 2).

| Pair | Identifier carried | Typed as | Not parsed? | Resolver named in the rewording | Structure needed? | Result |
|---|---|---|---|---|---|---|
| **P4** identity part (P-v0.8 §3.3, §8 "Origin" row, `proposal.schema.json`) | A workflow-run reference, in place of WD's tuple {kind, origin, source root, name, revision} | An uninterpreted string. `proposal.schema.json` drops the `origin` enumeration limited to WD §6.1's values (V18-2 m-9) | P keeps no rule that reads kind, origin or revision. The §3.3 sentences on adapted identity ("An unadapted carried workflow keeps its original origin; …") are WD's rules and are withdrawn from P | The App-side record, DEL-04-03's reader, resolves the run to its workflow tuple, linked by the host request id, as P §3.3 already does for SWBPIPE ("the App records both App-side and links them by the host's request id"). The run identity is issued by DEL-02-03's run starter. Both are third parties to P4's pair | **None in the current phase.** REQ-003 and V4-HI-21 require the "workflow run it came from", not the tuple's parts. P §8's "Origin" row must show the run reference, not a workflow name or revision. The governance-phase constraint derivation still uses WD's checkpoint declaration; that is the L residual (§21.4) | **Passes GC-3**, given the P §8 change and the R-9 amendment (§22.2) |
| **P9** (WR-v0.2 §4.3 RB-4a, §7 DEL-04-03 row, §8 ledger) | The A15 record identity returned in DEL-01-04's capture report | An uninterpreted string | WR only compares the whole string: "never emits a *registered* transition without a matching ledger line" | DEL-04-03's reader. The act control's writer (DEL-01-04) maps WR's descriptor to RS's form, which RB-4a already assigns ("the act control's writer maps it") | **None.** WR's own checks run on its own descriptor (ID-2), not on the record | **Passes GC-3** |
| **P15** (C-v0.8 §6.2; `read_result.schema.json` `$defs/act_evidence_ref`) | `act_record_reference`, an RS act-record identity | An uninterpreted string. Today it uses C's `#/$defs/identity`, which is already `{"type": "string", "minLength": 1}`. The rewording states that it is uninterpreted and resolved by DEL-04-03 | C keeps no act or lapse rule. Withdraw rule 4 and the "Must not be strengthened by" column for act evidence (§21.1). **Remove `act_evidence_ref.lapse_state`** from `read_result.schema.json` (a required property today), and remove its row in §6.2 ("Lapse state \| DEL-04-03 §7 vocabulary …") | DEL-04-03's reader, or the host where host-presented (RS L-9) | **None.** `act_kind`'s enumeration is DEL-04-01's A-codes, through the admitted DEP-03-01-024, and stays. That is not the pair's supplier | **Passes GC-3** |
| **P19** (LOOP-v0.9 §6.2 "Grant in force"; l.2045–2050 O-5; l.210 RP-4) | AS's settings-version identity in force at route decision | An uninterpreted string | LOOP no longer records AS state values. The rewording removes "grant value, display state (O-6), scope and policy-class record reference", and "grant in force: unconfirmed", which is AS's state. LOOP keeps "grant in force: not received", which is its own observation that no reference arrived. O-5's "recorded when they differ" becomes: carried; compared by the record or the display owner (R-3.6 "Record both" is met by RS) | DEL-04-02 (AS §12.1) and the host route, which "resolves treatment" (ACT §5.3) | **None.** LOOP's allow rule uses only its own DF-3 and DF-6 data, and the host-reported treatment uses ACT §5.2's vocabulary (admitted DEP-05-01-018) | **Passes GC-3**, given those three textual removals |

**No rewording needs part of the identifier's structure.** So no row stays I under GC-3 item 3. Two passes are conditional:
- P4 depends on the P §8 "Origin" row change;
- P19 depends on LOOP dropping "unconfirmed" and O-5's comparison.

If either change is refused, that row stays I.

### 22.2 Integrator rulings (GC-4)

Amending these rulings is **HELP_HUMAN's act** at application time after checkpoint 1. Each amendment is listed in the owner-facing checkpoint. None is an owner decision.

| Ruling | Amended text | Needed by |
|---|---|---|
| **R-9** | "workflow identity is carried everywhere as {kind, origin, source root, name, revision}" | P4's identity rewording (P §3.3, §8, `proposal.schema.json`) |
| **R14-1** | "Every CE kind gets an RS entry kind" and "RS states the mapping" | The registry form of P12, P18, P20 and M-X2 (§21.6) |

**Corrections to §21.**
- §21.1 and §21.7 said P17 "revisits integrator rulings R-8 and R2-6", and the CSV said "revisits R-8, R2-6". That is **withdrawn**. GC-4 item 3 holds that R-8, R2-6 and R-3 point 6 already allow P17's rewording: they require the references to be recorded, and RS records them. The owner still sees the Q-11 reversal.
- §21.10's "Whether the integrator rulings … allow the rewordings" is closed by GC-4.

### 22.3 P10 rewritten (supersedes §21.5 and CSV M-14-R; RVG B-M3)

**Source.**
- R12-4: "ADAPTER maps each path's observed items to record elements."
- EXEC §2.5.1's per-path rows restate ADAPTER's mappings: AW-1 uses NM-1, AW-2 uses OM-1, AW-4 uses NM-2, AW-8 uses §4.5, AW-9 uses OC-9, and AW-10 uses §7.7.
- The reached-when *evaluation*, whether an observed event matches WD §4.3.1's kind, is EXEC's own.

**Move: IV by design rewording. No responsibility moves.**
- **EXEC.**
  - EXEC-v0.7 §2.5.1 (AW-1, AW-2, AW-4, AW-8…AW-10) and the §9.1 DEL-03-03 row consume ADAPTER-mapped observations in an input form EXEC defines: *operation call started*, *outcome observed* and *not evaluable*, each carrying ADAPTER's limit label as an uninterpreted string (GC-3) defined by ADAPTER.
  - EXEC's rows cite no NM, OM or OC semantics.
  - EXEC keeps the evaluation.
  - Design agent: **DEL-02-03**.
- **ADAPTER.**
  - ADAPTER-v0.7 §4.1, §4.5, §4.6 and §7.7 emit those inputs, mapping each native path per R12-4.
  - `checkpoint_observation.schema.json`'s `exec_event` already names the EXEC input each observation feeds.
  - ADAPTER's statement "evaluates no reached-when" still holds.
  - Design agent: **DEL-03-03**.

**Tests.**
- GC-1 (a) holds for EXEC once the citations are gone.
- GC-1 (b): ADAPTER checks its own mapping.

**ScopeOfWork.** S1 in DEL-02-03 CLM-002's "consumes, and does not define" clause. There is no mirror. No ownership moves. DEL-02-03 CLM-002 says "`DEL-03-03` owns external-channel receiving", and R12-4 already allows the move (GC-4 item 3).

**Fallbacks**, only if the rewording is refused: IV-O, DEC, CUT or MRG, as in §21.5.

**Correction.** §21.5's "P10 is an owner-level act" was built on RVG C2-M5, which RVG has withdrawn (B-M3). **P10 joins group 1.**

### 22.4 P15's schema field (RVG B-m1)

P15's rewording removes `act_evidence_ref.lapse_state` from DEL-03-01's `read_result.schema.json`:
- it is a required property today;
- it is a string carrying an RS §7 state value.

The same rewording drops `lapse_state` from that `$def`'s `required` list. It also states that `act_record_reference` is an uninterpreted string resolved by DEL-04-03. This is all DEL-03-01's design agent's work (§22.1).

### 22.5 ACT §5.1: the operation-identity row (adds to §21.2's table)

The same computation as §21.2: all admitted and held arcs, with §21.8 scenario C's moves.

| Inputs registered as I | O-4 | O-3 | O-2 | O-1 |
|---|---|---|---|---|
| **Operation identity only** (DEL-04-01 → DEL-03-01) | **2-cycle {DEL-03-01, DEL-04-01}, 1 row**, closed with the admitted DEP-03-01-024 | same 2-cycle | same 2-cycle | inside a 15-member component, 7 rows; the 2-cycle is part of it |
| Grant state only | 12 members, 1 row | — | — | 15 members, 7 rows |
| Checkpoint state only | 11 members, 3 rows | — | — | 15 members, 9 rows |
| All five | 12 members, 5 rows | — | — | 15 members, 11 rows |

Even the least contested ACT §5.1 input forms a cycle, under every option. M-Q-ACT's owner question stands. RVG B-n1 agrees that checkpoint state reads I; it is a boundary call.

### 22.6 Bottom line for SCC-002 (supersedes §21.9)

**Group 1 — closed by design rewordings.** Each also needs S1 ScopeOfWork wording through an SCA the owner accepts, plus HELP_HUMAN's amendments of R-9 and R14-1 (GC-4). Each relies on GC-3 for its identifiers.
- **All 17 I–I pairs under O-3 and O-4:**
  - P1, P6, P7, P8, P21: no Design change needed beyond S1;
  - P3: WD §4.3.4, §6.4;
  - P4: P §3.3, §8, schema; R-9;
  - P5: re-target; G1-m5;
  - P9: WR;
  - **P10: EXEC §2.5.1 and ADAPTER §4.1, §4.5, §4.6, §7.7**;
  - P11: EXEC §4.10;
  - P12, P18, P20: RS registry; R14-1;
  - P15: C §6.2 and `read_result.schema.json`;
  - P17: P §3.3, §4.4; the owner sees the Q-11 reversal;
  - P19: LOOP §6.2.
- **16 pairs under O-1 and O-2.** P4's governance-phase residual stays there (§21.4).
- **Condition.** P5, P9 and P17, and the admitted layer into DEL-04-01 generally, hold only while ACT §5.1's inputs stay unregistered or are classed E (§21.2, §22.5).

**Group 2 — owner acts.**
- **P4 under O-1 and O-2:** a cut of the governance-phase residual (smallest), or DEC, IV-O or MRG.
- **The non-I–I rows:**
  - P13 (DEP-02-03-022, E/L) under O-1…O-3: a cut, or confirmation by its register owner;
  - P2, P14 and P16 under O-1: V and V/L cuts;
  - the V residuals of P1 and P8 under O-1.
- **M-Q-ACT:** whether ACT §5.1's inputs are registered. If they are registered as I, they become cycle-closing rows; even operation identity alone forms a cycle (§22.5).

**Group 3 — what remains per option** (G1 r2 kinds, closure as computed in §21.8; RVG A.1 reproduces it):

| Option | Group 1 only (scenario B; no owner act on any I–I pair) | Group 1 + P4 cut (scenario C) | C, without P1 and P8's V residuals (D) |
|---|---|---|---|
| O-4 | **acyclic** | acyclic | acyclic |
| O-3 | P13: {DEL-02-03, DEL-05-01}, 1 row | P13 | P13 |
| O-2 | P4 and P13: two 2-member components, 1 row each | P13 | P13 |
| O-1 | 12 members, 7 rows: P1, P2, P4, P8, P13, P14, P16 | 12, 6: P1, P2, P8, P13, P14, P16 | 12, 4: P2, P13, P14, P16 |

**Sensitivities, from §21.8:**
- P3 not re-anchored: O-4 leaves 5 members and 1 row.
- Registry moves with V residuals: O-1 rises to 9 rows.
- Any ACT §5.1 input registered as I: §22.5.

**No decomposition is required anywhere.** The fallbacks for P10 and P4 include one, but neither needs it.

### 22.7 Not established (narrow repair)

| Item | Why |
|---|---|
| Whether the host's proposal views must show a workflow name or revision (P §8) | REQ-009 does not require it, and V4-HI-21 requires only the run. If an accepted text requires it, P4's identity row stays I (GC-3 item 3) |
| The exact EXEC input forms in §22.3 | Named from RVG B-M3 and EXEC §2.5.1's row references. The wording is the design agents' |

## 23. 2026-10-04 E residuals (RVG-C2 Addendum B, B2-M1)

**Standing.** This section responds to RVG-C2 Addendum B (`reviews/RVG-C2.md`, sha256 `0736ec4cf9bf47d3a3a82eb40230b566403e8d98f85b77dae702cbc7377e6629`, commit `0c815a8cdf`). It is append-only and supersedes:
- the O-1…O-3 columns of §22.6's per-option table;
- the "Residual" cells of the CSV rows named below.

§22.6's O-4 column and its group-1 and group-2 structure stand, as RVG confirms.

### 23.1 Which moves leave a runtime flow (E residual)

An invert removes the consumer's definitional need. It does not remove runtime instances the consumer still receives. Under K-3 those stay rows of kind E, just as §21 records V residuals for P1 and P8.

**Moves that leave an E residual on their arc:**

| Pair (row) | Runtime flow that remains | Does a source support an S1 wording that removes the receipt? | Residual |
|---|---|---|---|
| P10 (DEP-02-03-026) | EXEC records ADAPTER's observations, now in EXEC's own input form | **No.** DEL-02-03 CLM-002 assigns the recording to EXEC: "`DEL-03-03`'s observations … which this slice records". Making the adapter write the record would move recording ownership (S2) | **E** |
| P12 (DEP-04-03-025) | RS's writer and reader take EXEC's checkpoint entries | **No.** DEL-04-03 CLM-004: "The App/shared evidence-record owner owns this format, App reader/writer". EXEC R14-1: EXEC's root "validates one recorder output {RS kind, observed time, body}", which RS writes. Supplier-written entries would move the writer (S2) | **E** |
| P18 (DEP-04-03-022) | RS's writer receives settings-in. AS §12.1, DEL-04-03 row: "Written as a `settings_version` entry in order with the operation entries (RS §13, §14.1)" | **No**, for the same CLM-004 reason | **E** |
| P20 (DEP-04-03-028) | RS's writer receives LOOP's destination events as R15 entries | **No**, for the same reason | **E** |
| M-X2 (DEP-04-03-026) | RS's writer receives ADAPTER's external dispatch entries | **No**, for the same reason | **E** |
| P19 (DEP-05-01-025) | LOOP's dispatch record receives AS's settings-version identity on each dispatch | **Partly.** The host route resolves treatment from the host's own control (ACT §5.3; AS §3: "the control (App or host) is the authority for the current grant"). R-3.6's "Record both" is met by RS's ordered `settings_version` entries. But AS §12.1 defines "**Grant in force per dispatch** (defined here)" for this receiver, and DEL-05-01 CLM-002 states the consumption. Removing the carriage would need AS §12.1's DEL-05-01 row withdrawn as well as S1 in DEL-05-01 CLM-002. I do not claim the sources settle it | **E** by default. The alternative is named, not adopted |

**Moves that leave no runtime flow on their arc:**
- P3, P6, P7, P21: the consumer receives only definitions or requirements.
- P11: EXEC reads A12 control relations from the record, not from AS.
- P5, P9, P15, P17: the act meaning comes through admitted DEP-…→DEL-04-01 rows. Record identities arrive through DEL-01-04's capture report (P9) or the host (P15), not from DEL-04-03.
- P4 identity part: the workflow-run reference reaches the dispatching channel (LOOP or ADAPTER) from DEL-02-03's run starter. That flow is on the existing arcs DEL-05-01 → DEL-02-03 and DEL-03-03 → DEL-02-03, not on DEL-03-02 → DEL-02-01. DEL-03-02, as a contract, receives no instance.

### 23.2 Per-option table (supersedes §22.6 group 3's O-1…O-3 columns)

My recomputation reproduces RVG's Addendum B figures exactly. G1 r2/r3 kinds, held arcs. "Rows" is the exact minimum. Group 1 is the §22 move set, now with the five E residuals; the "+P19" lines add the sixth.

| Scenario | O-1 | O-2 | O-3 | O-4 |
|---|---|---|---|---|
| Group 1 only (B), E residuals ×5 | 12 members, 11 rows | 5 / 5 (P10, P12, P13, P18, P20) + 2 / 1 (P4) | 5 / 5 | **acyclic** |
| B, E residuals ×5 + P19 | 12 / 12 | 5 / 6 + 2 / 1 | 5 / 6 | acyclic |
| Group 1 + P4 cut (C), E residuals ×5 | 12 / 10 | 5 / 5 | 5 / 5 | **acyclic** |
| C, E residuals ×5 + P19 | 12 / 11 | 5 / 6 | 5 / 6 | acyclic |
| D (C, without P1 and P8's V residuals), E residuals ×5 | 12 / 8 | 5 / 5 | 5 / 5 | acyclic |
| D, E residuals ×5 + P19 | 12 / 9 | 5 / 6 | 5 / 6 | acyclic |

**Reading.**

1. **O-4 is unchanged.** It is acyclic with no owner act on any I–I pair. Every residual is E or V, and O-4 keeps only P and I.

2. **Under O-3 and O-2, the 5-member component is {DEL-02-03, DEL-03-03, DEL-04-02, DEL-04-03, DEL-05-01}.**
   - Its exact minimum is 5 rows, or 6 with P19. Some rows in that minimum are I-side rows (DEP-02-03-013, DEP-04-02-008, DEP-05-01-019), so it is not a set of cut candidates.
   - **If owner cuts are restricted to E rows**, it closes with 6 cuts: the E residuals of P10, P12, P18 and P20, the M-X2 residual, and P13's DEP-02-03-022. With P19's residual, 7 cuts are needed.
   - Computed: cutting the P10, P12, P18 and P20 residuals plus P13 still leaves 1 row, M-X2's DEP-04-03-026. Adding P19's residual raises that remainder to 2.

3. **O-1** adds to the O-3 set:
   - the V residuals of P1 and P8;
   - the V and V/L rows of P2, P14 and P16;
   - P4's L residual, unless it is cut (scenario B against C).

**Group 3 restated.**

| Option | What remains after group 1 and the P4 cut | Owner acts that close it |
|---|---|---|
| O-4 | nothing | none |
| O-3 | one 5-member component | per-edge cuts of 6 E rows (7 with P19's residual) |
| O-2 | as O-3 | as O-3; plus the P4 cut, if not already made |
| O-1 | 12 members, 10 rows (11 with P19) | as O-2; plus V cuts of P1, P2, P8, P14 and P16 |

**Consequence (RVG B.4).** After the moves, the owner's class choice weighs more than G1 r3's pre-move figures suggest:
- O-4 leaves nothing to cut;
- O-3 still needs about six per-edge cuts on E rows.

### 23.3 SCC-001 has no E residual

SCC-CASE-001's IV of DEP-01-01-024 (that case's §1.6) leaves no runtime flow to DEL-01-01. The sign-in and substitution evidence stays with DEL-01-05 (DEL-01-05 REQ-007; ACCESS §12). Its closure table stands.

## 24. 2026-10-04 correction of §23.3 (RVG2-CASE-001 C1-M1)

§23.3's claim that SCC-001's move leaves no runtime flow is **withdrawn**, and so is "Its closure table stands". This section supersedes §23.3.

**The flow.** HOSTING-BOUNDARY-v0.9 §8.3 still receives two runtime values from DEL-01-05: the requested provider and model (ACCESS §1 I-3), and the destination class (I-4). HOSTING's VC-26, which serves VER-005, takes the class from DEL-01-05's configuration. So the arc DEL-01-01 → DEL-01-05 keeps an E residual, with V.

**Consequence for SCC-001** (SCC-CASE-001 §6.1). SCC-001 is acyclic under O-4. Under O-1…O-3 it stays a 2-cycle until the owner makes a per-edge cut of that arc.

**Consequence for this case.**
- SCC-002's own figures in §22 and §23 are unaffected, because SCC-001 is a separate component.
- If N08 is registered as I, it merges the two. Under O-2 it gives 13 members and 8 rows; under O-3, 12 members and 7 rows (SCC-CASE-001 §6.2).
