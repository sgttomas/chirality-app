# Operational source locations

Runnable sources moved outside `execution/`. The declarative contracts, findings, data and historical records stay in this deliverable. Current commands use the operational locations below, from the repository root. Relative imports and specification-data reads use the preserved PKG/DEL/Work structure under `app/contract_inputs/`; native support and signing preparation have their own App homes.

Original source identities are from `109441b501edd86453d263f4207ff6199dbd9a78`. The digest column identifies the original bytes moved in pure-rename commits. Unbound current sources may have separate locator edits; bound sources retain exactly those bytes. Historical citations keep their original locators and are recoverable in Git history.

| Original logical path | Current operational path | Original SHA-256 | Bound bytes |
|---|---|---|---|
| `execution/PKG-03/DEL-03-02/Work/prototype/proposal_states.py` | `app/contract_inputs/PKG-03/DEL-03-02/Work/prototype/proposal_states.py` | `1e4264b84d5d7e8168447dc2d4844f658d5324e02e2b02421ee0c9d11f3188c7` | no |
| `execution/PKG-03/DEL-03-02/Work/prototype/swbpipe_corpus_map.py` | `app/contract_inputs/PKG-03/DEL-03-02/Work/prototype/swbpipe_corpus_map.py` | `9dcd359461c7c0dbc9ba981d7298d44929e57dbebd2c53cff766254a9a66da0c` | no |

`tools/ci/execution-inputs.json` records current physical source/data locations. Specification-data copies remain distinct from the authoring originals; repository checks compare full bytes or the existing selected documentary extents. This move creates no qualification, acceptance, publication, reconstruction or native-run result.
