# App v4 — evidence inventory for the 60% position

- **What this is.** A source-cited inventory of where each of the 41
  deliverables stands, for HELP_HUMAN's owner-facing 60% position statement.
  It decides nothing, makes no design change and judges nothing on the
  owner's behalf. The criterion it is read against is
  `projects/chirality-app-v4/loop/LOOP_INIT.md` (§"Develop the detail
  appropriate to the phase", the paragraph beginning "The human assesses the
  60% position"): "developed design/interfaces and a route to completion for
  which further structural changes are no longer anticipated".
- **Author.** Type 2 TASK (Claude Opus 5.5), run
  `APP-V4-DESIGN-PASS-4-20261003`, dispatched by HELP_HUMAN. Read-only git;
  no network; this file is the only write.
- **State read.** Read at `161f8a0d0d` (branch `claude/app-v4-design-pass-4-t2`,
  2026-10-04). Version labels are taken from each file's "Contribution" line
  at that commit.
- **Refresh.** First written at `48df7404c7`. Refreshed at `161f8a0d0d` for
  the closeout commits `48df7404c7..161f8a0d0d`:
  - `18d6eae3e4`: O-C's pins and LHQ2-R2;
  - `821f236649`: EU-F3R2;
  - `9ba5dfe49c`: EU-F4R;
  - `158c0b2859`: EU-F3R3 and EU-F4R2;
  - `c4577c333a`, `a1734df11e`, `528536b668`, `161f8a0d0d`: the review
    confirmations.

  Only the rows for DEL-09-05, 09-07, 09-11, 09-12, 11-01, 11-02 and 11-03,
  and gaps G-12 and G-28, changed.
  - DEL-03-04's ACT re-pin was already in `48df7404c7`.
  - At the refresh, the working tree also held an uncommitted addition to
    `RUN/R23_RESOLUTIONS.md`: R23-54, which bears on G-24. It is outside the
    refreshed commit range and is not reflected here. G-24 stands as
    written at `161f8a0d0d`.

## How to read this

**Paths.** `E/` = `projects/chirality-app-v4/execution/`. A deliverable's
files are under `E/PKG-nn_…/1_Working/DEL-nn-mm_…/` (`Design/`,
`ScopeOfWork.md`, `Dependencies.csv`, `_STATUS.md`). Run folders:
`RUN/` = `E/_Coordination/AgentRuns/APP-V4-DESIGN-PASS-4-20261003/`;
`FI/`, `INT/`, `BA/`, `P2/`, `P3/`, `SCA2/`, `SCA3/` = the
`E/_Coordination/AgentRuns/` folders `APP-V4-FIRST-INCREMENT-20260928`,
`APP-V4-SWBPIPE-INTAKE-20260928`, `APP-V4-BASIS-ALIGN-20260928`,
`APP-V4-DESIGN-PASS-2-20260930`, `APP-V4-DESIGN-PASS-3-20261001`,
`APP-V4-SCA002-20260929`, `APP-V4-SCA003-20261002`.
`H4/` = `E/_DAG/DAG-004/HANDOFF_STATE.md`.

**Designed in.** FI = first increment (`FI/RECEIPT.md`), later revised by
INT (v0.6), P2 (v0.7–v0.8), P3 (v0.9) and P4 rows. P3 = design pass 3
(`P3/RECEIPT.md`). P4-T1 / P4-T2 = design pass 4 tranches 1 and 2
(`RUN/RECEIPT.md`, `RUN/DISPATCH.md`).

**Evidence standing codes.** **D** definition only. **F** fixture or
prototype evidence: a design's own checks passing on constructed inputs.
**O-sup** observed behaviour of the supplier (Codex App Server) at a named pin
on a local model; this is not App behaviour. **R** checks run against real
project records or the repository; this is not product behaviour. **No row
has observed App product behaviour.** Every Design file's status line reads
"not implemented" (or "not run on any candidate"), and no App candidate
exists. For example, `RUN/RECEIPT.md` §Limits: "Nothing is implemented,
built, signed or qualified. All evidence comes from fixtures and
prototypes."

**Open-matter categories.**
- (a) Decisions reserved to the person.
- (b) Items carried to the next ScopeOfWork or register amendment.
- (c) Ordinary design work remaining, with the agent or deliverable named.
- (d) External dependencies: SWBPIPE, PEC, Domains, the Codex supplier.

"Owner" means the person. Agents are named as agents (O-A…O-F, HELP_HUMAN).
**AIO** marks items the files assign to the "App implementation owner".
DECISION-L L-7 (`P3/OWNER_DECISIONS.md` L183) records "the App
implementation owner is the owner". R23-17 (`RUN/R23_RESOLUTIONS.md`),
however, treats such items in EXP as implementer choices that are "not owner
questions". Which reading applies to each AIO item is not recorded (Part C,
G-24).

**Recurring items, used by tag in Part A.**

| Tag | Item | Owner as recorded | Point of need | Source |
|---|---|---|---|---|
| HJ | SWBPIPE host joins deferred: no join, witness or adoption; SWBPIPE answers are "data, not commitments" | Owner (DECISION-3); SWBPIPE owner (DEP-001) | When the owner resumes UI-SUCCESSOR | `INT/RECEIPT.md`; `RELAY_ANSWERS_SWBPIPE.md` header; `Open_Issues.csv` OI-021 |
| OI21 | First connected operation, autonomy and environment unbound; operation-specific reserved additions | Owner via the outside SWB session, with the App/shared owner | Before connected-activity ScopeOfWork and execution | `Open_Issues.csv` OI-021 |
| PL | OI-013/OI-014 placement of loop, panel and shared parts | "Shared contract owner with SWB implementation owner"; "App/shared contract owners" (role names; no person or agent mapped) | Before structural or production allocation | `Open_Issues.csv` OI-013, OI-014 |
| PD | OI-008 App process division | AIO, "(phase review)" | Before architecture production contracts | e.g. RECOVERY U-R8, AAC U-AAC-1, NPTD U-P7 |
| CV | Consequence vocabulary (ACT U-02), PROPOSED for the owner's phase review | Owner at the phase review; DEL-04-01 with the host policy owner | Before class assignment in DEL-03-01 | ACT §8.5, U-02 |
| GP | D6: governance-phase holds. Closed for Phase 1; re-opens only when the owner takes up the governance phase | Owner (DECISION-4 D4-1) | When a workflow needs enforced checkpoints | EXEC U-E1; GUIDE §2.13 |
| A12 | SCA-V4-003 Q-9: the A12 destination-grant mapping rows are held | Owner, at the next amendment | Before LHQ-23's evidence expectations are fixed | `SCA3/OWNER_DECISIONS.md` Q-9; `SCA3/AMENDMENT_PACKET/LEDGER.md` |
| CID | Content-identity algorithm (HOSTING U-08 / RS U-04); sha-256 is a TEST VALUE | AIO with DEL-04-03 | Before records are relied on | HOSTING U-08; FR §11; DV §9 |
| CX | Codex supplier: qualification pin chosen at candidate build (R23-22); sign-in and API key not observed (L-6 "not now"; OI-010); delegation on the stock route not provoked (OBS-2 O-4) | AIO; owner for any credential observation | Before qualification | R23-22; ACCESS U-A2; OBS_2 result line |

## Part A — per deliverable (41 rows)

Columns: (1) ID and name · (2) Design artifacts and version (HEAD) · (3)
Designed in · (4) Review standing · (5) Interfaces: main joins and whether
each was checked against the other side's Design text · (6) Evidence · (7)
Open matters, by category a/b/c/d · (8) Structural-change risk.

Supplier and consumer sets come from DAG-004 (`E/_DAG/DAG-004/DependencyEdges.csv`
and `CandidateEdges.csv`, computed by script; * = held arc).

### PKG-01 Native App and third-party harness integration

| (1) | (2) | (3) | (4) | (5) | (6) | (7) | (8) |
|---|---|---|---|---|---|---|---|
| **DEL-01-01** Stock Codex hosting and supplier contract | `HOSTING_BOUNDARY.md` HOSTING-BOUNDARY-v0.9; `PIN_SPIKE_0.158.0.md` PIN-SPIKE-v0.1; `OBS_1/2/3_0.158.0.md` (dated records); `VERSION_ADVANCE_0.160.0.md` VERSION-ADVANCE-0.160.0-v0.1; 3 schemas; `generated/0.158.0/`; prototype | FI → P3 (v0.9). VA in P4 (node VC) | v0.9: `P3/reviews/V21-B` → V21b-B MERGE AS DRAFTS; `P3/reviews/V22` MERGE. VA: ruled R23-22; inside P1 MERGE (`RUN/reviews/P1_PREMERGE.md`) | Supplies 01-02, 01-03, 01-04, 01-06, 02-01, 02-03, 02-04, 03-03, 03-04, 04-03, 06-01, 09-01, 09-02, 09-06; SCC-001 with 01-05*. Checked: V1-A/V1-C (FI, v0.1); `P2/comparisons/V18-2/3/4` (WD, ADAPTER and EXEC joins, v0.8); `P3/F/F0_JOINS.md` (44 rows against the pass-3 files); V21-B. **One-sided now:** PRC relies on App-origin reads (R23-45, R23-50, R23-53) that HOSTING §6.8 still lists as "not observed". The receiver row and the "no turn = no items" note are carried to HOSTING's next revision (R23-37.2, R23-45.2) | O-sup (0.158.0 OBS-1/1b/2/3; 0.160.0 VA) + F (supplier double; boundary model) | (a) U-18 start-up fetch acceptability (owner with DEL-01-05). (c) AIO: U-01 qualification pin, U-02 = PD, U-05, U-06, U-07, U-12, U-13, U-15, U-17, U-20, U-26; U-09 and U-16 with DEL-01-02; U-27 with DEL-04-03; HOSTING §UNRESOLVED. Next-revision items: R23-37.2, R23-45.2, R23-30.1 (Root citations), R23-22.3 (Δ1/Δ2 notes). (d) CX; U-19 unobserved live behaviours; U-21 supplier "experimental" label | None recorded for its own scope. Guard: any reverse row would merge SCCs (H4 "Standing note: DEL-01-01") |
| **DEL-01-02** Durable execution and request recovery | `EXECUTION_AND_RECOVERY.md` RECOVERY-v0.2; 3 schemas + examples; prototype | P3 | `P3/reviews/V21-A` → V21b-A MERGE AS DRAFTS; V22 MERGE | Suppliers 01-01, 04-01. Consumers 01-03, 01-04, 02-02 (NR-04), 02-03 (NR-01), 03-03 (NR-02), 04-03, 09-02. Checked: F0 (D1 joins; P3); V21-A/V21-B (joins with the first-increment files). NR-0x rows are TBD/PENDING (H4). **Pending:** R23-37.2 (a thread with no turn must read as having no items) is not yet in RECOVERY | F + O-sup (OBS-2 O-1…O-3, O-5…O-7) | (c) U-R2, U-R3 (with the owner for privacy), U-R7, U-R12 (App execution/recovery owner: role); AIO U-R4 numbers; U-R8 = PD. (d) U-R1: OBS-2 gaps (child interrupt, shared session store) | None recorded |
| **DEL-01-03** Native plans, tools and delegation views | `NATIVE_PLANS_TOOLS_DELEGATION.md` NPTD-v0.2; 3 schemas; prototype | P3 | V21-A → V21b-A MERGE AS DRAFTS; V22 MERGE | Suppliers 01-01, 01-02. Consumers 01-04 (NR-05), 02-02, 06-01, 09-02, 09-05. Checked: F0; V21-A; FR-v0.1 consumes the §7.7 export as is (FR §7), reviewed in RV-E2. S1-A S-3 (`RUN/SURVEY/S1-A.md` §3.2: "the delegation export may be too narrow"): no ruling located. R23-37.2 pending here too | F + O-sup (OBS-2/OBS-3 plan mode) | (a) U-P1 checklist surface (owner as AIO, at a version advance); U-P7 = PD. (c) U-P3 with DEL-02-04; U-P6 = CID. (d) U-P4, U-P8, U-P9: later observations | None recorded. Register: DAG-004 source drift on 2 files (TargetLocation repair; Part B) |
| **DEL-01-04** Native requests, outcomes and attachments | `APP_ACT_CONTROL.md` AAC-v0.3; `NATIVE_INTERACTION_RECEIVING.md` NIR-v0.3; 5 schemas + examples; prototype | P3; A16 rows and NIR Δ3 in P4-T1 | v0.2: V21-A → V21b-A; V22. v0.3 rows: `RUN/reviews/RV-E1.md` CONFIRMED READY; P1 MERGE | Suppliers 01-01, 01-02, 01-03 (NR-05), 01-05 (NR-07), 04-01; held 02-02*, 02-03*, 02-04*, 04-02*, 04-03* (SCC-002). Consumer 09-02. Checked: F0; V21-A; early path AAC → RS → decision view → readers (`RUN/E/RR-E`, `RR-F`, 9/9); C1 §3 "NIR-v0.3 consumers", "AAC-v0.3 consumers": Holds | F (`run_cases.py` 159/0; C1 §4) | (c) U-AAC-3 SEAL-2 (AIO with DEL-04-03); U-AAC-5 (integrator); U-NIR-1, U-NIR-2, U-NIR-4, U-NIR-10 (AIO); U-AAC-1 = PD. (b) U-AAC-7 is closed by SCA-V4-003 (OUT-005 added; `SCA3/RECEIPT.md`). (a)/(d) TBD-001 = OI21; TBD-004 = CX | Proposed new arc DEL-01-04 → DEL-01-06 (SEAL-2 relies on the signed App), carried (`PKG §13`). SCC-neutral by `dag_reach.py` (run for this inventory); it would need a DAG successor |
| **DEL-01-05** Native OAuth sign-in, API-key and local-provider access | `ACCOUNT_AND_PROVIDER_ACCESS.md` ACCESS-v0.2; `ACCOUNT_HOME_DECISION_RECORD.md` ACCOUNT-HOME-RECORD-v0.2; 4 schemas; prototype | P3; §13 row by C2 (P4) | V21-A → V21b-A; V22; P1 (C2 row) | SCC-001 with 01-01*. Consumers 01-04 (NR-07), 05-01, 09-02. Checked: F0; V21-A. **Register conflict:** V25 m-1, DEL-05-01 → DEL-01-05 (H4 "V25 m-1"). U-A9 is answered by R23-30.2 but carried to ACCESS's next revision | F + O-sup (OBS-2 O-6 home mechanism, no credential; OB-9 start-up traffic) | (a) U-A2 sign-in/API-key observation (owner: "not now", L-6); OI-010. (c) AIO: U-A4, U-A5, U-A6; U-A8 (DEL-04-03 with integrator); U-A10. (d) U-A7, U-A13, U-A14, U-A15, U-R3: later observations | V25 m-1: reconciling it may turn the arc into a non-requirement, "a departure for a later successor" (H4) |
| **DEL-01-06** macOS packaging and distribution evidence | `PACKAGING_AND_DISTRIBUTION.md` PKG-v0.2; identity and terms schemas + examples; prototype | P4-T1 (O-B) | `RUN/reviews/RV2-PKG-U2.md` READY (repairs and PKG-R12…R14 confirmed); P1 MERGE | Suppliers 01-01; SCC-003 with 09-01*. Consumer 09-02. Checked: C1 §3 "EXP-v0.2 → PKG" Holds; "DEL-09-02 → DEL-01-06" Holds. Seams to 02-02, 02-04, 01-04 have **no rows** (PKG §4.2 I-4; §13) | F (`check_pkg.py` 66/0 with the vendor tree) + O-sup (`codesign -d` over the 0.160.0 vendor tree) | (a) Signing with the owner's Apple account when a package is made (R23-13.2); U-PKG-7 = OI-007 (owner and supplier). (c) U-PKG-1 (confirm G-2/G-5/G-7 at the first package); U-PKG-2, U-PKG-4, U-PKG-5 (AIO); U-PKG-8. (b) PKG §13: three bundle-seam rows; the counterpart of DEP-09-02-014; CLM-002 and TBD-003 wording; OI-011 record (R23-26). (d) U-PKG-6: OI-011's SWB part waits for HJ | **Three new arcs proposed** (02-02, 02-04, 01-04 → 01-06; PKG §13; R23-2). SCC-neutral by the reach script; an added-arc departure, so a DAG successor (DA §5 item 1). SCC-003 treatment is unruled (CASE-003 R1 recommended; R2 merge-group is a conditional alternative) |

### PKG-02 Workflow and role portability

| (1) | (2) | (3) | (4) | (5) | (6) | (7) | (8) |
|---|---|---|---|---|---|---|---|
| **DEL-02-01** Portable workflow contract and shared allocation | `WORKFLOW_DECLARATION.md` WD-v0.9; `EXAMPLES.md` WD-EX-v0.9; schema + examples; prototype | FI → P3 | V21-B → V21b-B MERGE AS DRAFTS; V22 MERGE | Suppliers 01-01, 04-01; held with 02-03, 03-01, 03-02, 04-03, 05-01, 05-02 (SCC-002). Consumers include 03-04, 08-02, 09-02, 09-06, 10-03. Checked: V1-C; `P2/comparisons/V18-2` (14 joins; 3 MAJOR at v0.8, ruled in `P2/R14_RESOLUTIONS.md` R14-3/5/6 and applied at nodes RP-1…RP-4); F0 (13 rows). **One-sided:** U-17 states every §9 row's consumer confirmation as "None"; the consumers' own files are "a record, not an owner confirmation" (WD §12 U-17). U-01 carriage stays PROPOSED until DEL-02-03/05-01/05-02 "confirm or object" | F | (c) U-36 declared chaining: "later work of this deliverable"; U-01, U-02, U-08 PROPOSED; U-03 (with DEL-04-03) = CID; U-17 confirmations (R23-31.8: for deliverable owners). (a) U-16 = OI-003; U-14 = OI-018 for hosts; U-12/U-13 = PL. (d) U-05b, U-09, U-19, U-29, U-35 (SWBPIPE owner decisions; HJ) | None recorded. Mirror maturity difference DEL-08-02 → DEL-02-01 (H4) |
| **DEL-02-02** Workflow-making workspace and registration | `WORKSPACE_AND_REGISTRATION.md` WR-v0.2; schema + examples; prototype | P3 | V21-A → V21b-A; V22 | Suppliers 01-02 (NR-04), 01-03, 04-01; held 01-04*, 02-01*, 02-03*, 04-03*. Consumers 09-02, 09-06. Checked: F0; V21-A. U-WR-11 vocabulary shared with DEL-01-04 is open for "the next comparison". **Pending:** R23-37.2 not yet applied | F + O-sup (OBS-3 per-turn supply) | (c) Integrator: U-WR-7, U-WR-10, U-WR-12, U-WR-13, U-WR-18; U-WR-1 = CID; U-WR-3 (DEL-04-03); U-WR-2 = PD; U-WR-8 = PL. (d) U-WR-14, U-WR-15, U-WR-19: later observations. U-WR-5: host listing (HJ) | Proposed new arc DEL-02-02 → DEL-01-06 (PKG §13). SCC-neutral; needs a successor |
| **DEL-02-03** Workflow execution compatibility and round-trip support | `EXECUTION_COMPATIBILITY.md` EXEC-v0.7; checkpoint schema proposed-0.7 (A16, `decisionPackageFile`); compatibility-report schema; prototype | FI → P3; schema rows in P4-T1 | V21-B → V21b-B; V22; schema rows RV-E1 READY; P1 | Suppliers 01-01, 01-02 (NR-01), 04-01; held with 01-04 (X-1, narrow), 02-01, 02-02, 03-01…03-03, 04-02, 04-03, 05-01. Consumers include 03-04, 09-02, 09-06, 10-03. Checked: V1-A/C; V18-2/3/4; F0 (20 rows); RV-E1 (A16 package-file shape, R23-24); early path. C1 §3 found and repaired a broken DEL-09-06 W14 rehearsal caused by this file's prototype (44/0 after) | F (`run_all.py` 126/0) | (a) GP (U-E1, U-E23). (c) U-E16 (with DEL-04-03); U-E19 host precedence; U-E2 = PL. (d) U-E9, U-E11…U-E15, U-E17, U-E18, U-E25, U-E26 (HJ, SWBPIPE answers) | None recorded. Reach-check note: a reliance row DEL-09-01 → DEL-01-04 or → DEL-04-03 would close a cycle (EXP §14 O-4) |
| **DEL-02-04** Additive role selection and supply | `ROLE_SUPPLY.md` ROLE-v0.2; 2 schemas + examples; prototype | P3 | V21-A → V21b-A; V22 | Suppliers 01-01; held 02-01*. Consumers 03-04, 10-03, 11-02; held 01-04*, 04-03*. Checked: F0; V21-A. DEL-11-02 AA I-2: supplier-side row only (R22-7-open) | F + O-sup (K-10 limit observed through an adapter) | (c) U-R3 child-role carrier (AIO; a later observation); U-R4; U-R9, U-R11 (role-guidance owner); U-R10 (integrator); U-R1 = CID; U-R5 = PD; U-R6 = PL. (a) U-R8 = OI-024 adoption. (d) U-R13, U-R14 observations; U-R7 = HJ | Proposed new arc DEL-02-04 → DEL-01-06 (PKG §13). SCC-neutral; needs a successor |

### PKG-03 Host capability and operation contracts

| (1) | (2) | (3) | (4) | (5) | (6) | (7) | (8) |
|---|---|---|---|---|---|---|---|
| **DEL-03-01** Capability catalog and read-basis contract | `CATALOG_AND_READ_BASIS.md` C-v0.8; catalog, read-result and edition-change schemas + examples; prototype; custody of FX-PIPE-01 and SH-1 (SCA3 Q-8) | FI → P2 (v0.8) | Last content review in P2: `P2/reviews/V19-A`/V19b MERGE AS DRAFTS; V20-A HOLD → RV20 → V20b MERGE. Not in V21-B's scope | Held with 02-01, 02-03, 03-02, 04-02, 04-03, 05-01, 05-02, 09-09 (SCC-002). Admitted supplier 04-01. Checked: V1-B; V18-3/4 (with SH-1). **One-sided:** all host-side items U-C2…U-C15 (HJ). FX-PIPE-01 has not yet adopted LHQ's L-LHQ-1/2 (R23-16) | F (SH-1 simulated host) | (a) OI-003 (owner with host contract owner); CV; S-01-4 held (Q-7). (c) U-C1 serialization etc. (capability-contract owner: role); R23-16 adoption. (d) U-C2…U-C7, U-C9…U-C13, U-C15: host owner / SWBPIPE (HJ) | **S-01-4 (held at SCA-V4-003 Q-7)** would change protected AC-004/REQ-004 (`SCA3/AMENDMENT_PACKET/LEDGER.md` L188). That is a ScopeOfWork obligation change, pending a host join |
| **DEL-03-02** Proposal, validation and outcome contract | `PROPOSAL_LIFECYCLE_AND_OUTCOMES.md` P-v0.8; proposal and proposal-state schemas; prototype | FI → P2 | As DEL-03-01 (V19-A/V19b; V20b) | Held with 02-01, 03-01, 04-02 and others (SCC-002); admitted 04-01. Checked: V1-B; V18-2 (M-2 token `applied_receipt`, ruled R14-6); V18-3/4. **One-sided:** U-P2…U-P10 on the host (HJ) | F | (a) OI-003, CV. (c) U-P1 identity representation (narrowed). (d) U-P2…U-P8, U-P10 (host owner / SWBPIPE) | None recorded |
| **DEL-03-03** Local external-agent receiving adapter | `ADAPTER_ENABLEMENT_AND_RECEIVING.md` ADAPTER-v0.7; channel-status, checkpoint-observation and dispatch-record schemas; prototype | FI → P3 | V21-B → V21b-B; V22 | Suppliers 01-01, 01-02 (NR-02, PENDING), 04-01; held SCC-002. Consumers 03-04, 09-06; held 02-03*, 04-03*, 09-09*. Checked: V18-3 (SH-1 bridge); F0. Missing DOWNSTREAM mirror to DEL-03-04 (ADAPTER UNRESOLVED, F-11) | F + O-sup (OBS-1/1b: MCP and CLI paths) | (c) TBD-007 OC-1…OC-12 ("App external-host integration owner with external host owner": roles). (a) R8-Q4b launch variable as A13 evidence (owner, deferred); OI-003; GP. (d) SQ-28, SQ-08, SQ-13, SQ-12 (SWBPIPE owner decisions; HJ) | None recorded |
| **DEL-03-04** Host boundary and integration guide | `HOST_INTEGRATION_GUIDE.md` GUIDE-v0.7 (ACT row re-pinned to ACT-POLICY-v0.11 at `48df7404c7`; landed before this refresh) | FI → P3 (v0.6); v0.7 by C2 (P4-T1) | v0.6 in V21-B → V21b-B; v0.7 inside P1 MERGE; the T2 re-pin row is not yet reviewed | Consumes 18 deliverables (all admitted). Pin check 25/25 after O-A's re-pin (`RUN/OWNERS/O-A.md` "CURRENT"). The guide says the check "binds the table to those bytes only; it is not a review of their content" (GUIDE §4.5). **Unchecked against tranche 2:** M10.1 and M10.2 cite "accepted SoW meaning (outside undertaking, D1)", and G-2 reads "PEC and Domains receiving not started" (GUIDE §4.4). A grep finds 0 references to PRC, CFB, DRC or RTD, although DAG-004 admits 03-04 → 07-01, 07-02, 08-01, 08-02 | D | (a) OI21, OI-003, GP, R8-Q4b; TBD-007…009 = OI-022, OI-023, OI-026. (c) M10.1/M10.2 "owner-open" to drop at the next revision (R23-34.8). (d) SWBPIPE owner decisions (ANS §2); relay of the DECISION-5 host obligations (HJ) | None recorded |

### PKG-04 Human acts, autonomy and run evidence

| (1) | (2) | (3) | (4) | (5) | (6) | (7) | (8) |
|---|---|---|---|---|---|---|---|
| **DEL-04-01** Operation-policy and human-act distinctions | `ACT_AND_POLICY_CONTRACT.md` ACT-POLICY-v0.11; policy-class schema + examples; prototype | FI → P3; A16 (v0.10) in P4-T1; §10.3 row (v0.11) in P4-T2 | v0.9: V21-B; v0.10: RV-E1 CONFIRMED READY; P1. v0.11: "covered by the pre-merge review" (`RUN/DISPATCH.md`), which is **not yet recorded** | No suppliers. 20 admitted consumers. Checked: V1-A (8 receivers, v0.1); V18-1; RV-E1 (A16 rows). F-RA1: the joins to DEL-10-03 are recorded on the consumer side only (RA §3.4) | F (`validate_policy.py` 6 PASS) | (a) CV (§8.5: four questions for the owner's phase review); U-16 = R8-Q4b; A12 (SC2-04-01-2 held); U-05 actual person grants (the person, at VER). (b) REQ-002 naming A16 (R23-18.4); F-RA1 mirror row. (c) U-12 = PL. (d) U-04, U-06, U-15 (SWBPIPE) | **SC2-04-01-2 (held, Q-9)** would change AC-007 and VER-007 and add an AX, with a new EXTERNAL constraint row R2-04-01-b (`LEDGER.md` L225, L427). An obligation change, pending the owner's A12 confirmation |
| **DEL-04-02** Visible autonomy and result standing | `AUTONOMY_AND_STANDING_EXCHANGE.md` AS-v0.9; settings-in schema + examples; prototype | FI → P3 | V21-B → V21b-B; V22 | Admitted 04-01; held with 02-03, 03-01, 03-02, 04-03, 05-01 (SCC-002); new held NR-08 from 01-04. Checked: V1-B; V18-1. **One-sided:** host items U-04…U-07, U-12 (HJ) | F | (a) CV; GP; OI21 (U-01). (c) U-20 grant display for a host without grants (DEL-04-02 with integrator; PROPOSED); U-08 = PL. (d) U-04…U-07, U-12, U-18 (host / SWBPIPE) | None recorded |
| **DEL-04-03** Content-bound decisions and compact run records | `RECORD_SEMANTICS.md` RS-v0.10; `RS_RECORD.schema.json` format 0.1 + example sets; prototype | FI → P3; A16 rows in P4-T1 | v0.9: V21-B; v0.10: RV-E1 CONFIRMED READY; P1 | Supplies 06-01, 06-02, 09-02, 09-05, 09-06, 09-11, 10-03 and others; SCC-002 hub (degree 29, H4). Checked: V1-A/B; V18-1, V18-4; V18-2 M-3 (origin enum, ruled R14-3); F0; the early path validated the A16 record against the schema (RV-E1). S1-C S-2: who writes a host-agent run record depends on PL | F (`run_prototype.py` 67 PASS) | (c) U-04 serialization and identity (= CID); U-05 App record location (with OI-014 owners); U-32 SEAL-2 (AIO); U-33 account email or digest (with integrator; owner privacy review). (a) GP; CV. (d) U-06, U-09, U-11, U-12, U-14, U-15, U-19, U-21, U-27, U-29 (host / SWBPIPE) | **S1-C S-2** (`RUN/SURVEY/S1-C.md` §D2): if the loop is shipped as a shared component (PL open), RS §3's producer column and LOOP's mapping move. Not ruled |

### PKG-05 Embedded-host receiving integration

| (1) | (2) | (3) | (4) | (5) | (6) | (7) | (8) |
|---|---|---|---|---|---|---|---|
| **DEL-05-01** Minimal-loop and model receiving contract | `LOOP_RECEIVING_CONTRACT.md` LOOP-v0.9; destination-request and tool-call schemas; prototype | FI → P3 | V21-B → V21b-B; V22 | Admitted 01-05 (V25 m-1 conflict), 04-01; held SCC-002. Consumers 03-04, 08-01, 09-06; held 02-01*, 02-03*, 04-02*, 04-03*, 05-02*, 09-09*. Checked: V1-C; V18-3; LOOP/PANEL pair check (`P2/reviews/V20-A`, node H). **One-sided:** host Q-1…Q-7 answered, but not agreed (HJ). F-RA1 | F + O-sup (OBS-1 Chat Completions stream shapes) | (a) R-OPEN-1 quantitative responsiveness ("Owner, if wanted"); GP; network-destination governance phase (owner). (c) "Hold machine confirmation (EXEC-v0.5 §4)": DEL-02-03 "at the next integration review", still listed. (d) DEP-05-01-024 model interface ("UNKNOWN supplier"); DEP-001; seat mapping U-09 | None recorded beyond PL (S1-C S-2) |
| **DEL-05-02** Host panel and shared interaction receiving | `PANEL_RECEIVING_CONTRACT.md` PANEL-v0.9 | FI → P3 | V21-B → V21b-B; V22 | Admitted 04-01; held SCC-002. Consumers 03-04, 09-06. Checked: V1-C; V18-3; V20-A pair check. F-RA1 (no SoW receiver or mirror for DEL-10-03). §3.8 network-destination surfaces are not named by the ScopeOfWork (F-12) | F | (a) F-12 scope of §3.8 (owner, at the next amendment or the phase review); A12 (S-0502-1 held); GP. (c) PN-5 grant display (integrator). (d) DEP-001 Q-1…Q-9; DEP-05-02-017 actual human acts (the person at execution) | **S-0502-1 (held, Q-9):** option A would change CLM-002 and OUT-001 (`LEDGER.md` L256). An obligation change; option B (no change) stands meanwhile |

### PKG-06 File-based fleet coordination

| (1) | (2) | (3) | (4) | (5) | (6) | (7) | (8) |
|---|---|---|---|---|---|---|---|
| **DEL-06-01** Bounded delegation and current work-graph records | `FLEET_RECORDS.md` FR-v0.1 (RF-5a in place, R23-39; claim-connector check FV10-R9); prototype `run_fleet.py`; fixture FX-FL1 | P4-T1 (O-A); RF-5a in P4-T2 | `RUN/reviews/RV-E2.md` READY; `RV2-FV10.md` READY (RF-5a, FV10-R7/R8); P1 (T1). The FV10-R9 check (46/46) is "covered by the pre-merge review": not yet recorded | Consumes 01-01, 01-03 (§7.7 export), 04-03, 07-01 (all admitted; FR §7). Supplies 06-02, 09-05. Checked: early path (RR-E/RR-F); RV2-FV10 against DEL-07-02's CS-R1 with vendored inputs (R23-44). Mirror maturity difference DEP-06-01-013 (H4) | F (`run_fleet.py` 46/46 per DISPATCH) | (a) PD ("Owner, at the phase review", FR §11). (c) AS-1 guidance text (O-A with DEL-02-04); CID. (d) OI-022 PEC; delegation on a stock route unobserved (CX) | None recorded. S1-A S-2/S-6 (an SCC would form if DEL-04-03 consumed PKG-06) were avoided by R23-8/R23-2 |
| **DEL-06-02** Return, waiting and human-decision workspace | `DECISION_VIEW.md` DV-v0.1; `FLEET_VIEWS.md` FV-v0.1 (FV-10 connector waiting cause added) | P4-T1; FV-10 in P4-T2 | RV-E1 (DV) and RV-E2 READY; RV2-FV10 READY; P1 (T1) | Consumes 04-01, 04-03, 06-01, 07-02. Supplies 09-05 (C1 §3 "DEL-09-05 RW-1 → DEL-06-02 FV-4a": Holds). The package reaches the act control as a runtime value, with no row (R23-2) | F (`run_views.py` 36/36 per DISPATCH) | (c) CID. Layout and notification not designed (OI-006, no owner) | None recorded |

### PKG-07 PEC receiving and connector fallback

| (1) | (2) | (3) | (4) | (5) | (6) | (7) | (8) |
|---|---|---|---|---|---|---|---|
| **DEL-07-01** PEC first-consumer contract and adoption evidence | `PEC_RECEIVING.md` PRC-v0.4; receiving-record schema | P4-T2 (O-D, EU-D1) | `RUN/reviews/RV2-EUD1.md` READY (PRC-v0.1…v0.3 and the R23-52/P-H1d round confirmed) | SCC-004 with 07-02*. Consumers 03-04, 06-01, 09-10. **PEC side unchecked:** "Agreement of §2's questions and §3's mapping" waits on the PEC owner (PRC §10). HOSTING §6.8 receiver row: see DEL-01-01 | F + O-sup (P-H1b/c/d: App-origin `mcpServer/tool/call` at 0.158.0 with the MCP double; R23-50, R23-53) | (c) Further probe for a later request in the same turn or after compaction (O-D, before reliance); release-level adoption (App receiving owner, after a qualified release). (d) PEC tool representation and operations (PEC owner, EXTERNAL); OI-022 | None recorded. S2-D S-1 avoided by H-1 (R23-34.3) |
| **DEL-07-02** Connector limitation and source-file recovery paths | `CONNECTOR_FALLBACK.md` CFB-v0.2 (label covers several byte states; cite by sha256, R23-52.3); standing and route-account schemas | P4-T2 (EU-D1) | RV2-EUD1 READY | SCC-004 with 07-01*, 08-01*. Consumers 03-04, 06-02 (FV-10), 09-10. Checked: RV2-EUD1 cross-owner EUD1-R1 ruled R23-40; RV2-FV10 checked FV against CS-R1 | F (`run_d.py` 297/297; isolated reader RR-EUD1 46/46 after R23-45.1) | (c) Placement of route accounts (O-D with DEL-06-01). (d) OI-022 terms (DEL-07-01 with PEC owner); OI-023 terms (DEL-08-01) | None recorded. S2-D S-6 cycle guards: rows to PKG-06 would form SCCs; H-6 keeps them as files |

### PKG-08 Domains research receiving

| (1) | (2) | (3) | (4) | (5) | (6) | (7) | (8) |
|---|---|---|---|---|---|---|---|
| **DEL-08-01** Domains query, admission and freshness contract | `DOMAINS_RECEIVING.md` DRC-v0.1; receiving-record schema | P4-T2 (EU-D1) | RV2-EUD1 READY (DRC-v0.1 in the reviewed unit) | Admitted supplier 05-01; SCC-004 with 07-02*. Consumers 03-04, 08-02 (DEP-08-02-005), 09-10. **Domains side: no provider exists**; every input is invented (DRC status) | F | (a) OI-026 provider allocation; starting the Domains-enabled increment; any relaxation of V4-HOST-02 (person's acts, R23-34 preamble; DRC §7). (c) **§6–§8 are "outline"** (DRC header). (d) DEP-003 Domains; admitting party "Open" | None recorded. S2-D S-4 (Domains tool class) not opened (R23-34.5) |
| **DEL-08-02** Later research-to-design receiving activity | `RESEARCH_TO_DESIGN.md` RTD-v0.2 | P4-T2 (O-D) | `RUN/reviews/RV2-RTD1.md` READY (RTD-v0.2 confirmed) | Admitted 02-01, 08-01. Consumer 03-04. Suppliers pinned by sha256 and checked before use (RTD1-R1). Mirror maturity difference DEP-08-02-006 (H4) | F (`check_rtd.py` 19/19) | (b) CLM-006, TBD-003, REQ-005, AC-006, VER-005 OI-001/002 wording (RTD §10). (c) Shared rows for the candidate-approval act in ACT, RS, CE, GUIDE and WD (their owners, when the Domains increment is selected); RTD1-R2, RTD1-R3 notes. (d) HQ-1…HQ-6 (SWBPIPE via the person; HJ) | **H-4/S-5:** a new candidate-approval act's rows go into five shared files when the Domains increment is selected (R23-34.4; A16 precedent: "rows, not a restructure") |

### PKG-09 Candidate examination and connected journeys

| (1) | (2) | (3) | (4) | (5) | (6) | (7) | (8) |
|---|---|---|---|---|---|---|---|
| **DEL-09-01** Candidate examination infrastructure and evidence protocol | `EXAMINATION_PROTOCOL.md` EXP-v0.2; 3 record schemas; prototype | P4-T1 (O-B) | `RUN/reviews/RV-EXP-U1.md` CONFIRMED READY; U-EXP-1 closure confirmed by P1 (P1-F1) | Admitted 01-01 (maps to HOSTING §9.3; R23-1); SCC-003 with 01-06*. Consumers 09-02, 09-05, 09-06, 09-07, 09-09, 09-10, 09-11, 09-12. Checked: C1 §3 (EXP → DOS, DAC, PKG, SQ: Holds). **Mismatch carried:** DEL-09-12 does not use `activity: validation` (PV1-R8; U-PV-4). The O-3 spelling `not-run`/`not_run` is mapped, not unified | F (`check_exp.py` 77/0) | (a) U-EXP-6 = OI-016. (c) U-EXP-2 runner names (implementer, R23-17); U-EXP-5 waits for DEL-01-06's package. (b) O-1 register statement (DEP-09-01-019); U-PV-4 at EXP's next revision. (d) U-EXP-7 (OI-003, OI-021, OI-023/026) | S2-F S-F3: "relaxing a required field" in EXP for validation records could be a check change (`RUN/SURVEY/S2-F.md` E4). Carried, not ruled |
| **DEL-09-02** Standalone App candidate qualification | `STANDALONE_QUALIFICATION.md` SQ-v0.2 (65 supplier cases; stimuli ST-1…ST-5) | P4-T1 (O-B) | `RUN/reviews/RV2-SQ-U3.md` READY; P1 | 12 admitted suppliers (01-01…01-06, 02-01…02-03, 04-01, 04-03, 09-01). Consumer 11-03. Checked: C1 §3 "EXP → SQ" (29/29 citations resolve); SQ pins RECOVERY, NPTD, WD, WR, HOSTING, EXP (C1 §1); `check_sq.py` checks 65 supplier-case citations. Under R23-33, SQ `candidate` maps to EXP | F (`check_sq.py` 114/0) | (b) SQ §11: TBD-002 (OI-009, ASC-ISS-002), TBD-001, TBD-003, CLM-001, REQ-006 wording; counterparts for DEP-09-02-014 and -018. (c) U-SQ-2 model choice (implementer; a download needs the owner's yes); U-SQ-3; U-SQ-5 (DEL-01-03/01-01). (d) U-SQ-6 real Codex lost-acknowledgment capture before RUN-A (DEL-01-01 with DEL-01-02); U-SQ-4 = OI-010 | None recorded |
| **DEL-09-05** Fleet coordination and longer-work recovery witness | `DECISION_ATTRIBUTION_CASE.md` DAC-v0.1 (`8810b957…`; closeout pins at `18d6eae3e4`) | P4-T1 (O-C, early path EP-05) | `RUN/reviews/RV-EP.md` CONFIRMED READY. Closeout pin lines: inside the pre-merge review (G-27) | Admitted 01-03, 04-01, 04-03, 06-01, 06-02, 09-01. Checked: early path; C1 §3 "EXP → DAC" and "RW-1 → FV-4a" Holds. DAC:12 now pins ACT-POLICY-v0.11 (`597f13bd…`) and DAC:141 pins FV `8c4e8378…`. I checked both against the current files by sha256. Each pin was hand-checked against the supplier diff (`RUN/DISPATCH.md`, O-C closeout row) | F (`fw04_check.py` 22/0) | (c) **Covers VER-004 only.** "Every other part of DEL-09-05 (the two delegations, the graph, the queue, the interruption and recovery witness) is a later unit" (DAC header "Serves"). The V4-EXM-13 undertaking fixture: O-C, a later unit. (d) An App candidate; the actual person (DEP-09-05-012) | None recorded; the design is thinner than its obligations (Part C) |
| **DEL-09-06** Connected activity contract and workflow round trip | `CONNECTED_ACTIVITY_CONTRACT.md` CA-v0.7; `RELAY_QUESTIONS_SWBPIPE.md` RELAY-v0.3 (relayed and answered); `RELAY_ANSWERS_SWBPIPE.md` (received); `FACTS_SQ01_SQ32.md`; W14 schema + rehearsal | FI → P3 | V21-B → V21b-B; V22; W14 re-pin inside P1 | 13 admitted suppliers; consumers 03-04, 09-07. Checked: V18-4 (CA, XT and the four SCA-V4-002 arcs); C1 found and repaired a W14 break. **Host side:** "0 of 10 steps are examinable there now" (`P2/RECEIPT.md`). Reverse-arc guard carried (H4) | F (W14 rehearsals 44/0 on SH-1 and fixtures) | (a) OI21; GP; R8-Q4b; OI-003. (c) The CA W14 narrative note (owner's choice, C1 §6 item 7). (d) DEP-001 EC-01…EC-14; SWBPIPE owner decisions (ANS §2); DECISION-5 host obligations not relayed (`INT/RECEIPT.md`); HJ | Guard: some new rows would be SCC-forming departures (H4 "DEL-09-06 reverse-arc guard"). None proposed |
| **DEL-09-07** Local host candidate qualification | `LOCAL_HOST_QUALIFICATION.md` LHQ-v0.2; `TRAFFIC_OBSERVATION_PLAN.md` TOP-v0.1; `QUALIFICATION_DOSSIER.md` DOS-v0.1; CIR, traffic and dossier schemas. At `161f8a0d0d`: LHQ `d59a1ea0…`, TOP `dcfcddf0…`, DOS `b4de982f…`. LHQ2-R2 is a CI-5 sentence added in place at `18d6eae3e4`, label unchanged | P4-T1 (O-C); LHQ-v0.2 in P4-T2 | RV-LHQ-U1/U2 CONFIRMED READY. RV3 READY at LHQ `90f461cb`, DOS `687032c0` (`RUN/reviews/RV3-EUF1.md` Addendum 3). LHQ2-R2 is CLOSED (RV3, `a1734df11e`; RV3-EUF1 Addendum 9 "confirmed"). The N8 and pin-line changes are left to the pre-merge review (G-27) | Admitted 09-01, 09-06. Consumers 09-11, 11-03. Checked: C1 §3 (EXP → DOS; DOS → RRM withheld classes: Holds). R23-36: CIR maps to EXP. **Host side:** HC-1…HC-13 answered, none committed; "0 of 4 cases can start"; V4-EXM-20 "cannot pass against its current product" (`RUN/OWNERS/O-C.md` LHQ-U1 claim 7). Closeout pins at `18d6eae3e4`: DOS and TOP pin LHQ `d59a1ea0…` (I checked this by sha256); DOS pins the v0.2 CIR schema, which settles LHQ2-R2's pin. LHQ line 10 keeps its GUIDE-v0.7 pin deliberately. HELP_HUMAN's ruling is in `RUN/DISPATCH.md`, the O-C closeout row: GUIDE changed only its ACT row at `48df7404c7`, and HC-7.3/7.9 are untouched. | D for cases ("No case has run"); F (`top_check.py`, `dos_check`) | (a) OI21; A12 (F-5: four SCA-V4-003 DEFERs bear on LHQ-23); S-01-4 (owner at the host join). (c) P1-F2 (TOP §7 times as instants; next revision); F-4 receiver sentence; SH-1 rehearsals (O-C, later unit). (d) DEP-05-01-024 "UNKNOWN supplier"; SWBPIPE relay list (HELP_HUMAN prepares, owner relays); PL (App candidate's role) | None recorded beyond A12, S-01-4 and PL |
| **DEL-09-09** External control and catalog-extension trace | `EXTERNAL_TRACE_CASES.md` XT-v0.7; result-record schema | FI → P3 | V21-B → V21b-B; V22 | Admitted 04-01, 09-01; held SCC-002 (02-03, 03-01…03-03, 04-02, 04-03, 05-01). Consumers 03-04; held 03-01*. Checked: V18-4. **Host side** IN-02…IN-30 (HJ) | F | (a) OI-003; OI21; OI-005 (additional hosts); GP; R8-Q4b. (c) F-18 V4-EXM-25 completion rule for per-batch Apply (integrator). (d) DEP-001; IN-30 fixture reset (next relay); actual A13 and A5 acts (the person) | None recorded |
| **DEL-09-10** Optional connector consumption witness | `CONNECTOR_WITNESS.md` CW-v0.2 | P4-T2 (EU-D1) | RV2-EUD1 READY | Admitted 07-01, 07-02, 08-01, 09-01. Records follow EXP-v0.2. No upstream row for DEL-09-01 (register note; R23-34.8) | F (EU-D1 rehearsal) | (c) **Dossier §5 is "outline"**; IA-1, IA-3, CW-RB, CW-BD case detail and an `outside_coverage` case are "next unit" (O-D; CW §7; `RUN/OWNERS/O-D.md` "Open, with owners"). (d) QC-1 joined witness waits for a qualified PEC release (PEC owner) and adoption; Domains cases wait for the Domains increment | None recorded |
| **DEL-09-11** Later run reconstruction witness | `READER_METHOD.md` RRM-v0.1; input-set and account schemas; prototype (`3e24df27…`; closeout pins at `18d6eae3e4`) | P4-T1 (O-C, EP-11) | RV-EP CONFIRMED READY. Closeout pin lines: inside the pre-merge review (G-27) | Admitted 04-03, 09-01, 09-07. Checked: C1 §3 (DOS ↔ RRM enums equal; NOTE: DOS omits RRM's `definition` standing). RRM:15 now pins DOS `b4de982f…` and RRM:19 pins ACT-POLICY-v0.11; I checked both by sha256. RRM check 19/0 (DISPATCH) | F (`run_standing_check.py` 19/0; isolated readers RR-E and RR-F on the fixture) | (b) REQ-002 wording on destinations (R23-11). (d) Source V4-EXM-20 journey and receipts (DEL-09-07; HJ); durable receipts (SQ-09 (c), SWBPIPE owner, next relay) | **Basis-level tension S1-C S-3 / S2-F S-F6:** with session-only receipts every week-later reference is unresolvable, and the App-side remedy "contradicts the basis". Recorded, not resolved |
| **DEL-09-12** Practitioner validation and feedback disposition | `PRACTITIONER_VALIDATION.md` PV-v0.4 (`f928f5fd…`); schema; valid examples and 29 invalid examples | P4-T2 (O-F): EU-F4 (v0.2) → EU-F4R (v0.3, `9ba5dfe49c`) → EU-F4R2 (v0.4, `158c0b2859`) | `RUN/reviews/RV2-PV1.md`: REPAIR on v0.2 (PV1-R1 MAJOR); v0.3 READY, PV1-R1…R8 CONFIRMED (`c4577c333a`); Addendum 2: PV-v0.4 READY, PV2-R1 and PV2-N2 CONFIRMED (`528536b668`). Nothing open; the PV2-N3 note means "no change for 60%" (DISPATCH). | Admitted 04-01, 09-01. Consumers 10-02 (UC §9 receives the method notes; both sides state the join, and no comparison record was found), 11-03. **Hand-over to DEL-11-03 stated and mechanically compared, not adopted.** PV §2 O-3: "DEL-11-03's first cut therefore refuses this record as it stands". The stated differences are `format`, `arrangement_ref` and `is_replacement_condition`. `check_pv.py` K-12 recomputes them against the first cut (U-PV-3). EXP still expects `activity: validation` (U-PV-4) | F (`check_pv.py` 38/38; PV §8) | (a) U-PV-1 = OI-016 period and activities (owner, P-2); U-PV-5 = OI-020 (P-6). (c) U-PV-3 ("design agent O-F at DEL-11-03's next revision"); U-PV-4 (EXP's next revision). (d) U-PV-2: candidates (DEL-09-02; DEL-09-07 with SWBPIPE; HJ) | None recorded. S2-F S-F3 (EXP required field) as for DEL-09-01 |

### PKG-10 Project definition and manual-led practice

| (1) | (2) | (3) | (4) | (5) | (6) | (7) | (8) |
|---|---|---|---|---|---|---|---|
| **DEL-10-01** Project execution basis and manual application | `EXECUTION_BASIS.md` EB-v0.4; `eb1/` (comparison, key) | P4-T2 (O-E, EB-1) | `RUN/reviews/RV3-EB1.md` Addendum 3: EB-v0.4 READY; RR-EB1 early path passed (R23-38) | No suppliers. Consumers 10-02, 10-03, 10-04, 11-01, 11-02 (EB §7). R23-35 basis binding (`RUN/BASIS_BINDING.md`, 9/9 pins) | R (primary records; isolated reader on real records) | (c) **"VER-004, 005, 007 and 008 not run \| O-E \| Before this file is offered for the 60% review"** (EB §9). (a) OI-018 (rest), OI-019, OI-020, OI-024; DEP-006 | None recorded. PN-2: making the basis binding a loop step "would change LOOP_INIT" (`RUN/OWNERS/O-E.md`), an instruction change, not a deliverable structure change |
| **DEL-10-02** Proportionate undertaking controls and practice feedback | `UNDERTAKING_CONTROLS.md` UC-v0.2 | P4-T2 (O-E) | `RUN/reviews/RV3-UC1.md` REPAIR → addendum: UC-v0.2 READY | SCC-005 with 10-04*. Admitted 09-12, 10-01. UC §9 receives DEL-09-12's observations | R | (a) **Stage disposition of PN-1, PN-2, PN-3, PN-5, PN-6 (owner, at the 60% stage discussion)**; VER-007 dispositions (UC §12). (c) VER-002 unit-brief case (re-marked partial, R23-46.4); VER-005 (O-E) | None recorded. SCC-005 unruled (CASE-006 R1 recommended) |
| **DEL-10-03** Shared commitments and consumer responsibility account | `RESPONSIBILITY_ACCOUNT.md` RA-v0.2; prototype `ra_check.py` | P4-T2 (O-E) | `RUN/reviews/RV3-RA1.md` READY on RA-v0.1 (2 MINOR). **RA-v0.2 is not yet confirmed by RV3** (DISPATCH: "pending the pre-merge review") | Ten admitted suppliers (02-01, 02-03, 02-04, 03-01, 03-02, 04-01, 04-03, 05-01, 05-02, 10-01), each cited by sha256 and rechecked by `ra_check.py`. Consumers 10-04, 11-01, 11-02. **F-RA1:** three joins (04-01, 05-01, 05-02 → 10-03) are recorded on one side only (RA §3.4) | R (`ra_check.py` 31/0) | (b) F-RA1 mirror rows and SoW receivers (register and SoW owners). (c) VER-004 build and runtime checks "outstanding at their points of need". (a)/(c) Unconfirmed shared allocations (WD U-17, OI-014) are for the deliverable owners (R23-31.8) | None recorded (F-RA1 rows are MIRROR; no new arc, RA §3.4) |
| **DEL-10-04** Project production dependency DAG | `DAG_ACCOUNT.md` DA-v0.3; prototype `dag_reach.py` (the project's reach script, R23-51) | P4-T2 (O-E) | `RUN/reviews/RV3-DA1.md` READY (v0.1, and v0.2 addendum). **DA-v0.3 not yet confirmed** | SCC-005 with 10-02*. Admitted 10-01, 10-03. DA §4 rechecks the interface account against DAG-001…004 | R (strict audit on DAG-001…004; reach script self-test 5/5) | (c) Apply CASE-002's drafted DAG-004 evidence update (HELP_HUMAN via `scc-resolution-case`). (b) DEP-005 row text lags D4 and R23-22 (DA §8). Currency step 2 done at 128/130 | None recorded |

### PKG-11 Adoption and replacement continuity

| (1) | (2) | (3) | (4) | (5) | (6) | (7) | (8) |
|---|---|---|---|---|---|---|---|
| **DEL-11-01** Preserved history and coexistence account | `CONTINUITY_ACCOUNT.md` CA-v0.4 (`ea171162…`, `821f236649`); schema | P4-T2 (O-F) | `RUN/reviews/RV3-CA1.md` READY (v0.1, v0.2 and v0.3 addenda). CA-v0.4: RV3 "EU-F3R2 READY", CA2-N1 CONFIRMED (`RUN/reviews/RV3-AA1.md`, addendum EU-F3R2; `a1734df11e`). Nothing open | Admitted 10-01, 10-03, 11-02; SCC-006 with 11-03*. CA §2: I-1 vendors the DEL-10-03 draft; O-1 hand-over adopted by RP-v0.4 | R (real git and archive checks) + F (`check_ca.py` 37/37, DISPATCH) | (a) U-CA-1 continuing obligations per lane (lane owners with the owner; OI-024). (c) U-CA-2 C-7 archive digest record (HELP_HUMAN to route); U-CA-3 (DEL-11-03 coordinator); U-CA-5 (O-F) | None recorded. CASE-007 R1 used for design (F-R8); "a later graph choice of R2 or R3 would change no Design file" (S2-F S-F5) |
| **DEL-11-02** Consumer-specific renewed-basis adoption | `ADOPTION_ACCOUNT.md` AA-v0.3 (`b8fe830b…`): `821f236649`, amended in place for AA3-R1 at `158c0b2859`; schema | P4-T2 (O-F) | `RUN/reviews/RV3-AA1.md`: REPAIR on v0.1; EU-F3R READY; EU-F3R2 READY, AA2-R1 CONFIRMED; EU-F3R3 "READY; AA3-R1 resolved" (`161f8a0d0d`). DISPATCH: "All tranche-2 design units are now READY with no open BLOCKING, MAJOR or MINOR findings" | Admitted 02-04 (supplier row only, R22-7-open), 10-01, 10-03. Consumers 11-01, 11-03. D-GOV-52 real case: App v4 adopted (R23-30); App v3 and Runtime "notice delivered; receiving decision not recorded" | R (D-GOV-52 records) + F (`check_aa.py` 47/47, DISPATCH) | (a) U-AA-2 first adopters and end of coexistence (owner with consumers; OI-024; P-4). (b) U-AA-3 DEP-02-04-013 consumer row. (d) U-AA-1 App v3 and Runtime decisions (those loops' owners); U-AA-4 (DEL-02-04, DEL-01-01). Checker limits listed by O-F (`RUN/OWNERS/O-F.md` "Claimed rules without a negative case") | None recorded |
| **DEL-11-03** Owner replacement evidence packet | `REPLACEMENT_PACKET.md` RP-v0.6; packet-manifest and disposition schemas; fixture FX-RP1-6. File `42eef807…`: the label is unchanged, and the LHQ pin moved in place to `d59a1ea0…` at `821f236649` | P4-T2 (O-F, EU-F1) | `RUN/reviews/RV3-EUF1.md` Addendum 8: RP-v0.6 READY. Addendum 9: the LHQ pin note is "confirmed". Early path passed (R23-49; readers RR-EUF1/2/3) | Admitted 09-02, 09-07, 09-12, 11-02; SCC-006 with 11-01*. Consumes SQ, DOS, CIR and EXP on real files (R23-33, R23-36). **One-sided:** RP still holds the first-cut `practitioner_standing` `$defs`, which refuses PV-v0.4's hand-over as it stands (PV §2 O-3). Adoption is carried to RP's next revision (U-PV-3; DISPATCH EU-F4R row) | F (`check_rp.py` 99/99); supplier evidence "illustrative (schema examples)" | (a) P-1 replacing v3.0.1 and P-5 public release (owner; "Prepared only; never performed or implied"). (c) Remote re-check of REFERENCES §2 (DEL-11-03 coordinator); rendered presentation view (O-F, EU-F1 "Open"). (d) OI21, DEP-001, HJ: "OUT-002 stays incomplete"; PL | None recorded. A replacement-qualification claim needs both witnesses (R23-43) |

## Part B — project level

### B.1 DAG version and currency

- **Accepted graph:** DAG-004 (`E/_DAG/_LATEST.md`: "Latest: DAG-004",
  accepted 2026-10-03, basis `75764184b9`). It has 41 nodes, 129 admitted
  arcs, 83 held arcs in six SCCs and 355 exclusions (H4 "Objective…").
- **Currency.** The latest observation is
  `E/_Evaluation/DAGCurrency/_LATEST.md` → `CURRENCY_APP_V4_DEL0103_TLFIX_2026-10-03_2016`:
  CURRENT_WITH_EVIDENCE_DRIFT, with nothing DAG pending. The drift is the
  accepted repair of DEL-01-03's absolute TargetLocation values.
- **Rechecked for this inventory:**
  - `shasum -a 256 -c _DAG/DAG-004/SOURCE_MANIFEST.sha256` from `E/`
    gives 128 OK and 2 FAILED: DEL-01-03 `Dependencies.csv` and
    `_DEPENDENCIES.md`. This matches DA §5 step 2 and the DISPATCH closeout
    row;
  - `MANIFEST.sha256` gives 37/37 OK;
  - `_LATEST_ACCEPTED.md` still names GROUP3-20260928T001055Z.
- **Pending departures that would need a successor (DAG-005):**
  - the three proposed bundle-seam arcs (PKG §13; SCC-neutral by
    `dag_reach.py`);
  - a possible V25 m-1 reconciliation (H4).
  No successor is drafted.

### B.2 SCC cases

Each case's "Current confirmed tracking" reads "CaseState:
EVIDENCE_ACCUMULATING" (CP1 through `_DAG/_Candidates/DAG-001/BASIS_DECISION.md`).
The preserved inquiry sections read HUMAN_RULINGS_PENDING. Each case
recommends R1 (coordinated contributions). **No case has a ruling, remedy or
closure.**

| SCC (DAG-004) | Case | Members | Held arcs | Pass-4 use | State notes |
|---|---|---|---:|---|---|
| SCC-001 | SCC-CASE-001 | DEL-01-01, 01-05 | 2 | — | Unchanged |
| SCC-002 | SCC-CASE-002 (CASE-004 as history) | 01-04, 02-01…02-04, 03-01…03-03, 04-02, 04-03, 05-01, 05-02, 09-09 | 71 | Definition proceeds on provisional versions (H4) | **DAG-004 evidence update drafted, not applied.** `SCA3/DAG_PREP/CASE-002_EVIDENCE_UPDATE.proposed.md` ("DRAFT, NOT APPLIED"). The datasheet's latest section is the DAG-003 observation (checked by heading list). Owner: HELP_HUMAN via `scc-resolution-case` (DA §8). DISPATCH routes it to the next amendment list |
| SCC-003 | SCC-CASE-003 | DEL-01-06, 09-01 | 2 | R1 milestones in EXP and PKG | R2 (objective-scoped merge-group) is kept as a conditional alternative |
| SCC-004 | SCC-CASE-005 | DEL-07-01, 07-02, 08-01 | 4 | CASE-005 R1 for the H-3 vocabulary (R23-34.1) | — |
| SCC-005 | SCC-CASE-006 | DEL-10-02, 10-04 | 2 | — | — |
| SCC-006 | SCC-CASE-007 | DEL-11-01, 11-03 | 2 | R1 for design (F-R8) | — |

### B.3 Open_Issues (26 rows; `E/_Decomposition/Open_Issues.csv`)

Disposition is judged from each row's own Status and Consequence text.
Rulings recorded elsewhere but not in the row are noted.

| OI | Title | Status | Owner (row) | Point of need (row) | Row text shows |
|---|---|---|---|---|---|
| OI-001 | Reserved human acts | OPEN | Owner with App/SWB contract owners | Before operation-policy production contracts | **Partly ruled:** D2 for App/shared; additions under OI-021, host adoption under DEP-001 |
| OI-002 | Classifier routine permissions | OPEN | Owner with App/SWB contract owners | Before permission-policy implementation | **Partly ruled:** D3 for the App; host adoption under DEP-001 |
| OI-003 | Automatic catalog extension | OPEN | Owner with host contract owner | Before claiming extension capability | Open |
| OI-004 | v3 chat import disposition | OPEN | Owner | Before transition contract relies on it | Open |
| OI-005 | Additional essential hosts | OPEN | Owner | Before examination scope is frozen | Open |
| OI-006 | Further fleet management scope | OPEN | Owner | During FEED before production contracts | Open |
| OI-007 | Distributed sign-in terms | OPEN | Owner and relevant supplier | Before public release beyond owner use | Open |
| OI-008 | App process division | OPEN | App implementation owner | Before architecture production contracts | Open |
| OI-009 | Codex sign-in account home | RESOLVED_BY_OWNER_DECISION | Owner with App implementation owner | Before account integration | **Ruled** at choice level (K-1; L-7). Credential sign-in not observed; API key stays with OI-010 |
| OI-010 | API-key protocol detail | OPEN | App implementation owner | Before API-key implementation/qualification | Open |
| OI-011 | Signing and notarisation | OPEN | App implementation owner with SWB owner | Before packaged distribution witness | Open in the row. R23-26 settles the App-side arrangement for design (option B); the row update is carried |
| OI-012 | Codex version pin | OPEN | App implementation owner | Before protocol generation and qualification | **Partly ruled:** D4 definition pin 0.158.0; qualification pin open. The R23-22 rule is not in the row |
| OI-013 | Per-host loop placement and persistence | OPEN | Shared contract owner with SWB implementation owner | Before shared/host boundary contracts | Open |
| OI-014 | Shared contract/component placement | OPEN | App/shared contract owners | Before structural/production allocation | Open |
| OI-015 | Cross-engine vs native-platform examination | RESOLVED_BY_SOURCE | Source reconciliation | Resolved before Group1 | Ruled |
| OI-016 | Owner validation activity and period | OPEN | Owner | Before practitioner validation in use | Open |
| OI-017 | Project manual pins | RESOLVED_FOR_CURRENT_DEFINITION_RUN | Owning project-definition manager | Before dependent execution relies on editions | **Partly:** current run only. R23-35 requires each undertaking to bind its own basis |
| OI-018 | Instruction distribution/adoption | OPEN | Owner with instruction owners | Before instruction changes or dependent supply | **Partly:** App answered (K-9, L-2); hosts and others open |
| OI-019 | Consequential manual gaps | OPEN | Owner with execution manager | When a gap affects selected work | Open |
| OI-020 | Manual revision responsibility | OPEN | Owner | Before revising manuals from feedback | Open |
| OI-021 | First connected activity definition | OPEN | Owner via outside SWB session and App/shared owner | Before connected-activity SoW and execution | Open |
| OI-022 | PEC first receiving envelope | OPEN | App consumer owner and PEC owner | Before operational consumer reliance | Open. PRC-v0.4 proposes the App side |
| OI-023 | Domains receiving contract and timing | OPEN | Owner with Domains/SWB/App receiving owners | Before the Domains-enabled increment | Open. DRC-v0.1 proposes the App side in part |
| OI-024 | Staged adoption and retirement | OPEN | Owner with affected consumers | Before each adoption/retirement | Open |
| OI-025 | Objective deliverable mappings | RESOLVED_BY_GROUP2 | WORKING_ITEMS | Completed at Group2 | Ruled |
| OI-026 | Domains provider ownership | OPEN | Owner with App/Domains/SWB definition owners | Before allocating Domains provider production | Open |

Tally, from the row text: **3 ruled** (009, 015, 025), **5 partly ruled**
(001, 002, 012, 017, 018) and **18 open**. Of the 18 open rows:
- the person is named in 004, 005, 006, 016 and 020, and jointly in 003,
  007, 019, 021, 023, 024 and 026;
- 008, 010 and 011 name the App implementation owner, which is the owner
  per L-7 (see G-24);
- 013, 014 and 022 name only roles.

### B.4 Items carried to the next ScopeOfWork or register amendment

| # | Item | Source |
|---|---|---|
| N-1 | Overtaken ScopeOfWork wording in all eight tranche-1 deliverables (OI-001/002 "remain OPEN", the D4 pin and similar) | R23-7, R23-11; `RUN/RECEIPT.md` |
| N-2 | DEL-09-02 OI-009 wording (closure audit ASC-ISS-002), TBD-001/002/003, CLM-001, REQ-006; counterparts of DEP-09-02-014/-018 | SQ §11; `SCA3/RECEIPT.md` |
| N-3 | DEL-04-01 REQ-002 naming A16 | R23-18.4 |
| N-4 | OI-011 register record (SWB part waits for HJ); OI-012 row lacks R23-22 | R23-26.2; B.3 |
| N-5 | Bundle-seam arcs 02-02, 02-04, 01-04 → 01-06 (**new arcs**: DAG successor) | PKG §13; R23-2 |
| N-6 | DEL-01-06 CLM-002 and TBD-003 wording | PKG §13 |
| N-7 | DEL-08-02 CLM-006, TBD-003, REQ-005, AC-006, VER-005 OI-001/002 wording; DEP-09-01-027's missing upstream row in DEL-09-10 | RTD §10; R23-34.8; CW header |
| N-8 | EXP O-1 statement for DEP-09-01-019 | EXP §14 |
| N-9 | DEL-09-07 F-4 receiver sentence (DEL-09-11) | LHQ §8 |
| N-10 | DEL-09-11 REQ-002 wording on destinations (amended V4-HI-70) | RRM §UNRESOLVED |
| N-11 | F-RA1: SoW receivers and mirror rows for 04-01, 05-01, 05-02 → 10-03 | RA §3.4 |
| N-12 | U-AA-3: consumer-side row for DEP-02-04-013 (R22-7-open) | AA §9; R23-32 F-R15 |
| N-13 | DEP-005 row text lags D4 and R23-22 | DA §4, §8 |
| N-14 | **Held at SCA-V4-003 (owner items):** Q-7 S-01-4; Q-9 SC2-04-01-2, S-0502-1, R2-04-01-b, R-0502-2; Q-14 R-02-4; three basis items (P2-C1-B-B-2, P2-C1-C-B-1, P2-C1-C-B-2); R22-7-open | `SCA3/OWNER_DECISIONS.md` DECISION-1; `LEDGER.md` DEFER rows |
| N-15 | Five expected mirror rows not extracted; V25 m-1; three mirror maturity differences; the SatisfactionStatus convention; OI-001/002 constraint rows in nine registers | H4 "Open matters" |
| N-16 | CASE-002 DAG-004 evidence update (DISPATCH routes it to "the next amendment list"; DA §8 names `scc-resolution-case`) | `RUN/DISPATCH.md` last row; DA §8 |
| N-17 | SCA-V4-003 is still `OPEN_PENDING_DERIVATIVE_CLOSURE`: Design re-pins (21 of 23 done per `RUN/RECEIPT.md`); `Coverage_Telemetry.json` stale (owner-deferred) | `E/_ScopeChange/_LATEST.md`; H4 |

### B.5 External dependencies (`E/_Decomposition/External_Dependencies.csv`)

| DEP | Supplier | Present satisfaction (register) | What waits on it, per the records |
|---|---|---|---|
| DEP-001 | SWBPIPE outside implementation session | OWNER_REPORTED_BUILDING_BEFORE_AGENT_ACTION_INTEGRATION | Every host join (HJ). LHQ: 0/4 cases can start. CA: 0/10 steps examinable on SWBPIPE. V4-EXM-20 cannot pass against SWBPIPE's current per-batch Apply. Durable receipts (SQ-09 (c)). DECISION-5 host obligations not relayed. SWBPIPE owner decisions (ANS §2) |
| DEP-002 | PEC owning project | OPTIONAL_RECEIVING_QUALIFICATION_UNESTABLISHED_AT_ffb2b6289 | PRC agreement (§2/§3), PEC tool representation, qualified release; DEL-09-10 QC-1 |
| DEP-003 | Domains provider (allocation TBD, OI-026) | OWNER_REPORTED_KNOWLEDGE_OUTSIDE_REPO_PARALLEL_LATER_JOIN | DRC admitted sources and contract; DEL-08-02 increment; DEL-09-10 Domains cases |
| DEP-004 | OpenAI (conditional Anthropic) | UNCONFIRMED | OI-007, before public release |
| DEP-005 | Pinned Codex/Tauri/local-server suppliers | VERSION_AND_ENVIRONMENT_TO_DEFINE (row lags D4 and R23-22) | Qualification pin (R23-22 rule); sign-in and API-key observation (L-6, OI-010); stock-route delegation; U-SQ-6 lost-acknowledgment capture; OBS gaps. Pins: 0.158.0 definition, 0.160.0 checked and design-compatible |
| DEP-006 | Owners of affected Root, Runtime, App and Piping consumers | NOT_ADOPTED_BY_THIS_DRAFT | App v3 and Runtime D-GOV-52 receiving decisions not recorded (AA U-AA-1); OI-024 |

Person's acts recorded as later, at their own points of need (R23-32
P-1…P-7; R23-34 preamble):
- P-1 replacing v3.0.1;
- P-2 OI-016;
- P-3 use and fitness;
- P-4 staged adoption and retirement;
- P-5 public release;
- P-6 method changes;
- P-7 OI-021;
- OI-026;
- starting the Domains increment;
- any relaxation of V4-HOST-02;
- signing with the owner's Apple account (R23-13.2).

## Part C — where the 60% criterion is not yet evidenced

The criterion has two parts. "Interfaces developed" means each is checked
against the other side's actual Design text. "No further structural change
anticipated" covers a new or split deliverable, a changed ScopeOfWork
obligation, an SCC-forming row, or a DAG successor. Each gap below gives its
source and one line on what would evidence closure.

### C.1 Structural changes still anticipated on the record

- **G-01. Held ScopeOfWork obligation changes.**
  - S-01-4: DEL-03-01 REQ-004 and protected AC-004.
  - SC2-04-01-2: DEL-04-01 AC-007 and VER-007, plus a new AX.
  - S-0502-1 option A: DEL-05-02 CLM-002 and OUT-001.
  - The rows R2-04-01-b and R-0502-2.

  All are held at SCA-V4-003 Q-7/Q-9 for later owner decisions
  (`SCA3/OWNER_DECISIONS.md`; `LEDGER.md` L188, L225, L256, L427, L470).
  LHQ F-5 and TOP depend on them.
  *Evidence:* an owner decision on Q-7/Q-9 at the next amendment, or a
  recorded "option B stands".
- **G-02. New arcs proposed, so a DAG successor is needed.** Bundle seams
  DEL-02-02, 02-04, 01-04 → DEL-01-06 (PKG §13; R23-2). They are SCC-neutral
  by `dag_reach.py` (run for this inventory). An added arc is "still an
  added-arc departure" (DA §5 item 1). V25 m-1 may also become a departure
  (H4).
  *Evidence:* the rows extracted and a DAG-005 accepted, or a decision that
  no row is needed.
- **G-03. Six SCCs with no ruling.** Every case recommends R1; none is ruled.
  CASE-003 keeps an R2 merge-group alternative. CASE-002's DAG-004 evidence
  update is drafted but not applied (B.2).
  *Evidence:* the CASE-002 update applied, and the owner's treatment of each
  case (or an explicit "R1 as tracking").
- **G-04. Placement undecided (OI-013/014, OI-008).** S1-C S-2 records that
  if the loop ships as a shared component, RS §3's producer column and
  LOOP's mapping move. LHQ and DOS treat the App candidate's role in an
  embedded run as "affected while unknown". PD appears as "(phase review)"
  in RECOVERY U-R8, NPTD U-P7, AAC U-AAC-1 and FR §11.
  *Evidence:* the placement decisions, or a recorded deferral with the
  affected rows named.
- **G-05. Basis-level tension on receipts** (S1-C S-3; S2-F S-F6; RRM
  UNRESOLVED). With session-only host receipts, week-later reconstruction
  cannot resolve references, and the App-side remedy "contradicts the
  basis". The resolution waits on SWBPIPE (SQ-09 (c)).
  *Evidence:* a SWBPIPE durable-receipt commitment, or a basis decision.
- **G-06. Domains increment rows foreseen.** A new candidate-approval act
  needs rows in ACT, RS, CE, GUIDE and WD (R23-34.4, S2-D S-5). A Domains
  tool class (S-4) is not opened (R23-34.5).
  *Evidence:* stated as deferred to the Domains increment. It is
  structural-adjacent, but the record calls such changes rows.

### C.2 Interfaces checked on one side only, or against superseded text

- **G-07. Every App ↔ SWBPIPE host interface.**
  - Host joins are deferred (DECISION-3).
  - The answers are "data, not commitments".
  - DECISION-5 host obligations are not relayed (`INT/RECEIPT.md`).
  - DEL-09-07: 0/4 cases can start; DEL-09-06: 0/10 steps examinable.
  - This affects DEL-03-01…03-04, 04-01…04-03 (host parts), 05-01, 05-02,
    09-06, 09-07, 09-09, 09-11 and 11-03 (OUT-002).

  *Evidence:* the host joins resumed and the relay delivered.
- **G-08. OI-021 is unbound.** The first connected operation, autonomy and
  environment are undecided. LHQ, CA, XT, ACT, AS and RS carry parameter
  slots.
  *Evidence:* the owner's OI-021 decision via the SWB session.
- **G-09. PEC and Domains have no counterparty.** PRC §2/§3 need agreement
  with the PEC owner. DRC has no provider; all inputs are invented.
  *Evidence:* the PEC owner's agreement or a qualified release; an OI-026
  allocation.
- **G-10. HOSTING (DEL-01-01) lags pass-4 findings.** It still lists
  App-origin reads as "not observed" (§6.8), while PRC relies on R23-50/53.
  R23-37.2 (a thread with no turn has no items) is not yet in HOSTING, WR,
  RECOVERY or NPTD. R23-30.1 (Root citations) and R23-30.2 (ACCESS U-A9) are
  also not yet applied.
  *Evidence:* the HOSTING, ACCESS, WR, RECOVERY and NPTD revisions that
  carry these.
- **G-11. GUIDE (DEL-03-04) is not updated for tranche 2.** M10.1 and M10.2
  cite "accepted SoW meaning (outside undertaking)". G-2 reads "PEC and
  Domains receiving not started". A grep finds 0 references to
  PRC/CFB/DRC/RTD, although 03-04 admits all four as suppliers. The GUIDE
  pin check binds bytes, not content (GUIDE §4.5).
  *Evidence:* a GUIDE revision mapping M10 to the tranche-2 files.
- **G-12. DEL-09-12 ↔ DEL-11-03 and ↔ DEL-09-01.**
  - **PV-v0.4's final hand-over statement.** PV §2 O-3 says the hand-over
    supersedes RP's first cut and "DEL-11-03 adopts it at its next
    revision".
  - **The two sides do not yet agree.** "DEL-11-03's first cut therefore
    refuses this record as it stands": `format` and the added
    `arrangement_ref` and `is_replacement_condition` differ, and the first
    cut is closed.
  - **The difference is mechanically bounded.** `check_pv.py` K-12
    recomputes the differences and validates the record against the first
    cut with them undone.
  - **PV's own limit.** K-12 "cannot show that DEL-11-03's next revision
    will take the stated differences".
  - **Owner of the fix.** U-PV-3 is assigned to "design agent O-F at
    DEL-11-03's next revision". RP-v0.6 is unchanged (DISPATCH EU-F4R
    row).
  - **EXP mismatch.** EXP still requires `activity: validation` with an
    outcome that PV does not use (U-PV-4; PV1-R8; S2-F S-F3).

  *Evidence:* RP's and EXP's next revisions adopting PV's shapes.
- **G-13. WD §9 consumer confirmations absent** (WD U-17: "Every row
  'None'"). U-01 carriage is PROPOSED "until then it is not settled".
  R23-31.8 leaves the confirmations to the deliverable owners.
  *Evidence:* recorded confirm-or-object from DEL-02-03, 05-01, 05-02, 03-02,
  02-02 and 02-04.
- **G-14. Last all-join comparisons predate current versions.**
  - The full receiver comparisons for PKG-02…05 are V18-1…4 at v0.6–v0.8
    (P2), plus F0 and V21 for pass-3 joins.
  - Pass-4 changes were checked as rows (RV-E1; C1 §3 lists specific
    interfaces).
  - DEL-03-01 and 03-02 were last content-reviewed in P2.
  - "Hold machine confirmation (EXEC-v0.5 §4)" is still listed as awaiting
    "the next integration review" in LOOP and PANEL.

  *Evidence:* a receiver comparison over current versions, limited to joins
  changed since V18/F0.
- **G-15. Register-level one-sided joins.**
  - F-RA1 (three rows).
  - Five expected mirror rows not extracted.
  - Three mirror maturity differences.
  - Missing counterparts: DEP-09-01-027, DEP-09-02-014/-018 and
    DEP-02-04-013.
  - DEL-09-07 F-4.
  - The V25 m-1 contradictory pair.
  - DEL-03-03's absent DOWNSTREAM mirror to DEL-03-04.
  - DEL-09-12 O-2's dispositions target "UNKNOWN" in the register
    (DEP-09-12-013).

  None changes an arc except V25 m-1 possibly.
  *Evidence:* the register UPDATE at the next amendment.
- **G-16. FX-PIPE-01 has not adopted L-LHQ-1/2** (R23-16); DEL-09-07 cites
  them as local additions.
  *Evidence:* DEL-03-01's next revision.

### C.3 Designs thinner than their obligations

- **G-17. DEL-09-05** covers VER-004 only. The two delegations, the graph,
  the queue and the interruption/recovery witness are "a later unit" (DAC
  header).
  *Evidence:* designs for VER-001…003 and 005…007.
- **G-18. DEL-08-01 DRC-v0.1.** §6–§8 are "outline". The Design file cites
  none of VER-001…008. OUT-002 depends on admitted sources that do not
  exist.
  *Evidence:* §6–§8 completed and a VER mapping.
- **G-19. DEL-09-10 CW-v0.2.** The dossier (§5) is "outline". IA-1, IA-3,
  CW-RB, CW-BD and an `outside_coverage` case are "next unit".
  *Evidence:* O-D's next unit.
- **G-20. DEL-10-01 EB-v0.4** states "VER-004, 005, 007 and 008 not run …
  Before this file is offered for the 60% review" (EB §9).
  *Evidence:* those VERs run, or the owner told they were not.
- **G-21. DEL-10-02 UC-v0.2.** The VER-002 case is partial (R23-46.4).
  VER-005 and VER-007 are open. PN-1/2/3/5/6 dispositions are reserved to
  the owner "at the 60% stage discussion".
  *Evidence:* the owner's PN dispositions at the stage discussion.
- **G-22. DEL-02-01 U-36** declared chaining is "later work of this
  deliverable".
  *Evidence:* WD's next revision.
- **G-23. Implementation-time design items** across PKG-01/02 are numbered
  and not designed: HOSTING U-05…U-27, RECOVERY U-R2…U-R4/U-R7/U-R12, ACCESS
  U-A4…U-A6, ROLE U-R3/U-R4/U-R9…U-R11, WR U-WR-7…U-WR-18, NIR U-NIR-1/2/10.
  Each has the point of need "before implementation".
  *Evidence:* named as such; whether 60% requires them is the owner's
  reading.

### C.4 Open matters with unclear owner or decision route

- **G-24. "App implementation owner" (AIO).** DECISION-L L-7 makes the AIO
  the owner, but R23-17 treats AIO items as implementer facts, "not owner
  questions". Dozens of items carry this label (G-23), and the per-item
  route is not recorded.
  *Evidence:* one recorded rule for AIO items.
- **G-25. Role-only owners with no person or agent mapping.**
  - "Shared contract owner with SWB implementation owner" (OI-013).
  - "App/shared contract owners" (OI-014).
  - "App external-host integration owner" (ADAPTER TBD-007 OC-1…OC-12).
  - "App execution/recovery owner" (RECOVERY).
  - "App role-guidance owner" (ROLE).
  - "Integrator" (WR, ROLE, AAC, XT F-18, AS U-20).
  - "UNKNOWN supplier" for DEP-05-01-024, the model interface (LOOP; LHQ).
  - "DEL-11-03 coordinator" (CA U-CA-3; RP).

  *Evidence:* a mapping of each role to the person or an agent.
- **G-26. Items pointed at "the owner's phase review".**
  - CV with four questions (ACT §8.5).
  - PD.
  - PANEL F-12.
  - U-A2 "asked again at the phase review if the design needs it".
  - Earlier lists in `P2/RECEIPT.md` and `P3/RECEIPT.md`, "Open for the
    owner's phase review".

  Whether the 60% review is that phase review is not stated in the records
  read.
  *Evidence:* these put to the owner, or explicitly deferred.

### C.5 Review and record state of the current candidate

- **G-27. Tranche 2 is not through its pre-merge review.** The branch is 40
  commits ahead of the local `origin/main` ref at `161f8a0d0d` (`git log`, not fetched).
  Items DISPATCH marks "covered by the pre-merge review" are unconfirmed:
  ACT-POLICY-v0.11, RA-v0.2, DA-v0.3, FV10-R9 (46/46), and the N8 and DOS
  fixes.
  *Evidence:* the tranche-2 pre-merge review on the actual candidate.
- **G-28. Units in repair or uncommitted — RESOLVED at `161f8a0d0d`.**
  - **O-C's pins and LHQ2-R2** were committed at `18d6eae3e4`: DAC:12/141,
    RRM:15/19, DOS:9, TOP:7, the DOS v0.2 CIR schema pin and the CI-5 line.
    RV3 recorded LHQ2-R2 CLOSED at `a1734df11e` (RV3-EUF1 Addendum 9). I
    checked the new pins by sha256 against the current files. LHQ line 10
    keeps GUIDE-v0.7 by HELP_HUMAN's ruling (DISPATCH, O-C closeout row).
  - **CA-v0.4 and AA-v0.3** were committed at `821f236649` (EU-F3R2). AA3-R1
    was amended in place at `158c0b2859`. RV3 confirmed EU-F3R2 at
    `a1734df11e` and EU-F3R3 at `161f8a0d0d` (RV3-AA1 addenda).
  - **PV** went to v0.3 at `9ba5dfe49c` (RV2 READY, `c4577c333a`) and to
    v0.4 at `158c0b2859` (RV2 READY, `528536b668`; RV2-PV1 Addendum 2).
  - **RP-v0.6's LHQ pin** moved in place at `821f236649` (RV3-EUF1 Addendum
    9).

  DISPATCH: "All tranche-2 design units are now READY with no open BLOCKING,
  MAJOR or MINOR findings". The pin-line and mechanical changes remain for
  the pre-merge review (G-27).
- **G-29. Derivative-closure debt.**
  - SCA-V4-003 is still `OPEN_PENDING_DERIVATIVE_CLOSURE`.
  - `Coverage_Telemetry.json` is stale (owner-deferred).
  - The 17 re-pinned Design files pin pre-UPDATE `Dependencies.csv` bytes
    (C1 §6 item 4).
  - Six VERSION_ADVANCE §7.1 rows pin bytes held in no commit (R23-29.3).

  *Evidence:* the closure audit, or the owner's recorded acceptance of the
  debt.

### C.6 Evidence-standing limits

- **G-30. No App candidate exists, and nothing is built, signed or
  qualified.** Product evidence is fixture or prototype only.
  - Supplier observations cover one Codex pin (0.158.0, with 0.160.0
    checked), one local LM Studio model and the probed routes only.
  - Not observed: sign-in, API key, stock-route delegation, the checklist
    surface, the child-role carrier and the lost-acknowledgment capture.
  - Signing reliance waits for FP-1/FP-3 on the first package (PKG U-PKG-1).

  This is consistent with a design-phase position, but it is the reliance
  limit the statement must carry.
- **G-31. Review independence and enforcement.**
  - All pass-4 reviews were Claude Opus 5.5 reviewing Claude Opus 5.5 work.
    R23-31.5 records this "as an observation for the 60% discussion".
  - Host write and network isolation is "not observed to be host-enforced;
    unknown" (R23-47).
  - O-F lists checker rules with no negative case (`RUN/OWNERS/O-F.md`).

### Not established, and what was looked at

- **S1-A S-3** (delegation export may be too narrow). No ruling was found in
  R23 or DECISIONS_PENDING. FR §7 consumes NPTD §7.7 unchanged, and RV-E2
  passed it. The disposition is not established.
- **Which 2 of SCA-V4-003's 23 Design re-pins remain.** `RUN/RECEIPT.md`
  says 21 of 23 and names PIN_SPIKE. C1 §2 counts 23 as 19 + O-A's four. The
  second remaining file is not established.
- **Whether a unit reviewer, rather than P1, reviewed VERSION_ADVANCE.**
  Only the R23-22 ruling and P1 were found.
- **Ownership mapping for role-named owners (G-25).** No record maps them to
  the person or to an agent.
- **Whether the 60% review is "the phase review" (G-26).** Not stated in
  LOOP_INIT, the receipts or R23.
- **Interface between DEL-09-12 and DEL-10-02.** Both sides state it (PV §2
  O-1; UC §9). No comparison record was found.
- **Prototype counts.** These are as recorded in C1 §4 and `RUN/DISPATCH.md`.
  They were not rerun for this inventory, except `dag_reach.py` (four
  queries) and the two DAG-004 manifests.
