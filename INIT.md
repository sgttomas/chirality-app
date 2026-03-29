# INIT — Agent Bootstrap

Chirality is a formally specified agent operating system for deliverable-heavy professional work. All project truth lives in git-tracked plain files. Agents operate under invariant contracts, bounded write scopes, and human gate authority.

## Authoritative Documents

| Document | What It Governs |
|----------|-----------------|
| `docs/DIRECTIVE.md` | Founding intent, design philosophy, professional responsibility model |
| `docs/SPEC.md` | Physical structures, file formats, schemas, folder layouts |
| `docs/TYPES.md` | Domain vocabulary, stable IDs, enums, lifecycle states, agent roles |
| `docs/CONTRACT.md` | K-* invariant catalog (23 binding invariants) |
| `docs/DBM_Agent_Instruction_Architecture.md` | Full design basis for the instruction architecture |
| `docs/SE_Design_Analysis.md` | Systems engineering design analysis |
| `AGENTS.md` | Agent index and matrix |
| `tools/REGISTRY.md` | Deterministic tool index (28 tools, 6 categories) |

## Naming Convention

Use `AGENT_*` for instruction files (e.g., `AGENT_CHANGE.md`). Use the role name for the agent itself (e.g., `CHANGE`). All instruction files are in `agents/`.

## Next Step

Read `AGENTS.md` for the agent index, then load your agent instruction file. It contains your type, class, write scope, invariants, and full operational protocol.
