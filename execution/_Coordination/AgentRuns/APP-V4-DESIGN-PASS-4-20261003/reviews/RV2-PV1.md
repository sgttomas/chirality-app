# RV2-PV1: review of EU-F4, DEL-09-12 PV-v0.2 (practitioner validation and feedback disposition)

- **Reviewer.** RV2 (Type 2 TASK), Claude Opus 5.5 (`claude-opus-5-5`). Run `APP-V4-DESIGN-PASS-4-20261003`, 2026-10-04. Method: `coordinated-knowledge-work` §3.
- **Unit.** Owner O-F, committed at `0e3591a65d` on `claude/app-v4-design-pass-4-t2`.
  - The working tree equals the commit for DEL-09-12 `Design/` and `F/pv/`.
  - `git status --short --ignored` on those paths prints nothing.
  - All seven hashes in `OWNERS/O-F.md` "EU-F4 — refrozen" match:

    | File | sha256 (prefix) |
    |---|---|
    | `PRACTITIONER_VALIDATION.md` | `2240ab36…` |
    | schema | `2b7c2b9e…` |
    | valid examples | `82ab49ae…` |
    | invalid examples | `c15ccd26…` |
    | `pvlib.py` | `fc82093c…` |
    | `check_pv.py` | `628e63d3…` |
    | records manifest | `32256269…` |

- **Basis read.**
  - DEL-09-12 ScopeOfWork (`40eaf09f…`, matches the pin): OUT, CLM, REQ, AC, VER and TBD, all read.
  - R23-32 and R23-33.
  - S2-F §§ F-R12…F-R14.
  - EXP-v0.2 `candidate_subject` and its §3.3 lines.
  - DEL-10-02 UC §5 and §9 (`da0176cb…`).
  - DEL-11-03's first-cut `$defs/practitioner_standing` (current `rp.packet-manifest.schema.json`).
  - The DAG-004 edge files.

## Verdict: **REPAIR**

There is no BLOCKING finding. There is **1 MAJOR**, and there are **5 MINOR** and **2 NOTE**.

### What holds

- **No overstated evidence.**
  - The real records (PV-ARR-1, PV-STANDING-1) state `not_agreed`, no agreement, no period, no activity, both expressions `blocked` with causes, 0 observations and `is_replacement_condition: false`.
  - The builder stops if OI-016 (App v4) or OI-021 closes, or if DECISION-3's text is gone.
  - Every example carries ILLUSTRATIVE or INVENTED in its candidate, agreement, statements or limits.
  - Observations have `standing: illustrative`.
  - Nothing claims a practitioner observation, agreement or disposition.
- **Agreement act boundary.** The agreement is the owner's act in OWNER_DECISIONS form: actor const "the owner", recorder not "the owner", record and custody required. A plan is never an agreement (schema; invalid 3, 4; N-1).
- **Records.** The observation record has no outcome or score (F-R12). "Not observed" carries no statements.
- **F-R13 routing.** Routing reads the real ScopeLedger at the commit, and an unknown anchor gives `unresolved` (K-10).
- **F-R14.** It holds in every Design file and record.
- **Method note.** It carries exactly UC §5's fields, and UC §9 says it receives them so (K-11).
- **Interfaces.** The DAG-004 standings in §2 are right:
  - DEP-09-12-011, DEP-09-12-012, DEP-09-01-029 and DEP-11-03-009 are admitted;
  - DEP-09-12-007, -008, -009, -010 and -013 are not topological.
- **Checker.** It reruns at **27/27**.
  - Each schema-refused invalid example fails its own `$def` for the reason its `why` names. I printed each.
  - The four rule cases (11…14) pass the schema and fail only their rule.
- **Scope.** The checker is sized to the design question: two files, 339 lines, K-1…K-13 and N-1…N-14, and no machinery beyond the records, the rules and their negatives.

### What fails

The **disposition** record does not hold the act boundary that OUT-003, REQ-003 and REQ-004 require. Three claimed design rules can be broken by records that still pass `check_pv`, and O-F's list of uncovered rules does not name them.

## Findings

### PV1-R1 — MAJOR: a disposition's decision has no recorder and no decider rule, and a successor-basis proposal can be recorded as decided (§3.3; schema `$defs/disposition.decision`; REQ-003, REQ-004, AC-003, AC-004)

**Evidence.**
- The schema's `decision` allows only `state`, `actor`, `record_ref` and `scope`. `actor` is any string, and there is no recorder field.
- §3.3 says the successor-basis treatment is "kept proposed until its own decision and adoption". REQ-004 says "Keep proposed successor-basis changes proposed until their actual decision and adoption evidence exists", and "who decided what". AC-003 requires "faithful transcription with separate recorder attribution".
- Probe E (`$TMPDIR/rv2/probe_pv.py`): a disposition with `proposed_treatment: successor_basis_proposal` and `decision: {state: decided, actor: "O-F (agent)", record_ref: "chat line", scope: "v5.0 basis"}` **passes the schema and PV-R1…R3**.
- §8's list of rules without a negative case does not mention this, and neither does O-F.md's.

**Consequence.**
- The record cannot distinguish the decider from whoever wrote the line down.
- It lets an agent's string stand as the decision on a requirement, method or v5.0 basis.
- It shows a successor-basis proposal as decided on a single reference with no adoption evidence.

These are the confusions REQ-003 forbids:
- the disposition (DEL-09-12's routing act);
- the owning deliverable's or the owner's decision (CLM-003; UC §7, "where the owner decides"; OI-020/P-6 for a manual);
- the adoption.

**Repair.**
- Give `decision` a `recorder`, with recorder ≠ actor or `recorder_stated_by_record`, as the agreement has.
- Require the decision's `record_ref` and `actor` to name the decider the kind requires:
  - feature or workflow: the owning deliverable's record;
  - method: the DEL-10-02 stage decision (UC §7), with the owner as actor where UC says so.
- For `successor_basis_proposal`, refuse `decided` unless separate decision **and** adoption references exist. Or keep it `proposed` by schema, and record the later decision and adoption as their own acts.
- Add the negative cases, and list any part left to review in §8.

### PV1-R2 — MINOR: "always two, `app` and `swbpipe`" is not enforced (§3.1; schema `expressions`)

**Evidence.**
- §3.1 says "There are always two, `app` and `swbpipe`". The schema has `minItems: 2, maxItems: 2` and no uniqueness rule.
- Probe A: an agreed arrangement with two `app` expressions and no `swbpipe` passes the schema and PV-R2.
- This is not in §8's list of uncovered rules, nor in O-F.md's.

**Repair.** Add a `contains` rule for each expression, or a rule over `expression` values. Add a negative case.

### PV1-R3 — MINOR: no rule ties an observation, or an agreed arrangement, to what makes it validation (§3.1 "Nothing before `agreed` counts as validation"; AC-001; REQ-001)

**Probes, each of which passes the schema and PV-R1…R3:**
- **C:** an `actual_use` observation with an identified-looking candidate (`abc123`/`build-7`), whose `arrangement_ref` is the real `PV-ARR-1 v1` (`not_agreed`) and whose `activity_id` is in no arrangement.
- **B:** an agreed arrangement whose available expression has `candidate: null` and `material: null`. AC-001 requires "identified candidates" and "eligible material".
- **H:** a standing `in_use` with `agreement_ref: null`.

**Consequence.**
- The standing's "0 observations while not agreed" (schema; N-3) guards only the hand-over.
- An observation record can claim actual use under no agreement, on an unselected activity, or on a candidate other than the arrangement's.

**Repair.** Add one cross-record rule (PV-R4) over an observation and its arrangement:
- the arrangement is `agreed` or `in_use`;
- the activity is owner-selected for that expression;
- the candidate equals that expression's candidate.

Also require, for an agreed arrangement:
- an identified candidate and material on every `available` expression;
- `agreement_ref` whenever the standing is past `not_agreed`.

Alternatively, list these in §8 as not enforced.

### PV1-R4 — MINOR: the SWBPIPE expression records an App candidate shape where the supplier gives a host candidate (§3.1, §3.2; I-2, I-4; R23-33)

**Evidence.**
- Both expressions' `candidate` is EXP `candidate_subject.app_candidate` (`revision`, `build_identity`).
- EXP-v0.2 keeps the host as a separate `host_candidate` string ("Joined witnesses only"). R23-33 makes EXP's identity canonical for the **App** candidate.
- §2 I-2 names DEL-09-07 and SWBPIPE as the host candidate's suppliers.
- In the observation, `configuration.host_candidate` is optional even when `expression` is `swbpipe`.

**Consequence.** A SWBPIPE session can be recorded without the host candidate it ran on, or with the host's identity forced into the App's fields.

**Repair.**
- For `swbpipe`, carry both the App candidate (EXP `app_candidate`, or null) and the host candidate (EXP `host_candidate` / the LHQ CIR reference).
- Require `host_candidate` on `swbpipe` observations.

### PV1-R5 — MINOR: "carried identically" to DEL-11-03 overstates; the hand-over changes a field's type (§2 O-3; K-12)

**Evidence.**
- §2 says "The values the first cut reads (open issue, standing, no agreement and no observation while not agreed) are carried identically (`check_pv.py` K-12)".
- The first cut's `observations` is an **array** (`maxItems: 0` while not agreed). PV's is an **integer** count (`const: 0`).
- `format` also differs (`RP-v0.1-first-cut` vs `PV-v0.1`).
- K-12 checks only `open_issue` and the `standing` enum.

**Consequence.** RP's adoption (U-PV-3, carried, not a finding here) will meet a type change the claim does not mention.

**Repair.** State the shape change in O-3, and have K-12 compare against the first-cut `$def`'s required fields and types, or say that it does not.

### PV1-R6 — MINOR: "owner" names agents (header; §7)

**Evidence.**
- The header reads "owner O-F (Type 2, Claude Opus 5.5)".
- §7's "Owner" column assigns U-PV-2 to DEL-09-02 and DEL-09-07, U-PV-3 to O-F, and U-PV-4 to O-B. Elsewhere in the same table, "The owner" is the person (U-PV-1, U-PV-5).
- In this file "the owner" is otherwise the person throughout (OI-016's "Owner", P-2, P-3, the agreement actor, the observer const).

**Repair.**
- Use "agent owner O-F" or "assigned to" for agents and deliverables.
- Keep "owner" for the person.
- "Feature owners" is the ScopeOfWork's own term (CLM-003) and can stay, but should not be shortened to "owner".

### PV1-R7 — NOTE: wording slips in the evidence lists

- §8's VER table cites the invalid examples loosely:
  - VER-002 "(invalid 1, 2, 9; PV-R1)", where PV-R1 is invalid 11;
  - VER-004 "(invalid 5, 6; PV-R3 ×2)", where PV-R3 is invalid 13 and 14.

  The "without a negative case" list in §8 has the right numbers.
- Valid example 2 (the agreed arrangement) carries the limit "illustrative example of a proposal; not an agreement". That text was copied from example 1.
- `pvlib.py`'s docstring says "rules PV-R1..PV-R4" and "PV-v0.1". There is no PV-R4.
- `check_pv` K-6 checks schema refusals against the top-level `oneOf` only. Each one does fail its own `$def` for its named reason; I checked by `def_errors`.
- N-2's mutated arrangement is also schema-invalid (`agreement` uses `by`; the activity has no `activity_id`), so it shows only that PV-R2's function fires. Invalid example 12 shows PV-R2 on a schema-valid record.

### PV1-R8 — NOTE: EXP and PV still read the validation activity differently

- EXP-v0.2 says DEL-09-12 "Records `activity: validation` only for an actual practitioner's use (§3.3)" (line 116; U-EXP-6).
- PV does not use it (F-R12; U-PV-4, a note for O-B).
- This is consistent with R23-32 F-R12. EXP's next revision should say that DEL-09-12 keeps its own record, so the two files stop disagreeing.

## What I checked and how

- **Rerun, not rebuilt.** `python3 -B check_pv.py` gave **27/27**. No `__pycache__` was left.
- **Refusal reasons.** I ran each invalid example against its kind's `$def`, using `check_pv.def_errors`, and printed the messages:
  - 1 and 2: extra `outcome` and `score`;
  - 3: no agreement object;
  - 4: recorder equals actor;
  - 5: `record_ref` and `scope` missing;
  - 6: method not to DEL-10-02;
  - 7: `False` expected;
  - 8: `0` expected;
  - 9: not-observed with items;
  - 10: unqualified issue;
  - 11…14: schema-clean.
- **Probes.** `$TMPDIR/rv2/probe_pv.py` (A, B, C, D, E, G, H) imports `pvlib` and the schema unchanged.
  - D (a `TBD` placeholder) passes, which matches the disclosed keyword limit.
  - G (recorder "The owner") passes, which matches the disclosed string comparison.
- **O-F.md's list of claimed rules without a negative case is truthful for what it names.** It names:
  - PV-R1 and PV-R3 on examples only;
  - the keyword placeholder test;
  - the string recorder test;
  - the act boundary by review.

  It **omits** the three claims probes A, C and E break (PV1-R1…R3).
- **Interfaces against the supplier and receiver text.**
  - EXP `candidate_subject` (PV1-R4).
  - UC §5's field table and §9.
  - RP's first-cut `practitioner_standing` (PV1-R5).
  - The ScopeLedger rows for V4-EXE-01 (three IN rows, DEL-01-02).
  - The DAG-004 edges.
- **Not done.**
  - I did not rebuild the records (K-3 already does, at the recorded commit).
  - I did not review DEL-11-03's adoption (U-PV-3, carried by direction).
  - No network, no git writes, and no edits to O-F's files.
