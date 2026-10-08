# H3B-1 R1 — Stop/start custody serialization

The independent reviewer reproduced a P1 defect on CANDIDATE.initial.json: genuine Host.stop completed while start was paused after its final H5/token check, then resumed start spawned a child and reported ready. The reviewer supplied a test-only scheduling barrier; no supplier/native App act occurred. Author independently reran the unchanged reviewer harness and reproduced failure (checks/r1-author-original-repro.log, exit 101). The original instrumentation is retained verbatim at checks/r1-original-instrumentation.patch. Manager retains the independent review packet separately.

## Cause and bounded repair

High-confidence cause: final tuple/attempt check held Inner only temporarily, and source attachment_gate was acquired after actual spawn/allocation. Stop does not own recovery_writer, so it could complete in that gap. A later start step then published child custody without another serialized Stop-state check. This was a real connecting-path defect, not a test-only synthetic trust issue.

Successor start now acquires recovery_writer, then the SAME attachment_gate used by Stop, then Inner for the final check; it retains the source gate through actual spawn/allocation and pipe/generation publication. Both writer and source-gate acquisitions after the final scan are nonblocking. Probe/scans remain outside both gates. Stop either wins before this boundary and no child/counter is created, or waits and observes the fully published child. Generation is captured before releasing custody so reader setup cannot borrow a later generation. Existing legacy post-spawn gate/allocation behavior remains unchanged.

The connected late-Stop ordering also requires successor handshake settlement to stay scoped. Successor initialize and initialized writes bind captured H5; readiness and failure require the captured attempt, same H5, handshaking state and open source under attachment_gate. An old response/error never promotes stopped state or kills a newer source. Legacy handshake behavior remains on its prior branch. This is part of the same Stop/start repair, not H3B-2 artifact work.

## Regression boundary

Four maintained per-instance scheduling regressions cover: real Stop winning before final gate (no spawn/counter); real Stop waiting after final check then ending the published child; late response and old error refusing stopped/newer sources; busy source gate refusing without waiting after audit. The original barrier position is preserved as after_successor_check, but Stop runs on another test thread because the repaired behavior intentionally blocks it until custody is published. A second hook pauses handshake after publication to observe completed Stop before start resumes.

An initial new test incorrectly expected an empty Child handle after the ordering that legitimately spawns and then stops. on_eof intentionally retains the reaped Child handle. The corrected check proves exited status and zero recorded surviving descendants, plus stopped state, no LT-09, and no late mutation. The initial assertion failure is retained in checks/r1-test-expectation.log; production was not changed to satisfy that test expectation.

The initial candidate and original check logs remain preserved. Current CANDIDATE.json binds the repaired source; R1 check logs report final default/production/legacy results. Scanner/reference resolver source was not changed by R1. No commit, source-pin/Design change, artifact publication, native supplier execution, download, credential use, qualification or release is included. Independent repaired-candidate backcheck and final integration remain pending.

The scoped successor branch also retains actual handshakeReportedIdentity and handshakeConsistency under the same checked gate, including a contradictory version before refusal. A fifth regression checks that diagnostic preservation and absence of ready. No old response can write those fields after Stop or generation replacement.
