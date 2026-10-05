# I5 examination-account consuming join — refined 2026-10-05

TASK `/root/group_a_execution/catalog_adapter_production`, parent `/root/group_a_execution`; native delegated descendant, no delegation. This record is the only write. Shared lib/App/runtime_session and reviewed external_trace remain frozen. No Cargo, native operation, model, network/auth, Git or schema change.

## Actual receiving path

`lib.rs::select_external_observation` takes no renderer path/origin: native dialogs pick catalog/read/optional counterpart. `runtime_session::receive_external_selection` retains prior custody on cancel/failure, calls ExternalObservation::load once, stores memory-only custody, and exposes it through host_status. App.tsx ExternalObservationPanel displays complete original documents/bytes, tagged native path identity separately from lossy display, and explicit limits. This is implemented source, not an operated native selector witness. The stages are C-specific and cannot admit XT/EXP records as catalog operations.

## Required source basis versus available App facts

The current developed schemas/protocol require the following; shape admission never authenticates the source's declarations.

| Field and clause | Required supplied content | Current App source / limit |
|---|---|---|
| XT result subject, X-R1 / XC-00 / §3.4 | Joined subject: app_candidate, host_candidate, identification_record; rehearsal: double identity/source/file digests; definition: definition_label | No real XC-00 host/App joined identification in this entry. Supplier versionIdentity is not App/host candidate identity. Preserve source subject kind. |
| EXP run_basis / subject, EXP-R2/R3 / §4.1 | Candidate: revision and build_identity; packaged=true additionally package_record. Double: identity/file digests. Definition: version_label. | No immutable executing-App revision/build/package identity producer in this entry. Do not invent a build hash or treat a supplied revision as verified executable identity. |
| XT configuration, §3.4 | realization_family and native_path; optional endpoint/profile/model_destination (requested/effective or explicit not_observed) | No external host family/path/endpoint is actually selected here. Do not derive N-MCP/N-CLI from ordinary Codex events. |
| EXP configuration, EXP-R2 / §4.1 | codex_pin and route; candidate also model/model_server. Model/server allow explicit not_observed/not_applicable. Codex pin allows a version or not_applicable, not an omitted/guessed value. Native routes additionally platform/native_route/WKWebView; packaged non-not-run additionally package record. | host_status can expose versionIdentity/supplierStanding when observed and accessSelection/thread requested/reported model/provider facts. These describe the supplier/session, not an imported examination's settings or native witness. No current examination WKWebView/package/runner evidence is supplied by this path. |
| Date, XT §3.4; EXP §4.1/schema | XT date string; EXP {value, source}, with source observed_clock / record_timestamp / stated_by_person | Person-stated date is explicitly permitted by EXP. Preserve the imported run date/source. Receipt clock, if collected, is separate and never fills or replaces run date. |
| EXP case/criterion/support/evidence, §4.1 and §3.4 | Case/owner, criterion source/text identity, support revision, outcome/parts, provenance and currency | Carry these from original selected bytes. Native file selection proves no criterion was evaluated, human act occurred, source review was independent, or reported pass applies to this executable. |

## Minimal truthful explicit person-supplied basis

Refinement: the earlier proposed internal verified-executable binding is needed for an actual current candidate examination, but must not block **read-only import of a supplied result**. Use a complete existing XT/EXP record selected by the person as the source basis, without introducing a new basis schema or manufacturing a result. EXP explicitly permits person-stated date; its declared candidate/configuration are source claims. Label the bound basis `person-supplied examination record; executable/host/native observation not verified`.

For the first bound intake, select candidate-bearing EXP or XT records. Extract the full declared subject, configuration and date with their exact field meanings from that same retained byte buffer. Keep the EXP revision/build tuple intact; a revision string used as the existing TraceAccount routing key is not the whole candidate identity. Keep each import's account isolated: do not merge a same-revision/different-build source into an existing account. XT's exact app_candidate string remains its source key. Origin is native-selected input custody/source reference, not an invented examination producer or person-act identity. Use the original record_id when present as a source-record reference, not proof of its author.

Definition/rehearsal records retain their actual non-candidate subject. If an explicit candidate-bearing account basis is absent, or required candidate/config/date fields are missing, retain unbound raw bytes/parsed claims and the precise missing/refusal reason. Never mint a fake candidate or convert their run_basis to candidate. Existing I5 definition/rehearsal helper checks remain local evidence. Current executing-App candidate identification stays separately not-established until its actual producer is supplied.

## Exact released shared entry and recipient

Sole owner adds `select_examination_record(app, state, record_kind: String, evidence_kind: String) -> Result<Value,String>`. IPC supplies only bounded record-format and **declared evidence-category** choices; native Rust selection supplies the local path. No renderer path, trusted-source flag or verified-candidate argument. Read once, retain tagged native path identity/display limit and exact bytes, and parse solely as untrusted data.

Internal `supplied_examination_basis(record: &Value, source: &SelectedInput) -> Result<SuppliedExaminationBasis, BindingNotSupplied>` extracts the source basis above; it does not claim current executable verification. With a complete supplied basis, call frozen TraceAccount::new / receive using SuppliedRecord's source candidate key, input-custody origin/reference, explicit category/kind and unchanged bytes. Keep full source subject/config/date and `basisStanding` alongside the account snapshot. Existing canonical schema and semantic checks decide record refusal; absence of basis keeps raw input unbound. Classification stays a supplied claim: an import does not certify native_supplier/actual_host, and existing join gates remain false.

Add one memory-only AppState session and host_status.examinationAccount; selection cancel/failure retains the prior account. Render complete original documents/bytes, source basis, raw refusal, unknown/not-supplied limits and false joined counts. Import observation time/current supplier facts may be separately displayed with their real sources; never substitute them for the original examination configuration/date. No result is authored from this import, no current executable pass or human act is recorded, and payload text is never instructions.

## Focused connected oracles

Exercise actual released native-selector callback → single byte read → supplied-basis extraction → TraceAccount → later host_status/UI. Check a complete person-supplied candidate record (including stated_by_person date) without executable/native verification; missing basis retaining raw bytes; cancelled selection retaining prior account; same revision/different build not merged; source file replacement not retargeting; source configuration/date not overwritten by receipt/current supplier facts. Carry the unchanged canonical controls and exact EXP-EX-08 applicability overlap mutant through this path, with refusal/raw evidence and no joined promotion. These are own-code receiving checks; actual native selection/examination proof remains a separate witness.

EXP §3.1/EXP-R1, §3.2/EXP-R2/R3, §3.4 and §4.1; XT §3.4 X-R1…5 and §5 control this intake. V4-EXM-24/25 stay uncounted, OI-003 unresolved, DECISION-3 joins deferred. No human checkpoint is needed to receive the expressly selected untrusted record; a real examination, OI-003 ruling or host act retains its own authority.

## Consulted origins

- `projects/chirality-app-v4/app/src-tauri/src/lib.rs` sha256 `4ab7de274ac32b661d1af1c540a30680c699597e22da07bca700fa5a3b79a989`
- `projects/chirality-app-v4/app/src-tauri/src/runtime_session.rs` sha256 `ed2e61b60828a2cd39510e919cc00bff733185e68120fa5726684ae11a940601`
- `projects/chirality-app-v4/app/src/App.tsx` sha256 `316cd7b31c5d8b8857380779a02936e766c71374eebb12d406baebca2f4e1d4a`
- `projects/chirality-app-v4/app/src-tauri/src/external_trace.rs` sha256 `22d9ad6b3fa7d8efe1156cb4c77e6e0def94b744ecef41b7ecfe4734b776f407`
- `projects/chirality-app-v4/app/src-tauri/src/access.rs` sha256 `8a8036429f23f095ce6f13110fdcc6a0d93e1e3a20cd0720bfd69e24e7ace32d`
- `projects/chirality-app-v4/app/src-tauri/src/hosting.rs` sha256 `fe3d797cff2cc2bd89b41673052fa0cd6012ab1e24b8ad11b5c2ad5895075315`
- `projects/chirality-app-v4/app/src-tauri/resources/external_trace/xt-result-record.schema.json` sha256 `3b0ff2bbd1da8dab61147218b6c512146b58b4dc13eea6a2b1c60f7c5b697b4b`
- `projects/chirality-app-v4/app/src-tauri/resources/external_trace/exam.result-record.schema.json` sha256 `f7871c96cef25bb974aea73feca009ed3caf843db5077d80612f13b130af2081`
