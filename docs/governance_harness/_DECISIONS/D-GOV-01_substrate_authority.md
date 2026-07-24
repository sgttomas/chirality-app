# D-GOV-01 — Substrate authority for the governance harness

Status:       RULED
HumanRuling:  Option A approved as recommended by owner (Ryan Tufts), 2026-07-01
Ruling SHA:   82a35c545282889841ce789c3e24f2ca68991ba1 (publication commit, 2026-07-01)
Date:         2026-07-01
FramedBy:     governance_harness_plan_v3 (2026-07-01, merged)

## Decision to make

Which substrate holds operational governance state, and what write posture may
the harness take?

## Options

- **A (recommended):** Git-tracked authored plain files are the sole authority
  for Chirality governance state. The harness never writes governed authority
  files; it may write labeled generated artifacts (reports, briefs, evidence
  records) under declared generated paths. Any database used by Chirality
  governance or harness tooling is a rebuildable, gitignored projection: safe
  to delete, regenerated from files by one command, never cited as authority
  (the shipped `catalog.sqlite` pattern). The only write-path interventions are
  precondition guards that refuse objectively-broken transitions. No
  coordinator process, no leases, no database-owned status, no CLI-owned
  governance writes.
- **B:** SQLite control plane owning leases, runs, gates, queues, and derived
  status, with the CLI as the supported write surface (per the 2026-06-23
  integration assessment / Option C of the 2026-06-22 transcript).

## Scope note

This ruling governs **Chirality governance state and harness projections
only**. Engine-owned domain truth (e.g. the OpenPipeStress SQLite-backed
persistence store for model states and analysis runs) is sanctioned
authoritative domain truth under CONTRACT §1.12 K-DOMAIN-1 and the ADOPTED
`open_pipe_stress` profile; it is governed by the K-DOMAIN family, not by this
record.

## Recommendation

Option A. Basis: DIRECTIVE.md §2.1 + §5 structural constraints; K-AUTH-1,
K-STATUS-1; the `catalog.sqlite` precedent; the v2.1 plan §03 verdict, held
twice under adversarial review. The fork has flipped three times across plan
generations (transcript → v2.1 → assessment → bench plans) because no ruled
record existed.

## Supersedes

- Option C recommendation, `plans/.archive/task-management-planning-26-06-22.md` §14
- Control-plane architecture, `plans/.archive/governance_harness_integration_assessment_2026-06-23.md`

Paths corrected 2026-07-01 by live-repo verification; both live under
`plans/.archive/` (gitignored archive; outside version control).

## Consequence

Re-opening this fork requires superseding this record. Any future proposal for
database-owned governance state must cite and argue against this ruling.
