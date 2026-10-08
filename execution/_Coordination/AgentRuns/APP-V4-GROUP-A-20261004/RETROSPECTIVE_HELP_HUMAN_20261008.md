# Retrospective — HELP_HUMAN session 2026-10-07/08 (Claude Opus 5.5, Claude Code)

The owner asked for this before the handoff: an evaluation of HELP_HUMAN's
own performance, any recommended changes to `coordinated-knowledge-work`,
and the behaviours the successor should and should not follow.

**Basis.** Workflow `chirality-root:bundled:workflow:coordinated-knowledge-work`,
`WORKFLOW.md` sha256 `44049bcd38b88378cd757ea34516f01edb0b0e93d8e9e3ac2b47ac61c9271b18`,
read in full for this assessment. The evidence is this run's reviews V7–V16,
DISPATCH and OWNER_DECISIONS.

This is self-assessment. It is not an independent review, and it accepts
nothing.

## What the session produced

- The resume recovered the paused checkpoint and the lost machine-local
  resources, with the owner's download approvals.
- The connected journey (J1–J5) was built, reviewed and integrated in PR 1113.
- A first native witness found a real usability defect (D-1). That led to
  two owner decisions and a Design change (CC-WR-RECONFIRM).
- J6 and J8 were built, reviewed, repaired and integrated.
- A second native witness confirmed the repairs.
- PR 1115 carries J6, J8, the second witness and the run records.
- Each implementation passed through an independent review. Every first
  review found at least one real defect, and every repair was confirmed by
  the reviewer who raised it.

## What worked, and should continue

1. **Prove the usable path natively, early (§1).** The first native witness
   found D-1: an unreadable dialog, where Return silently registered. More
   than 600 passing tests could not have found it. Without the witness, the
   gate account would have rested on component evidence alone.
2. **Keep owners and reviewers through repairs (§2, §3).**
   - The J5 owner carried J8 through its repairs and the merge with J6.
   - The V14 and V15 reviewers each confirmed their own findings (R1).
   - Confirmation rounds were cheap and fast because the reviewer already
     held the context.
3. **Verify each return before relying on it (§3).** Before relying on a
   hand-back, HELP_HUMAN checked:
   - branch ancestry;
   - the log hashes against the return;
   - that the integrated `app/` bytes equal the reviewed candidate (an empty
     `git diff`).

   The last check let one review warrant carry through an integration
   without a rebuild.
4. **Send each shared premise to its owner (§5).**
   - The owner decided the identical-bytes question (re-confirmation) and the
     dialog default key, each with exact words recorded.
   - Conflicts between design rules (CI-24, CI-25) were logged for their
     owners, not silently resolved in code.
5. **Pace the work around the human.** Point-specific approvals were asked
   only at real decision points. The owner pressed only the dialog acts, one
   at a time; everything else was driven for them.

## Where HELP_HUMAN fell short

1. **The coordinator's own records overclaimed, repeatedly. This is the main
   failure.** Independent reviews caught HELP_HUMAN's own wording four times:
   - V12 F1: a 90% gate weighting attributed to the owner.
   - V14-R1 R1-1: "Return and Escape never act", recorded, and told to the
     owner, before it was observed.
   - V16 F2–F7: "Return chose Don't register", "only the middle button
     acted", "D-3 repaired", and unretained screens cited as evidence.
   - V16 F1: "kept byte for byte". The files were never committed; see
     item 2.

   The pattern was the same each time: an inference or an expectation
   written as an observation. Each time it then spread into several records
   (CI-22, OWNER_DECISIONS, WORK_GRAPH, the PR body), so the repair took
   edits in several files (§5).
2. **Evidence retention was claimed but never checked in the committed
   form.**
   - The repository ignores `**/.chirality/`, so the witness workspace
     records were silently left out.
   - That included witness 1113, whose PR merged with the false claim.
   - Nobody ran `shasum -c` from a clean checkout until V16.
3. **Evidence was lost to clean-up order.** The scratch Codex home was
   deleted at the owner's choice before the model-reply excerpt, which held
   no credential, was copied into evidence. The reply is now not verifiable.
   The order should have been: retain, verify, then offer clean-up.
4. **A dispatch error.** The V15 reviewer was launched without worktree
   isolation and wrote into the HELP_HUMAN checkout. It was harmless here,
   but it weakened the custody boundary.
5. **Native witnessing was slow and costly.**
   - The App page carries the full review JSON, often thousands of lines,
     and jumps to the bottom after every native dialog.
   - Background clicks do not reach the Tauri web view.
   - Most of the witness time went on scrolling and screenshots, not on
     observing. This was not raised as an App defect until O-3/O-4.
6. **Owner-facing statements ran ahead of evidence.** The Escape claim
   reached the owner as a fact in chat before it was established. Status
   reports to the owner need the same discipline as the records.

## Recommendations for `coordinated-knowledge-work`

These are recommendations only. Root `AGENTS.md` requires the
`create-workflow` workflow for any revision, done by HELPS_HUMANS, with the
owner deciding. HELP_HUMAN has not edited the workflow.

The workflow's guidance held up well. The failures above came from
HELP_HUMAN not applying it, mostly not from gaps in it. Two additions would
have prevented the two costliest failures. Both are general to knowledge
work:

- **R-1 (§3 or §5): the coordinator's own records are returns too.** §3
  says "verify consequential claims against the output and evidence" for
  returns. The coordinator's own records, status statements and PR
  descriptions should face the same test. One way to write it: "Write an
  observation only for what the retained evidence shows; label inferences
  and expectations as such; a coordinator's statement to the decision owner
  is a consequential claim." An independent check of coordination records
  before merge (V16) found real defects, which supports this.
- **R-2 (§6): check retention where the result will be consumed, and
  retain before clean-up.** §6 already says "preserve the result … identify
  local-only recovery dependencies". It could add: verify that preserved
  evidence exists in its shared or committed form, not only in the
  producer's local copy (ignore rules, local-only files and uncommitted
  paths can make a retention claim false). Extract non-sensitive evidence
  before removing the environment that produced it.

Optional, as experience notes rather than rules: these observations could
be added to `REVIEW-NOTES.md` as experience records, which "add no
execution gates". No other change is recommended; adding more process would
go against the workflow's own §6 stopping rule.

## For the successor: behaviours to follow

**Do:**
- Use what this run already established. Read the handoff, then enter at
  the unfinished decision; do not restart (§ intro). The next item is C1,
  bounded reconciliation.
- Give every child its own worktree (`isolation: "worktree"`), reviewers
  included. Have it switch to its base branch inside that worktree first.
- Keep the same owner through repairs and the same reviewer for
  confirmation. Use a fresh reviewer for each new candidate and for the PR
  head.
- Before relying on a return, check ancestry and log hashes. Copy its logs
  into `validation/` with `SHA256SUMS`. Prove that the integration preserved
  the reviewed bytes (empty `git diff` against the reviewed candidate).
- Write records from retained evidence:
  - Before claiming anything is retained, run `shasum -c` against a clean
    `git archive` of the head.
  - Use `git add -f` for anything under a `.chirality/` path.
  - Separate observed, inferred and not retained.
  - Say who performed each step.
- For native witnesses:
  - Get point-specific approval for one artifact and one plan.
  - The owner performs every act; HELP_HUMAN drives everything else.
  - Grant screenshot access to `UserNotificationCenter` to record the alert,
    but never click it.
  - Retain evidence before any clean-up.
- Tell the owner only what is established, and name what is expected but
  not yet observed.
- Run C1 within §6's bounds:
  - Map each obligation to existing reviewed evidence and reuse those
    warrants.
  - State residuals truthfully.
  - Do not let reconciliation grow into a new audit.
  - The owner decides 90%.

**Do not:**
- Do not record an expectation as an observation, in records or in chat.
- Do not say evidence is "kept" until it verifies from the committed head.
- Do not delete or log out of an environment before extracting its
  non-sensitive evidence.
- Do not resolve a design-rule conflict in code without logging it for its
  owner.
- Do not widen scope:
  - SEAL-2 stays deferred.
  - SWBPIPE, PEC and Domains stay with their owners.
  - The optional follow-ups (R1-1 code, O-1…O-3, D-3 compact JSON) are not
    hidden gates for C1.
- Do not poll CI or agents in loops. Wait for notifications, and do
  independent work meanwhile.
- Do not fill parallel slots for their own sake. This run used at most two
  implementers and two reviewers at a time, and that was enough.

## Graph traversal advice

- **Batching.** The productive rhythm was: build the next connecting piece,
  get an independent review, repair, have the reviewer confirm, integrate,
  witness natively where human behaviour matters, then open one PR per
  batch with a head review.
- **Parallelism.** Two independent branches (J6, J8) ran well in parallel
  when the coordinator named the shared files and routed the overlap at
  integration (a merge with both sides kept). Note in each brief which
  shared files another branch is touching.
- **Where the remaining work lies.** It is mostly reconciliation and
  records (C1, M1, F1), not code. Cost and risk now sit in claims, not in
  compilation, so apply the "do" list on records especially strictly.
