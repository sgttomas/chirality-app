# Operational source locations

Runnable sources moved outside `execution/`. The declarative contracts, findings, data and historical records stay in this deliverable. Current commands use the operational locations below, from the repository root. Relative imports and specification-data reads use the preserved PKG/DEL/Work structure under `app/contract_inputs/`; native support and signing preparation have their own App homes.

Original source identities are from `109441b501edd86453d263f4207ff6199dbd9a78`. The digest column identifies the original bytes moved in pure-rename commits. Unbound current sources may have separate locator edits; bound sources retain exactly those bytes. Historical citations keep their original locators and are recoverable in Git history.

| Original logical path | Current operational path | Original SHA-256 | Bound bytes |
|---|---|---|---|
| `execution/PKG-05/DEL-05-01/Work/prototype/assemble_tool_calls.py` | `app/contract_inputs/PKG-05/DEL-05-01/Work/prototype/assemble_tool_calls.py` | `cdac36935a2506a313b88bfa656900c12d032f9ad9fe1cc1c8f4e2d9b68b3f5b` | no |
| `execution/PKG-05/DEL-05-01/Work/prototype/destination_flow.py` | `app/contract_inputs/PKG-05/DEL-05-01/Work/prototype/destination_flow.py` | `ea2d75e519436c9073a40cdc5158af2bece23d19f068a306aaf7f7cf6998a01e` | no |
| `execution/PKG-05/DEL-05-01/Work/prototype/schema_subset.py` | `app/contract_inputs/PKG-05/DEL-05-01/Work/prototype/schema_subset.py` | `b4ce8e06934f411bd5ca825a663b2c11e5bd97d2794be01abedf6328360c5142` | no |

`tools/ci/execution-inputs.json` records current physical source/data locations. Specification-data copies remain distinct from the authoring originals; repository checks compare full bytes or the existing selected documentary extents. This move creates no qualification, acceptance, publication, reconstruction or native-run result.
