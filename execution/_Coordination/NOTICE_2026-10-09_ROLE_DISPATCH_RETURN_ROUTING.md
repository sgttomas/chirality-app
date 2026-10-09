# Notice: dispatch and return routing in the role files (2026-10-09)

**Source:** the Root instruction tranche `ROLE-DISPATCH-RETURN-ROUTING-20261009`.

**Change:**
- `agents/AGENT_WORKING_ITEMS.md`: on a host that ends a delegated run at its turn end and routes its contributors' late reports to its caller, a manager keeps its turn open until its dispatched work returns. It dispatches with blocking calls, batching independent work for parallelism, and reads returns from their records.
- `agents/AGENT_HELPS_HUMANS.md`: on such a host, keep the turn open until dispatched work returns, and read returns from their records.
- `agents/AGENT_HELP_HUMAN.md`: on such a host, managers get standing assignments, and a misrouted return gets a pointer to its record, not a relay.

**Basis:** On the Claude Code desktop host (Agent SDK, background and non-interactive subagents), reports from contributors that finished after their manager's turn ended went to Agent 0 (7 of 11 such cases in one session). Trials on 2026-10-09 showed that blocking dispatch keeps every report with the manager, including across chained batches.

**For the receiving loop:** This notice communicates the Root change; it does not adopt it on the loop's behalf. Decide adoption at the next applicable entry or governance review. Existing rulings remain in force.
