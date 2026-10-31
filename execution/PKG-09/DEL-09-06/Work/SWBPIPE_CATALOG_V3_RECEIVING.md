# Integrated SWBPIPE catalog v3 receiving

App explicitly receives `sgttomas/SWBPIPE` PR15 at actual merge
`4d8cb7b0c8f101d5102813e634e23ecba29b310e`, from checked head
`aa62c3dc7bf14d50b925a1b480ff54fb1b8bf3c2`. Both repository-root paths were
read in full from that immutable integrated source:

- `execution/PKG-16/DEL-16-06/Work/agent-capability-catalog.json`
- `apps/desktop/src-tauri/resources/agent-capability-catalog.json`

Each is 61,618 bytes, SHA256
`652ccc0c25263a01ce103a8a7a3e64a7c01833b0588dcbc054ad461301b810ec`.
The exact canonical bytes are retained at
[catalog-v3/agent-capability-catalog.json](catalog-v3/agent-capability-catalog.json),
not reauthored or treated as a second evolving catalog. The source selection and
read extents are in [DEL-03-02's versioned pins](../../../PKG-03/DEL-03-02/Work/swbpipe-catalog-v3-pins.json).
SWBPIPE owns the tool list, catalog and host implementation. The catalog's own
`design_contract_not_live` standing and historical embedded provenance remain
unchanged; the receiving selection separately identifies the actual merge.

## Received interface and strict fixture behavior

The same six tools remain. `swbpipe_propose_operations` is still proposal-only;
there is no Apply, acceptance, release or permission tool. The agent supplies
only `operation_id`, `operation_kind`, `target`, `change` and `rationale`.
Host-owned attribution, status, queue, source, validation, audit and professional
boundary fields are refused, including at nested target/change and proposal
object boundaries. Agent-supplied `author_type=agent` or `operation_status=proposed`
is refused too: truthful-looking values do not transfer their source actor.

The nine fixed intent branches are:

| Operation / target | Change / field path |
|---|---|
| modify / Node | set_field / position.x, position.y or position.z |
| create / Material | create_material / materials |
| create / Node | create_node / nodes |
| connect / Element | connect_pipe_run / pipe_segments |
| create / Support | create_support / supports |
| create / Load | create_load_case / load_cases |
| create / Load | create_primitive_load / primitive_loads |
| modify / Load | update_load / pressure_regions |
| modify / Model | set_field / pressure_profile |

Deletion, components, bend insertion, library records, combinations and general
model settings have no admitted branch. Crossed discriminators, missing fields,
wrong types and bounds, duplicate JSON keys, ambiguous operation ids and
host-only field injections refuse. Batch limits and required bounded referential
assumptions remain. Existing initial/captured basis, stale/live and retained
record joins, generation/workspace/handle correspondence, duplicate/detached
completion and result withholding checks remain.

The old coordinate-only fixture checked every intent against project length.
The explicit v3 path retains that equality for Node position edits, while new
branches use their exact schema constraints. `none`/dimensionless branches and
stress/primitive-load branches are no longer incorrectly treated as coordinate
edits. Descriptive guidance is never parsed into a unit policy or operation
permission. Native applier validation of payload JSON strings, dimension/unit
consistency, object existence, batch order and semantic feasibility remains
SWBPIPE-owned. SWBPIPE Agent 0 confirmed no counterpart mismatch for this
boundary on 2026-10-31: applier checks are authoritative; unit descriptions are
guidance, and a future binding catalog-level unit rule requires a new version/hash.
These receiving tests do not mint full native intents, queue a
batch or simulate a person's Apply. A schema-valid `after` string is not a
native-valid operation.

Summary requires `projectId`, `schemaVersion`, `pressureContract` and
`pressureProfileBefore` alongside existing context. `read_results.filter` is
optional; when supplied it requires bounded unique `kinds` and `entityRefs`
arrays. Input validation and retained-run correspondence are checked here.
Actual row filtering, cursor-to-filter/basis/run ownership and permitted-view
coverage require host evidence; descriptions are guidance, not authority.
The fixture schema evaluator rejects unsupported keywords while permitting
textual `description`; all twelve expanded input/output schemas are also checked
with JSON Schema Draft 2020-12. No protocol, native ingress or custody code changes.

## Identity separation and verification

The original App proposal remains `e1e3f4615b6f766b313c3492506f68254afd8a06` /
`64aad707acd1d409f3d255381fc597e2ee74e7a4d048aadc5382414d63c64f8c`.
Historical v2 remains `sgttomas/chirality@c48efef77bbb799f3ebe902eb213a88330a5994e`
at its original `projects/chirality-piping/.../Design/` path, SHA256
`fe1439998d709e5f3e9641a4d39567000ced56c498fab5b6b8f2028df7c9f669`.
The prior receiving test is retained byte-for-byte as
`catalog-v2/receiving-test.py.txt`, with its explicit v2 export
requirement (execute with `PYTHONPATH=app/supplier_checks python3` and an exact
v2 `--catalog` export). No historical v2 export was reacquired or executed in
this adoption; origin regressions were rerun. The 84-case operation corpus and its original pins/mapping remain
historical inputs; catalog adoption does not refresh or requalify that corpus.
New pins alone use `sgttomas/SWBPIPE`, repository-root paths and `Work`.

The current receiving loader pins both selection bytes and catalog size/hash.
Old, unknown, altered, absent and oversized catalog inputs refuse; neither an
origin/v2 record nor a relabelled catalog supplies current v3 identity. Ordinary
checks use the retained exact snapshot and need no sibling checkout or network:

```sh
python3 app/supplier_checks/swbpipe_projection_test.py
python3 app/supplier_checks/swbpipe_receiving_test.py
```

An explicit `--catalog <export>` is checked against the same integrated identity.
All receiving events/actors/material are invented. The tests establish offline
source/schema/correspondence behavior only, not live execution, an actual human
act, supplier isolation, criterion 17 qualification, acceptance or release.

## Remaining live evidence

SWBPIPE owns the planned oMLX W9-A build/solve/report witness and supplies its
exact plan/resource profile, integrated host candidate and artifact identity,
provider/model configuration, admitted session/basis, immutable proposals and
assumptions, displayed review, person's actual Apply, resulting model/hash,
solve/run identity, permitted filtered result pages and actual report. Preserve
failed/blocked/unknown outcomes and host-owned transport/domain joins. App's
parent coordinates model time and the owner act; this receiving lane neither
schedules nor duplicates it. W9-A remains development evidence; criterion 17
still requires criterion 1's full reference system. Native lifecycle/isolation,
stale/interruption/recovery, same-run traffic and remaining dossier/acceptance
obligations keep their separate evidence requirements.
