# I3-POLICY — bounded policy and standing producer/consumer unit

TASK `/root/group_a_execution/policy_standing_production`, parent `/root/group_a_execution`; delegated-harness-native descendant; gpt-6.1-sol medium; no descendants. Base `38bb2bc87a5874ceacbe241fe0a909f887dd16a4`, branch `codex/app-v4-group-a-production`. Only new `act_policy.rs`, `standing.rs`, `tests/policy_standing.rs`, `resources/policy_standing/`, and this change record are owned. No Git, Cargo, lib, Design, shared validator, UI, graph, MEMORY, network, supplier or credential writes/execution.

## Produced contract slice

- ACT §2.1–2.6, §4.1/4.3, §5.3–5.6: canonical policy/settings JSON Schema 2020-12 shape validation uses the existing offline declared-ID registry without rewriting. `SchemaClaim` preserves a claim document but has no conversion into admitted act/control/default inputs. Additional duplicate identity and reserved-not-widenable checks preserve the Design prototype's semantic negatives.
- `resolve` is a pure consuming function for the host route at validation and application, not a second host route. Direct scope checks include workspace, object subset and run, and opaque supplied period/consequence tokens. The consequence placeholder cannot establish direct scope. Only a typed admitted A12 bound to setting content and a typed established control observation opens direct. Reserved A4–A7/A10/A12/A13 and person-only A15/A16 remain person-only. Direct requests do not silently become proposals. No operation or grant creates acceptance or reliance.
- AS §3: pending/requested/refused changes annotate the prior governing grant; loss of confirmation clears current authority. The overlay is for one caller-selected class/control slot; it is not a cross-scope supersession engine or a parser of settings versions. Default policy values require separately admitted decision and host adoption inputs, not the existence of a valid example.
- RS §7 L-1…L-13 / AS §4, §8: opaque method+identity comparisons retain absent, unavailable, incomparable and not-evaluated states. Returning to bound content after an observed lapse keeps that history visible and does not silently restore checkpoint satisfaction. Current per-subject standing can join actual admitted acts over unchanged and newly checked subjects; A9/A14/A8/A2 never satisfy the human act. A12 checkpoint satisfaction additionally requires control establishment and is not lapse evaluated.
- Phase-1 overlay preserves declaration findings, unknowns, not-reached, negative, waiting and performed observations. Before resume a performed act's lapse returns to waiting; after resume it is an act-lapsed annotation without a new hold; after end performed becomes lapsed. A waiting ended run stays waiting. There is no stop/resume implementation, hold support, automation request, new human prompt or native act manufacture. `governed` is a visible declaration flag with guidance semantics.
- Mixed items keep accepted/rejected/queued/left/unknown independently; a performed reduced subject is never all accepted. Standing facets remain separately attributed rather than becoming a combined professional label.

## Evidence and exact checks

Final command, repo-root working directory:

```sh
CARGO_HOME=/tmp/chirality-app-v4-group-a-cargo-home cargo test --offline --locked --manifest-path projects/chirality-app-v4/app/src-tauri/Cargo.toml --test policy_standing
```

Exit 0: **10 passed, 0 failed** (nine own tests and one imported shared-validator test). rustc 1.92.0 (`ded5c06cf`), cargo 1.92.0 (`344c4567c`). Manager granted then received release of the shared Cargo slot. Initial invocation from repo root without `--manifest-path` refused with missing Cargo.toml; subsequent command was corrected. Initial seven-test run passed; final result above covers added grant-history/identity-restoration/A12 checks. No full-suite/native/supplier witness is claimed.

Canonical combined stdout/stderr: `app/src-tauri/resources/policy_standing/test-output.txt`; source hashes and actual consultation limits: `basis.json`; four byte-identical source-mapped maintained fixtures: `manifest.json`; frozen owned candidate SHA-256s: `candidate.json`, all in that same resource directory. Independent Python comparison confirmed all four maintained fixtures equal their current Design sources and recorded SHA-256s. The JSON examples and synthetic typed admissions remain fixtures; no person performed these acts. Runtime uses canonical maintained schemas, not dated run assets.

Frozen source hashes:

- act_policy.rs: `96a6d9d2b9a24ca1dcf17f05e62942fb44c2331531813b0f33c87e877ca7188b`
- standing.rs: `4d5e1d022562d5bf34c97306c99613026356a151905bcb904e1994fcab193ae9`
- tests/policy_standing.rs: `5b8f4dcd1521641a6c226adffd8ca467316809f884cc7fa61379ffb8ace257aa`

## Integration needs and retained obligations

Manager owns module exports in lib and invocation from actual admitted route/record-out consumers. `AdmittedAct`, `ConfirmedGrant`, `AdmittedDefault`, `StandingAct` are **explicit caller admission assertions**, deliberately not Deserialize types, not evidence verifiers, not record readers, and not constructors of proof from writable files. The caller must supply actual capture admission, authority/source limits, exact subject scope and current standing, purpose, and established control observation; identifiers alone never suffice. `phase_one_overlay` consumes the caller's admitted prior disposition and merely renders it; it must never be called to promote a schema claim to performed. `StandingFacets` is a data carrier, not a renderer or reader validation pass.

Before connected use, owner modules still need admission adapters, exact actor/capture provenance and timestamp/recording-mode/evidence-limit display, settings-version comparison, cross-scope established supersession, proposal item-decision admission, A5 reached-when validation, item-left replacement handling at the next arrival, operation origin/undo/later-checking paths, and host application re-resolution. This unit does not complete DEL04-01/02 or their whole OUT/AC obligations. Later I3 units retain native A15 control integration, full record reader and custody-proof cold replay. SEAL-2 selection is pending human decision; no sealing, trusted persisted replay, host construction, host adoption, acceptance, gate or professional claim is supplied here. Independent review is required before fan-in; this TASK remains the repair owner.

2026-10-05 independent successor review V2-I3-POLICY-R1 is READY for bounded fan-in; both findings closed. Consumer must expose optional evidence_limit. Manager moved retrospective review_history bytes unchanged to this run evidence/I3-policy-review-history; original path references remain historical. Maintained source fixtures, module and test bytes are unchanged. Actual admission/current control/full reader/cross-scope/SEAL-2 are still unfinished.
