# Domains receiving: query, admission and freshness

- **Contribution:** DEL-08-01/DRC-v0.1 (new). Owner O-D, run
  `APP-V4-DESIGN-PASS-4-20261003`, early unit EU-D1. This version carries
  what EU-D1 needs (§2–§5) and the outline of the rest (§6–§8). Serves
  OUT-001 (§2–§4), OUT-003 (§5, through `RUN/D/`) and OUT-004 (§7).
- **Status:** PROPOSED. No Domains provider, contract, corpus, deployment or
  admitted source exists. Every Domains input in EU-D1 is invented.
- **Basis:** ScopeOfWork sha256 `df2795869011f9364d5acf7541d66e2c32ffdd382c757153ad8d1fe8492607d7`
  (revised under SCA-V4-001: CLM-003, AX-005; no SCA-V4-003 block bears on
  it); Dependencies.csv `69bc284d0f71ed0d13d3c6c49e7267e447bc02f8d5e37df790eff1e2d4432a06`.
  Accepted basis: PRD V4-CON-01, -03, V4-HOST-02 (DECISION-5), OQ-03; HOST
  V4-HI-60, -62, -64, §8.1; EXAMINATION V4-EXM-30, -32. Rulings: R23-34
  items 1, 5, 6 and its preamble (OI-026, starting the Domains-enabled
  increment and any relaxation of V4-HOST-02 are the person's acts at their
  own points of need).
- **Schema:** `domains.receiving-record.schema.json` (references DEL-07-02's
  `connector.standing.schema.json`).

## 1. Boundary (REQ-008)

This file defines what a receiver needs from a Domains query and how it
records and shows it. It selects no provider, database, corpus, transport,
deployment or wire field. Provider allocation (OI-026) and the start of the
Domains-enabled increment (OI-023's milestone) are not decided here.

## 2. Query and result meanings (REQ-001)

| Element | Meaning |
|---|---|
| Request | A research question and its intended use (the use admission is judged against) |
| Result | One located source passage: source reference, the source revision it was indexed from, a snippet, and the admission state supplied |
| Index basis | What the result set was built from, as supplied |
| Contract identity | The identified query contract (HOST §8.1 "Search-tool/query interface"); null while unidentified |

A result locates evidence. It establishes no membership, standing,
applicability or authority (V4-CON-01; V4-HI-60).

## 3. Admission (REQ-002)

- A source is **admitted** for an intended use at an **identified revision**
  by an admission basis the receiving decisions establish. EU-D1's basis
  `ADM-1` is invented.
- A located source without admission is `located_not_admitted` (CFB §2.3).
- Admission at one revision does not carry to a later revision.
- The admitting party is **not named here**: it comes with the provider and
  receiving decisions (OI-023, OI-026; REQ-002 "not an invented standing
  human gate").
- PEC's state plays no part in admission (SOW-247; CFB CS-R4).

## 4. Freshness and standing (REQ-003; rules DR-1…DR-4)

- **DR-1 Absence.** No response → condition `absent`, envelope `unknown`, no
  results, route needed.
- **DR-2 Envelope.** `adopted` only when the query contract is identified and
  established with its admission basis; otherwise `not_adopted`.
- **DR-3 Condition per result,** by revision, with no age threshold: the
  receiver reads the source's current revision; equal to the indexed
  revision → `current`; different → `stale`; unreadable → `unknown`. The
  response condition is the worst result's (CFB §2.2 order).
- **DR-4 Tier and reliance.** `admitted` if the result's admission is
  supplied and found in the admission basis; `located_not_admitted` if
  supplied as not admitted; otherwise `unknown`. Reliance follows CFB CS-R1.
  A stale admitted result supports nothing, because the admitted revision
  is not the source as it stands.

## 5. EU-D1 cases (`RUN/D/`)

- **QD:** "Which admitted source supports the (invented) statement 'line
  EX-L1 support spacing is 3.0 m', and does that support hold for the
  source as it stands now?"
- **DM-1:** a constructed result set built from SRC-1 rev-A (admitted at
  rev-A) and SRC-2 (never admitted). SRC-1 now stands at rev-B and says
  2.4 m. Expected: envelope `adopted`, condition `stale`; r1 admitted but
  stale, r2 located-not-admitted; no reliance. The route
  (`ra:EUD1-QD`) reads SRC-1 rev-B and names the missing re-admission.
- **DM-2:** no response → `absent`; no research context is fabricated.
- **With PEC:** OC-1 pairs DM-1 with PEC absent (P6); IA-2 pairs DM-2 with
  PEC adopted-current (P1). Domains' standing is derived from Domains
  inputs only.

REQ-004's fixtures ("candidate query/result fixtures grounded in admitted
test sources and the identified query contract") stay **unexercised**:
EU-D1's sources and contract are invented, not admitted or identified.

## 6. Deployment and data-boundary compatibility (REQ-006; outline)

V4-HOST-02 (DECISION-5) is settled. For a host's agent, the arrangements
compatible with it are:

| Arrangement | Compatible because | Supplier text |
|---|---|---|
| Local or in-process query tool | Adds no destination | CLM-003 |
| Stateless MCP server the person allows (revision 2026-07-28) | An allowed destination, recorded and shown | LOOP-v0.9 §5.1.1, §5.3 DF-7 |
| Host catalog entry that declares its external contact | Declared traffic passes the destination check | LOOP §5.3 DF-1, DF-4 |
| Remote service | Only as a destination the person allows | HOST §8.1 |

Undeclared traffic of a host operation is refused at contact unless allowed
(LOOP DF-F8; N-OPEN-3). A relaxation of V4-HOST-02 would be a basis
amendment, which is the person's act. Nothing indicates one is needed.
SWBPIPE's DEC-051 open residency is SWBPIPE's to reconcile at the host joins
(DECISION-3).

## 7. Decision account (OUT-004; outline)

| Matter | Owner (as the files state) | Point of need | Standing |
|---|---|---|---|
| Provider allocation (OI-026) | Owner with App/Domains/SWB definition owners | Before allocating provider production | Person's act (R23-34); not now |
| Starting the Domains-enabled increment (OI-023 milestone) | Owner with Domains/SWB/App receiving owners | Before that increment | Person's act (R23-34); not now |
| Query contract, admission and freshness terms (OI-023 content) | App side: this file; agreement with the provider | Before dependent implementation | App side proposed here |
| How a workflow declares a Domains tool | Domains-enabled increment (R23-34 item 5: WD keeps two classes) | Before the research workflow is declared | Noted, not opened |
| Admitting party | With the allocation | Before reliance | Open |

## 8. Handoffs

- To DEL-07-02: Domains derivation rules (§4); limitation cases (§5).
- To DEL-08-02 (DEP-08-02-005): §2–§4 and §7 for the research method.
- To DEL-09-10 (DEP-09-10-007): §5's cases for OC-1 and IA-2.
- Not to LOOP: LOOP does not consume this deliverable (R23-34 item 6); a
  Domains tool reaches a host loop as a catalog entry or an allowed MCP
  server.
