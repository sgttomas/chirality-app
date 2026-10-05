# Notice: construct-local-work-graph wording revised (Root tranche ROOT-CONSTRUCT-LOOPINIT-WORDING-20261005, 2026-10-05)

**What changed.** Two sentences of the bundled `workflows/construct-local-work-graph/WORKFLOW.md` changed, approved by the owner. The record is `execution/_Coordination/AgentRuns/ROOT-CONSTRUCT-LOOPINIT-WORDING-20261005/OWNER_DECISIONS.md`, relative to the repository root.
1. **The introduction** now says `LOOP_INIT.md` "supplies, or points to," the evergreen procedure. A LOOP_INIT in the binding form, such as App v4's or Piping's, points to the bundled workflows instead of restating them.
2. **§3's list of loops that adopt the method's receipt convention** now reads "(currently App, App v4, Piping and PEC)".

**What did not change:** the method itself, its template and its description. The workflow index is unchanged.

**For the receiving loop.** No action is required. A loop that pins or packages this workflow's bytes decides whether and when to re-pin. Running sessions keep the instructions they loaded until their next entry.
