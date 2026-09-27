# Independent Group 1 review — App v4

**Verdict: REVISE_BEFORE_GROUP1_PRESENTATION.** Four actionable source-fidelity/normalization findings remain in the frozen v1 package. They are bounded repairs, not new scope choices or extra human checkpoints. The original producer should repair the working candidate; the manager should return its exact identity for independent affected checks before presenting Group 1. This review does not accept Group 1 or any later structure.

## Identity and independence

Reviewer: terminal TASK `/root/renewal_research_strategy/v4_group1_review`, delegated through the native collaboration harness by WORKING_ITEMS `/root/renewal_research_strategy`, under HELP_HUMAN `/root`. This reviewer did not author the candidate and made no candidate, seed, ledger, Git, provider, or instruction changes. No descendants were created. The write boundary was this review directory, excluding preserved `input-v1/`. Enforcement is the host filesystem permission boundary plus the supplied TASK scope, not proof that the harness enforces the narrower textual boundary. No model override was requested or made; no different-model-family independence is claimed.

Reviewed candidate: `input-v1/REVIEW_CANDIDATE.json`, all ten named files. SHA256 of main `SOFTWARE_DECOMP.md`: `162e6f9f5108faee376ee2505850b3f33ab95c70e87e4e8a0882398836e379a6`. SHA256 of `ScopeLedger.csv`: `428492bf62e5590dfeffc9ddfc82bc6ec6bbc48c7b672d0cfac2926d9dcf5a94`. All ten frozen files matched their declared hashes. Repository HEAD: `4087a4f8c500a84b85dc9e8652b632550ab21a5a`, branch `codex/app-v4-project-definition-20260926`. The candidate is untracked working material, so its hashes, not HEAD alone, identify this review.

Accepted basis: `projects/chirality-app-v4/execution/_Coordination/Acceptances/APP-V4-BASIS-20260926/`, including the separate `ACCEPTANCE.md`, `COMPOSITE_BASIS.json`, full owner J–O, accepted HTML recommendations, and preserved five original seed documents. All seven composite component hashes matched. The five original seed files also matched their donor Git blobs at `9375abccaa5bccc9ca79b5ce6b8f5d26a30b977c`. I did not substitute the concurrently consolidated documents for this identified basis.

The selected method is `chirality-root:bundled:workflow:software-decomp`. I read its descriptor, entry, Group 1 method and output contract, plus Root `AGENTS.md`, `agents/AGENT_TASK.md` and `chirality-change`. `SOURCE_LEDGER.json` records actual independent reads, origins, scope and hashes. The user’s acceptance authorizes decomposition/project definition; it does not confirm this unseen normalization. No combined review, Group 2 preparation, accepted pointer or snapshot is asserted.

## Findings

### F1 — P2: Remove the remaining settled Domains ownership claims

**Affected:** SOW-023–027, SOW-249, SOW-261; `Vocabulary_Map.csv` Domains row; related OI-023/OI-026 and DEP-003.

SOW-023–027 Notes still say “provider construction external”; SOW-249 describes an “externally owned database/search capability”; the Domains vocabulary row calls it an “Independent external knowledge provider.” The main document, SOW-261, OI-026 and DEP-003 correctly say allocation/ownership remains TBD. In particular, SOW-249 is an affirmative ownership statement in the scope text, not merely an architectural description of a connector interface.

**Source:** full `OWNER_DIRECTIONS.md` J–L and its interpretation; `ACCEPTANCE.md` expressly distinguishes SWB’s external implementation owner, PEC’s existing project and unresolved Domains allocation. J declares the database/search capability; K establishes parallel development and subsequent integration; L establishes query → research context → design candidate → human approval. None assigns Domains construction to an external owner. The TASK no-implementation fence is not such an assignment.

**Repair:** retain the accepted Domains capability, App receiving/research duties and later timing; make these remaining ownership phrases explicitly unresolved in agreement with SOW-261/OI-026. Describe connector independence separately from provider ownership. Do not change IN receiving duties to OUT or make Domains an initial HTML-D05 gate.

### F2 — P2: Repair semantic dependency and section mappings

**Affected:** `External_Dependencies.csv` DEP-001–006 and `Source_Sections.csv`; concrete erroneous joins include SOW-115, SOW-116, SOW-151, SOW-188, SOW-199, SOW-236–241, SOW-111–113. Inspect every row, not only these examples.

The IDs exist, but several joins do not represent the stated source or dependency:

- DEP-004, written native-sign-in distribution terms, maps SOW-115 (additional essential hosts), SOW-116 (further fleet scope), and SOW-151 (Pi excluded as current host-loop dependency). Those are not contributions supplied by the sign-in-terms dependency.
- DEP-003, later Domains provider integration, maps SOW-188 (the SWB construction exclusion) and SOW-199/236–241 (the initial connected activity and outside-session coordination). Its point-of-need prose correctly says Domains is later, but these unqualified joins misleadingly make the initial activity appear dependent on Domains. Scope rows about later Domains receiving behavior/allocation do belong here; accepted connected-activity rows should be linked only with an explicit later-increment relationship if needed.
- `Source_Sections.csv` maps PRD §7 “Interfaces” to fallback replacement SOW-111–113; the cited replacement source is PRD §8 and EXAMINATION §7. PRD §1 maps SOW-097/099–101 whose principle sources are PRD §5/ARCHITECTURE §1. These are not merely cross-references within the named source section.

**Source:** original PRD §§1, 5, 7–9; original ARCHITECTURE §§6–7; HTML-D05/D06; owner K. These source locations were independently read.

**Repair:** check source-path plus section identity and the actual meaning of each dependency edge. Remove unrelated joins or qualify the relationship explicitly. Keep external points of need and fallback prose, which are mostly sound. Do not interpret an existing ID or a shared section number as evidence of a dependency. Regenerate the affected coverage evidence and verify it semantically.

### F3 — P2: Keep the conditional pre-release sign-in obligation IN

**Affected:** SOW-117, OI-007, DEP-004 and their treatment summaries/objective links.

SOW-117 marks the entire statement “Obtain the stated written sign-in distribution terms before public release beyond the owner's use” TBD. The supplier answer is unresolved, but the accepted source already identifies when it is needed. No separate IN row preserves that conditional obligation. Downstream Group 2 maps only IN items to production, so this treatment can drop the prerequisite from production coverage while retaining only an open question.

**Source:** original PRD OQ-08 says written confirmation is needed before public release; original ARCHITECTURE §8 gives “Written answers before public release (OQ-08)” as the mitigation and §6 distinguishes owner use from distribution. M accepts stated open matters and external dependencies. The workflow explicitly separates accepted scope from unknown choices.

**Repair:** preserve the conditional obligation as IN, retaining the unconfirmed answer and responsible supplier in OI-007/DEP-004. A separate TBD detail is acceptable if needed, without renumbering existing IDs. Keep future Anthropic terms conditional on a concrete future need, and do not imply this review authorizes release or requires a new approval gate.

### F4 — P2: Distinguish project-method obligations from product capability

**Affected:** `Scope_Classification.csv`, especially SOW-240, SOW-245 and SOW-257; inspect adjoining transition and adoption rows for the same issue.

These rows are classified Product even though their subjects are the conduct of the undertaking: preparing the increment’s SoW, owners and checks before execution (SOW-240); retaining agent/manager/human coordination responsibilities when PEC is absent (SOW-245); and verifying later mainline changes before relying on the pinned research (SOW-257). Their statements are source-grounded and should remain accounted for, but the classification invites later conversion into product features or software deliverables. The package already has a suitable ProjectMethodConstraint category and uses it correctly for SOW-241’s human-relayed coordination.

**Source:** HTML-D05’s “before execution” SoW instruction; HTML-D06’s absent/limited PEC allocation of work; HTML-D07’s instruction to verify later mainline. HTML’s current direction C explicitly says manual practice does not settle every practice as an App interface feature. The Group 1 brief requires this distinction.

**Repair:** reclassify the project-method/coordination obligations and review neighboring rows with the same criterion. Preserve genuinely product-facing records, presentation, connector fallback and receiving contracts as Product. This is a classification correction, not deletion of accepted work.

## Coverage and checks

I read all five original seed documents, all seven accepted HTML recommendations and full J–O, then compared the scope statements, statuses and notes with their cited sources. I checked all 136 original V4 definition mappings (PRD 56; ARCHITECTURE 13; HOST_INTEGRATION 29; EXAMINATION 20; OPERATING_METHOD 18), the seven HTML and six owner-message coverage entries, 43 source-section rows, every OUT/TBD item, ten objectives, vocabulary, 26 issue entries and six dependencies. This was source-fidelity review, not just CSV validation.

`CHECKS.json` records independently computed results. `COVERAGE_CHECKS.csv` records each original definition’s exact source location and mapped treatment. Results: 262 unique scope IDs; 223 IN, 15 OUT, 24 TBD; all definition IDs accounted for; all definition source-line and treatment summaries correct; no dangling scope references; reciprocal objective links consistent; SOW-262/SOW-263 absent and their retirement recorded; all Group 2 structural columns appropriately blank. The ten objectives are grounded and reasonable Group 1 success conditions; they do not themselves assert implementation success. Mechanical checks cannot certify the semantic joins discussed in F2.

Substantive distinctions that are correctly retained:

- Qualified parity is IN; automatic all-channel extension remains a separate open promise. Reserved-act/classifier choices remain open without permitting false human attribution.
- App/shared types, loop, components, receiving and research duties remain IN; SWB construction has an actual external session with human relay; PEC has its separate provider project. F1 identifies the remaining Domains exception to this otherwise sound boundary.
- Domains is parallel/later, not the initial connected-activity gate; Piping Designer is an application capability using the same four roles.
- Source custody/acceptance acts M/N have coverage entries without invented production scope. Retired administrative SOW IDs are not reused.
- WebKit plus Chromium interface examination is compatible with macOS-first shipping. I read original OWNER_MESSAGES M-06/M-07 and MAINTAINABILITY_ANALYSIS §11.3: future Windows-native witnesses are target-dependent. OI-015 need not be reopened as a fabricated platform conflict.
- HTML-Dxx versus CONCEPT-Dxx is disambiguated. Unselected shared-service, broad-replacement and other alternatives are not normalized as new commitments.
- Thesis/history preservation, owner governance, manual-led practice, SoW technical commitments and staged replacement are carried without an invented Root rearchitecture or current provider implementation.

## Limits and return

This finding record covers the frozen ten-file v1 only. It does not review future consolidated seed bytes, accept a structural package, verify supplier behavior, launch HX-01/E1, test an App/host, authenticate the original chat transcript, or qualify a provider/consumer. I inspected the protected-thesis preservation commitment in the candidate; I did not separately audit all imported thesis bytes or the complete 76-file donor inventory. No mutable consolidated seed was used as authority. The supporting original decision/analysis reads are lineage evidence, not newly adopted requirements.

The retained endpoint-only local-operation requirement (SOW-017/V4-HOST-02) is not weakened by Domains intent. Domains deployment/transport is not fixed here; no incompatibility or network exception should be invented from that open detail.

All four findings were sent promptly to the manager for original-author repair. Repairs require a newly identified candidate and affected source/consistency checks. Git integration later remains separate from Group 1 confirmation and downstream acceptance.
