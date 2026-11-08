# Operational source locations

Runnable sources moved outside `execution/`. The declarative contracts, findings, data and historical records stay in this deliverable. Current commands use the operational locations below, from the repository root. Relative imports and specification-data reads use the preserved PKG/DEL/Work structure under `app/contract_inputs/`; native support and signing preparation have their own App homes.

Original source identities are from `109441b501edd86453d263f4207ff6199dbd9a78`. The digest column identifies the original bytes moved in pure-rename commits. Unbound current sources may have separate locator edits; bound sources retain exactly those bytes. Historical citations keep their original locators and are recoverable in Git history.

| Original logical path | Current operational path | Original SHA-256 | Bound bytes |
|---|---|---|---|
| `execution/PKG-02/DEL-02-03/Work/prototype/checkpoint_recorder.py` | `app/contract_inputs/PKG-02/DEL-02-03/Work/prototype/checkpoint_recorder.py` | `303ff2de49f2a68504bd2698aced958ca504ca01b35330d4e6511971bf08c9f0` | no |
| `execution/PKG-02/DEL-02-03/Work/prototype/fx_double.py` | `app/contract_inputs/PKG-02/DEL-02-03/Work/prototype/fx_double.py` | `97e1cb1ab6525dd9ab5fa3eca841b258e98b44b7c33deca4e3806cdbba1274e9` | no |
| `execution/PKG-02/DEL-02-03/Work/prototype/jsonschema_subset.py` | `app/contract_inputs/PKG-02/DEL-02-03/Work/prototype/jsonschema_subset.py` | `6c6ff7634016deb22742444c72ccf7b05f1c1831491fc7a0570ae6f2c87e1a17` | no |
| `execution/PKG-02/DEL-02-03/Work/prototype/required_tool_check.py` | `app/contract_inputs/PKG-02/DEL-02-03/Work/prototype/required_tool_check.py` | `3d889b5477535c8973c83e1bf83ac3ceb9390648d3b2450109ae235faf88f0c7` | no |
| `execution/PKG-02/DEL-02-03/Work/prototype/run_all.py` | `app/contract_inputs/PKG-02/DEL-02-03/Work/prototype/run_all.py` | `3514fd0a42277baa3d2a18d1ade1db5715bddfbdabde570824bbcfcac0fd22f4` | no |

`tools/ci/execution-inputs.json` records current physical source/data locations. Specification-data copies remain distinct from the authoring originals; repository checks compare full bytes or the existing selected documentary extents. This move creates no qualification, acceptance, publication, reconstruction or native-run result.
