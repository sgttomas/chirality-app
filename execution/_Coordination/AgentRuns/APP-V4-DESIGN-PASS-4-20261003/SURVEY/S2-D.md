# S2-D — Scoping survey: DEL-07-01, DEL-07-02, DEL-08-01, DEL-08-02, DEL-09-10

Run `APP-V4-DESIGN-PASS-4-20261003`, node T2-S, survey S2-D (Type 2 TASK,
Claude Opus 5.5, high effort). Read-only on project state; this file is the
only write. Written 2026-10-04 at repository HEAD `d2929fd62b`. It claims no
SWBPIPE, PEC or Domains join, witness, delivery or adoption, and changes no
register, ScopeOfWork, status, graph, DAG, basis or Design file.

Paths are relative to `projects/chirality-app-v4/execution` unless they start
with `docs/` (then `projects/chirality-app-v4/docs/`) or `pec/` (then
`projects/pec/`). **States** marks what a file says; **Inference** marks mine.
Rulings are cited by ID (R23-21 item 1).

Labels for "who decides" (brief S2, change 2):
- **RESERVED**: a governing text reserves it to the person (quoted).
- **EXTERNAL**: another party's contribution or act (PEC owner, Domains
  provider, SWBPIPE owner).
- **SETTLED**: an existing ruling or decision already answers it.
- **DERIVED / INTEGRATION**: my proposed answer, for HELP_HUMAN to rule.
- **ORDINARY**: the deliverable owner's design decision.

---

## 0. What was read and how

| Input | How read | Identity (sha256, first 16 hex, `shasum -a 256`) |
|---|---|---|
| Run `BRIEFS.md` (Common rules; S1; S2), `WORK_GRAPH.md` ("Coordination", nodes), `R23_RESOLUTIONS.md` (all), `OWNER_DECISIONS.md`, `OWNER_DECISIONS_2.md`, `RECEIPT.md`, `DECISIONS_PENDING.md`, `DISPATCH.md` (tail) | Whole | `53f8d877b6ed324b`, `34b2e489e4e9f82b`, `fafa6ed7364ca930` (R23-1…R23-30, as first read), `e4350f61a93edf0d`, `5744a66813b57946`, `a45055e25070d981`, `e4284bc29f361481`. **BRIEFS, WORK_GRAPH, OWNER_DECISIONS_2 and DISPATCH are modified in the working tree** (`git status`); the hashes are of the working bytes I read. R23_RESOLUTIONS.md then gained **R23-31** (on S2-E) in the working tree while this survey was being written; read at `06021e6c0f77d5f0` (`git diff`: 47 lines appended, nothing else changed). It bears here only on S-2 |
| `workflows/coordinated-knowledge-work/WORKFLOW.md` | Whole | `44049bcd38b88378…`, equal to the pin in OWNER_DECISIONS.md |
| Tranche-1 surveys `SURVEY/S1-A.md`, `S1-B.md`, `S1-C.md` | S1-A whole structure and Part 3; S1-B/S1-C structure | `616568603f93a62c`, `1b4de1cb45f22479`, `6b2c3032c9a83b6d` |
| The five deliverables: `ScopeOfWork.md`, `Dependencies.csv`, `_STATUS.md`, `_CONTEXT.md` (DEL-08-01 `MEMORY.md`) | Whole; registers by Python `csv` | SoW: 07-01 `5e2fba1d2191d978`, 07-02 `6b618f9a0300794b`, 08-01 `df2795869011f936`, 08-02 `43a769703f235b26`, 09-10 `a976bf18fba98d13`. Registers: `62fc67a92d230f27`, `42b737be974b711a`, `69bc284d0f71ed0d`, `18b0ab8b79e9faac`, `98b586fb2c9432ac`. **All ten equal DAG-004's `SOURCE_MANIFEST.sha256` entries** (grep). All five `_STATUS.md`: INITIALIZED, 2026-09-27 |
| SoW history (`git log`) | — | All five INIT at `ddd721a90a`. Only DEL-08-01 was later revised: SCA-V4-001 (`340ecf341f`; CLM-003 revised, AX-005 added, DECISION-5). SCA-V4-002 and SCA-V4-003 touched none of the five SoWs, so R23-5 re-pins have no SCA-V4-003 block to read |
| `_DAG/_LATEST.md` → DAG-004; `HANDOFF_STATE.md`; `DependencyEdges.csv`, `CandidateEdges.csv`, `ExcludedRows.csv` | Handoff by grep; CSVs by script | `_LATEST` `b9353a41fe9765a3`; HANDOFF `3c374f5e9fa4cfaa`; edges `c43033742df768a6`, `2bfff10e3094d7fd`, `45f55e76ecf7c9aa`. `MANIFEST.sha256` passes. Reach over both layers computed by my own script (canonical arc = consumer → supplier; UPSTREAM keeps the row's order, DOWNSTREAM reverses it). I found no project-named "reach script" file; whoever proposes a row should rerun the designated one (R23-2) |
| `_DAG/cases/SCC-CASE-005/` (Case_Datasheet, Open_Questions, Case_QA, Handoff) | Whole | Datasheet `53fe8ecadb6975d6`; Open_Questions `8cdf25545060886f` |
| `_Decomposition/Open_Issues.csv` (OI-001, 002, 006, 012, 018, 021, 022, 023, 026); `External_Dependencies.csv` (DEP-002, DEP-003) | Rows by script | `9c2d916c277f8ce4`; `055703d9a7147ab9` |
| SCA-V4-003 `AMENDMENT_PACKET/LEDGER.csv`; SCA-V4-001 `Amendment_Actions.csv`; pass-2/3 `closeout/` | Script over DEFER/DROP rows; grep for DEL-07/08/09-10 | Ledger `e28661cdf3375e15` |
| Basis: `docs/PRD.md` V4-HOST-02, V4-CON-01…05, §3.1 (V4-EXT-01), §8, OQ-02/03; `docs/HOST_INTEGRATION.md` V4-HI-60…65, §8.1; `docs/ARCHITECTURE.md` V4-ARC-22; `docs/EXAMINATION.md` §2 (EXM-01…05), V4-EXM-30…32; `docs/OPERATING_METHOD.md` §6 | Clause text | PRD `bb6e786f7a6c01dc`, HOST `d4331c39db7f452c`, ARCH `317d5789272c5206`, EXAM `471798bc2f2dc020`, OPS `98836b5240ed235e` (the pins the Design files carry; `git log -- docs/` shows only SCA-V4-001/002 commits since) |
| Accepted-basis acceptance: `OWNER_DIRECTIONS.md` J/U1…O/U5; `DECISION_BRIEF.html#d6`; `Changes/APP-V4-CLARIFICATION-20260927/DIRECTION.md` | Whole; d6 text extracted by script | `72fc5d9c8d8ebb38`, `02d38cb18041c529`, `78d3aa2e7ac0e702` |
| Earlier owner records: FIRST-INCREMENT DECISION-1 (D1, D2, D3); SWBPIPE-INTAKE DECISION-3; DESIGN-PASS-3 DECISION-L (L-3, L-7) | At the cited items | `a9869129753631b8`, `5fd780bf90a4d517`, `8a5d11149045770d` |
| `_Coordination/HANDOFF_SWBPIPE_DOMAINS.md`; `_Coordination/PEC_UPSTREAM_COMPARISON_2026-09-27.md`; DEL-09-06 `RELAY_ANSWERS_SWBPIPE.md`, `FACTS_SQ01_SQ32.md` (data only) | Whole / grep for Domains, PEC | `09c816dce2ed67ba`, `a8b8fd9c7d898b53`, `afb6e063e7e5dfcc`, `733fb88a701317be` |
| Supplier and sibling Design files (tranche 1 and A16 rows): EXP-v0.2, SQ-v0.2, DAC-v0.1, LHQ-v0.1, TOP-v0.1, DOS-v0.1, RRM-v0.1, PKG-v0.2, FR-v0.1, FV-v0.1, DV-v0.1 (DECISION_VIEW), ACT-POLICY-v0.10, RS-v0.10, AAC-v0.3, GUIDE-v0.7 | grep for `DEL-07-0`, `DEL-08-0`, `DEL-09-10`, `PKG-07`, `PKG-08`, `PEC`, `Domains`; hits read in context; EXP §2–§3 read | EXP `ff0187dafd9e1f02`, SQ `3e5d0f12c6190710`, DAC `1fc4fd272c4f155c`, LHQ `20361a0be76904d4`, TOP `f82a58f6f0681f20`, DOS `b2ffba7135652c9e`, RRM `fcaa654437127306`, PKG `0d8d14d2ce08d859`, FR `3e3ba16c9c73f941`, FV `15e25a24f53feb2a`, DV `b944b0be081a56a4`, ACT `1bf0ce8e413d2b8f`, RS `2e7afb1bb8b872c0`, AAC `de39976e93500c94`, GUIDE `a656682e2584ea86` |
| First-increment and pass-3 files naming these deliverables or their surfaces: LOOP-v0.9 (§5.1.1, §5.3, N-OPEN-3, §10.4), WD-v0.9 (§4.2.1, §8), HOSTING-v0.9 §6.8, NPTD (§6 tool row), ADAPTER (OC-2, OC-3), VERSION_ADVANCE_0.160.0 | Sections cited | LOOP `2bac33a883b176e2`, WD `262c9e5417cf67b5`, HOSTING `5401f26d9a2a739a`, VERSION_ADVANCE `0dee021d7dc42596` |
| Generated protocol types at 0.158.0 | The committed JSON Schema bundle `…/generated/0.158.0/json-schema/experimental/codex_app_server_protocol.v2.schemas.json`, by script (MCP definitions) | `34f28a486d00fbd2` (equal to the hash NPTD cites). Pin basis of this survey: **0.158.0**; 0.160.0 is checked design-compatible (R23-22). VC's Δ2 (`mcpServerStatus/list serverName`, additive) touches an MCP surface named here; nothing below relies on it. VC did not re-check the OBS-1 MCP route at 0.160.0 (VERSION_ADVANCE item 8) |
| PEC (external; data, not commitment): `pec/docs/PRD.md` (PEC-K-01…03, K-11, PEC-ORI-001…007, PEC-API-001…007, PEC-SVC-004); `pec/…/DEL-04-03…/ScopeOfWork.md` (CLM-003, CLM-019, REQ-016…023); `pec/…/DEL-08-06…/ScopeOfWork.md` (REQ-001, REQ-013…015, TBD-003…007); `D-PEC-108` | Clause text | PRD `ae49b8065698f003`; DEL-04-03 SoW `10819cb2ea90c766` (status INITIALIZED); DEL-08-06 SoW `aecc513161c1e8a5` (status INITIALIZED); D108 `dcfd7aaa3be28e8e`. `git log ffb2b6289..HEAD -- projects/pec` is **empty**: no PEC change since the D108 pin the App's DEP-002 records; D108 is the newest PEC decision file |
| Domains | `ls projects/`: no Domains project exists in this repository (consistent with "Domains knowledge develops outside this repository", CLARIFICATION) | — |
| App v3 exemplar (evidence only, never a v4 commitment): `chirality-app-dev/frontend/src/lib/harness/mcp/pec-bridge-client.ts`, `…/__tests__/integration/pec-bridge.integration.test.ts`, `docs/harness/reliance_boundary_register.md` (RB-PEC-ADAPTER) | Heads and rows | `337d320b5251525a`, `3944e5a586a9a496`, `efbe0fde26c17e20` |
| `loop/LOOP_INIT.md` (60% description) | Lines 135–156 | `3790159b4f60bb4f` |

Not read: PIN_SPIKE, OBS_1…3 directly (cited as HOSTING states them);
Design files with no connector mention (other than those named above) were
not searched for implicit assumptions.

---

## 0.1 Cluster facts that every part below relies on

**F-1 External parties, as the files state them now.**

- **PEC.** The App's DEP-002 is `OPTIONAL_RECEIVING_QUALIFICATION_UNESTABLISHED_AT_ffb2b6289`.
  D108 accepted the D1 bytes as-is, with RF-001 MAJOR retained and PEC
  DEL-00-01/AC-002 partly met. PEC's response-layer contract (DEL-04-03) and
  its agent tool surface (DEL-08-06) are **INITIALIZED**: no response, tool
  or release exists. What *is* fixed on PEC's side (states, PEC PRD):
  - the three-field stamp: examined-through SHA, generation time, per-feed
    freshness (PEC-ORI-003);
  - per-claim citations: file path, anchor and/or SHA (PEC-ORI-004);
  - a separate reliance envelope: pin, per-feed coverage/freshness with
    limitations, per-claim trust tier, and a file-fallback signal
    (PEC-ORI-007; DEL-04-03 REQ-016…023);
  - query kinds: orientation, deltas since a SHA, gate verdicts,
    decision-slate reads and presence reads (DEL-08-06 REQ-001; PEC-ORI-001,
    002);
  - a local-only service, Unix socket by default, with token-scoped access
    (PEC-API-001), and a read-only query interface "packaged for agent tool
    calls". "Enabling it in any harness, App or agent configuration is
    consumer-owned" (PEC-API-007; PEC-K-03);
  - "No governed act may require a PEC read or write" (PEC-K-01).
  Open on PEC's side: tool representation, operations and parameters, and
  the no-response signal's representation (DEL-08-06 TBD-003, 004, 006);
  the token mechanism and the transport (its AX-007).
- **Domains.** No provider, project, contract, corpus or deployment exists in
  this repository. DEP-003 is `OWNER_REPORTED_KNOWLEDGE_OUTSIDE_REPO_PARALLEL_LATER_JOIN`.
  Provider allocation is OI-026.
- **SWBPIPE.** Host joins are deferred (DECISION-3: "defer the host joins";
  the joins "wait until the owner resumes SWBPIPE UI-SUCCESSOR"; "App v4's
  60% work continues on App-side contracts, receiving definitions and
  fixtures"). SWBPIPE's answers say nothing about Domains, and no SWBPIPE
  record acknowledges App v4 (FACTS X-7). One answer bears on the Domains
  data boundary: SWBPIPE's DEC-051 "open residency" allows an
  owner-configured provider "with no app-side guard, gate or indicator"
  (RELAY answers, the "Conflict for the App to note" item; FACTS X-6).

**F-2 One SCC inside the cluster.** DAG-004 holds four arcs among DEL-07-01,
DEL-07-02 and DEL-08-01: 07-01 ↔ 07-02 and 07-02 ↔ 08-01 (SCC-004, case
SCC-CASE-005, `SCC_UNRESOLVED`). DAG-004 HANDOFF_STATE: "Candidate edges are
held and non-gating. They drive no blocker queue, wave, schedule, dispatch
readiness or readiness claim." SCC-CASE-005 recommends **R1** ("coordinated
contribution milestones … keep the four default arcs and all row evidence").
Its Q1 ("Does the human select R1 …, R2 … or R3?") is a project-dag
checkpoint question. CP1 confirmed tracking only (CaseState
EVIDENCE_ACCUMULATING). **Inference:** design can proceed on R1's four
milestones without a ruling, exactly as SCC-002's members do ("definition
proceeds on provisional versions", HANDOFF_STATE).

**F-3 Reach (DAG-004, both layers; my script).**

| Deliverable | Reaches (admitted) | Reached by (admitted) | Added by held arcs |
|---|---|---|---|
| DEL-07-01 | none | DEL-03-04, 06-01, 06-02, 09-05, 09-10 | Reaches 23 (through 07-02 → 08-01 → 05-01 → SCC-002); reached also by 07-02, 08-01, 08-02 |
| DEL-07-02 | none | DEL-03-04, 06-02, 09-05, 09-10 | as 07-01; reached also by 06-01, 07-01, 08-01, 08-02 |
| DEL-08-01 | DEL-01-05, 04-01, 05-01 | DEL-03-04, 08-02, 09-10 | reached also by 06-01, 06-02, 07-01, 07-02, 09-05 |
| DEL-08-02 | DEL-01-01, 01-05, 02-01, 04-01, 05-01, 08-01 | DEL-03-04 | — |
| DEL-09-10 | DEL-01-01, 01-05, 04-01, 05-01, 07-01, 07-02, 08-01, 09-01 | none | — |

Row tests (consumer → supplier; "cycle" means the supplier already reaches
the consumer):

| Possible row | Admitted layer | Both layers |
|---|---|---|
| DEL-07-02 → DEL-06-02 | **cycle** | **cycle** |
| DEL-07-02 → DEL-06-01 | none | **cycle** |
| DEL-07-01 → DEL-06-01 | **cycle** | **cycle** |
| DEL-05-01 → DEL-08-01 | **cycle** | **cycle** |
| DEL-04-01 → DEL-08-02 | **cycle** | **cycle** |
| DEL-07-01 → DEL-01-01, → DEL-01-03, → DEL-01-05, → DEL-03-03, → DEL-04-03 | none | none |
| DEL-07-02 → DEL-04-03, → DEL-09-01 | none | none |
| DEL-08-02 → DEL-04-01, → DEL-04-03, → DEL-02-02, → DEL-01-04 | none | none |
| DEL-08-01 → DEL-02-01 | none | none |
| DEL-09-10 → DEL-04-03, → DEL-06-02, → DEL-08-02 | none | none |

---

# Part 1 — DEL-07-01 PEC first-consumer contract and adoption evidence

Type API_CONTRACT; responsible party "App PEC receiving owner; PEC provider
owner supplies released qualification evidence" (`_CONTEXT.md`);
INITIALIZED; no `Design/` folder.

## 1.1 Obligations (28: 4 OUT, 8 REQ, 8 AC, 8 VER; also 5 CLM, 4 AX, 1 TBD)

Basis keys: **CON** = PRD V4-CON-02/03; **HI** = V4-HI-61…63; **D6** =
DECISION_BRIEF d6 (accepted by J/U1, "I accept all your recommendations");
**EXM** = V4-EXM-30; **PEC** = PEC DEL-04-03 CLM-003/019, REQ-016…023 (a
provider constraint, CLM-005); **D108**.

| Item | One line | Rests on |
|---|---|---|
| OUT-001 | DOC: first-consumer questions and receiving contract: questions, source/claim standing, source-file route, ownership interfaces, OI-022 choices where needed | D6; HI-61; CON-02 |
| OUT-002 | CODE: receiving adapter and inspectable presentation of envelope, pins, citations, claim/feed coverage, freshness, limitations, handoff to the source route | HI-61/62; CON-02/03 |
| OUT-003 | TEST: source-pin, claim, coverage and freshness fixtures; simulated preparation kept apart from an actual qualified witness | EXM; D6 |
| OUT-004 | DOC: qualification/release/consumer-adoption evidence account: what coverage is available for reliance, what is pending | CON-02; D6; D108 |
| REQ-001 | Contract names proposed first questions, required source/claim/feed meanings, their relation to stamp vs reliance declaration, and the file route; undecided terms stay in TBD-001; no fixture label promoted to an accepted term | D6; PEC |
| REQ-002 | Consume PEC through its own interface; record-tier reliance only within qualified, released, deliberately adopted coverage; availability, valid envelope or passing fixtures do not suffice | CON-02; HI-61 |
| REQ-003 | Pin, source reference, coverage, freshness, standing, limits inspectable; stamp ≠ reliance declaration; missing values stay visible limits; freshness comparison details at TBD-001 | HI-61; PEC |
| REQ-004 | Presence is advisory, never correctness, permission, execution authority or a ruling; no PEC projection becomes source authority; no blanket re-read gate | HI-61; CON-02 |
| REQ-005 | Absent/stale/partial/failing: unsupported conclusions named, question handed to DEL-07-02's route; total absence handled receiver-side; silence ≠ empty work, readiness or permission | CON-03; HI-62; D6 |
| REQ-006 | Before reliance: evidence account binds contract and adoption to actual provider release, coverage, qualification evidence and limits; carries D108 accurately; no inferred repair or readiness; no unrelated PEC cleanup required | D108; DEP-002 |
| REQ-007 | Performs no act owned by 06-01, 06-02, 07-02, 08-01, 08-02, PEC, agents, managers, the human or Piping | Allocation rows; CLM-004 |
| REQ-008 | Verification traces a source pin through response to receiving action, then the same question absent/stale/partial/failing; fixtures declare simulated terms; missing inputs pending, never pass | EXM |
| AC-001 | Each question mapped to claims/sources, stamp and reliance meanings, file route, parties; every exact term agreed or held under OI-022; no parser descriptor as production schema | REQ-001 |
| AC-002 | Covered-adopted case alone permits reliance; unqualified, unreleased, unadopted, outside-coverage cases show the missing condition and route, without blocking independent work | REQ-002 |
| AC-003 | Pin, source, coverage, freshness, standing, limits exposed; stamp not conflated with declaration; missing/stale values not made complete | REQ-003 |
| AC-004 | Presence advisory; record-tier bounded; no execution or governed decision created | REQ-004 |
| AC-005 | Same question under each limited condition and no response: unsupported conclusions, route and responsibility handed to 07-02 | REQ-005 |
| AC-006 | Evidence account links provider identity, coverage, adoption; unsupplied inputs pending; D108 meaning preserved; no reliance claimed before OI-022 terms and evidence | REQ-006 |
| AC-007 | Every excluded act accounted to its owner; no old Runtime service presumed | REQ-007 |
| AC-008 | Witness record names question, pin, response, action; criteria mapped; simulated vs actual distinguished; pending inputs named | REQ-008 |
| VER-001 | Inspect contract vs six scope rows, OI-022, seed/d6, CLM-005; trace terms; fixture-to-contract provenance | AC-001 |
| VER-002 | Exercise adapter over qualification, release, adoption, coverage variations; simulated cases bound to assumptions, live to OUT-004 | AC-002 |
| VER-003 | Compare response values with displayed evidence, complete and limited; undecided comparisons unexecuted | AC-003 |
| VER-004 | Presence and record-tier fixtures plus code paths; no upgrade of presence; no owner act written | AC-004 |
| VER-005 | Repeat the question absent/stale/partial/failing and no response; inspect handoff to 07-02 | AC-005 |
| VER-006 | Audit account vs provider contract, release, adoption, OI-022/DEP-002, D108 | AC-006 |
| VER-007 | Act-by-act boundary review incl. external owners; no Runtime bridge, no Piping adoption | AC-007 |
| VER-008 | Audit fixture/witness manifest vs V4-EXM-30 sequence | AC-008 |

**Overtaken or re-read by later decisions** (SoW unrevised; carry per R23-11
only where wording is actually wrong):
- Nothing in the SoW is contradicted. D108 is still the newest PEC fact
  (F-1). The "parent-reported prospective domain-engine contract" (TBD-001)
  remains unconfirmed: no matching PEC record was found (the comparison
  report's search; nothing in `pec/` since).
- **Re-read:** the responsible "App PEC receiving owner" and OI-022's "App
  consumer owner" sit beside DECISION-L L-7 ("the App implementation owner is
  the owner"). R23-17 already treats items "left to the App implementation
  owner" as ordinary design matters, not owner questions. I apply the same
  reading to the App side of OI-022 (§1.4).
- **Re-read:** "App receiving adapter" (OUT-002) is read with D-GOV-43 and
  L-3 ("follow the person's own plugin setting") and HOSTING §6.8: the App's
  Codex already reaches local MCP servers through the person's
  configuration. This shapes the adapter's route (§1.4 Q-1).

## 1.2 Joins

| Row(s) | Consumer → supplier | Type; maturity / satisfaction | DAG-004 |
|---|---|---|---|
| DEP-07-01-009…012 | DEL-07-01 → PEC provider (contract and shape; response and source identity; release and qualification; DEL-04-03 semantics) | PREREQ/INTERFACE/CONSTRAINT; TBD / PENDING | not topological (SR-2) |
| DEP-07-01-013 | DEL-07-01 → D-PEC-108 (DOCUMENT) | CONSTRAINT; PENDING | not topological |
| DEP-07-01-014; mirror DEP-07-02-014 | DEL-07-01 → DEL-07-02 (common route) | INTERFACE; INITIALIZED / PENDING | **held** (SCC-004) |
| DEP-07-02-010 (rep.), -012 (same arc); mirror DEP-07-01-015 | DEL-07-02 → DEL-07-01 (PEC terms; later envelope account) | INTERFACE; INITIALIZED / PENDING | **held** (SCC-004) |
| DEP-06-01-011 | DEL-06-01 → DEL-07-01 | CONSTRAINT; INITIALIZED / TBD | admitted |
| DEP-09-10-005 | DEL-09-10 → DEL-07-01 | PREREQUISITE; INITIALIZED / TBD | admitted |
| DEP-03-04-016 | DEL-03-04 → DEL-07-01 | INTERFACE; INITIALIZED / TBD | admitted |
| DEP-06-01-012; DEP-06-02-016 | DEL-06-01, DEL-06-02 → PEC owning project | CONSTRAINT; TBD | not topological |

**What existing Design files already assume or require of DEL-07-01:**
- **FR-v0.1 (DEL-06-01).** §7: "Consumed (DEP-06-01-011, admitted) | DEL-07-01
  | Coverage and adoption account before relying on a changed PEC consumer
  path | Only at a format change PEC consumes | §8 holds the change". §8: PEC
  consumers "**PEC: none adopted** (OI-022; DEP-002 unestablished)"; "for
  PEC, DEL-07-01 supplies the affected coverage and adoption account". §8
  example: "If PEC later consumes items, DEL-07-01 states whether its coverage
  includes the element before anyone relies on it." **Requires:** OUT-004's
  account must be able to answer per format element, not only per feed.
- **FV-v0.1 and DV-v0.1 (DEL-06-02).** FV §2: "Not inputs (**SETTLED** by
  REQ-005, V4-REC-03, CAP-7): … PEC." DV §… "PEC absent, stale or failing |
  No effect: PEC is not an input (REQ-006)". **Requires:** DEL-07-01's
  presentation lives outside the fleet views; no PEC claim enters a
  queue or decision row.
- **RS-v0.10 OF-2:** "PEC projections … may **locate** evidence. Their
  assertion that an act occurred creates none." Consistent with REQ-004.
- **GUIDE-v0.7 (DEL-03-04).** M10.1: "PEC, where selected: own interface;
  pin, source reference, coverage, freshness; reliance only on
  qualified/released coverage adopted by the consumer; qualified, limited and
  absent distinguished | DEL-07-01/07-02 accepted SoW meaning *(outside
  undertaking, D1)* … | owner-open". HC-10.2 asks "PEC: which
  qualified/released coverage is relied on, adopted by the consumer?". X-12,
  X-16; TBD-007. **Requires:** a host-facing statement of the PEC receiving
  conditions that GUIDE can cite in place of "accepted SoW meaning". The
  "owner-open" label (M10.1, TBD-007) predates the owner's "Scope of owner
  questions" direction; see §6.2 H-8.
- **HOSTING-v0.9 §6.8** (not a register join; the surface DEL-07-01 would
  use). `mcpToolCall` items: caller "**The agent**", "Native delivery only".
  `mcpServer/tool/call`: caller "**The App**", "App-origin only: recorded with
  initiator … No use on a host channel is defined in this increment … It
  requires a thread identity; whether the call or its result enters that
  thread's items or model context is **not observed**", receiver DEL-03-03.
  Config writes: "App, only as **person-directed**".

## 1.3 Proposed contract changes still open

None. SCA-V4-003's LEDGER has no row naming DEL-07-01 (script over all 216
rows; its only connector-adjacent rows are the DECISION-5 A12-mapping DEFERs,
Q-9, which name DEL-04-01 and DEL-05-02). The pass-2 closeout (C1-B) records
GUIDE rows 8 and 10 as "Partial … definitions owed by deliverables outside"
the first increment; that is the GUIDE gap this pass fills, not a contract
change.

## 1.4 Open items, who decides, and what waits for PEC

| # | Item | Shapes design now? | Options and what the files say | Who decides |
|---|---|---|---|---|
| Q-1 | **Consumption route** in the App: (a) the agent calls PEC's tool surface as an MCP server in the person's Codex configuration, observed as `mcpToolCall`; (b) App-origin reads through Codex (`mcpServer/tool/call`) against the same configured server; (c) an App-held client to PEC's socket with its own token | **Yes** — architecture of OUT-002, credentials, HOSTING §6.8 receivers, DEL-09-10's route | PEC-API-007 and PEC-K-03: enabling is "consumer-owned". L-3: follow the person's plugin setting. HOSTING §6.8: App config writes only person-directed; `mcpServer/tool/call` result's entry into model context "not observed". (c) needs App custody of a PEC token, while D-GOV-43 has Codex custody authentication and PEC's token mechanism is open; the v3 exemplar did exactly (c) (loopback client, env-credential login, App-offered tools) and is RETIRED (RB-PEC-ADAPTER). | **INTEGRATION** for HELP_HUMAN (cross-owner: DEL-01-01, DEL-03-03). Proposed in §6.2 H-1 |
| Q-2 | **First consumer question(s)** | **Yes** — every fixture and the DEL-09-10 case hang on it | REQ-001 assigns the proposal to this deliverable. PEC covers what its feeds declare: orientation per loop (receipts, gate states, owner directions, work-graph READY/ACTIVE/BLOCKED nodes), deltas since a SHA (PEC-ORI-001/002/005). FR §8: PEC has adopted no App `chirality.fleet.record` coverage; FR-D2 states the method's Markdown work graphs are "a practice DEL-10-02 owns" | **DERIVED** (H-2): App side proposes; agreement with the PEC owner at the point of need (EXTERNAL) |
| Q-3 | **Receiving semantic model**: how the stamp, the envelope, per-claim tier and the fallback signal map to App standing | **Yes** | PEC fixes the elements (F-1); REQ-003 keeps "exact response representations and freshness comparison details" at TBD-001 | **ORDINARY**, within H-3's common vocabulary (07-02); exact representation EXTERNAL |
| Q-4 | **Freshness comparison** | Yes (one rule) | No time threshold may be invented (TBD-001). PEC's pin is a commit SHA (REQ-017); the receiving project has git history (RS OF-6) | **DERIVED**: compare the pin with the project's current revision of the claim's cited paths: *current* only if no cited path changed after the pin; *stale* if one did; *unknown* if not determinable. Per-feed freshness shown as PEC states it. Agreement on per-feed meaning EXTERNAL |
| Q-5 | **App receiving adoption** (who, how recorded) | Only its record form; the act's point of need ("before operational reliance") is not reached, since no qualified release exists | CLM-004: "the App receiving owner owns App adoption". PEC DEL-08-06 REQ-015: "enable itself in no consumer (the consumer's decision)" | **INTEGRATION** (H-7): two facts. Release-level adoption by the App receiving owner, recorded in OUT-004 against the release identity (as the qualification pin is, R23-22). Per-installation enablement is the person's own Codex configuration (person-directed). Not RESERVED by any text I found; nearest is Root AGENTS.md "The human remains accountable for what is accepted or relied upon", an accountability statement |
| Q-6 | OI-022 PEC-side terms (tool representation, operations, grain, no-response signal, release identification) | No: design carries them as named slots | DEL-08-06 TBD-003/004/006; PEC AX-007 | **EXTERNAL** (PEC owner), at the point of need |
| Q-7 | D108 treatment | No | SoW states it fully | **SETTLED** by the SoW |

**What the App can design and evidence now without PEC:** the questions
(within PEC's declared query kinds), the receiving semantic model and
standing states, the route architecture, the presentation contract, the
same-question limitation cases, the adoption evidence account's form with
D108 carried, and constructed fixtures labelled as such (HOSTING §9.2
`constructed`). **What waits for PEC:** the exact tool/response
representation, any `recorded` fixture (EXM-02 needs a real exchange), the
qualified source-pin → response → action trace, and adoption. No deferral
record names PEC; PEC is "optional to start" (CON-02; CLARIFICATION).

## 1.5 What exists to build on

- **PEC's semantic contract** (F-1): enough to define App-side records and
  constructed envelopes without inventing elements.
- **Supplier surfaces at 0.158.0:** generated types for
  `McpServerToolCallParams` (server, threadId, tool required; arguments,
  `_meta`), `McpToolCallResult`, `McpServerStatus`; HOSTING §6.8's
  classification; NPTD §6 tool row (`mcpToolCall`: server, tool, arguments,
  status, result or error, durationMs, readOnlyHint). ADAPTER OC-2/OC-3
  (realization family; configuration locus) is a ready pattern for "a local
  service the App's Codex reaches as an MCP server". DEL-01-01's
  `prototype/obs1_mcp_double.py` is a local MCP double usable for a bounded
  observation. OBS-1 observed `mcpServerStatus/list` live on one local route;
  it did not observe an MCP tool reaching the model (the `namespace` tool
  drop).
- **App v3 exemplar (evidence only):** a loopback HTTP client for the old PEC
  v1 proposal lane with an endpoint allowlist and environment credentials,
  wrapped as App-offered MCP tools; its register row is RETIRED and d6 says an
  old bridge test "does not qualify current PEC". It shows the cost of route
  (c): App credential handling and App-offered tools, which HOSTING has none
  of in this increment.

## 1.6 Design scope for this pass (to the 60% level)

1. `Design/PEC_RECEIVING.md` (proposed label PRC-v0.1): the first questions
   (H-2) with claims, feeds, stamp and envelope meanings, file route and
   parties; the excluded-act map (REQ-007).
2. The receiving model and a schema for the App's receiving record
   (`pec.receiving-record.schema.json`, PROPOSED): pin, generation time,
   per-feed coverage/freshness/limitation, per-claim citation and tier,
   fallback signal, release identity, adoption standing, the App's
   standing derived under H-3, unsupported conclusions. Valid and invalid
   examples, validated when written (cheap check).
3. Route and sequences (H-1): agent call observed; App-origin read if ruled;
   no response; malformed or partial envelope; signal not stated → *unknown*.
4. Presentation contract: what is shown, presence labelled advisory, nothing
   entering fleet views (FV/DV settled).
5. OUT-004 evidence-account form: release identity, coverage, qualification
   and gate evidence slots, D108 carried verbatim, pending inputs.
6. Verification design VER-001…008 with constructed fixtures FX-PEC-n and
   the declared simulated terms.

Leave out: wire fields, tokens, transport, budgets, UI layout, any PEC-side
production, any App-held PEC credential.

---

# Part 2 — DEL-07-02 Connector limitation and source-file recovery paths

Type BACKEND_FEATURE_SLICE; "App connector-receiving owner; managers and
human retain fallback coordination"; INITIALIZED; no `Design/` folder.

## 2.1 Obligations (27: 3 OUT, 8 REQ, 8 AC, 8 VER; also 5 CLM, 4 AX, 2 TBD)

Basis keys: **CON** = V4-CON-02…04; **HI** = V4-HI-61/62, -30…33 (CLM-005);
**D6**; **§3.1** = PRD staged connections ("Without PEC, agents perform more
source comparison …"); **EXM** = V4-EXM-30.

| Item | One line | Rests on |
|---|---|---|
| OUT-001 | Receiving behaviour: standing, freshness, limits; absent/stale/partial/failing distinguished; route to sources, independently for PEC and Domains; later PEC join | CON-03; HI-62; ARC-22 |
| OUT-002 | DOC: source-file reconstruction and responsibility account: questions, sources and revisions, gaps, agent/manager/human duties, later PEC handoff | D6; §3.1 |
| OUT-003 | TEST: independent availability and fallback fixtures, candidate-bound | EXM |
| REQ-001 | Show source identity, standing, coverage/freshness, limits; distinguish qualified/current from limited/absent; unsupported conclusions named; missing metadata never normalized | CON-03; HI-62 |
| REQ-002 | Each limited condition: explicit route to sources and work to reconstruct, or "source unavailable" with who must obtain it; total absence receiver-side; reading files is not authority | D6; HI-62 |
| REQ-003 | No empty work, readiness or permission from failed feeds; distinct acts keep actor/subject/evidence; no synthetic ordering | HI-30…33; CLM-005 |
| REQ-004 | Route works through ordinary records before fleet software; agents compare, managers review/integrate, the human coordinates; prepared ≠ performed; fleet views not a prerequisite | §3.1; D6 |
| REQ-005 | PEC and Domains independent; development starts and continues with both absent; dependent work waits without marking inputs satisfied | CON-02…04; ARC-22 |
| REQ-006 | Later PEC join uses DEL-07-01's envelope; uncovered material keeps the route; no restart gate; no inference from D108 | CON-02; HI-61 |
| REQ-007 | Fixtures exercise limitation and independence; same question across cases; simulated vs actual; pending inputs named | EXM |
| REQ-008 | No act owned by 07-01, 08-01, 08-02, 06-01, 06-02, 04-01, 04-03, PEC, Piping, the Domains allocation owners, agents, managers or the human | CLM-003/005 |
| AC-001 | Five conditions distinguished; available values shown; unsupported conclusions named | REQ-001 |
| AC-002 | Each condition incl. no response exposes route and gaps; missing source → explicit unresolved need | REQ-002 |
| AC-003 | No empty-work/readiness/permission conclusion; separate act subjects kept | REQ-003 |
| AC-004 | Route followable from files without PEC or fleet software; duties prepared/performed/outstanding | REQ-004 |
| AC-005 | Four combinations: PEC with Domains absent; Domains with PEC absent; both absent; PEC absent with stale Domains | REQ-005 |
| AC-006 | Later join uses DEL-07-01's exact standing; prepared/unqualified/unadopted stay limited even with D108 | REQ-006 |
| AC-007 | Evidence binds candidate, question, inputs; simulation distinguished; pending explicit | REQ-007 |
| AC-008 | Every excluded act kept with its owner, incl. the unresolved Domains allocation; no fleet prerequisite | REQ-008 |
| VER-001…008 | Inspect presentation per condition; follow the same question through the conditions; inspect inferences and acts; walk the route from files only; exercise the four combinations; examine a file-route-to-PEC join; audit fixture records vs V4-EXM-30; act-by-act boundary review | AC-001…008 one-for-one |

**Overtaken or re-read:** nothing contradicted. CLM-003's "DEL-04-01 owns
the operation-policy/human-act contract" is now ACT-POLICY-v0.10 (A1–A16).
REQ-004's "managers" maps to the App's roles: HELP_HUMAN/WORKING_ITEMS
(Type 0/1) review and integrate; TASK (Type 2) agents compare (Root
`AGENTS.md` Roles). **Inference.**

## 2.2 Joins

| Row(s) | Consumer → supplier | Type; maturity / satisfaction | DAG-004 |
|---|---|---|---|
| DEP-07-02-010, -012; mirror DEP-07-01-015 | DEL-07-02 → DEL-07-01 | INTERFACE; INITIALIZED / PENDING | **held** (SCC-004) |
| DEP-07-02-011; mirror DEP-08-01-010 | DEL-07-02 → DEL-08-01 | INTERFACE; INITIALIZED / PENDING | **held** (SCC-004) |
| DEP-07-01-014; mirror DEP-07-02-014 | DEL-07-01 → DEL-07-02 | INTERFACE | **held** |
| DEP-08-01-009 | DEL-08-01 → DEL-07-02 | INTERFACE; INITIALIZED / TBD | **held** |
| DEP-07-02-013 | DEL-07-02 → project graphs, decisions, revisions, source records (DOCUMENT) | INTERFACE; TBD / PENDING | not topological |
| DEP-07-02-015 | DEL-07-02 hands to DEL-06-02 (canonical DEL-06-02 → DEL-07-02) | HANDOVER; INITIALIZED / PENDING | admitted |
| DEP-09-10-006 | DEL-09-10 → DEL-07-02 | PREREQUISITE | admitted |
| DEP-03-04-017 | DEL-03-04 → DEL-07-02 | INTERFACE | admitted |

**What existing Design files assume of DEL-07-02:**
- **FV-v0.1 §6:** "Consumed (DEP-07-02-015, admitted, PENDING) | DEL-07-02 |
  The source-file recovery route and connector limitation states, once
  DEL-07-02 is designed | Not yet available: no connector state is shown;
  nothing else changes". FV §8: "Connector limitation states in waiting
  causes (DEP-07-02-015) | DEL-07-02 (tranche 2) | When DEL-07-02 is
  designed". **Requires:** a connector limitation state FV can name as a
  waiting cause, and a route it can point to.
- **GUIDE-v0.7** M10.3: "Independent absent/limited paths: first connected
  work proceeds without PEC or Domains | CA-v0.7 §6 …; HI V4-HI-62, -64 |
  defined draft (staging only)"; X-12; HC-10.1.
- **SCC-CASE-005** (case, not Design): milestone 1, "DEL-07-02 maps
  limited/absent conditions, ordinary records/revisions, missing sources and
  actual agent/manager/human responsibilities. It can document and walk an
  independently supported source-file question before either connector or
  later fleet software is available."

## 2.3 Proposed contract changes still open

None (LEDGER script; no DEL-07-02 row).

## 2.4 Open items and who decides

| # | Item | Shapes design now? | Options / files | Who decides |
|---|---|---|---|---|
| Q-8 | **Common standing vocabulary** used by 07-01, 08-01, 09-10 and FV | **Yes** — the cluster's shared interface | V4-CON-03, V4-HI-62 name the conditions; SCC-CASE-005 milestone 1 puts the common definition here | **DERIVED** (H-3) |
| Q-9 | **How the route reads fleet records** (FR work graphs, coordination log) | **Yes** | A row DEL-07-02 → DEL-06-02 closes a cycle in the admitted layer; → DEL-06-01 closes one in both layers (F-3). REQ-004: "without making those views a prerequisite"; DEP-07-02-013 already names source records as DOCUMENT input | **DERIVED** (H-6): read them as project files under DEP-07-02-013; FV consumes this deliverable, never the reverse |
| Q-10 | **Route account format and location** | Yes | V4-HI-63 wants versioned formats; OI-013/OI-014: no common service | **ORDINARY**: its own versioned record with the user's project (as FR-D2/FR-D3) |
| Q-11 | TBD-001 (OI-022 terms), TBD-002 (OI-023/026) | No: common route needs neither | SoW: "defines the source route now and uses actual terms before dependent implementation" | Via DEL-07-01 / DEL-08-01; EXTERNAL parts wait |
| Q-12 | Which records evidence that an agent, manager or the human **performed** a duty | Yes (prepared vs performed) | RS OF-1/OF-8; FR records (dispatch, return, review, integration) are the App's evidence of fleet duties | **ORDINARY**, reading those records as files |

**Without external parties:** everything in this deliverable can be designed
and rehearsed now; it is the one piece of the cluster with no external
input except actual source files (DEP-07-02-013), which exist.

## 2.5 What exists to build on

- FR-v0.1 records and reader facts (selected, brief, dispatch, return,
  review, integration; *unknown* never promoted), and FX-FL1; FV-v0.1's
  waiting-cause model and its empty connector slot; RS-v0.10 OF-1…OF-9.
- The method's own work graphs (Root `construct-local-work-graph`; SPEC
  §9.8) as the most common source a route reads in this repository.
- DAG-004's "held, non-gating" rule and SCC-CASE-005's four milestones.
- App v3: no fallback component worth citing beyond the retired adapter row.

## 2.6 Design scope for this pass

1. `Design/CONNECTOR_FALLBACK.md` (proposed CFB-v0.1): the standing
   vocabulary (H-3) with each connector's mapping slots; condition → route
   map; unsupported-conclusion rules; independence matrix (AC-005's four).
2. `connector.route-account.schema.json` (PROPOSED): question; sources with
   revisions; gaps; per-duty actor, standing prepared/performed/outstanding
   with the evidence file; conclusions supported and unsupported.
3. Sequences: limitation detected → conclusions withheld → route account →
   duties; later PEC join rule (REQ-006).
4. Interfaces: to 07-01 and 08-01 (connector-specific meanings, SCC-004
   milestones); to FV (waiting cause, DEP-07-02-015); from files
   (DEP-07-02-013).
5. Failure behaviour: source missing; revision not resolvable; contradictory
   sources; route account torn → *unknown*.
6. Verification design with constructed and real-file fixtures.

Leave out: connector-specific terms; fleet implementation; any policy
ruling.

---

# Part 3 — DEL-08-01 Domains query, admission and freshness contract

Type API_CONTRACT; "App/shared Domains receiving owner; provider/tool owner
remains unresolved"; INITIALIZED; revised under SCA-V4-001 (CLM-003, AX-005).

## 3.1 Obligations (28: 4 OUT, 8 REQ, 8 AC, 8 VER; also 5 CLM, 5 AX, 2 TBD)

Basis keys: **CON** = V4-CON-01, -03; **HOST02** = V4-HOST-02 as revised by
DECISION-5; **HI** = V4-HI-60, -62, -64, §8.1; **OQ3** = PRD OQ-03; **EXM** =
V4-EXM-30/32.

| Item | One line | Rests on |
|---|---|---|
| OUT-001 | DOC: source-admission and query receiving contract: request/result meanings, references, standing, provenance, freshness, limits; open details named | CON-01; HI-60; §8.1 |
| OUT-002 | CONFIG: candidate query/result fixtures over admitted test sources and the identified query contract, **when those inputs exist** | HI §8.1; EXM-32 |
| OUT-003 | TEST: unavailable, unsuitable, stale; admission/authority distinctions; PEC independence | CON-03; HI-62 |
| OUT-004 | DOC: owner/allocation, query-tool, deployment and data-boundary decision account with owners and points of need | OQ3; HI §8.1 |
| REQ-001 | Define consumption through a research workflow; references preserved; retrieval ≠ membership, standing, applicability, authority; no wire/platform/field chosen | CON-01; HI-60 |
| REQ-002 | Admission: identity, standing, provenance, limits and admission basis before reliance; hit ≠ admitted; independent of PEC; no invented human gate | HI §8.1; d6 |
| REQ-003 | Freshness checked against the source/admission basis; stale or unestablished shown with its limit; no invented age threshold | HI-60 |
| REQ-004 | Fixtures against identified meanings and admitted test sources; four cases; unexercised cases named; no live-delivery claim | EXM-32 |
| REQ-005 | Limitation cases connect to DEL-07-02's route; absent-PEC/stale-Domains kept; neither connector a prerequisite | CON-03; EXM-30 |
| REQ-006 | Account keeps OI-023/026 owners and points of need; separates allocation, tool, deployment, transport, boundary, admission; demonstrates V4-HOST-02 compatibility at the query point or names the decision needed | HOST02; HI §8.1; OQ3 |
| REQ-007 | Handoff to DEL-08-02 with contract, limits, open decisions, standing; no inferred approval; Domains not an initial D05 condition | HI-64; §3.1 |
| REQ-008 | No act owned by the host owner (DEL-05-01), 08-02, SWBPIPE, the human, 07-02, managers, 09-10; allocation stays open | CLM-002…005 |
| AC-001…AC-008 | Query contract; admission contract; current/stale/unestablished freshness; fixtures bound or unexercised; limitation cases with route; decision account; handoff; boundary | REQ-001…008 one-for-one |
| VER-001…008 | Contract vs scope and V4-CON-01/HI-60 with a hit-without-standing case; admitted vs located source with PEC absent; freshness cases; fixture-to-source audit; limitation cases incl. absent-PEC/stale-Domains; account vs OI-023/026, DEP-003, V4-HOST-02/PKG-05; handoff vs DEL-08-02; boundary audit | AC-001…008 one-for-one |

**Overtaken or re-read:** CLM-003 already reads DECISION-5. The A12
network-destination subclass that a person's grant to a Domains destination
would be (ACT §2.1 A12, R8-13) is designed; its ScopeOfWork wording in
DEL-04-01 is the SCA-V4-003 DEFER under Q-9 ("Its stated condition (owner
confirms the A12 mapping) has not occurred"). That deferral is DEL-04-01's,
not this deliverable's; the design here cites ACT's A12 row as designed.

## 3.2 Joins

| Row(s) | Consumer → supplier | Type; maturity / satisfaction | DAG-004 |
|---|---|---|---|
| DEP-08-01-008 | DEL-08-01 → DEL-05-01 | INTERFACE; INITIALIZED / TBD | admitted |
| DEP-08-01-009 | DEL-08-01 → DEL-07-02 | INTERFACE | **held** |
| DEP-07-02-011; mirror DEP-08-01-010 | DEL-07-02 → DEL-08-01 | INTERFACE | **held** |
| DEP-08-02-005; mirror DEP-08-01-012 | DEL-08-02 → DEL-08-01 | INTERFACE | admitted |
| DEP-09-10-007; mirror DEP-08-01-011 | DEL-09-10 → DEL-08-01 | PREREQUISITE | admitted |
| DEP-03-04-018 | DEL-03-04 → DEL-08-01 | INTERFACE | admitted |
| DEP-08-01-013…016 | Domains query access (OI-026); admitted test sources (UNKNOWN); OI-023 resolution; OI-026 resolution | PREREQ/CONSTRAINT; TBD | not topological |
| DEP-09-01-020 | DEL-09-01 → "External Domains receiving owners — later research-fixture admission" | PREREQUISITE; TBD | not topological |

**What existing Design files assume of DEL-08-01:**
- **LOOP-v0.9 §10.4:** "DEL-08-01 (outside the first increment) |
  DEP-08-01-008 (admitted) | Embedded-integration receiving requirements, and
  the host-agent destination constraint a Domains query must be compatible
  with | §5.1.1; N-OPEN-3 names tool-caused traffic 'e.g. a later Domains
  query' and leaves it open". N-OPEN-3: "From R8-13 it is governed by the
  allow list and in-work grants (NW-8…NW-13) … traffic an entry
  **declares** in its external-contact declaration is the agent's and passes
  V-D (§5.3 DF-1, DF-4); traffic a host operation makes without declaring it
  is refused at contact unless allowed (DF-F8)." DF-7: MCP servers only if
  stateless (revision 2026-07-28). **Requires:** a Domains query reaches a
  host's agent as a host catalog entry with an external-contact declaration,
  or as a stateless MCP server the person allows; a local/in-process
  arrangement adds no destination (CLM-003).
- **EXP-v0.2 §2.1 IN-8:** "Admission input for a later research fixture |
  Domains/SWB/App receiving owners (OI-023, OI-026) | DEP-09-01-020, not
  topological | Only if a research fixture is used | Not used".
- **GUIDE-v0.7** M10.2 ("Domains in the later research-to-design increment
  … | 03-04/TBD-008 (OI-023); 03-04/TBD-009 (OI-026) | outside undertaking
  (D1); owner-open"), HC-10.3, X-13, X-17 ("Domains provider allocation |
  Owner decision retained in 03-04/TBD-009").

## 3.3 Proposed contract changes still open

None naming DEL-08-01 in SCA-V4-003. SCA-V4-001 O-18 (CLM-003) was applied.

## 3.4 Open items and who decides

| # | Item | Shapes design now? | Files | Who decides |
|---|---|---|---|---|
| Q-13 | **Query/result, admission and freshness meanings** (OI-023's content part) | **Yes** — the contract itself | REQ-001…003 assign the definition to this deliverable, "sufficient for the provider and receiving tool-contract owners to identify a usable interface" | **ORDINARY/DERIVED** (App side). Agreement with the provider: **EXTERNAL**, provider unallocated |
| Q-14 | **Deployment/data-boundary compatibility** | Yes (a compatibility matrix, not a choice) | V4-HOST-02 settled by DECISION-5; LOOP §5.1.1, §5.3 (DF-1, DF-7), N-OPEN-3; HOST §8.1 "Resolve a compatible query/tool arrangement before relying on it, **or obtain an explicit decision on an affected constraint**" | Matrix **DERIVED** from LOOP. A relaxation of V4-HOST-02 would be a basis amendment: **RESERVED** (the owner's direction: "HELP_HUMAN brings the owner only acts the governing texts reserve to the person, such as … accepting an amendment"). Conditional; nothing indicates it is needed |
| Q-15 | **Provider allocation** (OI-026) | **No**: the design is allocation-neutral | OI-026 Owner "Owner with App/Domains/SWB definition owners"; point of need "Before allocating Domains provider production and committing its integration" | **RESERVED**: DEL-07-02 REQ-008 "no Domains provider allocation reserved to the owner with App/Domains/SWB definition owners"; DEL-09-10 REQ-006 "Domains provider allocation remains an Owner decision with the definition owners". **Not needed in this pass** |
| Q-16 | **When the Domains-enabled increment starts** (OI-023's "receiving milestone") | No | OI-023 Owner "Owner with Domains/SWB/App receiving owners"; point of need "Before later Domains-enabled design increment" | **RESERVED** in substance: selecting an undertaking is the owner's (OWNER_DECISIONS: the owner chose "4 A+C" among undertakings). **Not needed now**: this pass designs the App's receiving definition, which "develops in parallel" (PhaseHint) |
| Q-17 | Who admits content | No: a slot | REQ-002: "as established by the provider/receiving decisions in CLM-002, not an invented standing human gate" | EXTERNAL (with the allocation) |
| Q-18 | SWBPIPE's DEC-051 open residency vs V4-HOST-02 | No for the App contract; yes for the later host witness | RELAY answers "Conflict for the App to note" | **EXTERNAL** (SWBPIPE owner); deferred with host joins (DECISION-3) |

**Without Domains:** the contract meanings, admission and freshness models,
the compatibility matrix, the decision account, the handoff form, and
limitation cases on constructed sources can all be designed now. **Waits for
Domains:** an identified query contract and admitted test sources, without
which REQ-004's fixtures stay *unexercised* by the SoW's own terms
("Fixtures … when those inputs exist"); actual query access; any
compatibility evidence on a real arrangement.

## 3.5 What exists to build on

LOOP §5.1.1 (NW-8…NW-16), §5.3 (DF-1…DF-10), its destination-flow
prototype; ACT A12 network-destination subclass; HOST §8.1;
`HANDOFF_SWBPIPE_DOMAINS.md` "Domains" section (the activity "query domain
evidence → build research context → create a design candidate → human
approval"); RS OF-2/OF-3 (references, never copies). App v3: nothing.

## 3.6 Design scope for this pass

1. `Design/DOMAINS_RECEIVING.md` (proposed DRC-v0.1): request and result
   meanings; reference, source identity, admission standing, provenance,
   freshness basis; located ≠ admitted ≠ applicable.
2. Admission evidence model with an unallocated admitting-party slot.
3. Freshness model: index build basis vs source revision or date;
   current/stale/unestablished; no age threshold.
4. Compatibility matrix (Q-14; H-6: local/in-process; stateless MCP as an allowed
   destination; host catalog entry with external-contact declaration; remote
   service only as an allowed destination), citing LOOP's rules.
5. OUT-004 decision account: OI-023 parts, OI-026, owners, points of need,
   EXTERNAL vs RESERVED vs App-side.
6. Handoff form to DEL-08-02 and to DEL-09-10; the Domains mapping into
   H-3's vocabulary; limitation cases on constructed sources, with the
   fixture cases REQ-004 needs listed as unexercised.

Leave out: provider, database, corpus, transport, deployment choice, schema
fields beyond meanings.

---

# Part 4 — DEL-08-02 Later research-to-design receiving activity

Type DOC_UPDATE; "App/shared method and Domains receiving integration owner;
external SWB owner implements host use; human owns approval"; PhaseHint
"Subsequent connected increment; no initial D05 prerequisite"; INITIALIZED.

## 4.1 Obligations (22: 3 OUT, 7 REQ, 7 AC, 5 VER; also 6 CLM, 3 AX, 3 TBD)

Basis keys: **CON** = V4-CON-01, -04, -05; **HI** = V4-HI-60, -64, -65,
§8.1, V4-HI-25/30…33/40…42; **AUT** = V4-AUT-01…05; **EXM** = V4-EXM-31/32;
**EXT** = V4-EXT-01; **OPS6**.

| Item | One line | Rests on |
|---|---|---|
| OUT-001 | Research workflow and contribution/point-of-need account: admitted query → inspectable context → identified candidate for human approval | CON-04/05; HI §8.1 |
| OUT-002 | App/shared receiving integration and host handoff; proposals distinct from received answers | EXT; OPS6; HI §8.1 |
| OUT-003 | Coordinated V4-EXM-32 witness, candidate-bound, with unavailable/unsuitable input; a prepared account is not the witness | EXM-32 |
| REQ-001 | Trace admitted query/source → evidence, inference, gaps → candidate → intended human decision; consumes DEL-08-01, PKG-02, PKG-04 meanings | CON-01/05; HI-60/65 |
| REQ-002 | Limited input exposed with its effect on context and candidate; dependent work waits; independent continues | CON-03/04; HI-62/64 |
| REQ-003 | Account of contributions, owners or open allocation, standing, points of need | HI §8.1; §3.1 |
| REQ-004 | Handoff separates App/shared and host contributions; human relay; no guessed API, transport, corpus, deployment, date | EXT; OPS6; V4-SHR-03 |
| REQ-005 | Candidate decision evidence: candidate, subject and scope, actual actor, evidence, recorder distinct; changed content lapses applicability; distinct acts; adopted policy applied, OI-001/002 custody kept | AUT; HI-25/30…33/65 |
| REQ-006 | Qualification binds provider/query contract, sources, workflow, host, candidate; completed live witness needs an actual content-bound decision; negatives kept; favourable approval not required | EXM-32; HI-64 |
| REQ-007 | No act owned by 08-01, PKG-02, PKG-04, SWBPIPE, the host, the human, the provider allocation, the OI-001/002 owners | CLM-003…006 |
| AC-001…AC-007 | Method path; contribution account; handoff; live witness; limited input; act distinctions; boundary | REQ-001…007 (AC-002, 003, 007 by VER-002) |
| VER-001 | Trace a context account from references to candidate; interfaces | AC-001 |
| VER-002 | Review account and handoff; owners, points of need, relay, boundary, four roles | AC-002, 003, 007 |
| VER-003 | Coordinate V4-EXM-32 through the human after inputs exist; observe path and an actual decision | AC-004 |
| VER-004 | Admitted unavailable/unsuitable/stale cases under the actual query contract | AC-005 |
| VER-005 | Examine an actual content-bound decision, fabrication and content-change cases, under the adopted policy | AC-006 |

**Overtaken by later decisions (carry under R23-11):**
- **CLM-006, TBD-003, REQ-005's last sentence, AC-006 and VER-005** say
  OI-001 and OI-002 "remain OPEN" and must be carried "to their owners before
  fixing dependent criteria". FIRST-INCREMENT DECISION-1 D2 and D3 ruled both
  for the App/shared contracts; OI-001's Consequence now reads: "Ruled for
  the first increment's App/shared contracts by …DECISION-1 D2 …;
  operation-specific additions remain under OI-021 and host adoption under
  DEP-001." The residue for this deliverable is OI-021/DEP-001 (host side),
  not OI-001/002 as a whole. (DEL-04-01's equivalent SoW wording was revised
  by SCA-V4-001, ACT F-10.)
- **DECISION-4 (Phase 1)** shapes REQ-005 and VER-005: a checkpoint naming
  the candidate approval is plan guidance; the agent asks; the act is
  recorded only when the person performs it; no hold is enforced (GUIDE
  header "Phase"; WD §4.3). **Re-read, not a contradiction.**

## 4.2 Joins

| Row(s) | Consumer → supplier | Type; maturity / satisfaction | DAG-004 |
|---|---|---|---|
| DEP-08-02-005 | DEL-08-02 → DEL-08-01 | INTERFACE; INITIALIZED / TBD | admitted |
| DEP-08-02-006; mirror DEP-02-01-037 (SCA-V4-003 RP1-MX-0201) | DEL-08-02 → DEL-02-01 | INTERFACE; TBD / TBD | admitted |
| DEP-08-02-007 | DEL-08-02 → PKG-04 (package) | INTERFACE; TBD | not topological |
| DEP-08-02-008…010, -012 | Provider/query arrangement; admitted sources; SWBPIPE host integration and approval route; the person's actual decision | PREREQUISITE; TBD | not topological |
| DEP-08-02-011 | DEL-08-02 hands to the external SWBPIPE owner | HANDOVER; TBD | not topological |
| DEP-03-04-019 | DEL-03-04 → DEL-08-02 | INTERFACE | admitted |

**What existing Design files assume of DEL-08-02:**
- **WD-v0.9 §8** (receivers outside the increment): "DEL-08-02: the portable
  method meanings (§3, §4) … The 'evidence' of DEP-08-02-006 … [is] named by
  those rows and not yet defined or produced here: OUT-004 is designed only,
  and no case has been run (§13)". WD §4.2.1 has **exactly two tool classes**:
  "host operation requirement" (a host catalog operation) and "harness
  capability requirement"; HC-2: "A host operation reached through an MCP
  server or a command-line tool is a host operation requirement … and is
  never declared as `mcp-tool-call`". See S-4.
- **ACT-POLICY-v0.10 §2.1** alias exclusions: "Design-candidate approval
  (V4-CON-05; V4-HI-65) is a separate act in a later increment. It is **not**
  A6." §14 F-2: "Design-candidate approval. It has no canonical name yet. One
  will be needed in the Domains increment."
- **GUIDE-v0.7** M10.2, HC-10.3 (as Part 3).
- **CA (DEL-09-06) §6 staging:** "Later | Domains research/design-candidate
  increment; PEC coordination | Their own contracts | — | Outside this
  activity".

## 4.3 Proposed contract changes still open

None in SCA-V4-003 beyond the applied mirror row RP1-MX-0201 (DEP-02-01-037,
INCLUDE). New: the overtaken OI-001/002 wording above, for the next
amendment (R23-11).

## 4.4 Open items and who decides

| # | Item | Shapes design now? | Files | Who decides |
|---|---|---|---|---|
| Q-19 | **Candidate-approval act kind** | **Yes** — OUT-002's act contract (AC-006) cannot be written without it | ACT F-2; alias exclusion; precedents R12-5 (A15) and R23-8 (A16) | **DERIVED** (H-4) |
| Q-20 | **How a workflow declares a Domains query tool** | **Yes** — the research workflow's declared part | WD §4.2.1 two classes; SWBPIPE has no capability catalog (WD R8-10 note) | **INTEGRATION** (H-5; structural S-4) |
| Q-21 | Whether the host adds candidate approval to **its own reserved list** | No (host side, later) | D2: "The host names and enforces its own list (V4-HI-30). Operation-specific additions are made when the concrete SWB operation is selected (OI-021)"; OI-021 Owner "Owner via outside SWB session and App/shared owner" | **RESERVED** jointly with the external owner (OI-021 names the Owner). **Not needed now**; deferred with host joins (DECISION-3) |
| Q-22 | The research workflow's authoring and registration | No (design of its declared part only) | SoW: "this INIT contract does not itself create or register a workflow"; Root AGENTS.md: load `create-workflow` before creating one; registering is the person's A15 | Authoring later; registration is the person's act at that time (not a decision now) |
| Q-23 | Host handoff content | Yes (prepared, not sent) | OPS6; DECISION-3 | **ORDINARY**: prepare as "next relay" items, as HANDOFF already does; sending is the owner's relay (O/U5) |
| Q-24 | Provider allocation, receiving milestone | No | OI-026, OI-023 | RESERVED, not now (Part 3 Q-15, Q-16) |

**Without SWBPIPE, Domains or the person:** the method model, the declared
part (with H-5), the act contract (with H-4), the contribution account, the
prepared host questions, the V4-EXM-32 case definition with its stimuli, and
a rehearsal over constructed sources and a constructed candidate can all be
done now. **Waits:** the provider/query contract and admitted sources
(Domains), host query use and the approval route (SWBPIPE, deferred), and
the person's actual decision for a completed live witness.

## 4.5 What exists to build on

WD-v0.9 declared part (expected inputs, required tools, checkpoints with
`required_act`, returned outputs/evidence); EXEC requirement check; ACT §2.1
(A1 propose, A8 request, A9 record, alias exclusions); RS §6 human-act
records and lapse rules (changed content → act lapses, the REQ-005
"changed content visibly invalidates" need); DAC (DEL-09-05) and the early
path E as the pattern for a person's decision carried to a reader; WR
(DEL-02-02) A15 registration for when the workflow is authored; the HANDOFF
"Domains" section. App v3: nothing comparable.

## 4.6 Design scope for this pass

1. `Design/RESEARCH_TO_DESIGN.md` (proposed RTD-v0.1): method model
   (query → retrieved evidence → inference and gaps → candidate identity →
   request (A8) → the person's act), each with its evidence and owner.
2. Declared-part sketch of the research workflow in WD form (not a
   registered workflow), using H-5's tool class.
3. Act contract (H-4): subject (candidate content identity and its context
   account identity), scope, actor, capture by the host facility, lapse on
   content change, relation to A2/A5/A6/A7.
4. Contribution and point-of-need account (HI §8.1's five rows).
5. Prepared host questions for the next relay (not sent; DECISION-3).
6. V4-EXM-32 case definition with declared stimuli (R23-27: unavailable
   source, unsuitable source, stale source, changed candidate content, an
   agent's "approved" claim) and the rehearsal plan.

Leave out: workflow registration; SWBPIPE implementation; provider; UI.

---

# Part 5 — DEL-09-10 Optional connector consumption witness

Type TEST_SUITE; "App connector examination owner; provider owners supply
identified qualification/response evidence"; INITIALIZED.

## 5.1 Obligations (18: 2 OUT, 6 REQ, 5 AC, 5 VER; also 4 CLM, 2 AX, 3 TBD)

Basis keys: **EXM** = V4-EXM-30, §§1–2 (EXM-01…05), §7; **CON**, **HI**,
**ARC22**, **D6** as above.

| Item | One line | Rests on |
|---|---|---|
| OUT-001 | V4-EXM-30 suite: qualified/current, limited, absent; same question; absent-PEC/stale-Domains; independent availability | EXM-30; D6 |
| OUT-002 | Candidate-bound witness: one actual source pin through qualified PEC extraction/response to the permitted action, with fallback and actors | EXM-30; D6 |
| REQ-001 | Qualified trace with pin, citation, coverage, freshness, limits and actual qualification/release/adoption evidence; envelope alone is not a witness | EXM-30; CON-02 |
| REQ-002 | Same question absent/stale/partial/failing; unsupported conclusions, actual route, actual actor work | EXM-30; CON-03; HI-62 |
| REQ-003 | PEC stopped + Domains index older than sources; independent availability; Domains contract applied where needed; nothing selected by a test | EXM-30; ARC22 |
| REQ-004 | Candidate, date, configuration (harness/model versions, model server); passed/failed/blocked/not run/inconclusive; unqualified reported as unqualified; changed candidate reopens | EXM-01…03 |
| REQ-005 | Provider limits and consumer adoption kept; D108 kept; faithful recording distinct from performing; no synthetic act ordering | HI-61/65; EXM §7 |
| REQ-006 | No act owned by 07-01, 07-02, 08-01, 08-02, PEC, SWB, the allocation owners, managers or the human | CLM-002/003 |
| AC-001…AC-005 | Qualified case; four limited cases; original combination and independence; result binding and standing; custody and act boundaries | REQ-001…006 |
| VER-001…VER-005 | Follow the actual pin; compare limited observations; inspect the original case; audit binding and provenance; review the dossier vs owners and acts | AC-001…005 one-for-one |

**Overtaken or re-read:** nothing contradicted. The SoW's outcome words map
to EXP-v0.2 §3.1 (`pass`, `fail`, `blocked`, `not-run`, `inconclusive`;
R23-1, R23-20). Its "harness/model versions and model server" equals EXP-R2.
**Register note (R23-11):** DEP-09-01-027 (DEL-09-01 hands to DEL-09-10) is
admitted, but DEL-09-10's register has no upstream row for DEL-09-01 (rows
005–011 checked). It gates nothing; it is a register asymmetry for the
register owners.

## 5.2 Joins

| Row(s) | Consumer → supplier | DAG-004 |
|---|---|---|
| DEP-09-10-005, -006, -007 | DEL-09-10 → DEL-07-01, 07-02, 08-01 (PREREQUISITE; INITIALIZED / TBD) | admitted |
| DEP-09-01-027 (DEL-09-01's DOWNSTREAM row) | DEL-09-10 → DEL-09-01 | admitted |
| DEP-09-10-008…011 | PEC extraction/response and release evidence; the consumer's adopted envelope; actual source files; OI-022 resolution | not topological |

No deliverable consumes DEL-09-10 by row (all registers searched).

**What existing Design files assume of DEL-09-10:** EXP-v0.2 §2.2 OUT-1…6
list DEL-09-10 as a receiver of the result record, change-impact record,
review protocol, routes, fixture rules and support revision (DEP-09-01-027).
EXP-R3: "Only a `candidate` record stands for a scenario (V4-EXM-nn), whatever
its outcome"; R23-19, R23-20 and R23-27 govern parts, outcomes and stimuli.

## 5.3 Proposed contract changes still open

None.

## 5.4 Open items and who decides

| # | Item | Shapes design now? | Files | Who decides |
|---|---|---|---|---|
| Q-25 | Selected receiving consumer | Yes | EXM-30: "The App is the first intended PEC consumer" | **SETTLED** |
| Q-26 | The coordination question | Yes | Must be DEL-07-01's question (REQ-008 there; EXM-30 "the same coordination question") | **DERIVED** (= H-2) |
| Q-27 | Limited conditions and the original combination as **declared stimuli** | Yes | R23-27 item 1 ("Where a ScopeOfWork VER item requires a condition, the scenario's run creates it as a named stimulus") | **SETTLED** by R23-27 |
| Q-28 | Qualified case when no qualified PEC exists | Yes (its standing) | EXM-30: "An unqualified delivery is reported as such"; R23-20: `blocked` needs an attempt; `not-run` if not attempted | **DERIVED**: planned and recorded `not-run` with `missing_inputs` (PEC release, App adoption) until attempted; `blocked` if attempted and stopped |
| Q-29 | Route (interface vs native) | Yes | EXM-04; EXP §8 | **ORDINARY** within EXP |

**Without PEC or Domains:** the whole suite design, case definitions with
stimuli, the rehearsal of every limited case on constructed envelopes and
sources, and the dossier form. **Waits:** the qualified joined witness
(AC-001) and any `candidate` record that stands for V4-EXM-30.

## 5.5 What exists to build on

EXP-v0.2 (three record schemas, rules EXP-R1…R9, routes, `check_exp.py`);
SQ-v0.2 §3.4's declared-stimulus table (ST-1…ST-5) as the model; LHQ's
case blocked at its start (LF-1) and DOS's per-case gap sheets as the model
for PEC and Domains gaps; RRM for an isolated reader.

## 5.6 Design scope for this pass

1. `Design/CONNECTOR_WITNESS.md` (proposed CW-v0.1): cases QC-1 (qualified
   joined trace), LC-1…LC-4 (absent/no response, stale, partial, failing; one
   question), OC-1 (PEC stopped, Domains index older than its sources),
   IA-1…IA-3 (independent availability); each with parts, declared stimuli
   and not-applicable declarations (R23-19).
2. Mapping of DEL-07-02's standing vocabulary into parts and expectations,
   and of results into EXP records.
3. Evidence provenance per part (`constructed` now; `recorded`/`live` only
   with a real PEC); routes (WebKit and Chromium plus native smoke).
4. Dossier with PEC and Domains gap sheets (DOS pattern).
5. Verification design VER-001…005.

Leave out: building other owners' fixtures; any claim of the joined witness.

---

# Part 6 — Across the cluster

## 6.1 Items genuinely reserved to the person

None is needed in this pass. Four exist at later points of need:

| Item | Quoted basis | Point of need | Design text depending on it now |
|---|---|---|---|
| Domains provider allocation (OI-026) | DEL-07-02 REQ-008: "no Domains provider allocation reserved to the owner with App/Domains/SWB definition owners"; DEL-09-10 REQ-006: "Domains provider allocation remains an Owner decision with the definition owners" | "Before allocating Domains provider production and committing its integration" | None (allocation-neutral design) |
| Starting the Domains-enabled increment (OI-023's receiving milestone) | OI-023 Owner "Owner with Domains/SWB/App receiving owners"; the owner selects undertakings ("4 A+C") | "Before later Domains-enabled design increment" | None |
| Host-specific reserved additions incl. candidate approval on SWBPIPE (OI-021 residue of OI-001) | D2: "Operation-specific additions are made when the concrete SWB operation is selected (OI-021)"; OI-021 Owner "Owner via outside SWB session and App/shared owner" | Before the host's operation-policy contract; host joins deferred (DECISION-3) | None |
| Any relaxation of V4-HOST-02 for a Domains deployment | HOST §8.1 "or obtain an explicit decision on an affected constraint"; the owner's direction lists "accepting an amendment" among acts reserved to the person | Only if no compatible arrangement exists | None |

Also permission, not a decision: if the side probe in §6.5 needs a Codex
binary that is not already present, OWNER_DECISIONS records "Any other
download, or a sign-in, needs a new owner answer." A `codex` executable is
on the PATH; its version was not checked (read-only survey).

## 6.2 Proposed for HELP_HUMAN to rule (ranked by how much design text depends on them)

| ID | Question | Proposed answer | Label |
|---|---|---|---|
| **H-3** | One standing vocabulary for both connectors | DEL-07-02 defines it; DEL-07-01, 08-01, 09-10 and FV use it. Three independent facets: **envelope** (qualified-released-adopted · not adopted · outside coverage · not applicable for Domains); **condition** (current · stale · partial · failing · absent-no-response · unknown); **claim tier** (record · presence-advisory · admitted-source · located-not-admitted). Only *adopted + current + record/admitted* supports reliance; every other combination names its unsupported conclusions and the route. Connector-specific meanings come from 07-01/08-01 under SCC-CASE-005's R1 milestones; no new row | DERIVED (V4-CON-03, V4-HI-62, DEL-07-02 REQ-001, SCC-CASE-005 milestone 1) |
| **H-2** | The App's first PEC consumer question | Project-scope orientation over PEC's declared feeds: "For loop/undertaking L at revision R, which work items are ready, active or blocked, with owners and gate states, and what changed since S?" (PEC-ORI-001/002/005). Answered by the route from the method's work graphs and decision records. No PEC coverage of the App's `chirality.fleet.record` assumed (FR §8). Agreement with the PEC owner at the point of need | DERIVED (DEL-07-01 REQ-001; PEC-ORI-001/002; FR §8, FR-D2) |
| **H-1** | PEC consumption route in the App | Through the person's own Codex MCP configuration only: (a) agent calls observed as `mcpToolCall` (NPTD tool row); (b) App-origin reads for the presentation via `mcpServer/tool/call`, recorded with initiator App, **only after** a bounded local observation settles whether such a result enters thread items or model context (HOSTING §6.8 "not observed"). No App-held PEC client, socket or token. Enablement is the person's configuration act (person-directed). Adds DEL-07-01 as a receiver in HOSTING §6.8 at its next revision (a row) and, if (b) is used, a register row DEL-07-01 → DEL-01-01 (reach: no cycle) | INTEGRATION (PEC-API-007, PEC-K-03, L-3, D-GOV-43, HOSTING §6.8; v3 route (c) retired) |
| **H-4** | Candidate-approval act | A canonical row now, PROPOSED (e.g. **A17 *approve candidate***): decision actor the person; subject one candidate's content identity with its context account; captured by the host's facility (V4-HI-31); not A5, not A6 (alias exclusion); lapses on candidate content change; no agent performs it. Rows at their owners' next revisions: ACT §2.1/§2.4/§2.5/§9/§10.1, RS §6.1/§6.2/§13.3 and schema enum, DEL-02-03 `actRef` if a checkpoint may name it, GUIDE act lists. The host's reserved list stays OI-021 | DERIVED (ACT F-2; R12-5, R23-8 precedent; V4-CON-05, V4-HI-65) |
| **H-5** | Declaring a Domains (or PEC) tool in a workflow | Add a third, opaque tool class to WD §4.2.1, **provider tool requirement**, referencing the provider/query contract identity, with necessity and fallback; EXEC reports it *not established* until a contract identity exists. WD must not consume DEL-08-01 by row (DEL-08-01 reaches DEL-02-01 through held arcs); the reference stays opaque, as host operations already are | INTEGRATION (WD §4.2.1, HC-2; SWBPIPE has no catalog) |
| **H-6** | How DEL-07-02 reads fleet records; how Domains tools reach a host loop | DEL-07-02 reads FR records and work graphs as project files under DEP-07-02-013; FV consumes DEL-07-02 (DEP-07-02-015), never the reverse. Domains tools reach LOOP only as host catalog entries with external-contact declarations or as allowed stateless MCP servers; LOOP does not consume DEL-08-01 | DERIVED (F-3 reach; R23-2 pattern) |
| **H-7** | App receiving adoption | Release-level adoption recorded by the App receiving owner in OUT-004 against the release identity and evidence (as the qualification pin, R23-22); per-installation enablement is the person's own configuration. Point of need: a qualified PEC release, which does not exist | INTEGRATION |
| **H-8** | Overtaken wording and labels | Carry to the next amendment (R23-11): DEL-08-02 CLM-006, TBD-003, REQ-005 (last sentence), AC-006, VER-005 (OI-001/002 "remain OPEN"; residue OI-021/DEP-001). Register owners: DEL-09-10's missing upstream row for DEP-09-01-027. GUIDE's next revision: M10.1/M10.2 and TBD-007…009 "owner-open" read "open at point of need; App side designed in PRC/CFB/DRC/RTD" | DERIVED (R23-11; owner "Scope of owner questions") |
| **H-9** | Lifecycle | The five move INITIALIZED → IN_PROGRESS when design starts, by `write_status.sh` | DERIVED (R23-28 precedent) |

## 6.3 Structural questions that could force restructuring of an earlier Design file

- **S-1 PEC route (H-1).** Choosing route (c) would put a PEC token in App
  custody: ACCESS (DEL-01-05) and HOSTING §2/§6.8 assume Codex custodies
  authentication and the App writes the person's configuration only when
  person-directed. That is a structural change; H-1 avoids it. Route (b)
  adds a receiver row to HOSTING §6.8 and depends on an unobserved fact.
- **S-2 What PEC can cover.** If the App's PEC question is about App
  undertakings recorded in `chirality.fleet.record`, PEC needs a feed profile
  for that format and FR §8 gains PEC as a consumer (a row); if instead the
  method's Markdown graphs stay the only PEC-covered source, the App's
  records and the method's practice diverge for PEC purposes (S1-A's K-C,
  now with a consumer attached). H-2 avoids depending on either for this
  pass. R23-31 item 1 places the method's practice in PKG-10 as this
  project's own execution controls and the App's product support in PKG-06
  and PKG-02, so the PEC-coverage question belongs to DEL-06-01's FR §8
  account (O-A) and to the PEC owner, not to O-E.
- **S-3 FV's connector slot.** FV §6/§8 already reserve the waiting cause;
  adding it is a row in FV §4 (O-A). No restructure, provided H-3's states
  arrive as named values FV can show without interpreting PEC or Domains.
- **S-4 Workflow tool classes (H-5).** WD §4.2.1 and HC-2 define two classes;
  a provider tool fits neither. The additive class touches WD's declared-part
  schema enum, EXEC's EV-3/EV-4 and the GUIDE checklist. If instead the
  answer were "Domains must be wrapped as a host catalog operation", SWBPIPE
  (no catalog, WD R8-10 note) could not declare it at all.
- **S-5 Candidate-approval act (H-4).** Rows in ACT, RS, DEL-02-03's
  checkpoint schema and GUIDE, as A16 was (R23-18, R23-21 version labels).
  Its subject binds a host content identity; SWBPIPE has only a whole-model
  hash today (SQ-03), so the act's subject definition must accept that.
- **S-6 Cycle guards (F-3).** Rows that would close cycles: DEL-07-02 →
  DEL-06-02 or → DEL-06-01; DEL-07-01 → DEL-06-01; DEL-05-01 → DEL-08-01;
  DEL-04-01 → DEL-08-02; DEL-02-01 → DEL-08-01. Each would be an SCC-forming
  departure. H-6 keeps all of them as files or runtime values.

## 6.4 Early unit for the cluster: **EU-D1 "one question, five conditions, two connectors"**

**Why this unit.** The premise most likely to invalidate dependent work is
the shared standing model and the same-question source route (H-3): DEL-07-01,
07-02, 08-01, 09-10 and FV all consume it, and SCC-004 means it is defined
jointly. A wrong model would be repeated in four Design files and a sibling's
view. The unit also tests H-2 (is the first question answerable from files and
inside PEC's declared feeds?) and independence (absent PEC, stale Domains).

**Path (authoritative input → production → consumption).**
1. **Authoritative input.** Real project files at two fixed commits of this
   repository (for example this run's `WORK_GRAPH.md`, `DISPATCH.md` and
   `R23_RESOLUTIONS.md`, read at commit S and at a later commit R), and PEC's
   semantic contract text (F-1) as the only source of envelope elements.
2. **DEL-07-02 route account.** Question Q1 (H-2) answered from the files
   alone: sources with revisions, gaps, supported conclusions, and the duties
   (agent compared; manager review/integration; human coordination) marked
   prepared, performed or outstanding with the evidence file for each.
   Validated against `connector.route-account.schema.json` when written.
3. **DEL-07-01 receiving.** Six constructed PEC inputs, labelled
   `constructed`: adopted + current; not adopted (envelope valid); stale
   (pin before the latest change to a cited path); partial (one feed
   uncovered); failing (fallback signal set); no response. Each becomes a
   receiving record with H-3 standing and its unsupported conclusions.
4. **DEL-08-01 variant.** A constructed admitted-source index older than its
   sources, with PEC absent (the original combination), mapped into H-3.
5. **DEL-09-10 record.** One EXP rehearsal result record (run basis
   `rehearsal`, so it cannot stand for V4-EXM-30, EXP-R3) with parts LC-1…4,
   OC-1 and QC-1; QC-1 is `not-run` with `missing_inputs` (PEC release, App
   adoption).
6. **Consumption.**
   - **FV (DEL-06-02, owner O-A)** reads the connector standing as a waiting
     cause for one work item through DEP-07-02-015, in FV's prototype.
     Adoption is checked in O-A's returned files (R23-21).
   - **An isolated reader** (a fresh agent, RRM pattern), given only the route
     account and the receiving records, answers Q1 for each condition and
     lists the conclusions it cannot support.

**Consumption check (what counts as working).**
- EXP's `check_exp.py` passes the DEL-09-10 record, and the schemas validate
  every record.
- FV shows the connector cause and never *ready* for a connector-dependent
  item.
- The reader's answers match the route account's ground truth in every
  condition. No condition yields "no work", "ready" or "permitted". The
  stale, partial and failing conditions each produce at least one named
  unsupported conclusion. The Domains-stale/PEC-absent case is handled by
  each connector's own facet.
- The comparison checker is reviewed against an account it did not author
  (tranche 1's lesson: a checker that agreed only with its author's
  accounts).

**Independent side probe (cheap, resolves H-1's open fact).** A bounded local
observation at pin 0.158.0 with DEL-01-01's `obs1_mcp_double.py`: does an
App-origin `mcpServer/tool/call` result enter the thread's items or model
context? No network, no sign-in, a scratch Codex home under a path without
the user name (R23-22 item 4). Owned with DEL-01-01. It needs a Codex binary;
if none is usable without a download, the owner's answer is needed first.

**What stays unaffected meanwhile.** DEL-08-02's method, act contract (once
H-4 is ruled) and V4-EXM-32 case definition do not depend on EU-D1's premise
and can proceed in parallel.

## 6.5 Limits

- Nothing was run against a candidate; no Codex process was started.
- PEC and Domains facts come from repository files only (no network).
- Reach was computed by my script, not by a project-designated tool.
- The App-side parts of OI-022 and OI-023 are treated as design matters on
  the reading in §1.1 and §3.4; HELP_HUMAN rules the labels.
- I read the SWBPIPE records as data about SWBPIPE's state, never as
  commitments.
