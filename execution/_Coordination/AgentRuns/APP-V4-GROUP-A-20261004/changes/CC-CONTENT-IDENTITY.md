# CC-CONTENT-IDENTITY — Bounded App byte and workflow-package methods

PROPOSED named technical selection, applied in DEL-02-01/DEL-02-04/DEL-03-01 Design only; fresh independent review and consumer propagation required. 2026-10-04. TASK `/root/group_a_execution/design_hosting_access` under WORKING_ITEMS `/root/group_a_execution`; no descendants. No RS, app, Cargo, Git, shared graph, MEMORY, SoW, register, supplier execution/network/download/auth/model turn changes.

## Decision-ready choice

Select two explicitly designated **App-only** production methods:

- `chirality.app.exact-bytes.sha256/v1`: lowercase 64-hex SHA-256 of exact stored/supplied bytes, no normalization or excluded bytes. ROLE uses it separately for source/role-set/default bytes, composed guidance and child-config file bytes; composition wrappers and UTF-8 encoding are part of the actual composed bytes. It also defines App-owned file identity, subject to RS receiving adoption. Existing method/value objects remain unchanged in shape.
- `chirality.app.workflow-package.sha256/v1`: SHA-256 over ASCII method designation plus NUL, then u64 big-endian file count, then for each file sorted by UTF-8 relative `/` path bytes: u64 path byte length, path bytes, u64 content byte length, exact file bytes. Lowercase 64-hex value. No ambiguous separators/concatenation or parsed JSON normalization. A recoverable ordered manifest holds path, byte length and exact-byte method/digest per file; it is evidence beside the package, not the package hash input. Root path/name/origin remain tuple elements distinct from content.

This technical choice concretizes existing WD U-03 and ROLE U-R1 promises for App-owned content. C TBD-003 host technical agreements remain open: no host read/subject/whole-model/change-item hash, host canonicalization, host method scheme or one-effect is selected. C §5.5 explicitly preserves exact opaque host carriage and method comparability. No scope or accepted obligation is reduced; no new human gate inferred from an ordinary implementation choice. Independent named review is still required before product use.

## Source-faithful boundaries recovered

WD §6.1 RV-1 includes **every** regular file beneath the package at any depth; RV-2 refuses symlink/non-regular entries, never follows them; RV-3 uses stored bytes without line-ending/encoding/whitespace normalization; RV-4 uses UTF-8 relative paths with `/`, ordered by those bytes; RV-5 omits empty directories only. No file/content exclusion introduced. Directory containers are traversed; symlink roots, specials, unreadable content and invalid UTF-8 paths refuse identity establishment. OS metadata files remain included; WR HY-4 may separately refuse them for registration rather than silently remove them. The method identifies a captured snapshot; WR RB-1…RB-4 retain live-source/copy/registration drift checks. Hash computation alone never proves an atomic filesystem read, registration, human act or qualification.

WR ID-1/ID-2 already equate reviewed draft folder content with registered revision content under RV-1…RV-5; both now use the same package method. A15 binds that method/value per RB-4, not just a name/location/UUID. WD tuples keep origin/source root/name/derived-from and holding-library semantics. Stored bytes of WORKFLOW.md remain distinct from a parsed declaration or WR-FRAME-1 run-start composition; a composed message uses exact-byte method separately, and a source identity must not be replaced by the composed-message digest.

EXEC TR-4 carriage manifest carries source tuple, revision identity/method, declaration contract version, tool/checkpoint summaries, compatibility report, observed exporter, time and transfer identity. It is a convenience and does not override the package's declaration. It remains a separate artifact; if put physically inside the package, its bytes enter RV-1 without any self-exclusion. Digest/manifest records should be stored outside the identified tree to avoid changing the content they identify. Package creation requires the original regular file set, never source narrowing to fit a parser.

ROLE CO-1…CO-5 preserve part offsets/lengths/source identities and no normalization; new method changes only identity designation from illustration to production selection. Non-UTF-8 guidance remains refused; supplied ≠ adopted, inherited ≠ freshly supplied, unknown remains unknown. Historical illustration values/methods are carried unchanged and do not become comparable by relabelling.

C §5.1–5.3 and SoW REQ-004 require host-supplied read/subject identities and methods; whole-model fallback remains over-lapse, never App-computed host evidence. C SH-1 truncated sorted-JSON identity is the double's own assumption, not selected by this change. RS OF-3/L-1/L-2 keep domain truth and host identity with the host; method mismatch/missing comparability is unknown/incomparable. RS content/method fields, operational UUID record IDs, captures, transfer IDs and offer/test digests are separate facts; this selects no global canonicalization.

## Changes and checks

WD §6.1 defines exact framing and manifestation; U-03/VC-56 and schema description record its bounded scope without narrowing accepted legacy/host identity values. Prototype revision output adds the recoverable manifest and selected designation. ROLE §6.1/U-R1 and cid() use exact-byte method; existing supply examples retain historical methods while fresh emitted records use the selected one. C §5.5/U-C1 scopes the decision to App subjects. Two prototype READMEs explain current versus historical methods.

Offline standard-library checks: WD selftest **62/62**; ROLE full suite **38/38** (including exact-byte abc known vector and line-ending/Unicode-byte sensitivity); package independent framed reference vector plus binary bytes, empty-directory/relocation invariance, content/line-ending/system-file/path sensitivity and symlink/root-link/FIFO refusal all passed. Local temporary invented fixtures removed. Existing validators/schemas passed without new field-shape constraints; method strings remain opaque for old/host content. `git diff --check` passed in owned fences.

Package reference vector: files WORKFLOW.md=`workflow\n` (9 bytes), resource.bin=`00 ff` (2 bytes); digest `0c8db7f93e14aa8b667df62e56d4f7de4e3d0eae64e80112a1f519a8d26d7767`. Role abc vector `ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad`.

```text
PASS package reference framing; all file bytes/binary bytes; empty-directory and relocation invariance; line-ending/system-file/path sensitivity; link/root-link/FIFO refusal
Package known-vector: 0c8db7f93e14aa8b667df62e56d4f7de4e3d0eae64e80112a1f519a8d26d7767
62 checks, 62 passed, 0 failed
PASS CC-CONTENT-IDENTITY exact bytes known vector
PASS CC-CONTENT-IDENTITY no normalization
TOTAL pass=38 fail=0
```

## Required outside-fence propagation

**RS owner (do not edit by this TASK):** `DEL-04-03/Design/RECORD_SEMANTICS.md` §6.1 Bound content, HA-10 reviewed-draft/registered entries, §7 L-1/L-2, §10 consumer rows, §13 broad "algorithm unselected" and U-04 must distinguish selected bounded App methods from still-open host/global methods. For new App file acts/A16 c₀/m₀ and c₁/m₁ use exact-byte method; for A15 bound revision/reviewed draft content use package method and maintain WR ID-2 equality. R3 source/composed role bytes carry ROLE's exact method unchanged; workflow source package and run-start text are different identities/scopes. RS schema `$defs/contentIdentity` remains `{value, method}`/existing variants, no global const restriction. Preserve historical/host method/value, OF-3/L-1 no-mint-host rule and L-2 incomparable behavior. No record-UUID rehash or host one-effect claim. Any record-entry normalization algorithm remains separately owned.

**WR:** `DEL-02-02/Design/WORKSPACE_AND_REGISTRATION.md` ID-2/RB-1…RB-4/G-0, schemas/registration/snapshot prototype: compute this exact same package method for live/staged/registered bytes and per-file manifest sizes/digests; include all resources/binary companions, never WORKFLOW.md alone. Capture/revalidation retains complete snapshot identity and prior revision; stored manifest lives outside package. Run-start composed message uses exact-byte method separately. Shipped manifests and library records keep their actual historical method; no silent remint/adoption.

**EXEC:** `DEL-02-03/Design/EXECUTION_COMPATIBILITY.md` TR-4/U-E16 and carriage schemas/prototypes: carry revision_method and value exactly, source tuple/holding library/derived-from preserved. Complete package file set on transfer; manifest summary never overrides declared content. Method mismatch remains unknown; no host reproduction assumed. Receiver can adopt App method expressly or retain its native method.

**HOSTING/implementation I2:** carried guidance identity in DEL-01-01 HOSTING §8.2/client-record mapping and `app/src-tauri/src/` source parser/composer must hash exact serialized bytes at the boundary with ROLE/WR's exact-byte designation; source package identity stays distinct. New workflow identity maps prototype `method` to schema `revision_method`, value to `revision`; new App producers include method even though legacy-compatible schema allows absent/other designation. Do not use offer digest or UUID as content identity. The prototype consumes captured trusted temp trees; production must enforce coherent snapshot/no-link/unreadable refusal before immutable review/supply under WR RB-1…RB-4; no atomicity/concurrency claim from the prototype alone.

**I4/host consumers:** `DEL-03-02/Design/PROPOSAL_LIFECYCLE_AND_OUTCOMES.md`, `DEL-03-03/Design/ADAPTER_ENABLEMENT_AND_RECEIVING.md`, LOOP/PANEL and I4 code carry host-supplied canonical/subject/change-item method/value unchanged, including whole-model scope. They may not mint replacement content IDs from parsed host JSON, equate them with App package identities, claim one-effect or remap truncated SH-1 identities. C's host U-C1/TBD-003 and P one-effect mechanism remain external-owner decisions. GUIDE repins after adopted consumers; manager controls shared graph/MEMORY/issue dispositions.

## Related SUP1 ROLE/WD receiving preparation (read-only return)

0.160.0 regenerated ThreadStartParams, ThreadResumeParams, ThreadForkParams and native envelopes equal prior shapes. VERSION_ADVANCE records role/source/run-text/resume/fork carriage mechanisms with real limits: workflow remains per-run turn text, role remains conversation-start developerInstructions; fork new instructions remain ignored and fork no longer gets fresh environment context. These observations support shape/mechanism adoption only. The parent fixed-text hosted probe establishes model access, not role guidance/child-role enforcement/namespace support.

Receiving ROLE §5.2/§5.3 must deliberately pin new generated shapes while preserving additive agents.<ROLE>.description/config_file, exclusive byte-verified child configs with product guidance+child role, forbidden base/feature/policy overrides and supplied/adopted distinction. U-R3 per-thread config versus session-flags carrier remains with App implementation owner until actual chosen candidate proves it; adapter delegation was explicitly not rechecked at new pin. Real model multiAgentVersion, provider namespaceTools availability, fresh child role/config supply and inherited fork records require their own actual candidate evidence before claims; no inference from parent synthetic text. WD capability group mapping may retain unchanged generated names, but EXEC availability at 0.160 remains not-established until its owner adopts version-bound evidence. This content method change supplies neither provider qualification nor supplier carrier choice.

## Risks, authority and reserved matters

Method changes intentionally make old and new designations incomparable; preserve originals and do not mutate old registered revisions/A15s to create comparability. Exact bytes are sensitive to checkout conversions and OS filename spellings as RV3/4 require. Consumers need stable snapshots; mutable-tree races/copy drift remain WR's enforcement obligation. The prototype is method evidence, not product race resistance. Digest identity never implies accepted semantics, authorization, actual human act, one-effect or supplier/model adoption.

App technical choice is within the delegated owners' current promises, applied as proposed for fresh review; no scope/SoW amendment or human checkpoint created. RS receiving adoption must be reviewed independently rather than silently treated as complete. Host canonicalization/read/subject/change identity, one-effect, host carrier/storage and broader HOSTING U-08 remain with their owning external sessions. SUP1 carrier/provider evidence and method consumer checks remain manager execution work.

## Source origins / current input SHA-256

Root/role/loop inherited and already read; selective SoW identity clauses/Memory recovery, WD RV1–5/CR5–6/identity chain, WR ID/RB/LS8, EXEC TR4, ROLE CO/§6/U-R1, C §5/SoW REQ004/TBD003, RS OF3/HA10/L1–2/§13/U04 read. Current snapshots below may be followed by changes from their own active owners; this record does not pin those owners to stopping their work.

- `AGENTS.md` — `f96feb19d297c74e10048c506805b2fe3622c50cfefd6078f599724556113977`
- `agents/AGENT_TASK.md` — `1a13a5b00b3ce01ff8519efe6b46bcbe0cd6a5b7985e24282fa7efa2c57c8fb7`
- `projects/chirality-app-v4/loop/LOOP_INIT.md` — `45c23cf477e23aff1d0152189caf7e8ebfb53eca42e3a1fae87a06af8c197f28`
- `projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-03_Content-bound decisions and compact run records/Design/RECORD_SEMANTICS.md` — `e581c9bfc3474b7963a5afc043afb7ba47874fe17d633f0f1cd3ff1cacce1335`
- `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-02_Workflow-making workspace and registration/Design/WORKSPACE_AND_REGISTRATION.md` — `5ed5da8842b32b87ae68db3476192a55fc8ff151802684b10bdca16eaa8b8d8b`
- `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-03_Workflow execution compatibility and round-trip support/Design/EXECUTION_COMPATIBILITY.md` — `2e3a19b839e4645e9ff90dce0b9556e6c4fcb089b5f4dc1cb2605ae2436793c3`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-01_Stock Codex hosting and supplier contract/Design/VERSION_ADVANCE_0.160.0.md` — `0dee021d7dc425967b8cc6e867a970fd9397d63ff0f6d3c317e24fb900fad97a`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-01_Stock Codex hosting and supplier contract/Design/generated/0.160.0/COMPARISON.json` — `ca0ce6ca70503427dd44a4bf35d701d6a5dcf646323154bef605a585d1432227`
- `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-04_Additive role selection and supply/Design/role-supply-record.schema.json` — `eaa6e682aa6077f8ab89858e3f52d0e91d7117b5c03ea4c68c72ec0d95c5f639`
- `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-01_Portable workflow contract and shared allocation/ScopeOfWork.md` — `9479fc882decd3721a346ff5723751091db9965a65d6078baf6562ed1779bd49`
- `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-01_Portable workflow contract and shared allocation/MEMORY.md` — `0ebec31f096d87a6e388ff21c778146d03cc91548cac2e488c26c7792c76d6c0`
- `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-04_Additive role selection and supply/ScopeOfWork.md` — `2327508f2290e7cf2528950d65bc331d72a80d8413a13fe31ea8f867cce4d176`
- `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-04_Additive role selection and supply/MEMORY.md` — `40a3adf98b5e16c60b068e8384d8c48d9d913064d52e922f2ebb3d5785cc5d26`
- `projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-01_Capability catalog and read-basis contract/ScopeOfWork.md` — `48f0496c88b52a48aa86c606d3879b1bc09b9fd8631e765cf06ab02d168c1b6c`
- `projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-01_Capability catalog and read-basis contract/MEMORY.md` — `22dd02775d00fc630a702e965c16676807e25c2dce301e4f96f0b0b1229bcba7`

## Captured pre-edit identities

- `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-01_Portable workflow contract and shared allocation/Design/WORKFLOW_DECLARATION.md` — `262c9e5417cf67b56cf7c3678128ad406e8b4e2fda7057a07bebf04254ab2f31`
- `projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-01_Capability catalog and read-basis contract/Design/CATALOG_AND_READ_BASIS.md` — `0e3ba39cd926a2063fc93621c17ed39d1fc8622b2256f08005d1286e99795294`
- `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-04_Additive role selection and supply/Design/ROLE_SUPPLY.md` — `c8474d919bceec7d6b5b9dc328b03569b2c64f9d849ff950a2e33062cc1034cf`
- `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-01_Portable workflow contract and shared allocation/Design/prototype/wdproto.py` — `570269324bf2d487136b26b3501269dc722c2548a1492eda20f62d5d8fb300db`
- `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-04_Additive role selection and supply/Design/prototype/role_supply.py` — `9d333757aee088191450bcc214eb219c88ba41c08c58974dcfba2cc6c369ff5d`
- `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-01_Portable workflow contract and shared allocation/Design/workflow-declaration.schema.json` — `2982a1878dba563734ba754d5ca25e8872e761aca5e51f7c1377c6a5b5bc27c4`
- `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-01_Portable workflow contract and shared allocation/Design/prototype/README.md` — `4ed75405d199c05d908e2490393e6ec668e4ef6a8d3c1f5b5f9b7ab655775733`
- `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-04_Additive role selection and supply/Design/prototype/README.md` — `bcc0461af5da15b5b46dfbde20fe418305e5a5eb6f9736bb5b1137ab80cc3330`

## Candidate outputs / SHA-256 (record self-hash returned separately)

- `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-01_Portable workflow contract and shared allocation/Design/WORKFLOW_DECLARATION.md` — `a7a2ce85f573e4dd4a6a40de27080c6a5d8a55860b66a19ae26a34bf3ad51b1d`
- `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-01_Portable workflow contract and shared allocation/Design/workflow-declaration.schema.json` — `bb01a004e40da89e20183876774afc2308a921376eee4cf75e0c66fcdb405337`
- `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-01_Portable workflow contract and shared allocation/Design/prototype/wdproto.py` — `a1d626ddfe5cfcc3ee10a2065e5a601fd083d05e12dde003b27dcbc89b57cdbb`
- `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-01_Portable workflow contract and shared allocation/Design/prototype/content_identity_cases.py` — `7ab8f17386d71729343e262d69aea2a2e650906b8cc576f5ba54aa29cd3b2ddf`
- `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-01_Portable workflow contract and shared allocation/Design/prototype/README.md` — `7a967641fc7d108b25becf6f4cce9f1713ea3124098f636b892990f46cd918ed`
- `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-04_Additive role selection and supply/Design/ROLE_SUPPLY.md` — `eecdf63bb3cac94bc931605b55590512d44c4b6ff335c0670098c6308eac5ebe`
- `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-04_Additive role selection and supply/Design/prototype/role_supply.py` — `364fe4cd0b38a1867fd041f463d685b9c3df0674d92c813a5ae05311a302d54b`
- `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-04_Additive role selection and supply/Design/prototype/run_cases.py` — `a3983a62fc7feb9c3db2cbffd58b5e9a2a1e02ef77d511f8092a84ca954d837b`
- `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-04_Additive role selection and supply/Design/prototype/README.md` — `c808ca9c1d7ec4adac3fbd9c1ee2aeca7e73949f9d63f1ac553a0351b955f68d`
- `projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-01_Capability catalog and read-basis contract/Design/CATALOG_AND_READ_BASIS.md` — `4b5f43011eb276df923377cd0d79e0accaf65afba624814753c5612007412431`

## Citation repair R1

Original candidate association: record SHA-256 `ca6ba9e55d20339368f7f79bca6de168d0eb59b7e75af986a0729084fcd3a661`; C SHA-256 `510cfa73fc0ff9d2317ff91dfa59293cfb9582b6fcfae518e6479e6f09b20dce`. Reviewer/manager identified duplicate §5.4 headings: pre-existing relied-on/multi-read basis and new App-owned identity choice. Rename only the new App identity section to §5.5 and its new U-C1/record references; existing §5.4/P/read-basis/multi-read/staleness citations stay unchanged. No method/schema/algorithm semantics changed; no semantic test rerun required for this heading-only repair. Same reviewer backcheck remains required.
