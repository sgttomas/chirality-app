# Research to design candidate: method, act requirements and later witness

- **Contribution:** DEL-08-02/RTD-v0.1 (new; **frozen** 2026-10-04, after
  RV2 confirmed EU-D1 READY at `25054b04df`). Owner O-D, run
  `APP-V4-DESIGN-PASS-4-20261003`. Drafted in parallel with EU-D1 (R23-34
  item 10). Serves:
  - OUT-001: the method and the contribution account (§2, §3, §6);
  - OUT-002: the receiving integration, act requirements and host handoff
    (§4, §7);
  - OUT-003: the V4-EXM-32 witness design (§8).
- **Status:** PROPOSED. The later Domains-enabled increment is not started.
  Starting it is the person's act at its point of need (R23-34 preamble).
  No provider, admitted source, research workflow, host integration or
  approval route exists.
- **Basis:**
  - ScopeOfWork sha256 `43a769703f235b2605ec176c6c7e42c934b8980fa48148e434c27a42a3632006`
    (INIT; no SCA revision); Dependencies.csv `18b0ab8b79e9faac97161c92f0441197f9f609342c5beb5aa0e241b1158b88de`.
  - Accepted basis: PRD V4-CON-01, -04, -05, §3.1 (V4-EXT-01), V4-AUT-01…05,
    V4-ROLE-03; HOST V4-HI-25, -30…33, -60, -64, -65, §8.1; EXAMINATION
    V4-EXM-31, -32; OPERATING_METHOD §6.
  - Owner decisions: FIRST-INCREMENT DECISION-1 D2/D3; DECISION-3 (host
    joins deferred); DECISION-4 (Phase 1: checkpoints are plan guidance).
  - Rulings: R23-34 items 4, 5, 6, 8; R23-27 (declared stimuli); R23-19,
    R23-20.
- **Suppliers read:**
  - ACT-POLICY-v0.10 §2.1, including the alias exclusion "Design-candidate
    approval … is a separate act in a later increment. It is **not** A6", and
    F-2;
  - RS-v0.10 OF-1…OF-9 and L-rules;
  - WD-v0.9 §4.2.1 and §4.3.1 ("design-candidate approval … is a separate
    later-increment act and cannot be required here");
  - DRC-v0.1 (DEL-08-01) and CFB-v0.2 (DEL-07-02), at the hashes in
    `OWNERS/O-D.md`.
- **Schema:** `research.context-account.schema.json` (PROPOSED).
- **Check:** `prototype/check_rtd.py`. It consumes EU-D1's frozen Domains
  receiving records (`RUN/D/evidence/records/DR-DM-1.json`, `DR-DM-2.json`)
  and DEL-07-02's standing schema, read-only.

## 1. Boundary (REQ-007)

This file defines the App/shared contribution to the later activity: SWBPIPE's
agent queries Domains through a research workflow, builds context and produces
a design candidate for the person's decision. It does not:
- produce DEL-08-01's query/admission contract;
- produce PKG-02's portable method format or PKG-04's act records;
- implement anything in SWBPIPE;
- relay to the outside session;
- allocate a provider;
- perform or presume the person's decision.

The SWB Piping Designer is an application expression using the four standing
roles (CLM-001; V4-ROLE-03). No fifth role and no knowledge-browser UI are
designed.

## 2. Method model (REQ-001, REQ-002)

| Step | What happens | Owner | Evidence it leaves |
|---|---|---|---|
| M-1 Question | The research question and intended use are stated | Agent, from the person's request | The request (run record) |
| M-2 Query | The agent calls the Domains query tool | Agent; tool owned by the provider (OI-026) | DEL-08-01 receiving records (`dr:`) with standing |
| M-3 Evidence | Each result is classed by its standing: admitted evidence, located only, or limited | Agent, by DRC §4 rules | Context account `evidence[]` |
| M-4 Inference and gaps | Inferences name the evidence they rest on; gaps name what is missing and its effect | Agent | Context account `inferences[]`, `gaps[]` |
| M-5 Candidate | The host creates or changes a candidate design; its content identity is the host's | Agent through host operations; host owns the identity | Host receipt; context account `candidate` |
| M-6 Request | The agent asks the person for the candidate decision (A8 request) | Agent | A8 record |
| M-7 Decision | The person decides on the candidate (§4) | The person, through the host's facility | Human-act record, once the shared row exists |
| M-8 Apply / rely (separate) | Applying an edit (A2), accepting a proposal (A5), engineering approval (A6), checking (A4), reliance (A7) | Each its own actor | Each its own record; none follows from M-7 |

Rules (checked by `prototype/check_rtd.py`):
- **RC-1 Supported.** A context account is `supported` only if every evidence
  item the candidate ultimately rests on (through its inferences) is
  admitted evidence (CS-R1; Domains' reliable tier is `admitted`).
- **RC-2 Limited.** An account whose candidate rests on any located-only or
  limited item is `limited`, and it names the limit (in the inference's
  `limits` or in `gaps`).
- **RC-3 References resolve.** Every inference's `from` and the candidate's
  `rests_on` name evidence or inferences in the same account.
- **RC-4 Use follows standing.** Each evidence item's `use` is the one its
  cited receiving-record result's standing allows: reliance gives
  `admitted_evidence`; a located-not-admitted hit gives `located_only`;
  anything else gives `limited`. A stale admitted source is `limited`.
- **RC-5 A decidable candidate has an identity.** A candidate offered for the
  person's decision carries the host's content identity (§4 CA-2).
- **RC-6 Held.** When Domains is absent or the needed sources are
  unavailable or unsuitable, the account is `held`: no candidate is
  produced from it, and the gap is named (schema). Independent work
  continues (V4-CON-03; REQ-002). Nothing fabricates context in place of a
  missing input (HOST §8.1).
- The account and the candidate each carry their own identity, and the
  decision binds both (§4 CA-2).

## 3. Research context account (`research.context-account.schema.json`)

Elements: question; the receiving records used; evidence items with source,
revision, statement and use; inferences with what they rest on; gaps with
effect and who is responsible; the candidate reference and the host's content
identity; account standing (`supported`, `limited`, `held`); the recorder. The
account lives with the host project, as host-agent run records do (RS OF-9).
Its placement is not chosen here.

## 4. Candidate decision: requirements (PROPOSED definition; R23-34 item 4)

These are requirements on an act that does not yet exist in the shared
vocabulary. **No row is added to ACT, RS, CE or GUIDE now.** The shared rows
are added when the Domains-enabled increment is selected. WD §4.3.1 already
excludes this act from checkpoints for now.

| ID | Requirement | Source |
|---|---|---|
| CA-1 | The decision actor is the person. No agent, host or App performs it | V4-CON-05 "for the human to approve"; V4-HI-65; ACT §2.1 S3 |
| CA-2 | Subject: one candidate, bound by the host's content identity, together with the research context account (`rc:`) it was presented with, bound by that account's content identity. Without a host content identity there is nothing to bind, and the decision cannot be recorded as applying to it | V4-HI-65; RS OF-3; SWBPIPE SQ-03 (whole-model hash only, today) |
| CA-3 | Scope and purpose as the request (A8) states them | V4-AUT-03 |
| CA-4 | A decision pair: approve or decline. Silence, timeout, an agent's statement, tool success or a host receipt is not a decision | ACT §2.3; V4-AUT-03; REQ-005 |
| CA-5 | Evidence: capture by the host facility that presented the candidate, recorded by a faithful recorder distinct from the actor | V4-HI-31; RS OF-1, OF-8 |
| CA-6 | Lapse: a change to the candidate's content, or to the account it was decided with, ends the earlier decision's applicability. The record keeps it as lapsed; a new decision is needed | REQ-005 "changed content visibly invalidates"; RS L-rules |
| CA-7 | It establishes none of: application (A2), acceptance of edits (A5), engineering approval (A6), checking (A4), professional reliance (A7). None of those is a prerequisite for it | V4-CON-05; V4-HI-65; ACT §2 rule |
| CA-8 | Whether a host reserves it beyond CA-1 (its own list) is the host's operation-specific addition | D2 (OI-021); R23-34 preamble |
| CA-9 | Phase 1: a workflow may describe the step in prose; the agent asks; the act is recorded only when performed; no hold is enforced | DECISION-4 D4-1; WD §4.3.0 |

## 5. Declared-part sketch for the research workflow (WD form; not a registered workflow)

| Category | Content | Notes |
|---|---|---|
| Expected inputs | Research question (`person_supplied`); design basis (`host_read`, five-element read basis); admitted Domains query capability (necessity: required; absence effect: research `held`) | — |
| Required tools | Host operations for candidate creation: *host operation requirement* (opaque catalog identity); the Domains query tool | SWBPIPE has no catalog: such references are *not established* (WD R8-10 note). The Domains tool's class is a question for the Domains-enabled increment (R23-34 item 5; DRC §7) |
| Checkpoints | **None declarable now.** WD §4.3.1 excludes candidate approval from the closed list. The approval step is in prose (CA-9) | Becomes declarable when the shared row is added |
| Returned outputs | Context account; candidate reference | — |
| Returned evidence | Receiving records; host receipts; the decision record when one exists | — |

The workflow itself is authored later, under Root's `create-workflow`. Its
registration (A15) is the person's act at that time.

## 6. Contributions and points of need (REQ-003; HOST §8.1)

| Contribution | Owner, as the files state | Point of need | Standing now |
|---|---|---|---|
| Domain database and admitted sources | Provider owner TBD (OI-026) | Before research-context reliance | None |
| Query tool and its contract | Provider and receiving tool-contract owners; App side in DRC-v0.1 | Before dependent implementation | App side proposed (DRC) |
| Research workflow (method) | App/shared method owner (this file) with the host | Before the research-to-candidate increment | Method proposed here; workflow not authored |
| Host use, candidate presentation, approval route | External SWBPIPE owner, with the person | Before the connected host witness | Deferred (DECISION-3) |
| The decision itself | The person | When a candidate is presented | — |
| Starting the increment | The person (R23-34 preamble) | — | Not started |

PEC plays no part. Domains joins a later increment and is not an initial D05
prerequisite (CLM-002).

## 7. Host handoff (REQ-004; prepared, not relayed)

These are prepared for the next relay when the owner resumes the host joins
(DECISION-3). They are not sent, and a written question is not an agreement
(OPS §6).

| ID | Question for SWBPIPE | Why |
|---|---|---|
| HQ-1 | How would the agent reach a Domains query tool: catalog entry with an external-contact declaration, stateless MCP server, or in-process? | V4-HOST-02 compatibility (DRC §6) |
| HQ-2 | What content identity can a candidate carry: whole-model hash, per-object identity, revision? | CA-2 binding |
| HQ-3 | Which host facility would present the candidate and capture the person's decision, and what evidence reference would it give? | CA-5 |
| HQ-4 | How is DEC-051 open residency reconciled with V4-HOST-02 for research traffic? | DRC §6 |
| HQ-5 | Does SWBPIPE expect to reserve the candidate decision on its own list? | CA-8 (OI-021) |
| HQ-6 | Where would the context account live with the host project? | §3 |

## 8. V4-EXM-32 witness design (OUT-003; REQ-006)

| Part | Expectation | Declared stimulus (R23-27) |
|---|---|---|
| RD-1 Path | Query → evidence with standing → inferences and gaps → candidate identity → request → the person's actual decision with scope | — |
| RD-2 Unavailable input | Account `held`; no candidate from it; independent work continues | ST-D1 Domains unavailable |
| RD-3 Unsuitable input | A located-only result is not used as admitted evidence; the account is `limited` and names it | ST-D2 an unadmitted hit |
| RD-4 Stale input | An admitted source revised since indexing is `limited` | ST-D3 a source revised after indexing |
| RD-5 Not an act | No decision is recorded from an agent's "approved", from tool success or from silence | ST-D4 the agent claims approval; ST-D5 the request left unanswered |
| RD-6 Lapse | Changing the candidate after a decision lapses it | ST-D6 a candidate edit after the decision |

- A completed live witness needs every HOST §8.1 input and an actual decision
  by the person. A favourable decision is not required (REQ-006).
- Until the inputs exist, parts that need them are `not-run`, with missing
  inputs named (R23-20). Negative and partial evidence is kept, and never
  counts as completion.
- A rehearsal of RD-2…RD-4 can reuse EU-D1's Domains cases (DM-1, DM-2) as
  `rehearsal` records (EXP-R3: they stand for no scenario).

## 9. Interfaces

| Direction | With | What | Arc (DAG-004) |
|---|---|---|---|
| Consumed | DEL-08-01 (DEP-08-02-005) | Query, admission and freshness meanings; receiving records | admitted |
| Consumed | DEL-02-01 (DEP-08-02-006) | Portable method meanings (WD §3, §4) | admitted |
| Consumed | PKG-04 (DEP-08-02-007) | Distinct act identities (ACT, RS) | not topological |
| Handover | SWBPIPE owner via the person (DEP-08-02-011) | §7 | not topological |

- No register row is proposed. Rows to DEL-04-01 or DEL-04-03 would form no
  cycle (reach checked in S2-D F-3), but H-4 adds no row now.
- DEL-04-01 must never consume this deliverable: that row would close a
  cycle.

## 10. Carried to the next amendment (R23-34 item 8; R23-11)

CLM-006, TBD-003, the last sentence of REQ-005, AC-006 and VER-005 say OI-001
and OI-002 "remain OPEN". D2/D3 ruled them for the App/shared contracts. The
residue is OI-021 (host operation-specific additions) and DEP-001 (host
adoption). This file follows the current decisions (R23-7).

## 11. Verification design (VER-001…005)

| VER | Design |
|---|---|
| VER-001 | Trace a context account from receiving records through evidence, inferences and gaps to the candidate. RC-1…RC-6 are checked by `prototype/check_rtd.py`, over EU-D1's frozen Domains records (DM-1, DM-2): 18/18 at freeze |
| VER-002 | Inspect §6 and §7 against HOST §8.1, OPS §6 and DEP-003; the owners as stated; no smuggled UI, provider or host choice |
| VER-003 | §8 RD-1 on joined candidates (later) |
| VER-004 | §8 RD-2…RD-4; rehearsal on EU-D1's Domains cases. At freeze, `check_rtd.py`'s RCA-1 (from DM-1: stale and unadmitted → `limited`) and RCA-2 (from DM-2: absent → `held`) rehearse RD-2…RD-4's account rules; the live parts need the inputs in §6 |
| VER-005 | §8 RD-5, RD-6 against §4's requirements, once the act's shared rows exist |

## 12. Open

| Matter | Owner | Point of need |
|---|---|---|
| Shared rows for the candidate decision (ACT, RS, CE, GUIDE, WD closed list) | DEL-04-01, DEL-04-03, DEL-02-03, DEL-03-04, DEL-02-01 owners | When the Domains-enabled increment is selected |
| Domains tool class in workflow declarations | Domains-enabled increment (R23-34 item 5) | Before the research workflow is declared |
| Answers to HQ-1…HQ-6 | SWBPIPE owner via the person | When host joins resume |
