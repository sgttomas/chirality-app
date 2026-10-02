# App act control

- Contribution: DEL-01-04/AAC-v0.2 (supersedes AAC-v0.1, committed at
  `63a6e0fa47`, sha256 7e98118c774fcd9c3e60f04e7def51b3a11325995ae343426fba892ea439e181).
  Companion: [NATIVE_INTERACTION_RECEIVING.md](NATIVE_INTERACTION_RECEIVING.md)
  (DEL-01-04/NIR-v0.2), whose header records the basis, the inputs (round 1
  and round 2) and their sha256; they are not repeated here.
- **Standing: PROPOSED until SCA-V4-003 carries SC2-01-04-1** (R17-6). The
  obligation is not in DEL-01-04's ScopeOfWork (sha256 0cdb44e2…, NIR L-1);
  DECISION-K1 K1-4 directed that it be proposed for the next amendment, and
  the owner's pass-3 direction and DECISION-K3 (K-8) start its design now. This
  file amends SC2-01-04-1 for K-8 (A15, DEL-02-02 as consumer): proposal
  SC3-01-04-1 in the return file `D/D3.md`.
- Status: DRAFT DEFINITION — proposed, unsupplied, not implemented, not
  accepted. Beside it: two PROPOSED schemas with a valid and an invalid
  example each (§5), and the act-control part of the prototype in
  [`prototype/act_control.py`](prototype/act_control.py) (§8).
- Run and node: `APP-V4-DESIGN-PASS-3-20261001`, node D3.
- Serves: EXEC-v0.6 §5 CAP-1…CAP-9 (the requirements this control meets);
  EXEC RC-6 and §2.5.2 AE-2; ACT-POLICY-v0.8 §2.6 and §4.7 RC-3, RC-4; RS-v0.8
  §6.1 "App interface per EXEC CAP-1…CAP-9" and HA-10; DAG-003 arc X-1
  (DEP-02-03-027); DEL-01-04 REQ-005 and VER-005's positive case.

## Changes from v0.1

| Item | Ruling / source | Where | Change |
|---|---|---|---|
| L-4 | DECISION-L L-4 (clarified); R19-4 | §1.2, §2 AI-2, §3, §4.2, §5 | One A15 act may register several entries; each entry is composed from its own A15 descriptor and binds its own bytes; one changed or withdrawn entry makes the whole offer stale; each entry's registration outcome is reported beside the act. Shipped workflows are registered by the release and byte-equal entries are recognized by DEL-02-02; neither needs this act |
| C-01 | R18-1 | §4.2, §5, schemas 0.2 | `reviewedDraft.draft` is WR ID-3's string `draft:<location>:<name>@<content identity>`; `priorRevision` is an RS `workflowTuple` or null (RS defines the persisted form) |
| L-5 | DECISION-L L-5 | §6.2; U-AAC-2 | No OS password or biometric check per act: P-3 not adopted; U-AAC-2 closed |
| R18-5 | R18-5 (U-NIR-5) | AK-a | Opening the control from an arrival row by the person's click is the person's act, not a reaction: DERIVED |
| C-10 | R18-1 | §7 | The Codex account is the reported email or "ChatGPT account (no email reported)"; no plan type is recorded |
| O-6 | OBS-2 O-6 | §7 | Filled in part: each Codex home reports its own account (a second home sharing the first's configuration reported `null`); a signed-in account stays not observed (DECISION-L L-6) |
| C-22 | R18-1 | U-AAC-4 | Closed: the A15 order and names agree with WR |

**Binding inputs.** DECISION-K1 K1-1 (the agent asks; the product offers the
means and records what it observes), K1-2 (an earlier act on current content
counts), K1-3 (joint answer), K1-4 (the person's identity, "identity not
verified"; the obligation proposed for DEL-01-04's contract). DECISION-K3 as
revised, K-8: "Registration (A15) is performed through the person-only act
control of DEL-01-04, bound to the exact reviewed bytes; a draft changed after
review needs a new review." R17-5 (process division, PROPOSED), R17-6 (the act
control serves every reserved act kind including A15; standing facility, never
raised by an arrival; identity per K1-4), R17-11 (an A15 names its subject by
the reviewed draft content and, for a new revision, the prior revision), R17-12.

---

## 0. What the control is, in one paragraph

A dedicated control in the App that only the person can operate. It presents
one act kind at a time on one piece of App content whose content identity it
fixes when it presents it; it offers the decline where an act-declined event
exists; and when the person confirms in a confirmation surface the App's host
owns, it produces capture evidence and a direct-capture human-act record in
DEL-04-03's format. It is always available (a standing facility); no arrival,
request or rule opens it. Presenting it answers no supplier request.

## 1. Obligations

### 1.1 EXEC CAP-1…CAP-9: disposition

| CAP (EXEC-v0.6 §5) | Disposition here | Where |
|---|---|---|
| CAP-1 Scope: acts on App content (App files and App-side outputs by file content identity); A12 where an App control establishes the setting; not host content | **Amended (K-8):** App content also includes a **workflow draft's reviewed content**, for A15. A12: no setting the App itself establishes exists in this increment, so the control is ready for it but offers none (§1.2). Host content stays the host's facility (no proxy, U-E9) | §1.2 |
| CAP-2 Act control: one act kind at a time; kind in R-4 wording; bound subject with content identity; scope and purpose; actor requirement; the arrival it answers; the decline | **Accepted.** Wording per ACT §9 (§1.2). "The arrival it answers" is shown when the person opened the control from an arrival; otherwise the offer says "no arrival: a standing act" (RC-6). The decline is offered only where ACT §2.3 defines an act-declined event | §3, §5.1 |
| CAP-3 Direct capture record with a capture-evidence reference {act identity, actor, act kind, bound content identity with method, scope, purpose, time, surface "App interface", arrival reference} | **Accepted**, with the capture-evidence object defined as `aac.capture-evidence.schema.json`, and the record written through DEL-04-03's writer as `human_act` (recording mode *direct capture*, recorder role "App interface (capturing surface)") or `act_declined` | §5 |
| CAP-4 Not operable by automation | **Accepted**, stated as requirements NA-1…NA-6 and a PROPOSED placement under R17-5, with the limits that no placement removes | §6 |
| CAP-5 A14 settlements are never act evidence | Accepted unchanged | — |
| CAP-6 Answers to questions and elicitations are input to the agent, never act evidence; the App may respond by presenting its own control | Accepted. NIR LB-4 places the entry on every question card, never pre-filled from an arrival | NIR §4.2 |
| CAP-7 Conversation statements never satisfy | Accepted unchanged | — |
| CAP-8 Person identity per K1-4, "identity not verified"; A7's accountable professional as the person's own statement | Accepted; sources and their reading in §7 | §7 |
| CAP-9 Presenting is not answering | Accepted; also, operating the control settles no pending supplier request (prototype K-5) | §3 |

Rules this file adds (PROPOSED unless labelled):

| # | Rule | Source |
|---|---|---|
| AK-a | **Standing facility.** The control is reachable at all times from the act log, from any App file or output view, from a draft under review, from a question card (NIR LB-4) and from an arrival row's "where the act is performed" entry (SD-3). Nothing opens it except the person; when the person's click on an arrival row opens it, the person opened it and the product did not react to the arrival (R18-5, DERIVED) | RC-6; K1-1 (SETTLED); R17-6; R18-5 |
| AK-b | **No arrival raises it.** An arrival, a request, a supplier event or a rule never opens, focuses, highlights or notifies the control | SD-4; RC-4 (SETTLED by K1-1) |
| AK-c | **Bound to the bytes shown.** The offer fixes the subject's content identity when it is composed; the person's confirmation is accepted only if the subject still has that identity; otherwise nothing is captured and the person is asked to review again | K-8 (SETTLED for A15); PROPOSED for every kind |
| AK-d | **One kind, one subject, one confirmation.** Several subjects need several offers; a joint answer is several acts, each citing its referents (K1-3) | CAP-2; K1-3 |
| AK-e | **The record follows the capture.** The capture evidence exists before any record is written; a record write failure never loses the capture (RS FC-1) | RS §14 |
| AK-f | **Acts apart from their effects.** The A15 act is recorded at capture, as every kind is; the registration that follows is DEL-02-02's operation, and its outcome is reported beside the act ("registration not completed: ‹cause›"), never as part of it, as ACT keeps an acceptance apart from its application ("accepted — not applied", ACT §2.5; AS §8) | §4.2 (PROPOSED; agrees with DEL-02-02 WR-v0.1 §5.2 and SQ-G, node D5) |

### 1.2 Act kinds served in this increment

| Kind | Wording shown (ACT §9; CAP-2) | Served | Decline | Actor requirement | Subject |
|---|---|---|---|---|---|
| A4 | "mark checked" | **Yes**, on App files and App-side outputs | Yes (act-declined event) | The person | File content identity (RS L-1) |
| A6 | "approve (engineering approval)" | **Yes**, on App files | Yes | The accountable person | As A4 |
| A7 | "rely (professional reliance)" | **Yes**, on App files | Yes | The accountable professional; recorded as the person's own statement, with an evidence limit (CAP-8) | As A4 |
| A15 | "register workflow revision" | **Yes** (K-8); **one or several entries in one act** (L-4) | **No**: ACT §2.3 defines no act-declined event for A15; the person closes the control | The person | Per entry: the revision DEL-02-02's A15 descriptor names (WR RB-4), bound by that entry's reviewed draft content identity; relations per entry: the **reviewed draft** (WR ID-3 string and content) and, for a new revision, the **prior revision** (RS `workflowTuple`) (R17-11; C-01). WD's *derived-from* is not this act's relation. Shipped workflows are registered by the release and entries byte-equal to a shipped revision are recognized by DEL-02-02 (L-4); neither is offered here |
| A12 | "set grant" | Not offered: no setting the App itself establishes exists in this increment (CAP-1; ACT §2.6). The App's Codex settings are the user's own (D3) and model choice is not A12 (ACT §2.7) | (Yes, when one exists) | The person | Setting content |
| A5, A10 | "accept" / "rejected the item" | Not offered: no App-content proposal exists in this increment; host proposals use the host's act facility | — | — | — |
| A11 | — | Not offered: the proposer's act on a host proposal | — | — | — |
| A13 | — | Not offered: captured by the host's enablement facility; no App-owned external interface exists (ACT §2.6) | — | — | — |

R17-6 asks the control to serve every reserved act kind. Read with CAP-1, the
kinds above are those that have App content in this increment; the others are
listed with the reason they have no subject, so that adding one later is a
row, not a restructure.

---

## 2. Interfaces

| # | Exchange | Supplier → receiver | Condition | Failure behaviour |
|---|---|---|---|---|
| AI-1 | Subject content identity: App files and outputs (file content identity, RS L-1, method designation carried) | DEL-04-03's identity method (method unselected, RS U-04) → the control | At compose (AC-1) and at confirmation (AK-c) | Not obtainable → not offered ("the subject's content identity is not obtainable") |
| AI-2 | One or more A15 descriptors (WR-v0.1 RB-4, `a15_descriptor`; L-4: one per entry), each with: descriptor identity; subject (the target revision); bound content (the reviewed draft's content identity, equal to the revision's, WR ID-2); reviewed draft {draft, content}; prior revision or none; scope and purpose per library; and its **withdrawal** when the live draft or the slot changes (RB-3) | DEL-02-02 → the control (DEP-01-04-009, held) | A15 offers are composed only from a current descriptor | No descriptor → not offered; descriptor withdrawn or draft changed → AC-6 stale, nothing captured |
| AI-3 | Arrival and request references: the arrival {checkpoint, arrival ordinal} and run, the RS `act_request` record | DEL-02-03 (recorder) / DEL-04-03 (record-out) → the control (NR-2 proposed) | Only when the person opens the control from an arrival row or a request | Absent → the offer is a standing act; nothing is inferred |
| AI-4 | Act wording, record kinds, act class | DEL-04-01 → the control (DEP-01-04-011, admitted) | Every offer | — |
| AI-5 | Identity sources: the name set in the App (this control's setting, §7), the operating-system account, the Codex account as reported | The App; DEL-01-05 (NR-3 proposed) | Each capture | A source not available is absent; at least the operating-system account is always present |
| AI-6 | Report of the capture {A15 record identity, capture-evidence reference, descriptor identity, bound content}; DEL-02-02 then registers exactly those bytes and reports the outcome | The control → DEL-02-02 (K-8; WR §7, G-0) | A15, after capture and record | §4.2 |
| AI-7 | RS entries `human_act`, `act_declined` | The control → DEL-04-03's writer (DEP-01-04-012, held) | After capture (and for A15 after registration) | RS §14: late write, "record write failed" |
| AI-8 | The act record, observed by the checkpoint recorder | DEL-04-03 record → DEL-02-03 (AE-2: "Direct capture through the App act control") | When the act answers or counts at an arrival | DEL-02-03's §2.6 A-7, A-8 |

---

## 3. States (one transition table per offer)

| ID | From | Event | Guard | To | Record left |
|---|---|---|---|---|---|
| AX-01 | — | compose(kind, subject, scope, purpose[, arrival][, request]) | Kind served (§1.2); subject identity obtainable | **AC-1 composed** | The offer (not a record) |
| AX-02 | — | compose | Kind not served, or identity not obtainable | (refused) | Nothing; the reason is shown |
| AX-03 | AC-1 | present | The host shows the offer in its native confirmation (§6.2) | **AC-2 presented** | — |
| AX-04 | AC-2 | operate(source ≠ native confirmation) | — | AC-2 (unchanged) | Nothing; "not operable from ‹source›" returned to the caller (CAP-4) |
| AX-05 | AC-2 | dismiss | — | **AC-5 dismissed** | Nothing |
| AX-06 | AC-2 | act / decline | Subject identity now ≠ the offer's, or (A15) **any** entry's bytes changed or its descriptor withdrawn (RB-3; L-4) | **AC-6 stale** | Nothing; "content changed since it was shown" / "the workspace withdrew the A15 descriptor": review it again |
| AX-07 | AC-2 | decline | Kind has no decline (A15) | AC-2 (unchanged) | Nothing; "no decline for A15; close the control instead" |
| AX-08 | AC-2 | act | Identity equal; kind ≠ A15 | **AC-3 captured** | Capture evidence |
| AX-09 | AC-2 | decline | Identity equal; kind has a decline | **AC-4 declined** | Capture evidence (choice *decline*) |
| AX-10 | AC-2 | act | Identity equal; A15; descriptor current | **AC-3 captured**, then recorded (AX-12), then reported to DEL-02-02 (§4.2) | Capture evidence |
| AX-11 | AC-7 (A15) | registration not completed | DEL-02-02 reports failure for one or more entries | **AC-9 recorded; registration not completed** | The A15 record stands; each failed entry carries outcome "not completed: ‹reason›", each completed entry its revision; DEL-02-02's ledger says which had no effect |
| AX-12 | AC-3, AC-4 | record written | W-1 succeeded | **AC-7 recorded** | `human_act` or `act_declined` citing the capture |
| AX-13 | AC-3, AC-4 | record write failed | W-1 failed | **AC-8 record pending** | Capture evidence; the writer holds the entry |
| AX-14 | AC-8 | late write | W-2 succeeded | AC-7 | The entry, in order, then "record write failed" (RS FC-1) |
| AX-15 | (relaunch) | recovery | A capture whose record is in no log | AC-7 | The entry, written late (AC-R1) |

Not in the table, and so refused: any transition started by an arrival, a
request, a rule or a timer; a capture from AC-1 (an offer not presented); a
second capture from one offer; any record without capture evidence (RS HA-1).
The prototype exercised AX-01…AX-15 (§8).

---

## 4. Operating sequences, with failure behaviour

### 4.1 An act on App content (A4, A6, A7), standing or at an arrival

| Step | Action | By | Record | Failure: what fails · who reports · record · next |
|---|---|---|---|---|
| 1 | The person opens the control (AK-a) and chooses kind and subject; or opens it from an arrival row (SD-3; NIR PD-5), which carries the arrival's declared kind, subject, scope and purpose | Person | — | — |
| 2 | Compose: the host reads the subject's content identity and composes the offer from authoritative sources (never from agent-supplied text) | Host (R17-5) | — | Identity not obtainable · the control · nothing · not offered |
| 3 | Present in the host-owned native confirmation (§6.2) | Host | — | — |
| 4 | The person confirms *act* or *decline*, or dismisses | Person | — | Dismissed · — · nothing · AC-5 |
| 5 | Re-read the identity; compare with the offer | Host | — | Changed · the control · nothing · AC-6, "review again" |
| 6 | Capture evidence (§5.2), actor per §7 | Host | Capture evidence | The capture store cannot be written · the control · nothing captured · the person is told; nothing counts (RS HA-1) |
| 7 | Write `human_act` (*direct capture*) or `act_declined` through DEL-04-03's writer | Host → DEL-04-03 | RS entry | Write fails · the writer · capture kept, entry pending · late write with "record write failed" (RS FC-1); the display shows *missing in record* until written (AS §6) |
| 8 | The checkpoint recorder observes the record (AE-2); `act_counted` / `act_not_counted` / `arrival_declined` are DEL-02-03's | DEL-02-03 | Its entries | DEL-02-03 §2.6 A-8 |

### 4.2 Registration of a reviewed draft, A15 (K-8)

Aligned with DEL-02-02's WR-v0.1 §4.3 (RB-1…RB-5), §5.2 and SQ-G (node D5).

| Step | Action | By | Record | Failure: what fails · who reports · record · next |
|---|---|---|---|---|
| 1 | The person reviews the draft; DEL-02-02 shows the review package and, for a registrable disposition, hands the control an `a15_descriptor` (RB-2, RB-4); the draft is *under review* (NIR §7) | Person; DEL-02-02 | WR's `registration_disposition`, `a15_descriptor` | A refusing disposition (for example *refused: name taken*, K-6) · DEL-02-02 · *registration refused* · no descriptor, so no offer |
| 2 | The person opens the control on the draft, or on several reviewed drafts at once (L-4) ("Register…"); the offer holds one entry per current descriptor, each with: subject the target revision, bound content the reviewed draft's content identity, reviewed draft, prior revision (or none), scope and purpose per library ("make it available in the project library" / "… in the user library") | Person; host | — | No descriptor, or the live draft's identity ≠ the reviewed content · the control · nothing · not offered |
| 3 | Present in the native confirmation; the person confirms | Person | — | Dismissed · nothing · AC-5 (WR: the attempt is *withdrawn*, nothing inferred) |
| 4 | Re-read the live draft's identity and ask whether the descriptor is still current (RB-3) | Host | — | Changed or withdrawn · AC-6 · "review again" (K-8); DEL-02-02 reports *review stale* and the view shows "changed since review" |
| 5 | Capture evidence listing every entry with `descriptorId`, `revision`, `reviewedDraft` (WR ID-3 string, content) and `priorRevision` (RS `workflowTuple` or null) (R17-11; C-01) | Host | Capture evidence | As §4.1 step 6. One entry changed or withdrawn at step 4 · nothing captured for any entry (AX-06); the person reviews again and may leave that entry out |
| 6 | Write **one** A15 `human_act` for the act: bound subject every entry's revision; bound content every entry's reviewed content identity with method; relations `reviewedDraft` and `priorRevision` for one entry, or `registeredEntries` [{subject, reviewedDraft, priorRevision}] for several, as node F's RS change (FR-06, RS-v0.9, in progress at this node) defines them; purpose; capture evidence | Host → DEL-04-03 | RS `human_act` A15 | Write fails · as §4.1 step 7 (late write; the capture is kept). The App ends before the write · on relaunch the capture is recorded late (AX-15) |
| 7 | Report the capture to DEL-02-02 {record identity, capture-evidence reference, descriptor identity, bound content} | Host → DEL-02-02 | — | The workspace is not reachable · the control · the report is repeated when it is (WR SQ-X reconciles at App start) |
| 8 | DEL-02-02 registers exactly those bytes, entry by entry (WR SQ-G G-0…G-6), and reports per entry *registered* with the A15 record and the revision, or *registration not completed* with its cause | DEL-02-02 | WR `library_entry` | Not completed · DEL-02-02 · `library_entry` *not completed* citing the A15 · the act record stands, the capture carries the outcome, the view shows "registration not completed: ‹cause›; the act is recorded and had no effect"; registering again needs a new review and a new act |

**Why record at capture (PROPOSED; agrees with WR-v0.1).** The act is the
person's decision on the reviewed bytes; it is true when the person makes it
and does not depend on the library write. ACT already keeps an act apart from
its effect (an acceptance stays recorded when its application is refused
stale, ACT §2.5; AS §8 "accepted — not applied"). RS HA-10 holds: the record
is written only from capture evidence of the person's explicit registration.
A revision in the library with no A15 record is something WR's catalog view
states (S1-C §A.4 item 9), never something this control causes.

### 4.3 A decline

As §4.1 with *decline*: capture evidence with choice *decline*, then
`act_declined` {actor, declined kind, subject, time, capture evidence, and the
arrival and request where known}. It is not an act of that kind and satisfies
nothing that requires the act (ACT §2.3; DS-5).

### 4.4 Relaunch recovery (AC-R1)

On relaunch the host reads its capture store and DEL-04-03's logs. A capture
whose record is not in any log is recorded late, in order, with its own
capture time (`observedAt`), except an A15 whose registration did not
complete. A capture is never re-made and never back-dated.

---

## 5. Data (PROPOSED; JSON Schema 2020-12)

### 5.1 The offer — [`aac.offer.schema.json`](aac.offer.schema.json)

Schema 0.2 (`urn:chirality:app-v4:del-01-04:aac:offer:0.2`): {offer
identity; act kind (A4, A6, A7, A15); the wording; for A4, A6, A7 one subject
{class, reference, content identity}; for A15 `entries` (one or more, L-4),
each {descriptor identity, subject {target revision, content identity},
`reviewedDraft` {WR ID-3 string, content}, `priorRevision` (RS
`workflowTuple` or null)} (R17-11; C-01); scope; purpose; actor requirement;
whether a decline is offered; what it answers (an arrival and run, or "no
arrival: a standing act"); the act request it answers, where one was
recorded; composed at; offer digest}. Examples:
`aac.offer.example.valid.json` (2: an A4 at an arrival; one A15 over two
entries), `aac.offer.example.invalid.json` (9 cases, among them a prior
revision as a free string, a reviewed draft not in ID-3 form and an A15 with
no entries).

### 5.2 Capture evidence — [`aac.capture-evidence.schema.json`](aac.capture-evidence.schema.json)

{capture identity `cap:…`; offer identity and digest; choice (*act*,
*decline*); act kind; actor {name set in the App, operating-system account,
Codex account; `identityVerified` false; no plan type, C-10}; bound subject;
bound content; scope; purpose; captured at; surface "App interface"; input
source "host-native-confirmation"; what it answers; request reference; for
A15 `entries`, each {descriptor identity, revision, `reviewedDraft`,
`priorRevision` and, once DEL-02-02 reports it, that entry's registration
outcome (beside the act, AK-f)}; the RS record identity once written;
evidence limits; optional *seal* (§6.3)}. Schema 0.2. Examples:
`aac.capture-evidence.example.valid.json` (1: one A15 over two entries, one
registered and one not completed), `aac.capture-evidence.example.invalid.json`
(8 cases). Where captures are
stored is not chosen (OI-014; RS U-05); a reader resolves `cap:` references
through the store (RS §9 resolution status).

### 5.3 The RS entries the control writes

| RS element (§6.1; schema `humanAct`) | From |
|---|---|
| Act kind; act class | Offer; DEL-04-01 ("reserved to the person" for A4, A6, A7; "person's act (V4-WF-02)" for A15) |
| Decision actor | Capture actor (`person`, `identityVerified` false) |
| Recorder; recording mode | Entry header recorder role "App interface (capturing surface)"; *direct capture* |
| Bound subject; bound content | Capture (A15: the revision and its identity) |
| Scope; purpose | Capture |
| Capture evidence references | [{kind "capture evidence", ref `cap:…`, resolution at write "resolved"}] |
| Capture time | Capture |
| Evidence limits | "identity not verified"; for A7, the professional standing is the person's own statement |
| Relations | Arrival answered; act request; for A15 `reviewedDraft` and `priorRevision` (one entry) or `registeredEntries` (several) (R17-11; C-01; L-4), in RS's form after FR-06. The prototype reads the RS schema it finds and writes that form; under RS-v0.8 it wrote the single `derivedFrom` string (both runs passed; §8) |

The prototype wrote 7 such entries through DEL-04-03's own writer, which
validates every entry against `RS_RECORD.schema.json` before writing; all 7
were valid (K-16).

---

## 6. Not operable by automation (CAP-4)

### 6.1 Requirements

| # | Requirement |
|---|---|
| NA-1 | No path the App exposes to Codex or its agents operates the control: no MCP tool, dynamic tool, App command reachable from a conversation, URL scheme, file drop or watched folder. The App defines none of these for acts |
| NA-2 | The offer shown to the person is composed by the capture side from authoritative sources; text an agent wrote is never the act kind, subject, scope or purpose (it may appear only as the cited request) |
| NA-3 | Capture follows only the person's confirmation in a surface the interface's scripts cannot operate (§6.2) |
| NA-4 | The capture side checks that the confirmation is for the presented offer (offer identity and digest) and that the subject's identity is unchanged (AK-c) |
| NA-5 | Records the control writes are distinguishable, on read, from bytes another process wrote into the same files (§6.3) |
| NA-6 | The control states its limits (§6.4) where the person can read them; it never claims more |

### 6.2 PROPOSED placement (R17-5; OI-008 decides)

Under R17-5 the Rust host owns record writing and produces act capture from a
native interface event. Three ways to obtain the person's confirmation:

| Option | Confirmation surface | Against interface scripts | Against other local processes | Cost |
|---|---|---|---|---|
| P-1 | A button in the webview; the host checks an offer token | **Weak**: a script running in the webview can press it | As P-2 | Least |
| **P-2 (PROPOSED)** | A native confirmation the host owns and fills from the offer (for example a native dialog the host opens; whether Tauri 2's dialog facility is used is an implementation choice, not verified here): the act wording, subject and its identity, scope, purpose, the arrival or "standing act", and the buttons | **Holds**: the webview can ask the host to present an offer but cannot press the native buttons or change their text | A process of the same user that is granted macOS Accessibility control could press them (platform behaviour, inference) | Small |
| P-3 | P-2 plus an operating-system presence check (password or biometric) for each act | Holds | Holds against automation without the person's presence | One more step per act |

P-2 is PROPOSED for every kind. **P-3 is not adopted (DECISION-L L-5: no OS
password or Touch ID check per act now);** it stays recorded as an option a
later decision may take up. The
interface may show the offer in the webview too, for reading; only the native
confirmation captures.

### 6.3 Record provenance

| Option | What the reader can tell | Cost |
|---|---|---|
| SEAL-1 | Nothing beyond the file's content: a same-user process that can write the log could write a line that looks like a direct capture | None; the limit is stated |
| **SEAL-2 (PROPOSED)** | The capture side holds a per-installation key in the operating system's protected key store, available only to the signed App, and adds a *seal* over the capture evidence and over each entry it writes; the reader reports "capture not verifiable" for an entry without a valid seal | Key handling; a reader rule in DEL-04-03 (join J-R4) |

SEAL-2 is about where a record came from, not who the person is: K1-4's
"identity not verified" stands, and a verified identity stays a
governance-phase matter. The capture-evidence schema carries the optional
*seal* element at 0.1; the prototype does not implement it.

### 6.4 Limits that no placement removes (stated, not hidden)

- The person's tool-permission and sandbox settings are their own (D3). With
  a sandbox setting that lets an agent write anywhere the user can, an agent
  could write into the App's files; SEAL-2 makes such writes detectable, not
  impossible.
- A process granted Accessibility control by the person can operate native
  buttons (inference from platform behaviour); P-3 closes this for the acts
  it covers.
- The person is recorded from what the App observes (§7); "identity not
  verified" is always on the record.

---

## 7. The person's identity (CAP-8; DECISION-K1 K1-4)

| Source | How the App reads it | When absent |
|---|---|---|
| The name set in the App | A setting of this control ("Your name on acts you record"), stored in the App's own data; shown on every offer. **Assigned here** (S1-B O-04-4 left the home open; INTEGRATION, open to the integrator) | Absent from the record; the person is asked to set it on first use but may decline |
| The operating-system account | The account name of the user running the App, read by the host at capture | Always present |
| The Codex account, when Codex reports one | Read through DEL-01-05's account state (NR-3), originally Codex `account/read`: for a ChatGPT sign-in the reported email, or "ChatGPT account (no email reported)" when none is reported; no plan type (R18-1 C-10); for an API-key account nothing identifies a person; not signed in, nothing | Absent; never guessed. The account is that of the App-owned home running the conversation (K-1; L-1). **OBS-2 O-6 (filled in part):** each home reports its own account; a second home sharing the first's configuration reported `null`. A signed-in account is not observed (DECISION-L L-6) |

Every record carries `identityVerified` false and the evidence limit
"identity not verified". The answer submission of a request card uses the
same three sources to form its actor reference (NIR §4.5), so the register's
`person-via-interaction` origin and the act record name the person alike.

---

## 8. Verification

"Needs" as NIR §13.1. The prototype checks are in
`prototype/run_cases.py` group K and ran on 2026-10-01 and again on 2026-10-02 for v0.2 (all pass, model).

| Case | Expected | Needs | Prototype |
|---|---|---|---|
| VC-AAC-01 Kinds | A4, A6, A7, A15 offered; A12, A5, A13 not, each with its reason | model | K-1 pass |
| VC-AAC-02 Offer format | An A4 offer at an arrival with its request is valid | model | K-2 pass |
| VC-AAC-03 Automation refused | Operation from an agent tool, an MCP operation, an App rule, a supplier request or a webview script: refused, nothing captured | model; candidate with P-2 for the real surface | K-3 pass (5 sources) |
| VC-AAC-04 Positive capture (EXEC CH-23 (ii); NIR VC-NIR-16) | The person's confirmation captures A4 at an arrival; the RS `human_act` is *direct capture*, recorder ≠ actor, arrival and request cited, valid against RS's schema | model; **person** and candidate for the VER-005 positive case | K-4, K-6 pass (model) |
| VC-AAC-05 Presenting answers nothing | A question waits in the register while the person acts; it is still waiting | model | K-5 pass |
| VC-AAC-06 Decline | `act_declined`, valid against RS's schema | model | K-7 pass |
| VC-AAC-07 Stale binding | The file changes after the offer is shown: nothing captured | model | K-8 pass |
| VC-AAC-08 A15 | Offered only from a current descriptor; no decline; captured, recorded, then registered; capture valid with `reviewedDraft`, `priorRevision` | model; DEL-02-02's registration (D5) | K-8a, K-9…K-11 pass |
| VC-AAC-09 A15 registration fails; descriptor withdrawn | The act record stands and the outcome is reported beside it; a withdrawn descriptor captures nothing | model | K-12, K-12a pass |
| VC-AAC-10 Write failure | Capture kept; late write in order; "record write failed" | model (RS writer) | K-13, K-14 pass |
| VC-AAC-11 Relaunch recovery | A capture whose record was never written is recorded late | model | K-15 pass |
| VC-AAC-11a Dismiss; second capture | Dismissing records nothing; a second confirmation of a recorded offer is refused | model | K-5a, K-5b pass |
| VC-AAC-09b Several entries (L-4) | One changed entry makes the whole offer stale; two current entries: one capture, one RS record naming both, each entry's outcome beside it | model | K-12b, K-12c pass |
| VC-AAC-12 All entries conform | Every RS entry the control wrote is valid | model | K-16 pass (9 entries at v0.2) |
| VC-AAC-13 Native confirmation | A script in the webview cannot complete a capture; the native confirmation shows the offer's own text | candidate | Not run |
| VC-AAC-14 Provenance | An entry written by another process without a valid seal is reported "capture not verifiable" | candidate; DEL-04-03 reader rule | Not run (SEAL-2 not implemented) |

## 9. UNRESOLVED

| Item | Owner | Point of need | Effect |
|---|---|---|---|
| U-AAC-1 OI-008: placement of capture (P-2 under O-1) | App implementation owner (phase review) | Before architecture production contracts | §6.2 PROPOSED |
| U-AAC-2 *Closed (DECISION-L L-5):* no per-act OS check now | — | — | P-3 not adopted |
| U-AAC-3 SEAL-2 and its reader rule | App implementation owner with DEL-04-03 | Before act-control implementation | PROPOSED; J-R4 |
| U-AAC-4 *Closed (R18-1 C-22):* record at capture, registration after, outcome beside the act, as WR | — | — | §4.2 |
| U-AAC-5 Home of "the name set in the App" | Integrator | Node F | Assigned here |
| U-AAC-6 Codex account of a signed-in home | DEL-01-05; observation only with a new owner answer (L-6) | Before act-control implementation | §7: O-6 filled in part |
| U-AAC-7 Contract standing | Owner, through SCA-V4-003 | The amendment node | PROPOSED until SC2-01-04-1 (as amended, SC3-01-04-1) is carried |

## Changes

- v0.2 (D round 2, 2026-10-02): see "Changes from v0.1".
- v0.1 (D round 1): first version.
