# Operational source locations

Runnable sources moved outside `execution/`. The declarative contracts, findings, data and historical records stay in this deliverable. Current commands use the operational locations below, from the repository root. Relative imports and specification-data reads use the preserved PKG/DEL/Work structure under `app/contract_inputs/`; native support and signing preparation have their own App homes.

Original source identities are from `109441b501edd86453d263f4207ff6199dbd9a78`. The digest column identifies the original bytes moved in pure-rename commits. Unbound current sources may have separate locator edits; bound sources retain exactly those bytes. Historical citations keep their original locators and are recoverable in Git history.

| Original logical path | Current operational path | Original SHA-256 | Bound bytes |
|---|---|---|---|
| `execution/PKG-01/DEL-01-06/Work/prototype/check_pkg.py` | `app/contract_inputs/PKG-01/DEL-01-06/Work/prototype/check_pkg.py` | `1b6f1232fe0b200ffbb0eb56dfbbdfe4a4f29dab3c83e8e1d42b195d752f8d23` | yes |
| `execution/PKG-01/DEL-01-06/Work/prototype/read_tree.py` | `app/contract_inputs/PKG-01/DEL-01-06/Work/prototype/read_tree.py` | `6dacea788f0a0690ca04bc95f4d50332f4d3ddafb5bb0339147460e64b2debdb` | yes |

`tools/ci/execution-inputs.json` records current physical source/data locations. Specification-data copies remain distinct from the authoring originals; repository checks compare full bytes or the existing selected documentary extents. This move creates no qualification, acceptance, publication, reconstruction or native-run result.

Retained Python source `execution/PKG-01/DEL-01-06/Work/unsigned-release-input-build/12d26b8db5-278899dad62e/build-driver.py.txt` now has physical location `tools/historical_reconstruction/unsigned_release_input_build/12d26b8db5-278899dad62e/build-driver.py.txt`, with unchanged SHA-256 `2f97e7894e40f16c275beb8667fe07f53b45b9f79d0e70ad559b1809104ee51e`. Original historical citations retain their logical identity through Git history. It was moved without execution; no historical build, receiving observation or acceptance is reconstructed.
