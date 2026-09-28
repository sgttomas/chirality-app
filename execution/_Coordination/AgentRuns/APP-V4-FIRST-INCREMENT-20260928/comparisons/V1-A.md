# V1-A — Policy-consumer comparison (DEL-04-01 → eight receivers)

- Run: APP-V4-FIRST-INCREMENT-20260928, node V1-A (CASE-002 Q-03 for the policy joins)
- Reviewer: independent Type 2 reviewer (Claude Code `Agent` subagent). Not an author of any compared file. No delegation, no git, no network.
- Standing: REVIEW EVIDENCE — element-by-element meaning comparison of v0.1 definitions. It decides no OI, performs no human act, and changes no design.
- Basis read: [BRIEFS.md](../BRIEFS.md) "Common brief", "Owner rulings now in force", "V1" (sha256 `295c050f…7121`); [OWNER_DECISIONS.md](../OWNER_DECISIONS.md) `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` (sha256 `f3f8e5f3…f2e`); the SoWs' `Dependencies.csv` rows named in §6; `P/docs/HOST_INTEGRATION.md` V4-HI-02, -22, -30…33, -40…42; `P/docs/PRD.md` V4-AUT-01…05, V4-WF-02, V4-CON-05; `P/docs/EXAMINATION.md` V4-EXM-22; `DECISION_BRIEF.html#d3`.

`P` = `projects/chirality-app-v4/execution`. Section references such as "04-01 §4.3" point into the Design files below.

## 1. Versions compared

| Side | Contribution as read | File (sha256 at read) | Consuming element(s) / VER |
|---|---|---|---|
| Supplier | DEL-04-01/ACT-POLICY-v0.1 | `DEL-04-01…/Design/ACT_AND_POLICY_CONTRACT.md` (`e6457535…3763`) | V-01…V-13 carried; V-20…V-23 held |
| Receiver | DEL-04-03/RS-v0.1 | `RECORD_SEMANTICS.md` (`1e4bb89e…c462`) | §0 act names, §6 human-act record, R6, HA-1…6; VER-002/003 (its VC-04…09). Register: DEP-04-01-016 (no mirror, RF-01) |
| Receiver | DEL-04-02/AS-v0.1 | `AUTONOMY_AND_STANDING_EXCHANGE.md` (`4c540c88…bd01`) | §2 grant model, §3 display states, §5 change sequence, §8/§9; VER-001, VER-005 (its VC-01, VC-09). Register: DEP-04-02-007/-011/-012 |
| Receiver | DEL-03-01/C-v0.1 | `CATALOG_AND_READ_BASIS.md` (`c13518c9…0b72`) | §3 element 8 (SOW-164), §4.1, §6.2, §10.1; VER-001, VER-005 (VC-C-01, VC-C-05). Register: DEP-03-01-024 |
| Receiver | DEL-03-02/P-v0.1 | `PROPOSAL_LIFECYCLE_AND_OUTCOMES.md` (`313487c0…bce`) | §2, §3.3, §4.1, §4.4, §9, §10; REQ-012, VER-011/013 (VC-P-11/13). Register: DEP-03-02-017 |
| Receiver | DEL-02-01/WD-v0.1 + WD-EX-v0.1 | `WORKFLOW_DECLARATION.md` (`bacfcb71…fc5e`), `EXAMPLES.md` (`69ac3dbf…d55a`) | §4.3 checkpoints, §4.4 promised standing, E1/E2; REQ-003, VER-003. Register: DEP-02-01-018 |
| Receiver | DEL-05-01/LOOP-v0.1 | `LOOP_RECEIVING_CONTRACT.md` (`fd80420c…c55c4`) | §2.2 tool offering class, §2.3 events, §2.4, §6 V-5, §9; REQ-007, VER-008 (VC-08). Register: DEP-05-01-018 |
| Receiver | DEL-05-02/PANEL-v0.1 | `PANEL_RECEIVING_CONTRACT.md` (`07c1e1c5…6f1e`) | §3.3, §3.4, §5, PC-22/23; REQ-003, VER-003 (VC-03). Register: DEP-05-02-008/-014/-015 |
| Receiver | DEL-01-01/HOSTING-BOUNDARY-v0.1 | `HOSTING_BOUNDARY.md` (`f1da7f76…d728`) | §2 table, H8, H9, R3, R7, R8, §11; REQ-007/008, VER-007 (VC-15). Register: no DEL-04-01 or OI-002 row (RF-03) |

**Check performed.** For each receiver: (1) listed each act, class, treatment, grant or label meaning it takes from DEL-04-01 "by accepted meaning"; (2) compared it with the supplier's statement of the same element (act taxonomy §2, S1–S12, grant model §4, SWB default §5, policy-class record §6, label rule §7, value map §8); (3) checked the focus terms across all nine files: act names and kinds (including reject, withdraw, grant change, registration), class values, grant model, widening bounds, "checked", "approval"; (4) checked where D2/D3 change a v0.1 statement; (5) checked the register rows in §6. No receiver had a supplied DEL-04-01 version. All nine files say they will reconcile at V1, so every receiver is comparing against accepted-basis meaning, not against ACT-POLICY-v0.1.

## 2. Agreements

| # | Element (supplier) | Receivers that state the same meaning |
|---|---|---|
| AG-01 | Evidence of one act kind never establishes another, and there is no universal acceptance prerequisite (04-01 §2, S3) | 04-03 D11, HA-3; 04-02 S10, DS-4; 03-01 §6.2 rules 1–2; 03-02 §10 rules; 02-01 I-1, I-3; 05-01 A-1, C-3; 05-02 W-4; 01-01 §11 closing paragraph |
| AG-02 | `success` ≠ acceptance; queued until the host records acceptance and application (S5, V-05) | 04-03 D5, OE-1; 04-02 S5; 03-01 S-C6; 03-02 S-P7, §4.1 rule 1; 02-01 S-G, I-2; 05-01 TL-3; 05-02 PC-08 |
| AG-03 | Proposals say "accept", never "approve" (S7, V-07) | 04-03 D9; 04-02 S8, DS-1; 03-02 S-P9, §8; 02-01 S-I; 05-01 §9; 05-02 W-1, PC-11 |
| AG-04 | Checkpoints override every grant, and a checkpoint is satisfied only by evidence of its own act kind (S9, §2.3, W-b) | 04-02 §4; 02-01 S-F, I-1, R-5; 05-01 C-1, C-2; 05-02 W-5; 03-02 S-P13, §4.4; 04-03 R8 |
| AG-05 | Agent examination (A3) is distinct from A4 (S11, V-12) | 04-03 R10, E3(d); 04-02 §8 "Agent examination" facet; 03-01 OP-C3, §10.4; 03-02 §10 "Agent finding"; 02-01 §4.3.2; 05-01 §9; 05-02 K-1, PC-12 |
| AG-06 | Decision actor and recorder are separate elements (§2.4, A9) | 04-03 FA-8, HA-2; 04-02 DS-2; 03-01 §6.2 rule 3; 03-02 §10; 02-01 I-5; 05-01 A-3; 05-02 W-2; 01-01 R7 |
| AG-07 | No certified, sealed, approved or code-compliant standing from agent output (S4, V-08) | 04-03 HA-4; 04-02 S11; 03-01 §6.2 rule 5; 02-01 S-L, FB-10; 05-01 §9; 05-02 §5 |
| AG-08 | Class vocabulary is the four V4-HI-02 values (V-02) | 03-01 §3 #8; 04-02 §2; 04-03 §6.1 |
| AG-09 | Widening cannot turn reserved, proposal-only or unresolved classes into direct application (W-c, W-d, W-e) | 04-02 §2 "Policy bound"; 03-02 §4.4 last bullet; 03-01 §3 class rules |
| AG-10 | Direct application carries origin, undo route and later-check route (S1, W-h) | 04-02 §7; 03-02 §4.4; 05-02 §5; 04-03 §5 "applied (direct)" |
| AG-11 | The grant is person-set, visible and changeable during work, and is recorded per run. A later change never re-labels an earlier operation (§4.4, V-04) | 04-02 §3, §5 step 5; 04-03 R6, §5 "settings version governing the route decision"; 03-02 §4.4 |
| AG-12 | Routine tool permission (A14) is not a human act and not the autonomy grant | 04-02 §2; 04-03 U-02; 03-01 §3 last class rule; 02-01 §4.3.2; 01-01 R8 ("an answer of any kind is tool-execution permission … not proposal acceptance, checking, approval … or reliance") |
| AG-13 | Silence or timeout never settles a request (A14 evidence) | 01-01 H8, R3; 04-02 S12 |
| AG-14 | SWB default: propose, with row, multi-row or batch acceptance, and per-row content binding (§5, V-11) | 04-02 §2; 03-02 §4.3; 05-02 §3.3; 04-03 E1 |
| AG-15 | Content binding, visible lapse, and no carry-over to new content (S6, V-06) | 04-03 §7 L-6; 04-02 §8; 02-01 I-4; 05-01 C-4; 05-02 W-3; 03-02 §5 re-draft |
| AG-16 | Acceptance ≠ application. Applied only with a receipt (A2 vs A5) | 03-02 §4.1 rule 2; 04-03 §5; 05-02 §3.3 "Must not"; 02-01 E1 `adjustment` standing |
| AG-17 | Unresolved policy is never a permission, default or pass (REQ-004) | All nine files state it in their reading section |
| AG-18 | A carried class value has a decision-basis reference (§6) | 03-01 VC-C-01 ("adopted value with policy source"); 04-03 §6.1 ("decision-basis reference"); 03-02 §2 ("governing policy") |
| AG-19 | Agents may prepare or request an act; a request is never the act (A8) | 05-01 §2.3 "Act requested" (agent, request only); 04-02 §5 step 1; 02-01 §4.3.2 |

## 3. Disagreements

Severity: **BLOCKING** means R1 cannot repair the receivers consistently until the supplier repairs this. **MAJOR** means consumers would behave or record differently at integration. **MINOR** means a wording or ownership mismatch with limited behavioural effect.

### D-01 BLOCKING — Canonical act-kind names are not shared

- **Supplier.** 04-01 §2.1 names A5 **Accept**, A6 **Approve (engineering approval)** and A7 **Rely (professional reliance)**. A9 **Faithfully record** is a *companion act* (§2.2), and A10–A14 are named acts. §7: "The word **approve** is used only for A6". It also says design-candidate approval (V4-HI-65) "is its own act with distinct identity … outside this first increment".
- **Receivers.**
  - 02-01 §4.3.1 lists the accepted-basis names it uses: "*accept a proposed edit* …, *mark checked* …, *approve* (V4-HI-30; **V4-CON-05 design-candidate approval**), ***accept professional reliance*** (d3; V4-AUT-05)". FB-04 then says a checkpoint naming an act kind "not recognized by the current DEL-04-01 version" can only become performed "through evidence of that named kind", and that consumers "report **not established** rather than substituting a nearby kind". Under 04-01's names, a 02-01 checkpoint that requires "accept professional reliance" is therefore unsatisfiable.
  - 04-03 §0 and 04-02 §0 list "**accept an edit**" and put "**faithful recording**" in the list of act kinds. Neither lists A8 or A10–A14.
  - 05-01 §2.4 uses "accept an edit, mark checked, approve, rely".
  - 05-02 §5 uses "Acceptance of a proposed edit", "Marking checked", "Approval" and "Professional reliance".
- **Basis note.** d3 and V4-CON-05 do say "accepting professional reliance". V4-HI-33 reserves "accept" wording for proposals in the interface. V4-CON-05 design-candidate approval is a different subject from A6.
- **Resolution.** DEL-04-01 v0.2 publishes one canonical name per act kind and an alias table that maps basis wording to it. For example, map "accepting professional reliance" (d3, V4-CON-05) to A7 *rely*, and keep "accept" for A5 only. It should also state whether A9 is an act kind or a recording mode (see D-18). Then 02-01 (§4.3.1, U-04, E1 "Not declared" line), 04-03 §0, 04-02 §0, 05-01 §2.4 and 05-02 §5 adopt the canonical names. 02-01 removes V4-CON-05 from the basis of *approve*. Design-candidate approval stays a separate, later-increment act.

### D-02 MAJOR — The SWB model-change class value differs between supplier and receivers

- **Supplier.** In the 04-01 §5 policy-class record, the "Catalog human-act class" row reads "**may apply within granted autonomy**", with "Decision standing: accepted default". V-11 carries it to DEL-03-01 "class and default".
- **Receivers.**
  - 03-01 §3: "The accepted SWBPIPE default *autonomy setting* for model changes is proposal … That is a default setting under DEL-04-02, **not a class ruling**". §10.1 gives OP-C4 and OP-C5 the class "`UNRESOLVED{OI-001}`; accepted V4-HI-41 default setting = proposal".
  - 04-02 §0, 04-03 §0 and 05-01 §2.2 all say class values are `UNRESOLVED{OI-001}` without exception.
  - 04-02 F2 nonetheless widens the `op:add-support` class to direct, which its own §3 row "policy unresolved → No direct treatment" would forbid.
- **Why it matters.** V4-HI-41 says "the person may widen it". A widenable class is by meaning neither *proposal only* nor *reserved*, so 04-01's value is derivable. But 04-01 states it as a record value without marking it DERIVED.
- **Resolution.** 04-01 marks the V-11 class value as DERIVED from V4-HI-41 "may widen". It notes that operation-specific additions come with OI-021, per D2 last sentences. 03-01 carries V-11 for the model-change entries (OP-C4, OP-C5), with the pending OI-021 additions noted, instead of `UNRESOLVED{OI-001}`. 04-02, 04-03 and 05-01 replace their blanket "UNRESOLVED throughout" with "per the DEL-04-01 policy-class record".

### D-03 MAJOR — Class of operations that perform a human act (marking checked)

- **Supplier.** 04-01 §4.3 rule 3: "Act kind A4–A7 on any subject (check, accept, approve, rely) → *request the person's act*. An agent is never the decision actor of these … **This is independent of OI-001**". D2(a) now also reserves "marking work checked".
- **Receivers.**
  - 03-01 §10.1 OP-C6 "Mark row checked" has class "`UNRESOLVED{OI-001}`".
  - 05-02 K-4: "Which operations reserve marking checked to the person … are `UNRESOLVED{OI-001}`". W-6 and PC-23 are HELD on the same ground.
- **Resolution.** 04-01 v0.2 adds an explicit rule: a catalog operation whose effect is to perform or record A4–A7 as the person's act carries class **reserved to the person**. The basis is settled (S3, rule 3) and is now also D2(a)–(d). 03-01 OP-C6 and 05-02 K-4 then carry that value.

### D-04 MAJOR — Channel-off is encoded as "unavailable"

- **Supplier.** In 04-01 §4.2, the **unavailable** treatment is "not offered, with the same reason the person would see (V4-HI-04, -52)". §4.3 rule 1: "External actor, access not enabled → *unavailable*, with reason". FX-24 expects "Unavailable, with reason".
- **Receivers.** 03-01 §4.1 lists "**Channel not enabled**" as one of four distinct non-success results and says "They must never be encoded as one another … Only *unavailable* is subject to the HI-04 parity rule". 03-02 §9 lists "channel not enabled" separately from "unavailable".
- **Resolution.** 04-01 renames the rule-1 outcome to *channel not enabled* and keeps *unavailable* only for failed catalog preconditions (HI-04 parity). It then updates FX-24.

### D-05 MAJOR — Treatment vs runtime outcome when an agent lacks authority

- **Supplier.**
  - 04-01 §4.3 rule 7: "otherwise → *propose*". An operation outside the direct grant is routed to a proposal.
  - Rules 3–4 → *request the person's act*.
  - Rule 5 → *no policy basis* ("This contract supplies no treatment … A fixture reports AWAITING-DECISION").
- **Receivers.**
  - 03-01 §4.1 "**Not permitted for this actor** — … (e.g. reserved to the person; **outside grant**)".
  - 03-02 §2: "A difference arising from authority is reported as *not permitted* with the governing policy (or `UNRESOLVED{OI-001/002}`)". 03-02 §9 lists "not permitted | Actor lacks authority (reserved / outside grant / `UNRESOLVED{OI-001/002}`)".
  - 04-02 §3 "policy unresolved → **No direct treatment**" leaves proposing open. 04-01 rule 5 gives no treatment at all.
  - 05-01 §6 V-5 places the choice in the "Host route" ("Application or proposal per the person's autonomy and adopted policy"). 04-01 V-03 assigns "loop dispatch" to DEL-05-01.
- **Resolution.** 04-01 v0.2 adds a treatment → runtime-outcome map covering four points:
  1. Treatment is resolved before submission, on the host route per V4-HI-20/40. The loop only relays.
  2. A request to apply directly without a *direct* treatment is refused as *not permitted*, naming the governing treatment. It is never silently converted into a proposal.
  3. *Request the person's act* at runtime is *not permitted*, plus an A8 request.
  4. Whether *propose* remains available for a *no policy basis* class is stated explicitly.

  Then 03-01, 03-02, 04-02 and 05-01 cite the map.

### D-06 MAJOR — Agent-requested grant changes are conflated with person-set changes that the control has not yet confirmed

- **Supplier.** 04-01 §4.4: "An agent-originated grant change is a request (A8) until the person sets it. DEL-04-02 shows it as requested and not established". FX-23 and D2(e) now reserve grant changes to the person.
- **Receiver.**
  - 04-02 §3, entry evidence for **requested-unestablished**: "Person **(or an agent on the person's request)** submitted a change; control has not confirmed it". §6 settings-in carries a single "setting actor (the person)" and an establishing evidence of "person's control event". An agent-originated request would therefore be recorded with the person as setting actor.
  - 04-03 §8 repeats the same settings-in shape.
- **Resolution.** 04-02 splits two states: *requested by agent (A8; no person act)* and *set by person, not yet confirmed by control*. Settings-in carries *requester* and *setting actor* separately, and a person-set state needs person-act evidence. 04-03 R6 and §8 mirror this. 04-01 needs no change beyond citing D2(e).

### D-07 MAJOR — The grant's person-set scope is missing

- **Supplier.**
  - 04-01 §4.1 "*person grant*: For each operation class: direct or propose, **within a person-set scope**". §4.4 cites V4-AUT-01 "within a scope the person sets" and SOW-074 "per operation class and consequence".
  - DEP-04-01-020 names a "recorded person-set operation/consequence scope".
  - FX-20 widens "scoped to FX-MODEL-A". U-08 assigns the scope descriptor to "DEL-04-02 with DEL-04-03 | M3 settings-in / record-out exchange".
- **Receivers.**
  - 04-02 §2: "a treatment *t(k)* ∈ {direct, propose}". Its elements are per class only, with no scope element. F2 widens `op:add-support` with no scope.
  - 04-02 §6 and 04-03 §8 settings-in have no scope element.
  - 05-02 F-3 separately flags the "active autonomy scope display".
- **Resolution.** 04-02 adds a *scope* element to the grant, to each display state and to settings-in. The dimensions remain representation-neutral: examples are model or workspace, object set, run, period and consequence. 04-03 R6 and §8 mirror it. This closes 04-01 U-08.

### D-08 MAJOR — Which grant governs an operation, and who owns the in-flight rule

- **Supplier.** 04-01 §4.4: "The treatment recorded for each operation is the one in effect **when that operation was resolved**". U-09, the in-flight effect of narrowing, is owned by "DEL-04-02 with DEL-03-02".
- **Receivers.**
  - 03-02 §3.3 origin element "Autonomy standing **at drafting**". §4.4: "the grant it relied on (DEL-04-02 standing **at application**)" and "the standing actually in force at application is what is recorded".
  - 04-02 §5 step 4: "Which version governed an operation already evaluated or in flight is a **host fact**". Its U-06 owner is "Responsible host owner (DEP-001)".
  - 04-03 §5 records a single "settings version governing the route decision".
- **Resolution.** 04-01 defines "resolution" as the host route's evaluation at validation or application (V4-HI-20/22). It requires both the drafting-time and the resolution-time standing to be recorded when they differ, and names U-09 as DEL-04-01 policy plus host enforcement (DEP-001). 03-02 renames its two elements to match. 04-02 U-06 and 04-03 §5 align.

### D-09 MAJOR — A checkpoint requiring A5 combined with a direct grant cannot complete

- **Supplier.** 04-01 §4.3 rule 2 applies only "**At** a declared checkpoint". Nothing says that a checkpoint requiring A5 on an operation's output forces that operation to be proposed.
- **Receiver.**
  - 02-01 EXAMPLES E1 `CP-accept` subject: "the queued adjustment proposal". E2 R-5: "Person granted direct application for support changes; agent applies directly … `CP-accept`: awaiting act (run holds regardless)". VC-11: "Change applies with origin/undo; `CP-accept` still holds the run".
  - No proposal exists to accept, so the run can never release.
  - 04-02 F6 has the same shape: a checkpoint while `op:adjust-run` is direct.
- **Resolution.** 04-01 adds a DERIVED rule from V4-HI-42 and D2(b): when a declared checkpoint requires A5 on an operation's result, that operation's treatment is *propose* regardless of the grant. The alternative is to declare such a workflow invalid under a direct grant. 02-01 then revises R-5 and VC-11: either the change is proposed, or the checkpoint requires an act whose subject exists (A4 on applied rows).

### D-10 MAJOR — A negative decision at a checkpoint

- **Supplier.** 04-01 §2.3: "A checkpoint is satisfied **only by evidence of that act kind**". A10 **Reject** is a separate act kind. No negative form is defined for A4, A6 or A7.
- **Receivers.**
  - 02-01 §4.3.4 "**performed** — Evidence of the required act … **Includes a negative decision where the act kind has one**". §4.3.1 "on negative decision (e.g., rejects a proposal)". E1 `CP-check` has "on decline: stop and report".
  - 04-02 §4 "Discharged requires a human-act record reference … of the declared act kind".
  - 05-01 C-2 "resumes only on the host's evidence of the **specified** act".
  - Under 04-02 and 05-01, a rejection never releases `CP-accept`. Under 02-01 it counts as "performed".
- **Resolution.** 04-01 defines decision pairs (A5 ↔ A10). It states that for A4, A6 and A7 a person's decision not to act is a recorded stop or decline event, not an act of that kind. 02-01 separates *resolved negatively (A10)* from *performed*. 04-02 §4 and 05-01 C-2 add the negative branch.

### D-11 MAJOR — Which recorders may faithfully record

- **Supplier (internally split).**
  - S3 is SETTLED: "Faithfully recording an actually performed act is allowed, with decision actor ≠ recorder" (V4-AUT-03, V4-HI-31, d3).
  - A9 says: "**It grants no recording permission.** Which recorders may record which act kinds: `UNRESOLVED{OI-001}`". FX-09 adds "No recording permission is inferred (`UNRESOLVED{OI-001}` Q5)".
- **Receivers.** All take the permissive reading:
  - 04-03 E2 has an App agent faithfully record the engineer's mark checked, and marks it "Valid" (VC-04).
  - 02-01 I-5: "A recorder (App, host, agent) **may** faithfully record".
  - 03-02 §10: "Recorder (host or agent)".
  - 05-02 W-2: "an agent or host recorded".
  - 03-01 §6.2 rule 3: "(host, or an agent reporting what the host recorded)".
- **D2 effect.** D2 does not answer Q5.
- **Resolution.** 04-01 reconciles S3 with A9. Faithful recording by any recorder is permitted as a record shape (settled). What stays open is only whether a particular host requires capture by its own facility: the host names and enforces its own list (V4-HI-30; D2), so this is a DEP-001 host question and not OI-001. Receivers keep their text. 04-03 E2 and VC-04 add "conformant as shape; host capture requirement per host".

### D-12 MAJOR — "Checked" has at least five senses

- **Supplier.** A4 "Mark checked" is the human act, now reserved by D2(a). S1 and §4.2 say "later-check route". §7 has a label rule for accept and approve only; there is none for "checked".
- **Receivers.**
  - 04-02 §8 standing facet "Host checks": value **checked**, which "here means *host checks passed*".
  - 02-01 §4.4 promised standing "*agent-checked (non-mutating)*".
  - E1 step "Check" with `‹C: run stress check›`.
  - 03-01 OP-C3 "Check support spacing". §3 #5 "includes non-mutating checks".
  - 05-01 §9 and 05-02 §3.4 "Agent check".
  - 04-02 §7, 03-02 §4.4 and 05-02 §5 "check route" / "later-check route".
  - The basis itself uses the word both ways: d3 "the agent checking the engineer's work" and V4-HI-12 "checks passed".
- **Assessment.** 04-02 and 05-02 each separate the senses locally. There is no shared rule, and 02-01's "agent-checked" standing is the kind of label S4 and X-19 warn about.
- **Resolution.**
  - 04-01 v0.2 adds a label rule. Unqualified "checked" / "Checked" is reserved for A4. Host results say "host checks passed: ‹named checks›". Agent work is "examination" / "findings". "Later-check route" is access for later examination or checking and implies no act.
  - 04-02 renames its facet value to "host checks passed".
  - 02-01 renames "agent-checked" to "agent-examined (non-mutating)".

### D-13 MAJOR — "Approval" overload in the hosting boundary (the D3 focus)

- **Supplier.** A14 is a separate subject: "must not be confused with an attributable human or professional act". §7 and F-2 note that harness tool-permission "approvals" are A14, not A5 or A6. D3 now rules: "routine tool-permission and sandbox modes (including any classifier-based mode) remain the user's own Codex setting per project/turn. They govern tool execution only".
- **Receiver.**
  - 01-01 R7: "Which answers an **autonomy policy** may give automatically is `UNRESOLVED{OI-001}` / `UNRESOLVED{OI-002}` (**DEL-04-01/04-02**)".
  - H9: "Approval, sandbox … settings … (DEL-01-05; **policy per DEL-04-01/04-02**)".
  - These tie supplier tool-approval answers to the host-operation autonomy grant. 04-02 §2 explicitly excludes that subject ("not shown inside this autonomy display as a grant").
  - 01-01 R8 is correct and agrees (AG-12).
- **Resolution.** 01-01 v0.2 cites D3 in H9, R7, the §2 table, U-04 and F-09:
  - Approval and sandbox modes are the user's own Codex setting, carried unchanged (DEL-01-05 for settings, DEL-01-04 for answers).
  - The DEL-04-01/04-02 autonomy grant governs host operations only.
  - No App rule answers affirmatively.
  - U-11, automatic decline, stays open.

  04-01 V-21 lists DEL-01-01 as a consumer. See also RF-03.

### D-14 MINOR — Who decides A14

04-01 A14 decision actor: "The person". 01-01 §6.1 settlement origin allows `app-rule:<named rule>` and `app-explicit-error` for declines and errors (R2, R3). Under D3 a supplier-internal classifier mode may also settle without any App answer.

**Resolution.** 04-01 A14: affirmative answers come from the person, or from the user's own Codex mode inside the supplier (D3). The App only issues an explicit decline or error, under a named rule with truthful origin.

### D-15 MINOR — Who may withdraw

04-01 A11: "The proposer | Its own proposal". 03-02 §4.1 "withdrawn | Proposer **or person** withdrew it", and U-P6 puts the withdrawal class under OI-001. D2 does not reserve withdrawal.

**Resolution.** 04-01 states whether a person removing an agent's proposal is A10 (reject) or A11. 03-02 aligns and drops the OI-001 tag from U-P6.

### D-16 MINOR — Host refusal appears under "rejected"

03-02 §4.1 "rejected | The person (act recorded by host) **or host refusal on validation at application (U-P5)**". Under 04-01, A10 is a person's act, and a host refusal is an A2 outcome ("refused with reason").

**Resolution.** 03-02 moves host refusal to a refusal outcome and keeps "rejected" for A10 only. U-P5 stays host input.

### D-17 MINOR — Grant change is not recorded as an act kind

04-03 HA-5: "recorded in R6 with the person as setting actor. Whether it is also a named act kind is a DEL-04-01 reconciliation point (U-08)". 04-02 U-04 says the same. 04-01 names it A12, and D2(e) reserves it.

**Resolution.** 04-03 records A12 through a human-act record, or R6 entries cite A12 act evidence. U-08 closes for grant change.

### D-18 MINOR — Recording-mode terms

04-03 §6.1 "*direct capture* (recorder captured the person's act in its own interface) or *faithful recording* (recorder ≠ capturing surface …)". 04-01 A9 covers any recorder distinct from the decision actor, including a host facility.

**Resolution.** 04-01 states that A9 covers both. 04-03 keeps *recording mode* as a sub-element under A9.

### D-19 MINOR — Act class on the human-act record

04-03 §6.1 "Act class | The operation's policy class at the time … | Yes (value or 'unresolved')". 04-01 §2.4 has no class element. A4 performed in the host UI may involve no catalog operation.

**Resolution.** 04-03 makes the element "as applicable" and allows "reserved to the person (D2)" for act kinds. 04-01 adds an optional *governing policy reference* to §2.4.

### D-20 MINOR — Which acts a checkpoint may require

04-01 §2.3: "(A4–A7, **or another human act the workflow declares**)". 02-01 §4.3.1: "Exactly one human act kind, named by its DEL-04-01 accepted name", with FB-04.

**Resolution.** 04-01 enumerates the acts a checkpoint may require: A4–A7, plus any companion act it permits, such as A12. 02-01 keeps its closed list.

### D-21 MINOR — Recorder for approval

05-02 §5 "Approval | Person | **Host**". Acceptance and marking checked allow "Host (or a faithful recorder)". 04-01 A9 applies to A4–A7 uniformly.

**Resolution.** 05-02 aligns the approval row after D-11.

### D-22 MINOR — Grant vs class in PC-22

05-02 PC-22 "geometry **stays proposal-only** (V4-EXM-22 shape)". V4-EXM-22 says the engineer "keeps proposals for model geometry", which is a person grant of *propose*. It is not the unwidenable catalog class *proposal only* (04-01 W-d).

**Resolution.** 05-02 rewords the case as "the grant keeps geometry at propose".

### D-23 MINOR — OI-002 used as a class value

03-01 §3 #8 allows `UNRESOLVED{OI-002}` as a class value, while its own rule says routine permission and human act "are never encoded in the same element value". 04-01 §6 class values have only OI-001. D3 now rules that hosts have no classifier mode.

**Resolution.** 03-01 removes OI-002 from element 8. 03-02 §2 and §9 drop "OI-002" from *not permitted*.

### D-24 MINOR — Missing host-outcome and act rows

05-01 §2.3 "Host outcome … (ran, refused with reason, stale, queued, applied with receipt reference, outcome unknown)". §9 has no reject or withdraw rows.

**Resolution.** 05-01 adds accepted, rejected and withdrawn, relayed with actor (A5, A10, A11).

### D-25 MINOR — Lapse granularity owners point at each other

04-03 U-07 "Partial-lapse effect … | **DEL-04-01** with Owner". 04-01 U-10 "Batch acceptance as one act or many | **DEL-04-03**", and §5 "Each accepted proposal row is bound to its own proposed content".

**Resolution.** 04-01 states that per-row binding means per-row lapse for A5. For multi-row A4, whether the purpose survives stays an owner question with a named owner. This overlaps V1-B.

## 4. Absent inputs

| # | Absent element | Receiver needing it | Owner | Point of need |
|---|---|---|---|---|
| AB-01 | Rule for an **unconfirmed** grant. 04-02 §3 proposes "most conservative … (proposal where uncertain)" and its U-05 names DEL-04-01. 04-01 §4.3 rule 7 covers only "no person grant recorded" | DEL-04-02 | DEL-04-01 with host policy owner | Before DEL-04-02 OUT-001 |
| AB-02 | Whether workflow **review/registration** (V4-WF-02) is a named act kind. 04-01 §2.2 says "not enumerated here"; 04-03 U-08 and §10 ask DEL-04-01 | DEL-04-03; DEL-02-02 (later undertaking per D1) | DEL-04-01 with DEL-02-02 | DEL-04-03 record v0.2 |
| AB-03 | Lapse of a performed checkpoint act returns the hold. Stated by 02-01 I-4 and 05-01 C-4, but not in 04-01 §2.3 | DEL-02-01, DEL-02-03, DEL-05-01 | DEL-04-01 (DERIVED from S6, S9) | Before the DEL-02-03 hold design |
| AB-04 | **Consequence** vocabulary (04-01 U-06). No receiver carries a consequence statement: the 03-01 entry has no such element, and 04-02 and 04-03 scopes lack it (see D-07) | DEL-03-01, DEL-04-02 | DEL-04-01 with host policy owner | Before class assignment in DEL-03-01 |
| AB-05 | How A14 settlements relate to run and act records (04-01 OI-002 Q4). D3 does not answer it. 04-03 U-02: "whether it appears in R6 is open" | DEL-04-03, DEL-01-02 | DEL-04-01 with DEL-04-03 (no longer an owner OI after D3) | DEL-04-03 record v0.2 |
| AB-06 | Host capture requirement per act kind (the residue of 04-01 OI-001 Q5 after D-11) | DEL-04-03, DEL-05-02 | Host owner (DEP-001) | Before host act-recording integration |
| AB-07 | **Policy revision identity** (04-01 §6). Receivers cite "policy source" (03-01), a "decision-basis reference" (04-03) or "governing policy" (03-02), but no revision | DEL-03-01, DEL-03-02, DEL-04-03 | DEL-04-01 (representation-neutral) | v0.2 of each |
| AB-08 | Receiver DEL-02-03 (DEP-04-01-013, in D1 scope) has no Wave-1 design, so the checkpoint-hold consumption of V-03 and V-09 was not compared | DEL-02-03 | WORKING_ITEMS / W7 | When DEL-02-03 is drafted |
| AB-09 | Operation-specific reserved additions for the first connected operation (D2 last sentences) | DEL-03-01, DEL-05-01, DEL-05-02 | Owner via outside SWB session (OI-021) | Before connected SoW |
| AB-10 | An adopted-decision record for D2 and D3 in 04-01 §6 form (decision basis `APP-V4-FIRST-INCREMENT-20260928-DECISION-1`, actor Ryan, 2026-09-28, recorder HELP_HUMAN). §6 currently says "Adopted decision is currently empty" | All receivers | DEL-04-01 (R1) | R1 |

## 5. Where owner rulings D2 and D3 change v0.1 statements

| File and location | v0.1 statement | Effect of D2 / D3 |
|---|---|---|
| 04-01 §3 "Not settled", §6 "Adopted decision is currently empty", §4.3 rule 4, §8.2 V-20/V-21, §10 OI-001 Q2/Q3/Q7 and OI-002 Q1–Q3, U-01, U-02, FX-16/18/23 | OI-001 and OI-002 open; no adopted decisions | D2 reserves (a) marking checked, (b) accepting a proposal where autonomy requires one, (c) engineering approval, (d) reliance, (e) grant change and external enablement. It adds that the host names its own list, that no grant widens past a reserved act or checkpoint, and that additions come at OI-021. This answers Q2, Q3 and Q7. Q1 moves to OI-021. **Not answered:** Q4 (reject; D2 does not reserve it at App/shared level), Q5 (recorder), Q6 (consequence vocabulary). D3 answers OI-002 Q1–Q3 (App: user's Codex setting; hosts: no classifier mode, SWB default proposal applies; tool permission never stands in for a reserved act). Q4 stays open (AB-05). FX-23 is no longer AWAITING (grant change is reserved). FX-18 in a host becomes non-conformant (no classifier mode), and in the App it is the user's setting |
| 04-01 §3 last sentence | "pending … D2/D3 have no recorded owner answer" | Superseded by OWNER_DECISIONS.md |
| 04-03 §0, §6.1 act class, HA-5, HA-6, U-01, U-02, U-08 | Class values `UNRESOLVED{OI-001}` throughout; grant-change kind open; routine permission open | Reserved acts are now adopted, with class carried with a decision basis. Grant change is a reserved act (D2e). U-02 narrows to AB-05 |
| 04-02 §0, §2 "Policy bound", §2 routine-permission bullet, U-01, U-02, U-04 | Class values unresolved; routine permission `UNRESOLVED{OI-002}` | D2(e) makes grant change reserved (see D-06). D3 confirms routine permission is outside the autonomy display: App = user's Codex setting; host = none |
| 03-01 §3 #8, class rules, OP-C4/C5/C6, UNRESOLVED OI-001 and OI-002 rows | OP-C6 unresolved; OI-002 as a class value | OP-C6 is reserved (D2a). OP-C4/C5 are pending OI-021 additions only. OI-002 is removed as a class value (D3; D-23) |
| 03-02 §2, §9 "not permitted", §10 rules, U-P6, UNRESOLVED rows | "which acts are always reserved remains `UNRESOLVED{OI-001}`, and classifier-based routine permission `UNRESOLVED{OI-002}`" | D2 list applies. D3: no classifier mode in hosts. U-P6 (withdrawal) is not covered by D2 |
| 02-01 §4.3.2 bullets 3–4, U-05, U-06, EX UNRESOLVED last row | "A checkpoint does not decide whether the act kind is always reserved … `UNRESOLVED{OI-001}`" | A4–A7 are reserved at App/shared level (D2a–d). Checkpoints still hold regardless. The statement that a checkpoint is not a permission prompt is now backed by D3 |
| 05-01 §2.2 tool offering class, §2.4, §9 A-4, UNRESOLVED OI-001 and OI-002 rows | "The loop carries whatever DEL-04-01 adopts. It holds no default of its own" | D3: hosts have no classifier permission mode, and the SWB default proposal mode applies. The loop now carries a ruled value, not an open one. Operation-specific classes wait on OI-021 |
| 05-02 K-4, W-6, PC-23, UNRESOLVED OI-001 and OI-002 rows | Reserving marking checked, and classifier effect on checking, both unresolved; PC-23 HELD | D2(a) reserves marking checked. D3 means no classifier mode in hosts. PC-23 can carry expected results for its classifier sub-cases (a classifier auto-grant in the host is non-conformant). Only operation-specific additions stay HELD (OI-021) |
| 01-01 §2 row "Approval/sandbox policy …", H9, R7, U-04, F-09 | `UNRESOLVED{OI-002}`; "D3 recommendation pending" | D3 rules the App side: the user's own Codex setting per project/turn, governing tool execution only. This is consistent with the D-GOV-43 row, which moves from open to adopted-by-owner for the first increment. R7 must stop routing this through DEL-04-01/04-02 (D-13) |
| 01-01 U-01, §10, R5 ("pin's generated types") | Pin `UNRESOLVED{OI-012}` | D4 (outside V1-A focus): pin 0.158.0 selected. Noted only |

## 6. Register findings (`Dependencies.csv`)

Rows checked: DEL-04-01 DEP-04-01-012…021; DEL-04-02 DEP-04-02-007/-008/-009/-011/-012; DEL-04-03 DEP-04-03-011…020; DEL-03-01 DEP-03-01-022…030; DEL-03-02 DEP-03-02-016…019; DEL-02-01 DEP-02-01-018/-019; DEL-05-01 DEP-05-01-018/-019; DEL-05-02 DEP-05-02-008/-009/-014/-015; DEL-01-01 DEP-01-01-016…024.

| # | Finding | Rows | Suggested owner action (not performed here) |
|---|---|---|---|
| RF-01 | DEL-04-03 has **no UPSTREAM row** targeting DEL-04-01. It mirrors neither DEP-04-01-016 (DOWNSTREAM HANDOVER to DEL-04-03) nor its own design's "DEL-04-01 (act kinds, act classes)" input. There is only an OI constraint, DEP-04-03-019 | DEP-04-01-016; DEP-04-03-011…020 | Add a DEL-04-03 UPSTREAM INTERFACE row to DEL-04-01 (C1 or WORKING_ITEMS) |
| RF-02 | DEL-04-01 has **no DOWNSTREAM rows** for three receivers that declare it upstream: DEL-03-02 (DEP-03-02-017), DEL-05-01 (DEP-05-01-018) and DEL-05-02 (DEP-05-02-008). This confirms 04-01 F-1 | DEP-04-01-012…016 | Add mirror rows in DEL-04-01 |
| RF-03 | DEL-01-01 has **no row** for DEL-04-01, OI-002/D3 or DEL-01-04, although H9, R7 and §11 cite "policy per DEL-04-01/04-02" and `UNRESOLVED{OI-002}`. DEL-04-01 V-21 also omits DEL-01-01 | DEP-01-01-016…024; DEP-04-01-012…016 | Preferred: repair R7/H9 per D-13, so that the constraint is D3 via DEL-01-05/01-04 (existing DEP-01-01-021/-022/-024 then suffice). Otherwise add an OI-002 (now D3) constraint row |
| RF-04 | OI-001 and OI-002 constraint rows are present in DEL-04-01 (-017/-018), DEL-04-02 (-011/-012), DEL-04-03 (-019) and DEL-05-02 (-014/-015). They are **absent** from DEL-03-01, DEL-03-02, DEL-02-01 and DEL-05-01, whose designs all carry `UNRESOLVED{OI-001/002}` rows. After D2/D3 every such row should point at the decision record | as listed | C1 reconciles the pointers (OWNER_DECISIONS "Effects" says rows are not rewritten by that record) |
| RF-05 | DEL-05-01 and DEL-05-02 have no DEL-04-02 row, but 04-01 V-03/V-04 have DEL-05-01 "consult per operation" and 05-02 F-3 needs the active scope display | DEP-05-01-018/-019; DEP-05-02-008/-009 | Decide at the SoW level whether the loop and panel consume DEL-04-02 directly or through DEL-04-01/03-02 |
| RF-06 | Mirrors verified as consistent: DEP-04-01-012 ↔ DEP-02-01-018; DEP-04-01-014 ↔ DEP-03-01-024; DEP-04-01-015 ↔ DEP-04-02-007 | — | None |

## 7. Prioritized repair list for R1

1. **DEL-04-01 v0.2 first** (the receivers depend on it):
   1. canonical act names and alias table (D-01);
   2. D2/D3 adopted-decision records in §6 form (AB-10), and §3/§10 updated per §5 of this file;
   3. SWB model-change class marked DERIVED (D-02), and the rule that act-performing operations are *reserved* (D-03);
   4. the treatment → runtime-outcome map, with *channel not enabled* separated from *unavailable* and the evaluation point named (D-04, D-05);
   5. the checkpoint rules: A5-requiring checkpoint forces *propose* (D-09), decision pairs and negative decisions (D-10), lapse re-opens the hold (AB-03), and the enumerated checkpoint act set (D-20);
   6. S3 and A9 reconciled on faithful recording (D-11), and the A9 modes (D-18);
   7. a "checked" label rule (D-12);
   8. the A14 actor with D3 and an App-rule decline (D-14);
   9. resolution timing and the U-09 owner (D-08), plus the unconfirmed-grant rule (AB-01);
   10. withdraw vs reject by a person (D-15), per-row lapse for A5 (D-25), and a decision on registration (AB-02);
   11. V-21 consumers to include DEL-01-01, and mirror rows (RF-02).
2. **DEL-04-02**: split agent-requested from person-set-unconfirmed, with separate requester and setting actor in settings-in (D-06); add the grant **scope** element (D-07); rename the "checked" facet (D-12); drop the blanket class-unresolved statement (D-02).
3. **DEL-02-01**: adopt canonical names and drop V4-CON-05 from *approve* (D-01); fix E2 R-5/VC-11 (D-09); separate negative resolution from *performed* (D-10); rename "agent-checked" (D-12); apply the D2 reserved list (§5).
4. **DEL-03-01**: SWB model-change class per V-11 (D-02); OP-C6 reserved (D-03); remove OI-002 from element 8 (D-23); cite the outcome map (D-05).
5. **DEL-01-01**: rewrite H9, R7, the §2 row, U-04 and F-09 on D3, and stop routing tool-permission answers through the autonomy grant (D-13, RF-03).
6. **DEL-04-03**: canonical names (D-01); record A12 (D-17); recording mode under A9 (D-18); make act class "as applicable" (D-19); mirror scope and requester in R6/§8 (D-06, D-07); add an UPSTREAM DEL-04-01 row (RF-01).
7. **DEL-03-02**: withdraw actor (D-15); host refusal out of "rejected" (D-16); drafting-time vs resolution-time standing (D-08); not-permitted per the map (D-05).
8. **DEL-05-01 / DEL-05-02**: carry D3 (no host classifier mode) and D2(a) in K-4/W-6/PC-23/A-4; names (D-01); outcome and act rows (D-24); approval recorder (D-21); PC-22 wording (D-22); negative checkpoint branch (D-10).
9. **Registers (C1 / WORKING_ITEMS)**: RF-01…RF-05.

## 8. Counts

- Agreements: 19 (AG-01…AG-19).
- Disagreements: 25. BLOCKING 1 (D-01); MAJOR 12 (D-02…D-13); MINOR 12 (D-14…D-25).
- Absent inputs: 10 (AB-01…AB-10).
- Register findings: 5 defects (RF-01…RF-05) and 1 verified-consistent note (RF-06).
