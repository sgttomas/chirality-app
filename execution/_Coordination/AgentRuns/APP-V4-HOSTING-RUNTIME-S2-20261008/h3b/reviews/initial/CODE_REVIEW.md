# H3B-1 independent review — initial frozen candidate

**CHANGES REQUIRED: one confirmed blocking finding.** Exact five initial maintained-file hashes are retained in ORIGINAL_CANDIDATE.json. Source hashes matched before examination. Review is read-only; temporary harness changes only force a valid concurrent schedule and add an independent fixture. Source origins and role/mechanism are in READ_BASIS.json.

## P1 — A completed Stop can be overwritten by a stale start after its final recheck

Location: hosting.rs final prospective/start-attempt recheck (approximately lines 790–800), subsequent state transition/spawn, and attachment_gate acquisition after allocation (approximately line 879). Start releases Inner after checking the attempt and holds only recovery_writer through spawn. Stop uses attachment_gate and Inner, not recovery_writer. Therefore Stop can complete between final validation and the subsequent spawn/publication; the pending starter does not check cancellation again and overwrites the stopped state.

Confirmed using the genuine Host.start and Host.stop paths with an invented supplier double. The temporary copy pauses immediately after the final tuple/token check, before the verification transition. Main test calls Host.stop, observes its successful return and state `stopped`, then resumes start. Start returns `Ok` with state `ready`, generation spawnCounter 1 and an owned child. The test cleans up that unexpected child before failing. A completed user stop must not be followed by an unrequested process start.

Reproduction: `reviewer_stop_after_final_check_prevents_spawn`; log stop-race.log. Exact temporary source delta: STOP_RACE_INSTRUMENTATION.patch. The test-only barrier changes scheduling only; it does not alter production conditions, force state directly, or replace Stop. All actual source files remain unchanged.

Repair direction: serialize Stop with the final attempt/session/counter check through spawn, generation allocation and child-handle publication using a shared custody/attachment guard and consistent lock order. Retain scan/probe outside that guarded section. A stale attempt must refuse without overwriting newer state, and exceptional postspawn failure must kill/reap the locally owned child. Independently backcheck the same schedule against the repaired candidate before fan-in.

## Other observations and review limits

The five-file diff preserves default legacy configuration, adds explicit staged mode selection, retains absent compiled S3 selection and unavailable integrity/custody refusal, and describes the in-memory unverified snapshot separately from pending durable S1 artifacts. Probe output/time limits and process-group cleanup use WNOWAIT to retain the leader identity until kill/reap; the stated hostile-escape limitation remains explicit. Native setup retains P2/P3 role/workflow handlers and the custom-protocol declaration. None of these observations constitutes a final integration verdict while the blocker remains.

No production supplier/App execution, credential use, download, canonical Design/pin/MEMORY write or branch change occurred. Synthetic fixtures only. Shared target released to the author after this reproduction. Whole H3B/S2, durable transport/publication and canonical receiving remain later work.
