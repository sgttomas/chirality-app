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
- **Files:** `runtime/distribution/s1-<opaque>/.chirality-s1/` holds
  `observed.json`, `installed.json`, `preflight.json` and `transport.json`. A
  later folder holds `lifecycle.json` (`distribution_store_s1.rs:204-256`).
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
  - Sealing returns without a keychain operation or marker (`capture_seal_keychain.rs:610-614`).
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

This takes about 25 minutes of the owner's time. Every App act is the owner's
own act. The agent does not log in as, automate, or receive the password of the
test user. "Agent:" lines run in the owner's own session, after approval.

1. **Create the user.** System Settings ▸ Users & Groups ▸ Add User: Standard,
   name `Chirality V4 Test` / `chiralityv4test` or the owner's choice, with a
   private password. Switch to the user. In Setup Assistant, skip the Apple
   Account and iCloud.
2. **Get the DMG (Q1).**
   - Agent: serve only a clone of the DMG on `127.0.0.1` and give the URL.
   - Owner: in Safari, download it. Then double-click it to mount it, and drag
     the App into the test user's own `Applications` folder (create it if
     missing), not `/Applications`.
   - Agent: stop the server.
3. **Run two commands.** In the test user's Terminal, run the two lines the agent
   gives. They run `signed_witness_collect.sh prepare`, which creates the invented
   fixtures and prints the paths, and `… c1 ~/Downloads/<dmg>`, which records the
   pre-launch facts. Eject the DMG. Start a full-screen recording (⇧⌘5) into
   `/Users/Shared`.
4. **First launch.** Double-click **Chirality App v4** in that `Applications`
   folder, never Spotlight or Launchpad, and answer **Open** to Gatekeeper.
5. **Set up.** Complete Desktop setup with the printed paths and the only
   supplier option, then confirm **Prepare home and save for next launch**.
   Press ⌘Q; the App should exit with no question.
6. **Relaunch** the same way. Wait for "Codex is connected".
7. **Mark checked, before enrollment.** Mark `check-1.txt` checked (Scope `witness`,
   Purpose `pre-enrollment`). Press **Read file-act log and current content**.
   Run the `c2` command.
8. **Enroll.** App menu ▸ **Prepare capture sealing…** ▸ **Prepare capture
   sealing**. If any keychain or password prompt appears, choose Deny or Cancel
   and stop here.
9. **Mark checked, after enrollment.** Mark `check-2.txt` checked (Purpose
   `after enrollment`) and press **Read…** again. Run the `c3` command.
10. **Close and reopen.** Close the window with the red button. Click the running
    **Chirality App v4** Dock tile; its name shows on hover, and it is the only
    Chirality tile in this fresh user's Dock. The same workspace returns.
11. **Quit, relaunch, verify, quit.** ⌘Q. Relaunch, wait for "Codex is
    connected", press **Read…**, then ⌘Q again. Run the `c4` command. Stop the
    recording and tell the agent.

If anything else appears, such as a refusal, a hang or an unexpected dialog,
stop. Note it and tell the agent. Do not retry, grant, override, force-quit or
log out unless the owner separately decides on an exceptional recovery (below).

## Internal evidence checklist

| Item | Source | Kind | Missing means |
|---|---|---|---|
| Installer quarantine and SHA | c1 `dmg.txt` | command output | blocked |
| Mounted and installed Gatekeeper, installed quarantine, signature, entitlements, cdhash | c1 `mounted.txt`, `installed.txt` | command output | blocked; a refusal is a failure |
| First-launch Gatekeeper dialog | recording | displayed only | inconclusive |
| Setup saved, then Quit, then relaunch at `saved-request` | recording; c4 `request.json`, `appdata-metadata.txt` | display + file | failed or blocked as observed |
| S4 observation, custody and supplier ready handshake | c4 `distribution/*/{observed,installed,preflight,transport,lifecycle}.json`; display "ready"/"verified-pin" | App files + display | no export exists; packaging confirms sufficiency |
| SC-3 pre-enrollment capture is unsealed, with no marker or `capture-seal` directory | c2 capture without `seal` and with the limit; c2 `marker-stat.txt` shows both absent | App files | failed |
| One enrollment, committed marker | c3 `continuity.s1.json` (one key, `pending` null) | App file | failed or unknown |
| Sealed capture verifies, before and after restart | captures with `seal`; recorded **Read…** rows | file + display | failed |
| No second add across restart | c3 vs c4 marker: identical bytes, inode, mtime | App file only | inconclusive |
| No keychain prompt | recording | display only | inconclusive |
| Window hide and reopen; Quit with no question; App and supplier exit | recording; agent's read-only census, if approved | display + process listing | as observed |

Claim limits:

- **Marker and recording are not OS proof.** An unchanged marker plus the
  recording support "no second add" and "no prompt" at the App's own level. They
  are not an OS-level keychain trace and do not prove provider internals.
- **Displayed text is display evidence only.** It is not an authoritative export.
- **The census is corroboration only.** It neither establishes ownership nor
  proves the absence of escape.
- **Unrecorded outcome.** Enrollment success is visible only on screen.

The collector copies **only** these items:

- the marker and the `capture-seal` existence check;
- the captures and act logs;
- `request.json`;
- the five named distribution files;
- an AppData name and metadata listing that stops at `account-homes/`;
- fixture hashes.

It never enters `account-homes/` (the Codex home), never reads the keychain, and
copies no fixture contents or other runtime files. All of it stays in private
scratch until the agent's disclosure review. `transport.json` and
`preflight.json` contents have not been reviewed yet. Nothing from it is
committed or published before that review. The packaging owner must confirm that
these files can feed `packaged-s4-binding/1`, and the runtime owner that they
meet SC-3, **before** execution. No sufficiency is claimed here.

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

1. Create the standard test user (the owner's act).
2. Choose the quarantine transfer:
   - **Q1 (recommended):** a loopback-only Safari download, with a short-lived
     agent server.
   - **Q2:** an `xattr` attribute written by the test user, recorded as synthetic.
3. Approve steps 1–11, including one real keychain enrollment in the test user,
   the screen recording, the collector runs, and optionally the agent's
   read-only `ps` census of the test user's processes.
