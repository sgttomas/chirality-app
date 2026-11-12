# Release 4.0.0: build, sign and record the package

Three tools turn a finished source into the 4.0.0 package `Chirality.app`
(bundle identifier `com.chirality.app`, version 4.0.0, minimum macOS 15,
Apple Silicon), as DEL-01-06 governs:

| Tool | Who runs it | What it does |
|---|---|---|
| `build.py` | an agent | builds the unsigned candidate and writes `CANDIDATE.json` |
| `owner_sign.py` | the owner only | signs, notarizes and staples, then writes the package identity record |
| `record.py check` | the owner or an examiner the owner authorises | re-reads a package and reports every difference from its record |

Inside `Chirality.app` the main executable is `Contents/MacOS/chirality-app-v4`:
Tauri names the bundle after `productName` ("Chirality", set in the generated
overlay) and keeps the Cargo binary name for the executable, because no
`mainBinaryName` is set. The supplier's Codex is at `Contents/Resources/codex/`
unchanged.

## Building the candidate (agents)

`build.py` takes a frozen source export (never a live checkout), the vendor
tree with its expected manifest and pin, the resolved `rustc`, `cargo`,
`clang` and `ld`, and seven environment entries (`PATH`, `HOME`, `LANG`,
`CARGO_HOME`, `NPM_CONFIG_CACHE`, `NPM_CONFIG_USERCONFIG`,
`NPM_CONFIG_GLOBALCONFIG`) pointing at prepared offline caches:

```sh
python3 app/packaging/release/build.py \
  --source-root /abs/export --revision <40-hex> \
  --vendor /abs/vendor --expected-manifest <64-hex> --pin <pin> \
  --env PATH=... --env HOME=... --env LANG=en_US.UTF-8 --env CARGO_HOME=... \
  --env NPM_CONFIG_CACHE=... --env NPM_CONFIG_USERCONFIG=... --env NPM_CONFIG_GLOBALCONFIG=... \
  --tool rustc=... --tool cargo=... --tool clang=... --tool ld=... \
  --out /abs/new-candidate
```

It writes the publisher input (identifier and Developer ID team) from the
compiled keychain selection in `app/src-tauri/src/capture_seal_keychain.rs`
of the export into its output, unless `--publisher-input` and
`--publisher-sha256` supply one. It then runs `prepare.py`, `check_plan` and
`verify_cargo_build_input`, runs the recipe from an empty environment, and
checks the result: Apple's `dyld_info -validate_only` on every Mach-O, the
Info.plist identity, the vendor tree by bytes, modes and types, every mapped
resource by bytes, the compiled publisher binding and requirement inside the
executable, and that the App's own code carries only the linker's ad hoc
signature. Any failure leaves `BUILD_REFUSED.json` and no `CANDIDATE.json`.
The provisioning profile is not a build input: `owner_sign.py` places it.

## Signing, notarizing and stapling (the owner)

### Have ready

- In your login keychain: your **Developer ID Application** certificate with
  its private key, named `Developer ID Application: <your name> (8A7JL35U4S)`.
- A **notarytool keychain profile**, stored once by you with
  `xcrun notarytool store-credentials <profile-name>`. Only its name is given
  to the tool.
- The **Developer ID provisioning profile** for `com.chirality.app`
  downloaded from your developer account, and its digest from
  `shasum -a 256 <file>`.
- The **candidate directory** an agent built (it holds `CANDIDATE.json` and
  `RELEASE_LIMITATIONS_4.0.0.md`), and a checkout of this repository with
  Python 3 and `jsonschema`.
- No `APPLE_*`, `TAURI_SIGNING_*` or notary variables in your shell.

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
`codesign` to use your key; that is your act. Notarization waits for Apple's
answer, usually a few minutes.

It signs the App once (hardened runtime, timestamp, exactly the
`com.apple.application-identifier` and `com.apple.developer.team-identifier`
entitlements), never with `--deep` or `--force` and never inside the
supplier's Codex. It makes the disk image `Chirality-4.0.0.dmg` holding the App
and `Release Limitations.md`, signs it, notarizes it, staples the ticket to the
disk image only, and has Gatekeeper assess the disk image and the App on a
read-only mount.

This procedure installs nothing. Installing the package, which replaces an
installed v3.0.1, is your act at the installed-package observation.

### If it stops

It prints `STOP: <step>: <reason>`, writes `STOPPED.json` and runs nothing
further.

| Step | Meaning |
|---|---|
| `refused` | An argument, the environment, the host or the candidate is not acceptable; nothing ran. The reason names which. A candidate that "does not verify" changed after it was built: ask for a new build. |
| `0 supplier signatures` | A file in the supplier's Codex lacks the supplier's signature, hardened runtime or timestamp. The supplier's files are never re-signed (DEL-01-06 CLM-002): whether this pin can ship is your decision. |
| `1 copy` | The working copy of the App differs from the candidate. Retry in a new folder; report it if it recurs. |
| `2 profile` | The provisioning profile does not grant `8A7JL35U4S.com.chirality.app` for team 8A7JL35U4S as a Developer ID profile, or has expired. |
| `3 entitlements` | The profile and the compiled publisher identity disagree. |
| `4 sign App` | `codesign` failed: usually the identity name, a locked keychain or a refused access prompt. See `log.jsonl`. |
| `5 verify App` | The signed App is not what was intended (verification, requirement, entitlements, or a change beyond the executable, `_CodeSignature` and the profile). Do not use it. |
| `6 disk image` | Making, signing or verifying the disk image failed. |
| `7 notarize` | Apple did not accept the disk image, reported issues, or its log names another file. `notarization-log.json` or `log.jsonl` holds Apple's answer. Nothing was stapled. |
| `8 staple` | Stapling or validating the ticket failed. |
| `9 Gatekeeper` | Gatekeeper did not accept the disk image or the App, or the mounted copy differs. |
| `10 record` | The package identity record could not be read from the package. |
| `unexpected` | Any other error; the message names it. |

### Send back

The whole `--out` folder: the disk image, `PACKAGE_IDENTITY.json`,
`RESULT.json`, `notarization-log.json`, `entitlements.plist` and `log.jsonl`.
It holds no credential: identity and profile appear only as the names you
gave, and the provisioning profile only inside the App, where it ships.

## Checking a package against its record

Mount the disk image read-only, then:

```sh
hdiutil attach -readonly -nobrowse -mountpoint /path/mnt Chirality-4.0.0.dmg
python3 app/packaging/release/record.py check PACKAGE_IDENTITY.json \
  --dmg Chirality-4.0.0.dmg --app /path/mnt/Chirality.app \
  --limitations-source <source>/docs/RELEASE_LIMITATIONS_4.0.0.md
hdiutil detach /path/mnt
```

It exits 0 with no differences, or 1 and lists each one. It runs
`codesign -d`, `stapler validate` and `spctl --assess`, which only the owner or
an examiner the owner authorises runs on the real package.
