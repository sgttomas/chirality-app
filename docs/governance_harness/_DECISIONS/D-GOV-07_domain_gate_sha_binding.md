# D-GOV-07 — Domain gate acceptance binding convention

Status:       RULED
HumanRuling:  Approved as recommended by owner (Ryan Tufts), 2026-07-01
Ruling SHA:   82a35c545282889841ce789c3e24f2ca68991ba1 (publication commit, 2026-07-01)
Date:         2026-07-01
FramedBy:     governance_harness_plan_v3 (2026-07-01, merged)

## Decision to make

Verified v2.1 finding: domain gate acceptance binds by content SHA-256 only,
not a git commit SHA — a K-AUTH-2 gap. What is the binding convention?

## Recommendation

Domain gate acceptances bind to **both**: the content SHA-256 (what was
accepted) and a git commit SHA (when/where it entered the governed record).
Existing acceptances are grandfathered with a WARN finding until re-bound.
This is a prerequisite for the deferred domain-shape verifier (D-GOV-03), not
for the project-shape MVP.

Coverage note (2026-07-01 live-repo verification): the SHA-256-only binding
is fully materialized only in the chirality domain (`GATE6_ACCEPTANCE.md`
"Key Artifact Hashes" table plus `Gate6_Publication_Manifest.csv` with an
SHA256 column, no commit SHA anywhere); other domains express gate acceptance
via lighter `gate_snapshots/_LATEST_GATE6.md` pointer files without a
manifest. The re-binding convention must therefore cover **both** forms —
manifest-based and pointer-based acceptances.
