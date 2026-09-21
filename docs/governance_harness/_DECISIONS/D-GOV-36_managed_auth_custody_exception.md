# D-GOV-36 — Managed authentication custody, bootstrap and logout

Status: RULED — 2026-09-06 custody/bootstrap/logout boundaries EFFECTIVE; 2026-09-07 account-only amendment APPLIED_UNPUBLISHED.
Owner: Ryan Tufts
Owner decision date: 2026-09-06 (local MDT)
Accepted source basis: main@2c75eb4bf03436eb305310996044eca0b67d3116
CandidateSHA: 4827bbe0cf309aa891c90bdf4c38586f726abb21
PublicationSHA: e1dee34315ff4ca448b0fbc14e5542b6bad9fac2
EffectiveSHA: e1dee34315ff4ca448b0fbc14e5542b6bad9fac2
ID allocation: D-GOV-36 verified next free on application basis main@2c75eb4.

## Recorded owner act and exact referent

> I approve these three recommended dispositions.

The owner act is transcribed in
`projects/chirality-app-dev/execution/_Coordination/_DECISIONS/D-APP-126_RULING_CREDENTIAL_CUSTODY_BOOTSTRAP_AND_LOGOUT_2026-09-06.md`,
SHA256 `4480ad2e70bfcac6487980d9a310ae52720cb472c10467897d97aaf184e55a73`.
The exact selected slate is
`projects/chirality-app-dev/execution/_Coordination/AgentRuns/APP_RUNTIME_CONTRACT_REVIEW_2026-09-06/control/CUSTODY_DECISION_SLATE_v1.md`,
SHA256 `429b2e8305d2e79b1a55f539174cc133e413bbf6c79eb951df77cb0c222b5cc2`.
This records settled choices. Root recording was applied under the explicit owner M2 grant below, published from candidate `4827bbe0cf309aa891c90bdf4c38586f726abb21`, and became effective through PR #740 merge `e1dee34315ff4ca448b0fbc14e5542b6bad9fac2`.

## Narrow later disposition

Owner selected all three dispositions in the pinned App slate, as recorded by D-APP-126. For managed Codex authentication, permit the daemon-owned exact trusted supplier authentication process to persist credentials using explicitly configured built-in OS keyring as a narrow exception to D-GOV-20 ruled architecture items 2–3's exclusive daemon/Electron safeStorage custody formulation. The packaged daemon remains the sole lifecycle and access controller. Authentication for each canonical root is independently acquired in root-private app-owned contexts. No cross-root credential copying, shared authenticated home, ambient credentials, client/tool-worker credential access or plaintext fallback is permitted. Qualification of the exact supplier, backend and process/storage boundaries is required before operational reliance. A custom adapter is justified only by a demonstrated remaining gap.

Permit an account-only nonexecuting bootstrap auth namespace for sign-in before folder selection. It grants neither project/no-folder execution nor folder consent. Bootstrap credentials are not copied to root contexts. Preserve authenticated project-scoped Unix control, no TCP control listener, operational/non-authoritative credential state, local-model residency and every unaffected D-GOV-20 exclusion. Local profile/settings do not constitute client authority or an additional cloud account.

Global account switch/sign-out durably fences every hosted context in the active account generation. Local-model contexts are unaffected and folder disconnect is local to that folder. Retire tool/turn execution first; retain only necessary purpose-limited context for a separately authorized bounded remote-revoke attempt; then retire auth processes and clear local credentials, verifying cleanup. Ungranted, offline or impossible revoke proceeds to local cleanup with remote state unknown. Do not retain credentials indefinitely or claim browser-wide/provider-global revocation. Human-approval assurance remains separate.

This records selected boundaries, not source implementation, live login/provider/credential operations, protected-fixture retries, supplier acceptance, publication, merge, cutover or release authorization. Exact source/configuration/status and bootstrap+A/B briefs follow through Runtime and App scopes.


## Supersession and effect

This later instrument supplies only the stated exception to D-GOV-20 Ruled architecture items 2–3 and the stated bootstrap/logout boundaries. The original D-GOV-20 decision remains immutable. Its retained transcription in PRD_ROOT remains read with actual later amendments, as that section already requires. Runtime ownership migration remains accepted; no Root product activation is restored.

The App and Runtime loops apply affected contract and derivative changes through their owning instruments. Release of dependent work requires this owner act and applicable notices on fetched origin/main, accepted owning contracts and separately authorized execution scope. Root M2 application authorization is recorded below. Validation is recorded in the application run; publication and effective main observability remain pending.

## Exact Root application authorization

Owner Ryan Tufts, 2026-09-06 America/Edmonton, verbatim:

> Yes apply and validate this bounded Root governance change, including its required M2/G4 manifest, coordination records, and App/Runtime notices

This applies the previously reviewed candidate patch SHA256 `a536943ebc8e646094f025e7f13b74413a6ae959abbc010149f11921ff05dcf9` with truthful application metadata, plus the expressly named manifest and coordination records. Application evidence and byte-identical copies of the otherwise unpublished App ruling/slate are in `execution/_Coordination/AgentRuns/ROOT_D126_CUSTODY_APPLICATION_2026-09-06/`. Those copied sources retain their original hashes and authority class; they do not apply App owning instruments. No commit, push, publication, merge or operational reliance is authorized by this grant.


## Account-only public Unix authority amendment — 2026-09-07

Owner Ryan Tufts ruled: “I approve this narrow authority amendment.” The exact
referent and preserved proposed source are recorded in
`execution/_Coordination/AgentRuns/ROOT_ACCOUNT_AUTHORITY_AMENDMENT_2026-09-07/author/OWNER_RULING.md`.
This section records the narrow substantive boundary described below. Existing
sections above remain historical except for the current-facing status and Git
identity backfill at the head of this record.

Permit a dedicated authenticated account-only authority on the App-facing public
Runtime Unix API, limited to nonexecuting bootstrap authentication, its
status/cancellation and hosted-account lifecycle control/observation. This is
the only exception here to the retained project-scoped Unix control wording.
It grants no project access, folder consent, model/tool execution or direct
private-supervisor access. Project operations, including folder disconnect and
its result retrieval, retain project-scoped authorization. Missing or invented
project IDs are never authorization. No TCP control listener or additional
user/cloud enrollment is introduced.

Only this authority boundary is selected. No endpoint names, complete wire
contract, recipient-delivery mechanism, implementation or operational readiness
are accepted. D126/D36's settled one-sign-in target, independently acquired
root-private authentication, no credential copying or shared authenticated home,
explicit OS-keyring qualification, independent folder consent, nonexecuting
bootstrap, global hosted generation fencing, folder-local disconnect,
local-model independence and bounded cleanup order remain unchanged.

The following seven gates remain before complete wire acceptance and source
activation:

| Gate / owning return | Required concrete disposition |
| --- | --- |
| Root + Runtime authority | Root records the exact D36 interpretation/amendment under its boundary authority. Runtime SCOPE_CHANGE assesses canonical DEL09 REQ-001/002 and DEL06 implications, applies only an authorized exact candidate, records accepted snapshot, derivative/adoption disposition and affected-client notices. Existing decomposition basis is not repinned merely for a later source commit. |
| Runtime + App host authority | Specify authenticated recipient delivery, private storage/access, trusted host identity, issuance/validation/revocation, daemon/host generation binding, replacement/exit detection and renderer method allowlist. A local profile, same-UID file mode, broad operator bearer or newly minted token alone is insufficient proof. No mechanism is established by this ruling. |
| Runtime generation and lifecycle | Specify durable transactions, context admission/fencing inventory, retirement hooks, finite deadlines, late completion/cancellation rules, crash reconciliation and exact internal supervisor operation allowlist. Keep the private supervisor inaccessible to App/CLI. |
| Runtime + App successor recovery | Define separately who may observe old operation outcomes after account-capability rotation, who may direct cleanup/recovery and what may mutate. Do not restore revoked authority or automatically expose old operations to every newly issued account token. Persisted daemon-owned safe cleanup must not depend on the old caller continuing to poll. Distinguish bounded local cleanup from restarting login or replaying uncertain remote revoke. Exact recipient/operation lineage, disclosure scope and recovery authority remain unresolved; no successor grant is selected here. |
| Runtime + App consumer contract | Resolve the exact versioned routes, strict schemas/errors, operation ownership/correlation and ceremony/binding/availability projection, including unavailable identity. Preserve corrected project-authorized result retrieval and discriminated start results. Ceremony completion is not hosted readiness. App owns host bridge and UI adoption. |
| WORKING_ITEMS + independent review | Seal exact source targets, synthetic ports/fixtures, configuration and checks only after the relied contract is accepted. Include rotation/recovery, stale/revoked callers, crash/late completion, bounded cleanup, cross-project denial and strict mixed/secret payload rejection. Review the actual candidate independently before integration. |
| App + Runtime paired validation | Bind rebuilt and actually running Runtime daemon/client/contracts and App/CLI artifacts. Exercise the accepted journey and unsupported version/error behavior. Earlier stub registration or PR746 CI is not this proof. Live login, OS/backend isolation, exact supplier identity/qualification and release remain separately gated. |

Current production remains unavailable before effects with unavailable binding
and hostedReady:false. This boundary does not enable live start, supplier/build/
credential operations, protected-fixture retries, no-folder execution, a new
success-identity schema, lifecycle promotion or release. No successor recovery
grant is selected. Standing Git authority is separate and supplies no contract
acceptance or operational authority.

Runtime must apply the affected DEL09/DEL06 contract changes through its owning
SCOPE_CHANGE instruments with exact accepted snapshots, derivative dispositions
and notices. Root successor adoption follows where required. Neither an
accepted downstream SOW nor a repinned decomposition basis is claimed here.
