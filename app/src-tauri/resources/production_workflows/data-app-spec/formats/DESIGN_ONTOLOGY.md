# Application design ontology (0.1)

- **Formal source:** [`app_design.linkml.yaml`](app_design.linkml.yaml).
- **Generated schemas:**
  - [`app-design.schema.json`](app-design.schema.json) for design records;
  - [`app-patterns.schema.json`](app-patterns.schema.json) for pattern catalogues.
- **Catalogue:** [`patterns.yaml`](patterns.yaml).
- **Checker:** [`../tools/check_design.py`](../tools/check_design.py), with its mutation tests
  [`../tools/test_check_design.py`](../tools/test_check_design.py).
- **Worked example:** [`../examples/gw-review.design.yaml`](../examples/gw-review.design.yaml)
  and the specification compiled from it,
  [`../examples/gw-review.appspec.yaml`](../examples/gw-review.appspec.yaml). Its intent
  is illustrative.

The worked example tests expressibility only (thesis
`docs/thesis/CHIRALITY_FRAMEWORK.md` §1).

## 1. What it is for

The application-family ontology ([ONTOLOGY.md](ONTOLOGY.md)) says what an app
specification contains. When an existing app is reproduced, the reference app supplies
the design: which views, which controls, in which order. When a new app is created,
nothing supplies it. Someone has to decide what the app is for and turn that into
specification elements.

The design ontology is the level above. It records:
- who needs to find out or decide what, about which subjects, from which data, and with
  what consequence;
- the reusable design knowledge (patterns) that connects kinds of need to specification
  elements;
- the options considered, the choices made, and on whose authority;
- a trace from every need to the specification elements that answer it.

The two documents have different jobs:

| Document | Question it answers | Basis for | Read by the builder? |
|---|---|---|---|
| Design record (`AppDesign`) | Does the specified app answer the needs? | Validation, and the human's design checkpoint | No |
| Specification (`AppSpec`) | Does the build conform? | Verification, the conformance suite and the build | Yes: it is the single contract |

Keeping the design record out of the builder's reach preserves the single contract. Any
meaning the build needs must be in the specification. The design record explains why
the specification has that shape.

## 2. Why this layer is needed

Three findings point to it:
- **Hidden semantics.** Reproducing existing apps shows that most of what a specification
  must say is invisible in the interface: baselines, estimators, rounding, non-detect
  rules, status-quo definitions. In a new app nobody has
  made those choices yet. Someone must ask them.
- **Valid but wrong.** LLM-generated specifications fail mostly by being valid and wrong,
  through plausible assumptions. Spec Kit's response is to mark "[NEEDS CLARIFICATION]"
  instead of guessing (https://github.com/github/spec-kit/blob/main/spec-driven.md). The authoring questions
  and design gaps here are the same move, made structural.
- **Judgment stays with persons.** An agent may record and propose design judgments but
  not originate them (thesis Framework §2.5; Chapter 5 §5.5). So a choice needs a place
  where its authority is recorded.

## 3. Structure: the four perspectives

The design problem is organised by the thesis's four perspectives (Framework §3.2). The
table's last column restates what the thesis says each perspective can expose, applied
to apps.

| Perspective | Classes | What it exposes in an app design |
|---|---|---|
| Ontology: what kind of thing is this? | `Actor`, `Subject`, `PropertyOfInterest`, `DataHolding` | Confusing users with decision makers; a property with no unit or value semantics; data assumed available that is not |
| Epistemology: what supports the answer? | `InformationNeed` (with `TaskFacets` and an interpretation), `KnowledgeNeed` | A question with no answering view; an answer resting on a criterion, method or rule nobody has supplied |
| Praxeology: how does intent become usable work? | `Activity` (ordered steps), `Decision` (with `AppRole` and what lies outside the app), `Alternative` | Views in no useful order; a decision the app silently makes; alternatives with no realisation |
| Axiology: what matters, to whom, with what consequence? | `Concern`, `Obligation`, `Preference`, `ErrorConsequence`, `TierProposal`, `NonUse` | Obligations traded as preferences; a tier with no grounds; a non-use the app never states |
| Design (the bridge) | `DesignOption`, `DesignChoice`, `SettledQuestion`, `Delegation`, `SupportingElement`, `ScopeExclusion` | A choice with no authority; a pattern used without its authoring questions answered |

The perspectives correct one another, as the thesis says. A consequence found under
axiology can demand a stronger uncertainty display under epistemology. A decision found
under praxeology can create a need nobody asked for.

The design record also uses the application-family ontology's epistemic classes,
imported rather than duplicated:
- `Claimable` (basis and standing);
- `Warrant` and `SourceReference`;
- `Gap`, `Conflict` and `Ruling`.

## 4. Tasks as facets

A need's task records what answering it asks of the user. The visualization task
literature treats this not as one label but as several independent facets. In a single
list of tasks:
- compare, identify and summarise are query actions;
- locate is a search mode;
- trend is a target.

Schulz et al. put it directly: "the same motive can be pursued through different
actions and the same action can be performed for different motives" (Schulz et al.
2013 §3.2.1). `TaskFacets` therefore records:

| Facet | Values | Source |
|---|---|---|
| `goal` | discover_explore, discover_confirm, present, enjoy, produce | Brehmer & Munzner 2013 "why"; Schulz et al. 2013 goal |
| `search` | lookup, browse, locate, explore: whether the target and its location are known | Brehmer & Munzner |
| `query` (required) | identify, compare, summarise | Brehmer & Munzner |
| `target` (required) | value, extremes, distribution, outliers, clusters, trend, correlation, similarity, topology, shape | Munzner's targets; Schulz et al.'s characteristics |
| `cardinality` (required) | single, multiple, all | Schulz et al. |
| `template` | Amar et al.'s ten analytic tasks, e.g. filter, retrieve_value, sort | Amar, Eagan & Stasko 2005 |
| `decision_stage` | intelligence, design, choice, review | Simon's stages, as used by Dimara & Stasko 2022 |
| `local_task` | monitor, verify_inputs, forecast, simulate, solve, teach | Local additions, flagged as such |

**Local additions.**
- None of the cited typologies contains *decide*. Dimara & Stasko "could not find a
  taxonomy that contains decision making as an explicit task". None appears to contain
  *monitor* either; the nearest precedents are dashboard factors.
- Schulz et al. allow a task space to be adapted for a domain without changing its five
  dimensions. `local_task` goes further: it is this ontology's own facet, for
  tasks the typologies lack, and it stays visible as local.
- `identify` over all items is a recorded departure. Brehmer & Munzner associate
  identify with a single target. Here a need such as "which wells exceed"
  identifies each item's status across the whole set.
- *Decide* is deliberately not a task. A decision is made by a person and recorded as a
  `Decision`. A need can only inform its choice stage (`decision_stage: choice`). This
  keeps the thesis's line between reckoning and judgment inside the vocabulary.

**Patterns.** A pattern addresses task subspaces, Schulz et al.'s compound tasks: allowed
values per facet, with unlisted facets unconstrained. A need matches when every
constrained facet takes a listed value (rule D-P1). The mutation tests showed why the
constraints matter. A map subspace that left `target` open matched a correlation
question, until its targets were listed.

**Alignments used and not used.**
- *Traceability.* GQM's chain of goal, question and metric, and GQM+Strategies' rules
  of *relevance* and *coverage*, correspond here to:
  - every need serving an activity or decision (D-N0);
  - every need being answered (D-Q1);
  - every view tracing to a need (D-V1).

  GQM+Strategies' *interpretation model* is `InformationNeed.interpretation`: what
  counts as met or missed (D-IM1).
- *Decision structuring.* A structured decision making overview separates the roles:
  "Values define desired goals and objectives, while science helps to predict how well
  different actions meet those goals and objectives" (CAKE overview). This
  grounds `AppRole` and rules D-D2 to D-D4.
  - `Concern.kind` (fundamental or means) and `Concern.measure_type` (natural, proxy or
    constructed) come from Robin Gregory's SDM slides.
  - Neither source is the SDM book, which was not read.
- *Elicitation.* The design study methodology warns that "most users do not
  accurately introspect" about their needs, and against "not identifying front line
  analyst and gatekeeper". This grounds the actor roles `front_line_analyst`
  and `gatekeeper`, and the screening checks in data-app-spec method §2.1.
- *Not adopted.*
  - Draco's weighted soft constraints rank single-view designs, and its task facet has
    only `value` and `summary`. The catalogue does not rank options
    automatically; the human chooses.
  - Bach et al.'s 42 dashboard patterns are, by their authors' statement, descriptive
    and not claims of good design. The patterns here are no stronger. They add
    authoring questions and pitfalls grounded in observed failures, and still claim
    only `PROPOSAL` standing.

## 5. Design knowledge: patterns

A `DesignPattern` connects a kind of need to specification elements. It records:
- **Addresses:** the task types it answers.
- **Applies when:** the data characteristics it needs, e.g. `spatial_points` or
  `criteria_available`.
- **Provides:** the specification elements it contributes, named by their app_family
  classes. The checker verifies that these classes exist.
- **Settles:** the authoring questions a design must answer when it uses the pattern.
  These are the hidden semantics, stated once so they can be reused. Each carries the
  evidence of why it matters, such as the corpus defect it would have prevented.
- **Pitfalls:** failures seen in the corpus, each with its grounds.
- **Alternatives and composition:** other patterns for the same need, and the patterns
  it usually combines with.

**The catalogue.** It has 23 patterns, 99 authoring questions, 14 grounded pitfalls and 28
task subspaces.
- Twenty-one patterns were derived from a survey of public data apps.
- `result_provenance` comes from provenance standards rather than the surveyed apps, none
  of which showed a "data as of" date.
- `rule_based_screening` was added for the worked example. No surveyed app applies
  adopted rules per subject.

A catalogue derived from existing apps describes what was built, not everything that
should be. New patterns enter with `standing: PROPOSAL` and the note "not observed in
the corpus".

**Archetypes, explained.** The ten archetypes found bottom-up (ONTOLOGY.md §7) become
`ArchetypeDerivation`s: recurring compositions of patterns.
- `qc_compliance` is criterion or baseline checking plus series detail.
- `decision_support` is a consequence table or composite score, with scenarios and a
  solver where needed.

An app can combine patterns that no archetype names. The worked example combines upload,
criterion check, trend test, map, detail and rule-based screening.

## 6. Rules

`tools/check_design.py` implements these rules.

| Rule | Check | Level |
|---|---|---|
| D-ID, D-REF | Identifiers unique; references resolve to the expected class | error |
| D-RUL | A ruling marked made has `decided_by` and `evidence` | error |
| D-RUL2 | A made ruling's evidence names an existing design decision record (`DESIGN_DECISION.md`) | error |
| D-RUL3 | What a made ruling's scope covers, including the gaps its choices cite, still matches the digest in its decision record, so a choice, answer or gap edited after the ruling is caught | error |
| D-RUL4 | The decision record lists the ruling under `Rulings made` and not under `Rulings returned` | error |
| D-RUL5 | A ruling that adopts a knowledge need adopts identified content: `adopted_content` has a SHA-256, and its file, where given, still matches | error |
| D-CAT | Catalogue: authoring keys unique per pattern; every provided element kind is an app_family class | error |
| D-P0 | An option's pattern exists in the catalogue | error |
| D-P1 | The need's task facets fall within one of the pattern's task subspaces | warning |
| D-TK1 | `compare` needs cardinality multiple or all (Schulz et al. §4.2) | error |
| D-IM1 | An evaluative need (confirmatory or monitoring) states its interpretation: what counts as met or missed | warning |
| D-U1, D-N0, D-K0 | Every user asks something; every need serves an activity or decision; every knowledge need is used | warning |
| D-D1 | A decision names alternatives (one of them the status quo) and concerns | error / warning |
| D-D2 | `app_role` rank or recommend names a ruling that adopts the logic or weights, by the decision makers' authority | error if none is named; not ruled until it is made |
| D-D3 | Alternatives all realised by the same element or field propose an alternative per subject, so the role must be recommend or rank | error |
| D-D4 | Every decision names a disclosed non-use; its statement must say who decides (a lexical check) | error / warning |
| D-D5 | The ruling that adopts a decision's logic names the knowledge needs (decision rules, expert judgment) that hold it | error |
| D-T0 | A tier is proposed, with error consequences as grounds | warning |
| D-DEL | A delegation cannot cover consequential choices | error |
| D-CH2 | A choice binds only under a made ruling, or for presentation and routine choices under a made delegation; a choice naming neither is an error | error |
| D-CH4 | The ruling a choice, decision, delegation or the tier cites names it in its scope | error |
| D-CH7 | Consequential choices, the tier and delegations are the owner's: a ruling with authority `delegated` cannot bind them | error |
| D-CH8 | An answer to a question the pattern marks as a specialist judgment (`default_authority`) names an authority | warning |
| D-GAP1, D-GAP2 | A gap counts as ruled around only if a made ruling names it; a question whose gap is marked resolved, with no answer written, is unaddressed | warning, and not ruled |
| D-CH3 | Every authoring question of the chosen pattern is answered or recorded as a gap; no unknown keys | error / not ruled |
| D-CH6 | An answer whose `authority` is a domain expert or the accountable professional binds only under a made ruling by that authority that names it | not ruled |
| D-GR1 | Needs and answers carry a basis: how each was found, or that it is the author's proposal | warning |
| D-T1, D-T2 | Every trace resolves in the specification, to an element id or a root path, and to a sensible class | error / warning |
| D-Q1, D-Q2 | Every need is answered by something users see | error / warning |
| D-V1 | Every specification view traces to a need or is listed as supporting | warning |
| D-DC1, D-AL1 | Every decision shows its consequences; every alternative is realised | error |
| D-O1 | A concern that informs a decision is measured, unless declared qualitative | warning |
| D-NU1 | Every non-use is disclosed, verbatim, by a specification element or `purpose.non_uses` | error / warning |
| D-K1, D-OB1 | Every knowledge need is satisfied, and every obligation addressed, by something other than placeholders, or recorded as an open gap | error / warning, and not ruled |
| D-DH1 | Available data are realised by a data source | warning |
| D-SYNC1–3 | Where both documents state a fact (tier, question wording, app id), they agree | error |

**Verdicts.**
- The design is **RULED**, **RULED WITH OPEN GAPS** (naming the blocking ones), **RULED
  WITH GAPS RULED AROUND** or **NOT RULED**, always *as recorded*.
- The trace is **COMPLETE** or **INCOMPLETE**.

**What the verdicts can and cannot show.** The checker reads records. It verifies that
a made ruling has a decision record, that the ruling's scope and authority fit what
cites it, and that nothing it covers has changed since. It cannot establish that a
person made the ruling. That rests on the decision record's response and attribution,
as the thesis separates a prohibition from the mechanism that tries to enforce it
(Chapter 6 §6.8.3). Obligations that only a human act can meet, such as
authentication, are listed as conditions of acceptance rather than counted as met. A
ruled, fully traced design is not thereby right or adequate. Acceptance is the owner's.

**What the tests show.** `tools/test_check_design.py` mutates the worked example 41
ways, and each chosen mutation is reported by the rule meant to catch it. The chosen
mutations are not an exhaustive set.

An independent examination, and then a backcheck of its repairs, found defects that
earlier versions passed:
- fake ruling evidence;
- rulings cited outside their scope;
- answers or gaps edited after a ruling;
- returned rulings marked as made;
- delegated rulings binding consequential choices;
- node-level traces evading D-D3;
- unrelated disclosures meeting D-D4;
- decision rules adopted without identified content.

All of these are now rules and cases.

**What still passes, by design or by limit:**
- An agent can write a decision record and transcribe rulings into it. The checker
  verifies consistency, not authenticity. That rests on the response and its
  attribution.
- A consequential choice relabelled routine before its ruling. The coverage table shows
  each choice's category to the human, and the examiner checks it (data-app-spec method §7).
- A specialist question answered with `authority: owner` stated explicitly. D-CH8 warns
  only when no authority is named.
- D-D4's check that the disclosure says who decides is lexical.

## 7. Consistency with the thesis

| Thesis commitment | Mechanism |
|---|---|
| Judgment stays with the person; agents extend reckoning (Framework §2.5) | Agents propose options and answers. A choice binds only under a ruling whose scope names it, and a professional judgment only under a ruling by that professional (D-CH2, D-CH4, D-CH6). Questions only a person can answer remain gaps until ruled (method §2.3). The checker reads records, so whether a person ruled rests on the decision record (§6). |
| Descriptive record versus constitutive act; an agent may transcribe but not originate a human act (Ch. 5 §5.5; Ch. 6 §6.8.3) | Rulings are made at the design checkpoint and recorded in `DESIGN_DECISION.md`. The design record transcribes them with `evidence` (D-RUL). |
| The human's words and the agent's interpretation stay distinct | `IntentStatement.words` and `interpretation` are separate. `illustrative` marks invented intent, as in the worked example. |
| Applicable obligations govern what can be accepted; negotiable preferences support choices among permissible alternatives (Framework §3.2) | `Obligation` and `Preference` are separate classes. Only preferences are traded. |
| Proportionate rigor (Framework §3.2; Ch. 7 §7.9.3) | A delegation lets the human rule once for presentation and routine choices. One checkpoint ruling can cover several consequential choices, each named in its scope. |
| The app does not decide; generated output does not claim authority in its own voice (Ch. 6 §6.8.3) | `AppRole` stops at `recommend`, and only under logic adopted by the decision makers' authority (D-D2). Per-subject candidates count as recommendations (D-D3). Every decision must name a disclosed non-use saying the decision is the decision maker's (D-D4). |
| Configurational multiplicity: the schema does not dictate the limits of knowledge (Ch. 3 §3.6.3) | Patterns are hypotheses with grounds. The catalogue grows by marked proposals. Gaps keep unknowns visible. |
| The fractal property (Framework §3.4) | The four questions recur at the app's scale (the design record), at the result's scale (each authoring question asks what supports one number) and at the framework's scale (the catalogue's own grounds and standing). |
| Deterministic does not mean correct (Ch. 6 §6.7.3) | A complete trace shows only that every need reaches an element. Whether the element answers the need is the examiner's question (data-app-spec method §7). |
| Values and choice belong to the decision maker; analysis predicts consequences (structured decision making) | `AppRole` stops short of deciding. Weights or recommendation logic bind only under a made ruling (D-D2). `outside_the_app` lists what the decision weighs that the app does not model. |
| Consumers state their needs; tools derive reverse links (AGENTS.md) | Needs state `answered_by`. The checker derives orphan views and unchosen needs; no reverse links are stored. |

## 8. Relation to the application-family ontology

| Design element | Realised in the specification by | Trace slot |
|---|---|---|
| `Subject` | `EntityType` | `represented_by` |
| `PropertyOfInterest` | `ObservableProperty`, fields, results | `represented_by` |
| `DataHolding` | Data sources | `realized_by` |
| `InformationNeed` | Views, metrics, exports, messages | `answered_by` |
| `KnowledgeNeed` | Criteria, methods, parameter tables, packs, data products | `satisfied_by` |
| `Activity` | Navigation, exports, provenance views | `supported_by` |
| `Decision` | Consequence views and metrics | `consequences_shown_by` |
| `Alternative` | A scenario, an output series, or a category of a derived field | `realized_by` |
| `Concern` | Metrics, objectives | `measured_by` |
| `Obligation` | Any element, or a root path such as `build_profile.access`, that addresses it; an obligation met only by a human act is marked `met_by_act` and carried as an acceptance condition | `addressed_by` |
| `NonUse` | Text, caveats, `purpose.non_uses` | `disclosed_by` |
| `SettledQuestion` | The elements the answer became | `realized_by` |

The specification restates only what the builder needs: intended use, non-uses and the
tier. D-SYNC keeps the restatements equal. A later version should remove the duplication
where possible.

## 9. Projection

The same projector, `tools/project_schema.py`, generates both schemas. It gained three things for this
ontology, documented in its usage text:
- **Local imports.** Merged, with the imported root ignored.
- **A `--root` option.** Used for the catalogue schema.
- **Imported definitions only when reachable.** All local definitions are still emitted.

The reachability work found that app_family's `Region` class is referenced by no slot.

## 10. Known limitations

- **Single authorship.** One author wrote the ontology, the catalogue, the worked example
  and the checker. The worked example's intent is invented.
- **Partly grounded vocabulary.** The task facets follow published typologies, but those
  typologies were validated mainly for their descriptive power. The local additions are
  this ontology's own.
- **Patterns from a survey.** Their granularity and completeness rest on the apps surveyed.
- **Unverified sources.** Some knowledge-need sources in the example are named but not
  read: the Alberta Tier 1 document, and the EPA trend chapter.
- **No sketch tool.** The design checkpoint's sketch is specified; no tool produces it.
- **Records, not acts.** The checker trusts transcribed records within the limits in §6.
  Choice categories and answer authorities are the author's proposals; the examiner
  and the human check them.
