# QA CHECKS — domain-source-atomize

## Output presence

- Exactly two files exist after the run:
  - `OUTPUT_LEDGER_PATH` (per-unit atom CSV)
  - `OUTPUT_VOCAB_SEED_PATH` (per-unit vocabulary seed CSV)
- No files outside the declared write boundary were created or modified.

## Atom CSV schema

- Header row is exactly: `LocalSeq,UnitStatement,SourceRef,ContentHash,InOutStatus,SectionID,DispatchUnitID,Corrects,Notes`
- File is UTF-8.
- Columns are present and correctly ordered. No extra columns.

## Per-row invariants (atom CSV)

For every row:

| Check | Rule |
|---|---|
| `LocalSeq` | Strictly increasing positive integer; starts at `1`; no gaps; no duplicates |
| `UnitStatement` | Non-empty; one concept per row; preferred length ≤ 50 words |
| `SourceRef` | Non-empty; dual citation `<book>.md:L####\|<book>.html#anchor` |
| `SourceRef` MD line | Falls within `LINE_START..LINE_END` (inclusive) |
| `ContentHash` | Non-empty; exactly 12 lowercase hex characters; equals `sha1(UnitStatement)[:12]` |
| `InOutStatus` | One of `IN`, `OUT`, `TBD` |
| `SectionID` | Member of `TARGET_SECTION_IDS` from `RuntimeOverrides` |
| `DispatchUnitID` | Equals `DISPATCH_UNIT_ID` from `RuntimeOverrides` |
| `Corrects` | Empty OR semicolon-separated list of `HBA-<PREFIX>-NNNNN` IDs |
| `Notes` | Optional; free-form |

## IN/OUT/TBD discipline

- No IN row whose `UnitStatement` is a bare page number, isolated heading text, navigational marker, copyright statement, dedication, or other boilerplate. Such rows must be OUT or omitted.
- TBD is reserved for content the persona must rule on at Gate 2 — not a catch-all for tired classification. Prefer IN or OUT when the classification is clear; use TBD only when ambiguity is real.
- A slice that produces zero IN atoms is valid (`RUN_STATUS=NO_FINDINGS`) — write an empty (header-only) atom CSV plus the vocab CSV.

## ContentHash cross-check

- The merge tool re-derives `sha1(UnitStatement)[:12]` and fails the merge if the declared `ContentHash` does not match. The worker must produce the correct hash.
- Hashes are stable across reruns: identical `UnitStatement` → identical hash.

## Vocab seed CSV schema

- Header row is exactly: `CandidateTerm,Synonyms,Definition,SourceRefs,Notes`
- File is UTF-8.
- Columns are present and correctly ordered. No extra columns.

## Per-row invariants (vocab CSV)

For every row:

| Check | Rule |
|---|---|
| `CandidateTerm` | Non-empty; case preserved as it appears in the source |
| `Synonyms` | Empty OR semicolon-separated list |
| `Definition` | Empty OR a single explicit definition extracted from the source |
| `SourceRefs` | Non-empty; semicolon-separated dual-citation entries |
| `Notes` | Optional; free-form |

- The vocab CSV may be empty (header-only) when the slice contains no candidate canonical terms.

## Failure reporting

The worker reports a structured `RUN_STATUS`:

- `SUCCESS` — atoms emitted, all checks above pass
- `NO_FINDINGS` — slice read but no IN atoms emitted; OUT rows MAY be emitted; vocab CSV MAY be empty
- `FAILED_INPUTS` — inputs were invalid; header-only CSVs written at both output paths
- `FAILED` — slice could not be processed (unexpected encoding, malformed skeleton, write-boundary violation attempt, etc.); a brief explanation accompanies the status

The worker also reports:

- `DISPATCH_UNIT_ID`
- `ATOM_COUNT` (total rows in atom CSV)
- `IN_COUNT`, `OUT_COUNT`, `TBD_COUNT`
- `VOCAB_COUNT`

## Defects that block downstream

These defects block the per-source merge step (`merge_source_atomizations.py per-source`) — surface them to the orchestrator for re-dispatch rather than allowing them to enter the merged ledger:

- Missing `ContentHash` or mismatch with re-derived hash
- Non-monotonic `LocalSeq`
- `SectionID` outside `TARGET_SECTION_IDS`
- `SourceRef` MD line outside `LINE_START..LINE_END`
- Empty `UnitStatement` on an IN row
- Boilerplate (page-numbers-only, header-only) emitted as IN
- File-write outside the declared write boundary
- Final stable `AtomicUnitID` written by the worker (it's the merge tool's responsibility)

## Required evidence

- Worker stdout / RUN_STATUS captured by TASK is sufficient evidence for routine success.
- For `FAILED` and `FAILED_INPUTS` runs, the explanation accompanying RUN_STATUS is the evidence; the orchestrator decides whether to re-dispatch with corrected parameters.
