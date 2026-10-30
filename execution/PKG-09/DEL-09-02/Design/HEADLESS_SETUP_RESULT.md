# Existing headless setup route: bounded result and recovery basis

This closes the current setup-test preparation with actual source-bound evidence,
not a new App runtime, schema, qualification dossier or release decision. Current
owner direction authorizes unattended agent computer/UI testing, superseding
the former physical-presence requirement. The latest closure direction starts
no further runs/builds/fronts: retain this result for Agent0 integration/handoff.
All UI actions already performed were AGENT actions under owner direction;
none is represented as a personal owner click or positive human-act qualification.

## Actual focused result

Source: `d908cbec5b3425f0ad37e9a0337a16d427d61cea`, debug test profile,
features `[]`. The retained standalone App remains the different, unsigned
`custom-protocol` candidate `795362874d-a391547a5c5d`; the test runner is not
a new App candidate. Actual raw output, commands, environment, Cargo artifact
and exact source/lock hashes are in
[the headless evidence](../Evidence/EXP/d908cbec5b-headless-setup-20261030T055603Z/result.json).

- ONE offline locked jobs2 test compilation/freshness command passed in
  87.054697 seconds; no second manual compile or broad suite was run.
- Exact Rust `joined_empty_setup_prepare_protected_request_fresh_root_and_native_consumers`:
  **1 passed, 0 failed**, 1922 unrelated tests filtered out.
- Existing `desktop-setup.test.mjs`: **7 passed, 0 failed, 0 skipped**.
  That unchanged Node route internally invokes and asserts **1 passed, 0 failed**
  for `mounted_setup_packets`, then consumes its actual Rust DTO marker.
  Thus the bounded exercised scope is two Rust cases plus seven React checks.
  Node retained producer output in memory; a separate raw DTO log was not saved.
  The already-passing producer was not rerun merely to create another log.
- Entire clone/compile/focused operation: 2026-10-30 05:56:03.429–05:57:37.963Z,
  within the 05:54:46–06:04:46 headless-only window. Required slot and sampled
  App-aware/T3-root deduplicated monitor: no abort, peak 3,669,488 KiB, minimum
  kernel availability 91%. Original candidate/target/cache/witness were not used
  as writable targets; APFS clones and a new scratch Codex home were used.

Cargo identified the actual rebuilt executable (not inferred from its name):

```text
/private/tmp/chirality-headless-setup-rr4kghso/target/debug/deps/chirality_app_v4_lib-849a2caba3ae822e
122,057,288 bytes
SHA-256 a211316352dfdbae6587d321d84e71a8650b71f837ce037c9e9e89889177eb62
```

The Cargo compiler-artifact records `profile.test: true`, `features: []`,
`fresh: false`, the actual package/manifest and executable. Its hash remains
unchanged after the focused runs. The old original-target runner has the same
basename but different bytes/hash (`24b0fb5d…33770b2`) and was not overwritten.
[Source qualification](../Evidence/EXP/d908cbec5b-headless-setup-20261030T055603Z/source-qualification.json)
binds actual source files/manifests/locks and the accepted offline Cargo result;
it claims no exhaustive audit of every transitive source cache.

## Exact existing invocation and reuse

These were the executed commands, using the allowlisted environment retained
in the result: private `CARGO_HOME`/`CARGO_TARGET_DIR`, jobs2, offline,
`CHIRALITY_SKIP_CODEX=1`, fresh scratch `CODEX_HOME` and `TMPDIR`, Node 24 and
the prepared Rust toolchain. No sibling checkout is required by these test
commands. The retained guard source is evidence of this run, not a new product
flag or general framework.

```sh
# cwd: app/src-tauri; one authorized compile/freshness operation
cargo test --offline --locked --lib --no-run --message-format=json

# cwd: app/src-tauri; Cargo-reported executable, exact focused native core case
/private/tmp/chirality-headless-setup-rr4kghso/target/debug/deps/chirality_app_v4_lib-849a2caba3ae822e \
  desktop_startup::tests::joined_empty_setup_prepare_protected_request_fresh_root_and_native_consumers \
  --exact --nocapture --test-threads=1

# cwd: app; includes actual Rust mounted_setup_packets plus React/miniDOM
node --test tests/desktop-setup.test.mjs
```

For later authorized reuse, require matching source/lock/runner identities and
use a newly allocated scratch Codex home. Node's existing route calls Cargo
against that warmed private target; changed source can require compilation,
which needs its own coordinated window. Missing caches/runner/source are an
explicit input gap, not authority to fetch or silently substitute. No rerun is
needed solely to rename this evidence or claim a different screen condition.

## What ran, and what did not

The joined Rust test exercises production create-only prepare/save, actual
0600 request/0700 parent storage, release/reacquisition of real OS-held leases,
fresh resolve/admission, source/home/project binding, and the actual startup
consumer initializer on invented scratch data (records, installation/capture,
attachments, recovery and guidance joins). It asserts Host absent, generation
null, no threads/auth file, and no supplier resource directory. It never calls
`Host::start`. This is a simulated fresh process via dropped/reopened owners,
not an observed OS App quit/relaunch or installed-custody qualification.

The mounted route renders actual React/App source and consumes actual Rust
fixture packets. miniDOM supplies the document/window; IPC responses and handler
calls are injected. Fixture preparation/injected confirmation is not a real
native dialog, human act or production IPC transport. No display, AX,
AppKit/WebKit window, supplier, authentication or model was used. This route
can test routine core logic without screen interaction; an actual screensaver
or locked-session trial was not performed and no lock/security setting changed.
Native WebKit input/AX commit, parented dialogs, actual IPC, supplier startup/
handshake, packaged resource consumption and complete workflow/access-mode
qualification remain uncovered. The headless pass does not repair or convert
the earlier selector automation failure into a native pass.

## Preserved failed A and current applicability

[Native A raw evidence](../Evidence/EXP/795362874d-a391547a5c5d/native-A-20261030T051817Z/result.json)
and the [offline diagnosis](NATIVE_SETUP_SELECTOR_DIAGNOSIS.md) retain the failed
assertions, partial UI states and actor correction. The original App exited/
was reaped code 0 at 05:27:15.115511Z, before its deadline, following targeted
agent Escape/Command-Q. No setup preview/save/account home or admitted supplier
generation was observed; B never launched. The unique App-data root remains
absent, but WebKit/WebsiteData and Caches/WebKit state exists and was not deleted
to manufacture freshness. The three-namespace absence condition must not be
reasserted for a later continuation. No supplier exit facts are fabricated for
a source that was never admitted/observed; sampled monitoring is not an
exhaustive process/network audit.

The raw original state says owner-only actions because it was created before
the later delegated-UI direction. It is preserved unchanged, with this explicit
current attribution. The exact original `b7edb0b0…b417a7` preparation brief is
retained as historical evidence; physical presence is superseded, not silently
claimed satisfied. Native/human-act criteria themselves are not waived.

The closure contribution's full whitespace check reports only the preserved raw
`joined-native-consumers.stdout:6` blank line at EOF. Excluding that one exact
raw-output path leaves the remaining source/docs/evidence diff clean. The raw
bytes/digest are not trimmed or covered by a broad attributes/CI exception.

## Named consumers and retention

The receiving owner is App HELP_HUMAN/Agent0 in
<t3-thread://v2/00d44996-9458-4eba-bed2-ffb8f49dab60/dcd88874-e45b-4faf-ad20-7541072dc619>,
for integration and the announced project-Agent0 handoff. DEL-09-02's standalone
examination owner consumes this bounded proof and its native gaps; DEL-01-06's
desktop/publication owner retains the candidate and source/package context.

Retain `/private/tmp/chirality-desktop-current-ukt5ir80/` (candidate, archive,
original target, witness inputs, failed A, controller draft and review copies)
and `/private/tmp/chirality-headless-setup-rr4kghso/` (qualified runner, cloned
cache/target, fresh test home, commands/raw output). The offline live-controller
draft is AST-parsed only, SHA-256
`91c9ca98d7bf8d784e2cea5cbd42d237230b9018d58f5e04e369a755d5b7720c`;
it was never launched, is not a qualified supported tool, and closure does not
authorize running it. Its exact unused source is also retained as
[raw `.py.txt` evidence](../Evidence/EXP/d908cbec5b-headless-setup-20261030T055603Z/offline-native-controller-v2.py.txt),
so it is not stranded only in scratch. It was used by neither native A nor the
headless run, and remains an unsupported draft, not a reusable invocation or
product implementation. Raw repository evidence carries `SHA256SUMS`; cache and
large runner remain local at the exact paths/hashes above. No deletion until
Agent0/named consumers confirm recovery and retention needs are satisfied.

Cleanup disposition for that confirmation: preserve the original candidate/
archive/build/witness and qualified headless runner plus raw result/provenance.
The separate headless Cargo-cache clone, duplicate bundle/build objects and
temporary test files are disposable after integration unless Agent0 identifies
an actual warm-target replay need. Removing those inputs would end the warmed
Cargo/Node invocation basis; later reuse would require the retained prepared
source cache and a separately authorized compile, not an automatic fetch.
Do not retain this worktree solely as the storage location for drafts: they are
included in this closure PR. Retire only integrated owned refs/worktree after
the receiving owner clears handoff/recovery. No such deletion is performed by
this collection change.

The existing [terms owner-action proposal](../../../PKG-01/DEL-01-06/Design/OPENAI_SIGNIN_OWNER_ACTION_DRAFT.md)
is included solely as **PENDING OWNER DISPOSITION**, exact SHA-256
`6e75343511784b3effb3fe20158bd725c6980a978735cb9145821a6cf034c4ce`.
Its retained consumer is Agent0/owner for actual first-offering/evidence
disposition. No accepted clauses/schema/terms record, supplier contact,
distribution decision, acceptance, release or production custody changes here.
No new fronts, reviews or runtime work follow from this closure contribution.
