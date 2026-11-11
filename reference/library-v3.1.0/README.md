# Library 3.1.0 contributor selection

App pins `library-v3.1.0` at `88ab3f4f5f8ec7f7e030279164dbd1a4aa38b514`.
Read the selected shared checkout only after verifying that revision.
DEL-10-01 owns the local adoption.

The [release notes](https://github.com/sgttomas/chirality-library/releases/tag/library-v3.1.0)
identify a 9,984,000-byte source archive with reported SHA-256
`6553f7cc735740233f236bc773a3a43c03163d4351a6575d320694fb271d91ad`.
No archive was downloaded; the digest is published metadata. The local clean
checkout HEAD and tag resolved to the selected commit.

`MANIFEST.json` is a small edition delta, not a full Library distribution. It
binds ten role/registry/reader inputs at 3.1.0 by Git blob/mode, length and hash.
Only HELP_HUMAN and INTERLOCUTOR changed; their exact new blobs are in `source/`.
The eight unchanged inputs reuse the retained 3.0.0 fixture through explicit
repository-relative `retainedPath` values. The unchanged document-metadata
schema likewise retains its 3.0.0 location and has a separate manifest binding.
All eleven source identities were compared with the selected 3.1.0 Git objects.

The existing App v3 receiving harness exports these inputs into an isolated
folder and checks the current roles with the released validator and resolver.
App CI reads only repository-local inputs. Earlier fixtures and their results
keep their original editions; the nineteen App headers still use the same
schema. Product Work sources and packaged instructions remain basis89ac/four
roles. Future product adoption follows its own source-selection process.
