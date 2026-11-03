# Rederived notice selection after the dev-only Cargo.toml change

Main commit `4e942918f1fc4e99140665b2cbb36024c937255e` added the `tauri` `test`
feature (and a comment) under `[dev-dependencies]` in `app/src-tauri/Cargo.toml`.
Runtime declarations, `Cargo.lock`, npm manifests and App `LICENSE.md` are
blob-identical to the previous notice basis `7fdb470b…`. The notice verifier hashes
the full manifest, so it refused the current source. The completed production plan
`app-selected-production-plan-ram3f93n` recorded this as a currentness limit.

Repair, with every change derived by the existing tools:

| Record | Before | After |
|---|---|---|
| `notices/index.json` Cargo.toml digest | `cbf24969…7183` | `32aeb2fa…3638` |
| index basis / App source revision | `7fdb470b…` | `4e942918…` |
| index SHA-256 (metadata `index_sha256`) | `4e27d99c…c3e2` | `fbf873b8…6ac4` |
| `receipts.plan()` SHA-256 | `c2602bbf…4d4d` | `07c32038…b6e1` |
| selection SHA-256 | `43a34ee2…e8e3` | `62b13884…f6da` |
| supplement `manifest.json` SHA-256 | `89a91bd9…c2cb` | `920751ff…79d0` |

`selection.json` keeps the original components and basis text unchanged; only
`plan_sha256` is rebound. `supplement/` was produced by `receipts.py stage`
from the unchanged `../sources` in a separate scratch directory (the stage
command refuses outputs inside the repository), then copied here. The
`LICENSE.md` bytes are identical (SHA-256 `7f976f7e…0c54`). The manifest differs
from the original only in `index_sha256`, `plan_sha256` and `selection_sha256`.
`receipts.py verify --intake <abs>/../sources` reports 11 verified, 0 missing
and 0 errors against the new plan. `check-stage --output <abs>/supplement`
passes. The original `../selection.json`, `../supplement/` and `../receipt.json`
are retained as truthful records bound to the old plan; the original supplement
now refuses `check-stage`.

No download, build, signing or launch was performed. Standing and limits are
unchanged from [SCOPE.md](../SCOPE.md): this is a technical selection, not legal
approval. Full terms, copyright coverage, the Apple SDK question, transitive
coverage and the four supplier associations remain open. No candidate has
consumed this supplement yet.
