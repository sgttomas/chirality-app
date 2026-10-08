# Static distribution support

This separate opt-in command reads selected S1 inputs and actual supplier trees.
It never stages, signs, launches, probes, writes runtime state, or grants supplier
trust. Existing `inventory` and `prepare` commands and their source guards are
unchanged and remain standard-library-only.

Use the existing Python `jsonschema` dependency and an explicitly selected,
reviewed build of the Rust `distribution-static` example. Nothing is downloaded
or built automatically. The scanner must support `scan ABSOLUTE_TREE` and
`compare EXPECTED_JSON ACTUAL_JSON` with the complete Inventory JSON contract.

```
python3 app/packaging/prepare.py static-distribution \
  --request /absolute/physical/inputs/request.json \
  --scanner /absolute/physical/distribution-static \
  --published-tree /absolute/physical/published \
  --packaged-tree /absolute/physical/packaged
```

At least one tree is required; an omitted side remains explicitly unmeasured.
Use physical absolute paths (no links). Output is one JSON support report on
stdout: exit 0 for consistent or explicitly incomplete support reports, 1 for
mismatch, 2 for refusal. Exit 0 is
never qualification, release registration, or runtime verification.

## Exact input contract

The request is a closed JSON object with `format: "static-distribution-input/1"`:

- `build_selection`: digest-bound `build-selection.s2` with exact `method`,
  `schema_ids`, `expected` and `attestation` fields from the existing S2 format.
- `s1_package`: selected `pkg-identity.s1`; `verification_artifact` must be null.
- `legacy_package`: separately selected exact `PKG-v0.2` package bytes, whose
  value and identity must equal the S1 envelope's embedded legacy package.
- `terms`: the separate selected `PKG-v0.2` terms record (schema plus PK-R4).
- `candidate`: a closed object with `app_revision`, `build_identity`,
  `package_record_id` and `installer_sha256_before_notarisation`.
- `installer`: actual selected installer bytes, checked against the candidate
  and legacy PKG digest. No App-binary content binding is invented: legacy PKG
  has no App-binary digest.
- `scanner`: `{ "sha256": "<exact executable digest>",
  "declared_source_revision": "<operator's source claim>" }`.

Every artifact field is `{ "path": "contained/relative/name", "sha256":
"<64 lowercase hex>" }`, relative to the request's directory. No absolute or
escaping artifact path is accepted. Exact bytes are hashed before parsing.
Duplicate keys, unknown typed versions, links, hard links and special files
refuse. Typed JSON/source files are bounded at 32 MiB; streamed scanner,
installer and opaque evidence files at 512 MiB each; total frozen inputs at
1 GiB. Exceeding a limit refuses explicitly, never truncates.

Only schema-owned reference edges are followed. Expected-reference acquisition,
label/generation evidence and attestation review/adoption evidence are opaque
bytes, even if they happen to contain JSON with path/hash pairs. Such incidental
content is never opened or interpreted as another dependency.

## Claims and limits

The new private `sources.json` selects the canonical S1 Design cohort and its
actual legacy/schema/model dependencies. It does not repin the old producer.
Guarded source code and all selected inputs are copied to a private snapshot;
the canonical model executes against those copies. Originals and scanner bytes
are rechecked, and measured trees rescanned, before the report is returned.
Scanner execution uses a copy of its selected bytes. Its digest and declared
revision are operator consistency evidence, not authenticated compiled provenance.

The report always says `standing: "development-unverifiable"`, with a separate
`comparison: "consistent" | "incomplete" | "mismatch"`, blockers, exact selected artifact digests,
and measured/unmeasured sides. Missing expected/side/evidence artifacts or an unmeasured side
retain known measured facts and make comparison incomplete unless a known mismatch
takes precedence. Permanent missing trust/probe/qualification blockers are separate; no replacement reference is invented. Complete inventory equality includes root and
directory modes, file kind, path, size and hash. Manifest equality alone is
insufficient. Legacy summaries/executable digests are checked only against each
actually measured side. Canonical model passes establish value consistency only;
its `reference-equal` return is not emitted as an observed status. Missing
attestation never suppresses independently known tree, pin, or candidate
contradictions. Signing, terms, every-Mach-O coverage and other selected claims
are not new observations. Trusted compiled anchor, signature/build integrity,
installed custody, probe, label, native package checks and qualification remain
missing. No H5, S1 observed verification, lifecycle event, Host, Selected or Store
is created or invoked.

## Maintained checks

```
DISTRIBUTION_STATIC_BIN=/absolute/physical/distribution-static \
  PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover \
  -s app/packaging/static_distribution -p test_connected.py
```

Fixtures are invented, including their signature/packaging value fields. The
suite invokes the actual prepare command and selected built Rust scanner. Two
explicit mutation wrappers test snapshot/recheck behavior; they are test seams,
not scanner provenance. No supplier fixture is executed.
