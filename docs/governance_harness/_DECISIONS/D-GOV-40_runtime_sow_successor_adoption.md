# D-GOV-40 — Runtime SOW successor adoption

Status: EXISTING AUTHORITY APPLIED LOCALLY; publication and fetched-main backcheck pending.
Owner: Ryan Tufts. Date: 2026-09-07 America/Edmonton.
Basis: D-GOV-37; exact proof-closed staged candidate at `c5192790f98ec024e7c2728cb1d4df3ae2b2a2dd`.

## Existing authority and exact Runtime acceptance

This record applies D-GOV-37's existing owner direction for bounded Root recognition of owning-accepted Runtime successors. It does not create, quote, or infer a new semantic owner vote.

Runtime's owning acceptance manifest `projects/chirality-runtime/execution/_ScopeChange/ACCEPTANCE_SOW_PROPAGATION_SCA002_SCA003_2026-09-07/OUTPUT_MANIFEST.json`, SHA256 `e90c7850b6ef22a18db9929b2d8e1c80c22ec04fcd174fac15493469f5de602e`, binds owner acceptance `0329293b691862f9bd1d3ca2977278e3706b278aa3ac4d177f24a289fa016367`, accepted subject `37141786ee3806d41402996f9cb7e022bbb071d94efadc46f151f310d2c864a5`, postimage index `ffac42013c68c2ce2f36469b7e37808fffab0d0f18fa723d9a1d7439a3d3e470`, audit snapshot `432aa2e1238d93c4b28e923ba19e12e3bfbaf52152845f8195eb18a9e27665b1`, application addendum `efb4011fa2a777d096ec15d50964234a8aef218a3bed1971c5a817d21a7dc6d0`, and current pointer `da47241ba281cb65cf7f74dfd74fbbf5c65d220ad5488b607d8b70f1245edc81`.

## Exact bounded adoption

The new immutable Root policy preserves the prior three adoption objects byte-for-byte and in order, then appends one `D36_RUNTIME_SOW_PROPAGATION` adoption:

- DEL-02-06: `e87e567f7be38e6a98a2c15ee44dd7f5c2e7ebdf72628155ea18a62e539aaa54` to `2e66ee8681800307f5675db63c9870413bb6148bc5cace8e3423ac89b4eeaefe`;
- DEL-02-09: `5e46d0a1538618d69b4e9ae6368b5a71dc96aeb4bc4d2d9c46a6d0b23cbcc46e` to `0d154c0067da5a9152c46497bead5cd16cfe3fc524a0bc0648c103b32822fd3e`.

The format-aware verifier is limited to this frozen Runtime acceptance schema and verifies the acceptance package and members, owner acceptance, Markdown subject, manager and audit manifests and members, application addendum and members, acceptance bindings, postimage-index projection, current pointer, exact live postimages, Root handoff/input bindings, and predecessor continuity. App DEL-02-05 is outside this policy. Missing, altered, duplicate, mixed, escaping, symlinked, wrong-type, App-path, and unknown-path states fail closed.

Branch-local accepted bytes may report `accepted-pending-publication`, `published=false`, and `execution_authority=false`. Main publication is observed separately. This act changes no Runtime/App SOW or canonical bytes, source, supplier/account operation, credential, implementation, fixture, lifecycle, hold, hosted readiness, release, or cross-project concordance state.
