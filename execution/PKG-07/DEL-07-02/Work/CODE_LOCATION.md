# Operational source locations

Runnable sources moved outside `execution/`. The declarative contracts, findings, data and historical records stay in this deliverable. Current commands use the operational locations below, from the repository root. Relative imports and specification-data reads use the preserved PKG/DEL/Work structure under `app/contract_inputs/`; native support and signing preparation have their own App homes.

Original source identities are from `109441b501edd86453d263f4207ff6199dbd9a78`. The digest column identifies the original bytes moved in pure-rename commits. Unbound current sources may have separate locator edits; bound sources retain exactly those bytes. Historical citations keep their original locators and are recoverable in Git history.

| Original logical path | Current operational path | Original SHA-256 | Bound bytes |
|---|---|---|---|
| `execution/PKG-07/DEL-07-02/Work/check_account_materialization_v03.py` | `app/contract_inputs/PKG-07/DEL-07-02/Work/check_account_materialization_v03.py` | `4ad6ae3044286df1c1cea58bfc9abf05e862543e42ac8f4a782e0d1fa38fd2b4` | no |
| `execution/PKG-07/DEL-07-02/Work/check_content_review_v02.py` | `app/contract_inputs/PKG-07/DEL-07-02/Work/check_content_review_v02.py` | `53f59b1696077dee954f149833f720429be263df9dacfbaee1dd61d9f667ba93` | no |
| `execution/PKG-07/DEL-07-02/Work/check_contribution_evidence_v01.py` | `app/contract_inputs/PKG-07/DEL-07-02/Work/check_contribution_evidence_v01.py` | `f7895b1778141235c0d71c407254c1aa26a590413557ce00cbdf9234b5c67ba9` | no |
| `execution/PKG-07/DEL-07-02/Work/check_record_reconstruction_v04.py` | `app/contract_inputs/PKG-07/DEL-07-02/Work/check_record_reconstruction_v04.py` | `a55cb0edfae2c82f69cd261b88b72946d13e40d876d651931dc6175efb8005dd` | no |
| `execution/PKG-07/DEL-07-02/Work/check_route_account_v02.py` | `app/contract_inputs/PKG-07/DEL-07-02/Work/check_route_account_v02.py` | `a33214c5d61a91533bd2d64acc054b6091a922e629cafe22da8758b77ae496e1` | no |

`tools/ci/execution-inputs.json` records current physical source/data locations. Specification-data copies remain distinct from the authoring originals; repository checks compare full bytes or the existing selected documentary extents. This move creates no qualification, acceptance, publication, reconstruction or native-run result.
