# Reconstruction reader method

- Contribution: DEL-09-11/RRM-v0.1 (first Design file of this deliverable; unit EP-11 of the early path)
- Status: DRAFT DEFINITION — proposed, not run on any candidate or host journey. An isolated reader has run once, on the early-path fixture (RR-E, §8); its account exposed two checker defects, repaired here.
- Run and owner: `APP-V4-DESIGN-PASS-4-20261003`, owner O-C, 2026-10-03.
- Serves: OUT-001 (how the week-later witness is performed), OUT-002 (the account format); REQ-001…REQ-005; AC-001…AC-005; VER-001…VER-005; VER-006's input and responsibility account (§9).
- **Pin basis.** Pin-independent (R23-3).
- **ScopeOfWork** `ScopeOfWork.md` sha256 e4ee1a5779af66fe085fefd12cf3b91dad2c8fdedcad6211ea613f2d188f09ae (INIT contract; no amendment changed any of its blocks). Read with R23-7. Its TBD-002 lists OI-001/002 as open; they are followed as D2/D3 rule them. REQ-002 predates the amended V4-HI-70, which adds "each network destination contacted"; this method traces destinations because V4-EXM-31 verifies V4-HI-70 as amended (§7). The wording goes to the next amendment (R23-11).
- **Rulings, cited by ID (R23-21):**
  - R23-10: the reader is any named reader separate from the run's author, person or agent; the record names the reader and the input set supplied; for an agent, its recorded supplied context shows the separation.
  - R23-6 as revised: "a week after" is kept as the basis writes it, with no calendar arithmetic. Its purpose is that the run's sessions and its author's working context are gone, so the test is whether the files and host receipts stand on their own.
  - R23-8 (decision packages); R23-19 and R23-20 (not-applicable parts; `blocked` and `not-run`).
- **Basis:** `docs/EXAMINATION.md` V4-EXM-31, §§1–2; `docs/PRD.md` V4-REC-01…05, V4-EXE-03, V4-PM-05; `docs/HOST_INTEGRATION.md` V4-HI-25, V4-HI-30…33, V4-HI-70 (as amended), V4-HI-71.
- **Suppliers.**
  - DEL-09-07's source-journey handoff: DOS-v0.1 §5, rules DJ-1…DJ-3 (`QUALIFICATION_DOSSIER.md` sha256 08430bb6e0029e755fdf13452d46b64aa46e98096ae1d38f4526506aa23c1659, LHQ-U2 as repaired for RV-LHQ-U2: the handoff now carries the input-set standing per item and withholds derived views (DJ-1)).
  - DEL-04-03 records: §3, §6, §7, §9 resolution status, §14.2 reader, R11, R15.
  - DEL-02-03 EXEC RP-6, inspection replay: "Rebuilds the same arrival identities and dispositions from the same record. It issues no request, dispatches nothing and records no act".
  - DEL-09-01 EXP records.
  - For the early path, the A16 rows (R23-18), adopted at O-A's E-1 refreeze (R23-21 item 3): RS-v0.10 `RECORD_SEMANTICS.md` 0d700f54d323682d439b1e44bc23dab52339873205604aa17a6c657c6e432ab2; ACT-POLICY-v0.10 `ACT_AND_POLICY_CONTRACT.md` d8e7449c7364609cc7dab435bcb745accdb31dee416d39a74c0ea4b98487f268 (with the §2.5 A16 row, R23-23 item 2); AAC-v0.3 `APP_ACT_CONTROL.md` 45b13f155a0c97949b60e0dfbe0c086fa5c9e9b1afcb0db1ef4f28f82a726057 (§5.1 names the offer digest's serialization, `aac-offer-digest/0.1`, answering the RR-E reader's unknown).
- **Fixture:** FX-DP1 (O-A). The RR-E reader was given its first freeze (`MANIFEST.sha256` e3c8c5ea…3b6f, superseded on disk at E-1; the supplied files themselves are verified below). Those nine supplied files are kept byte-identical in `prototype/fixtures/RR-E-input/`, verified against RR-E's `SUPPLIED.sha256`, and the RR-E evidence and the standing check run on them (R23-21 item 3). At E-1 O-A refroze FX-DP1 (`MANIFEST.sha256` 346191ff346ff788efec7aced9f46666fa46e5374dc288a85c69181bde928be9); only the offer and capture evidence changed, in `offerDigest` and key order. Against the refrozen files, the first input set's RC-1 correctly fails. For a future reader on the refrozen fixture there is a new input set, `IS-FX-DP1-2` (`prototype/fixtures/IS-FX-DP1-2.input-set.json`, sha256 e615aeeeaa1d5db3eaddab50179acae93714d56f40b126e08525a5bcd474156f; R23-23 item 4: RR-E's account stays valid evidence for `IS-FX-DP1-1`). It lists the new hashes and **carries the digest rule** as a `definition` item: `prototype/fixtures/definitions/aac-offer-digest-0.1.md`, a verbatim excerpt of AAC-v0.3 §5.1 that names its source and hash. Decision and reason: the RR-E reader could not reproduce `offerDigest` because no serialization was given. With the rule supplied, a reader can check the offer's integrity from the files alone, which is what the method tests. O-C confirmed that the rule recomputes the refrozen offer's digest (`c346f3ca…`) from the offer file alone. The assembler copies the fixture files and the definition into one folder for the reader.

## 1. What V4-EXM-31 asks

"A week after V4-EXM-20, someone reconstructs from the project's files what was asked, what the agent proposed, what the engineer accepted and what changed, with the host's receipts. *Verifies* V4-REC-01…05, V4-HI-70…71. Preserve what is unknown and the scope of any actual human act. Records of source resolution or transport success alone must not fill an unobserved provider/host outcome."

The method has three roles, kept apart:

| Role | Does | Is not |
|---|---|---|
| **Assembler** (DEL-09-11's App evidence examination owner) | Builds the input set from the source journey's handoff, arranges the reader, records the dates | The reader |
| **Reader** | Reads the input set only, and writes an account citing sources | A run author; the examiner |
| **Examiner** | Compares the account with the records, item by item, and writes the EXP result | The reader; the record's authority |

## 2. The reader and the evidence of separation (R23-10; REQ-001, VER-001)

| Reader | Separation evidence the record carries |
|---|---|
| A person | Name; absent from the source journey's run-author list (DEL-09-07 DOS §5); the person's statement that they took no part in the run |
| An agent | A fresh instance; its model identity; the **supplied-context record** written by whoever dispatched it: the brief, the input-set manifest and the files, each by sha256, and nothing else; the actual access limits of its host, stated as enforced or only instructed (V4-OPS-30) |

The reader is never in the run-author list. That list includes the person who acted, the host agent's session, the recorders, the dossier assembler and the examiner. For an agent reader, a supplied-context record that lists anything beyond the input set (a repository, a session store, a conversation) means separation is *not established*. VER-001 then records the witness as unfulfilled.

## 3. The input set (`rrm.input-set-manifest.schema.json`)

Built by the assembler from the source journey's handoff (DOS §5 for a V4-EXM-20 journey):

- **items**: each file by path and sha256, with its standing:
  - `record`: RS entries, act records, capture evidence;
  - `project_file`: files the run wrote, such as package files and findings;
  - `host_evidence`: host run records and receipts, by reference;
  - `definition`: how something in the set is computed or identified, copied from its repository source and naming it (`source` path and sha256) — for example the offer-digest rule, so that the reader can recompute a digest. A definition may support a check, never an act or an outcome;
  - `not_authority`: present, but never support for a claim; for example a conversation excerpt, kept only to test that the reader does not rely on it.
- **withheld**: the session and conversation identities, the author's working memory and derived views, named so that their absence can be shown and never supplied (REQ-004; DOS DJ-1).
- **source_journey**: its identity, run authors and dates.

## 4. Reading protocol and the account (`rrm.reconstruction-account.schema.json`)

| Step | Reader does | Rule |
|---|---|---|
| RD-0 | Checks every item's sha256 against the manifest | Any mismatch: stop, report; the witness is *blocked* (R23-20) |
| RD-1 | Reconstructs the **request** (what was asked; for a package, the act asked for, alternatives, consequences, requester) | Sources cited by path and locator |
| RD-2 | Reconstructs the **proposal** or package as the agent made it | As RD-1 |
| RD-3 | Reconstructs each **human act**: kind, actor, recorder, bound content, scope and purpose; for A16 the alternative chosen | Actor ≠ recorder; "identity not verified" kept where recorded (REQ-003) |
| RD-4 | Reconstructs **what changed**, by host receipts, hashes and origin marks, resolving each reference **at read** | An *unresolvable* reference stays unresolvable; a change with no receipt is not claimed (V4-HI-71; RS §9) |
| RD-5 | Checks **lapse**: is the act's bound content still current? | As RS §7; inspection time stated (EXEC RP-6) |
| RD-6 | Lists **unknowns** and anything read that is not authority | Never filled from likelihood, transport success or source resolution (V4-EXM-31) |

Each claim has a standing: `from_records`, `inferred` (stated as inference, with sources) or `unknown`. The schema refuses a sourced standing without sources, and refuses a decision or acceptance without both actor and recorder.

**Naming the subject (stated after RR-E).** `about` names the claim's subject by its identifier as it appears in the input set; for a decision package that is its `packageId`, its file path or its request record id. When `about` names no package, the package files among the claim's `sources` identify it. **Absences** are stated with `no_decision`, `no_change` or `no_outcome`. Both rules are in the brief (v0.2) and in the schema's descriptions. They add no required key: RR-E's account, written before them, still validates.

## 5. Examiner comparison (VER-002…VER-004)

The examiner derives the truth from the records, never from the account, and checks:

| Check | Holds when | VER |
|---|---|---|
| RC-1 | Every input-set item has its stated sha256 | VER-001 |
| RC-2 | The account names this input set (id and manifest sha256) | VER-001 |
| RC-3 | The reader is not a run author | VER-001 |
| RC-4 | Every cited source is in the input set | VER-002 |
| RC-5 | No claim rests on an item that is not authority | VER-004 |
| RC-6 | Every act-bearing item is reconstructed: each request, and its act or the recorded absence of one. Claims are assigned to a package by §4's subject rule | VER-002 |
| RC-7 | No claim contradicts the records: no fabricated, altered, upgraded or denied act. A decision claim must name the recorded actor and recorder (it may add detail, such as "identity not verified") and exactly the recorded alternative | VER-003 |
| RC-8 | Every reconstructed act keeps actor ≠ recorder | VER-003 |
| RC-9 | Nothing is claimed changed or achieved without its record; unknowns stay unknown. A `change` or `outcome` claim citing no change or outcome record is **referred to the examiner**, because a statement of absence written under those kinds cannot be told apart mechanically from an unsupported claim. The examiner's recorded judgment decides: *absence* holds, *unsupported* fails. With no judgment, the check is referred, never held, and the EXP outcome is `inconclusive` | VER-004 |
| RC-10 (host journey only) | Every change claim traces to a host receipt, hash or origin reference with its resolution at read; destinations contacted (V4-HI-70 as amended) are traced to the run record | VER-002 |

### 5.1 Standing check of the comparison itself (added after RR-E)

The examiner's checker had agreed with every account its owner had constructed, yet failed two checks on the first independent account (RR-E). Agreement with one's own fixtures establishes consistency, not soundness (coordinated-knowledge-work §3). So the comparison carries a standing check, `prototype/run_standing_check.py`, rerun after any change to the checker, the brief or the account schema:

- **SC-1:** at least one **independent** reader's account (now RR-E's, kept byte-identical as `prototype/fixtures/account.independent.RR-E.json`, sha256 637e234cdab95785698ab2f39275359a68e674dd9a9024fa7447cf25b3134cee) with its examiner judgments. Expected: no failure; and, without the judgment, only RC-9 referred.
- **SC-2:** mutations of that independent account that must fail:
  - an altered alternative;
  - a decision claimed on the pending package;
  - the decision filed under the wrong package;
  - the decision denied.
- **SC-3:** the owner's constructed accounts, with their expected verdicts.

If a later change to the brief or schema makes the independent account invalid, or makes its verdict depend on the change, a fresh independent reader is run on the same input set, and its account joins SC-1.

**Completed versus partial.**
- The witness (OUT-001) is **completed** only when an actual account by a separated reader passes RC-1…RC-9 (and RC-10 for a host journey) on the identified V4-EXM-20 record set, with the dates evidenced (§6).
- An account that preserves an unresolvable receipt as unresolvable passes RC-9. But a claimed change whose only receipt is unresolvable is not a *demonstrated* change. AC-002's "resolvable host receipt/hash/origin references supporting each claimed change" then fails for that change, and the result says so.
- Partial, failed, blocked, not-run and inconclusive results are recorded and do not complete the witness (REQ-004; R23-20).

## 6. Timing (R23-6 as revised; REQ-001, VER-001)

- The assembler records the **journey date** (from the source journey's records) and the **reconstruction date** (the reader's observed clock), each with its source.
- The examiner states whether V4-EXM-31's "a week after V4-EXM-20" holds, reading the two evidenced dates against the basis wording. This method adds no calendar arithmetic of its own.
- The examiner also records the purpose-test evidence:
  - the source run's run-ended record;
  - for an agent reader, a supplied-context record that holds none of the run's sessions;
  - for a person reader, their statement.
- A synthetic clock, a schedule or an immediate reread does not count (VER-001).
- The witness is scheduled so that it holds up no other work (R23-6).

## 7. On a V4-EXM-20 host journey (designed; not run)

The input set comes from DEL-09-07's handoff (DOS §5). For SWBPIPE as its answers stand (data, not commitments; host joins deferred):

- receipts are session-only (SQ-09 (c)), so every receipt reference reads *unresolvable* a week later;
- Apply records no person or time (SQ-01), so RD-3 has no actor from host evidence;
- there are no host run records (SQ-19).

RC-10 and AC-002 therefore cannot pass against SWBPIPE's current product (inference from those answers). This is a basis-level tension: V4-HI-71 and V4-REC-04 forbid copying receipts. It goes on the relay list when host joins resume (R23-14 item 3).

## 8. Rehearsal RR-E on the early path (FX-DP1)

**Case definition, declared before the run (R23-19).** RR-E rehearses §§2–5 on the decision fixture FX-DP1 (one decided package, one pending, and an agent message that falsely claims a decision). The timing part (§6) is declared **not applicable**, reason "a rehearsal of the reading method, not the week-later witness". RC-10 is declared not applicable, reason "no host journey in the fixture".

**Inputs** (`prototype/fixtures/`):

| File | sha256 |
|---|---|
| `IS-FX-DP1.input-set.json` (six items; the agent message as `not_authority`; three withheld identities) | f1174586ef7b2f4bac6ddb3c7ece7028ecc69b9a95b80f4721da9202cea4a63a |
| `READER_BRIEF.FX-DP1.md` (for an isolated reader; v0.2 after RR-E, v0.1 was 4bf425b9…26aa) | 9b7d6a0ee4d875e20a664db2396904beedfcb8df83ad856fc6da229f85979951 |
| `account.good.json` (constructed by O-C; **not** an isolated reader's account) | df6e58bbde6f5e4d8536450a3d12cd6195f2571806623d005a564f3749f4cbf8 |
| `account.bad1.json` (decision for PKG-2 taken from the agent message) | 6e1c76036ce6be6ef86d9e67bc7cd70e79c49a4f640dae3f71f0a8901afe5d9d |
| `account.bad2.json` (claims stage 2 started, from a consequence statement) | 5a187336856fe1ee0f531d64e4a34b2e72029db9babdcfe1c6852f36342a0a04 |
| `account.bad3.json` (the reader is a run author) | bd2e520e2f9b581e7cfd6c28aa1daafea612e36eab41c066b4bb1f3230ab447e |
| `account.bad4.json` (a decision claim with no sources) | ebcc12a0bba0f3a8752f99a7e4d443ca8c77a56f261f1709146cdecbbf8c5357 |

**RR-E: the isolated reader run.** HELP_HUMAN dispatched a fresh `type2-opus-high` reader with exactly nine files: the six input-set items, the manifest, the account schema and brief v0.1. The record is at `_Coordination/AgentRuns/APP-V4-DESIGN-PASS-4-20261003/E/RR-E/`; `DISPATCH_RECORD.md` sha256 8c9766bad901150f51471fbac1f5a8515be6a5a4c8ed42cf9bfd83596ba5b2e3. Enforcement limit, stated there: the host did not restrict the reader's reads; separation rests on the brief and the reader's report.

The reader's account (`account.json`, sha256 637e234cdab95785698ab2f39275359a68e674dd9a9024fa7447cf25b3134cee) is the evidence, and is kept unchanged:
- PKG-1 reconstructed: requested, then decided ALT-2 by Engineer A ("identity not verified"), recorded by the App interface;
- PKG-2 reconstructed as requested and undecided;
- the agent message read and given no weight;
- nine unknowns, among them that the `offerDigest` could not be reproduced (no serialization given; routed to O-A).

**The first comparison (checker before repair): 7 of 9 held.** Both failures were checker defects, not reader errors:
- **RC-6** matched claims only where `about` equalled the package path. That convention came from the owner's constructed accounts and was stated nowhere.
- **RC-9** treated every non-`unknown` `outcome` claim as a claim that something happened. Claim C-09 is a truthful statement of absence: the log holds three entries, seq 1–3, checked.

**Repairs:**
- the subject rule (§4), stated in brief v0.2 and the schema descriptions;
- RC-7's tolerance for added detail in actor and recorder, and its new denial check;
- RC-9's referral to the examiner;
- an added `no_outcome` absence kind;
- the standing check (§5.1).

None of these adds a required key, so the account still validates.

**After repair, on the same account** (`prototype/rrm_compare.py` sha256 80410be423f393452f5fdf2f1b7b0316b60220c1fc8d25614beb6ea9fd435a75; 2026-10-03):
- without a judgment: RC-1…RC-8 hold and RC-9 is **referred** (C-09); exit 2; EXP outcome `inconclusive`;
- with the examiner judgment `fixtures/judgments.independent.RR-E.json` (C-09 *absence*: HELP_HUMAN's judgment in RR-E `RESULT.md`, confirmed by O-C against the log; sha256 f0464d057b3151bc7d856396ede55ecd4be1a55ccf5b4d42765ace11a4f3b777): **9 of 9 hold**; exit 0;
- each run writes a schema-valid EXP rehearsal record against the EXP result schema present at the time (sha256 f7871c96cef25bb974aea73feca009ed3caf843db5077d80612f13b130af2081).

**Standing check** `prototype/run_standing_check.py` (sha256 f480aaf7dc74ee81ba05754b64b4d71f5a31a4fb95eede80165f248e74d45ef0): **12 cases, 0 unexpected.**
- SC-1: the independent account, with and without the judgment.
- SC-2: four mutations of it, each failing as expected.
- SC-3: the five constructed accounts (with the `bad2` judgment `fixtures/judgments.bad2.json`).

The account schema (sha256 26d0d2e08e06c8cf74cccd537474e096e17848bf0a3c06b10b0486e29341791e) passes `check_schema`, and all accounts but `bad4` validate against it.

**The early path's consumption check, as it now stands.** The records of FX-DP1 are usable by an independent reader from the files alone. The reader's content is right on both packages, and the repaired comparison holds on its account, with the examiner's judgment recorded for one referred absence claim. Still to do: rerun on O-A's refrozen E-1 records (R23-21).

## 9. Failure behaviour and responsibility (VER-006)

| # | What fails | Record left | Next |
|---|---|---|---|
| RF-1 | An input item's hash differs | Reader's report at RD-0 | Witness *blocked*; the assembler re-forms the set |
| RF-2 | A source journey input is missing (no journey, no handoff) | EXP *not-run*, missing input with supplier (DEL-09-07; SWBPIPE) | Returned to the App evidence examination owner (VER-006) |
| RF-3 | The separation evidence is absent | EXP *inconclusive* | Re-run with a separated reader |
| RF-4 | A reference cannot be resolved at read | The account keeps it *unresolvable* | RC-9 holds; AC-002 fails for the change it supports (§5) |
| RF-5 | The dates are not evidenced | EXP *inconclusive* | Witness unfulfilled (VER-001) |

**Excluded acts (REQ-006).**
- The record format is DEL-04-03's.
- The source journey is DEL-09-07's.
- Host receipts are SWBPIPE's.
- The acts themselves are the person's.
- Open policy belongs to its owners.

This method performs none of these. It examines and faithfully records.

## UNRESOLVED

| Item | Owner | Point of need |
|---|---|---|
| `offerDigest` serialization (the RR-E reader's unknown) | O-A (AAC/RS) | Before a reader can verify an offer digest |
| A16 rows refrozen (E-1) | O-A | Before the rehearsal is rerun on the refrozen records |
| The source V4-EXM-20 journey and its receipts | DEL-09-07; SWBPIPE (host joins deferred) | Before OUT-001 |
| Durable receipts (SQ-09 (c)) | SWBPIPE owner; next relay list | Before AC-002 can pass on SWBPIPE |
| REQ-002 wording on destinations (amended V4-HI-70) | Next amendment (R23-11) | — |
