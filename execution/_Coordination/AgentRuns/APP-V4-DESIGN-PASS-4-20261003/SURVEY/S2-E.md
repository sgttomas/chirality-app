# S2-E — Scoping survey: PKG-10 (DEL-10-01, DEL-10-02, DEL-10-03, DEL-10-04)

Run `APP-V4-DESIGN-PASS-4-20261003`, node T2-S, survey S2-E. Executor: Type 2
TASK (Claude Opus 5.5), read-only on project state, written 2026-10-04 at
HEAD `d2929fd62b` with the run's uncommitted BRIEFS/DISPATCH/OWNER_DECISIONS_2
and WORK_GRAPH edits present in the worktree (read as working bytes, hashes
below). This file claims no SWBPIPE join, witness or adoption, and changes no
register, ScopeOfWork, status, DAG, case, basis, coordination or Design file.

Paths are relative to `projects/chirality-app-v4/execution` unless they start
with `docs/` (App v4 basis) or are marked Root. **States** marks what a file
says; **Inference** marks mine. Labels for proposed answers follow R9/R23:
SETTLED, DERIVED, INTEGRATION, PROPOSED. Pin basis (R23-3): pin-independent;
nothing here relies on a Codex protocol fact.

## 0. What was read and how

All hashes are sha256 by `shasum -a 256`, first 16 hex shown.

| Input | How read | Identity |
|---|---|---|
| Run `BRIEFS.md` (Common rules, S1, S2), `R23_RESOLUTIONS.md` (whole), `OWNER_DECISIONS.md`, `OWNER_DECISIONS_2.md`, `RECEIPT.md`, `DISPATCH.md`, `DECISIONS_PENDING.md`; `WorkGraphs/APP-V4-DESIGN-PASS-4-20261003/WORK_GRAPH.md` | Whole | `53f8d877b6ed324b`, `fafa6ed7364ca930`, `e4350f61a93edf0d`, `5744a66813b57946`, `a45055e25070d981`, `5ea21c01ab986e62`; graph `34b2e489e4e9f82b` |
| Root `workflows/coordinated-knowledge-work/WORKFLOW.md` | Whole | `44049bcd38b88378`, equal to the hash OWNER_DECISIONS.md records |
| Tranche-1 survey `SURVEY/S1-A.md` (model of form; its K-C/Q-A3 and S-7 bear on PKG-10) | Whole; S1-B/S1-C by heading only | `616568603f93a62c` |
| The four PKG-10 `ScopeOfWork.md`, `Dependencies.csv`, `_CONTEXT.md`, `_STATUS.md`; DEL-10-03 `MEMORY.md` | Whole; registers by script | SoW `7a89fc3874386d42` (10-01), `d93ec4c043b783c0` (10-02), `31bc607defa42914` (10-03), `fb62502a0f59b226` (10-04). Registers `ec95f7c0246bc83b`, `42a7edd14cb1d48c`, `7b9bcfafd3637b1e`, `2469ec61bdf3017d`: each equals its `SourceRegisterSHA256` in DAG-004. `git log`: 10-01, 10-02, 10-04 SoWs have only the INIT commit `ddd721a90a` plus register extraction `c1038ae5ac`; 10-03 was revised once, by SCA-V4-002 (`1efd4bcdad`, REQ-005 and AX-005). All four `_STATUS.md`: INITIALIZED (2026-09-27) |
| `_Decomposition/Deliverables.csv`, `Packages.csv`, `Open_Issues.csv`, `External_Dependencies.csv` | Rows for PKG-06, PKG-10, OI-013/014/017–026, DEP-006 | `552df0609e7c5b4d`; Open_Issues `9c2d916c277f8ce4`; External_Dependencies `055703d9a7147ab9` |
| `_DAG/_LATEST.md`; DAG-004 `HANDOFF_STATE.md`, edge/candidate/exclusion/node CSVs, `MANIFEST.sha256`, `SOURCE_MANIFEST.sha256`; DAG-001…004 `ACCEPTANCE_RECORD.md` owner quotes; `_DAG/cases/SCC-CASE-006/` | Handoff whole; CSVs by script; case contract, datasheet, QA | Handoff `3c374f5e9fa4cfaa`. `MANIFEST.sha256` passes. `SOURCE_MANIFEST.sha256`: 128 of 130 entries match today; the two that differ are DEL-01-03's `Dependencies.csv` and `_DEPENDENCIES.md`, the drift already recorded by `_Evaluation/DAGCurrency/_LATEST.md` (CURRENT_WITH_EVIDENCE_DRIFT, no deliverable DAG pending). Datasheet `e39ecee4709afc4e` |
| `_Coordination/CURRENT_EXECUTION_BASIS.md`, `_COORDINATION.md`, `HANDOFF_30_PERCENT.md`, `THIRTY_PERCENT_REVIEW.md` (headings), `INITIAL_SETUP_SUMMARY.md` (hash only), the D-GOV-52 notice | Whole / head | `99d0800967fb16fd`, `8fadef166d35f40c`, `f95e10b1e34ed13f`, `1474503fd0c8d202`, `08db981a7b93cc91` |
| Manuals and methods pinned in CURRENT_EXECUTION_BASIS | Recomputed today | All nine pinned files (Consolidated v7, Field Book v1, Agent User Manual v3; `project-setup`, `scope-of-work`, `dependency-extract`, `audit-dep-closure`, `project-dag` WORKFLOW.md; `preparation` SKILL.md) **match** their recorded hashes byte for byte. Field Book §1, User Manual §§14, 19 read; others by heading |
| App v4 basis `docs/OPERATING_METHOD.md` (whole); `PRD.md`, `ARCHITECTURE.md`, `HOST_INTEGRATION.md`, `EXAMINATION.md` | OPS whole; others hash only | OPS `98836b5240ed235e`; PRD `bb6e786f7a6c01dc`; ARCH `317d5789272c5206`; HOST `d4331c39db7f452c`; EXAM `471798bc2f2dc020` (all equal to the hashes S1-A recorded) |
| `loop/LOOP_INIT.md` | Whole | `3790159b4f60bb4f` |
| Root `docs/SPEC.md` §5.4, §9.7–9.8, §11.2; `workflows/construct-local-work-graph/WORKFLOW.md`; `workflows/project-dag/resources/*` (hash only); `tools/REGISTRY.md` rows; `tools/validation/validate_root_work_graph_dispatch.py` head | Sections | SPEC `feb5e79c0b60b515`; construct-local-work-graph `fa04e1347f859465`; project-dag contract `a55edc3b89a2b641`, currency `d2927ed4ac96ebc7`, graph-version `ff6b7ba5b455e5e2`, method `4a5566bfbc9f3d6b`; Root `AGENTS.md` `f96feb19d297c74e` (the D-GOV-52 bytes the notice names) |
| Tranche-1 and earlier Design files naming PKG-10 (grep `DEL-10-0`/`PKG-10` over every `Design/`) | Hits read in context | FR-v0.1 `3e3ba16c9c73f941` and `fleet.record.schema.json` `e4dd5100b9641907`; EXP-v0.2 `ff0187dafd9e1f02` (§7); RRM-v0.1 `fcaa654437127306` (headings); PKG-v0.2 `0d8d14d2ce08d859` (P-2/P-3 rows); WD-v0.9 `262c9e5417cf67b5`; EXEC-v0.7 `138b04eb0fe71632`; ROLE-v0.2 `c8474d919bceec7d`; C-v0.8 `0e3ba39cd926a206`; P-v0.8 `ad6a3083e7b808e2`; ACT-POLICY-v0.10 `1bf0ce8e413d2b8f`; RS-v0.10 `2e7afb1bb8b872c0`; LOOP-v0.9 `2bac33a883b176e2`; PANEL-v0.9 `4898b6f80832b3ba` |
| SCA-V4-003 `AMENDMENT_PACKET/LEDGER.csv` and packet `.md` files | grep `DEL-10`/`PKG-10` | `e28661cdf3375e15` |
| App v3 exemplar `projects/chirality-app-dev/frontend/scripts/prepare-packaged-instruction-root.mjs` (DEL-10-03 CLM-007) | Declarations only | `fe0fa50df51e4a77`; last commits `95b3425195`, `9b005c23a7`. Evidence only, never a v4 commitment |

Reach was computed by a scratch script over DAG-004's admitted and held
layers (consumer → supplier; DOWNSTREAM rows reversed), the method S1-A used.

---

## 0.1 The finding that frames everything else

**States.** The four PKG-10 deliverables are the App v4 *project's own*
execution controls, not App product features:

- Types: DEL-10-01, 10-02 and 10-03 are `DOC_UPDATE`; DEL-10-04 is
  `DATA_MODEL_CHANGE` whose artifacts are "DOC: identified project dependency
  DAG and interface registers; DOC: closure/examination and current-basis
  acceptance evidence" (Deliverables.csv).
- PKG-06's package row excludes them: "Project dependency DAG and project
  practice are PKG-10" (Packages.csv).
- DEL-10-02's row: "Use file-native undertaking controls immediately; PKG-06
  product views may later render them and are not a prerequisite to this
  undertaking or their own construction."
- OPERATING_METHOD's preamble: "This document applies the accepted
  manual-led practice to the undertaking."
- FR-v0.1 FR-D2 (DEL-06-01, tranche 1): "The method's current Markdown work
  graphs (Root SPEC §9.8) are a practice DEL-10-02 owns, not a format with
  identified versions; this format does not change them, and their adoption
  of it would be a separate instruction change."

**Inference.** The brief's framing ("the App's support for practices this
project already uses") is right about the practices and wrong about where the
App's *product* support sits: that is PKG-06 (records and views) and PKG-02
(bundled workflows), already designed. PKG-10's results are accounts of how
this project is defined and run, and most of their substance **already
exists** in project records produced by Root methods:

| Deliverable | Existing record that already carries most of it | Produced by |
|---|---|---|
| DEL-10-01 OUT-001 | `_Coordination/CURRENT_EXECUTION_BASIS.md` (manual and method pins, standing, OI-017 scope) | WORKING_ITEMS as "Owning project-definition manager" |
| DEL-10-01 OUT-002 | `_COORDINATION.md`, `HANDOFF_30_PERCENT.md`, `loop/LOOP_INIT.md` "Project pointers" | project-setup; 30% closeout |
| DEL-10-02 OUT-001 | Nine `WorkGraphs/*/WORK_GRAPH.md` and their `AgentRuns/` records | `construct-local-work-graph`, SPEC §9.8, now `coordinated-knowledge-work` |
| DEL-10-04 OUT-001/002 | `_DAG/DAG-001…004`, `_DAG/cases/`, `_Evaluation/DepClosure/`, `_Evaluation/DAGCurrency/` | `project-dag`, `audit-dep-closure`, `scc-resolution-case` |

So "60% design" here means: a thin account per deliverable that maps each
obligation to the record that meets it, checks that record, and fills the
real gaps. It does not mean inventing App rules. Root governance already
settles most of the practice (§§1.5, 2.5, 3.5, 4.5 below).

---

# Part 1 — DEL-10-01 Project execution basis and manual application

DOC_UPDATE; "App project-definition manager; owner decides consequential
adoption/departure"; INITIALIZED; no `Design/` folder.

## 1.1 Obligations (27: 3 OUT, 8 REQ, 8 AC, 8 VER)

Basis keys (the SoW's own): **A** acceptance APP-V4-BASIS-20260926 (HTML-D01/07,
directions A/C); **B** Group3 snapshot and OI-017/DEP-006; **O** OPERATING_METHOD
V4-OPS-01/04/10–14/31–33, PRD V4-CST-04, OQ-05; **C** clarification
APP-V4-CLARIFICATION-20260927; **Q** `_COORDINATION.md`; **F/M/U** the three
manuals; **W** `scope-of-work`, `software-decomp`, `project-setup` handoff clauses.
CLM-001…005, TBD-001 and AX-001…003 read, not counted.

| Item | One line | Rests on |
|---|---|---|
| OUT-001 | Execution-basis account: adopted manual/method pins with standing, composite/decomposition transfer, open adoption detail, named consumers; inspected ≠ adopted | B, A, O, F §§2–3, U §§4–6 |
| OUT-002 | Package/deliverable setup and working/checking/issued handoff; developmental positions; a contract's existence is not fulfilment | B, Q, O-01/04/33, F §§1/4, M §§3.4–3.8, U §§5–7 |
| OUT-003 | Manual purpose/application/departure account; not a form per rule | A HTML-D01, O-10…13, C, U §1 |
| REQ-001 | Identify composite, later direction, final snapshot and downstream standing; carry unresolved inputs with owner/point of need; route later changes to affected decisions only | A, B, C, O §1/O-33 |
| REQ-002 | Each adopted manual by edition and content identity; method source-qualified identity; adopting record/scope; historical and read ≠ adopted; resolve TBD-001 before dependent reliance | O-11, B OI-017, U §§1/4 |
| REQ-003 | Preserve identities and working/checking/issued purposes; transfer decomposition to setup and local contracts; existing vs incomplete vs future preparation; use Q's choices | B, Q, O-01, F §4, M, U §6 |
| REQ-004 | Explain six positions by what they establish, DAG before 30%; no effort percentages; uneven maturity | O-04, F §§1–2, M §1.7, U §5 |
| REQ-005 | F as route, M by reasoning section, U for repository application; unused mechanism: purpose, treatment, departure; no added scope, no Root-first hierarchy, no thin-loop default | A HTML-D01, O-10…13/§7, C, B, U §1 |
| REQ-006 | Distinguish definition, work, verification, validation, acceptance, reliance; actor and subject per act; no invented acts or synthetic ordering | CLM-001/003/004, M §1.6, U §§1/4, Q |
| REQ-007 | Serve named setup/local-SoW/project-definition consumers by reference; carry adoption implications to PKG-11 with DEP-006's point of need; no paperwork, copied corpus, product UI, precedence tree | B, C, O-12…14/31–32 |
| REQ-008 | No act owned by DEL-10-02/03/04, DEL-11-01/02, setup/status actors or the owner | B, Q, A |
| AC-001…AC-008 | One per REQ, as stated in the SoW (trace to Group1/2/3 and setup without repeating approval; inspected vs adopted; source-faithful handoff, INITIALIZED never substituted; six positions; three manuals for their roles; actor/subject standing; named reader per output, PKG-11 interface; owners preserved) | REQ-001…008 |
| VER-001…VER-008 | Compare against A/B/Q/O; recover edition bytes and adoption record; walk the handoff as a setup reader; compare positions with F §1, M §1.7, U §5; read application account against manuals; positive/negative act cases; trace outputs to readers and PKG-11; boundary-owner checker plus semantic examination | AC-001…008 |

**Overtaken or re-read by later decisions.**

- **TBD-001 / OI-017** is no longer simply OPEN. Open_Issues states
  `RESOLVED_FOR_CURRENT_DEFINITION_RUN`: CURRENT_EXECUTION_BASIS records the
  three editions and method origins "for this App-v4 definition run/current
  basis", and "A later or changed basis needs its own deliberate pins before
  reliance". The SoW wording predates this (carry to the next amendment,
  R23-11).
- **CLM-004 and REQ-006's recording rules** are consistent with how every
  later run records owner acts (OWNER_DECISIONS files: exact text, custody
  "the session transcript; recorded by HELP_HUMAN"). Nothing overtakes them.
- **Methods used since setup** are not in CURRENT_EXECUTION_BASIS:
  `construct-local-work-graph` (LOOP_INIT §1), `scope-change`,
  `scc-resolution-case`, `bounded-reconciliation`, and
  `coordinated-knowledge-work` (owner-selected for this run; its hash recorded
  in OWNER_DECISIONS.md). **Inference:** their identities live in their run
  records; OUT-001 indexes them rather than copying them.
- **OI-018** (instruction distribution): Open_Issues states that the App part
  is "answered by DECISION-K3 K-9 as amended by DECISION-L L-2"; D-GOV-52
  (R23-30) is the latest applied instance. It bears on OUT-003 only as a
  worked example.

## 1.2 Joins

| Row(s) | Consumer → supplier | Type; maturity / satisfaction | DAG-004 |
|---|---|---|---|
| DEP-10-02-011 | DEL-10-02 → DEL-10-01 | INTERFACE; INITIALIZED / TBD | admitted |
| DEP-10-03-017 | DEL-10-03 → DEL-10-01 | PREREQUISITE; INITIALIZED / TBD | admitted |
| DEP-10-04-005 | DEL-10-04 → DEL-10-01 | PREREQUISITE; INITIALIZED / TBD | admitted |
| DEP-11-01-009 | DEL-11-01 → DEL-10-01 ("actual manual/method pins … distinguishing this run selection from adoption or instruction supply") | PREREQUISITE; INITIALIZED / TBD | admitted |
| DEP-10-01-020 | DEL-11-02 → DEL-10-01 (handover of adoption implications) | HANDOVER; INITIALIZED / TBD | admitted |
| DEP-10-01-012…019, 021, 022 | Documents (basis, clarification, Group3, `_COORDINATION`, F, M, U, CURRENT_EXECUTION_BASIS), setup/local-SoW readers, App-v4 owner | CONSTRAINT/PREREQUISITE/HANDOVER; TBD / TBD | excluded, NOT_TOPOLOGICAL (SR-2) |

**States (computed).** DEL-10-01 has no deliverable supplier and reaches
nothing; it is reached by DEL-10-02, 10-03, 10-04, 11-01, 11-02 and 11-03. No
held arc touches it. No Design file names DEL-10-01.

## 1.3 Proposed contract changes still open

None in the SCA-V4-003 ledger targets a PKG-10 SoW (grep of `LEDGER.csv`:
only mirror rows on suppliers' registers name DEL-10-03). **For the next
amendment (R23-11), inference:** TBD-001's OPEN wording against OI-017's
current standing.

## 1.4 Open items and who decides

| Item | Shapes the design now? | Answer the texts support | Who decides |
|---|---|---|---|
| **E1-1 Where OUT-001…003 live** | Yes: file plan | The existing records are the homes; DEL-10-01 gets one thin Design file that maps obligations to them and fills gaps. The SoW: "These documentary outputs may be sections of one usable account with references to existing decisions and controls … this contract does not prescribe another governance corpus or duplicate snapshots"; V4-OPS-31 | **DERIVED**, for HELP_HUMAN |
| **E1-2 Who maintains CURRENT_EXECUTION_BASIS and later pin records** | Yes: writer of OUT-001's core | The "owning project-definition manager" (OI-017 owner), which in this project is HELP_HUMAN acting in the WORKING_ITEMS function, as CURRENT_EXECUTION_BASIS itself states and R23-28 applied. O-E prepares text; the manager writes the coordination record | **INTEGRATION**, for HELP_HUMAN |
| **E1-3 Pins for later undertakings** | Yes: REQ-002/AC-002 content | Later undertakings rely on the recorded pins while the bytes are unchanged (verified today, §0); each run's work graph or brief cites them; a changed edition gets a deliberate re-pin record before reliance (V4-OPS-11: "adopt changed editions deliberately"; OI-017 row) | **DERIVED** |
| E1-4 Consequential departures (CLM-004) | Only if one is found | Rows known so far are already decided: Root-first hierarchy superseded (V4-OPS-12; A/C, HTML-01); thin-loop default not mandatory (V4-OPS-14); dated App-v3 entry pointers, including User Manual §14, are "not v4 product requirements" (LOOP_INIT "Manual-led v4 practice"). E2-4 (reviewer preference) may become one | Reserved to the owner if consequential (quote in §5.2); none identified now |
| E1-5 Developmental position | No | SETTLED by Field Book §1 and V4-OPS-04. Actual position: 30% accepted (DAG-001 ACCEPTANCE_RECORD: "I have reviewed and now approve the 30% package …"); work toward 60% under way | 60% assessment reserved to the person (§5.2), not open now |
| OI-018 remainder | No | Hosts and other instruction owners; the App part is answered | External; not this pass |

## 1.5 What exists to build on

- **Root settles the practice.** SPEC §11.2 and §5.4 (pointers and
  acceptance), §9.8 (run records); `project-setup` (lifecycle rules applied in
  `_COORDINATION.md`); Field Book §1 (positions table: "Percentage labels
  describe development positions. They do not measure effort, code, or tasks
  completed").
- **Project records** (§0.1 table), with a chain of actual owner acts already
  recorded with custody: Group1/2/3 decisions; setup ("Approve the recommended
  setup plan"); SCA-V4-001/002/003 Group-3 snapshots; DAG-001…004 acceptances
  ("I accept DAG-004."); this run's OWNER_DECISIONS and OWNER_DECISIONS_2.
- **Worked example for OUT-003 and DEP-10-01-020:** D-GOV-52, a changed
  shared instruction, its notice to App v4 and App v4's recorded adoption in
  R23-30 (V4-OPS-14 "Receiving adoption").
- **Tools:** `tools/scope_of_work/check_boundary_owner_resolution.py` (VER-008's
  "registered boundary-owner checker"); `shasum -c` for pin rechecks.
- **App v3:** not relevant to DEL-10-01 beyond the User Manual §14 pointer it
  dates.

## 1.6 Design scope for this pass

1. **`Design/EXECUTION_BASIS.md`** (one file, three sections, one per OUT):
   - basis chain: each accepted act (actor, exact subject, record, custody
     limits) linked, not copied; later material changes and which decisions
     they reopened (REQ-001, REQ-006);
   - pin table: manual editions and method identities with hashes recomputed
     at writing; standing per row (selected/adopted, inspected, historical
     candidate such as `e548d4cf…`); methods selected by later undertakings,
     indexed to their run records; the re-pin rule (E1-3);
   - handoff for an arriving setup/local-SoW author or manager: where each
     thing is, what INITIALIZED means and does not mean, what is prepared vs
     remaining (REQ-003), and the six positions with the project's actual,
     uneven position (REQ-004);
   - application/departure table: practice → purpose → actual treatment →
     departure? → deciding record (REQ-005, OUT-003);
   - consumers and handovers: DEL-10-02, 10-03, 10-04, 11-01, 11-02 (DEP-006
     point of need).
2. **Verification design** for VER-001…008, including a hash recheck script
   and the boundary-owner checker run.

**Leave out:** rewriting CURRENT_EXECUTION_BASIS or `_COORDINATION.md` (manager
records; proposals go to HELP_HUMAN); any precedence ordering; manual copies;
adoption on behalf of other loops (DEL-11-02).

---

# Part 2 — DEL-10-02 Proportionate undertaking controls and practice feedback

DOC_UPDATE; "App undertaking manager; human at applicable stage decisions";
INITIALIZED; no `Design/` folder.

## 2.1 Obligations (27: 3 OUT, 8 REQ, 8 AC, 8 VER)

Basis keys: **B1** Group3 allocation, OI-017…020; **B2** OPS V4-OPS-02/03/20–23/30–32/34,
PRD OQ-05; **B3** HTML recommendations 01/07, U1/U4; **B4** manuals; **B5**
`_COORDINATION.md`, setup RUN_BRIEF, project-definition WORK_GRAPH.
CLM-001…006, TBD-001…003, AX-001…004 read, not counted.

| Item | One line | Rests on |
|---|---|---|
| OUT-001 | Work-graph control and return/reader conventions in the existing file-native records | B1, OPS-02/03/31/32, F §§2/5, U §§9/10, B5 |
| OUT-002 | Permission/isolation and independent-check account per undertaking and candidate | OPS-30/34, U §§3/10, M §1.5 |
| OUT-003 | Node-linked practice observations and stage dispositions | OPS-20/21/31/32, M §§5.4/7.4 |
| REQ-001 | One current graph per undertaking; recover outcome, basis, mapping, inputs/holds, owner, write boundary, check, returns, review/integration, next; DAG ≠ route ≠ executing; accepted DAG used once current | CLM-001/003, OPS-02, F §5, U §9, B5 |
| REQ-002 | Four roles proportionately; briefs (purpose, basis, parent and mechanism, authority, writes, checks, return) and returns examined before integration | OPS-03, F §§2/5, U §§3/10 |
| REQ-003 | Each record names reader and consumption point; Git/PRs primary; faithful recording of human acts; no act proves another | OPS-31/32, U §4, M §7.4, B5 |
| REQ-004 | Enforcement account: host-reported vs brief-stated; worktree ≠ sandbox; nothing "enforced" because followed | CLM-005, OPS-30 |
| REQ-005 | Independent-check account: reviewer separation, basis, candidate identity, checks, findings, backchecks; model identity only when exposed | CLM-005, OPS-30/34 |
| REQ-006 | Brief practice observation at the node when practice proved useful, ill-fitting or ambiguous; manual section/edition; none manufactured | OPS-20/31, M §§5.4/7.4 |
| REQ-007 | At the applicable decision or stage discussion, bring notes to the owner; preserve disposition (proposed revision, scoped departure, no change); OI-019/020 carried | SOW-222, OPS-21…23, HTML 01/07 |
| REQ-008 | No act owned by DEL-10-01, 10-04, 06-01, 06-02, the human, the host or the examiner | allocation rows |
| AC-001…AC-008 | One per REQ, as stated (recover route from one graph without fleet/PEC; arrangement without compulsory hierarchy; reader/use, faithful recording; capability account; checking account; node notes; dispositions; boundary) | REQ-001…008 |
| VER-001…VER-008 | Graph walkthrough; arrangement vs brief/return; record set vs reader/use table with positive/negative act cases; brief vs actual host permissions; candidate bindings through review; notes traced to node and manual section; dispositions vs decision evidence; boundary-owner comparison | AC-001…008 |

**Overtaken or re-read by later decisions.**

- **CLM-004** ("Future product views can render file records") is now concrete:
  FR-v0.1 FR-D2 keeps the Markdown graphs as DEL-10-02's practice and names
  their adoption of the fleet format "a separate instruction change"; FR's
  graph record carries `projectDagRef` ("The project DAG this graph's route
  reads, or 'none'; the graph does not restate it").
- **REQ-001's graph practice** is now also governed by Root SPEC §9.8 (graph
  location, Git-tracked, "An executed child is required for an execution
  claim; a brief alone is insufficient") and by `coordinated-knowledge-work`,
  which the owner selected for this run.
- **TBD-001** carries OI-017 as OPEN; see Part 1.

## 2.2 Joins

| Row(s) | Consumer → supplier | Type; maturity / satisfaction | DAG-004 |
|---|---|---|---|
| DEP-10-02-011 | DEL-10-02 → DEL-10-01 | INTERFACE; INITIALIZED / TBD | admitted |
| DEP-09-12-012 | DEL-10-02 → DEL-09-12 (method observations and dispositions from practitioner validation) | HANDOVER (DOWNSTREAM on DEL-09-12's side); INITIALIZED / PENDING | admitted |
| DEP-10-02-012; mirror DEP-10-04-014 | DEL-10-02 → DEL-10-04 (graph-based selection uses the accepted current DAG) | CONSTRAINT; INITIALIZED / TBD | **held**, SCC-005, SCC-CASE-006 |
| DEP-10-04-006 | DEL-10-04 → DEL-10-02 (graph production consumes current control records) | PREREQUISITE; INITIALIZED / TBD | **held**, SCC-005, SCC-CASE-006 |
| DEP-10-02-013 | DEL-10-02 → the owner at the stage discussion | HANDOVER; TBD / TBD | excluded, NOT_TOPOLOGICAL |

**What existing Design files assume of DEL-10-02 (tranche 1).**

- FR-v0.1 §2 FR-D1: "Files written with ordinary tools keep the file-native
  route working with or without the App (DEL-10-02; REQ-005; AC-007)."
- FR-v0.1 §2 FR-D2 (quoted in §0.1) and §10: "Undertaking practice; project
  DAG | DEL-10-02; DEL-10-04 | `projectDagRef` cites; nothing restated".
- `fleet.record.schema.json` work-graph revision: "Not the project DAG
  (DEL-10-04)."
- EXP-v0.2 §7 RV-1…RV-6 (candidate review protocol, R23-12): DEL-10-02 does
  not consume it, but its separation and model-identity rules are the
  product-side form of the same V4-OPS-34 commitment (E2-4).

**SCC-CASE-006 (states).** CaseState EVIDENCE_ACCUMULATING; recommends R1
(keep both arcs held; name the record subset and the post-acceptance use);
R2 (cut) and R3 (merge group) are human rulings, none made; DAG-001's basis
decision confirmed the tracking. **Inference:** under DAG-004 the held arcs
are non-gating, DAG-004 is accepted and current, and the controls already
use it, so R1 needs no further act.

## 2.3 Proposed contract changes still open

None in the SCA-V4-003 ledger. Next-amendment candidate (inference): TBD-001's
OI-017 wording, as in Part 1.

## 2.4 Open items and who decides

| Item | Shapes the design now? | Answer the texts support | Who decides |
|---|---|---|---|
| **E2-1 Home of OUT-001** | Yes | SETTLED practice: SPEC §9.8, `construct-local-work-graph` §§3–4, LOOP_INIT §1, `coordinated-knowledge-work`. The Design file instantiates the SoW's own reader/use table against the actual records and names gaps; it adds no new file per run | **DERIVED** |
| **E2-2 Practice-note convention** (REQ-006) | Yes | A short "Practice notes" entry in the run record, linked from the graph node, citing manual section and edition and observed conditions. Project-local; the Root graph template is unchanged. Making it reusable would revise a Root workflow through `create-workflow` (out of scope) | **DERIVED**; O-E proposes, HELP_HUMAN integrates as graph maintainer |
| **E2-3 First notes** | Yes: OUT-003 has real content | Tranche-1 observations already recorded: the mid-repair checkpoint that moved HEAD under owners' pins (RECEIPT "Coordinator lesson"); the early path exposing what unit reviews missed; a checker that agreed only with its own author's constructed accounts; the owner's "Scope of owner questions" correction (over-escalation). Each needs its manual locus added | **DERIVED** |
| **E2-4 V4-OPS-34 for this project's own reviews** | Yes: OUT-002/REQ-005 | **States:** V4-OPS-34 says "Independently review identified candidates, with the original D-13 preference for a Codex reviewer and the stated different-model Claude fallback", and applies it to the post-act consolidation itself. Pass-4 reviews (RV, RV2, P1) were Claude Opus 5.5, as were the authors; the reviews record that identity honestly. No earlier ruling addresses project design reviews (grep of all run records). **Proposed reading:** the independence requirement is met by a separate session that did not author the subject, with identity reported; the model-family preference applies with full force to product candidate examination (EXP §7; R23-12); the pass-4 practice is recorded as an observation for the stage discussion. If HELP_HUMAN finds that reading unsupported, the practice is a consequential departure for the owner (V4-OPS-13) | **INTEGRATION**, for HELP_HUMAN; owner only if ruled a departure |
| E2-5 Disposition of notes at the stage discussion (REQ-007; DEP-10-02-013) | No (prepare the package) | The texts reserve this to the person (quote in §5.2). Point of need: the 60% phase review | Reserved to the person; not open now |
| E2-6 OI-019 consequential manual gap | Only when one affects selected work | Owner with execution manager, "When consequential gap affects selected work". None identified now | Reserved jointly when triggered |
| E2-7 OI-020 manual revision authorship | Only if a revision is proposed | Owner, "Before revising manuals from feedback". None proposed | Reserved when triggered |
| E2-8 Permission/isolation account form (REQ-004) | Yes, locally | A short section in each run's DISPATCH or BRIEFS: host-reported vs instruction-asserted vs untested. This run already states "Fences are verified afterwards by `git status`" and SCC-CASE-006's contract says "Host workspace access exceeds this brief's file boundary; compliance does not prove isolated enforcement" | **DERIVED** |
| E2-9 SCC-CASE-006 | No | R1 stands under DAG-004; R2/R3 would be cut/merge rulings reserved to the person (DEL-10-04 CLM-001); none proposed | No ruling needed |
| E2-10 Receiving DEL-09-12's observations (DEP-09-12-012) | Little | Same note convention; waits for practitioner validation (S2-F) | O-E with O-F |

## 2.5 What exists to build on

- **Root settles:** SPEC §9.8; `construct-local-work-graph` (graph form,
  "Keep one current account of the ready work, holds and next safe action",
  run records for detail); `coordinated-knowledge-work` §§1–6 (owners,
  reviewers, findings, adoption checks); LOOP_INIT §§0–6; the four-role
  table in Root `AGENTS.md`.
- **Records:** nine work graphs; run folders with BRIEFS, DISPATCH, OWNERS/,
  reviews/, closeout/, RECEIPT; the reviews' identity lines ("RV (Type 2
  TASK, Claude Opus 5.5)").
- **Tools:** `tools/validation/validate_root_work_graph_dispatch.py` (G3) checks
  declared write targets and disjoint concurrent writes, but only for Root's
  `execution/_harness/work_graph.yaml` (`root-work-graph/v1`); it does not read
  App v4's Markdown graphs. **Inference:** reusable as a model for a fence
  check, not directly.
- **Product side, for contrast only:** FR-v0.1 and FV-v0.1 (PKG-06); EXP §7.
- **App v3 exemplar:** `managed-delegation.ts` and `WORK_GRAPH.json`, as S1-A
  §1.5 records; ARCH §3 lists the v3 delegation wrappers as "Not selected".

## 2.6 Design scope for this pass

1. **`Design/UNDERTAKING_CONTROLS.md`**:
   - controls map: the SoW's reader/use table bound to the actual records and
     to the Root texts that settle each (SETTLED vs DERIVED marked);
   - brief and return conventions as practised (BRIEFS "Common rules",
     DISPATCH rows, OWNERS records), checked element by element against
     REQ-002; gaps named;
   - per-run capability and independent-check account form (E2-4, E2-8);
   - practice-note convention and the first notes (E2-2, E2-3);
   - the stage-disposition package form for the 60% review (REQ-007),
     marked pending;
   - DAG use: the accepted current version and live satisfaction (REQ-001),
     SCC-CASE-006 standing;
   - receiving convention for DEL-09-12's observations.
2. **Verification design** VER-001…008 against this run's own graph as the
   worked case.

**Leave out:** product records and views (PKG-06); any change to Root's graph
template or SPEC; a new register or parallel tracking system (V4-OPS-31).

---

# Part 3 — DEL-10-03 Shared commitments and consumer responsibility account

DOC_UPDATE; "App/shared renewal definition owner with affected consumer
owners"; INITIALIZED; no `Design/` folder; `MEMORY.md` has one SCA-V4-002 entry.

## 3.1 Obligations (22: 3 OUT, 7 REQ, 6 AC, 6 VER)

Basis keys: **BASIS** Group3 (SOW-230…234); **HTML** d1/d2/d7; **OWNER** U1/U4/U5;
**PRD** V4-CST-04, V4-WF-03/05, V4-AUT, V4-REC; **ARCH** §§2–5; **HOST** §1–4;
**OPS** V4-OPS-01/10–14/31–34, §§5–7; **OPEN** OI-013/014/017/018/024, DEP-006;
**SEED**; **PRACTICE**. CLM-001…007, TBD-001…003, AX-001…005 read, not counted.

| Item | One line | Rests on |
|---|---|---|
| OUT-001 | Responsibility map: concepts, guidance, product commitments; meaning, standing, owner, consuming contract, open allocation | BASIS, HTML d1–d2, ARCH §5, HOST §1 |
| OUT-002 | Promise trace: affected commitment → current wording/decision → SoW → derivative/interface/evaluation | HTML d1, PRD §0, OPS-01/12/13 |
| OUT-003 | Historical applicability and active consumer/packaging/tool-path account, for PKG-11 | HTML d1/d7, ARCH §5, OPS-14, DEP-006 |
| REQ-001 | Cover all three classes and each affected owner's contribution; trace, not take over | SOW-230, HTML d1 |
| REQ-002 | Every promise affected by relocation or changed supply reaches SoW, derivative and verification; a moved file or schema pass discharges nothing | SOW-231, PRD §0, OPS-01/13 |
| REQ-003 | Classify historical statements against later decisions; Root-first hierarchy, thin-loop default, fixed shared TypeScript allocation kept as history | SOW-232, HTML d1/d7, SEED, OPS-11…14 |
| REQ-004 | Before a placement/supply change is relied on, check packaging selectors, instruction consumers, resolution/supply and tool paths against current source; static vs runtime kept apart | SOW-233, HTML d1/d7/e1, ARCH §5, OPS-14 |
| REQ-005 | Start from compatible workflow/checkpoint, identity, human-act, catalog and evidence contracts; keep Codex/Tauri/minimal loop on a person-chosen model (as amended by SCA-V4-002); justify any shared implementation; placement open under TBD-001 | SOW-234, HTML d2, ARCH, SCA-V4-002 |
| REQ-006 | No act owned by PKG-02/03/04/05, PKG-11, PKG-10 siblings, the SWBPIPE owner, the person or the professional | allocation rows |
| REQ-007 | Every claimed act keeps actor, subject, evidence, custody; no inferred acceptance or adoption | PRD V4-AUT/REC, HTML d3/d7, OPS-14 |
| AC-001…AC-006 | Map coverage; promises retained; applicability per historical statement; consumer/packaging checks or explicit hold; compatible obligations mapped with direction kept; act attribution | REQ-001…007 |
| VER-001…VER-006 | Map vs SOW-230 and CLM rows; two-way promise comparison; applicability vs SEED and later direction; selector/tool-path chain from CLM-007 (no network or migration); interface review against PKG-02…05; exclusion and attribution examination | AC-001…006 |

**Overtaken or re-read.** REQ-005 was revised by SCA-V4-002 (AX-005 records
it). CLM-007's lead is App v3's packaging script; the v4 counterpart now
exists as a proposed design: PKG-v0.2 rows P-2 (`Contents/Resources/workflows/`,
DEL-02-02) and P-3 (`Contents/Resources/instructions/`, product `AGENTS.md`,
role files, `roles.json`, DEL-02-04). TBD-002's OI-017 is overtaken as in
Part 1.

## 3.2 Joins

| Row(s) | Consumer → supplier | Type; maturity / satisfaction | DAG-004 |
|---|---|---|---|
| DEP-10-03-008 (mirror DEP-02-01-040) | DEL-10-03 → DEL-02-01 | INTERFACE; INITIALIZED / TBD (mirror PENDING) | admitted |
| DEP-10-03-009 (mirror DEP-02-03-040) | → DEL-02-03 | INTERFACE; INITIALIZED / TBD | admitted |
| DEP-10-03-010 (mirror DEP-02-04-018) | → DEL-02-04 | INTERFACE; INITIALIZED / TBD (mirror PENDING) | admitted |
| DEP-10-03-011 (mirror DEP-03-01-042) | → DEL-03-01 | INTERFACE; INITIALIZED / TBD (mirror PENDING) | admitted |
| DEP-10-03-012 (mirror DEP-03-02-033) | → DEL-03-02 | INTERFACE; INITIALIZED / TBD | admitted |
| DEP-10-03-013 | → DEL-04-01 | INTERFACE; INITIALIZED / TBD | admitted |
| DEP-10-03-014 (mirror DEP-04-03-045) | → DEL-04-03 | INTERFACE; INITIALIZED / TBD (mirror PENDING) | admitted |
| DEP-10-03-015 | → DEL-05-01 | INTERFACE; INITIALIZED / TBD | admitted |
| DEP-10-03-016 | → DEL-05-02 | INTERFACE; INITIALIZED / TBD | admitted |
| DEP-10-03-017 | → DEL-10-01 | PREREQUISITE; INITIALIZED / TBD | admitted |
| DEP-10-04-007 (mirror DEP-10-03-020) | DEL-10-04 → DEL-10-03 | PREREQUISITE; INITIALIZED / TBD | admitted |
| DEP-11-01-008 | DEL-11-01 → DEL-10-03 | PREREQUISITE; INITIALIZED / TBD | admitted |
| DEP-11-02-008 | DEL-11-02 → DEL-10-03 | PREREQUISITE; INITIALIZED / TBD | admitted |
| DEP-10-03-018, 019 | current packaging source; PKG-11 | PREREQUISITE/HANDOVER; TBD | excluded, NOT_TOPOLOGICAL |

**What the supplier Design files already provide for DEL-10-03, by section.**

- WD-v0.9 §9 "Shared contract/component responsibility map (OUT-003; REQ-005;
  AC-005)" and §8 receiver row: "DEL-10-03: the workflow, role and checkpoint
  semantics (§4.3, §5) and the shared allocation (§9)". U-17: every §9 row's
  owner confirmation is "None"; the internal half is a confirm-or-object
  request; "The SWBPIPE half waits with the host joins (DECISION-3)."
- EXEC-v0.7 receiver row: "DEL-10-03: the workflow compatibility and
  checkpoint receiving obligations (§2 …".
- ROLE-v0.2 O-5: "DEL-10-03: supply obligations | DEP-10-03-010 | §3–§6".
- C-v0.8 §8 "Three-surface responsibility map — skeleton", two rows naming
  "DEL-10-03 account" with OI-013/OI-014 unresolved.
- P-v0.8 §13: "Provide to | DEL-10-03 … | Proposal, validation and outcome
  obligations for the shared responsibility account: §1 and this table".
- ACT-POLICY-v0.10 consumer table: "DEL-10-03 | DEP-10-03-013 | none | Not
  mapped in detail".
- RS-v0.10 consumer row: "§2 authority rules, §13 format, §14 writer and
  reader sequences … no common service or implementation is inferred".
- LOOP-v0.9 §10.4 receiver row (§5, §10, §12) and §10.1 "Responsibility map";
  PANEL-v0.9 §6 "Reusable-component allocation account".

**Inference.** The responsibility content already exists in nine supplier
files; DEL-10-03's map is an index over them plus the cross-project
(Root/Runtime/App v3/Piping) consumer layer none of them covers.

**Cycle guard (computed).** DEL-10-03 reaches 13 deliverables on the admitted
layer and 21 on both, including all of PKG-01…05, DEL-09-01 and DEL-09-09. Any
new row making one of those consume DEL-10-03 (or DEL-10-02/10-04, which reach
it) forms an SCC. PKG-06, DEL-09-05, 09-11 and 09-12 do not reach PKG-10.

## 3.3 Proposed contract changes still open

None targets DEL-10-03. Related, applied: SC3-02-04-9 and R3-02-04-a..b (DEL-02-04
names DEL-10-03 as receiver; mirror row added); RP1-MX-0203 (DEL-02-03 mirror).

## 3.4 Open items and who decides

| Item | Shapes the design now? | Answer the texts support | Who decides |
|---|---|---|---|
| **E3-1 Which promises are "affected"** | Yes: population of OUT-002 | Those whose supply or placement changes between v3/Root practice and v4: workflow/role/checkpoint semantics (PKG-02), catalog and proposal contracts (PKG-03), human acts and records (PKG-04), host receiving (PKG-05), instruction supply (OI-018 remainder; D-GOV-52), packaging (PKG-v0.2 P-2/P-3). Bounded by the nine admitted supplier rows, DEP-006 and OI-013/014/018/024 (SoW: "A promise is an accepted obligation, not every incidental historical mechanism") | **DERIVED**; O-E's ordinary decision, stated |
| **E3-2 Unconfirmed shared allocations** (WD U-17; OI-014) | Yes: OUT-001 standing column | OI-014's owner is "App/shared contract owners", that is, the deliverable owners, not the person. The map records each row's confirmation state; confirmations come at the next comparison. The SWBPIPE half waits (DECISION-3) | **INTEGRATION** |
| E3-3 OI-013 loop placement | No (carried) | "Shared contract owner with SWB implementation owner, Before shared/host implementation boundary contracts" | External; waits with host joins |
| E3-4 OI-024 staged adoption/retirement | No (carried) | "Owner with affected consumers, Before each adoption/retirement decision"; PKG-11's domain | Reserved jointly when triggered |
| E3-5 Cross-project consumers (Root, Runtime, App v3, Piping, PEC) | Yes: OUT-003 rows | Static traces now (repository read-only); receiving adoption remains each owner's (DEP-006: "NOT_ADOPTED_BY_THIS_DRAFT") | **DERIVED** |
| E3-6 ACT's "Not mapped in detail" row | Little | O-E maps from ACT's text; any row edit in ACT is O-A's under R23-21 | Row-level, not structural |

## 3.5 What exists to build on

The nine supplier sections above; PKG-v0.2 P-2/P-3 and the R23-2 seam
direction ("DEL-02-02, 02-04 or 01-04 → DEL-01-06 … never the reverse"); the
D-GOV-52 notice as a worked instruction-consumer example (App v4 substantive;
App v3 and Runtime informational; none to Piping or PEC, per
OWNER_DECISIONS_2); the App v3 script's `ROOT_FILES`, `PRODUCT_AGENTS_SOURCE`
(`projects/chirality-app-dev/instructions/AGENTS.md`), `DOC_FILES`,
`TOOL_FILES` (CLM-007; evidence only); the sibling projects
`chirality-runtime`, `chirality-piping` and `pec`, each with its own
`AGENTS.md`, readable for static traces.

## 3.6 Design scope for this pass

1. **`Design/RESPONSIBILITY_ACCOUNT.md`**:
   - population bound (E3-1) with the reason for each inclusion;
   - responsibility map indexing the nine supplier sections by class, with
     standing and confirmation state, without restating them;
   - two-way promise trace: accepted source → current decision → SoW →
     Design label/section → VER; unavailable derivatives explicit;
   - historical applicability rows (Root-first hierarchy, thin-loop default,
     shared TypeScript allocation) with preserved original references;
   - consumer/packaging/tool-path account: v3 script (historical), v4 P-2/P-3
     (proposed), D-GOV-52 (applied example), Runtime/Piping/PEC static
     consumers; outstanding checks with their point of need;
   - handovers to PKG-11 (DEP-10-03-019) and DEL-10-04 (DEP-10-03-020).
2. **Verification design** VER-001…006, including the two-way comparison as a
   script over the supplier files' receiver rows.

**Leave out:** placement decisions (OI-013/014); adoption or migration acts
(PKG-11, DEP-006); network experiments (VER-004 forbids them); repository
rearchitecture.

---

# Part 4 — DEL-10-04 Project production dependency DAG

DATA_MODEL_CHANGE; "App project dependency owner; owner accepts examined
current DAG"; INITIALIZED; no `Design/` folder. Read only: no `_DAG`, case,
register or ScopeOfWork file is touched.

## 4.1 Obligations (29: 2 OUT, 9 REQ, 9 AC, 9 VER)

Basis keys: **B1** Group3; **B2** OPS; **B3** `_COORDINATION.md`; **B4** owner
directions J–O, HTML 01/05/06/07, PRD §0; **B5** `project-dag` and resources;
**B6** manuals; **B7** `construct-local-work-graph`; **B8** External_Dependencies,
Open_Issues; **B9** HOST V4-HI-60–63, ARCH §6, EXAM §§1–2; **B10** SoW standard.
CLM-001…003, the DEP-001…006 interface account, TBD-001/002 and AX-001…003
read, not counted.

| Item | One line | Rests on |
|---|---|---|
| OUT-001 | Identified DAG and interface registers: inventory, edge meaning and direction, admitted, candidates, exclusions, provenance, external contributions | B1, B5, B6 |
| OUT-002 | Closure/examination and acceptance evidence: source/tool identities, accounting, independent review, decisions, immutable version, handoff, currency | B1, B3, B5, B6 |
| REQ-001 | Objective, semantics, direction, tracking, completeness, selection rules; inventory frozen independently of register availability | B1, B3, B5, B6 |
| REQ-002 | Each relationship's fields and provenance; DECLARED vs extracted; mirrors without double counting | B3, B5, B6 |
| REQ-003 | External contributions and open matters with owner/point of need; pending external delivery does not block acceptance | B1, B3–B6, B8, B9 |
| REQ-004 | Inventory and coverage before topology; admitted layer acyclic and strict-audited; every active row once; unresolved cycles held, non-gating | B3, B5, B6 |
| REQ-005 | Basis and version checkpoints as decision packages; independent examination by a non-assembler | B3, B5, B6 |
| REQ-006 | Record actual decisions with actor, custody, subject hashes; immutable accepted version; pointer moves only to it | B1, B3, B5 |
| REQ-007 | Currency: unchanged, evidence drift, departure, incomplete; DAG pending; successor or rejection by the human | B5–B7 |
| REQ-008 | INITIALIZED is contract maturity only; no self-bootstrap; acceptance does not pass 30% or satisfy inputs | B1–B3, B5–B7, B10 |
| REQ-009 | No act owned by DEL-10-01/02/03, external suppliers, source owners or the human | B1, B3–B9 |
| AC-001…AC-009 | One per REQ, as stated | REQ-001…009 |
| VER-001…VER-009 | Inventory/basis comparison; row provenance and fidelity; interface account vs current external rows; closure and `audit_dag.py --canonical --strict`; independent review; decision custody vs presented hashes; currency comparisons; readiness/reliance cases; boundary-owner check | AC-001…009 |

**Overtaken by actual production (states).** The SoW defines a future
result; it has since been produced four times:

- DAG-001, accepted with the 30% package (owner: "I have reviewed and now
  approve the 30% package …"); DAG-002 and DAG-003 as successors; DAG-004
  accepted 2026-10-03 ("I accept DAG-004."), 129 admitted arcs, 83 held in six
  SCCs, 355 exclusions, 41 nodes, no exemptions.
- `_DAG/_LATEST.md` names DAG-004 in SPEC §11.2 form; seven SCC cases under
  `_DAG/cases/`; closure snapshots and eight currency observations under
  `_Evaluation/`.
- The latest currency observation is CURRENT_WITH_EVIDENCE_DRIFT, "no
  deliverable is DAG pending"; my recheck of DAG-004's source manifest agrees
  (§0).

**Inference.** OUT-001 and OUT-002 exist. DEL-10-04's remaining design work is
the evidence account that maps each REQ/AC/VER to those records, plus the
ongoing currency obligation (REQ-007) through the rest of this pass.

## 4.2 Joins

| Row(s) | Consumer → supplier | Type; maturity / satisfaction | DAG-004 |
|---|---|---|---|
| DEP-10-04-005 | DEL-10-04 → DEL-10-01 | PREREQUISITE; INITIALIZED / TBD | admitted |
| DEP-10-04-007 (mirror DEP-10-03-020) | DEL-10-04 → DEL-10-03 | PREREQUISITE; INITIALIZED / TBD | admitted |
| DEP-10-04-006 | DEL-10-04 → DEL-10-02 | PREREQUISITE; INITIALIZED / TBD | **held**, SCC-005 / SCC-CASE-006 |
| DEP-10-02-012 (mirror DEP-10-04-014) | DEL-10-02 → DEL-10-04 | CONSTRAINT; INITIALIZED / TBD | **held**, SCC-005 / SCC-CASE-006 |
| DEP-10-04-008…013 | Inventory, local contracts and declarations, external records, project-dag method, independent examination, the owner's decisions | TBD / TBD | excluded, NOT_TOPOLOGICAL |

**Existing Design files assume of DEL-10-04:** FR-v0.1 §1 ("They are not the
project DAG (DEL-10-04, V4-OPS-02)"), §10, and the schema's `projectDagRef`.
No Design file depends on DEL-10-04 producing anything new.

**Inference on DEP-10-04-007.** DAG-001…004 were accepted without a DEL-10-03
account. DAG-004's reading rule 5 ("A missing input constrains the stated
part of the work that needs it") and REQ-008 allow that: the arc constrains
only the part of graph production that uses responsibility relationships.

## 4.3 Proposed contract changes still open

None. The SoW's present-tense "Establish … before the 30% position" is
fulfilled in fact; whether its wording should now read as maintenance is a
next-amendment note (R23-11), not a change this pass needs.

## 4.4 Open items and who decides

| Item | Shapes the design now? | Answer the texts support | Who decides |
|---|---|---|---|
| **E4-1 Design = evidence account over existing records** | Yes | SETTLED by `project-dag` and SPEC §5.4; the account maps obligations to DAG-001…004, cases, closure and currency, and reruns the read-only checks (manifest; `audit_dag.py --canonical --strict` to scratch) | **DERIVED** |
| **E4-2 Currency during tranche 2** | Yes: REQ-007 procedure | Owners run reach before proposing any row (R23-2); register changes are audited for currency at the pass closeout; a departure makes the affected deliverables DAG pending and needs a successor | The successor's acceptance is reserved to the person (§5.2); triggered only by a departure |
| E4-3 SCC-CASE-006 | No | R1 stands; see E2-9 | No ruling needed |
| E4-4 Interface account DEP-001…006 | Little | Recheck against current External_Dependencies (DEP-002's D108 facts, DEP-003 with OI-023/026); record, decide nothing | **DERIVED** |
| E4-5 Lifecycle | No | Move the four PKG-10 deliverables INITIALIZED → IN_PROGRESS when their design starts, as R23-28 did for tranche 1. CHECKING remains human-only (`write_status.sh`) | **INTEGRATION**, HELP_HUMAN's act |

## 4.5 What exists to build on

`project-dag` (WORKFLOW.md pinned in CURRENT_EXECUTION_BASIS; resources hashed
in §0); `audit-dep-closure`; `scc-resolution-case`; SPEC §5.4 and §11.2;
`tools/coordination/audit_dag.py`, `analyze_dep_closure.py`,
`materialize_local_dependencies.py`; `tools/validation/validate_scc_resolution_case.py`;
DAG-004's handoff (reading rules, guards, waits).

## 4.6 Design scope for this pass

1. **`Design/DAG_ACCOUNT.md`**: obligation → evidence map for OUT-001/002 and
   REQ-001…009; results of the read-only reruns, with tool identity,
   command, exit and input hashes (VER-004); the currency procedure for this
   pass and its closeout (E4-2); SCC-CASE-006 standing; the interface account
   recheck; the handoff to DEL-10-02 and `construct-local-work-graph`.

**Leave out:** any write to `_DAG`, cases, registers or `_Evaluation`; any
successor preparation unless a departure appears.

---

# Part 5 — Across the four deliverables

## 5.1 External parties: what PKG-10 can do now, and what waits

| Party | Bears on | Designable and evidenced now | Waits |
|---|---|---|---|
| SWBPIPE | DEL-10-03 (OI-013; WD U-17 SWBPIPE half); DEL-10-04 DEP-001 | The account records the open allocation and its point of need | Confirmations and placement, with the host joins (DECISION-3 of `APP-V4-SWBPIPE-INTAKE-20260928` defers them) |
| PEC | DEL-10-04 DEP-002; DEL-10-03 consumer row | Recorded standing (D108 limits) only | Nothing in PKG-10 needs PEC |
| Domains | DEL-10-04 DEP-003, OI-023/026 | Recorded only | Nothing in PKG-10 needs Domains |
| Connectors | None | — | — |
| Practitioners | DEL-10-02 ← DEL-09-12 (DEP-09-12-012) | The receiving convention for method observations | Actual observations, after practitioner validation (S2-F) |
| Root/Runtime/App v3/Piping consumer owners | DEL-10-03 OUT-003; DEL-10-01 → DEL-11-02 | Static source traces from this repository | Receiving adoption, each owner's (DEP-006) |
| The person | §5.2 | Packages prepared in advance | Acts at their points of need |

## 5.2 Items genuinely reserved to the person

None needs the person now. Five acts are reserved by the texts and arise only
at their own points of need:

1. **Acceptance of a successor DAG, or rejection of a departure.** SPEC §5.4:
   "Authority comes from the human's acceptance"; DEL-10-04 CLM-001: "The human
   owner decides the concrete graph basis and version acceptance, consequential
   cut/merge treatments, and acceptance or rejection of departures." Trigger: a
   departure. None now.
2. **Disposition of practice notes at the stage discussion.** DEL-10-02 REQ-007:
   "the manager shall bring the relevant practice notes to the owner and
   preserve their actual disposition"; ResponsibleParty "human at applicable
   stage decisions". Point of need: the 60% phase review, which the person
   assesses (LOOP_INIT: "The human assesses the 60% position").
3. **A consequential departure from adopted practice.** DEL-10-01 CLM-004: "The
   owner decides consequential adoption/departure"; V4-OPS-13: "Prepare
   consequential departures for the human". Only if E2-4 is ruled a departure.
4. **Manual revision authorship (OI-020)**, Owner, "Before revising manuals from
   feedback"; and **consequential manual gaps (OI-019)**, Owner with execution
   manager, "When consequential gap affects selected work". Neither triggered.
5. **Applying a Root instruction change** (OWNER_DECISIONS.md: "HELP_HUMAN brings
   the owner only acts the governing texts reserve to the person, such as
   applying an instruction change"). PKG-10 proposes none (§5.4).

## 5.3 Items proposed for HELP_HUMAN to rule

| ID | Proposed answer | Label |
|---|---|---|
| E1-1, E2-1, E4-1 | PKG-10's outputs live in the existing project records; each deliverable gets one thin Design file that maps obligations to them, checks them and fills gaps | DERIVED |
| E1-2 | The "project-definition manager", "undertaking manager" and "project dependency owner" are HELP_HUMAN acting in the WORKING_ITEMS function; O-E prepares, the manager writes coordination records such as CURRENT_EXECUTION_BASIS | INTEGRATION |
| E1-3 | Later undertakings rely on the recorded manual pins while bytes are unchanged and cite them; a changed edition gets a deliberate re-pin record first | DERIVED |
| E2-2, E2-3 | Project-local practice-note convention in run records, linked from graph nodes; seeded with tranche 1's recorded lessons | DERIVED |
| **E2-4** | V4-OPS-34's independence is met for design units by a separate non-authoring session with identity reported; the Codex preference binds product candidate examination (EXP §7, R23-12); the pass-4 practice is a recorded observation for the 60% discussion. If HELP_HUMAN rejects this reading, it becomes reserved item 3 | INTEGRATION |
| E2-8 | Per-run capability and check account as a short section of DISPATCH/BRIEFS | DERIVED |
| E3-1 | Bound the affected-promise population to the nine supplier rows, DEP-006 and OI-013/014/018/024 | DERIVED |
| E3-2 | Unconfirmed shared allocations are the deliverable owners' to confirm (OI-014), recorded with their state; SWBPIPE half waits | INTEGRATION |
| E4-5 | INITIALIZED → IN_PROGRESS for DEL-10-01…04 when design starts, by HELP_HUMAN (R23-28 precedent) | INTEGRATION |

## 5.4 Root instruction changes: where the App's version would need one

- **Fleet format as the method's graph format.** FR-D2 already records that
  adopting `chirality.fleet.record` for work graphs would change Root SPEC §9.8
  and `construct-local-work-graph` (S1-A S-7). **Recommendation:** no; PKG-10
  keeps the Markdown graphs.
- **A reusable practice-note field.** Adding one to
  `construct-local-work-graph/resources/work-graph-template.md` is a Root
  workflow revision (`create-workflow`). **Recommendation:** keep it
  project-local until the stage discussion shows it is useful.
- **Manual revisions from feedback** (OI-020): Root `docs/alignment-manual/`;
  the owner's.
- **Precedent for the route:** D-GOV-52 (R23-30). The packet was prepared under
  direction, the owner approved application, notices went out, and App v4
  recorded its adoption.

## 5.5 Structural questions that could force restructuring an earlier Design file

- **SQ-E1 `projectDagRef` is a free string** in FR-v0.1's graph revision
  ("…or 'none'"). If the App product must read a user project's accepted DAG
  with its currency (SPEC §5.4's blocker rules), a structured reference
  (pointer, version, currency observation) would be needed. That is an
  additive schema change for O-A, not a restructure, and no PKG-10 obligation
  requires it. Allocation note: no deliverable visibly owns "the App reads a
  user's project DAG"; PKG-06 excludes the DAG and PKG-10 is project practice.
  Worth a look by O-A, low risk.
- **SQ-E2 Two shared-allocation maps.** WD §9 (DEL-02-01 OUT-003) and DEL-10-03
  OUT-001 both map shared responsibility. If DEL-10-03 restated rather than
  indexed, the two would drift; if it finds a conflict, WD §9 rows change. That
  is row-level, not a restructure.
- **SQ-E3 ACT-POLICY-v0.10's DEL-10-03 row** says "Not mapped in detail". Mapping
  it is a row in a shared file under R23-21, owned by O-A.
- **SQ-E4 Generalising E2-4 into EXP §7** would restructure EXP's review protocol.
  Recommendation: do not; EXP governs product candidates.
- **SQ-E5 Cycle guard.** Any row in which a PKG-01…05, DEL-09-01 or DEL-09-09
  deliverable consumes a PKG-10 deliverable forms an SCC (DEL-10-03 reaches all
  of them). The bundle seams (R23-2) and DEL-02-04's role supply must stay
  "PKG-10 reads them", never the reverse.

None of these is likely. The larger risk is the framing in §0.1: if HELP_HUMAN
or the owner expected PKG-10 to specify App product behaviour, every PKG-10
Design file would take a different shape. The early unit tests that premise.

## 5.6 Proposed early unit for the cluster

**EB-1: the project's execution basis, read cold.**

- **Premise carried:** PKG-10's results are thin accounts over existing
  project records, and those records are enough for a reader who was not
  there to recover:
  - the project's basis and governing methods;
  - its actual position;
  - which acts were the person's.

  If that fails, all four designs change shape, not just DEL-10-01. The unit
  also carries the pin-currency rule (E1-3) and the actor ≠ recorder
  distinctions that DEL-10-02 and 10-04 reuse.
- **Path:**
  1. Authoritative inputs: CURRENT_EXECUTION_BASIS, the Group1/2/3 and setup
     decisions, the SCA Group-3 snapshots, the DAG acceptance records and this
     run's OWNER_DECISIONS files.
  2. O-E writes DEL-10-01 `Design/EXECUTION_BASIS.md`, §§ basis chain, pin
     table and application/departure table, with every hash recomputed by
     script at writing. This is the cheap check, placed where pin defects
     enter.
  3. An input-set manifest in RRM's format (`rrm.input-set-manifest.schema.json`,
     reused, not changed) lists the account and the files it links.
- **Consumption check:**
  1. HELP_HUMAN dispatches a fresh isolated reader, as for RR-E/RR-F, given
     only that manifest.
  2. The reader answers a question key declared before the read (the R23-19
     principle):
     - which manual editions and methods govern the current undertaking, and
       with what standing;
     - the project's development position and what the 60% assessment needs;
     - for three named decisions (Group3, DAG-004, D-GOV-52 application): the
       actor, the recorder, the exact subject and the custody;
     - which items remain open, with owner and point of need;
     - what an arriving setup or local-SoW author must use and must not redo.
  3. O-E compares the answers to the key. Misses are traced to the account or
     to the underlying records, not to the reader.
- **Second consumer:** O-F's use of the pin account for DEL-11-01 (admitted arc
  DEP-11-01-009), when its unit needs it.
- **Gate:** DEL-10-02's and DEL-10-04's accounts do not expand until EB-1
  passes. DEL-10-03's population bound (E3-1) can proceed in parallel; it
  depends on the supplier Design files, not on EB-1.

## 5.7 Counts

105 obligations: DEL-10-01 27, DEL-10-02 27, DEL-10-03 22, DEL-10-04 29 (OUT
11, REQ 32, AC 31, VER 31). Register rows touching PKG-10:
- rows in the four PKG-10 registers, all ACTIVE, anchors included: 22, 13,
  20 and 14;
- DAG-004 arcs: 18 admitted; 2 held, both in SCC-005;
- DAG-004 exclusions touching PKG-10: 27 (21 rows in PKG-10 registers, NOT_TOPOLOGICAL
  or MIRROR, and 6 supplier-side MIRROR rows).

## 5.8 Limits

- The four PKG-10 SoWs were read whole; the manuals only at the sections
  named; most supplier Design files only at the sections that name PKG-10.
- No tool was run except hashing, manifest checks and the scratch reach
  script; `audit_dag.py` was not rerun.
- The run's BRIEFS, DISPATCH, OWNER_DECISIONS_2 and WORK_GRAPH were read as
  uncommitted working bytes (hashes in §0); a later commit may change them.
- `SCC-CASE-006/Case_Contract.md` contains an absolute home path. I saw it
  and did not change it; whether it falls under the redaction record is for
  HELP_HUMAN.
