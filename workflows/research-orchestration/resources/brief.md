# BRIEF_SCHEMA — research-orchestration

WORKING_ITEMS receives this orchestration brief. Each child receives a separate
bounded brief with an exact, disjoint `OUTPUT_DIR` and the effective
source-qualified `researcher` skill descriptor in its ordered `methods` field.
Load resources for the current stage.

## Required brief fields

| Field | Type | Example |
|---|---|---|
| `PURPOSE` | string | "Scope the next dev program from the post-stabilization state." |
| `Workflow` | literal | `research-orchestration` |
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

`DIRECT` rows are answered by a single `query_source_index.py`/`grep` call.
`AGENT` rows are dispatched as TASK streams with
`methods: [{kind: "skill", name: "researcher", source: <descriptor.source>, sourceRootId: <descriptor.sourceRootId>}]`,
where the descriptor came from effective catalog discovery.

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
