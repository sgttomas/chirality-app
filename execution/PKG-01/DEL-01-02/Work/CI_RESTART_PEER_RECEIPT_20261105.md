# Restart test: observe the peer receipt before comparing the wire

PR #130 head `99d56890` failed its shard B Stop/Restart cohort in
`real_host_restart_starts_a_new_process_and_continues_no_conversation`.
The peer log contained the expected sequence except for the final
`initialized` notification. The Host had completed its local write and become
ready; that does not establish when the fixture has read and logged the frame.

The test now waits, within three seconds, for the peer to observe the second
`initialized`, then retains the exact full-sequence equality assertion. Its
new-generation and zero-loaded-conversation assertions remain. A missing
handshake still fails, as does an extra resume or other logged request.
Only the test changes; Host/Stop/Restart behavior and requirement maturity do
not change.

Verification used the existing Python peer, offline locked Cargo, fresh
scratch homes and ordinary slot/memory guards. A temporary 150 ms peer delay
reproduced the original CI mismatch; the repaired test passed under that same
delay. The delay was removed before the final run. The full `codex_stop::tests`
cohort then passed 37/37 in 13.55 seconds. No stock supplier, model or native
App was run, and this establishes no native qualification.

Private evidence under `chirality-t3`: the failed job log is in
`scratch/app-pr130-ci-failure-2dkeb_gs/`; the controlled before/after logs,
final `cohort.log` and invocation are in
`scratch/app-pr130-restart-sync-vbbn13p5/`.
