# Work graph — Group B packaging and qualification

## Intent and selected route

Stable run: **APP-V4-GROUP-B-20261008**. WORKING_ITEMS `/root/group_b_manager`
owns integration under HELP_HUMAN `/root`. Current graph ref:
`codex/app-v4-group-b-offline-preparation`, now based on merged first slice
`462f66975d36cd10d5b8455193ada9517d28d353` (PR #1117); originally based on Group A closeout merge
`7b0170ed4d3f0a1a0b4b9cdb2128a60526d74af9` (PR #1116).

The owner accepted Group A's closeout and directed development of the next
Group. Exact words and relay custody are in
[OWNER_DECISIONS.md](../../AgentRuns/APP-V4-GROUP-B-20261008/OWNER_DECISIONS.md).
This activates **B — DEL-01-06, DEL-09-01, DEL-09-02** within the accepted
A → {B,C} → D → E order. It is not a 90% decision. The intended result is
usable examination support, candidate-specific macOS packaging evidence, and
a standalone qualification dossier with truthful outcomes and input gaps.
A partial or failed dossier can be useful evidence; it does not qualify an
unpassed scenario. This initial slice starts production; the whole graph remains
open until its required production, examinations and final integration occur.

Methods: `chirality-root:bundled:workflow:construct-local-work-graph` and
`chirality-root:bundled:workflow:coordinated-knowledge-work`. Source identity and
consultation evidence: [BASIS.md](../../AgentRuns/APP-V4-GROUP-B-20261008/BASIS.md).
App v4 has no software-workflow.json; App v3 procedures do not apply.

**Thin route:** M1 examination file support → a packaging evidence consumer
with exact candidate/build/pin joins and negative checks → independently reviewed
first slice. Then finish package configuration and first-package checks, receive
M2 package plus its install witness, execute M3 smoke, and carry SQ's three
joined scenarios on an identified candidate. Configuration work can advance
beside M1; M1 does not wait for M2. Native witnesses require their actual inputs
and point-specific owner authorization. No owner credentials enter agent custody.

## Deliverable scope and source reading

| Deliverable | Existing basis and production | Selected result and checks | Nodes |
|---|---|---|---|
| DEL-01-06 macOS packaging | ScopeOfWork OUT-001…004; Design PKG-v0.2, schemas and read-only prototypes. No Group B package or signing/notarisation result supplied at entry. | Configured Apple Silicon bundle, exact tree/binary/entitlement identity, actual install witness, honest unresolved terms record; VER-001…005 | B2, B4–B6, B9 |
| DEL-09-01 examination support | ScopeOfWork OUT-001…004; EXP-v0.2 result/review/change schemas, rules, native forms and route admission definitions. | Maintained offline support, fixture/replay evidence, candidate/configuration/date capture, protected criteria/reopening/review, WebKit/Chromium and native packaged support; VER-001…009 | B1, B3, B6, B7 |
| DEL-09-02 standalone qualification | ScopeOfWork OUT-001/002; SQ-v0.2, exact step map and dossier schema/prototype. Group A native journey is narrower historical evidence. | One dossier for V4-EXM-10/11/12 on one candidate, stimuli ST-1…5, native N-1, explicit missing inputs, separate examiner and DEL-11-03 handoff; VER-001…008 | B7, B8 |

Full-scope obligations stay in the source contracts. No Design, SoW, criteria,
dependency register, lifecycle or DAG amendment is made by this graph. Current
Design headers retain historical drafting labels; reviewed definitions and
later accepted decisions are read through their sources rather than rewritten.

## Work

The manager owns graph/run/shared-document writes and integration. A TASK owns
only its brief's files in its isolated worktree; reviewers are separate from
authors. Each production slice carries its necessary documentation and checks.

| ID / outcome | Deliverables, owner and write boundary | Needs / why | Completion check | State |
|---|---|---|---|---|
| G0 recover basis and executable graph | All B; manager; this graph and run only | Owner steering, Group A closeout, three SoWs/Designs/dependencies, GC-8 | Source hashes, current DAG evidence, exact decision custody, relationship account | COMPLETE entry at 7b0170ed; BASIS.md |
| B1 first usable EXP→PKG file path (partial M1) | DEL-09-01 OUT-002/003 + DEL-01-06 OUT-002; support_production TASK; new app/examination or scoped tools, group_b tests and production evidence only | EXP/PKG canonical schemas/rules; identified App source candidate; no native input needed | Offline CLI checks canonical shapes and rules; exact candidate/build/pin/support joins; false-pass negatives; candidate-bound technical artifact with honest limits | COMPLETE bounded partial M1 at author 703f834e0d; ten tests and independent V1 checks pass; merged into manager branch only; production/SUPPORT_CHECK.json |
| V1 independent first-slice review/repair | B1 plus graph integration; separate TASK, review files only | Frozen B1 revision | Source fidelity, false-pass probes, no contract weakening, actual output and complete diff reviewed; author repairs and reviewer confirms | COMPLETE V1 READY on combined 949e0d84a7; no actionable findings; reviews/V1-FIRST-SLICE.md |
| P1 first substantive integration | Manager/HELP_HUMAN; B1, graph, checks and slice documentation | V1 READY and actual candidate checks | PR with graph and implementation; required CI; merge coordinated with HELP_HUMAN | COMPLETE PR #1117 merged at 462f66975d; parent-coordinated exact-head review and CI retained in PR |
| B2 unsigned package configuration and inventory | DEL-01-06 OUT-001/002; packaging TASK, app packaging files and PKG evidence assigned before dispatch | Group A App source/pin, complete approved vendor tree, current WR/ROLE bundle inputs | CF-1…8 represented without credentials; P-0…4 layout; FP-0 at selected pin; FP-1(a) actual tree/mode/link comparison; missing content marks incomplete | ACTIVE offline inventory/staging increment in package-prep TASK; explicit inputs and incomplete state retained |
| A-IN full distribution verification receiving | DEL-01-01 owning Group A follow-up; HELP_HUMAN coordinates; B manager receives only | Before FP-2/W-4, actual expected full-tree identity and runtime verification/launcher contribution | Reviewed implementation produces verified standing for exact packaged tree; development digest exception never satisfies this | ACTIVE receiving investigation recorded in distribution_input/PROPOSAL.md; CC-HOSTING-DISTRIBUTION-01 separately commissioned by HELP_HUMAN; implementation/qualified identity pending |
| B3 finish reusable support and route admission | DEL-09-01 OUT-001…004; examination TASK, maintained fixtures/adapters and EXP evidence | B1; identified recordings and installed runner engines; route configuration | Resolve CI-26 full support identity representation through owning Design review; EXP-VC-01…15 relevant checks; five outcomes, actor separation negatives, review/change/criteria checks; EXP-DC-RUNNER WebKit/Chromium sensitivity/isolation; N-1 form; N-2 only if separately admitted | PLANNED; absent recordings/engines stay named gaps, no downloads presumed |
| B4 first-package signing/notary decision package | DEL-01-06; packaging owner prepares exact candidate/configuration/commands and FP record; owner performs account acts | B2 unsigned package + FP-0/FP-1(a); actual App identity/minimum OS chosen; owner point-specific action | Reviewable signing/notarisation subject and consequences; no credential in records; no signature or notary claim before action | PLANNED; owner act needed only at signing/notarisation point |
| B5 signed package identity and Option B reliance | DEL-01-06 OUT-002; packaging owner/owner act, PKG evidence | B4 execution; unchanged supplier tree and full signatures | FP-1(b), FP-3 pass before Option B reliance; outer deep-strict and Gatekeeper evidence; PK-R1…9; no fallback without cause/CS-1…4 and HELP_HUMAN Design route | PLANNED; SIGN-1 B accepted for design, reliance unestablished |
| B6 M2 install witness and M3 packaged smoke | DEL-01-06 OUT-003 and DEL-09-01 OUT-004; respective examiners, evidence only | B3 support, B5 package, A-IN verification, quarantine and point-specific native authorization | PKG W-0…6/FP-2/4/5 with WKWebView/config/date; separate EXP native packaged smoke citing same package/support; Gatekeeper refusal is fail, absent unattempted package is not-run | PLANNED; no package/native act supplied |
| B7 standalone candidate and case preparation | DEL-09-02; workflow integration owner with examiner; SQ fixtures/case definitions/evidence | Group A applicable feature evidence; B1/B3 support; selected candidate/configuration; package optional under SQ I-6 | Exact SQ step map; pre-run ST-1…5 and tool-request setting; identify missing supplier inputs; candidate and case-definition hashes; neither historical native pass nor component test substitutes | PARTIAL implementation f7dc413074 independently READY at preparation-only scope; nine tests; CC-SQ-J2-ST4 source correction pending; examination unopened |
| B8 joined V4-EXM-10/11/12 and dossier | DEL-09-02; independent candidate examiner, SQ evidence | B7 ready inputs, N-1 owner acts authorized, ST-5 real recorded counterpart, ST-4 route or counterpart, three usable modes | Two registered refinements; S11 inside RUN-A; same candidate RUN-B; three distinct conversations/modes; EXP and SQ rules; separate review; handoff to DEL-11-03 with disclaimers | PLANNED; any missing contribution remains explicit, no substitute-mode pass |
| B9 supplier terms record | DEL-01-06 OUT-004; packaging recorder; owner/supplier acts external to agent | Existing OI-007 at release point; response only when supplied | Unresolved record until actual written response/custody; actor distinct from recorder; public distribution decision separate | READY for unresolved record; receipt is not a current development prerequisite |
| CC-SQ-J2-ST4 source correction | DEL-09-02 Design owner sq_st4_design; Design and named change packet only | Existing J-2 prose and ST-4 staged_at conflict with J-2 map stimuli | Minimal unchanged-intent correction independently reviewed; source locks/examples/preparation regenerated; no examination pass | ACTIVE bounded Design TASK; no silent source amendment |
| V2 offline B2/B7 review and integration | Separate TASK reviewer; manager integrates; bounded preparation code/tests and run evidence | Frozen B2/B7 source candidate | Source-faithful cases, actual input inventory and negative checks; no fabricated readiness/native evidence; independent review and P2 PR/CI | ACTIVE; B7 preliminary READY; B2 F1 relative-path containment defect routed to author before fan-in |
| C1 final bounded reconciliation | All B; manager; affected records within granted scope | Intended production/evidence integrated | bundled:bounded-reconciliation; both directions against three SoWs; required missing work returns to graph; only no-home material concern invokes task-management | PLANNED, single final stage |
| M1 central receipt and MEMORY | All B; manager; AgentRuns receipt and three MEMORY entries | C1 | One concise result/check/limit receipt and terse local pointers, no status inflation | PLANNED |
| F1 final PR | HELP_HUMAN coordinates merge; manager prepares | All required nodes/decisions, final independent review and required CI | Actual final PR merge establishes undertaking completion, never product/gate acceptance | PLANNED |

Executable node dependencies are acyclic: G0→B1→V1→P1;
G0→B2→B4→B5→B6; B1→B3→B6; G0+B1+B3→B7→B8;
G0→B9; intended production integrations→C1→M1→F1. B4's owner-act boundary
is not an extra stop on B1/B2/B3/B7/B9.

## Relationships and readiness (GC-8)

Entry inventory found only the Group A development graph; no B/C/D/E development
graph existed. All WorkGraphs were searched for B identifiers and Group B;
Group A's relationships below are carried here. Historical definition/design
and graph-closure graphs remain at their original paths.

- **Accepted DAG:** DAG-004, latest currency CURRENT_WITH_EVIDENCE_DRIFT;
  no deliverable DAG pending. Entry hash check of 130 source-manifest members
  found only the same two DEL-01-03 TargetLocation-repair files as that audit.
  Registers' TBD/PENDING are not satisfied by this graph. Read both
  DEP-09-01-019 and its DEL-01-01-031 mirror where maturity differs.
- **Within B, SCC-003:** held DEP-09-01-021/016 retain their non-gating
  standing. EXP §10's actual contributions order M1 support, M2 package plus
  identity and install witness, then M3 smoke. A held arc is not a held case.
- **B consumes A:** stock pin/tree/hosting (DEL-01-01), account inputs
  (DEL-01-05), SQ feature joins (DEL-01-02/03/04, DEL-02-01/02/03,
  DEL-04-01/03); D04/U05/U06 retain AAC key-store/signing input and WR/ROLE
  bundle-content relations. Their current bytes must be checked when used;
  old Design pins do not automatically adopt later changes. CP0 receiving
  notices remain adoption work. Group A C1 and CI-19…25 do not establish all
  inputs. B2/B7 check the particular contribution before relying on it.
- **A consumes B:** existing DEP-09-09-012 (external trace uses EXP) is the
  accepted acyclic exception to group order; protocol definition exists but
  candidate qualification remains unclaimed. O-1's A–B cycle/P16 cut and held
  rows retain their recorded standing. No new reverse relationship is added.
- **C:** U10 optional B→C rehearsal remains optional and unselected. No
  connector, PEC or Domains completion is a standalone starting condition.
  Carry this relation into C's graph when constructed.
- **D/E consume B:** EXP supplies DEL-09-05/06/07/10/11 (D), DEL-09-12 (E),
  and SQ supplies DEL-11-03 (E). Each receiver owns its journey/adoption.
  Carry these relationships into their graphs at entry; no new standing list.
- New order reversal, cross-group cycle, deliverable change, or invalidation
  of another group's finished work goes immediately through HELP_HUMAN to the
  owner under GC-7. Ordinary input gaps do not imply those conditions.

## Current state and recovery

Current continuation source candidate: 462f66975d (fresh fetched origin/main; new branch, clean at entry). Initial source candidate was 7b0170ed. Graph maintainer: group_b_manager.
Manager worktree: `/Users/ryan/.codex/worktrees/app-v4-group-b-implementation/chirality`.
B1/P1 are integrated. B2 owner support_production uses the existing isolated
app-v4-group-b-support worktree on new branch codex/app-v4-group-b-package-prep
from 462f66975d. B7 owner standalone_preparation uses its own
app-v4-group-b-case-prep worktree and branch, also from 462f66975d. Both are
TASK descendants using requested gpt-6-astra/low; no shared files are delegated.
Manager owns graph, shared documentation, coordination and integration.
Actual native-descendant mechanism, model request, supplied basis, write fences
and returns are recorded in [DELEGATION.md](../../AgentRuns/APP-V4-GROUP-B-20261008/DELEGATION.md).

B2 entry technical inspection is retained in [PACKAGE_INPUT_ACCOUNT.md](../../AgentRuns/APP-V4-GROUP-B-20261008/PACKAGE_INPUT_ACCOUNT.md): bundling is disabled in the current source, production resource placement remains unsupplied, and HOSTING only provides labelled development identity. HELP_HUMAN retains coordination of the known DEL-01-01 full-distribution verification input at FP-2/W-4.

**Next:** finish bounded B2 inventory/unsigned preparation and B7 standalone
case preparation, freeze their candidate and obtain V2 independent review before
P2 integration. Candidate values and actual supplier load-command inspection are
in [CANDIDATE_VALUES.md](../../AgentRuns/APP-V4-GROUP-B-20261008/offline-preparation/CANDIDATE_VALUES.md).
15.0 and dev.chirality.app-v4 are candidate recommendations, not a durable signed
identity or runtime compatibility claim. The manager returns exact reviewed HEAD
to HELP_HUMAN for PR/CI/main merge. Native launch, signing/notarization, downloads,
credentials, SEAL-2 and human acts stay outside this slice.

**Carried limits:** SEAL-2 cold native-origin proof remains owner-deferred in
Group A I3-CUST and CI-10; B does not complete or silently implement it. Its
key-store entitlement/profile consequence is assessed only once that feature is
implemented. CI-11 positive user verification, child-role/native item limits,
CI-19/20/21/24/25 Design questions and CI-23 prototype failure retain their
source owners. Group A's native Cancel/A16/request/file-act and broader provider
witness gaps remain evidence gaps. SQ's ST-5 real capture, conditional ST-4
counterpart, account/API/local mode configuration and point-specific person acts
remain B7/B8 inputs. Signing architecture SIGN-1 is decided for App design;
OI-011 SWB part and next amendment remain open. OI-007 supplier terms gate public
release beyond owner use, not this development. No lifecycle or 90% act follows.


## First-slice integration evidence

Author `fc027ae116` implementation plus `703f834e0d` evidence is integrated in
the manager branch. [Production return](../../AgentRuns/APP-V4-GROUP-B-20261008/production/RETURN.md)
and [technical check](../../AgentRuns/APP-V4-GROUP-B-20261008/production/SUPPORT_CHECK.json)
retain original candidate identities and limits. The examiner independently ran
ten tests, compared semantic-rule functions to their pinned sources, and checked
additional mismatch/reopening cases and evidence hashes. No native result is
supplied. Final combined review is READY in [V1-FIRST-SLICE.md](../../AgentRuns/APP-V4-GROUP-B-20261008/reviews/V1-FIRST-SLICE.md); P1 merged as PR #1117 at 462f66975d; B2/B7 continuation remains open. C1/M1/F1 are not
performed merely because this first slice is useful; no final receipt or MEMORY
closure entry is created at this checkpoint.
