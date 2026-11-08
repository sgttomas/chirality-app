# Operational source locations

Runnable sources moved outside `execution/`. The declarative contracts, findings, data and historical records stay in this deliverable. Current commands use the operational locations below, from the repository root. Relative imports and specification-data reads use the preserved PKG/DEL/Work structure under `app/contract_inputs/`; native support and signing preparation have their own App homes.

Original source identities are from `109441b501edd86453d263f4207ff6199dbd9a78`. The digest column identifies the original bytes moved in pure-rename commits. Unbound current sources may have separate locator edits; bound sources retain exactly those bytes. Historical citations keep their original locators and are recoverable in Git history.

| Original logical path | Current operational path | Original SHA-256 | Bound bytes |
|---|---|---|---|
| `execution/PKG-01/DEL-01-02/Work/prototype/check_generation_ref.py` | `app/contract_inputs/PKG-01/DEL-01-02/Work/prototype/check_generation_ref.py` | `0db53012909f0e064a408219833e2484ab14c70154986ffa89b458819d1672bd` | no |
| `execution/PKG-01/DEL-01-02/Work/prototype/check_later_protocol_error.py` | `app/contract_inputs/PKG-01/DEL-01-02/Work/prototype/check_later_protocol_error.py` | `675ab6556734fd3bf9a125cca10421937427d61fd424498e255f8f624dc8a204` | no |
| `execution/PKG-01/DEL-01-02/Work/prototype/check_project_context.py` | `app/contract_inputs/PKG-01/DEL-01-02/Work/prototype/check_project_context.py` | `1ba99c0b8a750ba3a2467d78561940b6e2ed24dae27b9f61af46d4687fb7c929` | no |
| `execution/PKG-01/DEL-01-02/Work/prototype/generation_ref.py` | `app/contract_inputs/PKG-01/DEL-01-02/Work/prototype/generation_ref.py` | `23ff8f64ad43fbee297af86ed36ac98b68aea9bf8eb49de22eef0596b63a5701` | no |
| `execution/PKG-01/DEL-01-02/Work/prototype/project_context.py` | `app/contract_inputs/PKG-01/DEL-01-02/Work/prototype/project_context.py` | `f6fb259360d685632d3f54263818fa58224e26575e28f8a717056efe9c42b1f9` | no |
| `execution/PKG-01/DEL-01-02/Work/prototype/recovery_model.py` | `app/contract_inputs/PKG-01/DEL-01-02/Work/prototype/recovery_model.py` | `c9ca3fb1075ebe8e6a3ee64bc5a5a96754339786815bed7910d33378a1da9f6a` | no |
| `execution/PKG-01/DEL-01-02/Work/prototype/run_cases.py` | `app/contract_inputs/PKG-01/DEL-01-02/Work/prototype/run_cases.py` | `38474dd178cca170b1a74fde392c8c86ce38b48a1fa538ee3962b1ece56a4d91` | no |
| `execution/PKG-01/DEL-01-02/Work/prototype/supplier_stub.py` | `app/contract_inputs/PKG-01/DEL-01-02/Work/prototype/supplier_stub.py` | `fd0545fd955ce406d3034e6f44eada8fd1323c5d23726ffc0daaed8164d36fc7` | no |

`tools/ci/execution-inputs.json` records current physical source/data locations. Specification-data copies remain distinct from the authoring originals; repository checks compare full bytes or the existing selected documentary extents. This move creates no qualification, acceptance, publication, reconstruction or native-run result.
