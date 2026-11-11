---
schema: chirality-deliverable-sow/v1
deliverable_id: DEL-03-01
package_id: PKG-03
decomposition_basis: execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z
project_scope_refs: [SOW-018, SOW-067, SOW-068, SOW-069, SOW-072, SOW-157, SOW-158, SOW-159, SOW-160, SOW-161, SOW-162, SOW-163, SOW-164, SOW-165, SOW-166, SOW-167, SOW-168, SOW-169]
package_objective_refs: [OBJ-004, OBJ-005]
---

# Capability catalog and read-basis contract

## Purpose and Objective Traceability

This deliverable contributes one definition of what a host's capability catalog says and what a read through it returns. With it, the person, the host's embedded agent and an external agent mean the same thing by an operation, by the reason it is unavailable, by the content and standing of a read, and by the basis a later action cites. The App/shared capability-contract owner produces the definition: its schemas, the map of which surfaces are generated from the catalog, and the fixtures that exercise them. Each host builds its own catalog and supplies its own tables, results and diagnostics.

It serves OBJ-004 by giving the three kinds of consumer a common operation meaning, and OBJ-005 by keeping a read's standing and basis attributable and no stronger than the host gives. Its sources are PRD V4-HOST-03, V4-PAR-01…03, V4-PAR-05, V4-AUT-03, OQ-02, OQ-10 and OQ-11; HOST_INTEGRATION §§1–3 (V4-HI-01…04, V4-HI-10…12) and V4-HI-30…32; ARCHITECTURE V4-ARC-20…21; and EXAMINATION V4-EXM-21, V4-EXM-24 and V4-EXM-25. The draft 4.0.0 release target names no exit criterion for this deliverable; the live SWBPIPE journey of its criterion 5 is read and judged in this contract's terms.

| Assigned scope | Local contribution | Output |
|---|---|---|
| SOW-018 | Semantic parity between person and agent across reads, operations, results and recovery, with human acts kept separate | OUT-001; OUT-002 |
| SOW-067, SOW-068 | Reads and changes described once, in one catalog that all three surfaces use | OUT-001; OUT-002 |
| SOW-069, SOW-166 | A read returns the person's tables, results and diagnostics with the same standing; an unavailable operation has the same result and reason for everyone | OUT-001; OUT-003 |
| SOW-157 to SOW-164 | The fields every entry declares, including its human-act and autonomy class | OUT-001 |
| SOW-072, SOW-165 | Which surfaces are generated from or checked against the catalog, what each adapter still does, and the extension promise kept apart | OUT-002 |
| SOW-167, SOW-168 | Every read returns its basis, and a later action cites the basis it relied on | OUT-001; OUT-003 |
| SOW-169 | Results show current or historical standing, checks passed and limitations, never stronger for an agent | OUT-001; OUT-003 |

## Deliverable Definition — Ontology

- **OUT-001** — The catalog and read-basis schemas: a catalog edition as a consumer discovers it, the event by which a host reports a new edition, and a read result with its non-success forms. Each has valid and invalid example documents, and each carries the conformance rules a schema cannot express. A document a host supplies either conforms or is refused with the rule it failed. Supports SOW-018, SOW-067, SOW-068, SOW-069, SOW-157 to SOW-164 and SOW-166 to SOW-169; OBJ-004 and OBJ-005.
- **OUT-002** — The generated-surface and adapter-responsibility map: for the human interface, the embedded tools and the external interface, what is generated from the catalog, what is checked against it, what is hand-built, what each adapter still implements and who receives each part. It carries the extension promise and its route to a decision. Supports SOW-018, SOW-067, SOW-068, SOW-072 and SOW-165; OBJ-004.
- **OUT-003** — Contract fixtures and their comparison results for availability, reads, basis and standing across the three surfaces, including current and historical reads, unavailable operations and later-action basis references. They include the shared fixture catalogue FX-PIPE-01 and the simulated host SH-1, which other deliverables use as their test double. Supports SOW-018, SOW-069, SOW-160, SOW-162 and SOW-166 to SOW-169; OBJ-004 and OBJ-005.

Terms:

- **Surfaces.** The human interface (H), the host's embedded agent (E) and an external agent (X): three ways to reach the same operation.
- **Catalog edition.** One published set of entries of one host, named by host identity and edition identity; a host reports a new edition by an edition-change event, and a consumer computes no edition identity.
- **Entry.** One operation a person can perform, read or change. It declares a stable identity and a version; a purpose a person and an agent both read; a schema for its arguments (each argument's name, kind and whether it is required); its preconditions, each with the reason given when it does not hold; its effects (none, or the kinds of object it changes); a schema for its result, including standing and the host checks it may report; its errors, each with an identity, a meaning, where it is raised and its effect (none, partial or unknown); its class; and its exposure on each surface.
- **Class.** None; may apply within granted autonomy; proposal only; reserved to the person; or *no policy basis*, with its reason (omitted, unassigned, or awaiting an operation-specific ruling). The values and the reserved acts are those of the operation policy that `DEL-04-01` carries.
- **Exposure.** Per surface, whether the entry is exposed; declared by the host and independent of class.
- **External contact.** For an entry through which a host's embedded agent reaches a network destination: the destination category and whether the destination is fixed or taken from a named argument of that entry. The catalog also carries the host's destination-request entry, through which its agent asks the person for a destination.
- **Read basis.** Workspace identity, generation, model revision and canonical content identity, the last with the designation of the method that produced it.
- **Subject content identity.** A host-supplied identity of one object or row in a read, with its method designation, distinct from the read-level identity. A whole-model identity, where that is all a host supplies, stands for every subject it covers.
- **Non-success results.** Unavailable (a named precondition does not hold, with its reason and the basis evaluated); not permitted; not exposed on this surface; channel not enabled; and error (a declared error). Each names who reports it. None is a success with empty content.
- **Standing.** Current or historical; the named host checks passed or failed, with the basis they evaluated; known limitations; and any human act the host evidences, carried by reference with its lapse state. An agent's finding is never shown as a check or as a person's act.
- **Evidence kinds.** Illustrative (supports the definition only), test-double (holds for that double) and actual host (holds for that candidate).
- **FX-PIPE-01 and SH-1.** FX-PIPE-01 is one invented piping model with its catalog entries and one timeline of revisions with named variants. SH-1 is one simulated host holding that state, reached over both native paths: an MCP tool path and a command-line path.

Boundary:

- **CLM-001** — The App/shared capability-contract owner owns this definition, the map and the fixtures. Each host owner, SWBPIPE's own project for the first host, owns its catalog, its domain objects and truth, its tables, results and diagnostics, its content identities, validation and application, receipts and interface. A host offers, records and presents human acts; the person performs them.
- **CLM-002** — `DEL-03-02` owns the proposal, validation and outcome contract and takes operation identity and the read basis from here. `DEL-03-03` owns the App's external receiving. `DEL-04-01` owns the operation policy and its classes. `DEL-04-03` owns the act record's field set and lapse vocabulary, which a read's standing carries without redefining. The loop and panel schemas of `DEL-05-01` and `DEL-05-02` are checked by the same mechanism as this contract's and stay theirs.
- **CLM-003** — `DEL-02-01` and `DEL-02-03` use entries as the descriptors of a workflow's required tools. Whether the extension promise is kept, narrowed or deferred is the owner's decision with the host contract owner (TBD-002); `DEL-09-09` traces one new operation as the evidence for it.

## Completion and Reliance Basis — Epistemology

- **REQ-001** — A host's reads and changes are described once, and the human interface, the embedded agent and an external agent use that one meaning. Parity is of meaning, standing and recovery; identical gestures are not required. A consumer resolves every operation reference against an identified catalog edition. [SOW-018, SOW-067, SOW-068; V4-HI-01, V4-HI-03]
- **REQ-002** — Every entry declares the elements listed under *Entry*. Its class is drawn from the adopted operation policy, and an operation without an adopted class says so (*no policy basis*) and is never silently treated as reserved. Exposure is declared per surface and independently of class. An entry through which a host's embedded agent reaches a network destination carries its external-contact declaration, and the catalog carries the destination-request entry and the non-success results for a destination the person has not allowed. [SOW-157 to SOW-164; V4-HI-02; PRD V4-HOST-02]
- **REQ-003** — A read returns the tables, results and diagnostics the person sees, with the same standing. An operation unavailable to the person is unavailable to the agents with the same result and the same reason. [SOW-069, SOW-166; V4-HI-04, V4-HI-10]
- **REQ-004** — Every read carries its basis, and each object or row carries its subject content identity. The App computes no host identity. A later action cites the basis of the read it relied on, and that citation is never replaced by a queue-time or newly selected basis. [SOW-167, SOW-168; V4-HI-11, V4-HI-32]
- **REQ-005** — A read result shows whether it is current or historical, the checks it passed and its known limitations, and an agent-facing form never states more than the host gives. Execution, checking, the acceptance of a proposal, approval and professional reliance are separate subjects with their own actors: a success establishes none of the others, and none of these acts is made a prerequisite of another independently evidenced act. A human act the host evidences may be reported faithfully, with the person as its actor and the recorder named apart. [SOW-169, SOW-018; V4-HI-12, V4-HI-25, V4-HI-31; PRD V4-AUT-03]
- **REQ-006** — The map names each of the three surfaces, states for each part whether it is generated from the catalog, checked against it or hand-built, and what its adapter still implements, and names who receives each part. It presumes no common service and no provider-specific schema, and it keeps the original promise that a new operation reaches every actor without separate work as undecided. [SOW-072, SOW-165; V4-HI-03; V4-ARC-20]
- **REQ-007** — This deliverable performs no act owned by another, as allocated in CLM-001…CLM-003: it builds no host catalog, computes no domain result, validates or applies nothing, produces no receipt and performs no human act; and it defines no proposal contract, external receiving, policy or record format.

- **AC-001** — One catalog definition covers every element of an entry and both reads and changes. A conforming catalog document is accepted; one that lacks a required element, repeats an operation identity or an argument name, or names a destination argument its entry does not declare is refused with that rule. The examples keep operation identity and version apart from read basis, and an adopted class is distinguishable from an unresolved one. Verify by VER-001. [REQ-001; REQ-002]
- **AC-002** — For the same operation and basis, the read documents for H, E and X carry the same tables, results, diagnostics and standing. The comparison states the evidence kind for each surface and lists what is absent. Verify by VER-002. [REQ-001; REQ-003]
- **AC-003** — An operation whose precondition does not hold gives the same unavailable result, reason and evaluated basis on all three surfaces, and never a success with empty content. Verify by VER-003. [REQ-003]
- **AC-004** — Every fixture read carries all four basis elements: workspace identity, generation, model revision, and canonical content identity with its method designation. Each object or row of a fixture read carries a subject content identity with its method designation, supplied by the host, and no identity in a read is computed by the App. A later action names the basis of the read it relied on and still names it after an intervening change. A serialization or identity method not yet agreed is named as such and not supplied as an invented field. Verify by VER-004. [REQ-004]
- **AC-005** — Read fixtures show current and historical standing, the checks passed and the limitations. A successful operation or an agent's finding carries no human act, and an act the host evidences is carried with the person as actor and the recorder apart. No fixture gives an agent a stronger standing than the host's. Verify by VER-005. [REQ-005]
- **AC-006** — The map accounts for all three surfaces: what is generated, what is checked, what is hand-built, the adapter work that remains, and who receives tool descriptors (`DEL-02-01`, `DEL-02-03`), operation identity and basis (`DEL-03-02`) and the policy class (`DEL-04-01`). It counts matching types as no evidence of an integrated consumer. Verify by VER-006. [REQ-006]
- **AC-007** — The map states the original extension promise, states that it is undecided, and names the trace of one new operation and the owner's decision that fixing its criterion needs. It claims no automatic availability and no saving, and selects no narrower criterion. Verify by VER-007. [REQ-006]
- **AC-008** — Across the three outputs, every act REQ-007 excludes is assigned to its owner, every open input has its owner, its point of need and its consequence, and a host's conformance is stated only on that host's own documents. Verify by VER-008. [REQ-007]

## Production and Verification Method — Praxeology

The schemas are JSON Schema documents with valid and invalid instances. Their property names are this contract's own labels: they select no host or supplier wire field, transport, identity algorithm or placement, and identities are opaque strings. Rules a schema cannot state are part of the contract and are checked with it: operation identities are unique within an edition and argument names within an entry; a destination taken from an argument names an argument of its entry; and a successful read names the edition discovered, an operation and version in it, a surface on which that entry is exposed, and only host checks the entry declares. A host document is kept as supplied beside anything derived from it. One fixture catalogue and one simulated host serve every deliverable that needs a test double, so their results can be compared.

- **VER-001** — Executable check (observes each example and each altered catalog document accepted or refused with its rule) and comparison with a named reference (the field list of HOST_INTEGRATION V4-HI-02): every element of an entry, the identity and version distinction and the adopted or unresolved class.
- **VER-002** — Comparison with a named reference (the read documents of the same operation and basis on H, E and X): table, result, diagnostic and standing content, with the evidence kind recorded for each surface.
- **VER-003** — Executable check (observes the result of a call whose precondition does not hold, on each surface): the same unavailable result, reason and evaluated basis, and no empty success.
- **VER-004** — Executable check (observes the four basis elements of each fixture read, the subject content identity and method designation of each object or row with the party that supplied them, and the basis a later action names, before and after an intervening change): every element is present, every identity is the host's, and the original basis is kept.
- **VER-005** — Executable check (observes the standing in current and historical read fixtures, and what a successful operation, an agent's finding and a host-evidenced act each carry): standing is no stronger than the host's and no act is inferred.
- **VER-006** — Judgment by an independent reviewer: reads the map against the three surfaces, CLM-001…CLM-003 and the decomposition's interfaces, checking each generated or checked part for its conformance route and each open allocation for its owner.
- **VER-007** — Comparison with a named reference (PRD V4-PAR-05 and OQ-10, EXAMINATION V4-EXM-24): the map's statement of the promise, its undecided standing and the trace and decision it names.
- **VER-008** — Judgment by an independent reviewer: audits each excluded act against its owner and each open input for owner, point of need and consequence.

## Governing Values and Decisions — Axiology

- **AX-002** — One meaning on every surface, and decision rights left with the person. Better means fewer differences between what an entry or a read says on H, E and X for the same operation and basis; never by weakening a precondition, a reason, an error or a standing mark, and never by attributing a human act.
- **AX-003** — Shared meaning does not prescribe shared construction. Better means more of the contract checkable on a supplied document, so that a nonconforming catalog or read is refused with its rule; never by selecting a host wire field, an identity algorithm or a common service that its owners have not agreed.
- **TBD-001** — Which operations carry a reserved or other class beyond the adopted first-increment policy is undecided (owner with the affected App and host design owners). Until ruled, such an entry is *no policy basis* and nothing that depends on its class is claimed. Whether a host adopts and enforces the policy is that host's to evidence.
- **TBD-002** — Whether the promise that a new catalog operation reaches the person and both agents without separate work is retained, narrowed to defined generated surfaces or deferred is undecided (owner with the host contract owner). AC-007 fixes no criterion before that decision.
- **TBD-003** — Where the catalog schemas and any shared checker are placed, how a host serializes its catalog and reads, the content-identity algorithm and the scheme of method designations are unagreed (App/shared capability-contract owner with the affected host and consumer owners). The semantic fields are fixed; no wire name, hash algorithm or common service is.
- **TBD-004** — The operation, the autonomy permitted and the candidate environment of the first connected activity are undecided (owner, through the SWBPIPE session, with the App owner), and SWBPIPE's actual catalog, tables, diagnostics, availability and basis are its own to supply. No conformance is stated for that host before them.

## Output and Evaluation Matrix

| Output | Objective refs | Requirement/claim refs | Acceptance refs | Verification refs | Evidence expectation |
|---|---|---|---|---|---|
| OUT-001 | OBJ-004, OBJ-005 | REQ-001; REQ-002; CLM-001; CLM-002 | AC-001 | VER-001 | Owner ruling: HOST_INTEGRATION V4-HI-02 lists the fields and PRD V4-HOST-02 the destination elements. The example documents are the product's own and guard only against change. |
| OUT-003 | OBJ-004, OBJ-005 | REQ-001; REQ-003; CLM-001 | AC-002 | VER-002 | Owner ruling: PRD V4-PAR-03 and HOST_INTEGRATION V4-HI-10 say the views and standing are the same. On SH-1 the comparison is between the product's own documents and guards against change; an actual host's documents on its three surfaces are the independent comparison. |
| OUT-003 | OBJ-004 | REQ-003 | AC-003 | VER-003 | Owner ruling: HOST_INTEGRATION V4-HI-04 says the reason is the same. Observed on SH-1 as a guard against change; independently on an actual host's surfaces. |
| OUT-003 | OBJ-004 | REQ-004; CLM-002 | AC-004 | VER-004 | Owner ruling: HOST_INTEGRATION V4-HI-11 names the basis elements and says a later action cites the basis relied on. The expected basis and subject content identities of each step are those the fixture timeline states before the run. |
| OUT-003 | OBJ-004, OBJ-005 | REQ-005; CLM-001 | AC-005 | VER-005 | Owner ruling: HOST_INTEGRATION V4-HI-12, V4-HI-25 and V4-HI-31 and PRD V4-AUT-03 say what standing and which acts may be shown. |
| OUT-002 | OBJ-004 | REQ-001; REQ-006; CLM-001; CLM-002; CLM-003 | AC-006 | VER-006 | Owner ruling: HOST_INTEGRATION V4-HI-03 and ARCHITECTURE V4-ARC-20, with the decomposition's allocation of each receiver. |
| OUT-002 | OBJ-004 | REQ-006; CLM-003; TBD-002 | AC-007 | VER-007 | Owner ruling: the original promise in PRD V4-PAR-05 and the treatment OQ-10 requires. |
| OUT-002 | OBJ-004, OBJ-005 | REQ-007; CLM-001; CLM-002; CLM-003; TBD-001; TBD-002; TBD-003; TBD-004 | AC-008 | VER-008 | Owner ruling: the accepted decomposition's allocation of each act and the open issues' named owners. |
