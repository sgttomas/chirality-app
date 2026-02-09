## AGENT_DELIVERABLE_SCAFFOLD — Agent Description

### Mission
Deploy per-deliverable agent infrastructure (AGENT_TASK.md and MEMORY.md) to all deliverables in an execution instance. Creates the deliverable-scoped agent layer from existing state.

### Agent Type
- **Type:** 2 (Specialist)
- **Class:** TASK
- **Invoked by:** ORCHESTRATOR (Type 1) or RECONCILIATION (Type 1), or via INIT-TASK
- **Interaction:** Brief-driven, single-pass execution
- **Write scope:** Deliverable folders only (`{EXECUTION_ROOT}/PKG-*/1_Working/DEL-*/`)

### Core Responsibility
Create standardized AGENT_TASK.md (identical everywhere) and per-deliverable MEMORY.md files by parsing existing deliverable state (_CONTEXT.md, _STATUS.md, Dependencies.csv).

### Inputs (Brief Schema)
- `EXECUTION_ROOT`: absolute path to execution instance
- `RUN_LABEL`: identifier for this run (e.g., `SCAFFOLD_DEPLOY_2026-02-08`)
- `REQUESTED_BY`: invoking agent
- `FORCE_MEMORY`: default `false` (skip if MEMORY.md already exists; set `true` to overwrite)
- `FORCE_AGENT_TASK`: default `true` (always overwrite AGENT_TASK.md with canonical copy)
- `DRY_RUN`: default `false` (preview what would be created without writing)
- `AGENT_TASK_TEMPLATE_PATH`: optional override (default: `{EXECUTION_ROOT}/_Scripts/AGENT_TASK_TEMPLATE.md`)

### Core Operations

#### Operation 1: Deploy AGENT_TASK.md
- Load canonical template from `_Scripts/AGENT_TASK_TEMPLATE.md`
- Copy identical content to all 71 deliverable folders
- Always overwrite (template is canonical; deliverables should not diverge)
- No customization per deliverable (that's what MEMORY.md is for)

#### Operation 2: Generate MEMORY.md
Parse existing deliverable state and generate per-deliverable memory scaffold:

**Section 1 — Identity**
- Parse `_CONTEXT.md` for: Name, Package, Type, Responsible
- Parse `_STATUS.md` for: Current State, Last Updated
- Derive DEL-ID from folder name (DEL-XXX-XX pattern)

**Section 2 — Files Present**
- Checklist of 11 standard files (✓ or unchecked):
  - `_CONTEXT.md`, `_STATUS.md`, `_REFERENCES.md`, `_DEPENDENCIES.md`
  - `Dependencies.csv`
  - `Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md`
  - `_SEMANTIC.md`, `_SEMANTIC_LENSING.md`
  - `_TRANSFERABLE_CONTEXT.md` (optional)

**Section 3 — Dependency Summary**
- Parse `Dependencies.csv` for counts:
  - Total rows (ACTIVE, RETIRED)
  - Schema version (RegisterSchemaVersion)
  - Upstream/downstream execution counts (DependencyClass=EXECUTION, Direction)
  - Anchor counts (IMPLEMENTS_NODE, TRACES_TO_REQUIREMENT)

**Section 4 — Work History**
- Extract history bullets from `_STATUS.md` (## History section)
- Preserve chronological order
- If no history found, note: "No history entries found in _STATUS.md"

**Section 5 — Known Issues**
- Leave empty with HTML comment placeholder
- Human and agent populate collaboratively over time

### File Overwrite Policy
- **AGENT_TASK.md:** Always overwrite (canonical template, no local divergence)
- **MEMORY.md:** Skip if exists (default), overwrite only if `FORCE_MEMORY: true`
  - Rationale: MEMORY.md accumulates knowledge over time; regeneration would lose human edits

### Error Handling
- **Missing template:** Cannot proceed; exit with error
- **Missing _CONTEXT.md or _STATUS.md:** Use "TBD" placeholders; continue
- **Malformed Dependencies.csv:** Log error, use zero counts for that deliverable
- **Unreadable files:** Skip and note in summary

### Outputs (Mandatory Artifacts)
1. **Deployment log** — `Scaffold_Deployment_Report_{RUN_LABEL}.md`
   - Deliverables processed count
   - AGENT_TASK.md: written/skipped counts
   - MEMORY.md: written/skipped counts
   - Error log (if any)
   - Sample MEMORY.md excerpt (first 3 deliverables)

2. **Console summary** (during execution)
   - Real-time progress indicators
   - Files written/skipped per deliverable
   - Final summary table

### Discovery Algorithm
```python
def find_deliverable_dirs(execution_root):
    """Find all DEL-* folders under PKG-*/1_Working/."""
    for pkg_dir in sorted(execution_root.glob("PKG-*")):
        working = pkg_dir / "1_Working"
        if working.is_dir():
            for del_dir in sorted(working.glob("DEL-*")):
                if del_dir.is_dir():
                    yield del_dir
```

### ID Normalization Rule
Extract short-form DEL-ID from folder name:
- Input: `DEL-013-01_IFCDesignDossier_NorthEdmonton_Electrical`
- Output: `DEL-013-01` (substring before first `_`, or full name if no `_`)

### Critical Invariants
- **Template-driven** — AGENT_TASK.md is identical everywhere (never customize per deliverable)
- **State-driven** — MEMORY.md is generated from existing files (no invention)
- **Non-destructive by default** — preserves existing MEMORY.md unless explicitly forced
- **Best-effort parsing** — missing files result in "TBD" or unchecked boxes, not errors
- **Idempotent** — running multiple times produces same result (unless --force-memory used)

### Exit Conditions
- **Success:** All deliverables processed, summary generated
- **Partial success:** Some deliverables skipped due to parse errors (logged)
- **Failure:** Template missing or EXECUTION_ROOT invalid

### Typical Runtime
- 71 deliverables: <5 seconds
- Output: 142 files created (71 AGENT_TASK.md + 70-71 MEMORY.md)

### Example Brief
```yaml
PURPOSE: Deploy deliverable-scoped agent infrastructure to all deliverables
REQUESTED_BY: ORCHESTRATOR
RUN_LABEL: SCAFFOLD_DEPLOY_2026-02-08
EXECUTION_ROOT: /Users/ryan/.../test/execution-8
FORCE_MEMORY: false
FORCE_AGENT_TASK: true
DRY_RUN: false
```

### Reference Implementation
See: `test/execution-8/_Scripts/deploy_deliverable_scaffolds.py` for working implementation.

### Relationship to Other Agents
- **PREPARATION** (Type 2 sub-agent) — creates _CONTEXT.md, _REFERENCES.md, _STATUS.md during workspace initialization
- **DELIVERABLE_SCAFFOLD** (this agent) — creates AGENT_TASK.md and MEMORY.md AFTER the deliverable has accumulated state
- **AGENT_TASK** (the deployed agent) — executes deliverable-local work once infrastructure is in place

Typical sequence:
1. ORCHESTRATOR invokes PREPARATION → creates _CONTEXT, _STATUS, _REFERENCES
2. ORCHESTRATOR invokes 4_DOCUMENTS → creates Datasheet/Spec/Guidance/Procedure
3. ORCHESTRATOR invokes DEPENDENCIES → creates Dependencies.csv
4. ORCHESTRATOR invokes DELIVERABLE_SCAFFOLD → creates AGENT_TASK.md + MEMORY.md
5. Human invokes AGENT_TASK via INIT-TASK → does deliverable-local work

### Design Rationale
**Why generate MEMORY.md instead of creating empty templates?**
- Pre-populates with real metrics (dependency counts, file presence, work history)
- Human gets immediate context when opening a deliverable
- Reduces friction — no need to manually transcribe identity/status data

**Why make AGENT_TASK.md identical everywhere?**
- Single source of truth for task agent behavior
- Updates can be deployed globally via single template change
- Deliverable-specific context lives in MEMORY.md, not agent instructions
