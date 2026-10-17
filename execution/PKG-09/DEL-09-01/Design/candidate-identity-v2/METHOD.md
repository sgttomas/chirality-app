# Development App candidate identity — candidate-identity-v2

Owner: DEL-09-01 (EXP §4.1 candidate subject; §8.4 candidate key). Consumer:
DEL-09-02 (SQ I-13, the integration owner names the candidate). This method
supplies the `app_candidate` values an EXP record cites for an unpackaged
`native_development` build. DEL-01-06 retains its package identity and witness.
Identification opens no examination and selects no qualification candidate.

## Bundle tree identity: `chirality.app.bundle-tree.sha256/v2`

The measured root is the built `.app` directory. Its location, name and times
are excluded under the operating constraint below. The root and descendants
represent these values:

- root: `mode`, `uid`, `gid`, `xattrs`;
- directory: `path`, `kind: dir`, `mode`, `uid`, `gid`, `xattrs`;
- regular file: the directory fields with `kind: file`, plus `size` and the
  SHA-256 of its exact bytes;
- symbolic link: the directory fields with `kind: symlink`, plus exact `target`
  text. Its metadata belongs to the link, not its referent.

`mode` is `st_mode & 07777` as an integer. `xattrs` is a name-sorted list of
`{name, size, sha256}` of attribute values. Paths are relative, `/`-separated
UTF-8, ordered by their exact UTF-8 bytes. The inventory contains no absolute
filesystem location or user name.

**Metadata policy.**

- Ownership (`uid`, `gid`) is represented for the root and every kind of
  entry. A copy under different ownership is a different identity. The
  examining account, its group memberships and surrounding filesystem access
  remain examination configuration, not facts established by this digest.
- Set-user-ID and set-group-ID bits are refused on every entry and the root.
  The sticky bit is represented in `mode`.
- Any nonempty macOS extended ACL is refused on the root or any entry,
  including a link. ACLs can grant or deny access independently of mode.
  The reader uses `acl_get_fd_np` or `acl_get_link_np`, not a parsed listing.
  Darwin's `ENOENT` for an absent extended ACL is accepted; other read errors
  refuse. A returned ACL is validated before its first entry is queried.
- Any nonzero BSD `st_flags` is refused, including hidden, immutable,
  restricted and compressed states. A compressed copy needs a copy with that
  flag cleared and its content reidentified, or a revised method.
- The only allowlisted extended attribute is `com.apple.provenance`. Its
  name, length and value digest are represented, including on links and the
  root. macOS can attach this attribute to a local build; its presence is not
  grounds for ignoring it. The reader observes the value actually returned
  by macOS, even if an attempted write or removal reports success without
  changing it. All other xattrs refuse, including quarantine, resource forks,
  FinderInfo and `com.apple.cs.*` signature attributes. Resource-fork content
  is therefore never silently outside the identity. An allowlist change
  requires revising the method.
- Hard-linked regular files or symlinks, FIFOs, sockets, devices and other
  types refuse.
- Names refuse invalid UTF-8, empty components, `.`, `..`, `/`, backslash,
  CR, LF and NUL. Link target text also refuses invalid UTF-8, backslash,
  CR, LF and NUL; its `/`, `.` and `..` components undergo containment checks.

**Operating constraint for excluded location and times.** Access, modification,
change and birth times are outside the identity; reading can change access
time, and copying or extraction can change the other times without changing
represented content. This is a content and metadata identity, not a claim
that timestamps or location can never affect macOS or App observations.
Use the identified copy in a controlled location. Between the pre-run recheck
and the examination, do not relocate it or alter its metadata. The examination
must not rely on file dates, timestamp-based resource selection or cached
LaunchServices registration to establish which bundle runs: select the
identified bundle's executable directly and bind its location and actual
OS/account/launch configuration in the examination record. A scenario that
observes excluded times, location, launch registration or other external
state must bind that state separately; this digest alone is insufficient for
that comparison. Reidentifying a copy does not prove such state equivalent.
The tool neither resets timestamps nor clears system caches. The bundle name
is separately checked in the record, despite being outside the tree digest.

**Links.** Targets are represented without following links during content
reads. Resolution over the inventory follows directory and file link chains,
refusing any absolute or empty target, intermediate or final escape above the
bundle root, missing target, file traversal (including `file/`, `file/.` and
`file/..`), cycle or chain exceeding 32 links. A link to the bundle root is
contained. The same checks apply to stored inventories.

The identity is `chirality.app.bundle-tree.sha256/v2:` followed by lowercase
SHA-256 of canonical JSON of `{"entries": ..., "method": ..., "root": ...}`:
sorted keys, separators `,` and `:`, UTF-8, no trailing newline. The DEL-01-06
PKG §5.2 regular-file manifest is separately recorded: SHA-256 of byte-ordered
`<file sha256>  <relative path>\n` lines, with the last newline included.
The manifest alone does not identify the tree.

**Reading.** macOS is required for live identification and checking, so flags,
ACLs and xattrs cannot silently disappear on another platform. Portable stored
inventory validation, containment and manifest tests remain useful there.
Every ancestor is opened relative to its held parent with no-follow directory
opens; a symlink root or ancestor refuses. Ancestor bindings are checked after
traversal. Regular files are opened no-follow and nonblocking. File reads
bracket bytes with stat, ACL and xattr observations. Directory walks bracket
listing and descendants with those observations too. Stat comparisons include
device, inode, type/mode, owner, link count, size, modification/change times
and flags, excluding access time. Symlink ACL/xattr reads use macOS no-follow
path APIs, bracketed by leaf stats, with parent/root binding checks; link text
is read relative to its held parent. Two complete inventories must agree.
The Info.plist re-read uses no-follow descriptors and must reproduce its
inventoried bytes and metadata. These checks detect ordinary concurrent
changes; they do not establish custody against a hostile writer that changes
and restores state between observations, or prevent changes after reading.

**Validation.** Before computing an identity, the stored inventory must have
exact field sets, known kinds, integer modes/owners/sizes (booleans refused),
allowed sorted unique xattrs, SHA-256 values, byte-ordered unique paths with
listed directory parents, and contained links. Malformed shapes refuse with
exit 2. Plist identity fields must have the expected text types; the identifier
must be a dotted ASCII identifier suitable for an App-data path, and the
executable must be one filename naming an inventoried regular file under
`Contents/MacOS`.

## Candidate identification record

`candidate-identification.schema.json` defines the record. It binds:

- Full commit SHA, commit tree and exported subtree tree; tracked files and
  Git mode-120000 links under the prefix are verified against their blobs.
  Exported type, link text, regular-file bytes and Git executable status must
  match; export traversal refuses link ancestors.
- Declared build procedure, profile, signing state, features, command,
  configuration overlays, toolchain, lockfiles, offline flag, allowlisted
  environment and build times, with optional phases. These are supplied build
  facts, not observations reconstructed or attested by this tool.
- Bundle name, identifier, version, executable and Info.plist digests,
  regular-file manifest, kind counts, metadata summary and inventory digest.
  Refused metadata summary values are zero by construction; represented
  owners and xattr counts are derived from the complete inventory.
- Historical absence at identification of three per-user identifier-selected
  locations: `~/Library/Application Support/<id>` (Tauri App data),
  `~/Library/WebKit/<id>` (persistent WebKit data), and
  `~/Library/Caches/<id>` (identifier-selected cache). Every one must lack an
  entry of any kind, including a dangling symlink. A non-directory or link in
  their ancestry refuses rather than making absence ambiguous. The ordered
  checked-location declaration must match these exact paths and identifier.
  These are the scope of the freshness check, not a census of external state:
  HTTPStorages, Logs, Preferences and Saved Application State are not claimed
  fresh by this method. A journey relying on additional state must control
  and bind it separately. Historical absence is no promise after launch.
- The supplier-not-bundled declaration; each examination binds its actual
  supplier pin, distribution identity and configuration (EXP §4.1).

`candidate_key` is the revision's first 10 hex characters, a hyphen and the
build digest's first 12 hex characters (EXP §8.4). The record and inventory
belong in the journey owner's `Evidence/EXP/<candidate key>/`.

`app/examination/candidate_identity/identify.py` computes `inventory`, writes
`record`, or performs read-only `check`. `check` validates the record and
stored inventory, recomputes their digest/identity, reads the live bundle and
compares it. For an equal tree it independently derives every bundle field
listed above and verifies the App-data directory and all checked-location
declarations. It does not reassert historical freshness by requiring current
App data to be absent. Exit 0 means agreement, 1 a difference, 2 refusal. It
builds, launches and executes nothing from the bundle. The regression entry
is `app/tests/candidate_identity_test.py`, using the prepared local Python
`jsonschema` environment without supplier invocation or downloads.

## Development build route and v1 boundary

Follow `app/packaging/unsigned/README.md` from an exact-revision `git archive`
export, with prepared offline caches, a private target directory and the
allowlisted environment. The development route uses debug, `--no-sign`,
`--features custom-protocol` and `tauri.development.conf.json`, plus a product
name and identifier overlay selecting new App-data paths. Do not bundle the
supplier for this route.

`chirality.app.bundle-tree.sha256/v1` omitted ownership, flags, ACLs and xattrs
and did not contain links. It is not redefined by these repairs: the tool
computes only v2. A historical v1 record is not a v2 identification and needs
reidentification before it can be cited as v2.

Identity establishes no reproducible build, signature verification,
notarisation, package witness, native observation, qualification, replacement
or acceptance. Changed candidates keep their own results and affected checks
reopen under EXP §6.2.
