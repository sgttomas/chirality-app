# Signed candidate b3dd4145: owner-testing proposal

Standing: **proposal, not run.** Prepared offline on 2026-11-03; revised after
Agent 0's review. Nothing here has been launched, installed, enrolled, captured,
recorded or served. No account exists. No step runs until the owner approves it
concretely. Source facts are cited at the exact signed source `f664ee1d`.

## Subject

| Fact | Value |
|---|---|
| DMG | `Chirality-App-v4-4.0.0-f664ee1d-b3dd4145.dmg`, 156,986,610 bytes |
| DMG SHA-256 (post-staple) | `34ab566132e059d3e51885c87907898238ba95421c88d1303d535d19eafcf26e` |
| Contained App | `Chirality App v4.app`, bundle-tree v2 `b3dd4145779e711a0169c08b2f1757eace19e38e08effe03a18c5bef986b5fb8` |
| Source / ID / version / minimum | `f664ee1dd55f403f7c3498df3f09ac50f77c9a0c` / `com.chirality.app` / 4.0.0 / macOS 15.0 |
| Executable SHA-256 / cdhash | `49f61681…3e6` / `e1bf4644f66389011964e99cec43fc853b6b4158` |
| Recorded standing | Signed, notarized (`430e7461-…`, Accepted) and stapled. Gatekeeper accepted the DMG and the mounted App (read-only mount, no launch). |

The facts come from the [owner signing record](../../../PKG-01/DEL-01-06/Work/selected-production-build/f664ee1d-caec11a00be3/owner-signing.json)
and the scratch `notarization-record.json`. The build is publisher
`selected-production`, and the keychain selection is compiled.

This is a new subject. Candidate `1f67d3822b-8c83d74ae3ce`, the `j58087z7` and
`zootd3ob` attempts, and the `795362874d`/`fdcf608fb5` histories keep their own
subjects. Nothing transfers from them, and no AX fix is inferred.

The local DMG has no `com.apple.quarantine` attribute. Production step 5 treats
missing quarantine as **blocked**, so the transfer must create it.

## Isolation basis

The App's data lives at `~/Library/Application Support/com.chirality.app`. That
directory holds the capture-seal marker, the records store and the account homes,
and the SEAL-C item lives in the user's data-protection keychain. v3 uses the
same bundle ID. A fresh **standard** macOS user isolates all of these per user,
and gives SC-3 its required fresh namespace with no legacy `capture-seal`
directory.

This is App-namespace isolation, not a security boundary. macOS standard users
share the `staff` group, so the test user could read the owner's group-readable
files. Neither the App nor the procedure touches them. No VM, guest, cloud or
media is involved.

## Source-verified journey at f664ee1d

Launch and setup:

- **Empty AppData:** launch state is `setup-required`, with the banner "Setup
  needed" (`desktop_startup.rs:692,776-788`; `DailyWorkspace.tsx:41,46`).
- **No supplier yet:** no account home is created and no supplier starts
  (`lib.rs:2754`).
- **Setup only saves for the next launch:**
  - The person chooses **Prepare a new account home** and three shared paths:
    `Shared config.toml`, `Shared AGENTS.md` and `Shared skills directory`.
  - Then a project directory, then the supplier option **Bundled supplier —
    unqualified owner-use development**.
  - Then **Review setup effects**, then the native dialog "Desktop setup — next
    launch only" with the button **Prepare home and save for next launch**.
  - The result is "Setup saved for your next launch. Your current workspace has
    not changed." (`DesktopSetupPanel.tsx:82,107-139`;
    `desktop_setup_confirmation.rs:11-12,121-122`).
- **What setup writes** (`desktop_startup.rs:1428-1430,1515-1542`;
  `home_resources.rs:357-372`):
  - `account-homes/account-<opaque>/`, a new 0700 home;
  - links to the three shared paths;
  - `desktop-startup/request.json`, mode 0600.
- **Shared-path prerequisites:**
  - Setup accepts missing targets, but at the next launch the release build
    refuses to start the supplier unless they exist (`attachment_custody.rs:241-246`;
    `runtime_session.rs:2483-2488`; `lib.rs:2640`; `hosting.rs:1511`).
  - `config.toml` and `AGENTS.md` must be regular files with exactly one hard
    link, and `skills` a directory (`desktop_startup.rs:100-108`).
  - Replacing a shared file between setup and relaunch, as some editors do on
    save, returns the App to setup (`desktop_startup.rs:93-131`).
  - The App checks metadata only (`desktop_startup.rs:1547-1568`).
- **Project prerequisites:** the project must be an existing directory with no
  symlinked ancestor, not overlapping AppData or the shared paths
  (`desktop_startup.rs:889-895`; `storage.rs:117-129`). At startup the App writes
  `.chirality/project.json` into it (`lib.rs:2582-2588`).
- **Relaunch:**
  - The saved request is revalidated, and the state becomes `saved-request`
    (`desktop_startup.rs:778,899-1001`).
  - The production supplier configuration replaces the setup's bundled choice
    (`desktop_startup.rs:941-949`; `hosting_successor.rs:56-65`).
  - The supplier starts automatically (`lib.rs:2753-2765`) with `CODEX_HOME` set
    to the account home and credential variables removed (`hosting.rs:1614-1617`;
    `hosting_successor.rs:179-184`).
  - No credential check precedes the `initialize`/`initialized` handshake
    (`hosting.rs:1706-1784`).

S4 and readiness (`hosting_successor.rs:286-320`; `installed_custody.rs:56-131`):

- **Checks:** full supplier-tree equality, then the installed-custody observation,
  then the `--version` probe, then pre-spawn revalidation.
- **Display:**
  - On success, Host diagnostics show "State: ready" and "Supplier standing:
    verified-pin", with banner "Codex is connected" (`App.tsx:2149-2171`;
    `DailyWorkspace.tsx:42`).
  - On refusal, the text reads "production refused after complete tree equals
    selected reference: …", with banner "Codex could not stay connected".
- **Files:** each publication `runtime/distribution/s1-<opaque>/` holds the
  selected reference members plus `.chirality-s1/` with `observed.json`,
  `installed.json`, `preflight.json` and `transport.json`. The transport file
  lists every closure entry. A later publication holds `lifecycle.json`
  (`distribution_store_s1.rs:7-11,142-157,225-256`).
- **No export:** the App has no export of these. `hosting_s4_export.rs` is
  test-only.

A4 capture, enrollment and verification:

- **Where:** Workspace tools ▸ **Files and standing acts** ▸ "App file acts and
  act log" (`App.tsx:2116-2117`; `FileActPanel.tsx:95-105`).
- **Making a capture:**
  1. **Kind** `mark checked`, plus non-empty **Scope** and **Purpose**.
  2. **Select file and freeze preview…**, which opens the picker "Select one App
     workspace file or saved output".
  3. **Review native act / decline / cancel…**, which opens the dialog
     "Chirality — act on App content" with the button **mark checked**
     (`file_act_native.rs:56-87`).
- **Eligible files:** any regular, non-symlinked file inside the project.
  Neither a model nor sign-in is needed (`act_control_file.rs:127-217`).
- **Where captures land:** `records/projects/<key>/captures/<id>.json`. Act lines
  go to `acts/*.jsonl`. The capture binds the file's SHA-256, not its content.
- **Before enrollment:**
  - Sealing first establishes publisher and S4 authority, then returns before
    any keychain operation or marker (`capture_seal_keychain.rs:164-175,610-614,931-937`).
  - The capture records "capture not sealed (SEAL-C keychain continuity not
    enrolled; …)" (`act_control_file.rs:390-395`).
- **Enrollment:**
  - App menu ▸ **Prepare capture sealing…** opens the dialog "Prepare capture
    sealing". It names the service, account and access group, and reads
    "Committed and pending key IDs: none observed". Its buttons are **Leave
    unchanged** and **Prepare capture sealing**.
  - Success shows "Capture sealing check completed for the prepared
    installation." (`seal_c_enrollment.rs:18-23,117-195`).
  - Preconditions: `capture-seal` is absent and the base item reads as missing
    (`capture_seal_keychain.rs:505-509,785-793`).
  - The item is a data-protection, non-synchronizable item, with no UI allowed,
    `WhenUnlockedThisDeviceOnly` (`capture_seal_keychain_macos.rs:195-203,405-411`).
  - The marker `capture-seal-keychain/continuity.s1.json` is published as
    pending before the add, then as committed (key IDs and digests only)
    (`capture_seal_keychain.rs:292-310,1007-1019`).
  - The outcome notice goes to the screen and stderr only. No App file records it.
- **Verification:**
  - It runs only when the person presses **Read file-act log and current
    content**. It is not automatic on relaunch.
  - A row that fails shows a "…; not verified here" line, such as "capture has no
    App seal …".
  - A verified row shows no such line and `captureCorrespondence: true`. The App
    has no positive "verified" wording (`capture_seal.rs:292-312`;
    `file_act_view.rs:488-567`).
  - Do not press **Observe file-act content changes and save history**. It may
    write lapse records.

Window and Quit:

- **Closing the window hides it.** The App keeps running (`lib.rs:2685-2688`).
- **Reopening:** the macOS reopen event, sent when the running App's own Dock
  tile is clicked, shows the original window (`lib.rs:2841,1308-1314`). No menu
  item shows the window.
- **Quit item:** the App's own **Quit Chirality App v4** item. With no live work
  it exits **without** a question (`app_quit.rs:12-15,118-128`). The "Quit
  Chirality" question appears only with live work, which this model-free session
  cannot create.

## Owner-facing sequence

This takes about 30 minutes of the owner's time. Every App act is the owner's
own act. The agent never logs in as, automates or receives the password of the
test user. "Agent:" lines run in the owner's own session, after approval. Only
Q1 is offered for quarantine. A synthetic `xattr` route is not part of this
request.

1. **Create the user.** System Settings ▸ Users & Groups ▸ Add User: Standard,
   `Chirality V4 Test` / `chiralityv4test` or the owner's choice, with a private
   password. Switch to it. In Setup Assistant, skip the Apple Account and iCloud.
2. **Agent stages the tools and the download.**
   - The agent copies `signed_witness_collect.sh` from the approved PR head into
     `/Users/Shared/chirality-v4-witness-tools/` (0755 directory, 0644 file) and
     prints its SHA-256.
   - It clones the DMG into a fresh scratch directory, checks `34ab5661…26e`,
     and serves only that directory on `http://127.0.0.1:8765/`.
3. **Download and install.** Do this in the test user.
   - In Terminal, first run
     `C=/Users/Shared/chirality-v4-witness-tools/signed_witness_collect.sh`, then
     `shasum -a 256 "$C"`, and compare with the agent's value. If you open a new
     Terminal window later, run the `C=` line again.
   - In Safari, open `http://127.0.0.1:8765/` and download the DMG. Tell the
     agent, which stops the server.
   - In Terminal, run `sh "$C" prepare`. It creates the private evidence folder
     and the invented fixtures, and prints the setup paths.
   - Double-click the DMG in Downloads. Make a folder `Applications` in the test
     user's home and drag **Chirality App v4** into it. Do not use `/Applications`.
4. **Gate.** Run `sh "$C" c1 ~/Downloads/Chirality-App-v4-4.0.0-f664ee1d-b3dd4145.dmg`.
   It must end with **Gate passed**. On **STOP** or **refused**, do not launch;
   tell the agent.
   Eject the DMG.
5. **Record.** Press ⇧⌘5 ▸ Options ▸ Save to ▸ Other Location… and choose
   `/Users/Shared/chirality-v4-witness-out/recording`. Then Record Entire Screen.
6. **First launch.** Double-click **Chirality App v4** in the test user's
   `Applications` folder, never Spotlight or Launchpad. Answer **Open** to
   Gatekeeper. "Setup needed" appears.
7. **Set up.** Use **Prepare a new account home**, the four paths printed by
   `prepare`, and the only supplier option. Then **Review setup effects** ▸
   **Prepare home and save for next launch**, and the same button in the native
   dialog. Press ⌘Q; the App exits with no question.
8. **Relaunch** the same way. Wait for "Codex is connected". Open **Host
   diagnostics** so that "State: ready … codex-cli 0.160.0" and "Supplier
   standing: verified-pin" are on screen for a few seconds. If Codex does not
   connect, stop.
9. **Before enrollment.**
   - Open **Files and standing acts**. Set Kind `mark checked`, Scope `witness`
     and Purpose `pre-enrollment`.
   - Press **Select file and freeze preview…** and pick `check-1.txt`. Then press
     **Review native act / decline / cancel…** ▸ **mark checked**.
   - Press **Read file-act log and current content** and expand **Source,
     content identities and correction relations** on the `check-1.txt` row. Its
     lines include "capture has no App seal … not verified here".
   - Run `sh "$C" c2`.
10. **Enroll.** App menu ▸ **Prepare capture sealing…**. The dialog shows
    "Committed and pending key IDs: none observed". Choose **Prepare capture
    sealing**; the notice reads "Capture sealing check completed for the
    prepared installation." If any keychain or password prompt appears, choose
    Deny or Cancel, and stop.
11. **After enrollment.**
    - In **Files and standing acts**, set Purpose `after enrollment`. Press
      **Select file and freeze preview…**, pick `check-2.txt`, then **Review native
      act / decline / cancel…** ▸ **mark checked**.
    - Press **Read file-act log and current content** and expand the `check-2.txt`
      row. It must show no "not verified here" line and must show
      `"captureCorrespondence": true`. Otherwise stop.
    - Run `sh "$C" c3`. Do not run `c2` again.
12. **Close and reopen.** Close the window with the red button. Click the running
    **Chirality App v4** Dock tile, the only Chirality tile in this Dock (its name
    shows on hover). The same workspace returns.
13. **Restart and verify.**
    - Press ⌘Q (it exits with no question). Relaunch as in step 6 and wait for
      "Codex is connected", with Host diagnostics open.
    - Press **Read…** and expand the same `check-2.txt` row: same `captureId`, no
      "not verified here", `captureCorrespondence` true, and no prompt.
    - Press ⌘Q.
14. **Finish.** Run `sh "$C" c4`, then stop the recording. Run `sh "$C" handoff
    <owner account>`, which gives only the owner's own account read access to
    the evidence folder. Tell the agent.

If anything else appears, such as a refusal, a hang or an unexpected dialog,
stop. Tell the agent. Do not retry, grant, override, force-quit or log out
unless the owner separately decides on an exceptional recovery (below). A
refused checkpoint command leaves its partial folder in place. It is never
rerun over that folder.

## Internal evidence checklist

All files listed are under `/Users/Shared/chirality-v4-witness-out/`.

| Item | Evidence | Kind | If missing or failed |
|---|---|---|---|
| W-0 installer digest and quarantine | `c1/dmg-sha256.txt`, `dmg-quarantine.txt`, `dmg-xattr-l.txt`; `gate.txt` | command output | blocked |
| W-1 mounted Gatekeeper | `c1/mounted-spctl.txt` | command output | blocked; a refusal is a failure |
| W-2 install path (per-user `~/Applications`, a recorded deviation), installed quarantine, first-launch Gatekeeper | `c1/installed-path.txt`, `installed-quarantine.txt`, `installed-xattr-l.txt`; recording | command output + display | blocked; a refusal is a failure |
| W-2 translocation component | `c4/appdata/runtime/distribution/s1-*/.chirality-s1/installed.json` | App file | inconclusive |
| W-6 installed signature, exact entitlements, cdhash, embedded profile `5eccea61`, stock supplier identifiers, installed content and structure | `c1/installed-*.txt`, `installed-entitlements.plist`, `installed-profile-sha256.txt`, `supplier-*.txt`, `installed-content.txt`, `installed-ownership.txt`; `gate.txt` | command output | blocked |
| W-3/W-4/W-5 version, Codex verified, supplier ready | `c1/installed-version.txt`; `c4` distribution publications; Host diagnostics on the recording | file + display | failed or blocked as observed |
| Setup saved, then Quit, then relaunch at `saved-request` | recording; `c4/appdata/desktop-startup/request.json`, `appdata-metadata.txt` | display + file | failed or blocked as observed |
| S4 publication closure | `c4/appdata/runtime/distribution/s1-*/`, the complete App-written publications (selected reference members plus `.chirality-s1/{observed,installed,preflight,transport,lifecycle}.json`) | App files | no App export exists |
| SC-3 pre-enrollment: capture unsealed; no marker and no `capture-seal` directory | `c2/appdata/records/projects/*/captures/*.json` (no `seal`, with the limit); `c2/marker-stat.txt` | App files | failed |
| One enrollment, committed marker | `c3/appdata/capture-seal-keychain/continuity.s1.json` (one key, `pending` null) | App file | failed or unknown |
| The same sealed capture verifies before and after restart | `c3`/`c4` capture with `seal`; recorded expanded rows | file + display | failed |
| No second add across restart | `c3` vs `c4` marker: identical bytes, inode and mtime | App file only | inconclusive |
| No keychain prompt | recording | display only | inconclusive |
| Window hide and reopen; Quit with no question; App and supplier exit | recording; the agent's read-only census, if approved | display + process listing | as observed |

Claim limits:

- **Marker and recording are not OS proof.** An unchanged marker plus the
  recording support "no second add" and "no prompt" at the App's own level. They
  are not an OS-level keychain trace and do not prove provider internals.
- **Displayed text is display evidence only.** It is not an authoritative export.
- **The census is corroboration only.** It neither establishes ownership nor
  proves the absence of escape.
- **Unrecorded outcome.** Enrollment success is visible only on screen.

### Collector

[`signed_witness_collect.sh`](signed_witness_collect.sh) copies only the items
above:

- the c1 command outputs;
- the marker and `capture-seal` stats;
- captures and act logs, at their AppData-relative paths;
- `request.json`;
- the complete `runtime/distribution/s1-*` publications;
- an AppData name and metadata listing in which `account-homes` itself is pruned,
  so it is never read;
- a content manifest of the invented fixtures.

Its safeguards:

- It refuses symlinks along every path before any traversal, stat, hash or copy.
  That covers the output root, the given DMG, the AppData root, the fixture root,
  the marker directory, the capture, act and distribution directories, every
  member of the installed App, and the `manifest` root.
- Copied trees and manifests also refuse special files and names containing
  newlines.
- Every traversal, temporary-file, sort, stat and hash step is checked
  explicitly, so a failure gives exit 2 and no digest. This does not rely on
  `set -e`, which is suppressed when callers test a function.
- The mounted DMG App is read only through `spctl` and `xattr`.
- It never overwrites.
- It never reads the keychain.
- Output is 0700/0600 under a root that it creates and checks: owned by the user,
  mode 0700, not a symlink.
- After c4, `handoff` grants read access to exactly one named account through
  ACLs.
- c1 has two failure outcomes, and either means do not launch:
  - exit 3 records each failed check as STOP in `gate.txt`;
  - exit 2 ("refused") stops at an unsafe or unreadable path before the gate
    finishes, leaving partial evidence in `c1/`.

**Installed-copy comparison.** Bundle-tree v2 `b3dd4145` remains the identity
of the signed package. The DMG's contained App was recorded with that identity.
v2 also binds ownership and refuses extended attributes outside its allowlist
(`identify.py`). A correctly quarantined copy owned by the test user therefore
cannot be expected to reproduce it, so v2 is neither recomputed nor redefined
here.

c1 instead checks a separate **content-and-structure manifest**. It covers every
path, its type and permission bits, file SHA-256s and link targets. It excludes
owner, group, times and extended attributes. Its digest must equal
`ae04bcaaba7c3eb7ec77248cd2302d5449c3421f2e2b353e1b4e2d7e69b14f6a`, computed by
the helper's `manifest` mode on the retained signed App directory. Deep strict
verification and the cdhash bind the same content to the signature. Quarantine
and ownership are recorded separately. If a Finder copy changes any permission
bit, c1 stops. There is no automatic chmod and no baseline replacement. The
packaging lane accepted this in place of an
installed v2 value (see below).

Assurance so far: fake-home checks only, repeatable as
[`test_signed_witness_collect.py`](test_signed_witness_collect.py). Its 12 tests
pass, run in task scratch. They cover:

- administrator refusal, the private 0700 root and no rerun of `prepare`;
- c2–c4 allowlist copies, 0600 modes and no overwrite;
- `account-homes` (made mode 000) never read;
- refusal of symlinks at the fixture root, the marker directory, the capture
  directory and the given DMG;
- manifest refusal of newline names, FIFOs, unreadable files, unreadable
  directories and a symlinked root;
- manifest failure when `find` or `sort` fails;
- digest change on content change;
- `handoff` granting exactly one named account and refusing an unknown one.

When the retained candidate is present, one more test runs c1 on a quarantined
clone. There, every check passes except DMG quarantine and the mount, and an
added symlink in the App is refused.

c1 also ran against an APFS clone of the signed App and the real DMG. The DMG
digest, the deep strict check, notarized Gatekeeper, cdhash, identifier, team,
exact entitlements, embedded profile, the four stock supplier identifiers,
content and structure, executable and version 4.0.0 all passed. Quarantine and the
mounted checks stopped, as expected for a local, unmounted copy.

Disclosure: Gatekeeper and codesign output contains the certificate holder's
name. Any repository record redacts it as
`origin=Developer ID Application: <name> (8A7JL35U4S)`, as packaging records do.
Evidence otherwise stays in private scratch until the agent's disclosure review.
The account-home names and project paths it contains refer only to the test user.

## Consumer confirmation (before the owner is asked to approve)

- **Packaging** (<t3-thread://v2/00d44996-9458-4eba-bed2-ffb8f49dab60/mcp:launch:29a4e14ac4c1423f4ccd20d7605000caf9a5b6d9030c967d51875cd09021e07f>),
  2026-11-03:
  - It matched the subject: DMG `34ab5661…`, App `b3dd4145`, executable
    `49f61681`, cdhash `e1bf4644`.
  - It specified the W-0, W-1, W-2, W-6 and S4-join observations, which c1/c4
    now collect.
  - It accepts per-user `~/Applications` as a recorded W-2 deviation.
  - It joins the publications to package identity `b3dd4145`, publisher binding
    `58463a02`, requirement `86d40090`, and the DMG digests `1a962e3a` (pre-staple)
    and `34ab5661` (stapled).
  - It requires no additional install, launch, account or enrollment permission.
- **Runtime / SEAL-C** (<t3-thread://v2/00d44996-9458-4eba-bed2-ffb8f49dab60/mcp:launch:72b0bb46c6645f2fd7155deab7d5ff1fa5b3b56a4e77151178a0e322c1e906ae>),
  2026-11-03, read-only at `f664ee1d`: **confirmed** that c2/c3/c4 plus the
  recording meet SC-3's retain list. No owner step changes. It also confirmed
  the source reading above, with one precision:
  - Pre-enrollment sealing first builds publisher and S4 authority
    (`capture_seal_keychain.rs:164-175`). It then returns "SEAL-C keychain
    continuity not enrolled; not verified here" for the absent directory
    (`:931-937`) before any keychain call.
  - Any other c2 reason is SC-3 blocked or failed at that cause.

  The analysis-time joins it requires, all from files already collected:
  - **J1:** the c2 limit text is exactly that "not enrolled" reason, and c2
    stats show `capture-seal-keychain/` and `capture-seal/` absent.
  - **J2:** the c3 marker has format `capture-seal-keychain-continuity.s1`,
    exactly one committed key, `pending` null, and `scope_sha256`
    `f076bd22f90843aab58b83253b452ce81f1d0f02d2cda1706e9cf63f378975c4`.
  - **J3:** the `check-2` seal key ID equals the marker's committed key, and the
    `check-2` capture bytes are identical from c3 to c4.
  - **J4:** the `check-1` capture bytes are identical across c2, c3 and c4, and
    stay unsealed.
  - **J5:** the c3 and c4 markers are identical in bytes, inode and mtime. This
    is App-level evidence, not an OS trace.
  - **J6:** the c4 S4 `installed.json` names the same signed App (cdhash and
    path) as c1.

  The embedded-profile check (`5eccea61`) was added to c1 at its suggestion.
  The prompts that matter on the recording are at enrollment, at the `check-2`
  seal, and at the restart verification. SC-4 and SC-5 remain uncovered. W-3,
  W-4 and W-5 stay with this lane.
- **Packaging, W-6 installed-copy comparison:** **accepted** at head `8e8bb816`
  (2026-11-03).
  - Packaging independently reproduced the manifest digest `ae04bcaa…6a`, both
    from the retained signed App directory and from the App inside the stapled
    DMG `34ab5661` (read-only nobrowse mount, detached).
  - Its join binds the package identity bundle-tree v2 `b3dd4145` to that
    manifest for the installed copy.
  - v2 is neither recomputed for the installed copy nor redefined, and
    quarantine is never removed.

## Exceptional recovery (owner decides at the time; nothing is pre-authorized)

- **App hangs, or Quit is refused:** record it and tell the agent. Proposed
  options for the owner to decide on are waiting, Force Quit, or logging out of
  the test user. The latter two are abnormal settlements.
- **Supplier outlives the App:** record the census. Nobody signals it. Logging
  out of the test user is the proposed recovery act, and it needs the owner's
  explicit decision.
- **Gatekeeper, enrollment or keychain refusal or prompt:** stop that part.
  Never grant, override, retry or delete.

## Retention

Keep the test user, its keychain item, AppData, fixtures, the recording and the
handoff folders. Also keep the DMG, the pre-staple DMG, the signed and unsigned
Apps and all logs. They stay until the named consumers (packaging S4/W-0…W-6,
runtime SC-3/SC-6, this native lane) confirm receipt and integration, and any
needed recovery is released. Deleting the test user is a later, separate owner
decision. It is not proposed now.

## Not covered

- model access or sign-in (V4-EXM-12);
- the V4-EXM-10/11 journeys;
- the live-work Quit question;
- SC-4;
- SC-5, blocked for 4.0.0;
- v3 work;
- acceptance, replacement or release.

The setup option shows the wording "Bundled supplier — unqualified owner-use
development", and this build ignores that choice in favour of the production
configuration. The Host diagnostics also repeat the prefix "Desktop setup
required:". Both are wording findings for Agent 0. Changing either creates a new
candidate.

## Owner decisions requested

Runtime and packaging confirmations are recorded above.

1. Create the standard test user (the owner's act).
2. Approve the Q1 transfer: a loopback-only Safari download from a short-lived
   agent server, plus the agent staging the helper in
   `/Users/Shared/chirality-v4-witness-tools/`.
3. Approve steps 1–14. They include one real keychain enrollment in the test
   user, the screen recording, the collector runs and the final single-account
   handoff. Optionally, approve the agent's read-only `ps` census of the test
   user's processes.
