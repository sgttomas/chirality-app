# Staged S4 file receiving

`receive.py` joins a specifically selected synthetic Host export to the existing
canonical EXP/PKG six-record cohort. A successful report means exact exported
file correspondence. It does not mean native S1 semantics were rerun, that a
serialized projection restored native authority, or that an App was qualified.
The maintained Host reader remains the sole implementation of its inventory,
label, reviewer, phase and outcome semantics.

## Inputs and command

Supply the physical path to `exchange.json`, its separately selected SHA256,
and a canonical support selection plus its separately selected SHA256:

```sh
python3 -B app/examination/distribution_receiving/receive.py /physical/export/exchange.json \
  --exchange-sha256 SELECTED_EXCHANGE_SHA256 \
  --selection /physical/records/selection.json \
  --selection-sha256 SELECTED_SUPPORT_SELECTION_SHA256
```

The command emits JSON and exits zero only on correspondence. An unavailable,
missing, contradictory, unsupported or malformed input exits 2. All filesystem
components must be real directories/files, including the supplied parent path;
for example use `/private/tmp` rather than a `/tmp` symbolic link on macOS.
No path inside a producer's raw configuration, originalSource, mirrorLocator,
command or event is opened or executed. Those values remain reported data.

The closed `group-b-s1-reader-exchange.v1` has `case`, `readback`, `actualLt09`,
`members`, `selectedSourceMembers`, `producer` and `applicationCandidate`.
`publication/` holds unchanged raw files, including transport. The sorted member
manifest records path, size and SHA256. Selected exports also contain the exact
declared source files in `selected-source/`; unselected exports have a null
source manifest and no source directory. The export and support-selection
SHA256 arguments freeze caller-selected bytes, not producer credibility.

`producer` identifies a synthetic Host test, its exact source revision,
executable SHA256, command and features. `applicationCandidate` independently
identifies an invented application revision/build for the consumer fixture.
The test executable digest never substitutes for an App build identity.
Arbitrary caller-supplied claims about either remain unauthenticated.

## What is checked

The receiver fixes the full `observed-lifecycle-reader.s3` receipt and selected
source hashes in `pins.json`; callers cannot supply an alternative method.
It reuses the unchanged S1 schemas for shapes, then resolves exact observation,
actual LT09 envelope, transport and declared selected-source references. It
checks projection/raw equality, complete manifest inventory, source/mirror
byte equality, generation and pin correspondence, and explicit supported
standing. Only contract-declared selected references are dependencies; incidental
path/hash objects inside opaque evidence stay opaque. Missing or malformed
nonnull references cannot turn into an unselected success.

Verified outcomes, custody pass, missing LT09, other envelope kinds, mixed
methods, changed sources and byte/path substitutions refuse. No native-held
`S1Reference` or sealed `Selected` is reconstructed. The native reference's
unserialized files and device/inode checks belong to the live Host read.
Preserved exports cannot authenticate that read or detect all semantic forgery.
A fully fabricated internally consistent exchange remains only file
correspondence, never authenticated observation or native semantic validity.

The receiver snapshots original EXP/PKG bytes using no-follow reads and calls
`support_identity/canonical.py` unchanged. That checker still performs its
complete before/after/rerun/review/change/package join. Candidate revision/build
and supplier pin must agree with its selected current package cohort. Existing
package prerequisite gaps remain visible. This bounded package cohort does not
impose a package prerequisite on SQ's native-development cases. Existing SQ,
blank native forms, source locks and historical consumers are unchanged.

Descriptor reads and closure inventories are bounded filesystem observations,
not an atomic hostile-filesystem snapshot. Source pinning establishes selected
technical correspondence, not canonical publication/adoption or verified
producer use. S3, installed custody, actual App/build, native examination,
M1 runner qualification, package witnesses and release remain separate.

## Maintained tests

```sh
python3 -B app/tests/group_b_distribution_receiving_test.py
```

The default selected/unselected fixtures are actual synthetic Host exports,
retained byte-for-byte with their provenance in the sibling fixture README.
The corresponding EXP/PKG records are clearly invented test records; no package,
review, repair or examination act occurred. No Rust build or supplier run is
needed to replay these file tests. Set `CHIRALITY_S4_TEST_EXPORTS` to a fresh
Host-export directory to repeat the same connected receiving tests. The
receiver still requires its pinned producer source revision and full receipt.
