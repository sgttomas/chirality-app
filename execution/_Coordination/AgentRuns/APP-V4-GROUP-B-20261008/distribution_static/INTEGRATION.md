# A-IN-S2 static distribution connection

Base main15f5c51818 after reviewed S1 Design adoption. WORKING_ITEMS
/root/distribution_integration_manager under HELP_HUMAN; existing TASK
production_roles owns new scanner example/tests, production_workflows owns new
packaging/static_distribution/tests and scoped prepare.py dispatch, existing TASK
bundle_review independently reviews. No new agents/worktrees. Existing worktrees
use new branches preserving earlier refs. Manager owns fan-in and exact-head checks.

## Missing connection and approved fence

Legacy packaging copies P1 from a caller manifest but does not consume an exact
S1 reference/attestation/build-selection closure joined to candidate/package bytes.
Native Selected::production is intentionally unavailable without S3 compiled
selection; its fixture constructor is test-only. Store adds native namespace/H5
custody. Neither capability can be manufactured by a static caller's JSON/digest.
Existing preflight/selection/store source hashes also participate in S4 identity.
The parent approved a separate static support consumer, leaving those files/pins
unchanged rather than expanding this slice into a source renewal.

Only new scanner example, packaging consumer/fixtures/tests/source guard, and a
scoped prepare.py command dispatch are allowed. Existing prepare commands and
source guards remain. The scanner calls unchanged public scan/equal; no supplier,
label probe, launcher, native App, signing or credentials. A Cargo example target
avoids adding a second App binary/default-run ambiguity. Existing semantic/store
code informed the authority boundary; no parallel native authority is invented.

## Bounded work graph and contract

| Node | Owner / output | Check / standing |
|---|---|---|
| S2-ST1 | Existing production_roles; new offline scanner example/tests | Actual descriptor scanner invoked on invented trees; bytes/mode/type/link refusals; no supplier invocation |
| S2-ST2 | Existing production_workflows; actual prepare.py static-distribution route | Exact selected artifact closure, S1 and retained legacy PKG/terms checks; physical scan; candidate/installer binding; stale-input negatives |
| S2-ST3 | Manager; joined maintained consuming-path checks | Invoke actual command and scanner, preserve old commands/pins, inspect report/counterexamples |
| S2-ST4 | Existing bundle_review; independent actual-head review | No false trusted anchor, no mismatch hidden by missing qualification, no source reopen substitution or invented unmeasured side |
| S2-ST5 | HELP_HUMAN receiving | Reviewed exact commit, checks/limits; parent coordinates PR/merge |

ST1+ST2→ST3→ST4 (repair loop)→ST5. The report's permanent standing is
development-unverifiable. Static equality/mismatch and source/value-check results
are separate fields; none is production verified or S1 reference-equal standing.
Inputs bind exact selected build-selection, reference, attestation and evidence,
S1 package and separately selected legacy PKG/terms, candidate descriptor and
installer bytes. Measured published and/or packaged sides are explicit; an
unmeasured side is never invented. The legacy record has no App-binary digest,
so exact selected record/installer correspondence does not authenticate App code.

Current missing compiled production trust, installed custody, real label/probe,
qualification and native/package witnesses remain missing. No H5, Host event,
Selected/Store capability or qualification attestation is minted by this tool.
Known tree/pin/candidate contradiction outranks absent trust. Source drift refuses
and requires a reviewed new selection, never an existing-reader pin refresh.

## Limits and authority

Owner explicitly excludes Codex supplier/probe/launcher execution, H11 Stop,
production verified standing, S3 qualification, signing, credentials and native
App witnesses. No MEMORY writes: active owner direction supersedes the loop
convention. New private tool source selection does not change historical readers
or accepted packaging sources.json. Parent confirmed shared prepare.py fence
before edits. Review/validation and actual freezes will be appended at fan-in.
