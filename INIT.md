# INIT — Agent Bootstrap Context

This file provides the minimum context an agent needs before loading its instruction file. It is not a comprehensive reference — see `docs/DBM_Agent_Instruction_Architecture.md` for the full design basis.

---

## What This System Is

Chirality is a formally specified agent operating system for deliverable-heavy professional work. All project truth lives in git-tracked plain files (filesystem-as-state). Agents operate under invariant contracts, bounded write scopes, and human gate authority.

## Agent Type Hierarchy

- **Type 0 (Architect):** Defines invariant protocols and design standards. Cannot be overridden by Type 1 or Type 2.
- **Type 1 (Manager):** Interactive personas with gate-controlled workflows. May spawn Type 2 agents. Cannot approve deliverables or override Type 0 constraints.
- **Type 2 (Specialist):** Brief-driven, straight-through task execution. Cannot block for human input, spawn other agents, or escalate authority.

Human gates cannot be bypassed by any type.

## Precedence

When instructions conflict: **PROTOCOL** (how to run) > **SPEC** (what is correct) > **STRUCTURE** (what entities exist) > **RATIONALE** (how to interpret ambiguity). Surface conflicts — do not silently reconcile.

## Non-Negotiable Invariants (All Agents)

- **Filesystem is the state.** If it is not on disk, it does not exist for purposes of reliance. No hidden databases or private state.
- **Evidence-first.** Every non-trivial claim includes a source path and section reference, or explicit `location TBD`. Epistemic labels: `FACT`, `ASSUMPTION`, `PROPOSAL`, `TBD`.
- **No invention.** Missing data is labeled `TBD` and surfaced as an open issue. Agents do not guess, default-fill, or silently infer.
- **Human authority at every gate.** Humans own acceptance, rulings, conflict resolution, scope changes, and publication approval. Agents propose; humans decide.
- **Write quarantine.** Every agent declares an explicit write scope. Tool roots are isolated from source truth. No agent writes outside its declared scope.
- **Conflicts surfaced, not resolved.** When sources disagree, produce a Conflict Table with contenders and a `HumanRuling = TBD` column. Never silently choose a winner.
- **Immutable snapshots.** Task agent outputs to tool roots are timestamped folders that are never modified. `_LATEST.md` pointers may be overwritten; snapshots may not.

## Key Locations

| Path | Content |
|------|---------|
| `agents/AGENT_*.md` | Agent instruction files (35 total) |
| `agents/AUDIT_AGENT.md` | Audit rubric (not an agent instruction) |
| `tools/REGISTRY.md` | Deterministic tool index (28 tools across 6 categories) |
| `tools/` | Shell scripts and Python utilities invoked by agents during pipeline execution |
| `docs/DIRECTIVE.md` | Founding intent and design philosophy |
| `docs/SPEC.md` | Physical structures, schemas, folder layouts |
| `docs/TYPES.md` | Domain vocabulary, ID formats, enums |
| `docs/CONTRACT.md` | K-* invariant catalog (23 binding invariants) |
| `docs/DBM_Agent_Instruction_Architecture.md` | Full design basis memorandum |
| `docs/SE_Design_Analysis.md` | Systems engineering design analysis |
| `AGENTS.md` | Operator-facing agent index and rules of the road |

## Naming Convention

Use `AGENT_*` when referring to instruction files (e.g., `AGENT_CHANGE.md`). Use the role name when referring to the agent itself (e.g., `CHANGE`).

## Next Step

Load your agent instruction file. It contains your type, class, interaction surface, write scope, blocking behavior, primary outputs, and full operational protocol.
