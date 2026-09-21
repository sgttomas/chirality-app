# audit-agents — method

## Method

### Step 0 — Preconditions

1) Confirm the invocation brief is readable and names its authorized caller: HELP_HUMAN may dispatch bounded TASK work directly, or a Type 1 manager may dispatch it.
2) Confirm `RUBRIC_FILE` exists and is readable.
3) Confirm `FILES_TO_AUDIT` is non-empty.
4) Confirm `CANON_FILE` exists.
   - If canon is missing: still run inventory + drift detection; mark canon-dependent checks as `BLOCKER`.
5) Run `python3 {INSTRUCTION_ROOT}/tools/validation/validate_agent_instructions.py --repo-root {INSTRUCTION_ROOT} --json <requested-role-files>` and include its findings as structural evidence. When workflow packages are explicitly in scope, also run `python3 {INSTRUCTION_ROOT}/tools/validation/validate_workflow_metadata.py {INSTRUCTION_ROOT}/workflows --json` and retain the results for the scoped packages; distinguish structural checks from semantic review.

---

### Step 1 — Bind the reviewed component and its configuration

For each audited role file, record its path, revision, and hash; resolve its role entry in agents/registry.json and record type, instruction path, direct-entry and delegation eligibility, capability ceiling, and write-scope ceiling. Read the role’s four sections for its actual characteristic behavior.

For each explicitly included workflow or tool, record the selected entrypoint/resources, execution configuration, input/output contracts, callers, and accepted source basis. Compare actual write behavior with the applicable workflow and brief targets; a role’s prose is not an output-path registry.

---

### Step 2 — Apply the rubric

Apply the actual sections of docs/rubrics/AUDIT_AGENT.md:
- **Roles:** assess distinct attention and judgment, contributions of the four sections, human/role relationships, placement of methods and metadata, and concise expression.
- **Workflows and tools:** for included components, trace inputs through return, branches, recovery, authority, independence, resource selection, evidence, outputs, and effective permissions.
- **Findings and disposition:** record the observed excerpt or behavior, applicable contract, practical impact, proposed correction, and unresolved decision.

Produce one reviewed-component record per scoped file and a suite synthesis when the relationships span multiple files. Record the reviewed revisions and human decisions once; report which rubric questions apply to each component.

For any `PARTIAL` or `NONCONFORMANT` result:
- include evidence excerpt (≤25 words) with a location,
- include canon excerpt (≤25 words) with a location (if available),
- propose the minimal fix (rewrite block or diff hunk).

---

### Step 3 — Issue log

Produce a prioritized Issue Log with columns:
- `ID`, `Severity`, `File(s)`, `Type`, `Symptom`, `Evidence`, `CanonRequirement`, `Fix`

Severity guidance:
- `BLOCKER` — invalid authority, capability, scope, or executable contract
- `HIGH` — changes substantive results, decisions, or reliable handoff
- `MEDIUM` — material ambiguity, duplication, or compatibility drift
- `LOW` — local clarity or hygiene defect
- `INFO` — relevant observation without a demonstrated defect

---

### Step 4 — Patch plan

Produce the patch plan required by the brief:
- In CONFORMANCE mode, prefer the smallest coherent repair against the accepted basis.
- In authorized REDESIGN mode, describe the intended role or component change and the contracts it supersedes.
- Make routine repair choices explicit; route unresolved changes to intent, authority, or acceptance criteria to the caller.

Do not apply patches.

---

### Step 5 — Publish snapshot and return summary

1) Write all artifacts into the run snapshot folder.
2) Update `_LATEST.md` pointer.
3) Return to the invoking manager:
   - snapshot path,
   - top issues (≤10),
   - blockers and recommended next action (accept / request WORKING_ITEMS (workflow: change) patches / rerun tighter scope).

---
