# Follow-up notice: the seven pinned hashes need no re-pinning (Root tranche ROOT-AUM-PEC-AND-FOLLOWUPS-20261005, 2026-10-05)

**To:** the App v4 development loops. **From:** HELP_HUMAN (Claude Code session), by the owner's direction to clean up the items left for later. The record is `execution/_Coordination/AgentRuns/ROOT-AUM-PEC-AND-FOLLOWUPS-20261005/`, relative to the repository root.

**What this follows.** `NOTICE_2026-10-05_ROOT_LOOP_INIT_READING_SENTENCE.md` listed seven hashes in App v4's product resources that tranche ROOT-LOOPINIT-AUM-ALIGNMENT-20261005 (#1094) made stale. It left the receiving loop to decide whether to re-pin them.

**What the follow-up found.** The seven hashes are point-in-time records of what two App v4 TASKs consulted, and nothing App v4 derived from those files is affected.
- **`policy_standing/basis.json`** records one TASK's consultation basis: its role, parent, mechanism, model and base `38bb2bc87a`. **`policy_standing/a16/basis.json`** records a consultation and its sources. **`instructions/SOURCE_MAP.json`** records the sources its author read for App v4's bundled `AGENTS.md` and `agents/*.md`.
- **Each entry states what was read at that time.** Several other entries in the same files already differ from current files after App v4's own later changes. Updating a hash without re-reading would misstate what was consulted.
- **The candidates depend on these exact bytes.** Each `policy_standing/**/candidate.json` pins its `basis.json` by hash, so editing a basis would also break that candidate's provenance.
- **No App v4 code or test reads these maps.**
- **The changed files were read only in parts that did not change:**
  - `SOURCE_MAP.json` gives LOOP_INIT's read extent as "Execution entry only; not product defaults", and none of App v4's bundled instruction files contains the changed sentence.
  - It gives the Agent User Manual's read extent as "Headings to level three only", and those headings are unchanged.
  - It gives the alignment-manual README's read extent as "Current editions", and the editions are unchanged; #1094 changed only the README's render-basis lines.
- **This tranche changes the Agent User Manual and the README again.** The AUM's PEC statements are corrected with its headings unchanged; the README gets a new render basis and a pointer to the v8 revision's production note. Both are read only in parts that did not change, so the `user_manual` and `manual_index` pins, and the matching entries in `policy_standing/basis.json`, now trail by two revisions. The recommendation is the same.

**Recommendation.** Leave the seven hashes as they are, as records of what was read. A loop that next re-authors App v4's bundled instructions or re-derives a policy-standing basis records the bytes it actually reads at that time.
