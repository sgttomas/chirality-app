# Owner decisions — APP-V4-BASIS-ALIGN-20260928

## Direction to start (owner, exact, 2026-09-28)

> "go ahead with the next undertaking as recommended."

**The recommendation it answers.** This is the recorder's last message of run
APP-V4-SWBPIPE-INTAKE-20260928. The next undertaking should bring the accepted
basis in line with what the owner has decided, before more design work builds
on it. It covers:

- the proposed ScopeOfWork, register and dependency-graph (DAG-002) changes
  from the first closeout (C1-A/B/C, CLOSEOUT_ACCOUNT);
- the accepted-basis wording updates: V4-WF-05 (phased checkpoints), V4-HOST-01
  and V4-ARC-11 (OAuth; no default), and V4-HOST-02 (DECISION-5);
- the SoW wording that assumes a run waits at a checkpoint: EXEC F-29, CA F-22,
  GUIDE G-12 and LOOP G-6.

Earlier recommendations the recorder treats as carried into "as recommended",
**to be confirmed at the checkpoints**, not assumed:

- recording IN_PROGRESS for the 14 first-increment deliverables;
- the ruling on the disputed arc DEL-03-02 → DEL-04-03 (lean: not proposed).

## Governance route

Both routes have owner checkpoints. No governed file changes before the owner
accepts the packet at the checkpoint that governs it.

- **Accepted basis and ScopeOfWork:** `scope-change`, grouped checkpoints 1–3.
  The accepted amendment is applied by `scope-of-work` MODE=REVISE, one
  deliverable per brief.
- **Registers and DAG:** register changes are applied by bounded
  per-deliverable briefs (`dependency-extract` or human declaration, as the
  row requires). A currency audit then records the DEPARTURE, and
  `project-dag` TRIGGER=SUCCESSOR prepares DAG-002 for the owner's acceptance
  at checkpoint 2.

## Checkpoint A: owner answers (exact, 2026-09-28), DECISION-6 (partial)

| Question presented | Owner's answer (exact) |
|---|---|
| Accept the wording package (SCA-V4-001) as prepared? | "I want to review the packet first" |
| Four closeout corrections that widen or sharpen scope: adopt which? | "what do you recommend and why" |
| Record the 14 first-increment deliverables as IN_PROGRESS now? | "Yes, record IN_PROGRESS (Recommended)" |
| Dependency arcs for DAG-002: 41 arcs, keep X-1, disputed arc out? | "Accept the 41; keep X-1 (Recommended)" |

## Effects

- **Scope-change groups 1–2** are not yet accepted. The owner is reviewing the
  packet. No doc, decomposition or SoW edit is applied.
- **Lifecycle:** the owner directs recording INITIALIZED → IN_PROGRESS for
  DEL-04-01, 04-02, 04-03, 03-01, 03-02, 03-03, 03-04, 02-01, 02-03, 05-01,
  05-02, 01-01, 09-06 and 09-09 (SPEC: by the Human or WORKING_ITEMS).
- **Arc set** (for DAG-002 preparation):
  - the refreshed 41 are accepted, with X-1 kept;
  - N-12 and N-B8 are not proposed.

  DAG-002 itself still needs the owner's acceptance at checkpoint C.
