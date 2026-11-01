# One-file macOS runtime license-source receipt proposal

2026-11-01. Current integrated index: 22 components, 30 retained texts, five
macOS-specific components with explicit missing upstream text. Neither the index
nor those gaps is changed by this metadata-only contribution.

The five locked archives' recorded `.cargo_vcs_info.json` revisions and README
`../../LICENSE.md` links resolve to repository-root LICENSE.md. Public GitHub
commit and exact-tree metadata establish that all three revisions select the
**same Git blob**, `540ae4c81adb5f64a9f61e222b688880da24300e`, **1,339 bytes**.
The adjacent `macos-runtime-license-metadata.json` retains per-crate archive and
README identities, declaration targets/licenses, commit→tree→file relationships,
query URLs/dates and full-response custody hashes. No authentication headers or
file/archive body retrieval were used.

| Cached crate | Version | Exact upstream revision |
|---|---|---|
| objc2 | 0.6.4 | `8852b424193ca41602281b3d7540d7c8ed51e49a` |
| objc2-app-kit | 0.3.2 | `7b1abfd750a2cacaea71d6a56ecfb83cb7de560b` |
| objc2-foundation | 0.3.2 | `7b1abfd750a2cacaea71d6a56ecfb83cb7de560b` |
| block2 | 0.6.2 | `b4167b582b2f75f9a1be75495c41b765344fd03c` |
| dispatch2 | 0.3.1 | `8852b424193ca41602281b3d7540d7c8ed51e49a` |

All rows retain their distinct `cfg(target_os = "macos")` association. The
mixed declared-license expressions are preserved; a shared README link/blob
is not a generic MIT substitution or a license election.

## Minimal additional owner retrieval decision

Retrieve **one file, 1,339 bytes**:

<https://raw.githubusercontent.com/madsmtm/objc2/8852b424193ca41602281b3d7540d7c8ed51e49a/LICENSE.md>

Expected Git blob ID: `540ae4c81adb5f64a9f61e222b688880da24300e`.
Purpose: receive the exact upstream text linked by the five cached crate
READMEs, inspect its actual scope against their declarations, and preserve an
upstream-Git notice association. Do not mislabel it as a member of the crate
archives, which omit it. After authorised receipt, check exact size and Git
blob hash and record a SHA-256 of the raw bytes before any notice-input adoption.
Any further referenced text requires its own evidence and acquisition scope;
this proposal does not authorise following links or downloading a repository.

The inspected prepared Cargo cache had no root notice file of this exact size,
and neither the selected local Chirality nor App Git object database contained
this blob. This is a bounded local search, not a whole-machine absence claim.
The missing input is therefore this exact upstream file body; no download or
new text coverage is claimed yet.

## Combined next source-receipt packet

The existing [ten-file Codex proposal](RETRIEVAL_PROPOSAL.md) remains separately
pending: 128,666 bytes pinned to Codex commit a956835d020762cb2b570053af06f643a11c0ecc.
If the owner approves both scopes, the total is **11 unique files, 130,005 bytes**.
Approval or merge of either proposal must not be treated as approval of the other.
No binary archives, signing credentials or production identity inputs are needed
for these receipts.

Already available exact Codex root LICENSE/NOTICE stay separate: their local
bytes match the pinned Codex tree metadata, so no retrieval is requested for
them. The four complete main/code-mode-host/rg/zsh binary→source→notice
associations remain open; the ten Codex files target their unresolved build/
assembly edges. The macOS file above addresses five different direct-runtime
text gaps. Neither set supplies complete transitive coverage, legal approval,
supplier qualification, native evidence or release authority.

The production-subject recommendation remains `com.chirality.app.v4` under the
recovered team, pending owner selection. This notice receipt work does not choose
that subject, alter the existing closed publisher input, or activate signing or
keychain enrollment. Existing package/S4/EXP/SQ formats and retained bundles are
unchanged.
