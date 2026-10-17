# Development App candidate identity — candidate-identity-v2

Owner: DEL-09-01 (EXP §4.1 candidate subject; §8.4 candidate key). Consumer:
DEL-09-02 (SQ I-13, the integration owner names the candidate). It supplies
the `app_candidate` values an EXP result record cites for an unpackaged
`native_development` build. A DEL-01-06 package keeps its own package identity
record; this method neither replaces it nor makes a development build a package.

## Bundle tree identity: `chirality.app.bundle-tree.sha256/v2`

The measured root is the built `.app` directory. Its location and name are not
part of the identity. The root and every descendant are represented with the
metadata that decides what the App can read, run or be denied, and every other
state is refused rather than omitted.

- root: `mode`, `uid`, `gid`, `xattrs`;
- directory: path, `kind: dir`, `mode`, `uid`, `gid`, `xattrs`;
- regular file: as a directory with `kind: file`, plus `size` and the SHA-256
  of its exact bytes;
- symbolic link: as a directory with `kind: symlink`, plus its target text.

`mode` is `st_mode & 07777` as an integer. `xattrs` lists each extended
attribute as `{name, size, sha256}` of its value, sorted by name. Paths are
relative, `/`-separated, exact UTF-8 bytes, sorted by those bytes.

**Metadata policy.**

- *Ownership* (`uid`, `gid`) is represented: with the mode it decides which
  user can read, run or replace an entry. A copy made under another owner, or
  into a directory whose group new entries inherit, is a different identity;
  examine the identified bundle where it was identified, or identify the copy.
- *Set-user-ID and set-group-ID bits* are refused. The sticky bit is part of
  `mode`.
- *ACLs*: any non-empty extended ACL on the root or an entry is refused. An
  ACL can grant or deny the running user access that the mode does not show.
- *BSD file flags*: any non-zero `st_flags` is refused (for example
  `UF_IMMUTABLE`, `UF_HIDDEN`, `SF_RESTRICTED`, and `UF_COMPRESSED` from
  transparent compression). A bundle copied with compression needs a
  decompressed copy or a revised method.
- *Extended attributes* are refused unless allowlisted. The allowlist is
  `com.apple.provenance` only, represented by name and value digest, never
  omitted. macOS attaches it to files created by a provenance-tracked process
  (every entry and the root of C1 carry it from the offline build); an
  ordinary process cannot remove it (`xattr -d` returns success and the
  attribute remains, observed on macOS 26.6.2), so refusing it would refuse
  every local build. The system uses it to attribute a file's origin, so a
  different value is a different identity. Everything else is refused,
  including `com.apple.quarantine` (it changes Gatekeeper's first-launch
  behaviour; a quarantined candidate belongs to the packaged route, PKG-R1),
  `com.apple.ResourceFork`, `com.apple.FinderInfo` and `com.apple.cs.*`
  (signature data kept outside a file's bytes). Adding a name to the allowlist
  is a method revision.
- *Times* are outside the identity. Access time changes when the bundle is
  read. Modification, change and birth times change whenever the same bytes
  are copied or extracted, and nothing that reads this bundle gives them
  meaning: the host's readers of bundle resources (`lib.rs`,
  `runtime_session.rs`, `hosting_successor.rs`,
  `compiled_development_selection.rs`, `workflow_library.rs`) use no file
  time, and the one time comparison nearby, in `role_supply.rs`, detects
  change during a single read of the person's editable guidance copy; the ad-hoc linker signature covers bytes, not times, and where the
  system's launch registration consults a bundle's modification date it is
  to decide when to re-read `Info.plist`, whose bytes are in the identity.
  Including times would make
  the identity follow handling rather than content. Times are still used to
  detect change while reading (below).
- *Names*: invalid UTF-8, empty names, `.`, `..` and names containing `/`,
  `\`, CR, LF or NUL are refused.
- *Other types*: hard-linked regular files, FIFOs, sockets and devices are
  refused.

**Links.** A link's target text is represented and never followed while
reading. Each link must resolve, following any chain, to an entry inside the
bundle: an absolute or empty target, a `..` that leaves the root, a missing
target, a path through a regular file, or a cycle or chain of more than 32
links is refused. Resolution runs over the inventory itself, so a stored
inventory is checked the same way.

The identity is `chirality.app.bundle-tree.sha256/v2:` followed by the
lowercase SHA-256 of the canonical JSON (sorted keys, separators `,` and `:`,
UTF-8, no trailing newline) of `{"entries", "method", "root"}`. The DEL-01-06
PKG §5.2 regular-file manifest is recorded beside it for comparison; the
manifest alone never identifies the tree.

**Reading.** Opens are descriptor-relative and do not follow links. Each file's
device, inode, size, modification and change times are compared before and
after its bytes are read, and each directory's times before and after it is
listed. Two complete passes must be equal. This detects ordinary change
during reading; it is not custody against a concurrent hostile writer.
Extended attributes and ACLs are read through the macOS C library; other
platforms are refused.

**Validation.** A stored inventory is validated before any identity is
computed: exact field sets per kind, integer modes without set-ID bits,
integer owners, allowlisted and sorted extended attributes, byte-ordered
unique paths whose parents are listed directories, and contained links.
Malformed input is a refusal (exit 2), never an exception.

## Candidate identification record

`candidate-identification.schema.json` defines the record. It binds:

- the commit (full SHA, commit tree and the exported subtree's tree), with every
  tracked file and link under the exported prefix verified byte for byte
  against the revision after the build;
- the build procedure, profile, signing state, features, exact command,
  configuration overlays (path, SHA-256 and content), toolchain versions,
  lockfile digests, offline flag, allowlisted environment, start and finish
  times and, optionally, the timed phases between them;
- the bundle's name, identifier, version, executable and Info.plist digests,
  file manifest, entry counts, observed metadata state (zero ACL entries,
  flags and set-ID bits; each represented extended attribute with its count;
  the owners; the link count) and the complete inventory file with its
  SHA-256;
- the per-user places the bundle identifier selects (Application Support,
  Caches, WebKit, HTTPStorages, Logs, the preferences file and saved
  application state). Each must have no entry of any kind at identification,
  a dangling link included, so the candidate starts with fresh App data;
- that the Codex supplier is not bundled: each examination record binds its own
  pin, distribution identity and configuration (EXP §4.1).

`candidate_key` is the revision's first 10 hex characters, a hyphen and the
build identity's first 12 hex characters (EXP §8.4). The record and inventory
live in the journey owner's `Evidence/EXP/<candidate key>/`.

The tool `app/examination/candidate_identity/identify.py` computes the
inventory and identity (`inventory`), writes a record (`record`) and checks an
existing bundle against a record (`check`). `check` recomputes the stored
inventory's digest and identity, reads the bundle again and compares, and
recomputes the name, identifier, version, executable, Info.plist digest, file
manifest, counts, metadata state and App data directory against the record.
It exits 0 only when all agree, 1 on a difference and 2 on a refusal. It
builds, launches and executes nothing from the bundle. Its regression test is
`app/tests/candidate_identity_test.py`.

## Build route for a development candidate

Follow `app/packaging/unsigned/README.md` (debug, `--no-sign`,
`--features custom-protocol`, `tauri.development.conf.json`) from a `git archive`
export of the exact revision, with the existing offline npm and Cargo caches,
a private target directory and an allowlisted environment without signing or
notarisation variables. Add one overlay that gives the candidate its own
product name and bundle identifier, so its App data places are new. Do not
bundle the supplier for this route.

## Relation to v1

`chirality.app.bundle-tree.sha256/v1` (first head of PR #1411, 9d49d0c3de)
left ownership, file flags, ACLs and extended attributes outside the identity
and did not require links to stay inside the bundle, so behaviour could change
under one identity. It is withdrawn, not redefined: no tool computes it and no
retained record carries a v1 identity.

## Limits

Identity is of the bytes and represented metadata read, not a
reproducible-build claim. It establishes no signing, notarisation, package
record, native witness, qualification, replacement or acceptance. A rebuilt
or changed bundle is a different candidate (EXP §6.2); results stay with the
candidate they name.
