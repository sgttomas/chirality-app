# Current artifact — signing decision delta

Prepared for the manager's assessment, not an owner prompt or authorization.
This updates the candidate facts in ../signing-preparation/DECISION_PACKET.md;
that historical packet stays unchanged. PKG Design §§3–4 and7–9, its reviewed
CF/FP/SIGN requirements and canonical unresolved OpenAI terms remain the warrants.
No new command, identity lookup, copy, build, signing or native action occurred.

## Exact reviewed subject

Artifact author cc18e792f4ced071605bce9709c6d1397de36540; independent physical review
65ad37c8aecbc388c7021bfcc2fda048141186c6 found no blocking findings. The review checked
all1,033 source inputs and75 App entries plus actual ZIP payload, not merely logs.
Built source is9a82cbcf29c46bb6f722c074b5854de7ef470450, current at its freeze only;
build identity B2-UNSIGNED-9a82cbcf-20261009. This replaces the stale f793 artifact
as the subject of this decision delta, not as a rewrite of its evidence.

| Subject | Bound identity |
|---|---|
| App file manifest | 5ee389191acb585483efbf1e54dde5034e1b44aa1bd22e2df4b70ff793d14bfd |
| P0 executable SHA-256 | 7fe364a05737f4f9696eb4fb9d6cf9671000c4c38a5ac5ca950bc1b0c637bca0 |
| Actual app_zip SHA-256 | a3ea8fba0045e1e9773dc7755bc613066c278a81e1432b6986e0b9619a5ac09f |
| ZIP size | 145846066 bytes |
| Actual configuration | Development debug, arm64, custom-protocol only; default legacy distribution; no successor/synthetic anchor |
| CF5 values | dev.chirality.app-v4.skeleton; version0.0.0; minimum macOS15.0; no microphone key |

The retained paths are those in RETURN.md and the independent artifact review.
P1/P2/P3 equal their selected sources. P1 is cached development0.160.0, not an
R23-22 qualification selection. P0 remains incidental linker-ad-hoc, without an
App Developer ID, sealed resources or bound Info.plist. The actual unsigned ZIP
is available; no faithful legacy PKG identity or full static-consumer result exists.

## Smallest useful next decision

A **limited App-signing experiment on a preserved copy of this exact development
candidate** is now concrete enough for the manager to assess. Its question is
whether explicit P0/outer App signing under SIGN-1 Option B leaves P1 unchanged
and yields a valid outer signature. It would not qualify the supplier, exercise
runtime, notarise, install, release, or settle production configuration.

Before an executable point-action package can be issued, the owner must choose
that limited purpose and accept these exact development CF5 values for the
experiment, or select different values/source requiring a new build and review.
The actual Developer ID Application name and team (CF1) and owner account-act
direction are not supplied. No keychain or signing-identity discovery has been
performed. For this limited purpose, explicitly select SIGN-3's no additional
App entitlements arrangement and exclude SEAL-2/key-store qualification; if that
purpose needs entitlements, their exact files and rationale are inputs first.
These are real choices and missing inputs, not invented signer placeholders.

The absent S3 reference, R23-22 qualified selection and verified H3B are **not a
technical gate to this limited static signing experiment**. They prevent using
its result as a qualified production package, supplier verification or FP2/W4
runtime witness. A broader intended outcome would need those contributions at
its relevant receiving/runtime point. The actual post-sign installed FP2/W4
witness cannot be required before the signing that makes it possible.

No owner question or signing request is issued by this delta. If the manager
chooses to pursue the limited experiment, obtain the above concrete selections
and actual identity/direction, then present a narrowly bounded point-action
package. Otherwise retain this reviewed unsigned artifact without another build.

## Consequences and sequence after any later authorization

1. Preserve the reviewed unsigned App and ZIP unchanged. Make a separately owned
   experiment copy and verify its complete identity first. This makes abandonment
   reversible by retaining the original; signing itself changes bytes and cannot
   be described as preserving the original artifact identity.
2. Reconfirm pre-sign P1 equality against the selected cached tree (the observed
   FP1(a) comparison operation). Apply the selected Developer ID to P0 first and
   then the explicit outer App. As repaired in the earlier packet, only the
   outer-App operation uses --force to replace the ordinary signature established
   by the first step. Neither signing operation uses --deep; supplier signatures
   are not replacement targets. No commands are run here.
3. Recompare P1 bytes, modes, links and member set after signing; perform the
   required deep strict **verification**, then bind new P0, App inventory and
   actual signature evidence. Stop on mismatch or verification failure; classify
   the recorded cause under PKG§7.3 rather than automatically re-sign supplier code.
   This supplies only the observed FP1(b) operation at this experiment's scope.
4. A signed archive must be newly created and re-inventoried. It receives a new
   ZIP hash and replaces the unsigned ZIP only as the subject of a later signed
   experiment; the original remains historical and is never overwritten. The
   current ZIP hash cannot identify changed signed contents.
5. Notarisation is a **separate later account/network act**. CF7 profile name and
   direction remain absent. Accepted CF6 describes a signed DMG; the current
   schema-allowed app_zip does not silently substitute a ZIP notarisation route
   for that design. Select the concrete installer route/bytes and any required
   reviewed route treatment before a submission request. FP3 acceptance, followed
   by stapling/assessment and qualified quarantine/native examination, remains
   unperformed. A successful local signing experiment alone does not establish it.

SIGN-1 Option B reliance still requires applicable FP1(a), FP1(b) and FP3 passes
on the relevant candidate. Physical equality and metadata do not authenticate
supplier acquisition or select a qualification pin. Full package identity must
report actual signing actor/configuration and outcomes, with recorder separate;
it must not be fabricated merely to unblock the static consumer.

OpenAI terms remain unresolved and public distribution not_made. The written
response is needed before public release beyond owner use; it is not a new
barrier to this independent development experiment. LS5/LS8 admission, S4/S3,
verified H3B, FP2/W4, M2/M3, SEAL-2 and release remain separate obligations.
This delta is candidate-bound preparation only; its own independent review follows.
