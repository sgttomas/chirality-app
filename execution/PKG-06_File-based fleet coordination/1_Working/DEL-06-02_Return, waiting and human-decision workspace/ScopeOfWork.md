---
schema: chirality-deliverable-sow/v1
deliverable_id: DEL-06-02
package_id: PKG-06
decomposition_basis: projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z@941c4d35f994594ce8aacd81758ab39079bddad6
project_scope_refs: [SOW-085, SOW-086, SOW-087, SOW-088, SOW-089]
package_objective_refs: [OBJ-006]
---

# Return, waiting and human-decision workspace

## Purpose and Objective Traceability

Enable the coordinator to examine returned work, understand why work waits and
make attributable decisions from packages naming the exact act, alternatives
and consequences. This SOFTWARE UX_UI_SLICE is owned by the App
fleet-experience owner. Its contribution to OBJ-006 is recoverable coordination
views grounded in ordinary project files; it does not by itself deliver the
whole fleet journey.

| Accepted scope | Local contribution | Current source clause |
|---|---|---|
| SOW-085 | Visible queue of returns awaiting examination | PRD V4-PM-03 |
| SOW-086 | Waiting work explained by recorded cause | PRD V4-PM-03 |
| SOW-087 | Exact-act human decision packages with alternatives and consequences | PRD V4-PM-04 |
| SOW-088 | Coordination state recoverable across sessions from files | PRD V4-PM-05 |
| SOW-089 | Rebuildable coordination views that remain derived | PRD V4-PM-06 |

Source keys below are repository-root-relative source identities, not new
records or alternative authority:

- **Allocation:** `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/DECISION.md` and its `canonical/Deliverables.csv` rows DEL-06-01, DEL-06-02, DEL-04-01, DEL-04-03, DEL-09-05, DEL-10-02 and DEL-10-04; `canonical/Packages.csv` row PKG-06; `canonical/Objectives.csv` row OBJ-006; `canonical/ScopeLedger.csv` rows SOW-085 through SOW-089. The actual Group3 decision establishes accepted standing despite historical pending labels within frozen rows.
- **Composite:** `projects/chirality-app-v4/execution/_Coordination/Acceptances/APP-V4-BASIS-20260926/ACCEPTANCE.md`, `OWNER_DIRECTIONS_EXCERPTS.md` U1–U5, `DECISION_BRIEF.html` decisions 03, 05 and 06, and `original-seed/PRD.md` V4-PM-03 through V4-PM-06. Later explicit directions qualify the accepted HTML recommendations and original seed.
- **PRD:** `projects/chirality-app-v4/docs/PRD.md` §0, V4-AUT-03 through V4-AUT-05, V4-PM-01 through V4-PM-06 and V4-REC-01 through V4-REC-04.
- **Host:** `projects/chirality-app-v4/docs/HOST_INTEGRATION.md` responsibility table, V4-HI-25, V4-HI-30 through V4-HI-33, V4-HI-61 through V4-HI-63 and §8 file-based fallback.
- **Recovery:** `projects/chirality-app-v4/docs/ARCHITECTURE.md` §3 properties distinguishing conversation recovery from undertaking recovery; `projects/chirality-app-v4/docs/EXAMINATION.md` V4-EXM-13.
- **Practice:** `projects/chirality-app-v4/docs/OPERATING_METHOD.md` V4-OPS-30 through V4-OPS-33; `projects/chirality-app-v4/execution/_Coordination/_COORDINATION.md` accepted INITIAL setup rules.
- **Open matters:** the Allocation snapshot's `canonical/Open_Issues.csv` and `canonical/External_Dependencies.csv`, with explicitly later receiving dispositions in `projects/chirality-app-v4/execution/_Decomposition/Open_Issues.csv` and `External_Dependencies.csv`.

## Deliverable Definition — Ontology

- **OUT-001** — CODE: return-review queue and waiting-cause views exposing returned work, the pending examination and recorded ownership, with waiting causes traced to the work records. Covers SOW-085, SOW-086; supports OBJ-006. Sources: Allocation DEL-06-02; PRD V4-PM-03.
- **OUT-002** — CODE: prepared human decision-package view, showing the exact act requested, alternatives, consequences and the relevant recorded decision standing. It participates in file-derived cross-session reconstruction. Covers SOW-087, SOW-088, SOW-089; supports OBJ-006. Sources: Allocation DEL-06-02; PRD V4-PM-04 through V4-PM-06; Host V4-HI-30 through V4-HI-33.
- **OUT-003** — TEST: cross-session reconstruction and queue/decision fixtures for these views, with source/candidate-bound results available to the joined fleet examiner. Covers SOW-085, SOW-086, SOW-087, SOW-088, SOW-089; supports OBJ-006. Sources: Allocation DEL-06-02 and DEL-09-05; Recovery V4-EXM-13. Fixtures implement the requirements here; their setup creates no additional product scope.
- **OUT-004** — DOC: view derivation and ownership boundary, identifying the authoritative file inputs, native observation distinction, recovery limits, receiving interfaces and accountable review/integration actors. Covers SOW-085, SOW-086, SOW-087, SOW-088, SOW-089; supports OBJ-006. Sources: Allocation DEL-06-02; PRD V4-PM-05/06; Host §8; Practice V4-OPS-31/32.

The following claims allocate acts and interfaces; an artifact's existence does
not prove an executing child, a completed review, integration or a human act.
All deliverable identifiers in these claims belong to the App v4 project.

- **CLM-001** — `DEL-06-01`, owned by the App fleet-record owner, supplies the versioned bounded brief/current undertaking work-graph records and native-delegation associations. This view slice consumes that record contract; native running-state observations are evidence of their own subjects, separate from returned, reviewed and integrated work. Sources: Allocation DEL-06-01 and DEL-06-02; Recovery §3.
- **CLM-002** — `DEL-04-01` defines and carries adopted operation-policy and human-act distinctions under the App/shared human-act contract owner; the owner and host policy owner decide unresolved classes. `DEL-04-03` carries the content-bound decision/run record format and App record reader/writer under the App/shared evidence-record owner. Host owners supply receipts and the offered/recorded/presented human-act interfaces; the person performs the attributable human act and the accountable professional owns professional reliance. A recorder may faithfully record a performed human act without becoming its actor. Sources: Allocation DEL-04-01 and DEL-04-03; Composite decision 03; PRD V4-AUT-03/05; Host responsibility table and V4-HI-25/30/31/32/33.
- **CLM-003** — Managers retain actual review and integration ownership, including when PEC is absent; the human retains consequential decisions. `DEL-09-05`, owned by the App fleet integration owner with independent examiner, owns the joined fleet/longer-work recovery witness that joins these views, graph records, native descendants and actual-act records. Local fixtures supply evidence to that owner without claiming the joined result. Sources: Composite decisions 05/06; Allocation DEL-09-05; Recovery V4-EXM-13; Host §8.
- **CLM-004** — `DEL-10-02` belongs to the App undertaking manager, with the human at applicable stage decisions, and owns file-native undertaking controls/practice feedback. `DEL-10-04` belongs to the App project dependency owner, with the owner accepting the examined current DAG, and owns the project production dependency DAG. These controls can precede PKG-06 product views. The existing PEC owning project supplies PEC; PKG-07 owns App receiving/qualification duties. PEC observes within its qualified adopted coverage, without dispatching, owning an execution queue or writing human rulings. Sources: Allocation DEL-10-02, DEL-10-04 and PKG-06 exclusions; Composite decision 06; Host V4-HI-61/62/63; Open matters DEP-002.

## Completion and Reliance Basis — Epistemology

- **REQ-001** — The return queue shall expose returned work awaiting examination and its recorded ownership/pending-review standing. Receiving a return, observing a worker stop or reading a success notification shall not silently mark that return checked, accepted or integrated. Sources: SOW-085; Allocation DEL-06-02; PRD V4-PM-03; CLM-001, CLM-003.
- **REQ-002** — Waiting views shall explain waiting by the cause evidenced in the files, retaining the affected contribution and responsible ownership. Dependent work, independent ready work and returned work waiting for review shall remain distinguishable where the basis supports those conclusions; missing evidence shall remain an identified gap rather than invented readiness or an empty queue. Sources: SOW-086; Recovery V4-EXM-13; Host V4-HI-62; CLM-001, CLM-003.
- **REQ-003** — A decision package shall state the exact act requested, its subject/basis, alternatives and consequences, retaining pending versus actually recorded decisions. Applying an operation, accepting a proposed edit, checking, approval and professional reliance shall retain their distinct actors and evidence; an operation's success or a projection shall not imply another act. Proposal-edit decisions shall say accept, not approve. Sources: SOW-087; PRD V4-PM-04 and V4-AUT-03; Host V4-HI-25/30/31/33; CLM-002.
- **REQ-004** — The view shall faithfully present an actually performed human act recorded through the owning record interface, distinguishing the decision actor from the recorder and preserving the content/scope/purpose binding and visible lapse supplied by the actual-act record. It shall leave an unobserved act unclaimed. Each evidenced act retains its own standing: no synthetic requirement that acceptance occur before any independently evidenced checking, application or other act is introduced by the view. Sources: SOW-087, SOW-089; Allocation DEL-04-03; Composite decision 03; PRD V4-AUT-03; Host V4-HI-25/31/32; CLM-002.
- **REQ-005** — Coordination views shall reconstruct status across sessions from project files, preserving ownership, returns awaiting review, what was actually reviewed/integrated, pending choices and changed-basis limitations. Native running observations, conversation recovery and the derived view shall remain distinguishable from recorded work/act state. Rebuilding or rendering shall not create a return, review, integration, decision or permission. Sources: SOW-088, SOW-089; PRD V4-PM-05/06 and V4-REC-02/03; Allocation DEL-06-02; Recovery; CLM-001, CLM-002, CLM-003.
- **REQ-006** — The views and their definition shall support the file-native route without PEC availability or their own prior product existence. PEC absence, stale/partial/failing coverage or a missing feed shall not cancel accountable review/integration ownership or imply empty work, readiness or permission. Any future PEC-derived input is received through its identified adopted interface, retaining the source authority and limitations. Sources: SOW-088, SOW-089; Allocation DEL-06-02 PhaseHint and DEL-10-02; Composite decision 06; Host V4-HI-61/62/63 and §8; CLM-003, CLM-004.
- **REQ-007** — This deliverable shall perform no act owned by another deliverable: defining/writing the underlying graph and delegation association belongs to `DEL-06-01` (CLM-001); defining or deciding policy and writing the canonical human-act/run format belongs to the contract/record owners of `DEL-04-01` and `DEL-04-03`, with unresolved policy decisions retained by the owner and host policy owner (CLM-002); conducting and accepting the joined fleet witness belongs to the integration owner/independent examiner of `DEL-09-05` and the actual accepting actor under the applicable method, not this local view (CLM-003); maintaining project practice and accepting the project DAG belongs respectively to `DEL-10-02` and `DEL-10-04` and their named human actors (CLM-004). Actual review/integration remains with managers (CLM-003); human decision and professional reliance remain with the person/accountable professional, while hosts offer/record/present those acts (CLM-002); PEC provider construction and receiving qualification remain with the PEC owning project and PKG-07 (CLM-004). This boundary excludes those acts from this slice while retaining its required consuming, presenting and evidence-return duties.

- **AC-001** — Given a recorded return awaiting examination, the queue exposes it with recorded ownership and pending-review state; native completion or success without review/integration evidence does not promote it. Verified by VER-001. Sources: REQ-001; SOW-085; Allocation DEL-06-02.
- **AC-002** — Waiting fixtures preserve and show the evidenced cause and ownership for dependent work and pending review alongside independently supported ready work; an unavailable cause or unsupported readiness remains visible as a limitation. Verified by VER-002. Sources: REQ-002; SOW-086; Recovery V4-EXM-13.
- **AC-003** — A pending human decision is presented as the exact requested act with subject/basis, alternatives and consequences; proposal acceptance is labeled accept and does not establish checking, approval or professional reliance. Verified by VER-003. Sources: REQ-003; SOW-087; Host V4-HI-25/30/33.
- **AC-004** — An actually performed human decision can be faithfully presented from its record with human actor distinct from recorder and applicable content binding/lapse visible; absent human evidence, tool success or a view rebuild cannot fabricate that act. Independently evidenced checking/application remains visible without invented prior acceptance. Verified by VER-004. Sources: REQ-003, REQ-004; SOW-087, SOW-089; CLM-002.
- **AC-005** — After cross-session reconstruction and an interruption with a changed basis, the views recover the file-backed return, review/integration standing, resource/worker ownership, waiting causes and pending choices, preserving gaps and lapse rather than treating a recovered conversation or native observation as their proof. Rebuild does not alter the source records or perform the represented acts. Verified by VER-005. Sources: REQ-005; SOW-088, SOW-089; Recovery V4-EXM-13.
- **AC-006** — With PEC absent, the queue/waiting/decision views remain reconstructable from sufficient project files and managers retain review/integration ownership; a simulated limited or unavailable observation never supplies readiness, permission or empty-work conclusions. The documented bootstrap permits file-native undertaking controls before product views. Verified by VER-006. Sources: REQ-006; SOW-088, SOW-089; CLM-003, CLM-004.
- **AC-007** — The derivation/boundary documentation and local evidence identify each consumed file/record interface, actual review/integration responsibility, human actor versus recorder, unresolved decisions and points of need; they provide the local fixture results to DEL-09-05 without asserting a joined fleet pass or taking over the acts enumerated in REQ-007. Verified by VER-007. Sources: REQ-007; SOW-085, SOW-086, SOW-087, SOW-088, SOW-089; Allocation DEL-06-02 and DEL-09-05.

Completion is candidate-bound production and evidence satisfying these criteria;
this initial contract supplies neither code nor a product qualification. The
local evidence is an input to the whole-journey owner. Schema validity, an
INITIALIZED contract, a successful test or a rendered view cannot establish an
unperformed human act or professional reliance.

## Production and Verification Method — Praxeology

1. Confirm the identified graph/actual-act input contracts and the operation
   policy actually applicable to each exposed act. Carry unresolved inputs to
   their stated point of need; define independent file-based behavior now.
2. Implement the bounded queue, waiting and decision views from those inputs.
   Retain source identities and distinguish derived display from the owning
   writer/actor. Choose UI layout and technical means during design without
   inventing a wire schema or additional feature commitment here.
3. Build the local fixtures below against the identified candidate and file
   basis. Verify both faithful evidence presentation and resistance to false
   promotion. These are future production checks, not tests executed by INIT.
4. Record candidate identity, relevant file/record inputs, observed outcomes
   and limitations with the fixture evidence. Supply that evidence and the
   derivation boundary to the App fleet integration owner for DEL-09-05's
   joined examination; keep actual acceptance separate.

- **VER-001** — Exercise the queue with a returned item awaiting examination and a native-completion/success observation without review or integration evidence; compare the displayed return/owner/state to the source records. Check promotion occurs only on evidence of its own act, never merely on notification.
- **VER-002** — Exercise recorded dependency waiting, pending review and separately ready work, plus an unavailable cause/basis; compare displayed causes, ownership and limitations to the exact file inputs without imposing an invented exhaustive cause taxonomy.
- **VER-003** — Inspect a pending decision package against its source: exact act, subject/basis, alternatives and consequences are present, and accept/check/approval/reliance labels preserve their subjects. Record source-to-view differences.
- **VER-004** — Pair a positive faithful-recording case (a performed human act, human actor distinct from recorder, content-bound record and visible lapse when that content changes) with negative cases lacking actual human evidence. Include independently evidenced checking/application without prior acceptance and operation success without acceptance; verify the view preserves only the respective warranted acts.
- **VER-005** — Rebuild the local views in another session from the same ordinary project files, then exercise interrupted review/integration and a changed basis. Compare recovered returns, owners, waiting, pending decisions and actual reviewed/integrated standing to those files; compare input hashes before/after rebuild. Keep native observation and conversation-recovery evidence separate and report unrecoverable facts. These fixtures contribute to, rather than replace, the joined V4-EXM-13 witness.
- **VER-006** — Exercise file-backed view reconstruction with no PEC and with a limited/missing observation. Verify that sufficient files support the view, unsupported conclusions remain limited, and ownership is retained. Inspect the documented path from pre-existing file-native controls to the later product views. No PEC wire-field experiment or provider qualification is part of this check.
- **VER-007** — Review OUT-004 and the candidate-bound local fixture handoff against CLM-001 through CLM-004, REQ-007 and the Allocation rows. Check every excluded act's named owner, each receiving interface and each open matter's owner/point of need, and confirm the local evidence does not claim the joined witness or any unperformed human act.

## Governing Values and Decisions — Axiology

- **AX-001** — Ordinary files retain coordination/decision authority; displays and notifications expose their evidence and limitations. The product serves the coordinator without making a projection an actor. Sources: PRD V4-PM-05/06; Host V4-HI-61/62/63.
- **AX-002** — Preserve the accepted composite precedence and graduated autonomy: no blanket reserved-act list, classifier default, inferred acceptance prerequisite or transferred human/professional responsibility is adopted here. Policy definition and actual policy choice remain separate. Sources: Composite decision 03; PRD V4-AUT-03/04; CLM-002.
- **AX-003** — Keep records useful for recovery, decision and examination, and retain candid enforcement/observability limits. This contract authoring changes no lifecycle; under approved setup the manager may separately record INITIALIZED only after a valid contract and affected independent check pass. Sources: Practice; `_COORDINATION.md`.
- **AX-004** — App v4 file-native work proceeds without PEC. Later PEC receiving metadata, including D108's accepted-as-is limitation, does not establish a repaired criterion, qualified release or App adoption; receiving currency is rechecked at its actual reliance point. Sources: current Open matters OI-022/DEP-002; Composite decision 06. No separate PEC capability or wire protocol is selected here.
- **TBD-001** — OI-001, reserved human acts: **Owner with App/SWB contract owners** must choose always-reserved acts by operation and consequence **before operation-policy production contracts**. A concrete unruled operation waits for its applicable ruling; truthful view definition and independently supported work continue. Source: accepted/current Open_Issues.csv OI-001; CLM-002.
- **TBD-002** — OI-002, classifier routine permissions: **Owner with App/SWB contract owners** resolves App/host treatment and distinguishes routine tool permissions from professional acts **before permission-policy implementation**. No classifier behavior is selected by these views. Source: accepted/current Open_Issues.csv OI-002.
- **TBD-003** — OI-006, further fleet management scope: **Owner** defines any additional outcome beyond accepted option B **during FEED before corresponding production contracts**. No additional scheduling, staffing or whole-manual product feature follows from this slice. Source: accepted/current Open_Issues.csv OI-006; PRD §4.6 and OQ-06.
- **TBD-004** — OI-022, first PEC receiving envelope: **App consumer owner and PEC owner** define first consumer questions, exact response/tool contract, coverage/freshness/limits, no-response fallback and release/adoption evidence **before operational consumer reliance**. DEP-002's supplier is the **PEC owning project**, needed **before reliance on covered PEC consumer claims; not before v4 preparation or initial work**. PKG-07 owns the receiving work; no all-PEC-cleanup prerequisite is introduced. Source: accepted/current Open matters OI-022/DEP-002; CLM-004.

There is no identified contradiction among the assigned accepted scope and the
cited current clauses. Layout, implementation decomposition and exact fixtures
remain technical means; this contract adds no numerical threshold, universal
staffing count or performance promise.

## Output and Evaluation Matrix

| Output | Objective refs | Requirement/claim refs | Acceptance refs | Verification refs | Evidence expectation |
|---|---|---|---|---|---|
| OUT-001 | OBJ-006 | REQ-001, CLM-001, CLM-003 | AC-001 | VER-001 | Candidate/source-bound queue fixture; pending review retained after native completion/success |
| OUT-003 | OBJ-006 | REQ-001, CLM-001, CLM-003 | AC-001 | VER-001 | Candidate/source-bound queue fixture; pending review retained after native completion/success |
| OUT-001 | OBJ-006 | REQ-002, CLM-001, CLM-003 | AC-002 | VER-002 | Cause/owner/source comparisons and explicit unsupported-readiness case |
| OUT-003 | OBJ-006 | REQ-002, CLM-001, CLM-003 | AC-002 | VER-002 | Cause/owner/source comparisons and explicit unsupported-readiness case |
| OUT-002 | OBJ-006 | REQ-003, CLM-002 | AC-003 | VER-003 | Exact-act package and decision-label comparison |
| OUT-003 | OBJ-006 | REQ-003, CLM-002 | AC-003 | VER-003 | Exact-act package and decision-label comparison |
| OUT-002 | OBJ-006 | REQ-003, REQ-004, CLM-002 | AC-004 | VER-004 | Positive faithful human-record case; separate recorder; lapse and fabrication negatives; independently evidenced acts |
| OUT-003 | OBJ-006 | REQ-003, REQ-004, CLM-002 | AC-004 | VER-004 | Positive faithful human-record case; separate recorder; lapse and fabrication negatives; independently evidenced acts |
| OUT-001 | OBJ-006 | REQ-005, CLM-001, CLM-002, CLM-003 | AC-005 | VER-005 | Cross-session/interruption comparison, changed-basis limits and source-hash preservation |
| OUT-002 | OBJ-006 | REQ-005, CLM-001, CLM-002, CLM-003 | AC-005 | VER-005 | Cross-session/interruption comparison, changed-basis limits and source-hash preservation |
| OUT-003 | OBJ-006 | REQ-005, CLM-001, CLM-002, CLM-003 | AC-005 | VER-005 | Cross-session/interruption comparison, changed-basis limits and source-hash preservation |
| OUT-001 | OBJ-006 | REQ-006, CLM-003, CLM-004 | AC-006 | VER-006 | File-native absent/limited-PEC reconstruction and bootstrap/ownership evidence |
| OUT-002 | OBJ-006 | REQ-006, CLM-003, CLM-004 | AC-006 | VER-006 | File-native absent/limited-PEC reconstruction and bootstrap/ownership evidence |
| OUT-003 | OBJ-006 | REQ-006, CLM-003, CLM-004 | AC-006 | VER-006 | File-native absent/limited-PEC reconstruction and bootstrap/ownership evidence |
| OUT-004 | OBJ-006 | REQ-006, CLM-003, CLM-004 | AC-006 | VER-006 | File-native absent/limited-PEC reconstruction and bootstrap/ownership evidence |
| OUT-003 | OBJ-006 | REQ-007, CLM-001, CLM-002, CLM-003, CLM-004 | AC-007 | VER-007 | Source-grounded ownership/interface map and local evidence handoff to joined fleet owner with unresolved points of need |
| OUT-004 | OBJ-006 | REQ-007, CLM-001, CLM-002, CLM-003, CLM-004 | AC-007 | VER-007 | Source-grounded ownership/interface map and local evidence handoff to joined fleet owner with unresolved points of need |
