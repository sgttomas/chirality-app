---
schema: chirality-deliverable-sow/v1
deliverable_id: DEL-09-12
package_id: PKG-09
decomposition_basis: execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z
project_scope_refs: [SOW-207, SOW-208, SOW-209]
package_objective_refs: [OBJ-008, OBJ-010]
---

# Practitioner validation and feedback disposition

## Purpose and Objective Traceability

This deliverable finds out whether v4 is fit for real design work, by having the owner do such work with it and keeping what the owner noticed. It contributes three things: the arrangement the owner agreed to (what work, in which applications, over what period, with what material); the account of what the owner actually observed in use; and the disposition of each observation, routed to the requirement, workflow or method that owns it. The owner is the practitioner. The App validation coordinator arranges the work and routes the observations, and judges nothing on the owner's behalf.

SOW-207 is the arrangement, SOW-208 the account of use and SOW-209 the dispositions. They serve OBJ-008 (verification and validation kept distinct, without overstating partial or unrun evidence), and SOW-209 also serves OBJ-010 (accountable commitments and manual-led practice). Its sources are EXAMINATION §1 and V4-EXM-40…42, PRD V4-CST-05/06 and §8, and OPERATING_METHOD V4-OPS-20…23 and 31…34.

## Deliverable Definition — Ontology

- **OUT-001** — The validation arrangement: the realistic design work the owner chose, in the Chirality App and in SWBPIPE, the agreed period, the invented or owner-controlled material, the identified candidates, and the evidence that the owner agreed. Supports SOW-207; OBJ-008.
- **OUT-002** — The account of use: what the owner actually observed, linked to its source, for each application, with candidate, configuration, date, conditions and limits, and with the coverage that was not observed stated. Supports SOW-208; OBJ-008.
- **OUT-003** — The feedback dispositions: each observation linked to the commitment that owns it and to its recipient, the treatment proposed and any decision actually made, including any proposed change to a successor basis with its standing. Supports SOW-209; OBJ-008 and OBJ-010.

Terms:

- **Validation in use.** A practitioner doing realistic work to judge fitness for use. Agent-operated scenarios, automated checks and fixture runs are verification and never establish it. Real use by the owner on invented material is validation.
- **What to notice.** Four design aims, none of them a score: whether the results warranted confidence for the attention they took (the owner's measure); where the person had to work around the product; where agent and person could not see the same thing; and where a record was needed and missing, or kept and never read.
- **Disposition.** For one observation: a proposed revision, a scoped departure, or no change, with who decided and in what scope. A proposal stays a proposal until its decision and adoption are evidenced.

Boundary:

- **CLM-001** — The owner is the practitioner and decides the period and the activities; the coordinator routes observations to their owners.
- **CLM-002** — Agents do development testing. The owner's product testing begins after readiness has been recommended to the owner, and a control operated by an agent establishes no act of the owner.
- **CLM-003** — `DEL-10-02` receives method feedback and `DEL-10-01` carries the adopted method and edition, with the owner deciding consequential adoption or departure. Feature owners keep changes to their requirements and their focused checks. `DEL-09-01` owns the examination support. Routing an observation performs none of those later acts.
- **CLM-004** — SWBPIPE's own project builds the host and its surface for offering, recording and presenting human acts; coordination with it is relayed by the human. `DEL-04-01` carries the operation policy: for the first increment five acts are reserved to a person, with operation-specific additions undecided (owner, with the affected App and host design owners), and routine tool permission is the person's own Codex setting and never stands for one of them.
- **CLM-005** — The owner decides replacement and publication on their own evidence, which `DEL-11-03` assembles; `DEL-11-01` carries preservation and continuing obligations. Replacement retires no other project and establishes no professional reliance.
- **CLM-006** — For 4.0.0 this deliverable covers the owner's use of the App alone. The owner's use of SWBPIPE is held outside 4.0.0, as `DEL-09-07` and `DEL-09-11` are, and may be worked on in support of SWBPIPE. Where a requirement or criterion below names both applications, it is met for 4.0.0 on the App.

## Completion and Reliance Basis — Epistemology

- **REQ-001** — The arrangement records the owner's actual agreement for both applications, on realistic work of the owner's choosing and invented or owner-controlled material. A plan written by the coordinator is neither agreement nor use.
- **REQ-002** — The account holds actual observations and their limits, with candidate, configuration, date and source links sufficient to revisit them, addressing the four aims. It carries no numerical pass score and assumes no favourable conclusion. The absence of an observed issue says nothing about use that was not observed.
- **REQ-003** — Observed execution, acceptance of a proposal, checking, approval and professional reliance stay attributed to their actual actors and evidence. A real human act is recorded faithfully, the human actor apart from the recorder, with its subject. Tool success, a proposed action, a verification pass or an agent's inference is never turned into a human act, and acceptance is not required before another independently evidenced act.
- **REQ-004** — Each observation is routed to the owning requirement, workflow or method, keeping the original observation, its conditions, the commitment and source it concerns, the recipient and the evidence of disposition. Method observations cite the section of the selected manual and the existing work record. Where like work is compared, preparation, review, repair, integration, recovery and waiting are distinguished by cause; source size or elapsed time alone measures nothing.
- **REQ-005** — Each undecided matter that a selected activity depends on is carried with its owner, consequence and point of need. Definition, supplied inputs, performed use, decision and adoption are separately evidenced facts.
- **REQ-006** — This deliverable performs no act owned by another, as allocated in CLM-003, CLM-004 and CLM-005: it changes no requirement, decides no method, policy, replacement, adoption or retirement, builds nothing in SWBPIPE, and performs no person's judgment.
- **REQ-007** — For 4.0.0 the owner uses the candidate after Agent 0 has recommended it ready, and answers yes or no on whether it is ready. The answer is the owner's act, recorded in the owner's words. The work and its period are the owner's to choose at the time and are not fixed in advance.

- **AC-001** — The arrangement names each application in it, the candidate, the work the owner chose and the material, as the owner chose them, and holds the owner's own agreement. The work and its period are the owner's to choose at the time of use and are not fixed in advance. Verify by VER-001. [REQ-001; CLM-001; CLM-006]
- **AC-002** — The account holds what the owner actually observed while using the identified candidate, for each of the four aims, with candidate, configuration and date, grounds and limits, and states what was not observed. No automated or fixture-only result appears as validation. Verify by VER-002. [REQ-002; CLM-002]
- **AC-003** — Each act in the records names its actual actor, subject and evidence, with the recorder separate; an owner's judgment recorded by the coordinator names the owner as actor and the coordinator as recorder; no agreement, approval or reliance appears that a person did not perform; and an independently evidenced act is not refused for lack of an earlier acceptance. Verify by VER-003. [REQ-003]
- **AC-004** — Every recorded observation is traced to its owning requirement, workflow or method and to a recipient, and has a disposition that distinguishes a proposal from a decision, with the decider and the scope. A proposed change to a successor basis is kept with its standing. Each method observation cites the section of the selected manual, its observed conditions and the existing work record that carries the work. Where like work is compared, the comparison separates preparation, review, repair, integration, recovery and waiting by cause and draws no conclusion from source size or elapsed time alone. Verify by VER-004. [REQ-004; CLM-003]
- **AC-005** — The arrangement and the dispositions carry each undecided matter with its owner, consequence and point of need, and contain no period, operation, autonomy policy, candidate environment or retirement that its owner did not decide. Verify by VER-005. [REQ-005]
- **AC-006** — The dispositions and their links keep each excluded act of REQ-006 with its owner. Verify by VER-006. [REQ-006]
- **AC-007** — After Agent 0 has recommended the candidate ready, the owner has used it and answered yes or no on whether it is ready; the answer is recorded in the owner's words with the owner as actor and the recorder separate, and every observation the owner made has a disposition (AC-004). Verify by VER-007. [REQ-007; REQ-003]

An unfavourable finding, faithfully kept, meets these criteria and leaves the product's fitness issue open with its owner. A criterion that needs agreement or use is unmet until the agreement or the use has happened.

## Production and Verification Method — Praxeology

The coordinator prepares the arrangement with the owner and obtains the owner's agreement before any use counts as validation. The owner then does the chosen work in both applications over the agreed period, and the coordinator records what the owner reports, with its conditions and gaps. Observations go to their owners, and consequential method or basis changes go to the decision that owns them. When a candidate or its basis changes, the affected evidence is revisited and the earlier evidence stays evidence of its own subject. Arrangement, observation and disposition are kept as three kinds of record; a method observation stays at the work record that already carries the work (OPERATING_METHOD V4-OPS-20). Where the arrangement, the account and the dispositions are kept is undecided (owner).

- **VER-001** — Inspect the arrangement against V4-EXM-40 and the source of the owner's agreement. Compare the coverage planned with the coverage performed.
- **VER-002** — Review the records of use and the owner's observations against V4-EXM-40/41 and the arrangement: candidate, configuration, date and each aim, with an issue not observed kept apart from use not observed.
- **VER-003** — Trace each attributed act to its real source and content, including one owner judgment recorded by the coordinator, and check that a receipt, a prepared proposal or a verification pass has supplied no human act, and that an independently evidenced check or execution is kept without demanding a prior acceptance.
- **VER-004** — Follow each observation to its commitment, recipient and disposition; for method feedback inspect the manual section, the conditions and the work record, and the decision if one was made. Where like work is compared, check that the comparison is by cause and rests on neither source size nor elapsed time alone.
- **VER-005** — Compare the undecided matters below with the arrangement and the dispositions, and check for evidence of resolution before any activity that depends on one and that no dependent activity starts before its point of need is met.
- **VER-006** — Review each excluded act in REQ-006 against CLM-003, CLM-004 and CLM-005.
- **VER-007** — Comparison with an outside source: the recorded answer is compared with the owner's own words and with the candidate the owner used, and the observations the owner reported are counted against their dispositions. A recommendation, a passing check or an agent's summary is not the answer.

## Governing Values and Decisions — Axiology

- **AX-001** — The question is whether results merit the attention they demand. Observations improve commitments and practice; nothing assumes that the architecture is beneficial, that findings will be favourable, or that a successor basis must follow.
- **AX-002** — Agreement, use, faithful recording, independent checking, adoption and professional reliance are different facts. Better means a larger share of the owner's observations reaching an owner with a disposition; never by restating an observation more favourably than the owner made it, or by counting a check as use.
- **AX-003** — The owner's judgment is the result. Better means less of the owner's attention spent on arranging and recording for the same observations kept; never by having an agent stand in for the owner's use.
- **TBD-001** — The period and the work of the owner's use are the owner's to choose at the time and are not fixed in advance. Until the owner has used the candidate, verification and validation remain distinct, no use counts as validation, and AC-001 and AC-007 are unmet.
- **TBD-003** — The operation, autonomy and environment of the first connected activity are undecided (owner, through the SWBPIPE session, with the App owner). Validation in SWBPIPE waits for them and for a host candidate. It is held outside 4.0.0 (CLM-006).
- **TBD-004** — First adopters, continuing obligations and the end of coexistence are undecided (owner with the affected consumers). A disposition that proposes adoption or retirement goes to that decision.

## Output and Evaluation Matrix

| Output | Objective refs | Requirement/claim refs | Acceptance refs | Verification refs | Evidence expectation |
|---|---|---|---|---|---|
| OUT-001 | OBJ-008 | REQ-001; CLM-001 | AC-001 | VER-001 | The owner's own words of agreement, compared by an independent reviewer with what the arrangement records (applications, work, period, material and candidates) and with V4-EXM-40. Only the owner's agreement establishes the arrangement; a reviewer can show that the record matches it, not supply it. |
| OUT-002 | OBJ-008 | REQ-002; CLM-002 | AC-002 | VER-002 | Outside source: the owner's own observations while using the candidate. EXAMINATION V4-EXM-41 states the four aims. |
| OUT-002 | OBJ-008 | REQ-003; CLM-004 | AC-003 | VER-003 | Outside source: the act as the person performed it, set against the record. PRD V4-AUT-03 states what may be recorded. |
| OUT-003 | OBJ-008; OBJ-010 | REQ-004; CLM-003 | AC-004 | VER-004 | Each disposition, compared by an independent reviewer with the observation as the owner reported it and with its recipient's own record of decision, or shown as pending where none exists; each method observation also compared with the manual section it cites and the work record that carries the work (EXAMINATION V4-EXM-42, OPERATING_METHOD V4-OPS-20…23). |
| OUT-001 | OBJ-008 | REQ-005; CLM-001; CLM-005 | AC-005 | VER-005 | The arrangement and the dispositions, compared by an independent reviewer with the undecided matters under Axiology and with the decision record of each matter's named owner, for anything stated as decided that its owner has not decided. |
| OUT-003 | OBJ-008; OBJ-010 | REQ-006; CLM-003; CLM-004; CLM-005 | AC-006 | VER-006 | The dispositions and their links, read by an independent reviewer against the allocation of each act in CLM-003 to CLM-005 (the decomposition rows of DEL-09-12, DEL-10-01, DEL-10-02, DEL-04-01, DEL-11-01 and DEL-11-03, and PRD V4-EXT-01 and §8). |
| OUT-002 | OBJ-008 | REQ-007; CLM-001; CLM-002; CLM-006 | AC-007 | VER-007 | Outside source: the owner's own answer, in the owner's words, set against the record of it and the candidate it concerns. Only the owner's yes or no establishes the verdict; a recommendation of readiness does not. |
