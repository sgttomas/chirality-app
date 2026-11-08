# Operational source locations

Runnable sources moved outside `execution/`. The declarative contracts, findings, data and historical records stay in this deliverable. Current commands use the operational locations below, from the repository root. Relative imports and specification-data reads use the preserved PKG/DEL/Work structure under `app/contract_inputs/`; native support and signing preparation have their own App homes.

Original source identities are from `109441b501edd86453d263f4207ff6199dbd9a78`. The digest column identifies the original bytes moved in pure-rename commits. Unbound current sources may have separate locator edits; bound sources retain exactly those bytes. Historical citations keep their original locators and are recoverable in Git history.

| Original logical path | Current operational path | Original SHA-256 | Bound bytes |
|---|---|---|---|
| `execution/PKG-03/DEL-03-01/Work/prototype/run_fixture.py` | `app/contract_inputs/PKG-03/DEL-03-01/Work/prototype/run_fixture.py` | `88b8a5300320b793ffd403a76b59e2be0b800fa0851486c8f10478906b22c050` | no |
| `execution/PKG-03/DEL-03-01/Work/prototype/run_swbpipe_profile.py` | `app/contract_inputs/PKG-03/DEL-03-01/Work/prototype/run_swbpipe_profile.py` | `4be14a4f240227def11a96337c651c89fa2384c808c7d0f163d109b13042474e` | no |
| `execution/PKG-03/DEL-03-01/Work/prototype/schema_subset.py` | `app/contract_inputs/PKG-03/DEL-03-01/Work/prototype/schema_subset.py` | `d65b90796f13ad5417865c2478d40d478f1a0d55470a8ca27bd0a25cf7568723` | no |
| `execution/PKG-03/DEL-03-01/Work/prototype/simhost.py` | `app/contract_inputs/PKG-03/DEL-03-01/Work/prototype/simhost.py` | `27693ccf00e0baa9b80475c609342cddb4c026f332d899bfc980e1eb25447434` | no |
| `execution/PKG-03/DEL-03-01/Work/prototype/simhost_swbpipe.py` | `app/contract_inputs/PKG-03/DEL-03-01/Work/prototype/simhost_swbpipe.py` | `c84eaf353fa7445e7fbee66a29c2abec3b52573f8f90804fd40d1f642012d768` | no |
| `execution/PKG-03/DEL-03-01/Work/prototype/validate_all.py` | `app/contract_inputs/PKG-03/DEL-03-01/Work/prototype/validate_all.py` | `7f64d33c247ba3f78bc3755a2b7578f4bdb3e02e980bda6710bb22cea2a21aa9` | no |

`tools/ci/execution-inputs.json` records current physical source/data locations. Specification-data copies remain distinct from the authoring originals; repository checks compare full bytes or the existing selected documentary extents. This move creates no qualification, acceptance, publication, reconstruction or native-run result.
