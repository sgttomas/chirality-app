---
name: coordinated-knowledge-work
description: Use when related contributions must become one usable knowledge-work result and the team needs sustained ownership, independent assurance, shared changes, and completion.
metadata:
  kind: instruction
  surface: workflow
---
# Coordinated knowledge work

Use this method when several contributors — managers, bounded executors and reviewers — must produce one result that an owner will use: a software deliverable, an engineering document, a research finding. A single contributor carrying a bounded change does not need it.

## 1. Plan from the deliverables and test what the plan rests on

Agent 0 maps the deliverables and their dependency conditions, identifies who owns integration and which claims need independent examination, and chooses contributions that can carry the work through. The integration owner establishes how the combined result will be checked before the contributions widen: an executable check, a comparison with a named reference, or a judgment by a named role. Where the work has that shape, carry a thin version through to its final place first, for example one representative section taken from its source to the delivered document, so that the combined check runs on something real before effort multiplies. Decide which contributions need a persistent owner, which can be bounded assignments, and what each must receive before starting. The reported piping corpus used persistent managers, bounded executors and separate reviewers; the [experience notes](REVIEW-NOTES.md) retain that arrangement and its limits.

Before building on a premise — a design rationale, an interpretation, a figure taken from another contributor — check it against the purpose it serves. Work that passes its own checks can still rest on a premise nobody tested, and expanding that work multiplies the defect.

## 2. Brief so the owner can carry the work through

Give the assignment in full in the dispatch: the integration owner, exact input basis, deliverables, the acceptance criteria and the check that will be applied to the return, write boundary, review route and decision rights, the ordinary decisions the contributor may make, and conditions requiring escalation or a stop. Say who applies the check where the contributor cannot. A contributor may run that check on its own work; it does not reshape it. The contributor retains ownership through ordinary repairs. Its first useful return should be a substantive output or a precise obstacle, rather than a request for permission to perform the next ordinary step.

For each host and dispatch route, establish what instructions and context a contributor actually receives and can retrieve. Carry the applicable host, safety and data rules that route does not reliably supply, including rules that prevent silent failures. Name authoritative repository resources and their revision; verify access where a missed rule would matter. If the contributor has no other usable context, supply it in the brief. An established route need not be investigated again at every dispatch unless its behavior or relevant conditions change.

Name the return route: how a finished or blocked owner reaches the coordinator, giving the exact version, the checks performed and any open choice in a few lines. A completion that lands where the coordinator is not watching looks like silence from both sides. Prefer a route the host actually delivers to the integration owner, such as a supported blocking wait or completion notice. Where delivery depends on a contributor sending a message, or the coordinator may stop first, choose a recovery mechanism the host supports, proportionate to the cost of a missed return. Follow host prohibitions on polling or timers. If needed recovery is unavailable, state the limitation and choose a dispatch route that can deliver the result. A recovery mechanism inside the coordinator's session stops with it.

If satisfying an expectation would require removing, narrowing, or bypassing an existing check, pause that affected change and expose the conflict. Establish the requirement and authority for any change to the check; a newly passing result does not justify weakened assurance. The same stop applies when a contributor concludes that a criterion itself is mistaken. It neither edits the criterion nor works around it, and sends its reason and evidence through the integration owner to whoever holds that commitment. The integration owner does not rule on a commitment that is not its own. Continue unaffected work.

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

Stop at the agreed result supported by adequate evidence, not when every imaginable improvement is exhausted. That evidence includes the combined check applied to the integrated version. Report a criterion still in dispute as open, not as met. If the work must pause first, leave it recoverable from its own records: each open contribution's description states its exact version, what was checked on it, what remains and the next step, and the deliverables reflect what was done. No separate handoff document is needed.

The [experience record and application notes](REVIEW-NOTES.md) give the evidence behind this method and its limits.
