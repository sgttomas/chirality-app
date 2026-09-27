# Chirality App v4 — Group2 structural proposal

**Standing: GROUP1_CONFIRMED / GROUP2_PROPOSED. Revision G2-draft-2-clarification, 2026-09-27.** Package role: working surface. No Group2 acceptance, Group3 audit, production setup or implementation is claimed.

## Accepted basis and current subject

Group1 was actually confirmed through the question and answer in [DECISION.md](checkpoint_snapshots/GROUP1-20260927T222641Z/DECISION.md). Resolve the [accepted pointer](checkpoint_snapshots/_LATEST_GROUP1.md), manifest and handoff before this proposal. Its fourteen frozen subject/evidence copies retain the exact presented bytes, including historical draft labels and relative links; those labels do not reverse the decision.

That snapshot binds APP-V4-BASIS-20260926, the accepted clarification, all 262 stable ScopeItemIDs (234 IN / 15 OUT / 13 TBD), vocabulary and ten objectives. Original seed/composite/thesis and earlier candidates are unchanged. The selected method remains chirality-root:bundled:workflow:software-decomp. Current Package and Deliverable mappings are proposals derived from the accepted Group1 meaning, not new product scope.

## Proposed flat work domains

| Package | Cohesive work domain | Deliverables | Scope IN / OUT / TBD |
|---|---|---:|---:|
| PKG-01 | Native App and third-party harness integration | 6 | 41 / 10 / 0 |
| PKG-02 | Workflow and role portability | 4 | 29 / 1 / 0 |
| PKG-03 | Host capability and operation contracts | 4 | 35 / 1 / 1 |
| PKG-04 | Human acts, autonomy and run evidence | 3 | 19 / 0 / 2 |
| PKG-05 | Embedded-host receiving integration | 2 | 13 / 2 / 0 |
| PKG-06 | File-based fleet coordination | 2 | 8 / 0 / 1 |
| PKG-07 | PEC receiving and connector fallback | 2 | 13 / 1 / 0 |
| PKG-08 | Domains research receiving | 2 | 7 / 0 / 1 |
| PKG-09 | Candidate examination and connected journeys | 9 | 34 / 0 / 3 |
| PKG-10 | Project definition and manual-led practice | 4 | 22 / 0 / 3 |
| PKG-11 | Adoption and replacement continuity | 3 | 13 / 0 / 2 |

[Packages.csv](Packages.csv) gives each domain's contribution, inclusion criteria and exclusions. [Deliverables.csv](Deliverables.csv) specifies 41 bounded outputs, proposed responsibility, anticipated artifacts, receiving interfaces, local verification and context envelope. These are functional responsibilities carried through the four standing roles, not a new role roster, personal assignments or accepted external commitments. PhaseHint values are nonbinding definition/dependency guidance; Packages are not phases.

[ScopeLedger.csv](ScopeLedger.csv) gives each IN/OUT/TBD item exactly one accountable Package home. Only IN items map to Deliverables. [Allocation_Rationale.csv](Allocation_Rationale.csv) explains the homes; cross-package supporting contributions do not create second homes. Accepted scope statements, statuses, source references, objective links and open matters are preserved. The [objectives](Objectives.csv) now have proposed Deliverable mappings; their substantive statements remain accepted Group1 content.

## Integration ownership and critical interfaces

| Joined result | Integration owner in the proposal | Inputs and independent/joined examination |
|---|---|---|
| Complete standalone create–execute–save/review–reuse–refine loop | DEL-02-02 | Native supplier/session/UI contributions DEL-01-01..05; portable declarations/checkpoints DEL-02-01/03; act/evidence DEL-04-03. DEL-09-02 qualifies the identified candidate across workflow, recovery and all three access scenarios. |
| First connected host activity and App/host workflow round trip | DEL-09-06 | PKG-02 methods, PKG-03 catalog/proposal/external-access contracts, PKG-04 acts/records, PKG-05 receiving and actual external SWB contributions. DEL-09-07 qualifies the local host activity; DEL-09-09 examines external control and extension traces. |
| Fleet coordination across returned work and decisions | DEL-06-02 with DEL-06-01 source records | Native child identities and PKG-04 actual acts; DEL-09-05 joins the recovery witness. Product work graphs remain distinct from DEL-10-04's project production DAG. |
| Optional coordination/knowledge consumption | DEL-07-01 and DEL-08-01/02, independently | Providers retain publication/construction responsibilities; DEL-07-02 supplies an independently applicable fallback pattern, not a PEC runtime prerequisite for Domains. DEL-09-10 tests combined limited/absent states. |
| Adoption and replacement decision | DEL-11-02/03 | Examined candidate evidence plus DEL-11-01 continuing-obligation/preservation account; receiving owners adopt, and the human makes the replacement decision. |

These are proposed contribution/interface paths, not an accepted DAG or schedule. Feature Deliverables retain their own criteria and checks. PKG-09 owns reusable examination support and joined candidate evidence, not all testing or a late-phase substitute for local proof. Actual dependency records and the accepted project DAG follow accepted decomposition/local SoWs and selected setup choices.

## Five boundary recommendations and qualifications

1. Keep native App/supplier behavior and the workflow workspace separate, with DEL-02-02 accountable for the complete standalone result. Conditional legacy reuse remains optional.
2. Keep portable method meaning, host operation meaning, attributable acts and embedded receiving explicit. SOW-019/136/144 remain included receiving/conformance responsibilities; SWB owns host-specific construction and internals. Common implementation needs an agreed repeated responsibility and allocation, not merely the word shared.
3. Keep PEC and Domains homes independent. PEC construction remains OUT; Domains provider allocation stays TBD. Qualified product PEC consumption remains within its released/adopted envelope; preparing the contract and fixtures does not require that envelope already to exist. No provider, data destination, token, wire format or readiness is invented.
4. Use one standalone qualification dossier and one local host qualification packet, retaining their named scenarios as task-sized cases. Unaccepted draft IDs DEL-09-03, DEL-09-04 and DEL-09-08 were retired into DEL-09-02 and DEL-09-07; no ID was reused or other unit renumbered. DEL-09-09 remains distinct because external-control recovery and the extension-claim trace use a different receiving boundary.
5. Keep project definition/practice and adoption/continuity as concrete named-reader outputs. The 42 method constraints qualify coherent results, not one Deliverable per rule or copied manuals. File-native undertaking controls work before PKG-06 product support. The project DAG may represent pending external contributions; delivered PEC/SWB capability is not a prerequisite to honestly defining it. Shared renewal is confined to accepted responsibilities and consumer effects, not directory rearchitecture.

## Implementation approach

The [scoped owner clarification](../_Coordination/Changes/APP-V4-IMPLEMENTATION-CLARIFICATION-20260927.md) confirms Codex is sufficient initially and explains implementation sourcing. PKG-01 owns native App integration of the stock third-party harness, including Codex-native OAuth/sign-in in DEL-01-05; it is not a new Chirality App agent engine. “Owned” identifies behavior, receiving-contract fit and maintenance responsibility, not mandatory original authorship.

Assess relevant Pi, T3 Code, v3 and other exemplars and selectively reuse/adapt suitable components or patterns against the receiving contract. Preserve significant source/version/attribution and adaptation rationale in existing SoW/PR records, then qualify the actual code/versions and applicable reuse terms. The retained dated reports locate candidates; they do not certify present fitness or licensing. No dedicated research Package, per-row checklist, mandatory copy, whole-application fork or generic multi-harness gateway is introduced. Pi runtime adoption remains a distinct architecture choice; minimal-host receiving, external construction and conditional shared allocation stay as accepted.

## Coverage, context and carried decisions

[Coverage_Telemetry.json](Coverage_Telemetry.json) records actual stage checks. Proposed counts: 262 scope items; 11 Packages; 41 Deliverables; 10 objectives; no unassigned scope, no IN item without production mapping, no OUT/TBD production mapping, no unmapped objective. Envelopes:2 S /31 M /8 L /0 XL.

The eight L units are DEL-01-01, DEL-01-02, DEL-02-02, DEL-09-01, DEL-09-02, DEL-09-06, DEL-09-07 and DEL-09-09. [ContextBudgetQA.csv](ContextBudgetQA.csv) explains their coupled state or joined proof context, the work already split out and the required boundary control. Recommend retaining them with those qualifications; reassess when local SoW detail supplies actual implementation context. No XL exception is requested. Size labels are context judgments, not file-count promises or fixed model limits.

[Open_Issues.csv](Open_Issues.csv) retains the exact policy, extension, technical means, extra host/fleet, validation-period, provider-allocation and adoption matters with their points of need. OI-025's earlier stage-deferral is mechanically answered by this proposed all-objective mapping; its structural standing follows the actual Group2 decision. No carried substantive value is silently decided.

The [workflow](../_Coordination/WORKFLOW_UPSTREAM_COMPARISON_2026-09-27.md) and [PEC](../_Coordination/PEC_UPSTREAM_COMPARISON_2026-09-27.md) comparisons remain bounded source accounts. At integration base 7e0125a7, PEC TM1 has recorded its future consumer-contract consideration, hosted-CI notice and deferred K3 publication. No provider PRD/source/API/profile change or newly delivered domain-engine contract was supplied by that cleanup. SCA-APP-012's owning derivative work and future relevant provider inputs remain separate; only a material changed warrant reopens affected preparation.

## Checkpoint and next stage

The [Group2 reader](../_Coordination/Reviews/APP-V4-GROUP2-20260927-CANDIDATE-2/READER.md) and manifest identify this proposal for confirmation or correction, including coverage findings and context/boundary qualifications. Its [independent review](../_Coordination/Reviews/APP-V4-GROUP2-20260927-CANDIDATE-2/REVIEW.md) carries the actual-candidate verdict.

Only after the human confirms Group2 will its immutable snapshot/pointer be written. Group3 then assembles the accepted decisions and receives its separate independent final audit and human acceptance before downstream setup. Existing owner authorization carries the undertaking forward through those real checkpoints; routine Git integration does not replace them.

[Companion_Inventory.csv](Companion_Inventory.csv) identifies each working/register/check surface and its reader. No production Package/Deliverable folders or local ScopeOfWork contracts are created by this structural proposal.
