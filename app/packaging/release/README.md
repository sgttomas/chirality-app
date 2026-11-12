# Release 4.0.0: build, sign and record the package

Three tools turn a finished source into the 4.0.0 package `Chirality.app`
(bundle identifier `com.chirality.app`, version 4.0.0, minimum macOS 15,
Apple Silicon), as DEL-01-06 governs:

| Tool | Who runs it | What it does |
|---|---|---|
| `build.py` | an agent | builds the unsigned candidate and writes `CANDIDATE.json` |
| `owner_sign.py` | the owner only | signs, notarizes and staples the App, then the disk image, then writes the package identity record |
| `record.py check` | the owner or an examiner the owner authorises | re-reads a package and reports every difference from its record |

Inside `Chirality.app` the main executable is `Contents/MacOS/chirality-app-v4`:
Tauri names the bundle after `productName` ("Chirality", set in the generated
overlay) and keeps the Cargo binary name for the executable, because no
`mainBinaryName` is set. The supplier's Codex is at `Contents/Resources/codex/`
unchanged.

## Building the candidate (agents)

`build.py` takes a frozen source export (never a live checkout), the vendor
tree with its expected manifest and pin, prepared offline caches, the
resolved `rustc`, `cargo`, `clang` and `ld`, and only `PATH` and `LANG` from
the caller:

```sh
python3 app/packaging/release/build.py \
  --source-root /abs/export --revision <40-hex> \
  --vendor /abs/vendor --expected-manifest <64-hex> --pin <pin> \
  --cargo-cache /abs/prepared-cargo-home --npm-cache /abs/prepared-npm-cache \
  --env PATH=<toolchain bin>:<node bin>:/usr/bin:/bin --env LANG=en_US.UTF-8 \
  --tool rustc=... --tool cargo=... --tool clang=... --tool ld=... \
  --out /abs/new-candidate
```

Everything the install and the build write is inside `--out`: the source
export and both caches are copied in and never written, and `HOME`, `TMPDIR`,
`CARGO_HOME`, `CARGO_TARGET_DIR`, `CODEX_HOME` and npm's cache, logs and
configuration all point inside `--out`. `PATH` must name the toolchain's own
`bin` directory, not rustup proxies.

It writes the publisher input (identifier and Developer ID team) from the
compiled keychain selection in `app/src-tauri/src/capture_seal_keychain.rs`
of the export into its output, unless `--publisher-input` and
`--publisher-sha256` supply one. It then runs `prepare.py`, `check_plan` and
`verify_cargo_build_input`, installs the npm dependencies offline, runs the
recipe from an empty environment, and checks the result:

- Apple's `dyld_info -validate_only` passes on every Mach-O file.
- The Info.plist states the release identity.
- The vendor tree matches the input in bytes, modes and types.
- Every mapped resource matches its source in bytes.
- The executable holds the compiled publisher binding and requirement.
- The App's own code carries only the linker's ad hoc signature.

`CANDIDATE.json` is written only after every check passes. A failed run
leaves `BUILD_FAILED.json` and `INCOMPLETE.txt`, and the signing step refuses
such a folder. The provisioning profile is not a build input: `owner_sign.py`
places it.

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
- The **candidate directory** an agent built (it holds `CANDIDATE.json` and
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

The run signs the App and checks the signature. It then archives the App for
submission, notarizes it, staples its ticket to it and checks it again. It
makes the disk image `Chirality-4.0.0.dmg` from the stapled App and
`Release Limitations.md`, signs the disk image, notarizes it and staples its
ticket to it. Last, Gatekeeper assesses the disk image and the App on a
read-only mount, and the run writes the package identity record. Some things
it never does:

- It signs exactly twice, once for the App and once for the disk image.
- It never signs with `--deep` or `--force`, and never inside the supplier's
  Codex.
- After the App's ticket is stapled, nothing writes into the App.

**Two notarization waits.** The run submits to Apple's notary service twice,
once for the App and once for the disk image, and waits for each answer. The
service usually answers within minutes; sometimes it takes longer. That is an
expectation, not a promise. If a wait is interrupted, for example when the
network drops, the run stops with a STOP. Nothing is half-published: a ticket
is stapled only after an accepted answer, and the folder is never
distributed by the tool. Run again into a new `--out` folder.

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
supplier's files are shown unchanged by the comparison of the whole tree,
bytes, modes and types, after signing and again after stapling, together with
their unchanged code-directory hashes.

### If it stops

It prints `STOP: <step>: <reason>`, writes `STOPPED.json`, runs nothing
further and writes no `RESULT.json`.

| Step | Meaning |
|---|---|
| `refused` | An argument, the environment, the host, a location or the candidate is not acceptable; nothing ran. A candidate that "does not verify" changed after it was built, or its build did not finish: ask for a new build. |
| `0 supplier signatures` | A file in the supplier's Codex lacks the supplier's signature, hardened runtime, timestamp or code-directory hash, or its entitlements are unreadable. The supplier's files are never re-signed (DEL-01-06 CLM-002): whether this pin can ship is your decision. |
| `1 copy` | The working copy of the App differs from the candidate. Retry in a new folder; report it if it recurs. |
| `2 profile` | The provisioning profile does not grant `8A7JL35U4S.com.chirality.app` for team 8A7JL35U4S as a Developer ID profile, or has expired. |
| `3 entitlements` | The profile and the compiled publisher identity disagree. |
| `4 sign App` | `codesign` failed: usually the identity name, a locked keychain or a refused access prompt. See `log.jsonl`. |
| `5 verify App` | The signed App is not what was intended (verification, requirement, entitlements, a failed display, or a change beyond the executable, `_CodeSignature` and the profile). Do not use it. |
| `6 notarize App` | Archiving the App changed it or failed; or Apple did not accept the App, reported issues, gave no issues field, or its log names other bytes. Nothing was stapled. |
| `7 staple App` | Stapling or validating the App's ticket failed, or stapling changed more than adding the ticket. |
| `8 verify stapled App` | The stapled App no longer verifies as intended. |
| `9 disk image` | Making, signing, verifying or displaying the disk image failed. |
| `10 notarize disk image` | As step 6, for the disk image. |
| `11 staple disk image` | Stapling or validating the disk image's ticket failed. |
| `12 Gatekeeper` | Gatekeeper did not accept the disk image or the App, the mounted copy differs, or the disk image did not detach. |
| `13 record` | An observation the record states failed (a display, an entitlement reading, a ticket validation, a Gatekeeper assessment), or the disk image did not detach. No record is written. |
| `unexpected` | Any other error; the message names it, redacted. |

### Send back

Send the whole `--out` folder:

- the disk image
- `PACKAGE_IDENTITY.json` and `RESULT.json`
- `notary/`, with the App archive and both notarization logs
- `entitlements.plist` and `log.jsonl`

It holds no credential. One redaction step covers the command log, the
record, the notarization logs, STOP text and standard output. It removes
anything shaped like a password, key, token or account e-mail, and any team
identifier other than 8A7JL35U4S and the supplier's. The identity and profile
appear only as the names you gave, and the provisioning profile only inside
the App, where it ships.

The notarization logs are saved **redacted**. To fetch an original again:

```sh
xcrun notarytool log <submission-id> --keychain-profile <profile-name> original-log.json
shasum -a 256 original-log.json
```

The submission ids are in `PACKAGE_IDENTITY.json` under `notarization`. The
digest should equal that entry's `original_log_sha256`.

## Checking a package against its record

Mount the disk image read-only, then:

```sh
hdiutil attach -readonly -nobrowse -mountpoint /path/mnt Chirality-4.0.0.dmg
python3 app/packaging/release/record.py check /path/release-folder/PACKAGE_IDENTITY.json \
  --dmg Chirality-4.0.0.dmg --app /path/mnt/Chirality.app \
  --limitations-source <source>/docs/RELEASE_LIMITATIONS_4.0.0.md
hdiutil detach /path/mnt
```

It compares the App as signed and the App as signed and stapled, both
tickets, the Gatekeeper assessments, the notarization results against the
saved logs and the App archive, and every recorded fact. It exits 0 with no
difference, or 1 and lists each one, including any observation that failed.
It runs `codesign -d`, `stapler validate` and `spctl --assess`, which only the
owner or an examiner the owner authorises runs on the real package.
