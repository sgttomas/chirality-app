# Work graph — Group B packaging and qualification

## Intent and selected route

Stable run: **APP-V4-GROUP-B-20261008**. WORKING_ITEMS `/root/group_b_manager`
owns integration under HELP_HUMAN `/root`. Current graph ref:
`codex/app-v4-group-b-next-production`, based on current main
`f2e7a2a9ff3ba4e6f5dd0f726766961c8dba1ce1`. Owner steering: “resume work on App v4”,
relayed by HELP_HUMAN in the active chat. Accepted Group A closeout still governs;
this is no 90% act. No MEMORY writes under the owner's later instruction.

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
| B1 first usable EXP→PKG file path (partial M1) | DEL-09-01 OUT-002/003 + DEL-01-06 OUT-002; support_production TASK; new app/examination or scoped tools, group_b tests and production evidence only | EXP/PKG canonical schemas/rules; identified App source candidate; no native input needed | Offline CLI checks canonical shapes and rules; exact candidate/build/pin/support joins; false-pass negatives; candidate-bound technical artifact with honest limits | COMPLETE bounded partial M1 at author 703f834e0d; ten tests and independent V1 checks pass; merged in PR #1117; production/SUPPORT_CHECK.json |
| V1 independent first-slice review/repair | B1 plus graph integration; separate TASK, review files only | Frozen B1 revision | Source fidelity, false-pass probes, no contract weakening, actual output and complete diff reviewed; author repairs and reviewer confirms | COMPLETE V1 READY on combined 949e0d84a7; no actionable findings; reviews/V1-FIRST-SLICE.md |
| P1 first substantive integration | Manager/HELP_HUMAN; B1, graph, checks and slice documentation | V1 READY and actual candidate checks | PR with graph and implementation; required CI; merge coordinated with HELP_HUMAN | COMPLETE PR #1117 merged at 462f66975d; parent-coordinated exact-head review and CI retained in PR |
| B2 unsigned package configuration and inventory | DEL-01-06 OUT-001/002; packaging TASK, app packaging files and PKG evidence assigned before dispatch | Group A App source/pin, complete approved vendor tree, current WR/ROLE bundle inputs | CF-1…8 represented without credentials; P-0…4 layout; FP-0 at selected pin; FP-1(a) actual tree/mode/link comparison; missing content marks incomplete | PARTIAL reviewed e8c98c423 inventory/staging increment integrated;16 tests; actual42-file staging; no App package |
| A-IN full distribution verification receiving | DEL-01-01 owning Group A follow-up; HELP_HUMAN coordinates; B manager receives only | Before FP-2/W-4, actual expected full-tree identity and runtime verification/launcher contribution | Reviewed implementation produces verified standing for exact packaged tree; development digest exception never satisfies this | OPEN; CC-HOSTING-DISTRIBUTION-01 proposed successor staged with current accepted consumer basis preserved; A-IN-S1…S5 below retain implementation/qualified-reference work |
| B3 finish reusable support and route admission | DEL-09-01 OUT-001…004; examination TASK, maintained fixtures/adapters and EXP evidence | B1; identified recordings and installed runner engines; route configuration | Resolve CI-26 full support identity representation through owning Design review; EXP-VC-01…15 relevant checks; five outcomes, actor separation negatives, review/change/criteria checks; EXP-DC-RUNNER WebKit/Chromium sensitivity/isolation; N-1 form; N-2 only if separately admitted | PARTIAL review/change support merged PR #1121, 51 combined tests; next B3-N1 below; CI-26 and actual route admission remain open |
| B4 first-package signing/notary decision package | DEL-01-06; packaging owner prepares exact candidate/configuration/commands and FP record; owner performs account acts | B2 unsigned package + FP-0/FP-1(a); actual App identity/minimum OS chosen; owner point-specific action | Reviewable signing/notarisation subject and consequences; no credential in records; no signature or notary claim before action | PLANNED; owner act needed only at signing/notarisation point |
| B5 signed package identity and Option B reliance | DEL-01-06 OUT-002; packaging owner/owner act, PKG evidence | B4 execution; unchanged supplier tree and full signatures | FP-1(b), FP-3 pass before Option B reliance; outer deep-strict and Gatekeeper evidence; PK-R1…9; no fallback without cause/CS-1…4 and HELP_HUMAN Design route | PLANNED; SIGN-1 B accepted for design, reliance unestablished |
| B6 M2 install witness and M3 packaged smoke | DEL-01-06 OUT-003 and DEL-09-01 OUT-004; respective examiners, evidence only | B3 support, B5 package, A-IN verification, quarantine and point-specific native authorization | PKG W-0…6/FP-2/4/5 with WKWebView/config/date; separate EXP native packaged smoke citing same package/support; Gatekeeper refusal is fail, absent unattempted package is not-run | PLANNED; no package/native act supplied |
| B7 standalone candidate and case preparation | DEL-09-02; workflow integration owner with examiner; SQ fixtures/case definitions/evidence | Group A applicable feature evidence; B1/B3 support; selected candidate/configuration; package optional under SQ I-6 | Exact SQ step map; pre-run ST-1…5 and tool-request setting; identify missing supplier inputs; candidate and case-definition hashes; neither historical native pass nor component test substitutes | PARTIAL source-bound preparation and CC-SQ-J2-ST4 merged PR #1119; next B7-FX below; examination unopened |
| B8 joined V4-EXM-10/11/12 and dossier | DEL-09-02; independent candidate examiner, SQ evidence | B7 ready inputs, N-1 owner acts authorized, ST-5 real recorded counterpart, ST-4 route or counterpart, three usable modes | Two registered refinements; S11 inside RUN-A; same candidate RUN-B; three distinct conversations/modes; EXP and SQ rules; separate review; handoff to DEL-11-03 with disclaimers | PLANNED; any missing contribution remains explicit, no substitute-mode pass |
| B9 supplier terms record | DEL-01-06 OUT-004; packaging recorder; owner/supplier acts external to agent | Existing OI-007 at release point; response only when supplied | Unresolved record until actual written response/custody; actor distinct from recorder; public distribution decision separate | READY for unresolved record; receipt is not a current development prerequisite |
| CC-SQ-J2-ST4 source correction | DEL-09-02 Design owner sq_st4_design; Design and named change packet only | Existing J-2 prose and ST-4 staged_at conflict with J-2 map stimuli | Minimal unchanged-intent correction independently reviewed; source locks/examples/preparation regenerated; no examination pass | COMPLETE reviewed faithful correction b66d0b16f2 integrated d6bcee8ce6; B7 consumer8d05714c84; CI-28; reviewed and merged PR #1119 |
| V2 offline B2/B7 review and integration | Separate TASK reviewer; manager integrates; bounded preparation code/tests and run evidence | Frozen B2/B7 source candidate | Source-faithful cases, actual input inventory and negative checks; no fabricated readiness/native evidence; independent review and P2 PR/CI | COMPLETE PR #1119; 35 integrated tests and 119 definition checks; narrow preparation standing |
| B2-U unsigned Tauri candidate route | DEL-01-06; bounded TASK sq_st4_design; new packaging/unsigned and tests/evidence, existing config changes require exact fence | Current accepted PKG P0-4/CF; cached Tauri/Rust/npm; actual candidate/resource inputs | Concrete config/build route; build incomplete unsigned bundle if permitted without auto-signing, or precise blocked operation/input; distinguish P1 staging from App bundle | ACTIVE; no signing/native execution; P2/P3 gaps explicit |
| B7-FX usable invented workflow fixtures and real consumer checks | DEL-09-02/DEL-09-01; standalone_preparation TASK; new standalone fixtures and group_b_fixture tests; exact cfg(test) module declaration in lib.rs | Accepted SQ/WD/WR/EXEC; actual maintained Rust parser/review/snapshot path | Invented workflow/collision inputs pass real consumer, meaningful negatives; no registration/act/native stimulus fabricated | ACTIVE from current main; no duplicate validator |
| B3-N1 usable blank native-step forms | DEL-09-01/DEL-09-02; support_production TASK; new native_forms and group_b_native_forms tests | EXP §8.2, current source-bound B7 prep and SQ steps | Actual prep→ordered form path, blank unobserved fields and explicit no-examination standing; meaningful mismatch tests | ACTIVE; N-1 execution unrun |
| V4 integrated consuming-path review | Separate reviewer first_slice_review; manager fan-in | Frozen B7-FX/B3-N1 code/evidence, current main | Independent contract/consumer review, affected integration tests, private-term checks and parent PR | PLANNED after frozen contributions |
| C1 final bounded reconciliation | All B; manager; affected records within granted scope | Intended production/evidence integrated | bundled:bounded-reconciliation; both directions against three SoWs; required missing work returns to graph; only no-home material concern invokes task-management | PLANNED, single final stage |
| M1 central receipt | All B; manager; AgentRuns receipt only | C1 | Concise result/check/limit receipt; no MEMORY writes under current owner direction | PLANNED |
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

Current source: f2e7a2a9ff. PR #1117 supplied partial EXP→PKG support;
#1119 supplied unsigned supplier staging and source-bound standalone preparation;
#1121 supplied review/change-impact joins; #1122 preserved accepted contracts and
staged the A-IN successor proposal. Their reviews and limits remain in the run.
Prior graph checkpoints are retained in [resumed-production/PRIOR_GRAPH.md](../../AgentRuns/APP-V4-GROUP-B-20261008/resumed-production/PRIOR_GRAPH.md), not current next steps.

**Next:** finish B2-U, B7-FX and B3-N1 through their actual consumers, independently
review and integrate. These are disjoint from HELP_HUMAN's separately assigned
A-IN-S1 design owner. Accepted HOSTING/PKG/EXP/SQ pins remain authoritative;
no bare hash repin. B2 full package progression requires actual resource/config
inputs and the A-IN route below; the existing 42-file staging is not an App
package. Candidate values remain 15.0 and dev.chirality.app-v4, with no durable
signed identity or native App compatibility established.

**Carried limits:** CI-26 complete M1 identity, CI-27 full distribution identity,
SEAL-2 cold native-origin proof (Group A I3-CUST/CI-10), Group A CI-11 and
CI-19…25 receiving matters, ST-4 usable route/recording, ST-5 real candidate-pin
capture, account/API/local modes and native/person inputs remain open. SIGN-1
Option B is accepted design; reliance waits FP-1(a/b)/FP-3. OI-011 SWB portion
and OI-007 public-distribution terms retain their owners/points of need. No
credentials, downloads, native launch/acts, signing/notarisation or MEMORY writes.

**DEL-11-03 receiving notice:** CC-SQ-J2-ST4 was faithfully corrected and
reviewed in #1119. Group E's owner must assess its pinned SQ prose/example
identities before reliance. Historical fixtures remain frozen; existing actual
dossiers require examiner EXP §6.2 impact assessment. No automatic adoption.

Actual delegation, bases and limits are in [DELEGATION.md](../../AgentRuns/APP-V4-GROUP-B-20261008/DELEGATION.md); this manager owns graph and integration.

## A-IN receiving continuation — CC-HOSTING-DISTRIBUTION-01

Receiving increment owned by WORKING_ITEMS `/root/distribution_integration_manager`
under HELP_HUMAN, branch `codex/app-v4-distribution-integration`; current Group B
manager retains the rest of this graph. [Integration disposition](../../AgentRuns/APP-V4-GROUP-B-20261008/distribution_integration/INTEGRATION.md)
records the named staged route. The in-place Design candidate `4c5f691c82` did
not preserve runnable source-pinned consumers. Accepted HOSTING/PKG bytes remain
at their existing paths; the base-bound `distribution_integration/stage/PROPOSED_DESIGN.patch`
and concise DISTRIBUTION_IDENTITY proposal retain the full proposed amendment. Source locks and freshness refusals are unchanged. Current B2/B7 remain
preparation only. A-IN is not complete, CI-27 stays open, and this is no method
adoption, qualified expected reference, FP-2/W-4 or Group B completion.

| ID / output | Accountable owner and write boundary | Concrete inputs / prerequisites | Completion evidence / state |
|---|---|---|---|
| A-IN-S1 coherent versioned successor contracts | DEL-01-01 + DEL-01-06 Design owners, HELP_HUMAN coordinates; respective Design schemas/prototypes/examples | Proposed HOSTING/PKG successors, DISTRIBUTION_IDENTITY method, reviewed inventory model, current lifecycle/PKG v0.2 contracts | Full expected/observed reference and lifecycle successor, immutable exact-byte verification reference, PKG successor and PK-R1 rules, historical-version handling; independently reviewed named adoption with complete consumer plan. OPEN, ready for bounded offline implementation assignment; no qualified record minted |
| A-IN-S2 connected runtime and packaging implementation | Group A DEL-01-01 implementation owner with DEL-01-06 packaging owner; hosting/resolver/launcher/lifecycle and packaging code/tests under coordinated fence | S1 reviewed contracts; native resource configuration and generated identity references; synthetic expected-reference doubles | No-follow complete scanner, generation/custody/refusal, resolver→verifier→probe→launcher chain, direct PATH convention, immutable record resolver, packaging successor output; negative/mutation and joined offline checks, independent review. OPEN; production verified standing awaits S3 |
| A-IN-S3 qualified supplier-reference artifact | DEL-01-01 qualification owner through HELP_HUMAN; exact supplier-reference evidence and adoption record | S1/S2 method, actual archive source/digest/acquisition authorization and extraction custody, pin/platform, maintained generated-output identity, passed version-advance evidence; separately authorized isolated label probe | Independently checked complete reference bytes/digest and technical adoption bound to reviewed App build; no observation promoted to expectation. OPEN; missing acquisition/generation/probe evidence stays missing; downloads/credentials/probe execution need existing authority |
| A-IN-S4 examination and standalone receiving joins | Group B DEL-09-01/02 owners with DEL-01-06; consumer code/fixtures/manifests and named adoption notice | S1/S2 successor artifacts plus S3 for verified claims; current EXP/SQ exact candidate/package/support contracts | Reject mixed versions, unresolved/missing expected references and false verified claims; immutable full-artifact digest resolution, exact package/candidate/support joins; affected regressions and independent review. OPEN; legacy/preparation consumers retain accepted basis until atomic adoption |
| A-IN-S5 package witness and downstream reliance | Group B packaging/examiners; B5/B6 evidence; HELP_HUMAN coordinates owner acts | S2/S3/S4, actual candidate/package/support, FP-0/1(a)/1(b)/3 and permitted native/install actions | Actual FP-2/W-4 runtime evidence joins exact package/reference; Option B and EXP/SQ criteria maintained. OPEN, no synthetic substitution; B4/B5/B6 and owner points remain governing |

S1→S2; S1+S2+actual authorized evidence→S3; S1+S2→S4 implementation
(with S3 required for verified claims); S2+S3+S4+B5→S5. This refines A→B
contributions already recorded, adds no group-order reversal or new deliverable.
DEL-01-02/03/05 and DEL-04-03 receive S1/S2 changes for generation,
diagnostics/version and configuration impact assessment before adoption; later
EXP/SQ consumers receive S4 support changes at their point of need. Their
current basis is unchanged by this staging notice. Group A carries the
matching relation. Accountable future owners are not already-dispatched executors.
