# PRD Amendment: Domain Engine Integration for Chirality App

**Document ID:** CHIRALITY-PRD-AMENDMENT-DOMAIN-ENGINES-001  
**Applies to:** `PRD_CHIRALITY_APP.md`  
**Primary example profile:** OpenPipeStress  
**Status:** Draft amendment  
**Prepared for:** Chirality App and OpenPipeStress integration planning  
**Purpose:** Extend Chirality App so it can safely orchestrate deterministic domain engines without becoming those engines.

---

## 1. Amendment Summary

This amendment adds a **Domain Engine Integration** capability to Chirality App.

Chirality remains a local-first desktop harness for governed agents, deliverables, filesystem-native project state, lifecycle records, dependency registers, deterministic tools, and human review. It does **not** become a domain-specific engineering application, solver, CAD tool, stress-analysis engine, or professional prover.

The amendment introduces a reusable integration pattern:

```text
Chirality App
  = governed agent/workflow/deliverable harness

Domain Engine
  = deterministic specialist software that owns its domain model and computation

Human Operator
  = accountable reviewer and decision authority
```

For OpenPipeStress specifically:

```text
Chirality orchestrates, documents, summarizes, reconciles, and governs.
OpenPipeStress owns the piping model, GUI, solver, model states, analysis runs, comparisons, and handoff packages.
The external professional stress tool validates for reliance.
The responsible engineer accepts.
```

This amendment is intended to support OpenPipeStress as the first concrete domain-engine integration while preserving Chirality’s generality for future domain tools.

---

## 2. Source Basis

This amendment is based on the following agreed product direction:

1. Chirality App’s existing PRD defines a local desktop harness for governed AI agents operating against a selected filesystem working root, with project truth stored in git-tracked files and human authority retained at gates.
2. OpenPipeStress v0.2 defines an analysis-grade piping design engine with a full analytical stress-analysis core, schema-backed physical model, model states, analysis runs, comparison records, and handoff packages.
3. The agreed integration model is federated rather than monolithic:
   - Chirality does not embed or replace OpenPipeStress.
   - OpenPipeStress does not become a general-purpose agent operating system.
   - Agents do not directly mutate canonical engineering model states.
   - Integration occurs through deterministic tools, manifests, operation proposals, summaries, reports, and human-gated workflows.

---

## 3. Product Decision

Add support for **Domain Engine Profiles** and **Domain Tool Adapters**.

A Domain Engine Profile tells Chirality:

- what domain engine is present;
- which files are authoritative domain artifacts;
- which files are generated summaries or manifests;
- which paths are protected from direct agent writes;
- which paths agents may write to;
- which deterministic tools are available;
- which tool outputs are safe for agents to read;
- which human gates are required before changes become accepted project state.

A Domain Tool Adapter exposes deterministic commands from a domain engine to Chirality. The adapter may validate models, summarize model state, run analysis, compare states, produce report fragments, or generate handoff manifests. It must not allow agents to bypass domain-engine validation or human authority.

---

## 4. Definitions

### 4.1 Domain Engine

A domain engine is specialist software that owns domain-specific models, calculations, validation, and graphical or technical workflows.

Examples:

- OpenPipeStress for piping design and stress-analysis model authoring;
- a future electrical load-flow engine;
- a future structural frame-analysis engine;
- a future process simulation engine;
- a future schedule/cost engine.

### 4.2 Domain Engine Profile

A structured configuration that describes how Chirality may discover, read, invoke, summarize, and govern a domain engine inside a working root.

### 4.3 Domain Tool Adapter

A deterministic command-line or API surface provided by the domain engine and callable by Chirality.

### 4.4 Authoritative Domain Artifact

A file or folder that represents domain truth owned by the domain engine. Agents must not directly edit these artifacts unless the domain profile explicitly permits a narrow safe action.

For OpenPipeStress, examples include:

```text
project.ops.yaml
states/
runs/
comparisons/
handoff/
canonical model files
analysis result files
```

### 4.5 Chirality-Readable Artifact

A summary, manifest, report fragment, warning list, assumption register, delta table, or checklist that Chirality agents may read, summarize, reconcile, or cite.

### 4.6 Agent-Writable Artifact

A file that agents may create or modify under explicit write scope. Examples include:

```text
operation proposals
review notes
TBD registers
draft report sections
handoff checklists
dependency registers
reconciliation notes
```

### 4.7 Protected Write Path

A path that agents may not directly modify. Changes to protected domain artifacts must occur only through the domain engine, a deterministic adapter command, or an explicitly human-approved operation.

### 4.8 Operation Proposal

A structured proposed domain-model change. An operation proposal is not accepted model truth. It is a draft artifact for human review and domain-engine validation.

---

## 5. Amendment to Chirality Product Goals

Add the following product goal:

> Support local deterministic domain-engine integrations through file-based profiles, tool adapters, manifests, protected write paths, and human-gated operation proposals, while preserving Chirality’s role as a governed agent harness rather than a domain computation engine.

This goal extends Chirality’s current deterministic tool registry and filesystem-native project truth model.

---

## 6. Amendment to Non-Goals

Add the following non-goals:

Chirality must not:

1. Become a domain-specific engineering solver, CAD system, piping stress analysis program, or professional validation/prover tool.
2. Directly edit canonical domain-engine model states unless the domain engine profile explicitly exposes a safe deterministic operation and the required human gate is satisfied.
3. Treat agent-generated domain advice as accepted engineering work.
4. Declare domain-specific professional acceptance, code compliance, certification, sealing, or approval.
5. Parse or normalize proprietary third-party engineering software outputs unless a specific adapter is separately scoped, implemented, and validated.
6. Store authoritative domain truth in hidden chat state, transient session memory, vendor systems, or untracked UI state.
7. Bypass the domain engine’s schema validation, solver validation, or professional-boundary notices.

---

## 7. Amendment to Product Principles

Add the following product principles.

### 7.1 Domain Engines Own Domain Truth

When a domain engine is integrated, Chirality may orchestrate, summarize, and govern work around it, but the domain engine remains the owner of its canonical model and calculation records.

### 7.2 Agents Propose; Domain Tools Validate; Humans Accept

Agents may draft operation proposals, review notes, and summaries. Domain-engine tools validate and compute. Humans accept or reject changes and decide what can be relied upon.

### 7.3 Deterministic Tools Over Agent Interpretation

Agents must not improvise domain results. They must rely on deterministic tool outputs, manifests, logs, reports, and explicitly cited project files.

### 7.4 Protected Domain Paths Are Write-Quarantined

Canonical domain model files, model states, analysis runs, result files, comparison records, and handoff packages are protected unless the domain profile permits a specific deterministic write path.

### 7.5 Manifests Make Domain State Legible

Every domain-engine integration should generate bounded, human-readable and machine-readable artifacts so Chirality can reason about domain work without needing to own domain internals.

---

## 8. Scope Additions

### 8.1 In Scope

The following are added to Chirality scope when this amendment is adopted:

- Domain Engine Profile registry.
- Domain Tool Adapter discovery.
- Domain artifact scanning inside the working root.
- Profile-defined protected write paths.
- Profile-defined agent-writable paths.
- Deterministic invocation of approved domain tools.
- Domain tool result capture as bounded summaries, manifests, CSVs, Markdown files, and JSON/YAML records.
- Agent creation of operation proposals and review notes.
- Human-gated application of domain operations.
- Domain-specific professional-boundary notices.
- Domain-specific IP/data-boundary review checklists where applicable.

### 8.2 Out of Scope Unless Separately Approved

The following remain out of scope unless separately amended:

- Embedding the OpenPipeStress 3D GUI inside Chirality.
- Implementing the OpenPipeStress solver inside Chirality.
- Directly editing OpenPipeStress canonical model-state files from agents.
- Parsing CAESAR II, AutoPIPE, or other commercial stress-analysis result files.
- Declaring external prover validation complete.
- Issuing professional approval, code compliance, or ready-for-construction status.
- Network-based vendor integrations outside Chirality’s approved network policy.
- Cloud storage of domain model truth.

---

## 9. Functional Requirements Added by This Amendment

Priority definitions follow the Chirality PRD:

- `P0`: required for safe/useful current capability if domain integration is included.
- `P1`: important for quality, governance, or adoption.
- `P2`: desirable or future hardening.

| ID | Priority | Requirement | Acceptance Criteria |
|---|---:|---|---|
| FR-DOM-001 | P0 | Chirality shall support a Domain Engine Profile schema. | A profile can declare engine name, version, root paths, authoritative artifacts, readable artifacts, protected write paths, agent-writable paths, deterministic tools, and required human gates. |
| FR-DOM-002 | P0 | Chirality shall validate domain profiles before use. | Invalid profiles fail with typed errors; profile validation does not silently downgrade protected paths. |
| FR-DOM-003 | P0 | Chirality shall distinguish authoritative domain artifacts from Chirality-readable artifacts. | UI and agent context identify which files are domain truth and which are summaries, drafts, or manifests. |
| FR-DOM-004 | P0 | Chirality shall enforce protected domain write paths at tool-invocation and agent-write boundaries where implemented. | Agents cannot directly write protected model-state, analysis-run, comparison, or handoff paths through Chirality-managed writes. |
| FR-DOM-005 | P0 | Chirality shall allow agents to write only profile-permitted proposal/review paths. | Operation proposals, review notes, TBD registers, and report drafts are allowed only in configured agent-writable paths. |
| FR-DOM-006 | P0 | Domain tool calls shall be deterministic and bounded. | Tool output is structured, size-limited, logged, and does not rely on hidden app state for authoritative project truth. |
| FR-DOM-007 | P0 | Domain tool results shall be captured as project files when they affect project reasoning. | Summaries, manifests, warnings, deltas, or report fragments are written under the working root, not hidden in chat only. |
| FR-DOM-008 | P1 | Chirality shall expose domain artifacts in working-root scans. | Domain projects, states, runs, comparisons, handoff packages, and generated summaries are discoverable in the UI. |
| FR-DOM-009 | P1 | Chirality shall expose approved domain tools through the existing deterministic tool registry or an equivalent domain-tool registry. | Agents can invoke only declared tools with declared input/output contracts. |
| FR-DOM-010 | P1 | Chirality shall support operation proposal files. | Agents can create structured proposals that a domain engine may later validate, preview, and apply with human approval. |
| FR-DOM-011 | P1 | Chirality shall support human approval metadata for domain operation application where tool-supported. | Applied operations can bind to approval reference, user identity where available, timestamp, source proposal, and resulting domain artifact hash. |
| FR-DOM-012 | P1 | Chirality shall support domain professional-boundary notices. | Domain summaries and reports can include required language prohibiting automated certification, sealing, approval, or professional reliance. |
| FR-DOM-013 | P1 | Chirality shall support domain IP/data-boundary checks where a profile defines them. | Agents and tools can flag protected-content risk, private-data leakage risk, and missing provenance. |
| FR-DOM-014 | P2 | Chirality shall support domain profile UI panels. | Users can inspect profile status, protected paths, available tools, latest summaries, warnings, and proposals. |
| FR-DOM-015 | P2 | Chirality shall support launch/deep-link actions into domain applications where supported. | Users can open a domain model in its native GUI without Chirality becoming the GUI. |
| FR-DOM-016 | P2 | Chirality shall support future external result states as domain-readable artifacts. | External results can be represented as structured artifacts and compared by the domain engine without Chirality declaring professional validation. |

---

## 10. API Additions

The following API additions are proposed. Endpoint names are provisional.

| Endpoint | Method | Purpose |
|---|---|---|
| `/api/domain/profiles/list` | GET | List domain profiles available in the working root and bundled instruction root. |
| `/api/domain/profile/validate` | POST | Validate a domain engine profile. |
| `/api/domain/artifacts/scan` | GET | Scan the selected working root for domain-engine artifacts declared by active profiles. |
| `/api/domain/tool/invoke` | POST | Invoke a declared deterministic domain tool with validated arguments. |
| `/api/domain/proposals/list` | GET | List operation proposals for a selected domain engine. |
| `/api/domain/proposal/validate` | POST | Validate an operation proposal against profile schema and, where available, domain-engine validation. |

Any endpoint that writes or mutates authoritative domain artifacts must be separately reviewed and must respect human-gate requirements.

---

## 11. Domain Engine Profile Shape

A minimal profile should resemble:

```yaml
domain_profile:
  schema_version: "1.0"
  id: "open_pipe_stress"
  name: "OpenPipeStress"
  engine_type: "piping_design_and_stress_model_authoring"
  profile_version: "0.1"

  domain_root_patterns:
    - "OpenPipeStress/"
    - "**/OpenPipeStress/"

  authoritative_artifacts:
    - "OpenPipeStress/project.ops.yaml"
    - "OpenPipeStress/states/**"
    - "OpenPipeStress/runs/**"
    - "OpenPipeStress/comparisons/**"
    - "OpenPipeStress/handoff/**"

  chirality_readable_artifacts:
    - "Model_Manifest.md"
    - "Model_Manifest.yaml"
    - "RUN-*_summary.md"
    - "CMP-*_summary.md"
    - "CMP-*_delta_table.csv"
    - "Handoff_Manifest.md"
    - "Export_Warnings.md"
    - "TBD_Register.md"

  protected_write_paths:
    - "OpenPipeStress/project.ops.yaml"
    - "OpenPipeStress/states/**"
    - "OpenPipeStress/runs/**"
    - "OpenPipeStress/comparisons/**"
    - "OpenPipeStress/handoff/**"

  agent_writable_paths:
    - "OpenPipeStress/proposals/**"
    - "Review_Notes.md"
    - "TBD_Register.md"
    - "Draft_Report_Sections/**"

  deterministic_tools:
    - id: "ops.validate_model"
      mode: "read_only"
    - id: "ops.summarize_model"
      mode: "read_only"
    - id: "ops.list_states"
      mode: "read_only"
    - id: "ops.list_runs"
      mode: "read_only"
    - id: "ops.run_analysis"
      mode: "domain_controlled_write"
      requires_human_confirmation: true
    - id: "ops.compare_states"
      mode: "domain_controlled_write"
      requires_human_confirmation: false
    - id: "ops.compare_runs"
      mode: "domain_controlled_write"
      requires_human_confirmation: false
    - id: "ops.generate_handoff"
      mode: "domain_controlled_write"
      requires_human_confirmation: true
    - id: "ops.generate_report_fragment"
      mode: "read_only_or_summary_write"
    - id: "ops.check_boundary_language"
      mode: "read_only"
    - id: "ops.check_private_data_boundary"
      mode: "read_only"

  professional_boundary:
    agent_must_not_claim:
      - "code compliant for reliance"
      - "professionally approved"
      - "certified"
      - "sealed"
      - "ready for construction"
      - "external prover validated unless supplied as external human record"
```

---

## 12. OpenPipeStress as the First Domain Engine Profile

### 12.1 Integration Intent

OpenPipeStress should be integrated as a domain engine that provides:

- model validation;
- model summarization;
- state/run enumeration;
- internal analysis runs;
- deterministic comparisons;
- operation proposals;
- handoff package generation;
- report fragments;
- IP/data-boundary checks;
- professional-boundary language checks.

### 12.2 Chirality Should Read

Chirality may read:

```text
model manifests
state summaries
analysis-run summaries
warning lists
assumption registers
comparison summaries
delta tables
handoff manifests
draft report fragments
operation proposals
review notes
TBD registers
```

### 12.3 Chirality Should Not Directly Write

Chirality agents must not directly write:

```text
canonical OpenPipeStress project files
accepted model states
analysis run result records
comparison result records
handoff package internals
solver outputs
professional acceptance records
```

### 12.4 Chirality May Write

Chirality agents may write, if inside declared agent-writable paths:

```text
operation proposals
review notes
TBD registers
scope notes
handoff checklists
draft report sections
dependency register entries
change records
reconciliation notes
```

---

## 13. Suggested Working-Root Layout for OpenPipeStress Projects

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

## 14. Agent Behavior Rules for Domain Engines

Agents operating under a domain profile must follow these rules:

1. Do not fabricate domain results.
2. Do not directly mutate protected domain artifacts.
3. Do not invent missing engineering data.
4. Treat unknowns as `TBD`.
5. Use deterministic tool outputs as evidence.
6. Cite model state IDs, run IDs, comparison IDs, manifest hashes, and file paths where available.
7. Write proposals, not accepted changes.
8. Preserve professional-boundary language.
9. Preserve IP/data-boundary language.
10. Request or record human review when a proposed action would affect relied-upon project state.

---

## 15. Validation Requirements for This Amendment

When implemented, the Domain Engine Integration feature should be tested for:

- profile schema validation;
- protected path recognition;
- safe tool invocation;
- invalid tool argument rejection;
- write-scope enforcement;
- proposal file creation;
- rejection of direct writes to protected domain artifacts;
- handling of missing domain engine executable;
- handling of invalid domain model;
- handling of large domain outputs;
- redaction of private data in generated summaries;
- professional-boundary language checks;
- deterministic output for repeated tool calls.

---

## 16. Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---:|---|
| Agents directly modify engineering model truth | High | Protected write paths, deterministic tools, operation proposals, human gates. |
| Chirality is mistaken for a domain solver | High | Product language says Chirality orchestrates and governs; domain engine computes. |
| Agent summaries misrepresent technical results | High | Require deterministic tool outputs, bounded summaries, citations to manifests/runs/comparisons. |
| Domain tools expose private data to chat unnecessarily | High | Redaction, summary controls, private-data boundary checks. |
| Operation proposals are mistaken for accepted model changes | Medium/High | Label proposals clearly; accepted changes must be applied by domain engine with human approval. |
| Professional status labels imply approval | High | Prohibit automatic code-compliant, certified, approved, ready-for-construction labels. |
| Domain profile overfits to OpenPipeStress | Medium | Define generic Domain Engine Profile with OpenPipeStress as first example. |
| Integration expands current release scope too much | Medium | Treat as amendment/future scope unless explicitly added to a release decomposition. |

---

## 17. Release Strategy

This amendment should be implemented in stages.

### Stage A: Specification Only

Deliverables:

- this amendment;
- `DOMAIN_ENGINE_PROFILE_SPEC.md`;
- OpenPipeStress example profile;
- path/write-boundary policy;
- operation proposal schema.

### Stage B: Read-Only Domain Awareness

Deliverables:

- profile validation;
- artifact scanning;
- manifest ingestion;
- read-only tool invocation;
- agent access to generated summaries.

### Stage C: Domain-Controlled Tool Invocation

Deliverables:

- approved tool invocation registry;
- deterministic result capture;
- analysis-run and comparison generation through the domain adapter;
- write outputs only through domain-controlled tools.

### Stage D: Operation Proposal Workflow

Deliverables:

- proposal authoring;
- proposal validation;
- diff preview where domain tool supports it;
- human approval metadata;
- optional apply operation through domain engine, not through raw agent writes.

### Stage E: Deeper UI Convenience

Deliverables:

- profile status panel;
- launch/open-in-domain-app actions;
- proposal browser;
- domain artifact summary dashboard.

---

## 18. Chirality PRD Text Insertions

### 18.1 Add to Product Summary

Add:

> Chirality may integrate with deterministic domain engines through explicit domain profiles and tool adapters. In such integrations, Chirality governs agent work, deliverables, manifests, review notes, and human gates, while the domain engine owns domain-specific model truth and computation.

### 18.2 Add to In Scope

Add:

> Domain Engine Profile support for local deterministic specialist tools, including profile validation, protected write paths, agent-writable proposal paths, domain tool invocation, and generated manifests/summaries.

### 18.3 Add to Out of Scope

Add:

> Chirality does not become the domain engine. It does not directly solve, certify, approve, or professionally validate domain-specific engineering work, and it does not allow agents to directly modify protected domain model artifacts.

### 18.4 Add to Known Gaps and Risks

Add:

| ID | Area | Risk / Gap | Product Decision |
|---|---|---|---|
| KG-DOM-001 | Domain engines | Chirality does not yet have a formal profile schema for domain-engine integrations. | Add Domain Engine Profile support before integrating OpenPipeStress beyond manual file-based workflows. |
| KG-DOM-002 | Protected domain writes | Current write quarantine may not be sufficient for canonical engineering model files. | Domain integrations must define protected write paths and agent-writable proposal paths. |
| KG-DOM-003 | Domain tool outputs | Agent summaries can misrepresent technical results if not grounded in deterministic tool outputs. | Domain agents must rely on manifests, summaries, hashes, run IDs, and deterministic tool outputs. |
| KG-DOM-004 | Professional reliance | Domain integrations can create false impression of engineering approval. | Domain profiles must carry professional-boundary language and prohibit automatic approval/code-compliance labels. |

---

## 19. Acceptance Criteria for Amendment Adoption

This amendment is adopted when:

1. The Chirality PRD includes domain-engine integration as an explicit future or active scope item.
2. A Domain Engine Profile schema exists.
3. OpenPipeStress has a draft profile using that schema.
4. Protected write paths and agent-writable paths are clearly defined.
5. The PRD states that Chirality does not become the domain solver or professional prover.
6. The PRD states that domain operations require deterministic tools and human gates.
7. Future implementation work can be decomposed into profile validation, artifact scanning, tool invocation, and proposal workflows.

---

## 20. Guiding Statement

The guiding statement for this amendment is:

> Chirality is the governed professional-work harness. Domain engines are the deterministic specialist tools. Agents create proposals and organize evidence. Humans decide what can be relied upon.
