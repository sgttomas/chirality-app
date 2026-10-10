# Codex 0.160.0 macOS arm64 supplier reference (A-IN-S3)

**Standing: authored reference, frozen for independent review. It is not attested,
adopted or qualified.** `expected.json` is an `expected-reference.s1` record for
the stock `@openai/codex@0.160.0-darwin-arm64` vendor tree, made by DEL-01-01
under method `codex-vendor-tree-v1`. Reliance requires a separate
`adoption-attestation.s1` naming its exact SHA-256, an independent reviewer and
technical adoption by the App implementation owner through HELP_HUMAN. The S1
model refuses the reference without one. No attestation exists yet.

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
label, tree and generation joins. The attestation case is skipped until an
attestation exists. A pass does not establish review, adoption, authenticity of
evidence, installed custody, signature validity or App/package qualification.
R23-22 still selects the qualification pin when a candidate is built.

The reviewer may reproduce the tree from the retained archive with
`extraction.json` and compare it to the inventory in `expected.json`. Record the
review and adoption in the attestation, then select both digests in the App build
recipe. Do not edit these bytes after review: a correction is a new reference.
