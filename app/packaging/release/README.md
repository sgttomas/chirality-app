# Release 4.0.0: build the candidate

`build.py` turns a finished source into the unsigned candidate of the 4.0.0
package `Chirality.app` (bundle identifier `com.chirality.app`, version 4.0.0,
minimum macOS 15, Apple Silicon), as DEL-01-06 governs. An agent runs it. It
signs nothing; signing, notarizing and stapling the package are the owner's
acts and are not described here.

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

- **Returnable files** are the ones that may be sent back: `CANDIDATE.json`,
  `BUILD_REFUSED.json` or `BUILD_FAILED.json`.

  These files hold only values the tool builds itself or picks out of a
  tool's output: digests, return codes, shaped identifiers, the two public
  team identifiers, known entitlement keys, and fixed words and reasons. Each
  value is checked against a stated form, with a length bound, before it is
  written. That check confirms a value's form, not where it came from: a value
  of valid form that the code selected passes, even if the text inside it is
  something one would not want to send (for example an identifier a tool
  printed, or a file name in the supplier's tree). Read the files before
  sending them.
- **The private folder**, `PRIVATE-raw-output-may-hold-account-details-do-not-send`,
  holds the raw command output and full error traces, for diagnosis on the
  machine that ran the build. It **may contain account details**.
  - It stays on that machine and is not sent back.
  - The rule: no tool, test or agent of ours opens, lists or walks it. Every
    path the tools accept is refused by name if it lies inside a folder of this
    name, before anything is opened.
  - Our tests give the tools an in-memory writer instead. They also run under
    a guard in the test process that refuses the usual ways of listing or
    reading such a folder. The guard is a convention that helps us keep the
    rule, not an enforcement: it does not cover every way a program can reach
    a folder (its limits are written where it is defined, in
    `app/tests/release_fixtures.py`), and agents run as the machine's user,
    so nothing technical stops them.
  - When the run is done, delete it.

A failure prints one fixed reason, which names the step and the observation
that failed. It can usually be acted on without sending anything. The detail
is in the private folder.

A refusal that comes before the output folder exists (a wrong argument, a
location inside `/Applications` or `~/Library`, an existing `--out`) writes
nothing at all: it prints its fixed reason and runs nothing, and there is no
`BUILD_FAILED.json`. That file exists only for runs that created their output
folder.

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
- Before copying, it refuses every link of every kind in the export and both
  caches: a symbolic link, and a hard link (a regular file whose link count is
  above one).
- It refuses any input path inside a folder named as the private folder, by
  name, before opening anything.
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

- Apple's `dyld_info -validate_only` returns zero and prints nothing at all,
  on either stream, for every Mach-O file (its manual: "Display nothing if
  binary is valid"). No output line of it is declared, so any line is a
  failure.
- The Info.plist states the release identity.
- The vendor tree matches the input in bytes, modes and types.
- Every mapped resource matches its source in bytes.
- The executable holds the compiled publisher binding and requirement.
- The App's own code carries only the linker's ad hoc signature.

**Publishing the candidate.** `CANDIDATE.json` appears only as the last act:
the description is verified once more, then renamed into place. Any failure
before that leaves `INCOMPLETE.txt` and `BUILD_FAILED.json`, and such a folder
is not a candidate. The provisioning profile is not a build input: it is placed
at signing.
