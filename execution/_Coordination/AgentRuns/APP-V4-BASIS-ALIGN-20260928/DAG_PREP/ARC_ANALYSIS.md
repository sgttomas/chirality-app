# ARC_ANALYSIS: the C1 arcs refreshed, SCC recomputation and the disputed arc (node P2)

- **Run and node:** `APP-V4-BASIS-ALIGN-20260928`, node P2. This is preparation only.
- **Basis:** commit `874508f16`.
- **Method:** `chirality-root:bundled:workflow:project-dag`, with its graph-version rules SR-1…SR-7 as confirmed for DAG-001 (`DAG-001/GRAPH_BASIS.md`; `BASIS_DECISION.md` DECISION-1).
- **Direction:** arcs are written **consumer → supplier** ("depends on"). An UPSTREAM row gives From → Target; a DOWNSTREAM row gives Target → From.
- **Companions:** [REGISTER_CHANGES.md](REGISTER_CHANGES.md) and [SUCCESSOR_PLAN.md](SUCCESSOR_PLAN.md).
- **Scripts and outputs:** `evidence/scc_recompute.py` and `evidence/scc_result.json`. Rerun from the repository root with `python3 <run>/DAG_PREP/evidence/scc_recompute.py <out.json>`. The cross-check is `evidence/audit_dag_crosscheck.json`.

## 1. Arc sets compared

| Set | Content | Arcs |
|---|---|---:|
| S0 | DAG-001: every ACTIVE EXECUTION deliverable-target row of the 41 live registers, one arc per ordered pair. Equal to DAG-001 `DependencyEdges.csv` + `CandidateEdges.csv` (checked) | 161 (109 admitted, 52 candidate) |
| S1 | S0 + the 40 distinct C1 arcs as proposed (C1's own check) | 201 |
| S2 | S0 + the **refreshed** set: 38 kept C1 arcs + R8-A, R8-B and X-1. N-12 and N-B8 are dropped | 202 |
| S2g | S0 + only the 32 arcs grounded without further P1 wording | 193 |

## 2. The 40 C1 arcs, re-checked against the current evidence

### 2.1 Result

| | Count |
|---|---:|
| C1 distinct arcs | 40 |
| Kept, evidence unchanged | 32 |
| Kept, Statement amended for R8-1 phasing (N-02, N-13, N-17, N-25, N-26, N-27) | 6 |
| **Dropped** (N-12, N-B8; §3) | **2** |
| **Added** by the refresh: R8-A and R8-B (R8-13 intake), X-1 (a side effect of C1 SoW correction SC-02-03-4) | **3** |
| Refreshed set | **41** |
| of which grounded by a C1 SoW correction | 32 |
| of which need P1 SoW wording or an owner declaration (§2.3) | 9 |

Every kept arc still has corroborating text in the current (post-R8) Design files. R6, R7 and R8 moved no relationship from one deliverable to another. R8 re-phased the hold content that 6 arcs carry, and it added the two network-destination relationships.

"Current evidence" in the table gives the Design line that corroborates each side, from the host register's own file. "SoW grounding" names the C1 SoW correction that makes the row extractable under the accepted rule (REGISTER_CHANGES §2.1). "Layer" follows DAG-001's rules on S2: arcs whose endpoints share a non-trivial SCC are **candidate** (SR-7, non-gating); the rest are **admitted**.

### 2.2 Arc table

| Arc | Consumer → supplier | Origin | Current evidence (Design corroboration, file:line) | R6–R8 effect | SoW grounding | Disposition | Layer |
|---|---|---|---|---|---|---|---|
| N-01 | DEL-04-02 → DEL-03-01 | C1-A | AS `AUTONOMY_AND_STANDING_EXCHANGE.md`:460; C `CATALOG_AND_READ_BASIS.md`:8 | none | SC-04-02-2 (its direct-consumption option) | KEEP | candidate |
| N-02 | DEL-04-02 → DEL-02-03 | C1-A | AS `AUTONOMY_AND_STANDING_EXCHANGE.md`:237; EXEC `EXECUTION_COMPATIBILITY.md`:1215 | Hold values → governance phase (R8-1); overlay annotations and report remain Phase 1. Amend | SC-04-02-2 (P1 refresh for R8-1) | KEEP (Statement amended) | candidate |
| N-03 | DEL-05-01 → DEL-04-02 | C1-A = C1-C #1 | AS `AUTONOMY_AND_STANDING_EXCHANGE.md`:12; LOOP `LOOP_RECEIVING_CONTRACT.md`:1368 | R8-13 adds network grants to the grant in force | S5-1-1; SC-04-02-2 | KEEP | candidate |
| N-04 | DEL-05-02 → DEL-04-02 | C1-A = C1-C #2 | AS `AUTONOMY_AND_STANDING_EXCHANGE.md`:12; PANEL `PANEL_RECEIVING_CONTRACT.md`:461 | R8-13 adds ND-5 network-destination grant display from AS §3 | S5-2-2; SC-04-02-2 | KEEP | candidate |
| N-05 | DEL-03-02 → DEL-04-02 | C1-A = C1-B N-B2 | AS `AUTONOMY_AND_STANDING_EXCHANGE.md`:12; P `PROPOSAL_LIFECYCLE_AND_OUTCOMES.md`:701 | none | SC-04-02-2 | KEEP | candidate |
| N-06 | DEL-03-03 → DEL-04-02 | C1-A = N-B5 | AS `AUTONOMY_AND_STANDING_EXCHANGE.md`:12; ADAPTER `ADAPTER_ENABLEMENT_AND_RECEIVING.md`:1055 | none | SC-04-02-2 | KEEP | candidate |
| N-07 | DEL-02-03 → DEL-04-02 | C1-A | AS `AUTONOMY_AND_STANDING_EXCHANGE.md`:12; EXEC `EXECUTION_COMPATIBILITY.md`:1197 | none | SC-02-03-4; SC-04-02-2 | KEEP | candidate |
| N-08 | DEL-09-06 → DEL-04-02 | C1-A = C1-C #10 | CA `CONNECTED_ACTIVITY_CONTRACT.md`:541 | none | S9-6-3 | KEEP | admitted |
| N-09 | DEL-09-09 → DEL-04-02 | C1-A = C1-C #13 | XT `EXTERNAL_TRACE_CASES.md`:110 | none | S9-9-4 | KEEP | candidate |
| N-10 | DEL-04-03 → DEL-03-01 | C1-A | RS `RECORD_SEMANTICS.md`:448; C `CATALOG_AND_READ_BASIS.md`:8 | none | SC-04-03-1 | KEEP | candidate |
| N-11 | DEL-03-01 → DEL-04-03 | C1-A = N-B1 | RS `RECORD_SEMANTICS.md`:448; C `CATALOG_AND_READ_BASIS.md`:479 | none | **needs P1 wording or a declaration** (P1) | KEEP | candidate |
| N-12 | DEL-03-02 → DEL-04-03 | C1-A | see §3 | P-v0.6 §13 still has no Expect-from DEL-04-03 | — | **DROP** (not proposed) | — |
| N-13 | DEL-04-03 → DEL-02-03 | C1-A | RS `RECORD_SEMANTICS.md`:447; EXEC `EXECUTION_COMPATIBILITY.md`:1212 | Hold machine → governance phase; recording rules Phase 1. Amend | SC-04-03-1 (P1 refresh for R8-1) | KEEP (Statement amended) | candidate |
| N-14 | DEL-04-03 → DEL-03-03 | C1-A | RS `RECORD_SEMANTICS.md`:450; ADAPTER `ADAPTER_ENABLEMENT_AND_RECEIVING.md`:1062 | none | SC-04-03-1 | KEEP | candidate |
| N-15 | DEL-04-03 → DEL-01-01 | C1-A | RS `RECORD_SEMANTICS.md`:454 | R8-13 RS R15 is host-loop only; R5/R13 facts from HOSTING §8.3 unchanged | SC-04-03-1 | KEEP (confirm at K1) | admitted |
| N-16 | DEL-02-01 → DEL-01-01 | C1-A | WD `WORKFLOW_DECLARATION.md`:929 | none | SC-02-01-1, SC-02-01-2 | KEEP | admitted |
| N-17 | DEL-02-01 → DEL-02-03 | C1-A | WD `WORKFLOW_DECLARATION.md`:923; EXEC `EXECUTION_COMPATIBILITY.md`:1210 | Hold support governance phase; Phase-1 statement §2.1 and `governed` flag added (R8-1). Amend | **needs P1 wording or a declaration** (P1 (SC-02-01-6 refreshed to state consumption of DEL-02-03)) | KEEP (Statement amended) | candidate |
| N-18 | DEL-02-01 → DEL-03-02 | C1-A | WD `WORKFLOW_DECLARATION.md`:925; P `PROPOSAL_LIFECYCLE_AND_OUTCOMES.md`:709 | none | SC-02-01-1, SC-02-01-3 | KEEP | candidate |
| N-19 | DEL-09-06 → DEL-02-01 | C1-A = C1-C #4 | WD `WORKFLOW_DECLARATION.md`:20; CA `CONNECTED_ACTIVITY_CONTRACT.md`:541 | none | S9-6-3 | KEEP | admitted |
| N-20 | DEL-03-03 → DEL-02-01 | C1-A = N-B6 | WD `WORKFLOW_DECLARATION.md`:956; ADAPTER `ADAPTER_ENABLEMENT_AND_RECEIVING.md`:1057 | none | **needs P1 wording or a declaration** (P1 (SC-02-01-1 must name DEL-03-03 as a receiver, not as a supplier)) | KEEP | candidate |
| N-21 | DEL-02-03 → DEL-03-02 | C1-A | EXEC `EXECUTION_COMPATIBILITY.md`:1195; P `PROPOSAL_LIFECYCLE_AND_OUTCOMES.md`:709 | none | SC-02-03-4 | KEEP | candidate |
| N-22 | DEL-02-03 → DEL-05-01 | C1-A | EXEC `EXECUTION_COMPATIBILITY.md`:1199 | LOOP §2.4.4 host-loop hold → governance phase (R8-8); arrival/binding/events unchanged | **needs P1 wording or a declaration** (P1) | KEEP | candidate |
| N-23 | DEL-02-03 → DEL-01-01 | C1-A | EXEC `EXECUTION_COMPATIBILITY.md`:1200 | none | SC-02-03-4 | KEEP | admitted |
| N-24 | DEL-02-03 → DEL-03-03 | C1-A | EXEC `EXECUTION_COMPATIBILITY.md`:1201; ADAPTER `ADAPTER_ENABLEMENT_AND_RECEIVING.md`:1063 | none | SC-02-03-4 | KEEP | candidate |
| N-25 | DEL-05-02 → DEL-02-03 | C1-A = C1-C #3 | EXEC `EXECUTION_COMPATIBILITY.md`:1215; PANEL `PANEL_RECEIVING_CONTRACT.md`:47 | PANEL now reads EXEC §2.1–§2.2 and CR-8/CR-9 directly; C1 condition obsolete. Amend | S5-2-3 (main option; P1 refresh for R8-1) | KEEP (Statement amended) | candidate |
| N-26 | DEL-09-09 → DEL-02-03 | C1-A = C1-C #14 | XT `EXTERNAL_TRACE_CASES.md`:244 | IN-25 governance-phase only; TS-0/CMP-01 compatibility report per surface is Phase 1. Amend | S9-9-4 (P1 refresh for R8-1) | KEEP (Statement amended) | candidate |
| N-27 | DEL-03-03 → DEL-02-03 | C1-A = N-B7 | EXEC `EXECUTION_COMPATIBILITY.md`:1213; ADAPTER `ADAPTER_ENABLEMENT_AND_RECEIVING.md`:1057 | ADAPTER §11 now "Phase 1 guidance and recording … governance phase: hold machine". Amend | **needs P1 wording or a declaration** (P1 (S-03-4 refreshed for R8-1 and naming DEL-02-03)) | KEEP (Statement amended) | candidate |
| N-28 | DEL-09-06 → DEL-04-01 | C1-A = C1-C #9 | CA `CONNECTED_ACTIVITY_CONTRACT.md`:540 | none | S9-6-3 | KEEP | admitted |
| N-B3 | DEL-03-02 → DEL-02-01 | C1-B | WD `WORKFLOW_DECLARATION.md`:913; P `PROPOSAL_LIFECYCLE_AND_OUTCOMES.md`:702 | none | **needs P1 wording or a declaration** (P1) | KEEP | candidate |
| N-B4 | DEL-03-03 → DEL-01-01 | C1-B | ADAPTER `ADAPTER_ENABLEMENT_AND_RECEIVING.md`:1056 | none | **needs P1 wording or a declaration** (P1) | KEEP | admitted |
| N-B8 | DEL-03-03 → DEL-04-03 | C1-B | see §3 | ADAPTER-v0.4 §11 has no Expect-from DEL-04-03 | — | **DROP** (not proposed) | — |
| N-B9 | DEL-03-04 → DEL-01-01 | C1-B | GUIDE `HOST_INTEGRATION_GUIDE.md`:349 | none | S-04-6 | KEEP | admitted |
| N-B10 | DEL-03-04 → DEL-09-06 | C1-B | GUIDE `HOST_INTEGRATION_GUIDE.md`:350 | GUIDE-v0.3 also consumes the SWBPIPE answers (ANS, FACTS) held in DEL-09-06 | S-04-6 | KEEP | admitted |
| N-B11 | DEL-03-04 → DEL-09-09 | C1-B | GUIDE `HOST_INTEGRATION_GUIDE.md`:353 | none | S-04-6 | KEEP | admitted |
| N-C1 | DEL-09-06 → DEL-02-02 | C1-C #5 | CA `CONNECTED_ACTIVITY_CONTRACT.md`:546 | none | S9-6-3 | KEEP | admitted |
| N-C2 | DEL-09-06 → DEL-03-01 | C1-C #6 | CA `CONNECTED_ACTIVITY_CONTRACT.md`:540 | none | S9-6-3 | KEEP | admitted |
| N-C3 | DEL-09-06 → DEL-03-02 | C1-C #7 | CA `CONNECTED_ACTIVITY_CONTRACT.md`:541 | none | S9-6-3 | KEEP | admitted |
| N-C4 | DEL-09-06 → DEL-03-03 | C1-C #8 | CA `CONNECTED_ACTIVITY_CONTRACT.md`:543 | ADAPTER F-22…F-24 ruled (R8-12) | S9-6-3 | KEEP | admitted |
| N-C5 | DEL-09-06 → DEL-01-01 | C1-C #11 | CA `CONNECTED_ACTIVITY_CONTRACT.md`:541 | none | S9-6-3 | KEEP | admitted |
| N-C6 | DEL-09-09 → DEL-05-01 | C1-C #12 | XT `EXTERNAL_TRACE_CASES.md`:103 | none | S9-9-4 | KEEP | candidate |
| R8-A | DEL-04-02 → DEL-05-01 | R8 intake | AS `AUTONOMY_AND_STANDING_EXCHANGE.md`:213 (+214) | New, from R8-13 (DECISION-5): the AS §3 network-destination display is taken "from the host's control (LOOP §5.1.1 …)" | **needs P1 wording or a declaration** (P1) | ADD | candidate |
| R8-B | DEL-04-03 → DEL-05-01 | R8 intake | RS `RECORD_SEMANTICS.md`:194 | New, from R8-13: the R15 source is "through DEL-05-01 events (LOOP §2.3, §5.1.1)" | **needs P1 wording or a declaration** (P1) | ADD | candidate |
| X-1 | DEL-02-03 → DEL-01-04 | found in refresh | EXEC `EXECUTION_COMPATIBILITY.md`:1202 | None. It is a side effect of C1 SC-02-03-4 (see REGISTER_CHANGES §2.4 item 2) | SC-02-03-4 | ADD | candidate |

### 2.3 Arcs whose SoW grounding is missing (owner item O-2)

The current Design text supports each of these arcs, but no C1 SoW correction states the consumption. The current SoWs name the other deliverable only as an *owner*, and DAG-001 extraction did not read ownership sentences as inputs. Under the accepted rule ("local SoWs and accepted interfaces") extraction cannot write them. Each takes one of three routes:
- **(a)** P1 adds a consumption sentence to the host SoW, traced to the accepted C1 arc proposal, and extraction writes the row. **Recommended.**
- **(b)** The owner declares the relationship in `_DEPENDENCIES.md`.
- **(c)** It is left out. This is SCC-neutral (§4).

| Arc | Row to write (host) | Natural P1 hook | Layer |
|---|---|---|---|
| N-11 DEL-03-01 → DEL-04-03 | N-B1 (DEL-03-01) | DEL-03-01 CLM or REQ-004 near S-01-4: "consumes the DEL-04-03 act field set and lapse vocabulary". Alternatively, refine DEL-04-03 SC-04-03-2 "PKG-03 basis/receipts" to name DEL-03-01 | candidate |
| N-17 DEL-02-01 → DEL-02-03 | R-02-01-h (DEL-02-01) | SC-02-01-6 (TBD-004), refreshed for DECISION-4, stating that WD adopts EXEC's Phase-1 statement and governance-phase hold values | candidate |
| N-20 DEL-03-03 → DEL-02-01 | R-02-01-k (DEL-02-01, DOWNSTREAM) | SC-02-01-1 reworded so that DEL-03-03 *receives* the declared constraints (also avoids the reverse arc; REGISTER_CHANGES §2.4 item 1) | candidate |
| N-22 DEL-02-03 → DEL-05-01 | R-02-03-e (DEL-02-03) | SC-02-03-4: add "`DEL-05-01` supplies arrival observation, binding and loop events" | candidate |
| N-27 DEL-03-03 → DEL-02-03 | N-B7 (DEL-03-03) | S-03-4 refreshed for R8-1 and naming DEL-02-03 | candidate |
| N-B3 DEL-03-02 → DEL-02-01 | N-B3 (DEL-03-02) | A new DEL-03-02 CLM sentence: "consumes DEL-02-01 workflow identity and checkpoint declarations" | candidate |
| N-B4 DEL-03-03 → DEL-01-01 | N-B4 (DEL-03-03) | A new DEL-03-03 CLM sentence: "consumes DEL-01-01 supplier surfaces at the pin" | **admitted** |
| R8-A DEL-04-02 → DEL-05-01 | R8-AS-1 (DEL-04-02) | A DEL-04-02 sentence carrying DECISION-5's network-destination display, if P1's DECISION-5 wording reaches this SoW | candidate |
| R8-B DEL-04-03 → DEL-05-01 | R8-RS-1 (DEL-04-03) | SC-04-03-1 extended: "network-destination events from `DEL-05-01`" (R15) | candidate |

## 3. The disputed arc DEL-03-02 → DEL-04-03 (C1-A N-12)

The question is whether the proposal contract (P, DEL-03-02) requires a contribution from the record semantics (RS, DEL-04-03) before part of its own work. Both are in SCC-002, so the arc would sit in the non-gating candidate layer either way. It changes no SCC membership (§4), no readiness verdict and no schedule. What is at stake is only whether the registers assert a consumption that the consumer does not state.

### 3.1 Evidence for the arc

1. **RS-v0.6 §10, row DEL-03-02** (`RECORD_SEMANTICS.md`:449) reads:

   > "| DEL-03-02 | §5 evidence rules | §9 outcomes; …"

   Its "Consumes (meaning)" column says that P consumes RS §5. This is the strongest item, and it is on the supplier's side.
2. **C1-A N-12** cites V1-B RF-03 and reads "P §4.1 consumes acceptance acts".
3. **DEL-04-03 SoW CLM-004** reads "PKG-03 basis/receipts … consume this format" (DEP-04-03-012 → PKG-03). The package includes DEL-03-02.
4. **P cites RS elements:**
   - §3.2: author identity "DEL-04-03 R11 records it as an evidence limit";
   - §3.3: "The App-side request origin is recorded by DEL-04-03" and "recorded as an evidence limit (DEL-04-03 R11)";
   - §4.5: acts "lapse under the ordinary rule (V4-HI-32; DEL-04-03 L-6)".

### 3.2 Evidence against the arc

1. **P-v0.6 §13, "Interfaces provided and expected"** (`PROPOSAL_LIFECYCLE_AND_OUTCOMES.md`:695–713):
   - it has "Expect from" rows for DEL-03-01, DEL-04-01, DEL-04-02, DEL-02-01 and the host owner, and **none for DEL-04-03**;
   - it has a "Provide to DEL-04-03" row. This is unchanged since P-v0.5, which C1-B compared.
2. **P §2 authority table** (line 80) reads:

   > "Human-act and run-record format | DEL-04-03 | Supplied: outcomes, receipt links, change-item content identity, item-left events"

   P's stated role toward RS is supplier.
3. **P §4.1** takes acceptance from the host. The *accepted* state is entered by "The person (A5); host captures", with evidence "Host-captured A5 bound to the change-item content identity". The authority table adds that P "Consumes captured acts as evidence" from the host's facility, not from RS records. C1-A's reading, "P §4.1 consumes acceptance acts", describes host capture, not DEL-04-03.
4. **The RS side depends on P, not the reverse.**
   - RS §5, "Operation entries and outcome evidence", adopts P's vocabulary: "Outcome vocabulary is DEL-03-02 §9 … adopted unchanged" (line 253) and "request-side origin per DEL-03-02 §3.3" (line 230).
   - The "§5 evidence rules" that RS §10 says P consumes are RS's rules for recording P's outcomes. P's own reporting rule ("Applied is reported only with a host receipt reference", §4.1 rule 2) is stated in P and does not cite RS.
5. **P's citations of R11 and L-6 point to where its outputs land** (evidence limits recorded in R11) and to a lapse rule whose meaning is ACT's:
   - ACT §10.1 V-06 lists DEL-03-02 as a consumer of content binding, lapse, supersession and undo;
   - the existing arc DEL-03-02 → DEL-04-01 (DEP-03-02-017) already carries that.
6. **The DEL-03-02 SoW names DEL-04-03 four times, always as the owner of records.** DAG-001 extraction took these as DEP-03-02-019, DOWNSTREAM HANDOVER from P to RS. No C1 SoW correction for DEL-03-02 states consumption of DEL-04-03. The RS-side correction SC-04-03-1 states that RS *receives* outcomes, content identities and receipt links from DEL-03-02. The arc therefore has no SoW grounding (REGISTER_CHANGES §2.1).
7. **C1-B**, which compared the supplier text directly, did not support it. The same reasoning applies to the adapter (N-B8, below).

### 3.3 Recommendation: not proposed

This agrees with the integrator's lean. The consumer's own contract does not state the input. The supplier-side table cell is the only support, and it describes a record-destination relationship. The arc is SCC-neutral and has no grounding.

**Actions:**
- **Withhold the arc in the registers.** No DEL-03-02 UPSTREAM row and no DEL-04-03 DOWNSTREAM row (R-04-03-p is dropped).
- **Keep package row DEP-04-03-012 (→ PKG-03) unchanged.** It is non-topological. C1-B's alternative, retargeting it to DEL-03-01 only, would be a SoW-driven change and is not needed for DAG-002.
- **Route the RS §10 DEL-03-02 cell to DEL-04-03's owner** as a wording finding for the next RS revision. The owner either restates it as "P's outcomes are recorded under §5", or, if P really needs RS §5 before part of its work, P adds an "Expect from DEL-04-03" row and a later extraction pass adds the arc as a new departure.
- **Record the ruling at K1** in the decision record, so that the extraction briefs can cite it.

**The same treatment applies to N-B8 (DEL-03-03 → DEL-04-03).**
- ADAPTER-v0.4 §11 has no "Expect from DEL-04-03" row, and it "Provide[s] to DEL-04-03" external dispatch entries, recorded acts and evidence limits.
- Its header lists RS R5/R7/R11/R13 "for joins only", to name where the adapter's evidence lands.
- RS §10's DEL-03-03 row is the mirror image of the DEL-03-02 cell.
- C1-B itself allowed "keep only N-14".

**Recommendation:** drop N-B8 and keep N-14 (DEL-04-03 → DEL-03-03). This is SCC-neutral.

## 4. SCC recomputation

Tarjan's algorithm over the 41 inventory nodes (`evidence/scc_recompute.py`):

| Set | Non-trivial SCCs (member counts) | Change from DAG-001 |
|---|---|---|
| S0 (DAG-001) | SCC-001 {01-01, 01-05} 2; SCC-002 13; SCC-003 {01-06, 09-01} 2; SCC-004 {07-01, 07-02, 08-01} 3; SCC-005 {10-02, 10-04} 2; SCC-006 {11-01, 11-03} 2 | — |
| S1 (C1's 40 arcs) | identical | **none**. This confirms C1's statement |
| S2 (refreshed 41) | identical | **none** |
| S2g (32 grounded only) | identical | **none** |

SCC-002 remains the 13 members DEL-01-04, 02-01, 02-02, 02-03, 02-04, 03-01, 03-02, 03-03, 04-02, 04-03, 05-01, 05-02 and 09-09.

- **Any outcome of O-2 gives the same SCCs.** Adding arcs can only merge components. S0 and S2 have identical partitions, so every arc set between them has the same partition too. Whichever of the 9 ungrounded arcs are grounded, declared or left out, SCC membership is unchanged.
- **Cross-check.** The registered `tools/coordination/audit_dag.py` (sha256 `830d0d53…3449a`, unchanged since DAG-001) was run without `--strict` on a scratch file of DAG-001's 161 admissible rows plus 41 synthetic rows for S2. It exits 0 and reports the same six SCCs (`active_graph.sccs`; `evidence/audit_dag_crosscheck.json`).
- **The admitted layer of S2 has no SCC.** Tarjan's algorithm on the 124 admitted arcs finds none, and no existing DAG-001 arc changes layer.
- **No case opens or closes.** CASE-002 gains held arcs within its unchanged 13-member set: 26, or 18 if only the grounded arcs are added. It should be updated through `scc-resolution-case`, with evidence rows only and no ruling (SUCCESSOR_PLAN §2, step 5).

### 4.1 The five SCC-enlarging arcs stay out

Each was re-tested alone on S2 and on S1:

| # | Arc | Current text that might suggest it | Effect if added (S2) | Stays out? |
|---|---|---|---|---|
| E-1 | DEL-09-09 → DEL-09-06 | XT uses RELAY and the CA §7.2 ladder; CA §11.2 provides DEL-09-09 the step map and relay file | SCC-002 → **14** (adds DEL-09-06) | **Yes.** XT's real inputs are the SWBPIPE answers (DEP-001, DEP-09-09-014), and host joins are deferred (DECISION-3) |
| E-2 | DEL-09-09 → DEL-03-04 | XT cites GUIDE as a reference | SCC-002 → **19**: adds DEL-03-04 and DEL-09-06, and absorbs SCC-004 {07-01, 07-02, 08-01} and DEL-08-02 | **Yes.** Reverse citation of a reader guide |
| E-3 | DEL-04-01 → DEL-03-01 | C Receivers "DEL-04-01 (fixture re-pointing)"; ACT §5.1 lists operation identity from DEL-03-01 as a **runtime** resolution input | SCC-002 → **16** (adds DEL-04-01, DEL-01-02, DEL-01-03) | **Yes.** A fixture citation and a runtime input to the policy function, not a production input to ACT's definition |
| E-4 | DEL-04-01 → DEL-03-03 | ACT cites ADAPTER v0.1/v0.2 | SCC-002 → **16** (same) | **Yes** |
| E-5 | DEL-09-06 → DEL-03-04 | CA cites GUIDE (GUIDE only sourced SQ-29…32) | New 2-node SCC {03-04, 09-06}, with N-B10 | **Yes** |

The R6–R8 and R8-13 changes add no text that turns any of these into a consumed input. R8-13 adds one more citation of the same kind (K-1 below).

### 4.2 Other relationships in the current text that stay out

These are not proposed, with their tested effect:

| # | Relationship (consumer → supplier) | Source text | Effect on S2 | Reason |
|---|---|---|---|---|
| K-1 | DEL-04-01 → DEL-05-01 | **R8-13:** ACT §2.7 "The network rules themselves are LOOP-v0.6 §5.1.1" | SCC-002 → **16** (as E-3) | ACT's A12 subclass is grounded in DECISION-1 D2(e) and DECISION-5, not in LOOP's definition. The citation names where the rules live. LOOP already consumes ACT (DEP-05-01-018) |
| K-2 | DEL-04-01 → DEL-02-01 | WD §8 receivers "DEL-04-01 policy"; ACT §5.1 checkpoint state from DEL-02-01, DEL-02-03, DEL-05-01, P (runtime) | SCC-002 → **16** | As E-3 |
| K-3 | DEL-01-01 → DEL-03-03 | ADAPTER §11 "Provide to DEL-01-01: observed MCP/dynamic-tool facts for the classification R4-12 assigns to HOSTING" | **SCC-001 + SCC-002 + SCC-003 merge (19)** | An observation fed back for HOSTING's classification, not an input HOSTING's boundary contract waits for. **The new admitted arcs into DEL-01-01 (N-15, N-16, N-23, N-B4, N-B9, N-C5) make any such reverse arc merge SCCs.** Even at S0 the path DEL-04-03 → DEL-01-02 → DEL-01-01 already does |
| K-4 | DEL-01-01 → DEL-04-03 | RS §10 "DEL-01-01 consumes R3, R5, R13 meanings" | merge (19) | HOSTING S-7 supplies observed facts "through DEL-01-02". It records into RS; it does not consume RS before its work |
| K-5 | DEL-01-01 → DEL-05-01 | R8-13 HOSTING scope note "governs host agents only (LOOP-v0.6 §5.1.1)" | merge (19) | A scope note |
| K-6 | DEL-09-06 → DEL-09-09 | CA §11.1 "DEL-09-09 \| V4-EXM-25 joined cases XC-*" | none | C1-C: coordination under CLM-006, not a consumed input |
| K-7 | DEL-09-06 → DEL-09-07 | CA §11.1 "DEL-09-07 \| V4-EXM-20…23 on CA/E — Not in this undertaking" | new SCC {09-06, 09-07} | Shared activity; DEL-09-07 consumes CA (DEP-09-07-011) |
| K-8 | DEL-04-03 → DEL-02-01 | RS §10 "DEL-02-01 … Supplies back: workflow identity; checkpoint reached-when, subject class" | none (inside SCC-002) | Not in C1. No SoW grounding. Candidate for a later extraction pass; noted for the integrator |
| K-9 | DEL-02-01 → DEL-03-03 | Only SC-02-01-1's wording (REGISTER_CHANGES §2.4 item 1) | none | Unevidenced direction; guard in the brief |
| K-10 | DEL-04-02 → DEL-05-02 | AS §3 "(… PANEL §3.8 ND-5)" | none | A presentation cross-reference; PANEL consumes AS (N-04) |
| K-11 | DEL-03-03 → DEL-09-06 | ADAPTER §11 "Expect from DEL-09-06/RELAY-v0.3 … as the single relay channel" | SCC-002 → **14** (adds DEL-09-06, which already reaches SCC-002 through DEP-09-06-013 and now N-C4) | C1-B: the actual inputs are the SWBPIPE answers (DEP-03-03-010/-011). Guard in the DEL-03-03 brief |
| K-12 | DEL-01-01 → DEL-04-01 | ACT V-21 lists DEL-01-01 as a consumer | none | C1-A/C1-B: D3 reaches DEL-01-01 through DECISION-1 (R-10); DEP-01-01-021/-022/-024 suffice |

## 5. Layer placement under DAG-001's rules

SR-1…SR-5 carry forward unchanged: all canonical types, no cut or merge ruling, no confirmation hold. SR-6 chooses the representative, and SR-7 holds intra-SCC arcs.

| Refreshed arcs | Admitted layer | Candidate layer (SCC-002 / CASE-002) |
|---|---|---|
| Grounded (32) | 14: N-08, N-15, N-16, N-19, N-23, N-28, N-B9, N-B10, N-B11, N-C1, N-C2, N-C3, N-C4, N-C5 | 18: N-01…N-07, N-09, N-10, N-13, N-14, N-18, N-21, N-24, N-25, N-26, N-C6, X-1 |
| Needing P1 or a declaration (9) | 1: N-B4 | 8: N-11, N-17, N-20, N-22, N-27, N-B3, R8-A, R8-B |
| **Total (41)** | **15** | **26** |

**Expected DAG-002 counts:**

| Case | Admitted | Candidate | Total | SCCs | Nodes |
|---|---:|---:|---:|---|---:|
| All 41 arcs | 124 | 78 | 202 | 6, unchanged | 41, inventory unchanged (GROUP3) |
| Grounded arcs only | 123 | 70 | 193 | 6, unchanged | 41 |

In both cases the admitted layer is acyclic.

**Where the new admitted arcs point:**
- DEL-01-01 is a new admitted supplier to DEL-02-01, 02-03, 03-03, 03-04, 04-03 and 09-06. It sits in SCC-001, whose two held arcs are unchanged.
- DEL-09-06 is a new admitted consumer of DEL-01-01, 02-01, 02-02, 03-01, 03-02, 03-03, 04-01 and 04-02. It stays outside SCC-002 **only while no reverse arc is added** (E-1, E-5, K-6/K-11 guards).
- DEL-03-04 is a new admitted consumer of DEL-01-01, 09-06 and 09-09.

**Representative rows change on 4 existing arcs** (SR-6, consumer UPSTREAM first). This is evidence drift, not a departure:

| Arc | DAG-001 representative | New representative | Layer |
|---|---|---|---|
| DEL-04-02 → DEL-03-02 | DEP-03-02-018 | R-04-02-a (DEP-04-02-015) | candidate |
| DEL-04-03 → DEL-04-01 | DEP-04-01-016 | R-04-03-a | admitted |
| DEL-04-03 → DEL-03-02 | DEP-03-02-019 | R-04-03-b | candidate |
| DEL-04-03 → DEL-04-02 | DEP-04-02-009 | R-04-03-c | candidate |

In each case the old representative becomes a MIRROR. Its type differs (HANDOVER against INTERFACE), which is complementary in DAG-001's MirrorAssessment reading. The assembling TASK re-runs the mirror comparison for these four.

