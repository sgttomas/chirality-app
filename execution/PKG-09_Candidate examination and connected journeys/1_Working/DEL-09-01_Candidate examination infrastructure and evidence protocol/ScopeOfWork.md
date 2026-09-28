---
schema: chirality-deliverable-sow/v1
deliverable_id: DEL-09-01
package_id: PKG-09
decomposition_basis: projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z@941c4d35f994594ce8aacd81758ab39079bddad6
project_scope_refs: [SOW-103, SOW-155, SOW-189, SOW-190, SOW-191, SOW-192, SOW-193, SOW-194, SOW-229]
package_objective_refs: [OBJ-008, OBJ-010]
---

# DEL-09-01 — Candidate examination infrastructure and evidence protocol

## Purpose and Objective Traceability

Provide reusable support for examining identified candidates and recording actual scenario execution and independent review. The App examination owner integrates the runner, fixture and evidence adapters. Each candidate's independent reviewer is separate from its author. Feature owners retain focused tests; journey owners use this support to join their own seams and assemble their own witnesses. Examination occurs when each candidate's named contributions are available; it is not a late testing phase.

This is the SOFTWARE production definition for the accepted TEST_SUITE. Its initialization defines planned outputs and checks; it supplies no product implementation, executed product witness, practitioner validation, release or lifecycle transition.

OBJ-008 is served by candidate-specific verification and honest limits on unrun or partial evidence. OBJ-010 is served by accountable independent review and source-grounded examination practice. Neither objective is discharged project-wide by this local contribution.

| Assigned scope | Local contribution | Output |
|---|---|---|
| SOW-103 | Invented verification material; later validation may use invented or owner-controlled material | OUT-001 |
| SOW-155 | WebKit and Chromium interface execution support, separately from native platform qualification | OUT-004 |
| SOW-189 | Candidate, harness/model/server configuration and date bound to results | OUT-002 |
| SOW-190 | Verification/validation distinction and passed/failed/blocked/not-run/inconclusive standing | OUT-002; OUT-003 |
| SOW-191 | Recorded real exchanges for repeatable seam tests; few deliberate live-model runs | OUT-001 |
| SOW-192 | Candidate changes reopen affected scenarios | OUT-003 |
| SOW-193 | macOS WebKit examination and targeted packaged-application smoke support | OUT-004 |
| SOW-194 | Criteria remain protected during repair | OUT-003 |
| SOW-229 | Independent review of identified candidates with actual reviewer/model identity | OUT-003 |

Source keys used below resolve to these repository records. Original-seed text is read within the accepted composite, qualified by later owner directions and HTML recommendations; consolidated documents expose the current clauses without claiming prior human examination of their later bytes.

| Key | Source and applicable locus |
|---|---|
| DEC | `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/DECISION.md`; `canonical/Deliverables.csv` DEL-09-01 and named interface rows; `canonical/Packages.csv` PKG-01/PKG-09; `canonical/Objectives.csv` OBJ-008/OBJ-010; `canonical/ScopeLedger.csv` the nine assigned rows, all under that same snapshot |
| OI | Snapshot `canonical/Open_Issues.csv`, with explicitly identified current dispositions in `projects/chirality-app-v4/execution/_Decomposition/Open_Issues.csv`; external boundaries in the corresponding snapshot and current `External_Dependencies.csv` |
| PRD | `projects/chirality-app-v4/docs/PRD.md` §0, V4-CST-06, V4-REC-05 and §9; original V4-CST-06 in `projects/chirality-app-v4/execution/_Coordination/Acceptances/APP-V4-BASIS-20260926/original-seed/PRD.md` |
| EXM | `projects/chirality-app-v4/docs/EXAMINATION.md` §§1–2, V4-EXM-01…05, §§4–7; original §§1–2 and V4-EXM-40 in `projects/chirality-app-v4/execution/_Coordination/Acceptances/APP-V4-BASIS-20260926/original-seed/EXAMINATION.md` |
| ARC | `projects/chirality-app-v4/docs/ARCHITECTURE.md` §1/M-7, §§3/6/8; original §1/M-7 and §8 in `projects/chirality-app-v4/execution/_Coordination/Acceptances/APP-V4-BASIS-20260926/original-seed/ARCHITECTURE.md` |
| OPS | `projects/chirality-app-v4/docs/OPERATING_METHOD.md` V4-OPS-30…34; original V4-OPS-34 in `projects/chirality-app-v4/execution/_Coordination/Acceptances/APP-V4-BASIS-20260926/original-seed/OPERATING_METHOD.md`; `projects/chirality-app-v4/conceptual/DECISIONS.md` D-13 |
| HTML | `projects/chirality-app-v4/execution/_Coordination/Acceptances/APP-V4-BASIS-20260926/DECISION_BRIEF.html` decisions 03–05; `OWNER_DIRECTIONS_EXCERPTS.md` U1–U5 in that same directory |
| HOST | `projects/chirality-app-v4/docs/HOST_INTEGRATION.md` §§5–8; EXM §1 identifies the external host's responsibility |
| COORD | `projects/chirality-app-v4/execution/_Coordination/_COORDINATION.md`, approved INITIAL definition setup and NO_STATUS_TOUCH authoring rule |

## Deliverable Definition — Ontology

- **CLM-001** — DEC assigns this deliverable reusable candidate-bound examination support, the App examination owner as integrator, and a reviewer separate from each candidate author. Accepted anticipated artifacts are fixture tests, evidence-capture scripts, an examination/review protocol, and WebKit/Chromium/native package execution support. Feature owners retain focused tests; this support joins their seams.
- **CLM-002** — PRD V4-CST-06 and EXM §§1–2 require invented verification material, candidate/configuration/date attribution and the five outcome states. Practitioner validation is a different activity with the owner as principal practitioner; invented or owner-controlled material is allowed there. No real client or engineering data is required. ARC M-7 and EXM V4-EXM-02 prefer recorded real protocol exchanges to live models where possible.
- **CLM-003** — EXM V4-EXM-03…05 limit earlier passes to their examined candidate, reopen affected checks after code changes, protect criteria during repair, and require WebKit/Chromium interfaces plus targeted native package smoke witnesses. OI-015 is RESOLVED_BY_SOURCE: both engines supply maintenance/portability evidence; macOS-first shipping does not imply a Windows release.
- **CLM-004** — OPS V4-OPS-34 and D-13 require independent candidate review with a Codex reviewer preference and the stated different-model Claude fallback if the Codex session is unavailable; the assigned SOW-229 retains different-family review where available. Actual separation and exposed model identity must be reported. Fresh context alone proves no model-family difference.
- **CLM-005** — Under DEC, `DEL-01-06` and its App packaging owner produce macOS packaging/distribution evidence; its owner obtains supplier terms. `DEL-09-02`'s App workflow-experience integration owner with independent examiner assembles standalone qualification. App fleet integration and independent examination belong to `DEL-09-05`; App connected-activity integration and human relay belong to `DEL-09-06`; App connected-activity examination with external SWB execution/traffic/receipts belongs to `DEL-09-07`; external-host examination and owner disposition of the extension promise belong to `DEL-09-09`; connector examination and provider qualification evidence belong to `DEL-09-10`; later reconstruction by an independent reader belongs to `DEL-09-11`. `DEL-09-12` carries owner practitioner validation and App validation coordination. Feature production and focused implementation tests stay with the respective feature owners; none of those acts is transferred to this harness.
- **CLM-006** — EXM §1, HTML 03–05/U1/U5 and HOST preserve external SWBPIPE implementation ownership and human-relayed coordination. The host offers, records and presents host actions; the person performs any actual human act. Applying, proposing, accepting an edit, checking, approving and accepting professional reliance have separate actors/evidence; one does not establish another. Faithful recording of an observed human act is allowed, with decision actor distinct from recorder. Unresolved operation policy is decided by the owners at the points in TBD-001; this evidence protocol carries their decisions rather than making them.

- **OUT-001** — Reusable invented-data and recorded-protocol fixture support for repeatable seam tests, with fixture/exchange origin and applicable candidate/configuration identified. Supports SOW-103 and SOW-191; objective OBJ-008. [CLM-001; CLM-002]
- **OUT-002** — Candidate/configuration evidence-capture scripts and their usable records, distinguishing actual observations, missing inputs and verification versus validation. Supports SOW-189 and SOW-190; objective OBJ-008. [CLM-001; CLM-002; CLM-006]
- **OUT-003** — Outcomes, reopening, criterion-protection and independent-review protocol, with candidate-bound review/evidence references usable by journey owners and reviewers. Supports SOW-190, SOW-192, SOW-194 and SOW-229; objectives OBJ-008 and OBJ-010. [CLM-001…CLM-006]
- **OUT-004** — Reusable WebKit, Chromium and native packaged-application execution harness support, retaining the actual engine/platform/package identity and distinct evidence standing. Supports SOW-155 and SOW-193; objective OBJ-008. [CLM-001; CLM-003]

## Completion and Reliance Basis — Epistemology

- **REQ-001** — Fixture support shall use invented engineering material for verification, trace recorded exchanges to their actual origin and applicable configuration, and permit replay for repeatable seams where feasible. Live-model runs remain few and deliberate without inventing a numerical budget. Invented fixtures and replay evidence retain their nature and do not certify an unobserved live host. [CLM-002; EXM V4-EXM-02]
- **REQ-002** — Every examination result shall name its candidate, date, harness/model versions and model server configuration, identify the criterion and actual evidence, and retain passed, failed, blocked, not-run or inconclusive standing. Passed/failed report observed evaluation against the criterion; blocked records the preventing condition; not-run states that execution has not occurred; inconclusive preserves insufficient or ambiguous evidence. Missing product inputs shall not be reported as an executed product pass or failure. [CLM-002; EXM §§1–2]
- **REQ-003** — Evidence capture shall distinguish agent-operated verification from actual practitioner validation and preserve the actor and scope of any recorded human act. It shall faithfully record an actually performed act while keeping the recorder distinct from the actor, and shall not infer acceptance, checking, approval or professional reliance from execution success. No ordering dependency between independently evidenced acts is invented by this protocol. [CLM-002; CLM-006; HTML 03]
- **REQ-004** — Candidate changes shall reopen affected scenarios; earlier passes remain attached to their original candidate. The protocol shall connect the changed candidate, affected checks, rerun evidence and remaining uncertainty without presenting an old pass as current. [CLM-003; EXM V4-EXM-03]
- **REQ-005** — Repairs shall preserve the examined criteria and their source identity. A failure is diagnosed and fixed; deleting the check, lowering the criterion or calling an unresolved policy settled shall not constitute repair. Any separately authorized criterion disposition retains its explicit decision and supersession; the examination author does not make that decision. [CLM-003; CLM-006; HTML 04]
- **REQ-006** — Independent review shall bind the actual examined candidate and identify reviewer separation from its author, exposed model identity and any availability limitation. It shall preserve the Codex preference and stated different-model Claude fallback, seek a different model family where available, and make no unsupported family-diversity claim. Findings and their dispositions remain distinct from human acceptance or product release. [CLM-004]
- **REQ-007** — Interface execution support shall cover WebKit and Chromium, including the macOS WebKit environment, and short smoke checks of each targeted packaged application on its in-scope platform. Browser results and native packaged results shall be separately identifiable; the former shall not substitute for a required native or actual-host witness. Targeted platform scope stays explicit and introduces no Windows shipping commitment. [CLM-003]
- **REQ-008** — The harness shall perform no act owned by another deliverable: package production/distribution by `DEL-01-06`; standalone qualification by `DEL-09-02`; fleet qualification by `DEL-09-05`; connected-activity agreement/workflow round trip by `DEL-09-06`; local host qualification by `DEL-09-07`; external control/catalog-extension qualification by `DEL-09-09`; connector qualification by `DEL-09-10`; later run reconstruction by `DEL-09-11`; and practitioner validation/feedback coordination by `DEL-09-12`, each with its actor in CLM-005. It supplies reusable support and evidence interfaces to those owners. Feature implementation/focused tests remain with feature owners under CLM-001 and CLM-005; external host implementation remains with the outside SWBPIPE session, human coordination/acts and unresolved policy decisions with the respective actors under CLM-006 and TBD-001. Evidence records shall not imply that these excluded acts occurred merely because support or a handoff exists.

- **AC-001** — OUT-001 supplies invented verification fixtures with usable origin/configuration references, without requiring real client/engineering material or selecting a Domains corpus/admission permission. Verify by VER-001. [REQ-001; CLM-002]
- **AC-002** — OUT-001 enables repeatable seam examination from recorded real exchanges where feasible, marks replay versus live observations, and makes deliberate live-run selection and limits visible without inventing a run quota or claiming replay as a live joined witness. Verify by VER-002. [REQ-001; CLM-002]
- **AC-003** — OUT-002 captures candidate, harness/model/server configuration, date, criterion, evidence and each of passed, failed, blocked, not-run and inconclusive with the meanings in REQ-002; absent product inputs never become an executed product pass/failure. Verify by VER-003. [REQ-002]
- **AC-004** — OUT-002 and OUT-003 preserve verification versus practitioner validation and actor/recorder separation, can faithfully record an actually performed human act, and reject fabricated human acts or inferred approval/reliance from tool success. Verify by VER-004. [REQ-003]
- **AC-005** — OUT-003 retains the old candidate's pass as historical, identifies affected checks after a candidate change and requires their current evidence or explicit unresolved standing. Verify by VER-005. [REQ-004]
- **AC-006** — OUT-003 carries failures through diagnosis/repair against the protected criterion, preserving any explicit separately authorized policy/criterion disposition without silently weakening or deleting the failed criterion. Verify by VER-006. [REQ-005]
- **AC-007** — OUT-003 makes independent candidate review usable with author/reviewer separation, candidate identity, actual model identity when exposed, availability limits and finding/disposition records; fresh context is never reported as proof of a different family. Verify by VER-007. [REQ-006]
- **AC-008** — OUT-004 supports both WebKit and Chromium interface execution and native smoke checks for each targeted packaged application, with macOS WebKit and in-scope native identities distinguished. Missing native/host inputs remain explicitly unrun or blocked rather than replaced by a browser pass. Verify by VER-008. [REQ-007]
- **AC-009** — All outputs retain the contribution and actor boundaries in REQ-008, consume focused feature evidence without taking over its production, and carry each applicable unresolved choice with its owner and point of need; no support artifact is represented as a journey, validation, release or policy decision. Verify by VER-009. [CLM-001; CLM-005; CLM-006; TBD-001]

## Production and Verification Method — Praxeology

The following methods define future checks on the delivered infrastructure/protocol; they are not reports of execution during INIT. Begin each actual examination with an identified candidate, applicable source criteria, selected configuration and available contributions. Use feature-owner evidence to select and join seams. Return candidate-specific results and limitations to the named journey owner and independent reviewer. Technical runner, record format and fixture details are developed within these outcomes; no API/wire field, numerical threshold or new universal policy is selected here.

- **VER-001** — Inspect the fixture set and its origins against PRD V4-CST-06 and the selected seam contracts. Confirm invented verification content, no required client data, and explicit provider/admission responsibility if a later research fixture is involved. Evidence: fixture references, basis/configuration and any missing admission input.
- **VER-002** — Exercise the reusable seam support against identified recorded exchanges and inspect repeatability and replay provenance. Review the basis for any deliberate live checks. Evidence: applicable exchange source, fixture/candidate/configuration identity, replay outcomes and live/replay limits; actual host execution remains separately evidenced.
- **VER-003** — Exercise evidence capture with representative supported outcomes, including missing-input and inconclusive cases. Inspect complete candidate/configuration/date/criterion binding and truthful standing. Evidence: produced records and observed capture behavior; illustrative records used to test the recorder are labeled as such, not product results.
- **VER-004** — Examine records for verification, practitioner validation, execution and human acts. Include a positive faithful record of an actually evidenced human act with actor distinct from recorder, and negative attempts to manufacture acceptance/checking/approval/reliance from execution or silence. Evidence: source act and scope, recorded attribution and rejected fabrication; no real human act is invented for a fixture.
- **VER-005** — Compare evidence for an identified earlier candidate and a changed candidate; inspect the affected-scenario determination and exercise the reopening route. Evidence: preserved prior result, change/affected-check links and current rerun or unresolved standing.
- **VER-006** — Compare the criterion before and after a repair and follow the failure, diagnosis, repair and rerun evidence. Confirm that a weakened/deleted check is not used to erase failure; if a criterion was separately changed, inspect the actual authorized disposition and retained prior standing. Evidence: criterion identities and disposition/repair chain.
- **VER-007** — Inspect an independently produced candidate review record against the author and candidate basis. Confirm actual reviewer separation, exposed model identity or unavailability, preference/fallback treatment, findings and closure limits. Evidence: exact reviewed candidate and reviewer return; no fresh-context-to-family inference.
- **VER-008** — Exercise the harness routes with the identified interface candidate in WebKit and Chromium, and the actual targeted packaged applications for native smoke checks. Keep engine/platform/configuration outcomes separate and report unavailable native/host input honestly. Evidence: actual interface and native execution records; do not claim unavailable routes passed.
- **VER-009** — Review output interfaces and protocol against DEC, OI and CLM-005/CLM-006. Enumerate each excluded act, its actual owner and the supporting claim, and inspect open-choice custody at its point of need. Evidence: bounded interface/owner mapping and findings; accepted contract maturity does not prove supplied contributions or joined readiness.

## Governing Values and Decisions — Axiology

- **AX-001** — The accepted Group3 decomposition and composite source precedence govern this definition. Source paths, planned tests, historical passes and actual candidate execution are separate facts. Mechanical schema/checklist checks verify this contract's definition only. COORD leaves lifecycle changes to the authorized manager after the independent definition check; this author does not modify status.
- **AX-002** — Criteria originate in accepted scope and source commitments, not in tests written to fit an implementation. Maintain criterion fidelity through repair and retain honest unknowns. Defined infrastructure, independent component passes or prepared coordination files do not establish a joined witness, practitioner fitness, human acceptance or professional reliance.
- **AX-003** — Keep records useful to candidate review, decisions, reliance and recovery. Preserve actual source/candidate identities and observations without inventing measurements, maintenance savings, a fixed live-run budget or a new approval ritual. No required native witness is discharged by portability evidence.
- **TBD-001** — These existing choices retain their source owners and timing. They constrain only the dependent criterion, fixture, qualification or execution; independent examination-support definition continues. DEC/OI and current EXM preserve the following; this deliverable records decisions when supplied and does not decide them.

| Open matter | Exact recorded owner | Exact recorded point of need | Local consequence |
|---|---|---|---|
| OI-001 — Reserved human acts | Owner with App/SWB contract owners | Before operation-policy production contracts | No blanket always-reserved list is fixed by this protocol |
| OI-002 — Classifier routine permissions | Owner with App/SWB contract owners | Before permission-policy implementation | Preserve routine permission versus professional-act distinction without selecting a classifier policy |
| OI-003 — Automatic catalog extension | Owner with host contract owner | Before claiming extension capability or fixing its acceptance criterion | Carry the actual disposition and protected criterion; no automatic extension pass is inferred |
| OI-005 — Additional essential hosts | Owner | Before examination scope is frozen | Do not invent an additional host or platform commitment |
| OI-011 — Signing and notarisation | App implementation owner with SWB owner | Before packaged distribution witness | Require identified packaging evidence from its owner before relying on that witness |
| OI-012 — Codex version pin | App implementation owner | Before protocol generation and qualification | Historical version examples are not the selected replay/qualification pin |
| OI-016 — Owner validation activity and period | Owner | Before practitioner validation in use | Owner-selected activities and agreed period remain open; no numeric period/fitness score is invented |
| OI-021 — First connected activity definition | Owner via outside SWB session and App/shared owner | Before connected-activity SoW and execution | Useful operation, permitted autonomy and candidate environment remain their decision |
| OI-023 — Domains receiving contract and timing | Owner with Domains/SWB/App receiving owners | Before later Domains-enabled design increment | Admission/query/provenance/freshness and privacy-compatible receiving arrangements govern a later research fixture |
| OI-026 — Domains provider ownership and App/program boundary | Owner with App/Domains/SWB definition owners | Before allocating Domains provider production and committing its integration | No provider construction allocation is inferred from support fixtures |

OI-015 is already resolved by source reconciliation and creates no new owner prompt. SWBPIPE's externally supplied execution and provider contribution records stay with their responsible owners; Domains joins later and PEC is not a blanket prerequisite to starting App definition. No present satisfaction of those dependencies is claimed by this contract.

## Output and Evaluation Matrix

| Output | Objective refs | Requirement/claim refs | Acceptance refs | Verification refs | Evidence expectation |
|---|---|---|---|---|---|
| OUT-001 | OBJ-008 | REQ-001; CLM-002 | AC-001 | VER-001 | Invented fixture and admission/origin inspection |
| OUT-001 | OBJ-008 | REQ-001; CLM-002 | AC-002 | VER-002 | Recorded seam replay and deliberate live-check distinction |
| OUT-002 | OBJ-008 | REQ-002; CLM-002 | AC-003 | VER-003 | Candidate/configuration/date and five-state evidence records |
| OUT-002 | OBJ-008 | REQ-003; CLM-006 | AC-004 | VER-004 | Faithful human-act record plus fabrication negatives; verification/validation distinction |
| OUT-003 | OBJ-008 | REQ-004; CLM-003 | AC-005 | VER-005 | Changed-candidate affected-check and reopening evidence |
| OUT-003 | OBJ-008 | REQ-005; CLM-003; CLM-006 | AC-006 | VER-006 | Protected criterion and truthful repair/disposition chain |
| OUT-003 | OBJ-008; OBJ-010 | REQ-006; CLM-004 | AC-007 | VER-007 | Independent candidate review and actual model/separation limits |
| OUT-004 | OBJ-008 | REQ-007; CLM-003 | AC-008 | VER-008 | Distinct WebKit/Chromium and in-scope native witnesses |
| OUT-003 | OBJ-008; OBJ-010 | REQ-008; CLM-001; CLM-005; CLM-006 | AC-009 | VER-009 | Excluded-act owner mapping, open-choice custody and support/journey boundary |
