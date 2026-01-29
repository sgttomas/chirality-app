# Agent Framework Patch Notes — 2026-01-28

This bundle updates the agent instruction set to align with the clarified operating model:

- Deliverables (working-items) progress locally through lifecycle states:
  `OPEN → INITIALIZED → IN_PROGRESS → CHECKING → ISSUED`.
- Stage gates (e.g., 30/60/90/IFC) and cross-deliverable coordination are human-managed and may be represented externally (Gantt, table, etc.).
- Dependency graphs are optional. If dependencies are not tracked, tools must not report “blocked/available” as if a complete graph exists.
- Cross-deliverable coherence checks live in a dedicated RECONCILIATION agent, invoked by humans when desired.

## Files included

- `AGENT_ORCHESTRATOR_REVISED_v3.md`
  - Records a human-confirmed coordination representation (Schedule-first | Declared deps | Full graph) and dependency tracking mode (`NOT_TRACKED` | `DECLARED` | `FULL_GRAPH`)
  - Computes blockers only when dependency tracking is enabled
  - Adds optional “Reconcile” function (spawn RECONCILIATION agent)

- `AGENT_PREPARATION_REVISED_v3.md`
  - Always creates `_DEPENDENCIES.md`, but supports `NOT_TRACKED` stub mode
  - Removes assumption that an “approved dependency graph” always exists

- `AGENT_4_DOCUMENTS_REVISED_v3.md`
  - Treats `Procedure.md` as dual-use and recursive (produce/operate)
  - Runs three-pass enrichment by default and overwrites existing drafts
  - Records unresolved conflicts in a local Conflict Table in `Guidance.md` (rulings remain human-owned)
  - Allows citations with "location TBD" and labels explicit ASSUMPTIONs

- `AGENT_RECONCILIATION.md` (new)
  - Read-only cross-deliverable coherence checks
  - Produces a reconciliation report + conflict table for human rulings

- `COORDINATION_RECORD_TEMPLATE.md`
  - Optional human-owned template for recording coordination representation and any critical declared dependencies


## v3 (2026-01-28) — Decomposition Compatibility Fixes

These changes were prompted by a real project decomposition (Canola Oil Transload Facility — Phase 1) and resolve two execution blockers:

1. **Filesystem-safe folder labels**
   - Package/deliverable folder names may require sanitization (e.g., `/` cannot appear in folder names).
   - The canonical deliverable name is still stored exactly in `_CONTEXT.md` for traceability.

2. **Objective mapping extraction when expressed as ranges**
   - Some decompositions express objective support as deliverable *ranges grouped by package*.
   - WORKING_ITEMS and 4_DOCUMENTS now use the deliverable’s package ID to associate objectives (and treat “best-effort” mappings as advisory unless the human confirms).

Additional improvement:
- ORCHESTRATOR ingestion now also extracts the decomposition’s **Reference Documents** list and high-level **Decisions Captured** when present.
