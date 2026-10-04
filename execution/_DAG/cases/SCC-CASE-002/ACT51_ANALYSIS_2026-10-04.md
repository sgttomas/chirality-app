# SCC-CASE-002 — ACT §5.1: DEL-04-01's five semantic inputs (2026-10-04)

- **Run:** `APP-V4-GRAPH-CLOSURE-20261004`. The assignment is HELP_HUMAN's message to owner O-A, under the common brief `CASE_BRIEF_COMMON.md`.
- **Author:** a Type 2 TASK agent (Claude Opus 5.5, owner notes O-A). No delegation. Read-only git.
- **Standing:** analysis for the owner's checkpoint. **It decides nothing.** It changes no Design file, register, ScopeOfWork or `_DAG` version. "Proposed" means a later brief may take it up. Cut and merge are the owner's (doctrine §2 rule 3).
- **What it answers.** M-Q-ACT-N (`MOVES_PROPOSED_2026-10-04.csv`) asks whether ACT §5.1's inputs become register rows. For each input, this file answers three questions:
  1. Is it I or E under G1 r3's K-3?
  2. Can ACT be reworded so that DEL-04-01 states its rules in its own vocabulary, with the suppliers' instances arriving only at runtime (GC-1, GC-3)?
  3. If an input must stay I, which move closes its cycle, and does that move need an owner act?
- **Paths:** `E/` is `projects/chirality-app-v4/execution/`. `ACT` is DEL-04-01 `Design/ACT_AND_POLICY_CONTRACT.md`.

## 0. Basis and checks

Read at HEAD `bb81cedb6a`. SCC-CASE-002's §23 and the CSV's E-residual rows were committed at `fdc713c439`, with the hashes below. Every file below was hashed when read.

| File | sha256 |
|---|---|
| `E/_Coordination/AgentRuns/APP-V4-GRAPH-CLOSURE-20261004/SURVEY/G1.md` (r3) | `3d6543bc2a05e5e62cb9673c1d3177386f484de38d9058a0b396eee9299f0a45` |
| `…/GC_RULINGS.md` (GC-1…GC-4) | `27265cc9245fd7c2d93096dd8f2978376b51c48daf0e77fc110ced4c7c3318dc` |
| `…/CASE_BRIEF_COMMON.md` | `c83e0f86ca55c26ddc6abd2cfa817256fd6ed42f6013a926b72016825c703468` |
| `…/reviews/RVG-C2.md`, committed text, Addenda A and B. A later uncommitted edit by another agent was not relied on | `0736ec4cf9bf47d3a3a82eb40230b566403e8d98f85b77dae702cbc7377e6629` |
| `E/_DAG/cases/SCC-CASE-002/PAIR_ANALYSIS_2026-10-04.md` (§1–§23) | `139fd8ea6927746c0aa22bad11bd700161d3f477042e4368b481ad94c001054a` |
| `E/_DAG/cases/SCC-CASE-002/MOVES_PROPOSED_2026-10-04.csv` | `daab5d298d98569dd00e79f90ba0e3afdc7ae8452bce2d279c6e42729ac80432` |
| ACT (ACT-POLICY-v0.11) | `597f13bda1fe1c1fa97b9db8ebc92483c2b43ebcbdc784d91be1f57fa93df5f2` |
| DEL-04-01 `Design/ACT_POLICY_CLASS_RECORD.schema.json` | `694a284f48155ab7a7d0e24d47ec809a06ec3a909dbb104a28374164d3f6cb7e` |
| DEL-04-01 `ScopeOfWork.md` | `2cd1dc9e542a9ee38ee0dd2a217bd717ecd960b2df009f59b4b2c562d350d862` |
| DEL-04-01 `Dependencies.csv` | `bde049827079db9afa16a46a3a752a1f9cfbd92156655502553cbe421fa986c9` |
| DEL-04-02 `Design/AUTONOMY_AND_STANDING_EXCHANGE.md` (AS-v0.9) | `4eca598f13c8c0745f94c605b8940a094b55e57b9f7478c989824af229085857` |
| DEL-03-02 `Design/PROPOSAL_LIFECYCLE_AND_OUTCOMES.md` (P-v0.8; §3.3 only) | `ad6a3083e7b808e247562fa0cc3762192b121ff99e75e8ac8167ab25da555eb3` |
| DEL-02-03 `ScopeOfWork.md` | `625b299ec1d48de1b80dff74796774cc95ee466870bec06a196e16b840af6e5f` |
| `APP-V4-FIRST-INCREMENT-20260928/R1_RESOLUTIONS.md` (R-3, R-5, R-7, R-8) | `2f9c7e72aa8362624ad830377a70077b27a27bf03871f8e87811a28e6e177ec4` |
| `…/R2_RESOLUTIONS.md` (R2-6) | `77cfb845ec305365f12218f83f332069155de5f362139b7a6fe2bf12cdebd088` |
| `…/R4_RESOLUTIONS.md` (R4-6) | `50a009b2ef487bad6ef5e89b5c4493095f18f83149fcb83b00050de485032a24` |
| `E/_DAG/DAG-004/DependencyEdges.csv` / `CandidateEdges.csv` | `c43033742df768a6fb493701d25b1d73240366172c05b1d0caa143650690966e` / `2bfff10e3094d7fd86da563006c965694563ec10d0fc78e9b1d9958fefa42025` |
| Scratch script `$TMPDIR/act51/act51.py` (not in the repository) | `1381f3e47d3a25b7fb1dd5de54f30f9da758c912c3aa511833937c14c2e2f204` |

**Checks run** (all scripted, own code):

| Check | Result |
|---|---|
| G1 r3 kinds parsed from G1's row tables (§2 held, Appendix A admitted) | 212 arcs, all classified (P 43, I 156, V 5, L 5, E 3). Every consumer → supplier pair in G1 equals the DAG-004 arc direction |
| Baseline | SCC-002 is 13 members / 21 rows under O-1. Under O-2…O-4 it is 12 members with 18 / 18 / 17 rows. All equal G1 §1.3 |
| C2's move set, as modelled in §4 | Reproduces §21.8 scenario C (O-1 12/6; O-2 and O-3 P13; O-4 acyclic) and every §23.2 line (C+E×5 O-1 12/10, O-2 and O-3 5/5; B 12/11; D 12/8; +P19 12/11 and 5/6) |
| §21.2 / §22.5 table | Reproduced exactly: operation identity is a 2-cycle under O-2…O-4 and 15/7 under O-1; grant state 12/1 and 15/7; checkpoint state 11/3 and 15/9; all five 12/5 and 15/11 |
| Admitted arcs into DEL-04-01 | 20 consumers. DEL-04-01 consumes nothing (no admitted or held arc) |

"m/r" means a component of m members whose exact minimum cycle-closing set is r rows (minimum feedback arc set, dynamic programming over member subsets).

## 1. Short answer

| Input (ACT §5.1) | Supplier named | Kind today (K-3) | Reword in ACT so it is DEL-04-01's own vocabulary? | Residual after rewording | Owner act needed |
|---|---|---|---|---|---|
| *grant state* | DEL-04-02 | **I** | **Yes.** ACT §5.1, §5.3 rule 7, §5.4, §10.1 V-04, §11, with fixtures FX-19/20/23 and §7 | None | **None**, under any option |
| *checkpoint state* | DEL-02-01, DEL-02-03, DEL-05-01, and also P §3.3 (DEL-03-02) | **I** ×3 (RVG B-n1). P §3.3 is **L** (governance phase) | **Yes.** ACT §5.1, §5.3 rule 2, §4.0 AP-10, §4.4's carriage bullet | None | **None**, under any option |
| *operation identity and class* | DEL-03-01 (classes host-named) | **I by text only.** The schema already meets GC-3 conditions 1–2 | **Yes.** ACT §5.1, §8.1 rows, and two schema descriptions | None | **None**, under any option |

- **Why no residual (§3).** DEL-04-01 is a contract. It receives no instance. The host route resolves treatment (R-3 point 1; ACT §5.3), so runtime values flow among the host route and the suppliers, not into DEL-04-01. This is C2's own reasoning for P4 in §23.1: "DEL-03-02, as a contract, receives no instance."
- **Effect.** With the rewordings, M-Q-ACT-N's owner question is answered by design: DEL-04-01 gains no supplier row. SCC-002's closure is exactly C2 §23.2, and ACT §5.1 adds nothing under any option.
- **Fallback.** If a rewording is refused, that input stays I and closes a cycle with an admitted reverse row under **every** option. It then needs an owner act; the smallest is a per-edge cut (§2.4).
- **Larger exposure found.** ACT cites the same suppliers outside §5.1, which G2 did not survey (§6):
  - §2.4 cites EXEC §4.10;
  - §4.0 and §4.3 adopt WD and EXEC rules by citation;
  - §4.4 cites P §3.3, ADAPTER and LOOP;
  - §6 uses C §4.1 and P §9;
  - §2.7 cites LOOP's network rules;
  - §13 takes its fixture subjects from C §10.

  Any one of these, entered as an I row, re-forms a cycle. So "DEL-04-01 has no supplier" needs the §6 passages handled too, not only §5.1.

## 2. Per input

**The reciprocal rows.** Each supplier already consumes DEL-04-01 through an admitted row, all I under G1 r3 Appendix A:

| Admitted row | Consumer → supplier | Kind | Deciding sentence |
|---|---|---|---|
| DEP-04-02-007 | 04-02 → 04-01 | I | EQ: "This deliverable consumes those policy and record contributions." |
| DEP-02-01-018 | 02-01 → 04-01 | I/V | ST: "Receive adopted human-act distinctions … for checkpoint declarations and VER-003 examples" |
| DEP-02-03-012 | 02-03 → 04-01 | I | EQ: "Use only the identified adopted operation policy for dependent cases" |
| DEP-05-01-018 | 05-01 → 04-01 | I/V | ST: "Receive the adopted operation-policy/human-act distinction contract for checkpoint/event/evidence examples" |
| DEP-03-01-024 | 03-01 → 04-01 | I | EQ: "App v4 DEL-04-01 supplies adopted classes before an affected operation-policy representation is fixed." |
| DEP-03-02-017 | 03-02 → 04-01 | I | EQ: "adopted policy distinctions from DEL-04-01 are definition inputs." (the supplier of P §3.3; see §2.2) |

**What DEL-04-01's ScopeOfWork says.**
- CLM-002 lists the five suppliers' ownership, then says: "This deliverable supplies their policy meaning without taking over their production."
- REQ-007 assigns declaration to DEL-02-01, checkpoint execution to DEL-02-03, catalog schemas to DEL-03-01 and the autonomy and standing UI to DEL-04-02. It ends: "Supplying policy requirements and receiving attributable evidence remain this deliverable's work."
- Neither states any consumption of a grant state, checkpoint state or operation identity. Its register (`Dependencies.csv`, 33 rows) has DOWNSTREAM rows DEP-04-01-012…016 and -025 to these suppliers, and no UPSTREAM row to any of them.

**Reading.** The ScopeOfWork places DEL-04-01 upstream of all five, and the registers agree. Only the Design text of ACT §5.1 names them as suppliers. The cycle is therefore a **projection artefact** of how ACT words its inputs, not a part-level contradiction:
- DEL-04-01's part (defining resolution rules) needs no supplier definition once the rules are stated over its own terms;
- the suppliers' parts consume those terms through the admitted rows.

### 2.1 Grant state (DEL-04-01 → DEL-04-02)

**ACT today.**
- §5.1: "*grant state* for the class | **effective (person-set)** · **effective (policy default)** · requested by agent (A8) · set by person, not yet confirmed · unconfirmed · not set · refused (reason). Each state carries a **grant value** (direct/propose) and a scope. | DEL-04-02 (R-8; R2-6)".
- §5.3 rule 7 is rule-bearing on these states ("**effective (person-set)** with grant value *direct* and the operation inside the scope → *apply directly*"; "Requested by agent, set but not confirmed, unconfirmed or refused → no direct branch").
- §5.4 repeats them. §10.1 V-04 lists "the seven states" as a value ACT carries, with DEL-04-02 among its consumers. §11 has "Autonomy and standing UI, grant states | DEL-04-02 | Supply V-04, V-08".

**The supplier.**
- AS §2 is headed "Grant model received", "Received from DEL-04-01 §5 and §8": grant value, scope, A12.
- AS §3 "Grant display states" defines the seven states under "(R-8; R2-6)", with entry evidence and a **"Direct branch?"** column: "Yes, if grant value is direct"; "Only if the record's default is *direct* — none in the first increment"; "No" for the rest. It also says "Display is derived; the control (App or host) is the authority for the current grant".

**The rulings and ScopeOfWork.**
- R-8 is headed "(owners: DEL-04-02, DEL-04-03)" and lists "**Grant display states**". It adds, as policy: "The direct branch applies only in the **effective** direct state." R2-6 adds *effective (policy default)* and "A default opens the direct branch only if the policy record's default is *direct*".
- DEL-02-03 ScopeOfWork assigns "grant display definition to `DEL-04-02`" (REQ-006) and says "`DEL-04-02` owns grant display states" (CLM-002).

**Q1: kind today is I.**
- The seven states are DEL-04-02's display states (R-8; DEL-02-03 REQ-006), and ACT's rule 7 is rule-bearing on them. ACT does not define them.
- V-04 claims to supply them, which contradicts R-8's owner line. The text is internally inconsistent, and the ruling decides it.

**Q2: rewording. Yes.** ACT needs only the policy part, which R-8 and R2-6 themselves phrase as policy: whether a direct branch is open. AS's "Direct branch?" column is already the mapping of AS's states onto that.

| File and section | Change (design agent: **DEL-04-01**) |
|---|---|
| ACT §5.1, *grant state* row | Rename to *grant standing* for the class, with four values in ACT's own terms:<br>- **direct in force**: a person-set grant value *direct*, by an A12 whose control relation is *established* (§2.4), with the operation inside its scope;<br>- **default in force**: no person-set grant in force for the class, so the policy-class record's default applies (§8);<br>- **no direct branch**: any other recorded condition;<br>- **unassigned**: no setting and no default.<br>Replace the supplier cell with: "Meaning: this contract (R-8's direct-branch rule; R2-6). Instances: resolved on the host route at validation and application (§5.3), which the host reports. DEL-04-02's display states map onto these values (AS §3, 'Direct branch?'). This contract receives no instance." |
| ACT §5.3 rule 7 | State the four cases over grant standing, keeping the effects unchanged (*apply directly*; the record's default, *propose* for P-03; *propose* available with direct *not permitted*; rule 5 with reason *unassigned*) |
| ACT §5.4 | Keep grant value, scope, requester and setting actor, and the two settings references; these are ACT's under R-8 bullets 2–4. Drop the display-state names. Add (GC-3 item 2): "A settings reference is an uninterpreted string, compared whole; DEL-04-02's settings-in and DEL-04-03's reader resolve it." |
| ACT §10.1 V-04 and §11 | V-04 becomes "Grant by A12, with scope, grant value, the grant-standing values and two settings references". §11's row reads "grant display states: DEL-04-02's (R-8); this contract supplies the grant standing (V-04)" |
| ACT §7 (l.1420), §13 FX-19, FX-20, FX-23, VC-001, VC-006 | Expected results name the grant standing, with AS's display shown as the display. For example, FX-19: "default in force: propose (P-03); displayed *effective (policy default)*" |
| AS-v0.9 §2 (optional, **DEL-04-02**) | One line: "§3's 'Direct branch?' column maps these states onto ACT §5.1's grant standing." AS already states the mapping, so GC-1 (a) holds for ACT without this line |

**Tests.**
- **GC-1 (a).** ACT then uses no state value of AS. The *established* control relation is ACT's own A12 vocabulary (§2.4; R4-6). See §6 on its EXEC citation.
- **GC-1 (b).** The mapping is checked outside ACT: by AS §3 and its fixtures (VC-19 state walk), and by host evidence (DEP-001).
- **GC-3.** The settings references are the only identifiers. They are uninterpreted, resolved by DEL-04-02 or DEL-04-03, and the text says so.
- **GC-4.** No integrator ruling is amended. The rewording aligns ACT with R-8's owner line and R2-6. R-3 point 6 ("Record both") is unaffected.
- **ScopeOfWork.** None. DEL-04-01 OUT-001 already covers "the person-set grant", and no ScopeOfWork states this consumption.

**A latent conflict the rewording exposes, not decided here.**
- ACT rule 7 lists "Requested by agent" among the no-direct cases.
- AS §3 says "agent A8 → *requested by agent* (governing state unchanged)", and AS shows the request "beside the governing state". Under AS, an effective direct grant still governs while a request is open.
- The rewording must take one reading. I would take AS's, which is R-8's "(A8; no person act)". It is a design question for the DEL-04-01 and DEL-04-02 design agents, under review.

### 2.2 Checkpoint state (DEL-04-01 → DEL-02-01, DEL-02-03, DEL-05-01; and P §3.3)

**ACT today.**
- §5.1: "*checkpoint state* | Whether a declared checkpoint applies, the act it requires, and any governing checkpoint constraint | DEL-02-01; DEL-02-03; DEL-05-01; P §3.3".
- §5.3 rule 2:
  - "At a checkpoint: *request the person's act* (S9)";
  - "An A5 checkpoint constraint on this operation forces *propose* (§4.4)";
  - Phase 1 is plan guidance, and "Rule 2 binds on the host route for governed checkpoints in the governance phase".
- §4.0 AP-10: "A checkpoint declared **`governed`** (WD-v0.8 §4.3.1; PROPOSED)".
- §4.4: "The change request carries a **governing checkpoint constraint**: {workflow run, checkpoint name, required act A5, operation} (DEL-03-02 P §3.3)".

**The suppliers.**
- R-5 (owners: "DEL-02-01 declares; DEL-05-01 evaluates in hosts; DEL-02-03 owns hold machine").
- ACT §4 intro: "DEL-02-01 declares checkpoints (WD §4.3). DEL-05-01 evaluates them in hosts. DEL-02-03 owns the hold machine".
- P §3.3, "Governing checkpoint constraint — governance phase (retained; R8-1)": "{workflow run identity, checkpoint name, required act A5, operation identity}. Absent otherwise. In Phase 1 the App carries none".

**Q1: kinds today.**
- **DEL-02-01: I.** "Whether a declared checkpoint applies" and `governed` use WD's declaration.
- **DEL-02-03 and DEL-05-01: I.** Arrival and its evaluation are theirs (R-5), and ACT does not define the form in which it receives them. RVG B-n1: "I would class it I". This is a boundary call.
- **DEL-03-02 (P §3.3): L** by K-6. "governance phase (retained)" governs the whole of P's constraint element, and "In Phase 1 the App carries none".

**Q2: rewording. Yes.** Rule 2 needs three facts, all expressible in ACT's own terms:
1. whether an arrival is open on this operation;
2. which act it requires (§4.1's closed list, ACT's);
3. whether ACT's own §4.4 constraint is in force.

It also needs whether the governance phase binds the checkpoint.

| File and section | Change (design agent: **DEL-04-01**) |
|---|---|
| ACT §5.1, *checkpoint state* row | Rename to *checkpoint standing* for this operation, with values in ACT's own terms:<br>- **none**;<br>- **open arrival requiring ⟨A4 / A5 / A6 / A7 / A12⟩**: an arrival has been observed, and its required act from §4.1 is not yet *performed* in §4.3's sense;<br>- **A5 constraint in force** (§4.4).<br>Each carries **binding: yes or no**, meaning the governance phase holds on it; in Phase 1 none binds. Supplier cell: "Meaning: this contract §4.1, §4.3 (*performed*), §4.4. Instances: reported on the host route by the executor that observed the arrival. In hosts that is the loop under DEL-05-01's contract; App-side it is DEL-02-03's recorder. Each maps its own declaration and arrival data onto these values (R-5). The declaration owner states which declaration element makes a checkpoint binding. This contract receives no instance." |
| ACT §5.3 rule 2 | Restate over checkpoint standing:<br>- an open arrival → *request the person's act*;<br>- A5 constraint in force → *propose*;<br>- the Phase 1 paragraph is unchanged;<br>- "binds on the host route for checkpoints reported **binding**, in the governance phase" |
| ACT §4.0 AP-10 | "A checkpoint the declaration marks **binding** (DEL-02-01 maps its `governed` element onto this; R8-1) is honoured in Phase 1 only as guidance". The WD-v0.8 §4.3.1 citation becomes a pointer to the mapping owner |
| ACT §4.4, the carriage bullet | "The constraint reaches the host route as DEL-03-02's change request carries it (P §3.3), with an assurance (R4-14; R5-2). This contract reads only whether a **host-held** constraint is in force." Any carried {workflow run, checkpoint name, operation} is a set of uninterpreted strings (GC-3). The run identity is resolved by DEL-02-03's run starter, the checkpoint name by DEL-02-01's declaration, and the operation by the catalog owner |

**Tests.**
- **GC-1 (a).** ACT uses no WD field, EXEC or LOOP state value, or P element, provided the §6 items on §4.0 and §4.3 are also re-anchored. Rule 2 itself then reads only ACT's terms.
- **GC-1 (b).** WD, EXEC and LOOP check their mapping. They already consume ACT §4.1 and §4.2 (admitted DEP-02-01-018, -02-03-012, -05-01-018). Host evidence (DEP-001) checks the route.
- **GC-3.** The three identifiers in the constraint are carried only, never parsed, and their resolvers are named.
- **GC-4.** No amendment, as far as read:
  - R-5's owner line is kept;
  - R2-12, R4-14 and R5-2 (carriage) are kept;
  - R8-1 (phasing) is kept.

  R8-11 item 5, on `governed`, was not read (§7).
- **ScopeOfWork.** None.

### 2.3 Operation identity and class (DEL-04-01 → DEL-03-01)

**ACT today.**
- §5.1: "*operation identity* and *operation class* | The catalog operation and its host-named class | DEL-03-01 (V4-HI-01/02); host names classes (V4-HI-30)".
- §8.1: "*class identity* | A host-named operation class (V4-HI-30), or an act-defined class (P-02)"; "*covered operations* | Catalog operation identities and versions (DEL-03-01)".
- In the schema, `coveredOperations[].operationId` is `{"type": "string"}` and `version` is `{"type": "string"}`. `classIdentity` is `{kind: enum ["host-named operation class", "act-defined class"], name: string}`; the `kind` enum is ACT's own.

**The supplier.** DEL-03-01 ScopeOfWork:
- "App v4 DEL-03-02 needs operation identity and original read basis";
- "App v4 DEL-04-01 supplies adopted classes before an affected operation-policy representation is fixed" (the admitted DEP-03-01-024).

The catalog carries ACT's human-act class and ACT's policy-record reference per entry: §8.1 "Reference from a consumer", "DEL-03-01 element 8's policy record reference".

**Q1: kind today.** **I by text** (C2 §21.2: "It uses the catalog identity scheme"). Structurally the row is close to opaque:
- **GC-3 condition 1 holds.** The schema types both identifiers as plain strings, with no pattern taken from C.
- **GC-3 condition 2 holds.** No ACT rule constructs or parses them. Rules 3–8 key on the class value, which is ACT's (§8; V4-HI-02), and on act coverage (P-02, ACT's).
- **GC-3 condition 3 fails, and item 2 is not met.** The text names DEL-03-01 as supplier, not as resolver, and does not say the identifiers are uninterpreted.
- **The class name is not DEL-03-01's.** It is host-named (V4-HI-30), a third party.

**Q2: rewording. Yes, and it is the smallest of the three.**

| File and section | Change (design agent: **DEL-04-01**) |
|---|---|
| ACT §5.1, operation row | "*operation identity* and *class identity* are uninterpreted strings (GC-3). This contract compares them whole, for equality only, with a policy-class record's covered operations and class identity, and never constructs, parses or validates them. Resolvers: the catalog owner for operation identity (DEL-03-01's catalog schema; the host's catalog implementation, CLM-003); the host for class names (V4-HI-30). An operation's catalog human-act class is a value of §8's set, carried per catalog entry (DEP-03-01-024). This contract receives no instance." |
| ACT §8.1, the *class identity* and *covered operations* rows | The same statement: uninterpreted, with its resolver |
| `ACT_POLICY_CLASS_RECORD.schema.json` `operationId`, `version` and `classIdentity.name` | Add a `description` only: "Uninterpreted string; resolved by the catalog owner (operation) or the host (class name); compared whole." No type or pattern changes, so the frozen validator results are unaffected (to be re-run by the design agent) |

**Tests.**
- **GC-1 (a)** holds once GC-3 holds, since no C field, state value or scheme is used.
- **GC-1 (b).** The catalog owner and the host check identity (C's `#/$defs/identity`; DEP-001).
- **GC-3** items 1–2 are met by the text. Item 3 does not bite: no rule needs the identifier's structure.
- **GC-4.** No amendment.
- **ScopeOfWork.** None.
- **Undo (R3-4).** "the policy-class record of the operation whose receipt it reverses" needs the reversed operation's identity. The host route reports it at runtime, and it stays uninterpreted.

### 2.4 Q3: if an input must stay I

Each input, if registered as I, forms a direct 2-cycle with its admitted reverse row. Through DEL-04-01's other consumers it can also pull in further members. The table is computed on C2's §23 model (C, with E×5), with the component that contains DEL-04-01:

| Input registered as I (rewording refused) | O-1 | O-2 | O-3 | O-4 |
|---|---|---|---|---|
| Operation identity | 15/11 | 2/1 {03-01, 04-01} | 2/1 | 2/1 |
| Grant state | 15/11 | 13/6 | 13/6 | 12/1 |
| Checkpoint, DEL-02-01 only | 15/11 | 4/1 {02-01, 03-01, 03-02, 04-01} | 4/1 | 4/1 |
| Checkpoint, DEL-02-03 only | 15/11 | 13/6 | 13/6 | 10/1 |
| Checkpoint, DEL-05-01 only | 15/11 | 13/6 | 13/6 | 11/1 |
| Checkpoint ×3 | 15/13 | 13/8 | 13/8 | 11/3 |
| All five | 15/15 | 13/10 | 13/10 | 12/5 |
| P §3.3 as L (DEL-04-01 → DEL-03-02) | 15/11 | 3/1 {03-01, 03-02, 04-01} | acyclic | acyclic |

At O-1, the 15 members are {01-02, 01-03, 01-04, 02-01…02-04, 03-01…03-03, 04-01, 04-02, 04-03, 05-01, 09-09}.

**Closing move for an input that stays I.** Any of these needs an owner act:
- **CUT, the smallest.** A per-edge objective ruling on the new row (SR-4), with the obligation kept in the register at its point of need.
- **IV-O.** Move the definition into DEL-04-01.
  - For grant state this contradicts DEL-02-03 REQ-006 and CLM-002 ("grant display definition to `DEL-04-02`"; "`DEL-04-02` owns grant display states"), so it is an S2 ScopeOfWork change. It also amends R-8's owner line (GC-4).
  - For checkpoint state it contradicts R-5 and DEL-04-01 REQ-007.
- **DEC of DEL-04-01.** Split §5's resolution order (and §6) from the act and policy vocabulary that the 20 consumers read. This goes through `scope-change`. Not shown to close: AS reads §5.4 as well as §8, so the split line needs design.
- **MRG.** Merge with the supplier.

**Registering as E instead does not help under O-1…O-3.** Computed: all five as E give 15/15, 13/10 and 13/10, and only O-4 is acyclic. E rows sequence under O-1…O-3 (G1 §1.3). A row entered "as E" would therefore be worse than no row at all. That is why §3 matters.

## 3. Why the rewordings leave no runtime residual (RVG B2-M1)

RVG Addendum B holds that "An invert removes the consumer's definitional need. It does not remove runtime instances the consumer still receives." Under K-3 those are E rows. The test is whether DEL-04-01 receives instances. It does not:

1. **DEL-04-01 is a contract.** ScopeOfWork line 16 calls it "This API_CONTRACT". CLM-001 lists its artifacts: "an operation/autonomy and human-act document, adopted policy-class configuration, and reserved-act/semantic-label tests". Nothing in it reads or writes runtime records. That differs from DEL-04-03 ("App reader/writer") and DEL-02-03 (the recorder), whose residuals C2 §23.1 keeps.
2. **Treatment is resolved on the host route.** R-3 point 1: "Treatment is resolved on the **host route** at validation and again at application … The loop and the external adapter relay the actor's intent and do not decide treatment." ACT §5.3 says the same. AS §2: "Governs host operations only." So the App has no component that evaluates §5.3 and would receive these instances on DEL-04-01's behalf.
3. **Host validation and application belong to the external SWBPIPE owner** (DEL-04-01 CLM-003, REQ-007; DEP-001). The runtime join is host integration. Host joins are deferred, and an external dependency is not a deliverable arc.
4. **C2 §23.1 applies the same reasoning to P4:** "DEL-03-02, as a contract, receives no instance."

**One limit (§7).** DEL-04-01 REQ-007 ends "Supplying policy requirements and receiving attributable evidence remain this deliverable's work."
- That is a stated receipt, of act evidence. It is G2's item A2 (DEL-04-01 → DEL-01-04 capture evidence), not one of the §5.1 inputs.
- If dependency-extract reads it as a runtime receipt and enters a row (E), it forms a cycle with DEL-01-04's admitted DEP-01-04-011 under O-1…O-3.
- It is outside this assignment and is not analysed here.

## 4. Closure with the rewordings

**Model.**
- **C2's group 1 (§22, §23.1).** These arcs are removed: P3, P5, P6, P7, P9, P11, P15, P17 and P21. P19 is removed, or E in the "+P19" lines.
- **E residuals:** P10, P12, P18, P20 and M-X2.
- **V residuals:** P1 and P8.
- **P4's identity part:** an L residual in B; cut in C and D.
- **ACT §5.1 under the rewordings:** no row.

| Scenario | O-1 | O-2 | O-3 | O-4 |
|---|---|---|---|---|
| C, E×5, ACT §5.1 reworded (no rows) | 12/10 | 5/5 {02-03, 03-03, 04-02, 04-03, 05-01} | 5/5 | **acyclic** |
| C, E×5 + P19 E, ACT §5.1 reworded | 12/11 | 5/6 | 5/6 | acyclic |
| The same without the rewordings, all five as I (fallback) | 15/15 | 13/10 | 13/10 | 12/5 |

**Reading.**
- With the rewordings, DEL-04-01 is in no SCC under any option, and every figure equals C2 §23.2.
- ACT §5.1 therefore adds **no owner act** under any option. The remaining owner acts are C2's (§23.2, "Group 3 restated"); they are not this file's.
- Other SCCs (001, 003, 004, 005, 006) are unchanged by anything here.

## 5. Owner acts for ACT §5.1, per option

| Option | With the three rewordings (reviewed design changes by DEL-04-01's design agent) | If a rewording is refused and the input is registered |
|---|---|---|
| O-1 | None | One owner act per refused input (CUT smallest; or IV-O with S2, DEC, MRG) |
| O-2 | None | As O-1. P §3.3 as L also needs one |
| O-3 | None | As O-1. P §3.3 (L) leaves with its class |
| O-4 | None | As O-1. P §3.3 (L) leaves with its class |

- **M-Q-ACT-N becomes a design outcome, not an owner question.** DEL-04-01's ScopeOfWork and registers already decide it (GC-2): no supplier row exists, and none is warranted once ACT states its inputs in its own vocabulary.
- **What the owner sees** at the checkpoint, as reviewed design changes: the rewordings, the AS–ACT "Requested by agent" reading (§2.1), and the §6 inventory.

## 6. Other ACT passages with the same exposure (not in G2; inventory, not analysed to the same depth)

G2 surveyed ACT §5.1, §10.1 and §10.3 (G2 l.64). A read of the rest of ACT finds design-level use of the same suppliers. None is a register row today. Each, if entered as an I row, would re-form a cycle through the admitted reverse rows above. Computed for DEL-04-01 → DEL-03-02 (P §9, I): a 3-member component {03-01, 03-02, 04-01}, 1 row, under O-2…O-4, inside the 15-member component under O-1.

| ACT passage | What it takes, and from whom | Likely kind | Treatment in the same pattern (design agent: DEL-04-01) | Ruling |
|---|---|---|---|---|
| §2.4 "A12 and the control relation (R4-6; EXEC §4.10 AR-1…AR-4)"; §2.8 LC-3a | The control relation values *established*, *pending*, *refused* and *unconfirmed*, from DEL-02-03 | I | State them as ACT's own A12 vocabulary, anchored on R4-6, whose text carries the rule ("A refused A12 does not count … A pending A12 leaves the checkpoint *waiting*. A lost confirmation makes it *unknown*"). Drop the EXEC citation. C2 §21.3 (P11) already reads EXEC as the owner, so the two must agree | R4-6 (kept) |
| §4.0 "The execution rules are EXEC-v0.6 §2.1 (PH-1…PH-10) and §2.2 (GV-1…GV-5); the declaration side is WD-v0.8 §4.3.0 (CG-1…CG-7)" | Phase rules from DEL-02-03 and DEL-02-01 | I/L | Re-anchor to R8-1, R8-11 and R9-1/R9-2, as C2-m1 did for WD | R8-1, R9-x (kept) |
| §4.3 "The vocabulary is shared: … (WD §4.3.4)"; "The disposition rule is WD §4.3.7 … which this contract adopts by citation"; EXEC §4.7, §4.9, §4.11, §4.12, HD-5 | Disposition vocabulary and rules, from DEL-02-01 and DEL-02-03 (F-14: "Rules adopted by citation from EXEC") | I | Re-anchor the vocabulary to R-5, whose text lists the six words, and the rules to R2-18, R4-3, R4-4 and R4-7. Or invert: ACT states the act-side meaning, and WD and EXEC cite ACT | R-5, R2-18, R4-x (not all read) |
| §4.4, governance-phase definition | P §3.3's carriage form; ADAPTER §5.1–§5.3 carriage assurances; LOOP §6.2 | L (governance phase) | As §2.2's §4.4 bullet. Leaves under O-3 and O-4 regardless | R2-12, R4-14, R5-2 |
| §6 "Runtime non-success outcomes use DEL-03-01 §4.1. Proposal and operation outcomes use DEL-03-02 P §9 (R-7)" | Outcome vocabularies from DEL-03-01 and DEL-03-02 | I | C §4.1: cite R-3 point 2, whose text lists the four values with their meanings. P §9: R-7 makes P §9 "canonical" without listing it, so ACT §6 rows 4–5 need P's terms. Either ACT §6 maps treatment to "the application outcome (R-7)" without enumerating it and P §9 carries "refused is never A10", or R-7 is amended (GC-4) | **R-3.2, R-7: may need amendment** |
| §2.7 "The network rules themselves are LOOP-v0.8 §5.1.1 (NW-8…NW-16) … the flow they run in is DEL-05-01/LOOP-v0.8 §5.3" | Network-destination rules from DEL-05-01 | I | Not analysed. DECISION-5 and R8-13 carry the person-only grant | — |
| §13 "Subjects come from **C-v0.4 §10**, carried in C-v0.8 §10" | Fixture subjects for OUT-003, a principal output, so K-5 does not make them V | P or I | Not analysed. Candidate: the fixtures become a shared fixture set owned by one side, or a V/test-data row if the owner treats OUT-003's subjects as test data | — |

**Consequence.** "DEL-04-01 gains no supplier" holds today only because no ScopeOfWork sentence and no register row states any of these. A later `dependency-extract` pass over ACT could enter any of them. To make the 60% premise robust ("the DAG won't change"), each needs the same treatment as §2, or an explicit record that it is a citation of a ruling and not a contract input.

## 7. Not established

| Item | Why |
|---|---|
| R8-11 item 5 (`governed`) and R9-1/R9-2, read as cited only | §2.2's AP-10 rewording assumes they allow a mapping owned by the declaration owner. Not checked at source |
| R2-18, R4-3, R4-4, R4-7, R8-13, DECISION-5 | Read only as ACT cites them. Not read at source |
| Whether R-7 must be amended for ACT §6 | §6 above. It depends on how ACT §6 is reworded |
| The "Requested by agent" conflict between ACT rule 7 and AS §3 | A design reading (§2.1), for the design agents and review |
| DEL-04-01 REQ-007's "receiving attributable evidence" (G2 A2) | Outside this assignment (§3). It could become an E row into DEL-01-04 |
| DEC of DEL-04-01 as a fallback | Not shown to close, because AS reads §5.4 as well as §8 |
| Whether `dependency-extract` would enter rows from the §6 passages | That is the workflow's call. The figures here assume no row once reworded |
| §13 fixture subjects and §2.7 network rules | Inventoried, not analysed |
| The kinds of rows not read here | G1 r3's, taken as RVG confirmed them. My parse reproduces G1's counts and arc directions |
