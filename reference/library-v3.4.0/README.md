# Library 3.4.0 contributor selection

App selects `library-v3.4.0` at
`1bba3d170e7a25bc2a04e0a4dfe77b624ea440ca`, replacing 3.3.0 for new contributor
reliance. DEL-10-01 owns the adoption.

The published `chirality-library-3.4.0-source.tar` is 9,820,160 bytes, with
SHA-256 `b4f0ec20b5e9a26125a16002e95895e5171ebeb6d4e44664e400f18dfe9eb7b5`,
and holds 779 files. The tag resolves to the selected commit. The archive on
the shared development host has that digest; no release asset was downloaded
for this selection. It is extracted at
`~/dev/chirality-library-releases/library-v3.4.0` on that host. Run the
release's tools from there with Python's `-B` flag, so that no bytecode cache
is written into the folder and it stays equal to the archive.

On another machine, an explicitly selected checkout at the selected commit or
the verified release archive supplies the same source. Verify the tag and
commit first; a path alone is not a source selection. To prepare a separate
export from a checkout without changing it:

```sh
CHIRALITY_LIBRARY=$(mktemp -d /tmp/app-library-source.XXXXXX)
git -C <checkout> archive 1bba3d170e7a25bc2a04e0a4dfe77b624ea440ca | tar -xf - -C "$CHIRALITY_LIBRARY"
```

`MANIFEST.json` is a small contributor and test delta, not a Library
distribution. It lists each released input the App's checks read, with its Git
blob, digest and where the App retains it. Six inputs changed in this edition
and are retained here: the HELP_HUMAN and INTERLOCUTOR role files, the
comparison workflow, the project-entry template, the workflow catalog and the
metadata guide. Inputs whose released bytes did not change keep the retained
copy they had: the other three role files in `reference/library-v3.3.0/`, and
the registry, the licence and the three readers in `reference/library-v3.0.0/`.
The document metadata schema is unchanged and is retained here as well, so
that the check that reads it has it beside the manifest. Tests export the
selected inputs into scratch without a sibling checkout or network dependency.

The earlier folders stay, and none is the current selection.
`reference/library-v3.3.0/` and `library-v3.0.0/` hold inputs this manifest
still points to. All four, with `library-v3.1.0/` and `library-v2.1.0/`,
record the selection made at their edition and are read by the tests of those
editions.

The tests check that each retained file equals what the manifest records and
that the selected roles and the comparison workflow resolve from an export
built from the retained files. They do not establish that the manifest's
digests are the release's: that was established once, by comparing each row
with the extracted release, when this folder was made.

The entry documents' `metadata.upstream` names this edition: `AGENTS.md` and
`init-prompt.md` were compared with this edition's project-entry template and
reconciled. Packaged instruction resources under
`app/src-tauri/resources/instructions/` keep their own source identities and
are not changed by this selection. The App's bundled workflows under
`app/src-tauri/resources/production_workflows/` are every workflow of this
edition, generated from the archive above by `tools/library_workflows`, which
takes the archive's size and digest from `MANIFEST.json` here.
