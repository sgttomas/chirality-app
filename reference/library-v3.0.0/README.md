# Library 3.0.0 contributor-source receiving

App selects released `library-v3.0.0` at
`5170575f3f4c1fc51386fa5cd38c7ef9ac048b20` for contributor instructions.
The [owning adoption account](../../execution/PKG-10/DEL-10-01/Work/LIBRARY_V3_RECEIVING.md)
states the adopted practice, project-entry comparison, checks and limits.
This edition supersedes c35/v2.1 for new contributor work; retained older
results and fixtures keep their source identities.

The release's migration notes were read first at
<https://github.com/sgttomas/chirality-library/releases/tag/library-v3.0.0>.
Both the local clean checkout HEAD and tag resolve to the selected commit.
The published source archive is 9,984,000 bytes with reported SHA-256
`fe7e5787a1a4812b8a3d56b19bfc59a2321c5f0e48f676c2ccc80c8c118a073c`.
No archive was downloaded; that digest is release metadata, not an App-computed
archive verification.

`source/` is a **partial test fixture**, not a Library distribution or product
instruction update. Its ten exact Git blobs are the five role files, registry,
role validator and its frontmatter-parser dependency, resolver and LICENSE.
`MANIFEST.json` binds every path, blob/mode, byte length and SHA-256. The copied
validator needs existing PyYAML; the resolver's optional CLI brief-normalization
path is not selected. No full workflow catalog, renderer or Library suite is
copied or claimed.

`tools/validation/test_library_v3_operational_adoption.py` exercises this closure
in ordinary App governance CI without the sibling checkout, Git or network.
The old v2.1 fixture and checks remain historical. The v2.1 reader rejects the
v3 role YAML headers; the v3 reader accepts them. Complete source fingerprints
include the headers, and INTERLOCUTOR still requires explicit method eligibility
and write targets.

The App's product instruction source in DEL-02-04 Work and shipped copies keep
basis89ac/four roles and their existing source bindings. This receiving does
not claim packaged v3 adoption, model uptake or native/product qualification.
