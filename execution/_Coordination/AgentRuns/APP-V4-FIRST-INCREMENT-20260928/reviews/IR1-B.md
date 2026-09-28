# IR1-B — Independent review: catalog and proposal joins (v0.2)

- Run: APP-V4-FIRST-INCREMENT-20260928, node IR1-B
- Reviewer: Type 2 reviewer (Claude Code `Agent` subagent). It does not delegate
  and authored none of the reviewed files.
- Scope (BRIEFS.md, IR1-B):
  - DEL-03-01/C-v0.2 and DEL-03-02/P-v0.2, checked against DEL-04-01, DEL-04-02,
    DEL-04-03, DEL-05-01, DEL-05-02 and DEL-02-01;
  - the shared fixture FX-PIPE-01 (C §10), checked against every file that
    cites it;
  - R2 items X-5, X-6, X-7, X-8 and X-9.
- Standing: this is a review record. It is not a design change, an owner
  ruling, an acceptance or a human act. Severity uses BLOCKING / MAJOR /
  MINOR. "Change side" names the file that should move.
- Note on independence: W3 drafted both C and P, and the same executor
  repaired them together at R1 ("co-revised in this run", C header). Like
  LOOP↔PANEL, the C↔P join has had no independent v0.2 check before this
  review.

## 0. Files reviewed

The files were read from the worktree. The run inputs were compared by
sha256, and the two SoW hashes match the values in the C and P headers.

| File | sha256 |
|---|---|
| DEL-03-01 `Design/CATALOG_AND_READ_BASIS.md` (C-v0.2) | 358182b18b1fe13f9af6e6f5a61c9ed57f91b6ab29ea0c9adab06fe0081d6d82 |
| DEL-03-02 `Design/PROPOSAL_LIFECYCLE_AND_OUTCOMES.md` (P-v0.2) | 942c1a3ab5ad7bda865640067f0fd550d7cfd1acd8f6ee228f6906452adf8c89 |
| DEL-04-01 `Design/ACT_AND_POLICY_CONTRACT.md` (ACT-POLICY-v0.2) | e50f1fe2f5bb2e3280bc62175e5aeeaa4508eed713424d82c54536a9fb5993a9 |
| DEL-04-02 `Design/AUTONOMY_AND_STANDING_EXCHANGE.md` (AS-v0.2) | 3a4e8b01366c229c463f805aef402edd378a9491ed692f778b89b94a777a329c |
| DEL-04-03 `Design/RECORD_SEMANTICS.md` (RS-v0.2) | 56a3f839f5133813d18fe630bcedf7b30cab8f72e815e9d174f87b0994e21c69 |
| DEL-05-01 `Design/LOOP_RECEIVING_CONTRACT.md` (LOOP-v0.2) | 1151d432c106ed3c1980918eca9d9360116292e3b9c602ed67f4c2d6718762c9 |
| DEL-05-02 `Design/PANEL_RECEIVING_CONTRACT.md` (PANEL-v0.2) | 0a8a0dbe18ed3e6cc893003e41c4b70b6bbae288d2c02a99d7044c00d719a700 |
| DEL-02-01 `Design/WORKFLOW_DECLARATION.md` (WD-v0.2) | c25bccc5f3ac02c84522148eeaa8a6ef0f5eb4a380686773cff45f57a448a55c |
| DEL-02-01 `Design/EXAMPLES.md` (WD-EX-v0.2) | 50b7600de8503f51f440e5947ebd4ea7a559781e2497d5d880a8d683f7a9c43e |
| DEL-01-01 `HOSTING_BOUNDARY.md` / `PIN_SPIKE_0.158.0.md` | 16711a83…c84007a / 26ea0c2f…b40334. Grepped only: neither cites FX-PIPE-01 or C/P fixture entries |
| DEL-03-01 `ScopeOfWork.md` | 179a6d355d84dba915daddd746d9d62eb7c8ef483e68122a096dfbde6f6b3b84 (matches the C header) |
| DEL-03-02 `ScopeOfWork.md` | 42328987c71dd243323805faf2634067cca0113b81ca93d4d129193b2a71128a (matches the P header) |
| OWNER_DECISIONS.md | f3f8e5f31ec87006fc9ab459c6ae57d08638439c234fa959ba2605914cf81f2e |
| R1_RESOLUTIONS.md | 2f9c7e72aa8362624ad830377a70077b27a27bf03871f8e87811a28e6e177ec4 |
| R2_CANDIDATES.md | fa99768452e7b2049de0f43318f544ae34e2ca8706f2e638b82948c164f73c1b |
| BRIEFS.md (working copy) | 8ae84cf046e12c21972937065ed81b96a7913724e264b3f889423cb767493966 |

The v0.1 comparisons (V1-A, V1-B, V1-C) were used for history only.

## 1. Summary

| Severity | Count |
|---|---|
| BLOCKING | 0 |
| MAJOR | 10 (B-M1…B-M10) |
| MINOR | 13 (B-m1…B-m13) |

**Verdict.** The set is **fit to merge as v0.2 drafts**. No BLOCKING item was
found. The v0.2 files keep their DRAFT standing and do not claim
implementation, host delivery, SWBPIPE adoption, qualification or any human
act. Most R1 resolutions do hold at the C/P joins. The MAJOR items are
disagreements *between* v0.2 texts. Each has a clear side to change, and R2
should repair them before V2 or W7 consumers rely on the joins. Three
clusters matter most:

- the acceptance-checkpoint override (its outcome and its carriage);
- the class vocabulary and exposure semantics;
- the shared fixture, which most consumers have not yet adopted.

## 2. Join-by-join: R1 resolutions that hold, and residual disagreement

### 2.1 C ↔ P (single-author pair; M1-C/M1-P and M3-CP)

| R1 item | Holds in both? | Evidence |
|---|---|---|
| R-6 change-item content identity built from C elements | Yes | C §3.3 "Subject content identity availability"; P §3.1 row "Change-item content identity"; C §9 table row → P §3.1 |
| R-6 subject content identity and method designation | Yes | C §5.1, §5.3; P §3.2 rows "Relied-on basis reference", "Subject content identities" |
| R-7 §4.1 / §9 canonical outcomes, evaluated basis on non-success | Yes, with naming nits (B-m4) | C §4.1 "canonical with P §9"; P §9 carries every C §4.1 result |
| Relied-on basis carried unchanged; later basis recorded separately | Yes | C §5.4; P §3.2 and §5 "No silent refresh" |
| Applied-outcome association (V1-B D-22) | Partly. Resulting objects are missing (**B-M6**) | C §9; P §9 "applied (receipt)" |
| R-9 generation = lineage epoch; an edit changes the model revision | Yes | C §5.1; P §5 trigger; C Tg |
| M3-CP return (T3→T13) | Steps agree | C §9 and VC-C-04; P §11. Retry at T13 conflicts with P §5 (**B-M7**) |
| Acceptance checkpoint forces proposal | C defers to P §4.4. P §4.4 is ambiguous on the direct-request outcome (**B-M2**) | C §3.1 rule 3; P §4.4 |
| Class values | Both use "policy basis pending", which diverges from DEL-04-01 (**B-M1**) | C §3.1; P §2 |

**B-M7 (MAJOR): retry vs stale vs one effect, own-effect revision advance.**
Change side: P, and C §10.3 T13.

- P §5: "A retry resubmits the same proposal identity and content without a
  new read; if its basis no longer holds it is refused stale like any
  submission."
- P §7: "a repeat reports the existing state (queued, applied with the *same*
  receipt, etc.)".
- C T13 (r14): "agent resubmits PR-2 (same proposal identity) → repeat
  reports RC-1".

PR-2 relies on B2 (r13), and its own item 1 moved the model to r14 at T12.
Under the "any model revision" reading of U-C3, the §5 rule refuses the T13
retry as stale. §7 and T13 instead expect it to report RC-1. The same problem
arises when accepted items of one proposal are applied separately (U-P7): the
first item's application would stale its siblings.

Proposed repair:

- P states precedence. A resubmission of a proposal identity the host
  already holds (queued, decided or applied) reports the existing per-item
  state and is not re-validated. The stale check applies to a first receipt
  and to application of a not-yet-applied item.
- U-C3 names the own-effect case explicitly: a revision advance caused by the
  same proposal's own applied items. Whether it counts is a host input, but
  the contract must say which default fixtures assume.

Host evidence stays DEP-001.

**B-M6 (MAJOR): the applied-outcome association does not identify the
resulting objects.** Change side: P §9 and §3.4, with C §9 forward table.

P §9 defines the association as "proposal/item identity, relied-on basis,
receipt reference, resulting revision". Several consumers need to know which
objects the application created or changed, and their post-application
subject content identities:

- C OP-C4 promises "new support identity; applied-outcome association" (C
  §10.2);
- WD SB-1 binds rows "by the receipt that produced or changed them";
- WD E1 `CP-check` has the subject "rows created or changed by the receipt";
- LOOP §2.4.1 kind (c) binds "to the rows produced, as the outcome identifies
  them".

A created support has no identity at drafting. P §3.4 "Affected object" is
therefore only a description ("new support on R-100 at 4.2 m"), and nothing
in P carries the identity the host assigns.

Proposed repair:

- Add *resulting objects* to the association: identities created or changed,
  with their subject content identities and method designation where the
  host supplies them. Otherwise record "not supplied" as an evidence limit.
- Whether the receipt itself carries them remains a host observation.

### 2.2 P → DEL-04-03 (outcomes, receipt links, origin)

| R1 item | Holds? | Evidence |
|---|---|---|
| R-7 adoption of P §9 and C §4.1 unchanged | Yes in substance | RS §5 outcome table, with every P §9 row present |
| Per-submission recording; one effect is a host obligation | Yes | RS OE-3; P §7 "Recording" |
| Retry keeps identity; re-draft is new with lineage | Yes | RS OE-2 and OE-4; P §3.1 and §5 |
| Receipts linked, not copied; host origin mark linked | Yes | RS FA-3, §5; P §3.3 closing paragraph |
| Two settings references | Yes | RS §5; P §3.3 |
| R-6 A5/A10 c₁ = change-item content identity; application does not lapse | Yes | RS L-1, L-10; P §3.1 rules 2–3 |
| Stale after acceptance (was U-P3) | P decided it; RS still holds it open (**B-m2**) | P §4.2 "The recorded A5 stays bound … not lapsed; the item is not applied"; RS U-09 "disposition of A5 on that path open" |
| Undo | Relation names differ (**B-m3**) | P §4.5 "reverses ⟨receipt⟩"; RS OE-6 "*undoes* ⟨entry⟩" |

Residual MINOR items:

- **B-m4**: RS says "stale (refused)" where P says "refused — stale". RS uses
  "reporter" where P uses "observer".
- **B-m8**: RS §5 folds "author identity (seat/role instance)" into one
  element, while P §3.3 keeps author identity (seat instance) and seat role
  meaning separate.

### 2.3 P → DEL-04-02 (direct branch, grant in force)

| R1 item | Holds? | Evidence |
|---|---|---|
| R-8 direct branch only in *effective* + direct | Yes | AS §3 table "Direct branch?"; P §4.4 entry condition |
| Two settings references; application reference host-reported or *unconfirmed* | Yes | AS §5 step 4, §7; P §3.3 |
| Narrowing and widening in flight (R-3.6/3.7) | Yes | AS §5 steps 4–5; P §4.2 |
| Abstract host contribution (origin, undo, later-check, receipt) | Yes | AS §7; P §4.4 bullet 2 |
| Undo = a change through the one route; *undone* = applied (receipt) | Yes. AS asked P to confirm, and P §4.5 does | AS §7 "Undo interaction"; P §4.5 |

Residual items:

- **B-m3**: AS §8 "Route and outcome" has no "applied, then reversed by
  ⟨receipt⟩" standing, although P §4.5 requires it.
- **B-m13 / X-8**: there is no display rule for an accepted item later
  refused as stale.
- **B-M8**: AS F9 "host checks passed: spacing (r13)" treats OP-C3 spacing as
  a host check. C does not.

### 2.4 DEL-04-03 ↔ DEL-04-02 (M3 exchange; reviewed only where C/P elements are carried)

- RS §8 and AS §6 are textually identical.
- The C/P elements they carry agree with C and P: c₀/c₁ with method, bound
  subject, evaluated/relied/current bases, and item dispositions.
- IR1-A owns the rest of this join.

### 2.5 C → DEL-04-03 (content identities and lapse)

| R1 item | Holds? | Evidence |
|---|---|---|
| R-6 three c₁ sources; L-2 compares method designations | Yes | RS L-1, L-2; C §5.2 rule 6, §5.3 |
| Unrelated edit does not lapse a subject-bound act | Yes | C §5.3 bullet 2 and §10.6; RS L-1, E4 |
| Generation or restore handling left open | Yes, consistent | C U-C2 and Tg; RS L-11 and U-12 |
| Lapse vocabulary by reference | Partly (**B-m1**) | C §6.2 lists seven states. RS §7 and AS §8 list eight: C omits "matches c₀ again after observed lapse" |

### 2.6 C/P ↔ DEL-04-01 (policy supplier)

| R1 item | Holds? | Evidence |
|---|---|---|
| R-1 canonical names A1–A14; A10 reserved wherever A5 is | Yes | C §3.1 rule 1; P S-P14 and §10; ACT §2.1 |
| R-2 reserved-act operations; SWB model change DERIVED with default propose | Yes | C §3.1 rules 1–2 and OP-C6/C7/C8; P S-P14; ACT P-02, P-03 |
| R-3 map: not permitted + A8; no silent conversion | Yes in general. Not at the checkpoint override (**B-M2**) | C §4.1; P §2; ACT §6 rows 6–7 |
| R-4 labels | Yes in C and P. The shared fixture use differs (**B-M8**) | C §6.2; P §10 |
| Class vocabulary | **No** (**B-M1**) | See below |
| Reserved entries and exposure | **No** (**B-M4**) | See below |

**B-M1 (MAJOR): class vocabulary name and extent.** Change side: C §3.1, P §2
and §4.4, and LOOP §2.2. Owner of the vocabulary: DEL-04-01 (ACT V-02).

The quoted texts:

- ACT §5.1: "none | may apply within granted autonomy | proposal only |
  reserved to the person | *no policy basis*".
- ACT §5.3 rule 5: "A class is *no policy basis* when it is omitted,
  unassigned, or `UNRESOLVED{OI-021}` for a concrete operation."
- C §3.1: "…or **policy basis pending** (operation-specific addition awaited
  under `UNRESOLVED{OI-021}`)". P §2 uses the same name.
- LOOP §2.2: "The four V4-HI-02 values: *none*; *may apply within granted
  autonomy*; *proposal only*; *reserved to the person*". The fifth value is
  missing, yet LOOP O-4 relies on it.
- AS §2 and RS §8 use "no policy basis".

The C/P value is both differently named and narrower, because it omits
*omitted* and *unassigned*.

Also, C §3.1 "Value standing" (adopted, DERIVED, accepted default setting,
policy basis pending) cannot express ACT §8.1 *decision standing* values
*settled-by-basis* or *INTEGRATION*. P-06 is an INTEGRATION record (**B-m12**).

Proposed repair:

- C, P and LOOP adopt ACT's name and definition.
- C's value-standing list mirrors ACT §8.1.

**B-M4 (MAJOR): whether a reserved entry can be "not exposed".** Change side:
C §2 invariant 5 and ACT §6 row 8 / U-11.

- C §2 inv. 5: "An agent request for it yields *not permitted* (§4.1), never
  *unavailable*, *missing* or *not exposed*".
- ACT §6 row 8: "If offered: invocation → row 7. If withheld: **not exposed
  on this surface** (R-9)". ACT FX-35 treats the withheld case as conformant.
- LOOP TL-5: "The loop does not decide treatment and does not withhold an
  exposed entry on its own reading of its class."

Exposure (C element 9) is a host-declared, per-surface fact. Class is a
policy fact. The two texts conflate them in opposite directions.

Proposed repair:

- C inv. 5 becomes: "class alone never produces *unavailable*, *missing* or
  *not exposed*; exposure is element 9, independent of class. If the host
  exposes a reserved entry, an agent request yields *not permitted* + A8."
- ACT row 8 becomes: "*withheld*" means the host's element-9 value, never a
  loop or adapter choice.
- ACT U-11 is closed by LOOP TL-5.

**B-M2 (MAJOR): outcome of a direct request under an acceptance
checkpoint.** Change side: P §4.4 and §14 E-2.

- P §4.4: "The change is drafted as a proposal whose items are the
  checkpoint's bound subject; the direct branch is not entered."
- P E-2 row: "Workflow checkpoint requires A5 on OP-C4 while OP-C4 is granted
  direct | Drafted as a proposal; run waits for A5".
- ACT §4.4: "A direct request for it is *not permitted* (§6)". ACT FX-29 says
  the same.
- WD I-7 and FB-14: "**not permitted** … never silently converted".
- LOOP C-6: "returns **not permitted**. The loop never converts it into a
  proposal (R-3.3)". PANEL PC-24 agrees.

P is the owner of the canonical outcome taxonomy, and its wording can be read
as the route converting the request, which R-3.3 forbids.

Proposed repair: P §4.4 and E-2 say that a request to apply directly →
*not permitted* naming the forced treatment. The proposer may then submit a
proposal separately, and that proposal's items become the checkpoint subject.

**B-M3 (MAJOR): the carriage of the checkpoint constraint is not a P element.**
This is X-9; see §3.

### 2.7 C/P → DEL-05-01 (loop)

| R1 item | Holds? | Evidence |
|---|---|---|
| R-3.1 treatment on the host route; loop relays intent | Yes | LOOP §6, O-4 to O-6; P §2 |
| R-7 outcomes unchanged; observer-attributed unknown; retry keeps identity | Yes | LOOP TL-2, §6.3; P §4.1 overlay, §3.1 |
| Every dispatch carries origin, seat role and grant in force | Mostly. Reason is missing (**B-m8**) | LOOP §6.2; P §3.3 |
| R-9 catalog edition; entry-version mismatch is a host error | Yes | LOOP O-3; C §7 |
| TL-4 basis, standing and subject identities passed through | Yes | LOOP TL-4; C §5 |
| R-9 *not exposed* distinct from *missing* | **No** (**B-M5**) | See below |
| Class vocabulary | **No** (**B-M1**) | LOOP §2.2 |

**B-M5 (MAJOR): "not exposed on this surface" is both a loop-side class-1
failure and a host class-2 outcome.** Change side: LOOP V-2, MC-5, FX-U3 and
TL-2. C §4.1 also needs a reporter rule.

- LOOP V-2: "named operation offered from edition K and exposed on the
  embedded surface | Loop | Loop-side failure "unknown or unoffered
  operation"". MC-5 lists "not offered or not exposed" under V-2.
- LOOP TL-2 class 2 and TL-5: "An entry not exposed on the embedded surface
  is reported as *not exposed on this surface*".
- LOOP FX-U3: "Rejected at V-2 / reported *not exposed on this surface*".
- C §4.1 lists *not exposed* as a result carrying "Entry identity; surface;
  exposure value" but names no reporter. RS §5 gives "Host / adapter".

Proposed repair:

- LOOP V-2 splits into two failures:
  - *missing / unoffered* (no entry in edition K);
  - *not exposed on this surface* (the entry exists and element 9 says it is
    not exposed). This case is reported by the loop from the host-declared
    element, with the same meaning as C §4.1.
- C §4.1 states that a loop or adapter may report *not exposed* from element
  9, naming itself as reporter.

### 2.8 C/P → DEL-05-02 (panel)

| R1 item | Holds? | Evidence |
|---|---|---|
| R-7 outcome list incl. not exposed and channel not enabled; "accept" wording; refused ≠ rejected | Yes | PANEL §3.3; P §9, §8 |
| Per-item dispositions; derived state never stronger | Yes | PANEL §3.3; P §4.3 |
| Direct only in *effective* direct; forced proposal → not permitted | Yes (PANEL is correct; P needs B-M2) | PANEL §3.3 "Direct autonomy and checkpoints", PC-24 |
| R-6 acceptance unit = change item | Yes | PANEL §3.3 "Acceptance unit"; P §3.1 |
| K-4 reserved | Yes | PANEL K-4; C OP-C6 |

Residual MINOR items:

- **B-m2**: PANEL still holds "accepted-but-unapplied item whose basis fails"
  as unresolved, although P decided the contract rule.
- **B-m8**: PANEL §3.3 origin omits seat role meaning and the two settings
  references.
- **B-m13 / X-8**: the accepted-then-stale display is missing.

### 2.9 C/P → DEL-02-01 (workflow declaration)

| R1 item | Holds? | Evidence |
|---|---|---|
| Tool references opaque to C operation identity; equality-only versions | Yes (C additionally proposes a host compatibility statement, U-C9, consistent with WD U-07) | WD §4.2.2; C §3.2 |
| R-9 exposure outcomes: unagreed → not established | Yes as meaning. It breaks the shared fixture (**B-M10**) | WD §4.2.4; C §3 #9 |
| R-5 forced treatment → not permitted | Yes in WD. P is at odds (**B-M2**). Carriage is open (**B-M3**) | WD I-7, FB-14, U-19 |
| P per-item dispositions and all-items-decided indication for §4.3.7 | Supplied (P §4.3). The mapping is IR1-C / X-14 | WD §4.3.7 |
| Read basis includes method designation | **No** (**B-m9**) | WD §4.1 lists four elements; C §5.1 has five |
| Rows produced are identifiable from the applied outcome | **No** (**B-M6**) | WD SB-1; P §9 |

## 3. Assigned R2 candidate positions

### X-5 — Undo through the one route: **amend**

Confirm P §4.5 as the canonical rule, and add the following.

1. **One relation name.** The name is "reverses". It is carried on the undo's
   applied outcome and names the reversed change's receipt. The run record
   additionally references the reversed entry.
   - RS OE-6 "undoes ⟨entry⟩" becomes "reverses ⟨receipt⟩ (entry ⟨ref⟩)".
   - C T17 already uses "reverses RC-2".
2. **Lapse wording.** Replace P §4.5 "Undo does not erase or lapse an earlier
   act record" with: "An undo erases no act record. An A5/A10 on the reversed
   change item is not lapsed by the undo, because its item content is
   unchanged; the item's standing shows 'applied, then reversed by
   ⟨receipt⟩'. Acts bound to subject content that the undo changes (e.g. an
   A4 on the applied row) lapse under the ordinary rule (RS L-1; V4-HI-32)."
   As written, the P sentence can be read to suppress V4-HI-32 lapse.
3. **Display.** AS §8 "Route and outcome" adds "applied, then reversed by
   ⟨receipt⟩".
4. **Catalog completeness.** C §2 invariant 1 requires an entry for every
   operation a person can perform. The fixture undo at T17 has no OP-C entry.
   Either add a fixture entry (e.g. "Undo change by receipt", class per
   policy) or state in C that host undo is a catalog operation whose entry is
   a host input (U-P8).

### X-6 — FX-PIPE-01 alignment: **amend**

The target is right: every file re-points to the C-v0.2 §10 identifiers. C
must first be made able to carry every consumer's needs. Otherwise re-pointing
forces new local labels. Actual v0.2 state:

| File | Divergence observed | Stated as divergence? |
|---|---|---|
| ACT §7, §13 | Cites C-v0.1 (header line 13). Uses "OP-C5 'Adjust run node elevation'", which C-v0.2 redefined as "Set support stiffness". Proposals are "P-1/P-2", which collide with ACT's own P-01…P-06 records and with the "P" contribution label. Uses "S-5". FX-27 puts the S-2 edit at r13, whereas C has the S-3 edit at r13 (T6) and the S-2 edit at r15 (T14). Adds OP-X1 | Only OP-X1, FX-Professional-P and CP-1…3 are stated |
| RS §12 | Proposal "P-2", "relied basis B2 (r12)" (C: B1 = r12, B2 = r13), items i1–i3 on S-3/S-4/S-5 under OP-C4 "add support" | Yes, stated as pending IR1 |
| AS §11 | S-1…S-5, P-2, ⟨set:n⟩, "OP-X"; "OP-C3 check" | Yes, stated |
| LOOP §0, §11 | R-101/R-102, N-10…N-40, S-7, FX-U2 load-case gesture | Yes, stated as provisional |
| PANEL §0, §7 | R-101/R-102, S-7…S-9 | Yes, stated as provisional |
| WD-EX | `‹read supports›` (= C OP-C1), rows N1/N2/E, OP-C3 "Check support spacing", post-application edit at "r12 → r13", "elevation" attribute (C has none) | Partly (U-26) |
| P | Consistent with C T1–T17 | — |

Amended treatment:

1. **C first** (C §10). Add the following:
   - (a) one entry whose class is *no policy basis*, to serve ACT FX-16 and
     AS F1 "OP-X" (e.g. "Renumber nodes");
   - (b) fixture exposure values (**B-M10**);
   - (c) a settled OP-C3 standing (**B-M8**);
   - (d) an undo entry or statement (X-5 point 4);
   - (e) T15 scope written in R-8 dimensions (**B-m10**);
   - (f) optional named settings versions (⟨set-1⟩, ⟨set-2⟩), which P E-2
     already assumes.
2. **Then every consumer** replaces its local labels with C identifiers and
   T-steps, and cites C-v0.2 by sha256. "P-n" proposal labels become
   "PR-n".
3. **Allowed local labels.** Parse-level, endpoint and responsiveness
   fixtures (LOOP MC/MS/RS, "large model") may keep local labels, and each
   must say why (R-9).

### X-7 — Consumers adopt C §4.1 incl. *not exposed on this surface*: **amend**

Checked result:

- RS §5, PANEL §3.2/§3.3, WD §4.2.4 and ACT §6 adopt it.
- AS adopts it indirectly through P §9. **B-m13** asks AS §8 to list it.
- LOOP adopts it in TL-2/TL-5 but contradicts it at V-2 (**B-M5**).

Amendment:

- C §4.1 adds a reporter rule: host, or a loop or adapter reading element 9,
  with the reporter named.
- LOOP splits V-2 as in B-M5.
- C inv. 5 and ACT row 8 are reconciled as in B-M4.

### X-8 — Accepted item later refused stale displays "accepted, refused — stale": **amend**

Agree, with fuller wording and all affected owners:

- **Display** (AS §8 route/outcome facet; PANEL §3.3 per item): "accepted by
  ‹person› — not applied: refused — stale (relied ‹B›, current ‹B′›)". The A5
  is shown *not lapsed*, still bound to its item content. The item's derived
  state is never "accepted" alone, nor "applied". A re-draft shows no carried
  acceptance.
- **Record** (RS §5): the A5 act record and the application-time refusal
  entry are both present. RS U-09 and PANEL "Unresolved" are narrowed to
  "host evidence that application re-checks the basis (DEP-001)", matching
  P U-P3 (narrowed).
- **Checkpoint consequence.** An A5 checkpoint already *performed* on that
  item stays performed, but the declared output is not produced. This is
  referred to X-14 / DEL-02-03 for how WD §4.3.7 and the hold machine treat
  it.

### X-9 — How "acceptance checkpoint forces proposal" reaches the host route: **amend**

Agree that the constraint travels with the dispatch and the host route refuses
a direct application as *not permitted*. Also agree that it is a DEP-001 relay
question. Amendments:

1. **P must define the element (B-M3, MAJOR).**
   - P §3.3 origin and attribution adds a **governing checkpoint constraint**:
     workflow run identity, checkpoint reference, and the required act A5 on
     this operation's result.
   - P §4.4 says the host route resolves *propose* when the constraint is
     present.
   - Today only LOOP §6.2 carries it ("Checkpoint constraint | Present if a
     declared checkpoint requires A5 on this operation's result").
   - P's §3.3 table has no such element, and ACT §5.1 lists "checkpoint
     state" as an input with supplier "DEL-02-01; DEL-02-03; DEL-05-01" but
     names no carriage.
2. **Every channel.** The external adapter (DEL-03-03) must carry it too. An
   App workflow run through the host's external surface has checkpoints known
   only App-side (DEL-02-03). So the embedded loop is not the only carrier.
3. **Authority limit.** A dispatch-carried constraint is supplied by the
   actor's side. The host cannot tell an omitted constraint from none. The
   relay question should therefore ask whether the host can obtain the
   declaration independently for host-origin workflows. For an App-carried
   run, the omission of a constraint the declaration contains is an App-side
   defect, recorded as an evidence limit (RS R11).
4. **Outcome wording** follows B-M2: *not permitted*, never converted.

## 4. Other residual findings

**B-M8 (MAJOR): OP-C3 standing is read two ways.** Change side: C §10.2 first,
then WD-EX E1/E7 and AS F9.

- C OP-C3 is "Examine support spacing", with the result "findings authored by
  the requester (A3); no human-act standing".
- WD-EX reads it as a host check:
  - "`OP-C3` | Check support spacing (non-mutating check)";
  - "The host's support-spacing result for the run | host result via
    `OP-C3`";
  - "*host checks passed: support spacing* only where the host says so".
- AS F9 has "host checks passed: spacing (r13)".
- C's own host checks at T1 are "equilibrium" and "unit consistency".

Proposed repair: C states that OP-C3 returns a host-computed exceedance table,
a host result with basis and standing. An agent's interpretation citing it is
A3 findings. C also says whether "support spacing" is a named host check
("host checks passed" is only meaningful when no exceedance is reported).
Consumers then align.

**B-M9 (MAJOR): the shared fixture is not yet adopted.** See X-6. This is
listed as its own MAJOR because ACT §7, the SWB default example that DEL-04-01
labels as the accepted default's illustration, still uses the retired OP-C5
meaning and cites C-v0.1.

**B-M10 (MAJOR): fixture exposure values make the shared fixture
unexercisable.** Change side: C §10.2.

- Every C entry has exposure "unagreed ×3".
- WD §4.2.4: "If that element's value is "unagreed", the outcome is **not
  established**".
- LOOP TL-1 offers only entries "exposed on the embedded surface".

Against FX-PIPE-01, then, no WD required tool is *present*, LOOP offers
nothing, and WD E1/E2, LOOP FX-V1/FX-V2 and PANEL PC-05…07 cannot be run.

Proposed repair: C §10.2 carries **fixture-assumed** exposure values (e.g.
"exposed (fixture assumption)" on H/E/X for OP-C1…C5 and C9, plus one variant
entry per non-exposed case). The §8 responsibility map stays *unagreed*,
because the map is about real host agreement and the fixture is not.

MINOR items not already described above:

- **B-m5**: evidence labels differ.
  - LOOP §12 uses CONTRACT-REVIEWED / FIXTURE-EXECUTED / HOST-OBSERVED /
    NOT-OBSERVED.
  - PANEL uses DEFINED / EXECUTED / LIMITED / AWAITING INPUT / HELD.
  - C and P use illustrative / test-double / actual host.
  - Repair: publish one mapping, owned by C per V1-B D-19.
- **B-m6**: the boundary between an availability precondition and a
  validation error is unstated.
  - C OP-C4 treats "location on run" as a precondition ("Location is not on
    run R-100" → *unavailable*).
  - LOOP FX-D1 treats the same kind of condition ("Support at node N-99, not
    on R-101") as *refused* at V-4.
  - Repair: C states the rule. A declared element-4 precondition gives
    *unavailable*, with HI-04 parity. An element-7 error at validation gives
    *refused — invalid*. LOOP FX-D1 re-points to an element-7 error such as
    E-location-occupied.
- **B-m7**: the sibling-drafts rules disagree.
  - P §3.1 rule 5: "separate proposals unless a draft explicitly names the
    proposal it extends".
  - LOOP MC-8: "The loop never merges sibling calls into one proposal with
    items. Items come only from one call's arguments".
  - Repair: both are marked open (U-P9, T-OPEN-1). Align them to one rule
    before FX-M8.
- **B-m9**: WD §4.1 lists four basis elements. C §5.1 has five (with method
  designation).
- **B-m10**: the T15 grant "direct for OP-C9 class scope 'support labels on
  R-100'" is hard to express.
  - OP-C9 shares the model-change class with OP-C4 and OP-C5 ("as OP-C4").
  - "Labels" is not an R-8 scope dimension unless it is expressed as
    consequence, whose vocabulary is U-02 and still open.
  - PANEL PC-22 needs a "low-consequence class" distinct from geometry.
  - Repair: write the scope as object set + consequence (U-02-dependent), or
    give OP-C9 its own host-named class with a stated policy basis. Under ACT
    U-06 and W-e, a class without a policy basis could not be granted direct.
- **B-m11**: two fixtures phrase remedies as UI gestures, contrary to C §4.2.
  - LOOP FX-U2: "select a load case first".
  - WD-EX E7: "no run is selected in the host UI".
- **B-m12**: C §3.1 value standing is incomplete (see B-M1).

## 5. SoW fidelity

**DEL-03-01 (C).**

- Every REQ-001…REQ-007 obligation and AC-001…AC-008 is addressed. No
  obligation was found dropped.
- Additions are labeled as proposed or R1-derived:
  - exposure element 9;
  - catalog edition;
  - open-description invariant;
  - version compatibility statement;
  - non-mutating basis rule;
  - identity method designation (a fifth basis element beside REQ-004's four,
    a superset).
- Owning the one shared Wave-1 fixture (R-9) takes C's OUT-003 beyond its own
  REQs. T11–T17 serve P and DEL-04-x. This is acceptable as an R1
  integration assignment, but C §10 should say so, so it is not read as SoW
  scope.
- No wire name, transport, hash or placement is selected. The §8 mention of
  "MCP server or CLI" describes V4-HI-50 and selects neither.

**DEL-03-02 (P).**

- All thirteen REQs and all twelve scope rows are covered (VC-P-01 map).
- The additions beyond V4-HI-23 are labeled as proposed or INTEGRATION:
  - refused — invalid;
  - application error;
  - stale at application;
  - undo;
  - sibling drafts.
- The additions include no selected mechanism.

**Basis findings for C1** (not design defects):

- DEL-03-01 SoW REQ-002 and TBD-001, and DEL-03-02 SoW AC-013 and TBD-001,
  still describe OI-001/OI-002 as unresolved. C and P correctly apply D2 and
  D3 instead. The SoW text should be reconciled at C1 without changing scope.
- The C↔P M3-CP mirror row (DEP-03-01-026 DOWNSTREAM) is still missing, as
  C §9 and P UNRESOLVED already state.

## 6. Over-claiming and standing

No over-claim was found in C or P:

- Both keep the DRAFT status.
- Host adoption of D2/D3 is "not evidenced" (C §3.1; P S-P14).
- One effect is "a host obligation to be evidenced" (P §7).
- AC-004 is held until an executable return exists (C §9; P §11).
- Every fixture act is labeled invented.

Owner decisions are used correctly:

- D2 is carried as the App/shared list, with host enforcement left to the
  host.
- D3 is applied: no classifier class value, and A14 is App-side only.
- D4 is not invoked.
- Items marked DERIVED match R-2. Items marked INTEGRATION match R-3.5, R-3.6
  and R-6.

In consumer files, the one standing-relevant wording issue is ACT §7. It
presents a fixture built on a retired catalog meaning as the illustration of
the accepted default (B-M9).

## 7. Prioritized R2 repair list (IR1-B scope)

1. **Acceptance-checkpoint override** (B-M2, B-M3 / X-9). P §4.4 and E-2
   outcome wording. P §3.3 gains the governing-checkpoint-constraint element.
   ACT §5.1 names carriage. DEL-03-03 is named as a carrier. The DEP-001 relay
   question is recorded.
2. **Class vocabulary** (B-M1, B-m12). C, P and LOOP adopt ACT "no policy
   basis" and its definition. C value standing mirrors ACT §8.1.
3. **Exposure semantics** (B-M4, B-M5 / X-7). Rewrite C inv. 5. Rewrite ACT
   row 8 and close U-11. Split LOOP V-2. Add the C §4.1 reporter rule.
4. **Applied-outcome resulting objects** (B-M6). P §9 and C §9 forward table.
5. **Retry vs stale own-effect** (B-M7). P §5 and §7 precedence. Fix C T13.
   Name the own-effect case in U-C3.
6. **Shared fixture** (B-M8, B-M10, then B-M9 / X-6). C settles OP-C3
   standing, adds fixture exposure values, a no-policy-basis entry, undo, and
   a T15 scope. Then every consumer re-points: ACT §7/§13 first, then RS §12,
   AS §11, WD-EX, LOOP and PANEL.
7. **Undo** (X-5 amendments; B-m3). Relation name, lapse wording, AS
   "reversed" standing, catalog entry.
8. **Accepted-then-stale display and record** (X-8; B-m2, B-m13).
9. **Remaining MINORs** (B-m4…B-m11) and SoW text reconciliation at C1.

## Verification cases (for this review; designed, not run)

| Case | Procedure | Expected result after R2 |
|---|---|---|
| IR1-B-VC-1 | Grep all nine files for "policy basis pending", "no policy basis" and the class-value lists | One name and one definition (ACT's). LOOP lists five values |
| IR1-B-VC-2 | Trace a direct request under an A5 checkpoint through P §4.4/E-2, ACT §4.4, WD I-7, LOOP C-6 and PANEL PC-24 | *not permitted* everywhere. P §3.3 has the constraint element |
| IR1-B-VC-3 | Trace "not exposed" through C inv. 5, C §4.1, ACT §6 row 8, LOOP V-2/TL-5 and RS §5 | One meaning, with the reporter named. Class never implies exposure |
| IR1-B-VC-4 | Replay C T10–T13 under both U-C3 readings | The T13 retry reports RC-1 under both readings, or the fixture states which reading it assumes |
| IR1-B-VC-5 | For WD E1 `CP-check` and LOOP FX-C1, locate the source of the rows' identities | Found in the P §9 association (resulting objects) |
| IR1-B-VC-6 | Grep consumers for R-101, N-30, S-5, S-7, P-1, P-2, "Adjust run node elevation" and "Check support spacing" | Only stated, justified local labels remain. Citations point to C-v0.2 by hash |
