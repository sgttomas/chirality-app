---
name: research-orchestration
description: Coordinate bounded research streams, independent verification, recoverable evidence, and synthesis.
---

# research-orchestration

WORKING_ITEMS investigates a question through bounded research streams, independent verification, and synthesis. It owns stream allocation, retries, fan-in, human decision routing, and any shared pointer.
It may consult the wider source-qualified skill/workflow catalogs deliberately
when the research route is unclear, recording origins and collisions without
silently replacing an already selected method. Catalog visibility and workflow
metadata never grant tools or execution permissions.

## Method

1. Freeze the question, accepted domain basis, retrieval snapshot, and expected coverage. Use [the brief fields](resources/brief.md) and [accepted-source contract](resources/contract.md).
2. Scout freshness. Route a narrow exact lookup to a direct tool call. For a
   broader inquiry, discover the effective `researcher` skill descriptor and
   assign it to TASK in the ordered `methods` field as
   `[{kind: "skill", name: "researcher", source: <descriptor.source>, sourceRootId: <descriptor.sourceRootId>}]`.
   Preserve that selected source-qualified identity and treat inherited anchors
   as claims to verify.
3. Allocate a distinct `OUTPUT_DIR` for each stream. Each child writes its own packet and query log with `--no-update-latest`. Shared synthesis and pointer writes have one owner.
4. Validate returned packets and independently re-verify load-bearing claims before they enter authority at `R3+`. Record disagreements in `Conflicts.csv` with both sources.
5. Recover failed streams individually, retaining completed packets. Resume a failed stream only when the host exposes a real resume facility; otherwise start a new bounded attempt from the preserved evidence. Record attempt parentage and never claim a resume that did not execute.
6. Synthesize the validated evidence into an immutable aggregate packet. State coverage gaps and route the decisions the research reframes to the human. Update an authorized pointer only after finalization.

Use [the detailed inquiry method](resources/method.md) for question classification and source interpretation. Load [checks](resources/checks.md) at fan-in and [tool behavior](resources/tools.md) when invoking retrieval operations.

## Controls and results

`MAX_RETRIES` defaults to 2 and permits 0–3 additional attempts per failed stream. `ANCHOR_POLICY` is LIGHT by default or NONE when selected. `CRITIC_REQUIRED` defaults to true; regardless of that choice, each load-bearing claim requires independent live verification before `R3+`. `FRESHNESS_GATE` defaults to WARN: report stale indexes and their limits; refresh is a separately authorized undertaking.

Every planned stream has a terminal status: COMPLETED, RETRIED-COMPLETED, FAILED-WITH-PARTIAL, or FAILED-NO-OUTPUT. Preserve partial packets. Missing streams produce explicit coverage gaps and a READY_WITH_COVERAGE_GAPS aggregate verdict, never a complete-coverage claim.
