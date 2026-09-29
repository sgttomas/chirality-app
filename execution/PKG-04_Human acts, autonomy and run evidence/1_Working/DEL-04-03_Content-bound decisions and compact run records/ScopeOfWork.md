---
schema: chirality-deliverable-sow/v1
deliverable_id: DEL-04-03
package_id: PKG-04
decomposition_basis: projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z@941c4d35f994594ce8aacd81758ab39079bddad6
project_scope_refs: [SOW-092, SOW-093, SOW-094, SOW-095, SOW-096, SOW-143, SOW-186]
package_objective_refs: [OBJ-004, OBJ-005]
---

# Content-bound decisions and compact run records

## Purpose and Objective Traceability

DEL-04-03 supplies the App/shared evidence-record contribution to PKG-04,
Human acts, autonomy and run evidence. It keeps attributable human acts and
run provenance recoverable from ordinary project files, links host evidence,
and makes content-bound lapse visible. OBJ-004 is served by a shared record
contract that preserves host authority; OBJ-005 is served by attributable,
reconstructable acts, result standing and run provenance. This contract
specifies required production; it does not claim that implementation, host
adoption or the later reconstruction witness has occurred. [B1, B2]

| Accepted scope | Local contribution | Objective | Contract anchors |
|---|---|---|---|
| SOW-092 | Ordinary project/workspace files for workflow definitions, human decisions and accepted records | OBJ-005 | OUT-001; REQ-001; AC-001 |
| SOW-093 | Harness sessions remain operational; file records carry human-act authority | OBJ-005 | OUT-001; OUT-002; REQ-001; AC-001 |
| SOW-094 | Compact project run records reference host receipts, hashes and origin evidence | OBJ-005 | OUT-001; OUT-002; REQ-002; AC-002 |
| SOW-095 | Each recorded human act identifies its content, scope, purpose and actual actor | OBJ-005 | OUT-001; OUT-002; REQ-003; REQ-004; AC-003; AC-004 |
| SOW-096 | Changed bound content makes the act visibly lapsed | OBJ-005 | OUT-002; OUT-003; REQ-004; AC-004 |
| SOW-143 | Shared format and receiving contract for host-agent runs linked to host receipts; host construction remains with its owner | OBJ-004 | OUT-001; OUT-004; REQ-005; REQ-006; AC-007 |
| SOW-186 | Run identity and observed workflow/version, conversation, autonomy, operations/outcomes, receipts, human acts and model | OBJ-005 | OUT-001; OUT-002; REQ-002; REQ-003; AC-002; AC-003; AC-005 |

Source keys below identify exact source loci. The frozen accepted rows are
read as part of the accepted composite: later owner directions and accepted
HTML recommendations qualify original draft language. Consolidated documents
express that composite; they were not themselves previously hash-approved by
the owner. [B3]

| Key | Source and relevant locus |
|---|---|
| B1 | `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/DECISION.md`; same snapshot `canonical/Deliverables.csv` rows DEL-04-01, DEL-04-02, DEL-04-03, DEL-09-11; `Packages.csv` PKG-04; `Objectives.csv` OBJ-004/OBJ-005; `ScopeLedger.csv` seven assigned rows |
| B2 | Same accepted snapshot `canonical/Open_Issues.csv` OI-001, OI-002, OI-013, OI-014 and `External_Dependencies.csv` DEP-001; current equivalents under `projects/chirality-app-v4/execution/_Decomposition/` retain these relevant dispositions |
| B3 | `projects/chirality-app-v4/execution/_Coordination/Acceptances/APP-V4-BASIS-20260926/ACCEPTANCE.md`, `COMPOSITE_BASIS.json`, `OWNER_DIRECTIONS.md` J–O and `DECISION_BRIEF.html` decisions d2/d3; originals in that acceptance's `original-seed/PRD.md` V4-REC-02…05, `HOST_INTEGRATION.md` V4-HI-32/70/71 and `ARCHITECTURE.md` §4 |
| P | `projects/chirality-app-v4/docs/PRD.md` V4-REC-01…05, V4-AUT-03…05, V4-PM-06 and OQ-02 |
| H | `projects/chirality-app-v4/docs/HOST_INTEGRATION.md` §1, V4-HI-25, V4-HI-30…33, V4-HI-70…71 |
| A | `projects/chirality-app-v4/docs/ARCHITECTURE.md` §4 host-agent record property and responsible host implementation boundary; V4-ARC-20 shared meaning and placement |
| E | `projects/chirality-app-v4/docs/EXAMINATION.md` V4-EXM-21/22 distinctions and V4-EXM-31 reconstruction and unknown outcomes |
| O | `projects/chirality-app-v4/docs/OPERATING_METHOD.md` V4-OPS-30…32 actual enforcement, proportion and record purpose |

## Deliverable Definition — Ontology

- **CLM-001** — Ordinary files in the user's project/workspace hold workflow definitions, the person's decisions and accepted records. A Codex/harness session store is operational, and a derived coordination view is not the authority for a human act. A host retains domain truth in its own store. [B1 SOW-092/SOW-093; P V4-REC-01…03, V4-PM-06]
- **CLM-002** — A compact run record identifies the workflow/version, conversation, autonomy settings, requested operations and their outcomes, host receipt references, actual human acts, and model used with its observed destination per turn; for a host's agent it also identifies each network destination contacted, with the allowing grant or list entry. Host receipts, hashes and origin marks evidence what changed; the run record links that evidence without copying it. [B1 SOW-094/SOW-186; H V4-HI-70/71; P V4-REC-04]
- **CLM-003** — The actual human decision actor and the agent or software recording that act are different roles. Faithful recording of a performed act is permitted; false attribution is prohibited. Execution, proposal acceptance, human checking, approval and professional reliance are distinct subjects: evidence of one establishes none of the others by itself. An operation's success is not a human act. [B3 d3; P V4-AUT-03; H V4-HI-25/30/31/33; E V4-EXM-21/22]
- **CLM-004** — The App/shared evidence-record owner owns this format, App reader/writer, content-change lapse handling and local contract fixtures. PKG-02 workflow definitions/checkpoints, PKG-03 basis/receipts and PKG-06 decisions consume this format; it receives act kinds and classes from App `DEL-04-01`, settings-in from `DEL-04-02`, subject content identities and method designations from `DEL-03-01`, operation outcomes, change-item content identities and receipt links from `DEL-03-02`, checkpoint arrival, act and lapse events (with hold events retained for the governance phase) and compatibility reports from `DEL-02-03`, external dispatch entries from `DEL-03-03`, observed supplier facts (supplied guidance, model and destination, tool-permission settlements) from `DEL-01-01`, and a host agent's network-destination events (destination contacted, destination grant, destination declined) from `DEL-05-01` (`APP-V4-SWBPIPE-INTAKE-20260928-DECISION-5`); App `DEL-04-02` owns autonomy/result-standing receiving components, and App `DEL-09-11` owns the later reconstruction witness with a separate reconstructing reader. App `DEL-04-01` defines and carries adopted policy; the owner with affected App/SWB contract owners decides unresolved operation classes and classifier policy. [B1 deliverable rows; B2 OI-001/OI-002]
- **CLM-005** — The host owner supplies receipts and offers, records and presents host human acts; the person actually performs the human act, and the accountable professional owns professional-reliance/certification judgments. Host-specific domain changes, receipt production, domain-store truth and embedded run recording implementation belong to the responsible host implementation owner; SWBPIPE construction is in the outside SWBPIPE session. Shared format responsibility does not transfer those acts to the App. [B1 DEL-04-03/PKG-04; B2 DEP-001; B3 J/O; H §1, V4-HI-30/31/71; P V4-AUT-05; A §4]
- **CLM-006** — A recorded human act binds to identified content, scope and purpose. A change to that bound content causes visible lapse. Reconstruction preserves the scope of actual acts and what remains unknown; source-resolution or transport success cannot fill an unobserved host outcome. [B1 SOW-095/SOW-096; P V4-REC-05; H V4-HI-32; E V4-EXM-31]

- **OUT-001** — Versioned human-act and run-file format (CONFIG), with record-authority documentation: ordinary-file identity, act/content/scope/purpose association and the compact run inventory with source references. Concrete serialization and wire-field spellings remain design choices within these semantics. Supports SOW-092, SOW-093, SOW-094, SOW-095, SOW-143 and SOW-186; OBJ-004 and OBJ-005. [B1; CLM-001; CLM-002; CLM-003; CLM-006]
- **OUT-002** — App record writer/reader and visible content-change lapse handling (CODE), consuming actual acts, operation outcomes and host evidence without claiming stronger standing than supplied. Supports SOW-092, SOW-093, SOW-094, SOW-095, SOW-096 and SOW-186; OBJ-005. [B1; CLM-001; CLM-002; CLM-003; CLM-006]
- **OUT-003** — Identity, reference and lapse fixtures (TEST) that exercise the versioned format and App handling, including actual human-act recording and false-attribution negatives. These fixtures produce evidence for the defined criteria; they create no additional product scope. Supports SOW-092, SOW-093, SOW-094, SOW-095, SOW-096 and SOW-186; OBJ-005. [B1 anticipated artifacts; CLM-001; CLM-002; CLM-003; CLM-006]
- **OUT-004** — Record-authority, receipt-link and consumer/host interface documentation (DOC), identifying the shared format's consuming responsibilities and host run-recording contribution for later reconstruction. Supports SOW-092, SOW-093, SOW-094, SOW-095, SOW-143 and SOW-186; OBJ-004 and OBJ-005. [B1 interfaces; B2 DEP-001; H §1/§9; A §4; CLM-004; CLM-005]

## Completion and Reliance Basis — Epistemology

- **REQ-001** — The format and App reader/writer shall retain workflow definitions, human decisions and accepted records as ordinary project/workspace files. Harness session content and rebuilt views shall remain operational or derivative; neither shall confer authority for a human act. Host domain truth shall remain with the host source identified in CLM-001. [SOW-092; SOW-093]
- **REQ-002** — Each compact project run record shall identify workflow/version, conversation, autonomy settings, requested operations and their observed outcomes, host receipt references, actual human acts, and model used with its observed destination per turn; for a host's agent, each network destination contacted, with the allowing grant or list entry (PRD V4-HOST-02 as revised by `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-5`). It shall link the host's receipts, hashes and origin evidence rather than copy them, and preserve unknown or unobserved outcomes as such instead of filling them from source-resolution or transport success. [SOW-094; SOW-186; CLM-002; CLM-006]
- **REQ-003** — Recording shall preserve the actual human actor and scope of a performed act separately from its recorder and the recorder's available evidence. An agent or software may faithfully record an actually performed human act; it shall not fabricate, impersonate or upgrade an act. Execution, proposal acceptance, checking, approval and professional reliance shall each retain their own actor/evidence; evidence of one shall establish no other act, and the record format shall impose no universal acceptance prerequisite on an independently evidenced different act. [SOW-095; SOW-186; CLM-003; CLM-005]
- **REQ-004** — Every human-act record shall bind to its identified content, scope and purpose. When that bound content changes, the App shall show the act as lapsed for the changed content while retaining the identity of what the act actually concerned; the previous act shall not silently apply to the new content. [SOW-095; SOW-096; CLM-006]
- **REQ-005** — The shared format and receiving documentation shall identify how PKG-02 definitions/checkpoints, PKG-03 basis/receipts, PKG-05 loop and panel receiving (`DEL-05-01`, `DEL-05-02`), PKG-06 decisions and the PKG-09 connected-activity and trace contracts (`DEL-09-06`, `DEL-09-09`) consume the record meaning and how host-agent runs use it with receipt references. App `DEL-04-02` receives the run evidence for standing/autonomy display, and App `DEL-09-11` receives the records for its separate later witness, as owned in CLM-004. Host implementation/adoption or receipt availability shall be reported only when evidenced, under CLM-005. [SOW-143; SOW-186; B1 interfaces; B2 DEP-001]
- **REQ-006** — This deliverable shall perform no act owned by another deliverable or external owner: deciding unresolved operation classes/classifier policy belongs to the owner with affected App/SWB contract owners, while defining/carrying adopted policy belongs to App `DEL-04-01`; constructing autonomy/standing UI belongs to App `DEL-04-02`; performing the later reconstruction witness belongs to App `DEL-09-11` (CLM-004). Host domain changes, receipt production, domain storage and host-specific embedded recording implementation belong to the responsible host owner, with SWBPIPE construction in its outside session; performing an actual human decision belongs to the person, and professional-reliance/certification judgments belong to the accountable professional (CLM-005). Faithful recording of those evidenced acts remains the local duty in REQ-003. [B1; B2; B3; H §1; A §4]

- **AC-001** — The format and App read/write path keep workflow definitions, human decisions and accepted records in ordinary project/workspace files, and identify sessions and derived views as non-authoritative for human acts. A session-only assertion or derived-view label supplies no missing human act. Verify with VER-001. [REQ-001; CLM-001]
- **AC-002** — The versioned format and App record path account for every run component named in REQ-002 and resolve the supplied host receipt/hash/origin references to their identified sources without reproducing host evidence or domain truth as a replacement authority. Verify with VER-001. [REQ-002; CLM-002]
- **AC-003** — A fixture with evidence of an actual human act is faithfully written/read with the person as decision actor, the recorder distinguishable, and its content/scope/purpose and evidence limits intact. Cases containing only an agent proposal, operation success or permission grant produce no invented human acceptance, checking, approval or reliance. An independently evidenced act remains recordable without manufacturing a different prior act. Verify with VER-002. [REQ-003; CLM-003; CLM-005]
- **AC-004** — An act bound to identified content/scope/purpose remains associated with that subject; changing the bound content makes its lapse visible and does not carry the act forward as effective for the changed content. The unchanged-content comparison preserves the original association. Verify with VER-003. [REQ-004; CLM-006]
- **AC-005** — Read/write and receiving cases with missing receipts or unobserved outcomes retain explicit uncertainty. Resolving a source or completing transport does not become evidence that a host change or human act occurred. Verify with VER-004. [REQ-002; REQ-003; CLM-006]
- **AC-006** — The delivered identity, reference and lapse fixtures exercise the record format and App handling against AC-001 through AC-005, including positive faithful recording, absent/unsupported acts, changed bound content and unknown host outcomes; reported results identify the candidate and actual observations without claiming the later host journey or reconstruction witness. Verify with VER-005. [OUT-003; B1 anticipated TEST artifacts; E V4-EXM-31]
- **AC-007** — The interface/authority documentation accounts for each consumer in REQ-005 and each excluded act and actual owner in REQ-006, preserves host receipt authority and shared host-run format duties, and identifies unprovided host contributions and unresolved choices without asserting delivery, adoption or policy decisions. Verify with VER-006. [CLM-004; CLM-005; B2]

## Production and Verification Method — Praxeology

Production proceeds from the accepted semantic inventory and actual consumer
responsibilities. Define the versioned format, implement the App read/write
and lapse behavior, and use local fixtures to examine those obligations.
Resolve an open operation or implementation allocation only at its affected
point of need through its actual owner. Receive host implementation evidence
for host-dependent use; a local fixture is evidence of its bounded scenario.
These production steps are specified here, not authorized for execution by the
initialization task. [B1; B2; A; O]

- **VER-001** — Inspect the versioned format and exercise representative App file read/write cases against the source inventory in REQ-001 and REQ-002. Trace every declared run component and receipt/hash/origin link to its supplied source, compare file identity with session/derived-view assertions, and inspect whether host material was copied into a substitute authority. Preserve candidate identity and actual field/reference observations for AC-001 and AC-002.
- **VER-002** — Run paired faithful-recording and fabrication-negative cases for AC-003: evidenced person act with a separate recorder; agent proposal only; operation success only; permission grant only; and an independently evidenced act without evidence of a different act. Compare recorded actor, subject, evidence and standing to the supplied case. No case assumes the unresolved global reserved-act list has been ruled.
- **VER-003** — For AC-004, write/read an act against identified content/scope/purpose, observe an unchanged-content control, change the bound content, and inspect the displayed lapse and retained original association. Record the compared content identities and actual observations; a passing schema check alone does not prove visible lapse.
- **VER-004** — For AC-005, exercise missing-receipt, unobserved-host-outcome and transport/source-resolution-only cases through record handling and receiving interpretation. Compare the resulting standing to the supplied evidence and show that unknowns remain unknown.
- **VER-005** — Inspect fixture coverage and run the identity/reference/lapse suite against the identified format/App candidate for AC-006. Check that each required semantic case is represented and its result reports observed behavior and limits; distinguish these local checks from App DEL-09-11's later reconstruction witness.
- **VER-006** — For AC-007, review the documentation against B1/B2 and CLM-004/CLM-005. Trace each consumer interface, each enumerated excluded act to its actual owner, each retained open choice to its point of need, and each host delivery/adoption assertion to received evidence. Return precise gaps rather than infer fulfillment from a prepared handoff.

## Governing Values and Decisions — Axiology

- **AX-001** — The accepted Group3 decision establishes this bounded definition basis, including open matters and external contributions. Historical pending/draft labels inside frozen sources do not undo that acceptance. It establishes neither implementation completion nor host adoption or professional reliance. [B1]
- **AX-002** — Apply the composite source order in B3. The original blanket wording against recording human acts does not override the later accepted distinction between fabricated attribution and faithful recording. Preserve separate acts and actors; neither automatic trust nor a universal approval chain follows from graduated autonomy. [B3 d3; P V4-AUT-03/04; H V4-HI-31]
- **AX-003** — Keep evidence proportionate to reconstruction and its named consumers. Record links and content identities serve attribution and lapse; copying host receipts or private transcripts into a new authority does not. Actual enforcement follows the host, while brief restrictions remain instructions unless separately enforced. [O V4-OPS-30…32; H V4-HI-71]
- **AX-004** — Revised under scope-change amendment `SCA-V4-001` (accepted snapshot `projects/chirality-app-v4/execution/_ScopeChange/SCA-V4-001_2026-09-28_2155`), applying `APP-V4-FIRST-INCREMENT-20260928-DECISION-1`, `APP-V4-FIRST-INCREMENT-20260928-DECISION-2` (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-FIRST-INCREMENT-20260928/OWNER_DECISIONS.md`), `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4` and `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-5` (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-SWBPIPE-INTAKE-20260928/OWNER_DECISIONS.md`). Revised: CLM-002, CLM-004, REQ-002, REQ-005 and TBD-001. Added: AX-004. Removed: none.
- **TBD-001** — OI-001/OI-002 were ruled for the first increment by `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2/D3; App DEL-04-01 carries them. Operation-specific additions remain open under OI-021 (owner via the outside SWB session and App/shared owner; before the connected-activity SoW). Resolve the affected choice before fixing dependent operation/permission implementation or examination criteria; ordinary-file authority, faithful attribution and content-bound lapse can be defined independently. This contract neither adopts the former App/host classifier default nor makes all records wait for a global list. [B2; P OQ-02; H V4-HI-30/31]
- **TBD-002** — OI-013/OI-014 retain host-specific placement/persistence and shared contract/component placement with the shared contract owner, SWB implementation owner and App/shared contract owners at their stated design points of need. This contract specifies shared meaning and the App contribution without prescribing a common service, fixed reuse allocation, wire fields or host conversation persistence. DEP-001 carries the external host contribution; a prepared contract is not receiving adoption. [B2; A §4, V4-ARC-20; B3 d2/J/O]

## Output and Evaluation Matrix

| Output | Objective refs | Requirement/claim refs | Acceptance refs | Verification refs | Evidence expectation |
|---|---|---|---|---|---|
| OUT-001 | OBJ-005 | REQ-001; CLM-001 | AC-001 | VER-001 | Candidate format and App file round-trip observations; session/view authority comparison |
| OUT-001 | OBJ-005 | REQ-002; CLM-002 | AC-002 | VER-001 | Required run inventory and resolved receipt/hash/origin source references, with copy/authority inspection |
| OUT-002 | OBJ-005 | REQ-003; CLM-003; CLM-005 | AC-003 | VER-002 | Paired actual-act recording and fabrication-negative observations with actor, recorder, subject and limits |
| OUT-002 | OBJ-005 | REQ-004; CLM-006 | AC-004 | VER-003 | Bound-content identities, unchanged control, changed-content lapse and original-act association |
| OUT-002 | OBJ-005 | REQ-002; REQ-003; CLM-006 | AC-005 | VER-004 | Missing evidence and transport/source-only cases retain unknown host outcomes and absent acts |
| OUT-003 | OBJ-005 | REQ-001; REQ-002; REQ-003; REQ-004; CLM-006 | AC-006 | VER-005 | Candidate-bound fixture coverage and actual local results, explicitly separate from later host/reconstruction witnesses |
| OUT-004 | OBJ-004; OBJ-005 | REQ-005; REQ-006; CLM-004; CLM-005 | AC-007 | VER-006 | Consumer/host interface and one-for-one owner trace, open-choice dispositions and exact external evidence limits |
