---
schema: chirality-deliverable-sow/v1
deliverable_id: DEL-09-10
package_id: PKG-09
decomposition_basis: execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z
project_scope_refs: [SOW-205]
package_objective_refs: [OBJ-007, OBJ-008]
---

# Optional connector consumption witness

## Purpose and Objective Traceability

This deliverable shows, on an identified App candidate, what the App does when an optional connector feed is limited, stale, partial, failing or absent: the limits stay visible, the same coordination question is answered from the project's source files, and a missing feed is never read as empty work, readiness or permission. Where the receiving consumer has actually adopted a connector, it also traces one source identity through that connector to the action it permits. It contributes the V4-EXM-30 case suite and the candidate-bound account of its results. The App connector examination owner integrates it; provider owners supply their own qualification and response evidence. It builds no connector and no fallback.

SOW-205 serves OBJ-007 (explicit receiving contracts and truthful fallback) and OBJ-008 (candidate-specific outcomes that do not overstate partial or unrun evidence). Its sources are PRD V4-CON-01…05 and §3.1, HOST_INTEGRATION V4-HI-60…65 and §8.1, ARCHITECTURE V4-ARC-22, and EXAMINATION §§1–2 and V4-EXM-30. The draft 4.0.0 release target names no exit criterion for this deliverable.

## Deliverable Definition — Ontology

- **OUT-001** — The V4-EXM-30 case suite for the receiving consumer: one coordination question examined with a current feed where a connector is adopted, and with limited, stale, partial, failing and absent feeds, each connector's availability treated independently. Supports SOW-205; OBJ-007 and OBJ-008.
- **OUT-002** — The candidate-bound witness account: for each case, the source, coverage, freshness and standing shown, the conclusions marked as unsupported, the source-file route actually taken and who did the work, the outcome, and the inputs that were missing. Supports SOW-205; OBJ-007 and OBJ-008.

Terms:

- **Feed conditions.** Current: the connector answers within its adopted coverage and freshness. Limited: it answers with stated limits. Stale: its index is older than its sources. Partial: it covers part of the question. Failing: it errors. Absent: it is not running or not adopted.
- **Adopted connector.** A connector whose provider has released it with qualification evidence and which the receiving consumer has recorded as adopted for a stated coverage. An answer from a connector, or its mere presence, establishes neither source correctness, authority to act, nor a human ruling.
- **Source-file fallback.** Answering the coordination question from the project's own files. Agents locate and compare graphs, decisions and revisions; managers keep review and integration; the human carries coordination between undertakings.

Boundary:

- **CLM-001** — Delivery of the PEC connector, its first-consumer examination and its adoption are retired, and no replacement provider is required. The PEC fixtures that remain exercise compatibility of the receiving contract only and stand for no live provider. No connector adoption is required of the receiving consumer; AC-001 applies only to a connector it has adopted.
- **CLM-002** — `DEL-07-01` owns the retained PEC compatibility meaning; `DEL-07-02` owns the App's presentation of connector limits and the source-file fallback; `DEL-08-01` owns the Domains query, admission and freshness contract and its fixtures; `DEL-08-02` owns the later Domains research-to-design witness. SWBPIPE implements its own use of connectors. These are inputs here, and their production stays with their owners.
- **CLM-003** — Provider qualification and publication belong to the provider's owner, adoption to the receiving consumer, and every human act to the person who performs it. This examination records their evidence and its limits.

## Completion and Reliance Basis — Epistemology

- **REQ-001** — For a connector the receiving consumer has actually adopted, one source identity is traced through the connector's answer to the action that answer permits, keeping the examined-through identity, source reference, coverage, freshness, limits and the release and adoption evidence that support the action. A valid envelope or supplied metadata alone is neither a correct covered claim nor a completed witness.
- **REQ-002** — The same coordination question is asked with limited, absent, stale, partial and failing feeds. The unsupported conclusions, the source-file route actually taken and the work done by each fallback actor are observed. Reconstruction from sources is used only where its basis is sound, and what stays unknown or unavailable is recorded. A missing or failed feed never implies empty work, readiness or permission.
- **REQ-003** — The case of the PEC connector absent together with a Domains index older than its sources is kept, observing both the absence and the staleness and the fallback to files. Each connector's availability and limits are distinguished independently: neither is a prerequisite of the other or of independent App work. No provider, database platform, deployment or data destination is selected by a test.
- **REQ-004** — Each result binds candidate, date and configuration and has one of the five examination outcomes. An unqualified delivery is reported as unqualified, and negative, partial, blocked or unavailable evidence does not complete a witness. A changed candidate reopens the affected cases; inspection, prepared tests and component passes do not replace the joined observation.
- **REQ-005** — A provider's release and qualification limits and the consumer's actual adoption are kept when judging a permitted action. A human act actually performed is recorded faithfully, with actor, subject and scope apart from the recorder; no act, approval or professional reliance is inferred from an execution, a recorded approval or a connector's answer.
- **REQ-006** — This deliverable performs no act owned by another, as allocated in CLM-002 and CLM-003.

- **AC-001** — For each connector the receiving consumer has adopted, the trace of one source identity through the connector's answer to the permitted action is complete on the candidate, with source identity, coverage, freshness, limits and release and adoption evidence inspectable. With no adopted connector the case is declared not applicable before the run and passes nothing. Verify by VER-001. [REQ-001; CLM-001]
- **AC-002** — With the feed limited, absent, stale, partial and failing, the candidate answers the same coordination question by showing which conclusions the feed does not support, and the source-file recovery is carried out with its agents, managers and human named, or the reason it could not be is stated. No case shows missing feed data as empty work, readiness or permission. Verify by VER-002. [REQ-002]
- **AC-003** — The case of the PEC connector absent with a stale Domains index is run and its file fallback observed, and the evidence shows each connector's availability separately, with neither implying the other's readiness, and independent App work proceeds with either or both connectors unavailable. Verify by VER-003. [REQ-003]
- **AC-004** — Each result names candidate, configuration and date, its outcome and its evidence limits, and the cases reopened by a candidate change. Fixture and component evidence is never presented as a joined outcome. Verify by VER-004. [REQ-004]
- **AC-005** — The account keeps provider limits, the actual adoption, the undecided matters with their owners and the allocation of CLM-002 and CLM-003. A human act in the trace is recorded with its actor distinct from the recorder, and an absent act is not supplied from anything else. Verify by VER-005. [REQ-005; REQ-006]

## Production and Verification Method — Praxeology

The examination owner identifies the candidate and the receiving consumer, the limit and fallback contribution from DEL-07-02, the Domains contract fixtures from DEL-08-01 and whatever provider evidence exists. Cases use invented material and recorded exchanges where a recording can show the criterion, each marked as replayed, directly observed or supplied by a provider. Interface cases run in WebKit and Chromium with a native package smoke check. Results use the DEL-09-01 record formats and go to independent examination.

- **VER-001** — Follow the source identity, the connector's answer and the receiving action against the consumer's adopted coverage, and check the provider's release and the consumer's adoption evidence. An envelope-only check does not verify the criterion.
- **VER-002** — Compare the limited, absent, stale, partial and failing observations against the same coordination question, follow the fallback sources and each actor's work, and inspect what the candidate shows as unsupported.
- **VER-003** — Run the absent-PEC, stale-Domains case and its file recovery, and compare the availability cases for independence, including continuation of independent work with both unavailable.
- **VER-004** — Audit each result's candidate, configuration and date, its provenance and route, and the cases reopened after a change.
- **VER-005** — Review the account against CLM-001…CLM-003 and the undecided matters below, including the positive record of any human act and the negatives for a fabricated one.

## Governing Values and Decisions — Axiology

- **AX-001** — A connector's availability, its qualified release, a consumer's adoption, operational reliance and a human act are different facts, and none establishes another. Better means more of what a feed did not support made visible to the person at the point of use; never by presenting a feed's silence as an answer.
- **AX-002** — Connectors are optional. Better means the coordination question answered from source files with less unknown left over when a feed is missing; never by making a connector a condition of starting independent work.
- **TBD-002** — Source admission, query, provenance and freshness for Domains, its research workflow and its deployment and data boundary are undecided (owner with the Domains, SWBPIPE and App receiving owners). They bear on the stale-Domains part of AC-003 only through the DEL-08-01 fixtures.
- **TBD-003** — Who builds the Domains provider is undecided (owner with the App, Domains and SWBPIPE definition owners). Nothing here assigns it.

## Output and Evaluation Matrix

| Output | Objective refs | Requirement/claim refs | Acceptance refs | Verification refs | Evidence expectation |
|---|---|---|---|---|---|
| OUT-002 | OBJ-007; OBJ-008 | REQ-001; CLM-001 | AC-001 | VER-001 | Outside source: the provider's own release and qualification evidence and the source file the claim cites. EXAMINATION V4-EXM-30 states the trace. |
| OUT-001 | OBJ-007; OBJ-008 | REQ-002; CLM-002 | AC-002 | VER-002 | Outside source: the project's source files, read directly, give the answer the fallback must reach. PRD V4-CON-03 states what a missing feed may not imply. |
| OUT-001 | OBJ-007; OBJ-008 | REQ-003; CLM-002 | AC-003 | VER-003 | Owner ruling: ARCHITECTURE V4-ARC-22 on independent availability. The stale index is an invented fixture whose age against its sources is set by construction. |
| OUT-002 | OBJ-007; OBJ-008 | REQ-004 | AC-004 | VER-004 | Owner ruling: EXAMINATION §§1–2. An independent reviewer reads the records against the candidate identification. |
| OUT-002 | OBJ-007; OBJ-008 | REQ-005; REQ-006; CLM-002; CLM-003 | AC-005 | VER-005 | Owner ruling: the accepted decomposition's allocation of each act, and the act the examiner watched where one occurs. |
