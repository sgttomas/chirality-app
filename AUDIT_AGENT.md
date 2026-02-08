# AUDIT_AGENT.md — Rubric for Auditing `AGENT_*.md` Instruction Files

This rubric is used by **AUDIT_AGENTS (Type 2)** to audit agent instruction files for coherence and conformance against the canonical standard (`agents/AGENT_HELPS_HUMANS.md`).

## Severity Levels (use consistently)

- `BLOCKER`: prevents safe or correct execution (missing write-scope rules, missing critical inputs/outputs, contradictory permissions).
- `HIGH`: likely to cause incorrect behavior or unsafe drift at scale.
- `MED`: correctness risk, unclear contract, or weak QA; fix soon.
- `LOW`: polish, clarity, formatting; fix when convenient.

## Audit Metadata (fill once per run)

- `AuditRunID`:
- `Auditor`:
- `Date`:
- `CanonicalStandardPath`: `agents/AGENT_HELPS_HUMANS.md` (or override)
- `FilesAudited`:
- `Notes`:

## Canon Extraction (fill once per run)

Record the canonical requirements you are enforcing (short bullets, with file locations):

- Required Agent Header Block fields (class/surface/scope/blocking/outputs)
- Write quarantine + snapshot expectations for task agents
- Provenance/no-invention/conflict surfacing expectations
- Brief-driven pipeline expectations for task agents

## Per-File Worksheet (copy once per audited file)

### File
- `Path`:
- `AgentRoleName`:
- `DeclaredAGENT_TYPE`:
- `DeclaredAGENT_CLASS`:
- `DeclaredINTERACTION_SURFACE`:
- `DeclaredWRITE_SCOPE`:
- `DeclaredBLOCKING`:
- `DeclaredPRIMARY_OUTPUTS`:

### R1 — Header Block Completeness

Checks:
- Naming convention line present (or explicitly delegated to project-level standard).
- Agent Type table present and includes: `AGENT_TYPE`, `AGENT_CLASS`, `INTERACTION_SURFACE`, `WRITE_SCOPE`, `BLOCKING`, `PRIMARY_OUTPUTS`.

Findings:
- `Severity`:
- `Evidence` (<=25 words + location):
- `CanonRequirement` (<=25 words + location):
- `RecommendedFix`:

### R2 — Contract Clarity (Inputs/Outputs)

Checks:
- Inputs are explicit (required vs optional).
- Outputs are explicit and deterministic (file names/locations), and aligned with write scope.
- Any referenced external contract/rubric files exist.

Findings:
- `Severity`:
- `Evidence`:
- `CanonRequirement`:
- `RecommendedFix`:

### R3 — Permission & Write-Scope Hygiene

Checks:
- Write scope matches described behavior (no hidden edits).
- Task agents are straight-through (`BLOCKING=never`) unless explicitly justified.
- No recursive-ingestion risk when writing to tool roots (exclusions stated if applicable).

Findings:
- `Severity`:
- `Evidence`:
- `CanonRequirement`:
- `RecommendedFix`:

### R4 — Epistemic Controls (Provenance / No Invention)

Checks:
- Provenance fields required for extracted/aggregated claims.
- Unknowns handled as `TBD` / `UNKNOWN` with explicit labeling.
- Conflicts/duplicates surfaced; no silent resolution unless explicitly directed.

Findings:
- `Severity`:
- `Evidence`:
- `CanonRequirement`:
- `RecommendedFix`:

### R5 — QA Contract

Checks:
- The agent defines acceptance checks (schema validity, coverage reporting, contradiction surfacing).
- Failure posture is explicit (warn-and-continue vs fail-fast; no silent fixes).

Findings:
- `Severity`:
- `Evidence`:
- `CanonRequirement`:
- `RecommendedFix`:

### R6 — Snapshot / Run-History Contract (Task Agents)

Checks (apply when the agent writes any artifacts):
- Defines what each run writes and where.
- Defines immutability/pointer behavior (or an explicit alternative like append-only run history).

Findings:
- `Severity`:
- `Evidence`:
- `CanonRequirement`:
- `RecommendedFix`:

### Summary

- `OverallStatus`: PASS | WARN | FAIL
- `TopIssues` (max 10):
- `PatchPlan` (minimal edits; prefer diffs or rewrite blocks):

