# Reading Chirality as the worked example

**Prospective method, 2026-09-19. No case findings are asserted here.** This
document sets expectations before reconstructing episodes from `chirality/`
and its subprojects. It is part of the explanatory manual, not a registered
workflow or a new requirement on project execution.

## 1. The question the case can answer

The [theory](01_theory.md) proposes relationships among project definition,
coordination, continuity and accountable reliance. The worked example asks how
those relationships appear in actual work, including where their predicted
benefit is absent or their use introduces friction.

The case cannot establish universality by finding familiar words in the
repository. A directory called a work graph does not establish that it guided
execution; a review record does not establish that the review found relevant
defects; a decision log does not establish accurate attribution. The evidence
must show what the participants did, what changed and what consequences can
reasonably be connected to it.

Chirality is both the subject of the theory's development and the later example.
That dependence limits the strength of confirmation. Expectations are informed
by experience already known to the author and owner. Freezing them before the
systematic case reconstruction helps expose later changes of interpretation;
it does not create an independent or blinded experiment.

## 2. Units and selection

Use a bounded **episode** as the primary unit: a question or commitment, the
relevant decisions and work, and an observable disposition or interruption. An
episode can cross commits, agents, branches and packages. Its bounds should
follow the question being examined rather than a convenient number of files.

Candidate classes include initial definition, decomposition and dependency
resolution, coupled implementation, parallel execution, integration, interrupted
continuation, reconciliation, and release. The intended study draws from the
root project and subprojects rather than using a fictional supplementary case.
Which actual episodes belong in those classes remains to be established.

Select successful, failed, interrupted and apparently uneventful episodes where
records permit comparison. Record the selection rationale and available coverage
before assessing outcomes. Include episodes that lack the expected structure or
use a simpler practice successfully. A project may have no well-evidenced example
of a proposed phase; report that limitation instead of supplying one by inference.

Freeze a theory revision and an episode inventory before the detailed analysis.
If a later discovery changes the inventory or proposition, record the reason
and preserve the earlier version. Such changes can improve the study; presenting
them as original predictions would misstate its evidential strength.

## 3. Prospective expectations and contrary evidence

The following expectations are agent-authored deductions from the theory. They
are not owner rulings, numerical acceptance thresholds or established findings.

| Proposition | What to look for | Evidence that would weaken or revise it |
|---|---|---|
| **P1: coordination follows work condition** | Shifts between dialogue, coupled work, autonomous traversal and narrow integration track identifiable changes in uncertainty or coupling | The same arrangement works equally well across materially different conditions; switches add coordination cost without an identified benefit; tooling alone explains the outcome |
| **P2: relationships among views matter** | A failure crosses composition, precedence, provenance or synthesis boundaries despite local success | The four-view account adds no explanatory detail beyond an ordinary defect description; failures remain unclassified; alternative groupings explain them better |
| **P3: dependency analysis exposes decisions** | SCC analysis reveals a concrete unresolved interface or interpretation, followed by a reasoned change and workable order | Cycle processing changes only labels; the same obstacle persists; missing acyclic dependencies dominate the problem; a cycle was harmless for the actual objective |
| **P4: readiness differs from closure** | Ready work proceeds usefully while broader obligations remain explicit; final examination finds relationships invisible to local readiness | Wider prerequisites were actually necessary before the work could proceed; the distinction hides unfinished commitments; repeated closure checking provides a benefit the theory understates |
| **P5: assessable boundaries improve delegation** | Returns with clear purpose, scope and expected evidence integrate with fewer reconstructive questions or less rework | Brief detail adds overhead without changing outcomes; tacit interaction suffices; model capability, task simplicity or shared context explains the apparent advantage |
| **P6: connected verification exposes boundary failures** | User journeys reveal a defect across components or hosts that the earlier checks did not cover | Connected tests repeat existing coverage at high cost; the important defects arise elsewhere; a proposed native witness exercises no host-dependent behaviour |
| **P7: continuity needs provenance and interpretation** | A successor reconstructs decisions and remaining work from identified sources, or fails because attribution/supersession is wrong despite intact files | Missing provenance has no material effect in the episode; better retrieval alone resolves the difficulty; apparently complete records still fail to carry the understanding needed |
| **P8: process must improve work or assessability** | A control detects a relevant defect, preserves a consequential relationship or makes a decision more intelligible | A control repeatedly produces artifacts or interruptions without an identifiable contribution; removing it under proper authority improves execution without the predicted loss |

A single supporting incident is an illustration, not a causal estimate. A
counterexample may identify a boundary condition rather than reject the entire
proposition. The analysis should make that distinction explicit instead of
protecting every proposition from possible revision.

## 4. Reconstruct the episode before classifying it

For each episode, establish the objective, accepted basis, available inputs,
participants and authority. Reconstruct the sequence using versioned artifacts,
diffs, work graphs, briefs, retained returns, raw checks and attributed owner
directions. Distinguish a contemporaneous record from a later explanation.

Record what could have been known at each decision. A later successful repair
does not show that the original decision was unreasonable given its inputs;
nor does a later narrative establish that the team used a practice it only
described afterwards. Branch state and uncommitted work may matter where their
identity can be established. Do not reconstruct missing bytes from confident
handoff prose.

Then examine the four structures and perspectives. Permit several structures
to bear on one episode, and permit an episode to remain unexplained. State
whether a classification was independently checked and what the checker could
see. A fresh agent can challenge the reconstruction; it is not a substitute for
an independent practitioner or evidence from a separate project.

## 5. Absence and the limits of the record

Use distinct descriptions for four situations:

1. **Not found in the examined record:** the search did not locate evidence.
2. **Coverage insufficient:** missing history or inputs prevent a conclusion.
3. **Evidence of omission:** a sufficiently reconstructed episode shows that
   the relevant act or relationship was omitted where it mattered.
4. **Deliberate deferral or inapplicability:** the team explicitly chose another
   arrangement, or the proposed practice had no relevant job to do.

These are analytical distinctions, not new lifecycle states. A conspicuous
absence needs an explanation of why the evidence would be expected to exist,
which sources were examined and what alternative explanation remains. It must
not be inferred solely from a missing filename or an empty field.

In particular, absence of documentation does not prove absence of understanding.
Presence of documentation does not prove that its author or reader understood
the work. Observed actions, decisions and corrections can bear on understanding,
but the case cannot inspect a participant's knowing directly.

## 6. Attention, quality and resource observations

The owner-adopted warranted-confidence/attention aim needs several observations,
not an invented score. Where actually recorded, report preparation and review
effort, interventions, repeated decisions, reconstruction effort, defects found
and their consequences. Separate measurements from estimates and impressions.

Counts alone are ambiguous. Fewer questions can mean better preparation or
unreported uncertainty. More findings can mean better detection or poorer work.
Faster execution can transfer effort to integration or to the owner. A long
review can be valuable for a consequential change and disproportionate for a
small reversible one.

Model, reasoning configuration, harness capabilities, task difficulty, writer
experience, source quality and shared-resource contention are possible rival
explanations. Preserve their actual attribution when available. Do not infer
comparative model performance from a few differently scoped assignments or
equate the configured model name with an independently verified serving model.

The case may support qualitative judgments about where attention was well spent.
It should not claim to have measured warranted confidence as a validated quantity
without a separate definition and evaluation of that measure.

## 7. Form of the eventual worked account

Each episode should tell a readable project-management story: the problem,
available basis, consequential choices, work performed, observed outcome and
remaining uncertainty. A compact evidence table can connect material assertions
to the identified records. Preserve one canonical raw evidence source rather
than duplicating logs across the narrative.

After the reconstruction, explain which theoretical expectations the episode
supports, complicates or contradicts. Identify alternative explanations and
the limits of the conclusion. Separate recommendations for future practice
from claims about what actually happened.

The cross-episode synthesis should report where the theory helped expose
relationships hidden in operational detail, where an expected pattern was
absent, and where the theory itself needed revision. It should retain unresolved
cases and successful simpler practices. A useful manual can learn that a
particular form of control is unnecessary under stated conditions.

## 8. Coherence checks during composition

The author examines the argument outline, the complete theory draft and the
integrated response to independent review. A bounded source check tests
attribution and conceptual boundaries. A fresh reviewer then challenges the
whole frozen draft, including this method. These are the current drafting
arrangements, not a permanent manager roster imposed on readers.

| Perspective | Questions for the author and reviewer |
|---|---|
| Ontology | Are product, project, records, work units, roles and graphs used consistently? Are the four structures distinct from the four philosophical perspectives? |
| Epistemology | Can the reader distinguish definitions, propositions, observations, interpretations and recommendations? Are source support, missing evidence and claim limits visible? |
| Praxeology | Does each recommended practice address the problem the argument identifies? Are entry conditions, authority, return and failure treatment coherent with the theory? |
| Axiology | Do practices serve useful software, adequate grounds for reliance and effective human attention? Are competing purposes and residual consequences visible? |

Cross-check the answers. For example, a recommendation for autonomy must retain
the authority boundary the argument assumes; a recommendation for evidence must
not pretend that records exhaust understanding; a recommendation for proportionate
review must not silently relax the criterion being verified.

Independent editorial review can improve this draft. It cannot make its
propositions empirically established or constitute the owner's acceptance.
Those distinctions remain part of the account the manual is trying to explain.
