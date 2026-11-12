# data-app-spec: method

## 1. Intake and framing

Recover the human's purpose and the application boundary:
- who uses the app;
- which questions it answers and which decisions it informs;
- what it must not be relied on for.

Classify the app against the archetypes in the ontology (`ONTOLOGY.md` §7). Most apps
combine two or three. Each archetype contributes its authoring questions to stages 3 to 5.

Propose a consequence tier with its grounds:
- what a wrong result would cause and for whom;
- how detectable a wrong result is;
- who is accountable for reliance.

The tier decides the reviews (`gates.md`). It is the human's ruling, not the agent's
conclusion.

Inventory sources and their permitted use:
- domain documents;
- data sources and licences;
- a reference app and its source, if any.

Record what each can support. In `derive` mode, establish what observation is
authorised: initial HTML only, live interaction, a source request, or execution of
the reference code. A missing permission limits the specification; it does not
license guessing. Also ask for the default fidelity policy (reproduce as observed, or
correct known weaknesses). Individual departures from it are ruled before freeze (§8).

**Checkpoint A.** Present:
- purpose, users, questions, decisions and non-uses;
- archetypes;
- the proposed tier and its grounds;
- mode and scope;
- the source basis and its limits;
- the approach to authoring and examination.

Record the human's words and the agent's separately identified interpretation in
`SPEC_RECORD.md`.

## 2a. Design (`new` and `revise` modes)

The design record (`formats/app_design.linkml.yaml`; DESIGN_ONTOLOGY.md explains it)
captures what the app is for before anything is specified. Build it with the human, in
the human's terms. An illustrative or agent-proposed need is marked as such; it is never
presented as the human's.

### 2.1 Elicit by perspective

Ask the four questions of the thesis (Framework §3.2) about the app. They correct one
another, so return to earlier answers when a later one changes them.

| Perspective | Ask | Record |
|---|---|---|
| Ontology | What is the app about? Which things, which properties, which data exist, on what terms? | `Actor`, `Subject`, `PropertyOfInterest`, `DataHolding` with availability and access |
| Epistemology | What do the users need to find out? What would support an answer: which criteria, methods, parameters? | `InformationNeed` in the asker's words, with its task; `KnowledgeNeed` |
| Praxeology | What do users do with the answers, in what order? Which decisions do they inform, among which alternatives? What lies outside the app? | `Activity` with steps; `Decision` with `app_role` and `outside_the_app`; `Alternative` |
| Axiology | What matters, to whom? Which obligations bind, and which preferences can be traded? What would a wrong answer cost, and how detectable is it? | `Concern`, `Obligation`, `Preference`, `ErrorConsequence`, `TierProposal`, `NonUse` |

Before going further, ask the two screening questions the design study methodology
draws from its pitfalls:
- Could the problem be automated, with no app at all?
- Do existing tools already serve it well enough?

Either answer can end the undertaking. Identify the front-line analyst and the gatekeeper
early (actor roles `front_line_analyst` and `gatekeeper`).

Rules:
- Record the human's words verbatim in `intent` and the interpretation separately.
- Give each need a `basis` warrant that says how it was found: the owner's words,
  observation of the work, an existing artefact, or the agent's inference. Users do not
  reliably introspect about their own needs (F §3.3), so combine interviews with
  observation where the tier warrants it.
- Record each need's task as facets (DESIGN_ONTOLOGY.md §4). For an evaluative need,
  state its interpretation: what counts as met or missed.
- Do not invent needs, users, decisions or obligations. Where something is unknown,
  record a gap with its consequence.
- A decision's `app_role` is at most `recommend`, and only under a made ruling that
  adopts the recommendation logic. The app never decides.
- Obligations govern what can be accepted. They are not traded against preferences.

### 2.2 Propose options

For each need, decision and activity, propose at least one option, usually as an
application of a catalogue pattern whose task subspaces contain the need's task facets. Where a consequential trade-off exists, propose two
and state each one's strengths, weaknesses and prerequisites. The checks:
- a pattern's `applies_when` holds for the data;
- the pattern addresses the need's task;
- its pitfalls are named in the option where they apply.

When no pattern fits, propose a new one in the catalogue with `standing: PROPOSAL`, the
note "not observed in the corpus", and its grounds. Report it to the catalogue
maintainer, as schema gaps are reported.

### 2.3 Settle the authoring questions

Each chosen pattern lists the questions a design must settle: the hidden semantics that code
otherwise settles silently. Answer each with grounds, or record a gap
that says who can answer it. An agent may propose answers. A judgment the human or an
accountable professional must make stays a gap until a ruling answers it.

### 2.4 Sketch

Produce a low-fidelity sketch from the proposed layout: one group per activity step, in
order, with each element labelled by the need it answers. The sketch is for the human's
review; it is not the layout's authority.

### 2.5 Design checkpoint

Run `tools/check_design.py` on the design record and the catalogue. Compute each
proposed ruling's digest with `check_design.py --digest` and put it in the record
before presenting. Then present:
- the coverage table (need, task, pattern, choice and its category, answering elements);
- the answers that need a domain expert's or the professional's ruling, with that
  person's role, presented to that person;
- the options with their trade-offs, and the proposed choices;
- the authoring-question answers and the gaps;
- the tier proposal, the non-uses and the obligations;
- the sketch.

Record the response (contract), and transcribe the rulings it makes into the design
record with `decided_by` and `evidence`. A ruling binds only what its scope names and
only with its own authority; the owner's ruling does not answer a question the design
assigns to the professional of record. Choices the human returns go back to
2.2. A design need not be settled before domain knowledge and binding begin, but the
candidate for checkpoint B is compiled only from choices recorded as ruled. A draft
compiled from proposed choices may inform the design checkpoint; it is labelled as a
draft.

## 2b. Reference inventory (`derive` mode)

Assign one bounded TASK per reference app, or per large module of one. The inventory
records every element under ontology headings:
- controls, views and data sources;
- transforms and analyses with their parameters;
- domain knowledge, provenance and validation;
- exports, layout and navigation, reactivity, performance and error handling.

Each finding is labelled observed (app HTML, source at a pinned revision),
documented (the author's material), inferred, or TBD with what would resolve it.

The inventory also lists two things a specification must state:
- what the UI does not show: hidden constants, ordering rules, rounding,
  empty states;
- candidate known-answer tests with their sources.

Defects found in the reference become fidelity decisions, not silent corrections.
Related apps that share ids or data are context, not evidence of the target's
behaviour.

When live observation is authorised, observe the app's complete rendered state, not only
what it computes:

1. **Every widget whole.**
   - For a chart: the full figure, including layout shapes, annotations, legends and axes, as
     well as its data traces. A probe that reads only traces will miss threshold bands and
     legends drawn in the layout.
   - For a map: every layer's style, the legend and the layer-control groups.
   - For a table: pagination (including whether it shows when everything fits on one page),
     search, sorting, the column set under each filter, and how cells display dates,
     times and numbers.
2. **Every state.** Capture the default, representative selections, and the empty, sparse,
   failing and inverted-input states. Record the viewport size observed, and how each
   area's height behaves at that size (fills the window, fixed, or sized to content).
3. **The reference's own data.** Where the app offers a download or export, take it. Then
   reconcile it to the primary source row by row, recording:
   - the rule that reproduces it (station and variable selection, QC filter, units,
     time-zone handling, precedence among duplicates);
   - the residual differences.
4. **Reproduce before specifying.** Reproduce every observed computed output from the
   evidence before writing the method down. The author's documentation is evidence and can
   contradict the app's behaviour; record any contradiction as a fidelity decision.
   - When outputs do not reproduce, test the dependency versions current when the
     reference was built before concluding the method differs.
   - Check whether row order or ties affect the result. If they do, the data product
     preserves the order the result depends on.
5. **Name captures as evidence.** Keep every capture under a stable name, and cite it from
   the `basis` entries that rely on it.

## 3. Domain knowledge

Run `domain-knowledge-intake` for the knowledge the app needs. Examples:
- criteria with their editions;
- methods with assumptions and applicability;
- parameter tables with row-level grounds;
- definitions and caveats.

Reuse an accepted pack where its scope covers the need. The specification
references the pack by identity and copies only the items it uses into its
`domain` section.

## 4. Analysis binding

Run `analysis-binding` for each computation the app performs beyond the closed
transform vocabulary. Each binding returns:
- a component registry entry (interface plus pinned implementation, or a
  specification for a new component);
- parameter values with grounds;
- preconditions with user-facing messages;
- explicit result semantics;
- known-answer tests.

## 5. Author the specification

In `new` and `revise` modes, compile the candidate from the design choices recorded as
ruled (a draft may use proposed choices, labelled as a draft):
- each settled answer becomes the elements its `realized_by` names;
- each need's `answered_by`, each alternative's `realized_by` and each non-use's
  `disclosed_by` are completed as the elements are written;
- the specification states again only what the builder needs (intended use, non-uses,
  tier), and those statements must match the design record (rules D-SYNC1 to D-SYNC3).

Write the specification in ontology terms. A useful order:
1. data sources and their contracts (schema, units, CRS, licence, vintage);
2. transforms;
3. analyses from the bindings;
4. metrics;
5. for decision support: objectives, levers, alternatives and scenarios;
6. state variables;
7. controls and interactions;
8. views;
9. layout;
10. content, exports, the provenance policy and the verification plan.

Keep implementation choices in the build profile.

State layout sizing: the viewport sizes the app is specified for (in `derive` mode, at
least the reference's), and how each tab or area's height behaves at them. Without it, a
builder picks a height, and content can clip at a size the tests do not check.

Where the schema has no slot for a value a test needs, such as a marker stroke or dynamic
heading text, put the value in the element's `description`. Then declare in a resolved gap
that such prose is binding, so the suite author can derive tests from it.

For each archetype, settle its authoring questions. For example:
- `spatiotemporal_map`: CRS, time step with calendar semantics, interpolation
  method and variance, colour-domain policy over time.
- `decision_support`: objectives, alternatives, the status-quo definition, the
  consequence table, assumptions and the limits of the tool's role in a social choice.

Ground consequential elements (`basis`). Mark scoped standing where useful. When
something is unknown, record a gap with its consequence rather than a plausible
value. Prepare proposed rulings for consequential choices, but leave the decision
to the human.

When the schema cannot express a need, write it as a visible `x-` extension. Then
report it to the ontology maintainer as a schema gap, with the example that needs
it. Builders must not rely on extensions, and a specification depending on one is
not buildable for that part.

Do not record the agent's recommendations as extensions, for example a recommended option
on a fidelity decision. Under the builder input contract's P5, an extension on a built
element makes the builder refuse. Present recommendations to the human as proposed
rulings instead.

## 6. Validate

Run the structural validator (JSON Schema of the bound release) and the semantic
validator on the canonical form. In `new` and `revise` modes, also run
`tools/check_design.py` with `--spec`: every need, decision, alternative, knowledge
need and non-use must trace to specification elements, and no view may lack a need
unless the design record lists it as supporting. Repair errors. Then review:
- warnings;
- open gaps;
- undecided fidelity decisions, and selections whose ruling is not yet made;
- placeholders;
- extensions.

Report the buildability verdict with its reasons. A structurally buildable
specification is not thereby correct, adequate or accepted.

## 7. Examine and repair

Give a separately prepared examiner:
- the frozen candidate;
- its sources and inventories;
- the domain pack and bindings;
- the original directions;
- the scope.

In `new` and `revise` modes, also give the design record and the catalogue entries it
uses. Do not give only the author's summary. The examiner's focus:
- fidelity to the sources and, in derive mode, to the reference;
- coherence of departures;
- unsupported claims;
- flattened uncertainty: a TBD, assumption or conflict that became settled prose;
- unit and CRS consistency;
- interaction and scenario semantics;
- whether the known-answer tests can distinguish correct from defective behaviour;
- in `new` and `revise` modes:
  - whether each need is actually answered by the elements it traces to;
  - whether an authoring answer became settled without its grounds;
  - whether a choice labelled presentation or routine changes meaning;
  - whether an answer that is a domain or professional judgment was assigned to the
    owner;
  - whether an obligation counted as addressed is in fact met, or still needs a human
    act at acceptance.

In `derive` mode, the examiner also:
- compares each element with the named captures, including chart layout, legends and
  empty or error states;
- recomputes every number that a fidelity decision's or gap's consequence states, since
  the human rules on those statements.

Walk representative user scenarios from question to view through the
specification. Use the review categories of `software-prd` (Incorrect,
Unsupported, Missing, Flattened, Outdated, Incomplete) and add the domain reviews
the tier requires. Repair within authority, backcheck changed elements, and
present remaining findings without ruling them.

## 8. Lock, freeze and accept

Before freezing, obtain the human's rulings on every departure the agent recommends,
such as a fidelity decision it would correct. A ruling deferred to checkpoint B forces a
second freeze if it changes the build.

Resolve every pinned asset, dataset, data product manifest, component bundle,
pack and template expansion into `appspec.lock` with hashes. Then freeze:
1. Produce the canonical `appspec.json` by parsing the authoring form with the validator's
   own parser. YAML 1.1 and 1.2 resolve some scalars differently; for example, `1e-12` is a
   string under 1.1.
2. Assert that every value is a JSON scalar.
3. Check that the canonical form is equivalent to the authoring form.
4. Validate the canonical file itself, parsed as JSON.

`tools/freeze_candidate.py` does all four, writes the lock with every member's size and
hash, and writes the manifest the contract describes. It refuses to overwrite an existing
candidate.

Then present checkpoint B:
- the identified closure;
- validation output and buildability;
- review account and remaining findings;
- open gaps;
- proposed accepted portions and constraints;
- the proposed next use.

Write the decision snapshot from the human's response (contract).

A specification finding raised after acceptance, by the suite author, the builder or an
examiner, returns here in `revise` mode:
1. Classify it: settled by the specification on a closer reading; a material ambiguity
   that changes what a user sees or what a number means; or immaterial.
2. A material finding gets the smallest evidence-grounded amendment, frozen under a new
   candidate id. The predecessor and its acceptance record are preserved.
3. A focused recheck covers the changed elements and confirms by diff that nothing else
   changed.
4. A new checkpoint B follows. Acceptance of the predecessor does not carry over to new
   bytes.

## 9. Hand off

Return:
- the `HANDOFF_STATE.md` path;
- exact identities;
- acceptance scope;
- review coverage;
- open work;
- the proposed next undertaking.

Two routes are possible:
- **`data-app-build`.** Use it when every component bundle, data product and builder
  capability the specification uses exists. An agent builds the app and the
  conformance tests decide.
- **`software-decomp`.** Use it when new components, data products or builder
  capabilities are needed. WORKING_ITEMS decomposes them, and the app is built once
  they exist.

Do not start either without the human's direction.

## Interruption and recovery

Before a pause, retain:
- the candidate, sources and inventories;
- explicit decisions;
- completed contributions;
- open findings and the next proposed work.

Cite actual locations. On return, inspect the files and current instructions
before relying on the handoff. New sources, a changed reference deployment, a new
domain-pack edition or a later human decision may invalidate part of the
preparation. Re-open only the affected elements. Preserve unaffected examination
evidence where the change does not touch what it rests on.

A partial specification can be returned with its coverage stated. It is not an
accepted specification of the uncovered remainder.
