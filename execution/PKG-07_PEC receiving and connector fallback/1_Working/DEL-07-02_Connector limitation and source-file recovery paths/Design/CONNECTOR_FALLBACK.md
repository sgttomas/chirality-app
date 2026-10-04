# Connector standing and the source-file route

- **Contribution:** DEL-07-02/CFB-v0.2. It supersedes CFB-v0.1 (sha256
  `ae49d6543f92c38c3c3772c39e4fa4ebfdb53f33bedae3f0f75339dd88be33c8`, the
  EU-D1 freeze RV2 reviewed), repaired for RV2-EUD1 under R23-40 (EUD1-R1,
  R1 item 2, R2, R5) and R23-37 item 3; see "Changes". Owner O-D, run
  `APP-V4-DESIGN-PASS-4-20261003`, early unit EU-D1. Serves OUT-001
  (receiving behaviour: §2, §3), OUT-002 (the route and responsibility
  account: §4, §5) and OUT-003 (fixtures: §8, through `RUN/D/`).
- **Status:** PROPOSED. Designed and rehearsed on constructed inputs; not
  built, not qualified. No PEC or Domains response, release or adoption
  exists (DEP-002 unestablished at `ffb2b6289`; DEP-003 parallel/later).
- **Basis:** ScopeOfWork sha256 `6b618f9a0300794b8edd4c6f2fb3e50a9d51f3647c446abc668755a25cd12151`
  (INIT `ddd721a90a`; no SCA revised it, so R23-5 has no block to read);
  Dependencies.csv `42b737be974b711a72570e910b716a834782ffaba5e693dd23988163170f9122`.
  Accepted basis: PRD V4-CON-02…04 and §3.1, HOST_INTEGRATION V4-HI-61/62,
  §8.1, ARCHITECTURE V4-ARC-22, EXAMINATION V4-EXM-30, DECISION_BRIEF d6.
  Rulings: R23-34 items 1, 2, 6, 10 (H-3 vocabulary here; H-2 question; H-6
  files, not rows); R23-2, R23-21 item 1. SCC-CASE-005 R1 milestone 1.
- **Pin basis:** no Codex surface is relied on here.
- **Schemas:** `connector.standing.schema.json` (the vocabulary, §2) and
  `connector.route-account.schema.json` (§4), Draft 2020-12.

## 1. What this file decides

A connector (PEC, later Domains) may be qualified and current, limited, or
absent. This file gives one way to say which, a rule for when its material
may be relied on, the conclusions nothing about a connector can establish,
and the route that answers the same question from ordinary project files.
Connector-specific derivation is DEL-07-01's (PEC, PRC-v0.1) and DEL-08-01's
(Domains, DRC-v0.1). They use this vocabulary; they do not redefine it.

## 2. The standing vocabulary (frozen at EU-D1; R23-34 item 1; repaired at v0.2)

Every connector item shown or recorded by the App carries a **standing**
with three facets. The App never shows connector material without it.

### 2.1 Envelope: has the receiving owner established a basis for reliance?

| Value | Meaning |
|---|---|
| `adopted` | **PEC:** the release is qualified and released, and the App has deliberately adopted it for this feed (DEL-07-01 OUT-004 account; R23-34 item 7). **Domains:** an identified query contract and admission basis established by the receiving decisions (DEL-08-01 OUT-004; OI-023) |
| `not_adopted` | Material exists, but that basis is not established (unqualified, unreleased or unadopted release; unidentified Domains contract) |
| `outside_coverage` | The item's subject is outside the adopted coverage |
| `unknown` | No material, or the basis cannot be determined |

### 2.2 Condition: what state is the material in against its sources?

| Value | Meaning (connector-specific tests in PRC §4 and DRC §4) |
|---|---|
| `current` | Supplied for the asked revision, with no stated limitation and no failure signal |
| `stale` | Built from an earlier state of a source that has since changed |
| `partial` | Some needed coverage is missing, unparsed or truncated (PEC-ORI-006) |
| `failing` | The provider reports it is failing its own checks (PEC's file-fallback signal set) or its response is unusable |
| `absent` | No response at all; handled by the receiver, since no response can carry a signal (DEL-07-01 REQ-005) |
| `unknown` | The condition cannot be determined (e.g. the failure signal is not stated; a pin the receiver cannot compare) |

When several hold, the shown value follows the order **absent, failing,
partial, stale, unknown, current**, and every one that holds is listed in
`reasons`. Nothing ever becomes `current` by default.

### 2.3 Claim tier: what kind of item is it?

| Value | Meaning |
|---|---|
| `record` | **PEC only.** Record tier (derived from files; PEC-K-05) |
| `presence_advisory` | **PEC only.** Presence fact, advisory at its stated heartbeat age; never correctness. It cites PEC's presence record, never a file (PEC-K-02) |
| `admitted` | **Domains only.** Source admitted for the intended use, at an identified revision |
| `located_not_admitted` | **Domains only.** Search hit without admission (retrieval is not admission; DEL-08-01 REQ-001/002) |
| `unknown` | Either connector. Tier not stated; never treated as `record` or `admitted` |

A standing names its connector, and a record's standings name that record's
connector. The schema refuses a tier of the other connector (RV2 EUD1-R2).

### 2.4 Rules

- **CS-R1 Reliance, per connector.** An item supports reliance **only if**
  envelope is `adopted`, condition is `current`, and the tier is the
  connector's reliable tier: **PEC `record`; Domains `admitted`**. Every
  other combination supports none. The schema enforces one direction (a
  reliance claim must have those values for its connector); the prototype
  checks the other (those values give reliance).
- **CS-R2 What a connector may establish (restated, R23-40, from V4-CON-02,
  V4-CON-03 and V4-HI-62).**
  - (i) A connector's **absence or any limitation never implies** empty work,
    readiness, completion or permission.
  - (ii) A **relied record-tier claim** (adopted + current + `record`)
    **reports only what its cited record states at its pin.** "The work graph
    at S marks O-B1 READY" is a report of the record, not an App conclusion
    that O-B1 may start. Presence, and the connector itself, never establish
    readiness to start, completion or permission.
  - Record values: every record lists `no_work`, `ready`, `permitted` and
    `correct_by_presence` as prohibited, so no consumer has to infer them.
    "Completion" (done, satisfied) is not a record value (R23-40 item 2); it
    is stated in §3 with CS-R5.
- **CS-R3 Unsupported conclusions are named.** Each record lists, with
  reasons, the conclusions its material does not support, in words a reader
  can use.
- **CS-R4 Independence.** A connector's standing is derived from that
  connector's inputs only. PEC's standing never changes Domains', and the
  reverse (REQ-005; V4-ARC-22). §8 checks this by deriving each with the
  other's inputs removed.
- **CS-R5 No promotion.** `unknown` is never shown as `current`, a missing
  value never as complete, a prepared duty never as performed (REQ-001,
  REQ-004).

## 3. Condition → route

| Standing of the question's material | The App shows | Route |
|---|---|---|
| Reliance supported for every part of the question | The items with their standing | Not needed for those parts |
| Reliance supported for some parts | Those items; the other parts as "not covered" | Needed for the other parts |
| Any other standing, or `absent` | The standing, its reasons and the unsupported conclusions; no connector conclusion | Needed for the whole question |

Independently supported work continues meanwhile. A part that has only the
connector as its source waits, with the missing input named, and is never
marked satisfied (REQ-005).

**Prohibited conclusions (R23-40 item 2; consumers such as FV refer here).**
Connector material, its limitation or its absence never establishes, for any
item:
1. that no work remains (empty work);
2. that it is ready to start, may be dispatched or is permitted;
3. that it is complete, done or satisfied (CS-R5: a missing input is never
   marked satisfied; `unknown` is never promoted);
4. that anything is correct because of a presence fact.

A connector need counts as met only when CS-R1 supports reliance. Meeting a
need is not readiness: an item's readiness is decided by its consumer's own
file-based rules (for FV, V4-PM-06; RF-5a, R23-39).

## 4. The route account (`connector.route-account.schema.json`)

One account per affected question, written with the user's project
(OI-013/OI-014: no common service; as FR-D3). It holds:
- the question, the revision asked and, for a change question, the since
  revision;
- the trigger: which connector, why, and the receiving records that sent it;
- each source read: path, revision, sha256 of the bytes read and its role;
- the facts found, each with its source and anchor;
- gaps, each with its effect and who is responsible for closing it; when a
  needed source is unavailable, that is a gap, never a guessed answer
  (REQ-002);
- conclusions supported (basis `source_route`), unsupported, and the four
  prohibited ones;
- the duties, each with its actual standing (§5);
- the recorder and time.

Reading files is how the answer is found, not what makes it authoritative
(REQ-002). Records the account cites keep their own standing.

## 5. Duties and their standing (REQ-004; d6; PRD §3.1)

| Duty | Actor role (in the App) | Meaning |
|---|---|---|
| `locate_compare` | agent (TASK, Type 2) | Find the graphs, decisions and revisions and compare them |
| `review_integrate` | manager (HELP_HUMAN or WORKING_ITEMS) | Review the account and integrate its result |
| `cross_undertaking_coordination` | person | Carry what crosses undertakings or projects |

Standing: `prepared`, `performed`, `outstanding` or `not_required` (with a
reason). `performed` needs the actor and evidence (schema rule). A brief, a
source read or a future fleet view is never evidence that someone performed
a duty.

## 6. Interfaces

| Direction | With | What | Arc (DAG-004) | When it fails |
|---|---|---|---|---|
| Supplied to | DEL-07-01 (DEP-07-01-014) | The vocabulary, §3 and the route account | held (SCC-004; R1 milestone) | — |
| Supplied to | DEL-08-01 (DEP-08-01-009) | The same, for Domains | held (SCC-004) | — |
| Consumed from | DEL-07-01 (DEP-07-02-010/012) | PEC derivation rules; later, the adopted envelope account | held | PEC items stay `unknown`/`not_adopted`; route used |
| Consumed from | DEL-08-01 (DEP-07-02-011) | Domains derivation rules | held | Domains items stay `not_adopted`; route used |
| Offered to | DEL-06-02 FV (DEP-07-02-015) | A connector waiting cause: the standing (§2) and the route account reference | admitted | FV shows no connector state (its current behaviour) |
| Read as files | Project graphs, decisions, fleet records (DEP-07-02-013) | Sources of the route | not topological | A missing source is a gap |
| Supplied to | DEL-09-10 (DEP-09-10-006) | Records and fixtures for its cases | admitted | — |

**R23-34 item 6 (H-6).** This deliverable reads fleet records and work
graphs as files. A row to DEL-06-02 would close a cycle in the admitted
layer, and a row to DEL-06-01 one in both layers. FV consumes this
deliverable, never the reverse.

## 7. Failure behaviour

| Case | Behaviour |
|---|---|
| Source missing or unreadable | Gap with its responsible party; the affected part unsupported |
| Revision not resolvable | Condition `unknown`; route says so |
| Sources contradict each other | Both facts recorded with anchors; the conclusion unsupported until resolved by its owner |
| Record or account unreadable | The consumer shows `unknown`; nothing is inferred |
| Connector recovers later | New receiving records; earlier route accounts stay as written |

## 8. Verification (designed; EU-D1 rehearsal in `RUN/D/`)

| VER | How EU-D1 exercises it | Standing |
|---|---|---|
| VER-001 | Six PEC and two Domains records: standing, reasons, unsupported conclusions | rehearsed (constructed) |
| VER-002 | One question Q1 through absent, stale, partial and failing, plus not-adopted and an unresolvable citation (P8); route account `ra:EUD1-Q1` on the real work graph at two commits | rehearsed |
| VER-003 | CS-R2 on every record; no "no work" although no node is READY/ACTIVE/BLOCKED (T2 is PLANNED); P7 (Q1 asked at S, adopted and current) relies on "the work graph at S marks O-B1, O-C1 READY" as a report and still names "may be started now" unsupported | rehearsed |
| VER-004 | Route walked from files only; duties performed/outstanding/not required with evidence | rehearsed |
| VER-005 | OC-1 (PEC absent + Domains stale) and IA-2 (PEC adopted-current + Domains absent); CS-R4 by removing the other connector's inputs | rehearsed |
| VER-006 | Later PEC join: P1 (adopted) vs P2 (not adopted) | rehearsed on a constructed account only |
| VER-007 | EXP rehearsal records in DEL-09-10 | rehearsed |
| VER-008 | §6 owner boundary | inspection |

## 9. Open

| Matter | Owner | Point of need |
|---|---|---|
| FV's connector waiting cause (S-3) | O-A (DEL-06-02), row in FV | After this vocabulary is frozen |
| PEC-specific terms (OI-022) | DEL-07-01 with the PEC owner | Before PEC-dependent implementation |
| Domains admission/query terms (OI-023) | DEL-08-01 with the Domains receiving owners | Before Domains-dependent implementation |
| Placement of route accounts in a user project | O-D, with DEL-06-01's placement | Before implementation |

## Changes

| Finding (ruling) | Change | Where |
|---|---|---|
| RV2 EUD1-R1 (R23-40 items 1, 2) | CS-R2 restated: (i) absence or limitation never implies empty work, readiness, completion or permission; (ii) a relied record-tier claim reports only what its cited record states at its pin. The prohibited conclusions, including completion, are listed in §3 with CS-R5, and the need/readiness distinction is stated for consumers (FV). Case P7 added | §2.4, §3, §8 |
| RV2 EUD1-R2 | CS-R1 per connector (PEC `record`, Domains `admitted`); tiers marked per connector; the schema refuses cross-connector tiers and standings | §2.3, §2.4; `connector.standing.schema.json`; DEL-07-01/08-01 record schemas |
| RV2 EUD1-R5 | `connector.route-account.schema.json` gains `written_at_source` (`observed_clock` or `build_constant`) | §4 (schema) |
| OD-F1 (owner) | Presence facts cite PEC's presence record, never a file | §2.3 |

