# Operational source locations

Runnable sources moved outside `execution/`. The declarative contracts, findings, data and historical records stay in this deliverable. Current commands use the operational locations below, from the repository root. Relative imports and specification-data reads use the preserved PKG/DEL/Work structure under `app/contract_inputs/`; native support and signing preparation have their own App homes.

Original source identities are from `109441b501edd86453d263f4207ff6199dbd9a78`. The digest column identifies the original bytes moved in pure-rename commits. Unbound current sources may have separate locator edits; bound sources retain exactly those bytes. Historical citations keep their original locators and are recoverable in Git history.

| Original logical path | Current operational path | Original SHA-256 | Bound bytes |
|---|---|---|---|
| `execution/PKG-06/DEL-06-01/Work/prototype/fleet_store.py` | `app/contract_inputs/PKG-06/DEL-06-01/Work/prototype/fleet_store.py` | `d0722975342e810f482736e106b71615d9e95ee0c4ef8289ad299f83266eba5d` | no |
| `execution/PKG-06/DEL-06-01/Work/prototype/run_fleet.py` | `app/contract_inputs/PKG-06/DEL-06-01/Work/prototype/run_fleet.py` | `396758b56d83122a19d2164098cdf22eb328628b24594e37449afd306e594a3e` | no |

`tools/ci/execution-inputs.json` records current physical source/data locations. Specification-data copies remain distinct from the authoring originals; repository checks compare full bytes or the existing selected documentary extents. This move creates no qualification, acceptance, publication, reconstruction or native-run result.
