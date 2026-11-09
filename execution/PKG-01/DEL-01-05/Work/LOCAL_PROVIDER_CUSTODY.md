# Authenticated oMLX through Codex custody

The selected local route applies ACCESS §4 K2-1 and V4-ARC-04: a dedicated
App-owned Codex home holds the local provider's account credential. It does
not use the omitted standalone OpenAI API-key product mode or its H-key UI.
ACCESS CR-8 remains intact. The App never writes the key to a configuration
file, environment, command line or App credential store.

The owner-selected nonsecret destination is `http://127.0.0.1:8000/v1`, provider
`chirality-omlx`, model `mlx-community/Qwen3.6-35B-A3B-8bit`. This bounded route
admits only that provider, endpoint and model. Other local providers retain
their existing anonymous route; this capability grants no endpoint discovery,
server launch, model load or external account authority.

## Source support and limits

The mechanism is source-established at Codex 0.167.0 commit
`086ccc833bc9cf01024ad2dd6af7dbd421b6bf9a`:

- [account processor](https://github.com/openai/codex/blob/086ccc833bc9cf01024ad2dd6af7dbd421b6bf9a/codex-rs/app-server/src/request_processors/account_processor.rs#L462)
  sends `account/login/start {type:apiKey,apiKey}` to Codex custody. Login saves
  and reloads auth; its acknowledgment does not validate the key at a server.
- [login manager](https://github.com/openai/codex/blob/086ccc833bc9cf01024ad2dd6af7dbd421b6bf9a/codex-rs/login/src/auth/manager.rs#L1090)
  saves the API-key variant using Codex's selected credential backend. This
  route fixes `cli_auth_credentials_store="file"`; Codex writes `auth.json`
  in its own local home using private atomic replacement. The App checks its
  metadata without reading credential contents. No keychain service is added.
- [provider auth](https://github.com/openai/codex/blob/086ccc833bc9cf01024ad2dd6af7dbd421b6bf9a/codex-rs/model-provider/src/auth.rs#L284)
  uses the home auth for a custom provider with `requires_openai_auth=true` and
  no provider credential override. [Provider routing](https://github.com/openai/codex/blob/086ccc833bc9cf01024ad2dd6af7dbd421b6bf9a/codex-rs/model-provider-info/src/lib.rs#L469)
  gives the explicit local base URL precedence over OpenAI defaults. Bearer
  authorization goes to that provider's transport.
- [Catalogue eligibility](https://github.com/openai/codex/blob/086ccc833bc9cf01024ad2dd6af7dbd421b6bf9a/codex-rs/model-provider/src/models_endpoint.rs#L320)
  excludes this custom provider with an explicit base URL and no catalogue
  URL. [The manager](https://github.com/openai/codex/blob/086ccc833bc9cf01024ad2dd6af7dbd421b6bf9a/codex-rs/models-manager/src/manager.rs#L749)
  suppresses API-key discovery for it. Bundled model metadata is not an oMLX
  model discovery result; the App offers only the owner's explicit model.
- Login-notification account reading and background workspace routing require
  ChatGPT auth before backend discovery. API-key token refresh returns without
  contacting a token endpoint; rate-limit reads reject non-Codex-backend auth.
  Installed/recommended remote plugin paths also exclude API-key auth. This
  home fixes plugins off. These checks do not qualify every curated or
  configurable service and are not a universal no-egress claim.
- [Redirect handling](https://github.com/openai/codex/blob/086ccc833bc9cf01024ad2dd6af7dbd421b6bf9a/codex-rs/http-client/src/route_aware_redirect.rs#L112)
  strips Authorization across origins in the route-aware path; default
  redirects use the supplier's HTTP client policy. An explicit local base URL
  does not establish a universal network sandbox. Actual transport behavior,
  oMLX acceptance and server substitution remain unobserved for this route.

Native capability admission binds the actual canonical package: main SHA-256
`030316ecfbb41f4e7946e584b0063ef333b7a36cd312ba349f2f6869e39b62cc` and full
inventory manifest SHA-256
`158dd67072236253a694ca06d9bf7bfdebbe20d4a197bbf675433cbdddea7e7b` at the
original full generation. Matching the npm main executable or declaring a pin
alone cannot establish the canonical 42-file tree. This source assessment
neither adopts a supplier distribution nor transfers .160 runtime evidence.

## Native implementation and receiving contract

`home_resources.rs` and `runtime_session.rs` allocate the explicit local home
`codex-omlx` under the selected App-data root and include its prospective path
in the existing Root protective namespace binding. The source is separate from
H-acct and H-key. Its internal recovery class is `H-omlx`; its public mode is
`local-provider`. Native threads and pointers retain their original home,
generation and supplier receipts. No thread, account or project is migrated.

The home has its own fixed NONSECRET `config.toml`, without account configuration,
AGENTS or skills links. Process-start overrides fix its provider definition,
provider/model selection, file credential backend and plugins-off setting.
The App creates its home with mode 0700, nonsecret config and empty auth lock
with mode 0600. Existing unsafe modes, links, hard links or configuration drift
are refused without chmod, overwrite or migration. Codex alone writes the key
into its credential file. These permissions do not promise secrecy from the
same user, root, backups or OS memory and are not an erasure guarantee.

The nonsecret IPC commands are `prepare_local_provider()` and
`submit_local_provider_key(generation)`, both bound to the actual invoking
native window. Neither takes a key, endpoint or model argument. Preparation
creates only fixed local resources and the selected supplier source; key entry
is a native secure field, followed by the existing private account pipe.
Original source, generation, config and window are checked around entry. One
entry attempt per generation is consumed even on cancel or unknown outcome;
there is no automatic retry or replay. Account/H-key wrappers retain their
existing signature, wording and behavior.

The DTO names `modeHomeClass`, `entryId`, `providerId`, `endpoint`, `model`,
`generation` and `credentialState`. The fixed entry is `local-provider-keyed`.
States are `entry-required` or `configured-not-verified`; the latter requires
an actual matching private login acknowledgment and same-source API-key account
read. Configuration, acknowledgment and account type establish no credential
validity, actor identity, personal act or completed model run. Raw keys never
enter renderer DTOs, App journals, history, captures or error text. Existing
private account transport supplies fixed withholding.

## Child receiving at the selected source

The .167 canonical subject can receive parent `thread/start` dotted
`agents.<ROLE>.description` and `agents.<ROLE>.config_file` entries. Source role
parsing applies the role's child-only developer instructions. The supplier's
supported V2 explicit-role spawn permits both no-history and full-history
forks; V1 full-history forks reject an explicit role override. The old .160
both-fork observations are retained only at their original subject.

App admission preserves source/config-layer and namespace guards, requires the
actual selected source, and rechecks that supplier subject before dispatch.
Observed adoption still requires the original completed activity, correlated
child `thread/read`, original parent/turn and current parent carrier. Positive
synthetic .167 receiving fixtures are not new native behavioral evidence.
Supplier-owned carrier/control and generated-protocol updates are separate
integration inputs. No generic declared-pin promotion is allowed.

The owning Scope's candidate-native, account-coexistence, substitution and
network verification obligations remain. Scripted/source checks support only
the behavior they exercise; secure key provisioning and actual local-server
use await the owner's useful-point act through the secure route.
