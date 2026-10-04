# Dispatch log — APP-V4-GRAPH-CLOSURE-20261004

Executors are `type2-opus-high` (Claude Opus 5.5, high effort). Briefs are
recorded verbatim in the session transcript and extracted at commit
points.

| Who | Event |
|---|---|
| G1 | Dispatched: objective and SCC-edge survey (read-only; writes SURVEY/G1.md) |
| G2 | Dispatched: register-versus-design currency survey (read-only; writes SURVEY/G2.md) |
| G2 | Returned. 211/212 arcs matched. 30 missing (27 new + 3 bundle seams); 1 contradiction (V25 m-1); 0 unsupported; 13 ambiguous. Five missing relationships would form or grow an SCC: N08 (merges SCC-001/002/003 into 19 members), N13 (new {09-07, 09-11}), N22, N26, N27. Further SCC-forming ambiguous items: A1–A3, A7, A9. HELP_HUMAN spot-checked N08 (ACCESS L63) and N27 (ADAPTER L1446, "by join; no register row") at source. 33 registers need UPDATE (~31 consumer + 39 mirror rows). The SCC-forming items go to G1 for classification by kind before any extraction |
