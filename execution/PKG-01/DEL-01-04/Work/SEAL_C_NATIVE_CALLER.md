# SEAL-C native prepared-intent caller

Named source implementation `SEAL-C-NATIVE-CALLER-01`, following integrated
PR #77 (`fa04f39a`). Parent authorized this exact join after native-owner
confirmation of no overlapping Rust writes and reuse of the existing original-
window confirmation path. The purpose is to close the missing native caller,
not select a namespace or activate the separately compiled None gate.

## Actual wiring and authority

`seal_c_enrollment.rs` supplies a native-menu-only worker and the confirmation /
key-setup / Quit coordinator. `lib.rs` adds its module and exact menu-event
branch, conditionally inserts **Prepare capture sealing…** next to Quit, and
uses a generic explicit-key-operation refusal notice for Quit. Existing Quit
logic and all `app_quit.rs` production code are unchanged.

`capture_seal_keychain::enrollment_compiled_available()` is a pure compiled
eligibility query: macOS release and KEYCHAIN_SELECTION present. It performs no
publisher validation, namespace read, keychain probe or filesystem lookup. It
is NOT `selected_route()`, which includes invalid publisher routing. With None,
the menu is absent and the request's same gate rejects dispatch before window
lookup, worker creation or provider preparation. Some only makes the action
eligible; real authority is still validated by preparation and consumption.
There is no new renderer command, MCP tool, CLI/path/URL/environment input or
startup enrollment. The existing provider takes no caller path.

The native caller retains the configured `main` Window once at menu dispatch,
before spawning the off-main-thread worker. It requests restore/show/focus only
for that retained original before preparation; failure refuses. A successful
visibility request is not proof of foreground/native presentation. It never selects a focused, first or
replacement window afterward. The native question uses
`native_lifecycle_confirmation::confirm` unchanged, with safe **Leave unchanged**
and explicit **Prepare capture sealing** choices. The statement names the
original prepared location, service/account/group and committed/pending IDs;
bounded-content presentation uses the existing native-statement mechanism.
No secret key bytes are presented or logged.

## One pending question and final admission

A separate process-local RAII question lease prevents duplicate enrollment
questions. It is held through preparation, confirmation and consumption, and released
on cancellation, errors or success before any result notice. A duplicate event is ignored,
not queued or replayed. This gate is not persistent authority and cannot be
restored from a record.

The shared coordinator executes this actual sequence:

1. Refuse if Quit is already open or proceeding. Require the original window to
   pass a main-thread handle check, then prepare the private provider intent.
2. Present that intent's exact preview using the retained original. No key_setup,
   App writer or provider lock is held across the human question. Cancellation
   or presentation/window error drops the intent without consumption.
3. After affirmative choice, acquire the existing `AppState.key_setup` mutex
   with `try_lock`. Contention or unavailable/poisoned admission refuses without
   a provider call; no automatic retry. Check both Quit busy and proceeding.
4. Schedule a read-only main-thread `checked(&original, |_| ())` through the new
   `native_lifecycle_confirmation::revalidate_original` helper. Scheduling,
   handle or channel failure refuses; no replacement or parentless path.
5. Recheck Quit after that main-thread interval. Consume the same non-cloneable
   PreparedSealEnrollment once, retaining key_setup until the actual return.
   The provider performs fresh authority/policy and in-lock root/absence/marker
   joins. A provider refusal is not replaced by a newly prepared intent.

If Quit won before key admission, enrollment refuses. If enrollment holds
key_setup first, existing request_quit's nonblocking acquisition refuses to
proceed until the operation returns. Lock order is unchanged: host key_setup →
provider authority refresh → enrollment lock → continuity lock. No provider path
waits back on the host key mutex. A Quit question may briefly become busy before
its key_setup refusal; the final Quit check conservatively refuses if it observes
that state. This is not permission to settle/exit during the key operation.

The original-window helper establishes availability **at its check**, not an
atomic lifetime lease for all subsequent provider work. Existing blocking
provider lock waits can delay App-initiated Quit; external termination/logout can
still interrupt work and is covered by the provider's durable reservation rules.
No new timeout is interpreted as success. These limits remain explicit.

## Outcomes and attribution

Cancellation records no enrollment result. On success the UI reports only
**Capture sealing check completed for the prepared installation**; internally
this is `ProviderReturnedSuccess`. It does not claim a new key was created,
that no pending recovery occurred, or that a human identity was verified.
On error the actual refusal is presented only through the retained original
window, or logged if that original cannot present; no unowned alert fallback.
Both the key mutex and question lease are released before result presentation. No new durable approval/permission journal or cryptographic
framework is added.

This is an administrative setup request. Accessibility/authorized automation
may operate native controls; no personal-act, native-origin or agent-exclusion
claim follows from the dialog. SEAL-2 remains deferred. The caller does not
import development keys, regenerate missing pending secrets, choose a profile,
change entitlements or enable KEYCHAIN_SELECTION. Ordinary sealing/verification/
rotation keep their no-initial-enrollment behavior.

## Source assurance and remaining witness

`seal_c_enrollment_tests.rs` uses invented one-use intents and injected
presentation/provider returns with the actual question gate, key_setup mutex
and AppQuit state/admission methods. It covers safe cancellation, preparation/
presentation failure, no key lock across confirmation, duplicate events, lock
contention after affirmative, Quit before/during/after the question, decided
Quit, original-window loss, final Quit recheck, enrollment-first exclusion of
Quit, provider stale/error/no-retry and guard release. Existing native-confirmation,
Quit and provider cohorts remain required. The added source CI cohort preserves
all existing filters. These are headless source fixtures, not an AppKit/dialog,
real-keychain or signed-production witness.

Actual namespace/profile/signer admission and the SC-0…SC-6 signed witness remain
separate. The worker is now source-wired, so the prior design's missing-caller
condition is closed **in source**, but None keeps it unavailable. No actual
native menu invocation or SecItem operation is performed by this contribution.
Parent owns integration and reserved activation/signing decisions; the native
owner retains actual dialog/window qualification and its candidate/controller.

Initial source verification: guarded offline/locked serial cohorts passed
13 native enrollment caller tests, 18 existing native-confirmation tests,
19 Quit-related tests and 43 provider tests. The offline preparation tests
passed 11 and CI-selection tests passed 62. Deliverable validation reported zero
errors; read-only comparison of current package producer dependencies against
its receiving profile found no drift, so no generated closure was changed.
These results and independent review/final exact-head CI are retained in the PR.
