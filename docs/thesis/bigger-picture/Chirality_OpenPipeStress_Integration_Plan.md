# Integration Plan: Chirality App and OpenPipeStress

**Document ID:** CHIRALITY-OPS-INTEGRATION-PLAN-001  
**Status:** Draft implementation plan  
**Related amendment:** `CHIRALITY-PRD-AMENDMENT-DOMAIN-ENGINES-001`  
**Purpose:** Plan the concrete changes needed to integrate OpenPipeStress with the Chirality App agent framework.

---

## 1. Integration Thesis

The best integration is a **filesystem-native, deterministic domain-tool integration**.

Chirality should not embed the OpenPipeStress GUI, solver, or model engine. OpenPipeStress should not become a general-purpose agent operating system. Instead:

```text
Chirality App
  orchestrates agents, deliverables, review notes, change records, dependency registers, summaries, and human gates.

OpenPipeStress
  owns the physical piping model, analytical model, solver, model states, analysis runs, comparisons, handoff packages, and GUI editing.

OpenPipeStress Tool Adapter
  exposes deterministic commands Chirality can call safely.

Human Operator
  accepts or rejects changes and decides what can be relied upon.
```

This gives Chirality useful visibility into OpenPipeStress work without letting agents directly mutate engineering model truth.

---

## 2. Integration Levels

Integration should proceed through levels. Do not jump directly to deep automation.

### Level 0: Manual File-Based Coordination

No code integration required.

- User runs OpenPipeStress manually.
- User exports summaries, reports, manifests, and comparison files.
- Chirality agents read those files and help with review notes, assumptions, TBDs, handoff checklists, and deliverable scaffolding.

### Level 1: Read-Only Deterministic Adapter

Chirality can call OpenPipeStress tools that do not mutate canonical model truth.

Examples:

```text
ops.validate_model
ops.summarize_model
ops.list_states
ops.list_runs
ops.list_comparisons
ops.check_private_data_boundary
ops.check_professional_boundary_language
```

### Level 2: Domain-Controlled Output Generation

Chirality can request OpenPipeStress to produce analysis runs, comparisons, and handoff packages through the OpenPipeStress adapter. These are domain-controlled writes, not raw agent writes.

Examples:

```text
ops.run_analysis
ops.compare_states
ops.compare_runs
ops.generate_handoff
ops.generate_report_fragment
```

Some of these should require explicit user confirmation.

### Level 3: Operation Proposal Workflow

Agents can create structured operation proposals. OpenPipeStress validates and previews them. The user accepts or rejects them in the OpenPipeStress GUI or through a future deterministic approval path.

Example:

```text
agent writes proposal → OpenPipeStress validates → user reviews diff → OpenPipeStress applies → new model state
```

### Level 4: External Result State Support

Future only.

Users may import or manually enter selected external professional-tool results as structured result states. OpenPipeStress compares them using its generic comparison engine. Chirality summarizes the result but does not declare validation or professional acceptance.

---

## 3. Target Architecture

```text
┌──────────────────────────────────────────────┐
│ Chirality Desktop Harness                     │
│ - agents                                      │
│ - workbench / pipeline                        │
│ - deliverables                                │
│ - dependency registers                        │
│ - lifecycle records                           │
│ - git-tracked project truth                   │
└─────────────────────┬────────────────────────┘
                      │ deterministic tool calls
                      │ manifests / proposals / summaries
                      ▼
┌──────────────────────────────────────────────┐
│ OpenPipeStress Tool Adapter / CLI             │
│ - validate schema                             │
│ - summarize model                             │
│ - list states and runs                        │
│ - run analysis                                │
│ - compare states/runs                         │
│ - generate handoff package                    │
│ - generate report fragments                   │
│ - validate operation proposals                │
└─────────────────────┬────────────────────────┘
                      │
                      ▼
┌──────────────────────────────────────────────┐
│ OpenPipeStress Domain Application             │
│ - 3D GUI                                      │
│ - schema-backed physical model                │
│ - analytical model                            │
│ - solver                                      │
│ - model states                                │
│ - analysis runs                               │
│ - comparison records                          │
│ - handoff packages                            │
└──────────────────────────────────────────────┘
```

---

## 4. Required Artifacts

### 4.1 Chirality-Side Artifacts

Create or amend:

```text
CHIRALITY-PRD-AMENDMENT-DOMAIN-ENGINES-001.md
DOMAIN_ENGINE_PROFILE_SPEC.md
DOMAIN_TOOL_ADAPTER_SPEC.md
DOMAIN_WRITE_BOUNDARY_POLICY.md
DOMAIN_OPERATION_PROPOSAL_SPEC.md
```

### 4.2 OpenPipeStress-Side Artifacts

Create or amend:

```text
OPENPIPESTRESS_CHIRALITY_PROFILE.yaml
OPENPIPESTRESS_CHIRALITY_ARTIFACT_LAYOUT.md
OPENPIPESTRESS_CLI_ADAPTER_SPEC.md
OPENPIPESTRESS_OPERATION_PROPOSAL_SCHEMA.yaml
OPENPIPESTRESS_REPORT_FRAGMENT_SPEC.md
OPENPIPESTRESS_HANDOFF_MANIFEST_SPEC.md
```

### 4.3 Project-Root Artifacts

For a real project:

```text
Model_Manifest.md
Model_Manifest.yaml
Model_Warnings.md
Model_Assumptions.md
RUN-*_summary.md
CMP-*_summary.md
CMP-*_delta_table.csv
Handoff_Manifest.md
Export_Warnings.md
TBD_Register.md
Review_Notes.md
```

---

## 5. Recommended Project Layout

```text
projectRoot/
  INIT.md

  PKG-01_PipingDesign/
    DEL-01-01_DesignBasis/
      _STATUS.md
      Datasheet.md
      Specification.md
      Guidance.md
      Procedure.md
      TBD_Register.md

    DEL-01-02_OpenPipeStressModel/
      _STATUS.md
      Model_Manifest.md
      Model_Manifest.yaml
      Model_Warnings.md
      Model_Assumptions.md
      OpenPipeStress/
        project.ops.yaml
        states/
        runs/
        comparisons/
        handoff/
        proposals/

    DEL-01-03_InternalStressAnalysis/
      _STATUS.md
      RUN-0041_summary.md
      RUN-0052_summary.md
      Solver_Diagnostics.md

    DEL-01-04_StateComparison/
      _STATUS.md
      CMP-0007_summary.md
      CMP-0007_delta_table.csv
      Review_Notes.md

    DEL-01-05_ExternalProverHandoff/
      _STATUS.md
      Handoff_Manifest.md
      Export_Warnings.md
      External_Review_TBDs.md

  _Sources/
    line_list/
    pid_extracts/
    equipment_interfaces/
    owner_requirements/

  _Reconciliation/
    piping_model_reconciliation/

  _Change/
    model_change_records/

  _Archive/
```

---

## 6. OpenPipeStress Tool Adapter Contract

The OpenPipeStress adapter should expose commands with strict input/output schemas.

### 6.1 `ops.validate_model`

Purpose:

Validate schema, units, topology, missing inputs, private-data references, and solve blockers.

Inputs:

```yaml
model_path: "PKG-01_PipingDesign/DEL-01-02_OpenPipeStressModel/OpenPipeStress/project.ops.yaml"
state_id: "STATE-0018" # optional
```

Outputs:

```text
validation_summary.json
validation_summary.md
warnings.md
blockers.md
```

### 6.2 `ops.summarize_model`

Purpose:

Generate Chirality-readable model summary.

Outputs:

```text
Model_Manifest.yaml
Model_Manifest.md
Model_Warnings.md
Model_Assumptions.md
```

### 6.3 `ops.list_states`

Purpose:

List available model states.

Outputs:

```text
states_index.yaml
states_index.md
```

### 6.4 `ops.list_runs`

Purpose:

List available analysis runs.

Outputs:

```text
runs_index.yaml
runs_index.md
```

### 6.5 `ops.run_analysis`

Purpose:

Run internal OpenPipeStress analysis on a selected model state.

Inputs:

```yaml
model_state_id: "STATE-0018"
analysis_settings_id: "default"
load_cases:
  - W
  - T1
  - D1
approval_ref: "optional-human-confirmation-reference"
```

Outputs:

```text
RUN-0052/
  analysis_run.yaml
  results_summary.md
  solver_diagnostics.md
  warnings.md
```

Notes:

- This is a domain-controlled write.
- It should not mutate the model state.
- It may require explicit user confirmation in Chirality depending on profile settings.

### 6.6 `ops.compare_states`

Purpose:

Compare two model states.

Inputs:

```yaml
model_state_a: "STATE-0012"
model_state_b: "STATE-0018"
mapping_table: "MAP-0009" # optional
tolerance_profile: "TOL-DEFAULT-001"
```

Outputs:

```text
CMP-0007/
  comparison.yaml
  comparison_summary.md
  changed_entities.csv
  unmatched_entities.csv
```

### 6.7 `ops.compare_runs`

Purpose:

Compare two analysis runs.

Inputs:

```yaml
analysis_run_a: "RUN-0041"
analysis_run_b: "RUN-0052"
mapping_table: "MAP-0009"
tolerance_profile: "TOL-DEFAULT-001"
```

Outputs:

```text
CMP-0008/
  comparison.yaml
  result_delta_table.csv
  comparison_summary.md
  out_of_tolerance.md
```

### 6.8 `ops.generate_handoff`

Purpose:

Generate a handoff package for downstream modeling or external professional stress-analysis validation.

Outputs:

```text
handoff/
  handoff_manifest.yaml
  Handoff_Manifest.md
  exported_model_file
  units_manifest.yaml
  entity_id_manifest.yaml
  warnings.md
  unresolved_assumptions.md
```

Notes:

- This is a domain-controlled write.
- It should require explicit user confirmation before generation or final packaging.

### 6.9 `ops.generate_report_fragment`

Purpose:

Produce report sections that Chirality may include in a larger deliverable package.

Outputs:

```text
report_fragments/
  analysis_summary.md
  warnings_and_assumptions.md
  comparison_summary.md
  professional_boundary_notice.md
```

### 6.10 `ops.validate_operation_proposal`

Purpose:

Validate a proposed model operation without applying it.

Inputs:

```yaml
proposal_path: "OpenPipeStress/proposals/PROP-0003_add_guide.yaml"
base_model_state: "STATE-0018"
```

Outputs:

```text
proposal_validation.yaml
proposal_validation.md
proposal_diff_preview.md
blockers.md
warnings.md
```

### 6.11 `ops.apply_operation_proposal`

Future only.

Purpose:

Apply a validated proposal through OpenPipeStress with explicit human approval.

Inputs:

```yaml
proposal_path: "OpenPipeStress/proposals/PROP-0003_add_guide.yaml"
base_model_state: "STATE-0018"
approval_ref: "human-approval-sha-or-record"
```

Outputs:

```text
new_model_state_id: "STATE-0019"
operation_application_record.yaml
operation_application_record.md
```

Notes:

- This must never be implemented as raw file mutation by an agent.
- It must go through OpenPipeStress validation and state creation.

---

## 7. Operation Proposal Schema

A minimal OpenPipeStress operation proposal should look like:

```yaml
operation_proposal:
  schema_version: "1.0"
  id: "PROP-0003"
  title: "Add guide support near rack bent 4"
  created_by: "chirality_agent"
  created_at: "2026-05-04T10:00:00-06:00"
  base_model_state: "STATE-0018"

  operation:
    type: "add_support"
    target_line: "P-1001"
    proposed_location:
      station: "42 ft"
    support_type: "guide"

  rationale:
    summary: "Reduce lateral displacement in thermal operating case."
    evidence:
      - type: "analysis_run"
        id: "RUN-0052"
      - type: "comparison"
        id: "CMP-0007"

  constraints_considered:
    - "rack_support_zone_A"
    - "clearance_zone_CZ-07"

  unresolved_assumptions:
    - "Final structural attachment details pending."
    - "Guide stiffness requires user confirmation."

  professional_boundary:
    status: "proposal_only"
    notice: "This proposal is not an accepted engineering change until reviewed and applied by the user through OpenPipeStress."
```

---

## 8. Chirality Agent Workflows

### 8.1 Model Review Workflow

```text
1. Agent calls ops.summarize_model.
2. Agent reads Model_Manifest.md, warnings, and assumptions.
3. Agent updates TBD_Register.md.
4. Agent drafts Review_Notes.md.
5. User reviews notes and decides actions.
```

### 8.2 Analysis Review Workflow

```text
1. User or agent requests ops.run_analysis.
2. OpenPipeStress creates an analysis run.
3. Agent summarizes solver diagnostics and warnings.
4. Agent drafts analysis review notes.
5. Human user evaluates engineering significance.
```

### 8.3 Comparison Workflow

```text
1. User selects State/Run A and State/Run B.
2. Chirality calls ops.compare_states or ops.compare_runs.
3. OpenPipeStress produces comparison records and delta tables.
4. Agent summarizes major deltas, unresolved issues, and suggested review questions.
5. User decides whether to modify the model.
```

### 8.4 External Prover Feedback Workflow

```text
1. User validates or reviews model in external professional stress software.
2. User records external review comments manually in Chirality or OpenPipeStress.
3. Agent turns comments into TBDs or operation proposals.
4. User applies changes through OpenPipeStress.
5. User saves new model state and reruns internal analysis.
6. User compares old and new states/runs.
```

### 8.5 Handoff Package Workflow

```text
1. User requests handoff package.
2. Chirality calls ops.generate_handoff.
3. OpenPipeStress generates handoff manifest and export files.
4. Agent drafts handoff checklist and export warnings summary.
5. User transfers package to downstream modeling/prover workflow.
```

---

## 9. Boundaries and Guardrails

### 9.1 Agents May Write

Only in permitted paths:

```text
operation proposals
review notes
TBD registers
draft report sections
handoff checklists
dependency entries
change records
reconciliation notes
```

### 9.2 Agents Must Not Directly Write

```text
OpenPipeStress project.ops.yaml
accepted model states
analysis run result files
comparison result files
handoff package internals
solver outputs
professional acceptance records
private rule packs
private component libraries
private material libraries
```

### 9.3 Domain Tools May Write

Only through declared domain-controlled operations:

```text
analysis runs
comparison records
handoff packages
report fragments
validation summaries
manifest outputs
```

### 9.4 Human Must Decide

Human review is required for:

```text
accepted model changes
external prover interpretation
professional reliance
final report issuance
code-compliance conclusions
construction/fabrication/operation decisions
private data release
```

---

## 10. Chirality Backlog Epics

### EP-C-DOM-001: Domain Engine Profile Schema

Implement a schema for domain profiles.

Deliverables:

```text
DOMAIN_ENGINE_PROFILE_SPEC.md
profile validation tool
OpenPipeStress example profile
tests for invalid profiles
```

### EP-C-DOM-002: Domain Tool Registry

Extend or wrap the deterministic tool registry for domain-engine tools.

Deliverables:

```text
domain tool registration
tool argument schemas
tool output schemas
tool invocation API
tool execution logging
```

### EP-C-DOM-003: Protected Path Guard

Add guardrails for protected domain paths.

Deliverables:

```text
protected path matcher
agent-writable path matcher
write-attempt validation
error messages
test fixtures
```

### EP-C-DOM-004: Domain Artifact Scanner

Scan working roots for domain artifacts.

Deliverables:

```text
domain artifact index
profile status summary
model/run/comparison/handoff discovery
UI read-only display
```

### EP-C-DOM-005: Operation Proposal Support

Allow agents to create and validate operation proposals.

Deliverables:

```text
proposal templates
proposal schema validation
proposal browser
validation tool invocation
review-note linkage
```

### EP-C-DOM-006: Domain Report and Boundary Checks

Support domain-specific report fragments and professional/IP boundary checks.

Deliverables:

```text
report fragment ingestion
professional boundary checker
private data leakage checker
protected-content warning workflow
```

---

## 11. OpenPipeStress Backlog Epics

### EP-OPS-CHIR-001: CLI Adapter

Create an OpenPipeStress CLI adapter with stable commands.

Deliverables:

```text
ops validate-model
ops summarize-model
ops list-states
ops list-runs
ops run-analysis
ops compare-states
ops compare-runs
ops generate-handoff
ops generate-report-fragment
ops validate-operation-proposal
```

### EP-OPS-CHIR-002: Chirality Artifact Layout

Define where generated summaries, manifests, reports, warnings, and proposals live.

Deliverables:

```text
OPENPIPESTRESS_CHIRALITY_ARTIFACT_LAYOUT.md
sample project root
sample model manifest
sample run summary
sample comparison summary
```

### EP-OPS-CHIR-003: Manifest and Summary Generators

Generate bounded outputs for agents.

Deliverables:

```text
Model_Manifest.yaml
Model_Manifest.md
RUN-*_summary.md
CMP-*_summary.md
Handoff_Manifest.md
warnings.md
assumptions.md
```

### EP-OPS-CHIR-004: Operation Proposal Schema

Define structured model operation proposal formats.

Deliverables:

```text
OPENPIPESTRESS_OPERATION_PROPOSAL_SCHEMA.yaml
proposal examples
validation command
diff preview command
```

### EP-OPS-CHIR-005: Human-Gated Proposal Application

Future.

Deliverables:

```text
proposal review UI
apply operation command
approval reference capture
new model state creation
operation application record
```

### EP-OPS-CHIR-006: Professional and IP Boundary Checks

Create deterministic checks for generated outputs.

Deliverables:

```text
professional-boundary language checker
private-data leakage checker
protected-content risk checker
report notice generator
```

---

## 12. Testing Plan

### 12.1 Chirality Tests

Add tests for:

```text
domain profile validation
protected path matching
agent-writable path matching
domain artifact scanning
tool invocation argument validation
tool output capture
failed tool behavior
proposal file validation
no direct writes to protected paths
```

### 12.2 OpenPipeStress Tests

Add tests for:

```text
CLI command success and failure paths
schema validation outputs
model summary determinism
state/run listing determinism
analysis run reproducibility
comparison determinism
handoff manifest completeness
proposal validation without model mutation
private-data redaction
professional-boundary notices
```

### 12.3 End-to-End Tests

Create fixture project:

```text
fixture_projects/open_pipe_stress_chirality_demo/
```

Test flow:

```text
1. Chirality scans working root.
2. Domain profile validates.
3. ops.summarize_model produces manifest.
4. Agent reads manifest and drafts review notes.
5. ops.run_analysis creates run summary.
6. ops.compare_runs creates delta table.
7. Agent drafts comparison summary.
8. ops.generate_handoff creates handoff manifest.
9. Chirality verifies protected paths were not directly modified by agents.
```

---

## 13. Implementation Sequence

### Phase 0: Confirm Scope and Create Specs

Owner: product/architecture

Deliverables:

```text
CHIRALITY-PRD-AMENDMENT-DOMAIN-ENGINES-001.md
DOMAIN_ENGINE_PROFILE_SPEC.md
OPENPIPESTRESS_CHIRALITY_PROFILE.yaml
OPENPIPESTRESS_CLI_ADAPTER_SPEC.md
```

Exit criteria:

- Domain engine integration is formally scoped.
- OpenPipeStress profile is drafted.
- Protected paths and agent-writable paths are defined.

### Phase 1: Build OpenPipeStress Read-Only Adapter

Owner: OpenPipeStress development

Deliverables:

```text
ops.validate_model
ops.summarize_model
ops.list_states
ops.list_runs
```

Exit criteria:

- Chirality can read model summaries without mutating model truth.

### Phase 2: Add Chirality Domain Profile Support

Owner: Chirality development

Deliverables:

```text
profile loader
profile validator
artifact scanner
tool registry entries
protected path guard
```

Exit criteria:

- Chirality can discover an OpenPipeStress project and list safe artifacts/tools.

### Phase 3: Add Analysis, Comparison, and Handoff Tool Calls

Owner: shared

Deliverables:

```text
ops.run_analysis
ops.compare_states
ops.compare_runs
ops.generate_handoff
domain tool invocation UI/API
tool output capture
```

Exit criteria:

- User can trigger deterministic OpenPipeStress outputs from Chirality without direct agent writes to canonical model truth.

### Phase 4: Add Agent Proposal Workflow

Owner: shared

Deliverables:

```text
operation proposal templates
proposal validation
proposal browser
review notes linkage
```

Exit criteria:

- Agents can propose model changes as files.
- OpenPipeStress can validate proposals.
- User remains the application/acceptance gate.

### Phase 5: Add Optional Deep-Link / Launch Support

Owner: shared

Deliverables:

```text
open model in OpenPipeStress
open state/run/comparison in OpenPipeStress
open proposal in OpenPipeStress
```

Exit criteria:

- User can move from Chirality review context into OpenPipeStress GUI quickly.

### Phase 6: Future External Result State Support

Owner: OpenPipeStress first, Chirality second

Deliverables:

```text
external result state schema
manual external result entry/import
comparison support
Chirality summary generation
```

Exit criteria:

- User can compare internal OpenPipeStress results against structured external result states without Chirality declaring professional validation.

---

## 14. Immediate Next Actions

1. Add the Chirality PRD amendment to the Chirality project documentation.
2. Draft `DOMAIN_ENGINE_PROFILE_SPEC.md`.
3. Draft `OPENPIPESTRESS_CHIRALITY_PROFILE.yaml`.
4. Draft `OPENPIPESTRESS_CLI_ADAPTER_SPEC.md`.
5. Implement read-only OpenPipeStress adapter commands first.
6. Implement Chirality profile validation and artifact scanning second.
7. Only then add analysis/comparison/handoff tool invocation.
8. Defer raw external prover parsing, formal prover status, and automatic approval workflows.

---

## 15. What Success Looks Like

A successful first integration lets a user do this:

```text
1. Select a Chirality working root.
2. Chirality detects an OpenPipeStress project.
3. User asks an agent to review the piping model state.
4. Agent calls deterministic OpenPipeStress summary tools.
5. Agent drafts review notes and TBDs from actual model warnings.
6. User runs or selects an analysis run.
7. Agent summarizes solver diagnostics and changed results.
8. User requests a handoff package.
9. OpenPipeStress generates the handoff package.
10. Chirality creates the handoff checklist and deliverable record.
11. Human user decides what to do next.
```

No agent fabricates engineering results. No agent directly edits canonical model truth. No software claims professional approval. The project record remains local, versioned, inspectable, and governed.

---

## 16. Guiding Statement

> Use Chirality to govern the work around OpenPipeStress. Use OpenPipeStress to perform and preserve the engineering model and analysis. Use the external professional tool for relied-upon validation. Use human judgment for acceptance.
