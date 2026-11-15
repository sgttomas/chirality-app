# The 0.160.0 to 0.167.0 comparison

`0.160.0-to-0.167.0.json` is the result of comparing what the App relies on in
the supplier's generated schema, and the recorded exchanges, between Codex
0.160.0 and 0.167.0. `0.160.0-to-0.167.0.dispositions.json` holds the 51
authored decisions it rests on, one for each change it found. Both are
evidence, kept as files. They are not regenerated.

## How it was made

By `app/supplier_checks/version_advance.py` as it stood at commit 40518eb5 of
this repository, which is not in the maintained tree and is not maintained. At
that commit the file regenerates byte for byte. The tool classified nothing:
it listed every relied-on definition, and every definition one reaches by
reference, as unchanged or changed, and each change needed a decision by a
named decider naming exactly that change. The decisions were made by reading
the App's consumers at the lines each entry cites, in `app/src-tauri/src` and
`app/src` outside tests, at revision 4bb28164; a later change to those
consumers is not covered by them.

## What independent readings established

These are what the file may be cited for. They are readings by reviewers who
did not write the tool, not the tool's own verdict.

- The review of pull request 234 at e491f9ed regenerated the result byte for
  byte, followed the references from the relied-on roots independently and
  found the same 331 reached definitions with the same 39 changed or added,
  and read every difference against the production consumers: of the 58
  decisions then, none was to be moved or withdrawn.
- The review of pull request 249 at 40518eb5 regenerated this file byte for
  byte, repeated the reference walk with the same counts, and found the 51
  findings to be those 58 less the seven that concerned the `st5-race`
  scenario, with every other identifier unchanged, each decision naming one
  finding once, and the three corrected evidence wordings agreeing with the
  code.

## What is not established

- **The word "passed" in the file is not relied on.** The second review showed
  eight ways in which the tool admitted an input it had not read in full: the
  generation record's health fields; the matching of replies to requests, a
  missing begin event and the harness's own contrary readings; a production
  module gated `#[cfg(all(not(test), ...))]` read as a test module, and a
  linked source folder skipped; a method's params given as `allOf` not
  followed, and a null definition read as absent; the inside of a distribution
  record, and two absent digests read as equal; an exception applied wider
  than its reason; conflicting or malformed manifest rows dropped; a present
  file holding `null` read as an absent one. So "passed" means that this tool
  found these 51 changes in these inputs and each has a decision. It does not
  mean the inputs were whole, and it does not mean no other change exists.
- **The relied-on set is derived heuristically**, from protocol method names
  written as string literals in the host source outside what the tool took for
  test code. A name built at run time is missed. A supplier surface the host
  never names is outside the set and invisible (the supplier's remote control
  methods and its status notification are an example). Three responses could
  not be mapped by name; the first review found their definitions unchanged
  between these pins.
- **Two of the eight bear on what the relied-on set contains, and were looked
  for in the inputs this file was made from.** In `app/src-tauri/src` at
  commit 40518eb5, a search for `cfg(all(` on a line that also holds
  `not(test)` finds nothing, and the folder holds no symbolic link. Of the 63
  relied-on methods, the only ones whose params are not a bare reference are
  `account/logout` and `configRequirements/read`, and both are `{"type":
  "null"}`, with no definition behind them. Those are searches of that source
  and of the two bundles, stated as what was searched; they are not a proof
  that the tool misread nothing else.
- **The recorded evidence at each pin is established up to each scenario's
  last required reply and no further**, as the note beside the recordings
  says. The 0.160.0 recordings carry no socket observation.
- It is not qualification of a pin (DEL-01-01 AC-011), and it says nothing of
  how the supplier behaves inside a real model turn.

## How it is used

`supplier_checks/same_basis.py` admits a pin whose generated files are
byte-identical to 0.167.0's. For such a pin this comparison and its decisions
carry over, because the basis is the same bytes; nothing else about the
supplier carries over with them.

`supplier_checks/test_version_advance_evidence.py` checks only that the two
files agree with each other.

## Remaining item

An advance to a supplier release whose generated schema differs cannot be
admitted by `same_basis.py`, and no general comparison is maintained. One
would have to be built to this rule before such an advance: a result only from
inputs each bound to the supplier identity it claims and each read in full,
which means admitting every record whole against a closed shape, reading
configuration gates in the host source as the compiler does or refusing what
it cannot read, and following every form a schema can take to reach a
definition.
