# Operational source locations

Runnable sources moved outside `execution/`. The declarative contracts, findings, data and historical records stay in this deliverable. Current commands use the operational locations below, from the repository root. Relative imports and specification-data reads use the preserved PKG/DEL/Work structure under `app/contract_inputs/`; native support and signing preparation have their own App homes.

Original source identities are from `109441b501edd86453d263f4207ff6199dbd9a78`. The digest column identifies the original bytes moved in pure-rename commits. Unbound current sources may have separate locator edits; bound sources retain exactly those bytes. Historical citations keep their original locators and are recoverable in Git history.

| Original logical path | Current operational path | Original SHA-256 | Bound bytes |
|---|---|---|---|
| `execution/PKG-02/DEL-02-02/Work/prototype/text_method_controls.py` | `app/contract_inputs/PKG-02/DEL-02-02/Work/prototype/text_method_controls.py` | `c5853f53421fc82cc07728b49b1d406eb3e860c15290367d2797542c57229b24` | no |
| `execution/PKG-02/DEL-02-02/Work/prototype/wrproto.py` | `app/contract_inputs/PKG-02/DEL-02-02/Work/prototype/wrproto.py` | `4fd9d7706c62af2ad41acbf4da0f2d1e56edbe0785ebaa3e3a783adf99a3f567` | no |

`tools/ci/execution-inputs.json` records current physical source/data locations. Specification-data copies remain distinct from the authoring originals; repository checks compare full bytes or the existing selected documentary extents. This move creates no qualification, acceptance, publication, reconstruction or native-run result.
