# Operational source locations

Runnable sources moved outside `execution/`. The declarative contracts, findings, data and historical records stay in this deliverable. Current commands use the operational locations below, from the repository root. Relative imports and specification-data reads use the preserved PKG/DEL/Work structure under `app/contract_inputs/`; native support and signing preparation have their own App homes.

Original source identities are from `109441b501edd86453d263f4207ff6199dbd9a78`. The digest column identifies the original bytes moved in pure-rename commits. Unbound current sources may have separate locator edits; bound sources retain exactly those bytes. Historical citations keep their original locators and are recoverable in Git history.

| Original logical path | Current operational path | Original SHA-256 | Bound bytes |
|---|---|---|---|
| `execution/PKG-02/DEL-02-04/Work/prototype/jsonschema_lite.py` | `app/contract_inputs/PKG-02/DEL-02-04/Work/prototype/jsonschema_lite.py` | `b4fea5e8d68e0ef283ee775dea7005c09855779937942907e0d12de1593b6dd6` | no |
| `execution/PKG-02/DEL-02-04/Work/prototype/role_supply.py` | `app/contract_inputs/PKG-02/DEL-02-04/Work/prototype/role_supply.py` | `364fe4cd0b38a1867fd041f463d685b9c3df0674d92c813a5ae05311a302d54b` | no |
| `execution/PKG-02/DEL-02-04/Work/prototype/run_cases.py` | `app/contract_inputs/PKG-02/DEL-02-04/Work/prototype/run_cases.py` | `34179ac2200a596da05e3c532debbc4ad2f9bd240de2f66312750a8449f83856` | no |

`tools/ci/execution-inputs.json` records current physical source/data locations. Specification-data copies remain distinct from the authoring originals; repository checks compare full bytes or the existing selected documentary extents. This move creates no qualification, acceptance, publication, reconstruction or native-run result.
