# Codex 0.167.0 — current development integration

The owner selected 0.167.0 for assessment/integration. This replaces the active
0.160.0 development pin, without transferring its qualification or observed
exchanges. Production still refuses the historical compiled 0.160.0 reference.
The App consumes the new generated schemas directly and preserves native fields.

The official annotated `rust-v0.167.0` tag resolves to source commit
`086ccc833bc9cf01024ad2dd6af7dbd421b6bf9a`. The owner-approved
[canonical macOS arm64 package](https://github.com/openai/codex/releases/download/rust-v0.167.0/codex-package-aarch64-apple-darwin.tar.gz)
is 166,340,155 bytes, SHA-256
`af45ed45d940d7998809622c1c0296d3098ed7d7fad695284422c228bd454517`.
Full size/hash verification preceded extraction; all 50 members are ordinary
files/directories, with no links or special entries. The exact 42-file,
30-Mach-O inventory and metadata are retained in
[CANONICAL_DISTRIBUTION.json](../../../../app/src-tauri/resources/supplier/0.167.0/CANONICAL_DISTRIBUTION.json).
Its file manifest is `158dd67072236253a694ca06d9bf7bfdebbe20d4a197bbf675433cbdddea7e7b`.

The acting main is SHA-256
`030316ecfbb41f4e7946e584b0063ef333b7a36cd312ba349f2f6869e39b62cc`.
It equals the retained installed npm generator main. The entire trees differ:
the canonical package adds `bin/codex-exec-server` (61,038,432 bytes,
SHA-256 `385736a6d82e125d4946a672074eb3a9f13e45a4aaecee4b72d592c0e1bb566a`)
and changes `codex-package.json` to declare `execServer` at that path. Every
other shared entry's content, type and mode matches. The npm generator tree
has 41 files/29 Mach-Os and manifest
`e4ea2270217a849432a8d86bb3b45fa7a643781a1afffabf8ba5dfd9ffcaa257`;
it is not the selected acting distribution.

The exact development assertion invokes a complete canonical-member preflight
before `--version`, using the maintained no-follow inventory/comparison seam.
Missing, additional or changed members/modes/metadata refuse. Both main and
exec server must be executable Mach-Os. The archive has no root member, so the
owned private/bundled container's mode is separate from its declared members.
A match retains `unverified-development` and supplies all 42 file identities;
it authenticates no signature and grants no S3/S4 or installed custody.
Other development assertions retain their existing route. Production's old
reference refusal remains in force. Files can change after preflight; this is
an observation with the maintained check-to-execution race limit.

Both package preparers preserve the complete vendor tree beneath
`Contents/Resources/codex/`, including the new helper, rather than treating it
as a renamed/re-signed Tauri sidecar. They require the exact 0.167.0 metadata
and helper. Preparation still cannot borrow the old distribution attestation.
Supplier [install-context](https://github.com/openai/codex/blob/086ccc833bc9cf01024ad2dd6af7dbd421b6bf9a/codex-rs/install-context/src/lib.rs)
recognizes a main under package `bin/`, with sibling `codex-resources` and
`codex-path`; its manifest reader consumes version, not an App-invented helper
launcher. [arg0](https://github.com/openai/codex/blob/086ccc833bc9cf01024ad2dd6af7dbd421b6bf9a/codex-rs/arg0/src/lib.rs)
prepends package `codex-path`. Executor
[runtime options](https://github.com/openai/codex/blob/086ccc833bc9cf01024ad2dd6af7dbd421b6bf9a/codex-rs/exec-server/src/runtime_options.rs)
retain the actual main path for hidden helper modes. App adds no exec-server
service or direct helper launch. Actual discovery/custody and helper permission,
sandbox, signature/hardened-runtime behavior remain candidate-bound runtime
qualification, including the newly supplied executable; 0.160.0 S3/S4 cannot
establish them.

The manual product-CI supplier step uses this exact canonical archive, verifies
size/hash before safe extraction, and selects its direct vendor root. PR shards
acquire no supplier. Preparing this workflow is not a manual dispatch or a new
runtime qualification.

## Generated protocol and consumer deltas

[GENERATION.json](../../../../app/src-tauri/resources/supplier/0.167.0/GENERATION.json)
identifies the actual isolated installed-npm generation, empty allowlisted
environment, fresh homes and bounded argv. One stable pass produced 322 JSON
files/3,751,081 bytes; one experimental pass produced 470 files/4,654,630 bytes.
The manifest identifies all 792 outputs. Only the two consumed experimental
bundles are compiled into App; no TypeScript generation or repeatability claim
is made. Canonical main equality preserves that actual generator identity;
there was no redundant rerun or relabeling of its original tree provenance.

Root definition names are unchanged; `ClientRequest`,
`CommandExecutionApprovalKind`, `InitializeCapabilities` and
`ServerNotification` have validation changes. Experimental v2 definitions
increase from 776 to 827, with 51 additions and no removals. The relevant
consumer consequences are:

| Native change | App receiving meaning |
|---|---|
| Provider capabilities removes `namespaceTools` | Codex removed the provider gate on tool namespaces ([openai/codex PR 50447](https://github.com/openai/codex/pull/50447)). By the owner's decision of 2026-11-09, delegation reads present when `multiAgentVersion` and the effective `features.multi_agent` allow it, and missing only for those two negatives; a legacy `namespaceTools` echo is ignored. DEL-01-03 [`NATIVE_PLANS_TOOLS_DELEGATION.md`](../../DEL-01-03/Work/NATIVE_PLANS_TOOLS_DELEGATION.md) §7.1 states the rule. |
| Optional initialize `requiredHumanApproval`; new approval kind `humanCommand` | App does not advertise/adopt the capability. An unsolicited checkpoint is explicitly unsupported and cannot become an ordinary or session grant. Existing command approvals remain supported. |
| Optional fork `attachToSource`/prediction fields; turn `parentTurnId`, `rootTurnId`, metadata patch; steer metadata patch | App does not send the new controls. Existing exact start/fork/text/steer/interrupt request shapes remain the receiving basis. Native additional fields are preserved. |
| Optional history attached-thread/exclusion filters and `readState(s)` | Existing list/read/page joins remain; new filters are not supplied or treated as custody. |
| New account GCP/workspace variants | Not adopted as an access mode by this contribution; native access owner retains the account seam. |
| Audio file-ID input alternative; expanded error variants; network `reviewDomains` | No new input/tool permission is inferred. Native items/errors remain source-faithful; approval/permission regressions cover existing decisions. |

Generated shape compatibility proves no runtime-child delivery. The current
[child-role source basis](../../../PKG-02/DEL-02-04/Work/CHILD_ROLE_CARRIER_0.167.0.md)
separates V1 and V2 and retains historical receiving evidence at its actual pin.

## Local credential design input

The selected source supports the K2-1 route: custom provider with explicit
localhost `base_url`, `wire_api="responses"`, `requires_openai_auth=true`,
and no `env_key`, `experimental_bearer_token`, command auth, AWS, gateway or
credential-bearing header override. A dedicated local Codex home receives
`account/login/start` with the private `apiKey` variant. This is internal local
mode; it does not restore the omitted OpenAI API product UI.

[account_processor.rs](https://github.com/openai/codex/blob/086ccc833bc9cf01024ad2dd6af7dbd421b6bf9a/codex-rs/app-server/src/request_processors/account_processor.rs)
dispatches that variant to `login_with_api_key` using the configured Codex home
and selected credential-store backend.
[login auth manager](https://github.com/openai/codex/blob/086ccc833bc9cf01024ad2dd6af7dbd421b6bf9a/codex-rs/login/src/auth/manager.rs)
constructs the API-key auth document and saves it; that function performs no
credential-validation HTTP call. In file mode,
[storage.rs](https://github.com/openai/codex/blob/086ccc833bc9cf01024ad2dd6af7dbd421b6bf9a/codex-rs/login/src/auth/storage.rs)
uses the selected home's `auth.json`, a private replacement file and atomic
replacement. This is Codex custody, not App credential persistence.

[provider auth](https://github.com/openai/codex/blob/086ccc833bc9cf01024ad2dd6af7dbd421b6bf9a/codex-rs/model-provider/src/auth.rs)
uses selected `CodexAuth` for a provider requiring auth, and turns its API-key
token into the Bearer header.
[provider metadata](https://github.com/openai/codex/blob/086ccc833bc9cf01024ad2dd6af7dbd421b6bf9a/codex-rs/model-provider-info/src/lib.rs)
preserves explicit `base_url`; default OpenAI/FedRAMP URLs are not substituted
when it is present. The
[models endpoint](https://github.com/openai/codex/blob/086ccc833bc9cf01024ad2dd6af7dbd421b6bf9a/codex-rs/model-provider/src/models_endpoint.rs)
also preserves explicit base URL; no remote `model_catalog_url` should be
configured. Private login/Create diagnostics must continue withholding token
parameters/content. This source route establishes neither observed no-egress
nor oMLX Responses/model compatibility. Native credential implementation,
secure owner key input and actual destination/custody checks belong to the
access owner and later authorized runtime work.

The separate `experimental_bearer_token` field is real and would send a Bearer
header, but persisting it through config writes puts the token in provider
configuration and conflicts with CR-8/K2-3. It is not the selected design.
No credential RPC was inferred from freeform configuration schemas.

Login completion can schedule ancillary plugin work. The source
[remote plugin guard](https://github.com/openai/codex/blob/086ccc833bc9cf01024ad2dd6af7dbd421b6bf9a/codex-rs/core-plugins/src/remote.rs)
rejects non-Codex-backend auth before authenticated remote plugin fetching;
[AuthMode](https://github.com/openai/codex/blob/086ccc833bc9cf01024ad2dd6af7dbd421b6bf9a/codex-rs/protocol/src/auth.rs)
explicitly makes API-key auth non-Codex-backend. This does not establish a
universal no-egress result for other configured/curated services.


No real key, provider connection, supplier session/turn, installation or App
launch was used in this source/protocol integration. Notice/source investigation
is deferred to this version; old root-body DEFER and unresolved supplier-source
coverage do not become closed through this upgrade or archive intake.
