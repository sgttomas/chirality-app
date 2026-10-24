---
name: coordinated-knowledge-work
description: Use when related contributions must become one usable knowledge-work result and the team needs sustained ownership, independent assurance, shared changes, and completion.
---
# Coordinated knowledge work

Use this method when several contributors — managers, bounded executors and reviewers — must produce one result that an owner will use: a software deliverable, an engineering document, a research finding. A single contributor carrying a bounded change does not need it.

## 1. Plan from the deliverables and test what the plan rests on

Agent 0 will explore the deliverables and their dependencies to map out a path of work that can be delegated to Type 1 and Type 2 agents.

Before building on a premise — a design rationale, an interpretation, a figure taken from another contributor — check it against the purpose it serves. Work that passes its own checks can still rest on a premise nobody tested, and expanding that work multiplies the defect.

## 2. Brief so the owner can carry the work through

Agent 0 must name the input basis, deliverables, write boundary, review route, ordinary decisions they may make, and conditions requiring escalation or a stop. The manager agent's first useful return should be a substantive output or a precise obstacle—not a request for permission to perform the next ordinary step.

The brief is all the contributor knows. Carry the host, safety and data rules in it in full, including those that prevent silent failures, rather than assuming the contributor will find them.

Name the return route: how a finished or blocked owner reaches the coordinator, giving the exact version, the checks performed and any open choice in a few lines. A completion that lands where the coordinator is not watching looks like silence from both sides. Add a backstop that runs independently of the coordinator's session; a timer that lives inside that session stops with it.

If satisfying an expectation would require removing, narrowing, or bypassing an existing check, pause that affected change and expose the conflict. Establish the requirement and authority for any change to the check; a newly passing result does not justify weakened assurance. Continue unaffected work.

## 3. Re-derive shared generated artifacts

When two lanes change the same generated or registered artifact, whoever integrates second takes in the other's result and re-derives the artifact on top with its maintained tools. Never hand-merge generated files or pinned values.

## 4. Plan for shared limits

Contributors that draw on one budget — a usage quota, memory, disk, build or review capacity — stop together when it runs out. Size concurrency to the budget, not to the number of available units, and keep the finished work waiting for review within what reviewers can absorb. Reuse passing evidence instead of repeating it when work changes hands, and delete integrated work's worktrees, build output and scratch.

## 5. Move a reviewed contribution into use without restarting its review

For every ready contribution, ask **which claim remains unestablished**. Separate three questions:

| Question | Evidence that can answer it |
| --- | --- |
| Is the interpretation or transformation substantively correct? | Comparison with authoritative evidence, an independent derivation, or another check appropriate to the claim. |
| Does the required representation work? | Checks of the actual saved output: structure, rendering, meaningful typography, calculations, or other relevant behavior. |
| Did integration preserve the checked result and its relationships? | Scoped comparison with the reviewed version and checks of the actual consuming location, references, and affected dependencies. |

These are different warrants, not three compulsory approval rounds. A renderer or matching hash cannot establish source meaning. Conversely, a copied, unchanged table does not need another cell-by-cell source reading merely because it moved into the deliverable. Combine compatible placement and integration checks where the governing requirements permit.

Integrate only the version that was checked: confirm that the version under review is the version being integrated. Record coordination agreements — merge order, ownership, scheduling of exclusive resources — where the integration itself is reviewed (for software, the pull request description), not in the design or the deliverable.

Before ordering a repair, establish which actual artifact supports the finding. A stale preview or flattened extraction can manufacture an apparent discrepancy. If that representation is itself a required consumer output, repair it; otherwise correct the finding and preserve the valid result. Trace affected dependencies, not just changed file hashes.

## 6. Diagnose the waiting before adding people, tools, or interruptions

At a stalled or aging item, locate the next useful result and the person or operation that releases it. Then establish:

1. **Was the next task actually dispatched, and could its return reach the coordinator?** A completed turn followed by a queued message may leave an owner waiting while the coordinator believes work continues. A finished return delivered where the coordinator is not watching looks like silence from both sides.
2. **What actually ran or exists?** Inspect the last operation, saved or reported partial work, and available session/error state. Work may exist before a narrative handoff; absence of a file does not prove inactivity.
3. **Where is the elapsed time going?** Distinguish source reasoning, tool execution, preparation, review waiting, and integration waiting. State uncertainty where the host exposes no diagnosis.

Agent 0 should intervene when the undertaking's purpose, tradeoffs, or management approach need correction. Repeatedly asking Agent 1 to ask Agent 2 for another update is evidence that the arrangement needs attention, not a substitute for fixing it.

## 7. Finish when the authorized conditions are established

Stop at the agreed result supported by adequate evidence, not when every imaginable improvement is exhausted. If the work must pause first, leave it recoverable from its own records: each open contribution's description states its exact version, what was checked on it, what remains and the next step, and the deliverables reflect what was done. No separate handoff document is needed.

The [experience record and application notes](REVIEW-NOTES.md) give the evidence behind this method and its limits.
