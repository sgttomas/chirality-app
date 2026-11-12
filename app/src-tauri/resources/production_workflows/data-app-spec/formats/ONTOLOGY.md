# Interactive data application family ontology (0.1)

The formal source is [`app_family.linkml.yaml`](app_family.linkml.yaml); the JSON Schema
[`app-spec.schema.json`](app-spec.schema.json) is generated from it
([PROJECTION.md](PROJECTION.md)).

This ontology is a way to represent this application family so that people and agents
can specify apps and a builder can consume the specification. Its coherence is not
evidence that it works; use is (thesis `docs/thesis/CHIRALITY_FRAMEWORK.md` §1;
Chapter 3 §3.1). Thesis references are paths in this repository.

## 1. What the ontology is for

An app specification answers four questions about one application, the same four the
thesis asks of any work (Chapter 3 §3.2):

| Question | In an app specification |
|---|---|
| What kind of thing is this? (ontology) | The domain entities and knowledge the app is about, the representation that constitutes the app, and the implementation conveniences kept apart from both |
| What supports the claim? (epistemology) | Grounds for every consequential element, explicit gaps, conflicts between sources, rulings that adopted a course under uncertainty, and known-answer tests |
| How does intent become usable work? (praxeology) | Data flow, analyses bound to versioned components, state and interactions, the build profile, and the review gates the workflow applies |
| What matters, to whom? (axiology) | Intended use and non-uses, decisions supported, objectives for decision support, and a consequence tier that sets proportionate review |

The ontology is **scaffolding, not a closed classification**. Configurational
multiplicity (Chapter 3 §3.6.3) means a schema "does not dictate the limits of
knowledge". So the ontology:
- gives every object a visible extension point (`x-` keys), which builders must not rely on;
- keeps unknowns visible (`Gap`, `standing: TBD`) rather than letting the format force a value;
- changes only through a governed revision with a version (§9).

## 2. Consistency with the thesis

| Thesis commitment | Where it lives in the ontology |
|---|---|
| Three levels stay distinct: work or domain entity, representation, implementation convenience (Ch. 3 §3.2.1) | Every class carries a `level` annotation (`domain`, `representation`, `implementation`, plus `epistemic` and `verification`). Domain classes say what the app is about (stations, pollutants, objectives, subpopulations, methods). Representation classes are the app (data flow, views, controls). `BuildProfile`, `Materialization`, `RuntimePin` and `Theme` are implementation conveniences. They "must not change the meaning of any semantic element", and a materialised result must equal its runtime result within tolerance. |
| A requirement, an assumption, a physical model, a proposed operation, a result and an acceptance are different things (Ch. 3 §3.2.1) | `Criterion` is an issued or required value (e.g. the 11 ppb objective). A statistically estimated control limit is a `Result`, not a `Criterion`, a confusion SPC demos often show. `Method` is the idealization; `AnalysisComponent` is an implementation; `Analysis` is the use in this app. A specification is a proposal; acceptance is external. |
| Claim, Warrant, Status, Gap, Conflict, Ruling (Ch. 3 §3.2.2; Ch. 5) | The `Claimable` mixin gives elements `basis` (warrants of kind observed, documented, inferred, derived, expert judgment, owner direction or ruling) and a scoped `standing` (FACT, ASSUMPTION, PROPOSAL, TBD). `Gap`, `Conflict` and `Ruling` are first-class elements. |
| FACT/ASSUMPTION/PROPOSAL/TBD are useful labels, not an exhaustive ontology; a label is not its evidence (Ch. 3 §3.2.2) | `standing` is optional and never replaces `basis`. The checker treats `standing: TBD` as a placeholder that blocks a build (rule R-TBD1); it does not treat FACT as proof. |
| Grounds, examination and reliance change independently (Ch. 3 §3.2.2; Ch. 5 §5.5) | The specification carries grounds. Examinations and acceptance are separate records bound to the specification's content hash. They are outside the content they identify, as in software-prd's DECISION.md. `ReviewRequirement` states which examinations are needed, never that they occurred. |
| Descriptive records versus constitutive acts; agents may transcribe but not originate a human act (Ch. 5 §5.5; Ch. 6 §6.8.3) | `Ruling.status` is `proposed` (agent-prepared, no authority) or `made`. `made` requires `decided_by` and `evidence` of the act; the checker rejects a made ruling without them. |
| Numerical verification, model applicability and engineering adequacy are three questions (worked example) | Verification: `KnownAnswerTest`, `PropertyTest`, component `tolerance`. Applicability: `Method.assumptions`, `applicability`, `limitations`, `Assumption.consequence_if_violated`, `Caveat`. Adequacy for intended use: `Purpose.intended_use`, `non_uses`, `ConsequenceAssessment`, and the owner's external acceptance. A passing known-answer test says nothing about applicability. |
| Generated output must not claim acceptance in its own voice (Ch. 6 §6.8.3; Ch. 3 §3.6.5) | The specification never records its own acceptance. `ProvenanceItem.acceptance_status` tells the built app to *read* the external acceptance record and show who accepted what, for which purpose, at which hash, or that no acceptance exists. |
| Deterministic does not mean correct (Ch. 6 §6.7.3) | The builder's determinism is a reproducibility property (`data-app-build`'s builder input contract). Correctness rests on known-answer tests, applicability conditions and review. |
| Proportionate rigor; a control earns its place by what it contributes against attention, delay and complexity (Ch. 3 §3.2.4; Ch. 7 §7.9.3) | `ConsequenceTier` (T0–T3) keys the review gates (`resources/gates.md`). Lower tiers carry fewer obligations; most slots are optional. |
| The fractal property: the questions recur at several scales (Ch. 3 §3.3) | **Result:** units, grounds, result provenance, known-answer tests. **Application:** purpose, consequence, the specification's grounds and gaps. **Framework:** the ontology's own versioning and review through create-workflow. |
| Judgment stays with the person; agents extend reckoning (Framework §2.5) | Agents draft specifications, extract domain knowledge and bind analyses. The owner, domain experts and accountable professionals set purpose and tier, make rulings, accept domain packs and specifications, and own reliance. |

## 3. Class groups

Classes by group. Exact slots are in the LinkML source; this section explains roles.

**Identity, purpose and consequence.**
- `AppSpec` (root). Ontology alignment: close to `prov:Plan`, since the specification is the plan a build follows.
- `AppIdentity` and `LineageLink`: reproduces, succeeds, variant of or informed by another app, with repository and revision.
- `Purpose`: intended use, questions, decisions supported, users, non-uses, archetypes.
- `ConsequenceAssessment`: tier, error consequences, detectability, affected parties and the ruling that set the tier.

**Domain (what the app is about).**
- `EntityType`: aligned with `sosa:FeatureOfInterest`. Examples: a monitoring station, a well, a caribou subpopulation.
- `ObservableProperty`: aligned with `sosa:ObservableProperty`. Has a unit and value semantics such as ratio, circular, censored or probability. Value semantics exist so that, for example, a circular quantity such as wind direction does not enter a linear correlation.
- `Criterion`: issued or required values with bound, averaging period, statistic, jurisdiction, instrument and edition.
- `ClassificationScheme`: classed bins.
- `Method`: the idealization, with assumptions, applicability and limitations.
- `Assumption`, `Definition`, `Caveat`.
- `ParameterTable`: keyed domain parameters with per-row grounds, such as demographic rates by management action and subpopulation.
- `KnowledgePackRef`: an accepted, versioned output of the domain-knowledge-intake workflow.
- `Lever` and `Objective`, for decision support.

**Data (inputs and data flow).** `DataNode` is abstract: anything that yields data.
- **Sources:**
  - `BundledDataset`: a hashed snapshot.
  - `DataProductSource`: versioned and produced upstream. Preparation stays out of the app.
  - `UploadSource`: a user contract with rules and an example.
  - `ExternalServiceSource`: endpoint, secret by name only, refresh, failure behaviour.
  - `GeneratedSource`: seeded.
- **Transforms.** A closed vocabulary of twelve kinds plus `ComponentTransform`, the escape hatch:
  - source selection, field selection (including a user column-role mapping), parsing, filtering, sorting, dropping missing values;
  - head/tail phase split, temporal aggregation with a completeness threshold, gap filling;
  - join, derivation, reprojection.
- **Results:** typed outputs of analyses, including rasters with a CRS.
- **Schemas:** `TableSchema` and `Field` follow Frictionless Table Schema types, adding unit, role, value semantics and aggregation basis. Frictionless itself has no unit property.

**Analysis.**
- `AnalysisComponent` is a registry entry with four parts:
  - a typed interface: input ports, parameters with domains and units, output ports;
  - a pinned `Implementation`: language, package and version, entry point, source repository and revision, licence, bundle hash;
  - determinism class, tolerance and preconditions;
  - the known-answer tests that qualify it.
- `Analysis` binds a component in this app: inputs, parameter values with grounds, outputs, preconditions with user-facing messages, recompute mode, and explicit result semantics (e.g. "limits are frozen from the baseline").
- `Metric` defines a reported quantity: formula or source field, unit, rounding, clamps, missing rule and display.
- `Scenario` is an evaluation context of parameter overrides (§6.4).

**State and interaction.**
- `StateVariable`: typed, with a domain. A temporal domain uses a calendar step (`P1M`), not a fixed number of days, which drifts against calendar months.
- `Control`: eight kinds by value type. It sets a state variable; the widget is only a hint.
- `Interaction`: an event (view event, state change, trigger, app start, data loaded) and ordered effects (set, toggle or reset state; snapshot or clear a scenario; run; navigate; download).

**Presentation.**
- `View` kinds:
  - charts in a Vega-Lite-like layer and encoding grammar;
  - a domain control chart with phase-aware parts;
  - a matrix heatmap;
  - maps with point, raster and polygon layers;
  - tables;
  - a decision-support consequence table;
  - KPI, text, document and provenance views;
  - `RegisteredView`, the renderer escape hatch.
- Supporting classes: `ColorScale` (domain policy, midpoint criterion, cap); `Layout`, `NavItem` and `Placement` (layout refers to elements by id); `TextBlock` with a verbatim flag; `Asset` with a hash; `Message`; `Export`.

**Provenance and epistemics.**
- `SourceReference`: aligned with `dcterms:BibliographicResource` and `prov:Entity`. Has a locator, retrieval date, hash, licence, access and status note (e.g. "HTTP 404 on 2026-11-02").
- `Warrant`.
- `ProvenancePolicy`: what the app shows, and whether results carry "how was this computed" provenance.
- `Gap`, `Conflict`, `Ruling`.
- `FidelityDecision`: for a specification derived from an existing app, whether an observed behaviour is reproduced, corrected, omitted or deferred, and under which ruling.

**Verification.**
- `VerificationPlan`: known-answer tests with oracle kind, source, inputs, parameters, expected values with tolerances, and any confirmation still needed; property tests; checks the builder generates; data contract checks; review requirements.

**Implementation (kept apart).**
- `BuildProfile`: target, runtime pins, materialisation strategies, access, hosting region, theme.

## 4. Principal relations

| Relation | From → to | Meaning | Alignment |
|---|---|---|---|
| `inputs` | Transform, View → DataNode | consumes | `prov:used` |
| `outputs` | Analysis → Result | produces | `prov:wasGeneratedBy` (inverse) |
| `component` | Analysis → AnalysisComponent | executed by | `prov:wasAssociatedWith` a software agent |
| `implements` / `method` | Component, Analysis → Method | realises the idealization | — |
| `sets` | Control → StateVariable | user sets state | — |
| `from_state`, `source_field_from` | binding → StateVariable | reads state | — |
| `applies_to`, `overrides` | Scenario → Analysis | evaluation context | — |
| `observable` | Criterion, Field → ObservableProperty | about this property | `sosa:observedProperty` |
| `instrument` | Criterion → SourceReference | issued by | `dcterms:source` |
| `basis` | Claimable → Warrant → SourceReference | grounded by | `prov:wasDerivedFrom` / `prov:hadPrimarySource` |
| `affects` | Gap, Conflict → element path | consequence lands here | — |
| `adopted_by`, `ruling` | element → Ruling | authorised under uncertainty | qualified `prov:wasAttributedTo` with role |
| `lineage` | AppIdentity → reference app | reproduces / succeeds | `prov:wasRevisionOf`, `prov:wasInfluencedBy` |

The specification contains no reverse links. Tools derive them, as the library's
deliverable queries do (AGENTS.md, "consumer states its needs; tools derive reverse links").

## 5. Constraints

Constraints sit in three layers, and each layer establishes something different.

1. **Structural (JSON Schema).** Types, required slots, enumerations, closed objects,
   patterns and the `kind` discriminator. Passing establishes form only.
2. **Semantic rules (validator).** These are rules JSON Schema cannot express:

   | Rule | Check |
   |---|---|
   | R-ID | Identifiers are unique across the specification |
   | R-REF | Every reference resolves to an element of the expected class or a subclass |
   | R-PATH | Element paths start with an existing identifier |
   | R-EXPR | Every `$name` in an expression is a state variable |
   | R-PB1 | A parameter binding has exactly one of value, expression, state or TBD |
   | R-PL1 | A placement has exactly one of ref or items |
   | R-IF1 | Bindings, scenario overrides and test parameters name declared parameters and ports |
   | R-COV | State set by a control is read somewhere, so no control is inert |
   | R-KAT | Every analysis component has a known-answer test (warning) |
   | R-RUL | A ruling marked made carries the decider and evidence of the act |
   | R-TBD1 | Placeholders block a build |
   | R-GAP | Open gaps blocking build block a build |
   | R-FD | Undecided fidelity decisions block a build |
   | R-FD2 | A fidelity selection names a ruling and binds only once that ruling is made; an author cannot originate one |

   `tools/check_spec.py` implements all of these.
3. **Obligations (workflow and validator profiles).** Not yet checked by a tool:
   - **Archetype obligations** (§7). Examples:
     - `qc_compliance` requires baseline or limit semantics and a known-answer test per statistical component;
     - `decision_support` requires objectives, alternatives and a consequence view;
     - `spatiotemporal_map` requires a declared CRS and interpolation method.
   - **Tier obligations** (`resources/gates.md`). Example: from T1, a provenance display of data sources and a known-answer test for every analysis component.

## 6. Semantics

These rules give the specification a single meaning for the builder.

1. **Data flow.**
   - The node graph is derived from references and must be acyclic.
   - A node recomputes when a state variable or upstream node it references changes.
   - An analysis with `recompute.mode: on_trigger` waits for its trigger.
   - An analysis whose outputs no visible view, export or metric consumes need not be computed (lazy evaluation; N-02).
2. **State.**
   - A state variable starts at `initial`, or `initial_expression` evaluated at start.
   - A control displays and sets its state variable.
   - `reset_state` restores the initial value.
   - Domains bound to other state (`max_expression: $popstart`) are re-evaluated on change. A value left outside its domain is clamped to the nearest bound and reported as an interaction event.
3. **Interactions.**
   - When an event fires, the condition is evaluated on the state before the event's effects.
   - Effects apply in the order listed.
   - Recomputation happens once, after all effects.
   - A `snapshot_scenario` records the listed state variables' current values as the scenario's overrides. Unlisted state stays live, which is how a reference scenario can keep a global horizon and starting population current.
4. **Scenarios.**
   - Evaluating analysis A under scenario S means running A with the base state, then S's `derived_from` overrides, then S's own overrides.
   - An override expression that names a result (e.g. `mp_breakeven_p`) uses that result evaluated under S.
   - `metric@scenario` in an expression names a metric evaluated under another scenario.
   - A consequence-table cell is its row metric evaluated under its column scenario.
5. **Metrics.** Order of application: compute, clamp, round (mode and digits), then the missing rule (`missing_when` → `missing_display`).
6. **Fidelity.**
   - A selected fidelity decision binds the behaviour it names once the ruling it names
     is made. Until then the selection is a proposal and blocks a build. An author may
     propose a selection but cannot originate the ruling.
   - `reproduce` requires the specification to state the behaviour exactly, defects included.
   - `undecided` and `defer` block a build.
7. **Gaps.** An open gap whose `blocking` includes `build` prevents a faithful build. A ruling may authorise a successor build without supplying the missing grounds (`status: ruled_around`). The thesis: a ruling "can select a course of action under uncertainty without turning the uncertain premise into a fact".
8. **Build profile.** May choose where and when computation happens. May not change results beyond component tolerance, labels, or the set of behaviours.

## 7. Archetypes as authoring patterns

Archetypes come from a survey of public data-app galleries. They are patterns, not
types: apps combine two or three. In the specification they are classifications. They guide authoring and
checking: which questions the workflow asks and which obligations apply. They do not
instruct the builder.

| Archetype | Authoring questions the workflow must settle | Example in this family |
|---|---|---|
| explorer | Which filters, which linked views, which exports | A river water-quality explorer |
| indicator_surveillance | Indicator definitions, comparators, release vintages, suppression | A public-health indicator dashboard |
| spatiotemporal_map | CRS, layers, time step, interpolation method and its variance, colour-domain policy over time | An interpolated air-quality map; a raster scenario atlas |
| live_monitoring | Refresh policy, staleness display, thresholds | A continuous air-monitoring feed |
| qc_compliance | Baseline or limit derivation, rule set, criteria source and edition, phase semantics | Control charts; guideline screening of site samples |
| calculator | Function, units, input bounds | An engineering calculator |
| model_simulator | Model binding, parameter bounds, run gate, seeds | A dispersion model; a population simulator |
| decision_support | Objectives, alternatives, levers, consequence table, assumptions, social-choice limits | Comparing management actions for a wildlife population |
| analysis_workbench | Upload contract, role mapping, staged pipeline, validation messages | Upload-and-analyse tools |
| teaching_demo | Narrative, seeded randomness | Statistics teaching apps |

Out of scope for this family:
- chat or LLM features;
- CRUD and forms;
- multi-user write-back;
- games;
- real-time instrument control;
- GIS editing;
- general-purpose analysis environments.

Where an app contains such a feature, the specification records it as out of scope rather than approximating it.

## 8. Open ontology, closed specification

The ontology's meaning is open to revision, but each specification is validated
closed-world: unknown keys fail unless they are visible `x-` extensions. LinkML is a
closed-world schema language suited to validation, while OWL is open-world and suits
aligning vocabularies (LinkML FAQ; OWL 2 Primer). A JSON-LD context generated from the
LinkML source would let specifications be
read as linked data aligned with PROV-O, SOSA, QUDT and DCAT without changing their
JSON.

## 9. Versions and identity

Four identities stay distinct:

| Identity | Example | Notes |
|---|---|---|
| Format version | `appspec_version: "0.1"` | Validation-relevant |
| Ontology release | `ontology_version` | Semantic Versioning |
| Application version | `app.app_version` | |
| Content identity | sha256 of the canonical JSON | What examination and acceptance bind |

Format migrations are forward-only and stepwise, with golden fixtures, as
Grafana does. Stable element identifiers survive revisions.

## 10. Known limitations of 0.1

- The expression language is defined only as far as the features in use.
- The namespace URI `https://chirality.ai/ns/app-family/` is a placeholder.
- `tools/project_schema.py` produces the projection; it is not a general LinkML generator.
- Some values a test needs have no slot yet, such as marker strokes and dynamic heading
  text. A specification carries them in `description` text and declares that text binding.
