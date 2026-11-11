---
schema: chirality-deliverable-sow/v1
deliverable_id: DEL-09-11
package_id: PKG-09
decomposition_basis: execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z
project_scope_refs: [SOW-206]
package_objective_refs: [OBJ-005, OBJ-008]
---

# Later run reconstruction witness

## Purpose and Objective Traceability

This deliverable shows that the records of a host run stand on their own. A week after one identified V4-EXM-20 journey, a named reader who took no part in it reconstructs, from the project's files and the host's receipts alone, what was asked, what the agent proposed, what the engineer accepted and what changed, and says plainly what cannot be known. It contributes that witness and the reader's account. The App evidence examination owner integrates it. It writes no record format and runs no host journey.

SOW-206 serves OBJ-005 (attributable human acts, standing and provenance) and OBJ-008 (candidate-specific examination that does not overstate partial evidence). Its sources are PRD V4-REC-01, V4-REC-03…05 and V4-AUT-01…05, HOST_INTEGRATION V4-HI-25, 30…33 and 70…71, and EXAMINATION §§1–2 and V4-EXM-31. The draft 4.0.0 release target names no exit criterion for this deliverable.

## Deliverable Definition — Ontology

- **OUT-001** — The V4-EXM-31 witness: one reconstruction, by a named reader separate from the run's authors, of one identified V4-EXM-20 host journey a week after it, with the input set supplied, both dates, and the result. Supports SOW-206; OBJ-005 and OBJ-008.
- **OUT-002** — The reader's account: the request, the agent's proposal, the engineer's actual acceptance and the actual change, each with its sources and the host's receipt references, the content, scope and purpose of each human act, any lapse, and the unknowns. Supports SOW-206; OBJ-005 and OBJ-008.

Terms:

- **Run authors.** Everyone who took part in the source journey: the person who acted, the host agent's session, the recorders, the dossier's assembler and the examiner. The reader is none of them.
- **Reader.** A named person or agent. A person states that they took no part in the run. An agent is a fresh instance whose supplied context is recorded: the brief, the input-set manifest and the files, each by content hash, and nothing else, with its host's access limits stated as enforced or only instructed. A supplied context that includes anything beyond the brief, the manifest and the input set means separation is not established.
- **Input set.** The files given to the reader, each with a content hash and a standing: a record, a project file the run wrote, host evidence by reference, a definition (which may support a check and never an act or an outcome), or not authority (present only to test that the reader does not rely on it). The run's harness session and conversation stores, the author's working memory and derived views are withheld and named as withheld.
- **Claim standing.** Each claim in the account is from records, inferred (stated as inference, with its sources) or unknown. A decision or acceptance is claimed only with both its actor and its recorder.
- **A week after.** As EXAMINATION V4-EXM-31 writes it; this scope fixes no calendar date. An immediate reread, a schedule or a synthetic clock does not meet it.

Boundary:

- **CLM-001** — `DEL-04-03` owns the run and decision record format, the App's writer and reader of it, and the handling of lapse. `DEL-09-07` owns the V4-EXM-20 journey, its dossier and the host receipt references this witness reads. `DEL-09-01` owns the examination record formats. The reconstruction of the App's own runs from its records store has no examination criterion yet and is not part of this witness.
- **CLM-002** — SWBPIPE's own project owns the host, its domain truth, its validation, application and solve, its receipts, hashes and origin marks, and the run record of a host-agent run (HOST_INTEGRATION V4-HI-70). The host offers, records and presents human acts; the person performs them; the accountable professional decides professional reliance.
- **CLM-003** — The witness examines the operation policy that was actually in force for its source journey and decides none. Routine permission settings never establish a human or professional act.

## Completion and Reliance Basis — Epistemology

- **REQ-001** — The witness uses one identified V4-EXM-20 record set and a named reader separate from the run's authors, and records the journey date and the reconstruction date, each with its source. A plan, an immediate reread, or elapsed time without an actual reconstruction is not the witness.
- **REQ-002** — From the project's files the reader recovers the request, the proposal, the engineer's actual acceptance and the actual changes, and traces workflow source identity and version, conversation, model, autonomy settings, requested operations and observed outcomes through the run record to the host's receipts, hashes and origin marks. Receipt references are kept as references; no second copy of the host's truth is made.
- **REQ-003** — Each reconstructed human act keeps its actual actor apart from its recorder, its content, scope and purpose, and any visible lapse where its bound content changed. Proposing, applying, accepting an edit, checking, engineering approval and professional reliance are separate acts; evidence of one establishes none of the others, and the account adds no order between independently evidenced acts beyond what the records and the operation policy in force require. Tool success, silence, a resolved source or a successful transport is never promoted into a human act or an unobserved outcome.
- **REQ-004** — The reader relies only on the project's source records and the linked host evidence. Private agent memory, a harness transcript or session store, and a derived view may help locate evidence and are never authority. Missing, conflicting, inaccessible or unobserved evidence is identified as such.
- **REQ-005** — Each result names candidate, configuration, date, reader and source run, has one of the five examination outcomes, and keeps observation apart from inference. An earlier candidate's pass supports that candidate only. A successful reconstruction speaks only to the acts recorded and requires no new approval, validation or reliance.
- **REQ-006** — This deliverable performs no act owned by another, as allocated in CLM-001, CLM-002 and CLM-003.

- **AC-001** — A reader who is not among the run's authors has actually reconstructed one identified V4-EXM-20 journey from a supplied input set whose every item matches its recorded hash, the examiner states, from the two evidenced dates read against V4-EXM-31's wording, whether a week has passed, and the record shows that the source run had ended and that none of its sessions was supplied to the reader. Verify by VER-001. [REQ-001]
- **AC-002** — The account reconstructs the request, the proposal, the engineer's acceptance and the change, every claim cites items in the input set, and every claimed change traces to a host receipt, hash or origin reference resolved at the time of reading. A reference that does not resolve is reported as unresolvable and the change is not claimed; AC-002 is then not met for that change. Verify by VER-002. [REQ-002]
- **AC-003** — Every reconstructed act names the recorded actor and recorder, distinct from each other, with its content, scope and purpose, and exactly what was recorded; an act whose bound content has changed is shown as lapsed; and the account contains no acceptance, check, approval or reliance that the records do not hold. Verify by VER-003. [REQ-003]
- **AC-004** — Where the records do not show a host or provider outcome, the account says unknown, even where the source resolved or the transport succeeded; and no claim rests on an item marked not authority, on a withheld source, or, for an act or an outcome, on a definition. Verify by VER-004. [REQ-004]
- **AC-005** — The witness and the account identify candidate, source run, reader, dates and configuration, state the outcome and its limits, and name the checks to revisit when the candidate or its basis changes. Neither is presented as validation of the product, human approval or professional reliance. Verify by VER-005. [REQ-005]
- **AC-006** — The account identifies the records and the journey evidence actually supplied and who supplied them, the boundary with the host, and any undecided matter that bears on a criterion, and keeps each excluded act with its owner. Verify by VER-006. [REQ-006; CLM-001; CLM-002; CLM-003]

## Production and Verification Method — Praxeology

The examination owner identifies the source journey and its records, assembles the input set with its manifest, and assigns the reader. The reader first checks every item against the manifest and stops if any differs; then reconstructs the request, the proposal, each human act, what changed, lapse, and the unknowns, in that order, citing sources by path. The examiner derives the truth from the records, never from the account, and compares. The witness is scheduled so that it holds up no other work. Fixture exercises of the reading method keep their own identity and never stand for the witness.

- **VER-001** — Examine the source journey's evidence, the reader's separation evidence, the input set's hashes and both dates, and the reader's actual return. Record a missing journey, an unseparated reader or unmet timing as an unfulfilled witness.
- **VER-002** — Trace each assertion about request, proposal, acceptance and change to items in the input set and to the host's receipt, hash or origin references, resolving each. Check that every act-bearing item is reconstructed, or its absence stated.
- **VER-003** — Compare each reconstructed act with its record: actor, recorder, content, scope, purpose and alternative. Inspect lapse against identified content-change evidence; where the source journey contains no change to an act's bound content, examine lapse on a separately identified content-change fixture and keep that result's provenance apart from the witness. Check that no act is fabricated, altered, upgraded or denied.
- **VER-004** — Compare the account with the gaps in the sources, including an outcome that was not observed although its source resolved. Check that nothing withheld or not authority supports a claim. A claim of change that cites no change record is referred to the examiner, whose recorded judgment decides between a stated absence and an unsupported claim.
- **VER-005** — Inspect the result's identity, outcome, limits and applicability after change, and check that its conclusion reaches only the reconstructed journey.
- **VER-006** — Compare the account of inputs and responsibilities with CLM-001, CLM-002 and CLM-003, keeping proposed, received, adopted and executed contributions apart.

## Governing Values and Decisions — Axiology

- **AX-001** — Source authority, truthful standing and recoverable content identity govern the witness. Faithful recording of an act actually performed is what is being read for. Better means a larger share of the account's claims standing from records with receipts that still resolve; never by letting an inference or a recollection stand as a record.
- **AX-002** — The evidence is proportionate to its reader. Owning records are linked, and no second store of host truth or authority is built. Better means a reader needs fewer items outside the run record to reconstruct the journey; never by supplying the reader with the run's sessions or the author's context.
- **AX-003** — Only an actual reconstruction of an actual journey is the witness. Validation in use, replacement and professional reliance keep their own subjects and their own human acts.
- **TBD-001** — Whether the host's receipts for the source journey will still resolve a week later depends on SWBPIPE keeping them beyond the session, which is its owner's decision. If they do not, each receipt reference is reported as unresolvable, no change is claimed, and AC-002 cannot be met on that journey.
- **TBD-003** — The operation, autonomy and environment of the source journey are undecided (owner, through the SWBPIPE session, with the App owner) and reach this witness through DEL-09-07. The witness cannot be run before that journey has been.

## Output and Evaluation Matrix

| Output | Objective refs | Requirement/claim refs | Acceptance refs | Verification refs | Evidence expectation |
|---|---|---|---|---|---|
| OUT-001 | OBJ-005; OBJ-008 | REQ-001; CLM-001 | AC-001 | VER-001 | The journey's date from the DEL-09-07 dossier and the reconstruction's date from the reader's return, judged by the examiner against V4-EXM-31's "a week after V4-EXM-20"; the input set compared item by item with its manifest; and the reader's separation, shown by a record written by whoever dispatched the reader, compared with the dossier's list of everyone who took part in the run. For an agent reader, the dispatch record shows what was supplied; it shows that nothing else was available only so far as the host enforced the reader's access limits. |
| OUT-002 | OBJ-005; OBJ-008 | REQ-002; CLM-001; CLM-002 | AC-002 | VER-002 | Outside source: the host's own receipts, hashes and origin marks, resolved at reading. The examiner derives the expected account from the records independently of the reader. |
| OUT-002 | OBJ-005; OBJ-008 | REQ-003; CLM-002 | AC-003 | VER-003 | The source journey's act records, as examined in DEL-09-07 against the acts its examiner watched. No independent grounds here: they are the product's own earlier output, so this criterion shows the reader recovers them unchanged and not that they were right. |
| OUT-002 | OBJ-005; OBJ-008 | REQ-004 | AC-004 | VER-004 | The examiner's own reading of the gaps in the records, made without the account, compared claim by claim with the account's unknowns, and each cited item's standing in the manifest (not authority, withheld, definition) checked against the claim it supports. |
| OUT-001 | OBJ-005; OBJ-008 | REQ-005 | AC-005 | VER-005 | The result record and the account, compared by an independent reviewer with the candidate identification, the configuration and dates actually examined and the outcome rules of EXAMINATION §§1–2, and their conclusion read for any claim beyond the reconstructed journey. |
| OUT-002 | OBJ-005; OBJ-008 | REQ-006; CLM-001; CLM-002; CLM-003 | AC-006 | VER-006 | The account's statement of inputs, suppliers and boundaries, compared by an independent reviewer with the allocation in CLM-001 to CLM-003 (the decomposition rows of DEL-04-03, DEL-09-07 and DEL-09-11, and HOST_INTEGRATION V4-HI-70 and V4-HI-71) and with the dossier and records actually supplied. |
