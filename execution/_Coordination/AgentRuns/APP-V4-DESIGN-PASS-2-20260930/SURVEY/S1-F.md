# S1-F — outside suppliers and consumers of the first increment

Run `APP-V4-DESIGN-PASS-2-20260930`, node S1-F. Executor: Type 2 TASK (Claude,
model `claude-fable-5-1`), no delegation. Read-only on project state; this file
is the only file written. Paths are relative to
`projects/chirality-app-v4/execution`.

"The 14" are DEL-01-01, 02-01, 02-03, 03-01, 03-02, 03-03, 03-04, 04-01,
04-02, 04-03, 05-01, 05-02, 09-06 and 09-09. "Outside" means any other App v4
deliverable. Arc direction is consumer → supplier.

Two kinds of statement are kept apart below. **States:** what a file says,
with its location. **Inference:** what I conclude from those statements.

## 0. What was read, and how

| Item | How it was used |
|---|---|
| `BRIEFS.md` of this run ("Common rules", "S1") and `OWNER_DECISIONS.md` | Read whole |
| `_DAG/DAG-003/HANDOFF_STATE.md` | Read whole. `MANIFEST.sha256` checked from its folder: 37 of 37 OK. `SOURCE_MANIFEST.sha256` checked from the execution root: 130 of 130 OK. `_DAG/_LATEST.md` reads `Latest: DAG-003`; `_Evaluation/DAGCurrency/_LATEST.md` reports CURRENT |
| `_DAG/DAG-003/DependencyEdges.csv` (124 rows) and `CandidateEdges.csv` (78 rows) | Parsed with a script (`csv.DictReader`); the row counts equal the HANDOFF's 124 admitted and 78 held arcs. Consumer and supplier derived from `Direction` per the HANDOFF rule |
| Live `Dependencies.csv` of all 41 deliverables | Parsed; for every arc below, every row in either end's register whose `TargetDeliverableID` is the other end was printed and read |
| `_DEPENDENCIES.md` of both ends | Searched for the other end's ID; the matching passages read |
| `ScopeOfWork.md` of DEL-01-02, 01-04, 01-05 | Read whole |
| `ScopeOfWork.md` of DEL-02-02, 02-04, 09-01 | Ontology, Epistemology, Praxeology and Axiology sections read whole (all CLM, OUT, REQ, AC, VER, AX, TBD items); the traceability header and the closing matrix were not read |
| `ScopeOfWork.md` of the other 25 deliverables touched by an arc | The items the register rows cite, read by item ID (listed per arc below). Not read whole |
| The 17 first-increment Design files | Searched for every outside deliverable ID (count table in §4.1); every matching passage read with its section heading. HOSTING §6.4–§6.5, §7, §8, §13 and UNRESOLVED; RS §4, §10 and UNRESOLVED; EXEC §5; ACT §10; LOOP §1, §4, §10; GUIDE §2.10, HC-10, §4.4; CA §2.5, §11 and UNRESOLVED; XT §6 were read as blocks. No Design file was read whole |
| `RELAY_ANSWERS_SWBPIPE.md`, `FACTS_SQ01_SQ32.md` | Not read for content. SWBPIPE facts below are quoted from the 17 Design files that carry them, as data about SWBPIPE's state |
| `loop/LOOP_INIT.md`, "Develop the detail appropriate to the phase" | Read whole |
| `APP-V4-FIRST-INCREMENT-20260928/OWNER_DECISIONS.md` (DECISION-1, D1…D4) | Read |
| `_ScopeChange/_LATEST.md`, both `Amendment_Actions.csv` | Read for which SoWs were revised; cross-checked against each SoW's own AX marker and `git log` |

Repository HEAD when read: `4698471d9e42f9be1f349b26e799a56dd8189ffb`. No file
was modified by this node other than this one.

## 1. The arc set

Computed from the two CSVs: **53 arcs** have exactly one end among the 14.

| | Admitted | Held | Total |
|---|---:|---:|---:|
| Consumer among the 14, supplier outside | 10 | 4 | 14 |
| Supplier among the 14, consumer outside | 33 | 6 | 39 |

The integrator's orientation is confirmed in every particular: the ten
admitted and four held inward arcs, the 17 admitted outside consumers and the
four held ones (DEL-01-04, 01-05, 02-02, 02-04).

Every one of the 53 representative rows is `ACTIVE`, `EXECUTION` class.
`RequiredMaturity` is `INITIALIZED` on 50 and `TBD` on three (DEP-06-01-013,
DEP-08-02-006, DEP-09-01-019). `SatisfactionStatus` is `TBD` on 46 and `PENDING` on 7: **no register records
any of these contributions as satisfied.** The live rows agree with the DAG-003
copies on both fields.

## 2. Consumer among the 14, supplier outside (14 arcs)

### 2.1 Summary

"Side" says which register carries the arc. "Now" answers the brief's
question: does the first-increment **design** need the supplier's definition
now? The reasoning for each is in §2.2.

| # | Arc | Layer | Representative row | Side | Contribution (from the row) | Now? |
|---|---|---|---|---|---|---|
| I-1 | DEL-04-03 → DEL-01-02 | Admitted | DEP-01-02-020 (DOWNSTREAM HANDOVER; TBD) | Supplier only | Compact observation evidence, actual observed events and explicit outcome gaps | No. Later (implementation and fixtures). One wording disagreement inside the 14 to fix now (§2.2) |
| I-2 | DEL-05-01 → DEL-01-05 | Admitted | DEP-01-05-014 (DOWNSTREAM HANDOVER; PENDING) | Supplier only | Applicable local-server capability requirements and qualification limits | No. Later (it is a qualification output) |
| I-3 | DEL-09-06 → DEL-02-02 | Admitted | DEP-09-06-026 (UPSTREAM INTERFACE; TBD) | Consumer only | Review and registration for the connected workflow round trip | Definition no; one joint ruling yes (registration as a recorded act) |
| I-4 | DEL-03-04 → DEL-02-04 | Admitted | DEP-03-04-010 (UPSTREAM INTERFACE; TBD) | Consumer only | Additive role guidance and supply receiving semantics, for the guide entry and completeness comparison | No. Later |
| I-5 | DEL-03-04 → DEL-07-01 | Admitted | DEP-03-04-016 | Consumer only | PEC first-consumer receiving and adoption-evidence expectations | No. Conditional by the accepted basis |
| I-6 | DEL-03-04 → DEL-07-02 | Admitted | DEP-03-04-017 | Consumer only | Connector limitation and source-file recovery responsibilities | No. Conditional |
| I-7 | DEL-03-04 → DEL-08-01 | Admitted | DEP-03-04-018 | Consumer only | Domains receiving, query, admission and freshness requirements | No. Later increment |
| I-8 | DEL-03-04 → DEL-08-02 | Admitted | DEP-03-04-019 | Consumer only | Later research-to-design receiving contribution | No. Later increment |
| I-9 | DEL-09-06 → DEL-09-01 | Admitted | DEP-09-01-024 (DOWNSTREAM HANDOVER; TBD) | Supplier only | Reusable examination support and evidence interfaces | No. Needed before candidate-bound results |
| I-10 | DEL-09-09 → DEL-09-01 | Admitted | DEP-09-09-012 (UPSTREAM PREREQUISITE; PENDING); mirror DEP-09-01-026 | Both | Examination infrastructure and the WebKit/Chromium and packaged-smoke evidence protocol | No. Same |
| I-11 | DEL-01-01 → DEL-01-05 | Held (SCC-001) | DEP-01-01-024 (UPSTREAM INTERFACE; TBD) | Consumer only | Native sign-in and server-substitution evidence, "when needed" for the local qualification witness | No. The owner decision OI-009 is the part that touches the design |
| I-12 | DEL-02-03 → DEL-01-04 (X-1) | Held (SCC-002) | DEP-02-03-027 (UPSTREAM INTERFACE; TBD) | Consumer only | App act control and person identity | Construction no; a decision yes. The most consequential of the 14 (§2.2, §5) |
| I-13 | DEL-02-03 → DEL-02-02 | Held (SCC-002) | DEP-02-03-010 (UPSTREAM INTERFACE; TBD) | Consumer only (the opposite arc is DEP-02-02-015) | Workflow-making, reviewed-registration and source-qualified selection contract | No. Later; one open choice (selection slot policy) |
| I-14 | DEL-04-03 → DEL-02-04 | Held (SCC-002) | DEP-02-04-012 (DOWNSTREAM HANDOVER; PENDING) | Supplier only | Role-specific source identity, actual supplied bytes and enforcement-limit evidence | No. Later |

**States (registers):** four of the fourteen arcs (I-1, I-2, I-9, I-14) exist
only as a DOWNSTREAM row in the outside supplier's register. The consumer's
register and SoW do not name the supplier: `grep` for the supplier ID in the
consumer's `ScopeOfWork.md`, `Dependencies.csv` and `_DEPENDENCIES.md` returns
nothing for I-1, I-2 and I-14. For I-9 the consumer's `_DEPENDENCIES.md` says
the mirror was "not extracted: no SoW ground; consumer row represents the arc".

### 2.2 Per arc

#### I-1 DEL-04-03 → DEL-01-02 (admitted)

- **States (supplier SoW, DEL-01-02).** Praxeology opening paragraph: the
  owner "provides state/request interfaces to App-v4 DEL-01-04 and compact
  observation evidence to App-v4 DEL-04-03". OUT-004: the evidence handoff
  "links actual observed events and gaps into the receiving record contract;
  it creates no competing authoritative transcript or new human-act schema".
  REQ-006: supply "observed events and explicitly unknown outcomes to the
  receiving UI and compact-evidence interface". VER-007 checks the handoff
  "within this slice's handoff, not the sibling record schema".
- **States (consumer SoW, DEL-04-03).** CLM-004, as revised by SCA-V4-001,
  lists what the record format receives. The list names DEL-04-01, 04-02,
  03-01, 03-02, 02-03, 03-03, 05-01, and "observed supplier facts (supplied
  guidance, model and destination, tool-permission settlements) from
  `DEL-01-01`". It does not name DEL-01-02. The live row for that input is
  DEP-04-03-027 (arc N-15, admitted).
- **What waits.** Inference from the two SoWs: the DEL-04-03 record entries
  that depend on durable custody — settlement and acknowledgment observation
  across window loss, reconnect and relaunch. The Design files name the
  waiting parts exactly (next bullet).
- **Shape already assumed by the 17 Design files.**
  - RS §4 R13 (tool-permission settlements): supplier "DEL-01-01 observed
    facts in this undertaking; DEL-01-02 later (D1)". RS UNRESOLVED U-20:
    "R13 feed beyond DEL-01-01 observed facts", owner DEL-01-02, point of need
    "DEL-01-02 definition", effect "R13 fed by DEL-01-01 only". RS §10 last
    row: DEL-01-02, 01-04, 02-02, 02-04 consume "R3/R4/R7/R13" and supply
    back "Observation evidence; role bytes; App capture control"; "Outside
    this undertaking (D1)".
  - HOSTING §6.4: "read settlement and acknowledgment observation", caller
    "DEL-01-02; DEL-04-03 via DEL-01-02". §6.5 "Split with DEL-01-02 (to
    reconcile when DEL-01-02 is defined)". §8 S-1 (what DEL-01-02 receives and
    what is "not supplied here": durable custody, reconnect/relaunch,
    persistence, recovery reads, settlement fixtures, descendant policy).
    §8 S-7: evidence goes to "DEL-04-03 (through DEL-01-02)". §8.2: supplied
    guidance records "reach DEL-04-03 through DEL-01-02 (S-7)". Findings F-01
    and F-15; UNRESOLVED U-09 (acknowledgment observation mechanism), U-10
    (stop-time handling), U-14 (unknown-request split), U-16 (descendants).
  - ADAPTER §5.6 and §10.2 XF-41: in-flight custody across an App restart is
    "AWAITING INPUT (DEL-01-02, later undertaking, D1)". XT §3.2 XC-06 carries
    the same limit.
- **Disagreement between files (states).** HOSTING routes the evidence to
  DEL-04-03 *through DEL-01-02* (§6.4, §8 S-7, §8.2). The DEL-04-03 SoW
  CLM-004 (revised), register row DEP-04-03-027 and RS R3/R5/R13 take the same
  facts *from DEL-01-01 directly* in this undertaking. The graph admits both
  arcs (N-15 and this one).
- **Design need now.** Inference: no. RS defines the elements semantically and
  allows *unknown*; nothing in RS selects a writer placement (RS U-05, U-16).
  What waits is implementation and the settlement fixtures. The route wording
  above can be reconciled inside the 14 (HOSTING S-7, §6.4, §8.2 against
  DEL-04-03 CLM-004) without any DEL-01-02 design.
- **Smallest supplier-side definition, if wanted.** A short DEL-01-02 note
  that (a) accepts or amends HOSTING §6.5's split; (b) states the three
  behaviours HOSTING leaves to it — acknowledgment observation (U-09),
  stop-time handling of outstanding entries (U-10), descendant handling
  (U-16) — as states and failure behaviour; (c) names which RS elements it
  feeds (R4, R7, R11 "lost acknowledgement", R13) and by which route.

#### I-2 DEL-05-01 → DEL-01-05 (admitted)

- **States (supplier SoW, DEL-01-05).** CLM-004: "DEL-01-05 supplies
  applicable local-server capability requirements to that receiving
  contribution". REQ-008: requirements and qualification limits go to the
  PKG-05 receiving contribution, "distinguishing the App's Codex-provider
  interface from the host's model/loop interface". AC-009 adds "without
  claiming host conformance from App qualification alone". The content comes
  from OUT-004, candidate-bound qualification evidence.
- **States (consumer SoW, DEL-05-01).** No mention of DEL-01-05 or of an input
  from the App account/provider owner. REQ-002 requires the host model
  contract to stay "distinct from the standalone App's Codex App
  Server/provider interface". The model-interface input is DEP-05-01-024,
  supplier UNKNOWN.
- **Shape assumed by the Design files.** LOOP does not name DEL-01-05 (zero
  occurrences). LOOP §1 keeps the two model interfaces apart ("A local server
  that serves both interfaces does not join them"). LOOP §4 states the minimal
  Chat Completions capability from V4-ARC-10 itself. LOOP §10.3 lists "Model
  interface | UNKNOWN (DEP-05-01-024) | Not supplied". HOSTING §8.1 L-6 says
  the two interfaces are qualified separately.
- **What waits.** Nothing in DEL-05-01 is stated to wait for it. Inference:
  the handoff would inform LOOP §4 and the OUT-002 model-interface fixtures
  once DEL-01-05 has qualified a local server on a candidate.
- **Design need now.** No. The contribution is a qualification output; it
  needs a candidate, a configured server and the selected pin (DEL-01-05
  TBD-003).
- **Observation (states, then inference).** DEL-01-05's SoW was not revised by
  either amendment and speaks of local servers only. DEL-05-01's SoW, revised
  by SCA-V4-001, now covers a cloud model reached by OAuth sign-in or an API
  key, with no default. Neither SoW says whether the handoff covers anything
  for a host's cloud model. Inference: it does not; host credentials and
  endpoints belong to the host native layer (DEL-01-05 CLM-004).

#### I-3 DEL-09-06 → DEL-02-02 (admitted)

- **States (consumer SoW, DEL-09-06).** CLM-003 (revised by SCA-V4-001):
  "App DEL-02-02 (later undertaking) review and registration". REQ-008 lists
  DEL-02-02 among the feature owners whose construction is excluded.
- **States (supplier SoW, DEL-02-02).** REQ-002 (draft until reviewed and
  explicitly registered), REQ-003 (no silent overwrite; visible collision
  disposition), REQ-004 (source-qualified identity across project, user,
  bundled and host-supplied origins; no silent rebind), REQ-006 and AC-006
  (an actual review/registration "is faithfully recorded and presented with
  the human actor distinct from any recorder and bound to its content, scope
  and purpose"). The SoW does not name DEL-09-06.
- **What waits (states, CA).** CA §8.2 W14-01 (transfer App → host) and W14-09
  (host → App refinement registered in the App): "AWAITING INPUT (DEL-02-02)".
  CA §6 ST-5. CA §12.1 F-1: "OUT-003 cannot complete in this undertaking
  (DEL-02-02 registration outside D1)". CA UNRESOLVED: the reusable workflow
  itself (the OUT-002 artifact) is authored "with DEL-02-02 (later) under
  `create-workflow`".
- **Shape assumed by the Design files.** A specific one:
  - CA §4 round-trip table: App library LIB-A1 holds registered workflows;
    the relayed host copy is held in LIB-A2; "draft base ⟨rev-3⟩ → registered
    with derived-from".
  - EXEC §6.1 (listed, selected, opened/drafted/registered links), §6.3 TR-1
    ("Drafts are not carried: a draft has no workflow identity"), §6.5
    HR-1…HR-7, §7.3 RT-6 and RT-7.
  - WD §6.3 (collision and rebinding), §6.4, §8 (DEL-02-02 receives §3, §6,
    §4.6, §5; "Not exercised in this undertaking").
  - PANEL §6 names DEL-02-02 as a possible second consumer of workflow
    identity and holding-library presentation.
- **Open choices that sit on this join (states).** ACT §2.1 lists workflow
  registration among the human acts that "keep the attribution invariants
  but have no canonical name here"; ACT UNRESOLVED U-08 and §12 item 6. RS U-08: "Workflow
  review/registration as act kind … Not recorded here". WD U-10 and EXEC
  U-E19: selection slot policy, host origin in unqualified precedence, and
  whether a selection follows new revisions.
- **Design need now.** Inference: the supplier's full definition is not
  needed; the assumed shape agrees with DEL-02-02's REQ-002…REQ-004. One item
  is structural for the 14: whether review/registration is a recorded act
  kind. DEL-02-02 AC-006 requires that record; ACT and RS do not yet offer it.
  A later "yes" adds an act kind to ACT §2.1's closed table and a record kind
  to RS §6. That ruling belongs to DEL-04-01 with the owner and can be made
  without a DEL-02-02 Design file.
- **Smallest supplier-side definition, if wanted.** A DEL-02-02 note stating
  the library interface the 14 already assume: list, select, open read-only,
  draft, review, register; the collision disposition; the slot policy (WD
  U-10); and how a registration is evidenced.

#### I-4 DEL-03-04 → DEL-02-04 (admitted)

- **States.** DEL-03-04 SoW receiving-map row "Host methods and roles" names
  "App DEL-02-01/DEL-02-03/DEL-02-04 receiving"; CLM-003; REQ-005; VER-004.
  DEL-02-04's SoW does not name DEL-03-04.
- **What waits.** GUIDE §2.8 M8.6 (four roles behind one host seat; additive
  role guidance with per-thread/turn supplied-guidance evidence) and §2.12
  X-06. GUIDE §4.4 G-1: DEL-02-04 "has no Design file; M8.6 … rest[s] on SoW
  meaning plus HOSTING S-6".
- **Shape assumed.** HOSTING §8 S-6 (carriage through the supplier's supported
  inputs; at 0.158.0 `baseInstructions` and `developerInstructions` on thread
  start and resume) and §8.2 ("the source identity supplied by the composing
  owner (DEL-02-04 …)"). WD §5.1–§5.2 and §6.2 ("supplied … App: DEL-02-04 /
  DEL-01-01"). EXEC §6.1 supplied link. RS R3 and R5a. PIN_SPIKE §6 P-15:
  whether resume overrides apply to an already-loaded thread is not observed,
  "open for DEL-02-04".
- **Design need now.** No. The guide row is written against the consumer-side
  seam and is marked outside the undertaking. The role-file structure and
  distribution are left to DEL-02-04 and OI-018 (WD §7; WD U-14).
- **Smallest supplier-side definition, if wanted.** What a role-guidance
  *source identity* is; which supplier input carries role guidance and which
  carries workflow guidance; the order of composition; and the
  enforcement-limit statement per role (DEL-02-04 REQ-003, REQ-004).

#### I-5 … I-8 DEL-03-04 → DEL-07-01, 07-02, 08-01, 08-02 (admitted)

- **States (DEL-03-04 SoW).** Receiving-map row "Selected connectors";
  CLM-005; REQ-006 ("First connected work may proceed without either
  connector"); VER-005; TBD-007 (OI-022, "Before operational consumer
  reliance"), TBD-008 (OI-023, "Before later Domains-enabled design
  increment"), TBD-009 (OI-026). All four register rows carry the note
  "Conditional connector coverage in guide, not a connector availability
  prerequisite".
- **States (supplier SoWs).** None of the four names DEL-03-04. DEL-08-01's
  `_DEPENDENCIES.md`: "The SoW does not name DEL-03-04, so no supplier-side
  mirror … is extracted."
- **What waits.** GUIDE §2.10 rows M10.1 and M10.2; HC-10.2 and HC-10.3; §2.12
  X-12 and X-13. GUIDE titles §2.10 "conditional, not designed here". §4.4
  G-2: "PEC and Domains receiving not started … By design (conditional)".
- **Design need now.** No. The accepted basis stages the first connected work
  without PEC or Domains (CA §6 ST-0…ST-5; GUIDE M10.3), and the owning
  decisions are open at later points of need.
- **Inference, for S1-E to confirm.** DEL-08-01 CLM-003 was revised by
  SCA-V4-001 to the host-agent destination constraint. GUIDE M10.2 and HC-10.3
  cite DEL-08-01 "accepted SoW meaning" and do not repeat that constraint; row
  7 carries V4-HOST-02 separately. A one-line cross-reference would align
  them. This is a re-pin matter inside the 14, not outside design.

#### I-9, I-10 DEL-09-06 → DEL-09-01 and DEL-09-09 → DEL-09-01 (admitted)

- **States (supplier SoW, DEL-09-01).** REQ-008: the harness "supplies
  reusable support and evidence interfaces to those owners" (DEL-09-06 and
  DEL-09-09 are named in CLM-005). REQ-002: every result names candidate,
  date, harness and model versions and server configuration, and keeps
  passed, failed, blocked, not-run or inconclusive. REQ-007: WebKit and
  Chromium, and native packaged smoke checks. OUT-001…OUT-004 are fixture
  support, capture scripts, the protocol and the execution harness.
- **States (consumers).** DEL-09-09 REQ-008 and CLM-002 name DEL-09-01.
  DEL-09-06's SoW does not; its REQ-007 and AC-007 take the same outcome set
  and attribution from EXAMINATION §§1–2 directly.
- **What waits (states).** XT §2 IN-03: "Not defined in this undertaking". XT
  §6: "until it exists, interface observations carry the limit 'protocol not
  yet defined'". CA §6 ST-1 (App-local executable fixtures need the "DEL-09-01
  protocol"); CA UNRESOLVED: "DEL-09-01 evidence protocol … Before
  candidate-bound results … Labels per C mapping only".
- **Shape assumed.** Evidence labels from the C mapping (*illustrative*,
  *test-double*, *actual host*, AWAITING INPUT / HELD / NOT-OBSERVED, LIMITED)
  in CA §7.1 and XT §6, used beside the five EXAMINATION outcome states.
- **Design need now.** No. Every verification case in the 17 files is
  "designed, not run"; host joins are deferred (DECISION-3), so no
  candidate-bound result is due in this pass. The basis document supplies the
  outcome states and attribution rules the two consumers cite.
- **Smallest supplier-side definition, if wanted.** One page: the elements of
  an examination result record; how the C-mapping labels relate to the five
  outcome states; how replay, browser and native evidence are marked.

#### I-11 DEL-01-01 → DEL-01-05 (held, SCC-001)

- **States.** DEL-01-01 VER-005: "native sign-in and server-substitution
  evidence is received from its own owner when needed". Row note: "the source
  does not impose an unconditional prerequisite". SCC-CASE-001 datasheet: the
  return is "neither unconditional nor a prerequisite to all supplier
  definition/production".
- **What waits.** Only the portions of DEL-01-01's qualification witness
  (OUT-004, AC-005) that invoke native sign-in or server substitution.
- **Shape assumed.** HOSTING §8 S-4; §8.1 L-1…L-6 (the requirement account
  handed to DEL-01-05; L-2 and L-3 "not-observed"); §11 owner row; UNRESOLVED
  U-03 (OI-009 account home, "Configuration-identity element open"), U-18
  (supplier network fetch at start), U-19 (live behaviours need a credential
  or local provider), U-20 (partition of server-request kinds, with
  DEL-01-04/01-05), U-22.
- **Design need now.** No supplier definition. Inference: the item on this
  join that can change HOSTING's structure is **OI-009** — the account home
  affects the start sequence (§4.2), the version probe's home (§7.2) and the
  fresh-home fetch (F-14). It is an owner decision "with App implementation
  owner" (DEL-01-05 REQ-005, TBD-001), not a DEL-01-05 design task.

#### I-12 DEL-02-03 → DEL-01-04 (held, SCC-002; arc X-1)

- **States (consumer SoW, DEL-02-03).** CLM-002 (revised by SCA-V4-002):
  "`DEL-01-04` (later undertaking) constructs the App act control"; the slice
  consumes "`DEL-01-04`'s App act control and person identity, for the
  App-side positive capture fixtures (OUT-003, VER-003), which await that
  later undertaking". REQ-006 lists "App act control construction to
  `DEL-01-04`". HANDOFF: X-1 is narrow — only those fixtures wait.
- **States (supplier SoW, DEL-01-04).** The words "act control", "person
  identity" and "capture" do not occur (`grep -c -i` returns 0 for each). The
  outputs are approval/question cards (OUT-001), turn/outcome and attachment
  presentation (OUT-002), fixtures (OUT-003) and the workflow-draft receiving
  contract (OUT-004). The nearest text is REQ-005 ("An actually performed
  human act may be faithfully displayed or recorded through the designated
  recording interface with decision actor distinct from recorder") and VER-005
  ("the person actually performs the act on identified content and a separate
  recorder preserves it"). SCA-V4-002 revised CLM-005, VER-005, TBD-001,
  TBD-002 and TBD-004 only (AX-004). DEL-01-04's `_DEPENDENCIES.md`: "no
  source sentence here names DEL-02-03, so no row was added."
- **Shape assumed by the Design files.** The consumer side has written the
  supplier's requirements:
  - EXEC §5 CAP-1…CAP-9: scope (App content; no proxy control for host
    content); a dedicated control for one act kind at a time that also offers
    the decline; the direct-capture record and its capture-evidence reference;
    "Not operable by automation" (CAP-4); tool-permission, user-input and
    conversation are never capture evidence; person identity `UNRESOLVED`
    (CAP-8, U-E8). "Construction of the control is DEL-01-04's".
  - ACT §2.6; RS §6 and U-28; WD U-25; EXAMPLES U-25; GUIDE §2.5 M5.3 and
    §4.4 G-1; CA §5 and §8.2 W14-05 (AF-1 variant); EXEC §7.2 CH-23 (ii)
    "AWAITING INPUT (DEL-01-04 control; U-E8)".
- **What waits.** States: DEL-02-03 OUT-003 and VER-003 App-side positive
  capture fixtures. Inference: also the AF-1 variant of CA W14-05 and any
  App-content *performed* disposition in RS §12 examples.
- **Design need now.** Construction: no. But two things are open that a later
  answer could push back into the 14:
  1. **Inference.** Nothing in DEL-01-04's SoW obliges it to build the control
     that seven Design files assign to it (ACT, EXEC, RS, WD, EXAMPLES, GUIDE
     and CA, as cited above). The ask exists only on the consumer
     side. Closing that needs a SoW revision (a scope-change matter, not
     writable in this run).
  2. **States.** The App person identity scheme is unresolved in EXEC (U-E8),
     RS (U-28) and WD (U-25). Inference: it sets the *decision actor* element
     of every App-captured human-act record (RS §6.1) and the evidence limit
     RS attaches to App-captured acts, so it is a data-definition choice
     inside the 14, and an owner choice.
  Further inference: with SWBPIPE supplying no capture-evidence reference
  (SQ-01 as carried in RS U-11 and GUIDE M5.3) and host joins deferred, the
  App act control is the only route by which any act can reach *performed* in
  Phase 1. Without it the first increment's positive human-act case has no
  executable route on either side.
- **Smallest supplier-side definition, if wanted.** A DEL-01-04 interface note
  limited to the act control: acceptance or amendment of CAP-1…CAP-9; the
  person identity scheme chosen by the owner; what the control takes in (act
  kind, subject and content identity, scope, purpose, actor requirement,
  arrival) and puts out (direct-capture record, act-declined event); and the
  process placement that makes CAP-4 true. The last depends on OI-008 (HOSTING
  §12 is a proposal only).

#### I-13 DEL-02-03 → DEL-02-02 (held, SCC-002)

- **States.** DEL-02-03 CLM-001 ("This slice receives those contracts"),
  REQ-005 ("routing changed drafts through the existing reviewed-registration
  contract"), VER-005 ("registration remains with DEL-02-02").
- **What waits.** EXEC §6.5 HR-1…HR-7 and §7.3 RT-6/RT-7, whose "registration
  side [is] not exercised" (U-E19); §11.1 F-12, "Changed-draft return
  uncompared".
- **Design need now.** No; same shape and same open choices as I-3.

#### I-14 DEL-04-03 → DEL-02-04 (held, SCC-002)

- **States (supplier SoW, DEL-02-04).** REQ-004: "Provide the role-specific
  identity and limit evidence to the existing record/adoption interfaces in
  CLM-002"; OUT-002; AC-005 ("usable by the existing PKG-04 and PKG-11
  interfaces without defining their schema"). DEL-04-03's SoW does not name
  DEL-02-04; its CLM-004 takes "supplied guidance" from DEL-01-01.
- **What waits.** Inference: the role-specific source identity inside RS R3.
  RS R3 names "DEL-01-01 (App); host loop (relay)" as suppliers and allows
  *unknown*.
- **Design need now.** No. R3 is generic over guidance inputs.

### 2.3 What the first-increment design needs now, and what it needs later

**Needs later (implementation, fixtures or qualification; no supplier
definition needed to write the 14 to design depth):** I-1, I-2, I-4…I-10,
I-13, I-14, and the construction part of I-12. For each, the consumer's Design
file already states the receiving side and marks the dependent case AWAITING
INPUT or outside the undertaking.

**Needs now — decisions that sit on an outside join but can be taken without
an outside Design file (inference):**

| # | Decision | Where it is open today | Who decides | Why now |
|---|---|---|---|---|
| N-1 | App person identity scheme | EXEC U-E8; RS U-28; WD U-25 | Owner (the files name DEL-01-04 with DEL-04-03) | Sets the actor element of App-captured act records |
| N-2 | Whether DEL-01-04's contract carries the App act control | DEL-02-03 CLM-002 says yes; DEL-01-04's SoW does not say it | Owner, through scope change | The consumer-side requirement has no supplier-side obligation |
| N-3 | Workflow review/registration as a recorded act kind | ACT U-08; RS U-08 | DEL-04-01 with the owner | DEL-02-02 AC-006 requires the record; a later "yes" changes ACT §2.1 and RS §6 |
| N-4 | Evidence route from DEL-01-01 to DEL-04-03: direct, or through DEL-01-02 | HOSTING §6.4, S-7, §8.2 against DEL-04-03 CLM-004 and RS R13 | Integrator, inside the 14 | Two first-increment files disagree |
| N-5 | OI-009 account home | HOSTING U-03; DEL-01-05 TBD-001 | Owner with App implementation owner | Changes HOSTING §4.2 and §7.2 |

## 3. Supplier among the 14, consumer outside (39 arcs)

"Offered" compares the supplier's Design file with what the consumer's
register row and its cited SoW items ask for. Every Design file is a DRAFT
DEFINITION ("proposed, unsupplied, not implemented, not accepted", in each
header), so "offered" never means supplied or qualified. "Named" says whether
the Design file names the consumer at all.

### 3.1 Supplier DEL-01-01 (HOSTING-BOUNDARY-v0.6; PIN-SPIKE-v0.1)

| Arc | Layer | Row (mirror) | Consumer asks for | Offered in the Design file | Named |
|---|---|---|---|---|---|
| DEL-01-02 → | Admitted | DEP-01-02-018 (DEP-01-01-019) | Process/protocol boundary and selected-version types (CLM-001; Praxeology) | §4 lifecycle, §5, §6 register and §6.4 operations; seam S-1; JSON Schema bundles committed under `Design/generated/0.158.0/` (TS not committed, §7.3). Definition only: pin 0.158.0 is "definition/generation; not qualification" (U-01). The split with DEL-01-02 is unreconciled (§6.5, F-01, U-14) | Yes |
| DEL-01-03 → | Admitted | DEP-01-03-011 (DEP-01-01-020) | Generated native types, selected supplier identity and its qualification evidence (CLM-002; REQ-004) | S-2; §7.1 version identity record. States that at 0.158.0 a plan update carries the whole plan with no revision identity. Qualification evidence: none | Yes |
| DEL-01-04 → | Admitted | DEP-01-04-007 (DEP-01-01-021) | Hosting boundary, supplier identity, generated types, protocol qualification (CLM-002) | S-3 (register operations, refusal reasons incl. `origin-not-permitted`, settlement). Request-kind partition is a proposal (U-20). Qualification: none | Yes |
| DEL-01-05 → | Held (SCC-001) | DEP-01-05-012, with DEP-01-05-013 (DEP-01-01-022) | Selected protocol/pin; embedding-qualification input (CLM-003; REQ-007) | S-4; §8.1 L-1…L-6 requirement account, with L-2 and L-3 "not-observed". Embedding qualification: none | Yes |
| DEL-01-06 → | Admitted | DEP-01-06-006 (DEP-01-01-023) | Identified stock Codex binary and App hosting basis (CLM-001) | S-5; §7.1 distribution content identity (spike-observed hashes; "expected" identity "Not yet recorded"); composition open (U-17) | Yes |
| DEL-02-04 → | Admitted | DEP-02-04-010 (no mirror; HOSTING F-16 records the missing row) | Identified supported supplier receiving contract for additive role supply (VER-002) | S-6; §8.2. P-15: adoption on resume not observed | Yes |
| DEL-06-01 → | Admitted | DEP-06-01-013 (maturity TBD) | The actual selected pin "before protocol generation and native-association qualification" | The pin for definition and generation only; PIN_SPIKE §6 P-13 observes subagent items in generated types. The qualification pin is open (U-01) | No |
| DEL-09-01 → | Admitted | DEP-09-01-019 (maturity TBD; CONSTRAINT) | Selected pin for replay and qualification | Same; §9 recorded-exchange fixture method bears on DEL-09-01 OUT-001 | No |
| DEL-09-02 → | Admitted | DEP-09-02-009 | Hosting/protocol contribution and scoped feature checks before the joined witness | Designed verification cases only; no candidate | No |

### 3.2 Supplier DEL-04-01 (ACT-POLICY-v0.6)

All eight consumers ask for the "applicable adopted operation policy". ACT §8
gives the policy representation (class records; DECISION-1 record §8.2), §9
the label rules, §10.1 the value-to-consumer map. §10.3 lists "Other declared
consumers (not mapped in detail)": DEL-01-02, 02-02, 03-04, 06-02, 09-02,
09-05, 09-12 and 10-03, each with its row ID.

| Arc | Layer | Row | Offered | Named |
|---|---|---|---|---|
| DEL-01-02 → | Admitted | DEP-01-02-021 | §10.1 V-21 (P-04 routine tool permission; D3) names it. The consumer's TBD-003 still reads OI-001/OI-002 as open (unrevised SoW) | Yes |
| DEL-01-04 → | Admitted | DEP-01-04-011 | V-01, V-05, V-07 (label rules §9, which is what its VER-005 compares against), V-08, V-21; header Receivers | Yes, mapped |
| DEL-02-02 → | Admitted | DEP-02-02-016 | §10.3 only. Registration has no canonical act name (§2.1; U-08) | Listed |
| DEL-06-02 → | Admitted | DEP-06-02-009 | §10.3 only. "reserved coordination decisions (V4-PM-04)" have no canonical name (§2.1) | Listed |
| DEL-09-02 → | Admitted | DEP-09-02-018 | §10.3 only | Listed |
| DEL-09-05 → | Admitted | DEP-09-05-009 | §10.3 only | Listed |
| DEL-09-12 → | Admitted | DEP-09-12-011 | §10.3 only | Listed |
| DEL-10-03 → | Admitted | DEP-10-03-013 | §10.3; §11 boundary accounting | Listed |

### 3.3 Supplier DEL-04-03 (RS-v0.6)

RS names semantic elements only: "No serialization, field spelling, type, file
path, persistence …" (§0; U-04, U-05, U-16). Its header says "no writer,
reader or fixture exists". A consumer asking for a *format* or a
*reader/writer interface* is offered the meaning, not the format.

| Arc | Layer | Row (mirror) | Consumer asks for | Offered | Named |
|---|---|---|---|---|---|
| DEL-01-04 → | Held | DEP-01-04-012 | Act/run-record and recording interface; actor/subject evidence; supplied lapse standing (REQ-005) | §6, §7; §10 last row "Outside this undertaking (D1)"; U-28 | Yes |
| DEL-02-02 → | Held | DEP-02-02-017 | Record behaviour for truthful review/registration presentation (REQ-005, REQ-006) | **Not offered for registration**: U-08 "Not recorded here" | Yes |
| DEL-06-01 → | Admitted | DEP-06-01-008 | Evidence/act record interface and identified source records (REQ-004) | §10 row "PKG-06 (DEL-06-01/06-02)": act records, actor ≠ recorder, lapse; "Decision records as act subjects" | Yes |
| DEL-06-02 → | Admitted | DEP-06-02-010 | Record format and owning reader/writer interface (REQ-004) | Same row; meaning only | Yes, as "PKG-06 (DEL-06-01/06-02)" |
| DEL-09-02 → | Admitted | DEP-09-02-019 | Act/run record contribution and scoped feature evidence | §6, §12 examples (invented), designed cases; no evidence | No |
| DEL-09-05 → | Admitted | DEP-09-05-010 | Decision/run formats and App recording | Same | No |
| DEL-09-11 → | Admitted | DEP-09-11-005 (DEP-04-03-015) | Identified compact records and reference/lapse fixtures | §10 row DEL-09-11 ("Complete records for the week-later reconstruction"); EXEC §4.12 RP-6 inspection replay. No record or fixture exists | Yes |
| DEL-10-03 → | Admitted | DEP-10-03-014 | Record format and writer/reader obligations, for the responsibility trace | §10 consumer table; §11 excluded acts | No |

### 3.4 Suppliers DEL-02-01 (WD-v0.6, WD-EX-v0.6) and DEL-02-03 (EXEC-v0.4)

| Arc | Layer | Row | Consumer asks for | Offered | Named |
|---|---|---|---|---|---|
| DEL-02-02 → DEL-02-01 | Held | DEP-02-02-014 | Portable declaration and shared-allocation contract | WD §8: DEL-02-02 receives §3, §6, §4.6, §5; "Not exercised in this undertaking". WD U-10 open | Yes |
| DEL-02-04 → DEL-02-01 | Held | DEP-02-04-011 | Portable four-role receiving contract and applicable shared allocation | WD §5; §9 row A-6 (`UNRESOLVED{OI-014}`); U-09 seat mapping; §7 leaves role files to DEL-02-04 / OI-018 | Yes |
| DEL-08-02 → DEL-02-01 | Admitted | DEP-08-02-006 (maturity TBD) | Portable method meanings and evidence | WD §3–§6 generically | No |
| DEL-09-02 → DEL-02-01 | Admitted | DEP-09-02-015 | Workflow declarations and scoped feature evidence for V4-EXM-10 | WD and EXAMPLES; no evidence | No |
| DEL-10-03 → DEL-02-01 | Admitted | DEP-10-03-008 | Portable semantics and justified shared allocation | WD §9 responsibility map (OUT-003), which is the matching content; every row is unagreed (U-17) | No |
| DEL-02-02 → DEL-02-03 | Held | DEP-02-02-015 | Capability/checkpoint execution and round-trip support; missing capability, required checkpoint and unknown outcome preserved | EXEC §3, §4, §6.5; §9.1 and §10 name DEL-02-02; F-12 changed-draft return uncompared | Yes |
| DEL-09-02 → DEL-02-03 | Admitted | DEP-09-02-017 | Capability/checkpoint execution contribution and feature evidence | Designed cases only | No |
| DEL-10-03 → DEL-02-03 | Admitted | DEP-10-03-009 | Compatibility and checkpoint receiving obligations | EXEC §2 parties table; §10 excluded acts | No |

### 3.5 Suppliers DEL-03-01, 03-02, 05-01, 05-02, 09-06

| Arc | Layer | Row | Consumer asks for | Offered | Named |
|---|---|---|---|---|---|
| DEL-10-03 → DEL-03-01 | Admitted | DEP-10-03-011 | Catalog/read-basis obligations | C §8 three-surface responsibility map; two rows name DEL-10-03 | Yes |
| DEL-10-03 → DEL-03-02 | Admitted | DEP-10-03-012 | Proposal/validation/outcome obligations | P §13 interfaces; §1 authority map | No |
| DEL-10-03 → DEL-05-01 | Admitted | DEP-10-03-015 | Host-loop and native-network receiving obligations | LOOP §10.1 responsibility map; §10.2 | No |
| DEL-10-03 → DEL-05-02 | Admitted | DEP-10-03-016 | Host-panel receiving obligations | PANEL §6 reusable-component allocation account | No |
| DEL-08-01 → DEL-05-01 | Admitted | DEP-08-01-008 | Embedded-integration receiving requirements, to show query/tool compatibility with the host-agent destination constraint (CLM-003, revised by SCA-V4-001; REQ-006) | LOOP §5.1.1 NW-8…NW-16 and §5.2 cases. `UNRESOLVED{N-OPEN-3}`: "tool-caused traffic (e.g. a later Domains query) … which traffic of a host operation counts as the agent's stays open" | No |
| DEL-09-07 → DEL-09-06 | Admitted | DEP-09-07-011 | "The actual agreed activity and App/host workflow round-trip agreement", incl. the selected operation, permitted autonomy and exact candidate environment (CLM-003; Praxeology) | CA §11.2: step map §2.3 for CA/E, staging §6, evidence ladder §7. **The agreement is not offered**: operation, autonomy and environment are `UNRESOLVED{OI-021}` (CA §2.5 DI-1…DI-3) and host joins are deferred | Yes |

### 3.6 Reading of §3

**States.** Fifteen of the 39 outside consumers are not named by the
supplier's Design file (the "No" rows above; checked by counting the
consumer's ID in the supplier's Design files). ACT lists eight consumers as
"not mapped in detail", seven of them outside the 14.

**Inference.**

- The ten consumers that ask for *definition content* a first-increment file
  already holds (the DEL-10-03 arcs, DEL-08-02, DEL-08-01) are served at draft
  level; adding them to the suppliers' receiver tables is a bounded edit.
- The consumers that ask for *evidence on a candidate* (DEL-09-02, 09-05,
  09-11, 09-07, 06-01's native-association qualification, 09-01's replay pin)
  cannot be served by any design pass; they wait for implementation.
- Two asks are not offered even as definition: DEL-02-02's review/registration
  record (RS U-08; ACT U-08) and DEL-09-07's actual agreement (OI-021).
- One supplier statement could be sharpened now at no cost: LOOP N-OPEN-3,
  which DEL-08-01's revised CLM-003 leans on.

## 4. The six named outside deliverables

### 4.1 Occurrences in the 17 Design files

Counts of each outside ID per file (`grep -c`, lines). All other outside IDs
with an arc return zero except: DEL-01-03 in HOSTING (6) and PIN_SPIKE (4);
DEL-01-06 in HOSTING (8) and PIN_SPIKE (2); DEL-09-11 in EXEC (2) and RS (4);
DEL-09-07 in CA (17), GUIDE (2), RELAY_QUESTIONS (1) and XT (1); DEL-10-03 in
C (2) and ACT (1); DEL-09-02 in ACT (2) and CA (3); DEL-09-05 in ACT (1) and
CA (2); DEL-09-12 and DEL-06-02 in ACT (1 each); DEL-06-01 in RS (1);
DEL-07-01 and DEL-08-01 in GUIDE (4 each); DEL-07-02 and DEL-08-02 in GUIDE
(2 each).

| Design file | 01-02 | 01-04 | 01-05 | 02-02 | 02-04 | 09-01 |
|---|---:|---:|---:|---:|---:|---:|
| HOSTING_BOUNDARY | 31 | 15 | 23 | 1 | 9 | 0 |
| PIN_SPIKE_0.158.0 | 3 | 1 | 5 | 0 | 2 | 0 |
| WORKFLOW_DECLARATION | 0 | 1 | 0 | 15 | 12 | 0 |
| EXAMPLES | 0 | 1 | 0 | 5 | 2 | 0 |
| EXECUTION_COMPATIBILITY | 0 | 9 | 0 | 20 | 2 | 0 |
| CATALOG_AND_READ_BASIS | 0 | 0 | 0 | 0 | 0 | 0 |
| PROPOSAL_LIFECYCLE_AND_OUTCOMES | 0 | 0 | 0 | 0 | 0 | 0 |
| ADAPTER_ENABLEMENT_AND_RECEIVING | 4 | 1 | 1 | 0 | 0 | 0 |
| HOST_INTEGRATION_GUIDE | 0 | 3 | 0 | 6 | 5 | 0 |
| ACT_AND_POLICY_CONTRACT | 3 | 7 | 0 | 4 | 0 | 0 |
| AUTONOMY_AND_STANDING_EXCHANGE | 0 | 0 | 0 | 0 | 0 | 0 |
| RECORD_SEMANTICS | 3 | 3 | 0 | 3 | 1 | 0 |
| LOOP_RECEIVING_CONTRACT | 0 | 0 | 0 | 0 | 1 | 0 |
| PANEL_RECEIVING_CONTRACT | 0 | 0 | 0 | 1 | 0 | 0 |
| CONNECTED_ACTIVITY_CONTRACT | 0 | 3 | 0 | 15 | 0 | 5 |
| RELAY_QUESTIONS_SWBPIPE | 0 | 0 | 0 | 3 | 0 | 0 |
| EXTERNAL_TRACE_CASES | 1 | 0 | 0 | 0 | 0 | 7 |

Every one of these passages refers to the outside deliverable "by accepted SoW
meaning only" and marks it a later undertaking under D1 (for example HOSTING
header and F-15; EXEC header; GUIDE header; CA header; XT header).

### 4.2 Folder contents and SoW revision

None of the six has a `Design/` folder or any design, code, test or fixture
file. `_SEMANTIC.md` is a 174-byte placeholder in each ("No semantic-lensing
pipeline selected"). `_STATUS.md` reads `INITIALIZED`, last updated
2026-09-27, in each.

| Deliverable | Beyond ScopeOfWork.md, Dependencies.csv and _DEPENDENCIES.md | Register rows (ACTIVE / all) | SoW sha256 (first 16) | Revised by SCA-V4-001 | Revised by SCA-V4-002 |
|---|---|---|---|---|---|
| DEL-01-02 | `_CONTEXT.md`, `_REFERENCES.md`, `_SEMANTIC.md`, `_STATUS.md`, `_run_records/dependency-extract-20260927.md` | 21 / 21 | `057ae2fdf4c3e98c` | No | No |
| DEL-01-04 | The same four control files; `MEMORY.md` (two run entries); three run records (20260927, 20260929, 20260929-sca002) | 18 / 19 (DEP-01-04-014 retired) | `0cdb44e297010b70` | No | **Yes**: CLM-005, VER-005, TBD-001, TBD-002, TBD-004 revised; AX-004 added |
| DEL-01-05 | The same four control files; one run record | 16 / 16 | `baf68c79b5b8fdf0` | No | No |
| DEL-02-02 | The same four control files; `MEMORY.md` (two run entries); three run records | 18 / 19 | `5814116909db8120` | No | **Yes**: TBD-001, TBD-002 revised; AX-004 added |
| DEL-02-04 | The same four control files; one run record | 16 / 16 | `3acfaa62a3bbf003` | No | No |
| DEL-09-01 | The same four control files; two run records (`dependency-extract-20260927.md`, `dependency-target-resolution-20260928.md`) | 30 / 30 | `8e53669468bd5885` | No | No |

How checked: each SoW's own AX marker ("Revised under scope-change amendment
…"); `git log` on each `ScopeOfWork.md` (the four unrevised ones have one
commit, `ddd721a90a`, 2026-09-27; the two revised ones add `1efd4bcdad`,
2026-09-29); and the deliverable IDs named in the two `Amendment_Actions.csv`
files.

**States.** The four unrevised SoWs do not contain "DECISION-1" or "0.158.0".
They still describe OI-001, OI-002 and OI-012 as open: DEL-01-02 TBD-001 and
TBD-003; DEL-01-05 TBD-003 ("the unidentified supplier pin"); DEL-02-04's
open-matter table; DEL-09-01 TBD-001's table. `_ScopeChange/_LATEST.md` says
SCA-V4-002 revised the OI-001/002/012 text "in DEL-09-07, DEL-01-04 and
DEL-02-02" only.

**Inference.** Design work on DEL-01-02, 01-05, 02-04 or 09-01 would start
from a SoW that lags the first-increment rulings (D2, D3, D4). That lag would
have to be carried as a stated reading or fixed by a further scope change
first. No executor in this run may write a SoW.

## 5. Recommendation (advice for an owner question; not settled)

### 5.1 The question

Should any outside deliverable get design work inside this pass? The owner's
standing answer is DECISION-1 D1: "The standalone-App definitions
(DEL-01-02…05, 02-02, 02-04) are left for a later undertaking; this one does
not start them." The start direction for this run names the first increment
only.

### 5.2 Recommendation

**Do not open a Design file for any outside deliverable in this pass, with one
candidate exception to put to the owner: DEL-01-04, limited to the App act
control and person identity.** Settle N-1…N-5 (§2.3) as decisions and as edits
inside the 14.

In order of value:

1. **Ask the owner N-1 and N-2 together.** If the owner wants an App-side
   *performed* act to be part of what the 60% position shows, then DEL-01-04
   is the one outside deliverable that warrants a bounded node. It would need
   a SoW revision first, since its SoW does not state the control, and would
   then be an interface note of the size described under I-12. If the owner
   does not, record the person identity choice only, and leave X-1 held as it
   is.
2. **Reconcile N-4 inside the 14.** No outside work.
3. **Put N-3 to DEL-04-01's node**, with an owner question if the node cannot
   settle it from records.
4. **Put N-5 (OI-009) to the owner** if HOSTING is to be structurally settled
   in this pass.
5. **Add the unnamed outside consumers to the suppliers' receiver tables**
   (§3.6) as part of the re-pin; this is bookkeeping in the 14.

### 5.3 Reasons for keeping outside design out

- D1 is an owner decision and has not been changed. The run's start direction
  does not widen it.
- By my reading, no inward arc requires the supplier's *definition* for the 14
  to reach the six-aspect depth LOOP_INIT describes (§2.3). Ten of the
  fourteen contributions are implementation, fixture or qualification
  evidence; four are conditional on decisions that are open at later points of
  need (OI-022, OI-023, OI-026).
- The four held arcs are non-gating by the DAG-003 reading rule, and X-1 is
  narrow by the HANDOFF's standing note.
- The consumer side already carries the supplier requirements where they
  matter (EXEC §5 CAP-1…CAP-9; HOSTING §6.5 and §8 S-1…S-7; EXEC §6.5; WD §8).
  An outside Design file would mostly restate them.
- Four of the six outside SoWs lag the D2, D3 and D4 rulings (§4.2). Designing
  on them invites a second re-pin.
- The pass already has 17 files to re-pin and deepen. LOOP_INIT: "Size
  concurrency to actual review and integration capacity".
- The standalone-App designs depend on OI-008 (process division) and OI-014
  (shared placement), both open with the App implementation owner.

### 5.4 Reasons against (for doing some outside design now)

- LOOP_INIT puts the 60% position at "a route to completion for which further
  structural changes are no longer anticipated". Three outside joins still
  carry a choice that could change a first-increment file: the person
  identity and act control (I-12), registration as an act (I-3), and the
  DEL-01-01/DEL-01-02 split (I-1).
- The act control is the only route to a *performed* act in Phase 1 (I-12).
  If it stays undefined on the supplier side, the increment's central positive
  case stays a designed case with no executable route, and the same open item
  is carried in seven files (ACT, EXEC, RS, WD, EXAMPLES, GUIDE, CA).
- LOOP_INIT: "Coordinate coupled work until its inputs permit independent
  progress". DEL-01-01 and DEL-01-02 share the outstanding-request register;
  HOSTING defines DEL-01-02's half by proposal (§6.5) with no receiving
  comparison (F-15).
- A one-sided requirement can be wrong. DEL-01-04's SoW frames its work as
  native request cards and faithful display; whether a dedicated act control
  fits that slice has not been examined from its side.

### 5.5 If the owner wants more than DEL-01-04

Second in line is **DEL-01-02**, limited to the register split and the
evidence handoff (I-1): it closes HOSTING F-01, U-09, U-10, U-14 and U-16 and
RS U-20. I would not recommend DEL-01-05 (its open item is the owner decision
OI-009), DEL-02-02 (the 14 already assume a shape consistent with its SoW; the
open item is N-3), DEL-02-04 (OI-018 is open), DEL-09-01 (nothing
candidate-bound is due), or DEL-07-01, 07-02, 08-01, 08-02 (conditional by the
accepted basis).

## 6. Limits of this survey

- The ScopeOfWork files of the 25 deliverables not listed as read whole in §0
  were read by cited item only. A statement there that bears on a join but is
  not cited by a register row could have been missed.
- The Design files were searched by deliverable ID. A passage that assumes an
  outside contribution without naming the deliverable (for example by package
  or by role name) would not have been found, except where it fell inside a
  block read for another reason.
- "Offered" in §3 compares text with text. No fixture was run and no candidate
  exists.
- The SWBPIPE facts cited (SQ-01, SQ-02, SQ-17, SQ-29) are taken as the 17
  Design files carry them. They describe SWBPIPE's state on 2026-09-28 and are
  not commitments.
- This file claims no SWBPIPE join, witness or adoption, and changes no
  register, SoW, status or graph.
