# Signed candidate b3dd4145: owner-testing proposal

Standing: **proposal, not run.** Prepared offline on 2026-11-03. Nothing in this
document has been launched, installed, enrolled, captured or created. No account
exists. No operation follows until the owner approves the stages below.

## Subject

| Fact | Value |
|---|---|
| DMG | `Chirality-App-v4-4.0.0-f664ee1d-b3dd4145.dmg`, 156,986,610 bytes |
| DMG SHA-256 (post-staple) | `34ab566132e059d3e51885c87907898238ba95421c88d1303d535d19eafcf26e` |
| Contained App | `Chirality App v4.app`, bundle-tree v2 `b3dd4145779e711a0169c08b2f1757eace19e38e08effe03a18c5bef986b5fb8` |
| Source / ID / version / minimum | `f664ee1dd55f403f7c3498df3f09ac50f77c9a0c` / `com.chirality.app` / 4.0.0 / macOS 15.0 |
| Executable SHA-256 / cdhash | `49f61681…3e6` / `e1bf4644f66389011964e99cec43fc853b6b4158` |
| Recorded standing | Signed, notarized (`430e7461-…`, Accepted) and stapled. Gatekeeper accepted the DMG and the mounted App (read-only mount, no launch). Deep strict verification is valid. |

The signing and notarization facts come from the
[owner signing record](../../../PKG-01/DEL-01-06/Work/selected-production-build/f664ee1d-caec11a00be3/owner-signing.json)
and the scratch `notarization-record.json` in `app-signed-candidate-8DnXAldk`.
The build is publisher `selected-production`. The keychain selection is compiled,
so the App menu offers **Prepare capture sealing…** just above **Quit Chirality App v4**.

This is a new subject. Candidate `1f67d3822b-8c83d74ae3ce`, the `j58087z7`
and `zootd3ob` attempts, and the `795362874d`/`fdcf608fb5` histories keep their
own subjects. None of their observations, admissions or AX results transfer here,
and none is inferred to be fixed.

The local DMG carries no `com.apple.quarantine` attribute: it was produced
locally, not downloaded. Both parent directories are private (`/Users/ryan` is
0750 with an ACL; the candidate directory is 0700). Under production step 5,
missing quarantine is **blocked**, so a deliberate transfer step is required.

## Why a separate macOS user

At this source, AppData is `~/Library/Application Support/com.chirality.app`.
The capture seal, the keychain marker and the records store all derive from it,
and the keychain items live in the user's own keychain. v3 uses the same bundle
ID. A different bundle name or path, or a different `HOME`, does not isolate
these. A fresh standard user isolates them per user, and the owner's existing v3
data, keychain and records are never touched. It also gives SC-3 the fresh
namespace it needs, with no legacy `capture-seal` directory.

This route is the proposed isolation in
[V4 test subject](../../../PKG-01/DEL-01-06/Work/V4_TEST_SUBJECT.md) step 2 and
the [SEAL-C signing join](../../../PKG-01/DEL-01-06/Work/SEAL_C_KEYCHAIN_SIGNING_JOIN.md).
It needs no VM, guest, cloud or media.

## What the owner does

All UI acts in the test user are the owner's own acts. No agent automation,
Accessibility grant or screen capture runs in that session. Estimated owner time
is 45–60 minutes. No model, sign-in, credential or internet use is involved.

### 0. Create the test user (owner, once)

1. System Settings ▸ Users & Groups ▸ Add User. Make it a **Standard** user (not
   an administrator). Full name `Chirality V4 Test`; account name
   `chiralityv4test`, or another name the owner chooses. Choose a password and keep it private.
   Never give it to an agent.
2. Switch to the new user with fast user switching. In Setup Assistant, skip the
   Apple Account and iCloud, Siri and Screen Time, and decline analytics. With no
   Apple Account, iCloud Keychain cannot sync the test key.
3. If FileVault asks whether this user may unlock the disk, either answer is
   fine. It does not affect the test.

### 1. Transfer with real quarantine (owner, with one authorized agent step)

Recommended (Q1): with the owner's authorization, the agent copies only the DMG
(by clone) into a fresh scratch directory. It checks the copy's SHA-256 and
serves that directory from a **loopback-only** HTTP server (`127.0.0.1`, one port, running as the owner's
user) for this step only. In the test user, the owner opens Safari at the given
`http://127.0.0.1:<port>/` URL and downloads the DMG, allowing downloads from
that site if Safari asks. Safari's download sets a genuine quarantine attribute.
The agent stops the server once the owner confirms the download. No traffic
leaves the machine.

Fallback (Q2), only if the owner prefers it: the owner copies the DMG to
`/Users/Shared`, and the test user moves it to `~/Downloads` and writes a
quarantine attribute with `xattr`. That makes the attribute synthetic, and the
result would record it that way.

### 2. Pre-launch facts (owner runs read-only commands in the test user's Terminal)

Create the handoff folder `/Users/Shared/chirality-v4-witness-YYYYMMDD/`, owned
by the test user and readable by others (the default). Then run:

```sh
W=/Users/Shared/chirality-v4-witness-YYYYMMDD; D=~/Downloads/Chirality-App-v4-4.0.0-f664ee1d-b3dd4145.dmg
{ date -u; whoami; id -Gn; sw_vers; ls -ld ~/Library/Application\ Support/com.chirality.app 2>&1
  shasum -a 256 "$D"; xattr -p com.apple.quarantine "$D"; } > "$W/00-prelaunch.txt" 2>&1
```

Expected: `id -Gn` does not list `admin`. AppData does not exist. The SHA is
`34ab5661…26e`. A quarantine value is present.

Open the DMG in Finder. Then, before copying anything:

```sh
M="/Volumes/Chirality App v4/Chirality App v4.app"
spctl -a -vv -t exec "$M" > "$W/01-mounted-gatekeeper.txt" 2>&1
```

Drag the App into `~/Applications` in the test user's home (create the folder if
it is missing). Do **not** use `/Applications`, which holds v3. Eject the DMG. Then:

```sh
A=~/Applications/"Chirality App v4.app"
{ xattr -p com.apple.quarantine "$A"; codesign -dvvv --entitlements - "$A"
  codesign --verify --deep --strict --verbose=2 "$A"; spctl -a -vv -t exec "$A"; } > "$W/02-installed.txt" 2>&1
```

### 3. Session (owner; turn on screen recording first)

Start a screen recording of the whole session (⇧⌘5 ▸ Record Entire Screen) and
save it into `$W`. SC-3's no-prompt observation needs the recording. Launch the
App only by double-clicking `Chirality App v4` in the Finder window showing
`~/Applications`. Do not use Spotlight, Launchpad or the Dock, which could pick
v3 because both share the bundle ID.

| Step | Owner act | Observe |
|---|---|---|
| L1 | First launch; answer **Open** in the Gatekeeper dialog | Exact dialog text, then the main window. A refusal is a **failure**. Do not use "Open Anyway" in System Settings. |
| L2 | Set up the workspace on a new empty folder `~/ChiralityV4Fixtures/p1` | Setup completes. Codex reaches ready in the App's diagnostics (State/generation text). This is the S4 pre-spawn observation and the supplier ready handshake. Model access is not needed. |
| L3 | Create a small invented text file in the project. In the file-act panel, choose **mark checked** and confirm in the native dialog | SC-3 pre-enrollment capture: it is recorded with its "capture not sealed" limit, and no key or marker is created. |
| L4 | App menu ▸ **Prepare capture sealing…** ▸ **Prepare capture sealing** | One explicit first enrollment. **Any keychain password prompt is an SC-3 failure:** choose Deny or Cancel, note it and stop the enrollment part. |
| L5 | Mark a second invented file as checked, the same way as L3 | The capture records as sealed, with no unsealed limit, and its verification reads verified. |
| L6 | Close the main window, then reopen it using whatever the App offers (Dock icon or Window menu) | The same workspace returns with no new setup. If the window cannot be reopened, or closing it ends the App, record exactly what happened. |
| L7 | App menu ▸ **Quit Chirality App v4** | Normal Quit and confirmation wording. The App and Codex both exit. |
| L8 | Relaunch from the same Finder window (expect no Gatekeeper dialog) | Saved workspace relaunch. The L5 capture still verifies with no new keychain add and no prompt. This is SC-3's restart subject. |
| L9 | Quit normally, then stop the screen recording | Normal settlement. |

After L9, copy the evidence. These copies hold no secrets: the key stays in the
keychain and is never exported.

```sh
cp -R ~/Library/Application\ Support/com.chirality.app "$W/appdata"
cp -R ~/ChiralityV4Fixtures "$W/fixtures"
ps -axo user,pid,ppid,pgid,stat,comm | grep -i -E 'chirality|codex' > "$W/09-after-quit-ps.txt"
```

Keep short written notes in `$W/notes.txt`: times, each dialog's text, and
anything unexpected. Then tell the agent that the folder is ready.

### Recovery (owner acts; record each before acting)

- **App stops responding:** wait 60 seconds, then try Quit. If that fails, Force
  Quit (⌥⌘⎋). Record this as abnormal, not a clean settlement.
- **Codex is still running after the App exits** (Activity Monitor, search
  `codex`): do not kill it. Record what is shown, then log out of the test user.
  Logout ends that user's processes. Record the logout as the owner's recovery act.
- **Keychain prompt, enrollment refusal or Gatekeeper refusal:** stop that part.
  Do not retry, grant, override or delete anything. Return the evidence as it is.
- **Cleanup:** keep the test user, its keychain, AppData and fixtures until the
  agent confirms the evidence is received and integrated. They are the restart
  subject. Afterwards the owner may delete the user in Users & Groups, choosing
  "Delete the home folder". That removes the test key, AppData and fixtures. The
  DMG, the unsigned and signed originals and all logs stay preserved. The owner's
  own user, v3 and its data are never part of either step.

## What the agent does

- **Before the session:** if the owner approves Q1, the clone, SHA check and
  loopback server for step 1 only. Optionally, with the owner's authorization, a
  read-only process census from the owner's own session during L2 and L7–L9
  (`ps` filtered to the test user). That census corroborates what the owner sees.
  It does not establish ownership, signal any process or replace the owner's observation.
- **After the session:** copy `$W` into a private scratch evidence root, hash it
  and record what was observed against this subject. Results keep their actual
  standing: passed, failed, blocked, not run or inconclusive. The packaging owner
  assembles `static-package-input/2` with the outer `packaged-s4-binding/1`
  request from these files and the retained pre/post installer bytes, then runs
  the existing `app/packaging/successor/check.py` with an independently selected
  publisher trust. The runtime owner reads the L3–L8 SC-3 evidence. This lane
  records native lifecycle (L1, L2, L6–L9) and returns the joined account.
- The agent never sees the test user's password, never logs in as that user,
  never reads that user's keychain and never runs anything inside that session.

## What this run can and cannot establish

It can supply the production step 5 installed facts: installer quarantine,
mounted and installed Gatekeeper results, installed quarantine, first launch and
version, the actual S4 observation and supplier ready handshake, and the
installed signature, entitlements and cdhash. It can also supply SC-3, plus
basic window close/reopen and Quit/relaunch on the actual signed subject.

It does not supply:

- model access or sign-in (V4-EXM-12);
- the full V4-EXM-10/11 plan-to-refinement journeys;
- SC-4 locked/denied/missing native behavior;
- SC-5, which stays blocked under the 4.0.0 disposition;
- FP/W-4 beyond what the packaging receiver checks;
- v3 comparison or migration, which the owner excluded;
- acceptance, replacement or release.

Those remain outstanding or need separate concrete steps. In particular,
V4-EXM-12 needs the owner present for sign-in and key entry.

## Owner decisions requested

1. Approve, or change, creating the standard local user (step 0). The owner performs it.
2. Choose the quarantine transfer: Q1, loopback Safari download with one agent
   server step (recommended), or Q2, a synthetic `xattr` attribute.
3. Approve the session steps L1–L9, including the one explicit enrollment in L4.
   L4 creates a real keychain item in the test user only. Say whether to add the
   optional read-only process census from the owner's session.
4. Confirm the cleanup rule: the test user is kept until the agent confirms
   integration, and is then deleted by the owner.
