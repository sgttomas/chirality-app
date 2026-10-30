# S4 installed-integrity technical clause

Named technical change: `S4-INSTALLED-INTEGRITY-01`, 2026-10-30. Implements the
App Agent 0 direction for the explicitly selected S1 production route. Source
selection is [distribution-s1/README.md](distribution-s1/README.md), selecting
original pre-flattening DISTRIBUTION_IDENTITY SHA-256
`d51c1130f5a1356fcc2a6100f1486e8ee3a0728de59f4fe69d4ac6a1580e5290`.
The current sibling and historical PROPOSED_DESIGN.patch are not adopted.
This clause supplies the installed-observation mechanism under HOSTING §7.2;
it does not change commitments, select a publisher or qualified supplier pin,
accept an App candidate, or authorize signing, accounts or release.

## Live production rule

After selected full supplier-tree and generated-reference equality, the App
observes its own installed bundle and running process through Security.framework.
`installed_custody.rs` compiles `COMPILED_PUBLISHER_REQUIREMENT: Option<&str> = None`.
The absent selection refuses before signature/identity inspection or supplier
execution. Owner selection must independently bind the production bundle
identifier and publisher/certificate anchor. The App's designated requirement,
environment, UI, caller path and disk evidence cannot supply this authority.
Debug, development, non-macOS, unsigned and ad-hoc cases cannot pass production.

Static validation uses strict validation, all architectures and nested code,
without skipping resources or executable validation, plus no-network. Dynamic
validation checks the running process against the SAME requirement, no-network.
Both observations must agree on executable location, cdhash, bundle identifier,
team identifier and signature flags; ad-hoc signatures, absent hardened runtime
and enabled or malformed get-task-allow refuse. Nested standard code locations
are validated recursively; sealed non-code resources are checked by static
validation. Full supplier-tree equality separately covers every supplier byte.
This does not add a supplier-signature trust anchor or runtime SecAssessment.

The observer resolves the current executable's own bundle. The supplied resource
location is only compared to that bundle's Contents/Resources, never used to
choose the object trusted. The observer returns a private-field process-local
`InstalledCustody`, with no deserialization constructor. Only after that result
may the isolated label probe run. Tree equality and installed integrity are
rechecked after the probe and at the existing final pre-spawn revalidation,
without changing native generation/admission gates or process/quit custody.
Known supplier-tree contradiction dominates a missing publisher requirement.

The Security SDK's dynamic no-network capability requires macOS 11.3 or later;
unsupported API/flag results refuse. This does not select a product minimum OS.
No publisher identity or entitlement is inspected by this change's None-gated
production path. Source fixtures use invented values, and no codesign operation
is part of assurance.

## Versioned evidence and reader

`observed-lifecycle-reader.s4.v1` selects new `observed-verification.s4` and
`lifecycle-event.s4` envelopes. Old shapes keep their original meaning: the
historical `observed-lifecycle-reader.s3.v0.10` path refuses custody pass and S4
records. Old schema IDs/source hashes and frozen receiving pins are unchanged.
The S4 extension is separate from the frozen S1 PUBLICATION.json cohort.

The custody check references exact bytes of `installed-custody-observation.s4`:

- Full generation tuple, complete inventory and selected source/build-selection,
  reference and adoption-attestation association.
- App observer revision, requirement text digest, exact static/dynamic flags,
  matching cdhash/identifier/team/signature flags/get-task-allow facts.
- Resolved bundle, executable, Resources and parent paths; translocation is
  `not-established`, with only a separately identified AppTranslocation path
  component observation.
- `process-observation-evidence-only` standing, trusted-stable-installed-bundle-and-parent-path assumption,
  explicit mutation/check-to-exec and qualification limits.

Hash-before-parse, closed shapes, known revisions, semantic facts and all joins
are required. Null/opaque evidence, different generation/inventory/selection,
requirement or cdhash, or reserialization under the old digest refuse. The Store
requires a typed observation to publish a verified pre-spawn record; its reader
checks correspondence only. No readback constructs live startup authority.
Synthetic positive evidence is explicitly marked and supported only by cfg(test).

## Consumers and limits

The successor alone reports `verified-pin`; legacy `verified` and development
`unverified-development` remain unchanged. NativeActivity, App diagnostics and
native_items project the host standing and evidence; they do not derive trust
from these strings. The frozen `app/examination/distribution_receiving/receive.py`
requires unverified-development and rejects verified evidence. EXP/SQ package
joins and `app/packaging/static_distribution/check.py` retain their existing
cohorts; the latter requires `verification_artifact: null`. S4 does not activate
those producers/readers or repin them. Their later adoption needs explicit
candidate-bound receiving evidence. See the DEL-01-06
[signing join](../../DEL-01-06/Work/INSTALLED_INTEGRITY_S4_SIGNING_JOIN.md).

A trusted stable installed bundle and parent path are assumptions, not
immutability. Parent writability is not checked; translocated launches are
recorded, not refused solely for translocation. Hostile same-user
or administrator mutation and the bounded check-to-exec race remain. No observed
App Management protection, translocation guarantee, quarantine, Gatekeeper,
notarization or installation witness is claimed. S4 source checks are not
FP-1a/b, FP-2, FP-3, FP-4, FP-5 or W-4, and cannot supply S5's native witness.
Production remains unavailable with the compiled requirement None.

## Assurance and remaining evidence

Focused source fixtures exercise synthetic positive observation/LT-04, exact
joins and historical refusal, unsigned/ad-hoc and invalid signing facts, None/
debug/platform gates, pre-probe supplier contradiction, and a non-Codex resource
mutation despite equal supplier tree. They do not execute the actual supplier,
model or native candidate. Check results and independent review are retained in
the reviewed PR; failures and unrun native qualification remain distinct.

Implementation source verification on 2026-10-30: offline macOS Rust library
filter `installed_` passed 11 tests (10 installed-observer/S4 cases plus one
existing installed-workflow test). The build-selection regression group passed
9 tests; its explicitly supplied stock-tree check remained ignored. Both ran
through t3_cargo/t3_slot with jobs=2, memory guard active, fresh scratch Codex
homes and scratch temporary directories. Schema correspondence passed for all
14 maintained mappings; deliverables check reported zero errors. These are
source-test results, not a signed-App FFI success or native/package witness.

Signing information returned for the dynamic process is disk-backed (including
Security.framework kSecCodeInfoFlags); matching static/dynamic fields are a
consistency join, not independent runtime integrity proof. Running-process
assurance comes from SecCodeCheckValidity against the same compiled requirement.
Optional kernel guest-requirement matching can be assessed with the later exact
publisher requirement; it is not claimed here. The trusted stable parent-path
assumption and unestablished translocation/App Management protections remain
explicit limits, not observed access controls.

Independent Claude Opus 5.5/high review of e555852b plus CI-only 7b9f8cd6
identified a redundant production_config store flag that changed a source test's
refusal point. The flag was removed, preserving real callers' existing store
requirements. Review repairs also reject mixed S4/old observed envelopes, require
S4 custody pass and matching verified-pin standing, move Store signature recheck
before its namespace lease, and clarify disk-backed signing information and
trusted stable parent-path assumptions. The compiled requirement stays None;
these repairs do not activate package/EXP/SQ consumers or qualify native behavior.

Post-review verification: the entire `hosting::successor::tests` module with
`distribution-successor` enabled passed 103 tests; four explicit stock/export
opt-ins remained ignored. `installed_custody::tests` passed four tests. The
previously broken production override/refusal test passed and is now selected
explicitly by PR CI. CI-selection tests passed 62; schema mappings remained 14
passing and deliverables reported zero errors. The guarded successor test process
completed normally in about 102 seconds; no actual stock supplier, model or
retained native candidate was run. The reviewer found no further blocker within
the None-gated source scope; the manager implemented and checked the bounded
repairs rather than claiming a signed-runtime success.
