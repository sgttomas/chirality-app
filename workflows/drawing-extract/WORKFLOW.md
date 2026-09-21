---
name: drawing-extract
description: "Extract target-specific evidence from engineering drawings through coverage design, bounded visual extraction, deterministic QA, assembly, and recovery."
metadata:
  category: Documents and drawings
  applicability: Extract target-specific structured evidence from engineering drawing sets.
---

# Extract evidence from drawings

WORKING_ITEMS owns the source-to-result undertaking. The human selects the drawing type, extraction target, schema, review depth, and recovery or duplicate policy. TASK extracts from each bounded page or tile; deterministic tools prepare geometry, validate artifacts, and assemble results.

## Method

1. **Resolve the target before creating outputs.** Validate the drawing type and target using the registry in [CONTRACT.md](CONTRACT.md). DRAWING_SET titleblock inventory, PFD equipment headers, and P_AND_ID valve counts are implemented. ISOMETRIC and GA remain registered, unsupported targets and reject before rasterization. A separately authorized experimental target has its own bounded schema and outputs.
2. **Design coverage.** Rasterize the selected pages. Prepare header slices for PFD equipment, four corner crops plus a thumbnail for titleblocks, or overlapping read tiles with disjoint emit boxes for P&ID symbols. Record any page-specific crop overrides.
3. **Dispatch the applicable bounded workflow.** Use TASK with `drawing-extract-page`, `drawing-titleblock-page`, or `pandid-valve-symbol-instance`. Resume only with matching source, target, field selections, and applicable crop/tile configuration. Requeue work invalidated by changed geometry.
4. **Inspect coverage and evidence.** Run target validators and count reports. For PFDs, sanitize stubs, assess low-count or empty pages against the crops, recover missed blocks where indicated, and record final counts. For P&IDs, count classified symbol instances supported by isolated crops and page-global geometry; text alone cannot create counted valves.
5. **Assemble and compare.** Build target-specific tables, provenance, duplicate reports, and aggregates with tools. Preserve raw candidates when adding later review dispositions. Detailed-to-basic reconciliation and equipment-data merge run only when their required reference inputs are supplied.
6. **Return coverage and recovery state.** Name successful, empty, reference-sheet, and failed outcomes separately. Report unresolved coverage, duplicate judgments, optional merge conflicts, and the exact inputs required for a rerun.

## Resources and acceptance

Load [CONTRACT.md](CONTRACT.md) for the single target-dispatch registry, runtime parameters, output layouts, and tool paths. Load [PROCEDURE.md](PROCEDURE.md) for the selected target's phase details. Use [ACCEPTANCE.md](ACCEPTANCE.md) to validate source identity, scope-complete assembly, provenance, and honest findings.

Run folders remain mutable while their artifacts are assembled and reviewed; freeze them at closure. Later reruns create a new run folder. `_LATEST.md` is a convenience pointer and does not substitute for acceptance. Resolve tool commands against the declared tool root.
