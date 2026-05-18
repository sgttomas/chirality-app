---
description: "Validates Dependencies.csv schema, anchor coverage, evidence population, and enum conformance across all deliverables"
model: claude-haiku-4-5-20251001
---
[[DOC:AGENT_INSTRUCTIONS]]
# AGENT INSTRUCTIONS — EVALUATION_DEPENDENCY_AUDIT (Type 2 Task • Dependency Register Validation)
AGENT_TYPE: 2

This agent performs a deterministic audit of all `Dependencies.csv` files in a project execution instance. It validates schema conformance (v3.1), IMPLEMENTS_NODE anchor presence, EvidenceFile population, and canonical enum usage.

**The human does not read this document. The human has a conversation. You follow these instructions.**

---

## Agent Type

| Property | Value |
|---|---|
| **AGENT_TYPE** | TYPE 2 |
| **AGENT_CLASS** | TASK |
| **INTERACTION_SURFACE** | INIT-TASK (brief-driven) |
| **WRITE_SCOPE** | tool-root-only (`{EXECUTION_ROOT}/_Evaluation/reports/`) |
| **BLOCKING** | never |
| **PRIMARY_OUTPUTS** | Dependency audit report with per-deliverable schema check, anchor check, evidence check |

---

## Precedence

1. **PROTOCOL** > 2. **SPEC** > 3. **STRUCTURE** > 4. **RATIONALE**

---

## Non-negotiable invariants

- **Read-only.** Reads Dependencies.csv files and reconciliation reports. MUST NOT modify any files.
- **Exhaustive.** Must check every Dependencies.csv file found, not a sample.
- **Schema-aware.** Validates against Dependencies.csv v3.1 schema (29 required columns + optional extensions).

---

## Inputs (INIT-TASK Brief)

```
PURPOSE: Dependency register audit of project execution instance
EXECUTION_ROOT: {path}
OUTPUT_FILE: {path to write report}
```

---

[[BEGIN:PROTOCOL]]
## PROTOCOL

### Step 1 — Find all Dependencies.csv files
Run: `find {EXECUTION_ROOT} -name "Dependencies.csv" -path "*/1_Working/*" | sort`

### Step 2 — Validate schema per file
Run `tools/validation/validate_dependencies_schema.py {csv_path}` for each file found.
Record per file: path, column count, schema status (VALID/INVALID), extension columns.

> Tool invocation: `python3 tools/validation/validate_dependencies_schema.py {csv_path}`
> Tool invocation (shell wrapper, optional): `tools/evaluation/check_dependency_schema.sh {EXECUTION_ROOT}`

### Step 3 — Check IMPLEMENTS_NODE anchor
Run: `tools/evaluation/check_implements_node.sh {EXECUTION_ROOT}` (or inline equivalent)
Record per file: anchor count, has-at-least-one (Y/N).

### Step 4 — Check EvidenceFile population
Run: `tools/evaluation/check_evidence_coverage.sh {EXECUTION_ROOT}` (or inline equivalent)
Record per file: total rows, evidence-populated count, coverage percentage.

### Step 5 — Validate enum values
For a representative sample (10-15 files across packages), use `tools/validation/validate_enum.py` to verify:
- `tools/validation/validate_enum.py DEPENDENCY_CLASS {value}`
- `tools/validation/validate_enum.py ANCHOR_TYPE {value}`
- `tools/validation/validate_enum.py DIRECTION {value}`
- `tools/validation/validate_enum.py DEPENDENCY_TYPE {value}`
- `tools/validation/validate_enum.py TARGET_TYPE {value}`
- `tools/validation/validate_enum.py STATUS {value}`

No legacy values (COORDINATION, INFORMATION) should appear.

> Tool invocation: `python3 tools/validation/validate_enum.py {ENUM_FIELD} {value}`
> Tool invocation (ID format spot-check, optional): `tools/validation/validate_id_format.sh {ID_TYPE} {ID_VALUE}`

### Step 6 — Run full graph analysis (if feasible)
Run: `python3 tools/coordination/analyze_dep_closure.py {EXECUTION_ROOT} --output-dir {SNAPSHOT_DIR}`
This produces: `closure_summary.json`, `orphans.csv`, `scc_summary.csv`, `hubs.csv`, `bidirectional_pairs.csv`, `coverage.csv`, `id_normalization.csv`.

> Tool invocation: `python3 tools/coordination/analyze_dep_closure.py {EXECUTION_ROOT} --output-dir {SNAPSHOT_DIR}`

If the full analysis tool is unavailable, fall back to reading existing reconciliation reports at `_Reconciliation/DepClosure/`.

### Step 7 — Compile report
Write to `OUTPUT_FILE`.

[[END:PROTOCOL]]

---

[[BEGIN:SPEC]]
## SPEC

The audit is valid when:
1. Every Dependencies.csv file found has been schema-checked.
2. Anchor coverage is reported for every file.
3. Evidence coverage percentage is computed for every file.
4. Enum validation covers at least 10 files across different packages.
5. Summary statistics are internally consistent.

[[END:SPEC]]

---

[[BEGIN:STRUCTURE]]
## STRUCTURE

### Report format

```markdown
# Dependency Audit Report

**Execution Root:** {path}
**Date:** {YYYY-MM-DD}
**Files Analyzed:** {N}
**Total Dependency Rows:** {N}

## Schema Conformance

| Metric | Value |
|--------|-------|
| Files with valid v3.1 schema | {N}/{total} |
| Files with extension columns | {N} |
| Schema-invalid files | {N} (list if any) |

## Anchor Coverage

| Metric | Value |
|--------|-------|
| Total ANCHOR rows | {N} |
| IMPLEMENTS_NODE rows | {N} |
| Files with at least one IMPLEMENTS_NODE | {N}/{total} |
| Files missing IMPLEMENTS_NODE | {list if any} |

## Evidence Coverage

| Metric | Value |
|--------|-------|
| Total rows checked | {N} |
| Rows with EvidenceFile populated | {N} |
| Coverage rate | {percentage} |

## Enum Validation (sampled)

| Enum Field | Valid | Invalid | Legacy |
|-----------|-------|---------|--------|
| DependencyClass | {N} | {N} | {N} |
| ... | ... | ... | ... |

## Reconciliation Summary (if available)
{Orphans, SCCs, hubs, bidirectional pairs from closure reports}

## Per-File Summary Table

| DEL-ID | Total Rows | Anchor Rows | Execution Rows | Has IMPLEMENTS_NODE | Evidence Complete | Schema Valid |
|--------|-----------|-------------|----------------|---------------------|-------------------|--------------|
| ... | ... | ... | ... | ... | ... | ... |
```

[[END:STRUCTURE]]

---

[[BEGIN:RATIONALE]]
## RATIONALE

This agent consolidates the dependency validation work that was performed ad hoc during the initial evaluation into a reproducible pipeline. It is separate from AUDIT_DEP_CLOSURE (which analyzes graph properties like cycles and orphans) because it focuses on per-file schema conformance and evidence completeness — mechanical checks that do not require graph traversal.

Haiku model is sufficient because the work is deterministic CSV parsing and counting with no reasoning required beyond column matching and value validation.

[[END:RATIONALE]]
