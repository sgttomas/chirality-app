# Candidate examination protocol and support

- **Contribution:** DEL-09-01/EXP-v0.2. It supersedes EXP-v0.1 (frozen unit
  U1, file sha256 `dc6b6a0c24a3c780e017de3e078473d3303386961f3feb576604d134648ecbc0`),
  repaired for review RV-EXP-U1 (findings EXP-R-A…EXP-R-M; see "Changes")
  under rulings R23-17, R23-19, R23-20 and R23-21; U-EXP-1 closed in place
  under R23-22 after RV's confirmation. The schemas move to
  `…:0.2` with records in format `EXP-v0.2`.
- **Status:** DRAFT DEFINITION — proposed, unsupplied, not implemented, not
  accepted. Beside it: three PROPOSED schemas (JSON Schema 2020-12), each
  with valid, invalid and rule-violation example sets, and a design
  prototype `prototype/check_exp.py` (not product code).
- **Run and node:** `APP-V4-DESIGN-PASS-4-20261003`, node O-B1; owner O-B
  (Type 2, Claude Opus 5.5), 2026-10-03.
- **Serves:** OUT-001…OUT-004; REQ-001…REQ-008; designed cases for
  VER-001…VER-009 (§12). Nothing here is executed against a candidate.
- **Basis, pinned by current bytes** (`shasum -a 256`, working tree at
  `58645e7c66` plus this run's uncommitted files):
  - ScopeOfWork.md `8e53669468bd5885739ceaeb633dc5a3b134a04f1bf862235d8d2272dd5f658a`.
    **R23-5 re-pin:** this ScopeOfWork is unchanged since INIT
    (`ddd721a90a`); no SCA-V4-003 block changed it (no ledger row has
    DEL-09-01 as its deliverable), so no block bears on this file.
  - `Dependencies.csv` `96ea447bba37f1225d305569226e822123ab52d9aa2e2e5c8f48e5200e5352f9`.
  - `docs/EXAMINATION.md` `471798bc2f2dc0202ae40d9d5cf033a22ae41af2a0afdf58032cf37a687957d0`
    (§§1–2, V4-EXM-01…05, §§3–7); `docs/PRD.md`
    `bb6e786f7a6c01dc5ce2f16f58e6c600989a12808ff47ce4fd87924bcc6c49bd`
    (V4-CST-02, V4-CST-06); `docs/ARCHITECTURE.md`
    `317d5789272c5206599936fa9b4e68551b30016d226b88039f0153afa02d828c`
    (§1 M-7, §6, §8); `docs/OPERATING_METHOD.md`
    `98836b5240ed235ec2ad38b08a9525dc9f2b366145c0736f7c70d22c1c93c5dd`
    (V4-OPS-30…34); `docs/HOST_INTEGRATION.md`
    `d4331c39db7f452cd3ba72fdfa4bad540a6053931218359a93646971acb28d9f` (§1).
  - Supplier: DEL-01-01 `HOSTING_BOUNDARY.md` (HOSTING-v0.9)
    `5401f26d9a2a739a725771c8ce83c62ac5fa07be69b0338ee5670b9453d76d87` (C1 re-pin, R23-21 item 4)
    (§7.1, §9.1–§9.6); `PIN_SPIKE_0.158.0.md`
    `0e090a4ca14e3ec323e8302ea4bc4e1fefc66bee50d0d3247e1cd0ddc04eb115`.
  - Receivers' files read to check the interface (cross-references, not
    reliance): DEL-09-06 `CONNECTED_ACTIVITY_CONTRACT.md` (CA-v0.7)
    `44a9b288291c0716ba34945aae46163b69f5af96d0292ca03d343eec5811a9ee` (C1 re-pin, R23-21 item 4)
    and `w14-result-record.schema.json`
    `20d3c976912318dde2d189f6a3761796ee09f40f01b398dd2fe50ab91b429b91`;
    DEL-09-09 `EXTERNAL_TRACE_CASES.md`
    `cc1543619b767ede6af9fb614c82faa7430da634b4846fa263a1da619383808a` (C1 re-pin, R23-21 item 4)
    and `xt-result-record.schema.json`
    `3b0ff2bbd1da8dab61147218b6c512146b58b4dc13eea6a2b1c60f7c5b697b4b`;
    DEL-01-04 `APP_ACT_CONTROL.md` at AAC-v0.2, the version relied on
    (R23-21 item 3; committed at `31d65b0be3`)
    `062ce28c8a4ec0bc79fc6b6c421245057a59815df14b88fa779b61eeb98be7d7`.
    O-A's AAC-v0.3 (A16) leaves NA-3 and VC-AAC-03, the only parts cited,
    unchanged (`git diff` checked 2026-10-03).
  - Graph: `_DAG/DAG-004/HANDOFF_STATE.md`
    `3c374f5e9fa4cfaa479699cddf5191b69bba2e0fe4707cb17acbe27dddc528ba`;
    SCC case `_DAG/cases/SCC-CASE-003/Case_Datasheet.md`
    `3e5277f6535597eb39e0a750dcb16d11712b738065ece2275b9b33b599a364e2`.
  - Rulings, cited by ID (R23-21): R23-1, R23-2, R23-3, R23-5, R23-7,
    R23-11, R23-12, R23-13, R23-15 (partial capture, consistent with F-4),
    R23-17, R23-19, R23-20, R23-21, R23-22. Review: `reviews/RV-EXP-U1.md`.
    Other run records:
    `OWNER_DECISIONS.md`
    `e4350f61a93edf0d2d4bfc588fcaa17ae23981baa6059617dcc430cda3008cd8`
    (including "Scope of owner questions": no human checkpoint is added here);
    `SURVEY/S1-B.md`
    `1b4de1cb45f2247905115e8c5b46473b4827cbda9b9a60f44c2e94063bd9f6da`
    (§2). Standing owner decisions of earlier runs: first-increment D2, D3,
    D4; pass-3 DECISION-K3 K-1, DECISION-L L-1, L-6, L-7; SCA-V4-003
    DECISION-1 Q-5 (App act control in DEL-01-04).
- **Pin basis (R23-3).** Written for either Codex pin, 0.158.0 or 0.160.0.
  The pin is a parameter of every record (`configuration.codex_pin`) and of
  every fixture. The only supplier facts this file relies on are HOSTING
  §9.2's fixture labels, §9.3's outcome labels and §9.1's capture and
  redaction method, all stated by HOSTING-v0.9 at 0.158.0. The labels are
  HOSTING's definitions, not Codex behaviour. The redaction categories were
  extended from what the 0.158.0 stream carries and may grow at another pin;
  EXP refers to them by reference, so the record format does not change. If
  node VC or a HOSTING revision changes §9.2 or §9.3, the prototype's EXP-R9
  check fails at once. Examples exist at both pins (§12).
- **Receivers:** DEL-09-02, 09-05, 09-06, 09-07, 09-09, 09-10, 09-11, 09-12
  (admitted arcs; §2.2); DEL-01-06 (held, SCC-003); the named independent
  reviewer of each candidate (DEP-09-01-030, not topological).

## 0. Reading this file

**What it is.** The protocol and the reusable support with which App v4
candidates are examined: what a result record is, how a result is bound to
its candidate and configuration, what the five outcomes mean, how fixtures
and recorded exchanges are used, how a change reopens checks, how criteria
are protected during repair, how a candidate is independently reviewed, and
how WebKit, Chromium and native packaged runs are told apart.

**What it is not.** No journey's cases (each journey owner defines its own:
DEL-09-02, 09-05…09-12); no feature tests (feature owners keep them); no
package (DEL-01-06); no host implementation (external); no human act, which
only the person performs; no policy (OI-001/OI-002 rulings D2/D3 are
carried, not made); no CI configuration (LOOP_INIT: no v4
`software-workflow.json` exists).

**Labels.** As in the other App v4 Design files: SETTLED (accepted text
says so), DERIVED (follows from accepted text), INTEGRATION (an integrator
ruling), PROPOSED (this file's design choice).

**Overtaken wording followed (R23-7, R23-11).** The ScopeOfWork's TBD-001
reads OI-001/OI-002 as unruled and OI-012 as having no pin. This file
follows the current decisions: D2/D3 rule OI-001/OI-002 for the first
increment; D4 selected 0.158.0 as the definition and generation pin, while
the qualification pin is still open (OI-012). CLM-004/REQ-006's reviewer
rule is applied as R23-12 reads V4-OPS-34. The wording is listed for the
next amendment (R23-11), not edited here.

## 1. Owner and act boundary (REQ-008; CLM-001, CLM-005, CLM-006)

| Act | Owner | This file's part |
|---|---|---|
| Integrate runner, fixture and evidence adapters | App examination owner (DEL-09-01) | Defines them (§4–§9) |
| Focused feature tests | Each feature owner | Consumes their evidence by reference (§2.1 IN-2) |
| Journey cases and their witnesses | DEL-09-02, 09-05, 09-06, 09-07, 09-09, 09-10, 09-11 | Supplies the record, outcome and reopening rules they use |
| Practitioner validation and its period | DEL-09-12 with the owner (OI-016) | Records `activity: validation` only for an actual practitioner's use (§3.3) |
| Package, signing, install/launch witness | DEL-01-06 | Native smoke route consumes the package (§10, SCC-003 M2) |
| Independent review | The candidate's independent reviewer | Supplies the review record and its rules (§7) |
| Any human act (review, registration, grant, denial, sign-in, decision) | The person | Records an actually performed act by reference to its own record, actor distinct from recorder; never manufactures one (§3.5) |
| Criterion change | Whoever the governing instrument names | Cites the disposition; never makes it (§6.3) |

## 2. Interfaces

### 2.1 Inputs

| ID | Input | Supplier | Arc (DAG-004) | Point of need | If absent |
|---|---|---|---|---|---|
| IN-1 | Selected Codex pin (definition pin 0.158.0; qualification pin under OI-012); HOSTING §9.2 fixture labels, §9.3 outcome labels, §9.1 capture and redaction method, §7.1 distribution identity elements | DEL-01-01 | DEP-09-01-019, admitted | Before protocol generation, replay and qualification | Records carry the pin they ran on; no qualification claim (§5.2 F-8) |
| IN-2 | Focused feature evidence and the feature owners' designed cases (e.g. RECOVERY VC-R-*, NIR VC-NIR-*, AAC VC-AAC-*, ACCESS VC-A*, NPTD NV-*) | Feature owners | DEP-09-01-014, not topological | Seam selection and joining | Seam left out of the join; named as a missing input |
| IN-3 | Recorded real exchanges with origin and configuration | DEL-01-01's capture method; journey owners' captures | DEP-09-01-015, not topological | Replay seam checks | Replay case `not-run`, missing input named |
| IN-4 | Identified candidate, applicable criteria, selected configuration, available contributions | Journey owner | DEP-09-01-013, not topological | Each actual examination | No record is written; the case stays `AWAITING INPUT` (§5.1) |
| IN-5 | Package and its OUT-002 identity record; install/launch witness | DEL-01-06 | DEP-09-01-016, **held** (SCC-003) | Before the native packaged smoke (SCC-003 M2) | Native packaged route `blocked`, never replaced by a browser pass (§9) |
| IN-6 | Independently produced review record | The candidate's reviewer | DEP-09-01-017, not topological | VER-007 | No independence claim |
| IN-7 | Evidence of an actually performed human act | The person, through the act's own surface | DEP-09-01-018, not topological | The positive faithful-record check (VER-004) | The positive case stays `not-run`; no act is invented for a fixture |
| IN-8 | Admission input for a later research fixture | Domains/SWB/App receiving owners (OI-023, OI-026) | DEP-09-01-020, not topological | Only if a research fixture is used | Not used |

**Register note (for the next amendment, R23-11; no row added).**
DEP-09-01-019's Statement names only the selected pin. R23-1 has this file
rely on HOSTING §9's labels and method over the same admitted arc. A
statement widening is listed in §14; it adds no arc.

### 2.2 Outputs

| ID | Output | Receiver | Arc (DAG-004) | What the receiver gets |
|---|---|---|---|---|
| OUT-1 | The result record format and rules (§4.1; `exam.result-record.schema.json`; the rule set EXP-R1…R9, §3.5) | DEL-09-02, 09-05, 09-06, 09-07, 09-09, 09-10, 09-11, 09-12 | DEP-09-01-022…029 (representatives DEP-09-02-020, DEP-09-05-011, DEP-09-06-035, DEP-09-09-012, and DEP-09-01-025, -027, -028, -029), admitted | Candidate/configuration/date binding; outcome meanings; evidence provenance; missing-input and blocked reporting |
| OUT-2 | The change-impact record and reopening sequence (§4.3, §6.2) | Same | Same | Which results a change makes historical, which cases it reopens |
| OUT-3 | The review record and protocol (§4.2, §7) | Same; the independent reviewer | Same; DEP-09-01-030 | How a review is bound, who may review, what is reported |
| OUT-4 | Interface and native execution routes and their identities (§8, §9) | Same; DEL-01-06 | Same; DEP-09-01-021 (**held**, SCC-003) | Route kinds, engine/platform identity, native route method |
| OUT-5 | Fixture support rules (§5) | Same | Same | Invented material, recorded exchanges, replay versus live marking, live-run selection |
| OUT-6 | Support revision identity (§4.4) | Same; DEL-01-06 | Same | Which revision of this support a record or a package's witness used (SCC-003 M1) |

**How DEL-09-06 and DEL-09-09 meet this (R23-1: mapping only).** Their
PROPOSED W14 and XT result records stay as they are. §3 maps their
outcome, run kind and evidence labels to this record one to one; the
prototype checks the outcome mapping against their schemas (EXP-R9).
Where a W14 or XT record lacks an element V4-EXM-01 names (harness and model
versions and model server are not separate fields there; W14 carries them
through its W14-00 identification record and `model_destination`), the
journey's record keeps that through its own identification record; this file
asks nothing more of it (§14 observation O-2).

## 3. Vocabulary and mapping (R23-1)

### 3.1 Outcomes

This record's outcome values are HOSTING §9.3's outcome labels, as written:
`pass`, `fail`, `blocked`, `not-run`, `inconclusive` (INTEGRATION, R23-1).
DEL-09-01 does not govern them. HOSTING names them without defining them.
Their meanings follow EXAMINATION §1 and ScopeOfWork REQ-002, with the
`blocked`/`not-run` boundary set by **R23-20 (INTEGRATION)**, so that every
receiver applies them the same way:

| EXP value (= HOSTING §9.3) | Meaning | W14 / XT schema value | EXAMINATION §1 word |
|---|---|---|---|
| `pass` | The criterion was evaluated on the actual subject and met | `passed` | passed |
| `fail` | The criterion was evaluated on the actual subject and not met | `failed` | failed |
| `blocked` | The case was attempted, at its start or later, and a stated precondition or dependency stopped it; the cause is recorded (`blocked_by`, required) | `blocked` | blocked |
| `not-run` | The case was planned for this candidate and not attempted; why, or what is missing, is recorded | `not_run` | not run |
| `inconclusive` | Execution occurred but the evidence is insufficient or ambiguous for the criterion | `inconclusive` | inconclusive |

**Aggregation over parts (EXP-R1, DERIVED from CA W-R6, in these labels;
R23-19):** over the **applicable** parts only, `fail` if any part failed;
otherwise `blocked` if any part is blocked; otherwise `pass` if every part
passed; otherwise `not-run` if no part ran; otherwise `inconclusive`. A case
outcome never hides a failed part.

**Parts that do not apply (R23-19, DERIVED).** A part may be declared not
applicable only in the case definition as bound to its fixture, before the
run, with its reason. The record lists it under `parts_not_applicable` with
the case definition and its sha256 (`declared_in`); it is left out of
aggregation and never also appears among the run parts. A part declared
applicable that did not run is `not-run`, and the case cannot pass (an
applicable `not-run` part beside passes aggregates to `inconclusive`).

### 3.2 Run basis and evidence labels

| EXP `run_basis` | Means | CA §7.1 / XT label | HOSTING §9.6 | RECOVERY / NIR "Needs" |
|---|---|---|---|---|
| `definition_check` | The definition's rules run on a model or prototype | *illustrative* (definition check) | "a case that passes shows that the rules run end to end as written" | D (model) / *model* |
| `rehearsal` | A test double, or a replayed recording, without a candidate | *test-double* (rehearsal) | supplier double; replay | D, F / *double*, *fixture* |
| `candidate` | An identified App candidate (and host candidate, where joined) | *actual host* (joined witness) where a host is involved | "the candidate" | C (with P where a person acts) / *candidate*, *person* |

Only a `candidate` record can stand for a scenario (V4-EXM-nn) or a VER
criterion, whatever its outcome (EXP-R3; the schema refuses a scenario on
any other basis). The CA/XT gap labels (AWAITING INPUT, HELD,
NOT-OBSERVED) are case states here (§6.1), not outcomes.

### 3.3 Activity

`verification` (agent- or person-operated scenario against a candidate) or
`validation` (a practitioner's actual use, DEL-09-12's activity; requires the
practitioner and a candidate basis). Neither substitutes for the other
(EXAMINATION §1; REQ-003).

### 3.4 Evidence provenance, fixture standing and limits

- **Provenance** (each evidence reference carries one; EXAMINATION §2; XT
  §6): `test_definition`, `recorded_replay`, `static_inspection`,
  `live_observation`, `person_act`, `host_receipt`, `review_record`,
  `feature_check`. One evidence set may hold several; each keeps its own.
- **Fixture standing:** HOSTING §9.2's labels as written: `recorded`,
  `recorded-truncated`, `mutated`, `constructed` (EXP-R9 checks them
  against HOSTING).
- **Limits** carry their own vocabulary name (`{label, vocabulary}`): EXP's
  own limits, or another owner's (for example RS-v0.9's evidence-limit
  labels). This file does not define or check other owners' labels; a
  journey that uses RS's labels checks them against RS (as CA's prototype
  does). DERIVED: DEL-09-01 cannot rely on DEL-04-03 without a cycle
  (DEL-04-03 reaches DEL-09-01 through held arcs; DAG-004, both layers).

### 3.5 The rule set (EXP-R1…EXP-R9)

| Rule | Statement | Enforced by |
|---|---|---|
| **EXP-R1** | Outcome is the aggregate of the applicable parts (§3.1); a declared not-applicable part is listed with its pre-run declaration and never also run | Prototype; schema requires `declared_in` |
| **EXP-R2** | Basis, subject and route bind: each `run_basis` has its subject kind; a `candidate` record names pin, route, model and model server; native routes name platform, native route and the WKWebView identity; interface routes name engine, platform and their runner definition check; a `native_packaged` result other than `not-run` needs a candidate built as a DEL-01-06 package with its record; `ui_automation` names its tool and tool definition check | Schema |
| **EXP-R3** | Only a `candidate` record stands for a scenario (V4-EXM-nn), whatever its outcome | Schema (no `scenario` on other bases); prototype as a second check |
| **EXP-R4** | A part that needs native evidence passes only on evidence from a native route | Prototype |
| **EXP-R5** | Every cited act names an actor other than its recorder | Prototype |
| **EXP-R6** | A review reported as independent has a reviewer who is not an author and whose separation held; a claim of a different model family needs both identities exposed and of different families | Prototype |
| **EXP-R7** | Review standing matches its findings: `no_findings` has none, `findings_open` has an open one, `findings_dispositioned` has none open | Prototype; schema requires `confirmed_by` for a repair |
| **EXP-R8** | Every affected prior result of a change is `historical` or `reopened` and cites that change | Prototype |
| **EXP-R9** | Outcome and fixture labels equal HOSTING §9.3 and §9.2; the mapping to W14 and XT is one to one | Prototype, reading the actual files |

Required reasons (`blocked_by` for `blocked`; `not_run_because` or
`missing_inputs` for `not-run`; `limits` for `inconclusive`) are schema
conditions of the outcome, not separate rules.

## 4. Data (PROPOSED; R12-2: names are Chirality's; placement §8.4)

### 4.1 Result record — `exam.result-record.schema.json`

One record per examined case or part on one subject. Elements:

| Element | Meaning | Rule |
|---|---|---|
| `support_revision` | This support's revision (EXP version, schema id, prototype digest) | §4.4; SCC-003 M1 |
| `case` | Case id, owning deliverable, scenario (V4-EXM-nn) where one applies, part | The journey owns the case |
| `criterion` | Source criterion and the sha256 of its text as examined (R23-17); a criterion disposition reference if a separately authorized one applies | §6.3 |
| `activity` | `verification` / `validation` | §3.3 |
| `run_basis`, `subject` | Basis and its matching subject: candidate (revision, build identity, packaged and its DEL-01-06 record), double (identity and file digests, replayed recording), or definition (version label) | Schema ties basis to subject |
| `configuration` | Codex pin; distribution identity (HOSTING §7.1) where verified; model requested/reported/version; model server (kind, label, version, App-owned home H-acct/H-key per K-1/L-1); route (§8: kind, engine, platform, WKWebView identity on native routes, native route method, runner or tool definition check); tool-permission and sandbox settings in effect, by reference (HOSTING §9.1; D3); host profile | V4-EXM-01. For a `candidate` basis, pin, route, model and model server are required, each as a value or `not_observed`/`not_applicable` |
| `date` | Value and source (`observed_clock`, `record_timestamp`, `stated_by_person`) | As evidenced |
| `outcome`, `parts`, `parts_not_applicable` | §3.1; not-applicable parts with their pre-run declaration (R23-19) | EXP-R1 |
| `evidence` | References with provenance, digest, route, fixture standing, redaction record | Linked, never copied |
| `missing_inputs`, `blocked_by`, `not_run_because` | What is missing and from whom; what blocked; why not run | Required by outcome (schema) |
| `limits` | `{label, vocabulary, detail}` | Required for `inconclusive` |
| `acts_cited` | Record reference, kind as its owner names it, actor, recorder, capture evidence | EXP-R5 actor ≠ recorder |
| `currency` | `current`, `historical` or `reopened`, with the change record | §6.2 |

### 4.2 Review record — `exam.review-record.schema.json`

Review kind (`v4_ops_34`, the review V4-OPS-34 requires, or
`additional_person`), whether it is reported as independent, subject
(candidate or definition identity), the evidence set the reviewer actually
read, the authors, the reviewer with actual separation and model identity
(or `not_exposed`), for a `v4_ops_34` review the preference (`preferred:
codex`, `used`: `codex` or `claude_fallback`, and the fallback reason), the
family claim, findings with claim, evidence, consequence and disposition, the
review standing and the date. §7.

### 4.3 Change-impact record — `exam.change-impact.schema.json`

The change (kind: candidate code, Codex pin, configuration, fixture, native
route, support revision, criterion disposition, package, case definition; description;
evidence; disposition reference for a criterion disposition), from and to
identities, the affected cases with their prior results and reasons (and
rerun results once run), how the rest were judged unaffected, and the date.
§6.2.

### 4.4 Support revision

A support revision is this file's version label (now EXP-v0.2), the three
schema `$id`s (`…:0.2`) and the sha256 of `prototype/check_exp.py`. It is published by the
deliverable's freeze or merge, never by a record writer. Every record names
the revision it was written under. A later revision that changes a rule a
result relied on is a change of kind `support_revision` (§6.2).

## 5. Fixture support (OUT-001; REQ-001)

- **FX-1 Invented material only** (V4-CST-06; SETTLED). Fixtures carry a
  subject label naming them invented; no client or engineering data is
  required. A later research fixture needs its admission input (IN-8) and
  is not used otherwise.
- **FX-2 Recorded exchanges** follow HOSTING §9.1 capture and redaction
  categories and §9.2 standing labels, by reference (R23-1). A redacted
  fixture never claims byte identity with the original exchange.
- **FX-3 Replay versus live.** A replay is `run_basis: rehearsal`,
  `route: seam_replay`, `provenance: recorded_replay`. A live seam run on a
  candidate is `route: seam_live`. A replay never stands for a live or
  joined witness (EXP-R3; CA §7.1).
- **FX-4 Pin binding.** A recording is bound to the pin it was captured at.
  Replaying it against another pin is allowed as a comparison (HOSTING §9.5
  step 6) and is recorded with both pins in its evidence; it is not a
  result at the new pin.
- **FX-5 Live-run selection (PROPOSED).** A live run is chosen only where no
  recording can show the criterion (an act, a native step, a first capture,
  a changed pin). The record names the reason in `limits` with vocabulary
  `EXP` (`live run: <reason>`). No quota is set (REQ-001).
- **FX-6 Fixture inventory.** Each journey keeps its fixture list; EXP asks
  only that each fixture has an origin, a pin where Codex is involved, a
  standing label and a digest.

## 6. States and sequences

### 6.1 Case state (per case, per subject)

| State | Entered when | Leaves to |
|---|---|---|
| DESIGNED | The journey defines the case (with any not-applicable parts declared, R23-19) | PLANNED; AWAITING INPUT |
| PLANNED | The case is planned for a named candidate (an examination of that candidate is opened) | RUN; or RECORDED as `not-run` |
| AWAITING INPUT | A named input (§2.1) is missing | PLANNED when it arrives |
| HELD | An input is held by an unresolved owner matter (e.g. host joins deferred, DECISION-3) | PLANNED when released |
| RUN | Execution attempted | RECORDED |
| RECORDED | A result record exists | REOPENED on a change; stays otherwise |
| REOPENED | A change-impact record names the case | PLANNED (rerun) |

**Every planned case gets a record (R23-20, INTEGRATION).** Once a case is
planned for a named candidate it is recorded honestly, whatever happens: a
case not attempted is `not-run` with `not_run_because` or `missing_inputs`;
a case attempted and stopped at its start by a stated precondition or
dependency is `blocked` with `blocked_by` (as DEL-09-07 LHQ LF-1 does).
Before a candidate is named (DESIGNED, or AWAITING INPUT with no subject),
there is no subject to bind a record to, so the journey lists the case with
its missing input instead.

**Held arcs are not HELD cases.** SCC-003's held arcs (and any DAG-004
candidate edge) place no case in HELD and drive no readiness (DAG-004
`HANDOFF_STATE.md` reading rule 3). A native packaged smoke case is
AWAITING INPUT for the actual package (IN-5) and nothing else.

### 6.2 Reopening (REQ-004; V4-EXM-03)

**SQ-1 A change arrives** (any change kind in §4.3):
1. The examination owner writes a change-impact record naming from/to.
2. **Reliance map.** For each recorded result, the record's own elements
   say what it relied on: subject identity, `codex_pin`, configuration,
   route, fixtures (digests), support revision, criterion identity. A result
   is affected if the changed thing appears in any of them. A result whose
   reliance cannot be read is affected (DERIVED from V4-EXM-03: only an
   actual check supports a candidate).
3. Each affected result's `currency` becomes `historical` (its subject is
   superseded) or `reopened` (same subject, a changed configuration, fixture
   or rule); it keeps its outcome and evidence (EXP-R8).
4. Each affected case returns to PLANNED; its rerun result cites the change.
5. The unaffected basis is written down. Old passes stay attached to their
   own candidate.

### 6.3 Repair with the criterion protected (REQ-005; V4-EXM-05)

**SQ-2 A failure:** record `fail` → diagnose (evidence of cause) → repair in
the owning deliverable → new candidate → change-impact record → rerun
against the **same criterion identity**. If the criterion text's identity
differs from the one examined, the rerun is not a repair of that failure
unless a separately authorized disposition is cited (`disposition_ref`, and
a change of kind `criterion_disposition`). Deleting the case or lowering
the criterion is not repair; a record showing it is a finding (§7).

### 6.4 Examining a case

**SQ-3:**
1. The journey owner names candidate, configuration and route; checks the
   inputs (§2.1). Missing → AWAITING INPUT, named; once planned on a named
   candidate, a case not attempted is recorded `not-run` (§6.1).
2. For a supplier pin: the candidate's supplier verification (HOSTING §7.2)
   result is read. `refused` → the case is `blocked` by the supplier
   verification (F-8).
3. Run on the route (§8, §9). Capture evidence with provenance and route.
4. Write the result record with the support revision; validate it against
   the schema and EXP-R1…R9 (§3.5) before it is relied on.
5. Return results and limits to the journey owner and the reviewer.

## 7. Independent review protocol (REQ-006; OUT-003)

**Reviewer (SETTLED by V4-OPS-34 as written; R23-12).** A Codex reviewer,
with the stated different-model Claude fallback (`review_kind: v4_ops_34`).
A person may review **in addition** (`review_kind: additional_person`); that
never replaces the V4-OPS-34 review and carries no preference. No other
reviewer kind is provided for. Each review reports actual separation and
model identity.

- **RV-1 Binding.** A review names the exact subject (candidate revision and
  build identity, or definition and digest) and the evidence set read. It
  covers only that subject.
- **RV-2 Separation.** The reviewer is not an author of the candidate or of
  the evidence under review. `separation` records what actually held:
  `separate_person`, `separate_session_no_authoring`, or `not_separate`.
  An honest `not_separate` review is a valid record with
  `reported_as_independent: false`; EXP-R6 fires only when a review is
  reported as independent while separation does not hold.
- **RV-3 Preference and fallback.** `preferred` is always `codex`; `used` is
  `codex` or `claude_fallback`. For the fallback, `fallback_reason` states the actual unavailability
  as observed (for example, no Codex reviewer session could be started for
  this examination). Choosing the fallback for convenience is not an
  unavailability.
- **RV-4 Model identity and family.** Each party's model identity is
  recorded with where it was exposed, or `not_exposed`. A claim of a
  different model family needs both identities exposed and of different
  families (EXP-R6). A fresh context is reported as such and says nothing
  about family.
- **RV-5 Findings.** Each finding states the affected claim, its evidence
  and its consequence. The owner repairs; the reviewer who raised it
  confirms the repair (`confirmed_by`). Standing is review standing only
  (`no_findings`, `findings_open`, `findings_dispositioned`; EXP-R7); it is
  never acceptance, release or professional reliance.
- **RV-6 How a Codex reviewer is run (PROPOSED).** The reviewer is a Codex
  conversation given the evidence set as files and the review brief, in a
  home or session not used to author the candidate. Its reported model is
  read from Codex's own report where Codex exposes it (HOSTING §8.3 observed
  model destination), else `not_exposed`.

## 8. Execution routes (OUT-004; REQ-007)

### 8.1 Routes and the native route choice

| Route | What runs | Identity recorded | Supports |
|---|---|---|---|
| `model_only` | A prototype or model | Definition version | Definition checks only |
| `seam_replay` | App seam against a supplier double replaying a recording | Double digests; recording; pin | Seam regression |
| `seam_live` | App seam against a live supplier on a candidate | Candidate; pin; distribution identity | Seam checks on that candidate |
| `interface_webkit` | The App interface in a WebKit engine | Engine name and version; platform | Interface portability evidence (V4-EXM-04) |
| `interface_chromium` | The App interface in Chromium | Engine name and version; platform | Interface portability evidence |
| `native_development` | An unpackaged App build on macOS Apple Silicon | Candidate; platform; WKWebView identity; native route | Native behaviour on that build; not a packaged witness |
| `native_packaged` | The DEL-01-06 package, installed | Candidate with package record; platform; WKWebView identity; native route | Packaged smoke (V4-EXM-04) |

**Interface runner (technical choice, R23-13; PROPOSED).** The App's
interface is run in a cross-engine browser test runner with a WebKit
project and a Chromium project, against the supplier double or recorded
fixtures behind the interface's seam. A runner such as Playwright is the
expected kind; the implementer chooses it against §8.3's definition check,
and its name, version and admitting check are recorded per run (`engine`,
`runner_definition_check`; R23-17 item 3).
*General knowledge, not verified in this repository:* a browser runner's
WebKit build is not the macOS WKWebView the App ships in. So the WebKit
route is portability evidence; the WKWebView is covered by the native routes.

**Native route (technical choice, R23-13; recorded with reasons).**

- **N-1 Person-operated (the standing route for every native step that
  includes a person's act or an OS-level action).** The person operates the
  App on macOS; the examiner records each step on a native-step form
  (`form_ref`): step, time, what was done, what was observed, captures. Reasons:
  1. V4-EXM-10/11/12 contain acts only the person performs (review,
     registration, grant, denial, sign-in, key entry). An automation tool
     operating them would not be the person; REQ-003 forbids manufacturing
     the act, and DEL-01-04's act control, by its own text, captures only the
     person's confirmation (AAC NA-3; VC-AAC-03) — a consistent
     cross-reference, not a reliance.
  2. Window close/reopen, quit and relaunch are OS-level steps that the
     feature owners' native cases already mark as needing the person and a
     candidate (RECOVERY VC-R-14 "C, P"; NIR VC-NIR-11).
  3. *General knowledge, not verified here:* Tauri's WebDriver route has not
     supported macOS WKWebView, and macOS UI automation needs an
     Accessibility permission the person grants on that machine.
- **N-2 UI automation (admitted for steps with no human act).** For the
  packaged smoke (start, handshake shown, a conversation opens) and for
  repeated rechecks, a macOS UI-automation tool may run the steps once that
  tool version has passed its definition check (§8.3, EXP-DC-N2) on the
  candidate. The tool, its version and that check's record are recorded
  (`tool`, `tool_definition_check`). A step that is a human act is never run
  by N-2.
- **Route change.** Changing N-1/N-2, the tool or its version is a
  configuration change (§6.2, kind `native_route`); affected native results
  are reopened.
- **WKWebView identity.** Every native record names the macOS WebKit
  environment the interface ran in (`webview`: WKWebView, WebKit version, OS
  version), so the macOS WebKit environment is identified apart from the
  browser runner's WebKit (REQ-007, AC-008).

### 8.2 Native-step form (route N-1; U-EXP-3, decided)

One Markdown file per native record, `forms/<record_id>-N1.md` beside the
records (§8.4), cited by `native_route.form_ref` and digested in the
record's evidence. Layout:

- **Header:** record id; candidate revision and build identity; package
  record if any; Codex pin; WKWebView/WebKit and OS versions; the person
  operating; the examiner recording; date and time zone.
- **Step table**, one row per step in the case definition's order:

  | Step | Time (local, with offset) | Action and who did it | Observed | Captures (path, sha256) | Deviation or limit |
  |---|---|---|---|---|---|

- **Close:** steps not reached and why; the examiner's statement that the
  rows were written during the run, not reconstructed.

A row records what the person did, never an act on the person's behalf;
acts are cited by their own records (EXP-R5).

### 8.3 Definition checks for a runner or an N-2 tool (R23-17 item 3)

Before any result from a runner or tool counts, its version passes a
definition check, recorded as an EXP result record.

**EXP-DC-RUNNER** (interface runner; `run_basis: definition_check`, subject
the runner and its version; once per runner version):

- **DC-R1 Engine identity:** each project reports its engine name and
  version, and they match what the record will carry.
- **DC-R2 Sensitivity:** against the supplier double or a recorded fixture
  behind the interface seam, a known-pass probe passes and a known-fail
  probe (a deliberately wrong expectation) fails, in both engines.
- **DC-R3 Missing target:** an absent element or view yields `blocked` with
  its cause, never `pass`.
- **DC-R4 Evidence:** every run writes its captures with paths and sha256
  that the record cites.
- **DC-R5 Isolation:** the runner reaches no network destination other than
  the local fixture server (observed, not assumed).

**EXP-DC-N2** (UI-automation tool; `run_basis: candidate`, on the candidate
it will be used on; repeated for each candidate and tool version):

- **DC-N1 Paired steps:** the tool runs an act-free step list (launch, read
  the version, open a new conversation, close the window) and its reported
  observations equal a person's N-1 record of the same steps on the same
  candidate.
- **DC-N2 No act:** the tool's attempt to operate the App act control is
  refused and captures nothing (consistent with AAC NA-3, VC-AAC-03).
- **DC-N3 Missing window:** with the App not running, the tool reports
  `blocked` with its cause.
- **DC-N4 Evidence:** as DC-R4.
- **DC-N5 Permission:** the Accessibility permission the tool needs is
  granted by the person on that machine and recorded in the form.

The admitting record is cited by every later result
(`runner_definition_check`, `tool_definition_check`; EXP-R2).

### 8.4 Where records live (U-EXP-3, decided; OI-013/OI-014: no common service)

Records are files. No service, database or shared index is presumed.

- Each journey owner keeps its own records in its deliverable's working
  folder: `<PKG>/1_Working/<DEL>/Evidence/EXP/<candidate key>/`, where the
  candidate key is the candidate's revision (short form) and build identity
  digest prefix.
- One JSON file per record, named `<record_id>.json`; native-step forms in
  `forms/`; change-impact records in the folder of the deliverable that
  owns the change's examination; review records beside the records they
  review.
- DEL-09-01 keeps only its support revisions (this folder) and its own
  records (EXP-DC-*, EXP-VC-*) under its own `Evidence/EXP/`.
- A reader finds records by this path convention; nothing else needs to be
  running.

## 9. Native and browser evidence kept apart

- **NB-1** Each evidence reference carries its route. A part marked
  `needs_native` can `pass` only with evidence on a native route (EXP-R4).
- **NB-2** A native route that is unavailable makes the part `blocked`
  (attempted and stopped, cause stated) or `not-run` (not attempted), naming
  the missing input; it is never replaced by a browser `pass`.
- **NB-3** `native_development` never stands for `native_packaged`. A
  `native_packaged` result other than `not-run` needs a candidate built as a
  DEL-01-06 package with its record (schema, EXP-R2); without a package the
  case is `not-run` with the package as missing input.
- **NB-4** No Windows platform is introduced (V4-CST-02; OI-015).

## 10. SCC-003 R1 milestones (DEL-01-06 ↔ DEL-09-01), made concrete

SCC-CASE-003 recommends R1: explicit contributions under the existing
owners, both source relationships kept, no cut or merge. The two held arcs
stay held; nothing here changes a register or the graph.

| Milestone | Contribution | From → to | Identity that marks it | Then |
|---|---|---|---|---|
| **M1** Support revision usable | This file's support revision (§4.4): schemas, rules, native-step form N-1, route identities | DEL-09-01 → DEL-01-06 (DEP-09-01-021) | `EXP-vX.Y` + schema `$id`s + prototype sha256, at a freeze or merge | DEL-01-06 writes its install/launch witness (its OUT-003) as an EXP result record under that revision |
| **M2** Package available | A package and its OUT-002 identity record (App, Codex distribution identity, signing, entitlements), with DEL-01-06's own install/launch witness | DEL-01-06 → DEL-09-01 (DEP-09-01-016) | DEL-01-06's package record reference, cited in `subject.app_candidate.package_record` | Native packaged smoke leaves AWAITING INPUT (IN-5); the held arcs make nothing ready or blocked (§6.1) |
| **M3** Native packaged smoke run | EXP route `native_packaged` on that package | DEL-09-01 → journey owners and reviewer | Result records citing M1's revision and M2's record | Journeys use the package for their native witnesses |

Rules: M1 and M2 carry their own versions and may change independently; a
new M1 revision or a new M2 package is a change (§6.2) that reopens only the
results that cite the old one. DEL-01-06's own witness (its AC-003) and
DEL-09-01's smoke are separate results on the same package; neither stands
for the other. M1 does not wait for M2, and DEL-01-06's configuration work
does not wait for M1 (no finish-before-start order).

## 11. Failure behaviour

| ID | Condition | Behaviour | Record |
|---|---|---|---|
| F-1 | No identified candidate | No run; case AWAITING INPUT | None: no subject (journey's list) |
| F-1a | Candidate named, case planned, not attempted | `not-run` with reason or missing input (R23-20) | Result record |
| F-1b | Case attempted, stopped at its start by a stated precondition | `blocked` with its cause (R23-20) | Result record |
| F-2 | An input missing mid-case | That part `blocked`; parts needing its end state `not-run`, "blocked by ‹part›"; other parts may run | EXP-R1 aggregation |
| F-3 | Evidence insufficient or ambiguous | `inconclusive` with a limit | `limits` required |
| F-4 | Capture failed or redaction failed | The capture is discarded; the part is `blocked` (capture), never `pass` from memory. A partial capture that still bears on the criterion is `inconclusive` with its limit, never `pass` (consistent with R23-15) | `blocked_by: capture`, or `limits` |
| F-5 | Native route unavailable | NB-2 | `blocked` / `not-run` |
| F-5a | Runner or N-2 tool without a passed definition check | Its results do not count; the case is `not-run` on that route | EXP-R2 (schema) |
| F-6 | Reviewer is an author, or separation not held | Recorded honestly (`not_separate`, `reported_as_independent: false`); a valid record that is not independent | EXP-R6 only if reported as independent |
| F-7 | Model identity not exposed | `not_exposed`; no family claim | EXP-R6 |
| F-8 | Supplier verification refused (HOSTING §7.2 mismatch or unverifiable) | Case `blocked` by supplier verification; the unverified supplier is never examined as the pinned one | `blocked_by` |
| F-9 | Date source uncertain | Record the date with its source; `stated_by_person` when only stated | `date.source` |
| F-10 | Criterion text changed since examined | §6.3: not a repair unless a disposition is cited | `criterion.identity` differs |
| F-11 | Record fails schema or EXP rules | Not relied on until repaired; the run's evidence is kept | Prototype check |
| F-12 | A chat statement, tool success, silence or timeout offered as a human act | Not cited as an act (REQ-003) | EXP-R5 and the journey's own act rules |

## 12. Verification (designed; VER-001…VER-009)

"Needs": *model* = runs on `prototype/check_exp.py` now; *candidate* = an App
build; *person* = an actual act or person-operated step; *package* = M2.
A *model* result passes no VER criterion.

| Case | Serves | Setup and action | Expected | Needs | Prototype 2026-10-03 |
|---|---|---|---|---|---|
| EXP-VC-01 Fixture inventory | VER-001, AC-001 | Inspect each journey's fixture list against FX-1, FX-6 | Invented material; origin, pin, standing, digest present; admission input named for any research fixture | Journey fixture lists | Not run |
| EXP-VC-02 Replay and live marking | VER-002, AC-002 | Replay a recorded exchange (HOSTING §9.4 X-01 side) on the double at each pin | Rehearsal record, `seam_replay`, `recorded`; a missing recording at the other pin is `not-run` with its input | model; recordings | Examples EXP-EX-02 (0.158.0) and EXP-EX-03 (0.160.0) valid |
| EXP-VC-03 Capture of all five outcomes | VER-003, AC-003 | Records for each outcome, incl. missing-input and inconclusive | Schema enforces reasons; EXP-R1 aggregation | model | Valid and invalid sets pass; EXP-R1 detected (EXP-RV-01) |
| EXP-VC-04 Human acts: positive and negatives | VER-004, AC-004 | A record citing an actually performed act; attempts with actor = recorder | Actor ≠ recorder; the negative detected; no act manufactured for a fixture | model; **person** for the positive case | EXP-R5 detected (EXP-RV-03); positive case not run |
| EXP-VC-05 Reopening | VER-005, AC-005 | Pin change 0.158.0 → 0.160.0 over a replay result | Prior result `historical` citing the change; rerun at new pin | model; then candidate | EXP-EX-CI-01 valid; EXP-R8 detected (EXP-CIR-01) |
| EXP-VC-06 Protected criterion | VER-006, AC-006 | A failure, then a rerun with a changed criterion identity, with and without a disposition | Without a disposition it is not a repair; with one, both standings kept | model | Change-impact schema rejects a criterion disposition without its decision (EXP-CII-01) |
| EXP-VC-07 Review record | VER-007, AC-007 | Codex reviewer; Claude fallback with reason; honest not-separate review; additional person review; reviewer = author reported as independent; unexposed family claim; reviewer kind outside V4-OPS-34 | Preference and fallback reported; honest non-separation valid; EXP-R6/R7 enforced | model; then a real review | EXP-RX-01…04 valid; EXP-RXI-04 (`other`), -05, -06 rejected; EXP-R6 ×3, EXP-R7 detected |
| EXP-VC-08 Routes | VER-008, AC-008 | WebKit and Chromium interface runs; native development and packaged smoke | Engine/platform/runner check on interface routes; WKWebView identity on native routes; native part fails EXP-R4 on browser evidence; a packaged pass without a package is refused | model; candidate; **package** | EXP-EX-07 valid; EXP-INV-09 (RV P1), -12, -13, -14 rejected; EXP-R4 detected (EXP-RV-02); EXP-EX-04 `not-run` (no package) |
| EXP-VC-09 Boundary and open matters | VER-009, AC-009 | Review §1, §2 and §14 against the rows and CLM-005/006 | Each excluded act has its owner; open matters with owner and point of need | Review | Not run (review) |
| EXP-VC-10 Vocabulary mapping | REQ-002; R23-1 | Compare EXP outcome and fixture labels with HOSTING §9.2/§9.3 and with the W14/XT enums | Equal to HOSTING; one-to-one onto W14/XT | model | EXP-R9: 4 checks pass |
| EXP-VC-11 Scenario evidence basis | REQ-002, REQ-007 | A definition check carrying a scenario, with a `fail` | Refused | model | EXP-INV-10 (RV P2) rejected by the schema |
| EXP-VC-12 M1–M3 | SCC-003 R1 | A package witness and a smoke result citing M1 and M2 | Both identities cited; changes reopen only their citers | candidate; package | Not run |
| EXP-VC-13 Parts that do not apply | R23-19 | Four parts pass and one is declared not applicable before the run; one part both declared and run; an applicable part not run | `pass`; the double listing and the hidden `not-run` are detected; a declaration without its case definition is refused | model | EXP-EX-08 `pass`; EXP-R1 detected (EXP-RV-04, -05); EXP-INV-15 rejected |
| EXP-VC-14 Blocked versus not-run | R23-20 | `blocked` without a stated cause; a packaged case with no package | Refused; recorded `not-run` with the package as missing input | model | EXP-INV-11 rejected; EXP-EX-04 valid |
| EXP-VC-15 Runner and N-2 tool admission | R23-17 item 3; §8.3 | EXP-DC-RUNNER on a runner version; EXP-DC-N2 on a candidate | DC-R1…R5, DC-N1…N5 pass before results count | model for the record form; candidate | EXP-EX-06 (illustrative DC record) valid; checks not run |

**Prototype run** (`PYTHONDONTWRITEBYTECODE=1 python3 check_exp.py` in
`prototype/`, Python 3 with `jsonschema` 4.26.0, Draft 2020-12, no network,
writes nothing), 2026-10-03, at EXP-v0.2: **TOTAL 77, FAIL 0**. It checks
that the three schemas are valid 2020-12 schemas; that 12 valid records
pass and break no rule; that 24 invalid records fail their schemas; that 10
schema-valid rule-violation records are each caught by the named rule
(EXP-R1 ×3, R4, R5, R6 ×3, R7, R8); the EXP-R9 vocabulary checks read from
the actual HOSTING, W14 and XT files; that §3.5 lists EXP-R1…R9 once each;
and that examples exist at both pins. RV's scratch probes P1–P7
(`reviews/RV-EXP-U1.md`) were rerun against the repaired files: P1, P2, P5
and P6 are now refused; P4 and P3 behave as R23-19/RV EXP-R-F intend (see
the O-B reply). It establishes structural validity and that the rules run as
written; it says nothing about a candidate.

## 13. UNRESOLVED

| ID | Item | Owner | Point of need | Effect here |
|---|---|---|---|---|
| U-EXP-1 | Qualification Codex pin (OI-012) | **Closed by rule (R23-22):** 0.158.0 stays the definition and generation pin (D4); 0.160.0 is checked and design-compatible; the qualification pin is the newest version that has passed a version-advance check when a candidate is built. No owner decision is needed unless a check finds a changed relied-on behaviour | When a candidate is built | Records carry the pin; a pin change is a change of kind `codex_pin` (§6.2) |
| U-EXP-2 | Interface runner and N-2 tool names and versions | The implementer chooses them against §8.3's definition checks; recorded as facts of the result (R23-17 item 3) | Before the first interface or N-2 run | Not a design gap: the admission criterion is §8.3 |
| U-EXP-5 | M2 package and DEL-01-06's signing arrangement | DEL-01-06 (R23-13) | Before native packaged smoke | `native_packaged` cases `not-run` (AWAITING INPUT) until then |
| U-EXP-6 | OI-016 validation period and activities | Owner | Before validation in use | `validation` records only on actual use |
| U-EXP-7 | OI-003, OI-021, OI-023/026 | As in ScopeOfWork TBD-001 | Their journeys' points of need | None here |

Closed at v0.2: **U-EXP-3** (placement and form layout: decided, §8.2,
§8.4; R23-17 item 4); **U-EXP-4** (digest: sha256, R23-17 item 1; the
schema now requires `sha256:` digests for criteria and declarations).

## 14. Observations for other owners (no file of theirs is changed)

- **O-1 (register statement; for the next amendment, R23-11).**
  DEP-09-01-019 names only the selected pin; R23-1 relies on HOSTING §9's
  labels and capture method over the same admitted arc. Suggested
  Statement addition: "…and HOSTING's fixture standing labels, outcome
  labels and capture/redaction method, which DEL-09-01's examination record
  maps to". No new arc (the arc DEL-09-01 → DEL-01-01 is admitted); no
  reach change.
- **O-2 (W14 and XT, R23-1: no restructure).** Neither schema has fields for
  harness version, model version or model server; W14 relies on its W14-00
  identification record and `model_destination`, XT likewise. The mapping in
  §3 stands; whether those journeys want explicit fields is theirs.
- **O-3 (HOSTING, its own authority).** HOSTING §9.3 spells `not-run`;
  W14/XT spell `not_run`. This file uses HOSTING's spelling and maps.
- **O-4 (no row proposed).** EXP cites AAC (DEL-01-04) and RS (DEL-04-03)
  only as cross-references; a reliance row DEL-09-01 → DEL-01-04 or →
  DEL-04-03 would close a cycle through held arcs (DAG-004, both layers), so
  none is proposed.

## Changes

| Version | Change |
|---|---|
| EXP-v0.1 (2026-10-03) | First Design file: protocol, three PROPOSED schemas with example sets, prototype check (52/0) |
| EXP-v0.2 (2026-10-03) | Repair for RV-EXP-U1. EXP-R-A: not-applicable parts declared before the run, listed apart, out of aggregation (R23-19; §3.1, schema `parts_not_applicable`). EXP-R-B: `blocked`/`not-run` per R23-20, labelled INTEGRATION; every planned case gets a record; `blocked` requires its cause (§3.1, §6.1, F-1a/b). EXP-R-C: a `native_packaged` result other than `not-run` needs a packaged candidate with its record (schema; EXP-INV-09 = RV P1). EXP-R-D: definition checks EXP-DC-RUNNER and EXP-DC-N2 given content (§8.3); placement and form layout decided (§8.2, §8.4); U-EXP-1/2/4 restated per R23-17; digests sha256. EXP-R-E: one rule table EXP-R1…R9 with EXP-R2 defined (§3.5). EXP-R-F: `reported_as_independent`; honest non-separation valid. EXP-R-G: `other` removed; `additional_person` review kind. EXP-R-H: no scenario on non-candidate bases (schema). EXP-R-I: held arcs place no case in HELD; packaged smoke AWAITING INPUT for the package. EXP-R-J: AAC pin kept at AAC-v0.2, the version relied on, with v0.3's effect checked (R23-21 item 3); rulings cited by ID (R23-21 item 1). EXP-R-K: WKWebView identity on native routes. Prototype 77/0 |
| EXP-v0.2, in place (2026-10-03) | After RV's confirmation (READY): U-EXP-1 closed under R23-22 (§13). No rule, schema or example changed |
