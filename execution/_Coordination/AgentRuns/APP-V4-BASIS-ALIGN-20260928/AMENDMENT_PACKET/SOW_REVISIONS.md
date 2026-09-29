# SoW revisions — APP-V4-BASIS-ALIGN-20260928, node P1

**Status: PROPOSED (scope-change checkpoint-group-2 preparation). Nothing here
is applied.** Every edit below is an exact old → new replacement for one
`ScopeOfWork.md`, to be applied after the owner accepts it, by
`scope-of-work` `MODE=REVISE`, one deliverable per brief (owner direction,
[OWNER_DECISIONS.md](../OWNER_DECISIONS.md), "Governance route").

- **Basis:** commit `874508f16`. Every "old" block was checked against the
  current SoW bytes: each occurs exactly once, and the edits apply in the
  listed order with no overlap (see "Mechanical checks" at the end).
- **Companion files:** [IMPACT_ASSESSMENT.md](IMPACT_ASSESSMENT.md) (atomic
  actions, DAG impact), [BASIS_AMENDMENT.md](BASIS_AMENDMENT.md) (PRD,
  ARCHITECTURE, HOST_INTEGRATION, EXAMINATION and decomposition rows),
  [OWNER_ITEMS.md](OWNER_ITEMS.md) (decisions needed).

## Reading this file

- **Edit IDs** are `E-<deliverable>-<nn>`. Apply each deliverable's edits in
  the listed order. A few edits anchor on text an earlier edit of the same
  deliverable introduces; this is stated where it applies.
- **Disposition** of the source proposal: **KEEP** (C1 text applied as
  written), **AMEND** (C1 text refreshed against the current Design files and
  decisions; the reason is given), **NEW** (not a C1 item; traced to a later
  finding or an owner decision).
- **Conditional** edits depend on an owner item in
  [OWNER_ITEMS.md](OWNER_ITEMS.md). If the owner declines one, drop that
  edit and remove its IDs from the deliverable's amendment-reference line.
- **Acceptance-conditional tokens.** `{AMENDMENT_ID}` is the accepted
  amendment ID (recommended `SCA-V4-001`, item O-1). `{AMENDMENT_SNAPSHOT}` is
  the accepted group-3 snapshot folder name under
  `projects/chirality-app-v4/execution/_ScopeChange/`. Both are filled at
  application from the accepted records; no other byte depends on the
  acceptance act.
- **Amendment reference.** Each revised SoW gains one Axiology `AX-*` line
  naming the amendment, its snapshot, the decisions applied, and the revised,
  added and removed IDs (REVISE step 4). Its ID list is exactly the IDs whose
  text the accepted edits change.
- **No new OUT, AC or VER IDs** are added anywhere, and no ID is renumbered or
  removed. New IDs are TBD and AX only. The matrix gains no row; two matrix
  cells change wording.
- **Frontmatter is unchanged** in every SoW, including `decomposition_basis`.
  Several SoWs define their row keys ("G3", "B", "D") as the Group3 snapshot
  named in the frontmatter, so moving the basis would break those keys. The
  amended ledger rows are cited explicitly instead (item O-22).

Decision identities used in the new text:

| Short form here | Full identity | Record |
|---|---|---|
| DECISION-1 (D1–D4) | `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` | `execution/_Coordination/AgentRuns/APP-V4-FIRST-INCREMENT-20260928/OWNER_DECISIONS.md` |
| DECISION-2 (D5, D6) | `APP-V4-FIRST-INCREMENT-20260928-DECISION-2` | same file |
| DECISION-3 | `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-3` | `execution/_Coordination/AgentRuns/APP-V4-SWBPIPE-INTAKE-20260928/OWNER_DECISIONS.md` |
| DECISION-4 (D4-1, D4-3) | `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4` | same file |
| DECISION-5 | `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-5` | same file |

The SoW text always uses the full identity.

## Summary

| Deliverable | Prior SoW sha256 | Lifecycle | Edits | From C1 (K / A) | New | Conditional |
|---|---|---|---|---|---|---|
| DEL-04-01 | `fc1a0503abad4196e869402b664bd76280773d197b5c77994c34e858a406f5e6` | INITIALIZED | 11 | 9 / 1 | 1 (AX) | — |
| DEL-04-02 | `23a28caabd61da20dc2efed722f7e487856ef4488ab4f3454be4ed3249725e21` | INITIALIZED | 8 | 3 / 3 | 2 | E-0402-02, -03 (O-11); E-0402-08 (O-15) |
| DEL-04-03 | `74d42c38eaf2a6638b75bc5184f1741bc7d4f17171662a05a233d40f245340c1` | INITIALIZED | 5 | 2 / 2 | 1 (AX) | E-0403-03 (O-10, O-14) |
| DEL-02-01 | `080d7f5a8e55d93c06f51e5332b53954deb03e0877b1ee49be3011e3de14a294` | INITIALIZED | 9 | 4 / 2 | 3 | — |
| DEL-02-03 | `9a921ba500271c441e64db2e1f34acf41c95fa7821d6dff3d8659352bb4db7fb` | INITIALIZED | 13 | 1 / 4 | 7 | — |
| DEL-03-01 | `179a6d355d84dba915daddd746d9d62eb7c8ef483e68122a096dfbde6f6b3b84` | INITIALIZED | 7 | 4 / 1 | 2 | E-0301-04, -05 (O-9) |
| DEL-03-02 | `42328987c71dd243323805faf2634067cca0113b81ca93d4d129193b2a71128a` | INITIALIZED | 7 | 2 / 3 | 2 | E-0302-03 (O-9) |
| DEL-03-03 | `5ac5db97eba3851eb5324054e5a2b38429a53e8e9c85428903432cd8d9efb1b6` | INITIALIZED | 7 | 3 / 2 | 2 | E-0303-02 (O-9, O-10) |
| DEL-03-04 | `203c09288850d33ec3490d00da48bd6bbbc91ae395141c1374c4c6b04ad9a436` | INITIALIZED | 7 | 2 / 4 | 1 (AX) | E-0304-06 (O-13) |
| DEL-01-01 | `eddd122cf8b6e2c1ce5933ddb82aa9ec8591baa138a20f439e171ce5d83c4773` | INITIALIZED | 4 | 3 / 0 | 1 (AX) | — |
| DEL-05-01 | `6fbbb580bdacb7f34b4df98a826519a28c087aff6e589ad27330ee556a83b568` | INITIALIZED | 15 | 2 / 2 | 11 | — |
| DEL-05-02 | `5c554956e91b2d8d5056176f85717cbd0e17a2d2d2991a52ea4ff185ebfd40cb` | INITIALIZED | 7 | 4 / 2 | 1 (AX) | E-0502-03 (O-12) |
| DEL-09-06 | `511f2c0016920cbf67476f1b8d911ed85d6cfa419e7a6b15f3c7e20457779b37` | INITIALIZED | 6 | 2 / 2 | 2 | E-0906-02 part (a) (O-10) |
| DEL-09-09 | `082db8fa70bf0ceb8c8bf3c3a7fc4a222994858c66fdc7d9e5f16909f3ed862d` | INITIALIZED | 6 | 4 / 1 | 1 (AX) | — |
| DEL-09-07 | `36cc2e24595f0585111929204e27943f68b79bb54001ba52a3356aba9f78c1a0` | INITIALIZED | 10 | — | 10 | whole deliverable (O-19) |
| DEL-08-01 | `581b399ff56c5c9ee153916727b6245cda9aa116487087759f2b2bd7c765ddf1` | INITIALIZED | 2 | — | 2 | whole deliverable (O-18) |
| **Total** | | | **124** | **45 / 29** | **49** | |

An "edit" is one numbered E-block (124 blocks, 162 old → new replacements).
The "From C1" column counts C1 items, not blocks: several C1 items can map to
one block, and one item can span several blocks (the mapping is in the C1
disposition register below). "New" counts E-blocks with no C1 source: the 16
amendment-reference AX lines and 33 other edits. Four of the 33 are the node-P2
grounding sentences E-0301-07, E-0302-07, E-0303-07 and E-0402-08. They are
numbered after the other edits of their deliverable but placed before its AX
line, and the checks applied them in the listed order.

---

## DEL-04-01 — Operation-policy and human-act distinctions

REVISION_SCOPE: SOW-179 traceability row; CLM-002; CLM-004; REQ-004; AC-004;
AC-007; VER-004; VER-007; AX-001; TBD-001; TBD-002; new TBD-004; new AX-005.

#### E-0401-01 · SOW-179 traceability row · C1 SC-04-01-1 · KEEP
Target: DEL-04-01
Trace: DECISION-1 D2; ACT §8.2 P-01; ACT F-10.
```old
| SOW-179 | Adopted reserved-act policy and enforcement obligations for embedded and external agents; pending global list retained |
```
```new
| SOW-179 | Adopted reserved-act policy and enforcement obligations for embedded and external agents; first-increment reserved list adopted by `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2; operation-specific additions retained (OI-021) |
```

#### E-0401-02 · CLM-002 · C1 SC-04-01-2 · KEEP
Target: DEL-04-01
Trace: ACT F-1; V1-A RF-02; ACT §10 V-01…V-14. Grounds the C1 mirror rows R-04-01-a…f (no new arc).
```old
This deliverable supplies their policy meaning without taking over their production.
```
```new
This deliverable supplies their policy meaning without taking over their production. It also supplies policy meaning to App v4 `DEL-03-02`, `DEL-03-03`, `DEL-03-04`, `DEL-05-01`, `DEL-05-02` and `DEL-09-09`, each of which declares it upstream in its own register.
```

#### E-0401-03 · CLM-004 · C1 SC-04-01-3 · KEEP
Target: DEL-04-01
Trace: DECISION-1 D2/D3 and its "Effects" (C1 reconciles the pointers).
```old
S/DECISION_BRIEF.html#d3 explicitly leaves both choices open.
```
```new
S/DECISION_BRIEF.html#d3 explicitly leaves both choices open. For the first increment's App/shared contracts, the owner ruled OI-001 and OI-002 in `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` (D2, D3; record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-FIRST-INCREMENT-20260928/OWNER_DECISIONS.md`). Operation-specific additions remain with OI-021; the `Open_Issues.csv` rows are updated through their own route.
```

#### E-0401-04 · REQ-004, third sentence · C1 SC-04-01-4 · KEEP
Target: DEL-04-01
Trace: DECISION-1 D2/D3; the requirement's meaning is unchanged.
```old
A concrete unruled operation shall await the applicable OI-001/OI-002 decision before dependent operation-policy production or permission-policy implementation;
```
```new
A concrete unruled operation shall await its applicable decision (for the first increment: operation-specific additions under OI-021; the App/shared OI-001/OI-002 rulings are `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2/D3) before dependent operation-policy production or permission-policy implementation;
```

#### E-0401-05 · AC-004 and VER-004 · C1 SC-04-01-5 · KEEP
Target: DEL-04-01
Trace: ACT F-10; ACT VC-004; DECISION-1 D2.
```old
unresolved operations identify the applicable OI-001/OI-002 decision, owner and point of need
```
```new
unresolved operations identify the applicable open policy decision (OI-021 or a successor), with its owner and point of need
```
```old
- **VER-004** — Compare each adopted reserved-act case with its actual policy decision and inspect embedded/external enforcement conformance evidence from the responsible implementation. For each unruled case, inspect the OI-001/OI-002 owner and point-of-need hold;
```
```new
- **VER-004** — Compare adopted reserved-act cases with `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2 and its DERIVED extensions; compare each adopted reserved-act case with its actual policy decision and inspect embedded/external enforcement conformance evidence from the responsible implementation. For each unruled case, inspect the open policy decision (OI-021 or a successor), with its owner and point-of-need hold;
```

#### E-0401-06 · AC-007 and VER-007 · C1 SC-04-01-6 · KEEP
Target: DEL-04-01
Trace: ACT §8.1 rules; ACT VC-007; DECISION-1 D2/D3.
```old
and supplies no inferred always-reserved list or classifier treatment.
```
```new
and supplies no reserved list or classifier treatment beyond the adopted `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` rulings.
```
```old
Compare unresolved entries to OI-001/OI-002 and confirm they select neither a global list nor classifier behavior.
```
```new
Compare carried values with `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2/D3 (and their labeled DERIVED/INTEGRATION extensions) and unresolved entries with OI-021 and the other open items; confirm none selects a value without a decision basis.
```

#### E-0401-07 · AX-001 · C1 SC-04-01-7 · KEEP
Target: DEL-04-01
Trace: DECISION-1.
```old
do not resolve the questions explicitly retained in S/DECISION_BRIEF.html#d3 and OI-001/OI-002.
```
```new
do not resolve the questions explicitly retained in S/DECISION_BRIEF.html#d3 and OI-001/OI-002. Those questions were subsequently ruled for the first increment by `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2/D3; the historical texts still do not supply values.
```

#### E-0401-08 · TBD-001 · C1 SC-04-01-8 · KEEP
Target: DEL-04-01
Trace: DECISION-1 D2; ACT U-01. DECISION-4 D4-1 confirms that reserved acts stand. The DECISION-5 person-only network-destination grant is not added here (item O-15).
```old
- **TBD-001** — OI-001 remains OPEN: owner with App/SWB contract owners chooses always-reserved acts by concrete operation and consequence before operation-policy production contracts. This SoW defines the required work/evidence without choosing that list. Any affected concrete policy production waits for the decision; independent definition continues.
```
```new
- **TBD-001** — OI-001 — ruled for the first increment (App/shared contracts) by `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2: marking checked; accepting a proposal where the autonomy requires one; engineering approval; professional reliance; changing the grant or enabling external access. The host names and enforces its own list (V4-HI-30; DEP-001). Operation-specific additions remain OPEN under OI-021 (owner via the outside SWB session and App/shared owner; before the connected-activity SoW).
```

#### E-0401-09 · TBD-002 · C1 SC-04-01-9 · KEEP
Target: DEL-04-01
Trace: DECISION-1 D3.
```old
- **TBD-002** — OI-002 remains OPEN: owner with App/SWB contract owners distinguishes routine tool permissions from professional acts and settles App/host classifier treatment before permission-policy implementation. No historical pending value or fixture default substitutes for this decision.
```
```new
- **TBD-002** — OI-002 — ruled by `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D3: in the App, routine tool-permission and sandbox modes (including classifier-based modes) remain the user's own Codex setting and never stand in for a reserved or professional act; hosts have no classifier permission mode in the first increment. No open part remains for the first increment.
```

#### E-0401-10 · new TBD-004 · C1 SC-04-01-10 · AMEND
Target: DEL-04-01
Trace: DECISION-4 D4-1 (phased checkpoints); R8-1; R8-2 (D6 closed for Phase 1); ACT F-20.
**Why amended:** C1 deferred App-side holds to SWBPIPE's SQ-02 answer (D6). SQ-02
is now answered (no host-held route planned), and DECISION-4 makes
checkpoints plan guidance in the current phase, with enforced holds a later
governance layer. The TBD now records that phasing. It also reads REQ-001's
and REQ-006's "checkpoint override" wording for the current phase, which ACT
F-20 flagged.
```old
- **TBD-003** — DEP-001 host implementation/conformance evidence remains external and unestablished by this contract. Obtain the relevant host contribution before claiming corresponding host enforcement or connected behavior; its absence does not erase the App/shared policy definition duty.
```
```new
- **TBD-003** — DEP-001 host implementation/conformance evidence remains external and unestablished by this contract. Obtain the relevant host contribution before claiming corresponding host enforcement or connected behavior; its absence does not erase the App/shared policy definition duty.
- **TBD-004** — Declared checkpoints are phased (`APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4` D4-1). In the current phase a declared checkpoint is plan guidance: its required act is recorded only when the person performs it, autonomy never records or substitutes that act (REQ-001, REQ-006), reserved acts stand, and neither the App nor a host's embedded loop claims or enforces a hold. Enforced holds, including App-side run holds (`APP-V4-FIRST-INCREMENT-20260928-DECISION-2` D6, closed for the current phase), are a later governance layer for the workflows that need it. **Owner:** the owner, when a workflow needs enforced checkpoints. **Point of need:** before any checkpoint is claimed held. This limits the VER-001 and VER-006 checkpoint cases to recording in the current phase; it does not change the policy meaning.
```

#### E-0401-11 · new AX-005 (amendment reference) · NEW · acceptance-conditional
Target: DEL-04-01
Trace: `scope-of-work` REVISE step 4.
```old
Later lifecycle acts remain separate.
```
```new
Later lifecycle acts remain separate.
- **AX-005** — Revised under scope-change amendment `{AMENDMENT_ID}` (accepted snapshot `projects/chirality-app-v4/execution/_ScopeChange/{AMENDMENT_SNAPSHOT}`), applying `APP-V4-FIRST-INCREMENT-20260928-DECISION-1`, `APP-V4-FIRST-INCREMENT-20260928-DECISION-2` (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-FIRST-INCREMENT-20260928/OWNER_DECISIONS.md`) and `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4` (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-SWBPIPE-INTAKE-20260928/OWNER_DECISIONS.md`). Revised: the SOW-179 traceability row, CLM-002, CLM-004, REQ-004, AC-004, AC-007, VER-004, VER-007, AX-001, TBD-001 and TBD-002. Added: TBD-004 and AX-005. Removed: none.
```

---

## DEL-04-02 — Visible autonomy and result standing

REVISION_SCOPE: source key U; CLM-002; REQ-007; AC-004; VER-004; TBD-001;
TBD-002; new TBD-006; new AX-004.

#### E-0402-01 · Source key U · C1 SC-04-02-1 · KEEP
Target: DEL-04-02
Trace: V1-B RF-01, RF-05; AS §4, §7, §8.
```old
| U | App v4 sibling contracts under `projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/`: `DEL-04-01_Operation-policy and human-act distinctions/ScopeOfWork.md` and `DEL-04-03_Content-bound decisions and compact run records/ScopeOfWork.md`; independently checked definition inputs, not implemented products |
```
```new
| U | App v4 sibling contracts: under `projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/`, `DEL-04-01_Operation-policy and human-act distinctions/ScopeOfWork.md` and `DEL-04-03_Content-bound decisions and compact run records/ScopeOfWork.md`; under `projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/`, `DEL-03-01_Capability catalog and read-basis contract/ScopeOfWork.md` and `DEL-03-02_Proposal, validation and outcome contract/ScopeOfWork.md`; and `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-03_Workflow execution compatibility and round-trip support/ScopeOfWork.md`; independently checked definition inputs, not implemented products |
```

#### E-0402-02 · CLM-002 · C1 SC-04-02-2 · AMEND · conditional (O-11)
Target: DEL-04-02
Trace: V1-A RF-05; V1-B RF-06; V1-C RF-4/RF-5; X-16; IR1-C §4; DECISION-4 D4-1.
**Why amended:** C1 named "`DEL-02-03` hold-support values and checkpoint
annotations". Under DECISION-4, hold support is the governance-phase
definition (R8-1). In the current phase AS consumes the checkpoint recording
annotations (AS header; EXEC §2.1 PH-6…PH-8). **Condition:** C1 made this
edit conditional on the SoW-level decision V1-A RF-05 asks for (direct
consumption, or routing through DEL-04-01/DEL-03-02). All five designs
consume directly (item O-11).
```old
This deliverable consumes those policy and record contributions. Defined and independently checked contracts
```
```new
This deliverable consumes those policy and record contributions. It also consumes App v4 `DEL-03-02` proposal/outcome and direct-application origin semantics, `DEL-03-01` read-basis and standing facets, and `DEL-02-03` checkpoint recording annotations (with the hold-support values retained for the governance phase). Its visible autonomy state is received by `DEL-05-01`, `DEL-05-02`, `DEL-03-02`, `DEL-03-03` and `DEL-02-03`. Defined and independently checked contracts
```

#### E-0402-03 · REQ-007, first sentence · C1 SC-04-02-3 · AMEND · conditional (O-11)
Target: DEL-04-02
Trace: AS §10; DECISION-4 D4-1.
**Why amended:** "the checkpoint hold machine" becomes "checkpoint recording
meanings and the governance-phase hold machine" (R8-1). **Condition:** this
edit names owners `DEL-02-03`, `DEL-05-01` and `DEL-03-03`. Only E-0402-02 names
them in CLM-002, which REQ-007 cites, so the boundary-owner check needs both
edits together.
```old
producing the human-act/run-file format, App reader/writer and content-change lapse handling belongs to App `DEL-04-03` (CLM-002).
```
```new
producing the human-act/run-file format, App reader/writer and content-change lapse handling belongs to App `DEL-04-03` (CLM-002); checkpoint recording meanings, the governance-phase hold machine and their annotations belong to App `DEL-02-03` (host loops: `DEL-05-01` receiving); channel status and model-destination display belong to App `DEL-03-03` (CLM-002).
```

#### E-0402-04 · AC-004 and VER-004 · C1 SC-04-02-4 · KEEP
Target: DEL-04-02
Trace: R-4 label rule (an unqualified "checked" means A4 only); AS §8 host-check facet.
```old
Current, historical, checked, limited and lapsed result cases
```
```new
Current, historical, host-checks-passed (each named check with its evaluated basis), limited and lapsed result cases
```
```old
Supply current, historical, checked, limited, content-lapsed
```
```new
Supply current, historical, host-checks-passed (each named check with its evaluated basis), limited, content-lapsed
```

#### E-0402-05 · TBD-001 and TBD-002 · C1 SC-04-02-5 · KEEP
Target: DEL-04-02
Trace: DECISION-1 D2/D3; IR1A-20; AS §10 note. This is the SC-04-01-8/-9 text in this file's citation style.
```old
- **TBD-001** — OI-001, Reserved human acts, remains OPEN. Owner: **Owner with App/SWB contract owners**. Point of need: **Before operation-policy production contracts**. Required resolution: choose always-reserved acts by concrete operation and consequence. The global list is not fixed; false attribution is already prohibited. App DEL-04-01 carries adopted policy and is not the decision actor. [I; S d3]
```
```new
- **TBD-001** — OI-001, Reserved human acts — ruled for the first increment (App/shared contracts) by `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2: marking checked; accepting a proposal where the autonomy requires one; engineering approval; professional reliance; changing the grant or enabling external access. The host names and enforces its own list (H V4-HI-30; I DEP-001). Operation-specific additions remain OPEN under OI-021 (owner via the outside SWB session and App/shared owner; before the connected-activity SoW). App DEL-04-01 carries adopted policy and is not the decision actor. [I; S d3]
```
```old
- **TBD-002** — OI-002, Classifier routine permissions, remains OPEN. Owner: **Owner with App/SWB contract owners**. Point of need: **Before permission-policy implementation**. Required resolution: distinguish routine tool permissions from professional acts and settle App/host treatment. No classifier behavior was selected by normalization. [I; P V4-AUT-04; S d3]
```
```new
- **TBD-002** — OI-002, Classifier routine permissions — ruled by `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D3: in the App, routine tool-permission and sandbox modes (including classifier-based modes) remain the user's own Codex setting and never stand in for a reserved or professional act; hosts have no classifier permission mode in the first increment. No open part remains for the first increment. [I; P V4-AUT-04; S d3]
```

#### E-0402-06 · new TBD-006 · C1 SC-04-02-6 · AMEND
Target: DEL-04-02
Trace: DECISION-4 D4-1; R8-1; R8-2; AS header (Phase 1: the overlay shows arrivals and acts as observation).
**Why amended:** C1's D6 deferral is replaced by the DECISION-4 phasing. The
display rule "never show an unenforced hold as held" becomes "show no hold in
the current phase".
```old
Independent App definition can proceed. [I DEP-001; S J/O]
```
```new
Independent App definition can proceed. [I DEP-001; S J/O]
- **TBD-006** — Declared checkpoints are phased (`APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4` D4-1). In the current phase the receiving display shows checkpoint arrivals and acts as observation, and it shows no hold, no hold-support value and no *unsupported* result for a hold reason. The autonomy display still never implies that a checkpoint's act is done (REQ-001). Hold-support display and App-side run holds (`APP-V4-FIRST-INCREMENT-20260928-DECISION-2` D6, closed for the current phase) belong to the later governance layer. **Owner:** the owner, when a workflow needs enforced checkpoints. **Point of need:** before hold-display fixtures run.
```

#### E-0402-08 · CLM-002 (consumption sentence) · NEW (node P2 grounding for R8-A) · conditional (O-15)
Target: DEL-04-02
Trace: grounds arc R8-A (DEL-04-02 → DEL-05-01), per ARC_ANALYSIS §2.3. Design basis: AS-v0.6 §3 network-destination grants, "from the host's control (LOOP §5.1.1 …)" (AS lines 213–214); R8-13. Decision: DECISION-5 ("Every destination contacted is recorded and shown"; the allow list; in-work grants). The A12 mapping of these grants stays INTEGRATION and is not stated here.
```old
Defined and independently checked contracts do not establish
```
```new
It also consumes, from App v4 `DEL-05-01`, a host agent's network-destination allow list, in-work destination grants and contacted-destination record, which `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-5` requires to be shown. Defined and independently checked contracts do not establish
```

#### E-0402-07 · new AX-004 (amendment reference) · NEW · acceptance-conditional
Target: DEL-04-02
```old
[CLM-001 through CLM-006; O V4-OPS-31/32]
```
```new
[CLM-001 through CLM-006; O V4-OPS-31/32]
- **AX-004** — Revised under scope-change amendment `{AMENDMENT_ID}` (accepted snapshot `projects/chirality-app-v4/execution/_ScopeChange/{AMENDMENT_SNAPSHOT}`), applying `APP-V4-FIRST-INCREMENT-20260928-DECISION-1`, `APP-V4-FIRST-INCREMENT-20260928-DECISION-2` (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-FIRST-INCREMENT-20260928/OWNER_DECISIONS.md`) `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4` and `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-5` (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-SWBPIPE-INTAKE-20260928/OWNER_DECISIONS.md`). Revised: source key U, CLM-002, REQ-007, AC-004, VER-004, TBD-001 and TBD-002. Added: TBD-006 and AX-004. Removed: none.
```

---

## DEL-04-03 — Content-bound decisions and compact run records

REVISION_SCOPE: CLM-002; CLM-004; REQ-002; REQ-005; TBD-001; new AX-004.

#### E-0403-01 · CLM-004 · C1 SC-04-03-1 · AMEND
Target: DEL-04-03
Trace: V1-A RF-01; V1-B RF-02, RF-04, RF-07; IR1A-19; RS §10; EXEC §9.2; DECISION-4 D4-1.
**Why amended:** "hold-machine events" becomes "checkpoint arrival, act and
lapse events, with hold events retained for the governance phase". This
follows the RS Phase-1 header (records keep arrivals, acts and lapses as
observation; no hold, re-hold or hold-support value in Phase 1). The
`DEL-05-01` network-destination clause is added from DECISION-5 and R8-13.
```old
PKG-06 decisions consume this format;
```
```new
PKG-06 decisions consume this format; it receives act kinds and classes from App `DEL-04-01`, settings-in from `DEL-04-02`, subject content identities and method designations from `DEL-03-01`, operation outcomes, change-item content identities and receipt links from `DEL-03-02`, checkpoint arrival, act and lapse events (with hold events retained for the governance phase) and compatibility reports from `DEL-02-03`, external dispatch entries from `DEL-03-03`, observed supplier facts (supplied guidance, model and destination, tool-permission settlements) from `DEL-01-01`, and a host agent's network-destination events (destination contacted, destination grant, destination declined) from `DEL-05-01` (`APP-V4-SWBPIPE-INTAKE-20260928-DECISION-5`);
```
The `DEL-05-01` clause grounds arc R8-B (DEL-04-03 → DEL-05-01; RS R15 "through DEL-05-01 events (LOOP §2.3, §5.1.1)", RS line 194; R8-13; ARC_ANALYSIS §2.3). The `DEL-01-01` clause grounds N-15, which C1 made conditional (owner item O-29).

#### E-0403-02 · REQ-005 · C1 SC-04-03-2 · KEEP
Target: DEL-04-03
Trace: existing UPSTREAM rows DEP-05-01-019, DEP-05-02-009, DEP-09-06-015, DEP-09-09-011; RS §10.
```old
identify how PKG-02 definitions/checkpoints, PKG-03 basis/receipts and PKG-06 decisions consume the record meaning
```
```new
identify how PKG-02 definitions/checkpoints, PKG-03 basis/receipts, PKG-05 loop and panel receiving (`DEL-05-01`, `DEL-05-02`), PKG-06 decisions and the PKG-09 connected-activity and trace contracts (`DEL-09-06`, `DEL-09-09`) consume the record meaning
```

#### E-0403-03 · CLM-002 and REQ-002 · C1 SC-04-03-3 · AMEND · conditional (O-10, O-14)
Target: DEL-04-03
Trace: DECISION-2 D5 (no gate, SETTLED); R4-1; R5-4 (record and show for App runs: an INTEGRATION reading, not yet owner-confirmed); DECISION-5 "Record and show" (SETTLED for host agents); R8-13 (RS R15).
**Why amended:** DECISION-5 settles that every destination a host's agent
contacts is recorded and shown, in any model mode. C1 covered only the App's
per-turn model destination. The claim CLM-002 carries the same inventory, so
it changes with REQ-002.
```old
host receipt references, actual human acts and model used. Host receipts,
```
```new
host receipt references, actual human acts, and model used with its observed destination per turn; for a host's agent it also identifies each network destination contacted, with the allowing grant or list entry. Host receipts,
```
```old
host receipt references, actual human acts and model used. It shall link
```
```new
host receipt references, actual human acts, and model used with its observed destination per turn; for a host's agent, each network destination contacted, with the allowing grant or list entry (PRD V4-HOST-02 as revised by `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-5`). It shall link
```

#### E-0403-04 · TBD-001 · C1 SC-04-03-4 · KEEP
Target: DEL-04-03
Trace: DECISION-1 D2/D3; IR1A-20; RS §11 note.
```old
- **TBD-001** — OI-001/OI-002 retain the exact always-reserved operation classes and classifier-permission policy with the owner and affected App/SWB contract owners. App DEL-04-01 carries adopted policy.
```
```new
- **TBD-001** — OI-001/OI-002 were ruled for the first increment by `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2/D3; App DEL-04-01 carries them. Operation-specific additions remain open under OI-021 (owner via the outside SWB session and App/shared owner; before the connected-activity SoW).
```

#### E-0403-05 · new AX-004 (amendment reference) · NEW · acceptance-conditional
Target: DEL-04-03
```old
[O V4-OPS-30…32; H V4-HI-71]
```
```new
[O V4-OPS-30…32; H V4-HI-71]
- **AX-004** — Revised under scope-change amendment `{AMENDMENT_ID}` (accepted snapshot `projects/chirality-app-v4/execution/_ScopeChange/{AMENDMENT_SNAPSHOT}`), applying `APP-V4-FIRST-INCREMENT-20260928-DECISION-1`, `APP-V4-FIRST-INCREMENT-20260928-DECISION-2` (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-FIRST-INCREMENT-20260928/OWNER_DECISIONS.md`), `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4` and `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-5` (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-SWBPIPE-INTAKE-20260928/OWNER_DECISIONS.md`). Revised: CLM-002, CLM-004, REQ-002, REQ-005 and TBD-001. Added: AX-004. Removed: none.
```

---

## DEL-02-01 — Portable workflow contract and shared allocation

REVISION_SCOPE: CLM-002; CLM-003; REQ-002; REQ-003; REQ-006; VER-003;
TBD-003; new TBD-004; new AX-005.

#### E-0201-01 · CLM-002 · C1 SC-02-01-1 · AMEND
Target: DEL-02-01
Trace: WD §8, §10; V1-C RF-7; R2-12, R2-18; DECISION-1 D2/D3; DECISION-4 D4-1.
**Why amended:**
- The governing checkpoint constraint is now the governance-phase
  definition (R8-1: R2-12 carriage assurance retained, not in force in
  Phase 1). It is labeled so.
- C1 wrote "`DEL-03-03` carries constraints on the external channel". Node P2
  found that DAG-001 extraction reads CLM-002 names as inputs, so that
  wording would ground an unevidenced reverse arc, DEL-02-01 → DEL-03-03
  (REGISTER_CHANGES §2.4 item 1). DEL-03-03 is therefore worded as a
  receiver. The same wording grounds N-20 (DEL-03-03 → DEL-02-01; ADAPTER §11
  "Expect from DEL-02-01 / DEL-02-03").
```old
`DEL-04-01` defines and carries adopted operation policy and human-act distinctions; the owner and host policy owner retain decisions on unresolved classes (OI-001/OI-002);
```
```new
`DEL-04-01` defines and carries adopted operation policy and human-act distinctions, including the first-increment OI-001/OI-002 rulings (`APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2/D3); operation-specific additions remain with the owner via the outside SWB session (OI-021); `DEL-03-02` owns proposal/outcome semantics, including item dispositions, item-left events and the governing checkpoint constraint (governance phase); `DEL-01-01` supplies the harness capability inventory and supplied-guidance identity evidence; `DEL-03-03` receives the declared checkpoint constraints, for carriage on the external channel in the governance phase;
```

#### E-0201-02 · REQ-002, second sentence · C1 SC-02-01-2 · KEEP
Target: DEL-02-01
Trace: WD §4.2.1; WD U-08; V1-C RF-7.
```old
Tool requirements shall refer to the capability meaning supplied by CLM-002, and tool schemas shall remain open.
```
```new
Host-operation requirements shall refer to the capability meaning supplied by `DEL-03-01`; harness-capability requirements shall refer to capability meaning supplied through `DEL-01-01` (CLM-002). Tool schemas shall remain open.
```

#### E-0201-03 · REQ-006 · C1 SC-02-01-3 · KEEP
Target: DEL-02-01
Trace: WD §10 rows.
```old
catalog-semantic definition by `DEL-03-01`, operation-policy contract definition and carrying adopted policy by `DEL-04-01`,
```
```new
catalog-semantic definition by `DEL-03-01`, proposal/outcome definition by `DEL-03-02`, external-channel constraint carriage by `DEL-03-03`, operation-policy contract definition and carrying adopted policy by `DEL-04-01`,
```

#### E-0201-04 · CLM-003, last sentence · C1 SC-02-01-4 · KEEP
Target: DEL-02-01
Trace: DECISION-1.
```old
qualified by HTML-D03 and OI-001/OI-002.
```
```new
qualified by HTML-D03 and the first-increment OI-001/OI-002 rulings in `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2/D3.
```

#### E-0201-05 · TBD-003, first sentence · C1 SC-02-01-5 · KEEP
Target: DEL-02-01
Trace: IR1A-20 pattern; WD §10. The false-attribution and OI-018 sentences are unchanged.
```old
- **TBD-003** — OI-001 and OI-002 retain operation-specific reserved-act and classifier policy choices with the owner and App/SWB contract owners at their stated policy points of need.
```
```new
- **TBD-003** — OI-001 and OI-002 were ruled for the first increment by `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2/D3 (carried by DEL-04-01). Operation-specific reserved additions remain with OI-021.
```

#### E-0201-06 · new TBD-004 (after TBD-003) · C1 SC-02-01-6 · AMEND
Target: DEL-02-01
Trace: DECISION-4 D4-1; R8-1; WD header, §4.3.0, U-33; R8-11 item 3.
**Why amended:** C1's TBD said that App-only checkpoints are *not
enforceable* and that a workflow depending on one is *unsupported* in App
runs. R8-1/PH-3 now rules that out in the current phase (no *unsupported* for
a hold reason). The TBD records the phasing and the retained definition.
Placement: this SoW keeps its TBDs in the Epistemology section, so TBD-004
follows TBD-003 there.
```old
the open guidance requirement does not decide that mechanism.
```
```new
the open guidance requirement does not decide that mechanism.
- **TBD-004** — Declared checkpoints are phased (`APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4` D4-1). In the current phase a declared checkpoint is plan guidance. The declaration still states its required act, when it is reached, its subject and its held actions. The act is recorded only when the person performs it, and no hold support is assigned. Neither the App nor a host's embedded loop holds a run or reports a workflow unsupported because a hold cannot be enforced. Hold support and enforced holds (`DEL-02-03`) are kept as the governance-phase definition, so that every workflow needing governance can be served. App-side run holds (`APP-V4-FIRST-INCREMENT-20260928-DECISION-2` D6) are closed for the current phase. This contract consumes `DEL-02-03`'s statement of the current phase and, for the governance phase, its hold-support values; it does not define them. **Owner:** the owner, when a workflow needs enforced checkpoints. **Point of need:** before any checkpoint is claimed held.
```
Grounds arc N-17 (DEL-02-01 → DEL-02-03), per node P2's hook (ARC_ANALYSIS §2.3). Design basis: WD §8 "Expected from suppliers" (DEL-02-03 row); WD header and §4.3.0 (Phase 1); R4-7, R4-8 and R5-1 (WD adopts EXEC-owned values). Decision: DECISION-4 D4-1.

#### E-0201-07 · REQ-003 · NEW
Target: DEL-02-01
Trace: DECISION-4 D4-1 (V4-WF-05's first half phased, second half in force); R8-1; WD U-33; EXEC §2.1 PH-4.
**Why:** REQ-003 says "A required checkpoint waits for its actual act". This is
the same waiting assumption as EXEC F-29, CA F-22, GUIDE G-12 and LOOP G-6.
It was not flagged for this SoW, but DECISION-4 phases it.
```old
A required checkpoint waits for its actual act, but there is no synthetic rule
```
```new
A required checkpoint's act is recorded as done only when the person actually performs it (holding the run until then is the governance-phase definition, TBD-004), but there is no synthetic rule
```

#### E-0201-08 · VER-003 · NEW
Target: DEL-02-01
Trace: as E-0201-07.
```old
Verify that each case reports only the evidenced act and any actual checkpoint hold.
```
```new
Verify that each case reports only the evidenced act and, for a checkpoint in the governance phase, any actual hold.
```

#### E-0201-09 · new AX-005 (amendment reference) · NEW · acceptance-conditional
Target: DEL-02-01
```old
Basis: Clarification, Accepted decomposition DECISION.md and Setup authority.
```
```new
Basis: Clarification, Accepted decomposition DECISION.md and Setup authority.
- **AX-005** — Revised under scope-change amendment `{AMENDMENT_ID}` (accepted snapshot `projects/chirality-app-v4/execution/_ScopeChange/{AMENDMENT_SNAPSHOT}`), applying `APP-V4-FIRST-INCREMENT-20260928-DECISION-1`, `APP-V4-FIRST-INCREMENT-20260928-DECISION-2` (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-FIRST-INCREMENT-20260928/OWNER_DECISIONS.md`) and `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4` (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-SWBPIPE-INTAKE-20260928/OWNER_DECISIONS.md`). Revised: CLM-002, CLM-003, REQ-002, REQ-003, REQ-006, VER-003 and TBD-003. Added: TBD-004 and AX-005. Removed: none.
```

---

## DEL-02-03 — Workflow execution compatibility and round-trip support

REVISION_SCOPE: Purpose (first sentence); SOW-052 traceability row; OUT-003;
CLM-002; CLM-003; REQ-002; REQ-006; AC-002; AC-007; VER-002; matrix row
REQ-002/AC-002 (evidence cell); TBD-001; TBD-002; new TBD-006; new AX-004.

EXEC F-29 also names REQ-003. REQ-003 contains no waiting clause: it concerns
faithful receipt of a performed act, which is in force in both phases. It is
left unchanged.

#### E-0203-01 · Purpose, first sentence · NEW (EXEC F-29)
Target: DEL-02-03
Trace: EXEC F-29; DECISION-4 D4-1.
```old
makes selected workflow requirements actionable in the current host, holds declared human checkpoints, and supports App/host workflow transfer and refinement.
```
```new
makes selected workflow requirements actionable in the current host, requests the human acts its declared checkpoints require and records them only when performed (holding the run at a checkpoint is the governance-phase definition, TBD-006), and supports App/host workflow transfer and refinement.
```

#### E-0203-02 · SOW-052 traceability row · NEW (EXEC F-29; ledger action A21)
Target: DEL-02-03
Trace: EXEC F-29; DECISION-4 D4-1; BASIS_AMENDMENT D-04 (SOW-052 amended).
```old
| SOW-052 | Request and wait for each declared checkpoint act despite direct-operation autonomy | OBJ-003; OBJ-005 | G3 ScopeLedger.csv SOW-052; current/original PRD.md V4-WF-05 and HOST_INTEGRATION.md V4-HI-42 |
```
```new
| SOW-052 | Request each declared checkpoint act despite direct-operation autonomy; in the current phase the checkpoint is plan guidance and the run is not held; waiting until the act is performed is the governance-phase definition | OBJ-003; OBJ-005 | ScopeLedger.csv SOW-052 as amended by `{AMENDMENT_ID}` (the G3 row holds the prior text); current PRD.md V4-WF-05 and HOST_INTEGRATION.md V4-HI-42 as amended; original PRD.md V4-WF-05 |
```

#### E-0203-03 · OUT-003 · NEW (EXEC F-29)
Target: DEL-02-03
Trace: EXEC F-29; DECISION-4 D4-1 (hold cases retained, not deleted).
```old
- **OUT-003** — Missing-tool, checkpoint-hold and source-preserving round-trip fixtures
```
```new
- **OUT-003** — Missing-tool, checkpoint-recording (with governance-phase hold cases retained) and source-preserving round-trip fixtures
```

#### E-0203-04 · CLM-002 (append) · C1 SC-02-03-4, part 1 · AMEND
Target: DEL-02-03
Trace: EXEC §9.1, §10; DECISION-4 D4-1.
**Why amended:**
- The governing checkpoint constraint and the external-channel carriage
  assurance are labeled governance phase (R8-1: R2-12 carriage assurance
  retained as governance-phase definition).
- The `DEL-05-01` clause is added to ground arc N-22 (DEL-02-03 → DEL-05-01;
  EXEC §9.1 LOOP row; ARC_ANALYSIS §2.3). R8-8 makes the host-loop hold
  governance phase, while arrival, binding and events are unchanged.

**Owner item O-28:** the `DEL-01-04` clause grounds arc X-1 (DEL-02-03 →
DEL-01-04). X-1 is inside SCC-002, but it makes DEL-01-04 `DAG pending`. The
alternative is to move that clause to REQ-006, whose exclusions extraction
does not read as inputs.
```old
supplies receipt evidence without becoming its decision actor. Source: G3 Deliverables.csv DEL-03-01, DEL-04-01/03;
```
```new
supplies receipt evidence without becoming its decision actor. `DEL-03-02` owns proposal item dispositions, item-left events and the governing checkpoint constraint (governance phase); `DEL-04-02` owns grant display states; `DEL-03-03` owns external-channel receiving, including the governance-phase carriage assurance; `DEL-05-01` supplies arrival observation, subject binding and loop events from host loops (its host-loop hold is governance phase); `DEL-01-01` supplies observed supplier facts; `DEL-01-04` (later undertaking) constructs the App act control. Source: G3 Deliverables.csv DEL-01-01, DEL-01-04, DEL-03-01, DEL-03-02, DEL-03-03, DEL-04-01/02/03, DEL-05-01;
```

#### E-0203-05 · CLM-003 (append) · C1 SC-02-03-1 · AMEND
Target: DEL-02-03
Trace: DECISION-4 D4-1; R8-2 (D6 closed for Phase 1); EXEC F-10 (R8 update), §2.1 PH-2.
**Why amended:** C1 said that "No App-side hold point is currently allocated…
deferred to SQ-02". Under DECISION-4 the current phase needs no App hold point
(EXEC F-10, R8 note), SQ-02 is answered, and D6 is closed for Phase 1 and
re-opens with the governance phase.
```old
The standalone App continues to execute through stock Codex.
```
```new
The standalone App continues to execute through stock Codex. In the current phase no App-side hold point is needed, because declared checkpoints are plan guidance (`APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4` D4-1); how the App would hold its own runs (`APP-V4-FIRST-INCREMENT-20260928-DECISION-2` D6) is closed for the current phase and re-opens with the governance phase (TBD-006).
```

#### E-0203-06 · REQ-002 · C1 SC-02-03-2 (REQ-002 part) · AMEND (EXEC F-29)
Target: DEL-02-03
Trace: EXEC F-29; DECISION-4 D4-1; EXEC §2.1 PH-1, PH-2, PH-4, PH-10.
**Why amended:** C1 kept REQ-002 and flagged narrowing it as a scope change.
DECISION-4 is that owner decision: V4-WF-05's first half is phased, not
withdrawn. REQ-002 therefore states the in-force half and keeps holding as the
retained governance-phase definition.
```old
- **REQ-002** — At a declared checkpoint, request the required human act and hold the run at that checkpoint until the person performs that act, even where the applicable operation autonomy otherwise allows direct application. Interrupted or replayed history must preserve the checkpoint's identity and actual disposition. Sources: SOW-052/SOW-053; PRD.md V4-WF-05; HOST_INTEGRATION.md V4-HI-42; EXAMINATION.md V4-EXM-14/22.
```
```new
- **REQ-002** — At a declared checkpoint, request the required human act and record it as done only when the person performs it, even where the applicable operation autonomy otherwise allows direct application. In the current phase the checkpoint is plan guidance: the person and the agents manage any pause, and neither the App nor a host's embedded loop holds or blocks the run or reports the workflow unsupported because a hold cannot be enforced. Holding the run at the checkpoint until the act is performed is the governance-phase definition, retained for workflows that need it (TBD-006). Interrupted or replayed history must preserve the checkpoint's identity and actual disposition. Sources: SOW-052/SOW-053 as amended; PRD.md V4-WF-05; HOST_INTEGRATION.md V4-HI-42; EXAMINATION.md V4-EXM-14/22; `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4` D4-1.
```

#### E-0203-07 · REQ-006 · C1 SC-02-03-4, part 2 · KEEP
Target: DEL-02-03
Trace: EXEC §9.1, §10.
```old
catalog semantics belong to `DEL-03-01`, adopted operation-policy definition to `DEL-04-01`, and act/run-record format and writer/reader construction to `DEL-04-03` (CLM-002);
```
```new
catalog semantics belong to `DEL-03-01`, proposal/outcome semantics to `DEL-03-02`, grant display definition to `DEL-04-02`, external adapter construction and carriage to `DEL-03-03`, supplier observation to `DEL-01-01`, App act control construction to `DEL-01-04`, adopted operation-policy definition to `DEL-04-01`, and act/run-record format and writer/reader construction to `DEL-04-03` (CLM-002);
```

#### E-0203-08 · AC-002 · C1 SC-02-03-2 (AC-002 part) · AMEND (EXEC F-29)
Target: DEL-02-03
Trace: EXEC F-29 ("the act is not recorded as done until evidence shows it occurred", PH-4); DECISION-4 D4-1.
**Why amended:** C1 appended hold-support reporting and "action during hold".
Under R8-1 no hold-support value is reported in the current phase, and
"action during hold" is no longer a marker. The criterion takes F-29's
Phase-1 reading.
```old
- **AC-002** — A declared checkpoint requests its named human act and remains waiting despite direct-operation autonomy, interruption or replay until evidence shows that required act actually occurred. Verify by VER-002. Sources: REQ-002; SOW-052/SOW-053.
```
```new
- **AC-002** — A declared checkpoint requests its named human act, and the act is not recorded as done — despite direct-operation autonomy, interruption or replay — until evidence shows that the required act actually occurred. In the current phase no hold is claimed or enforced; for a workflow that takes up the governance phase, the checkpoint also keeps the run waiting until that evidence. Verify by VER-002. Sources: REQ-002; SOW-052/SOW-053.
```

#### E-0203-09 · AC-007 · NEW (EXEC F-29)
Target: DEL-02-03
Trace: EXEC F-29; DECISION-4 D4-1.
```old
cover the accepted missing-tool, checkpoint-hold and source-preserving
```
```new
cover the accepted missing-tool, checkpoint-recording (and, where taken up, governance-phase hold) and source-preserving
```

#### E-0203-10 · VER-002 · NEW (EXEC F-29)
Target: DEL-02-03
Trace: EXEC F-29; DECISION-4 D4-1.
```old
- **VER-002** — Exercise checkpoint arrival under identified direct-application autonomy with no human act, then interruption/replay and later performance of the required act. Inspect request, waiting state and advancement evidence; direct permission or successful unrelated work must not release the checkpoint. Implements AC-002 using V4-WF-05, V4-HI-42 and V4-EXM-14/22.
```
```new
- **VER-002** — Exercise checkpoint arrival under identified direct-application autonomy with no human act, then interruption/replay and later performance of the required act. Inspect the request, the recorded act state and the later act evidence; direct permission, successful unrelated work or continuation of the run must not record the act as performed. Hold cases (waiting state, release only by the act) are exercised only for a workflow that takes up the governance phase. Implements AC-002 using V4-WF-05, V4-HI-42 and V4-EXM-14/22.
```

#### E-0203-11 · TBD-001, TBD-002 and new TBD-006 · C1 SC-02-03-5 (KEEP) and SC-02-03-3 (AMEND)
Target: DEL-02-03
Trace: DECISION-1 D2/D3 (TBD-001/002); DECISION-4 D4-1; R8-2; EXEC GV-3, GV-4 (TBD-006).
**Why SC-02-03-3 is amended:** C1's TBD-006 was "App-side run holds deferred to
SQ-02". SQ-02 is answered, D6 is closed for the current phase, and the open
matter is now when the governance phase is taken up. That is an owner matter
the SWBPIPE-intake receipt lists as waiting.
```old
- **TBD-001** — OI-001, reserved human acts. **Owner:** Owner with App/SWB contract owners. **Point of need:** Before operation-policy production contracts. Choose always-reserved acts by concrete operation and consequence; the global list is not fixed, while false attribution is already prohibited. DEL-04-01 carries the adopted result; it is not the deciding actor.
- **TBD-002** — OI-002, classifier routine permissions. **Owner:** Owner with App/SWB contract owners. **Point of need:** Before permission-policy implementation. Distinguish routine permissions from professional acts and settle App/host treatment; normalization selects no classifier behavior. This point of need is separate from TBD-001.
```
```new
- **TBD-001** — OI-001, reserved human acts — ruled for the first increment (App/shared contracts) by `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2: marking checked; accepting a proposal where the autonomy requires one; engineering approval; professional reliance; changing the grant or enabling external access. The host names and enforces its own list (V4-HI-30; DEP-001). Operation-specific additions remain OPEN under OI-021 (TBD-005). DEL-04-01 carries the adopted result; it is not the deciding actor.
- **TBD-002** — OI-002, classifier routine permissions — ruled by `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D3: in the App, routine tool-permission and sandbox modes (including classifier-based modes) remain the user's own Codex setting and never stand in for a reserved or professional act; hosts have no classifier permission mode in the first increment. No open part remains for the first increment.
```
```old
while the owner supplies the decision.
```
```new
while the owner supplies the decision.
- **TBD-006** — Governance phase for declared checkpoints (`APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4` D4-1). **Owner:** the owner, when a workflow needs enforced checkpoints; then App/shared owners for placement (OI-014). **Point of need:** before any App or host checkpoint hold is claimed enforced. The retained hold definitions serve that phase. App-side run holds (`APP-V4-FIRST-INCREMENT-20260928-DECISION-2` D6) re-open then, with SWBPIPE's answer to relay SQ-02 (no host-held route planned) as an input.
```

#### E-0203-12 · Matrix row OUT-001 / REQ-002 / AC-002 / VER-002, evidence cell · NEW (EXEC F-29)
Target: DEL-02-03
Trace: EXEC F-29.
```old
| OUT-001 | OBJ-003; OBJ-005 | REQ-002 | AC-002 | VER-002 | Checkpoint request/hold/history and actual act arrival under direct autonomy |
```
```new
| OUT-001 | OBJ-003; OBJ-005 | REQ-002 | AC-002 | VER-002 | Checkpoint request, recorded act state and history, and actual act arrival under direct autonomy; governance-phase hold evidence only where taken up |
```

#### E-0203-13 · new AX-004 (amendment reference) · NEW · acceptance-conditional
Target: DEL-02-03
```old
INITIALIZED is defined-contract maturity, not input satisfaction, implementation, readiness or release.
```
```new
INITIALIZED is defined-contract maturity, not input satisfaction, implementation, readiness or release.
- **AX-004** — Revised under scope-change amendment `{AMENDMENT_ID}` (accepted snapshot `projects/chirality-app-v4/execution/_ScopeChange/{AMENDMENT_SNAPSHOT}`), which also amends ScopeLedger row SOW-052. Applies `APP-V4-FIRST-INCREMENT-20260928-DECISION-1`, `APP-V4-FIRST-INCREMENT-20260928-DECISION-2` (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-FIRST-INCREMENT-20260928/OWNER_DECISIONS.md`) and `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4` (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-SWBPIPE-INTAKE-20260928/OWNER_DECISIONS.md`). Revised: the Purpose first sentence, the SOW-052 traceability row, OUT-003, CLM-002, CLM-003, REQ-002, REQ-006, AC-002, AC-007, VER-002, the REQ-002 matrix evidence cell, TBD-001 and TBD-002. Added: TBD-006 and AX-004. Removed: none.
```

---

## DEL-03-01 — Capability catalog and read-basis contract

REVISION_SCOPE: OUT-001; REQ-002; REQ-004; VER-004; TBD-001; new AX-004.

#### E-0301-01 · REQ-002, last sentence · C1 S-01-1 · KEEP
Target: DEL-03-01
Trace: DECISION-1 D2/D3; R-2; R2-1; IR1-B §5; C UNRESOLVED.
```old
Preserve the declared none/may-apply/proposal-only/reserved distinctions, with unresolved concrete assignments explicit rather than silently applying the historical blanket reserved list.
```
```new
Preserve the declared none/may-apply/proposal-only/reserved distinctions, and represent an operation without an adopted class explicitly (no policy basis) rather than silently applying the historical blanket reserved list. The first-increment App/shared reserved acts and routine-permission treatment are those adopted by `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2/D3 and carried by DEL-04-01; operation-specific additions remain OI-021 and host adoption remains DEP-001.
```

#### E-0301-02 · TBD-001 · C1 S-01-2 · KEEP
Target: DEL-03-01
Trace: DECISION-1 D2/D3 and its "Effects".
```old
- **TBD-001** — OI-001/OI-002 (P OQ-02): the owner with App/SWB contract owners must resolve concrete reserved-act and classifier policy before the affected operation-policy production contract or permission implementation. App v4 DEL-04-01 carries the adopted decision; this catalog receives it. The field obligations remain included, while unresolved assignments and their dependent conformance claims remain held.
```
```new
- **TBD-001** — OI-001/OI-002 (P OQ-02): ruled for the first increment at App/shared level by owner decision `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2 (five reserved acts) and D3 (routine tool permission is the App user's own Codex setting; no classifier mode in hosts), carried by App v4 DEL-04-01. Still open: operation-specific additions (OI-021) and host adoption and enforcement (DEP-001). The field obligations remain included; conformance claims that depend on an unadopted assignment remain held.
```

#### E-0301-03 · OUT-001, REQ-004 sentence 1, VER-004 sentence 1 · C1 S-01-3 · KEEP
Target: DEL-03-01
Trace: R-6; C §5.1. This lifts the claim's granularity: the source term (V4-HI-11) is kept. The anchor ledger row DEP-03-01-017 (SOW-167) is not changed.
```old
every read describes workspace identity, generation, model revision and canonical content hash.
```
```new
every read describes workspace identity, generation, model revision and canonical content hash (received as a canonical content identity with its identity-method designation; the algorithm stays unselected under TBD-003).
```
```old
Every read shall carry the workspace identity, generation, model revision and canonical content hash of the basis it describes.
```
```new
Every read shall carry the workspace identity, generation, model revision and canonical content hash (received as a canonical content identity with its identity-method designation; the algorithm stays unselected under TBD-003) of the basis it describes.
```
```old
Inspect each fixture read for workspace identity, generation, model revision and canonical content hash,
```
```new
Inspect each fixture read for workspace identity, generation, model revision and canonical content hash (as a canonical content identity with its identity-method designation),
```

#### E-0301-04 · REQ-004, new second sentence · C1 S-01-4 · AMEND · conditional (O-9)
Target: DEL-03-01
Trace: R-6 (V1-B D-02, BLOCKING); DEL-04-03 L-1; R2-13; R8-4 (whole-model identity); R8-3.
**Why amended:** R8-4 rules that a host's whole-model identity is received as
the identity of every subject it covers, and that the App never computes
identities. SWBPIPE supplies only a whole-model identity (SQ-03/SQ-07
answers). The scope addition states that case. **Owning decision:** a scope
addition (C1 "need an owning decision").
```old
of the basis it describes. Every later action shall cite
```
```new
of the basis it describes. Each object or row in a read result also carries a host-supplied subject content identity with its method designation, distinct from the read-level identity, for per-item basis checks, act binding and lapse; where a host supplies only a whole-model identity, that identity is received as the identity of every subject it covers, and the App never computes identities itself. Every later action shall cite
```
Note: this edit anchors on text that E-0301-03 leaves unchanged. The two
edits do not overlap.

#### E-0301-05 · REQ-002, element list · C1 S-01-5 · KEEP · conditional (O-9)
Target: DEL-03-01
Trace: R-9; R2-4; C §3 #9. R8-5 relies on it (SWBPIPE's `unsupported_method` maps to "not exposed on this surface"). **Owning decision:** a scope addition.
```old
meaningful errors; and human-act/autonomy class drawn from the adopted operation policy.
```
```new
meaningful errors; human-act/autonomy class drawn from the adopted operation policy; and host-declared exposure per consumer surface, independent of class.
```

#### E-0301-07 · CLM-002 (consumption sentence) · NEW (node P2 grounding for N-11)
Target: DEL-03-01
Trace: grounds arc N-11 (DEL-03-01 → DEL-04-03), per ARC_ANALYSIS §2.3. Design basis: C-v0.6 §6.2 rows "Human-act evidence (faithfully carried) … at least the DEL-04-03 §6.1 act field set" and "Lapse state | DEL-04-03 §7 vocabulary"; V1-B RF-03 (C1-A N-11 = C1-B N-B1). No owner decision is needed; this states an existing consumption.
```old
These are distinct contributions, not acts performed by this catalog contract.
```
```new
These are distinct contributions, not acts performed by this catalog contract. This catalog contract consumes the `DEL-04-03` act field set and lapse vocabulary that read results carry as standing (human-act evidence and lapse state).
```

#### E-0301-06 · new AX-004 (amendment reference) · NEW · acceptance-conditional
Target: DEL-03-01
```old
Sources: A V4-ARC-20; B #d2/#d4/U5; I DEP-001.
```
```new
Sources: A V4-ARC-20; B #d2/#d4/U5; I DEP-001.
- **AX-004** — Revised under scope-change amendment `{AMENDMENT_ID}` (accepted snapshot `projects/chirality-app-v4/execution/_ScopeChange/{AMENDMENT_SNAPSHOT}`), applying `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-FIRST-INCREMENT-20260928/OWNER_DECISIONS.md`) and the integration rulings R-6, R-9 and R8-4 named there. Revised: OUT-001, CLM-002, REQ-002, REQ-004, VER-004 and TBD-001. Added: AX-004. Removed: none.
```

---

## DEL-03-02 — Proposal, validation and outcome contract

REVISION_SCOPE: OUT-001; CLM-003; REQ-004; REQ-008; REQ-012; AC-009; AC-013;
TBD-001; new AX-004.

#### E-0302-01 · REQ-012 sentence 1; AC-013; TBD-001 · C1 S-02-1 · KEEP
Target: DEL-03-02
Trace: DECISION-1; R-2; IR1-B §5; P UNRESOLVED.
```old
The contract shall consume adopted operation/autonomy and human-act distinctions without assigning the unresolved global reserved list or routine-classifier policy.
```
```new
The contract shall consume adopted operation/autonomy and human-act distinctions — for the first increment the reserved acts and routine-permission treatment adopted by `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2/D3 and carried by DEL-04-01 — without assigning operation-specific additions (OI-021).
```
```old
preserves OI-001/OI-002 as unresolved at their stated points of need,
```
```new
applies the adopted `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2/D3 distinctions and preserves operation-specific additions (OI-021) and host adoption (DEP-001) as open at their points of need,
```
```old
- **TBD-001** — OI-001 retains the global always-reserved human-act list with the owner and App/SWB contract owners, before operation-policy production contracts. OI-002 retains routine-classifier permission treatment with those owners, before permission-policy implementation. DEL-04-01 receives the actual decisions;
```
```new
- **TBD-001** — OI-001 and OI-002 were ruled for the first increment's App/shared contracts by `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2 (five reserved acts) and D3 (in the App, routine tool-permission and sandbox modes are the user's own Codex setting; hosts have no classifier mode), carried by DEL-04-01. Still open: operation-specific additions under OI-021 (owner via the outside SWB session and App/shared owner, before connected-activity SoW and execution) and host adoption and enforcement under DEP-001;
```

#### E-0302-02 · CLM-003, sentence 2 · C1 S-02-2 · AMEND
Target: DEL-03-02
Trace: R-6; R2-13; P §3.2; R8-4.
**Why amended:** adds R8-4's whole-model case, as in E-0301-04.
```old
HOST V4-HI-11 describes workspace identity, generation, model revision and canonical content hash; this deliverable carries that basis
```
```new
HOST V4-HI-11 describes workspace identity, generation, model revision and canonical content hash (received as a canonical content identity with its identity-method designation, plus the subject content identities of relied-on targets, or a host's whole-model identity received as the identity of every subject it covers); this deliverable carries that basis
```

#### E-0302-03 · REQ-008 sentence 1 and AC-009 · C1 S-02-3 · KEEP · conditional (O-9)
Target: DEL-03-02
Trace: R-7 (one effect is a host obligation to be evidenced, not a recorded fact); P §7; GUIDE G-7. **Owning decision:** a protected acceptance criterion (C1 "need an owning decision").
```old
Repeated submission of the same proposal shall have only one effect.
```
```new
Repeated submission of the same proposal shall have at most one application effect per change item. This is a host obligation (CLM-002) that the contract makes testable; each submission is recorded separately with only the effects actually observed.
```
```old
yields only one application effect; unverifiable outcome remains unknown
```
```new
yields at most one application effect per change item in the observed host receipts; an observed second effect is recorded as a failed host obligation, not hidden; unverifiable outcome remains unknown
```

#### E-0302-04 · REQ-004 (append) · C1 S-02-4 · AMEND
Target: DEL-03-02
Trace: R-1; R-6; R-7; P §4.1; R8-5.
**Why amended:** R8-5 maps a host's own `withdrawn` (SWBPIPE: the person
cleared the queue) to "item left the queue", never A10 or A11. The clause
keeps App terms apart from host terms of the same name.
```old
Granted direct application remains distinct from a proposal and does not manufacture acceptance. Source: SOW-171;
```
```new
Granted direct application remains distinct from a proposal and does not manufacture acceptance. States and dispositions apply per change item. *Rejected* is only the person's rejection (A10) and *withdrawn* only the proposer's withdrawal (A11); a host refusal, including a stale one, is *refused*, not rejected, and a host's own outcome term of the same name is mapped as the host reports it, never read as A10 or A11. Source: SOW-171;
```

#### E-0302-05 · OUT-001 (append) · C1 S-02-5 · AMEND
Target: DEL-03-02
Trace: R-6; R2-12; R4-14; R5-2; P §3.1, §3.3; DECISION-4 D4-1.
**Why amended:** the governing checkpoint constraint and its carriage
assurance are the governance-phase definition (R8-1; P header).
```old
host receipt references and the old/new-value information required by host proposal views.
```
```new
host receipt references and the old/new-value information required by host proposal views; the change-item content identity; and, for a checkpoint in the governance phase, the governing checkpoint constraint with its carriage assurance.
```

#### E-0302-07 · CLM-003 (consumption sentence) · NEW (node P2 grounding for N-B3)
Target: DEL-03-02
Trace: grounds arc N-B3 (DEL-03-02 → DEL-02-01), per ARC_ANALYSIS §2.3. Design basis: P-v0.6 §13 "Expect from DEL-02-01: Workflow identity; checkpoint declarations (required act, subject class, reached-when); §4.3.7 item rule"; P §3.3, §4.3; R-9, R2-12, R2-18. Decision: DECISION-4 D4-1 (the constraint is governance phase). Guard: this names no DEL-04-03 input, so N-12 stays dropped.
```old
Sources: DELIVERABLES row DEL-03-01; HOST V4-HI-02, V4-HI-11 and V4-HI-21.
```
```new
It also consumes App v4 `DEL-02-01` workflow identity (kind, origin, source root, name, revision) for proposal origin, and its checkpoint declarations (required act, subject class, reached-when) with the item rule for an acceptance checkpoint; the governing checkpoint constraint derived from them applies only in the governance phase. Sources: DELIVERABLES rows DEL-03-01 and DEL-02-01; HOST V4-HI-02, V4-HI-11 and V4-HI-21.
```

#### E-0302-06 · new AX-004 (amendment reference) · NEW · acceptance-conditional
Target: DEL-03-02
```old
This contract does not supply a project-DAG acceptance or release/qualification decision.
```
```new
This contract does not supply a project-DAG acceptance or release/qualification decision.
- **AX-004** — Revised under scope-change amendment `{AMENDMENT_ID}` (accepted snapshot `projects/chirality-app-v4/execution/_ScopeChange/{AMENDMENT_SNAPSHOT}`), applying `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-FIRST-INCREMENT-20260928/OWNER_DECISIONS.md`) and `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4` (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-SWBPIPE-INTAKE-20260928/OWNER_DECISIONS.md`). Revised: OUT-001, CLM-003, REQ-004, REQ-008, REQ-012, AC-009, AC-013 and TBD-001. Added: AX-004. Removed: none.
```

---

## DEL-03-03 — Local external-agent receiving adapter

REVISION_SCOPE: REQ-002; REQ-003; REQ-004; AC-002; VER-003; TBD-001;
TBD-002; new AX-004.

#### E-0303-01 · TBD-001 and TBD-002 · C1 S-03-1 · KEEP
Target: DEL-03-03
Trace: DECISION-1; ADAPTER F-10.
```old
- **TBD-001** — OI-001, reserved human acts: **Owner with App/SWB contract owners**; **Before operation-policy production contracts**. Choose always-reserved acts by concrete operation and consequence. This adapter consumes the resulting adopted policy; it does not author the decision.
- **TBD-002** — OI-002, classifier routine permissions: **Owner with App/SWB contract owners**; **Before permission-policy implementation**. Distinguish routine tool permissions from professional acts and settle App/host treatment. No old drafting default is selected here.
```
```new
- **TBD-001** — OI-001, reserved human acts: ruled for the first increment's App/shared contracts by `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2; this adapter consumes the adopted list through DEL-04-01. Operation-specific additions remain under OI-021; host adoption and enforcement remain under DEP-001.
- **TBD-002** — OI-002, classifier routine permissions: ruled by `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D3: in the App, routine tool-permission and sandbox modes are the user's own Codex setting; hosts have no classifier mode.
```

#### E-0303-02 · REQ-002 sentences 3–4 and AC-002 · C1 S-03-2 · AMEND · conditional (O-9, O-10)
Target: DEL-03-03
Trace: DECISION-2 D5; R4-1; R4-13; R5-4; ADAPTER F-14, F-2, §3.3 E-2, §3.4; DECISION-5.
**Why amended:** the old REQ-002 pointed to "V4-HOST-02's
configured-model-server data limit". DECISION-5 revises that requirement
(host agents; no "in local operation" qualifier), so the text names the
revised requirement. **Owning decision:** a protected criterion (AC-002),
and the record-and-show clause rests on the R5-4 reading (item O-10).
```old
The adapter shall carry the selected local/privacy data boundary without treating enablement as permission for another data destination. Host local operation retains V4-HOST-02's configured-model-server data limit; this requirement does not silently assign that host rule to every App conversation or select a model/transport.
```
```new
Host content read over the channel may flow to the model the person selected for the App conversation, cloud included; the App gates neither enablement nor requests on that destination and adds no other destination (no App relay, telemetry or remote endpoint) (`APP-V4-FIRST-INCREMENT-20260928-DECISION-2` D5). The App records the observed model destination and shows it in the channel status as information, not as a gate. A host may restrict its own channel (DEP-001); PRD V4-HOST-02, as revised by `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-5`, governs the host's embedded agent. This requirement selects no model or transport.
```
```old
Disabled access produces an explicit disabled result and no host request;
```
```new
Disabled access produces an explicit disabled result and no App-originated host request; the host's refusal is the authoritative "off" for agent-originated requests;
```
```old
enablement supplies no additional autonomy or data-destination grant.
```
```new
enablement supplies no autonomy grant and adds no destination beyond the conversation's selected model.
```

#### E-0303-03 · REQ-003 sentence 2 · C1 S-03-3 · KEEP
Target: DEL-03-03
Trace: R-3 point 3 (INTEGRATION); P §2, §4.4; C §4.1.
```old
Direct application is permissible only within the person's grant and operative host policy; otherwise the request remains a proposal.
```
```new
Direct application is permissible only under an effective direct treatment within the person's grant and operative host policy; otherwise a direct request is *not permitted* — never silently converted — and the agent may propose instead.
```

#### E-0303-04 · REQ-003 sentence 3 and VER-003 · C1 S-03-4 · AMEND
Target: DEL-03-03
Trace: DECISION-4 D4-1; R8-1; R8-11 items 2 and 4; ADAPTER F-13 (R8 note).
**Why amended:** C1 said that each checkpoint "reports its hold support … and
records action during hold, with App-side holds UNRESOLVED{D6}". In the
current phase no hold support is reported, and D6 is closed for this phase.
The checkpoint case records the act only when it is performed.
```old
Workflow checkpoints retain their required human act.
```
```new
Workflow checkpoints retain their required human act. In the current phase a checkpoint on this channel is plan guidance: its act is recorded only when the person performs it and the App claims no hold (`APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4` D4-1); hold support and enforced holds on this channel are `DEL-02-03`'s governance-phase definition (CLM-002).
```
```old
reserved-act refusal and checkpoint wait.
```
```new
reserved-act refusal and a checkpoint case whose act is recorded only when performed, with no hold claimed (a hold case only for a workflow in the governance phase).
```

#### E-0303-07 · CLM-002 (consumption sentence) · NEW (node P2 grounding for N-27 and N-B4)
Target: DEL-03-03
Trace: grounds arcs N-27 (DEL-03-03 → DEL-02-03) and N-B4 (DEL-03-03 → DEL-01-01), per ARC_ANALYSIS §2.3. Design basis: ADAPTER-v0.4 §11 "Expect from DEL-01-01/HOSTING-BOUNDARY-v0.6 and the pin record" (supplier surfaces at 0.158.0) and "Expect from DEL-02-01 / DEL-02-03" (current-phase guidance and recording; governance phase: hold machine and hold support); W8 F-11. Decisions: DECISION-1 D4 (pin); DECISION-4 D4-1 (phasing). Guard: this sentence names no DEL-09-06 input (ARC_ANALYSIS K-11).
```old
This adapter consumes these definitions with adopted PKG-04 operation-policy distinctions;
```
```new
This adapter consumes these definitions with adopted PKG-04 operation-policy distinctions, App `DEL-01-01`'s supplier MCP/dynamic-tool surfaces and channel-status facts at the definition pin 0.158.0 (`APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D4), and App `DEL-02-03`'s checkpoint statement for the current phase and, for the governance phase, its hold machine, hold-support values and required-tool check;
```

#### E-0303-05 · REQ-004 sentence 1 · C1 S-03-5 · KEEP
Target: DEL-03-03
Trace: R-7; P §7. Aligns with S-02-3.
```old
duplicate submission's one-effect meaning,
```
```new
duplicate submission's at-most-one-effect-per-item meaning, which is a host obligation to be evidenced,
```

#### E-0303-06 · new AX-004 (amendment reference) · NEW · acceptance-conditional
Target: DEL-03-03
```old
WORKING_ITEMS owns separate setup recording after validation and independent checking.
```
```new
WORKING_ITEMS owns separate setup recording after validation and independent checking.
- **AX-004** — Revised under scope-change amendment `{AMENDMENT_ID}` (accepted snapshot `projects/chirality-app-v4/execution/_ScopeChange/{AMENDMENT_SNAPSHOT}`), applying `APP-V4-FIRST-INCREMENT-20260928-DECISION-1`, `APP-V4-FIRST-INCREMENT-20260928-DECISION-2` (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-FIRST-INCREMENT-20260928/OWNER_DECISIONS.md`), `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4` and `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-5` (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-SWBPIPE-INTAKE-20260928/OWNER_DECISIONS.md`). Revised: CLM-002, REQ-002, REQ-003, REQ-004, AC-002, VER-003, TBD-001 and TBD-002. Added: AX-004. Removed: none.
```

---

## DEL-03-04 — Host boundary and integration guide

REVISION_SCOPE: receiving-map rows "Basis", "Origin, undo and proposal
presentation", "Autonomy" and "Loop and panel" (column 4, or column 3 for
"Basis"); CLM-003; REQ-002; REQ-004; REQ-005; TBD-001; TBD-002; new AX-004.

#### E-0304-01 · REQ-004 sentence 2; TBD-001; TBD-002 · C1 S-04-1 · KEEP
Target: DEL-03-04
Trace: DECISION-1; GUIDE F-5.
```old
It shall carry each unresolved reserved-class and classifier decision at its exact owner and point of need in TBD-001/TBD-002.
```
```new
It shall carry the adopted `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2/D3 distinctions and each remaining class decision (operation-specific additions, OI-021) at its exact owner and point of need (TBD-001, TBD-002, TBD-006).
```
```old
- **TBD-001** — OI-001, Reserved human acts. Owner: **Owner with App/SWB contract owners**. Point of need: **Before operation-policy production contracts**. Choose always-reserved acts by concrete operation and consequence; global list not fixed, false attribution already prohibited. The guide carries the decision need to App v4 DEL-04-01 without deciding it. Source: I OI-001.
- **TBD-002** — OI-002, Classifier routine permissions. Owner: **Owner with App/SWB contract owners**. Point of need: **Before permission-policy implementation**. Distinguish routine tool permissions from professional acts and settle App/host treatment; no historical drafting default is adopted. Source: I OI-002.
```
```new
- **TBD-001** — OI-001, Reserved human acts — ruled for the first increment's App/shared contracts by `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2 (five reserved acts), carried by App v4 DEL-04-01. The residue is operation-specific additions under OI-021 (TBD-006) and host adoption under DEP-001. False attribution is already prohibited. Source: I OI-001; `APP-V4-FIRST-INCREMENT-20260928-DECISION-1`.
- **TBD-002** — OI-002, Classifier routine permissions — ruled by `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D3: in the App, routine tool-permission and sandbox modes are the user's own Codex setting; hosts have no classifier mode in the first increment. The residue is host adoption under DEP-001. Source: I OI-002; `APP-V4-FIRST-INCREMENT-20260928-DECISION-1`.
```

#### E-0304-02 · Receiving map, row "Basis", column 3 · C1 S-04-2 · AMEND
Target: DEL-03-04
Trace: R-6; GUIDE G-7; R8-4.
**Why amended:** adds R8-4's whole-model case.
```old
receive workspace identity, generation, model revision and canonical content hash |
```
```new
receive workspace identity, generation, model revision and canonical content hash (as a canonical content identity with its method designation) and per-subject content identities (or a host's whole-model identity received as each covered subject's identity) |
```

#### E-0304-03 · Receiving map, row "Origin, undo and proposal presentation", and REQ-002 · C1 S-04-3 · KEEP
Target: DEL-03-04
Trace: R-7; GUIDE G-7. Aligns with S-02-3.
```old
stale/refusal, unchanged targets, duplicate-one-effect and unknown-outcome expectations from Q;
```
```new
stale/refusal, unchanged targets, at-most-one-effect per item as a host obligation to be evidenced, and unknown-outcome expectations from Q;
```
```old
unchanged targets, duplicate-one-effect and truthful unknown/receipt outcomes;
```
```new
unchanged targets, at-most-one-effect per item as a host obligation to be evidenced, and truthful unknown/receipt outcomes;
```

#### E-0304-04 · Receiving map, row "Loop and panel", and REQ-005 last sentence · C1 S-04-4 · AMEND (GUIDE G-6)
Target: DEL-03-04
Trace: DECISION-2 D5; R4-1; GUIDE G-6, F-16; DECISION-4 D4-3; DECISION-5; R8-9; R8-13.
**Why amended:** C1 kept "the local-server default and local-data constraint
(V4-HOST-02)" for the host's agent. DECISION-4 D4-3 removes the default, and
DECISION-5 revises V4-HOST-02. The row and REQ-005 now state the revised
host-agent rule; App conversations still follow D5.
```old
native endpoint/key boundary, local-server default and local-data constraint, malformed-call/schema-before-domain validation
```
```new
native network and credential boundary; for the host's embedded agent, a local or cloud model the person chooses with no default (PRD V4-HOST-01) and data sent only to the selected model service and person-allowed destinations, each recorded and shown (PRD V4-HOST-02; `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4` D4-3 and `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-5`); App conversations reading host content follow `APP-V4-FIRST-INCREMENT-20260928-DECISION-2` D5; malformed-call/schema-before-domain validation
```
```old
Host local operation retains its configured-model-server-only data boundary.
```
```new
The host's embedded agent sends data only to the model service the person selected and to destinations the person has allowed, with every destination recorded and shown (PRD V4-HOST-02 as revised by `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-5`); App conversations reading host content follow `APP-V4-FIRST-INCREMENT-20260928-DECISION-2` D5.
```

#### E-0304-05 · Receiving map, row "Autonomy", column 4 · C1 S-04-5 · AMEND (GUIDE G-12)
Target: DEL-03-04
Trace: DECISION-4 D4-1; R8-1; GUIDE G-12, F-16, §2.14.
**Why amended:** C1 said that checkpoints "wait where hold support is enforced
… with App-run holds UNRESOLVED{D6}". Under DECISION-4, no hold is enforced in
the current phase, and hold support is the governance-phase definition.
```old
declared checkpoints still wait; unresolved classes stay open |
```
```new
declared checkpoints are plan guidance in the current phase — their acts are recorded only when performed and no hold is claimed — and hold only for a workflow that takes up the governance phase (`APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4` D4-1); unresolved classes stay open |
```

#### E-0304-06 · CLM-003 (append) · C1 S-04-6 · AMEND · conditional (O-13)
Target: DEL-03-04
Trace: GUIDE F-4; GUIDE header "Consumed inputs"; R8-12 item 7 (GUIDE-v0.3 pins RELAY_ANSWERS and FACTS). Pairs with C1 arcs N-B9…N-B11 (routed to node P2).
**Why amended:** GUIDE-v0.3 also consumes SWBPIPE's recorded answers (DEL-09-06
Design files), so "relay questions" becomes "relay questions and recorded
SWBPIPE answers".
```old
External SWB construction stays with the host implementation owner; shared placement remains an owner decision.
```
```new
External SWB construction stays with the host implementation owner; shared placement remains an owner decision. The guide also consumes App v4 DEL-01-01's supplier boundary (native surfaces for optional external access), DEL-09-06's relay questions and recorded SWBPIPE answers (the host-contribution column) and DEL-09-09's external trace cases, citing them without performing their acts.
```

#### E-0304-07 · new AX-004 (amendment reference) · NEW · acceptance-conditional
Target: DEL-03-04
```old
authorizes implementation, passes 30%, accepts a DAG or establishes product release.
```
```new
authorizes implementation, passes 30%, accepts a DAG or establishes product release.
- **AX-004** — Revised under scope-change amendment `{AMENDMENT_ID}` (accepted snapshot `projects/chirality-app-v4/execution/_ScopeChange/{AMENDMENT_SNAPSHOT}`), applying `APP-V4-FIRST-INCREMENT-20260928-DECISION-1`, `APP-V4-FIRST-INCREMENT-20260928-DECISION-2` (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-FIRST-INCREMENT-20260928/OWNER_DECISIONS.md`), `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4` and `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-5` (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-SWBPIPE-INTAKE-20260928/OWNER_DECISIONS.md`). Revised: the receiving-map rows "Basis", "Origin, undo and proposal presentation", "Autonomy" and "Loop and panel", CLM-003, REQ-002, REQ-004, REQ-005, TBD-001 and TBD-002. Added: AX-004. Removed: none.
```

---

## DEL-01-01 — Stock Codex hosting and supplier contract

REVISION_SCOPE: CLM-003; REQ-006; TBD-002; new AX-005. No refresh change:
DECISION-5 governs host agents only, and the App's Codex keeps the person's
configuration (HOSTING R8-13 note).

#### E-0101-01 · CLM-003 sentence 1 · C1 S-11-1 · KEEP
Target: DEL-01-01
Trace: DECISION-1 D4; HOSTING U-01.
```old
historical 0.154.0 and reported 0.157.1 are not adopted pins.
```
```new
historical 0.154.0 and reported 0.157.1 are not adopted pins. Owner decision `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D4 selected Codex 0.158.0 as the definition and generation pin for the first undertaking; it is re-examined before implementation, upgrades are deliberate, and the selection establishes no qualification (DEP-005).
```

#### E-0101-02 · TBD-002 · C1 S-11-2 · KEEP
Target: DEL-01-01
Trace: DECISION-1 D4; PIN_SPIKE; HOSTING §10, U-01, U-21.
```old
- **TBD-002** — OI-012 is OPEN with the App implementation owner, needed **before protocol generation and qualification**. No v4 supplier version has been adopted by this contract. DEP-005 remains VERSION_AND_ENVIRONMENT_TO_DEFINE; required published interfaces are needed before their respective implementation/qualification witnesses. [I, E, N]
```
```new
- **TBD-002** — OI-012: 0.158.0 selected for definition and generation by `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D4; observations recorded in `Design/PIN_SPIKE_0.158.0.md`. Remaining under OI-012, with the App implementation owner: re-examination before implementation and the pin used for qualification on an identified App candidate. DEP-005 remains VERSION_AND_ENVIRONMENT_TO_DEFINE for qualification witnesses; required published interfaces are needed before their respective implementation/qualification witnesses. [I, E, N]
```

#### E-0101-03 · REQ-006 sentence 2 · C1 S-11-3 · KEEP
Target: DEL-01-01
Trace: DECISION-1 D4.
```old
Pin selection is included work; neither historical version is selected by this contract.
```
```new
Pin selection is included work; the definition/generation pin 0.158.0 was selected by owner decision `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D4, neither historical version is selected, and the implementation/qualification pin follows re-examination.
```

#### E-0101-04 · new AX-005 (amendment reference) · NEW · acceptance-conditional
Target: DEL-01-01
```old
Preserve failures and uncertainty proportionately to their bearing on the stated criterion. [G, C, E DEP-005]
```
```new
Preserve failures and uncertainty proportionately to their bearing on the stated criterion. [G, C, E DEP-005]
- **AX-005** — Revised under scope-change amendment `{AMENDMENT_ID}` (accepted snapshot `projects/chirality-app-v4/execution/_ScopeChange/{AMENDMENT_SNAPSHOT}`), applying `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D4 (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-FIRST-INCREMENT-20260928/OWNER_DECISIONS.md`). Revised: CLM-003, REQ-006 and TBD-002. Added: AX-005. Removed: none.
```

---

## DEL-05-01 — Minimal-loop and model receiving contract

REVISION_SCOPE: Purpose (first sentence); traceability row for
SOW-015/016/017/137/138; source table (new "Decisions" row); OUT-001; OUT-002;
OUT-003; CLM-001; CLM-002; CLM-004; REQ-001; REQ-006; AC-001; AC-002;
VER-001; VER-002; TBD-003; new AX-004. REQ-007 and VER-008 are unchanged:
LOOP G-6 records that their hold-free wording needs no change under R8-1.

#### E-0501-01 · Purpose, first sentence · NEW (LOOP G-6)
Target: DEL-05-01
Trace: DECISION-4 D4-3 (no default); R8-9; LOOP G-6.
```old
Define the App/shared receiving and conformance contribution to the minimal local-first embedded host loop.
```
```new
Define the App/shared receiving and conformance contribution to the minimal embedded host loop, which runs on a local or cloud model the person chooses.
```

#### E-0501-02 · Traceability row, model and network contribution · NEW (LOOP G-6; DECISION-5)
Target: DEL-05-01
Trace: DECISION-4 D4-3; DECISION-5; BASIS_AMENDMENT D-01…D-03, D-05, D-06 (SOW-015/016/017/137/138 amended).
```old
| Local model default, person-selected cloud model with supplied key, restricted local traffic and native endpoint/key protection | SOW-015; SOW-016; SOW-017; SOW-137; SOW-138 | OUT-001; OUT-002; OUT-003 |
```
```new
| Person-chosen local or cloud model with no default (cloud by OAuth sign-in or API key), agent data sent only to the selected model service and person-allowed destinations with each destination recorded and shown, and native enforcement with key and credential protection | SOW-015; SOW-016; SOW-017; SOW-137; SOW-138 (as amended by `{AMENDMENT_ID}`) | OUT-001; OUT-002; OUT-003 |
```

#### E-0501-03 · Source table, new "Decisions" row · NEW
Target: DEL-05-01
Trace: DECISION-4; DECISION-5.
```old
| PRD | `projects/chirality-app-v4/execution/_Coordination/Acceptances/APP-V4-BASIS-20260926/original-seed/PRD.md`, V4-HOST-01/02, V4-WF-05, V4-AUT-03/05 and V4-REC-03/05 |
```
```new
| PRD | `projects/chirality-app-v4/execution/_Coordination/Acceptances/APP-V4-BASIS-20260926/original-seed/PRD.md`, V4-HOST-01/02, V4-WF-05, V4-AUT-03/05 and V4-REC-03/05 |
| Decisions | `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-SWBPIPE-INTAKE-20260928/OWNER_DECISIONS.md`: `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4` (D4-1 phased checkpoints; D4-3 model access) and `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-5` (host-agent network destinations); current `projects/chirality-app-v4/docs/PRD.md` V4-HOST-01/02 and `projects/chirality-app-v4/docs/ARCHITECTURE.md` V4-ARC-11/12 as amended by `{AMENDMENT_ID}` |
```

#### E-0501-04 · OUT-001, OUT-002, OUT-003 · NEW (LOOP G-6; DECISION-5)
Target: DEL-05-01
Trace: DECISION-4 D4-3; DECISION-5; LOOP §5.1 (NW-1…NW-16).
```old
the native-network endpoint/key boundary,
```
```new
the native-network destination and credential boundary,
```
```old
local and explicitly chosen cloud settings, and endpoint/key-boundary scenarios
```
```new
local and cloud model choices (no default; cloud by OAuth sign-in or API key), allowed, requested and disallowed destinations, and destination/credential-boundary scenarios
```
```old
local endpoint confinement, key separation
```
```new
destination confinement and recording, key and credential separation
```

#### E-0501-05 · CLM-001 · NEW (DECISION-4 D4-3; DECISION-5)
Target: DEL-05-01
Trace: LOOP NW-3…NW-6 (extended to the sign-in credential, R8-9); DECISION-5.
```old
native networking, endpoint enforcement, key custody,
```
```new
native networking, destination enforcement, key and credential custody,
```

#### E-0501-06 · CLM-002 · C1 S5-1-1, part 1 · KEEP
Target: DEL-05-01
Trace: V1-A RF-05; V1-C RF-5/AB-04; R2 X-16; LOOP O-6, §6.2, §10.1; AS Receivers and U-15. Pairs with C1 R5-1-1 (arc N-03, node P2).
```old
; and `DEL-05-02` owns the App/shared panel receiving contribution.
```
```new
; `DEL-04-02` owns the autonomy-grant display states and standing exchange, which this deliverable consumes as the grant in force carried on each dispatch; and `DEL-05-02` owns the App/shared panel receiving contribution.
```

#### E-0501-07 · CLM-004 (append) · C1 S5-1-3 · KEEP
Target: DEL-05-01
Trace: DECISION-1 D2/D3; R2-11; LOOP §9 A-5. The DECISION-5 person-only grant is carried in REQ-001 (E-0501-09), not here.
```old
success alone and evidence of one act establish none of the others. Sources: Host §1
```
```new
success alone and evidence of one act establish none of the others. For the first increment's App/shared contracts, `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2 also reserves changing the autonomy grant or enabling external access (D2(e)); D3 establishes that hosts have no classifier permission mode. Operation-specific additions remain under OI-021, and host adoption under DEP-001. Sources: `APP-V4-FIRST-INCREMENT-20260928-DECISION-1`; Host §1
```

#### E-0501-08 · REQ-006 · C1 S5-1-1 part 2 (KEEP) and S5-1-2 (AMEND)
Target: DEL-05-01
Trace: S5-1-1 as E-0501-06. S5-1-2: R1 R-5; R4-2; R5-1; IR1-C §4; DECISION-4 D4-1; R8-8 (LOOP §2.4.4 host-loop hold relabelled governance phase).
**Why S5-1-2 is amended:** C1's sentence had the host loop "realize
`DEL-02-03`'s hold machine and hold-support values". Under DECISION-4 the host
loop enforces no hold in the current phase (R8-8). It records arrivals and
acts as observation. Realizing the retained hold machine is governance
phase. The "endpoint/key enforcement" wording also changes, to match the
revised V4-HOST-02.
```old
implementing workflow execution/checkpoint behavior of `DEL-02-03`;
```
```new
implementing workflow execution/checkpoint behavior of `DEL-02-03`; defining the autonomy-grant display states or standing exchange of `DEL-04-02`;
```
```old
endpoint/key enforcement implementation,
```
```new
destination and key/credential enforcement implementation,
```
```old
This exclusion preserves this deliverable's requirements, fixtures, conformance cases and owner coordination.
```
```new
This exclusion preserves this deliverable's requirements, fixtures, conformance cases and owner coordination. Stating the receiving obligations under which a host loop evaluates reached-when and records checkpoint arrivals and acts as observation (current phase), and, for the governance phase, realizes `DEL-02-03`'s retained hold machine and hold-support values, is this deliverable's receiving work, not implementation of `DEL-02-03` (`APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4` D4-1).
```

#### E-0501-09 · REQ-001 · NEW (LOOP G-6; DECISION-4 D4-3; DECISION-5)
Target: DEL-05-01
Trace: DECISION-4 D4-3 (OAuth or API key; no default); DECISION-5 (revised V4-HOST-02 wording; the two-level allow list; the stateless MCP revision 2026-07-28 only; person-only in-work grants; the always-off list; record and show; the outside-process limit; phasing); R8-9; R8-13; LOOP G-6, NW-1…NW-16.
```old
- **REQ-001** — The receiving contract shall require a user-controlled local model server by default, permit a cloud model only upon the person's choice and supplied API key, and restrict local-operation agent data transmission and requests to the configured model server. The host native layer shall carry the loop's requests, enforce the endpoint and keep keys outside interface scripts. Sources: PRD V4-HOST-01/02; Architecture V4-ARC-11/12 and §4; SOW-015/016/017/137/138.
```
```new
- **REQ-001** — The receiving contract shall present local and cloud models as options the person chooses among, with no default: a user-controlled local model server, or a cloud model reached by OAuth sign-in or an API key. The host's agent shall send data only to the model service the person selected and to destinations the person has allowed — in advance in an allow list (by category, such as web access, MCP servers or other APIs, or by named destination) or when the agent asks during its work — and contact nothing else: no analytics, silent provider switch or background download unless the person turns it on. Only the person grants a destination; the agent never grants itself one. An MCP server is allowed only if it follows the stateless MCP revision 2026-07-28. Every destination contacted shall be recorded and shown. The host native layer shall carry the loop's requests, enforce the selected model service and allowed destinations, and keep keys and sign-in credentials outside interface scripts; an outside process that is not sandboxed is recorded with the destinations it declares, as a stated evidence limit. Organization-locked allow lists and enforced sandboxing of outside processes are a later governance phase. Sources: PRD V4-HOST-01/02 and Architecture V4-ARC-11/12 as amended by `{AMENDMENT_ID}`; `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4` D4-3; `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-5`; Architecture §4; SOW-015/016/017/137/138.
```

#### E-0501-10 · AC-001 · NEW (LOOP G-6; DECISION-5)
Target: DEL-05-01
Trace: as E-0501-09; LOOP §5.1 states (local chosen; cloud signed in; cloud key supplied; cloud no credential; unconfigured).
```old
- **AC-001** — OUT-001 and OUT-002 require local-first selection, explicit person choice plus supplied key for cloud use, and configured-server-only local traffic; OUT-003 includes allowed local, disallowed destination and cloud-choice/key-absence cases with their expected outcomes. Verification: VER-001. Sources: REQ-001 and its assigned source clauses.
```
```new
- **AC-001** — OUT-001 and OUT-002 require the person's choice between local and cloud models with no default, cloud access by OAuth sign-in or an API key, and host-agent traffic only to the selected model service and person-allowed destinations, with each destination recorded and shown. OUT-003 includes local-chosen, cloud signed-in, cloud key-supplied, no-credential and unconfigured cases, an allow-listed destination, an in-work request that the person grants and one the person declines (reported to the agent as "destination not allowed by the person"), and a disallowed-destination case, with their expected outcomes. Verification: VER-001. Sources: REQ-001 and its assigned source clauses.
```

#### E-0501-11 · AC-002 · NEW (DECISION-4 D4-3; DECISION-5)
Target: DEL-05-01
Trace: as E-0501-09.
```old
identify the host native network enforcement point and require keys to remain outside interface scripts;
```
```new
identify the host native network enforcement point for the selected model service and allowed destinations and require keys and sign-in credentials to remain outside interface scripts;
```

#### E-0501-12 · VER-001 · NEW (LOOP G-6; DECISION-5)
Target: DEL-05-01
Trace: as E-0501-09.
```old
- **VER-001** — Trace model-selection and destination cases in OUT-002/003 to PRD V4-HOST-01/02 and Architecture V4-ARC-11. Inspect the expected local/cloud choice/key outcomes and evidence separation; later host execution observations must identify configuration and observed destinations. Record missing host observations explicitly.
```
```new
- **VER-001** — Trace model-selection and destination cases in OUT-002/003 to PRD V4-HOST-01/02 and Architecture V4-ARC-11/12 as amended. Inspect the expected model-choice, credential, allow-list, in-work request and decline outcomes, the destination record and evidence separation; later host execution observations must identify configuration, the grants in force and observed destinations. Record missing host observations explicitly.
```

#### E-0501-13 · VER-002 · NEW (DECISION-4 D4-3; DECISION-5)
Target: DEL-05-01
Trace: as E-0501-09.
```old
Inspect the native-network receiving contract and endpoint/key cases against Architecture V4-ARC-12. Require evidence of the actual native routing/enforcement and script/key separation before claiming host conformance;
```
```new
Inspect the native-network receiving contract and destination/credential cases against Architecture V4-ARC-12 as amended. Require evidence of the actual native routing/enforcement, the destination record and script/credential separation before claiming host conformance;
```

#### E-0501-14 · TBD-003 (append) · C1 S5-1-4 · AMEND
Target: DEL-05-01
Trace: RELAY §3; LOOP §13; DECISION-3; R8-7 (standing *answered*); RELAY_ANSWERS SQ-29 ("None exists, and none is selected").
**Why amended:** C1 said the file was "prepared for human relay and not
delivered". The owner relayed it, and SWBPIPE answered on 2026-09-28. The
answers are recorded as answers, not commitments (DECISION-3), and host joins
are deferred.
```old
no present satisfaction is inferred beyond the recorded owner-reported building standing.
```
```new
no present satisfaction is inferred beyond the recorded owner-reported building standing. The questions for these inputs are relayed through the coordination file DEL-09-06 `Design/RELAY_QUESTIONS_SWBPIPE.md` (SQ-01, SQ-02, SQ-03, SQ-08, SQ-11, SQ-19, SQ-21, SQ-29…SQ-32); that file is a coordination route, not an input this deliverable consumes. SWBPIPE's answers, received 2026-09-28, are recorded in DEL-09-06 `Design/RELAY_ANSWERS_SWBPIPE.md` as answers about its current state, not commitments. SQ-29 asked for the model-interface basis of DEP-05-01-024; SWBPIPE has none selected, so that basis stays UNKNOWN. Host joins are deferred until the owner resumes SWBPIPE UI-SUCCESSOR (`APP-V4-SWBPIPE-INTAKE-20260928-DECISION-3`).
```

#### E-0501-15 · new AX-004 (amendment reference) · NEW · acceptance-conditional
Target: DEL-05-01
```old
accepted project DAG, 30% passage, release or fallback replacement. Source: Setup.
```
```new
accepted project DAG, 30% passage, release or fallback replacement. Source: Setup.
- **AX-004** — Revised under scope-change amendment `{AMENDMENT_ID}` (accepted snapshot `projects/chirality-app-v4/execution/_ScopeChange/{AMENDMENT_SNAPSHOT}`), which also amends ScopeLedger rows SOW-015, SOW-016, SOW-017, SOW-137 and SOW-138. Applies `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-FIRST-INCREMENT-20260928/OWNER_DECISIONS.md`), `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-3`, `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4` and `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-5` (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-SWBPIPE-INTAKE-20260928/OWNER_DECISIONS.md`). Revised: the Purpose first sentence, the model and network traceability row, the source table, OUT-001, OUT-002, OUT-003, CLM-001, CLM-002, CLM-004, REQ-001, REQ-006, AC-001, AC-002, VER-001, VER-002 and TBD-003. Added: AX-004. Removed: none.
```

---

## DEL-05-02 — Host panel and shared interaction receiving

REVISION_SCOPE: CLM-002; CLM-004; OUT-003; REQ-001; REQ-003; REQ-005;
REQ-006; AC-005; Production-method paragraph; TBD-003; TBD-004; TBD-005;
the P/OQ-11 paragraph; new AX-004.

#### E-0502-01 · TBD-004, TBD-005, REQ-003 last sentence, CLM-004 first sentence · C1 S5-2-1 · KEEP
Target: DEL-05-02
Trace: DECISION-1 D2/D3 and "Effects"; R2 and R4 "Carried to C1"; V2 §4.
```old
The owner with App/SWB contract owners decides unresolved reserved-act and classifier policy;
```
```new
The owner with App/SWB contract owners decides unresolved reserved-act and classifier policy (ruled for App/shared contracts by `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2/D3);
```
```old
It shall consume adopted policy and checkpoint distinctions without deciding OI-001/OI-002.
```
```new
It shall consume adopted policy and checkpoint distinctions — `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2/D3 as carried by DEL-04-01 — without deciding operation-specific additions (OI-021).
```
```old
- **TBD-004** — Consumed-policy issue OI-001, Reserved human acts, remains OPEN. Owner: **Owner with App/SWB contract owners**. Point of need: **Before operation-policy production contracts**. The global always-reserved list is not fixed; false attribution is already prohibited. This panel contract consumes the eventual affected adopted policy through CLM-002 and CLM-004 rather than deciding it. Source: I/OI-001.
- **TBD-005** — Consumed-policy issue OI-002, Classifier routine permissions, remains OPEN. Owner: **Owner with App/SWB contract owners**. Point of need: **Before permission-policy implementation**. Distinguish routine tool permissions from professional acts and settle App/host treatment; no classifier behavior is selected here. Source: I/OI-002.
```
```new
- **TBD-004** — OI-001 is ruled for the first increment's App/shared contracts by `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2 (five reserved acts), carried through DEL-04-01. Operation-specific additions remain under OI-021, and host naming, enforcement and adoption under DEP-001 (V4-HI-30). This panel contract consumes the adopted policy through CLM-002 and CLM-004 rather than deciding it. Source: I/OI-001; `APP-V4-FIRST-INCREMENT-20260928-DECISION-1`.
- **TBD-005** — OI-002 is ruled by `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D3: in the App, routine tool-permission and sandbox modes are the user's own Codex setting. Hosts have no classifier mode in the first increment, and the SWB default proposal mode applies. Source: I/OI-002; `APP-V4-FIRST-INCREMENT-20260928-DECISION-1`.
```

#### E-0502-02 · CLM-002 and REQ-006 · C1 S5-2-2 · KEEP
Target: DEL-05-02
Trace: PANEL §3.6, F-3; V1-C RF-4; V1-A RF-05; X-16; IR1-C §4. Pairs with C1 R5-2-1 (arc N-04, node P2).
```old
and `DEL-05-01` supplies loop messages/tools/events/checkpoints and receiving requirements.
```
```new
and `DEL-05-01` supplies loop messages/tools/events/checkpoints and receiving requirements. `DEL-04-02` supplies autonomy-grant display states and active scope.
```
```old
loop-event receiving definition to App-v4 `DEL-05-01`, each as CLM-002 states.
```
```new
loop-event receiving definition to App-v4 `DEL-05-01`; grant display and standing-exchange definition to App-v4 `DEL-04-02`, each as CLM-002 states.
```

#### E-0502-03 · CLM-002 and REQ-006 · C1 S5-2-3 · AMEND · conditional (O-12)
Target: DEL-05-02
Trace: PANEL §3.2, §3.5, F-8 (v0.6: hold-support display is governance phase only), F-10 (Phase-1 display words apply EXEC PH-6…PH-8); R4-3…R4-7; R5-1; DECISION-4 D4-1. Pairs with C1 R5-2-2 (arc N-25, node P2).
**Why amended:** C1 had DEL-02-03 supplying "hold-support values and
hold-machine meanings". In the current phase PANEL displays EXEC's Phase-1
recording meanings. Hold support and the hold machine are governance-phase
(PANEL F-8). **Owner alternative (C1):** consume these meanings only through
DEL-05-01, which adds no arc. **Sequencing:** this edit anchors on text that
E-0502-02 introduces.
```old
`DEL-04-02` supplies autonomy-grant display states and active scope.
```
```new
`DEL-04-02` supplies autonomy-grant display states and active scope. `DEL-02-03` supplies the checkpoint recording meanings the panel displays in the current phase (arrival, act recorded only when performed, act-lapsed label) and, for the governance phase, the retained hold-support values and hold-machine meanings (resume, re-hold, run end, act ordering, mixed decisions).
```
```old
grant display and standing-exchange definition to App-v4 `DEL-04-02`, each as CLM-002 states.
```
```new
grant display and standing-exchange definition to App-v4 `DEL-04-02`; workflow execution, checkpoint recording and hold-machine definition to App-v4 `DEL-02-03`, each as CLM-002 states.
```

#### E-0502-04 · P/OQ-11 paragraph · C1 S5-2-4 · KEEP
Target: DEL-05-02
Trace: V1-C RF-9; PANEL F-4. The owner wording of OQ-11 differs from that of OI-021; the register route reconciles them (C1 R5-2-4).
```old
P/OQ-11 separately leaves
```
```new
P/OQ-11 (tracked as OI-021 in `Open_Issues.csv`, owner *Owner via outside SWB session and App/shared owner*, point of need *before connected-activity SoW and execution*) separately leaves
```

#### E-0502-05 · TBD-003 · C1 S5-2-5 · AMEND
Target: DEL-05-02
Trace: PANEL F-5, F-8; R2-20 / X-17; RELAY §1 P1; R8-7; DECISION-3; DECISION-4 D4-1.
**Why amended:** RELAY was "prepared and not delivered" at C1. It is now
relayed and answered, SQ-02's constraint handling is governance-phase input,
and host joins are deferred.
```old
For this deliverable, receive the relevant panel/view and interaction evidence;
```
```new
For this deliverable, receive the relevant panel/view and interaction evidence, including a stable capture-evidence reference for each host-captured act (RELAY SQ-01), host handling of the governing checkpoint constraint (SQ-02; governance phase) and the host loop's actual behavior. The questions are relayed through the coordination file DEL-09-06 `Design/RELAY_QUESTIONS_SWBPIPE.md` (a coordination route, not an input this deliverable consumes), and SWBPIPE's answers, received 2026-09-28, are recorded in `Design/RELAY_ANSWERS_SWBPIPE.md` as answers about its current state, not commitments. Host joins are deferred until the owner resumes SWBPIPE UI-SUCCESSOR (`APP-V4-SWBPIPE-INTAKE-20260928-DECISION-3`);
```

#### E-0502-06 · "checked" wording lift · C1 S5-2-6 · KEEP
Target: DEL-05-02
Trace: R1 R-4 (an unqualified "checked" is reserved for A4). The meaning is unchanged.
```old
Their checked definitions are consumed here
```
```new
Their identified, independently compared definitions are consumed here
```
```old
when the corresponding checked interfaces and external host inputs exist
```
```new
when the corresponding identified, independently compared interfaces and external host inputs exist
```
```old
the checked workflow, catalog, proposal, standing/record and loop-event definitions
```
```new
the identified, independently compared workflow, catalog, proposal, standing/record and loop-event definitions
```
```old
using checked source contracts and identified host inputs
```
```new
using identified, independently compared source contracts and identified host inputs
```
```old
identifies the checked interfaces and external inputs used
```
```new
identifies the independently compared interfaces and external inputs used
```
```old
against the checked input definitions in CLM-002
```
```new
against the identified, independently compared input definitions in CLM-002
```

#### E-0502-07 · new AX-004 (amendment reference) · NEW · acceptance-conditional
Target: DEL-05-02
```old
Sources: O and the task brief's NO_STATUS_TOUCH boundary.
```
```new
Sources: O and the task brief's NO_STATUS_TOUCH boundary.
- **AX-004** — Revised under scope-change amendment `{AMENDMENT_ID}` (accepted snapshot `projects/chirality-app-v4/execution/_ScopeChange/{AMENDMENT_SNAPSHOT}`), applying `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-FIRST-INCREMENT-20260928/OWNER_DECISIONS.md`), `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-3` and `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4` (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-SWBPIPE-INTAKE-20260928/OWNER_DECISIONS.md`). Revised: CLM-002, CLM-004, OUT-003, REQ-001, REQ-003, REQ-005, REQ-006, AC-005, the production-method paragraph, the P/OQ-11 paragraph, TBD-003, TBD-004 and TBD-005. Added: AX-004. Removed: none.
```

---

## DEL-09-06 — Connected activity contract and workflow round trip

REVISION_SCOPE: CLM-003; CLM-005; OUT-004; REQ-003; REQ-008; AC-004;
VER-004; matrix row REQ-003/AC-004 (evidence cell); TBD-002; new TBD-003; new
AX-004.

#### E-0906-01 · TBD-002 (policy part) and CLM-005 sentence 2 · C1 S9-6-1 · KEEP
Target: DEL-09-06
Trace: DECISION-1; CA F-3 (v0.1); R4 "Carried to C1". The OI-003 part of TBD-002 is unchanged.
```old
- **TBD-002** — Preserve relevant policy choices without deciding them: OI-001 owner with App/SWB contract owners, **before operation-policy production contracts**, chooses always-reserved acts by concrete operation/consequence; OI-002 same owners, **before permission-policy implementation**, settles classifier routine-permission treatment. False attribution is already prohibited; historical defaults do not settle these choices.
```
```new
- **TBD-002** — `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2 rules OI-001 for the first increment's App/shared contracts (five reserved acts), and D3 rules OI-002 (App: the user's Codex setting; hosts: no classifier mode; SWB default proposal mode). Operation-specific reserved additions remain with the owner via the outside SWB session and the App/shared owner under OI-021, before connected-activity SoW and execution. Host adoption remains under DEP-001. False attribution is already prohibited; historical defaults do not settle the remaining choices.
```
```old
The owner with App/SWB contract owners decides the unresolved reserved-act and classifier policies (OI-001/002).
```
```new
The owner with App/SWB contract owners decides the unresolved reserved-act and classifier policies (OI-001/002; ruled for App/shared contracts by `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2/D3; operation-specific additions under OI-021).
```

#### E-0906-02 · new TBD-003 · C1 S9-6-2 · AMEND · part (a) conditional (O-10)
Target: DEL-09-06
Trace: DECISION-2 D5 (SETTLED no gate) and R4-1/R5-4 (record and show; INTEGRATION reading); DECISION-4 D4-1; R8-1; R8-2; DECISION-3; CA F-22.
**Why amended:** C1 deferred D6 to SQ-02 and made App-only checkpoints *not
enforceable* and the workflow *unsupported* on the App route. Under
DECISION-4 there is no hold and no *unsupported* for a hold reason in the
current phase, and D6 is closed for this phase. DECISION-3 has since deferred
the host joins, which bears on OUT-003.
```old
and its examination belongs to App DEL-09-09 under CLM-006 (B open rows; D decision 03; P OQ-02; H §5–7).
```
```new
and its examination belongs to App DEL-09-09 under CLM-006 (B open rows; D decision 03; P OQ-02; H §5–7).
- **TBD-003** — Later owner decisions. (a) `APP-V4-FIRST-INCREMENT-20260928-DECISION-2` D5 is settled: host content read over the external channel may reach the model the person selected, with no App gate; the App records the destination per turn and shows it. (b) Declared checkpoints are phased (`APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4` D4-1). In the current phase a checkpoint is plan guidance, its act is recorded only when the person performs it, and no App or host hold arises, nor any *unsupported* result for a hold reason. App-side run holds (D6 of the same DECISION-2) are closed for the current phase and re-open with the governance phase; SWBPIPE's SQ-02 answer (no host-held route planned) is an input to that phase. This bears on REQ-003/AC-004 (W14-04) and on AC-003's "made usable in App" (W14-09) only for a workflow in the governance phase. (c) Host joins are deferred until the owner resumes SWBPIPE UI-SUCCESSOR (`APP-V4-SWBPIPE-INTAKE-20260928-DECISION-3`); OUT-003's joined witness cannot complete before then. **Owner:** the owner. **Point of need:** (b) before any checkpoint hold is claimed enforced; (c) before the live W14 steps.
```

#### E-0906-03 · CLM-003 sentence 1 and REQ-008 · C1 S9-6-3 · KEEP
Target: DEL-09-06
Trace: CA F-2 (v0.1); CA §2.3, §4, §5, W14-08. Pairs with C1 R9-6-1…3 (eight arcs, node P2).
```old
App PKG-02 supplies workflow-making and portability, specifically App DEL-02-03 execution compatibility and transfer/adaptation behavior; App PKG-03 supplies catalog meanings/tools; App PKG-04 supplies records of actual content-bound acts; App PKG-05 supplies receiving integration.
```
```new
App PKG-02 supplies workflow-making and portability, specifically App DEL-02-03 execution compatibility and transfer/adaptation behavior, App DEL-02-01 portable declaration, identity and revision meaning, and App DEL-02-02 (later undertaking) review and registration; App PKG-03 supplies catalog meanings/tools, specifically App DEL-03-01, DEL-03-02 and DEL-03-03 catalog/read-basis, proposal/outcome and external-receiving meanings; App PKG-04 supplies records of actual content-bound acts through App DEL-04-03, adopted operation policy and act distinctions through App DEL-04-01 and grant display through App DEL-04-02; App PKG-05 supplies receiving integration; App DEL-01-01 supplies the App-side supplied-guidance and model-destination evidence.
```
```old
feature construction and focused checks belong to App PKG-02/03/04/05 owners, including App DEL-02-03, App DEL-05-01 and App DEL-05-02 (CLM-003);
```
```new
feature construction and focused checks belong to App PKG-02/03/04/05 owners, including App DEL-02-01, DEL-02-02, DEL-02-03, DEL-03-01, DEL-03-02, DEL-03-03, DEL-04-01, DEL-04-02, DEL-04-03, DEL-05-01 and DEL-05-02, and supplier observation belongs to App DEL-01-01 (CLM-003);
```

#### E-0906-04 · OUT-004 · C1 S9-6-4 · AMEND
Target: DEL-09-06
Trace: CA §7.2, §9; RELAY §4; R8-7 (standing *answered*); DECISION-3.
**Why amended:** the ladder now has an actual standing (*answered*) and a
recorded answer file.
```old
identifying what is still missing and who owns it at each point of need. Scope: SOW-240; SOW-241.
```
```new
identifying what is still missing and who owns it at each point of need. The question set is `Design/RELAY_QUESTIONS_SWBPIPE.md`, SWBPIPE's recorded answers are `Design/RELAY_ANSWERS_SWBPIPE.md`, and the account is `Design/CONNECTED_ACTIVITY_CONTRACT.md` §9. Each contribution holds exactly one standing on the ladder prepared → relayed → answered → committed → delivered → adopted → examined; the SWBPIPE answers stand at *answered*. Scope: SOW-240; SOW-241.
```

#### E-0906-05 · REQ-003, AC-004, VER-004 and matrix evidence cell · NEW (CA F-22)
Target: DEL-09-06
Trace: CA F-22; DECISION-4 D4-1; R8-1; CA W14-04 (designs both parts).
```old
A declared checkpoint waits for its required human act even under direct autonomy;
```
```new
A declared checkpoint's required human act is requested and recorded only when the person performs it, even under direct autonomy (in the current phase the checkpoint is plan guidance and no hold is exercised; a hold is exercised only for a workflow that takes up the governance phase, TBD-003);
```
```old
holds a declared checkpoint when its required human act is absent despite direct autonomy,
```
```new
never records a declared checkpoint's act as performed when the required human act is absent despite direct autonomy (holding the checkpoint only for a workflow in the governance phase),
```
```old
then the declared checkpoint hold under granted direct autonomy.
```
```new
then the declared checkpoint under granted direct autonomy, whose act is not recorded until performed (a hold is inspected only for a workflow in the governance phase).
```
```old
| Tool availability/unsupported outcome, checkpoint hold, faithful real-act record and fabrication/content-change cases |
```
```new
| Tool availability/unsupported outcome, checkpoint act recording (hold only in the governance phase), faithful real-act record and fabrication/content-change cases |
```

#### E-0906-06 · new AX-004 (amendment reference) · NEW · acceptance-conditional
Target: DEL-09-06
```old
Common meaning is not compulsory common execution (B; D J/O; A §4–5).
```
```new
Common meaning is not compulsory common execution (B; D J/O; A §4–5).
- **AX-004** — Revised under scope-change amendment `{AMENDMENT_ID}` (accepted snapshot `projects/chirality-app-v4/execution/_ScopeChange/{AMENDMENT_SNAPSHOT}`), applying `APP-V4-FIRST-INCREMENT-20260928-DECISION-1`, `APP-V4-FIRST-INCREMENT-20260928-DECISION-2` (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-FIRST-INCREMENT-20260928/OWNER_DECISIONS.md`), `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-3` and `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4` (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-SWBPIPE-INTAKE-20260928/OWNER_DECISIONS.md`). Revised: CLM-003, CLM-005, OUT-004, REQ-003, REQ-008, AC-004, VER-004, the REQ-003/AC-004 matrix evidence cell and TBD-002. Added: TBD-003 and AX-004. Removed: none.
```

---

## DEL-09-09 — External control and catalog-extension trace

REVISION_SCOPE: CLM-002; CLM-004; REQ-003; REQ-004; REQ-009; TBD-002; new
TBD-005; new AX-005.

#### E-0909-01 · TBD-002 · C1 S9-9-1 · KEEP
Target: DEL-09-09
Trace: DECISION-1; XT F-1 (v0.1); R4 "Carried to C1".
```old
- **TBD-002** — OI-001, Reserved human acts, remains OPEN with **Owner with App/SWB contract owners**, **Before operation-policy production contracts**; choose always-reserved acts by concrete operation/consequence. OI-002, Classifier routine permissions, remains OPEN with the same owner, **Before permission-policy implementation**; distinguish routine permissions from professional acts and settle App/host treatment. App DEL-04-01 carries the resulting adopted policy and is not its ruling actor. This examination does not select a global reserved list or classifier mode. [S1, S3; S8 §5; S9 OQ-02]
```
```new
- **TBD-002** — OI-001 and OI-002 are ruled for the first increment's App/shared contracts by `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2 (five reserved acts) and D3 (App: the user's Codex setting; hosts: no classifier mode). App DEL-04-01 carries the adopted decision. Operation-specific additions remain under OI-021 (TBD-003), and host adoption under DEP-001. This examination selects no reserved list or classifier mode. [S1, S3; S8 §5; S9 OQ-02]
```

#### E-0909-02 · REQ-003 · C1 S9-9-2 · KEEP
Target: DEL-09-09
Trace: R1 R-6; XT J-2. This is a wording lift; the owning decision applies only if it is contested.
```old
Preserve the original inspected workspace identity, generation, model revision and canonical content hash through the chain,
```
```new
Preserve the original inspected workspace identity, generation, model revision and canonical content identity with its identity-method designation (DEL-03-01 read basis; the algorithm stays unselected) through the chain,
```

#### E-0909-03 · REQ-004 · C1 S9-9-3 · KEEP
Target: DEL-09-09
Trace: R1 R-7; XT F-6; XC-05. Aligns REQ-004 with AC-004 and VER-004.
```old
submitting the same proposal twice has one domain effect.
```
```new
submitting the same proposal twice has one domain effect. That is a host obligation to be evidenced from domain evidence (DEP-001); where the effect is unobserved, the record states "one effect unevidenced".
```

#### E-0909-04 · CLM-002 and REQ-009 · C1 S9-9-4 · KEEP
Target: DEL-09-09
Trace: XT F-2; IN-22, IN-25, IN-29; TS-0. Pairs with C1 R9-9-1…3 (arcs, node P2). "Hold-support values" carries the governance-phase label (R8-1), consistent with DEL-02-03.
```old
`DEL-09-01` owns reusable candidate examination support.
```
```new
`DEL-09-01` owns reusable candidate examination support. `DEL-05-01` owns the App/shared embedded-loop receiving contribution used for the embedded surface of the three-channel trace; `DEL-04-02` owns grant display states; `DEL-02-03` owns the per-surface compatibility report and the hold-support values (governance phase).
```
```old
, and reusable harness construction to App `DEL-09-01`, each under CLM-002.
```
```new
, reusable harness construction to App `DEL-09-01`, embedded-loop receiving definition to App `DEL-05-01`, grant display definition to App `DEL-04-02`, and compatibility-report and hold-support definition to App `DEL-02-03`, each under CLM-002.
```

#### E-0909-05 · new TBD-005 and CLM-004 · C1 S9-9-5 · AMEND · part conditional (O-10)
Target: DEL-09-09
Trace: DECISION-2 D5; R5-4; DECISION-4 D4-1; R8-1; R8-6 (SQ-28 answered: no enablement facility; channel stays *not enabled*); DECISION-3; XT S-9, S-10, S-11, §3.3; XT F-9, F-10.
**Why amended:** D6 is replaced by the DECISION-4 phasing, and SQ-28's answer
and the host-join deferral are recorded. The D5 record-and-show clause rests
on the R5-4 reading (item O-10).
```old
Later owner resolution must be reflected before freezing any affected wider examination scope. [S3]
```
```new
Later owner resolution must be reflected before freezing any affected wider examination scope. [S3]
- **TBD-005** — Later owner decisions. `APP-V4-FIRST-INCREMENT-20260928-DECISION-2` D5 is settled: the App does not gate by model destination; the destination is recorded per turn and shown. Declared checkpoints are phased (`APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4` D4-1): XC-10's checkpoint parts are recording cases in the current phase and hold cases only in the governance phase. Every live external case needs the host's A13 enablement facility with a capture-evidence reference (SQ-28). SWBPIPE answered that it has none, so its channel stays *not enabled*, and host joins are deferred until the owner resumes SWBPIPE UI-SUCCESSOR (`APP-V4-SWBPIPE-INTAKE-20260928-DECISION-3`). **Owner:** the owner; the host owner for the enablement facility (DEP-001). **Point of need:** before the live XC cases.
```
```old
A prepared contract, component pass or received draft is not evidence of external agreement, delivery, adoption or a completed connected witness.
```
```new
A prepared contract, component pass or received draft is not evidence of external agreement, delivery, adoption or a completed connected witness. The consolidated question set is the coordination file DEL-09-06 `Design/RELAY_QUESTIONS_SWBPIPE.md`, relayed by the owner and answered 2026-09-28; SWBPIPE's answers are recorded in DEL-09-06 `Design/RELAY_ANSWERS_SWBPIPE.md` as answers about its current state, not commitments. These files are a coordination route, not an input this examination consumes: its inputs are SWBPIPE's contributions under DEP-001.
```

#### E-0909-06 · new AX-005 (amendment reference) · NEW · acceptance-conditional
Target: DEL-09-09
```old
the manager records any later authorized transition separately. [S1, S5, S7, S11]
```
```new
the manager records any later authorized transition separately. [S1, S5, S7, S11]
- **AX-005** — Revised under scope-change amendment `{AMENDMENT_ID}` (accepted snapshot `projects/chirality-app-v4/execution/_ScopeChange/{AMENDMENT_SNAPSHOT}`), applying `APP-V4-FIRST-INCREMENT-20260928-DECISION-1`, `APP-V4-FIRST-INCREMENT-20260928-DECISION-2` (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-FIRST-INCREMENT-20260928/OWNER_DECISIONS.md`), `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-3` and `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4` (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-SWBPIPE-INTAKE-20260928/OWNER_DECISIONS.md`). Revised: CLM-002, CLM-004, REQ-003, REQ-004, REQ-009 and TBD-002. Added: TBD-005 and AX-005. Removed: none.
```

---

## DEL-09-07 — Local host candidate qualification (not one of the 14; conditional O-19)

This SoW owns V4-EXM-22 and V4-EXM-23 (SOW-201, SOW-202), which the basis
amendment changes (BASIS_AMENDMENT A15, A16, D-07, D-08). C1 did not compare
it; every edit is NEW.

REVISION_SCOPE: Purpose (first paragraph); SOW-202 traceability row;
REQ-005; REQ-006; AC-005; AC-006; VER-005; VER-006; matrix row
REQ-006/AC-006 (evidence cell); new AX-004.

#### E-0907-01 · Purpose · NEW
Target: DEL-09-07
Trace: DECISION-5.
```old
human checkpoints, endpoint-only traffic and actual receipt recovery.
```
```new
human checkpoints, host-agent traffic limited to the selected model service and person-allowed destinations, and actual receipt recovery.
```

#### E-0907-02 · SOW-202 traceability row · NEW
Target: DEL-09-07
Trace: DECISION-5; BASIS_AMENDMENT D-08.
```old
| SOW-202 | Observe all host traffic during the local-model journey against its configured endpoint |
```
```new
| SOW-202 | Observe all host traffic during the local-model journey against the selected model service and the person's allowed destinations, each recorded and shown (as amended by `{AMENDMENT_ID}`) |
```

#### E-0907-03 · REQ-005 · NEW
Target: DEL-09-07
Trace: DECISION-4 D4-1; EXAMINATION V4-EXM-22 as amended (BASIS_AMENDMENT A15).
```old
and a declared workflow checkpoint shall stop the run for the person's act despite that autonomy.
```
```new
and a declared workflow checkpoint shall request the person's act and record it only when the person performs it, despite that autonomy; stopping the run at the checkpoint is examined only for a workflow that takes up the governance phase (PRD V4-WF-05 as amended; `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4` D4-1).
```

#### E-0907-04 · AC-005 · NEW
Target: DEL-09-07
Trace: as E-0907-03.
```old
and a workflow checkpoint holding for the person's act despite autonomy.
```
```new
and a workflow checkpoint whose act is requested and recorded only when the person performs it, despite autonomy (a hold is examined only for a workflow in the governance phase).
```

#### E-0907-05 · VER-005 · NEW
Target: DEL-09-07
Trace: as E-0907-03.
```old
and workflow checkpoint hold/release only by the required actual human act.
```
```new
and a workflow checkpoint whose act is recorded only on the required actual human act (and, for a workflow in the governance phase, hold/release only by that act).
```

#### E-0907-06 · REQ-006 · NEW
Target: DEL-09-07
Trace: DECISION-5; EXAMINATION V4-EXM-23 as amended (BASIS_AMENDMENT A16).
```old
V4-EXM-23 shall observe all host network traffic during V4-EXM-20 and establish that no request goes anywhere except the configured model server. Evidence shall address the actual host/native route enforcing the configured endpoint.
```
```new
V4-EXM-23 shall observe all host network traffic during V4-EXM-20 and establish four things: requests go only to the model service the person selected and to destinations the person allowed, in advance or when the agent asked during its work; a declined request reaches no destination and is reported to the agent as "destination not allowed by the person"; nothing else is contacted unless the person turned it on; and every destination contacted is recorded and shown. Evidence shall address the actual host/native route enforcing the selected model service and allowed destinations; an outside process that is not sandboxed is examined within that stated limit.
```
```old
Sources: EXM V4-EXM-23/04; PRD V4-HOST-02; ARC V4-ARC-12.
```
```new
Sources: EXM V4-EXM-23/04 and PRD V4-HOST-02 as amended by `{AMENDMENT_ID}`; ARC V4-ARC-12; `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-5`.
```

#### E-0907-07 · AC-006 · NEW
Target: DEL-09-07
Trace: as E-0907-06.
```old
- **AC-006** — All host network traffic throughout the V4-EXM-20 local-model journey is observed and shows no request to any destination other than the configured model server, with candidate-specific evidence of the actual native host endpoint boundary.
```
```new
- **AC-006** — All host network traffic throughout the V4-EXM-20 local-model journey is observed and shows requests only to the selected model service and to destinations the person allowed, with each destination contacted recorded and shown, any declined request reaching no destination, and candidate-specific evidence of the actual native host destination boundary.
```

#### E-0907-08 · VER-006 · NEW
Target: DEL-09-07
Trace: as E-0907-06.
```old
Receive and independently examine complete host-network observation for the same V4-EXM-20 candidate/run/configured endpoint and actual native enforcement evidence. Account for the observation boundary and any gaps; compare every observed destination with the configured model server.
```
```new
Receive and independently examine complete host-network observation for the same V4-EXM-20 candidate/run, its selected model service and allowed destinations, and actual native enforcement evidence. Account for the observation boundary and any gaps; compare every observed destination with the selected model service, the allow list and in-work grants in force, and the destination record.
```

#### E-0907-09 · Matrix row REQ-006 / AC-006, evidence cell · NEW
Target: DEL-09-07
Trace: as E-0907-06.
```old
| All-host traffic observation on same live journey and actual native endpoint enforcement evidence |
```
```new
| All-host traffic observation on same live journey, destination record and actual native destination-enforcement evidence |
```

#### E-0907-10 · new AX-004 (amendment reference) · NEW · acceptance-conditional
Target: DEL-09-07
```old
definition is neither product completion nor replacement. Sources: EXM §§1–2,7; COORD.
```
```new
definition is neither product completion nor replacement. Sources: EXM §§1–2,7; COORD.
- **AX-004** — Revised under scope-change amendment `{AMENDMENT_ID}` (accepted snapshot `projects/chirality-app-v4/execution/_ScopeChange/{AMENDMENT_SNAPSHOT}`), which also amends ScopeLedger rows SOW-201 and SOW-202 and EXAMINATION V4-EXM-22/23. Applies `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4` and `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-5` (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-SWBPIPE-INTAKE-20260928/OWNER_DECISIONS.md`). Revised: the Purpose paragraph, the SOW-202 traceability row, REQ-005, REQ-006, AC-005, AC-006, VER-005, VER-006 and the REQ-006/AC-006 matrix evidence cell. Added: AX-004. Removed: none.
```

---

## DEL-08-01 — Domains query, admission and freshness contract (not one of the 14; conditional O-18)

CLM-003 states the old V4-HOST-02 constraint ("no data destination other than
the configured model server"). The revised V4-HOST-02 would contradict it.
REQ-006 and VER-006 ("compatibility with V4-HOST-02", "reject inference of …
an additional data destination") stay correct under the revised requirement
and are unchanged. PKG-08 work is excluded from this undertaking. This is a
consistency edit only (item O-18).

REVISION_SCOPE: CLM-003; new AX-005.

#### E-0801-01 · CLM-003 · NEW
Target: DEL-08-01
Trace: DECISION-5 (revised V4-HOST-02; the "in local operation" qualifier dropped).
```old
The accepted local-operation constraint permits no data destination other than the configured model server. Domains must meet that constraint at its actual query/tool intersection; a compatible local/in-process arrangement may suffice, and neither a remote transport nor an inherent conflict is selected.
```
```new
The accepted host-agent destination constraint (PRD V4-HOST-02, as revised by `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-5`) permits data to go only to the model service the person selected and to destinations the person has allowed, in advance or when the agent asks. Domains must meet that constraint at its actual query/tool intersection. A local/in-process arrangement adds no destination, and a remote query service is contacted only as a destination the person has allowed. Neither a remote transport nor an inherent conflict is selected.
```

#### E-0801-02 · new AX-005 (amendment reference) · NEW · acceptance-conditional
Target: DEL-08-01
```old
This contract creates no synthetic ordering between independently evidenced acts. [B3, B5/V4-CON-05, B6/V4-HI-65, B7]
```
```new
This contract creates no synthetic ordering between independently evidenced acts. [B3, B5/V4-CON-05, B6/V4-HI-65, B7]
- **AX-005** — Revised under scope-change amendment `{AMENDMENT_ID}` (accepted snapshot `projects/chirality-app-v4/execution/_ScopeChange/{AMENDMENT_SNAPSHOT}`), applying `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-5` (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-SWBPIPE-INTAKE-20260928/OWNER_DECISIONS.md`). Revised: CLM-003. Added: AX-005. Removed: none.
```

---

## C1 disposition register (all 74 proposals)

Refreshed against the Design files at `874508f16`, R6–R8, DECISION-3/4/5 and
the SWBPIPE answers. **KEEP 45 · AMEND 29 · DROP 0.** No proposal was dropped.
Each D6-deferral item still has a real open matter behind it: when the
governance phase is taken up. It is therefore amended into that form rather
than removed. C1's flag on SC-02-03-2 ("narrowing REQ-002 … would be a scope
change on the owning route") is retired: DECISION-4 is that owner decision.

| C1 item | Deliverable | Disposition | Edit | Reason (for AMEND) |
|---|---|---|---|---|
| SC-04-01-1 | DEL-04-01 | KEEP | E-0401-01 | — |
| SC-04-01-2 | DEL-04-01 | KEEP | E-0401-02 | — |
| SC-04-01-3 | DEL-04-01 | KEEP | E-0401-03 | — |
| SC-04-01-4 | DEL-04-01 | KEEP | E-0401-04 | — |
| SC-04-01-5 | DEL-04-01 | KEEP | E-0401-05 | — |
| SC-04-01-6 | DEL-04-01 | KEEP | E-0401-06 | — |
| SC-04-01-7 | DEL-04-01 | KEEP | E-0401-07 | — |
| SC-04-01-8 | DEL-04-01 | KEEP | E-0401-08 | DECISION-4 confirms that reserved acts stand. The DECISION-5 grant is left to O-15 |
| SC-04-01-9 | DEL-04-01 | KEEP | E-0401-09 | — |
| SC-04-01-10 | DEL-04-01 | AMEND | E-0401-10 | D6 deferral → DECISION-4 phasing; reads the checkpoint-override wording for the current phase (ACT F-20) |
| SC-04-02-1 | DEL-04-02 | KEEP | E-0402-01 | — |
| SC-04-02-2 | DEL-04-02 | AMEND (cond. O-11) | E-0402-02 | "hold-support values" → checkpoint recording annotations; hold support retained for the governance phase |
| SC-04-02-3 | DEL-04-02 | AMEND (cond. O-11) | E-0402-03 | "hold machine" → recording meanings plus the governance-phase hold machine |
| SC-04-02-4 | DEL-04-02 | KEEP | E-0402-04 | — |
| SC-04-02-5 | DEL-04-02 | KEEP | E-0402-05 | — |
| SC-04-02-6 | DEL-04-02 | AMEND | E-0402-06 | D6 → phasing; no hold shown in the current phase |
| SC-04-03-1 | DEL-04-03 | AMEND | E-0403-01 | "hold-machine events" → arrival/act/lapse events (RS Phase-1 header); adds DEL-05-01 network-destination events (grounds R8-B, P2) |
| SC-04-03-2 | DEL-04-03 | KEEP | E-0403-02 | — |
| SC-04-03-3 | DEL-04-03 | AMEND (cond. O-10, O-14) | E-0403-03 | adds DECISION-5's record duty for host-agent destinations; CLM-002 aligned |
| SC-04-03-4 | DEL-04-03 | KEEP | E-0403-04 | — |
| SC-02-01-1 | DEL-02-01 | AMEND | E-0201-01 | governing checkpoint constraint labeled governance phase; DEL-03-03 worded as a **receiver**, which avoids the unevidenced arc DEL-02-01 → DEL-03-03 and grounds N-20 (P2) |
| SC-02-01-2 | DEL-02-01 | KEEP | E-0201-02 | CLM-002 citation kept in parentheses |
| SC-02-01-3 | DEL-02-01 | KEEP | E-0201-03 | — |
| SC-02-01-4 | DEL-02-01 | KEEP | E-0201-04 | — |
| SC-02-01-5 | DEL-02-01 | KEEP | E-0201-05 | — |
| SC-02-01-6 | DEL-02-01 | AMEND | E-0201-06 | "not enforceable / unsupported in App runs" is ruled out by R8-1/PH-3; the TBD records the phasing and states consumption of DEL-02-03 (grounds N-17, P2) |
| SC-02-03-1 | DEL-02-03 | AMEND | E-0203-05 | no App hold point is needed in the current phase; D6 closed for this phase |
| SC-02-03-2 | DEL-02-03 | AMEND | E-0203-06, E-0203-08 | EXEC F-29: REQ-002/AC-002 take the phased wording; C1's owner flag is retired (DECISION-4) |
| SC-02-03-3 | DEL-02-03 | AMEND | E-0203-11 | TBD-006 becomes "governance phase for checkpoints"; SQ-02 answered |
| SC-02-03-4 | DEL-02-03 | AMEND | E-0203-04, E-0203-07 | constraint and carriage assurance labeled governance phase; adds `DEL-05-01` (grounds N-22, P2); the `DEL-01-04` clause (arc X-1) is kept as owner item O-28 |
| SC-02-03-5 | DEL-02-03 | KEEP | E-0203-11 | — |
| S-01-1 | DEL-03-01 | KEEP | E-0301-01 | — |
| S-01-2 | DEL-03-01 | KEEP | E-0301-02 | — |
| S-01-3 | DEL-03-01 | KEEP | E-0301-03 | — |
| S-01-4 | DEL-03-01 | AMEND (cond. O-9) | E-0301-04 | adds R8-4 (whole-model identity as each subject's identity; App never computes) |
| S-01-5 | DEL-03-01 | KEEP (cond. O-9) | E-0301-05 | — (R8-5 now relies on it) |
| S-02-1 | DEL-03-02 | KEEP | E-0302-01 | — |
| S-02-2 | DEL-03-02 | AMEND | E-0302-02 | adds R8-4 |
| S-02-3 | DEL-03-02 | KEEP (cond. O-9) | E-0302-03 | — |
| S-02-4 | DEL-03-02 | AMEND | E-0302-04 | adds R8-5 (a host term of the same name is never A10/A11) |
| S-02-5 | DEL-03-02 | AMEND | E-0302-05 | constraint and carriage assurance scoped to the governance phase |
| S-03-1 | DEL-03-03 | KEEP | E-0303-01 | — |
| S-03-2 | DEL-03-03 | AMEND (cond. O-9, O-10) | E-0303-02 | V4-HOST-02 named "as revised by DECISION-5"; stale local-operation sentence removed |
| S-03-3 | DEL-03-03 | KEEP | E-0303-03 | — |
| S-03-4 | DEL-03-03 | AMEND | E-0303-04 (with E-0303-07) | hold-support reporting and D6 → Phase-1 recording case (ADAPTER F-13 R8 note); names DEL-02-03 as the owner of the governance-phase definition (grounds N-27, P2) |
| S-03-5 | DEL-03-03 | KEEP | E-0303-05 | — |
| S-04-1 | DEL-03-04 | KEEP | E-0304-01 | — |
| S-04-2 | DEL-03-04 | AMEND | E-0304-02 | adds R8-4 |
| S-04-3 | DEL-03-04 | KEEP | E-0304-03 | — |
| S-04-4 | DEL-03-04 | AMEND | E-0304-04 | GUIDE G-6: no local default (D4-3); revised V4-HOST-02 (DECISION-5) |
| S-04-5 | DEL-03-04 | AMEND | E-0304-05 | GUIDE G-12: checkpoints phased (D4-1) |
| S-04-6 | DEL-03-04 | AMEND (cond. O-13) | E-0304-06 | adds the recorded SWBPIPE answers (GUIDE-v0.3 pins) |
| S-11-1 | DEL-01-01 | KEEP | E-0101-01 | — |
| S-11-2 | DEL-01-01 | KEEP | E-0101-02 | — |
| S-11-3 | DEL-01-01 | KEEP | E-0101-03 | — |
| S5-1-1 | DEL-05-01 | KEEP | E-0501-06, E-0501-08 | — |
| S5-1-2 | DEL-05-01 | AMEND | E-0501-08 | the host loop records in the current phase; realizing the hold machine is governance phase (R8-8) |
| S5-1-3 | DEL-05-01 | KEEP | E-0501-07 | — |
| S5-1-4 | DEL-05-01 | AMEND | E-0501-14 | RELAY relayed and answered; SQ-29 answered (no interface selected); joins deferred |
| S5-2-1 | DEL-05-02 | KEEP | E-0502-01 | — |
| S5-2-2 | DEL-05-02 | KEEP | E-0502-02 | — |
| S5-2-3 | DEL-05-02 | AMEND (cond. O-12) | E-0502-03 | Phase-1 recording meanings; hold support and hold machine for the governance phase (PANEL F-8) |
| S5-2-4 | DEL-05-02 | KEEP | E-0502-04 | — |
| S5-2-5 | DEL-05-02 | AMEND | E-0502-05 | RELAY answered; SQ-02 is governance-phase input; joins deferred |
| S5-2-6 | DEL-05-02 | KEEP | E-0502-06 | AC-005 phrased "identifies the independently compared interfaces" to avoid "identifies the identified" |
| S9-6-1 | DEL-09-06 | KEEP | E-0906-01 | — |
| S9-6-2 | DEL-09-06 | AMEND (part (a) cond. O-10) | E-0906-02 | D6 → phasing; no *unsupported* for a hold reason; DECISION-3 join deferral added |
| S9-6-3 | DEL-09-06 | KEEP | E-0906-03 | — |
| S9-6-4 | DEL-09-06 | AMEND | E-0906-04 | standing *answered*; answers file named |
| S9-9-1 | DEL-09-09 | KEEP | E-0909-01 | — |
| S9-9-2 | DEL-09-09 | KEEP | E-0909-02 | — |
| S9-9-3 | DEL-09-09 | KEEP | E-0909-03 | — |
| S9-9-4 | DEL-09-09 | KEEP | E-0909-04 | "hold-support values (governance phase)" label only |
| S9-9-5 | DEL-09-09 | AMEND (part cond. O-10) | E-0909-05 | D6 → phasing; SQ-28 answered (no facility; *not enabled*); joins deferred |

Totals: C1-A 31 (KEEP 19, AMEND 12); C1-B 24 (KEEP 14, AMEND 10); C1-C 19
(KEEP 12, AMEND 7).

## Grounding for node P2's nine arcs, and extraction guards

Node P2 (DAG_PREP/ARC_ANALYSIS §2.3) found nine arcs that the current Design
text supports but no C1 SoW correction states. The integrator asked P1 to
draft route (a): a consumption sentence in the consumer's SoW, applied by
REVISE, which extraction can then read.

| Arc (consumer → supplier) | Grounding edit | Design basis | Decision |
|---|---|---|---|
| N-11 DEL-03-01 → DEL-04-03 | E-0301-07 (CLM-002) | C §6.2 human-act evidence and lapse-state rows | — (states an existing consumption) |
| N-17 DEL-02-01 → DEL-02-03 | E-0201-06 (TBD-004) | WD §8 DEL-02-03 row; WD §4.3.0; R4-7, R4-8, R5-1 | DECISION-4 D4-1 |
| N-20 DEL-03-03 → DEL-02-01 | E-0201-01 (CLM-002, receiver wording) | ADAPTER §11 "Expect from DEL-02-01 / DEL-02-03" | DECISION-4 D4-1 |
| N-22 DEL-02-03 → DEL-05-01 | E-0203-04 (CLM-002) | EXEC §9.1 LOOP row | DECISION-4 D4-1 (host-loop hold governance phase, R8-8) |
| N-27 DEL-03-03 → DEL-02-03 | E-0303-07 (CLM-002) and E-0303-04 (REQ-003) | ADAPTER §11; W8 F-11 | DECISION-4 D4-1 |
| N-B3 DEL-03-02 → DEL-02-01 | E-0302-07 (CLM-003) | P §13 "Expect from DEL-02-01"; §3.3, §4.3 | DECISION-4 D4-1 (constraint governance phase) |
| N-B4 DEL-03-03 → DEL-01-01 | E-0303-07 (CLM-002) | ADAPTER §11 "Expect from DEL-01-01 … pin record"; HOSTING §6.8, §8.3 | DECISION-1 D4 |
| R8-A DEL-04-02 → DEL-05-01 | E-0402-08 (CLM-002), conditional O-15 | AS §3 network-destination grants "from the host's control (LOOP §5.1.1)" | DECISION-5 |
| R8-B DEL-04-03 → DEL-05-01 | E-0403-01 (CLM-004) | RS R15 "through DEL-05-01 events" | DECISION-5 |

**Held out, as instructed:**
- No SoW text grounds **N-12** (DEL-03-02 → DEL-04-03) or **N-B8** (DEL-03-03 →
  DEL-04-03). DEL-03-02 and DEL-03-03 gain no sentence naming DEL-04-03 as
  an input. The DEL-04-03 edit (E-0403-01) names both only as suppliers to
  RS, which is the existing direction.
- **DEL-04-01** and **DEL-09-06** gain no SoW text that cites an SCC-002
  member as an input to them in the reverse direction:
  - DEL-04-01's only new naming is E-0401-02 ("supplies policy meaning
    to …"), which is supplier-side and grounds mirrors only. ACT §2.7's
    citation of LOOP §5.1.1 is not carried into any SoW.
  - DEL-09-06's new names are all its own suppliers (E-0906-03).
- **DEL-01-01** gains no text naming another deliverable (ARC_ANALYSIS K-3,
  K-4, K-5).

**Extraction guards.** Three C1 navigation pointers name DEL-09-06's relay
files inside SCC-002 member SoWs: DEL-05-01 TBD-003 (E-0501-14), DEL-05-02
TBD-003 (E-0502-05) and DEL-09-09 CLM-004 (E-0909-05). An arc from any of
them to DEL-09-06 would pull DEL-09-06 into SCC-002 (ARC_ANALYSIS E-1). Each
pointer therefore states that the file "is a coordination route, not an input
this deliverable consumes". The dependency-extract briefs for DEL-05-01,
DEL-05-02 and DEL-09-09 should carry the same guard, as P2's REGISTER_CHANGES
§2.4 does for its cautions.

Mechanical check of the result: every revised SoW still validates. A
section-by-section comparison of deliverable IDs before and after the edits
shows the new mentions are exactly the intended suppliers, receivers and
guarded pointers above.

## Later findings: EXEC F-29, CA F-22, GUIDE G-12, LOOP G-6

| Finding | Where applied | Notes |
|---|---|---|
| EXEC F-29 (DEL-02-03 REQ-002, REQ-003, AC-002; "the run waits") | E-0203-01…03, -06, -08…-10, -12 | REQ-003 unchanged (no waiting clause). F-29's suggested Phase-1 acceptance ("the act is not recorded as done until evidence shows it occurred") is used in AC-002 |
| CA F-22 (DEL-09-06 REQ-003, AC-004, VER-004) | E-0906-05 | Plus the matrix evidence cell |
| GUIDE G-12 (DEL-03-04 row 6 "checkpoints still wait") | E-0304-05 | Merged with C1 S-04-5 |
| LOOP G-6 (DEL-05-01 REQ-001, AC-001; V4-HOST-01 wording) | E-0501-01…05, -09…-13 | LOOP's proposed wording ("local and cloud are options … no default; a cloud model is reached by OAuth sign-in or an API key") is used. REQ-007/VER-008 unchanged, per G-6 |
| GUIDE G-6 (DEL-03-04 row 7) | E-0304-04 | Merged with C1 S-04-4 |
| (not flagged) DEL-02-01 REQ-003/VER-003 "waits" | E-0201-07, -08 | Same assumption; found in this refresh |
| (not flagged) DEL-09-07 V4-EXM-22/23 | E-0907-* | Follows from the EXAMINATION amendment |
| (not flagged) DEL-08-01 CLM-003 | E-0801-01 | Follows from the V4-HOST-02 revision |

Also checked and not changed: DEL-04-01 REQ-001/REQ-006/OUT-001 ("checkpoint
override"; read for the current phase by TBD-004); DEL-04-02 REQ-001 (the
display never implies a checkpoint discharged; consistent); DEL-05-01
REQ-007/VER-008 (per LOOP G-6); DEL-05-02 REQ-003; DEL-01-04 (cites V4-WF-05
for draft/registration only); DEL-01-05 and DEL-09-02 (App access modes;
DECISION-4/5 govern host agents); DEL-03-04 TBD-008 ("compatible with
V4-HOST-02" stays correct).

## Mechanical checks performed

A script in the scratch folder applied every block of this file to copies of
the 16 SoWs at `874508f16`. For each target it checked that each "old" block
occurs exactly once at the moment it is applied, in the listed order. The
tokens were replaced by placeholders (`SCA-V4-001`, a dummy snapshot name).
It then ran `tools/scope_of_work/validate_scope_of_work.py` and
`tools/scope_of_work/check_boundary_owner_resolution.py` on each revised
copy. The results are in [IMPACT_ASSESSMENT.md](IMPACT_ASSESSMENT.md)
§"Validation". These are pre-application checks of the proposal, not the
REVISE run or its `MODE=VERIFY`.
