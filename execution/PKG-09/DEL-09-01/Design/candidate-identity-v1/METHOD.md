# Development App candidate identity — candidate-identity-v1

Owner: DEL-09-01 (EXP §4.1 candidate subject; §8.4 candidate key). Consumer:
DEL-09-02 (SQ I-13, the integration owner names the candidate). It supplies
the `app_candidate` values an EXP result record cites for an unpackaged
`native_development` build. A DEL-01-06 package keeps its own package identity
record; this method neither replaces it nor makes a development build a package.

## Bundle tree identity: `chirality.app.bundle-tree.sha256/v1`

The measured root is the built `.app` directory. Its location is not part of
the identity; the root's permission bits are. Every descendant is an entry:

- directory: path, `kind: dir`, `mode`;
- regular file: path, `kind: file`, `mode`, `size`, SHA-256 of its exact bytes;
- symbolic link: path, `kind: symlink`, `mode`, its target text (never followed).

`mode` is `st_mode & 07777` as an integer. Paths are relative, `/`-separated,
exact UTF-8 bytes, sorted by those bytes. Other file types, hard-linked regular
files, invalid UTF-8 and names containing `/`, `\`, CR, LF or NUL are refused,
not omitted. Ownership, timestamps, extended attributes (including quarantine
and provenance) and ACLs are outside the identity; signatures embedded in files
are covered by their bytes.

The identity is `chirality.app.bundle-tree.sha256/v1:` followed by the
lowercase SHA-256 of the canonical JSON (sorted keys, separators `,` and `:`,
UTF-8, no trailing newline) of `{"entries", "method", "root_mode"}`. The DEL-01-06
PKG §5.2 regular-file manifest is recorded beside it for comparison; the manifest
alone never identifies the tree. Reading uses descriptor-relative no-follow
opens with before/after checks, and two complete passes must be equal. This
detects ordinary change during reading; it is not custody against a concurrent
hostile writer.

## Candidate identification record

`candidate-identification.schema.json` defines the record. It binds:

- the commit (full SHA, commit tree and the exported subtree's tree), with every
  tracked file under the exported prefix verified byte for byte against the
  revision after the build;
- the build procedure, profile, signing state, features, exact command,
  configuration overlays (path, SHA-256 and content), toolchain versions,
  lockfile digests, offline flag, allowlisted environment and times;
- the bundle's identifier, version, executable and Info.plist digests, file
  manifest, entry counts and the complete inventory file with its SHA-256;
- the App data directory the bundle identifier selects, which must be absent
  at identification so the candidate starts with a fresh App data directory;
- that the Codex supplier is not bundled: each examination record binds its own
  pin, distribution identity and configuration (EXP §4.1).

`candidate_key` is the revision's first 10 hex characters, a hyphen and the
build identity's first 12 hex characters (EXP §8.4). The record and inventory
live in the journey owner's `Evidence/EXP/<candidate key>/`.

The tool `app/examination/candidate_identity/identify.py` computes the
inventory and identity (`inventory`), writes a record (`record`) and recomputes
an existing bundle against a record (`check`, exit 0 only on equality). It
builds, launches and executes nothing from the bundle. Its regression test is
`app/tests/candidate_identity_test.py`.

## Build route for a development candidate

Follow `app/packaging/unsigned/README.md` (debug, `--no-sign`,
`--features custom-protocol`, `tauri.development.conf.json`) from a `git archive`
export of the exact revision, with the existing offline npm and Cargo caches,
a private target directory and an allowlisted environment without signing or
notarisation variables. Add one overlay that gives the candidate its own
product name and bundle identifier, so its App data directory is new. Do not
bundle the supplier for this route.

## Limits

Identity is of the bytes read, not a reproducible-build claim. It establishes
no signing, notarisation, package record, native witness, qualification,
replacement or acceptance. A rebuilt or changed bundle is a different candidate
(EXP §6.2); results stay with the candidate they name.
