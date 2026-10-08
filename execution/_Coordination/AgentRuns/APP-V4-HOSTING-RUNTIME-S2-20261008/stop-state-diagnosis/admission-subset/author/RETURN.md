# STOP-ADMISSION-01 frozen author candidate

Exact base cd79d9b477f7f33aa4d7a3683e26e6337039d412; existing `/Users/ryan/.codex/worktrees/hosting-lt23/chirality`, branch `codex/hosting-stop-admission`. Four staged files, no unstaged delta, no commit. CANDIDATE_FILES.json identifies every source hash; candidate.patch is the exact staged diff. Released design SHA5754f9841156b3778d15c50c2ce542b0d8680e71289ecdf589ce8149c68f3933. Parent retains release/independent design review; ORIGINS.json binds author inputs. Prior merged staged candidate retained in stash, and original diagnosis packet is unchanged.

## Bounded implementation

- Private NotSpawned/Installed current-attempt admission record, separate from historical H5/PID. Initial start transition serialized with Stop; checked attempt exhaustion precedes identity mutation.
- Both legacy and successor final admission checks hold the existing source gate through spawn/install. All late verification/refusal paths check current attempt/admission/state before mutation. No hash/probe/Store work moved under gate; existing successor try-lock refusals retained.
- Explicit LT20 for a matching verifying NotSpawned attempt, revoking its checked token and returning directly. Its event carries actor/reason/stopRecord. The branch never reaches stdin close, group probe/signal, EOF wait or REC closure, and does not overwrite historical Inner.stop_record. No new H5, exit/count/descendant assertion or terminal artifact.
- Legacy handshake settlement now uses the existing scoped generation/attempt settlement path with Installed marker checks. Current-source failure signalling/closure operations are unchanged; stale work is excluded before reaching them. Legacy initialized-write-error handling is preserved while final source checks forbid revival. Successor artifact path remains separate; legacy does not gain S1 publication.
- Test-only barriers work on both routes, and a pre-cleanup tripwire proves LT20 cannot fall through into historical process actions. No universal process-ownership/Child/wait rewrite.

## Final validation at exact frozen bytes

Offline existing cache and `/private/tmp/hosting-s2-target`; CARGO_INCREMENTAL=0, CHIRALITY_SKIP_CODEX=1. Synthetic invented fixture binaries only.

| Mode | Scope | Passed | Ignored | Log |
|---|---|---:|---:|---|
| default | successor::tests | 75 | 2 | stop-admission-successor-default.log |
| default | explicit other Host groups + distribution_ + connector_reconstruction | 163 | 2 | stop-admission-legacy-default.log |
| distribution-successor,custom-protocol | hosting:: + distribution_ + connector_reconstruction | 238 | 4 | stop-admission-production.log |

TEST_PARITY.json verifies the default union equals the production set of 238 passed names. Ignores are existing explicit-export/watchdog/oracle controls, not new skipped admission tests. Six new tests exercise both routes and multiple outcomes: original blocked probe success/failure with Stop-before-release; pre-gate cancellation/newer attempt; check-through-spawn serialization and pre-handshake Stop; stale handshake success/error/contradiction after replacement; historical H5/PID/stop record/REC first-cause preservation and late old EOF; inconsistent markers and overflow. Original D2 now cannot resurrect. Historical REC fixture observes supplier-stop cause before new LT20 and proves it unchanged after old EOF. Existing LT12/LT23, exporter, namespace/root, legacy transport/custody and connector coexistence checks pass, including original root-replacement no-write control.

`validate_private_terms.py --staged --from-host --require-terms`: four files, three terms, zero findings. Cached diff whitespace check passes. No identity override; no commit. Existing ignored synthetic frontendDist bytes used solely for production-feature Rust harness compilation, not frontend/bundle evidence. Disk11GiB before matrix; no new checkout/target or cleanup. Shared target is RELEASED.

## Original failures retained

Original unrepaired D2 is preserved in `/private/tmp/hosting-stop-diagnosis/verify-gate.log` and its diagnosis manifest. This repair's first focused D2 run passed (both routes and success/failure). First six-control run passed5/failed1: pause callback retained its test mutex and blocked a newer start until watchdog; fixed test-only hook to take/drop lock before callback. Second run passed5/failed1: strengthened historical first-cause assertion found the fixture's incomplete turn/home binding produced no actual loss-cause event; fixed synthetic fixture shape (`items:[]`) and explicit synthetic home binding. No product REC changes. Third focused run passed6. Final matrix includes the later both-route pre-handshake hook and checked-overflow ordering; all final logs are distinct and retained.

## Held residuals and review boundary

ALL signal/reap/group-ownership/descendant cleanup repairs remain held, including post-reap numeric identity risk and local allocation failure cleanup. This only suppresses stale attempts before existing actions; it is not a process-group safety proof. LT21/LT22, post-LT12 invalid mapping, missing fallback exit facts, LT23 first-count loss and restart completeness remain held. No full Stop/whole-trace conformance claim. No S3/SEAL2/hydration/native App/supplier qualification, downloads or credentials. B pins/files unchanged; reviewed committed-source export renewal and named adoption remain downstream work.

Independent exact-source implementation review is requested. Author passes are not independent acceptance. No new source edit should occur on this frozen candidate before review feedback.
