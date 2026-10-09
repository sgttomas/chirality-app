# AA-CAP author freeze

Frozen/staged/uncommitted in `/private/tmp/aa-cap-core`, branch `codex/app-v4-aa-cap-core`, basis `7c8c2190e70333e8d3f9b131aee708d493f15b63`. Exactly four authorized source files are listed in CANDIDATE_FILES.json; CANDIDATE.patch and hosting.rs.preimage bind the source delta. No commit/PR/CI/export/B pin change. Shared `/private/tmp/hosting-s2-target` is released; no build/test remains active.

## Basis and scope

Parent release selected exact brief commit `d73672d079c38b1f1e72bb81ee3af26dba70230a`, IMPLEMENTATION_BRIEF SHA `5e1cb22aca5472f30f7e6d31fcdcfc73ba7d33493b09a0f81bfae8caa58e4eee`, with pre-code independent review as retained in REVIEW_AND_RETURN.md. All five SOURCE_BASIS pins matched before edits. Four were present in checkout; the CCE proposal was omitted by sparse checkout but matched current Git bytes via git show. The held first-summary/Route B source was not adopted.

Implementation: normally compiled private dormant core, one optional Inner slot/checked epoch, no production reservation constructor. Ordinary sender calls pass None (including mechanical None arguments on existing private account callsites; no account behavior/action added). The cfg(test) reservation is explicit and single-use on the selected request registration, not a shared next-request switch. No public activation, role/WR source, account, C3 content/mint, accepted contract or new dependency.

Hooks bind actual SourceRequest/H5/pipe, record the receipt-domain dispatch cut at admitted prewrite, settle from the existing actual write result, observe current frames before response removal, and retire on closure/replacement. Existing classification, channels, journal/held frames, automatic replies and REC semantics are preserved. Test-only scheduling/settlement fields are absent from production; production core adds no mutex/worker or IO callback. No full native-schema helper is called by the core.

## Final verification

Exact final maintained bytes are covered by:

* `default-r7.log`:17 passed,0 failed; `cargo test --offline --manifest-path projects/chirality-app-v4/app/src-tauri/Cargo.toml --lib aa_cap -- --test-threads=1 --nocapture`.
* `production-r3.log`:17 passed,0 failed; same command plus `--features distribution-successor,custom-protocol`.

Both used existing private CARGO_HOME, existing shared CARGO_TARGET_DIR, CARGO_INCREMENTAL=0 and CHIRALITY_SKIP_CODEX=1. Only filtered aa_cap tests ran. BUILD_INPUT.json retains the manager-provided116-byte synthetic frontendDist SHA `3bdbdb72ac6c1c06209e7fbe295ff834bdc8ae540bdffc4afe9e9d1b942d162d`; this is a Rust harness compile input, not a frontend/package witness. Disk observed approximately5.5GiB free before final feature run; no duplicate target or evidence cleanup.

Actual test transport is an anonymous CLOEXEC pipe with nonblocking writer and owned read descriptor. Selected original request bytes (≤1024 serialized bytes) are actually written through existing write_complete and read back under1000ms/2048-byte acquisition limits. Mandatory automatic replies are also actual pipe writes outside reentrant hooks. No child process, Host.start, supplier, native App, signal, wait/reap or group action was executed by the test fixtures.

Response/notification frames supplied by tests are synthetic. Two write-error modes are explicitly simulated settlement (prewrite failure and reported partial attempt); neither claims kernel partial-write evidence. Pure core vectors supply simulated facts. A successful pipe case records written from the actual sender; model events alone cannot supply it.

Checks cover explicit reservation/nonstealing, actual complete write, early events before settlement, duplicate uncorrelated responses, late conflict, second final ID/same-text ambiguity, phase/text/extra/timestamp changes, failed/interrupted/unsupported selected fields, wrong Host/H5/thread/turn/pipe/epoch, no attempt, pre-cut receipts, send-vs-receipt separation, closure/retirement/counter exhaustion, limits and no-growth repetition, and absent/limited/refused differential ordinary protocol/client/channel/journal/server-reply/closure outcomes.

## Budget and method evidence

AA-CAP-PF1 fixed expected digest plus key-order/array-order/Unicode/scalar vectors passed. Exact serialized262144-byte input succeeds; one byte over fails without a successful prefix digest. Boundary/one-over controls include depth16, nodes4096 (also counted keys), object/array width128, UTF-8 string65536, key/identity256, request/message text and bounded RPC ID. Compile-time budget predicates and one-over budget tests cover8192 retained,65536 scratch and131072 incremental ceilings.

Measured core inline capacity1944 bytes. All retained identities are fixed arrays; no text/tree is owned by the core. Conservative sorted borrowed-reference capacity accounts for17 encoder recursion frames:52224 bytes, plus4096 visitor/sink/serializer working-value allowance. Compiler/runtime stack-frame overhead and pre-existing Host/parser/source-history storage are not claimed as incremental core-owned buffers. Test-only per-thread allocator accounting measured0 heap bytes for successful maximum-frame PF1, maximum-width object sort, rejected one-over serialization and borrowed-input bind. Cumulative allocated bytes bounds peak heap for those calls. The meter is test-only and delegates to System; no new production allocator/dependency.

Full native schema validity is expressly not performed. A final negative uses a string `Turn.error`: pinned `/definitions/v2/Turn/error` permits TurnError(object) or null. That frame meets the frozen response subset and can reach provisional consistency, while readout still states `nativeSchemaValidation=not-performed-by-core`. This is deliberate proof of limited meaning, not an acceptance of malformed supplier data for later mint.

## Preserved chronology and limits

`default-r1.log` is the original failed compile: four pre-existing include_str fixtures absent from the prepared sparse checkout. Manager restored exact tracked Design directories; no AA-CAP code repair was attributed to that checkout problem. Earlier passes remain separate: r2=9, r3=13, r4=15, default-final=16, r5/r6=17, production-r1=16 and production-r2=17. The final same-count refinement adds explicit interrupted/error-response/changed-result subcases in r7/production-r3. Those are incremental checks, not final-byte coverage. The final schema negative corrected an initially weak omission-of-error assertion after source inspection established error is optional; no earlier pass is relabelled as full schema proof. No assertion failure occurred in the core tests. A shell append attempted from the wrong directory failed without writing; the intended tests were later added at the correct path, with no product files outside the fence.

Official staged private check:4 files,3 private terms,0 findings. Staged diff check passed. Initial index staging was denied by filesystem sandbox; authorized metadata escalation staged the same four files, with no source change or commit.

Independent exact-candidate implementation review remains required, particularly the bounded allocation accounting and provisional shape semantics. Parent selected Group B option B: current-source S4 positives are explicitly held, historical cohorts remain, and no exports/repins are required for AA-CAP. Named receiving disposition belongs to the manager; no bare pin update, attribution/mint/role/account authority, S3 qualification or production activation is inferred from these tests.
