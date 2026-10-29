# SWBPIPE receiving source and admission correspondence

## Origin and receiving standing

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
