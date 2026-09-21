# OD7-G1 Candidate Handoff

Status: `READY_FOR_OWNER_GATE — CANDIDATES NOT APPLIED`

Basis: `main@fb16e32ed60bb4f384cf1e07a83c4a14ff63bbae`

## Frozen package identities

| Package | Files including hash manifest | Hash-list entries | SHA-256 of `ARTIFACT_HASHES.sha256` |
|---|---:|---:|---|
| Root batch | 11 | 10 | recorded after this handoff in the final Root hash freeze |
| App | 10 | 9 | `42b4fbaf362d7c05038e0b4259416c68e2c326f796006ff3c2fa8824d29ac4d8` |
| Piping | 9 | 8 | `25eafabaecfafae52b3588b1a3c522b6dab9d4e91ca9676f6048c77c3dbad456` |

The Root hash-list identity is reported with the owner gate because a hash
manifest cannot contain its own digest. All three manifests reproduce every
listed artifact.

## Validated terminal state

- Six exact candidates are staged; zero live application occurred.
- Candidate basis and accepted derivative input are named.
- Piping C04 is visibly corrected from the evaluation's stale `0.9` target to
  accepted revision `0.10`: `_LATEST` `0.6 → 0.10`, with the companion
  frontmatter `0.9 → 0.10` returned separately for explicit approval.
- Original notices, ruled records, JSON contracts, corpus membership, hold
  semantics, product state, and lifecycle state are preserved except for the
  exact proposed future one-line identity/display/currency changes.
- Patch, ancestry, first-publication, App corpus, APP-HOLD, expected Piping
  mismatch, ID-scan, receipt, structured-file, path-containment, whitespace,
  inventory, and hash checks pass.
- The owner may approve all six or a named subset. A subset that changes a
  combined receipt or manifest requires a narrowed reissue.

## Remaining gate

Explicit owner approval of exact frozen candidate bytes. No Git action is
authorized or performed by this proposal-stage handoff.
