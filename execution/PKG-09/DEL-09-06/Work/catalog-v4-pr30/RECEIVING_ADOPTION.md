# PR30 catalog-v4 source-binding successor

This contribution explicitly selects `sgttomas/SWBPIPE` PR30 actual merge
`a659523a75dbbf2cdfcccdf8a667b6fb482e10ea`, checked head
`0c729ce5d09636341521f117e075d1a8d07acf32`. It is an App source-binding contribution
for review/integration, not a statement that this App change has already merged.
The behavioral v4 adoption in App PR44 remains at its actual PR27 source
`9b6281e7eaca924e6166336b87b6d25937c1ca04`; all original/v2/v3/PR27 artifacts,
readers and pins remain unchanged.

[The separate profile](../../../../PKG-03/DEL-03-02/Work/swbpipe-catalog-v4-pr30-pins.json)
has SHA256 `74f2b33ba5e35494704bea24f1ab1752ff2d6198a955b4ec8e4b75d80c297ca3`.
The new loader is `app/supplier_checks/swbpipe_catalog_v4_pr30_receiving.py`.
It requires that exact profile and every selected source's bytes/hash; failure
never falls back to the historical PR27 selection. The PR27 loader still uses
its own original profile. Equal catalog bytes do not make these profiles or
producer subjects interchangeable.

## Exact integrated sources and read extent

| Repository-root source | Bytes | SHA256 | Substantive read extent |
|---|---:|---|---|
| `execution/PKG-16/DEL-16-06/Work/agent-capability-catalog.json` | 50,864 | `8e9a4b4e3eec027d092033ea5d95f1648030520e797c5a660ab387531f23be17` | Full catalog; unchanged |
| `apps/desktop/src-tauri/resources/agent-capability-catalog.json` | 50,864 | `8e9a4b4e3eec027d092033ea5d95f1648030520e797c5a660ab387531f23be17` | Independently fetched, full-byte correspondence to canonical |
| `execution/PKG-16/DEL-16-06/Work/embedded-agent-host.md` | 53,811 | `40b64f0544431c16b10645d0ad69adf0b7f81522be6e82e7dbc78eb190a2766c` | 124–131, 234–261, 352–361 |
| `apps/desktop/src/services/embeddedAgentSession.ts` | 32,813 | `fa33d85e40b41d8acab10bf7d26c797449524f703eee09bdc9a960836badcf26` | 1–12, 28–38, 63–100, 101–130, 187–197, 221–278 |
| `apps/desktop/src/features/model-tree/removalIntents.ts` | 7,889 | `d7b2f9927daa1a4701655be9185919cc1ea062567f9f0b1b90377f9f4b8f5c5f` | 1–115: type-only import, shared formatter implementations and inspector call sites |

Exact snapshots and source sizes/hashes were verified from the integrated
commit during read-only intake. The unchanged catalog snapshot is reused by
path, with its PR30 publication identity recorded separately. Full-file hashes
establish byte identity, not substantive adoption of unread content. Ordinary
checks require only retained App files and prepared Python/Node, never a sibling
checkout or source fetch.

## Copy-to-import correspondence

The session now imports `nodeDeletionSummary`, `pipeDeletionSummary` and
`supportDeletionSummary` from `../features/model-tree/removalIntents`. Its own
number formatter was removed. The shared `applierDisplayNumber` uses the same
integer-below-1e15 branch, `String` conversion and exponent expansion as the
previous copy. Shared summaries trim the same label/endpoint/material fields.
The session preserves the same blank-label/endpoint/material checks and finite
three-coordinate check, so missing deletion text stays unavailable rather than
being synthesized by App.

`recordBefore` and all producer bytes following it are identical to the PR27
source, apart from line relocation. Thus component/support canonical before
construction, stamping, units, complete-result serialization/error handling,
cursor binding, basis checks and page/filter logic are unchanged. Host prose
only adds the fact that the inspector and session use the shared formatters.
No catalog table/schema/tool change, native command, modifier capability,
unit conversion or error-policy expansion is introduced.

The old M2 correspondence-test source is retained in the successor manifest as
an explicitly historical citation at `9b6281e7`, outside the PR30 selected-source
list. Its bytes were not reacquired at PR30 and no claim is made that its import
or assertions are unchanged there. Neither its old pass nor the new source
comparison is a new App/host native execution or applier qualification.

## Verification and scope reconciliation

The new source tests check exact publication identity, equal catalog/different
profile meaning, every missing/tampered dependency (including the new formatter),
old-producer substitution and mixed-profile refusal. Focused existing before,
cursor, serializer, Unicode-page and drift tests are reused with the explicitly
selected successor catalog. The ordinary original/v3/v4 suites remain intact.
CI adds the successor check alongside the previous version checks, never replaces
them. Applicable PR44 evidence is reused at its actual subject; no independent
review or run is relabelled as a PR30 execution.

DEL-09-06/09-07 ScopeOfWork and dependency obligations are reconciled by inspection:
only source selection changes, not their required behavior, acceptance, evidence
or owner boundaries. Code/check declarations identify this additive consumer;
no governing requirement needs rewriting. The parent authorized only the
catalog-receiving paragraph in CURRENT_EXECUTION_BASIS; surrounding terms and
publication/native obligations remain unchanged.

A future live subject using PR30 must cite this source identity and its actual
candidate/runtime evidence. This contribution supplies no live/native run,
model call, person's Apply, W9-A/criterion17 qualification, acceptance or release.
Parent owns the App merge. No unrelated admission/terminal/S4/package pins or
production modules change here.
