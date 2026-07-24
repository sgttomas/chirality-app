# D-GOV-05 — Minimal governance basis ratification

Status:       RULED
HumanRuling:  Option A approved as recommended by owner (Ryan Tufts), 2026-07-01
Ruling SHA:   82a35c545282889841ce789c3e24f2ca68991ba1 (publication commit, 2026-07-01)
Date:         2026-07-01
FramedBy:     governance_harness_plan_v3 (2026-07-01, merged)

## Decision to make

Root `docs/{DIRECTIVE,CONTRACT,SPEC,TYPES,PLAN}.md` are DRAFT pending
ratification, yet the harness will check invariants they define. Ratify what,
when?

## Options

- **A (recommended):** Ratify a minimal harness basis now: source-of-truth
  rule, human-authority rule (K-AUTH-1/2), generated-output rule, path
  containment (K-WRITE-2), provenance requirement (K-PROV-1), status canonicity
  (K-STATUS-1), and the D-GOV-02 severities. Full root ratification proceeds on
  its own track. The append-only History trailer grammar (one normalized line
  per transition; prose otherwise free) rides this ruling or a later narrow
  SPEC §3.1 amendment — parser caveat classes serve until then.
- **B:** Full root governance ratification before any enforcement claims.
- **C:** No ratification; harness stays advisory indefinitely with every report
  labeling each checked invariant's DRAFT status.

## Interim rule (until ruled)

All harness findings are advisory except purely local technical checks (path
containment, source-file existence, generated-output labeling), and every
report labels the ratification status of each invariant it checks (K-CLAIM-1).
