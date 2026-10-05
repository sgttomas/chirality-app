# Parent-run ROLE supplier capture probe

Prepared read-only TASK assignment, 2026-10-05. The author did **not** execute
Codex, start a provider/server, access auth/credentials, predict a model response,
run Cargo, download anything or edit App/Design sources. Independent candidate
check precedes parent execution. `ROLE_SUPPLIER_PROBE.py` uses only Python's
standard library.

Run from the repository root, with the parent's approved stock 0.160.0 binary:

```sh
python3 projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/probes/ROLE_SUPPLIER_PROBE.py \
  --codex "$CHIRALITY_CODEX_BIN" \
  --report projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/probes/ROLE_SUPPLIER_PROBE.result.json \
  --keep-scratch --timeout 20
```

`CHIRALITY_CODEX_BIN` must be the approved executable. The script hashes it before
launch and refuses any value other than the maintained 0.160.0 development hash
`112fae7a5a1223e673c8a1791d32338f37df8b527ff1159bb8adac6c4dbf1b4b`.
Matching this hash leaves the supplier **unverified-development**; it establishes
no qualified distribution identity. No existing Codex home or credential is used.

The owned mode0700 scratch root and its fresh CODEX_HOME are each made by
literal `/usr/bin/mktemp -d` at parent execution, as LOOP requires. The root
contains an otherwise empty workspace, synthetic native global/project AGENTS markers, private raw request
payloads and native stderr. The explicit provider is loopback127.0.0.1 only,
Responses wire API, explicit `gpt-6.1-sol` with `medium` effort, no OpenAI auth,
plugins/analytics off and remote-control loop disabled. Model/effort are named
in scratch configuration; medium is also sent as native turn/start effort.
The report retains actual native/provider-reported values separately. No user config is altered. This is configuration, not a claim of
OS-enforced network isolation or a measured socket census.

The capture-only endpoint records JSON request bodies locally and deliberately
returns HTTP400. It never reads/stores auth headers or forwards traffic. There
is no model prediction; error completion is expected. Two fresh threads use the
same native process/home/workspace/model/provider/prompt: no-App-guidance baseline,
then common + HELP_HUMAN. Actual server requests are not silently ignored: an
unexpected request gets an explicit unsupported-fixture error and aborts the
probe. Per-operation timeouts and process-group cleanup bound execution. Cleanup
checks the launch PGID even after normal stdin closure or an already exited
leader, signals remaining members with SIGTERM then bounded SIGKILL if needed,
and verifies process-group absence. Leader exit alone never establishes tree
end. An observable group remaining after bounded cleanup is unknown/failure,
sets the witness failed, and is reported; no cleanup success is fabricated.

## Pinned source/composition oracle

This script does not call Rust `Composition::new` or the App Host wrapper. It
uses the independently checked exact output permitted by the brief. It reads the
maintained reviewed resources, refuses changed common/role source hashes,
composes the exact production separator, then asserts **4856 bytes** and SHA256
`ad560fe79f9552fef1042dd613a0274ca87babd7165bc1ecd0a278a3ada98343`.
Common source SHA256 is `d9233f5af0393e045f0d50fe14b60ede6ec3558da625c1a0deec84fae07afc27`;
HELP_HUMAN source SHA256 is `11e619e41acad799b90552dda19a3d49c4d3921bcebbce7317254a58d03e04be`.
Role offset3887/length969, common offset0/length3858. Identity designation is
`chirality.app.exact-bytes.sha256/v1`; full composition and part hashes are
retained in the structural report. The wrapper's independently tested transport
facts and this native probe must be joined explicitly before claiming a
connected App journey.

## Oracles and truthful outcomes

Exit0 requires all of these; otherwise exit1 with structural evidence/error:

- Exact complete composition occurs in an actual provider **developer** text
  segment and is absent from the baseline. A occurrence in user/system text
  alone does not satisfy the developer carrier oracle.
- Actual observable native base text (`instructions`, or system message text)
  is nonempty and byte-equal across the paired captures. If those sources are
  absent, base preservation is **unknown** and this witness does not pass;
  omitted baseInstructions alone is insufficient.
- Synthetic native global and project markers occur in both request payloads.
  Neither marker is repeated in the user prompt or product composition.
  Native reported instructionSources is retained separately, including
  empty/not-reported; marker content does not manufacture a source-path report.
- Native request correlation/start responses are observed, and synthetic
  source/config files remain byte-identical after the pair.

The durable JSON contains only structural comparisons, source/bytes hashes,
known marker strings, instruction-source path reports, thread/turn references
and limits. It contains no whole supplier prompts, raw payload or auth header.
Raw bodies/stderr remain scratch-local when `--keep-scratch` is passed. Inspect
that **exact report-named scratch directory** locally for independent checking;
then remove it when its parent-owned evidence disposition permits. Without the
flag, the scratch tree is removed on completion. Processes/provider sockets are
closed in either case. Do not attach raw payloads to public Git/PR records.

This is primary HELP_HUMAN carriage/base/discovery evidence at one synthetic
route. Adoption is always unknown. No other primary/no-role coverage, role store
seeding/upgrade, lifetime/resume/fork, child configuration/inheritance, delegation
availability/enforcement, real model behavior or supplier/product qualification
is proved. A provider/schema failure or unexpected native request is a finding,
not a permission to change the oracle or claim supplied guidance.

## Author verification

Syntax compilation and pure helper checks only: the pinned production-output
oracle matches, and invented provider payloads distinguish exact carriage,
wrong user-only placement, changed native base and missing discovery markers.
No HTTP server or subprocess was started during author verification. The script
is prepared for independent review and parent execution, not reported run.

## Successor reviewer repair and preparation evidence

Original submitted candidate remains identified by script SHA256
`b19b175b5b5196c0dc429ee16524dac812b3156d63ea6d7b5b1968d407333fe6`
and README SHA256
`72fb2ef100e82461f92cbe83f404a80bda0be0ae821327f93d8045bb10b6199b`.
Manager relayed same-reviewer findings: empty instructions in both captures
produced nonempty segment lists containing empty bytes and incorrectly passed;
cleanup equated leader exit with process-group completion. These are repaired
within this original probe fence. No earlier executed native witness is claimed.

The successor requires at least one actual nonzero-length native-base segment
in **each** capture. Missing or empty base yields observable=false,
byte-equality=unknown and passed=false. The full original segment byte lists
remain the equality oracle, including empty segments/CRLF/whitespace; no
trimming or normalization makes unequal source bytes equal. Cleanup verifies
and terminates remaining owned process-group members even if the leader has
already exited, with explicit bounded failure if absence is not established.

Root's additional relayed corrections are included: the explicitly selected
capture-only model is gpt-6.1-sol with medium effort, rather than an arbitrary
unknown model, and literal mktemp-d creates CODEX_HOME and the containing root.
This still executes no prediction and proves no qualified model availability.

Harmless source-only self-check command (does not run Codex, HTTP, provider,
actual mktemp, auth, network or OS signal):

```sh
python3 projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/probes/ROLE_SUPPLIER_PROBE.py --self-check
```

Author observed exit0:

```text
PASS empty-base unknown/fail; exact CRLF byte comparison; five fake leader/descendant cleanup cases; model/effort constants. No native/provider/mktemp/OS signal executed.
```

The five cleanup cases cover leader already exited/normal stdin exit, each with
TERM-responsive and TERM-resistant descendants, plus a group still observable
after KILL that must fail. All signals, clock advancement, process waits and
streams are injected fakes. The actual mktemp/native/provider path remains
unexecuted and held for the same reviewer's successor backcheck and parent run.

## R1 constructor ownership and POST-only fixture successor

R1 submitted candidate association remains script
`98eca0a3055cf9791b38a26a47dd259f4d728d3d3d16b7e69a926a1f820719d8`
and README
`5a4a61d73903dd8e13e95451713761b6f7bedc136eb1974fc342927c78d5f9cb`.
Same reviewer `reviews/V0-ROLE-SUPPLIER-PROBE-R1.md` found the constructor branch
NOT READY: after Popen success, a failed reader setup left main's rpc unset and
the group/stderr unowned. Root resumed the original TASK for this ordinary
bounded repair; WORKING_ITEMS retains integration. Native execution remains held.

The constructor now establishes owned process/stderr state before reader
construction/start and guards every acquisition. Failed Popen closes the opened
stderr. Failed post-spawn reader construction/start invokes the same bounded
process-group termination/absence/reap/stream cleanup before rethrowing. If
cleanup cannot be established, the original exception carries that failure note;
an exception is never treated as proof that no child exists. Unstarted readers
are not joined. Cleanup ownership precedes constructor return, rather than
relying on main to receive an object that was never returned.

Three source-only constructor regressions inject spawn failure, reader factory
failure and reader start failure. Every fake cleanup primitive (killpg, clock,
sleep) is passed explicitly into the constructor; no default-bound actual
os.killpg can be reached. The fake cases assert stderr closure, no group operation
for failed spawn, and group absence/reap/stdin closure for successful spawn then
failed reader setup. Original empty-instructions and empty-system unknown/fail,
exact CRLF comparison and five leader/descendant cleanup cases remain.

The capture-only custom provider now explicitly sets
`supports_websockets = false`: it implements HTTP POST only. This is test-fixture
configuration, not a product default or availability qualification. Pinned source
support was directly checked by the manager and supplied to this TASK:
[Codex rust-v0.160.0 model-provider-info src/lib.rs lines179–181](https://raw.githubusercontent.com/openai/codex/rust-v0.160.0/codex-rs/model-provider-info/src/lib.rs)
defines the serde-default `pub supports_websockets: bool`. This TASK made no
external read; an earlier older-path404 was lookup history, not evidence of
absence. Explicit gpt-6.1-sol/medium, actual mktemp-d, exact reviewed composition
and capture/report custody are unchanged.

Author source-only command `python3 -B ROLE_SUPPLIER_PROBE.py --self-check`
(using the actual probe path) exits0 with:

```text
PASS empty-base unknown/fail; exact CRLF byte comparison; five fake leader/descendant cleanup cases; three guarded constructor failures; model/effort constants. No native/provider/mktemp/OS signal executed.
```

The same reviewer was notified of the source repair before successor freeze.
No actual subprocess, native/provider/server, mktemp, OS signal, model, auth,
network, Cargo, Git or delegation was executed. Successor source backcheck and
parent execution remain distinct unfinished steps.
