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
