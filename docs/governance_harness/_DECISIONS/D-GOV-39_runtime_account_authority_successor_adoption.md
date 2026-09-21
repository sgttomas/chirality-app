# D-GOV-39 — Runtime account-authority successor adoption

Status: RULED AUTHORITY APPLIED LOCALLY; publication and post-merge backcheck pending.
Owner: Ryan Tufts. Date: 2026-09-07 America/Edmonton.
Basis: PR #751 candidate `c3e9ab0f8e49314befc1fc81a9e01346641a7344`; D-GOV-36 narrow semantic approval; D-GOV-37 Root implementation direction.

## Existing authority and exact referent

This record applies existing authority; it does not create or paraphrase a new owner vote. D-GOV-36 records the owner's narrow account-only semantic approval, and D-GOV-37 records the owner's authorization for bounded Root recognition of owning-accepted Runtime successors. The consolidated Agent 0 direction authorizes the sequencing used here: exact branch-local accepted Runtime bytes may be recognized as `accepted-pending-publication` within PR #751, followed by CI, publication, and a fetched-main backcheck.

Runtime's immutable Gate 5 owner acceptance is `projects/chirality-runtime/execution/_ScopeChange/ACCEPTANCE_SCA003_GATE5_2026-09-07/OWNER_ACCEPTANCE.md`, SHA256 `edfd03dfc559438531af1e714532210caf54aae4b959f246e9065f75eba0365e`. It binds exact subject `projects/chirality-runtime/execution/_Coordination/AgentRuns/APP_V3_CONSOLIDATED_RESUME_2026-09-07/scope/GATE5_POSTSTATE_MANIFEST.json`, SHA256 `0fcaae692e617419b6ea34fc4b57aaf6c855317803adbe3e88ebec2ff963470b`. The acceptance package manifest is SHA256 `a4cd1680631e44835e3f89c008ea791251d874c20052ca7ec4351fb92d332990`; it records the complete accepted SCA-002 to SCA-003 chain, including SCA-002 snapshot SHA256 `8865716ba1fb55188658ae39ae9cef06ef17290b0801552621e93faee76aeda3` and SCA-003 snapshot SHA256 `ce84376323a5d213c8a6dadcbf47534ecba407a9128543250f55e4b13eaaaa48`.

## Exact bounded adoption

Preserve the `D36_STAGE1` and `D36_STAGE2` adoption objects and their order. The new immutable policy adds one `D36_ACCOUNT_AUTHORITY` entry. Its exact current canonical changes are:

- `ACCOUNT_CONTROL_AUTHORITY_DISPOSITION.md`: absent to `19baaea22ba3a5b2dc465c30f7e8273db7b1833fd4a9bf6c2de0fc6056dcdd9d`;
- `Chirality_Runtime_SOFTWARE_DECOMP_v1_0.md`: `d26e03f580f1d33a7c906f8509418ab6d0f5774b7b5102a593dbae400eb381e1` to `413687ca6a857f5464a3205e9f9c4b29ace512c8d2b67dfa095ef3640fab883e`;
- `RUNTIME_SCOPE_LEDGER.csv`: `3d9b7210994804c53e7433fd497a8b417dcd7bae67c95b1bc9168abd8063e2d9` to `bffda2701dea3667a63f72194404db72b20520802a7d840af13ac456fb1f149d`.

The helper must verify the owner acceptance, accepted subject and every subject member, acceptance package and every package member, both snapshot manifests and every snapshot member, exact chain identities, final canonical hashes, predecessor continuity, and bounded live paths. Missing, tampered, mixed, unknown, or escaping evidence/state fails closed. Publication remains a separate observation against `origin/main`; recognition grants no execution authority.

This tranche changes no Runtime bytes, SOW, source/product, supplier, fixture, lifecycle, hold, activation, release, `.gitattributes`, historical policy/run record, or four effective-state YAML files. App and Runtime notices coordinate publication and backcheck only. Root-first publication is followed by Runtime publication/synchronization as applicable and a fetched-main recognition backcheck.
