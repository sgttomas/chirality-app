# Independent S1 review

Verdict: **READY for the bounded proposed successor package**, candidate `7aa1ae354b` (full revision and artifact hashes in CHECKS.json). No unresolved blocking findings at this scope. This is not technical adoption, completed A-IN-S1 canonical rollout, supplier qualification, production implementation, FP-2/W-4, Group B completion or a stage-gate decision.

Reviewer: independent TASK `/root/distribution_successor_design/s1_review`, harness-native descendant of HELPS_HUMANS `/root/distribution_successor_design`; no delegation. Reviewer authored only this reviews directory, in an isolated checkout. Source reading origins and limits are in READ_BASIS.json. Reviewed change against receiving main `015f9763ead9294b3857038e5d9cbaf2f9816244` is confined to distribution_successor. Earlier main routing changes are receiving basis, not this review's authored scope.

## Findings and disposition

1. Draft LT-24 accepted an unverifiable artifact with no observed label. Independently reproduced; final model requires raw and parsed label. Negative reproduced on the final candidate and refused.
2. Draft LT-24 accepted a pre-probe observation despite the pre-server revalidation duty. Final model requires pre-spawn evidence; independent negative refused.
3. Draft package join could reuse an observation across App builds sharing a supplier tree. Final candidate_subject joins App revision, build identity, package-record ID and installer digest. Independent foreign-build negative refused. The runtime artifact remains external to the installer, avoiding a digest cycle.
4. Draft package checker required an already verified runtime witness for every package record. Final successor separates static distribution_status from optional runtime evidence; missing qualification is representable as unverifiable. Independently exercised a pending-reference package successfully without promoting it.

The first two were concrete reviewer findings. The latter concerns were also identified and coordinated by the parent; all repairs were inspected independently on the assembled candidate.

## Evidence and conclusions

- Independently reran all 13 author tests: pass. Nine additional reviewer vectors in probe_review.py pass, covering valid joins, untrusted selection, cross-build mismatch, pending inputs, development standing, missing label, pre-spawn requirement, contradiction precedence and exact-byte tampering.
- Independently compared the embedded legacy lifecycle and PKG schema properties/required/conditional/definition shapes to their originals: equal. The model checks the pinned legacy transition table and invokes pinned PKG semantic rules. PK-R4's unchanged separate terms record remains explicitly mandatory; no assertion that this prototype checks terms or whole lifecycle streams.
- Independently recomputed preservation hashes and compared canonical HOSTING/PKG plus all four production source manifests to the original basis: unchanged.
- The immutable reference → independent attestation → build-selection → compiled App anchor is acyclic. No earlier artifact contains its own digest or final package identity. The checker accepts an externally trusted attestation selection only as an explicit offline test seam; production anchor construction, signature/integrity and stable custody remain S2/S3/S5 duties. Self-declared JSON or equal digests do not authenticate an actor or qualify a supplier.
- The proposed method preserves full path/type/mode/size/digest comparison and inventory identity rather than reducing equality to a file manifest. Candidate reference and runtime artifacts carry generation, launcher, configuration, evidence and missing-input standing. Known contradictions dominate gaps.
- Adoption routing explicitly retains R23-22 pin selection; DEL-01-02/03/05 and DEL-04-03 receiving assessments; exact EXP/SQ candidate/package/support joins; CI-26's three schema IDs plus prototype digest; historical version standing; FP/signature/native and owner-act obligations. No new B→A prerequisite or cross-group cycle was found. Supplier-reference qualification does not await a signed App/package witness.

## Limits for reliance

These checks establish only the proposed record/value model and migration plan. They do not inspect actual supplier acquisition, generation correspondence, probe evidence, reviewer authority, signatures, hostile filesystem races or installed custody. Actual scanner, immutable resolver, compiled trust anchor, lifecycle stream behavior, EXP/SQ full identity joins and all native witnesses remain their named later work. The narrow prototype's passing values must not be treated as authenticated qualification. Independent review of canonical adoption and connected implementation is still required on their actual revisions.

## Schema size and coverage assessment

The complete legacy embeddings are justified at this proposal scope: they preserve closed historical shapes while adding versioned envelopes, rather than allowing new fields in old records. Independent structural equality checks cover their preserved constraints, and every local schema reference resolves (25 references across six schemas). This is duplication with a maintenance cost, not added assurance from line count. Canonical adoption should retain explicit generation/source checks for these copies or a reviewed self-contained reference packaging strategy.

The 13 tests and nine independent vectors cover the critical identified false-verified paths in this offline model, including exact bytes, selected trust, contradictory evidence, tree modes/generated identity, retained signing rule, cross-candidate identity and LT-24. They are not exhaustive schema/property fuzzing, filesystem/race testing, full PK-R/transition scenario coverage or a connected production proof. Preserved legacy checks and required future consumer regression suites remain necessary.
