# Library 3.3.0 contributor selection

App selects `library-v3.3.0` at
`ec3ee2d1b398eba1fb3227ccf93e2569df95bacd`, replacing 3.1.0 for new contributor
reliance and skipping 3.2.1. The [owning findings](../../execution/PKG-10/DEL-10-01/Work/LIBRARY_V3_3_RECEIVING.md)
record the entry-document and retained-method dispositions.

The published `chirality-library-3.3.0-source.tar` is 10,004,480 bytes, with
SHA-256 `e3db320a1d6b7b69dcb2e71d171849904189da1ce7666aa522ae91d6b98c3b20`.
The tag resolves to the selected commit. A local `git archive` of that commit
matches the published digest; no release asset was downloaded. The existing
shared working checkout remains at its own revision and is not silently used as
3.3.0. When it differs from the selected commit, prepare a separate instruction
source without changing that checkout:

```sh
CHIRALITY_INSTRUCTION_ROOT=$(mktemp -d /tmp/app-library-source.XXXXXX)
git -C /Users/ryan/dev/chirality-library archive ec3ee2d1b398eba1fb3227ccf93e2569df95bacd | tar -xf - -C "$CHIRALITY_INSTRUCTION_ROOT"
```

Read selected roles and methods from that exact export. Verify the source tag
and commit first; on another machine an explicitly selected checkout or the
verified release archive supplies the same source. A path alone is not a source
selection.

`MANIFEST.json` is a small contributor/test delta. Five changed role blobs are
retained here; unchanged registry, parser/validator, resolver, index builder and
license inputs retain their exact earlier fixture paths. The new metadata
schema and the comparison workflow, canonical project-entry resource, catalog
and metadata guide retain their released Git identities. This is not a full
Library distribution or a product instruction package. Tests export the selected
inputs into scratch without a sibling checkout or network dependency.

The entry documents' `metadata.upstream` records a fresh, fully reconciled 3.3.0
basis against the applicable project-entry sections. It attributes no prior
history. The top-level coordination package remains the exact migration/test
input bound by `reference/migration/shared-inputs.json`; the selected Library
method is the operational source. Packaged instruction resources, their
basis89ac/four-role binding and packaged workflow SOURCE_MAP remain separate.
