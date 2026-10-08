# H3B-1 author checks

Initial freeze (historical) source candidate: CANDIDATE.initial.json, receiving f79317be861bb63553512de3197b22d556268198. All process tests use invented local fixtures; no actual supplier or App launched. Offline Cargo cache and /private/tmp/hosting-s2-target were used serially with manager authorization. Existing unrelated unused/dead-code warnings remain.

| Check | Result | Evidence |
|---|---|---|
| Default `cargo test --offline --lib hosting:: -- --test-threads=1` | 127 passed; 1 intentionally ignored subprocess fixture exercised through its passing watchdog | checks/hosting-final.log |
| `cargo test --offline --features distribution-successor,custom-protocol --lib hosting::successor::tests -- --test-threads=1` | 11 passed; production feature compiled, only synthetic fixture processes executed | checks/production.log |
| `cargo test --offline --lib distribution_preflight -- --test-threads=1` | 13 passed; scanner/trust-chain source unchanged subsequently | checks/scanner.log |
| `cargo test --offline --test hosting_contract` | 6 passed on final integrated candidate | checks/legacy-final.log |
| Locked dependencies `npm ci --offline --ignore-scripts`; actual frontend `npm run build` | Both passed, no manifest/lock changes | checks/npm.log, checks/frontend.log |
| Source `git diff --check` | Passed; staged raw Cargo logs retain original blank EOF lines and produce cosmetic warnings only | author check |

The first production-feature compile refused absent ../dist in this fresh checkout; actual frontend build resolved that environment prerequisite. No fake frontend assets were used. Source hashes remain unchanged after final feature/Host checks. Independent review and required CI remain pending. Official `validate_private_terms.py --staged --from-host --require-terms` passed: 15 changed files, 3 terms, zero findings. No author commit is made in this checkpoint.

## R1 repaired candidate

Current source hashes: CANDIDATE.json. Diagnosis and original failure preservation: R1_REPAIR.md. Only hosting.rs and hosting_successor.rs changed since the initial maintained-source freeze.

| Check | Result | Raw evidence |
|---|---|---|
| Unchanged independent original Stop/start reproducer, author rerun | Expected failure reproduced, 1 failed, exit 101; cancelled attempt spawned | checks/r1-author-original-repro.log |
| Repaired full default Host suite | 131 passed; 1 expected ignored watchdog fixture | checks/r1-hosting.log |
| Final affected successor suite after scoped handshake diagnostic preservation | 16 passed, default features | checks/r1-successor.log |
| Same final successor suite with distribution-successor,custom-protocol | 16 passed | checks/r1-production.log |
| Final legacy hosting contract suite | 6 passed | checks/r1-legacy.log |

The full Host run preceded the last scoped handshake-diagnostic retention change; the affected successor suite was rerun on final bytes in both feature modes, and final legacy checks followed. Scanner/reference resolution source is unchanged, retaining the initial 13 passing checks. All R1 tests are synthetic fixture process tests. No real supplier/App/native acts or new dependencies were used. Source-only diff whitespace check passes; original raw log blank EOF lines remain untouched. Final official staged private-term validation passed: 24 files, 3 terms, zero findings, before any commit. Shared target is released after these completed checks; independent backcheck and manager integration remain pending.
