# CC-HOSTING-DISTRIBUTION-01 — A-IN-S1 successor package

Status: proposed, not adopted. This package supplies a concrete successor for review. Accepted HOSTING/PKG Design bytes and all production source pins remain authoritative. Neither merge nor schema conformance qualifies a supplier, an App package, a user journey or a stage gate. No owner decision is recorded here. PKG U-PKG-3/R23-22 remains controlling: select the newest pin with a passed version-advance check when the candidate is built. The retained 0.160.0 package is only a method-shape sample and design-compatible source, not the automatic qualification pin.

## Decision and source boundary

Basis: origin/main `f2e7a2a9ff3ba4e6f5dd0f726766961c8dba1ce1`; PR #1122's staged patch and DISTRIBUTION_IDENTITY proposal; Group A and Group B A-IN-S1…S5. The focused prior patch remains historical staging. The candidate contracts in `contracts/` and the exact proposed prose amendment here travel together; do not apply the old patch alone as a complete migration.

- PROPOSAL: Adopt a complete versioned distribution contract cohort after review.
  - Evidence: distribution_integration/INTEGRATION.md records the failed partial migration, unchanged accepted preimages, and three rejecting freshness guards; Group B graph A-IN-S1 specifies full expected/observed/lifecycle/PKG successor contracts.
  - Change: Select the candidate schemas, semantic rules, examples and this adoption plan as one named technical successor; place the reviewed artifacts in owning Design homes only in the separately named adoption change. Migrate producers, consumers and pins at their explicitly declared points below.
  - Why: Complete inventory equality must survive runtime, packaging and examination boundaries without being reduced to the historical file manifest.
  - Risk: Merely repinning current readers would falsely claim support for fields and checks they do not implement.
  - Status: PROPOSED

- PROPOSAL: Separate immutable supplier reference from its qualification attestation.
  - Evidence: DISTRIBUTION_IDENTITY.md “Expected-record provenance and bounded qualification” currently includes reviewer, reviewed revision and recorded adoption among expected-record elements; it also requires exact-byte artifact digest and independent review.
  - Change: Replace that paragraph with the exact text below. Reference bytes contain measurements and acquisition/generation provenance. A separate attestation binds their digest, independent review and named technical adoption. Build selection binds both exact artifacts.
  - Why: Review/adoption can refer to frozen reference bytes without changing the bytes it reviewed or introducing a self-referential digest.
  - Risk: A digest proves identity, not authentic authority; consumers need a trusted build selection and verified attestation chain, not an arbitrary caller-supplied JSON object.
  - Status: PROPOSED

MISSING: actual supplier acquisition/extraction/generation/probe qualification; runtime scanner/launcher implementation; production consumer adoption; real package and install witnesses.

NEEDS_HUMAN_RULING: no new stage-gate or release act requested. The existing method/launcher proposal still needs its named owning technical adoption. If the owner rejects the bounded package-shape restrictions or launcher convention, select a reviewed alternative before dependent implementation relies on them.

DEPENDENCY_NOTES: S1→S2; S1+S2+authorized supplier evidence→S3; S1+S2→S4 implementation, S3 before verified reliance; S2+S3+S4+B5→S5. No completed Group B product is an input to supplier-reference qualification.

## Exact proposed amendment to staged prose

Replace DISTRIBUTION_IDENTITY.md's first paragraph under “Expected-record provenance and bounded qualification” with:

> A supplier reference is an immutable artifact produced by DEL-01-01, not a caller assertion or a runtime observation promoted in place. It carries schema/method version; supplier pin/platform; official archive locator and digest, acquisition authorization/custody evidence; extraction procedure/source-subtree locator; full inventory and manifest; launcher convention; maintained generated-output reference identity (pin, kind/variant, formatter policy, manifest); and digest-bound observation evidence. Freeze these bytes before independent review. A separate immutable qualification attestation identifies the reference by exact-byte SHA-256, its author, independent reviewer, reviewed source revision, review evidence and named technical adoption. The attestation does not embed its own digest; the trusted App build selection binds both reference and attestation digests. Missing or untrusted attestation is unverifiable. A `qualified: true` field or a syntactically valid attestation does not confer qualification. Neither artifact contains the final App package identity. No current artifact is asserted qualified.

Read later “qualified expected-reference binding” as this pair and its trusted build selection. The full-tree identity method, exclusion/rejection rules, label/generated comparison, LT-24 mismatch precedence, stable-custody limits, launcher PATH convention and K-12 remain unchanged. The earlier focused HOSTING §7.4 and PKG §§4.4/5.5 additions must reference the reviewed successor package and version identities rather than claim that schemas remain undelivered.

## Proposed S2 build-selection anchor

The trusted selection is not a field an arbitrary record caller may choose. S2 shall create a small immutable build-selection document containing the selected method/schema identities and exact SHA-256 digests of the supplier reference and qualification attestation. Its exact-byte digest is compiled into the App executable from the reviewed source/build recipe. The selection and both artifacts ship as resources outside the measured vendor tree. At runtime, the App checks the compiled digest against selection bytes, then checks both selected artifact digests before parsing/reliance. Production has no environment, path, UI or record parameter that can replace this anchor. The prototype's separately supplied trusted digest is a test seam, not that production implementation.

Replacing both resource files cannot satisfy an unchanged compiled anchor. Replacing the executable or entire bundle is a separate integrity/custody threat: production reliance requires the existing reviewed build/signature/integrity chain and trusted stable installed-bundle custody. Record failure or unavailable trust as unverifiable; a matching digest alone is insufficient. Development unsigned builds may establish source/test consistency at explicit development standing, never signed production qualification or FP-2/W-4. This selects no new signing identity, performs no signing/notary act, and does not claim hostile same-user filesystem isolation.

The dependency order is reference bytes → separate attestation → build-selection bytes → compiled App → signed/package identity. No reference, attestation or selection contains the final package digest or its own digest. Later package/runtime records bind the actual final candidate; supplier qualification does not wait for that package. S2 must test wrong selection bytes, arbitrary replacement pairs, wrong compiled anchor, unsupported versions and unavailable integrity/custody, while S3/S5 supply actual qualification evidence.

## Alternatives and consequences

| Choice | Consequence and responsibility |
|---|---|
| Recommended: separate immutable reference and attestation | An acyclic evidence chain; permits reference qualification before packaging; requires exact-byte resolution and trusted selection of both artifacts. Keeps review/adoption external to measured content. |
| Embed review/adoption in the reference | Requires freezing a pre-review payload with a separately specified digest domain and an external signature/attestation anyway, or a second review of changed bytes. Greater complexity; cannot hash the self-contained final object including its own digest. Not implemented by this candidate. |
| Keep legacy contracts indefinitely | Existing offline preparation and historical reading remain usable at their narrow standing. Full-tree verified runtime and FP-2/W-4 remain unsatisfied; no false promotion or substitute development digest. |
| Generalize package shape now | Supporting links, hardlinks or alternative launcher conventions changes the identity method and scanner threat assumptions; requires a new reviewed method, fixtures and consumer migration. No evidence currently requires this expansion. |

## Named adoption and consumer plan

Recommendation to the App implementation owner through HELP_HUMAN: technically select the reviewed bounded tree/direct-launcher method, the separate-attestation clarification, candidate versioned schema cohort and this consumer plan. This is within existing U-08/U-17 ownership; it requests no additional human checkpoint. Record technical selection separately from the later canonical consumer rollout.

Technical adoption record must identify reviewed source commit, exact artifact set/digests, selected schema/method versions, owning adopter, independent review disposition, consumer statuses and limits. Preserve the accepted preimages and historical readers. This document is a proposed adoption record structure, not a completed adoption.

| Owner / phase | Concrete contribution and adoption condition |
|---|---|
| DEL-01-01 + DEL-01-06 / S1 | Review the complete candidate cohort; resolve staged prose clarification; named technical adoption into Design. Old closed shapes remain versioned historical shapes, never accept new fields opportunistically. |
| Group A hosting / S2 | Implement no-follow complete scanner, descriptor custody, typed production/development resolver, trusted reference+attestation selection, label/generated checks, pre-server revalidation and generation-bound observed artifact. Lifecycle producer/reader fixtures migrate together. Verified requires the full proof chain; any detected mismatch refuses. |
| Group B packaging / S2 | Produce full published/packaged inventory artifacts, successor PKG record and exact reference/attestation joins. Keep FP-0/1(a)/1(b)/3 and PK-R duties. Pending qualification is an explicit missing input, not Option B reliance. Current app/packaging/sources.json changes only with implemented successor reader and reviewed Design adoption. |
| DEL-01-01 qualification / S3 | Independently check authorized acquisition, extraction, inventory, isolated label observation, generated-output correspondence and passed version advance. Bind the actual selected pin under R23-22, with its passed version-advance evidence; freeze reference; review it; issue separate attestation; select both in reviewed build. No package/install witness prerequisite. No downloads/native probes are authorized by this plan. |
| DEL-01-02/03/05 and DEL-04-03 / S1–S2 notices | Assess generation, diagnostics/version display, homes/configuration, recovery and record-reference implications. Preserve secret exclusions and existing full-generation custody. Record each adoption or evidenced no-impact decision; do not change their pins from this package. |
| EXP / S4 | Resolve immutable artifacts by exact bytes; check complete candidate/package/support identity joins, reference+attestation pair and runtime verification. Preserve CI-26's full EXP identity (three schema IDs plus prototype digest); existing opaque aliases remain explicit tooling aliases. Migrate app/examination/sources.json and admission/sources.json only with corresponding reviewed reader behavior. |
| SQ / S4 | Propagate resolved reference/PKG/runtime identity through exact candidate, package and support joins; reject mixed successor/legacy claims. Migrate standalone sources only with actual reader and tests; retain all joined journey, mode, recorded-counterpart and owner-act requirements. |
| Packaging + examiners / S5 | Use actual installed candidate with qualified reference, full runtime artifact and exact package/support identity. FP-2/W-4 remains a real witness. Signature/notary/installation and owner acts remain separately authorized. No synthetic fixtures substitute. |

The implementation may stage successor support behind explicit version dispatch while historical readers remain active. Production adoption is complete only for a cohort whose connected paths and source guards have been checked on the actual candidate. Do not relax/remove freshness guards to admit a partial rollout. Unexpected B→A production dependency, cross-group cycle, deliverable change or invalidation of accepted Group A closeout returns to HELP_HUMAN under GC-7.

## Review and evidence boundary

Author checks establish schema/value representation and preservation only. Independent review must examine the full cohort, exact-byte resolution, reference/attestation trust separation, contradiction precedence, legacy duties, and the absence of B→A production dependence. S2 must additionally exercise filesystem mutation, links/types/modes/empty directories/root mode, unknown versions, wrong artifact bytes, missing or forged selection, PATH relocation, generation/custody and connected packaging/runtime cases. S3 and S5 need actual separately authorized evidence.

This assignment uses harness-native delegation: HELPS_HUMANS `/root/distribution_successor_design` under HELP_HUMAN `/root`; bounded TASK `successor_schema` owns the candidate contracts in an isolated worktree, requested gpt-6-astra/low. Parent owns adoption prose and fan-in; independent reviewer remains separate. File fences provide operational isolation, not a stronger sandbox. No MEMORY, instruction, graph, accepted Design, production pin, credential or native operation is changed.
