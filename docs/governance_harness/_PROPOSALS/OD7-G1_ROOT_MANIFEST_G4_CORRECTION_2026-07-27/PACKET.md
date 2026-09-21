# OD7-G1 Root G4 Correction Candidate

> **Status: CANDIDATE — NOT APPROVED OR APPLIED.** This additive proposal
> does not alter the three frozen OD7-G1 packages or authorize any live write.

| Field | Value |
|---|---|
| Candidate | `OD7-G1-ROOT-G4-CORRECTION` |
| Basis | `main@fb16e32ed60bb4f384cf1e07a83c4a14ff63bbae` |
| Original approved Root package manifest SHA-256 | `d6421ce6076238fd49dc0469d1160f8dc7698b2e730d8833e57136baaa957aa0` |
| Prepared by | `HELPS_HUMANS`, managed by `HELP_HUMAN` |
| Artifact class | proposal; non-authoritative |
| Date | 2026-07-27 |

## Finding

During exact live application, the repository's registered G4 validator
rejected the original candidate
`PROPOSED_ROOT_MANIFEST_ROOT-OD7-G1-20260727.yaml`:

```text
manifest ROOT-OD7-G1-20260727.yaml: m2_gate missing keys: ['self_merge']
manifest ROOT-OD7-G1-20260727.yaml: m2_gate.merge_gate is
'exact-owner-approved-candidate'; M2 requires 'human-gated-pr'
```

The original candidate's validation established YAML parsing but did not run
the registered G4 validator. The live application was fully reverted before
staging or Git action. All three original proposal packages remain
byte-identical at their approved hashes.

## Exact correction

If separately approved:

1. use `CORRECTED_ROOT_MANIFEST_ROOT-OD7-G1-20260727.yaml`, not the original
   proposed Root manifest, as the exact source for the live tranche manifest;
2. use `CORRECTED_ROOT_RECEIPT_53.md`, not the original proposed Root receipt,
   as the exact append fragment;
3. retain every other approved C01–C06 candidate byte unchanged; and
4. route the resulting Root instruction-surface PR through a human-gated merge.
   The standing session self-merge authorization is not used for that PR
   because registered G4 requires `self_merge: false`.

The manifest correction is exactly:

- `m2_gate.merge_gate: exact-owner-approved-candidate` →
  `m2_gate.merge_gate: human-gated-pr`; and
- `m2_gate.self_merge_after_owner_gate: true` →
  `m2_gate.self_merge: false`.

The receipt correction adds this package to candidate identity, records G4
validation, and states the human-gated merge requirement. No decision,
register, notice, decomposition, App, Piping, product, runtime, repin, or
SCOPE_CHANGE byte changes relative to the original approved batch.

## Gate

DecisionID: `OD7-G1-ROOT-G4-CORRECTION`
RequestedBy: `HELPS_HUMANS` through `HELP_HUMAN`
Question: Approve the two corrected exact Root fragments in this package,
with all other C01–C06 bytes unchanged and the Root PR reserved for a human
merge?
Recommendation: approve. This is the smallest correction that conforms the
approved batch to the registered deterministic G4 contract without weakening
the guard or silently misrecording the integration route.
DownstreamBlocked: OD7-G1 application and Git closeout.
