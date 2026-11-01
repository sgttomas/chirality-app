# Package/S4 -> EXP -> SQ receiving v1

The usable current path is explicit: packaging's `packaged-s4-binding/1` and
`static-package-input/2` evidence are checked by its authoritative successor
validator, then joined to existing EXP-v0.2 results and an SQ-v0.2 dossier.
This is selected-evidence consistency with synthetic regression coverage, not
an actual package/installer/native witness or a release decision.

## Interface and identity

`app/examination/package_receiving/adapter.py` consumes packaging's maintained
`check(request_path, evidence_root=..., trusted_publisher_sha256=...)` API.
No scanner, tree measurement, supplier or native operation runs. All nested
artifact references use one explicit evidence root. The validator's exact
source closure comes from its maintained `source_dependencies()` function and
is pinned in `sources.package-v1.json`, not taken from caller evidence.

EXP `subject.app_candidate.package_record` and SQ `candidate.package_record`
cite the OUTER wrapper `record_id`. The producer report independently joins
`candidate.package_record_id` to the INNER static legacy record. These identities
must differ as well as remain semantically distinct; equal strings refuse so
inner-record citations cannot masquerade as wrapper citations. The receiver
neither derives one from the other nor translates
S4 bytes into the S1 `verification_artifact` slot or into PKG-v0.2.

The separate `exp-package-witness-binding/1` sidecar binds exact wrapper bytes,
wrapper identity, candidate tuple, receiving-code/source-profile identity,
configuration digest, original EXP support tuple/declaration and current terms
documentary selection. It is a receiving declaration, not proof of actual
producer use or a published new EXP/package schema. Existing canonical bindings
for EXP results/reviews/changes and legacy packages are unchanged.

Publisher trust comes from an independently selected configuration file and its
separately supplied digest:

```json
{"format":"exp-package-receiving-config/1","trusted_publisher_sha256":null}
```

The field may be null (reported missing trust) or the exact independently chosen
publisher-binding digest. The request cannot choose that digest for the reader.
Synthetic tests supply an invented trust configuration explicitly; no actual
publisher or owner act is inferred. Changing configuration requires new explicit
selection and sidecar correspondence. A matching digest establishes consistency,
not authentication, signing authority or live-start permission.

## Direct EXP use

From `app/`, with prepared Python dependencies and a scratch Codex home:

```sh
python3 examination/package_receiving/adapter.py bind \
  --request PACKET/binding.json --evidence-root PACKET \
  --configuration CONFIG.json --configuration-sha256 SELECTED_CONFIG_SHA
python3 examination/package_receiving/adapter.py package-link \
  --request PACKET/binding.json --evidence-root PACKET \
  --configuration CONFIG.json --configuration-sha256 SELECTED_CONFIG_SHA \
  --result RESULT.json --revision SELECTED_REV --build SELECTED_BUILD \
  --pin SELECTED_CODEX_PIN --package-ref OUTER_WRAPPER_RECORD_ID
```

The link preserves original EXP result-schema/rule checks, candidate/native-
packaged route, packaged subject, exact revision/build/Codex pin, full EXP support
identity, current currency and wrapper citation. Producer errors are errors;
producer missing inputs and a linked non-pass native result remain gaps. Reported
static/FP/S4 values never establish an actual native run. Reports retain false
qualification, release and live-authority flags and the producer's limits.

## SQ use and strict closure

The additive `sq_receiving/receive_packages.py` selects
`sq-exp-receiving-selection.package-s4.v1` with the existing closed selection
fields plus `package_source_profile_sha256` and `configuration_sha256`.
`package_witness` is a new explicit artifact kind with exact record/binding refs;
`packages` still maps each cited outer wrapper to its result slots. Configuration
path/digest are separate command-line arguments, never selected by the packet.

```sh
python3 examination/sq_receiving/receive_packages.py PACKET/sq-selection.json \
  --selection-sha256 SELECTED_SELECTION_SHA \
  --configuration CONFIG.json --configuration-sha256 SELECTED_CONFIG_SHA
```

The original SQ result, review, evidence-set, scenario, candidate, change-impact,
reopening/history and completeness joins remain in the successor worker. Legacy
package artifacts retain the original validator and conditional package-link.
The report names each package's selected route and whether S4 witness evidence
was selected. Legacy completeness never claims an S4 check. New witness
artifacts invoke packaging's validator and preserve errors/missing
through the final SQ report. Missing cited packages, unreferenced artifacts,
duplicate identities, mismatched candidates/configuration/profiles and mixed
sidecars refuse. The successor is explicitly current-purpose; historical
correspondence continues through the original reader unchanged.

The worker captures existing historical EXP/SQ sources as before. Packaging's
maintained Work closure is staged in a SEPARATE private source root, so an
historical Design directory cannot redirect its resolver to an incomplete
layout. Its imports/schemas read only that captured closure; no ambient-repo
fallback is allowed. Evidence remains under the separately selected packet root.

Exit 0 means complete selected consistency, not qualification. Errors, missing
or unsupported joins remain nonzero. Existing external/native evidence references
remain visible; selected coverage never authenticates review independence,
human acts, signatures, custody, signing/notary/installation or release.

## Generation, compatibility and remaining release evidence

Run `python3 app/examination/package_receiving/generate.py` from repository root
after integrating a changed producer/checker head. It derives the package profile,
new SQ source pins and reader constants, and refuses collisions with the original
SQ source selection. It does not refresh old terms, standalone, admission,
canonical, distribution or terminal cohorts. Never hand-merge generated pins.
`app/tests/package_successor_receiving_fixtures.py` composes packaging's maintained
synthetic generator with the existing SQ fixtures and maintained aggregation
rule; original fixture/evidence bytes are not rewritten.

DEL-09-01/DEL-09-02 ScopeOfWork and dependency requirements were reconciled by
inspection and remain unchanged. The new Work accounts and code/check declarations
identify the implemented receiving path. In particular the full-document current-
admission Scope/protocol subjects are not changed to force a repin.

Real release evidence still requires the selected publisher/owner inputs,
identified actual signed/notarized package and installer, full actual inventories,
applicable installed S4/native/FP observations and joined candidate results,
independent examination and the owner's separate release/replacement decision.
No fixture pass supplies those acts or artifacts. Unrelated known terminal/S4
historical-source conditions are not swept into this adoption.

## Downstream native journey readiness (2026-11-01)

Inspected against integrated main `e5a18920574ed56a8e4bf57f78566d7dab7ccfd8`.
This receiving update uses the existing EXP/SQ contracts and reader selection;
it changes no criterion, source profile, fixture, protocol or bound Scope bytes.
DEL-09-01's existing dependency conditions and code/check declarations still
apply. Native DEL-09-02 owns execution and its controller; this lane performs
only offline receiving checks and reconciles supplied evidence.

### Received subjects and limits

- PR65's committed input-test evidence under DEL-01-06
  `Work/unsigned-release-input-build/12d26b8db5-278899dad62e/` binds source
  `12d26b8db5f251be97d83d4f574196697df40a70`, bundle tree
  `278899dad62ebbc6dd701490f71b20bd04e1329bca4dbefbd5d88eecd83e31f0`, and
  executable P0 `1b3c6c2ec345845122322134cd6f9b59e60d32c78ef0795a5e2b4e5cf26796b8`.
  Its records report 3,504 source-export files, 50 resource mappings/full
  Resources correspondence, version 4.0.0/minimum macOS 15.0. Receiving checked
  the committed plan/observation/inventory/load-command digest joins; it did not
  remeasure or launch the retained bundle. Publisher binding/projection hashes
  describe `null\n`, with compiled values `None`. These are unavailable publisher
  inputs, never real typed packet bindings. This release-profile input build
  is not a debug-v3 candidate-identification record or installed S4 witness.
- The attended candidate is separately `1f67d3822b-8c83d74ae3ce`, source
  `1f67d3822b685c9c0d0ac4d52b0e52a570ef3d52`, tree
  `8c83d74ae3ce1ea0116234ff654f1db23ebb6ccc760d05c1af66c325b19039b1`.
  [Native preparation](../../../DEL-09-02/Work/POST_I_BOW2KD_RETAINED_SHELL.md)
  binds controller `8b2569d5`, root `app-attended-prepared-j58087z7`, manifest
  `6a2e17f393912a4150bac88dc59fe000ba872cd7a42ec662e6995697254ef252`.
  The document's **unrun** status is historical preparation standing: parent
  subsequently reported this root consumed, failed initial focus after
  capture/parser progress, owner normal Quit, normal exit 0/admin wait 0,
  56.973 s/no overrun. No setup, B, Stop or LT23. This paragraph records that
  supplied report, not independent raw-run validation or a completed EXP result.
  Preserve the original result/closure receipts with the native owner; do not
  rearm that root or relabel this candidate to current main.
- Earlier `fdcf608fb5-23c6c3f22f5e` setup and failed B observations retain their
  actual candidate/source. They do not qualify the later attended or release
  input builds. PR68 parenting and PR70/73/74 controller changes are source
  preparation; PR69 recovery backend is integrated but inactive.

Original App Child exit/reap and released controller resources are
**administrative closure**, not supplier settlement. The
[native terminal route](../../../DEL-09-02/Work/NATIVE_TERMINAL_RECEIPT_ROUTE.md)
requires the observed full generation `{appSession, home, spawnCounter}`,
source-bound stopped/tree-ended/LT23, actual exit facts and original process-
group descendant check, retaining unknowns and detached-descendant limits.
An installed issuer/terminal publication additionally needs its actual same-source
LT09/S4/custody/store joins. Neither AX text nor EOF, wait 0, expected home paths,
static package consistency or an invented combination of session fields supplies
that publication. No actual terminal packet has been admitted here. The
[historical LT09/LT23 disposition](../HISTORICAL_DISTRIBUTION_TERMINAL_DISPOSITION.md)
retires synthetic cohorts from current release reliance, preserving their tests,
guards and bytes; actual lifecycle/cleanup remains owed.

### Executable coverage and next action

These are existing executable checks, not a new qualification framework:

| Seam | Existing executable coverage | What it cannot establish |
|---|---|---|
| Create/try/review/register/reuse/refine | Rust `workflow_journey_tests.rs::journey_select_register_run_check_end_and_reopen_after_process_loss`, `workflow_trials_tests.rs`; React `workflow-drafts`, `trials`, `registration-review`, `workflow-selection` tests | Fixture Python supplier and synthetic A15, not a model/tool witness or person's registration; Root APIs are below some command/native-dialog guards |
| Interruption/restart | Journey test retains publication/run records across dropped sessions; `run_restart_tests.rs`, `hosting_recovery_reads_tests.rs`; mounted `clean-trial-restart`, `recovery-custody`, `history-continue-navigation` tests consume source DTOs | Simulated process loss/fixture requests are not actual App relaunch, waiting tool request, personal Quit or exhaustive child settlement |
| Three access modes | `access.rs` selection/home/generation refusals, `access_provider_tests.rs` private config/fresh Start refusals; mounted `access-provider` tests preserve source/home/choice | No complete credentialed M12-1…6 witness. Three configured entries, a canary loopback fixture or an anonymous local provider cannot substitute for three working modes |
| Downstream receiving | `group_b_standalone_test`, `group_b_pre_run_inputs_test`, `group_b_native_forms_test`, `group_b_sq_receiving_test`, `group_b_package_successor_test` | Preparation and evidence consistency only; never authenticates a person's act, signing or native outcome |

Rust/React source above was inspected, not re-executed in this lane; some Node
suites launch Cargo fixture producers, so they are not silently treated as pure
presentation checks. Native final checks keep priority. The focused Python
results below exercise the actual preparation/form/receiving paths without an
App, supplier, native library, model or scanner. No missing offline join has yet
required a new adapter or fixture cohort.

The smallest missing join is **actual case input and evidence**, not a new
source lock: the maintained pre-run helper intentionally leaves the candidate,
configuration, record IDs, observations and outcomes unassigned. Bind an actual
examiner-declared case definition and its inputs before a journey; do not edit
or repin the generated blank preparation into an executed dossier. Changed real
draft bytes need their own exact case binding, not substitution into the fixed
13-role example selection. Completed evidence uses EXP results/SQ dossier and
explicit canonical sidecars; `check-blank` is not a completed-form validator.

1. **Native owner first:** fix and demonstrate the initial attended path on its
   exact candidate/controller/state admission; obtain actual setup/save and B
   source/generation facts, and the scoped cancel/readback/closure observations
   assigned to that attempt. A/B incarnations here are not SQ RUN-A/RUN-B.
   Neither successful entry nor cancellation passes a workflow scenario or
   confirms Stop. Do not infer permission for a new run from this account.
2. **Before SQ RUN-A:** integration owner resolves SQ U-SQ-3/I-6: development
   build or installed package, with the actual candidate/build/Codex pin,
   runtime configuration, native route/tool check and examiner. Development
   observations remain `native_development`; they cannot qualify a later signed
   subject. U-SQ-3's conditional SEAL-2 capture limit must be recorded if applicable,
   not treated as SEAL-2 implementation or activation (it remains deferred).
   Record the actual selected seal/capture standing and limits. Examiner freezes
   the case definition, new-input/collision bytes, ST-4 delegation route and
   ST-5 actual candidate-pin capture/replay requirements. J-1 starts empty;
   maintained fixtures are examples, not preinstalled/registered workflows.
3. **V4-EXM-10 with V4-EXM-11 inside the same RUN-A:** plan/tool work and delegated
   child J-1/2; draft/try J-3/4; collision review J-5; ST-3 unperformed-act negatives
   then actual person's A15 J-6; reuse J-7; two tried/reviewed/registered refinements
   J-8/9, repeating ST-3 negatives at J-8 before registration, while revision 1
   remains unchanged (ST-1). Keep J-8R/J-9R recorded but
   uncounted. Insert S11-1 interruption while the J-2 child is active, S11-2…4
   close/reopen/deny/grant at actual J-7 requests, S11-5 quit with live J-8 trial
   and waiting request, then S11-6 admitted continuation and truthful recovery.
   No request means blocked, not pass; continuation is not recovery of the whole
   undertaking. ST-1…3 have no replay replacement; preserve required ST-4/5
   counterparts and unknowns. N-2 automation does not become a person's A15.
4. **V4-EXM-12, SQ RUN-B on the same candidate:** the person performs actual
   sign-in in H-acct and key entry in distinct H-key, with the owner present for
   credential use under repository controls; select identified local endpoint/
   model, retain explicit no-default choice, then three distinct conversations
   with all modes remaining selectable and credential-custody checks. Missing
   credential/server input remains awaiting input; no substitute-mode pass or
   new auth/download act is authorized by preparation.
5. **Package/release:** recovered team `8A7JL35U4S` is not a selected publisher;
   proposed `com.chirality.app.v4` awaits owner selection. Packaging receives the
   private publisher selection/digest, freezes the actual production subject and
   emits original/public binding plus App inventory. Runtime/packaging settle
   SEAL-C namespace/entitlement/profile/enrollment inputs before owner signing,
   notarization/stapling, pre/post installer bytes and installed quarantined
   S4/full-generation/native witness. Use the existing wrapper and independent
   configuration, preserving missing/null/error standing. Finally join actual
   candidate results and independent review for the owner's release/replacement
   decisions. Development-build SQ results retain only their original candidate;
   a different signed release subject requires applicable package-native results
   or an explicit outstanding limitation for the owner's decision, never silent
   transfer of qualification. Resolve U-SQ-3 before execution; this ordering does
   not force a development-first run. Separate source-applicable SWBPIPE reference-system/Apply/lifecycle
   witness and criterion 17 remain required; catalog source tests are not it.

### Verification of this reconciliation

At the inspected main basis, 89 focused Python tests passed: standalone 12,
connected pre-run inputs/forms 12, and native forms/SQ/package receiving 65.
They include exact-source/fixture tamper, completed-form refusal, missing terms/
S4/trust, rehashed null/generation contradictions, native failure propagation
and isolated closure replay. No skipped failure, new cohort or current pin
renewal was used. The broad manual suite, Rust/React suites and actual native/
signed/host journeys were not run here. The two historical distribution guard
drifts remain exactly as recorded in the linked disposition.

Bounded independent Claude Opus5.5/high review of `1131aa9b` found no blockers.
Manager repairs make U-SQ-3's pre-run subject choice, repeated J-8 ST-3 negatives,
the person's credential-entry role and retained predecessor/native histories
explicit. Review did not rerun tests or validate the private j580 observations.
CI's historical stale-`hosting.rs` wording was reported to Agent 0 for a separate
text correction; CI selection and guards remain unchanged here.
