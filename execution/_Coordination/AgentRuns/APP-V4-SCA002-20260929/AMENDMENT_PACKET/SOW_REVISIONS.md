# SoW revisions — SCA-V4-002, node P1

**Status: PROPOSED (scope-change checkpoint-group-2 preparation). Nothing here
is applied.** Every edit is an exact old → new replacement in one
`ScopeOfWork.md`. It is applied after the owner accepts the amendment, by
`scope-of-work` `MODE=REVISE`, one deliverable per brief, closing with
`MODE=VERIFY` (the same route as SCA-V4-001).

- **Basis:** commit `102f09c1a`. Every "old" block was checked against the
  current SoW bytes. Each occurs exactly once when applied in the listed
  order, and the blocks do not overlap. See "Mechanical checks" at the end.
- **Lifecycle:** DEL-02-01, 02-03, 03-03, 04-02 and 01-01 are IN_PROGRESS.
  DEL-10-03, 09-07, 01-04 and 02-02 are INITIALIZED. REVISE admits both.
  None is CHECKING or ISSUED, so no reopening is involved.
- **Companion files:** [IMPACT_ASSESSMENT.md](IMPACT_ASSESSMENT.md),
  [BASIS_AMENDMENT.md](BASIS_AMENDMENT.md), [ARC_EFFECT.md](ARC_EFFECT.md)
  and [OWNER_ITEMS.md](OWNER_ITEMS.md).

## Reading this file

The conventions are the same as the SCA-V4-001 file, which the owner
accepted:

- **Edit IDs** are `F-<deliverable>-<nn>`. The "F" series keeps them distinct
  from SCA-V4-001's `E-` IDs. Apply each deliverable's edits in the listed
  order.
- **Tokens.** `{AMENDMENT_ID}` is the accepted amendment ID (recommended
  `SCA-V4-002`, item Q-1). `{AMENDMENT_SNAPSHOT}` is the accepted group-3
  snapshot folder name under `projects/chirality-app-v4/execution/_ScopeChange/`.
  Both are filled at application from the accepted records. No other byte
  depends on the acceptance act.
- **Amendment reference.** Each revised SoW gains one Axiology `AX-*` line
  naming the amendment, its snapshot, the decisions applied, and the revised,
  added and removed IDs (REVISE step 4).
- **No new OUT, AC, VER, REQ, CLM or TBD IDs.** Nothing is renumbered or
  removed. The only new IDs are the AX lines. No matrix row changes.
- **Frontmatter is unchanged** in every SoW (the SCA-V4-001 reading O-22).
- **Conditional** edits depend on an owner item. If the owner declines the
  item, drop those edits and that deliverable's AX line.

Decision identities used in the new text:

| Short form here | Full identity in the SoW text | Record |
|---|---|---|
| FI DECISION-1 (D2, D3, D4) | `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` | `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-FIRST-INCREMENT-20260928/OWNER_DECISIONS.md` |
| SI DECISION-4 (D4-3) | `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4` | `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-SWBPIPE-INTAKE-20260928/OWNER_DECISIONS.md` |
| BA DECISION-8, DECISION-10 | `APP-V4-BASIS-ALIGN-20260928-DECISION-8`, `APP-V4-BASIS-ALIGN-20260928-DECISION-10` | `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-BASIS-ALIGN-20260928/OWNER_DECISIONS.md` |

The BA record labels its decisions "DECISION-8" and "DECISION-10" without a
run prefix. The full form follows the pattern the earlier records use, and
each AX line also cites the record path.

## Summary

| Deliverable | Prior SoW sha256 | Lifecycle | Edits (blocks / pairs) | Item | Conditional |
|---|---|---|---|---|---|
| DEL-10-03 | `4e16817e71f1df39afd3e3dd8175a04e9d4cc2384bf42065e91e16a5452b5f92` | INITIALIZED | 2 / 2 | 1 (local-first) | — |
| DEL-02-01 | `6ccc860ba48aee9392fbf90fef323577c7599655164442e6f3fb0b78fe36f0dc` | IN_PROGRESS | 2 / 2 | 2 (N-18) | Q-4 |
| DEL-02-03 | `a4ffcd8711ad0ee50d9ca6876d0b19972f9f3ba9a7a129578068c4a918c24c0e` | IN_PROGRESS | 2 / 2 | 2 (N-21, N-24, X-1) | Q-4 (per arc) |
| DEL-09-07 | `53b51d309d060089a6a88dae565867a92348789ee01430927e7464c7c2d3cba0` | INITIALIZED | 4 / 4 | 3 (OI-001/002) | — |
| DEL-01-04 | `7261a58f93d4531ca080c16d7fe088818871c3444085bade2eb2350ace94e60a` | INITIALIZED | 6 / 6 | 3 (OI-001/002/012) | — |
| DEL-02-02 | `b0a1a8a4aa6f53057c8db4bb33c65c5e697f45ae509088a570a70ff8cee295ec` | INITIALIZED | 3 / 3 | 3 (OI-001/002/012) | — |
| DEL-03-03 | `fdd22e25a0a43c55d31ca38f3fcb44931af8ebee6d34da62ff1f214013fb2881` | IN_PROGRESS | 3 / 3 | 4 (CLM-002 tail) | — |
| DEL-04-02 | `e077f20a95efc193e4de5489824e84278449b64dda615fb913c9dbd6070122f9` | IN_PROGRESS | 2 / 2 | proposed addition | Q-6 |
| DEL-01-01 | `f65dc666708dc06fbff046cf293ff529024ad9487829d2c105b3678c86a8acc9` | IN_PROGRESS | 2 / 2 | proposed addition | Q-6 |
| **Total** | | | **26 / 26** | | |

Without the Q-6 additions: 7 SoWs, 22 blocks. The 26 blocks include 9
amendment-reference AX lines.

---

## DEL-10-03 — Shared commitments and consumer responsibility account

REVISION_SCOPE: REQ-005; new AX-005.

#### F-1003-01 · REQ-005 · item 1 ("local-first")
Target: DEL-10-03
Trace: SI DECISION-4 D4-3; BA DECISION-8 answer 3 ("Small follow-on amendment"); PRD V4-HOST-01 and ARCHITECTURE V4-ARC-11 as amended by SCA-V4-001. The wording follows the accepted PKG-05 text (SCA-V4-001 D-13): "the minimal host loop, on a local or cloud model the person chooses".
```old
retaining stock Codex/App-owned hosting, Tauri and the minimal local-first host loop.
```
```new
retaining stock Codex/App-owned hosting, Tauri and the minimal host loop, which runs on a local or cloud model the person chooses, with no default; a cloud model is reached by OAuth sign-in or an API key (PRD V4-HOST-01 and ARCH V4-ARC-11 as amended by `SCA-V4-001`; `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4` D4-3).
```

#### F-1003-02 · new AX-005 (amendment reference) · acceptance-conditional
Target: DEL-10-03
```old
Sources: `docs/DELIVERABLE_SCOPE_OF_WORK_STANDARD.md` §§2/5/8/10; `projects/chirality-app-v4/execution/_Coordination/_COORDINATION.md`; EXAM §§1–2/7.
```
```new
Sources: `docs/DELIVERABLE_SCOPE_OF_WORK_STANDARD.md` §§2/5/8/10; `projects/chirality-app-v4/execution/_Coordination/_COORDINATION.md`; EXAM §§1–2/7.
- **AX-005** — Revised under scope-change amendment `{AMENDMENT_ID}` (accepted snapshot `projects/chirality-app-v4/execution/_ScopeChange/{AMENDMENT_SNAPSHOT}`), applying `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4` D4-3 (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-SWBPIPE-INTAKE-20260928/OWNER_DECISIONS.md`) as routed by `APP-V4-BASIS-ALIGN-20260928-DECISION-8` (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-BASIS-ALIGN-20260928/OWNER_DECISIONS.md`). Revised: REQ-005. Added: AX-005. Removed: none.
```

---

## DEL-02-01 — Portable workflow contract and shared allocation

REVISION_SCOPE: CLM-002 (one appended sentence); new AX-006.

#### F-0201-01 · CLM-002 (consumption sentence) · item 2, arc N-18 · conditional (Q-4)
Target: DEL-02-01
Trace: grounds N-18 (DEL-02-01 → DEL-03-02). Design evidence: WD-v0.6 §8 "Expected from suppliers", row DEL-03-02 (change-item content identity; item dispositions, all-decided, item-left events; applied-outcome object identities; used in WD §4.3.6 and §4.3.7); WD §4.3.7 "DEL-03-02 supplies per-item dispositions, the "all items decided" indication and item-left events (P §4.3)"; P-v0.6 §13 "Provide to DEL-02-01 / DEL-02-03". The sentence names only the current-phase inputs; the governance-phase constraint is left in the existing ownership clause. Guard: names no other deliverable.
```old
These are receiving interfaces, not transferred implementation assignments.
```
```new
These are receiving interfaces, not transferred implementation assignments. Checkpoint subject binding and item-level decisions consume `DEL-03-02`'s change-item content identities, per-item dispositions, all-items-decided indication, item-left events and applied-outcome object identities; this contract does not define them.
```

#### F-0201-02 · new AX-006 (amendment reference) · acceptance-conditional
Target: DEL-02-01
```old
Revised: CLM-002, CLM-003, REQ-002, REQ-003, REQ-006, VER-003 and TBD-003. Added: TBD-004 and AX-005. Removed: none.
```
```new
Revised: CLM-002, CLM-003, REQ-002, REQ-003, REQ-006, VER-003 and TBD-003. Added: TBD-004 and AX-005. Removed: none.
- **AX-006** — Revised under scope-change amendment `{AMENDMENT_ID}` (accepted snapshot `projects/chirality-app-v4/execution/_ScopeChange/{AMENDMENT_SNAPSHOT}`), applying `APP-V4-BASIS-ALIGN-20260928-DECISION-10` (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-BASIS-ALIGN-20260928/OWNER_DECISIONS.md`), which routed this contract's statement of the proposal-contract outputs it consumes to this amendment. Revised: CLM-002. Added: AX-006. Removed: none.
```

---

## DEL-02-03 — Workflow execution compatibility and round-trip support

REVISION_SCOPE: CLM-002 (one appended sentence); new AX-005.

#### F-0203-01 · CLM-002 (consumption sentence) · item 2, arcs N-21, N-24, X-1 · conditional (Q-4, per clause)
Target: DEL-02-03
Trace: grounds N-21 (DEL-02-03 → DEL-03-02), N-24 (DEL-02-03 → DEL-03-03) and X-1 (DEL-02-03 → DEL-01-04). Design evidence: EXEC-v0.4 §9.1 rows DEL-03-02 (per-item dispositions, item-left events, all-items-decided, change-item content identity, applied outcome with resulting objects; used in §4.4, §4.11, §4.12), DEL-03-03 (§7.7 checkpoint observation on X) and DEL-01-04 (App act control CAP-2 and person identity; used in §5); ADAPTER-v0.4 §7.7 "Phase 1 (R8-1). The adapter observes arrivals and act records and passes them to DEL-02-03 for recording" and §11 "Provide to DEL-02-03"; P-v0.6 §13 "Provide to DEL-02-01 / DEL-02-03"; EXEC §5 "Construction of the control is DEL-01-04's (later undertaking, D1). App-side positive capture cases are therefore AWAITING INPUT (CH-23)" and U-E8. If the owner drops an arc at Q-4, delete its clause and adjust the list punctuation. Guard: names no DEL-04-01 or DEL-09-06 input.
```old
`DEL-01-04` (later undertaking) constructs the App act control. Source: G3 Deliverables.csv
```
```new
`DEL-01-04` (later undertaking) constructs the App act control. This slice consumes, and does not define: `DEL-03-02`'s per-item dispositions, item-left events, all-items-decided indication, change-item content identities and applied outcomes with their resulting objects, for checkpoint recording and interrupted or replayed history (REQ-002, REQ-003); `DEL-03-03`'s observations of checkpoint arrivals and act records on the external channel, which this slice records (REQ-002, REQ-003); and `DEL-01-04`'s App act control and person identity, for the App-side positive capture fixtures (OUT-003, VER-003), which await that later undertaking. Source: G3 Deliverables.csv
```

#### F-0203-02 · new AX-005 (amendment reference) · acceptance-conditional
Target: DEL-02-03
```old
the REQ-002 matrix evidence cell, TBD-001 and TBD-002. Added: TBD-006 and AX-004. Removed: none.
```
```new
the REQ-002 matrix evidence cell, TBD-001 and TBD-002. Added: TBD-006 and AX-004. Removed: none.
- **AX-005** — Revised under scope-change amendment `{AMENDMENT_ID}` (accepted snapshot `projects/chirality-app-v4/execution/_ScopeChange/{AMENDMENT_SNAPSHOT}`), applying `APP-V4-BASIS-ALIGN-20260928-DECISION-10` (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-BASIS-ALIGN-20260928/OWNER_DECISIONS.md`), which routed this slice's statement of the proposal, external-channel and App act-control inputs it consumes to this amendment. Revised: CLM-002. Added: AX-005. Removed: none.
```

---

## DEL-09-07 — Local host candidate qualification

REVISION_SCOPE: CLM-002 (policy clause); TBD-002; TBD-003; new AX-005.
Named in the owner's scope as "DEL-09-07 (TBD-002/003)". CLM-002 carries
the same statement, so it is aligned with them (IMPACT §4, V-3).

#### F-0907-01 · CLM-002, policy clause · item 3
Target: DEL-09-07
Trace: FI DECISION-1 D2/D3; OI-021. Same treatment as SCA-V4-001 E-0906-01 (DEL-09-06 CLM-005). REQ-009 still reads correctly ("the unresolved human-act/classifier policy belongs to the owner with App/SWB contract owners"), because the remaining matters stay with that owner.
```old
The person sets operation autonomy, while unresolved reserved-act/classifier policy remains with the owner and App/SWB contract owners.
```
```new
The person sets operation autonomy. Reserved acts and classifier treatment are ruled for the first increment's App/shared contracts (`APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2/D3); any reserved-act or classifier matter those rulings do not cover stays with the owner and App/SWB contract owners, with operation-specific additions under OI-021.
```

#### F-0907-02 · TBD-002 · item 3
Target: DEL-09-07
Trace: FI DECISION-1 D2; SCA-V4-001 E-0203-11 and E-0401-08 wording. PRD OQ-02 is kept, narrowed to what D2 leaves open (SCA-V4-001 O-26 left the PRD markers for a later basis update).
```old
- **TBD-002** — OI-001: choose always-reserved acts by concrete operation and consequence; owner is **Owner with App/SWB contract owners**; point of need is **Before operation-policy production contracts**. False attribution is already prohibited. PRD OQ-02 additionally requires the affected operation/permission contract and examination criterion to await the policy disposition. This deliverable consumes the adopted choice; it does not decide it.
```
```new
- **TBD-002** — OI-001 — ruled for the first increment's App/shared contracts by `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2: marking checked; accepting a proposal where the autonomy requires one; engineering approval; professional reliance; changing the grant or enabling external access. The host names and enforces its own list (HOST V4-HI-30; DEP-001). Operation-specific additions for the examined activity remain OPEN under OI-021 (TBD-001). Any matter the ruling does not cover stays with the **Owner with App/SWB contract owners**, point of need **Before operation-policy production contracts**. False attribution is already prohibited. PRD OQ-02 still requires an examination criterion that depends on such an uncovered operation to await its disposition. This deliverable consumes the adopted choice; it does not decide it.
```

#### F-0907-03 · TBD-003 · item 3
Target: DEL-09-07
Trace: FI DECISION-1 D3 ("the SWB default proposal mode applies (V4-HI-41)").
```old
- **TBD-003** — OI-002: distinguish routine tool permissions from professional acts and settle App/host classifier treatment; owner is **Owner with App/SWB contract owners**; point of need is **Before permission-policy implementation**. No classifier behavior is selected here. As PRD OQ-02 states, the dependent examination criterion is fixed only after the applicable disposition; unrelated verification and definition remain possible.
```
```new
- **TBD-003** — OI-002 — ruled by `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D3: in the App, routine tool-permission and sandbox modes (including classifier-based modes) remain the user's own Codex setting and never stand in for a reserved or professional act; hosts have no classifier permission mode in the first increment, and the SWB default proposal mode applies (HOST V4-HI-41). Host adoption remains under DEP-001. No classifier behavior is selected here. As PRD OQ-02 states, a dependent examination criterion outside that ruling is fixed only after its disposition; unrelated verification and definition remain possible.
```

#### F-0907-04 · new AX-005 (amendment reference) · acceptance-conditional
Target: DEL-09-07
```old
VER-005, VER-006 and the REQ-006/AC-006 matrix evidence cell. Added: AX-004. Removed: none.
```
```new
VER-005, VER-006 and the REQ-006/AC-006 matrix evidence cell. Added: AX-004. Removed: none.
- **AX-005** — Revised under scope-change amendment `{AMENDMENT_ID}` (accepted snapshot `projects/chirality-app-v4/execution/_ScopeChange/{AMENDMENT_SNAPSHOT}`), applying `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2/D3 (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-FIRST-INCREMENT-20260928/OWNER_DECISIONS.md`). Revised: CLM-002, TBD-002 and TBD-003. Added: AX-005. Removed: none.
```

---

## DEL-01-04 — Native requests, outcomes and attachments

REVISION_SCOPE: CLM-005 (policy clause); VER-005 (last sentence but one);
TBD-001; TBD-002; TBD-004; new AX-004. CLM-002 and source key O stay
unchanged: both remain true ("historical version numbers are not a v4 pin";
the rows keep their points of need).

#### F-0104-01 · CLM-005, policy clause · item 3
Target: DEL-01-04
Trace: FI DECISION-1 D2/D3. REQ-006 still resolves: it names "the Owner with App/SWB contract owners, as CLM-005 states", and CLM-005 keeps that owner for the matters the rulings do not cover.
```old
the **Owner with App/SWB contract owners** decides unresolved OI-001 and OI-002, rather than this UI slice or the policy deliverable deciding them.
```
```new
the owner ruled OI-001 and OI-002 for the first increment's App/shared contracts (`APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2/D3), and the **Owner with App/SWB contract owners** decides any matter those rulings do not cover, with operation-specific additions under OI-021, rather than this UI slice or the policy deliverable deciding them.
```

#### F-0104-02 · VER-005 · item 3
Target: DEL-01-04
Trace: FI DECISION-1 D2/D3; SCA-V4-001 E-0401-05 pattern.
```old
A concrete unresolved policy-dependent operation remains subject to its own OI-001/OI-002 ruling; test construction does not decide it.
```
```new
Adopted reserved acts and classifier treatment are those of `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2/D3 as carried through the PKG-04 interface; a concrete policy-dependent operation those rulings do not cover remains subject to its own ruling (OI-021 or a successor); test construction does not decide it.
```

#### F-0104-03 · TBD-001 · item 3
Target: DEL-01-04
Trace: FI DECISION-1 D2.
```old
- **TBD-001** — OI-001, Reserved human acts: **Owner with App/SWB contract owners**; point of need **Before operation-policy production contracts**. Choose always-reserved acts by concrete operation and consequence. This contract carries current non-fabrication and act distinctions and consumes adopted policy; it does not decide a global reserved list. Source: O; H.
```
```new
- **TBD-001** — OI-001, Reserved human acts — ruled for the first increment's App/shared contracts by `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2 (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-FIRST-INCREMENT-20260928/OWNER_DECISIONS.md`): marking checked; accepting a proposal where the autonomy requires one; engineering approval; professional reliance; changing the grant or enabling external access. Operation-specific additions remain OPEN under OI-021. Any matter the ruling does not cover stays with the **Owner with App/SWB contract owners**, point of need **Before operation-policy production contracts**. This contract carries current non-fabrication and act distinctions and consumes adopted policy through CLM-005; it does not decide a reserved list. Source: O; H.
```

#### F-0104-04 · TBD-002 · item 3
Target: DEL-01-04
Trace: FI DECISION-1 D3.
```old
- **TBD-002** — OI-002, Classifier routine permissions: **Owner with App/SWB contract owners**; point of need **Before permission-policy implementation**. Distinguish routine tool permissions from professional acts and settle App/host treatment. No classifier behavior is selected here. Source: O; H.
```
```new
- **TBD-002** — OI-002, Classifier routine permissions — ruled by `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D3: in the App, routine tool-permission and sandbox modes (including classifier-based modes) remain the user's own Codex setting and never stand in for a reserved or professional act; hosts have no classifier permission mode in the first increment. Native tool permission keeps its native semantics in this slice (REQ-005). No classifier behavior is selected here. Source: O; H.
```

#### F-0104-05 · TBD-004 · item 3 (OI-012)
Target: DEL-01-04
Trace: FI DECISION-1 D4; DEL-01-01 TBD-002 as revised by SCA-V4-001 (E-0101-02). The DEP-005 sentence is kept verbatim.
```old
- **TBD-004** — OI-012, Codex version pin: **App implementation owner**; point of need **Before protocol generation and qualification**. Select an identified supported supplier pin.
```
```new
- **TBD-004** — OI-012, Codex version pin: `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D4 selected Codex 0.158.0 as the definition and generation pin; it is re-examined before implementation, and upgrades are deliberate. Remaining under OI-012, with the **App implementation owner**: the pin used for implementation and for qualification on an identified App candidate, point of need **Before protocol generation and qualification** for that candidate.
```

#### F-0104-06 · new AX-004 (amendment reference) · acceptance-conditional
Target: DEL-01-04
```old
The manager's later lifecycle recording, accepted dependency graph, implementation authorization, receiving adoption and release remain separate acts.
```
```new
The manager's later lifecycle recording, accepted dependency graph, implementation authorization, receiving adoption and release remain separate acts.
- **AX-004** — Revised under scope-change amendment `{AMENDMENT_ID}` (accepted snapshot `projects/chirality-app-v4/execution/_ScopeChange/{AMENDMENT_SNAPSHOT}`), applying `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2, D3 and D4 (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-FIRST-INCREMENT-20260928/OWNER_DECISIONS.md`). Revised: CLM-005, VER-005, TBD-001, TBD-002 and TBD-004. Added: AX-004. Removed: none.
```

---

## DEL-02-02 — Workflow-making workspace and registration

REVISION_SCOPE: TBD-001; TBD-002 (OI-012 clause); new AX-004. AX-003
("the broader always-reserved-act list and classifier-permission policy are
not [settled]") stays: the product-level list (PRD OQ-02) is still open.

#### F-0202-01 · TBD-001 · item 3
Target: DEL-02-02
Trace: FI DECISION-1 D2/D3.
```old
- **TBD-001** — OI-001 retains broader operation-level reserved-act decisions with the owner and affected App/SWB contract owners, with PointOfNeed "Before operation-policy production contracts". OI-002 retains classifier-permission decisions with those owners, with PointOfNeed "Before permission-policy implementation".
```
```new
- **TBD-001** — OI-001 and OI-002 were ruled for the first increment's App/shared contracts by `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2 (five reserved acts) and D3 (in the App, routine tool-permission and sandbox modes, including classifier-based modes, remain the user's own Codex setting and never stand in for a reserved or professional act); record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-FIRST-INCREMENT-20260928/OWNER_DECISIONS.md`. Broader operation-level reserved-act decisions that D2 does not cover remain with the owner and affected App/SWB contract owners, with PointOfNeed "Before operation-policy production contracts"; operation-specific additions are made under OI-021.
```

#### F-0202-02 · TBD-002, OI-012 clause · item 3
Target: DEL-02-02
Trace: FI DECISION-1 D4.
```old
OI-012 leaves the supplier version pin with that owner before generation/qualification.
```
```new
For OI-012, `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D4 selected Codex 0.158.0 as the definition and generation pin; re-examination before implementation and the pin used for qualification remain with that owner before generation/qualification.
```

#### F-0202-03 · new AX-004 (amendment reference) · acceptance-conditional
Target: DEL-02-02
```old
No successful execution, proposal state or neighboring evidence supplies a missing human act. [P1 V4-WF-02 and V4-AUT-03–04; H1 V4-HI-25 and V4-HI-30–31; D1 decision 03]
```
```new
No successful execution, proposal state or neighboring evidence supplies a missing human act. [P1 V4-WF-02 and V4-AUT-03–04; H1 V4-HI-25 and V4-HI-30–31; D1 decision 03]
- **AX-004** — Revised under scope-change amendment `{AMENDMENT_ID}` (accepted snapshot `projects/chirality-app-v4/execution/_ScopeChange/{AMENDMENT_SNAPSHOT}`), applying `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2, D3 and D4 (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-FIRST-INCREMENT-20260928/OWNER_DECISIONS.md`). Revised: TBD-001 and TBD-002. Added: AX-004. Removed: none.
```

---

## DEL-03-03 — Local external-agent receiving adapter

REVISION_SCOPE: CLM-002 (last clause and its Sources); REQ-005 (the policy
clause that cites CLM-002); new AX-005.

#### F-0303-01 · CLM-002 tail · item 4
Target: DEL-03-03
Trace: FI DECISION-1 D2/D3; the SoW's own TBD-001 (operation-specific additions under OI-021; host adoption and enforcement under DEP-001) and TBD-002. What actually remains open: operation-specific reserved-act additions (OI-021, owner via the outside SWB session and App/shared owner) and the host's adoption and enforcement of its own list (DEP-001). No classifier matter remains open for the first increment.
```old
the actual Owner with App/SWB contract owners retains unresolved reserved-act and classifier decisions. Sources: Group3 Deliverables DEL-03-01/02/03, Packages PKG-04 and Open_Issues OI-001/OI-002;
```
```new
the first-increment reserved acts and classifier treatment are ruled (`APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2/D3; TBD-001, TBD-002); the owner via the outside SWB session and the App/shared owner retain operation-specific reserved-act additions (OI-021, TBD-006), and the external host owner retains adoption and enforcement of its own reserved list (DEP-001). Sources: Group3 Deliverables DEL-03-01/02/03, Packages PKG-04 and Open_Issues OI-001/OI-002/OI-021;
```

#### F-0303-02 · REQ-005, policy clause · item 4 (consequential)
Target: DEL-03-03
Trace: REQ-005 cites CLM-002 for this owner. Changing CLM-002 alone would leave REQ-005 naming an owner and a decision that CLM-002 no longer carries.
```old
unresolved reserved/classifier policy decisions remain with the Owner with App/SWB contract owners (CLM-002)
```
```new
operation-specific reserved-act additions remain with the owner via the outside SWB session and the App/shared owner, and host adoption and enforcement of its reserved list with the external host owner (CLM-002)
```

#### F-0303-03 · new AX-005 (amendment reference) · acceptance-conditional
Target: DEL-03-03
```old
Revised: CLM-002, REQ-002, REQ-003, REQ-004, AC-002, VER-003, TBD-001 and TBD-002. Added: AX-004. Removed: none.
```
```new
Revised: CLM-002, REQ-002, REQ-003, REQ-004, AC-002, VER-003, TBD-001 and TBD-002. Added: AX-004. Removed: none.
- **AX-005** — Revised under scope-change amendment `{AMENDMENT_ID}` (accepted snapshot `projects/chirality-app-v4/execution/_ScopeChange/{AMENDMENT_SNAPSHOT}`), applying `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2/D3 (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-FIRST-INCREMENT-20260928/OWNER_DECISIONS.md`). Revised: CLM-002 and REQ-005. Added: AX-005. Removed: none.
```

---

## DEL-04-02 — Visible autonomy and result standing (proposed addition; conditional Q-6)

The same defect as the DEL-03-03 tail, found in this pass: CLM-004 says the
owner "decides the unresolved … choices in OI-001 and OI-002", while the
SoW's own TBD-001/TBD-002 (revised under SCA-V4-001) say both are ruled.

REVISION_SCOPE: CLM-004 (first sentence); new AX-005.

#### F-0402-01 · CLM-004, first sentence · conditional (Q-6)
Target: DEL-04-02
Trace: FI DECISION-1 D2/D3. REQ-006 and REQ-007 cite CLM-004; the owner they name is kept.
```old
- **CLM-004** — The Owner with App/SWB contract owners decides the unresolved reserved-act and routine-classifier choices in OI-001 and OI-002.
```
```new
- **CLM-004** — The owner ruled OI-001 and OI-002 for the first increment's App/shared contracts (`APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2/D3; TBD-001, TBD-002); the Owner with App/SWB contract owners decides any reserved-act or routine-classifier matter those rulings do not cover, with operation-specific additions under OI-021.
```

#### F-0402-02 · new AX-005 (amendment reference) · conditional (Q-6), acceptance-conditional
Target: DEL-04-02
```old
Revised: source key U, CLM-002, REQ-007, AC-004, VER-004, TBD-001 and TBD-002. Added: TBD-006 and AX-004. Removed: none.
```
```new
Revised: source key U, CLM-002, REQ-007, AC-004, VER-004, TBD-001 and TBD-002. Added: TBD-006 and AX-004. Removed: none.
- **AX-005** — Revised under scope-change amendment `{AMENDMENT_ID}` (accepted snapshot `projects/chirality-app-v4/execution/_ScopeChange/{AMENDMENT_SNAPSHOT}`), applying `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2/D3 (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-FIRST-INCREMENT-20260928/OWNER_DECISIONS.md`). Revised: CLM-004. Added: AX-005. Removed: none.
```

---

## DEL-01-01 — Stock Codex hosting and supplier contract (proposed addition; conditional Q-6)

The [N] source line still says "no selected version/environment is
established", while CLM-003, REQ-006 and TBD-002 (revised under SCA-V4-001)
record the 0.158.0 definition and generation pin.

REVISION_SCOPE: source list line [N]; new AX-006.

#### F-0101-01 · source line [N] · conditional (Q-6)
Target: DEL-01-01
Trace: FI DECISION-1 D4.
```old
row DEP-005 — still open; no selected version/environment is established.
```
```new
row DEP-005 — still open. `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D4 selected 0.158.0 as the definition and generation pin (CLM-003, TBD-002); no implementation or qualification version or environment is established.
```

#### F-0101-02 · new AX-006 (amendment reference) · conditional (Q-6), acceptance-conditional
Target: DEL-01-01
```old
Revised: CLM-003, REQ-006 and TBD-002. Added: AX-005. Removed: none.
```
```new
Revised: CLM-003, REQ-006 and TBD-002. Added: AX-005. Removed: none.
- **AX-006** — Revised under scope-change amendment `{AMENDMENT_ID}` (accepted snapshot `projects/chirality-app-v4/execution/_ScopeChange/{AMENDMENT_SNAPSHOT}`), applying `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D4 (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-FIRST-INCREMENT-20260928/OWNER_DECISIONS.md`). Revised: the [N] source line. Added: AX-006. Removed: none.
```

---

## Extraction guards

These are for the `dependency-extract` UPDATE briefs that follow REVISE
(IMPACT §7):

- **The four arcs.** F-0201-01 and F-0203-01 are written as "consume …; does
  not define", the form this repository's extractors read as UPSTREAM
  (compare DEP-02-01-026). They are expected to yield exactly N-18, N-21,
  N-24 and X-1. The existing ownership clauses in the same CLM-002 stay
  non-edges, as the Run Notes record.
- **No other new arc.** No other edit names a deliverable that its SoW does
  not already cite as a supplier (IMPACT §5, the mention check). The AX lines
  name no deliverable.
- **DEL-04-01 and DEL-09-06.** No edit makes DEL-04-01 consume anything, and
  no edit names DEL-09-06. The DEL-09-06 guard (DAG-002 HANDOFF_STATE) holds.
- **OI-001/002 constraint rows.** Rows that quote the replaced TBD text
  (IMPACT §5 lists them) are re-quoted or retired `source_revised` with the
  successor row named, the way DEP-02-03-015/-016 were under SCA-V4-001.

## Mechanical checks performed

`sow_dryrun.py` (scratch `P1-002/`) parsed this file. It found 26 blocks and
26 old → new pairs in 9 deliverables. It applied each deliverable's blocks in
order to a copy of the SoW at `102f09c1a`, with `{AMENDMENT_ID}` =
`SCA-V4-002` and a dummy snapshot name. Results:

| Check | Result |
|---|---|
| Prior-contract sha256 equals the Summary table | 9/9 |
| Each "old" block occurs exactly once when applied | 26/26 |
| Unfilled tokens after filling | 0 |
| Frontmatter unchanged | 9/9 |
| `tools/scope_of_work/validate_scope_of_work.py` on each revised copy | 9/9 PASS (`SOW_V1`) |
| `tools/scope_of_work/check_boundary_owner_resolution.py` on each revised copy | 9/9 exit 0 |
| New deliverable IDs named by the new text, beyond those the old file already names | 0 |
| Same, with and without the Q-6 additions | 7/7 and 9/9 PASS |

These are checks of the proposal before application. They are not the REVISE
run or its `MODE=VERIFY`.
