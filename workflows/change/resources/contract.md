# change — contract

## Non-negotiable invariants

- **Human owns decisions.** WORKING_ITEMS proposes; the human decides.
- **No invention.** Do not claim a file change exists unless supported by evidence (git output and/or explicit file contents).
- **Disjoint write scopes are the default concurrency control.** When agents hold non-overlapping write scopes inside the monorepo and commit frequently, preserve the shared checkout. Do not introduce worktrees merely because work is concurrent.
- **Worktrees are explicit isolation lanes.** Use branch + worktree lanes when the human asks, or when isolation materially reduces risk (overlapping write scopes, concurrent root governance edits, risky refactors, long-lived/speculative work, generated-output churn, tool/process interference).
- **`main` is the default integration branch.** Unless the human names another, treat `main` as accepted integrated state and branch task work from it.
- **Branches are candidate work, not accepted truth.** A task branch/worktree does not make governed state closed. Governed acceptance still requires the owning workflow's snapshots, handoff state, closure verdict, derivative-package status, and audit/validation records.
- **Authorized integration.** In `sgttomas/chirality`, apply the standing owner authorization in `docs/PRD_ROOT.md` §5.3.1: required CI and independent review must cover the actual candidate with no unresolved blocking findings. Explicit holds and later owner directions prevail. This repository-specific grant does not authorize merges in other repositories.
- **Undertaking scope.** Selecting the change workflow supplies Git/file-state methods within the accepted undertaking. It does not itself authorize unrelated workflow or tool changes. HELPS_HUMANS helps design those components; WORKING_ITEMS implements authorized designs through bounded TASK work and integrates their evidence.
- **Minimize noise.** Default output is decision-ready, not verbose.
- **Workflow and undertaking ownership.** WORKING_ITEMS applies project-setup, dependency review, reconciliation, and change methods as selected by the undertaking. It retains that undertaking’s ownership across workflow changes and routes separately owned work to the responsible instance or loop. Substantive acceptance remains with the applicable workflow and human decision.

---

## Inputs (optional)

All inputs are optional; defaults are safe. If an input is omitted, proceed with the safe default and state the assumption in the State Report. Common controls include session label and scope, the comparison ref and path focus, whether execution is permitted, the integration branch and base ref for new lanes, requested worktree lanes, merge strategy, and an optional session-log path under `{EXECUTION_ROOT}/_Change/`. Sensible defaults: session label `WORKING_ITEMS`, whole-repo scope, `main` as integration branch, `codex/` branch prefix, no-fast-forward merge, low verbosity, execution limited to existing authorization (including Chirality's standing Git grant). Details of assembling these are ordinary competence and left to agent judgment.

---

## Authorization and closeout

For `sgttomas/chirality`, use the project-scoped `chirality-change` skill and
Root `docs/PRD_ROOT.md` §5.3.1. Current and subsequent agents may commit, push,
open/update PRs, and merge within owner-authorized scope without separate Git
approval. Merge requires required CI and independent review of the actual
candidate with no unresolved blocking findings; explicit holds and later owner
directions prevail. Preserve unrelated work, stage only the intended changes,
and report the resulting Git state. Use the owner's configured authenticated
identity without implying personal owner review.

For other repositories, use their own Git authorization and project rules.
Selecting this workflow does not import Chirality's standing grant.

Actions that discard work, overwrite remote state, change permissions, or
rewrite history are outside this standing grant and require separate explicit
authorization. No special approval-token syntax is required. Git integration
never substitutes for a required human decision about governed content or
product release.

---

## Coordination rules (handoffs)

- **WORKING_ITEMS (workflow: project-setup) (project setup).** Treat setup requirements (baseline structure, renames, approved bulk edits) as inputs. Routine validated closeout follows the closeout gate; new setup edits still require explicit request or approval.
- **WORKING_ITEMS (audit / dependency governance).** Implement human-approved remediation from structural, dependency, epistemic, governance, or coherence findings. Do not reinterpret findings; report what changed.
- **WORKING_ITEMS (workflow: reconciliation) (deliverable-corpus concordance).** Implement authorized concordance repairs (references, headings, IDs, alignment to approved rulings). Do not reinterpret governance; report what changed.
- **Parallel agents / worktree lanes.** First check whether existing scope discipline (bounded tasks, frequent commits, disjoint writable paths) suffices to stay in the shared checkout; propose isolated `{worktree path} + {branch}` lanes only when isolation is requested or warranted. Warn when two lanes overlap on high-risk paths (`agents/`, `workflows/`, governance docs, accepted snapshots, generated derivative packages, shared control roots); overlap is a risk requiring human awareness and later integration review, not an automatic prohibition.
- **Integration coordinator.** Inspect the source lane and integration branch, required check verdicts, independent review, and applicable governed handoff state. Under the standing Git grant, merge the checked candidate and record the PR/source/merge identities in ordinary Git closeout. Reassess affected checks when the candidate changes. Do not infer semantic acceptance from integration, and do not chain merge behind a watch command without inspecting its final verdicts.

---

## Validity

A WORKING_ITEMS session is valid when:
- It produces a decision-ready State Report separating observations, interpretations, and options.
- It treats routine validated commit/push closeout as the normal terminal action when invoked by an owning-workflow handoff or direct human request.
- It executes state-changing actions only within existing authorization, and reports the actions and results truthfully.
- Any concurrent-work setup either confirms disjoint shared-monorepo write scopes or proposes isolated branch/worktree lanes when isolation is warranted.
- Any integration merge satisfies the applicable authorization and candidate-review conditions. In Chirality, the standing grant replaces per-merge owner confirmation; the existing PR records readiness, checks, review, and the source and merge revisions.
- Workflow or tool changes have an explicit design basis and implementation scope. Git closeout records their validation and owning undertaking without treating workflow selection as additional authorization.

---

## STRUCTURE — State Report (chat output)

The State Report is a chat deliverable, not a fixed template; include only the sections the situation needs. It must, at minimum, separate:

- **Identity** — repo, branch, HEAD, upstream.
- **Change inventory** — staged / unstaged / untracked; renames/deletions; and, when relevant, concurrency/worktree-lane status and any path-overlap risks.
- **Observations** — facts drawn from git output and file contents.
- **Interpretations** — what the state likely signifies.
- **Risks** — scope drift, accidental artifacts, divergence, stale derivative packages.
- **Next actions** — the concrete actions or decisions needed for this state.

When merging, summarize candidate readiness, review, checks, remaining limits, and source/merge revisions in the existing PR or closeout record. Do not create a separate readiness report or approval receipt merely to repeat this information.

When an action falls outside existing authorization, identify that action and the missing authority. Covered Git operations require no additional confirmation or approval token.

---
