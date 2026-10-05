# Independent namespace/REC/NIR guard review — 2026-10-05

**NOT READY for the full supplied Core guard contract: NG-1 is a blocking source-confirmed probe adapter defect.** The actual Root consuming path is separately owned and presently uses a received probe; this finding does not claim that path has already exercised the defective owned-probe branch. No other actionable finding established in the frozen bounded guard/ARC retention review.

TASK `/root/group_a_execution/namespace_guard_review_resume`, parent WORKING_ITEMS `/root/group_a_execution`, delegated-harness-native replacement reviewer after desktop restart. This instance does not claim the original reviewer's identity or execution. Software-code-review selected from the project skill. No delegation. Sole write is this report. No Cargo, product/test/Design/Git mutation, real-home/content/credentials/auth/native supplier/model/network/download operation or filesystem reproduction occurred. Manager was notified of the source finding before this return.

## Exact candidate and basis

Resolved Git root `/Users/ryan/.codex/worktrees/077c/chirality`; `git rev-parse HEAD` returned `f480d8c10353dd3172650647f30d670bb4dfab93`. Independently computed SHA-256 with `shasum -a 256`:

| Frozen source | SHA-256 |
|---|---|
| app/src-tauri/src/hosting.rs | `6c48be0e0fdd32a8446095d4681cc11ff5e756ac8cc9d51df1b460ef0b51c82c` |
| app/src-tauri/src/recovery.rs | `f0fff309d2f8eec23046b5349e4969308ef26319a4e5b6eedf46b3c4da50bc31` |
| app/src-tauri/src/attachment_custody.rs | `ef12389694a41dba4148004f5c85522911496e7508cc19d8e6839f489f98e350` |
| app/src-tauri/src/auth_rpc.rs | `566b52ab2d2eedbc2f98835c07cd3369a2f9046f33d7cead063bbe9ddc45734f` |
| app/src-tauri/tests/native_namespaces.rs | `219d12f039afa218fc5205a215e05c4f58856ceb6aab7fd27c077211ddbff6d5` |
| app/src-tauri/src/home_resources.rs | `5d55a03511acf04609456f647589f82e2456bc9caeaf0d35b5880515e7f6a5f9` |

Core sources remained unmodified in targeted `git status --short`; shared lib.rs/runtime_session.rs changed during this review under their separate owner's delta. They are not included in this guard readiness claim. The shared adapter was consulted only to establish that its current probe uses ExistingHomeReference, rather than imply this reviewed bug already occurs in that consumer.

Read accepted final CC-NIR packet `5df0554883cb4ff7d89b0b480733b197f11ac03e0a02d3a2163aa3a820e9831e`, independent definition review `8659df7131ed956e321115fc21c9c21c30aea8e771a0d61c5a90a99870bb464b`, CC-REC packet `8f348991da3f927910bea3bdeb13391bfc4b2ee49b5459a0d4a81c35320847ad`, independent definition review `0fdac540585c6708d1d731b55f1ef2f58005aed163be1df38337855e0f724fe3`, native guard author return `6ba33bb3a4942f4027bf629d5e091b79385ac75c17dadfb7d9aa8945e08689f8`, shared custody/ARC1 return `31af9afa1efa98b582970843887964d7e21a84d417dc19fb95a3c69bf98408cf`, and ARC1 independent review `85c50659c92af30ce78d631e39dc668ce0fb74b9041d941b0536759237d6dca8`. Predecessor failures remain historical; neither their checks nor former reviewer identity is borrowed.

## NG-1 — owned probe direct entries are rejected as missing M-A sharing

**Blocking, P2.** Location: `app/src-tauri/src/attachment_custody.rs:202–205`, NativeHomeNamespace::observe's Planned branch; explanatory source `home_resources.rs:303–306`.

Trigger: create a legitimate OwnedHomePlan for HomeClass::Probe with shared=None beneath the explicit App root, prepare its directory, and later have an ordinary direct config.toml or AGENTS.md file or direct skills directory in that probe. Supply it through the public NativeHomeNamespace::planned API together with distinct healthy account/key homes and disjoint REC/NIR domains. No foreign target, malformed path, missing required M-A descriptor or content inspection is involved.

OwnedHomePlan::observe intentionally reports ResourceState::Conflict when target=None and a fixed entry exists, captioning it "probe has an existing resource; preserved, not shared by this module". That is not a namespace overlap determination. The new Planned adapter rejects every Conflict before computing its `class != Probe` required-sharing flag or letting protected() inspect actual fixed metadata. Consequently from_root refuses the safe complete binding; if this probe was initially empty and the binding installed, any later direct entry makes both REC append and NIR use fail. Healthy unrelated account persistence/attachments are then suspended by a probe-local direct entry that remains entirely inside the already protected H-probe.

The final CC-NIR R1 paragraph at lines 188–194 explicitly distinguishes probe's source-owned "no shared resources" from missing REQUIRED M-A descriptors, allows direct local native entries protected by H, and says it chooses no requirement that a native home stay empty. The independent final definition review repeats that no empty-home probe policy is introduced. OwnedHomePlan exposes Probe as an accepted class; NativeHomeNamespace::planned accepts that owning descriptor without an exclusion. This is therefore an implementation mismatch in the supplied guard API, even though the current separately owned Root adapter supplies its probe using the received branch.

Repair direction: retain the strict planned Account/ApiKey M-A relationship checks, but let Probe with no intended targets pass to the existing fixed-entry metadata checks. Those checks already permit correct-type absent/direct H-protected entries and refuse unknown exposed symlinks, wrong types, unavailable closure and geometry conflicts. Do not simply accept every Conflict, infer sharing, or drop native-resource protections. Add focused owned-probe positive controls for safe direct fixed entries before bind and after installation, plus exposed-link/wrong-type inverse controls. Assert healthy REC/NIR use remains available for the direct control and unchanged bytes on refusal. Existing seven namespace tests exercise direct entries only through ExistingHomeReference, so their passes do not cover this branch.

This finding is source-confirmed, not described as an executed failing fixture. No broad suite rerun is required to establish the deterministic branch mismatch. The manager may commission a focused synthetic reproduction/repair under its compile reservation.

## Examined behavior and retained limits

The finite binding is private Rust source descriptors, not JSON/H5/completeness Boolean authority. from_root rejects empty/duplicate IDs/classes, resolves current/prospective homes and only the three fixed names plus supplied sources, protects declared and actual source targets, and rejects unknown foreign links or current drift. No home-directory census or native content read appears in this path. App parent-of-key allowance is guarded by S/C/lock domains and native protected closure; domains and actual owning leaves remain fixed. Full generation/home membership is validated before NIR client publication/readback. Host dispatch rechecks durable preparation under its existing source lock before the actual source-generation/pipe commit barrier. This review does not claim hostile filesystem isolation, absent-name future case equivalence or atomic custody against arbitrary later replacement; the prior home-resource review explicitly retains those limits.

REC independently checks its own declared leaf geometry, parent redirection, single-link regular leaf and opened dev/inode/name association before read/append. App preflight reads the actual configured leaf and source-home membership, and binding installation occurs only after successful preflight. A bad candidate cannot replace the healthy installed ledger binding. The preserved descriptor early-return repair records the configured path/session before attempted guarded open, allowing restored geometry to expose original ledgerUnavailable/bindingCommitted:false without creating a second ledger/home or claiming persistence success.

Native request/reply/Stop paths remain independent of optional REC append success. CapturedRecoveryQueue retains strong App ownership while live Inner remains weak; writer/ledger IO finishes before live-source updates. The drift test exercises actual owned cat reply/Stop, immutable RQ facts and unchanged disk followed by restoration and explicit exact-once flush. The full SourceRequest/ordered attachment test checks actual prepared source metadata, foreign-home refusal and current-use drift before attachment dispatch; refusal leaves native Host ready. ARC1's retired-source tests retain pointer facts/errors after Host/readers retirement and preserve one-attempt unknown App-end behavior. No new storage root, persisted schema/kind, retry or native qualification is inferred.

Author evidence records 99 affected passing checks (namespace7, Host70, REC10, attachment6, startup6), with the ignored internal Host worker covered by its active watchdog. Those are author executions, not reviewer executions. I inspected their actual source assertions and recorded failures. I ran only read-only Git/source/hash commands (`git rev-parse`, targeted `git status`, bounded `git diff --stat`, `rg`, `sed`, `cat`, `shasum`) plus the report-writing Python command. No cargo test/check was invoked. One initial repository-wide git status emitted an unrelated existing symlink-loop warning; targeted Core status succeeded. No result is inferred from that warning.

## Context custody

Root AGENTS, TASK role, App-v4 LOOP_INIT, alignment README/current Agent User Manual headings through level three, full Field Book, Group A work graph, pause handoff, and the named packets/reviews were read. Group A graph reports no active B/C/D/E graphs; bounded TASK review does not reconstruct/resume their graphs. No other full role or workflow was activated. Actual origin hashes follow.

| Source-qualified repository path | SHA-256 |
|---|---|
| `AGENTS.md` | `f96feb19d297c74e10048c506805b2fe3622c50cfefd6078f599724556113977` |
| `agents/AGENT_TASK.md` | `1a13a5b00b3ce01ff8519efe6b46bcbe0cd6a5b7985e24282fa7efa2c57c8fb7` |
| `.agents/skills/software-code-review/SKILL.md` | `ee085d589c44f912d11a59eead8edac214f0343761d26b0d33e886a979888bca` |
| `projects/chirality-app-v4/loop/LOOP_INIT.md` | `45c23cf477e23aff1d0152189caf7e8ebfb53eca42e3a1fae87a06af8c197f28` |
| `docs/alignment-manual/README.md` | `31217d30b0d2743bef0d7c1a54bb9a81814d56b24ff0961cf01d9532952e305f` |
| `docs/alignment-manual/CHIRALITY_AGENT_USER_MANUAL_v3.md` | `08ca0e40cd5157574a011bac57d539e77e9007a0d46494785da8b92745391b1a` |
| `docs/alignment-manual/Project_Management_for_Human_Agent_Teams_Field_Book_v1.md` | `02d53a3966220001318aacf3f46e1b63b8695a098c81b20f4e3e1531b93024d3` |
| `projects/chirality-app-v4/execution/_Coordination/WorkGraphs/APP-V4-GROUP-A-20261004/WORK_GRAPH.md` | `fe6d026d733489cf10c6b602deeb2b09f2244c0e392ec99ce9629df160ac6ad6` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/PAUSE_HANDOFF.md` | `21e8156ce28cdc74bdd59d417f0cfa368fa25e22d3fa0aa18ccf251438a501c1` |

Return NG-1 to Core for bounded repair and exact successor backcheck. Ordinary source repair introduces no new human approval gate. Shared consuming review, real home/auth/native/UI qualification and whole-Group-A completion remain separate.

## NG-1 / PG-1 exact affected successor backcheck — 2026-10-05

**READY for the bounded Core namespace/REC/NIR guard contribution; NG-1 (manager PG-1) repaired. No remaining actionable finding in the reviewed scope.** Original report prefix SHA-256 `6ebab240e445456807a4d33cd21204c34f3bb13a63adbc55de59b2ce166d7428` remains unchanged. This is the same replacement reviewer instance's affected backcheck, not a claim of the historical reviewer's identity, independent test execution, whole factory/Root consumer readiness or native qualification.

Independently hashed/read exact successor custody `04f82cbd64fe5a9c40b57556a804c063740019d584f0cf68aeab9172a2d58082` and namespace tests `765e90d46fa52a25760bd5e7472727c436b13d1b6074bdc072643aacf1e7af85`; unchanged Host6c48/RECf0ff/auth566/home_resources5d55 match the original pins above. The actual product diff against f480 is one Probe class condition plus explanatory comment; the tests append three controls. Original seven tests independently compare as an exact unchanged byte prefix. Original failing before-binding positive body independently compares byte-identical to the preserved original-test-additions.rs body.

Actual author original-vector evidence read/hashed: `probes/PG1-PLANNED-PROBE/original-result.json` SHA `92bd966065b1acc3e3d8b07d1b18a522cc080b4a34fc62d255a1d57684203f80`, additions SHA `58298648acd32e67d3cefa6a6fed6481d60e1e046e550f968a02f767255c12d9`. It associates a read-only Git archive of exact f480 unchanged product source with the appended control, approved offline/locked cache/skip-stock command and exit101, 0/1 pass, exact anticipated safe-direct Probe refusal. This is now an executed original failure by Core, distinct from this reviewer's original source-only finding. It is not inferred from an unrelated pass or altered criterion.

The successor excludes only Probe from the preliminary M-A sharing-state rejection. Account/ApiKey retain their original required-sharing checks. Probe still reaches unchanged protected(), which observes all three actual fixed names, protects absent/direct entries by home/slot location, and refuses foreign links without declared source closure, unresolved targets, wrong types, unknown metadata and owning geometry collisions. Probe's target=None is not promoted to a safe Boolean. No contents are read or resources copied/repaired. The inspected source now conforms to the named final NIR/REC no-empty-home/probe distinction.

Positive controls place direct config.toml/AGENTS.md files and skills directory under the actual OwnedHomePlan Probe before binding and after installing an initially empty binding; REC append and current NIR scope use remain available. The inverse loops cover each of those three names against foreign target, unresolved target, actual-owning-domain target, and wrong direct type (12 combinations). Each checks fresh binding rejection, installed NIR/REC use rejection and unchanged existing ledger bytes. These preserve the original protection while exercising the precise adapter branch missed by the earlier received-Probe control. NIR full publication/source/dispatch and unavailable recovery/startup behavior remain covered by the unchanged affected receiving tests and the preserved original Host controls; the pure NIR scope assertion alone is not claimed as a new full native send witness.

Read/independently hashed final author return `changes/I1-NATIVE-NAMESPACE-GUARD-RESUME.md` SHA `9fc33e65feeff8a4c9d7476d70bd2018c1d36cd368a98b84abe477743f74b070`, and actual tested-source manifest `probes/PG1-PLANNED-PROBE/repair-result.json` SHA `50f7898d10fad3c4976a5e9dbc7d3f5ed259c4ba5917370d1423fa4847495ebc`. Exact Core pins match the reviewed successor; manifest retains shared stationary compile inputs rather than claiming the unrelated consuming delta is independently reviewed. Actual author commands from app/src-tauri used approved `CARGO_HOME=/tmp/chirality-app-v4-group-a-cargo-home`, `CHIRALITY_SKIP_CODEX=1`, `--offline --locked`:

- `cargo test --offline --locked --test native_namespaces`: exit0, 10/10 PASS, compile8.31s/run0.40s; includes the original failed positive unchanged and the inverse12.
- `cargo test --offline --locked --test attachment_transport --test recovery_startup`: exit0, 6+6 PASS, compile0.90s/run0.20s/0.06s.

Author22/22 is actual tested-source evidence, not reviewer execution. Four existing native_history dead-code warnings are disclosed. Manager selected these affected checks and declined blanket Host70/REC10 repetition for this narrow condition; those source files are unchanged and the adapter repair does not alter their healthy, mandatory-reply/Stop, full-generation, strong queued-fact or restoration mechanics. Original99 remains historical on its original source, not relabeled as successor executions. The unchanged test prefix, retained original-vector oracle, explicit inverse controls and actual successor result establish repair; a passing count alone would not.

Reviewer executed only read-only hash/diff/source comparisons and the append command; no Cargo/process/native/auth/source mutation or delegated work. Author released the completed Cargo lane before its final freeze. Separately reported shared access consumer test failures belong to that consumer's repair/review, with no guard source change or borrowed pass here. No universal hostile-filesystem guarantee, real H-key/home/auth/model/supplier/UI witness, whole Group A completion, human acceptance or release follows.

Release this exact bounded Core contribution for manager fan-in and the separately owned consuming review. Ordinary repair/backcheck adds no new human approval gate.
