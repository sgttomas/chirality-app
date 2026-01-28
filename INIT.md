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

Current status:

- PKG-00 (DEL-00.01 through DEL-00.08) enrichment completed and logged in `_COORDINATION.md`.
- PKG-01 (DEL-01.01 through DEL-01.04) enrichment completed and logged in `_COORDINATION.md`.
- Next expected package: PKG-02 (DEL-02.01 through DEL-02.09), unless the user specifies otherwise.

Operating rules:

- Follow `/Users/ryan/ai-env/projects/chirality-app/agents/AGENT_INSTRUCTIONS_BUNDLE_2026-01-28_v3/AGENT_4_DOCUMENTS_REVISED_v3.md`
- Each invocation performs three enrichment passes and overwrites existing drafts
- Do not modify metadata files (`_CONTEXT.md`, `_DEPENDENCIES.md`, `_REFERENCES.md`)
- Log each deliverable completion in `test/execution/_Coordination/_COORDINATION.md` under "4_DOCUMENTS Enrichment Log"
- Commit changes as directed by the user (typically after each deliverable)
- Keep working through the deliverables the user specifies for this session; when done, ask for the next batch. Stop only when the user says there are no remaining tasks.

Start prompt to user:

"Which deliverable(s) should I enrich next? Provide DEL-ID(s) or a package range."
