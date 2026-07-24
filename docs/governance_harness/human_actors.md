# human_actors — Owner-Curated Identity Allowlist

Status: ACTIVE. Identity source for `RuledBy`/`AdoptedBy`/`HumanRuling`
attribution matching, per D-GOV-04 (ruled by owner 2026-07-01; ruling SHA
82a35c545282889841ce789c3e24f2ca68991ba1; record:
`_DECISIONS/D-GOV-04_human_actor_identity.md`).

Behavior: identity-dependent harness checks REFUSE (exit 2) when this file
is absent or an attributed actor does not match an entry below — refuse
rather than guess (D-GOV-04: misclassifying a human as an agent would
false-block).

Maintenance: owner-curated. Additions and removals are owner edits,
published by CHANGE. Do not extend this list programmatically.

## Actors

| Canonical name | Role | Matchable aliases | Git identity | Email | Effective |
|---|---|---|---|---|---|
| Ryan Tufts | Owner / sole maintainer; sole author of binding rulings (K-AUTH-1) | `owner`, `Owner`, `Ryan Tufts (owner)` | `Ryan Tufts <ryan@Mac.lan>` | ryan@chirality.ai | 2026-07-01 |
