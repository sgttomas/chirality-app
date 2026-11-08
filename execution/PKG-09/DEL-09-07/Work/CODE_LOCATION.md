# Operational source locations

Runnable sources moved outside `execution/`. The declarative contracts, findings, data and historical records stay in this deliverable. Current commands use the operational locations below, from the repository root. Relative imports and specification-data reads use the preserved PKG/DEL/Work structure under `app/contract_inputs/`; native support and signing preparation have their own App homes.

Original source identities are from `109441b501edd86453d263f4207ff6199dbd9a78`. The digest column identifies the original bytes moved in pure-rename commits. Unbound current sources may have separate locator edits; bound sources retain exactly those bytes. Historical citations keep their original locators and are recoverable in Git history.

| Original logical path | Current operational path | Original SHA-256 | Bound bytes |
|---|---|---|---|
| `execution/PKG-09/DEL-09-07/Work/prototype/cir_check.py` | `app/contract_inputs/PKG-09/DEL-09-07/Work/prototype/cir_check.py` | `6f32a9511acc505b074cc6983589c790900832f36dfc5fa8669850bbffbd2bad` | no |
| `execution/PKG-09/DEL-09-07/Work/prototype/dos_check.py` | `app/contract_inputs/PKG-09/DEL-09-07/Work/prototype/dos_check.py` | `c845bed87d155ab5f1a047c456d923c48c33e8495f38c0c3f6bfca47f60cdb6e` | no |
| `execution/PKG-09/DEL-09-07/Work/prototype/top_check.py` | `app/contract_inputs/PKG-09/DEL-09-07/Work/prototype/top_check.py` | `cf128073437772b3f14f2d7f5c42b2043087f19a1f4a9b82ba487a839b135139` | no |

`tools/ci/execution-inputs.json` records current physical source/data locations. Specification-data copies remain distinct from the authoring originals; repository checks compare full bytes or the existing selected documentary extents. This move creates no qualification, acceptance, publication, reconstruction or native-run result.
