# SCC-CASE-005 — pair analysis of SCC-004 (DEL-07-01, DEL-07-02, DEL-08-01), 2026-10-04

- **Standing.** This is a case evidence update under `workflows/scc-resolution-case`. It is evidence for the owner's checkpoint, not a ruling.
  - Nothing is changed by this file: no row, register, ScopeOfWork, Design file, DAG version or existing case file.
  - Every move below is a **proposal**. Cut and merge are the owner's (`docs/CYCLE_DRIVEN_RESOLUTION.md` §2 rule 3).
  - Any ScopeOfWork wording is applied by `scope-of-work` under an amendment the owner accepts.
  - CaseState stays EVIDENCE_ACCUMULATING. The CP1-20260928 ruling (basis and tracking only) carries forward unchanged.
- **Run.** `APP-V4-GRAPH-CLOSURE-20261004`, case work under `CASE_BRIEF_COMMON.md` (sha256 `c83e0f86ca55c26ddc6abd2cfa817256fd6ed42f6013a926b72016825c703468`, committed at `b459b4f2d1`).
  - Author: O-D, a Type 2 TASK agent (Claude Opus 5.5) dispatched by HELP_HUMAN. It does not delegate.
  - O-D is also the design agent of all three members' Design files (CFB, PRC, DRC). The rewordings proposed here are therefore O-D's to make, under review, once the owner's checkpoint allows them.
  - Branch `claude/app-v4-graph-closure`, HEAD `c6c1fd74b2`, clean tree. Read-only git.
- **Paths.** `E/` is `projects/chirality-app-v4/execution/`. "Pair A" is DEL-07-01 ↔ DEL-07-02 and "pair B" is DEL-07-02 ↔ DEL-08-01, the two 2-cycles G1 r3 §2.4 names.

## 0. Basis and checks

| File | sha256 |
|---|---|
| `E/_DAG/DAG-004/CandidateEdges.csv` | `2bfff10e3094d7fd86da563006c965694563ec10d0fc78e9b1d9958fefa42025` |
| `E/_DAG/DAG-004/DependencyEdges.csv` | `c43033742df768a6fb493701d25b1d73240366172c05b1d0caa143650690966e` |
| `E/_DAG/DAG-004/ExcludedRows.csv` | `45f55e76ecf7c9aac3bd923838eee8c302d6b2776e4fa3c221e51f9cf465664e` |
| `docs/CYCLE_DRIVEN_RESOLUTION.md` | `bbd41a8d091c7fa81fce6462c1d5e976832e5879b6ab8c3c74147e2df55e514f` |
| `…/APP-V4-GRAPH-CLOSURE-20261004/SURVEY/G1.md` (r3) | `3d6543bc2a05e5e62cb9673c1d3177386f484de38d9058a0b396eee9299f0a45` |
| `…/APP-V4-GRAPH-CLOSURE-20261004/GC_RULINGS.md` (GC-1…GC-4) | `27265cc9245fd7c2d93096dd8f2978376b51c48daf0e77fc110ced4c7c3318dc` |
| `…/APP-V4-GRAPH-CLOSURE-20261004/reviews/RVG-G1.md` | `0dd4ae6dd491c9183736c7b3b3ecdb5124f42a73618ec7607ee82fe4e06f8257` |
| Method example: `E/_DAG/cases/SCC-CASE-002/PAIR_ANALYSIS_2026-10-04.md`, `MOVES_PROPOSED_2026-10-04.csv` | `ad196971250aacb14f1eb5b8381549014615e23f606b06b96a7c8c44588f8250`, `c9bd426b90c2b54426c3321c673bfbfe1016596a484dcb2af2eec7187bba31c9` |
| DEL-07-01 ScopeOfWork | `5e2fba1d2191d97832a3f09feeb91f4f4231775a6a99b2b6c769a54c43edc5e3` |
| DEL-07-02 ScopeOfWork | `6b618f9a0300794b8edd4c6f2fb3e50a9d51f3647c446abc668755a25cd12151` |
| DEL-08-01 ScopeOfWork | `df2795869011f9364d5acf7541d66e2c32ffdd382c757153ad8d1fe8492607d7` |
| DEL-07-02 `Design/CONNECTOR_FALLBACK.md` (CFB-v0.2) | `69c1f10eb1ed0ecb65dbf75844d3d47daaae0842697f0e41c51b072c41353f16` |
| DEL-07-01 `Design/PEC_RECEIVING.md` (PRC-v0.4) | `4abb2c05736ee7cb7f6e67cb387bda7d6aaf3e27348bd0f319765d5e5c433c3e` |
| DEL-08-01 `Design/DOMAINS_RECEIVING.md` (DRC-v0.1) | `7bfa7fc496667652340573e7b50bc3fe94edfc4490e8b83d29a1feea2b558243` |

All Design files above are "PROPOSED" and none is accepted.

**Checks run.** The scripts are scratch files under `$TMPDIR` (`scc004_fid.py`, `scc004_close.py`), not in the repository.

| Check | Result |
|---|---|
| Arcs | DAG-004 has exactly 4 held arcs among the three members: DEL-07-01 → DEL-07-02 (DEP-07-01-014), DEL-07-02 → DEL-07-01 (DEP-07-02-010), DEL-07-02 → DEL-08-01 (DEP-07-02-011), DEL-08-01 → DEL-07-02 (DEP-08-01-009). This matches G1 r3 §2.4 |
| Mirror and same-arc rows | From `ExcludedRows.csv` `RepresentedBy`: DEP-07-02-014 mirrors DEP-07-01-014; DEP-07-01-015 (MIRROR) and DEP-07-02-012 (SAME_ARC) ride on DEP-07-02-010; DEP-08-01-010 mirrors DEP-07-02-011 |
| Live fidelity | All 8 rows are ACTIVE. Each `EvidenceQuote` occurs in its register's ScopeOfWork (whitespace, `` ` `` and `*` normalised) |
| Baseline | With every arc kept, Tarjan over the whole DAG-004 graph (both layers) gives SCC-004 = the 3 members, and an exact minimum feedback arc set of 2 under O-1…O-4. This reproduces G1 r3. No path through a non-member returns into the component, so arcs outside it cannot change its closure |
| Closure with moves | §5, by the same script |

**Kinds.** G1 r3 throughout. RVG's G1 review settled that DEP-07-02-010 and DEP-07-02-011 are both I (G1-M2). All four cycle-forming rows are I.

**Quotes.** Quotes are verbatim from the file named. `…` marks an omission inside a quoted sentence.

## 1. How each pair is decided

The question and the discriminator are those of SCC-CASE-002 §1:
- **The question.** Does B's contribution to A depend, inside B, on the part of B that needs A's contribution? If the Designs show an order of parts with no such dependency, the 2-cycle is a **projection artefact**. Otherwise it is a **real ordering contradiction**.
- **Rule-bearing or carry-only.** A rule-bearing row can be reversed only by moving definitional ownership. A carry-only row can be withdrawn behind an opaque reference, under GC-1 and GC-3.

Move codes and ScopeOfWork effect codes (S1, S2) are SCC-CASE-002 §1's. IV here means:
- the contract stays with the owner the ScopeOfWork already names;
- the cycle-closing arc is withdrawn as a contract input, because the consumer carries the supplier's records only by an opaque reference (GC-1, GC-3);
- the reverse arc already exists, so the edge in effect reverses.

**The one fact both pairs share.** Ruling R23-34 item 1 placed the standing vocabulary in DEL-07-02: "One standing vocabulary, defined in DEL-07-02 … DEL-07-01, DEL-08-01, DEL-09-10 and FV use it". CFB-v0.2 §1 says the derivation rules are the connector owners': "Connector-specific derivation is DEL-07-01's (PEC: `PEC_RECEIVING.md`, rules PR-1…PR-7 …) and DEL-08-01's (Domains, DRC-v0.1). They use this vocabulary; they do not redefine it." So:
- the vocabulary and the route are defined first (CFB §2–§5);
- each connector owner then applies its own rules and emits standing in that vocabulary (PRC §4 PR-1…PR-7; DRC §4 DR-1…DR-4);
- DEL-07-02's route reads those records at runtime.

What still makes DEL-07-02 a consumer of the two connectors is wording, not need: the ScopeOfWork sentences behind DEP-07-02-010/011/012, and CFB §6's two "Consumed from" rows.

## 2. Pair A — DEL-07-01 ↔ DEL-07-02

### 2.1 Rows

| Row | From → To | EvidenceQuote | Statement (excerpt) | Mirror / same-arc |
|---|---|---|---|---|
| DEP-07-01-014 | 07-01 → 07-02 | "connect the affected coordination question to the source-file route supplied by `DEL-07-02`" (DEL-07-01 REQ-005) | "The App PEC contract and adapter require the source-file route supplied by DEL-07-02 for unsupported absent, stale, partial or failing PEC cases, including total absence." | DEP-07-02-014: "this deliverable supplies its limitation and source-route handoff." (DEL-07-02 CLM-003) |
| DEP-07-02-010 | 07-02 → 07-01 | "App DEL-07-01 resolves and carries those terms; this deliverable defines the source route now and uses actual terms before dependent implementation/reliance." (DEL-07-02 TBD-001) | "Use DEL-07-01 actual PEC receiving terms before PEC-dependent implementation or reliance; the source-file route can be defined and used independently." | SAME_ARC DEP-07-02-012 and MIRROR DEP-07-01-015, below |
| DEP-07-02-012 (same arc) | 07-02 → 07-01 | "A later PEC join uses the exact coverage and qualification/release/App-adoption standing supplied by the App receiving owner" (DEL-07-02 AC-006; SourceRef also REQ-006, VER-006) | "For a later operational PEC join, consume the App receiving-owner evidence account for the exact envelope coverage, qualification, release and deliberate App adoption; unsupported material retains source recovery." | — |
| DEP-07-01-015 (mirror) | 07-01 hands to 07-02 (arc 07-02 → 07-01) | "the affected source-file route and the agent/manager/human responsibility handed to DEL-07-02" (DEL-07-01 AC-005) | "DEL-07-01 hands DEL-07-02 the affected coordination question, unsupported conclusions, source-file route context and accountable agent/manager/human responsibility for fallback treatment." | — |

### 2.2 ScopeOfWork

- DEL-07-01 REQ-005: "The App PEC contract and adapter shall identify unsupported conclusions for absent, stale, partial or failing PEC and connect the affected coordination question to the source-file route supplied by `DEL-07-02` in CLM-004."
- DEL-07-01 AC-005: "… absent, stale, partial and failing PEC cases identify unsupported conclusions, the affected source-file route and the agent/manager/human responsibility handed to DEL-07-02 …"
- DEL-07-02 CLM-003: "`DEL-07-01` owns first PEC questions, exact receiving terms, its adapter and qualification/release/App-adoption evidence; this deliverable supplies its limitation and source-route handoff."
- DEL-07-02 TBD-001 (quoted in §2.1).
- DEL-07-02 REQ-006: "When qualified PEC capability becomes available, this contribution shall connect its recovery path to the App envelope whose qualification, release and deliberate receiving adoption are established by the App PEC receiving owner in CLM-003."
- DEL-07-02 VER-006: "Examine a file-route-to-PEC join with the App DEL-07-01 evidence account: compare declared coverage, current limitations, qualification, release and App adoption with the consumed envelope. … Treat simulated joins as development evidence; actual adoption requires its own evidence …"

### 2.3 Design, both sides

**DEL-07-01 (PRC-v0.4).**
- §4 PR-5: "CFB CS-R1 (PEC: `record`)".
- PR-2: "`adopted` only if the response's release and every feed the question needs are adopted in the OUT-004 account (§6)".
- `pec.receiving-record.schema.json` takes the standing from DEL-07-02 by `"$ref": "urn:chirality:app-v4:del-07-02:connector-standing:0.1#/$defs/standing"`, and the conclusions by `…#/$defs/conclusions`.
- §5: `route.account_ref` names DEL-07-02's route account.

So DEL-07-01's receiving rules produce values of DEL-07-02's vocabulary. They are **rule-bearing** on it, which makes DEP-07-01-014 a definitional I.

**DEL-07-02 (CFB-v0.2).**
- §6, "Consumed from | DEL-07-01 (DEP-07-02-010/012) | PEC derivation rules; later, the adopted envelope account | held | PEC items stay `unknown`/`not_adopted`; route used".
- §2.1 defines `adopted` for PEC by citation: "the release is qualified and released, and the App has deliberately adopted it for this feed (DEL-07-01 OUT-004 account; R23-34 item 7)".
- §2.2's heading row cites "(connector-specific tests in PRC §4 and DRC §4)".
- §4 lists "the trigger: which connector, why, and the receiving records that sent it". The route-account schema types `trigger.receiving_records` as `{"type": "string", "minLength": 1}`: no pattern, and no `pr:` prefix check.

**What CFB actually uses.**
- No rule of CFB §2–§5 reads a PRC rule, an OUT-004 field, a PEC element name or a `pr:` identity.
- The "PEC derivation rules" CFB §6 says it consumes are applied in DEL-07-01. CFB receives only their result, a standing in its own vocabulary.
- CFB's own failure column says it works without them: "PEC items stay `unknown`/`not_adopted`; route used".
- EU-D1 shows the same at runtime: the route account `ra:EUD1-Q1` answers Q1 from files under every PEC condition, and `run_d` I-1 shows each connector's records unchanged with the other's inputs removed.

### 2.4 Order and verdict

**Part order.**
1. CFB §2 vocabulary and §4 route-account format.
2. PRC §4 derivation, which emits CFB values.
3. DEL-07-01 receiving records at runtime, with `route.account_ref`.
4. DEL-07-02 route accounts, which list the records that sent the question.
5. Later: DEL-07-02 VER-006's examination of an actual PEC join, against DEL-07-01's evidence account.

DEL-07-02's contribution to DEL-07-01 (the vocabulary and the route) depends on nothing DEL-07-01 supplies. Only step 5, a check, reads DEL-07-01's fields.

**Verdict: projection artefact.** One verification residual remains (step 5).

### 2.5 Move: M-01, IV by design rewording

**Arc:** DEL-07-02 → DEL-07-01, covering DEP-07-02-010, SAME_ARC DEP-07-02-012 and MIRROR DEP-07-01-015 (G1 K-7).

**Move.** DEL-07-02 receives DEL-07-01's material only as runtime receiving records, carried by an opaque reference. The vocabulary stays DEL-07-02's (R23-34 item 1). The PEC terms and the derivation stay DEL-07-01's (its CLM-004, REQ-001…REQ-006; DEL-07-02 CLM-003). No ScopeOfWork-assigned ownership moves.

**GC-1 test.**
- **(a) holds after the rewording.** CFB uses no field, state value or identity scheme that DEL-07-01 defines. The standing values are CFB's own.
- **GC-3 for the record identity.** It is typed as an uninterpreted string (already true in the schema). It is neither constructed, parsed nor validated. Only whole-string equality is used, to list and link. The rewording names the resolver, **DEL-07-01** (the record's writer and reader).
- **(b) holds.** Conformance of DEL-07-01's records to CFB's vocabulary is checked outside DEL-07-02:
  - by the supplier, whose schema `$ref`s CFB's standing schema and whose check validates every record (EU-D1 `run_d` S-1, S-neg);
  - by a third party, DEL-09-10's witness, whose pass conditions are CW-v0.2 §3.
- DEL-07-02's own check of an actual join, VER-006, is recorded as **V** (GC-1 (b)) and stays a register obligation at its point of need.

**Design rewording (design agent: O-D, for DEL-07-02).** Proposed text; not applied by this file.
- **CFB §1**, after "They use this vocabulary; they do not redefine it.", add:
  > "DEL-07-02 consumes none of their rules. It receives their receiving records at runtime, each carried only by its record identity, an uninterpreted string resolved by its writer (DEL-07-01 for PEC, DEL-08-01 for Domains) (GC-3). It reads only the standing those records carry, in this vocabulary."
- **CFB §2.1**, `adopted` row: replace "(DEL-07-01 OUT-004 account; R23-34 item 7)" with "as determined by DEL-07-01 from its OUT-004 account (PRC PR-2); this file reads only the resulting value".
- **CFB §2.2**, heading row: "(connector-specific tests in PRC §4 and DRC §4)" becomes "(each connector owner applies its own tests: PRC §4, DRC §4)".
- **CFB §4**, the trigger bullet becomes:
  > "the trigger: which connector, why, and the identities of the receiving records that sent it, as uninterpreted strings resolved by their writers (GC-3)".
- **CFB §6**, replace the row "Consumed from | DEL-07-01 (DEP-07-02-010/012) | …" with:
  > "Receives at runtime, by reference | DEL-07-01 | Receiving records (identity and standing in this vocabulary); not a contract input (GC-1) | none (withdrawn) | PEC items stay `unknown`; route used".

  Add a row:
  > "Verification | DEL-07-01 OUT-004 evidence account | VER-006's examination of an actual PEC join | V, at the actual join | Join not examined; simulated joins stay development evidence".

**ScopeOfWork wording: S1** (no ownership moves), applied by `scope-of-work` under an owner-accepted SCA.
- **DEL-07-02 TBD-001**, the clause quoted by DEP-07-02-010. Proposed:
  > "App DEL-07-01 resolves those terms and applies them in its receiving records, which express standing in this deliverable's vocabulary; this deliverable defines the vocabulary and the source route, and receives DEL-07-01's records only by reference."
- **DEL-07-02 REQ-006**, the clause behind DEP-07-02-012. Proposed:
  > "connect its recovery path to DEL-07-01's receiving records, whose envelope standing the App PEC receiving owner establishes from qualification, release and deliberate receiving adoption (CLM-003)".

  AC-006 needs no change: the standing it uses is "supplied by the App receiving owner" in DEL-07-02's own vocabulary.
- **DEL-07-01 AC-005**, receiver clause, *conditional*. Only if `dependency-extract` still reads "handed to DEL-07-02" as a contract input after the Design rewording. Proposed:
  > "… the agent/manager/human responsibility of DEL-07-02's source-file route, to which the receiving record refers …"

  No obligation changes.

**Residual.** **V** on the same arc, at DEL-07-02 VER-006's point of need (an actual PEC join). It also covers VER-001's "Use the relevant agreed connector meanings" for PEC. VER-006 is not narrowed here: narrowing a check is not an agent's move (workflow §2).

**Closes the arc under:** O-2, O-3 and O-4. Under O-1 the V residual sequences (§5).

**Anchor.**
- DEL-07-02: CFB-v0.2 §2, §4; `connector.standing.schema.json`; `connector.route-account.schema.json`.
- DEL-07-01: PRC-v0.4 §4, §5; `pec.receiving-record.schema.json`.

### 2.6 The other closing row of pair A, not moved

**DEP-07-01-014 (07-01 → 07-02)** stays I.
- PRC's rules produce CFB's values, and its schema `$ref`s CFB's standing.
- Reversing it would move the vocabulary's ownership to DEL-07-01. That is IV-O, and it contradicts R23-34 item 1.

## 3. Pair B — DEL-07-02 ↔ DEL-08-01

### 3.1 Rows

| Row | From → To | EvidenceQuote | Statement (excerpt) | Mirror |
|---|---|---|---|---|
| DEP-07-02-011 | 07-02 → 08-01 | "Connector-specific meanings come from the receiving owners in CLM-003 and unresolved terms in TBD-001 and TBD-002" (DEL-07-02 REQ-001; SourceRef also CLM-003, TBD-002) | "Consume DEL-08-01 Domains admission/query/provenance/freshness meanings and the applicable resolved data-boundary terms when integrating the Domains-specific path; common fallback and independent work continue without Domains." | DEP-08-01-010: "This contract defines the Domains-specific admission/query cases they consume." (DEL-08-01 CLM-005) |
| DEP-08-01-009 | 08-01 → 07-02 | "App v4 `DEL-07-02`, owned by the App connector-receiving owner, supplies the common connector limitation/source-file recovery behavior;" (DEL-08-01 CLM-005; SourceRef also REQ-005) | "Use the common connector limitation/source-file recovery behavior for Domains-specific unavailable, unsuitable and stale-source cases." | — |

### 3.2 ScopeOfWork

- DEL-07-02 REQ-001: "Connector-specific meanings come from the receiving owners in CLM-003 and unresolved terms in TBD-001 and TBD-002 (CLM-001, CLM-002)."
- DEL-07-02 CLM-003: "`DEL-08-01` owns Domains-specific admission/query/provenance/freshness terms and the unresolved deployment/data-boundary account".
- DEL-08-01 CLM-005: "App v4 `DEL-07-02` … supplies the common connector limitation/source-file recovery behavior; … App v4 `DEL-09-10` … supplies the broader optional-connector witness. This contract defines the Domains-specific admission/query cases they consume."
- DEL-08-01 REQ-005: "… connect to the supported source-based recovery/responsibility route in CLM-005."

### 3.3 Design, both sides

**DEL-08-01 (DRC-v0.1).**
- §4 DR-4: "Reliance follows CFB CS-R1".
- `domains.receiving-record.schema.json` `$ref`s CFB's standing.
- §8: "To DEL-07-02: Domains derivation rules (§4); limitation cases (§5)."

DRC is rule-bearing on CFB's vocabulary, which makes DEP-08-01-009 a definitional I.

**DEL-07-02 (CFB-v0.2).**
- §6, "Consumed from | DEL-08-01 (DEP-07-02-011) | Domains derivation rules | held | Domains items stay `not_adopted`; route used".
- §2.1 `adopted` for Domains cites "DEL-08-01 OUT-004; OI-023".
- §2.3's Domains tiers, `admitted` and `located_not_admitted`, are CFB's own values, and DRC DR-4 maps to them.
- No CFB rule reads a DRC rule or element.
- The data-boundary terms in DEP-07-02-011's Statement bind the Domains query path (DRC §6). DEL-07-02's route reads project files and contacts no Domains destination.

### 3.4 Order and verdict

**Part order.**
1. CFB §2 vocabulary and route.
2. DRC §4 derivation, which emits CFB values.
3. Domains receiving records at runtime.
4. DEL-07-02 route accounts by reference.
5. DEL-07-02 VER-001's comparison "using the relevant agreed connector meanings", if it is extracted as a row.

**Verdict: projection artefact.** There is at most one verification residual (step 5).

### 3.5 Move: M-02, IV by design rewording

**Arc:** DEL-07-02 → DEL-08-01, covering DEP-07-02-011 and MIRROR DEP-08-01-010.

**GC-1 and GC-3.** As M-01.
- Record identities are uninterpreted strings resolved by DEL-08-01.
- Conformance is checked by DEL-08-01's schema `$ref` and by DEL-09-10's cases OC-1 and IA-2.

**Design rewording (design agent: O-D, for DEL-07-02 and DEL-08-01).**
- **CFB §1 and §4:** as M-01, which already covers DEL-08-01.
- **CFB §2.1**, `adopted` for Domains: "as determined by DEL-08-01 (DRC DR-2); this file reads only the resulting value".
- **CFB §6**, replace "Consumed from | DEL-08-01 (DEP-07-02-011) | Domains derivation rules | …" with:
  > "Receives at runtime, by reference | DEL-08-01 | Receiving records; not a contract input (GC-1) | none (withdrawn) | Domains items stay `unknown`; route used".
- **DRC §8**, "To DEL-07-02: Domains derivation rules (§4); limitation cases (§5)." becomes:
  > "To DEL-07-02: none as definitions. This file applies DEL-07-02's vocabulary and route (DEP-08-01-009). Its receiving records reach DEL-07-02's route only by reference at runtime (GC-3; resolver: this deliverable). Limitation cases (§5) go to DEL-09-10."

**ScopeOfWork wording: S1** (no ownership moves).
- **DEL-07-02 REQ-001**, the sentence quoted by DEP-07-02-011. Proposed:
  > "Connector-specific meanings are applied by the receiving owners in CLM-003 (with unresolved terms in TBD-001 and TBD-002), who express each item's standing in this deliverable's vocabulary; this deliverable defines no connector-specific term."
- **DEL-08-01 CLM-005**, last sentence, the mirror's quote. Proposed:
  > "This contract defines the Domains-specific admission/query cases `DEL-09-10` consumes; it applies `DEL-07-02`'s common vocabulary and route to them, and `DEL-07-02` receives Domains material only as this deliverable's receiving records, by reference."

  DEL-09-10's consumption is already its own admitted row, DEP-09-10-007, mirrored by DEP-08-01-011.

**Residual.** V, **conditional**: DEL-07-02 VER-001's "Use the relevant agreed connector meanings", if `dependency-extract` reads it as a row for Domains. VER-005 needs no Domains contribution: "against the receiving contracts **or explicitly simulated equivalents**".

**Closes the arc under:** O-2, O-3 and O-4. It also closes under O-1 if no VER-001 row is extracted.

### 3.6 The other closing row of pair B, not moved

**DEP-08-01-009 (08-01 → 07-02)** stays I, for the reason in §2.6: DRC is rule-bearing on CFB's vocabulary.

## 4. Integrator rulings the moves would amend (GC-4)

| Ruling | Text amended | Needed by |
|---|---|---|
| **R23-34 item 1** | "It is built under SCC-CASE-005 R1, with no new row." | M-01 and M-02 replace R1 (coordinated milestones, which keep the cycle) with inversion for this component. The rest of item 1 (one vocabulary, defined in DEL-07-02; three facets; the reliance rule) is unchanged, and the moves rely on it |

- Amending it is HELP_HUMAN's act at application, listed in the owner-facing checkpoint (GC-4 item 2).
- No other ruling is touched:
  - R23-34 items 3, 6 and 7 (consumption route, files not rows, adoption as two facts) agree with the moves;
  - R23-37, R23-40, R23-50, R23-52 and R23-53 concern contents that do not change.
- **SCC-CASE-005 Open_Questions Q1** asked the human to choose R1, R2 or R3. It is not a ruling. This proposal offers an invert, which Q1 did not list. The owner's checkpoint decides whether it replaces R1.

## 5. Closure under each option (G1 r3 kinds)

**Model.**
- The whole DAG-004 graph, both layers, every arc outside the component kept under every option. That is a superset, so the results are conservative.
- The component's four arcs take the kinds below.
- The script reports the members left and the exact minimum feedback arc set.

| Scenario | O-1 | O-2 | O-3 | O-4 |
|---|---|---|---|---|
| S0: today, no move | 3 members, 2 rows | 3, 2 | 3, 2 | 3, 2 |
| **S1: M-01 + M-02, V residual on both arcs** | **3 members, 2 rows** (both V residuals) | **acyclic** | **acyclic** | **acyclic** |
| S2: M-01 + M-02, no VER-001 row extracted (V residual on pair A only) | 2 members {07-01, 07-02}, 1 row | acyclic | acyclic | acyclic |
| S3: S1 + owner acts on the V residuals | acyclic | acyclic | acyclic | acyclic |
| S4: M-01 only | 3, 2 | 2 {07-02, 08-01}, 1 | 2, 1 | 2, 1 |
| ALT: owner cuts of the I arcs of DEP-07-02-010 and DEP-07-02-011, no rewording | acyclic | acyclic | acyclic | acyclic |

**What remains under each option, given M-01 and M-02:**
- **O-2, O-3, O-4:** nothing. The component closes with no owner act.
- **O-1:** the V residuals.
  - Pair A certainly: DEL-07-02 VER-006.
  - Pair B only if VER-001 is extracted as a row.
  - Each needs an owner act: a per-edge cut of the V residual, or an owner-accepted SCA that narrows DEL-07-02 VER-006/VER-001 so that their comparison with DEL-07-01's account is left to DEL-07-01's own VER-006. DEL-07-01 VER-006 already audits that account: "Audit the evidence account's identities and links against the actual provider contract, qualification/release evidence, consumer adoption …".
  - Narrowing a check is the owner's to accept.

## 6. Summary

| Pair | Verdict | Move | Who | Closes under |
|---|---|---|---|---|
| A: DEL-07-01 ↔ DEL-07-02 | Projection artefact; V residual (VER-006) | **M-01: IV by design rewording** of DEP-07-02-010 with DEP-07-02-012 and DEP-07-01-015 (CFB §1, §2.1, §2.2, §4, §6), plus S1 on DEL-07-02 TBD-001 and REQ-006 (and DEL-07-01 AC-005, conditionally) | O-D (design agent); SCA for S1 | O-2, O-3, O-4. O-1 needs an owner act on the V residual |
| B: DEL-07-02 ↔ DEL-08-01 | Projection artefact; V residual only if VER-001 is extracted | **M-02: IV by design rewording** of DEP-07-02-011 with DEP-08-01-010 (CFB §2.1, §6; DRC §8), plus S1 on DEL-07-02 REQ-001 and DEL-08-01 CLM-005 | O-D; SCA | O-2, O-3, O-4, and O-1 if no VER-001 row |

- **Owner acts needed.**
  - **O-2 to O-4:** none.
  - **O-1:** a cut or an accepted narrowing of DEL-07-02 VER-006's V residual. The same for VER-001, if it is extracted.
- **HELP_HUMAN:** amend R23-34 item 1's "built under SCC-CASE-005 R1".
- **Alternative**, not preferred: owner cuts of both I arcs. Those cuts would leave the ScopeOfWork sentences contradicting the graph.
- **Not proposed:** moving DEP-07-01-014 or DEP-08-01-009. Both are rule-bearing on DEL-07-02's vocabulary, so reversing them is IV-O and contradicts R23-34 item 1.

## 7. Not established

| Item | Why |
|---|---|
| Whether `dependency-extract` reads DEL-07-02 VER-001 ("Use the relevant agreed connector meanings") as a row after the rewording | It decides whether pair B has a V residual under O-1 (S1 vs S2) |
| Whether `dependency-extract` stops reading DEL-07-01 AC-005's "handed to DEL-07-02" as a contract input once CFB carries records by reference | If it does not, the conditional S1 on AC-005 is needed |
| Whether the owner prefers narrowing DEL-07-02 VER-006 to a per-edge cut under O-1 | Owner's choice. Both are listed |
| Review of the proposed CFB and DRC rewordings | They are proposals. Each is reviewed when applied |

## 8. 2026-10-04 repair (RVG-CASE-005: C5-M1, C5-m1)

**Standing and scope.**
- This section repairs §1–§7 under review RVG-CASE-005 (`reviews/RVG-CASE-005.md`, sha256 `a86c9a959696a54146c2d3c77cd8ebd866782b67f8b72ea2341e767736c738cd`, commit `e987d34d2c`, verdict REPAIR, narrow).
- It is append-only. Nothing above is deleted. Where this section and an earlier one differ, **this section supersedes** it.
- **Superseded:**
  - §2.5's "Residual" and "Closes the arc under" lines;
  - §3.5's same two lines;
  - the M-01 rewording sentence for CFB §1 ("It reads only the standing …");
  - §5's closure table and "What remains";
  - §6's owner-acts paragraph;
  - the CSV rows M-01, M-02, M-03 and M-04, superseded by M-01-R, M-02-R and M-03-R.
- **What stands, as RVG confirmed:**
  - both artefact verdicts;
  - the rewordings' direction;
  - R23-34 item 1's vocabulary ownership;
  - the GC-1 (b) claim;
  - leaving DEP-07-01-014 and DEP-08-01-009 unmoved;
  - the GC-4 entry for R23-34 item 1.

### 8.1 C5-M1: the runtime hand-over is an E row on both arcs

**Finding accepted.** The rewording withdraws the *contract* input (I) but keeps a *runtime* flow on both arcs:
- **Arc DEL-07-02 → DEL-07-01.**
  - DEL-07-01 REQ-005 ("connect the affected coordination question to the source-file route supplied by `DEL-07-02`") and AC-005 (the responsibility "handed to DEL-07-02") send each affected question to DEL-07-02's route at runtime.
  - The proposed CFB §6 row ("Receives at runtime, by reference | DEL-07-01 | Receiving records") says so in terms.
- **Arc DEL-07-02 → DEL-08-01.** The proposed DRC §8 ("Its receiving records reach DEL-07-02's route only by reference at runtime") and the CFB §6 row for DEL-08-01 keep the same flow.

**Kind.** The consumer, DEL-07-02, defines the format of what it receives: the route-account trigger, in CFB's own schema. By G1 r3 K-3 each arc is therefore **E**, not removed. This is the same pattern as RVG-C2 B2-M1, accepted in SCC-CASE-002 §23. On pair A the arc also keeps the **V** residual (DEL-07-02 VER-006).

**Can an S1 wording remove the runtime receipt without moving ScopeOfWork ownership? No.**
- The runtime receipt is DEL-07-02's assigned obligation, not wording that a consumption sentence carries:
  - DEL-07-02 OUT-001: "App connector receiving behavior that shows standing, freshness and limitations, distinguishes absent/stale/partial/failing conditions, and connects affected questions to source recovery independently for PEC and Domains."
  - REQ-001: "The App shall show the source identity, standing, available coverage/freshness information and limitations of connector-supplied material."
  - AC-001: "Receiving evidence distinguishes qualified/current, absent, stale, partial and failing material, shows the available source/standing/coverage/freshness information and names unsupported conclusions".
- DEL-07-02 can show the standing of connector-supplied material, and route the affected question, only if it receives that material's standing at runtime.
- Removing the receipt would move the showing and routing obligation to DEL-07-01 and DEL-08-01. That is **S2**, an ownership move (IV-O), or a decomposition. Either is the owner's.
- The conditional S1 on DEL-07-01 AC-005 (§2.5) rewords the hand-over but keeps it, as RVG notes.
- **No S1 wording removes it.**

### 8.2 C5-m1: the CFB §1 sentence, reworded

**Finding accepted.** "It reads only the standing those records carry, in this vocabulary" would read `response_standing`, `claims` and `conclusions`. Those fields belong to DEL-07-01's record structure (`pec.receiving-record.schema.json` properties), even though their values are CFB `$def`s. That breaks GC-1 (a).

**Replacement for the M-01 CFB §1 sentence** (design agent: O-D, for DEL-07-02; proposed, not applied):
> "DEL-07-02 consumes none of their rules and reads no field of a receiving record. The trigger of a route account (the connector, the standing in this vocabulary, why, and the identities of the receiving records concerned) is supplied in this file's route-account format by the connector owner that sends the question. The record identities are uninterpreted strings resolved by their writers, DEL-07-01 for PEC and DEL-08-01 for Domains (GC-3)."

**Consequences in CFB, for the same rewording:**
- **§4's trigger bullet:**
  > "the trigger, as supplied by the sending connector owner in this format: which connector, the standing in this vocabulary (§2), why, and the record identities (uninterpreted; GC-3)".
- **`connector.route-account.schema.json`:** `trigger` gains `standing` (`$ref` to this file's own `#/$defs/standing`). Its `receiving_records` stays an uninterpreted string array.
- **The REQ-001 display** shows the standing carried in that trigger, in CFB's own format. DEL-07-01's fields are not read.

With this text, (a) holds:
- the connector owners write CFB's format, on the existing arcs DEP-07-01-014 and DEP-08-01-009;
- DEL-07-02 reads only its own format.

It does not remove the E row of §8.1. It makes the remaining flow cleanly E, with no I part.

### 8.3 Closure, repaired (supersedes §5)

**Model.**
- As §5: the whole DAG-004 graph, both layers, every arc outside the component kept.
- DEP-07-01-014 and DEP-08-01-009 stay I.
- Arc DEL-07-02 → DEL-07-01 is E, with a V residual. Arc DEL-07-02 → DEL-08-01 is E.
- Script: `$TMPDIR/scc004_repair.py`.

| Scenario | O-1 | O-2 | O-3 | O-4 |
|---|---|---|---|---|
| R1: M-01-R + M-02-R (E on both arcs; V also on pair A) | 3 members, 2 rows | 3, 2 | 3, 2 | **acyclic** |
| R2: R1 + owner cuts of arcs DEL-07-02 → DEL-07-01 and DEL-07-02 → DEL-08-01 | acyclic | acyclic | acyclic | acyclic |
| R3: E on pair A only (pair B removed) | 2 {07-01, 07-02}, 1 | 2, 1 | 2, 1 | acyclic |
| ALT-DEC: DEL-07-02 split into (a) vocabulary and route definition and (b) runtime receiving and display. Conservative model: every outer arc of DEL-07-02 is given to both parts | acyclic | acyclic | acyclic | acyclic |

This reproduces RVG's computation (C5-M1).

**Owner acts and what remains, by option, given M-01-R and M-02-R:**

| Option | Owner acts needed | What remains without them |
|---|---|---|
| **O-4** | **None** | Nothing: E and V both leave |
| **O-3** | **2 arc cuts:** DEL-07-02 → DEL-07-01 (covering DEP-07-02-010, -012 and DEP-07-01-015; the E residual) and DEL-07-02 → DEL-08-01 (covering DEP-07-02-011 and DEP-08-01-010; the E residual) | 3 members, 2 rows |
| **O-2** | The same 2 arc cuts | 3 members, 2 rows |
| **O-1** | The same 2 arc cuts. The first also covers VER-006's V residual on that arc (RVG C5-n2). Narrowing VER-006 alone no longer suffices | 3 members, 2 rows |

- **Relation to M-ALT.** These are the same two arcs as M-ALT. Under O-1…O-3 the rewording changes *what* the cut reclassifies, a runtime hand-over instead of an interface. It does not change how many owner acts are needed. Under O-4 it removes both, with no owner act.
- **Owner alternative to the cuts under O-1…O-3: a decomposition of DEL-07-02** (ALT-DEC).
  - Split DEL-07-02 into a definition part (CFB §2–§5: vocabulary, route-account format, route method) and a runtime part (OUT-001/REQ-001 receiving behaviour and display, the route's execution).
  - The connectors consume the definition part. The runtime part consumes the connectors' material.
  - It closes under every option with no cut. It is a decomposition change through `scope-change`, so it is the owner's. It is listed, not recommended: two cuts are smaller.
- **The VER-001 extraction question (§7, S1/S2)** no longer decides anything for pair B, because the E residual is there either way (RVG C5-n3).

### 8.4 Summary (supersedes §6 where they differ)

| Pair | Verdict | Move | Residual on the arc | Closes with no owner act under | Owner act under the others |
|---|---|---|---|---|---|
| A: DEL-07-01 ↔ DEL-07-02 | Projection artefact (stands) | **M-01-R**: IV by design rewording (the §2.5 text, with §8.2's CFB §1, §4 and schema wording); S1 as §2.5 | **E** (runtime hand-over, DEL-07-02 OUT-001/REQ-001 and DEL-07-01 REQ-005/AC-005) and **V** (VER-006) | **O-4** | O-1…O-3: owner cut of arc DEL-07-02 → DEL-07-01 (M-03-R), or ALT-DEC |
| B: DEL-07-02 ↔ DEL-08-01 | Projection artefact (stands) | **M-02-R**: IV by design rewording (§3.5, with §8.2); S1 as §3.5 | **E** (runtime hand-over, DEL-07-02 OUT-001/REQ-001 and DRC §8) | **O-4** | O-1…O-3: owner cut of arc DEL-07-02 → DEL-08-01 (M-03-R), or ALT-DEC |

**Not established (adds to §7):**
- whether `dependency-extract` would record the E rows as one row per arc or several, which does not change the arc arithmetic;
- the owner's choice between the two cuts and ALT-DEC under O-1…O-3.
