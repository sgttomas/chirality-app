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

## Ownership and execution

- HELP_HUMAN / Agent 0: purpose, scope, cross-project alignment, inspection of
  integrated returns and escalation of reserved choices.
- One WORKING_ITEMS / Type 1 owner: feasibility, implementation sequence,
  integration, ordinary repairs, checks and affected-deliverable reconciliation.
- HELPS_HUMANS / Type 1: bounded design contributions when an actual question
  warrants them; no compulsory additional management layer.
- TASK / Type 2: bounded implementation, investigation or independent scrutiny;
  no further delegation.

All Type 1 agents use `gpt-6.1-sol` with `reasoningEffort=high`.
All Type 2 agents use `gpt-6.1-terra` with `reasoningEffort=xhigh` and
`serviceTier=priority`, the available faster service setting. Managers and
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
