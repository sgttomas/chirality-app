# Unsigned supplier preparation return

Implementation candidate: `fb5e152036`; author TASK
`/root/group_b_manager/support_production`, parent WORKING_ITEMS
`/root/group_b_manager`; no delegation. Basis: PR #1117 main merge
`462f66975d36cd10d5b8455193ada9517d28d353`.

Maintained `app/packaging/prepare.py` and `inventory.py` now inventory and stage
an explicitly selected complete supplier tree into P-1, compare content/modes/
links and preserve the rest of the unsigned package configuration as an input
account. They never invoke supplier code or packaging/signing tools. Canonical
PKG sources are pinned; no dated evidence is a maintained dependency.

Fifteen tests pass. Negative coverage includes changed file bytes/modes/root
mode, missing/extra files, file and directory links without following them,
symlink roots/output, special files, ambiguous manifest paths, wrong pin or
manifest, absent inputs, non-executable main binary, reused/overlapping outputs,
failed copy publication, and unavailable/malformed signature observations.

The actual approved 0.160.0 tree has 42 files and 30 Mach-O, with the canonical
manifest `327effb91a5854eccb388321b4b160e059795f0402c553f594e85365189d8d12`.
`preparation.json` records a real equal staging comparison, including modes.
The concrete output remains at
`/private/tmp/chirality-group-b-unsigned-rosc6usm/stage/`; supplier bytes are
not added to Git. `PREPARATION_CHECK.json` binds the source commit/tree/tool
hashes, commands, outputs, origins, limits and staging path.

`host-inventory.json` reports FP-0 pass by read-only Apple signature display:
all 30 Mach-O carry the stated supplier authority, team, hardened runtime and
timestamp, without get-task-allow; the tree has no links and stayed unchanged.
`sandbox-inventory.json` preserves an inconclusive observation of the same
bytes: the host sandbox hid authority/timestamp and warned about entitlements.
The tool treats those unavailable observations as inconclusive. A reviewed
read-only host escalation supplied the usable display; no supplier ran.

This is **partial B2**, not a package. Only P-1 was staged. No Tauri build,
FP-1(a), signing, FP-1(b), notarisation/FP-3, FP-2/W-4, native smoke or SQ result
is claimed. Existing guidance and four role files were inspected as assets,
not staged/adopted as production content. App binary, version, role set,
shipped workflows/manifest, signing identity and notary profile remain missing.

The parent-proposed `dev.chirality.app-v4` and minimum macOS `15.0` are explicit
preparation parameters, not durable identity acceptance or tested OS coverage.
The parent retains their grounds/owner coordination. `tauri.conf.json`, shared
README, Design, contracts, dependencies and graph are unchanged.

## Parent continuation

- Route independent review against the final branch and repairs back here.
- Add the explicit packaging test command to shared documentation/required
  checks as appropriate; normal `npm test` was not changed and does not run it.
- Keep B2 partial: finish actual App/P2/P3/P4 production content and Tauri
  resource mapping under their owners, then perform FP-1(a) after actual bundling.
- Keep the existing A-IN full-distribution verification input before FP-2/W-4.
  This inventory/copy path does not change HOSTING's development-only verifier.
- Preserve SIGN-1 B and its actual FP-1(a/b)/FP-3 prerequisites. OI-011 SWB part
  remains open. No new contract amendment is proposed by this implementation.

The host's existing Git identity was used without changing account settings.
Source and technical preparation checks are ready for review, not owner review,
acceptance, release or a completed Group B stage.
