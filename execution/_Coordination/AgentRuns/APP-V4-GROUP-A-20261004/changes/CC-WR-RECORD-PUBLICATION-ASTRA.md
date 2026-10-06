# CC-WR-RECORD-PUBLICATION — private proposal

2026-10-05. Fresh native Type 2 TASK `/root/group_a_execution_astra/wr_publication_design`, parent `/root/group_a_execution_astra`; no descendants. Bounded WR design-owner contribution; private proposed bytes only. No maintained Design/schema/code writes, adoption, Cargo/Git, native/supplier/network/auth or downloads. Parent retains full lifecycle and archive scope. Selected skill: project proposal-format.

- PROPOSAL: Allocate immutable WR supplier publication under the opened project
  - Evidence: WR §8, §16.1, SC-1/SC-5/SC-6 and SQ-RUN; WR run_text schema explicitly links source bytes rather than copying them. RS §13.7 selects App-local Rust/project storage and forbids fallback; RS W-0…W-2 preserve failure and original pending facts. EXEC SQ-A A-12 preserves ongoing work during recording gaps; the narrower SC-1 publication prerequisite concerns dispatch of this prepared workflow text only.
  - Change: Apply the attached private patch only after named affected independent review and owning-source disposition. It adds WR §16.8 WP-1…WP-7 and a separate versioned envelope schema, preserving all existing body schemas. Exact path `.chirality/records/workflow/<UUID>.json`; exact opaque reference `wr-record:v1:<UUID>`. Explicit owning-project resolver, no-replace immutable publication, original-byte retry, reference-only RS receiving, and visible incomplete recording are specified in the patch.
  - Why: supply durable supplier evidence without treating an in-memory preparation or native page token as a recorded fact.
  - Risk: two-commit WR→RS gaps, source-store loss, unknown project, filesystem durability/containment, collisions, and reader version mismatch require the specified tests. Reference validity alone does not authenticate source or qualify native observation.
  - Status: PROPOSED

Reservation examination: WR §1 excludes shared-type placement from that historical design; U-WR-8 assigns it to App/shared contract owners, and U-WR-2 assigns process placement to App implementation owner. RS §13.7 subsequently records the owner's App-local approval. None of these clauses reserves a new WR subpath decision to the human. LOOP_INIT “Change control” requires named, reviewed changes propagated to consumers. This proposal completes that process; it does not claim an unreviewed subpath was previously selected. No deliverable/DAG/group-order change or new host allocation is proposed. Human gate/acceptance authority is unchanged.

The durable run_text remains metadata/framing plus source reference under its existing schema: no new text snapshot or transcript mirror is introduced. Its App-composed text can be reconstructed only while exact revision bytes resolve; failures are truthful. supply_check stores comparison identities and actual source references, never native pages. Original native turn UUID remains opaque; sibling RS proposal owns its representation and incomparable state. The parent's reported exact832 verified delivery/owned HTTP400 witness remains historical limited delivery evidence; no model uptake, registration, UI or lifecycle qualification follows here.

API fit: publish(explicit project, immutable envelope) → published(ref) or pending/failure; resolve(explicit project, ref) → typed body or explicit resolution limit. RS references use existing evidenceRef shape, kind supply record, with actual resolutionAtWrite; RS must compare thread/nativeTurn and check basis/content. Run-text selection links and check basis links resolve through basis_records while preserving original body identifiers.

MISSING: implementation and affected independent review; connected publication/failure/restart tests; RS receiving adoption. No claim those exist.

NEEDS_HUMAN_RULING: none identified within this bounded owner-directed allocation.

DEPENDENCY_NOTES: WR/RS/Root/EXEC existing Group A joins only. Propagate adopted source to bundled resource/schema registry, publisher/resolver and RS receiving tests; source provenance digest registry if applicable. Broad lifecycle remains deferred to parent-owned assignment. Source-qualified identities and selected-development limits stay intact.

## Inspected origins

- `AGENTS.md` — `f96feb19d297c74e10048c506805b2fe3622c50cfefd6078f599724556113977`
- `agents/AGENT_TASK.md` — `1a13a5b00b3ce01ff8519efe6b46bcbe0cd6a5b7985e24282fa7efa2c57c8fb7`
- `.agents/skills/proposal-format/SKILL.md` — `63e6d2545c31df939511a5a137c214d5444ca562f6abf9b048de3aa2f8dac59d`
- `projects/chirality-app-v4/loop/LOOP_INIT.md` — `c2e88f81439ed03578fee13fd7563082fefdfe11096d9134a59531eba3b985bd`
- `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-02_Workflow-making workspace and registration/Design/WORKSPACE_AND_REGISTRATION.md` — `bd61f48ca97eba9c7665b31ff7506672f18152d57a20b0ffd361a168750af989`
- `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-02_Workflow-making workspace and registration/Design/workspace-registration.schema.json` — `cfd6d3e252b72247d8e1ad0ced3b43b119c5785935002d493407757bd57066e9`
- `docs/alignment-manual/README.md` — `5eee30d902c57a251bf885f91bfa0481a7834ec6945c3382baf15d2e2980c63d`
- `docs/alignment-manual/CHIRALITY_AGENT_USER_MANUAL_v3.md` — `2535efe547f2368e06d965d189efc47c7c46f28c2d6fd4777b0b8cece9003fa7`
- `docs/alignment-manual/Project_Management_for_Human_Agent_Teams_Field_Book_v1.md` — `02d53a3966220001318aacf3f46e1b63b8695a098c81b20f4e3e1531b93024d3`

## Private-byte check

Python parsed the proposed envelope JSON and generated a unified patch without changing maintained sources. Initial example-discovery check failed because examples are JSONL, not individual JSON files; no schema failure was found. Corrected discovery: Draft 2020-12 metaschema and 5 existing valid WR body examples in the proposed envelope passed using locally registered schemas; each rejected an extra native_transcript property. Relation/durability/runtime checks remain pending; this is not implementation evidence.

RS sibling fit: native R3 requires actual resolved run_text/check references and exact thread/nativeTurn/check-state/content correlation. Preserve the actual queried native turn for negative states when known; absence remains pending, never fabricated. Live source receipt authority cannot be recreated by JSON reread.
