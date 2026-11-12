# TOOL_POLICY — research-orchestration

## Preferred tool order

1. `tools/source_catalog/check_snapshot_freshness.py` — scout-stage freshness gate (run first).
2. `tools/retrieval/scaffold_research_packet.py --no-update-latest` — create each packet up
   front so work is written into it as it proceeds (enables partial-packet salvage). Each
   AGENT stream scaffolds its own packet at its allocated `OUTPUT_DIR`; the owner scaffolds
   the aggregate packet. Without `--no-update-latest` the scaffolder rewrites
   `{ResearchRoot}/_LATEST.md`, which is outside this workflow's write boundary.
3. `tools/retrieval/query_source_index.py --run-log {PACKET}/Query_Log.csv` — every query
   (direct and stream) logs into its own allocated packet.
4. (per load-bearing claim) a live-tree or accepted-snapshot source read for verification;
   re-query / cross-`--mode` may help locate evidence for the critic stage but is not itself
   such verification.

## Allowed deterministic tools

### Effective tool restrictions

- None. `allowed-tools` is intentionally omitted from `WORKFLOW.md`: this workflow widens no
  authority, and its tools are agent-guided composition steps, not load-time-enforced grants.

### Operationally invoked

- `tools/source_catalog/check_snapshot_freshness.py`
- `tools/retrieval/scaffold_research_packet.py`
- `tools/retrieval/query_source_index.py` (with `--run-log` / `--log-dir`)
- `tools/source_catalog/validate_source_database.py` (optional deeper integrity check)

## Expected use of reasoning

Agent/LLM work — not tool work: triage routing (DIRECT vs AGENT),
anchor-vs-assumption judgment, using the effective source-qualified `researcher`
skill directly when the brief assigns it or dispatching and supervising bounded
TASK streams with that descriptor in their ordered `methods` field, adversarial
critique of load-bearing claims, conflict adjudication, coverage-gap synthesis,
and the decision to stop retrying a failed stream. Orchestration itself is agent
territory; the deterministic tools only scout freshness, scaffold the packet,
and log queries.

## Disallowed use

- `tools/source_catalog/build_source_database.py` and `tools/retrieval/build_source_index.py`
  — no silent refresh; a `STALE` verdict is surfaced, never auto-rebuilt.
- Any write outside the research packet and the run record.
- Merging external/web evidence into accepted domain truth.
- Auto-approving or applying the downstream decision the research reframes.

## Write boundary

Write only within `{ResearchRoot}/RCH_<UTC>_<slug>/**` (the immutable packet, once created)
and `_run_records/TASK_RUN_*.md`. `{ResearchRoot}/_LATEST.md` is outside the boundary. The packet is writable by its assigned owner during the run and immutable once finalized; a rerun creates a
new packet. No source, ledger, register, snapshot, index, or accepted-truth file is modified.
