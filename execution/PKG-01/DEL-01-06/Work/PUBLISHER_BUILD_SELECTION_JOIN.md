# Publisher build-selection receiving join

`PUBLISHER-BUILD-SELECTION-01` supplies the runtime owner's
[publisher build interface](../../DEL-01-01/Work/PUBLISHER_BUILD_SELECTION.md),
not a publisher selection or signing act. It follows merged S4 PR #36 and keeps
its selected original supplier source, Option B and qualification limits.
`PUBLISHER_SELECTION_OWNER_ACTION_DRAFT.md` remains packaging/owner decision
preparation; this file does not choose its real values.

Owner input field names are exactly `format: publisher-build-selection.s1`,
`production_bundle_identifier`, and `developer_id_team_identifier`. There is no
requirement-text, key, certificate or notary credential field. The parent can
request those two values once after the owner chooses the route. Secure file
handling protects handling, not eventual secrecy in the shipped signature or
compiled requirement. The build additionally needs the exact input-byte SHA-256,
physical private-file locator and explicit `production-v1` mode; see the owning
interface for build-only variable names and refusal rules.

Consumer files for later adoption are:

- `app/src-tauri/schemas/publisher-build-selection.s1.schema.json`
- `app/src-tauri/schemas/publisher-build-binding.s1.schema.json`
- `app/src-tauri/schemas/publisher-build-public-projection.s1.schema.json`
- `app/src-tauri/build_support/developer-id-application.s1.requirement-template.txt`
- `app/src-tauri/build_support/publisher_selection.rs` and `build.rs`
- `app/src-tauri/src/publisher_selection.rs` and named reader
  `observed-lifecycle-reader.s4.publisher-v1`.

The Work source schemas are maintained separately under DEL-01-01
`Work/publisher-build-selection/` with exact schema-copy mapping. None are a
rewrite or repin of frozen supplier S1/S3 inputs.

The generated original binding identifies input, requirement, template,
generator, build recipe, all publisher schemas, Cargo manifest/lock, effective
Tauri configuration and build context by SHA-256. It also carries exact selected
identifier/team. The App compiles the original binding and its digest together
with the requirement. A separate public projection references the original
binding digest and has its own compiled digest; it omits identity values and is
explicitly not selection authority. Preserve the original bytes privately where
needed. A redacted derivative is never supplied as if it were the original under
the original digest, and neither record self-hashes its own bytes.

Packaging must join the compiled original-binding digest (and any separately
published projection digest) to the actual source revision, final App executable/
cdhash, build/version/effective identifier, configuration and package identities.
The input identifier must match the effective Tauri production configuration or
the build refuses. Bind the pkg-identity logical record ID, exact package envelope,
pre-notarization installer digest and separate post-staple/install subject.
The compiler-included binding is not a final executable hash or full source-tree
attestation. The existing supplier S2/S3 selection remains a separate required
join. Default builds still compile None and cannot qualify production custody.

Offline/PKG/EXP/SQ readers need their own explicit matching trusted publisher
selection and candidate-bound adoption; this implementation activates none of
those consumers. Serialized records and public projections cannot construct
live start authority. FP-0/1, signing/notary/installation, FP-2/W-4, S5,
minimum-OS support, terms and publication decisions retain their separate actual
evidence/owner conditions. No retained native candidate/state is touched.
