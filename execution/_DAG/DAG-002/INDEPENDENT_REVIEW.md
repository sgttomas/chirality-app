# V12 — independent review of the SoW revisions, the registers and the DAG-002 candidate

**Verdict: READY FOR CHECKPOINT C.** There are 0 BLOCKING findings, 3 MINOR
and 6 NOTE.

- F2 (the review packet) must be closed before the package is presented.
- F3 changes what the owner's answer to option A covers.

These are presentation steps. They are not defects in the graph, the
registers or the SoWs.

This review accepts nothing and claims no owner act. DAG-002 is an unaccepted
candidate, `_DAG/_LATEST.md` still names DAG-001, and only the owner can
decide checkpoint C.

## Reviewer and basis

| Item | Value |
|---|---|
| Node | V12, a Type 2 TASK (Claude Code subagent). It does not delegate. It wrote none of the reviewed files. It is the separate review instance that `project-dag` method Stage 4 step 3 requires, and it also gives the independent check of the RV (REVISE) and DX (register) work |
| Candidate | commit `e9dc4633b693cd8e3308a3aaa71b901262829ebb`, working tree clean. The change reviewed is `a0af39f8c..e9dc4633b` (checkpoint B accepted → checkpoint C package). The graph basis is `b585e5ebe`. No `PKG-*` byte changed between `b585e5ebe` and `e9dc4633b` |
| Authority read | `OWNER_DECISIONS.md` DECISION-6…9 (exact text); accepted snapshot `_ScopeChange/SCA-V4-001_2026-09-28_2155/` (`Amendment_Actions.csv` sha256 `069645d9…`, whose MODIFY rows name exactly the 16 revised deliverables); `AMENDMENT_PACKET/SOW_REVISIONS.md` sha256 `9b4d700ddc9d…7e27b`, which is unchanged since checkpoint B; `BRIEFS.md` RV and DX; `DISPATCH.md` (the DEL-09-06 guard ruling) |
| Method | `workflows/scope-of-work` (REVISE and VERIFY); `workflows/dependency-extract` (WORKFLOW.md, resources/checks.md); `workflows/project-dag` (resources/method.md, currency.md, graph-version.md); `docs/SPEC.md` §11.2 |
| Tools used | `tools/coordination/audit_dag.py` `830d0d53…3449a`; `tools/scope_of_work/validate_scope_of_work.py` `f0f10590…`; `check_boundary_owner_resolution.py`; `tools/validation/validate_dependencies_schema.py`, `validate_enum.py`, `validate_id_format.sh`, `validate_decomposition_registers.py` (EVQ, DRB); `validate_scc_resolution_case.py` |
| Own scripts | Seven scripts in the session scratchpad `V12/`, none reused from RV, DX or D1: `sow_apply.py` `e9554daf…`, `regs.py` `009beb02…`, `regcheck.py` `7f474d4e…`, `q2.py` `e26e2746…`, `q3.py` `5d831f32…`, `acct.py` `8cf1d70d…`, `sr6.py` `1e72bb42…` |
| Mode | Git read-only, no network. The only write is this file |

## 1. SoW REVISE: independent VERIFY — PASS

`sow_apply.py` parsed `SOW_REVISIONS.md` itself: 124 E-blocks and 162
old → new pairs. It applied each deliverable's blocks, in the listed order, to
that deliverable's `ScopeOfWork.md` at `a0af39f8c`. The two tokens were filled
from the accepted records: `{AMENDMENT_ID}` = `SCA-V4-001`,
`{AMENDMENT_SNAPSHOT}` = `SCA-V4-001_2026-09-28_2155`.

| Check | Result |
|---|---|
| Prior-contract sha256 equals the SOW_REVISIONS summary | 16/16 |
| Each `old` block occurs exactly once when applied | 162/162 |
| Applying the blocks reproduces the file at `e9dc4633b` **byte for byte** | 16/16. So nothing outside the E-blocks changed |
| Frontmatter unchanged (O-22) | 16/16 |
| Unfilled `{AMENDMENT…}` tokens | 0 |
| Each block's `Target:` is its own deliverable | 16/16 |
| `validate_scope_of_work.py` | 16/16 PASS, `SOW_V1` |
| `check_boundary_owner_resolution.py` | 16/16 exit 0 |
| `_STATUS.md` changed anywhere in the diff | 0 |
| Lifecycle | 14 IN_PROGRESS and 2 INITIALIZED (DEL-08-01, DEL-09-07). None is CHECKING or ISSUED, so REVISE was admissible |

The deliverable folders gained no other changes. Outside the run folder, the
diff touches only these files:

- 16 `ScopeOfWork.md`;
- 18 `Dependencies.csv`, 18 `_DEPENDENCIES.md` and 18 run records;
- `_DAG/_Candidates/DAG-002/`;
- `_DAG/cases/SCC-CASE-002/`;
- the two `_Evaluation` snapshots and their `_LATEST.md` files.

The carried items in DISPATCH are correctly left alone: the DEL-03-03 CLM-002
tail, and the REVISION_SCOPE header lines that omit CLM-002 for DEL-03-01 and
DEL-03-03. The AX lines do name CLM-002, and the E-blocks apply as written.

## 2. Registers (18 deliverables) — PASS, with F1

The registers that changed are exactly the DECISION-9 set: the 16 revised
deliverables plus DEL-01-04 and DEL-02-02.

| Check | Result |
|---|---|
| Rows extracted from ScopeOfWork.md only | All 435 ACTIVE rows in the 18 registers are `Origin=EXTRACTED` with `EvidenceFile=ScopeOfWork.md` and `LastSeen` 2026-09-29. There is no ACTIVE `DECLARED` row |
| Quote verbatim in the current SoW | 401 exact substrings. **34 match only after inline-code backticks are ignored** (F1). 0 not found |
| Quote length ≤ 30 words | 435/435 |
| Schema, enum and ID validators | 18/18 schema VALID; every used enum value valid; every DEP, DEL and PKG ID valid; DependencyID prefix = FromDeliverableID; IDs unique |
| `validate_decomposition_registers.py --families EVQ,DRB` over all 41 | 0 errors, 0 warnings |
| `_DEPENDENCIES.md` counts against the CSV | 18/18 agree |
| Human-owned sections (Tracking Mode, Declared Upstream, Declared Downstream) | **54/54 byte-identical** to `a0af39f8c` |
| Row deletions | 0. There are 63 new rows (53 deliverable-target, 10 EXTERNAL) and 52 carried rows with field edits |

**Retirements (4).** All four are justified:

- DEP-02-03-015/-016 and DEP-05-02-014/-015 were the OI-001/OI-002
  open-decision constraints;
- the revised TBD text now says these are ruled for the first increment by
  `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2/D3 (DEL-02-03 TBD-002: "No
  open part remains for the first increment");
- each note names the row that carries the residue: DEL-04-01 (DEP-02-03-012,
  DEP-05-02-008) and OI-021.

Each retirement is `retired_by=source_revised`, keeps its row, and keeps
`LastSeen` at the last observation.

**Guards.** I checked every row in all 41 registers, of any status.

- No row makes an SCC-002 member depend on DEL-09-06.
- DEL-09-06 has no DOWNSTREAM row to any deliverable. Its DOWNSTREAM rows 020
  and 033 target the external DEP-001.
- Only DEL-03-04 (N-B10) and DEL-09-07 reach DEL-09-06, and neither is in
  SCC-002.
- There is no DEL-09-09 → DEL-09-06 arc and no DEL-09-09 → DEL-03-04 arc.
- There is no DEL-03-02 → DEL-04-03 arc (N-12) and no DEL-03-03 → DEL-04-03
  arc (N-B8).
- None of E-1…E-5 or K-1…K-12 (ARC_ANALYSIS §4) is present.
- DEL-04-01 consumes no deliverable.
- The three guarded pointers (DEL-05-01 TBD-003, DEL-05-02 TBD-003 and
  DEL-09-09 CLM-004) produced no row on DEL-09-06.

The integrator's DEL-09-06 ruling matches three sources:

- SOW_REVISIONS "Grounding … and extraction guards": "DEL-09-06's new names
  are all its own suppliers";
- ARC_ANALYSIS §4.1–4.2;
- the arc set the owner accepted in DECISION-6, which includes N-19,
  N-C1…N-C4 and N-08.

**The four arcs that rest only on a supplier-side row.** I read the consumer
SoWs.

| Arc | Supplier row | Consumer SoW | Warranted? |
|---|---|---|---|
| N-05 DEL-03-02 → DEL-04-02 | DEP-04-02-021 HANDOVER, EXPLICIT: "Its visible autonomy state is received by … DEL-03-02 …" | CLM-004 names DEL-04-02 only as owner of "autonomy and result-standing receiving behavior". The SoW otherwise frames DEL-03-02 as *supplier* to DEL-04-02 (CLM-004 last sentence; Production paragraph). REQ-004/AC-005 turn on "granted direct autonomy" | **Yes, on the supplier's explicit statement.** The consumer is compatible but silent. The arc forms a reciprocal pair with DEP-04-02-015 inside SCC-002 |
| N-06 DEL-03-03 → DEL-04-02 | DEP-04-02-022, same sentence | CLM-002 consumes "adopted PKG-04 operation-policy distinctions"; REQ-003 "actual adopted autonomy and reserved-act rules … policy supplied through PKG-04"; OUT-002 "actual access and autonomy grants" | **Yes.** The consumer states consumption at package level (PKG-04), and the supplier resolves it to DEL-04-02 |
| N-07 DEL-02-03 → DEL-04-02 | DEP-04-02-023, same sentence | CLM-002 "`DEL-04-02` owns grant display states"; REQ-006 exclusion; REQ-002/VER-002 operate "under identified direct-application autonomy" | **Yes, on the supplier's explicit statement.** The consumer text is an ownership sentence only, the same kind that left N-21 and N-24 unproduced (F6 note) |
| N-20 DEL-03-03 → DEL-02-01 | DEP-02-01-027 INTERFACE, IMPLICIT/MEDIUM: "`DEL-03-03` receives the declared checkpoint constraints, for carriage on the external channel in the governance phase" | DEL-03-03 does not name DEL-02-01. It consumes DEL-02-03's checkpoint statement and hold machine (CLM-002), and REQ-003 says "Workflow checkpoints retain their required human act" | **Yes, as a governance-phase interface.** The row and its Notes say so ("no current-phase carriage is implied"). The arc is held and non-gating |

All four sit inside SCC-002 and are held. None changes a verdict.

## 3. Closure and currency — PASS

`regs.py` recomputed the arcs from all 41 registers at `a0af39f8c` and
`e9dc4633b`. It took ACTIVE EXECUTION rows with a DELIVERABLE target; UPSTREAM
is From → Target and DOWNSTREAM is Target → From. It then ran Tarjan's
algorithm.

- **Arcs:** 161 → 198: 37 added, 0 removed. The added set equals `added_arcs.csv`.
- **SCCs:** 6, with member sets identical before and after: SCC-002's 13; {01-01, 01-05}; {01-06, 09-01}; {07-01, 07-02, 08-01}; {10-02, 10-04}; {11-01, 11-03}.
- **Rows:** 403 → 462 ACTIVE EXECUTION rows; 201 → 254 with a deliverable target.
- **SCC-002 internals:** 76 rows, 62 arcs and 16 reciprocal pairs. There are 22 pairs in the whole graph. This matches the closure report and CASE-002.
- **Currency:** `DEPARTURE` is correct, because arcs were added. The endpoints of the 37 added arcs are exactly the 15 listed as `DAG pending`: the 14 first-increment deliverables plus DEL-02-02 (via N-C1).
- **DEL-01-04 is not pending,** and the report gives the right reason. X-1 is not in any register, so no changed arc touches DEL-01-04. Its register's byte changes are evidence drift only.
- **Manifest checks:** DAG-001's `MANIFEST.sha256` gives 61/61 OK. `SOURCE_MANIFEST.sha256` against the current tree gives 78 OK and 52 FAILED, and the 52 are exactly the 16 SoWs, 18 CSVs and 18 `_DEPENDENCIES.md`.

## 4. DAG-002 candidate — PASS

| Check | Result |
|---|---|
| `python3 tools/coordination/audit_dag.py --dag-dir projects/chirality-app-v4/execution/_DAG/_Candidates/DAG-002 --canonical --strict`, from the repository root | **exit 0**: 124 edges, 41 nodes, canonical findings 0, endpoint issues 0, SCCs 0, duplicates 0, bidirectional 0 |
| Accounting (`acct.py`) | 124 + 74 + 264 = **462**. Every ACTIVE EXECUTION row is placed exactly once, with 0 unplaced and 0 duplicated. Every placement's `SourceRegisterSHA256` and `SourceRecord` match the live register. The 198 admitted and candidate rows equal their source rows in all 29 core columns |
| Arc sets | Admitted ∪ candidate = my 198 arcs. Candidate = exactly the 74 intra-SCC arcs. DAG-001's admitted and candidate sets are subsets of DAG-002's, so no existing arc changes layer |
| Exclusions | NOT_TOPOLOGICAL 208 (EXTERNAL 150, DOCUMENT 26, PACKAGE 18, UNKNOWN 14), MIRROR 54, SAME_ARC 2. Every MIRROR and SAME_ARC names its arc's representative |
| SR-6 representative | Recomputed as consumer UPSTREAM, then DECLARED, then lowest ID: 198/198 agree |
| Carried rules and rulings | SR-1…SR-7 unchanged. `DeliverableNodes.csv` is byte-equal to DAG-001's. Each SCC's `CaseRef`, `OpenQuestion` and `CandidateReason` are identical to DAG-001's for all six SCCs. Only the arc set is reopened, and it was decided at checkpoint A |
| Case citations | All 74 held arcs are `SCC_UNRESOLVED` and cite their continuing case (SCC-002 → CASE-002, SCC-004 → CASE-005, and so on) |
| CASE-002 update | Evidence only: E3-* rows, F-046, a datasheet section and QA note. The figures (76/62/16; the 22 labels; the representative and mirror account) agree with my recomputation. `validate_scc_resolution_case.py` gives PASS, exit 0 |
| `PROPOSED_LATEST.md` | Its first two lines are the SPEC §11.2 form (`Latest: DAG-002`, `Updated: {ACCEPT_DATE}`). The extra field lines and prose do not disturb `dependency_evidence.POINTER_LINE` (a multiline regex) |
| Protected files | `_DAG/_LATEST.md` and `_DAG/DAG-001/` are unchanged in the diff; DAG-001 `MANIFEST.sha256` gives 61/61 OK |
| Source manifest | 130/130 OK against the current tree; sha256 `6d1021f1…93250`; same paths as DAG-001; 52 changed |
| Other GRAPH_BASIS figures | RequiredMaturity TBD 215; SatisfactionStatus TBD 302; DEL-04-01 has 20 admitted dependents and 0 suppliers; DEL-04-03 has degree 27; both mirror maturity differences exist as stated |

## 5. CHECKPOINT_C.md — PASS, with F2 and F3

**Facts.** I checked every factual claim against the files, and all are true:

- 37 arcs added: 15 admitted and 22 held;
- 0 arcs removed;
- 6 SCCs with unchanged members, and nodes byte-identical;
- 462 rows, each placed once;
- the strict audit exits 0;
- 15 deliverables pending, and DEL-01-04 not pending, for the stated reason;
- DEL-01-01 supplies six deliverables and DEL-09-06 consumes eight;
- N-12 and N-B8 are absent and all nine grounded arcs are present;
- the hub list is correct (27/20/20);
- all eight file hashes in §8 match.

**The four accepted arcs that were not produced.** §4 and §5 explain N-18,
N-21, N-24 and X-1 accurately:

- The DEL-02-01 and DEL-02-03 SoWs name DEL-03-02, DEL-03-03 and DEL-01-04
  only as owners or constructors.
- Both registers recorded the ownership-is-not-an-edge convention before this
  run, in their Run Notes at `a0af39f8c`.
- No supplier SoW names DEL-02-01 or DEL-02-03 as a receiver. I checked
  DEL-03-02, DEL-03-03 and DEL-01-04.
- All four would be held inside SCC-002, so no verdict changes.
- X-1's absence keeps DEL-01-04 off `DAG pending`.

**Recommendations.** They are sound, subject to F2 and F3:

- One successor for all 37 arcs is right. Splitting keeps deliverables
  pending longer and decides nothing extra.
- Option A leaves no work held.
- Keeping the DEL-09-06 guard in the handoff is right: any reverse row would
  form a cycle.
- Writing the §11.2 pointer at publication is right.

**Nothing implies acceptance.** The page says so twice, and §7 is conditional
throughout.

## Findings

### BLOCKING

None.

### MINOR

**F1 — 34 evidence quotes drop inline-code backticks.**

- **Affected rows:** DEL-04-01 (9: 017, 018, 022–027, 029), DEL-04-02 (12:
  011, 012, 015–023, 025) and DEL-04-03 (13: 019, 021–032).
- **What differs:** each quote reproduces the SoW's words exactly but leaves
  out the SoW's `` ` `` marks, for example `` App v4 `DEL-03-02` `` → "App v4
  DEL-03-02".
- **Disclosure:** the DX-1 run records disclose it ("markdown emphasis/code
  marks ignored"). The DX-1 returns say "verbatim quotes".
- **Why it matters:** it breaks the repository's convention. At `a0af39f8c`,
  758/758 ACTIVE quotes were exact substrings, and the other 15 registers are
  exact now.
- **Effect:** none on any arc, count or verdict. The EVQ validator does not
  test substrings.
- **Route:** the three register owners (`dependency-extract`) re-quote
  exactly at the next UPDATE, for example with SCA-V4-002. Alternatively, the
  owner records the relaxed convention explicitly.

**F2 — The review packet is sequenced after acceptance.**

- **The problem:** CHECKPOINT_C §7 step 1 puts `REVIEW_PACKET.md` under "If
  you accept". The method puts it before checkpoint 2 (Stage 4 step 4: "Write
  `REVIEW_PACKET.md` with the SHA-256 of every graph file being presented"),
  and §8 of the page itself says the packet "will restate them for
  presentation".
- **A related gap:** because both checkpoints are taken together, the method
  requires recording "that the decision covers both". §7 step 2 does not say
  this.
- **Fix before presenting:**
  - write `REVIEW_PACKET.md` with the eight hashes and this review;
  - move §7 step 1 ahead of the decision;
  - have the ACCEPTANCE_RECORD state that it covers checkpoints 1 and 2.

**F3 — Option A widens SCA-V4-002 beyond what the owner authorized.**

- DECISION-8 authorized SCA-V4-002 for one item: DEL-10-03 REQ-005
  "local-first".
- Option A routes more to it: the consumption wording for N-18, N-21, N-24
  and X-1. The page's C2-5 routes the carried DX and RV items there as well:
  - the OI-001/002/012 SoW text in DEL-09-07, DEL-01-04 and DEL-02-02;
  - the DEL-03-03 CLM-002 tail;
  - the A17b line join.
- The page should say that answering "A" also widens that follow-on
  amendment's scope. Otherwise the widening needs its own scope decision under
  `scope-change`.

### NOTE

**F4.** In option B, "DAG-002 grows to 41 arcs" should read "41 added arcs
(202 in all)".

**F5.** DX-1 read ARC_ANALYSIS.md, REGISTER_CHANGES.md §1–§3 and the DAG-001
edge files during its DEL-04-01 comparison. That was before it extracted its
other five deliverables. It disclosed this in each run record, so the
extraction was not blind to the expected arcs.

- **Mitigation:** every row is grounded by a quote in the current SoW (§2),
  and the four arcs DX-2 did not produce show the extractors did not simply
  copy P2.

**F6.** N-07 and the unproduced N-21 and N-24 have the same kind of text on
the consumer side: DEL-02-03 names the supplier only as an owner.

- **Why N-07 is in the graph:** only because DEL-04-02's SoW names DEL-02-03
  as a receiver, while the DEL-03-02 and DEL-03-03 SoWs do not.
- **N-05** is in the same position.
- **For the owner:** keep this in view when choosing between option A and
  option D for the four arcs. SCA-V4-002 could also give N-05 and N-07
  consumer-side wording.

**F7.** The as-dispatched DEL-09-06 guard wording ("must not gain rows that
consume any SCC-002 member") is not in BRIEFS.md. It is recorded only in the
DX-3 return and the DEL-09-06 Run Notes. The ruling itself is correct (§2).

**F8.** OI-001/OI-002 constraint rows are handled differently across
registers:

- retired in DEL-02-03 and DEL-05-02;
- amended and kept in DEL-04-01, DEL-04-02, DEL-04-03 and DEL-09-06.

Both treatments are source-grounded and off-arc. This is a consistency point
for the register owners.

**F9.** `pointer_form_check.json` tested a two-line pointer, not the bytes of
`PROPOSED_LATEST.md`. The parser's multiline `Latest:` regex reads both the
same way, so the result carries over.

## Counts

- **SoW revisions:** 16 SoWs, 124 E-blocks, 162 replacements. 16/16 reproduce
  exactly and 16/16 validate; 0 `_STATUS.md` changes.
- **Registers:** 18 registers and 435 ACTIVE rows (401 exact quotes, 34
  backtick-only). 54/54 human sections unchanged. 63 rows added, 52 edited, 4
  retired, 0 deleted.
- **Graph:** 198 arcs (161 + 37, 0 removed) and 6 unchanged SCCs. 15 `DAG
  pending`.
- **DAG-002:** 41 nodes; 124 admitted, 74 held and 264 excluded, which is 462
  rows. `audit_dag --canonical --strict` exits 0.
