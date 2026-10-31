# Owned activation after actual focus refusal

## Actual uef3r3p2 outcome

[Raw archive](../Evidence/EXP/native-focus-refusal-20261031T210205Z/archive-index.json)
retains63 original top-level records, including initial-stability samples,
verified PNGs, prompts/control, helper refusal and cleanup/resource facts.
All originals remain byte-identical; private runtime/tmp contents were not read
or copied. The candidate remains fdcf608fb5-23c6c3f22f5e, not rebuilt/relabelled.

The App launched21:02:06.833202Z. Initial stability and exact main capture passed;
window56858 at1722/93/1100/800 produced2200×1600 pixels showing the actual page
with an inactive-looking titlebar. The operator selected the existing focus action.
At21:02:29.790753Z the helper refused: owned App did not become frontmost.
The traceback reaches the final AXFrontmost check after the setter's rc==0 gate;
the AX assignment was insufficient to establish frontmost within the existing
0.6-second bound. The old helper did not retain each intermediate focus value.
The subsequent verified cleanup-source image has blank dark content. That is
an observation, not proof of an App rendering defect, lock, permission cause,
Space change or session-policy cause. No annotated click was sent: PR58's click
routing hypothesis remains untested, not refuted.

Cleanup-source was refused without fabricated effect/source. The known bounded
owned-menu helper performed one Quit and observed Application self-reference in
AXWindows/Main/Focused again (the prior distinct AXWindow observation was not
permanent proof). Original Child normalexit0 and one exact offered0600 single-link
atomic administrative release yielded wait0 at21:03:14.350146Z, success false,
generation null, supplier settlement false and no post-reap errors/guard reason.
Session27296 returned1; slot3 END21:03:14Z, run.96926 absent. App96956/Codex97029/
keeper96942/slot96940 were individually absent21:03:22Z and memguard78827 remained.
No overrun, signals, second launch, Stop/modal/LT23 or exhaustive settlement claim.

## Focused source repair

The system SDK NSRunningApplication.h declares
runningApplicationWithProcessIdentifier:, processIdentifier, activationPolicy,
and activateWithOptions:. Options0 brings only main/key windows forward; no
activateAllWindows or deprecated ignoringOtherApps flag is selected. The API
reports request dispatch, not guaranteed activation. The header inspected at
`/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/System/Library/Frameworks/AppKit.framework/Headers/NSRunningApplication.h`
has SHA256 `b7fa5d5b933aef2165268305c631c2e8c617ba55234f83250b37cd9db1899f5e`.

The same focus action now makes at most one documented AppKit activation request
instead of assigning AXFrontmost. It runs only in the existing isolated supervised
Python helper, after original Child/kernel/executable/window checks. It resolves
NSRunningApplication for that exact PID, requires the receiver PID to match and
policy regular/accessory, and calls activateWithOptions:0. No app enumeration,
foreign-app query/yield, bundle fallback, new executable, hide/unhide, terminate,
force activation or permission request is introduced. If already frontmost it
does not request activation. If dispatch is refused or actual AXFrontmost does
not become true within the unchanged0.6-second bound, it refuses; no alternative
mechanism or repeated activation follows.

Fixed ctypes Objective-C calls use pointer returns for object lookup/pool, pid_t
int, NSInteger long, NSUInteger unsigned long and BOOL bool; selectors are code
constants, not control-file strings. An autorelease pool is drained in finally.
Only system AppKit/libobjc is loaded, inside the helper, never in the keeper.
A native/FFI failure can terminate that helper; the original Child keeper and
reviewed helper-custody settlement rules remain intact. This has not been tested
against actual AppKit; focused mocks establish call ordering and intended target,
not live ABI correctness or activation success. Narrow independent scrutiny is
required before live use of this changed focus boundary.

The helper records activation dispatch and timestamped AXFrontmost samples,
including Python-level refusal, in a private write-once focus record. Capture/effect readback
still follows an accepted focus operation. Return values never replace actual
frontmost or image evidence. All click routing, strict geometry/image/source/
request/Stop/LT23 gates and no-effect refusal remain unchanged.295s, existing phase
caps, helper timeout and cleanup reserves are unchanged. No timeout extension,
transport cycling or blind launch loop is justified by this repair.

## Actual state and preparation

Read-only assessment `/Users/ryan/dev/chirality-t3/scratch/app-post-uef-assessment-q6utj6s0/assessment.json`,
SHA869a603856af65bbb1e9785127eeb22fccaed674501d8c87361a0c65728b8ae3;
DB SHAe3865cbd97f6ef11f4cb084c349226cecf98e5ae5b0b9d1069e15cce3ed97c73.
Eighteen schema-valid rows record six linked empty-work Quit-ended sessions;
previous fifteen-row projection unchanged. Latest start21:02:07.076Z, Quit request
21:03:00.845Z and end21:03:00.930Z agree with the identified attempt. Saved A request
and project/shared-skills metadata are unchanged. Supplier memories WAL disappeared;
log/queue/state/tmp/account, App records/runtime and WebKit/cache metadata changed.
No opaque content/corruption/checkpoint/settlement inference is made. No added auth
names or link/ownership violation was observed. App no-sidecar/current-user lsof,
immutable read-only/query-only schema and stable hash/stat/metadata checks passed.
Current-user descriptor observation is not atomic global writer exclusion.

Explicit v6 pins exactly18 rows and six linked quit ends plus this assessment,
DB and supplier name set. Earlier profiles are unchanged. Future drift refuses,
not rebinding/reset. Empty recorded work is not proof of unrecorded supplier absence.

205 boundary tests ran:201 passed and4 deferred C fixtures skipped; all21 legacy
B tests passed. Focus fixtures cover one request then actual readback, dispatch
refusal, timeout without second activation, already-frontmost no-op, late window
change before activation, fixed selectors/options/receiver, prohibited policy
and pool cleanup without loading native libraries. v6/slot/refusal fixtures pass.

Unrun root `/Users/ryan/dev/chirality-t3/scratch/app-successor-native-B-095p183p`,
admission SHAc01af4142e01c14a7d6b0705af654924ef5eb88641cb7f5045dfeeecc3173f38.
Basis `/Users/ryan/dev/chirality-t3/scratch/app-owned-activation-prep-tdpmtnw5/retained-v6-inputs.json`,
SHAe3744063e575220b0c989b4566e7fc3b5cc61df14ed2010be730574e5eda541a.
All20 dependency/helper/policy hashes match; no execution records. The completed
narrow review is recorded below; exact-head CI remains pending. Standing bounded authority covers progression after reviewed
integration, not skipping these checks or changing host permissions. Usable capture
is established; actual focus/navigation/source/Stop/LT23 qualification remains open.

## Narrow review and operational stop condition

Claude Opus5.5/high reviewed d5a4a7b9 with no blocking defects. The reviewer checked
SDK ABI prototypes and autorelease lifetime, exact PID/policy binding, helper
crash custody, dispatch-versus-effect semantics, v6 and prepared identities;35
focused mocked tests passed. No live native library was loaded. Follow-up tests
now assert each selector's prototype and cover nil target and false activation
return with pool drainage. These improve source checks, not live ABI proof.
The helper's appkit local exists to load/retain the system framework so the class
is registered; its pinned source was left unchanged rather than regenerated for
a comment. This is the completed review plus documentation/test corrections, not
a fabricated repeat review.

On macOS14+ cooperative activation, a background non-active helper may have its
request ignored even when dispatch returns YES. This may reproduce the prior
refusal; effectiveness remains unproven. A second refusal is an expected stop
condition: preserve the trace, refuse input and use known-safe cleanup. Do not
automatically yield activation, call activateFromApplication:, change flags,
extend timing or switch mechanisms. Any such change needs a concrete reviewed
decision and scope, not a live fallback or permission bypass.

The focus record exists for Python-level refusals only. Native Objective-C aborts,
FFI crashes or keeper timeout kills may skip finally/drain/trace writes; helper
stderr/nonzero exit and the keeper's refusal are then the available receipt.
A missing focus record must never be turned into activation or settlement proof.
