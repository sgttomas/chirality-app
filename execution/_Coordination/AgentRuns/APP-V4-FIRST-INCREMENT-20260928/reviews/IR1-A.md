# IR1-A — Independent review of the v0.2 set: policy and records

- Run: APP-V4-FIRST-INCREMENT-20260928, node IR1-A (Type 2 reviewer; no delegation; authored none of the reviewed files)
- Date: 2026-09-28
- Brief: [BRIEFS.md](../BRIEFS.md) "Common brief", "Owner rulings now in force", "IR1" (IR1-A: DEL-04-01, DEL-04-02, DEL-04-03 against each other and against the policy/record consumers in the other six files; R2 items X-1, X-2, X-3, X-4, X-13, X-15)
- Standing: review findings and recommendations only. This review performs no human act, accepts nothing, and does not issue R2 rulings (HELP_HUMAN does).
- Write scope honoured: only this file was written. No network access. Disclosure: at the start of the session the reviewer ran one read-only `git log --oneline -3` and one `git status --short` before noting the brief's "no git operations" rule; nothing was changed by them and no further git command was run.

## 1. Files reviewed (sha256 of the bytes read)

| File | Lines | sha256 |
|---|---|---|
| DEL-04-01 `Design/ACT_AND_POLICY_CONTRACT.md` (ACT-POLICY-v0.2) | 827 | e50f1fe2f5bb2e3280bc62175e5aeeaa4508eed713424d82c54536a9fb5993a9 |
| DEL-04-02 `Design/AUTONOMY_AND_STANDING_EXCHANGE.md` (AS-v0.2) | 318 | 3a4e8b01366c229c463f805aef402edd378a9491ed692f778b89b94a777a329c |
| DEL-04-03 `Design/RECORD_SEMANTICS.md` (RS-v0.2) | 434 | 56a3f839f5133813d18fe630bcedf7b30cab8f72e815e9d174f87b0994e21c69 |
| DEL-03-01 `Design/CATALOG_AND_READ_BASIS.md` (C-v0.2) | 577 | 358182b18b1fe13f9af6e6f5a61c9ed57f91b6ab29ea0c9adab06fe0081d6d82 |
| DEL-03-02 `Design/PROPOSAL_LIFECYCLE_AND_OUTCOMES.md` (P-v0.2) | 575 | 942c1a3ab5ad7bda865640067f0fd550d7cfd1acd8f6ee228f6906452adf8c89 |
| DEL-02-01 `Design/WORKFLOW_DECLARATION.md` (WD-v0.2) | 706 | c25bccc5f3ac02c84522148eeaa8a6ef0f5eb4a380686773cff45f57a448a55c |
| DEL-02-01 `Design/EXAMPLES.md` | 327 | 50b7600de8503f51f440e5947ebd4ea7a559781e2497d5d880a8d683f7a9c43e |
| DEL-05-01 `Design/LOOP_RECEIVING_CONTRACT.md` | 864 | 1151d432c106ed3c1980918eca9d9360116292e3b9c602ed67f4c2d6718762c9 |
| DEL-05-02 `Design/PANEL_RECEIVING_CONTRACT.md` | 468 | 0a8a0dbe18ed3e6cc893003e41c4b70b6bbae288d2c02a99d7044c00d719a700 |
| DEL-01-01 `Design/HOSTING_BOUNDARY.md` | 889 | 16711a83fec3439d7be634f6d62512be2a87f0dec32bd84028a39425bc84007a |
| DEL-01-01 `Design/PIN_SPIKE_0.158.0.md` (policy-relevant rows only) | 350 | 26ea0c2fae8212ca46ed2ff60ddfaef5ca28e0ed73aae2105017d7ceccb40334 |

DEL-04-01/02/03 were read in full, with their ScopeOfWork.md files. The other files were read in the sections that carry policy or record meaning (C §§2–6, 10; P §§0–14; WD §4.3; LOOP §§2.2–2.3, 6, 9; PANEL §§3.3–3.6, 5; HOSTING §6 R7/R8, S-7, U-list), plus targeted searches across all nine.

Basis files, all matching the hashes the designs cite: `OWNER_DECISIONS.md` f3f8e5f31ec87006fc9ab459c6ae57d08638439c234fa959ba2605914cf81f2e; `R1_RESOLUTIONS.md` 2f9c7e72aa8362624ad830377a70077b27a27bf03871f8e87811a28e6e177ec4; `R2_CANDIDATES.md` fa99768452e7b2049de0f43318f544ae34e2ca8706f2e638b82948c164f73c1b; V1-A 01811533…4c09, V1-B 09eebfe0…1cae, V1-C 8d46258a…94a6. SoW hashes match the headers: DEL-04-01 fc1a0503…f5e6, DEL-04-02 23a28caa…5e21, DEL-04-03 74d42c38…40c1.

## 2. Summary

| Severity | Count | IDs |
|---|---|---|
| BLOCKING | 0 | — |
| MAJOR | 8 | IR1A-01 … IR1A-08 |
| MINOR | 13 | IR1A-09 … IR1A-21 |

**Verdict.** The set is **fit to merge as v0.2 drafts**. No finding makes a
file misstate an owner ruling, claim implementation, host delivery or a
performed human act, or break a join so badly that the merged drafts would
mislead a reader who also has this review. The eight MAJOR items are real
v0.2 ↔ v0.2 disagreements that the R1 repairers could not see because each
worked from R1_RESOLUTIONS rather than sibling text. They should be repaired in
R2 before any receiver treats these joins as confirmed.

The core R1 rulings do hold across the texts:
- R-1: canonical names A1–A14 are used everywhere;
- R-6: A5 binds to change-item content identity, and L-1 has three c₁ sources;
- R-7: the outcome taxonomy is adopted unchanged;
- R-8: display states and the two settings references are consistent;
- M3: the DEL-04-02 §6 / DEL-04-03 §8 exchange text is byte-identical (checked by diff).

The residual defects sit at the edges of those rulings:
- the fifth class value;
- how reserved entries are offered;
- decline scope and naming;
- A12 binding;
- default-derived grants;
- undo and lapse;
- fixture alignment;
- the "perform or record" wording.

## 3. Joins — R1 resolutions that hold, and residual disagreements

### 3.1 R1 resolutions checked in the actual v0.2 texts

| Ruling | Holds in | Residual |
|---|---|---|
| R-1 canonical names; closed checkpoint list A4/A5/A6/A7/A12 | 04-01 §2.1/§4.1; 04-02 §0; 04-03 §0; P §10; WD §4.3.1/FB-03; LOOP §9; PANEL §5 | Negative-path scope for A12: IR1A-03 |
| R-2 D2/D3 in the policy representation; reserved class for act-performing operations; SWB class DERIVED with default propose; OI-002 removed | 04-01 §3, §8.3; 04-02 §2; 04-03 §0; C §3.1; P S-P14/15; LOOP §2.2; PANEL K-4; HOSTING R7 | Fifth-value vocabulary: IR1A-01. "Perform or record": IR1A-08 (X-1). Over-claim labels: IR1A-16 |
| R-3 treatment resolved on the host route; *not permitted* never converted; no-policy-basis → propose available; in-flight narrowing and widening | 04-01 §5.3–§6; 04-02 §2, §5; 04-03 §5; C §4.1; P §2, §4.2; LOOP O-4/O-5; PANEL §3.3 | Offer/withhold of reserved entries: IR1A-02. Automatic vs offered A8: IR1A-10 |
| R-4 labels | 04-01 §9; 04-02 §8/§9; C §6.2; WD §4.4; PANEL §3.4 | 04-02 F9 labels an agent examination "host checks passed" (IR1A-07) |
| R-5 reached-when, subject binding, dispositions, forced propose, capturing-surface evidence | 04-01 §4; 04-02 §4; 04-03 R8/HA-7; P §4.4; WD §4.3; LOOP; PANEL W-5 | Decline scope and name: IR1A-03. Lapse-before-resume sequence: IR1A-09. Run-ended while waiting: IR1A-18 |
| R-6 content identities; acceptance unit = change item; application does not lapse A5; stale ≠ lapse | 04-01 §2.5; 04-03 §6.1, L-1, L-2, L-10; C §5.1, §5.3; P §3.1, §4.2; WD SB-2; PANEL §3.3 | A12 binding: IR1A-04. Undo vs lapse: IR1A-06 |
| R-7 P §9 + C §4.1 adopted unchanged; application error with effect; observer-attributed unknown; per-submission recording; retry keeps identity | 04-03 §5 (table matches P §9 row by row); 04-02 §8; LOOP TL-2/TL-3; PANEL §3.3 | Accepted-then-stale display: IR1A-11 (X-8) |
| R-8 display states, scope, requester vs setting actor, two settings references, record-out additions | 04-02 §3/§5/§6 = 04-03 R6/§8; P §3.3, §4.4; LOOP O-5/O-6; PANEL §3.6 | Default-derived *effective*: IR1A-05 (X-4). A12 binding: IR1A-04 (X-13) |
| R-9 workflow identity; generation vs revision; exposure; shared fixture | 04-03 R2 = WD §6.1 = P §3.3; C §5.1 generation; C element 9 | Fixture divergence: IR1A-07 (X-6) |
| R-10 supplied-guidance identity per thread and turn; A14 origin | 04-03 R3 and HOSTING §7 (lines 577–589); 04-03 R13 origins match HOSTING settlement origins in meaning | R13 feed path: IR1A-19 |

### 3.2 Residual disagreements

#### MAJOR

**IR1A-01 — The fifth class value has two names and two coverages.**
- DEL-04-01 §5.1/§8.1: "none | may apply within granted autonomy | proposal only | reserved to the person | *no policy basis*". Rule 5 says a class is *no policy basis* "when it is omitted, unassigned, or `UNRESOLVED{OI-021}`". DEL-04-02 §2, DEL-04-03 §8 and LOOP O-4 use "no policy basis".
- C §3.1 uses "**policy basis pending** (operation-specific addition awaited under `UNRESOLVED{OI-021}`)". P §2 and §4.4 use "*policy basis pending* (OI-021)". This covers the OI-021 case only; C has no value for an omitted or unassigned class (04-01 FX-17).
- LOOP §2.2 "Vocabulary. The four V4-HI-02 values" omits the fifth value, although its own O-4 invokes it.
- DEL-04-01 §5.1 labels the whole five-value list "Vocabulary SETTLED by V4-HI-02". The fifth value is INTEGRATION (R-3.5).
- **Change:**
  - C, P and LOOP adopt DEL-04-01's value name *no policy basis* (DEL-04-01 owns the class vocabulary, V-02). They add a reason sub-element: class omitted · unassigned · operation-specific addition pending `UNRESOLVED{OI-021}`.
  - LOOP lists five values.
  - DEL-04-01 §5.1 marks the four V4-HI-02 values SETTLED and the fifth INTEGRATION.

**IR1A-02 — Reserved entries: "withheld → *not exposed*" conflicts with C and LOOP.**
- DEL-04-01 §6 row 8: "If withheld: **not exposed on this surface** (R-9) … DEL-05-01 with DEL-03-01 chooses offer or withhold". FX-35 expects "Withheld: *not exposed on this surface*", and U-11 is held open.
- C §2 invariant 5: "An entry whose class is *reserved to the person* remains described to every consumer. An agent request for it yields *not permitted* … never *unavailable*, *missing* or *not exposed*."
- LOOP TL-5: "The loop does not decide treatment and does not withhold an exposed entry on its own reading of its class."
- DEL-04-01 conflates a loop's offering choice with the host's per-surface exposure (C element 9). Exposure is not a policy consequence.
- **Change DEL-04-01:**
  - Row 8 becomes: reserved entries are described and, where exposed, offered; invocation → row 7.
  - *Not exposed on this surface* is only the host's element-9 value and is never used to express a class.
  - FX-35 is rewritten as "invoked → *not permitted* + A8 offered; *not exposed* or *unavailable* for a class reason → non-conformant".
  - U-11 is closed by LOOP TL-5.

**IR1A-03 — Decline event: scope, name and "stop" conflation.**
- Scope. DEL-04-01 §2.3 and WD I-6/§4.3.4 give the negative path for A4, A6, A7 **and A12**. DEL-04-02 §4, DEL-04-03 §3/HA-8, LOOP §2.3 ("Person's decision not to perform A4/A6/A7") and PANEL W-5d cover A4/A6/A7 only. A declined A12 checkpoint therefore has no record kind in DEL-04-03 and no display in DEL-04-02 or PANEL. R-5 itself says "For A4/A6/A7", while R-1 admits A12 checkpoints. DEL-04-01 is right to extend the scope.
- "decline/stop" merges two things:
  - a decision not to perform the act on the bound subject, which gives *resolved negatively*;
  - stopping the work (V4-EXE-01, listed separately in DEL-04-01 §2.1). Under X-12, a run that ends while waiting stays *waiting* with a run-ended event.
- One person action must not fall under both rules.
- The word "decline" is already used for A14 settlements (HOSTING §6: `answered | declined`, "explicit negative answer by the person"). P §4.1 also describes A10 as "The person declined the item".
- **Change:** as the X-2 amendment in §4.

**IR1A-04 — A12 binds to a settings version that may never exist.**
- DEL-04-03 §6.1 gives the A12 bound subject as "settings version" and c₀ as "settings-version identity". E7: "⟨act:5⟩ A12 set grant, bound subject ⟨set:2⟩".
- DEL-04-02 §5 creates that version only when "Control establishes → new settings version ⟨set:n+1⟩". A refused setting never gets one. The act (*set by person, not yet confirmed*) comes before the version.
- DEL-04-01 §2.5: A12 binds to "The setting the act establishes. PROPOSED: a later A12 or A13 supersedes the earlier one. No lapse is defined."
- DEL-04-03 L-1 has no A12 source. Evaluated literally, an A12 is *unknown (unavailable)* or *lapsed* at every later settings version.
- WD SB-4/U-27: the binding is "not yet defined by any supplier".
- **Change:** DEL-04-01, DEL-04-03 and DEL-04-02 as the X-13 amendment in §4.

**IR1A-05 — A grant that is effective by default is shown two ways.**
- DEL-04-02 §3: *effective* when "an A12 record … exists (or the value is the policy default)". F1: "OP-C4/C5 *effective: propose*" (default). *not set* = "No setting and no default supplied".
- DEL-04-01 §5.3 rule 7 lists *not set* among the non-effective states: "Where no grant is set, the host's conservative default applies". FX-19: "OP-C4 … with no grant set → *propose*".
- So the same fixture situation is *effective* in DEL-04-02 and *not set* in DEL-04-01.
- The settings-in element (DEL-04-02 §6 = DEL-04-03 §8) has no slot for a default's basis. It offers only "requester (person, or agent via A8)" and "setting actor (the person, only where an A12 exists)".
- **Change:** as the X-4 amendment in §4.

**IR1A-06 — Undo and act lapse (P §4.5) contradicts S6 and L-6; the relation names differ.**
- P §4.5: "Undo does not erase or lapse an earlier act record; the reversed item's standing shows 'applied, then reversed by ⟨receipt⟩'."
- This holds for A5 on the reversed change item, whose change-item identity is unchanged.
- It is wrong for A4/A6/A7 bound to rows the undo changes. V4-HI-32/S6 and DEL-04-03 L-6 require those to lapse. Example: C T16–T17, where an A4 on S-4 before RC-3 would lapse.
- The relation is "reverses ⟨receipt⟩" in P but "*undoes ⟨entry⟩*" in DEL-04-03 §5/OE-6.
- **Change P:** "Undo never erases an act record. A5/A10 on the reversed item keep their binding and are not lapsed. Acts bound to subject content that the undo changes lapse under the ordinary rule." DEL-04-03 adopts P's relation (reverses ⟨receipt⟩, plus the entry link). This input goes to IR1-B's X-5.

**IR1A-07 — Fixture divergence in the policy and record files (X-6).**
- DEL-04-01 cites "DEL-03-01/C-v0.1 §4.1 and §10" (header line 13).
  - Its §7 and §13 fixtures use proposal P-1, a support "S-5" and **OP-C5 "Adjust run node elevation"**, but C-v0.2 OP-C5 is "Set support stiffness".
  - FX-27 puts the S-2 edit at r13 with S-3 as control. C's timeline has the S-3 edit at r13 (T6) and the S-2 edit at r15 (T14).
  - FX-22 invokes a "reliance operation", which is not in C §10.2.
  - FX-06 (A5, then stale at application) is not on C's timeline. It is legitimate but undeclared.
  - The §13 preamble declares only OP-X1, FX-Professional-P and CP-1…3 as divergences.
- DEL-04-02 §11 and DEL-04-03 §12 declare local labels, as they were required to.
  - DEL-04-02 F9 "host checks passed: spacing (r13)" turns the OP-C3 agent examination (C: "findings … (A3)") into a host check. The host checks in C are "equilibrium" and "unit consistency". This is exactly the R-4 confusion the file forbids.
  - DEL-04-03 E1 binds OP-C4 "Add support" items to existing supports S-3/S-4.
- **Change:** all three re-point to C §10.
  - Proposal fixtures use T5–T13 (PR-1/PR-2, item 1 add support at 4.2 m, item 2 S-3 stiffness).
  - A4 and lapse use T2/T6/T14.
  - A12 uses T15; direct application and undo use T16/T17.
  - Stale-after-accept stays as a declared local divergence.
  - F9 uses a named host check.

**IR1A-08 — "Perform or record" in the reserved-operation rule (X-1); A10 missing from P-02.**
- The same wording appears in:
  - DEL-04-01 P-02 and §5.3 rule 3;
  - C §3.1 rule 1;
  - LOOP §2.2;
  - PANEL K-4 ("perform or record A4").
- It reserves any operation that *records* the person's act, while A9 lets an agent faithfully record one. DEL-04-01 F-7 reconciles the two only by an unstated placement assumption.
- C rule 1 and OP-C8 also reserve A10-performing operations. DEL-04-01 P-02 and §5.3 rule 3 list "A4–A7, A12 or A13" only (P-01a covers A10 as an act, not the operations).
- **Change:** as the X-1 amendment in §4. Add A10 to P-02 and to rule 3.

#### MINOR

- **IR1A-09 Lapse sequence at a checkpoint.**
  - DEL-04-01 §4.3 and PANEL W-5e: "A lapse before the run resumes returns the checkpoint to *waiting*".
  - DEL-04-02 §4, DEL-04-03 L-12 and WD §4.3.4: the disposition becomes **lapsed**.
  - State one sequence in DEL-04-01: a lapse event is always recorded; the disposition becomes *lapsed*; before resume it re-enters *waiting* for a new act on current content; after resume, re-hold is DEL-02-03's.
- **IR1A-10 A8 on a reserved call.**
  - LOOP TL-5: "The call to a reserved entry is recorded as an A8 request" (automatic).
  - C §4.1/P §2: "an A8 *request* is offered".
  - DEL-04-01 §6 row 7: "An A8 request to the person".
  - Align on *offered*. An A8 exists only when the agent actually issues it, with the requester identified. A failed call is not silently turned into a request put to the person.
- **IR1A-11 Accepted, then refused as stale (X-8, IR1-B's).**
  - P §4.2 settles it: A5 stays bound, the item is not applied, re-draft is a new item. It is labelled INTEGRATION.
  - DEL-04-03 U-09 still says "disposition of A5 on that path open". DEL-04-02 §8 and PANEL §3.3 ("Unresolved") have no display rule.
  - DEL-04-02 should add "accepted by ‹person›; refused — stale (relied/current bases); not applied". DEL-04-03 should close U-09 by citing P §4.2 (host evidence stays DEP-001).
- **IR1A-12 Record-shape details.**
  - DEL-04-01 §2.1 A9 lists "the person" as a possible recorder, while §2.4 makes "recorder named as decision actor" non-conformant. DEL-04-03 §6.1 excludes the person as recorder. State that self-recording is *direct capture* by the capturing surface.
  - DEL-04-01 §2.4 omits A13 from the non-conformance list; DEL-04-03 HA-2 includes it.
  - DEL-04-03 §3 counts A11 as a human act without the condition "when the person is the proposer".
  - DEL-04-03 §6.1 *act class* omits A10 and states A5 as reserved unconditionally (its §0 states it correctly).
  - DEL-04-03 §6.1 *act kind* "A1–A14" should exclude A9, which is a recording act (the recording mode element carries it), and A14, which is never a human-act record (X-3).
- **IR1A-13 Lapse vocabulary.**
  - C §6.2 claims "DEL-04-03 vocabulary" but omits "matches c₀ again after observed lapse" (DEL-04-03 §7; DEL-04-02 §8).
  - Add *superseded* for A12/A13 after X-13.
- **IR1A-14 "Treatment" is overloaded.**
  - DEL-04-01 §5.2 uses treatment = execute · apply directly · propose · request the person's act.
  - DEL-04-02/04-03 use "treatment (direct / propose)" for the grant value.
  - Rename the latter *grant value* (DEL-04-01 §5.4 already speaks of "the grant value **propose**").
- **IR1A-15 DEL-04-03 inventory additions.**
  - R3, R5a and R13 go beyond the SoW REQ-002/SOW-186 inventory. They are sourced from R-10, R-7 and D3.
  - Mark them as additions with their source. VC-02 should accept "not applicable" with a reason, for example R13 in host runs (LOOP A-5: no A14 in the host loop).
- **IR1A-16 Over-claimed standing labels.**
  - DEL-04-01 P-04 standing reads "Adopted decision: DECISION-1 D3. The App never answers A14 affirmatively by rule…". D3 rules only that modes remain the user's Codex setting and that hosts have no classifier mode. The App-rule restriction is R-2 (DERIVED/INTEGRATION) and should be labelled so.
  - A13 "enable **or disable**" is marked ADOPTED D2e, but D2e names only "enabling external-agent access". Label the reservation of disabling DERIVED or PROPOSED.
  - See also the SETTLED label on the fifth class value (IR1A-01).
- **IR1A-17 FX-16.** "The person performs A12 granting direct for [a no-policy-basis class]" has no display state. Under W-e the control should refuse the setting, giving *refused (reason: no policy basis)* in DEL-04-02 terms. Rewrite FX-16 to that, and add the same case to DEL-04-02 F1/F3b.
- **IR1A-18 Run ended while waiting (X-12, IR1-C's).** WD §4.3.4 keeps *waiting* plus a run-ended event. DEL-04-03 R8 has only "Not observed → *not reached*", and LOOP's "Run ended" event exists. Add the run-ended event to R8 and to DEL-04-02 §4.
- **IR1A-19 R13 feed path.** HOSTING S-7 sends settlements "to DEL-04-03 through DEL-01-02", and DEL-01-02 is outside this undertaking under D1. R13 is well defined, but in this undertaking it is fed only by DEL-01-01's observed facts. Record the hold in DEL-04-03 U-10.
- **IR1A-20 SoW text vs rulings.**
  - All three SoWs (DEL-04-01 TBD-001/002, AC-004, VER-004; DEL-04-02 TBD-001/002; DEL-04-03 TBD-001) still read OI-001/OI-002 as OPEN.
  - The designs correctly carry DECISION-1 and do not edit the SoWs.
  - This is a pointer reconciliation for C1, not a design defect. Note it in each design's findings so VER-004/VER-006 reviewers are not surprised.
- **IR1A-21 Closable holds.**
  - DEL-04-01 U-11 is closable by LOOP TL-5 (IR1A-02).
  - DEL-04-02 U-03 and DEL-04-03 U-03 ("supplier elements taken from R1_RESOLUTIONS … confirm at IR1") are confirmed by §3.1 above, except the items listed there.
  - DEL-04-01 U-07 and DEL-04-03 U-10 point at each other for A14 placement; X-3 closes both.

## 4. Positions on assigned R2 items

**X-1 — "perform or record" vs A9. Position: AMEND.** Suggested wording:

> An operation is **reserved to the person** when its effect is to perform,
> through the capturing surface, an act of kind A4, A5, A6, A7, A10, A12 or
> A13. This includes creating or changing the host's own act state for that
> act, such as a row's checked state or an item's acceptance disposition.
> Faithful recording (A9) is never performed through such an operation.
> App-side A9 records are DEL-04-03 files, not catalog operations. If a host
> offers an operation that stores an agent's faithful record, that operation:
> - must not create or change act state;
> - must cite the capturing surface's evidence;
> - carries recording mode *faithful recording* with the agent as recorder;
> - never satisfies a checkpoint by itself;
> - takes its class from ordinary policy (*no policy basis* until assigned).
>
> Whether any host offers such an operation is a DEP-001 relay question.

- Apply this in DEL-04-01 P-02 and §5.3 rule 3, C §3.1 rule 1, LOOP §2.2 and PANEL K-4.
- Close DEL-04-01 F-7.
- The proposed treatment's phrase "attribute an act to the person as performed in the host" is too loose. A faithful record also attributes a performed act to the person. The line is *performance* (act state), not attribution.

**X-2 — Name and disposition of the negative event. Position: AMEND.**
- Canonical name (DEL-04-01): **act-declined event**, not bare "decline event". This avoids the A14 settlement state `declined` (HOSTING §6) and P §4.1's "declined the item".
- Scope: required act A4, A6, A7 **or A12** (IR1A-03).
- Elements: actor (the person); declined act kind; bound subject; time; evidence from the capturing surface, where faithful records are permitted as record shape (WD I-6).
- It never records the declined act as performed.
- Disposition: **resolved negatively** — agree.
- Remove "/stop". Stopping the work (V4-EXE-01) is a separate person action. It produces a run-ended event, and a waiting checkpoint stays *waiting* (X-12). A person who wants both declines and then stops, and both events are recorded.
- Sweep: DEL-04-02 §4/§9 DS-5, DEL-04-03 §3/HA-8/R8, LOOP §2.3, PANEL W-5d, WD §4.3.1/§4.3.4, and P §4.1 "declined the item" → "rejected the item (A10)".

**X-3 — A14 settlements recorded in R13. Position: AGREE, with two additions.**
- A14 settlements are recorded only in run-record element R13:
  - never in R6;
  - never as a human-act record of any kind, including A14 itself;
  - never as a grant entry.
- R13 carries the settlement origin as HOSTING states it: the person via interaction with the actor reference as supplied; the user's Codex mode inside the supplier; an App named-rule decline or error.
- Close DEL-04-01 U-07 and DEL-04-03 U-10, which currently each defer to the other.
- Additions:
  - DEL-04-03 §3/§6.1 remove A14 from the human-act kinds (IR1A-12);
  - R13 is "not applicable" in host-loop runs (LOOP A-5);
  - its feed in this undertaking is DEL-01-01's observed facts only, because DEL-01-02 is outside D1 (IR1A-19).

**X-4 — Effective grant from the policy default without A12. Position: AGREE, amended to close IR1A-05.**
- Add the display state **effective (policy default)**. It needs no A12. Settings-in carries:
  - setting actor *none — policy default*;
  - requester *none*;
  - the governing DEL-04-01 policy-class record and its default value (for example P-03 *propose*) in place of the A12 reference.
- **effective (person-set)** requires an A12 reference plus control confirmation.
- A person-set state without A12 is a defect.
- *not set* means no person setting **and** no default. Its treatment follows DEL-04-01 rule 5 / U-06.
- A default can open the direct branch only where a policy-class record's default is *direct* with a decision basis. No such record exists in the first increment (P-03 default is *propose*; other defaults are U-06).
- Apply in DEL-04-01 §5.1/§5.3 rule 7/FX-19, DEL-04-02 §3/§6/F1, DEL-04-03 R6/§8, and P §3.3 (standing at drafting).

**X-13 — Binding and lapse for an A12 checkpoint subject. Position: AGREE, amended; keep PROPOSED.**
- **Binding.** The A12 act binds to the **grant-setting content** it sets: operation class(es), grant value and scope. It does not bind to a settings version identity.
  - The version the control establishes (or its refusal) is a *relation* on the record.
  - At an A12 checkpoint, the subject referent is the setting content named at arrival, for example the agent's A8-requested setting (WD SB-4).
  - An A12 on different setting content is recorded but does not satisfy that checkpoint.
- **No lapse.** A12/A13 are not lapse-evaluated (L-1 does not apply).
  - A later A12 on an overlapping class and scope, or a later A13, **supersedes** it. The record shows *superseded by ⟨act⟩*.
  - A checkpoint the earlier act performed stays *performed*, with the supersession shown.
  - The operations that follow are governed by the grant state in force at route decision and application, as today.
- **Held for DEL-02-03 (W7).** Whether an A12 checkpoint whose setting is then *refused* by the control counts as performed. The act exists but establishes nothing.
- **Apply:**
  - DEL-04-01 §2.5 (keep PROPOSED; close F-9 into it);
  - DEL-04-03 §6.1 bound subject and c₀ for A12/A13, plus a new L-0 "A12/A13: supersession, not lapse", and E7;
  - DEL-04-02 §8 human-act facet adds *superseded*;
  - WD SB-4/U-27;
  - C §6.2 lapse list (IR1A-13).

**X-15 — Propose available with no policy basis vs REQ-004. Position: AGREE with the reading; AMEND the wording.**
- "Produces no effect" is inaccurate. An accepted proposal is applied.
- Suggested wording:

  > For a *no policy basis* class, proposing (A1) remains available because
  > proposing is agent-available for any change (S3). It confers no
  > permission. The proposal itself changes nothing. Any effect requires the
  > person's reserved A5 (D2b) and application through the host route.
  > Direct application is *not permitted*. An A12 attempting to widen the
  > class is refused (W-e).
  >
  > REQ-004's hold applies to **production** and is not lifted. No policy
  > configuration, catalog class assignment, permission-policy
  > implementation or connected-operation integration that depends on the
  > value proceeds until the decision (OI-021). Records and displays show
  > "no policy basis — held (OI-021)". Fixtures report such cases as
  > **held**, never as passes. P-06 stays labelled INTEGRATION.

- LOOP O-4 should label the rule INTEGRATION (R-3.5) rather than cite V4-HI-41 alone.

**Observations on items assigned elsewhere** (input for IR1-B/IR1-C, not positions):
- X-5: agree that undo goes through the one route, subject to the IR1A-06 correction on lapse.
- X-6: see IR1A-07 for the 04-xx specifics.
- X-8: see IR1A-11.
- X-12: see IR1A-18 and the "/stop" split in X-2.

## 5. SoW-fidelity findings

- **DEL-04-01.**
  - Every REQ-001…REQ-007 obligation is represented:
    - REQ-001 in §5 and §4.4;
    - REQ-002 in §2;
    - REQ-003 in §9, FX-14/15 and S4;
    - REQ-004 in P-01…P-06 with host naming and enforcement;
    - REQ-005 in §9;
    - REQ-006 in §5.6 and §7;
    - REQ-007 in §11.
  - OUT-002 "by operation and consequence" stays partly open through U-02, which is correctly held.
  - No wire, transport or placement is selected.
  - Tension: REQ-004 "omission or an unresolved value shall not be treated as permission" against P-06. See X-15.
  - The SoW's TBD-001/002 wording predates DECISION-1 (IR1A-20).
- **DEL-04-02.**
  - REQ-001…REQ-007 are covered: §3/§5, §6, §7, §8, §9, §10 and the verification cases.
  - OUT-001 (CODE) and OUT-003 (TEST) are correctly limited to design.
  - No scope is added beyond the R-8-derived display states. Undo is a change through the one route; P confirms this.
- **DEL-04-03.**
  - REQ-001…REQ-006 and AC-001…AC-007 are covered.
  - The REQ-005 consumer list (PKG-02, PKG-03, PKG-06, DEL-04-02, DEL-09-11, host) is complete in §10.
  - R3/R5a/R13 are additions (IR1A-15).
  - No serialization or algorithm is selected, and `⟨…⟩` is explicitly opaque.

## 6. Over-claiming and standing

- **No file claims:**
  - implementation;
  - qualification;
  - host delivery or adoption (each defers to DEP-001);
  - a performed human act.
- Fixtures are labelled invented, and results "designed, not run".
- The DECISION-1 record in DEL-04-01 §8.2 truthfully shows actor ≠ recorder, and custody without a platform timestamp.
- **Over-claimed labels:**
  - P-04 attributes the App-rule restriction to D3;
  - A13 "disable" is labelled ADOPTED;
  - the fifth class value is labelled SETTLED.

  See IR1A-16 and IR1A-01.
- C, P, LOOP and PANEL correctly mark the reserved-operation rule DERIVED and P-06 INTEGRATION.

## 7. Prioritized R2 repair list

| # | Item | Files to change | Finding / R2 |
|---|---|---|---|
| 1 | One fifth class value *no policy basis* with a reason sub-element; LOOP lists five values; label it INTEGRATION | C §3.1, §4.1, §10.2; P §2, §4.4; LOOP §2.2; 04-01 §5.1 | IR1A-01 |
| 2 | Reserved-act operation rule restated as act-state performance; A10 added; the A9 route kept out | 04-01 P-02, §5.3 r3, F-7; C §3.1 r1; LOOP §2.2; PANEL K-4 | IR1A-08 / X-1 |
| 3 | Reserved entries offered, never "not exposed" for a class reason; FX-35 rewritten; U-11 closed | 04-01 §6 r8, FX-35, U-11 | IR1A-02 |
| 4 | Act-declined event named, scoped to A4/A6/A7/A12, separated from stopping the run | 04-01 §2.3; 04-02 §4, DS-5; 04-03 §3, HA-8, R8; LOOP §2.3; PANEL W-5d; WD §4.3; P §4.1 wording | IR1A-03 / X-2 |
| 5 | *effective (policy default)* state and default-basis slot in settings-in; *not set* redefined | 04-01 §5.1, §5.3 r7, FX-19; 04-02 §3, §6, F1; 04-03 R6, §8; P §3.3 | IR1A-05 / X-4 |
| 6 | A12 binds to setting content; supersession replaces lapse; *superseded* display | 04-01 §2.5, F-9; 04-03 §6.1, L-0, E7; 04-02 §8; WD SB-4, U-27; C §6.2 | IR1A-04 / X-13 |
| 7 | Undo lapses subject-bound acts on changed rows; one relation name | P §4.5; 04-03 §5, OE-6 | IR1A-06 / X-5 |
| 8 | Re-point fixtures to C §10; fix OP-C5, the r13/r15 labels and F9 "host checks passed: spacing" | 04-01 §7, §13; 04-02 §11; 04-03 §12 | IR1A-07 / X-6 |
| 9 | X-15 wording in 04-01 F-5 and P-06; "held" fixture outcome; FX-16 → refused (reason) | 04-01; 04-02 F1; LOOP O-4 label | X-15, IR1A-17 |
| 10 | R13 confirmed; U-07/U-10 closed; A14 and A9 excluded from human-act kinds | 04-01 U-07, §10.2 V-25; 04-03 R13, U-10, §3, §6.1 | X-3, IR1A-12, IR1A-19 |
| 11 | Accepted-then-stale display; U-09 closed | 04-02 §8; PANEL §3.3; 04-03 U-09 | IR1A-11 / X-8 |
| 12 | Lapse-before-resume sequence; run-ended while waiting | 04-01 §4.3; 04-02 §4; 04-03 L-12, R8; PANEL W-5e | IR1A-09, IR1A-18 |
| 13 | Minor alignments: A8 "offered"; C lapse vocabulary; "grant value" term; standing labels on P-04 and A13 | LOOP TL-5; 04-01 §6 r7; C §6.2; 04-02, 04-03; 04-01 P-04, A13 | IR1A-10, -13, -14, -16 |
| 14 | Note SoW TBD/AC wording vs DECISION-1 for C1 | findings sections only | IR1A-20 |

Items 1–8 are MAJOR and should land in R2 before receivers rely on the joins.
Items 9–14 can land in the same pass or be carried as listed findings.

## 8. Statement

The v0.2 policy and record set is fit to merge as v0.2 drafts. There are no
BLOCKING items. The MAJOR items above are cross-file alignment repairs for R2.
None requires an owner policy decision beyond those already in DECISION-1,
except the item held for DEL-02-03 under X-13 (whether a refused A12 counts at
a checkpoint) and the DEP-001 relay question under X-1.
