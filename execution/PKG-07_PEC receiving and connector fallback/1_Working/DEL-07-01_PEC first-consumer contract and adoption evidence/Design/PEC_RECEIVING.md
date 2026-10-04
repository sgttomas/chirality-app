# PEC first-consumer receiving contract

- **Contribution:** DEL-07-01/PRC-v0.2. It supersedes PRC-v0.1 (sha256
  `1a8acc8593dfb5c27faa63e5306cf636717aa07a552b68115336de349ecb379d`, the
  EU-D1 freeze RV2 reviewed), repaired for RV2-EUD1 (R23-40; EUD1-R1, R3,
  R4) and owner finding OD-F1, and updated to R23-37; see "Changes". Owner O-D, run
  `APP-V4-DESIGN-PASS-4-20261003`, early unit EU-D1. Serves OUT-001 (§2,
  §3, §7), OUT-002 (§4, §5, §8, as definition), OUT-003 (§9, through
  `RUN/D/`) and OUT-004 (§6, its form).
- **Status:** PROPOSED. No PEC response, tool, release or App adoption
  exists: PEC DEL-04-03 and DEL-08-06 are INITIALIZED; DEP-002 is
  `OPTIONAL_RECEIVING_QUALIFICATION_UNESTABLISHED_AT_ffb2b6289`; D-PEC-108
  is the newest PEC decision (no PEC change since, `git log`).
- **Basis:** ScopeOfWork sha256 `5e2fba1d2191d97832a3f09feeb91f4f4231775a6a99b2b6c769a54c43edc5e3`
  (INIT; no SCA revision); Dependencies.csv `62fc67a92d230f27bb5b3b62d4a65772245dc1810ef0b74f05df749c94308fa3`.
  Accepted basis: PRD V4-CON-02/03, HOST V4-HI-61…63, EXAMINATION
  V4-EXM-30, DECISION_BRIEF d6. PEC's own contract, read as a provider
  constraint (CLM-005), not as an adopted wire schema: PEC PRD PEC-K-01…03,
  PEC-ORI-001…007, PEC-API-001, PEC-API-007 (sha256 prefix `ae49b8065698f003`);
  DEL-04-03 CLM-003, CLM-019, REQ-016…023 (`10819cb2ea90c766`); DEL-08-06
  REQ-001, REQ-015, TBD-003/004/006 (`aecc513161c1e8a5`). Rulings: R23-34
  items 1, 2, 3, 7; R23-22.
- **Pin basis:** 0.158.0 (HOSTING-v0.9 §6.8 surfaces; §4.1).
- **Schema:** `pec.receiving-record.schema.json` (references DEL-07-02's
  `connector.standing.schema.json`).

## 1. Boundary (REQ-007)

The App consumes PEC; it never builds, extracts, qualifies or publishes it.
PEC owns no execution, queue or ruling (V4-CON-02). The fleet views do not
read PEC (FV-v0.1 §2, "Not inputs (SETTLED …) PEC"; DV-v0.1). PEC's receiving
record and presentation are this deliverable's. The source-file route is
DEL-07-02's.

## 2. The first consumer question (R23-34 item 2)

**Q1.** For one loop or undertaking L at revision R: (a) which work-graph
nodes are READY, ACTIVE or BLOCKED; (b) which other nodes are open (any
state other than COMPLETE); (c) which nodes changed state or were added
since revision S.

| Part | PEC query kind it maps to | Claims and feed | Stamp vs envelope meaning used | Without reliance |
|---|---|---|---|---|
| (a) | Orientation (PEC-ORI-001: open nodes "over work-graph READY/ACTIVE/BLOCKED nodes") | Record-tier claims, feed `work_graphs` | Pin = examined-through SHA; per-feed coverage and freshness from the envelope | Route (DEL-07-02) |
| (b) | **Outside PEC's orientation coverage** for nodes in other states | — | — | Route, always (or a delta claim for a node that changed) |
| (c) | Deltas since a caller SHA (PEC-ORI-002) | Record-tier delta claims, feed `work_graphs` | As (a) | Route |

Q1 is answered from the method's files (the Markdown work graph), which PEC's
feeds declare. No PEC coverage of the App's `chirality.fleet.record` is
assumed (FR-v0.1 §8: "PEC: none adopted"). The terms above are the App's
proposal; agreeing them with the PEC owner is OI-022, at the point of need.

## 3. What PEC states, and how the App keeps it apart

| PEC meaning (source) | App element | Kept apart from |
|---|---|---|
| Three-field stamp: examined-through SHA, generation time, per-feed freshness (PEC-ORI-003) | `stamp` | The envelope (REQ-003) |
| Reliance envelope: pin, per-feed coverage/freshness/limitation, per-claim trust tier, file-fallback signal (PEC-ORI-007; DEL-04-03 REQ-016…020) | `envelope_elements`, per-claim `stated_tier` | The stamp |
| Citation: path, anchor and/or SHA (PEC-ORI-004) | per-claim `citation` | — |
| Release identity and stated qualification (§12 gate; DEL-10-13) | `release` | Adoption (§6) |

A value PEC does not supply stays null and is a visible limitation.

## 4. Deriving the standing (rules PR-1…PR-7)

- **PR-1 Absence.** No response → condition `absent`, envelope `unknown`,
  no stamp, no envelope, no claims; route needed (REQ-005).
- **PR-2 Envelope.** `adopted` only if the response's release and every
  feed the question needs are adopted in the OUT-004 account (§6);
  otherwise `not_adopted`. A claim outside the adopted feeds is
  `outside_coverage`.
- **PR-3 Condition** (all that hold are recorded; the shown one follows
  CFB §2.2's order):
  - fallback signal `set` → `failing`; `not_stated` → `unknown`;
  - a needed feed with a stated limitation or partial coverage → `partial`;
  - **freshness by content, no time threshold (TBD-001):** if the pin is not
    a revision the receiver can read → `unknown`; if the cited source path
    has different content at the pin than at the asked revision → `stale`;
  - otherwise `current`.
- **PR-4 Claim tier.** `record` → `record`; `presence` → `presence_advisory`,
  shown with its heartbeat age; anything else → `unknown`. A presence fact
  cites PEC's presence record, never a file (PEC-K-02).
- **PR-5 Claim reliance.** CFB CS-R1 (PEC: `record`). In a current
  response, a record-tier claim whose cited file has **different content**
  at its citation revision than at the asked revision is `stale`. A
  citation revision the receiver cannot read is `unknown` ("revision not
  comparable"). Content is compared, not revision identifiers (RV2
  EUD1-R4): a citation may name the commit that last changed the file.
- **PR-7 Citations resolve.** A record-tier claim's citation must resolve:
  the path is a project file, the revision is readable, and the anchor (if
  any) is a heading in that file at that revision. If it does not resolve,
  the claim's condition is `unknown`, with the reason, and it supports no
  reliance (owner finding OD-F1).
- **PR-6 Conclusions.** Per Q1 part: connector reliance where every needed
  claim supports it and covers the part; otherwise the route. A relied
  part is worded as a report of the record at its pin ("PEC reports, from
  the work graph recorded at ‹pin›: …"), never as an App conclusion
  (CFB CS-R2 (ii); R23-40). Every record names, as unsupported, that any
  item is ready to start, complete or permitted because of PEC material. The four
  prohibited conclusions are always listed (CS-R2), and so are the named
  unsupported conclusions (CS-R3): presence never shows anyone is working or
  that anything is correct; a not-adopted release is reported as unqualified,
  not as a failed product (V4-EXM-30).

## 5. Receiving record (`pec.receiving-record.schema.json`)

One record per response (or no response) per question: input identity and
fixture standing; release; adoption read; stamp; envelope elements;
response standing; claims with their standing; conclusions; route reference.
`simulated: true` with `simulated_terms` for every record built from
constructed input (REQ-008). Records live with the user's project
(OI-013/OI-014).

## 6. Adoption evidence account (OUT-004; R23-34 item 7)

Two facts, recorded apart:
1. **Release-level adoption** by the App receiving owner: release identity,
   adopted feeds, the qualification and release evidence relied on, accepted
   limitations, and D108 carried as stated ("ACCEPT_AS_IS; RF-001 MAJOR
   retained; DEL-00-01/AC-002 partly met; no repair, readiness, release or
   adoption inferred"). Recorded like the qualification pin (R23-22).
2. **Per-installation enablement:** the person's own Codex configuration
   of PEC's tool surface (PEC-API-007 "consumer-owned"; L-3), changed by
   the App only when the person directs it (HOSTING §6.8).

Neither is needed before a qualified PEC release exists. Until then every
envelope is `not_adopted` or `unknown`. EU-D1's account is constructed and
says so.

## 7. Route of consumption (R23-34 item 3; R23-37 item 1)

| Path | Use | Standing |
|---|---|---|
| Agent tool call to PEC's MCP server in the person's Codex configuration, observed as `mcpToolCall` (HOSTING §6.8; NPTD tool row) | The agent's use; the App builds a receiving record from the observed result | Designed |
| App-origin `mcpServer/tool/call` to the same configured server, recorded with initiator App | The App's own presentation read, for **App views** | **Permitted for App views by R23-37 item 1's condition, met by probe P-H1b** (below). Recorded with initiator App and never presented as the agent's call (HOSTING §6.8) |
| App-held PEC client, socket or token | — | Excluded (R23-34 item 3) |

**What the probes observed** (`RUN/D/probe/`; 0.158.0; DEL-01-01's MCP
double; scratch homes under `/tmp`, removed; no sign-in, no download):
- **P-H1, no model.** The call's result returned to the App, and the server
  received the thread id in `_meta`. No notification followed. The thread's
  persisted rollout gained nothing: one line, no trace of the call.
  `thread/items/list` failed before and after ("not supported yet"), so "no
  entry in thread items" rests on the absence of notifications and on the
  rollout, not on an items read (RV2 EUD1-R3). R23-37 item 1 rules thread
  items and history settled as "no entry".
- **P-H1b, the next turn's model input.** DEL-01-01's OBS-2 provider tap,
  in capture-only mode on loopback, recorded the request Codex sent for the
  next turn and forwarded nothing; no model was called, and LM Studio was
  not started. The request's `input` held three `message` items. None of the
  call's markers (`P-EX-1`, `toolReceivedAtMs`, the result text) appeared
  anywhere in the request, and there was no tool-call or tool-output item.
  R23-37 item 1's condition holds: **no trace in the model's input.**
- **Scope of that result:** 0.158.0, one custom Responses provider route,
  the first request of the next turn. A later pin or route rechecks it at
  its version-advance check.
- The HOSTING §6.8 receiver row for DEL-07-01 goes to DEL-01-01's next
  revision (not edited here).
- **Recorded for DEL-01-01's owner (R23-37 item 2):** `thread/items/list` and
  `thread/read` with turns answered "not supported yet" on a thread with no
  turn.

## 8. Presentation (OUT-002, as definition)

The App shows, per item: the statement, its citation, the stamp and envelope
values, the standing (three facets and reasons), and whether it supports
reliance. A presence fact is labelled advisory with its age. When the route
is needed, the App shows the route account's answer marked "from files",
next to the PEC material and never merged into it. Layout is not designed
here.

## 9. Fixtures and verification (EU-D1; `RUN/D/`)

FX-EUD1 P1…P8, all `constructed` from the elements in §3:
- P1 adopted and current;
- P2 not adopted (stated unqualified);
- P3 adopted with pin at S (stale);
- P4 adopted, feed partly parsed (partial);
- P5 adopted, fallback signal set (failing);
- P6 no response (absent);
- P7 the question asked **at S** (Q1-S), adopted and current: c1 relied as
  "the work graph at S marks O-B1, O-C1 READY", while "may be started now"
  is named unsupported (R23-40);
- P8 as P1, but claim c3's anchor is not in the cited file: c3 is `unknown`
  (PR-7), and (c) goes to the route.

The sources are this run's real work graph at commits `e4a0c2c4c3` (S) and
`e086dfff32` (R).

| VER | EU-D1 | Standing |
|---|---|---|
| VER-001 | §2's mapping; every term agreed or open (§10) | inspection |
| VER-002 | P1 vs P2 vs no adoption | rehearsed |
| VER-003 | Stamp and envelope kept apart; missing values null; P8 unresolvable citation | rehearsed |
| VER-004 | c8 presence never relied on; P7 relied report establishes no readiness; no owner act written | rehearsed |
| VER-005 | P3…P6 same question, route handoff | rehearsed |
| VER-006 | §6 form, D108 carried | form only; no real account |
| VER-007 | §1 | inspection |
| VER-008 | DEL-09-10's records | rehearsed |

## 10. Open (OI-022 and others)

| Matter | Who | Point of need |
|---|---|---|
| PEC's tool representation, operations, parameters, no-response signal (DEL-08-06 TBD-003/004/006) | PEC owner (EXTERNAL) | Before dependent adapter behaviour |
| Agreement of §2's questions and §3's mapping | App receiving owner with the PEC owner | Before operational reliance |
| Per-feed freshness meaning beyond the revision test | Same | Same |
| HOSTING §6.8 receiver row for App-origin reads (§7) | DEL-01-01's owner | DEL-01-01's next revision |
| Release-level adoption (§6) | App receiving owner | After a qualified PEC release |

## Changes

| Finding (ruling) | Change | Where |
|---|---|---|
| RV2 EUD1-R1 (R23-40) | Relied parts are worded as reports of the record at its pin. Every record names "ready to start, complete or permitted" as unsupported. Case P7 (Q1 asked at S) added | §4 PR-6, §9 |
| RV2 EUD1-R3 (R23-37) | §7 cites R23-37 item 1 and states which observations support it; P-H1b's result is recorded; App-origin reads are permitted for App views | §7, §10 |
| RV2 EUD1-R4 | PR-5 compares content at the citation, not revision identifiers; an unreadable citation revision is `unknown` | §4 PR-3, PR-5 |
| OD-F1 (owner, from RR-EUD1) | PR-7: a record-tier citation must resolve, or the claim is `unknown`. Presence facts cite PEC's presence record. Case P8 added; claims renumbered (presence c9 → c8) | §4 PR-4, PR-7, §9 |

