# CC-WR-PKG-CANDIDATE-01 — pre-release workflow examination route

PROPOSED technical change to DEL-02-02 WR, with DEL-01-06 PKG receiving impact.
No canonical Design, source pin or runnable standing is changed by this proposal.
Author: Codex WORKING_ITEMS `/root/distribution_integration_manager` under
HELP_HUMAN `/root`. The parent expressly selected the conservative current
boundary after independent source assessment: candidate assets may be prepared
and checked, but cannot self-assert LS-5/LS-8 registration. This document prepares
the consequential choice; independent review and source-owner disposition remain
required before adoption. It is not a reusable workflow.

- PROPOSAL: Add an explicitly bounded candidate-examination admission alongside release registration
  - Evidence: DEL-02-02 Design/WORKSPACE_AND_REGISTRATION.md §3 (bundled workflows and shipped-revision manifest owned by the release), §4.6 LS-5/LS-8 (shipped in the App release; the release registered it), TT-1/TX-1 (only admitted standing composed), §15 U-WR-18 (integrator selects v4 shipped revisions; owner decides v3-copy recognition); DEL-01-06 Design/PACKAGING_AND_DISTRIBUTION.md §4.1 P-2 and §4.3 I-3 (candidate content is build input; absent content makes package incomplete). Independent review found no explicit public-distribution prerequisite, but also no statement granting a self-described candidate manifest registration authority.
  - Change: Through a named reviewed WR amendment, add a candidate-examination standing distinct from LS-5/LS-8. Eligibility requires an identified immutable App build and exact bundle manifest/package identities selected by the v4 contents integrator, a reviewed technical selection/adoption record naming that subject and allowed examination scope, and an explicit examiner-selected candidate route. A caller-provided manifest, boolean, filesystem match or build label alone cannot confer eligibility. The actual resolver must bind the reviewed selection to the compiled build input and actual physical package; runtime refusal precedes preparation/supply when that binding or scope is absent or inconsistent. No candidate entry becomes historical shipped content until the release owner records that exact revision as shipped. Preserve existing LS-5/LS-8 words and historical standing; extend TT-1/TX-1 explicitly only for this named bounded route, never by silently treating candidates as releases.
  - Why: Permits a real first-package pre-release workflow examination while making its authority, exact source and limits inspectable; avoids circularly requiring a completed release before examining the candidate that would be released.
  - Risk: Overbroad admission could turn any invented manifest into runnable content or bypass ordinary draft/A15 registration. The route therefore applies only to the closed reviewed candidate build set, not arbitrary local copies, and retains source/selection/current-content checks and truthful candidate status. The method does not authorize native launch, supplier execution or human acts; those still need their existing point-specific authority.
  - Status: PROPOSED

- PROPOSAL: Keep candidate inventory separate from actual shipped history and propagate the accepted route atomically
  - Evidence: WR LS-8 same-name equality, shipping-release source root and vacant unregistered slot; WD §6.1 source-qualified content identity; PKG P-2 read-only bundle and I-3 candidate completeness. Current P2 producer uses an explicit release_subject explicitly marked as a candidate and empty historical_shipped_revisions, while current runtime admits registered revisions and refuses development/candidate standing.
  - Change: Define candidate manifest semantics and the release-registration receipt in the WR amendment before implementing the candidate route. Candidate identity includes method, exact name/revision/full file-set and source commit/path identities plus build subject; actual release history is a distinct append-only reviewed input keyed by shipping-release identity. On a real release, record exact candidate-to-release correspondence and add its revisions to shipped history; a build/test pass alone cannot make that transition. Do not add v3 history unless the owner chooses U-WR-18's optional v3 recognition. Adopt amended record/parser/catalog/runtime/examination support together; old candidates and receipts retain their original scope.
  - Why: Separates current build evidence, release registration and library-copy recognition, allowing reviewers to assess each claim with its actual source.
  - Risk: Updating a manifest or consumer pin alone would assert stronger standing without corresponding authority and invalidate existing evidence. All affected consumers must reject mixed/missing bindings until the joined change is reviewed and adopted.
  - Status: PROPOSED

## Exact affected consumers and review checks

| Owner / source | Required change on adoption | Required proof |
|---|---|---|
| DEL-02-02 WR §3/§4.6/TT-1/TX-1/U-WR-18; DEL-02-01 WD §6.1 only if identity semantics change | Name candidate authority, receipt/binding and boundaries; preserve release and no-v3-default semantics | Independent source/authority review; no implied human acceptance |
| app/src-tauri/resources/production_workflows/MANIFEST.json and workflow_catalog.rs | Separate closed candidate set and evidenced shipping history; validate complete exact subject/content and no invented receipt | Wrong release/name/revision/method, duplicate/extra/missing files, edited resources, untrusted manifest and false historical entries refuse |
| workflow_workspace.rs SelectionAdmission/Selection verification; workflow_library.rs existing ledger checks | New explicitly typed candidate admission only under adopted receipt; LS-8 remains real shipped history with valid vacant slot | Recheck registry and physical content at use; registered, malformed/unreadable and orphan revision-store states refuse candidate-copy reinterpretation |
| runtime_session.rs WorkflowRootSession/run_admission/prepare/send; lib.rs native resolver/commands; App.tsx display | Examiner explicitly selects bound candidate route; ordinary candidate browsing never enables run; source and scope survive preparation/supply records | No route/receipt or mismatched build refuses before prepared records/supplier send; held-copy mutation/registration after selection refuses; candidate wording remains visible |
| Group B DEL-01-06 packaging producer and DEL-09-01/02 examination receivers | Package P-2 exact bytes/digest; bind candidate/support/route and actual authorizing examination scope; keep FP and native outcomes separate | Complete package inventory is not workflow release registration or qualification; native candidate evidence cannot become shipped-history evidence |

## Decision interface

Recommended: retain the currently enforced refusal and have WR/PKG source owners
review this narrow route as a separate named adoption before enabling it. The
alternative is to use existing genuine A15-registered copies for pre-release
examinations and defer release-bound catalog admission until the release owner
provides the required actual registration. Either route leaves P2 asset
preparation and P3 role validation independently useful. Parent coordinates
source-owner concurrence and any human product/release choice; this proposal
creates no automatic fresh owner gate for ordinary mechanical validation.

MISSING: reviewed/adopted candidate route and its exact authority-receipt contract;
actual release registration/shipping evidence for LS-5/LS-8; independent final
review of this proposal and actual producer/consumer candidate.

NEEDS_HUMAN_RULING: no new owner act is asserted as already required. HELP_HUMAN
must route any substantive product/release-policy choice exposed by source-owner
review; optional v3-copy recognition remains the owner's unselected choice.

DEPENDENCY_NOTES: P2 assets and closed validation can be received as candidate
build inputs; current candidate catalog remains non-runnable. No package
qualification, LS-5/LS-8 release standing, A-IN verification or owner acceptance
is supplied. Group B decides receiving/adoption at its actual point of need.
