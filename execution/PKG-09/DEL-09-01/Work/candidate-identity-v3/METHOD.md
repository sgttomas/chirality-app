# Complete-content development candidate identification — v3

DEL-09-01 adds this record profile for DEL-09-02 and DEL-01-06. It repairs
the active producer/reader `app/examination/candidate_identity/identify.py`:
v2's closed supplier shape requires `bundled: false`, and the producer formerly
emitted that declaration for any bundle. That scope cannot describe the
complete-content development route, which includes Codex in Resources.

The v2 schema, historical records and bundle-tree v2 method are unchanged.
`record` without supplier inputs still writes v2, now refusing a codex subtree
rather than declaring it absent. Supplying both `--supplier-archive` and
`--supplier-acquisition` selects this closed v3 record shape. `check` dispatches
by the explicit format; unknown versions refuse. This is an additive technical
representation within ScopeOfWork REQ-002 and OUT-001/003, not a changed
qualification criterion or acceptance.

## Subject and evidence

The complete `.app` still uses `chirality.app.bundle-tree.sha256/v2`: all
supplier bytes, modes, ownership and permitted metadata join the same two-pass
inventory and build identity. The candidate key and EXP `app_candidate` values
are unchanged. `native_development` and `packaged: false` mean this unsigned
development App is not an identified signed/notarised distribution package.
P1's presence does not turn it into DEL-01-06's qualified package.

The new profile requires declared debug, unsigned (`signing: none`), offline
build facts with `custom-protocol`. These remain supplied build facts, not
compiled-feature or signature attestation. Linker ad-hoc output and supplier
signatures confer no Developer ID signing or package qualification. Source
export/blob verification, build/config/toolchain/lockfile account, App-data
freshness observation, inventory checking and all v2 metadata restrictions
continue unchanged; see [the v2 method](../candidate-identity-v2/METHOD.md).

The supplier is explicitly `bundled: true`, rooted at
`Contents/Resources/codex`, with `unqualified-development` standing. The
read-only `bundled_supplier.py` reader measures an existing macOS arm64 stock
platform tarball, compares its SHA-256 and size with the supplied acquisition
record and compares every vendor file's bytes, size and mode with the bundle
inventory. Missing/extra files and directories, duplicate/unsafe tar paths,
links and special vendor entries refuse. Explicit tar directory modes must
match; implicit ancestor directory modes have no tar claim and remain measured
by the complete bundle identity. Package metadata outside the vendor subtree
is not bundled or part of this supplier comparison.

The exact acquisition record is retained as `supplier-acquisition.json` beside
the record and inventory, bound by SHA-256. Its declared official npm locator,
archive filename, measured archive size/digest, pin, file count and regular-file
manifest are recorded. The reader supports the official macOS arm64 platform
filename/URL convention only. It does not authenticate the supplier origin,
owner authorization, obtaining actor or acquisition custody. No tar extraction,
network request, credential read or supplier execution occurs.

`check` revalidates retained acquisition bytes and inventory-derived supplier
fields, then checks the live complete bundle using the existing method. It
does not need the original archive or reassert acquisition custody. The
archive-to-inventory comparison is the original identification observation;
tampering with a record and every bound artifact is not prevented by hashes.
These are bounded observations, not installed custody or a signature service.

## Use and consumers

Use the existing `record` arguments with:

```sh
--supplier-archive /absolute/existing/codex-0.160.0-darwin-arm64.tgz \
--supplier-acquisition /absolute/identified/acquisition.json
```

No version/pin advance is selected here. DEL-09-02 consumes the same candidate
revision/build/key and the new truthful supplier declaration; actual model,
configuration, examination, acts and independent review remain separate.
The SQ/EXP receiving adapters consume their own pinned dossier/EXP shapes and
opaque candidate identities, not this record's supplier object. No receiving
pin or frozen packet is changed. DEL-01-06 can use the archive correspondence
alongside its P2/P3 content comparisons, but package identity, FP checks,
installed custody, signing/notary, terms and native install/launch remain owed.
Historical v2 records retain their original meaning and remain readable.
