# Closeout account — APP-V4-FIRST-INCREMENT-20260928 (node C1)

Method: `chirality-root:bundled:workflow:bounded-reconciliation`
(Root `workflows/bounded-reconciliation/WORKFLOW.md`). Integrator: HELP_HUMAN.

The per-deliverable comparisons are in the three closeout records:

| Record | Deliverables | Candidate compared |
|---|---|---|
| [C1-A.md](C1-A.md) | DEL-04-01, 04-02, 04-03, 02-01, 02-03 | `d3cebd1cc` |
| [C1-B.md](C1-B.md) | DEL-03-01, 03-02, 03-03, 03-04, 01-01 | `c7f5513db` |
| [C1-C.md](C1-C.md) | DEL-05-01, 05-02, 09-06, 09-09 | `816c917f0` |

The later R6 and R7 edits changed no ScopeOfWork, register or lifecycle file.
R6-1 amends hold-support classification, and readers should apply it to the
records' R5-1 citations. R7-3 settles the derivation of held actions for A5
and kind (a) checkpoints. V5 checked R6 and V6 checks R7, each against the
candidate it names.

## Boundary of this closeout

DAG-001's `SOURCE_MANIFEST.sha256` binds every `ScopeOfWork.md`,
`Dependencies.csv` and `_DEPENDENCIES.md`. Editing any of them would move
DAG-001 currency. New register arcs would change the accepted graph and need a
`project-dag` departure. This closeout therefore **applies no change** to
those files, or to `_STATUS.md`, `_CONTEXT.md` or `_REFERENCES.md`. Each
warranted change is recorded as a precise proposal in C1-A/B/C, for a
successor route.

Documents this closeout did change:

- the SWBPIPE handoff pointer (`_Coordination/HANDOFF_SWBPIPE_DOMAINS.md`),
  with canonical act terms and the corrected 30% standing;
- MEMORY run rows (node M1);
- this run's receipt.

**D0 result:** both DAG-001 manifests pass at the final candidate. No bound
file changed.

## Commitment ↔ result, in summary

All 14 in-scope deliverables have version-identified 60%-level definitions in
their `Design/` folders. No OUT item is unaddressed.

| Deliverable | OUT developed / partial | Main reasons for partial |
|---|---|---|
| DEL-04-01 | 2 / 1 | Consequence vocabulary; OI-021; representation placement |
| DEL-04-02 | 3 / 0 | — |
| DEL-04-03 | 3 / 1 | Serialization and record location |
| DEL-02-01 | 3 / 1 | Wire schemas; harness-capability naming |
| DEL-02-03 | 2 / 1 | App-side hold unallocated (D6; U-E23) |
| DEL-03-01 | 2 / 1 | Responsibility map *unagreed* (OI-003) |
| DEL-03-02 | 3 / 0 | — |
| DEL-03-03 | 2 / 1 | MCP vs CLI (TBD-007); native mapping |
| DEL-03-04 | 1 / 2 | Rows 8 and 10 outside D1; VER-007 checker not run |
| DEL-01-01 | 1 / 3 | Implementation, qualification and live seam work (OUT-002/003/004) |
| DEL-05-01 | 3 / 1 | Model-interface supplier UNKNOWN (DEP-05-01-024) |
| DEL-05-02 | 2 / 2 | Host panel implementation (OI-013/014); human acts for positive cases |
| DEL-09-06 | 0 / 4 | OI-021; joined witness needs host candidate, DEL-02-02, DEL-09-01, D6 |
| DEL-09-09 | 0 / 3 | Live witness inputs; OI-003 ruling |

"Partial" means that a definition exists and the remainder needs an owner
decision, a host input, implementation, qualification or a witness. None of it
is hidden. Each item is `UNRESOLVED` with an owner and a point of need in its
Design file.

## Proposed changes, for a successor route (none applied)

| Kind | Count | Examples |
|---|---|---|
| ScopeOfWork corrections | about 74 (C1-A 31, C1-B 24, C1-C 19) | Pointers from OI-001/002 "open" to DECISION-1; D4/D5/D6 pointers; wording lifts (canonical content identity with method designation; one effect as a host obligation to be evidenced; "host checks passed" vs A4). Gaps: DEL-02-03 REQ-002 App hold (D6), and a new DEL-09-06 TBD (D6). **Need an owning decision:** DEL-03-01 scope additions (subject content identity, per-surface exposure); DEL-03-02/03-03 protected-criteria wording (one effect; data destination) |
| Register mirror rows | about 76 (C1-A 27, C1-B 33, C1-C 16) | Missing supplier-side DOWNSTREAM rows; package-row retargeting such as DEP-03-01-022 and DEP-04-03-012; TBD/PENDING normalization |
| New arcs | **40 distinct** | Recomputed SCCs: no proposed arc changes SCC membership. About 25 lie inside SCC-002 (candidate layer). About 15 would enter the admitted layer (e.g. into DEL-01-01, and from DEL-09-06 and DEL-03-04). Any new arc needs a DAG-002 departure. One is disputed: C1-A N-12, DEL-03-02 → DEL-04-03, which C1-B does not support. Three were considered and **not** proposed because they would enlarge or create SCCs: DEL-09-09 → DEL-09-06, DEL-09-09 → DEL-03-04, DEL-09-06 → DEL-09-09 |

**Lifecycle.** All 14 deliverables are INITIALIZED. For each, IN_PROGRESS would
now be the truthful state (SPEC: INITIALIZED → IN_PROGRESS by the Human or
WORKING_ITEMS). This closeout does not change it.

## Consequences routed

- **To the owner** (next steering):
  - relay the SWBPIPE questions;
  - D6 follow-up on App-side held actions (EXEC U-E23);
  - capture-after-arrival vs counting prior acts, and its repeat-grant cost
    (U-E4);
  - successor route for the proposed SoW/register changes and a DAG-002
    departure;
  - lifecycle recording;
  - custody of the shared fixture FX-PIPE-01;
  - DEL-01-05 matters: the Codex fresh-home plugin fetch (L-4) and the
    supplier's `[experimental]` labels.
- **Review residuals:** V6 left six MINOR wording items (m-1, m-3 to m-7:
  GUIDE comparison note and M8.1, RELAY sub-question count, EXEC SQ-02
  citations, the WD-EX E8 A5 clause, and a malformed held-actions edge case).
  None changes a value or the relay. They go to the next in-place pass on
  these files.
- **Task Management:** no intake. Every concern has an identified home: an
  owner decision, the successor dependency/DAG route, a SWBPIPE relay
  question, or a named deliverable's `UNRESOLVED` row.
