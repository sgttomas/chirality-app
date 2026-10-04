# Reader brief — EU-F1, input set IS-FX-RP1-2

You are an isolated reader. Your job is to read one decision package from its files, as the person
who must decide it would, and answer fixed questions about it. You are testing whether the files
let a decision maker see what is being decided, on what evidence, and what is missing.

## What you may read

Only the files listed in `IS-FX-RP1-2.input-set.sha256`, which are beside this brief. Check each
file's sha256 against that list before you start, and report any mismatch. Do not open any other
file, repository, web page or tool output, and do not use what you may know about the project
from elsewhere. If the files do not answer a question, say so; do not fill the gap from outside.

The input set is a fixture. Its supplier evidence is illustrative (copied from schema examples),
and nobody has decided anything. You do not decide anything either, and you must not describe any
act as performed unless a file records it.

## What you write

One JSON file, `account.json`, valid against `rp.reader-account.v2.schema.json`. For each question
Q-1…Q-12 give:

- `fields`: the structured answers, using exactly the values the schema allows;
- `statement`: one or two sentences in your own words;
- `sources`: the input-set paths you relied on.

Add `issues` for anything in the files that a decision maker would find confusing, contradictory,
missing or misleading. Leave it empty if there is none. Also fill `reader` and `input_set`.

## Questions

- **Q-1 The decision.** Who decides it (`decider`)? What is the package's identity (`package_id`)?
  What act kind does it request (`act_kind`)?
- **Q-2 The candidate.** What revision does the package name for the candidate (`subject_revision`,
  copied exactly)? What do the files say about the App candidate of the joined local-host journey
  (`joined_journey_app_candidate`)? Is one candidate established across both obligations
  (`reconciliation`)?
- **Q-3 The core-loop obligation** (the first replacement condition). For each of the seven
  elements, what status does the packet give (`elements`)? What is the obligation's status
  (`obligation`)? Is it established as evidence for replacement (`established`)? Which scenarios
  does the packet set outside the core loop (`outside_scenarios`)?
- **Q-4 The journey obligation** (the second replacement condition). What is its status (`status`)?
  Is P20-A counted as a completed witness (`counts_as_completed_witness`)? How many acceptance acts
  are cited (`acceptance_acts`)? Is there an independent review record (`independent_review`)?
- **Q-5** Is the replacement evidence complete (`replacement_evidence_complete`)?
- **Q-6 What is missing.** List the packet's gap identities (`gap_ids`), the deliverables named as
  suppliers of those gaps (`gap_supplier_deliverables`, as `DEL-nn-nn`), and whether practitioner
  validation is listed as one of the gaps (`practitioner_validation_is_a_gap`).
- **Q-7 The alternatives.** For each alternative the package names, say whether v3.0.1 remains the
  fallback (`v3_0_1_remains_fallback`), whether choosing it would also be a public-release act
  (`also_a_public_release_act`), and whether it retires anything (`retires_anything`).
- **Q-8 Current standing.** What is the decision's state (`decision_state`)? Is any owner act
  recorded (`owner_act_recorded`)? What is v3.0.1's status now (`v3_0_1_status`)?
- **Q-9 Practitioner validation.** What is its standing (`standing`)? Is it a condition for
  replacement (`is_replacement_condition`)?
- **Q-10** What does the packet say it never establishes (`never_established`)?
- **Q-11 Continuity.** Does the thesis identity match (`thesis_identity`)? Was the fallback's
  identity re-checked against the remote release (`fallback_identity_remote_rechecked`)? Are the
  continuing-obligation dispositions supplied (`continuing_obligations`)? Is consumer adoption
  status supplied (`adoption_status`)?
- **Q-12** What is the evidence standing of the whole packet (`evidence_standing`)?

## Your return

Return `account.json` and a short note on any file you could not use, any check that failed, and
anything you were tempted to infer but did not.
