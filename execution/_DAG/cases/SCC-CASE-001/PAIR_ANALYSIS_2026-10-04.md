# SCC-CASE-001 — pair analysis of SCC-001, DEL-01-01 ↔ DEL-01-05 (2026-10-04)

- **Standing.** Case evidence under `workflows/scc-resolution-case`. It is evidence for the owner's checkpoint, not a ruling.
  - No row, register, ScopeOfWork, Design file, DAG version or existing case file is changed.
  - Every move is a **proposal**. Cut and merge are the owner's (`docs/CYCLE_DRIVEN_RESOLUTION.md` §2 rule 3).
  - Any ScopeOfWork revision is applied by `scope-of-work` under an amendment (SCA) the owner accepts.
  - CaseState stays EVIDENCE_ACCUMULATING, and the CP1-20260928 ruling carries forward unchanged.
- **Run.** `APP-V4-GRAPH-CLOSURE-20261004`, case work under `CASE_BRIEF_COMMON.md`. Author: a Type 2 TASK agent (Claude Opus 5.5) dispatched by HELP_HUMAN. It does not delegate.
- **Method.** As SCC-CASE-002's `PAIR_ANALYSIS_2026-10-04.md` (§1–§22), with GC-1…GC-4.
- **Paths.** `E/` is `projects/chirality-app-v4/execution/`. The pair label P1 is local to this case.

## 0. Basis and checks

| File | sha256 |
|---|---|
| `E/_Coordination/AgentRuns/APP-V4-GRAPH-CLOSURE-20261004/CASE_BRIEF_COMMON.md` | `c83e0f86ca55c26ddc6abd2cfa817256fd6ed42f6013a926b72016825c703468` |
| `E/_Coordination/AgentRuns/APP-V4-GRAPH-CLOSURE-20261004/SURVEY/G1.md` (r3) | `3d6543bc2a05e5e62cb9673c1d3177386f484de38d9058a0b396eee9299f0a45` |
| `E/_Coordination/AgentRuns/APP-V4-GRAPH-CLOSURE-20261004/GC_RULINGS.md` | `27265cc9245fd7c2d93096dd8f2978376b51c48daf0e77fc110ced4c7c3318dc` |
| `E/_DAG/DAG-004/CandidateEdges.csv` | `2bfff10e3094d7fd86da563006c965694563ec10d0fc78e9b1d9958fefa42025` |
| `E/_DAG/DAG-004/ExcludedRows.csv` | `45f55e76ecf7c9aac3bd923838eee8c302d6b2776e4fa3c221e51f9cf465664e` |
| `E/_DAG/cases/SCC-CASE-001/Candidate_Remedies.csv` (read; not changed) | `8d3bd50648695bfe629a88b3bbd7de536b90ca32b500de259c7b7d5125f4286b` |
| `E/_DAG/cases/SCC-CASE-001/Case_Datasheet.md` (read; not changed) | `301067dacf2e2d83edd1dca86638a271ee0b773b110cfa3420d58e963eb371c4` |

**Designs read, by section.** Both are "DRAFT DEFINITION", not accepted.
- DEL-01-01: `HOSTING_BOUNDARY.md` (HOSTING-BOUNDARY-v0.9), §8 (receivers and suppliers table, §8.1), §11 and the verification cases.
- DEL-01-05: `ACCOUNT_AND_PROVIDER_ACCESS.md` (ACCESS-v0.2), §1, §12, §13 and §19.

**Checks run.** The scripts are scratch files under `$TMPDIR`.

| Check | Result |
|---|---|
| Held rows | DAG-004 holds exactly two rows for SCC-001: DEP-01-01-024 and DEP-01-05-012. Their arcs form one reciprocal pair |
| Mirror rows (`ExcludedRows.csv` `RepresentedBy`) | Arc DEL-01-05 → DEL-01-01 also carries DEP-01-01-022 (DOWNSTREAM HANDOVER) and DEP-01-05-013 (UPSTREAM PREREQUISITE). Arc DEL-01-01 → DEL-01-05 carries only DEP-01-01-024 |
| Live fidelity | All four rows were read from the live registers. Statements and quotes are given below as they stand |
| Kinds | G1 r3 (§2.1; Appendix A for the admitted layer), applied graph-wide as r3 states. Held: I 71, V 5, P 3, L 3, E 1. Admitted: I 85, P 40, L 2, E 2 |
| Baseline (no moves) | O-1: {DEL-01-01, DEL-01-05}, 1 row. O-2, O-3 and O-4: no component, because the V row leaves. This reproduces G1 r3 |

## 1. P1 — DEL-01-01 ↔ DEL-01-05

### 1.1 Rows

| Row | From → To | Direction / type | EvidenceQuote | Statement | Mirror / same arc |
|---|---|---|---|---|---|
| DEP-01-01-024 | 01-01 → 01-05 | UPSTREAM INTERFACE, INITIALIZED / TBD | "native sign-in and server-substitution evidence is received from its own owner when needed." | "Receive native sign-in and server-substitution evidence from the App v4 DEL-01-05 account/provider owner when needed for the local qualification witness; the source does not impose an unconditional prerequisite." | — |
| DEP-01-05-012 | 01-05 → 01-01 | UPSTREAM PREREQUISITE, INITIALIZED / PENDING | "DEL-01-05 consumes that identified protocol/pin" | "DEL-01-05 consumes the identified selected Codex protocol/pin supplied by DEL-01-01 before its mode/provider implementation and qualification depend on that input." | DEP-01-01-022, DEP-01-05-013 |

### 1.2 ScopeOfWork

**DEL-01-01** (`E/PKG-01…/DEL-01-01_…/ScopeOfWork.md`):
- **VER-005:** "Compare the chosen Codex embedding behavior against its identified published protocol using recorded exchange fixtures and the applicable candidate witness; inspect local-provider requirements handed to the App account/provider owner against the selected protocol. Record unsupported/unobserved portions explicitly; native sign-in and server-substitution evidence is received from its own owner when needed. Verifies AC-005."
- **AC-005**, which VER-005 verifies: "… qualification does not assert that account flows or server substitution are completed here."
- **CLM-004:** "`DEL-01-05` (App account/provider integration owner) owns native sign-in, API-key and local-provider access and configured-server substitution checks".

**DEL-01-05:**
- **CLM-003:** "`DEL-01-01`, the App supplier-integration owner's contribution, owns stock App Server hosting, process/protocol ownership, supplier-pin definition, generated protocol types and selected embedding qualification. DEL-01-05 consumes that identified protocol/pin and contributes the account/provider and local-server portion of joint SOW-149 qualification."
- **TBD-003:** "The App implementation owner selects the qualification pin through the DEL-01-01 contribution before qualification. DEL-01-05 then establishes its mode/provider behavior against that input."
- **REQ-007:** "a compliant local server shall be substitutable through supported provider settings … The required embedding-qualification input is the contribution named by CLM-003."

### 1.3 Design

**DEL-01-01, HOSTING-BOUNDARY-v0.9:**
- §8's table row for DEL-01-05 reads: "DEP-01-05-012 (held), DEP-01-05-013; this register's DEP-01-01-022, and DEP-01-01-024 (UPSTREAM, held) | The selected protocol and pin; embedding-qualification input | S-4; §8.1".
- §8.1 is the "Local-provider requirement account (REQ-005, AC-005; to DEL-01-05)".
- §11 "Owner / act boundary" assigns "Sign-in (including OAuth), API key, local provider …, substitution checks" to "DEL-01-05 (ACCESS-v0.2; ACCOUNT-HOME-RECORD-v0.2)", with "Flows, configuration, substitution evidence".
- VC-12 (VER-005) expects "no substitution claimed".
- No HOSTING section or verification case uses sign-in or substitution evidence from DEL-01-05.

**DEL-01-05, ACCESS-v0.2:**
- §1 I-10: "Selected pin and embedding qualification input; sign-in and substitution evidence 'when needed' | DEL-01-01 ↔ DEL-01-05 (DEP-01-05-012/013; DEP-01-01-022/024; held, SCC-001) | Held arcs gate nothing".
- §12 "Qualification and substitution (REQ-007, OUT-004) — designed only": "No candidate exists, so nothing is qualified. … record pin and distribution identity (HOSTING §7.1) …".
- §13: "DEP-01-01-024 (held, SCC-001; no counterpart here) | DEL-01-01 consumes | Sign-in and substitution evidence 'when needed' | §12 (designed); return file proposes a mirror row".
- §19 (S-4 not supplied): "Server-substitution checks | §12, VC-A08".

### 1.4 Kind (confirmed independently)

**DEP-01-01-024 is V/L.**
- The quote and SourceRef sit in VER-005, so the point of need is DEL-01-01's verification. "When needed" places it behind a condition.
- Boundary check (RVG G1-m2): K-5 should not apply where the point of need is the consumer's own OUT. Here the verification is of AC-005, and AC-005 excludes the content: "qualification does not assert that account flows or server substitution are completed here". The evidence is therefore not an input to DEL-01-01's OUT-004 claim. V stands.

**DEP-01-05-012 is P.**
- Its content is a selected value, the pin and protocol (K-4).
- It is needed "before its mode/provider implementation and qualification".
- Read as I under K-2, it would still sequence under every option, so nothing turns on P against I.

**The pair is not I–I.**

### 1.5 Order of the parts

- DEL-01-01's contribution to DEL-01-05 is the pin, the protocol, the §8.1 account and the embedding qualification. None of it depends on sign-in or substitution evidence: AC-005 excludes it, and VC-12 claims no substitution.
- DEL-01-05's contribution to DEL-01-01, the sign-in and substitution evidence, does depend on DEL-01-01's pin (ACCESS §12; TBD-003).
- Part order: DEL-01-01 pin/protocol → DEL-01-05 implementation and qualification (§12) → DEL-01-01's VER-005 witness, "when needed".
- **Projection artefact.** There is no part-level contradiction.

### 1.6 Move

**The smallest move, by the brief's order of preference:**

1. **(i) Design rewording.** Not applicable. No DEL-01-01 Design text consumes the evidence (§1.3). The row rests only on the VER-005 sentence.
2. **(ii) Invert with no ownership move: proposed.**
   - Withdraw DEP-01-01-024 as an input to DEL-01-01's VER-005.
   - The sign-in and substitution evidence is DEL-01-05's own qualification output (REQ-007; ACCESS §12, VC-A08). DEL-01-05 already links "the DEL-01-01 embedding-qualification input" (AC-007; DEP-01-05-013). So the exchange runs one way only, DEL-01-05 → DEL-01-01, which is the reverse arc that already exists.
   - **ScopeOfWork: S1**, one sentence, in DEL-01-01 VER-005. Its last clause ("native sign-in and server-substitution evidence is received from its own owner when needed") is withdrawn, or reworded as a pointer such as "is DEL-01-05's qualification evidence (its REQ-007), outside this verification".
     - AC-005 is unchanged; it already excludes the content.
     - No ownership moves: DEL-01-01 CLM-004 already assigns "configured-server substitution checks" to DEL-01-05.
     - There is no mirror row to cover.
   - **Design follow-on**, for DEL-01-05's design agent: ACCESS-v0.2 §13 withdraws its "return file proposes a mirror row" note, and §1 I-10 drops the "'when needed'" evidence clause.
   - **Integrator rulings amended (GC-4): none found.** The row's support is the ScopeOfWork sentence alone. No R-ruling places the evidence in DEL-01-01's witness.
3. **(iii) Owner act, as the alternative: CUT** of DEP-01-01-024 as a conditional verification return. This is CASE-001's existing R2. It is needed only if the S1 revision is declined, and only under O-1.

**DEP-01-05-012: no move.** It is a production input, and the order it states (pin before mode and provider) is the order the Designs follow.

## 2. Closure (G1 r3 kinds, graph-wide)

**Model.** All 212 arcs: the 83 held arcs plus 129 admitted. Option filters apply graph-wide, as G1 r3 defines them: O-1 keeps all kinds, O-2 drops V, O-3 drops V and L, O-4 keeps P and I only. Exact minimum feedback arc set by dynamic programming over subsets.

| Scenario | O-1 | O-2 | O-3 | O-4 |
|---|---|---|---|---|
| No moves | {01-01, 01-05}, 1 row (DEP-01-01-024 or DEP-01-05-012) | none | none | none |
| **IV of DEP-01-01-024 (S1)** | **acyclic** | acyclic | acyclic | acyclic |
| Owner cut of DEP-01-01-024 instead | acyclic | acyclic | acyclic | acyclic |

## 3. Interaction with G2's N08 (DEL-01-05 → DEL-04-03, `destinationClass`)

**What N08 is.** G1 r3 §2b classes N08 as I (K-2). ACCESS l.63 says "DEL-04-03/RS-v0.8 R5 and its schema enum `destinationClass` were read for the class values (§3)". It closes through DEP-01-04-021 (01-04 → 01-05) and DEP-05-01-026 (05-01 → 01-05). N08 is not a register row. Whether it becomes one is `dependency-extract`'s judgment.

**Computed.** N08 entered as an I row; all arcs; G1 r3 kinds. "Group 1" means the move set of SCC-CASE-002 §22 (design rewordings, including P10's).

| Scenario | O-1 | O-2 | O-3 | O-4 |
|---|---|---|---|---|
| N08, no moves | 19 members, 23 rows | 13, 18 | 13, 18 | 13, 17 |
| N08 + this case's move | 14, 21 | 13, 18 | 13, 18 | 13, 17 |
| N08 + SCC-002 group 1, without this case's move | 18 members, 9 rows (adds DEL-01-01, 01-02, 01-03, 01-06, 09-01; DEP-01-01-024 and DEP-09-01-021 in the minimum set) | none | none | none |
| N08 + SCC-002 group 1 + this case's move | 13 members (SCC-002's O-1 residual + DEL-01-05), 7 rows, the same 7 rows as SCC-002's O-1 residual | none | none | none |

**Reading.**
1. **N08's cycle does not run through this pair.** It runs DEL-01-05 → DEL-04-03 ⇝ {DEL-01-04, DEL-05-01} → DEL-01-05. Neither of this case's arcs is on it, so this case's move neither creates nor closes N08's cycle.
2. **N08's fate depends on SCC-002's moves.** Under O-2…O-4, SCC-002's group-1 moves cut every path from DEL-04-03 back to DEL-01-05, so N08 forms no cycle.
3. **Under O-1 the two interact by merging.** N08 joins DEL-01-05 to SCC-002's O-1 residual.
   - Without this case's move, DEL-01-01 is also pulled in (through DEP-01-01-024), with DEL-01-02, 01-03, 01-06 and 09-01: 18 members.
   - With this case's move, the component is SCC-002's residual plus DEL-01-05. It needs no row beyond SCC-002's own 7.
   - So under O-1, this case's move keeps DEL-01-01 and its neighbours out of any N08 merger.
4. **N08's own move.** G1 r3 proposes inverting N08: ACCESS l.910 states the value the other way, "DEL-01-05 is the class's source". That is outside this case. It belongs to whoever takes up G2's design-stated rows.

## 4. Summary

| Pair | Kinds confirmed | Contradiction or artefact | Proposed move | ScopeOfWork effect | Anchor | Integrator rulings (GC-4) |
|---|---|---|---|---|---|---|
| P1 01-01 ↔ 01-05 | DEP-01-01-024 V/L; DEP-01-05-012 P | Artefact | IV: withdraw DEP-01-01-024 (DEL-01-01 VER-005 last clause); alternative owner CUT (R2) | S1 ×1 (DEL-01-01 VER-005), no ownership move | DEL-01-05 REQ-007, AC-007; ACCESS-v0.2 §12; HOSTING-v0.9 §8, §8.1, §11, VC-12 | None |

**Owner acts per option.**
- **O-1:** none, if the S1 revision is accepted through an SCA. Otherwise one cut of DEP-01-01-024.
- **O-2, O-3, O-4:** none. The V row leaves with the option. The S1 revision is still recommended so that the register states no input DEL-01-01 does not need.

**Closure.**
- SCC-001 closes under every option with the IV.
- Under O-2…O-4 it closes even without a move.
- If N08 is registered as I, it interacts only under O-1, as described in §3.

## 5. Not established

| Item | Why |
|---|---|
| Whether DEL-01-01's register owner (`dependency-extract`) re-extracts no row once VER-005 is reworded as a pointer | The proposed wording names DEL-01-05's evidence as outside the verification. A plain withdrawal of the clause leaves no doubt |
| The admitted-layer kinds | Taken from G1 r3 Appendix A as given; not re-derived |
| The DAG-004 observation in `Case_Datasheet.md` | The datasheet shows no DAG-002…DAG-004 successor observation. The membership is unchanged by my check: two members, two held rows. A case evidence update is not part of this brief |

## 6. 2026-10-04 repair (RVG2-CASE-001; GC-5)

**Standing.** This section responds to RVG2's review (`reviews/RVG2-CASE-001.md`, sha256 `684b874bf00dd3eb7d82aefc16d808a96d9b2a572d2cafcc4b3edc75e63dfec9`, commit `0d338dd7b1`, verdict REPAIR). It applies ruling GC-5 (`GC_RULINGS.md`, sha256 `7fcbb551ea4605f77eb09d70ff3b57549d01f07e2b7992be04feb8beade9c65b`).

It is append-only and supersedes:
- §1.3's sentence "No HOSTING section or verification case uses sign-in or substitution evidence from DEL-01-05";
- §1.6;
- §2;
- §3's readings 2 and 3, and the "none" cells of its table;
- §4.

The rows, quotes, kinds, the ownership claim and the DAG-004 baseline stand, as RVG2 confirms.

### 6.1 C1-M1 — the residual on DEL-01-01 → DEL-01-05

**What HOSTING-BOUNDARY-v0.9 still takes from DEL-01-05.** These uses are independent of VER-005's clause.

| Use | Design text | Kind |
|---|---|---|
| Requested provider and model, carried per thread and turn | §8.3: "the provider and model the App **requested** (carried from the person's choice through DEL-01-05; at 0.158.0 `modelProvider` and model on thread start/resume …)". ACCESS §1 I-3: "Conversation start: explicit `modelProvider` and `model` on `thread/start` … \| DEL-01-05 → DEL-01-01 S-4" | **E.** Runtime values HOSTING carries and records, whose format is the supplier pin's (K-3) |
| Destination class | §8.3: "The destination **class** (local or cloud) is derived from the provider configuration the person chose (DEL-01-05), not inferred by this boundary." ACCESS I-4: "DEL-01-05 → DEL-01-01 §8.3 → DEL-04-03 RS R5" | **E.** A per-conversation runtime value whose values are RS R5's (`destinationClass`) |
| VC-26 live part, verification column VER-005 | Expected "class taken from DEL-01-05's configuration"; status "live start needs credential or local provider" | **V** (K-5) |

**GC-5 item 1.** Each use is a dependency: HOSTING's §8.3 output and its VC-26 verification depend on DEL-01-05's values. **Item 3** does not allow withdrawing the VER-005 clause while these uses stay in the Design.

**Can a rewording remove them? Not on the present sources.**
- The class route (I-4) could run DEL-01-05 → DEL-04-03 directly. That moves the E flow to a new arc DEL-04-03 → DEL-01-05, and needs S1 in DEL-04-03 CLM-004, which today receives "observed supplier facts (… model and destination …) from `DEL-01-01`".
- The I-3 carriage cannot be removed. DEL-01-01 is the one that sends `thread/start`, and integrator ruling R5-4 keeps "requested and effective values separate", so HOSTING must receive the requested values.
- VC-26's live part could run on DEL-01-01's own local-provider configuration, as OBS-1 did. But the class expectation would then move to DEL-01-05's own cases.
- I do not claim these sources support a complete removal.

**Repair.**
- **The residual is recorded as E, with V.** It sits on the arc DEL-01-01 → DEL-01-05, alongside DEP-01-01-024.
- **M-01 is superseded.** The withdrawal of VER-005's clause would only relabel the arc; it would not close it.
- **GC-5 item 3 instead asks for S1 carry-in.** DEL-01-01's ScopeOfWork should state the depended-on interface: DEL-01-05's provider selection and destination class, carried per turn (§8.3), and DEL-01-05's configuration for VC-26's live start. VER-005's input then stays named.
- **C1-m1 is answered.** No check is narrowed.
- **C1-m3 is answered.** No IV is claimed. M-01's withdrawal was a cut-like withdrawal of a test input, not an invert, and it is withdrawn.

**Restated per-option table** (G1 r3 kinds, graph-wide, 212 arcs; N08 not entered):

| Scenario | O-1 | O-2 | O-3 | O-4 |
|---|---|---|---|---|
| Today (DEP-01-01-024 V/L) | {01-01, 01-05}, 1 row | no component | no component | no component |
| With the residual recorded as E (with V) | {01-01, 01-05}, 1 row | **{01-01, 01-05}, 1 row** | **{01-01, 01-05}, 1 row** | acyclic |
| Owner per-edge cut of the arc DEL-01-01 → DEL-01-05 (M-02-R) | acyclic | acyclic | acyclic | acyclic |

**Owner acts per option.**

| Option | Owner act needed |
|---|---|
| O-4 | none; the E and V content leaves with the option |
| O-1, O-2, O-3 | one per-edge cut of the arc DEL-01-01 → DEL-01-05, covering DEP-01-01-024 and the E/V residual. This is CASE-001's R2, widened to the whole arc. No agent move closes it |

DEP-01-05-012 (P) is still not moved.

### 6.2 C1-M2 — N08 against the post-§23 move set

**Model.** N08 is entered as an I row (DEL-01-05 → DEL-04-03), over all 212 arcs, with G1 r3 kinds. "Group 1" is SCC-CASE-002's §22 move set with §23's five E residuals:
- **B:** without the P4 cut;
- **C:** with the P4 cut.

Cells give the component containing DEL-01-05 (C1-m2: "no N08 component" means no component containing DEL-01-05, not that the graph is acyclic).

| Scenario | O-1 | O-2 | O-3 | O-4 |
|---|---|---|---|---|
| N08 + group 1 (B); SCC-001 arc as today (V/L) | 18 members, 14 rows | 6 members, 6 rows: DEL-01-05 + {02-03, 03-03, 04-02, 04-03, 05-01} | 6 / 6 | no N08 component |
| N08 + group 1 (B); residual recorded as E (§6.1) | 18 / 14 | **13 / 8** (DEL-01-01 pulled back in) | **12 / 7** | no N08 component |
| N08 + group 1 (B); owner cut of the SCC-001 arc | 13 / 12 | 6 / 6 | 6 / 6 | no N08 component |
| N08 + group 1 (C) (P4 cut); residual E | 18 / 13 | 12 / 7 | 12 / 7 | no N08 component |
| N08 + group 1 (C); owner cut of the SCC-001 arc | 13 / 11 | 6 / 6 | 6 / 6 | no N08 component |

Adding P19's E residual (§23) leaves every cell above unchanged. These figures reproduce RVG2's.

**Readings 2 and 3 restated.**
- **Reading 2 (restated).**
  - Only under O-4 do SCC-002's moves leave N08 without a cycle.
  - Under O-2 and O-3, §23's E residuals keep the 5-member component {02-03, 03-03, 04-02, 04-03, 05-01}. DEP-05-01-026 (admitted, I) then closes N08's path back, and N08 joins DEL-01-05 to that component (6 members, 6 rows).
  - With this case's E residual, DEL-01-01 is pulled in as well.
- **Reading 3 (restated).**
  - Under O-1, N08 gives 18 members and 14 rows without the SCC-001 cut, and 13 members and 12 rows with it. The earlier "13 / 7" is withdrawn.
  - The SCC-001 cut still keeps DEL-01-01 and its neighbours out of an N08 merger, under every option.
- **N08's own move.** If N08 becomes an I row, it needs its own invert under O-1, O-2 and O-3, not only under O-1. That invert is ACCESS l.910: "DEL-01-05 is the class's source". It is outside this case.

### 6.3 Summary (supersedes §4)

| Pair | Kinds | Artefact? | Move | Residual | Owner acts |
|---|---|---|---|---|---|
| P1 01-01 ↔ 01-05 | DEP-01-01-024 V/L; DEP-01-05-012 P | Artefact | No agent move closes it. GC-5 S1 carry-in of HOSTING §8.3's and VC-26's uses into DEL-01-01's ScopeOfWork | E (with V) on DEL-01-01 → DEL-01-05 | O-4: none. O-1…O-3: one per-edge cut of that arc |

### 6.4 Not established (repair)

| Item | Why |
|---|---|
| Whether a rerouting of the class (I-4) directly to DEL-04-03 is acceptable to DEL-01-01's and DEL-04-03's design agents | It would move, not remove, the E flow |
| GC-5 item 4 | This case's "no new row" conclusions stay provisional until the G2b inventory reports |
