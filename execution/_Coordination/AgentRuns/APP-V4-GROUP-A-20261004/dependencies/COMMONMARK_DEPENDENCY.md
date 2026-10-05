# CommonMark parser dependency packet

Metadata-only preparation by TASK `/root/group_a_execution/workflow_role_production`, parent `/root/group_a_execution`, 2026-10-04; same supplied model6.1/medium, no descendants. Official metadata/HEAD/tagged source reads were authorized for this turn; production remains frozen. No archive bodies, downloads, installation, real-cache/Cargo/shared source mutations, Git/auth/live turns or direct owner prompt.

## Concrete proposed admission

Use `pulldown-cmark = { version = "=0.13.4", default-features = false }`. The official sparse index lists **0.13.4** as the latest non-yanked stable release (published2026-05-20) and declares MSRV **1.71.1**, edition2021. Tagged Cargo.toml agrees. Observed App compiler is Rust1.92.0. This supersedes the arbitrary0.13.0 metadata candidate; no old production pin is changed by this packet.

Defaults `getopts` and `html` are disabled. No `serde`, `simd` or `gen-tests` feature is needed. Official tagged lib.rs unconditionally re-exports Parser/OffsetIter and defines Event, Tag, TagEnd and CodeBlockKind; only the HTML renderer is feature-gated. Tagged parse.rs exposes Parser::new_ext and into_offset_iter without feature gates. `Parser::new` uses Options::empty(); use empty runtime extension options for WD CommonMark carriage. The build script does nothing when gen-tests is absent.

## Exact missing archive request

| File | Official archive URL | HEAD Content-Length bytes | Official registry SHA-256 |
|---|---|---:|---|
| `pulldown-cmark-0.13.4.crate` | https://static.crates.io/crates/pulldown-cmark/pulldown-cmark-0.13.4.crate | 155043 | `e9f068eba8e7071c5f9511831b44f32c740d5adf574e990f946ddb53db2f314e` |
| `unicase-2.9.0.crate` | https://static.crates.io/crates/unicase/unicase-2.9.0.crate | 24368 | `dbc4bc3a9f746d862c45cb89d705aa10f187bb96c76001afab07a0d35ce60142` |

**Total missing compressed bytes:179,411.** Both files are absent from the approved cache. Main archive155,043 bytes; unicase24,368 bytes. Sparse-index checksums are metadata assertions, not a claim to have verified missing archive bodies. After explicit owner yes, download only this exact set, verify both hashes, then ask the manager to admit the exact feature/pin and narrow lock update. This packet is not download permission.

## Minimal closure and locked application comparison

With default features disabled, normal dependencies are bitflags^2, memchr^2.5 and unicase^2.6. The existing application lock/cache already has bitflags2.11.1 and memchr2.8.3; both archive hashes were checked against their lock checksums. unicase2.9.0 is the latest non-yanked stable satisfying version and has no registry dependencies. Its tagged manifest declares edition2018 and no Rust minimum; do not invent a declared MSRV or claim compilation. The existing application feature union/serde_core remains unchanged.

Metadata-only scratch Cargo resolution copied the actual application manifest/lock and existing sparse metadata to an isolated fresh home, added only the parser declaration, and seeded the two official index snapshots there. An unconstrained `cargo generate-lockfile --offline` chose165 added/163 removed/40 modified existing package entries and was **rejected**, not offered for App adoption. Restored the original scratch lock and ran `cargo update --offline -p chirality-app-v4`: **only pulldown-cmark0.13.4 and unicase2.9.0 added; no existing package/version/checksum change; the App root dependency list gains pulldown-cmark**. Both operations were metadata-only and fetched no archives. Original real lock remains SHA256`2fad2d658b3ffaf7b3973d5ab7da693788613f7462eaeca9d4b6b9ad826f7012`; narrow scratch lock SHA256`c1910cffc3fc311fc50cae1117d5aa379dc374142c643c3b22ad85998dbf86b2`. Exact parsed delta and full sources/HEAD headers are in COMMONMARK_DOWNLOAD_SET.json. Do not copy the unconstrained candidate.

## Narrow WD reader replacement feasibility

After admission, keep the immutable original package/source bytes and identity methods unchanged. Exclude only the first front-matter reading span as WDCR3 specifies, then use Parser::new_ext(reading_span,Options::empty()).into_offset_iter(). Event ranges are byte positions in that reading source; add the excluded front-matter byte offset if retaining original-file positions. Root `Start(CodeBlock(Fenced(info)))` with exact trimmed info `workflow-declaration` is the only admitted declaration block; track the complete Start/End container stack so list, blockquote, nested-code and HTML examples remain inactive. Collect code Text events for declaration JSON reading only, not for reminting package/source bytes. CommonMark indentation/tab/line-ending reading rules must never rewrite stored bytes. Keep absent, several-block FB02 and EOF-unclosed behavior. Preserve all17 existing tests/25 independent tab controls and add source-range, mixed container and source-byte controls before fan-in. Actual API compilation and parser behavior remain unverified until the exact archives are authorized and admitted; metadata feasibility is not full WD support, qualification or an actual registration/supply act.

## Retrieval boundaries and evidence

Normal sandbox DNS was unavailable; authorized public reads used escalated curl after review. crates.io version API returned403; official sparse indexes, static archive HEAD and official tagged source manifests/APIs supplied the usable metadata. Archive requests were HEAD only. All plain source reads were official tagged individual files, never source archives. Checksums, features, MSRV, exact byte sizes, source URLs/hashes and isolated resolution delta are retained in the JSON packet. Current hand-parser and all production hashes stay frozen; the parser remains held pending owner archive authorization, manager Cargo admission, replacement tests and independent review.
