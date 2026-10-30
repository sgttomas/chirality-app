# Bounded cached notice/source map — preparation only

2026-10-29. Inventory subject is retained candidate `795362874d-a391547a5c5d`, App source
`795362874dd73a25cf8d9cbf8d7dc0f8fbd38a98`; no candidate, stock supplier or
PR15 evidence was changed. This is a factual input/placement map, not complete
license compliance, legal interpretation or a new universal release blocker.

The complete source/path/version/archive-checksum/file-hash map is retained at
`/private/tmp/chirality-desktop-current-ukt5ir80/bounded-shipped-notice-map.json`,
SHA-256 `8b24f605c853aa90b22655bb022e071923957ad57302187e11c80a07b121a8fd`.
It retains the four component input gaps rather than substituting other
versions. Existing scratch remains in this manager's custody. The new separately
bounded source preparation is durable in
[`app/packaging/notices/index.json`](../../../../app/packaging/notices/index.json),
which retains package/version, archive/lock identity and exact member/hash
provenance without private cache paths. The index does not identify a new App.

## Actually shipped supplier content

All paths below are relative to P1 `Contents/Resources/codex/`; hashes come
from the identified unchanged full vendor tree and its exact archive comparison.

| Component/path | SHA-256 | Exact local license/notice input |
|---|---|---|
| Main `bin/codex` | `112fae7a5a1223e673c8a1791d32338f37df8b527ff1159bb8adac6c4dbf1b4b` | Package-level Apache declaration/README only; exact source LICENSE/NOTICE unavailable |
| `bin/codex-code-mode-host` | `679eedaea70529aa1cffc9bc0a0788c186412663544fa76c09d63b57f383a65a` | No component-specific source/notice association available |
| `codex-path/rg` | `7c7d5b09c3a57de864500c65dc2e9c4d2a5e96a3fc7b7d5318480c19887a739b` | Exact source version/build/license association unavailable |
| `codex-resources/zsh/bin/zsh` | `d715e06edcf1661edb2e7767d65fbd1b44af505edfb217281b701f0a6ae93b15` | Exact source version/build/license association unavailable |

P1 already preserves voice `NOTICE.md` and seven component license texts.
Its `manifest.json` declares build commit
`a956835d020762cb2b570053af06f643a11c0ecc` and binds the main/voice binary
digests; it does not separately establish provenance for code-mode-host/rg/zsh.
For each unresolved row the single next input is the exact source/notice
association matching that row's digest (for main, the declared source commit's
applicable license/notice files). Those branches stop here without acquisition
or guesses; a system-installed rg/zsh license is not a substitute.

The selected npm platform archive also contains `package/package.json` and
`package/README.md` **outside** the vendor subtree, hence outside current P1.
The former declares Apache-2.0 for `@openai/codex@0.160.0-darwin-arm64`;
the latter points to the repository's Apache license. Their exact SHA-256 values
are `2497ae33d4df7cb43618e3935fb1dfbff6a7bf536e2258776d1e95afc3c47017`
and `ba4e1f69ff48386e72a9c5e1edaf76aad64a475c2d51af79ccba6d1128261ba7`.
Neither supplies a complete component notice corpus. The archive has no root
LICENSE/NOTICE text to copy in place of the linked source. No inference about
legal noncompliance follows from that filename/content boundary alone.

## Direct App inputs: available and source-qualified

All 13 direct runtime Cargo packages have exact cached `.crate` archives whose
SHA-256 equals the selected Cargo.lock checksum. Their manifest and 25
license/notice member bytes match the cached source files. This map covers
pulldown-cmark 0.13.4, tauri 2.11.1, tauri-plugin-dialog 2.7.2,
raw-window-handle 0.6.2, serde 1.0.229, serde_json 1.0.151, sha2 0.10.9,
libc 0.2.189, uuid 1.23.1, getrandom 0.4.2, toml 1.1.2+spec-1.1.0,
jsonschema 0.58.5 and rusqlite 0.32.1. Build-only tauri-build 2.6.1 and its
two texts are qualified separately, excluded from this runtime proposal.

The direct JavaScript packages are @tauri-apps/api 2.11.0, react 19.2.7 and
react-dom 19.2.7. Their four license files and manifests match the exact cached
tarballs selected by package-lock integrity/resolved fields. No current version,
generic MIT text or unrelated package is substituted. Root App `LICENSE.md`
also matches the built source; SHA-256
`495c4cd17baafde07be4c358bd47237f259bb2e01914e94114efc97d7fa721da`.

The App manifests/locks were compared byte-for-byte with the built Git revision.
The 29 direct runtime notice artifacts are 132,835 bytes. None appears as a
complete standalone file in the retained bundle inventory; P2/P3 supply no
standalone notice resources. Current resource mappings have no App dependency
notice namespace. The actual frontend build asset also contains none of the
literal markers `@license`, `MIT license`, `LICENSE` or `Copyright`; that
limited observation does not establish what every compressed/compiled binary
section contains. The demonstrated packaging omission is the absence of these
known exact notice artifacts as associated resources, not a legal verdict.

## Separate opt-in source preparation

The new `app/packaging/notices/` source contains the exact App MIT file and 29 direct runtime
license/notice artifacts, with package versions, locked archive identities,
origin member paths and content digests. Preserve all provided alternative
license texts without asserting a new licensing choice. Known text size is
133,902 bytes plus the source index. Keep all existing P1 voice notices and
stock supplier bytes untouched; do not invent texts for the four unresolved
supplier rows or include build/dev-only packages in the runtime claim.

The explicitly selected `app/packaging/unsigned/tauri.notices.conf.json` adds
31 per-file resources (index plus 30 texts) to the ordinary unsigned development
configuration. Default/development/attested routes and all supplier bytes remain
unchanged. The read-only verifier checks the closed index, complete assets,
current direct manifests/locks and overlay; its opt-in archive mode independently
compares locked cached archives, exact tar members and the App Git source.
Focused rejection cases cover wrong/missing/extra assets, scope and overlay
errors. Filesystem staging checks the saved namespace. No prebuilt SDK mapper
runner is available here; real SDK mapping, actual bundling and native
readability are unrun under the no-build boundary. A later build would
be a different candidate with its own identification/content checks; never add
these resources to the retained artifact or rewrite PR15 evidence.

This implements ScopeOfWork OUT-001/REQ-001's bounded content preparation, not
its signed package or native witness. Scope commitments and needs, terms and
owner distribution decisions stay unchanged. The selected new source paths
were disclosed through Agent0 before implementation; no Windows/joined overlap
was identified. Independent provenance/inclusion review precedes readiness.

This 16-package direct-runtime map does not claim transitive completeness,
including the separately bundled SQLite selected through rusqlite. No broad
dependency expansion, supplier execution, network acquisition, native/model
run, registration or supplier contact occurred. Sign-in permission and the
pending terms-evidence amendment remain separate from this packaging finding.
