# P3 native role-entry follow-on

TASK follow-on under parent `/root/distribution_integration_manager`; no delegation.
Manager `f0072e0a05aced1683291592c9806002f2c6f016` merged non-rewriting as
`c004a907353b9a3a5a6572e6f39407c72cff6799` before implementation.

The parent's explicit follow-on expands the fence to lib.rs role entry/status,
maintained tests, and Cargo.toml's custom-protocol feature. No App setup, hosting,
workflow command or UI changes. Native Tauri mode was chosen after reporting its
actual source: prepared tauri 2.11.1 `is_dev()` returns the inverse of its
custom-protocol feature. Parent approved this standard mode instead of a
release/debug or filesystem-existence heuristic. Cargo now exposes
`custom-protocol = ["tauri/custom-protocol"]`. Production package owner must build
with this feature; merely producing a release/debug executable does not select it.

`thread_start` receives native AppHandle, calls the actual resource_dir/instructions
correspondence gate in production before claim/send, and refuses unavailable,
missing, altered or linked package resources without fallback. The development
route is explicitly labelled development-embedded-candidate and does not consult
package paths. Editable guidance remains separately read and validated. Both start
status objects carry roleSet identity and packageCorrespondence. Pre-send role
preparation failures produce explicit refusal status. host_status exposes roleSet
with roles, defaultRole, identity, availability and candidate/U-R6/U-R11 standing.

New maintained tests exercise good production package, missing package roles,
unavailable native resource root, development route without package fallback,
missing editable guidance refusal, exact identity and four-role/default metadata.
The compiled-mode assertion checks `tauri::is_dev() == !cfg!(feature =
"custom-protocol")`, so running the feature test proves production mode is compiled.
No native window, supplier, credentials, model or actual release invoked.

Checks use prepared offline caches and isolated temporary Cargo target:
- Default mode P3 checks: final 8 passed, including mode assertion.
- `cargo test --offline --locked --features custom-protocol --lib p3_`: 8 passed,
  including the native-mode assertion. This compiled the real production route.
- Initial feature build refused missing frontendDist; actual frontend was built
  with offline npm install and npm run build, both passed. No manifest/lock change.
- `git diff --check` passed. Existing unused/dead-code warnings remain.

Procedural deviation: the non-rewriting merge created its merge commit before the
required staged private-term check. This was reported immediately to the parent;
no rewrite hid it. The official range check over HEAD^1..HEAD then passed14 files,
3 private terms,0 findings. The authored follow-on commit runs the staged official
validator before commit. Configured Ryan C Tufts <ryan@chirality.ai> and absent
GIT_AUTHOR_EMAIL/GIT_COMMITTER_EMAIL/EMAIL overrides verified again.

U-R6/U-R11 remain open at their named owners/points. This is candidate wiring and
offline evidence, not package qualification, release/default decision or adoption.
