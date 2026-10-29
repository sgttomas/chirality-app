# Windows feasibility: first tranche

This is development investigation and a proposed implementation sequence under
`execution/_Coordination/WINDOWS_UNDERTAKING.md`. It establishes no Windows
shipping promise, support architecture, supplier qualification, owner
acceptance or release. Existing macOS v4.0 commitments continue to apply.

Source inspected: `36bd5d6eecbe1b835249cfce2722c0710f777c20`, the required
baseline and clean initial HEAD on `t3/windows-feasibility`. The instruction
source is repository `AGENTS.md` / `loop/LOOP_INIT.md` and shared Chirality
`1560bbf7f7add4637a20572a2b0d404ef121af63` WORKING_ITEMS and coordinated
knowledge-work. Packaged roles/workflows were not updated. Investigation date:
2026-10-28 local / 2026-10-29 UTC.

## Finding and immediate execution basis

Windows development can proceed in bounded platform-service slices alongside
macOS. The initial connected Windows slice is **not executable yet**: the
existing ARM64 guest lacks the selected build toolchain on PATH/registration,
and the current Rust implementation has substantial Unix-only custody and
persistence code. Installing tools alone will not supply parity.

The [common provisioning proposal](WINDOWS_PROVISIONING.md) records actual
guest observations, exact candidate versions/architectures, official sources,
source-pinned App/SWBPIPE dependency inventories, size measurements/estimates,
verification order and a concrete acquisition-integrity blocker. No Windows
installer/package payload, sign-in, model turn, guest installation or VM
reconfiguration occurred. Existing WebView2 is reusable pending a native
launch witness. Windows x64 remains a proposed primary verification target;
this ARM guest provides separately labelled emulated-x64 evidence.

## Executed checks and their limits

All development/test Codex homes were fresh `mktemp -d` scratch directories;
`~/.codex` was not used. Cargo and npm execution was offline. Public
documentation, release metadata, checksums and HTTP HEAD requests were read
only under Agent 0's subsequent metadata-research authorization.

| Check | Observed outcome | What it establishes |
|---|---|---|
| Baseline ancestor/HEAD and initial Git status | Required baseline equals HEAD; clean | Valid source basis; no merge needed |
| `python3 -m tools.deliverables --project . check` | 41 deliverables; no errors; six declared cycle groups | Graph representation consistency; no completion evidence from cycles |
| `neighborhood DEL-01-01`, `impact DEL-01-01` | Captured to scratch; 37 downstream affected deliverables | Large reach warrants bounded platform interfaces; not 37 immediate code edits |
| `npm ci --offline --no-audit --no-fund --ignore-scripts` in `app/` | 77 packages installed from prepared cache | Mac host dependencies available without downloads |
| `npm run build` | TypeScript + Vite pass, 58 modules; existing >500 kB bundle warning | Portable web build on Mac; no Windows WebView/native witness |
| `cargo check --offline --locked --manifest-path app/src-tauri/Cargo.toml` | Pass, Rust 1.97.1, Mac arm64; 78 warnings | Current native source compiles for the existing host |
| Same check with `--target x86_64-pc-windows-msvc` | Blocked in `libsqlite3-sys 0.30.1` C build: Windows-target `cc` cannot find `stdlib.h` | Mac cross-build lacks Windows C/SDK setup; App Rust compilation not reached, not an App Windows compile pass |
| `python3 src-tauri/schemas/sync.py` in `app/` | 11 schema resources match source bytes, hashes and IDs | Maintained schema consistency; no regeneration or adoption |
| `node --test tests/native-waiting.test.mjs tests/attachment-outcome.test.mjs` in `app/` | 34 tests pass; actual Rust fixture producers and mounted UI replay | Invented Mac Host/IPC/native-menu projection and attachment outcome regressions; no real native person control, Windows or supplier witness |
| App/SWBPIPE package inventory | Relevant peer input diff clean; committed locks parsed; 533 unique crate archives checksum-verified locally | Conservative combined source-package superset; not a solved Windows feature/platform closure |

Scratch for this execution: `/tmp/chirality-windows-feasibility.j4dTDO`.
It contains concise build logs, captured graph JSON and public metadata.
The Node regression output was observed directly; it was not saved as a
separate raw log. Scratch is disposable evidence, not governing instructions.
Saved acquisition/source-pin data lives beside this document. Reproduction
requires the prepared caches documented in `app/README.md`; the shared
Chirality instruction checkout is not a build/test dependency.

Windows App launch, stock supplier initialize/initialized, controlled supplier
stop, durable fixture publication/reopen, and native-control smoke are all
**not run**. No mock, Mac test or cross-compilation result substitutes for
them. No supplier was executed in this tranche. Windows credential/access
presentation and distribution remain outside the first credential-free slice.

## Verified source boundaries and proposed services

These are source observations, followed by proposed Windows mechanisms. The
mechanisms have not been proven by Windows execution. Keep Rust ownership of
file writes, records, supplier interaction and human-act capture under the
owner's OI-008 ruling; React remains presentation and person-initiated IPC.

### Process custody — DEL-01-01 / DEL-01-02

`app/src-tauri/src/process_group_custody.rs:3,57,136,258,367,415` uses Unix
process groups, `waitid(...WNOWAIT)` and signals. It retains the actual spawned
child reservation, binds it once to full `{appSession, home, spawnCounter}`
generation identity and refuses numeric group operations without that custody.
The member census is macOS-specific. An unavailable census yields
`checked:false,surviving:null`, never an invented zero; detached/escaped
descendants are unobserved. `hosting.rs:3857,3974` separates ready EOF,
startup handshake failure, leader exit, replacement and deliberate stop.
Unexpected ready EOF records survivors without automatically killing them;
deliberate Stop can force the original owned group. EOF does not prove exit.
See HOSTING §§3–4 and RECOVERY U-16/current implementation conditions.

Proposed seam: an opaque capability minted by actual spawn and bound once to
the generation, with leader exit observation, contained-member observation
(`complete` or `unknown` with reason), explicit stop/force facts and safe
retirement. It must not accept a persisted PID as fresh authority. A Windows
Job Object is a candidate: establish assignment before child code can spawn,
test nested jobs and breakaway policy, retain process/job handles, and refuse
or clean up a failed assignment before reporting ready. Merely calling
`taskkill /T`, killing the leader or searching process names loses custody.

Specify four events independently: protocol EOF, leader exit, intentional
stop and App death. Kill-on-job-close may change App-parent-death behavior;
killing on leader exit would change current ready-EOF survivor treatment.
Do not select either silently. Cross-project discussion should align the
meaning of ownership, cancellation, parent death and truthful observation
limits, without assuming identical implementation or a shared library.

### Namespace, locking and publication — DEL-01-02 / DEL-01-04 and consumers

`storage.rs:116,134,156,188,253` uses path symlink checks, Unix `flock`,
file/directory flushes and same-directory temporary publication. Create-once
publication uses a hard link; replacement uses rename. Attempted publication
can be uncertain even after an error. Other guarded readers/writers use
fd-relative no-follow traversal, inode/device identity, link-count checks
and exclusive rename operations; changing storage.rs alone is insufficient.
Examples include `desktop_startup.rs`, attachment custody, records-package
and workflow-library modules. Audit each operation through the owning
deliverable rather than replacing Unix imports en masse.

Proposed services: handle-backed native namespace/leaf identity; explicit
reparse-point, hard-link, drive/UNC and path-substitution policy; lifetime-held
shared/exclusive/nonblocking locks; create-once and replacement publication;
and a platform-specific durable-confirmation boundary. Windows volume/file
IDs, guarded handles, share modes and `LockFileEx` are candidates, not proven
equivalents. Distinguish refusal before attempt, attempted/unknown, visible
publication and confirmed durability. Windows ACLs and delete sharing cannot
be approximated by Unix mode-bit checks. Begin with guest-local NTFS and
explicitly refuse unproven remote/shared filesystem cases in the proposal;
changing public support/guarantees remains an owner decision.

### Recovery database — DEL-01-02

`recovery_store.rs:141,167,220,481,650` ties path device/inode to SQLite's
actual opened descriptor and checks side-file leaves. `descriptor_identity`
requires bundled SQLite **3.46.0**, `SQLITE_FCNTL_FILE_POINTER`, the connection's
VFS pointer, a VFS name beginning `unix`, and the pinned `UnixFileHead` layout.
The explicit refusal is an identity guarantee, not evidence that SQLite cannot
run on Windows. The store uses rollback DELETE journal, `synchronous=EXTRA`,
macOS fullfsync settings and a required post-commit parent-directory flush.
A failed post-commit flush is not-confirmed because commit may have landed.

The first design spike must bind the **actual Windows SQLite-opened handle**
to the guarded namespace and side-file policy with a reviewed supported
extension or a carefully pinned/checked Windows VFS adapter. Do not remove the
Unix guard, compare two path stats instead, or assume PRAGMA names imply the
same durability. Establish actual Windows VFS journal deletion, file flush and
namespace persistence behavior. Crash/reopen tests establish observed recovery,
not universal power-loss/device guarantees. If the required confirmation
cannot be established, refuse it or return not-confirmed; do not invent parity.

### Startup, paths and native interaction — DEL-01-01 / 04 / 05

`desktop_startup.rs:15,31,60` imports Unix metadata/open modes, represents only
`unix_bytes`, and mints device/inode references and process-held leases.
`attachments.rs:73` and `external_observation.rs:135` already represent
`windows_utf16` code units. Reuse that existing lossless representation in a
future implementation, with native path round trips and bounds; display text
must not become dispatch authority. Startup's create-only home preparation
and shared-resource symlinks need an explicit Windows link/ACL policy without
requiring an unapproved Developer Mode or elevation change.

`runtime_session.rs:2803,2814,3591` implements secure API-key entry and OAuth
presentation with AppKit and returns unavailable elsewhere.
`native_waiting.rs:124,158` builds the waiting menu only on macOS. Other
native act/confirmation controls also require candidate-specific Windows
smoke evidence; successful UI fixture replay does not supply it. Preserve the
current unavailable/refusal behavior until a proper native replacement exists.
The credential-free first slice does not need sign-in or secret entry.

### Git and supplier/distribution — neighboring owners and DEL-01-06

`connector_git_process.rs:79,145` pins `/usr/bin/git`, clears the environment,
uses Unix process/fd control and `/dev/null`, and disables prompts, protocols,
lazy fetch, replacement and optional locks. Windows needs an explicitly
identified installed Git and equivalent bounded process/config/network
refusals. Git 2.56.0.windows.4 is a provisioning proposal; its feature probes
(including `cat-file --batch --no-use-mailmap`, SHA-1/SHA-256 object format and
no-lazy-fetch) must run against that runtime before adapter adoption.

Current distribution/preflight/packaging, selected supplier paths/formats,
signing and `.github/workflows/app-v4.yml` are macOS-specific. The current
supplier reference does not cover Windows. Metadata confirms complete stock
Codex 0.160.0 npm packages for Windows ARM64 and x64; neither is acquired or
qualified. Windows packaging/signing and native x64 verification remain later
work, with owner support choices separate from DEL-01-06's existing macOS
Apple Silicon requirement.

## Proposed bounded sequence and effort

These are engineering estimates after inspection, not commitments or elapsed
agent-time promises. Missing acquisition/guest access and owner decision time
are excluded; revise after each native witness.

1. Resolve/pin acquisition metadata and authorize the common environment;
   provision and verify native ARM tools/x64 output, dependency caches and
   network-isolated supplier handshake harness: **1–3 engineering days** after
   inputs. An integrity mismatch or unsupported tool combination stops only
   that acquisition. Continue source/service design independently.
2. Specify process capability and namespace/SQLite confirmation contracts;
   implement isolated Windows probes with invented material: **3–6 days**.
   The decisive early question is SQLite opened-handle binding plus durable
   namespace confirmation. Return a refusal/guarantee conflict if unresolved.
3. Introduce small OS-specific process and storage adapters while retaining
   current Mac implementations; add targeted race/substitution/lock/uncertain
   publication regressions and Type 2 independent scrutiny: **5–10 days**.
   Avoid a repository-wide feature rewrite to hide missing services.
4. Join minimal App startup, lossless paths, stock initialize/stop, durable
   invented fixture, close/reopen validation and one native nonsecret control;
   obtain actual ARM-guest/emulated-x64 smoke evidence: **3–6 days** after
   prerequisites. This is the connected feasibility milestone, not full parity.

Rough order to that first connected slice is **2–5 engineering weeks**, with
high uncertainty concentrated in namespace durability and SQLite integration.
Credential UI, broader file/workflow/record paths, restricted Git, native
menus, Windows packaging, native-x64 examination and supplier/App qualification
remain subsequent slices; no full-port/release date is justified yet. macOS
work can remain independently finishable by reviewing small platform seams
and running affected Mac regressions with each integration.

## Reconciliation and cross-project decisions

Affected ScopeOfWork and dependency conditions were examined for DEL-01-01,
DEL-01-02, DEL-01-04, DEL-01-05, DEL-01-06 and PKG-09 examination. This tranche
changes documentation and adds an acquisition inventory only. No implemented
process, persistence, permission, UI or distribution behavior changed.
DEL-01-01 ScopeOfWork gains a nonnormative investigation pointer;
`deliverable.yaml` needs/conditions, other ScopeOfWork requirements and
historical evidence remain unchanged. The existing dependency cycles do not
close qualification. Later implementation must reconcile changed meaning
with each owning Design/ScopeOfWork/dependency condition in its own revision.

Agent 0 should take these specific proposals/questions to SWBPIPE: native
ARM host plus x64 output/emulation limits; process handles/job membership and
separate EOF/stop/parent-death policies; native file identity/reparse/locking/
publication/durability refusals; portable exchange path representation and
revision identity; opt-in transport readiness, stale refusal, host validation,
durable receipts and unknown outcomes; WebView2 compatibility. No new
transport, public architecture promise, cross-project library or receiving
adoption is established. Historical `HANDOFF_SWBPIPE_DOMAINS.md` remains
source-qualified input; PEC remains retired. The App manager is the sole
common provisioning writer only after inventory and exact authorization;
SWBPIPE owns its separate checkout, implementation and evidence.
