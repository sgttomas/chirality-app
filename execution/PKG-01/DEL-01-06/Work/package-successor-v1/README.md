# Explicit static package and S4 evidence consumer

`app/packaging/successor/check.py` consumes `static-package-input/2` and
`packaged-s4-binding/1` without scanner, supplier, App or network execution.
Legacy input/1, PKG-v0.2 and S1 schemas/readers retain their original meaning.
The static S1 package must keep `verification_artifact: null`. Terms select the
approved terms-position/v1 reader explicitly, never a fabricated legacy reply.

The static request revalidates exact package/reference/inventory/terms closure
and pre-notary installer bytes with the frozen canonical S1 value model.
Inventories are retained evidence, not newly scanned trees. The separate binding
joins App source/build/version/identifier, executable bytes and declared cdhash,
original publisher selection/binding/requirement, separate public projection,
effective Tauri config, supplier selection, S4 observation/custody/full generation
and inventory, and post-staple installer bytes. Missing or contradictory inputs
remain visible. These checks authenticate no signature, build, actor or native act.

## API

```python
source_dependencies()  # maintained root-relative source path -> exact SHA-256
check(request_path, *, evidence_root=None, trusted_publisher_sha256=None)
```

All artifact edges, including nested static and terms edges, are relative to
**one** selected evidence root (default: request parent). The caller separately
selects a trusted original publisher binding digest; it is never read from the
package. Missing trust is a gap, contradictory trust an error. Receiving code
must independently pin the reader source closure; the checker cannot authenticate
itself. Source/evidence bytes are rechecked before return. Traversal, links,
hardlinks, special files, unknown versions and conflicting hashes refuse. Typed
artifacts are capped at 2 MiB, opaque/binary files at 512 MiB, total snapshot at
1 GiB. This detects ordinary change, not hostile-writer isolation.

The report is `packaged-s4-check/1`, with `record_id`, `request_sha256`, `candidate`
(`revision`, `build_identity`, `codex_pin`, `package_record_id`), separate `errors`
and `missing`, complete followed `artifacts` path/digest map, maintained
`source_dependencies` and limits. `standing: evidence-consistency-only`,
`release_authorized: false` and `live_authority: false` are unconditional.
Malformed/version/hash/schema contradictions raise ValueError; CLI exit is 2 for
errors/refusal, 1 for gaps, 0 for complete selected consistency, never qualification.

The wrapper's caller-specified `record_id` is the EXP/SQ package-witness citation.
`candidate.package_record_id` is the different inner legacy ID, validated against
the static package. No wrapper is inserted into a legacy record or S1 runtime slot.

`source_dependencies()` needs no fixture. Its closure includes all maintained
code/schema/template/recipe inputs; AGENTS.md is solely the existing model's
repository-root marker, not product instruction adoption. The tests stage that
complete source and evidence closure into an offline worker without repository
fallback. No scanner is invoked by either API.

## Fixtures, ownership and limits

`fixtures.py::Fixture(root)` creates invented non-executable evidence. API:
`.request`, `.values`, `.put(name,value)`, `.put_raw(name,bytes)`, `.save()`,
`.check(trust=True)` and `.trusted_publisher_sha256` (an invented trust seam).
Run `python3 -m pytest -q app/tests/package_successor_test.py` from the repository.
None of the fixture's publisher, signature, notarisation or owner assertions are
actual observations or decisions.

DEL-09-01/02's examination owner separately implements explicit package-witness
sidecars, fixed receiving config and EXP/SQ joins using this authoritative API.
Existing bindings are unchanged. App Agent 0 owns final integration. This work
implements bounded OUT-001/002 preparation and REQ-001/002/005 exact receiving
joins, without changing commitments or supplying actual FP-2/W-4/S5 results.

A final executable hash joined to a declared cdhash is not cryptographic signature
verification or proof of compiler provenance. No disk artifact constructs live
InstalledCustody or selects the App's compiled publisher. Actual publisher input,
signed/notarised package, native installation, OS qualification and publication
remain separate. Minimum macOS 15, planned version 4.0.0 and separate v4 identity
choices do not supply the missing exact identifier/team or qualify a fixture.
