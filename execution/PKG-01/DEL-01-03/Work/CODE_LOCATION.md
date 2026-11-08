# Operational source locations

Runnable sources moved outside `execution/`. The declarative contracts, findings, data and historical records stay in this deliverable. Current commands use the operational locations below, from the repository root. Relative imports and specification-data reads use the preserved PKG/DEL/Work structure under `app/contract_inputs/`; native support and signing preparation have their own App homes.

Original source identities are from `109441b501edd86453d263f4207ff6199dbd9a78`. The digest column identifies the original bytes moved in pure-rename commits. Unbound current sources may have separate locator edits; bound sources retain exactly those bytes. Historical citations keep their original locators and are recoverable in Git history.

| Original logical path | Current operational path | Original SHA-256 | Bound bytes |
|---|---|---|---|
| `execution/PKG-01/DEL-01-03/Work/prototype/jsonschema_subset.py` | `app/contract_inputs/PKG-01/DEL-01-03/Work/prototype/jsonschema_subset.py` | `486e9286e5aa56888b5473f1c08493a115591255685a8a7bb88b93ff2cacffc0` | no |
| `execution/PKG-01/DEL-01-03/Work/prototype/npt_model.py` | `app/contract_inputs/PKG-01/DEL-01-03/Work/prototype/npt_model.py` | `06810c7a4b5ff0e8504ab3ca82e4dff440f3ebacc4a8bc6d0773a2cb0fca7453` | no |
| `execution/PKG-01/DEL-01-03/Work/prototype/run_cases.py` | `app/contract_inputs/PKG-01/DEL-01-03/Work/prototype/run_cases.py` | `a7b3e77860dd80a3a28e0c6ea6b64539e44d79b6940b18378c331d2976413559` | no |
| `execution/PKG-01/DEL-01-03/Work/prototype/scenarios.py` | `app/contract_inputs/PKG-01/DEL-01-03/Work/prototype/scenarios.py` | `963cf3b21afa35ef6b42f135a2ee547db7dc729329c7dee196a75e77fbe644e3` | no |

`tools/ci/execution-inputs.json` records current physical source/data locations. Specification-data copies remain distinct from the authoring originals; repository checks compare full bytes or the existing selected documentary extents. This move creates no qualification, acceptance, publication, reconstruction or native-run result.
