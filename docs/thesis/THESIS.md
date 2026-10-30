# From General Capability to Situated Participation

**The Chirality App v4 Thesis**

*Why an application for making methods is the first exemplar of Chirality*

## Abstract

An application can make general agent capability useful by connecting it to
meaningful objects, actions and consequences. The person stays engaged in
judgment, the agent contributes inquiry and action, and reusable methods carry
learning between undertakings.

The Chirality App begins with method itself. A person and an agent develop a
way of working through conversation, try it, examine its effects and make it
available for further use. Workflow authoring makes methods accessible to
inquiry without turning them into exhaustive orchestration.

App v4 gives this approach concrete form through native supplier hosting,
workflow trials, explicit human acts and recovery that distinguishes intent
from observed outcome. Actual use also exposes its limits: interrupting a turn
may leave a command running, a faithful trial may exercise a poor method, and
a recorded approval may tell little about the person's engagement.

Shared meanings and host-specific operations offer a route into domain
applications. Their value depends on useful participation and the effort
required to achieve it.

This essay develops the operative view of the work introduced in the
[shared introduction][S1]. Root asks what responsible participation should
preserve, the App asks how those commitments become usable activity, and
SWBPIPE examines the resulting means in a particular engineering practice. The
[support-arrangement example][S2] connects the three through one illustrative
revision, rather than reporting a completed integration witness.

## 1. The problem behind the application

An agent working beside an application can give advice about what a person
should do. An agent working within it can also inspect the relevant objects,
prepare a change, apply it within authority and examine its consequences. That
possibility changes the relationship between conversation and work: the
conversation can become a place from which the work is carried forward, rather
than a source of instructions the person must translate into a separate
sequence of actions.

The value does not come merely from reducing clicks: translation is also a
point at which meaning can be lost. A spoken reference to “that case” must
identify a particular object, a proposed revision must concern the version that
was examined, and a result must be understood under the conditions that
produced it. If an agent and a person act through different versions of those
meanings, they can appear to collaborate while changing different things.

Interruption makes the problem concrete. In one observed App configuration,
interrupting a turn running `sleep 90` ended the turn but did not establish
that the command had stopped; supplier history later reported that it had
completed.[O1] The person needed to know what happened before deciding how to
continue.
[Section 7.1](#71-a-counterexample-supplied-by-the-running-application)
examines that observation and the limits of the App's display. The application
needs to show what is known about the outcome and what remains uncertain.

**Why and under what conditions should an
application enable a general agent to participate in its work, and why should
workflow authoring be the first exemplar of that participation?**

One objection is that a strong coding agent with files and a command line may
already be sufficient. For many development tasks that is a serious alternative.
An additional App is justified only where it improves the person's access to
the work, preserves useful meaning or makes action and examination easier.
The existence of agents does not establish demand for another interface.
Chirality's case depends on those practical benefits becoming observable.

## 2. Shared orientation, particular subject

Four perspectives meet in application work. **Ontology** concerns its objects
and relationships. **Epistemology** concerns grounds and uncertainty.
**Praxeology** concerns effective action and correction. **Axiology** concerns
purpose, consequences and the costs of the means.

In an application these questions meet in an ordinary operation. A request
concerns an identifiable object, its proposed effect rests on a reading of that
object, carrying out the request changes what can happen next, and the person
cares about the consequences. Separating these questions analytically helps
expose a failure, but treating them as separate procedural duties would miss
how they relate.

Agent inquiry and action are **reckoning**: analysis, planning, criticism,
comparison and adaptive execution. **Judgment** is the person's situated,
committed engagement with what the work means, what matters and what they will
stand behind. It shapes the question before any final acceptance occurs.[R2]

Continuing authority gives an agent room to investigate and repair while
keeping consequential choices attributable. An assignment or adopted policy
supplies authorization. A host's available tools and permissions supply means
and limits for acting. Capability alone authorizes nothing. The appropriate
boundary depends on the activity.

The relationship among the views is iterative. A trial can reveal that a
workflow represents the wrong subject, that its evidence is insufficient, or
that its original purpose would impose more burden than benefit. That finding
returns to the representation, the method or the purpose it challenges. The
person and agent can revise authorized means directly, but changes to adopted
commitments belong to the authority that holds them. So feedback is part of
purposeful work, rather than a final evaluation attached to a fixed design.

## 3. Why making methods is the first exemplar

A useful method often begins before it can be specified. Someone meets a
problem, tries a framing, discovers a missing distinction and changes how they
proceed. A successful sequence can then be examined for what might be useful
again. That learning is neither the same as the transcript nor reducible to a
list of commands stripped of their purpose.

Conversation is valuable here because the subject can develop during the
exchange. The person need not supply a complete specification before receiving
help. The agent can make an assumption visible, suggest a comparison or carry
out an investigation that changes what the person asks. The resulting method
can express both a purpose and a way to approach it without determining every
step in advance.

Workflow authoring makes this process itself available as work. A draft can be
read, tried and revised, and its intended inputs and returned evidence can be
made explicit. Someone can tell the version under trial apart from one selected
for reuse. When later work reveals a limitation, the method can be corrected
rather than merely supplemented with another instruction in an ever-growing
conversation.

The App comes first because it makes the method available to its own inquiry.
The agent helps form the conditions of later work, and the person can examine
and decide on how they are formed.

This starting point has a cost. A method-authoring tool can become absorbed in
its own machinery. Elaborate registration and governance can make it harder to
carry out the activity whose method is being developed. A successful trial can
become an unnecessary prerequisite for every revision. So the product has to
earn its structure through the learning and control it gives the person. The
current design makes a fresh-conversation trial available, without making it a
universal condition of registration.

### 3.1 A trial must examine the intended method

Earlier attachment-based trials did not supply a workflow in the same way as a
registered run. This mattered: a favourable result could concern a different
framing or context, giving the author weak grounds for expecting the method to
behave similarly in use. The owner's later direction made trial fidelity an
explicit design concern.[A2]

The current implementation takes a snapshot of the draft and uses the same
composer as a registered run of that content. An explicit header identifies the
activity as a trial. The run reference and the folder of associated files
differ because they identify the trial's own subject. A source test compares
those texts and checks the permitted differences. Preparation also detects a
draft that changed while it was being read, and refuses to silently try another
version.[I1]

Trial fidelity answers whether the intended method was supplied in the relevant
form. The quality of the method and the model's use of that material require
further examination. A faithful trial can expose a poor framing as clearly as
it can support reuse. Its findings can require different inputs, a new
comparison or a changed objective, rather than merely running the same steps
again.

Two trial situations remain valuable in different ways. A delegated trial can
stay in the context of authoring and return findings to that conversation. A
clean trial can expose dependence on context the author has taken for granted.
Neither context is better in every case. The author needs to understand what
was tried and why its result bears on intended use.

Both trial phases are implemented, but native witnesses of both kinds and live
reads of delegation-availability signals remain open.[A2][I2]

## 4. Methods should guide action without replacing inquiry

A reusable workflow must preserve enough of a method to be useful elsewhere,
and it must also allow attention to circumstances its author did not foresee.
If it is only a vague statement of purpose, the next participant may have to
rediscover everything. If it prescribes every action, it can force unsuitable
work or hide a premise that no longer holds.

The App's distinction between a method written in prose and a small declared
part offers a way to manage this tension. Prose can convey purpose, conditions,
distinctions and examples. Declarations can identify expected inputs, tools,
human acts and outputs that the product can expose. Neither makes the workflow
a complete description of the work. The product observes selected features of
the method while the person and agent continue to interpret the work.[A1]

A reusable method carries recorded guidance and evidence, not its author's
whole understanding. The later participant must recognize which conditions
apply, what an example leaves out and where the method needs correction. Making
a resource easy to retrieve helps that interpretation, but it does not transfer
a knower's situated understanding into the next conversation.

Role guidance has a similar purpose. Conception, integration and bounded
execution describe contributions that can otherwise be left without an owner.
They need not prescribe a separate conversation or agent for every
contribution. Some work may benefit from a manager or from parallel
contributors; other work may be carried through by the person and one agent.
Flexibility in how work is arranged does not remove responsibility for bringing
the result together.

App v4 offers HELP_HUMAN, HELPS_HUMANS and WORKING_ITEMS as conversation roles;
TASK remains delegated. Choosing a role does not grant permission. Repository
assignments and the App's runtime settings govern different activities.[A1]

The native witness cautions against treating a role arrangement as an
accomplished coordination system. It observed a manager spawning a child,
waiting, sending a follow-up and closing it. It also found that the manager
could not message an unrelated conversation through that route. Some native
activity appeared without the full prompt or relationship information needed to
establish receipt, review and integration. The App showed those limits rather
than inferring completed coordination from the child's existence.[O1]

Useful orchestration makes responsibilities and returns easier to manage, but a
display of a team cannot establish that its contributions form a usable whole.

## 5. Meaningful perception and action

An application brings more than storage to an agent: it already distinguishes
objects, allowed operations, conditions and consequences. Those meanings are
often what makes the application useful to a person in the first place. Agent
participation becomes stronger when it can use them directly.

So the host-integration contract proposes a common capability catalog and one
route for validating and applying changes. The person's interface, the embedded
agent and an external controller should concern the same operations, with the
same reasons why an operation is unavailable. An agent may receive a structured
view rather than pixels. Semantic parity concerns what the view and action
mean, not identical presentation.[A3]

Consider a proposed change based on an earlier read. If the object has since
changed, applying the proposal to the newly selected object would silently
change the subject. Identifying the proposal's basis and refusing a stale
proposal make the relationship inspectable. Similarly, a retry after an
uncertain response must not simply create a second effect. These concerns come
from the meaning of the operation, not from a need to give every agent action a
ceremonial approval.

The [support-arrangement example][S2] makes the distinction concrete.
Inquiry begins with an access concern in the current arrangement. Operation
validation examines the declared preconditions of a proposed support edit.
Applying the edit, when authorized, changes the identified model state. Human
acceptance is a separate act concerning its particular subject. None of these
establishes that the arrangement is adequate for the physical undertaking. Refusing a stale
proposal can preserve the subject of inquiry, while a later comparison can
expose an additional construction or maintenance condition that the initial
framing left out. The App's contribution is to help those meanings and returns
stay connected.

Perception and action constrain one another: the agent needs a view adequate to
the action it proposes, and the result of the action must provide enough
evidence to continue. An application that offers powerful writes but incomplete
reads can produce decisive action on mistaken premises. One that offers rich
context but no useful operations leaves the person translating the result back
into work. The relevant unit of design is the connected activity.

The contract's distinctions between proposal, execution and human acceptance
follow from this relationship. Operation success establishes that the operation
ran under its stated semantics. Acceptance identifies a person's act concerning
a subject. Professional reliance concerns yet another relationship. Combining
them in a single “success” indicator would make the interface simpler by making
its meaning less dependable.

## 6. Preserving human judgment without multiplying gates

An agent can prepare a decision so well that the person has little additional
calculation to perform, but the person still has to engage with what the
decision means. More polished preparation can assist that engagement, or
discourage it by making the conclusion appear settled.

The application cannot ensure substantive judgment merely by requiring a
button press. It can make the subject clear, show the alternatives and
consequences, preserve the grounds and distinguish what was observed from what
was inferred. It can also prevent an automated rule from being recorded as an
actual human act. These are valuable contributions with limited claims.

Native request handling refuses answers that widen the requested permissions. A
constructed test also rejects an affirmative answer attributed to an App rule
rather than permitted interaction.[I3] These checks concern request handling,
but the person must still understand what they permit.

Trustworthy cold replay and native authenticity still need further
implementation and examination.[A4]

Preserving judgment also requires room for delegated action. Requiring a new
human act for every ordinary step can interrupt inquiry and use up the
attention needed for choices that matter. So the host contract distinguishes
operations that may apply within granted autonomy, proposals that need
acceptance and acts reserved to the person. The appropriate classes belong to
the host's actual work and adopted policy. The general framework does not
settle them for every application.[A3]

Workflow checkpoints currently guide the person and agents. Making the software
hold at checkpoints is deferred.[A1][A3]

The values involved include user control, useful production, privacy and the
cost of attention. Applicable obligations and safety constraints set conditions
on the work, and negotiable preferences concern choices within those
conditions. A faster interaction cannot justify recording an act the person did
not perform. Within the authorized space, however, a stricter control can
prevent one failure while creating delay or workarounds elsewhere. The relevant
conditions and unknowns must stay visible so that the person can judge the
consequences.

A design earns its place through the consequences it improves, including
whether the person can understand and use it. A workflow that creates more
alternatives than anyone can examine may diminish useful attention. A record
that exposes an unknown that matters can repay its cost. These are situated
assessments, not one universal optimization of speed, control or record volume.
Findings may justify removing a mechanism, refining a method or reconsidering a
prior purpose under its holder's authority.

## 7. Continuity is a relation to outcomes

Sustained work extends beyond what a window currently displays. A conversation
may continue while the view reloads, a request may remain outstanding, and a
command may have changed a file before its response was lost. After an
interruption, the practical question is what happened and what can safely
happen next.

Retaining a transcript helps, but does not answer every part of that question.
An intention recorded in text is not an applied operation. A write attempt is
not a received acknowledgment. A completed primary turn does not establish that
every descendant or process has stopped. Recovery needs access to the relevant
source of each fact and a way to preserve unknown outcomes.

App v4's process placement responds to this concern. The Rust host owns
supplier communication, records, file writes and human-act capture. The web
view presents and submits what the person initiates. Record and trial ticks now
run in their own host loops, and the periodic status read writes no record. So
closing observation is not designed to be the event that decides whether
recording continues.[A5][I4]

### 7.1 A counterexample supplied by the running application

In the first native witness, the person interrupted a turn running `sleep 90`.
The App observed the turn ending as interrupted, while the command had no live
completion item. After Codex was restarted, supplier history reported that the
command had completed with exit zero and a duration of approximately ninety
seconds.[O1]

In this configuration, ending the turn did not establish that its work had
stopped. The distinction mattered to what the person could safely do next.

The App's display retained the live observation and later history separately.
Its label did not claim that the command had been prevented from completing.
The observation also showed a usability limit: nothing had told the person that
the command continued. Correctly bounded data can still leave the person
without the practical understanding they need. This result challenges both how
interruption is represented and the recovery method built around it. The next
inquiry concerns the actual process outcome and what the person needs to see
before retrying. A label that accurately records the turn alone is not enough
for that purpose.

## 8. Native capability and the application's contribution

A general harness already embodies substantial work in tool use, interruption,
questions, planning and delegation. Recreating those capabilities inside a
generic abstraction can discard useful behaviour and create a second system to
maintain. It can also hide distinctions the supplier actually exposes.

The v4 architecture instead selects a stock, pinned supplier through its native
embedding interface. It preserves native items and presents them with their
source meanings. Chirality owns workflow use, the person–agent relationship,
host integration and the records needed for its particular acts and recovery.
The distinction identifies where the App contributes value and where it should
depend on capable existing means.[A5]

This is a design choice with costs. Native integration requires keeping up with
supplier changes and can tie useful interactions to a particular protocol.
Different suppliers may support different activities. Avoiding a generic
vocabulary does not remove the need for interpretation in the display: the
application still decides what to emphasize and how to expose a limitation.

Earlier supplier-host repairs combined several changes, so their outcomes do
not single out topology as the cause. Native hosting must be judged by
maintained functionality and total cost.[A5]

## 9. Re-derivation carries learning, not merely requirements

The App's successive implementations raise a question larger than version
management. What should persist when capabilities, experience and the intended
product have changed enough to justify another architecture?

Existing code carries both useful learning and contingent choices. A PRD can
help identify the commitments that should survive, but it cannot express every
interaction or failure discovered in use. So re-derivation requires a
relationship among current purpose, requirements, source, observations and
owner interpretation. It is not compilation from a complete specification.

V4 preserves the core activity of developing methods through conversation. It
also identifies earlier request cards, plan views, registration, attachment
handling and recovery rules as candidates for reuse. At the same time, it
rejects the old separate Runtime/socket topology and generic supplier-event
translation. These choices concern how to preserve useful experience while
replacing means that no longer fit the product's direction.[A5]

A rewrite can fail that purpose: it can discard subtle repairs, recreate
familiar defects or make a clean design less usable than its predecessor. So
the relevant achievement is retaining and improving useful behaviour, not the
speed with which a new codebase appears.

The native witness again gives a small example. Identifier fields were being
autocorrected, and role headers accumulated when conversations changed. Those
defects were found by operating the actual App. The source now uses exact-text
input attributes and a conversation-specific role-header key. The observation
records that the repairs had automated checks but had not themselves been
witnessed natively.[O1][I5]

An incorrect identifier or misleading role display can defeat the activity
before the wider framework becomes relevant. Experience must stay able to
correct the application at every scale.

## 10. Proliferation through particular applications

The App can demonstrate a way of making methods and using agents without
becoming the authority over every domain in which the method is used. This
limit is essential to proliferation. A piping application knows about models,
loads, cases and results; a different professional application will have
different objects and consequences. A generic agent vocabulary cannot replace
those meanings.

What can transfer is a set of useful relationships: methods with identifiable
sources, agent access to meaningful operations, visible limits of perception,
common validation, attributable human acts and recoverable outcomes. Each host
must supply the domain interpretation, actual operation and appropriate
authority policy. A host can adopt shared types or components where they serve
those responsibilities, without adopting a central executable service.[A3][A5]

SWBPIPE is a demanding next instance because meaningful operation cannot be
separated from engineering and numerical meaning. A successful tool call is
weak evidence if the model it changes no longer represents the intended
physical arrangement. A persuasive explanation cannot make up for incorrect
solver inputs. The host must connect perception, change and result to its
domain engine, while the professional remains responsible for reliance.

This proliferation could fail in several ways. Host-specific adapters may
require so much work that shared contracts provide little economic benefit. The
catalog may be too generic to express operations that matter, or too detailed
for agents and people to use. Recording human acts may become an administrative
burden. A common interface may hide differences that should remain explicit.
Transfer may depend so heavily on the originating owner's translation that
others cannot reproduce it.

A complete activity across the App and SWBPIPE remains to be demonstrated.[A3]
Its usefulness and the effort needed to add another operation will establish
more than counts of exposed tools or shared schemas.

## 11. Discussion: what the case supports

The [examination account][A6] distinguishes verification of a candidate from
validation through realistic use. Host operation validation has a narrower
meaning: it examines whether a proposed operation meets its defined conditions.
Implementation verification examines whether software performs its specified
behaviour. Neither establishes that the method fits an undertaking, that an
engineering idealization applies, or that a person has accepted reliance. Those
questions need their own subjects and grounds. Source inspection and constructed
tests leave several native-use questions open.

The owner remains the principal practitioner and architectural author. That
provides sustained purpose and unusually direct correction, but it limits
claims about transfer. Another person may not share the vocabulary, infer the
same boundaries or tolerate the same amount of operational detail. An interface
that works through its author's continuing interpretation can still be
incomplete as a product.

There is also a risk of rebuilding the administrative burden that Root has
removed. Product records are justified where they preserve meaningful acts,
identify uncertain outcomes or make recovery possible. They become less useful
when the person must maintain representations of facts the application already
knows. Removing a separate registration-attempt journal in the current
implementation, and using existing records and a liveness lock instead,
illustrates that implementation can be simplified while preserving a recovery
question.[A4]

So useful evaluation would examine both outcomes and costs. Can a person make
and improve a method without continual explanation from the developer? Does an
interruption leave them able to decide how to continue? Can a host operation be
added without duplicating its meaning across interfaces? Do the records expose
uncertainty that matters, or merely increase the amount to read? Such
observations would strengthen or qualify the design hypotheses.

## 12. Conclusion

General capability becomes application capability through a relationship to
what the application means and does. Accessible objects, useful operations and
inspectable consequences let agents carry work forward while the person's
judgment continues to shape its purpose.

Workflow authoring makes the means of work available for examination. A method
can develop through conversation, be tried in an identified form and change
through its effects. Reuse carries that learning into other work without
determining that work in advance.

The approach can proliferate where it serves a host's own objects and
practices. SWBPIPE tests it against engineering meaning and numerical
consequences. Success depends on how well people can use and revise those
means, including what they cost in attention, effort and control. The
evaluative findings must return to operative design and, where justified, to
the normative purposes it serves. The [shared conclusion][S3] develops that
continuing relationship across the three views.

## Source basis and reading

Implementation and observations are examined at
`a602024416ace9652f61bb2043889c307fd4e09d`. Tests were inspected rather than
rerun. Product requirements retain
their authority. App v4's frozen foundation is unchanged.

- **R1:** [Root thesis: A Generative Environment for Human–Agent Work][R1].
- **R2:** [The Chirality Framework][R2], especially knowledge, reckoning and
  judgment, the four perspectives and control costs.
- **D1:** [Shared conjecture][D1], preserved argument and definitions.
- **A1:** [App v4 PRD][A1], §§1–4: purpose, exemplar, roles, methods and host
  expressions. These are product commitments, not delivery evidence.
- **A2:** [Workflow workspace and registration design][A2], §§4.2, 5.5, 6,
  11 and 17: trial meaning, host placement and current implementation account.
- **A3:** [Host integration][A3], §§2–7: catalog, perception, changes,
  human acts and autonomy; §§8–9: connecting responsibilities and limits.
- **A4:** [App implementation account][A4], current path and storage/remaining
  work: useful source overview with explicitly unfinished witnesses.
- **A5:** [Architecture basis][A5], §§1–5: priorities, native hosting,
  process placement, reuse and shared responsibilities.
- **A6:** [Examination][A6], §§1–3: verification, validation and evidence limits.
- **I1:** [Trial implementation][I1] and [trial tests][I1T]: snapshot and
  registered-run text comparison. The tests were inspected, not rerun here.
- **I2:** [Trial flows][I2]: preparation, send, linking, fidelity and bring-back;
  delegation availability explicitly remains unestablished by live reads.
- **I3:** [Native request handling][I3]: request-specific answers, permission
  subsets and refusal of an App-rule affirmative origin.
- **I4:** [Host ticks][I4] and [host entry points][I4B]: autonomous observation
  loops and read-only status. [Stop-record tests][I4T] examine intent,
  acknowledgment, observed termination and reopening through constructed cases.
- **I5:** [Exact-text fields][I5] and [conversation presentation][I5B]: repairs
  corresponding to the first native witness's input and role-header defects.
- **O1:** [First native App witness, 10 October 2026][O1]: one development
  build and supplier configuration; observations, defects and explicit exclusions.

[R1]: ../../../../docs/thesis/README.md
[R2]: ../../../../docs/thesis/CHIRALITY_FRAMEWORK.md
[D1]: appendix_d_framework_s.md
[A1]: ../PRD.md
[A2]: ../../execution/PKG-02/DEL-02-02/Work/WORKSPACE_AND_REGISTRATION.md
[A3]: ../HOST_INTEGRATION.md
[A4]: ../../app/README.md
[A5]: ../ARCHITECTURE.md
[A6]: ../EXAMINATION.md
[I1]: ../../app/src-tauri/src/workflow_trials.rs
[I1T]: ../../app/src-tauri/src/workflow_trials_tests.rs
[I2]: ../../app/src-tauri/src/trial_flows.rs
[I3]: ../../app/src-tauri/src/native_requests.rs
[I4]: ../../app/src-tauri/src/host_tick.rs
[I4B]: ../../app/src-tauri/src/lib.rs
[I4T]: ../../app/src-tauri/src/stop_records_host_tests.rs
[I5]: ../../app/src/exactText.ts
[I5B]: ../../app/src/App.tsx
[O1]: ../../execution/PKG-01/DEL-01-02/Work/NATIVE_WITNESS_2026-10-10.md

[S1]: ../../../../docs/thesis/INTRODUCTION.md
[S2]: ../../../../docs/thesis/WORKED_EXAMPLE.md
[S3]: ../../../../docs/thesis/CONCLUSION.md
