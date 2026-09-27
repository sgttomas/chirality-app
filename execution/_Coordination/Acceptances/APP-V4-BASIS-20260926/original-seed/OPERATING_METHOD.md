# Chirality v4 — Operating method

**Status: DRAFT 1 — candidate, not accepted; pending the owner's
discussion of Q-11 (D-12).** How the v4 product is to be built. It records
the owner's proposal and the conditions HELPS_HUMANS proposed for it
(`conceptual/DISCUSSION_2026-09-25.md` §3), using the drafting defaults in
`conceptual/SEED_SET_PLAN.md` §3 where the owner has not yet answered.
Identifiers `V4-OPS-<nn>`.

The implementation session establishes its own decomposition, setup,
production contracts, dependency mapping and route (OD-13). This document
states the method it works within; it does not do that work.

## 1. The owner's proposal

> "The current development loop matches the decomposition and execution
> folder structures and contents. It uses graph traversal to guide work and
> can allow all manner of parallel and sequential work with teams of agents,
> subagents, or solitary work. So that structure is good and will be
> retained. But to guide the work graphs we have the agents follow the
> Project Management manual according to the Agents User Manual, is my
> proposal." (D-12)

## 2. What is retained

- **V4-OPS-01** The decomposition and execution folder structure: packages
  and deliverables, each with its working, checking and issued records.
- **V4-OPS-02** One project dependency graph (DAG), established before the
  30 % position, and one current work graph per undertaking, kept as a file,
  traversed to select and carry work.
- **V4-OPS-03** The four roles, with teams of agents, subagents, or solitary
  work as each undertaking needs (Field Book §2).
- **V4-OPS-04** The route of positions — Conceptual, FEED, 30 %, 60 %, 90 %,
  100 % — as positions of the work, not percentages of effort (Field Book
  §1). This seed set is the Conceptual output.

## 3. What guides the work

- **V4-OPS-10** Agents follow the *Project Management for Human–Agent Teams*
  method: the **Field Book** as the route they always carry; the
  **Consolidated manual** read by section when a step needs its reasoning (the
  Field Book cites the sections); and the **Chirality Agent User Manual** for
  how the method applies in this repository.
- **V4-OPS-11** **Pinned editions.** The v4 project names the editions it
  follows and adopts a new edition deliberately. Candidate pins, to be fixed
  by the implementation session at its start:

  | Manual | Blob at `2b0572fe0` | Blob at `origin/main` `94e9255b6` |
  |---|---|---|
  | Field Book v1 | `a34df1aff1ad` | `a34df1aff1ad` (unchanged) |
  | Consolidated v7 | `868e67ae95ec` | `868e67ae95ec` (unchanged) |
  | Agent User Manual v3 | `d5c66c463403` | `ade718527747` (changed with workflow repairs) |

- **V4-OPS-12** **Precedence.** Root governance, then the v4 project's own
  instructions, then the accepted v4 basis (this seed set) for *what* is
  built, then the manuals for *how* the work is organised. The manuals do not
  add requirements.
- **V4-OPS-13** **Purposes over mechanisms.** Where a manual names a
  repository mechanism the v4 project does not use, the purpose governs and
  the project records what it does instead.
- **V4-OPS-14** **Adoption.** The manuals state that reading them "does not
  amend those instructions or adopt a new execution basis". Adopting them as
  the v4 method therefore needs the v4 project's own instructions — a thin
  project loop file that points to the Field Book and states V4-OPS-11…13 —
  created by the implementation session as an instruction change with its
  own scope, with the owner's approval **[pending]**.

## 4. Feedback on the method

The owner's aim for the manuals is to "try again, examine through use, and
improve through feedback" (OD-08).

- **V4-OPS-20** When a practice helps, does not fit, or is ambiguous, the agent
  notes it briefly at the work-graph node where it happened, citing the
  manual section.
- **V4-OPS-21** At each stage gate the owner and the agent review those notes
  together. Each becomes a proposed manual revision, a deliberate departure
  for this project, or nothing.
- **V4-OPS-22** **[pending]** Where the manuals are silent — estimation,
  scheduling and risk have no practice in them — agents record what they did
  and bring consequential gaps to the owner.
- **V4-OPS-23** **[pending]** The owner revises the manuals, from changes
  agents propose.

## 5. Proportion

- **V4-OPS-30** Enforcement of boundaries comes from the host's real
  permissions and worktrees; the manuals describe intent, and independent
  review checks it (L-04).
- **V4-OPS-31** Keep records that serve a decision, a reliance claim or
  recovery. Git history and reviewed pull requests are the primary record of
  changes; do not duplicate them in parallel evidence systems (M-8, L-02).
- **V4-OPS-32** Do not create registers without a reader: anything emitted
  must be consumed at a named point, such as a stage gate or a work graph's
  entry step (L-06).
- **V4-OPS-33** Decompose once the basis is stable enough to hold still
  (L-03). This seed set is meant to provide that stability for v4.0.
- **V4-OPS-34** Independent review of identified candidates, with a reviewer
  from a different model family where available (D-13).

## 6. Questions still open with the owner

1. Does following the manuals replace the current loop instruction files for
   v4 entirely, or sit behind a thin project loop file that points to them
   (the draft assumes the thin file)?
2. Where the manuals are silent, should agents improvise and record, or
   bring the gap to the owner (the draft assumes both, by consequence)?
3. Who revises the manuals from the feedback (the draft assumes the owner,
   from agents' proposed changes)?
