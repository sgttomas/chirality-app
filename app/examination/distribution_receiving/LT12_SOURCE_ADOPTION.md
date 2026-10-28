# B-S4-LT12 source adoption — existing two-cohort contracts

Exact selected source: `938d20ef4bf0d07a7cc706d575e74f844d8caccf`.
The separately fixed active names are B-S4-LT12-SOURCE-LT09-v1 and
B-S4-LT12-SOURCE-TERMINAL-v1. Their pin files are pins.lt12-source-lt09-v1.json
and pins.lt12-source-terminal-v1.json. The LT09 selector is frozen first, then
the terminal helper hash and pins bind final receive.py. There is no dynamic
fallback, caller method choice or mutation of historical pin files.

## Actual source and receipt delta

Compared with source9af, the full reader receipt changes only storeReaderSha256:
`e89b7a56022fc2c5d0860788fa423a94d8072ca0ed184304183e5923ddbe8c57`
→ `51195cd106e75c81992e3508a1b435ea64d58b58fefc8d3f9f682baa52b9d0be`.
The producer unsupportedEnvelopes text now describes eligible same-H5 LT12/LT23.
The semantic revision, schema, namespace authority and all other reader receipt
identities are unchanged. Separate selected-source hashes bind the changed Host
integration sources; the author run records exact old/new source maps.

The producer's new capability does not change either receiving contract:
standalone remains group-b-s1-reader-exchange.v1 / actual LT09; terminal remains
group-b-s1-terminal-reader-exchange.v1 / actual LT09→LT23. Neither accepts LT12.
Only selectors, literal digests and named adoption identity change in maintained
receivers. Existing shape/file checks and canonical six-record engine remain
unchanged. Fully rehashed LT12 substitutions refuse on both receiving routes,
including both roles of the terminal pair. Old producer source and mixed store
reader identities also refuse.

## Evidence and limits

Fresh actual committed-source/recompiled synthetic exports are retained in
new group_b_lt12_source_lt09_fixtures and group_b_lt12_source_terminal_fixtures.
All prior pins/cohorts/evidence remain byte-exact history. Each provenance records
source, executable, command/features, exchange hashes and the independently
reviewed receipt identity. B checks raw copies and executable passively; no B
native/supplier action, Rust/App build or download is needed.

These cohorts export no LT12 event. They establish only their existing bounded
LT09 or LT09/LT23 file correspondence on the new source. They do not test or
prove LT12 EOF scheduling, terminal integrity, current native/namespace custody,
actual App/build, authenticated producer history, semantic reexecution, S3,
SEAL-2, M1/native qualification, package witness, canonical rollout or release.
All existing authority/qualification flags stay false. The invented canonical
candidate remains separate from the actual test harness. No SQ package gate.
