# Publisher build-selection implementation

Named technical change `PUBLISHER-BUILD-SELECTION-01`, following merged S4
PR #36 (`3cb060164ec8544bdd7ef700d9e095314d63a7e1`). This implements the
App Agent 0's bounded synthetic/default-None direction; it selects no real
publisher, identifier, version, minimum OS, signing act or release. The
[original S4 clause](INSTALLED_INTEGRITY_S4.md), selected distribution-s1 README
and original identity SHA-256
`d51c1130f5a1356fcc2a6100f1486e8ee3a0728de59f4fe69d4ac6a1580e5290` remain the
supplier/installed-observation basis. Frozen S1/S3 artifacts are unchanged.

## Input and build recipe

The only owner input is a closed UTF-8 JSON object:

```json
{
  "format": "publisher-build-selection.s1",
  "production_bundle_identifier": "invalid.example.synthetic",
  "developer_id_team_identifier": "SYNTHETIC0"
}
```

These are invented fixture values, not a selection. The identifier has at least
two ASCII alphanumeric/hyphen components (1–63 bytes each, alphanumeric at both
ends, total at most 253); the development skeleton identifier is refused. Team
is exactly ten uppercase ASCII alphanumeric characters. Duplicate or unknown
fields, arbitrary requirement logic, quote/backslash/control/Unicode injection
and malformed values refuse. The separately mapped
[publisher-build-selection.s1 schema](publisher-build-selection/publisher-build-selection.s1.schema.json)
documents the closed shape and is identity-bound by `input_schema_sha256`;
the typed parser enforces it at build time. The build does not run a JSON Schema
validator over the input. Schema conformance alone is not authorization.

The build-only controls are:

| Control | Meaning |
|---|---|
| `CHIRALITY_PUBLISHER_SELECTION=production-v1` | Explicit selected production recipe; no other mode is accepted |
| `CHIRALITY_PUBLISHER_INPUT_FILE` | Absolute physical locator of the private regular input file |
| `CHIRALITY_PUBLISHER_INPUT_SHA256` | Lowercase SHA-256 of the exact independently selected input bytes |

Parent `request_secret` file delivery may protect handling after the owner's
choice. It does not make the eventual shipped identifier/team/requirement
secret. No private key, notary credential, account or keychain input is accepted.
The source implementation uses only synthetic input. The private file must be
owned by the build user, have no group/other or special permission bits, be a
single-link regular file no larger than 16 KiB, and have a physical nonsymlink
locator. No-follow open, before/after metadata and exact-byte digest checks
refuse absent, changed, substituted or ambiguous inputs. Error messages omit
input contents and identity values.

`app/src-tauri/build.rs` calls
`build_support/publisher_selection.rs`. It uses the same locked Tauri config
parser and JSON overlay merge as tauri-build for the effective build identifier
and version; the selected identifier must equal that effective identifier.
Build configuration cannot independently select a publisher. Selected builds
require release profile, macOS arm64, the production custom protocol and
`distribution-successor`, with no development mode or synthetic supplier anchor.
A compiler guard in generated selected source independently refuses actual
test binaries, `debug_assertions`, Tauri `dev`, unsupported target or missing/contradictory
features, or absence of the build-script-only `chirality_publisher_selected`
compiler stamp. The stamp is emitted only after a successful explicit selection;
a restored stale Some file cannot compile into an unselected build. Runtime
repeats those guards. No runtime environment/config/file
lookup or IPC constructor is introduced.

Every generator call writes the compiler-facing None output and null/empty
companions BEFORE checking selection. Some is published LAST. Ordinary builds
with no controls remain None; stray controls or an invalid explicit selection
fail the build. Cargo tracks selection-control changes. Selected builds also
emit a never-created recheck sentinel dependency, forcing a re-read/hash on
every Cargo invocation even when input mtimes were restored. An unexpected
sentinel fails and requires a fresh build output directory. OUT_DIR is a
build-owned output, never a runtime input or selected publisher source.

## Independent requirement and binding

The maintained template is
`app/src-tauri/build_support/developer-id-application.s1.requirement-template.txt`.
It independently requires `anchor apple generic`, the exact selected identifier,
Developer ID intermediate OID `1.2.840.113635.100.6.2.6`, Developer ID Application
leaf OID `1.2.840.113635.100.6.1.13`, and exact leaf `subject.OU` team. Constrained
identifiers are quoted/escaped deterministically. No designated requirement,
certificate contents, running signature or arbitrary input logic supplies the
anchor. A synthetic Security.framework requirement-parser test checks syntax
without signing or inspecting any installed identity; it is not proof of a
real certificate, runtime signature or package.

OUT_DIR contains:

- `publisher_selection.rs`: compiler-included optional requirement, original
  binding JSON/digest and public projection JSON/digest.
- `publisher-requirement.txt`: exact deterministic requirement bytes.
- `publisher-build-binding.s1.json`: intact original binding, or `null` when
  unselected. It includes input/requirement/template/generator/recipe/input-schema,
  output-schema, Cargo manifest/lock and build-context SHA-256 identities; exact
  selected identifier/team; target/profile/debug/development/features; package
  name/version; effective App identifier/version and effective config digest.
- `publisher-build-public-projection.s1.json`: separately hashed derivative,
  referencing the original binding digest and omitting identity values/full
  context. It is labelled `redacted-derivative-not-selection-authority`, never
  substituted under an original artifact digest.

The binding is deterministic recursively key-sorted compact JSON. Input SHA
hashes original bytes, not reserialized JSON. Original binding and public
projection have distinct digests. Generated outputs are private-mode files;
"public projection" describes content, not permission to publish it.

The immutable compiled record binds these inputs to the consuming App build.
It does not self-hash the final binary, prove a source commit or authenticate the
build operator. Packaging must independently join actual source revision,
final executable/cdhash, App build/configuration and installer identities to
this compiled binding. The source/recipe/manifest hashes identify precisely
what this binding does cover; they are not a full source-tree attestation.
Supplier build-selection/reference/attestation digests remain separate.

## Runtime and consuming evidence

`src/publisher_selection.rs` has a private-field, non-deserializable compiled
selection type, constructed only from compiler-included constants with no
caller arguments. It checks original/public hashes, closed shapes, recipe
identities, exact template reconstruction and context joins. The original
input file and OUT_DIR companions are never read at runtime. This type supplies
the requirement to the existing installed observer; it is not installed
integrity itself. S4 still requires static and dynamic validation, full supplier
comparison, probe and pre-spawn rechecks before live authority can exist.

`observed-lifecycle-reader.s4.publisher-v1` explicitly names the new compiled
publisher association in reader identity, keeping both original-binding and
public-projection digests. This is a named reader revision, not silent extension
of the old identity. S1/S3 and existing S4 evidence schema bytes remain unchanged.
The configured Store's transport binds that exact reader identity. Value checking
or a matching public projection does not authenticate an observation producer or
construct live authority. Unselected builds reject real installed observations.
A future offline/package reader needs its own explicit trusted matching publisher
selection, exact App/record joins and evidence standing; this PR does not activate
that consumer or authorize live starts from serialized records.

## Verification and owner boundaries

Synthetic tests exercise exact recipe calls in isolated child environments,
Some→None and selected→failure in the same OUT_DIR, missing/changed/private-file
inputs, duplicate/unknown fields and injection, deterministic private/public
bindings, effective configuration mismatch, debug/development/target/feature
refusal, compiler cfg guards, runtime override rejection and requirement syntax.
Existing installed/S4 and production override guards remain selected. PR CI
explicitly runs the publisher generator/recipe/runtime cohorts. Dependencies are
already locked and builds use prepared offline caches, guarded slots, jobs=2
and fresh scratch Codex homes; no native retained candidate is rebuilt or run.

The owner still selects publisher/team and exact production identifier, with
minimum OS/version and final package terms at their own owners. Reported retained
candidate metadata supports 15.0 as an initial minimum option; 11.3 is only the
S4 API floor. Neither is a qualification result here. Actual signing, notarization,
installed/quarantined qualification, FP/S5 and publication remain separate.

Source assurance (2026-10-30, synthetic inputs only): the publisher filter passed
10 tests (nine generator/recipe/compiler/runtime tests plus one existing publisher
regression); installed/S4 filter passed 11. The entire successor module passed
103 tests with four explicit stock/export opt-ins ignored. CI-selection tests
passed 62, all 17 maintained schema mappings passed, and the deliverables checker
reported zero errors. Tests ran offline/locked through guarded slots with fresh
scratch homes. The template parsed successfully through Security.framework
without code signing or any certificate/installed-code inspection. These checks
establish source behavior and representation, not a selected publisher or signed
App capability. Independent review and exact-head hosted CI are recorded in the
follow-on PR before integration.

## Independent review disposition

Claude Opus 5.5/high reviewed `51f61394` against `3cb06016` and found no blockers
within the synthetic/default-None scope. The manager corrected the schema
enforcement claim, removed the unused raw requirement alias, aligned generator
and runtime quoting through the same serde_json string encoder, and added
recipe-level compiler-stamp/configuration-mismatch and synthetic-anchor checks.
No real selection, signing or qualification follows from this review.

Cargo fingerprints retain the build input locator and digest under target/, and
compiled outputs contain the full binding. Treat selected build caches/outputs
according to the original-private evidence policy. The unsalted input/requirement
digests in the public derivative can confirm guessed identifier/team values;
redaction is not secrecy or a publication decision. No selected Cargo freshness
end-to-end run was made: force-rerun behavior relies on Cargo's documented missing
dependency rule and the recipe's checked sentinel/stamp output. The real selected
App execution path remains a later signed-candidate witness.
