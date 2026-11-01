# Minimal pinned source retrieval proposal

Public unauthenticated metadata inspection only; no source/archive body fetched.
Exact Codex commit `a956835d020762cb2b570053af06f643a11c0ecc` resolves through
Git commit metadata to tree `c09968bc06fc543c9d8bd9ffbaaa72829b31f5d9`.
The complete non-truncated tree metadata reports each file's size and Git blob
identity. Exact metadata receipts, retrieval dates and hashes remain in the
adjacent `public-metadata.json` account; full responses are retained in its
scratch custody paths.

## Resolved locally without retrieval

The previously unassociated cached root LICENSE and NOTICE exactly match this
commit's Git blob IDs and sizes: LICENSE 10,926 bytes,
`4606e72e042564097e8780d66c1d4dcb611869bd`; NOTICE 242 bytes,
`2805899d56d0332d175cfc613c67d45d6f006db7`. They are preserved under
`app/packaging/supplier_notices/codex-0.160.0/` with their SHA-256 identities in
the metadata account. This closes exact root-text availability/correspondence
at the main manifest's declared commit, not full component/dependency notice
coverage or licensing applicability. No download of these two files is needed.

## Owner retrieval decision: ten text files, 128,666 bytes total

All URLs below name that exact commit, not a branch or moving release tag.
Verify the metadata-selected Git blob hash after any authorised retrieval;
text must be treated as source evidence, never executed. This request excludes
all binary archives, source tarballs, dependency downloads and linked follow-ups.
The purpose is to trace the remaining exact binary/build/notice associations.

| Pinned file URL | Bytes | Purpose |
|---|---:|---|
| [codex-rs/code-mode-host/Cargo.toml](https://raw.githubusercontent.com/openai/codex/a956835d020762cb2b570053af06f643a11c0ecc/codex-rs/code-mode-host/Cargo.toml) | 1,340 | Identify host package license inheritance and build target; not alone a binary association. |
| [codex-rs/Cargo.toml](https://raw.githubusercontent.com/openai/codex/a956835d020762cb2b570053af06f643a11c0ecc/codex-rs/Cargo.toml) | 20,615 | Resolve workspace license/source declarations used by host. |
| [.github/workflows/rust-release.yml](https://raw.githubusercontent.com/openai/codex/a956835d020762cb2b570053af06f643a11c0ecc/.github/workflows/rust-release.yml) | 82,797 | Trace exact release compilation/signing/assembly and input identities for retained host and packaged tools. |
| [scripts/codex_package/cargo.py](https://raw.githubusercontent.com/openai/codex/a956835d020762cb2b570053af06f643a11c0ecc/scripts/codex_package/cargo.py) | 5,872 | Trace which built host/main executables the package assembly selects. |
| [scripts/codex_package/layout.py](https://raw.githubusercontent.com/openai/codex/a956835d020762cb2b570053af06f643a11c0ecc/scripts/codex_package/layout.py) | 5,761 | Trace mapping into the platform vendor tree and preserved source inputs. |
| [scripts/codex_package/rg](https://raw.githubusercontent.com/openai/codex/a956835d020762cb2b570053af06f643a11c0ecc/scripts/codex_package/rg) | 2,592 | Read pinned rg input locator/digest metadata, without downloading that artifact. |
| [scripts/codex_package/codex-zsh](https://raw.githubusercontent.com/openai/codex/a956835d020762cb2b570053af06f643a11c0ecc/scripts/codex_package/codex-zsh) | 1,676 | Read pinned zsh input locator/digest metadata. |
| [.github/dotslash-zsh-config.json](https://raw.githubusercontent.com/openai/codex/a956835d020762cb2b570053af06f643a11c0ecc/.github/dotslash-zsh-config.json) | 856 | Identify zsh recipe bootstrap input, distinct from binary provenance. |
| [.github/workflows/rust-release-zsh.yml](https://raw.githubusercontent.com/openai/codex/a956835d020762cb2b570053af06f643a11c0ecc/.github/workflows/rust-release-zsh.yml) | 5,528 | Resolve exact zsh source/fork/build revision and artifact recipe. |
| [.github/scripts/build-zsh-release-artifact.sh](https://raw.githubusercontent.com/openai/codex/a956835d020762cb2b570053af06f643a11c0ecc/.github/scripts/build-zsh-release-artifact.sh) | 1,629 | Identify patch/build source and notice handling for zsh artifact. |

This is a concrete retrieval proposal, not permission already granted. Inspect
these exact small files first; only then identify any genuinely necessary next
file by its actual locator/size. Do not pre-authorise arbitrary sources referred
to by their content.

## Binary associations still unestablished

The public `rust-v0.160.0` release metadata targets the same commit and lists
code-mode-host arm64 archives. For example, the gzip archive is 23,825,926 bytes
with digest `dc70fbc76e9dcae5ae3d5424808c8e7c2df5e0db4ac827ddd4fbe339015aad75`.
Its digest is for the compressed archive, not the retained host binary
`679eedae…3a65a`. It is **not** in this retrieval request. The release metadata
reports `immutable: false`; preserve exact asset digest/ID observations rather
than equating a tag URL with immutable binary contents.

The likely rg version string led to a metadata-only query for
`BurntSushi/ripgrep` release tag `16.0.0`, which returned HTTP404. The zsh short
hash led to a query for `zsh-users/zsh` commit `77045ef`, also HTTP404. These
negative results disprove neither file existence elsewhere nor the possibility
of a supplier fork; they do not establish either repository as the correct
build source. The pinned supplier input descriptors/recipes above are the next
concrete route to the actual upstream locators and checksum transformations.

For main, retain its manifest byte→commit declaration and exact root texts,
then inspect assembly/license coverage before closing the whole association.
For host, establish package recipe/build→retained host hash. For rg and zsh,
resolve the supplier-selected release/fork/build inputs and applicable notices.
No all-component legal conclusion, complete transitive coverage, supplier
qualification or public release follows from metadata or content correspondence.
