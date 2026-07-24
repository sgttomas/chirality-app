# D-GOV-14 — PR #188 review closure

Status:       RULED
HumanRuling:  APPROVED — owner response, 2026-07-12: "My rulings are `APPROVED` for all."
Proposed SHA: ee35409f5cf3a81ecb29a271527156b991df97b9
Ruling SHA:   d22f80bf5d6c1190ce151df75d936bfcf4d38bc3
Date:         2026-07-12
FramedBy:     PR #188 multi-agent review and author remediation

## Decision requested

The implementation and review establish the following decision slate. None of
these items becomes ruled through authorship, testing, PR approval, or merge.

1. **Accept the workflow-component standard text.** Ratify the exact
   `docs/WORKFLOW_COMPONENT_STANDARD.md` text at the review-closure commit as
   the external design standard applied by HELPS_HUMANS.
2. **Accept the decomposition standard text.** Ratify the exact
   `docs/DECOMPOSITION_STANDARD.md` text at that commit as the external
   protocol shared by PROJECT_DECOMP, SOFTWARE_DECOMP, and DOMAIN_DECOMP.
3. **Accept the software workflow profile.** Ratify the exact
   `docs/SOFTWARE_WORKFLOW_PROFILE.md` text at that commit as the activation
   profile contract for WORKING_ITEMS software packages.
4. **Approve or reject D-GOV-13's fourteen-role table.** Approval makes the
   named dedicated Agent 2 candidates executable subject to their declared
   caller and tool allowlists. Rejection leaves named execution fail-closed
   and requires replacement-first migration to TASK/skills/tools or separately
   ruled role proposals.
5. **Confirm SCHEDULING retirement.** Confirm that the standalone SCHEDULING
   persona is retired and its human-gated manager semantics belong to
   ORCHESTRATOR, with repetitive calculation/rendering delegated downward.
6. **Confirm the K-AGENTS-1 interpretation.** Under D-GOV-11, root `AGENTS.md`
   is authoritative for the Agent 0/1/2 hierarchy and live roster; the 3×4
   NORMATIVE/OPERATIVE/EVALUATIVE matrix remains deployment UI routing
   vocabulary, not a runtime-authority taxonomy and not a required root index.
7. **Confirm legacy bridge retirement.** The record-less SDK Agent bridge is
   disabled after managed-delegation acceptance; managed child sessions are
   the sole executable app-harness delegation path.
8. **Confirm the in-flight carve-outs.** The resumed app-dev and piping
   concordance proto-runs may finish under their pinned method revisions,
   recorded owner steers, established write surfaces, and existing
   TASK/subagent execution. They are not required to adopt or simulate the
   unmerged managed-delegation paradigm mid-run. At terminal handoff, each run
   must record its accepted source-state basis, closure state, unresolved
   blockers, and lessons relevant to the final RECONCILIATION contract. After
   both proto-runs are integrated, PR #188 must be rebased onto their accepted
   state and fully revalidated before merge.
9. **Confirm the public governance boundary.** Publish D-GOV decision records,
   the implementation handoff, and `human_actors.md` because public authority
   verification depends on them. Exclude private-project TRB briefs, the
   practitioner-development backlog, private-project CI, and private loop
   launchers. The owner identity and business email in `human_actors.md` remain
   intentionally public if this item is accepted.

## Implementation evidence

The review-remediation tranche supplies atomic write reservations, early child
identity recording, parent binding only after validation, read-only
control-plane denial, symlink-safe reads, claim-status authority checks,
versioned amendment/work-graph contracts, strict specialist tool/caller
allowlists, untracked-path containment, bounded check execution, fail-closed
legacy delegation, public-export boundary repair, paused-run compatibility,
and consistency corrections across governance and professional-practice docs.

## Owner ruling

The owner approved all nine items after receiving an item-by-item explanation
of their context, effects, alternatives, and the revised proto-run wording for
item 8. This ruling ratifies the three exact standards at the Proposed SHA,
approves D-GOV-13's fourteen-role compatibility baseline, and confirms items
5–9 as written above. Merge remains intentionally held until the two proto-runs
produce stable handoffs and the integration/revalidation sequence in item 8 is
complete.
