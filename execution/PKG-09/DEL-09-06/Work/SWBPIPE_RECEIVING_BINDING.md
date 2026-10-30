# SWBPIPE receiving source and admission correspondence

## Current fixture admission and remaining activation boundary

This subsequent receiving update preserves the merged host basis below. It
receives committed fixture evidence, not a product-profile merge or activation.
At host `cc436e9fcf5a96e6a0d79336497817de129f1a5e`,
[`agent-libinfo-elimination.md`](https://github.com/sgttomas/chirality/blob/cc436e9fcf5a96e6a0d79336497817de129f1a5e/projects/chirality-piping/execution/PKG-16/DEL-16-06/Design/agent-libinfo-elimination.md)
has SHA256 `7edb2afec07e39c55f76e7b63638c08aab3892046c5e70840d3928b8a0c71361`.
It records the following distinct observations and dispositions:

| Source | Received observation | Limit |
|---|---|---|
| `26c5b24e59efbb351038791fb4d7b27da0a87e3e`, executed source `ee81da5261e18d5500734120a2070bb037adcd25` | Resealed A+sys preflight: three C EPERM outcomes, Rust 14/14; no-tools A refused with `configuration_load_error`, A+sys accepted | No turn/inference/tool compatibility or EOF/crash case. Both overall case verdicts remain false because app cleanup acknowledgments were unconfirmed |
| `68707f5d517e01d3a5bbf9f651edec72cca201ff` | Later owner-authorized removal of those two stopped-scope runtime/marker pairs after App confirmed no dependency | Original result unchanged, SHA256 `a354dad943aeeafd5e9b5f88282feda998e15fac8f4bd05ec0dff9e10650d286`; separate cleanup record SHA256 `62e210d3f15b3c0f4b4d2788a48cd87691a8ea8d7920b5bfd147967361e63a72` records no PID signals. Artifact deletion supplies no missing acknowledgment or lifecycle proof |
| `0a70e5d42fd2a1223b0e7ce2f81c523bb58ed46e` | Synthetic-identity no-tools diagnostic under plain A also refused; no config snapshot | No allow was added; denied lookups alone establish neither cause nor necessity |
| `a87121f993c832e4296ca839f9ec406c577acda9`, executed source `fa9416939ed648636d4ef314b89fc090ea1dd93b` | Exact reviewed A-plus-single-libinfo candidate: C three EPERM outcomes and Rust 14/14, then accepted no-tools `thread/start` with matching loaded configuration | No oMLX, model, keychain read, tools, turn or EOF/crash test. Overall verdict remains false: supplier scope stopped through deliberate anchor cleanup, app acknowledgment unconfirmed |

The last candidate adds only
`(allow mach-lookup (global-name "com.apple.system.opendirectoryd.libinfo"))`;
normalized profile SHA256 is
`be2fe1d54fcc5c60a00ed7d304bf2e4c4885d662d84bfe5a9c7fe6ff9c6f4d7c`.
It is not the A+sys import and does not combine synthetic-identity settings.
The loaded snapshot matched provider/model, private cwd and approval/sandbox
policies. Newly observed `/dev/autofs_nowait` and `/dev/dtracehelper` reads stay
denied under the host Agent 0 disposition; success did not require allowing them.

Independent review of the exact old/new proposal found no confirmed defect.
Host Agent 0 subsequently selected it for fixture qualification, retaining the
directory-broker limitation and reopening review if directory binding changes.
This is not owner risk acceptance for production. The host owns the exact
product-profile PR, its integration, remaining native cleanup/isolation proof
and activation decision. No App implementation prerequisite is identified.
Canonical Design/runtime catalog objects still equal the existing receiving
pin; no repin or catalog/schema test rerun is required.

The next App receiving check is the
[first actual desktop trace](../../DEL-09-07/Work/SWBPIPE_RECEIVING.md#first-desktop-trace-receiving-checks),
after the host establishes the native route. The exact proposed acceptance
staging in App PR #14 remains unadopted; this update changes no requirement.

## Current joined receiving basis (2026-10-29)

Merged host/source baseline received with App PR #14; later fixture evidence
and its activation limits are above.

App receiving basis: merged PR #11, App
`c5b33e37832364eaa04360540ea5e31bc08a9168`. Read-only inspection of the
selected SWBPIPE contribution checkout's committed objects establishes the
following source basis in `sgttomas/chirality`. No dirty host files are received.

| Contribution | Exact merged source | What the App receives |
|---|---|---|
| #1732, RT-E1 and criterion 17 | `541446a9f16e4e020a5703cda76e7fb94fbec819` | Owner-approved release target; criterion 17 builds, solves and explains criterion 1's reference system |
| #1736, catalog and host Design | `31084e1f792b0612013e508b30e2a5dabdc151e7` | Canonical catalog v2 and host-owned integration contract |
| #1738, harmless local-model witness | `4d80a3fb51dee1f7203d643338a75168442e0cb5` | Maintained source and reported actual summary call/result/follow-up, with bounded denial observations |
| #1747, Rust components | `f35601a16fc5de26c2571abc8ef775d10622fe80` | Catalog/schema validation, bounded framing/protocol and gated macOS custody components; no live desktop route |
| #1753, portable transport/session components | `f1161705823e003df630db455aa2ea227f38e666` | Stdio pump and host-driven session driver; live coordinator, webview bridge and completion ingress still absent |
| #1755, invented test-path repair | `3a4fa55369be67940b4d1de707b2bad8159dc0bd` | Inspected main snapshot; test placeholder repair, no new runtime capability |

Paths below are relative to `projects/chirality-piping/` at that last snapshot.
The canonical `execution/PKG-16/DEL-16-06/Design/agent-capability-catalog.json`
and generated `apps/desktop/src-tauri/resources/agent-capability-catalog.json`
both hash to `fe1439998d709e5f3e9641a4d39567000ced56c498fab5b6b8f2028df7c9f669`.
They equal the existing receiving pin `c48efef77bbb799f3ebe902eb213a88330a5994e`;
no repin or repeated catalog/schema suite is warranted. The App origin remains
`64aad707acd1d409f3d255381fc597e2ee74e7a4d048aadc5382414d63c64f8c`.

The committed [local witness account](https://github.com/sgttomas/chirality/blob/3a4fa55369be67940b4d1de707b2bad8159dc0bd/projects/chirality-piping/execution/PKG-16/DEL-16-06/Design/agent-local-witness.md)
(SHA256 `b3923ac169543472405f8314c604c3b382558ad3ff31d925a47889805dad19cc`)
reports one actual local-model `swbpipe_read_model_summary` call with invented
host-generated handle/count returned in the model's follow-up. Its
[`agent-witness-pin.json`](https://github.com/sgttomas/chirality/blob/3a4fa55369be67940b4d1de707b2bad8159dc0bd/projects/chirality-piping/execution/PKG-16/DEL-16-06/Design/agent-witness-pin.json)
(SHA256 `c4f096777262711a3e38a4691988362a1ac955f07d32400249efba848915550b`)
binds official stock Codex 0.160.0, oMLX 0.6.4/build 2529 and
`mlx-community/Qwen3.6-35B-A3B-8bit`, including archive/binary/model digests,
sizes and configuration. This is received host execution evidence, not a new
App execution or independent reconstruction of raw exchanges. Its pin file's
`pin_not_live_witness` label describes the pin artifact; the separate witness
account describes the observed run. The four denied-tool turns and native
component probes retain their stated limits; they establish neither universal
supplier isolation nor complete same-run host traffic evidence.

Source inspection of `embedded_agent/mod.rs`, `session_driver.rs`, `macos.rs`
and the host Design confirms that no product start control, live domain
dispatcher, webview model binding, completion command or panel is established.
The passing Python witness's profile is not the Rust launcher's activation
proof. Separately, unmerged fixture commit
`d08bb9b656a5b2eaedcc9c7af45d9159c57f85ec` records aligned no-tools and
summary-only thread admission failures (`configuration_load_error`) under the
restricted fixture profile. No turn/inference ran in those cases; they do not
disprove the earlier local witness, justify a catalog-schema change or establish
a fork requirement.
The host owner retains that investigation, native EOF/hard-death cleanup,
credential diagnostics and activation decisions. No fallback is selected here.

**Receiving gap addressed here:** a current, source-bound receiving and
applicability account joining these sources to DEL-09-07 and the release packet.
This Design repair supplies that account and
[the qualification receiving map](../../DEL-09-07/Work/SWBPIPE_RECEIVING.md).
No App runtime adapter defect or missing standalone external controller is
established by these sources. No App implementation prerequisite is needed for
the current host fixture. Existing v2 specimen coverage remains applicable
to the unchanged catalog; runtime host conformance is still owed by SWBPIPE.
New host interface bytes or evidence require affected receiving verification,
not silently following a mutable host branch.

## Publication verification (2026-10-29)

Historical PR #11 publication checkpoint; current host evidence is above.

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

At the v2 receiving checkpoint, the counterpart reported twelve expanded
standalone schemas, passing lint and independent review confirming the commitment
wording at ce6729f3. Agent 0 wording confirmation was requested through
[draft PR #1736](https://github.com/sgttomas/chirality/pull/1736).
That checkpoint was a received review account, not an App independent permissions
review, merge, confirmation or runtime adoption. Subsequent merges are bound in
the current basis above. No interface objection remained to the resolved slice.

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

## Remaining joined inputs

The current basis above supersedes earlier pending-review, pending-merge and
pending-harmless-roundtrip statements. SWBPIPE still owes the activated desktop
route, actual proposal review/application and truthful stale/interruption/outcome
evidence, native cleanup/isolation and full reference-system capability.
DEL-09-07 still needs candidate-bound local journey, durable evidence joins and
complete same-run traffic/native-enforcement observations. The
[receiving map](../../DEL-09-07/Work/SWBPIPE_RECEIVING.md) assigns these inputs
and identifies acceptance reconciliation reserved to the owner. W9-A remains
development evidence only. Source receipt does not qualify either product.
