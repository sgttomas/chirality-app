# Proposed common Windows development environment

Status: owner-reviewable proposal, 2026-10-28 local / 2026-10-29 UTC. No
installer or package payload was downloaded and nothing was installed in the
guest. App's WORKING_ITEMS manager owns this proposal and any subsequently
authorized common-guest provisioning. Agent 0 carries the owner decision and
cross-project agreement. This document does not authorize execution.

## Decision proposed

Use the existing Windows 11 ARM64 guest, **native ARM64 development tools and
x64 application output**, for development and explicitly labelled emulated-x64
execution. Keep x64 on an actual x64 Windows machine as a proposed later
verification target; Parallels ARM results cannot establish that evidence.
Use separate guest-native NTFS App and SWBPIPE checkouts, Cargo targets, npm
trees and scratch Codex homes. Do not use Mac shared mounts for custody,
locking, recovery or crash/reopen witnesses.

Select VS Build Tools **2022 17.14.43 Current**, build `17.14.37824.6`, subject
to the acquisition-integrity hold below. **17.14 LTSC does not exist.**
Microsoft's release history explicitly keeps 17.14 Current supported through
January 13, 2032. Using an older LTSC is not the proposed correction.

The selected architecture combination is documented as supported: the Build
Tools system requirements include Arm64 Windows; Visual Studio's ARM guide
documents `HostARM64\\x64`, `HostARM64\\ARM64` and `HostARM64\\x86` compilers.
The ARM64 target tools are needed even for x64 App output because Rust build
scripts and proc macros execute on the native ARM64 Rust host. Availability
on this particular guest still needs an installed-tool verification.

## Observed environment and source identity

App basis: `36bd5d6eecbe1b835249cfce2722c0710f777c20`, branch
`t3/windows-feasibility`. The required baseline is HEAD and the initial tree
was clean; no baseline merge was needed. Selected instruction library:
`/Users/ryan/dev/chirality` at `1560bbf7f7add4637a20572a2b0d404ef121af63`.
Consultation selects instructions, not product asset updates.

The manager independently observed macOS 26.6.2 build 25G83, arm64,
137,438,953,472 bytes RAM, Parallels 27.0.2 (58673), and one running Windows
11 guest. Read-only PowerShell via `prlctl exec`, with no username/password,
returned Windows 11 Pro `10.0.26200`, ARM64, 34,353,119,232 bytes RAM and
WebView2 `156.0.4314.50`. `Get-Command` returned no Rust/cargo/rustup,
Node/npm, Git or cl, and the queried Windows Kits registration was absent.
These are PATH/registration observations, not proof of machine-wide absence.
Read-only logical-disk metadata identifies guest `C:` as NTFS, size
273,214,861,312 bytes, free 216,054,390,784 bytes at observation; no shared-mount
or directory-content examination was needed.
PowerShell's ordinary module initialization is not a controlled App witness.

SWBPIPE separately reported the same guest/platform facts, no VS Installer,
and no CMake, pwsh or winget on PATH. Those extra absence claims remain peer
evidence. No need for CMake, pwsh or winget was established for this initial
lane; they are not proposed installations. Reuse existing WebView2, subject
to a Tauri/Wry launch witness; do not reinstall it by default.

SWBPIPE source is read-only checkout
`/Users/ryan/.t3/worktrees/chirality/t3-514d37a1`, branch
`codex/swbpipe-windows-feasibility`, revision
`1560bbf7f7add4637a20572a2b0d404ef121af63`, project
`projects/chirality-piping`. Agent 0 checked the supplied pins and committed
bytes. The manager rechecked relevant acquisition-input diffs against that
revision: no differences. Peer-reported dirty `docs/CI_STRATEGY.md`, untracked
`.github/workflows/piping-windows-core.yml` and
`execution/PKG-10/DEL-10-04/Design/` are not dependency inventory inputs.
Inventory uses `git show <revision>:<path>`, not changing working files.

## Proposed toolchain and acquisitions

Full URLs, hashes, byte measurements and source pins are saved in
[`windows-feasibility/acquisition-inputs.json`](windows-feasibility/acquisition-inputs.json)
and [`windows-feasibility/repository-packages.json`](windows-feasibility/repository-packages.json).
Sizes below are bytes; HEAD sizes describe compressed transfers, GitHub
asset sizes are publisher metadata, and cached sizes are local measurements.
None is a payload verification performed in this tranche.

| Item | Proposed version / architecture | Acquisition and size basis |
|---|---|---|
| VS Build Tools bootstrapper | 17.14.43 / installer detects ARM64 | Fixed-version Microsoft URL in the JSON; HEAD 4,474,088; **not the installation total** |
| C++ workload | `Microsoft.VisualStudio.Workload.VCTools` | Required dependencies only; do not add `--includeRecommended` or `--includeOptional` |
| x64/x86 output tools | `Microsoft.VisualStudio.Component.VC.Tools.x86.x64` | Catalog component 17.14.36510.44; includes `Microsoft.VisualCpp.Tools.HostARM64.TargetX64` |
| ARM64 host build tools | `Microsoft.VisualStudio.Component.VC.Tools.ARM64` | Catalog component 17.14.36510.44; includes ARM64EC dependency; no ARM64EC App output proposed |
| Windows SDK | `Microsoft.VisualStudio.Component.Windows11SDK.26100` | Catalog component 17.14.37011.9 advertises SDK **10.0.26100.7705**; verify actual installed SDK/tool versions |
| Rust bootstrap | rustup-init 1.29.2 / ARM64 MSVC | `static.rust-lang.org/rustup/archive/1.29.2/aarch64-pc-windows-msvc/rustup-init.exe`; HEAD 11,277,824 |
| Rust compiler | 1.97.1 / `aarch64-pc-windows-msvc` | Pinned release 2026-07-16; rustc 61,558,480; cargo 9,981,000; host std 22,621,952 |
| Extra Rust std | 1.97.1 / x64 MSVC and wasm32 | x64 std 22,603,560; wasm std 21,949,220; no second x64 host toolchain proposed |
| Node/npm | Node **24.18.0**, Windows ARM64 ZIP | Matches observed App development Node patch; official ZIP HEAD 33,361,856; retain bundled npm and record its version on extraction |
| Git | **2.56.0.windows.4**, ARM64 | Official `Git-2.56.0.4-arm64.exe`; GitHub asset 64,406,136; retain full runtime layout |
| wasm-bindgen CLI | **0.2.123**, x64 MSVC prebuilt | Official release `wasm-bindgen-0.2.123-x86_64-pc-windows-msvc.tar.gz`; 7,554,935; runs through guest x64 emulation |
| WebView2 | existing 156.0.4314.50 | Reuse; zero new payload proposed |
| Codex supplier | **0.160.0**, complete Windows x64 npm platform package | Published npm alias resolves `@openai/codex@0.160.0-win32-x64`; compressed HEAD size unavailable; published unpacked 450,619,016 |

Node 24 satisfies both current Vite 7 lanes; no lock update is proposed. The
wasm-bindgen release contains an x64 Windows prebuilt and no ARM64 Windows
prebuilt. Prefer that exact binary over `cargo install`; this avoids an
unbounded new CLI build dependency graph. Native ARM64 Node, Git and Rust
are available. An all-emulated-x64 host toolchain is an alternative only if
native-tool interoperability fails and the owner selects it; this proposal
does not silently add a second toolchain.

Codex also publishes the ARM64 Windows npm alias, unpacked 389,339,784 bytes.
Its existence is metadata evidence, not execution or App qualification. Acquire
one complete x64 platform package initially to exercise the proposed x64
target. Do not substitute a lone GitHub `codex.exe`, `codex-app-server.exe`,
or another differently assembled archive without reconciling the supplier
layout and identity. The existing App expected supplier reference is **macOS
ARM64 only** and cannot authenticate Windows bytes. The helper/code-mode
layout must be inventoried before use. Installing or enabling a Windows
sandbox service is not part of this credential-free handshake proposal.

## Acquisition integrity hold and complete size budget

Microsoft channel metadata identifies the 17.14.43 catalog as 30,443,792 bytes,
SHA-256 `5bd3b0b2ae509af2e9559b852f78545df0bf2c081dd850caed76f1dc134c511e`.
Two GETs of that exact official metadata URL, including an identity-encoding,
no-cache retry, instead returned 17,954,808 bytes, SHA-256
`87791000b1d6357e174f039ce9c2f03d150d4e90b45e8e52468d797dac62022c`.
The decoded catalog identifies the same version, but that does not resolve
the mismatch. Do not use these bytes as authenticated installation authority.
Resolve the channel/catalog join before acquiring or executing VS payloads;
do not bypass verification or guess that JSON formatting explains it.

A subsequent independent Type 2 metadata investigation reproduced the same
catalog bytes through a raw HTTP capture with normal TLS verification,
`Accept-Encoding: identity`, no automatic decompression, no redirects and
no response Content-Encoding. Agent 0 rechecked the saved body and channel
digests. This rules out client-side decompression for that capture; it does
not identify whether origin publication, caching or an intermediary produced
the discrepancy. Original collection provenance remains unavailable. Embedded
signature presence and the matching version label are not signature or payload
verification. No authenticated alternative or proposed repin was established.
The independent capture identities and remaining verification boundary are
recorded in `windows-feasibility/acquisition-inputs.json`; raw evidence and
the report remain in `/tmp/chirality-vs-forensics.7BqOwdJ1/`. Further identical
retries are not a resolution. Obtain an official matching catalog/reference
and establish its verification procedure before relying on this acquisition.

For planning only, a deliberately conservative traversal of that **unverified**
catalog follows required dependencies from the product, VCTools workload and
three explicit components above. It retains *all* versions, architectures and
languages for reached IDs, excludes optional/recommended dependencies unless
explicitly selected, and deduplicates payloads by SHA-256. It reaches 354 IDs,
1,671 payloads, **2,691,378,431 compressed bytes** and summed publisher
`installSizes` of **8,428,814,829 bytes**. This is not Installer resolution.
Reserve a proposed **4 GiB VS transfer cap** for these payloads plus engine,
channel/catalog and bootstrap dependencies; stop before exceeding it or adding
components, and return a revised manifest/budget. The cap is an estimate and
proposed authorization ceiling, not an observed download total. Microsoft's
generic Build Tools installed-space range is 2.3–60 GB; for this selection
reserve **15 GiB installed/cache space initially**, an estimate to revise
after verified layout resolution. Check guest free space first. No VM disk
resize is authorized.

The six Rust bootstrap/minimal-profile/extra-target archives total
**149,992,036 bytes**. Node, Git and wasm-bindgen add **105,322,927 bytes**.
These known non-VS tool transfers total **255,314,963 bytes**; metadata,
signatures and checksums add small separate transfers. Rust archive unpacked
sizes are not published in the consulted manifest. Reserve 2 GiB installed
for Rust/Node/Git/CLI as an estimate, plus separate build-output space.
Do not mistake these totals for both repositories' full acquisition budget.

Repository dependency budgets and unknown compressed sizes are recorded in the
JSON inventory. Use a **deduplicated lockfile superset**, including ARM64 host
build dependencies and all optional platform entries, rather than claiming an
exact resolver closure. Local cached archives may be copied only after their
lock checksums match; transfer source archives, never Mac node_modules or
compiled host artifacts. Registry HTTP HEADs did not provide npm compressed
lengths. The union contains **533 unique crate archives, 93,102,665 bytes**,
all locally cached and checksum-verified. It contains **354 npm archives**;
246 are cached with matching SRI, **59,984,300 compressed bytes**, and the
remaining 108 have **818,928,935 published unpacked bytes** with unknown
compressed sizes. This includes all platform optionals and is intentionally
larger than a Windows ARM host resolution. Propose a **1 GiB npm acquisition
cap** for the whole superset and a separate **512 MiB cap** for the single
complete Codex x64 archive. These are conservative estimates/stop limits, not
measurements or permission to fetch. Copying verified cached archives can
reduce new downloads; do not assume the guest already has those caches.

Together with 4 GiB VS and the 255,314,963 known tool bytes, propose an
**overall 6 GiB transfer ceiling**, including crate archives and metadata;
stop and revise before exceeding any component cap. Exact npm/Codex
compressed lengths are still unknown, and the VS integrity hold still applies.
This is a concrete plan for owner review, **not a ready request to execute
unverified VS acquisition**. Scope excludes browser downloads,
Tauri bundling/signing/installers and cargo-install CLI expansion.

Peak guest-space planning must include simultaneous inputs and outputs, not
just installed programs. The following **estimates are operating envelopes**,
not vendor minimums or measured Windows footprints. The vendor catalog's
8,428,814,829-byte installSizes sum remains unverified; Microsoft's generic
2.3–60 GB range is the only consulted system-wide published installed range.

| Simultaneously retained component | Proposed space envelope |
|---|---:|
| VS downloaded layout, metadata and engine/bootstrap inputs | 4 GiB |
| Installed VS, SDK and machine package cache | 15 GiB |
| Rust/Node/Git/CLI acquisition archives | 1 GiB |
| Installed Rust toolchain/targets, Node, Git and wasm-bindgen | 2 GiB |
| Separate per-project compressed registry/npm caches, including duplication | 3 GiB |
| Extracted Cargo source trees and separate npm dependency trees | 4 GiB |
| Two source checkouts and Git object stores | 5 GiB |
| Extracted complete Codex supplier | 1 GiB (publisher x64 unpacked size 450,619,016 bytes) |
| App Cargo dev/test outputs | 20 GiB |
| SWB core/desktop/wasm outputs across its separate roots | 20 GiB |
| Invented fixtures, scratch homes, recovery DBs and bounded logs | 3 GiB |
| **Subtotal / rounded peak envelope** | **78 GiB / 80 GiB** |

Require **100 GiB free on guest-native NTFS before provisioning**: the rounded
80 GiB peak plus a 20 GiB OS/user headroom reserve. The observed free space is
about 201 GiB, so it passes this planning threshold at observation time only.
Recheck immediately before execution. Actual archive/layout/install/dependency
and target-directory sizes must be recorded at each gate; if an envelope is
unsupported or would be exceeded, stop that step and revise the proposal
before proceeding. Do not delete user files, silently share mutable caches,
resize the VM disk or count future cleanup as already freed space. OS updates,
other applications and later release/bundler/browser outputs are outside this
envelope and must not consume the reserved headroom unnoticed.

## Repository roots and package requirements

App uses `app/{package.json,package-lock.json}` and
`app/src-tauri/{Cargo.toml,Cargo.lock,build.rs,tauri.conf.json}`. Its lock has
484 registry crates and 136 npm entries across platforms. All 484 `.crate`
archives are present locally, checksum-verified, totalling 86,865,082 bytes;
77 npm archives are locally present with matching integrity, 23,116,586 bytes.
Windows ARM64 npm native optionals include Tauri CLI 2.11.1, esbuild 0.28.1
and Rollup 4.62.2; those ARM64 packages are not in the observed Mac npm cache.
SQLite is bundled source, so MSVC and SDK headers/libraries are required.
React/Vite portability does not make Rust or native controls portable.

SWBPIPE initial core roots, each with its own adjacent Cargo.lock, are
`core/solver/{frame_kernel,curved_bend,sparse_direct}`,
`core/serialization/canonical_json` and `core/product_physics`. The first four
use default test/dev features/profiles; product_physics uses default `check
--lib`. Desktop diagnosis uses `apps/desktop/src-tauri`, default features,
dev profile, `native-smoke` OFF. Follow its current local path dependencies
under `core`; no root Cargo workspace is implied. Wasm roots are
`core/model_operations/operation_applier` and `core/loads/self_weight_wasm`,
features `wasm`, release profile, `wasm32-unknown-unknown`, then the exact
wasm-bindgen CLI. Frontend npm workspace root is `projects/chirality-piping`,
with `apps/desktop` as local workspace. The eight current Cargo locks and
workspace npm lock, not historical provenance/build-artifact locks, define
the recorded inventory. No git/custom registry source was found in those
locks. Do not import host user configuration or credentials.

Python availability in the guest was **not established**. `app/README.md`
requires Python 3 for schema and supplier checks, and some existing tests invoke
`python3`. This initial acquisition proposal deliberately defers those Windows
checks: native compile-blocker discovery and the Vite build do not authorize
claiming the deferred suite passes. Keep Python-dependent checks **not run**.
Before a later fixture/supplier-check gate depends on them, inspect nonsecret
`py`/`python`/`python3` command availability and actual interpreter identity;
if no compatible interpreter exists, pin and budget an official Python
acquisition through a revised owner-reviewed proposal. Resolve the Windows
command-name/harness differences without removing checks or silently treating
the Store execution alias as an installed interpreter. No Python payload is
included or authorized here.

SWBPIPE's `/bin/ps` and process-group worktree build-lock guard is a known
Windows blocker. Port it in its owning repository before claiming a full
frontend/wasm build; never bypass it. SWBPIPE owns its fixes and build evidence.

## Ordered execution plan, after exact owner authorization

1. Resolve the VS metadata mismatch; refresh fixed catalog/channel identities,
   component closure, engine dependencies and package budget. Confirm the
   fixed bootstrapper's ProductVersion and Microsoft Authenticode signature.
   Record approvals naming files/sources/size caps, including secondary VS
   payloads and repository archives. Public metadata research is the only
   network work authorized by the current brief.
2. Read guest-native NTFS filesystem and free-space facts, existing installation
   inventory and pending-reboot status. Coordinate a provisioning window through
   Agent 0; do not reset, power off, resize or close user applications. Any
   reboot requirement is a return condition, not permission to reboot.
3. Acquire a pinned en-US ARM64-aware VS layout with the VCTools workload and
   explicit x64/x86, ARM64 and SDK components; omit recommended/optional sets.
   Verify payload hashes/signatures and actual layout size before install;
   retain a receipt. Use that layout offline for the guest install. Reconcile
   any newly required engine payload before acquisition.
4. Extract the pinned Node ARM64 ZIP, install the selected Git ARM64 runtime,
   and provision rustup 1.29.2 without automatic Visual Studio prerequisites or
   PATH/profile modification. Use isolated task CARGO_HOME/RUSTUP_HOME,
   explicit paths and recorded process environments. Install toolchain
   `1.97.1-aarch64-pc-windows-msvc` with
   `--profile minimal`, x64 and wasm std; do not add docs/rustfmt/clippy.
5. Extract the official wasm-bindgen x64 prebuilt. Check `rustc -vV`, cargo,
   node/npm, Git and `wasm-bindgen --version`. From the ARM64 native tools
   environment, compile and execute tiny invented ARM64 and x64 C/Rust probes,
   inspect PE architecture, and identify native versus emulated execution.
   Confirm SDK headers, libraries and HostARM64 linkers, not just PATH entries.
6. Populate separate per-project caches from checksum-verified source archives
   and explicitly approved missing archives; use `npm ci --offline` and
   `cargo ... --offline --locked`. Keep npm lifecycle behavior scoped to known
   packages; skip Playwright browser provisioning. Run SWB's bounded core tests
   first, then shell diagnosis and App Windows compile-blocker discovery. Each
   manager owns its checkout, features, output directory and result attribution.
7. Inventory the entire selected Codex x64 package, verify npm integrity,
   preserve helpers/resources and use fresh invented workspace/home/config.
   Establish outbound-network denial on Windows before any supplier execution;
   do not assume a localhost provider setting blocks startup traffic. Then
   record version, stdio initialize/initialized, controlled stop and zero login,
   thread or model requests. A stand-in cannot supply this witness.
8. Only after platform-service implementation/regressions and independent
   scrutiny, join App launch, supplier handshake/stop, durable invented fixture,
   reopen/validation and native-control smoke. Existing unavailable branches
   remain truthful until replaced and witnessed. No acceptance/release follows
   from tool installation or build success.

Integrity plan: use release-manifest SHA-256 for Rust archives and bootstrap,
Node signed SHASUMS plus archive hash, GitHub-published SHA-256 for Git/wasm
assets plus Windows publisher signatures where applicable, npm lock/SRI and
registry signing/provenance metadata for npm archives, and VS signed
channel/catalog plus every payload hash and Authenticode. Publisher metadata
was read; signatures and payloads were not verified here. Halt on any mismatch.

Official references consulted: [VS release history](https://learn.microsoft.com/en-us/visualstudio/releases/2022/release-history),
[VS ARM guide](https://learn.microsoft.com/en-us/visualstudio/install/visual-studio-on-arm-devices?view=vs-2022),
[Build Tools requirements](https://learn.microsoft.com/en-us/visualstudio/releases/2022/system-requirements#microsoft-visual-studio-build-tools-2022-system-requirements),
[component IDs](https://learn.microsoft.com/en-us/visualstudio/install/workload-component-id-vs-build-tools?view=vs-2022),
[Rust 1.97.1 manifest](https://static.rust-lang.org/dist/channel-rust-1.97.1.toml),
[Node 24.18.0](https://nodejs.org/dist/v24.18.0/SHASUMS256.txt),
[Git release](https://github.com/git-for-windows/git/releases/tag/v2.56.0.windows.4),
[wasm-bindgen 0.2.123](https://github.com/wasm-bindgen/wasm-bindgen/releases/tag/0.2.123),
[Codex npm pin](https://registry.npmjs.org/@openai%2fcodex/0.160.0).
