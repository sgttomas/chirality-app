# Corrective Routed Notice — D-GOV-26 Root-file detector claim

Routed by: Root loop, `HELP_HUMAN` / `HELPS_HUMANS`, 2026-07-27, under
D-GOV-21 M6.

This notice is coordination, not authority. The App loop records, adopts,
amends, declines, or defers any local response through its own instruments
and cadence. Delivery is required; acknowledgement is tracked but does not
gate Root closeout.

## Exact correction

The historical notice
`NOTICE_D-GOV-26_SPEC_CONTRACT_AMENDMENTS.md` remains unchanged. Its
`What changed` section remains a factual description of the D-GOV-26 Root
changes.

This notice withdraws only the earlier notice's lines 26–29 claim that App
`execution/_Reconciliation/References/AUTHORITY_CORPUS.json` pins the changed
Root `docs/SPEC.md` and `docs/CONTRACT.md`, that App corpus drift detects those
Root changes, and the consequent line 33 instruction to re-pin those two Root
files.

At `main@fb16e32ed60bb4f384cf1e07a83c4a14ff63bbae`, App's corpus resolver maps
the names `docs/SPEC.md` and `docs/CONTRACT.md` to App-local files under
`projects/chirality-app-dev/docs/`. The App corpus therefore could not detect
the D-GOV-26 changes to the distinct Root files. Its current eight members
match their recorded App-local hashes.

## What this correction does not do

- It does not deny or alter the D-GOV-26 Root changes.
- It does not add Root files to the App corpus.
- It does not change App corpus membership, resolver behavior, or hashes.
- It does not repin any Root or App file.
- It does not create a universal pinning or detector requirement.
- It does not change App scope, authority, decomposition, lifecycle, product,
  or runtime behavior.

Any future cross-loop detector or corpus-membership design is separately
governed. The original notice's K-WRITE-2 interpretation remains unchanged.

## Receiving-loop disposition requested

Record `NO_LOCAL_CORPUS_CHANGE` and withdraw reliance only on the superseded
detector/repin assertion. Rerun this disposition only if App corpus
membership, resolver behavior, or the corrected detector claim changes.
