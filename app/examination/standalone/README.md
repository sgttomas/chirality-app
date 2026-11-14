# Standalone case preparation

From `projects/chirality-app-v4/app`, using Python's standard library only:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 examination/standalone/prepare.py prepare > /tmp/standalone-plan.json
PYTHONDONTWRITEBYTECODE=1 python3 examination/standalone/prepare.py check /tmp/standalone-plan.json
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'group_b_standalone*test.py' -v
```

The output is a machine-readable **preparation**, not an SQ dossier or EXP
result. It preserves the accepted map's 36 ordered steps (34 counted),
file-qualified supplier cases, five stimuli, action/observation text, native
route requirements, preconditions and run insertion points. RUN-A contains
V4-EXM-10 and V4-EXM-11; RUN-B, RUN-J1 and RUN-J2 have the same still-unfilled
candidate slot. The journey steps J1-1…J1-6 and J2-1…J2-7 cite their governing
acceptance criteria instead of supplier cases, mark the J2 sessions and the
steps performed at the act control, and the preparation's
`journey_record_requirements` states what each attempted journey step and
journey must say: who operated it and by what means, what was done outside the
App's controls, what the App's window did not give, what the examination could
not perceive or operate, and any intervention. J1-4 and J2-7 carry planned
parts that each keep their own outcome and need native evidence; J1-4, J1-5 and
J2-7 name the observations their outcome rests on (the changed file, and the
two byte comparisons for each run-start turn), each with its expected result.
The invented inventory rows are input material for future substantive tool
work and new-input reuse; no workflow is authored or registered by this tool.

A build identity,
qualification pin, runtime configuration, person-operated native journey and
candidate-applicable supplier evidence remain unsupplied. The missing-input
list describes this preparation's entry, not a live discovery of external
systems. Historical Group A evidence supplies no new candidate outcome.

`check` compares the complete preparation with its regenerated, hash-bound
basis. The step map (`../sq_receiving/sq.step-map.json`), the per-step action
and observation cells (`step-operations.json`) and the local missing/invented
input JSON are the exact inputs listed in `sources.terms-v1.json`. It fails
closed on changed inputs, altered order/counting, omissions,
substitute routes, fabricated readiness/results and extra fields, including
`examination_opened`. A successful check means only preparation fidelity.
This deliberately strict checker accepts no future executed dossier: use the
accepted SQ/EXP schema and rules for that separate artifact. Updating this
preparation requires a reviewed source-basis update, not editing an output to
claim readiness.

Before the examiner declares the actual pre-run case definition, bind actual
invented workflow/collision bytes and fixtures, receive the named inputs,
identify one executable candidate and configuration, and retain ST-5's real
candidate-pin capture as required rehearsal evidence for its part only.
ST-1…3 cannot use replay; ST-4 needs its identified delegation route or the
required counterpart. The integration owner opens the examination separately.
Every planned case then gets an honest EXP result, including unattempted ones,
and later review/handoff follows SQ. No native launch, account operation,
download, signing, SEAL-2 implementation or product qualification occurs here.

## Freeze exact maintained pre-run inputs

`pre_run_inputs.py` is a separate technical preparation helper. It validates the
unchanged B7 plan, captures the fixed source basis and full canonical EXP support
selection, and binds all 13 explicit maintained fixture roles by exact bytes.
It introduces no EXP sidecar, dossier schema, result record or ready state.
Executable helpers, canonical support sources and all maintained fixture roles
are captured by exact byte identity.

From `app/`, first generate the ordinary plan, calculate its exact file digest,
and supply that digest explicitly:

```sh
python3 -B examination/standalone/prepare.py prepare > /private/tmp/b7-plan.json
shasum -a 256 /private/tmp/b7-plan.json
python3 -B examination/standalone/pre_run_inputs.py freeze \
  --plan /private/tmp/b7-plan.json --plan-sha256 <exact-plan-sha256> \
  > /private/tmp/b7-inputs.json
shasum -a 256 /private/tmp/b7-inputs.json
python3 -B examination/standalone/pre_run_inputs.py check \
  --plan /private/tmp/b7-plan.json --selection /private/tmp/b7-inputs.json \
  --selection-sha256 <previously-frozen-selection-sha256>
```

The fixed role list identifies WORKFLOW.md and tally.py for revisions 1/2/3 and
the same-name collision example, plus initial/reuse/refinement/duplicate-negative
CSV inputs. All required roles must remain exact; missing/extra fields, duplicate
keys, changed identities, different bytes and additional fixture companions
refuse. Source changes require a reviewed pin update. No fixture code executes.
Descriptors read files without following links; symlink components, traversal
and nonregular files refuse. Use real paths such as `/private/tmp`, not a
symlink alias. Digests establish file correspondence, not external provenance.

The helper runs existing preparation and support readers against an exact
captured source snapshot and removes its scratch copy afterward. The selected
support tuple is **preparation source correspondence only**: it is neither proof
of producer use nor SQ/native result-consumer adoption. Null candidate fields
and the complete existing missing-input list are preserved, including its
historical entry wording; the helper does not reinterpret it as live readiness.
The original `invented-inputs.json` remains context; explicit CSV roles identify
the actual selected test bytes without silently rewriting that context.

J-1 still begins in an empty project. The maintained fixtures are examiner
examples for later drafting, not a replacement for the person's plan, draft
trial, review or A15. Nothing is installed or registered. A changed actual draft
cannot pass this fixed selection and requires a fresh exact case-definition
binding under the examiner's later scope. This is preparation for that work,
not the final pre-run case-definition declaration or an opened examination.

The connected form wrapper is documented in `../native_forms/README.md`.
Run the maintained offline checks with:

```sh
python3 -B -m unittest discover -s tests -p 'group_b_pre_run_inputs_test.py' -v
```

## The examination table

`table.py` prints every planned step of a release for one named candidate, its latest outcome as the result records
for that candidate state it, and, kept apart, the scripted driver's runs and the session comparison's rows. Its
docstring gives what it reads and how. Its claim (App Agent 0, 14 November 2026): a step prints as passed only when a
result record for that step, on the candidate named, says passed, and no other record for that step on that
candidate of the same latest date says otherwise, every record for that step on that candidate can be placed in
time, and no record that could bear on any step (one naming no step, or one that cannot be read at all) remains;
every other state prints as what it is; cited rows are listed
beneath the table and never raise, lower or protect an outcome or a count; the driver's runs and the comparison's rows
are never counted as steps.

The table accepts one written form for a time, `YYYY-MM-DDTHH:MM:SS` with an optional fraction of a second and its
zone, and a calendar date `YYYY-MM-DD`, and refuses the rest, because a time read wrongly can make an older pass beat
a later failure.

A record that cannot be read is never less damaging to a pass than a readable failure would have been. The doubt it
carries reaches as far as what it could be (App Agent 0, on the INTERLOCUTOR's finding):
- **Another candidate, readably named.** It bears on nothing here.
- **A step named, but not placed.** On the candidate named but with a date that cannot be placed in time, or naming no
  candidate (it cannot be shown to be another's): that step's outcome is not known. The step prints and counts as
  inconclusive, whatever its other records say, and the reason is printed directly under the counts.
- **No step named, or not readable at all** (not JSON, not a JSON object; a truncated failure record, say). It may bear
  on any step, so while one remains no pass is established. A row whose records say passed prints as inconclusive,
  saying that a record that could not be read may bear on it, and counts as inconclusive. Failed, blocked, not run and
  inconclusive rows stay as they are, and every row and its readable evidence still print. A step with no readable
  record does not say it was not run: it says that no readable result is recorded and that a record that could not be
  read may bear on it, and it is still counted as not run (App Agent 0, from the INTERLOCUTOR). The counts line itself says
  how many such records there are and how many passes they hold.

Nothing else is relied on to confine that doubt: not a file's name, and not any part of content that failed to read.

**What releases a table held this way** is resolving each such record, never deleting it to clear an inconclusive
result. The person who keeps the results does one of two things for each record:
- reads what the record was and writes a corrected record beside it, keeping the original as it is; or
- establishes that the record does not belong to this set of results and moves it out of the folder, noting why.

Removing a readable failure record is something the table cannot see.

**What the table trusts.** The table trusts the identities a record states. A record that readably names another
candidate, or a step the plan does not know, is listed beneath the table and lowers nothing. The table does not
establish that whoever wrote the record named them correctly, nor that every record made is in the folder. Only
`.json` files directly in the results folder are read. A record that names no candidate or no step is different: its
relevance is unknown, which is why it is treated as in the rule above.

Limits:
- Citations are listed only for the records that decide a shown step.
- A malformed comparison header or driver report can still stop the whole print. Then nothing is printed on stdout,
  and stderr says "THE TABLE WAS NOT PRINTED: " and why, with exit status 3.
