# Catalog proposal and offline witness preparation

Standing: original App-side preparation, 2026-10-28; no live witness in this file.
Later SWBPIPE adoption and v2 checks are recorded in
[the receiving account](SWBPIPE_RECEIVING_BINDING.md). The observations and open
inputs below retain their original preparation basis, not current host status.
SWBPIPE_CATALOG_PROPOSAL.json is the single source offered for SWBPIPE adoption.
The Python specimen reads that file, not another catalog. Copying the JSON
requires no App runtime or sibling checkout. Expand catalog-local schema
references before publishing standalone MCP-style descriptors or dynamic tools.

The assignment's integration-proposal input had SHA256
7d6dd0a0c3b11bb8ec14394ae890de0cf3c6a239aed9b55d01ef03c38b9117ab;
its exact copy is preserved in contribution commit
e1e3f4615b6f766b313c3492506f68254afd8a06 at SWBPIPE_CODEX_INTEGRATION.md's
repository path. The current proposal may carry later owner steering; those
edits do not rebind the original witness input. Execution steering was read
from the parent at dispatch, SHA256
0a33bbba6a898ed22a801db48267fbb85b2a0b2638f298a01f2f1db401b06e90.
Neither copy nor consultation updates bundled product instructions.

## Source and interface reconciliation

Shared role/method source: /Users/ryan/dev/chirality, WORKING_ITEMS and
coordinated-knowledge-work, at 1560bbf7f7add4637a20572a2b0d404ef121af63.
SWBPIPE source was consulted read-only at that same pin. Paths below are
relative to projects/chirality-piping:

- apps/desktop/src/types.ts: PreviewModel, EditorOperationIntent,
  ModelHashEvidence, MechanicsResult.
- apps/desktop/src/features/workspace/workspaceSession.ts:
  registerOperationBatch, handleRunOperationBatch, handleRun, session events,
  revision gates and model hash own the live model/review/run state.
- apps/desktop/src/services/operationBatchService.ts: native batch validation
  and application take model, batch and claimedModelHash.
- core/model_operations/operation_applier/src/lib.rs, Node field rules:
  position.x/y/z use UnitSource::ProjectUnits("length").
  schemas/model.schema.yaml describes stored global Cartesian positions in
  project.units.length. Metres are a fixture choice, not universal storage units.
- apps/desktop/src/features/results/resultReader.ts and
  features/result-export/csvTable.ts: result standing, units, exact decimals
  and withheld/status cells are existing host concerns. The bounded projection
  must use permitted view/value semantics, not expose raw private rows.

SWBPIPE HELP_HUMAN reviewed the first proposal and required native operation
intents and a separate orientation call. Both are incorporated. Its naming
review raised no other objections; adoption of these revised bytes is unclaimed.
The native discriminators are operation_kind, target.object_type,
change.change_kind and change.field_path: no parallel kind field is added.
Slice 1 admits only Node coordinate set_field intents. Future kinds add native
subschemas to this one proposal tool. The host constructs the enclosing
OperationBatch and stamps correlation; agent-supplied IDs/source/validation
strings are untrusted metadata.

Batch count is host configuration returned by summary, not a schema constant.
JSON limits are fixture/default values, not permission to increase production
budgets. Rust applier semantic validation still checks before-state, exact
document-unit match and finite values. Native before/after are strings, as in
the actual intent type; the schema does not assert their semantic validity.
Summary admitted-kind tokens describe capabilities, not an argument language.

The bridge must check claimed hash before registerOperationBatch: that existing
function snapshots the current model itself, so blindly calling it would rebase
an old proposal. Model revision/generation/hash are rechecked on completion;
run/state IDs may legitimately advance after a solve. Observe reports original
proposal basis separately from current basis. Correlation refusal during a
mutation must preserve its true outcome as applied/unknown in host records,
not claim nothing happened. Restart recovery is absent from this specimen.

DEL-09-06 ScopeOfWork REQ-001/005/007, AC-003/005/007 and deliverable.yaml still
require actual coordinated input/adoption and joined execution. DEL-09-07
REQ-002/003/005/006/007 and AC-002/003/005/006/007 still require specific live
operations, durable outcomes, autonomy and network evidence. This proposal
changes no acceptance or dependency condition; those files are unchanged.
It does not fulfill direct-autonomy, row-acceptance, workflow-roundtrip or
complete-traffic claims. Agent 0 must reconcile later owner-confirmed commitment
changes in their owning documents. RT-E1/criterion 17 remain draft PR #1732.
W9-A is only a development witness; criterion 17 uses criterion 1's W-17/O-1
full reference system. This operation subset cannot yet build either system.

## Offline check and limits

Run only this small standard-library check after inspecting its source:

    scratch_codex_home=$(mktemp -d /tmp/swbpipe-offline.XXXXXX)
    CODEX_HOME="$scratch_codex_home" PYTHONDONTWRITEBYTECODE=1 python3 app/supplier_checks/swbpipe_projection_test.py

Observed here: 8 tests passed in 0.009 s using a fresh scratch Codex home;
staged diff whitespace check passed. No live or broad check was run.

No supplier subprocess, model, server, Cargo, npm, GUI, network, credential read
or sibling checkout is used. Fixtures are invented in the test file.
Checks cover expanded declarations against supported pinned protocol fields,
contentItems/inputText/success, request identities, duplicate completion,
changed generation/workspace/revision/hash, missing/wrong solve claim,
page/byte limits, malformed arguments and withheld-value protection.
Domain rejection yields success=true with explicit rejected standing;
only execution_error yields success=false. Neither claims successful mutation.

The fixture evaluator supports only the keywords used here; it is not a
production JSON Schema validator. Production still needs full Rust validation,
pre-allocation admission, bounded producers, handle lookup/expiry, concurrent
call quotas, cursor/run binding and serialized interruption/apply admission.
These are specified policy, not established by this Python oracle.
No persistence, permissions or runtime ingress changes occur here.
Before a real bridge is integrated, Agent 0 should arrange independent scrutiny
of command_ingress/reach changes, session isolation, persistence, interruption
races and outcome recovery, with targeted host regression checks.

## Candidate inputs and actual observations still required

Public repository inputs identify candidates, not installed availability:

- App generated schemas: app/src-tauri/resources/supplier/0.160.0/ and its
  MANIFEST.sha256.
- Stock macOS arm64 package provenance:
  app/src-tauri/resources/distribution-reference/distribution-s1/references/codex-0.160.0-macos-arm64/
  acquisition.json, expected.json, custody.json and extraction.json.
  Recorded candidate: @openai/codex@0.160.0-darwin-arm64,
  https://registry.npmjs.org/@openai/codex/-/codex-0.160.0-darwin-arm64.tgz.
  No artifact search, download, install or executable launch was performed.
- app/supplier_checks/records_delivery.py supplies a capture-only local
  provider/LM Studio pattern; it was not run and is not a real-model witness.
  Its fixture endpoint is not a selected real server. Exact installed server
  version, model file/hash/quantization, context settings, endpoint and available
  authorized binary path remain required owner/host inputs.

After owner authorization for live load, bind executable hash, schema hash,
server/model identities, host revision, catalog hash, configuration and date.
Use a fresh scratch Codex home and empty agent cwd. Retain these observations:

1. Start stock app-server over private stdio with experimental dynamic tools.
   Capture actual model-visible definitions and an actual model-generated call,
   including arguments and thread/turn/call/RPC identity. Return a fresh invented
   nonce/value and observe a follow-up answer grounded in it. Tool listing,
   greetings and provider-request capture alone do not pass.
2. Through the live webview, summary/read, native proposal, actual human
   rejection and acceptance, observe, solve and results retain original,
   evaluated and current bases plus run standing. Test intervening edits, wrong
   workspace/generation, duplicate/unsolicited completion, stale page/run handles,
   native-invalid intents, unit mismatch and oversized data. Verify no duplicate
   apply, pending withdrawal versus apply-winning interruption, and truthful
   unavailable/unknown outcomes after session loss.
3. Probe built-in shell, patch/file-write, arbitrary file read and network escape
   with invented canaries only. Put the outside-cwd read canary in an authorized
   scratch sibling, never a credential or private host file. Record actual deny
   or allow responses and independent sentinel/network effects. Empty cwd,
   prompts, selected provider, read-only setting and stdio alone do not prove
   privacy/destination isolation. An unattempted probe is inconclusive.
   All-host traffic remains DEL-09-07's same-run obligation; loopback probes
   cannot replace it.
4. Keep turn interrupt separate from solve-job cancellation; verify panel
   progress and final health with actual native invocation. Do not invent a
   streaming dynamic-tool channel. Full MCP transport is not included; its
   stateless 2026-07-28 envelopes/input-required behavior need separate work
   if adopted.
5. Use W9-A for development and the complete W-17/O-1 reference system for
   criterion 17 after admitting remaining native operation kinds. Observe local
   model capability; no hosted substitution or formal qualification is authorized.
   Focused owner UI conversations precede substantive UI design.

No live driver is offered: an executable opt-in run needs exact authorized
binary/server/model and isolation configuration first. This specimen and list
prepare that run without starting a supplier or implying local configuration
alone enforces isolation.
