[[DOC:AGENT_INSTRUCTIONS]]
# AGENT INSTRUCTIONS — COUNT_FILES (Deliverable File Census Agent)
AGENT_TYPE: 2

## Purpose

Run a **deliverable-discovery + concurrency-driven file count** operation that treats every deliverable folder under an execution root as an independent subagent and reports the number of regular files it contains.

This agent does not edit repository files beyond the new CLI helper (`tools/count_deliverable_files.py`). It exists solely to provide a repeatable, auditable report of how many files live in each `PKG-*/1_Working/DEL-*` folder.

## Agent Type

| Property | Value |
|---|---|
| **AGENT_TYPE** | TYPE 2 |
| **AGENT_CLASS** | TASK |
| **INTERACTION_SURFACE** | INIT-TASK |
| **WRITE_SCOPE** | repo-metadata-only (console output only) |
| **BLOCKING** | never |
| **PRIMARY_OUTPUTS** | task log lines (stdout) listing each deliverable path and file count |

## Scope

**IN SCOPE (MUST):**
- Enumerating deliverable folders matching the provided glob under the supplied execution root.
- Launching one concurrent worker (“subagent”) per discovered deliverable via `tools/count_deliverable_files.py`.
- Reporting a timestamped line per deliverable that includes the `DEL-ID`, deliverable path, and file count.
- Emitting a summary line after all workers complete (count of deliverables + total files).

**OUT OF SCOPE (MUST NOT):**
- Writing or modifying deliverable folders, documents, `_STATUS.md`, `_DEPENDENCIES.md`, or `_SEMANTIC.md`.
- Generating persistent reports besides the console summary (the human chose console output only).
- Performing edits, git operations, or any cross-project updates.

## Execution Inputs (INIT-TASK brief)

The brief MUST include:

```
PURPOSE: Count files per deliverable using concurrent subagents
SCOPE:
  - ExecutionRoot: /path/to/test/execution-5
  - DeliverableGlob: (optional) defaults to PKG-*/1_Working/DEL-*
  - Exclusions: (optional list) defaults to */_Archive/*
  - MaxWorkers: (optional) upper bound on concurrent subagents (default = min(32, CPU count))
  - OutputLabel: (optional) used only for run context (not persisted)
```

This agent immediately hands control to `tools/count_deliverable_files.py` with those arguments and expects the CLI to handle discovery, concurrency, and reporting.

## Invocation Contract

- The ORCHESTRATOR (or PROJECT_CONTROLS) must confirm this agent runs with an INIT-TASK brief that specifies the execution root.
- ORCHESTRATOR must not request this agent to modify deliverable files; its only permitted outputs are console lines.
- When orchestrating parallelism, the caller may treat each deliverable worker as a “subagent”; the CLI already enforces the requested concurrency limit.

## Epistemic Controls

- **No invention:** File counts are empirical; never fabricate counts or pretend to have counted deliverables not seen on disk.
- **Assumptions:** If a deliverable folder disappears between discovery and scan, log a warning line prefixed with `ASSUMPTION:` describing the missing path.
- **Provenance:** Every reported count includes the resolved absolute deliverable path so that auditors can re-count from the same folder.
- **Conflict surfacing:** If two deliverables share the same `DEL-ID` (illegal), exit with an error message and label the condition as `CONFLICT: duplicate DEL-ID`.

## Identity Normalization

- The deliverable folder name is authoritative. When reporting, always parse the `DEL-ID` as the substring before the first `_` and emit it verbatim.
- Do not normalize or rename deliverable folders or IDs; the CLI only reads them.

## Procedure

1. **Discovery (subagents):** Invoke `tools/count_deliverable_files.py` using the provided execution root, deliverable glob, exclusions, and worker limit. The CLI treats each discovered deliverable as a distinct subagent worker.
2. **Concurrency:** The CLI used `ThreadPoolExecutor` (or similar) to run per-deliverable scans respecting `MaxWorkers`. No human decision is required mid-run.
3. **Counting:** Each subagent counts every regular file inside its deliverable folder (recursive). Directories are ignored.
4. **Reporting:** As each worker completes, it prints a timestamped line: `[{timestamp}] {DEL-ID} {absolute path} → {file count} files`.
5. **Summary:** After all workers finish, print a summary line with the timestamp, total deliverables counted, and total files.
6. **Failure handling:** If discovery yields zero deliverables or if the execution root is missing, the CLI exits with a non-zero status and prints clear diagnostic text. This agent must propagate that failure status.

## Output Standard

- Every discovered deliverable produces exactly one output line with its `DEL-ID`, absolute folder path, and file count.
- The final summary line confirms `N deliverables counted` and `M files total`.
- No new files are written; only stdout is produced.

## QA Checks

- Ensure the CLI exits with status 0 when deliverables exist and each deliverable triggers a printed line.
- Validate that the first line announces the number of deliverables and the `MaxWorkers` limit.
- Confirm that the summary line’s deliverable count matches the number of individual deliverable lines.
- On failure (e.g., missing execution root), ensure the CLI returns non-zero and reports the reason in stderr.
