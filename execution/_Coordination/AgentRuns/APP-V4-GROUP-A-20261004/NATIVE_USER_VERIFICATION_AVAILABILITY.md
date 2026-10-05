# Native userVerification availability — bounded source packet

2026-10-05. TASK `/root/group_a_execution/runtime_core_production`, parent `/root/group_a_execution`; native descendant, no delegation. Source preparation for Root review, not scope disposition, acceptance or qualification. Only this packet is written. Public official documentation/source metadata was read; no package download, gated RPC, sign-in, enrollment, key operation, live verification, model or Cargo operation; no Git mutation. Read-only status/whitespace metadata checks were used.

## Result and current App consequence

Published 0.160.0 documentation resolves the previously untyped proof-content mapping. It also supplies a receiving constraint: Chirality's current client identity does not satisfy the supplier's automatic userVerification advertisement predicate. This is a source-derived constraint on that route, not an observed execution result or a claim that all verification primitives are globally unavailable.

The App currently refuses device-verification acceptance explicitly: `app/src-tauri/src/runtime_session.rs` line 216, and `app/src/App.tsx` lines 29, 64–66. Request-card decline/cancel remain available. Full NIR support is not complete.

## Published evidence and exact inspection boundaries

All URLs are official OpenAI stock sources pinned to `rust-v0.160.0`, except the separately marked general guide. Remote ranges below are the browser tool's **zero-based extracted page lines**, not asserted GitHub source-file line anchors; raw and HTML renderings have different numbering. Local ranges are one-based file lines at inspection.

| Source | Inspected relevant ranges | Contribution |
| --- | --- | --- |
| [Pinned app-server README, raw](https://raw.githubusercontent.com/openai/codex/refs/tags/rust-v0.160.0/codex-rs/app-server/README.md) · [human-readable source](https://github.com/openai/codex/blob/rust-v0.160.0/codex-rs/app-server/README.md) | raw L45–64; L94–113; L121–160. Earlier HTML view L212–217 and L233–251 agrees on these clauses | Cancellation, receiving scope, readiness/enrollment and proof handoff |
| [Pinned initialize processor, raw](https://raw.githubusercontent.com/openai/codex/refs/tags/rust-v0.160.0/codex-rs/app-server/src/request_processors/initialize_processor.rs) · [source](https://github.com/openai/codex/blob/rust-v0.160.0/codex-rs/app-server/src/request_processors/initialize_processor.rs) | raw L98–122 and L140–144; earlier HTML L905–949 and L986–992 | Advertisement predicate and connection enablement |
| [Pinned MCP protocol source](https://github.com/openai/codex/blob/rust-v0.160.0/codex-rs/app-server-protocol/src/protocol/v2/mcp.rs) | HTML L3404–3427 and L3619–3665 | Typed verification request; response content forwarded unchanged |
| [Official general app-server guide](https://developers.openai.com/codex/app-server/) (redirects to ChatGPT Learn) | Whole fetched page searched for `userVerification`: no match | Bounded guide search only; not evidence of global absence |

The initialization predicate is experimental API enabled **and** supported device **and** either in-process `codex-tui` or local stdio `Codex Desktop`. The source excludes opting other hosts in through client extensions. Current `app/src-tauri/src/hosting.rs` lines 426–430 supplies experimentalApi true but client name `chirality-app-v4`; the identity branch therefore does not match. No relabeling/spoofing, supplier patch, or opt-in bypass is proposed. This advertisement constraint must be distinguished from documented local-transport primitive access and an actual capability witness.

## Documented proof, enrollment and cancellation

For the accepted wire action, place the native `verify.result.proof` object directly in `content`, not its containing result wrapper:

```json
{"action":"accept","content":{"credentialId":"<native value>","signature":"<native value>"},"_meta":null}
```

Placeholders describe representation only; they are no proof. The protocol forwards content unchanged. Native proof must remain tied to the original challenge, pending request, full generation and actual issuer; schema-valid JSON alone does not establish that origin or verifier acceptance.

The README assigns backend registration to the trusted UI: acquire an enrollment challenge, sign it, match credential ID, then submit public metadata and proof. Require non-null algorithm/public key, preserve authenticated account, and reconcile uncertain registration. Local readiness/key creation is not server registration. No browser/registration endpoint is specified in the inspected verification clauses. Account OAuth/device-code sign-in is a separate flow; verification has a ChatGPT-identity prerequisite.

Native cancellation targets its client RPC ID on the same connection, separately from the elicitation. A signal acknowledgment does not prove termination or rollback; discard late proof after elicitation closure. Failures retain their closed native type/reason categories. These facts do not establish SEAL-2 or App person identity.

## Remaining prerequisite and bounded absence

Inspected the pinned sources above and primary-source searches for userVerification, enrollment challenge, registration, proof/content mapping and `ecdsaP256Sha256X962`. The accessible sources supply the enrollment sequence but no backend endpoint or enrollment/verifier request-response specification. Direct attempts to read the pinned `codex-mcp/src/user_verification_elicitation.rs`, guessed app-server user-verification module/tree and guessed TUI/user-verification paths returned cache misses/internal fetch errors; a pinned raw MCP protocol fetch also failed while its HTML source was readable. Those failures do not establish file/API absence. No third-party search result was relied on.

Root's concrete route choices are: pursue a supplier-supported third-party receiving/registration contract; adopt a separately reviewed supplier version/interface that actually supports this client; or retain this mode as unavailable in the current App path with its production obligation open. An own-authenticator option in supplier prose does not itself override advertisement eligibility or supply backend registration. Each productive route needs exact backend identity/binding and candidate-native witnesses for valid proof, rejection, cancellation/late results and uncertainty. Synthetic source/schema/transport checks can prepare that unit but cannot establish native verification success.

Ordinary request custody, native non-verification cards, decline/cancel, role guidance, records/acts and other authorized production continue. P3 packaging and SEAL-2 retain their separate owners, identity, custody and witnesses; this packet neither satisfies nor expands them. No human action is requested now.

## Local source identity at inspection

| Origin | SHA-256 |
| --- | --- |
| `projects/chirality-app-v4/app/src-tauri/src/hosting.rs` | `b25b8e937c58e296047f36789b2b53eaa5b6599278a2ef1cc58d12dffdd19343` |
| `projects/chirality-app-v4/app/src-tauri/src/runtime_session.rs` | `77114507c1715442d6384d7cd9dde71c97bfaf80bc6f69f6428affda150f412e` |
| `projects/chirality-app-v4/app/src/App.tsx` | `9501bb821cf06739df7a19461b8f33803f6fac380abde78925f5f857beb1985c` |
| `projects/chirality-app-v4/app/src-tauri/resources/supplier/0.160.0/codex_app_server_protocol.schemas.json` | `7243ba241962af92ca60581f1a81808ebda4212a800f8b205f54703bcfd508c5` |

## NIR production consequence — bounded receiving-owner assessment

2026-10-05. TASK `/root/group_a_execution/design_aac`, parent WORKING_ITEMS
`/root/group_a_execution`; native descendant, no delegation. Packet author
ownership transferred by parent for this append only. Existing evidence above
is retained verbatim, including its historical source hashes. Read-only local
contract assessment; no fresh remote verification, supplier execution, gated
RPC, network, enrollment, key, API, credentials, product/Design or Git changes.
Source predicate below is relied on as the packet author's identified pinned
source finding, not this TASK's independent supplier witness.

### Exact promise and negotiated boundary

| Governing clause | Consequence for this mode |
| --- | --- |
| Current PRD V4-APP-01 and original seed V4-APP-01 | Full native harness experience includes approvals/questions. It names no guaranteed universally available hardware/authenticator or every first-party application. It remains the broad functionality commitment. |
| Current PRD V4-APP-04 / original seed V4-APP-04; V4-EXE-02/03 | Preserve native requests; answer or explicitly decline requests actually raised; show only observed events. No request that was never raised may be fabricated as received, answered or verified. |
| DEL-01-04 ScopeOfWork OUT-001, REQ-001, AC-001 | Provide native answer/decline through the execution-owner interface; offer only supplier-listed answer forms; unsupported/unknown errors remain explicit. A capability unavailable on this supplier/client is a truthful limit, not a successful answer. |
| DEL-01-04 REQ-006/007; CLM-002/003; VER-001/007 | Supplier pin/protocol qualification belongs to DEL-01-01, custody/settlement to DEL-01-02. NIR retains its receiving obligations and reports unresolved input and candidate limits; simulated cases cannot replace actual candidate/supplier response evidence. |
| NIR §4.1 `mcpServer/elicitation/request` row | Explicitly includes `openai/userVerification` as known-answerable/person-input; the card shows the challenge, completed only by the person. This exact mode promise goes beyond generic handling of unavailable method names. |
| NIR §4.2 FO-6 | An elicitation card offers accept with content, decline and cancel. For this mode, positive acceptance needs authentic challenge-bound proof through the supported supplier path; handwritten JSON, synthetic signature fields or a decline are not that completion. |
| HOSTING §6.1 familiar set and §7.3 experimental status | Familiar methods are reference output limited by declared handshake capabilities; undeclared method capabilities are unfamiliar. Merely declaring experimental API does not establish an advertised MCP mode or native proof/enrollment readiness. The enclosing elicitation method and this mode's advertisement are different predicates. |
| HOSTING §6 R9; §8.4 HCG-A07 (historical definition-pin account) | Person-input content comes only from the person's path; a named rule may decline/error, never fabricate content. Elicitation answers remain conversation input, not AAC human acts, SEAL-2 provenance or professional identity. The pin-specific availability account must be re-examined for 0.160.0 rather than inferred from 0.158.0 schema presence. |
| DEL-01-01 ScopeOfWork REQ-005/VER-005, AX-001/004 | Published requirements and observed capability are separate; qualify the actual stock supplier/candidate and disclose unsupported/unobserved portions. Private supplier modification or unsupported translation is outside this contract. |

The packet's **0.160.0 source-derived automatic advertisement predicate** is
experimental enabled AND supported device AND either the in-process codex-tui
branch or the exact local-stdio Codex Desktop identity branch. With the truthful
Chirality client identity reported above, the identity condition is false even
when experimental is enabled and hardware is supported. This conclusion is
bounded to that predicate and route: it neither says every first-party client
qualifies nor proves every local verification RPC, own-authenticator primitive,
backend API or alternate supplier version is unavailable. Changing the name to
one of the eligible clients would spoof provenance, not satisfy a receiving
input. The supplied finding that extensions cannot opt another host in is not
reversed by an App opt-in setting.

### Production standing

**Conforming negotiated handling with a disclosed limit:** use the truthful
Chirality identity/capabilities, preserve actual receipt and supplier settlement,
allow native decline/cancel where offered, refuse unavailable positive proof
with its cause, and never invent a verification result or imply verification
from silence. If no userVerification request is raised because this route never
advertises the mode, there is no unanswered received request to settle. This
alone does not breach the no-silence/no-fabrication receiving rules.

**Required positive behavior still incomplete:** NIR §4.1 and FO-6 expressly
include the mode and its positive answer path. The current supplier/client
route does not establish that path; the packet reports the App refuses its
positive device-verification acceptance. Consequently full NIR production or
positive userVerification qualification cannot be claimed. Schema/transport
fixtures and decline/cancel can demonstrate bounded receiving behavior but
cannot close that missing functionality or witness. The source-derived
non-advertisement is not itself an owner waiver, a reclassification of all
elicitations as unsupported, or proof that an alternative valid native route
can never supply the required input. Other independent production continues.

### Smallest supplier-supported dependency and actual owner choices

The smallest missing **receiving input** is a documented stock-supplier route
that admits this truthful third-party client to challenge/proof handling,
together with the exact trusted registration/verifier contract for that route.
A route must state how the mode is legitimately advertised or otherwise
legitimately delivered to this client, how an authenticator is registered to
the authenticated identity (including enrollment challenge and credential ID),
and how challenge-bound proof content is admitted. The existing local primitive
and documented enrollment sequence are useful parts, not the complete input:
no backend endpoint/request-response contract or honest Chirality advertisement
route is supplied by this packet. Therefore no complete current 0.160.0
supplier-supported Chirality positive route can be specified from these sources.
Do not replace that gap with a guessed endpoint or a global impossibility claim.

A concrete next research/coordination unit for DEL-01-01/01-05 with NIR is to
obtain that exact third-party supplier receiving/registration contract, or
identify a published stock version/interface that already provides it. Pin the
eligible client/transport/device/account predicates and backend binding, then
perform upgrade comparison and candidate-native positive/rejection/cancellation/
late-result/uncertain-registration witnesses under separately authorized native
operations. Native verification proves no AAC actor identity or SEAL-2 origin.
It is unnecessary to redesign general request custody to identify this input.

The owner decision changes different things depending on its actual words:

- Authorize pursuit of the missing supplier contract/version: authorizes that
  bounded investigation; it does not establish availability, enrollment or
  product completion. No download/auth/key permission is inferred.
- Adopt an identified stock supplier version/interface after evidence and named
  review: changes the supplier basis and affected receiving implementation;
  keep truthful client identity and positive native witnesses. No identified
  alternative is qualified in this packet.
- Continue this increment with this mode unavailable: records an explicit
  capability qualification and keeps the required positive obligation open.
  It does not by itself narrow NIR or allow declaring full production complete.
  Removing/deferring the express mode promise or changing completion criteria
  requires its owning scope/change/acceptance disposition; the present TASK
  proposes no such amendment or blanket product scope reduction.

Selecting Codex Desktop/TUI by name as a replacement would change the actual
hosting/integration boundary and needs a concrete supported architecture;
it is not the smallest App setting or a route established here. No supplier
patch, spoofed identity, opt-in bypass, generalized first-party restriction,
request fabrication or current contract narrowing is proposed. Root owns the
human question after this evidence/obligation distinction.

### Consequence assessment source identity

Pre-append packet SHA-256: `fa965f35c61340c998b9cd2cbd545480b7cf30710e21e01a032bd149519d7603`.
This section read the exact local clauses identified above. Local source bytes
are bound below; earlier supplier URLs/ranges and their inspection limits remain
as recorded by the packet author, with no new network witness claimed.

- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design/NATIVE_INTERACTION_RECEIVING.md`: `f9794dcc24d55b813b760daa0f120d9fc53c4893282e907b550e60cdb085ab7a`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/ScopeOfWork.md`: `8434cc47ec28e1397e7dae548183543567f0b5fcfdefaebc0b44bc1f709aacf3`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-01_Stock Codex hosting and supplier contract/Design/HOSTING_BOUNDARY.md`: `47b8f1c6fb01e1f495099b06cd3fc10e95d03c032e8d122ede4378f28e194087`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-01_Stock Codex hosting and supplier contract/ScopeOfWork.md`: `bbc81a8d31eeacab3497acf297c8c6eeac7b2f6febda5381f332ec14b8f65d02`
- `projects/chirality-app-v4/docs/PRD.md`: `bb6e786f7a6c01dc5ce2f16f58e6c600989a12808ff47ce4fd87924bcc6c49bd`
- `projects/chirality-app-v4/execution/_Coordination/Acceptances/APP-V4-BASIS-20260926/original-seed/PRD.md`: `ff57362886b76da07df6feaed1630661f427c071dc5720c38c0a61d7d9e90491`
