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

## Freeze exact maintained pre-run inputs

`pre_run_inputs.py` is a separate technical preparation helper. It validates the
unchanged B7 plan, captures the fixed source basis and full canonical EXP support
selection, and binds all 13 explicit maintained fixture roles by exact bytes.
It introduces no EXP sidecar, dossier schema, result record or ready state.
Historical preparation and canonical source locks remain unchanged.

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
