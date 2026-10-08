# H3B namespace admission R1 independent review

Verdict: READY for bounded manager fan-in of repaired frozen candidate, manifest SHA-256 e26f25651db18a2fdfe89ef851be2a570cb17c60c9f44870aded2aefc306b6e9, base 7fd670cc061a564d9a1c3a8cc3e85a4f870cf418. Original P1 is repaired and its original failing vector is killed. No unresolved blocking finding. This does not confer whole-head, Group B adoption, CI or production standing.

Rechecked all maintained hashes and 48-path scope. Only distribution_store.rs differs among maintained files from the original frozen candidate; remaining additions are repair/failure/review evidence and return updates. Initial report, manifest, patch and both diagnostic/failure logs retained in author/review_initial are byte-identical to independent originals. No accepted B pin, canonical Design, MEMORY or unrelated C3 change is included.

The repair factors validated_root to open and validate one descriptor and return it. Geometry-only admission preflight discards that descriptor; Store::guard keeps it through its return. The hook runs after validation with the descriptor still owned, and there is no second path open. publish_attempt and S1 guard_s1/publication/read callers consequently rely on the checked object. Later path identity checks can refuse a renamed original, but publication no longer writes through the replacement merely because it occupies the old name. This restores the previous descriptor boundary; it does not claim an atomic filesystem snapshot or rollback of work in the genuine original directory.

Independent validation:

- Original reviewer test body/name byte-identical to the failed source-only control.
- Default original replacement vector: 1 passed, 0 failed.
- distribution-successor/custom-protocol original replacement vector: 1 passed, 0 failed.
- Combined deterministic namespace suite: 12 passed, 1 intentionally ignored worker (worker exercised through watchdog). Covers busy read/write, Stop/EOF liveness, old capabilities and outcomes, unavailable REC, final failures, two-home S1 continuity and the cold-read/hot-join boundary.
- Maintained app diff whitespace check passed.

Raw independent results are default-original-vector.log, combined-original-vector.log and combined-namespace.log; HASH_CHECKS.json preserves exact scope and correspondence. Reviewed author affected repair matrix reports 68 passed/2 intentionally ignored in each feature mode, including Store, S1 and namespace tests. Earlier broad passes remain historical and are not evidence that the original bug was absent. The initial patch-transplant compile diagnostic is preserved separately.

Reuse the initial full code/claims review for unchanged files: production Root wiring invokes the real coordinated adapter; shared authority/operation lease order, separately leased postwrite persistence, retained hot-join lease, private REC preparation and truthful postcommit setup limits fit the exact approved proposal. HomeSession/router failure tests remain wrapper-level injections, not exhaustive actual UI/router fault execution; source ordering and actual Host-construction refusal are separately inspected/tested. No unsupported broad claim is added by this READY.

No reviewed-source edits, native supplier/App launch, downloads or credentials. Shared target used serially and released. Existing independent TASK mechanism and reviewed proposal basis unchanged. Next: manager committed-head integration backcheck, fresh exact-source exports and Group B named adoption before final CI. Source-pin drift is not permission for bare repinning. No S3 issuer, restart hydration, other lifecycle mapping or release follows from this increment.
