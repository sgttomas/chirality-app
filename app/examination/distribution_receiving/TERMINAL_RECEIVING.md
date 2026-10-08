# B-S4-TERMINAL-RECEIVING-v1

Separate fixed file-consumer contract for actual synthetic completed LT09/LT23
export pairs. Selected producer source is
`9af67409ed0e625fcd8e0e9a0c59975fccfcae71`. It uses
`group-b-s1-terminal-reader-exchange.v1`; the standalone LT09 v1 contract is
unchanged and neither consumer accepts the other's exchange shape.

```sh
python3 -B app/examination/distribution_receiving/terminal.py /physical/case/exchange.json \
  --exchange-sha256 SELECTED_EXCHANGE_SHA256 \
  --selection /physical/records/selection.json \
  --selection-sha256 SELECTED_CANONICAL_SELECTION_SHA256
```

The completed marker must be named exchange.json. Pending/queued/unavailable
readback, diagnostic filenames/markers, unexpected case members and missing or
malformed references refuse. A completed case has predecessor/publication,
terminal/publication and selected-source only when selected. All raw members
and manifests are checked by bounded no-follow reads. Raw producer locators are
historical data, never paths to open. Extra/missing entries and substitutions
refuse; this is not an atomic snapshot or runtime authentication.

## Reuse and exact joins

The new literal pins.terminal-v1.json digest selects the full receipt and source
hashes, including the final unchanged-algorithm receive.py and terminal exporter.
The captured receive.py bytes are checked before its definitions are executed.
The new initializer establishes its own fixed source basis; it does not assert
that a historical source guard passed or mutate historical pins/global state.

An internal outer-format projection presents the actual predecessor LT09 fields
and unchanged raw closure to the frozen existing file-check algorithm. It mints
no record binding, changes no event and never rewrites LT23 as LT09. That path
calls the unchanged canonical six-record EXP/PKG checker. The internal projected
exchange digest is labelled by its enclosing predecessor_canonical_join; the
outer report separately binds the real terminal exchange digest.

The terminal path checks unchanged schema shapes, exact raw/projection/event
correspondence, full same-H5 generation, increasing actual event sequence,
distinct immutable publication names/locators, identical pre-spawn observation
bytes/reference, source association and every shared closure byte. The same
candidate/build/pin therefore joins both publications through the single exact
canonical selection. The terminal envelope must be actual LT23 tree-ended,
stopping→stopped, while predecessor remains LT09. Shape and file joins are not
another native inventory/label/custody/outcome semantic engine.

## Claims and limits

A successful terminal_pair_file_correspondence_passed report says the supplied
exported pair corresponds. It does not authenticate actual event history,
terminal integrity, zero surviving descendants, current namespace authority,
native references, application build or supplier qualification. Pre-spawn
observation remains pre-spawn; association with LT23 is no renewed probe or
custody. Authority/qualification flags stay false. The Host's native-held
read/export and worker behavior remain separately owned evidence, not a JSON
capability restored by this CLI.

Both maintained cases are byte-exact actual committed-source/recompiled
synthetic Host exports, with producer source/executable/command/features and
provenance. The EXP/PKG cohort remains explicitly invented; no examiner/package
act or verified support use is inferred. S3, M1/native qualification, real App
build, package witness, canonical rollout, owner gate and release remain separate.
No SQ package gate is added.

Tests: `python3 -B app/tests/group_b_terminal_receiving_test.py`.
No Rust build or native/supplier run is required for replay. Original f267, b7,
5c9 cohorts/pins and prior evidence remain unchanged. The separately named
TERMINAL_SOURCE_LT09_ADOPTION.md keeps the standalone LT09 CLI current.
