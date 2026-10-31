# Integrated catalog-v4 receiving selection

The explicit v4 reader selects `sgttomas/SWBPIPE` PR27 actual merge
`9b6281e7eaca924e6166336b87b6d25937c1ca04`, from checked head
`2cd052e6746aa4404f852a39d8630b70fabf696c`. The earlier candidate
`15e40a07…` remains preparation history in `RECEIVING_PREPARATION.md`; its old
52,622-byte prose and line numbers are not silently used as current authority.

[The versioned selection](../../../../PKG-03/DEL-03-02/Work/swbpipe-catalog-v4-pins.json)
binds five independently fetched integrated sources:

| Source | Bytes | SHA256 |
|---|---:|---|
| canonical Work/agent-capability-catalog.json | 50,864 | `8e9a4b4e3eec027d092033ea5d95f1648030520e797c5a660ab387531f23be17` |
| packaged resources/agent-capability-catalog.json | 50,864 | `8e9a4b4e3eec027d092033ea5d95f1648030520e797c5a660ab387531f23be17` |
| Work/embedded-agent-host.md | 53,735 | `6342146e130b67e8ecd2b9ebee311dde6a665370d7771f2ce4e862d0cbb7003c` |
| apps/desktop/src/services/embeddedAgentSession.ts | 33,432 | `d766442debf2e49bff3b2e45da9013828e324e4b97824639b9224006b0230492` |
| apps/desktop/src/services/embeddedAgentM2.test.ts | 8,878 | `f4a78e9a634fc0fd177f63d360d82e4f4f8c548e3735f2054695d1524c22b478` |

Full repository-root paths and actual read extents are in the selection. Catalogs
were read in full; the host contract was read at 124–131, 212–260 and 351–360,
the producer at 28–38, 57–74, 94–138, 195–205 and 229–286; and the
correspondence test at 12–15 and 58–90. Whole-file hashes
establish byte identity; they do not claim substantive adoption of unread parts.
Exact retained copies permit offline checks without a sibling checkout, supplier,
network or host execution. Only string data is read from the producer snapshot;
its code is never run by App tests.

## Version and operation boundary

V3's exact selection, loader, original receiving tests, catalog, v2 history and
frozen App origin remain unchanged. Current v4 is a separately selected loader
and specimen, not a relabelled v3 catalog. Both versions run in CI. Wrong hashes,
missing/tampered supplementary files, altered selections and crossed catalog
versions refuse. No EXP/admission/terminal/S4/package pin changes occur here.

Seven tools retain proposal-only mutation. `swbpipe_read_records` is added using
the existing host ingress command. The flat `operationIntent` schema closes
individual enums but permits invalid cross-products by itself; the separate
`admittedOperations` table is mandatory. Its 16 rows expand to 19 exact tuples.
The App specimen checks all combinations against that table and tests each
admitted tuple. It never injects the table into supplier tool declarations or
interprets descriptions as new authority. A smaller declaration is not evidence
of behavioral equivalence.

The nine v3 branches remain, with structural component-symbol insertion,
objective-connector hardware/pressure-model edits, support configuration edits
and Component/Support/Element/Node deletions added. Agent-supplied attribution,
status, source/queue, validation/audit/professional-boundary fields refuse.
Modifier fields, k/SIF/stiffness-scaling/source paths, bend realization/insertion,
library records, kind changes/combinations, and load-case/primitive-load deletion
have no admitted tuple. Native validation of opaque `after` payloads—including
nested modifiers on any route—remains with the SWBPIPE applier. App does not
implement that applier or claim a structural schema pass makes a payload safe
or applicable. SWBPIPE's separately reported #23 defense remains its subject.

## Read, before-text and cursor joins

Read-record pages bind family and live basis through completion. Separately
supplied invented host-retained cursor evidence binds tool/workspace/basis/run,
family or result filter, and a nonnegative next offset. It is not a new agent
argument, production cursor registry or authenticated host custody.

For deletions/configuration/objective-connector edits, the specimen compares
opaque exact before strings against separately retained target/basis evidence.
Missing delete text refuses; the receiver never manufactures a deletion summary,
normalizes an exponent or trims a label to make a match. Stored units remain
unchanged, with no conversion. The original coordinate-unit guard is retained;
other native dimension/unit and before/payload semantics remain host-owned.

Actual source nuance: the catalog's `sourceRoute` mentions `removalIntents.ts`,
but integrated session lines 57–74 contain its own `engineDisplayNumber` and
`deleteText`, and lines 94–108 contain `recordBefore`. Those bytes, not a literal
import, are the selected producer. The selected `embeddedAgentM2.test.ts` imports both the session helpers and
inspector builders, and asserts equality, actual applier success on invented
untrimmed-label/exponent-coordinate cases, and refusal of the old exponent-form
text. App inspected those assertions and numeric vectors; it did not execute
the host test or thereby qualify a native/live act.
The announced future import refactor is neither a dependency nor silently
adopted. Current before strings are received as host evidence, not regenerated.

## Byte bounds and outcome distinctions

The revised contract and actual producer agree:

- Each raw unescaped `recordText` and before value is at most 16,384 UTF-8 bytes.
- Each compact `JSON.stringify({id,recordText,before})` entry includes escaping.
  The running sum is **at most 49,152**, excluding array punctuation and envelope.
  A fitting entry beyond the aggregate budget starts the next page.
- Any encountered record's own bound violation (including a single escaped entry
  over 49,152 or ID over 160 UTF-16 code units) fails the whole call `unavailable`;
  earlier accumulated records cannot be returned as a successful partial page.
- The entire serialized result has a distinct 65,536-byte cap. Exceeding it is
  `execution_error`, not `unavailable`. No result is truncated or skipped.

The restricted Python entry serializer handles a string-only object tree and
is compared with Node `JSON.stringify`/`TextEncoder`: quotes, backslashes,
controls, astral Unicode, separators, lone surrogates and numeric-looking strings.
It is not a general JS number serializer or native canonicalizer. Complete-result
size is checked against separately supplied serialized evidence bytes, not an
invented Python reserialization. Tests distinguish equality/one-byte overflow,
escaped entries, ID UTF-16 length, whole-call failure and aggregate pagination.
The specimen's own emitted wire also keeps its existing output-cap check; that
is a separate fixture wire, not a byte-for-byte host transport reproduction.

Catalog/summary argument/result/page/pending/operation values are reported
fixture/default configuration, not universal qualification requirements. The
specific producer bounds above belong to the selected source version. Another
configured operation cap is honored without rewriting the schema or claiming
all production configurations use these defaults.

## Evidence and remaining work

The receiving tests establish source correspondence, declared schema/table and
bounded invented joins. They perform no model, native runtime, supplier call,
actual person's Apply, deletion, modifier authoring, acceptance or release.
W9-A and criterion17 remain separately scoped host/parent evidence: actual
candidate/configuration/model/session, displayed proposals and before basis,
actual review/Apply and resulting hash, solver/run/filtered result/report,
interruption/recovery/custody/traffic and the full criterion1 reference system
are not supplied by these fixtures. Parent owns final App integration.
