# SCA-V4-001 — Propagation plan

**Standing: accepted at checkpoint group 2 (owner DECISION-7, 2026-09-28), as
transcribed after the act** from the accepted packet revision 2:
OWNER_ITEMS.md O-3 (sha256 `2b90eb4a…98ef`) and IMPACT_ASSESSMENT.md §§6,
8–11 (sha256 `7fd523c2…348e`). Where this file and the packet differ, the
packet governs. Execution-stage readings are recorded separately in
[Decision_Log.md](Decision_Log.md), not here.

Variant `SOFTWARE`; posture `FIRST_AMENDMENT`. All 47 actions are `MODIFY`:
no `ADD`, `REMOVE`, `RECLASSIFY`, `MERGE` or `SPLIT`, so there is no
parent-closure set, no child-closure remap and no folder relocation.

## 1. Write boundary (O-3, named exactly)

- `projects/chirality-app-v4/docs/PRD.md`, `ARCHITECTURE.md`,
  `HOST_INTEGRATION.md`, `EXAMINATION.md` (BASIS_AMENDMENT Part A);
- `execution/_Decomposition/SOFTWARE_DECOMP.md`, `ScopeLedger.csv`,
  `Vocabulary_Map.csv`, `Deliverables.csv`, `Consolidated_Coverage.csv`, and
  conditionally `Packages.csv` (O-8) and `Open_Issues.csv` (O-17) — both
  conditions accepted (DECISION-7) (Part B);
- the `_CONTEXT.md` of DEL-02-03, DEL-05-01, DEL-09-07, and DEL-05-02 (O-8)
  (B7);
- the 16 `ScopeOfWork.md` files, applied only by `scope-of-work`
  MODE=REVISE, one brief per deliverable, closing with MODE=VERIFY.

Plus the scope-change's own artifacts under `execution/_ScopeChange/`.

**Application route (O-3, recommendation accepted).** The docs,
decomposition and `_CONTEXT.md` edits are applied as the scope-change
candidate poststate after K1. The 16 REVISE briefs run only after the owner
accepts group 3. Group 3 (the audited poststate) is presented at the next
owner checkpoint (K2/"checkpoint B").

## 2. Direct authoritative writes after group 2 (candidate)

| Surface | Package role | Classification | Edits |
|---|---|---|---|
| `docs/PRD.md` | accepted-basis carrier, treated as working surface | DIRECT_EDIT | A01, A02/A03, A04, A05, A06 |
| `docs/ARCHITECTURE.md` | same | DIRECT_EDIT | A11a, A11b, A08/A09, A10 |
| `docs/HOST_INTEGRATION.md` | same | DIRECT_EDIT | A12, A13, A14 |
| `docs/EXAMINATION.md` | same | DIRECT_EDIT | A15, A16 |
| `_Decomposition/SOFTWARE_DECOMP.md` | working surface | DIRECT_EDIT | D-16 (COV-121) |
| `ScopeLedger.csv` | authoritative companion register | DIRECT_EDIT (field) | D-01…D-08, `ScopeItemStatement` and `DecisionRef` |
| `Vocabulary_Map.csv` | authoritative companion register | DIRECT_EDIT (field) | D-09 |
| `Deliverables.csv` | authoritative companion register | DIRECT_EDIT (substring) | D-10a/b, D-11a–d, D-12a–c |
| `Packages.csv` | authoritative companion register | DIRECT_EDIT (substring) | D-13 (O-8) |
| `Open_Issues.csv` | authoritative companion register | DIRECT_EDIT (field) | D-14a/b (O-17); `Status` stays OPEN |
| `Consolidated_Coverage.csv` | authoritative companion register (hash-bound aliases) | RECOMPUTE | B8: 126 rows (PRD 60, HOST_INTEGRATION 31, EXAMINATION 22, ARCHITECTURE 13) take the post-amendment SHA256, git blob and line; the nine amended IDs append "amended by SCA-V4-001" to `Standing` |
| DEL-02-03 `_CONTEXT.md` | working surface (variant default write) | DIRECT_EDIT | D-10a, D-10b |
| DEL-05-01 `_CONTEXT.md` | same | DIRECT_EDIT | D-11a…D-11d, D-13 |
| DEL-05-02 `_CONTEXT.md` | same | DIRECT_EDIT | D-13 |
| DEL-09-07 `_CONTEXT.md` | same | DIRECT_EDIT | D-12a…D-12c |

## 3. Acceptance-conditional edits (applied only after group-3 acceptance)

BASIS_AMENDMENT names three tokens that are filled from the accepted
group-3 record: `{AMENDMENT_ID}` (= `SCA-V4-001`), `{AMENDMENT_SNAPSHOT}`
(the accepted snapshot folder) and `{ACCEPT_DATE}` (the date of the owner's
group-3 act). The edits that carry them:

| Edit | Target | Slot rule |
|---|---|---|
| A07 (3 pairs) | `docs/PRD.md` status paragraph, §0 source table, link definitions | fill `{AMENDMENT_ID}`, `{ACCEPT_DATE}` |
| A17a | `docs/ARCHITECTURE.md` status paragraph | same |
| A17b | `docs/HOST_INTEGRATION.md` status paragraph | same |
| A17c | `docs/EXAMINATION.md` status paragraph | same |
| D-15 | `_Decomposition/SOFTWARE_DECOMP.md`: new `## Decision Log` section before `## Checkpoint and next stage` | fill `{AMENDMENT_ID}`, `{ACCEPT_DATE}`, `{AMENDMENT_SNAPSHOT}` |

Consequence recorded in the packet: A07 and A17 change document bytes and
line numbers, so `Consolidated_Coverage.csv` (B8) is recomputed again by
the same rule after they are applied.

## 4. Deliverable `MODIFY` actions and lifecycle (IMPACT_ASSESSMENT §11)

| Deliverables | `_STATUS.md` | Consequence |
|---|---|---|
| DEL-01-01, 02-01, 02-03, 03-01, 03-02, 03-03, 03-04, 04-01, 04-02, 04-03, 05-01, 05-02, 09-06, 09-09 | IN_PROGRESS (owner DECISION-6, commit `67a2fac4b`) | REVISE admits IN_PROGRESS |
| DEL-09-07, DEL-08-01 | INITIALIZED | REVISE admits INITIALIZED |

No affected deliverable is CHECKING or ISSUED. No register row authorizes a
reopening; no `write_status.sh --amendment` path arises. No `_STATUS.md` is
written by this amendment.

`_CONTEXT.md` edits per deliverable are those of §2. DEL-05-02's
`_CONTEXT.md` changes only for D-13 (O-8).

## 5. Downstream reruns and handoffs (not executed by the scope-change)

| Package / surface | Owner | Status after the amendment | Required action |
|---|---|---|---|
| 16 `ScopeOfWork.md` (A32–A47) | `project-setup` INCREMENTAL → `scope-of-work` MODE=REVISE | pending group 3 | One brief per deliverable carrying `AMENDMENT_REF` (ID, accepted group-3 snapshot, the deliverable's action row, register hash), `REVISION_SCOPE` (its list heading in SOW_REVISIONS), `PRIOR_CONTRACT_SHA256`, `SOURCE_STATE` (IN_PROGRESS or INITIALIZED), `STATUS_POLICY=NO_STATUS_TOUCH`, and a closing MODE=VERIFY |
| Design definitions of the 14 deliverables | each Design owner | STALE_REBUILD_REQUIRED | Re-pin SoW and doc hashes; close EXEC F-29, CA F-22, GUIDE G-12/G-6/F-16, LOOP G-6, WD U-33, ACT F-20, PANEL F-9 and the "flagged for the next accepted-basis update" notes; GUIDE re-pinned last |
| `Coverage_Telemetry.json` and the post-change baseline | audit-decomp (TASK) | STALE_REBUILD_REQUIRED (already stale: COV-119, COV-120) | Post-change baseline, same seven-package scope as the pre-change baseline |
| DAG-001 | project-dag | Currency DEPARTURE on SoW application | Currency audit, then the DAG-002 candidate (checkpoint C) |
| `Dependencies.csv` registers | dependency-extract, per deliverable | Not changed by this amendment | Node P2 route |
| RELAY/SWBPIPE handoff | App manager / human | CURRENT as relayed | Carry DECISION-5 obligations at the next relay |
| Post-acceptance closure | `audit-scope-closure` | — | After incremental setup and the REVISE runs |

NO_CHANGE: `Allocation_Rationale.csv`, `Source_Coverage.csv`,
`Scope_Classification.csv`, `Source_Sections.csv`, `Objectives.csv`,
`ContextBudgetQA.csv`, `Companion_Inventory.csv`, `External_Dependencies.csv`,
`checkpoint_snapshots/GROUP*`, `_DAG/DAG-001/*`, `Dependencies.csv`,
`_DEPENDENCIES.md`, `_Coordination/HANDOFF_SWBPIPE_DOMAINS.md` and the RELAY
file.

## 6. Closure validation lane (IMPACT_ASSESSMENT §9)

Before group 3:
1. an `audit-decomp` post-change baseline over the same seven-package scope
   (PKG-01, 02, 03, 04, 05, 08, 09; 30 deliverables), compared with
   `BASELINE/coverage_summary.json`. Expected: COV-121 and the Change
   Register part of COV-127 close, and COV-119/120 close on the telemetry
   recompute;
2. after the REVISE runs: `validate_scope_of_work.py` and
   `check_boundary_owner_resolution.py` on each revised SoW, and a diff that
   confines each SoW change to its `REVISION_SCOPE`;
3. the `Consolidated_Coverage.csv` recompute;
4. an independent review of the candidate.

Pre-existing findings (COV-119, COV-120, COV-122…COV-126 and the
non-Change-Register part of COV-127) are not attributed to this amendment.

## 7. DAG impact (IMPACT_ASSESSMENT §10)

`_DAG/DAG-001/SOURCE_MANIFEST.sha256` binds the 41 `ScopeOfWork.md`,
`Dependencies.csv` and `_DEPENDENCIES.md`, the GROUP3 canonical CSVs and
`DECISION.md`, `_LATEST_ACCEPTED.md` and `_Coordination/_COORDINATION.md`. The
basis docs, the working decomposition files and `_CONTEXT.md` are not bound,
so the candidate application leaves DAG-001 current. The SoW REVISE runs
(after group 3) change up to 16 bound entries and the currency audit then
records a DEPARTURE. No SoW edit adds, removes or reverses an arc.

## 8. Checkpoint recording (O-24)

One owner act addressing both subjects is recorded in two immutable decision
snapshots, `SCA-V4-001_GROUP-1_2026-09-28` and
`SCA-V4-001_GROUP-2_2026-09-28`. The group-2 snapshot binds
`Amendment_Actions.csv` by hash.
