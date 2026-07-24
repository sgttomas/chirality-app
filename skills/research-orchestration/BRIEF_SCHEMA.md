# BRIEF_SCHEMA — research-orchestration

Dispatch contract for invoking `research-orchestration` through `TASK` (or for a Type-1
persona running the fan-out directly). When `TASK` loads this skill via `TaskSkill:
research-orchestration`, it also loads `SKILL.md` + companions. `CustomInstructions` carry
run-specific reinforcement; they do not replace skill hydration — `SKILL.md` is authoritative.

## Required brief fields

| Field | Type | Example |
|---|---|---|
| `PURPOSE` | string | "Scope the next dev program from the post-stabilization state." |
| `TaskSkill` | literal | `research-orchestration` |
| `Question` | string | "What remains for R6 extensibility, and what are the boundaries?" |
| `DomainRoot` | path | `domains/chirality-app-dev` |
| `RetrievalSnapshot` | path | `domains/chirality-app-dev/_LocalIndexes/_LATEST.md` |
| `ResearchRoot` | path | `domains/chirality-app-dev/_Research` |
| `StreamPlan` | table | see below |
| `ApplyEdits` | bool | `true` (the packet + run record are written) |
| `AllowedWriteTargets` | list | `["{ResearchRoot}/RCH_*/", "_run_records/"]` only |

### `StreamPlan` shape

One row per sub-question:

| sub-question | route | load-bearing? | critic? |
|---|---|---|---|
| "Enumerate the current tool-descriptor surface" | AGENT | yes | yes |
| "Exact name of the collision-check helper" | DIRECT | no | no |

`DIRECT` rows are answered by a single `query_source_index.py`/`grep` call. `AGENT` rows are
dispatched as `RESEARCHER` streams.

## Optional fields

| Field | Type | Notes |
|---|---|---|
| `AnchorSet` | list | Caller-supplied "facts" — each is re-verified, not trusted. |
| `PacketSlug` | string | Slug for `RCH_<UTC>_<slug>/`; defaults from `Question`. |

## RuntimeOverrides

| Override | Meaning | Default | Allowed |
|---|---|---|---|
| `MAX_RETRIES` | per-stream transient-failure retries | `2` | `0`–`3` |
| `CRITIC_REQUIRED` | run the adversarial live critic before `R3+` | `true` | `true`/`false` |
| `ANCHOR_POLICY` | how much to anchor | `LIGHT` | `LIGHT`/`NONE` |
| `FRESHNESS_GATE` | behavior on a `STALE` snapshot | `WARN` | `WARN` (no other; never auto-refresh) |

## Recommended `CustomInstructions` (defense-in-depth)

- "No silent stream loss — record every planned stream's terminal status."
- "Load-bearing claims require live re-verification before `R3+`; do not promote an inherited
  brief fact to a warrant."
- "On `API 500`, retry only the failed stream(s) via `resumeFromRunId`, cap at `MAX_RETRIES`,
  then surface coverage-gaps — do not restart the whole batch."
- "Do not rebuild/refresh the index; surface a `STALE` verdict instead."
- "Defer the human-gated decisions the research reframes to the caller; this skill packages
  and recommends, it approves nothing."
