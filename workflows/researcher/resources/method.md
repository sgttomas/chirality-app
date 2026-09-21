# researcher — method

## Method

1. **Ground from parameters.** Resolve `DOMAIN_ROOT`, `ACCEPTED_SNAPSHOT_PATH`, and
   `RETRIEVAL_SNAPSHOT` from the brief — never from chat or session memory. If a required
   parameter is missing, return `STATUS: FAILED_INPUTS` naming what is missing; do not invent.
2. **Guard the write scope.** Confirm `OUTPUT_DIR` resolves under `{RESEARCH_ROOT}`;
   otherwise STOP with `ERROR: OUTPUT_DIR_OUTSIDE_RESEARCH_ROOT`.
3. **Scaffold the packet first** with
   `python3 {INSTRUCTION_ROOT}/tools/retrieval/scaffold_research_packet.py --research-root {RESEARCH_ROOT} --output-dir {OUTPUT_DIR} --slug <slug> --no-update-latest`
   so every later step writes *into* the packet (write-as-you-go). The packet must be allocated exactly at OUTPUT_DIR; verify the returned path. Refuse an existing completed packet; a recovery attempt uses a fresh allocated packet.
4. **Freshness scout.** Run `tools/source_catalog/check_snapshot_freshness.py --snapshot
   {RETRIEVAL_SNAPSHOT} --json`; record the `FRESH|STALE` verdict in `HANDOFF_STATE.md`. Do
   **not** rebuild. If `STALE`, every retrieval-only claim carries a staleness caveat and
   load-bearing claims must be re-verified against the live tree.
5. **Classify.** Use `RESEARCH_MODE` if given; otherwise classify per `evidence.md`
   Step 1 and record the assumption.
6. **Retrieve and synthesize** per `inquiry.md`, logging every query with
   `tools/retrieval/query_source_index.py … --run-log {OUTPUT_DIR}/Query_Log.csv` (logged
   queries must match executed queries — do not transcribe from memory). Populate
   `Evidence_Map.csv` incrementally, setting `VerificationSource`, `AssertionMode`
   (`READ`/`RUN`), and `LoadBearing` on each row.
7. **Re-verify load-bearing anchors.** Any brief-supplied "fact" enters as
   `VerificationSource = INHERITED_BRIEF` and is treated as `R1`-equivalent. It MUST be
   independently verified against the live tree or accepted snapshot before any load-bearing
   claim reaches `R3` or better. Never let an inherited brief fact become a warrant unchecked.
8. **Record amendment candidates** as `Amendment_Candidates.csv` rows (structured, not
   prose), so the dispatcher can route them to `WORKING_ITEMS (workflow: scope-change)` / `WORKING_ITEMS (workflow: domain-decomp)`.
9. **Partial-return on failure.** On a transient error (API 5xx, tool error, timeout),
   return `STATUS: PARTIAL` with whatever was written plus an explicit `CoverageGaps[]`
   naming what was not covered and why. Never discard partial results or fail silently.
10. **Return, do not act.** Emit the structured return object (STRUCTURE) to the parent.
    Route nothing yourself; conflicts and amendment candidates are the parent's/human's to
    rule on.

---
