  You are taking over SDK cutover work in `/Users/ryan/ai-env/projects/chirality-app`.

  Primary objective:
  - Execute a wholesale migration from CLI subprocess runtime to Anthropic Agent SDK.
  - No dual runtime path and no legacy junk left behind.

  Source of truth:
  - `frontend/AGENT_HARNESS_SDK_CUTOVER_CHECKLIST.md`
  - Follow Task IDs and phase commit batches exactly (`P0-C1` through `P5-C1`).

  Critical constraints:
  1. Preserve current SSE `UIEvent` contract and `ChatPanel` behavior.
  2. Keep Chirality workflow overlays (persona/system append prompting).
  3. Configure SDK for Claude Code parity:
     - `systemPrompt` preset `claude_code` + append
     - `tools` preset `claude_code`
     - explicit `settingSources`
     - parity for resume/model/maxTurns/permission behavior (`dontAsk` -> bypass permissions behavior).
  4. Remove `/api/chat`, CLI manager, and NDJSON parser only in planned removal phase.
  5. Keep changes minimal, reversible, and commit-batch scoped.

  Progress tracking protocol (required after each completed task):
  1. In `frontend/AGENT_HARNESS_SDK_CUTOVER_CHECKLIST.md`:
     - Mark completed checklist items as `[x]`.
     - Keep Task IDs as canonical status.
  2. For each finished commit batch:
     - Append an entry to `frontend/AGENT_HARNESS_SESSION_LOG.md` including:
       - date/time
       - batch ID (e.g., `P2-C1`)
       - completed Task IDs
       - commit SHA
       - validation results
       - blockers/risks (if any)
  3. Use commit message format:
     - `<type>: <batch-id> <task-id list>`
     - Example: `feat: P2-C1 RT-004 RT-005 RT-008 API-001 API-002`

  Execution requirements:
  - Start by confirming repo state, then run `P0-C1`.
  - Use the plan tool and track status by Task IDs.
  - For each batch: implement, validate, summarize changed files + results + next batch.
  - If parity/performance regresses, stop and recommend rollback to baseline tag.

  Deliverable after each batch:
  - Completed Task IDs
  - Files changed
  - Validation outcomes
  - Next batch recommendation
