# V6 WR/RS publication implementation review

2026-10-05. Fresh independent Type 2 TASK `/root/group_a_execution_astra/wr_rs_implementation_review`, parent `/root/group_a_execution_astra`; Astra/low per dispatch. Native delegated-harness descendant, no descendants. Selected software-code-review skill. Sole write is this report; no code/schema edits, Cargo/compiler/test execution, Git, native/supplier/network/auth or credential operations.

## Disposition

**REPAIR REQUIRED: one blocking implementation finding.** WR persistence/preparation has no independently established blocker within its bounded supplied API. RS cannot yet claim both workflow purposes. Joint compilation and executed receiving/backchecks remain pending; this read-only review is not whole-pipeline readiness or permission to treat cold records as live supply.

## Blocking finding WRRS-1 — actual end-notice records cannot correspond

Location: private RS `src-tauri/src/record_supply.rs:187` (`source_identity(&run_text["workflow"])`), with actual WR `src-tauri/src/workflow_workspace.rs:871–892` and RS `record_supply_tests.rs:48–74`.

Trigger: publish an actual `PreparedEndPublication` and a corresponding end-notice check, then call `correspond` or `read_correspondence`. `PreparedRunText::end_notice` constructs a run_text containing purpose, framing, run, conversation, lines, text_identity and text_bytes; it supplies no workflow tuple. RS unconditionally requires six workflow tuple members. Therefore even otherwise valid end-notice evidence returns Invalid("kind absent/empty") and its RS reading becomes Limited. The published end notice has no basis reference to recover that tuple with the current API. This is a missing source join, not merely an unavailable native check constructor.

The authored both-purposes test only changes purpose on a synthetic run-start body, keeping workflow and workflow_file. The retained workflow_file is forbidden for end-notice by the actual WR schema. It therefore cannot detect the producer/receiver mismatch, even if all six Rust tests pass.

Repair direction: preserve source identity from the actual original owning run/source record through an explicit checked linkage or approved source-compatible metadata path. Validate run/conversation/project correspondence; do not parse a shortened frame revision, invent a tuple, or mint live authority from resolved history. Exercise a genuine/schema-valid produced end notice through immutable resolution and the RS reader, including wrong owning-run/source rejection. Any owning-contract amendment must follow named source review. Until then scope RS readiness to the supplied start-only path and retain the end-notice obligation as unfinished.

## Examined behavior and boundaries

- WR requires an absolute explicit project, traverses descriptors with O_NOFOLLOW, pins device/inode, and refuses cross-project pending publication. UUID mapping is fixed; no cwd/library/user fallback exists. Immutable staging/write/sync/link-no-replace/directory-sync path preserves pending bytes; collisions refuse replacement. An uncertain link retains identity and bytes for retry. Resolution validates envelope/body/record_id and required selection/run_text/check relations. Historical versions remain unsupported.
- Typed registered selection and original PreparedRunText are retained. Development admission cannot become registered. Reopening exact revision bytes and comparing workflow content precedes publication. Published handles retain original prepared content and have no native send side effect. Source loss fails rather than causing source/transcript copying. Explicit-selection construction does not supply the missing actual selection-event seam or a proposal-confirmed selection producer.
- CompletedSupplyCheck fields are private, no Deserialize or production constructor exists, and raw PendingRecord construction is private. Its supply_check constructor consumes that token and a resolved run_text, preserves original read_at and source references. These are useful persistence boundaries, but no genuine completed-check producer exists. This review does not approve a future arbitrary JSON setter or coverage-seal-only factory.
- RS checks same-project, kinds, immutable basis reference, run/conversation/purpose, composed text method/value and optional expected workflow identity. Native turn comes from check.turn; no ordinal/client-ID fallback exists. All six states are retained. Verified unequal methods/values are refused; incomparable remains unchanged. Historical resolution returns a visibly limited historical claim, not an append capability. The old generic writer's existence is not a new live receiving route.
- RS reader validates the complete entry, re-resolves both references, checks semantic fields and retains legacy ordinal standing. It does not elevate resolutionAtWrite to current proof. There is no new native append operation consuming HistoricalSupply. Actual before-send, completed source-owned check, post-send WR/R3 append, no-resend recovery and lifecycle remain unsupplied Root/EXEC joins.
- WR body/envelope metadata remains reference-based; no native transcript/pages/generated prompt store was introduced. New RS schema and policy pins are in the private change manifest. Coordinated maintained propagation and final ordinary-build privacy controls remain manager work.

## Evidence and limits

Read-only Python hashing independently verified every changed private WR and RS file against its supplied manifest: zero mismatches. All four maintained adopted source hashes match CC-WR-RS-SOURCE-ADOPTION.json. WR patch SHA-256 is `84f238d583c8fd25a4ac71abb2c68541dc68773e30295bddb0134bd43528f784`; RS patch is `5724ee74a57f932872f0f62999ceaf04819c36c9c2a1c9053db9636c4e3d4871`. Frozen WR executable hashes to `4ef64772ec2a08ed8b5687f1929f972e5581e3451729f8c355c37f0759969ce5`.

WR owner reports 56 affected tests (7 store tests), failed ordinary-build raw construction E0451, and restored ordinary check passed. Those are owner evidence, not rerun by this reviewer. RS six tests are authored and unexecuted; no independent pass claimed. Initial shell wildcard search failed before searching due to no matching workflow_run*.rs; corrected direct workflow_workspace reads established actual producer. This was review discovery only, not a candidate failure.

Missing verification: joined compile; repaired real end-notice receiver control; actual ProjectRecords-to-RS cold-reader cases, missing/corrupt references and two-read versus retry behavior; genuine source-bound live producer privacy and native scope/content controls; connected pre-send/no-resend/R3 failure checks. Earlier exact832 delivery evidence cannot discharge these new obligations. No new human ruling identified; parent owns repair/integration and test-lane release.

## Supplied and consulted origin binding

Root AGENTS was supplied and matched on disk; TASK/skill/Loop, manual README/headings/full Field Book, current graph (orientation only), adopted source record, exact source proposals/review, implementation reports/manifests, private implementation/tests and relevant producer/schema clauses were consulted. No other role activated. Hashes below bind consulted instructions and controlling records; private changed-file manifests bind inspected implementation files.

- `AGENTS.md` — `f96feb19d297c74e10048c506805b2fe3622c50cfefd6078f599724556113977`
- `agents/AGENT_TASK.md` — `1a13a5b00b3ce01ff8519efe6b46bcbe0cd6a5b7985e24282fa7efa2c57c8fb7`
- `.agents/skills/software-code-review/SKILL.md` — `ee085d589c44f912d11a59eead8edac214f0343761d26b0d33e886a979888bca`
- `projects/chirality-app-v4/loop/LOOP_INIT.md` — `c2e88f81439ed03578fee13fd7563082fefdfe11096d9134a59531eba3b985bd`
- `docs/alignment-manual/README.md` — `5eee30d902c57a251bf885f91bfa0481a7834ec6945c3382baf15d2e2980c63d`
- `docs/alignment-manual/CHIRALITY_AGENT_USER_MANUAL_v3.md` — `2535efe547f2368e06d965d189efc47c7c46f28c2d6fd4777b0b8cece9003fa7`
- `docs/alignment-manual/Project_Management_for_Human_Agent_Teams_Field_Book_v1.md` — `02d53a3966220001318aacf3f46e1b63b8695a098c81b20f4e3e1531b93024d3`
- `projects/chirality-app-v4/execution/_Coordination/WorkGraphs/APP-V4-GROUP-A-20261004/WORK_GRAPH.md` — `737e1934a0e7a309e5a872fa09283e036b872bc7069b757ad83d988a9c9027d2`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/CC-WR-RS-SOURCE-ADOPTION.json` — `9933567c7749074bd3b9134dfd72a72947841676278711cc11200217a1684f69`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/reviews/V6-WR-RS-PUBLICATION-SOURCE.md` — `5737d6e4ad444415904ab14c214677e7a082dbf89c97aec8ebf726933de8740f`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/CC-WR-RECORD-PUBLICATION-ASTRA.md` — `e94b7d8d3049b75753e674874bfbc9ca5b1365afb44fea9de58b762d902b92c1`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/CC-WR-RECORD-PUBLICATION-ASTRA.patch` — `55bb2709aa35264987b8465825b9a3ca844b57d6fc7e19811c771f8144cd8a75`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/CC-RS-WR-SUPPLY-FIT-ASTRA.md` — `23105e395383fa1f60bb14c8d12ced052a0319325a0c0fd429fad520adb8b441`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/proposed-rs-supply/RS-SUPPLY.patch` — `d445af2916bf15cbfb929121c8ddeb40f893fefd224897da76eb757672138206`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/I2-WR-PUBLICATION-IMPLEMENTATION-ASTRA.md` — `799270e7ce8c0df64fd1a789630693d8a629647530c2ed380f8a04a3d096c572`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/I2-RS-SUPPLY-IMPLEMENTATION-ASTRA.md` — `2d605d46db5275f8efb62d0a9d02b7d26e524dd0491afb5c53b97da52390303d`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/I2-WR-PUBLICATION-IMPLEMENTATION-ASTRA.manifest.json` — `7bee4fc01b737c4e2c1fba9b419bfb35ea9b065dc1ac4c3d138a06fc5547bd0f`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/private-rs-supply-implementation/manifest.json` — `dc453d3962bfbdede0ec3773e2f0fddf39a825868aa68b7e7fa636679564e440`

## WRRS-1 repaired-candidate independent backcheck — 2026-10-05

**READY for bounded producer/persistence plus historical receiver fan-in. WRRS-1 is resolved.** No unresolved blocking finding remains in this reviewed slice. This supersedes the initial repair-required disposition only for the identified successor. It does not establish complete native publication, Root orchestration, live R3 append, EXEC lifecycle or product qualification.

The named end-notice source clarification was independently reviewed and technically adopted. Its maintained source matches adoption SHA-256 `094602acb5e1ba8b68bffc7475da8a80557749d134eddb60c8c4d4a676019656`. Body schemas remain unchanged. WR now requires end→original start→selection in one explicit owning project. It checks run/conversation and limits the purpose exception to end→start; checks continue matching their own text purpose/content. Optional run-start expected_workflow is still compared by full method/value, with a different-method/same-value refusal test. End bodies acquire neither copied workflow bytes nor invented workflow fields.

PreparedEndPublication re-resolves its supplied original start and requires its complete body equal the original typed PreparedRunText record. The resulting envelope cites that start. RS re-resolves the end and its original start under the explicit project, preserves the actual end composed-content identity, and derives sourceIdentity only from that start's full workflow tuple. Missing/wrong/cross-project lineage stays refused or limited. Historical-only result and private constructorless CompletedSupplyCheck boundaries remain unchanged. No new live append factory is supplied.

Independent verification against `/private/tmp/rs-supply-endnotice-repair/app` found zero mismatches across all 262 joined manifest paths. All retained validation-log hashes matched. The original receiver control exactly equals the original frozen source prefix except final blank-line whitespace. The frozen joined executable matched SHA-256 `49ece8b6f9f62979166dbaf22b0a9da7b222798b3e11333a90fcba9bcc7b67f3` before execution.

Executed directly, without Cargo/compiler or supplier operations:

- `/private/tmp/rs-supply-endnotice-repair/frozen-joined-tests records::supply:: --nocapture`: **10 passed, 0 failed**, 246 filtered out.
- `/private/tmp/rs-supply-endnotice-repair/frozen-joined-tests workflow_workspace::publication:: --nocapture`: **8 passed, 0 failed**, 248 filtered out.

These 18 distinct checks include the actual PreparedEndPublication→disk resolution→RS reader/reopen path; identical real end bytes cause the preserved original receiver's exact `R3 correspondence refused: kind absent/empty` error and succeed in the repaired receiver. They also cover wrong original run/conversation, absent link, source disappearance, cross-project records with identical UUID references, native turn/thread/purpose/state/source/content/run drift, corrupt check bytes, absent-turn refusal, incomparable methods, immutable retry/collision and typed source loss/development refusal. Synthetic registration/check fixtures remain explicitly historical; no native completed-check constructor was bypassed on the ordinary path.

The owner's broader 70-test affected run and ordinary cargo check are retained in verified logs, not relabelled as this reviewer's execution. No Cargo was invoked, no shared target touched, and no source/schema edits were made. Sole write remains this report. The actual Root completed-check producer, selection-event provenance, pre-send gate, post-send WR/R3 failure/no-resend join and lifecycle obligations remain parent-owned and unsupplied by this slice.

Successor WR patch: `b7e5248a87e390bd048a3a408f997a69ec26688c736b9abf4a4091cd88dd34fd`. RS patch: `6446b687a7eb586701a7f851f61a37b5bbe985f93816ade4bbac54b85ea1c307`.

Additional consulted byte bindings:

- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/CC-WR-END-NOTICE-SOURCE-ADOPTION.json` — `aea9631b708dd4f8083c0bd7af7a61a8969f89d56b7bb3d238e0319ac3e9b6b3`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/reviews/V6-WR-RS-PUBLICATION-SOURCE.md` — `edf1bc3c0d846e0f0a7b93151069b147794556f6c10c25baf6656bfe3178d02d`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/private-rs-supply-endnotice-repair/manifest.json` — `e2d37fafc8cd004e947123dfa3ea9d13dba5ccdaaf90eeac75c2b8475fcf1223`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/private-rs-supply-endnotice-repair/joined-source-manifest.json` — `23ab2c644defe916d3f5b53785302cacfa0bff2726a8d452ce53ae97622d8b06`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/private-rs-supply-endnotice-repair/implementation.patch` — `6446b687a7eb586701a7f851f61a37b5bbe985f93816ade4bbac54b85ea1c307`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/private-rs-supply-endnotice-repair/REPAIR.md` — `9c6faf377ae725a3306967ecc711a7fdc4d3b960c58145472928e3c57c377540`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/private-rs-supply-endnotice-repair/validation.json` — `ace19945780e6d7560d51aec7df87c08a4eeae430e027746437245bf3609d330`

## Narrow historical-control cleanup preservation — 2026-10-05

**READY for maintained fan-in; prior bounded implementation review preserved.** No production or contract delta. Exact predecessor comparison has only deletion of `record_supply_original_control.rs` and the narrow test edit: old module/include, two historical-failure assertions and associated comments removed; publisher regression renamed. Every current producer/publisher/body/content/source/RS-validation/cold-reader and negative correspondence assertion remains unchanged. There is no dated-run source/include dependency. This is not a broad review renewal or a claim that historical evidence executed on the successor.

The original receiver evidence copy is byte-identical, SHA-256 `086e9f29677ffba27073a54bf3a27880dbc1de97f0fce33dd0dcc61ef00b4aae`; ORIGINAL_FAILURE_BINDING.json preserves original exact failure, predecessor patch, executable and canonical logs. Historical proof is retained outside maintained compilation.

Successor patch SHA-256 `b975c3ff8f72116253d9971753191bd1b1bc444b50a6d4051b091ad41ce9305a`; manifest `e7b9afb9c9fbb013c9c580ce23680eefcc2245efcf87ea4897cc8d32f719cd2b`. All joined source hashes matched; owner execution's 9 RS + 5 WR before/after hashes matched current bytes. Independently verified all three execution log hashes and frozen executable `b89608d92752c44f55808d0c172b5fac3895372e67d86645cc437de2c3298bd6`.

Owner performed offline locked no-run compilation and two exact affected current tests, each 1 passed/0 failed: `actual_end_notice_resolves_original_source_and_preserves_end_content` and `actual_end_publisher_resolves_source_and_cold_reads`. Reviewer read their canonical results and verified byte binding; no Cargo/compiler or tests executed by this reviewer for the cleanup. Existing reviewed production behavior and unchanged regressions retain earlier evidence; full rerun was unnecessary. Constructorless CompletedSupplyCheck and missing live Root/R3 obligations remain unchanged.

Evidence byte bindings:

- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/private-rs-supply-current-tests/validation.json` — `46d52810ba1d5adca2b5afb347870c8574c414617a599fc5f785ed7e76bbd78c`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/private-rs-supply-current-tests/current-tests-only.diff` — `02e24d7a27573945cc226259e23c986fdaf5805a6c613e74d8778d76612ddb5c`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/private-rs-supply-current-tests/joined-source-manifest.json` — `1559909b6b58026f310ad33e38a7961c6a3cc15a368e8623a6fb00b9bb9f21e6`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/evidence/WR-RS-PUBLICATION/ORIGINAL_FAILURE_BINDING.json` — `291402e15a12b493399378a3237a837b20cfa45275f81272b4e2d8a1c2f16218`
