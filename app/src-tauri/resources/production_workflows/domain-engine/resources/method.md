# domain-engine — method

## Method

### Function 1 - Intake and Classification

**Goal:** Understand the domain-engine request and classify the integration level.

Actions:
1. Identify the domain engine, working root, desired workflow, and expected outputs.
2. Classify the request into one or more action types:
   - `PROFILE_ADOPTION`
   - `ARTIFACT_SCAN`
   - `READ_ONLY_REVIEW`
   - `DOMAIN_TOOL_INVOCATION`
   - `OPERATION_PROPOSAL`
   - `HANDOFF_WORKFLOW`
   - `BOUNDARY_AUDIT`
   - `FRAMEWORK_EXTENSION`
3. Identify whether the work is project-runtime work or framework-maintenance work.
4. State known profile status: `NONE | DRAFT | VALIDATED | ADOPTED | STALE | INVALID | UNKNOWN`.
5. Surface missing prerequisites as `TBD`.

Gate 1 question:

```text
I classify this as <ACTION_TYPE> at <INTEGRATION_LEVEL> for <DOMAIN_ENGINE_ID>. The current profile status is <STATUS>. Is that the correct target?
```

### Function 2 - Profile and Boundary Design

**Goal:** Establish or review the profile that defines safe integration.

Actions:
1. Locate or draft the Domain Engine Profile.
2. Identify and classify artifacts:
   - authoritative domain artifacts
   - Chirality-readable artifacts
   - agent-writable artifacts
   - protected write paths
   - domain-controlled write outputs
3. Identify human gates:
   - profile adoption
   - write-boundary approval
   - mutating tool calls
   - operation proposal application
   - handoff/reliance decisions
4. Identify boundary notices:
   - professional status limits
   - IP/data limits
   - external prover status limits
5. If a deterministic profile validator is missing, prepare a HELPS_HUMANS requirement brief.
6. If profile design becomes a recurring bounded method, prepare a HELPS_HUMANS candidate brief.

Gate 2 question:

```text
Do you approve this profile boundary: authoritative artifacts, readable artifacts, protected paths, agent-writable paths, declared tools, and human gates?
```

### Function 3 - Artifact Discovery and Readiness

**Goal:** Make domain-engine state legible without letting agents own it.

Actions:
1. Scan or request a scan of declared profile paths.
2. Prefer deterministic scanners when they exist.
3. If no scanner exists and the scan is mechanical, prepare a HELPS_HUMANS requirement brief.
4. Produce an artifact inventory that labels each file/folder by role.
5. Identify missing manifests, stale summaries, absent run IDs, missing comparison IDs, missing warnings, and missing assumptions.
6. Do not infer model state from unbounded raw internals when a bounded manifest is expected.

Output:
- artifact inventory
- missing/invalid profile evidence
- recommended next safe integration level

Gate 3 question:

```text
The artifact inventory says <SUMMARY>. May I proceed using these readable artifacts and these protected-path assumptions?
```

### Function 4 - Domain Tool Adapter Planning

**Goal:** Decide whether declared domain tools are safe to invoke.

Actions:
1. Read the profile's deterministic tool declarations.
2. For each requested tool, classify its mode:
   - `read_only`
   - `summary_write`
   - `domain_controlled_write`
   - `proposal_validate`
   - `proposal_apply`
3. Confirm input schema, output schema, output location, side effects, and failure behavior.
4. Confirm whether human confirmation is required before invocation.
5. Reject raw shell/API calls that are not declared by profile or approved by the human for this run.
6. If argument validation, output capture, or protected-path checks are deterministic and missing, prepare HELPS_HUMANS requirement briefs.

Gate 4 question:

```text
This tool plan will invoke <TOOLS> with mode <MODES>, write outputs to <PATHS>, and protect <PROTECTED_PATHS>. Do you approve this invocation plan?
```

### Function 5 - Runtime Orchestration

**Goal:** Route bounded work to the correct runtime layer.

Actions:
1. If the work is a bounded method already represented by a repo-native workflow, dispatch TASK with `Workflow`.
2. If the work is bounded but no workflow exists, either:
   - dispatch TASK in generic shell mode for one-off execution, or
   - prepare a HELPS_HUMANS candidate brief if the pattern is recurring.
3. If the work is deterministic and LLM-independent, prepare a HELPS_HUMANS requirement brief rather than doing it by prose.
4. If the work would write protected domain artifacts directly, stop.
5. If the work writes allowed proposal/review artifacts, restrict `AllowedWriteTargets` to profile-approved paths.
6. Require evidence fields in all review notes, proposal rationales, and handoff checklists.

TASK dispatch must use the bounded brief contract defined by `docs/AGENT_WORKFLOW_RUNTIME.md` and any target workflow's `brief.md`.

### Function 6 - Operation Proposal Workflow

**Goal:** Let agents propose domain changes without accepting them as truth.

Actions:
1. Confirm the profile permits operation proposals.
2. Confirm the proposal schema and allowed proposal path.
3. Draft or dispatch drafting of the proposal using only cited evidence.
4. Mark proposal status as `proposal_only`.
5. Invoke proposal validation only through declared deterministic tools.
6. Record warnings, blockers, assumptions, and required human rulings.
7. Do not apply the proposal unless the domain engine exposes a safe apply operation and the human explicitly approves it.

Gate 5 question:

```text
This proposal remains proposal-only. It may be validated by <TOOL> and cannot become accepted model truth without your approval. Proceed?
```

### Function 7 - Handoff and External Prover Workflow

**Goal:** Support professional validation workflows without claiming validation.

Actions:
1. Confirm whether the workflow is internal review, handoff preparation, or external-prover feedback intake.
2. Ensure handoff packages are generated by the domain engine or domain adapter, not by raw agent mutation.
3. Draft Chirality-side handoff checklists, TBD registers, review notes, and change-record scaffolds.
4. Label external prover comments as human-supplied or tool-supplied evidence.
5. Do not declare external validation complete unless an authoritative human-provided record states that status.

### Function 8 - Closure and Handoff State

**Goal:** End each domain-engine run with explicit state.

Actions:
1. Record what was read, written, invoked, proposed, or deferred.
2. Classify outputs as:
   - authoritative domain artifact
   - Chirality-readable artifact
   - agent-writable artifact
   - snapshot / handoff artifact
   - derived publication artifact
3. Record current profile status and integration level.
4. Record stale artifacts and rerun requirements.
5. Record remaining blockers and next owning workflow.
6. If a snapshot was produced, update only the approved pointer file.

Closure is invalid if:
- protected paths were directly edited by agents;
- mutating tools were invoked without required approval;
- proposal-only artifacts were described as accepted changes;
- professional or external validation status was invented;
- outputs affecting project reasoning exist only in chat.

---
