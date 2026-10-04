# G2b — Abbreviation-aware inventory of cross-deliverable Design uses (GC-5)

- **Run.** `APP-V4-GRAPH-CLOSURE-20261004`, survey G2b. A Type 2 TASK for HELP_HUMAN (Claude Opus 5.5), with no delegation.
- **Standing.** This is survey evidence. It decides nothing and changes no row, register, ScopeOfWork, Design file, case file or DAG. "Dependency" below means a dependency under GC-5 item 1, as this survey reads it. Every classification is a reading for review.
- **Paths.** `E/` is `projects/chirality-app-v4/execution/`.
- **Basis.**
  - HEAD `765936cbb1`, clean tree. No `Design/` file changed between `35f2d2ca38` (the brief's commit) and HEAD (`git diff --name-only`).
  - Inputs, by sha256:
    - `GC_RULINGS.md` `e375cabe…` (GC-1…GC-6; GC-6 was added during this survey and changes no classification rule used here);
    - `SURVEY/G1.md` r3 `3d6543bc…` (kinds K-1…K-7; options O-1…O-4);
    - `reviews/RVG-ACT51.md` `6edbaf25…`;
    - `SURVEY/G2.md` `24cc2a6f…`;
    - DAG-004 `DependencyEdges.csv` `c4303374…` and `CandidateEdges.csv` `2bfff10e…`;
    - `dag_reach.py` `63259575…` (DEL-10-04 `Design/prototype/`).
- **Scripts.** All scripts are scratch files under `$TMPDIR/g2b/`, not in the repository:
  - `scan.py`: alias map and scan;
  - `kinds.py`: G1 r3 kind of each arc;
  - `reach.py`: option-aware reach and SCC effect;
  - `show.py`: line review.

## 1. Method

1. **Alias map (§2).** Built from every top-level `Design/*.md` and `Design/*.schema.json` of the 41 deliverables:
   - each contribution label (`DEL-xx-yy/ABBR-vN`, collected from every header);
   - every Design file name;
   - every schema file name and its dotted or underscored stem;
   - every schema `$id`.
   
   Matching follows these rules:
   - **Distinctive abbreviations** are matched as words wherever they appear: HOSTING, RECOVERY, NPTD, AAC, NIR, ACCESS, WD, WR, EXEC, ROLE, ADAPTER, GUIDE, ACT-POLICY, RS, LOOP, PANEL, RELAY, XT, LHQ, RRM, DAC, EXP.
   - **Short or ambiguous abbreviations** count only when followed by a version (`-v0`), a section (`§`) or a rule/element id (for example `P §9`, `C-v0.8`, `AS §3`, `RP-R6`): C, P, ACT, AS, CA, FR, FV, DV, UC, EB, RA, DA, AA, RP, PV, CW, DOS, TOP, CIR, PRC, CFB, DRC, RTD, SPIKE, PKG, SQ.
   - `SQ-nn` relay-question ids are not mapped. They identify SWBPIPE's answers held in DEL-09-06's folder, which ADAPTER §11 records as "not a contribution".
   - `CA` maps to DEL-09-06, except in files of DEL-10-03 and DEL-11-01…11-03, where it means DEL-11-01's continuity account.
   - `PKG` maps only to `PKG-v0`/`PKG §`, never to a package id.
   - Plain-word schema stems (`catalog`, `proposal`) are dropped as false matches.
   
   The map has **300 entries** (58 abbreviation forms, 118 file names, 61 schema stems, 63 `$id` values), plus the `DEL-xx-yy` pattern.
2. **Scan.**
   - **Markdown.** Each line of the 55 top-level Design files is matched against the map. Every line that names another deliverable becomes one *use* for the pair (citing deliverable → named deliverable). Each use is tagged *history* (under a "Changes" heading), *pin* (the line carries a content hash) or *body*.
   - **Schemas.** Every non-local `$ref` in every Design JSON file was listed. There are 39, of which 37 cross deliverables. They fall on 7 pairs, all carried by DAG-004 arcs: 02-02→02-01, 03-02→03-01, 03-03→03-01, 04-03→02-03, 04-03→04-02, 07-01→07-02 and 08-01→07-02.
   - **Result.** 10,584 uses on 536 ordered pairs. 211 pairs are DAG-004 arcs in the same direction; one more arc (09-05→01-03) has no use in the consumer's Design. The other 325 pairs, plus one pair found by cross-check (09-11→06-02, through the FX-DP1 fixture), are the 326 candidates classified in §4.
3. **Classification (GC-5).** Each candidate pair was read line by line, use-verb lines first ("consumes", "relies", "uses", "adopts", "per", "mirrors", "follows", "validates against" and similar). It is counted once:
   - **Dependency (K-2/K-4).** The consumer's own rules, outputs, fixtures or checks need the supplier's rule, vocabulary, state set, identity scheme or artifact. The deciding sentence is quoted. Kinds follow G1 r3. V (K-5) and L (K-6) are noted where they apply.
   - **Not a dependency.** One of the GC-5 item 2 exclusions applies:
     - attribution, owner map, receiver list, cross-reference or example;
     - an uninterpreted identifier (GC-3);
     - content carried by a ruling's or the basis's own text. RVG-ACT51's ACT-M1(b) test is used: a ruling counts only where its own text states the rule. A ruling that only points to a Design does not.
     
     Two further reasons are used:
     - **Runtime value.** The Design says the value is handed at run time, and its rules do not use the value's internal structure (GC-1(a)). Where they do use it, the pair is classed as a dependency (FR→ROLE) or unclear (NPTD→EXEC).
     - **Pin-only or label-list mention.**
   - **Unclear.** The text supports both readings. It is quoted.
4. **For each dependency** (§5):
   - its status: DAG-004 arc (matched), one of G2's 30, a G2 §5 ambiguous item, or new;
   - the `dag_reach.py --dag DAG-004 CONSUMER SUPPLIER` verdict;
   - the effect under O-1…O-4, from `reach.py`. Each arc is given the G1 r3 primary kind of its representative row, parsed from G1's §2 and Appendix A tables, so all 212 are classified. O-2 drops V, O-3 drops V and L, and O-4 keeps only P and I. The new pair is filtered by its own kind.
   
   Effects are given as **inside** (no membership change), **GROW** (members join), **MERGE** (existing SCCs join) or **NEW**.
5. **Cases (§6).** Each new SCC-forming or unclear pair is checked against the member sets of the open analyses: SCC-CASE-001, 002 (with ACT51), 003, 005, 006 and 007, and SCC-CANDIDATE-N13.

## 2. Alias map (300 entries)

| Deliverable | Abbreviations (as matched) | Design files | Schema files, stems and `$id` |
|---|---|---|---|
| DEL-01-01 | HOSTING, HOSTING-BOUNDARY, OBS-1, OBS-1b, OBS-2, OBS-3, PIN-SPIKE, PIN_SPIKE, SPIKE | `HOSTING_BOUNDARY.md`, `OBS_1_0.158.0.md`, `OBS_2_0.158.0.md`, `OBS_3_0.158.0.md`, `PIN_SPIKE_0.158.0.md`, `VERSION_ADVANCE_0.160.0.md` | `hosting.client-request-record.schema.json`; `hosting.lifecycle-event.schema.json`; `hosting.server-request-entry.schema.json`; `urn:chirality:del-01-01:hosting-boundary:v0.8:client-request-record`; `urn:chirality:del-01-01:hosting-boundary:v0.8:lifecycle-event`; `urn:chirality:del-01-01:hosting-boundary:v0.9:server-request-entry` |
| DEL-01-02 | RECOVERY | `EXECUTION_AND_RECOVERY.md` | `recovery.app-ledger-entry.schema.json`; `recovery.custody-event.schema.json`; `recovery.stop-request.schema.json`; `urn:chirality:app-v4:del-01-02:app-ledger-entry:0.2`; `urn:chirality:app-v4:del-01-02:custody-event:0.2`; `urn:chirality:app-v4:del-01-02:stop-request:0.2` |
| DEL-01-03 | NPT, NPTD | `NATIVE_PLANS_TOOLS_DELEGATION.md` | `npt.delegation-export.schema.json`; `npt.item-anchor.schema.json`; `npt.plan-revision.schema.json`; `chirality:app-v4:DEL-01-03:npt.delegation-export:v0.2`; `chirality:app-v4:DEL-01-03:npt.item-anchor:v0.2`; `chirality:app-v4:DEL-01-03:npt.plan-revision:v0.1` |
| DEL-01-04 | AAC, NIR | `APP_ACT_CONTROL.md`, `NATIVE_INTERACTION_RECEIVING.md` | `aac.capture-evidence.schema.json`; `aac.offer.schema.json`; `nir.answer-submission.schema.json`; `nir.attachment-supply-record.schema.json`; `nir.draft-transition.schema.json`; `urn:chirality:app-v4:del-01-04:aac:capture-evidence:0.3`; `urn:chirality:app-v4:del-01-04:aac:offer:0.3`; `urn:chirality:app-v4:del-01-04:nir:answer-submission:0.1`; `urn:chirality:app-v4:del-01-04:nir:attachment-supply-record:0.2`; `urn:chirality:app-v4:del-01-04:nir:draft-transition:0.2` |
| DEL-01-05 | ACCESS, ACCOUNT-HOME-RECORD | `ACCOUNT_AND_PROVIDER_ACCESS.md`, `ACCOUNT_HOME_DECISION_RECORD.md` | `access.capability-handoff.schema.json`; `access.conversation-selection.schema.json`; `access.network-observation.schema.json`; `access.state.schema.json`; `chirality:app-v4:DEL-01-05:access.capability-handoff:v0.2`; `chirality:app-v4:DEL-01-05:access.conversation-selection:v0.2`; `chirality:app-v4:DEL-01-05:access.network-observation:v0.2`; `chirality:app-v4:DEL-01-05:access.state:v0.2` |
| DEL-01-06 | PKG | `PACKAGING_AND_DISTRIBUTION.md` | `pkg.identity-record.schema.json`; `pkg.terms-record.schema.json`; `urn:chirality:app-v4:del-01-06:distribution-terms-record:0.2`; `urn:chirality:app-v4:del-01-06:package-identity-record:0.2` |
| DEL-02-01 | WD, WD-EX | `EXAMPLES.md`, `WORKFLOW_DECLARATION.md` | `workflow-declaration.schema.json`; `urn:chirality:app-v4:del-02-01:workflow-declaration:WD-v0.8` |
| DEL-02-02 | WR | `WORKSPACE_AND_REGISTRATION.md` | `workspace-registration.schema.json`; `urn:chirality:app-v4:del-02-02:workspace-registration:WR-v0.2` |
| DEL-02-03 | EXEC | `EXECUTION_COMPATIBILITY.md` | `checkpoint-record-entries.schema.json`; `compatibility-report.schema.json`; `chirality:del-02-03/exec-checkpoint-entry-bodies/proposed-0.7`; `chirality:del-02-03/exec-compatibility-report/proposed-0.6` |
| DEL-02-04 | ROLE | `ROLE_SUPPLY.md` | `role-limit-account.schema.json`; `role-supply-record.schema.json`; `urn:chirality:app-v4:del-02-04:role-limit-account:0.2`; `urn:chirality:app-v4:del-02-04:role-supply-record:0.2` |
| DEL-03-01 | C | `CATALOG_AND_READ_BASIS.md` | `catalog.schema.json`; `edition_change_event.schema.json`; `read_result.schema.json`; `urn:chirality:app-v4:proposed:catalog`; `urn:chirality:app-v4:proposed:edition-change-event`; `urn:chirality:app-v4:proposed:read-result` |
| DEL-03-02 | P | `PROPOSAL_LIFECYCLE_AND_OUTCOMES.md` | `proposal.schema.json`; `proposal_state.schema.json`; `urn:chirality:app-v4:proposed:proposal`; `urn:chirality:app-v4:proposed:proposal-state` |
| DEL-03-03 | ADAPTER | `ADAPTER_ENABLEMENT_AND_RECEIVING.md` | `channel_status.schema.json`; `checkpoint_observation.schema.json`; `external_dispatch_record.schema.json`; `urn:chirality:app-v4:proposed:channel-status`; `urn:chirality:app-v4:proposed:checkpoint-observation`; `urn:chirality:app-v4:proposed:external-dispatch-record` |
| DEL-03-04 | GUIDE | `HOST_INTEGRATION_GUIDE.md` |  |
| DEL-04-01 | ACT, ACT-POLICY | `ACT_AND_POLICY_CONTRACT.md` | `ACT_POLICY_CLASS_RECORD.schema.json`; `urn:chirality:app-v4:del-04-01:policy-class-record:0.1` |
| DEL-04-02 | AS | `AUTONOMY_AND_STANDING_EXCHANGE.md` | `AS_SETTINGS_IN.schema.json`; `urn:chirality:app-v4:del-04-02:settings-in:0.1` |
| DEL-04-03 | RS | `RECORD_SEMANTICS.md` | `RS_RECORD.schema.json`; `urn:chirality:app-v4:del-04-03:rs-record:0.1` |
| DEL-05-01 | LOOP | `LOOP_RECEIVING_CONTRACT.md` | `LOOP_DESTINATION_REQUEST.schema.json`; `LOOP_TOOL_CALL.schema.json`; `chirality:app-v4/DEL-05-01/LOOP_TOOL_CALL/0.1`; `urn:chirality:app-v4:del-05-01:destination-request:0.1` |
| DEL-05-02 | PANEL | `PANEL_RECEIVING_CONTRACT.md` | `PANEL_RETURN_INPUT.schema.json`; `chirality:app-v4/DEL-05-02/PANEL_RETURN_INPUT/0.1` |
| DEL-06-01 | FR | `FLEET_RECORDS.md` | `fleet.record.schema.json`; `urn:chirality:app-v4:del-06-01:fleet-record:0.1` |
| DEL-06-02 | DV, FV | `DECISION_VIEW.md`, `FLEET_VIEWS.md` |  |
| DEL-07-01 | PRC | `PEC_RECEIVING.md` | `pec.receiving-record.schema.json`; `urn:chirality:app-v4:del-07-01:pec-receiving-record:0.1` |
| DEL-07-02 | CFB | `CONNECTOR_FALLBACK.md` | `connector.route-account.schema.json`; `connector.standing.schema.json`; `urn:chirality:app-v4:del-07-02:connector-standing:0.1`; `urn:chirality:app-v4:del-07-02:route-account:0.1` |
| DEL-08-01 | DRC | `DOMAINS_RECEIVING.md` | `domains.receiving-record.schema.json`; `urn:chirality:app-v4:del-08-01:domains-receiving-record:0.1` |
| DEL-08-02 | RTD | `RESEARCH_TO_DESIGN.md` | `research.context-account.schema.json`; `urn:chirality:app-v4:del-08-02:research-context-account:0.1` |
| DEL-09-01 | EXP | `EXAMINATION_PROTOCOL.md` | `exam.change-impact.schema.json`; `exam.result-record.schema.json`; `exam.review-record.schema.json`; `urn:chirality:app-v4:del-09-01:exam-change-impact:0.2`; `urn:chirality:app-v4:del-09-01:exam-result-record:0.2`; `urn:chirality:app-v4:del-09-01:exam-review-record:0.2` |
| DEL-09-02 | SQ | `STANDALONE_QUALIFICATION.md` | `sq.dossier.schema.json`; `urn:chirality:app-v4:del-09-02:standalone-dossier:0.2` |
| DEL-09-05 | DAC | `DECISION_ATTRIBUTION_CASE.md` |  |
| DEL-09-06 | CA, RELAY | `CONNECTED_ACTIVITY_CONTRACT.md`, `FACTS_SQ01_SQ32.md`, `RELAY_ANSWERS_SWBPIPE.md`, `RELAY_QUESTIONS_SWBPIPE.md` | `w14-result-record.schema.json`; `urn:chirality:app-v4:proposed:w14-result-record` |
| DEL-09-07 | CIR, DOS, LHQ, TOP | `LOCAL_HOST_QUALIFICATION.md`, `QUALIFICATION_DOSSIER.md`, `TRAFFIC_OBSERVATION_PLAN.md` | `lhq.candidate-identification.schema.json`; `lhq.dossier-manifest.schema.json`; `lhq.traffic-observation.schema.json`; `urn:chirality:app-v4:del-09-07:candidate-identification:0.1`; `urn:chirality:app-v4:del-09-07:dossier-manifest:0.1`; `urn:chirality:app-v4:del-09-07:traffic-observation:0.1` |
| DEL-09-09 | XT | `EXTERNAL_TRACE_CASES.md` | `xt-result-record.schema.json`; `xt-work-account.schema.json`; `urn:chirality:app-v4:proposed:xt-result-record`; `urn:chirality:app-v4:proposed:xt-work-account` |
| DEL-09-10 | CW | `CONNECTOR_WITNESS.md` |  |
| DEL-09-11 | RRM | `READER_METHOD.md` | `rrm.input-set-manifest.schema.json`; `rrm.reconstruction-account.schema.json`; `urn:chirality:app-v4:del-09-11:input-set-manifest:0.1`; `urn:chirality:app-v4:del-09-11:reconstruction-account:0.1` |
| DEL-09-12 | PV | `PRACTITIONER_VALIDATION.md` | `pv.practitioner-validation.schema.json`; `urn:chirality:app-v4:del-09-12:practitioner-validation:0.3` |
| DEL-10-01 | EB | `EXECUTION_BASIS.md` |  |
| DEL-10-02 | UC | `UNDERTAKING_CONTROLS.md` |  |
| DEL-10-03 | RA | `RESPONSIBILITY_ACCOUNT.md` |  |
| DEL-10-04 | DA | `DAG_ACCOUNT.md` |  |
| DEL-11-01 | — | `CONTINUITY_ACCOUNT.md` | `ca.continuity-account.schema.json`; `urn:chirality:app-v4:del-11-01:continuity-account:0.2` |
| DEL-11-02 | AA | `ADOPTION_ACCOUNT.md` | `aa.adoption-account.schema.json`; `urn:chirality:app-v4:del-11-02:adoption-account:0.2` |
| DEL-11-03 | RP | `REPLACEMENT_PACKET.md` | `rp.disposition.schema.json`; `rp.packet-manifest.schema.json`; `urn:chirality:app-v4:del-11-03:rp-disposition:0.1`; `urn:chirality:app-v4:del-11-03:rp-packet-manifest:0.5` |


## 3. Totals

| Class | Pairs | Of which SCC-forming under at least one option |
|---|---:|---:|
| Dependency carried by a DAG-004 arc (matched) | 212 (211 with consumer uses; DEP-01-03-021's arc 09-05→01-03 is stated only by NPTD §10.2) | — |
| **Dependency not carried by an arc** | **62** | **23** |
| — already one of G2's 30 | 24 (N01, N03…N25) | 3 (N08, N13, N22) |
| — a G2 §5 ambiguous item | 9 (A2, A3 ×5, A6, A7, A8) | 7 (A2, A3 ×5, A7) |
| — **new** (in neither G2 list) | **29** | **13** |
| **Unclear** | **13** (including N27 and A1) | 11 |
| **Not a dependency** | **251** | — |

**Not-a-dependency reasons.**

| Reason | Pairs |
|---|---:|
| Receiver list (the use runs the other way) | 116 |
| Attribution or owner map | 37 |
| Cross-reference, comparison or proposal to another owner | 30 |
| Pin or sibling-label list only | 22 |
| Runtime value stated by the Design | 17 |
| Ruling- or basis-carried | 10 |
| Explicit "not a contribution" or "no reliance" in the Design | 8 |
| Example | 7 |
| Other | 4 |

**Reconciliation with G2.**
- **Of G2's 30:**
  - 24 are confirmed as dependencies.
  - **N02** (DEL-01-01 → DEL-04-01) is not: the content V-21/V-25 is carried by D3 and R2-8, which HOSTING cites directly.
  - **N26** (DEL-01-01 → DEL-02-03) is not: HOSTING's own text holds the observations, and the join is discharged.
  - **N27** is unclear.
  - **K1–K3** are not consumer uses. Only DEL-01-06's PKG §4.2/§13 states them, and WR, ROLE and AAC use no PKG content. The reverse uses (01-06 → 01-04, 02-02, 02-04) appear in §4.1 and §4.2.
- **Of G2 §5:**
  - A2, A3, A6, A7 and A8 are dependencies.
  - A1 is unclear.
  - A4 and A9 have no use in the consumer's Design (RS never names NPTD; EB names DEL-10-04 only as a receiver).
  - A5 is not a dependency.

## 4. Classification of the 326 candidate pairs

Each pair is counted once. "Uses" counts every line naming the supplier, including pins and history.

### 4.1 Dependencies not carried by a DAG-004 arc (62)

| # | Consumer → supplier | Uses | Kind | Status | Deciding citation and sentence | dag_reach | SCC effect by option (own script) |
|---|---|---:|---|---|---|---|---|
| D01 | 01-03 → 04-03 | 10 | I | **new** | NPTD §9 TA-4 l.477–480: "TA-4 Faithful display. An act record handed in … is shown "<act kind> by <person> (identity not verified) · recorded by <recorder>" with content, scope and purpose (K1-4; RS §6.1); a record naming the recorder as actor is not shown as an act (RS HA-2)" (K-2: record element meanings and a record rule used in the consumer's display rule) | **SCC-FORMING** | O-1: GROW 14 (+01-03) from 13; O-2…O-4: GROW 13 (+01-03) from 12 |
| D02 | 01-04 → 02-01 | 5 | I | **new** | AAC §2 AI-2 l.116; NIR §7 l.628: "The control maps WR's snake_case to its own spelling one to one (WD §3.6; prototype `from_wr_descriptor`)"; NIR: "`content` \| The draft's content identity with method (WD §6.1 RV-1…RV-5; algorithm open, WD U-03)" (K-2: identity scheme and spelling rule used in the consumer's own definitions) | **SCC-FORMING** | O-1…O-4: inside |
| D03 | 01-05 → 04-03 | 16 | I | G2 N08 | ACCESS header l.63; §8 l.601: "DEL-04-03/RS-v0.8 R5 and its schema enum `destinationClass` were read for the class values (§3)"; "as last read, in RS's `codexAccount` form" (= G2 N08) (K-2: vocabulary (RS R5 destination classes; RS `codexAccount` form)) | **SCC-FORMING** | O-1: MERGE 19 (+01-02,01-03) from 2+2+13; O-2…O-4: GROW 13 (+01-05) from 12 |
| D04 | 01-06 → 01-04 | 7 | L | **new** | PKG §3 SIGN-3 l.217; §12 U-PKG-8 l.522: "**One possible need is named:** SEAL-2's key store (AAC §6.3) may need a keychain-access-group or application-identifier entitlement and a provisioning profile (G-8 …); it is confirmed at FP-2 once SEAL-2 is implemented and, if needed, recorded in the OUT-001 configuration" (K-2, conditional (L by K-6: "once SEAL-2 is implemented"): the consumer's entitlement configuration depends on AAC's key store) | **SCC-FORMING** | O-1: MERGE 15 from 13+2; O-2: no cycle; O-3…O-4: out (kind L) |
| D05 | 02-01 → 01-04 | 23 | V | G2 N22 | WD §13 l.1792; EXAMPLES E1e l.972; §12 U-25: "App capture AWAITING INPUT (the act control, DEL-01-04: AAC-v0.2 §4.1, designed, not built)" (K-5 (V): App-side positive capture cases need the act control (= G2 N22)) | **SCC-FORMING** | O-1: inside; O-2…O-4: out (kind V) |
| D06 | 02-02 → 01-01 | 19 | I | G2 N01 | WR §7 l.365; §1 l.68: "DEL-01-01 supplier boundary \| none direct \| … v0.2: the supplier facts §16 rests on at Codex 0.158.0 (OBS-3 W-1…W-6; the generated `TurnStartParams`, `Turn`, `ThreadItem`, `UserInput`)" (K-2: supplier facts and generated types the run-start composition rests on (= G2 N01)) | no cycle | O-1…O-4: no cycle |
| D07 | 02-03 → 09-06 | 23 | V | **new** | EXEC §7.3 RT-11 l.1946: "RT-11 Evidence account for DEL-09-06 \| All MT/CH/RT cases, joined by CA W14 cases: W14-01 ← RT-1; … following CA-v0.6 §8.2 (R10-11: the consumer's list governs; V18-4 m-1)" (K-5 (V): the consumer's evidence account follows the receiver's case list ("the consumer's list governs")) | **SCC-FORMING** | O-1: GROW 14 (+09-06) from 13; O-2…O-4: out (kind V) |
| D08 | 03-01 → 02-01 | 23 | P | **new** | C §10.4 V-GR1 l.1140: "V-GR1 Grant checkpoint arrives before T15 (R5-7) \| T14 (r15), replacing T15–T16 in a separate run 13 of WD-EX E1d — workflow {…, `label-with-grant`, ⟨rev-D1⟩}, carried unadapted, declaring `CP-grant` (A12; reached-when kind (a) …)" (K-4: the consumer's shared fixture incorporates the supplier's example workflow) | **SCC-FORMING** | O-1…O-4: inside |
| D09 | 03-03 → 05-01 | 17 | I | **new** | ADAPTER §5.1 l.662: "Mirrors LOOP §6.2 for the external channel. Every dispatch carries, or the record states it lacks, each element" (K-2: the consumer's dispatch record is defined as a mirror of the supplier's) | **SCC-FORMING** | O-1…O-4: inside |
| D10 | 03-04 → 01-02 | 24 | I | G2 N03 | GUIDE §2.11 l.549; §2.4 l.442: "RECOVERY-v0.2 §8.2 (the App's custody events `observation_lost`, with its in-flight items, and `app_…`)" in Row 4; §2.11 "this guide cites them where a matrix line meets them (M4.6, M5.1, …)" (K-4/K-2: supporting contribution integrated into the consumer's matrix (= G2 N03)) | no cycle | O-1…O-4: no cycle |
| D11 | 03-04 → 01-03 | 16 | I | G2 N04 | GUIDE §2.8 l.489; §2.9 l.510: "… otherwise present (NPTD-v0.2 §7.1) \| defined draft; answered" (K-2 (= G2 N04)) | no cycle | O-1…O-4: no cycle |
| D12 | 03-04 → 01-04 | 35 | I | G2 N05 | GUIDE §2.5 l.451: "App act control for App content and for A15 (designed by DEL-01-04 in AAC-v0.2 …)" (K-2 (= G2 N05)) | no cycle | O-1…O-4: no cycle |
| D13 | 03-04 → 01-05 | 24 | I | G2 N06 | GUIDE §2.7 l.474: "a host could use it only through a Responses interface behind the same boundary (LOOP §4, §13; ACCESS-v0.2 §11 CH-8, §20; R19-4)" (K-2 (= G2 N06)) | no cycle | O-1…O-4: no cycle |
| D14 | 03-04 → 02-02 | 37 | I | G2 N07 | GUIDE §2.5 l.454: "the workflow per run as run-start text with its supply check, WR-v0.2 §16.2, §16.6; R19-1, R19-7" (K-2 (= G2 N07)) | no cycle | O-1…O-4: no cycle |
| D15 | 04-01 → 01-04 | 32 | I | new (G2 §5 A2) | ACT §2.6 l.522; §2.1 l.342: "A4, A6, A7 on App content \| The App interface's act control (EXEC CAP-1…CAP-3), designed in DEL-01-04/AAC-v0.2 (§1.2, §4.1 …)" (K-2: capturing-surface design the consumer's capture rules rely on (RVG-ACT51 ACT-M1)) | **SCC-FORMING** | O-1: GROW 16 (+01-02,01-03,04-01) from 13; O-2…O-4: GROW 15 (+01-02,01-03,04-01) from 12 |
| D16 | 04-01 → 02-01 | 54 | I | new (G2 §5 A3) | ACT §5.1 l.1220: "*checkpoint state* \| Whether a declared checkpoint applies, the act it requires, and any governing checkpoint constraint \| DEL-02-01; DEL-02-03; DEL-05-01; P §3.3" (K-2: checkpoint state; WD §4.3.7 item rule adopted by citation (RVG-ACT51 §2)) | **SCC-FORMING** | O-1: GROW 16 (+01-02,01-03,04-01) from 13; O-2…O-4: GROW 15 (+01-02,01-03,04-01) from 12 |
| D17 | 04-01 → 02-02 | 25 | I | **new** | ACT §2.1 l.342; §2.5 l.451: "Capture evidence from DEL-01-04's App act control (AAC-v0.2 §4.2 …), composed from DEL-02-02's A15 descriptor (WR-v0.2 §4.3 RB-4), bound to the exact reviewed bytes"; RVG: A15's bound content is "WR ID-2" (K-2: identity scheme of the A15 subject (RVG-ACT51 ACT-M1)) | **SCC-FORMING** | O-1: GROW 16 (+01-02,01-03,04-01) from 13; O-2…O-4: GROW 15 (+01-02,01-03,04-01) from 12 |
| D18 | 04-01 → 02-03 | 99 | I | new (G2 §5 A3) | ACT §2.1 l.343; §4.6 l.1054: "The package file's shape is DEL-02-03 `$defs/decisionPackageFile` (R23-24)"; "support** (EXEC §3.6). Each takes exactly one of four values (R5-1)" (K-2: package-file shape; hold-support values (L, governance phase); checkpoint state) | **SCC-FORMING** | O-1: GROW 16 (+01-02,01-03,04-01) from 13; O-2…O-4: GROW 15 (+01-02,01-03,04-01) from 12 |
| D19 | 04-01 → 03-01 | 46 | I | new (G2 §5 A3) | ACT §2.5 l.447; §6 l.1358: "A4, A6, A7 on host content \| **Subject content identity** (DEL-03-01 §5.3), per object or row"; "Runtime non-success outcomes use DEL-03-01 §4.1" (K-2: subject content identity; non-success outcomes) | **SCC-FORMING** | O-1: GROW 16 (+01-02,01-03,04-01) from 13; O-2…O-4: GROW 15 (+01-02,01-03,04-01) from 12 |
| D20 | 04-01 → 03-02 | 25 | I | **new** | ACT §2.5 l.446; §6 l.1359: "A5, A10 \| **Change-item content identity** (DEL-03-02): operation identity and version, bound targets, old/new values, relied-on basis"; "outcomes use DEL-03-02 P §9 (R-7)" (K-2: change-item content identity; P §9 outcomes (R-7 only directs)) | **SCC-FORMING** | O-1: GROW 16 (+01-02,01-03,04-01) from 13; O-2…O-4: GROW 15 (+01-02,01-03,04-01) from 12 |
| D21 | 04-01 → 04-02 | 24 | I | new (G2 §5 A3) | ACT §5.1 l.1218: "*grant state* for the class \| … Each state carries a **grant value** (direct/propose) and a scope. \| DEL-04-02 (R-8; R2-6)" (K-2: grant states (= G2 A3; RVG-ACT51: grant state is I)) | **SCC-FORMING** | O-1: GROW 16 (+01-02,01-03,04-01) from 13; O-2…O-4: GROW 15 (+01-02,01-03,04-01) from 12 |
| D22 | 04-01 → 04-03 | 62 | I | **new** | ACT §2.5 l.448; §2.4: "A4, A6, A7 on App files \| File content identity (DEL-04-03)"; "The lapse-state vocabulary is DEL-04-03's" (l.514) (K-2: file content identity; lapse-state vocabulary (RVG-ACT51 ACT-M1)) | **SCC-FORMING** | O-1: GROW 16 (+01-02,01-03,04-01) from 13; O-2…O-4: GROW 15 (+01-02,01-03,04-01) from 12 |
| D23 | 04-01 → 05-01 | 43 | I | new (G2 §5 A3) | ACT §2.7 l.580, l.587: "The A8 is a call to the host's **destination request entry** (C-v0.8 §3.4; LOOP §5.3 DF-1) …"; "the request ends *not granted* ("not grantable") … (LOOP §5.3 DF-3 A-3, DF-6)" (K-2: destination-request sequences; checkpoint state) | **SCC-FORMING** | O-1: GROW 16 (+01-02,01-03,04-01) from 13; O-2…O-4: GROW 15 (+01-02,01-03,04-01) from 12 |
| D24 | 04-02 → 02-01 | 10 | I | **new** | AS §4 OV-7 l.398; §4 l.468: "OV-7 `governed` and invalid declarations \| A checkpoint declared **`governed`** (WD-v0.8 §4.3.1; PROPOSED) shows the flag and is otherwise treated as guidance (EXEC PH-9)"; "Mixed items at an A5 checkpoint (WD §4.3.7 confirmed by EXEC §4.11)" (K-2: declaration flags and item rule displayed by the consumer's overlay rules) | **SCC-FORMING** | O-1…O-4: inside |
| D25 | 06-01 → 02-04 | 8 | I | **new** | FR §3.1 l.140–142: "It is never handed from ROLE's limit account or NPTD's export, which use only `stated-not-enforced`, `enforced-by-supplier` and `unknown`. A delegating role's limit stays within `stated-not-enforced` or `unknown` (ROLE LA-5)" (K-2: the consumer's rule ranges over the supplier's standing values (FR §7 calls the value runtime)) | no cycle | O-1…O-4: no cycle |
| D26 | 06-01 → 07-02 | 5 | I | G2 N17 | FR §6 RF-5a l.252: "The reader validates the record's standing against DEL-07-02's `connector.standing.schema.json`, using the vendored copy" (K-2: standing schema (= G2 N17)) | no cycle | O-1…O-4: no cycle |
| D27 | 06-02 → 02-03 | 5 | I | G2 N09 | DV §2 l.55; §7 l.140: "RS `act_request` entries carrying `alternatives` (packages) \| DEL-04-03 format; body DEL-02-03 CE-4" (K-2: package body schema (= G2 N09)) | no cycle | O-1…O-4: no cycle |
| D28 | 07-01 → 01-01 | 11 | I | G2 N10 | PRC §7 l.147–148; §10 l.269: "App-origin `mcpServer/tool/call` … Recorded with initiator App and never presented as the agent's call (HOSTING §6.8)"; "HOSTING §6.8 receiver row for App-origin reads (§7) \| DEL-01-01's owner" (K-2: supplier surfaces of the route of consumption (= G2 N10)) | no cycle | O-1…O-4: no cycle |
| D29 | 08-02 → 04-01 | 8 | I | G2 N20 | RTD §4 l.119–125; §9 l.196: "Silence, timeout, an agent's statement, tool success or a host receipt is not a decision \| ACT §2.3 …"; "Consumed \| PKG-04 (DEP-08-02-007) \| Distinct act identities (ACT, RS) \| not topological" (K-2: act rules used by the consumer's candidate-decision requirements (= G2 N20; deferred by R23-34 H-4)) | no cycle | O-1…O-4: no cycle |
| D30 | 08-02 → 04-03 | 10 | I | G2 N21 | RTD §4 l.120; §3 l.107: "the decision cannot be recorded as applying to it \| V4-HI-65; RS OF-3 …"; "as host-agent run records do (RS OF-9)" (K-2: record rules (= G2 N21; deferred)) | no cycle | O-1…O-4: no cycle |
| D31 | 08-02 → 07-02 | 3 | I | **new** | RTD header l.45: "It consumes EU-D1's frozen Domains receiving records and DEL-07-02's standing schema, read-only" (K-2: standing schema read by the consumer's check) | no cycle | O-1…O-4: no cycle |
| D32 | 09-05 → 01-04 | 6 | I | new (G2 §5 A6) | DAC header "Suppliers" l.11–19; §2 l.51: "This file relies on the A16 rows, so it pins those versions: … DEL-01-04/AAC-v0.3 … (§1.2 A16 row, AK-a…AK-f, §5.1 `aac-offer-digest/0.1`), with its schemas `aac.offer.schema.json` … and `aac.capture-evidence.schema.json`"; FW-04 expects "Capture evidence resolvable, and agreeing with the record \| RS record; AAC capture evidence" (§7 records "None" under R23-2) (K-2 (witness inputs; K-5 exception: the witness is DEL-09-05's output) (= G2 A6)) | no cycle | O-1…O-4: no cycle |
| D33 | 09-05 → 02-03 | 3 | I | G2 N11 | DAC header "Suppliers" l.17; §1 l.28: "DEL-02-03 `checkpoint-record-entries.schema.json` (the CE-4 request body and … the package file's own `$def`)" (K-2: CE-4 body and package `$def` (= G2 N11)) | no cycle | O-1…O-4: no cycle |
| D34 | 09-06 → 01-04 | 21 | I | G2 N12 | CA §5 l.613; §8.5 W14-05 l.811; UNRESOLVED l.1283: "W14-05 \| SQ-01; a person's act on invented material (DEP-09-06-024); DEL-01-04 for AF-1"; "DEL-01-04 owner for the control \| Before W14-01/W14-09" (K-2/K-4 for the witness (K-5 exception: OUT-003 is the witness) (= G2 N12)) | no cycle | O-1…O-4: no cycle |
| D35 | 09-06 → 01-05 | 1 | I | **new** | RELAY l.1141: "(LOOP-v0.9 §13 NR-L1; DEL-01-05/ACCESS-v0.2 §11 CH-8; R19-4; added in place …)" (K-2: a relay row derived from the supplier's content) | no cycle | O-1…O-4: no cycle |
| D36 | 09-06 → 03-04 | 32 | I | **new** | RELAY P8 l.816–819: "### P8 — the embedded loop's model and network side (addendum: DEL-03-04 GUIDE-v0.1 G-3, CC-5) These four questions cover host-loop evidence that the integration guide's receiving map needs and that v0.1 did not ask (GUIDE M2.4, M7.2, M7.3, M7.5; HC-2.4, HC-7.2…HC-7.4)" (K-2: the relay question set is derived from the guide's receiving-map needs (consumer-needs feedback)) | **SCC-FORMING** | O-1…O-4: NEW {03-04,09-06} |
| D37 | 09-07 → 02-01 | 4 | P | **new** | LHQ §2.1 l.58–59: "`WF` \| The reusable connected workflow the run carries out \| `supports-adjust` ⟨rev-3⟩ (C §10.1; DEL-02-01 WD-EX E1)"; "`label-with-grant` ⟨rev-D1⟩ (WD-EX E1d, with E1c's `CP-check`)" (K-4: fixture workflows (registered only as package row PKG-02, DEP-09-07-012)) | no cycle | O-1…O-4: no cycle |
| D38 | 09-07 → 02-03 | 5 | I | **new** | LHQ §6.2 LR-7 l.302: "LR-7 A current-phase record carries no hold claim (CA W-R4; EXEC PH-2)" (K-2: outcome rule (package row PKG-02)) | no cycle | O-1…O-4: no cycle |
| D39 | 09-07 → 03-01 | 15 | P | **new** | LHQ §2.1 l.44: "\| Slot \| Meaning \| Fixture binding (C §10.2, FX-PIPE-01) \| Used by \|" (K-4: fixture bindings (package row PKG-03, DEP-09-07-013)) | no cycle | O-1…O-4: no cycle |
| D40 | 09-07 → 03-02 | 9 | I | **new** | LHQ §5.1 l.165, l.170: "20-5 … Agent submits PR-1 \| **Refused — stale**, with relied B1, current B2 and reason"; "applied association (P §4.3)" (K-2: proposal outcomes as expectations (package row PKG-03)) | no cycle | O-1…O-4: no cycle |
| D41 | 09-07 → 04-01 | 6 | I | **new** | LHQ §5.3 l.219; §5.1 l.169: "**no** acceptance recorded (ACT §2.2: direct application is never A5)"; "Human-act records with capture-evidence references (RS §6; ACT §2.1 A5, A10)" (K-2: act rules as expectations (package row PKG-04, DEP-09-07-014)) | no cycle | O-1…O-4: no cycle |
| D42 | 09-07 → 04-02 | 12 | I | **new** | LHQ §3 l.86: "the grant value and scope in force at start, and its display state (AS §3), or the host's own fixed treatment … (AS §3 …)" (K-2: grant display states in the CIR (package row PKG-04)) | no cycle | O-1…O-4: no cycle |
| D43 | 09-07 → 04-03 | 23 | I | **new** | LHQ §5.1 l.160; DOS §1 l.22: "Read entry with basis (RS R7)"; "each with its RS §9 resolution status at write: *resolved*, *unresolvable* or *not supplied*" (K-2: record kinds and resolution status (package row PKG-04)) | no cycle | O-1…O-4: no cycle |
| D44 | 09-07 → 05-01 | 17 | I | **new** | LHQ §5.1 l.161; §5.4 l.234: "Dispatch record (LOOP §6.2)"; "LOOP §5.2's cases give the expectations" (K-2: dispatch record and loop cases as expectations (package row PKG-05, DEP-09-07-015)) | no cycle | O-1…O-4: no cycle |
| D45 | 09-07 → 05-02 | 5 | I | **new** | LHQ §5.1 l.158; §5.4 l.246: "Host run record; AS §3 display; PANEL §3.3"; "Every contact, the decline and any refusal shown apart (AS §3.2; PANEL ND-4)" (K-2: panel views as expectations (package row PKG-05)) | no cycle | O-1…O-4: no cycle |
| D46 | 09-07 → 09-11 | 28 | I | G2 N13 | DOS §5 l.118: "**Withheld items**, each with identity and kind, using DEL-09-11's input-set classes (`harness_session`, `host_agent_conversation`, `app_conversation`, `author_memory`, `derived_view`)" (K-2: the handoff uses the supplier's input-set classes (= G2 N13)) | **SCC-FORMING** | O-1…O-4: NEW {09-07,09-11} |
| D47 | 09-09 → 01-02 | 5 | I | G2 N14 | XT §3.2 XC-06 l.185: "App-restart custody defined by DEL-01-02: the relaunch sequence RECOVERY-v0.2 §5 SQ-R and the custody events of §8.2 (`observation_lost` with …)" (K-2: custody definitions in a trace case (= G2 N14)) | no cycle | O-1…O-4: no cycle |
| D48 | 09-09 → 02-01 | 11 | I | **new** | XT §0 l.46; header l.4: "outcomes P §9 / C §4.1; class values C §3.1; dispositions WD §4.3.4"; "for checkpoints declared **`governed`** (WD-v0.7 §4.3.1, PROPOSED)" (K-2: disposition vocabulary used by the trace) | **SCC-FORMING** | O-1: inside; O-2…O-4: no cycle |
| D49 | 09-09 → 09-06 | 28 | I | new (G2 §5 A7) | XT §2 l.86: "Standing uses the C evidence-label mapping and the DEL-09-06 contribution ladder (CA §7.2)"; §3.4 l.244 "The same elements carry the same meanings as DEL-09-06's W14 …" (K-2: standing ladder used by the input account (= G2 A7; both Designs call it a cross-reference)) | **SCC-FORMING** | O-1: GROW 14 (+09-06) from 13; O-2…O-4: no cycle |
| D50 | 09-10 → 09-07 | 1 | I | **new** | CW §5 l.88–90: "a PEC gap sheet … and a Domains gap sheet (contract, admitted sources, OI-023/OI-026), in DOS-v0.1's pattern" (K-2: the consumer's dossier follows the supplier's dossier pattern) | no cycle | O-1…O-4: no cycle |
| D51 | 09-11 → 01-04 | 3 | P | G2 N24 | RRM header "Suppliers" and "Fixture" l.19–21: "For the early path, the A16 rows (R23-18), adopted …: … AAC-v0.3 `APP_ACT_CONTROL.md` … (§5.1 names the offer digest's serialization, `aac-offer-digest/0.1` …)"; "It … **carries the digest rule** as a `definition` item: … a verbatim excerpt of AAC-v0.3 §5.1" (K-4 (early path): the offer-digest rule is carried into the reader's input set as a `definition` item (= G2 N24)) | no cycle | O-1…O-4: no cycle |
| D52 | 09-11 → 02-03 | 2 | I | G2 N15 | RRM header "Suppliers" l.17; §4 RD-5 l.65: "DEL-02-03 EXEC RP-6, inspection replay: "Rebuilds the same arrival identities and dispositions from the same record …""; "RD-5 \| Checks **lapse** … \| As RS §7; inspection time stated (EXEC RP-6)" (K-2: inspection-replay rule (= G2 N15)) | no cycle | O-1…O-4: no cycle |
| D53 | 09-11 → 04-01 | 2 | I | G2 N23 | RRM header "Suppliers" l.19: "ACT-POLICY-v0.11 … (R23-25: a later A16 supersedes for current standing; a correction is not a decision …)" (K-2 (early path): A16 rows and supersession rule (= G2 N23)) | no cycle | O-1…O-4: no cycle |
| D54 | 09-11 → 06-02 | 0 | P | G2 N25 | RRM header "Fixture" l.21; DV §7 l.145: "Fixture: FX-DP1 (O-A). The RR-E reader was given its first freeze …"; DV: "To DEL-09-05 and DEL-09-11: the fixture FX-DP1 and its manifest" (K-4 (early path): the FX-DP1 fixture (= G2 N25)) | no cycle | O-1…O-4: no cycle |
| D55 | 09-12 → 09-02 | 3 | P | G2 N18 | PV §2 I-2 l.62: "I-2 \| Identified candidates for each expression \| DEL-09-02 (App), DEL-09-07 and SWBPIPE (host); DEP-001 \| DEP-09-12-008, -009 \| Before use in that expression" (K-4: identified App candidate (= G2 N18; DEP-09-12-008 is UNKNOWN)) | no cycle | O-1…O-4: no cycle |
| D56 | 09-12 → 09-07 | 3 | I | G2 N19 | PV §2 I-2 l.62; §3.1 l.91: "`host_candidate` is EXP `candidate_subject.host_candidate`: the host build, or the DEL-09-07 LHQ candidate identification record that names it (I-2: DEL-09-07 and SWBPIPE supply it)" (K-4/K-2: identified host candidate and its CIR form (= G2 N19)) | no cycle | O-1…O-4: no cycle |
| D57 | 09-12 → 10-02 | 12 | I | **new** | PV §3.5 l.138: "**`method_note`** has exactly DEL-10-02 UC §5's fields, read from UC at the commit (K-11)" (K-2: the hand-over record has the receiver's field set (consumer-defined format)) | **SCC-FORMING** | O-1…O-2: GROW 3 (+09-12) from 2; O-3: NEW {09-12,10-02}; O-4: no cycle |
| D58 | 10-03 → 01-06 | 6 | I | new (G2 §5 A8) | RA §4.2 l.239; §2.2 l.108: "App v4 \| PKG-v0.2 P-2 `Contents/Resources/workflows/` (DEL-02-02), P-3 `Contents/Resources/instructions/` (DEL-02-04) \| PROPOSED; not built \| Before relying on a v4 package's supply: compare P-2/P-3's actual contents … (DEL-01-06's first-package checks)" (K-2: the consumer's packaging/tool-path account records the supplier's layout (= G2 A8)) | no cycle | O-1…O-4: no cycle |
| D59 | 11-02 → 01-01 | 2 | P | **new** | AA §5 l.127; §9 U-AA-4 l.198: "HOSTING-v0.9 §2/§8.2 (DEL-01-01) \| DEL-01-01 owner \| **pending next revision** \| Same check" (K-4: the promise trace is built from the supplier's passage) | no cycle | O-1…O-4: no cycle |
| D60 | 11-02 → 01-05 | 1 | P | **new** | AA §5 l.128: "ACCESS-v0.2 §9/U-A9 (DEL-01-05) \| DEL-01-05 owner \| **pending next revision** \| Same check" (K-4: the promise trace is built from the supplier's passage) | no cycle | O-1…O-4: no cycle |
| D61 | 11-03 → 02-03 | 2 | I | G2 N16 | RP §4.5 RP-R6 l.153: "The package validates against DEL-02-03's `$defs/decisionPackageFile`, and the rules there apply" (K-2: package-file schema (= G2 N16)) | no cycle | O-1…O-4: no cycle |
| D62 | 11-03 → 09-01 | 19 | I | **new** | RP §5 l.161; §4.1 l.121: "the subject maps to EXP's `candidate_subject`"; "what the dossier records …, in EXP's outcome vocabulary, worst first" (K-2: canonical candidate identity and outcome vocabulary (R23-33 only directs)) | no cycle | O-1…O-4: no cycle |

### 4.2 Unclear (13)

| # | Consumer → supplier | Uses | Kind if registered | Status | Citation and quote | dag_reach | SCC effect by option |
|---|---|---:|---|---|---|---|---|
| U01 | 01-01 → 01-04 | 60 | I | **new** | HOSTING §6.1 l.767; UNRESOLVED U-20 l.2172: "From v0.9 both co-owners have answered: DEL-01-04 states the answer path per kind (NIR-v0.2 §4.1 …) and the decline form per kind (NIR-v0.2 §4.3 DM-1…DM-6; this file's §6.2.1 RT-08)" | **SCC-FORMING** | O-1: MERGE 19 (+01-02,01-03) from 2+13+2; O-2…O-4: GROW 16 (+01-01,01-02,01-03,01-05) from 12 |
| U02 | 01-01 → 03-03 | 42 | I | G2 N27 | HOSTING §6.8 heading "(R4-12; ADAPTER F-3)"; ADAPTER §11 l.1446: ADAPTER: "Provide to \| DEL-01-01 (by join; no register row) \| Observed MCP/dynamic-tool facts (§3.5) for the classification R4-12 assigns to HOSTING" (= G2 N27, a design-time join) | **SCC-FORMING** | O-1: MERGE 19 (+01-02,01-03) from 2+13+2; O-2…O-4: GROW 16 (+01-01,01-02,01-03,01-05) from 12 |
| U03 | 01-03 → 02-03 | 9 | I | **new** | NPTD §5.7 l.275; §10.1 l.495: runtime value by design ("run markers (DEL-02-03, R19-2)", "no register row; R17-10"), but §5.7 displays EXEC's run-marker fields "(thread, turn, start or end, workflow, revision)" defined by EXEC SD-6/RE-7 | **SCC-FORMING** | O-1: GROW 14 (+01-03) from 13; O-2…O-4: GROW 13 (+01-03) from 12 |
| U04 | 01-04 → 03-01 | 1 | I | **new** | AAC §5.1 l.271: "Until a canonicalization is selected for the project (DEL-03-01 TBD-003; RS U-04), this is the AAC's own TEST VALUE method" (a pending use at the selection point) | **SCC-FORMING** | O-1…O-4: inside |
| U05 | 01-06 → 02-02 | 5 | I | **new** | PKG §4.1 P-2 l.240; §4.2 I-3 l.263: "P-2 `Contents/Resources/workflows/` \| Bundled workflows and the shipped-revision manifest \| DEL-02-02 (WR §3; LS-5, LS-8; L-4)"; "a build-time input to a package candidate … not a production dependency of DEL-01-06 on DEL-02-02/02-04 (as R23-2 treats a decision package as a runtime value)". By K-4 the bytes are needed to produce a complete candidate; R23-2 frames the direction the other way (K1) | **SCC-FORMING** | O-1: MERGE 15 from 13+2; O-2…O-4: no cycle |
| U06 | 01-06 → 02-04 | 5 | I | **new** | PKG §4.1 P-3 l.241; §4.2 I-3 l.263: "P-3 `Contents/Resources/instructions/` \| Product guidance `AGENTS.md`, the four role files and the role set `roles.json` \| DEL-02-04 (ROLE §4.1, §4.2 GS-1)"; same framing as 01-06>02-02 (K2 is the other direction) | **SCC-FORMING** | O-1: MERGE 15 from 13+2; O-2…O-4: no cycle |
| U07 | 04-03 → 01-04 | 25 | I | new (G2 §5 A1) | RS §6.1 l.530; §6.2 HA-10 l.565: "For the App interface the capture evidence is DEL-01-04's object (`aac.capture-evidence.schema.json`, AAC-v0.2 §5.2), cited by its `cap:` identity and resolved through the act control's capture store (§9); RS copies none of it" (close to GC-3, without the GC-3 statement); HA-10 "Written only from capture evidence … at DEL-01-04's App act control (AAC-v0.2 §4.2; K-8)" | **SCC-FORMING** | O-1…O-4: inside |
| U08 | 04-03 → 09-06 | 9 | I | **new** | RS §4 R11 l.332: "**act offered without a capture-evidence reference**, written against the observation or operation entry, never as a human-act record (EXEC A-7; DEL-09-06 CAF-24; HA-1) — these seven adopted from their suppliers" (EXEC is a registered supplier; whether CA CAF-24 is a co-source is not stated) | **SCC-FORMING** | O-1: GROW 14 (+09-06) from 13; O-2…O-4: GROW 13 (+09-06) from 12 |
| U09 | 06-01 → 01-02 | 4 | I | **new** | FR §6 l.332; §7 l.345: "Observe a child \| Codex process stops, App quits or relaunches (RECOVERY DEF-5/6/7) \| `observation_ended` with the cause"; §7 calls it "Runtime value (no row)" | no cycle | O-1…O-4: no cycle |
| U10 | 08-02 → 09-01 | 1 | I | **new** | RTD §8 l.188: "A rehearsal of RD-2…RD-4 can reuse EU-D1's Domains cases … as `rehearsal` records (EXP-R3: they stand for no scenario)" (an optional rehearsal using EXP's record rule) | no cycle | O-1…O-4: no cycle |
| U11 | 09-01 → 09-06 | 5 | V | **new** | EXP header l.37; §3.5 EXP-R9 l.244: "Receivers' files read to check the interface (cross-references, not reliance): DEL-09-06 … `w14-result-record.schema.json`"; "EXP-R9 \| … the mapping to W14 and XT is one to one \| Prototype, reading the actual files" (a check of receivers; V if registered) | **SCC-FORMING** | O-1: MERGE 16 (+09-06) from 13+2; O-2…O-4: out (kind V) |
| U12 | 09-01 → 09-09 | 12 | V | **new** | EXP header l.42; §3.5 EXP-R9 l.244: as 09-01>09-06, for `xt-result-record.schema.json` | **SCC-FORMING** | O-1: MERGE 15 from 2+13; O-2…O-4: out (kind V) |
| U13 | 09-12 → 11-03 | 14 | I | **new** | PV §3.2 l.107; §2 l.70–74: "The placeholder test matches DEL-11-03's (RP-v0.5, unchanged in RP-v0.6), and like it is **keyword-based**"; O-3 "supersedes DEL-11-03's first-cut `$defs/practitioner_standing` … DEL-11-03 adopts it at its next revision" (the record is PV's; the test is aligned with RP's) | **SCC-FORMING** | O-1…O-2: GROW 3 (+09-12) from 2; O-3…O-4: NEW {09-12,11-03} |

### 4.3 Dependencies already carried by a DAG-004 arc (212)

Representative line: the first consumer-Design line naming the supplier, ranked by section (interfaces, inputs, suppliers, joins, receiving first) and then by a use verb. Layer and G1 r3 primary kind are the arc's.

| Consumer → supplier | Layer, kind | Uses | Representative citation (file, line, section: excerpt) |
|---|---|---:|---|
| 01-01 → 01-05 | held, V | 63 | HOSTING_BOUNDARY l.753 §6.1 Entry meaning (semantic elements): …by this boundary; the Codex account element is the account DEL-01-05 reports for the home that runs the conversation (the reported email, or "ChatGPT… |
| 01-02 → 01-01 | admitted, P | 141 | EXECUTION_AND_RECOVERY l.414 §4.1 Offered: …01-04 / Any state / Listed entries of the ready generation (HOSTING §6.4 list outstanding) and closed entries of earlier generations and sessions with… |
| 01-02 → 04-01 | admitted, I | 6 | EXECUTION_AND_RECOVERY l.436 §4.2 Consumed: …/ DEL-04-01 (ACT §10.1 V-21) / P-04 routine tool permission (D3): the person's own Codex set… |
| 01-03 → 01-01 | admitted, P | 69 | NATIVE_PLANS_TOOLS_DEL l.98 §2. Receiving comparison of seam S-2 (clo: …/ S-2 element (HOSTING §8) / How DEL-01-03 uses it / Standing /… |
| 01-03 → 01-02 | admitted, I | 16 | NATIVE_PLANS_TOOLS_DEL l.101 §2. Receiving comparison of seam S-2 (clo: …Accepted. Within a generation, re-attachment by position is DEL-01-02's; after a generation closes the views rebuild from Codex history (R18-1 C-03),… |
| 01-04 → 01-01 | admitted, P | 72 | NATIVE_INTERACTION_REC l.178 §1.1 Process placement (R17-5: PROPOSED; : …ave one authoritative source that survives a window reload (HOSTING H2, H3; V4-EXE-01) / Rust host: register and write path; the interface renders car… |
| 01-04 → 01-02 | admitted, I | 36 | NATIVE_INTERACTION_REC l.189 §2. Interfaces: …in SCC-002). R17-10: DEL-01-02 and DEL-01-03 consume nothing from this… |
| 01-04 → 01-03 | admitted, I | 18 | NATIVE_INTERACTION_REC l.189 §2. Interfaces: …in SCC-002). R17-10: DEL-01-02 and DEL-01-03 consume nothing from this… |
| 01-04 → 01-05 | admitted, I | 12 | NATIVE_INTERACTION_REC l.254 §4.1 Kinds at 0.158.0 and how each is met: …t/chatgptAuthTokens/refresh / known-app-unsupported unless DEL-01-05 adopts external-token login / None: an information line / As above, rule app-ru… |
| 01-04 → 02-02 | held, I | 61 | APP_ACT_CONTROL l.116 §2. Interfaces: …ling one to one (WD §3.6; prototype from_wr_descriptor) / DEL-02-02 → the control (DEP-01-04-009, held) / A15 offers are composed only from a curren… |
| 01-04 → 02-03 | held, I | 33 | APP_ACT_CONTROL l.117 §2. Interfaces: …nt, arrival ordinal} and run, the RS act_request record / DEL-02-03 (recorder) / DEL-04-03 (record-out) → the control (NR-2 proposed) / Only when th… |
| 01-04 → 02-04 | held, I | 7 | NATIVE_INTERACTION_REC l.529 §5.7 Runs in a conversation and the "Star: …. The shipped product guidance that tells the agent both is DEL-02-04's (ROLE-v0.2 §4.2 GS-7); the run-start text that repeats them for the run in for… |
| 01-04 → 04-01 | admitted, I | 25 | NATIVE_INTERACTION_REC l.201 §2. Interfaces: …from agent output (V-08), routine tool permission (V-21) / DEL-04-01 → DEL-01-04 / Every label this deliverable shows / A value not carried is shown… |
| 01-04 → 04-02 | held, I | 24 | NATIVE_INTERACTION_REC l.680 §8. Act presentation (REQ-005; AC-005; VE: …workflow revision" (A15), "tool permission" (A14) / ACT §9; AS DS-1 /… |
| 01-04 → 04-03 | held, I | 69 | APP_ACT_CONTROL l.117 §2. Interfaces: …d run, the RS act_request record / DEL-02-03 (recorder) / DEL-04-03 (record-out) → the control (NR-2 proposed) / Only when the person opens the cont… |
| 01-05 → 01-01 | held, P | 109 | ACCOUNT_AND_PROVIDER_A l.159 §1. Interfaces: …served-in-generated-types) / Codex → DEL-01-05, carried by DEL-01-01 S-4 / ready(g) of the home's child (HOSTING §4.1) / A request with no response… |
| 01-06 → 01-01 | admitted, P | 25 | PACKAGING_AND_DISTRIBU l.112 §2.1 The supplier's tree (observed): …/ 0.158.0 / Partly read (PIN_SPIKE §3; spike copy pruned) / — / 2DC432GLL2 / yes (bin/codex, zsh) / bin/codex… |
| 01-06 → 09-01 | held, I | 24 | PACKAGING_AND_DISTRIBU l.266 §4.2 Interfaces: …/ I-6 Package and identity record / Here → DEL-09-01, DEL-09-02 / DEP-09-01-016 (held, M2); DEP-09-02-014 (admitted) / Package + OUT-… |
| 02-01 → 01-01 | admitted, I | 61 | WORKFLOW_DECLARATION l.1571 §8. What each receiver receives from this: …d per §3.7; EV-3's presence rule for the §4.2.5 names reads HOSTING §8.4's availability signals through the group mapping of HC-7, with observed route… |
| 02-01 → 02-03 | held, I | 199 | EXAMPLES l.971 §E1e — A6 and A7 checkpoints, two further: …dex at the pin and its HCG-A03 availability signal is read (EXEC EV-3, EV-3a: the rule is active for file-change; WD §4.2.5 HC-4); otherwise *not es… |
| 02-01 → 03-01 | held, I | 85 | EXAMPLES l.797 §E1e — A6 and A7 checkpoints, two further: …d-from *none*. A local fixture (L-WDEX-39…L-WDEX-41 below): C §10… |
| 02-01 → 03-02 | held, I | 41 | WORKFLOW_DECLARATION l.1556 §8. What each receiver receives from this: …/ DEL-03-02 proposal (DEP-03-02-027) / §6.1 identity tuple, for proposal origin; §4.3.1 requ… |
| 02-01 → 04-01 | admitted, I | 27 | EXAMPLES l.979 §E1e — A6 and A7 checkpoints, two further: …operation. On SWBPIPE, A6 and A7 are not software acts (ACT §2.6, from… |
| 02-01 → 04-03 | held, I | 36 | WORKFLOW_DECLARATION l.610 §4.1 Expected inputs (SOW-042): …and its content identity are recorded when it is supplied (DEL-04-03). /… |
| 02-01 → 05-01 | held, I | 47 | WORKFLOW_DECLARATION l.1554 §8. What each receiver receives from this: …/ DEL-05-01 loop (DEP-05-01-016) / §4.3.0 (Phase 1: the host loop enforces no hold); §4.3.1… |
| 02-01 → 05-02 | held, I | 24 | WORKFLOW_DECLARATION l.1596 §8. What each receiver receives from this: …he labels are the Wave A versions (R9-5, R9-11) and the RS, PANEL, LOOP, P and HOSTING states come from direct reading / Used in /… |
| 02-02 → 01-02 | admitted, I | 7 | WORKSPACE_AND_REGISTRA l.349 §7. Interfaces: …nterface is **offered**; R17-10's cycle guard is respected (DEL-01-02 and DEL-01-03 consume nothing from here).… |
| 02-02 → 01-03 | admitted, I | 7 | WORKSPACE_AND_REGISTRA l.349 §7. Interfaces: …offered**; R17-10's cycle guard is respected (DEL-01-02 and DEL-01-03 consume nothing from here).… |
| 02-02 → 01-04 | held, I | 41 | WORKSPACE_AND_REGISTRA l.354 §7. Interfaces: …/ DEL-01-04 native requests, outcomes, attachments, draft view / DEP-02-02-013 (receive) and… |
| 02-02 → 02-01 | held, I | 39 | WORKSPACE_AND_REGISTRA l.356 §7. Interfaces: …/ DEL-02-01 portable contract / DEP-02-02-014 · held / Identity tuple ($defs/workflow_ident… |
| 02-02 → 02-03 | held, I | 47 | WORKSPACE_AND_REGISTRA l.357 §7. Interfaces: …/ DEL-02-03 execution, compatibility, round trip / DEP-02-02-015 (receive) and DEP-02-03-010… |
| 02-02 → 04-01 | admitted, I | 14 | WORKSPACE_AND_REGISTRA l.359 §7. Interfaces: …/ DEL-04-01 operation policy and human acts / DEP-02-02-016 · admitted / A15's act table ent… |
| 02-02 → 04-03 | held, I | 36 | WORKSPACE_AND_REGISTRA l.360 §7. Interfaces: …/ DEL-04-03 records / DEP-02-02-017 · held / The A15 human-act record (RS §6.1, HA-10) in th… |
| 02-03 → 01-01 | admitted, I | 82 | EXECUTION_COMPATIBILIT l.2015 §9.1 Expected from suppliers: …/ DEL-01-01 (HOSTING; DEP-02-03-023, arc N-23) / Supplied-guidance evidence (§8.2); observed… |
| 02-03 → 01-02 | admitted, I | 34 | EXECUTION_COMPATIBILIT l.1265 §4.4 Events consumed: …ded / Run owner (R2-5). App run: the person's explicit end (RECOVERY-v0.2 §2 DEF-4) or the run owner's (RE-6), nothing else (AE-7); host loop: LOOP-v0… |
| 02-03 → 01-04 | held, V | 50 | EXECUTION_COMPATIBILIT l.2017 §9.1 Expected from suppliers: …/ DEL-01-04 (design pass 3; DEP-02-03-027, arc X-1) / App act control (CAP-2) and person ide… |
| 02-03 → 02-01 | held, I | 199 | EXECUTION_COMPATIBILIT l.890 §3.2 Inputs consumed: …ility, purpose, stage); compatible roles; delegation need / WD §3.4, §4.2.1–§4.2.2, §4.7 / Consumed unchanged; restriction ≠ requirement (WD §4.2.3) /… |
| 02-03 → 02-02 | held, I | 59 | EXECUTION_COMPATIBILIT l.2018 §9.1 Expected from suppliers: …/ DEL-02-02 (design pass 3; DEP-02-03-010) / Listing, selection (the selection record), draf… |
| 02-03 → 03-01 | held, I | 42 | EXECUTION_COMPATIBILIT l.892 §3.2 Inputs consumed: …/ **Exposure** per surface (element 9) / C §3 #9 / Read directly at discovery; *unagreed* → not established /… |
| 02-03 → 03-02 | held, I | 23 | EXECUTION_COMPATIBILIT l.1255 §4.4 Events consumed: …ions of checkpoint arrivals and act records, SoW CLM-002, DEP-02-03-026, ADAPTER-v0.6 §7.7 CO-1, CO-6 and checkpoint_observation.schema.json; how an… |
| 02-03 → 03-03 | held, I | 61 | EXECUTION_COMPATIBILIT l.894 §3.2 Inputs consumed: …/ Channel state (external access; A13) / C §4.1; V4-HI-52; ADAPTER-v0.6 §3.2, §3.6 / Surface-level, never per requirement. The report's two values re… |
| 02-03 → 04-01 | admitted, I | 15 | EXECUTION_COMPATIBILIT l.2011 §9.1 Expected from suppliers: …/ DEL-04-01 (ACT; DEP-02-03-012) / A1–A15 (A15 register workflow revision, R12-5, never chec… |
| 02-03 → 04-02 | held, I | 22 | EXECUTION_COMPATIBILIT l.2012 §9.1 Expected from suppliers: …/ DEL-04-02 (AS; the supplier's row DEP-04-02-023 only, no row in this deliverable's registe… |
| 02-03 → 04-03 | held, I | 113 | EXECUTION_COMPATIBILIT l.1259 §4.4 Events consumed: …/ Act-lapsed event / Host / record reader (RS L-6); on X, ADAPTER CO-8 as input (subject, method, earlier and later identity, or subj… |
| 02-03 → 05-01 | held, E | 49 | EXECUTION_COMPATIBILIT l.1255 §4.4 Events consumed: …an App run observes an arrival is §2.5 AW-1…AW-12) / loop (LOOP §2.4.1); host outcome (P §9) / Creates an arrival /… |
| 02-04 → 01-01 | admitted, I | 50 | ROLE_SUPPLY l.531 §7.1 Consumed: …/ C-3 / DEL-01-01: completed collabAgentToolCall items and thread/read of children (**no thre… |
| 02-04 → 02-01 | held, I | 15 | ROLE_SUPPLY l.533 §7.1 Consumed: …/ C-5 / DEL-02-01: role meanings, compatible roles / DEP-02-04-011 (held) / — / — /… |
| 03-01 → 03-02 | held, V | 72 | CATALOG_AND_READ_BASIS l.648 §5.4 Citing the relied-on basis in a late: …d ⟨basis⟩, current ⟨basis⟩); failing targets not supplied" (P §5).… |
| 03-01 → 04-01 | admitted, I | 26 | CATALOG_AND_READ_BASIS l.9 §Capability catalog and read-basis contra: …G-003 HANDOFF open matters). By join, with no register row: DEL-04-01 (fixture re-pointing); every file citing the §10 shared fixture catalogue (R-9;… |
| 03-01 → 04-03 | held, I | 33 | CATALOG_AND_READ_BASIS l.9 §Capability catalog and read-basis contra: …DEL-04-02 — read-basis and standing facets (DEP-04-02-016); DEL-04-03 — subject content identities and method designations (DEP-04-03-023); DEL-05-01… |
| 03-01 → 09-09 | held, V | 24 | CATALOG_AND_READ_BASIS l.669 §5.4 Citing the relied-on basis in a late: …REQ-004. This is a risk for the joined witness (DEL-09-09), not an… |
| 03-02 → 02-01 | held, I | 27 | PROPOSAL_LIFECYCLE_AND l.1023 §13. Interfaces provided and expected: …/ Expect from / DEL-02-01 (DEP-03-02-027) / Workflow identity; checkpoint declarations (required act, subj… |
| 03-02 → 03-01 | held, I | 63 | PROPOSAL_LIFECYCLE_AND l.208 §3.2 Consumed catalog meaning (from DEL-0: …/ Arguments / C §3 #3 / Checked against the catalog input schema before host domain validation (DEL-05-0… |
| 03-02 → 04-01 | admitted, I | 6 | PROPOSAL_LIFECYCLE_AND l.1021 §13. Interfaces provided and expected: …/ Expect from / DEL-04-01 (DEP-03-02-017) / A1–A15 names (A15, R12-5, not checkpoint-requirable); class re… |
| 03-02 → 04-02 | held, I | 11 | PROPOSAL_LIFECYCLE_AND l.1022 §13. Interfaces provided and expected: …/ Expect from / DEL-04-02 (supplier row DEP-04-02-021; no UPSTREAM row in this register) / Grant display s… |
| 03-03 → 01-01 | admitted, I | 69 | ADAPTER_ENABLEMENT_AND l.32 §Adapter enablement and receiving: …nly as **observed supplier facts at pin 0.158.0**, with the DEL-01-01… |
| 03-03 → 01-02 | admitted, I | 25 | ADAPTER_ENABLEMENT_AND l.102 §1. Parties and the owner/act map (REQ-00: …nd requests across a stop, a supplier exit or a relaunch is DEL-01-02's (RECOVERY-v0.2 §2, §8.2) (v0.7, FD-01; these were "a later undertaking, D1" th… |
| 03-03 → 02-01 | held, L | 24 | ADAPTER_ENABLEMENT_AND l.82 §0. How to read this definition: …s confirmed by the owner at SCA-V4-001 OWNER_ITEMS O-25):** WD I-7 is plan guidance; the agent proposes as the plan expects, and the App carries no co… |
| 03-03 → 02-03 | held, I | 88 | ADAPTER_ENABLEMENT_AND l.84 §0. How to read this definition: …onal annotation "continued past ‹checkpoint› before ‹act›" (EXEC PH-2, PH-3, PH-7). D6 re-opens only when the governance phase is taken up. SWBPIPE an… |
| 03-03 → 03-01 | held, I | 73 | ADAPTER_ENABLEMENT_AND l.66 §0. How to read this definition: …deferred), never as commitments (DECISION-3). Fixture subjects come from FX-PIPE-01 (C-v0.8 §10); local… |
| 03-03 → 03-02 | held, I | 67 | ADAPTER_ENABLEMENT_AND l.77 §0. How to read this definition: …ccess results are C §4.1's; proposal/operation outcomes are P §9's; both adopted unchanged / R-7; C §4.1; P §9 /… |
| 03-03 → 04-01 | admitted, I | 45 | ADAPTER_ENABLEMENT_AND l.78 §0. How to read this definition: …**disabling** external access is also A13 / D2; R-1; R2-3; ACT §2.1 /… |
| 03-03 → 04-02 | held, I | 12 | ADAPTER_ENABLEMENT_AND l.99 §1. Parties and the owner/act map (REQ-00: …/ Grant display states and standing display / App DEL-04-02 / Consumed; supplies the external-channel facts it displays /… |
| 03-04 → 01-01 | admitted, I | 73 | HOST_INTEGRATION_GUIDE l.57 §Host boundary and integration guide: …: C, P, ADAPTER, ACT, AS, RS, WD, WD-EX, EXEC, LOOP, PANEL, HOSTING, CA, XT. Unchanged: SPIKE, RELAY, ANS, FACTS. Version labels unchanged (no version… |
| 03-04 → 02-01 | admitted, I | 74 | HOST_INTEGRATION_GUIDE l.660 §2.15 SWBPIPE receiving mappings (R8-3, R: …trict preflight refuses unknown fields (SQ-02 (a), SQ-31) / WD required-tool references cannot resolve against SWBPIPE; OUT-003's round trip cannot co… |
| 03-04 → 02-03 | admitted, I | 114 | HOST_INTEGRATION_GUIDE l.5 §Host boundary and integration guide: …an App run observes an arrival and a request is defined in EXEC-v0.7 §2.4–§2.5 (the current-phase recorder, RC-1…RC-10, and the App-run reached-when… |
| 03-04 → 02-04 | admitted, I | 33 | HOST_INTEGRATION_GUIDE l.884 §4.2 Receiving-map evidence obligations →: …pp; additive role guidance / M8.1–M8.7; §2.14 (role supply: ROLE-v0.2 at v0.6, G-1 closed) /… |
| 03-04 → 03-01 | admitted, I | 68 | HOST_INTEGRATION_GUIDE l.656 §2.15 SWBPIPE receiving mappings (R8-3, R: …not supplied* (RS R11). De-duplication first is unchanged / C §5.4; P §5; RS R11 / M3.4; HC-3.4 /… |
| 03-04 → 03-02 | admitted, I | 53 | HOST_INTEGRATION_GUIDE l.656 §2.15 SWBPIPE receiving mappings (R8-3, R: …eceives and shows the **host's stated staleness scope** (SWBPIPE: the whole model), never narrowed; failing targets *not supplied* (RS R11). De-duplic… |
| 03-04 → 03-03 | admitted, I | 79 | HOST_INTEGRATION_GUIDE l.657 §2.15 SWBPIPE receiving mappings (R8-3, R: …neages read *unknown (incomparable)* (R13-1; C §5.2 rule 1; ADAPTER RD-2). SWBPIPE main has no workspace identity or generation (SQ-07 (a)); whether i… |
| 03-04 → 04-01 | admitted, I | 81 | HOST_INTEGRATION_GUIDE l.659 §2.15 SWBPIPE receiving mappings (R8-3, R: …b (launch variable as A13 evidence) deferred to the owner / ACT §2.6; ADAPTER §3.2; RS R11 / M5.3; M9.1; M9.2; HC-9.1 /… |
| 03-04 → 04-02 | admitted, I | 30 | HOST_INTEGRATION_GUIDE l.660 §2.15 SWBPIPE receiving mappings (R8-3, R: …" (PROPOSED; may be deferred). OI-021 stays open / WD §4.2; AS §3; RS R11 / M1.1; M1.7; M6.2; M8.3 /… |
| 03-04 → 04-03 | admitted, I | 106 | HOST_INTEGRATION_GUIDE l.656 §2.15 SWBPIPE receiving mappings (R8-3, R: …ole model), never narrowed; failing targets *not supplied* (RS R11). De-duplication first is unchanged / C §5.4; P §5; RS R11 / M3.4; HC-3.4 /… |
| 03-04 → 05-01 | admitted, I | 99 | HOST_INTEGRATION_GUIDE l.57 §Host boundary and integration guide: …t the B8 pins: C, P, ADAPTER, ACT, AS, RS, WD, WD-EX, EXEC, LOOP, PANEL, HOSTING, CA, XT. Unchanged: SPIKE, RELAY, ANS, FACTS. Version labels unchange… |
| 03-04 → 05-02 | admitted, I | 50 | HOST_INTEGRATION_GUIDE l.57 §Host boundary and integration guide: …B8 pins: C, P, ADAPTER, ACT, AS, RS, WD, WD-EX, EXEC, LOOP, PANEL, HOSTING, CA, XT. Unchanged: SPIKE, RELAY, ANS, FACTS. Version labels unchanged (no… |
| 03-04 → 07-01 | admitted, I | 6 | HOST_INTEGRATION_GUIDE l.77 §Host boundary and integration guide: …EC, LOOP, PANEL, HOSTING, CA, RELAY, XT; unchanged — SPIKE. DEL-07-01, DEL-07-02, DEL-08-01 and DEL-08-02 are referenced by accepted SoW meaning only;… |
| 03-04 → 07-02 | admitted, I | 4 | HOST_INTEGRATION_GUIDE l.77 §Host boundary and integration guide: …ANEL, HOSTING, CA, RELAY, XT; unchanged — SPIKE. DEL-07-01, DEL-07-02, DEL-08-01 and DEL-08-02 are referenced by accepted SoW meaning only; they are o… |
| 03-04 → 08-01 | admitted, I | 6 | HOST_INTEGRATION_GUIDE l.77 §Host boundary and integration guide: …NG, CA, RELAY, XT; unchanged — SPIKE. DEL-07-01, DEL-07-02, DEL-08-01 and DEL-08-02 are referenced by accepted SoW meaning only; they are outside this… |
| 03-04 → 08-02 | admitted, I | 4 | HOST_INTEGRATION_GUIDE l.77 §Host boundary and integration guide: …XT; unchanged — SPIKE. DEL-07-01, DEL-07-02, DEL-08-01 and DEL-08-02 are referenced by accepted SoW meaning only; they are outside this undertaking (… |
| 03-04 → 09-06 | admitted, I | 92 | HOST_INTEGRATION_GUIDE l.57 §Host boundary and integration guide: …D-EX, EXEC, LOOP, PANEL, HOSTING, CA, XT. Unchanged: SPIKE, RELAY, ANS, FACTS. Version labels unchanged (no version bump at RQ). Script (B8's, unchang… |
| 03-04 → 09-09 | admitted, I | 35 | HOST_INTEGRATION_GUIDE l.57 §Host boundary and integration guide: …ER, ACT, AS, RS, WD, WD-EX, EXEC, LOOP, PANEL, HOSTING, CA, XT. Unchanged: SPIKE, RELAY, ANS, FACTS. Version labels unchanged (no version bump at RQ).… |
| 04-02 → 02-03 | held, I | 43 | AUTONOMY_AND_STANDING_ l.825 §12.1 Provided to receivers (AS 5; PROPOS: …/ DEL-02-03 (DEP-04-02-023) / The display meanings of EXEC's annotations (§4); for an A12 ch… |
| 04-02 → 03-01 | held, I | 17 | AUTONOMY_AND_STANDING_ l.147 §0. Reading this definition: …- Examples are **fixture subjects** from DEL-03-01/C-v0.4 §10 (FX-PIPE-01), carried in C-v0.8 §10.… |
| 04-02 → 03-02 | held, I | 12 | AUTONOMY_AND_STANDING_ l.791 §12. Receivers (from the registers; R9-6): …/ DEL-03-02 / DEP-04-02-021 / none / held (SCC-002) / Visible autonomy state / §3 (states, i… |
| 04-02 → 04-01 | admitted, I | 23 | AUTONOMY_AND_STANDING_ l.186 §2. Grant model received: …Received from DEL-04-01 §5 and §8; this deliverable renders and exchanges it.… |
| 04-02 → 04-03 | held, I | 61 | AUTONOMY_AND_STANDING_ l.824 §12.1 Provided to receivers (AS 5; PROPOS: …NIR-v0.2 §9 PD-1…PD-7) / DEL-01-04 renders from record-out (RS-v0.9 §8) and compares with it (§6, K-3); it decides placement and behaviour in the App,… |
| 04-02 → 05-01 | held, I | 35 | AUTONOMY_AND_STANDING_ l.789 §12. Receivers (from the registers; R9-6): …/ DEL-05-01 / DEP-04-02-019 / DEP-05-01-025 / held (SCC-002) / Visible autonomy state. DEP-0… |
| 04-03 → 01-01 | admitted, I | 21 | RECORD_SEMANTICS l.787 §10.1 Receivers and suppliers by register: …/ DEL-01-01 / DEP-04-03-027 / none / admitted / Observed supplier facts: supplied guidance,… |
| 04-03 → 01-02 | admitted, I | 20 | RECORD_SEMANTICS l.748 §10. Consumer and host interface: …/ DEL-01-02 (RECOVERY-v0.2; v0.9) / — (R17-10: DEL-01-02 consumes nothing of DEL-04-03 and w… |
| 04-03 → 02-01 | held, I | 20 | RECORD_SEMANTICS l.211 §1. Settled distinctions relied on: …(EXEC-v0.6 §2.1; WD-v0.8 §4.3.0). This format records a checkpoint's… |
| 04-03 → 02-02 | held, I | 33 | RECORD_SEMANTICS l.750 §10. Consumer and host interface: …/ DEL-02-02 (WR-v0.2; v0.9) / A15 records (HA-10), which its library_entry cites; R2 *sele… |
| 04-03 → 02-03 | held, I | 99 | RECORD_SEMANTICS l.748 §10. Consumer and host interface: …bservation_lost / observation_recovered reach R8 through DEL-02-03 (CE-13, CE-14) / Designed (PROPOSED), not built; a turn interrupt is not recorde… |
| 04-03 → 02-04 | held, I | 12 | RECORD_SEMANTICS l.751 §10. Consumer and host interface: …/ DEL-02-04 (ROLE-v0.2; v0.9) / R3 and R5a meanings / The supply record 0.2 (role guidance a… |
| 04-03 → 03-01 | held, I | 32 | RECORD_SEMANTICS l.733 §10. Consumer and host interface: …/ DEL-03-01 / R7 identity/basis; c₁ for A4/A6/A7 / Subject content identity; method designat… |
| 04-03 → 03-02 | held, I | 19 | RECORD_SEMANTICS l.784 §10.1 Receivers and suppliers by register: …/ DEL-03-02 / DEP-04-03-024 / DEP-03-02-019 / held / Operation outcomes, change-item content… |
| 04-03 → 03-03 | held, I | 38 | RECORD_SEMANTICS l.735 §10. Consumer and host interface: …/ DEL-03-03 / Nothing before its own work: these name where the adapter's evidence lands — R… |
| 04-03 → 04-01 | admitted, I | 29 | RECORD_SEMANTICS l.781 §10.1 Receivers and suppliers by register: …/ DEL-04-01 / DEP-04-03-021 / DEP-04-01-016 / admitted / Act kinds and classes /… |
| 04-03 → 04-02 | held, I | 30 | RECORD_SEMANTICS l.737 §10. Consumer and host interface: …/ DEL-04-02 / Record-out (§8), including R15 and the read state of entries (v0.8) / Settings… |
| 04-03 → 05-01 | held, I | 55 | RECORD_SEMANTICS l.738 §10. Consumer and host interface: …/ DEL-05-01 / R3/R4/R5/R5a/R7/R8/R15/R16 meanings; the §13 entry kinds its events map to (LO… |
| 05-01 → 01-05 | admitted, I | 11 | LOOP_RECEIVING_CONTRAC l.7 §Minimal-loop and model receiving contrac: …y through a Responses interface added behind §4's boundary (DEL-01-05/ACCESS-v0.2 §11 CH-8; §4; §13); nothing is selected and host joins stay deferred… |
| 05-01 → 02-01 | held, I | 55 | LOOP_RECEIVING_CONTRAC l.37 §Minimal-loop and model receiving contrac: …3; table in §10.4): among the first-increment deliverables, DEL-02-01 (DEP-02-01-020, held), DEL-02-03 (DEP-02-03-022, held), DEL-03-04 (DEP-03-04-014… |
| 05-01 → 02-03 | held, I | 94 | LOOP_RECEIVING_CONTRAC l.37 §Minimal-loop and model receiving contrac: …st-increment deliverables, DEL-02-01 (DEP-02-01-020, held), DEL-02-03 (DEP-02-03-022, held), DEL-03-04 (DEP-03-04-014, admitted), DEL-04-02 (DEP-04-02… |
| 05-01 → 03-01 | held, I | 47 | LOOP_RECEIVING_CONTRAC l.83 §0. How to read this definition: …**Fixture.** Cases use the shared fixture **FX-PIPE-01** of DEL-03-01/C-v0.4… |
| 05-01 → 03-02 | held, I | 39 | LOOP_RECEIVING_CONTRAC l.585 §2.3 Events: …/ Host / Stale refusal, A11 or host refusal, per item (from DEL-03-02 item-left events, R2-18) /… |
| 05-01 → 04-01 | admitted, I | 33 | LOOP_RECEIVING_CONTRAC l.458 §2.2 Tools: …host route resolves direct or propose from the grant state (ACT §5.3 rule 7) /… |
| 05-01 → 04-02 | held, I | 34 | LOOP_RECEIVING_CONTRAC l.37 §Minimal-loop and model receiving contrac: …(DEP-02-03-022, held), DEL-03-04 (DEP-03-04-014, admitted), DEL-04-02 (DEP-04-02-018, held), DEL-04-03 (DEP-04-03-028, held), DEL-05-02 (DEP-05-02-010… |
| 05-01 → 04-03 | held, I | 108 | LOOP_RECEIVING_CONTRAC l.6 §Minimal-loop and model receiving contrac: …ADAPTER cite. Recording a **declined** request is required: DEL-04-03's ScopeOfWork CLM-004 names "destination declined" among the network-destination… |
| 05-01 → 05-02 | held, I | 77 | LOOP_RECEIVING_CONTRAC l.6 §Minimal-loop and model receiving contrac: …nt of the destination flow** (DF-1…DF-10) that ACT, AS, RS, PANEL, C, P and ADAPTER cite. Recording a **declined** request is required: DEL-04-03's Sc… |
| 05-02 → 02-01 | held, I | 31 | PANEL_RECEIVING_CONTRA l.35 §Host panel and shared interaction receiv: …EST.md → DAG-003): among the first-increment deliverables, DEL-02-01 (DEP-02-01-021, held: host-panel consumer requirements; §3, §6), DEL-03-04 (DEP-… |
| 05-02 → 02-03 | held, I | 53 | PANEL_RECEIVING_CONTRA l.35 §Host panel and shared interaction receiv: …9 (DEL-04-03), -010 (DEL-05-01), -019 (DEL-04-02) and -020 (DEL-02-03), all held, and -008 (DEL-04-01), admitted; the supplier-side rows DEP-04-01-026… |
| 05-02 → 03-01 | held, I | 17 | PANEL_RECEIVING_CONTRA l.35 §Host panel and shared interaction receiv: …is register's ACTIVE rows: DEP-05-02-005 (DEL-02-01), -006 (DEL-03-01), -007 (DEL-03-02), -009 (DEL-04-03), -010 (DEL-05-01), -019 (DEL-04-02) and -02… |
| 05-02 → 03-02 | held, I | 17 | PANEL_RECEIVING_CONTRA l.35 §Host panel and shared interaction receiv: …VE rows: DEP-05-02-005 (DEL-02-01), -006 (DEL-03-01), -007 (DEL-03-02), -009 (DEL-04-03), -010 (DEL-05-01), -019 (DEL-04-02) and -020 (DEL-02-03), all… |
| 05-02 → 04-01 | admitted, I | 24 | PANEL_RECEIVING_CONTRA l.35 §Host panel and shared interaction receiv: …-019 (DEL-04-02) and -020 (DEL-02-03), all held, and -008 (DEL-04-01), admitted; the supplier-side rows DEP-04-01-026, DEP-04-02-020 and DEP-04-03-03… |
| 05-02 → 04-02 | held, I | 37 | PANEL_RECEIVING_CONTRA l.6 §Host panel and shared interaction receiv: …are ND-2 PS-1…PS-6; the destinations-contacted display is **DEL-04-02's (AS-v0.8 §3.2)**, which ND-4 presents for a host panel. Recording a **declined… |
| 05-02 → 04-03 | held, I | 32 | PANEL_RECEIVING_CONTRA l.6 §Host panel and shared interaction receiv: …a host panel. Recording a **declined** request is required: DEL-04-03's ScopeOfWork CLM-004 names "destination declined" among the events the record f… |
| 05-02 → 05-01 | held, I | 127 | PANEL_RECEIVING_CONTRA l.6 §Host panel and shared interaction receiv: …om v0.8 (node B5) §3.8 receives the one destination flow of DEL-05-01/LOOP-v0.8 §5.3; the prompt states are ND-2 PS-1…PS-6; the destinations-contacted… |
| 06-01 → 01-01 | admitted, P | 8 | FLEET_RECORDS l.342 §7. Interfaces: …/ Consumed (DEP-06-01-013, admitted) / DEL-01-01 / The pin the observations name / — / The observation's pin says which /… |
| 06-01 → 01-03 | admitted, I | 9 | FLEET_RECORDS l.340 §7. Interfaces: …/ Consumed (DEP-06-01-007, admitted) / DEL-01-03 / The delegation export (§7.7) and spawn items, as the App writer's input for d… |
| 06-01 → 04-03 | admitted, I | 22 | FLEET_RECORDS l.341 §7. Interfaces: …/ Consumed (DEP-06-01-008, admitted) / DEL-04-03 / RS act_request and human_act records for decision needs and act references… |
| 06-01 → 07-01 | admitted, P | 5 | FLEET_RECORDS l.343 §7. Interfaces: …/ Consumed (DEP-06-01-011, admitted) / DEL-07-01 / Coverage and adoption account before relying on a changed PEC consumer path /… |
| 06-02 → 04-01 | admitted, I | 5 | DECISION_VIEW l.138 §7. Interfaces: …(records, states, lapse); DEP-06-02-009 → DEL-04-01 (act names, label… |
| 06-02 → 04-03 | admitted, I | 28 | DECISION_VIEW l.58 §2. Inputs: …rd states (partial, read limited, refused, nonconformant) / DEL-04-03 §3, §14.2 / Limits on the view / Shown as limits, never used /… |
| 06-02 → 06-01 | admitted, I | 26 | FLEET_VIEWS l.75 §2. Inputs: …/ RS act_request and human_act records, read by DEL-06-01's decision-need rule (FR RF-6) / DEL-04-03 / Decision waits / "cause not establi… |
| 06-02 → 07-02 | admitted, L | 9 | FLEET_VIEWS l.230 §6. Interfaces: …/ Consumed (DEP-07-02-015, admitted) / DEL-07-02 / The connector standing vocabulary (CFB-v0.2 §2, vendored in DEL-06-01 prototy… |
| 07-01 → 07-02 | held, I | 7 | PEC_RECEIVING l.57 §2. The first consumer question (R23-34 i: …per-feed coverage and freshness from the envelope / Route (DEL-07-02) /… |
| 07-02 → 07-01 | held, I | 10 | CONNECTOR_FALLBACK l.42 §2.1 Envelope: has the receiving owner es: …sed, and the App has deliberately adopted it for this feed (DEL-07-01 OUT-004 account; R23-34 item 7). **Domains:** an identified query contract and a… |
| 07-02 → 08-01 | held, I | 8 | CONNECTOR_FALLBACK l.42 §2.1 Envelope: has the receiving owner es: …and admission basis established by the receiving decisions (DEL-08-01 OUT-004; OI-023) /… |
| 08-01 → 05-01 | admitted, I | 4 | DOMAINS_RECEIVING l.123 §8. Handoffs: …- Not to LOOP: LOOP does not consume this deliverable (R23-34 item 6); a… |
| 08-01 → 07-02 | held, I | 7 | DOMAINS_RECEIVING l.17 §Domains receiving: query, admission and : …chema:** domains.receiving-record.schema.json (references DEL-07-02's… |
| 08-02 → 02-01 | admitted, I | 8 | RESEARCH_TO_DESIGN l.195 §9. Interfaces: …/ Consumed / DEL-02-01 (DEP-08-02-006) / Portable method meanings (WD §3, §4) / admitted /… |
| 08-02 → 08-01 | admitted, I | 9 | RESEARCH_TO_DESIGN l.194 §9. Interfaces: …/ Consumed / DEL-08-01 (DEP-08-02-005) / Query, admission and freshness meanings; receiving records / a… |
| 09-01 → 01-01 | admitted, P | 30 | EXAMINATION_PROTOCOL l.130 §2.1 Inputs: …3 / Recorded real exchanges with origin and configuration / DEL-01-01's capture method; journey owners' captures / DEP-09-01-015, not topological / Re… |
| 09-01 → 01-06 | held, V | 15 | EXAMINATION_PROTOCOL l.132 §2.1 Inputs: …e and its OUT-002 identity record; install/launch witness / DEL-01-06 / DEP-09-01-016, **held** (SCC-003) / Before the native packaged smoke (SCC-003… |
| 09-02 → 01-01 | admitted, P | 11 | STANDALONE_QUALIFICATI l.144 §2. Interfaces: …/ I-1 / Hosting/protocol, verification, recorded seams / DEL-01-01 / DEP-09-02-009, admitted / Before any step / All steps awaiting_input /… |
| 09-02 → 01-02 | admitted, P | 16 | STANDALONE_QUALIFICATI l.145 §2. Interfaces: …/ I-2 / Recovery contribution and checks / DEL-01-02 / DEP-09-02-010, admitted / S11-1…S11-6 / Those steps wait /… |
| 09-02 → 01-03 | admitted, P | 8 | STANDALONE_QUALIFICATI l.146 §2. Interfaces: …/ I-3 / Plan, tool, delegation views / DEL-01-03 / DEP-09-02-011, admitted / J-1, J-2, S11-6 / Those steps wait; plan items optio… |
| 09-02 → 01-04 | admitted, P | 22 | STANDALONE_QUALIFICATI l.147 §2. Interfaces: …Request cards, outcomes, draft view; **App act control** / DEL-01-04 / DEP-09-02-012, admitted (row names the interaction view; the act control is us… |
| 09-02 → 01-05 | admitted, P | 11 | STANDALONE_QUALIFICATI l.148 §2. Interfaces: …/ I-5 / Account/provider access, homes, focused checks / DEL-01-05 / DEP-09-02-013, admitted / M12-1…M12-6 / V4-EXM-12 waits /… |
| 09-02 → 01-06 | admitted, P | 3 | STANDALONE_QUALIFICATI l.149 §2. Interfaces: …/ I-6 / Package and identity record / DEL-01-06 / DEP-09-02-014, admitted / Only if the native steps run on a package / Steps ru… |
| 09-02 → 02-01 | admitted, P | 6 | STANDALONE_QUALIFICATI l.150 §2. Interfaces: …/ I-7 / Workflow declaration / DEL-02-01 / DEP-09-02-015, admitted / J-5, J-7 / Those steps wait /… |
| 09-02 → 02-02 | admitted, P | 18 | STANDALONE_QUALIFICATI l.146 §2. Interfaces: …/ J-1, J-2, S11-6 / Those steps wait; plan items optional (WR J-1) /… |
| 09-02 → 02-03 | admitted, P | 5 | STANDALONE_QUALIFICATI l.152 §2. Interfaces: …/ I-9 / Run start, per-run supply, run end / DEL-02-03 / DEP-09-02-017, admitted / J-7…J-9 / Those steps wait /… |
| 09-02 → 04-01 | admitted, P | 3 | STANDALONE_QUALIFICATI l.153 §2. Interfaces: …/ I-10 / Adopted policy (D2/D3) / DEL-04-01 / DEP-09-02-018, admitted / J-6, S11-3/4 act classification / Settled distinctio… |
| 09-02 → 04-03 | admitted, P | 5 | STANDALONE_QUALIFICATI l.154 §2. Interfaces: …/ I-11 / Act and run records / DEL-04-03 / DEP-09-02-019, admitted / J-6…J-9, S11-3/4 / Those steps wait /… |
| 09-02 → 09-01 | admitted, I | 31 | STANDALONE_QUALIFICATI l.155 §2. Interfaces: …/ I-12 / EXP record, outcomes, routes, review / DEL-09-01 / DEP-09-02-020, admitted / Every step / No record can be written /… |
| 09-05 → 01-03 | admitted, P | 0 | No use in the consumer's Design; the supplier states it (NPTD §10.2 "fixtures and designed cases \| DEL-09-02, DEL-09-05") |
| 09-05 → 04-01 | admitted, I | 3 | DECISION_ATTRIBUTION_C l.148 §7. Interfaces: …/ DEL-04-01 / A8, A16 rows; the adopted policy for the reserving instrument / DEP-09-05-009… |
| 09-05 → 04-03 | admitted, I | 22 | DECISION_ATTRIBUTION_C l.147 §7. Interfaces: …/ DEL-04-03 / act_request with alternatives and consequences; human_act A16; HA-1, HA-11… |
| 09-05 → 06-01 | admitted, P | 4 | DECISION_ATTRIBUTION_C l.150 §7. Interfaces: …/ DEL-06-01 / The package file the agent writes, within the undertaking's records / DEP-09-0… |
| 09-05 → 06-02 | admitted, P | 10 | DECISION_ATTRIBUTION_C l.149 §7. Interfaces: …/ DEL-06-02 / The decision view (DV-1…DV-9); FX-DP1; the waiting view's ready labels (FV-4a;… |
| 09-05 → 09-01 | admitted, I | 11 | DECISION_ATTRIBUTION_C l.152 §7. Interfaces: …/ DEL-09-01 / EXP result records and native-route forms / DEP-09-05-011 (admitted) / EXP-v0.… |
| 09-06 → 01-01 | admitted, P | 36 | CONNECTED_ACTIVITY_CON l.953 §11.1 Expected from suppliers: …/ HOSTING (DEL-01-01) / DEP-09-06-032 / App-side supplied-guidance and model-destination evidence (HO… |
| 09-06 → 02-01 | admitted, I | 83 | CONNECTED_ACTIVITY_CON l.90 §1. Settled distinctions relied on: …oint" for the current phase, OWNER_ITEMS O-25, DECISION-7); WD I-7 is plan guidance in that sense. **Who requests in the current phase (R9-1; SETTLED… |
| 09-06 → 02-02 | admitted, I | 69 | CONNECTED_ACTIVITY_CON l.938 §11.1 Expected from suppliers: …first-increment deliverables, and the arc to DEL-02-02, are in DAG-003's… |
| 09-06 → 02-03 | admitted, I | 173 | CONNECTED_ACTIVITY_CON l.98 §1. Settled distinctions relied on: …it; a record never says *performed* without the act (R9-1; DEL-02-03 REQ-002, "preserve the checkpoint's identity and actual disposition"; PH-6). How… |
| 09-06 → 03-01 | admitted, I | 70 | CONNECTED_ACTIVITY_CON l.943 §11.1 Expected from suppliers: …/ C (DEL-03-01) / DEP-09-06-027 / Catalog/read-basis meanings, as cited per step in §2.3 / C-v0… |
| 09-06 → 03-02 | admitted, I | 40 | CONNECTED_ACTIVITY_CON l.944 §11.1 Expected from suppliers: …/ P (DEL-03-02) / DEP-09-06-028 / Proposal/outcome meanings, as cited per step in §2.3 / P-v0.7… |
| 09-06 → 03-03 | admitted, I | 86 | CONNECTED_ACTIVITY_CON l.945 §11.1 Expected from suppliers: …/ ADAPTER (DEL-03-03) / DEP-09-06-029 / External-receiving meanings: channel states; model destinatio… |
| 09-06 → 04-01 | admitted, I | 50 | CONNECTED_ACTIVITY_CON l.946 §11.1 Expected from suppliers: …/ ACT (DEL-04-01) / DEP-09-06-030 / Adopted operation policy and act distinctions, as cited in S-… |
| 09-06 → 04-02 | admitted, I | 30 | CONNECTED_ACTIVITY_CON l.947 §11.1 Expected from suppliers: …/ AS (DEL-04-02) / DEP-09-06-031 / Grant display, as cited in CA-0, CA-H, CA-R and DI-2 / AS-v0.… |
| 09-06 → 04-03 | admitted, P | 88 | CONNECTED_ACTIVITY_CON l.948 §11.1 Expected from suppliers: …/ RS (DEL-04-03) / DEP-09-06-015; supplier-side DEP-04-03-031 / Records of actual content-bound… |
| 09-06 → 05-01 | admitted, I | 66 | RELAY_QUESTIONS_SWBPIP l.836 §SQ-29 The host loop's model interface an: …- **Depends.** DEP-05-01-024 (supplier UNKNOWN); LOOP-v0.4 §1, §4, §7 MC-6,… |
| 09-06 → 05-02 | admitted, I | 43 | CONNECTED_ACTIVITY_CON l.950 §11.1 Expected from suppliers: …/ PANEL (DEL-05-02) / DEP-09-06-017 / Panel receiving requirements (CA-H) / PANEL-v0.7 /… |
| 09-06 → 09-01 | admitted, I | 8 | CONNECTED_ACTIVITY_CON l.956 §11.1 Expected from suppliers: …/ DEL-09-01 / Supplier-side DEP-09-01-024 / Reusable examination support and evidence interf… |
| 09-07 → 09-01 | admitted, I | 34 | LOCAL_HOST_QUALIFICATI l.336 §8. Interfaces and excluded acts (REQ-009: …/ Common examination support and record mapping / DEL-09-01 / Consumes (DEP-09-01-025; R23-1) /… |
| 09-07 → 09-06 | admitted, P | 16 | LOCAL_HOST_QUALIFICATI l.335 §8. Interfaces and excluded acts (REQ-009: …/ Agreed activity, reusable workflow, round trip / DEL-09-06 / Consumes the agreement (DEP-09-07-011) /… |
| 09-09 → 02-03 | held, I | 29 | EXTERNAL_TRACE_CASES l.78 §1. Settled distinctions relied on: …check depends on the required tools and the channel state (EXEC-v0.5 PH-1…PH-3; R8-2). An observed arrival is recorded, with the request where it can… |
| 09-09 → 03-01 | held, I | 70 | EXTERNAL_TRACE_CASES l.99 §2. Examination input account (REQ-001; A: …/ IN-04 / Catalog and read-basis contract / DEL-03-01 C-v0.7 (DEP-09-09-007) / §3, §4 / Defined (*illustrative*) /… |
| 09-09 → 03-02 | held, I | 26 | EXTERNAL_TRACE_CASES l.89 §2. Examination input account (REQ-001; A: …round-1 versions (C-v0.8, P-v0.8, ADAPTER-v0.6, ACT-POLICY-v0.8, RS-v0.8,… |
| 09-09 → 03-03 | held, I | 62 | EXTERNAL_TRACE_CASES l.101 §2. Examination input account (REQ-001; A: …06 / External receiving contribution and focused fixtures / DEL-03-03 ADAPTER-v0.5 (DEP-09-09-009) / §3 / Defined; native family only, no interpositio… |
| 09-09 → 04-01 | admitted, I | 21 | EXTERNAL_TRACE_CASES l.102 §2. Examination input account (REQ-001; A: …/ IN-07 / Adopted operation policy and act distinctions / DEL-04-01 ACT-POLICY-v0.7 (DEP-09-09-010; D2/D3; §2.6 A13; §4.6 hold support, governance p… |
| 09-09 → 04-02 | held, I | 15 | EXTERNAL_TRACE_CASES l.90 §2. Examination input account (REQ-001; A: …LOOP-v0.8, AS-v0.8, EXEC-v0.6), each adding PROPOSED schemas, sequences and… |
| 09-09 → 04-03 | held, I | 29 | EXTERNAL_TRACE_CASES l.89 §2. Examination input account (REQ-001; A: …-1 versions (C-v0.8, P-v0.8, ADAPTER-v0.6, ACT-POLICY-v0.8, RS-v0.8,… |
| 09-09 → 05-01 | held, I | 22 | EXTERNAL_TRACE_CASES l.90 §2. Examination input account (REQ-001; A: …LOOP-v0.8, AS-v0.8, EXEC-v0.6), each adding PROPOSED schemas, sequences and… |
| 09-09 → 09-01 | admitted, I | 11 | EXTERNAL_TRACE_CASES l.98 §2. Examination input account (REQ-001; A: …col; WebKit/Chromium and packaged-smoke evidence protocol / DEL-09-01 (outside D1; DEP-09-09-012) / §6 / Not defined in this undertaking /… |
| 09-10 → 07-01 | admitted, P | 3 | CONNECTOR_WITNESS l.25 §1. Subject and consumer: …PEC consumer", V4-EXM-30). The coordination question is DEL-07-01's Q1… |
| 09-10 → 07-02 | admitted, P | 3 | CONNECTOR_WITNESS l.27 §1. Subject and consumer: …l absent-PEC/stale-Domains combination. Standing is read in DEL-07-02's… |
| 09-10 → 08-01 | admitted, I | 1 | CONNECTOR_WITNESS l.26 §1. Subject and consumer: …(PRC-v0.1 §2). Domains' research question QD (DRC-v0.1 §5) carries the… |
| 09-10 → 09-01 | admitted, I | 11 | CONNECTOR_WITNESS l.19 §Optional connector consumption witness: …DEL-09-01; DEP-09-01-027 is admitted from DEL-09-01's side. For the… |
| 09-11 → 04-03 | admitted, P | 6 | READER_METHOD l.48 §3. The input set (`rrm.input-set-manifes: …- record: RS entries, act records, capture evidence;… |
| 09-11 → 09-01 | admitted, I | 11 | READER_METHOD l.86 §5. Examiner comparison (VER-002…VER-004): …a limit. The judgment file's reference and hash go into the EXP record's evidence. With no judgment, the check is referred, never held, and the EXP ou… |
| 09-11 → 09-07 | admitted, P | 8 | READER_METHOD l.45 §3. The input set (`rrm.input-set-manifes: …Built by the assembler from the source journey's handoff (DOS §5 for a V4-EXM-20 journey):… |
| 09-12 → 04-01 | admitted, I | 1 | PRACTITIONER_VALIDATIO l.63 §2. Interfaces: …/ I-3 / Adopted operation policy for recording acts / DEL-04-01 ACT / DEP-09-12-011, admitted / When an observed session involves human acts / A… |
| 09-12 → 09-01 | admitted, I | 10 | PRACTITIONER_VALIDATIO l.64 §2. Interfaces: …/ I-4 / Examination support / DEL-09-01 EXP / DEP-09-01-029, admitted / Observation records / Candidate identity uses EX… |
| 10-02 → 09-12 | admitted, E | 3 | UNDERTAKING_CONTROLS l.287 §9. Receiving practitioner observations (: …DEL-09-12 hands over method observations and dispositions. They enter as… |
| 10-02 → 10-01 | admitted, P | 6 | UNDERTAKING_CONTROLS l.206 §6. Practice notes for this run (held her: …/ PN-3 / T2-E (EB-1) / RV3 reviewed EB-v0.1 for correctness while RR-EB1 read it cold. Both found the sam… |
| 10-02 → 10-04 | held, L | 4 | UNDERTAKING_CONTROLS l.282 §8. DAG use and the SCC-CASE-006 pair (RE: …DEL-10-04's mapping unit names its use of them. No cut or merge is needed… |
| 10-03 → 02-01 | admitted, I | 8 | RESPONSIBILITY_ACCOUNT l.167 §3.2 Reverse: does any supplier record na: …entry in §1.2: DEL-02-01 CLM-002, DEL-02-03 CLM-003, DEL-02-04 CLM-002,… |
| 10-03 → 02-03 | admitted, I | 4 | RESPONSIBILITY_ACCOUNT l.167 §3.2 Reverse: does any supplier record na: …entry in §1.2: DEL-02-01 CLM-002, DEL-02-03 CLM-003, DEL-02-04 CLM-002,… |
| 10-03 → 02-04 | admitted, I | 5 | RESPONSIBILITY_ACCOUNT l.167 §3.2 Reverse: does any supplier record na: …entry in §1.2: DEL-02-01 CLM-002, DEL-02-03 CLM-003, DEL-02-04 CLM-002,… |
| 10-03 → 03-01 | admitted, I | 6 | RESPONSIBILITY_ACCOUNT l.168 §3.2 Reverse: does any supplier record na: …DEL-03-01 CLM-002, DEL-03-02 CLM-004, DEL-04-03 REQ-005.… |
| 10-03 → 03-02 | admitted, I | 4 | RESPONSIBILITY_ACCOUNT l.168 §3.2 Reverse: does any supplier record na: …DEL-03-01 CLM-002, DEL-03-02 CLM-004, DEL-04-03 REQ-005.… |
| 10-03 → 04-01 | admitted, I | 9 | RESPONSIBILITY_ACCOUNT l.203 §3.4 Finding F-RA1: three joins are recor: …Their Design files do acknowledge the consumer: ACT §10.3, LOOP §10.4 and… |
| 10-03 → 04-03 | admitted, I | 5 | RESPONSIBILITY_ACCOUNT l.168 §3.2 Reverse: does any supplier record na: …DEL-03-01 CLM-002, DEL-03-02 CLM-004, DEL-04-03 REQ-005.… |
| 10-03 → 05-01 | admitted, I | 6 | RESPONSIBILITY_ACCOUNT l.203 §3.4 Finding F-RA1: three joins are recor: …Their Design files do acknowledge the consumer: ACT §10.3, LOOP §10.4 and… |
| 10-03 → 05-02 | admitted, I | 7 | RESPONSIBILITY_ACCOUNT l.204 §3.4 Finding F-RA1: three joins are recor: …the PANEL Receivers line.… |
| 10-03 → 10-01 | admitted, P | 4 | RESPONSIBILITY_ACCOUNT l.71 §1.4 Excluded, with the reason (so the bo: …/ Manual editions / DEL-10-01's (DEP-10-03-017 is an input basis, not a promise) /… |
| 10-04 → 10-01 | admitted, P | 2 | DAG_ACCOUNT l.6 §Project production dependency DAG — evid: …Status: DRAFT DEFINITION, frozen for RV3** with UC-v0.2 and EB-v0.4.… |
| 10-04 → 10-02 | held, P | 5 | DAG_ACCOUNT l.137 §6. Consumers (handoff): …/ DEL-10-02 (held arc DEP-10-02-012, SCC-005) / Graph-based selection uses the accepted curr… |
| 10-04 → 10-03 | admitted, P | 1 | DAG_ACCOUNT l.112 §5. Currency through the rest of this pas: …is absent. Cases include for example DEL-02-04 → DEL-10-03 is SCC-forming and… |
| 11-01 → 10-01 | admitted, P | 1 | CONTINUITY_ACCOUNT l.52 §2. Interfaces: …/ I-2 / Manual and method pins / DEL-10-01 (EB; CURRENT_EXECUTION_BASIS) / DEP-11-01-009, admitted / Before a selector cite… |
| 11-01 → 10-03 | admitted, P | 7 | CONTINUITY_ACCOUNT l.51 §2. Interfaces: …ping), historical applicability, packaging and tool paths / DEL-10-03 RA (draft, vendored) / DEP-11-01-008, admitted / Before an obligation row is rel… |
| 11-01 → 11-02 | admitted, P | 9 | CONTINUITY_ACCOUNT l.53 §2. Interfaces: …/ I-3 / Adoption status / DEL-11-02 / DEP-11-01-010, admitted / Each account version / not_supplied /… |
| 11-01 → 11-03 | held, L | 9 | CONTINUITY_ACCOUNT l.56 §2. Interfaces: …O-2 / The owner's replacement disposition, returned / from DEL-11-03 / DEP-11-03-015, held / After an attributable owner act / Standing stays "pendin… |
| 11-02 → 02-04 | admitted, E | 4 | ADOPTION_ACCOUNT l.57 §2. Interfaces: …ly evidence (O-3: "the same evidence, no adoption claim") / DEL-02-04 ROLE-v0.2 / DEP-02-04-013, admitted (supplier's row; R22-7-open) / When a candid… |
| 11-02 → 10-01 | admitted, L | 1 | ADOPTION_ACCOUNT l.58 §2. Interfaces: …/ I-3 / Manual and edition pins / DEL-10-01 / DEP-10-01-020, admitted / Before a row cites a manual edition / None cited /… |
| 11-02 → 10-03 | admitted, P | 6 | ADOPTION_ACCOUNT l.56 §2. Interfaces: …s and responsibility (X-1: Root, Runtime, App v3, Piping) / DEL-10-03 RA-v0.2 / DEP-11-02-008, admitted / Each account version / Rows from DEP-006, pr… |
| 11-03 → 09-02 | admitted, P | 5 | REPLACEMENT_PACKET l.65 §2. Interfaces: …1 / SQ dossier record and its handoff (to: DEL-11-03) / DEL-09-02 / DEP-11-03-006, admitted / Packet assembly / OUT-001 *not evidenced*; gap named… |
| 11-03 → 09-07 | admitted, P | 12 | REPLACEMENT_PACKET l.66 §2. Interfaces: …dossier manifest handoff_del_11_03 and the CIR it cites / DEL-09-07 / DEP-11-03-007, admitted / Packet assembly / OUT-002 *incomplete*; gap named /… |
| 11-03 → 09-12 | admitted, P | 5 | REPLACEMENT_PACKET l.110 §3.3 Inputs from DEL-11-01 and DEL-09-12: …- **practitioner_standing** (from DEL-09-12) carries "OI-016 (App v4)" (F-R14) and a standing (not_agreed … ended). When… |
| 11-03 → 11-01 | held, P | 12 | REPLACEMENT_PACKET l.67 §2. Interfaces: …/ I-3 / Continuity hand-over (DEL-11-01 CA $defs/continuity_handoff; from RP-v0.4, replacing the first cut) / DEL-11-0… |
| 11-03 → 11-02 | admitted, P | 8 | REPLACEMENT_PACKET l.69 §2. Interfaces: …/ I-5 / Adoption status: DEL-11-02's AA $defs/adoption_status (S-6, deliverable_record, from RP-v0.5; named ow… |

### 4.4 Not dependencies (251)

| Consumer → supplier | Uses | GC-5 item 2 exclusion or other reason | Citation and representative text |
|---|---:|---|---|
| 01-01 → 01-02 (reverse arc in DAG-004) | 95 | cross-reference | HOSTING §4.4 l.566: "recovery reads prefer those (RECOVERY-v0.2 §5 R-4 …)"; "DEL-01-02 adopts this reading" (use runs 01-02→01-01) |
| 01-01 → 01-03 (reverse arc in DAG-004) | 38 | ruling-carried (R18-1 C-04, R21-1); cross-reference | HOSTING §8.4 HCG-A08 l.1451: signal stated from R18-1 C-04 and "R21-1's order"; NPTD §7.1 cited as "the reference" |
| 01-01 → 01-06 (reverse arc in DAG-004) | 12 | receiver list / owner map | HOSTING §8 S-5 l.1203: S-5 seam row naming the receiver |
| 01-01 → 02-01 (reverse arc in DAG-004) | 40 | cross-reference (use runs 02-01→01-01) | HOSTING §8.4 l.1483: "This file owns the supplier facts and the grouping, and WD-v0.8 §4.2.5 follows it" |
| 01-01 → 02-02 | 19 | attribution (runtime value carried as any turn input) | HOSTING §8 S-6 l.1204; §8.2 l.1286: "composed by DEL-02-02 … the boundary carries it as any turn input and records it" |
| 01-01 → 02-03 (reverse arc in DAG-004) | 61 | attribution / receiver lists | HOSTING §6.7 l.992: "How an App run observes an arrival and a request is DEL-02-03's, defined in EXEC"; G2 N26 (EXEC §9.2 OBS-1 list) is a discharged design-time join: HOSTING's own text holds the observations |
| 01-01 → 02-04 (reverse arc in DAG-004) | 55 | attribution | HOSTING §8.2 l.1285: "recorded by DEL-02-04 as `inherited` from its source (ROLE-v0.2 F-1)" |
| 01-01 → 03-01 | 3 | cross-reference | HOSTING §6.8 l.1089: required-tool catalog read described as App-origin |
| 01-01 → 03-02 | 3 | attribution | HOSTING §6.8 l.1082: "host outcome per DEL-03-02/03-03" |
| 01-01 → 03-04 (reverse arc in DAG-004) | 7 | receiver list | HOSTING §8 l.1218: receivers table row |
| 01-01 → 04-01 | 7 | ruling-carried (D3, R-2, R2-8) | HOSTING §2 l.319; §6.3 l.915: "the DEL-04-01/04-02 autonomy grant governs host operations only, and no App rule answers A14 affirmatively (R-2 D3 bullet)"; "(R2-8; DEL-04-03 R13; App runs only)". G2 N02 (ACT §10.3 V-21/V-25) is therefore not a GC-5 dependency |
| 01-01 → 04-02 | 2 | pin / sibling-label list / case table (no body use) | —: header pin or label list only |
| 01-01 → 04-03 (reverse arc in DAG-004) | 48 | receiver lists / attribution | HOSTING §8.3 l.1351: "The run-level value … and the rule that a switch starts no new run are DEL-04-03's (R5-4); this boundary supplies only per-turn facts" |
| 01-01 → 05-01 | 8 | cross-reference | HOSTING §2 l.326: "(LOOP-v0.7 §5.1.1). It governs host agents only" |
| 01-01 → 05-02 | 3 | pin / sibling-label list / case table (no body use) | —: header pin or label list only |
| 01-01 → 06-01 (reverse arc in DAG-004) | 2 | receiver list | HOSTING §8 l.1222: receivers table |
| 01-01 → 09-01 (reverse arc in DAG-004) | 4 | receiver list | HOSTING §8 l.1222: receivers table |
| 01-01 → 09-02 (reverse arc in DAG-004) | 2 | receiver list | HOSTING §8 l.1223: receivers table |
| 01-01 → 09-06 (reverse arc in DAG-004) | 7 | receiver list | HOSTING §8 l.1205: S-7 seam receiver |
| 01-01 → 09-07 | 3 | pin / sibling-label list / case table (no body use) | —: header pin or label list only |
| 01-01 → 09-09 | 2 | pin / sibling-label list / case table (no body use) | —: header pin or label list only |
| 01-02 → 01-03 (reverse arc in DAG-004) | 13 | receiver list (offered operations) | RECOVERY §4.1 l.412: "observe … DEL-01-03 (execution-state stream; DEP-01-03-012)" |
| 01-02 → 01-04 (reverse arc in DAG-004) | 44 | receiver list / meanings supplied to the presenter | RECOVERY §3.4 l.325: "Labels (the `outcomeLabel` element; meanings for DEL-01-04)" |
| 01-02 → 01-05 | 8 | runtime value (explicit no row) | RECOVERY §4.2 l.437: "the App-owned homes from DEL-01-05 … No row; none is consumed as a contribution" |
| 01-02 → 02-03 (reverse arc in DAG-004) | 17 | attribution | RECOVERY §2 l.136: "through DEL-02-03's run end (EXEC AE-7, RE-6). DEL-01-02 neither performs nor records it" |
| 01-02 → 02-04 | 2 | shared rule stated in own text | RECOVERY §4.1 l.419: "Nothing is overridden on `thread/resume` (one rule with ACCESS-v0.2 Q-11 and ROLE-v0.2 §5.5)" |
| 01-02 → 03-03 (reverse arc in DAG-004) | 7 | receiver list | RECOVERY §4.1 l.421: "tag / look up … DEL-03-03" |
| 01-02 → 04-03 (reverse arc in DAG-004) | 20 | proposal to receivers; explicit no use | RECOVERY §8.2 l.646: "DEL-01-02 writes nothing in DEL-04-03's format (R17-10 …). It offers the custody events; each receiver maps them"; ledger "as RS §13.1 option S-A" is a comparison (rule stated in own text) |
| 01-02 → 09-02 (reverse arc in DAG-004) | 1 | receiver list | RECOVERY header l.12: "DEL-09-02 via its DEP-09-02-010" |
| 01-02 → 09-05 | 1 | attribution | RECOVERY §0 l.77: "(REQ-006 forbids the claim; PKG-06, DEL-09-05)" |
| 01-02 → 09-09 | 3 | receiver (supports G2 N14 in the other direction) | RECOVERY header l.12: "Receivers without a register row (Design reliance only; see §14): … DEL-09-09 (XT XC-06, L-XT-3)" |
| 01-03 → 01-04 (reverse arc in DAG-004) | 35 | receiver list / owner map; runtime values | NPTD §10.1 l.495; §16.3 l.714: "Not proposed, by design: DEL-01-03 consuming DEL-01-04 … those are runtime values (§10.1)"; shared G-4 wording stated in own text |
| 01-03 → 01-05 | 1 | owner map | NPTD §16 l.698: "Account, provider and model selection (K-3) \| DEL-01-05" |
| 01-03 → 02-01 | 3 | cross-reference (use runs 02-01→01-03) | NPTD §7.1 l.365: "this section is the reference R21-1 names; EXEC EV-3a, its `_delegation` and WD §4.2.5 follow it" |
| 01-03 → 02-02 (reverse arc in DAG-004) | 6 | receiver list | NPTD header l.14: "Receivers … DEL-02-02 via DEP-01-03-013" |
| 01-03 → 02-04 | 16 | runtime value (explicit no row) | NPTD §10.1 l.495; header l.15: "K-10 label (DEL-02-04, ROLE O-6)"; "its K-10 label is a runtime value handed to this file" |
| 01-03 → 06-01 (reverse arc in DAG-004) | 5 | receiver list | NPTD §10.2 l.505: "delegation export … PKG-06 / DEL-06-01 (DEP-06-01-007)" |
| 01-03 → 09-02 (reverse arc in DAG-004) | 3 | receiver list | NPTD §10.2 l.506: "fixtures and designed cases \| DEL-09-02, DEL-09-05" |
| 01-03 → 09-05 (reverse arc in DAG-004) | 2 | receiver list | NPTD §10.2 l.506: as above |
| 01-04 → 06-02 | 2 | runtime value (R23-2, explicit no row) | AAC §1.2 l.98: "The package reaches the control as a **runtime value** … (R23-2: no register row from DEL-06-02)" |
| 01-04 → 09-02 (reverse arc in DAG-004) | 1 | receiver list | NIR §2 IF-12 l.210: "DEL-01-04 → DEL-09-02" |
| 01-05 → 01-02 | 14 | runtime value (explicit no row) | ACCESS §1 l.171: "the live work … comes from DEL-01-02's `assess live work` operation … read at run time; no row DEL-01-05 → DEL-01-02 is proposed" |
| 01-05 → 01-04 (reverse arc in DAG-004) | 8 | receiver list | ACCESS §1 I-5, I-6 l.163: "DEL-01-05 → DEL-01-04 (conversation start display, K-3)" |
| 01-05 → 01-06 | 2 | attribution (alternative not selected) | ACCESS §20 l.1000: "Packaging items for DEL-01-06: keychain access, a loopback port …" (in an alternative considered) |
| 01-05 → 02-03 | 1 | ruling-carried (K1-4; R18-1 C-10) | ACCESS header l.64; §8 l.599: "EXEC CAP-8 and RS §6.1 were read for K1-4"; account form "INTEGRATION by R18-1 C-10" |
| 01-05 → 02-04 | 3 | shared rule stated in own text; coordination | ACCESS §6 l.552; UNRESOLVED l.1028: "(one rule with RECOVERY-v0.2 §4.1 and ROLE-v0.2 §5.5)" |
| 01-05 → 05-01 (reverse arc in DAG-004) | 22 | cross-reference (rule stated in own text "by analogy"); receiver | ACCESS §1 I-4 l.162: "(HOSTING §8.3; LOOP N-OPEN-1 closure, applied here by analogy)" |
| 01-05 → 09-02 (reverse arc in DAG-004) | 4 | receiver list | ACCESS §13 l.772: "DEP-09-02-013 (admitted) \| DEL-09-02 consumes" |
| 01-06 → 01-05 | 2 | reach note / pin list | PKG §4.2 l.272: "DEL-01-06 reaches only DEL-01-01, DEL-01-05 and DEL-09-01" |
| 01-06 → 09-02 (reverse arc in DAG-004) | 3 | receiver list | PKG header l.68: "Receivers: DEL-09-02 (DEP-09-02-014, admitted)" |
| 02-01 → 01-02 | 2 | attribution in an operating sequence | WD §3.9 l.561: "Run A ends only by the person's end (DEL-01-02 DEF-4) or its run owner's end" |
| 02-01 → 01-03 | 4 | ruling-carried (R18-1 C-04, R21-1) | WD §4.2.5 l.725: "Availability (C-04 by R18-1, reading order by R21-1; HOSTING HCG-A08; NPTD-v0.2 §7.1, the reference; EXEC EV-3a)" |
| 02-01 → 02-02 (reverse arc in DAG-004) | 66 | attribution (App realization of C-4/C-5 and OS rows stated as WR's) | WD Changes FW-04 l.52; §3.9 OS-1…OS-3 l.546–548: "C-4 gains the App side: pinned on its revision … (WR SL-2, PROPOSED …) … C-4 stands"; "App drafts are DEL-02-02's" |
| 02-01 → 02-04 (reverse arc in DAG-004) | 30 | ruling-carried (R17-9) / attribution | WD §5.2 l.1394: "a conversation may have no role, shown "No role", never a fifth role (R17-9; ROLE-v0.2 §3.1 SL-2)" |
| 02-01 → 03-03 (reverse arc in DAG-004) | 11 | receiver list / allocation map | WD §8 l.1557; §9 l.1632: receiver row; allocation map owners |
| 02-01 → 03-04 (reverse arc in DAG-004) | 13 | receiver list | WD §8 l.1558: receiver row |
| 02-01 → 04-02 | 3 | pin / sibling-label list / case table (no body use) | —: header pin or label list only |
| 02-01 → 08-02 (reverse arc in DAG-004) | 4 | receiver list | WD §8 l.1563: receiver row |
| 02-01 → 09-02 (reverse arc in DAG-004) | 4 | receiver list | WD §8 l.1563: receiver row |
| 02-01 → 09-06 (reverse arc in DAG-004) | 23 | receiver list; example | WD §8 l.1559; EXAMPLES E3 l.1073: receiver row; example cites CA §3.2 |
| 02-01 → 09-09 | 3 | pin / sibling-label list / case table (no body use) | —: header pin or label list only |
| 02-01 → 10-03 (reverse arc in DAG-004) | 4 | receiver list | WD §8 l.1563: receiver row |
| 02-02 → 01-05 | 2 | runtime value (explicit) | WR §7 l.364: "DEL-01-05 account and model access \| none (runtime value only)" |
| 02-02 → 02-04 | 15 | ruling-carried (R20-9, R17-8/R19-7) | WR §16.2 l.509: "The line repeats, for the run in force, the two agent lines the shipped product guidance states (ROLE-v0.2 §4.2 GS-7; R20-9)" |
| 02-02 → 09-02 (reverse arc in DAG-004) | 5 | receiver list | WR §7 l.361; §8 l.377: "DEL-09-02 standalone qualification \| DEP-09-02-016 / DEP-02-02-018" |
| 02-02 → 09-06 (reverse arc in DAG-004) | 5 | receiver list; attribution | WR §7 l.362; §4.1 l.126: "Registration for the round trip (CA §4 …)"; "as CA §4, EXEC RT-6 and WD-EX E3 already assume" |
| 02-03 → 01-03 | 10 | runtime value; ruling-carried (R18-1 C-04) | EXEC §2.7 l.841; §3.4 l.949: "DEL-01-03 (run markers, a runtime value)"; "v0.7 (R18-1 C-04; HOSTING … HCG-A08 …; NPTD-v0.2 §7.1)" |
| 02-03 → 01-05 | 7 | ruling-carried (R18-1 C-10); runtime via DEL-01-04 | EXEC §9.1 l.2021: "The Codex account of the home that runs the conversation, for CAP-8 (ACCESS-v0.2 §8) \| … form per R18-1 C-10" |
| 02-03 → 02-04 | 15 | runtime value (explicit); R20-4 | EXEC §2.7 l.841; §9.1: "the role in force, or "no role" (ROLE-v0.2 SL-7, a runtime value)" |
| 02-03 → 03-04 (reverse arc in DAG-004) | 9 | receiver list | EXEC §9.2 l.2034: receiver row |
| 02-03 → 05-02 (reverse arc in DAG-004) | 24 | receiver list / attribution | EXEC header l.39; §2 l.358: "Also read by DEL-05-02 and DEL-04-02 for display"; "a DEL-02-03 checker only if OI-014 allocates one (PANEL §3.2)" |
| 02-03 → 09-02 (reverse arc in DAG-004) | 3 | receiver list | EXEC §9.2 l.2040: receiver row |
| 02-03 → 09-09 (reverse arc in DAG-004) | 6 | receiver list | EXEC §9.2 l.2036: receiver row |
| 02-03 → 09-11 | 2 | example | EXEC §4.12 RP-6 l.1658: "Inspection replay (read-only, e.g. DEL-09-11)" |
| 02-03 → 10-03 (reverse arc in DAG-004) | 3 | receiver list | EXEC §9.2 l.2040: receiver row |
| 02-04 → 01-02 | 2 | owner map | ROLE §1 l.92: "durable custody of other owners' records (DEL-01-02, C-19)" |
| 02-04 → 01-03 | 10 | runtime value (explicit) / owner map | ROLE §7.2 O-6 l.547: "DEL-01-03: role per thread … carried as handed (C-07, C-08) \| none (runtime)" |
| 02-04 → 01-04 (reverse arc in DAG-004) | 11 | receiver list | ROLE §7.2 O-8 l.549: "DEL-01-04: the role list with its preselection …" |
| 02-04 → 01-05 | 4 | runtime value (explicit) | ROLE §7.1 C-7 l.534: "DEL-01-05: a chosen model (K-3); the App home's links (R18-6) \| none (runtime)" |
| 02-04 → 02-02 | 11 | attribution | ROLE §1 l.89: "Workflow supply per run (DEL-02-02 composes the run-start text; DEL-02-03 starts the run; R19-7)" |
| 02-04 → 02-03 | 11 | attribution; ruling-carried (R20-1, R20-11) | ROLE §4.2 l.260; §3.1 l.148: "The App reads only these exact forms in these places, never prose (EXEC RC-5)"; "(INTEGRATION; EXEC owns the reading; U-R10)" |
| 02-04 → 03-04 (reverse arc in DAG-004) | 3 | receiver list | ROLE §7.2 O-4 l.545: "DEL-03-04: semantics for row 8" |
| 02-04 → 04-01 | 2 | cross-reference (negative statement) | ROLE §3.1 SL-4 l.136: "Choosing a role grants nothing and is not one of ACT-v0.8's acts" |
| 02-04 → 04-03 (reverse arc in DAG-004) | 12 | proposal to receiver; owner map | ROLE §6.1 l.459: "It is the proposed body of RS R3 `supplied_guidance` for **role guidance**" |
| 02-04 → 10-03 (reverse arc in DAG-004) | 1 | receiver list | ROLE §7.2 O-5 l.546: "DEL-10-03: supply obligations" |
| 02-04 → 11-02 (reverse arc in DAG-004) | 4 | receiver list; owner map | ROLE §7.2 O-3 l.544; §6.4 l.517: "Consumer adoption \| Not here. DEL-11-02 records …" |
| 03-01 → 01-01 | 1 | pin / sibling-label list / case table (no body use) | —: header pin or label list only |
| 03-01 → 02-03 (reverse arc in DAG-004) | 44 | attribution (consumer behaviour described) | C §2.3 CF-1, CF-3 l.228–230; §7.1 l.840: "Every entry and every required-tool reference on that surface is *not established* (EXEC EV-4; ADAPTER §3.2)"; "Required-tool check … \| EXEC's evaluator" |
| 03-01 → 03-03 (reverse arc in DAG-004) | 42 | example / attribution | C §2.3 CF-1 l.228; §2.1 l.182: "(for example the supplier reports that tool discovery failed, ADAPTER-v0.6 §3.5)"; "The consumer: the host loop (DEL-05-01) or the App (DEL-03-03)" |
| 03-01 → 03-04 (reverse arc in DAG-004) | 4 | receiver list | C header l.9: receivers line |
| 03-01 → 04-02 (reverse arc in DAG-004) | 10 | receiver list / responsibility map | C §1 l.110: "DEL-04-02 \| Autonomy grant display states and standing display; consumes §6" |
| 03-01 → 05-01 (reverse arc in DAG-004) | 37 | receiver list; consumer mapping | C §2 l.125: "DEL-05-01 "catalog identity" maps to it (V1-C D-27)" |
| 03-01 → 05-02 (reverse arc in DAG-004) | 10 | receiver list | C §1 l.112; §4.1 l.424: "they consume, not redefine, these meanings"; "DEL-04-03, DEL-05-01 and DEL-05-02 adopt both unchanged (R-7 …)" |
| 03-01 → 09-06 (reverse arc in DAG-004) | 6 | receiver list | C header l.9: receivers line |
| 03-01 → 10-03 (reverse arc in DAG-004) | 5 | receiver list / responsibility map | C header l.9; §8 l.907: receivers line |
| 03-02 → 01-01 | 1 | pin / sibling-label list / case table (no body use) | —: header pin or label list only |
| 03-02 → 02-03 (reverse arc in DAG-004) | 38 | ruling-carried (R5-1); receiver list; authority map | P §4.4 l.542; §1 l.110: "takes one of four values per checkpoint and surface (R5-1; DEL-02-03 EXEC …)" |
| 03-02 → 03-03 (reverse arc in DAG-004) | 18 | receiver list; attribution | P §13 l.1027; §2 l.127: "Provide to \| DEL-03-03 (DEP-03-02-020)" |
| 03-02 → 03-04 (reverse arc in DAG-004) | 4 | receiver list | P §13 l.1031: "Provide to \| DEL-03-04" |
| 03-02 → 04-03 (reverse arc in DAG-004) | 16 | cross-reference (use runs 04-03→03-02) | P §0 l.35; §3.3 l.254: "DEL-04-03, DEL-05-01 and DEL-05-02 adopt it"; "(… adopted in RS R11 by …)" |
| 03-02 → 05-01 (reverse arc in DAG-004) | 25 | cross-reference (use runs 05-01→03-02) | P §3.1 l.199: "adopts this rule (R12-7, INTEGRATION; LOOP-v0.8 §7 MC-8)" |
| 03-02 → 05-02 (reverse arc in DAG-004) | 9 | receiver list; cross-reference | P §13 l.1029; §4.4 l.531: "Provide to \| DEL-05-02" |
| 03-02 → 09-06 (reverse arc in DAG-004) | 6 | receiver list | P §13 l.1035: "Provide to \| DEL-09-06" |
| 03-02 → 09-09 (reverse arc in DAG-004) | 8 | receiver list; cross-reference | P §1 l.113; §4.2 l.422: "Joined external witness … \| DEL-09-09 \| Supplied: fixtures and outcome expectations" |
| 03-02 → 10-03 (reverse arc in DAG-004) | 4 | receiver list | P §13 l.1036: "Provide to \| DEL-10-03" |
| 03-03 → 01-04 | 6 | owner map; attribution of a trigger | ADAPTER §1 l.102; §3.6 l.393: "with DEL-01-04 presenting the requests the person answers (NIR-v0.2 §4)"; "the person's Stop Codex or Restart Codex … (RECOVERY-v0.2 DEF-5; NIR-v0.2 §5.2)" |
| 03-03 → 01-05 | 6 | owner map; fact cited | ADAPTER §1 l.102; §9 l.1280: "DEL-01-05 the accounts, providers and configuration writes (ACCESS-v0.2 §1, §3)" |
| 03-03 → 03-04 (reverse arc in DAG-004) | 8 | receiver list | ADAPTER §11 l.1442: "Provide to \| DEL-03-04" |
| 03-03 → 04-03 (reverse arc in DAG-004) | 53 | cross-reference (use runs 04-03→03-03, R14-3); attribution | ADAPTER §4.6 l.576; §3.1 l.183: "every value of this record's outcome list adopted by RS-v0.8 §5 (R14-3)"; "App records them (RS R5 model destination)" |
| 03-03 → 05-02 | 4 | cross-reference | ADAPTER §10 l.1300: fixture inventory note |
| 03-03 → 09-06 (reverse arc in DAG-004) | 25 | explicit "not a contribution" (host record cited) | ADAPTER §11 l.1439: "Cites (a host record; not a contribution) \| SWBPIPE's answers to RELAY-v0.3, held in DEL-09-06's folder" |
| 03-03 → 09-09 (reverse arc in DAG-004) | 28 | cross-reference (rehearsal alignment); receiver | ADAPTER §10.2 l.1377: "XF-40 … (rehearses XT XC-05 / L-XT-2)" |
| 03-04 → 06-02 | 1 | attribution (runtime value per R23-2) | GUIDE §2.5 l.451: "which reaches the control as a runtime value when the person opens it from DEL-06-02's decision view" |
| 03-04 → 09-07 | 2 | attribution | GUIDE HC-7 l.807: "V4-EXM-23 observation (DEL-09-07, outside D1)" |
| 03-04 → 10-03 | 2 | pin / sibling-label list / case table (no body use) | —: header pin or label list only |
| 04-01 → 01-01 | 14 | ruling-carried (D3, R2-8); cross-reference | ACT §10.1 V-21, V-25 l.1700–1701; §9 l.1674: "V-21 \| P-04 routine tool permission \| D3 plus INTEGRATION"; "V-25 \| A14 recorded only in R13 … \| R2-8"; label rule names HOSTING's A14 `declined` only to exclude it |
| 04-01 → 01-02 (reverse arc in DAG-004) | 5 | receiver list | ACT §10.3 l.1742: "DEL-01-02 \| DEP-01-02-021" |
| 04-01 → 03-03 (reverse arc in DAG-004) | 25 | ruling-carried (R4-13, R4-14, R5-2); cross-reference | ACT §4.4 l.960; §2.6 l.524: "Carriage assurance (R4-14, final per R5-2; ADAPTER §5.1–§5.3)"; "Standing: PROPOSED by DEL-04-01 under R4-13" |
| 04-01 → 03-04 (reverse arc in DAG-004) | 10 | receiver list | ACT §10.3 l.1737: "DEL-03-04 \| … The guide integrates and checks this contract" |
| 04-01 → 05-02 (reverse arc in DAG-004) | 25 | cross-reference (cases elsewhere awaiting input) | ACT §4.4 l.991: "fixtures are AWAITING INPUT (FX-29; LOOP FX-C9, PANEL PC-24, WD VC-11)" |
| 04-01 → 06-02 (reverse arc in DAG-004) | 3 | receiver list | ACT §10.3 l.1745: "DEL-06-02 \| DEP-06-02-009 \| none \| Not mapped in detail" |
| 04-01 → 09-02 (reverse arc in DAG-004) | 3 | receiver list | ACT §10.3 l.1746: as above |
| 04-01 → 09-05 (reverse arc in DAG-004) | 2 | receiver list | ACT §10.3 l.1747: as above |
| 04-01 → 09-06 (reverse arc in DAG-004) | 12 | receiver list | ACT §10.3 l.1741: as above |
| 04-01 → 09-09 (reverse arc in DAG-004) | 10 | receiver list | ACT §10.1 l.1693: consumer columns |
| 04-01 → 09-12 (reverse arc in DAG-004) | 2 | receiver list | ACT §10.3 l.1748: as above |
| 04-01 → 10-03 (reverse arc in DAG-004) | 3 | receiver list | ACT header l.79: as above |
| 04-02 → 01-01 | 5 | cross-reference | AS §2 l.216: "The App's own Codex is not governed by it (HOSTING §2)" |
| 04-02 → 01-04 (reverse arc in DAG-004) | 9 | receiver list; owner map | AS §12.1 l.824; §10 l.725: "Placing the checkpoint overlay … \| DEL-01-04 (NIR-v0.2 §9); this file defines the components and their meaning" |
| 04-02 → 03-03 (reverse arc in DAG-004) | 20 | receiver list; supplier-side check of receivers; fixture cross-reference | AS §12 l.17; VC-20 l.922; §11 F19 l.773: "VC-20 Receiver conditions (AS 5) \| §12.1 against each receiver's own text (… ADAPTER §5.5 …)" |
| 04-02 → 03-04 (reverse arc in DAG-004) | 7 | receiver list | AS §12 l.794: receiver row |
| 04-02 → 05-02 (reverse arc in DAG-004) | 24 | receiver list; attribution | AS §3.1 l.330; §12.1 l.821: "the contact is shown where contacts are shown (PANEL ND-4)" |
| 04-02 → 09-06 (reverse arc in DAG-004) | 6 | receiver list | AS §12 l.795: receiver row |
| 04-02 → 09-09 (reverse arc in DAG-004) | 5 | receiver list | AS §12 l.796: receiver row |
| 04-03 → 01-05 | 6 | cross-reference (mapping runs 01-05→04-03); runtime value | RS §4 R5 l.325; §6.1 l.523: "DEL-01-05 maps its access entry kinds onto these classes"; codexAccount "supplied by DEL-01-05 … to the act control" |
| 04-03 → 03-04 (reverse arc in DAG-004) | 8 | receiver list | RS §10 l.736: receiver row |
| 04-03 → 05-02 (reverse arc in DAG-004) | 9 | receiver list | RS §10 l.739: receiver row |
| 04-03 → 06-01 (reverse arc in DAG-004) | 3 | receiver list | RS §10 l.743: receiver row |
| 04-03 → 06-02 (reverse arc in DAG-004) | 2 | receiver list | RS §10.1 l.773: receiver row |
| 04-03 → 09-02 (reverse arc in DAG-004) | 4 | receiver list | RS §10 l.745: receiver row |
| 04-03 → 09-05 (reverse arc in DAG-004) | 4 | receiver list | RS §10 l.746: receiver row |
| 04-03 → 09-09 (reverse arc in DAG-004) | 7 | receiver list | RS §10 l.742: receiver row |
| 04-03 → 09-11 (reverse arc in DAG-004) | 5 | receiver list | RS §10 l.744: receiver row |
| 04-03 → 10-03 (reverse arc in DAG-004) | 4 | receiver list | RS §10 l.747: receiver row |
| 05-01 → 01-01 | 39 | corroborating observation; rules stand on FB-CC-1 (= G2 A5) | LOOP UNRESOLVED l.2741; §4.1: "§4's representation rows, MC-6 and MC-8 are PROPOSED from it; OBS-1 observed the four points on one local server (§4.1) and changed none of them" |
| 05-01 → 02-02 | 1 | owner map | LOOP §9 l.2298: "A15 … \| Person, in the App (ACT-POLICY-v0.8 §2.1; DEL-02-02) \| Nothing: not a host-loop act" |
| 05-01 → 02-04 | 1 | owner map (UNRESOLVED) | LOOP UNRESOLVED l.2762: "Seat role mapping (U-09) \| DEL-02-01 with SWB owner and DEL-02-04" |
| 05-01 → 03-03 | 10 | attribution; receivers of LOOP's account | LOOP §5.3 l.1756; §1 l.381: "the one account of the destination flow (DF-1…DF-10) that ACT, AS, RS, PANEL, C, P and ADAPTER cite" |
| 05-01 → 03-04 (reverse arc in DAG-004) | 6 | receiver list | LOOP §10.4 l.2390: receiver row |
| 05-01 → 08-01 (reverse arc in DAG-004) | 3 | receiver list | LOOP §10.4 l.2396: receiver row |
| 05-01 → 09-06 (reverse arc in DAG-004) | 21 | receiver list; relay route | LOOP §10.4 l.2394: receiver row |
| 05-01 → 09-09 (reverse arc in DAG-004) | 4 | receiver list | LOOP §10.4 l.2395: receiver row |
| 05-01 → 10-03 (reverse arc in DAG-004) | 3 | receiver list | LOOP §10.4 l.2397: receiver row |
| 05-02 → 01-01 | 5 | cross-reference | PANEL §3.8 l.664: "(ARCH §4 …; HOSTING §2)" |
| 05-02 → 01-04 | 6 | attribution (capture surface per K-8); allocation account | PANEL §5 l.859; §6 l.898: "A15 … \| Person \| DEL-01-04's App act control (AAC-v0.2 §4.2), presenting DEL-02-02's A15 descriptor" |
| 05-02 → 02-02 | 6 | attribution; allocation account | PANEL §6 l.898: "App workflow experience (DEL-02-02: WR-v0.2 §4.4 selection, §4.6 library standing …)" |
| 05-02 → 03-03 | 7 | attribution | PANEL §3.7 l.646: "The external channel's own display is DEL-03-03's" |
| 05-02 → 03-04 (reverse arc in DAG-004) | 6 | receiver list | PANEL header l.35: receivers line |
| 05-02 → 09-06 (reverse arc in DAG-004) | 15 | receiver list; relay route | PANEL §8 l.1074: relay questions |
| 05-02 → 09-09 | 2 | pin / sibling-label list / case table (no body use) | —: header pin or label list only |
| 05-02 → 10-03 (reverse arc in DAG-004) | 2 | receiver list | PANEL header l.35: receivers line |
| 06-01 → 01-04 | 1 | owner map | FR §10 l.421: "Act and run records, decision capture \| DEL-04-03; DEL-01-04's act control \| Cites and reads" |
| 06-01 → 02-03 | 1 | cross-reference (negative) | FR §4 AS-4 l.210: "It is not RS's act-request identification (EXEC RC-5 governs that)" |
| 06-01 → 03-03 | 1 | cross-reference (a finding cited as reason) | FR §2 l.80: "adding one would change the whole App's tool set (ADAPTER F-9)" |
| 06-01 → 06-02 (reverse arc in DAG-004) | 9 | receiver list | FR §7: "Offered (DEP-06-02-008) \| DEL-06-02" |
| 06-01 → 09-05 (reverse arc in DAG-004) | 3 | receiver list | FR §7 l.347: "Offered (DEP-09-05-006) \| DEL-09-05" |
| 06-01 → 09-11 | 1 | receiver list | FR §8 l.357: "DEL-09-11 (reconstruction, through its input set)" |
| 06-01 → 10-02 | 3 | owner map | FR §10 l.425: "Undertaking practice; project DAG \| DEL-10-02; DEL-10-04 \| `projectDagRef` cites; nothing restated" |
| 06-01 → 10-04 | 2 | owner map; reference string | FR §1 l.67; §10 l.425: "They are not the project DAG (DEL-10-04 …)" |
| 06-02 → 01-02 | 1 | pin list | DV header l.24: pin line |
| 06-02 → 01-04 | 10 | runtime value (R23-2); attribution of the control's rules | DV §5 l.114–118: "the App opens DEL-01-04's act control … nothing opens the control except the person (AAC AK-a, AK-b)" |
| 06-02 → 07-01 | 1 | example of a runtime record (vocabulary from DEL-07-02) | FV §2 l.76: "e.g. DEL-07-01's PEC receiving record or DEL-08-01's Domains record) \| DEL-07-02 vocabulary" |
| 06-02 → 08-01 | 1 | example of a runtime record | FV §2 l.76: as above |
| 06-02 → 09-05 (reverse arc in DAG-004) | 4 | receiver list | DV §7 l.145: "To DEL-09-05 and DEL-09-11: the fixture FX-DP1" |
| 06-02 → 09-11 | 2 | receiver list | DV §7 l.145: as above |
| 07-01 → 01-03 | 1 | cross-reference | PRC §7 l.147: "observed as `mcpToolCall` (HOSTING §6.8; NPTD tool row)" |
| 07-01 → 04-03 | 3 | false match (PEC project's DEL-04-03) | PRC l.19, l.71: "PEC DEL-04-03 and DEL-08-06 are INITIALIZED" |
| 07-01 → 06-01 (reverse arc in DAG-004) | 2 | cross-reference | PRC §2 l.63: "(FR-v0.1 §8: "PEC: none adopted")" |
| 07-01 → 06-02 | 1 | cross-reference | PRC §1 l.44: "(FV-v0.1 §2, "Not inputs (SETTLED …) PEC"; DV-v0.1)" |
| 07-01 → 09-10 (reverse arc in DAG-004) | 1 | receiver list | PRC §9 l.260: "VER-008 \| DEL-09-10's records" |
| 07-02 → 06-01 | 2 | explicit no row (read as files, R23-34 item 6) | CFB §6 l.179: "a row to DEL-06-01 one in both layers. FV consumes this deliverable, never the reverse" |
| 07-02 → 06-02 (reverse arc in DAG-004) | 3 | receiver list | CFB §6 l.173: "Offered to \| DEL-06-02 FV" |
| 07-02 → 09-01 | 1 | location of verification records | CFB §8 l.202: "VER-007 \| EXP rehearsal records in DEL-09-10 \| rehearsed" |
| 07-02 → 09-10 (reverse arc in DAG-004) | 2 | receiver list | CFB §6 l.175: "Supplied to \| DEL-09-10" |
| 08-01 → 02-01 | 1 | deferred decision noted, not opened | DRC §7 l.115: "How a workflow declares a Domains tool \| Domains-enabled increment (R23-34 item 5 …) \| Noted, not opened" |
| 08-01 → 08-02 (reverse arc in DAG-004) | 1 | receiver list | DRC §8 l.121: "To DEL-08-02" |
| 08-01 → 09-10 (reverse arc in DAG-004) | 1 | receiver list | DRC §8 l.122: "To DEL-09-10" |
| 08-02 → 01-04 | 1 | comparison | RTD §12 l.227: "(as A16 and AAC do)" |
| 08-02 → 02-03 | 1 | proposal of shared rows, deferred | RTD §12 l.225: "Shared rows for the candidate decision (ACT, RS, CE, GUIDE, WD closed list) \| … \| When the Domains-enabled increment is selected" |
| 08-02 → 03-04 (reverse arc in DAG-004) | 2 | proposal of shared rows, deferred | RTD §4 l.113: "No row is added to ACT, RS, CE or GUIDE now" |
| 08-02 → 10-03 | 1 | pin / sibling-label list / case table (no body use) | —: header pin or label list only |
| 09-01 → 01-02 | 3 | example; label crosswalk column | EXP §2.1 IN-2 l.129; §3.2 l.198: "(e.g. RECOVERY VC-R-*, NIR VC-NIR-*, …)" |
| 09-01 → 01-03 | 1 | example | EXP §2.1 IN-2 l.129: as above |
| 09-01 → 01-04 | 12 | explicit cross-reference, not reliance | EXP §8.1 l.467; §14 O-4 l.685: "DEL-01-04's act control, by its own text, captures only the person's confirmation (AAC NA-3; VC-AAC-03) — a consistent cross-reference, not a reliance"; "EXP cites AAC (DEL-01-04) and RS (DEL-04-03) only as cross-references" |
| 09-01 → 01-05 | 1 | example | EXP §2.1 IN-2 l.129: as above |
| 09-01 → 04-03 | 6 | explicit no reliance | EXP §3.4 l.229: "DERIVED: DEL-09-01 cannot rely on DEL-04-03 without a cycle" |
| 09-01 → 09-02 (reverse arc in DAG-004) | 4 | receiver list | EXP §2.2 l.146: receivers |
| 09-01 → 09-07 (reverse arc in DAG-004) | 1 | example | EXP §6.1 l.343: "(as DEL-09-07 LHQ LF-1 does)" |
| 09-01 → 09-12 (reverse arc in DAG-004) | 2 | receiver list; owner map | EXP §1 l.116: "Practitioner validation and its period \| DEL-09-12 with the owner" |
| 09-02 → 09-07 | 1 | attribution | SQ §0 l.103: "no host witness (DEL-09-07)" |
| 09-02 → 11-03 (reverse arc in DAG-004) | 12 | receiver list | SQ §2 O-1 l.157: "→ DEL-11-03" |
| 09-05 → 04-02 | 2 | transitive schema reference (through RS) | DAC header l.15; §6 l.113: "with DEL-04-02's `AS_SETTINGS_IN.schema.json`, which RS references" |
| 09-05 → 09-11 | 1 | explicit no row (shared fixture only) | DAC §7 l.153: "None (no row; the early path shares the fixture only)" |
| 09-05 → 10-03 | 2 | pin / sibling-label list / case table (no body use) | —: header pin or label list only |
| 09-06 → 02-04 | 3 | attribution (App-side step) | CA §4 l.567: "role guidance separately (ROLE-v0.2; HOSTING §8.2)" |
| 09-06 → 09-02 | 3 | owner map | CA §10 l.920: excluded acts and owners |
| 09-06 → 09-05 | 2 | owner map | CA §6 l.638; §10 l.920: "not evidence of longer-work recovery (DEL-09-05)" |
| 09-06 → 09-07 (reverse arc in DAG-004) | 19 | receiver list | CA header l.31; §11.1 l.961: "DEL-09-07 \| none (it is a consumer, §11.2)" |
| 09-06 → 09-09 | 57 | explicit cross-reference, no row | CA header l.31; §2.3.1 l.273: "Cross-references without a register row (not receiving arcs): DEL-09-09 (V4-EXM-24/25; shared act cases …)" |
| 09-06 → 11-03 | 1 | owner map | CA §10 l.920: excluded acts and owners |
| 09-07 → 01-01 | 6 | cross-reference; method lesson | LHQ §6.2 l.294; TOP §2.1 l.32: "DEL-09-01 maps its record to HOSTING §9.3's labels (R23-1); this file uses EXAMINATION's spelling" |
| 09-07 → 01-06 | 2 | runtime value (the candidate when one exists) | LHQ §3 l.80: "package digest (DEL-01-06's packaged candidate when one exists)" |
| 09-07 → 03-03 | 1 | explicitly not applicable | LHQ §6.1 l.269: "Not applicable: … CAF-34 (an App restart with a submission in flight, ADAPTER PI-6; replaced on E by LF-14)" |
| 09-07 → 03-04 | 4 | basis-carried (V4-ARC-12) | LHQ §5.4 l.248: "which refuses what is not allowed (V4-ARC-12; GUIDE HC-7.3)" |
| 09-07 → 09-09 | 4 | attribution | LHQ §1 l.36; §8 l.344: "the external channel CA/X and V4-EXM-25 are DEL-09-09's" |
| 09-07 → 11-03 (reverse arc in DAG-004) | 18 | receiver list | LHQ header l.13; DOS §4: "Receivers. DEL-11-03 (DEP-11-03-007 …)" |
| 09-09 → 01-01 | 8 | owner of a finding | XT §9.2 l.708: "… \| DEL-04-03 with DEL-01-01" |
| 09-09 → 03-04 (reverse arc in DAG-004) | 8 | receiver list | XT header l.22: "DEL-03-04 (its guide consumes the external trace cases; DEP-03-04-023 …)" |
| 09-09 → 05-02 | 7 | host-owner allocation in an account | XT §5.1.1 l.545: "Host owner → DEL-05-02; DEL-03-03" |
| 09-09 → 09-07 | 1 | note for another owner | XT §9.1 F-8 l.699: "Unchanged; noted for DEL-09-07" |
| 09-10 → 08-02 | 1 | owner note | CW §7 l.107: "Domains cases on admitted sources (V4-EXM-32 is DEL-08-02's)" |
| 09-11 → 10-03 | 1 | pin note | RRM header l.19: "changes only the label, the change note and the §10.3 DEL-10-03 row" |
| 09-12 → 01-02 | 1 | example | PV §3.4 l.132: "Examples: `V4-EXE-01` → DEL-01-02" |
| 09-12 → 10-01 | 1 | owner map | PV §0 l.43: "changing a requirement or a manual (feature owners; DEL-10-01/10-02 …)" |
| 10-01 → 09-01 | 2 | pointer | EB §2 l.75: "V4-OPS-34 for product candidates (EXP §7, R23-12), which is unchanged" |
| 10-01 → 09-02 | 1 | record of an owner direction | EB §2 B-12 l.69: "(1) DEL-09-02's OI-009 wording carried to the next amendment" |
| 10-01 → 10-02 (reverse arc in DAG-004) | 1 | receiver list | EB §7 l.268: receiver row |
| 10-01 → 10-03 (reverse arc in DAG-004) | 1 | receiver list | EB §7 l.269: receiver row |
| 10-01 → 10-04 (reverse arc in DAG-004) | 2 | receiver list | EB §7 l.270: receiver row |
| 10-01 → 11-01 (reverse arc in DAG-004) | 1 | receiver list | EB §7 l.271: receiver row |
| 10-01 → 11-02 (reverse arc in DAG-004) | 1 | receiver list | EB §7 l.272: receiver row |
| 10-02 → 06-01 | 1 | verification note | UC §11 l.304: VER-008 follow-up |
| 10-02 → 09-01 | 1 | pointer | UC §4.1 l.129: "For product candidates: EXP §7" |
| 10-03 → 02-02 | 3 | owner attribution | RA §2.2 l.106: "Supply of bundled workflows: DEL-02-02" |
| 10-03 → 10-04 (reverse arc in DAG-004) | 1 | receiver list | RA §3.2 l.172: consumer rows |
| 10-03 → 11-01 (reverse arc in DAG-004) | 1 | receiver list | RA §3.2 l.172: consumer rows |
| 10-03 → 11-02 (reverse arc in DAG-004) | 4 | receiver list | RA §1.3 l.59: "Handed to PKG-11 (DEP-10-03-019)" |
| 10-04 → 01-01 | 1 | pin / sibling-label list / case table (no body use) | —: header pin or label list only |
| 10-04 → 01-03 | 4 | evidence note | DA §3 l.72: "(DEL-01-03 TargetLocation repair)" |
| 10-04 → 01-05 | 1 | pin / sibling-label list / case table (no body use) | —: header pin or label list only |
| 10-04 → 02-04 | 1 | example | DA §5 l.112: "Cases include for example DEL-02-04 → DEL-10-03 is SCC-forming" |
| 10-04 → 03-01 | 1 | pin / sibling-label list / case table (no body use) | —: header pin or label list only |
| 10-04 → 03-02 | 1 | pin / sibling-label list / case table (no body use) | —: header pin or label list only |
| 10-04 → 06-01 | 2 | explicit reference string only | DA §6 l.139: "A reference string only; the App reading a user's DAG is unowned and not added (R23-31.10)" |
| 10-04 → 11-01 | 1 | pin / sibling-label list / case table (no body use) | —: header pin or label list only |
| 10-04 → 11-03 | 1 | pin / sibling-label list / case table (no body use) | —: header pin or label list only |
| 11-02 → 11-01 (reverse arc in DAG-004) | 6 | receiver list; attribution | AA §2 O-1 l.60; §6 l.139: "The correction is carried into DEL-11-01 CA-v0.3 and DEL-11-03 RP-v0.6 S-6" |
| 11-02 → 11-03 (reverse arc in DAG-004) | 6 | receiver list; attribution | AA §2 O-2 l.61: "O-2 \| The same hand-over \| DEL-11-03" |
| 11-03 → 01-04 | 1 | runtime record cited | RP §6.2 l.216: "that A16 record is cited as well. No ACT, RS, AAC or shared schema changes" |
| 11-03 → 04-03 | 2 | analogy; rule stated in own text | RP §6.2 l.222: "makes the disposition *lapsed*, as an A16 on a changed file lapses (RS L-1)" |
| 11-03 → 09-11 | 2 | cross-reference (location class) | RP §4.2 l.139: "the DEL-09-11 handoff (`elsewhere_in_dossier`)" |

## 5. SCC effect

### 5.1 New SCC-forming dependencies (in neither G2 list), one line each

Effects are on DAG-004, with the pair added alone, under O-1 / O-2 / O-3 / O-4.

| Consumer → supplier | Use (short) | Effect | Kind |
|---|---|---|---|
| **01-03 → 04-03** | NPTD TA-4 shows act records by RS §6.1 elements and applies RS HA-2 | DEL-01-03 joins SCC-002 (14 / 13 / 13 / 13) | I |
| **04-01 → 04-03** | ACT §2.5 file content identity; lapse vocabulary | DEL-04-01, 01-02 and 01-03 join (16 / 15 / 15 / 15) | I |
| **04-01 → 02-02** | ACT A15 subject from WR's descriptor (RB-4) | as above | I |
| **04-01 → 03-02** | ACT §2.5 change-item content identity; P §9 outcomes | as above | I |
| **09-06 → 03-04** | RELAY P8 questions derived from GUIDE's receiving-map needs | NEW {03-04, 09-06} under every option | I |
| **09-12 → 10-02** | PV `method_note` has "exactly DEL-10-02 UC §5's fields" | SCC-005 grows to {09-12, 10-02, 10-04} (O-1, O-2); NEW {09-12, 10-02} (O-3); no cycle (O-4) | I |
| **01-06 → 01-04** | PKG SIGN-3 entitlements depend on AAC §6.3's key store | MERGE SCC-002 + SCC-003 (O-1 only) | L |
| **02-03 → 09-06** | EXEC RT-11 follows CA §8.2's case list ("the consumer's list governs") | DEL-09-06 joins SCC-002 (O-1 only) | V |
| 01-04 → 02-01 | AAC maps WR spellings "one to one (WD §3.6)"; NIR content identity per WD §6.1 | inside SCC-002 | I |
| 03-01 → 02-01 | C's V-GR1 fixture is a run of WD-EX E1d | inside SCC-002 | P |
| 03-03 → 05-01 | ADAPTER's dispatch record "Mirrors LOOP §6.2" | inside SCC-002 | I |
| 04-02 → 02-01 | AS OV-7 shows WD's `governed` flag; WD §4.3.7 item rule | inside SCC-002 | I |
| 09-09 → 02-01 | XT uses "dispositions WD §4.3.4" | inside SCC-002 (O-1); no cycle (O-2…O-4) | I |

**G2 items confirmed as SCC-forming.**
- N08 (01-05 → 04-03): MERGE SCC-001 + 002 + 003 into 19 (O-1); 01-05 joins (O-2…O-4).
- N13 (09-07 → 09-11): NEW pair.
- N22 (02-01 → 01-04): V; inside SCC-002 (O-1).
- A2 and A3 ×5 (DEL-04-01 → 01-04, 02-01, 02-03, 03-01, 04-02, 05-01): DEL-04-01, 01-02 and 01-03 join (16 / 15 / 15 / 15).
- A7 (09-09 → 09-06): DEL-09-06 joins (O-1).

**Unclear SCC-forming pairs.**
- 01-01 → 01-04 and 01-01 → 03-03 (N27): MERGE into 19 (O-1); 16 (O-2…O-4).
- 01-03 → 02-03: 01-03 joins.
- 01-04 → 03-01: inside.
- 01-06 → 02-02 and 01-06 → 02-04: MERGE 002 + 003 (O-1).
- 04-03 → 01-04 (A1): inside.
- 04-03 → 09-06: 09-06 joins.
- 09-01 → 09-06 and 09-01 → 09-09 (EXP-R9; V): MERGE (O-1).
- 09-12 → 11-03: SCC-006 grows, or NEW {09-12, 11-03}.

### 5.2 Cumulative SCC sets

| Added to DAG-004 | O-1 | O-2 | O-3 | O-4 |
|---|---|---|---|---|
| Nothing | 6: 002 (13), 004 (3), 001, 003, 005, 006 | 4: 002 (12), 004, 005, 006 | 2: 002 (12), 004 | 2: 002 (12), 004 |
| The 24 confirmed G2 N items | 5: **19** {01-01…01-06, 02-01…02-04, 03-01…03-03, 04-02, 04-03, 05-01, 05-02, 09-01, 09-09}; 004; {09-07, 09-11}; 005; 006 | 5: **13** (002 + 01-05); 004; {09-07, 09-11}; 005; 006 | 3: 13; 004; {09-07, 09-11} | 3: 13; 004; {09-07, 09-11} |
| **All 62 dependencies** | 4: **26** {01-01…01-06, 02-01…02-04, 03-01…03-04, 04-01…04-03, 05-01, 05-02, 07-01, 07-02, 08-01, 08-02, 09-01, 09-06, 09-09}; {09-12, 10-02, 10-04}; {09-07, 09-11}; {11-01, 11-03} | 6: **16** {01-02…01-05, 02-01…02-04, 03-01…03-03, 04-01…04-03, 05-01, 05-02}; **{03-04, 09-06, 09-09}**; 004; {09-12, 10-02, 10-04}; {09-07, 09-11}; 006 | 5: 16; {03-04, 09-06, 09-09}; 004; {09-07, 09-11}; {09-12, 10-02} | 4: 16; {03-04, 09-06, 09-09}; 004; {09-07, 09-11} |
| 62 dependencies + 13 unclear | 3: 26; {09-12, 10-02, 10-04, 11-01, 11-03}; {09-07, 09-11} | 3: 25 (the 26 without 01-06); {09-12, 10-02, 10-04, 11-01, 11-03}; {09-07, 09-11} | 3: 25; {09-12, 10-02, 11-03}; {09-07, 09-11} | 3: 25; {09-07, 09-11}; {09-12, 11-03} |

Under O-1, SCC-004 (CASE-005) is drawn into the 26 by these paths:
- 09-09 → 09-06 (A7) → 03-04 (new, RELAY P8) → 07-01, 07-02 and 08-01 (admitted rows of DEL-03-04) → 08-01 → 05-01 (admitted) → SCC-002;
- 03-04 → 08-02 → 04-01 (N20) adds DEL-08-02.

Without A7, or without 09-06 → 03-04, SCC-004 stays separate. Under O-2…O-4 it stays separate in every row.

## 6. Cross-check of the open case analyses

These are the SCC-forming dependency and unclear pairs that touch each case's members, either at an endpoint or in the resulting component. Each case's "no new row" conclusion needs re-reading against them.

| Case (members) | Pairs flagged | Effect on the case's conclusion |
|---|---|---|
| **SCC-CASE-001** {01-01, 01-05} | Dependency N08 01-05 → 04-03. Unclear 01-01 → 01-04 (HOSTING U-20 / NIR answer paths) and 01-01 → 03-03 (N27) | Its analysis already treats N08 (§5, "N08, no moves" 19 members). The two unclear pairs are new to it. If either is registered, DEL-01-01 joins SCC-002 even with this case's move: O-2…O-4 give 16 with 01-01, 01-02, 01-03 and 01-05 |
| **SCC-CASE-002** (13 members) **and ACT51** (DEL-04-01) | **Dependencies:**<br>• new: 01-03 → 04-03; 01-04 → 02-01; 01-06 → 01-04 (L); 02-03 → 09-06 (V); 03-01 → 02-01; 03-03 → 05-01; 04-01 → 02-02, 03-02, 04-03; 04-02 → 02-01; 09-09 → 02-01<br>• G2 / §5 items: N08, N22; A2, A3 ×5; A7<br>**Unclear:** 01-01 → 01-04; 01-01 → 03-03; 01-03 → 02-03; 01-04 → 03-01; 01-06 → 02-02, 02-04; 04-03 → 01-04 (A1); 04-03 → 09-06; 09-01 → 09-09 | • **Membership.** DEL-01-03 joins through NPTD TA-4 (01-03 → 04-03), which no case lists.<br>• **ACT51.** Its §5.1 table covers grant, checkpoint and operation identity. RVG ACT-M1 adds RS, AAC and WR. G2b also finds **ACT §2.5 change-item content identity / P §9 (04-01 → 03-02)**, beyond P §3.3 as L, and **ACT §2.7 → LOOP DF-1/DF-3/DF-6 (04-01 → 05-01)**, beyond checkpoint state. Nine DEL-04-01 supplier pairs in all, each forming a 16 / 15 / 15 / 15 component alone.<br>• **Inside SCC-002.** The five new pairs (01-04 → 02-01, 03-01 → 02-01, 03-03 → 05-01, 04-02 → 02-01, 09-09 → 02-01) add I rows inside the component. They can raise the minimum cycle-closing set that the §23 tables report |
| **SCC-CASE-003** {01-06, 09-01} | Dependency 01-06 → 01-04 (L). Unclear 01-06 → 02-02, 01-06 → 02-04 (PKG bundle layout), 09-01 → 09-06, 09-01 → 09-09 (EXP-R9, V). Through N08 / N27, SCC-003 joins the 19 under O-1 | Its sufficiency note (l.203: "stays sufficient while N08, N26 and N27 are not registered uninverted") now also depends on 01-06 → 01-04 (O-1 only, being L) and on the EXP-R9 reading (O-1 only, being V) |
| **SCC-CASE-005** {07-01, 07-02, 08-01} | No pair alone. Cumulatively under O-1, A7 together with 09-06 → 03-04 merges SCC-004 into the 26 (§5.2) | "No new row" holds under O-2…O-4. Under O-1 it depends on A7 and on RELAY P8 (09-06 → 03-04) |
| **SCC-CASE-006** {10-02, 10-04} | **Dependency 09-12 → 10-02** (PV §3.5: `method_note` has exactly UC §5's fields) | **New to the case.** SCC-005 gains DEL-09-12 under O-1 and O-2, and a new {09-12, 10-02} forms under O-3 (SCC-005 itself leaves under O-3). No cycle under O-4 |
| **SCC-CASE-007** {11-01, 11-03} | Unclear 09-12 → 11-03 (PV's placeholder test "matches DEL-11-03's") | If it is registered: SCC-006 gains DEL-09-12 under O-1 and O-2, and {09-12, 11-03} forms under O-3 and O-4. With 09-12 → 10-02 also registered, SCC-005, SCC-006 and DEL-09-12 merge into 5 members (O-1, O-2) |
| **SCC-CANDIDATE-N13** {09-07, 09-11} | N13 itself | The other uses touching the pair are not SCC-forming: 09-07 → 02-01, 02-03, 03-01, 03-02, 04-01, 04-02, 04-03, 05-01, 05-02 (registered only as PKG-02…05 package rows, DEP-09-07-012…015); 09-11 → 01-04, 02-03, 04-01, 06-02; 09-10 → 09-07; 09-12 → 09-07. The candidate's conclusion is unaffected |

## 7. Limits

- **Sampling for "not a dependency".**
  - **Small pairs.** Every line of every candidate pair was ranked, use-verb lines first, and the top 4–9 were read. More were read wherever a use appeared.
  - **Large pairs.** For pairs with many uses (for example HOSTING → RECOVERY, 80; ACT → EXEC, 68), the remaining lines were not all read.
  - **Safeguard.** A pattern pass over every body line of the 251 not-dependency pairs looked for strong use phrases ("relies on", "mirrors", "follows", "adopts", "validates against", "in X's terms", "'s vocabulary/fields"). It returned 61 lines. All were re-read, and each is a receiver statement, a ruling or a cross-reference.
  - **Residual risk.** A dependency stated without a use verb in a large pair could still be missed. ACT shows that rule-bearing citations can sit in table cells.
- **Matched pairs** (§4.3) were not re-classified under GC-5. They carry register arcs, which G2 checked against interface tables, and their representative line is chosen automatically.
- **What was not scanned.**
  - Citations by rule id alone, without any abbreviation (for example "CAP-2", "HA-10", "SD-1"). Most such ids are prefixed by their owner's abbreviation in these Designs, but not all.
  - Observation records' internal text was scanned. Prototype code, fixtures and non-schema JSON were not.
- **Judgment calls in the classification.** The kind assignments and the runtime-value reading in §1 are this survey's application of GC-5 and G1 r3. Five calls in particular need review:
  - RELAY P8 (09-06 → 03-04) counted as a dependency, though the questions were relayed and answered;
  - XT's "standing uses … the contribution ladder" (A7) counted as a dependency, though both Designs call it a cross-reference;
  - EXP-R9 left unclear, as a receiver-conformance check;
  - NPTD TA-4 counted as a dependency, though NPTD §16.3 calls act records runtime values;
  - PKG's bundle layout left unclear.
- **Rulings not read at source:** R5-1, R4-14, R12-7, R17-9, R20-1, R20-11, R23-33, K-8 and K1-4. Where a not-dependency classification rests on them, it assumes, as the citing Designs say, that each carries the rule. R18-1 C-04 and R21-1 (HCG-A08) and R20-9 were checked at source.
- **Effects are per pair on DAG-004**, except §5.2. Minimum cycle-closing sets were not recomputed; the case agents hold those models.
