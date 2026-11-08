# Operational source locations

Runnable sources moved outside `execution/`. The declarative contracts, findings, data and historical records stay in this deliverable. Current commands use the operational locations below, from the repository root. Relative imports and specification-data reads use the preserved PKG/DEL/Work structure under `app/contract_inputs/`; native support and signing preparation have their own App homes.

Original source identities are from `109441b501edd86453d263f4207ff6199dbd9a78`. The digest column identifies the original bytes moved in pure-rename commits. Unbound current sources may have separate locator edits; bound sources retain exactly those bytes. Historical citations keep their original locators and are recoverable in Git history.

| Original logical path | Current operational path | Original SHA-256 | Bound bytes |
|---|---|---|---|
| `execution/PKG-09/DEL-09-11/Work/prototype/rrm_compare.py` | `app/contract_inputs/PKG-09/DEL-09-11/Work/prototype/rrm_compare.py` | `4863074553ebbc27b67ff9190d599cc73c7c79e0ec31079f3092724063957be8` | no |
| `execution/PKG-09/DEL-09-11/Work/prototype/run_standing_check.py` | `app/contract_inputs/PKG-09/DEL-09-11/Work/prototype/run_standing_check.py` | `8eb1bd19615cd1ad140b0f042a01fceacaa3867d857339975a046f90aae83b46` | no |

`tools/ci/execution-inputs.json` records current physical source/data locations. Specification-data copies remain distinct from the authoring originals; repository checks compare full bytes or the existing selected documentary extents. This move creates no qualification, acceptance, publication, reconstruction or native-run result.
