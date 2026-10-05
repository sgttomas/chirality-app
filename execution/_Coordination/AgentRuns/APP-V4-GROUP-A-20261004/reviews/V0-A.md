# V0-A — independent frozen CC-A contract review

Date: 2026-10-04. Verdict: **definition ready for manager fan-in and bounded consumer propagation; no blocking, major, or minor defect found in the reviewed candidate.** This is not an implementation verdict, AC/VER pass, product qualification, owner acceptance, placement selection, or release.

## Assignment and identified basis

Independent TASK `/root/group_a_execution/aac_contract_review`, delegated-harness-native child of WORKING_ITEMS `/root/group_a_execution`; parent hierarchy continues to HELP_HUMAN `/root`. Supplied assignment: review frozen CC-A, CI-4/5/6 and authorized CI-1/2 consumer changes against base `e916ad1789`, write only this review. No delegation occurred. Actual tools: read-only local Git/source inspection, installed Python and jsonschema, offline existing prototype commands, and creation of this review. No Git mutation, download, network, credentials inspection, sign-in, live turn, product/Design edit, or lifecycle act occurred.

Selected skill: `.agents/skills/software-code-review/SKILL.md`. No V4 software-workflow.json or scope validator profile was presumed. Root/TASK/LOOP_INIT, current manual index, manual headings through level 3, full Field Book, manual 60% guidance, Group A work graph, V0-BASIS, SoW, CC-A and relevant original decision records were read. The current graph inventory contains no B/C/D/E development graph; cross-group propagation remains with the manager through Group A's recorded relationships and receiving graphs when constructed.

CC-A change record SHA-256 `c4cd3162e77fe6463ed8d6ba1db040d2deb2bb4021b21c07ba7bc3603db0b893`; AAC SHA-256 `bdcc8643f1ecc2423d5a90b2ba5afb3eac572c34525f5fa144732b3ee3eda02d`. All 15 entries in CC-A's final frozen contribution manifest match their actual bytes, including the four retained outputs. Reviewed every changed tracked contribution against `e916ad1789`, plus the new sequence model and retained results. No candidate drift was observed during this review. Other concurrent product changes are outside this verdict.

## Contract conclusions

| Criterion | Independent assessment |
|---|---|
| CI-4 scope | AAC §4.1a and both schema descriptions use exactly “not named by the package” for omitted/empty package scope, show it in native confirmation and copy it into capture/RS. Nonempty strings stay unchanged; non-string input is invalid. Package schema remains optional; absence is not inferred authority. The run OWNER_DECISIONS records the actual owner choice by trusted relay. Current RS §13.6 independently carries the same label while retaining absence/empty in the source request. |
| CI-5 authoritative choice | §4.1a freezes host offer/digest, selected ID and shown actor before opening confirmation; native text includes the chosen statement and every consequence, content/scope/purpose and references. More than three choices remain possible. Full-text failure refuses presentation. Native Cancel/dismiss captures nothing; changed/absent/unreadable package, invalid digest, ambiguous ID, cancelled snapshot and repeated capture refuse. New callback text/choice cannot replace the frozen choice. NA-1…4 remain applicable and no script route is authorized. |
| CI-6 durable sequence | §5.2a requires complete validated durable capture before append; initial recordId absent; RS alone mints the ID. Verified written entry precedes add-once atomic backlink replacement. Original act facts remain immutable; equal backlink is no-op, different backlink conflicts. Failed backlink retains AC-7 with explicit pending message. Uncertain publication cannot be called definite absence. Recovery verifies capture-ref and facts, requires complete readable logs before late write, holds torn/ambiguous/orphan/conflicting cases, and shares the writer/capture boundary with W-2 flush. No current bytes, new capture, backdating, duplicate act or log truncation is allowed. Conditional resealing does not adopt SEAL-2. |
| CI-1 consumer registry | run_cases.py loads EXEC checkpoint schema under its declared ID into the same Registry as RS. Full combined cases resolve the composed schema; no reference rewrite/fallback was added. Earlier failing outputs remain historical evidence rather than being erased. |
| CI-2 NIR consumer | Answer schema ID/format 0.2 requires exactly the complete object `{appSession, home, spawnCounter}` with positive counter and nonempty identities. No integer/null legacy union. Model receives retain full tuple; closed-generation keys and answer correlation use all components. R-16a rejects equal counters from another session or home without settling the outstanding request. Other native answer/origin/refusal criteria are preserved. |

P-2 remains labelled PROPOSED in AAC §6.2 and R17-5; rejection of P-3 in DECISION-L L-5 is not affirmative P-2 approval. The actual graph-closure owner record says “I am accepting the 60% gate cleared.” That decision allows Group A detail work through the local graph; it does not verify native script isolation or select every path. OI-008 retains the App implementation owner under SoW TBD-003 and L-7. There is no basis here for inventing another owner ceremony to clarify this already commissioned contract. The manager must retain truthful placement standing and examine the implemented boundary.

The placement comparison in CC-A is a proposal only. AAC explicitly leaves capture storage unchosen; its durable same-directory publication requirement does not choose a directory. User-library A15 capture/log resolution, legacy log discovery, migration and cross-project portability remain inputs to the exact placement implementation. No common service or host allocation follows from this review.

## Independent checks and evidence limits

- Existing `PYTHONDONTWRITEBYTECODE=1 python3 cc_a_sequence.py`, cwd DEL-01-04 Design/prototype: exit 0, **20/20**. Stdout SHA-256 `a4076de9bd08e7990a194ef569baa83b30e9e8e13a74bef00ee262f9c0146417`, no stderr.
- Existing `PYTHONDONTWRITEBYTECODE=1 python3 run_cases.py`, same cwd: exit 0, **161/161**. Stdout SHA-256 `71e630445eb2489d144f2ca4f35c73e6aece029dcceeba5cc59a6d5c1064cd0d`, no stderr. Scratch logs use the existing system temp convention; no fixed output file was overwritten by this review.
- Installed `jsonschema` 4.26.0, Draft202012Validator: checked schema validity and independently validated AAC offer 4 valid/19 invalid examples, capture 3 valid/15 invalid examples, NIR 1 valid/6 invalid examples. All expected outcomes agree. Five additional NIR mutations reject integer, null, missing spawnCounter, zero counter, and historical formatVersion 0.1. An initial local check script incorrectly assumed NIR's valid fixture was a list and raised IndexError after all example checks; corrected to its `instance` field and reran the five mutations successfully. No candidate repair was involved.
- Python `/Library/Frameworks/Python.framework/Versions/3.13/bin/python3`, 3.13.7. The sequence model assumes atomic publication/replacement and exclusive scan/append; it has no filesystem, native surface or real W-2 pending queue. Its 20 checks do not demonstrate concurrent workers, native full-text layout, inaccessible scripting, uncertain fsync, or OS crash durability. Historical act_control.py still pre-mints its model ID; the 161-case combined pass is schema/model compatibility evidence, not CI-6 product evidence. Author claims expressly retain these limits, so this is a residual verification obligation rather than a defect hidden by a pass.

## Required propagation and return

The definition is usable as the bounded implementation basis. Consumption is not yet satisfied merely by this review:

1. Group A host act_control/lib and RS writer must implement and test the frozen choice, initial durable capture, verified add-once backlink, explicit failure truth, full log discovery and shared W-2/recovery serialization. Exercise publication uncertainty, crash before/after append, failed replacement, torn logs, simultaneous recovery/flush and repeated recovery on the actual filesystem; native witness must cover full selected text and script attempts.
2. RS owner/reader and EXEC checkpoint recorder must preserve writer-minted identity and original capture time, count only conformant actual records, and distinguish recorded/link-pending from absent/pending. AAC backlink alone never establishes a record. RS CI-4 text is already aligned; this review does not claim the remaining CI-6 writer/reader propagation is implemented.
3. WR A15 registration must avoid repeated effects on backlink/recovery retry and retain separate per-entry outcomes. Resolve the owning library's capture/log references before path implementation.
4. DEL-01-01/02 request register, DEL-01-04 card/submission validators, schema registries and product tests must adopt exact answer ID `urn:chirality:app-v4:del-01-04:nir:answer-submission:0.2` and complete generation correlation. Historical 0.1 records need explicit version treatment; silently admitting them through a union would undo CI-2.
5. Carry decision-view/standing semantics to downstream DEL-06-02 and DEL-04-02 readers and conditional SEAL-2 consequences to packaging. Group A already records those cross-group relationships; actual receiving adoption belongs to each owner.

No new deliverable, changed group order, narrowed acceptance criterion, extra per-act presence check or new human gate is proposed. Product propagation remains bounded by the manager's release of the relevant scope and outstanding concrete placement/validator dependencies. Return: no frozen definition blocker; actionable consumer and product-witness obligations above remain open under their existing graph nodes.

## Read-source fingerprints

Hashes below identify observed source bytes, not human hash approval or adoption by consumers. CC-A's matching full frozen manifest supplies the contribution/output fingerprints.

| Source | SHA-256 |
|---|---|
| `AGENTS.md` | `f96feb19d297c74e10048c506805b2fe3622c50cfefd6078f599724556113977` |
| `agents/AGENT_TASK.md` | `1a13a5b00b3ce01ff8519efe6b46bcbe0cd6a5b7985e24282fa7efa2c57c8fb7` |
| `.agents/skills/software-code-review/SKILL.md` | `ee085d589c44f912d11a59eead8edac214f0343761d26b0d33e886a979888bca` |
| `projects/chirality-app-v4/loop/LOOP_INIT.md` | `45c23cf477e23aff1d0152189caf7e8ebfb53eca42e3a1fae87a06af8c197f28` |
| `docs/alignment-manual/README.md` | `31217d30b0d2743bef0d7c1a54bb9a81814d56b24ff0961cf01d9532952e305f` |
| `docs/alignment-manual/CHIRALITY_AGENT_USER_MANUAL_v3.md` | `08ca0e40cd5157574a011bac57d539e77e9007a0d46494785da8b92745391b1a` |
| `docs/alignment-manual/Project_Management_for_Human_Agent_Teams_Field_Book_v1.md` | `02d53a3966220001318aacf3f46e1b63b8695a098c81b20f4e3e1531b93024d3` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/reviews/V0-BASIS.md` | `3d9644efdd2086630b6c319871c54d3eb0239d80d131f43083d0927b2270b906` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/OWNER_DECISIONS.md` | `cc1c7f3aaaf9dbf02cd6676afd80662fe1c051ef43142a1965b0d8d6a5cf6617` |
| `projects/chirality-app-v4/execution/_Coordination/WorkGraphs/APP-V4-GROUP-A-20261004/WORK_GRAPH.md` | `93fb8dd8a544e9b8a44d5d028d5f6c07d707ba300d417dd09cbc89a8e0d8fc44` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/ScopeOfWork.md` | `8434cc47ec28e1397e7dae548183543567f0b5fcfdefaebc0b44bc1f709aacf3` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-DESIGN-PASS-3-20261001/R17_RESOLUTIONS.md` | `b0af81bcbad9bc52fddc99119c42a19019a9b174677d5b92a0a2f5c8b4f8e198` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-DESIGN-PASS-3-20261001/OWNER_DECISIONS.md` | `8a5d11149045770dfcf1a19ebabb86bfe9f04cd3e65ed36166cb8593e2fe20ac` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-DESIGN-PASS-4-20261003/OWNER_DECISIONS.md` | `e4350f61a93edf0d2d4bfc588fcaa17ae23981baa6059617dcc430cda3008cd8` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GRAPH-CLOSURE-20261004/OWNER_DECISIONS.md` | `9494d39b7405fc6342aea13e00073fbdebe21c5014e32620b752321fa1aa6136` |
| `projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-03_Content-bound decisions and compact run records/Design/RECORD_SEMANTICS.md` | `0cbf416d3740955971a1c94b92416b0d78936ea462231882b232e8671854b5f3` |
