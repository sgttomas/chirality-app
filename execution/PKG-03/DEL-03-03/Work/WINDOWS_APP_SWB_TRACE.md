# App ↔ SWB: actual producer/consumer trace and missing joins

Source investigation, 2026-10-28; no transport selected, no external dispatch,
supplier/model run, host mutation or Windows execution. This supplements
`ADAPTER_ENABLEMENT_AND_RECEIVING.md` with current implementation standing;
it changes no commitment, receiving allocation or dependency condition.

## Source identity and scope

App basis **`79315c26b104b534a89ed8e9b1e716f3da3440d0`**, isolated App
worktree `/Users/ryan/.t3/worktrees/chirality-app/t3-3d8dd1d5`. All App paths
below are relative to that revision. Peer reads use
`git show 1560bbf7f7add4637a20572a2b0d404ef121af63:<path>` in read-only
`/Users/ryan/.t3/worktrees/chirality/t3-514d37a1`; peer paths below are relative
to its `projects/chirality-piping/`. Latest peer candidate
`b78b0feac0aa1e6bbc4606597e10accc54b7eb51` adds Windows CI/design and release
wording only (four-file diff), not a production transport join. No peer writes,
merge or commitment follow from inspection. Older App handoff notes and
`docs/HOST_INTEGRATION.md` §11 are historical source accounts, not current
integration evidence.

## App: what actually runs and what is only an exercised seam

| Producer → consumer | Exact App paths / binding | Standing and missing join |
|---|---|---|
| React person action → native selected documents | `app/src/App.tsx:2010` invokes `select_external_observation`; registered Tauri command `app/src-tauri/src/lib.rs:1773,2753` calls `runtime_session.rs:614` `receive_external_selection`. | Implemented IPC to native pickers for catalog/read/optional counterpart JSON. No renderer-supplied path or host origin. This is selection of documents, not enabling host dispatch. |
| Selected paths → bound supplied read | `external_observation.rs` `DocumentEvidence::load`, `ExternalObservation::load`; `catalog.rs` `Catalog::receive`/`receive_read`; compiled via `lib.rs`. | Original bytes/document and actual selected native path retained in memory; schema/edition/operation/basis consistency assessed. Snapshot explicitly says `hostOrigin:unverified`, `dispatch:none`, comparison scope supplied documents only. Reported currency is a supplied claim, not observed live SWB currency. |
| Explicitly supplied proposal → injected call boundary | `proposal.rs` `BoundProposal::receive`, `SubmissionCustody`; `external_adapter.rs:25` `Channel::submit(FnOnce(&[u8]) -> Result<Vec<u8>,String>)`. | These two modules are **not declared by production `lib.rs`**. Integration tests `tests/catalog_adapter.rs:82–85` and `tests/swbpipe_receiving.rs:6–12` include them by path. No production Tauri command, socket, MCP client, CLI spawn or SWB receiver is joined to `Channel::submit`. The injected closure is a test seam. |
| Channel claim → dispatch permission check | `external_adapter.rs` `Channel::receive`/`submit`; `resources/catalog_adapter/channel_status.schema.json`; `tests/catalog_adapter.rs:134` disabled/enabled case. | Schema and supplied enablement/configuration/reachability claims checked; disabled submits call nothing. This is not an implemented native host enablement act, listener/access control or verified reachable endpoint. |
| Bound request → result custody | `proposal.rs` `SubmissionCustody::begin/observe/outcome_missing`, `external_adapter.rs` `DispatchAccount::receive_for_proposal`. | In-memory exact request bytes; same identity/different bytes refused; repeated submission refused pending host one-effect mechanism. Missing/malformed result becomes unknown; transport/native success cannot become applied or human acceptance. No production durable outgoing-submission journal or restart reconciliation to a SWB receipt is established by these modules. |
| SWB-mapped fixtures → App receivers | `resources/swbpipe_receiving/`, `tests/swbpipe_receiving.rs`; owning `DEL-03-02/Design/SWBPIPE_CORPUS_RECEIVING.md`. | 84-case illustrative mapping and SH-1 test-double documents. Mapping's peer basis is **`8212c765ec0bcc812ad4c4f7079bc661b55d70ab`**, not today's production pin. Profiles can omit workspace/generation and expose only whole-model identity; they cannot establish a complete citable current host basis. Never call these bytes a live SWB response. |
| Supplier-facing Host → actual owned stock child | `hosting.rs` `Host::start:1367`, `OwnedProcess::spawn:1528`, `request_begin_*:1837`, `spawn_reader:3572`; `process_group_custody.rs`. | Implemented App→Codex JSON-RPC stdio with full generation custody and correlated source requests. Codex `mcpServerStatus/list` or command execution capability does not establish a configured SWB endpoint, selected executable, opt-in grant or durable host effect. No supplier execution occurred here. |
| Selected XT/EXP evidence → trace view | `trace_receiving.rs`, `external_trace.rs`, `lib.rs` native selection and `trace_selection` state. | Memory-only untrusted evidence intake, not a producer of actual external execution or origin verification. Native result selection cannot establish host application, receipt durability or a person's checking/acceptance. |

The actual production read-only App path ends at a **person-supplied document
receiver**. The exercised App submission seam ends at an **injected test
closure**. Neither ends at SWB's live controller. App Host's genuine stdio
transport ends at its selected stock Codex child, with separate identity and
unknown-outcome rules. Similar JSON shapes do not join these paths.

## SWB: actual local service trace at the production pin

| Producer → consumer | Peer paths / binding | What it establishes; what it does not |
|---|---|---|
| SWB editor operation service → native IPC | `apps/desktop/src/services/operationService.ts:57–84` calls `invokeWithIngress("validate_model_operation"/"apply_model_operation", {model,intent,claimedModelHash})`; `nativeIngress.ts:92` encodes UTF-8 JSON and calls `@tauri-apps/api/core.invoke` with `x-swbpipe-ingress:args-json-v1`. | Real **same-App local** Tauri invocation. Its `stillCurrent` hook/refusal retry is request-admission behavior, not an external App endpoint or one-effect remote submission protocol. Browser fallback calls local WASM. |
| Native invocation → validation/application engine | `apps/desktop/src-tauri/src/lib.rs:2243–2291`, registered handlers; `command_ingress::admit` then `validate_operation` / `apply_operation`; core `model_operations/operation_applier`. | Validates/applies supplied model+intent under local ingress/memory and core operation rules, returns operation outcome/model. It does not by itself identify App workflow/run, establish host opt-in external access, select a live workspace or commit a saved project. |
| Local project Save → guarded store transaction | `apps/desktop/src-tauri/src/lib.rs:2724–2775` `save_local_project`, `save_project_in_store`, `guarded_write_project_rows`; request includes `confirmed_revision` and `expected_base`. | Real local persistence with revision guards and transaction commit. Its result is not a receipt for an external App proposal unless an actual host-owned receiving route binds original request identity/basis, operation and durable save. Model application and project-save durability are distinct. File-save APIs have their own uncertainty states (`model_document_save.rs` documents `saved_durability_uncertain`). |
| Headless caller → runner | `core/runner/headless/src/bin/openpipestress-runner.rs:1–11`, `main` and argument handling. | Narrow foreground local JSON CLI, stdin/file input and stdout/explicit file output. This is not a live desktop controller listener, App catalog adapter or a selected App↔SWB transport. No invocation was made. |
| Public API / extension definitions | `api/api_boundary_contract.yaml` `x_contract_metadata`; `docs/architecture/extension_domain_contracts.md:23–36`. | Schema-first draft; transport/endpoint/loader/grant persistence remain TBD. Extensions must use host application-service commands/queries/jobs; no SQL or raw store authority. Definitions do not instantiate a receiver. |

SWB's stale-intent/refused-source tests and save revision guards are valuable
**local** evidence. They cannot establish that a future external submission
cites and rechecks the basis originally read in App, or that retries have one
durable effect. Likewise 929 peer-reported Mac core tests, Windows typechecks
and supplemental native-x64 CI are not Windows App/supplier/native integration
evidence. No shared implementation is selected by this trace.

## Required joins for a later connected App↔SWB journey

These are concrete missing contributions and falsifiable future witness
requirements, not instructions to build external integration in this tranche.

| Join / owner | Required observation before claiming it exists |
|---|---|
| Host-owned catalog/read producer → App receiver (SWB producer; App receiving owner) | Actual deployed source revision, catalog edition and operation version, workspace identity + generation + model revision + canonical content/hash method from the **same** controller the person sees. App binds original bytes/source and refuses missing required basis; opening a fixture cannot attest origin. Distinguish repository/build identity from runtime workspace/model identity. |
| Local opt-in + App configuration → actual channel (host policy/native-act owner; App adapter owner) | External access initially off, actual person's enablement record tied to local host/endpoint and applicable grant; explicit App-side selection; disable/revoke prevents new dispatch. An enabled JSON claim is insufficient. No transport or grant persistence chosen here. |
| Bound App proposal → SWB ingress (both receiving owners, coordinated by Agent 0) | Select a transport only through owning design; bind host/workspace/generation, exact original read basis, proposal/operation identity/version, origin/run/conversation and target content. Same one validation/application route and reserved-act policy; no direct persistence hooks. Current local Tauri invocation is not externally callable by implication. |
| Original basis → stale refusal (SWB) | Mutate/reload workspace after App reads, then submit the frozen proposal; actual host refuses the original basis before effect with reason. Later selection must not retarget. The App must show refusal separately from transport failure and from incomplete citable basis. |
| Submission → durable result/receipt → reopen (SWB effect/dedup/persistence owner; App custody/records owner) | Host durably binds original submission identity/content, application outcome and resulting revision/receipt; repeated identity/same bytes has one effect, conflicting bytes refused. App retains original submission and receipt reference with source standing and reconciles after reopen without inventing human acceptance. Existing in-memory SubmissionCustody and local Save are not this joined protocol. |
| Effect then lost acknowledgment → truthful unknown/reconciliation (both) | Kill/disconnect after possible host effect but before App observes response. App says outcome unknown, does not blindly resend/rebase. Observe by original identity against durable host result. Host not-known is a scoped report, not proof no effect outside its persistence coverage. Native API/CLI exit success alone never applied/accepted/durable. |

Handoff records must keep host receipts by reference and distinguish actual
operation execution, proposal acceptance, engineering approval, marking checked
and professional reliance (`docs/HOST_INTEGRATION.md` V4-HI-11/20…25/30…32/50…52/70…71;
DEL-04-01 ACT). A schema, instruction or historical exchange is not a producer,
and an App record of a supplied claim does not authenticate a SWB receipt.

The next **Windows App milestone remains standalone**: App launch → actual
stock-supplier initialize/initialized and controlled stop → invented fixture
durable reopen → native control, after the platform probe/choice gates in
`../../../PKG-01/DEL-01-02/Design/WINDOWS_PLATFORM_SERVICES.md`. It needs no
external SWB listener or new transport. Agent 0 can carry the above missing
joins to the peer owner without delaying this milestone or committing either
repository to an unselected mechanism.
