# CC-A — native A16 choice and capture-to-record sequence

Run APP-V4-GROUP-A-20261004; 2026-10-04. TASK `/root/group_a_execution/design_aac`,
parent `/root/group_a_execution` WORKING_ITEMS. Actual mechanism:
delegated-harness-native child; no further delegation. This is a recovered
current contribution, not a claim to be any earlier design owner. Source root
initially located from the active filesystem checkout at
`/Users/ryan/.codex/worktrees/077c/chirality` (contains Root AGENTS and projects), then confirmed by the required read-only
`git rev-parse --show-toplevel`, exit 0, same absolute path. No Git mutation
or publication operation was performed; parent clarified that boundary.

## Standing and proposed change

**PROPOSED; independent review pending; product propagation withheld.** Named
change CC-A covers CI-5 and CI-6, plus the authorized CI-4 absence wording, AAC-v0.3 → AAC-v0.4 candidate. The schema
shape/ID stays 0.3; its optional recordId description now states the runtime
sequence. ScopeOfWork, shared app code, issues, graphs, MEMORY and lifecycle
are unchanged by this TASK. The prior SoW already assigns OUT-005/REQ-008/
AC-008/VER-008; this clarifies binding and persistence without adding an act
kind, human gate, workflow, or deliverable.

- CI-5: webview selection followed by host-frozen native Decide/Cancel;
  the native surface displays authoritative chosen statement and every
  consequence, and capture/RS use that frozen alternative. Webview scripts
  cannot confirm or rewrite native text. Rechecks preserve AK-c/NA-4.
- CI-6: initially durable capture without recordId; writer mints the RS ID;
  after verified append, host adds its ID once with atomic persistence.
  Recovery finds the RS capture reference and validates matching facts before
  repair or replay. AC-7 remains recorded when only the backlink fails.

## Rationale and concrete failures

CI-5's at-most-three-button observation is supplied evidence in CONTRACT_ISSUES,
not a fresh dependency/product-spec verification. Two fixed native buttons
avoid encoding the alternatives as native buttons. Host lib.rs currently
holds the act mutex while composing, presenting and confirming; its immutable
command argument chooses the same ID. The contract makes that binding explicit
and requires full text, duplicate-ID/digest refusal and no new callback choice.
The candidate has no native witness in this TASK.

CI-6's host currently rewrites the capture with std::fs::write and ignores the
backlink error. A crash/failure can lose or tear that file. Its in-memory state
alone cannot resolve a restarted host. The selected smallest sequence retains
the existing optional backlink instead of adding a second object or transferring
ID minting out of RS. Atomic durable replacement preserves the original capture;
the RS reference, not the backlink alone, proves an append happened. A failed
or uncertain sync, unreadable/torn log, conflicting or duplicate entry cannot
justify replay. Shared serialization must cover check/flush/append, not merely
the final file update. Conditional seals require resealing the updated object;
this neither adopts nor implements SEAL-2.

The prior prototype's _record sets recordId before append. It is historical
model evidence and remains intact; old checks cannot be cited as the new
sequence. Dedicated CC-A checks use invented immutable act facts, snapshots
and a ledger double, and do not establish filesystem or native-host durability.

## CI-4 coordination — owner-selected absence label

Parent relayed the RS owner's recommendation: preserve valid 0.1 packages with
optional scope and render an explicit absence marker. Exact AAC text now applied as the owner-selected candidate:

> For A16, if package scope is absent or empty, the host sets offer scope to
> "not named by the package". This is an explicit absence label, not inferred
> scope. The native confirmation shows exactly that label, and capture and RS
> copy it unchanged. Nonempty package scope is copied without substitution.

This resolves the optional-package/required-offer mismatch without invalidating
existing valid package files. Actual owner answer, relayed by parent WORKING_ITEMS
from HELP_HUMAN on 2026-10-04: "Use the explicit absence label (recommended)".
Custody is the parent's active human chat; this child received that trusted
relay and does not claim personal owner review. Authoritative run decision
pointer: `../OWNER_DECISIONS.md` (parent records the relay there). AAC §4.1a
and scope field descriptions are changed; package/schema shape and product
files are unchanged. Independent review and product propagation remain pending.
No interpretation of actor, purpose or neighboring scope supplies missing scope;
non-string scope is invalid, not absence. Both AAC field shapes stay required
and nonempty.

## Consumer adoption before propagation

| Consumer / owner | Required adoption/check |
|---|---|
| Group A implementation owner, app/src-tauri/src/act_control.rs and lib.rs | Frozen native choice, full-text failure, one capture, durable creation and add-once replacement, explicit backlink error, restart/late-write reconciliation. |
| Group A RS owner, DEL-04-03 RECORD_SEMANTICS §13.2/§14 and writer | Preserve writer-minted IDs/W-0/W-1/W-2; serialize reconciliation by capture reference with pending queue and recovery; compare actual matching facts, handle orphan/conflict/torn entry. Sibling Design propagation stays with CC-R owner. |
| DEL-02-03 checkpoint recorder / EXEC | Consumption counts only a real conformant record; no backlink alone or webview selection counts. CI-4 selected absence wording copied unchanged. |
| DEL-02-02 registration / WR | For A15, backlink retry makes no new act/registration; existing per-entry outcomes stay beside immutable act facts. |
| DEL-06-02 decision view (downstream group owner) | Selection is proposed until native capture; display recorded versus record-link-pending; no fabricated alternative after capture. Carry through parent to its future graph. |
| DEL-04-02 standing view / DEL-04-03 reader | Existing entry remains evidence if backlink pending and original capture resolves; ambiguous/unverifiable data carries limits; no duplicated/superseding act on replay. |
| Packaging / seal owner (conditional SEAL-2) | Durable atomic publication on target filesystem; updated object needs a fresh valid seal and unchanged original act facts. No entitlement/credential act in this TASK. |

These are consumer work and notices, not claims of adoption. Parent owns shared
integration and later graph/interface notices. No cross-group order change is
proposed. Review must cover the final AAC candidate and owner-selected CI-4 wording
before app propagation. Native candidate interruption/durability and script
custody witnesses remain product checks. Existing OI-008/SEAL-2/signed-in identity
questions retain their owners; CC-A creates no fresh approval ceremony.

## Checks and return

Commands and canonical stdout are recorded below after execution. Reads only:
manual headings, full Field Book, selected manual §§10–11, Root/TASK/App v4 loop,
current graph and complete graph inventory (no B/C/D/E graph exists), current
SoW/MEMORY, historical decision sources, AAC, schema/prototype and relevant RS
identity/writer rows, app act/record/native host code and contract issues.
No App v3 policy is applied; its mistakenly discovered loop/instructions were
read while locating App v4 and supplied no reliance rules to this change.

## Supplied/read source bytes before this edit

Hashes identify actually read current files, including historical decision
records; historical owner custody statements are not new owner review. RS may
be concurrently revised by its authorized sibling; these hashes bind the bytes
observed here, not a future integrated candidate.

| Source (relative to repository) | SHA-256 |
|---|---|
| `AGENTS.md` | `f96feb19d297c74e10048c506805b2fe3622c50cfefd6078f599724556113977` |
| `agents/AGENT_TASK.md` | `1a13a5b00b3ce01ff8519efe6b46bcbe0cd6a5b7985e24282fa7efa2c57c8fb7` |
| `projects/chirality-app-v4/loop/LOOP_INIT.md` | `45c23cf477e23aff1d0152189caf7e8ebfb53eca42e3a1fae87a06af8c197f28` |
| `docs/alignment-manual/README.md` | `31217d30b0d2743bef0d7c1a54bb9a81814d56b24ff0961cf01d9532952e305f` |
| `docs/alignment-manual/CHIRALITY_AGENT_USER_MANUAL_v3.md` | `08ca0e40cd5157574a011bac57d539e77e9007a0d46494785da8b92745391b1a` |
| `docs/alignment-manual/Project_Management_for_Human_Agent_Teams_Field_Book_v1.md` | `02d53a3966220001318aacf3f46e1b63b8695a098c81b20f4e3e1531b93024d3` |
| `projects/chirality-app-v4/execution/_Coordination/WorkGraphs/APP-V4-GROUP-A-20261004/WORK_GRAPH.md` | `921252cf288bcf4b49c0738f7276295fd46a2eda29d3c132d7f97c4e500dddea` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/ScopeOfWork.md` | `8434cc47ec28e1397e7dae548183543567f0b5fcfdefaebc0b44bc1f709aacf3` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/MEMORY.md` | `b6bf3813988d774dd7f5c40da1c9588592bbae82c837a89f5d2fc94d9273748a` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design/APP_ACT_CONTROL.md` | `de39976e93500c9455c000b78363ad192fe56fd8aa87c680284f78db939acf65` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design/aac.capture-evidence.schema.json` | `54af340140bb5896157348910917ebf7abcbaab839a14113cfcfa1b66b205b43` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design/prototype/act_control.py` | `27e0095819ecdb165ccb317927361026a6b168a6641f4ab2b4b4a3e35e01294e` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design/prototype/README.md` | `586d356f3a4ddb193ae84012f26e02396a046b5ab4193208ac0c48ffe2957d4b` |
| `projects/chirality-app-v4/app/CONTRACT_ISSUES.md` | `b34507c62daec69fe2ca7152757757a31d6429d7786c797c7097e693f2675639` |
| `projects/chirality-app-v4/app/src-tauri/src/act_control.rs` | `6a43e6eabf0de1a40ef0768ca1444fe46018c56aecaaad558dc3420743c81ac4` |
| `projects/chirality-app-v4/app/src-tauri/src/lib.rs` | `2995fc41188438c344f0dcd8c7a948e0b796703b6cb1a8a263bb176e176944e0` |
| `projects/chirality-app-v4/app/src-tauri/src/records.rs` | `9a7d2bf86679489868ea4b5bd2aeb3f3187a992bcfbd40c09384aa94bf99e7bc` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-DESIGN-PASS-3-20261001/OWNER_DECISIONS.md` | `8a5d11149045770dfcf1a19ebabb86bfe9f04cd3e65ed36166cb8593e2fe20ac` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-DESIGN-PASS-4-20261003/OWNER_DECISIONS.md` | `e4350f61a93edf0d2d4bfc588fcaa17ae23981baa6059617dcc430cda3008cd8` |
| `projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-03_Content-bound decisions and compact run records/Design/RECORD_SEMANTICS.md` | `a2c390b4641c47ae3150b52ff97365ccbff3dec08274fb2f3892d311e7c674b3` |

## Executed checks (2026-10-04)

- `PYTHONDONTWRITEBYTECODE=1 python3 cc_a_sequence.py` in DEL-01-04 Design/prototype:
  exit 0, 20 checks / 0 failures. Canonical output:
  `Design/prototype/results/RUN_2026-10-04_CC-A.txt`. Assumptions: snapshots
  and serialized publication/scan/append are indivisible; no native dialog or
  filesystem durability is exercised. CI-4 absence/non-string cases included.
- `PYTHONDONTWRITEBYTECODE=1 python3 run_cases.py`, same directory: exit 1
  during K-4, RS prototype validator cannot resolve sibling CI-1's new
  `chirality:del-02-03/exec-checkpoint-entry-bodies/proposed-0.7#/$defs/arrivalRef`.
  Canonical output: `Design/prototype/results/RUN_2026-10-04_CC-A_LEGACY.txt`.
  Reported to parent for CC-R reconciliation; this child changes no sibling
  validator or schema. Earlier S schema checks pass, but combined model pass
  is withheld. The failure is not treated as repaired by dedicated model pass.

Exact Python executable/version/host, command/cwd, changed environment and
stdout/stderr/exit are in those output files. No package download, sign-in,
credential access, Codex execution or live turn occurred. Re-run with those
commands using the retained script/schema and sibling dependency versions.
Native persistence/custody and conditional seals remain unverified.

## Consumer registry repair and current combined-check result

Parent authorized the bounded CC-R/CI-1 consumer adoption in this Design
prototype: register DEL-02-03 checkpoint schema explicitly under its `$id`.
`run_cases.py` now locates EXEC_DESIGN and loads that schema into the same
Registry as RS. No automatic sibling lookup, schema rewrite or altered criterion.
Rerun completes 159 checks / 1 failure, exit 1: R-16 has eight NIR generation
integers but sibling CC-H's HOSTING register schema requires generation objects.
All K act-control checks pass on the old model; they remain insufficient for
CC-A durable persistence. Output: `Design/prototype/results/
RUN_2026-10-04_CC-A_REGISTRY.txt`. Parent notified for CC-H consumer reconciliation.

## Bounded placement comparison requested by parent

Read-only packet comparison: `../PLACEMENT_DECISION_PREPARATION.md`. Recommend
App-local components with no common service or host allocation, subject to
independent review and the owning placement decision. The project's capture
store proposed there suits project file/standing/run acts. **A15's capture must
travel with the same owning library as its act log**, including a user library:
a project-only capture root would leave a portable user-library act with an
unresolvable capture after changing projects. Smallest concrete proposal:

> Project acts use the opened project's `.chirality/captures/` with per-run and
> per-writer/standing logs in the packet's `.chirality/records/` layout. A15
> library acts and captures use that library's `.chirality/records/acts.jsonl`
> and `.chirality/captures/`. The act owner supplies the exact capture-store
> root to the resolver/writer; storage-safe keys are not governed identities.
> A missing/unwritable owning root reports failure without fallback. Recovery
> enumerates that owner's complete log set and capture store under one writer
> boundary, including explicitly registered legacy skeleton logs. Preserve old
> log bytes, record IDs and capture references; do not recapture or reissue acts
> during migration. Capture movement needs preserved-ID/content verified copy
> before switching resolution, and incomplete migration stays pending.

This recommendation is not applied to AAC paths, product code or schemas.
Production release of I3 needs review of exact discovery/migration/cross-project
resolution, safe key minting and persistence on the target filesystem. User
library registration may operate against a writable library without a writable
project; a project act cannot silently relocate to that library. This resolves
the App slice, not host OI-013 or every OI-014 candidate. Parent owns any actual
placement decision record and sibling/downstream adoption.

Prior custody search: first-increment OWNER_DECISIONS leaves OI-008 with the
App implementation owner; R17-5 explicitly labels Rust/native placement an
integration proposal; DECISION-L L-5 rejects an OS password/Touch ID check per
act, L-7 names the App implementation owner. No separate affirmative P-2 owner
act was found in those sources. CC-A follows existing frozen P-2 semantics and
the authorized CI-5 clarification; it requests no fresh native-presence gate
and does not represent P-3's rejection as P-2 approval. Parent should assess
the already accepted 60% design gate and its custody before reopening OI-008.

Additional observed source hashes:

- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/PLACEMENT_DECISION_PREPARATION.md`: `c7db441de1ec7cbb658ad48a4475e5857bf6d7975a9575992f610c3542e65ee0`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-FIRST-INCREMENT-20260928/OWNER_DECISIONS.md`: `a9869129753631b865cbbb00a138c0f497d5ac8a4b67f5746169d1f9a668ad2c`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-DESIGN-PASS-3-20261001/R17_RESOLUTIONS.md`: `b0af81bcbad9bc52fddc99119c42a19019a9b174677d5b92a0a2f5c8b4f8e198`

## CC-H/CI-2 consumer adoption and final model checks

Parent relayed hosting owner's authoritative invented fixture tuple
`{appSession: "aac-fixture-session", home: "account", spawnCounter: 1}`.
`nir_model.py` now retains the complete tuple and keys closed generations by
all three components; the close-generation case passes that tuple, retaining
its original refusal criterion. No guessed real identity or null request
generation is introduced. Final combined `run_cases.py`: **161 checks, 0 failed,
exit 0**, canonical `Design/prototype/results/RUN_2026-10-04_CC-A_INTEGRATED.txt`.
The first unresolved-reference and later generation failures are repaired by
explicit consumer adoption and preserved in their earlier outputs. Dedicated
CC-A state model remains 20/20. Product/native and durable persistence are not
established by these model checks.

Final consumer source hashes:

- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-01_Stock Codex hosting and supplier contract/Design/hosting.server-request-entry.schema.json`: `388560979f0f75e39f489a9daef67e6ca9d29a743c94dc6d1705c59ecc04599c`
- `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-03_Workflow execution compatibility and round-trip support/Design/checkpoint-record-entries.schema.json`: `00d5203a2fa9d099b25f2f8da5732f2d869a18fd0846ebe33d25c9ae2ae135d3`
- `projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-03_Content-bound decisions and compact run records/Design/RS_RECORD.schema.json`: `c94dbd441388f52de4dbce5b79859abf2a07223bf236f209eedcb6aee548e3e6`
- `projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-03_Content-bound decisions and compact run records/Design/prototype/record_store.py`: `22d3acacce2afe642b38261e62a610d234c224c18e5fac1144b669d676e82cd0`
- `projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-03_Content-bound decisions and compact run records/Design/prototype/minischema.py`: `2851bb7cd4977b9612edfbf2ad30adc04f70d81dcba37d19b89d47d3df3a8a85`

Further CI-2 consumer propagation authorized by parent: NIR answer submission
schema and examples move from 0.1 integer generation to **0.2 complete H5
object**, with no integer union. All register-double fixture receives and
closures use the hosting owner's invented full tuple, while NIR answer
serialization preserves it. NIR §4.5 names the new ID and full correlation.
Consumers must adopt `urn:chirality:app-v4:del-01-04:nir:answer-submission:0.2`: 
DEL-01-04 card/submission validators, DEL-01-01 definition/DEL-01-02 request
register answer operation, and any schema registry/product test importing
the answer schema. This named CC-H consumer contribution needs independent
review alongside CC-A; no request meaning or refusal criterion is weakened.

Final two added R-16a correlation checks reject equal spawn counters with
different appSession or home, retaining the outstanding request. All 161
combined cases pass on the final candidate; no native or persistence claim.

## Frozen contribution hashes (CC-A itself is returned separately)

- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design/APP_ACT_CONTROL.md`: `bdcc8643f1ecc2423d5a90b2ba5afb3eac572c34525f5fa144732b3ee3eda02d`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design/NATIVE_INTERACTION_RECEIVING.md`: `fdcb8e987f76453c29fd6e609c5de4dac3c8d354b0779598acd2dd58f6d8c288`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design/aac.offer.schema.json`: `f2091fcf2583b6863370ba51d86f4c8671dbae5bbd6fe0e39046154d98c7d066`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design/aac.capture-evidence.schema.json`: `4405a1228e5982d948eb82776aaaf54d966d4305f8829a656473a523ad1ca4ba`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design/nir.answer-submission.schema.json`: `042d58af76d5977a156ec6bc16b81f31b717b6d433e89555960b747516aadfb6`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design/nir.answer-submission.example.valid.json`: `8fc1b8366aaabf4779256dd401bfe4818fcd00eb6f4cae3ee300d84658201606`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design/nir.answer-submission.example.invalid.json`: `3d23b966d04aa6e796ffefd9cf9172f2da95d40c4fe253e3b05eaee04abbaf2b`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design/prototype/cc_a_sequence.py`: `fe03014eadb0f01c8670e6d3659bd01bb447eef85f6f33cc8454e19b6fb68823`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design/prototype/nir_model.py`: `8541651a4f90e6b1b7c7d0a529382d5941012f5d3d1603bbd928fb2498b22c8f`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design/prototype/run_cases.py`: `532813fdaa8736559606d7e6b8cbf39f2d616ce20c16280a32716a4f8f7417ab`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design/prototype/README.md`: `dd046a7beb6ecdd9427d9071b768701b4ca72fd8718cce0804f857f0da94fd78`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design/prototype/results/RUN_2026-10-04_CC-A.txt`: `f76b5f39f6d614c014470e9b327b5f9a296792925871a937041765b6e13283f6`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design/prototype/results/RUN_2026-10-04_CC-A_LEGACY.txt`: `7d840b5d904d2473c29fde65b661aecd716f9846fae281ccc4bfe8c3cd577c8a`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design/prototype/results/RUN_2026-10-04_CC-A_REGISTRY.txt`: `173c7e907d43942c6b61955be6588dadacc6d72bc48d9c91745fb6f8edc638a7`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design/prototype/results/RUN_2026-10-04_CC-A_INTEGRATED.txt`: `553d91f295154b870bde74f96179e12a835496346e380a8324bf901645fc8ef5`
