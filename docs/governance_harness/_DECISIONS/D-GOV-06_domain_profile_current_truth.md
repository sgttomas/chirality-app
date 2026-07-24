# D-GOV-06 — Current truth of the open_pipe_stress profile

Status:       RULED
HumanRuling:  Approved as recommended by owner (Ryan Tufts), 2026-07-01
Ruling SHA:   82a35c545282889841ce789c3e24f2ca68991ba1 (publication commit, 2026-07-01)
Date:         2026-07-01
FramedBy:     governance_harness_plan_v3 (2026-07-01, merged)

## Decision to make

The archive's current-state surfaces contradict each other: ADOPTED
(RULINGS_PUBLISHED.md top; INDEX table; YAML `profile_status`; validation
report) versus DRAFT/not-adopted (same file's stale closing paragraph; INDEX
banner; YAML header comment; `.DRAFT` filename). The harness must not silently
normalize this; a human must rule the fact (K-CONFLICT-1).

## Recommendation

Affirm **ADOPTED**, on the basis of the recorded Gate-2 owner ruling of
2026-06-21 (D-T0-06 path: validator built, profile passed, Gate 2 ruled), and
direct a CHANGE-published cleanup of the contradicting surfaces — all six
verified still present at HEAD by the 2026-07-01 live-repo verification pass
(last touched by commit 3ab4c8f22, 2026-06-21):

1. `RULINGS_PUBLISHED.md`: delete the stale closing paragraph ("Profile
   remains DRAFT... and not ADOPTED").
2. `DOMAIN_ENGINE_INDEX.md` banner — **both** halves: "No profile is ADOPTED"
   and "No decision is ruled" (the `_DECISIONS/_REGISTER.md` shows all 8
   D-T0-* RULED 2026-06-21).
3. Profile YAML header comments (the lines saying DRAFT / NOT validated / NOT
   adopted / no validator exists) **and** the `open_issues` entry "Profile
   stays DRAFT".
4. The `.DRAFT` filename: rename the file off `.DRAFT`.
5. D-T0-06's HumanRuling line, still ending "Profile stays DRAFT until the
   validator exists" — superseded by its own Progress (2026-06-21) note but
   never marked as such.
6. `_DomainEngines/_LATEST.md`: the line framing the snapshot as "PROPOSAL,
   not yet owner-accepted" while the same file declares tier-0 adoption
   complete.

Note that some of these contradictions are documented-deliberate — the YAML
inline comment says "Filename retains historical .DRAFT; profile_status is
authoritative" — i.e. a half-finished cleanup, which is exactly why a full
CHANGE-published sweep is directed rather than further piecemeal fixes. The
cleanup diff becomes the first fixture the harness's self-check must pass on
live files.
