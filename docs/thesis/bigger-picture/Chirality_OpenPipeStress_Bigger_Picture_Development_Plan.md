# Development Plan: Chirality + OpenPipeStress + Domain Engine Ecosystem

**Document ID:** CHIRALITY-DOMAIN-ENGINE-ECOSYSTEM-DEVPLAN-001  
**Status:** Draft development plan  
**Prepared for:** Chirality App, OpenPipeStress, and future deterministic domain-engine integrations  
**Purpose:** Define the bigger-picture development path that connects governed AI agents, deterministic engineering engines, local project truth, professional review, and external validation tools.

---

## 1. Executive Summary

This development plan treats Chirality App and OpenPipeStress as parts of a larger professional-engineering software ecosystem.

The ecosystem is not a single monolithic application. It is a layered system:

```text
Chirality App
  = governed professional-work harness and agent operating layer

Domain Engine Framework
  = profile, tool-adapter, artifact, write-boundary, and operation-proposal layer

OpenPipeStress
  = first deterministic domain engine: piping design, model authoring, and stress-analysis core

External Professional Prover Tools
  = industry-accepted validation tools used outside the design engine

Human Professional / Responsible Reviewer
  = final authority for project reliance
```

The guiding architecture is:

> **Agents propose and organize. Domain engines compute and preserve model truth. External tools validate for reliance. Humans accept. Git-tracked files remember.**

The first concrete use case is OpenPipeStress. But the bigger picture is broader: Chirality should become the governed operating layer for many deterministic professional domain engines, not just piping stress analysis.

---

## 2. Core Strategic Thesis

Professional AI systems should not replace deterministic engineering engines or professional judgment. They should coordinate them.

The combined system should make professional work faster and more traceable by ensuring that:

1. project truth lives in local, versioned files;
2. domain truth lives in deterministic domain engines;
3. agents operate through explicit scopes, tools, proposals, and manifests;
4. unknowns become `TBD`, not guesses;
5. computations come from deterministic tools, not agent improvisation;
6. professional reliance remains a human and project-authority act;
7. external prover tools remain authoritative where the industry requires them.

For OpenPipeStress, the key chain is:

```text
Design basis
  -> design knowledge
  -> schema-backed piping model
  -> internal stress-analysis run
  -> model-state / analysis-run comparison
  -> handoff package
  -> external professional stress tool
  -> human interpretation
  -> revised OpenPipeStress model state
  -> comparison and report package
```

For Chirality, the key chain is:

```text
Scope
  -> packages
  -> deliverables
  -> dependencies
  -> agent work
  -> deterministic tool outputs
  -> review notes
  -> human gates
  -> git-tracked project record
```

The ecosystem works when these two chains are connected through files, manifests, adapters, and human-gated operations.

---

## 3. System Roles and Boundaries

### 3.1 Chirality App Role

Chirality is responsible for:

- working-root selection;
- project scaffolding;
- agent orchestration;
- package and deliverable structure;
- dependency registers;
- lifecycle records;
- review notes;
- assumption and TBD registers;
- deterministic tool invocation;
- generated summaries and report drafts;
- human gate support;
- git-trackable project memory.

Chirality is not responsible for:

- solving piping stress models;
- owning the OpenPipeStress canonical model;
- approving engineering work;
- declaring code compliance;
- parsing proprietary third-party engineering results unless separately scoped;
- replacing domain tools.

### 3.2 Domain Engine Framework Role

The Domain Engine Framework is the bridge between Chirality and deterministic specialist software.

It is responsible for:

- domain engine profile schema;
- artifact discovery;
- protected path declarations;
- agent-writable path declarations;
- deterministic tool adapter contracts;
- tool invocation logging;
- operation proposal schema;
- generated summary and manifest conventions;
- professional-boundary and IP/data-boundary checks.

It is not a solver. It is not a domain application. It is an integration contract.

### 3.3 OpenPipeStress Role

OpenPipeStress is responsible for:

- schema-backed physical piping model;
- analytical model transformation;
- full internal piping flexibility/stress analytical engine;
- 3D GUI and model editing;
- model states;
- analysis runs;
- generic model-state and analysis-run comparisons;
- rule-pack evaluation using user-supplied data;
- handoff packages;
- deterministic summaries and reports;
- operation proposal validation;
- professional and IP/data boundary notices.

OpenPipeStress is not responsible for:

- being a general-purpose agent OS;
- becoming the project’s full deliverable-management layer;
- claiming industry-standard professional validation by itself;
- replacing external professional stress-analysis prover tools;
- accepting or sealing engineering work.

### 3.4 External Prover Tool Role

External professional stress-analysis tools are responsible for project validation when the organization or project requires accepted industry software.

They are not controlled by Chirality or OpenPipeStress in the near-term MVP.

Near-term workflow is human-mediated:

```text
OpenPipeStress handoff package
  -> user loads/recreates model in external tool
  -> user interprets external results
  -> user updates OpenPipeStress model
  -> OpenPipeStress compares model states/runs
  -> Chirality records review notes and deliverables
```

### 3.5 Human Professional Role

The human professional or accountable reviewer is responsible for:

- deciding what is correct for the project;
- accepting or rejecting agent proposals;
- accepting or rejecting model changes;
- interpreting external prover results;
- issuing or approving deliverables where appropriate;
- ensuring licensed standards, project basis, and owner requirements are applied correctly.

---

## 4. Program Architecture

### 4.1 Layered Architecture

```text
┌─────────────────────────────────────────────────────────┐
│ Human Professional / Responsible Reviewer                │
│ - judgment                                               │
│ - acceptance                                             │
│ - external validation interpretation                     │
│ - project authority                                      │
└───────────────────────────────▲─────────────────────────┘
                                │
┌───────────────────────────────┴─────────────────────────┐
│ Chirality App                                             │
│ - governed agent harness                                  │
│ - working-root/project structure                          │
│ - deliverables and dependency records                     │
│ - review notes, TBDs, reports                             │
│ - deterministic tool calls                                │
└───────────────────────────────▲─────────────────────────┘
                                │
┌───────────────────────────────┴─────────────────────────┐
│ Domain Engine Framework                                  │
│ - profiles                                                │
│ - adapters                                                │
│ - protected paths                                         │
│ - agent-writable paths                                    │
│ - operation proposals                                     │
│ - manifests and summaries                                 │
└───────────────────────────────▲─────────────────────────┘
                                │
┌───────────────────────────────┴─────────────────────────┐
│ OpenPipeStress                                            │
│ - piping physical model                                   │
│ - analytical model                                        │
│ - solver                                                  │
│ - GUI                                                     │
│ - states, runs, comparisons                               │
│ - handoff packages                                        │
└───────────────────────────────▲─────────────────────────┘
                                │
┌───────────────────────────────┴─────────────────────────┐
│ External Professional Prover Tools                        │
│ - accepted stress-analysis validation                     │
│ - project reliance workflow                               │
└─────────────────────────────────────────────────────────┘
```

### 4.2 Data and Control Flow

```text
Chirality creates project/deliverable structure
  ↓
OpenPipeStress creates/owns domain model
  ↓
OpenPipeStress generates manifests and summaries
  ↓
Chirality agents review summaries and propose actions
  ↓
OpenPipeStress validates proposed operations
  ↓
Human accepts/rejects proposed changes
  ↓
OpenPipeStress creates new model states/runs/comparisons
  ↓
Chirality records review notes, TBDs, reports, handoff checklists
  ↓
External prover validation occurs outside the system
  ↓
Human feeds conclusions back into project record
```

### 4.3 Governing Rule

No agent should ever be the source of accepted engineering truth.

Agents may create:

```text
drafts
summaries
review notes
operation proposals
TBD registers
dependency rows
handoff checklists
report fragments
```

Agents must not directly create:

```text
accepted model states
solver results
professional approval
code-compliance conclusions
external-prover validation status
signed or sealed records
```

---

## 5. Development Program Phases

The development program should proceed in ten phases.

Each phase has a distinct purpose and exit gate. The phases are not merely feature releases; they are risk-management steps.

---

# Phase 0: Product Alignment and Governance Baseline

## Objective

Lock the shared vision before building integration code.

## Build / Produce

- `CHIRALITY_PRD_Amendment_Domain_Engine_Integration.md`
- `Chirality_OpenPipeStress_Integration_Plan.md`
- this development plan
- OpenPipeStress v0.2 PRD alignment note
- source-basis map across Chirality, OpenPipeStress, IP/data policy, and professional-boundary policy

## Key Decisions

- Chirality is the governed work harness.
- OpenPipeStress is the first deterministic domain engine.
- The integration is federated, not monolithic.
- Domain engines own canonical domain artifacts.
- Agents create proposals and summaries, not accepted engineering changes.
- Human gates remain mandatory for reliance.

## Exit Criteria

- Project owner accepts this architecture.
- Chirality PRD amendment is adopted or marked as pending adoption.
- OpenPipeStress PRD recognizes Chirality integration as an external/domain profile pathway.
- Non-goals are explicit and visible.

---

# Phase 1: Domain Engine Framework Specification

## Objective

Define the general integration layer once, so OpenPipeStress does not become a one-off hack.

## Chirality Work

Create:

```text
DOMAIN_ENGINE_PROFILE_SPEC.md
DOMAIN_TOOL_ADAPTER_SPEC.md
DOMAIN_WRITE_BOUNDARY_POLICY.md
DOMAIN_OPERATION_PROPOSAL_SPEC.md
DOMAIN_ARTIFACT_MANIFEST_SPEC.md
DOMAIN_BOUNDARY_NOTICE_SPEC.md
```

## OpenPipeStress Work

Create:

```text
OPENPIPESTRESS_CHIRALITY_PROFILE.yaml
OPENPIPESTRESS_CHIRALITY_ARTIFACT_LAYOUT.md
OPENPIPESTRESS_CLI_ADAPTER_SPEC.md
OPENPIPESTRESS_OPERATION_PROPOSAL_SCHEMA.yaml
```

## Acceptance Criteria

- A domain profile can declare:
  - authoritative artifacts;
  - Chirality-readable artifacts;
  - protected write paths;
  - agent-writable paths;
  - deterministic tools;
  - professional-boundary phrases;
  - IP/data-boundary constraints.
- The OpenPipeStress profile validates against the general domain profile schema.
- The profile makes it clear which artifacts agents may and may not touch.

## Exit Gate

The framework can describe OpenPipeStress without embedding piping-specific logic in Chirality core.

---

# Phase 2: OpenPipeStress Foundational Engine

## Objective

Build enough OpenPipeStress core functionality for the domain engine to be real, not just an integration shell.

## OpenPipeStress Work

Implement:

```text
canonical project schema
unit system
schema-backed physical model
physical-to-analytical transformation
3D nodes with six degrees of freedom
straight pipe/beam elements
rigid elements
basic supports/restraints
weight and thermal loads
imposed displacements
linear static solver
force/moment recovery
fundamental stress recovery
solver diagnostics
local-first project storage
```

## Chirality Work

No deep integration yet. Chirality may only store planning artifacts and review notes.

## Acceptance Criteria

- OpenPipeStress can solve benchmark models deterministically.
- Schema round-trips without data loss.
- Solver results bind to explicit model inputs.
- Missing data and solver blockers are visible.
- No protected standards data is bundled.

## Exit Gate

OpenPipeStress has a credible deterministic core before Chirality agents begin reasoning around it.

---

# Phase 3: Model States, Analysis Runs, and Comparison

## Objective

Make OpenPipeStress outputs auditable, repeatable, and comparable.

## OpenPipeStress Work

Implement:

```text
named immutable model states
analysis runs attached to model states
analysis-run metadata
result hashes
model-state hashes
generic model-state comparison
generic analysis-run comparison
stable ID mapping
manual mapping support
tolerance profiles
comparison reports
```

## Chirality Work

Prepare for read-only consumption of:

```text
Model_Manifest.md
RUN-*_summary.md
CMP-*_summary.md
delta tables
warning lists
assumption registers
```

## Acceptance Criteria

- Same state + same solver version + same settings yields reproducible run metadata.
- Two states can be compared deterministically.
- Two runs can be compared deterministically.
- Comparison outputs are suitable for human and agent review.
- The comparison tool does not imply external validation or professional approval.

## Exit Gate

The domain engine can generate the core artifacts that Chirality agents need to summarize and reason about safely.

---

# Phase 4: Chirality Read-Only Domain Awareness

## Objective

Let Chirality discover and read OpenPipeStress artifacts without writing domain truth.

## Chirality Work

Implement:

```text
domain profile loader
domain profile validator
domain artifact scanner
protected path recognition
read-only domain tool registry
domain artifact UI display
agent context injection for domain summaries
```

## OpenPipeStress Work

Implement read-only adapter commands:

```text
ops.validate_model
ops.summarize_model
ops.list_states
ops.list_runs
ops.list_comparisons
ops.check_private_data_boundary
ops.check_professional_boundary_language
```

## Acceptance Criteria

- Chirality can detect an OpenPipeStress project inside a working root.
- Chirality can show model states, runs, comparisons, warnings, and manifests.
- Agents can summarize actual OpenPipeStress-generated summaries.
- Agents cannot directly write protected domain artifacts.
- If OpenPipeStress is missing or invalid, Chirality reports this without pretending to know the domain state.

## Exit Gate

Chirality can safely support OpenPipeStress review workflows without changing the engineering model.

---

# Phase 5: Domain-Controlled Analysis, Comparison, and Handoff Invocation

## Objective

Allow Chirality to request deterministic OpenPipeStress outputs through approved tools.

## Chirality Work

Implement:

```text
domain tool invocation API
tool argument validation
tool output capture
tool invocation logging
human confirmation prompts for high-impact tools
domain result file indexing
```

## OpenPipeStress Work

Implement write-producing adapter commands:

```text
ops.run_analysis
ops.compare_states
ops.compare_runs
ops.generate_handoff
ops.generate_report_fragment
```

## Safety Rule

These are domain-controlled writes. They are not agent writes.

## Acceptance Criteria

- A user can trigger an OpenPipeStress analysis run through Chirality.
- OpenPipeStress creates the run record, not the agent.
- A user can trigger comparison generation through Chirality.
- OpenPipeStress creates comparison records and delta tables.
- A user can generate a handoff package.
- Chirality records summaries and checklist artifacts.
- Protected canonical domain files remain controlled by OpenPipeStress.

## Exit Gate

Chirality can orchestrate deterministic domain work while preserving domain ownership.

---

# Phase 6: Agent Review and Operation Proposal Workflow

## Objective

Let agents become useful design assistants without letting them directly mutate models.

## Chirality Work

Implement:

```text
operation proposal templates
proposal authoring support
proposal browser
proposal-to-review-note linkage
TBD extraction from proposal blockers
proposal lifecycle metadata
```

## OpenPipeStress Work

Implement:

```text
ops.validate_operation_proposal
proposal schema validation
proposal diff preview
proposal warnings/blockers
proposal rationale capture
```

## Future OpenPipeStress Work

Later implement:

```text
ops.apply_operation_proposal
human approval capture
new model state creation
operation application record
```

## Acceptance Criteria

- Agents can draft operation proposals.
- OpenPipeStress can validate proposals without mutating the model.
- Users can inspect proposed changes and blockers.
- Invalid proposals do not become model changes.
- Accepted changes, when implemented, create new model states through OpenPipeStress only.
- Agent output is clearly marked as proposal-only.

## Exit Gate

Agents can participate in design iteration safely.

---

# Phase 7: OpenPipeStress GUI + Chirality Review Loop

## Objective

Make the human workflow smooth across both applications.

## OpenPipeStress Work

Implement or mature:

```text
3D GUI model editing
model tree
property inspector
operation history
state/run browser
comparison browser
warning panel
constraint panel
proposal review UI
handoff package UI
```

## Chirality Work

Implement:

```text
open-in-domain-app actions
deep links where supported
domain dashboard
proposal list panel
review note generation
deliverable package generation
```

## Acceptance Criteria

A user can:

1. review an issue in Chirality;
2. open the relevant OpenPipeStress model/state/run;
3. modify the model in the OpenPipeStress GUI;
4. save a new model state;
5. run analysis;
6. compare before/after;
7. return to Chirality to update review notes and deliverables.

## Exit Gate

The integrated workflow feels like one governed professional process, even though the applications remain distinct.

---

# Phase 8: External Prover Handoff Workflow

## Objective

Support the real professional validation workflow without overbuilding proprietary integrations too early.

## OpenPipeStress Work

Implement:

```text
handoff package generator
units manifest
entity ID manifest
load-case manifest
support/restraint manifest
warnings manifest
unresolved assumptions manifest
target mapping metadata
unsupported behavior flags
```

## Chirality Work

Implement:

```text
handoff checklist generator
external review TBD register
external review comment intake
change-record scaffolding
post-review comparison summary workflow
```

## Workflow

```text
OpenPipeStress generates handoff package
  -> Chirality drafts checklist and review package
  -> user uses external professional stress tool
  -> user records comments/findings
  -> agent converts findings into TBDs/proposals
  -> user revises OpenPipeStress model
  -> OpenPipeStress compares states/runs
  -> Chirality records outcome
```

## Acceptance Criteria

- No automatic claim of external validation is made.
- The user can record external review comments.
- Chirality can organize external-review-driven changes.
- OpenPipeStress can compare pre-review and post-review model states.
- Reports distinguish internal analysis from external review and human acceptance.

## Exit Gate

The workflow supports real engineering practice without pretending to automate professional reliance.

---

# Phase 9: Platformization Beyond OpenPipeStress

## Objective

Make Domain Engine Integration reusable for future professional tools.

## Chirality Work

Abstract:

```text
domain profile registry
domain dashboard
adapter invocation pattern
artifact scanner
operation proposal UI
protected path guard
boundary notice framework
```

## Candidate Future Domain Engines

Examples:

```text
structural frame analysis engine
electrical load-flow engine
process simulation engine
cost estimating engine
scheduling/risk engine
document-code-compliance checker
inspection/test planning engine
```

## Acceptance Criteria

- A second domain engine can be described by a profile without modifying core Chirality logic.
- Domain tools can be listed, invoked, and summarized generically.
- Professional-boundary and protected-write behavior applies to all domain engines.

## Exit Gate

Chirality becomes a true governed professional-work harness for deterministic domain engines.

---

# Phase 10: Advanced Intelligence and Cross-Domain Coordination

## Objective

Use agents to coordinate across multiple deterministic engines and deliverable packages.

## Possible Capabilities

```text
cross-domain dependency graph
design-basis impact analysis
multi-engine change propagation
change-package generation
risk/TBD heat maps
handoff readiness scoring
agent-generated scenario proposals
domain-engine comparison dashboards
external result state support
```

## Guardrail

Even at this stage, agents remain coordinators and proposal generators. They do not become approving authorities.

## Acceptance Criteria

- Agents can identify cross-domain impacts using deterministic artifacts.
- Users can see which deliverables, model states, and handoff packages are affected by a change.
- The system supports change management without automatic professional acceptance.

---

## 6. Workstreams

The program should be managed through parallel but coordinated workstreams.

---

## Workstream A: Chirality Core Hardening

### Purpose

Ensure Chirality is reliable enough to be the professional-work harness.

### Key Work

```text
agent instruction context composition
working-root validation
session persistence
SSE stability
attachment policy
runtime options
tool registry stability
lifecycle transitions
dependency registers
git/file audit behavior
typed errors
desktop packaging
```

### Special Attention

Before relying on agents for project workflows, Chirality should close the known gap where provider turns validate persona existence but do not fully compose selected agent instructions and working-root governance context into the live provider path.

### Done When

- Agent turns are governed by correct persona and project context.
- Deterministic tools are callable and logged.
- Project truth remains in working-root files.
- Human-gate posture remains visible.

---

## Workstream B: Domain Engine Framework

### Purpose

Build the reusable integration layer.

### Key Work

```text
profile schema
profile validator
artifact scanner
protected write paths
agent-writable paths
domain tool registry
tool output capture
operation proposal schema
domain boundary notices
domain fixture tests
```

### Done When

- OpenPipeStress can be integrated through a profile.
- Chirality can support at least one additional hypothetical profile without major redesign.
- Agents cannot write protected domain artifacts through supported write paths.

---

## Workstream C: OpenPipeStress Core

### Purpose

Build the deterministic engineering engine.

### Key Work

```text
schema
unit system
physical model
analytical model
solver
loads
supports
stress recovery
states
runs
comparison
reports
handoff
GUI
rule packs
private libraries
validation suite
```

### Done When

- OpenPipeStress can model, solve, save, compare, and export a small but meaningful piping design case.
- Outputs are deterministic and auditable.
- No protected standards content is shipped.

---

## Workstream D: OpenPipeStress Adapter

### Purpose

Expose OpenPipeStress safely to Chirality.

### Key Work

```text
CLI adapter
read-only commands
write-producing domain-controlled commands
summary generators
manifest generators
proposal validation
report fragment generation
boundary check commands
```

### Done When

- Chirality can call OpenPipeStress tools without directly editing canonical model files.
- Tool outputs are bounded and suitable for agent context.
- Adapter commands have schemas, tests, and deterministic outputs.

---

## Workstream E: Professional and IP/Data Governance

### Purpose

Prevent the ecosystem from making unsafe or legally risky claims.

### Key Work

```text
professional-boundary notices
report language checks
agent language checks
private data boundary checks
protected content quarantine
contribution review process
public/private artifact separation
provenance fields
```

### Done When

- Reports and agent outputs do not imply professional acceptance.
- Public artifacts do not contain protected standards data.
- Private rule packs and project data are excluded from public outputs by default.

---

## Workstream F: Demonstration and Validation Projects

### Purpose

Create proof that the ecosystem works.

### Demo Project 1: Simple OpenPipeStress Model

```text
small L-bend or U-loop model
two model states
two analysis runs
one comparison
one handoff manifest
one Chirality review package
```

### Demo Project 2: External Review Feedback Loop

```text
initial OpenPipeStress model
user-recorded external review comments
agent-created operation proposal
user-applied model change
new analysis run
comparison summary
handoff update
```

### Demo Project 3: Domain Engine Template

```text
mock second domain engine
profile only
read-only summaries
protected paths
operation proposal fixture
```

### Done When

- A new user can understand the whole system from fixture projects.
- Tests prove agents do not directly write protected domain files.
- The demo demonstrates the big-picture architecture.

---

## 7. Release Roadmap

This roadmap describes integrated program releases, not just individual app versions.

---

## Program Release 0: Manual Bridge

### Goal

Use Chirality and OpenPipeStress side by side with no code integration.

### Includes

```text
development plan
PRD amendment
integration plan
working-root layout
manual artifact export/import guidance
review note templates
TBD register templates
handoff checklist templates
```

### Success

A user can manually export OpenPipeStress artifacts and use Chirality agents to organize review work.

---

## Program Release 1: Read-Only Domain Awareness

### Goal

Chirality can discover and summarize OpenPipeStress projects.

### Includes

```text
domain profile schema
OpenPipeStress profile
profile validation
artifact scanner
ops.validate_model
ops.summarize_model
ops.list_states
ops.list_runs
```

### Success

Agents can read actual OpenPipeStress summaries and produce useful review notes without editing model truth.

---

## Program Release 2: State/Run/Comparison Integration

### Goal

Chirality can request or consume OpenPipeStress states, runs, and comparisons.

### Includes

```text
ops.run_analysis
ops.compare_states
ops.compare_runs
tool output capture
comparison summaries
delta tables
protected path guard
```

### Success

A user can compare two model states or two analysis runs and have Chirality summarize the result.

---

## Program Release 3: Handoff Package Integration

### Goal

Support the external prover workflow.

### Includes

```text
ops.generate_handoff
handoff manifest
export warnings
external review TBD register
handoff checklist
external review comment intake
```

### Success

A user can prepare a professional-tool handoff package and maintain a clear review record in Chirality.

---

## Program Release 4: Operation Proposal Workflow

### Goal

Agents can propose model changes safely.

### Includes

```text
operation proposal schema
proposal templates
ops.validate_operation_proposal
diff preview
proposal browser
review notes linkage
```

### Success

An agent can propose a support or route change, OpenPipeStress can validate the proposal, and the user can decide whether to apply it.

---

## Program Release 5: Human-Gated Application

### Goal

Validated proposals can be applied through OpenPipeStress with human approval.

### Includes

```text
ops.apply_operation_proposal
approval reference capture
new model state creation
operation application record
OpenPipeStress proposal review UI
```

### Success

An accepted proposal creates a new OpenPipeStress model state through the domain engine, never through raw agent mutation.

---

## Program Release 6: Platform Domain Engine Kit

### Goal

Make the integration reusable beyond OpenPipeStress.

### Includes

```text
domain engine starter kit
profile examples
adapter templates
fixture domain engine
documentation
test harness
```

### Success

A second deterministic domain engine can integrate with Chirality using the same pattern.

---

## Program Release 7: Cross-Domain Professional Workbench

### Goal

Coordinate multiple domain engines and deliverables.

### Includes

```text
cross-domain dependency tracking
change impact analysis
domain dashboard
risk/TBD heat map
multi-engine handoff packages
```

### Success

Chirality becomes a governed professional-work operating layer across multiple deterministic tools.

---

## 8. MVP Definition

The first meaningful integrated MVP should include:

```text
Chirality:
  - domain profile validation
  - artifact scanner
  - protected path recognition
  - read-only tool invocation
  - agent access to OpenPipeStress summaries
  - review/TBD/draft report generation

OpenPipeStress:
  - canonical schema
  - small model solving
  - named model states
  - analysis runs
  - run summaries
  - comparison summaries
  - handoff manifest skeleton
  - read-only CLI adapter

Shared:
  - OpenPipeStress domain profile
  - working-root layout
  - fixture project
  - professional-boundary notices
  - IP/data-boundary notices
```

MVP does **not** include:

```text
direct agent editing of OpenPipeStress models
external commercial software output parsers
automatic external validation status
automatic professional approval
full dynamic analysis
full CAD/BIM integration
full route optimization
```

---

## 9. Technical Architecture Decisions

### 9.1 Filesystem as Shared Boundary

The integration should use files and manifests as the shared boundary.

Reasons:

- aligns with Chirality project-truth model;
- preserves local-first operation;
- supports git diff, audit, rollback, and human review;
- avoids hidden database state;
- allows domain engines to retain their own internal schemas.

### 9.2 CLI / Tool Adapter First

OpenPipeStress should expose a CLI or equivalent deterministic adapter before deep UI integration.

Reasons:

- easier to test;
- easier to invoke from Chirality;
- easier to log;
- avoids GUI automation;
- keeps domain computation deterministic.

### 9.3 Protected Paths

Domain profile must declare protected paths.

Reasons:

- prevents raw agent mutation of accepted model truth;
- makes safety visible;
- supports testable guardrails;
- preserves domain-engine ownership.

### 9.4 Generated Summaries and Manifests

OpenPipeStress should produce bounded summaries for Chirality agents.

Reasons:

- agents cannot safely read unlimited model/result internals;
- summaries reduce context overload;
- manifests allow traceability;
- warnings/TBDs become easy to organize.

### 9.5 Operation Proposals

Agents should propose changes as structured data.

Reasons:

- proposals can be validated before application;
- user can inspect diffs;
- invalid or unsafe proposals can be rejected;
- applied changes can create new model states with traceability.

---

## 10. Engineering Backlog Summary

### 10.1 Chirality Backlog

```text
CH-DOM-001  Domain profile schema
CH-DOM-002  Domain profile validator
CH-DOM-003  Domain artifact scanner
CH-DOM-004  Protected path guard
CH-DOM-005  Domain tool registry
CH-DOM-006  Tool invocation API
CH-DOM-007  Tool output capture
CH-DOM-008  Operation proposal authoring
CH-DOM-009  Proposal browser
CH-DOM-010  Domain dashboard
CH-DOM-011  Boundary notice framework
CH-DOM-012  Domain fixture tests
```

### 10.2 OpenPipeStress Backlog

```text
OPS-CORE-001  Canonical schema
OPS-CORE-002  Unit system
OPS-CORE-003  Physical model
OPS-CORE-004  Analytical model transform
OPS-CORE-005  Solver MVP
OPS-CORE-006  Stress recovery
OPS-STATE-001 Model states
OPS-RUN-001   Analysis runs
OPS-CMP-001   Model-state comparison
OPS-CMP-002   Analysis-run comparison
OPS-HAND-001  Handoff manifest
OPS-CLI-001   CLI adapter
OPS-CLI-002   Summary generator
OPS-CLI-003   Boundary check commands
OPS-PROP-001  Operation proposal schema
OPS-PROP-002  Proposal validation
OPS-GUI-001   Model editor
OPS-GUI-002   State/run/comparison browser
```

### 10.3 Shared Backlog

```text
SHARED-001 OpenPipeStress domain profile
SHARED-002 Working-root fixture project
SHARED-003 End-to-end demo script
SHARED-004 Professional-boundary test cases
SHARED-005 Protected path write-attempt tests
SHARED-006 Handoff checklist template
SHARED-007 External review feedback workflow
```

---

## 11. Testing Strategy

### 11.1 Chirality Tests

Test:

```text
domain profile validation
profile discovery
invalid profile rejection
protected path matching
agent-writable path matching
domain artifact scanning
tool invocation argument validation
tool output capture
failed tool behavior
missing domain engine behavior
write-attempt rejection
```

### 11.2 OpenPipeStress Tests

Test:

```text
schema round-trip
unit conversion
solver benchmarks
model-state hashing
analysis-run reproducibility
comparison determinism
handoff manifest completeness
summary generation determinism
proposal validation without mutation
private-data redaction
professional-boundary notices
```

### 11.3 Integration Tests

Test:

```text
Chirality scans fixture project
OpenPipeStress profile validates
ops.summarize_model creates manifest
agent reads manifest and writes review notes
ops.run_analysis creates run summary
ops.compare_runs creates delta table
agent writes comparison review
ops.generate_handoff creates manifest
protected paths are not directly mutated by agents
```

### 11.4 Governance Tests

Test:

```text
agent output does not claim code compliance
agent output does not claim professional approval
report fragments contain required notices
protected content is flagged
private rule-pack content is not leaked
external prover status is not fabricated
```

---

## 12. Demonstration Scenario

The first end-to-end demonstration should be deliberately small.

### Scenario

A designer creates a simple piping route with an anchor, elbow, support, and thermal load.

### Flow

```text
1. Chirality scaffolds project structure.
2. OpenPipeStress creates model state STATE-0001.
3. OpenPipeStress runs analysis RUN-0001.
4. Chirality agent summarizes warnings and TBDs.
5. User modifies support in OpenPipeStress.
6. OpenPipeStress creates STATE-0002 and RUN-0002.
7. OpenPipeStress compares RUN-0001 and RUN-0002.
8. Chirality agent drafts comparison review.
9. OpenPipeStress generates handoff manifest.
10. Chirality agent drafts external prover handoff checklist.
```

### Demonstration Success

The demonstration succeeds if:

- results come from OpenPipeStress, not the agent;
- review notes come from Chirality agents, not the solver;
- model changes occur through OpenPipeStress, not raw agent edits;
- files are local and git-trackable;
- no professional approval is implied.

---

## 13. Key Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---:|---|
| Chirality becomes too domain-specific | High | Use generic Domain Engine Profile with OpenPipeStress as first profile. |
| Agents mutate engineering model truth | High | Protected paths, write guards, operation proposals, domain-controlled tools. |
| OpenPipeStress becomes an agent OS | Medium | Keep OpenPipeStress focused on model, GUI, solver, states, runs, comparison, and handoff. |
| Agent summaries fabricate engineering conclusions | High | Require deterministic tool outputs, manifests, run IDs, comparison IDs, and boundary notices. |
| Users mistake internal results for professional validation | High | Report notices, professional boundary policy, no automatic approval/compliance statuses. |
| External prover workflow is overbuilt too early | Medium | Start with handoff manifest and user-mediated feedback; defer external output parsers. |
| Private or protected data leaks into public artifacts | High | IP/data checks, redaction, private-by-default paths, provenance requirements. |
| Domain profiles are too rigid | Medium | Version profile schema and allow domain-specific extensions. |
| Integration delays OpenPipeStress solver work | Medium | Build OpenPipeStress core first; integrate through summaries and adapter later. |
| Integration delays Chirality core hardening | Medium | Keep Domain Engine Framework staged after core harness stability. |

---

## 14. Decision Gates

### Gate 1: Architecture Acceptance

Question:

```text
Do we accept Chirality + Domain Engine + OpenPipeStress as a federated architecture?
```

Required evidence:

```text
PRD amendment accepted
integration plan accepted
protected boundaries understood
```

### Gate 2: OpenPipeStress Core Credibility

Question:

```text
Is OpenPipeStress deterministic enough to expose to agents?
```

Required evidence:

```text
solver benchmarks
schema round-trip tests
states/runs implemented
summary generator implemented
```

### Gate 3: Read-Only Integration Safety

Question:

```text
Can Chirality read OpenPipeStress outputs without risking model mutation?
```

Required evidence:

```text
domain profile validation
artifact scanner
read-only adapter commands
protected path tests
```

### Gate 4: Domain-Controlled Write Safety

Question:

```text
Can Chirality request domain-generated outputs without agents writing protected files?
```

Required evidence:

```text
tool invocation logs
output capture
domain-controlled write tests
human confirmation for high-impact commands
```

### Gate 5: Proposal Workflow Safety

Question:

```text
Can agents propose changes without users mistaking proposals for accepted engineering work?
```

Required evidence:

```text
proposal schema
proposal validation
proposal labels
diff preview
user acceptance path
```

### Gate 6: Handoff Workflow Utility

Question:

```text
Does the handoff workflow reduce rework and improve external validation readiness?
```

Required evidence:

```text
handoff manifest completeness
external review checklist
post-review comparison workflow
user feedback
```

---

## 15. Documentation Plan

Produce or update:

```text
README_DOMAIN_ENGINES.md
DOMAIN_ENGINE_PROFILE_SPEC.md
DOMAIN_TOOL_ADAPTER_SPEC.md
DOMAIN_WRITE_BOUNDARY_POLICY.md
DOMAIN_OPERATION_PROPOSAL_SPEC.md
OPENPIPESTRESS_CHIRALITY_PROFILE.yaml
OPENPIPESTRESS_CLI_ADAPTER_SPEC.md
OPENPIPESTRESS_CHIRALITY_USER_GUIDE.md
OPENPIPESTRESS_HANDOFF_WORKFLOW.md
OPENPIPESTRESS_AGENT_PROPOSAL_GUIDE.md
PROFESSIONAL_BOUNDARY_GUIDE.md
IP_DATA_BOUNDARY_GUIDE.md
```

---

## 16. Success Metrics

### 16.1 Platform Metrics

```text
number of valid domain profiles
number of deterministic domain tools registered
number of protected path write attempts blocked
number of generated manifests/summaries
number of successful domain tool invocations
time to onboard a new domain profile
```

### 16.2 OpenPipeStress Metrics

```text
solver benchmarks passed
schema round-trip pass rate
analysis-run reproducibility rate
comparison determinism rate
handoff manifest completeness
number of unresolved critical solver defects
```

### 16.3 Workflow Metrics

```text
time from model state to review summary
time from comparison to review note
time from analysis run to handoff checklist
number of TBDs resolved
number of external-review changes traced to model states
number of agent proposals accepted/rejected
```

### 16.4 Governance Metrics

```text
professional-boundary violations caught
private-data leakage incidents
protected-content quarantine events
reports with required notices
agent outputs with cited deterministic evidence
```

---

## 17. Long-Term Product Vision

The long-term product is not “AI that does engineering.”

The long-term product is:

> **A local-first professional engineering operating environment where governed agents coordinate work around deterministic domain engines, with humans retaining authority and git-tracked files preserving the project record.**

OpenPipeStress is the first example because piping stress analysis is a strong proving ground:

- it has real engineering consequences;
- it depends on deterministic mechanics;
- it requires rich model state;
- it has clear professional boundaries;
- it has established external prover tools;
- it benefits from rapid iteration and traceable assumptions;
- it has many places where agents can help without becoming the authority.

If this works for OpenPipeStress, the pattern can generalize to other professional domains.

---

## 18. Near-Term Next Actions

1. Adopt the Chirality PRD amendment for Domain Engine Integration.
2. Create the formal Domain Engine Profile specification.
3. Create the OpenPipeStress domain profile.
4. Build OpenPipeStress core schema and read-only summary generator.
5. Build Chirality profile validation and artifact scanning.
6. Build protected path guard tests.
7. Create a small OpenPipeStress fixture project.
8. Demonstrate read-only model review in Chirality.
9. Add state/run/comparison generation.
10. Add handoff manifest generation.
11. Add operation proposal workflow.
12. Defer external prover parsers and automatic validation statuses.

---

## 19. Guiding Statement

> Build the ecosystem so every role stays honest: Chirality governs work, agents propose, OpenPipeStress computes, external tools validate, humans accept, and the filesystem remembers.
