# RV-E1 — review of E-1, the early path (owner O-A): one decision package decided by the person

- **Reviewer and method.** RV (Type 2 TASK, Claude Opus 5.5), run `APP-V4-DESIGN-PASS-4-20261003`, 2026-10-03. Method: `coordinated-knowledge-work` §3.
- **Basis.** Rulings R23-2, R23-8, R23-9, R23-18, R23-21, R23-22 and R23-23 (cited by ID; R23 file now `7772dd3e…`). O-A's record is `OWNERS/O-A.md`: the E-1 refreeze, the offer-digest addendum and the R23-23 follow-ups.
- **Reviewed bytes.** Every hash below was recomputed with `shasum -a 256`:

| File | sha256 reviewed |
|---|---|
| DEL-04-01 `ACT_AND_POLICY_CONTRACT.md` (ACT-POLICY-v0.10, with the R23-23 §2.5 row) | `d8e7449c7364609cc7dab435bcb745accdb31dee416d39a74c0ea4b98487f268` |
| DEL-02-03 `EXECUTION_COMPATIBILITY.md` (L3 only, R23-23) | `202a0f8f997b0cb8e0ba21f03eac8c6e69e62cc1963b81d038915db644c4865a` |
| DEL-04-03 `RECORD_SEMANTICS.md` (RS-v0.10), `RS_RECORD.schema.json`, `.invalid.examples.json`, `.valid.act-log.example.jsonl` | `0d700f54…`, `44331659…`, `0eca6b27…`, `b34997bb…` (all as O-A lists) |
| DEL-02-03 `checkpoint-record-entries.schema.json` (proposed-0.7), `.example.invalid.json`, `.example.decision-package.valid.json`, `prototype/run_all.py`, `prototype/README.md` | `e56d33dc…`, `25b8d913…`, `2404eead…`, `2fc3605a…`, `6407bf4c…` |
| DEL-01-04 `APP_ACT_CONTROL.md` (AAC-v0.3) | `45b13f155a0c97949b60e0dfbe0c086fa5c9e9b1afcb0db1ef4f28f82a726057` |
| DEL-01-04 `aac.offer.schema.json`, `aac.capture-evidence.schema.json` | `662083f8…`, `54af3401…` |
| DEL-01-04 AAC examples (offer valid/invalid; capture valid/invalid) | `f595c2dd…`, `94667c14…`, `f6bf269f…`, `ddcd74dd…` |
| DEL-01-04 `NATIVE_INTERACTION_RECEIVING.md` (NIR-v0.3) | `aca40c0e…` |
| DEL-06-02 `DECISION_VIEW.md` (DV-v0.1) | `f4aa6206…` |
| `E/run_e.py`, `E/proposed_rows.json`, `E/make_fixture.py`, `E/decision_view.py` | `11ccd319…`, `9b58806a…`, `804c81c4…`, `f0f838a1…` |
| FX-DP1 `MANIFEST.sha256` | `346191ff…`; every file passes `shasum -a 256 -c` |
| `E/README.md` | `e4381c20…`, which O-A.md does not list (E1-R6) |

## Verdict: **REPAIR**

There is 1 MAJOR finding, 3 MINOR and 4 NOTE, and no BLOCKING finding.

The path works end to end. Its schema rows are additive, and A16 is coherent everywhere except the stale citations in E1-R2. Only one thing stops READY: the first artifact on the path, the package file the agent writes, has no defined shape. It does not match R23-18 item 3, and O-A's claim says it does.

## Findings

### E1-R1 — MAJOR — the package file is not the CE-4 body, and no shape is defined for it (R23-18 item 3; O-A claim "The package file is the CE-4 body with form 'decision package file'"; DECISION_VIEW §7; RS §13.6)

- **The ruling and the claims.**
  - R23-18 item 3: "The package file is the CE-4 request body with PR-2's `form` value; no second shape."
  - O-A.md, DECISION_VIEW §7 ("the package file the agent writes is that body (R23-18 item 3)") and RS §13.6 ("the package file is that body") all state that this holds.
- **What the fixture shows.**
  - `FX-DP1/project/decisions/PKG-1.json` has the keys `actKind, alternatives, consequences, packageId, purpose, scope, subject`.
  - Its `act_request` body (`rec:app:coord:0001`) has `actKind, alternatives, association, consequences, evidence, form, purpose, requester, scope, subject, time`.
  - I validated the file against CE-4 `actRequest` (`jsonschema`, `$ref` to `#/$defs/actRequest`) and it fails: `packageId` is unexpected, and `requester`, `form`, `association`, `evidence` and `time` are required but missing.
  - `make_fixture.py` L39 writes `packageId` into the file.
- **Inference.** The ruling cannot be met literally. CE-4's `evidence` names the package file by its own content identity (`claimedIdentity` `sha256:cf885b17…`, which matches the file's bytes), so a file that contained its own body would have to contain its own hash.
- **Consequence.** The path starts with an agent writing a package file, and nothing defines what that file must contain:
  - which elements the agent writes;
  - which ones the App writer adds (requester, form, association, evidence, time);
  - what `packageId` is.

  The decision view, the act control's offer (AI-9) and DEL-09-11's reader all depend on that file. This reopens an interface, so it is not at the 60% level.
- **Route.** This needs a ruling first, because R23-18 item 3 is itself unsatisfiable. It goes to HELP_HUMAN.
- **Suggested shape of the repair.** Define the package file as the CE-4 body without the writer-supplied elements, plus `packageId` (or with `packageId` dropped), and add a `$def` for it in DEL-02-03's schema 0.7 or in RS. State the mapping from file to `act_request`, and add a valid and an invalid example. Then correct the three claims.

### E1-R2 — MINOR — ACT's A16 row cites the versions without A16 (ACT §2.1 L342)

- **Evidence.** The ACT A16 row says "Capture evidence from **DEL-01-04's App act control** (AAC-v0.2 §1.2) … recorded per RS-v0.9 §6.1 under HA-1". AAC-v0.2 (`062ce28c…`, HEAD) has no A16 row; it arrives in AAC-v0.3. RS-v0.9 has no A16 rows and no HA-11; both arrive in RS-v0.10.
- **What is already right.** ACT §2.5's new A16 row correctly cites "RS-v0.10 §6.1, HA-11", and RS HA-11 correctly cites "AAC-v0.3 §1.2".
- **Repair.**
  - Cite AAC-v0.3 §1.2 and RS-v0.10 §6.1, HA-11.
  - In ACT §4.1, also name A16 beside A15 as outside the closed list, since the A16 row points there.

### E1-R3 — MINOR — the EXEC status line was garbled by the R23-23 correction (`EXECUTION_COMPATIBILITY.md` L3)

- **Evidence.** The new line reads: "`checkpoint-record-entries.schema.json`, schema 0.7 since pass 4: …; this document's text is otherwise EXEC-v0.7 as before, R23-23), which under R14-1 defines the **bodies** …". The parenthesis now closes before the clause that describes the schema, so "which … defines the bodies" appears to refer to the whole list.
- **Reliance.** `git diff HEAD` shows L3 is the only line that changed. The pins of `69e6e79a…` (GUIDE, VERSION_ADVANCE, DEL-09-02, DEL-09-07 LHQ) rely on EXEC's sections, not on L3, so their reliance is untouched (R23-21 item 3).
- **Repair.** Reword the line. Also say whether the bytes change without a new label conforms to R23-21 item 2. I read R23-23 item 2 as authorising an in-place correction.

### E1-R4 — MINOR — the offer-digest method leaves two cases unspecified (AAC-v0.3 §5.1, `aac-offer-digest/0.1`)

- **What holds.** The digest recomputes from the offer file alone, independently of the prototype. I removed `offerDigest`, applied `json.dumps(sort_keys=True, separators=(",",":"), ensure_ascii=False)`, encoded the result as UTF-8 and took sha-256. The result is `c346f3ca…febff3e`, equal to the value in the offer and in the capture.
- **What the stated rules do not fix.**
  - **Numbers.** How numbers are serialized is not stated. The present offers contain only strings and booleans; a number such as `1.0` versus `1` would diverge across implementations.
  - **Characters outside ASCII.** Characters written "as themselves, not `\u` escapes" are untested, because the fixture holds no non-ASCII text. Implementations also differ on U+2028 and U+2029.
- **Repair.** State number serialization, or forbid numbers in the digested offer. Add one non-ASCII case to the AAC examples.

### E1-R5 — NOTE — A16 cannot satisfy a D2-reserved act, though actClass is not bound per kind

- **Where it is enforced.**
  - CE `actCounted.actKind` and checkpoint `requiredAct` are `A4, A5, A6, A7, A12` (schema 0.7), so an A16 cannot count at any checkpoint.
  - ACT §4.1's list is closed.
  - The ACT A16 row and RS HA-11 say a package naming another kind is decided by that kind.
  - DV-4 (`decision_view.py`) refuses an act whose kind differs from the package's, in both directions: RV-5 and RV-6 pass.
- **The residue.** RS's schema accepts an A16 `human_act` whose `actClass` is "reserved to the person", and an A4 whose `actClass` is "person's act (V4-PM-04)". My probe used DEL-04-03's own `minischema` registry. This predates the unit: an A15 with "reserved to the person" is also accepted. So it is not a relaxation introduced here, but binding `actClass` per kind would close it.
- **Not enforceable by schema.** Whether a "coordination decision" is in fact reserved rests on the cited instrument (ACT A16 row). That is correctly left to the package's cited workflow or instrument.

### E1-R6 — NOTE — record keeping

- `E/README.md` is `e4381c20…`. O-A.md lists `82e3fe38…`, and the R23-23 section names no new hash.
- O-A.md's refreeze table still lists ACT at `b45cd113…`. The R23-23 section supersedes it with `d8e7449c…`. A reader of the table alone would pin the wrong bytes.

### E1-R7 — NOTE — re-deciding one package

DV-6 shows the latest A16 in written order. Neither ACT nor RS says whether a second A16 on the same unchanged package is a correction (RS OF-5), a new decision, or not allowed.

### E1-R8 — NOTE — RR-E remains valid for its input set

- RR-E's account (`637e234c…`) read the previous offer and capture bytes (`92d49511…` and `cc66321d…`, in `SUPPLIED.sha256`). Under R23-23 item 4 it stays evidence for IS-FX-DP1-1.
- The reader's digest gap is now closed by AAC-v0.3 §5.1, and the recomputation above confirms the fix.
- RC-6 and RC-9 are defects in O-C's checker and are routed to O-C. They are not part of E-1.

## Claims checked

| Claim | Result | How |
|---|---|---|
| Every change is additive; none narrows or relaxes a check | **Holds** | `git diff HEAD` on RS, ACT, AAC, NIR, the EXEC schema and its examples: only new enum values, new properties and new rules guarded by A16 or by new properties. The prose rows only append A16 (word diff). HEAD's own examples under the new schemas (`jsonschema`): AAC offer HEAD valid 3/3 still valid and HEAD invalid 16/16 still rejected; capture 2/2 and 12/12; EXEC `example.valid` 12/12 valid and `example.invalid` 7/7 still rejected. RS: `run_prototype.py` 67 PASS ("all expectations held"), with the earlier valid logs and INV-RS-1…24 included |
| PR-5's rewritten form means the same as the stated allOf/not | **Holds** | `form` is required in `actRequest` and enumerated, so "not const 'decision package file'" equals the enum of the other five forms, and `alternatives: false` equals "not required". Mechanical check: I substituted the stated `anyOf`+`not` form from `proposed_rows.json` into a copy of the schema and compared it with the file's form over 96 instances (form ∈ six values plus another value plus absent; alternatives absent, two, one or empty; consequences absent, one or empty). There were 0 disagreements. One coupling to note: PR-5's second branch repeats the form enum, so a future form value must be added in both places |
| A16 coherent across ACT, RS, AAC and CE-4/CE-10 | **Holds, except E1-R1 (file shape) and E1-R2 (citations)** | Actor is the person (ACT §2.1; RS §6.1 decisionActor; AAC §1.2). Subject is one package plus the alternative chosen (ACT §2.1, §2.5; RS §6.1 bound subject and content; AAC offer `subject`, `requestRef`, `alternatives`; capture `alternativeChosen`). Evidence is AAC capture under HA-1 and HA-11. There is no act-declined event: ACT §2.1, RS HA-11, AAC offer `declineAvailable: false`, INV-E-5/6 and INV-RS-28 agree. CE-10 `actRef` carries A16 and run_e's A16 `act_lapsed` is valid. "decide" is A16's wording only (AAC rule 3; ACT §9). D2: E1-R5 |
| Decision view derives only from records and package files and writes nothing | **Holds** | `decision_view.py` read in full: it only opens files for reading, its inputs are the RS log and the package files the requests cite, and conversation text is never read. run_e D: "input set unchanged by every derivation (7 files, hashes equal)". DECISION_VIEW §2 excludes conversation, native status and PEC (SETTLED by CAP-7, HA-1) |
| NIR's `Turn.error` wording holds at both pins | **Holds against the VC record** | NIR §5.1 quotes 0.158.0 "Only populated when the Turn's status is failed" and 0.160.0 "Error associated with a failed or interrupted turn", which equal `VERSION_ADVANCE_0.160.0.md` Δ3 (L59). TO-4 keeps an interrupted turn interrupted, with "Codex reported: ‹message›" and never "Failed", which follows VC's recommendation (L156). I did not regenerate the protocol types (no network); I relied on VC's record |
| The offer digest recomputes from the offer file alone | **Holds** (E1-R4 for the unstated cases) | Independent recomputation, described above |

## Prototypes rerun (not rebuilt)

| Prototype | Result |
|---|---|
| DEL-04-03 `run_prototype.py` | 67 PASS, "RESULT: all expectations held" |
| DEL-02-03 `run_all.py` | 118 ok, "ALL CHECKS HOLD: 0 failure(s)" |
| DEL-01-04 `run_cases.py` | "159 checks, 0 failed" |
| DEL-04-01 `validate_policy.py` | 6 PASS, all held |
| `E/run_e.py` | "all expectations held (47/47)" |
| FX-DP1 `shasum -a 256 -c MANIFEST.sha256` | 6/6 OK |

Scratch probes are under `$TMPDIR/rv` (`additive.py`, `rs_probe.py`). Nothing was written in the unit.

## Not checked

- E-2 (DEL-06-01), which is not in this unit.
- Regeneration of the Codex protocol types at either pin.
- AAC §5.1's claim that the method is not RFC 8785, which is stated as unchecked.
- O-A's list of pins on the old hashes (R23-21 item 4), beyond spot checks: ACT and RS `4ef8c042…` and `a91882e7…` in DEL-09-07, and AAC `062ce28c…` in DEL-09-01, are correct.

## Repair confirmation (2026-10-03)

- **Basis.** R23-24 (supersedes R23-18 item 3) and R23-25.
- **Bytes reviewed.** Every file in the CURRENT table of `OWNERS/O-A.md`, recomputed with `shasum -a 256`; all match. Among them:
  - ACT `1bf0ce8e…25c1`, RS `75a32e55…b234`, EXEC schema `a5271857…b45c`, EXEC `EXECUTION_COMPATIBILITY.md` `3add943d…eb84`;
  - AAC `de39976e…cf65`, DECISION_VIEW `b944b0be…206d`;
  - `E/run_e.py` `81c973de…9774`, `E/decision_view.py` `6fae1738…d65b`;
  - FX-DP1 manifest `9501ef81b94c24b71a00c3611cbfa5b8eed2214eb575208283be4c3b46f034c5`.
- **Additivity.** HEAD is now the coordinator's WIP checkpoint `09ca67d094`, which already contains E-1, so I re-ran the additivity check against the pre-pass base `cec590c5c3`. At that base, the examples that were valid and invalid are still valid and invalid under the current EXEC and AAC schemas. The EXEC schema diff from that base removes nothing except the replaced enum tails and the `$id` and description lines.

### Verdict: **CONFIRMED — READY**. E-1 has no open BLOCKING, MAJOR or MINOR finding.

| Finding | Status | Confirmed against (actual files) |
|---|---|---|
| **E1-R1 MAJOR (R23-24)** | **Repaired** | DEL-02-03 schema `$defs/decisionPackageFile`: `additionalProperties: false`. It requires format `chirality.decision-package`, formatVersion, packageId (`pkg:…`, "never a hash of the file"), actKind, subject, purpose, `reservedBy` and alternatives, each with one or more consequences. It has no recorder element and no self-hash. Its examples: the valid one validates, and INV-PKG-1…6 are rejected, including "the act_request body offered as the file". **FX-DP1:** PKG-1.json and PKG-2.json validate as package files. Each `act_request` validates as CE-4, and its `evidence.claimedIdentity` equals the sha-256 of the file. Each request equals a mapping I wrote from RS §13.6's text, not imported from O-A: actKind, subject, purpose, scope, alternatives {id, statement} in order, and consequences one per statement, with the recorder adding only requester, form, association, time and evidence; packageId and reservedBy are not copied. `request_from_file` (EXEC `run_all.py` L334) implements the same mapping. RS §13.6 (L1198–1226), DECISION_VIEW (basis line, §1, §7, §9) and the EXEC schema description cite R23-24 |
| E1-R2 MINOR | **Repaired** | ACT A16 row (L342) now cites AAC-v0.3 §1.2, RS-v0.10 §6.1, HA-1 and HA-11, and the package shape. §4.1 (L795–797) names A16 outside the closed list |
| E1-R3 MINOR | **Repaired** | EXEC L3 is split into separate sentences. It says the line was corrected in place under R23-23 item 2 without a new label |
| E1-R4 MINOR | **Repaired** | AAC §5.1 (L240–273) now states object order, separators, string escapes (short forms, `\u00xx` lowercase, everything else as itself including U+007F and U+2028/2029), integers only, literals, and that the method is undefined on non-integers. The offer schema has no `"type": "number"` and one integer. I wrote my own serializer from the §5.1 text: FX-DP1's offer (with U+00FC ü, U+2248 ≈ and U+2028) gives `f0d82571…`, which equals the offer and the capture. AAC's A16 example also matches. Python `json.dumps(sort_keys, (",",":"), ensure_ascii=False)` produces the same bytes |
| E1-R5 NOTE | Unchanged, as agreed | actClass is not bound per kind. This predates the unit |
| E1-R6 NOTE | **Adopted** | O-A.md has a CURRENT section that marks the older tables as history |
| E1-R7 NOTE (R23-25) | **Decided and coherent** | Stated consistently: a later A16 on the same package is a new decision that supersedes the earlier for current standing, both stay recorded, and a correction (RS OF-5, `corrects`) is not a new decision. Where it is stated: ACT §2.1 A16 row (L342) and §2.5 (L451, "on the same unchanged package"); RS HA-11 (L599–602); DV-6 (DECISION_VIEW L82–90); FR RF-6 (FLEET_RECORDS L217–221). Implemented in `E/decision_view.py` L108–139 and `fleet_store.py` `_decision_state`: corrected entries are dropped, then the latest holds. run_e RV-8 and RV-9 pass. RS's `corrects` element exists in the schema |
| E1-R8 NOTE | No action needed | — |

**Note (not a finding).** RS §7 L-0, cited as the model ("as L-0 for A12"), still names only A12, A13 and A15. The A16 rule lives in HA-11. A one-line cross-reference in L-0 would help a reader who starts from §7.

**Checks rerun (not rebuilt), on the files as they are:**

| Check | Result |
|---|---|
| DEL-04-03 `run_prototype.py` | 67 PASS, "all expectations held" |
| DEL-02-03 `run_all.py` | 126 ok, "ALL CHECKS HOLD: 0 failure(s)" |
| DEL-01-04 `run_cases.py` | "159 checks, 0 failed" |
| DEL-04-01 `validate_policy.py` | all held |
| `E/run_e.py` | "all expectations held (56/56)" |
| FX-DP1 `shasum -a 256 -c` | 6/6 OK |

**Consequence for O-C's EP units (`reviews/RV-EP.md`).** EP-R4 can now be repaired against `reservedBy` in the package file. FW-04 and RRM rerun on manifest `9501ef81…`.
