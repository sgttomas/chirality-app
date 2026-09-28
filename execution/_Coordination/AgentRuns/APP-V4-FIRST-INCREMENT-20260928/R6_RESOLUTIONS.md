# R6 micro-rulings — V4 residuals (final pre-merge pass)

Integrator: HELP_HUMAN. Inputs: [V4-A](reviews/V4-A.md) and
[V4-B](reviews/V4-B.md). Both returned **MERGE AS DRAFTS**, 0 BLOCKING, with
5 MAJOR and 23 MINOR items between them.

These rulings are applied **in place**, with no version bump. Each file records
them in its latest "Changes from …" table under an R6 ID. R1–R5 stand except
where amended here.

## R6-1 Hold-support classification by held actions (V4-A MAJOR-1/2; amends R5-1 HS-3/HS-5)

The EXEC §3.6 assignment is decided by **what the checkpoint must hold**, not by
how it arrives:

- **Host-held class (HS-3).** Every action the checkpoint must hold is a **host
  operation** on the external channel, such as the governed operation, or the
  host operations after arrival until the act. The value follows the SQ-02
  status:
  - answered, with host-held carriage evidenced on a candidate → *enforced on
    the host route*;
  - unanswered → *not established*;
  - answered with no host-held route → *not enforceable*.
- **App-side class (HS-5).** At least one held action is App-side: an App agent
  turn, an App tool or harness action, or an App file write or return step. In
  App runs the value is *not enforceable* (D6), whatever SQ-02 returns.
- **Host loop (HS-2)** and **invalid declarations (HS-1)** are unchanged.
  - Invalid declarations take **no value**, and the check is *not
    established*. This confirms EXEC F-22; LOOP aligns.
- **Workflow precedence** (EXEC §3.5) is unchanged.

Recompute the affected cases by their actual held actions:

- E1 `CP-check` (holds Return, App-side) → *not enforceable*; E1 via X →
  *unsupported*. No change.
- E1c/E1d `CP-check`: classify per its declared held actions, and state the
  result.
- E1d via X: include E1c's `CP-check`, then apply precedence. EXEC MT-16,
  WD-EX E8 and WD VC-37 follow.
- AS F6c, RS E10 `CP-row-check`, ACT `CP-L4`: classify by held actions.

Owner files: EXEC first. CA §2.2/WR-11, RELAY SQ-02, GUIDE §2.14, WD §4.3.8 /
WD-EX E8, AS, RS and ACT then follow. WR-11's advice becomes: keep a
checkpoint's held actions on host operations if it must be enforceable from the
App.

## R6-2 Value corrections

- **C V-GR1 and its change row:** `CP-grant` via X is *not established*, because
  it is HS-3 on OP-C9 while SQ-02 is unanswered (V4-A MAJOR-3, V4-B MAJOR-1).
- **AS F18/VC-03:** E1 on X is **unsupported** (V4-A MAJOR-4).
- **WD-EX R-16(iv):** after a refused A12 in V-GR1, **⟨set-1⟩** stays in force.

## R6-3 What "held" means per value (V4-A minor)

| Value | What happens at the hold |
|---|---|
| *enforced by the host loop* | The run stops at its next action. |
| *enforced on the host route* | The host refuses the held host operations. Any other action is recorded as *action during hold*. |
| *not established* / *not enforceable* | Nothing is stopped. Actions are recorded as *action during hold*. |

Fix RS L-12, AS §4 and WD I-9.

## R6-4 Labels and stale markers

- LOOP renames its HS-0…HS-4 labels to **LH-0…LH-4**, and closes G-5.
- Remove "pending", "not yet in C" and "C-v0.5 to add" markers where the
  element exists at the candidate.
- ACT FX-44: fix the cite to **WD VC-41**.
- EXEC L-EXEC-13/14: re-point their reasons to GR-P/GR-R/GR-S.
- CA W14-03: add MT-2 and MT-16.
- HOSTING: close U-25 and F-22, since EXEC settles them.
- C FXA-5: mention `CP-check` as well as `CP-accept`.
- ADAPTER GC-5: state the "other than an A5 constraint" exception per R6-1.

## R6-5 Relay and index hygiene (before the owner relays)

- **D5 attribution:** CA DI-5, the RELAY Basis line and XT IN-14 credit only
  "flow, no gate" as SETTLED. "Record and show" is labelled INTEGRATION.
- **Model-supplied → not enforceable:** CA, XT and RELAY state this only for
  the case where SQ-02 has been answered with no host-held route.
- **RELAY ledger:** correct the version history in the "Prepared" row.
- **GUIDE:** update the pinned hashes to the final bytes; refresh the CC-11
  conflict list and F-11.
- **RS R11 action during hold:** carry the **turn initiator**
  (person-directed / agent / App rule) (EXEC F-24).
