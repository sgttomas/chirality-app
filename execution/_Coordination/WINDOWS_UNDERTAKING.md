# Windows feasibility and cross-platform development

## Authority and purpose

The owner resumed App v4 development on 2026-10-28 and directed Agent 0 to
proceed with the proposed Windows undertaking: bounded feasibility first,
then evidence-led platform-service implementation, parity and examination.
Keep one application codebase and keep macOS delivery independently finishable.
The owner also authorized direct coordination with the SWBPIPE Windows session.

This authorizes development and investigation. Windows shipping architecture,
support promises, changed guarantees, acceptance and releases remain owner
decisions. The current macOS v4.0 commitment is not silently broadened.

Initial source baseline: `25979a63995c59b818f56804203e5c5069306887`, including
the development-resumption entry-document changes. Source findings from the
preceding assessment are inputs to verify, not Windows execution evidence.

## Current target and resource authority — 2026-10-29

The former target was privately confirmed SAME as the owner's CAEPIPE VM.
It is permanently off-limits to both Windows efforts, including discovery,
guest sessions, scratch/probes, installers, Tools/configuration, power/reset
and cloning/migration. Its CAEPIPE data/settings/exchange surfaces are not
development inputs. Earlier readiness questions and guest-probe briefs do not
authorize access, even if that guest is running or unlocked.

The owner subsequently corrected the route: they do not intend to run a
second local Windows instance. The separate-local-VM route is superseded and
on hold, including further image acquisition, attachment, setup, boot and
provisioning. Preserve its existing dormant hardware and private binding;
do not delete, access or change them. No media availability or prior CLEAR
revives that earlier authorization. Earlier hardware/acquisition records below
are historical and do not create a live provisioning dependency.

Current Windows development continues through hosted native-Windows CI and
repository-local work. If a concrete future requirement cannot be met there,
Agent 0 must bring the exact unmet capability and cloud options to the owner
before any acquisition or spend. Cloud provisioning is not authorized. Product,
supplier and native qualification requirements remain unchanged, as do the VS
metadata-integrity hold and the CAEPIPE exclusion. No new work front is opened.

Earlier identifier-bearing evidence projections are now redacted, with
original digests and privately retained originals noted. Outcomes and original
source hashes are preserved. Existing Git history is not rewritten; it can
still contain identifiers from before the private-identity direction.

## Ownership and execution

- HELP_HUMAN / Agent 0: purpose, scope, cross-project alignment, inspection of
  integrated returns and escalation of reserved choices.
- One WORKING_ITEMS / Type 1 owner per bounded tranche: implementation,
  ordinary repairs, checks and affected-deliverable reconciliation. The
  provisioning route is held, with no active guest writer. Hosted-fixture
  owners have no VM authority. Agent 0 integrates their returns.
- HELPS_HUMANS / Type 1: bounded design contributions when an actual question
  warrants them; no compulsory additional management layer.
- TASK / Type 2: bounded implementation, investigation or independent scrutiny;
  no further delegation.

All Type 1 agents use `gpt-6.1-sol` with `reasoningEffort=high`.
Following the owner's updated steer on 2026-10-29, all Type 2 agents use
`gpt-6.1-sol` with `reasoningEffort=medium` and `serviceTier=default`
(standard service). This supersedes the earlier Terra/xhigh/priority setting;
historical review records retain the settings actually used. Managers and
Agent 0 may decide when Type 2 contributions are useful. Do not substitute
models or settings silently if unavailable. Initially cap active implementation
contributors at two, with at most one independent reviewer alongside them.

Use `/Users/ryan/dev/chirality/workflows/coordinated-knowledge-work/WORKFLOW.md`
and the role files selected by repository `AGENTS.md`. Each dispatch specifies
its objective, exact input basis, allowed reads/writes, integration owner,
review route, ordinary decisions, reserved choices and actual return mechanism.
Managers own repairs through integration. Review the actual version integrated.

## First useful return

Establish the host/guest architecture and available Windows toolchain, verify
the pinned supplier's Windows basis as far as authorized inputs allow, and
identify actual build blockers. Aim for a small connected slice: launch,
supplier handshake without credentials or a live model, controlled stop,
durable invented fixture data, reopen/validation, and native-control smoke
evidence. Distinguish each observed result from modeled or unrun behavior.

Return the actual source revision, environment and checks, substantive output
or precise obstacle, proposed platform boundaries, next implementation sequence
and revised effort estimate. An inaccessible guest or missing authorized
dependency does not prevent repository-only investigation and design.

Start from DEL-01-01 (supplier/process hosting), DEL-01-02 (recovery),
DEL-01-04 (native requests/attachments), DEL-01-05 (access), DEL-01-06
(macOS packaging), and PKG-09 (examination). Use the deliverables tools to
trace affected consumers. Reconcile changed implementation meaning with the
affected ScopeOfWork, Design and dependency conditions in the same change.
Independent scrutiny is required for persistence, permissions and destructive
operations. Do not weaken or bypass a check to claim portability.

## Cross-project coordination

App Agent 0: [Chirality App for windows](t3-thread://v1/7821dcff-74fd-4895-8c77-56074ddcb84a).
Peer: [SWBPIPE for windows](t3-thread://v1/533ebf43-c41f-41e8-bfd7-91517fff8a7e).
Agent 0 sent the initial coordination proposal on 2026-10-28. SWBPIPE Agent 0
returned a compatible feasibility plan and proposed the App manager as the
single provisioning writer for a common Windows guest/toolchain. App Agent 0
accepted that allocation: inventory first, SWB requirements supplied by its
manager, separate guest-native checkouts/build directories, and no duplicate
installers or uncoordinated VM mutations. Download authorization remains
required. This resource agreement establishes no technical contract adoption.

SWBPIPE reported an arm64 Mac host with 128 GiB RAM and subsequently supplied
its checked, read-only inventory: Parallels 27.0.2; a running Windows 11 Pro
10.0.26200 Arm64 guest with 32 GiB RAM; PowerShell execution through
`prlctl exec` usable. Rust/cargo/rustup, Node/npm, Git, `cl`, CMake and `pwsh`
were absent from PATH; VS Installer was absent, no Windows SDK was registered,
and `winget` was absent. WebView2 156.0.4314.50 was registered. SWBPIPE states
that inventory made no guest writes, downloads or VM changes. This is
peer-supplied execution evidence, not an independent App observation; absence
from PATH is not proof of absence everywhere on the machine.

Both coordinators propose x64 as the primary Windows verification target,
with Parallels Arm/emulated-x64 evidence labelled separately; no public
architecture/support commitment was made. SWBPIPE also reports passing host
Windows-x64 cross-compilation checks for `curved_bend --tests` and
`product_physics --lib`; these are not Windows execution or App evidence.

### First feasibility return and common provisioning proposal

SWBPIPE requested VS Build Tools 2022 17.14 LTSC, C++ x64/x86 and SDK
10.0.26100, Rust 1.97.1 MSVC with `x86_64-pc-windows-msvc` and
`wasm32-unknown-unknown` targets, Node 24 LTS, Git 2.x and
`wasm-bindgen-cli` exactly 0.2.123. These are proposed requirements, not
resolved components, selected downloads or download/install authorization.

The App implementation owner must resolve supported ARM-hosted x64 compiler
components, Rust host architecture, exact patches, official sources and sizes,
and subsequent payloads or credible bounded bootstrapper totals into one
owner-reviewable proposal. Include project dependency acquisition, version
verification, installation order and NTFS-local, separate project build paths.
Distinguish measured, vendor-published and estimated sizes. Reuse existing
WebView2 if sufficient; CMake, PowerShell 7 and winget are included only if
the selected build path demonstrates a need. Source contradictions or unknown
payload bounds must be exposed before authorization. Metadata/header research
is permitted; installer/package payload downloads and installations are not.
No AC-004 exclusive stack-witness window is currently planned by SWBPIPE.

The first App feasibility return is committed at
`716a8e795968b82c42f84cf67f26ad817d64bdfe` and integrated through a merge
commit. Its owning records are
`../PKG-01/DEL-01-01/Design/WINDOWS_FEASIBILITY.md` and
`../PKG-01/DEL-01-01/Design/WINDOWS_PROVISIONING.md`, with source-pinned
acquisition/package JSON beside them. Independent Type 2 scrutiny examined
`61e12b8e92445903e5fb3edc90b9098d121fb043`; its two planning findings were
repaired in the returned revision. Agent 0 inspected the actual review return,
the repair delta and integration, including the 78 GiB estimated simultaneous
footprint, 80 GiB rounded envelope and 100 GiB initial free-space threshold.
This is development integration, not owner acceptance or installation approval.

The proposed 6 GiB transfer ceiling remains an estimate. VS 17.14 is Current,
not LTSC. Its channel/catalog byte identities disagree in the saved official
metadata reads; this unresolved acquisition join blocks VS payload acquisition
and installation. Python-dependent Windows checks are explicitly deferred.
An independent metadata-only Type 2 investigation reproduced the catalog
response exactly with no content coding or redirects; Agent 0 inspected the
actual return, raw body, channel and headers. The root cause remains unknown;
no authenticated alternative or repin was established. The acquisition record
retains the source/digests and scratch-evidence references. Resolve official
matching metadata and trust before acquisition; do not repeat identical reads
or treat unverified signatures as proof.
Mac offline build/check evidence is recorded; Windows cross-compilation stopped
in the bundled SQLite C build before App Rust compilation. No Windows App,
supplier, native-control or durable-reopen witness is established.

### Process-policy coordination input

SWBPIPE's current ordinary worker policy requires termination on spawning-App
death, including memory-headroom-stopped workers. Source basis
`1560bbf7f7add4637a20572a2b0d404ef121af63`, read independently by App Agent 0:
`projects/chirality-piping/execution/PKG-04/DEL-04-07/Design/memory-budget-decision.md`
and `projects/chirality-piping/apps/desktop/src-tauri/src/solve_worker.rs`
(worker description and parent-exit handling). Cancellation/session reset
termination does not release its pool reservation until exit/reap and the
applicable result-custody condition. A Windows Job kill-on-close mechanism
may preserve that policy; it does not select App's parent-death behavior.
Neither EOF nor successful termination-request delivery proves process exit.

SWB's counted-heap grant, measured process footprint and fresh host-headroom
admission require separate Windows definitions and evidence. A Job OS memory
limit is not an automatic replacement for those quantities. These are
source-qualified peer constraints for subsequent design, not shared-library
adoption or a change to App's custody contract.

Align before dependent implementation on Windows architecture/evidence targets,
shared VM/toolchain scheduling, process ownership and termination semantics,
file identity/locking/publication/durability, portable exchange, native runtime
provisioning and the actual App-to-host interface. Preserve source/revision
identity, opt-in access, stale refusal, host-owned validation, truthful receipts
and unknown outcomes. Reuse verified lessons; a shared implementation or new
transport is not presumed necessary.

Share concrete findings or consequential proposals at milestones, with exact
artifact/revision references; avoid acknowledgment loops. Agent 0 carries
cross-project commitments and records actual decisions in the affected owning
Designs. Neither session edits or accepts commitments for the other repository.
The existing `HANDOFF_SWBPIPE_DOMAINS.md` remains source-qualified historical
coordination input, not proof of current adoption. PEC remains retired.

## Operating boundaries

Use fresh scratch Codex homes, never `~/.codex`, and invented test material.
Do not sign in, use credentials, run live model turns or access private user
data. Build offline by default. Downloads require explicit owner permission
identifying file, source and size; shared VM/toolchain mutations must be
coordinated before execution. Do not power off, reset or reconfigure a guest
or interfere with the owner's running applications.

Preserve release tags, imported ancestry and existing verification criteria.
No force pushes, protection bypasses, permission changes or release actions.
Do not modify `foundation/thesis/`, the shared Chirality library, SWBPIPE or
packaged role/workflow assets as incidental portability work. Small platform
changes may use short-lived branches/PRs; no long-lived Windows fork is selected.
Completion returns through the host's delegated-task mechanism to Agent 0;
the host's durable task state and completion notification carry continuity
independently of a wait or timer inside the coordinator's current turn.

## Platform-contract return and next bounded fixture

The platform-contract tranche returned
`974aa66893f2c0a53a5df87e46eb3c3c0db185d5` and is integrated through a
merge commit. Agent 0 inspected the independent review of `13c12063` and the
local P-01 repair: ordered creation instrumentation, retained descendant
HANDLE/membership proof and a deliberate early-escape negative control.
The returned contract/trace/evidence files were preserved byte for byte.

`execution/PKG-01/DEL-01-02/Design/WINDOWS_PLATFORM_SERVICES.md` records proposed process,
namespace, lock, publication and SQLite probe gates. SQLite 3.46.0 supports
actual opened-main HANDLE retrieval through its public file-control API;
that does not resolve open-time/sidecar races or the Windows directory-sync
gap. App crash cleanup and Windows durable confirmation remain reserved,
unselected policy/profile questions. Fixtures may compare candidate behavior
without selecting a production policy or inventing durable success.

`execution/PKG-03/DEL-03-03/Design/WINDOWS_APP_SWB_TRACE.md` identifies production App receiving
of person-selected documents and test-compiled submission seams. No live
App-to-SWB transport or durable external submission receipt is established.
The first Windows App milestone remains standalone. The provisioning
amendment proposes a full short-path App checkout; generated paths remain
untested and no global long-path setting is selected.

The next bounded implementation may investigate package-free Windows fixtures
using existing PowerShell/.NET facilities, with independent code scrutiny
before execution. Limit writes to fresh task-owned guest scratch and actions
to fixture-owned process/Job HANDLEs; do not install packages, change guest
settings, inspect user data or affect unrelated applications. If existing
facilities cannot support the fixture, report that precise prerequisite and
continue repository-only preparation. Fixture results establish only the
recorded OS/architecture/harness behavior, not Rust-adapter/App parity,
supplier/native-control evidence, or a durability guarantee. Exact pinned
SQLite probes remain deferred until their real prerequisite is available.

## Fixture preparation and byte-preserving checkout

The package-free process-fixture tranche returned local source
`3ad9ac047df21358b223a3d744f9df77eac64fda`, integrated with ancestry preserved.
The C# P01/P02 harness is prepared, but its initial execution driver failed
independent scrutiny: continuous scratch namespace guards did not span
compilation, and the compiler lifetime was not bounded independently of host
command survival. The unsafe route was removed; `--run` refuses before guest
contact. Read-only metadata establishes the installed ARM64 .NET compiler,
PowerShell FullLanguage and unchanged Restricted policy, not compilation or
native test results. Both blocking guards remain repairs, not waived conditions.
No guest fixture files, compiler, helper processes or Jobs were created.

The next minimal implementation is the guarded bootstrap, with independent
review of the actual repaired version before any write/compile/run. Existing
Reflection.Emit facilities may permit the needed Win32 guard calls in memory
before invoking the installed compiler; this is an investigation option, not
a verified solution or authority to weaken either guard. Continue the saved
fixture suite only after those conditions hold. No package acquisition or
production policy change follows from this preparation.

SWBPIPE reported native-x64 fixture results at
`226de96777a1f7e8c5ba5ce3fe1e31f82839fe00`; those peer results do not qualify
App's source or memory policy. Its separate checkout failure exposed a relevant
App risk: Git newline conversion can change exact-byte inputs. App had no
attributes policy. The scoped `.gitattributes` correction and
`app/tests/check_git_checkout_bytes.py` preserve hashed input families without
global settings or fixture/reference rewrites. A real temporary-index checkout
with `core.autocrlf=true` changed ten selected committed LF inputs without the
policy; after it, all eleven protected inputs (including intentional CRLF)
matched, while unprotected text still converted. This host Git regression and
passing schema/hash checks are not native Windows execution evidence.

## Supplemental hosted fixture publication

The hosted process-fixture tranche returned
`0b7afaede2a6b1a0cbf76498307e24ad4832fdd0` and is integrated with ancestry
preserved. Agent 0 inspected the independent Sol/medium/default review of
`02a32983` and the small compatibility repairs: checkout-scoped
`core.autocrlf=false` for every bound input and the legacy compiler's supported
bounded `/help` version probe. The five integrated source inputs bind exactly
to HEAD blobs. Eleven hosted and eight retained guest-driver host regressions
passed in the tranche; they are not native results.

The new workflow is supplemental, disposable GitHub-hosted native-x64 Windows
only, with preinstalled compiler/Python and no package acquisition or Parallels
operation. Existing required App/Mac checks and policy are unaffected. Native
P01/P02 behavior and observed cleanup remain pending until an actual run and
source-bound artifact are inspected. The guest bootstrap/namespace and
production App/SQLite/durability obligations remain separate.

Two hosted native attempts compiled and observed both P01 controls and safety
cleanup, then failed P02-A with a live leader but no EOF observation. The
additional stderr-alias close was not a solution; the second trace showed
equal standard-handle values. Neither an extra writer nor a PeekNamedPipe
defect is established. Research led to bounded direct-read diagnostic source
`f9f042a8f455a51902a78d3ce8d6dbba157bf4fd`, now integrated byte for byte.
Agent 0 inspected the Sol/medium/default independent review and exact-prefix
verifier repair. A uses one synchronous read on the same stdout HANDLE,
post-close metadata, original eight-second/live-leader checks, and joined-reader
cleanup; EOF after cleanup cannot become a pass. Seventeen host tests passed.
The repaired candidate's native compilation/execution remains pending.

## New build guest hardware return

The environment owner returned `a7f46d3b818bc22df2e58b149ae1676c14dcf273`:
new ARM64/Windows11 hardware, 4 fixed vCPUs, 16384 MiB fixed RAM and a fresh
sparse 256 GiB NVMe disk. The actual state is stopped/zero uptime, never
booted, with no media or installed Windows. Private binding was atomically
replaced and read back under its sole-writer lock; protected exclusion and
other metadata remain. Agent 0 inspected the final review and proof-file
digests, validated the private binding without printing identifiers, and
confirmed the fixture source still refuses guest access. No VM operation or
binding write was performed by that integration check.

The public owning record/receipt retain dormant sharing child preferences
separately from disabled parent/global gates; runtime isolation is untested.
That earlier media-dependent next step is superseded by the current owner hold;
media availability cannot advance attachment/setup. The
owner cannot obtain it manually at present; do not pressure them, retry the
rejected source API, or reuse any CAEPIPE state. Mac Agent 0's latest actual
CLEAR ended the exclusive window, but no powered use is needed or scheduled
while media is absent. Hosted work is independent.

## Publishing route

The initial ordinary feature-branch push reported a server-side bypass because
the active `protect-main` ruleset matched `~ALL` branches. The owner authorized
the proposed scope correction. An independent Type 2 reviewer checked the
exact before/proposed writable JSON and current default branch; Agent 0 then
changed only the include selector to `~DEFAULT_BRANCH`. API readback preserved
the name, active enforcement, branch target, creation/update/deletion rules,
exclusions and every bypass actor/mode. Effective-rule queries confirm these
three rules still apply to `main` and do not apply to this feature branch.
Ordinary feature-branch publication may resume; protection bypasses and
unrelated rule/permission changes remain unauthorized.
