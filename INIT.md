# INIT — Agent Bootstrap

Chirality is a formally specified agent operating system for deliverable-heavy professional work. All project truth lives in git-tracked plain files. Agents operate under invariant contracts, bounded write scopes, and human gate authority. The theoretical foundation, the regulatory grounding, and the argument for why this architecture takes the form it does are developed in `docs/thesis/`.

## Authoritative Documents

| Document | What It Governs |
|----------|-----------------|
| `docs/DIRECTIVE.md` | Founding intent, design philosophy, professional responsibility model |
| `docs/SPEC.md` | Physical structures, file formats, schemas, folder layouts |
| `docs/TYPES.md` | Domain vocabulary, stable IDs, enums, lifecycle states, agent roles |
| `docs/CONTRACT.md` | K-* invariant catalog: 20 binding invariants defined across CONTRACT.md §1 |
| `docs/DBM_Agent_Instruction_Architecture.md` | Full design basis for the instruction architecture |
| `docs/SE_Design_Analysis.md` | Systems engineering design analysis |
| `CHIRALITY_FRAMEWORK.md` | The Chirality Theory: knowledge, accountability, and the four pillars |
| `PROFESSIONAL_ENGINEERING.md` | Professional practice standard (APEGA regulatory mapping) |
| `AGENTS.md` | Agent index and matrix |
| `tools/REGISTRY.md` | Deterministic tool index (28 tools, 6 categories) |

## Naming Convention

Use `AGENT_*` for instruction files (e.g., `AGENT_CHANGE.md`). Use the role name for the agent itself (e.g., `CHANGE`). All instruction files are in `agents/`.

## Session Bootstrap

### Known-persona sessions (most Type 0 / Type 1 work)

When the persona is already decided and the task is scoped:

```
Bootstrap this session in read-only mode.

Read, in order:
1. INIT.md
2. AGENTS.md — read for naming convention, matrix layout, and the active agent's row;
   full index scan is not required unless the session involves routing or governance
3. agents/AGENT_<PERSONA>.md
4. <HANDOFF_OR_PLAN>.md — if this is a continuing thread
5. agents/AGENT_<PERSPECTIVE>.md — only if explicitly relevant to this session

After reading, do not start the work yet.
Reply with:
- Loaded documents
- Your role, type, write scope, and interaction surface
- What you will NOT do (scope constraints, forbidden writes)
- The governing files for this session
- Any assumptions you are carrying forward
- Ready to receive the specific task instructions
```

### Architecture / meta sessions

When the work touches governance, agent design, suite composition, or plan execution:

```
Bootstrap this architecture session in read-only mode.

Read, in order:
1. INIT.md
2. AGENTS.md — full read for suite orientation, matrix, and index
3. agents/AGENT_HELPS_HUMANS.md — adopt this design posture
4. agents/AGENT_<ACTIVE_PERSONA>.md
5. plans/NEXT_SESSION_HANDOFF.md
6. Any specifically named plan or policy files for this thread

After reading, do not start the work yet.
Reply with:
- Loaded documents
- Session posture and decision rights
- Active roadmap / handoff state
- What is authoritative vs reference-only
- Ready to receive the task
```

### When to read `AGENTS.md` in full

A targeted pass (naming convention, matrix, active agent's row) is sufficient when the persona is known and the task is scoped. A full read is justified when:

- the starting persona is not yet decided
- routing among agents is central to the session
- the work touches governance, indexing, or suite composition
- the session is architecture or meta work
