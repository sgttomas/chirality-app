# INIT — 4_DOCUMENTS Enrichment Prompt

Read these files in order:

1. `/Users/ryan/ai-env/projects/chirality-app/README.md` — project context and filesystem paths
2. `/Users/ryan/ai-env/projects/chirality-app/AGENTS.md` — agent index and runbooks
3. `/Users/ryan/ai-env/projects/chirality-app/agents/AGENT_CHIRALITY-APP.md` — framework boundaries and workflow guidance

Then orient to the current workspace:

- Read `/Users/ryan/ai-env/projects/chirality-app/test/execution/_Coordination/_COORDINATION.md`
- Confirm the execution workspace exists at `/Users/ryan/ai-env/projects/chirality-app/test/execution/`
- (Optional) list deliverable folders under `/Users/ryan/ai-env/projects/chirality-app/test/execution/*/1_Working/`

Task: Run the 4_DOCUMENTS enrichment process for deliverable working-item folders.

Next session orientation:

- Begin directly in PKG-03 (`test/execution/PKG-03_*` folders); read only the `_CONTEXT.md`, `_REFERENCES.md`, and any reference sections needed for that specific package and its deliverables.
- You do not need to verify or re-read earlier deliverables—the updated drafts and `/_Coordination/_COORDINATION.md` already capture the current state. Trust that the deliverables listed are `INITIALIZED`.
- Keep relationships between deliverables limited to what is obvious within the current package; stay focused on the package scope, decomposition notes, and the deliverable ID(s) you are assigned. Try to minimize reading outside PKG-03 unless a later instruction explicitly references another package.

Current status:

- PKG-00 (DEL-00.01 through DEL-00.08) enrichment completed and logged in `_COORDINATION.md`.
- PKG-01 (DEL-01.01 through DEL-01.04) enrichment completed and logged in `_COORDINATION.md`.
- PKG-02 (DEL-02.01 through DEL-02.09) enrichment finished with three coordinated passes and logged in `_COORDINATION.md`; references remain to be added in each `_REFERENCES.md`.
- Next expected package: PKG-03 (DEL-03.01 through DEL-03.06), unless the user specifies otherwise.

Operating rules:

- Follow `/Users/ryan/ai-env/projects/chirality-app/agents/AGENT_INSTRUCTIONS_BUNDLE_2026-01-28_v3/AGENT_4_DOCUMENTS_REVISED_v3.md`
- Each invocation performs three enrichment passes and overwrites existing drafts
- Do not modify metadata files (`_CONTEXT.md`, `_DEPENDENCIES.md`, `_REFERENCES.md`)
- Log each deliverable completion in `test/execution/_Coordination/_COORDINATION.md` under "4_DOCUMENTS Enrichment Log"
- Commit changes as directed by the user (typically after each deliverable)
- Keep working through the deliverables the user specifies for this session; when done, ask for the next batch. Stop only when the user says there are no remaining tasks.

Start prompt to user:

"Which deliverable(s) should I enrich next? Provide DEL-ID(s) or a package range."

Persistent notes (carry these forward):

- The workspace now reflects the current status for PKG-02; a future agent does *not* need to retrace the preceding work to know what happened. Trust the lifecycle entries in `_COORDINATION.md` and the updated deliverable drafts as the authority on where things stand.
- Keep the focus narrowly on the package and deliverables identified for your session (PKG-03 in this case). Read only their `_CONTEXT.md`, `_REFERENCES.md`, and anything directly needed for the four documents you are enriching; do not revisit earlier packages unless specifically asked.
- Project context (scope, objectives, decisions captured in the decomposition) is important for each PKG-03 deliverable, so make sure the agent has quick access to the relevant sections but skip re-reading older material. Relationships between deliverables beyond what’s stated in the current package are not part of the task unless explicitly pointed out.
