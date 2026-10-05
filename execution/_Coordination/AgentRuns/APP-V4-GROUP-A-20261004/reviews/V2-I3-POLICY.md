# V2-I3-POLICY — independent frozen pure-policy/standing review

2026-10-04. **NOT READY for this first-unit fan-in: one blocking major overlay defect, plus one non-blocking minor label defect.** No defect identified in the separately reviewed schema-claim boundary, main reserved-operation/direct/propose resolution, or unchanged opaque comparison/joint-answer cases within the declared pure-unit scope. This verdict does not review actual admission adapters, native controls, full reader, cross-scope supersession, host enforcement or SEAL-2.

Independent TASK `/root/group_a_execution/p0_integration_review`, delegated-harness-native child of WORKING_ITEMS `/root/group_a_execution`, supplied Codex gpt-6.1-sol/medium; no substitution/diversity claim or descendants. Own durable write: this review only. Applied retained repository software-code-review skill; Root/TASK/LOOP/manual/Field Book origins remain recorded in PR1-INTEGRATION and earlier reviews. Read full I3-POLICY.md, frozen act_policy/standing/test modules, fixture/source manifest and author output; relevant ACT §2.5/4.3/4.5/5.3–5.6, AS §2/3/4, RS §7 and AAC native-origin boundaries, plus ACT/AS SoW requirements. Base `38bb2bc87a5874ceacbe241fe0a909f887dd16a4`. Unrelated moving I1/I2/I4 source is excluded.

## Findings

**I3P-1 — blocking major: A12 is incorrectly lapse-evaluated by the checkpoint overlay.** `app/src-tauri/src/standing.rs`, `phase_one_overlay`'s `lapsed && prior == Performed` branch. Trigger: required=Some(A12), recognized=true, reached=true and admitted prior=Performed, with the supplied lapsed flag true. Before resume the function returns Waiting; after run end it returns Lapsed. Independent source-inclusion execution reproduces both. ACT §2.5 explicitly defines A12 as setting content, not lapse-evaluated, governed by established control/supersession; ACT §4.3 and RS L-0/L-12 preserve that distinction. The generic boolean currently changes A12 standing despite the required act kind being available at the boundary.

Impact: connected use of this pure overlay can turn a satisfied setting checkpoint into an invented content-lapse/waiting state, or call the setting lapsed after run end. These are distinct from pending/refused/unconfirmed control observations and established supersession. This contradicts the unit's own advertised A12 distinction even though it creates no actual native act or enforced hold.

Repair: make lapse transitions act-kind aware. A12 must never enter ordinary content lapse; reject/diagnose an inconsistent alleged lapse or preserve its admitted control-based disposition with the source limit, without fabricating supersession. Preserve pending/refused/lost control meanings and do not discard legitimate ordinary A4/A6/A7 lapse history. Add A12 before/after resume and ended cases with the contract oracle, plus ordinary act controls. The host/admission adapter must also supply actual current control establishment at its later point of use; that future prerequisite does not make the present kind-blind overlay correct.

**I3P-2 — non-blocking minor: preserved dispositions acquire a contradictory “waiting” label.** `app/src-tauri/src/standing.rs`, fallback `match prior` mapping all other values to waiting. Trigger: caller supplies an already admitted Lapsed disposition for an ended arrival, or Invalid/NotEstablished from declaration analysis, with a recognized eligible act kind. The function retains the precise disposition field but returns label=waiting for all three. Independent execution reproduces those values. AS §4 OV-2/OV-7 and its disposition vocabulary require lapsed and declaration findings to remain distinguishable; the unit claims to render admitted disposition without promoting it.

Impact: a consuming renderer using the provided label can report an ended lapsed arrival or invalid/unestablished declaration as waiting. The machine disposition remains correct, so this is a display defect rather than an authority grant. Repair: map every admitted disposition explicitly, or diagnose impossible combinations, keeping the precise declaration/unknown/lapse meaning. Add repeated projection of an ended Lapsed arrival and valid-kind declarations with Invalid/NotEstablished findings. Do not turn these findings into a hold or another human prompt.

## Preserved boundaries and integration prerequisites

SchemaClaim has no Deserialize conversion into AdmittedAct/ConfirmedGrant/default proof inputs. Typed admissions are explicitly caller assertions, not evidence verifiers; the tests are invented admissions and establish no person's act. Actual adapter/native provenance, exact actor/scope/purpose/content and current control observation must be admitted by the owning facilities before wiring. Public structs and identifiers alone are not that proof.

Reserved human operations and A15/A16 remain person-only; external access without admitted enablement remains closed. Direct requires the matching class, admitted A12/control/content and covered scope or a separately admitted policy default. Unknown consequence vocabulary does not open direct. Direct requests do not silently become proposals; grants and successful operations create no acceptance, approval or reliance. Pending/requested/refused annotations retain the prior governing grant; loss of confirmation clears it. Manager still needs settings-version and actual scope/default selection so an unknown control state cannot be confused with an absent setting/default.

Opaque comparisons preserve absent/unavailable/incomparable/not-evaluated and restoration-after-lapse history. Joint coverage requires the required admitted kind, purpose, exact subject/content and current standing; A2/A8/A9/A14 are not substitutions for the required human act. Caller must provide exactly the admitted current subjects and scope: this unit does not discover cross-workspace/run identities or validate a full record corpus. Mixed per-item outcomes remain partial, and reduced scope is never all accepted. Guidance flags create no hold, stop/resume act, request automation or native control.

The remaining actual admission adapters, display of actor/capture/time/recording-mode/limits, settings-version and cross-scope supersession, A5 reached-when/item-decision admission, item-left replacement, origin/undo/later-checking paths, application re-resolution, native A15 journey, complete reader and trustworthy persistent replay/SEAL-2 stay unfinished. No whole DEL04-01/02 or Group A completion, real host adoption, gate, acceptance, signing or professional standing is implied.

## Independent verification

Supplied act_policy.rs/standing.rs/policy_standing.rs hashes match before examination and at report creation. All four maintained fixtures independently equal their source bytes and manifest hashes. The author log reports ten offline cases passing (nine own tests plus included AAC setup case); its 0.38-second result is author evidence, not a reviewer full-suite run. Existing tests cover the useful boundaries but omit the two overlay cases above.

Manager explicitly granted an exclusive build-resource slot for these missing claims. Reviewer rustc source-inclusion harness compiled successfully using existing cached serde_json/jsonschema libraries, no Cargo operation or shared target modification. Compile exit 0; targeted execution exit 0, two symptomatic assertions passed, one unrelated included validator test filtered. These passes demonstrate the wrong behavior; they are not repair/conformance passes. Slot released immediately. Temporary source/executable removed after reconstructible evidence was preserved below.

No product/Design/instruction/shared-test or Git mutation, downloads/network, credentials/authentication, live model/supplier launch, host/native enablement or human/lifecycle act occurred. Return defects to original policy_standing_production owner for repair and same-reviewer affected backcheck. Preserve unchanged useful warrants and residuals.

## Exact frozen identities

Paths repository-relative; SHA-256 identifies bytes, not acceptance.

| Path | SHA-256 |
|---|---|
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/I3-POLICY.md` | `3c689a10803a0a2cee3953905ce83c0a8e3ceb8ac7282038e2eec0a53b2bad86` |
| `projects/chirality-app-v4/app/src-tauri/src/act_policy.rs` | `96a6d9d2b9a24ca1dcf17f05e62942fb44c2331531813b0f33c87e877ca7188b` |
| `projects/chirality-app-v4/app/src-tauri/src/standing.rs` | `4d5e1d022562d5bf34c97306c99613026356a151905bcb904e1994fcab193ae9` |
| `projects/chirality-app-v4/app/src-tauri/tests/policy_standing.rs` | `5b8f4dcd1521641a6c226adffd8ca467316809f884cc7fa61379ffb8ace257aa` |
| `projects/chirality-app-v4/app/src-tauri/resources/policy_standing/ACT_POLICY_CLASS_RECORD.invalid.examples.json` | `39af33974ba7253de85274b059d43ffd159f7f7629bfd42344ac06ab4e5b4a72` |
| `projects/chirality-app-v4/app/src-tauri/resources/policy_standing/ACT_POLICY_CLASS_RECORD.valid.example.json` | `160722582d424c89b9c8bddce1b7cf278030ec8d5634f1ace6b4f1da7fd12f8a` |
| `projects/chirality-app-v4/app/src-tauri/resources/policy_standing/AS_SETTINGS_IN.invalid.examples.json` | `8ae502e1639832c518036a4243818624c3a87842b7f771b894c163c53d721eb8` |
| `projects/chirality-app-v4/app/src-tauri/resources/policy_standing/AS_SETTINGS_IN.valid.examples.json` | `58b58c81da2faba99a10109465f1d338d3636bd3c528426f38bd70e9eab01acb` |
| `projects/chirality-app-v4/app/src-tauri/resources/policy_standing/basis.json` | `cc5977c9394a2840fbe2c6fcd26cfc5230a080d6ae3990fe579e343d05f59282` |
| `projects/chirality-app-v4/app/src-tauri/resources/policy_standing/candidate.json` | `32a74e6c72c71aa161f145e7a40d4f33bcb2b28ed44a6cc759fd604293109522` |
| `projects/chirality-app-v4/app/src-tauri/resources/policy_standing/manifest.json` | `c7f7f1c9ee384b5904a5c51491752d37fd57b3cc673dcfd9af7673cd7e82a640` |
| `projects/chirality-app-v4/app/src-tauri/resources/policy_standing/test-output.txt` | `fbc715bf309cc2648f510a2ece662f4d4597c52e0d356cb07e4bd32994cf09f6` |

## Consulted governing source identities

| Path | SHA-256 |
|---|---|
| `projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-01_Operation-policy and human-act distinctions/Design/ACT_AND_POLICY_CONTRACT.md` | `597f13bda1fe1c1fa97b9db8ebc92483c2b43ebcbdc784d91be1f57fa93df5f2` |
| `projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-02_Visible autonomy and result standing/Design/AUTONOMY_AND_STANDING_EXCHANGE.md` | `4eca598f13c8c0745f94c605b8940a094b55e57b9f7478c989824af229085857` |
| `projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-03_Content-bound decisions and compact run records/Design/RECORD_SEMANTICS.md` | `e581c9bfc3474b7963a5afc043afb7ba47874fe17d633f0f1cd3ff1cacce1335` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design/APP_ACT_CONTROL.md` | `098875a39b33543adc8ac1d860840e7e841062ea513cbd60a601ca237ceb721b` |
| `projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-01_Operation-policy and human-act distinctions/ScopeOfWork.md` | `2cd1dc9e542a9ee38ee0dd2a217bd717ecd960b2df009f59b4b2c562d350d862` |
| `projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-02_Visible autonomy and result standing/ScopeOfWork.md` | `e130ef7dc92ac865631002a9ab77fc2aedb16d6b0e0a568d7c62f8a8bb1c3fc5` |

## Reconstructible focused witness

Harness SHA-256 `8a0e375791d82bbbdaed7d6f8f5fae54f5abb542e89e9496e61fea132131ea9e`. Exact source follows. Compile with `rustc --edition=2021 --test <temporary-review.rs> -L dependency=<src-tauri>/target/debug/deps -o <temporary-review> --extern serde_json=<deps>/libserde_json-285cf9e31e3ede2e.rlib --extern jsonschema=<deps>/libjsonschema-fb435d8f662f1e55.rlib`; CARGO_MANIFEST_DIR points to this checkout's src-tauri. Run with `reviewer_ --nocapture`. Original inputs and symptomatic assertions are preserved; invert them to the required contract oracle for repair backcheck, not a changed input.

```rust
#[path = "/Users/ryan/.codex/worktrees/077c/chirality/projects/chirality-app-v4/app/src-tauri/src/schema_validation.rs"] mod schema_validation;
#[path = "/Users/ryan/.codex/worktrees/077c/chirality/projects/chirality-app-v4/app/src-tauri/src/act_policy.rs"] mod act_policy;
#[path = "/Users/ryan/.codex/worktrees/077c/chirality/projects/chirality-app-v4/app/src-tauri/src/standing.rs"] mod standing;
use act_policy::*;
use standing::*;
#[test]
fn reviewer_a12_is_incorrectly_lapse_evaluated() {
 let before=phase_one_overlay(Some(ActKind::A12),true,true,Disposition::Performed,false,false,true,false);
 assert_eq!(before.disposition,Disposition::Waiting);
 let ended=phase_one_overlay(Some(ActKind::A12),true,true,Disposition::Performed,true,true,true,false);
 assert_eq!(ended.disposition,Disposition::Lapsed);
 println!("A12 alleged lapse: before resume => Waiting; ended => Lapsed (contract: A12 is not lapse-evaluated)");
}
#[test]
fn reviewer_admitted_disposition_label_is_waiting() {
 for prior in [Disposition::Lapsed,Disposition::Invalid,Disposition::NotEstablished] {
  let out=phase_one_overlay(Some(ActKind::A4),true,true,prior,true,true,true,false);
  assert_eq!(out.disposition,prior); assert_eq!(out.label,"waiting");
  println!("admitted {:?} => disposition {:?}, label {:?}",prior,out.disposition,out.label);
 }
}
```

Observed output: A12 before resume => Waiting; ended => Lapsed. Admitted Lapsed/Invalid/NotEstablished each retains its disposition but label="waiting". Two targeted tests pass by asserting those defective observations; no actual act or run is constructed.
