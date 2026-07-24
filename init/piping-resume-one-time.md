Resolve `REPO_ROOT` with `git rev-parse --show-toplevel`. You need to be working in the dedicated
worktree for the chirality-piping D-41 concordance run. Before doing substantial
work:

1. Find the worktree for the chirality-piping D-41 concordance run. As of
   2026-07-12 it is `{REPO_ROOT}/.claude/worktrees/chirality-piping-d41-concordance-9811cb`
   on branch `claude/chirality-piping-d41-concordance-9811cb` (verify with
   `git worktree list`; if your harness cannot use it, create a fresh worktree
   from that branch — never work on the primary checkout). The read-only
   frozen evidence worktree is `{REPO_ROOT}/.claude-worktrees/piping-frozen-551f84ef6`.
2. Write only inside `projects/chirality-piping/` in this worktree. Never touch
   chirality-app-dev, the primary checkout, or another active worktree.

Set `WORKING_ROOT={REPO_ROOT}/projects/chirality-piping` and enter through:

`init/init-prompt.md` → `loop/LOOP_INIT.md` → newest `loop/WORKPLAN_*.md` →
`loop/LOOP_RECEIPTS.md`

Resume:
`projects/chirality-piping/execution/_Reconciliation/DeliverableConcordance/
DELIVERABLE_CONCORDANCE_2026-07-11_1305`

Enter through the project’s current loop instructions. Then read, in authority
order:

- latest 3 loop Receipts (25–27);
- the run folder’s `RUN_BASIS.md` end-to-end (including the W4-complete,
  addendum-9 incident, and current pause/concurrency entries);
- `R1_CONVENTIONS.md` Parts A–D;
- the W1–W4 calibration carry-forward in `PACKAGE_SUMMARIES/PKG-00..12.md`
  (each summary’s "Cross-ledger risks carried forward" section is binding
  calibration for W5);
- R0/R0b review files for calibration context;
- the pinned plan §§6–8 at
  `551f84ef6be656f1603ce0acfa5e3935aa9683c7`.

<last-work>
PAUSED at owner direction after W4 (Receipt 26). Waves W1–W4 are complete: 75
of 101 ledgers; W4 added 20 corrected ledgers / 491 rows across PKG-09..12,
four package fan-ins, package summaries PKG-09..12, full-wave revalidation,
and durable closeout. PR #207 was merged to main by owner direction as
`b3db98c7b75347e79db0727bed7b92ae874960ab`. W5 has not been dispatched and
no W5 artifacts or agents are in flight.

Owner acts pending before/at resume:
1. **Frozen-tree restoration (addendum-9 incident):** six untracked
   git-ignored artifact sets sit in the frozen evidence worktree
   (`.claude-worktrees/piping-frozen-551f84ef6`) — enumerated in RUN_BASIS.
   Restore via scoped `git clean -fdX` there (or recreate from the pinned
   SHA), or direct the orchestrator to treat them as allow-listed
   contamination.
2. **Two items listed in Receipt 25 for owner ruling (not repaired):**
   (a) RUN_BASIS's W3 pause entry names the rescinded Receipt-17 steer in
   its forward-looking resume lines — superseded by LOOP_INIT §7, left
   frozen as a run record; (b) a factual defect in the W3 package
   summaries: `PACKAGE_SUMMARIES/PKG-06/07/08.md` say "All pilots fable
   per the Receipt-17 steer," but W3 discovery pilots were opus (fan-in
   statements are correct). Do not treat that sentence as fact, and do not
   repair it without owner direction; the calibration content of those
   summaries is unaffected and remains binding.

Next work on resume: dispatch R2 W5 (PKG-13..17, 26 deliverables) under the
owner's 2026-07-12 concurrency direction (Receipt 27): **for each package,
dispatch one deliverable-grained pilot per deliverable and run every pilot in
that package concurrently**. The former ≤4-concurrency cap is superseded for
all remaining waves. Keep packages as the fan-in/checkpoint units; do not
combine multiple deliverables into one pilot. Model assignment remains
MODEL-AGNOSTIC per LOOP_INIT §7: the owner names model(s) at session or
dispatch time; absent that, use the capability-tier fallback and record the
model used for every role. W5 briefs must carry R1_CONVENTIONS + the binding
W1–W4 calibration items from PKG-00..12 summaries + addendum-9 mitigation
(porcelain `--ignored=matching`; six known paths allow-listed until restored;
lockless cargo only via copy-out; `pytest -p no:cacheprovider`; no in-tree
`py_compile`). After package-concurrent discovery, run the high-effort fan-in
(one verifier per package; all self-flagged rows, all non-ALIGNED rows, ≥2
ALIGNED rows per ledger), owning-pilot corrections, full-wave revalidation,
package summaries, RUN_BASIS entry, receipt/model attribution, and
wave-boundary commit/push/PR. Then complete R3 synthesis and R6 backcheck per
the durable method, write RUN_SUMMARY.md, and STOP.

Durable working artifacts from prior sessions are sufficient; scratchpad
copies may be absent. Reconstruct W5 briefs from R1_CONVENTIONS,
R0B_CONVENTIONS, PKG-00..12 summaries, and W2–W4 verification reports. The
structural validator is re-derivable: 20-column header byte-exact to any
committed ledger; enums from R0B conventions + addenda; ClaimID
`DEL-XX-XX-<REQ|ACC|EXC|DECL|REM>-NNN` contiguous per token and matching
ClaimType; RFC-4180 CRLF; addendum-6 DECL rows NOT_APPLICABLE; histograms in
notes must recount from the CSV.
</last-work>

Run-local conventions override generic defaults where they say so. Live Git and
durable run records override this prompt if they reveal a contradiction; STOP
and report any material contradiction rather than guessing.

After W5, complete R3 and R6 per the durable method, write `RUN_SUMMARY.md`, and
STOP. No lifecycle transitions or R4/R5 repair work without my explicit ruling.
All claim dispositions are agent judgments, never human rulings.
