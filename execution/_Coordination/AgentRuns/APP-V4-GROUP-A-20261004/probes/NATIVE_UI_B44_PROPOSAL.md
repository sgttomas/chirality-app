# Prepared native UI inspection — b44 file-act build

Status: built and not launched. Source `b44f6bfc1aa435d1160cc2701db46a54bd958a3c`, now included in merged PR1099 (`c1571f7febcb4b710c8aa5633f1f5c4460c3faf3`). Full source archive passed550 top-level Rust checks, Node3, frontend and schema6; independent core/consumer reviews are recorded. This is an unsigned development bundle, not release qualification.

- App: `/private/var/folders/0s/50y7rb796d1bqdxmpcz6qg800000gn/T/chirality-v4-ui1099-lgcc5ir5/Chirality v4 Fixture Probe.app`.
- Main binary SHA-256: `b41b885ce8acd7700dca3a204b9c3f0fe7177a8cdec018bd4af864a80c8d5f2f`.
- Overlay SHA-256: `bfdb3d3e2fe1f6991f9f5edcf9caa7d03ea884ea49a4770885f65a5118925736`.
- Distinct App identifier: `dev.chirality.v4.ui1099`; its own test App-data folder may be created.
- Physical workspace: the same temporary root's `workspace/`, containing only `notes/native-ui-test.txt` with an explicit synthetic-test statement.
- Offline locked build succeeded; signing explicitly skipped; detached bundle copied before releasing the shared build target.

Requested operation: launch with normal macOS process permissions; inspect workflow/file-act panels and storage status; select only the supplied synthetic fixture; inspect the offer, open and dismiss native confirmation; check the resulting display/absence of captured acts; close the App. Supplier/home environment is removed. No Codex process, model, sign-in or credential operation is configured.

The agent will not confirm positive acts or declines, register workflows, touch real project files, or claim a human/engineering act from automation. Dismiss-only inspection tests controls and cancellation; actual human capture remains a separate witness. This request concerns this new artifact. The earlier approval covered the older196914 bundle, and the earlier automatic approval review required direct permission for an unsigned App launch outside the command sandbox.
