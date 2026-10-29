# Dedicated Windows build guest — hardware ready, media pending

Recorded 2026-10-29 against `de122cc4a768ea8ae5ebb9bbba11a169aad9d94e`.
The owner authorized a separate Windows build guest for Chirality App and
SWBPIPE Windows. This record owns this bounded preparation tranche; it does
not establish Windows product support, supplier qualification or acceptance.
Machine-readable evidence is in `WINDOWS_BUILD_GUEST_RECEIPT.json` beside this
file. Public records identify the new target only as `chirality-windows-build`.

## Actual result

A fresh Parallels guest was created and configured in exclusive task-owned
storage outside Git. Its private binding was durably replaced and read back,
with the protected exclusion and existing unrelated metadata preserved.
`created_for_builds=true` and actual configured `ram_mib=16384` are recorded.
This binding does not admit the fixture driver: `GUEST_ACCESS_ON_HOLD` remains
unchanged.

Actual readback establishes:

- Parallels **27.0.2 (58673)** on an Apple **ARM64** host with
  **137,438,953,472 bytes RAM** and **18 logical CPUs**.
- New guest: Windows 11 built-in distribution preset, **ARM CPU**, EFI ARM64,
  Secure Boot on and CRB TPM. No user template, clone, import or restore image.
- **4 fixed vCPUs**, **16,384 MiB configured RAM**, with automatic CPU count
  and automatic RAM sizing off. Both CLI and saved configuration were checked.
- One fresh expandable, sparse **256 GiB NVMe** disk. The descriptor reports
  **536,870,912 logical sectors × 512 bytes = 274,877,906,944 bytes**. Its
  descriptor and extent resolve inside the newly generated bundle; no existing
  disk was attached. Initial bundle allocation was **2,154,496 bytes**.
- No network adapter, optical drive, USB or sound device. No installation
  media, floppy, physical passthrough, restore image or unattended media.
- Global host isolation on; host/guest folder sharing, home/all-disk/custom
  sharing, shared profile, application sharing, SmartMount, cloud, clipboard,
  location, SSH identity synchronization, printer/camera/smart-card/gamepad
  sharing disabled at their applicable controls. Autostart and default answers
  off. Parallels Tools absent and automatic Tools updates off.
- Final state **stopped**, **zero uptime**, **never booted**. Boot order is the
  new disk only. No Windows kernel/runtime or Windows Setup readiness has been
  established. This is hardware readiness with media missing.

The successful CLI `create` operation returned no UUID in stdout/stderr. The
owner clarified that canonical `Identification/VmUuid` in the exclusively
generated new bundle is valid creation-return identity. Extraction checked one
fresh bundle/config, exact creation argv/name/destination, successful receipt,
ownership, birthtime order, canonical field uniqueness and nonsymlink resolved
paths. Under the sole-writer lock, its normalized UUID differed from the
protected exclusion. A direct-UUID read-only registration check then confirmed
the exact newly created home/name before any `set` or binding. No name lookup,
unknown-target adoption or broad guest listing occurred. Raw identities and
receipts remain private outside Git.

## Isolation evidence and limits

Two stored guest-sharing child preferences remain **on**:
`AutoMountCloudDrives` and `ShareRemovableDrives`. Commands requesting off
returned success without changing those values. Their **GuestSharing parent
and AutoMount are off**, global host isolation is on, and Tools/network/USB
are absent. The final verifier checks these parent/global gates explicitly and
records the dormant child values. `DragAndDrop=1` also remains stored behind
global isolation and absent Tools. Shared-profile `UseTrashBin=1` and
application `SmartSelect=1` remain dormant behind their disabled sharing controls. This is a configuration assessment for the
powered-off stage; effective isolation inside a running Windows guest is
**unrun**. Revalidate before adding controllers, installing Tools, enabling
sharing or changing isolation.

Automatic gamepad sharing required a standalone final off command. It read
back off in both CLI and XML; subsequent unrelated sharing sets had been
observed to reset it on. The final verifier therefore requires actual off,
and no further guest `set` followed that final repair. Future configuration
changes must recheck it rather than rely on successful command exit alone.

## Microsoft media receipt and source-access obstacle

Canonical source:
<https://www.microsoft.com/en-us/software-download/windows11arm64>.
The page and its published download API identify normal **Windows 11
multi-edition ISO for Arm64**, **26H2**, **build 26300.9457**, **English
(United States)**; product edition ID **3816**, SKU **27162**. This is source
metadata, not an installed OS version or an owner-selected Windows edition.

The official ARM64 page's English 64-bit row publishes expected SHA-256:

```text
8992f2d2cfd2fa647e579e9eb31fc21f34da8333c29b6170fde17d2ed6623e9c
```

The scripted request following the page's published endpoint/query shape,
using a fresh session, received an Errors-only response from Microsoft's
`GetProductDownloadLinksBySku` service:

```text
ErrorSettings.SentinelReject
Sentinel marked this request as rejected.
Type: 8
```

**Exact ISO filename, download locator, published size, actual byte size and
actual SHA-256 are unknown. ISO bytes transferred: zero.** No ISO was attached
or installed. The expected hash is publisher page metadata obtained over
normal TLS; there is no file to compare and no publisher signature claim.
The rejection establishes this request's source-access obstacle, not its cause
or a general/permanent Microsoft outage. No API retry, mirror, UUP assembly,
evaluation/developer image, account/challenge bypass or credential use followed.
No expiring locator was returned or published.

The owner is unable to obtain the media manually at present. Exact existence
checks, without enumerating Home or Downloads, found none of these conventional
public-installer candidates in the standard Downloads location:
`Win11_26H2_English_Arm64.iso`, `Win11_26H2_English_Arm64v2.iso`,
`Win11_25H2_English_Arm64.iso`, `Windows 11.iso`. These candidate names do not
resolve the unknown official artifact identity. No other cache contents,
existing guest disk or private exchange were searched or reused.

## Storage, authority and next boundary

Task-owned stable inputs, the new bundle, scripts and private receipts live
under `/Users/ryan/ChiralityBuildInputs/windows-arm64-20261029-k7yh9aim/`,
outside Git/worktrees. The directory is private to the owner. A fresh scratch Codex home was created
for development/checks; no Codex test used `~/.codex`, sign-in or credentials.
Initial host free space was **816,671,096,832 bytes**; free space at the final
receipt is recorded separately in the JSON. Sparse disk creation was preceded
by a same-filesystem **256 GiB + 32 GiB reserve** check. Before acquiring media,
recheck free space using the actual ISO length in addition to that budget.
OS-image bytes remain separate from the earlier 6 GiB tool/package proposal.
No user data was deleted and no heavy compile/model workload ran.

The binding transaction held the sole-writer lock, rechecked the unchanged null
preimage/exclusion, and required successful complete hardware validation. It
used a same-directory mode-0600 temporary file, file fsync, atomic replacement,
directory fsync and exact readback; private intent/result evidence was saved.
All guest mutations used explicit argument arrays and the proven fresh UUID,
with normalized exclusion checks before each dispatch.

Mac Agent0's actual **CLEAR** was relayed after the exclusive memory-witness
window ended; elapsed time was not used as clearance. This tranche performed
no power operations. The new guest stays off while media is unavailable. A
later on-demand powered-use window remains capped at 16 GiB and must respect
new exclusive announcements; only this new target may be suspended/stopped.

Resume acquisition/attachment only when the normal authorized official media
becomes available. Establish its exact file/source/length, compute SHA-256,
compare the publisher expectation exactly, and stop on mismatch **before
attachment/installation**. No further route/image approval is requested here.
Licence/EULA acceptance, edition/product-key decisions, purchases, activation
and account sign-in remain owner acts. No Express/unattended acceptance,
account import, OOBE or execution-policy bypass is authorized.

No Parallels Tools, Visual Studio, Rust, Node, Git or package installation,
App fixture/supplier/native-control/P01/P02/SQLite work, hold lifting or release
action occurred. Other acquisition/VS integrity holds remain unchanged. No
protected-guest discovery, query, configuration, power, session, disk or data
operation occurred.

## Assurance and deliverable reconciliation

Independent reviews covered the source-access obstacle, create-only safety
repairs, canonical fresh identity/configuration, and actual final verification
plus binding persistence. Historical completed reviews used
`gpt-6.1-terra/xhigh/priority`; after owner steering, the identity/configuration
and final binding reviews used `gpt-6.1-sol/medium/default`. Provenance is
preserved in the JSON. Three nonblocking final hardening findings were applied
before execution: XML `Fdd` exclusion, explicit disk boot-order assertion, and
error-type-only uncertain-binding evidence when parsing the actual target fails.
The complete verifier then passed; binding replacement and readback succeeded.

The selected shared role/method source was `/Users/ryan/dev/chirality` at
`1560bbf7f7add4637a20572a2b0d404ef121af63`. This consultation did not update
packaged product roles/workflows. DEL-01-01 `ScopeOfWork.md`, existing Windows
design records and `deliverable.yaml` conditions were reconciled with this
environment-only result: contract, qualification, macOS commitments and
dependency meanings are unchanged. Only this new owning artifact and its new
sanitized JSON are in this tranche. Parent Agent0 owns final integration and
pointer reconciliation.

Focused repository checks passed: deliverable check (41 deliverables, zero
errors; six reported dependency cycles, with no dependency declaration changed),
JSON/readiness consistency, public identity redaction, and diff whitespace.
No App build or Windows/runtime test was run for this documentation/environment
tranche.
