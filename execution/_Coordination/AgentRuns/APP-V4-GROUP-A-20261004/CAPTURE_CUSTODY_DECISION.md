# Capture custody decision preparation — CI-10 / U-AAC-3

2026-10-04. **PROPOSED, for the human App implementation owner (DECISION-L L-7).** Prepared by read-only TASK `/root/group_a_execution/capture_custody_decision`, delegated-harness-native child of `/root/group_a_execution`; no descendants. Only this packet is writable. Reader/use: Root HELP_HUMAN presents the choice; WORKING_ITEMS, AAC/RS owners and later Group B consume the actual decision and its readiness conditions. This is neither a decision nor trustworthy replay evidence.

## Concrete finding and current boundary

V1-ACT ACT-1 shows an App path that turns matching schema-valid writable capture/pending files into a new direct-capture `human_act` without a native confirmation. The existing native-only allocation selects Rust hosting and native confirmation; it does not select a provenance seal. Valid JSON, matching bytes, a digest or `inputSource` text cannot establish origin.

Root's authorized CC-CUST-A/CC-CUST-R prerequisite clarification permits trusted hot-process retry with unchanged original capture, and add-once backlink repair to exactly one matching already durable RS entry. Cold unverified files remain visible, retained and held from new append. Existing-record repair upgrades no provenance. CI-10 / I3 therefore remains open for legitimate persistent replay. Keeping SEAL-1's honest unsigned-file limit cannot authorize a file-drop replay path or satisfy that remaining obligation. AAC §5.2a, NA-1/3/5, §6.3/6.4, RS HA-10 and R-7 all remain in force.

## Choices to put to the owner

| Choice | Concrete decision and consequence |
|---|---|
| **1 — Adopt SEAL-2, staged implementation and native qualification (recommended)** | Adopt a per-installation protected OS signing key available only to the admitted signed App, seals on capture evidence and every entry the App capture side writes, and the RS reader rule. Implement the contract and simulated/offline paths in A now. Hold real protected custody, trustworthy cold replay and native verification claims until the actual signed candidate and key-access proof. Preserve all native act kinds and relaunch requirements. |
| **2 — Keep SEAL-2 undecided and hold trustworthy cold replay** | Continue the authorized fail-closed repairs and independent work. Do not label persistent replay complete or treat SEAL-1 as a substitute. U-AAC-3 and I3 remain required owner decisions/work before completion. No new signing act is authorized. |

A permanent SEAL-1-only outcome would leave NA-5 and legitimate restart replay unfulfilled unless the owner separately amends their scope through the governing route. This packet does not recommend or enact that narrowing. An alternative custody design may be proposed, but must meet the same preserved obligations and receive its own owner review; no general service or external-host construction is needed or proposed here.

**Exact proposed decision text for choice 1:**

> I adopt SEAL-2 for App-native capture custody, with a protected per-installation OS signing key available only to the admitted signed App. The capture side seals the immutable captured facts, reseals the full capture after the add-once record backlink, and seals the entries it writes. DEL-04-03 adds its conditional seal format and reader rule: a missing, invalid or untrusted seal is shown as “capture not verifiable” and cannot authorize new automatic act replay. The person's identity remains unverified. Group A implements the reviewed contract, platform adapter and offline simulated-key tests now; actual key isolation, restart replay and portable verification remain unqualified until independently examined on the actual signed candidate. I permit the staged A sealing interface/code → B signed test build → A native/provenance tests → B final qualification route, preserving A's outstanding replay obligation until that backcheck passes. This decision does not authorize a download, use of credentials, signing, notarization, publication, distribution or release; those acts still require their actual point-of-use authorization.

Record the human's actual words and custody in OWNER_DECISIONS, separately from this proposed wording. Choice 1 is a concrete architecture and staging choice; signing identity and portability choices below remain visible prerequisites rather than invented approved values.

## Controls the reviewed implementation must define

- **Only native capture can invoke sealing.** No renderer, agent command, watched path or generic “sign this JSON” endpoint receives a signing operation. The host freezes authoritative offer/facts and signs only after the native event. Reading files never re-creates hot custody. A key handle alone proves no human act; NA-1/3 remain necessary.
- **Coverage and immutability.** Define a versioned, domain-separated byte rule for capture and entry seals, excluding only the seal itself; cover capture identity, full original facts, context/storage references and the entry header/body. The optional backlink is added once and resealed using the same admitted capture key, as AAC §5.2a requires. Preserve old complete evidence on failure; a stale seal never qualifies the changed object. Refuse mismatched identity/facts, conflict, incomplete history or uncertain durability rather than append another act. Do not treat cryptography as a fix for ACT-2…7.
- **Admission and replay.** Verify the persisted original capture against an admitted installation key and exact captured facts before a cold pending submission can mint/write its writer-owned ID. Distinguish missing key, invalid signature, unknown issuer, unsupported seal version and simulated issuer; each holds new automatic append and preserves bytes. Keep already recorded act/backlink status distinct from pending annotation. Native interruption cases still need evidence.
- **Reader and portable evidence.** Prefer asymmetric signatures so readers need no private signing key. Export only public verification material, its identity and independently grounded binding to the installation/signed App, plus the versioned byte rule and verification evidence. A public key stored beside writable files is not a trust anchor: another process could replace key and seal together. A portable verifier with only such self-supplied material must report “capture not verifiable”; a mathematical signature match alone cannot mean App origin. Define how a recipient obtains/trusts that binding before claiming portable verified provenance. Missing anchors must not prevent reading retained historical facts with explicit limits.
- **Lifecycle.** Name the actual Developer ID team, bundle identifier/designated requirement, key-store access group/entitlements/profile if needed, supported OS versions, locked/unavailable-key behavior, update continuity, reinstall/loss/rotation and historical verification policy. No guessed identity, shared signing service, silent key export, synchronizing secret or arbitrary fallback key. No per-act password/Touch ID requirement is added (L-5). No person's identity verification is added.

These are acceptance conditions for named reviewed AAC/RS seal changes, not finished code or a silently selected algorithm. A proposed asymmetric algorithm and macOS key-store access configuration must be frozen with their test vectors/API evidence before implementation claims. Other-platform verification or protected replay support remains an explicit scope/qualification choice; this macOS packet supplies no portable OS-key guarantee.

## Ordering and ownership — conditional GC-7 notice to Root

PKG I-4 explicitly supplies DEL-01-04 with the signed App identity, stable Developer ID team/bundle identifier and any SIGN-3 key-store entitlement. U-PKG-8 confirms that entitlement/profile at FP-2 of the actual candidate; PKG describes these as expected, not observed. Root clarification received through trusted parent relay after initial finding: **B/C loops may start once A contracts are agreed; there is no blanket A-completion-before-B-start gate.** This is orientation from Root, not a new human seal decision, signing authorization or gate acceptance.

Under that orientation the proposed bounded route is **A sealing interface/code → B signed test build → A native/provenance tests → B final qualification**. A retains its trustworthy persisted replay obligation and open I3 evidence throughout; B supplies the identified signed candidate/configuration and owns its final packaging qualification. No new deliverable cycle or group-order reversal is established by this staged route. The signed-output join has been notified to the parent as a conditional GC-7 concern. Escalate immediately if actual required inputs cannot be supplied in this staging, create a real cycle, or make a previously completed group's work wrong; do not resolve that by narrowing replay.

Record the relationship in A's work graph and carry it into B's graph when formed (GC-8). There is no active B graph found in this read. This packet does not change LOOP_INIT, silently reallocate an A obligation, or treat code readiness/simulated tests as qualified native origin. The owner decides custody now; native signing acts remain separately coordinated at their actual point of use.

| Point of need | Owner / readiness |
|---|---|
| Select custody and staging | Human App implementation owner, via Root; pending |
| Named seal contracts + RS minor format/R-7/R11 propagation | AAC and DEL-04-03 owners in A; pending choice, independent review required |
| Adapter and offline implementation | A implementation owner; no network/keychain/credentials required for simulation |
| Exact App signing identity/configuration and native acts | Human with B DEL-01-06; unknown identity, actual authorization and FP-2/native proof required |
| Signed candidate replay/custody negative controls and independent backcheck | A/B coordinated owners; open until exact candidate evidence |

## Offline feasibility and native evidence boundary

Read-only local cache inspection found current sha2 and dialog source, but no security-framework, keyring, ring, ed25519 or hmac crate source in the inspected registry. Cargo.toml presently has no signing/key-store dependency. SHA-256 hashing alone is no seal. The local macOS SDK Security headers expose `SecKeyCreateRandomKey`, `SecKeyCreateSignature`, `SecKeyVerifySignature`, `SecKeyCopyPublicKey`, key-access-group/data-protection-keychain attributes and code-validity checks. They support investigating a narrow macOS adapter without downloading a general key service. Their presence does **not** prove entitlement/profile admission, only-signed-App isolation, non-exportability or actual candidate behavior. Key access flags can request user presence; selecting them would reopen L-5 and is not proposed.

Offline tests can use an injected in-memory **SIMULATED / NOT OS-PROTECTED / NOT TRUSTED FOR PRODUCTION REPLAY** signer/verifier, outside production key selection. Fixtures must explicitly identify the simulated issuer; production admission refuses it. Test native-event gating, valid retained facts across a simulated restart, fabricated matching capture/pending files, signature/key substitution, changed facts/backlink, stale/absent seal, rotation/loss, duplicate/existing-record reconciliation and writer interruption ordering. Fixed signed-byte vectors test verification interoperability once an algorithm is selected; a mock signature only tests control logic. No test should claim signed-App custody.

Later native evidence must identify the signed binary/team/bundle/configuration and nonsecret public key binding; exercise a real native act, capture-before-write interruption/relaunch, exactly-once late record, unchanged binding after upgrade, refusal from an unsigned/differently signed process, unavailable key, and reader verification from the portable evidence set. Preserve exact observed errors and limits; do not export private keys. Signing/notarization/credential use and downloads remain unperformed here and require point-of-use human coordination.

## Supplied basis and execution limits

Resolved repository with git rev-parse; HEAD `cb5a88b29ac10fc0c09f9b6a44f497ab917e8a71`, shared dirty Group A work preserved. Read Root/TASK, App v4 LOOP_INIT, manual headings/Field Book and decision sections, current Group A graph, accepted grouping/GC-7/8, AAC §5.2a/§6.3/§6.4/U-AAC-3, RS HA-10/R-7/U-32, PKG SIGN-3/I-4/FP-2/U-PKG-8, ACT-1 review, L-7 and current owner/provider records. Initial discovery also consulted App v3 AGENTS/LOOP before identifying v4; these are inapplicable and no v3 rule is used as authority. No build, network, downloads, keychain access, signing, sign-in, credentials, Git mutation, code or sibling record edit occurred.

### Read source hashes (current bytes, not a frozen integrated candidate)

- `AGENTS.md` — `f96feb19d297c74e10048c506805b2fe3622c50cfefd6078f599724556113977`
- `agents/AGENT_TASK.md` — `1a13a5b00b3ce01ff8519efe6b46bcbe0cd6a5b7985e24282fa7efa2c57c8fb7`
- `projects/chirality-app-v4/loop/LOOP_INIT.md` — `45c23cf477e23aff1d0152189caf7e8ebfb53eca42e3a1fae87a06af8c197f28`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design/APP_ACT_CONTROL.md` — `098875a39b33543adc8ac1d860840e7e841062ea513cbd60a601ca237ceb721b`
- `projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-03_Content-bound decisions and compact run records/Design/RECORD_SEMANTICS.md` — `e581c9bfc3474b7963a5afc043afb7ba47874fe17d633f0f1cd3ff1cacce1335`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-06_macOS packaging and distribution evidence/Design/PACKAGING_AND_DISTRIBUTION.md` — `0d8d14d2ce08d859ec3b304f5c8c250afa7f0a6fe95eae3a61920f71d2a442b4`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/reviews/V1-ACT.md` — `1ac9f852f49b1e41e0e3502692d8df72dfc0818d3f6153b61dd8ded5a5595833`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/OWNER_DECISIONS.md` — `57e9412cbbc84862c2658a573ed9390a333ace8400c22bd6a81c8ce0eb77535a`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/provider/README.md` — `045dc875ffb2bb020d321e48b152f0256e705e7b83e185fcfd9b0d0257a339c3`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-DESIGN-PASS-3-20261001/OWNER_DECISIONS.md` — `8a5d11149045770dfcf1a19ebabb86bfe9f04cd3e65ed36166cb8593e2fe20ac`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GRAPH-CLOSURE-20261004/GROUPS.md` — `d96c399755fe2369cab96d29f73744834a98d70678f2f273f9ad01b0b129940f`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GRAPH-CLOSURE-20261004/GC_RULINGS.md` — `22187acaffb9a0e2c5ef6ed415cce0c62c6e6db06361405cf8caf642b5a59a92`
- `projects/chirality-app-v4/execution/_Coordination/WorkGraphs/APP-V4-GROUP-A-20261004/WORK_GRAPH.md` — `c44b21fcd66d44f37fcd5ac05832f452cc76a7e7e0cfd7601585885f1f44e41c`
- `docs/alignment-manual/README.md` — `31217d30b0d2743bef0d7c1a54bb9a81814d56b24ff0961cf01d9532952e305f`
- `docs/alignment-manual/CHIRALITY_AGENT_USER_MANUAL_v3.md` — `08ca0e40cd5157574a011bac57d539e77e9007a0d46494785da8b92745391b1a`
- `docs/alignment-manual/Project_Management_for_Human_Agent_Teams_Field_Book_v1.md` — `02d53a3966220001318aacf3f46e1b63b8695a098c81b20f4e3e1531b93024d3`
- `projects/chirality-app-dev/AGENTS.md` — `41995dfe123041e1d0235a73e532fddb913f2c2124a9e8ec43857a87d7e5822c`
- `projects/chirality-app-dev/loop/LOOP_INIT.md` — `8b975c10acf6c4394f5423d4def20aeb4583159c691e8d3d11a41ce7451e6a25`
- `projects/chirality-app-v4/app/src-tauri/Cargo.toml` — `2d89ee516e013d3e8990c15a2eaeebb1ce08588934a26193bfb93b604e4f7d31`
- `projects/chirality-app-v4/app/CONTRACT_ISSUES.md` — `b4a8d32e5af67c196cb938d82a74f65f59389812ca427ecce930ef3acc99b4a1`
