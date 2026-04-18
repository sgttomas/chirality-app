# PLAN — Active Roadmap

This document is the active roadmap and index for planned work in the Chirality project execution system.

Detailed, implementation-oriented plans live under [`plans/`](../plans/). Historical completed-roadmap material that previously lived in this file has been moved to [`plans/PLAN_HISTORY_AND_COMPLETED_NORMALIZATION_RECORD.md`](../plans/PLAN_HISTORY_AND_COMPLETED_NORMALIZATION_RECORD.md).

---

## 1. Current Architectural Direction

The current direction is:

- **`TASK` is the canonical Type 2 shell** for new bounded workflows.
- **Profiles stay small and rare.** `DELIVERABLE_TASK` remains the main compatibility profile; any additional profile must justify shell-level behavior rather than method prose.
- **Method logic moves into skills.** Recurring bounded execution methods should be expressed as repo-native skills with the four canonical skill documents.
- **Deterministic steps move into tools.** Validation, normalization, reporting, and repeatable transforms should be implemented as deterministic helpers under `tools/`.
- **Human-facing orchestration stays in Type 1 personas.** Type 1 agents own workflow composition, scope selection, batching, consolidation, and gate-controlled human interaction.
- **The existing `ORCHESTRATOR` pipeline is grandfathered.** The working `ORCHESTRATOR` path and its retained subordinate task-family agents remain valid while the rest of the Type 2 layer is rationalized.

This document tracks that direction at a high level. Detailed migration and implementation decisions belong in the linked plan files below.

---

## 2. Active Roadmap Themes

| Theme | Status | Detailed Plan |
|-------|--------|---------------|
| Type 2 rationalization toward `TASK` + skills + tools | Active | [`plans/TYPE2_RATIONALIZATION_MASTER_PLAN.md`](../plans/TYPE2_RATIONALIZATION_MASTER_PLAN.md) |
| Audit workflow normalization | Active | [`plans/AUDIT_WORKFLOW_NORMALIZATION_PLAN.md`](../plans/AUDIT_WORKFLOW_NORMALIZATION_PLAN.md) |
| Evaluation workflow normalization | Active | [`plans/EVALUATION_WORKFLOW_NORMALIZATION_PLAN.md`](../plans/EVALUATION_WORKFLOW_NORMALIZATION_PLAN.md) |
| TOOL_POLICY Tier 1 structural validator hardening | Ready | [`plans/TOOL_POLICY_TIER1_VALIDATOR_PLAN.md`](../plans/TOOL_POLICY_TIER1_VALIDATOR_PLAN.md) |
| Drawing-extract architecture + tool hardening | Active | [`plans/DRAWING_EXTRACT_ARCHITECTURE_DESIGN.md`](../plans/DRAWING_EXTRACT_ARCHITECTURE_DESIGN.md), [`plans/DRAWING_EXTRACT_TOOL_AUDIT.md`](../plans/DRAWING_EXTRACT_TOOL_AUDIT.md) |
| Hypergraph regression-hardening fixtures | Active | [`plans/BUILD_HYPERGRAPH_DELTA_FIXTURE_PLAN.md`](../plans/BUILD_HYPERGRAPH_DELTA_FIXTURE_PLAN.md), [`plans/KTY_SUPPORTS_OBJ_LEDGER_ABSENT_FIXTURE_PLAN.md`](../plans/KTY_SUPPORTS_OBJ_LEDGER_ABSENT_FIXTURE_PLAN.md) |
| DOMAIN knowledge indexing follow-on | Active | [`plans/DOMAIN_KNOWLEDGE_INDEXING_PLAN.md`](../plans/DOMAIN_KNOWLEDGE_INDEXING_PLAN.md) |

Unsplit backlog items still on the roadmap:

- Frontend normalization of matrix/pipeline selectors to the canonical post-wrapper architecture
- R11 tool-contract enforcement beyond current TOOL_POLICY coverage
- Content-hash enforcement for `_REFERENCES.md`
- Deliverable-level lock semantics for concurrent task execution
- Staleness-propagation tooling over dependency edges and baseline SHAs

---

## 3. Plan Index

### Architecture and Governance

- [`plans/TYPE2_RATIONALIZATION_MASTER_PLAN.md`](../plans/TYPE2_RATIONALIZATION_MASTER_PLAN.md) — end-state architecture for reducing remnant standalone Type 2 agents outside the grandfathered `ORCHESTRATOR` pipeline.
- [`plans/TOOL_POLICY_TIER1_VALIDATOR_PLAN.md`](../plans/TOOL_POLICY_TIER1_VALIDATOR_PLAN.md) — deterministic validator expansion for skill tool-policy structure.

### Workflow Normalization

- [`plans/AUDIT_WORKFLOW_NORMALIZATION_PLAN.md`](../plans/AUDIT_WORKFLOW_NORMALIZATION_PLAN.md) — migrate audit execution out of standalone Type 2 agents into `TASK` skills, with a human-facing `AUDIT` manager if required.
- [`plans/EVALUATION_WORKFLOW_NORMALIZATION_PLAN.md`](../plans/EVALUATION_WORKFLOW_NORMALIZATION_PLAN.md) — preserve `EVALUATION` as Type 1 manager while migrating evaluation specialists into `TASK` skills.

### Drawing Extraction

- [`plans/DRAWING_EXTRACT_TOOL_AUDIT.md`](../plans/DRAWING_EXTRACT_TOOL_AUDIT.md) — tool-layer audit and seam analysis.
- [`plans/DRAWING_EXTRACT_ARCHITECTURE_DESIGN.md`](../plans/DRAWING_EXTRACT_ARCHITECTURE_DESIGN.md) — locked architectural design for the current drawing-extract pipeline.

### Focused Engineering Follow-ons

- [`plans/DOMAIN_KNOWLEDGE_INDEXING_PLAN.md`](../plans/DOMAIN_KNOWLEDGE_INDEXING_PLAN.md)
- [`plans/BUILD_HYPERGRAPH_DELTA_FIXTURE_PLAN.md`](../plans/BUILD_HYPERGRAPH_DELTA_FIXTURE_PLAN.md)
- [`plans/KTY_SUPPORTS_OBJ_LEDGER_ABSENT_FIXTURE_PLAN.md`](../plans/KTY_SUPPORTS_OBJ_LEDGER_ABSENT_FIXTURE_PLAN.md)

---

## 4. Historical Record

Completed migration slices, historical hardening notes, and the pre-refactor roadmap narrative are preserved in:

- [`plans/PLAN_HISTORY_AND_COMPLETED_NORMALIZATION_RECORD.md`](../plans/PLAN_HISTORY_AND_COMPLETED_NORMALIZATION_RECORD.md)

That file is the historical record for the large normalization work that previously lived in this document, including the archived C-pattern-wrapper normalization and HELPS_HUMANS governance-extension record.

---
