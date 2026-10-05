# Stock userVerification route follow-up

2026-10-05. Bounded TASK `/root/stock_verification_followup`, parent HELP_HUMAN `/root`; delegated-harness-native descendant, no delegation. Source investigation only on official `openai/codex` `rust-v0.160.0`. Sole write: this report. No supplier execution, native/device/status call, authentication, enrollment, keys, proofs, model turns, installs, archive/package/binary download, source vendoring, external-session message or Git mutation. Public text was inspected through web retrieval in memory. A shell public-text read failed DNS before returning bytes.

## Answer and new evidence

**The primitives do not implement backend credential registration or verifier binding.** Their service dispatches local readiness/key/signing operations; its enrollment branch returns public metadata and explicitly leaves registration to the trusted caller. This is affirmative implementation evidence, beyond the prior packet's inaccessible-path gap. [Stock service](https://raw.githubusercontent.com/openai/codex/rust-v0.160.0/codex-rs/app-server/src/user_verification.rs).

**A truthful third-party local client can invoke the documented primitives independently of automatic advertisement, at the source-admission level.** The RPC dispatch checks initialization and experimental opt-in. The native service receives origin, account/cancellation guards and operation; no client-name or advertised-extension eligibility is passed into that admission path. This does not establish successful hardware use on this candidate. [RPC handler](https://raw.githubusercontent.com/openai/codex/refs/tags/rust-v0.160.0/codex-rs/app-server/src/message_processor.rs).

**That independence does not provide a third-party hosted elicitation route.** Outgoing `UserVerification` requests select an owner from the eligible connection set and return without sending when no owner exists. This gate is distinct from direct local RPC admission. [Outgoing routing](https://raw.githubusercontent.com/openai/codex/rust-v0.160.0/codex-rs/app-server/src/outgoing_message.rs).

## Trace and exact inspection basis

All URLs below are official source under the named tag. Remote `L` ranges are zero-based browser-extracted lines, not GitHub source-file anchors. Local schema line numbers are one-based. No remote bytes were vendored or hashed. The [release page](https://github.com/openai/codex/releases/tag/rust-v0.160.0) links tag `rust-v0.160.0` to [commit a956835d020762cb2b570053af06f643a11c0ecc](https://github.com/openai/codex/commit/a956835d020762cb2b570053af06f643a11c0ecc). Sources were fetched by tag URLs; a commit-addressed byte comparison was not performed.

| Source-qualified path and inspected ranges | Checked fact |
| --- | --- |
| Local `app/src-tauri/resources/supplier/0.160.0/codex_app_server_protocol.schemas.json`, L262–372, L30784–30856, L30960–31085 | Five typed requests exist. Enrollment response describes caller-owned backend completion; proof is challenge signature consumed by the verifier. Schema presence alone proves no implementation/admission. |
| [codex-rs/app-server-protocol/src/protocol/common.rs](https://raw.githubusercontent.com/openai/codex/refs/tags/rust-v0.160.0/codex-rs/app-server-protocol/src/protocol/common.rs), extracted L469–513 | All five methods registered as experimental with `serialization: None`; no identity predicate in these registrations. |
| [codex-rs/app-server/src/message_processor.rs](https://raw.githubusercontent.com/openai/codex/refs/tags/rust-v0.160.0/codex-rs/app-server/src/message_processor.rs), L605–738, L926–1085 | Request context registers before dispatch; initialized/experimental gates precede handler. Cancel signals the same-connection ID and acknowledges. Status/enroll/delete/verify call `Service.handle(operation, rpc_gate, cancellation, origin)`, then send a checked response. These branches impose no first-party name or pending-elicitation requirement. |
| [codex-rs/app-server/src/user_verification.rs](https://raw.githubusercontent.com/openai/codex/rust-v0.160.0/codex-rs/app-server/src/user_verification.rs), all 263 extracted lines; especially L50–124, L140–238 | WebSocket/remote-control operations except status are rejected. Identity comes from cached ChatGPT account-user ID; build support is required. Guards cover connection, cancellation and auth revision/identity. A bounded worker calls provider status/ensure_key/delete/verify. Enrollment returns credential metadata; deletion's TODO names future backend integration. No backend challenge acquisition, registration submission or verifier network call exists in this service's operation path. |
| [codex-rs/user-verification/src/lib.rs](https://raw.githubusercontent.com/openai/codex/rust-v0.160.0/codex-rs/user-verification/src/lib.rs), all 84 extracted lines | Provider contract explicitly excludes network registration and assigns backend revocation to caller. It exposes local status/key/signing operations; stock provider selection is macOS or unsupported. Device probing is separate from key/enrollment checks. |
| [codex-rs/app-server/src/request_processors/initialize_processor.rs](https://raw.githubusercontent.com/openai/codex/refs/tags/rust-v0.160.0/codex-rs/app-server/src/request_processors/initialize_processor.rs), L74–144 | Automatic mode insertion and eligible-connection enablement require experimental + supported device + exact InProcess/codex-tui or Stdio/Codex Desktop pair. Stored experimental opt-in remains separate. |
| [codex-rs/app-server/src/outgoing_message.rs](https://raw.githubusercontent.com/openai/codex/rust-v0.160.0/codex-rs/app-server/src/outgoing_message.rs), L48–92, L219–255, L301–372 | Request cancellation scope is selected by method; registry/cancel does not consult eligible connections. Elicitation routing does consult them, captures account identity/revision, chooses one owner and rechecks eligibility before proceeding. |
| [codex-rs/app-server/README.md](https://raw.githubusercontent.com/openai/codex/refs/tags/rust-v0.160.0/codex-rs/app-server/README.md), L94–160 | Documents trusted-host backend enrollment challenge → verify → matched credential → public metadata/proof submission; account preservation and uncertain-registration reconciliation. Direct verify needs no pending elicitation. The prose does not supply registration endpoint/schema. |

`app/src-tauri/src/hosting.rs` currently supplies truthful `chirality-app-v4`, `experimentalApi: true` and stdio at local L481–483 and L420–438. Earlier packet's hosting hash/ranges are historical; current hash differs. No App runtime was invoked.

## Limits and smallest next unit

Separate the five questions:

- **API admission:** source supports truthful local stdio Chirality direct RPC use after initialize/experimental opt-in, subject to service guards. No successful call is witnessed.
- **Automatic advertising/delivery:** current identity fails the source predicate; direct RPC use cannot populate the eligible set or create a hosted pending request.
- **Device availability:** build/platform/account/native readiness remain unobserved. No platform probe or status call was made.
- **Backend registration/binding:** a separate trusted host/backend contract is required. The inspected implementation affirmatively leaves this responsibility outside the primitives. No exact enrollment challenge, registration, revocation, verifier/account binding or retry/reconciliation endpoint contract was obtained. This is a bounded missing contract, not a claim no such service exists anywhere.
- **Actual proof handoff:** a local signature result is neither registered identity nor verifier acceptance. Legitimate challenge origin, original pending request and backend consumption remain separate evidence obligations.

The smallest source/integration input is the supplier-supported trusted registration/verifier contract and legitimate third-party elicitation delivery route. An additional source clarification could identify how another supported stock interface delivers the mode; changing Chirality's client name is not that input. For direct primitives alone, the smallest later witness is an expressly authorized stock candidate/local stdio test retaining `chirality-app-v4`, with experimental opt-in and native/account readiness, plus cancellation/account-change behavior. Such a test must not be confused with hosted-mode or backend qualification. No native test is authorized or performed by this report.

Fetch limits: initial `refs/tags` service URL failed; the tag-short raw URL succeeded with complete service text. Guessed mod/processor paths, macOS implementation/key namespace, supplier RPC/activation test files and `user_verification_auth.rs` variants returned fetch errors/cache misses. These are retrieval limits, not absent API claims. Native-provider implementation and the separate eligibility/auth helper were not independently read; provider contract + complete dispatch/service + outgoing routing suffice for the bounded answers above, not broader supplier qualification. `lib.rs` startup source was also read (imports/module context), with no further claimed result.

## Supplied/local basis custody

Root-relative origins below, except explicitly absolute skill origin. SHA-256 of actual local bytes read; manual read extent is README, User Manual headings through level three, Field Book in full. No work graph construction/resumption, authority adoption or closeout is performed by this bounded investigation.

| Origin | SHA-256 |
| --- | --- |
| `AGENTS.md` | `f96feb19d297c74e10048c506805b2fe3622c50cfefd6078f599724556113977` |
| `agents/AGENT_TASK.md` | `1a13a5b00b3ce01ff8519efe6b46bcbe0cd6a5b7985e24282fa7efa2c57c8fb7` |
| `projects/chirality-app-v4/loop/LOOP_INIT.md` | `45c23cf477e23aff1d0152189caf7e8ebfb53eca42e3a1fae87a06af8c197f28` |
| `docs/alignment-manual/README.md` | `31217d30b0d2743bef0d7c1a54bb9a81814d56b24ff0961cf01d9532952e305f` |
| `docs/alignment-manual/CHIRALITY_AGENT_USER_MANUAL_v3.md` | `08ca0e40cd5157574a011bac57d539e77e9007a0d46494785da8b92745391b1a` |
| `docs/alignment-manual/Project_Management_for_Human_Agent_Teams_Field_Book_v1.md` | `02d53a3966220001318aacf3f46e1b63b8695a098c81b20f4e3e1531b93024d3` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/NATIVE_USER_VERIFICATION_AVAILABILITY.md` | `cff8370bfb84dd92bdd8a64b956d692495e5dc0553280ae5defaa7d87fcae9e1` |
| `projects/chirality-app-v4/app/src-tauri/resources/supplier/0.160.0/codex_app_server_protocol.schemas.json` | `7243ba241962af92ca60581f1a81808ebda4212a800f8b205f54703bcfd508c5` |
| `projects/chirality-app-v4/app/src-tauri/src/hosting.rs` | `0c381383a6c68d15bae9935b2ebca1e2f2f24099f27291714aaa72263a281a2d` |
| `/Users/ryan/.codex/skills/.system/openai-docs/SKILL.md` | `aa6829e21df2223167c85d2e49b6337a7345c84c1033f1ec10182c7882b36d45` |

OpenAI Docs skill body was consulted for source guidance; the explicit parent brief required local schemas first and official pinned repository sources, overriding its generic source-order/domain defaults. No route reference, installation, auth or broader product guidance was used.

## Parent corroboration — 2026-10-05

HELP_HUMAN `/root` independently read the same pinned service, provider trait, outgoing router, initialized-request dispatcher and initializer through public web reads. The service calls only local provider operations and leaves registration to its caller; the provider trait expressly excludes network registration. The initialized direct-RPC branches pass connection, cancellation and origin to the service without the first-party eligibility condition. Separately, the initializer populates the verification-eligible connection set only under its exact first-party transport/name predicate, and the outgoing router does not send the hosted verification request without an eligible owner. These observations corroborate the report's bounded distinction. They do not establish a successful local primitive call, hardware readiness, backend enrollment or an available truthful third-party hosted route. No native operation or authority/scope change was performed.
