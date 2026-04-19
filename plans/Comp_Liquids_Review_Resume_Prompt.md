# Comp & Liquids Review Resume Prompt

Use this prompt to resume after context compaction.

---

## Campaign Context

You are the campaign controller (SCOPE_CHANGE persona, Opus) for the West Doe Two-Root DBM Remediation and Publication Campaign. The campaign has 8 phases. You own Phases 1, 2, and 7.

**Completed:**
- Phase 1: Authority freeze (`plans/Campaign_Authority_Freeze.md`)
- Phase 2: Allocation matrix frozen (`plans/Authority_Allocation_Matrix.csv`, 26 rows)
- Phase 3-4: Deepcut remediation complete (SCA-003 applied, Phase 4 regeneration done)
- Phase 5-6: Comp & Liquids remediation complete (SCA-003 applied, Phase 6 regeneration done)
- Deepcut review + repair pass complete (`plans/Deepcut_Review_Run_Summary.md`)

**Pending:**
- Comp & Liquids review + repair pass (THIS TASK)
- Phase 7: Cross-root conformity gate (after both reviews complete)
- Phase 8: Publication (separate sessions)

**Key campaign artifacts:**
- `plans/WEST_DOE_TWO_ROOT_DBM_REMEDIATION_AND_PUBLICATION_PLAN.md`
- `plans/WEST_DOE_EXECUTION_MODEL.md`
- `plans/Campaign_Authority_Freeze.md`
- `plans/Authority_Allocation_Matrix.csv`
- `plans/Deepcut_Terminology_Decisions.md`
- `plans/Deepcut_Review_Run_Summary.md`
- `plans/DEEPCUT_DECOMPOSITION_AND_FOLDER_REVIEW_PLAN.md` (reference for how Deepcut review was done)

## Your Task Now

Execute the review + repair plan at `plans/COMP_AND_LIQUIDS_DECOMPOSITION_AND_FOLDER_REVIEW_PLAN.md`.

This plan follows the same pattern as the Deepcut review you already completed. Read the plan first — it defines the exact execution sequence, scope boundaries, repair rules, and required outputs.

## How You Did the Deepcut Review (pattern to follow)

1. **Phase 1 (baseline inventory):** Enumerated all files under `_Decomposition/`, `_ScopeChange/`, and all KTY folders. Recorded counts.

2. **Phases 2-4 and 6 (heavy lifting):** Dispatched three Opus agents in parallel:
   - Phase 3 agent: decomposition parity cross-checks across all registers
   - Phase 4 agent: KTY metadata review across all folders (_CONTEXT.md, _STATUS.md, _REFERENCES.md consistency)
   - Phase 6 agent: terminology and interface sweep (LPG, FUTURE, Pembina HVP, flare, incinerator, cross-facility)

3. **Phase 5 (classification):** Synthesized findings into 4 buckets: DECOMP_LOCAL_REPAIR, KTY_METADATA_REPAIR, DOMAIN_DOCUMENTS_RERUN, HUMAN_DECISION_REQUIRED.

4. **Phase 7 (repair execution):** Dispatched parallel agents for mechanical repairs:
   - Sonnet agents for CSV register fixes (ledger, subject register, KTY register)
   - Direct edits for vocabulary map, KTY metadata, terminology decisions
   - Opus agent for main doc Coverage & Open Issues refresh

5. **Phase 8 (downstream):** Dispatched parallel agents for regeneration:
   - Sonnet for domain-documents reruns (one KTY per agent)
   - Opus for DOMAIN_HYPERGRAPH and AUDIT_DECOMP
   - Sonnet for terminology QA verification sweep

6. **Wrote run summary** at `plans/Deepcut_Review_Run_Summary.md`.

## Key Lessons from Deepcut Review

- The plan assumed 132 KTY folders but actual count was 98. Verify actual counts before proceeding.
- SCA-001 retirements were frequently not propagated to KTY metadata or register status columns.
- KTY Register column values (UnitCount, OpenIssueCount) drifted from Notes field values and ledger.
- Main doc Coverage & Telemetry block and Open Issues tables were stale.
- "Cross-Fence" was corrected to "Cross-Facility" as canonical term.
- Vocabulary map and terminology decisions file needed updates alongside decomposition fixes.
- Always update telemetry JSON after ledger corrections.
- The DOMAIN_HYPERGRAPH will likely have KA-naming blockers (DUPLICATE_NODE_ID) — these are pre-existing.
- After all repairs, run AUDIT_DECOMP to verify structural invariants still hold.

## Governing Contracts

Read these for the current write-scope rules:
- `agents/AGENT_SCOPE_CHANGE.md` (recently revised: DOMAIN write scope includes decomposition + annex CSVs + _ScopeChange)
- `skills/domain-documents/SKILL.md` (recently revised: metadata drift must be surfaced as follow-on, not fixed inside skill)
- `plans/WEST_DOE_TWO_ROOT_DBM_REMEDIATION_AND_PUBLICATION_PLAN.md` (recently revised: Phase 4/6 includes explicit metadata alignment step)

## Output

Write the run summary to `plans/Comp_Liquids_Review_Run_Summary.md` following the same structure as `plans/Deepcut_Review_Run_Summary.md`.

After the review is complete, both roots will be ready for Phase 7 (cross-root conformity gate).
