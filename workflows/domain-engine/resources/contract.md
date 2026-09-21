# domain-engine — contract

## Runtime Variables and Defaults

This file is project-generic. Do not embed project-specific absolute paths or OpenPipeStress-only assumptions.

Resolve these variables from the human prompt, working-root state, existing profile files, or explicit project records:

| Variable | Meaning |
|---|---|
| `WORKING_ROOT` | User-selected project root where project truth lives |
| `INSTRUCTION_ROOT` | Release-managed Chirality instruction root |
| `DOMAIN_ENGINE_ID` | Stable profile identifier, for example `open_pipe_stress` |
| `DOMAIN_ENGINE_ROOT` | Domain-engine-owned folder or project file root |
| `DOMAIN_PROFILE_PATH` | Domain Engine Profile file, if present |
| `DOMAIN_CONTROL_ROOT` | Project-level Chirality control area for domain integration records |
| `DOMAIN_TOOL_ADAPTER` | Declared deterministic CLI/API adapter for the domain engine |
| `INTEGRATION_LEVEL` | `MANUAL_BRIDGE | READ_ONLY | DOMAIN_CONTROLLED_WRITE | OPERATION_PROPOSAL | EXTERNAL_RESULT_STATE` |

Default only when no project-local convention exists and the human approves creation:

```text
DOMAIN_CONTROL_ROOT = {WORKING_ROOT}/_DomainEngines/
```

Do not create `DOMAIN_CONTROL_ROOT` silently. If the root does not exist, propose it and wait for human approval before writing.

---

## Non-Negotiable Invariants

- **Domain engines own domain truth.** Canonical model files, model states, analysis runs, comparison records, solver outputs, native GUI state, and handoff package internals remain owned by the domain engine.
- **Chirality governs the work around the domain engine.** Chirality may manage profiles, manifests, summaries, review notes, operation proposals, TBD registers, dependency records, handoff checklists, and human gate records.
- **No agent is the source of accepted engineering truth.** Agents create drafts, summaries, questions, and proposals. Humans accept or reject. Domain tools compute and validate.
- **Profiles are mandatory beyond manual bridge mode.** WORKING_ITEMS must not claim a read-only or tool-integrated workflow is governed unless a profile or equivalent approved boundary record defines authoritative artifacts, readable artifacts, protected paths, agent-writable paths, tools, and human gates.
- **Protected paths are write-quarantined.** Agents must not directly write protected domain artifacts. A profile may permit specific domain-controlled operations, but those operations must go through declared deterministic tools and required human gates.
- **Domain tool adapters are deterministic and bounded.** Adapter commands must have declared inputs, outputs, modes, side effects, failure behavior, and output capture rules.
- **Human gates are mandatory for consequential transitions.** Profile adoption, protected path policy, mutating domain tool invocation, operation proposal application, external validation status, and professional reliance decisions require explicit human approval.
- **No professional status invention.** WORKING_ITEMS must not declare code compliance, certification, sealing, approval, ready-for-construction status, or external prover validation unless a human-provided authoritative record is present and cited.
- **No hidden project truth.** Domain integration records that affect project reasoning must be written as project files, not retained only in chat, app state, caches, or vendor systems.
- **Evidence-first.** Claims about domain artifacts, tool outputs, warnings, assumptions, deltas, and blockers must cite files, IDs, manifests, run records, comparison IDs, or explicit `TBD`.
- **Unknowns become TBD.** Missing engineering data, missing adapter outputs, ambiguous model ownership, and unclear professional status are recorded as `TBD`, not guessed.
- **OpenPipeStress is an example, not the ontology.** Do not hard-code piping-specific assumptions into the generic integration pattern.
- **Skill and tool boundaries are preserved.** Recurring bounded methods are workflow candidates. Deterministic validation, scanning, matching, schema checks, and template generation are tool candidates. WORKING_ITEMS specifies and hands those needs to HELPS_HUMANS; it does not collapse the layers.

---

## Domain integration boundaries

The selected domain integration workflow consumes accepted decomposition and project state, develops the integration profile, and coordinates approved engine operations and their evidence. It preserves these responsibilities:

- **Domain computation.** The domain engine performs its declared model operations, calculations, comparisons, and native artifact production. WORKING_ITEMS invokes and interprets those operations under the accepted profile.
- **Professional acceptance.** The human professional or accountable reviewer decides what can be relied upon.
- **Decomposition and setup.** Creating or amending decomposition and initializing a workspace require their selected workflows and accepted scope. WORKING_ITEMS may switch to an authorized workflow within its undertaking; separately owned work is routed to the responsible instance or loop. Domain integration alone leaves those accepted sources unchanged.
- **Bounded execution.** TASK executes assigned methods or briefs and returns evidence for integration.
- **Workflow and tool design.** HELPS_HUMANS helps conceive the workflows, interfaces, and integration features. WORKING_ITEMS implements accepted designs through bounded TASK assignments and integrates their evidence.
- **Framework maintenance.** Project-runtime integration does not authorize edits to the release-managed instruction root. Framework changes require an explicitly scoped Root undertaking; route the requirement to its owner.
- **Git, review, evaluation, and concordance.** These are selected workflows with their own source boundaries, human decisions, and acceptance conditions. WORKING_ITEMS can coordinate them within authorized scope, preserving independent review where required; it routes separately owned undertakings through their owners.

---

## Definitions

| Term | Meaning |
|---|---|
| **Domain Engine** | Specialist deterministic software that owns domain-specific models, calculations, validation, and native workflows |
| **Domain Engine Profile** | Structured configuration declaring artifact classes, protected paths, agent-writable paths, deterministic tools, and human gates |
| **Domain Tool Adapter** | Deterministic CLI/API surface exposed by a domain engine and callable by Chirality under profile constraints |
| **Authoritative Domain Artifact** | File/folder that represents domain truth owned by the domain engine |
| **Chirality-Readable Artifact** | Manifest, summary, warning list, assumption register, delta table, checklist, or report fragment safe for agents to read and cite |
| **Agent-Writable Artifact** | Proposal, review note, TBD register, draft report section, checklist, dependency note, or reconciliation note permitted by profile |
| **Protected Write Path** | Path agents must not directly modify |
| **Domain-Controlled Write** | Write produced by a declared domain tool, not raw agent file mutation |
| **Operation Proposal** | Structured proposed model/domain change; not accepted truth until validated and human-approved |
| **External Prover Record** | Human-supplied or tool-supplied evidence from an external professional validation workflow |
| **Boundary Notice** | Required language preventing false claims of professional approval, code compliance, certification, sealing, or external validation |

---

## Inputs

### Required for Any Run

- Human request describing the desired domain-engine action.
- `WORKING_ROOT` or enough context to resolve it.
- Intended `INTEGRATION_LEVEL` or enough information to classify it.

### Required Beyond Manual Bridge

- `DOMAIN_ENGINE_ID`.
- `DOMAIN_PROFILE_PATH` or a human-approved profile design task.
- Declared authoritative artifacts.
- Declared protected write paths.
- Declared agent-writable paths.
- Declared deterministic tools or statement that no tools are available yet.

### Optional

- Domain tool adapter path and version.
- Existing manifests, summaries, warnings, assumptions, deltas, or handoff records.
- Operation proposal files.
- External prover comments or review records.
- Professional boundary language required by the project.
- IP/data-boundary constraints.
- Desired outputs and allowed writes.

---

## Integration Levels

WORKING_ITEMS classifies every request into one of these levels:

| Level | Token | Meaning | Agent posture |
|---:|---|---|---|
| 0 | `MANUAL_BRIDGE` | User manually exports domain summaries/manifests; Chirality agents read and organize them | Safe default; no tool integration required |
| 1 | `READ_ONLY` | Chirality invokes read-only deterministic tools such as validate, summarize, list states/runs | Requires profile and read-only tool contracts |
| 2 | `DOMAIN_CONTROLLED_WRITE` | Chirality requests domain-generated outputs such as runs, comparisons, report fragments, or handoff manifests | Requires profile, tool contract, output capture, and human confirmation where profile requires |
| 3 | `OPERATION_PROPOSAL` | Agents write structured proposals; domain engine validates/previews; human accepts/rejects | Requires proposal schema and protected path guard |
| 4 | `EXTERNAL_RESULT_STATE` | Future support for structured external-result records compared by the domain engine | Future only unless separately scoped |

Do not jump levels. If the human requests deep automation while lower-level profile/tool boundaries are missing, stop and present the missing prerequisites.

---

## Validity

### Valid Domain Engine Profile

A profile is valid for governed use when it declares:

| Field | Requirement |
|---|---|
| `schema_version` | Present |
| `id` | Stable ASCII token |
| `name` | Human-readable engine name |
| `engine_type` | Domain classification |
| `domain_root_patterns` | One or more discovery patterns |
| `authoritative_artifacts` | Files/folders owned by the domain engine |
| `chirality_readable_artifacts` | Bounded artifacts agents may read |
| `protected_write_paths` | Files/folders agents must not directly write |
| `agent_writable_paths` | Paths for proposals, notes, TBDs, drafts, and checklists |
| `deterministic_tools` | Declared tool IDs, modes, schemas, and human confirmation requirements |
| `professional_boundary` | Prohibited claims and required notices |

If any required field is missing, the profile status is `DRAFT` (incomplete but well-formed)
or `INVALID` (present but malformed or non-conforming), not `ADOPTED`. Use `UNKNOWN`
only at intake before the profile has been discovered or scanned; use `NONE` when no
profile exists.

### Valid Domain Tool Invocation

A domain tool invocation is valid when:

1. The active profile declares the tool.
2. The tool mode and side effects are known.
3. Required arguments are present and schema-valid.
4. Output paths are declared and writable by the domain tool.
5. Agent direct writes to protected paths are not used.
6. Required human confirmation was obtained before invocation.
7. Results are captured as project files when they affect project reasoning.
8. Failures are recorded explicitly.

### Valid Operation Proposal

An operation proposal is valid for review when:

| Field | Requirement |
|---|---|
| `proposal_id` | Stable proposal ID. |
| `profile_id` | Stable ID of the active domain engine profile. |
| `base_state` | Base model state or domain state, if applicable; otherwise explicit `TBD`. |
| `operation_name` | Declared operation name from the active profile or deterministic tool contract. |
| `status` | `proposal_only` until validated by declared deterministic checks and human-accepted. |
| `lifecycle` | One of `draft | ready_for_review | accepted | rejected | applied`. `proposal_only` covers `draft` and `ready_for_review`; `accepted` and `applied` require a human approval record bound to a git SHA per K-AUTH-2 and, where the engine has a terminal human-accepted lifecycle state, that external record. |
| `created_at` | Creation timestamp. |
| `created_by` | Actor that created the proposal. |
| `input_refs` | Evidence references such as manifests, warnings, run IDs, comparison IDs, schema refs, or file paths. |
| `intended_changes` | Proposed domain changes, each bounded to the profile and operation. |
| `deterministic_checks` | Declared checks to run before review or application, with result schema refs or explicit `TBD`. |
| `expected_output_refs` | Expected artifacts, IDs, summaries, validation records, or export refs. |
| `risks` | Known risks, including whether the operation can be fully checked by the engine. |
| `assumptions` | Unresolved assumptions, distinct from risks. |
| `blockers` | Unresolved blockers preventing acceptance or application. |
| `boundary_notice` | Professional-boundary language preventing claims of approval, certification, sealing, code compliance, ready-for-construction status, or external validation absent a cited human authoritative record. |
| `required_human_gate` | Gate token for the human-owned accept/reject decision; accepted/applied transitions bind to a git SHA per K-AUTH-2. |
| `operation_risk_class` | One of `engine_checkable | engine_silent`. Use `engine_silent` when correctness depends on judgment values or premises the engine cannot independently verify. |
| `provenance_on_judgment_values` | Required provenance for `engine_silent` values or explicit `TBD`. |
| `storage_path` | Path under a profile-approved `agent_writable_paths` entry. |

The active profile should identify the validate/apply result schema and deterministic-check
result schema used by its tool adapters. If those schemas are not yet declared, record them as
`TBD`; do not infer acceptance or application semantics from chat.

An operation proposal is invalid if it is represented as accepted domain truth before the
required human gate and domain-engine-controlled apply record exist.

### Human Agency Map

| Human-owned decision | WORKING_ITEMS may do |
|---|---|
| Adopt or reject a profile | Draft, analyze, and explain the profile |
| Approve protected write path policy | Surface path classes and risks |
| Approve mutating domain tool calls | Prepare invocation plan and capture outputs |
| Accept/reject operation proposals | Draft, validate, summarize, and record blockers |
| Interpret external prover results | Organize comments, TBDs, and change proposals |
| Decide professional reliance | Preserve boundary language and cite evidence |
| Approve publication/git actions | Hand off file lists and recommended commit notes to WORKING_ITEMS (workflow: change) |

### Skill and Tool Dispatch Rules

Route a workflow-design requirement to HELPS_HUMANS when the need is a recurring bounded method, such as:

- domain profile review method;
- domain artifact review package;
- operation proposal authoring;
- handoff checklist generation;
- external review feedback intake;
- domain report-fragment review.

Route a tool-design requirement to HELPS_HUMANS when the need is deterministic and LLM-independent, such as:

- domain profile schema validation;
- domain artifact scanning;
- protected path matching;
- agent-writable path matching;
- tool argument schema validation;
- tool output capture and indexing;
- proposal schema validation;
- boundary-language string checks;
- private-data/protected-content scanning.

WORKING_ITEMS may prepare workflow or tool requirement briefs for HELPS_HUMANS. It must not implement those components inside this workflow resource.

### Invalid States

The following states are invalid:

| Invalid state | Why it fails |
|---|---|
| Profile-free tool integration | No governed artifact/tool/write boundary exists |
| Agent direct edit to protected domain artifact | Violates domain ownership and write quarantine |
| Agent-generated domain result | Computation must come from deterministic domain tools |
| Proposal treated as accepted change | Human/domain-engine gate skipped |
| Hidden domain result in chat only | Violates filesystem project-truth model |
| External validation claim without record | Invents professional status |
| OpenPipeStress-specific rule in generic schema | Breaks general Domain Engine Framework |

---

## Artifacts and schemas

### System Map

```text
Human Professional / Responsible Reviewer
  owns acceptance, professional reliance, external validation interpretation

WORKING_ITEMS
  manages profiles, boundaries, tool plans, proposals, handoff state

TASK + workflows
  execute bounded methods within approved scope

HELPS_HUMANS tools
  perform deterministic scans, validation, matching, indexing, and capture

Domain Engine
  owns model truth, computation, GUI/native workflow, states, runs, comparisons, handoffs

Working Root
  stores project-visible records, summaries, proposals, manifests, and snapshots
```

### Workflow Coverage Map

WORKING_ITEMS covers the HELPS_HUMANS workflow-design surfaces as follows:

| HELPS_HUMANS surface | WORKING_ITEMS binding |
|---|---|
| Domain summary | Deterministic domain-engine integrations that connect Chirality project records to engine-owned domain truth |
| Ontology | Domain Engine, Profile, Tool Adapter, Authoritative Domain Artifact, Chirality-Readable Artifact, Agent-Writable Artifact, Protected Write Path, Operation Proposal, Handoff State |
| Human agency map | `SPEC` section `Human Agency Map` |
| Permission map | `STRUCTURE` section `Permission Map` |
| Brief format | INIT-TASK examples plus HELPS_HUMANS workflow/tool requirement brief shapes |
| Snapshot contract | `STRUCTURE` section `Snapshot Contract` and `Handoff State` |
| Schemas | profile shape, integration record, valid invocation, valid proposal, requirement briefs, handoff state |
| QA contract | `STRUCTURE` section `QA Contract` |
| Runbooks | `PROTOCOL` functions and `STRUCTURE` section `Runbooks` |
| Publication workflow | `STRUCTURE` section `Publication Workflow` |

### Permission Map

| Actor / layer | May read | May write | Must not write |
|---|---|---|---|
| Human operator | Any project-visible artifact the human is authorized to inspect | Any project artifact the human chooses to edit | N/A; human remains accountable for consequences |
| WORKING_ITEMS | Profiles, manifests, summaries, warnings, assumptions, proposals, review notes, handoff records, accepted decomposition/project records | Project-level domain integration control artifacts only, when approved | Protected domain artifacts, domain model truth, solver outputs, accepted model states, instruction-root files during project-runtime work |
| TASK dispatched by WORKING_ITEMS | Only files named in the brief and profile-readable artifacts inside scope | Only `AllowedWriteTargets` within `ScopePath` | Anything outside `ScopePath`; protected domain paths; undeclared tool outputs |
| HELPS_HUMANS | Workflow/tool needs and domain constraints | Design proposals and clarified interfaces | Human domain acceptance |
| WORKING_ITEMS | Accepted design and bounded implementation briefs | Workflow/tool implementation and integration evidence through TASK | Human domain acceptance |
| Domain tool adapter | Inputs declared by profile and invocation plan | Declared domain-controlled output paths only | Agent-writable review/proposal notes unless explicitly part of declared tool output |
| Domain engine application | Its own model files, states, runs, comparisons, handoff packages | Its own authoritative domain artifacts | Chirality instruction root or unrelated project records |
| WORKING_ITEMS (workflow: change) | Git state and explicit file lists | Staging/commits/tags only after human approval | Silent publish, force-push, or unstated file changes |

If the permission map conflicts with a project-local profile, use the stricter rule and request human resolution before proceeding.

### Recommended Control Package

When project-level domain integration records are needed and no stronger project convention exists, propose this layout:

```text
{WORKING_ROOT}/_DomainEngines/
  DOMAIN_ENGINE_INDEX.md
  profiles/
    <domain_engine_id>.yaml
  scans/
    SCAN_<YYYY-MM-DD>_<HHmm>/
      ARTIFACT_INVENTORY.md
      PROFILE_STATUS.md
      MISSING_ITEMS.md
  tool_runs/
    TOOLRUN_<YYYY-MM-DD>_<HHmm>/
      INVOCATION_PLAN.md
      RESULT_CAPTURE.md
      WARNINGS.md
  proposals/
    <domain_engine_id>/
      PROP-<NNNN>_<short_name>.yaml
  handoffs/
    HANDOFF_<YYYY-MM-DD>_<HHmm>/
      HANDOFF_STATE.md
      CHECKLIST.md
      EXTERNAL_REVIEW_TBDS.md
  boundary_reviews/
    BOUNDARY_<YYYY-MM-DD>_<HHmm>/
      PROFESSIONAL_BOUNDARY.md
      IP_DATA_BOUNDARY.md
  _LATEST.md
```

Snapshot folders are immutable. `_LATEST.md` may be updated only to point to the latest accepted snapshot or state record.

### Snapshot Contract

When WORKING_ITEMS writes a project-level run record, scan record, tool-run record, boundary review, proposal package, or handoff package, it must use a new immutable folder unless the project profile defines a stricter convention.

Minimum snapshot contents:

| File | Purpose |
|---|---|
| `Brief.md` | Human request, normalized action type, scope, profile, tools, permissions, and expected outputs |
| `RUN_SUMMARY.md` | Status, files read, tools invoked, outputs written, blockers, and next owner |
| `PROFILE_STATUS.md` | Active profile path, status, integration level, protected paths, readable artifacts, and open profile issues |
| `ARTIFACT_INVENTORY.md` | Role-labeled domain artifacts, readable artifacts, missing items, and stale indicators |
| `Handoff_State.md` | Closure state when downstream work remains |

Pointer behavior:

- `_LATEST.md` may be overwritten to point to the latest accepted snapshot.
- Existing snapshot folders must not be edited after closure.
- If a rerun is needed, create a new snapshot and update the pointer only after the human accepts it as current.

### QA Contract

Before closure, WORKING_ITEMS must check:

| Check | Required outcome |
|---|---|
| Profile status | Profile is `ADOPTED` for integrated workflows, or missing profile is explicitly recorded for `MANUAL_BRIDGE` |
| Protected paths | No direct agent writes to protected paths |
| Agent write scope | All agent writes fall under profile-approved agent-writable paths and explicit `AllowedWriteTargets` |
| Tool declaration | Invoked tools are declared by profile or explicitly approved by the human for the run |
| Tool results | Outputs affecting project reasoning are captured as project files |
| Provenance | Review notes, proposals, and handoff records cite files, IDs, tool outputs, or `TBD` |
| Proposal status | Operation proposals are marked `proposal_only` until accepted through the domain engine and human approval |
| Boundary notices | Professional/IP/data boundary notices are present where profile requires them |
| External validation | No external validation status is claimed without cited human-provided authority |
| Rerun guidance | Stale/missing manifests, summaries, validations, comparisons, or handoffs are listed with next owner |

If any required check fails, closure status is `BLOCKED` or `PARTIAL`, not `SUCCESS`.

### Runbooks

#### Runbook A - Adopt or Review a Domain Engine Profile

1. Classify the request as `PROFILE_ADOPTION`.
2. Read existing profile and relevant project/domain artifacts.
3. Produce or update the profile boundary summary.
4. Check required profile fields, protected paths, tools, and human gates.
5. Ask the Gate 2 approval question.
6. If approved, record profile status and next safe integration level.

#### Runbook B - Read-Only Domain Review

1. Confirm profile status permits `READ_ONLY`.
2. Inventory readable artifacts and missing manifests.
3. Prepare TASK brief with readable artifacts and restricted write targets.
4. Dispatch or propose bounded review work.
5. Capture review notes, TBDs, provenance, and blockers.
6. Close with `Handoff_State.md` when downstream action remains.

#### Runbook C - Domain Tool Invocation

1. Confirm profile declares the tool.
2. Classify mode and side effects.
3. Validate arguments and output paths.
4. Ask the Gate 4 approval question if required.
5. Invoke through the declared adapter or hand off to HELPS_HUMANS if adapter support is missing.
6. Capture outputs and QA results as project files.

#### Runbook D - Operation Proposal

1. Confirm the profile permits proposals and names an allowed proposal path.
2. Draft or dispatch proposal drafting with cited evidence.
3. Mark status `proposal_only`.
4. Validate through declared deterministic tool where available.
5. Record warnings, blockers, assumptions, and human rulings.
6. Do not apply without human approval and domain-engine-controlled application.

#### Runbook E - Handoff / External Prover Support

1. Confirm handoff intent and profile-supported artifacts.
2. Ensure handoff package internals come from the domain engine, not agents.
3. Draft Chirality-side checklist, TBD register, and review notes.
4. Record external comments as human-supplied evidence unless a validated adapter supplies them.
5. Close with boundary notices and next owner.

### Publication Workflow

The domain integration stage prepares publication evidence. Git closeout or publication uses the authorized change workflow and its applicable human decisions. WORKING_ITEMS may carry that stage within the same accepted undertaking or route it to the separately owning instance. When a domain-engine run changes project-visible records and publication is authorized:

1. Produce a file list grouped by artifact role.
2. Identify generated/derived artifacts separately from human-accepted records.
3. Include closure status, blockers, and rerun requirements.
4. Recommend a concise commit message only as `PROPOSAL`.
5. Select the change workflow for authorized Git operations within the undertaking, or hand the package to its separately owning instance. Apply its closeout and publication gates.

### Domain Integration Record

A domain integration record should include:

| Field | Meaning |
|---|---|
| `DomainEngineID` | Stable profile ID |
| `ProfilePath` | Path to active profile |
| `ProfileStatus` | `NONE | DRAFT | VALIDATED | ADOPTED | STALE | INVALID | UNKNOWN` |
| `IntegrationLevel` | Current approved level |
| `DomainEngineRoot` | Engine-owned root or project file |
| `AuthoritativeArtifacts` | Paths/patterns owned by the engine |
| `ReadableArtifacts` | Paths/patterns agents may read |
| `ProtectedWritePaths` | Paths/patterns agents must not directly write |
| `AgentWritablePaths` | Paths/patterns agents may write under explicit scope |
| `DeclaredTools` | Tool IDs and modes |
| `HumanGates` | Required approval points |
| `BoundaryNotices` | Professional and IP/data language |
| `OpenIssues` | `TBD` items and blockers |

### Minimal Domain Engine Profile Shape

```yaml
domain_profile:
  schema_version: "1.0"
  id: "<domain_engine_id>"
  name: "<Domain Engine Name>"
  engine_type: "<domain classification>"
  profile_version: "0.1"

  domain_root_patterns:
    - "<path or glob>"

  authoritative_artifacts:
    - "<engine-owned path or glob>"

  chirality_readable_artifacts:
    - "<manifest/summary/report path or glob>"

  protected_write_paths:
    - "<agent-prohibited path or glob>"

  agent_writable_paths:
    - "<proposal/review/checklist path or glob>"

  deterministic_tools:
    - id: "<tool.id>"
      mode: "read_only"
      requires_human_confirmation: false
      validate_result_schema: "<schema ref or TBD>"
      apply_result_schema: "<schema ref or TBD>"

  operation_proposal_contract:
    lifecycle:
      - "draft"
      - "ready_for_review"
      - "accepted"
      - "rejected"
      - "applied"
    risk_classes:
      - "engine_checkable"
      - "engine_silent"
    deterministic_check_result_schema: "<schema ref or TBD>"
    accepted_or_applied_requires:
      - "human approval bound to git SHA per K-AUTH-2"
      - "domain-engine-controlled apply or external terminal acceptance record"

  professional_boundary:
    agent_must_not_claim:
      - "code compliant for reliance"
      - "professionally approved"
      - "certified"
      - "sealed"
      - "ready for construction"
      - "external prover validated unless supplied as external human record"
```

### OpenPipeStress Example Binding

For OpenPipeStress profiles, the verified 2026-06-21 binding is:

| Class | Real paths/artifacts |
|---|---|
| Authoritative domain artifacts | `projects/chirality-piping/core/**` (engine, solver, and model operations); `projects/chirality-piping/schemas/**` (contracts); the engine project store per `projects/chirality-piping/schemas/project_persistence.schema.yaml` (model states, analysis runs, and comparisons; SQLite-backed, not a static directory tree); `projects/chirality-piping/core/handoff/**` |
| Chirality-readable artifacts | Records conforming to `projects/chirality-piping/schemas/{analysis_run,model_state,comparison_mapping,handoff_package}.schema.*` when produced; on-demand exports under `projects/chirality-piping/core/handoff/*` (`native_json`, `stress_neutral`, `review_geometry`); professional-boundary notices emitted by declared operation and rule-check tooling |
| Protected write paths | `projects/chirality-piping/core/**`, `projects/chirality-piping/schemas/**`, the engine project store, `projects/chirality-piping/core/handoff/**`, solver outputs, accepted model states |
| Agent-writable artifacts | `_DomainEngines/proposals/open_pipe_stress/**` for OperationProposals; `_DomainEngines/bridge/**` for review notes, TBD registers, checklists, and framework-maintenance records |

OpenPipeStress persists model, state, run, and comparison records in an engine-owned store
(SQLite-backed per `project_persistence.schema.yaml`) and emits readable artifacts on demand.
There is no `project.ops.yaml` file or static `states/`, `runs/`, or `comparisons/`
directory tree in the verified binding. The instance engineering lifecycle is its
`AnalysisStatus` vocabulary in `projects/chirality-piping/schemas/model.schema.yaml`.

### INIT-TASK Brief Example - Read-Only Domain Artifact Review

```markdown
PURPOSE: Review domain-engine generated summaries and draft review notes without touching protected domain artifacts.
RequestedBy: WORKING_ITEMS

ScopePath: <approved agent-writable review folder>
Workflow: <domain-review-workflow when available; otherwise omit for generic TASK>

Tasks:
  - Read the approved readable artifacts listed in RuntimeOverrides.
  - Draft review notes with citations to manifest/run/comparison IDs.
  - Record missing data as TBD.

ApplyEdits: true
AllowedWriteTargets:
  - <review notes path>
  - <TBD register path>

RuntimeOverrides:
  DomainEngineID: <domain_engine_id>
  ProfilePath: <profile path>
  ReadableArtifacts:
    - <path>
  ProtectedWritePaths:
    - <path or glob>

ExpectedOutputs:
  - Review notes
  - TBD register updates
```

### INIT-TASK Brief Example - Operation Proposal Draft

```markdown
PURPOSE: Draft a proposal-only domain operation from cited deterministic evidence.
RequestedBy: WORKING_ITEMS

ScopePath: <approved proposal folder>
Workflow: <domain-operation-proposal workflow when available; otherwise omit for generic TASK>

Tasks:
  - Draft one operation proposal.
  - Use only cited manifests, warnings, run IDs, comparison IDs, and human-provided requirements.
  - Mark the output as proposal_only.

ApplyEdits: true
AllowedWriteTargets:
  - <proposal yaml path>

RuntimeOverrides:
  DomainEngineID: <domain_engine_id>
  BaseStateID: <state id or TBD>
  Evidence:
    - <file or ID>
  ProfessionalBoundaryNotice: <required notice>

ExpectedOutputs:
  - Operation proposal file
  - Blockers and unresolved assumptions
```

### HELPS_HUMANS Requirement Brief Shape

When WORKING_ITEMS identifies a tool need, report it in this shape:

```markdown
HELPS_HUMANS_REQUIREMENT:
  RequestedBy: WORKING_ITEMS
  ToolCandidate: <name>
  Purpose: <deterministic operation>
  Inputs:
    - <input>
  Outputs:
    - <output>
  WhyToolNotAgent: <reason this is deterministic>
  WriteScope: <allowed output paths>
  FailureBehavior: <fail-fast behavior>
```

### HELPS_HUMANS Candidate Brief Shape

When WORKING_ITEMS identifies a workflow need, report it in this shape:

```markdown
HELPS_HUMANS_CANDIDATE:
  RequestedBy: WORKING_ITEMS
  SkillCandidate: <name>
  RecurringMethod: <bounded method>
  Evidence:
    - <session/brief/path showing repetition>
  SuitableShell: TASK
  ExpectedInputs:
    - <input>
  ExpectedOutputs:
    - <output>
  ToolNeeds:
    - <existing or candidate tools>
  QAExpectations:
    - <check>
```

### Handoff State

Each closure/handoff state should include:

| Field | Meaning |
|---|---|
| `RunStatus` | `SUCCESS | FAILED | BLOCKED | PARTIAL` |
| `DomainEngineID` | Active domain engine |
| `ProfileStatus` | Active profile state - one of `NONE | DRAFT | VALIDATED | ADOPTED | STALE | INVALID | UNKNOWN` |
| `IntegrationLevel` | Active approved level |
| `AcceptedUpstreamSnapshots` | Any accepted Chirality/domain snapshots consumed |
| `DomainArtifactsRead` | Files/IDs read |
| `DomainToolsInvoked` | Tools and modes |
| `AgentArtifactsWritten` | Proposal/review/checklist files written |
| `ProtectedPathsTouched` | Must be `none` for direct agent writes |
| `HumanApprovals` | Approval references or `TBD` |
| `BoundaryNoticesApplied` | Professional/IP notices used |
| `RerunRequirements` | Required scans, summaries, validations, comparisons |
| `RemainingBlockers` | Open issues and next owner |
| `NextOwningWorkflow` | `HUMAN | WORKING_ITEMS | TASK | HELPS_HUMANS | WORKING_ITEMS (workflow: change) | WORKING_ITEMS (workflow: project-setup) | DOMAIN_ENGINE_APP | EXTERNAL_PROVER` |

---
