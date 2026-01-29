# Agent Framework Patch Notes — 2026-01-28

This bundle updates the agent instruction set to align with the clarified operating model:

- Deliverables (working-items) progress locally through lifecycle states:
  `OPEN → INITIALIZED → IN_PROGRESS → CHECKING → ISSUED`.
- Stage gates (e.g., 30/60/90/IFC) and cross-deliverable coordination are human-managed and may be represented externally (Gantt, table, etc.).
- Dependency graphs are optional. If dependencies are not tracked, tools must not report “blocked/available” as if a complete graph exists.
- Cross-deliverable coherence checks live in a dedicated RECONCILIATION agent, invoked by humans when desired.

## Files included

- `AGENT_ORCHESTRATOR_REVISED.md`
  - Records a human-confirmed coordination representation (Schedule-first | Declared deps | Full graph) and dependency tracking mode (`NOT_TRACKED` | `DECLARED` | `FULL_GRAPH`)
  - Computes blockers only when dependency tracking is enabled
  - Adds optional “Reconcile” function (spawn RECONCILIATION agent)

- `AGENT_PREPARATION_REVISED.md`
  - Always creates `_DEPENDENCIES.md`, but supports `NOT_TRACKED` stub mode
  - Removes assumption that an “approved dependency graph” always exists

- `AGENT_4_DOCUMENTS_REVISED.md`
  - Treats `Procedure.md` as dual-use and recursive (produce/operate)
  - Records unresolved local inconsistencies as a seed list in `Guidance.md` (recording does not require a ruling; resolution still requires human decision later)

- `AGENT_RECONCILIATION.md` (new)
  - Read-only cross-deliverable coherence checks
  - Produces a reconciliation report + conflict table for human rulings

- `COORDINATION_RECORD_TEMPLATE.md`
  - Optional human-owned template for recording coordination representation and any critical declared dependencies

