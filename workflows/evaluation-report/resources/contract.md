# evaluation-report — contract

## Non-negotiable invariants

- **Read-only on project state.** This agent reads deliverable folders, tool roots, decomposition, source documents, and content digests. It MUST NOT write to any location outside `_Evaluation/reports/`.
- **Evidence-first.** Every check result cites specific file paths, counts, or quotations. No unsupported judgments.
- **No invention.** If evidence is insufficient to score a check, record the check as OBSERVATION with an explanation of what evidence is missing.
- **Conflicts surfaced.** If evidence contradicts the expected outcome, document the contradiction rather than resolving it silently.
- **One report per run.** Each invocation produces exactly one dimension report file.

---

## Inputs (INIT-TASK Brief)

```
PURPOSE: Score evaluation dimension {N}: {DimensionName}
EXECUTION_ROOT: {path}
DIMENSION: {N}
DIMENSION_NAME: {name}
CHECKS: {list of check IDs with descriptions}
DATA_SOURCES: {paths to read for evidence}
PROTOCOL_PATH: {path to EVALUATION_PROTOCOL.md}
OUTPUT_FILE: {path to write report}
```

---

## Validity

A dimension report is valid when:
1. Every check listed in the brief has a recorded result (PASS/FAIL/OBSERVATION).
2. Every result cites specific evidence (file path, count, or quotation).
3. The dimension score is one of: EXEMPLARY, CONFORMANT, PARTIAL, NON-CONFORMANT.
4. The score justification references the check results.
5. The report lists all evidence files read.
6. The report is written to the specified `OUTPUT_FILE` path.

---

## Artifacts and schemas

### Report format

```markdown
# Dimension {N}: {DimensionName}

**Score: {EXEMPLARY|CONFORMANT|PARTIAL|NON-CONFORMANT}**

**Evaluation Date:** {YYYY-MM-DD}
**Data Sources:** {summary of what was read}

---

## Checks

| Check ID | Result | Evidence | Notes |
|----------|--------|----------|-------|
| {ID} | {PASS/FAIL/OBSERVATION} | {specific evidence} | {context} |

---

## Detailed Findings

### {Check ID} — {Check Name}

**Result:** {PASS/FAIL/OBSERVATION}

**Evidence:**
{Detailed evidence with file paths and citations}

**Assessment:**
{Why this result was assigned}

---

## Score Justification

{Narrative explaining why the overall dimension score was assigned, referencing specific check results}

---

## Evidence Files Read

- {file_path_1}
- {file_path_2}
- ...
```

---
