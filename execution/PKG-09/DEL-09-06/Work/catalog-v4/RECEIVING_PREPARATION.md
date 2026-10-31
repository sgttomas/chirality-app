# Catalog-v4 receiving preparation

This is preparation against SWBPIPE PR27 checked head
`15e40a07dd0bb76d6b6939c7ff9a5177703218f9`, not adoption of an integrated source.
The existing catalog-v3 selection remains unchanged. Final source selection,
publication of exact retained inputs and independent receiving review await the
actual integrated source identity and reconciled producer contract.

Both catalog paths at this PR head were read in full and independently verified:
`execution/PKG-16/DEL-16-06/Work/agent-capability-catalog.json` and
`apps/desktop/src-tauri/resources/agent-capability-catalog.json`, each 50,864 bytes,
SHA256 `8e9a4b4e3eec027d092033ea5d95f1648030520e797c5a660ab387531f23be17`.

The additional Work source `embedded-agent-host.md` at that same head is
52,622 bytes, SHA256
`72462545890c9e0cbeefe7ebc3fc979c50f4dc52a238cdbc7386f5859a412a63`.
Actual read extents: 124–131 (relied-on summary/filter clause 125–128),
229–242 (record reading), 338–341 (cursor/unit boundary). Other document content
is not silently adopted. The quoted 124–127 extent stops before the filter clause.

## Prepared receiver boundary

A separate v4 specimen checks the flat intent schema AND the top-level
`admittedOperations` table: 16 rows expand to 19 exact tuples because coordinate
axes and objective-connector fields are listed separately. Descriptions cannot
widen this table. Seven tool declarations are projected without injecting the
admission table into supplier tool fields. Host-owned attribution/status/queue/
source/validation/audit/professional-boundary fields remain refused.

New structural proposal admission does not implement native deletions, units,
modifier validation, object/reference semantics, batch application or authority.
No record payload is decoded to derive permission from its content. Exact
before strings for deletion/configuration/objective-connector edits are compared
only to separately supplied invented host-retained target/basis evidence. Missing
delete text is unavailable/refusal; the receiver does not synthesize an applier
summary, trim labels or normalize coordinate numbers. Native unit/dimension and
payload semantics remain with SWBPIPE. The original coordinate-unit guard remains.

Read-record calls retain live basis through completion and bind their requested
family/row count. Invented retained cursor records bind tool, workspace, basis,
run, family, filter and next offset. They are fixture representations of a host
lookup, never new agent wire fields or an implemented cursor registry.

## Producer-bound counting correction still requiring final source binding

SWBPIPE supplied a correction from
`apps/desktop/src/services/embeddedAgentSession.ts` lines 272–286 at the checked
PR head. Those producer bytes have not yet been independently received; exact
size/hash and integrated correspondence are requested. This correction supersedes
the earlier prose saying a page stops *before* 48 KiB:

- Raw unescaped UTF-8 `recordText` and each before string: at most 16,384 bytes.
- Entry byte count: compact JavaScript `JSON.stringify({id,recordText,before})`,
  including escaping. Sum of entries is at most 49,152 bytes, excluding enclosing
  array punctuation and result envelope. Equality is admitted.
- An oversized own entry fails the call as unavailable; no truncation or skipping.
- ID bound uses JavaScript UTF-16 string length, not Unicode scalar count.

The prepared Python counting helper is restricted to this string-only entry
grammar and is compared against Node `JSON.stringify` and `TextEncoder` on
Unicode, quotes, backslashes, controls, lone surrogates and numeric-looking text.
It does not implement general JavaScript numeric serialization or applier
canonicalization. The ordinary specimen output-byte cap remains a separate
check of the actual fixture wire it emits, not a producer serialization proof.
Host-reported argument/result/page/pending/operation limits are configured fixture
defaults, not universal schema constants or qualification criteria.

## Remaining work

Confirm actual integrated commit and all catalog/contract/producer hashes and
read extents; resolve conflicting prose before selecting the successor. Retain
v3/v2/original identity and tests. Complete strict receiver tests and independent
Claude review, then CI and ready return to App Agent 0. No live/native/model run,
owner Apply, acceptance, criterion17 qualification or release is established.
W9-A and criterion17 evidence remain separately owned by SWBPIPE and the parent.
