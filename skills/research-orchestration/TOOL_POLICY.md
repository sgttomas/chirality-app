# TOOL_POLICY — research-orchestration

## Preferred tool order

1. `tools/source_catalog/check_snapshot_freshness.py` — scout-stage freshness gate (run first).
2. `tools/retrieval/scaffold_research_packet.py` — create the immutable packet up front, so
   every stream writes into it (enables partial-packet salvage).
3. `tools/retrieval/query_source_index.py --run-log {PACKET}/Query_Log.csv` — all queries
   (direct and stream) log into the one packet.
4. (per load-bearing claim) re-query / cross-`--mode` for the adversarial critic stage.

## Allowed deterministic tools

### TASK-enforced

- None. `allowed-tools` is intentionally omitted from `SKILL.md`: this skill widens no
  authority, and its tools are agent-guided composition steps, not load-time-enforced grants.

### Operationally invoked

- `tools/source_catalog/check_snapshot_freshness.py`
- `tools/retrieval/scaffold_research_packet.py`
- `tools/retrieval/query_source_index.py` (with `--run-log` / `--log-dir`)
- `tools/source_catalog/validate_source_database.py` (optional deeper integrity check)

## Expected use of reasoning

Agent/LLM work — not tool work: triage routing (DIRECT vs AGENT), anchor-vs-assumption
judgment, dispatching and supervising `RESEARCHER` streams, the adversarial critique of
load-bearing claims, conflict adjudication, coverage-gap synthesis, and the decision to stop
retrying a failed stream. Orchestration itself is agent territory; the deterministic tools
only scout freshness, scaffold the packet, and log queries.

## Disallowed use

- `tools/source_catalog/build_source_database.py` and `tools/retrieval/build_source_index.py`
  — no silent refresh; a `STALE` verdict is surfaced, never auto-rebuilt.
- Any write outside the research packet and the run record.
- Merging external/web evidence into accepted domain truth.
- Auto-approving or applying the downstream decision the research reframes.

## Write boundary

Write only within `{ResearchRoot}/RCH_<UTC>_<slug>/**` (the immutable packet, once created)
and `_run_records/TASK_RUN_*.md`. The packet is immutable once scaffolded; a rerun creates a
new packet. No source, ledger, register, snapshot, index, or accepted-truth file is modified.
