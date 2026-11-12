# evaluation-report — method

## Method

### Step 1 — Read the evaluation protocol
Read `PROTOCOL_PATH` to understand the dimension definition, checks, and pass/fail criteria.

### Step 2 — Gather evidence
For each check in the dimension:
1. Read the specified data sources (deliverable files, tool root files, content digests, reconciliation reports, PDFs).
2. Execute deterministic queries using available tools where applicable:
   - File counts: `tools/evaluation/count_deliverable_files.sh {EXECUTION_ROOT}`
   - Lifecycle states: `tools/evaluation/extract_lifecycle_states.sh {EXECUTION_ROOT}`
   - Workspace summary: `tools/query/count_workspace_state.sh {EXECUTION_ROOT}`
   - Local need structure/reference observations: `tools.deliverables check` or the bounded dependency audit documented in `tools/evaluation/README.md`
   - Enum validation: `python3 tools/validation/validate_enum.py {ENUM_NAME} {value}`
   - ID format: `tools/validation/validate_id_format.sh {ID_TYPE} {ID_VALUE}`
   - Relevant neighbourhood/impact: read-only `tools.deliverables` queries, with `construct-local-work-graph` for the undertaking's sequencing assessment
3. Record evidence: file paths read, counts observed, specific text cited, tool invocation results. Local needs remain authoritative at their consumers; derived views do not become a dependency map. Preserve distinct condition/case/trigger, gating, unknown/external and outward-obligation meaning. The native CLI requires a project root in a Git repository with HEAD and reports native cycles only; see `tools/deliverables/README.md`. Every query loads all project declarations/path-presence references; use it only within the permitted read scope. Otherwise inspect relevant declarations directly and state coverage limits. A tool exit, source presence, producer lifecycle or reciprocal relation establishes no satisfaction/readiness verdict; assess the actual condition against the dimension's accepted criteria.

### Step 3 — Apply checks
For each check:
1. Compare gathered evidence against the pass/fail criteria.
2. Assign result: PASS, FAIL, or OBSERVATION.
3. Record evidence and notes.

### Step 4 — Score the dimension
Apply the scoring framework:
- EXEMPLARY: All checks pass; outputs exceed minimum requirements.
- CONFORMANT: All mandatory checks pass; minor observations noted.
- PARTIAL: Most checks pass; some gaps not compromising structural integrity.
- NON-CONFORMANT: Mandatory checks fail; structural integrity compromised.

### Step 5 — Write the report
Write the complete report to `OUTPUT_FILE` using the STRUCTURE schema.

---
