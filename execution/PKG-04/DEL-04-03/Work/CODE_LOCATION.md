# Operational source locations

Runnable sources moved outside `execution/`. The declarative contracts, findings, data and historical records stay in this deliverable. Current commands use the operational locations below, from the repository root. Relative imports and specification-data reads use the preserved PKG/DEL/Work structure under `app/contract_inputs/`; native support and signing preparation have their own App homes.

Original source identities are from `109441b501edd86453d263f4207ff6199dbd9a78`. The digest column identifies the original bytes moved in pure-rename commits. Unbound current sources may have separate locator edits; bound sources retain exactly those bytes. Historical citations keep their original locators and are recoverable in Git history.

| Original logical path | Current operational path | Original SHA-256 | Bound bytes |
|---|---|---|---|
| `execution/PKG-04/DEL-04-03/Work/prototype/check_cc_r.py` | `app/contract_inputs/PKG-04/DEL-04-03/Work/prototype/check_cc_r.py` | `dc4bd93882984fba2106461b6e4ceb26056b7bdd7e1d074e316ca158c3eebf22` | no |
| `execution/PKG-04/DEL-04-03/Work/prototype/check_content_receiving.py` | `app/contract_inputs/PKG-04/DEL-04-03/Work/prototype/check_content_receiving.py` | `e2634cc56039341358be9fcfd4f4013900d185f5feb53de6dcf59e03aae3effb` | no |
| `execution/PKG-04/DEL-04-03/Work/prototype/exec_to_rs.py` | `app/contract_inputs/PKG-04/DEL-04-03/Work/prototype/exec_to_rs.py` | `39e9e9f299dd5d8ae18b5eb97934d5f5b4db79267a34df5dcb41d3023613ca06` | no |
| `execution/PKG-04/DEL-04-03/Work/prototype/minischema.py` | `app/contract_inputs/PKG-04/DEL-04-03/Work/prototype/minischema.py` | `d30aaef3d59f295df45a121f0721100301e0141f4ebdf325a073995e5f158dd0` | no |
| `execution/PKG-04/DEL-04-03/Work/prototype/record_store.py` | `app/contract_inputs/PKG-04/DEL-04-03/Work/prototype/record_store.py` | `22d3acacce2afe642b38261e62a610d234c224c18e5fac1144b669d676e82cd0` | no |
| `execution/PKG-04/DEL-04-03/Work/prototype/run_prototype.py` | `app/contract_inputs/PKG-04/DEL-04-03/Work/prototype/run_prototype.py` | `30ec35ed4d5ceaad634dec85167887c9a04b96763f9a570edd8a9ba240f33979` | no |
| `execution/PKG-04/DEL-04-03/Work/prototype/test_minischema.py` | `app/contract_inputs/PKG-04/DEL-04-03/Work/prototype/test_minischema.py` | `5c728e2d3d1bfa19ee119d148cd1b906a56a86bb6b40ea17eed671f463602f8c` | no |

`tools/ci/execution-inputs.json` records current physical source/data locations. Specification-data copies remain distinct from the authoring originals; repository checks compare full bytes or the existing selected documentary extents. This move creates no qualification, acceptance, publication, reconstruction or native-run result.
