# CC-HOSTING-DISTRIBUTION-01 / S1 Design adoption

This named technical Design patch selects the S1 contract definitions under the
App implementation owner's U-08/U-17 direction relayed by HELP_HUMAN. Prepared
against main `9f1f96b17b9a9307827b8d00ae880a6c9a2c0039`; effective as a Design
source selection when this patch is independently reviewed and integrated.
Before then it is a review candidate. This is not a supplier-reference
attestation, consumer rollout, product acceptance, qualification or release.
No current supplier record becomes qualified by this selection.

## Single authoritative cohort and ownership

This directory is the single maintained Design home for the six S1 schemas and
their executable value rules. DEL-01-01 owns expected-reference, separate
adoption-attestation, observed-verification, lifecycle-event and inventory-artifact;
DEL-01-06 owns pkg-identity and its retained package obligations. Its adjacent
Design supplement selects this same physical cohort; there is no second package
schema copy. PUBLICATION.json binds every published file to the exact reviewed
source. All nine artifacts are unchanged from candidate `7aa1ae354b`, reviewed
in `7b3105d009` (PR #1125). The old run directory remains historical review
evidence, not a second current authority or a dependency of this directory.

The six `urn:chirality:distribution-successor:*` schema IDs and exact bytes are
retained. `model.py` supplies the schema-plus-semantic value rules; `basis.json`
retains its exact source dependencies, and `test_model.py` generates synthetic
fixtures in a temporary directory. The historical instruction-read entries in
basis.json are provenance, not instructions activated by this publication.
No example is a qualified supplier record. Any future schema or semantic change
needs a named reviewed successor; never silently change the meaning of an old ID.

## Precisely selected method and precedence

For this S1 cohort only, select these clauses of the unchanged sibling
DISTRIBUTION_IDENTITY.md (SHA-256
`d51c1130f5a1356fcc2a6100f1486e8ee3a0728de59f4fe69d4ac6a1580e5290`):

- Distribution identity method `codex-vendor-tree-v1`, in full: complete tree,
  root/directory modes, exact file bytes/modes/sizes, compatible file manifest,
  bounded entry restrictions and exact case-sensitive path identity.
- Launcher and configuration, in full: direct vendor executable and recorded
  PATH/configuration behavior, without authority to execute a supplier.
- Verifier obligations and standing, in full: full comparison before probe,
  pre-spawn revalidation, missing expectation unverifiable, contradiction
  precedence, descriptor custody and residual race limits.
- Expected-record provenance and bounded qualification, except its first
  paragraph is replaced for S1 by the separate-artifact paragraph below.

For this cohort, this supplement supersedes that file's header's staging-only
status, its statement that these method choices are unselected, and its
Representation and migration statement that the successor schemas are undelivered.
Those statements remain true of the historical proposal and old readers; they
are not the current standing of this published S1 definition. The remainder of
Representation and migration and Consumer and check boundary remains mandatory
migration guidance: exact-byte resolution, explicit versions, no old-shape
extension, joined consumer adoption and distinct native/package obligations.
Its historical MEMORY direction is superseded by the owner's no-memory direction.
This precedence does not apply the old PROPOSED_DESIGN.patch or change accepted
HOSTING_BOUNDARY.md, PACKAGING_AND_DISTRIBUTION.md or any consumer source pin.

The distribution-identity part of U-08 and the bounded direct-vendor composition/
launcher choice in U-17 are selected for this successor definition. Other
identity subjects, actual acquisition/pin choice, U-15/U-16 and implementation
conformance remain at their existing owners and points of need.

## Separate reference and qualification attestation

A supplier reference is an immutable artifact produced by DEL-01-01, not a
caller assertion or a runtime observation promoted in place. It carries
schema/method version; supplier pin/platform; official archive locator and
digest, acquisition authorization/custody evidence; extraction procedure/source
subtree; complete inventory and manifest; launcher convention; maintained
generated-output identity (pin, kind/variant, formatter policy, manifest); and
digest-bound observation evidence. Freeze these bytes before independent review.
A separate immutable qualification attestation identifies the reference by
exact-byte SHA-256, its author, independent reviewer, reviewed source revision,
review evidence and named technical adoption. The attestation does not embed its
own digest; trusted App build selection binds both artifacts. Missing or
untrusted attestation is unverifiable. Neither a qualified boolean, schema
conformance nor equal digests establish reviewer authority or qualification.
Neither artifact contains the final App package identity.

The ordered chain is reference → attestation → build-selection bytes → compiled
App anchor → package identity. Build selection identifies method/schema versions
and exact reference/attestation digests; its exact-byte digest is compiled from
the reviewed build recipe. No production caller path, environment value, UI flag
or replaceable resource pair may select that anchor. Signature/build integrity
and trusted stable installed custody remain required, not inferred from hashes.
An observed runtime witness remains outside the installer it measures. Logical
package-record ID is not the package-envelope digest. This avoids self-hash cycles.
The offline checker's selected-attestation argument is an explicit trusted test
seam, never production caller authority. S3 must supply actual separately
reviewed acquisition/generation/probe/version-advance evidence. PKG R23-22 still
selects the actual eligible pin; fixture 9.9.9 and historical 0.160.0 are not choices.

## Closed shapes and semantic duties

Schema conformance alone is insufficient. The unchanged model retains:

1. Local contained artifact resolution; hash exact bytes before parsing; unknown
   versions refuse. Re-serialized JSON is a different artifact.
2. Full inventory validity/equality and the preserved inventory method; manifest
   equality alone cannot establish tree equality.
3. Exact reference/attestation subject and selected digest; different author and
   reviewer values; required evidence resolution. Value checks do not authenticate
   people, evidence content or adoption authority.
4. Pin/platform/generated and raw/parsed label agreement. The label syntax is
   exactly `codex-cli <major.minor.patch>` with optional final LF. Unsupported
   syntax requires a successor, not heuristic acceptance.
5. Contradiction before missing/unverifiable before verified. Check evidence,
   launcher roots/PATH, wrapper environment and separate homes retain their rules.
6. Original v0.9 lifecycle shape and transition table; exact verification/full
   generation joins; LT-04 requires verified pre-spawn evidence. LT-24 requires
   actual label and unverifiable pre-spawn evidence, preserves its explicit
   development authorization/announcement and cannot waive mismatch. Early
   no-verification events remain only those explicitly enumerated by the model.
7. Full original PKG-v0.2 shape and semantic duties, static inventory comparison,
   exact candidate/runtime joins and explicit missing qualification. Package
   reference-equal is not runtime verified or FP-2/W-4. An optional runtime
   observation must belong to the exact App revision/build, package record and
   pre-notarisation installer digest. Every-Mach-O coverage is an evidenced input,
   not something the value model discovers.

All old closed schemas and records retain their original meaning. No new field
is added to a legacy record, no unsupported event becomes valid, and no opaque
EXP/SQ string gains artifact authority. PK-R4's separate terms schema/checker
remains mandatory; this model does not execute it. Signing, notarisation,
entitlements, quarantine, FP checks and install/package witnesses remain separate.
The preserved semantic oracle checks values, not complete lifecycle streams,
filesystem races, authentic evidence, actual source custody or supplier behavior.

## Held Host work and consumer activation

H11, HOSTING §4.7, REC loss/closure duties, automatic restart requirements and
existing descendant/Stop policy remain unchanged. The held STOP-STATE-01 Part1
Design is NOT READY: wait/signal/reap ownership and post-reap availability remain
unresolved. This definition does not publish LT25, authorize cached PID/PGID
signalling, waive restart, manufacture empty descendant checks, close a
historical generation as current, or license any held repair. Current bounded
reader/export support is not proof of complete Host conformance.

Consumers must select the exact versioned cohort and implement its joined
behavior before moving pins or relying on it. Byte-identical embedded schemas
are correspondence evidence only. At this patch's basis: Host staged readers
and S4 file cohorts exist with explicit unsupported installed-custody/verified
limits; legacy packaging remains active; #1161 SQ-EXP-RECEIVING-v1 checks selected
legacy SQ/EXP/review/package bytes and coverage, not S1 PKG semantics or supplier
qualification. None is switched by this publication. The accompanying impact
notice names exact current inputs and remaining receiving work.

Run the Design oracle offline with `PYTHONDONTWRITEBYTECODE=1 python3 test_model.py`
in this directory. Passing synthetic checks establishes representation and rules,
not any of the excluded operational or authority facts.
