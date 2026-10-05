# V0-ROLE-SUPPLIER-PROBE-R1 — source-only repair backcheck

2026-10-05. **NOT READY: constructor-failure cleanup remains unhandled.** Original empty-base and normal/exited-leader cleanup defects are repaired at reviewed R1 script `98eca0a3055cf9791b38a26a47dd259f4d728d3d3d16b7e69a926a1f820719d8`, README `5a4a61d73903dd8e13e95451713761b6f7bedc136eb1974fc342927c78d5f9cb`. Original b19 findings remain in V0-ROLE-SUPPLIER-PROBE.md. This is not native execution or supplier qualification.

Independent same TASK `/root/group_a_execution/contract_reviewer`, parent WORKING_ITEMS `/root/group_a_execution`, supplied Codex gpt-6.1-sol/medium, no substitution/diversity or descendants. Applied already-loaded software-code-review. Only syntax/pure helper/fake-process/RPC checks performed; no native subprocess, provider/HTTP endpoint, mktemp, OS signal, auth/network, Cargo, Git or product/Design execution/change. Only this review written.

## Supported repairs

RP-1: presence now requires nonempty base bytes while preservation compares the full ordered unnormalized byte sequences. Independent empty instructions and empty system-segment cases both yield unknown/fail; equal nonempty CRLF base passes and changing CRLF to LF fails. Composition remains exactly4856 bytes/ad560fe79f9552fef1042dd613a0274ca87babd7165bc1ecd0a278a3ada98343 with original source/part identities.

RP-2 ordinary close paths: PGID is checked independently of leader state, bounded TERM then KILL and absence observation precede successful cleanup report. Persistent group visibility yields unknown/failure, not leader-based success. The five injected fake-process cases pass. Native cleanup reality still belongs to later parent execution; fake signals/clock prove branches only.

Root corrections are present: explicit gpt-6.1-sol in configuration/thread request and medium in configuration/turn request, with requested and reported values distinguished. Independent fake-RPC call captures those exact request parameters without executing a supplier. Actual /usr/bin/mktemp -d for owned root and home is specified with strict owned-parent check/mode0700. This method was source-inspected, not executed. Loopback capture-only/no forwarding, cleared key/token environment, exact pinned oracle and local raw/report custody remain unchanged.

## Remaining blocking RP-2 initialization branch [P2]

Location: NativeRpc.__init__, after subprocess.Popen and before reader.start; main assignment `rpc = NativeRpc(...)`.

Trigger: Popen succeeds, then reader construction/start fails (for example thread resource exhaustion). The constructor has no guarded cleanup for the already-created process/stderr handle. Because constructor return failed, main's rpc remains None and its finally block cannot call close(). The original RP-2 remediation explicitly included owning initialization failures after spawning; repairing only close() does not address that branch.

Pure reproduction patches Popen to a fake process, Thread.start to raise RuntimeError, Path.open/chmod to fakes, and killpg to a mock. Observed injected reader startup failure; fake process cleanup calls=[], group signal calls=[], stderr.close=False. No actual process, file, signal or endpoint operated.

Repair: establish cleanup ownership as soon as Popen succeeds; guard subsequent reader setup and failure with bounded group termination/absence, owned leader reap and stderr closure. Guard Popen failure for its already-open stderr as well. Reuse the bounded cleanup semantics; do not weaken pass status or assume constructor exceptions imply no child. Add this fake constructor case to self-check and re-freeze for focused backcheck. No new owner checkpoint or live qualification is necessary to repair this source path.

## Commands/results

`python3 -B probes/ROLE_SUPPLIER_PROBE.py --self-check`: exit0, five fake group cases plus empty-base/CRLF/model-effort checks pass; no native/provider/mktemp/signals.

AST parse: pass. Independent exact-composition/empty-instructions/empty-system/nonempty-CRLF tests: pass. Fake capture_case RPC parameter check: pass. Constructor failure mock: cleanup omission reproduced as described. These observations are associated with the frozen R1 hashes above, even if a later repair advances the file.

Parent was notified before execution; no source readiness should be inferred until this remaining branch is repaired/backchecked. All unrelated earlier source warrants and no-adoption/lifetime/child/model/qualification limits remain intact.
