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

## What each tool passes to the commands it runs

None of the three passes your whole environment to a command it runs. Each
gives its commands a complete environment of its own:

| Tool | Environment of every command it runs |
|---|---|
| `build.py` | exactly the recipe allowlist: the recipe's fixed values, your `PATH` and `LANG` (the only two variables it accepts from you; anything else refuses), and the run's own writable paths inside `--out`. The same environment serves the three scope observations, the install, the build and `dyld_info`. |
| `owner_sign.py` | exactly `PATH=/usr/bin:/bin:/usr/sbin:/sbin`, your `HOME`, `LANG=en_US.UTF-8` and `TMPDIR` set to `tmp/` inside `--out`. Your environment is otherwise only inspected, to refuse credential-shaped variable names. |
| `record.py check` | exactly `PATH=/usr/bin:/bin:/usr/sbin:/sbin`, your `HOME` and `LANG=en_US.UTF-8`. |

`HOME` is the one value the signing and checking tools take from you. They run
Apple's tools by absolute path (`/usr/bin/codesign`, `/usr/bin/xcrun`,
`/usr/bin/hdiutil`, `/usr/sbin/spctl`, `/usr/bin/ditto`), and `xcrun` finds
`notarytool` and `stapler` in the developer directory selected on the machine,
because `DEVELOPER_DIR` is not passed. The tools give Apple's tools only the
names of your signing identity and notary profile; the keychain lookups are
Apple's tools', made for your user.

What their verification relies on: that those are the system's own tools and
report truthfully, that the inputs stay unchanged during the run (above), and
the digests and inventories the tools compute themselves. It does not rely on
any other value of your environment.

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
  value is checked against a stated form, with a length bound, before it is
  written. That check confirms a value's form, not where it came from: a value
  of valid form that the code selected passes, even if the text inside it is
  something you would not want to send (for example an identifier a tool
  printed, or a file name in the supplier's tree). Read the files before you
  send them. The command
  log holds the commands as the tool built them, with each return code and
  the length and SHA-256 of each output, never the output itself. The
  identity name and the profile name appear only as the values of `--sign`
  and `--keychain-profile`.
- **The private folder**, `PRIVATE-raw-output-may-hold-account-details-do-not-send`,
  holds the raw command output, the raw notarization logs and full error
  traces, for your own diagnosis. It **may contain account details**.
  - It stays on your machine and is not sent back.
  - The rule: no tool, test or agent of ours opens, lists or walks it. Every
    path the tools accept is refused by name if it lies inside a folder of this
    name, before anything is opened.
  - Our tests give the tools an in-memory writer instead. They also run under
    a guard in the test process that refuses the usual ways of listing or
    reading such a folder. The guard is a convention that helps us keep the
    rule, not an enforcement: it does not cover every way a program can reach
    a folder (its limits are written where it is defined, in
    `app/tests/release_fixtures.py`), and agents run as your user on your
    machine, so nothing technical stops them.
  - When the run is done, delete it or move it somewhere of your own.

A failure prints one fixed reason, which names the step and the observation
that failed. You can usually act on it without sending anything. The detail
is in the private folder.

A refusal that comes before the output folder exists (a wrong argument, a
location inside `/Applications` or `~/Library`, an existing `--out`) writes
nothing at all: it prints its fixed reason and runs nothing, and there is no
`STOPPED.json` or `BUILD_FAILED.json`. Those files exist only for runs that
created their output folder.

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
  --out /abs/new-candidate [--not-for-public-release]
```

**Release standing.** While any notice is open (`../notices/coverage.json`), the
build refuses with `BUILD_NOTICE_COVERAGE`; `BUILD_FAILED.json` lists the open
components by name, and any other notice gap by count. `--not-for-public-release`
is an explicit argument, off unless typed; nothing else sets it. With it, the
candidate is an examination candidate, never a publication candidate: the plan
records the standing (`release_standing`, `not_for_public_release` and the notice
coverage's digest, completeness and gap count in `input-inventory.json`, bound by
`PLAN_COMPLETE.json`), `CANDIDATE.json` carries it as `release_standing`, and
`common.load_candidate` refuses a described standing that is not one of
`common.STANDINGS` or differs from the plan. The option changes no bundle input:
the plan's configuration and build environment are the same with or without it,
so the same inputs give the same bundle bytes.

**Where the build writes.**
- The source export and both caches are copied into `--out`.
- Before copying, it refuses every link of every kind in the export and both
  caches: a symbolic link, and a hard link (a regular file whose link count is
  above one).
- It refuses any input path inside a folder named as the private folder, by
  whole component including case aliases, before opening anything. This includes
  the supplied tool paths and PATH directories. A directory-name pass rejects a private entry before
  descending into it, before the input trees are inventoried or copied.
- Before creating `--out`, it compares physical ancestry with the source,
  vendor and cache roots and with the directory holding each read-only input
  file (tools and any supplied publisher selection). An output inside any of
  these is refused. That refusal creates no output or failure receipt.
- These all point inside `--out`: `HOME`, `TMPDIR`, `CARGO_HOME`,
  `CARGO_TARGET_DIR`, `CODEX_HOME`, `RUSTUP_HOME`, and npm's cache, logs,
  prefix and configuration.
- Before each write it checks the target path and its parents by filesystem
  identity, and refuses an existing link.
- **Exception:** macOS gives each user a per-user temporary and cache folder
  that is not set through the environment. Xcode's tools may write there,
  and the build does not control it.

`PATH` must name the toolchain's own `bin` directory, not rustup proxies.
Every command the build runs receives exactly the recipe allowlist, as in
"What each tool passes to the commands it runs" above.

**Publisher input.** It writes the publisher input (identifier and Developer
ID team) from the compiled keychain selection in
`app/src-tauri/src/capture_seal_keychain.rs` of the export, unless
`--publisher-input` and `--publisher-sha256` supply one. A supplied identifier
and team must equal that source selection before the output is created. The
produced binding must also agree with both, as well as the selected input
digest and embedded requirement bytes.

**Then it runs** `prepare.py`, `check_plan` and `verify_cargo_build_input`,
installs the npm dependencies offline, runs the recipe, and checks the
result:

- Apple's `dyld_info -validate_only` returns zero and prints nothing at all,
  on either stream, for every Mach-O file (its manual: "Display nothing if
  binary is valid"). Both streams must be byte-empty; whitespace also fails.
- The Info.plist states the release identity.
- The vendor tree matches the input in bytes, modes and types.
- Every mapped resource matches its source in bytes.
- The executable holds the compiled publisher binding and requirement.
- The App's own code carries only the linker's ad hoc signature.

The three scope observations (`uname`, `sw_vers`, `xcrun`) have a different
declared form: zero exit, exactly one UTF-8-decoded stdout line of the expected
shape after Python `str.strip()` removes surrounding Unicode whitespace, and
no stderr beyond the ASCII whitespace removed by `bytes.strip()`. Additional
stdout lines, a missing value or other stderr fail. These are parser rules;
the invented tests are not observations of the Apple tools.

**Publishing the candidate.** `CANDIDATE.json` appears only as the last act:
the description is verified once more, then renamed into place. After output
creation, the failure handler attempts to leave an incomplete marker
(`INCOMPLETE.txt`) and fixed failure description (`BUILD_FAILED.json`); I/O
failures can prevent either. No candidate is published before final
verification, and the signing step refuses a folder without one. The
provisioning profile is not a build input: `owner_sign.py` places it.

## Signing, notarizing and stapling (the owner)

### First: what this candidate is for

Every candidate states its **release standing** in `CANDIDATE.json`
(`release_standing`), and the dry run below prints it first. There are three:

- `notice coverage complete`: built without `--not-for-public-release`, with
  every shipped component's notice covered.
- `not for public release (named by the caller)`, or the same followed by
  `; notice coverage is incomplete`: an **examination candidate**. An agent
  built it with `--not-for-public-release` typed in the build command. Nothing
  else sets it: no variable, configuration or default. While any notice is
  open, the build makes no other kind of candidate. Such a build is called
  like this:

  ```sh
  python3 app/packaging/release/build.py \
    ... the arguments shown under "Building the candidate" ... \
    --out /abs/new-candidate --not-for-public-release
  ```

You may sign, notarize and staple an examination candidate. That is how the
installed, signed package is examined (criterion 8 of the release target).
Its package is an examination package, never a publication candidate, and it
is not offered for public release while any component's notice is uncovered
(criterion 9). The run never changes or infers the standing: it refuses a
candidate whose standing is missing or differs from the candidate's plan
(`REFUSED_CANDIDATE`), and `RESULT.json` and the package identity record state
the standing as the candidate does. Signing and notarizing publish nothing;
publishing remains your separate decision.

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
   succeeded and the disk image detached. The record states the candidate's
   release standing (`release_standing`), copied unchanged.

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

- It stops with the reason "interrupted" (Control-C) or "unexpected" (any
  other error no check covers, such as a timeout), and writes `STOPPED.json`.
- It starts no further step. The one command it may still run is
  `hdiutil detach` of its own mount point, if the disk image was mounted at
  that moment. Whether the detach worked is in the command log; if it did not,
  run `hdiutil detach <the mount point>` yourself.
- A command that was running when the interruption came may or may not have
  finished. The output folder is then not a basis for anything: do not send
  its disk image, and do not continue from it.
- If a submission was already sent, Apple may still finish notarizing it.
  That publishes nothing, and nothing is stapled after an interruption.
- What is left in `--out` is yours to delete. `tmp/` there may hold
  temporary files of the tools; a fetched notarization log never stays there,
  because it is moved to the private folder as soon as the command returns.

**Starting again.** There is no resuming part-way. Every run starts from the
beginning, from the candidate folder, into a new `--out` folder, and submits
to Apple again. The candidate folder is only read, so the same candidate is
used again unless the run refuses it (`REFUSED_CANDIDATE`), in which case an
agent builds a new one.

This procedure installs nothing and launches nothing. Installing the
package, which replaces an installed v3.0.1, is your act at the
installed-package observation.

**Launching writes into your Library.** The package carries the identifier
`com.chirality.app`, the same one your installed v3.0.1 uses. Launching it is
your act. When it runs, the system web view inside the App writes its website
data and caches under `~/Library`, in folders named for that identifier, as
any launch of an App with that identifier does. Redirecting `HOME` or the
App's data folder does not change that. No tool or test of ours launches the
package, and nothing of ours removes any such folder; they are yours to
clean or keep.

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

It prints `STOP: <reason>`, writes `STOPPED.json`, starts no further step
(apart from detaching its own mount, as above) and writes no `RESULT.json`.
Each reason is one of a fixed list (`REASONS` in `common.py`, with the
owner's steps added from `observations.py`). It begins with the step it
comes from:

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

### A first run may stop on a line nobody declared

The tools read Apple's tools by one rule (`observations.py`). An output counts
only when every line of it is of a form declared for that command, and no key
appears twice in a property list or JSON it parses. Nothing is picked out of
other text, and nothing is concluded from the absence of an error message.
Each declared form names its source: Apple's published technical notes and
notarization documentation, and real outputs kept in this repository, or,
after a stop, your own report of a line's form (below). No form was taken
from running the tools, and none was invented.

Some commands are actions, not observations: the two signings, the archive
made with `ditto`, and `hdiutil create`, `attach` and `detach`. Their output
is not read. Each counts only when it returns zero, and what it did is then
observed: the signature verified and displayed, the archive and the disk
image present and assessed, the mounted contents compared with the stapled
App, and the mount point empty and no longer mounted after a detach.

**The entitlements are read as one whole property list.** `codesign -d
--entitlements - --xml` prints a property list. It counts only when the value
read from it is the whole document. The value is written out again as
Python's `plistlib` writes property lists. The original document is then read
a second way, by its own bytes and without `plistlib`, and must equal that
written copy. Only two things are set aside on both sides, and nothing else:

- **the document header**, compared by its XML declaration (version,
  encoding) and document type rather than by its bytes;
- **whitespace between elements**: space, tab, carriage return and line feed
  directly inside `plist`, `dict` or `array`, and after the document.

Everything else must be byte for byte the same: every element, attribute,
repeated entry and piece of text, in order, and the whitespace inside a value.
So two values side by side, stray text, a comment, a processing instruction,
an unknown element, an attribute or a key given twice all refuse. So does a
valid property list spelled differently from how `plistlib` writes it, for
example `<data>` wrapped differently, a date or number in another spelling,
a character reference, `<true></true>` for `<true/>`, a CDATA section, or no
document type. Entity declarations and undefined entity references refuse,
and nothing is fetched. The sources show entitlements in the written form,
but a first real run may still refuse one spelled otherwise. The reason then
names the entitlements observation of its step (for example
`S5_ENTITLEMENTS`), and the correction below applies unchanged.

**Separate file-reader limits.** The whole-document check above applies to
entitlement command output, not to the provisioning profile or `Info.plist`.
`record.profile_facts`, `prepare.profile_consistency` and
`common.read_info_plist` read their file values with the standard parser and
a repeated-key check. A repeated top-level value is not refused; the parser
can retain the last one. The affected fields are profile UUID, team, App ID,
allowed and unexpected entitlements and expiry, and the bundle identifier,
version, bundle version, minimum macOS and executable. File digests bind
bytes; they do not establish an unambiguous whole-document reading. This is
a named remaining item, outside the command-output repair.

The line-form command readers also have a separate limit: they decode UTF-8
with replacement, drop blank lines and strip trailing whitespace before
matching declared forms. Their result does not establish that the original
stream was valid UTF-8 or preserve those whitespace bytes.

Those sources do not show every line the real tools print. For example, no
source shows the line of `codesign -d` that names the executable. So **a
first real run may stop on a line of output nobody declared**. The reason
then says the output was "not an observation", and names the step.

It stops safely. The step that met the line was an observation, which comes
before anything that depends on it, so nothing further is signed, submitted
or stapled, and no record is written. The raw output is kept in the private
folder, as for every command.

The one correction:

1. You tell us the step and its fixed reason, from the `STOP:` line or
   `STOPPED.json`. Nothing from the private folder is needed for this.
2. An agent looks for the form of that line in the tool's published
   documentation, never in your private output, and adds it to
   `observations.py` with its source.
3. If no published documentation shows the line, the agent says so. You may
   then read your own private output and tell us only the line's form, with
   every value in it removed or replaced (for example `Executable=<path>`,
   never the path itself). An agent may declare that form, with its source
   named as your report (`OWNER` in `observations.py`), never as
   documentation. Only a form you have reported is added this way; none is
   guessed or invented, and no agent reads your raw output to learn it.
4. You run again from the beginning, with the corrected tools, the same
   candidate and a new `--out`, as under "Starting again" above. A correction
   to the declared forms changes the signing tools, not the candidate, so a
   new candidate is needed only if the run refuses the old one.

Each correction may let the run get further and meet the next undeclared
line, so this may repeat. Every repeat submits to Apple again.

### Send back

Send back the returnable files from the `--out` folder:

- `Chirality-4.0.0.dmg`
- `PACKAGE_IDENTITY.json`, and `RESULT.json` or `STOPPED.json`
- `notary/`: the two notarization summaries and the App archive
- `log.jsonl`
- `entitlements.plist`

Do not send the private folder.

**The original notarization logs are not compared by any tool here.** The
record holds each original log's SHA-256 (`original_log_sha256` under
`notarization` in `PACKAGE_IDENTITY.json`), computed when the log was fetched.
To compare one yourself, on your own machine, fetch it again and hash it:

```sh
xcrun notarytool log <submission-id> --keychain-profile <profile-name> original-log.json
shasum -a 256 original-log.json
```

The digest should equal the recorded one. The submission ids are in the same
record.

## Checking a package against its record

Mount the disk image read-only, then:

```sh
hdiutil attach -readonly -nobrowse -mountpoint /path/mnt /path/release-folder/Chirality-4.0.0.dmg
python3 app/packaging/release/record.py check /path/release-folder/PACKAGE_IDENTITY.json \
  --dmg /path/release-folder/Chirality-4.0.0.dmg --app /path/mnt/Chirality.app \
  [--candidate /path/to/candidate]
hdiutil detach /path/mnt
```

Give absolute paths. It refuses any path inside the private folder, by name,
before reading anything. It first refuses a record that lacks a required field. It then compares the
recorded facts with a new reading of the package:

- the App as signed, and the App as signed and stapled
- the vendor tree and the bundled resources
- signers and known entitlements
- the provisioning profile
- both tickets and both Gatekeeper assessments
- the notarization summaries, and the App archive, which is always compared

Every observation must succeed; a failed one is reported as a failure, never
as equal.

Its output is fixed text and counts, grouped by category. It names a
differing location only when the name is a field of the record's own shape,
or a path in the committed distribution record's inventory for the pin.
Anything else, such as an unexpected file name in the package or an unknown
key in the record, is counted and not named. No value read from a file or a
tool is printed.

Under `not_checked` it always lists the original notarization logs (compare
them by hand, as above), and candidate provenance and release standing unless
you give `--candidate`.

Under `release_standing` it shows the standing the record states, and whether
that was checked against the candidate (`checked_against_candidate`). Without
`--candidate` it is only the record's own statement. With `--candidate`, the
candidate's standing must be a known one equal to what its plan states, and
the record's must equal it; otherwise the result is not equal. A record whose
standing is missing or not a known standing is refused as lacking a required
field.

It exits 0 when there is no difference, 1 when there are differences, and 2
with a fixed message when it cannot read its inputs. It runs `codesign -d`,
`stapler validate` and `spctl --assess`, which only the owner or an examiner
the owner authorises runs on the real package.
