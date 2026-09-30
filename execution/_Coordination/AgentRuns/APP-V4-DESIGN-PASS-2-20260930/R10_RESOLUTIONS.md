# R10 rulings — on the disagreements returned by the alignment wave

Integrator: HELP_HUMAN. Inputs: the five return files in [WAVE_A/](WAVE_A/)
(part 3 of each). R9 stands except R9-2's second bullet, corrected by R10-1.
Labels as in R9.

## R10-1 R9-2 corrected: a direct application at a "proposal queued" checkpoint — DERIVED

Four executors returned the same point, and they are right. R9-2's second
bullet said the checkpoint's disposition "stays *act not performed*" and that
its act "is still requested". Both are wrong for this case:

- "Act not performed" is not one of the six shared disposition words (WD
  §4.3.4: waiting · performed · resolved negatively · lapsed · not reached ·
  unknown).
- In FX-C9 / PC-24 / V-CP1 / XF-25 the checkpoint's reached-when is kind (c),
  *proposal queued*. When the host applies directly, no proposal is queued,
  so the run never reaches the checkpoint.

**R9-2's second bullet now reads:** when the active grant lets the host apply
directly, no proposal arises and the host may apply. A checkpoint whose
reached-when is *proposal queued* is then **not reached**: nothing is
requested by reason of an arrival that did not occur, no A5 is forced, and
none is recorded. The record shows the direct application under the person's
grant. V4-HI-42's request clause applies to a checkpoint the run reaches:
where a checkpoint of any kind **is** reached while a grant permits direct
application, its act is requested and its disposition is *waiting*
("reached; act not yet recorded") until the person performs it.

Every file that carries R9-2's earlier words is reworded to this: ACT §4.4
and P-05; C §3.1 rule 3 and V-CP1; P §4.4 and E-2; ADAPTER §5.3 and XF-25;
LOOP C-6, FX-C9 and G-9 (closed); PANEL PC-24; CA wherever it repeats it.
"Act not performed" may stay as plain description only where it is not
presented as a disposition.

## R10-2 "Constraint not carriable on this host": which phase — INTEGRATION

The label is a record fact in either phase. In the current phase it says that
the expected governing constraint could not be carried and was recorded only
(ADAPTER GC-4, P §3.3). It bears on a hold-support value only in the
governance phase. RS R11 and U-19 drop the "governance phase" restriction and
say this; P and ADAPTER stand.

## R10-3 Which act fields a read result carries — DERIVED

DEL-03-01's ScopeOfWork (CLM-002) has C consume the DEL-04-03 act field set.
C §6.2 therefore refers to the whole set of RS §6.1 and does not define a
subset; any fields it lists are examples.

## R10-4 ADAPTER §11 "Expect from DEL-09-06 / RELAY" — DERIVED

ADAPTER cites SWBPIPE's answers, which are held in DEL-09-06's folder, as
data about the host. That is a citation of a host record, not a contribution
from DEL-09-06. The row is reworded as a citation. No register row is
proposed, and no arc toward DEL-09-06 arises (the DAG-003 guard on reverse
arcs into SCC-002 stands).

## R10-5 A host read that lacks workspace identity or generation — carried to Wave B

C §5.2 rule 1 and ADAPTER RD-2 disagree, and R8-12 item 6 decides only the
subject-identity part. It is decided in Wave B with the catalog interface
(node B3). Both texts stay, each with a note pointing at the other and at
this item.

## R10-6 The two ADAPTER evidence limits that RS R11 does not list — carried to Wave B

"Resubmission without prior observation" and "App-restart interruption" are
decided with the record's writer and failure sequences (node B4). Both texts
stay; RS §10 already states the gap.

## R10-7 "On negative decision", element absent — DERIVED from DECISION-4

Nothing stops a run in the current phase. WD §4.3.1 and EXEC §4.8 NG-2 are
labelled by phase as LOOP §2.4 already is: in the current phase the agent
follows the plan it worked out with the person; in the governance phase, for
a governed checkpoint, the run stops at the checkpoint. In both phases the
run is never recorded as if the act were positive.

## R10-8 Reached-when kind (b) on a message-form output — carried to Wave B

WD gains the element that designates a message as a declared output (node
B1), and EXEC's App-side table uses it (node B2). Until then LOOP §2.4.1's
sentence stands with a note that WD does not yet define the designating
element.

## R10-9 May a checkpoint require a network-destination grant — INTEGRATION

Not in this increment. A checkpoint's "grant setting" subject is an
operation-class grant only (WD §4.3.1, §4.3.6; EXEC §4.10 say so explicitly).
ACT ND-A1 already says an operation-class grant grants no destination; the
converse is stated beside it. A checkpoint on a network-destination grant is
recorded as a possible later extension, PROPOSED, with no definition.

## R10-10 A declared, malformed held-actions element (V6 m-7) — INTEGRATION

Governance phase only. The conservative default (HS-5, "at least one
App-side step") applies to any declared held-actions element that does not
show host operations only, whatever the checkpoint kind. No new failure row.
R7-3's derivation for an **absent** element on an A5 or kind (a) checkpoint
is unchanged.

## R10-11 Smaller items

- **EXEC §1 "I-1…I-7"** stays: I-8 and I-9 originate in EXEC, so it does not
  "consume" them.
- **WD D-1** (the sentence the executor added at WD §4.3, resting on R5-1 and
  R8-11 item 3): accepted.
- **CA §8.2 against EXEC RT-11** (CH-20 under W14-05; CH-9 under W14-07): the
  consumer's list governs which supplier cases it builds on. EXEC RT-11 is
  aligned to CA, provided each cited case contains what CA takes from it; if
  one does not, it is returned, not forced.
- **WD §8 examples for DEL-09-06** follow CA's actual use (E1, E1c, E1d, E8).
- **RELAY sub-question count:** the executor's stated composition (nine)
  stands; V6 m-3's "ten" is not adopted.
- **R9-4 applied to "record and show the destination per turn"** (SETTLED by
  OWNER_ITEMS O-10) in CA and XT: accepted; the same label is applied in the
  sibling files that still say "DECISION-2 reading".
- **Sibling section citations:** one pass over all 15 files checks every
  cross-file section or ID citation against the siblings' Wave A text.
