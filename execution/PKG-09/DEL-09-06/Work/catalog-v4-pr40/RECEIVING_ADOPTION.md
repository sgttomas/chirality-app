# PR40 workspace/hash receiving successor

This explicit source selection receives SWBPIPE PR40 actual merge
`cc91aadc9822c5c1d8ba3d883a3ee220dddc1b65`, checked head
`57f5028328bfa50b0a525b7186926a9da88979dc`. The first parent is
`bff8284ce6b14a75e5a046961235f20536e0975a`. App's PR27 and PR30 profiles remain
unchanged and separately inspectable; no previous fixture, source revision or
reported live outcome is relabelled.

[The PR40 profile](../../../../PKG-03/DEL-03-02/Work/swbpipe-catalog-v4-pr40-pins.json)
hashes to `e80f88f2098ff85860f4b6370bdb0e2707c0e9266e5644eae939f0d981f75569`.
Its nine source entries carry repository-root paths, sizes, hashes, snapshots
and actual read extents. Each was fetched and verified at the integrated commit.
The unchanged canonical and packaged catalog (50,864 bytes, `8e9a4b4e…`),
host contract (53,811 bytes, `40b64f05…`) and imported formatter (7,889 bytes,
`d7b2f992…`) reuse existing byte-identical snapshots with the PR40 publication
reference; this is explicit new correspondence, not inferred currency.

## Changed source and inspected evidence

| Source suffix | Bytes | SHA256 | Read extent |
|---|---:|---|---|
| `services/embeddedAgentSession.ts` | 33,980 | `732dba10c224b102e8da9ffb43476a2d0067d778edc7dc47f12305ad11227a1e` | 29–48, 192–198, 221–227, 240–266, 297–344 |
| `features/workspace/workspaceSession.ts` | 205,070 | `97dd3f1908ed733d99498a921b2be37d6513f048122db980eb8db5b95f90d009` | 350–374, 686–711, 3998–4035 |
| `Work/agent-live-session.md` | 16,928 | `334689dd04ebafececedadee45fc343258831c3f05f190976727070007523c1b` | 133–169 |
| `features/workspace/agentWorkspaceSnapshot.session.test.tsx` | 5,230 | `271f5e9075581af815a1c28b3d6e42045466ffd31164f4364764770fdf834bd9` | Full regression source |
| `services/embeddedAgentSession.test.ts` | 24,930 | `7b9ebc151459edb3915585443b4aea79b588780d53281c8e380621dd89a78601` | 1–72, 101–108 |

Full-file hashes identify bytes; unread portions are not wholesale adopted.
The host tests were inspected, NOT executed by App. Their assertions cover Start
past readiness after load/edit, unavailable pending hash and undo-before-render,
strict forms/refusals, registration/basis updates, engine batch validation,
catalog-form applied outcomes/proof and retained solve basis after live edit.
The live account reports previous Start/register refusals. App did not observe
those runs and does not infer successful Start or invalidate earlier offline
fixture evidence because those runs exposed host integration defects.

## Exact boundary meaning

`agentHash` converts only engine `sha256:` followed by 64 lowercase hex digits
to the catalog's bare 64 lowercase hex value. It preserves all other evidence
metadata. `catalogHash` validates a supplied bare catalog value and returns it
unchanged: it is NOT a reverse converter and does not insert a prefix. Invalid
forms have distinct `AGENT-ENGINE-HASH-FORM-REFUSED` and
`AGENT-CATALOG-HASH-FORM-REFUSED` refusals. There is no permissive prefix stripping,
uppercase normalization, guessed digest or source-revision rebinding.

Registration and updated basis use `agentHash`; current-basis comparison validates
the catalog side and compares it to converted workspace evidence. Proposal
`source_model_hash` remains `snap.hash.value`, and `validateOperationBatch` keeps
`snap.hash` in engine form. Applied proposal outcomes and solve receipt/output
hashes cross through `agentHash`. Retained result pages use the captured
`run.basis.modelHash`, already catalog form; they are not relabelled to the
current edited model. Null/unavailable outcomes are not manufactured hashes.

The workspace records `modelRevision.current` when computing a hash. Publication
requires the existing generation/UI-revision ownership checks AND that recorded
computed-for revision equals the live `modelRevision.current`, plus the existing
render-generation/live-generation correspondence. The UI revision and model
revision are different counters and need not equal each other. Pending hash or
an undo/edit that advances the model revision must not publish an older hash.
App does not implement the workspace, React lifecycle, hash computation or Start.

## Minimal App receiving work

A separate source loader verifies this fixed profile and all nine inputs. A small
offline evidence-correspondence helper checks supplied engine/catalog pairs,
unchanged metadata, engine batch/validation evidence, revision-owned snapshot
publication and retained result basis. It does not compute model hashes or
convert catalog values back to engine values. Invented tests join those checks
to the unchanged v4 `Pending` receiver, whose catalog-schema/basis protections
remain. Missing, tampered, mixed-profile and prior-session substitutions refuse.

The previous v4 behavior, table/schema/tool list, byte limits, source profiles
and original/v2/v3/PR27/PR30 evidence remain unchanged. No native command, runtime
module, supplier build, model invocation, property applier or unrelated pin
cohort is modified. Normal tests use only retained App files and prepared Python;
no sibling checkout or source download is a runtime prerequisite.

DEL-09-06/09-07 requirements and dependency conditions are reconciled by inspection:
this is an explicit receiving implementation of existing binding duties, not a
new acceptance criterion. Their code/check declarations identify the additional
loader/evidence checks. The parent-owned execution account remains untouched.

A future actual live candidate must include these fixes or establish equivalent
source applicability. This successor is source/schema/evidence correspondence,
not live/native/Apply/W9-A/criterion17 qualification, acceptance or release.
Actual candidate/configuration/model, source-to-artifact binding, admitted session,
review/Apply and result/run/traffic/recovery evidence remain separately owed.
