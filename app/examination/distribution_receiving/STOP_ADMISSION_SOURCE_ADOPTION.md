# Existing S4 Stop-admission-source renewal

Fixed source127d48f61d91b70d00d0670d2150c79b8ac26d1f is selected by
B-S4-STOP-ADMISSION-LT09-v1 and B-S4-STOP-ADMISSION-TERMINAL-v1, with new
pins.stop-admission-lt09-v1.json and pins.stop-admission-terminal-v1.json.
Standalone selector first, then terminal helper digest/source pins bind final
receive.py. All historical pins/cohorts/evidence remain unchanged. No fallback
or caller-selected source is introduced.

The full reader receipt and exported boundary remain identical to source2377.
Only hosting.rs and hosting_successor.rs change among the prior Host source pins;
terminal additionally binds the renewed standalone selector. The Host's private
start-admission repair prevents a cancelled attempt from later installing a child
or settling state. The maintained STOP_ADMISSION.md bounds its behavior: no
LT20 terminal artifact is produced, and historical generation/PID metadata is
not new custody. Those Host semantics are separately reviewed evidence; this
source adoption does not implement or qualify Stop behavior.

Receiver formats, algorithms, canonical six-record checks and row restrictions
are unchanged. Standalone accepts actual LT09; terminal accepts LT09→LT23.
New tests refuse fully rehashed LT20 substitution on both routes and both
terminal roles, and retain LT12 refusals, stale-source/mixed-reader and all prior
byte/closure/generation/event/path/marker/authority checks.

Fresh actual committed-source/recompiled synthetic exports live in
new group_b_stop_admission_lt09_fixtures and group_b_stop_admission_terminal_fixtures.
Provenance binds exact source/executable/command/features/exchange/receipt hashes.
B passively checks raw copies, actual executable, receipts and source members;
Host owns compilation/export history. The invented App candidate remains
separate from actual harness identity. No LT20 or LT12 exchange is received.

Source renewal establishes only existing bounded file correspondence. It does
not prove whole Stop conformance, cancelled probe termination, descendants absent,
current custody, native/namespace capability, terminal integrity, actual App/build,
authenticated history, semantic reexecution, S3/SEAL-2, M1/native qualification,
package witness, canonical rollout, owner gate or release. Existing authority and
qualification flags stay false. No SQ package gate is added.
