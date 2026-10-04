# App act control

- Contribution: DEL-01-04/AAC-v0.3 (supersedes AAC-v0.2, last changed at
  `31d65b0be3`, sha256 062ce28c8a4ec0bc79fc6b6c421245057a59815df14b88fa779b61eeb98be7d7;
  AAC-v0.2 superseded AAC-v0.1, committed at
  `63a6e0fa47`, sha256 7e98118c774fcd9c3e60f04e7def51b3a11325995ae343426fba892ea439e181).
  Companion: [NATIVE_INTERACTION_RECEIVING.md](NATIVE_INTERACTION_RECEIVING.md)
  (DEL-01-04/NIR-v0.3), whose header records the basis, the inputs (round 1
  and round 2) and their sha256; they are not repeated here.
- **Standing: PROPOSED until SCA-V4-003 carries SC2-01-04-1** (R17-6). The
  obligation is not in DEL-01-04's ScopeOfWork (sha256 0cdb44e2…, NIR L-1);
  DECISION-K1 K1-4 directed that it be proposed for the next amendment, and
  the owner's pass-3 direction and DECISION-K3 (K-8) start its design now. This
  file amends SC2-01-04-1 for K-8 (A15, DEL-02-02 as consumer): proposal
  SC3-01-04-1 in the return file `D/D3.md`.
- **v0.3 change (R23-8, R23-18, R23-21; run `APP-V4-DESIGN-PASS-4-20261003`, owner O-A):** A16 *decide* on a decision package: §1.2 row, §2 AI-9 (the package as a runtime value), and both §5 schemas with their examples (A16, the alternatives, `alternativeChosen`; additive, in place in schema 0.3); §5.1 names the offer digest's serialization (`aac-offer-digest/0.1`). **Re-pin (R23-5):** DEL-01-04 ScopeOfWork.md now has sha256 8434cc47ec28e1397e7dae548183543567f0b5fcfdefaebc0b44bc1f709aacf3 (SCA-V4-003 applied SC3-01-04-1, so the act control's obligation is now REQ-008/OUT-005/AC-008/VER-008, and the "Standing" bullet above is historical). Blocks read: G-0104-01…14. Bearing: G-0104-04, -09, -10, -12 and -14 (OUT-005, REQ-008, AC-008, VER-008 and the matrix row: "one act kind at a time on App content", "App files and outputs"; a decision package is an App file, so A16 falls within them), G-0104-08 (REQ-006: acts owned elsewhere) and G-0104-13 (AX-005); the others do not bear on this row.
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
| RV21 (repairs from V21; in place, no version step) | R21-3 (V21-A M-1; V21-B M-3); V21-A MINOR 1, 2, 3; V21-B m-11 | §1.2 A15 row; §2 AI-2, AI-7; §3 AX-06; §4.2; §4.4; §5.1–§5.3; §8; both schemas (0.3) and their examples; `prototype/act_control.py`, `prototype/run_cases.py` | **M-1/M-3 (R21-3):** an A15 offer is composed from exactly **one** DEL-02-02 descriptor, WR's `a15_descriptor` (one reviewed draft, `draft:`) or `a15_multi_descriptor` (L-4: two or more library entries registered in place, `entry:`, no prior revision), with the entries inside it; the reviewed-content pattern is RS-v0.9's `^(draft\|entry):(project\|user):[^@]+@.+$`; the wording gains "register workflow revisions" for the multi descriptor; v0.2's reading of L-4 as "several reviewed drafts at once" is withdrawn (several drafts are several acts, AK-d). New cross-check K-17 runs WR-v0.2's own two descriptor examples through the offer and the capture into RS's writer, and K-17b checks RS's L-4 act-log example (record 4, capture `cap:reg-in-place-2`) against the capture format. **MINOR 1:** A15 is recorded at capture like every kind; the two contrary phrases (AI-7, §4.4) are deleted. **MINOR 2:** §5.3's entry count follows the rerun. **MINOR 3:** RS-v0.9 cited as current. **m-11:** the capture's `codexAccount` takes RS's two forms exactly |

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
| A15 | "register workflow revision" (from WR's `a15_descriptor`); "register workflow revisions" (from WR's `a15_multi_descriptor`, L-4; R21-3) | **Yes** (K-8); one act is composed from **one** DEL-02-02 descriptor: one reviewed draft, or **two or more library entries registered in place** (L-4 as clarified; WR §4.7) | **No**: ACT §2.3 defines no act-declined event for A15; the person closes the control | The person | Per entry: the revision the descriptor names (WR RB-4, ME-3), bound by that entry's reviewed content identity; relations per entry: the **reviewed content** (WR ID-3 string, `draft:` for a reviewed draft or `entry:` for a library entry reviewed in place, and its content) and, for a new revision, the **prior revision** (RS `workflowTuple`; none for an entry registered in place) (R17-11; C-01). WD's *derived-from* is not this act's relation. Shipped workflows are registered by the release and entries byte-equal to a shipped revision are recognized by DEL-02-02 (L-4); neither is offered here. Several drafts are several acts (AK-d) |
| A16 | "decide" (ACT §2.1; R23-8; pass 4) | **Yes**, on one **decision package**: an App file the agent wrote, recorded as an R16 `act_request` with alternatives and consequences (RS §13.6). The package reaches the control as a **runtime value** when the person opens the control from DEL-06-02's decision view (R23-2: no register row from DEL-06-02); one package per act (AK-d) | **No**: ACT §2.1 defines no act-declined event for A16; the person closes the control or chooses an alternative the package offers | The person | The package, bound by its file content identity (AI-1; AK-c: a package changed after the offer captures nothing); the **alternative chosen**, one the package names; relation to its `act_request` entry (RS §6.1). The offer carries the alternatives with their consequences and the capture carries `alternativeChosen` (§5 schemas, AAC-v0.3 rows) |
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
| AI-2 | **One** A15 descriptor per act (R21-3): WR-v0.2's `a15_descriptor` (RB-4; one reviewed draft) or `a15_multi_descriptor` (§4.7 ME-3; L-4: two or more library entries registered in place), with: descriptor identity and kind; its entries, each with subject (the target revision), bound content (the reviewed content identity, equal to the revision's, WR ID-2), reviewed content (WR ID-3 string, `draft:` or `entry:`, and content) and prior revision or none; scope and purpose per library ("make it available …" / "make them available …"); and its **withdrawal** when a live draft or entry, or the slot, changes (RB-3, ME-4). The control maps WR's snake_case to its own spelling one to one (WD §3.6; prototype `from_wr_descriptor`) | DEL-02-02 → the control (DEP-01-04-009, held) | A15 offers are composed only from a current descriptor | No descriptor → not offered; descriptor withdrawn or any entry changed → AC-6 stale, nothing captured |
| AI-3 | Arrival and request references: the arrival {checkpoint, arrival ordinal} and run, the RS `act_request` record | DEL-02-03 (recorder) / DEL-04-03 (record-out) → the control (NR-2 proposed) | Only when the person opens the control from an arrival row or a request | Absent → the offer is a standing act; nothing is inferred |
| AI-4 | Act wording, record kinds, act class | DEL-04-01 → the control (DEP-01-04-011, admitted) | Every offer | — |
| AI-5 | Identity sources: the name set in the App (this control's setting, §7), the operating-system account, the Codex account as reported | The App; DEL-01-05 (NR-3 proposed) | Each capture | A source not available is absent; at least the operating-system account is always present |
| AI-6 | Report of the capture {A15 record identity, capture-evidence reference, descriptor identity, bound content}; DEL-02-02 then registers exactly those bytes and reports the outcome | The control → DEL-02-02 (K-8; WR §7, G-0) | A15, after capture and record | §4.2 |
| AI-7 | RS entries `human_act`, `act_declined` | The control → DEL-04-03's writer (DEP-01-04-012, held) | After capture, for every kind including A15 (AK-f; R18-1 C-22) | RS §14: late write, "record write failed" |
| AI-8 | The act record, observed by the checkpoint recorder | DEL-04-03 record → DEL-02-03 (AE-2: "Direct capture through the App act control") | When the act answers or counts at an arrival | DEL-02-03's §2.6 A-7, A-8 |
| AI-9 | A16's decision package as a **runtime value** (R23-2; no register row): the package file reference and content identity, its `act_request` record identity, act kind, scope, purpose, and the alternatives with their consequences | DEL-06-02's decision view → the control (DECISION_VIEW §5) | Only when the person opens the control from a pending package row; nothing else opens it (AK-a, AK-b) | Package file absent or changed since the request → not offered, or AC-6 stale and nothing captured (AK-c); no alternatives → not offered |

---

## 3. States (one transition table per offer)

| ID | From | Event | Guard | To | Record left |
|---|---|---|---|---|---|
| AX-01 | — | compose(kind, subject, scope, purpose[, arrival][, request]) | Kind served (§1.2); subject identity obtainable | **AC-1 composed** | The offer (not a record) |
| AX-02 | — | compose | Kind not served, or identity not obtainable | (refused) | Nothing; the reason is shown |
| AX-03 | AC-1 | present | The host shows the offer in its native confirmation (§6.2) | **AC-2 presented** | — |
| AX-04 | AC-2 | operate(source ≠ native confirmation) | — | AC-2 (unchanged) | Nothing; "not operable from ‹source›" returned to the caller (CAP-4) |
| AX-05 | AC-2 | dismiss | — | **AC-5 dismissed** | Nothing |
| AX-06 | AC-2 | act / decline | Subject identity now ≠ the offer's, or (A15) the descriptor withdrawn or **any** entry's bytes changed (RB-3, ME-4; L-4) | **AC-6 stale** | Nothing; "content changed since it was shown" / "the workspace withdrew the A15 descriptor": review it again |
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

Aligned with DEL-02-02's WR-v0.2 §4.3 (RB-1…RB-5), §4.7 (ME-1…ME-6), §5.2 and SQ-G (R21-3).

| Step | Action | By | Record | Failure: what fails · who reports · record · next |
|---|---|---|---|---|
| 1 | The person reviews the draft, or picks two or more library entries without a registration record (WR §4.7 ME-1, ME-2); DEL-02-02 shows the review package and, for a registrable disposition, hands the control **one** descriptor: an `a15_descriptor` for the draft (RB-2, RB-4) or an `a15_multi_descriptor` for the entries (ME-3); a draft is *under review* (NIR §7) | Person; DEL-02-02 | WR's `registration_disposition`; the descriptor | A refusing disposition (for example *refused: name taken*, K-6) or an entry refused by hygiene · DEL-02-02 · *registration refused* · no descriptor (or the entry left out), so no offer for it |
| 2 | The person opens the control on the draft, or on the reviewed library entries ("Register…"); the offer is composed from the one descriptor and holds its entries (one for a draft; two or more for library entries in place, L-4), each with: subject the target revision, bound content the reviewed content identity, reviewed content (`draft:` or `entry:` string, WR ID-3), prior revision (or none; always none in place), with the descriptor's scope and purpose per library and its wording, "register workflow revision" or "register workflow revisions" (R21-3) | Person; host | — | No descriptor, or a live draft's or entry's identity ≠ the reviewed content · the control · nothing · not offered |
| 3 | Present in the native confirmation; the person confirms | Person | — | Dismissed · nothing · AC-5 (WR: the attempt is *withdrawn*, nothing inferred) |
| 4 | Re-read every entry's live identity and ask whether the descriptor is still current (RB-3, ME-4) | Host | — | Changed or withdrawn · AC-6 · "review again" (K-8); DEL-02-02 reports *review stale* and the view shows "changed since review" |
| 5 | Capture evidence naming the descriptor (`descriptorId`, `descriptorKind`) and listing every entry with `revision`, `reviewedDraft` (WR ID-3 string, content) and `priorRevision` (RS `workflowTuple` or null) (R17-11; C-01; R21-3) | Host | Capture evidence | As §4.1 step 6. One entry changed or the descriptor withdrawn at step 4 · nothing captured for any entry (AX-06); the person reviews again and may leave that entry out |
| 6 | Write **one** A15 `human_act` for the act: bound subject every entry's revision; bound content every entry's reviewed content identity with method; relations `reviewedDraft` and `priorRevision` for an `a15_descriptor`, or `registeredEntries` [{subject, reviewedDraft, priorRevision}] for an `a15_multi_descriptor`, as RS-v0.9 §6.1 and its schema define them (HA-10; `reviewedDraft.draft` admits `draft:` and `entry:`); purpose; capture evidence | Host → DEL-04-03 | RS `human_act` A15 | Write fails · as §4.1 step 7 (late write; the capture is kept). The App ends before the write · on relaunch the capture is recorded late (AX-15) |
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
capture time (`observedAt`), for every kind including A15 (AK-e, AK-f). A
capture is never re-made and never back-dated.

---

## 5. Data (PROPOSED; JSON Schema 2020-12)

### 5.1 The offer — [`aac.offer.schema.json`](aac.offer.schema.json)

Schema 0.3 (`urn:chirality:app-v4:del-01-04:aac:offer:0.3`; RV21, R21-3; 0.2
had one descriptor per entry): {offer identity; act kind (A4, A6, A7, A15);
the wording; for A4, A6, A7 one subject {class, reference, content identity};
for A15 the **one** descriptor it is composed from {`descriptorId`,
`descriptorKind` `a15_descriptor` · `a15_multi_descriptor`} and its
`entries`, each {subject {target revision, content identity},
`reviewedDraft` {WR ID-3 string, `draft:` or `entry:`, content},
`priorRevision` (RS `workflowTuple` or null)} (R17-11; C-01): an
`a15_descriptor` has exactly one entry in the `draft:` form and the wording
"register workflow revision"; an `a15_multi_descriptor` has two or more
entries in the `entry:` form, none with a prior revision, and the wording
"register workflow revisions" (L-4); scope; purpose; actor requirement;
whether a decline is offered; what it answers (an arrival and run, or "no
arrival: a standing act"); the act request it answers, where one was
recorded; composed at; offer digest}. Examples:
`aac.offer.example.valid.json` (3: an A4 at an arrival; an A15 from one
`a15_descriptor`; an A15 over two library entries from one
`a15_multi_descriptor`), `aac.offer.example.invalid.json` (16 cases, among
them a prior revision as a free string, reviewed content not in ID-3 form, an
A15 with no entries, several entries with the singular wording, an
`a15_descriptor` with two entries, a `draft:` entry under the multi
descriptor, no descriptor, and 0.2's per-entry descriptor).

**AAC-v0.3 additions to the offer.** A16 (§1.2): one package as `subject`,
its `requestRef`, its `alternatives`, each with its consequences, the wording
"decide" and no decline. Examples: the fourth valid instance and INV-OF-17…19.

**Offer digest (AAC-v0.3; PROPOSED; from the isolated reader's finding in
run `APP-V4-DESIGN-PASS-4-20261003`, E/RR-E, and RV E1-R4).** Method
designation `aac-offer-digest/0.1`. `offerDigest` is the sha-256, in
lowercase hex, of the UTF-8 bytes of the offer **without** its `offerDigest`
member, serialized as JSON as follows:

- **Objects.** Members are sorted by key in code-point order. The offer's keys
  are all ASCII schema names, so code-point and UTF-16 order agree.
- **Separators.** `,` and `:`, with no whitespace outside strings. Arrays keep
  their order.
- **Strings.** `"` and `\` are escaped. U+0008, U+0009, U+000A, U+000C and
  U+000D are written as `\b`, `\t`, `\n`, `\f` and `\r`. Other characters
  below U+0020 are written as `\u00xx` with lowercase hex. **Every other
  character is written as itself**, including non-ASCII, U+007F, and U+2028
  and U+2029; none is `\u`-escaped.
- **Numbers.** Only integers occur in an offer (the schema has no
  non-integer number). They are written in decimal, with `-` for a negative
  value and no `+`, leading zeros, fraction or exponent.
- **Literals.** `true`, `false` and `null`.
- **Non-integer numbers.** The method is not defined over a non-integer
  number. An offer containing one is not offered.

This is the prototype's `nir_model.canonical()`. It is not claimed to be RFC
8785, and no equivalence with it was checked. Any reader can recompute the
digest from the offer file alone.

The A16 example carries ü, ≈ and U+2028 in a consequence. The run folder's
`E/run_e.py` recomputes that digest with an implementation written from this
text (not Python's `json`), and gets the same value; it also checks integer
serialization on the A4 example's `arrivalOrdinal`.

Until a canonicalization is selected for the project (DEL-03-01 TBD-003; RS
U-04), this is the AAC's own TEST VALUE method. The earlier examples' digests
stay labelled "illustration" and are not recomputable.

### 5.2 Capture evidence — [`aac.capture-evidence.schema.json`](aac.capture-evidence.schema.json)

{capture identity `cap:…`; offer identity and digest; choice (*act*,
*decline*); act kind; actor {name set in the App, operating-system account,
Codex account in RS's two forms only (the reported email, or "ChatGPT
account (no email reported)"; RS `$defs/person`; V21-B m-11);
`identityVerified` false; no plan type, C-10}; bound subject; bound content;
scope; purpose; captured at; surface "App interface"; input source
"host-native-confirmation"; what it answers; request reference; for A15 the
descriptor (`descriptorId`, `descriptorKind`) and `entries`, each {revision,
`reviewedDraft`, `priorRevision` and, once DEL-02-02 reports it, that
entry's registration outcome (beside the act, AK-f)}, with the same rules per
descriptor kind as the offer; the RS record identity once written; evidence
limits; optional *seal* (§6.3)}. Schema 0.3
(`urn:chirality:app-v4:del-01-04:aac:capture-evidence:0.3`; RV21). Examples:
`aac.capture-evidence.example.valid.json` (2: one A15 from an
`a15_descriptor`, registered; one A15 over two library entries in place, one
registered and one not completed), `aac.capture-evidence.example.invalid.json`
(12 cases, among them a Codex account in a form RS refuses and 0.2's
per-entry descriptor). Where captures are
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
| Relations | Arrival answered; act request; for A15 `reviewedDraft` and `priorRevision` (an `a15_descriptor`) or `registeredEntries` (an `a15_multi_descriptor`) (R17-11; C-01; L-4), in RS-v0.9's form. The prototype reads the RS schema it finds and writes that form; under RS-v0.8 (round 2's first run) it wrote the single `derivedFrom` string (§8) |

At the RV21 rerun the prototype wrote 11 such entries through DEL-04-03's own
writer, which validates every entry against `RS_RECORD.schema.json` before
writing; all 11 were valid (K-16; 9 at round 2 and RX2).

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
`prototype/run_cases.py` group K and ran on 2026-10-01 and again on 2026-10-02 for v0.2 (all pass, model); rerun at RV21 (2026-10-02, `results/RUN_2026-10-02_RV21.txt`): all pass, with K-12b…K-12d rewritten for one multi descriptor and K-17, K-17b new.

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
| VC-AAC-09b Several library entries in place (L-4; R21-3) | One `a15_multi_descriptor`: one changed entry makes the whole offer stale; two current entries: one capture, one RS record naming both (`registeredEntries`, `entry:` strings), the plural wording, each entry's outcome beside it; a multi descriptor with one entry is not offered | model | K-12b, K-12c, K-12d pass |
| VC-AAC-15 WR → AAC → RS cross-check (R21-3) | WR-v0.2's own `a15_descriptor` and `a15_multi_descriptor` examples, valid against WR's schema, compose valid offers and captures and an RS entry valid against RS's schema, with wording, descriptor, purpose and reviewed content unchanged; RS's L-4 act-log example (record 4, capture `cap:reg-in-place-2`) has capture evidence in this format and the control writes the same relations from it | model | K-17, K-17b pass |
| VC-AAC-12 All entries conform | Every RS entry the control wrote is valid | model | K-16 pass (11 entries at RV21; 9 at v0.2) |
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

- RV21 (repairs from V21, 2026-10-02; in place, no version step): R21-3, V21-A MINOR 1–3, V21-B m-11; row "RV21" in "Changes from v0.1".
- v0.2 (D round 2, 2026-10-02): see "Changes from v0.1".
- v0.1 (D round 1): first version.
