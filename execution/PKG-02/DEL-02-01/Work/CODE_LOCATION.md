# Operational source locations

Runnable sources moved outside `execution/`. The declarative contracts, findings, data and historical records stay in this deliverable. Current commands use the operational locations below, from the repository root. Relative imports and specification-data reads use the preserved PKG/DEL/Work structure under `app/contract_inputs/`; native support and signing preparation have their own App homes.

Original source identities are from `109441b501edd86453d263f4207ff6199dbd9a78`. The digest column identifies the original bytes moved in pure-rename commits. Unbound current sources may have separate locator edits; bound sources retain exactly those bytes. Historical citations keep their original locators and are recoverable in Git history.

| Original logical path | Current operational path | Original SHA-256 | Bound bytes |
|---|---|---|---|
| `execution/PKG-02/DEL-02-01/Work/prototype/content_identity_cases.py` | `app/contract_inputs/PKG-02/DEL-02-01/Work/prototype/content_identity_cases.py` | `7ab8f17386d71729343e262d69aea2a2e650906b8cc576f5ba54aa29cd3b2ddf` | no |
| `execution/PKG-02/DEL-02-01/Work/prototype/extract.mjs` | `app/contract_inputs/PKG-02/DEL-02-01/Work/prototype/extract.mjs` | `40f5f99e99012ab1731e5674e2c168c161afa4f9e0c789ac7fa4e071a483c101` | no |
| `execution/PKG-02/DEL-02-01/Work/prototype/wdproto.py` | `app/contract_inputs/PKG-02/DEL-02-01/Work/prototype/wdproto.py` | `07a8f9795c5384aba0c780c20c9ce5d221eb2a746581d8bfb84bd2d34a89c0f0` | no |

`tools/ci/execution-inputs.json` records current physical source/data locations. Specification-data copies remain distinct from the authoring originals; repository checks compare full bytes or the existing selected documentary extents. This move creates no qualification, acceptance, publication, reconstruction or native-run result.
