# PLAN — Published Roadmap

This document summarizes the published architectural direction for the Chirality public operating-system repository.

Detailed planning, unpublished implementation notes, and private execution records live outside this repository. This repository publishes the resulting architecture, agents, skills, tools, tests, documentation, and sanitized examples.

---

## 1. Current Architectural Direction

The current direction is:

- **`TASK` is the canonical Type 2 shell** for new bounded workflows.
- **Profiles stay small and rare.** `DELIVERABLE_TASK` remains the main compatibility profile; any additional profile must justify shell-level behavior rather than method prose.
- **Method logic moves into skills.** Recurring bounded execution methods should be expressed as repo-native skills with the four canonical skill documents.
- **Deterministic steps move into tools.** Validation, normalization, reporting, and repeatable transforms should be implemented as deterministic helpers under `tools/`.
- **Human-facing orchestration stays in Type 1 personas.** Type 1 agents own workflow composition, scope selection, batching, consolidation, and gate-controlled human interaction.
- **The existing `ORCHESTRATOR` pipeline is grandfathered.** The working `ORCHESTRATOR` path and its retained subordinate task-family agents remain valid while the rest of the Type 2 layer is rationalized.

This document tracks that direction at a high level. Detailed migration and implementation decisions are planned outside this public repository and published here only when they become part of the public operating-system surface.

---

## 2. Published Roadmap Themes

| Theme | Published Direction |
|-------|---------------------|
| Type 2 rationalization toward `TASK` + skills + tools | Continue migrating bounded workflows into `TASK` skills backed by deterministic tools. |
| Audit workflow normalization | Keep audit behavior governed by explicit contracts and reusable skill/tool surfaces. |
| Evaluation workflow normalization | Preserve `EVALUATION` as a Type 1 manager while keeping scoring and validation behavior testable. |
| TOOL_POLICY structural validation | Harden tool-policy validation so skill tool permissions remain explicit and machine-checkable. |
| Drawing-extract architecture + tool hardening | Maintain drawing-type-aware extraction tools with target-specific stubs and deterministic QA. |
| Hypergraph regression-hardening fixtures | Publish public-safe fixtures that protect graph construction and closure behavior. |
| DOMAIN knowledge indexing | Publish reusable indexing, atomization, and validation mechanisms without private source corpora. |

Unsplit backlog items still on the roadmap:

- Frontend normalization of matrix/pipeline selectors to the canonical post-wrapper architecture
- R11 tool-contract enforcement beyond current TOOL_POLICY coverage
- Content-hash enforcement for `_REFERENCES.md`
- Deliverable-level lock semantics for concurrent task execution
- Staleness-propagation tooling over dependency edges and baseline SHAs

---
