# First-package input account — source candidate 7b0170ed

This read-only technical account is bound to App source revision
`7b0170ed4d3f0a1a0b4b9cdb2128a60526d74af9`. It examines packaging inputs;
it is not a package identity record, an EXP native result or qualification.
No supplier binary or App was executed.

| PKG requirement / point of need | Observed source state | Needed contribution / owner |
|---|---|---|
| P-0/P-4; CF-2/3/5; B2 | tauri.conf.json names skeleton product, version 0.0.0, dev.chirality.app-v4.skeleton; bundle.active=false; no bundle resource mapping | Packaging owner supplies actual candidate configuration, stable App identifier/version and minimum macOS; no signing identity or credential inferred |
| P-1; FP-0/FP-1(a) | Current config has no complete vendor resources mapping. Group A README describes approved complete 0.160.0 tree and direct vendor entrypoint | Packaging owner verifies available approved full tree, modes/links/signature facts and copied identity; no download authorization inferred |
| HOSTING §7.2; FP-2/W-4 | hosting.rs verify(), lines 697–707, hashes bin/codex only; even matching development digest returns unverifiable with qualified full distribution identity absent. start allows the explicit labelled development exception, not verified standing | DEL-01-01 supplies reviewed full-distribution expected identity and runtime verification/launcher integration before packaged verified startup may pass. This is a known Group A development limit, not a new reversed dependency |
| P-2; WR LS-5/LS-8 | resources/development_workflows contains development catalog content and source map; no production bundle mapping in tauri.conf.json | WR/packaging owners identify the production bundled workflows/shipped-revision manifest and their bytes for actual P-2; do not rename a development example as shipped qualification |
| P-3; ROLE GS-1…3 | resources/instructions contains product guidance, four role files and SOURCE_MAP.json; no roles.json path found among those resources | ROLE/packaging owners supply/check the designed role-set artifact and actual P-3 placement; existing source files alone do not prove bundle composition |
| SIGN-1 B; FP-1(b)/FP-3 | No first Group B package produced or signed here | Owner Apple-account acts at their point of need, after concrete configuration; B keeps supplier signatures; no reliance until required checks pass |
| SQ I-6 | Qualification design permits native_development; package optional for those steps, and native_development never stands for native_packaged | Independent examiner identifies actual subject/route; source revision alone opens no native examination |

HELP_HUMAN confirmed in the active coordination message that the known
DEL-01-01 full-distribution verification contribution should be recorded at
FP-2/W-4; the parent will coordinate the Group A follow-up when it becomes the
next blocking input. This is an implementation coordination disposition, not
new human scope authority. Group A CI-11 concerns positive user verification;
it is distinct from this full-distribution verification gap.

## Source identities

- `projects/chirality-app-v4/app/src-tauri/tauri.conf.json` — sha256 `5f848cc760814808e8013aac972c1ecf90251818b41f4358ee0f342359c4b3ec`
- `projects/chirality-app-v4/app/src-tauri/src/hosting.rs` — sha256 `108d63fa18975ec38ecf488938ec86c8e4a19a2abc7fde9c19879a1b2639331a`
- `projects/chirality-app-v4/app/src-tauri/resources/instructions/SOURCE_MAP.json` — sha256 `ca3ff9b483d70a3c4dbe818c520cc3a16c750cbf81aa5bee88460c09c7f92f82`
- `projects/chirality-app-v4/app/src-tauri/resources/development_workflows/SOURCE_MAP.json` — sha256 `4f49c28ba5721b492bb28ca2799b7aeff30c11964cc4e1bda293e5d3d3f666c4`

## Offline continuation receiving evidence

The parent-supplied [A-IN proposal](distribution_input/PROPOSAL.md), source
commit 8ab04247db on 462f66975d, is integrated as technical investigation. It
reproduces the complete 42-file manifest but identifies HOSTING U-08/U-17 and
qualified expected-tree provenance as unresolved. HELP_HUMAN separately
coordinates CC-HOSTING-DISTRIBUTION-01. FP-2/W-4 remains blocked until reviewed
Design selection, qualified expected identity, and connected runtime/launcher
implementation arrive; inventory equality alone cannot supply them.

[Candidate values](offline-preparation/CANDIDATE_VALUES.md) retain 15.0 and
dev.chirality.app-v4 as proposals. Supplier load commands explain the former;
App binary compatibility and native launch have not been established. The
identifier creates no durable signed identity before the concrete signing
candidate is presented at the existing owner point of need.
