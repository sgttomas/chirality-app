# Exact 0.160.0 notice/source association investigation

2026-10-31, bounded local read-only investigation. This extends the historical
CACHED_SHIPPED_NOTICE_INPUTS account without changing its subject or treating
source strings as legal/qualification evidence. The adjacent observations.json
binds all four exact binaries, byte sizes, embedded string bytes/offsets and the
voice manifest. The maintained `app/packaging/supplier_notices/observe.py`
rechecks those hashes before and after observation, executes no binary and reads
no credential/account data. The official platform archive's previously retained
identity is fc789bcd…b57466; its acquisition account remains separate.

## What the available bytes establish

- **Main Codex:** the voice manifest explicitly lists main hash
  `112fae7a…4b1b4b` and declares build commit
  `a956835d020762cb2b570053af06f643a11c0ecc`. This gives a precise source-commit
  locator for the main component rather than a moving version/tag. The package
  metadata identifies `https://github.com/openai/codex.git`, directory codex-cli,
  and declares Apache-2.0. It does not contain root LICENSE/NOTICE texts.
- **Code-mode host:** exact hash `679eedae…3a65a` contains
  `code-mode-host/src/main.rs` and the same Codex CI workspace path prefix as
  main. These are build-source-location clues. The manifest does not list this
  binary or bind it independently to the declared build commit. A shared path
  prefix is not proof that both executables came from identical source.
- **rg:** exact hash `7c7d5b09…39739b` has NUL-delimited `16.0.0` at offset
  3,660,432 and `10.46 2025-08-27` immediately afterward at offset 3,660,439.
  The executable also embeds ripgrep help/repository references. This narrows
  the investigation to a likely ripgrep 16.0.0 / PCRE2 10.46 composition, but does
  not establish the upstream archive, build recipe, downstream patches or notices.
- **zsh:** exact hash `d715e06e…b15` embeds
  `zsh-5.9.0.3-test-87-g77045ef` and install paths for `5.9.0.3-test`. This
  identifies a concrete describe-style build string; a generic zsh 5.9 LICENSE
  cannot establish the exact fork/revision or patch set for this binary.

## Local source inputs checked and deliberately not substituted

The complete retained platform package contains its package.json/README and
vendor metadata plus voice notices/licenses. It does not include source or
component-specific notices for these four binaries. The prepared App Cargo
registry has no codex, ripgrep or zsh crate/source entry. The available Homebrew
ripgrep cache is **15.2.0**, not the binary's observed 16.0.0 string. The selected
local Chirality Git object database has no object at the main's declared Codex
commit; that is a check of this database, not a claim about every disk/object.
The runtime-plugin cache contains unrelated dependency notices, not an identified
0.160.0 source closure, and was not treated as an alternative authority.

A retained earlier supplier-packaging scratch contains an Apache LICENSE of
10,926 bytes (SHA d17f227e4df5da1600391338865ce0f3055211760a36688f816941d58232d8dc)
and Codex NOTICE of 242 bytes (SHA
9d71575ecfd9a843fc1677b0efb08053c6ba9fd686a0de1a6f5382fd3c220915), alongside
an Intel binary/archive. No matching 0.160.0 source-revision association was
found in its available account. Those texts are **not** copied into the new
bundle or promoted to matching this Apple Silicon subject merely because their
names/license family look suitable. Likewise no 0.154 notice reuse is made.

## Exact remaining inputs and next remedies

1. **Main:** obtain root LICENSE and NOTICE (if present) at the declared Codex
   commit, plus its release/package notice assembly definition. Candidate source
   locators are `https://raw.githubusercontent.com/openai/codex/a956835d020762cb2b570053af06f643a11c0ecc/LICENSE`
   and the same prefix plus `NOTICE`. These URLs are derived from retained
   package repository+commit metadata, not fetched/verified publications. Exact
   remote sizes/existence are unknown locally; the unrelated cached text sizes
   above must not be advertised as their download sizes. Next remedy is narrowly
   scoped metadata/source retrieval for these exact files once file/size authority
   is established, or receipt of an existing exact-commit source copy.
2. **Code-mode host:** the same commit's `codex-rs/code-mode-host/Cargo.toml`,
   applicable source-root LICENSE/NOTICE and the release recipe identifying the
   packaged code-mode-host bytes. Needed association is explicitly
   `679eedae…3a65a` → source revision/build inputs → applicable notices. Merely
   retrieving the main license would not establish this separate edge.
3. **rg:** the Codex 0.160.0 supplier packaging recipe/lock/checksum which selects
   the rg release input, and that input's notice/source inventory (including
   PCRE2 where actually linked). Match the retained `7c7d5b09…39739b` binary or
   an evidenced packaging transformation. The observed version string is a search
   lead, not authority to download an arbitrary v16.0.0 release or declare its
   license applicable. Exact file locator/size remains an upstream-recipe input.
4. **zsh:** the supplier's zsh fork/repository, full commit resolving
   `77045ef`, patch/build recipe and applicable LICENSE/notice files, bound to
   `d715e06e…b15`. The describe string is more precise than a generic version
   but does not disambiguate repositories. Exact file locator/size cannot be
   truthfully supplied until that build-source association is obtained.

Packaging owns tracing and assembling these inputs, rather than requesting an
owner legal conclusion or adding a generic supplier-inquiry gate. No external
message is sent; no network acquisition occurred in this inspection. A requested
acquisition must name the actual file/source/size and purpose, and should target
only these unresolved edges. Current conclusion: useful exact version/source
locators are narrowed; **none of the four full notice/source associations is yet
closed**. SQLite and direct-App notices are separate completed source-preparation
inputs. No complete transitive coverage, redistribution approval, qualification
or release follows from any of these observations.
