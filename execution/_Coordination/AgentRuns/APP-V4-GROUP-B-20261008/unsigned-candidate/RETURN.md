# B2 unsigned development candidate — actual build return

**Produced:** an actual incomplete Tauri `.app`, not Python staging. Branch
`codex/app-v4-group-b-unsigned-candidate`, base
`f2e7a2a9ff3ba4e6f5dd0f726766961c8dba1ce1`; actual build inputs are the base App
plus the new overlay. BUILD_INPUTS.json binds all 307 input files, checked equal
to the isolated scratch files after compilation. The final candidate commit
adds the portable overlay/documentation and this evidence; it does not modify
the compiled product source.

Artifact (local, deliberately not committed):
`/private/tmp/chirality-b2-unsigned-build/target/debug/bundle/macos/Chirality App v4 (development candidate).app`.
51 regular files, 31 Mach-O files, about 371 MiB on disk. Complete file/mode
inventory and manifest in BUNDLE_INVENTORY.json. Manifest:
`233ac5fdb7358d8120343751b02302f3864ada9b6b72f396ec76bf3d149e7eab`.

## Actual operations and checks

- Existing prepared Node24.5.0/npm11.5.2 dependencies were read through a
  scratch symlink; no install/download. Rust/cargo1.92.0 used a private target
  and private Cargo home with a read-through registry link to the approved
  restored Group A cache. No shared target was used.
- Frontend TypeScript/Vite build passed; Tauri debug build passed offline and
  locked. A second Tauri `bundle` invocation applied the explicit cached
  supplier directory map. Exact commands, config and exit0 logs are retained.
  Build emitted 29 existing dead-code warnings; no test suite or native behavior
  pass is inferred from compilation.
- CLI2.11.1 help was inspected before the build: both commands expose
  `--no-sign`. Actual logs report signing skipped. Local ld(1) explicitly says
  arm64 linking creates an ad-hoc signature by default. Work paused before
  compilation to identify that consequence; parent then explicitly clarified
  that incidental compiler output is within the authorized offline build.
  No manual signing or account identity was used. Read-only codesign display
  reports `adhoc,linker-signed`, no team, Info.plist not bound and no sealed
  resources. This is unqualified and supplies no SIGN-1/FP-1(b) evidence.
- The merged configuration validates against the installed CLI schema.
  Actual Info.plist matches version0.0.0, existing skeleton identifier and
  proposed minimum15.0. No microphone usage string appears.
- After actual bundling, all42 cached0.160.0 supplier files match by content,
  mode and links; no extra/missing entry; manifest
  `327effb91a5854eccb388321b4b160e059795f0402c553f594e85365189d8d12`.
  This observes FP-1(a)'s comparison operation on this specific incomplete
  development candidate. It is not a qualified pin, signature verification,
  archive provenance, runtime result or complete package handoff.
- P-3's actual guidance and four role files equal source bytes. roles.json is
  absent. P-2 production workflows and shipped-revision manifest are absent.
  Embedded development workflow content remains development-only.

## Remaining contributions

`package_complete:false`. P-0/P-1/P-4 exist; P-3 is partial; P-2 is missing.
The next complete candidate needs production P-2/manifest and P-3 roles.json
from their owners, the applicable A-IN/S1 verification contribution and actual
qualification-pin rule application. Source/config changes require a rebuilt
candidate and affected rechecks. Minimum OS and production bundle identity are
still proposals; the development version is grounded in current source.

No signing/notary credentials, native launch, supplier execution, install,
quarantine or code-mode test was performed. FP-1(b), FP-2/W-4, FP-3/4/5, M2/M3,
SIGN-1 reliance, stage gate, release and human account acts remain absent. The
outer bundle is unsigned notwithstanding its executable's linker signature.

## Provenance and scope

TASK native descendant `/root/group_b_manager/sq_st4_design`, parent
WORKING_ITEMS `/root/group_b_manager`; no delegation. Requested model/effort was
`gpt6astra/low`; this existing child's actual model was not independently exposed
by the task tools, so no model-switch claim is made. Root/TASK/loop and manual
context retained from the preceding bounded assignment; current instructions,
PKG SoW/Design P0–4/CF/FP, app config/build source, Group A cache recovery and
Group B graph were consulted. READ_BASIS.json and tool identities bind origins.

Only new app/packaging/unsigned and run/unsigned-candidate tracked files are
written. Existing Tauri config, App code, Design, A-IN/S1, pins, MEMORY and
instruction files are unchanged. Private-term staged validation is required
before each commit. No push. Independent review/integration belongs to manager.
