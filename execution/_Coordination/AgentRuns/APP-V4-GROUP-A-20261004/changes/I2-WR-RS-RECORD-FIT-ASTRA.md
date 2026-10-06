# WR → RS record-publication source fit

2026-10-05; fresh Astra/low native TASK `/root/group_a_execution_astra/workflow_record_lifecycle_fit`, parent `/root/group_a_execution_astra`. Source-fit continuation only. No code, Design, schema, graph or adoption changes; no Git, Cargo, tests, supplier/native execution or home inspection. The sole write is this report. Selected skill: project `proposal-format`, `.agents/skills/proposal-format/SKILL.md`. Prior report's instruction basis remains unchanged. No descendants.

## Determination

The existing source-owned delivery/comparison pipeline needs no replacement. A complete RS R3 mapping from every current WR check cannot yet be specified from the inspected accepted interfaces. This is narrower than “string and integer types conflict”: RS's turn is a Chirality record field, not selected as a supplier wire field; a legitimate separately established numeric turn could coexist with the opaque native ID in WR evidence. However no adopted mapping or producer of that number was found. Workflow-text R3 requires the number, rather than merely permitting it. Incomparable is a separate definite receiving omission.

### Exact legal mapping under the current contracts

RS `suppliedGuidance` requires `supplyForm`, `sourceIdentity`, `content`; App forms additionally require `supplyRecord`; workflow start/end forms additionally require `turn` and `supplyCheck` through the second `allOf` clause (RS schema lines 2044–2145). Thus `turn` is optional for some other forms but **not** for these workflow forms. Its type is integer ≥1. The schema's opening description explicitly says names are Chirality's and “no host or supplier wire field is selected.” Examples use positive numeric turns (chained-run start 6, end 9); these support a numeric record coordinate, not a UUID conversion. Neither the inspected RS/EXEC definitions, examples, maintained runtime/records code nor CONTRACT_ISSUES supplies its numbering domain, completeness rule or native-ID map. Do not assign 1 per workflow run, parse/hash a UUID, use request/receipt position, count a partial history page, or claim that an example number establishes an adopted ordinal algorithm.

Where an owning producer actually supplies an established numeric turn, the existing legal R3 body is:

- `supplyForm`: exact start/end-notice form; `thread`: actual conversation.
- `turn`: that producer's established positive integer, with native turn string retained exactly in the referenced WR check. Identity equality between those two values is never claimed.
- `sourceIdentity`: exact workflow source identity, retaining tuple/source root/revision via the supplier record; no holding-library substitution.
- `content`: composed text's exact method/value (RS R3 expressly says text content identity). Do not copy the chained-start example's older package identity as if it were the new composed-text identity.
- `supplyRecord`: `{kind:"supply record",ref:<published run_text reference>,resolutionAtWrite:<actual resolution>}`; `supplyCheckRecord`: the independently published immutable check reference. The latter is semantically required by SC-5/R3/VC-40 even though the body schema does not require it.
- `supplyCheck`: unchanged `verified`, either precise mismatch state, `not found`, or `unreadable`; `adoption:"unknown"`. `not checked` exists in RS only for actual absence of a check. A completed incomparable check cannot truthfully become not checked or unreadable.

The current native producer has opaque native turn identity but no established RS number. Therefore it can publish faithful WR evidence first; it cannot honestly complete the workflow R3 body by omitting turn or manufacturing a number. Preserve/report the missing RS mapping rather than claim a recorded R3. A `verified` check means exact source-bound supply only; no adoption, execution success or registration claim follows.

### Incomparable

WR's adopted CC-WR-TEXT-METHOD-ADOPTION paragraph and schema add `incomparable`; RS R3's enumerated prose and both Design/bundled schemas retain the older five states (plus schema `not checked`). No accepted lossy mapping was found. Historical unfamiliar methods remain opaque; equal digest characters under different methods never make verified. Current fresh exact-byte checks may avoid this case, but the general publication API must not pretend the consumer already accepts it.

### Allocation and failure are partly settled, partly still absent

RS §13.7 CC-P-R selects **App-local Rust ownership**, no common service. Known-project RS run/writer logs are `<project>/.chirality/records/runs/<safe-run-key>/<safe-writer-key>.jsonl`; safe path keys are not identities. Outside-run `records/acts/` is for acts only. A15's portable library acts/captures are a distinct allocation, not a fallback for workflow run evidence. `storage::project_log` and `records::append_project` implement the project-log seam.

WR §7/§8 and §16.1 allocate selection/run_text/supply_check production to DEL-02-02, and R2/R3 receiving to DEL-04-03; R3 references supplier records and does not embed them. **These sources do not select an on-disk path, envelope or resolver convention for the three immutable WR supplier records.** WR prototype's selection/text/check lists are in-memory examples; its library act log is not a run-evidence store. The opaque evidenceRef schema/example prefixes permit references but do not implement their resolver. No maintained WR publisher for these records was found. Thus no specific WR sidecar directory can truthfully be called an already accepted storage allocation.

For unknown project, RS §13.7 explicitly forbids silent relocation to user data, another project or different log: “No writable project/library attached supplies no alternative storage authority.” The selected workflow's library does not establish the conversation's project or grant a portable A15 log for run evidence. Keep recording unavailable/pending and expose missing-in-record; do not infer project from cwd or source root. Durable WR location/identity/resolution needs a bounded owner allocation before physical publication API implementation. Known-project RS placement alone does not settle it.

WR SC-1 is explicit: record run_text **before sending**. A conforming recorded-workflow path cannot call the sender before that required publication succeeds. This is record sequencing, not a new human permission gate. RS W-0/W-1/W-2 require visible failure, no best-effort invalid record, pending original entries in order and retained observedAt, then the failure evidence on a successful retry; if the writer ends first, missing records remain missing and a later run cannot back-fill them. The contract does not authorize marking a merely attempted write as recorded. After an already sent turn, a check/R3 write failure must retain observed facts as pending/missing and must not resend the turn. WR SC-6 makes a new read a **new check**; a retry of one pending publication preserves the same original check instead.

## Minimal owner proposals (no adoption)

- PROPOSAL: CC-WR-RS-SUPPLY-STATE — receive the adopted incomparable result
  - Evidence: WR CC-WR-TEXT-METHOD-ADOPTION and `$defs/supply_check/state`; RS §4 R3, VC-40 and `$defs/suppliedGuidance/properties/supplyCheck` omit it.
  - Change: RS owner adds `incomparable` to that R3 state list and receiving enum; specifies “supplied — not verified, incomparable methods; adoption unknown,” preserves original expected/observed methods through the WR reference, and adds a schema/round-trip negative-equality fixture. Propagate reviewed Design change to bundled schema and actual reader/display mapping.
  - Why: faithful receiving without inventing mismatch or no-check facts.
  - Risk: older enum readers reject the added state; they need explicit propagated source adoption, not silent relabelling.
  - Status: PROPOSED

- PROPOSAL: CC-WR-RS-NATIVE-TURN — represent the actually observed native turn without fabricated numbering
  - Evidence: RS schema header and workflow `allOf` require integer turn; WR supply_check uses opaque string turn; no numeric mapping found in maintained native producer or inspected source contracts.
  - Change: RS owner decides and records one bounded native workflow representation. Proposed minimal form: retain existing `turn` integer unchanged for established numeric coordinates; add optional `nativeTurn` nonempty opaque string to suppliedGuidance; for workflow forms require `supplyCheck` and at least one of `turn`/`nativeTurn`, with a native-form reader rule binding nativeTurn and thread to the referenced WR check and no numeric equivalence inferred. Add prose/positive/negative fixtures and propagate to bundled consumer. Do not widen unrelated model_turn or EXEC event bodies in this tranche. If the owner instead supplies an existing authoritative numeric map, cite that source and use it without this schema change.
  - Why: preserve observed native identity and historical numeric records while removing the need for fabricated ordinals.
  - Risk: adds a receiving representation; RS owner must assess versioning/read-limited behavior and connected display/reference consumers. This report cannot adopt it.
  - Status: PROPOSED — awaiting owning-source disposition

- PROPOSAL: CC-WR-SUPPLIER-RECORD-LOCATION — complete the bounded physical publication allocation
  - Evidence: WR §8 supplier records and SC-1/SC-5; RS §9 reference-only R3, §13.7 known-project ownership and no-fallback rule; maintained records/storage APIs expose only RS/project/capture allocation.
  - Change: WR/RS owners specify exact owning project-local storage target, immutable supplier record identity/envelope, collision/retry semantics and reference resolver for selection/run_text/supply_check, explicitly preserving SC-1 and W-0…W-2 and refusing unknown-project fallback. Then implement under the already selected Rust host; do not create a shared service or repurpose A15 acts storage. The exact subpath remains TBD in this source-fit report.
  - Why: gives the writer and reader one reviewable persistence contract instead of accidentally blessing a new sidecar convention.
  - Risk: unreviewed placement can leave R3 references unresolved after relaunch or write to the wrong project.
  - Status: PROPOSED

MISSING: authoritative RS numeric-turn mapping or adopted native representation; RS incomparable receiving; physical WR supplier evidence allocation/resolver.

NEEDS_HUMAN_RULING: none established by this source-fit examination. CC-WR-RS-NATIVE-TURN awaits owning-source disposition through named, reviewed change control. Parent determines whether the eventual disposition reaches an actually reserved human boundary; no new human checkpoint is established here.

Authority-label correction (2026-10-05, explicitly dispatched by parent): the earlier NEEDS_HUMAN_RULING label treated a new representation as sufficient reason for human escalation. No exact governing clause reserving this bounded mapping choice to the human was identified. App-v4 LOOP_INIT instead requires named, reviewed changes to agreed Design interfaces and propagation to consumers. The label is therefore corrected to PROPOSED/awaiting owning-source disposition. This correction adopts no representation, supplies no missing ordinal warrant, and leaves the mandatory workflow turn mapping, faithful incomparable receiving, SC-1 sequencing and storage/source findings unchanged.

DEPENDENCY_NOTES: All source/consumer joins are existing Group A WR/EXEC/RS/Root ownership. No deliverable, DAG or group-order change. Record-publication API preparation is independent of lifecycle: prepare immutable typed WR bodies → writer validates/publishes in original owning scope → returns durable reference or retained pending/failure → sender consumes only recorded run-text readiness → genuine native page check produces new immutable check → published reference feeds RS R3 where its identity contract is satisfied. This specifies operation ordering and returned standing, not new runtime factories or storage paths. Separate selected-development standing must remain development; these records confer no registered/A15 or lifecycle authority.

## Inspected source hashes

- `.agents/skills/proposal-format/SKILL.md` — `63e6d2545c31df939511a5a137c214d5444ca562f6abf9b048de3aa2f8dac59d`
- `projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-03_Content-bound decisions and compact run records/Design/RECORD_SEMANTICS.md` — `15266b5078ad1878dae20dc1fa2ef93723d187ce18d5fe780bd1af75c00d5f41`
- `projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-03_Content-bound decisions and compact run records/Design/RS_RECORD.schema.json` — `c94dbd441388f52de4dbce5b79859abf2a07223bf236f209eedcb6aee548e3e6`
- `projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-03_Content-bound decisions and compact run records/Design/RS_RECORD.valid.app-chained-run.example.jsonl` — `eb39c986da31805136feec0f75f5daf0a62a3776708a9425665c95dad14559ce`
- `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-02_Workflow-making workspace and registration/Design/WORKSPACE_AND_REGISTRATION.md` — `bd61f48ca97eba9c7665b31ff7506672f18152d57a20b0ffd361a168750af989`
- `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-02_Workflow-making workspace and registration/Design/workspace-registration.schema.json` — `cfd6d3e252b72247d8e1ad0ced3b43b119c5785935002d493407757bd57066e9`
- `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-02_Workflow-making workspace and registration/Design/prototype/wrproto.py` — `303474582a5192909b7f60e0108009d47efe77fd0477f1ec3c88f00b80fd9c62`
- `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-03_Workflow execution compatibility and round-trip support/Design/EXECUTION_COMPATIBILITY.md` — `dc7ed825629fbd9afa72e709068764edc12a43a003cf54e47bc7e81ae24e39cb`
- `projects/chirality-app-v4/app/CONTRACT_ISSUES.md` — `c499a9fce4d6e822ce1f911d2ae79c99f125e82d2f25d4c9f0da21d54c492d67`
- `projects/chirality-app-v4/app/src-tauri/src/runtime_session.rs` — `05af3f76da30a02dd425d9de025c623402a2fbdfefcdfc99c5f7201590c041f6`
- `projects/chirality-app-v4/app/src-tauri/src/workflow_workspace.rs` — `9fe3ceb4e569208b059dc1a1695f7baa54c8b8919a5a01dd18e2c2f859853f5c`
- `projects/chirality-app-v4/app/src-tauri/src/workflow_library.rs` — `633fe20ae46b1842a7d94567a69c3fa999fbc9814c09410a7cd69296d3480c38`
- `projects/chirality-app-v4/app/src-tauri/src/records.rs` — `ea498b90be82391446c97a9708b86fecab45d266eb3487f674c6803fde4284ea`
- `projects/chirality-app-v4/app/src-tauri/src/storage.rs` — `39cd09a746e7cde8730b9956d748bbabfe39c6b67dbafe44b992e254d1634e93`
- `projects/chirality-app-v4/app/src-tauri/src/record_semantics.rs` — `dc56618b97a9938f1e53ff1242fdb92c9bd6af1955ad02bb1ce7152ed255ec9f`
- `projects/chirality-app-v4/app/src-tauri/src/record_relations.rs` — `21352b5d151d1a2a5e1357f981227c9535c68960c46cc534c822ba9db0a1d011`
- `projects/chirality-app-v4/app/src-tauri/src/recovery.rs` — `f0fff309d2f8eec23046b5349e4969308ef26319a4e5b6eedf46b3c4da50bc31`
- `projects/chirality-app-v4/app/src-tauri/schemas/RS_RECORD.schema.json` — `c94dbd441388f52de4dbce5b79859abf2a07223bf236f209eedcb6aee548e3e6`
- `projects/chirality-app-v4/app/src-tauri/resources/workflow_role/workspace-registration.schema.json` — `cfd6d3e252b72247d8e1ad0ced3b43b119c5785935002d493407757bd57066e9`
