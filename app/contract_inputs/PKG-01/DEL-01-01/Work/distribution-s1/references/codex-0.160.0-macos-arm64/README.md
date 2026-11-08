# Codex 0.160.0 macOS arm64 supplier reference (A-IN-S3)

**Standing: qualified supplier reference, independently reviewed and technically
adopted; not yet selected by any App build.** `expected.json` is an
`expected-reference.s1` record for the stock `@openai/codex@0.160.0-darwin-arm64`
vendor tree, made by DEL-01-01 under method `codex-vendor-tree-v1`.
`attestation.json` (`adoption-attestation.s1`, SHA-256
`09e1fae9d243462132803d868174b70ddae111bde2106aa2351ebfe74c793fe9`) names the
record's exact digest. It cites the independent review in `review.md` (READY at
revision `b616fe3db0`) and HELP_HUMAN's technical adoption for the App
implementation owner in `adoption.json`. Reliance still requires a trusted App
build recipe that selects both digests.

DISTRIBUTION_IDENTITY names the producer (DEL-01-01) but no directory. This
location is proposed here, beside the S1 cohort it conforms to. The cohort's
`PUBLICATION.json` files are unchanged.

| | |
|---|---|
| Reference | `expected.json`, SHA-256 `754eebae912023aebe40cab157c0882081bec2d1d9db518627986526371a2a37` |
| Bundle root | `DEL-01-01/Design`; every artifact path in the record is relative to it |
| Tree | 53 entries (42 files, 11 directories), manifest `327effb9…8d12`; `bin/codex` `112fae7a…1b4b` |
| Label | `codex-cli 0.160.0` from an isolated H-probe (`label-probe.json`) |
| Generated output | `generated/0.160.0`, manifest file `411ea5d4…b8be`; joins in `generation-correspondence.json` |

The archive and extraction are never committed. `acquisition.json`,
`custody.json` and `extraction.json` record the owner's authorization as relayed,
the digests and how to reproduce the tree. The extracting umask (022) matters
because the archive carries no directory entries.

Check offline, without supplier bytes:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 test_codex_0160_reference.py
```

This checks schema conformance, exact evidence bytes, inventory validity and the
label, tree and generation joins. It also checks that the attestation, selected
by its pinned digest, joins the record, and that an unselected or changed
attestation is refused. A pass does not establish authenticity of review,
adoption or evidence, installed custody, signature validity or App/package
qualification. R23-22 still selects the qualification pin when a candidate is
built.

A tree can be reproduced from the retained archive with `extraction.json` and
compared to the inventory in `expected.json`. Do not edit the reviewed or
attested bytes: a correction is a new reference with a new review and attestation.
