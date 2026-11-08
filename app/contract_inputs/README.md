# Operational contract inputs

Runnable deliverable prototypes and their selected specification-data inputs live
here, outside the declarative `execution/` tree. The PKG/DEL/Work directory shape
preserves existing relative imports and data relationships. Native examination
support lives in `app/examination/native_support/`, signing preparation in
`app/packaging/seal_c/`, and historical DAG reconstruction in
`tools/historical_reconstruction/dag004/`.

`tools/ci/execution-inputs.json` lists source moves and selected data copies.
`source` retains the original authoring locator; `path` or `copy` is the current
physical location. The code digest records the bytes moved by the pure rename;
`bound: true` additionally requires the current bytes to remain identical.
Separate locator edits on unbound sources do not change a historical digest.
Owning `Work/CODE_LOCATION.md` files record the mappings.

Data copies begin byte-identical to their authoring source. Always-on repository
checks retain full-byte freshness, or the existing selected documentary extents
where that is the reader's established selection. The copied file's own digest
also remains checked. Current admission retains its full-document selection.
Do not regenerate or repin a historical identity to make a current check pass.
Group B authoring correspondence, source pins and documentary selectors continue
in repository checks even when product CI is not selected.

The static S1 reader retains the original basis as evidence and translates only
paths in a private current staging basis, outside `execution/`, with identical
dependency hashes. It reports this distinction and makes no original-path replay,
qualification, acceptance, native-run or release claim. Historical frozen inputs
and fidelity-only records retain their own subjects and original locators.
