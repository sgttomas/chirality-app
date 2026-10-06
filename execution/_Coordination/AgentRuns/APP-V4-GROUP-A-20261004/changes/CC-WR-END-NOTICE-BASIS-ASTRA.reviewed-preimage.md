# CC-WR-END-NOTICE-BASIS — bounded source clarification

2026-10-05. WR TASK `/root/group_a_execution_astra/wr_publication_design`, parent `/root/group_a_execution_astra`; no descendants. Source fit only, no Cargo or maintained/private implementation changes. REC owns the Cargo lane. Project proposal-format remains selected.

- PROPOSAL: Bind an end notice to its original published run start
  - Evidence: Actual `PreparedRunText::end_notice` at workflow_workspace.rs lines 871–898 emits validated run_text with purpose/run/conversation/lines/text identity/size, without workflow or workflow_file. WR schema's end-notice branch forbids workflow_file and chain and does not require a tuple. Existing WP-2 names start→selection and check→run_text but leaves end-notice source lineage unspecified; its generic purpose-agreement wording is insufficient for a different-purpose relation. Frozen WR implementation consequently permits zero end-notice basis; RS's unconditional workflow lookup cannot receive the actual producer output.
  - Change: Apply the attached narrow delta to the reviewed WR §16.8 proposal only after owning-source review/disposition. Require exactly one end-notice basis: the original published run-start for the same run/conversation, resolved through original selection in the same project. Narrow correspondence by relationship, preserve original body schemas and envelope schema, and derive only sourceIdentity from original start while content remains exact end-notice text identity.
  - Why: actual producer output becomes resolvable without copying or inventing workflow tuples or confusing start text with end text.
  - Risk: existing private end-notice envelopes with zero basis become incomplete under the clarified relationship; never silently retrofit them. Historical source evidence remains historical. A wrong original run or selection must refuse receiving. This is a named source change, not a helper guess or human acceptance.
  - Status: PROPOSED

The private source delta is based on applying the prior CC-WR-RECORD-PUBLICATION proposal (heading16.8) to the frozen maintained WR document. It changes WP-2 only. Envelope/body schema bytes remain unchanged. Prior implementation patch remains SHA-256 `84f238d583c8fd25a4ac71abb2c68541dc68773e30295bddb0134bd43528f784`; no code repair is represented as warranted yet.

Concrete receiving API after source disposition: `PreparedEndPublication::new(project, prepared, end, original_start: &ResolvedRecord, writer, observed_at)`. Require original_start same physical opened-project identity, record_kind run_text, purpose run start, exact prepared run/conversation/workflow/source scope, and original start resolved through selection. Set new end envelope basis_records to that original reference; preserve actual `prepared.end_notice(end)` body unchanged. Resolver follows end→start→selection, rejecting cycles by typed expected kind/purpose/depth. RS receives the resolved original start as a third historical typed record or resolves the single basis itself; it uses original start.workflow for sourceIdentity and end_notice.text_identity for content. check→end still matches purpose and exact text identity. No JSON or cold resolution gains live authority.

Preserved original negative: the frozen typed producer test `typed_publication_retains_prepared_text_and_refuses_lost_source_or_development` actually calls end_notice through PreparedEndPublication and validates the resulting body. It passed in the frozen 56-test binary. RS must retain a regression using this actual producer body, asserting workflow/workflow_file absent and previous unconditional source lookup fails, then demonstrate receiving through original start after repair. A start fixture renamed to end-notice is not this case. Source validation, negative cross-run/conversation/project/selection references and no-start/missing-start cases are required before amended implementation readiness.

MISSING: source review/disposition, then WR/RS private repairs and actual producer regression with granted Cargo lane.

NEEDS_HUMAN_RULING: none identified; this remains named owning-source change control inside existing Group A allocation.

DEPENDENCY_NOTES: WR supplies immutable relation and resolver, RS receives source identity, Root later integrates original-start custody with actual end lifecycle. No lifecycle expansion, native constructor, registration, live R3 authority or maintained adoption.

Patch SHA-256: `157f0844d2246b39215555b57329ae3ebbe1cd3c89f39c0250c0f81ac896e5cb`.
