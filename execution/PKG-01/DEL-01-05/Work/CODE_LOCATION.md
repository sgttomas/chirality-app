# Operational source locations

Runnable sources moved outside `execution/`. The declarative contracts, findings, data and historical records stay in this deliverable. Current commands use the operational locations below, from the repository root. Relative imports and specification-data reads use the preserved PKG/DEL/Work structure under `app/contract_inputs/`; native support and signing preparation have their own App homes.

Original source identities are from `109441b501edd86453d263f4207ff6199dbd9a78`. The digest column identifies the original bytes moved in pure-rename commits. Unbound current sources may have separate locator edits; bound sources retain exactly those bytes. Historical citations keep their original locators and are recoverable in Git history.

| Original logical path | Current operational path | Original SHA-256 | Bound bytes |
|---|---|---|---|
| `execution/PKG-01/DEL-01-05/Work/prototype/access_model.py` | `app/contract_inputs/PKG-01/DEL-01-05/Work/prototype/access_model.py` | `9dedb05bdaae5d6ba1f256f128a08454c6931d48532ae8fac336fdf9181de8e5` | no |
| `execution/PKG-01/DEL-01-05/Work/prototype/check_explicit_project_context.py` | `app/contract_inputs/PKG-01/DEL-01-05/Work/prototype/check_explicit_project_context.py` | `c6c9b3c52c78474f06bb24def1f4d9ab4602d258d68593eb3ad4887bbacb7c1d` | no |
| `execution/PKG-01/DEL-01-05/Work/prototype/jsonschema_subset.py` | `app/contract_inputs/PKG-01/DEL-01-05/Work/prototype/jsonschema_subset.py` | `486e9286e5aa56888b5473f1c08493a115591255685a8a7bb88b93ff2cacffc0` | no |
| `execution/PKG-01/DEL-01-05/Work/prototype/run_cases.py` | `app/contract_inputs/PKG-01/DEL-01-05/Work/prototype/run_cases.py` | `4fec6d1551ffc4471e54295d68e1fa23c1d094c27b9c506f0965c861ae596baa` | no |

`tools/ci/execution-inputs.json` records current physical source/data locations. Specification-data copies remain distinct from the authoring originals; repository checks compare full bytes or the existing selected documentary extents. This move creates no qualification, acceptance, publication, reconstruction or native-run result.
