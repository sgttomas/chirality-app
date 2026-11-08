# Operational source locations

Runnable sources moved outside `execution/`. The declarative contracts, findings, data and historical records stay in this deliverable. Current commands use the operational locations below, from the repository root. Relative imports and specification-data reads use the preserved PKG/DEL/Work structure under `app/contract_inputs/`; native support and signing preparation have their own App homes.

Original source identities are from `109441b501edd86453d263f4207ff6199dbd9a78`. The digest column identifies the original bytes moved in pure-rename commits. Unbound current sources may have separate locator edits; bound sources retain exactly those bytes. Historical citations keep their original locators and are recoverable in Git history.

| Original logical path | Current operational path | Original SHA-256 | Bound bytes |
|---|---|---|---|
| `execution/PKG-10/DEL-10-01/Work/prototype/eb1_check.py` | `app/contract_inputs/PKG-10/DEL-10-01/Work/prototype/eb1_check.py` | `889d7d4814a90758a3504a97a5ad60d3d758e78a42d5e9c10ab26f5a993ee164` | no |
| `execution/PKG-10/DEL-10-01/Work/prototype/make_input_set.py` | `app/contract_inputs/PKG-10/DEL-10-01/Work/prototype/make_input_set.py` | `92522b7c3f010166a39fe836d11c1c9029790e3ce9ceda071555997ce9029891` | no |

`tools/ci/execution-inputs.json` records current physical source/data locations. Specification-data copies remain distinct from the authoring originals; repository checks compare full bytes or the existing selected documentary extents. This move creates no qualification, acceptance, publication, reconstruction or native-run result.
