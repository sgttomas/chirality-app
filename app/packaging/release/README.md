# Release 4.0.0: build, sign and record the package

Three tools turn a finished source into the 4.0.0 package `Chirality.app`
(bundle identifier `com.chirality.app`, version 4.0.0, minimum macOS 15,
Apple Silicon), as DEL-01-06 governs:

| Tool | Who runs it | What it does |
|---|---|---|
| `build.py` | an agent | builds the unsigned candidate and publishes `CANDIDATE.json` |
| `owner_sign.py` | the owner only | signs, notarizes and staples the App, then the disk image, then writes the package identity record |
| `record.py check` | the owner or an examiner the owner authorises | re-reads a package and reports differences from its record, and what it did not check |

Inside `Chirality.app` the main executable is `Contents/MacOS/chirality-app-v4`:
Tauri names the bundle after `productName` ("Chirality", set in the generated
overlay) and keeps the Cargo binary name for the executable, because no
`mainBinaryName` is set. The supplier's Codex is at `Contents/Resources/codex/`
unchanged.

## What the tools withstand

These are operator-run tools on stable inputs. They are built so that an
observation that was not made, that failed, or that is incomplete cannot come
out as success, and so that drift and mistakes are caught. They are not a
filesystem snapshot. They are not built to withstand a writer changing the
inputs during the run, or someone with write access forging a record: a
completion marker or a recorded digest is not authentication.

## What the tools write, and the private folder

Each run writes two kinds of file into its own output folder.

- **Returnable files** are the ones you may send back:
  - the command log `log.jsonl`
  - the notarization summaries in `notary/`
  - `PACKAGE_IDENTITY.json`, `RESULT.json` or `STOPPED.json`
  - for a build, `CANDIDATE.json`, `BUILD_REFUSED.json` or `BUILD_FAILED.json`

  These files hold only values the tool builds itself or picks out of a
  tool's output: digests, return codes, shaped identifiers, the two public
  team identifiers, known entitlement keys, and fixed words and reasons. Each
  value is checked against a stated form before it is written. The command
  log holds the commands as the tool built them, with each return code and
  the length and SHA-256 of each output, never the output itself. The
  identity name and the profile name appear only as the values of `--sign`
  and `--keychain-profile`.
- **The private folder**, `PRIVATE-raw-output-may-hold-account-details-do-not-send`,
  holds the raw command output, the raw notarization logs and full error
  traces, for your own diagnosis. It **may contain account details**.
  - It stays on your machine and is not sent back.
  - Agents do not open it: no tool or test of ours reads it after writing.
    That is a rule, not a protection; agents run as your user on your
    machine.
  - When the run is done, delete it or move it somewhere of your own.

A failure prints one fixed reason, which names the step and the observation
that failed. You can usually act on it without sending anything. The detail
is in the private folder.

## Building the candidate (agents)

`build.py` takes:

- a frozen source export (never a live checkout)
- the vendor tree, with its expected manifest and pin
- the prepared offline caches
- the resolved `rustc`, `cargo`, `clang` and `ld`
- only `PATH` and `LANG` from the caller

```sh
python3 app/packaging/release/build.py \
  --source-root /abs/export --revision <40-hex> \
  --vendor /abs/vendor --expected-manifest <64-hex> --pin <pin> \
  --cargo-cache /abs/prepared-cargo-home --npm-cache /abs/prepared-npm-cache \
  --env PATH=<toolchain bin>:<node bin>:/usr/bin:/bin --env LANG=en_US.UTF-8 \
  --tool rustc=... --tool cargo=... --tool clang=... --tool ld=... \
  --out /abs/new-candidate
```

**Where the build writes.**
- The source export and both caches are copied into `--out`.
- It refuses any symbolic link in the caches, and any link in the export
  that leads out of it.
- These all point inside `--out`: `HOME`, `TMPDIR`, `CARGO_HOME`,
  `CARGO_TARGET_DIR`, `CODEX_HOME`, `RUSTUP_HOME`, and npm's cache, logs,
  prefix and configuration.
- Before each write it checks the target path and its parents by filesystem
  identity, and refuses an existing link.
- **Exception:** macOS gives each user a per-user temporary and cache folder
  that is not set through the environment. Xcode's tools may write there,
  and the build does not control it.

`PATH` must name the toolchain's own `bin` directory, not rustup proxies.

**Publisher input.** It writes the publisher input (identifier and Developer
ID team) from the compiled keychain selection in
`app/src-tauri/src/capture_seal_keychain.rs` of the export, unless
`--publisher-input` and `--publisher-sha256` supply one.

**Then it runs** `prepare.py`, `check_plan` and `verify_cargo_build_input`,
installs the npm dependencies offline, runs the recipe, and checks the
result:

- Apple's `dyld_info -validate_only` returns zero with no error text on every
  Mach-O file.
- The Info.plist states the release identity.
- The vendor tree matches the input in bytes, modes and types.
- Every mapped resource matches its source in bytes.
- The executable holds the compiled publisher binding and requirement.
- The App's own code carries only the linker's ad hoc signature.

**Publishing the candidate.** `CANDIDATE.json` appears only as the last act:
the description is verified once more, then renamed into place. Any failure
before that leaves `INCOMPLETE.txt` and `BUILD_FAILED.json`, and the signing
step refuses such a folder. The provisioning profile is not a build input:
`owner_sign.py` places it.

## Signing, notarizing and stapling (the owner)

### Have ready

- In your login keychain: your **Developer ID Application** certificate with
  its private key, named `Developer ID Application: <your name> (8A7JL35U4S)`.
- A **notarytool keychain profile**, stored once by you with
  `xcrun notarytool store-credentials <profile-name>`. Only its name is given
  to the tool.
- The **Developer ID provisioning profile** for `com.chirality.app`
  downloaded from your developer account, and its digest from
  `shasum -a 256 <file>`. It is only read, so it may stay wherever you keep it.
- The **candidate folder** an agent built (it holds `CANDIDATE.json` and
  `RELEASE_LIMITATIONS_4.0.0.md`), and a checkout of this repository with
  Python 3 and `jsonschema`. The candidate and `--out` may not be inside
  `/Applications` or `~/Library`; the limitations file is only read and may be
  anywhere.
- No `APPLE_*`, `TAURI_SIGNING_*` or notary variables in your shell.
- Time for two notarization waits (see below).

### Run

First see the exact commands it will run, then run it:

```sh
python3 app/packaging/release/owner_sign.py --dry-run \
  --identity "Developer ID Application: <your name> (8A7JL35U4S)" \
  --notary-profile <profile-name> \
  --candidate /path/to/candidate \
  --profile /path/to/Chirality.provisionprofile --profile-sha256 <digest> \
  --limitations /path/to/candidate/RELEASE_LIMITATIONS_4.0.0.md \
  --out /path/to/new-release-folder
```

Run the same command without `--dry-run`. macOS may ask you to allow
`codesign` to use your key; that is your act.

The run:

1. signs the App and checks the signature;
2. archives the App, notarizes it, staples its ticket to it, and checks it
   again;
3. makes the disk image `Chirality-4.0.0.dmg` from the stapled App and
   `Release Limitations.md`, signs it, notarizes it and staples its ticket to
   it;
4. has Gatekeeper assess the disk image and the App on a read-only mount;
5. writes the package identity record, and only after the last observation
   succeeded and the disk image detached.

It signs exactly twice, once for the App and once for the disk image. It never
signs with `--deep` or `--force`, and never inside the supplier's Codex.

**The stapled ticket.** Apple's stapler is expected to put the App's ticket at
`Contents/CodeResources`, outside what the signature seals. What the tool itself
establishes is narrower: after stapling, that file is the only change to the
App, and the App then passes its checks again.

**Two notarization waits.** The run submits to Apple's notary service twice,
once for the App and once for the disk image, and waits for each answer. The
service usually answers within minutes; sometimes it takes longer. That is an
expectation, not a promise.

**If the run is interrupted** (Control-C, a dropped network, a timeout):

- It stops with the reason "interrupted" or "unexpected", writes
  `STOPPED.json`, and runs nothing further.
- If a submission was already sent, Apple may still finish notarizing it.
  That publishes nothing, and nothing is stapled after an interruption.
- Run again into a new `--out` folder; that submits again.

This procedure installs nothing. Installing the package, which replaces an
installed v3.0.1, is your act at the installed-package observation.

A successful run does not show that the installed App will accept itself.
Only the installed observation shows that: at its start the App checks its
own signature against its compiled publisher requirement, and checks its
Codex.

### What step 0 and the checks after signing show

Step 0 reads the **signature metadata** of each supplier executable with
`codesign -d`: the signer, team, hardened runtime, timestamp, code-directory
hash and entitlements. It does not check cryptographic validity. The
supplier's files are shown unchanged by comparing the whole tree (bytes,
modes and types) after signing and again after stapling, together with their
unchanged code-directory hashes.

### If it stops

It prints `STOP: <reason>`, writes `STOPPED.json`, runs nothing further and
writes no `RESULT.json`. Each reason is one of a fixed list
(`REASONS` in `common.py`). It begins with the step it comes from:

- `refused`: nothing ran.
- `step 0` to `step 13`: that step's observation failed.
- `guard`, `unexpected` or `interrupted`.

A step 0 reason means a supplier file is not signed as expected. The
supplier's files are never re-signed (DEL-01-06 CLM-002), so whether this pin
can ship is your decision. A step 13 reason means an observation the record
would state failed. `STOPPED.json` then names which observations failed, and
no record is written.

If a STOP comes while the disk image is mounted, the run tries to detach it.
The command log shows whether that worked; if not, use `hdiutil detach`.

### Send back

Send back the returnable files from the `--out` folder:

- `Chirality-4.0.0.dmg`
- `PACKAGE_IDENTITY.json`, and `RESULT.json` or `STOPPED.json`
- `notary/`: the two notarization summaries and the App archive
- `log.jsonl`
- `entitlements.plist`

Do not send the private folder.

To check a saved notarization log against the record, fetch the original
again:

```sh
xcrun notarytool log <submission-id> --keychain-profile <profile-name> original-log.json
```

The submission ids are in `PACKAGE_IDENTITY.json` under `notarization`. Pass
the file to `record.py check` with `--app-original-log` or
`--disk-image-original-log`.

## Checking a package against its record

Mount the disk image read-only, then:

```sh
hdiutil attach -readonly -nobrowse -mountpoint /path/mnt Chirality-4.0.0.dmg
python3 app/packaging/release/record.py check /path/release-folder/PACKAGE_IDENTITY.json \
  --dmg Chirality-4.0.0.dmg --app /path/mnt/Chirality.app \
  [--candidate /path/to/candidate] [--app-original-log FILE] [--disk-image-original-log FILE]
hdiutil detach /path/mnt
```

It first refuses a record that lacks a required field. It then compares the
recorded facts with a new reading of the package:

- the App as signed, and the App as signed and stapled
- the vendor tree and the bundled resources
- signers and known entitlements
- the provisioning profile
- both tickets and both Gatekeeper assessments
- the notarization summaries, and the App archive, which is always compared

Every observation must succeed; a failed one is reported as a failure, never
as equal. Its output lists the differences and, under `not_checked`, what it
did not compare, such as candidate provenance without `--candidate`, or the
original log digests without the logs.

It exits 0 when there is no difference, 1 when there are differences, and 2
with a fixed message when it cannot read its inputs. It runs `codesign -d`,
`stapler validate` and `spctl --assess`, which only the owner or an examiner
the owner authorises runs on the real package.
