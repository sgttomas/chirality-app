# D-GOV-03 — MVP pilot scope

Status:       RULED
HumanRuling:  Approved as recommended by owner (Ryan Tufts), 2026-07-01
Ruling SHA:   82a35c545282889841ce789c3e24f2ca68991ba1 (publication commit, 2026-07-01)
Date:         2026-07-01
FramedBy:     governance_harness_plan_v3 (2026-07-01, merged)

## Decision to make

Which roots does the MVP harness read, and which are deferred.

## Recommendation

In scope (read + report only): `projects/chirality-app-dev`,
`projects/chirality-piping`, and the `_DomainEngines/` control area
(status + self-check only).

Deferred: `domains/*` roots (different shape; no `_STATUS.md`; needs its own
verify variant — see the deferred-findings register), and any write-path
feature beyond the `write_status.sh` precondition guard.

## Scope addenda (2026-07-01 live-repo verification)

- `projects/chirality-governance/` is out of scope **by construction**, not by
  omission: it is untracked and carries zero `DEL-*` and zero `_STATUS.md`
  (only PM source templates and a tier-0 handoff note) — there is no status
  corpus to read.
- Harness walks MUST exclude `.archive/` trees explicitly: app-dev's
  `.archive/` holds a full duplicate DEL tree (raw find counts 141 vs 53
  live), so an unfiltered walk double-counts and could lint archived copies.
- The pilot roots have divergent `_STATUS.md` schemas (app-dev frontmatter is
  approval-SHA-bearing; piping is minimal, without approval-SHA fields), so
  guard preconditions and parsers are adapter-declared per root; the piping
  approval-SHA schema alignment is a parked item.
- Adapter manifests must disambiguate `Dependencies.csv` vs
  `_DEPENDENCIES.md`, which coexist as distinct files per deliverable.
