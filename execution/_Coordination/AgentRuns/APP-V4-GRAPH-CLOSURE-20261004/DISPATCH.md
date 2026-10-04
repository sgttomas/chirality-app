# Dispatch log — APP-V4-GRAPH-CLOSURE-20261004

Executors are `type2-opus-high` (Claude Opus 5.5, high effort). Briefs are
recorded verbatim in the session transcript and extracted at commit
points.

| Who | Event |
|---|---|
| G1 | Dispatched: objective and SCC-edge survey (read-only; writes SURVEY/G1.md) |
| G2 | Dispatched: register-versus-design currency survey (read-only; writes SURVEY/G2.md) |
| G2 | Returned. 211/212 arcs matched. 30 missing (27 new + 3 bundle seams); 1 contradiction (V25 m-1); 0 unsupported; 13 ambiguous. Five missing relationships would form or grow an SCC: N08 (merges SCC-001/002/003 into 19 members), N13 (new {09-07, 09-11}), N22, N26, N27. Further SCC-forming ambiguous items: A1–A3, A7, A9. HELP_HUMAN spot-checked N08 (ACCESS L63) and N27 (ADAPTER L1446, "by join; no register row") at source. 33 registers need UPDATE (~31 consumer + 39 mirror rows). The SCC-forming items go to G1 for classification by kind before any extraction |
| G1 | Returned. 83 held rows; exact minimum cycle-closing sets: SCC-001 1, SCC-002 21 (21 reciprocal pairs, 11 of them I–I), SCC-003 1, SCC-004 2, SCC-005 1, SCC-006 1. Options O-1…O-6: narrowing by kind dissolves up to four SCCs (by owner cut rulings per row), but never SCC-002's 11 I–I pairs, which need invert, decompose or merge under every option. G2's SCC-forming rows: none is a production input by its own sentence. No option marked recommended. Rules K-1…K-7 and ten shared cases proposed |
| HELP_HUMAN | Next: (a) a standing graph reviewer, RVG (fresh), checks G1's kinds, rules and computations. A fresh reviewer because this is a new subject (graph analysis) and RV3's context is pass-4 design. (b) Early path C2 analyses SCC-002's 11 I–I pairs, which persist under every option, for invert or decompose (agent-proposable moves). Run in parallel |
| RVG | Reviewed G1/G2 (fresh reviewer). G1 REPAIR: the computations reproduce exactly, but M1 K-3 misclasses definition inputs as runtime E (RS schema refs show I); M2 DEP-07-02-010 L inconsistent with -011; M3 options applied only to held rows, not as objectives over all edges, and cut counts omitted; M4 "reopens CP1" framing one-sided. Corrected: kind choice settles 4 SCCs not 5; O-4 13–15 rows; SCC-002 core up to 12 members, 12–13 I–I pairs (P9, P12). G2 READY (1 MINOR). G1 repair to its author; C2 told to take in P9/P12 |
