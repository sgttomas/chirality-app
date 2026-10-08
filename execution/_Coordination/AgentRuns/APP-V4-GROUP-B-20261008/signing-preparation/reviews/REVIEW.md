# Independent B4/B9 preparation review

READY for bounded preparation fan-in at exact author
`b2231d16a7ca29d3947712996ffe186bd34305b3`; no unresolved blocking findings.
Initial candidate `a05abdc21b95710cd7d92c618c6b1913d90921c8` was reviewed against
`5d562a1f11bdad3f6794f6ff4ca25e665e9f5e06`. The repair changes only
DECISION_PACKET.md; physical artifact, terms and passive evidence are unchanged.

TASK `/root/group_b_successor/complete_content_review` is an independent native
child of WORKING_ITEMS `/root/group_b_successor`; no delegation. New managed
checkout and `codex/app-v4-b4-prep-review` branch were used. Author retains repair
custody; reviewer writes only this file. No push. This review applies to a
preparation packet, not signing authority, qualified-package standing or release.

## Findings repaired and rechecked

1. The initial SP2 outer-App command omitted --force after separately signing P0.
   Local `man codesign` documents that linker-signed signatures can be replaced
   without force, but ordinary existing signatures cannot. The outer operation
   must replace the App's main-code signature established by the first command.
   Repair adds --force solely to the explicit outer App target, prohibits nested
   supplier resigning, retains no --deep for signing and retains exact FP1(b)
   comparison. Static command review closes this finding; no signing occurred.
2. The initial prerequisite table demanded an actual H3B joined witness and the
   following paragraph demanded qualification inputs first, creating a possible
   circular prerequisite to signing. Repair explicitly separates implementation,
   selected source/pin/reference readiness from later installed signed-candidate
   FP2/W4/H3B runtime qualification. Later witnesses are required for qualified
   reliance and explicitly are not prerequisites to signing. Ordered step 8
   remains the later native examination. This closes the sequencing finding.

## Independent passive checks

- Re-read the retained B2 bundle using unchanged read_tree. All 74 entries,
  including 56 file hashes/sizes, directory/file modes, link state and displayed
  Mach-O metadata match the prior full inventory. Manifest remains
  `cd0e8f7216d6c85b1b1cee96300e3b1f4aeaea15bbc6185214345290bdb83c15`.
  This preserves the earlier independent physical review's subject.
- Compared packaged P1 with the actual selected approved cache; exact contents,
  modes and links agree, including root mode. Replayed unchanged fp0: all seven
  checks pass on 42 files, 10 directories, 30 Mach-O; manifest
  `327effb91a5854eccb388321b4b160e059795f0402c553f594e85365189d8d12`.
  These are cached development-tree metadata/content observations, not provenance,
  newest-version qualification, cryptographic signature verification or FP1(b).
- Initial sandboxed metadata display lacked some authority/timestamp/entitlement
  values; content comparison still passed. Scoped host permission for codesign
  display restored the full metadata and exact inventory match. No mutation,
  keychain enumeration, credentials, native App or supplier execution occurred.
- Independently compared actual P2 and P3 with current production_workflows and
  instructions resources: equal. Their earlier exact role/manifest binding review
  remains applicable to these unchanged bytes.
- Independently reproduced all ten changed compiled-source paths from f79317be
  to 5d562a1f and every old/new Git blob digest in STALE_SOURCE_BOUNDARY.json.
  The retained executable is not upgraded by newer source or support adoption.
- Verified all seven current SUPPORT_BASIS source pins and canonical-pins digest.
  The receiving supplement keeps inventory/unsigned preparation partial; this
  packet creates no canonical result/package cohort or retrospective producer-use
  claim. Terms records are outside the specified six-role cohort.
- Read the actual canonical OpenAI.json: absent at the preparation basis, now
  unresolved with not_made decision, actual author TASK recorder, and no response
  object. Independently passed unchanged Draft202012Validator schema and PK-R4
  terms_violations; its digest matches TERMS_VALIDATION.json. No contact, supplier
  response, legal conclusion or owner act is asserted.

## Decision and residual limits

The packet binds f79317be plus the identified overlay, exact P0 and full bundle
identities, rather than 5d562a1f or later Host implementation. CF1 App identity,
CF5 intended product values, CF7 profile and applicable source/reference and
entitlement choices are explicitly unresolved. Proposed operations preserve
Option B, separate human signing from recording, require post-sign supplier
comparison, and keep notarisation/stapling/quarantine observations distinct.
No signing readiness or point-action authorization follows from this READY.
R23-22 selection, applicable S3/H3B inputs, actual later native qualification,
FP1(b)/FP2/FP3/FP4/FP5, M2/M3 and owner release remain unsupplied for this artifact.
No artifact rebuild, copy, signing, installer, download or native operation was
performed. The review does not assert that the proposed commands were executed.

## Read origins and hashes

Root/TASK, selected review/change skills and LOOP_INIT were carried from the
prior bounded review and remain applicable; current source hashes are recorded
below. Prior manual entry reading is retained in complete-content/reviews/REVIEW.md.
This review read canonical PKG CF/FP/terms requirements, unchanged prototype
read/rule functions, current support supplement/pins, all new packet evidence,
and local codesign manual sections on force and linker-signed signatures.
No MEMORY was read or written. Git identity: Ryan C Tufts <ryan@chirality.ai>.
Staged private-term validation is required before committing this review.

- `AGENTS.md` — `f96feb19d297c74e10048c506805b2fe3622c50cfefd6078f599724556113977`
- `agents/AGENT_TASK.md` — `1a13a5b00b3ce01ff8519efe6b46bcbe0cd6a5b7985e24282fa7efa2c57c8fb7`
- `.agents/skills/software-code-review/SKILL.md` — `ee085d589c44f912d11a59eead8edac214f0343761d26b0d33e886a979888bca`
- `.agents/skills/chirality-change/SKILL.md` — `1a2b056263ec77e4104efdf99afe3fe76dda792334a243fb2f21c60bc9c81450`
- `projects/chirality-app-v4/loop/LOOP_INIT.md` — `c2e88f81439ed03578fee13fd7563082fefdfe11096d9134a59531eba3b985bd`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-06_macOS packaging and distribution evidence/Design/PACKAGING_AND_DISTRIBUTION.md` — `0d8d14d2ce08d859ec3b304f5c8c250afa7f0a6fe95eae3a61920f71d2a442b4`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-06_macOS packaging and distribution evidence/Design/pkg.terms-record.schema.json` — `46ee0d3c0072fd3a94c45749fd8da14ad05e6322367f2df51500e754eb6e6af9`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-06_macOS packaging and distribution evidence/Design/prototype/check_pkg.py` — `1b6f1232fe0b200ffbb0eb56dfbbdfe4a4f29dab3c83e8e1d42b195d752f8d23`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-06_macOS packaging and distribution evidence/Design/prototype/read_tree.py` — `6dacea788f0a0690ca04bc95f4d50332f4d3ddafb5bb0339147460e64b2debdb`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-06_macOS packaging and distribution evidence/Design/SUPPORT_IDENTITY_BINDING_V1.md` — `7affbb8cea544a29bbf485e4fc6b1e0c15d5666e9c3614110580d912ff344e5f`
- `projects/chirality-app-v4/app/examination/support_identity/canonical-pins.v1.json` — `9ad24d5d6fa38afbeaa39b532f9a10d9550f964f463a8a49356ef254caba35b4`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-06_macOS packaging and distribution evidence/Evidence/PKG/terms/OpenAI.json` — `d57ab4d4c3704c99294af73e862008589603e27c8d63bc8cba5b3d5be4cc13fd`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-B-20261008/signing-preparation/ARTIFACT_RECHECK.json` — `b1c8a64aaf2e8b4b8f8ae33c2c3b70ea49f2f001edc5e0d5978780006f4452c9`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-B-20261008/signing-preparation/AUTHOR_BASIS.json` — `20e576a961a6e73c081306875925c5132a9a61ad5aaf80aa675b06394ae0ca47`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-B-20261008/signing-preparation/COMMANDS.md` — `4b85dca01cf93b0f917b521349c6b68091f739a93fbfb0a11664a51d3cdcce24`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-B-20261008/signing-preparation/DECISION_PACKET.md` — `35438f8c96f8bcf37e098a66038f664e163104bda7e5d1b55c4eb419ca4cd291`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-B-20261008/signing-preparation/FP0_CACHED_VENDOR.json` — `1286a9126158a78fbe28982ba0225f4fabee24aedbc33b323560fcb4dadca6d3`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-B-20261008/signing-preparation/P2_SOURCE_JOIN.json` — `88dc6bbb6062a9c26d481175a1a7a56adb93e240d0c03d72e971b72a48485821`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-B-20261008/signing-preparation/P3_SOURCE_JOIN.json` — `ef66dbefec771e5cc064ba3aa2f309e14ad45724ae6eb7b1477f0b7aa1dd8621`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-B-20261008/signing-preparation/STALE_SOURCE_BOUNDARY.json` — `0976f10471d4fc52458a5a7000d3e17f1aa8f19f18ccc0c2143459e46ad5e7ef`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-B-20261008/signing-preparation/SUPPORT_BASIS.json` — `96c6e56ada48e0116c96f3d04624b1e91542c6db13ff96648df171ddaf537444`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-B-20261008/signing-preparation/TERMS_VALIDATION.json` — `64ab0a202f0acd647dfb4e43b8cfbbbabde697bb8a67b63d781459b3bb9055ed`
