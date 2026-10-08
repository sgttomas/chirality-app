# Standalone case preparation

From `projects/chirality-app-v4/app`, using Python's standard library only:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 examination/standalone/prepare.py prepare > /tmp/standalone-plan.json
PYTHONDONTWRITEBYTECODE=1 python3 examination/standalone/prepare.py check /tmp/standalone-plan.json
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'group_b_standalone*test.py' -v
```

The output is a machine-readable **preparation**, not an SQ dossier or EXP
result. It preserves the accepted map's 23 ordered steps (21 counted),
file-qualified supplier cases, five stimuli, action/observation text, native
route requirements, preconditions and run insertion points. RUN-A contains
V4-EXM-10 and V4-EXM-11; RUN-B has the same still-unfilled candidate slot.
The invented inventory rows are input material for future substantive tool
work and new-input reuse; no workflow is authored or registered by this tool.

`source_basis_revision` identifies inspected source only. A build identity,
qualification pin, runtime configuration, person-operated native journey and
candidate-applicable supplier evidence remain unsupplied. The missing-input
list describes this preparation's entry, not a live discovery of external
systems. Historical Group A evidence supplies no new candidate outcome.

`check` compares the complete preparation with its regenerated, hash-bound
basis. It fails closed on changed sources, altered order/counting, omissions,
substitute routes, fabricated readiness/results and extra fields, including
`examination_opened`. A successful check means only preparation fidelity.
This deliberately strict checker accepts no future executed dossier: use the
accepted SQ/EXP schema and rules for that separate artifact. Updating this
preparation requires a reviewed source-basis update, not editing an output to
claim readiness. Source locks identify the actual supplier files read here;
they do not adopt revisions beyond SQ's historical design pins.

Before the examiner declares the actual pre-run case definition, bind actual
invented workflow/collision bytes and fixtures, receive the named inputs,
identify one executable candidate and configuration, and retain ST-5's real
candidate-pin capture as required rehearsal evidence for its part only.
ST-1…3 cannot use replay; ST-4 needs its identified delegation route or the
required counterpart. The integration owner opens the examination separately.
Every planned case then gets an honest EXP result, including unattempted ones,
and later review/handoff follows SQ. No native launch, account operation,
download, signing, SEAL-2 implementation or product qualification occurs here.

CC-SQ-J2-ST4 reconciles the former J-2 prose/map discrepancy by including the
already required ST-4 in J-2's machine map. This consumer explicitly adopts that
independently reviewed correction; the source lock and generated preparation
retain its revision and bytes. No examination outcome follows from the correction.
