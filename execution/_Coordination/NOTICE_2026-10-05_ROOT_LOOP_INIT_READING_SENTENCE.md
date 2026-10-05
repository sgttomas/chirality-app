# Notice: one sentence of App v4's LOOP_INIT changed (Root tranche ROOT-LOOPINIT-AUM-ALIGNMENT-20261005, 2026-10-05)

**To:** the App v4 development loops. **From:** HELP_HUMAN (Claude Code session), by the owner's direction recorded in `execution/_Coordination/AgentRuns/ROOT-LOOPINIT-AUM-ALIGNMENT-20261005/OWNER_DECISIONS.md`. That path is relative to the repository root.

**What changed.** In `projects/chirality-app-v4/loop/LOOP_INIT.md`, the last sentence of "When to read further" now reads:

> If you are unsure whether a section matters, read it.

It used to read "If you are unsure whether something matters, ask the human." The old sentence conflicted with Root `AGENTS.md`: "uncertainty alone does not require an extra prompt". The new one keeps the reading decision with the agent, as the owner's guidance on LOOP_INIT intends. Nothing else in App v4's LOOP_INIT changed. Piping's LOOP_INIT took the same binding form, with this sentence, in PR #1092. The Agent User Manual is updated in the same tranche as this notice.

**What it affects in App v4.** Seven pins in App v4's product resources record files this tranche changes.

**The previous LOOP_INIT,** sha256 `45c23cf477e23aff1d0152189caf7e8ebfb53eca42e3a1fae87a06af8c197f28`, is pinned three times:
- `app/src-tauri/resources/instructions/SOURCE_MAP.json`, entry `loop`;
- `app/src-tauri/resources/policy_standing/basis.json`;
- `app/src-tauri/resources/policy_standing/a16/basis.json`.

**The manual files the tranche also changes** are pinned four times:
- `docs/alignment-manual/README.md`, sha256 `31217d30b0d2743bef0d7c1a54bb9a81814d56b24ff0961cf01d9532952e305f`, in `SOURCE_MAP.json` (entry `manual_index`) and in `policy_standing/basis.json`;
- `docs/alignment-manual/CHIRALITY_AGENT_USER_MANUAL_v3.md`, sha256 `08ca0e40cd5157574a011bac57d539e77e9007a0d46494785da8b92745391b1a`, in `SOURCE_MAP.json` (entry `user_manual`) and in `policy_standing/basis.json`.

No test or source compares these hashes with the live files, so nothing fails. The recorded basis is now one revision behind.

**For the receiving loop to decide.** Whether, when and how to re-pin. For example, `a16/basis.json` may be a fixed historical basis that should stay as it is. This notice changes no App v4 resource, and running sessions keep the instructions they loaded until their next entry.
