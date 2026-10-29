# SWBPIPE receiving source and admission correspondence

## Publication verification (2026-10-29)

The SWBPIPE Type 1 manager reconfirmed that its canonical catalog remains
byte-identical to c48efef77bbb799f3ebe902eb213a88330a5994e, SHA256
fe1439998d709e5f3e9641a4d39567000ced56c498fab5b6b8f2028df7c9f669.
There is no replacement pin. The catalog is SWBPIPE-owned; this App PR publishes
its frozen origin, receiving record and offline specimen, not a second catalog.

The counterpart reported #1736 merged at 31084e1f79. This supersedes the earlier
local-only/review-pending account retained below. Subsequent host/witness work
is separate evidence: the manager is currently investigating pinned supplier
stdin EOF and hard app death in fixtures, with launcher activation gated and
SMAppService an unselected fallback. This App publication neither duplicates
that investigation nor establishes actual process cleanup or live capabilities.

Publication rerun in a fresh scratch Codex home: 10 origin tests passed in
0.011 s; 6 exact-source receiving tests passed in 0.001 s. SHA256 checks passed
for both catalogs. The installed jsonschema Draft202012Validator.check_schema
accepted all 12 expanded input/output schemas in each catalog (24 total).
Whitespace checks passed. No dependency installation, supplier/model/GUI run,
heavy build or broad suite was performed.

To reproduce the optional receiving input, export it from any explicitly chosen
Chirality checkout containing the pinned commit, without changing that checkout:

    scratch_codex_home=$(mktemp -d /tmp/swbpipe-publication.XXXXXX)
    git -C "<selected Chirality checkout>" show c48efef77bbb799f3ebe902eb213a88330a5994e:projects/chirality-piping/execution/PKG-16/DEL-16-06/Design/agent-capability-catalog.json > "$scratch_codex_home/receiving-catalog.json"
    CODEX_HOME="$scratch_codex_home" PYTHONDONTWRITEBYTECODE=1 python3 app/supplier_checks/swbpipe_receiving_test.py --catalog "$scratch_codex_home/receiving-catalog.json"

The receiving test verifies the exact SHA256 before executing. Its input is an
explicit export, not a mutable sibling lookup or default build/test dependency.
The origin test requires only this App checkout:

    CODEX_HOME="$scratch_codex_home" PYTHONDONTWRITEBYTECODE=1 python3 app/supplier_checks/swbpipe_projection_test.py

The specimen parses JSON values; it is not a lexical numeric-fidelity guard.
It cannot recover model number tokens normalized upstream, nor establish full
supplier tool isolation. The pinned protocol exposes arbitrary JSON arguments
without a raw model-argument carrier. Production numeric admission, native
operation-string validation, record custody and permissions remain host work.

DEL-09-06/09-07 ScopeOfWork and deliverable.yaml conditions remain unchanged.
This contribution supplies no standalone App external-controller implementation,
platform qualification, acceptance, release or main-policy bypass.

## Current receiving revision: v2

This section supersedes the v1 equality/admission account below; that account
retains the initial receiving history.

Verified local receiving commit: c48efef77bbb799f3ebe902eb213a88330a5994e,
same checkout and catalog/Design paths identified below. Catalog identity:
swbpipe-catalog/2 / design_contract_not_live. Exact committed catalog SHA256:
fe1439998d709e5f3e9641a4d39567000ced56c498fab5b6b8f2028df7c9f669.

Independent SWBPIPE review prompted version 2 at
ce6729f3d67139baf137fff042eee6ba9908171a (catalog SHA256
6451dce8d37778e54b86eb9cdee4e3c035f904947e09c78c276fbe6fbb3bdc89).
The App manager inspected its catalog and Design diff from v1 and verified the
committed hash. V2 requires bounded proposal-level assumptions, preserves the
native operationIntent shape, and distinguishes current live basis from retained
proposal/job/run basis. App raised a concrete mismatch: proposal submission's
status enum could not report applied/withdrawn/unknown despite its new policy.
The counterpart resolved it in c48efef by adding exactly those three statuses.
That final catalog's hash is checked by the receiving test before evaluation.

The counterpart reports twelve expanded standalone schemas and claims lint
passing and independent review confirming the commitment wording at ce6729f3.
Agent 0 wording confirmation is requested through
[draft PR #1736](https://github.com/sgttomas/chirality/pull/1736).
This is a received review account, not an App independent permissions review,
merge, confirmation or runtime adoption. No interface objection remains to
the resolved slice.

The App specimen now selects the catalog's version explicitly. Origin/v1 tests
retain their original semantics. V2 behaves as follows:

- Summary/node/new-proposal/solve admission uses live basis. Historical proposal
  observation and result reads instead require a separately supplied, host-owned
  retained record with matching handle and captured basis.
- Workspace and application generation must still match the admitted session.
  Summary/node completion rejects live revision drift. Other completions bind
  original revision/hash and the host-retained outcome, allowing later live edits.
- Original RPC/call binding, duplicate and detached-session refusals remain.
  A completion cannot rebase its result to the newer live model or forge a
  different outcome from the supplied host record.
- Required bounded assumptions retain stable ids and operation references;
  duplicate assumption ids, duplicate/unknown affected operation references
  and ambiguous operation ids are refused. Native intent shape is unchanged.

The retained-record arguments are fixture-only representations of authoritative
host lookup, not new fields accepted from the webview or supplier. The specimen
does not implement a production record store, cursor registry, queue/apply race,
durable assumptions storage or general JSON Schema validation. Actual receiving
implementation still needs those targeted checks and independent scrutiny.
The v1 blanket current-revision equality is not evidence of v2 conformance.

App verification: 10 origin tests passed (0.016 s), plus 6 opt-in receiving tests
(0.001 s) against catalog bytes exported directly from c48efef, with SHA256
checked before loading. The receiving tests cover applied observation after
edit, solve completion after edit, historical result pages, stale live reads,
wrong generation/workspace/handles, rebasing/forgery/detachment/duplicates,
assumption bounds/references and the resolved proposal status enum.
Whitespace checks passed. No supplier, server, model, build or network run.

Reproduce the optional receiving check by exporting that exact committed JSON
to a fresh scratch directory, then running:

    CODEX_HOME="<fresh scratch home>" PYTHONDONTWRITEBYTECODE=1 python3 app/supplier_checks/swbpipe_receiving_test.py --catalog "<exported JSON>"

The test rejects a different catalog hash. Ordinary origin tests remain
self-contained; the optional check adds no sibling dependency to default tests.
The App catalog stays unchanged origin evidence at 64aad707… and is not a
second evolving source. Later receiving revisions require explicit rebinding
and affected verification, not silently following a mutable file.

## Initial v1 origin and receiving standing

The App origin is commit e1e3f4615b6f766b313c3492506f68254afd8a06.
Its four contribution files are:

- SWBPIPE_CATALOG_PROPOSAL.json in this Design directory: catalog origin,
  SHA256 64aad707acd1d409f3d255381fc597e2ee74e7a4d048aadc5382414d63c64f8c.
- SWBPIPE_CATALOG_WITNESS.md: original source reconciliation and live observations
  still required; the parent App has subsequently clarified its frozen-input
  provenance.
- app/supplier_checks/swbpipe_projection.py: offline projection/admission oracle.
- app/supplier_checks/swbpipe_projection_test.py: invented offline fixtures.

The fifth file in that commit, SWBPIPE_CODEX_INTEGRATION.md, is the frozen
assignment input, not current execution authority. Its original hash and the
first-dispatch steering hash remain historical evidence, not mutable pins.

On this continuation, the App manager read the parent App's current steering
and proposal READ-ONLY. Observed SHA256 values:

- execution/_Coordination/CURRENT_EXECUTION_BASIS.md:
  ff923b4b80a7fd485b86292dfcb5bde383b545768a48e065215737f5e9257a67
- execution/PKG-09/DEL-09-06/Design/SWBPIPE_CODEX_INTEGRATION.md:
  6c81431e4284faa69fa3aa9eb5115e6cad5b4b2b78a48b50bf0f9e84ee59327f

These observed versions authorize the scoped join through the respective
managers. They do not expand this App continuation beyond light source/design
and small offline checks.

The direct counterpart is
[SWBPIPE: App v4 coordination (Type 1)](t3-thread://v1/thread:delegated-task:command%3Amcp%3A430b7a29-d695-474c-bb92-8f42bc864914%3Adelegate-task%3Aa0-appv4-coord-mgr-20261028).
The receiving files are committed locally at these SWBPIPE paths:

- execution/PKG-16/DEL-16-06/Design/agent-capability-catalog.json
- execution/PKG-16/DEL-16-06/Design/embedded-agent-host.md

Verified receiving checkout: /Users/ryan/dev/chirality-t3/swbpipe-appv4-host,
reported branch codex/swbpipe-appv4-host, exact local commit
4d2c8254b534aed1490c02fa3db1d2aea741b52f. The App manager read both files
directly from that Git commit, not the mutable working tree. Catalog SHA256 is
eed9efa8db72f29b018e0715fa15e40f0e97bdf956cf2f0aba0b566d2417a8aa.

Receiving identity is swbpipe-catalog/1 with standing design_contract_not_live.
A parsed comparison with the frozen App origin found exactly three changed
top-level fields: catalogVersion, standing and source. Source retains the prior
provenance and adds appProposal repository/revision/path/hash. Definitions,
tools, limits, hostPolicy and projection compare equal; all remaining fields
are unchanged. The receiving Design explicitly preserves webview authority,
initial binding checks, claimed hash before queue registration, native intents,
proposal-only review and honest interruption/outcome semantics.

Standing: verified local design-contract adoption by SWBPIPE, not main-branch
integration or runtime adoption. The counterpart reports twelve expanded
standalone schemas and claims lint passing; those checks were not rerun by the
App manager. Commitment wording and Design enter independent SWBPIPE review,
then Agent 0 confirmation. The App comparison is receiving-source verification,
not that independent review or confirmation.

SWBPIPE owns the evolving catalog after adoption. The App proposal stays frozen
as origin evidence; this continuation changes no catalog bytes and creates no
second evolving catalog. Ordinary App tests remain self-contained against that
identified fixture. Any future test against a received catalog must identify
its exact source/hash rather than silently treating the origin as current.

The counterpart also relayed Agent 0's update that PR #1732 is merged at
541446a9f1, an official stock Codex binary download is approved, the existing
oMLX server is selected for the local witness, and a hosted provider is allowed.
These are received coordination statements; this App turn did not independently
inspect the merge, download artifacts, inspect server/model installation or run
a provider. Earlier draft wording remains truthful historical input. Current
commitment wording must be received from the merged source before reliance.
Hosted observations must remain distinct from the retained local-model witness.
No server/model installation is authorized or needed according to that return.

## Agreed native admission and bounded repair

The managers agree that:

- The webview remains model authority. Native operation intents go through Rust
  semantic validation and the existing proposal/review/application routes.
- claimedModelHash must match captured and current model hashes before
  registerOperationBatch; that function otherwise snapshots the new state.
- The host binding includes its request reference, original RPC/thread/turn/call,
  tool, workspace handle, application generation and model revision.
- Initial host binding must match the captured workspace/generation/revision,
  as well as completion matching the original binding. A caller must not be
  able to retarget the captured binding by mutating its input object.
- Correlation refusal after mutation admission is not evidence of nonexecution:
  preserve actual applied/unknown standing. Turn interruption is not rollback.

The counterpart explicitly concurred with the initial-basis binding check.
The App specimen previously checked completion correspondence but omitted initial
binding-to-basis admission. The repair validates the captured basis schema,
requires the catalog's complete binding field set, checks initial workspace,
generation and revision with exact types, rejects empty request/thread/turn/call/
tool identity and invalid RPC identity types, and keeps immutable copies.

Verification: ten standard-library offline tests passed in 0.015 s under a
fresh mktemp Codex home; git diff whitespace check passed. The two new tests
cover initial mismatches/missing identities and caller mutation after capture.
The original eight projection, native-intent, unit, limit, withheld-value,
domain-error and completion tests remain passing. No Cargo, npm, GUI, supplier,
model, server, download, credential access or broad suite ran.

This remains a specimen, not production ingress or a general validator.
No persistence/permission runtime changes occurred. Production bridge admission,
resource bounds, cursor/run ownership, interruption/application races and recovery
still require host tests and independent permissions/persistence scrutiny.
DEL-09-06/09-07 ScopeOfWork and deliverable.yaml commitments are unchanged:
the repair supplies no joined live witness, qualification or acceptance.

## Remaining receiving inputs

The receiving checkout/revision/catalog hash are now verified above. Independent
SWBPIPE review, Agent 0 confirmation and main integration remain unestablished.
The actual harmless roundtrip additionally needs the exact
supplier executable/schema hashes, oMLX version, model identity/artifact hash,
endpoint/configuration and observed tool-call/result/follow-up transcript.
Installation or selection alone does not establish tool isolation. The full
reference-system and same-run host traffic obligations remain separately
evidenced; W9-A remains development evidence only.
