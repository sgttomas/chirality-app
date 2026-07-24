# D-GOV-02 — Verifier severity taxonomy and override authority

Status:       RULED
HumanRuling:  Approved as recommended by owner (Ryan Tufts), 2026-07-01
Ruling SHA:   82a35c545282889841ce789c3e24f2ca68991ba1 (publication commit, 2026-07-01)
Date:         2026-07-01
FramedBy:     governance_harness_plan_v3 (2026-07-01, merged)

## Decision to make

What finding severities exist, what machine behavior each carries, and who may
override each.

## Recommendation

Adopt five severities with exit-code semantics. The harness **adopts** exit
0/1/2 as its convention, aligned with the newest validator class
(`tools/validation/validate_domain_engine_profile.py`); older tools vary
(`tools/REGISTRY.md` documents plain 0/1 for 18 tools, and some tools use
exit 3), so this ruling sets the convention going forward rather than
inheriting a uniform one. (Wording corrected 2026-07-01 by live-repo
verification; the prior draft claimed a "repo's existing uniform exit 0/1/2
validator convention.")

| Severity | Meaning | Machine behavior | Override |
|---|---|---|---|
| BLOCK | Objective violation **within the tool's declared observation boundary** | exit nonzero | Human only, recorded |
| REVIEW | Material issue requiring human judgment | exit 0 (nonzero in `--strict`) | Human disposition |
| WARN | Non-blocking inconsistency or hygiene issue | exit 0 | None needed |
| INFO | Contextual fact | exit 0 | n/a |
| NOT_APPLICABLE | Check skipped; preconditions absent | exit 0 + reason | n/a |

Caveats to adopt with it:
- "BLOCK" means *mechanically blocked within the declared observation
  boundary*, never *globally proven safe/unsafe*.
- `Ruling SHA: TBD` is **conditional**: REVIEW when the artifact self-declares
  bind-at-publish (the repo's lawful tier-0 flow); BLOCK only when the claim is
  being relied on as bound authority.
- A non-overridable BLOCK on the CHECKING→ISSUED judgment itself would violate
  K-GATE-1; BLOCKs apply to objective preconditions and hygiene only.
